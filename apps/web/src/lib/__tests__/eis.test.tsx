/** 임피던스 화면 — 두 세계가 섞이지 않는가, 못 믿을 숫자가 숫자로 보이는가.
 *
 *  이 화면이 존재하는 이유가 신뢰구간이므로(ADR 0019 §7), 시험의 절반은
 *  "수렴했지만 못 믿는다" 를 화면이 말하는지 본다.
 */

import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
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

import { Eis } from '../../pages/Eis'
import { SpectrumDetail } from '../../pages/SpectrumDetail'
import type { Spectrum, SpectrumDetail as Detail, SpectrumFit } from '../types'

type Handler = (url: string, init?: RequestInit) => unknown

function installFetch(handler: Handler) {
  const spy = vi.fn(async (url: string, init?: RequestInit) => {
    const result = handler(url, init)
    if (result instanceof Error) {
      return { ok: false, status: 422, statusText: 'Error',
               json: async () => ({ detail: result.message }) }
    }
    return { ok: true, status: 200, statusText: 'OK', json: async () => result ?? {} }
  })
  vi.stubGlobal('fetch', spy)
  return spy
}

const path = (url: string) => url.split('?')[0] ?? url
const params = (url: string) => new URL(url, 'http://x').searchParams

function spectrum(overrides: Partial<Spectrum> = {}): Spectrum {
  return {
    id: 1,
    sample_id: null,
    sample_name: null,
    name: 'sym_01',
    kind: 'solid',
    cell_config: 'sym',
    original_name: 'sym_01.mpr',
    sha256: 'abc',
    size_bytes: 2048,
    source_format: 'mpr',
    uploaded_at: '2026-08-24T10:00:00',
    n_points: 89,
    frequency_start_hz: 7e6,
    frequency_end_hz: 1e-2,
    amplitude_mv: 5,
    device: 'VSP-300',
    technique: 'Potentio Electrochemical Impedance Spectroscopy',
    at_cycle: null,
    measured_at: null,
    thickness_um: null,
    area_cm2: null,
    last_circuit: '',
    parse_error: '',
    updated_at: '2026-08-24T10:00:00',
    fit_count: 0,
    best_chi_squared: null,
    best_circuit: '',
    ...overrides,
  }
}

function fit(overrides: Partial<SpectrumFit> = {}): SpectrumFit {
  return {
    id: 11,
    spectrum_id: 1,
    circuit: 'R0-p(R1,CPE1)-p(R2,CPE2)',
    kind: 'solid',
    kind_now: 'solid',
    converged: true,
    chi_squared: 0.00089,
    reason: '',
    parameters: [
      { name: 'R0', value: 7.99, unit: 'Ω', stderr: 0.31, determined: true },
      { name: 'R1', value: 32.0, unit: 'Ω', stderr: 1.25, determined: true },
      { name: 'CPE1_Q', value: 2.6e-5, unit: 'S·sⁿ', stderr: 6e-6, determined: true },
      { name: 'CPE1_n', value: 0.58, unit: '', stderr: 0.02, determined: true },
      { name: 'R2', value: 26.6, unit: 'Ω', stderr: 1.26, determined: true },
      { name: 'CPE2_Q', value: 9.8e-4, unit: 'S·sⁿ', stderr: 1.6e-4, determined: true },
      { name: 'CPE2_n', value: 0.67, unit: '', stderr: 0.04, determined: true },
    ],
    arcs: [
      { parameter: 'R0', label: '직렬 저항', note: '배선', value_ohm: 7.99, determined: true },
      { parameter: 'R1', label: '벌크 저항', note: 'grain 내부', value_ohm: 32.0, determined: true },
      { parameter: 'R2', label: '입계 저항', note: 'grain boundary', value_ohm: 26.6, determined: true },
    ],
    conductivity: { missing: ['두께'] },
    dropped_inductive: 7,
    dropped_out_of_range: 0,
    frequency_low_hz: 0.01,
    frequency_high_hz: 3.4e5,
    starts: 9,
    starts_converged: 9,
    created_at: '2026-08-24T10:05:00',
    ...overrides,
  }
}

