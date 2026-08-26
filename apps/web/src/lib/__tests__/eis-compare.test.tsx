/** EIS 비교 — 맞춤 곡선을 실측 위에 얹는 자리.
 *
 *  이 화면의 규칙 하나가 시험의 대부분이다: **안 보이는 것은 복사할 수 없고,
 *  없는 것은 이름을 적는다.**  맞춤은 스펙트럼마다 있을 수도 없을 수도 있어서,
 *  없는 것을 말없이 빼면 그림에 곡선 하나가 모자란 채로 남는다 — 그 그림은
 *  "이 셀은 잘 맞았다" 와 구분되지 않는다.
 */

import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, describe, expect, it, vi } from 'vitest'

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

import { EisCompare } from '../../pages/EisCompare'

const path = (url: string) => url.split('?')[0] ?? url

function spectrum(id: number, name: string, area: number | null, fits: number) {
  return {
    id,
    sample_id: null,
    sample_name: null,
    name,
    kind: 'solid',
    cell_config: 'sym',
    original_name: `${name}.mpr`,
    sha256: `sha${id}`,
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
    group_id: null,
    group_name: '',
    group_parent_name: '',
    group_id_effective: null,
    group_name_effective: '',
    group_parent_name_effective: '',
    area_cm2_effective: area,
    fit_count: fits,
    best_circuit: fits ? 'R0-p(R1,CPE1)' : null,
    best_chi_squared: fits ? 0.002 : null,
    series_resistance_ohm: fits ? 8.0 : null,
  }
}

function points(id: number) {
  return {
    id,
    name: `s${id}`,
    kind: 'solid',
    at_cycle: null,
    frequency_hz: [1e5, 1e3, 1e1, 1e-1],
    z_re: [8.1, 20.0, 45.0, 66.0],
    z_im: [-1.2, -12.0, -9.0, -0.4],
    magnitude: [8.19, 23.3, 45.9, 66.0],
    phase_deg: [-8.4, -31.0, -11.3, -0.35],
  }
}

const FIT = {
  id: 90,
  spectrum_id: 1,
  circuit: 'R0-p(R1,CPE1)',
  kind: 'solid',
  kind_now: 'solid',
  converged: true,
  chi_squared: 0.002,
  reason: '',
  parameters: [],
  arcs: [],
  conductivity: {},
  dropped_inductive: 0,
  dropped_out_of_range: 0,
  frequency_low_hz: 0.1,
  frequency_high_hz: 1e5,
  starts: 1,
  starts_converged: 1,
  created_at: '2026-08-24T11:00:00',
  fitted_frequency_hz: [1e5, 1e3, 1e1, 1e-1],
  fitted_z_re: [8.0, 20.2, 44.8, 66.2],
  fitted_z_im: [-1.1, -12.2, -9.1, -0.5],
}

/** 이 화면이 부르는 것 전부.  안 세운 길로 새면 시험이 그것을 말해야 한다. */
function installFetch(seen: string[] = []) {
  const spy = vi.fn(async (url: string) => {
    seen.push(url)
    const body = (() => {
      switch (path(url)) {
        case '/api/eis/spectra':
          return [spectrum(1, 'A_fit', 0.785, 2), spectrum(2, 'B_bare', 0.785, 0)]
        case '/api/samples': return []
        case '/api/groups': return []
        case '/api/eis/points': return [points(1), points(2)]
        // 서버는 **가장 잘 맞은** 것만, 그리고 있는 것만 돌려준다.
        case '/api/eis/fits': return [FIT]
        default: return {}
      }
    })()
    return { ok: true, status: 200, statusText: 'OK', json: async () => body }
  })
  vi.stubGlobal('fetch', spy)
  return spy
}

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

/** 모드 단추와 복사 단추는 이름이 같다 ('맞춤').  둘을 뭉뚱그리면 무엇이
 *  바뀐 건지 시험이 말해 주지 못하므로, 각자의 울타리 안에서 찾는다. */
const modeButton = (name: string) =>
  within(screen.getByRole('group', { name: '그림' })).getByRole('button', { name })

async function renderPicked() {
  render(<MemoryRouter><EisCompare /></MemoryRouter>)
  await userEvent.click(await screen.findByRole('button', { name: '모두 선택' }))
  return () => document.querySelector('.copy-bar') as HTMLElement
}

describe('EIS 비교 — 맞춤', () => {
  it('맞춤으로 바꾸기 전에는 곡선을 부르지 않는다', async () => {
    const seen: string[] = []
    installFetch(seen)
    await renderPicked()

    await waitFor(() => expect(seen.some((url) => path(url) === '/api/eis/points'))
      .toBe(true))
    expect(seen.some((url) => path(url) === '/api/eis/fits')).toBe(false)

    await userEvent.click(modeButton('맞춤'))
    await waitFor(() => expect(seen.some((url) => path(url) === '/api/eis/fits'))
      .toBe(true))
  })

  it('안 맞춘 것은 이름을 적는다 — 곡선만 조용히 빠지면 잘 맞은 것처럼 보인다',
     async () => {
    installFetch()
    await renderPicked()

    await userEvent.click(modeButton('맞춤'))
    // 표에도 같은 문구가 있다.  경고문은 이름을 이어 붙이는 쪽이다.
    const warning = await screen.findByText(/아직 피팅 데이터가 없습니다 —/)
    expect(warning.textContent).toContain('B_bare')
    expect(warning.textContent).not.toContain('A_fit')
  })

  it('Origin 클립보드는 보이는 그림만 켠다', async () => {
    installFetch()
    const bar = await renderPicked()

    await waitFor(() =>
      expect(within(bar()).getByRole('button', { name: /나이퀴스트/ }))
        .toBeEnabled())
    expect(within(bar()).getByRole('button', { name: /^맞춤/ })).toBeDisabled()

    await userEvent.click(modeButton('맞춤'))
    await waitFor(() =>
      expect(within(bar()).getByRole('button', { name: /^맞춤/ })).toBeEnabled())
    expect(within(bar()).getByRole('button', { name: /나이퀴스트/ })).toBeDisabled()
  })
})
