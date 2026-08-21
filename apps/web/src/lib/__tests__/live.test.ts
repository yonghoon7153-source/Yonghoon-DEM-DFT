/** 공유 서버의 변경 알림 — 브라우저 쪽.
 *
 * 이 파일이 지키는 것은 두 가지다. 남이 바꾼 것은 반드시 전달되어야 하고,
 * 내가 방금 바꾼 것은 전달되면 안 된다. 둘 다 틀려도 아무 오류가 나지 않는다 —
 * 화면이 조용히 낡거나, 저장할 때마다 방금 보낸 것을 도로 읽어 올 뿐이다.
 */

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { _reset, noteOwnWrite, REVISION_HEADER, subscribe } from '../live'

class FakeStream {
  static open: FakeStream[] = []
  readonly url: string
  closed = false
  onerror: (() => void) | null = null
  private handlers: Record<string, ((event: MessageEvent<string>) => void)[]> = {}

  constructor(url: string) {
    this.url = url
    FakeStream.open.push(this)
  }

  addEventListener(name: string, handler: (event: MessageEvent<string>) => void) {
    const bucket = (this.handlers[name] ??= [])
    bucket.push(handler)
  }

  close() {
    this.closed = true
  }

  /** 서버가 한 줄 보냈다. */
  send(revision: number) {
    for (const handler of this.handlers.revision ?? []) {
      handler({ data: String(revision) } as MessageEvent<string>)
    }
  }
}

function headers(revision?: number) {
  return {
    headers: {
      get: (name: string) =>
        name === REVISION_HEADER && revision !== undefined ? String(revision) : null,
    },
  }
}

beforeEach(() => {
  FakeStream.open = []
  vi.stubGlobal('EventSource', FakeStream)
})

afterEach(() => {
  _reset()
  vi.unstubAllGlobals()
})

describe('변경 알림', () => {
  it('연결은 탭에 하나다 — 화면마다 열면 브라우저가 연결 수 제한에 걸린다', () => {
    subscribe(() => {})
    subscribe(() => {})
    subscribe(() => {})
    expect(FakeStream.open).toHaveLength(1)
    expect(FakeStream.open[0]!.url).toBe('/api/events')
  })

  it('남이 바꾸면 모든 구독자가 듣는다', () => {
    const heard: number[] = []
    subscribe((r) => heard.push(r))
    subscribe((r) => heard.push(r * 100))

    FakeStream.open[0]!.send(5)

    expect(heard).toEqual([5, 500])
  })

  it('내가 방금 쓴 것은 나에게 다시 알리지 않는다', () => {
    // 쓴 화면은 응답으로 이미 새 값을 받았다.  여기서 또 알리면 저장할 때마다
    // 방금 보낸 것을 도로 읽어 온다.
    const heard: number[] = []
    subscribe((r) => heard.push(r))

    noteOwnWrite(headers(9))
    FakeStream.open[0]!.send(9)

    expect(heard).toEqual([])
  })

  it('내 쓰기 다음에 남이 쓴 것은 듣는다', () => {
    const heard: number[] = []
    subscribe((r) => heard.push(r))

    noteOwnWrite(headers(9))
    FakeStream.open[0]!.send(9)
    FakeStream.open[0]!.send(10)

    expect(heard).toEqual([10])
  })

  it('같은 번호를 두 번 받아도 한 번만 알린다', () => {
    const heard: number[] = []
    subscribe((r) => heard.push(r))

    FakeStream.open[0]!.send(4)
    FakeStream.open[0]!.send(4)
    FakeStream.open[0]!.send(3) // 재연결 뒤 뒤늦게 도착한 옛 값

    expect(heard).toEqual([4])
  })

  it('마지막 구독자가 떠나면 연결을 닫는다', () => {
    const stop = subscribe(() => {})
    const stopToo = subscribe(() => {})

    stop()
    expect(FakeStream.open[0]!.closed).toBe(false)
    stopToo()
    expect(FakeStream.open[0]!.closed).toBe(true)
  })

  it('연결이 끊기면 간격을 늘려 가며 다시 붙는다', () => {
    vi.useFakeTimers()
    try {
      subscribe(() => {})
      FakeStream.open[0]!.onerror?.()

      // 즉시 다시 붙지 않는다 — 서버가 죽었을 때 모든 탭이 두들기면 안 된다.
      expect(FakeStream.open).toHaveLength(1)
      vi.advanceTimersByTime(2000)
      expect(FakeStream.open).toHaveLength(2)

      FakeStream.open[1]!.onerror?.()
      vi.advanceTimersByTime(2000)
      expect(FakeStream.open, '두 번째 실패는 더 오래 기다린다').toHaveLength(2)
      vi.advanceTimersByTime(2000)
      expect(FakeStream.open).toHaveLength(3)
    } finally {
      vi.useRealTimers()
    }
  })

  it('헤더가 없는 응답에도 죽지 않는다', () => {
    // 쓰기가 지나가는 길목이라, 여기서 던지면 "알림을 못 껐다" 가 "저장이
    // 안 됐다" 로 보인다.
    expect(() => noteOwnWrite(headers())).not.toThrow()
    expect(() => noteOwnWrite({})).not.toThrow()
  })
})

describe('EventSource 를 못 쓰는 브라우저', () => {
  it('주기적으로 물어보는 쪽으로 넘어간다', async () => {
    vi.stubGlobal('EventSource', undefined)
    const fetchSpy = vi.fn(async () => ({
      ok: true,
      json: async () => ({ revision: 3 }),
    }))
    vi.stubGlobal('fetch', fetchSpy)

    const heard: number[] = []
    subscribe((r) => heard.push(r))
    await vi.waitFor(() => expect(heard).toEqual([3]))
    expect(fetchSpy).toHaveBeenCalledWith('/api/revision')
  })
})
