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

import type {
  Cycle, DqdvSeries, DvdqSeries, FitParameter, ProfileSeries, SpectrumPoints,
} from './types'

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
/** 아직 끝나지 않은 곡선인가.
 *
 *  붙여 넣은 워크시트에는 표시를 붙일 자리가 없다 -- 위 '숫자만' 규칙이 그
 *  이유고, 그 규칙 자체는 옳다.  그래서 **구동 중인 셀의 잘린 마지막 곡선은
 *  복사하지 않는다.**  Origin 안에서는 완료 곡선과 구분되지 않고, 커서로 읽은
 *  마지막 값이 그 사이클의 용량으로 읽힌다 (CLAUDE.md §3: 구동 중인 셀의
 *  마지막 사이클 값은 절대 보고하지 않는다).
 *
 *  정상 종료한 곡선은 다르다.  `no_discharge` 는 "이 프로토콜은 방전을 안
 *  한다" 이고 그 숫자는 최종값이다 -- 뺄 이유가 없다.  이유를 모르는 것(옛
 *  기록, `unknown`)은 뺀다: 모르는 것을 최종값처럼 내보내지 않는다 (§0.4).
 */
export function stillRunning(item: {
  complete?: boolean
  incomplete_reason?: string
}): boolean {
  if (item.complete !== false) return false
  const reason = item.incomplete_reason ?? ''
  return reason === 'truncated' || reason === 'unknown' || reason === ''
}

/** 복사에서 빠지는 곡선 수 -- 화면이 몇 개를 뺐는지 말할 수 있도록. */
export function skippedForCopy(series: ProfileSeries[]): number {
  return series.filter(stillRunning).length
}

