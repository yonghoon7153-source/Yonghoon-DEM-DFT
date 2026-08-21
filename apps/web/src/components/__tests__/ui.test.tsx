import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { PlotLegend } from '../Plot'

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

describe('PlotLegend', () => {
  const many = Array.from({ length: 30 }, (_, i) => ({
    label: `${i + 1}번 방전`,
    x: [0, 1],
    y: [4, 3],
  }))

  it('곡선이 하나면 범례를 그리지 않는다', () => {
    const { container } = render(<PlotLegend series={many.slice(0, 1)} />)
    expect(container).toBeEmptyDOMElement()
  })

  it('넘치지 않으면 토글을 붙이지 않는다', () => {
    // jsdom 은 레이아웃이 없어 `scrollHeight` 가 늘 0 이다 — 넘치지 않는
    // 경우와 같으므로, 토글이 조건부라는 사실만 여기서 고정한다.
    render(<PlotLegend series={many} />)
    expect(screen.queryByRole('button', { name: /범례 전부 보기/ })).toBeNull()
  })

  it('모든 곡선을 칩으로 낸다 — 잘라내는 것은 높이지 개수가 아니다', () => {
    render(<PlotLegend series={many} />)
    expect(screen.getAllByRole('button')).toHaveLength(many.length)
    expect(screen.getByRole('button', { name: '30번 방전' })).toBeInTheDocument()
  })
})
