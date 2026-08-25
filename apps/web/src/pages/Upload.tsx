/** Drop .wrd files, attach them to a cell, and see what the instrument said. */

import { useCallback, useState } from 'react'
import { Link } from 'react-router-dom'

import { DropZone, UploadTargetFields, useUploadTarget } from '../components/UploadTarget'
import { Alert, Card, Empty, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { bytes, dateTime, num } from '../lib/format'
import { useAsync } from '../lib/hooks'
import type { Run } from '../lib/types'

interface Result {
  file: string
  run?: Run
  error?: string
}

export function Upload() {
  const [busy, setBusy] = useState(false)
  const [results, setResults] = useState<Result[]>([])

  // 그룹 · 새 셀 · 기존 셀 · 파일 이름을 셀 이름으로 — 세 업로드 화면이 같은
  // 부품을 쓴다 (ADR 0024).  같은 일을 세 번 적어 두면 한 번 고칠 때 두 곳이
  // 남는다.
  const pick = useUploadTarget(results.length)
  const orphans = useAsync(() => api.listRuns({ unassigned: true }), [results.length],
                         { live: true })

  const send = useCallback(
    async (files: FileList | File[]) => {
      const list = [...files]
      if (!list.length) return
      setBusy(true)
      try {
        const plan = await pick.planFor(list)
        for (const [index, file] of list.entries()) {
          try {
            const run = await api.uploadRun(file, plan[index] ?? null)
            setResults((current) => [{ file: file.name, run }, ...current])
          } catch (cause) {
            setResults((current) => [{
              file: file.name,
              error: String(cause instanceof Error ? cause.message : cause),
            }, ...current])
          }
        }
      } catch (cause) {
        // 셀을 만들다 실패했다.  파일은 하나도 안 올라갔으므로 그렇게 말한다.
        setResults((current) => [{
          file: '셀 만들기',
          error: String(cause instanceof Error ? cause.message : cause),
        }, ...current])
      } finally {
        setBusy(false)
      }
    },
    [pick],
  )

  return (
    <main className="page">
      <div className="page-head">
        <div>
          <h1>업로드</h1>
          <div className="sub">
            `.wrd` 를 그대로 올리면 장비 정보·스케줄·전 사이클을 한 번에 읽습니다.
            같은 파일을 다시 올려도 중복되지 않습니다.
          </div>
        </div>
      </div>

      <div className="split">
        <div className="col" style={{ gap: 14 }}>
          <Card title="파일 선택" tight>
            <div style={{ padding: 14 }}>
              <UploadTargetFields pick={pick} />

              <DropZone
                accept=".wrd"
                label="여기에 .wrd 파일을 끌어다 놓으세요"
                onFiles={send}
              />

              {busy ? (
                <div style={{ marginTop: 12 }}>
                  <Spinner label="파싱 중 — 20 MB 파일도 몇 초면 끝납니다" />
                </div>
              ) : null}
            </div>
          </Card>

          {results.length ? (
            <Card title="업로드 결과" tight>
              <div className="col" style={{ padding: 14, gap: 12 }}>
                {results.map((result, index) => (
                  <UploadResult key={`${result.file}-${index}`} result={result} />
                ))}
              </div>
            </Card>
          ) : null}
        </div>

        <Card
          title={`연결 안 된 파일 · ${orphans.error ? '—' : `${orphans.data?.length ?? 0}개`}`}
          tight
        >
          <div style={{ padding: 14 }}>
            {/* "모두 연결되어 있습니다" is an assertion; a failed fetch knows
                nothing of the kind, and hiding the error behind it sends the
                operator away from files that never made it into a cell. */}
            {orphans.error ? (
              <Alert kind="error">{orphans.error}</Alert>
            ) : orphans.loading && !orphans.data ? (
              <Spinner />
            ) : orphans.data?.length ? (
              <div className="col" style={{ gap: 12 }}>
                {orphans.data.map((run) => (
                  <OrphanRun
                    key={run.id}
                    run={run}
                    samples={pick.samples}
                    onAttached={() => orphans.reload()}
                  />
                ))}
              </div>
            ) : (
              <Empty title="모두 연결되어 있습니다" />
            )}
          </div>
        </Card>
      </div>
    </main>
  )
}

function UploadResult({ result }: { result: Result }) {
  if (result.error) {
    return (
      <Alert kind="error">
        <strong>{result.file}</strong> — {result.error}
      </Alert>
    )
  }
  const run = result.run
  if (!run) return null
  const schedule = run.schedule ?? {}
  return (
    <div className="col" style={{ gap: 4 }}>
      <div className="row">
        <strong>{run.original_name}</strong>
        <span className="badge finished">읽음</span>
        {run.sample_name ? (
          <Link className="tiny" to={`/samples/${run.sample_id}`}>
            {run.sample_name} 으로
          </Link>
        ) : (
          <span className="badge warn">셀 미연결</span>
        )}
      </div>
      <div className="small dim">
        {run.device_model} · S/N {run.serial_no} · ch{run.channel} · {bytes(run.size_bytes)}
      </div>
      <div className="small dim mono">
        {/* 화면 한 줄을 그리다 페이지 전체를 날리지 않는다.  파싱이 실패한 run 은
            이 숫자들이 비어 있을 수 있는데, 그때 보여 줘야 할 것은 바로 그
            실패다 — 빈 화면이 아니라. */}
        {(run.row_count ?? 0).toLocaleString()} 샘플 · {run.complete_cycle_count ?? 0}/
        {run.cycle_count ?? 0}{' '}
        사이클 · {dateTime(run.start_time)} → {dateTime(run.end_time)}
      </div>
      {schedule.upper_cutoff_v ? (
        <div className="small dim">
          스케줄: {schedule.lower_cutoff_v}–{schedule.upper_cutoff_v} V
          {schedule.c_rate ? ` · ${schedule.c_rate}C` : ''}
          {schedule.planned_cycles ? ` · 계획 ${schedule.planned_cycles} 사이클` : ''}
          {schedule.nominal_capacity_mah
            ? ` · 공칭 ${num(schedule.nominal_capacity_mah)} mAh`
            : ''}
        </div>
      ) : null}
      <div className="sep" />
    </div>
  )
}

function OrphanRun({
  run,
  samples,
  onAttached,
}: {
  run: Run
  samples: { id: number; name: string }[]
  onAttached: () => void
}) {
  const [confirming, setConfirming] = useState(false)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [choice, setChoice] = useState('')
  return (
    <div className="col" style={{ gap: 5 }}>
      <div className="small nowrap" title={run.original_name}>
        <strong>{run.original_name}</strong>
      </div>
      <div className="tiny dim mono">
        {run.complete_cycle_count}/{run.cycle_count} 사이클 · {dateTime(run.start_time)}
      </div>
      <select
        disabled={busy}
        value={choice}
        onChange={async (event) => {
          const value = event.target.value
          setChoice(value)
          if (!value) return
          setBusy(true)
          try {
            setError(null)
            await api.updateRun(run.id, { sample_id: Number(value) })
            onAttached()
          } catch (cause) {
            // The select would otherwise keep showing the chosen cell, which
            // reads as "attached" for a run that is still orphaned.
            setError(cause instanceof Error ? cause.message : String(cause))
            setChoice('')
          } finally {
            setBusy(false)
          }
        }}
      >
        <option value="">셀 선택…</option>
        {samples.map((sample) => (
          <option key={sample.id} value={sample.id}>
            {sample.name}
          </option>
        ))}
      </select>
      {confirming ? (
        <div className="row" style={{ gap: 6, alignItems: 'center' }}>
          <span className="tiny dim">기록에서 지웁니다. 원본 .wrd 는 남습니다.</span>
          <button
            className="danger"
            disabled={busy}
            onClick={async () => {
              setBusy(true)
              try {
                setError(null)
                await api.deleteRun(run.id)
                onAttached()
              } catch (cause) {
                setError(cause instanceof Error ? cause.message : String(cause))
                setConfirming(false)
              } finally {
                setBusy(false)
              }
            }}
          >
            지웁니다
          </button>
          <button className="ghost" disabled={busy} onClick={() => setConfirming(false)}>
            취소
          </button>
        </div>
      ) : (
        <button className="ghost tiny" onClick={() => setConfirming(true)}>
          이 파일 지우기
        </button>
      )}
      {error ? <Alert kind="error">{error}</Alert> : null}
      <div className="sep" />
    </div>
  )
}


/** 파일 이름에서 셀 이름을 만든다.

    `.wrd` 를 떼고, 뒤에 붙은 분할 번호(`_011`, `_012`)도 뗀다.  긴 실험은
    Smart Interface 가 그렇게 쪼개는데, 그 조각들은 한 셀의 이어지는 파일이지
    서로 다른 셀이 아니다 — 떼지 않으면 한 실험이 셀 두 개로 갈라진다. */
export function cellNameFor(fileName: string): string {
  const stem = fileName.replace(/\.wrd$/i, '')
  return stem.replace(/_\d{2,4}$/, '') || stem
}
