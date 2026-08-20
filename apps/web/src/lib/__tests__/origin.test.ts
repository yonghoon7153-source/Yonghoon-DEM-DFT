/** Origin 붙여넣기 블록.
 *
 * 여기서 틀리면 그래프가 조용히 이상해진다 — 곡선이 제 끝에서 0 으로 처박히거나,
 * 단위가 폰트에 따라 깨지거나, 잘린 사이클의 부분값이 점 하나로 찍힌다.
 */

import { describe, expect, it } from 'vitest'

import { cyclesTsv, plainUnit, profileTsv, tsvColumns } from '../origin'
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

describe('plainUnit', () => {
  it('위첨자를 쓰지 않는다 — 붙여 넣은 헤더에서 폰트를 타면 깨진다', () => {
    expect(plainUnit('mAh/cm2')).toBe('mAh/cm2')
    expect(plainUnit('mAh/g')).toBe('mAh/g')
    expect(plainUnit('mAh')).toBe('mAh')
    // 화면 쪽 basisUnit 은 mAh cm⁻² 를 쓴다.  그건 화면 전용이다.
    expect(plainUnit('mAh/cm2')).not.toContain('⁻')
  })
})

describe('tsvColumns', () => {
  it('길이가 다른 열은 -- 로 채운다 — 빈칸이나 0 이면 곡선이 원점으로 처박힌다', () => {
    const text = tsvColumns(['a', 'b'], ['V', 'V'], [['1', '2', '3'], ['9']])
    expect(text.split('\n')).toEqual(['a\tb', 'V\tV', '1\t9', '2\t--', '3\t--'])
  })

  it('탭으로 나눈다 — Origin 이 열로 읽는 구분자다', () => {
    expect(tsvColumns(['a'], [''], [['1']]).split('\n')[0]).toBe('a')
    expect(tsvColumns(['a', 'b'], ['', ''], [['1'], ['2']])).toContain('1\t2')
  })
})

describe('profileTsv', () => {
  it('곡선 하나마다 (용량, 전압) 열 한 쌍', () => {
    const text = profileTsv(
      [series({ cycle: 3, branch: 'charge' }), series({ cycle: 3, branch: 'discharge' })],
      'mAh/g',
    )
    const rows = text.split('\n')
    expect(rows[0]).toBe('3번 충전 용량\t3번 충전 전압\t3번 방전 용량\t3번 방전 전압')
    expect(rows[1]).toBe('mAh/g\tV\tmAh/g\tV')
    expect(rows[2]).toBe('0\t4.3\t0\t4.3')
  })

  it('사이클마다 길이가 다른 것이 정상이다 — 짧은 쪽을 -- 로 맞춘다', () => {
    const text = profileTsv(
      [series({ capacity: [0, 1, 2], voltage: [4.3, 3.7, 2.5] }),
       series({ cycle: 50, capacity: [0, 1], voltage: [4.3, 2.5] })],
      'mAh/g',
    )
    const rows = text.split('\n')
    expect(rows[rows.length - 1]).toBe('2\t2.5\t--\t--')
  })

  it('곡선의 자기 단위를 쓴다 — 한 셀만 mAh 로 떨어졌을 수 있다', () => {
    const text = profileTsv([series({ basis: 'mAh' })], 'mAh/g')
    expect(text.split('\n')[1]).toBe('mAh\tV')
  })

  it('그릴 것이 없으면 빈 문자열 — 헤더만 붙여 넣게 두지 않는다', () => {
    expect(profileTsv([], 'mAh')).toBe('')
  })
})

describe('cyclesTsv', () => {
  it('용량은 선택된 단위로, 효율은 %, 전압은 V', () => {
    const text = cyclesTsv([cycle()], 'mAh/g')
    const rows = text.split('\n')
    expect(rows[0]!.split('\t')).toEqual([
      '사이클', '방전용량', '충전용량', '쿨롱효율', '유지율',
      '에너지효율', '평균방전전압', '전압이력',
    ])
    expect(rows[1]!.split('\t')).toEqual(['', 'mAh/g', 'mAh/g', '%', '%', '%', 'V', 'V'])
    expect(rows[2]).toBe('1\t4.9\t5.1\t96.1\t100\t91\t3.7\t0.2')
  })

  it('잘린 사이클은 아예 빼고 준다', () => {
    // 구동 중인 셀의 마지막 사이클은 스텝 도중에 잘려 있다.  그 부분값이 점
    // 하나로 찍히면 그래프가 마지막에 꺾여 내려간다.
    const text = cyclesTsv([cycle({ cycle: 1 }), cycle({ cycle: 2, complete: false })], 'mAh')
    const rows = text.split('\n').slice(2)
    expect(rows).toHaveLength(1)
    expect(rows[0]!.startsWith('1\t')).toBe(true)
  })

  it('값이 없는 칸은 -- 다', () => {
    const text = cyclesTsv([cycle({ voltage_hysteresis: null, retention_pct: null })], 'mAh')
    const row = text.split('\n')[2]!.split('\t')
    expect(row[4]).toBe('--')
    expect(row[7]).toBe('--')
  })

  it('완료된 사이클이 없으면 빈 문자열', () => {
    expect(cyclesTsv([cycle({ complete: false })], 'mAh')).toBe('')
  })
})
