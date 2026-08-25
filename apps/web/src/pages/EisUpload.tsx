/** EIS 업로드 — 올리면서 무엇을 잰 것인지 분류한다.
 *
 *  **SOC 스캔이 별도 화면이 아닌 이유.**  SOC 스캔과 단일 스펙트럼은 같은
 *  `.mpr` 이고 같은 회로로 맞춘다.  다른 것은 파일 하나가 스윕 하나냐 스물이냐
 *  뿐이고, 그건 파일이 스스로 말한다 (ADR 0022).  그러니 목록을 둘로 가르는
 *  대신 **올릴 때 한 번 정하고**, 그 다음부터는 라이브러리에서 걸러 보면 된다.
 *
 *  파일이 말하는 것은 파일에게 묻는다 (§0.3).  스윕 수는 파싱하면 나오므로
 *  종류는 서버가 정하고, 이 화면의 드롭박스는 **덮어쓰기**다 — 사람이 "이건
 *  SOC 스캔이 아니라 온도별이다" 라고 말할 수 있어야 하고, 그때 그 말이 이긴다.
 */

import { useMemo, useRef, useState } from 'react'
import { Link } from 'react-router-dom'

import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { useAsync } from '../lib/hooks'
import type { CellConfig, EisKind, Spectrum } from '../lib/types'

const KINDS: { value: EisKind; label: string; hint: string }[] = [
  { value: 'liquid', label: '액체 전해질',
    hint: '두 아크가 SEI 와 전하이동' },
  { value: 'solid', label: '전고체',
    hint: '같은 두 아크가 벌크와 입계 — 이름이 다르다 (ADR 0019)' },
]

const CONFIGS: { value: CellConfig | ''; label: string }[] = [
  { value: '', label: '— 안 정함' },
  { value: 'full', label: '풀셀' },
  { value: 'half', label: '하프셀' },
  { value: 'sym', label: '대칭셀' },
]

/** 자유 입력의 보기.  목록을 고정하지 않는 이유는 랩이 새 목적을 계속
 *  만들어서다 — 고정하면 그때마다 코드를 고쳐야 한다. */
const PURPOSES = ['SOC별', '사이클별', '200 사이클', '구동 전', '온도별']

