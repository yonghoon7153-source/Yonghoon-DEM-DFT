import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { useState } from 'react'
import { describe, expect, it, vi } from 'vitest'

import { CyclePicker } from '../CyclePicker'
import type { Cycle, PartialCycle } from '../../lib/types'

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

/** The picker as the page actually uses it: something else owns the selection.
 *
 * 사이클 표의 행을 누르거나 그 카드의 초기화를 누르면 선택이 밖에서 바뀐다.
 * `value` 를 고정해 두고 테스트하면 그 경로가 통째로 안 보인다. */
function Controlled({ start }: { start: number[] }) {
  const [value, setValue] = useState(start)
  return (
    <>
      <CyclePicker cycles={cycles} value={value} onChange={setValue} basis="mAh" />
      <button type="button" onClick={() => setValue([])}>
        표에서 초기화
      </button>
      <button type="button" onClick={() => setValue([2, 3])}>
        표에서 행 선택
      </button>
      {/* 표의 행은 **토글**이다 (`SampleDetail` 의 `onSelect`).  단추가
          갈아치우기로 바뀐 뒤로, 여럿을 나란히 보는 길은 여기뿐이다. */}
      <button
        type="button"
        onClick={() => setValue((was) => (was.includes(10)
          ? was.filter((c) => c !== 10)
          : [...was, 10].sort((a, b) => a - b)))}
      >
        표에서 행 추가
      </button>
    </>
  )
}

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

  //: 한동안 이 둘은 토글이었다 (선택에 더하고 빼기).  쓰는 사람에게는 누른
  //  것이 안 먹는 것으로 읽혔다 — 열 곡선 위에 한 줄이 더해질 뿐이라 어느
  //  것이 1번인지 안 보이고, 한 번 더 누르면 사라졌다 (F&Q, 2026-08-30).
  it('첫 사이클 은 그 사이클만 남긴다', async () => {
    const onChange = vi.fn()
    render(<CyclePicker cycles={cycles} value={[2, 3, 10]} onChange={onChange} basis="mAh" />)
    await userEvent.click(screen.getByRole('button', { name: '첫 사이클' }))
    expect(onChange).toHaveBeenCalledWith([1])
  })

  it('마지막 도 마찬가지다 — 같은 줄의 단추는 다 갈아치운다', async () => {
    const onChange = vi.fn()
    render(<CyclePicker cycles={cycles} value={[1, 2]} onChange={onChange} basis="mAh" />)
    await userEvent.click(screen.getByRole('button', { name: '마지막' }))
    expect(onChange).toHaveBeenCalledWith([10])
  })

  //: "나타났다가 사라졌다가 해요" 가 이 시험의 이유다.  두 번 눌러도 그대로다.
  it('다시 눌러도 사라지지 않는다', async () => {
    render(<Controlled start={[1, 10]} />)
    const button = screen.getByRole('button', { name: '첫 사이클' })
    await userEvent.click(button)
    expect(screen.getByLabelText('사이클 선택')).toHaveValue('1')
    await userEvent.click(button)
    expect(screen.getByLabelText('사이클 선택')).toHaveValue('1')
  })

  //: 갈아치우기로 바꾸면서 잃을 뻔한 것 — "처음과 지금을 나란히".  그 성질은
  //  사라지지 않고 **사이클 표**로 옮겨 갔다 (행은 여전히 토글이다).  단추만
  //  보고 고치는 사람이 표까지 갈아치우지 않도록 여기서 못 박는다.
  it('처음과 지금을 나란히 보는 길은 표에 남아 있다', async () => {
    render(<Controlled start={[]} />)
    await userEvent.click(screen.getByRole('button', { name: '첫 사이클' }))
    expect(screen.getByLabelText('사이클 선택')).toHaveValue('1')
    await userEvent.click(screen.getByRole('button', { name: '표에서 행 추가' }))
    expect(screen.getByLabelText('사이클 선택')).toHaveValue('1,10')
  })

  //: 켜진 단추는 누를 것이 없어야 한다.  1·10 을 보고 있을 때 `첫 사이클` 이
  //  켜져 보이면, 눌러도 아무 일이 없다고 읽히는데 실제로는 10 이 사라진다.
  it('여럿을 보고 있으면 단추는 켜져 보이지 않는다', () => {
    const { rerender } = render(
      <CyclePicker cycles={cycles} value={[1]} onChange={() => {}} basis="mAh" />)
    expect(screen.getByRole('button', { name: '첫 사이클' })).toHaveClass('on')
    rerender(
      <CyclePicker cycles={cycles} value={[1, 10]} onChange={() => {}} basis="mAh" />)
    expect(screen.getByRole('button', { name: '첫 사이클' })).not.toHaveClass('on')
  })

  it('초기화 는 선택을 비운다', async () => {
    const onChange = vi.fn()
    render(<CyclePicker cycles={cycles} value={[1, 3]} onChange={onChange} basis="mAh" />)
    await userEvent.click(screen.getByRole('button', { name: '초기화' }))
    expect(onChange).toHaveBeenCalledWith([])
  })

  it('밖에서 선택이 바뀌면 입력란이 따라간다', async () => {
    // 표에서 행을 누르는 것과 위에서 타이핑하는 것이 같은 선택이어야 한다.
    // 따로 놀면 그래프는 네 곡선인데 입력란은 열 번 전에 친 것을 보여 준다.
    render(<Controlled start={[1]} />)
    const input = screen.getByLabelText('사이클 선택')
    expect(input).toHaveValue('1')
    await userEvent.click(screen.getByRole('button', { name: '표에서 행 선택' }))
    expect(input).toHaveValue('2,3')
    await userEvent.click(screen.getByRole('button', { name: '표에서 초기화' }))
    expect(input).toHaveValue('')
  })

  it('타이핑한 범위 표기를 되받아쓰지 않는다', async () => {
    // "1-3" 을 치면 위로는 [1,2,3] 이 올라간다.  그걸 그대로 "1,2,3" 으로
    // 되돌려 쓰면 다음 글자를 칠 자리가 사라진다.
    render(<Controlled start={[1]} />)
    const input = screen.getByLabelText('사이클 선택')
    await userEvent.clear(input)
    await userEvent.type(input, '1-3')
    expect(input).toHaveValue('1-3')
  })

  it('입력란을 비우면 선택도 빈다', async () => {
    const onChange = vi.fn()
    render(<CyclePicker cycles={cycles} value={[1, 2]} onChange={onChange} basis="mAh" />)
    await userEvent.clear(screen.getByLabelText('사이클 선택'))
    expect(onChange).toHaveBeenLastCalledWith([])
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

// --- 숫자 없는 사이클 ---------------------------------------------------------

const PARTIAL: PartialCycle[] = [
  { cycle: 11, run_id: 1, reason: 'no_discharge', has_charge: true, has_discharge: false },
]

describe('숫자 없는 사이클 고르기', () => {
  it('안 넘겨 주면 목록에 없다 — 그릴 수 없는 번호를 전체가 집으면 안 된다', async () => {
    const onChange = vi.fn()
    render(<CyclePicker cycles={cycles} value={[]} onChange={onChange} basis="mAh" />)
    await userEvent.click(screen.getByRole('button', { name: '전체' }))
    expect(onChange).toHaveBeenCalledWith([1, 2, 3, 10])
  })

  it('넘겨 주면 전체와 마지막이 그것까지 집는다', async () => {
    const onChange = vi.fn()
    render(
      <CyclePicker
        cycles={cycles}
        value={[]}
        onChange={onChange}
        basis="mAh"
        partial={PARTIAL}
      />,
    )
    await userEvent.click(screen.getByRole('button', { name: '전체' }))
    expect(onChange).toHaveBeenCalledWith([1, 2, 3, 10, 11])
  })

  it('고른 것이 숫자 없는 사이클이면 그렇게 말한다', () => {
    // 숫자 줄이 그냥 사라지면 방금 누른 것이 안 먹은 것으로 읽힌다.
    render(
      <CyclePicker
        cycles={cycles}
        value={[11]}
        onChange={() => {}}
        basis="mAh"
        partial={PARTIAL}
      />,
    )
    expect(screen.getByText('11번')).toBeInTheDocument()
    expect(screen.getByText(/방전 없음 — 곡선은 그리지만/)).toBeInTheDocument()
  })

  it('완료된 사이클을 고르면 평소처럼 숫자가 나온다', () => {
    render(
      <CyclePicker
        cycles={cycles}
        value={[3]}
        onChange={() => {}}
        basis="mAh"
        partial={PARTIAL}
      />,
    )
    expect(screen.getByText(/방전 4.920 mAh/)).toBeInTheDocument()
    expect(screen.queryByText(/곡선은 그리지만/)).toBeNull()
  })
})
