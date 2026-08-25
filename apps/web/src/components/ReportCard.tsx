/** The headline answer for one cell.
 *
 * Running or finished; the discharge capacity of the last cycle that actually
 * finished; retention against the reference cycle; that cycle's coulombic
 * efficiency; and where the fade knee is.
 */

import { basisUnit, cycleNumber, num, pct } from '../lib/format'
import { ko } from '../lib/i18n'
import type { Report } from '../lib/types'
import { Alert, CapacityMetric, Metric, MetricBand, StateBadge } from './ui'

export function ReportCard({ report }: { report: Report }) {
  const { reported, reference, knee } = report
  const running = report.state === 'running'
  const threshold = knee?.results.find((r) => r.method === 'threshold')

  return (
    <div>
      <div className="toolbar">
        <StateBadge
          state={report.state}
          confidence={report.state_confidence}
          cycle={report.in_progress_cycle}
        />
        <span className="badge plain">
          {report.planned_cycles
            ? `${report.cycles_complete} / ${report.planned_cycles} 사이클`
            : `${report.cycles_complete} 사이클 완료`}
        </span>
        {report.state_confidence === 'low' ? (
          <span className="badge warn" title="근거가 서로 엇갈립니다">
            근거 약함
          </span>
        ) : null}
        <span className="spacer" />
        {/* A count, not a control: the evidence list itself expands from the
            <details> at the bottom of the card.  This used to be a second
            <details> with the same label and an empty body, so it looked
            clickable and opened onto nothing. */}
        <span className="badge plain">판정 근거 {report.evidence.length}건</span>
      </div>

      {/* 완료된 사이클이 하나도 없을 때, **왜** 없는지.
       *
       * 이 줄이 없던 동안 화면은 지표가 전부 — 이고 아무 설명이 없었다.
       * 실측(260630_MJ1, 41,738행)에서 그것은 파싱 실패로 읽혔다 — 파일은
       * 멀쩡히 읽혔고, 그 프로토콜에 방전이 없었을 뿐이다. */}
      {report.no_complete_reason ? (
        <div style={{ padding: '12px 16px 0' }}>
          <Alert kind={report.no_complete_reason === 'truncated' ? 'info' : 'warn'}>
            {ko.noCompleteReason(report.no_complete_reason)}
          </Alert>
        </div>
      ) : null}

      {!report.reference_available && report.retention_note ? (
        <div style={{ padding: '12px 16px 0' }}>
          <Alert kind="warn">
            {report.reference_cycle_requested}번 사이클이 이 기록에 없어
            {reference ? ` ${reference.cycle}번` : ''} 사이클을 기준으로 계산했습니다.
          </Alert>
        </div>
      ) : null}

      <MetricBand>
        <CapacityMetric
          label={running ? '직전 완료 사이클 방전용량' : '마지막 사이클 방전용량'}
          value={reported?.discharge_capacity}
          basis={report.basis}
          accent
          note={
            reported
              ? running
                ? `${reported.cycle}번 — ${report.in_progress_cycle}번이 진행 중이라 그 직전 값`
                : `${reported.cycle}번 사이클`
              : report.no_complete_reason === 'no_discharge'
                ? '방전이 없어 사이클 용량이 없습니다'
                : '완료된 사이클이 아직 없습니다'
          }
        />
        <Metric
          label="용량 유지율"
          value={pct(report.retention_pct, 1)}
          unit="%"
          note={report.retention_note ? ko.retentionNote(report.retention_note) : undefined}
          muted={report.retention_pct === null}
        />
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
        <Metric
          label="용량 급감 시작"
          value={
            knee?.primary.detected
              ? knee.primary.onset_cycle != null
                ? `${cycleNumber(knee.primary.onset_cycle)}→${cycleNumber(knee.primary.cycle)}`
                : cycleNumber(knee.primary.cycle)
              : knee?.primary.status === 'insufficient'
                ? `${cycleNumber(knee.primary.candidate_cycle)}?`
                : knee?.primary.status === 'indeterminate'
                  ? '판정 불가'
                  : '검출 안 됨'
          }
          unit={knee?.primary.detected ? '번째' : undefined}
          note={knee ? ko.kneeReason(knee.primary.reason) : undefined}
          muted={!knee?.primary.detected}
        />
      </MetricBand>

      <MetricBand>
        <CapacityMetric
          label={`기준 ${reference?.cycle ?? '—'}번 방전용량`}
          value={reference?.discharge_capacity}
          basis={report.basis}
          note={
            reference
              ? `${num(reference.discharge_capacity_mah)} mAh · 이 값이 유지율 분모`
              : undefined
          }
        />
        <Metric
          label="열화율 초기 → 최근"
          value={
            knee?.fade_rate_early_pct_per_cycle != null
              ? `${num(knee.fade_rate_early_pct_per_cycle, 3)} → ${num(
                  knee.fade_rate_late_pct_per_cycle,
                  3,
                )}`
              : '—'
          }
          unit="%/cyc"
          note={knee ? `${knee.search_start_cycle}번 사이클부터 계산` : undefined}
          muted={knee?.fade_rate_early_pct_per_cycle == null}
        />
        <Metric
          label="80% 도달"
          value={
            knee?.projected_cycle_at_80pct
              ? cycleNumber(Math.round(knee.projected_cycle_at_80pct))
              : threshold?.detected
                ? cycleNumber(threshold.cycle)
                : '—'
          }
          unit="번째"
          note={
            knee?.projected_cycle_at_80pct
              ? '최근 열화율 선형 외삽 — 참고용'
              : threshold?.detected
                ? '실측 통과 지점'
                : '아직 80% 위'
          }
          muted
        />
        <Metric
          label="평균 방전전압"
          value={num(reported?.mean_discharge_voltage, 4)}
          unit="V"
          note={
            reference?.mean_discharge_voltage && reported?.mean_discharge_voltage
              ? `기준 대비 ${num(
                  reported.mean_discharge_voltage - reference.mean_discharge_voltage,
                  3,
                )} V`
              : '에너지 가중 평균 (E/Q)'
          }
          muted={!reported?.mean_discharge_voltage}
        />
      </MetricBand>

      <details style={{ padding: '10px 16px 12px' }}>
        <summary>상태 판정 근거 · {summarize(report)}</summary>
        <ul className="evidence" style={{ marginTop: 6 }}>
          {report.evidence.map((item, index) => (
            <li key={index}>
              <span className="tag">{ko.signal(item.signal)}</span>
              <span>
                {ko.evidence(item.detail)}
                <span className="arrow"> → {ko.stateTarget(item.points_to)}</span>
              </span>
            </li>
          ))}
        </ul>
      </details>
    </div>
  )
}

