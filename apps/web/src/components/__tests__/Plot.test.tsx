/** Colour regressions for the plot.
 *
 * A canvas has no cascade, so every colour the plot draws with is resolved to a
 * literal at build time.  Both cases here are ways that resolution used to end
 * up wrong on a dark surface: a light-only palette hex handed in by the caller
 * and drawn as-is, and axis colours frozen at the scheme the page was opened
 * with.
 */

import { act, render, screen } from '@testing-library/react'
import { existsSync, readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { SERIES_COLORS } from '../../lib/format'

// uPlot needs a real canvas; capturing the options it would have been built
// with is what these assertions are about anyway.
//
// The stand-in carries **scales** as well, because the zoom controls read and
// write them.  A fake with no `scales` is not a fake of uPlot -- the component
// would have to defend against a shape that cannot occur, and the defence is
// what the test would then be exercising.
type BuiltOptions = {
  series: { stroke: string }[]
  axes: { stroke: string }[]
  hooks?: { setScale?: ((u: unknown, key: string) => void)[] }
}
type Scale = { min: number; max: number; from?: string }
interface Built {
  options: BuiltOptions
  plot: { scales: Record<string, Scale>; setScale: (key: string, opts: Scale) => void }
}
const built = vi.hoisted(() => [] as Built[])

vi.mock('uplot', () => {
  class FakePlot {
    options: BuiltOptions
    // 0..10 가로, 0..100 세로.  '처음 눈금' 이 무엇이었는지가 이 시험의 전부라
    // 데이터에서 다시 계산하지 않고 여기서 못 박는다.
    scales: Record<string, Scale> = { x: { min: 0, max: 10 }, y: { min: 0, max: 100 } }
    constructor(options: unknown) {
      this.options = options as BuiltOptions
      built.push({ options: this.options, plot: this })
    }
    batch(fn: () => void) {
      fn()
    }
    setScale(key: string, opts: { min: number; max: number }) {
      this.scales[key] = { ...this.scales[key], ...opts }
      for (const hook of this.options.hooks?.setScale ?? []) hook(this, key)
    }
    destroy() {}
  }
  return { default: FakePlot }
})

import { oneRowHeight, Plot, PlotLegend, pointAt, sameView, splitAxisLabel } from '../Plot'
import type { PlotMarker } from '../Plot'

/** jsdom has no layout, so the plot would stay under its 80px width floor. */
function installWidth(width = 600) {
  const previous = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'clientWidth')
  Object.defineProperty(HTMLElement.prototype, 'clientWidth', {
    configurable: true,
    get: () => width,
  })
  return () => {
    if (previous) Object.defineProperty(HTMLElement.prototype, 'clientWidth', previous)
    else delete (HTMLElement.prototype as { clientWidth?: number }).clientWidth
  }
}

/** A controllable `prefers-color-scheme` listener. */
function installMatchMedia() {
  const listeners = new Set<() => void>()
  const previous = globalThis.matchMedia
  globalThis.matchMedia = ((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener() {},
    removeListener() {},
    addEventListener: (_type: string, fn: () => void) => listeners.add(fn),
    removeEventListener: (_type: string, fn: () => void) => listeners.delete(fn),
    dispatchEvent: () => false,
  })) as never
  return {
    flip: () => act(() => listeners.forEach((fn) => fn())),
    restore: () => {
      globalThis.matchMedia = previous
    },
  }
}

const SERIES = [{ label: '8번', x: [0, 1], y: [3.0, 4.2] }]
// Stable identity: the plot rebuilds whenever a prop changes identity, and this
// test is about it rebuilding when nothing but the scheme has.
const MARKERS: PlotMarker[] = []

