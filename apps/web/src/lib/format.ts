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
