import { describe, expect, it } from 'vitest'

import {
  basisAxis, basisUnit, cellConfigFromName, massFromName, nameFamily, num,
  parseCycleSpec, pct, spread, thicknessFromName,
} from '../format'

describe('num', () => {
  it('keeps significant figures rather than decimal places', () => {
    expect(num(5.2515)).toBe('5.252')
    expect(num(207.68)).toBe('207.7')
    expect(num(1234.5)).toBe('1235')
  })

  it('renders small values as significant figures, not rounded to zero', () => {
    expect(num(0.00104)).toBe('0.00104')
    expect(num(0.0000521)).toBe('0.0000521')
  })

  it('shows a dash for missing values rather than NaN', () => {
    expect(num(null)).toBe('—')
    expect(num(undefined)).toBe('—')
    expect(num(Number.NaN)).toBe('—')
  })

  it('renders an exact zero as 0', () => {
    expect(num(0)).toBe('0')
  })
})

describe('pct', () => {
  it('fixes the decimals so a column of efficiencies lines up', () => {
    expect(pct(99.6)).toBe('99.60')
    expect(pct(93.213, 1)).toBe('93.2')
  })
  it('shows a dash for missing values', () => {
    expect(pct(null)).toBe('—')
  })
})

describe('parseCycleSpec', () => {
  const available = [1, 2, 3, 4, 5, 10, 11, 12]

  it('expands ranges and lists', () => {
    expect(parseCycleSpec('1,3,10-12', available)).toEqual([1, 3, 10, 11, 12])
  })

  it('only returns cycles that exist', () => {
    expect(parseCycleSpec('1,99', available)).toEqual([1])
  })

  it('treats all and an empty string as everything', () => {
    expect(parseCycleSpec('all', available)).toEqual(available)
    expect(parseCycleSpec('  ', available)).toEqual(available)
  })

  it('accepts a reversed range', () => {
    expect(parseCycleSpec('12-10', available)).toEqual([10, 11, 12])
  })

  it('returns nothing for a spec that matches nothing', () => {
    expect(parseCycleSpec('900', available)).toEqual([])
  })
})