export function EisUpload() {
  const [kind, setKind] = useState<EisKind>('liquid')
  const [config, setConfig] = useState<CellConfig | ''>('')
  const [purpose, setPurpose] = useState('')
  const [attachTo, setAttachTo] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [made, setMade] = useState<Spectrum[]>([])
  const fileRef = useRef<HTMLInputElement>(null)
  const settingsRef = useRef<HTMLInputElement>(null)

  const samples = useAsync(() => api.listSamples(), [])
  const active = useMemo(
    () => KINDS.find((entry) => entry.value === kind) ?? KINDS[0]!, [kind])

  async function upload(files: FileList | null) {
    if (!files?.length) return
    setBusy(true)
    setError(null)
    setMade([])
    const added: Spectrum[] = []
    const problems: string[] = []
    // `.mps` 는 스펙트럼이 아니라 그 옆에 놓이는 설정 파일이다.  같이 골랐으면
    // 스펙트럼마다 곁들여 보내고, 혼자 왔으면 올릴 것이 없다.
    const settings = [...files].find((f) => f.name.toLowerCase().endsWith('.mps'))
    const spectra = [...files].filter((f) => f !== settings)
    try {
      for (const file of spectra) {
        try {
          const out = await api.uploadSpectrum(
            file,
            {
              kind,
              cell_config: config || undefined,
              purpose: purpose.trim() || undefined,
              sample_id: attachTo || undefined,
            },
            settings ?? null,
          )
          added.push(out)
        } catch (cause) {
          // 한 파일이 실패했다고 나머지를 안 올리면, 스무 개를 고른 사람이
          // 어디까지 됐는지 모른 채 처음부터 다시 하게 된다.
          problems.push(`${file.name}: ${
            cause instanceof Error ? cause.message : String(cause)}`)
        }
      }
      setMade(added)
      if (problems.length) setError(problems.join('\n'))
    } finally {
      setBusy(false)
      if (fileRef.current) fileRef.current.value = ''
      if (settingsRef.current) settingsRef.current.value = ''
    }
  }

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>EIS 업로드</h1>
          <div className="sub">
            EC-Lab 의 <code>.mpr</code>·<code>.mpt</code> 를 그대로 —
            SOC 스캔인지 단일 스펙트럼인지는 파일이 말합니다
          </div>
        </div>
      </div>

      {error ? <Alert kind="warn">{error}</Alert> : null}

      <Card title="무엇을 잰 것인가">
        <div className="grid cols-3" style={{ padding: 12, gap: 10 }}>
          <Field label="전해질" hint={active.hint}>
            <select
              aria-label="전해질"
              value={kind}
              onChange={(event) => setKind(event.target.value as EisKind)}
            >
              {KINDS.map((entry) => (
                <option key={entry.value} value={entry.value}>{entry.label}</option>
              ))}
            </select>
          </Field>
          <Field label="셀 구성" hint="아크의 뜻과 기본 회로를 정합니다">
            <select
              aria-label="셀 구성"
              value={config}
              onChange={(event) => setConfig(event.target.value as CellConfig | '')}
            >
              {CONFIGS.map((entry) => (
                <option key={entry.value} value={entry.value}>{entry.label}</option>
              ))}
            </select>
          </Field>
          <Field label="목적" hint="비우면 파일이 말하는 대로 (SOC 스캔은 자동)">
            <input
              aria-label="목적"
              list="eis-purposes"
              value={purpose}
              placeholder="예: SOC별, 200 사이클"
              onChange={(event) => setPurpose(event.target.value)}
            />
            <datalist id="eis-purposes">
              {PURPOSES.map((value) => <option key={value} value={value} />)}
            </datalist>
          </Field>
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
            accept=".mpr,.mpt,.mps"
            aria-label="스펙트럼 파일"
            onChange={(event) => void upload(event.target.files)}
            style={{ display: 'none' }}
          />
          <button type="button" className="primary" disabled={busy}
                  onClick={() => fileRef.current?.click()}>
            파일 고르기
          </button>
          {busy ? <Spinner label="올리는 중" /> : null}
          <span className="tiny dim">
            <code>.mps</code> 를 같이 고르면 진폭·장비 이름이 함께 들어갑니다.
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
                  <th style={{ textAlign: 'left' }}>종류</th>
                  <th>점</th>
                  <th style={{ textAlign: 'left' }}>목적</th>
                  <th style={{ textAlign: 'left' }}>셀</th>
                </tr>
              </thead>
              <tbody>
                {made.map((item) => (
                  <tr key={item.id}>
                    <td className="text">
                      <Link to={`/eis/${item.id}`}>{item.name}</Link>
                      {/* 같은 바이트를 다시 올린 것은 새 행이 아니다.  조용히
                          넘어가면 "올렸는데 개수가 안 늘었다" 가 된다. */}
                      {item.duplicate ? <span className="tiny dim"> (이미 있던 것)</span> : null}
                    </td>
                    <td className="text dim">
                      {(item.sweep_count ?? 1) > 1
                        ? `SOC 스캔 — 스윕 ${item.sweep_count}개`
                        : '단일 스펙트럼'}
                    </td>
                    <td>{item.n_points}</td>
                    <td className="text dim">{item.purpose || '—'}</td>
                    <td className="text dim">{item.sample_name ?? '— 안 붙임'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <Empty title="아직 올린 것이 없습니다" icon="↑">
            스윕이 여럿인 파일은 <b>스윕마다 한 줄</b>이 되고, 그 묶음이 SOC
            스캔입니다 — 라이브러리에서 종류로 걸러 볼 수 있습니다.
          </Empty>
        )}
      </Card>
    </main>
  )
}
