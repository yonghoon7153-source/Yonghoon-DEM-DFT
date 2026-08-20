/** The headline answer for one cell.
 *
 * Running or finished; the discharge capacity of the last cycle that actually
 * finished; retention against the reference cycle; that cycle's coulombic
 * efficiency; and where the fade knee is.
 */

import { basisUnit, cycleNumber, num, pct } from '../lib/format'
import type { Report } from '../lib/types'
import { Alert, CapacityMetric, Metric, StateBadge } from './ui'

export function ReportCard({ report }: { report: Report }) {
  const { reported, reference, knee } = report
  const running = report.state === 'running'

  return (
    <div className="col" style={{ gap: 12 }}>
      <div className="row" style={{ gap: 10 }}>
        <StateBadge
          state={report.state}
          confidence={report.state_confidence}
          cycle={report.in_progress_cycle}
        />
        {report.planned_cycles ? (
          <span className="badge plain">
            {report.cycles_complete} / {report.planned_cycles} 사이클
          </span>
        ) : (
          <span className="badge plain">{report.cycles_complete} 사이클 완료</span>
        )}
        {report.state_confidence === 'low' ? (
          <span className="badge warn">근거 약함</span>
        ) : null}
      </div>

      {!report.reference_available && report.retention_note ? (
        <Alert kind="warn">
          {report.reference_cycle_requested}번 사이클이 이 기록에 없어
          {reference ? ` ${reference.cycle}번` : ''} 사이클을 기준으로 계산했습니다.
        </Alert>
      ) : null}

      <div className="grid cols-4" style={{ gap: 1, background: 'var(--border)' }}>
        <div style={{ background: 'var(--surface)' }}>
          <CapacityMetric
            label={running ? '직전 완료 사이클 방전용량' : '마지막 사이클 방전용량'}
            value={reported?.discharge_capacity}
            basis={report.basis}
            note={
              reported
                ? running
                  ? `${reported.cycle}번 사이클 — ${report.in_progress_cycle}번이 진행 중이라 그 직전 값`
                  : `${reported.cycle}번 사이클`
                : '완료된 사이클이 아직 없습니다'
            }
          />
        </div>
        <div style={{ background: 'var(--surface)' }}>
          <Metric
            label="용량 유지율"
            value={pct(report.retention_pct, 1)}
            unit="%"
            note={report.retention_note || undefined}
            muted={report.retention_pct === null}
          />
        </div>
        <div style={{ background: 'var(--surface)' }}>
          <Metric
            label={`${reference?.cycle ?? report.reference_cycle_requested}번 사이클 쿨롱효율`}
            value={pct(reference?.coulombic_efficiency ?? null)}
            unit="%"
            note={
              report.first_cycle
                ? `1번 사이클은 ${pct(report.first_cycle.coulombic_efficiency, 2)}% (formation)`
                : undefined
            }
            muted={!reference?.coulombic_efficiency}
          />
        </div>
        <div style={{ background: 'var(--surface)' }}>
          <Metric
            label="용량 급감 시작"
            value={
              knee?.primary.detected ? cycleNumber(knee.primary.cycle) : '검출 안 됨'
            }
            unit={knee?.primary.detected ? '번째' : undefined}
            note={knee?.primary.reason}
            muted={!knee?.primary.detected}
          />
        </div>
      </div>

      <div className="grid cols-3" style={{ gap: 1, background: 'var(--border)' }}>
        <div style={{ background: 'var(--surface)' }}>
          <CapacityMetric
            label={`기준 ${reference?.cycle ?? '—'}번 방전용량`}
            value={reference?.discharge_capacity}
            basis={report.basis}
          />
        </div>
        <div style={{ background: 'var(--surface)' }}>
          <Metric
            label="열화율 (초기 → 최근)"
            value={
              knee?.fade_rate_early_pct_per_cycle !== null &&
              knee?.fade_rate_early_pct_per_cycle !== undefined
                ? `${num(knee.fade_rate_early_pct_per_cycle, 3)} → ${num(
                    knee.fade_rate_late_pct_per_cycle,
                    3,
                  )}`
                : '—'
            }
            unit="%/cyc"
            note={knee ? `${knee.search_start_cycle}번 사이클부터 계산` : undefined}
            muted={!knee?.fade_rate_early_pct_per_cycle}
          />
        </div>
        <div style={{ background: 'var(--surface)' }}>
          <Metric
            label="80% 도달 예상"
            value={
              knee?.projected_cycle_at_80pct
                ? cycleNumber(Math.round(knee.projected_cycle_at_80pct))
                : knee?.results.find((r) => r.method === 'threshold')?.detected
                  ? cycleNumber(knee.results.find((r) => r.method === 'threshold')!.cycle)
                  : '—'
            }
            unit="번째"
            note={
              knee?.projected_cycle_at_80pct
                ? '최근 열화율 선형 외삽 — 참고용'
                : knee?.results.find((r) => r.method === 'threshold')?.detected
                  ? '실측 통과 지점'
                  : '아직 80% 위'
            }
            muted
          />
        </div>
      </div>

      <details>
        <summary className="small dim" style={{ cursor: 'pointer' }}>
          상태 판정 근거 {report.evidence.length}건 · {report.state_summary}
        </summary>
        <ul className="evidence" style={{ marginTop: 8 }}>
          {report.evidence.map((item, index) => (
            <li key={index}>
              <span className="tag">{item.signal}</span>
              <span>
                {item.detail}
                <span className="faint"> → {item.points_to}</span>
              </span>
            </li>
          ))}
        </ul>
      </details>
    </div>
  )
}

const METHOD_LABELS: Record<string, string> = {
  segmented: '두 직선 교점 (segmented)',
  slope_ratio: '초기 대비 열화율 배수',
  threshold: '유지율 임계 통과',
  curvature: '최대 곡률',
  none: '—',
}

export function KneeDetail({
  report,
  selected,
  onSelect,
}: {
  report: Report
  selected: string
  onSelect: (method: string) => void
}) {
  const knee = report.knee
  if (!knee) return null
  return (
    <div className="col" style={{ gap: 8 }}>
      <div className="tiny dim">
        기준이 하나가 아닙니다. 넷 다 계산해서 보여 주고, 열화가 실제로 가속될 때만
        knee 로 인정합니다. 그래프의 세로선은 선택한 기준입니다.
      </div>
      <table>
        <thead>
          <tr>
            <th>기준</th>
            <th>사이클</th>
            <th style={{ textAlign: 'left' }}>판정</th>
          </tr>
        </thead>
        <tbody>
          {knee.results.map((result) => (
            <tr
              key={result.method}
              className={`clickable${selected === result.method ? ' selected' : ''}`}
              onClick={() => onSelect(result.method)}
            >
              <td className="text">
                {METHOD_LABELS[result.method] ?? result.method}
                {knee.primary.method === result.method && result.detected ? (
                  <span className="badge plain" style={{ marginLeft: 6 }}>
                    기본
                  </span>
                ) : null}
              </td>
              <td>{result.detected ? cycleNumber(result.cycle) : '—'}</td>
              <td className="text small dim">{result.reason}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="tiny faint">
        기준 사이클 {knee.reference_cycle}번 ({num(knee.reference_capacity_mah)} mAh
        {report.basis !== 'mAh' ? ` · 표시는 ${basisUnit(report.basis)}` : ''}) ·
        탐색 시작 {knee.search_start_cycle}번 · 표본 {knee.n_points} 사이클
      </div>
    </div>
  )
}
