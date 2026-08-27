/** SOC 스캔 상세 — 결정되지 않은 점을 어떻게 다루는지가 이 화면의 전부다. */

import { render, screen, waitFor } from '@testing-library/react'
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

import { ScanDetail } from '../ScanDetail'

function point(index: number, values: Record<string, number>) {
  return {
    spectrum_id: index, sweep_index: index, name: `sweep ${index}`,
    capacity_mah: index * 0.5, potential_v: 3.5 + index * 0.1,
    fit_id: Object.keys(values).length ? index : null,
    circuit: 'R0-p(R1,CPE1)', chi_squared: 0.01,
    values, labels: { R1: 'SEI 저항' },
  }
}

/** 스윕 하나의 점 — 나이퀴스트 겹쳐보기가 이것을 받는다. */
function sweepPoints(index: number) {
  return {
    id: index, name: `sweep ${index}`, kind: 'liquid', at_cycle: null,
    frequency_hz: [1e5, 1e3, 1e1, 1e-1],
    z_re: [5, 8, 14, 22], z_im: [0.5, -2, -4, -6],
    magnitude: [5, 8.2, 14.6, 22.8], phase_deg: [6, -14, -16, -15],
  }
}

/** **주소를 보고 답한다.**  하나로 뭉뚱그리면 `/points` 요청에도 스캔 객체가
 *  돌아오고, 화면은 그것을 배열로 여겨 죽는다 — 그런데 그 죽음은 "스캔을 못
 *  읽었다" 로 보여서, 실제 원인(엉뚱한 응답)과 정반대로 읽힌다. */
function installFetch(scan: unknown, points: unknown[] = [
  sweepPoints(1), sweepPoints(2), sweepPoints(3),
]) {
  vi.stubGlobal('fetch', vi.fn(async (url: string) => ({
    ok: true, status: 200, statusText: 'OK',
    json: async () => (String(url).endsWith('/points') ? points : scan),
  })))
}

function show() {
  return render(
    <MemoryRouter initialEntries={['/scans/abc']}>
      <Routes>
        <Route path="/scans/:sha256" element={<ScanDetail />} />
      </Routes>
    </MemoryRouter>,
  )
}

afterEach(() => vi.unstubAllGlobals())

