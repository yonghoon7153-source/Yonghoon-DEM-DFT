/** 대칭셀 대시보드 — 한 줄이 전해질 한 파일이고, 두 수가 그 줄에 있다. */

import { render, screen, within } from '@testing-library/react'
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

import { SymDashboard } from '../SymDashboard'
import type { SymDashboardRow } from '../../lib/types'

function row(over: Partial<SymDashboardRow> = {}): SymDashboardRow {
  return {
    sha256: 'abc', name: 'B12_activationE', original_name: 'B12.mpt',
    sample_id: null, sample_name: '', group_id: null, group_name: '',
    group_parent_name: '', owner: '안용훈', purpose: '이온전도도 스윕',
    cell_config: 'sym', sweeps: 9, fitted: 9,
    temperatures_written: 9, temperature_high_c: 60, temperature_low_c: -20,
    resistances_written: 9, thickness_mm: 0.79, area_cm2: 0.8501,
    sigma_top_ms_cm: 9.59, activation_energy_ev: 0.3284,
    activation_stderr_ev: 0.0103, r_squared: 0.99319, points_used: 9,
    reason: '', uploaded_at: '2026-09-16T13:57:00', ...over,
  }
}

function draw(rows: SymDashboardRow[], others = 0) {
  // 주소마다 다른 모양을 돌려준다.  그룹 목록에 대시보드 응답을 주면 화면이
  // 거기서 먼저 깨져서, 표가 왜 비었는지 알 수 없게 된다.
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const path = String(url).split('?')[0] ?? ''
    const body = path.includes('/sym/dashboard')
      ? { rows, other_scans: others } : []
    return { ok: true, status: 200, statusText: 'OK', json: async () => body }
  }))
  render(<MemoryRouter><SymDashboard /></MemoryRouter>)
}

describe('대칭셀 대시보드', () => {
  beforeEach(() => window.localStorage.clear())
  afterEach(() => {
    vi.unstubAllGlobals()
    vi.restoreAllMocks()
  })

  it('한 줄에 온도 범위·σ·Ea·R² 가 선다', async () => {
    draw([row()])
    const link = await screen.findByText('B12_activationE')
    const line = within(link.closest('tr') as HTMLElement)
    expect(line.getByText('60 ~ -20 °C')).toBeInTheDocument()
    expect(line.getByText('9.59')).toBeInTheDocument()
    // σ 가 어느 온도의 값인지 함께 — 안 적으면 파일마다 다른 온도의 값이
    // 한 열에 서고, 그 열은 견줄 수 없다.
    expect(line.getByText('60°C')).toBeInTheDocument()
    expect(line.getByText('0.328')).toBeInTheDocument()
    expect(line.getByText('0.99319')).toBeInTheDocument()
  })

  //: 아홉 중 셋만 적힌 파일에 범위만 적으면 다 적은 파일과 구분되지 않는다.
  it('온도가 덜 적혔으면 몇 개인지 함께 적는다', async () => {
    draw([row({ temperatures_written: 3, temperature_low_c: 40 })])
    expect(await screen.findByText('60 ~ 40 °C (3/9)')).toBeInTheDocument()
  })

  it('하나도 안 적혔으면 그렇게 말하고 Ea 는 비운다', async () => {
    draw([row({
      temperatures_written: 0, temperature_high_c: null, temperature_low_c: null,
      sigma_top_ms_cm: null, activation_energy_ev: null, r_squared: null,
      points_used: 0, reason: '온도와 이온전도도가 모두 적힌 스윕이 둘 이상이어야 합니다',
    })])
    const link = await screen.findByText('B12_activationE')
    const line = within(link.closest('tr') as HTMLElement)
    expect(line.getByText('아직 없음')).toBeInTheDocument()
    expect(line.getAllByText('—').length).toBeGreaterThanOrEqual(3)
  })

  it('대칭셀로 안 보이는 스캔이 있으면 그 수를 말한다', async () => {
    draw([row()], 2)
    expect(await screen.findByText(/대칭셀로 보이지 않는 스캔이 2개/))
      .toBeInTheDocument()
  })

  it('하나도 없으면 무엇을 하면 되는지 적는다', async () => {
    draw([])
    expect(await screen.findByText('대칭셀 측정이 없습니다')).toBeInTheDocument()
  })
})
