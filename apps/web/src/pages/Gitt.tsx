/** GITT — 기록 목록과 올리기.
 *
 *  충방전과 같은 `.wrd` 를 읽지만 섹션이 따로다 (ADR 0020).  충방전 도중
 *  임피던스를 재는 일은 흔하지만 GITT 를 끼우는 일은 드물어서 이어 붙일 이유가
 *  없고, 사이클링처럼 요약하면 아무 뜻 없는 사이클 수백 개가 나온다.
 */

import { useMemo, useRef, useState } from 'react'
import { Link } from 'react-router-dom'

import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { dateTime, num } from '../lib/format'
import { useAsync } from '../lib/hooks'

export function Gitt() {
  const [search, setSearch] = useState('')
  const [reloadKey, bumpReload] = useState(false)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [note, setNote] = useState<string | null>(null)
  const fileRef = useRef<HTMLInputElement>(null)

  const runs = useAsync(() => api.listGittRuns({ search: search || undefined }),
                        [search, reloadKey], { live: true })
  const rows = useMemo(() => runs.data ?? [], [runs.data])

  async function upload(files: FileList | null) {
    if (!files?.length) return
    setBusy(true)
    setError(null)
    setNote(null)
    let added = 0
    const remarks: string[] = []
    try {
      for (const file of files) {
        const made = await api.uploadGittRun(file)
        added += 1
        // 관찰을 삼키지 않는다 — 사이클링 파일을 여기 올렸다면 그 한 줄이
        // 유일한 신호다.
        if (made.pulse_note) remarks.push(`${made.name}: ${made.pulse_note}`)
      }
      setNote(`${added}개 올렸습니다`)
      if (remarks.length) setError(remarks.join('\n'))
      bumpReload((value) => !value)
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause))
    } finally {
      setBusy(false)
      if (fileRef.current) fileRef.current.value = ''
    }
  }

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>GITT</h1>
          <div className="sub">
            펄스와 휴지에서 준평형 전압 곡선(pseudo-OCV)과 확산계수를 뽑습니다
          </div>
        </div>
        <span className="spacer" />
        <div className="row">
          <input
            ref={fileRef}
            type="file"
            multiple
            accept=".wrd"
            aria-label="GITT 파일"
            onChange={(event) => void upload(event.target.files)}
            style={{ display: 'none' }}
          />
          <button type="button" className="primary" disabled={busy}
                  onClick={() => fileRef.current?.click()}>
            파일 올리기
          </button>
        </div>
      </div>

      {error ? <Alert kind="warn">{error}</Alert> : null}
      {note ? <Alert kind="info">{note}</Alert> : null}

      <Card
        title={`GITT 기록 ${rows.length}개`}
        actions={
          <Field label="검색">
            <input
              aria-label="검색"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="이름 또는 파일명"
            />
          </Field>
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
          <Empty title="아직 GITT 기록이 없습니다" icon="↑">
            Smart Interface 가 남긴 <code>.wrd</code> 를 그대로 올리면 됩니다 —
            텍스트로 내보낼 필요 없습니다.
          </Empty>
        )}
      </Card>
    </main>
  )
}
