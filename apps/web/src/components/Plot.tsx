/** uPlot wrapper.
 *
 * uPlot is imperative, so this is the one place that talks to it.  Series are
 * given as independent (x, y) pairs because charge and discharge branches do
 * not share an x grid -- uPlot wants one shared x, so each series is aligned
 * onto a merged, sorted x axis with nulls where it has no sample.
 */

import { useEffect, useMemo, useRef, useState } from 'react'
import uPlot from 'uplot'
import 'uplot/dist/uPlot.min.css'

import { useElementWidth } from '../lib/hooks'
import { arcWindow } from '../lib/eis'
import { num, SERIES_COLORS, seriesColor } from '../lib/format'

export interface PlotSeries {
  label: string
  x: number[]
  y: number[]
  color?: string
  dash?: number[]
  width?: number
  points?: boolean
  hidden?: boolean
  /** 숫자가 안 나오는 곡선 (잘렸거나 한쪽 브랜치가 없다).
   *
   *  선 굵기만으로 가르면 정적 캡처에서 사라진다 -- 1.0px 과 1.6px 은 인쇄물이나
   *  스크린샷에서 구분되지 않고, 범례 색칠에는 굵기가 아예 반영되지 않았다.
   *  이 표시가 범례 조각과 접힌 범례의 안내까지 따라간다. */
  partial?: boolean
  /** Draw across x positions this series has no sample at.  Defaults to true. */
  spanGaps?: boolean
  /** 범례에만 붙는 회색 꼬리표 — 그룹 · 소그룹처럼 **곡선을 고르는 데 쓰지만
   *  곡선의 이름은 아닌** 것.
   *
   *  이름에 이어 붙이지 않는 이유는 이름이 곧 열쇠이기 때문이다: 범례 조각의
   *  `key` 이자 숨김 목록의 값이라, 그룹을 바꿔 다시 그리면 숨겨 둔 곡선이
   *  도로 켜진다.  툴팁도 이름으로 자리를 잡으므로 거기까지 길어진다. */
  note?: string
}

export interface PlotMarker {
  x: number
  label: string
  color?: string
  /** 확정이 아닌 후보.  같은 굵기로 그리면 확정과 구분이 안 된다. */
  tentative?: boolean
}

interface Props {
  series: PlotSeries[]
  xLabel: string
  yLabel: string
  height?: number
  markers?: PlotMarker[]
  yRange?: [number | null, number | null]
  xRange?: [number | null, number | null]
  legend?: boolean
  /** 커서 팝업에 한 줄 더.  지금 가리키는 x 가 무엇을 뜻하는지.
   *
   *  DRT 의 τ 처럼 **좌표 자체가 물리를 말하는** 축이 있다.  숫자만 읽어 주면
   *  사람이 매번 머릿속에서 τ → 주파수 → 그 시간대의 현상을 되짚어야 한다.
   *  판정이 아니라 관례적인 구간 이름이므로, 부르는 쪽이 그렇게 적는다. */
  describeX?: (x: number) => string | null
  /** 가로 눈금에 적을 글자.  **좌표와 눈금이 다른 축**에 쓴다.
   *
   *  DRT 를 주파수로 볼 때가 그렇다: 좌표는 `log₁₀ f` 여야 (그래야 여섯 자리가
   *  고르게 퍼진다) 하는데, 사람이 읽어야 하는 것은 `2` 가 아니라 `10²` 이다.
   *  숫자를 그대로 두면 눈금이 지수라는 사실이 축 이름에만 남는다. */
  xTick?: (value: number) => string
  /** 가로 눈금을 어디에 놓을까.  `xTick` 과 짝이다 — 자릿수 눈금을 쓰려면
   *  눈금이 정수 자리에 떨어져야 `10^0.7` 같은 것이 안 나온다. */
  xSplits?: (min: number, max: number) => number[]
  /** "y ≥ 0" 버튼을 붙인다 (나이퀴스트).
   *
   *  임피던스는 고주파 끝에서 −Z″ 가 음수로 내려간다 (측정선의 인덕턴스).
   *  그 꼬리 때문에 세로축이 아래로 늘어나면 정작 보려던 아크가 위쪽 절반에
   *  눌려 납작해진다.  누르면 −Z″ ≥ 0 인 점들에만 화면을 맞춘다. */
  positiveFit?: boolean
  /** 두 축의 한 단위를 화면에서 같은 길이로 (나이퀴스트).
   *
   *  반원이 반원으로 보여야 한다.  세로가 눌리면 찌그러진 아크(CPE 지수가 낮은
   *  것)와 이상적인 반원이 화면에서 구분되지 않고, 사람이 회로를 고를 때 보는
   *  것이 바로 그 차이다.  가로 범위는 데이터가 정하고, 세로는 그 범위에
   *  그림 비율을 곱해 맞춘다 — 반대로 하면 아크의 폭이 화면 밖으로 나간다. */
  equalAspect?: boolean
  /** 지금 서버에서 다시 받아오는 중인가.
   *
   *  고른 것을 바꾸면 새 곡선이 올 때까지 **옛 곡선이 그대로 서 있다**
   *  (`useAsync` 가 재요청 중 옛 값을 지키는 것은 옳다 — 그림을 비우면 화면이
   *  깜빡이고 축이 튄다).  그런데 그러면 화면이 눌린 것을 못 알아들은 것처럼
   *  보이고, 사람은 같은 것을 한 번 더 누른다.  돌아가는 표시 하나면 갈린다. */
  busy?: boolean
}

/** Merge every series' x values into one sorted, de-duplicated axis.
 *
 * Voltage-vs-capacity branches never share an x grid -- every cycle stops at
 * its own capacity, and the samples land wherever the cycler logged them.  On
 * the merged axis each series is therefore mostly nulls, which is why series
 * default to spanning their gaps: joining a series' own points in x order
 * reproduces its curve exactly, while `spanGaps: false` would leave each
 * sample as an isolated dot.
 */
