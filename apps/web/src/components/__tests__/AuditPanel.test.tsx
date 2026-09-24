/** 스펙트럼 화면의 측정 품질 칸 (ADR 0046) — 랩이 "확실히 잡을 수 있으면" 한
 *  것은 KK 어긋남과 잡음이다.  그것이 칩·수·문장·그림으로 먼저 보이고, 맞춤과
 *  기록의 판정은 따로 적히는지를 본다. */

import { render, screen, waitFor, within } from '@testing-library/react'
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

import { AuditPanel, dcRows, residualSeries } from '../AuditPanel'
import type { AuditFinding, SpectrumAuditDetail } from '../../lib/types'

function finding(code: string, scope: AuditFinding['scope'], message: string,
                 severity: AuditFinding['severity'] = 'check', refs: string[] = []
): AuditFinding {
  const label = { problem: '문제', check: '확인', note: '참고' }[severity]
  return { severity, label, code, message, refs, circuits: [], scope }
}

/** 실측 풀셀 #1 (Dcell39) 꼴: 저주파 끝이 KK 를 어긴다. */
function drifting(extra: AuditFinding[] = []): SpectrumAuditDetail {
  return {
    audit: {
      id: 1, circuit: 'L1-R0-p(R1,CPE1)-TL1',
      misfit_mean: 0.0066, misfit_max: 0.028, misfit_at_hz: 0.0637,
      kk: {
        judged: true, reason: '', max_residual: 0.054, at_hz: 0.01, sigma: 0.0033,
        m: 23, per_decade: 3.1, dropped_inductive: 15, range_switches_hz: [595, 2.9],
      },
      findings: [
        finding('kk_violation', 'points',
                '저주파 끝 0.01–1.02 Hz 가 Kramers–Kronig 를 어깁니다', 'check',
                ['VADHVA2021.kk-validation-before-modelling']),
        finding('at_bound', 'fit', 'TL1_Wn 이 상한(0.8)에 붙었습니다'),
        finding('undetermined', 'fit', '미결정 파라미터: R0', 'note'),
        finding('area_large', 'record', '면적 10 cm² 는 펠릿·코인 셀의 면적으로 큽니다'),
        ...extra,
      ],
      worst: 'check',
    },
    references: [{
      id: 'VADHVA2021.kk-validation-before-modelling',
      citation: 'Vadhva 외 2021, p. 1935', claim_ko: '모델링 전에 KK 로 검사하라', quote: '',
    }],
    residuals: {
      frequency_hz: [0.01, 0.1, 1, 10, 100],
      kk: [0.054, 0.02, 0.004, 0.002, 0.003],
      fit_frequency_hz: [0.01, 0.1, 1, 10],
      fit: [0.028, 0.01, 0.004, 0.003],
      sigma: 0.0033,
      limit: 0.02,
    },
  }
}

function installFetch(body: unknown) {
  const spy = vi.fn(async (_url: string) => ({
    ok: true, status: 200, statusText: 'OK', json: async () => body,
  }))
  vi.stubGlobal('fetch', spy)
  return spy
}

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('AuditPanel', () => {
  it('puts what the points say first, then the fit and the record apart', async () => {
    const spy = installFetch(drifting())
    render(<AuditPanel spectrumId={1} />)
    await waitFor(() => expect(screen.getByText('KK 어긋남')).toBeTruthy())
    expect(String(spy.mock.calls[0]?.[0])).toContain('/api/eis/spectra/1/audit')
    expect(screen.queryByText('KK 통과')).toBeNull()

    // 수: 최대 잔차와 그 주파수, 선, 잡음과 보통 범위, 뺀 유도성 점, 범위 전환.
    expect(screen.getByText('5.4 % (10.0 mHz)')).toBeTruthy()
    expect(screen.getByText('2.0 % (2 % 와 6σ 중 큰 쪽)')).toBeTruthy()
    expect(screen.getByText('0.33 % (보통 0.1–0.5 %)')).toBeTruthy()
    expect(screen.getByText('꼭대기 15점 (배선 인덕턴스)')).toBeTruthy()
    expect(screen.getByText('595 Hz, 2.90 Hz')).toBeTruthy()

    // 문장은 그대로, 근거는 번호로 — 보고서와 같은 규칙.
    const kk = screen.getByText(/저주파 끝 0.01–1.02 Hz/)
    expect(kk.textContent).toContain('[근거 1]')
    // 맞춤은 어느 맞춤의 것인지 적고, 기록은 따로.
    expect(screen.getByText('맞춤 — 쓰는 맞춤 L1-R0-p(R1,CPE1)-TL1')).toBeTruthy()
    expect(screen.getByText('기록')).toBeTruthy()
    expect(screen.getByText(/면적 10 cm²/)).toBeTruthy()
    expect(screen.getByText('근거 1')).toBeTruthy()
  })

  it('says the fit was not judged when the points are too noisy', async () => {
    installFetch(drifting([finding('too_noisy_to_judge', 'fit',
      '잡음(KK 잔차의 σ ≈ 7.3 %)이 회로를 판정하는 문턱(평균 오차 3 %)보다 커서 맞춤은 '
      + '판정하지 않았습니다', 'note'),
      finding('kk_noisy', 'points', '잡음이 큽니다 (KK 잔차의 σ ≈ 7.3 %)', 'note')]))
    render(<AuditPanel spectrumId={1} />)
    await waitFor(() => expect(screen.getByText('맞춤 판정 안 함 — 잡음이 큼')).toBeTruthy())
    const chips = screen.getByLabelText('점 자체의 판정')
    expect(within(chips).getByText('잡음 큼')).toBeTruthy()
  })

  it('passes a clean spectrum', async () => {
    const clean = drifting()
    clean.audit.findings = []
    clean.references = []
    installFetch(clean)
    render(<AuditPanel spectrumId={1} />)
    await waitFor(() => expect(screen.getByText('KK 통과')).toBeTruthy())
    expect(screen.getByText('점 자체에 대한 판정은 없습니다.')).toBeTruthy()
  })
})

