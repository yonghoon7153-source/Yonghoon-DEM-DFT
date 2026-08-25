/** GITT 업로드 — 충방전 업로드와 같은 양식.
 *
 *  같은 `.wrd` 를 읽지만 섹션이 다르다 (ADR 0020).  다른 것은 **읽는 방식**이지
 *  올리는 방식이 아니므로, 그룹 → 셀 → 파일 순서와 끌어다 놓는 자리는 그대로
 *  가져왔다.
 *
 *  GITT 에만 있는 것은 오른쪽 아래 한 줄이다: 확산계수를 내려면 파일에 없는
 *  값 넷이 필요하고 (몰부피 · 몰질량 · 활물질 질량 · 면적), 그건 기록마다
 *  달라서 여기서 한 번에 받을 수가 없다.
 */

import { useCallback, useState } from 'react'
import { Link } from 'react-router-dom'

import { DropZone, UploadTargetFields, useUploadTarget } from '../components/UploadTarget'
import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { num } from '../lib/format'
import { useAsync } from '../lib/hooks'
import type { GittRun } from '../lib/types'

/** 자유 입력의 보기.  EIS 와 같은 이유로 목록을 고정하지 않는다 -- 랩이 새
 *  목적을 계속 만들고, 고정하면 그때마다 코드를 고쳐야 한다. */
const PURPOSES = ['SOC별', '저온', '고온', '코팅 전후', '두께별']

interface Result {
  file: string
  run?: GittRun
  error?: string
}

export function GittUpload() {
  const [purpose, setPurpose] = useState('')
  const [busy, setBusy] = useState(false)
  const [results, setResults] = useState<Result[]>([])

  const pick = useUploadTarget(results.length)
  const orphans = useAsync(
    () => api.listGittRuns().then((all) => all.filter((run) => !run.sample_id)),
    [results.length], { live: true })

  const send = useCallback(async (files: FileList | File[]) => {
    const list = [...files]
    if (!list.length) return
    setBusy(true)
    try {
      const plan = await pick.planFor(list)
      for (const [index, file] of list.entries()) {
        try {
          const sampleId = plan[index]
          const run = await api.uploadGittRun(file, {
            ...(sampleId ? { sample_id: sampleId } : {}),
            ...(purpose.trim() ? { purpose: purpose.trim() } : {}),
          })
          setResults((current) => [{ file: file.name, run }, ...current])
        } catch (cause) {
          // 한 파일이 실패했다고 나머지를 멈추지 않는다.
          setResults((current) => [{
            file: file.name,
            error: cause instanceof Error ? cause.message : String(cause),
          }, ...current])
        }
      }
    } catch (cause) {
      setResults((current) => [{
        file: '셀 만들기',
        error: cause instanceof Error ? cause.message : String(cause),
      }, ...current])
    } finally {
      setBusy(false)
    }
  }, [pick, purpose])

  return (
    <main className="page">
      <div className="page-head">
        <div>
          <h1>GITT 업로드</h1>
          <div className="sub">
            Smart Interface 가 남긴 <code>.wrd</code> 를 그대로 올리면 펄스와 휴지를
            갈라 읽습니다 — 텍스트로 내보낼 필요 없습니다.
          </div>
        </div>
      </div>

      <div className="split">
        <div className="col" style={{ gap: 14 }}>
          <Card title="파일 선택" tight>
            <div style={{ padding: 14 }}>
              <UploadTargetFields pick={pick} />

              <div className="grid cols-2" style={{ gap: 10, marginBottom: 12 }}>
                <Field label="④ 목적" hint="무엇을 보려고 잰 기록인가 · 비워도 됩니다">
                  <input
                    aria-label="목적"
                    list="gitt-purposes"
                    value={purpose}
                    placeholder="예: SOC별, 저온"
                    onChange={(event) => setPurpose(event.target.value)}
                  />
                  <datalist id="gitt-purposes">
                    {PURPOSES.map((value) => <option key={value} value={value} />)}
                  </datalist>
                </Field>
              </div>

              <DropZone
                accept=".wrd"
                label="여기에 .wrd 파일을 끌어다 놓으세요"
                hint="또는 눌러서 선택 · 여러 개 한 번에 가능"
                onFiles={send}
              />

              {busy ? (
                <div style={{ marginTop: 12 }}>
                  <Spinner label="펄스와 휴지를 가르는 중" />
                </div>
              ) : null}
            </div>
          </Card>

          {results.length ? (
            <Card title="업로드 결과" tight>
              <div className="col" style={{ padding: 14, gap: 10 }}>
                {results.map((result, index) => (
                  <Result key={`${result.file}-${index}`} result={result} />
                ))}
              </div>
            </Card>
          ) : null}
        </div>

        <div className="col" style={{ gap: 14 }}>
          <Card
            title={`셀에 안 붙은 기록 · ${orphans.error ? '—' : `${orphans.data?.length ?? 0}개`}`}
            tight
          >
            <div style={{ padding: 14 }}>
              {orphans.error ? (
                <Alert kind="error">{orphans.error}</Alert>
              ) : orphans.loading && !orphans.data ? (
                <Spinner />
              ) : orphans.data?.length ? (
                <div className="col" style={{ gap: 8 }}>
                  {orphans.data.map((run) => (
                    <div key={run.id} className="row" style={{ gap: 8 }}>
                      <Link to={`/gitt/${run.id}`}>{run.name}</Link>
                      <span className="tiny dim">펄스 {run.n_pulses}개</span>
                    </div>
                  ))}
                  <div className="tiny faint">
                    <Link to="/gitt/library">라이브러리</Link>에서 그 자리로 붙일 수
                    있습니다.
                  </div>
                </div>
              ) : (
                <Empty title="모두 붙어 있습니다" />
              )}
            </div>
          </Card>

          <Card title="확산계수를 내려면" tight>
            <div style={{ padding: 14 }} className="tiny dim">
              파일에 없는 값 넷이 필요합니다 — <b>몰부피 · 활물질 몰질량 ·
              활물질 질량 · 전극 면적</b>. 기록마다 다르므로 올린 뒤 각 기록
              화면에서 넣습니다. 없으면 <b>추정하지 않고</b> 무엇이 없는지
              말합니다 (ADR 0020).
            </div>
          </Card>
        </div>
      </div>
    </main>
  )
}

function Result({ result }: { result: Result }) {
  if (result.error) {
    return (
      <Alert kind="error">
        <strong>{result.file}</strong> — {result.error}
      </Alert>
    )
  }
  const run = result.run
  if (!run) return null
  return (
    <div className="col" style={{ gap: 4 }}>
      <div className="row" style={{ gap: 8 }}>
        <strong>{run.original_name || run.name}</strong>
        <span className="badge finished">읽음</span>
        {run.sample_name ? (
          <Link className="tiny" to={`/samples/${run.sample_id}`}>{run.sample_name}</Link>
        ) : <span className="tiny dim">셀 안 붙임</span>}
      </div>
      <div className="tiny dim">
        {run.purpose ? `${run.purpose} · ` : ''}펄스 {run.n_pulses}개 · {run.n_points}점
        {run.duration_h === null ? '' : ` · ${num(run.duration_h, 3)} h`}
      </div>
      {/* 사이클링 파일을 여기 올렸다면 이 한 줄이 유일한 신호다.  판정이 아니라
          관찰이라 조용히 삼키지 않는다. */}
      {run.pulse_note ? <Alert kind="warn">{run.pulse_note}</Alert> : null}
    </div>
  )
}