function mergeX(series: PlotSeries[]): number[] {
  const all = new Set<number>()
  for (const item of series) for (const value of item.x) all.add(value)
  return [...all].sort((a, b) => a - b)
}

/** Place a series' y values onto the merged axis, null where it has no sample. */
function alignY(item: PlotSeries, axis: number[]): (number | null)[] {
  const lookup = new Map<number, number>()
  for (let i = 0; i < item.x.length; i += 1) {
    const key = item.x[i]
    const value = item.y[i]
    if (key !== undefined && value !== undefined) lookup.set(key, value)
  }
  return axis.map((value) => lookup.get(value) ?? null)
}

function cssVar(name: string, fallback: string): string {
  if (typeof window === 'undefined') return fallback
  const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim()
  return value || fallback
}

/** Resolve `var(--token)` to a real colour.
 *
 * uPlot strokes a canvas, and a canvas has no cascade: handing it
 * `var(--discharge)` silently produces an invisible line.  Series colours are
 * therefore resolved here rather than at the call site, so a caller can use a
 * theme token like everywhere else in the app. */
function resolveColor(color: string | undefined, fallback: string): string {
  if (!color) return fallback
  const token = color.match(/^var\(\s*(--[\w-]+)\s*(?:,\s*(.+?))?\s*\)$/)
  if (!token) return color
  return cssVar(token[1]!, token[2]?.trim() ?? fallback)
}

/** Express a qualitative-palette colour as its theme token.
 *
 * `SERIES_COLORS` is a light-mode-only constant and callers hand its literal
 * hex straight in as `series.color`, so on the dark surface the grey and the
 * deep blues fall to about 2.4:1 -- below the 3:1 a line needs to be seen.
 * The palette slot is recovered here and rewritten as `var(--series-N, <hex>)`,
 * which app.css themes the way it themes --charge/--discharge; the literal hex
 * stays as the fallback, and a colour that is not from the palette (a caller's
 * own token or a one-off) is passed through untouched. */
function seriesToken(color: string | undefined, index: number): string {
  const slot = color
    ? SERIES_COLORS.indexOf(color.trim().toLowerCase())
    : index % SERIES_COLORS.length
  if (slot < 0) return color as string
  return `var(--series-${slot}, ${SERIES_COLORS[slot]})`
}

/** Axis, grid and label-plate colours, re-read when the OS scheme flips.
 *
 * uPlot bakes colours into canvas draw calls and a canvas has no cascade, so
 * unlike the rest of the app a plot cannot inherit a token change: it has to be
 * told, and rebuilt.  Without this a page left open across a light/dark switch
 * kept the old scheme's axes until the data happened to change. */
function readChartColors() {
  return {
    text: cssVar('--ink-3', '#7d8797'),
    grid: cssVar('--line', '#e5e7eb'),
    warn: cssVar('--warn', '#b54708'),
    surface: cssVar('--surface', '#ffffff'),
  }
}

function useChartColors(): ReturnType<typeof readChartColors> {
  const [colors, setColors] = useState(readChartColors)
  useEffect(() => {
    const query = window.matchMedia?.('(prefers-color-scheme: dark)')
    if (!query?.addEventListener) return
    const onChange = () => setColors(readChartColors())
    query.addEventListener('change', onChange)
    return () => query.removeEventListener('change', onChange)
  }, [])
  return colors
}

/** Split `"면적용량 (mAh cm⁻²)"` into its name and its unit.
 *
 * The axis label already carries the unit, and the cursor readout has to show
 * the same one -- a bare number next to a crosshair is the one thing that gets
 * copied into a slide with the wrong unit attached. */
export function splitAxisLabel(label: string): { name: string; unit: string } {
  const parts = label.match(/^(.*?)\s*\(([^()]*)\)\s*$/)
  if (!parts) return { name: label.trim(), unit: '' }
  return { name: (parts[1] ?? '').trim(), unit: (parts[2] ?? '').trim() }
}

/** One column of uPlot's aligned data -- a plain array or a typed array. */
type PlotColumn = { readonly length: number; readonly [index: number]: number | null | undefined }

/** The nearest real sample of one series to a merged-axis index.
 *
 * On the merged axis a series is mostly nulls (see `mergeX`), so the index the
 * cursor lands on usually has no value for the series under the mouse.  The
 * search walks outward and reports that sample's own x, so the pair shown in
 * the readout is a measurement that exists rather than a point interpolated
 * along the drawn line. */
export function pointAt(
  data: ArrayLike<PlotColumn>,
  seriesIdx: number,
  idx: number,
): { x: number; y: number } | null {
  const xs = data[0]
  const ys = data[seriesIdx]
  if (!xs || !ys) return null
  const take = (i: number) => {
    if (i < 0 || i >= ys.length) return null
    const y = ys[i]
    const x = xs[i]
    if (y === null || y === undefined || x === null || x === undefined) return null
    if (!Number.isFinite(y) || !Number.isFinite(x)) return null
    return { x, y }
  }
  // A series with no sample anywhere near would otherwise scan the whole axis
  // on every mouse move; 4000 indices is far past what any eye is aiming at.
  const LIMIT = 4000
  for (let step = 0; step <= LIMIT; step += 1) {
    const before = idx - step
    const after = idx + step
    if (before < 0 && after >= ys.length) break
    const hit = take(before) ?? (step === 0 ? null : take(after))
    if (hit) return hit
  }
  return null
}

/** What the cursor is pointing at, in plot pixels and in data units. */
interface Readout {
  left: number
  top: number
  /** Draw to the left of the cursor -- there is no room on the right. */
  flip: boolean
  label: string | null
  color: string | null
  x: number
  y: number | null
}

/** Keep the tip clear of the cursor itself. */
const TIP_GAP = 14
/** Roughly how wide the tip gets; used only to decide which side to flip to. */
const TIP_WIDTH = 150

const AXIS_FONT = '11px Pretendard, system-ui, sans-serif'
const LABEL_FONT = '600 11px Pretendard, system-ui, sans-serif'