describe('Plot colours', () => {
  let restoreWidth: (() => void) | undefined

  beforeEach(() => {
    built.length = 0
    restoreWidth = installWidth()
  })

  afterEach(() => {
    restoreWidth?.()
    document.documentElement.removeAttribute('style')
  })

  it('draws a palette colour through its theme token, not the light hex', () => {
    // What the dark block of app.css puts in --series-7; the caller still hands
    // in the light constant, as SampleDetail does via seriesColor().
    document.documentElement.style.setProperty('--series-7', '#9aa4b2')
    render(<Plot series={[{ ...SERIES[0]!, color: SERIES_COLORS[7]! }]} xLabel="x" yLabel="y" />)
    expect(built[0]?.options.series[1]?.stroke).toBe('#9aa4b2')
  })

  it('falls back to the palette index when the caller names no colour', () => {
    document.documentElement.style.setProperty('--series-0', '#60a5fa')
    render(<Plot series={SERIES} xLabel="x" yLabel="y" />)
    expect(built[0]?.options.series[1]?.stroke).toBe('#60a5fa')
  })

  it('leaves a colour that is not from the palette alone', () => {
    render(<Plot series={[{ ...SERIES[0]!, color: '#123456' }]} xLabel="x" yLabel="y" />)
    expect(built[0]?.options.series[1]?.stroke).toBe('#123456')
  })

  it('rebuilds with the new axis colours when the OS scheme flips', () => {
    const media = installMatchMedia()
    try {
      document.documentElement.style.setProperty('--ink-3', '#7d8797')
      render(<Plot series={SERIES} xLabel="x" yLabel="y" markers={MARKERS} />)
      expect(built.at(-1)?.options.axes[0]?.stroke).toBe('#7d8797')

      document.documentElement.style.setProperty('--ink-3', '#778494')
      media.flip()
      expect(built.at(-1)?.options.axes[0]?.stroke).toBe('#778494')
    } finally {
      media.restore()
    }
  })
})

describe('PlotLegend', () => {
  it('swatches a palette colour with its token so the chip follows the theme', () => {
    const { container } = render(
      <PlotLegend
        series={[
          { label: 'a', x: [], y: [], color: SERIES_COLORS[7]! },
          { label: 'b', x: [], y: [] },
        ]}
      />,
    )
    const swatches = container.querySelectorAll<HTMLElement>('.swatch')
    expect(swatches[0]?.style.background).toBe(`var(--series-7, ${SERIES_COLORS[7]!})`)
    expect(swatches[1]?.style.background).toBe(`var(--series-1, ${SERIES_COLORS[1]!})`)
  })
})

describe('범례 한 줄 접기', () => {
  // jsdom 에는 레이아웃이 없어서 offsetHeight 가 전부 0 이다.  렌더링 테스트로는
  // 이 계산이 틀린 것을 볼 수 없어서, 그대로 화면에 나갔다.
  it('칩 높이만으로 자르면 칩이 반토막 난다 — 컨테이너 padding 까지 센다', () => {
    // .legend-chips 는 border-box 이고 위 8px · 아래 12px 를 가진다.  clamp 를
    // 칩 높이 20px 로 두면 padding 이 그 20 을 다 써서 칩 몫이 0 이 되고,
    // 화면에는 칩의 윗동강만 남는다.
    expect(oneRowHeight(20, 8, 12)).toBe(40)
  })

  it('padding 을 못 읽으면 칩 높이만 쓴다 — NaN 이 clamp 를 통째로 날리지 않게', () => {
    expect(oneRowHeight(20, NaN, NaN)).toBe(20)
  })

  it('잴 칩이 없으면 0 — clamp 를 걸지 않는다는 뜻', () => {
    expect(oneRowHeight(0, 8, 12)).toBe(0)
  })
})

