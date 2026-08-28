/** EIS 라이브러리의 fitting 칸 — 접은 줄이 무엇을 말하는가.
 *
 *  접으면 스윕 스물이 한 줄이 된다.  그 줄에 **첫 스윕의** χ² 를 적으면
 *  하나만 맞춘 파일이 맞춘 파일로 보인다.  이 시험은 그 자리를 잡아 둔다:
 *  전부 맞췄을 때만 '완료' 이고, 일부면 몇 개인지 적는다.
 */

import { render, screen, waitFor, within } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

vi.hoisted(() => {
  const media = (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener() {},
    removeListener() {},
    addEventListener() {},
    removeEventListener() {},
    dispatchEvent: () => false,
  })
  globalThis.matchMedia = globalThis.matchMedia ?? (media as never)
})

import { EisLibrary } from '../EisLibrary'
import type { Spectrum } from '../../lib/types'

function sweep(index: number, fits: number, chi: number | null): Spectrum {
  return {
    id: index,
    sample_id: null,
    sample_name: null,
    name: 'HD_PE_200cycle_half_SOC',
    kind: 'liquid',
    cell_config: 'half',
    original_name: 'HD_PE_200cycle_half_SOC.mpr',
    sha256: 'scan-a',
    size_bytes: 2048,
    source_format: 'mpr',
    uploaded_at: '2026-08-24T10:00:00',
    uploaded_by: '안용훈',
    n_points: 4,
    frequency_low_hz: 0.1,
    frequency_high_hz: 1e5,
    at_cycle: null,
    purpose: '',
    note: '',
    sweep_index: index,
    sweep_count: 3,
    group_id: null,
    group_name: '',
    group_parent_name: '',
    group_id_effective: null,
    group_name_effective: '',
    group_parent_name_effective: '',
    last_circuit: '',
    parse_error: '',
    updated_at: '2026-08-24T10:00:00',
    fit_count: fits,
    best_circuit: fits ? 'R0-p(R1,CPE1)' : '',
    best_chi_squared: fits ? chi : null,
  } as unknown as Spectrum
}

function installFetch(spectra: Spectrum[]) {
  const spy = vi.fn(async (url: string) => {
    const path = String(url).split('?')[0] ?? ''
    const body = path.startsWith('/api/eis/spectra') ? spectra : []
    return { ok: true, status: 200, statusText: 'OK', json: async () => body }
  })
  vi.stubGlobal('fetch', spy)
  return spy
}

/** 그 파일 줄 하나 — 접혀 있으므로 표에 스캔 줄은 하나뿐이다.
 *
 *  `fitting` 은 여덟째 칸이다.  `—` 는 목적·사이클 칸에도 있으므로 글자로
 *  찾으면 엉뚱한 칸을 본다.
 */
async function scanRow() {
  const link = await screen.findByText(/SOC 스캔 · 스윕/)
  const row = link.closest('tr')
  expect(row).not.toBeNull()
  const cells = within(row!).getAllByRole('cell')
  return { row: within(row!), fitting: cells[7]! }
}

describe('EIS 라이브러리 — 접힌 스캔의 fitting 칸', () => {
  beforeEach(() => {
    window.localStorage.clear()
  })
  afterEach(() => {
    vi.unstubAllGlobals()
    vi.restoreAllMocks()
  })

  const draw = (spectra: Spectrum[]) => {
    installFetch(spectra)
    render(<MemoryRouter><EisLibrary /></MemoryRouter>)
  }

  it('스윕 전부가 맞춰졌으면 완료라고 적는다', async () => {
    draw([sweep(1, 1, 0.002), sweep(2, 1, 0.004), sweep(3, 1, 0.003)])
    const { fitting } = await scanRow()
    await waitFor(() => expect(fitting.textContent).toContain('fitting 완료'))
    // 가장 나쁜 χ² 를 함께 — 셋 중 0.004.
    expect(fitting.textContent).toContain('χ²≤0.004')
  })

  //: 여기가 이 시험의 이유다.  첫 스윕만 맞춰진 파일이 예전에는 맞춘 파일로
  //  보였다 (첫 줄의 χ² 를 그대로 적었으므로).
  it('첫 스윕만 맞춰진 파일을 맞춘 파일로 적지 않는다', async () => {
    draw([sweep(1, 1, 0.002), sweep(2, 0, null), sweep(3, 0, null)])
    const { fitting } = await scanRow()
    await waitFor(() => expect(fitting.textContent).toContain('fitting 1/3'))
    expect(fitting.textContent).not.toContain('fitting 완료')
  })

  it('맞춘 적이 없으면 —', async () => {
    draw([sweep(1, 0, null), sweep(2, 0, null), sweep(3, 0, null)])
    const { fitting } = await scanRow()
    await waitFor(() => expect(fitting.textContent).toBe('—'))
  })
})