/** What the plot looked like when it was built -- the view 초기화 goes back to.
 *
 * Recomputing "the whole data range" instead would land somewhere slightly
 * different: uPlot pads a y scale by 10 % and snaps tick-friendly bounds, and
 * an axis lock overrides both.  Capturing the scales uPlot actually settled on
 * makes 초기화 exact by construction -- it *is* the first view, not a
 * reconstruction of it. */
type HomeScales = Record<string, { min: number; max: number }>

function readScales(plot: uPlot): HomeScales {
  const home: HomeScales = {}
  for (const key of Object.keys(plot.scales)) {
    const scale = plot.scales[key]
    // A derived scale (`from`) follows its parent; setting it directly fights
    // uPlot rather than moving the view.
    if (!scale || scale.from != null) continue
    if (typeof scale.min !== 'number' || typeof scale.max !== 'number') continue
    if (!Number.isFinite(scale.min) || !Number.isFinite(scale.max)) continue
    home[key] = { min: scale.min, max: scale.max }
  }
  return home
}

/** Is the view still where it started?
 *
 * Compared against the span rather than absolutely: dV/dQ runs at 1e-9 and
 * capacity at 1e2, so any fixed epsilon is wrong for one of them.  The
 * tolerance is loose enough that uPlot's own float round-trips do not read as
 * a zoom, which would leave 초기화 lit on a plot nobody touched.
 */
/** 같은 단위/픽셀을 두 축 모두에 (리뷰 W3).
 *
 *  나이퀴스트의 45° 는 기울기가 물리다.  전에는 y 만 x 의 단위/픽셀에
 *  맞춰 **넓혔는데**, y 의 데이터 폭이 이미 그보다 크면 아무것도 하지 않아
 *  두 축의 단위/픽셀이 달랐다 — Warburg 꼬리가 화면 비율에 따라 눕거나
 *  섰다.  둘 중 성긴 쪽(단위/픽셀이 큰 쪽)에 다른 쪽을 맞춰 넓힌다;
 *  좁히는 일은 없으므로 데이터가 잘리지 않는다. */
export function equalAspectRanges(
  x: [number, number],
  y: [number, number],
  width: number,
  height: number,
): { x: [number, number]; y: [number, number] } {
  const safeWidth = Math.max(width, 1)
  const safeHeight = Math.max(height, 1)
  const xPerPx = (x[1] - x[0]) / safeWidth
  const yPerPx = (y[1] - y[0]) / safeHeight
  const perPx = Math.max(xPerPx, yPerPx, 0)
  if (perPx <= 0) return { x, y }
  const xCentre = (x[0] + x[1]) / 2
  const yCentre = (y[0] + y[1]) / 2
  const xHalf = (perPx * safeWidth) / 2
  const yHalf = (perPx * safeHeight) / 2
  return {
    x: [xCentre - xHalf, xCentre + xHalf],
    y: [yCentre - yHalf, yCentre + yHalf],
  }
}

export function sameView(home: HomeScales, now: HomeScales): boolean {
  for (const key of Object.keys(home)) {
    const was = home[key]!
    const is = now[key]
    if (!is) continue
    const span = Math.abs(was.max - was.min) || 1
    if (Math.abs(is.min - was.min) > span * 1e-6) return false
    if (Math.abs(is.max - was.max) > span * 1e-6) return false
  }
  return true
}

/** Both ends of an axis pinned by the caller's lock.
 *
 * 잠금은 **기본 화면**을 정한다.  사이클을 하나만 골랐을 때 y 축이 그 곡선에
 * 맞춰 다시 잡히면 같은 곡선이 훨씬 뚱뚱해 보이는데, 숫자는 하나도 안 변했다 --
 * 그것을 막는 것이 잠금의 일이다.
 *
 * 확대를 막는 것은 그 일이 아니다.  확대·이동 중에는 잠금을 잠시 놓고(
 * `overrideLock`), '전체' 를 누르면 잠긴 화면으로 정확히 돌아온다.  그래야
 * 원하는 크기의 블록으로 확대해 놓고 그 안을 끌면서 볼 수 있다.
 */
function fullyPinned(range: [number | null, number | null] | undefined): boolean {
  return range !== undefined && range[0] !== null && range[1] !== null
}

/** 한 번 누를 때 얼마나. */
const ZOOM_STEP = 0.6

const PINNED_HINT =
  '축 고정은 기본 화면만 정합니다 — 확대하면 잠시 풀리고, 전체를 누르면 그 화면으로 돌아옵니다'

/** Stable identity for the common `markers={[]}` case.
 *
 * The plot is rebuilt whenever its options change, and the cursor readout
 * re-renders this component on every mouse move.  A `[]` default literal would
 * be a new array on each of those renders, so the plot would be destroyed and
 * built again mid-hover and the crosshair would never survive a mouse move. */
const NO_MARKERS: PlotMarker[] = []

