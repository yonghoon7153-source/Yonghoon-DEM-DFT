/** DRT 가로축 — `log₁₀ τ (s)` 와 `f (Hz)`.
 *
 *  둘은 `τ = 1/(2πf)` 로 이어져 있어 **같은 그림을 좌우로 뒤집은 것**이다.
 *  이 파일이 못박는 것 둘:
 *   1. 좌표 왕복이 정확하다.  깨지면 눈금 설명(`describeX`)이 조용히 다른
 *      시간대를 적는다.
 *   2. f 축의 **눈금 글자는 좌표가 아니라 주파수**다.  `2` 를 그대로 두면
 *      1 kHz 짜리 눈금이 2 Hz 로 읽힌다.
 */

import { describe, expect, it } from 'vitest'

import {
  DRT_AXES, decadeSplits, drtAxisLabel, drtAxisShort, drtAxisTick,
  drtAxisValue, rawFromTau, tauFromAxis, validDrtAxis,
} from '../tauaxis'

describe('좌표', () => {
  it('τ 축은 log₁₀ τ 다', () => {
    expect(drtAxisValue('tau', 1)).toBe(0)
    expect(drtAxisValue('tau', 1e-3)).toBeCloseTo(-3, 12)
  })

  it('f 축은 log₁₀ f 이고 τ 축과 부호가 뒤집힌다 — 같은 그림의 좌우 반전', () => {
    // τ = 159 µs ↔ f = 1 kHz.
    expect(drtAxisValue('f', 1 / (2 * Math.PI * 1000))).toBeCloseTo(3, 12)
    // 고주파는 τ 축에서 왼쪽(작은 값), f 축에서 오른쪽(큰 값)이다.
    const fast = 1e-6
    const slow = 1e0
    expect(drtAxisValue('tau', fast)).toBeLessThan(drtAxisValue('tau', slow))
    expect(drtAxisValue('f', fast)).toBeGreaterThan(drtAxisValue('f', slow))
  })

  it('되돌아온다 — 눈금 설명이 이 왕복 위에 선다', () => {
    for (const axis of DRT_AXES) {
      for (const tau of [1e-6, 1e-3, 1, 250]) {
        expect(tauFromAxis(axis, drtAxisValue(axis, tau))).toBeCloseTo(tau, 9)
      }
    }
  })

  it('클립보드로는 날 것이 나간다 — 로그는 워크시트에서 못 되돌린다', () => {
    expect(rawFromTau('tau', 1e-3)).toBe(1e-3)
    expect(rawFromTau('f', 1 / (2 * Math.PI * 1000))).toBeCloseTo(1000, 9)
  })
})

describe('눈금 글자', () => {
  it('τ 축은 좌표가 곧 눈금이다', () => {
    expect(drtAxisTick('tau', -3)).toBe('-3')
    expect(drtAxisTick('tau', 0)).toBe('0')
  })

  it('f 축의 자리 눈금은 10ⁿ 이다 — 좌표를 그대로 두면 1 kHz 가 3 Hz 로 읽힌다', () => {
    expect(drtAxisTick('f', 0)).toBe('1')
    expect(drtAxisTick('f', 1)).toBe('10')
    expect(drtAxisTick('f', 2)).toBe('10²')
    expect(drtAxisTick('f', 4)).toBe('10⁴')
    expect(drtAxisTick('f', -1)).toBe('10⁻¹')
  })

  it('자리 사이(확대)에는 실제 주파수를 적는다 — 10^0.5 는 아무도 못 읽는다', () => {
    expect(drtAxisTick('f', 0.5)).toBe('3.16')
  })
})

describe('눈금 자리', () => {
  it('넓게 보면 자리마다 하나씩 — 그래야 지수 표기가 성립한다', () => {
    expect(decadeSplits(-1.4, 6.2)).toEqual([-1, 0, 1, 2, 3, 4, 5, 6])
  })

  it('확대해서 두 자리도 안 남으면 쪼갠다 — 눈금 하나뿐인 축은 아무 말도 안 한다',
     () => {
    expect(decadeSplits(2.9, 3.4).length).toBeGreaterThanOrEqual(2)
    expect(decadeSplits(3.1, 3.4).length).toBeGreaterThanOrEqual(2)
  })
})

describe('이름', () => {
  it('축 이름에 무엇을 그리는지가 적혀 있다', () => {
    expect(drtAxisLabel('tau')).toContain('log₁₀ τ')
    expect(drtAxisLabel('f')).toBe('f (Hz)')
    expect(drtAxisShort('tau')).toBe('log₁₀ τ')
    expect(drtAxisShort('f')).toBe('f (Hz)')
  })

  it('저장해 둔 값이 이상하면 기본(τ)으로', () => {
    expect(validDrtAxis('f')).toBe('f')
    expect(validDrtAxis('ln')).toBe('tau')
    expect(validDrtAxis(undefined)).toBe('tau')
  })
})
