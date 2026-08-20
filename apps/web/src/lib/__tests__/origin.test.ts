/** Origin 붙여넣기 블록.
 *
 * 여기서 틀리면 그래프가 조용히 이상해진다 — 곡선 끝에서 다음 곡선 시작으로
 * 선이 날아가거나, 없는 값이 0 으로 찍히거나, 잘린 사이클의 부분값이 점 하나로
 * 남거나.
 */

import { describe, expect, it } from 'vitest'

import { dischargeTsv, efficiencyTsv, profileTsv, tsvColumns } from '../origin'
import type { Cycle, ProfileSeries } from '../types'

function series(overrides: Partial<ProfileSeries> = {}): ProfileSeries {
  return {
    cycle: 3,
    branch: 'discharge',
    basis: 'mAh/g',
    points: 3,
    capacity: [0, 1, 2],
    voltage: [4.3, 3.7, 2.5],
    run_id: 1,
    label: '3번 방전',
    ...overrides,
  }
}

function cycle(overrides: Partial<Cycle> = {}): Cycle {
  return {
    cycle: 1,
    cycle_index: 0,
    run_id: 1,
    charge_capacity: 5.1,
    discharge_capacity: 4.9,
    charge_capacity_mah: 5.1,
    discharge_capacity_mah: 4.9,
    coulombic_efficiency: 96.1,
    energy_efficiency: 91.0,
    charge_energy_mwh: 19.0,
    discharge_energy_mwh: 17.3,
    mean_charge_voltage: 3.9,
    mean_discharge_voltage: 3.7,
    voltage_hysteresis: 0.2,
    voltage_max: 4.3,
    voltage_min: 2.5,
    retention_pct: 100,
    c_rate: null,
    temperature_mean: null,
    duration_h: 4.0,
    n_points: 900,
    complete: true,
    ...overrides,
  }
}

describe('tsvColumns', () => {
  it('숫자만 낸다 — 이름도 단위도 없다', () => {
    // 붙여 넣은 헤더는 Origin 워크시트의 데이터 행에 앉는다.  그리려면 먼저
    // 그 두 줄을 도로 잘라내야 한다.
    expect(tsvColumns([['1', '2']])).toBe('1\n2')
  })

  it('길이가 다른 열은 -- 로 채운다 — 빈칸이나 0 이면 곡선이 원점으로 처박힌다', () => {
    expect(tsvColumns([['1', '2', '3'], ['9']]).split('\n')).toEqual(['1\t9', '2\t--', '3\t--'])
  })

  it('탭으로 나눈다 — Origin 이 열로 읽는 구분자다', () => {
    expect(tsvColumns([['1'], ['2']])).toBe('1\t2')
  })
})

describe('profileTsv', () => {
  it('곡선을 두 열에 쌓고 사이를 -- 로 끊는다', () => {
    const text = profileTsv([
      series({ branch: 'charge', capacity: [0, 1], voltage: [2.5, 4.3] }),
      series({ branch: 'discharge', capacity: [0, 1], voltage: [4.3, 2.5] }),
    ])
    expect(text.split('\n')).toEqual([
      '0\t2.5',
      '1\t4.3',
      // 이 줄이 없으면 Origin 이 앞 곡선의 끝에서 뒤 곡선의 시작으로 선을 긋는다.
      '--\t--',
      '0\t4.3',
      '1\t2.5',
    ])
  })

  it('첫 곡선 앞에는 구분 줄을 넣지 않는다', () => {
    expect(profileTsv([series({ capacity: [0], voltage: [2.5] })]).split('\n')[0]).toBe('0\t2.5')
  })

  it('곡선 길이가 달라도 그냥 이어 붙는다 — 쌓은 것이라 들쭉날쭉할 것이 없다', () => {
    const text = profileTsv([
      series({ capacity: [0, 1, 2], voltage: [4.3, 3.7, 2.5] }),
      series({ cycle: 50, capacity: [0], voltage: [4.3] }),
    ])
    expect(text.split('\n')).toHaveLength(3 + 1 + 1)
  })

  it('그릴 것이 없으면 빈 문자열', () => {
    expect(profileTsv([])).toBe('')
  })
})

describe('사이클 열 두 개', () => {
  it('방전용량은 사이클 번호와 둘만', () => {
    expect(dischargeTsv([cycle({ cycle: 3 })])).toBe('3\t4.9')
  })

  it('쿨롱효율도 사이클 번호와 둘만', () => {
    expect(efficiencyTsv([cycle({ cycle: 3 })])).toBe('3\t96.1')
  })

  it('잘린 사이클은 아예 빼고 준다', () => {
    // 구동 중인 셀의 마지막 사이클은 스텝 도중에 잘려 있다.  그 부분값이 점
    // 하나로 찍히면 그래프가 마지막에 꺾여 내려간다.
    const text = dischargeTsv([cycle({ cycle: 1 }), cycle({ cycle: 2, complete: false })])
    expect(text.split('\n')).toEqual(['1\t4.9'])
  })

  it('값이 없는 칸은 -- 다', () => {
    expect(efficiencyTsv([cycle({ coulombic_efficiency: null })])).toBe('1\t--')
  })

  it('완료된 사이클이 없으면 빈 문자열', () => {
    expect(dischargeTsv([cycle({ complete: false })])).toBe('')
    expect(efficiencyTsv([cycle({ complete: false })])).toBe('')
  })
})
