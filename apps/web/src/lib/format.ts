/** Number and unit formatting.
 *
 * Lab readings are compared by eye across rows, so significant figures matter
 * more than decimal places: 207.7 mAh/g and 5.2515 mAh should both read
 * cleanly without either being padded to the other's precision.
 */

export function num(value: number | null | undefined, digits = 4): string {
  if (value === null || value === undefined || !Number.isFinite(value)) return '—'
  const magnitude = Math.abs(value)
  if (magnitude === 0) return '0'
  if (magnitude >= 1000) return value.toFixed(0)
  if (magnitude >= 100) return value.toFixed(Math.max(0, digits - 3))
  if (magnitude >= 10) return value.toFixed(Math.max(0, digits - 2))
  if (magnitude >= 1) return value.toFixed(Math.max(0, digits - 1))
  return value.toPrecision(Math.max(2, digits - 1))
}

/** 사람이 적은 그대로의 수 — 부동소수점 찌꺼기만 턴다.
 *
 * `num()` 과 다르다.  저쪽은 *측정값*을 일정한 유효숫자로 맞추는 것이고,
 * 여기는 "적힌 값을 그대로 보여 준다" 이다.  0.2C 를 "0.20C" 로, 205.9 mAh/g 를
 * "206" 으로 쓰면 사람이 넣지 않은 정밀도가 생기거나 값 자체가 달라진다.
 */
export function plain(value: number | null | undefined): string {
  if (value === null || value === undefined || !Number.isFinite(value)) return '—'
  return String(Number(value.toFixed(6)))
}

export function pct(value: number | null | undefined, digits = 2): string {
  if (value === null || value === undefined || !Number.isFinite(value)) return '—'
  return value.toFixed(digits)
}

export function cycleNumber(value: number | null | undefined): string {
  if (value === null || value === undefined || !Number.isFinite(value)) return '—'
  return Number.isInteger(value) ? String(value) : value.toFixed(1)
}

export function bytes(value: number): string {
  if (value < 1024) return `${value} B`
  if (value < 1024 ** 2) return `${(value / 1024).toFixed(0)} KB`
  if (value < 1024 ** 3) return `${(value / 1024 ** 2).toFixed(1)} MB`
  return `${(value / 1024 ** 3).toFixed(2)} GB`
}

export function dateTime(value: string | null | undefined): string {
  if (!value) return '—'
  const parsed = new Date(value)
  if (Number.isNaN(parsed.getTime())) return value
  const pad = (n: number) => String(n).padStart(2, '0')
  return (
    `${parsed.getFullYear()}-${pad(parsed.getMonth() + 1)}-${pad(parsed.getDate())} ` +
    `${pad(parsed.getHours())}:${pad(parsed.getMinutes())}`
  )
}

export function duration(hours: number | null | undefined): string {
  if (hours === null || hours === undefined || !Number.isFinite(hours)) return '—'
  if (hours < 1) return `${(hours * 60).toFixed(0)}분`
  if (hours < 48) return `${hours.toFixed(1)}시간`
  return `${(hours / 24).toFixed(1)}일`
}

/** The axis title for a capacity basis, with proper superscripts. */
export function basisAxis(basis: string): string {
  switch (basis) {
    case 'mAh/g':
      return '비용량 (mAh g⁻¹)'
    case 'mAh/cm2':
      return '면적용량 (mAh cm⁻²)'
    case 'mAh/cm3':
      return '부피용량 (mAh cm⁻³)'
    case '%':
      return '용량 활용률 (%)'
    default:
      return '용량 (mAh)'
  }
}

export function basisUnit(basis: string): string {
  switch (basis) {
    case 'mAh/g':
      return 'mAh g⁻¹'
    case 'mAh/cm2':
      return 'mAh cm⁻²'
    case 'mAh/cm3':
      return 'mAh cm⁻³'
    case '%':
      return '%'
    default:
      return 'mAh'
  }
}