describe('app.css series tokens', () => {
  // vitest runs with css: false, so the stylesheet is read as text.  Both
  // candidates because the suite may be started from the repo root or from
  // apps/web.
  const path = ['src/styles/app.css', 'apps/web/src/styles/app.css']
    .map((candidate) => resolve(process.cwd(), candidate))
    .find(existsSync)
  const css = path ? readFileSync(path, 'utf8') : ''
  const [light = '', dark = ''] = css.split('@media (prefers-color-scheme: dark)')

  it('defines every palette slot in both schemes, lifted for the dark surface', () => {
    SERIES_COLORS.forEach((hex, index) => {
      expect(light, `--series-${index} (light)`).toContain(`--series-${index}: ${hex};`)
      const value = dark.match(new RegExp(`--series-${index}:\\s*(#[0-9a-f]{6});`))?.[1]
      expect(value, `--series-${index} (dark)`).toBeDefined()
      expect(value, `--series-${index} (dark)`).not.toBe(hex)
    })
  })
})

// --- 커서 판독기 --------------------------------------------------------------

describe('splitAxisLabel', () => {
  it('축 이름과 단위를 나눈다', () => {
    expect(splitAxisLabel('면적용량 (mAh cm⁻²)')).toEqual({
      name: '면적용량',
      unit: 'mAh cm⁻²',
    })
  })

  it('단위가 없는 축은 이름만 남는다', () => {
    expect(splitAxisLabel('사이클')).toEqual({ name: '사이클', unit: '' })
  })
})

describe('pointAt', () => {
  // 병합 축 위에서 한 계열은 대부분 null 이다 (mergeX 참고).  커서가 닿은
  // 인덱스에 값이 없다고 판독을 포기하면, 프로파일 그래프에서는 거의 언제나
  // 빈 팝업이 뜬다.
  const DATA = [
    [0, 1, 2, 3, 4],
    [10, null, null, 40, null],
  ]

  it('커서가 닿은 자리에 값이 있으면 그대로 읽는다', () => {
    expect(pointAt(DATA, 1, 3)).toEqual({ x: 3, y: 40 })
  })

  it('값이 없으면 가장 가까운 실제 표본으로 물러난다 — 그 표본의 x 와 함께', () => {
    // 2번 인덱스는 비어 있다.  1번(값 없음) → 3번(값 있음) 순으로 밖으로 걷되,
    // 보고하는 x 는 병합 축의 2 가 아니라 그 표본이 실제로 놓인 3 이어야 한다.
    expect(pointAt(DATA, 1, 2)).toEqual({ x: 3, y: 40 })
  })

  it('앞쪽을 먼저 본다 — 같은 거리면 왼쪽 표본', () => {
    expect(pointAt([[0, 1, 2], [5, null, 7]], 1, 1)).toEqual({ x: 0, y: 5 })
  })

  it('표본이 하나도 없는 계열은 null 이다 — 없는 값을 지어내지 않는다', () => {
    expect(pointAt([[0, 1], [null, null]], 1, 0)).toBeNull()
  })
})

/** uPlot 인스턴스 중 판독기가 만지는 부분만. */
function fakeCursor(data: (number | null)[][], idx: number, left = 120, top = 40) {
  return {
    data,
    cursor: { left, top, idx },
    width: 600,
    over: { getBoundingClientRect: () => ({ left: 0, top: 0, width: 600, height: 300 }) },
  }
}

type CursorHooks = {
  hooks: {
    setSeries: ((u: unknown, i: number | null) => void)[]
    setCursor: ((u: unknown) => void)[]
  }
}

