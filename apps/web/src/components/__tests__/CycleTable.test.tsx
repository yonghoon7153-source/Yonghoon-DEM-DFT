/** 사이클 표의 단차 열 — 그럴듯한 잘못된 숫자를 막는 검사들.
 *
 * 여기서 틀리면 예외가 아니라 화면에 멀쩡히 찍힌 숫자로 나타난다. 부호를
 * 지우면 활성화(용량 증가)와 열화가 같아 보이고, 빈칸 대신 0 을 찍으면
 * "변화 없음" 과 "비교할 것이 없음" 이 같아 보이며, 사이의 사이클이 빠진
 * 단차에 표시가 없으면 다섯 사이클치 열화를 한 사이클로 읽는다.
 */

import { render, screen, within } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { CycleTable } from '../CycleTable'
import type { Cycle } from '../../lib/types'

function cycle(overrides: Partial<Cycle> = {}): Cycle {
  return {
    cycle: 2,
    cycle_index: 1,
    run_id: 1,
    charge_capacity: 5.4,
    discharge_capacity: 5.25,
    charge_capacity_mah: 5.4,
    discharge_capacity_mah: 5.25,
    coulombic_efficiency: 97.2,
    energy_efficiency: 91.1,
    charge_energy_mwh: 20,
    discharge_energy_mwh: 18,
    mean_charge_voltage: 3.9,
    mean_discharge_voltage: 3.6,
    voltage_hysteresis: 0.3,
    voltage_max: 4.3,
    voltage_min: 2.5,
    retention_pct: 100,
    c_rate: 0.2,
    temperature_mean: 25,
    duration_h: 10,
    n_points: 500,
    complete: true,
    ...overrides,
  }
}

function rowFor(number: number) {
  const cell = screen.getByText(String(number), { selector: 'td.text' })
  return cell.closest('tr') as HTMLElement
}

/** `+` 와 숫자가 서로 다른 텍스트 노드라 문자열 하나로는 못 찾는다.  칸의
 *  textContent 로 본다 — 사람이 화면에서 읽는 것이 그것이다. */
function cellTexts(row: HTMLElement): string[] {
  return [...row.querySelectorAll('td')].map((td) => (td.textContent ?? '').trim())
}

describe('사이클 표 · 단차', () => {
  it('손실은 음수로, 부호를 붙여 보여 준다', () => {
    render(
      <CycleTable
        basis="mAh"
        cycles={[
          cycle({ cycle: 1, discharge_delta: null, delta_base_cycle: null }),
          cycle({ cycle: 2, discharge_delta: -0.25, delta_base_cycle: 1, delta_span: 1 }),
        ]}
      />,
    )
    expect(cellTexts(rowFor(2))).toContain('-0.25')
  })

  it('증가는 + 로 보여 준다 — 활성화와 열화는 다른 일이다', () => {
    // 초기 사이클에 용량이 오르는 셀이 실제로 있다.  절대값으로 찍으면
    // 그것이 열화와 구분되지 않는다.
    render(
      <CycleTable
        basis="mAh"
        cycles={[cycle({ cycle: 2, discharge_delta: 0.3, delta_base_cycle: 1, delta_span: 1 })]}
      />,
    )
    expect(cellTexts(rowFor(2))).toContain('+0.30')
  })

  it('비교할 것이 없으면 0 이 아니라 빈칸이다', () => {
    // 0 은 "변화가 없었다" 로 읽힌다.  첫 사이클은 그런 뜻이 아니다.
    render(
      <CycleTable
        basis="mAh"
        cycles={[cycle({ cycle: 1, discharge_delta: null, discharge_delta_pct: null,
                         charge_delta: null, delta_base_cycle: null, delta_span: 0 })]}
      />,
    )
    const texts = cellTexts(rowFor(1))
    expect(texts).not.toContain('0')
    expect(texts.filter((t) => t === '—').length).toBeGreaterThanOrEqual(3)
  })

  it('구동 중인 사이클도 빈칸이다', () => {
    // 잘린 사이클의 용량은 파일이 끝난 순간까지 쌓인 부분값이다.  빼면
    // 급사처럼 보인다.
    render(
      <CycleTable
        basis="mAh"
        cycles={[cycle({ cycle: 9, complete: false, discharge_delta: null,
                         charge_delta: null, delta_base_cycle: null })]}
      />,
    )
    expect(within(rowFor(9)).getByText('진행 중')).toBeInTheDocument()
    expect(cellTexts(rowFor(9)).filter((t) => t === '—').length).toBeGreaterThanOrEqual(3)
  })

  it('사이의 사이클이 빠진 단차에는 몇 사이클치인지 표시한다', () => {
    // 3 → 8 은 다섯 사이클치 열화다.  표시가 없으면 한 사이클치로 읽힌다.
    render(
      <CycleTable
        basis="mAh"
        cycles={[cycle({ cycle: 8, discharge_delta: -0.5, delta_base_cycle: 3,
                         delta_span: 5, discharge_delta_per_cycle: -0.1 })]}
      />,
    )
    expect(within(rowFor(8)).getByText('×5')).toBeInTheDocument()
    // 몇 사이클치인지·사이클당 얼마인지는 툴팁이 말해 준다.
    const cell = [...rowFor(8).querySelectorAll('td')].find((td) => td.title.includes('3번 대비'))
    expect(cell?.title).toContain('5사이클치')
  })

  it('이웃한 사이클에는 표시를 붙이지 않는다', () => {
    render(
      <CycleTable
        basis="mAh"
        cycles={[cycle({ cycle: 2, discharge_delta: -0.25, delta_base_cycle: 1, delta_span: 1 })]}
      />,
    )
    expect(within(rowFor(2)).queryByText('×1')).not.toBeInTheDocument()
  })

  it('머리글이 표의 기준 단위를 따라간다', () => {
    render(<CycleTable basis="mAh/g" cycles={[cycle()]} />)
    // basisUnit 이 mAh/g 를 'mAh g⁻¹' 로 쓴다 — 표 전체가 같은 표기를 쓰므로
    // 단차 머리글만 다른 표기를 쓰면 그것이 버그다.
    const headers = [...document.querySelectorAll('th')].map((th) => th.textContent ?? '')
    const discharge = headers.find((h) => h.startsWith('방전 ('))
    expect(headers).toContain(`Δ${discharge}`)
    const charge = headers.find((h) => h.startsWith('충전 ('))
    expect(headers).toContain(`Δ${charge}`)
  })

  it('필드가 없는 옛 응답에서도 표가 깨지지 않는다', () => {
    // 갱신 전 서버가 아직 떠 있는 경우.  단차 열은 비어야지, 화면이 죽으면
    // 안 된다.
    const legacy = cycle()
    delete (legacy as Partial<Cycle>).discharge_delta
    delete (legacy as Partial<Cycle>).delta_span
    render(<CycleTable basis="mAh" cycles={[legacy]} />)
    // 표는 그려지고, 단차 칸만 비어 있어야 한다.
    expect(cellTexts(rowFor(2))).toContain('5.250')
    expect(cellTexts(rowFor(2)).filter((t) => t === '—').length).toBeGreaterThanOrEqual(3)
  })
})
