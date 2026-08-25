/** DRT — 스펙트럼에게 "몇 개냐" 를 묻는 화면.
 *
 *  등가회로는 아크가 몇 개인지를 회로를 그린 사람이 미리 정한다.  여기서는
 *  정하지 않는다.  대신 **λ 가 답을 정하므로**, 값 하나를 조용히 고르는 대신
 *  훑어 놓고 L 곡선 모서리를 이유와 함께 짚는다 (ADR 0005 와 같은 태도).
 *
 *  양 끝의 실패 모드가 함께 보여야 가운데가 선택으로 읽힌다: 작은 λ 는 잡음
 *  봉우리의 숲, 큰 λ 는 하나로 뭉친 덩어리.  그래서 슬라이더는 훑어 놓은
 *  결과들 사이를 옮겨 다니고, 매번 서버를 다시 부르지 않는다.
 */

import { useEffect, useMemo, useState } from 'react'

import { Plot, type PlotSeries } from './Plot'
import { Alert, Card, KeyValues, Spinner } from './ui'
import { api } from '../lib/api'
import { num, seriesColor } from '../lib/format'
import { useAsync } from '../lib/hooks'
import type { Drt } from '../lib/types'

export function DrtPanel({ spectrumId }: { spectrumId: number }) {
  const [order, setOrder] = useState(1)
  const [index, setIndex] = useState<number | null>(null)
  const sweep = useAsync(
    () => api.spectrumDrtSweep(spectrumId, { derivative_order: order }),
    [spectrumId, order],
  )

  // 모서리가 있으면 거기서 시작한다.  없으면 가운데 — 어느 쪽 실패 모드에도
  // 붙어 있지 않은 자리다.  둘 다 이유를 화면이 말한다.
  useEffect(() => {
    if (!sweep.data || index !== null) return
    // 응답이 비어 있을 수 있다 (풀지 못한 스펙트럼).  거기서 `.length` 를
    // 읽으면 화면 전체가 죽는데, 죽은 화면은 "DRT 를 못 풀었다" 보다 훨씬
    // 나쁜 소식이다 — 나이퀴스트도 파라미터도 함께 사라진다.
    const available = sweep.data.results ?? []
    if (!available.length) return
    const suggested = sweep.data.suggested_index ?? -1
    setIndex(suggested >= 0 ? suggested : Math.floor(available.length / 2))
  }, [sweep.data, index])

  useEffect(() => {
    setIndex(null)
  }, [spectrumId, order])

  const results = sweep.data?.results ?? []
  const shown: Drt | null = index === null ? null : (results[index] ?? null)

  const series = useMemo<PlotSeries[]>(() => {
    if (!shown) return []
    return [{
      label: `γ(τ) · λ=${format(shown.regularisation)}`,
      // 가로축은 로그 τ 다.  τ 자체를 쓰면 여섯 자리가 한 점에 뭉친다.
      x: shown.tau_s.map((value) => Math.log10(value)),
      y: shown.gamma_ohm,
      color: seriesColor(0),
      width: 2,
    }]
  }, [shown])

  if (sweep.error) {
    return (
      <Card title="DRT (이완 시간 분포)">
        <Alert kind="error">{sweep.error}</Alert>
      </Card>
    )
  }
  if (!shown) {
    return (
      <Card title="DRT (이완 시간 분포)">
        {sweep.data && !results.length ? (
          <Alert kind="info">
            이 스펙트럼으로는 DRT 를 풀지 못했습니다
            {sweep.data.suggested_reason ? ` — ${sweep.data.suggested_reason}` : ''}
          </Alert>
        ) : (
          <Spinner label="λ 를 훑는 중" />
        )}
      </Card>
    )
  }

  const suggested = sweep.data?.suggested_index ?? -1

  return (
    <Card
      title="DRT (이완 시간 분포)"
      actions={
        <div className="row" style={{ gap: 6 }}>
          <span className="tiny faint">평활 차수</span>
          <div className="segmented">
            {[0, 1, 2].map((value) => (
              <button
                key={value}
                type="button"
                className={order === value ? 'on' : ''}
                onClick={() => setOrder(value)}
              >
                {value}
              </button>
            ))}
          </div>
        </div>
      }
    >
      <div className="col" style={{ gap: 10 }}>
        <div className="col" style={{ gap: 4 }}>
          <label className="row" style={{ gap: 8 }}>
            <span className="tiny faint" style={{ minWidth: 74 }}>
              벌점 λ
            </span>
            <input
              type="range"
              aria-label="벌점 λ"
              min={0}
              max={Math.max(results.length - 1, 0)}
              step={1}
              value={index ?? 0}
              onChange={(event) => setIndex(Number(event.target.value))}
              style={{ flex: 1 }}
            />
            <span className="mono tiny" style={{ minWidth: 66, textAlign: 'right' }}>
              {format(shown.regularisation)}
            </span>
          </label>
          {suggested >= 0 ? (
            <div className="tiny faint">
              {sweep.data?.suggested_reason}
              {index !== suggested ? (
                <button
                  type="button"
                  className="ghost tiny"
                  onClick={() => setIndex(suggested)}
                >
                  거기로
                </button>
              ) : null}
            </div>
          ) : (
            // 모서리를 못 찾았으면 하나를 골라 주지 않는다 (§0.4).
            <Alert kind="info">{sweep.data?.suggested_reason}</Alert>
          )}
        </div>

        <Plot
          series={series}
          xLabel="log₁₀ τ (s)"
          yLabel="γ (Ω)"
          height={280}
          legend
        />

        <KeyValues
          rows={[
            ['R∞', `${num(shown.r_inf_ohm, 4)} Ω`],
            ['전체 분극', `${num(shown.total_polarisation_ohm, 4)} Ω`],
            ['χ²', num(shown.chi_squared, 4)],
            ['봉우리', `${shown.peaks.length}개`],
            ...(shown.dropped_inductive
              ? [['뺀 점', `유도성 ${shown.dropped_inductive}개`] as [string, string]]
              : []),
          ]}
        />

        {shown.peaks.length ? (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>주파수</th>
                  <th>τ</th>
                  <th>저항</th>
                  <th>γ 최대</th>
                </tr>
              </thead>
              <tbody>
                {shown.peaks.map((peak) => (
                  <tr key={peak.tau_s}>
                    <td>{format(peak.frequency_hz)} Hz</td>
                    <td>{format(peak.tau_s)} s</td>
                    {/* 봉우리 아래 넓이 — DRT 를 그림이 아니라 수로 만드는 것. */}
                    <td>{num(peak.resistance_ohm, 4)} Ω</td>
                    <td className="dim">{num(peak.gamma_ohm, 3)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="tiny faint">이 λ 에서는 봉우리가 없습니다.</div>
        )}
      </div>
    </Card>
  )
}

/** 여섯 자리를 오가는 값이라 고정 소수점으로는 못 읽는다. */
function format(value: number): string {
  if (!Number.isFinite(value)) return '—'
  if (value === 0) return '0'
  const magnitude = Math.abs(value)
  if (magnitude >= 1e4 || magnitude < 1e-2) return value.toExponential(2)
  return String(Number(value.toPrecision(3)))
}