export function Plot({
  series,
  xLabel,
  yLabel,
  height = 340,
  markers = NO_MARKERS,
  yRange,
  xRange,
  legend = false,
  equalAspect = false,
  positiveFit = false,
  busy = false,
  describeX,
  xTick,
  xSplits,
}: Props) {
  const [wrapRef, width] = useElementWidth<HTMLDivElement>()
  const plotRef = useRef<uPlot | null>(null)
  const nodeRef = useRef<HTMLDivElement>(null)
  const colors = useChartColors()
  const [readout, setReadout] = useState<Readout | null>(null)
  //: uPlot 이 정한 "커서에 가장 가까운 계열".  setSeries 로만 바뀐다.
  const focusRef = useRef<number | null>(null)
  //: 처음 잡힌 눈금.  '전체' 가 여기로 되돌린다.
  const homeRef = useRef<HomeScales | null>(null)
  const [zoomed, setZoomed] = useState(false)
  // 돋보기 기준 범위를 아직 못 잡았으면 버튼도 없는 셈이다.  눌러도 아무 일이
  // 없는 버튼은 고장 난 것으로 읽힌다.
  const [homeReady, setHomeReady] = useState(false)
  // 확대·이동 중에는 축 고정을 잠시 놓는다.
  //
  // **자물쇠는 "기본 화면" 을 정하는 것이지 확대를 막는 것이 아니다.**  잠근
  // 채로 두면 끌어서 고른 블록이 한 방향으로만 좁아져서, 사람은 "블록이 안
  // 생기고 회색이 화면을 덮는다" 로 읽는다.  원하는 크기로 확대해 놓고 그
  // 안을 끌면서 보는 것이 이 버튼들이 있는 이유다.
  //
  // 잠금이 필요한 이유(사이클을 하나만 골랐을 때 y 축이 그 곡선에 맞춰 다시
  // 잡혀 같은 곡선이 뚱뚱해 보이는 것)는 **기본 화면**에서 생기는 문제이므로,
  // '전체' 를 누르면 그 자리로 정확히 돌아간다.
  const overrideLock = useRef(false)

  const visible = useMemo(() => series.filter((s) => !s.hidden && s.x.length > 0), [series])

  // equalAspect 의 두 축 공동 해를 위해, 보이는 데이터의 극값을 한 번 잰다.
  const dataExtents = useMemo(() => {
    if (!visible.length) return null
    let xMin = Infinity
    let xMax = -Infinity
    let yMin = Infinity
    let yMax = -Infinity
    for (const item of visible) {
      for (const value of item.x) {
        if (value < xMin) xMin = value
        if (value > xMax) xMax = value
      }
      for (const value of item.y) {
        if (value === null || Number.isNaN(value)) continue
        if (value < yMin) yMin = value
        if (value > yMax) yMax = value
      }
    }
    if (!Number.isFinite(xMin) || !Number.isFinite(yMin)) return null
    return { x: [xMin, xMax] as [number, number], y: [yMin, yMax] as [number, number] }
  }, [visible])

  // Callers build these inline, so their identity changes on every render of
  // the parent; the plot only needs to be rebuilt when the values differ.
  const markerKey = markers
    .map((m) => `${m.x}|${m.label}|${m.color ?? ''}|${m.tentative ? 't' : ''}`)
    .join(';')
  const rangeKey = yRange ? `${yRange[0]}|${yRange[1]}` : ''
  const xRangeKey = xRange ? `${xRange[0]}|${xRange[1]}` : ''
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const steadyMarkers = useMemo(() => markers, [markerKey])
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const steadyRange = useMemo(() => yRange, [rangeKey])
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const steadyXRange = useMemo(() => xRange, [xRangeKey])

  const data = useMemo(() => {
    if (!visible.length) return null
    const axis = mergeX(visible)
    if (!axis.length) return null
    return [axis, ...visible.map((item) => alignY(item, axis))] as uPlot.AlignedData
  }, [visible])

  useEffect(() => {
    const node = nodeRef.current
    if (!node || !data || width < 80) return

    // 새 데이터로 다시 짓는 순간 이전 확대의 잠금 해제가 남아 있으면, 새
    // 그래프의 첫 눈금부터 equalAspect/축 고정이 꺼진 채 잡힌다 (W3).
    overrideLock.current = false

    const text = colors.text
    const grid = colors.grid

    const options: uPlot.Options = {
      width,
      height,
      legend: { show: legend },
      cursor: {
        // 끌어서 만든 사각형이 그대로 화면이 된다.
        //
        // `uni` 를 두면 가로로 길쭉한 드래그는 가로만 확대한다.  사람이 원하는
        // 것은 "이 블록을 크게" 이고, 한쪽만 확대되면 고른 세로 구간이 그대로
        // 남아 확대가 안 된 것처럼 보인다.  대신 `dist` 로 손 떨림만 거른다.
        //
        // 잠긴 축은 아예 못 끌게 한다.  끌 수 있게 두면 uPlot 이 잠금 범위를
        // 다시 씌우기 전까지 잠깐 움직이고, 그 사이 '축 고정' 이 꺼진 것처럼
        // 보인다 -- 버튼은 비활성인데 드래그는 되는 모순이었다.
        // 끌어서 만든 사각형이 그대로 화면이 된다.  잠긴 축이어도 마찬가지다 --
        // 잠금은 아래 overrideLock 이 잠시 놓는다.
        drag: { x: true, y: true, dist: 6 },
        // Shift 를 누른 채 끄는 것은 **이동**이다 (아래 직접 처리).  그대로 두면
        // uPlot 이 선택 사각형을 그려서, 옮기려던 사람이 확대를 하게 된다.
        bind: {
          mousedown: (_u, _target, handler) => (event: MouseEvent) => {
            if (event.shiftKey) return null
            // 끌기 시작한 순간부터 잠금을 놓는다.  선택이 끝난 뒤에 놓으면
            // uPlot 이 이미 잠금 범위로 되돌린 뒤라 늦다.
            overrideLock.current = true
            handler(event)
            return null
          },
        },
        focus: { prox: 24 },
        points: { size: 6, width: 1.5 },
      },
      scales: {
        x: {
          time: false,
          range: equalAspect
            ? (u, min, max) => {
                // 확대 중에는 손대지 않는다.  드래그로 고른 블록을 다시
                // 늘리면 사람이 고른 범위가 아닌 것이 나온다.
                if (overrideLock.current || !dataExtents) return [min, max]
                return equalAspectRanges(
                  [min, max], dataExtents.y,
                  u.bbox.width || 1, u.bbox.height || 1).x
              }
            : steadyXRange
              ? (_u, min, max) =>
                  overrideLock.current
                    ? [min, max]
                    : [steadyXRange[0] ?? min, steadyXRange[1] ?? max]
              : undefined,
        },
        y: {
          range: equalAspect
            ? (u, min, max) => {
                if (overrideLock.current || !dataExtents) return [min, max]
                return equalAspectRanges(
                  dataExtents.x, [min, max],
                  u.bbox.width || 1, u.bbox.height || 1).y
              }
            : steadyRange
              ? (_u, min, max) =>
                  overrideLock.current
                    ? [min, max]
                    : [steadyRange[0] ?? min, steadyRange[1] ?? max]
              : undefined,
        },
      },
      padding: [12, 14, 0, 0],
      axes: [
        {
          label: xLabel,
          labelSize: 28,
          labelGap: 4,
          stroke: text,
          ...(xSplits
            ? { splits: (_u: uPlot, _i: number, min: number, max: number) =>
                  xSplits(min, max) }
            : {}),
          ...(xTick
            ? { values: (_u: uPlot, splits: number[]) => splits.map(xTick) }
            : {}),
          // A dotted grid stays behind the data instead of competing with it.
          grid: { stroke: grid, width: 1, dash: [1, 3] },
          ticks: { stroke: grid, width: 1, size: 4 },
          font: AXIS_FONT,
          labelFont: LABEL_FONT,
          gap: 4,
        },
        {
          label: yLabel,
          labelSize: 40,
          labelGap: 4,
          stroke: text,
          grid: { stroke: grid, width: 1, dash: [1, 3] },
          ticks: { stroke: grid, width: 1, size: 4 },
          font: AXIS_FONT,
          labelFont: LABEL_FONT,
          size: 58,
          gap: 4,
        },
      ],
      series: [
        {},
        ...visible.map((item, index) => ({
          label: item.label,
          stroke: resolveColor(seriesToken(item.color, index), seriesColor(index)),
          width: item.width ?? 1.6,
          dash: item.dash,
          spanGaps: item.spanGaps ?? true,
          points: { show: item.points ?? false, size: 4 },
        })),
      ],
      hooks: {
        // 확대 여부는 **uPlot 의 눈금을 읽어서** 정한다.  버튼을 누른 횟수를
        // 세면 드래그 확대와 더블클릭 복귀를 놓치고, 그때 '전체' 버튼이
        // 화면과 어긋난 상태로 남는다 (꺼져 있는데 확대돼 있거나, 그 반대).
        setScale: [
          (u: uPlot) => {
            // **처음 눈금이 정해지는 순간을 여기서 잡는다.**
            //
            // 생성자가 반환할 때 uPlot 의 scales.*.min 은 아직 ±Infinity 다 --
            // 초기 commit 을 microtask 로 미루기 때문이다 (uPlot 1.6.32,
            // `_init → _setSize → commit`, `commit → microTask(_commit)`).
            // 생성 직후에 읽으면 readScales 가 {} 를 돌려주고, 그 뒤로 zoomBy
            // 는 순회할 축이 없어 아무 일도 안 하며 sameView({}, …) 는 늘 참이라
            // '축소'·'전체' 가 영영 비활성으로 남는다 -- 돋보기 셋이 전부 죽는다.
            if (!homeRef.current) {
              const first = readScales(u)
              if (!Object.keys(first).length) return
              homeRef.current = first
              setHomeReady(true)
              setZoomed(false)
              return
            }
            setZoomed(!sameView(homeRef.current, readScales(u)))
          },
        ],
        // 커서가 어느 계열에 붙었는지는 uPlot 이 focus.prox 로 이미 정한다.
        // 그 판단을 다시 구현하지 않고 그대로 받아 쓴다.
        setSeries: [
          (_u, seriesIdx) => {
            focusRef.current = seriesIdx
          },
        ],
        setCursor: [
          (u) => {
            const { left, top, idx } = u.cursor
            if (left === undefined || top === undefined || left < 0 || top < 0) {
              setReadout(null)
              return
            }
            if (idx === null || idx === undefined) {
              setReadout(null)
              return
            }
            const focus = focusRef.current
            const item = focus === null || focus === undefined ? undefined : visible[focus - 1]
            const point =
              focus === null || focus === undefined ? null : pointAt(u.data, focus, idx)
            // 팝업은 우리 껍데기 안에 그리고, uPlot 의 그림 영역은 그 안에서
            // 축 라벨만큼 밀려 있다.  두 사각형의 차이가 그 오프셋이다.
            const over = u.over?.getBoundingClientRect?.()
            const shell = wrapRef.current?.getBoundingClientRect?.()
            const dx = over && shell ? over.left - shell.left : 0
            const dy = over && shell ? over.top - shell.top : 0
            const axisX = u.data[0]?.[idx]
            setReadout({
              left: dx + left,
              top: dy + top,
              flip: left > (over?.width ?? u.width) - TIP_WIDTH,
              label: visible.length > 1 ? (item?.label ?? null) : null,
              color: item ? seriesToken(item.color, (focus as number) - 1) : null,
              x: point ? point.x : Number(axisX),
              y: point ? point.y : null,
            })
          },
        ],
        // **키를 아예 넣지 않는다.**  `draw: undefined` 는 다르다 -- uPlot 의
        // `fire()` 는 `evName in hooks` 로 걸러서 (uPlot 1.6.32, `fire`),
        // 키가 있으면 값이 undefined 여도 `hooks.draw.forEach` 를 부른다.
        // 표시선이 없는 그래프(거의 전부)는 그래서 **다시 그릴 때마다**
        // TypeError 를 냈고, 그 예외가 commit 을 중간에 끊었다: 끌어서 확대한
        // 사각형이 눈금까지 못 가고 그냥 사라졌다.  화면에는 오류가 안 보이니
        // "확대가 안 된다" 로만 보인다.
        ...(steadyMarkers.length ? {
          draw: [
              (u: uPlot) => {
                const ctx = u.ctx
                ctx.save()
                for (const marker of steadyMarkers) {
                  const x = u.valToPos(marker.x, 'x', true)
                  if (!Number.isFinite(x)) continue
                  ctx.strokeStyle = marker.color ?? colors.warn
                  ctx.lineWidth = marker.tentative ? 1 : 1.25
                  ctx.globalAlpha = marker.tentative ? 0.55 : 1
                  ctx.setLineDash(marker.tentative ? [2, 4] : [5, 4])
                  ctx.beginPath()
                  ctx.moveTo(x, u.bbox.top)
                  ctx.lineTo(x, u.bbox.top + u.bbox.height)
                  ctx.stroke()
                  ctx.setLineDash([])
                  const color = marker.color ?? colors.warn
                  ctx.font = LABEL_FONT
                  ctx.textAlign = 'left'
                  // A plate behind the label keeps it readable over the data.
                  const textWidth = ctx.measureText(marker.label).width
                  ctx.fillStyle = colors.surface
                  ctx.fillRect(x + 3, u.bbox.top + 2, textWidth + 8, 16)
                  ctx.fillStyle = color
                  ctx.fillText(marker.label, x + 7, u.bbox.top + 14)
                  ctx.globalAlpha = 1
                }
                ctx.restore()
              },
          ],
        } : {}),
      },
    }

    plotRef.current?.destroy()
    focusRef.current = null
    homeRef.current = null
    setReadout(null)
    setZoomed(false)
    setHomeReady(false)
    // 기준 범위는 여기서 읽지 않는다 -- 아직 정해지지 않았다.  위 setScale
    // 훅이 첫 commit 에서 잡는다.
    const plot = new uPlot(options, data, node)
    plotRef.current = plot

    // --- Shift + 드래그로 이동 ------------------------------------------------
    //
    // 확대해 놓고 옆을 보려면 옮길 수 있어야 하는데, 그냥 드래그는 이미 "이
    // 사각형을 크게" 가 가져갔다.  uPlot 에는 이동이 없으므로 직접 옮긴다.
    // 처음 범위 밖으로는 안 나간다 -- 계속 끌다 데이터가 사라지면 돌아오는
    // 길이 '전체' 버튼뿐이다.
    const over = plot.over
    let pan: { x: number; y: number; from: HomeScales } | null = null

    const onDown = (event: MouseEvent) => {
      if (!event.shiftKey || !homeRef.current) return
      event.preventDefault()
      overrideLock.current = true
      pan = { x: event.clientX, y: event.clientY, from: readScales(plot) }
      over.style.cursor = 'grabbing'
    }
    const onMove = (event: MouseEvent) => {
      if (!pan) return
      const width = over.clientWidth || 1
      const height = over.clientHeight || 1
      const home = homeRef.current ?? {}
      const from = pan.from
      const dx = event.clientX - pan.x
      const dy = event.clientY - pan.y
      plot.batch(() => {
        for (const key of Object.keys(from)) {
          const start = from[key]!
          const span = start.max - start.min
          // 화면 y 는 아래로 늘고 값은 위로 는다 -- 그래서 부호가 다르다.
          const shift = key === 'x' ? -(dx / width) * span : (dy / height) * span
          let min = start.min + shift
          let max = start.max + shift
          const limit = home[key]
          if (limit) {
            if (min < limit.min) { max += limit.min - min; min = limit.min }
            if (max > limit.max) { min -= max - limit.max; max = limit.max }
          }
          plot.setScale(key, { min, max })
        }
      })
    }
    const onUp = () => {
      if (!pan) return
      pan = null
      over.style.cursor = ''
    }

    over.addEventListener('mousedown', onDown)
    window.addEventListener('mousemove', onMove)
    window.addEventListener('mouseup', onUp)

    return () => {
      over.removeEventListener('mousedown', onDown)
      window.removeEventListener('mousemove', onMove)
      window.removeEventListener('mouseup', onUp)
      plotRef.current?.destroy()
      plotRef.current = null
      homeRef.current = null
    }
  }, [
    data,
    visible,
    width,
    height,
    xLabel,
    yLabel,
    steadyMarkers,
    steadyRange,
    steadyXRange,
    equalAspect,
    legend,
    colors,
    wrapRef,
  ])

  const xAxis = splitAxisLabel(xLabel)
  const yAxis = splitAxisLabel(yLabel)

  // 두 축이 모두 잠겨 있으면 확대가 그림을 못 바꾼다 -- uPlot 이 매 프레임
  // 잠금 범위를 다시 씌우기 때문이다.  아무 일도 안 일어나는 버튼을 내놓는
  // 대신 끄고, 왜 껐는지를 말한다.

  const anyLock = fullyPinned(steadyXRange) || fullyPinned(steadyRange)
  const lockNote = anyLock ? PINNED_HINT : ''

  /** 가운데를 붙잡고 폭만 줄이거나 늘린다.
   *
   *  커서 자리를 중심으로 잡을 수도 있지만, 버튼은 커서가 그래프 밖(버튼 위)에
   *  있을 때 눌린다.  그때 "마지막으로 머물던 자리" 를 쓰면 누를 때마다 다른
   *  곳으로 튀고, 두 번 눌러 원래대로 돌아오지도 않는다.
   *
   *  축소는 처음 범위를 넘지 않는다.  넘어가면 '축소' 를 계속 눌렀을 때
   *  데이터가 점점 작아지다 사라지고, '전체' 와 다른 곳에 멈춘다. */
  const zoomBy = (factor: number) => {
    const plot = plotRef.current
    const home = homeRef.current
    if (!plot || !home) return
    overrideLock.current = true
    plot.batch(() => {
      for (const key of Object.keys(home)) {
        const scale = plot.scales[key]
        const limit = home[key]!
        if (!scale || typeof scale.min !== 'number' || typeof scale.max !== 'number') continue
        const middle = (scale.min + scale.max) / 2
        const half = ((scale.max - scale.min) / 2) * factor
        const width = Math.min(half, (limit.max - limit.min) / 2)
        let min = middle - width
        let max = middle + width
        // 밖으로 밀려난 만큼 도로 안쪽으로 민다 -- 폭은 지키고 자리만 옮긴다.
        if (min < limit.min) { max += limit.min - min; min = limit.min }
        if (max > limit.max) { min -= max - limit.max; max = limit.max }
        plot.setScale(key, { min: Math.max(min, limit.min), max: Math.min(max, limit.max) })
      }
    })
  }

  /** −Z″ ≥ 0 인 점들에만 딱 맞춘다.
   *
   *  세로 아래끝은 **0 으로 고정**한다.  데이터의 최솟값에 맞추면 누를 때마다
   *  기준이 달라지고, 이 버튼의 이름이 곧 약속이다.
   *
   *  `equalAspect` 가 켜져 있으면 두 축의 단위/픽셀을 맞춘 뒤 세로를 **옮겨서**
   *  0 에서 시작하게 한다 — 다시 좁히면 비율이 깨지고, 나이퀴스트에서 비율은
   *  물리다 (반원이 반원으로 보여야 한다).
   *
   *  **아크가 있으면 아크에 맞춘다** (`arcWindow`).  실수축 위를 빼는 것만으로는
   *  확산 꼬리가 안 잘리고, 그 꼬리가 반원보다 높으면 세로 눈금이 통째로 늘어나
   *  반원이 납작해진다.  꼬리가 반원보다 낮으면 안 자른다 — 그때는 전부 보이는
   *  편이 낫다.
   */
  const fitPositive = () => {
    const plot = plotRef.current
    if (!plot) return
    let xMin = Infinity
    let xMax = -Infinity
    let yMax = -Infinity
    for (const item of visible) {
      for (let i = 0; i < item.x.length; i += 1) {
        const value = item.y[i]
        const at = item.x[i]
        if (value === null || value === undefined || !Number.isFinite(value)) continue
        if (value < 0 || at === undefined || !Number.isFinite(at)) continue
        if (at < xMin) xMin = at
        if (at > xMax) xMax = at
        if (value > yMax) yMax = value
      }
    }
    // 아무 점도 0 위에 없으면 아무 일도 하지 않는다.  빈 화면으로 옮기는 것보다
    // 안 움직이는 편이 낫다 -- 버튼이 회색이므로 눌리지도 않는다.
    if (!Number.isFinite(xMin) || !Number.isFinite(yMax)) return
    // **확산 꼬리는 한 번 더 자른다.**  `y ≥ 0` 은 실수축 위(유도성)만 빼는데,
    // 저주파 45° 직선이 반원 높이의 몇 배까지 올라가면 정작 회로를 고를 때
    // 보는 반원이 바닥에 눌린다.  아크가 사는 구간을 찾아서 (`lib/eis`) 거기에
    // 맞춘다 — 꼬리가 아크보다 낮으면 `null` 이고, 그때는 예전 그대로다.
    const arcs = arcWindow(visible)
    if (arcs) {
      xMax = Math.min(xMax, arcs.xMax)
      yMax = arcs.yMax
    }
    // 점 하나뿐이면 폭이 0 이다.  uPlot 은 min === max 를 그리지 못한다.
    const pad = (span: number, value: number) => (span > 0 ? span : Math.abs(value) * 0.1 || 1)
    let x: [number, number] = [xMin, xMax + (xMax > xMin ? 0 : pad(0, xMax))]
    let y: [number, number] = [0, yMax > 0 ? yMax : pad(0, 1)]
    if (equalAspect) {
      const fitted = equalAspectRanges(x, y, plot.bbox.width || 1, plot.bbox.height || 1)
      x = fitted.x
      // 폭은 그대로 두고 0 에서 시작하도록 옮긴다.
      y = [0, fitted.y[1] - fitted.y[0]]
    }
    overrideLock.current = true
    plot.batch(() => {
      plot.setScale('x', { min: x[0], max: x[1] })
      plot.setScale('y', { min: y[0], max: y[1] })
    })
  }

  /** 0 위에 그릴 것이 하나라도 있는가.  없으면 버튼을 끈다. */
  const hasPositive = useMemo(
    () => visible.some((item) => item.y.some(
      (value) => value !== null && value !== undefined && Number.isFinite(value) && value >= 0)),
    [visible])

  const resetZoom = () => {
    const plot = plotRef.current
    const home = homeRef.current
    if (!plot || !home) return
    // 처음 눈금은 잠금이 걸린 채로 잡힌 것이라, 여기로 돌아가면 잠금 화면으로
    // 정확히 돌아간다.  그 뒤의 자동 재계산부터 잠금이 다시 일한다.
    overrideLock.current = false
    plot.batch(() => {
      for (const key of Object.keys(home)) plot.setScale(key, { ...home[key]! })
    })
  }

  return (
    <div ref={wrapRef} className="plot-shell">
      {data ? (
        <>
          <div className="plot-zoom">
            {/* 단추 줄 **맨 앞** -- 그림 위에 겹치지 않는 자리다.  겹치면 새로
                고칠 때마다 데이터를 가리고, 하필 가려지는 것이 방금 바뀐
                부분이다. */}
            {busy ? (
              <span className="plot-busy" role="status" aria-label="새로 받는 중">
                <span className="spinner" aria-hidden="true" />
                <span className="tiny faint">새로 받는 중</span>
              </span>
            ) : null}
            <button
              type="button"
              className="sm ghost"
              onClick={() => zoomBy(ZOOM_STEP)}
              disabled={!homeReady}
              aria-label="확대"
              title={
                (lockNote || '확대 — 그래프 위를 끌면 그 사각형이 그대로 화면이 됩니다')
                + ' · Shift+드래그로 이동'
              }
            >
              🔍+
            </button>
            <button
              type="button"
              className="sm ghost"
              onClick={() => zoomBy(1 / ZOOM_STEP)}
              disabled={!homeReady || !zoomed}
              aria-label="축소"
              title={'축소'}
            >
              🔍−
            </button>
            {positiveFit ? (
              <button
                type="button"
                className="sm ghost"
                onClick={fitPositive}
                disabled={!homeReady || !hasPositive}
                aria-label="y 0 이상만"
                title="−Z″ 가 0 이상인 곳에만 화면을 맞춥니다 — 고주파 인덕턴스 꼬리 때문에 아크가 납작해질 때"
              >
                y ≥ 0
              </button>
            ) : null}
            <button
              type="button"
              className="sm ghost"
              onClick={resetZoom}
              disabled={!homeReady || !zoomed}
              aria-label="확대 초기화"
              title="처음 보이던 범위로 되돌립니다 (그래프를 더블클릭해도 됩니다)"
            >
              전체
            </button>
          </div>
          <div ref={nodeRef} />
        </>
      ) : (
        <div
          className="empty"
          style={{ height, display: 'grid', placeContent: 'center', padding: 0 }}
        >
          <div className="icon">⌁</div>
          그릴 데이터가 없습니다
        </div>
      )}

      {/* 커서 옆 판독기.  십자선만으로는 "여기가 몇 사이클의 몇 mAh/g 인지" 를
          눈대중으로 축까지 따라가야 한다.  pointer-events 를 끄지 않으면 팝업이
          제 밑의 커서를 가려 uPlot 이 마우스를 잃는다. */}
      {readout ? (
        <div
          className="plot-tip"
          style={{
            left: readout.left,
            top: readout.top,
            transform: readout.flip
              ? `translate(calc(-100% - ${TIP_GAP}px), -50%)`
              : `translate(${TIP_GAP}px, -50%)`,
          }}
        >
          {readout.label ? (
            <div className="tip-head">
              <span
                className="swatch"
                style={readout.color ? { background: readout.color } : undefined}
              />
              <span className="truncate">{readout.label}</span>
            </div>
          ) : null}
          <div className="tip-row">
            <span>{xAxis.name}</span>
            <b>
              {xTick ? xTick(readout.x) : num(readout.x)}
              {xAxis.unit ? ` ${xAxis.unit}` : ''}
            </b>
          </div>
          {readout.y === null ? null : (
            <div className="tip-row">
              <span>{yAxis.name}</span>
              <b>
                {num(readout.y)}
                {yAxis.unit ? ` ${yAxis.unit}` : ''}
              </b>
            </div>
          )}
          {describeX?.(readout.x) ? (
            <div className="tip-note">{describeX(readout.x)}</div>
          ) : null}
        </div>
      ) : null}
    </div>
  )
}