export function profileTsv(series: ProfileSeries[]): string {
  series = series.filter((item) => !stillRunning(item))
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

/** 겹쳐 본 사이클 추세를 두 열로 — (사이클, 값) 을 곡선마다 쌓는다.
 *
 * 프로파일·dQ/dV·dV/dQ 와 같은 배치다.  한 워크시트에 넷을 나란히 붙여 넣고
 * 보는 사람이 화면마다 다른 배치를 익힐 이유가 없다.
 *
 * **구동 중인 셀도 여기서는 뺀다.**  마지막 사이클이 잘려 있으면 그 점은
 * 그 셀의 용량이 아니라 "지금까지 넣은 양" 인데 (CLAUDE.md §3), 붙여 넣은
 * 워크시트에는 그렇다고 적을 자리가 없다.  다만 추세는 **점의 나열**이라
 * 마지막 하나만 문제이므로, 곡선을 통째로 버리지 않고 **그 점만** 뺀다.
 * 서버가 이미 완료 사이클만 싣는 경우에는 아무것도 안 빠진다.
 */
export function compareCyclesTsv(
  series: { points: { cycle: number; value: number }[] }[],
): string {
  const cycles: string[] = []
  const values: string[] = []
  for (const item of series) {
    if (!item.points.length) continue
    if (cycles.length) {
      cycles.push(MISSING)
      values.push(MISSING)
    }
    for (const point of item.points) {
      cycles.push(cell(point.cycle))
      values.push(cell(point.value))
    }
  }
  return tsvColumns([cycles, values])
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

/** 곡선마다 제 (x, y) 두 열 — 겹쳐 보려고 고른 것들을 Origin 에서도 가른다.
 *
 *  위 머리말의 "두 열" 규칙은 **한 셀의 여러 사이클**을 두고 쓴 것이다.  그
 *  때는 쌓는 편이 낫다: 곡선이 하나의 데이터셋이 되어 plot 명령 한 번에
 *  그려지고, 어차피 같은 셀이라 색이 같아도 잃는 것이 없다.
 *
 *  비교 화면은 반대다.  거기서 고른 곡선들은 **서로 다른 셀**이고, 서로 다른
 *  것으로 보이는 것이 그 화면의 전부다.  쌓아서 붙이면 Origin 에서 한 색
 *  한 범례가 되어, 화면에서 구분해 놓은 것을 붙여 넣는 순간 도로 잃는다.
 *  그래서 여기서는 곡선마다 두 열이다 — `bodeTsv` 가 이미 같은 배치다.
 *
 *  순서는 서버가 준 그대로 두었다.  서버는 셀 바깥 · 사이클 안쪽으로 도므로
 *  (`analysis.py`: `for sample_id … for number …`) 3·4 번을 고르면 열이
 *  [셀1 3번][셀1 4번][셀2 3번][셀2 4번] 순으로 나온다.
 */
function widePairs<T>(series: T[], pick: (item: T) => [number[], number[]]): string {
  const columns: string[][] = []
  for (const item of series) {
    const [xs, ys] = pick(item)
    // 점이 없는 곡선은 열을 차지하지 않는다.  빈 열 두 개는 Origin 에서
    // 데이터셋 두 개로 잡히고, 그리면 아무것도 없는 범례 항목이 된다.
    if (!xs.length) continue
    columns.push(xs.map(cell), ys.map(cell))
  }
  return columns.length ? tsvColumns(columns) : ''
}

/** 겹쳐 본 사이클 추세 — 곡선마다 (사이클, 값) 두 열. */
export function compareCyclesWideTsv(
  series: { points: { cycle: number; value: number }[] }[],
): string {
  return widePairs(series, (item) => [
    item.points.map((point) => point.cycle),
    item.points.map((point) => point.value),
  ])
}

/** 겹쳐 본 충방전 프로파일 — 곡선마다 (용량, 전압) 두 열.
 *
 *  구동 중이라 잘린 곡선은 여기서도 뺀다 (`profileTsv` 와 같은 이유).
 */
export function profileWideTsv(series: ProfileSeries[]): string {
  return widePairs(series.filter((item) => !stillRunning(item)),
                   (item) => [item.capacity, item.voltage])
}

/** 겹쳐 본 dQ/dV — 곡선마다 (전압, dQ/dV) 두 열. */
export function dqdvWideTsv(series: DqdvSeries[]): string {
  return widePairs(series, (item) => [item.voltage, item.dqdv])
}

/** 겹쳐 본 dV/dQ — 곡선마다 (용량, dV/dQ) 두 열.  x 가 용량인 것에 주의. */
export function dvdqWideTsv(series: DvdqSeries[]): string {
  return widePairs(series, (item) => [item.capacity, item.dvdq])
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

/** 고른 사이클만 남긴다.  `want` 가 null 이면 전부 (지금까지의 동작).
 *
 *  3·4 번만 보려고 골라 놓고 복사했는데 200 사이클이 통째로 나온다는 제보에서
 *  나왔다.  곡선(프로파일·dQ/dV)은 이미 고른 것만 나가는데 사이클 표만 전체라,
 *  **같은 화면에서 두 규칙이 달랐다** — 그 자체가 함정이다.
 *
 *  순서는 `cycles` 쪽을 따른다.  고른 순서(사람이 누른 순서)로 내보내면 3·4 를
 *  거꾸로 누른 사람의 워크시트만 거꾸로 앉는다.
 */
export function onlyCycles<T extends { cycle: number }>(
  cycles: T[], want: readonly number[] | null,
): T[] {
  if (want === null) return cycles
  const keep = new Set(want)
  return cycles.filter((item) => keep.has(item.cycle))
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

// -- 임피던스와 GITT (ADR 0019 · 0020) ---------------------------------------
//
// 위의 세 규칙을 그대로 따른다.  절차서의 마지막 단계가 "Copy to clipboard →
// 엑셀 → Origin" 이므로, 여기서 나오는 것이 그 워크시트에 그대로 들어가야 한다.
//
// 그리고 화면이 Ω 를 Ω·cm² 로 바꿔 그리고 있으면 **여기도 같이 바뀐다**.
// 축에 Ω·cm² 라고 적힌 그림을 보면서 붙여 넣은 열이 Ω 이면, 다른 것을 보고
// 있다는 사실이 워크시트 안에서는 드러나지 않는다 — 두 수의 비가 면적이라
// 소수점 자리만 다른 그럴듯한 수로 앉는다.

/** 임피던스 값 하나를 화면과 같은 단위로. 안 주면 날 것(Ω) 그대로. */
type Scale = (ohm: number) => number

const ohms = (scale?: Scale): Scale => scale ?? ((value) => value)

/** 나이퀴스트: Z′ 와 **−Z″**.
 *
 *  세로축이 −Z″ 인 것은 관례가 아니라 이 그림의 정의다.  허수부를 그대로 내면
 *  붙여 넣은 사람이 Origin 에서 `-col(B)` 를 다시 해야 하고 (절차서가 실제로
 *  그렇게 시킨다), 한 번 잊으면 아크가 아래로 뒤집힌 그림이 나온다.
 */
export function nyquistTsv(spectra: SpectrumPoints[], scale?: Scale): string {
  const z = ohms(scale)
  return stackedXy(spectra.map((item) => [item.z_re.map(z), item.z_im.map((v) => z(-v))]))
}

/** 겹쳐 본 나이퀴스트 — 스펙트럼마다 (Z′, −Z″) 두 열.
 *
 *  비교 화면 것이라 쌓지 않는다 (`widePairs` 머리말).  상세 화면의
 *  `nyquistTsv` 는 그대로 쌓는다 — 거기는 한 스펙트럼이다.
 */
export function nyquistWideTsv(spectra: SpectrumPoints[], scale?: Scale): string {
  const z = ohms(scale)
  return widePairs(spectra, (item) => [item.z_re.map(z), item.z_im.map((v) => z(-v))])
}

/** 겹쳐 본 pseudo-OCV — 기록마다 (용량, 전압) 두 열.
 *
 *  예전에는 이 자리에서 `이름 용량` `이름 전압` 머리글 줄을 함께 냈다.
 *  붙여 넣은 워크시트에서 머리글은 **데이터 첫 행**으로 앉아 도로 잘라내야
 *  하는 것이 되고, 그 규칙은 이 파일 머리말이 이미 정해 둔 것이다.
 */
export function pseudoOcvWideTsv(
  series: { x: number[]; y: number[] }[],
): string {
  return widePairs(series, (item) => [item.x, item.y])
}

/** 보드: 주파수, |Z|, 위상 — 세 열.
 *
 *  여기만 두 열이 아니다.  |Z| 와 위상은 축이 다르므로 쌓으면 한 축에 두
 *  단위가 섞인다.  스펙트럼이 여럿이면 세 열씩 나란히 놓는다.
 */
export function bodeTsv(spectra: SpectrumPoints[], scale?: Scale): string {
  const z = ohms(scale)
  const columns: string[][] = []
  for (const item of spectra) {
    columns.push(item.frequency_hz.map(cell))
    // |Z| 만 나눈다.  주파수는 Hz 고 위상은 무차원이라 면적과 상관이 없다.
    columns.push(item.magnitude.map((value) => cell(z(value))))
    columns.push(item.phase_deg.map(cell))
  }
  return columns.length ? tsvColumns(columns) : ''
}

/** 피팅 파라미터: 이름, 값, 1σ.
 *
 *  여기는 숫자만이 아니라 **이름부터** 나간다.  파라미터 표는 그리는 것이
 *  아니라 읽는 것이고, `R1` 없이 32.02 만 있는 열은 아무것도 아니다.
 *  절차서도 이 블록을 엑셀에 붙인다 ("Error값은 필요 없어 Delete 가능").
 */
export function fitParametersTsv(
  parameters: FitParameter[],
  /** 화면이 쓰는 것과 **같은** 단위로 내보내려고 받는다.  안 주면 날 것 그대로. */
  scale?: {
    value: (parameter: FitParameter, raw: number) => number
    unit: (parameter: FitParameter) => string
  },
): string {
  if (!parameters.length) return ''
  // 미결정 파라미터는 값도 내보내지 않는다.  화면에서는 "못 믿음" 표시가
  // 붙지만 엑셀에 붙은 순간 그 표시가 사라져 확정값처럼 읽힌다 (리뷰 #7) —
  // 추정값을 실측값처럼 내보내지 않는다 (§0.4).  이름은 남는다: 어떤 행이
  // 비었는지가 정보다.
  //
  // **단위가 한 열로 함께 나간다.**  `R2  4.83` 만 붙여 넣으면 그것이 Ω 인지
  // Ω·cm² 인지 워크시트 안에서는 알 길이 없고, 랩에서 주고받는 표는 늘
  // `R2 (ohm)` 처럼 단위를 달고 다닌다.  그리고 화면이 면적으로 나눈 값을
  // 보여 주고 있으면 **그 값 그대로** 나간다 — 보는 수와 붙이는 수가 다르면
  // 어느 쪽이 맞는지 확인하는 데 왕복이 든다.
  return parameters
    .map((p) =>
      p.determined
        ? [p.name,
           cell(scale ? scale.value(p, p.value) : p.value),
           scale ? scale.unit(p) : p.unit,
           cell(p.stderr === null || p.stderr === undefined ? p.stderr
                : scale ? scale.value(p, p.stderr) : p.stderr)].join('\t')
        : [p.name, MISSING, scale ? scale.unit(p) : p.unit, MISSING].join('\t'),
    )
    .join('\n')
}

/** DRT: τ 와 γ.
 *
 *  τ 를 그대로 낸다 — log 를 취하는 것은 그리는 쪽의 선택이고, 로그로 내보내면
 *  워크시트에서 원래 시간을 되돌릴 수 없다.
 */
export function drtTsv(drt: { tau_s: number[]; gamma_ohm: number[] }): string {
  if (!drt.tau_s.length) return ''
  return tsvColumns([drt.tau_s.map(cell), drt.gamma_ohm.map(cell)])
}

/** pOCV: 용량과 전압.  충전과 방전을 `--` 한 줄로 갈라 쌓는다. */
export function pocvTsv(pocv: {
  charge: { capacity_mah: number; voltage_v: number }[]
  discharge: { capacity_mah: number; voltage_v: number }[]
}): string {
  const branches = [pocv.charge, pocv.discharge].filter((b) => b.length)
  return stackedXy(branches.map((branch) => [
    branch.map((point) => point.capacity_mah),
    branch.map((point) => point.voltage_v),
  ]))
}

/** 확산계수: 용량과 D.
 *
 *  **숫자가 나온 점만** 낸다.  가정을 통과하지 못한 펄스를 `--` 로 끼워 넣으면
 *  Origin 에서는 선이 끊긴 자리로만 보이고, 왜 끊겼는지는 화면에만 남는다 —
 *  붙여 넣은 워크시트에서는 측정하지 않은 것과 구분되지 않는다.
 */
export function diffusionTsv(points: {
  capacity_mah: number
  d_cm2_s: number | null
  rest_s?: number | null
  drift_mv?: number | null
}[]): string {
  const usable = points.filter((point) => point.d_cm2_s !== null)
  if (!usable.length) return ''
  // 휴지 길이와 잔여 드리프트는 D 의 증거라 함께 나간다 (ADR 0020, 리뷰
  // #17): 엑셀에 D 만 붙으면 이완이 덜 된 휴지의 D 가 확정값처럼 읽힌다.
  return tsvColumns([
    usable.map((point) => cell(point.capacity_mah)),
    usable.map((point) => cell(point.d_cm2_s)),
    usable.map((point) => cell(point.rest_s ?? null)),
    usable.map((point) => cell(point.drift_mv ?? null)),
  ])
}

/** 몇 개가 빠졌나 — 조용히 빼면 붙여 넣은 사람이 점 수가 다른 것을 못 본다. */
export function skippedDiffusionPoints(points: { d_cm2_s: number | null }[]): number {
  return points.filter((point) => point.d_cm2_s === null).length
}

/** (x, y) 쌍 여럿을 두 열로 쌓는다.  `stackedPairs` 와 같은 배치이되 원본이
 *  `points` 를 들고 있지 않은 것들을 위해. */
function stackedXy(pairs: [number[], number[]][]): string {
  const drawable = pairs.filter(([xs]) => xs.length)
  if (!drawable.length) return ''
  const left: string[] = []
  const right: string[] = []
  for (const [xs, ys] of drawable) {
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
