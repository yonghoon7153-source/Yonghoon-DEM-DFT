/** Drop .wrd files, attach them to a cell, and see what the instrument said. */

import { useCallback, useRef, useState } from 'react'
import { Link } from 'react-router-dom'

import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
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
  const [over, setOver] = useState(false)
  const [busy, setBusy] = useState(false)
  const [results, setResults] = useState<Result[]>([])
  const [targetSample, setTargetSample] = useState<number | null>(null)
  const [newSampleName, setNewSampleName] = useState('')
  const inputRef = useRef<HTMLInputElement>(null)

  const samples = useAsync(() => api.listSamples(), [results.length])
  const orphans = useAsync(() => api.listRuns({ unassigned: true }), [results.length])

  const send = useCallback(
    async (files: FileList | File[]) => {
      const list = [...files]
      if (!list.length) return
      setBusy(true)

      let sampleId = targetSample
      try {
        if (!sampleId && newSampleName.trim()) {
          // A file name like No_1_dry_0.0316g_13pi_80wt%_0.2C_... already
          // carries the conditions, but reading them out of it would be
          // guesswork; the schedule inside the file is authoritative and gets
          // applied server-side after upload.
          const created = await api.createSample({ name: newSampleName.trim() })
          sampleId = created.id
          setTargetSample(created.id)
          setNewSampleName('')
        }
      } catch (cause) {
        setResults((current) => [
          { file: newSampleName, error: String(cause instanceof Error ? cause.message : cause) },
          ...current,
        ])
        setBusy(false)
        return
      }

      for (const file of list) {
        try {
          const run = await api.uploadRun(file, sampleId)
          setResults((current) => [{ file: file.name, run }, ...current])
        } catch (cause) {
          setResults((current) => [
            {
              file: file.name,
              error: String(cause instanceof Error ? cause.message : cause),
            },
            ...current,
          ])
        }
      }
      setBusy(false)
    },
    [targetSample, newSampleName],
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
              <div className="grid cols-2" style={{ gap: 10, marginBottom: 12 }}>
                <Field label="기존 셀에 연결">
                  <select
                    value={targetSample ?? ''}
                    onChange={(event) =>
                      setTargetSample(event.target.value ? Number(event.target.value) : null)
                    }
                  >
                    <option value="">연결 안 함 (나중에 지정)</option>
                    {samples.data?.map((sample) => (
                      <option key={sample.id} value={sample.id}>
                        {sample.name}
                      </option>
                    ))}
                  </select>
                </Field>
                <Field label="또는 새 셀 만들기" hint="이름만 입력">
                  <input
                    type="text"
                    value={newSampleName}
                    placeholder="No_1_dry_0.0316g"
                    disabled={targetSample !== null}
                    onChange={(event) => setNewSampleName(event.target.value)}
                  />
                </Field>
              </div>

              <div
                className={`dropzone${over ? ' over' : ''}`}
                onDragOver={(event) => {
                  event.preventDefault()
                  setOver(true)
                }}
                onDragLeave={() => setOver(false)}
                onDrop={(event) => {
                  event.preventDefault()
                  setOver(false)
                  void send(event.dataTransfer.files)
                }}
                onClick={() => inputRef.current?.click()}
                role="button"
                tabIndex={0}
                onKeyDown={(event) => event.key === 'Enter' && inputRef.current?.click()}
              >
                <div className="big">여기에 .wrd 파일을 끌어다 놓으세요</div>
                <div className="small">또는 눌러서 선택 · 여러 개 한 번에 가능</div>
                <input
                  ref={inputRef}
                  type="file"
                  accept=".wrd"
                  multiple
                  hidden
                  onChange={(event) => {
                    if (event.target.files) void send(event.target.files)
                    event.target.value = ''
                  }}
                />
              </div>

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

        <Card title={`연결 안 된 파일 · ${orphans.data?.length ?? 0}개`} tight>
          <div style={{ padding: 14 }}>
            {orphans.data?.length ? (
              <div className="col" style={{ gap: 12 }}>
                {orphans.data.map((run) => (
                  <OrphanRun
                    key={run.id}
                    run={run}
                    samples={samples.data ?? []}
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
        {run.row_count.toLocaleString()} 샘플 · {run.complete_cycle_count}/{run.cycle_count}{' '}
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
  const [busy, setBusy] = useState(false)
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
        defaultValue=""
        onChange={async (event) => {
          if (!event.target.value) return
          setBusy(true)
          try {
            await api.updateRun(run.id, { sample_id: Number(event.target.value) })
            onAttached()
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
      <div className="sep" />
    </div>
  )
}
