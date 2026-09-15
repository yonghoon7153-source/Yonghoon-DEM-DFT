import { describe, expect, it } from 'vitest'

import { stackOffsets } from '../stack'

/** 올릴 **양**은 이제 사람이 적는다 (`components/StackGap.tsx`).  여기 남은
 *  것은 "몇 번째 칸에 앉는가" 뿐이다 — 데이터가 아니라 순서의 문제라, 꺼 둔
 *  곡선을 어떻게 다루느냐가 전부다. */
describe('이격 — 몇 번째 칸에 앉는가', () => {
  it('켜 둔 것끼리 한 칸씩 올라간다', () => {
    const lifts = stackOffsets([{ y: [0, 1] }, { y: [0, 1] }, { y: [0, 1] }], 5)
    expect(lifts).toEqual([0, 5, 10])
  })

  //: 꺼 둔 것이 제 칸을 지키면 그림 가운데에 빈 띠가 남고, 그 띠는 "여기
  //  측정이 없다" 로 읽힌다.  접힌다.
  it('꺼 둔 곡선은 자리를 안 차지하고, 뒤엣것이 당겨 앉는다', () => {
    const lifts = stackOffsets([
      { y: [0, 10] },
      { y: [0, 1000], hidden: true },
      { y: [0, 10] },
    ], 5)
    expect(lifts[0]).toBe(0)
    expect(Number.isNaN(lifts[1]!)).toBe(true)
    expect(lifts[2]).toBe(5)
  })

  it('간격이 0 이면 전부 제자리 — 겹쳐 그린 것과 같다', () => {
    expect(stackOffsets([{ y: [0, 1] }, { y: [0, 1] }], 0)).toEqual([0, 0])
  })

  it('빈 목록은 빈 결과', () => {
    expect(stackOffsets([], 5)).toEqual([])
  })
})