interface LegendProps {
  series: PlotSeries[]
  onToggle?: (label: string) => void
}

/** A compact chip legend; uPlot's own legend is too tall for many series. */
/** Fold the legend to one row until asked to open.
 *
 * Cutting at a fixed number of chips does not cut at a fixed *height*: chip
 * widths run from "2번 충전" to a full cell name, so twelve of them are one row
 * on a wide screen and three rows on a narrow one.  Clamping the height
 * instead lets the browser decide how many fit, which is the only thing that
 * matters -- everything below the plot stays where it was.
 *
 * The row height is measured from a real chip rather than assumed, because the
 * chips carry the app's own font and padding.
 */
function useOneRowClamp(count: number) {
    const box = useRef<HTMLDivElement | null>(null)
    const [rowHeight, setRowHeight] = useState<number | null>(null)
    const [overflows, setOverflows] = useState(false)

    useEffect(() => {
      const node = box.current
      const chip = node?.firstElementChild as HTMLElement | null
      if (!node || !chip) return
      const measure = () => {
        const style = getComputedStyle(node)
        const oneRow = oneRowHeight(
          chip.offsetHeight,
          parseFloat(style.paddingTop),
          parseFloat(style.paddingBottom),
        )
        setRowHeight(oneRow || null)
        setOverflows(node.scrollHeight > oneRow + 2)
      }
      measure()
      const observer = new ResizeObserver(measure)
      observer.observe(node)
      return () => observer.disconnect()
    }, [count])

    return { box, rowHeight, overflows }
}

