/** GITT 라이브러리 — 기록이 한 줄씩.
 *
 *  대시보드는 **셀**이 한 줄이고 여기는 **기록**이 한 줄이다.  올리는 일은
 *  전용 화면이 가져갔고, 대신 여기에는 셀에 붙이는 길이 있다: 파일부터 올려
 *  두고 나중에 셀을 만드는 순서가 흔해서, 붙이는 일이 목록에서 바로 되어야
 *  한다 (ADR 0020).
 */

import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { GroupFilterFields, useGroupChoice } from '../components/GroupFilter'
import { DeleteMeasurementButton, RelatedCellSelect } from '../components/RelatedCell'
import { GroupTag, OwnerTag, leafOf } from '../components/RowTags'
import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { dateTime, num } from '../lib/format'
import { useAsync } from '../lib/hooks'

export function GittLibrary() {
  const [search, setSearch] = useState('')
  const [owner, setOwner] = useState('')
  const [purpose, setPurpose] = useState('')
  const [reloadKey, bumpReload] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const runs = useAsync(() => api.listGittRuns({ search: search || undefined }),
                        [search, reloadKey], { live: true })
  const samples = useAsync(() => api.listSamples(), [reloadKey])
  const group = useGroupChoice(reloadKey)

  const purposes = useMemo(() => {
    const seen = new Set<string>()
    for (const run of runs.data ?? []) if (run.purpose) seen.add(run.purpose)
    return [...seen].sort((a, b) => a.localeCompare(b, 'ko'))
  }, [runs.data])

  const inGroup = group.includes
  const rows = useMemo(() => {
    return (runs.data ?? []).filter((run) => {
      // '' 는 "안 붙임" 을 뜻하는 값이라 전체(null)와 구별해야 한다.
      if (owner === 'none' && run.sample_id) return false
      if (owner && owner !== 'none' && String(run.sample_id) !== owner) return false
      if (purpose && (run.purpose ?? '') !== purpose) return false
      // 그룹은 이제 **측정 자신의 것**이 먼저다 (ADR 0027) -- 셀에 안 붙은
      // 측정도 묶일 수 있고, `*_effective` 가 "자기 것 → 셀 것" 을 이미 편다.
      if (!inGroup(run.group_id_effective ?? null)) return false
      return true
    })
  }, [runs.data, samples.data, owner, purpose, group.effective, inGroup])

  async function attach(id: number, sampleId: string) {
    setError(null)
    try {
      // 빈 값은 떼어내기다.  `sample_id: null` 은 "안 보냄" 과 구별되지 않아
      // 서버가 clear 를 따로 받는다.
      await api.updateGittRun(id, sampleId
        ? { sample_id: Number(sampleId) }
        : { clear: ['sample_id'] })
      bumpReload((value) => !value)
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause))
    }
  }

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>GITT 라이브러리</h1>
          <div className="sub">
            기록이 한 줄씩 — 셀에 붙여 두면 대시보드와 셀 상세에서 같이 보입니다
          </div>
        </div>
      </div>

      {error ? <Alert kind="error">{error}</Alert> : null}

      {/* 거르기 줄의 모양은 셀 라이브러리를 그대로 따른다 -- 세 섹션이 서로를
          답습해야 한 번 배운 순서가 나머지 둘에서도 그대로 통한다 (ADR 0024). */}
      <Card title="필터" tight>
        <div className="grid cols-4" style={{ padding: 12, gap: 10 }}>
          <GroupFilterFields pick={group} hint="셀에 붙은 것만 남습니다" />
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
          <Field label="관계셀" hint="이 측정이 붙어 있는 충방전 셀">
            <select
              aria-label="관계셀"
              value={owner}
              onChange={(event) => setOwner(event.target.value)}
            >
              <option value="">전체</option>
              <option value="none">— 안 붙인 것</option>
              {(samples.data ?? []).map((sample) => (
                <option key={sample.id} value={sample.id}>{sample.name}</option>
              ))}
            </select>
          </Field>
          <Field label="검색" hint="이름 · 파일명">
            <input
              aria-label="검색"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="이름 또는 파일명"
            />
          </Field>
        </div>
      </Card>

      <Card title={`GITT 기록 ${rows.length}개`} tight>
        {runs.error ? (
          <Alert kind="error">{runs.error}</Alert>
        ) : runs.loading && !runs.data ? (
          <div style={{ padding: 20 }}><Spinner /></div>
        ) : rows.length ? (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left' }}>이름</th>
                  <th style={{ textAlign: 'left' }}>관계셀</th>
                  <th style={{ textAlign: 'left' }}>목적</th>
                  <th>펄스</th>
                  <th>점</th>
                  <th>기간</th>
                  <th style={{ textAlign: 'left' }}>확산계수</th>
                  <th>올린 때</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {rows.map((run) => (
                  <tr key={run.id}>
                    <td className="text">
                      {/* EIS 라이브러리와 같은 이름표 — 두 표를 나란히 놓고 보는
                          화면이라 한쪽에만 붙으면 그것이 먼저 눈에 띈다. */}
                      <GroupTag name={leafOf(run.group_label)} path={run.group_label} />
                      <OwnerTag owner={run.created_by} />
                      <Link to={`/gitt/${run.id}`}>{run.name}</Link>
                      {run.pulse_note ? (
                        <span className="tiny warn" title={run.pulse_note}> !</span>
                      ) : null}
                    </td>
                    <td className="text">
                      <div className="col" style={{ gap: 3, minWidth: 0, width: 200 }}>
                        <RelatedCellSelect
                          value={run.sample_id}
                          samples={samples.data ?? []}
                          label={`${run.name} 관계셀`}
                          onPick={(sampleId) =>
                            void attach(run.id, sampleId ? String(sampleId) : '')}
                        />
                        {run.sample_id ? (
                          <Link className="tiny truncate" to={`/samples/${run.sample_id}`}>
                            셀 화면 →
                          </Link>
                        ) : null}
                      </div>
                    </td>
                    <td className="text dim">{run.purpose || '—'}</td>
                    <td>{run.n_pulses}</td>
                    <td>{run.n_points}</td>
                    <td className="dim">
                      {run.duration_h === null ? '—' : `${num(run.duration_h, 3)} h`}
                    </td>
                    <td className="text dim">
                      {run.missing_for_diffusion.length
                        // 무엇이 없어서 못 내는지가 곧 다음에 할 일이다.
                        ? `${run.missing_for_diffusion.length}개 부족`
                        : '가능'}
                    </td>
                    <td className="dim">{dateTime(run.uploaded_at)}</td>
                    <td>
                      {/* 붙어 있어도 지울 수 있다.  원본 `.wrd` 는 남는다. */}
                      <DeleteMeasurementButton
                        name={run.name}
                        onError={setError}
                        onDelete={async () => {
                          await api.deleteGittRun(run.id)
                          bumpReload((value) => !value)
                        }}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <Empty title="해당하는 기록이 없습니다" icon="↯">
            <Link to="/gitt/upload">업로드</Link>에서 Smart Interface 의{' '}
            <code>.wrd</code> 를 그대로 올리면 됩니다.
          </Empty>
        )}
      </Card>
    </main>
  )
}
