/** 검수 — `bml audit` 이 이 스펙트럼에 하는 말, 측정의 사정이 먼저 (ADR 0046).
 *
 *  랩은 KK 어긋남과 잡음을 "문제" 로 세지 말고, 이 화면에서 **확실히** 보이게
 *  해 달라고 했다.  그래서 점 자체의 판정을 맨 위에 잔차 그림과 함께 둔다.
 *  맞춤과 기록의 판정은 그 아래 따로 적는다 — 한 목록에 섞으면 어긋남이 측정
 *  탓인지 회로 탓인지가 다시 섞인다.
 *
 *  **쓰는 맞춤**을 본다 (ADR 0045).  위의 나이퀴스트가 방금 시험 삼아 맞춘 것을
 *  그리고 있어도, 검수는 목록·σ·스캔이 읽는 맞춤의 것이다.  그래서 회로 이름을
 *  같이 적는다.
 */

import { useMemo } from 'react'

import { Plot, PlotLegend, type PlotSeries } from './Plot'
import { Alert, Card, KeyValues, Spinner } from './ui'
import { api } from '../lib/api'
import { seriesColor } from '../lib/format'
import { useAsync } from '../lib/hooks'
import type { AuditFinding, AuditReference, SpectrumAuditDetail } from '../lib/types'
import { hertz } from '../pages/Eis'

/** 점 자체의 판정 — 칩 하나에 한 사정.  문장은 아래 목록에 그대로 있다. */
const POINT_CHIPS: [string, string][] = [
  ['kk_violation', 'KK 어긋남'],
  ['kk_outlier', '튄 점'],
  ['kk_range_switch', '전류 범위 전환 자국'],
  ['kk_high_frequency', '고주파 끝 어긋남'],
  ['low_frequency_inductive', '저주파 유도성'],
  ['kk_noisy', '잡음 큼'],
]

const SEVERITY_BADGE: Record<AuditFinding['severity'], string> = {
  problem: 'danger', check: 'warn', note: 'plain',
}

const SCOPES: [AuditFinding['scope'], string][] = [
  ['fit', '맞춤'],
  ['record', '기록'],
]

/** 비율을 % 로.  잔차는 비율로 온다 (0.054 = 5.4 %). */
function pct(fraction: number | null | undefined, digits = 1): string {
  if (fraction === null || fraction === undefined || !Number.isFinite(fraction)) return '—'
  return `${(fraction * 100).toFixed(digits)} %`
}

export function AuditPanel({ spectrumId, refresh }: {
  spectrumId: number
  /** 바뀌면 다시 읽는다 — 맞춘 뒤, 쓰는 맞춤을 고른 뒤, 셀을 고친 뒤. */
  refresh?: unknown
}) {
  const state = useAsync(() => api.spectrumAudit(spectrumId), [spectrumId, refresh])
  const data = state.data

  const series = useMemo<PlotSeries[]>(() => residualSeries(data), [data])
  const numbering = useMemo(() => referenceNumbers(data), [data])

  if (state.error) {
    return <Card title="측정 품질"><Alert kind="error">{state.error}</Alert></Card>
  }
  if (!data) {
    return <Card title="측정 품질"><Spinner /></Card>
  }
  // 검수가 못 읽혀도 스펙트럼 화면은 서 있어야 한다 — 이 칸 하나가 깨지면
  // 나이퀴스트와 피팅까지 같이 사라진다 (옛 서버, 모양이 다른 답).
  if (!data.audit || !data.residuals) {
    return (
      <Card title="측정 품질">
        <div className="small faint">검수를 읽지 못했습니다 — 서버를 새로 띄우면 나옵니다.</div>
      </Card>
    )
  }
  const { audit, residuals } = data
  const kk = audit.kk ?? {}
  const findings = audit.findings ?? []
  const points = findings.filter((one) => one.scope === 'points')
  const codes = new Set(findings.map((one) => one.code))
  const chips = POINT_CHIPS.filter(([code]) => codes.has(code))
  const gated = codes.has('too_noisy_to_judge')

  return (
    <Card title="측정 품질">
      <div className="col" style={{ gap: 10 }}>
        <div className="chip-row" aria-label="점 자체의 판정">
          {kk.judged === false ? (
            <span className="badge unknown">KK 판정 못 함</span>
          ) : chips.length ? (
            chips.map(([code, label]) => (
              <span key={code} className={`badge ${code === 'kk_violation' ? 'warn' : 'plain'}`}>
                {label}
              </span>
            ))
          ) : (
            <span className="badge finished">KK 통과</span>
          )}
          {gated ? <span className="badge warn">맞춤 판정 안 함 — 잡음이 큼</span> : null}
        </div>

        {kk.judged === false ? (
          <div className="small dim">{kk.reason || '점이 모자라 KK 를 맞추지 못했습니다'}</div>
        ) : (
          <KeyValues
            cols={2}
            rows={[
              ['KK 잔차 최대', `${pct(kk.max_residual)}${
                kk.at_hz ? ` (${hertz(kk.at_hz)})` : ''}`],
              ['어긋남으로 보는 선', `${pct(residuals.limit)} (2 % 와 6σ 중 큰 쪽)`],
              ['잡음 σ', `${pct(kk.sigma, 2)} (보통 0.1–0.5 %)`],
              ['Voigt 소자', kk.m ? `${kk.m}개 (decade 당 ${(kk.per_decade ?? 0).toFixed(1)})` : '—'],
              ['뺀 유도성 점', kk.dropped_inductive
                ? `꼭대기 ${kk.dropped_inductive}점 (배선 인덕턴스)` : '없음'],
              ['전류 범위 전환', kk.range_switches_hz?.length
                ? kk.range_switches_hz.map(hertz).join(', ') : '—'],
            ]}
          />
        )}
        {kk.reason && kk.judged !== false ? (
          <div className="tiny faint">{kk.reason}</div>
        ) : null}

        <FindingList findings={points} numbering={numbering}
                     empty="점 자체에 대한 판정은 없습니다." />

        {series.length ? (
          <div>
            <Plot series={series} xLabel="log₁₀ f (Hz)" yLabel="|ΔZ| / |Z| (%)"
                  height={200} legend yRange={[0, null]}
                  pngName="KK 잔차" pngTitle="Kramers–Kronig 잔차" />
            {/* 곡선이 둘 이상이면 범례가 있어야 한다 — 색만으로 가르지 않는다. */}
            <PlotLegend series={series} />
            <div className="tiny faint" style={{ paddingTop: 6 }}>
              KK 는 선형·시불변인 셀이 그릴 수 있는 모든 스펙트럼을 그립니다 — 선 위로
              솟은 점은 어떤 회로로도 못 그리는 점입니다 (측정 중 셀 변화, 튄 점, 범위
              전환). 맞춤만 높고 KK 가 낮으면 회로 탓입니다.
            </div>
          </div>
        ) : null}

        {SCOPES.map(([scope, title]) => {
          const found = findings.filter((one) => one.scope === scope)
          if (!found.length) return null
          return (
            <div key={scope} className="col" style={{ gap: 6 }}>
              <div className="small dim" style={{ fontWeight: 600 }}>
                {scope === 'fit' && audit.circuit
                  ? `${title} — 쓰는 맞춤 ${audit.circuit}` : title}
              </div>
              <FindingList findings={found} numbering={numbering} />
            </div>
          )
        })}

        <References references={data.references} numbering={numbering} />
      </div>
    </Card>
  )
}

