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

function installFetch(scan: unknown) {
  vi.stubGlobal('fetch', vi.fn(async () => ({
    ok: true, status: 200, statusText: 'OK', json: async () => scan,
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
})
