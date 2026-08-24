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

import type { Cycle, DqdvSeries, DvdqSeries, ProfileSeries } from './types'

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
  return stackedPairs(series, (item) => [item.voltage, item.dqdv])
}

/** Every dV/dQ curve stacked into two columns, separated by a `--` row.
 *
 * The same shape as `dqdvTsv`, because the two are pasted into the same
 * worksheet and read side by side.  Note which column is which: here the
 * **capacity** is the x axis, so the first column is capacity and the second
 * is V per capacity — the mirror of dQ/dV, and the one thing somebody
 * copy-pasting between the two would get wrong.
 */
export function dvdqTsv(series: DvdqSeries[]): string {
  return stackedPairs(series, (item) => [item.capacity, item.dvdq])
}

/** Stack `(x, y)` pairs from many curves into two columns with `--` between.
 *
 * Curves that could not be computed are skipped rather than emitted as a lone
 * `--` row: an empty curve has no points to plot, and a separator with nothing
 * on either side of it is just a gap in the column.
 */
function stackedPairs<T extends { points: number }>(
  series: T[],
  pick: (item: T) => [number[], number[]],
): string {
  const drawable = series.filter((item) => item.points > 0)
  if (!drawable.length) return ''
  const left: string[] = []
  const right: string[] = []
  for (const item of drawable) {
    const [xs, ys] = pick(item)
    if (left.length) {
      left.push(MISSING)
      right.push(MISSING)
    }
    for (let i = 0; i < xs.length; i += 1) {
      left.push(cell(xs[i]))
      right.push(cell(ys[i]))
    }
  }
  return tsvColumns([left, right])
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

/** Three columns at once: cycle number, discharge capacity, coulombic efficiency.
 *
 * The rule above -- one button copies one thing -- holds when the two things
 * go to different plots.  These two go to the *same* one: capacity fade with
 * efficiency on the second axis is the figure people actually draw.  Copying
 * them separately means pasting twice and lining the cycle numbers up by hand,
 * and the two blocks can disagree in length the moment a cycle is incomplete.
 *
 * Same rule as the two-column blocks: only complete cycles, and a value that
 * is missing comes out as an empty cell rather than a zero.
 */
export function cycleAndEfficiencyTsv(cycles: Cycle[]): string {
  const complete = cycles.filter((cycle) => cycle.complete)
  if (!complete.length) return ''
  return tsvColumns([
    complete.map((c) => String(c.cycle)),
    complete.map((c) => cell(c.discharge_capacity)),
    complete.map((c) => cell(c.coulombic_efficiency)),
  ])
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
