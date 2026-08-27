import { describe, expect, it } from 'vitest'

import { STACK_GAP, stackOffsets, stackStep } from '../stack'

describe('이격 — 곡선을 위로 비껴 쌓기', () => {
  it('올릴 양은 가운데 곡선의 높이에서 나온다 (최댓값이 아니라)', () => {
    // 높이 1, 1, 1, 그리고 유난히 큰 100 하나.  실제 스캔이 이 모양이다 —
    // 마지막 SOC 의 확산 꼬리가 나머지보다 자릿수로 크다.
    const series = [
      { y: [0, 1] }, { y: [0, 1] }, { y: [0, 1] }, { y: [0, 100] },
    ]
    // 중앙값 1 × 간격.  100 을 썼으면 앞의 세 곡선이 서로 60 씩 떨어져
    // 각자 납작한 선이 됐을 것이다.
    expect(stackStep(series)).toBeCloseTo(STACK_GAP, 10)
  })

  it('꺼 둔 곡선은 높이 계산에도 자리 계산에도 안 든다', () => {
    const series = [
      { y: [0, 10] },
      { y: [0, 1000], hidden: true },
      { y: [0, 10] },
    ]
    // 꺼 둔 1000 이 들어갔으면 중앙값이 10 이 아니다.
    expect(stackStep(series)).toBeCloseTo(10 * STACK_GAP, 10)
    const lifts = stackOffsets(series, 5)
    expect(lifts[0]).toBe(0)
    expect(Number.isNaN(lifts[1]!)).toBe(true)
    // 꺼 둔 것이 제 칸을 지키면 그림 가운데에 빈 띠가 남고, 그 띠가
    // "여기 측정이 없다" 로 읽힌다.  접힌다.
    expect(lifts[2]).toBe(5)
  })

  it('평평하거나 그릴 것이 없으면 0 — 없는 간격을 지어내지 않는다', () => {
    expect(stackStep([])).toBe(0)
    expect(stackStep([{ y: [3, 3, 3] }])).toBe(0)
    expect(stackStep([{ y: [1, 2], hidden: true }])).toBe(0)
    // NaN·Infinity 만 든 곡선도 높이가 없다.
    expect(stackStep([{ y: [Number.NaN, Number.POSITIVE_INFINITY] }])).toBe(0)
  })

  it('짝수 개면 가운데 둘의 평균', () => {
    const series = [{ y: [0, 2] }, { y: [0, 4] }]
    expect(stackStep(series, 1)).toBeCloseTo(3, 10)
  })
})
