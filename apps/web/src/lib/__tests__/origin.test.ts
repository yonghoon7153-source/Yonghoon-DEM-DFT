/** Origin 붙여넣기 블록.
 *
 * 여기서 틀리면 그래프가 조용히 이상해진다 — 곡선 끝에서 다음 곡선 시작으로
 * 선이 날아가거나, 없는 값이 0 으로 찍히거나, 잘린 사이클의 부분값이 점 하나로
 * 남거나.
 */

import { describe, expect, it } from 'vitest'

import {
  bodeTsv,
  cycleAndEfficiencyTsv,
  onlyCycles,
  diffusionTsv,
  dischargeTsv,
  dqdvTsv,
  drtTsv,
  efficiencyTsv,
  fitParametersTsv,
  nyquistTsv,
  nyquistWideTsv,
  pocvTsv,
  profileTsv,
  profileWideTsv,
  compareCyclesTsv,
  compareCyclesWideTsv,
  dqdvWideTsv,
  pseudoOcvWideTsv,
  tsvColumns,
  skippedDiffusionPoints,
  skippedForCopy,
  stillRunning,
} from '../origin'
import type { Cycle, DqdvSeries, ProfileSeries, SpectrumPoints } from '../types'

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

// -- 임피던스와 GITT ---------------------------------------------------------
//
// 절차서의 마지막 단계가 "Copy to clipboard → 엑셀 → Origin" 이다.  화면에서
// 읽을 수는 있는데 밖으로 나갈 수 없으면 그 자리에서 절차가 끊긴다.

function spectrumPoints(overrides: Partial<SpectrumPoints> = {}): SpectrumPoints {
  return {
    id: 1, name: 's', kind: 'solid', at_cycle: null,
    frequency_hz: [1e4, 1e2],
    z_re: [8, 20],
    z_im: [-1.2, -12],
    magnitude: [8.09, 23.32],
    phase_deg: [-8.5, -31],
    ...overrides,
  }
}

describe('nyquistTsv', () => {
  it('세로축은 −Z″ 다 — Origin 에서 다시 뒤집을 필요가 없다', () => {
    // 절차서가 실제로 `-col(B)` 를 시킨다.  한 번 잊으면 아크가 아래로 뒤집힌
    // 그림이 나오고, 그것은 물리적으로 유도성 셀이다.
    expect(nyquistTsv([spectrumPoints()])).toBe('8\t1.2\n20\t12')
  })

  it('여러 스펙트럼은 `--` 한 줄로 갈라 쌓는다', () => {
    const text = nyquistTsv([
      spectrumPoints({ z_re: [1], z_im: [-2] }),
      spectrumPoints({ z_re: [3], z_im: [-4] }),
    ])
    expect(text).toBe('1\t2\n--\t--\n3\t4')
  })

  it('없으면 빈 문자열 — 조용히 성공한 척하지 않는다', () => {
    expect(nyquistTsv([])).toBe('')
  })

  it('화면이 Ω·cm² 로 그리고 있으면 두 열 다 Ω·cm² 로 나간다', () => {
    // 면적을 적어 축이 Ω·cm² 로 바뀌었는데 붙여 넣은 열이 Ω 이면, 두 수의
    // 비가 면적이라 워크시트 안에서는 그럴듯한 수로 앉는다 — 틀렸다는 것이
    // 드러나지 않는 종류의 오류다.
    expect(nyquistTsv([spectrumPoints()], (value) => value * 1.25))
      .toBe('10\t1.5\n25\t15')
  })
})

describe('bodeTsv', () => {
  it('세 열이다 — |Z| 와 위상은 축이 달라 쌓을 수 없다', () => {
    expect(bodeTsv([spectrumPoints()])).toBe('10000\t8.09\t-8.5\n100\t23.32\t-31')
  })

  it('면적으로 나누는 것은 |Z| 뿐이다 — 주파수는 Hz 고 위상은 무차원이다', () => {
    expect(bodeTsv([spectrumPoints()], (value) => value * 2))
      .toBe('10000\t16.18\t-8.5\n100\t46.64\t-31')
  })
})

