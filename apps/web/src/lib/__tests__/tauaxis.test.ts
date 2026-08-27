/** DRT 가로축 — `log₁₀ τ` 하나.
 *
 *  한때 `ln` 도 고를 수 있었다.  빼면서 남긴 것은 왕복이다: 축의 값에서 τ 를
 *  되돌리지 못하면 눈금 설명(`describeX`)이 조용히 다른 시간대를 적는다.
 */

import { describe, expect, it } from 'vitest'

import {
  TAU_AXIS_LABEL, TAU_AXIS_SHORT, tauAxisValue, tauFromAxis,
} from '../tauaxis'

describe('tauaxis', () => {
  it('τ 를 log₁₀ 로 옮긴다', () => {
    expect(tauAxisValue(1)).toBe(0)
    expect(tauAxisValue(1e-3)).toBeCloseTo(-3, 12)
    expect(tauAxisValue(100)).toBeCloseTo(2, 12)
  })

  it('되돌아온다 — 눈금 설명이 이 왕복 위에 선다', () => {
    for (const tau of [1e-6, 1e-3, 1, 250]) {
      expect(tauFromAxis(tauAxisValue(tau))).toBeCloseTo(tau, 9)
    }
  })

  it('이름에 밑이 적혀 있다 — 어느 로그인지가 그림에 없으면 폭을 못 읽는다', () => {
    expect(TAU_AXIS_LABEL).toContain('log₁₀')
    expect(TAU_AXIS_SHORT).toBe('log₁₀ τ')
    // `ln` 이 남아 있으면 화면 어딘가가 아직 옛 축을 말하고 있다는 뜻이다.
    expect(TAU_AXIS_LABEL).not.toContain('ln')
  })
})
