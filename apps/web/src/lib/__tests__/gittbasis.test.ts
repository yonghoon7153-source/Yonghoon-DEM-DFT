import { describe, expect, it } from 'vitest'

import { gittDivisor, splitByBasis } from '../gittbasis'
import type { GittRun } from '../types'

function run(over: Partial<GittRun> = {}): GittRun {
  return { id: 1, name: '기록', active_mass_g_effective: null,
           area_cm2_effective: null, ...over } as GittRun
}

describe('GITT 용량 축', () => {
  it('mAh 는 언제나 쓸 수 있다', () => {
    expect(gittDivisor(run(), 'mAh')).toBe(1)
  })

  it('나눌 수가 없으면 1 로 나누지 않는다', () => {
    // 1 로 나누면 mAh 를 mAh/cm² 라고 부르기만 한 숫자가 되고, 그것은 측정한
    // 면적용량과 화면에서 구별되지 않는다 (§0.4).
    expect(gittDivisor(run(), 'mAh/cm2')).toBeNull()
    expect(gittDivisor(run(), 'mAh/g')).toBeNull()
  })

  it('0 은 값이 아니다', () => {
    expect(gittDivisor(run({ area_cm2_effective: 0 }), 'mAh/cm2')).toBeNull()
  })

  it('못 쓰는 기록만 가른다', () => {
    // 섞으면 두 곡선의 길이 차이가 용량 차이인지 단위 차이인지 볼 수 없다.
    const withArea = run({ id: 1, area_cm2_effective: 1.33 })
    const without = run({ id: 2 })
    const split = splitByBasis([withArea, without], 'mAh/cm2')
    expect(split.kept.map((r) => r.id)).toEqual([1])
    expect(split.dropped.map((r) => r.id)).toEqual([2])
  })

  it('mAh 로 보면 아무도 안 빠진다', () => {
    expect(splitByBasis([run({ id: 1 }), run({ id: 2 })], 'mAh').dropped).toEqual([])
  })
})
