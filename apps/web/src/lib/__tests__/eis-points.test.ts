/** 실수축 위의 점을 어떻게 다루는가.
 *
 *  판정은 부호 하나다.  "고주파 몇 점" 처럼 세는 규칙으로 바뀌면 아크가
 *  실제로 유도성인 셀(리튬 도금 같은)에서 실측을 지우게 된다 — 그래서
 *  여기서 부호 규칙을 못박는다.
 */

import { describe, expect, it } from 'vitest'

import { inductiveCount, isScan, nyquistXy, sweepAt } from '../eis'

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

/** 스캔의 한 스윕인가, 그리고 그 스윕은 어느 상태에서 잰 것인가.
 *
 *  라이브러리·비교·스캔 상세 세 화면이 같은 판정을 써야 한 화면에서 "스캔"
 *  인 것이 다른 화면에서 낱장 스무 개로 흩어지지 않는다.
 */
describe('SOC 스캔의 스윕', () => {
  it('스윕이 둘 이상이면 스캔이다 — 안 적힌 것은 낱장', () => {
    expect(isScan({ sweep_count: 11 })).toBe(true)
    expect(isScan({ sweep_count: 1 })).toBe(false)
    expect(isScan({ sweep_count: null })).toBe(false)
    expect(isScan({})).toBe(false)
  })

  it('용량이 있으면 용량, 없으면 전위', () => {
    expect(sweepAt({ capacity_mah: 1.234, potential_v: 3.85 })).toBe('1.23 mAh')
    expect(sweepAt({ capacity_mah: null, potential_v: 3.85 })).toBe('3.85 V')
  })

  it('만방전(0 mAh)은 "모름" 이 아니다', () => {
    expect(sweepAt({ capacity_mah: 0 })).toBe('0 mAh')
  })

  it('둘 다 없으면 빈 문자열 — 0 으로 적으면 만방전과 구분되지 않는다', () => {
    expect(sweepAt({ capacity_mah: null, potential_v: null })).toBe('')
    expect(sweepAt({})).toBe('')
  })
})
