/** DRT 가로축 — `ln τ` 와 `log₁₀ τ` 는 같은 그림을 2.303 배로 늘인 것이다. */

import { describe, expect, it } from 'vitest'

import {
  TAU_AXES, tauAxisLabel, tauAxisShort, tauAxisValue, tauFromAxis, validTauAxis,
} from '../tauaxis'

describe('tauaxis', () => {
  it('기본은 ln — DRT 의 정의가 자연로그 위의 밀도다', () => {
    // 저장된 것이 없거나 모르는 값이면 `ln` 이다.  `log10` 으로 새면 같은
    // 봉우리가 다른 자리에 있는 것처럼 보인다.
    expect(validTauAxis(undefined)).toBe('ln')
    expect(validTauAxis(null)).toBe('ln')
    expect(validTauAxis('ln')).toBe('ln')
    expect(validTauAxis('무엇이든')).toBe('ln')
    expect(validTauAxis('log10')).toBe('log10')
  })

  it('두 축은 2.302585 배 — 봉우리 자리와 높이의 뜻은 안 바뀐다', () => {
    // τ = 1 은 뺀다 — 두 축 모두 0 이라 비율이 NaN 이다 (그 점은 같다는 것이
    // 이미 아래 `tauFromAxis` 왕복으로 걸린다).
    for (const tau of [1e-6, 1e-3, 12.5, 300]) {
      expect(tauAxisValue('ln', tau) / tauAxisValue('log10', tau))
        .toBeCloseTo(Math.LN10, 9)
    }
    expect(tauAxisValue('ln', 1)).toBe(0)
    expect(tauAxisValue('log10', 1)).toBe(0)
  })

  it('축의 값에서 τ 를 되돌린다 — 눈금 설명이 그것으로 대역을 말한다', () => {
    for (const axis of TAU_AXES) {
      for (const tau of [1e-6, 1e-3, 1, 12.5, 300]) {
        expect(tauFromAxis(axis, tauAxisValue(axis, tau))).toBeCloseTo(tau, 9)
      }
    }
  })

  it('축 이름에 밑이 들어 있다 — 그림만 잘라 붙여도 어느 축인지 알아야 한다', () => {
    expect(tauAxisLabel('ln')).toContain('ln')
    expect(tauAxisLabel('log10')).toContain('log₁₀')
    expect(tauAxisShort('ln')).toBe('ln τ')
    expect(tauAxisShort('log10')).toBe('log₁₀ τ')
  })
})
