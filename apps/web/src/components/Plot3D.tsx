/** 축이 셋인 그림 — SOC 스캔을 논문처럼.
 *
 *  **왜 uPlot 이 아닌가.**  이 저장소의 모든 그림은 uPlot 이다 (빠르고, 수만
 *  점을 견디고, 확대·이동이 공짜다).  그런데 uPlot 은 2D 다.  처음에는 3D 를
 *  흉내 내려고 곡선을 깊이만큼 오른쪽·위로 **밀었는데**, 그 그림은 축이 둘뿐이라
 *  깊이가 눈에 안 들어왔다 — 열한 곡선이 대각선으로 늘어선 한 덩어리로 보였다.
 *  축을 그리지 않으면 깊이는 없는 것과 같다.
 *
 *  그래서 여기서는 **직접 투영해서 SVG 로 그린다.**  잃는 것이 있다: 수만 점을
 *  못 견디고 (스캔은 스윕당 100 점 안팎이라 괜찮다), uPlot 의 확대·툴팁이 없다.
 *  얻는 것은 축 셋과 상자와 눈금 — 그것이 이 그림의 전부다.
 *
 *  **직교 투영이다** (원근 없음).  MATLAB 의 기본 뷰와 같은 이유: 원근이 붙으면
 *  뒤쪽 곡선이 작아져서, 아크가 실제로 작아진 것인지 멀리 있는 것인지 구분이
 *  안 된다.  이 그림에서 크기는 물리여야 한다.
 *
 *  **깊이는 계열마다 하나의 값**이다 (스윕 하나 = 전위 하나).  점마다 다른 깊이는
 *  안 받는다 — 우리 데이터에 그런 것이 없고, 받으면 면(surface)을 그려야 한다.
 */

import { useEffect, useMemo, useRef, useState } from 'react'

import { num, seriesColor } from '../lib/format'

export interface Series3D {
  label: string
  x: number[]
  y: number[]
  /** 이 곡선이 놓이는 깊이.  스윕 하나에 하나 (전위 V). */
  z: number
  color?: string
  hidden?: boolean
  /** 점을 찍을까.  실측은 점, 맞춤은 선. */
  points?: boolean
}

/** 처음 보는 각도 — MATLAB 의 기본(방위 −37.5°, 고도 30°) 과 같다.
 *
 *  이 각도가 관례가 된 이유가 있다: 세 축이 모두 보이고, 어느 축도 다른 축에
 *  가려지지 않으며, 깊이 방향이 오른쪽 뒤로 물러난다.  논문 그림이 대개 이
 *  모양이라 눈이 이미 읽을 줄 안다.
 */
const AZIMUTH0 = -37.5
const ELEVATION0 = 26

const MARGIN = { left: 74, right: 28, top: 22, bottom: 62 }

/** 눈금을 몇 칸으로 나눌까.  다섯이면 상자 세 면이 답답하지 않다. */
const TICKS = 5

/** 사람이 읽기 좋은 눈금 자리 (1·2·5 × 10ᵏ). */
function niceTicks(low: number, high: number, count = TICKS): number[] {
  if (!(high > low)) return [low]
  const rough = (high - low) / count
  const magnitude = 10 ** Math.floor(Math.log10(rough))
  const step = [1, 2, 2.5, 5, 10].map((m) => m * magnitude)
    .find((one) => one >= rough) ?? magnitude * 10
  const out: number[] = []
  for (let v = Math.ceil(low / step) * step; v <= high + step * 1e-9; v += step) {
    out.push(Number(v.toPrecision(12)))
  }
  return out.length ? out : [low, high]
}

interface Cube {
  /** 단위 정육면체 좌표 (0~1) → 화면 좌표. */
  at: (u: number, v: number, w: number) => { x: number; y: number }
}

/** 방위·고도로 직교 투영을 만든다.
 *
 *  `u` 는 가로(Z′), `v` 는 세로(−Z″), `w` 는 깊이(전위).  화면의 y 는 아래로
 *  자라므로 부호를 뒤집는다.
 */
function project(azimuth: number, elevation: number,
                 scale: number, centre: { x: number; y: number }): Cube {
  const az = (azimuth * Math.PI) / 180
  const el = (elevation * Math.PI) / 180
  const ca = Math.cos(az)
  const sa = Math.sin(az)
  const ce = Math.cos(el)
  const se = Math.sin(el)
  return {
    at(u, v, w) {
      // 가운데를 원점으로 두고 돌린다 — 안 그러면 회전이 그림을 화면 밖으로
      // 끌고 나간다.
      const du = u - 0.5
      const dv = v - 0.5
      const dw = w - 0.5
      const px = du * ca + dw * sa
      const depth = -du * sa + dw * ca
      return {
        x: centre.x + px * scale,
        y: centre.y - (dv * ce - depth * se) * scale,
      }
    },
  }
}

