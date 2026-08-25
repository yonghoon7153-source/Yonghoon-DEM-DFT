/** 실수축 위의 점을 어떻게 다루는가.
 *
 *  판정은 부호 하나다.  "고주파 몇 점" 처럼 세는 규칙으로 바뀌면 아크가
 *  실제로 유도성인 셀(리튬 도금 같은)에서 실측을 지우게 된다 — 그래서
 *  여기서 부호 규칙을 못박는다.
 */

import { describe, expect, it } from 'vitest'

import { inductiveCount, nyquistXy } from '../eis'

describe('유도성 점', () => {
  const zRe = [10, 8, 7, 9, 20]
  const zIm = [21.7, 7.4, -0.4, -2.1, -12]

  it('실수축 위의 점을 센다', () => {
    expect(inductiveCount(zIm)).toBe(2)
    expect(inductiveCount([-1, -2])).toBe(0)
  })

  it('안 빼면 −Z″ 로 뒤집기만 한다 — 점 수는 그대로', () => {
    const { x, y, dropped } = nyquistXy(zRe, zIm, false)
    expect(x).toEqual(zRe)
    expect(y).toEqual([-21.7, -7.4, 0.4, 2.1, 12])
    expect(dropped).toBe(0)
  })

  it('빼면 그 점들이 사라지고 몇 개인지 말한다', () => {
    const { x, y, dropped } = nyquistXy(zRe, zIm, true)
    expect(x).toEqual([7, 9, 20])
    expect(y).toEqual([0.4, 2.1, 12])
    expect(dropped).toBe(2)
  })

  it('0 은 유도성이 아니다 — 실수축 위가 아니라 실수축이다', () => {
    expect(inductiveCount([0])).toBe(0)
    expect(nyquistXy([5], [0], true).x).toEqual([5])
  })

  it('가운데에 있는 것도 부호만 보고 뺀다', () => {
    // 잡음으로 축을 넘는 점 하나가 곡선 가운데에 있을 수 있다.  "앞쪽 몇
    // 개" 로 자르면 그런 점이 남고, 남으면 아크 밑으로 선 하나가 꽂힌다.
    const { x, dropped } = nyquistXy([1, 2, 3], [-1, 0.5, -3], true)
    expect(x).toEqual([1, 3])
    expect(dropped).toBe(1)
  })

  it('눈금 바꾸기는 자른 뒤에 태운다 (면적 정규화)', () => {
    const { x, y } = nyquistXy([10, 20], [5, -10], true, (value) => value / 2)
    expect(x).toEqual([10])
    expect(y).toEqual([5])
  })
})
