/** The cell library: filter by date, cathode, process, C-rate; manage groups. */

import { useState } from 'react'
import { Link } from 'react-router-dom'

import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { num } from '../lib/format'
import { useAsync, useDebounced } from '../lib/hooks'
import type { Sample } from '../lib/types'

export function Library() {
  const [search, setSearch] = useState('')
  const [groupId, setGroupId] = useState<number | null>(null)
  const [cathode, setCathode] = useState('')
  const [process, setProcess] = useState('')
  const [dateFrom, setDateFrom] = useState('')
  const [dateTo, setDateTo] = useState('')
  const [creating, setCreating] = useState(false)

  const debouncedSearch = useDebounced(search)
  const groups = useAsync(() => api.listGroups(), [creating])
  const facets = useAsync(() => api.facets(), [])
  const samples = useAsync(
    () =>
      api.listSamples({
        search: debouncedSearch,
        group_id: groupId,
        cathode_type: cathode,
        process,
        date_from: dateFrom,
        date_to: dateTo,
      }),
    [debouncedSearch, groupId, cathode, process, dateFrom, dateTo, creating],
  )

  return (
    <main className="page">
      <div className="page-head">
        <div>
          <h1>셀 라이브러리</h1>
          <div className="sub">
            날짜·양극재·공정·C-rate 로 좁혀 보고, 그룹으로 묶어 비교합니다.
          </div>
        </div>
        <span className="spacer" />
        <NewSampleButton groups={groups.data ?? []} onCreated={() => setCreating((v) => !v)} />
      </div>

      <div className="split">
        <div className="col" style={{ gap: 14 }}>
          <Card title="필터" tight>
            <div className="grid cols-3" style={{ padding: 12, gap: 10 }}>
              <Field label="검색" hint="이름·양극재·메모">
                <input
                  type="text"
                  value={search}
                  onChange={(event) => setSearch(event.target.value)}
                  placeholder="No_1_dry…"
                />
              </Field>
              <Field label="그룹">
                <select
                  value={groupId ?? ''}
                  onChange={(event) =>
                    setGroupId(event.target.value ? Number(event.target.value) : null)
                  }
                >
                  <option value="">전체</option>
                  {groups.data?.map((group) => (
                    <option key={group.id} value={group.id}>
                      {group.name}
                    </option>
                  ))}
                </select>
              </Field>
              <Field label="양극재">
                <select value={cathode} onChange={(event) => setCathode(event.target.value)}>
                  <option value="">전체</option>
                  {facets.data?.cathode_type.map((value) => (
                    <option key={value} value={value}>
                      {value}
                    </option>
                  ))}
                </select>
              </Field>
              <Field label="공정">
                <select value={process} onChange={(event) => setProcess(event.target.value)}>
                  <option value="">전체</option>
                  {facets.data?.process.map((value) => (
                    <option key={value} value={value}>
                      {value}
                    </option>
                  ))}
                </select>
              </Field>
              <Field label="시작일">
                <input
                  type="date"
                  value={dateFrom}
                  onChange={(event) => setDateFrom(event.target.value)}
                />
              </Field>
              <Field label="종료일">
                <input
                  type="date"
                  value={dateTo}
                  onChange={(event) => setDateTo(event.target.value)}
                />
              </Field>
            </div>
          </Card>

          <Card title={`셀 ${samples.data?.length ?? 0}개`} tight>
            {samples.error ? (
              <div style={{ padding: 14 }}>
                <Alert kind="error">{samples.error}</Alert>
              </div>
            ) : samples.loading && !samples.data ? (
              <div style={{ padding: 20 }}>
                <Spinner />
              </div>
            ) : samples.data?.length ? (
              <SampleTable samples={samples.data} />
            ) : (
              <Empty title="조건에 맞는 셀이 없습니다">
                필터를 넓히거나 <Link to="/upload">파일을 올려</Link> 주세요.
              </Empty>
            )}
          </Card>
        </div>

        <Card title="그룹">
          <GroupManager onChanged={() => setCreating((v) => !v)} />
        </Card>
      </div>
    </main>
  )
}

