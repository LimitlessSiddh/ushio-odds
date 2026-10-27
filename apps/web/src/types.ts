export type View = 'grid' | 'arb' | 'watch' | 'performance' | 'journal'
export type Quote = { book: string; prices: number[] }
export type Game = { id: string; sport: string; league: string; away: string; home: string; commence_time: string; market: string; period: string; outcomes: string[]; quotes: Quote[] }
export type Board = { mode: 'fixture' | 'live'; provider: string; region: string; as_of: string; credit_state: { status: string; remaining: number | null }; capabilities: { sports: string[]; markets: string[]; props: string[] }; games: Game[] }
export type Hedge = { stakes: string[]; total_stake: string; profits: string[]; minimum_profit: string; roi_percent: string; is_theoretical_arb: boolean }
export type SavedScenario = { id: string; title: string; createdAt: string; result: Hedge; odds: number[] }
export type PairRecord = { id: string; date: string; event: string; books: string; status: 'settled' | 'open' | 'void'; stake: number; returned: number; fee: number }
export type Opportunity = { event_id: string; event: string; market: string; outcomes: string[]; books: string[]; odds: number[]; minimum_profit: string; roi_percent: string; mode: 'indicative' | 'revalidated' }
