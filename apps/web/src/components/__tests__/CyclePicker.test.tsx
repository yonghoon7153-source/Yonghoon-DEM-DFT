import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'

import { CyclePicker } from '../CyclePicker'
import type { Cycle } from '../../lib/types'

function cycle(n: number, discharge: number): Cycle {
  return {
    cycle: n,
    cycle_index: n - 1,
    run_id: 1,
    charge_capacity: discharge + 0.1,
    discharge_capacity: discharge,
    charge_capacity_mah: discharge + 0.1,
    discharge_capacity_mah: discharge,
    coulombic_efficiency: 99.6,
    energy_efficiency: 96.5,
    charge_energy_mwh: 16,
    discharge_energy_mwh: 15,
    mean_charge_voltage: 3.24,
    mean_discharge_voltage: 3.14,
    voltage_hysteresis: 0.1,
    voltage_max: 3.63,
    voltage_min: 1.88,
    retention_pct: 100,
    c_rate: 0.2,
    temperature_mean: null,
    duration_h: 9.6,
    n_points: 3500,
    complete: true,
  }
}

const cycles = [cycle(1, 5.25), cycle(2, 4.92), cycle(3, 4.92), cycle(10, 4.89)]

describe('CyclePicker', () => {
  it('reads the focused cycle back with its capacity', () => {
    render(<CyclePicker cycles={cycles} value={[3]} onChange={() => {}} basis="mAh" />)
    expect(screen.getByText('3번')).toBeInTheDocument()
    expect(screen.getByText(/방전 4.920 mAh/)).toBeInTheDocument()
    expect(screen.getByText(/CE 99.60%/)).toBeInTheDocument()
  })

  it('expands a typed range against the cycles that exist', async () => {
    const onChange = vi.fn()
    render(<CyclePicker cycles={cycles} value={[1]} onChange={onChange} basis="mAh" />)
    const input = screen.getByLabelText('사이클 선택')
    await userEvent.clear(input)
    await userEvent.type(input, '1-3')
    expect(onChange).toHaveBeenLastCalledWith([1, 2, 3])
  })

  it('warns when the selection matches nothing instead of silently clearing', async () => {
    render(<CyclePicker cycles={cycles} value={[1]} onChange={() => {}} basis="mAh" />)
    const input = screen.getByLabelText('사이클 선택')
    await userEvent.clear(input)
    await userEvent.type(input, '900')
    expect(screen.getByText(/선택된 사이클이 없습니다/)).toBeInTheDocument()
  })

  it('offers the last cycle as one click', async () => {
    const onChange = vi.fn()
    render(<CyclePicker cycles={cycles} value={[1]} onChange={onChange} basis="mAh" />)
    await userEvent.click(screen.getByRole('button', { name: '마지막' }))
    expect(onChange).toHaveBeenCalledWith([10])
  })
})