function detail(overrides: Partial<Detail> = {}): Detail {
  return {
    ...spectrum(),
    settings: {},
    thickness_cm: null,
    area_cm2_effective: null,
    fits: [],
    ...overrides,
  }
}

const CIRCUITS = {
  kinds: [
    { kind: 'liquid', label: '액체 전해질',
      presets: [{ circuit: 'R0-p(R1,CPE1)-p(R2,CPE2)', label: '두 아크', note: '기본' }] },
    { kind: 'solid', label: '전고체',
      presets: [{ circuit: 'R0-p(R1,CPE1)-p(R2,CPE2)-CPE3', label: '벌크+입계', note: '블로킹' }] },
  ],
}

const POINTS = {
  id: 1,
  name: 'sym_01',
  kind: 'solid',
  at_cycle: null,
  frequency_hz: [1e5, 1e3, 1e1, 1e-1],
  z_re: [8.1, 20.0, 45.0, 66.0],
  z_im: [-1.2, -12.0, -9.0, -0.4],
  magnitude: [8.19, 23.3, 45.9, 66.0],
  phase_deg: [-8.4, -31.0, -11.3, -0.35],
}

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

function renderList() {
  return render(
    <MemoryRouter initialEntries={['/eis']}>
      <Routes>
        <Route path="/eis" element={<Eis />} />
      </Routes>
    </MemoryRouter>,
  )
}

function renderDetail() {
  return render(
    <MemoryRouter initialEntries={['/eis/1']}>
      <Routes>
        <Route path="/eis/:id" element={<SpectrumDetail />} />
      </Routes>
    </MemoryRouter>,
  )
}

describe('EIS 목록', () => {
  it('종류를 바꾸면 그 종류만 불러온다 — 두 세계를 한 표에 섞지 않는다', async () => {
    const asked: (string | null)[] = []
    installFetch((url) => {
      if (path(url) === '/api/eis/spectra') {
        asked.push(params(url).get('kind'))
        return [spectrum()]
      }
      return []
    })

    renderList()
    await waitFor(() => expect(asked).toContain('liquid'))

    await userEvent.click(screen.getByRole('tab', { name: '전고체' }))
    await waitFor(() => expect(asked).toContain('solid'))
  })

  it('두 종류의 안내가 서로 다르다 — 같은 반원이 다른 것을 뜻한다', async () => {
    installFetch((url) => (path(url) === '/api/eis/spectra' ? [] : []))
    renderList()

    expect(await screen.findByText(/SEI 아크/)).toBeInTheDocument()
    await userEvent.click(screen.getByRole('tab', { name: '전고체' }))
    expect(await screen.findByText(/벌크 아크/)).toBeInTheDocument()
  })

  it('올릴 때 셀을 정해 두면 그 셀로 붙는다', async () => {
    let sent: URLSearchParams | null = null
    installFetch((url, init) => {
      if (path(url) === '/api/eis/spectra/upload' && init?.method === 'POST') {
        sent = params(url)
        return spectrum({ sample_id: 3 })
      }
      if (path(url) === '/api/samples') return [{ id: 3, name: 'No_1_dry' }]
      if (path(url) === '/api/eis/spectra') return []
      return []
    })

    renderList()
    await userEvent.selectOptions(await screen.findByLabelText('셀에 붙이기'), '3')
    await userEvent.upload(
      screen.getByLabelText('스펙트럼 파일'),
      new File(['x'], 'a.mpr', { type: 'application/octet-stream' }))

    await waitFor(() => expect(sent).not.toBeNull())
    expect(sent!.get('sample_id')).toBe('3')
  })

  it('고른 것만 일괄로 맞춘다', async () => {
    let sent: unknown = null
    installFetch((url, init) => {
      if (path(url) === '/api/eis/fit-batch') {
        sent = JSON.parse(String(init?.body))
        return { fitted: [], failed: [], requested: 1, converged: 1 }
      }
      if (path(url) === '/api/eis/spectra') {
        return [spectrum({ id: 7, name: 'a' }), spectrum({ id: 8, name: 'b' })]
      }
      return []
    })

    renderList()
    await userEvent.click(await screen.findByLabelText('a 고르기'))
    await userEvent.click(screen.getByRole('button', { name: /고른 1개 맞추기/ }))

    await waitFor(() => expect(sent).toEqual([7]))
    expect(await screen.findByText(/1\/1개 수렴/)).toBeInTheDocument()
  })

  it('일괄 피팅의 실패를 세어서 말한다 — 성공만 세면 반쯤 실패한 배치가 작아 보인다', async () => {
    installFetch((url) => {
      if (path(url) === '/api/eis/fit-batch') {
        return {
          fitted: [], requested: 3, converged: 1,
          failed: [{ spectrum_id: 8, detail: '점이 4개뿐입니다' }],
        }
      }
      if (path(url) === '/api/eis/spectra') return [spectrum({ id: 7, name: 'a' })]
      return []
    })

    renderList()
    await userEvent.click(await screen.findByLabelText('a 고르기'))
    await userEvent.click(screen.getByRole('button', { name: /맞추기/ }))

    expect(await screen.findByText(/1개 실패/)).toBeInTheDocument()
    expect(screen.getByText(/점이 4개뿐입니다/)).toBeInTheDocument()
  })
})

