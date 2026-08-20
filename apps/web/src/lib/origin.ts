/** Tab-separated blocks that paste straight into Origin.
 *
 * Origin reads a pasted block column by column, taking the first rows as the
 * Long Name and Units of each column when you paste onto the worksheet header.
 * Two things decide whether the graph comes out right:
 *
 * *Missing is `--`, never blank and never zero.*  Curves have different
 * lengths -- every cycle stops at its own capacity -- so a block of column
 * pairs is ragged, and something has to fill the short columns.  A blank cell
 * is read as 0 by some Origin import paths and a literal 0 by all of them, so
 * the curve dives to the origin at its own end.  `--` is Origin's own missing
 * value token and simply ends the line.
 *
 * *Units stay ASCII.*  The screen writes mAh cm⁻² with a real superscript;
 * pasted into a worksheet header that is a font-dependent gamble.  Here the
 * unit is written `mAh/cm2`, which every Origin build reads the same way.
 */

import type { Basis, Branch, Cycle, ProfileSeries } from './types'

/** Origin's missing value. */
export const MISSING = '--'

/** ASCII unit for a capacity basis -- superscripts do not survive a paste. */
export function plainUnit(basis: Basis | string): string {
  switch (basis) {
    case 'mAh/g':
      return 'mAh/g'
    case 'mAh/cm2':
      return 'mAh/cm2'
    case 'mAh/cm3':
      return 'mAh/cm3'
    case '%':
      return '%'
    default:
      return 'mAh'
  }
}

function cell(value: number | null | undefined): string {
  if (value === null || value === undefined || !Number.isFinite(value)) return MISSING
  return String(value)
}

/** Lay columns of differing length side by side, padding with `--`. */
export function tsvColumns(names: string[], units: string[], columns: string[][]): string {
  const depth = columns.reduce((most, column) => Math.max(most, column.length), 0)
  const rows = [names.join('\t'), units.join('\t')]
  for (let row = 0; row < depth; row += 1) {
    rows.push(columns.map((column) => column[row] ?? MISSING).join('\t'))
  }
  return rows.join('\n')
}

const BRANCH_KO: Record<Branch, string> = { charge: '충전', discharge: '방전' }

/** One (capacity, voltage) column pair per drawn curve.
 *
 * This is what is on screen, which is what the plot is for: the series arrive
 * already reduced for drawing (LTTB), so the block matches the picture rather
 * than the 20 MB original.  The CSV and XLSX buttons next to it hand over
 * every logged point.
 */
export function profileTsv(series: ProfileSeries[], basis: Basis | string): string {
  if (!series.length) return ''
  const names: string[] = []
  const units: string[] = []
  const columns: string[][] = []
  for (const item of series) {
    const title = `${item.cycle}번 ${BRANCH_KO[item.branch] ?? item.branch}`
    names.push(`${title} 용량`, `${title} 전압`)
    units.push(plainUnit(item.basis ?? basis), 'V')
    columns.push(item.capacity.map(cell), item.voltage.map(cell))
  }
  return tsvColumns(names, units, columns)
}

/** Two columns: cycle number and one value per complete cycle.
 *
 * One button copies one thing.  A block with eight columns in it is a
 * spreadsheet, not a plot, and picking the two you wanted out of it in Origin
 * is more work than pressing the button again.
 *
 * Incomplete cycles are left out, not blanked.  A running cell's last cycle is
 * cut off mid-step and its capacity is whatever had accumulated -- pasting it
 * would put a point on the plot that drops for no physical reason.
 */
export function cycleColumnTsv(
  cycles: Cycle[],
  name: string,
  unit: string,
  value: (cycle: Cycle) => number | null | undefined,
): string {
  const complete = cycles.filter((cycle) => cycle.complete)
  if (!complete.length) return ''
  return tsvColumns(
    ['사이클', name],
    ['', unit],
    [complete.map((c) => String(c.cycle)), complete.map((c) => cell(value(c)))],
  )
}

/** The cycle-trend curve: discharge capacity in the unit on screen. */
export function dischargeTsv(cycles: Cycle[], basis: Basis | string): string {
  return cycleColumnTsv(cycles, '방전용량', plainUnit(basis), (c) => c.discharge_capacity)
}

/** Coulombic efficiency, per cycle. */
export function efficiencyTsv(cycles: Cycle[]): string {
  return cycleColumnTsv(cycles, '쿨롱효율', '%', (c) => c.coulombic_efficiency)
}


/** Put text on the clipboard, with a path for browsers that refuse the API.
 *
 * `navigator.clipboard` needs a secure context, and the workbench is normally
 * reached over plain http on a lab machine (`http://localhost:5003` is secure,
 * `http://192.168.x.x:5003` from the bench laptop is not).  The hidden
 * textarea and `execCommand` are deprecated and still the only thing that
 * works there.
 */
export async function copyText(text: string): Promise<void> {
  if (navigator.clipboard?.writeText && window.isSecureContext) {
    await navigator.clipboard.writeText(text)
    return
  }
  const area = document.createElement('textarea')
  area.value = text
  // Off-screen rather than hidden: a display:none textarea cannot be selected.
  area.style.position = 'fixed'
  area.style.top = '-1000px'
  area.setAttribute('readonly', 'true')
  document.body.appendChild(area)
  try {
    area.select()
    if (!document.execCommand('copy')) throw new Error('클립보드 복사를 브라우저가 막았습니다')
  } finally {
    document.body.removeChild(area)
  }
}
