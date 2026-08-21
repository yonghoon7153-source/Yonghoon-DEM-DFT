/** Drop .wrd files, attach them to a cell, and see what the instrument said. */

import { useCallback, useMemo, useRef, useState } from 'react'
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
  //: 그룹을 여기서 정한다.  나중에 셀 화면에서 하나씩 붙이면, 같은 실험 묶음을
  //: 열 개씩 올리고 나서 열 번 다시 들어가야 한다.
  const [groupId, setGroupId] = useState<number | null>(null)
  //: 셀이 수십 개가 되면 드롭다운에서 눈으로 찾는 것이 느리다.  타이핑으로
  //: 좁힌다.
  const [sampleQuery, setSampleQuery] = useState('')
  //: 파일 하나가 셀 하나인 실험이 많다 (컷오프만 바꾼 열네 개짜리 묶음 같은).
  //: 그럴 때 이름을 열네 번 타이핑하게 두지 않는다.
  const [nameFromFile, setNameFromFile] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const samples = useAsync(() => api.listSamples(), [results.length], { live: true })
  const groups = useAsync(() => api.listGroups(), [results.length], { live: true })

  const matches = useMemo(() => {
    const all = samples.data ?? []
    const needle = sampleQuery.trim().toLowerCase()
    const inGroup = groupId === null ? all : all.filter((s) => s.group_id === groupId)
    if (!needle) return inGroup
    return inGroup.filter((s) => s.name.toLowerCase().includes(needle))
  }, [samples.data, sampleQuery, groupId])
  const orphans = useAsync(() => api.listRuns({ unassigned: true }), [results.length],
                         { live: true })

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
          const created = await api.createSample({
            name: newSampleName.trim(),
            ...(groupId === null ? {} : { group_id: groupId }),
          })
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

      // 같은 이름을 두 번 만들지 않도록, 이번 드롭에서 만든 것을 기억한다.
      const madeHere = new Map<string, number>()

      for (const file of list) {
        try {
          let target = sampleId
          if (nameFromFile) {
            const wanted = cellNameFor(file.name)
            const existing =
              madeHere.get(wanted) ??
              (samples.data ?? []).find((s) => s.name === wanted)?.id
            if (existing) {
              target = existing
            } else {
              const created = await api.createSample({
                name: wanted,
                ...(groupId === null ? {} : { group_id: groupId }),
              })
              madeHere.set(wanted, created.id)
              target = created.id
            }
          }
          const run = await api.uploadRun(file, target)
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
    [targetSample, newSampleName, groupId, nameFromFile, samples.data],
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
              {/* 그룹을 먼저 고른다.  아래 "기존 셀" 목록도 그 그룹으로 좁혀지고,
                  새로 만드는 셀은 그 그룹에 들어간다 — 한 실험 묶음을 통째로
                  올릴 때 나중에 하나씩 붙이지 않아도 된다. */}
              <Field
                label="① 그룹"
                hint="새 셀이 들어갈 곳 · 아래 목록도 좁혀집니다"
              >
                <select
                  value={groupId ?? ''}
                  aria-label="그룹"
                  onChange={(event) => {
                    const next = event.target.value ? Number(event.target.value) : null
                    setGroupId(next)
                    // 좁힌 목록에 없는 셀이 골라진 채로 남으면, 화면에는
                    // 안 보이는 셀에 파일이 붙는다.
                    setTargetSample(null)
                  }}
                >
                  <option value="">그룹 없음</option>
                  {groups.data?.map((group) => (
                    <option key={group.id} value={group.id}>
                      {group.name}
                    </option>
                  ))}
                </select>
              </Field>

              <div className="grid cols-2" style={{ gap: 10, margin: '10px 0 12px' }}>
                <Field
                  label="② 새 셀 만들기"
                  hint={nameFromFile ? '파일마다 셀 하나' : '이름만 입력'}
                >
                  <input
                    type="text"
                    value={newSampleName}
                    placeholder="No_1_dry_0.0316g"
                    disabled={targetSample !== null || nameFromFile}
                    onChange={(event) => setNewSampleName(event.target.value)}
                  />
                  <label className="tiny" style={{ display: 'block', marginTop: 6 }}>
                    <input
                      type="checkbox"
                      checked={nameFromFile}
                      onChange={(event) => {
                        setNameFromFile(event.target.checked)
                        if (event.target.checked) {
                          setNewSampleName('')
                          setTargetSample(null)
                        }
                      }}
                      style={{ marginRight: 6 }}
                    />
                    파일 이름을 셀 이름으로
                  </label>
                </Field>
                <Field
                  label="② 또는 기존 셀에 연결"
                  hint={
                    matches.length && sampleQuery.trim()
                      ? `${matches.length}개 일치`
                      : '이름을 쳐서 좁힐 수 있습니다'
                  }
                >
                  {/* 라벨은 Field 안의 첫 폼 요소에 붙는다.  검색칸이 먼저 오므로
                      select 는 자기 라벨을 따로 들어야 이름 없는 컨트롤이 되지
                      않는다. */}
                  <input
                    type="text"
                    value={sampleQuery}
                    placeholder="이름 일부…"
                    aria-label="셀 이름으로 찾기"
                    disabled={newSampleName.trim() !== ''}
                    onChange={(event) => {
                      setSampleQuery(event.target.value)
                      setTargetSample(null)
                    }}
                    style={{ marginBottom: 6 }}
                  />
                  <select
                    value={targetSample ?? ''}
                    aria-label="기존 셀에 연결"
                    disabled={newSampleName.trim() !== ''}
                    onChange={(event) =>
                      setTargetSample(event.target.value ? Number(event.target.value) : null)
                    }
                  >
                    <option value="">연결 안 함 (나중에 지정)</option>
                    {matches.map((sample) => (
                      <option key={sample.id} value={sample.id}>
                        {sample.name}
                      </option>
                    ))}
                  </select>
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