/** 상자의 여덟 꼭짓점 (u, v, w). */
const CORNERS: [number, number, number][] = [
  [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
  [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],
]

/** 열두 모서리 — 꼭짓점 번호 짝. */
const EDGES: [number, number][] = [
  [0, 1], [1, 2], [2, 3], [3, 0],
  [4, 5], [5, 6], [6, 7], [7, 4],
  [0, 4], [1, 5], [2, 6], [3, 7],
]

export function Plot3D({
  series,
  xLabel,
  yLabel,
  zLabel,
  height = 520,
  zTicks,
  zTickLabel,
}: {
  series: Series3D[]
  xLabel: string
  yLabel: string
  /** 깊이 축 이름 — 우리 경우 `전위 (V)`. */
  zLabel: string
  height?: number
  /** 깊이 눈금을 직접 정할 때 (스윕의 실제 전위들).  비우면 고르게 나눈다. */
  zTicks?: number[]
  /** 깊이 눈금에 적을 글자.  깊이가 **수가 아닐 때** 쓴다 — 비교 화면의 깊이는
   *  고른 스펙트럼의 이름이고, 거기에 `0.000` 이라고 적으면 아무 뜻이 없다. */
  zTickLabel?: (value: number) => string
}) {
  const box = useRef<HTMLDivElement>(null)
  const [azimuth, setAzimuth] = useState(AZIMUTH0)
  const [elevation, setElevation] = useState(ELEVATION0)
  const [zoom, setZoom] = useState(1)
  //: 확대한 뒤 **옮길** 수 있어야 한다.  가운데만 커지면 보고 싶은 구석이
  //  화면 밖으로 나가고, 그때 할 수 있는 일이 '전체' 뿐이다.
  const [pan, setPan] = useState({ x: 0, y: 0 })
  const drag = useRef<
    { x: number; y: number; az: number; el: number; pan: { x: number; y: number };
      move: boolean } | null>(null)
  const [width, setWidth] = useState(900)

  //: 휠로 확대할 때 **뒤의 화면이 같이 스크롤되면 안 된다.**  React 의
  //  `onWheel` 은 passive 로 붙어서 `preventDefault` 가 안 먹는다 (브라우저가
  //  무시한다).  그래서 직접, passive 를 끄고 붙인다.
  useEffect(() => {
    const node = box.current
    if (!node) return
    const onWheel = (event: WheelEvent) => {
      if (!event.deltaY) return
      event.preventDefault()
      setZoom((was) => Math.max(0.4,
        Math.min(8, was * (event.deltaY < 0 ? 1.12 : 1 / 1.12))))
    }
    node.addEventListener('wheel', onWheel, { passive: false })
    return () => node.removeEventListener('wheel', onWheel)
  }, [])

  // 폭은 부모가 정한다.  `ResizeObserver` 가 없는 환경에서는 기본값으로 그린다 —
  // 그림이 조금 좁을 뿐 안 그려지지는 않는다.
  useMemo(() => {
    const node = box.current
    if (!node || typeof ResizeObserver === 'undefined') return
    const watch = new ResizeObserver(() => setWidth(node.clientWidth || 900))
    watch.observe(node)
    return () => watch.disconnect()
  }, [])

  const shown = series.filter((one) => !one.hidden)

  const bounds = useMemo(() => {
    let xLow = Infinity, xHigh = -Infinity
    let yLow = Infinity, yHigh = -Infinity
    let zLow = Infinity, zHigh = -Infinity
    for (const one of shown) {
      for (const value of one.x) {
        if (!Number.isFinite(value)) continue
        if (value < xLow) xLow = value
        if (value > xHigh) xHigh = value
      }
      for (const value of one.y) {
        if (!Number.isFinite(value)) continue
        if (value < yLow) yLow = value
        if (value > yHigh) yHigh = value
      }
      if (Number.isFinite(one.z)) {
        if (one.z < zLow) zLow = one.z
        if (one.z > zHigh) zHigh = one.z
      }
    }
    if (!Number.isFinite(xLow) || !Number.isFinite(yLow)) return null
    // 깊이가 하나뿐이면 (스윕 하나, 또는 전위가 전부 같음) 상자를 못 세운다.
    if (!Number.isFinite(zLow) || zHigh <= zLow) {
      zLow = 0
      zHigh = Math.max(1, shown.length - 1)
    }
    const pad = (low: number, high: number) => {
      const span = high - low
      const room = span > 0 ? span * 0.05 : Math.abs(high) * 0.1 || 1
      return [low - room, high + room] as [number, number]
    }
    const [x0, x1] = pad(xLow, xHigh)
    const [y0, y1] = pad(yLow, yHigh)
    return { x: [x0, x1] as [number, number], y: [y0, y1] as [number, number],
             z: [zLow, zHigh] as [number, number],
             raw: { x: [xLow, xHigh] as [number, number],
                    y: [yLow, yHigh] as [number, number] } }
  }, [shown])

  if (!bounds) {
    return (
      <div className="empty" style={{ height }}>
        <div className="empty-icon">◱</div>
        <div>그릴 것이 없습니다</div>
      </div>
    )
  }

  const view = { width: Math.max(360, width), height }
  const inner = {
    width: view.width - MARGIN.left - MARGIN.right,
    height: view.height - MARGIN.top - MARGIN.bottom,
  }
  const centre = {
    x: MARGIN.left + inner.width / 2 + pan.x,
    y: MARGIN.top + inner.height / 2 + pan.y,
  }
  // 상자가 화면에 딱 맞게 — 돌리면 대각선이 길어지므로 그때마다 다시 잰다.
  const probe = project(azimuth, elevation, 1, { x: 0, y: 0 })
  let boxWide = 0
  let boxTall = 0
  for (const [u, v, w] of CORNERS) {
    const at = probe.at(u, v, w)
    boxWide = Math.max(boxWide, Math.abs(at.x) * 2)
    boxTall = Math.max(boxTall, Math.abs(at.y) * 2)
  }
  const scale = zoom * Math.min(inner.width / (boxWide || 1),
                                inner.height / (boxTall || 1))
  const cube = project(azimuth, elevation, scale, centre)

  const unit = {
    x: (value: number) => (value - bounds.x[0]) / (bounds.x[1] - bounds.x[0] || 1),
    y: (value: number) => (value - bounds.y[0]) / (bounds.y[1] - bounds.y[0] || 1),
    // **깊이는 거꾸로 넣는다** — 작은 값이 앞이다.
    //
    // `w = 1` 쪽이 화면 앞이다 (기본 각도에서 오른쪽 아래로 나온다).  그대로
    // 두면 가장 큰 전위가 앞, `#1` 이 맨 뒤에 선다.  스캔을 읽는 순서는 `#1`
    // 부터이고, 앞에 있는 곡선이 뒤의 것을 덮으므로 **먼저 읽을 것이 앞**에
    // 있어야 한다.  비교 화면도 같다: 먼저 고른 것이 앞이다.
    z: (value: number) =>
      1 - (value - bounds.z[0]) / (bounds.z[1] - bounds.z[0] || 1),
  }

  const corners = CORNERS.map(([u, v, w]) => cube.at(u, v, w))

  /** 눈금을 달 모서리를 고른다.
   *
   *  **각도에 따라 달라진다.**  돌리면 앞뒤가 바뀌므로 "0번 모서리" 로 박아
   *  두면 눈금이 상자 뒤로 숨는다.  가로·깊이는 화면에서 **가장 아래**,
   *  세로는 **가장 왼쪽** 모서리에 단다.
   */
  const pickEdge = (parallel: [number, number][], by: 'low' | 'left') => {
    let best = parallel[0]!
    let mark = Infinity
    for (const edge of parallel) {
      const a = corners[edge[0]]!
      const b = corners[edge[1]]!
      const score = by === 'low' ? -(a.y + b.y) / 2 : (a.x + b.x) / 2
      if (score < mark) { mark = score; best = edge }
    }
    return best
  }
  // u 방향(가로) 모서리 넷, w 방향(깊이) 넷, v 방향(세로) 넷.
  const uEdge = pickEdge([[0, 1], [3, 2], [4, 5], [7, 6]], 'low')
  const wEdge = pickEdge([[0, 4], [1, 5], [2, 6], [3, 7]], 'low')
  const vEdge = pickEdge([[0, 3], [1, 2], [4, 7], [5, 6]], 'left')

  const line = (points: { x: number; y: number }[]) =>
    points.map((one, i) => `${i ? 'L' : 'M'}${one.x.toFixed(1)},${one.y.toFixed(1)}`)
      .join(' ')

  const xTicks = niceTicks(bounds.x[0], bounds.x[1])
  const yTicks = niceTicks(bounds.y[0], bounds.y[1])
  const zTickValues = zTicks?.length ? zTicks : niceTicks(bounds.z[0], bounds.z[1])

  /** 눈금 하나 — 모서리 위의 자리와, 상자 **바깥**으로 뻗는 글자 자리. */
  const tickAt = (edge: [number, number], t: number, away: number) => {
    const [ai, bi] = edge
    const a = CORNERS[ai]!
    const b = CORNERS[bi]!
    const mix = (i: 0 | 1 | 2) => a[i] + (b[i] - a[i]) * t
    const on = cube.at(mix(0), mix(1), mix(2))
    // 바깥 방향 = 상자 가운데에서 이 점으로 가는 방향.
    const middle = cube.at(0.5, 0.5, 0.5)
    const dx = on.x - middle.x
    const dy = on.y - middle.y
    const len = Math.hypot(dx, dy) || 1
    return { on, out: { x: on.x + (dx / len) * away, y: on.y + (dy / len) * away } }
  }

  return (
    <div className="plot3d" ref={box} style={{ position: 'relative' }}>
      <div className="plot-zoom">
        <button type="button" className="sm ghost" aria-label="확대"
                title="확대 — 상자째 커집니다"
                onClick={() => setZoom((was) => Math.min(8, was * 1.25))}>🔍+</button>
        <button type="button" className="sm ghost" aria-label="축소"
                disabled={zoom <= 0.4}
                onClick={() => setZoom((was) => Math.max(0.4, was / 1.25))}>🔍−</button>
        <button type="button" className="sm ghost" aria-label="각도 초기화"
                title="처음 각도와 크기로"
                onClick={() => {
                  setAzimuth(AZIMUTH0)
                  setElevation(ELEVATION0)
                  setZoom(1)
                  setPan({ x: 0, y: 0 })
                }}>
          전체
        </button>
      </div>
      <svg
        width="100%"
        height={height}
        viewBox={`0 0 ${view.width} ${view.height}`}
        style={{ display: 'block', cursor: drag.current ? 'grabbing' : 'grab',
                 touchAction: 'none' }}
        onPointerDown={(event) => {
          drag.current = {
            x: event.clientX, y: event.clientY, az: azimuth, el: elevation,
            pan, // Shift 나 가운데 단추면 **옮기기** — 돌리기와 손이 갈린다.
            move: event.shiftKey || event.button === 1,
          }
          event.currentTarget.setPointerCapture(event.pointerId)
        }}
        onPointerMove={(event) => {
          const from = drag.current
          if (!from) return
          if (from.move) {
            setPan({ x: from.pan.x + (event.clientX - from.x),
                     y: from.pan.y + (event.clientY - from.y) })
            return
          }
          setAzimuth(from.az + (event.clientX - from.x) * 0.5)
          // 고도는 위아래로 넘어가면 상자가 뒤집혀서 눈금이 거꾸로 붙는다.
          // 5° 아래로 내려가면 상자가 납작해져 깊이가 사라지고, 0 을 지나면
          // 통째로 뒤집혀 눈금이 거꾸로 붙는다.  위쪽도 85 에서 멈춘다 —
          // 90 은 위에서 내려다본 그림이라 세로축이 점이 된다.
          setElevation(Math.max(5, Math.min(85,
            from.el - (event.clientY - from.y) * 0.4)))
        }}
        onPointerUp={(event) => {
          drag.current = null
          event.currentTarget.releasePointerCapture(event.pointerId)
        }}

      >
        {/* 상자.  열두 모서리를 옅게 — 이것이 "여기가 3D 다" 를 말하는 전부다. */}
        {EDGES.map(([a, b]) => (
          <path key={`${a}-${b}`} d={line([corners[a]!, corners[b]!])}
                stroke="var(--line)" strokeWidth={1} fill="none" />
        ))}

        {/* 바닥 격자 — 깊이가 눈에 들어오려면 바닥에 선이 있어야 한다. */}
        {xTicks.map((value) => {
          const u = unit.x(value)
          if (u < 0 || u > 1) return null
          return (
            <path key={`gx${value}`}
                  d={line([cube.at(u, 0, 0), cube.at(u, 0, 1)])}
                  stroke="var(--line)" strokeWidth={0.6} strokeDasharray="2 4"
                  fill="none" />
          )
        })}
        {zTickValues.map((value) => {
          const w = unit.z(value)
          if (w < 0 || w > 1) return null
          return (
            <path key={`gz${value}`}
                  d={line([cube.at(0, 0, w), cube.at(1, 0, w)])}
                  stroke="var(--line)" strokeWidth={0.6} strokeDasharray="2 4"
                  fill="none" />
          )
        })}

        {/* 곡선.  **뒤에서 앞으로** 그린다 — 앞의 것이 뒤의 것을 덮어야 깊이가
            읽힌다 (화가 알고리즘). */}
        {[...shown]
          .map((one, index) => ({ one, index }))
          .sort((a, b) => {
            const at = (s: Series3D) => cube.at(0.5, 0.5, unit.z(s.z))
            return at(a.one).y - at(b.one).y
          })
          .map(({ one, index }) => {
            const w = unit.z(one.z)
            const path = one.x.map((value, i) => cube.at(
              unit.x(value), unit.y(one.y[i] ?? 0), w))
            const colour = one.color ?? seriesColor(index)
            return (
              <g key={one.label}>
                <path d={line(path)} stroke={colour} strokeWidth={1.6} fill="none"
                      strokeLinejoin="round" />
                {one.points ? path.filter((_, i) => i % 2 === 0).map((at, i) => (
                  <circle key={i} cx={at.x} cy={at.y} r={1.6} fill={colour} />
                )) : null}
              </g>
            )
          })}

        {/* 눈금 셋. */}
        {xTicks.map((value) => {
          const u = unit.x(value)
          if (u < 0 || u > 1) return null
          const t = (uEdge[0] === 0 || uEdge[0] === 3 || uEdge[0] === 4 || uEdge[0] === 7)
            ? u : 1 - u
          const { on, out } = tickAt(uEdge, t, 12)
          return (
            <g key={`tx${value}`}>
              <path d={line([on, out])} stroke="var(--muted)" strokeWidth={1} />
              <text x={out.x} y={out.y + 4} textAnchor="middle"
                    className="plot3d-tick">{num(value, 3)}</text>
            </g>
          )
        })}
        {yTicks.map((value) => {
          const v = unit.y(value)
          if (v < 0 || v > 1) return null
          const t = (vEdge[0] === 0 || vEdge[0] === 1 || vEdge[0] === 4 || vEdge[0] === 5)
            ? v : 1 - v
          const { on, out } = tickAt(vEdge, t, 12)
          return (
            <g key={`ty${value}`}>
              <path d={line([on, out])} stroke="var(--muted)" strokeWidth={1} />
              <text x={out.x - 4} y={out.y + 4} textAnchor="end"
                    className="plot3d-tick">{num(value, 3)}</text>
            </g>
          )
        })}
        {zTickValues.map((value) => {
          const w = unit.z(value)
          if (w < 0 || w > 1) return null
          const t = (wEdge[0] === 0 || wEdge[0] === 1 || wEdge[0] === 2 || wEdge[0] === 3)
            ? w : 1 - w
          const { on, out } = tickAt(wEdge, t, 14)
          return (
            <g key={`tz${value}`}>
              <path d={line([on, out])} stroke="var(--muted)" strokeWidth={1} />
              <text x={out.x} y={out.y + 4} textAnchor="middle"
                    className="plot3d-tick">
                {zTickLabel ? zTickLabel(value) : num(value, 3)}
              </text>
            </g>
          )
        })}

        {/* 축 이름 — 각 모서리의 가운데에서 더 바깥으로. */}
        <text {...(() => { const { out } = tickAt(uEdge, 0.5, 38); return { x: out.x, y: out.y } })()}
              textAnchor="middle" className="plot3d-axis">{xLabel}</text>
        <text {...(() => { const { out } = tickAt(vEdge, 0.5, 46); return { x: out.x, y: out.y } })()}
              textAnchor="middle" className="plot3d-axis">{yLabel}</text>
        <text {...(() => { const { out } = tickAt(wEdge, 0.5, 40); return { x: out.x, y: out.y } })()}
              textAnchor="middle" className="plot3d-axis">{zLabel}</text>
      </svg>
      <div className="tiny faint" style={{ padding: '2px 10px 0' }}>
        끌어서 돌리고, <b>Shift</b>+끌어서 옮기고, 휠이나 🔍 로 상자째
        확대합니다 · 방위 {((azimuth % 360) + 360) % 360 > 180
          ? (((azimuth % 360) + 360) % 360) - 360
          : ((azimuth % 360) + 360) % 360}° · 고도 {elevation.toFixed(0)}°
      </div>
    </div>
  )
}
