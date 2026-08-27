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

import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { CopyBar } from '../components/CopyBar'
import { Plot, PlotLegend, type PlotSeries } from '../components/Plot'
import { Alert, Card, Empty, Field, Metric, MetricBand, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { num, seriesColor } from '../lib/format'
import { perArea } from '../lib/areanorm'
import { nyquistXy, sweepAt } from '../lib/eis'
import { useAsync, useStickyState } from '../lib/hooks'
import {
  Z_UNITS, Z_UNIT_KEY, type ZUnit, areaFor, validZUnit, zUnitLabel,
} from '../lib/zunit'
import { seriesWideTsv } from '../lib/origin'
import type { ScanPoint } from '../lib/types'

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
  const parameters = useMemo(() => scan.data?.parameters ?? [], [scan.data])
  //: 스윕 전부가 같은 면적일 때만 서버가 값을 준다 — 하나라도 어긋나면 `null`
  //  이고, 그때는 나눌 수가 없다 (섞인 수가 나온다).
  const scanArea = scan.data?.area_cm2_effective ?? null
  const area = areaFor(zPick, scanArea)
  const zUnit = zUnitLabel(area ? 'ohmcm2' : 'ohm')
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
    return (raw.data ?? []).map((item) => {
      const index = order.get(item.id) ?? 0
      const point = points[index]
      const { x, y } = nyquistXy(item.z_re, item.z_im, dropInductive,
                                 (value) => perArea(value, area))
      // 범례에 SOC 를 적는다.  `#3` 만으로는 어느 충전 상태인지 모르고,
      // 그것이 이 화면을 여는 이유다.  비교 화면도 같은 규칙을 쓴다
      // (`lib/eis: sweepAt`) — 두 화면이 같은 스윕을 다르게 부르면 안 된다.
      const at = point ? sweepAt(point) : ''
      return {
        label: `#${point?.sweep_index ?? index + 1}`,
        note: at || undefined,
        x,
        y,
        color: seriesColor(index),
        points: true,
        width: 1,
        hidden: hidden.includes(point?.sweep_index ?? -1),
      }
    })
  }, [raw.data, points, hidden, dropInductive, area])

  const shownOverlay = useMemo(
    () => overlay.filter((series) => !series.hidden), [overlay])

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
        title="나이퀴스트 — 스윕 전부"
        actions={
          <div className="row" style={{ gap: 10, alignItems: 'center' }}>
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
            <label className="tiny faint row" style={{ gap: 6, alignItems: 'center' }}>
              <input
                type="checkbox"
                checked={dropInductive}
                onChange={(event) => setDropInductive(event.target.checked)}
              />
              고주파 유도성 점 접기
            </label>
          </div>
        }
        tight
      >
        {raw.error ? <Alert kind="error">{raw.error}</Alert>
          : raw.loading && !raw.data ? <div style={{ padding: 20 }}><Spinner /></div>
          : overlay.length ? (
            <>
              <Plot
                series={overlay}
                xLabel={`Z′ (${zUnit})`}
                yLabel={`−Z″ (${zUnit})`}
                height={380}
                equalAspect
                positiveFit
              />
              {/* 골라 둔 단위가 이 스캔에서 안 되면 **말한다.**  말없이 Ω 로
                  떨어뜨리면 화면은 Ω·cm² 를 고른 채로 Ω 를 그리고 있게 된다. */}
              {zPick === 'ohmcm2' && !scanArea ? (
                <div className="tiny warn" style={{ paddingTop: 6 }}>
                  스윕들의 면적이 비었거나 서로 다릅니다 — Ω 로 그립니다.
                  <span className="tiny faint">
                    {' '}한 스캔은 한 셀이라 면적이 같아야 하는데, 스윕 하나의
                    면적만 고쳐 두면 대표값으로 나눈 수가 섞입니다.
                  </span>
                </div>
              ) : null}
              {area ? (
                <div className="tiny faint" style={{ paddingTop: 6 }}>
                  면적 {num(scanArea, 4)} cm² 로 나눈 값입니다.
                </div>
              ) : null}
              {/* 충방전 사이클 고르개와 같은 손놀림 — 조각을 눌러 켜고 끈다. */}
              <PlotLegend
                series={overlay}
                onToggle={(name) => {
                  const index = Number(name.replace('#', ''))
                  setHidden((current) => current.includes(index)
                    ? current.filter((one) => one !== index)
                    : [...current, index])
                }}
              />
              <CopyBar items={[{
                label: '나이퀴스트 (스윕 전부)',
                title: `스윕마다 Z′·−Z″ 두 열 — 지금 켜 둔 ${shownOverlay.length}개`,
                disabled: !shownOverlay.length,
                // **켜 둔 것만 나간다.**  화면에서 끈 스윕이 클립보드에
                // 따라가면, 붙여 넣은 표가 방금 본 그림과 다른 것이 된다.
                skipped: overlay.length - shownOverlay.length,
                skippedNote: (n) => `꺼 둔 ${n}개는 빠졌습니다`,
                build: () => seriesWideTsv(shownOverlay,
                                           { x: `Z′ (${zUnit})`, y: `−Z″ (${zUnit})` }),
              }]} />
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
            <Field label="파라미터">
              <select
                aria-label="파라미터"
                value={parameter}
                onChange={(event) => setParameter(event.target.value)}
              >
                {parameters.map((name) => (
                  <option key={name} value={name}>{name}</option>
                ))}
              </select>
            </Field>
          ) : null
        }
      >
        {curve ? (
          <>
            {label ? <div className="sub" style={{ marginBottom: 8 }}>{label}</div> : null}
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
          </>
        ) : (
          <Empty title="그릴 점이 없습니다" icon="∿">
            이 스캔에서 결정된 파라미터가 아직 없습니다.
          </Empty>
        )}
      </Card>

      <Card title={`스윕 ${points.length}개`} tight>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th style={{ textAlign: 'left' }}>이름</th>
                <th>용량 (mAh)</th>
                <th>전위 (V)</th>
                {/* **회로가 달라도 뜻이 같은 둘.**  파라미터 이름은 회로마다
                    달라서 (`R0`/`Rs`) 열이 될 수 없다 — 스캔 안에서 스윕마다
                    다른 회로가 이겼을 수 있고, 그때도 이 두 열은 이어진다. */}
                <th>R₀ (Ω)</th>
                <th>ΔR₀</th>
                <th>총저항 (Ω)</th>
                <th>Δ총저항</th>
                <th>점</th>
                <th style={{ textAlign: 'left' }}>회로</th>
                <th>χ²</th>
                {parameters.map((name) => <th key={name}>{name}</th>)}
              </tr>
            </thead>
            <tbody>
              {points.map((point, index) => (
                <tr key={point.spectrum_id}
                    className={hidden.includes(point.sweep_index) ? 'dim' : undefined}>
                  <td>{point.sweep_index}</td>
                  <td className="text">
                    <Link to={`/eis/${point.spectrum_id}`}>{point.name}</Link>
                  </td>
                  <td>{point.capacity_mah === null ? '—' : num(point.capacity_mah, 4)}</td>
                  <td>{point.potential_v === null ? '—' : num(point.potential_v, 4)}</td>
                  <td className={point.series_resistance_ohm === null ? 'dim' : ''}>
                    {point.series_resistance_ohm === null
                      ? '—' : num(point.series_resistance_ohm, 4)}
                  </td>
                  <td className="dim">{delta(points, index, 'series_resistance_ohm')}</td>
                  <td className={point.total_resistance_ohm === null ? 'dim' : ''}>
                    {point.total_resistance_ohm === null
                      ? '—' : num(point.total_resistance_ohm, 4)}
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
      </Card>
    </main>
  )
}
