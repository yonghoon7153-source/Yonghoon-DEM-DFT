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

  it('첫 사이클 과 마지막 은 서로를 밀어내지 않는다', async () => {
    // 한 화면에서 제일 보고 싶은 둘이 어디서 시작했고 지금 어디인가인데,
    // 두 버튼이 선택을 통째로 갈아치우면 그건 손으로 쳐야만 볼 수 있었다.
    const onChange = vi.fn()
    render(<CyclePicker cycles={cycles} value={[1]} onChange={onChange} basis="mAh" />)
    await userEvent.click(screen.getByRole('button', { name: '마지막' }))
    expect(onChange).toHaveBeenCalledWith([1, 10])
  })

  it('이미 골라 둔 사이클을 다시 누르면 뺀다', async () => {
    const onChange = vi.fn()
    render(<CyclePicker cycles={cycles} value={[1, 10]} onChange={onChange} basis="mAh" />)
    await userEvent.click(screen.getByRole('button', { name: '첫 사이클' }))
    expect(onChange).toHaveBeenCalledWith([10])
  })

  it('초기화 는 선택을 비운다', async () => {
    const onChange = vi.fn()
    render(<CyclePicker cycles={cycles} value={[1, 3]} onChange={onChange} basis="mAh" />)
    await userEvent.click(screen.getByRole('button', { name: '초기화' }))
    expect(onChange).toHaveBeenCalledWith([])
  })

  it('전체 는 정말 전체다', async () => {
    // 40개에서 잘려서, 196 사이클짜리 셀이 자기 기록을 다 못 보여 줬다.
    const many = Array.from({ length: 120 }, (_, i) => cycle(i + 1, 5 - i * 0.01))
    const onChange = vi.fn()
    render(<CyclePicker cycles={many} value={[1]} onChange={onChange} basis="mAh" />)
    await userEvent.click(screen.getByRole('button', { name: '전체' }))
    expect(onChange.mock.calls[0]![0]).toHaveLength(120)
  })
})
