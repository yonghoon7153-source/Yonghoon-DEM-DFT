/** A capacity-fade curve small enough to sit inside a table cell.
 *
 * A retention percentage tells you where a cell is; the shape tells you how it
 * got there. Two cells at 80 % — one fading steadily, one that fell off a
 * cliff at cycle 22 — need different attention, and only the shape shows that.
 */

import { useId, useMemo } from 'react'

interface Props {
  values: (number | null)[]
  width?: number
  height?: number
  color?: string
  /** Cycle index (0-based into `values`) to mark, e.g. the detected knee. */
  markIndex?: number | null
  title?: string
}

export function Sparkline({
  values,
  width = 108,
  height = 26,
  color,
  markIndex = null,
  title,
}: Props) {
  const gradientId = useId()

  const shape = useMemo(() => {
    const points = values
      .map((value, index) => ({ value, index }))
      .filter((p): p is { value: number; index: number } => p.value !== null)
    if (points.length < 2) return null

    const ys = points.map((p) => p.value)
    const min = Math.min(...ys)
    const max = Math.max(...ys)
    // A flat series would divide by zero; draw it down the middle instead.
    const span = max - min || 1
    const lastIndex = values.length - 1 || 1
    const pad = 2

    const x = (index: number) => (index / lastIndex) * (width - pad * 2) + pad
    const y = (value: number) =>
      height - pad - ((value - min) / span) * (height - pad * 2)

    const line = points.map((p, i) => `${i ? 'L' : 'M'}${x(p.index).toFixed(1)},${y(p.value).toFixed(1)}`)
    const first = points[0]!
    const last = points.at(-1)!
    const area =
      `${line.join('')}L${x(last.index).toFixed(1)},${height}` +
      `L${x(first.index).toFixed(1)},${height}Z`

    return {
      line: line.join(''),
      area,
      mark:
        markIndex !== null && markIndex >= 0 && markIndex <= lastIndex
          ? x(markIndex)
          : null,
      end: { x: x(last.index), y: y(last.value) },
    }
  }, [values, width, height, markIndex])

  if (!shape) {
    return (
      <svg className="sparkline" width={width} height={height} aria-hidden="true">
        <line
          x1={2}
          y1={height / 2}
          x2={width - 2}
          y2={height / 2}
          stroke="var(--line)"
          strokeDasharray="2 3"
        />
      </svg>
    )
  }

  const stroke = color ?? 'var(--accent)'
  return (
    <svg className="sparkline" width={width} height={height} role="img" aria-label={title}>
      {title ? <title>{title}</title> : null}
      <defs>
        <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={stroke} stopOpacity="0.20" />
          <stop offset="100%" stopColor={stroke} stopOpacity="0" />
        </linearGradient>
      </defs>
      <path d={shape.area} fill={`url(#${gradientId})`} />
      {shape.mark !== null ? (
        <line
          x1={shape.mark}
          y1={1}
          x2={shape.mark}
          y2={height - 1}
          stroke="var(--warn)"
          strokeWidth={1}
          strokeDasharray="2 2"
        />
      ) : null}
      <path d={shape.line} fill="none" stroke={stroke} strokeWidth={1.4}
            strokeLinejoin="round" strokeLinecap="round" />
      <circle cx={shape.end.x} cy={shape.end.y} r={1.9} fill={stroke} />
    </svg>
  )
}
