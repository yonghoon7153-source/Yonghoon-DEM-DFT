/** Ω 인가 Ω·cm² 인가.
 *
 *  이 파일이 못박는 것 하나: **이름과 수가 같은 판정에서 나온다.**  면적을
 *  모르는데 `Ω·cm²` 라고 적히는 화면이 이 모듈이 생긴 이유다 — 그 수는 실측
 *  ASR 과 똑같이 생겼고, 어느 쪽인지 알 방법이 없다 (§0.4).
 */

import { describe, expect, it } from 'vitest'

import { perArea } from '../areanorm'
import { areaFor, validZUnit, zUnitLabel } from '../zunit'

describe('areaFor', () => {
  it('Ω 를 고르면 면적이 있어도 안 나눈다', () => {
    expect(areaFor('ohm', 0.785)).toBeNull()
  })

  it('Ω·cm² 를 골랐고 면적이 있으면 그 면적', () => {
    expect(areaFor('ohmcm2', 0.785)).toBe(0.785)
  })

  it('면적을 모르면 null — 골랐어도 안 나눈다', () => {
    expect(areaFor('ohmcm2', null)).toBeNull()
    expect(areaFor('ohmcm2', undefined)).toBeNull()
    // 0 cm² 는 면적이 아니라 안 적힌 것이다.  나누면 전부 0 이 된다.
    expect(areaFor('ohmcm2', 0)).toBeNull()
  })

  it('perArea 와 짝이다 — null 이면 값이 그대로 간다', () => {
    expect(perArea(12, areaFor('ohmcm2', 2))).toBe(24)
    expect(perArea(12, areaFor('ohm', 2))).toBe(12)
    expect(perArea(12, areaFor('ohmcm2', null))).toBe(12)
  })
})

describe('zUnitLabel', () => {
  it('이름은 areaFor 의 결과로 정한다 — 안 나눈 수에 Ω·cm² 가 붙지 않게', () => {
    const area = areaFor('ohmcm2', null)
    expect(zUnitLabel(area ? 'ohmcm2' : 'ohm')).toBe('Ω')
    expect(zUnitLabel(areaFor('ohmcm2', 1) ? 'ohmcm2' : 'ohm')).toBe('Ω·cm²')
  })
})

describe('validZUnit', () => {
  it('저장해 둔 값이 이상하면 기본으로 — 화면마다 기본이 다르다', () => {
    expect(validZUnit('ohmcm2')).toBe('ohmcm2')
    expect(validZUnit('ohm', 'ohmcm2')).toBe('ohm')
    // 예전 열쇠에 남은 쓰레기, 손으로 고친 localStorage.
    expect(validZUnit('Ω')).toBe('ohm')
    expect(validZUnit(null, 'ohmcm2')).toBe('ohmcm2')
    expect(validZUnit(undefined)).toBe('ohm')
  })
})