function FindingList({ findings, numbering, empty }: {
  findings: AuditFinding[]
  numbering: Map<string, number>
  empty?: string
}) {
  if (!findings.length) {
    return empty ? <div className="small faint">{empty}</div> : null
  }
  return (
    <ul className="col" style={{ gap: 6, margin: 0, paddingLeft: 0, listStyle: 'none' }}>
      {findings.map((one, index) => (
        <li key={`${one.code}-${index}`} className="row small"
            style={{ gap: 8, alignItems: 'baseline', flexWrap: 'nowrap' }}>
          <span className={`badge ${SEVERITY_BADGE[one.severity]}`}>{one.label}</span>
          <span style={{ flex: 1, minWidth: 0 }}>
            {one.message}
            {one.refs.length ? (
              <span className="faint">
                {'  [근거 '}{one.refs.map((id) => numbering.get(id)).join('·')}{']'}
              </span>
            ) : null}
          </span>
        </li>
      ))}
    </ul>
  )
}

function References({ references, numbering }: {
  references: AuditReference[]
  numbering: Map<string, number>
}) {
  if (!references.length) return null
  const ordered = [...references].sort(
    (a, b) => (numbering.get(a.id) ?? 0) - (numbering.get(b.id) ?? 0))
  return (
    <details className="tiny">
      <summary className="faint">근거 {ordered.length}</summary>
      <ol style={{ margin: '6px 0 0', paddingLeft: 18 }}>
        {ordered.map((one) => (
          <li key={one.id} value={numbering.get(one.id)} style={{ marginBottom: 4 }}>
            <span className="dim">{one.citation}</span> — {one.claim_ko}
          </li>
        ))}
      </ol>
    </details>
  )
}

/** 논문 기록의 번호 — 화면에 나오는 판정 순서대로, 한 번씩 (보고서와 같은 규칙). */
function referenceNumbers(data: SpectrumAuditDetail | null): Map<string, number> {
  const numbering = new Map<string, number>()
  const findings = data?.audit?.findings ?? []
  const shown = [
    ...findings.filter((one) => one.scope === 'points'),
    ...findings.filter((one) => one.scope !== 'points'),
  ]
  for (const one of shown) {
    for (const id of one.refs) {
      if (!numbering.has(id)) numbering.set(id, numbering.size + 1)
    }
  }
  return numbering
}

/** 잔차 그림의 곡선 — KK(점 자체), 쓰는 맞춤, 어긋남의 선.
 *
 *  색은 나이퀴스트와 같은 자리다: 측정 쪽이 0 번, 맞춤이 1 번.  선은 곡선이
 *  아니라 기준이라 회색 점선이다. */
export function residualSeries(data: SpectrumAuditDetail | null): PlotSeries[] {
  const residuals = data?.residuals
  if (!residuals?.frequency_hz?.length) return []
  const x = residuals.frequency_hz.map((value) => Math.log10(value))
  const out: PlotSeries[] = [{
    label: 'KK — 점 자체',
    x,
    y: residuals.kk.map((value) => value * 100),
    color: seriesColor(0),
    points: true,
    width: 1,
  }]
  if (residuals.fit?.length) {
    out.push({
      label: `맞춤 — ${data?.audit.circuit || '쓰는 맞춤'}`,
      x: residuals.fit_frequency_hz.map((value) => Math.log10(value)),
      y: residuals.fit.map((value) => value * 100),
      color: seriesColor(1),
      points: true,
      width: 1,
    })
  }
  if (residuals.limit !== null && residuals.limit !== undefined) {
    const low = Math.min(...x)
    const high = Math.max(...x)
    out.push({
      label: `어긋남의 선 (${pct(residuals.limit)})`,
      x: [low, high],
      y: [residuals.limit * 100, residuals.limit * 100],
      color: 'var(--ink-3, #8a8f98)',
      dash: [6, 4],
      width: 1,
    })
  }
  return out
}
