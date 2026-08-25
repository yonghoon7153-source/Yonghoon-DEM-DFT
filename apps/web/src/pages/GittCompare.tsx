/** GITT 비교 — pseudo-OCV 를 겹쳐 본다.
 *
 *  이 화면이 겹치는 것은 **준평형 전압 곡선**이지 확산계수가 아니다.  D 는
 *  재료 상수에 기대는데 (ADR 0020), 그 상수는 기록마다 사람이 넣은 값이라
 *  서로 다른 셀의 D 를 한 그림에 놓으면 셀의 차이인지 입력의 차이인지
 *  구분되지 않는다.  pOCV 는 파일에서 바로 나오므로 그런 문제가 없다.
 */

import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { CopyBar } from '../components/CopyBar'
import { Plot, type PlotSeries } from '../components/Plot'
import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { seriesColor } from '../lib/format'
import { useAsync } from '../lib/hooks'
import type { GittRun, Pocv } from '../lib/types'

/** 한 번에 겹칠 수 있는 기록 수.  하나가 요청 하나라 무한정 늘릴 수 없다. */
const OVERLAY_LIMIT = 8

function label(run: GittRun): string {
  return [run.sample_name, run.name].filter(Boolean).join(' · ') || run.name
}

export function GittCompare() {
  const [search, setSearch] = useState('')
  const [chosen, setChosen] = useState<number[]>([])

  const runs = useAsync(() => api.listGittRuns(), [], { live: true })
  const rows = useMemo(() => {
    const needle = search.trim().toLowerCase()
    return (runs.data ?? []).filter((run) => !needle
      || run.name.toLowerCase().includes(needle)
      || (run.sample_name ?? '').toLowerCase().includes(needle))
  }, [runs.data, search])

  const selected = useMemo(
    () => chosen.filter((id) => rows.some((run) => run.id === id)), [chosen, rows])

  // 서버에 묶음 endpoint 가 없으므로 하나씩 부른다.  상한이 8 인 이유가
  // 이것이다 -- 스무 개를 고르면 요청 스무 개다.
  const curves = useAsync(
    () => Promise.all(selected.map((id) => api.gittPocv(id))),
    [selected.join(',')],
  )

  const fresh = useMemo(() => {
    const got = (curves.data ?? []).map((item: Pocv) => item.gitt_id).sort().join(',')
    return got === [...selected].sort().join(',')
  }, [curves.data, selected])

  const series = useMemo<PlotSeries[]>(() => {
    if (!fresh) return []
    const out: PlotSeries[] = []
    for (const curve of curves.data ?? []) {
      const run = rows.find((item) => item.id === curve.gitt_id)
      const color = seriesColor(rows.findIndex((item) => item.id === curve.gitt_id))
      // 충전과 방전을 한 색의 실선·점선으로.  둘을 다른 색으로 주면 기록이
      // 넷일 때 색이 여덟이 되어 어느 둘이 한 셀인지 안 보인다.
      if (curve.charge.length) {
        out.push({
          label: `${run ? label(run) : curve.gitt_id} 충전`,
          x: curve.charge.map((p) => p.capacity_mah),
          y: curve.charge.map((p) => p.voltage_v),
          color, points: true, width: 1.4,
        })
      }
      if (curve.discharge.length) {
        out.push({
          label: `${run ? label(run) : curve.gitt_id} 방전`,
          x: curve.discharge.map((p) => p.capacity_mah),
          y: curve.discharge.map((p) => p.voltage_v),
          color, points: true, width: 1.4, dash: [4, 3],
        })
      }
    }
    return out
  }, [curves.data, fresh, rows])

  const skipped = useMemo(
    () => (curves.data ?? []).reduce(
      (sum: number, c: Pocv) => sum + c.skipped_charge + c.skipped_discharge, 0),
    [curves.data])

  function toggle(id: number) {
    setChosen((now) => {
      if (now.includes(id)) return now.filter((item) => item !== id)
      if (now.length >= OVERLAY_LIMIT) return now
      return [...now, id]
    })
  }

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>GITT 비교</h1>
          <div className="sub">
            준평형 전압 곡선(pseudo-OCV)을 겹쳐서 — 같은 색의 실선이 충전,
            점선이 방전입니다
          </div>
        </div>
      </div>

      <Card
        title={`고른 것 ${selected.length} / ${OVERLAY_LIMIT}`}
        actions={
          <div className="row" style={{ gap: 6 }}>
            <Field label="검색" hint="이름 · 셀">
              <input
                aria-label="검색"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />
            </Field>
            <button type="button" onClick={() => setChosen([])}>비우기</button>
          </div>
        }
      >
        {runs.error ? (
          <Alert kind="error">{runs.error}</Alert>
        ) : runs.loading && !runs.data ? (
          <Spinner />
        ) : rows.length ? (
          <div className="col" style={{ gap: 10 }}>
            <div className="chips">
              {rows.map((run, index) => {
                const on = selected.includes(run.id)
                return (
                  <button
                    key={run.id}
                    type="button"
                    className={on ? 'chip on' : 'chip'}
                    aria-pressed={on}
                    onClick={() => toggle(run.id)}
                  >
                    <span className="dot" style={{ background: seriesColor(index) }} />
                    {label(run)}
                  </button>
                )
              })}
            </div>
            {selected.length >= OVERLAY_LIMIT ? (
              <div className="tiny faint">
                한 번에 {OVERLAY_LIMIT}개까지입니다 — 하나를 꺼야 다른 것을 켤 수
                있습니다.
              </div>
            ) : null}
          </div>
        ) : (
          <Empty title="고를 GITT 기록이 없습니다" icon="↯">
            <Link to="/gitt/upload">업로드</Link>에서 올려 주세요.
          </Empty>
        )}
      </Card>

      <Card title="pseudo-OCV">
        <CopyBar
          items={[{
            label: 'pseudo-OCV',
            disabled: !fresh || !series.length,
            build: () => {
              const head = series.map((s) => [`${s.label} 용량`, `${s.label} 전압`])
              const depth = Math.max(...series.map((s) => s.x.length), 0)
              const lines = [head.flat().join('\t')]
              for (let i = 0; i < depth; i += 1) {
                lines.push(series.map((s) => [
                  s.x[i] ?? '', s.y[i] ?? '']).flat().join('\t'))
              }
              return lines.join('\n')
            },
          }]}
        />
        {curves.error ? <Alert kind="error">{curves.error}</Alert> : null}
        {/* 뺀 펄스를 조용히 버리면 잘린 파일과 정상 파일이 곡선에서 구분되지
            않는다 (ADR 0020). */}
        {skipped ? (
          <Alert kind="warn">
            휴지가 뒤따르지 않아 {skipped}개 펄스를 뺐습니다 — 그 자리의 전압은
            평형이 아닙니다.
          </Alert>
        ) : null}
        {!selected.length ? (
          <div className="tiny faint" style={{ padding: 12 }}>
            위에서 기록을 골라 주세요.
          </div>
        ) : curves.loading && !curves.data ? (
          <Spinner />
        ) : series.length ? (
          <Plot series={series} xLabel="용량 (mAh)" yLabel="전압 (V)"
                height={380} legend />
        ) : null}
      </Card>
    </main>
  )
}
