/** 한 SOC 스캔 — 저항이 SOC 를 따라 어떻게 움직이는가.
 *
 *  이 화면의 x축은 용량(mAh) 이고, 없으면 전위(V) 다.  둘 다 파일이 스윕마다
 *  들려 보낸 실측이라 추정이 섞이지 않는다 (ADR 0022).  세로축은 맞춘 회로의
 *  파라미터 중 고른 하나다.
 *
 *  값이 **미결정** 인 점은 서버가 아예 빼고 보낸다 (§0.4).  그래서 선이 중간에
 *  끊어져 보이는데, 그것이 맞다 — 오차막대가 값을 삼킨 점을 다른 점과 똑같이
 *  그리면 화면이 없는 측정을 있는 것처럼 말하게 된다.
 */

import { useEffect, useMemo, useRef, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { CopyBar } from '../components/CopyBar'
import { ParamName } from '../components/ParamName'
import { Plot, PlotLegend, type PlotSeries } from '../components/Plot'
import { Plot3D, type Series3D } from '../components/Plot3D'
import { Alert, Card, Empty, Field, Metric, MetricBand, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { num, seriesColor } from '../lib/format'
import { perArea } from '../lib/areanorm'
import { nyquistXy, sweepAt } from '../lib/eis'
import { useAsync, useStickyState } from '../lib/hooks'
import {
  Z_UNITS, Z_UNIT_KEY, type ZUnit, areaFor, hasStoredZUnit, validZUnit, zUnitLabel,
} from '../lib/zunit'
import { rememberedLambda } from '../lib/drtlambda'
import { seriesWideTsv } from '../lib/origin'
import { paramMeaning } from '../lib/params'
import { usePinnedColumns } from '../lib/pincols'
import {
  DRT_AXES, DRT_AXIS_KEY, type DrtAxis, decadeSplits, drtAxisLabel, drtAxisShort,
  drtAxisTick, drtAxisValue, validDrtAxis,
} from '../lib/tauaxis'
import type { ScanPoint } from '../lib/types'

/** 스윕 표에서 붙여 둘 열의 수 — `#` 과 `이름`.
 *
 *  **처음에는 `점` 까지 열하나를 붙였는데 그게 화근이었다.**  붙인 열의 폭을
 *  다 더하면 화면보다 넓어서, 오른쪽으로 밀면 뒤쪽 붙인 열들이 나머지 표를
 *  통째로 덮었다 — `점` 열이 사라진 것으로 보였다.
 *
 *  오른쪽으로 밀면서 알아야 하는 것은 "이 줄이 누구 것인가" 하나이고, 그것은
 *  `#` 과 이름이다.  나머지는 함께 밀리는 편이 낫다. */
const PINNED_COLUMNS = 2

const CONFIG_LABEL: Record<string, string> = {
  full: '풀셀', half: '하프셀', sym: '대칭셀',
}

/** 앞 스윕과의 차이.  충방전 사이클 표의 `Δ방전` 과 같은 자리다.
 *
 *  **앞 스윕이 아니라 앞의 "값이 있는" 스윕과 견준다.**  가운데 스윕 하나가
 *  미결정이면 그 자리는 비는데, 거기서 Δ 를 끊으면 그다음 줄까지 같이 비어
 *  SOC 를 따라가던 눈이 두 번 멈춘다.  건너뛴 것은 아래 안내가 말한다.
 *
 *  첫 줄은 견줄 것이 없어 줄표다 — 0 이 아니다 (§0.4).
 */
export function delta(
  points: ScanPoint[], index: number,
  key: 'series_resistance_ohm' | 'total_resistance_ohm',
): string {
  const now = points[index]?.[key]
  if (now === null || now === undefined) return '—'
  for (let before = index - 1; before >= 0; before -= 1) {
    const was = points[before]?.[key]
    if (was === null || was === undefined) continue
    const change = now - was
    return `${change >= 0 ? '+' : '−'}${num(Math.abs(change), 3)}`
  }
  return '—'
}

/** 이 파라미터의 뜻 — 서버가 회로마다 붙여 보낸 것.
 *
 *  스윕마다 다른 회로가 이겼을 수 있어 **하나라도 아는 줄**에서 가져온다.
 *  아무도 모르면 빈 문자열이다 — 이름을 뜻인 척 되풀이하지 않는다 (§0.4).
 */
function meaningOf(points: ScanPoint[], name: string): string {
  // 서버가 붙인 아크 이름이 먼저다 — 그 저항이 **이 셀에서** 무엇인지는 셀
  // 구성에 달렸고 그것은 서버가 안다 (액체의 첫 아크는 SEI, 전고체 대칭셀의
  // 첫 아크는 벌크다).
  for (const point of points) {
    if (point.labels[name]) return point.labels[name]
  }
  // 없으면 회로 원소의 일반적인 뜻 — 스펙트럼 상세의 '뜻' 열과 같은 표를 쓴다.
  // 이것마저 없으면 빈 문자열이다: 이름을 뜻인 척 되풀이하지 않는다 (§0.4).
  return paramMeaning(name)
}

/** 용량이 있으면 용량, 없으면 전위.  둘 다 없는 점은 놓을 자리가 없다. */
function axisOf(points: ScanPoint[]): { key: 'capacity_mah' | 'potential_v'; label: string } {
  const withCapacity = points.filter((p) => p.capacity_mah !== null).length
  if (withCapacity >= points.length / 2) {
    return { key: 'capacity_mah', label: '용량 (mAh)' }
  }
  return { key: 'potential_v', label: '전위 (V)' }
}

export function ScanDetail() {
  const { sha256 = '' } = useParams()
  const scan = useAsync(() => api.getScan(sha256), [sha256])
  const [parameter, setParameter] = useState('')

  const points = useMemo(() => scan.data?.points ?? [], [scan.data])
  //: **스윕 전부를 한 번에 받는다.**  `/points` 의 열두 개 상한을 안 쓰는
  //  전용 경로다 (거기 상한은 사람이 아무거나 고를 수 있어서 있는 것이고,
  //  여기서 오는 수는 파일이 정한다).  낱개로 나눠 부르면 그리는 동안 축이
  //  여러 번 다시 잡히고, 그 사이 그림은 스캔의 일부만 보여 주면서 전부인
  //  척한다 — 겹쳐 보는 이유가 정확히 그 전체 모양인데.
  const raw = useAsync(() => api.scanPoints(sha256), [sha256])
  //: 끈 스윕.  이름이 아니라 **스윕 번호**로 기억한다 — 이름은 파일 이름에
  //  `#3` 을 붙인 것이라 길고, 번호가 곧 SOC 차례다.
  const [hidden, setHidden] = useState<number[]>([])
  //: 고주파 유도성 점을 접을까.  겹쳐 보는 화면에서는 세로 눈금이 하나라,
  //  한 스윕의 꼬리가 나머지 전부의 아크를 납작하게 만든다.
  const [dropInductive, setDropInductive] = useState(true)
  //: Ω 인가 Ω·cm² 인가.  상세·비교 화면과 **같은 열쇠**를 쓴다 (`lib/zunit.ts`) —
  //  한 스캔의 스윕을 여기서 Ω 로 보다 비교 화면에서 Ω·cm² 로 보면 같은 아크가
  //  다른 크기로 나오고, 그 말은 축 이름에만 남는다.
  const [storedZUnit, setZUnit] = useStickyState<ZUnit>(Z_UNIT_KEY, 'ohm')
  const zPick = validZUnit(storedZUnit, 'ohm')
  //: 나이퀴스트인가 DRT 인가.  **같은 스윕 선택을 함께 쓴다** — 나이퀴스트에서
  //  끈 스윕이 DRT 에서 도로 켜지면, 두 그림이 다른 집합을 말하게 된다.
  const [mode, setMode] = useState<'nyquist' | 'drt'>('nyquist')
  //: 겹쳐 그릴까 비껴 쌓을까.  논문이 SOC 스캔을 실을 때 쓰는 그림이 뒤쪽이다 —
  //  열한 곡선을 같은 축에 겹치면 가장 큰 것 하나만 보이고 나머지는 그 안에
  //  숨는다 (`lib/waterfall.ts` 에 왜, 그리고 무엇을 잃는지).
  const [solid, setSolid] = useState(false)
  //: DRT 가로축.  상세·비교 화면과 같은 열쇠 (`lib/tauaxis.ts`).
  const [storedAxis, setAxis] = useStickyState<DrtAxis>(DRT_AXIS_KEY, 'tau')
  const drtAxis = validDrtAxis(storedAxis)
  const parameters = useMemo(() => scan.data?.parameters ?? [], [scan.data])
  //: 스윕 전부가 같은 면적일 때만 서버가 값을 준다 — 하나라도 어긋나면 `null`
  //  이고, 그때는 나눌 수가 없다 (섞인 수가 나온다).
  const scanArea = scan.data?.area_cm2_effective ?? null
  const area = areaFor(zPick, scanArea)
  const zUnit = zUnitLabel(area ? 'ohmcm2' : 'ohm')

  //: **면적을 알면 Ω·cm² 로 연다.**  셀끼리 견주는 값이 그것이고 논문에 적는
  //  것도 그것이다.  단, 한 번이라도 골라 본 적이 있으면 그 선택이 이긴다 —
  //  Ω 로 바꿔 놓은 화면이 새로고침마다 되돌아가면 단추가 고장 난 것으로 읽힌다.
  useEffect(() => {
    if (scanArea && !hasStoredZUnit()) setZUnit('ohmcm2')
  }, [scanArea, setZUnit])
  const axis = useMemo(() => axisOf(points), [points])

  // 목록이 오기 전에는 고를 것이 없다.  첫 파라미터를 기본으로 세우되,
  // 사람이 고른 뒤에는 건드리지 않는다.
  useEffect(() => {
    const first = parameters[0]
    if (first && !parameters.includes(parameter)) setParameter(first)
  }, [parameters, parameter])

  const drawn = useMemo(() => {
    if (!parameter) return []
    const x: number[] = []
    const y: number[] = []
    for (const point of points) {
      const at = point[axis.key]
      const value = point.values[parameter]
      if (at === null || value === undefined) continue
      x.push(at)
      y.push(value)
    }
    if (!x.length) return []
    const series: PlotSeries = { label: parameter, x, y, points: true }
    return [series]
  }, [points, parameter, axis])

  //: 나이퀴스트 겹쳐보기.  색은 스윕 차례를 따라간다 — SOC 가 그 차례다.
  const overlay = useMemo<PlotSeries[]>(() => {
    const order = new Map(points.map((p, i) => [p.spectrum_id, i]))
    return (raw.data ?? []).flatMap((item) => {
      // **모르는 스윕은 그리지 않는다.**  예전에는 못 찾으면 0번으로 떨어져서
      // 그 곡선이 `#1` 이라는 이름과 1번의 색을 달고 나왔다 — 화면에 같은
      // 이름이 두 줄 서고, 어느 쪽이 진짜 1번인지는 아무 데도 없다 (§0.4).
      const index = order.get(item.id)
      if (index === undefined) return []
      const point = points[index]
      const { x, y } = nyquistXy(item.z_re, item.z_im, dropInductive,
                                 (value) => perArea(value, area))
      // 범례에 SOC 를 적는다.  `#3` 만으로는 어느 충전 상태인지 모르고,
      // 그것이 이 화면을 여는 이유다.  비교 화면도 같은 규칙을 쓴다
      // (`lib/eis: sweepAt`) — 두 화면이 같은 스윕을 다르게 부르면 안 된다.
      const at = point ? sweepAt(point) : ''
      return [{
        label: `#${point?.sweep_index ?? index + 1}`,
        note: at || undefined,
        x,
        y,
        color: seriesColor(index),
        points: true,
        width: 1,
        hidden: hidden.includes(point?.sweep_index ?? -1),
      }]
    })
  }, [raw.data, points, hidden, dropInductive, area])

  //: DRT 는 **볼 때만** 부른다.  스윕마다 한 번씩 푸는 계산이라, 나이퀴스트만
  //  보려던 사람이 그 시간을 대신 낼 이유가 없다.  λ 는 스펙트럼 상세에서
  //  옮긴 값을 그대로 쓴다 — 두 화면이 다른 λ 를 쓰면 같은 γ 가 다르게 생겨서
  //  나란히 놓는 이 화면이 곧바로 어긋난다.
  const lambda = rememberedLambda()
  const drt = useAsync(
    () => (mode === 'drt' && points.length
      ? Promise.all(points.map((point) =>
          api.spectrumDrt(point.spectrum_id,
                          { regularisation: lambda, derivative_order: 0 })
            .then((value) => ({ id: point.spectrum_id, value }))
            .catch(() => ({ id: point.spectrum_id, value: null }))))
      : Promise.resolve([])),
    [mode, points.map((p) => p.spectrum_id).join(','), lambda],
  )

  //: DRT 겹쳐보기.  나이퀴스트와 **같은 색·같은 이름·같은 껐다 켰다**를 쓴다.
  const drtOverlay = useMemo<PlotSeries[]>(() => {
    const order = new Map(points.map((point, index) => [point.spectrum_id, index]))
    return (drt.data ?? []).flatMap(({ id, value }) => {
      if (!value) return []
      const index = order.get(id)
      if (index === undefined) return []
      const point = points[index]
      return [{
        label: `#${point?.sweep_index ?? index + 1}`,
        note: point ? sweepAt(point) || undefined : undefined,
        x: value.tau_s.map((tau) => drtAxisValue(drtAxis, tau)),
        // γ 도 저항이다 — 나이퀴스트를 Ω·cm² 로 보면서 γ 만 Ω 로 두면 같은
        // 화면의 두 그림이 다른 자로 그려진다.
        y: value.gamma_ohm.map((gamma) => perArea(gamma, area)),
        color: seriesColor(index),
        width: 1.5,
        hidden: hidden.includes(point?.sweep_index ?? -1),
      }]
    })
  }, [drt.data, points, hidden, drtAxis, area])

  //: 지금 그리는 것.  **껐다 켰다는 하나**라, 어느 그림을 보고 있든 같은 스윕이
  //  꺼져 있다.
  const flat = mode === 'drt' ? drtOverlay : overlay

  //: 3D 는 **축이 셋인 그림**이다 (`components/Plot3D`).  전에는 곡선을 깊이만큼
  //  밀어 흉내를 냈는데, 축을 안 그리면 깊이는 없는 것과 같아서 열한 곡선이
  //  대각선으로 늘어선 한 덩어리로 보였다.
  //
  //  깊이는 **전위(V)** 다 — 계측기가 SOC 를 % 로 말해 주지 않으므로, 논문의
  //  `SOC 0/50/100 %` 자리에 실제 전위가 들어간다.  **켜 둔 것만 세운다**:
  //  꺼 둔 스윕이 자리를 차지하면 상자에 빈 칸이 생기고, 그 빈 칸이 "여기
  //  측정이 없다" 로 읽힌다.
  const solidSeries = useMemo<Series3D[]>(() => {
    const depth = new Map(points.map(
      (point) => [`#${point.sweep_index}`, point.potential_v ?? null]))
    return flat.filter((one) => !one.hidden).map((one, index) => ({
      label: one.label,
      x: one.x,
      y: one.y,
      // 전위를 모르는 스윕이 섞여 있으면 **차례**로 세운다 — 아는 것만 세우면
      // 모르는 것들이 한 자리에 겹치고, 그 겹침이 물리로 읽힌다.
      z: depth.get(one.label) ?? index,
      color: one.color,
      points: one.points,
    }))
  }, [flat, points])

  //: 깊이 눈금은 **스윕이 실제로 앉은 자리**다.  고르게 나눈 눈금을 쓰면 전위
  //  간격이 고르지 않은 스캔에서 눈금과 곡선이 어긋난다.
  const depthTicks = useMemo(
    () => [...new Set(solidSeries.map((one) => one.z).filter(Number.isFinite))]
      .sort((a, b) => a - b), [solidSeries])

  //: 전위를 다 아는가 — 모르면 깊이 축 이름이 `스윕 차례` 가 된다.
  const depthIsVolt = points.length > 0
    && points.every((point) => point.potential_v !== null)

  const shownOverlay = useMemo(
    () => flat.filter((one) => !one.hidden), [flat])
  //: 2D 로 그리는 것은 곧 `flat` 이다 (3D 는 `Plot3D` 가 따로 받는다).
  const series: PlotSeries[] = flat

  /** 범례 조각과 표의 줄이 **같은 것**을 누른다 (`#3` 을 껐다 켰다). */
  const toggleSweep = (sweep: number) =>
    setHidden((current) => current.includes(sweep)
      ? current.filter((one) => one !== sweep)
      : [...current, sweep])

  //: 스윕 표는 열이 스물이 넘는다 (파라미터가 열셋).  오른쪽으로 밀면 이름이
  //  화면 밖으로 나가고, 그때부터는 어느 스윕의 줄인지 알 수 없다.  `점` 까지
  //  붙여 둔다 — 거기까지가 "이 스윕이 무엇인가" 이고, 그 뒤가 맞춘 결과다.
  const tableBox = useRef<HTMLDivElement>(null)
  usePinnedColumns(tableBox, PINNED_COLUMNS, [points.length, parameters.length])

  const label = useMemo(() => {
    for (const point of points) {
      if (point.labels[parameter]) return point.labels[parameter]
    }
    return ''
  }, [points, parameter])

  const curve = drawn[0]
  const missing = points.length - (curve?.x.length ?? 0)

  if (scan.loading && !scan.data) {
    return <main className="page"><Spinner label="스캔을 읽는 중" /></main>
  }
  if (scan.error) {
    return <main className="page"><Alert kind="error">{scan.error}</Alert></main>
  }
  if (!scan.data) return null

  const head = scan.data
  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>{head.name}</h1>
          <div className="sub">
            <Link to="/eis/library">EIS 라이브러리</Link>
            {' · '}
            {head.kind === 'solid' ? '전고체' : '액체'}
            {head.cell_config ? ` · ${CONFIG_LABEL[head.cell_config] ?? head.cell_config}` : ''}
            {head.purpose ? ` · ${head.purpose}` : ''}
            {head.sample_id ? (
              <>
                {' · '}
                <Link to={`/samples/${head.sample_id}`}>{head.sample_name}</Link>
              </>
            ) : null}
          </div>
        </div>
      </div>

      <MetricBand>
        <Metric label="스윕" value={head.sweeps} />
        <Metric label="fitting 한 스윕" value={`${head.fitted} / ${head.sweeps}`}
                muted={head.fitted === 0} />
        <Metric label="회로" value={points.find((p) => p.circuit)?.circuit || '—'}
                muted={head.fitted === 0} />
      </MetricBand>

      {head.fitted === 0 ? (
        <Alert kind="info">
          아직 맞춘 회로가 없습니다.{' '}
          <Link to="/eis/spectra">여러 개 한꺼번에 맞추기</Link>에서 이 파일의
          스윕들을 골라 한 회로로 맞추면 여기에 추세가 그려집니다.
        </Alert>
      ) : null}

      {/* **나이퀴스트가 먼저다.**  파일 하나가 스윕 스물이면 목록에서는 줄이
          스무 개인데, 사람이 보려는 것은 그 스무 개가 SOC 를 따라 어떻게
          움직이는가 하나다.  아래 파라미터 추세는 그것을 숫자로 요약한 것이고,
          요약을 먼저 보여 주면 원래 모양을 못 본 채로 읽게 된다. */}
      <Card
        title={mode === 'drt' ? 'DRT — 스윕 전부' : '나이퀴스트 — 스윕 전부'}
        actions={
          <div className="row" style={{ gap: 10, alignItems: 'center' }}>
            {/* 같은 스윕을 두 눈으로 본다.  나이퀴스트는 아크의 모양, DRT 는
                그 아크가 몇 개인가 — SOC 를 따라 봉우리가 어떻게 옮겨 가는지가
                DRT 쪽에서 훨씬 먼저 보인다. */}
            <div className="segmented" role="group" aria-label="그림">
              <button type="button" className={mode === 'nyquist' ? 'on' : ''}
                      onClick={() => setMode('nyquist')}>나이퀴스트</button>
              <button type="button" className={mode === 'drt' ? 'on' : ''}
                      onClick={() => setMode('drt')}>DRT</button>
            </div>
            {/* 겹쳐 그릴까 비껴 쌓을까.  열한 곡선을 같은 축에 겹치면 가장 큰
                것 하나만 보이고 나머지는 그 안에 숨는다 — 논문이 SOC 스캔을
                실을 때 계단으로 그리는 이유가 그것이다. */}
            <div className="segmented" role="group" aria-label="보기">
              <button type="button" className={solid ? '' : 'on'}
                      onClick={() => setSolid(false)}>2D</button>
              <button type="button" className={solid ? 'on' : ''}
                      title="전위(V)를 깊이로 비껴 쌓습니다 — 값이 옮겨지므로 모양을 보는 그림입니다"
                      onClick={() => setSolid(true)}>3D</button>
            </div>
            {/* DRT 를 볼 때만 뜬다 — 나이퀴스트에는 τ 축이 없다. */}
            {mode === 'drt' ? (
              <div className="segmented" role="group" aria-label="가로축">
                {DRT_AXES.map((one) => (
                  <button key={one} type="button" className={drtAxis === one ? 'on' : ''}
                          onClick={() => setAxis(one)}>
                    {drtAxisShort(one)}
                  </button>
                ))}
              </div>
            ) : null}
            {/* 단위는 스캔 하나에 하나다 — 스윕끼리 견주는 화면이라 더 그렇다. */}
            <div className="segmented" role="group" aria-label="임피던스 단위">
              {Z_UNITS.map((one) => (
                <button
                  key={one}
                  type="button"
                  className={zPick === one ? 'on' : ''}
                  disabled={one === 'ohmcm2' && !scanArea}
                  title={one === 'ohmcm2' && !scanArea
                    ? '스윕들의 면적이 비었거나 서로 다릅니다 — 스펙트럼 상세에서 면적이나 지름을 적어 주세요'
                    : undefined}
                  onClick={() => setZUnit(one)}
                >
                  {zUnitLabel(one)}
                </button>
              ))}
            </div>
            {/* DRT 에는 뜻이 없다 — 서버가 풀 때 이미 뺀 점들이고, 여기 이
                단추는 나이퀴스트의 세로 눈금을 지키는 것이다. */}
            {mode === 'nyquist' ? (
              <label className="tiny faint row" style={{ gap: 6, alignItems: 'center' }}>
                <input
                  type="checkbox"
                  checked={dropInductive}
                  onChange={(event) => setDropInductive(event.target.checked)}
                />
                고주파 유도성 점 접기
              </label>
            ) : null}
          </div>
        }
        tight
      >
        {raw.error ? <Alert kind="error">{raw.error}</Alert>
          : raw.loading && !raw.data ? <div style={{ padding: 20 }}><Spinner /></div>
          : mode === 'drt' && drt.loading && !drt.data
            ? <div style={{ padding: 20 }}><Spinner label="DRT 를 푸는 중" /></div>
          : flat.length ? (
            <>
              {solid ? (
                <Plot3D
                  series={solidSeries}
                  xLabel={mode === 'drt' ? drtAxisLabel(drtAxis) : `Z′ (${zUnit})`}
                  yLabel={mode === 'drt' ? `γ (${zUnit})` : `−Z″ (${zUnit})`}
                  zLabel={depthIsVolt ? '전위 (V)' : '스윕 차례'}
                  zTicks={depthTicks}
                  height={560}
                />
              ) : mode === 'drt' ? (
                // DRT 는 두 축의 뜻이 달라서 `equalAspect` 가 없다 — 가로는
                // 로그 시간(또는 주파수), 세로는 저항이다.
                <Plot
                  series={series}
                  xLabel={drtAxisLabel(drtAxis)}
                  yLabel={`γ (${zUnit})`}
                  height={380}
                  busy={drt.loading}
                  xTick={(value) => drtAxisTick(drtAxis, value)}
                  xSplits={drtAxis === 'f' ? decadeSplits : undefined}
                />
              ) : (
                <Plot
                  series={series}
                  xLabel={`Z′ (${zUnit})`}
                  yLabel={`−Z″ (${zUnit})`}
                  height={380}
                  equalAspect
                  positiveFit
                />
              )}
              <div className="col" style={{ gap: 6, paddingTop: 8 }}>
              {solid && !depthIsVolt ? (
                // 전위를 모르는 스윕이 섞여 있다.  **말한다** — 깊이 축이
                // 물리가 아니라 차례라는 것이 축 이름에만 있으면 눈이 안 간다.
                <div className="tiny warn">
                  전위를 모르는 스윕이 있어 깊이를 <b>스윕 차례</b>로 세웠습니다 —
                  축의 간격이 전위 간격이 아닙니다.
                </div>
              ) : null}
              {mode === 'drt' ? (
                <div className="tiny faint">
                  벌점 λ = {lambda.toExponential(2)} · 평활 차수 0 — 스펙트럼
                  상세에서 옮긴 값을 그대로 씁니다. 두 화면이 다른 λ 를 쓰면
                  같은 γ 가 다르게 생겨서, 나란히 놓는 이 화면이 곧바로
                  어긋납니다.
                </div>
              ) : null}
              {/* 골라 둔 단위가 이 스캔에서 안 되면 **말한다.**  말없이 Ω 로
                  떨어뜨리면 화면은 Ω·cm² 를 고른 채로 Ω 를 그리고 있게 된다. */}
              {zPick === 'ohmcm2' && !scanArea ? (
                <div className="tiny warn">
                  스윕들의 면적이 비었거나 서로 다릅니다 — Ω 로 그립니다.
                  <span className="tiny faint">
                    {' '}한 스캔은 한 셀이라 면적이 같아야 하는데, 스윕 하나의
                    면적만 고쳐 두면 대표값으로 나눈 수가 섞입니다.
                  </span>
                </div>
              ) : null}
              {area ? (
                <div className="tiny faint">
                  면적 {num(scanArea, 4)} cm² 로 나눈 값입니다.
                </div>
              ) : null}
              {/* 충방전 사이클 고르개와 같은 손놀림 — 조각을 눌러 켜고 끈다.
                  **처음에는 전부 켜져 있다**: 스캔을 여는 이유가 전체 모양이고,
                  그 다음에 몇 개를 빼면서 본다.  '초기화' 로 비우고 하나씩
                  켜는 쪽이 편할 때도 있어 두 단추를 나란히 둔다.
                  아래 스윕 표의 줄과 **같은 것을 누른다** (`toggleSweep`) —
                  두 곳이 따로 놀면 표에서 흐린 줄이 그림에는 그려져 있다. */}
              <div className="row" style={{ gap: 6, alignItems: 'center' }}>
                <button type="button" className="sm" onClick={() => setHidden([])}>
                  전체
                </button>
                <button
                  type="button"
                  className="sm ghost"
                  onClick={() => setHidden(points.map((point) => point.sweep_index))}
                >
                  초기화
                </button>
                <span className="tiny faint" style={{ alignSelf: 'center' }}>
                  {shownOverlay.length} / {flat.length} 켬 — 조각을 눌러 켜고 끕니다
                </span>
              </div>
              {/* 쌓아 놓아도 조각은 **스윕**의 것이다 — 깊이 축 안내선은
                  켜고 끄는 것이 아니라 눈금이라 목록에 안 넣는다. */}
              <PlotLegend
                series={flat}
                onToggle={(name) => toggleSweep(Number(name.replace('#', '')))}
              />
              {/* 범례와 클립보드가 붙어 있으면 조각 줄의 마지막 칸과 'Origin
                  으로' 가 한 덩어리로 읽힌다 — 누르는 것이 다른 두 줄이다. */}
              <div>
                <CopyBar items={[{
                  label: mode === 'drt' ? 'γ(τ) (스윕 전부)' : '나이퀴스트 (스윕 전부)',
                  title: mode === 'drt'
                    ? `스윕마다 ${drtAxisShort(drtAxis)}·γ 두 열 — 지금 켜 둔 ${shownOverlay.length}개`
                    : `스윕마다 Z′·−Z″ 두 열 — 지금 켜 둔 ${shownOverlay.length}개`,
                  disabled: !shownOverlay.length,
                  // **켜 둔 것만 나간다.**  화면에서 끈 스윕이 클립보드에
                  // 따라가면, 붙여 넣은 표가 방금 본 그림과 다른 것이 된다.
                  skipped: flat.length - shownOverlay.length,
                  skippedNote: (n) => `꺼 둔 ${n}개는 빠졌습니다`,
                  build: () => seriesWideTsv(shownOverlay, mode === 'drt'
                    ? { x: drtAxisLabel(drtAxis), y: `γ (${zUnit})` }
                    : { x: `Z′ (${zUnit})`, y: `−Z″ (${zUnit})` }),
                }]} />
              </div>
              </div>
            </>
          ) : (
            <Empty title="점을 읽지 못했습니다" icon="∿">
              원본이 없으면 다시 올려 주세요.
            </Empty>
          )}
      </Card>

      <Card
        title={`${parameter || '파라미터'} vs SOC`}
        actions={
          parameters.length ? (
            // **이름만으로는 무엇인지 모른다.**  `CPE2_Q` 와 `Ws4_tau` 가
            // 세로로 열세 줄 늘어선 드롭박스에서 고르는 일은 외우고 있는
            // 사람만 할 수 있다.  서버가 회로마다 붙여 보내는 뜻
            // (`ScanPoint.labels`)을 이름 옆에 적고, 칸을 넓혀 그 줄이 안
            // 잘리게 한다.
            <Field label="파라미터" hint="세로축에 무엇을 놓을까">
              <select
                aria-label="파라미터"
                className="wide-select"
                value={parameter}
                onChange={(event) => setParameter(event.target.value)}
              >
                {parameters.map((name) => (
                  <option key={name} value={name}>
                    {meaningOf(points, name)
                      ? `${name} — ${meaningOf(points, name)}` : name}
                  </option>
                ))}
              </select>
            </Field>
          ) : null
        }
      >
        {curve ? (
          // 그림 · 경고 · 클립보드가 한 덩어리로 붙어 있으면 경고가 그림의
          // 일부처럼 읽힌다.  세 줄 사이에 같은 간격을 준다.
          <div className="col" style={{ gap: 12 }}>
            {label ? <div className="sub">{label}</div> : null}
            <Plot series={drawn} xLabel={axis.label} yLabel={parameter} height={320} />
            {missing > 0 ? (
              <Alert kind="warn">
                {missing}개 스윕은 이 파라미터가 결정되지 않아 빠졌습니다 —
                오차가 값을 삼킨 점은 추세로 세지 않습니다.
              </Alert>
            ) : null}
            <CopyBar items={[{
              label: `${parameter} vs SOC`,
              // 화면에 그려진 점만 나간다 — 표에 있는 줄표까지 따라가면
              // 엑셀에서 그것이 0 이 된다.
              skipped: missing,
              skippedNote: (n) => `${n}개 스윕은 값이 결정되지 않아 빠졌습니다`,
              build: () => [
                [axis.label, parameter].join('\t'),
                ...curve.x.map((at, i) => [at, curve.y[i]].join('\t')),
              ].join('\n'),
            }]} />
          </div>
        ) : (
          <Empty title="그릴 점이 없습니다" icon="∿">
            이 스캔에서 결정된 파라미터가 아직 없습니다.
          </Empty>
        )}
      </Card>

      <Card title={`스윕 ${points.length}개`} tight>
        {/* `점` 까지 붙여 두고 그 뒤로 민다 (`lib/pincols.ts`).  거기까지가
            "이 스윕이 무엇인가" 이고, 그 뒤(회로·χ²·파라미터 열셋)가 맞춘
            결과다 — 결과를 읽으려고 오른쪽으로 밀 때 왼쪽에 남아야 하는 것이
            앞의 아홉 열이다. */}
        <div className="table-wrap" ref={tableBox}>
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th style={{ textAlign: 'left' }}>이름</th>
                <th>용량 (mAh)</th>
                {/* 셀끼리 견주려면 면적으로 나눈 값이라야 한다.  면적을 아직
                    안 적었으면 **줄표** 다 — 0 으로 채우면 만방전과 구분되지
                    않는다 (§0.4). */}
                <th>용량 (mAh/cm²)</th>
                <th>전위 (V)</th>
                {/* **회로가 달라도 뜻이 같은 둘.**  파라미터 이름은 회로마다
                    달라서 (`R0`/`Rs`) 열이 될 수 없다 — 스캔 안에서 스윕마다
                    다른 회로가 이겼을 수 있고, 그때도 이 두 열은 이어진다.
                    **안 나눈 것과 나눈 것을 나란히** 둔다: ZView 결과와 맞춰
                    보는 것은 Ω 이고, 논문에 적는 것은 Ω·cm² 다. */}
                <th>R₀ (Ω)</th>
                <th>R₀ (Ω·cm²)</th>
                <th>ΔR₀ (Ω)</th>
                <th>총저항 (Ω)</th>
                <th>총저항 (Ω·cm²)</th>
                <th>Δ총저항 (Ω)</th>
                <th title="이 스윕에 실제로 있는 점의 수 — 한 파일 안에서도 스윕마다 다를 수 있습니다">점</th>
                <th style={{ textAlign: 'left' }}>회로</th>
                <th title="χ² — 가중 잔차의 제곱합을 자유도로 나눈 값. 작을수록 잘 맞은 것이고, 스펙트럼끼리 견줄 수 있습니다">χ²</th>
                {/* 이름 위에 마우스를 올리면 뜻이 뜬다.  `CPE2_Q` 가 열셋
                    나란히 있는 줄에서 이름만으로 고를 수 있는 사람은 외우고
                    있는 사람뿐이다. */}
                {parameters.map((name) => {
                  const meaning = meaningOf(points, name)
                  return (
                    // `title` 은 **원래 이름부터** 적는다.  머리 칸은 첨자로
                    // 그려서 (`CPE₁,Q`) 회로 칸에 쳐 넣을 글자와 다르다.
                    <th key={name} title={meaning ? `${name} — ${meaning}` : name}>
                      <ParamName name={name} />
                    </th>
                  )
                })}
              </tr>
            </thead>
            <tbody>
              {points.map((point, index) => (
                // **줄을 누르면 그 스윕이 켜지고 꺼진다** — 위 범례 조각과 같은
                // 것을 누른다.  두 곳이 따로 놀면 표에서 흐린 줄이 그림에는
                // 그려져 있고, 어느 쪽이 맞는지 화면이 말해 주지 않는다.
                // 이름은 링크라 눌러도 여기까지 안 온다 (스윕 상세로 간다).
                // 켜 둔 줄은 **파랗게** — 충방전 사이클 표와 같은 표시다.  꺼진
                // 것을 흐리게만 하면 "전부 꺼짐" 과 "전부 켜짐" 이 같아 보인다
                // (둘 다 흐린 줄이 없다).
                <tr key={point.spectrum_id}
                    className={`clickable${
                      hidden.includes(point.sweep_index) ? ' dim' : ' selected'}`}
                    title={hidden.includes(point.sweep_index)
                      ? '눌러서 그림에 켜기' : '눌러서 그림에서 끄기'}
                    onClick={() => toggleSweep(point.sweep_index)}>
                  <td>{point.sweep_index}</td>
                  <td className="text">
                    <Link to={`/eis/${point.spectrum_id}`}
                          onClick={(event) => event.stopPropagation()}>
                      {point.name}
                    </Link>
                  </td>
                  <td>{point.capacity_mah === null ? '—' : num(point.capacity_mah, 4)}</td>
                  <td className={point.capacity_mah === null || !scanArea ? 'dim' : ''}>
                    {point.capacity_mah === null || !scanArea
                      ? '—' : num(point.capacity_mah / scanArea, 4)}
                  </td>
                  <td>{point.potential_v === null ? '—' : num(point.potential_v, 4)}</td>
                  <td className={point.series_resistance_ohm === null ? 'dim' : ''}>
                    {point.series_resistance_ohm === null
                      ? '—' : num(point.series_resistance_ohm, 4)}
                  </td>
                  <td className={point.series_resistance_ohm === null || !scanArea
                    ? 'dim' : ''}>
                    {point.series_resistance_ohm === null || !scanArea
                      ? '—' : num(point.series_resistance_ohm * scanArea, 4)}
                  </td>
                  <td className="dim">{delta(points, index, 'series_resistance_ohm')}</td>
                  <td className={point.total_resistance_ohm === null ? 'dim' : ''}>
                    {point.total_resistance_ohm === null
                      ? '—' : num(point.total_resistance_ohm, 4)}
                  </td>
                  <td className={point.total_resistance_ohm === null || !scanArea
                    ? 'dim' : ''}>
                    {point.total_resistance_ohm === null || !scanArea
                      ? '—' : num(point.total_resistance_ohm * scanArea, 4)}
                  </td>
                  <td className="dim">{delta(points, index, 'total_resistance_ohm')}</td>
                  <td className="dim">{point.n_points || '—'}</td>
                  <td className="text dim">{point.circuit || '—'}</td>
                  <td className="dim">
                    {point.chi_squared === null ? '—' : num(point.chi_squared, 3)}
                  </td>
                  {parameters.map((name) => (
                    <td key={name} className={name in point.values ? '' : 'dim'}>
                      {/* 값이 없는 칸은 0 이 아니라 줄표다.  '결정되지 않음'
                          을 숫자로 채우면 표가 없는 측정을 말하게 된다. */}
                      {name in point.values ? num(point.values[name], 4) : '—'}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {/* 그림 밑에도 같은 단추가 있다.  표에서 줄을 끄다 보면 그림이 화면
            위로 사라져서, 다시 켜려고 스크롤해 올라가야 했다. */}
        <div className="row" style={{ gap: 6, padding: '6px 12px 2px',
                                      alignItems: 'center' }}>
          <button type="button" className="sm" onClick={() => setHidden([])}>
            전체
          </button>
          <button
            type="button"
            className="sm ghost"
            onClick={() => setHidden(points.map((one) => one.sweep_index))}
          >
            초기화
          </button>
          <span className="tiny faint">
            {points.length - hidden.length} / {points.length} 켬 — 줄을 눌러 켜고 끕니다
          </span>
        </div>
      </Card>
    </main>
  )
}
