/** DRT 화면 — λ 가 답을 정하므로 그 값이 화면에 있어야 한다. */

import { fireEvent, render, screen, waitFor, within } from '@testing-library/react'
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

import { DrtPanel, tauBand } from '../DrtPanel'

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

function drt(lambda: number, peaks: number, order = 0) {
  return {
    spectrum_id: 1,
    regularisation: lambda,
    derivative_order: order,
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

function sweep(suggested: number,
               reason = 'L 곡선의 곡률이 가장 큰 지점 (λ=0.01, 봉우리 2개)',
               order = 0) {
  return {
    spectrum_id: 1,
    results: [drt(1e-6, 5, order), drt(1e-4, 2, order),
              drt(1e-2, 2, order), drt(1, 1, order)],
    suggested_index: suggested,
    suggested_reason: reason,
  }
}

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

describe('DRT 화면', () => {
  it('모서리는 버튼에 남고, 시작 자리는 적어 둔 λ 다', async () => {
    // 모서리(L 곡선)는 "데이터가 지지하는 가장 매끄러운 답" 이라 근거로는
    // 옳지만, 이 실험실이 실제로 보는 자리는 그보다 왼쪽이다 — 전고체 셀은
    // 봉우리 서넛이 겹쳐서 모서리 λ 에서는 한 언덕으로 합쳐진다.  그래서
    // 시작 자리는 기억한 값이고, 모서리는 '거기로' 한 번 거리에 남는다.
    window.localStorage.clear()
    installFetch((url) =>
      path(url) === '/api/eis/spectra/1/drt/sweep' ? sweep(2) : {})
    render(<DrtPanel spectrumId={1} />)

    expect(await screen.findByText(/L 곡선의 곡률이 가장 큰 지점/)).toBeInTheDocument()
    // 아무것도 안 골랐으면 1e-5 에서 시작한다 — 이 목록에서 가장 가까운 것은
    // 1e-6 (index 0) 이다.  로그 자로 잰다: λ 는 10배씩 움직인다.
    expect(await screen.findByLabelText('벌점 λ')).toHaveValue('0')
  })

  it('옮긴 자리를 기억한다 — 다음에 열면 거기서 시작한다', async () => {
    // 매번 슬라이더를 왼쪽 끝까지 끄는 것이 일이 됐다는 제보에서 나왔다.
    window.localStorage.clear()
    installFetch((url) =>
      path(url) === '/api/eis/spectra/1/drt/sweep' ? sweep(2) : {})
    const first = render(<DrtPanel spectrumId={1} />)
    const slider = await screen.findByLabelText('벌점 λ')
    fireEvent.change(slider, { target: { value: '3' } })   // λ = 1
    first.unmount()

    render(<DrtPanel spectrumId={1} />)
    expect(await screen.findByLabelText('벌점 λ')).toHaveValue('3')
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
        const asked = params(url).get('derivative_order')
        orders.push(asked)
        // 서버처럼 **물어본 차수**를 돌려준다.  옛 mock 은 늘 같은 차수를
        // 답해서, 화면의 신선도 판정을 우연히만 통과했다.
        return sweep(2, undefined, Number(asked ?? 0))
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

describe('τ 구간 이름', () => {
  it('τ 를 주파수와 그 시간대의 이름으로 옮긴다', () => {
    // 관례적인 구간이고 판정이 아니다 — 문장이 "…대" 로 끝난다.
    expect(tauBand(-6, 'log10')).toContain('kHz')
    expect(tauBand(-6, 'log10')).toContain('벌크')
    expect(tauBand(-4, 'log10')).toContain('입계')
    expect(tauBand(-2, 'log10')).toContain('전하이동')
    expect(tauBand(0, 'log10')).toContain('전송선')
    expect(tauBand(2, 'log10')).toContain('측정 대역 끝')
  })

  it('τ 와 주파수는 ω τ = 1 로 이어져 있다', () => {
    // log τ = -2 → τ=0.01 s → f = 1/(2π·0.01) ≈ 15.9 Hz
    expect(tauBand(-2, 'log10')).toContain('15.9 Hz')
  })

  it('같은 숫자라도 축이 다르면 다른 대다 — 그래서 축을 반드시 받는다', () => {
    // −6 은 log₁₀ 에서 1 µs (벌크 이온전도), ln 에서 2.5 ms (전하이동) 다.
    // 기본값을 두면 축을 바꾼 화면이 조용히 다른 물리를 적는다.
    expect(tauBand(-6, 'log10')).toContain('벌크')
    expect(tauBand(-6, 'ln')).toContain('전하이동')
    // 주파수도 3만 배 다르다 — 같은 눈금을 다르게 읽는다는 뜻이다.
    expect(tauBand(-6, 'log10')).toContain('kHz')
    expect(tauBand(-6, 'ln')).toContain('Hz')
    // ln τ = 0 이나 log₁₀ τ = 0 이나 τ = 1 s 라 여기서는 같다.
    expect(tauBand(0, 'ln')).toBe(tauBand(0, 'log10'))
  })
})