describe('fitParametersTsv', () => {
  it('이름부터 나간다 — R1 없이 32.02 만 있는 열은 아무것도 아니다', () => {
    const text = fitParametersTsv([
      { name: 'R0', value: 7.99, unit: 'Ω', stderr: 0.31, determined: true },
      { name: 'CPE1_n', value: 0.58, unit: '', stderr: null, determined: false },
    ])
    // 미결정 행은 값도 나가지 않는다 — 엑셀에는 "못 믿음" 표시를 붙일 수
    // 없어서, 숫자로 내보내는 순간 확정값이 된다 (리뷰 #7).
    // 단위는 한 열로 함께 나간다: `R0  7.99` 만 붙여 넣으면 그것이 Ω 인지
    // Ω·cm² 인지 워크시트 안에서는 알 길이 없다.
    expect(text).toBe('R0\t7.99\tΩ\t0.31\nCPE1_n\t--\t\t--')
  })

  it('화면이 면적으로 나눈 값을 보고 있으면 그 값 그대로 나간다', () => {
    // 보는 수와 붙이는 수가 다르면 어느 쪽이 맞는지 확인하는 데 왕복이 든다.
    const text = fitParametersTsv(
      [{ name: 'R0', value: 8, unit: 'Ω', stderr: 0.4, determined: true }],
      {
        value: (parameter, raw) => (parameter.unit === 'Ω' ? raw / 2 : raw),
        unit: (parameter) => (parameter.unit === 'Ω' ? 'Ω·cm²' : parameter.unit),
      },
    )
    expect(text).toBe('R0\t4\tΩ·cm²\t0.2')
  })
})

describe('drtTsv', () => {
  it('τ 를 그대로 낸다 — 로그로 내보내면 워크시트에서 되돌릴 수 없다', () => {
    expect(drtTsv({ tau_s: [1e-4, 1e-2], gamma_ohm: [20, 5] }))
      .toBe('0.0001\t20\n0.01\t5')
  })
})

describe('pocvTsv', () => {
  it('충전과 방전을 `--` 로 가른다', () => {
    const text = pocvTsv({
      charge: [{ capacity_mah: 0, voltage_v: 3.0 }],
      discharge: [{ capacity_mah: 0, voltage_v: 3.4 }],
    })
    expect(text).toBe('0\t3\n--\t--\n0\t3.4')
  })

  it('한쪽만 있으면 구분선을 넣지 않는다', () => {
    expect(pocvTsv({ charge: [{ capacity_mah: 1, voltage_v: 3.1 }], discharge: [] }))
      .toBe('1\t3.1')
  })
})

describe('diffusionTsv', () => {
  it('숫자가 나온 점만 낸다', () => {
    // `--` 로 끼워 넣으면 Origin 에서는 선이 끊긴 자리로만 보이고, 왜 끊겼는지는
    // 화면에만 남는다 — 워크시트에서는 측정하지 않은 것과 구분되지 않는다.
    const text = diffusionTsv([
      { capacity_mah: 0, d_cm2_s: null, rest_s: 600, drift_mv: 0.5 },
      { capacity_mah: 0.5, d_cm2_s: 1.27e-6, rest_s: 600, drift_mv: 0.7 },
    ])
    expect(text).toBe('0.5\t0.00000127\t600\t0.7')
    expect(skippedDiffusionPoints([
      { d_cm2_s: null }, { d_cm2_s: 1e-6 },
    ])).toBe(1)
  })

  it('휴지·드리프트 증거가 D 와 같은 행으로 나간다 (ADR 0020)', () => {
    // 엑셀에 D 만 붙으면 이완이 덜 된 휴지의 D 가 확정값처럼 읽힌다.
    const text = diffusionTsv([
      { capacity_mah: 0.5, d_cm2_s: 1e-6, rest_s: 60, drift_mv: 20 },
    ])
    expect(text).toBe('0.5\t0.000001\t60\t20')
  })
})


