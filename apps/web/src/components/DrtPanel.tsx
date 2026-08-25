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

import { CopyBar } from './CopyBar'
import { Plot, type PlotSeries } from './Plot'
import { Alert, Card, KeyValues, Spinner } from './ui'
import { api } from '../lib/api'
import { num, seriesColor } from '../lib/format'
import { drtTsv } from '../lib/origin'
import { useAsync } from '../lib/hooks'
import type { Drt } from '../lib/types'

/** 그 시간대에 무엇이 사는가 — **관례적인 구간**이고 판정이 아니다.
 *
 *  DRT 는 τ 를 주지 이름을 주지 않는다.  이름은 문헌의 관례이고, 같은 τ 라도
 *  셀 구성에 따라 다른 것이 앉는다 (전고체 대칭셀의 저주파 아크는 계면이지만
 *  풀셀에서는 확산이다 — ADR 0019 가 아크 이름에서 이미 다룬 구분이다).
 *  그래서 문장이 "…대" 로 끝나고 단정하지 않는다.
 */
export function tauBand(logTau: number): string {
  const tau = 10 ** logTau
  const hz = 1 / (2 * Math.PI * tau)
  const where = hz >= 1000 ? `${(hz / 1000).toFixed(1)} kHz`
    : hz >= 1 ? `${hz.toFixed(1)} Hz` : `${(hz * 1000).toFixed(1)} mHz`
  const what = tau < 1e-5 ? '벌크 이온전도 · 배선 인덕턴스가 섞이는 대'
    : tau < 1e-3 ? '입계 · 계면 필름(SEI/CEI) 대'
      : tau < 1e-1 ? '전하이동 대'
        : tau < 10 ? '복합전극 전송선 · 고체 내 확산 대'
          : '아주 느린 확산 · 상변태 대 (측정 대역 끝)'
  return `≈ ${where} · ${what}`
}

const LAMBDA_NOTE =
  'λ 는 "얼마나 매끄럽게 볼까" 입니다. 키우면 봉우리가 넓어지고 서로 합쳐지며 ' +
  '**전체 분극이 줄어듭니다** — 과하게 매끄러우면 실제 분극을 깎습니다. 줄이면 ' +
  '데이터에 더 붙는 대신 잡음이 봉우리로 올라옵니다. 슬라이더를 움직이며 아래 ' +
  'χ² 와 전체 분극이 함께 어떻게 움직이는지 보는 것이 고르는 방법입니다.'

const ORDER_NOTE =
  '평활 차수는 **무엇을** 매끄럽게 볼지입니다. 0 = 값 자체를 작게 (봉우리가 ' +
  '낮아집니다), 1 = 기울기를 (기본), 2 = 곡률을 (넓지만 어깨가 살아남습니다).'

const WIDTH_NOTE =
  '봉우리가 넓은 데는 이유가 셋이고 셋 다 정상일 수 있습니다. ① DRT 자체의 ' +
  '해상도 한계 — 이상적인 R‖C 하나도 λ=1e-5 에서 0.5 decade 로 나옵니다. ' +
  '② CPE 지수 n<1 은 진짜로 넓습니다 (합성 스펙트럼에서 n=0.8 이면 1.3, ' +
  'n=0.6 이면 1.9 decade). ③ 복합전극의 전송선은 이완 시간이 하나가 아니라 ' +
  '**띠**입니다 — 봉우리가 아니라 넓은 언덕이 정상입니다 (ADR 0028).'

export function DrtPanel({ spectrumId }: { spectrumId: number }) {
  const [order, setOrder] = useState(1)
  const [index, setIndex] = useState<number | null>(null)
  const sweep = useAsync(
    () => api.spectrumDrtSweep(spectrumId, { derivative_order: order }),
    [spectrumId, order],
  )

  const results = useMemo(() => sweep.data?.results ?? [], [sweep.data])
  // 응답이 **지금 누른 차수의 것**인지.  useAsync 는 새 요청이 도는 동안 옛
  // 값을 유지하는데(다른 화면에서는 그게 맞다), 여기서는 차수 2 버튼 아래
  // 차수 1 의 γ 가 그려지고 복사까지 됐다 (리뷰 #19).  더 나쁜 것: 차수를
  // 바꾸면 index 를 비우는데, 옛 응답이 남아 있어 선택 효과가 옛 추천으로
  // 도로 채웠고 — 새 응답이 와도 index !== null 이라 새 추천을 안 탔다.
  // 결과마다 실려 오는 derivative_order 가 신선도의 증명이다.
  const fresh = sweep.data !== null &&
    (results.length === 0 || results[0]!.derivative_order === order)

  // 모서리가 있으면 거기서 시작한다.  없으면 가운데 — 어느 쪽 실패 모드에도
  // 붙어 있지 않은 자리다.  둘 다 이유를 화면이 말한다.
  useEffect(() => {
    if (!sweep.data || !fresh || index !== null) return
    // 응답이 비어 있을 수 있다 (풀지 못한 스펙트럼).  거기서 `.length` 를
    // 읽으면 화면 전체가 죽는데, 죽은 화면은 "DRT 를 못 풀었다" 보다 훨씬
    // 나쁜 소식이다 — 나이퀴스트도 파라미터도 함께 사라진다.
    if (!results.length) return
    const suggested = sweep.data.suggested_index ?? -1
    setIndex(suggested >= 0 ? suggested : Math.floor(results.length / 2))
  }, [sweep.data, fresh, results, index])

  useEffect(() => {
    setIndex(null)
  }, [spectrumId, order])

  const shown: Drt | null =
    !fresh || index === null ? null : (results[index] ?? null)

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
        {sweep.data && fresh && !results.length ? (
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
          <span className="tiny faint" title={ORDER_NOTE}>평활 차수 ⓘ</span>
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
            <span className="tiny faint" style={{ minWidth: 74 }} title={LAMBDA_NOTE}>
              벌점 λ ⓘ
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

        {/* 설정이 무엇을 하는지 화면에 적어 둔다.  λ 를 옮기면 봉우리 폭과
            전체 분극이 함께 움직이는데, 그 사실을 모르면 슬라이더를 "더 예쁜
            그림" 쪽으로 밀고 그 분극을 그대로 보고하게 된다. */}
        <div className="tiny faint">{LAMBDA_NOTE}</div>

        <Plot
          series={series}
          xLabel="log₁₀ τ (s)"
          yLabel="γ (Ω)"
          height={280}
          legend
          describeX={tauBand}
        />

        <details className="tiny faint">
          <summary>봉우리가 넓은데 왜인가요?</summary>
          <div style={{ marginTop: 6 }}>{WIDTH_NOTE}</div>
        </details>

        <CopyBar
          items={[{
            label: 'γ(τ)',
            // τ 를 그대로 낸다 -- 로그로 내보내면 워크시트에서 되돌릴 수 없다.
            title: 'τ 와 γ 두 열 · 지금 보고 있는 λ 의 것',
            build: () => drtTsv(shown),
          }]}
        />

        <KeyValues
          cols={2}
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
