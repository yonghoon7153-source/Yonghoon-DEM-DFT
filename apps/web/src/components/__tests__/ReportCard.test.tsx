/** The report card's controls have to do what they advertise.
 *
 * The toolbar used to carry a second `판정 근거 N건` <details> with an empty
 * body: styled like every other disclosure, arrow and all, opening onto
 * nothing while the real evidence list sat at the bottom of the card.
 */

import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { ReportCard } from '../ReportCard'
import type { Report, ResolvedCell } from '../../lib/types'

const CELL: ResolvedCell = {
  active_mass_g: null,
  active_wt_percent: null,
  composition: [],
  composition_label: '',
  composition_compact_label: '',
  composition_problems: [],
  area_cm2: null,
  volume_cm3: null,
  loading_mg_cm2: null,
  nominal_capacity_mah: null,
  nominal_specific_capacity_mah_g: null,
  available_bases: ['mAh'],
  unavailable: {},
  notes: {},
}

const REPORT: Report = {
  sample_id: 1,
  sample_name: 'No_1_dry',
  state: 'finished',
  state_confidence: 'high',
  state_summary: 'finished',
  evidence: [
    { signal: 'schedule', detail: 'planned cycles reached', points_to: 'finished' },
    { signal: 'recency', detail: 'last sample is old', points_to: 'finished' },
  ],
  cycles_observed: 44,
  cycles_complete: 44,
  planned_cycles: 44,
  in_progress_cycle: null,
  reference_cycle_requested: 3,
  reference_available: true,
  retention_pct: 69.4,
  retention_note: '',
  basis: 'mAh',
  basis_label: 'mAh',
  reported: {
    cycle: 44,
    discharge_capacity: 3.64,
    charge_capacity: 3.68,
    discharge_capacity_mah: 3.64,
    charge_capacity_mah: 3.68,
    coulombic_efficiency: 98.9,
    energy_efficiency: null,
    mean_discharge_voltage: 3.71,
    complete: true,
  },
  reference: {
    cycle: 3,
    discharge_capacity: 5.25,
    charge_capacity: 5.3,
    discharge_capacity_mah: 5.25,
    charge_capacity_mah: 5.3,
    coulombic_efficiency: 99.1,
    energy_efficiency: null,
    mean_discharge_voltage: 3.78,
    complete: true,
  },
  first_cycle: null,
  knee: null,
  resolved_cell: CELL,
}

describe('ReportCard', () => {
  it('has no disclosure that opens onto nothing', () => {
    const { container } = render(<ReportCard report={REPORT} />)
    const disclosures = [...container.querySelectorAll('details')]
    expect(disclosures.length).toBeGreaterThan(0)
    for (const details of disclosures) {
      expect(details.querySelector('summary')).not.toBeNull()
      // A summary and at least one thing to reveal.
      expect(details.children.length).toBeGreaterThan(1)
    }
  })

  it('states the evidence count without pretending to be expandable', () => {
    const { container } = render(<ReportCard report={REPORT} />)
    const count = screen.getByText('판정 근거 2건')
    expect(count.closest('details')).toBeNull()
    // The one disclosure that is left is the one holding the evidence list.
    expect(container.querySelectorAll('.evidence li')).toHaveLength(2)
  })
})

// --- 완료된 사이클이 하나도 없을 때 -------------------------------------------
//
// 실측: multi-step CCCV 파일(260630_MJ1, 41,738행)에 방전이 한 번도 없었다.
// 화면은 지표가 전부 — 이고 아무 설명이 없었다.  전부 맞는 말인데 **왜** 가
// 없어서 파싱 실패로 읽혔다.

function empty(reason: string): Report {
  return {
    ...REPORT,
    state: 'finished',
    cycles_complete: 0,
    in_progress_cycle: null,
    retention_pct: null,
    reported: null,
    reference: null,
    first_cycle: null,
    no_complete_reason: reason,
  }
}

describe('숫자가 하나도 없을 때', () => {
  it('방전이 없다고 말한다 — 그리고 그것이 계산에 무슨 뜻인지도', () => {
    render(<ReportCard report={empty('no_discharge')} />)
    expect(screen.getByText(/방전이 없습니다/)).toBeInTheDocument()
    // 무엇을 못 내는지까지 적어야 "고장" 이 아니라 "그런 실험" 으로 읽힌다.
    expect(screen.getByText(/사이클 용량·유지율·쿨롱효율/)).toBeInTheDocument()
  })

  it('잘린 것과 방전이 없는 것을 다르게 말한다', () => {
    // 하나는 기다리면 되고 하나는 영영 안 된다.  같은 문장으로 덮으면 안 된다.
    const { unmount } = render(<ReportCard report={empty('truncated')} />)
    expect(screen.getByText(/이어지는 파일/)).toBeInTheDocument()
    unmount()

    render(<ReportCard report={empty('no_discharge')} />)
    expect(screen.queryByText(/이어지는 파일/)).toBeNull()
  })

  it('지표 밑의 문구도 이유를 안다', () => {
    render(<ReportCard report={empty('no_discharge')} />)
    expect(screen.getByText('방전이 없어 사이클 용량이 없습니다')).toBeInTheDocument()
  })

  it('완료된 사이클이 있으면 이 줄은 안 나온다', () => {
    render(<ReportCard report={REPORT} />)
    expect(screen.queryByText(/방전이 없습니다/)).toBeNull()
  })
})


describe('DBW onset·point (ADR 0021)', () => {
  const dbw = {
    method: 'dbw' as const,
    cycle: 24.2,
    detected: true,
    reason:
      'fade leaves its early trend at cycle 20 (onset) and settles in by cycle 24, ' +
      'steepening 8.00x (-0.100 -> -0.800 %/cycle)',
    detail: {},
    status: 'detected' as const,
    candidate_cycle: 24.2,
    onset_cycle: 20.4,
  }
  const withKnee: Report = {
    ...REPORT,
    knee: {
      primary: dbw,
      results: [dbw],
      reference_cycle: 3,
      reference_capacity_mah: 5.25,
      search_start_cycle: 3,
      n_points: 44,
      fade_rate_early_pct_per_cycle: -0.1,
      fade_rate_late_pct_per_cycle: -0.8,
      projected_cycle_at_80pct: null,
      reference_note: '',
    },
  }

  it('타일이 onset→point 쌍을 보여 준다', () => {
    render(<ReportCard report={withKnee} />)
    expect(screen.getByText('20.4→24.2')).toBeInTheDocument()
  })

  it('onset 이 없으면 point 하나만 보인다', () => {
    const single = { ...dbw, onset_cycle: null }
    render(
      <ReportCard
        report={{ ...withKnee, knee: { ...withKnee.knee!, primary: single, results: [single] } }}
      />,
    )
    expect(screen.getByText('24.2')).toBeInTheDocument()
    // 열화율 지표의 "a → b" 는 화살표 양옆에 공백이 있다; knee 쌍(공백 없음)만 본다.
    expect(screen.queryByText(/\d→/)).not.toBeInTheDocument()
  })
})