describe('스펙트럼 상세', () => {
  function detailHandler(extra: Handler = () => undefined): Handler {
    return (url, init) => {
      const supplied = extra(url, init)
      if (supplied !== undefined) return supplied
      if (path(url) === '/api/eis/circuits') return CIRCUITS
      if (path(url) === '/api/samples') return [{ id: 3, name: 'No_1_dry' }]
      // DRT 패널도 같은 화면에 있다.  훑기 결과가 없으면 그 자리에서 "못
      // 풀었습니다" 가 뜨고, 나머지는 그대로 동작해야 한다.
      if (path(url) === '/api/eis/spectra/1/drt/sweep') {
        return { spectrum_id: 1, results: [], suggested_index: -1,
                 suggested_reason: '' }
      }
      if (path(url) === '/api/eis/spectra/1/points') return POINTS
      if (path(url) === '/api/eis/spectra/1') return detail()
      return []
    }
  }

  it('회로 프리셋을 누르면 입력란에 들어간다', async () => {
    installFetch(detailHandler())
    renderDetail()

    const input = await screen.findByLabelText('회로')
    await userEvent.click(screen.getByRole('button', { name: /벌크\+입계/ }))
    expect(input).toHaveValue('R0-p(R1,CPE1)-p(R2,CPE2)-CPE3')
  })

  it('맞추기는 고른 회로와 유도성 설정을 함께 보낸다', async () => {
    let sent: URLSearchParams | null = null
    installFetch(detailHandler((url, init) => {
      if (path(url) === '/api/eis/spectra/1/fit' && init?.method === 'POST') {
        sent = params(url)
        return fit()
      }
      return undefined
    }))

    renderDetail()
    const box = await screen.findByRole('checkbox')
    await userEvent.click(box)          // 유도성 빼기를 끈다
    await userEvent.click(screen.getByRole('button', { name: '맞추기' }))

    await waitFor(() => expect(sent).not.toBeNull())
    expect(sent!.get('drop_inductive')).toBe('false')
    expect(sent!.get('circuit')).toBe('R0-p(R1,CPE1)-p(R2,CPE2)-CPE3')
  })

  it('아크에 이 셀에서의 이름이 붙는다', async () => {
    installFetch(detailHandler((url) =>
      path(url) === '/api/eis/spectra/1' ? detail({ fits: [fit()] }) : undefined))

    renderDetail()
    const row = (await screen.findByText('R1')).closest('tr')!
    expect(within(row).getByText('벌크 저항')).toBeInTheDocument()
  })

  it('못 믿을 파라미터를 숫자만으로 두지 않는다', async () => {
    // 수렴한 피팅이 곧 측정은 아니다 — 이 화면이 있는 이유다.
    const undetermined = fit({
      parameters: [
        { name: 'R0', value: 7.99, unit: 'Ω', stderr: 0.31, determined: true },
        { name: 'CPE3_Q', value: 999.9, unit: 'S·sⁿ', stderr: 7.6e4, determined: false },
      ],
      reason: '물리적 한계에 붙은 파라미터: CPE3_Q',
    })
    installFetch(detailHandler((url) =>
      path(url) === '/api/eis/spectra/1' ? detail({ fits: [undetermined] }) : undefined))

    renderDetail()
    const row = (await screen.findByText('CPE3_Q')).closest('tr')!
    expect(within(row).getByText('미결정')).toBeInTheDocument()
    expect(screen.getByText(/물리적 한계에 붙은/)).toBeInTheDocument()
  })

  it('전고체인데 두께가 없으면 무엇이 없는지 말한다', async () => {
    installFetch(detailHandler((url) =>
      path(url) === '/api/eis/spectra/1' ? detail({ fits: [fit()] }) : undefined))

    renderDetail()
    expect(await screen.findByText(/두께.*필요합니다/)).toBeInTheDocument()
  })

  it('종류를 나중에 고쳤으면 그 사실을 말한다', async () => {
    // 이름은 지금 종류로 붙지만, 그 피팅은 다른 종류로 보고됐었다.
    installFetch(detailHandler((url) =>
      path(url) === '/api/eis/spectra/1'
        ? detail({ fits: [fit({ kind: 'liquid', kind_now: 'solid' })] })
        : undefined))

    renderDetail()
    expect(await screen.findByText(/액체 전해질 로 맞춘 것입니다/)).toBeInTheDocument()
  })

  it('뺀 점 수와 시작점 수를 보여 준다', async () => {
    installFetch(detailHandler((url) =>
      path(url) === '/api/eis/spectra/1' ? detail({ fits: [fit()] }) : undefined))

    renderDetail()
    expect(await screen.findByText('유도성 7점 뺌')).toBeInTheDocument()
    expect(screen.getByText('시작점 9/9')).toBeInTheDocument()
  })

  it('셀 구성을 고르면 저장한다 — 아크의 이름이 여기 걸려 있다', async () => {
    let sent: unknown = null
    installFetch(detailHandler((url, init) => {
      if (path(url) === '/api/eis/spectra/1' && init?.method === 'PATCH') {
        sent = JSON.parse(String(init.body))
        return spectrum({ cell_config: 'full' })
      }
      return undefined
    }))

    renderDetail()
    await userEvent.selectOptions(await screen.findByLabelText('셀 구성'), 'full')
    await waitFor(() => expect(sent).toEqual({ cell_config: 'full' }))
  })

  it('이름이 두께를 들고 있으면 옆에 회색으로 적는다 — 채워 넣지는 않는다', async () => {
    // 이름은 누군가 그렇게 부르기로 한 것이지 기록이 아니다.  오타에서 나온
    // 전도도는 측정된 것과 똑같이 생겼다.
    installFetch(detailHandler((url) =>
      path(url) === '/api/eis/spectra/1'
        ? detail({ name: '260719_No1_55_70um_sym_01', thickness_um: null })
        : undefined))

    renderDetail()
    expect(await screen.findByText('#70µm')).toBeInTheDocument()
    expect(screen.getByLabelText('두께')).toHaveValue(null)
  })

  it('이미 그 값이면 힌트를 띄우지 않는다 — 같은 말을 두 번 하지 않는다', async () => {
    installFetch(detailHandler((url) =>
      path(url) === '/api/eis/spectra/1'
        ? detail({ name: '260719_No1_55_70um_sym_01', thickness_um: 70,
                   cell_config: 'sym' })
        : undefined))

    renderDetail()
    await screen.findByLabelText('두께')
    expect(screen.queryByText('#70µm')).toBeNull()
    expect(screen.queryByText('#대칭셀')).toBeNull()
  })

  it('두께를 비우면 지운다', async () => {
    let sent: unknown = null
    installFetch(detailHandler((url, init) => {
      if (path(url) === '/api/eis/spectra/1' && init?.method === 'PATCH') {
        sent = JSON.parse(String(init.body))
        return spectrum()
      }
      if (path(url) === '/api/eis/spectra/1') return detail({ thickness_um: 70 })
      return undefined
    }))

    renderDetail()
    const input = await screen.findByLabelText('두께')
    await userEvent.clear(input)
    await userEvent.tab()
    await waitFor(() => expect(sent).toEqual({ clear: ['thickness_um'] }))
  })

  it('전고체 풀셀이면 전도도를 안 낸다고 미리 말한다', async () => {
    installFetch(detailHandler((url) =>
      path(url) === '/api/eis/spectra/1'
        ? detail({ kind: 'solid', cell_config: 'full' })
        : undefined))

    renderDetail()
    expect(await screen.findByText(/이온 블로킹 대칭셀에서만/)).toBeInTheDocument()
  })

  it('사이클 번호를 적으면 저장한다 — 초기와 200 사이클을 가르는 것이 그것이다', async () => {
    let sent: unknown = null
    installFetch(detailHandler((url, init) => {
      if (path(url) === '/api/eis/spectra/1' && init?.method === 'PATCH') {
        sent = JSON.parse(String(init.body))
        return spectrum({ at_cycle: 200 })
      }
      return undefined
    }))

    renderDetail()
    const input = await screen.findByLabelText('사이클')
    await userEvent.type(input, '200')
    await userEvent.tab()
    await waitFor(() => expect(sent).toEqual({ at_cycle: 200 }))
  })

  it('0 사이클은 "구동 전" 이지 빈 값이 아니다', async () => {
    installFetch(detailHandler((url) =>
      path(url) === '/api/eis/spectra/1' ? detail({ at_cycle: 0 }) : undefined))

    renderDetail()
    // 제목 줄에 "구동 전" 이 뜨고, 칸에는 0 이 들어 있다 — 빈 칸이 아니다.
    expect(await screen.findByLabelText('사이클')).toHaveValue(0)
    expect(screen.getAllByText(/구동 전/).length).toBeGreaterThan(0)
  })

  it('셀에 붙일 수 있다 — 안 그러면 셀 화면의 카드가 영영 빈다', async () => {
    let sent: unknown = null
    installFetch(detailHandler((url, init) => {
      if (path(url) === '/api/eis/spectra/1' && init?.method === 'PATCH') {
        sent = JSON.parse(String(init.body))
        return spectrum({ sample_id: 3, sample_name: 'No_1_dry' })
      }
      return undefined
    }))

    renderDetail()
    await userEvent.selectOptions(await screen.findByLabelText('셀'), '3')
    await waitFor(() => expect(sent).toEqual({ sample_id: 3 }))
  })

  it('셀에서 떼어낼 수도 있다', async () => {
    let sent: unknown = null
    installFetch(detailHandler((url, init) => {
      if (path(url) === '/api/eis/spectra/1' && init?.method === 'PATCH') {
        sent = JSON.parse(String(init.body))
        return spectrum()
      }
      if (path(url) === '/api/eis/spectra/1') {
        return detail({ sample_id: 3, sample_name: 'No_1_dry' })
      }
      return undefined
    }))

    renderDetail()
    await userEvent.selectOptions(await screen.findByLabelText('셀'), '')
    await waitFor(() => expect(sent).toEqual({ clear: ['sample_id'] }))
  })

  it('맞추지 못했으면 이유를 낸다', async () => {
    installFetch(detailHandler((url) =>
      path(url) === '/api/eis/spectra/1'
        ? detail({ fits: [fit({ converged: false, chi_squared: null, parameters: [],
                                arcs: [], reason: '어느 시작점에서도 수렴하지 않았습니다' })] })
        : undefined))

    renderDetail()
    expect(await screen.findByText(/어느 시작점에서도 수렴하지 않았습니다/)).toBeInTheDocument()
  })
})
