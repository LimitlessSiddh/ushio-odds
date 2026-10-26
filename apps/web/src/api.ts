import type { Board, Hedge } from './types'

const API = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API}${path}`, init)
  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(body.detail || 'Request failed')
  }
  return response.json() as Promise<T>
}

export const getBoard = (sport: string, market: string) => request<Board>(`/v1/odds?sport=${encodeURIComponent(sport)}&market=${encodeURIComponent(market)}`)
export const calculate = (odds: number[], amount: string, mode: 'budget' | 'fixed_first') => request<Hedge>('/v1/calculators/hedge', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ odds, amount, mode }) })
