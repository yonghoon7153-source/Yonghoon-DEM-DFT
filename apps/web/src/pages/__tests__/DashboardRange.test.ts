/** 겹쳐 보기의 세로 범위 — 튄 곡선 하나가 나머지를 납작하게 만들지 않도록. */

import { describe, expect, it } from 'vitest'

import { overlayRange, RETENTION_CEILING } from '../Dashboard'

describe('용량 유지율 겹쳐 보기', () => {
  it('다 200 % 아래면 손대지 않는다', () => {
    // 자를 것이 없는데 위를 200 으로 못 박으면 90~100 % 사이에서 갈리는 셀들이
    // 아래쪽 절반에 눌린다 — 정작 읽어야 할 차이가 거기 있다.
    expect(overlayRange([{ y: [100, 96, 91] }, { y: [100, 88] }])).toEqual({
      range: [null, null], clipped: false,
    })
  })

  it('하나라도 튀면 거기서 자른다', () => {
    // 실측: 한 셀이 15,000 % 로 찍혀 나머지 27개가 바닥의 선 하나가 됐다.
    expect(overlayRange([{ y: [100, 96] }, { y: [15000, 99] }])).toEqual({
      range: [null, RETENTION_CEILING], clipped: true,
    })
  })

  it('딱 200 % 는 자르지 않는다', () => {
    expect(overlayRange([{ y: [200] }]).clipped).toBe(false)
  })

  it('범례에서 끈 곡선은 안 센다', () => {
    // 사람이 이미 안 보겠다고 한 것이 범위를 정하면 안 된다.
    expect(overlayRange([{ y: [100] }, { y: [15000], hidden: true }])).toEqual({
      range: [null, null], clipped: false,
    })
  })

  it('빈 목록에서 죽지 않는다', () => {
    expect(overlayRange([])).toEqual({ range: [null, null], clipped: false })
  })

  it('NaN 은 세지 않는다', () => {
    expect(overlayRange([{ y: [Number.NaN, 100] }]).clipped).toBe(false)
  })
})
