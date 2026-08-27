/** 누른 자리를 붙잡아 두는가. */

import { afterEach, describe, expect, it, vi } from 'vitest'

import { keepInPlace } from '../anchor'

/** jsdom 에는 배치가 없으므로 위치를 우리가 정해 준다. */
function element(tops: number[]) {
  let call = 0
  return {
    getBoundingClientRect: () => ({ top: tops[Math.min(call++, tops.length - 1)] ?? 0 }),
  } as unknown as HTMLElement
}

/** rAF 를 손으로 돌린다 — 몇 번 돌릴지까지 시험이 정한다. */
function driveFrames(times: number) {
  const queue: FrameRequestCallback[] = []
  vi.stubGlobal('requestAnimationFrame', (fn: FrameRequestCallback) => {
    queue.push(fn)
    return queue.length
  })
  vi.stubGlobal('cancelAnimationFrame', () => {})
  return () => {
    for (let i = 0; i < times; i += 1) {
      const next = queue.shift()
      if (!next) return
      next(0)
    }
  }
}

afterEach(() => vi.unstubAllGlobals())

describe('keepInPlace', () => {
  it('위쪽이 줄어 요소가 올라가면 그만큼 되돌린다', () => {
    const scrollBy = vi.fn()
    vi.stubGlobal('scrollBy', scrollBy)
    const run = driveFrames(1)
    //            처음 잰 자리 ↓   다시 그린 뒤 ↓ (40px 위로 올라갔다)
    keepInPlace(element([300, 260]))
    run()
    expect(scrollBy).toHaveBeenCalledWith(0, -40)
  })

  it('안 움직였으면 스크롤을 건드리지 않는다 — 그 자체가 떨림으로 보인다', () => {
    const scrollBy = vi.fn()
    vi.stubGlobal('scrollBy', scrollBy)
    const run = driveFrames(3)
    keepInPlace(element([300, 300.2, 300]))
    run()
    expect(scrollBy).not.toHaveBeenCalled()
  })

  it('사람이 굴리기 시작하면 손을 뗀다 — 아니면 그 스크롤을 되돌려 버린다', () => {
    const scrollBy = vi.fn()
    vi.stubGlobal('scrollBy', scrollBy)
    const run = driveFrames(3)
    keepInPlace(element([300, 100, 100]))
    window.dispatchEvent(new Event('wheel'))
    run()
    expect(scrollBy).not.toHaveBeenCalled()
  })

  it('요소가 없으면 아무 일도 안 한다', () => {
    const scrollBy = vi.fn()
    vi.stubGlobal('scrollBy', scrollBy)
    expect(() => keepInPlace(null)).not.toThrow()
    expect(scrollBy).not.toHaveBeenCalled()
  })
})
