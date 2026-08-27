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
import { perArea } from '../lib/areanorm'
import { drtTsv } from '../lib/origin'
import { nearestLambdaIndex, rememberedLambda, rememberLambda } from '../lib/drtlambda'
import { useAsync, useStickyState } from '../lib/hooks'
import {
  TAU_AXES, TAU_AXIS_KEY, type TauAxis,
  tauAxisLabel, tauAxisShort, tauAxisValue, tauFromAxis, validTauAxis,
} from '../lib/tauaxis'
import type { Drt } from '../lib/types'

/** 그 시간대에 무엇이 사는가 — **관례적인 구간**이고 판정이 아니다.
 *
 *  DRT 는 τ 를 주지 이름을 주지 않는다.  이름은 문헌의 관례이고, 같은 τ 라도
 *  셀 구성에 따라 다른 것이 앉는다 (전고체 대칭셀의 저주파 아크는 계면이지만
 *  풀셀에서는 확산이다 — ADR 0019 가 아크 이름에서 이미 다룬 구분이다).
 *  그래서 문장이 "…대" 로 끝나고 단정하지 않는다.
 */
/** 축의 값을 주파수와 그 시간대의 이름으로.
 *
 *  **어느 축인지 반드시 받는다 (기본값을 안 둔다).**  `-6` 은 `log₁₀` 에서
 *  1 µs 이고 `ln` 에서 2.5 ms 다 — 앞은 '벌크 이온전도' 대, 뒤는 '전하이동'
 *  대다.  기본값을 두면 축을 바꾼 화면이 **조용히 다른 물리를 적는다.**
 */
