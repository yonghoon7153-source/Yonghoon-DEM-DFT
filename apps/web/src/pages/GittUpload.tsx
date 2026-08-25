/** GITT 업로드 — Smart Interface 의 `.wrd` 를 그대로.
 *
 *  텍스트로 내보낼 필요가 없다.  펄스와 휴지를 가르는 일은 서버가 하고,
 *  사람이 할 일은 **어느 셀의 것인지** 를 말하는 것뿐이다 — 그것이 없으면
 *  이 기록은 어느 대시보드에도 안 나온다.
 *
 *  셀을 안 정해도 올라간다.  파일부터 올려 두고 나중에 셀을 만드는 순서가
 *  흔하고, 없는 소속을 지어내는 것보다 비워 두는 편이 맞다 (§0.4).
 */

import { useRef, useState } from 'react'
import { Link } from 'react-router-dom'

import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { useAsync } from '../lib/hooks'
import type { GittRun } from '../lib/types'

export function GittUpload() {
  const [attachTo, setAttachTo] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [made, setMade] = useState<GittRun[]>([])
  const fileRef = useRef<HTMLInputElement>(null)

  const samples = useAsync(() => api.listSamples(), [])

  async function upload(files: FileList | null) {
    if (!files?.length) return
    setBusy(true)
    setError(null)
    setMade([])
    const added: GittRun[] = []
    const problems: string[] = []
    try {
      for (const file of files) {
        try {
          added.push(await api.uploadGittRun(
            file, attachTo ? { sample_id: attachTo } : undefined))
        } catch (cause) {
          // 한 파일이 실패했다고 나머지를 멈추지 않는다.
          problems.push(`${file.name}: ${
            cause instanceof Error ? cause.message : String(cause)}`)
        }
      }
      setMade(added)
      if (problems.length) setError(problems.join('\n'))
    } finally {
      setBusy(false)
      if (fileRef.current) fileRef.current.value = ''
    }
  }

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>GITT 업로드</h1>
          <div className="sub">
            Smart Interface 가 남긴 <code>.wrd</code> 를 그대로 — 텍스트로 내보낼
            필요 없습니다
          </div>
        </div>
      </div>

      {error ? <Alert kind="warn">{error}</Alert> : null}

      <Card title="어느 셀의 것인가">
        <div className="grid cols-3" style={{ padding: 12, gap: 10 }}>
          <Field label="셀에 붙이기" hint="비우면 안 붙임 — 나중에 붙여도 됩니다">
            <select
              aria-label="셀에 붙이기"
              value={attachTo}
              onChange={(event) => setAttachTo(event.target.value)}
            >
              <option value="">— 안 붙임</option>
              {(samples.data ?? []).map((sample) => (
                <option key={sample.id} value={sample.id}>{sample.name}</option>
              ))}
            </select>
          </Field>
        </div>
      </Card>

      <Card title="파일">
        <div className="row" style={{ padding: 12, gap: 10, flexWrap: 'wrap' }}>
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
            파일 고르기
          </button>
          {busy ? <Spinner label="올리는 중" /> : null}
          <span className="tiny dim">
            확산계수를 내려면 몰부피·몰질량·활물질 질량·면적이 필요합니다 —
            올린 뒤 기록 화면에서 넣으세요.
          </span>
        </div>
      </Card>

      <Card title={made.length ? `올린 것 ${made.length}개` : '올린 것'} tight>
        {made.length ? (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left' }}>이름</th>
                  <th>펄스</th>
                  <th>점</th>
                  <th style={{ textAlign: 'left' }}>셀</th>
                  <th style={{ textAlign: 'left' }}>관찰</th>
                </tr>
              </thead>
              <tbody>
                {made.map((item) => (
                  <tr key={item.id}>
                    <td className="text">
                      <Link to={`/gitt/${item.id}`}>{item.name}</Link>
                    </td>
                    <td>{item.n_pulses}</td>
                    <td>{item.n_points}</td>
                    <td className="text dim">{item.sample_name ?? '— 안 붙임'}</td>
                    {/* 사이클링 파일을 여기 올렸다면 이 한 줄이 유일한 신호다.
                        판정이 아니라 관찰이라 조용히 삼키지 않는다. */}
                    <td className="text dim tiny">{item.pulse_note || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <Empty title="아직 올린 것이 없습니다" icon="↑">
            펄스와 휴지로 이루어진 <code>.wrd</code> 를 올려 주세요.
          </Empty>
        )}
      </Card>
    </main>
  )
}
