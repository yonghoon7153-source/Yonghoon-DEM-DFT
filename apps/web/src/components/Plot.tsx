/** uPlot wrapper.
 *
 * uPlot is imperative, so this is the one place that talks to it.  Series are
 * given as independent (x, y) pairs because charge and discharge branches do
 * not share an x grid -- uPlot wants one shared x, so each series is aligned
 * onto a merged, sorted x axis with nulls where it has no sample.
 */

import { useEffect, useMemo, useRef } from 'react'
import uPlot from 'uplot'
import 'uplot/dist/uPlot.min.css'

import { useElementWidth } from '../lib/hooks'
import { seriesColor } from '../lib/format'

export interface PlotSeries {
  label: string
  x: number[]
  y: number[]
  color?: string
  dash?: number[]
  width?: number
  points?: boolean
  hidden?: boolean
  /** Draw across x positions this series has no sample at.  Defaults to true. */
  spanGaps?: boolean
}

export interface PlotMarker {
  x: number
  label: string
  color?: string
}

interface Props {
  series: PlotSeries[]
  xLabel: string
  yLabel: string
  height?: number
  markers?: PlotMarker[]
  yRange?: [number | null, number | null]
  legend?: boolean
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

export function Plot({
  series,
  xLabel,
  yLabel,
  height = 340,
  markers = [],
  yRange,
  legend = false,
}: Props) {
  const [wrapRef, width] = useElementWidth<HTMLDivElement>()
  const plotRef = useRef<uPlot | null>(null)
  const nodeRef = useRef<HTMLDivElement>(null)

  const visible = useMemo(() => series.filter((s) => !s.hidden && s.x.length > 0), [series])

  const data = useMemo(() => {
    if (!visible.length) return null
    const axis = mergeX(visible)
    if (!axis.length) return null
    return [axis, ...visible.map((item) => alignY(item, axis))] as uPlot.AlignedData
  }, [visible])

  useEffect(() => {
    const node = nodeRef.current
    if (!node || !data || width < 80) return

    const text = cssVar('--text-dim', '#5b6878')
    const grid = cssVar('--border', '#dfe3ea')

    const options: uPlot.Options = {
      width,
      height,
      legend: { show: legend },
      cursor: { drag: { x: true, y: true, uni: 20 }, focus: { prox: 24 } },
      scales: {
        x: { time: false },
        y: {
          range: yRange
            ? (_u, min, max) => [yRange[0] ?? min, yRange[1] ?? max]
            : undefined,
        },
      },
      axes: [
        {
          label: xLabel,
          labelSize: 30,
          stroke: text,
          grid: { stroke: grid, width: 1 },
          ticks: { stroke: grid, width: 1 },
          font: '11px system-ui, sans-serif',
          labelFont: '12px system-ui, sans-serif',
        },
        {
          label: yLabel,
          labelSize: 44,
          stroke: text,
          grid: { stroke: grid, width: 1 },
          ticks: { stroke: grid, width: 1 },
          font: '11px system-ui, sans-serif',
          labelFont: '12px system-ui, sans-serif',
          size: 62,
        },
      ],
      series: [
        {},
        ...visible.map((item, index) => ({
          label: item.label,
          stroke: item.color ?? seriesColor(index),
          width: item.width ?? 1.6,
          dash: item.dash,
          spanGaps: item.spanGaps ?? true,
          points: { show: item.points ?? false, size: 4 },
        })),
      ],
      hooks: markers.length
        ? {
            draw: [
              (u) => {
                const ctx = u.ctx
                ctx.save()
                for (const marker of markers) {
                  const x = u.valToPos(marker.x, 'x', true)
                  if (!Number.isFinite(x)) continue
                  ctx.strokeStyle = marker.color ?? cssVar('--danger', '#c92a2a')
                  ctx.lineWidth = 1.25
                  ctx.setLineDash([5, 4])
                  ctx.beginPath()
                  ctx.moveTo(x, u.bbox.top)
                  ctx.lineTo(x, u.bbox.top + u.bbox.height)
                  ctx.stroke()
                  ctx.setLineDash([])
                  ctx.fillStyle = marker.color ?? cssVar('--danger', '#c92a2a')
                  ctx.font = '11px system-ui, sans-serif'
                  ctx.textAlign = 'left'
                  ctx.fillText(marker.label, x + 4, u.bbox.top + 12)
                }
                ctx.restore()
              },
            ],
          }
        : undefined,
    }

    plotRef.current?.destroy()
    plotRef.current = new uPlot(options, data, node)
    return () => {
      plotRef.current?.destroy()
      plotRef.current = null
    }
  }, [data, visible, width, height, xLabel, yLabel, markers, yRange, legend])

  return (
    <div ref={wrapRef} className="plot-shell">
      {data ? (
        <div ref={nodeRef} />
      ) : (
        <div className="empty" style={{ height }}>
          그릴 데이터가 없습니다.
        </div>
      )}
    </div>
  )
}

interface LegendProps {
  series: PlotSeries[]
  onToggle?: (label: string) => void
}

/** A compact chip legend; uPlot's own legend is too tall for many series. */
export function PlotLegend({ series, onToggle }: LegendProps) {
  if (series.length <= 1) return null
  return (
    <div className="legend-chips">
      {series.map((item, index) => (
        <button
          key={item.label}
          type="button"
          className={`legend-chip${item.hidden ? ' off' : ''}`}
          onClick={() => onToggle?.(item.label)}
          title={item.hidden ? '표시' : '숨기기'}
        >
          <span
            className="swatch"
            style={{ background: item.color ?? seriesColor(index) }}
          />
          {item.label}
        </button>
      ))}
    </div>
  )
}