function SampleTable({ samples }: { samples: Sample[] }) {
  return (
    <div className="table-wrap" style={{ maxHeight: 'none' }}>
      <table>
        <thead>
          <tr>
            <th>셀</th>
            <th style={{ textAlign: 'left' }}>그룹</th>
            <th>날짜</th>
            <th style={{ textAlign: 'left' }}>양극재</th>
            <th>활물질 (mg)</th>
            <th>면적 (cm²)</th>
            <th>로딩 (mg/cm²)</th>
            <th>C-rate</th>
            <th>온도</th>
            <th>파일</th>
            <th>사이클</th>
          </tr>
        </thead>
        <tbody>
          {samples.map((sample) => {
            const cell = sample.resolved_cell
            return (
              <tr key={sample.id}>
                <td className="text">
                  <Link to={`/samples/${sample.id}`}>{sample.name}</Link>
                </td>
                <td className="text dim">{sample.group_name ?? '—'}</td>
                <td>{sample.test_date ?? '—'}</td>
                <td className="text dim">
                  {sample.cathode_detail || sample.cathode_type || '—'}
                </td>
                <td>{cell.active_mass_g ? num(cell.active_mass_g * 1000) : '—'}</td>
                <td>{num(cell.area_cm2)}</td>
                <td>{num(cell.loading_mg_cm2, 3)}</td>
                <td>{sample.c_rate ? `${sample.c_rate}C` : '—'}</td>
                <td>{sample.temperature_c !== null ? `${sample.temperature_c}°C` : '—'}</td>
                <td>{sample.run_count}</td>
                <td>{sample.cycle_count}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

function GroupManager({ onChanged }: { onChanged: () => void }) {
  const groups = useAsync(() => api.listGroups(), [])
  const [name, setName] = useState('')
  const [error, setError] = useState<string | null>(null)

  async function create() {
    if (!name.trim()) return
    try {
      await api.createGroup({ name: name.trim() })
      setName('')
      setError(null)
      groups.reload()
      onChanged()
    } catch (cause) {
      setError(String(cause instanceof Error ? cause.message : cause))
    }
  }

  return (
    <div className="col" style={{ gap: 10 }}>
      {error ? <Alert kind="error">{error}</Alert> : null}
      <div className="row">
        <input
          type="text"
          value={name}
          placeholder="새 그룹 이름"
          onChange={(event) => setName(event.target.value)}
          onKeyDown={(event) => event.key === 'Enter' && create()}
        />
        <button type="button" className="primary sm" onClick={create}>
          추가
        </button>
      </div>
      {groups.data?.length ? (
        <div className="col" style={{ gap: 6 }}>
          {groups.data.map((group) => (
            <div key={group.id} className="row" style={{ justifyContent: 'space-between' }}>
              <span>{group.name}</span>
              <span className="tiny faint">
                셀 {group.sample_count} · 파일 {group.run_count}
              </span>
            </div>
          ))}
        </div>
      ) : (
        <div className="tiny faint">아직 그룹이 없습니다.</div>
      )}
    </div>
  )
}

function NewSampleButton({
  groups,
  onCreated,
}: {
  groups: { id: number; name: string }[]
  onCreated: () => void
}) {
  const [open, setOpen] = useState(false)
  const [name, setName] = useState('')
  const [groupId, setGroupId] = useState<number | null>(null)
  const [error, setError] = useState<string | null>(null)

  if (!open) {
    return (
      <button type="button" className="primary" onClick={() => setOpen(true)}>
        셀 추가
      </button>
    )
  }

  return (
    <div className="row">
      <input
        type="text"
        autoFocus
        value={name}
        placeholder="셀 이름"
        onChange={(event) => setName(event.target.value)}
        style={{ width: 200 }}
      />
      <select
        value={groupId ?? ''}
        onChange={(event) => setGroupId(event.target.value ? Number(event.target.value) : null)}
        style={{ width: 150 }}
      >
        <option value="">그룹 없음</option>
        {groups.map((group) => (
          <option key={group.id} value={group.id}>
            {group.name}
          </option>
        ))}
      </select>
      <button
        type="button"
        className="primary"
        onClick={async () => {
          try {
            await api.createSample({ name, group_id: groupId })
            setName('')
            setOpen(false)
            setError(null)
            onCreated()
          } catch (cause) {
            setError(String(cause instanceof Error ? cause.message : cause))
          }
        }}
      >
        만들기
      </button>
      <button type="button" className="ghost" onClick={() => setOpen(false)}>
        취소
      </button>
      {error ? <span className="tiny" style={{ color: 'var(--danger)' }}>{error}</span> : null}
    </div>
  )
}
