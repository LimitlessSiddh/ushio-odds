import { expect, test } from '@playwright/test'

const apiBaseUrl = process.env.USHIO_E2E_API_BASE_URL ?? 'http://127.0.0.1:8100'

function minorCurrency(minor: number) {
  const value = BigInt(minor)
  const sign = value < 0n ? '−' : ''
  const digits = (value < 0n ? -value : value).toString().padStart(3, '0')
  return `${sign}CA$${digits.slice(0, -2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}.${digits.slice(-2)}`
}

function basisPoints(value: number) {
  const amount = BigInt(value)
  const sign = amount < 0n ? '−' : ''
  const digits = (amount < 0n ? -amount : amount).toString().padStart(3, '0')
  return `${sign}${digits.slice(0, -2)}.${digits.slice(-2)}%`
}

test.beforeEach(async ({ page }) => {
  await page.goto('/')
  await expect(page.getByRole('heading', { name: 'Odds screen' })).toBeVisible()
  await expect(page.getByText('Fixture replay · no provider observation yet')).toBeVisible()
})

test('saves a selected fixture hedge and retains it after reload', async ({ page }) => {
  await page.locator('button.best').first().click()
  await expect(page.getByText('Minimum outcome profit')).toBeVisible()
  await page.getByRole('button', { name: 'Save calculation' }).click()
  await expect(page.getByRole('heading', { name: 'Saved calculations' })).toBeVisible()
  await expect(page.locator('.card').filter({ hasText: 'Montréal Canadiens vs Toronto Maple Leafs' }).first()).toBeVisible()
  await page.reload()
  await page.locator('.rail nav button').nth(4).click()
  await expect(page.locator('.card').filter({ hasText: 'Montréal Canadiens vs Toronto Maple Leafs' }).first()).toBeVisible()
  await expect(page.getByText('Saved scenarios are calculations, never performance records or accepted bets.')).toBeVisible()
})

test('watchlist add and removal both persist across reload', async ({ page }) => {
  const addResponse = page.waitForResponse(response => response.url().includes('/v1/watchlist') && response.request().method() === 'POST' && response.status() === 200)
  await page.getByRole('button', { name: 'Toggle watchlist' }).first().click()
  await expect((await addResponse).json()).resolves.toMatchObject({ watched: true })
  await page.reload()
  await page.locator('.rail nav button').nth(2).click()
  await expect(page.getByText('Montréal Canadiens / Toronto Maple Leafs')).toBeVisible()
  await page.locator('.rail nav button').nth(0).click()
  const removeResponse = page.waitForResponse(response => response.url().includes('/v1/watchlist') && response.request().method() === 'POST' && response.status() === 200)
  await page.getByRole('button', { name: 'Toggle watchlist' }).first().click()
  await expect((await removeResponse).json()).resolves.toMatchObject({ watched: false })
  await page.reload()
  await page.locator('.rail nav button').nth(2).click()
  await expect(page.getByText('Star an event on the Odds screen to watch it.')).toBeVisible()
})

test('odds grid keeps focus visible, scrolls to rightmost books, and restores the calculator', async ({ page }) => {
  const watch = page.getByRole('button', { name: 'Toggle watchlist' }).first()
  await watch.focus()
  await expect(watch).toBeFocused()
  const didReachRightEdge = await page.locator('.scroll').evaluate((element: HTMLElement) => {
    element.scrollLeft = element.scrollWidth
    return element.scrollLeft + element.clientWidth >= element.scrollWidth
  })
  expect(didReachRightEdge).toBeTruthy()
  await expect(page.getByRole('columnheader', { name: /Rainbet/ })).toBeVisible()
  await page.getByRole('button', { name: 'Minimize calculator' }).click()
  await expect(page.locator('.calculator')).toHaveClass(/minimized/)
  await page.getByRole('button', { name: 'Restore calculator' }).click()
  await expect(page.locator('.calculator')).not.toHaveClass(/minimized/)
})

test('manual ledger correction is append-only, validated, and visible after reload', async ({ page }) => {
  const eventName = `E2E fixture correction ${Date.now()}`
  await page.locator('.rail nav button').nth(3).click()
  await page.getByPlaceholder('Event / matchup').fill(eventName)
  await page.getByPlaceholder('Book A / Book B').fill('Fixture A / Fixture B')
  await page.getByRole('button', { name: 'Save pair' }).click()
  const row = page.getByRole('row', { name: eventName })
  await expect(row).toBeVisible()
  await row.getByRole('button', { name: 'Correct' }).click()
  await expect(page.getByRole('dialog', { name: 'Correct ledger record' })).toBeVisible()
  await page.getByRole('button', { name: 'Append correction' }).click()
  const reason = page.getByPlaceholder('Why this projection needs correction')
  await expect(await reason.evaluate((element: HTMLTextAreaElement) => element.validity.valueMissing)).toBeTruthy()
  await reason.fill('Fixture result settled')
  await page.getByRole('button', { name: 'Append correction' }).click()
  await expect(page.getByRole('dialog')).toBeHidden()
  await page.reload()
  await page.locator('.rail nav button').nth(3).click()
  const reloadedRow = page.getByRole('row', { name: eventName })
  await reloadedRow.getByText(/1 correction/).click()
  await expect(reloadedRow).toContainText('Original')
  await expect(reloadedRow).toContainText('Fixture result settled')
})

test('correction dialog is labelled, focused, and closes with Escape without trapping the keyboard', async ({ page }) => {
  const eventName = `E2E escape ${Date.now()}`
  await page.locator('.rail nav button').nth(3).click()
  await page.getByPlaceholder('Event / matchup').fill(eventName)
  await page.getByPlaceholder('Book A / Book B').fill('Fixture A / Fixture B')
  await page.getByRole('button', { name: 'Save pair' }).click()
  const row = page.getByRole('row', { name: eventName })
  await row.getByRole('button', { name: 'Correct' }).click()
  const dialog = page.getByRole('dialog', { name: 'Correct ledger record' })
  await expect(dialog).toBeVisible()
  await expect(page.getByRole('button', { name: 'Close correction form' })).toBeFocused()
  await page.keyboard.press('Escape')
  await expect(dialog).toBeHidden()
  await page.getByPlaceholder('Event / matchup').focus()
  await expect(page.getByPlaceholder('Event / matchup')).toBeFocused()
})

test('performance headline metrics use the server ledger summary', async ({ page, request }) => {
  const eventName = `E2E summary ${Date.now()}`
  await page.locator('.rail nav button').nth(3).click()
  await page.getByPlaceholder('Event / matchup').fill(eventName)
  await page.getByPlaceholder('Book A / Book B').fill('Fixture A / Fixture B')
  await page.getByRole('button', { name: 'Save pair' }).click()
  const summary: { realised_net_minor: number; roi_basis_points: number; settled_count: number } = await (await request.get(`${apiBaseUrl}/v1/ledger/summary`)).json()
  await expect(page.getByText('Realised net profit').locator('..')).toContainText(minorCurrency(summary.realised_net_minor))
  await expect(page.getByText('ROI on settled stake').locator('..')).toContainText(basisPoints(summary.roi_basis_points))
  await expect(page.getByText('Completed pairs').locator('..')).toContainText(String(summary.settled_count))
})
