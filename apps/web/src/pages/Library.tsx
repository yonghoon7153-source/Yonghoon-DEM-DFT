/** The cell library: filter by date, cathode, process, C-rate; manage groups. */

import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { DeleteSampleButton } from '../components/DeleteSample'
import { Alert, Card, Empty, Field, Spinner, TrashIcon } from '../components/ui'
import { api } from '../lib/api'
import { nameFamily, num } from '../lib/format'
import { useAsync, useDebounced, useStickyState } from '../lib/hooks'
import type { Sample } from '../lib/types'

export function Library() {
  const [search, setSearch] = useState('')
  const [groupId, setGroupId] = useState<number | null>(null)
  const [cathode, setCathode] = useState('')
  const [process, setProcess] = useState('')
  const [dateFrom, setDateFrom] = useState('')
  const [dateTo, setDateTo] = useState('')
  // 목록을 다시 읽게 하는 토큰.  셀을 새로 만들 때도, 지울 때도 뒤집는다 —
  // 지우고 나서 목록이 그대로면 사라진 셀이 계속 보이고, 눌러 보면 404 다.
  const [reloadKey, bumpReload] = useState(false)
  const [groupBy, setGroupBy] = useStickyState<GroupKey>('workbench.libraryGroupBy', 'none')

  const debouncedSearch = useDebounced(search)
  const groups = useAsync(() => api.listGroups(), [reloadKey], { live: true })
  const facets = useAsync(() => api.facets(), [], { live: true })
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
    [debouncedSearch, groupId, cathode, process, dateFrom, dateTo, reloadKey],
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
        <NewSampleButton groups={groups.data ?? []} onCreated={() => bumpReload((v) => !v)} />
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

          <Card
            title={`셀 ${samples.data?.length ?? 0}개`}
            actions={
              <div className="row" style={{ gap: 6 }}>
                <span className="tiny faint">묶기</span>
                <div className="segmented">
                  {GROUP_KEYS.map(([value, label]) => (
                    <button
                      key={value}
                      type="button"
                      className={groupBy === value ? 'on' : ''}
                      onClick={() => setGroupBy(value)}
                    >
                      {label}
                    </button>
                  ))}
                </div>
              </div>
            }
            tight
          >
            {samples.error ? (
              <div style={{ padding: 14 }}>
                <Alert kind="error">{samples.error}</Alert>
              </div>
            ) : samples.loading && !samples.data ? (
              <div style={{ padding: 20 }}>
                <Spinner />
              </div>
            ) : samples.data?.length ? (
              <SampleTable
                samples={samples.data}
                groupBy={groupBy}
                onDeleted={() => bumpReload((v) => !v)}
              />
            ) : (
              <Empty title="조건에 맞는 셀이 없습니다">
                필터를 넓히거나 <Link to="/upload">파일을 올려</Link> 주세요.
              </Empty>
            )}
          </Card>
        </div>

        <Card title="그룹">
          <GroupManager onChanged={() => bumpReload((v) => !v)} />
        </Card>
      </div>
    </main>
  )
}

/** 무엇으로 묶을 수 있는가.
 *
 * 그룹은 사람이 만들어 붙이는 것이고, 나머지는 이미 셀에 적혀 있는 것이다.
 * 그룹을 만들기 전에도 "같은 조건 세 번 돌린 것" 을 나란히 보고 싶은 것이
 * 실제 요구라서, 이름으로 묶는 길을 열어 둔다.
 */
const GROUP_KEYS: [GroupKey, string][] = [
  ['none', '없음'],
  ['group', '그룹'],
  ['name', '이름'],
  ['cathode', '양극재'],
  ['process', '공정'],
  ['temperature', '온도'],
]

type GroupKey = 'none' | 'group' | 'name' | 'cathode' | 'process' | 'temperature'

/** 이 셀이 어느 묶음에 속하는가.  "" 는 값이 없다는 뜻이고, 그 묶음은 맨
 *  아래로 내린다 — 비어 있는 것이 목록의 첫인상이 되면 안 된다. */