/** The Korean one-liner, composed from the structured fields.
 *
 * The API's own `state_summary` is assembled in English for logs and the CLI;
 * rebuilding it here from the parts is more reliable than translating a
 * compound sentence, and stays correct as new fields appear. */
function summarize(report: Report): string {
  const parts: string[] = []
  if (report.state === 'running') {
    parts.push(
      report.in_progress_cycle
        ? `구동 중 · ${report.in_progress_cycle}번 사이클 진행`
        : '구동 중',
    )
  } else if (report.state === 'finished') {
    parts.push(
      report.in_progress_cycle
        ? `구동 중 아님 · 기록이 ${report.in_progress_cycle}번 사이클 도중에 끝남 (완료 ${report.cycles_complete})`
        : `${report.cycles_complete} 사이클 후 종료`,
    )
  } else {
    parts.push(`${report.cycles_complete} 사이클 기록 · 상태 불명`)
  }
  if (report.reported) {
    parts.push(`${report.reported.cycle}번 방전 ${num(report.reported.discharge_capacity_mah)} mAh`)
  }
  if (report.retention_pct !== null) parts.push(`유지율 ${pct(report.retention_pct, 1)}%`)
  if (report.reference?.coulombic_efficiency) {
    parts.push(`${report.reference.cycle}번 CE ${pct(report.reference.coulombic_efficiency)}%`)
  }
  if (report.knee?.primary.detected && report.knee.primary.cycle !== null) {
    const onset = report.knee.primary.onset_cycle
    parts.push(
      onset != null
        ? `급감 ${Math.round(onset)}→${Math.round(report.knee.primary.cycle)}번`
        : `급감 ${Math.round(report.knee.primary.cycle)}번`,
    )
  }
  return parts.join(' · ')
}


