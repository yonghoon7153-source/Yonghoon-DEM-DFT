/** The cell library: filter by date, cathode, process, C-rate; manage groups. */

import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { DeleteSampleButton } from '../components/DeleteSample'
import { GroupFilterFields, groupPath, useGroupChoice } from '../components/GroupFilter'
import { Alert, Card, Empty, Field, Spinner, TrashIcon } from '../components/ui'
import { api } from '../lib/api'
import { num } from '../lib/format'
import { useAsync, useDebounced, useStickyState } from '../lib/hooks'
import type { Group, Sample } from '../lib/types'

export function Library() {
  const [search, setSearch] = useState('')
  const [cathode, setCathode] = useState('')
  const [process, setProcess] = useState('')
  const [dateFrom, setDateFrom] = useState('')
  const [dateTo, setDateTo] = useState('')
  // 목록을 다시 읽게 하는 토큰.  셀을 새로 만들 때도, 지울 때도 뒤집는다 —
  // 지우고 나서 목록이 그대로면 사라진 셀이 계속 보이고, 눌러 보면 404 다.
  const [reloadKey, bumpReload] = useState(false)
  const [groupBy, setGroupBy] = useStickyState<GroupKey>('workbench.libraryGroupBy', 'none')
  // 작성자도 같은 자리에서 거른다.  서버에 보내면 고른 순간 선택지가 그 하나로
  // 줄어서 다른 사람 것으로 옮겨 갈 수가 없다.
  const [owner, setOwner] = useState('')

  const debouncedSearch = useDebounced(search)
  const group = useGroupChoice(reloadKey)
  const facets = useAsync(() => api.facets(), [], { live: true })
  const samples = useAsync(
    () =>
      api.listSamples({
        search: debouncedSearch,
        group_id: group.effective,
        cathode_type: cathode,
        process,
        date_from: dateFrom,
        date_to: dateTo,
      }),
    [debouncedSearch, group.effective, cathode, process, dateFrom, dateTo, reloadKey],
  )

  // 브라우저에 남아 있던 옛 선택('이름 묶음')을 걸러 낸다.  없어진 값이 그대로
  // 살아 있으면 묶기 줄에 아무 버튼도 안 켜지고, 표는 이유 없이 한 덩어리가
  // 된다 -- 화면은 멀쩡해 보이는데 아무도 그렇게 고른 적이 없다.
  const groupKey: GroupKey =
    GROUP_KEYS.some(([value]) => value === groupBy) ? groupBy : 'none'

  const owners = useMemo(() => {
    const seen = new Set<string>()
    for (const item of samples.data ?? []) {
      if (item.created_by) seen.add(item.created_by)
    }
    return [...seen].sort((a, b) => a.localeCompare(b, 'ko'))
  }, [samples.data])

  const shown = useMemo(
    () => (samples.data ?? []).filter((item) => !owner || item.created_by === owner),
    [samples.data, owner],
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
        <NewSampleButton groups={group.groups} onCreated={() => bumpReload((v) => !v)} />
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
              <Field label="작성자" hint="누가 올린 셀인가">
                <select
                  aria-label="작성자"
                  value={owner}
                  onChange={(event) => setOwner(event.target.value)}
                >
                  <option value="">전체</option>
                  {owners.map((value) => (
                    <option key={value} value={value}>
                      {value}
                    </option>
                  ))}
                </select>
              </Field>
              <GroupFilterFields pick={group} />
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
            title={`셀 ${shown.length}개`}
            actions={
              <div className="row" style={{ gap: 6 }}>
                <span className="tiny faint">묶기</span>
                <div className="segmented">
                  {GROUP_KEYS.map(([value, label]) => (
                    <button
                      key={value}
                      type="button"
                      className={groupKey === value ? 'on' : ''}
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
            ) : shown.length ? (
              <SampleTable
                samples={shown}
                groupBy={groupKey}
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
  // 누가 올린 셀인가.  한 서버를 여럿이 쓰면 표에서 남의 셀과 내 셀이 섞이고,
  // 이름만 보고는 알 수 없다 (ADR 0012 — 이름은 기록이지 신원 확인이 아니다).
  ['owner', '작성자'],
  ['cathode', '양극재'],
  ['process', '공정'],
  ['temperature', '온도'],
]

type GroupKey = 'none' | 'group' | 'owner' | 'cathode' | 'process' | 'temperature'

/** 이 셀이 어느 묶음에 속하는가.  "" 는 값이 없다는 뜻이고, 그 묶음은 맨
 *  아래로 내린다 — 비어 있는 것이 목록의 첫인상이 되면 안 된다. */
function bucketOf(sample: Sample, key: GroupKey): string {
  switch (key) {
    case 'group':
      return groupPath(sample.group_name, sample.group_parent_name)
    case 'owner':
      return sample.created_by ?? ''
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
                  {/* 가로 스크롤에 붙는 것은 이 span 이다 — 칸 자체는 표 전체
                      폭이라 붙잡을 여지가 없다 (app.css 의 .section-label). */}
                  <span className="section-label">
                    {key || <span className="faint">미입력</span>}
                    <span className="faint"> · {rows.length}개</span>
                  </span>
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
        {/* 누가 올렸나.  한 서버를 여럿이 쓰면 이것이 첫 번째 거르개다. */}
        <th style={{ textAlign: 'left' }}>작성자</th>
        {/* 그룹이 소그룹이면 "부모 · 자식" 으로 (ADR 0025).  자식 이름만 쓰면
            '80wt%' 같은 이름이 여러 실험에 있어 어느 것인지 알 수 없다. */}
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
        {/* 임피던스가 있다/없다조차 이 표에서는 안 보였다.  저항 하나가
            붙으면 셀끼리 바로 견줄 수 있고, 비어 있는 것도 뜻이 된다. */}
        <th>임피던스 (Ω)</th>
        {/* 이름 없는 칸.  머리에 '삭제' 라고 적으면 표를 훑을 때 그 글자가
            먼저 읽힌다 — 이 표는 셀을 찾으러 오는 곳이지 지우러 오는 곳이 아니다. */}
        <th />
      </tr>
    </thead>
  )
}

/** 구분 줄이 걸치는 칸 수.  SampleHead 의 <th> 개수와 같아야 한다. */
const COLUMN_COUNT = 16

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
      <td className="text dim">{sample.created_by || '—'}</td>
      <td className="text dim">
        {groupPath(sample.group_name, sample.group_parent_name) || '—'}
      </td>
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
      {/* 셋을 가른다: 안 쟀다(—) · 쟀는데 안 맞췄다(N개 · 안 맞춤) · 맞췄다(값).
          가운데를 '—' 로 뭉뚱그리면 다음에 할 일이 안 보인다. */}
      <td className={sample.impedance_ohm != null ? 'headline' : 'dim'}>
        {sample.impedance_ohm != null
          ? num(sample.impedance_ohm, 4)
          : sample.spectrum_count
            ? <span className="tiny">{sample.spectrum_count}개 · 안 맞춤</span>
            : '—'}
      </td>
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
  //: 새 그룹을 어디에 만드는가.  `null` 이면 최상위, 아니면 그 그룹의 소그룹.
  //  소그룹을 만들 자리가 여기밖에 없으면 안 되므로 업로드 화면에도 넣었지만,
  //  정리하는 자리는 여기다 (ADR 0025).
  const [parentId, setParentId] = useState<number | null>(null)
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
      await api.createGroup({
        name: name.trim(),
        ...(parentId === null ? {} : { parent_id: parentId }),
      })
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
        <select
          aria-label="어디에 만들까"
          value={parentId ?? ''}
          style={{ width: 150 }}
          onChange={(event) =>
            setParentId(event.target.value ? Number(event.target.value) : null)}
        >
          <option value="">최상위 그룹으로</option>
          {(groups.data ?? []).filter((group) => !group.parent_id).map((group) => (
            <option key={group.id} value={group.id}>{group.name} 아래</option>
          ))}
        </select>
        <button type="button" className="primary sm" onClick={create}>
          추가
        </button>
      </div>
      {groups.data?.length ? (
        <div className="col" style={{ gap: 6 }}>
          {treeOrder(groups.data).map((group) => (
            <div key={group.id} className="row"
                 style={{ justifyContent: 'space-between',
                          paddingLeft: group.parent_id ? 14 : 0 }}>
              <span>
                {group.parent_id ? <span className="faint">↳ </span> : null}
                {group.name}
                {group.subgroup_count
                  ? <span className="tiny faint"> · 소그룹 {group.subgroup_count}</span>
                  : null}
              </span>
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
                    title="그룹만 지웁니다. 안에 있던 셀과 소그룹은 남습니다."
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

/** 부모 바로 뒤에 그 자식들.  두 단계뿐이라 재귀가 필요 없다 (ADR 0025). */
function treeOrder(groups: Group[]): Group[] {
  const out: Group[] = []
  for (const group of groups.filter((item) => !item.parent_id)) {
    out.push(group)
    out.push(...groups.filter((item) => item.parent_id === group.id))
  }
  // 부모가 사라진 소그룹은 서버가 최상위로 올리므로 보통 없지만, 목록에서
  // 조용히 빠지는 것보다는 끝에라도 보이는 편이 낫다.
  out.push(...groups.filter((item) => !out.includes(item)))
  return out
}

function NewSampleButton({
  groups,
  onCreated,
}: {
  groups: Group[]
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
        {treeOrder(groups).map((group) => (
          <option key={group.id} value={group.id}>
            {groupPath(group.name, group.parent_name)}
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