describe('dcRows — was the cell at rest (ADR 0043 보완 7)', () => {
  it('reads the current when the potential was held, and how far it moved in a period', () => {
    expect(dcRows({ judged: true, duration_s: 968, source: 'current',
                    current_ua: [300, 95.5], potential_v: [3.7, 3.7], share: 0.078,
                    at_hz: 0.01 }))
      .toEqual([['직류 전류 (스윕 동안)', '300 → 95.5 µA (16.1 분)'],
                ['한 주기의 직류 변화', '교류 진폭의 7.8 % (10.0 mHz)']])
  })

  it('says a level that did not move did not move', () => {
    expect(dcRows({ judged: true, duration_s: 44, source: 'current',
                    current_ua: [0.012, 0.011], share: 2e-5, at_hz: 265 })[1])
      .toEqual(['한 주기의 직류 변화', '교류 진폭의 0.01 % 미만'])
  })

  it('does not read a potential the instrument held as a cell at rest', () => {
    expect(dcRows({ judged: true, duration_s: 44, source: 'potential',
                    potential_v: [3.7, 3.7], share: 1e-9, at_hz: 265 })).toEqual([])
  })

  it('reads the potential when that is what moved (a galvanostatic sweep)', () => {
    expect(dcRows({ judged: true, duration_s: 600, source: 'potential',
                    potential_v: [3.7012, 3.6921], share: 0.1, at_hz: 0.01 })[0])
      .toEqual(['직류 전위 (스윕 동안)', '3.7012 → 3.6921 V (-9.1 mV, 10.0 분)'])
  })

  it('says nothing when the file kept no record', () => {
    expect(dcRows(undefined)).toEqual([])
    expect(dcRows({ judged: false, reason: '파일에 점마다의 시각이 없습니다' })).toEqual([])
  })

  it('shows up among the numbers of the panel, and as a chip when it is a finding', async () => {
    const settling = drifting([finding('dc_drift', 'points',
      '직류 전류가 스윕 동안 300 → 95.5 µA 로 변했습니다 — 셀이 평형이 아니었습니다', 'note')])
    settling.audit.dc = { judged: true, duration_s: 968, source: 'current',
                          current_ua: [300, 95.5], share: 0.078, at_hz: 0.01 }
    installFetch(settling)
    render(<AuditPanel spectrumId={1} />)
    await waitFor(() => expect(screen.getByText('직류 전류 (스윕 동안)')).toBeTruthy())
    expect(screen.getByText('교류 진폭의 7.8 % (10.0 mHz)')).toBeTruthy()
    const chips = screen.getByLabelText('점 자체의 판정')
    expect(within(chips).getByText('셀이 안 쉼')).toBeTruthy()
  })
})

describe('AuditPanel on an answer it cannot read', () => {
  it('says so instead of taking the spectrum page down', async () => {
    installFetch({})                      // 옛 서버 · 모양이 다른 답
    render(<AuditPanel spectrumId={1} />)
    await waitFor(() => expect(screen.getByText(/검수를 읽지 못했습니다/)).toBeTruthy())
  })
})

describe('residualSeries', () => {
  it('draws the KK and fit residuals in % against log f, and the line flat across', () => {
    const [kk, fit, line] = residualSeries(drifting())
    expect(kk?.label).toBe('KK — 점 자체')
    expect(kk?.x).toEqual([-2, -1, 0, 1, 2])
    expect(kk?.y[0]).toBeCloseTo(5.4)
    expect(fit?.label).toBe('맞춤 — L1-R0-p(R1,CPE1)-TL1')
    expect(fit?.x).toHaveLength(4)
    expect(line?.x).toEqual([-2, 2])
    expect(line?.y).toEqual([2, 2])
    expect(line?.dash).toBeTruthy()
  })

  it('draws nothing without residuals', () => {
    const none = drifting()
    none.residuals = { frequency_hz: [], kk: [], fit_frequency_hz: [], fit: [],
                       sigma: null, limit: null }
    expect(residualSeries(none)).toEqual([])
    expect(residualSeries(null)).toEqual([])
  })
})
