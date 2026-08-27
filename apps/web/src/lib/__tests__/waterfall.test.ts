/** 비껴 쌓기 — 논문의 SOC 3D 그림.
 *
 *  이 파일이 못박는 것 둘:
 *   1. 깊이가 **전위**를 따라간다.  전위가 높은 스윕이 더 멀리 밀린다.
 *   2. 하나라도 전위를 모르면 **차례**로 민다.  아는 것만 밀면 모르는 것들이
 *      한 자리에 겹쳐 쌓이고, 그 겹침을 사람이 "같은 상태" 로 읽는다.
 */

import { describe, expect, it } from 'vitest'

import { depthGuide, stack } from '../waterfall'

const three = [
  { x: [0, 10], y: [0, 5] },
  { x: [0, 10], y: [0, 5] },
  { x: [0, 10], y: [0, 5] },
]

describe('stack', () => {
  it('전위가 높을수록 멀리 민다 — 가장 낮은 것은 제자리', () => {
    const out = stack(three, [3.5, 3.9, 4.3])
    expect(out.offsets[0]!.dx).toBe(0)
    expect(out.offsets[0]!.dy).toBe(0)
    expect(out.offsets[1]!.dx).toBeGreaterThan(0)
    expect(out.offsets[2]!.dx).toBeGreaterThan(out.offsets[1]!.dx)
    expect(out.offsets[2]!.dy).toBeGreaterThan(out.offsets[1]!.dy)
    expect(out.span).toEqual({ low: 3.5, high: 4.3 })
  })

  it('민 만큼 점이 옮겨진다 — 원래 배열은 그대로', () => {
    const out = stack(three, [3.5, 3.9, 4.3])
    expect(out.series[1]!.x[0]).toBeCloseTo(out.offsets[1]!.dx, 12)
    expect(three[1]!.x[0]).toBe(0)
  })

  it('전위 간격이 고르지 않으면 계단도 고르지 않다 — 그것이 정보다', () => {
    // 3.5 · 3.6 · 4.3 — 앞 둘은 붙어 있고 마지막이 멀다.
    const out = stack(three, [3.5, 3.6, 4.3])
    const first = out.offsets[1]!.dx - out.offsets[0]!.dx
    const second = out.offsets[2]!.dx - out.offsets[1]!.dx
    expect(second).toBeGreaterThan(first * 3)
  })

  it('하나라도 모르면 차례로 민다 — 아는 것만 밀면 나머지가 겹친다', () => {
    const out = stack(three, [3.5, null, 4.3])
    expect(out.span).toBeNull()
    const first = out.offsets[1]!.dx - out.offsets[0]!.dx
    const second = out.offsets[2]!.dx - out.offsets[1]!.dx
    expect(second).toBeCloseTo(first, 12)
    expect(first).toBeGreaterThan(0)
  })

  it('전위가 전부 같으면 쌓을 방향이 없다 — 차례로 민다', () => {
    const out = stack(three, [3.5, 3.5, 3.5])
    expect(out.span).toBeNull()
    expect(out.offsets[2]!.dx).toBeGreaterThan(0)
  })

  it('빈 목록은 빈 채로', () => {
    expect(stack([], []).series).toEqual([])
    expect(stack([], []).span).toBeNull()
  })
})

describe('depthGuide', () => {
  it('밀린 원점들을 잇는다 — 이 선이 깊이 축이다', () => {
    const out = stack(three, [3.5, 3.9, 4.3])
    const guide = depthGuide(out.offsets, { x: 0, y: 0 })
    expect(guide.x).toHaveLength(3)
    expect(guide.x[0]).toBe(0)
    expect(guide.x[2]).toBeCloseTo(out.offsets[2]!.dx, 12)
    expect(guide.y[2]).toBeCloseTo(out.offsets[2]!.dy, 12)
  })
})
