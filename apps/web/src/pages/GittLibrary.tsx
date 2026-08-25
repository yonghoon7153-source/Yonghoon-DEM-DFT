/** GITT 라이브러리 — 기록이 한 줄씩.
 *
 *  대시보드는 **셀**이 한 줄이고 여기는 **기록**이 한 줄이다.  올리는 일은
 *  전용 화면이 가져갔고, 대신 여기에는 셀에 붙이는 길이 있다: 파일부터 올려
 *  두고 나중에 셀을 만드는 순서가 흔해서, 붙이는 일이 목록에서 바로 되어야
 *  한다 (ADR 0020).
 */

import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { dateTime, num } from '../lib/format'
import { useAsync } from '../lib/hooks'

export function GittLibrary() {
  const [search, setSearch] = useState('')
  const [owner, setOwner] = useState('')
  const [reloadKey, bumpReload] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const runs = useAsync(() => api.listGittRuns({ search: search || undefined }),
                        [search, reloadKey], { live: true })
  const samples = useAsync(() => api.listSamples(), [reloadKey])
  const rows = useMemo(() => {
    const all = runs.data ?? []
    // '' 는 "안 붙임" 을 뜻하는 값이라 전체(null)와 구별해야 한다.
    if (owner === '') return all
    if (owner === 'none') return all.filter((run) => !run.sample_id)
    return all.filter((run) => String(run.sample_id) === owner)
  }, [runs.data, owner])

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

      <Card
        title={`GITT 기록 ${rows.length}개`}
        actions={
          <div className="row" style={{ gap: 6 }}>
            <Field label="셀">
              <select
                aria-label="셀"
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
            <Field label="검색">
              <input
                aria-label="검색"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="이름 또는 파일명"
              />
            </Field>
          </div>
        }
        tight
      >
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
                  <th style={{ textAlign: 'left' }}>셀</th>
                  <th>펄스</th>
                  <th>점</th>
                  <th>기간</th>
                  <th style={{ textAlign: 'left' }}>확산계수</th>
                  <th>올린 때</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((run) => (
                  <tr key={run.id}>
                    <td className="text">
                      <Link to={`/gitt/${run.id}`}>{run.name}</Link>
                      {run.pulse_note ? (
                        <span className="tiny warn" title={run.pulse_note}> !</span>
                      ) : null}
                    </td>
                    <td className="text">
                      <select
                        aria-label={`${run.name} 셀`}
                        value={run.sample_id ? String(run.sample_id) : ''}
                        onChange={(event) => void attach(run.id, event.target.value)}
                      >
                        <option value="">— 안 붙임</option>
                        {(samples.data ?? []).map((sample) => (
                          <option key={sample.id} value={sample.id}>{sample.name}</option>
                        ))}
                      </select>
                    </td>
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
