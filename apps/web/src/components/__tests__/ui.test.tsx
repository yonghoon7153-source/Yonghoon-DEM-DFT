import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { CapacityMetric, Metric, StateBadge } from '../ui'

describe('StateBadge', () => {
  it('names the state in Korean and shows the live cycle', () => {
    render(<StateBadge state="running" cycle={45} />)
    expect(screen.getByText(/구동 중 · 45번째 진행/)).toBeInTheDocument()
  })

  it('marks a finished cell without a cycle', () => {
    render(<StateBadge state="finished" />)
    expect(screen.getByText('사이클 종료')).toBeInTheDocument()
  })

  it('does not claim a state it cannot determine', () => {
    render(<StateBadge state="unknown" />)
    expect(screen.getByText('상태 불명')).toBeInTheDocument()
  })
})

describe('Metric', () => {
  it('renders a value with its unit and note', () => {
    render(<Metric label="유지율" value="69.4" unit="%" note="44번 vs 3번" />)
    expect(screen.getByText('유지율')).toBeInTheDocument()
    expect(screen.getByText('69.4')).toBeInTheDocument()
    expect(screen.getByText('44번 vs 3번')).toBeInTheDocument()
  })
})

describe('CapacityMetric', () => {
  it('labels the unit from the basis', () => {
    render(<CapacityMetric label="방전용량" value={207.68} basis="mAh/g" />)
    expect(screen.getByText('207.7')).toBeInTheDocument()
    expect(screen.getByText('mAh g⁻¹')).toBeInTheDocument()
  })

  it('shows a dash instead of inventing a number', () => {
    render(<CapacityMetric label="방전용량" value={null} basis="mAh" />)
    expect(screen.getByText('—')).toBeInTheDocument()
  })
})