/** 사퇴한 기준이 **무엇을 재고** 그렇게 판단했는가.
 *
 *  이유 한 줄은 결론이지 근거가 아니다.  "열화가 가속되지 않습니다" 를 읽은
 *  사람이 다음에 하는 일은 "얼마나 안 됐는데?" 를 묻는 것이고, 그 숫자는 이미
 *  `detail` 에 다 들어 있는데 화면이 버리고 있었다.
 *
 *  문턱값은 서버가 준다 (`knee.thresholds`).  여기 베껴 두면 서버가 문턱을 바꾼
 *  날 화면만 옛 숫자를 말한다.
 */
interface Measured {
  label: string
  value: string
  /** 필요한 쪽 값.  없으면 그냥 관측값이다 (문턱이 없는 항목). */
  need?: string
  /** 이 항목이 걸린 게이트인가 — 그 줄만 굵게. */
  failed?: boolean
}

export function kneeEvidence(
  detail: Record<string, number>,
  thresholds: Record<string, number> = {},
): Measured[] {
  const has = (key: string) => typeof detail[key] === 'number'
  const rows: Measured[] = []

  const push = (key: string, label: string, digits = 4, unit = '') => {
    if (!has(key)) return
    const value = `${num(detail[key], digits)}${unit}`
    const limit = thresholds[key]
    if (typeof limit !== 'number') {
      rows.push({ label, value })
      return
    }
    rows.push({
      label, value,
      need: `${num(limit, digits)}${unit} 이상`,
      // 문턱이 있는 항목은 미달일 때가 곧 사퇴 사유다.
      failed: (detail[key] as number) < limit,
    })
  }

  // -- 유지율 임계 (threshold) --------------------------------------------
  if (has('level')) {
    rows.push({ label: 'EOL 기준', value: `${num(detail.level, 3)} %` })
  }
  if (has('min_retention')) {
    rows.push({
      label: '기록 중 최저 유지율',
      value: `${num(detail.min_retention, 3)} %`,
      need: has('level') ? `${num(detail.level, 3)} % 미만` : undefined,
      // 한 번도 안 내려갔으면 그것이 사퇴 사유다.
      failed: has('level') && (detail.min_retention as number) >= (detail.level as number),
    })
  }
  if (has('first_cycle_below')) {
    rows.push({
      label: '처음 내려간 사이클', value: `${num(detail.first_cycle_below, 0)}번`,
    })
  }

  // -- 초기 대비 열화율 배수 (slope_ratio) ---------------------------------
  if (has('baseline_slope')) {
    rows.push({
      label: `초기 기울기 (${has('baseline_window')
        ? `${num(detail.baseline_window, 0)}사이클` : '초기'})`,
      value: `${num(detail.baseline_slope, 4)} %/cycle`,
    })
  }
  if (has('factor')) {
    rows.push({ label: '요구 배수', value: `${num(detail.factor, 2)}배` })
  }
  if (has('steepest_slope')) {
    rows.push({
      label: '가장 가팔랐던 구간',
      value: `${num(detail.steepest_slope, 4)} %/cycle`,
      need: has('slope_limit')
        ? `${num(detail.slope_limit, 4)} %/cycle 이하` : undefined,
      // 기울기는 음수라 "이하" 여야 통과다 -- 부등호가 다른 항목들과 반대다.
      failed: has('slope_limit')
        && (detail.steepest_slope as number) > (detail.slope_limit as number),
    })
  } else if (has('slope_limit')) {
    rows.push({ label: '넘어야 할 기울기', value: `${num(detail.slope_limit, 4)} %/cycle` })
  }
  if (has('slope_at_knee')) {
    rows.push({ label: '그 자리 기울기', value: `${num(detail.slope_at_knee, 4)} %/cycle` })
  }

  // -- 최대 곡률 -----------------------------------------------------------
  if (has('curvature')) {
    rows.push({ label: '최대 곡률', value: num(detail.curvature, 3) })
  }
  if (has('median_curvature')) {
    rows.push({ label: '곡률 중앙값', value: num(detail.median_curvature, 3) })
  }

  if (has('knee_onset')) {
    rows.push({ label: '이탈 시작(onset)', value: `${num(detail.knee_onset, 0)}번` })
  }
  if (has('breakpoint')) {
    rows.push({ label: '전환 지점', value: `${num(detail.breakpoint, 0)}번` })
  }
  if (has('second_transition')) {
    rows.push({ label: '두 번째 전환', value: `${num(detail.second_transition, 0)}번` })
  }
  push('slope_before', '앞 기울기', 4, ' %/cycle')
  push('slope_after', '뒤 기울기', 4, ' %/cycle')
  if (has('slope_late')) push('slope_late', '그 뒤 기울기', 4, ' %/cycle')
  push('slope_ratio', '가속 배수', 2, '배')
  push('drop_after_pct', '그 뒤 손실', 2, ' %p')
  push('fit_gain_score', '적합 이득', 1)
  if (has('separation_cycles')) {
    rows.push({
      label: '두 전환 사이', value: `${num(detail.separation_cycles, 0)} 사이클`,
    })
  }
  return rows
}

