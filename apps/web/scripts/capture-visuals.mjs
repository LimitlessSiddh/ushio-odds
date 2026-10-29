import { mkdir } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import { chromium } from 'playwright'

const output = new URL('../../../output/playwright/', import.meta.url)
const outputPath = fileURLToPath(output)
const views = [
  ['1280x720', 1280, 720],
  ['1600x900', 1600, 900],
  ['1024x768', 1024, 768],
  ['390x844', 390, 844],
]
const pages = [['odds', 0], ['arbitrage', 1], ['watchlist', 2], ['performance', 3], ['saved-calculations', 4]]

async function waitForRenderedState(page, theme, pageName) {
  await page.waitForFunction(expectedTheme => document.querySelector('.app')?.getAttribute('data-theme') === expectedTheme, theme)
  if (pageName === 'odds') {
    await page.locator('.table-wrap').waitFor({ state: 'visible' })
    await page.getByText('Fixture replay · no provider key').waitFor({ state: 'visible' })
  } else {
    await page.locator('.page').waitFor({ state: 'visible' })
  }
}

await mkdir(outputPath, { recursive: true })
const browser = await chromium.launch({ headless: true })
try {
  for (const theme of ['dark', 'light']) {
    for (const [label, width, height] of views) {
      const page = await browser.newPage({ viewport: { width, height } })
      await page.addInitScript(expectedTheme => localStorage.setItem('ushio-theme', JSON.stringify(expectedTheme)), theme)
      await page.goto('http://127.0.0.1:5173', { waitUntil: 'networkidle' })
      await waitForRenderedState(page, theme, 'odds')
      for (const [name, index] of pages) {
        if (name !== 'odds') await page.locator('.rail nav button').nth(index).click()
        await waitForRenderedState(page, theme, name)
        await page.screenshot({ path: `${outputPath}current-${theme}-${label}-${name}.png`, fullPage: false })
        if (name !== 'odds') await page.locator('.rail nav button').nth(0).click()
        if (name !== 'odds') await waitForRenderedState(page, theme, 'odds')
      }
      await page.close()
    }
  }
} finally {
  await browser.close()
}