describe('커서 판독기', () => {
  let restoreWidth: (() => void) | undefined

  beforeEach(() => {
    built.length = 0
    restoreWidth = installWidth()
  })

  afterEach(() => restoreWidth?.())

  function hover(idx: number, focus: number | null) {
    const options = built.at(-1)?.options as unknown as CursorHooks
    const u = fakeCursor(
      [
        [0, 1, 2],
        [3.0, 4.2, 4.4],
      ],
      idx,
    )
    act(() => options.hooks.setSeries[0]?.(u, focus))
    act(() => options.hooks.setCursor[0]?.(u))
  }

  it('축 이름과 단위를 붙여 x·y 를 적는다', () => {
    render(<Plot series={SERIES} xLabel="사이클" yLabel="면적용량 (mAh cm⁻²)" />)
    hover(1, 1)

    const tip = document.querySelector('.plot-tip') as HTMLElement
    expect(tip).not.toBeNull()
    expect(tip.textContent).toContain('사이클')
    expect(tip.textContent).toContain('1')
    expect(tip.textContent).toContain('4.200 mAh cm⁻²')
  })

  it('어느 계열에도 붙지 않았으면 y 를 적지 않는다 — 커서 높이는 측정값이 아니다', () => {
    render(<Plot series={SERIES} xLabel="사이클" yLabel="전압 (V)" />)
    hover(1, null)

    const tip = document.querySelector('.plot-tip') as HTMLElement
    expect(tip).not.toBeNull()
    expect(tip.textContent).toContain('사이클')
    expect(tip.textContent).not.toContain('V')
  })

  it('그래프를 벗어나면 사라진다', () => {
    render(<Plot series={SERIES} xLabel="사이클" yLabel="전압 (V)" />)
    hover(1, 1)
    expect(document.querySelector('.plot-tip')).not.toBeNull()

    // uPlot 은 마우스가 나가면 커서를 -10 으로 보낸다.
    const options = built.at(-1)?.options as unknown as CursorHooks
    const gone = fakeCursor([[0], [1]], 0, -10, -10)
    act(() => options.hooks.setCursor[0]?.(gone))
    expect(document.querySelector('.plot-tip')).toBeNull()
  })
})

// --- 돋보기 -----------------------------------------------------------------

describe('sameView', () => {
  // 어긋남을 **폭에 견주어** 본다.  dV/dQ 는 1e-9 자리에서 놀고 용량은 1e2 라,
  // 고정 epsilon 은 둘 중 하나에서 반드시 틀린다 -- 큰 축에서는 확대를 못 알아
  // 보고, 작은 축에서는 건드리지도 않은 그래프가 확대된 것으로 나온다.
  it('같은 눈금이면 같다', () => {
    expect(sameView({ x: { min: 0, max: 10 } }, { x: { min: 0, max: 10 } })).toBe(true)
  })

  it('float 왕복 오차는 확대가 아니다', () => {
    expect(sameView({ x: { min: 0, max: 10 } }, { x: { min: 1e-12, max: 10 } })).toBe(true)
  })

  it('1e-9 자리에서도 확대를 알아본다', () => {
    const home = { y: { min: 0, max: 4e-9 } }
    expect(sameView(home, { y: { min: 1e-9, max: 3e-9 } })).toBe(false)
  })

  it('없는 축은 판단하지 않는다 — 사라진 것과 옮겨진 것은 다르다', () => {
    expect(sameView({ x: { min: 0, max: 10 } }, {})).toBe(true)
  })
})

