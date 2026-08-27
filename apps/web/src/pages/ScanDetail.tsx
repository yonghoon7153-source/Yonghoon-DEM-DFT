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
import { Plot, type PlotSeries } from '../components/Plot'
import { Alert, Card, Empty, Field, Metric, MetricBand, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { num } from '../lib/format'
import { useAsync } from '../lib/hooks'
import type { ScanPoint } from '../lib/types'

const CONFIG_LABEL: Record<string, string> = {
  full: '풀셀', half: '하프셀', sym: '대칭셀',
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
  const parameters = useMemo(() => scan.data?.parameters ?? [], [scan.data])
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
                <th style={{ textAlign: 'left' }}>회로</th>
                <th>χ²</th>
                {parameters.map((name) => <th key={name}>{name}</th>)}
              </tr>
            </thead>
            <tbody>
              {points.map((point) => (
                <tr key={point.spectrum_id}>
                  <td>{point.sweep_index}</td>
                  <td className="text">
                    <Link to={`/eis/${point.spectrum_id}`}>{point.name}</Link>
                  </td>
                  <td>{point.capacity_mah === null ? '—' : num(point.capacity_mah, 4)}</td>
                  <td>{point.potential_v === null ? '—' : num(point.potential_v, 4)}</td>
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
