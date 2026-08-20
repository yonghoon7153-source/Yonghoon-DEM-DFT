import { describe, expect, it } from 'vitest'

import {
  basisAxis,
  basisUnit,
  massFromName,
  num,
  parseCycleSpec,
  pct,
  spread,
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
