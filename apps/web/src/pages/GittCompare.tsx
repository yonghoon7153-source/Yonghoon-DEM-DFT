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
import { useGroupChoice } from '../components/GroupFilter'
import { PickGrid } from '../components/PickGrid'
import { Plot, type PlotSeries } from '../components/Plot'
import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { seriesColor } from '../lib/format'
import { gittDivisor, splitByBasis, GITT_AXIS_LABEL, GITT_BASIS_LABEL,
         type GittBasis } from '../lib/gittbasis'
import { useAsync } from '../lib/hooks'
import { pseudoOcvWideTsv } from '../lib/origin'
import type { GittRun, Pocv } from '../lib/types'

/** 한 번에 겹칠 수 있는 기록 수.  하나가 요청 하나라 무한정 늘릴 수 없다. */
const OVERLAY_LIMIT = 8

function label(run: GittRun): string {
  return [run.sample_name, run.name].filter(Boolean).join(' · ') || run.name
}

export function GittCompare() {
  const [search, setSearch] = useState('')
  const [purpose, setPurpose] = useState('')
  const [sampleId, setSampleId] = useState<number | null>(null)
  const [chosen, setChosen] = useState<number[]>([])

  const runs = useAsync(() => api.listGittRuns(), [], { live: true })
  const group = useGroupChoice()
  //: 용량 축.  기본은 mAh — 질량·면적이 없는 기록이 하나라도 있으면 다른
  //  기준은 그것을 빼야 하고, 처음 여는 사람에게 곡선이 없어져 보이는 것보다
  //  단위가 기록마다 다르다는 것이 덜 놀랍다.
  const [basis, setBasis] = useState<GittBasis>('mAh')
  // 그룹은 셀의 성질이라 셀 표가 있어야 거를 수 있다.  EIS 비교와 같은 이유,
  // 같은 모양이다 (ADR 0024).
  const samples = useAsync(() => api.listSamples(), [], { live: true })

  const purposes = useMemo(() => {
    const seen = new Set<string>()
    for (const run of runs.data ?? []) if (run.purpose) seen.add(run.purpose)
    return [...seen].sort((a, b) => a.localeCompare(b, 'ko'))
  }, [runs.data])

  const cells = useMemo(() => {
    const seen = new Map<number, string>()
    for (const run of runs.data ?? []) {
      if (run.sample_id && run.sample_name) seen.set(run.sample_id, run.sample_name)
    }
    return [...seen].sort((a, b) => a[1].localeCompare(b[1], 'ko'))
  }, [runs.data])

  const inGroup = group.includes
  const rows = useMemo(() => {
    const needle = search.trim().toLowerCase()
    return (runs.data ?? []).filter((run) => {
      if (purpose && (run.purpose ?? '') !== purpose) return false
      if (sampleId !== null && run.sample_id !== sampleId) return false
      // 그룹은 이제 **측정 자신의 것**이 먼저다 (ADR 0027) -- 셀에 안 붙은
      // 측정도 묶일 수 있고, `*_effective` 가 "자기 것 → 셀 것" 을 이미 편다.
      if (!inGroup(run.group_id_effective ?? null)) return false
      return !needle
        || run.name.toLowerCase().includes(needle)
        || (run.sample_name ?? '').toLowerCase().includes(needle)
    })
  }, [runs.data, samples.data, search, purpose, sampleId, group.effective, inGroup])

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

  // 겹쳐 그릴 때 하나만 못 나눠도 그림이 거짓말을 한다: mAh 곡선과 mAh/cm²
  // 곡선이 같은 가로눈금에 서면 길이 차이가 용량 차이인지 단위 차이인지 볼
  // 방법이 없다.  빼고 이름을 적는다.
  const shownRuns = useMemo(
    () => splitByBasis(rows.filter((row) => selected.includes(row.id)), basis),
    [rows, selected, basis])
  const keptIds = useMemo(
    () => new Set(shownRuns.kept.map((run) => run.id)), [shownRuns])

  const series = useMemo<PlotSeries[]>(() => {
    if (!fresh) return []
    const out: PlotSeries[] = []
    for (const curve of curves.data ?? []) {
      const run = rows.find((item) => item.id === curve.gitt_id)
      if (!run || !keptIds.has(run.id)) continue
      // 기록마다 나누는 수가 다르다 (질량·면적이 다르므로).  하나로 묶어서
      // 나누면 그 순간 모든 곡선이 한 셀의 것이 된다.
      const per = gittDivisor(run, basis) || 1
      const color = seriesColor(rows.findIndex((item) => item.id === curve.gitt_id))
      // 충전과 방전을 한 색의 실선·점선으로.  둘을 다른 색으로 주면 기록이
      // 넷일 때 색이 여덟이 되어 어느 둘이 한 셀인지 안 보인다.
      if (curve.charge.length) {
        out.push({
          label: `${run ? label(run) : curve.gitt_id} 충전`,
          x: curve.charge.map((p) => p.capacity_mah / per),
          y: curve.charge.map((p) => p.voltage_v),
          color, points: true, width: 1.4,
        })
      }
      if (curve.discharge.length) {
        out.push({
          label: `${run ? label(run) : curve.gitt_id} 방전`,
          x: curve.discharge.map((p) => p.capacity_mah / per),
          y: curve.discharge.map((p) => p.voltage_v),
          color, points: true, width: 1.4, dash: [4, 3],
        })
      }
    }
    return out
  }, [curves.data, fresh, rows, basis, keptIds])

  const skipped = useMemo(
    () => (curves.data ?? []).reduce(
      (sum: number, c: Pocv) => sum + c.skipped_charge + c.skipped_discharge, 0),
    [curves.data])

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

      {runs.error ? <Alert kind="error">{runs.error}</Alert> : null}
      {runs.loading && !runs.data ? <Spinner /> : null}

      {selected.length ? (
        <Card title="고른 것" tight>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left' }}>이름</th>
                  <th style={{ textAlign: 'left' }}>관계셀</th>
                  <th style={{ textAlign: 'left' }}>목적</th>
                  <th>펄스</th>
                  {/* 이 GITT 가 어느 충방전 곡선 옆에서 나온 것인지 (ADR 0024). */}
                  <th style={{ textAlign: 'left' }}>충방전</th>
                </tr>
              </thead>
              <tbody>
                {rows.filter((run) => selected.includes(run.id)).map((run) => {
                  const cell = run.sample_id
                    ? (samples.data ?? []).find((s) => s.id === run.sample_id)
                    : undefined
                  return (
                    <tr key={run.id}>
                      <td className="text">
                        <Link to={`/gitt/${run.id}`}>{run.name}</Link>
                      </td>
                      <td className="text dim">
                        {run.sample_id
                          ? <Link to={`/samples/${run.sample_id}`}>{run.sample_name}</Link>
                          : '—'}
                      </td>
                      <td className="text dim">{run.purpose || '—'}</td>
                      <td>{run.n_pulses}</td>
                      <td className="text">
                        {cell?.run_count
                          ? <Link className="tiny" to={`/samples/${run.sample_id}#cycles`}>
                              사이클 {cell.cycle_count}
                            </Link>
                          : <span className="tiny faint">
                              {run.sample_id ? '충방전 없음' : '셀 안 붙음'}
                            </span>}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </Card>
      ) : null}

      <Card
        title="pseudo-OCV"
        actions={
          <div className="segmented" role="group" aria-label="용량 기준">
            {(['mAh', 'mAh/g', 'mAh/cm2'] as GittBasis[]).map((choice) => (
              <button key={choice} type="button"
                      className={basis === choice ? 'on' : ''}
                      onClick={() => setBasis(choice)}>
                {GITT_BASIS_LABEL[choice]}
              </button>
            ))}
          </div>
        }
      >
        {/* 그 기준을 못 쓰는 기록은 **뺀다.**  섞으면 두 곡선의 길이 차이가
            용량 차이인지 단위 차이인지 볼 방법이 없다 (§0.4). */}
        {shownRuns.dropped.length ? (
          <Alert kind="warn">
            {basis === 'mAh/g' ? '활물질 질량' : '면적'}이 적혀 있지 않아{' '}
            {shownRuns.dropped.length}개를 뺐습니다 —{' '}
            {shownRuns.dropped.map((run) => run.name).join(' · ')}.
            <span className="tiny faint">
              {' '}정확한 비교가 안 됩니다. 기록 상세나 붙은 셀에 적어 주세요.
            </span>
          </Alert>
        ) : null}
        <CopyBar
          items={[{
            label: 'pseudo-OCV',
            title: '기록마다 용량·전압 두 열',
            disabled: !fresh || !series.length,
            // 열마다 어느 기록인지.  열 한 쌍이 저마다 다른 셀이라 워크시트
            // 안에는 그것을 적을 자리가 없다.
            build: () => pseudoOcvWideTsv(series, {
              x: `용량 (${GITT_AXIS_LABEL[basis]})`, y: '전압 (V)',
            }),
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
            아래 목록에서 기록을 골라 주세요.
          </div>
        ) : curves.loading && !curves.data ? (
          <Spinner />
        ) : series.length ? (
          <Plot series={series} xLabel={GITT_AXIS_LABEL[basis]} yLabel="전압 (V)"
                height={380} legend busy={curves.loading || !fresh} />
        ) : null}
      </Card>

      {/* 세 비교 화면이 같은 고르개를 쓴다 (`PickGrid`) — EIS 와 같은 이유. */}
      <PickGrid
        title="기록 선택"
        group={group}
        groupHint="이 측정 또는 붙은 셀의 묶음"
        limit={OVERLAY_LIMIT}
        limitNote={`한 번에 ${OVERLAY_LIMIT}개까지입니다 — 하나를 꺼야 다른 것을 켤 수 있습니다.`}
        items={rows.map((run, index) => ({
          id: run.id,
          name: label(run),
          note: [`펄스 ${run.n_pulses}개`, run.purpose,
                 run.sample_name ? `셀: ${run.sample_name}` : null]
            .filter(Boolean).join(' · '),
          color: seriesColor(index),
        }))}
        picked={selected}
        onChange={setChosen}
        empty={(
          <Empty title="고를 GITT 기록이 없습니다" icon="↯">
            <Link to="/gitt/upload">업로드</Link>에서 올려 주세요.
          </Empty>
        )}
        extra={
          <>
            <Field label="관계셀" hint="이 측정이 붙어 있는 충방전 셀">
              <select
                aria-label="관계셀"
                value={sampleId ?? ''}
                onChange={(event) =>
                  setSampleId(event.target.value ? Number(event.target.value) : null)}
              >
                <option value="">전체</option>
                {cells.map(([id, name]) => (
                  <option key={id} value={id}>{name}</option>
                ))}
              </select>
            </Field>
            <Field label="목적" hint={purposes.length ? `${purposes.length}가지` : '아직 없음'}>
              <select
                aria-label="목적"
                value={purpose}
                onChange={(event) => setPurpose(event.target.value)}
              >
                <option value="">전체</option>
                {purposes.map((value) => (
                  <option key={value} value={value}>{value}</option>
                ))}
              </select>
            </Field>
            <Field label="검색" hint="이름 · 셀">
              <input
                aria-label="검색"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />
            </Field>
          </>
        }
      />

    </main>
  )
}
