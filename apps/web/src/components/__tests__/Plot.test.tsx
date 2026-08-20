/** Colour regressions for the plot.
 *
 * A canvas has no cascade, so every colour the plot draws with is resolved to a
 * literal at build time.  Both cases here are ways that resolution used to end
 * up wrong on a dark surface: a light-only palette hex handed in by the caller
 * and drawn as-is, and axis colours frozen at the scheme the page was opened
 * with.
 */

import { act, render } from '@testing-library/react'
import { existsSync, readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { SERIES_COLORS } from '../../lib/format'

// uPlot needs a real canvas; capturing the options it would have been built
// with is what these assertions are about anyway.
type BuiltOptions = { series: { stroke: string }[]; axes: { stroke: string }[] }
const built = vi.hoisted(() => [] as { options: BuiltOptions }[])

vi.mock('uplot', () => {
  class FakePlot {
    constructor(options: unknown) {
      built.push({ options: options as BuiltOptions })
    }
    destroy() {}
  }
  return { default: FakePlot }
})

import { Plot, PlotLegend, pointAt, splitAxisLabel } from '../Plot'
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
