/** 대칭셀 라이브러리 — 묶기와 스윕 전부 (ADR 0039).
 *
 *  처음에는 여기 한 줄이 늘 파일 하나였다.  그러면 **스윕 하나를 고칠 길이
 *  없다** — 온도를 한 칸만 고치거나, 잘못 잰 스윕 하나를 빼거나, 그 스윕만
 *  다른 셀에 붙이는 일이 실제로 있다.  이 시험이 편 줄의 단위를 잡아 둔다:
 *  줄에 스윕 하나가 적혀 있으면 지우는 것도 그 스윕 하나여야 한다.
 */

import { fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

vi.hoisted(() => {
  const media = (query: string) => ({
    matches: false, media: query, onchange: null,
    addListener() {}, removeListener() {},
    addEventListener() {}, removeEventListener() {}, dispatchEvent: () => false,
  })
  globalThis.matchMedia = globalThis.matchMedia ?? (media as never)
})

import { SymCells } from '../SymCells'
import type { Spectrum } from '../../lib/types'

function sweep(index: number, over: Partial<Spectrum> = {}): Spectrum {
  return {
    id: 100 + index,
    sample_id: null,
    sample_name: null,
    name: `B12_activationE #${index}`,
    kind: 'solid',
    cell_config: 'sym',
    original_name: 'B12_activationE.mpt',
    sha256: 'scan-sym',
    size_bytes: 2048,
    source_format: 'mpt',
    uploaded_at: '2026-09-16T13:57:00',
    uploaded_by: '안용훈',
    created_by: '안용훈',
    n_points: 59,
    frequency_low_hz: 10,
    frequency_high_hz: 7e6,
    at_cycle: null,
    purpose: '이온전도도 스윕',
    note: '',
    sweep_index: index,
    sweep_count: 3,
    temperature_c: [60, 40, 20][index - 1] ?? null,
    group_id: null,
    group_name: '',
    group_label: '',
    group_parent_name: '',
    group_id_effective: null,
    group_name_effective: '',
    group_parent_name_effective: '',
    last_circuit: '',
    parse_error: '',
    updated_at: '2026-09-16T13:57:00',
    fit_count: 1,
    best_circuit: 'R0-p(R1,CPE1)',
    best_chi_squared: 0.002,
    ...over,
  } as unknown as Spectrum
}

function installFetch(spectra: Spectrum[]) {
  const spy = vi.fn(async (url: string, init?: RequestInit) => {
    const path = String(url).split('?')[0] ?? ''
    const body = path.startsWith('/api/eis/spectra') ? spectra : []
    void init
    return { ok: true, status: 200, statusText: 'OK', json: async () => body }
  })
  vi.stubGlobal('fetch', spy)
  return spy
}

function calls(spy: ReturnType<typeof installFetch>) {
  return spy.mock.calls.map(([url, init]) => ({
    url: String(url).split('?')[0] ?? '',
    method: init?.method ?? 'GET',
  }))
}

const draw = (spectra: Spectrum[]) => {
  const spy = installFetch(spectra)
  render(<MemoryRouter><SymCells /></MemoryRouter>)
  return spy
}

const ALL = [sweep(1), sweep(2), sweep(3)]

describe('대칭셀 라이브러리', () => {
  beforeEach(() => window.localStorage.clear())
  afterEach(() => {
    vi.unstubAllGlobals()
    vi.restoreAllMocks()
  })

  it('기본은 묶기 — 파일 하나가 한 줄이고 온도는 범위로', async () => {
    draw(ALL)
    expect(await screen.findByText('B12_activationE')).toBeInTheDocument()
    expect(screen.getByText('60 ~ 20 °C')).toBeInTheDocument()
    // 스윕 셋이 한 줄로 접혔다.
    expect(screen.queryByText('B12_activationE #2')).toBeNull()
  })

  it('스윕 전부를 누르면 스윕이 한 줄씩 선다', async () => {
    draw(ALL)
    await screen.findByText('B12_activationE')
    fireEvent.click(screen.getByRole('button', { name: '스윕 전부' }))
    expect(await screen.findByText('B12_activationE #2')).toBeInTheDocument()
    // 그 줄의 온도는 **그 스윕 하나**의 것이다.
    const row = screen.getByText('B12_activationE #2').closest('tr') as HTMLElement
    expect(within(row).getByText('40 °C')).toBeInTheDocument()
    expect(within(row).getByText('2/3')).toBeInTheDocument()
  })

  //: 여기가 이 시험의 이유다.  줄에는 스윕 하나가 적혀 있는데 지우면 아홉이
  //  사라지면, 화면이 스스로 모순된다.
  it('편 줄의 지우기는 그 스윕 하나만 지운다', async () => {
    const spy = draw(ALL)
    await screen.findByText('B12_activationE')
    fireEvent.click(screen.getByRole('button', { name: '스윕 전부' }))
    const row = within(
      (await screen.findByText('B12_activationE #2')).closest('tr') as HTMLElement)

    fireEvent.click(row.getByRole('button', { name: /지우기$/ }))
    expect(row.getByText('스윕 2/3 만')).toBeInTheDocument()
    fireEvent.click(row.getByRole('button', { name: '지웁니다' }))

    await waitFor(() => expect(calls(spy)).toContainEqual(
      { url: '/api/eis/spectra/102', method: 'DELETE' }))
    expect(calls(spy).some((one) => one.url === '/api/eis/scans/scan-sym')).toBe(false)
  })

  it('접힌 줄의 지우기는 그 파일 전부다', async () => {
    const spy = draw(ALL)
    const row = within(
      (await screen.findByText('B12_activationE')).closest('tr') as HTMLElement)
    fireEvent.click(row.getByRole('button', { name: /지우기$/ }))
    expect(row.getByText('스윕 3개 전부')).toBeInTheDocument()
    fireEvent.click(row.getByRole('button', { name: '지웁니다' }))

    await waitFor(() => expect(calls(spy)).toContainEqual(
      { url: '/api/eis/scans/scan-sym', method: 'DELETE' }))
    expect(calls(spy).some((one) => one.url.startsWith('/api/eis/spectra/')
                                    && one.method === 'DELETE')).toBe(false)
  })

  it('스윕이 하나뿐인 파일은 이 화면에 안 선다 — 세울 표가 없다', async () => {
    draw([sweep(1, { sha256: 'single', sweep_count: 1, name: '단일' })])
    expect(await screen.findByText('대칭셀 스캔이 없습니다')).toBeInTheDocument()
  })
})