function bucketOf(sample: Sample, key: GroupKey): string {
  switch (key) {
    case 'group':
      return sample.group_name ?? ''
    case 'name':
      return nameFamily(sample.name)
    case 'cathode':
      return sample.cathode_detail || sample.cathode_type || ''
    case 'process':
      return sample.process || ''
    case 'temperature':
      return sample.temperature_c === null ? '' : `${sample.temperature_c}°C`
    default:
      return ''
  }
}

function SampleTable({
  samples,
  groupBy,
  onDeleted,
}: {
  samples: Sample[]
  groupBy: GroupKey
  onDeleted: () => void
}) {
  // 실패는 표 바깥에 한 번만 그린다.  행 안에 끼우면 열이 밀리고, 묶은 표에서는
  // 구분 줄까지 함께 밀린다.
  const [deleteError, setDeleteError] = useState<string | null>(null)
  const sections = useMemo(() => {
    if (groupBy === 'none') return null
    const buckets = new Map<string, Sample[]>()
    for (const sample of samples) {
      const key = bucketOf(sample, groupBy)
      const bucket = buckets.get(key)
      if (bucket) bucket.push(sample)
      else buckets.set(key, [sample])
    }
    // 값이 없는 묶음은 맨 아래.  나머지는 이름순 — 새로 올린 셀이 목록을
    // 흔들지 않게 하려면 순서가 내용에만 달려 있어야 한다.
    return [...buckets.entries()].sort(([a], [b]) => {
      if (!a) return 1
      if (!b) return -1
      return a.localeCompare(b, 'ko')
    })
  }, [samples, groupBy])

  const row = (sample: Sample) => (
    <SampleRow
      key={sample.id}
      sample={sample}
      onDeleted={onDeleted}
      onError={setDeleteError}
    />
  )
  const failure = deleteError ? (
    <div style={{ padding: '10px 14px 0' }}>
      <Alert kind="error">{deleteError}</Alert>
    </div>
  ) : null

  if (sections) {
    return (
      <div className="table-wrap pin-first" style={{ maxHeight: 'none' }}>
        <table>
          <SampleHead />
          {sections.map(([key, rows]) => (
            <tbody key={key || '(none)'}>
              <tr className="section">
                <th colSpan={COLUMN_COUNT}>
                  {key || <span className="faint">미입력</span>}
                  <span className="faint"> · {rows.length}개</span>
                </th>
              </tr>
              {rows.map(row)}
            </tbody>
          ))}
        </table>
        {failure}
      </div>
    )
  }

  return (
    <div className="table-wrap pin-first" style={{ maxHeight: 'none' }}>
      <table>
        <SampleHead />
        <tbody>{samples.map(row)}</tbody>
      </table>
      {failure}
    </div>
  )
}

/** 표의 머리.  묶은 표와 안 묶은 표가 같은 열을 쓰도록 한 곳에만 적는다 —
 *  둘로 갈라 두면 열을 하나 추가할 때 한쪽만 고치게 되고, 그러면 묶기를 켰을
 *  때만 헤더와 데이터가 한 칸씩 밀린다. */
function SampleHead() {
  return (
    <thead>
      <tr>
        <th>셀</th>
        <th style={{ textAlign: 'left' }}>그룹</th>
        <th>날짜</th>
        <th style={{ textAlign: 'left' }}>양극재</th>
        <th style={{ textAlign: 'left' }}>공정</th>
        <th style={{ textAlign: 'left' }}>조성</th>
        <th>활물질 (mg)</th>
        <th>면적 (cm²)</th>
        <th>로딩 (mg/cm²)</th>
        {/* 형성과 본 사이클은 다른 실험 조건이다.  한 칸에 하나만 보이면
            "0.1C 로 돌린 셀" 이 형성 0.1C 인지 본 사이클 0.1C 인지 알 수 없고,
            둘은 전혀 다른 시험이다. */}
        <th>C-rate (형성/본)</th>
        <th>온도</th>
        <th>파일</th>
        <th>사이클</th>
        {/* 이름 없는 칸.  머리에 '삭제' 라고 적으면 표를 훑을 때 그 글자가
            먼저 읽힌다 — 이 표는 셀을 찾으러 오는 곳이지 지우러 오는 곳이 아니다. */}
        <th />
      </tr>
    </thead>
  )
}

