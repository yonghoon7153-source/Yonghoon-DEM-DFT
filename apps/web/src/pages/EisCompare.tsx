/** EIS 비교 — 아무 스펙트럼이나 골라 겹쳐 본다.
 *
 *  셀 상세의 `CellSpectra` 와 겹쳐 그리는 일은 같지만 **고르는 범위**가 다르다.
 *  저쪽은 한 셀 안이고 여기는 전부다 — 서로 다른 셀의 200 사이클 임피던스를
 *  나란히 놓는 것이 이 화면의 이유고, 그건 저쪽에서는 할 수가 없다.
 *
 *  나이퀴스트는 두 축의 한 단위가 화면에서 같은 길이여야 한다 (`equalAspect`).
 *  세로가 눌리면 찌그러진 아크와 이상적인 반원이 구분되지 않고, 사람이 회로를
 *  고를 때 보는 것이 바로 그 차이다.
 */

import { useCallback, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { CopyBar } from '../components/CopyBar'
import { GroupFilterFields, useGroupChoice } from '../components/GroupFilter'
import { Plot, type PlotSeries } from '../components/Plot'
import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { num, seriesColor } from '../lib/format'
import { useAsync } from '../lib/hooks'
import { nyquistTsv } from '../lib/origin'
import type { EisKind, Spectrum } from '../lib/types'

/** 서버의 `/api/eis/points` 겹치기 상한과 같은 수. */
const OVERLAY_LIMIT = 12

/** 한 줄을 어떻게 부를까.  셀이 다르면 셀 이름이 먼저다 — 이 화면의 요점이
 *  서로 다른 셀을 나란히 놓는 것이라, 이름만으로는 어느 셀 것인지 모른다. */
function label(item: Spectrum): string {
  const parts = [item.sample_name, item.name].filter(Boolean)
  const tail = item.at_cycle === null ? '' : ` (${item.at_cycle}c)`
  return `${parts.join(' · ')}${tail}`
}

export function EisCompare() {
  const [kind, setKind] = useState<EisKind | ''>('')
  const [purpose, setPurpose] = useState('')
  const [sampleId, setSampleId] = useState<number | null>(null)
  const [search, setSearch] = useState('')
  const [chosen, setChosen] = useState<number[]>([])

  const spectra = useAsync(
    () => api.listSpectra({ kind: kind || undefined }), [kind], { live: true })
  const group = useGroupChoice()
  // 어느 셀이 어느 그룹인지는 스펙트럼이 아니라 셀이 안다.  그룹으로 거르려면
  // 그 표가 필요하고, 같은 표가 "충방전으로 가는 링크" 의 근거이기도 하다.
  const samples = useAsync(() => api.listSamples(), [], { live: true })

  /** 이 스펙트럼이 붙은 셀.  안 붙어 있으면 `undefined`. */
  const cellOf = useCallback(
    (item: Spectrum) => (samples.data ?? []).find((s) => s.id === item.sample_id),
    [samples.data])

  /** 지금 데이터에 실제로 있는 목적들.  목록을 고정하지 않는 이유는 목적이
   *  자유 입력이라서다 — 랩이 새 목적을 만들면 여기에 저절로 나타난다. */
  const purposes = useMemo(() => {
    const seen = new Set<string>()
    for (const item of spectra.data ?? []) if (item.purpose) seen.add(item.purpose)
    return [...seen].sort((a, b) => a.localeCompare(b, 'ko'))
  }, [spectra.data])

  /** 셀에 붙은 것만, 그룹 안에서.  붙지 않은 스펙트럼은 그룹이 없으므로
   *  그룹을 고른 순간 후보에서 빠진다 — 없는 소속을 지어내지 않는다 (§0.4). */
  const inGroup = group.includes
  const rows = useMemo(() => {
    const needle = search.trim().toLowerCase()
    const byId = new Map((samples.data ?? []).map((s) => [s.id, s]))
    return (spectra.data ?? []).filter((item) => {
      if (purpose && (item.purpose ?? '') !== purpose) return false
      if (sampleId !== null && item.sample_id !== sampleId) return false
      if (group.effective !== null) {
        const cell = item.sample_id === null ? undefined : byId.get(item.sample_id)
        if (!cell || !inGroup(cell.group_id)) return false
      }
      return !needle
        || item.name.toLowerCase().includes(needle)
        || (item.sample_name ?? '').toLowerCase().includes(needle)
    })
  }, [spectra.data, samples.data, search, purpose, sampleId, group.effective, inGroup])

  /** 드롭다운에 올릴 셀 — 스펙트럼이 하나라도 있는 것만. */
  const cells = useMemo(() => {
    const seen = new Map<number, string>()
    for (const item of spectra.data ?? []) {
      if (item.sample_id !== null && item.sample_name) seen.set(item.sample_id, item.sample_name)
    }
    return [...seen].sort((a, b) => a[1].localeCompare(b[1], 'ko'))
  }, [spectra.data])

  // 목록에서 사라진 것을 고른 채로 두면 그래프와 칩이 어긋난다.
  const selected = useMemo(
    () => chosen.filter((id) => rows.some((row) => row.id === id)), [chosen, rows])

  const points = useAsync(
    () => (selected.length ? api.spectraPoints(selected) : Promise.resolve([])),
    [selected.join(',')],
  )

  // 응답이 지금 고른 집합의 것인지.  바꾸는 사이 옛 응답이 남아 있으면 칩은
  // 꺼져 있는데 그래프와 클립보드는 켜진 집합을 말한다.
  const fresh = useMemo(() => {
    const got = (points.data ?? []).map((item) => item.id).sort().join(',')
    return got === [...selected].sort().join(',')
  }, [points.data, selected])

  const series = useMemo<PlotSeries[]>(() => {
    if (!fresh) return []
    return (points.data ?? []).map((item) => ({
      label: label(rows.find((row) => row.id === item.id) ?? ({} as Spectrum)),
      x: item.z_re,
      // 나이퀴스트 세로축은 −Z″ 다.
      y: item.z_im.map((value) => -value),
      color: seriesColor(rows.findIndex((row) => row.id === item.id)),
      points: true,
      width: 1,
    }))
  }, [points.data, fresh, rows])

  function toggle(id: number) {
    setChosen((now) => {
      if (now.includes(id)) return now.filter((item) => item !== id)
      // 상한을 넘겨 보내면 첫 화면부터 422 다.  조용히 무시하고 아래 문구가
      // 왜 안 켜지는지 말한다.
      if (now.length >= OVERLAY_LIMIT) return now
      return [...now, id]
    })
  }

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>EIS 비교</h1>
          <div className="sub">
            셀을 가리지 않고 골라 한 그림에 — 서로 다른 셀의 같은 시점을
            나란히 놓는 자리입니다
          </div>
        </div>
      </div>

      <Card
        title={`고른 것 ${selected.length} / ${OVERLAY_LIMIT}`}
        actions={
          <div className="row" style={{ gap: 6, flexWrap: 'wrap' }}>
            <GroupFilterFields pick={group} compact />
            <Field label="관계셀" hint="이 측정이 붙어 있는 충방전 셀">
              <select
                aria-label="관계셀"
                value={sampleId ?? ''}
                style={{ width: 150 }}
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
                style={{ width: 130 }}
                onChange={(event) => setPurpose(event.target.value)}
              >
                <option value="">전체</option>
                {purposes.map((value) => (
                  <option key={value} value={value}>{value}</option>
                ))}
              </select>
            </Field>
            <Field label="전해질">
              <select
                aria-label="전해질"
                value={kind}
                onChange={(event) => setKind(event.target.value as EisKind | '')}
              >
                <option value="">전체</option>
                <option value="liquid">액체</option>
                <option value="solid">전고체</option>
              </select>
            </Field>
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
        {spectra.error ? (
          <Alert kind="error">{spectra.error}</Alert>
        ) : spectra.loading && !spectra.data ? (
          <Spinner />
        ) : rows.length ? (
          <div className="col" style={{ gap: 10 }}>
            <div className="chips">
              {rows.map((row, index) => {
                const on = selected.includes(row.id)
                return (
                  <button
                    key={row.id}
                    type="button"
                    className={on ? 'chip on' : 'chip'}
                    aria-pressed={on}
                    onClick={() => toggle(row.id)}
                  >
                    <span className="dot" style={{ background: seriesColor(index) }} />
                    {label(row)}
                  </button>
                )
              })}
            </div>
            {selected.length >= OVERLAY_LIMIT ? (
              <div className="tiny faint">
                한 번에 {OVERLAY_LIMIT}개까지만 겹쳐 그립니다 — 하나를 꺼야 다른
                것을 켤 수 있습니다.
              </div>
            ) : null}
          </div>
        ) : (
          <Empty title="고를 스펙트럼이 없습니다" icon="∿">
            <Link to="/eis/upload">업로드</Link>에서 올려 주세요.
          </Empty>
        )}
      </Card>

      <Card title="나이퀴스트">
        <CopyBar
          items={[{
            label: '나이퀴스트',
            title: '고른 곡선을 Z′·−Z″ 두 열로 쌓아서',
            disabled: !fresh || !points.data?.length,
            build: () => nyquistTsv(points.data ?? []),
          }]}
        />
        {points.error ? <Alert kind="error">{points.error}</Alert> : null}
        {!selected.length ? (
          // 빈 그래프는 고장처럼 보인다.
          <div className="tiny faint" style={{ padding: 12 }}>
            위에서 스펙트럼을 골라 주세요.
          </div>
        ) : points.loading && !points.data ? (
          <Spinner />
        ) : series.length ? (
          <Plot series={series} xLabel="Z′ (Ω)" yLabel="−Z″ (Ω)"
                height={380} legend equalAspect positiveFit />
        ) : null}
      </Card>

      {selected.length ? (
        <Card title="고른 것" tight>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left' }}>이름</th>
                  <th style={{ textAlign: 'left' }}>관계셀</th>
                  <th style={{ textAlign: 'left' }}>목적</th>
                  <th>사이클</th>
                  <th>점</th>
                  <th>χ²</th>
                  <th style={{ textAlign: 'left' }}>회로</th>
                  {/* 이 임피던스가 어느 충방전 곡선 옆에서 나온 것인지.  두
                      섹션은 따로 서지만 셀 하나로 이어져 있다 (ADR 0024). */}
                  <th style={{ textAlign: 'left' }}>충방전</th>
                </tr>
              </thead>
              <tbody>
                {rows.filter((row) => selected.includes(row.id)).map((row) => (
                  <tr key={row.id}>
                    <td className="text">
                      <Link to={`/eis/${row.id}`}>{row.name}</Link>
                    </td>
                    <td className="text dim">
                      {row.sample_id === null
                        ? '—'
                        : <Link to={`/samples/${row.sample_id}`}>{row.sample_name}</Link>}
                    </td>
                    <td className="text dim">{row.purpose || '—'}</td>
                    <td>{row.at_cycle === null ? '—' : row.at_cycle}</td>
                    <td>{row.n_points}</td>
                    <td>{row.best_chi_squared === null
                      ? '—' : num(row.best_chi_squared, 3)}</td>
                    <td className="text dim mono">{row.best_circuit || '—'}</td>
                    <td className="text">
                      {cellOf(row)?.run_count
                        ? <Link className="tiny" to={`/samples/${row.sample_id}#cycles`}>
                            사이클 {cellOf(row)?.cycle_count}
                          </Link>
                        : <span className="tiny faint">
                            {row.sample_id === null ? '셀 안 붙음' : '충방전 없음'}
                          </span>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      ) : null}
    </main>
  )
}
