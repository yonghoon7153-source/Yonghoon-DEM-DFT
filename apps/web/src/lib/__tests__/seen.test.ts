import { beforeEach, describe, expect, it } from 'vitest'

import { countNewer, lastSeen, markSeen } from '../seen'

describe('알림 점', () => {
  beforeEach(() => window.localStorage.clear())

  it('한 번도 안 봤으면 전부 새 것이다', () => {
    expect(countNewer(['2026-08-26T10:00:00', '2026-08-26T11:00:00'], 0)).toBe(2)
  })

  it('본 뒤에 움직인 것만 센다', () => {
    const since = Date.parse('2026-08-26T10:30:00Z')
    expect(countNewer(['2026-08-26T10:00:00', '2026-08-26T11:00:00'], since)).toBe(1)
  })

  it('시계가 몇백 ms 어긋난 것으로 점을 켜지 않는다', () => {
    // 방금 내가 쓴 글이 곧바로 "안 읽음" 으로 돌아오면 그 점은 쓸모가 없다.
    const now = Date.parse('2026-08-26T10:00:00Z')
    expect(countNewer(['2026-08-26T10:00:00.400'], now)).toBe(0)
  })

  it('시각이 없는 항목은 세지 않는다', () => {
    expect(countNewer([null, undefined, ''], Date.now())).toBe(0)
  })

  it('본 때를 적어 두고 다시 읽는다', () => {
    markSeen('feedback', 1234)
    expect(lastSeen('feedback')).toBe(1234)
  })

  it('적어 둔 적 없으면 0 — 즉 전부 새 것', () => {
    expect(lastSeen('feedback')).toBe(0)
  })
})
