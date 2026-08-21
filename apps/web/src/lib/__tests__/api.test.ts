import { afterEach, describe, expect, it, vi } from 'vitest'

import { ApiError, api, unauthorized } from '../api'

function mockFetch(response: Partial<Response> & { json?: () => Promise<unknown> }) {
  const fake = vi.fn().mockResolvedValue({
    ok: true,
    status: 200,
    statusText: 'OK',
    json: async () => ({}),
    ...response,
  })
  vi.stubGlobal('fetch', fake)
  return fake
}

afterEach(() => vi.unstubAllGlobals())

describe('query building', () => {
  it('drops null, undefined and empty values so the API sees no blanks', async () => {
    const fetchMock = mockFetch({ json: async () => [] })
    await api.listSamples({ group_id: null, cathode_type: '', process: 'dry', c_rate: 0.2 })
    // 두 번째 인자는 더 이상 undefined 가 아니다 — 모든 요청이 이름 헤더를
    // 달고 나간다.  여기서 보는 것은 URL 조립이므로 그것만 본다.
    expect(fetchMock.mock.calls[0]?.[0]).toBe('/api/samples?process=dry&c_rate=0.2')
  })

  it('omits the question mark when nothing is filtered', async () => {
    const fetchMock = mockFetch({ json: async () => [] })
    await api.listSamples()
    expect(fetchMock.mock.calls[0]?.[0]).toBe('/api/samples')
  })

  it('keeps a false boolean, which is a real filter value', async () => {
    const fetchMock = mockFetch({ json: async () => ({}) })
    await api.sampleCycles(1, { complete_only: false })
    expect(fetchMock.mock.calls[0]?.[0]).toContain('complete_only=false')
  })
})

describe('error handling', () => {
  it("surfaces the server's own explanation", async () => {
    mockFetch({
      ok: false,
      status: 422,
      statusText: 'Unprocessable Entity',
      json: async () => ({ detail: 'active mass not set' }),
    })
    await expect(api.getSample(1)).rejects.toThrow('active mass not set')
  })

  it('carries the status code for the caller to branch on', async () => {
    mockFetch({ ok: false, status: 404, statusText: 'Not Found', json: async () => ({}) })
    await expect(api.getSample(1)).rejects.toMatchObject({ status: 404 })
  })

  it('falls back to the status line when the body is not JSON', async () => {
    mockFetch({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
      json: async () => {
        throw new Error('not json')
      },
    })
    await expect(api.getSample(1)).rejects.toBeInstanceOf(ApiError)
  })

  it('handles a 204 with no body', async () => {
    mockFetch({ status: 204 })
    await expect(api.deleteSample(1)).resolves.toBeUndefined()
  })
})

describe('uploads', () => {
  it('sends the file as multipart and names the sample in the query', async () => {
    const fetchMock = mockFetch({ status: 201, json: async () => ({ id: 1 }) })
    const file = new File([new Uint8Array([0, 1])], 'cell_012.wrd')
    await api.uploadRun(file, 7)
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit]
    expect(url).toBe('/api/runs/upload?sample_id=7')
    expect(init.method).toBe('POST')
    expect(init.body).toBeInstanceOf(FormData)
  })
})

describe('export urls', () => {
  it('builds a download link the browser can follow directly', () => {
    expect(api.exportCyclesUrl(3, { basis: 'mAh/g' })).toBe(
      '/api/export/samples/3/cycles.csv?basis=mAh%2Fg',
    )
  })
})

describe('문이 닫혔을 때 (ADR 0014)', () => {
  it('401 이면 화면을 다시 읽는다 — 암호를 묻는 한 장은 서버가 그린다', async () => {
    // 화면마다 401 을 따로 다루면 어딘가 하나는 "불러오지 못했습니다" 로만
    // 끝나고, 사용자는 암호 창을 못 본 채 앱이 고장 났다고 읽는다.
    const handle = vi.fn()
    const real = unauthorized.handle
    unauthorized.handle = handle
    try {
      mockFetch({
        ok: false,
        status: 401,
        statusText: 'Unauthorized',
        json: async () => ({ detail: '암호가 필요합니다.' }),
      })

      await expect(api.listSamples()).rejects.toBeInstanceOf(ApiError)
      expect(handle).toHaveBeenCalledTimes(1)

      // 한 화면이 요청 여럿을 동시에 보낸다.  전부 다시 읽으면 새로고침이
      // 겹쳐서 암호 창이 뜨지도 않는다.
      await expect(api.listSamples()).rejects.toBeInstanceOf(ApiError)
      expect(handle).toHaveBeenCalledTimes(1)
    } finally {
      unauthorized.handle = real
    }
  })
})
