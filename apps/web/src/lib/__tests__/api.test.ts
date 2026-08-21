import { afterEach, describe, expect, it, vi } from 'vitest'

import { ApiError, api } from '../api'

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