describe('spread', () => {
  it('picks evenly across the run, keeping both ends', () => {
    const picks = spread([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4)
    expect(picks[0]).toBe(1)
    expect(picks.at(-1)).toBe(10)
    expect(picks).toHaveLength(4)
  })

  it('returns the input when it is already short enough', () => {
    expect(spread([1, 2], 5)).toEqual([1, 2])
  })
})

describe('basis labels', () => {
  it('uses proper superscripts so axes read like a paper', () => {
    expect(basisUnit('mAh/g')).toBe('mAh g⁻¹')
    expect(basisUnit('mAh/cm2')).toBe('mAh cm⁻²')
    expect(basisAxis('mAh/cm2')).toContain('cm⁻²')
  })

  it('falls back to mAh for an unknown basis', () => {
    expect(basisUnit('mAh/kg')).toBe('mAh')
  })
})

describe('massFromName', () => {
  it('이 랩의 파일 이름에서 전극 질량을 읽는다', () => {
    expect(massFromName('CAM_LPSCl_4.6V_1_17.5mg')).toBe(17.5)
    expect(massFromName('CAM_LPSCl_3.8V_post_formation_17.6mg')).toBe(17.6)
  })

  it('정수 질량과 붙임/띄움을 모두 읽는다', () => {
    expect(massFromName('cell_18mg')).toBe(18)
    expect(massFromName('cell_18 mg')).toBe(18)
    expect(massFromName('cell_18MG')).toBe(18)
  })

  it('질량이 여럿이면 마지막 것 — 전극 질량이 이름 끝에 온다', () => {
    expect(massFromName('sep_5mg_cathode_17.5mg')).toBe(17.5)
  })

  it('mg 가 다른 단위의 일부이면 읽지 않는다', () => {
    // 없는 값을 지어내느니 아무것도 안 적는 편이 낫다.
    expect(massFromName('cell_200mAh_4.6V')).toBeNull()
    expect(massFromName('cell_3.5mgml')).toBeNull()
    expect(massFromName('4.6V_post_formation')).toBeNull()
    expect(massFromName('')).toBeNull()
    expect(massFromName(null)).toBeNull()
  })

  it('0 mg 은 질량이 아니다', () => {
    expect(massFromName('blank_0mg')).toBeNull()
  })
})

describe('nameFamily', () => {
  it('반복 실험을 하나로 묶는다 — 개체를 가리키는 꼬리만 뗀다', () => {
    expect(nameFamily('4.6V_1_17.5mg')).toBe('4.6V')
    expect(nameFamily('4.6V_2_18.1mg')).toBe('4.6V')
  })

  it('조건을 가리키는 말은 남긴다', () => {
    expect(nameFamily('4.0V_post_formation_18.9mg')).toBe('4.0V_post_formation')
  })

  it('파일 순번도 꼬리다', () => {
    expect(nameFamily('No_1_dry_011')).toBe('No_1_dry')
  })

  it('가운데 숫자는 건드리지 않는다 — No_1_dry 와 No_2_wet 은 다른 셀이다', () => {
    expect(nameFamily('No_1_dry')).toBe('No_1_dry')
    expect(nameFamily('No_2_wet')).toBe('No_2_wet')
  })

  it('전압처럼 숫자가 붙은 토큰은 숫자가 아니다', () => {
    expect(nameFamily('3.6V')).toBe('3.6V')
    expect(nameFamily('1000cyc_60oC_012')).toBe('1000cyc_60oC')
  })

  it('다 떼면 원래 이름을 돌려준다 — 이름 없는 더미가 생기면 안 된다', () => {
    expect(nameFamily('12345')).toBe('12345')
    expect(nameFamily('3_2_1')).toBe('3')
  })

  it('빈 이름은 빈 문자열', () => {
    expect(nameFamily('')).toBe('')
    expect(nameFamily(null)).toBe('')
  })
})

describe('massFromName 의 단어 경계', () => {
  it('밑줄이 뒤따라도 읽는다 — 밑줄은 단어 문자다', () => {
    // `\b` 로 쓰면 여기서 조용히 못 읽고, 힌트가 그냥 안 뜬다.
    expect(massFromName('4.6V_1_17.5mg_repeat')).toBe(17.5)
  })

  it('다른 단위에 붙은 mg 는 읽지 않는다', () => {
    expect(massFromName('cell_5mgml')).toBeNull()
  })
})

describe('thicknessFromName', () => {
  it('이름에 적힌 두께를 읽는다', () => {
    expect(thicknessFromName('260719_No1_55_70um_sym_01')).toBe(70)
    expect(thicknessFromName('pellet_120 um')).toBe(120)
    expect(thicknessFromName('pellet_85µm')).toBe(85)
  })

  it('마지막 것이 이긴다 — 둘을 적었으면 재는 쪽이 뒤에 온다', () => {
    expect(thicknessFromName('coat_20um_pellet_70um')).toBe(70)
  })

  it('없으면 없다고 한다', () => {
    expect(thicknessFromName('No_1_dry_17.5mg')).toBeNull()
    expect(thicknessFromName(null)).toBeNull()
  })
})

describe('cellConfigFromName', () => {
  it('대칭셀·풀셀·하프셀을 알아본다', () => {
    expect(cellConfigFromName('260719_No1_55_70um_sym_01')).toBe('sym')
    expect(cellConfigFromName('LPSCl_symmetric_02')).toBe('sym')
    expect(cellConfigFromName('NCM_full_cell_03')).toBe('full')
    expect(cellConfigFromName('Li_half_04')).toBe('half')
  })

  it('단어 경계를 지킨다 — symmetry 는 대칭셀이 아니다', () => {
    // 이름을 헐겁게 읽으면 회색 힌트가 틀린 것을 권한다.  힌트는 오타를
    // 잡으려고 있는 것이므로, 힌트가 틀리면 있느니만 못하다.
    expect(cellConfigFromName('symmetry_study_01')).toBeNull()
    expect(cellConfigFromName('fullerene_test')).toBeNull()
  })

  it('아무 말도 없으면 null 이다', () => {
    expect(cellConfigFromName('No_1_dry')).toBeNull()
    expect(cellConfigFromName(undefined)).toBeNull()
  })
})


describe('이름 힌트의 앞 경계 (리뷰 #33)', () => {
  it('지원하지 않는 표기의 꼬리만 떼어 보여 주지 않는다', async () => {
    const { massFromName, thicknessFromName } = await import('../format')
    // 쉼표 소수점과 과학 표기 — 통째로 못 읽으면 null 이다.
    expect(massFromName('cell_17,5mg')).toBeNull()
    expect(massFromName('cell_1e-3mg')).toBeNull()
    expect(thicknessFromName('pellet_70,5um')).toBeNull()
    expect(thicknessFromName('pellet_1e2um')).toBeNull()
    // 정상 표기는 그대로 읽힌다.
    expect(massFromName('No_1_dry_17.5mg_13pi')).toBe(17.5)
    expect(thicknessFromName('260719_No1_55_70um_sym_01')).toBe(70)
  })
})
