import type { Board, Hedge, LedgerCorrection, LedgerSnapshot, Opportunity, PairRecord, SavedScenario } from './types'

const API = import.meta.env.VITE_API_BASE_URL || `${window.location.protocol}//${window.location.hostname}:8000`

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API}${path}`, init)
  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(body.detail || 'Request failed')
  }
  return response.json() as Promise<T>
}

export const getBoard = (sport: string, market: string) => request<Board>(`/v1/odds?sport=${encodeURIComponent(sport)}&market=${encodeURIComponent(market)}`)
export const getOpportunities = (sport: string, market: string) => request<{ mode: string; provider: string; opportunities: Opportunity[] }>(`/v1/opportunities?sport=${encodeURIComponent(sport)}&market=${encodeURIComponent(market)}`)
export const calculate = (odds: number[], amount: string, mode: 'budget' | 'fixed_first') => request<Hedge>('/v1/calculators/hedge', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ odds, amount, mode }) })
export const refreshProviderBoard = (sport: string, market: string) => request<Board>('/v1/provider/refresh', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ sport, market }) })
export const getWatchlist = () => request<string[]>('/v1/watchlist')
export const toggleWatchlist = (eventId: string) => request<{ event_id: string; watched: boolean }>('/v1/watchlist', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ event_id: eventId }) })
export const getSaved = () => request<Array<{ id: string; title: string; payload: Omit<SavedScenario, 'id' | 'title' | 'createdAt'>; created_at: string }>>('/v1/saved-calculations')
export const createSaved = (title: string, payload: Omit<SavedScenario, 'id' | 'title' | 'createdAt'>) => request<{ id: string; title: string; created_at: string }>('/v1/saved-calculations', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ title, payload }) })
export const getLedger = () => request<Array<{ id: string; occurred_on: string; event_name: string; books: string; status: PairRecord['status']; total_stake: string; returned: string; fees: string; correction_count: number; original: LedgerSnapshot }>>('/v1/ledger')
export const getLedgerCorrections = (recordId: string) => request<LedgerCorrection[]>(`/v1/ledger/${encodeURIComponent(recordId)}/corrections`)
export const createLedgerCorrection = (recordId: string, data: { reason: string; status: PairRecord['status']; total_stake: string; returned: string; fees: string }) => request<{ id: string }>(`/v1/ledger/${encodeURIComponent(recordId)}/corrections`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
export const createLedger = (record: Omit<PairRecord, 'id' | 'date' | 'event' | 'stake' | 'fee'> & { date: string; event: string; stake: number; fee: number }) => request<{ id: string }>('/v1/ledger', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ occurred_on: record.date, event_name: record.event, books: record.books, status: record.status, total_stake: record.stake.toFixed(2), returned: record.returned.toFixed(2), fees: record.fee.toFixed(2) }) })
