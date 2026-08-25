/** GITT 화면 — 두 결과가 비어 있는 이유가 다르다는 것이 보여야 한다. */

import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { afterEach, describe, expect, it, vi } from 'vitest'

vi.hoisted(() => {
  const media = (query: string) => ({
    matches: false, media: query, onchange: null,
    addListener() {}, removeListener() {},
    addEventListener() {}, removeEventListener() {},
    dispatchEvent: () => false,
  })
  globalThis.matchMedia = globalThis.matchMedia ?? (media as never)
})

import { GittLibrary } from '../../pages/GittLibrary'
import { GittUpload } from '../../pages/GittUpload'
import { GittDetail } from '../../pages/GittDetail'
import type { Diffusion, GittRun, Pocv } from '../types'

type Handler = (url: string, init?: RequestInit) => unknown

function installFetch(handler: Handler) {
  const spy = vi.fn(async (url: string, init?: RequestInit) => ({
    ok: true, status: 200, statusText: 'OK', json: async () => handler(url, init) ?? {},
  }))
  vi.stubGlobal('fetch', spy)
  return spy
}

const path = (url: string) => url.split('?')[0] ?? url

function run(overrides: Partial<GittRun> = {}): GittRun {
  return {
    id: 1, name: 'gitt_01', original_name: 'gitt_01.wrd', sha256: 'abc',
    size_bytes: 2_000_000, uploaded_at: '2026-08-25T10:00:00',
    n_points: 400, n_pulses: 8, duration_h: 12.5, start_time: null,
    molar_volume_cm3: null, molar_mass_g: null, active_mass_g: null,
    area_cm2: null, min_rest_s: 0, parse_error: '', pulse_note: '',
    updated_at: '2026-08-25T10:00:00',
    missing_for_diffusion: ['몰부피 V_M', '몰질량 M_B', '활물질 질량', '계면 면적 S'],
    ...overrides,
  }
}

function pocv(overrides: Partial<Pocv> = {}): Pocv {
  return {
    gitt_id: 1,
    charge: [
      { capacity_mah: 0, voltage_v: 3.05, rest_s: 600, drift_mv: 0.04 },
      { capacity_mah: 0.5, voltage_v: 3.1, rest_s: 600, drift_mv: 0.04 },
    ],
    discharge: [],
    skipped_charge: 0, skipped_discharge: 0, skipped_reasons: [],
    ...overrides,
  }
}

function diffusion(overrides: Partial<Diffusion> = {}): Diffusion {
  return {
    gitt_id: 1,
    points: [
      { capacity_mah: 0, voltage_v: 3.05, d_cm2_s: null, delta_es_v: 0,
        delta_et_v: 0.02, pulse_s: 60, sqrt_t_r_squared: 1.0,
        reason: '직전 휴지가 없어 ΔE_s 를 잴 수 없습니다 (시리즈의 첫 펄스)' },
      { capacity_mah: 0.5, voltage_v: 3.1, d_cm2_s: 1.27e-6, delta_es_v: 0.05,
        delta_et_v: 0.02, pulse_s: 60, sqrt_t_r_squared: 1.0, reason: '' },
    ],
    missing: [], molar_volume_cm3: 20, molar_mass_g: 96, mass_g: 0.02,
    area_cm2: 1.33, usable: 1, total: 2,
    ...overrides,
  }
}

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

function renderDetail(handler: Handler) {
  installFetch(handler)
  return render(
    <MemoryRouter initialEntries={['/gitt/1']}>
      <Routes>
        <Route path="/gitt/:id" element={<GittDetail />} />
      </Routes>
    </MemoryRouter>,
  )
}

function detailHandler(extra: Handler = () => undefined): Handler {
  return (url, init) => {
    const supplied = extra(url, init)
    if (supplied !== undefined) return supplied
    if (path(url) === '/api/gitt/runs/1/pocv') return pocv()
    if (path(url) === '/api/gitt/runs/1/diffusion') return diffusion()
    if (path(url) === '/api/gitt/runs/1') return run()
    return []
  }
}

describe('GITT 업로드', () => {
  it('사이클링 파일을 올리면 관찰을 그대로 보여 준다 — 삼키지 않는다', async () => {
    installFetch((url, init) => {
      if (path(url) === '/api/gitt/runs/upload' && init?.method === 'POST') {
        return run({ name: 'cycling', n_pulses: 16,
                     pulse_note: '휴지(30 s)가 펄스(300 s)보다 길지 않습니다 — '
                                 + 'GITT 기록이 맞는지 확인해 주세요.' })
      }
      if (path(url) === '/api/gitt/runs') return []
      return []
    })
    render(<MemoryRouter><GittUpload /></MemoryRouter>)

    const input = await screen.findByLabelText('여기에 .wrd 파일을 끌어다 놓으세요')
    await userEvent.upload(
      input, new File(['x'], 'cycling.wrd', { type: 'application/octet-stream' }))

    expect(await screen.findByText(/GITT 기록이 맞는지/)).toBeInTheDocument()
  })

})