/** The mass written into a cell's name, in mg.
 *
 * This lab names its files with the electrode mass on the end --
 * `..._4.6V_1_17.5mg`.  That number is the one thing the `.wrd` does not know
 * (ADR 0003), so it has to be typed in by hand; showing what the name says
 * next to the field is how a typo gets caught before every mAh/g is wrong.
 * The last match wins: `..._3.8V_1_18.5mg` has one mass, but a name that
 * mentions two puts the electrode's own last. */
export function massFromName(name: string | null | undefined): number | null {
  if (!name) return null
  let found: number | null = null
  for (const match of name.matchAll(/(\d+(?:\.\d+)?)\s*mg\b/gi)) {
    const value = Number(match[1])
    if (Number.isFinite(value) && value > 0) found = value
  }
  return found
}

/** The part of a cell name shared by its replicates.
 *
 * This lab names cells for what the experiment was, then adds which replicate
 * and how much it weighed: `4.6V_1_17.5mg`, `4.6V_2_18.1mg`.  Those two are
 * the same condition run twice, and grouping them is the question people
 * actually ask of the library — without having to create an experiment group
 * for every condition first.
 *
 * So trailing tokens that identify the *individual cell* come off, and
 * everything that identifies the *condition* stays:
 *
 *     4.6V_1_17.5mg            -> 4.6V
 *     4.0V_post_formation_18.9mg -> 4.0V_post_formation
 *     No_1_dry_011             -> No_1_dry
 *
 * Only trailing tokens are stripped.  `No_1_dry` keeps its `_1` because the
 * `dry` after it says the number is part of the name, not a replicate index —
 * and a rule that reached into the middle would merge `No_1_dry` with
 * `No_2_wet`.
 *
 * A name that strips away to nothing keeps its full self.  Returning "" would
 * put every all-numeric name in one nameless heap.
 */
export function nameFamily(name: string | null | undefined): string {
  if (!name) return ''
  let stem = name.trim()
  // `17.5mg` is the mass, `011` is the file sequence or the replicate index.
  const droppable = /[\s_-]+(?:\d+(?:\.\d+)?\s*mg|\d+)$/i
  while (droppable.test(stem)) {
    stem = stem.replace(droppable, '')
  }
  return stem || name.trim()
}

/** Qualitative palette, ordered so adjacent series stay distinguishable and
 *  no pair collides under the common forms of colour blindness. */
export const SERIES_COLORS = [
  '#1d4ed8', '#ea580c', '#059669', '#7c3aed', '#db2777',
  '#0891b2', '#ca8a04', '#4b5563', '#2563eb', '#e11d48',
  '#15803d', '#b45309', '#6d28d9', '#0e7490', '#9f1239',
]

export function seriesColor(index: number): string {
  return SERIES_COLORS[index % SERIES_COLORS.length] as string
}

/** A cycle-number spec like `1,3,10-20` expanded to numbers. */
export function parseCycleSpec(spec: string, available: number[]): number[] {
  const trimmed = spec.trim().toLowerCase()
  if (!trimmed || trimmed === 'all' || trimmed === '전체') return available
  const wanted = new Set<number>()
  for (const part of trimmed.split(',')) {
    const piece = part.trim()
    if (!piece) continue
    if (piece.includes('-')) {
      const [from, to] = piece.split('-', 2).map((v) => Number.parseInt(v, 10))
      if (Number.isFinite(from) && Number.isFinite(to)) {
        for (let n = Math.min(from!, to!); n <= Math.max(from!, to!); n += 1) wanted.add(n)
      }
    } else {
      const value = Number.parseInt(piece, 10)
      if (Number.isFinite(value)) wanted.add(value)
    }
  }
  return available.filter((n) => wanted.has(n))
}

/** Evenly spaced picks from a list — "show me 8 cycles across the run". */
export function spread(values: number[], count: number): number[] {
  if (values.length <= count) return values
  const picks: number[] = []
  for (let i = 0; i < count; i += 1) {
    const index = Math.round((i * (values.length - 1)) / (count - 1))
    const value = values[index]
    if (value !== undefined && !picks.includes(value)) picks.push(value)
  }
  return picks
}