describe('돋보기', () => {
  let restoreWidth: (() => void) | undefined

  beforeEach(() => {
    built.length = 0
    restoreWidth = installWidth()
  })
  afterEach(() => restoreWidth?.())

  const at = () => built.at(-1)!.plot
  const button = (name: string) => screen.getByRole('button', { name })

  it('확대하기 전에는 전체·축소가 꺼져 있다', () => {
    // 켜져 있는데 눌러도 아무 일이 없으면 버튼이 고장 난 것으로 읽힌다.
    render(<Plot series={SERIES} xLabel="x" yLabel="y" />)
    expect(button('확대 초기화')).toBeDisabled()
    expect(button('축소')).toBeDisabled()
    expect(button('확대')).toBeEnabled()
  })

  it('확대하면 두 축이 함께 좁아지고, 전체가 켜진다', () => {
    render(<Plot series={SERIES} xLabel="x" yLabel="y" />)
    act(() => button('확대').click())
    // 0..10 의 60 % 를 가운데에 두면 2..8.
    expect(at().scales.x).toEqual({ min: 2, max: 8 })
    expect(at().scales.y).toEqual({ min: 20, max: 80 })
    expect(button('확대 초기화')).toBeEnabled()
  })

  it('전체는 처음 눈금으로 정확히 돌아간다', () => {
    // "데이터 전체 범위를 다시 계산" 이 아니라 **처음 잡힌 눈금**이어야 한다.
    // uPlot 은 세로축에 여유를 주고 눈금을 예쁜 값으로 스냅하므로, 다시 계산한
    // 값은 처음 그림과 조금씩 다르다 -- 초기화를 눌렀는데 처음과 다르면 그것이
    // 버그다.
    render(<Plot series={SERIES} xLabel="x" yLabel="y" />)
    act(() => button('확대').click())
    act(() => button('확대').click())
    act(() => button('확대 초기화').click())
    expect(at().scales.x).toEqual({ min: 0, max: 10 })
    expect(at().scales.y).toEqual({ min: 0, max: 100 })
    expect(button('확대 초기화')).toBeDisabled()
  })

  it('축소는 처음 범위를 넘지 않는다', () => {
    // 넘어가면 계속 누를 때 데이터가 점점 작아지다 사라지고, 전체와 다른 곳에
    // 멈춘다 -- 같은 "다 보이는 그림" 이 두 개가 된다.
    render(<Plot series={SERIES} xLabel="x" yLabel="y" />)
    act(() => button('확대').click())
    act(() => button('축소').click())
    act(() => button('축소').click())
    expect(at().scales.x).toEqual({ min: 0, max: 10 })
    expect(button('확대 초기화')).toBeDisabled()
  })

  it('구석에서 축소해도 폭은 지키고 자리만 안으로 민다', () => {
    render(<Plot series={SERIES} xLabel="x" yLabel="y" />)
    // 왼쪽 끝을 보고 있는 상태 (드래그 확대로 이렇게 된다).
    act(() => at().setScale('x', { min: 0, max: 2 }))
    act(() => button('축소').click())
    // 폭 2 → 3.33 이지만 왼쪽으로는 더 못 가므로 0 에서 시작한다.
    expect(at().scales.x!.min).toBe(0)
    expect(at().scales.x!.max).toBeCloseTo(10 / 3, 6)
  })

  it('드래그로 확대해도 전체가 켜진다 — 버튼 누른 횟수를 세지 않는다', () => {
    // uPlot 이 스스로 눈금을 바꾸는 길이 셋이다: 드래그 확대, 더블클릭 복귀,
    // 그리고 우리 버튼.  횟수를 세면 앞의 둘을 놓치고, 그때 버튼이 화면과
    // 어긋난 채로 남는다.
    render(<Plot series={SERIES} xLabel="x" yLabel="y" />)
    act(() => at().setScale('x', { min: 3, max: 4 }))
    expect(button('확대 초기화')).toBeEnabled()

    act(() => at().setScale('x', { min: 0, max: 10 }))
    expect(button('확대 초기화')).toBeDisabled()
  })

  it('축이 잠겨 있으면 확대를 끄고 이유를 말한다', () => {
    // 잠금이 걸린 축은 uPlot 이 매 프레임 그 범위를 다시 씌운다.  버튼을 살려
    // 두면 눌러도 그림이 안 바뀌고, 사람은 돋보기가 고장 났다고 읽는다.
    render(<Plot series={SERIES} xLabel="x" yLabel="y" xRange={[0, 5]} yRange={[1, 4]} />)
    expect(button('확대')).toBeDisabled()
    expect(button('확대').title).toContain('축 고정')
  })

  it('한쪽 끝만 잠근 것은 잠금이 아니다 — 반대쪽은 여전히 움직인다', () => {
    render(<Plot series={SERIES} xLabel="x" yLabel="y" yRange={[0, null]} />)
    expect(button('확대')).toBeEnabled()
  })

  it('그릴 것이 없으면 버튼도 없다', () => {
    render(<Plot series={[]} xLabel="x" yLabel="y" />)
    expect(screen.queryByRole('button', { name: '확대' })).toBeNull()
  })
})
