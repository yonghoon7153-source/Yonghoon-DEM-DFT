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

/** DRT 하나 — 봉우리가 하나인 γ(τ).  높이를 스펙트럼마다 다르게 두지 않는
 *  이유는 이격 폭이 **가운데 곡선의 높이**에서 나오기 때문이다: 같으면 그 폭이
 *  뻔해서, 올린 값이 맞는지 손으로 셀 수 있다. */
const DRT = {
  tau_s: [1e-4, 1e-3, 1e-2, 1e-1],
  gamma_ohm: [1.0, 6.0, 3.0, 0.5],
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
        default:
          // DRT 는 스펙트럼마다 한 번씩 부른다 (`/api/eis/spectra/{id}/drt`).
          if (/^\/api\/eis\/spectra\/\d+\/drt$/.test(path(url))) return DRT
          return {}
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

/** 모드 단추와 복사 단추는 이름이 같다 ('fitting').  둘을 뭉뚱그리면 무엇이
 *  바뀐 건지 시험이 말해 주지 못하므로, 각자의 울타리 안에서 찾는다. */
const modeButton = (name: string) =>
  within(screen.getByRole('group', { name: '그림' })).getByRole('button', { name })

async function renderPicked() {
  render(<MemoryRouter><EisCompare /></MemoryRouter>)
  await userEvent.click(await screen.findByRole('button', { name: '모두 선택' }))
  return () => document.querySelector('.copy-bar') as HTMLElement
}

describe('EIS 비교 — fitting', () => {
  it('fitting 으로 바꾸기 전에는 곡선을 부르지 않는다', async () => {
    const seen: string[] = []
    installFetch(seen)
    await renderPicked()

    await waitFor(() => expect(seen.some((url) => path(url) === '/api/eis/points'))
      .toBe(true))
    expect(seen.some((url) => path(url) === '/api/eis/fits')).toBe(false)

    await userEvent.click(modeButton('fitting'))
    await waitFor(() => expect(seen.some((url) => path(url) === '/api/eis/fits'))
      .toBe(true))
  })

  it('안 맞춘 것은 이름을 적는다 — 곡선만 조용히 빠지면 잘 맞은 것처럼 보인다',
     async () => {
    installFetch()
    await renderPicked()

    await userEvent.click(modeButton('fitting'))
    // 표에도 같은 문구가 있다.  경고문은 이름을 이어 붙이는 쪽이다.
    const warning = await screen.findByText(/아직 fitting 데이터가 없습니다 —/)
    expect(warning.textContent).toContain('B_bare')
    expect(warning.textContent).not.toContain('A_fit')
  })

  it('Origin 클립보드는 보이는 그림만 켠다', async () => {
    installFetch()
    const bar = await renderPicked()

    await waitFor(() =>
      expect(within(bar()).getByRole('button', { name: /나이퀴스트/ }))
        .toBeEnabled())
    expect(within(bar()).getByRole('button', { name: /^fitting/ })).toBeDisabled()

    await userEvent.click(modeButton('fitting'))
    await waitFor(() =>
      expect(within(bar()).getByRole('button', { name: /^fitting/ })).toBeEnabled())
    expect(within(bar()).getByRole('button', { name: /나이퀴스트/ })).toBeDisabled()
  })
})

/** SOC 스캔 — 파일 하나가 스윕 여럿.
 *
 *  고르개에서 이것이 스무 줄로 깔리면 그 파일 하나로 화면이 가득 찬다.  한
 *  줄로 접고, 펴서 스윕을 골라 겹친다 — SOC 별 나이퀴스트는 스윕마다 다른
 *  곡선이라 그중 몇을 고르는 것이 이 화면의 쓰임이다.
 */
function sweep(id: number, index: number, capacity: number) {
  return {
    ...spectrum(id, 'SOC_scan', 0.785, 0),
    sha256: 'sha-scan',
    sweep_index: index,
    sweep_count: 3,
    capacity_mah: capacity,
    potential_v: null,
  }
}

function installScanFetch() {
  const spy = vi.fn(async (url: string) => {
    const body = (() => {
      switch (path(url)) {
        case '/api/eis/spectra':
          return [sweep(11, 1, 0), sweep(12, 2, 1.0), sweep(13, 3, 2.0),
                  spectrum(2, 'B_bare', 0.785, 0)]
        case '/api/samples': return []
        case '/api/groups': return []
        case '/api/eis/points': return [points(12)]
        default: return {}
      }
    })()
    return { ok: true, status: 200, statusText: 'OK', json: async () => body }
  })
  vi.stubGlobal('fetch', spy)
  return spy
}

describe('EIS 비교 — SOC 스캔', () => {
  it('스캔은 한 줄로 접히고, 펴서 스윕 하나만 겹친다', async () => {
    installScanFetch()
    render(<MemoryRouter><EisCompare /></MemoryRouter>)

    // 접힌 상태: 스캔 한 줄 + 낱장 한 줄.  스윕 셋이 그대로 깔리지 않는다.
    const open = await screen.findByRole('button', { name: '스윕 고르기' })
    expect(screen.getByText(/스윕 3개/)).toBeTruthy()
    expect(screen.queryByText('#2')).toBeNull()

    await userEvent.click(open)
    await userEvent.click(screen.getByText('#2'))

    // '고른 것' 표가 스윕 번호와 그 SOC 를 적는다 — 이름은 셋이 다 같아서
    // 번호가 없으면 어느 줄이 어느 곡선인지 짚을 수가 없다.
    const table = document.querySelector('table') as HTMLElement
    expect(table.textContent).toContain('SOC_scan')
    expect(table.textContent).toMatch(/#2 · 1\.00 mAh/)
    expect(table.textContent).not.toContain('#3')
  })
})

/** 이격 — 곡선을 세로로 떼어 놓고 보는 자리.
 *
 *  이 보기의 위험은 하나다: **세로 눈금이 값이 아니게 된다.**  그래서 시험이
 *  보는 것도 그 자리다 — 올린 양을 화면이 적는가, 클립보드가 본값을 함께
 *  내는가, 그리고 fitting 에서는 아예 안 켜지는가 (거기서는 한 스펙트럼이
 *  곡선 둘이라, 둘이 다른 만큼 올라가면 "안 맞는 맞춤" 으로 보인다).
 */
describe('EIS 비교 — 이격', () => {
  const viewButton = (name: string) =>
    within(screen.getByRole('group', { name: '보기' })).getByRole('button', { name })

  function stubClipboard() {
    const written: string[] = []
    vi.stubGlobal('navigator', {
      ...navigator,
      clipboard: { writeText: async (text: string) => { written.push(text) } },
    })
    Object.defineProperty(window, 'isSecureContext', { value: true, configurable: true })
    return written
  }

  it('나이퀴스트에서 이격을 켜면 올린 양을 적는다', async () => {
    installFetch()
    await renderPicked()

    await userEvent.click(viewButton('이격'))
    const note = await screen.findByText(/씩 올려/)
    expect(note.textContent).toContain('세로 눈금은 그 스펙트럼의 값이 아닙니다')
  })

  it('DRT 에서도 켜진다', async () => {
    installFetch()
    await renderPicked()

    await userEvent.click(modeButton('DRT'))
    await userEvent.click(viewButton('이격'))
    expect(await screen.findByText(/씩 올려/)).toBeTruthy()
  })

  //: 여기가 이 보기의 유일한 함정이다.  fitting 에서 스펙트럼 하나는 곡선
  //  둘(점 = 측정, 파선 = 맞춤)이고, 둘이 서로 다른 만큼 올라가면 화면에
  //  "맞춤이 측정에서 떨어진" 그림이 나온다.
  it('fitting 에서는 단추도 없고 이격도 안 걸린다', async () => {
    installFetch()
    await renderPicked()

    await userEvent.click(viewButton('이격'))
    expect(await screen.findByText(/씩 올려/)).toBeTruthy()

    await userEvent.click(modeButton('fitting'))
    await waitFor(() => expect(screen.queryByText(/씩 올려/)).toBeNull())
    expect(screen.queryByRole('group', { name: '보기' })).toBeNull()

    // 나이퀴스트로 돌아오면 보던 대로 — 고른 것은 남아 있다.
    await userEvent.click(modeButton('나이퀴스트'))
    expect(await screen.findByText(/씩 올려/)).toBeTruthy()
  })

  it('이격 클립보드는 본값과 올린 값을 나란히 낸다', async () => {
    const written = stubClipboard()
    installFetch()
    const bar = await renderPicked()

    // 겹쳐 그린 동안에는 이격 칸이 아예 없다 — 안 보이는 그림은 복사할 수 없다.
    await waitFor(() =>
      expect(within(bar()).getByRole('button', { name: /나이퀴스트 복사/ }))
        .toBeEnabled())
    expect(within(bar()).queryByRole('button', { name: /이격/ })).toBeNull()

    await userEvent.click(viewButton('이격'))
    await userEvent.click(
      within(bar()).getByRole('button', { name: '나이퀴스트 (이격) 복사' }))

    const [tsv] = written
    expect(tsv).toBeTruthy()
    const [head, , first] = tsv!.split('\n')
    // 곡선마다 세 열: Z′ · 본값 · 올린 값.
    expect(head!.split('\t')).toHaveLength(6)
    expect(head).toContain('−Z″ + 이격')
    const cells = first!.split('\t')
    // 첫 곡선은 안 올린다 (맨 아래).  둘째는 올린 값이 본값보다 크다.
    expect(Number(cells[2])).toBeCloseTo(Number(cells[1]), 9)
    expect(Number(cells[5])).toBeGreaterThan(Number(cells[4]))
  })
})
