/** DRT 화면 — λ 가 답을 정하므로 그 값이 화면에 있어야 한다. */

import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
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

import { DrtPanel } from '../DrtPanel'

type Handler = (url: string) => unknown

function installFetch(handler: Handler) {
  const spy = vi.fn(async (url: string) => ({
    ok: true, status: 200, statusText: 'OK', json: async () => handler(url) ?? {},
  }))
  vi.stubGlobal('fetch', spy)
  return spy
}

const path = (url: string) => url.split('?')[0] ?? url
const params = (url: string) => new URL(url, 'http://x').searchParams

function drt(lambda: number, peaks: number) {
  return {
    spectrum_id: 1,
    regularisation: lambda,
    derivative_order: 1,
    tau_s: [1e-6, 1e-4, 1e-2, 1e0],
    gamma_ohm: [1, 20, 5, 0.2],
    r_inf_ohm: 5.0,
    inductance_h: null,
    chi_squared: 1e-4 * lambda,
    residual_norm: lambda,
    penalty_norm: 1 / lambda,
    peaks: Array.from({ length: peaks }, (_, i) => ({
      tau_s: 10 ** (-4 + i),
      frequency_hz: 1 / (2 * Math.PI * 10 ** (-4 + i)),
      gamma_ohm: 20 - i,
      resistance_ohm: 20 + 20 * i,
      tau_low_s: 10 ** (-5 + i),
      tau_high_s: 10 ** (-3 + i),
    })),
    total_polarisation_ohm: 60,
    dropped_inductive: 7,
  }
}

function sweep(suggested: number, reason = 'L 곡선의 곡률이 가장 큰 지점 (λ=0.01, 봉우리 2개)') {
  return {
    spectrum_id: 1,
    results: [drt(1e-6, 5), drt(1e-4, 2), drt(1e-2, 2), drt(1, 1)],
    suggested_index: suggested,
    suggested_reason: reason,
  }
}

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

describe('DRT 화면', () => {
  it('모서리가 있으면 거기서 시작하고 이유를 적는다', async () => {
    installFetch((url) =>
      path(url) === '/api/eis/spectra/1/drt/sweep' ? sweep(2) : {})
    render(<DrtPanel spectrumId={1} />)

    expect(await screen.findByText(/L 곡선의 곡률이 가장 큰 지점/)).toBeInTheDocument()
    expect(await screen.findByLabelText('벌점 λ')).toHaveValue('2')
  })

  it('모서리가 없으면 하나를 골라 주지 않고 그렇게 말한다', async () => {
    installFetch((url) =>
      path(url) === '/api/eis/spectra/1/drt/sweep'
        ? sweep(-1, 'L 곡선이 거의 직선이라 모서리가 없습니다')
        : {})
    render(<DrtPanel spectrumId={1} />)

    expect(await screen.findByText('L 곡선이 거의 직선이라 모서리가 없습니다'))
      .toBeInTheDocument()
  })

  it('λ 를 옮기면 그 λ 의 결과가 나온다 — 서버를 다시 부르지 않는다', async () => {
    const calls: string[] = []
    installFetch((url) => {
      calls.push(path(url))
      return path(url) === '/api/eis/spectra/1/drt/sweep' ? sweep(2) : {}
    })
    render(<DrtPanel spectrumId={1} />)

    const slider = await screen.findByLabelText('벌점 λ')
    const before = calls.length
    // 작은 λ 쪽 끝 — 잡음 봉우리가 다섯 개인 자리.
    fireRange(slider as HTMLInputElement, 0)
    await waitFor(() => expect(screen.getByText('5개')).toBeInTheDocument())
    expect(calls.length).toBe(before)
  })

  it('봉우리마다 그것이 감당하는 저항을 낸다', async () => {
    installFetch((url) =>
      path(url) === '/api/eis/spectra/1/drt/sweep' ? sweep(2) : {})
    render(<DrtPanel spectrumId={1} />)

    // 넓이가 저항이라는 것이 DRT 를 그림이 아니라 수로 만든다.
    const table = (await screen.findByText('저항')).closest('table')!
    const cells = within(table).getAllByRole('cell').map((cell) => cell.textContent)
    expect(cells).toContain('20.00 Ω')
    expect(cells).toContain('40.00 Ω')
  })

  it('뺀 유도성 점을 말한다', async () => {
    installFetch((url) =>
      path(url) === '/api/eis/spectra/1/drt/sweep' ? sweep(2) : {})
    render(<DrtPanel spectrumId={1} />)
    expect(await screen.findByText('유도성 7개')).toBeInTheDocument()
  })

  it('평활 차수를 바꾸면 다시 훑는다', async () => {
    const orders: (string | null)[] = []
    installFetch((url) => {
      if (path(url) === '/api/eis/spectra/1/drt/sweep') {
        orders.push(params(url).get('derivative_order'))
        return sweep(2)
      }
      return {}
    })
    render(<DrtPanel spectrumId={1} />)
    await screen.findByLabelText('벌점 λ')

    await userEvent.click(screen.getByRole('button', { name: '2' }))
    await waitFor(() => expect(orders).toContain('2'))
  })
})

/** jsdom 의 range 입력은 userEvent 로 값을 못 바꾼다 — 직접 이벤트를 쏜다. */
function fireRange(input: HTMLInputElement, value: number) {
  const setter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype, 'value')!.set!
  setter.call(input, String(value))
  input.dispatchEvent(new Event('input', { bubbles: true }))
}
