/** Tab-separated number blocks that paste straight into Origin.
 *
 * Three rules, each one a thing that went wrong in a worksheet:
 *
 * *Numbers only.*  No column names, no unit row.  A pasted header lands in the
 * data rows of an Origin worksheet, where it has to be cut out again before
 * anything will plot -- and whoever pressed the button already knows what they
 * pressed.
 *
 * *Two columns.*  A (capacity, voltage) pair per curve laid out side by side is
 * miserable to plot: Origin has to be told which X belongs to which Y, column
 * by column, and ten curves is twenty columns.  Stacked into two, it is one
 * plot command.
 *
 * *Missing is `--`, never blank and never zero.*  It is Origin's own missing
 * value, and a missing value breaks a line.  That is what lifts the pen between
 * stacked curves instead of flying it back across the plot, and what keeps a
 * cycle with no efficiency from being drawn at zero.
 */

import type { Cycle, DqdvSeries, ProfileSeries } from './types'

/** Origin's missing value. */
export const MISSING = '--'

function cell(value: number | null | undefined): string {
  if (value === null || value === undefined || !Number.isFinite(value)) return MISSING
  return String(value)
}

/** Lay columns side by side, padding the short ones with `--`. */
export function tsvColumns(columns: string[][]): string {
  const depth = columns.reduce((most, column) => Math.max(most, column.length), 0)
  const rows: string[] = []
  for (let row = 0; row < depth; row += 1) {
    rows.push(columns.map((column) => column[row] ?? MISSING).join('\t'))
  }
  return rows.join('\n')
}

/** Every drawn curve stacked into two columns, separated by a `--` row.
 *
 * What this gives up is one dataset per curve, so the curves come out sharing a
 * colour and a legend entry.  To colour them separately the wide layout is what
 * you want, and the profile CSV button next to this one writes exactly that.
 *
 * This copies what is on screen, which is what the plot is for: the series
 * arrive already reduced for drawing (LTTB), so the block matches the picture
 * rather than the 20 MB original.  CSV and XLSX hand over every logged point.
 */
export function profileTsv(series: ProfileSeries[]): string {
  if (!series.length) return ''
  const capacity: string[] = []
  const voltage: string[] = []
  for (const item of series) {
    if (capacity.length) {
      capacity.push(MISSING)
      voltage.push(MISSING)
    }
    for (let i = 0; i < item.capacity.length; i += 1) {
      capacity.push(cell(item.capacity[i]))
      voltage.push(cell(item.voltage[i]))
    }
  }
  return tsvColumns([capacity, voltage])
}

/** Every dQ/dV curve stacked into two columns, separated by a `--` row.
 *
 * Same layout as `profileTsv` for the same reason: somebody comparing a
 * capacity curve against its derivative in one worksheet should not have to
 * learn a second arrangement.
 *
 * Curves that could not be computed are skipped rather than emitted as a
 * lone `--` row.  An empty curve has no points to plot, and a separator with
 * nothing on either side of it is just a gap in the column.
 */
export function dqdvTsv(series: DqdvSeries[]): string {
  const drawable = series.filter((item) => item.points > 0)
  if (!drawable.length) return ''
  const voltage: string[] = []
  const values: string[] = []
  for (const item of drawable) {
    if (voltage.length) {
      voltage.push(MISSING)
      values.push(MISSING)
    }
    for (let i = 0; i < item.voltage.length; i += 1) {
      voltage.push(cell(item.voltage[i]))
      values.push(cell(item.dqdv[i]))
    }
  }
  return tsvColumns([voltage, values])
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
  value: (cycle: Cycle) => number | null | undefined,
): string {
  const complete = cycles.filter((cycle) => cycle.complete)
  if (!complete.length) return ''
  return tsvColumns([complete.map((c) => String(c.cycle)), complete.map((c) => cell(value(c)))])
}

/** The cycle-trend curve: discharge capacity, in whatever unit is on screen. */
export function dischargeTsv(cycles: Cycle[]): string {
  return cycleColumnTsv(cycles, (cycle) => cycle.discharge_capacity)
}

/** Coulombic efficiency, per cycle. */
export function efficiencyTsv(cycles: Cycle[]): string {
  return cycleColumnTsv(cycles, (cycle) => cycle.coulombic_efficiency)
}

/** Put text on the clipboard, with a path for browsers that refuse the API.
 *
 * `navigator.clipboard` needs a secure context, and the workbench is normally
 * reached over plain http on a lab machine (`http://localhost:5003` is secure,
 * `http://192.168.x.x:5003` from the bench laptop is not).  The hidden textarea
 * and `execCommand` are deprecated and still the only thing that works there.
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