/** 구분 줄이 걸치는 칸 수.  SampleHead 의 <th> 개수와 같아야 한다. */
const COLUMN_COUNT = 14

function SampleRow({
  sample,
  onDeleted,
  onError,
}: {
  sample: Sample
  onDeleted: () => void
  onError: (message: string | null) => void
}) {
  const cell = sample.resolved_cell
  return (
    <tr>
      <td className="text">
        <Link to={`/samples/${sample.id}`}>{sample.name}</Link>
      </td>
      <td className="text dim">{sample.group_name ?? '—'}</td>
      <td>{sample.test_date ?? '—'}</td>
      <td className="text dim">{sample.cathode_detail || sample.cathode_type || '—'}</td>
      <td className="text dim">{sample.process || '—'}</td>
      <td className="text dim tiny">{cell.composition_compact_label || '—'}</td>
      <td>{cell.active_mass_g ? num(cell.active_mass_g * 1000) : '—'}</td>
      <td>{num(cell.area_cm2)}</td>
      <td>{num(cell.loading_mg_cm2, 3)}</td>
      <td className="nowrap">
        {sample.c_rate || sample.c_rate_formation ? (
          <>
            <span className={sample.c_rate_formation ? '' : 'faint'}>
              {sample.c_rate_formation ? `${sample.c_rate_formation}C` : '—'}
            </span>
            <span className="faint"> / </span>
            <span className={sample.c_rate ? '' : 'faint'}>
              {sample.c_rate ? `${sample.c_rate}C` : '—'}
            </span>
          </>
        ) : (
          '—'
        )}
      </td>
      <td>{sample.temperature_c !== null ? `${sample.temperature_c}°C` : '—'}</td>
      <td>{sample.run_count}</td>
      <td>{sample.cycle_count}</td>
      <td style={{ whiteSpace: 'nowrap' }}>
        <DeleteSampleButton
          sampleId={sample.id}
          sampleName={sample.name}
          onDeleted={onDeleted}
          onError={onError}
        />
      </td>
    </tr>
  )
}

function GroupManager({ onChanged }: { onChanged: () => void }) {
  const groups = useAsync(() => api.listGroups(), [])
  const [name, setName] = useState('')
  const [error, setError] = useState<string | null>(null)
  // 그룹을 지우면 그 안의 셀은 남고 "그룹 없음" 이 된다 (FK 는 SET NULL 이 아니라
  // 모델이 nullable 이다). 그래도 한 번 눌러 사라지면 안 되므로 확인을 받는다.
  const [confirming, setConfirming] = useState<number | null>(null)
  const [busy, setBusy] = useState(false)

  async function remove(id: number) {
    setBusy(true)
    try {
      setError(null)
      await api.deleteGroup(id)
      setConfirming(null)
      groups.reload()
      onChanged()
    } catch (cause) {
      setError(String(cause instanceof Error ? cause.message : cause))
      setConfirming(null)
    } finally {
      setBusy(false)
    }
  }

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
              <span className="row tiny faint" style={{ gap: 8, alignItems: 'center' }}>
                셀 {group.sample_count} · 파일 {group.run_count}
                {confirming === group.id ? (
                  <>
                    <button
                      type="button"
                      className="danger tiny"
                      disabled={busy}
                      onClick={() => void remove(group.id)}
                    >
                      지웁니다
                    </button>
                    <button
                      type="button"
                      className="ghost tiny"
                      disabled={busy}
                      onClick={() => setConfirming(null)}
                    >
                      취소
                    </button>
                  </>
                ) : (
                  <button
                    type="button"
                    className="ghost icon"
                    aria-label={`${group.name} 그룹 지우기`}
                    title="그룹만 지웁니다. 안에 있던 셀은 남고 그룹 없음이 됩니다."
                    onClick={() => {
                      setError(null)
                      setConfirming(group.id)
                    }}
                  >
                    <TrashIcon size={13} />
                  </button>
                )}
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
