/** 셀 상세 아래의 임피던스 — 초기와 200 사이클을 겹쳐 보는 자리. */

import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
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

import { CellSpectra, spectrumLabel } from '../CellSpectra'

type Handler = (url: string) => unknown

function installFetch(handler: Handler) {
  const spy = vi.fn(async (url: string) => ({
    ok: true, status: 200, statusText: 'OK',
    json: async () => handler(url) ?? {},
  }))
  vi.stubGlobal('fetch', spy)
  return spy
}

const path = (url: string) => url.split('?')[0] ?? url
const params = (url: string) => new URL(url, 'http://x').searchParams

function spectrum(id: number, at_cycle: number | null, name = `s${id}`) {
  return {
    id, sample_id: 1, sample_name: 'A', name, kind: 'solid',
    cell_config: 'full', original_name: `${name}.mpr`, sha256: `h${id}`,
    size_bytes: 1, source_format: 'mpr', uploaded_at: '2026-08-24T10:00:00',
    n_points: 40, frequency_start_hz: 1e6, frequency_end_hz: 1e-2,
    amplitude_mv: 5, device: '', technique: '', at_cycle, measured_at: null,
    thickness_um: null, area_cm2: null, last_circuit: '', parse_error: '',
    updated_at: '2026-08-24T10:00:00', fit_count: 0, best_chi_squared: null,
    best_circuit: '',
  }
}

function points(id: number, at_cycle: number | null) {
  return {
    id, name: `s${id}`, kind: 'solid', at_cycle,
    frequency_hz: [1e4, 1e2, 1e0],
    z_re: [5 + id, 20 + id, 45 + id],
    z_im: [-1, -12, -3],
    magnitude: [5, 23, 45],
    phase_deg: [-8, -31, -4],
  }
}

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

function renderCard(handler: Handler) {
  installFetch(handler)
  return render(
    <MemoryRouter>
      <CellSpectra sampleId={1} />
    </MemoryRouter>,
  )
}

describe('셀의 임피던스', () => {
  it('처음에는 전부 켜서 겹쳐 그린다 — 비교하려고 들어온 화면이다', async () => {
    const asked: string[] = []
    renderCard((url) => {
      if (path(url) === '/api/eis/spectra') return [spectrum(1, 0), spectrum(2, 200)]
      if (path(url) === '/api/eis/points') {
        asked.push(params(url).get('ids') ?? '')
        return [points(1, 0), points(2, 200)]
      }
      return []
    })

    await waitFor(() => expect(asked).toContain('1,2'))
    expect(await screen.findByText('구동 전')).toBeInTheDocument()
    expect(screen.getByText('200 사이클')).toBeInTheDocument()
  })

  it('하나를 끄면 그것만 빠진 채로 다시 불러온다', async () => {
    const asked: string[] = []
    renderCard((url) => {
      if (path(url) === '/api/eis/spectra') return [spectrum(1, 0), spectrum(2, 200)]
      if (path(url) === '/api/eis/points') {
        asked.push(params(url).get('ids') ?? '')
        return [points(1, 0)]
      }
      return []
    })

    const chip = await screen.findByRole('button', { name: /구동 전/ })
    await userEvent.click(chip)
    await waitFor(() => expect(asked).toContain('2'))
    expect(chip).toHaveAttribute('aria-pressed', 'false')
  })

  it('전부 끄면 빈 그래프 대신 왜 비었는지 말한다', async () => {
    renderCard((url) => {
      if (path(url) === '/api/eis/spectra') return [spectrum(1, 0)]
      if (path(url) === '/api/eis/points') return [points(1, 0)]
      return []
    })

    await userEvent.click(await screen.findByRole('button', { name: '비우기' }))
    expect(await screen.findByText('고른 스펙트럼이 없습니다.')).toBeInTheDocument()
  })

  it('스펙트럼이 없으면 어디로 가야 하는지 말한다', async () => {
    renderCard((url) => (path(url) === '/api/eis/spectra' ? [] : []))
    expect(await screen.findByText('이 셀에 붙은 스펙트럼이 없습니다')).toBeInTheDocument()
    // 올릴 곳으로 바로 보낸다.  대시보드로 보내면 거기서 업로드를 한 번 더
    // 찾아야 하고, 이 화면에 온 사람은 이미 "없다" 를 본 참이다.
    expect(screen.getByRole('link', { name: /업로드/ }))
      .toHaveAttribute('href', '/eis/upload')
  })

  it('그 셀의 스펙트럼만 부른다', async () => {
    let asked: string | null = null
    renderCard((url) => {
      if (path(url) === '/api/eis/spectra') {
        asked = params(url).get('sample_id')
        return []
      }
      return []
    })
    await waitFor(() => expect(asked).toBe('1'))
  })
})

describe('spectrumLabel', () => {
  it('사이클 번호가 이름을 대신한다', () => {
    // 파일 이름 둘이 열두 글자쯤 같고 끝만 다르면, 겹쳐 놓은 그림에서 그것은
    // 이름이 없는 것과 같다.
    expect(spectrumLabel({ name: '260719_No1_sym_01', at_cycle: 0 })).toBe('구동 전')
    expect(spectrumLabel({ name: '260719_No1_sym_02', at_cycle: 200 })).toBe('200 사이클')
  })

  it('번호가 없으면 이름을 쓴다', () => {
    expect(spectrumLabel({ name: 'pellet_a', at_cycle: null })).toBe('pellet_a')
  })
})