/** How tall the chip box may be and still show exactly one row.
 *
 * The container is `box-sizing: border-box` and carries 8px above the chips
 * and 12px below, so a clamp set to the bare chip height (~20px) spends all of
 * it on padding and slices every chip in half -- which is what shipped.  Both
 * numbers here are border-box heights so `scrollHeight` can be compared
 * against them directly, and the toggle stops appearing over a legend that
 * already fits.
 *
 * Exported because jsdom has no layout engine: every offsetHeight there is 0,
 * so a rendering test cannot see this arithmetic go wrong. */
export function oneRowHeight(
  chipHeight: number,
  paddingTop: number,
  paddingBottom: number,
): number {
  if (!chipHeight) return 0
  return chipHeight + (paddingTop || 0) + (paddingBottom || 0)
}

export function PlotLegend({ series, onToggle }: LegendProps) {
  const [open, setOpen] = useState(false)
  const { box, rowHeight, overflows } = useOneRowClamp(series.length)
  const partialCount = series.filter((item) => item.partial).length
  if (series.length <= 1) return null
  const clamp = !open && overflows && rowHeight !== null
  return (
    <div className="col" style={{ gap: 6 }}>
      {overflows ? (
        <button
          type="button"
          className="sm legend-toggle"
          onClick={() => setOpen((was) => !was)}
          aria-expanded={open}
        >
          {(open ? '범례 접기' : '범례 전부 보기')
            + ` (${series.length}개`
            // 접혀 있으면 부분 곡선이 통째로 안 보일 수 있다.  몇 개가 그런
            // 곡선인지라도 말해 주면, 캡처만 보는 사람이 속지 않는다.
            + (partialCount ? ` · 부분 ${partialCount}개` : '')
            + ')'}
        </button>
      ) : null}
      <div
        ref={box}
        className="legend-chips"
        style={clamp ? { maxHeight: rowHeight, overflow: 'hidden' } : undefined}
      >
      {series.map((item, index) => (
        <button
          key={item.label}
          type="button"
          className={`legend-chip${item.hidden ? ' off' : ''}`}
          onClick={() => onToggle?.(item.label)}
          title={item.hidden ? '표시' : '숨기기'}
        >
          <span
            className={`swatch${item.dash ? ' dashed' : ''}${item.partial ? ' thin' : ''}`}
            style={
              item.dash
                ? { color: seriesToken(item.color, index), background: 'transparent' }
                : { background: seriesToken(item.color, index) }
            }
          />
          {item.label}
          {item.note ? <span className="legend-note">{item.note}</span> : null}
        </button>
      ))}
      </div>
    </div>
  )
}
