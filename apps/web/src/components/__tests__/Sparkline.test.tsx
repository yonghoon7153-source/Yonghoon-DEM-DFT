import { render } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { Sparkline } from '../Sparkline'

function paths(container: HTMLElement): SVGPathElement[] {
  return [...container.querySelectorAll('path')] as SVGPathElement[]
}

/** The second path is the line; the first is the area fill beneath it. */
function linePath(container: HTMLElement): string {
  return paths(container)[1]?.getAttribute('d') ?? ''
}

describe('Sparkline', () => {
  it('draws a line and a fill for a real series', () => {
    const { container } = render(<Sparkline values={[100, 98, 95, 80]} />)
    expect(paths(container)).toHaveLength(2)
    expect(container.querySelector('circle')).toBeInTheDocument()
  })

  it('falls back to a dashed rule when there is nothing to draw', () => {
    const { container } = render(<Sparkline values={[]} />)
    expect(paths(container)).toHaveLength(0)
    expect(container.querySelector('line')).toHaveAttribute('stroke-dasharray')
  })

  it('survives a flat series without dividing by zero', () => {
    const { container } = render(<Sparkline values={[100, 100, 100]} />)
    expect(linePath(container)).not.toContain('NaN')
  })

  it('skips gaps rather than plotting them as zero', () => {
    const { container } = render(<Sparkline values={[100, null, 90, null, 80]} />)
    // Three real points: one move-to and two line-tos.
    expect(linePath(container).match(/L/g) ?? []).toHaveLength(2)
  })

  it('marks the knee when one is given', () => {
    const { container } = render(
      <Sparkline values={[100, 99, 98, 80, 60]} markIndex={3} />,
    )
    expect(container.querySelector('line[stroke-dasharray]')).toBeInTheDocument()
  })

  it('ignores a mark outside the series', () => {
    const { container } = render(<Sparkline values={[100, 90]} markIndex={9} />)
    expect(container.querySelector('line[stroke-dasharray]')).not.toBeInTheDocument()
  })
})