export function tauBand(axisValue: number, axis: TauAxis): string {
  const tau = tauFromAxis(axis, axisValue)
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
  '전체 분극이 줄어듭니다 — 과하게 매끄러우면 실제 분극을 깎습니다. 줄이면 ' +
  '데이터에 더 붙는 대신 잡음이 봉우리로 올라옵니다. 슬라이더를 움직이며 아래 ' +
  'χ² 와 전체 분극이 함께 어떻게 움직이는지 보는 것이 고르는 방법입니다.'

const ORDER_NOTE =
  '평활 차수는 무엇을 매끄럽게 볼지입니다. 0 = 값 자체를 작게 (기본 · 봉우리가 ' +
  '가장 뾰족하고, 대신 λ 를 키우면 전체 분극이 함께 깎입니다), 1 = 기울기를, ' +
  '2 = 곡률을 (넓지만 어깨가 살아남습니다). 전고체 셀에서는 1·2 가 격자 끝에 ' +
  '봉우리를 남겨 추천 λ 를 못 고르는 일이 잦아 0 을 기본으로 둡니다.'

const WIDTH_NOTE =
  '봉우리가 넓은 데는 이유가 셋이고 셋 다 정상일 수 있습니다. ① DRT 자체의 ' +
  '해상도 한계 — 이상적인 R‖C 하나도 λ=1e-5 에서 0.5 decade 로 나옵니다. ' +
  '② CPE 지수 n<1 은 진짜로 넓습니다 (합성 스펙트럼에서 n=0.8 이면 1.3, ' +
  'n=0.6 이면 1.9 decade). ③ 복합전극의 전송선은 이완 시간이 하나가 아니라 ' +
  '하나의 띠입니다 — 봉우리가 아니라 넓은 언덕이 정상입니다 (ADR 0028).'

/** 평활 차수의 기본값 — 벌점을 γ 자체에 건다 (0차 티호노프).
 *
 *  오래 1 이었다.  기울기에 벌점을 걸면 전체 분극이 λ 에 거의 흔들리지 않아
 *  안전해 보였기 때문이다.  그런데 이 실험실의 실측 파일에서는 1·2 차가
 *  **답을 아예 못 낸다**: 격자 끝(측정하지 않은 주파수)에 작은 봉우리가 남고,
 *  `lcurve_corner` 가 그것을 이유로 모든 후보를 건너뛴다.
 *
 *  전고체 .mpr 여섯 개로 센 결과 — 추천 λ 를 찾은 개수:
 *    0차 6/6 · 1차 1/6 · 2차 1/6
 *  (full 1cyc, sym, half-NE 스윕 둘, half-PE 스윕 둘)
 *
 *  0 차의 대가는 λ 를 키울수록 γ 가 통째로 작아지는 것이다.  숨기지 않고
 *  아래 "전체 분극" 옆에 벌점 없는 답과의 비를 적는다.
 */
const DEFAULT_ORDER = 0

export function DrtPanel({ spectrumId, area = null }: {
  spectrumId: number
  /** 나눌 면적 (cm²).  `null` 이면 안 나눈다 — Ω 그대로다.
   *
   *  **γ 도 저항이다.**  봉우리 아래 넓이가 곧 그 과정의 저항이라, 나이퀴스트를
   *  Ω·cm² 로 보면서 γ 만 Ω 로 두면 같은 화면의 두 그림이 다른 자로 그려진다 —
   *  R∞ 와 전체 분극은 나이퀴스트에서 읽는 수와 곧바로 견주는 값이라 더 그렇다.
   *  판정은 화면이 하고 (`lib/zunit: areaFor`) 여기는 받은 대로 곱한다. */
  area?: number | null
}) {
  const [order, setOrder] = useState(DEFAULT_ORDER)
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
    // 적어 둔 λ 가 먼저다.  L 곡선 모서리는 '거기로' 버튼에 남는다.
    setIndex(nearestLambdaIndex(results.map((r) => r.regularisation), rememberedLambda()))
  }, [sweep.data, fresh, results, index])

  useEffect(() => {
    setIndex(null)
  }, [spectrumId, order])

  // 가로축의 밑.  기본은 `ln` 이고 (DRT 의 정의가 자연로그 위의 밀도다),
  // 고른 것은 이 브라우저에 남는다 — 비교 화면과 **같은 열쇠**를 써서 두
  // 화면이 같은 축으로 그린다 (`lib/tauaxis.ts`).
  const [storedAxis, setAxis] = useStickyState<TauAxis>(TAU_AXIS_KEY, 'ln')
  const axis = validTauAxis(storedAxis)

  const shown: Drt | null =
    !fresh || index === null ? null : (results[index] ?? null)

  // 적을 단위 이름.  **수를 곱한 것과 같은 판정에서 나온다** — 이름을 따로
  // 받으면 안 나눈 수에 `Ω·cm²` 만 붙는 화면이 만들어진다.
  const zUnit = area ? 'Ω·cm²' : 'Ω'

  const series = useMemo<PlotSeries[]>(() => {
    if (!shown) return []
    return [{
      label: `γ(τ) · λ=${format(shown.regularisation)}`,
      // 가로축은 로그 τ 다.  τ 자체를 쓰면 여섯 자리가 한 점에 뭉친다.
      // 밑을 고를 수 있고 기본은 `ln` 이다 (`lib/tauaxis.ts` 에 이유).
      x: shown.tau_s.map((value) => tauAxisValue(axis, value)),
      y: shown.gamma_ohm.map((value) => perArea(value, area)),
      color: seriesColor(0),
      width: 2,
    }]
  }, [shown, axis, area])

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

  // 벌점이 γ 를 얼마나 깎았나.  0 차에서는 벌점이 γ 자체에 걸리므로 λ 를
  // 키우면 전체 분극이 통째로 작아진다 — 실측 대칭셀에서 λ=1e-2 의 44.2 Ω 가
  // 벌점이 가장 약한 답의 61.1 Ω 였다.  그 차이를 안 적으면 깎인 쪽이
  // 측정값처럼 읽힌다 (§0.4).  1·2 차에서는 이 비가 1 근처라 조용하다.
  const leastPenalised = results.reduce(
    (best, item) => (item.regularisation < best.regularisation ? item : best),
    results[0]!,
  )
  const kept = leastPenalised.total_polarisation_ohm > 0
    ? shown.total_polarisation_ohm / leastPenalised.total_polarisation_ohm
    : 1

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
              onChange={(event) => {
                const next = Number(event.target.value)
                setIndex(next)
                // 옮긴 자리가 다음에 열 때의 기본값이 된다.
                const picked = results[next]?.regularisation
                if (picked) rememberLambda(picked)
              }}
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
                  onClick={() => {
                    setIndex(suggested)
                    const picked = results[suggested]?.regularisation
                    if (picked) rememberLambda(picked)
                  }}
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

        {/* 밑을 고르는 것뿐이라 봉우리 자리와 높이의 뜻은 안 바뀐다 — 같은
            그림을 2.303 배로 늘인 것이다.  그래도 폭을 자로 재서 적는
            사람에게는 다른 수라서, 어느 축으로 보고 있는지가 보여야 한다. */}
        <div className="row" style={{ gap: 8, alignItems: 'center' }}>
          <span className="tiny faint">가로축</span>
          <div className="segmented" role="group" aria-label="가로축">
            {TAU_AXES.map((one) => (
              <button key={one} type="button" className={axis === one ? 'on' : ''}
                      onClick={() => setAxis(one)}>
                {tauAxisShort(one)}
              </button>
            ))}
          </div>
        </div>

        <Plot
          series={series}
          xLabel={tauAxisLabel(axis)}
          yLabel={`γ (${zUnit})`}
          height={280}
          legend
          describeX={(value) => tauBand(value, axis)}
        />

        <details className="tiny faint">
          <summary>봉우리가 넓은데 왜인가요?</summary>
          <div style={{ marginTop: 6 }}>{WIDTH_NOTE}</div>
        </details>

        <CopyBar
          items={[{
            label: 'γ(τ)',
            // τ 를 그대로 낸다 -- 로그로 내보내면 워크시트에서 되돌릴 수 없다.
            title: `τ (s) 와 γ (${zUnit}) 두 열 · 지금 보고 있는 λ 의 것`,
            // 화면이 Ω·cm² 로 그리고 있으면 붙여 넣는 열도 Ω·cm² 다.
            build: () => drtTsv(shown, (value) => perArea(value, area)),
          }]}
        />

        <KeyValues
          cols={2}
          rows={[
            ['R∞', `${num(perArea(shown.r_inf_ohm, area), 4)} ${zUnit}`],
            ['전체 분극', kept < 0.95
              ? `${num(perArea(shown.total_polarisation_ohm, area), 4)} ${zUnit}`
                + ` · 벌점 없는 답의 ${(kept * 100).toFixed(0)}%`
              : `${num(perArea(shown.total_polarisation_ohm, area), 4)} ${zUnit}`],
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
                  <th>저항 ({zUnit})</th>
                  <th>γ 최대 ({zUnit})</th>
                </tr>
              </thead>
              <tbody>
                {shown.peaks.map((peak) => (
                  <tr key={peak.tau_s}>
                    <td>{format(peak.frequency_hz)} Hz</td>
                    <td>{format(peak.tau_s)} s</td>
                    {/* 봉우리 아래 넓이 — DRT 를 그림이 아니라 수로 만드는 것. */}
                    <td>{num(perArea(peak.resistance_ohm, area), 4)} {zUnit}</td>
                    <td className="dim">{num(perArea(peak.gamma_ohm, area), 3)}</td>
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