const METHOD_LABELS: Record<string, string> = {
  dbw: 'Double Bacon-Watts',
  segmented: '두 직선 교점',
  slope_ratio: '초기 대비 열화율 배수',
  threshold: '유지율 임계 통과',
  curvature: '최대 곡률',
  none: '—',
}

const METHOD_HINTS: Record<string, string> = {
  dbw: '이탈 시작(onset)과 급감 정착(point)을 한 적합으로 (ADR 0021)',
  segmented: '두 직선으로 볼 때 꺾이는 지점',
  slope_ratio: '열화율이 초기의 k배가 된 시점',
  threshold: 'EOL(기본 80%)을 넘은 시점',
  curvature: '곡선이 가장 심하게 휘는 지점',
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
      <div className="tiny faint">
        기준이 하나가 아닙니다. 전부 계산해서 보여 주고, 열화가 실제로 가속될 때만 knee
        로 인정합니다. 행을 누르면 그래프의 세로선이 바뀝니다.
        {' '}<b>마우스를 올려 두면 그 기준의 상세 내용(숫자와 문턱값)이 나옵니다.</b>
      </div>
      <div className="knee-choices">
        {knee.results.map((result) => {
          const on = selected === result.method
          const evidence = kneeEvidence(result.detail, knee.thresholds ?? {})
          return (
            <button
              key={result.method}
              type="button"
              className={`choice${on ? ' on' : ''}`}
              onClick={() => onSelect(result.method)}
            >
              <span className="head">
                <strong>{METHOD_LABELS[result.method] ?? result.method}</strong>
                {knee.primary.method === result.method && result.detected ? (
                  <span className="badge plain">기본</span>
                ) : null}
                <span className={`cycle${result.status === 'insufficient' ? ' tentative' : ''}`}>
                  {/* 확정이 아니어도 짚은 사이클은 보여 준다.  '—' 하나로
                      "안 꺾였다" 와 "아직 확인할 데이터가 없다" 를 같이
                      쓰면, 일찍 뽑은 셀이 안 꺾인 셀과 똑같아 보인다. */}
                  {result.detected
                    ? result.onset_cycle != null
                      ? `${cycleNumber(result.onset_cycle)}→${cycleNumber(result.cycle)}번`
                      : `${cycleNumber(result.cycle)}번`
                    : result.status === 'insufficient' && result.candidate_cycle !== null
                      ? `${cycleNumber(result.candidate_cycle)}번?`
                      : result.status === 'indeterminate'
                        ? '판정 불가'
                        : '—'}
                </span>
              </span>
              <span className="why">{METHOD_HINTS[result.method]}</span>
              <span className="why">{ko.kneeReason(result.reason)}</span>
              {/* 올려놓으면 근거가 나온다.  이유 한 줄은 결론이고, 사람이
                  다음에 묻는 것은 "얼마나?" 다 — 그 숫자는 이미 있는데 화면이
                  버리고 있었다.  걸린 게이트만 굵게. */}
              {evidence.length ? (
                <span className="knee-evidence" role="note">
                  <span className="tiny faint">{ko.kneeReason(result.reason)}</span>
                  <table>
                    <tbody>
                      {evidence.map((row) => (
                        <tr key={row.label} className={row.failed ? 'failed' : ''}>
                          <th>{row.label}</th>
                          <td>{row.value}</td>
                          <td className="dim">{row.need ? `필요: ${row.need}` : ''}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </span>
              ) : null}
            </button>
          )
        })}
      </div>
      <div className="tiny faint">
        기준 사이클 {knee.reference_cycle}번 ({num(knee.reference_capacity_mah)} mAh
        {report.basis !== 'mAh' ? ` · 표시는 ${basisUnit(report.basis)}` : ''}) · 탐색 시작{' '}
        {knee.search_start_cycle}번 · 표본 {knee.n_points} 사이클
      </div>
    </div>
  )
}
