/** Origin 붙여넣기 블록.
 *
 * 여기서 틀리면 그래프가 조용히 이상해진다 — 곡선 끝에서 다음 곡선 시작으로
 * 선이 날아가거나, 없는 값이 0 으로 찍히거나, 잘린 사이클의 부분값이 점 하나로
 * 남거나.
 */

import { describe, expect, it } from 'vitest'

import {
  cycleAndEfficiencyTsv,
  dischargeTsv,
  dqdvTsv,
  efficiencyTsv,
  profileTsv,
  tsvColumns,
  skippedForCopy,
  stillRunning,
} from '../origin'
import type { Cycle, DqdvSeries, ProfileSeries } from '../types'

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

describe('사이클 열 세 개 — 용량과 쿨롱효율을 한 번에', () => {
  it('사이클 · 방전용량 · 쿨롱효율 순서로 나온다', () => {
    // 순서가 곧 계약이다.  붙여 넣는 사람은 열 이름을 못 받으므로(헤더가 없다)
    // 두 번째가 용량이고 세 번째가 효율이라는 것만 믿고 축을 지정한다.
    expect(cycleAndEfficiencyTsv([cycle({ cycle: 3 })])).toBe('3\t4.9\t96.1')
  })

  it('세 열의 길이가 항상 같다 — 값이 비어도 줄이 밀리지 않는다', () => {
    const text = cycleAndEfficiencyTsv([
      cycle({ cycle: 1, coulombic_efficiency: null }),
      cycle({ cycle: 2, discharge_capacity: null }),
    ])
    expect(text.split('\n')).toEqual(['1\t4.9\t--', '2\t--\t96.1'])
  })

  it('잘린 사이클은 세 열에서도 빠진다', () => {
    const text = cycleAndEfficiencyTsv([cycle({ cycle: 1 }), cycle({ cycle: 2, complete: false })])
    expect(text.split('\n')).toEqual(['1\t4.9\t96.1'])
  })

  it('두 열짜리와 사이클 번호가 어긋나지 않는다', () => {
    // 따로 복사해서 손으로 붙이면 어긋날 수 있는 바로 그 지점 — 한쪽에만
    // 빠지는 사이클이 없어야 이 버튼이 존재할 이유가 있다.
    const cycles = [cycle({ cycle: 1 }), cycle({ cycle: 2, complete: false }), cycle({ cycle: 3 })]
    const three = cycleAndEfficiencyTsv(cycles).split('\n')
    const one = dischargeTsv(cycles).split('\n')
    expect(three.map((row) => row.split('\t')[0])).toEqual(one.map((row) => row.split('\t')[0]))
  })

  it('완료된 사이클이 없으면 빈 문자열', () => {
    expect(cycleAndEfficiencyTsv([cycle({ complete: false })])).toBe('')
  })
})

describe('dQ/dV 붙여넣기 블록', () => {
  function curve(overrides: Partial<DqdvSeries> = {}): DqdvSeries {
    return {
      cycle: 3,
      branch: 'discharge',
      basis: 'mAh/g',
      points: 3,
      voltage: [3.0, 3.1, 3.2],
      dqdv: [-1.5, -2.5, -1.0],
      run_id: 1,
      label: '3번 방전',
      voltage_step: 0.005,
      smoothing: 5,
      points_dropped: 0,
      reason: '',
      ...overrides,
    }
  }

  it('전압·dQdV 두 열로 쌓고 곡선 사이를 -- 로 끊는다', () => {
    const text = dqdvTsv([
      curve({ voltage: [3.0, 3.1], dqdv: [-1, -2], points: 2 }),
      curve({ cycle: 50, voltage: [3.0, 3.1], dqdv: [-3, -4], points: 2 }),
    ])
    expect(text.split('\n')).toEqual(['3\t-1', '3.1\t-2', '--\t--', '3\t-3', '3.1\t-4'])
  })

  it('만들지 못한 곡선은 건너뛴다 — 양옆이 빈 구분줄은 그냥 구멍이다', () => {
    const text = dqdvTsv([
      curve({ voltage: [3.0], dqdv: [-1], points: 1 }),
      curve({ cycle: 4, voltage: [], dqdv: [], points: 0, reason: '전압이 안 움직임' }),
    ])
    expect(text).toBe('3\t-1')
  })

  it('그릴 것이 없으면 빈 문자열', () => {
    expect(dqdvTsv([])).toBe('')
    expect(dqdvTsv([curve({ points: 0, voltage: [], dqdv: [] })])).toBe('')
  })

  it('방전의 음수 부호를 지우지 않는다 — 히스테리시스가 거기 있다', () => {
    const text = dqdvTsv([curve({ voltage: [3.0], dqdv: [-2.5], points: 1 })])
    expect(text).toBe('3\t-2.5')
  })
})

describe('아직 끝나지 않은 곡선은 복사하지 않는다', () => {
  // 붙여 넣은 워크시트에는 표시를 붙일 자리가 없다 ('숫자만' 규칙).  구동 중인
  // 셀의 잘린 마지막 곡선은 Origin 안에서 완료 곡선과 구분되지 않고, 커서로
  // 읽은 마지막 값이 그 사이클의 용량으로 읽힌다 (§3).
  const curve = (over: Partial<ProfileSeries>): ProfileSeries =>
    ({ label: 'c', capacity: [0, 1], voltage: [3, 4], points: 2, ...over }) as ProfileSeries

  it('잘린 곡선은 뺀다', () => {
    const text = profileTsv([
      curve({ label: '완료' }),
      curve({ label: '잘림', complete: false, incomplete_reason: 'truncated' }),
    ])
    // 곡선 하나만 남는다 -- 둘이면 사이에 `--` 로 끊긴 줄이 생긴다.
    expect(text.split('\n')).toHaveLength(2)
    expect(text).not.toContain('--')
  })

  it('정상 종료한 곡선은 그대로 낸다', () => {
    // no_discharge 는 "이 프로토콜은 방전을 안 한다" 이고 그 숫자는 최종값이다.
    const text = profileTsv([curve({ complete: false, incomplete_reason: 'no_discharge' })])
    expect(text.split('\n')).toHaveLength(2)
  })

  it('이유를 모르면 뺀다 — 모르는 것을 최종값처럼 내보내지 않는다', () => {
    expect(stillRunning({ complete: false, incomplete_reason: 'unknown' })).toBe(true)
    expect(stillRunning({ complete: false, incomplete_reason: '' })).toBe(true)
    expect(stillRunning({ complete: false, incomplete_reason: 'no_charge' })).toBe(false)
    expect(stillRunning({ complete: true })).toBe(false)
  })

  it('몇 개를 뺐는지 셀 수 있다 — 조용히 빼면 곡선 수가 다른 것을 못 본다', () => {
    expect(skippedForCopy([
      curve({}),
      curve({ complete: false, incomplete_reason: 'truncated' }),
      curve({ complete: false, incomplete_reason: 'no_discharge' }),
    ])).toBe(1)
  })
})
