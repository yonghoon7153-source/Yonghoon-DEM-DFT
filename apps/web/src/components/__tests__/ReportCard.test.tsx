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