describe('GITT 라이브러리', () => {
  it('확산계수를 낼 수 있는지 표에서 보인다', async () => {
    installFetch((url) => (path(url) === '/api/gitt/runs'
      ? [run({ id: 1, name: 'a' }),
         run({ id: 2, name: 'b', missing_for_diffusion: [] })]
      : []))
    render(<MemoryRouter><GittLibrary /></MemoryRouter>)

    const first = (await screen.findByText('a')).closest('tr')!
    const second = screen.getByText('b').closest('tr')!
    expect(within(first).getByText('4개 부족')).toBeInTheDocument()
    expect(within(second).getByText('가능')).toBeInTheDocument()
  })

  it('목록에서 바로 셀에 붙인다 — 파일부터 올리는 순서가 흔하다', async () => {
    const sent: { url: string; body: string }[] = []
    installFetch((url, init) => {
      if (path(url) === '/api/gitt/runs') {
        return [run({ id: 1, name: 'a', sample_id: null, sample_name: null })]
      }
      if (path(url) === '/api/samples') {
        return [{ id: 7, name: 'CELL-7', resolved_cell: {} }]
      }
      if (path(url) === '/api/gitt/runs/1' && init?.method === 'PATCH') {
        sent.push({ url: path(url), body: String(init.body) })
        return run({ id: 1, name: 'a', sample_id: 7, sample_name: 'CELL-7' })
      }
      return []
    })
    render(<MemoryRouter><GittLibrary /></MemoryRouter>)

    const picker = await screen.findByLabelText('a 셀')
    await userEvent.selectOptions(picker, '7')
    await waitFor(() => expect(sent).toHaveLength(1))
    expect(JSON.parse(sent[0]!.body)).toEqual({ sample_id: 7 })
  })

  it('떼어낼 때는 clear 를 보낸다 — null 은 "안 보냄" 과 구별되지 않는다', async () => {
    const sent: string[] = []
    installFetch((url, init) => {
      if (path(url) === '/api/gitt/runs') {
        return [run({ id: 1, name: 'a', sample_id: 7, sample_name: 'CELL-7' })]
      }
      if (path(url) === '/api/samples') {
        return [{ id: 7, name: 'CELL-7', resolved_cell: {} }]
      }
      if (path(url) === '/api/gitt/runs/1' && init?.method === 'PATCH') {
        sent.push(String(init.body))
        return run({ id: 1, name: 'a' })
      }
      return []
    })
    render(<MemoryRouter><GittLibrary /></MemoryRouter>)

    await userEvent.selectOptions(await screen.findByLabelText('a 셀'), '')
    await waitFor(() => expect(sent).toHaveLength(1))
    expect(JSON.parse(sent[0]!)).toEqual({ clear: ['sample_id'] })
  })
})

describe('GITT 상세', () => {
  it('pOCV 는 재료 상수 없이도 나온다', async () => {
    // 재료 상수가 하나도 없는 기록이다.  그래도 곡선과 점은 나와야 한다 —
    // 확산계수와 비어 있는 이유가 다른 것이 이 화면의 요점이다.
    renderDetail(detailHandler())
    expect(await screen.findByText('pOCV 점 2개')).toBeInTheDocument()
    const table = screen.getByText('휴지').closest('table')!
    expect(within(table).getAllByText('충전')).toHaveLength(2)
  })

  it('확산계수가 비어 있으면 무엇이 없는지 말한다 — pOCV 와 다른 이유다', async () => {
    renderDetail(detailHandler((url) =>
      path(url) === '/api/gitt/runs/1/diffusion'
        ? diffusion({ missing: ['몰부피 V_M', '계면 면적 S'], usable: 0, points: [] })
        : undefined))

    await userEvent.click(await screen.findByRole('tab', { name: '확산계수' }))
    expect(await screen.findByText(/몰부피 V_M · 계면 면적 S/)).toBeInTheDocument()
    // 추정값으로 채우면 안 된다는 이유까지 화면이 말한다.
    expect(screen.getByText(/추정의 제곱만큼/)).toBeInTheDocument()
  })

  it('재료 상수를 넣으면 저장한다', async () => {
    let sent: unknown = null
    renderDetail(detailHandler((url, init) => {
      if (path(url) === '/api/gitt/runs/1' && init?.method === 'PATCH') {
        sent = JSON.parse(String(init.body))
        return run({ area_cm2: 1.33 })
      }
      return undefined
    }))

    const input = await screen.findByLabelText('계면 면적 S')
    await userEvent.type(input, '1.33')
    await userEvent.tab()
    await waitFor(() => expect(sent).toEqual({ area_cm2: 1.33 }))
  })

  it('숫자가 안 나온 펄스는 이유와 함께 표에 남는다', async () => {
    // 조용히 빠지면 그 펄스가 없었던 것처럼 보인다.
    renderDetail(detailHandler())
    await userEvent.click(await screen.findByRole('tab', { name: '확산계수' }))
    expect(await screen.findByText(/시리즈의 첫 펄스/)).toBeInTheDocument()
    expect(screen.getByText('펄스 2개 · 숫자가 나온 것 1개')).toBeInTheDocument()
  })

  it('휴지 없이 끝난 펄스를 뺐으면 몇 개인지 말한다', async () => {
    renderDetail(detailHandler((url) =>
      path(url) === '/api/gitt/runs/1/pocv'
        ? pocv({ skipped_charge: 1,
                 skipped_reasons: ['휴지가 뒤따르지 않는 펄스'] })
        : undefined))

    expect(await screen.findByText(/뺀 펄스 1개/)).toBeInTheDocument()
  })

  it('√t 직선성이 낮은 점은 눈에 띈다', async () => {
    renderDetail(detailHandler((url) =>
      path(url) === '/api/gitt/runs/1/diffusion'
        ? diffusion({
            usable: 0,
            points: [{ capacity_mah: 0.5, voltage_v: 3.1, d_cm2_s: null,
                       delta_es_v: 0.05, delta_et_v: 0.02, pulse_s: 60,
                       sqrt_t_r_squared: 0.81,
                       reason: '√t 에 대해 직선이 아닙니다 (R²=0.810)' }],
          })
        : undefined))

    await userEvent.click(await screen.findByRole('tab', { name: '확산계수' }))
    const cell = await screen.findByText('0.810')
    expect(cell).toHaveClass('warn')
  })
})
