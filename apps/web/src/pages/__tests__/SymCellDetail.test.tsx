/** 대칭셀 화면 — 기계가 저항을 고르지 않는다 (ADR 0039).
 *
 *  실측에서 실수축 교점으로 읽으면 0.290 eV, 랩이 ZView 에서 읽으면 0.328 eV
 *  였고 두 읽기의 비도 일정하지 않았다 (2.01 → 3.03).  그래서 교점은 **보이되
 *  저절로 들어가지 않는다**.  이 시험이 그 자리를 잡아 둔다.
 */

import { fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

vi.hoisted(() => {
  const media = (query: string) => ({
    matches: false, media: query, onchange: null,
    addListener() {}, removeListener() {},
    addEventListener() {}, removeEventListener() {}, dispatchEvent: () => false,
  })
  globalThis.matchMedia = globalThis.matchMedia ?? (media as never)
})

import { SymCellDetail } from '../SymCellDetail'
import type { ConductivityRow, ScanConductivity } from '../../lib/types'

const SHA = 'abc123'

function row(index: number, over: Partial<ConductivityRow> = {}): ConductivityRow {
  return {
    spectrum_id: index, sweep_index: index, name: `B12 #${index}`,
    temperature_c: null, thickness_mm: 0.79, area_cm2: 0.8501,
    resistance_ohm: null, resistance_source: '', crossing_ohm: 4.817 + index,
    sigma_ms_cm: null, ...over,
  }
}

function conductivity(over: Partial<ScanConductivity> = {}): ScanConductivity {
  return {
    sha256: SHA, name: 'B12_activationE', sweeps: 3,
    rows: [row(1), row(2), row(3)],
    missing: ['온도', '저항'],
    activation: {
      activation_energy_ev: null, stderr_ev: null, basis: 'sigma',
      points_used: 0, reason: '온도와 이온전도도가 모두 적힌 스윕이 둘 이상이어야 합니다',
      fit: null, inverse_temperature: [], log_sigma: [],
    },
    ...over,
  }
}

function installFetch(data: ScanConductivity) {
  const spy = vi.fn(async (url: string, init?: RequestInit) => {
    const path = String(url).split('?')[0] ?? ''
    let body: unknown = {}
    if (path === `/api/eis/scans/${SHA}`) {
      body = { sha256: SHA, name: data.name, original_name: 'B12.mpt',
               kind: 'solid', cell_config: 'sym', purpose: '이온전도도 스윕',
               sample_id: null, sample_name: null, sweeps: data.sweeps,
               fitted: 0, parameters: [], area_cm2_effective: 0.8501, points: [] }
    } else if (path.endsWith('/conductivity')) {
      body = data
    } else {
      body = { sweeps: data.sweeps, filled: data.sweeps, cleared: 0 }
    }
    void init
    return { ok: true, status: 200, statusText: 'OK', json: async () => body }
  })
  vi.stubGlobal('fetch', spy)
  return spy
}

function sent(spy: ReturnType<typeof installFetch>) {
  return spy.mock.calls.map(([url, init]) => ({
    url: String(url).split('?')[0] ?? '',
    method: init?.method ?? 'GET',
    body: typeof init?.body === 'string' ? JSON.parse(init.body) : null,
  }))
}

function draw(data = conductivity()) {
  const spy = installFetch(data)
  render(
    <MemoryRouter initialEntries={[`/sym/${SHA}`]}>
      <Routes><Route path="/sym/:sha256" element={<SymCellDetail />} /></Routes>
    </MemoryRouter>,
  )
  return spy
}

describe('대칭셀 상세', () => {
  beforeEach(() => window.localStorage.clear())
  afterEach(() => {
    vi.unstubAllGlobals()
    vi.restoreAllMocks()
  })

  it('실수축 교점은 보이되 저항 칸에 저절로 들어가지 않는다', async () => {
    draw()
    await screen.findByText('B12_activationE')
    // 표에 제안이 적혀 있고
    expect(await screen.findByText(/교점 5\.82 Ω/)).toBeInTheDocument()
    // 저항 칸은 비어 있다.
    const box = screen.getByLabelText('전해질 저항 목록') as HTMLInputElement
    expect(box.value).toBe('')
  })

  it('제안을 누르면 그때 칸에 들어간다', async () => {
    draw()
    await screen.findByText('B12_activationE')
    fireEvent.click(screen.getByRole('button', { name: '실수축 교점으로 채우기' }))
    const box = screen.getByLabelText('전해질 저항 목록') as HTMLInputElement
    expect(box.value).toBe('5.817, 6.817, 7.817')
  })

  //: `(60, -20, 9)` 가 무엇으로 펼쳐졌는지 눈에 보이지 않으면, 아홉 개를
  //  적었다고 믿는 채로 여덟 개가 들어간다.
  it('등간격 축약을 펼쳐서 되읽어 준다', async () => {
    draw()
    await screen.findByText('B12_activationE')
    const box = screen.getByLabelText('온도 목록')
    fireEvent.change(box, { target: { value: '(60, 20, 3)' } })
    expect(await screen.findByText('60, 40, 20 °C')).toBeInTheDocument()
  })

  it('개수가 스윕과 다르면 누르기 전에 막고 두 수를 말한다', async () => {
    draw()
    await screen.findByText('B12_activationE')
    fireEvent.change(screen.getByLabelText('온도 목록'),
                     { target: { value: '60, 40' } })
    const warning = await screen.findByText(/스윕은 3개인데 2개를 적었습니다/)
    expect(warning).toBeInTheDocument()
    const card = warning.closest('.card') ?? document.body
    expect(within(card as HTMLElement).getByRole('button', { name: '적용' }))
      .toBeDisabled()
  })

  it('적용하면 스윕 차례대로 보낸다', async () => {
    const spy = draw()
    await screen.findByText('B12_activationE')
    fireEvent.change(screen.getByLabelText('온도 목록'),
                     { target: { value: '(60, 20, 3)' } })
    const warn = screen.queryByText(/스윕은/)
    expect(warn).toBeNull()
    const card = screen.getByLabelText('온도 목록').closest('.card') as HTMLElement
    fireEvent.click(within(card).getByRole('button', { name: '적용' }))
    await waitFor(() => expect(sent(spy)).toContainEqual({
      url: `/api/eis/scans/${SHA}/temperature`,
      method: 'PUT',
      body: { temperature_c: [60, 40, 20] },
    }))
  })

  it('아직 없는 것을 이름으로 말한다 — 지어내지 않는다', async () => {
    draw()
    expect(await screen.findByText(/온도 · 저항 이\(가\) 아직 없습니다/))
      .toBeInTheDocument()
  })

  it('두께는 mm 로 받고 µm 로 저장하는 것을 옆에 적는다', async () => {
    const spy = draw()
    await screen.findByText('B12_activationE')
    const box = screen.getByLabelText('두께 (mm)')
    fireEvent.change(box, { target: { value: '0.79' } })
    expect(await screen.findByText(/= 790 µm 로 저장/)).toBeInTheDocument()

    const card = box.closest('.card') as HTMLElement
    fireEvent.click(within(card).getByRole('button', { name: '적용' }))
    await waitFor(() => {
      const patch = sent(spy).find((call) => call.method === 'PATCH')
      expect(patch?.body?.thickness_um).toBe(790)
    })
  })

  it('활성화에너지가 나오면 기준과 함께 적는다', async () => {
    draw(conductivity({
      missing: [],
      rows: [row(1, { temperature_c: 60, resistance_ohm: 9.69, sigma_ms_cm: 9.59,
                      resistance_source: 'typed' }),
             row(2, { temperature_c: 40, resistance_ohm: 14.56, sigma_ms_cm: 6.38,
                      resistance_source: 'typed' }),
             row(3, { temperature_c: 20, resistance_ohm: 34.66, sigma_ms_cm: 2.68,
                      resistance_source: 'typed' })],
      activation: {
        activation_energy_ev: 0.3284, stderr_ev: 0.0103, basis: 'sigma',
        points_used: 3, reason: '',
        fit: { slope: -3.80724, intercept: 7.01784, slope_stderr: 0.11916,
               intercept_stderr: 0.4115, n_points: 3, dof: 1, rss: 0.0837,
               pearson_r: -0.99659, r_squared: 0.99319, adj_r_squared: 0.99222,
               slope_t: -31.95, slope_p: 7.6e-9, intercept_t: 17.05,
               intercept_p: 5.8e-7, f_value: 1020.9, f_p: 7.6e-9 },
        inverse_temperature: [3.0017, 3.1934, 3.4114],
        log_sigma: [-4.6473, -5.0544, -5.9213],
      },
    }))
    expect(await screen.findByText('0.328 eV')).toBeInTheDocument()
    expect(screen.getByText(/ln σ 대 1000\/T/)).toBeInTheDocument()
    // Origin 의 보고서가 그대로 — 그 표를 만들려고 Origin 을 다시 열지 않게.
    expect(screen.getByText('R-Square (COD)')).toBeInTheDocument()
    // 위 띠와 보고서 두 군데에 같은 수가 선다 — Origin 화면과 눈으로 대조할
    // 수 있어야 하므로 유효숫자로 줄이지 않는다 (0.9932 가 아니라 0.99319).
    expect(screen.getAllByText('0.99319')).toHaveLength(2)
    expect(screen.getByText('-3.80724 ± 0.11916')).toBeInTheDocument()
    // 저항이 어디서 왔는지는 **줄마다** 적힌다 — 한 열에 섞이면 나중에
    // 그 표를 보는 사람이 손으로 읽은 것과 맞춘 것을 가를 수 없다.
    expect(screen.getAllByText('적음')).toHaveLength(3)
  })
})