describe('비교 화면은 곡선마다 제 열을 갖는다', () => {
  // 쌓기와 넓게 펴기는 배치가 다른 것이 아니라 **용도가 다르다**.  한 셀의
  // 여러 사이클은 쌓는 편이 낫고 (plot 명령 한 번), 여러 셀을 겹쳐 본
  // 화면은 펴야 한다 — 쌓으면 Origin 에서 한 색 한 범례가 되어 그 화면이
  // 하려던 구분이 붙여 넣는 순간 사라진다.
  it('셀 둘이면 네 열이 되고, 쌓을 때의 -- 구분 줄은 없다', () => {
    const text = profileWideTsv([
      series({ capacity: [0, 1], voltage: [2.5, 4.3] }),
      series({ run_id: 2, capacity: [0, 2], voltage: [2.6, 4.2] }),
    ])
    expect(text.split('\n')).toEqual([
      '0\t2.5\t0\t2.6',
      '1\t4.3\t2\t4.2',
    ])
    expect(text).not.toContain('--\t--')
  })

  it('서버가 준 순서를 그대로 둔다 — 셀 바깥, 사이클 안쪽', () => {
    // analysis.py 가 `for sample_id … for number …` 로 돌기 때문에 3·4 번을
    // 고르면 [셀1 3번][셀1 4번][셀2 3번][셀2 4번] 로 온다.  화면이 순서를
    // 다시 만지면 열과 범례가 어긋난다.
    const text = profileWideTsv([
      series({ run_id: 1, cycle: 3, capacity: [11], voltage: [1] }),
      series({ run_id: 1, cycle: 4, capacity: [12], voltage: [2] }),
      series({ run_id: 2, cycle: 3, capacity: [21], voltage: [3] }),
      series({ run_id: 2, cycle: 4, capacity: [22], voltage: [4] }),
    ])
    expect(text).toBe('11\t1\t12\t2\t21\t3\t22\t4')
  })

  it('길이가 다른 곡선은 짧은 쪽을 -- 로 채운다', () => {
    // 쌓을 때와 달리 여기서는 길이가 곧 열 높이라, 채우지 않으면 열이
    // 어긋나 다음 곡선의 값이 위로 딸려 올라간다.
    const text = profileWideTsv([
      series({ capacity: [0, 1, 2], voltage: [4.3, 3.7, 2.5] }),
      series({ run_id: 2, capacity: [0], voltage: [4.3] }),
    ])
    expect(text.split('\n')).toEqual([
      '0\t4.3\t0\t4.3',
      '1\t3.7\t--\t--',
      '2\t2.5\t--\t--',
    ])
  })

  it('점이 없는 곡선은 빈 열 두 개를 남기지 않는다', () => {
    const base: DqdvSeries = {
      cycle: 3, branch: 'discharge', basis: 'mAh/g', points: 0,
      voltage: [], dqdv: [], run_id: 1, label: '없음',
      voltage_step: 0.005, smoothing: 5, points_dropped: 0, reason: '',
    }
    const text = dqdvWideTsv([
      base,
      { ...base, cycle: 4, points: 1, voltage: [3.7], dqdv: [-1.5], label: '있음' },
    ])
    expect(text).toBe('3.7\t-1.5')
  })

  it('구동 중이라 잘린 곡선은 넓게 펼 때도 뺀다', () => {
    const text = profileWideTsv([
      series({ complete: false, incomplete_reason: 'truncated' }),
      series({ run_id: 2, capacity: [0], voltage: [4.3] }),
    ])
    expect(text).toBe('0\t4.3')
  })

  it('사이클 추세도 셀마다 두 열', () => {
    const points = [{ cycle: 1, value: 100 }, { cycle: 2, value: 99 }]
    const wide = compareCyclesWideTsv([{ points }, { points: [{ cycle: 1, value: 80 }] }])
    expect(wide.split('\n')).toEqual(['1\t100\t1\t80', '2\t99\t--\t--'])
    // 쌓는 쪽은 그대로 살아 있다 — 상세 화면들이 아직 쓴다.
    expect(compareCyclesTsv([{ points }])).toBe('1\t100\n2\t99')
  })

  it('나이퀴스트도 스펙트럼마다 두 열이고 −Z″ 로 뒤집는다', () => {
    const spectrum = (re: number[], im: number[]) => spectrumPoints({
      frequency_hz: re.map(() => 1), z_re: re, z_im: im,
      magnitude: re, phase_deg: re,
    })
    expect(nyquistWideTsv([spectrum([10], [-5]), spectrum([20], [-6])]))
      .toBe('10\t5\t20\t6')
    // 상세 화면의 쌓는 판은 그대로다.
    expect(nyquistTsv([spectrum([10], [-5])])).toBe('10\t5')
  })

  it('pseudo-OCV 는 머리글 없이 숫자만 낸다', () => {
    // 예전에는 "이름 용량" 머리글 줄을 함께 냈다.  붙여 넣으면 데이터 첫
    // 행으로 앉아 도로 잘라내야 하는 것이 된다.
    const text = pseudoOcvWideTsv([{ x: [0, 1], y: [4.2, 4.1] }])
    expect(text.split('\n')[0]).toBe('0\t4.2')
    expect(text).not.toContain('용량')
  })
})


describe('onlyCycles', () => {
  const rows = [{ cycle: 1 }, { cycle: 3 }, { cycle: 4 }, { cycle: 100 }]

  it('null 이면 전부 — 지금까지의 동작', () => {
    expect(onlyCycles(rows, null)).toEqual(rows)
  })

  it('고른 것만 남긴다', () => {
    expect(onlyCycles(rows, [3, 4])).toEqual([{ cycle: 3 }, { cycle: 4 }])
  })

  it('순서는 사이클 쪽을 따른다 — 누른 순서가 아니다', () => {
    // 4·3 순으로 눌러도 워크시트는 3·4 로 앉는다.  누른 순서를 따르면 같은
    // 두 사이클이 사람마다 다른 순서로 나간다.
    expect(onlyCycles(rows, [4, 3])).toEqual([{ cycle: 3 }, { cycle: 4 }])
  })

  it('없는 번호는 조용히 무시한다', () => {
    expect(onlyCycles(rows, [3, 999])).toEqual([{ cycle: 3 }])
  })

  it('아무것도 안 고르면 빈 배열 — 전부가 아니다', () => {
    // null(전부)과 []( 아무것도)를 같게 다루면, 고르개를 비운 사람이 200
    // 사이클을 통째로 붙여 넣게 된다.
    expect(onlyCycles(rows, [])).toEqual([])
  })
})