describe('ScanDetail', () => {
  it('결정되지 않은 스윕은 그래프에서 빠지고, 몇 개인지 말한다', async () => {
    installFetch({
      sha256: 'abc', name: '스캔', original_name: 'scan.mpr', kind: 'liquid',
      cell_config: 'half', purpose: 'SOC별', sample_id: null, sample_name: null,
      sweeps: 3, fitted: 3, parameters: ['R0', 'R1'],
      points: [point(1, { R0: 5, R1: 20 }), point(2, { R0: 6 }),
               point(3, { R0: 7, R1: 24 })],
    })
    show()

    await screen.findByText('스캔')
    // R0 은 셋 다 결정됐다 — 경고가 없어야 한다.
    const picker = await screen.findByLabelText('파라미터')
    expect(screen.queryByText(/빠졌습니다/)).toBeNull()

    // R1 은 둘뿐이다.  빠진 하나를 조용히 넘기면 사람은 점 수가 다른 것을
    // 못 본다 -- 세 SOC 를 잰 셀의 추세가 두 점짜리 직선이 된다.
    await userEvent.selectOptions(picker, 'R1')
    await waitFor(() => expect(screen.getByText(/1개 스윕은/)).toBeTruthy())
  })

  it('맞춘 회로가 없으면 무엇을 하면 되는지 말한다', async () => {
    installFetch({
      sha256: 'abc', name: '스캔', original_name: 'scan.mpr', kind: 'liquid',
      cell_config: '', purpose: '', sample_id: null, sample_name: null,
      sweeps: 3, fitted: 0, parameters: [],
      points: [point(1, {}), point(2, {}), point(3, {})],
    })
    show()

    await screen.findByText(/아직 맞춘 회로가 없습니다/)
    // x 축은 살아 있다 — 무엇을 잰 것인지는 볼 수 있어야 한다.
    expect(screen.getByText('3.600')).toBeTruthy()
    expect(screen.getByText('3.800')).toBeTruthy()
  })

  it('값이 없는 칸은 0 이 아니라 줄표다', async () => {
    installFetch({
      sha256: 'abc', name: '스캔', original_name: 'scan.mpr', kind: 'liquid',
      cell_config: '', purpose: '', sample_id: null, sample_name: null,
      sweeps: 2, fitted: 2, parameters: ['R0', 'R1'],
      points: [point(1, { R0: 5, R1: 20 }), point(2, { R0: 6 })],
    })
    show()

    await screen.findByText('스캔')
    const dashes = await screen.findAllByText('—')
    expect(dashes.length).toBeGreaterThan(0)
    expect(screen.queryByText('0.0000')).toBeNull()
  })

  it('스윕을 한 화면에 겹쳐 그리고, 조각을 눌러 끈다', async () => {
    installFetch({
      sha256: 'abc', name: '스캔', original_name: 'scan.mpr', kind: 'liquid',
      cell_config: 'half', purpose: 'SOC별', sample_id: null, sample_name: null,
      sweeps: 3, fitted: 3, parameters: ['R0'],
      points: [point(1, { R0: 5 }), point(2, { R0: 6 }), point(3, { R0: 7 })],
    })
    show()
    // 스윕 셋이 조각 셋으로 — 파일 하나가 목록에서 세 줄이던 것을 한 그림으로.
    await waitFor(() =>
      expect(document.querySelectorAll('.legend-chip')).toHaveLength(3))
    // 조각에 SOC 를 적는다.  `#2` 만으로는 어느 충전 상태인지 모르고, 그것이
    // 이 화면을 여는 이유다.
    const chips = [...document.querySelectorAll('.legend-chip')]
    expect(chips.map((chip) => chip.textContent).join(' ')).toContain('mAh')
    // 끄면 조각이 남고 곡선만 빠진다 (충방전 사이클 고르개와 같은 손놀림).
    await userEvent.click(chips[1] as HTMLElement)
    expect(chips[1]!.className).toContain('off')
  })

  /** 단위는 화면 하나에 하나다.  나이퀴스트를 Ω 로 보다 비교 화면에서
   *  Ω·cm² 로 보면 같은 아크가 다른 크기로 나오고, 그 말은 축 이름에만 남는다. */
  it('면적이 있으면 Ω·cm² 로 바꿀 수 있다', async () => {
    window.localStorage.clear()
    installFetch({
      sha256: 'abc', name: '스캔', original_name: 'scan.mpr', kind: 'liquid',
      cell_config: 'half', purpose: 'SOC별', sample_id: null, sample_name: null,
      sweeps: 3, fitted: 3, parameters: ['R0'], area_cm2_effective: 2,
      points: [point(1, { R0: 5 }), point(2, { R0: 6 }), point(3, { R0: 7 })],
    })
    show()

    // 기본은 Ω — 계측기가 준 수다.  안 나눴으면 나눴다는 말도 없다.
    const ohm = await screen.findByRole('button', { name: 'Ω' })
    expect(ohm.className).toContain('on')
    expect(document.body.textContent).not.toContain('나눈 값입니다')

    await userEvent.click(screen.getByRole('button', { name: 'Ω·cm²' }))
    // **나눴으면 무엇으로 나눴는지 적는다.**  축 이름은 그림 안에 있어서
    // 캡처를 붙여 넣으면 따라가지만, 이 줄은 화면에서 바로 읽힌다.
    await waitFor(() =>
      expect(document.body.textContent).toContain('면적 2.000 cm² 로 나눈 값입니다'))
    expect(screen.getByRole('button', { name: 'Ω' }).className).not.toContain('on')
  })

  it('면적이 없거나 스윕마다 다르면 Ω·cm² 를 못 누르고, 왜인지 적는다', async () => {
    window.localStorage.clear()
    installFetch({
      sha256: 'abc', name: '스캔', original_name: 'scan.mpr', kind: 'liquid',
      cell_config: 'half', purpose: 'SOC별', sample_id: null, sample_name: null,
      sweeps: 2, fitted: 2, parameters: ['R0'], area_cm2_effective: null,
      points: [point(1, { R0: 5 }), point(2, { R0: 6 })],
    })
    show()

    const button = await screen.findByRole('button', { name: 'Ω·cm²' })
    expect(button).toBeDisabled()
    // 왜 못 누르는지가 단추에 붙어 있어야 한다 — 흐린 단추만으로는 고장이다.
    expect(button.getAttribute('title')).toContain('면적')
  })

  it('스윕 표에 R₀ 와 그 변화가 나온다 — SOC 를 따라가는 값이 그것이다', async () => {
    installFetch({
      sha256: 'abc', name: '스캔', original_name: 'scan.mpr', kind: 'liquid',
      cell_config: 'half', purpose: 'SOC별', sample_id: null, sample_name: null,
      sweeps: 2, fitted: 2, parameters: ['R0'],
      points: [
        { ...point(1, { R0: 5 }), series_resistance_ohm: 5, total_resistance_ohm: 30 },
        { ...point(2, { R0: 6 }), series_resistance_ohm: 6.5, total_resistance_ohm: 28 },
      ],
    })
    show()
    await screen.findByRole('columnheader', { name: 'R₀ (Ω)' })
    // 첫 줄은 견줄 것이 없어 줄표, 둘째 줄이 +1.5 다.
    expect(screen.getByText('+1.50')).toBeInTheDocument()
    // 내려간 것은 − 로 — 부호가 곧 이 열을 보는 이유다.
    expect(screen.getByText('−2.00')).toBeInTheDocument()
  })
})
