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
/** 한 스윕의 γ(τ).  DRT 는 스윕마다 한 번씩 부르는 계산이라 주소가 또 다르다. */
function drtOf(id: number) {
  return {
    spectrum_id: id,
    regularisation: 1e-5,
    derivative_order: 0,
    tau_s: [1e-4, 1e-2, 1],
    gamma_ohm: [2, 8, 1],
    r_inf_ohm: 5,
    inductance_h: null,
    chi_squared: 1e-4,
    residual_norm: 1e-3,
    penalty_norm: 1,
    peaks: [],
    total_polarisation_ohm: 11,
    dropped_inductive: 0,
  }
}

function installFetch(scan: unknown, points: unknown[] = [
  sweepPoints(1), sweepPoints(2), sweepPoints(3),
]) {
  vi.stubGlobal('fetch', vi.fn(async (url: string) => {
    const path = String(url).split('?')[0] ?? ''
    const body = path.endsWith('/points') ? points
      : path.includes('/drt') ? drtOf(Number(path.split('/')[4] ?? 1))
      : scan
    return { ok: true, status: 200, statusText: 'OK', json: async () => body }
  }))
}

function show() {
  return render(
    <MemoryRouter initialEntries={['/scans/abc']}>
      <Routes>
        <Route path="/scans/:sha256" element={<ScanDetail />} />
        {/* 이름 링크가 실제로 가는 자리.  안 세워 두면 클릭이 라우터를 빈
            화면으로 보내고, 시험은 "줄이 안 꺼졌다" 대신 "아무것도 없다" 를
            본다 — 두 실패가 같아 보인다. */}
        <Route path="/eis/:id" element={<div>스펙트럼 상세</div>} />
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
    }, [sweepPoints(1), sweepPoints(2)])
    show()

    const button = await screen.findByRole('button', { name: 'Ω·cm²' })
    expect(button).toBeDisabled()
    // 왜 못 누르는지가 단추에 붙어 있어야 한다 — 흐린 단추만으로는 고장이다.
    expect(button.getAttribute('title')).toContain('면적')
  })

  /** 두 곳이 따로 놀면 표에서 흐린 줄이 그림에는 그려져 있고, 어느 쪽이 맞는지
   *  화면이 말해 주지 않는다. */
  it('범례와 표가 같은 선택을 쓴다 — 전체·초기화도 함께 움직인다', async () => {
    installFetch({
      sha256: 'abc', name: '스캔', original_name: 'scan.mpr', kind: 'liquid',
      cell_config: 'half', purpose: 'SOC별', sample_id: null, sample_name: null,
      sweeps: 3, fitted: 3, parameters: ['R0'], area_cm2_effective: null,
      points: [point(1, { R0: 5 }), point(2, { R0: 6 }), point(3, { R0: 7 })],
    })
    show()

    await waitFor(() =>
      expect(document.querySelectorAll('.legend-chip')).toHaveLength(3))
    const chips = () => [...document.querySelectorAll('.legend-chip')]
    const rows = () => [...document.querySelectorAll('tbody tr')]
    // 처음에는 전부 켜져 있다 — 스캔을 여는 이유가 전체 모양이다.
    expect(chips().filter((chip) => chip.className.includes('off'))).toHaveLength(0)

    // 표의 줄을 누르면 그림의 조각이 꺼진다.
    await userEvent.click(rows()[1] as HTMLElement)
    expect(chips()[1]!.className).toContain('off')
    expect(rows()[1]!.className).toContain('dim')

    await userEvent.click(screen.getByRole('button', { name: '초기화' }))
    expect(chips().filter((chip) => chip.className.includes('off'))).toHaveLength(3)

    await userEvent.click(screen.getByRole('button', { name: '전체' }))
    expect(chips().filter((chip) => chip.className.includes('off'))).toHaveLength(0)
  })

  it('이름 링크를 눌러도 스윕이 꺼지지 않는다 — 그건 상세로 가는 길이다', async () => {
    installFetch({
      sha256: 'abc', name: '스캔', original_name: 'scan.mpr', kind: 'liquid',
      cell_config: 'half', purpose: 'SOC별', sample_id: null, sample_name: null,
      sweeps: 2, fitted: 2, parameters: ['R0'], area_cm2_effective: null,
      points: [point(1, { R0: 5 }), point(2, { R0: 6 })],
    }, [sweepPoints(1), sweepPoints(2)])
    show()

    await waitFor(() =>
      expect(document.querySelectorAll('.legend-chip')).toHaveLength(2))
    await userEvent.click(await screen.findByRole('link', { name: 'sweep 1' }))
    // 스펙트럼 상세로 갔다 — 줄을 끄지 않았다.
    expect(await screen.findByText('스펙트럼 상세')).toBeInTheDocument()
  })

  it('DRT 로 바꾸면 같은 스윕을 γ 로 그리고, 축 고르개가 함께 뜬다', async () => {
    window.localStorage.clear()
    installFetch({
      sha256: 'abc', name: '스캔', original_name: 'scan.mpr', kind: 'liquid',
      cell_config: 'half', purpose: 'SOC별', sample_id: null, sample_name: null,
      sweeps: 2, fitted: 2, parameters: ['R0'], area_cm2_effective: null,
      points: [point(1, { R0: 5 }), point(2, { R0: 6 })],
    }, [sweepPoints(1), sweepPoints(2)])
    show()

    // 나이퀴스트에는 τ 축이 없으므로 가로축 고르개도 없다.
    await screen.findByRole('group', { name: '그림' })
    expect(screen.queryByRole('group', { name: '가로축' })).toBeNull()

    await userEvent.click(screen.getByRole('button', { name: 'DRT' }))
    expect(await screen.findByRole('group', { name: '가로축' })).toBeTruthy()
    // 클립보드도 지금 보이는 그림을 따라간다.
    await waitFor(() =>
      expect(screen.getByRole('button', { name: /γ\(τ\) \(스윕 전부\)/ }))
        .toBeInTheDocument())
  })

  it('면적을 알면 용량과 저항을 면적으로 나눈 열이 함께 나온다', async () => {
    installFetch({
      sha256: 'abc', name: '스캔', original_name: 'scan.mpr', kind: 'liquid',
      cell_config: 'half', purpose: 'SOC별', sample_id: null, sample_name: null,
      sweeps: 1, fitted: 1, parameters: ['R0'], area_cm2_effective: 2,
      points: [{ ...point(1, { R0: 5 }), capacity_mah: 3,
                 series_resistance_ohm: 5, total_resistance_ohm: 30 }],
    }, [sweepPoints(1)])
    show()

    await screen.findByRole('columnheader', { name: '용량 (mAh/cm²)' })
    const cells = [...document.querySelectorAll('tbody tr td')]
      .map((cell) => cell.textContent)
    expect(cells).toContain('1.500')   // 3 mAh / 2 cm²
    expect(cells).toContain('10.00')   // 5 Ω × 2 cm²
    expect(cells).toContain('60.00')   // 30 Ω × 2 cm²
  })

  it('면적을 모르면 그 열은 줄표다 — 0 으로 채우면 만방전과 구분되지 않는다',
     async () => {
    installFetch({
      sha256: 'abc', name: '스캔', original_name: 'scan.mpr', kind: 'liquid',
      cell_config: 'half', purpose: 'SOC별', sample_id: null, sample_name: null,
      sweeps: 1, fitted: 1, parameters: ['R0'], area_cm2_effective: null,
      points: [{ ...point(1, { R0: 5 }), capacity_mah: 3,
                 series_resistance_ohm: 5, total_resistance_ohm: 30 }],
    }, [sweepPoints(1)])
    show()

    await screen.findByRole('columnheader', { name: 'R₀ (Ω·cm²)' })
    const row = document.querySelector('tbody tr')!
    const cells = [...row.querySelectorAll('td')].map((cell) => cell.textContent)
    // 용량 3, 그 다음 칸(mAh/cm²)이 줄표.
    expect(cells[2]).toBe('3.000')
    expect(cells[3]).toBe('—')
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
    }, [sweepPoints(1), sweepPoints(2)])
    show()
    await screen.findByRole('columnheader', { name: 'R₀ (Ω)' })
    // 첫 줄은 견줄 것이 없어 줄표, 둘째 줄이 +1.5 다.
    expect(screen.getByText('+1.50')).toBeInTheDocument()
    // 내려간 것은 − 로 — 부호가 곧 이 열을 보는 이유다.
    expect(screen.getByText('−2.00')).toBeInTheDocument()
  })
})
