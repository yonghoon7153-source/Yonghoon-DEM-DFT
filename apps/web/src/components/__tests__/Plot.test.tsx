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

import { Plot, PlotLegend } from '../Plot'
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
