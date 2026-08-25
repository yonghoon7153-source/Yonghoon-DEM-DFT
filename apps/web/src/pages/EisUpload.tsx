/** EIS 업로드 — 충방전 업로드와 같은 양식.
 *
 *  왼쪽에서 **그룹 → 셀 → 파일** 순으로 정하고 끌어다 놓는다.  오른쪽은 아직
 *  셀에 안 붙은 것들이다.  충방전 쪽과 순서·이름·모양을 맞춘 이유는 이 셋이
 *  실제로 같은 일이기 때문이다 — 측정 종류가 다르다고 손에 익은 순서까지
 *  달라지면 매번 다시 배워야 한다 (ADR 0024).
 *
 *  EIS 에만 있는 것은 가운데 한 줄이다: **무엇을 잰 것인가** (전해질 · 셀 구성 ·
 *  목적).  그 조합이 기본 회로와 아크의 이름을 정하므로 (ADR 0019) 올릴 때
 *  물어 두는 편이 낫다.
 *
 *  SOC 스캔인지 단일 스펙트럼인지는 **묻지 않는다.**  스윕 수는 파일이 스스로
 *  말하고 (§0.3), 올린 뒤 표가 그렇게 적어 준다.
 */

import { useCallback, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { RelatedCellIndex } from '../components/RelatedCell'
import { DropZone, UploadTargetFields, useUploadTarget } from '../components/UploadTarget'
import { Alert, Card, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { useAsync } from '../lib/hooks'
import type { CellConfig, EisKind, Spectrum } from '../lib/types'

const KINDS: { value: EisKind; label: string; hint: string }[] = [
  { value: 'liquid', label: '액체 전해질', hint: '두 아크가 SEI 와 전하이동' },
  { value: 'solid', label: '전고체',
    hint: '같은 두 아크가 벌크와 입계 — 이름이 다릅니다' },
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

interface Result {
  file: string
  spectrum?: Spectrum
  error?: string
}

export function EisUpload() {
  const [kind, setKind] = useState<EisKind>('liquid')
  const [config, setConfig] = useState<CellConfig | ''>('')
  const [purpose, setPurpose] = useState('')
  const [busy, setBusy] = useState(false)
  const [results, setResults] = useState<Result[]>([])

  // 파일 이름으로 셀을 만들지 않는다 — 여기서 파일은 셀이 아니라
  // 셀의 측정이다 (`UploadTargetFields` 머리말).
  const pick = useUploadTarget(results.length, false)
  const spectra = useAsync(() => api.listSpectra(), [results.length], { live: true })
  const samples = useAsync(() => api.listSamples(), [results.length], { live: true })

  // 색인 창은 **이번에 올린 것만** 편다.  한때 전부를 폈는데, 스펙트럼이
  // 쌓이자 방금 올린 파일이 수십 줄 사이에 묻혀서 정작 여기서 할 일 -- 방금
  // 것의 관계셀을 정하는 일 -- 이 제일 어려워졌다.  예전 것의 관계셀은
  // 목록·대시보드에서 그대로 고칠 수 있다.
  const mine = useMemo(
    () => new Set(results.map((item) => item.spectrum?.id)
      .filter((id): id is number => id !== undefined)),
    [results],
  )

  const send = useCallback(async (files: FileList | File[]) => {
    const all = [...files]
    if (!all.length) return
    setBusy(true)
    // `.mps` 는 스펙트럼이 아니라 그 옆에 놓이는 설정 파일이다.  같이 던졌으면
    // 스펙트럼마다 곁들여 보내고, 혼자 왔으면 올릴 것이 없다.
    const settings = all.find((f) => f.name.toLowerCase().endsWith('.mps'))
    const list = all.filter((f) => f !== settings)
    try {
      const plan = await pick.planFor(list)
      for (const [index, file] of list.entries()) {
        try {
          const spectrum = await api.uploadSpectrum(
            file,
            {
              kind,
              cell_config: config || undefined,
              purpose: purpose.trim() || undefined,
              sample_id: plan[index] ?? undefined,
            },
            settings ?? null,
          )
          setResults((current) => [{ file: file.name, spectrum }, ...current])
        } catch (cause) {
          // 한 파일이 실패했다고 나머지를 안 올리면, 스무 개를 던진 사람이
          // 어디까지 됐는지 모른 채 처음부터 다시 하게 된다.
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
  }, [pick, kind, config, purpose])

  return (
    <main className="page">
      <div className="page-head">
        <div>
          <h1>EIS 업로드</h1>
          <div className="sub">
            EC-Lab 의 <code>.mpr</code>·<code>.mpt</code> 를 그대로 올리면 주파수·
            임피던스를 한 번에 읽습니다. 같은 파일을 다시 올려도 중복되지 않습니다.
          </div>
        </div>
      </div>

      <div className="split">
        <div className="col" style={{ gap: 14 }}>
          <Card title="파일 선택" tight>
            <div style={{ padding: 14 }}>
              <UploadTargetFields pick={pick} />

              <div className="grid cols-3" style={{ gap: 10, marginBottom: 12 }}>
                <Field label="④ 전해질"
                       hint={KINDS.find((e) => e.value === kind)?.hint}>
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
                <Field label="⑤ 셀 구성" hint="아크의 뜻과 기본 회로를 정합니다">
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
                <Field label="⑥ 목적" hint="비우면 파일이 말하는 대로">
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
              </div>

              <DropZone
                accept=".mpr,.mpt,.mps"
                label="여기에 .mpr 파일을 끌어다 놓으세요"
                hint="또는 눌러서 선택 · 여러 개 한 번에 가능 · .mps 를 같이 던지면 진폭·장비 이름이 함께 들어갑니다"
                onFiles={send}
              />

              {busy ? (
                <div style={{ marginTop: 12 }}>
                  <Spinner label="읽는 중 — 스윕이 여럿이면 줄이 여러 개 생깁니다" />
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

        <Card title="관계셀 색인" tight>
          <div style={{ padding: 14 }}>
            {/* 오류를 문장 뒤에 숨기지 않는다.  실패한 조회는 "모두 붙어
                있습니다" 를 말할 근거가 없고, 그 단정은 셀에 못 들어간 파일에서
                사람을 돌려보낸다. */}
            {spectra.error ? (
              <Alert kind="error">{spectra.error}</Alert>
            ) : spectra.loading && !spectra.data ? (
              <Spinner />
            ) : (
              <RelatedCellIndex
                entries={(spectra.data ?? []).filter((item) => mine.has(item.id)).map((item) => ({
                  id: item.id,
                  name: item.name,
                  sampleId: item.sample_id,
                  sampleName: item.sample_name,
                  detail: `${item.n_points}점`,
                  href: `/eis/${item.id}`,
                }))}
                samples={samples.data ?? []}
                onAttach={async (id, sampleId) => {
                  await api.updateSpectrum(id, sampleId
                    ? { sample_id: sampleId }
                    : { clear: ['sample_id'] })
                  spectra.reload()
                }}
                onDelete={async (id) => {
                  await api.deleteSpectrum(id)
                  spectra.reload()
                }}
                emptyLabel="이번에 올린 스펙트럼이 여기 나옵니다 — 예전 것은 목록에서 고칠 수 있습니다"
              />
            )}
          </div>
        </Card>
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
  const item = result.spectrum
  if (!item) return null
  const sweeps = item.sweep_count ?? 1
  return (
    <div className="col" style={{ gap: 4 }}>
      <div className="row" style={{ gap: 8 }}>
        <strong>{item.original_name || item.name}</strong>
        <span className="badge finished">읽음</span>
        {/* 같은 바이트를 다시 올린 것은 새 행이 아니다.  조용히 넘어가면
            "올렸는데 개수가 안 늘었다" 가 된다. */}
        {item.duplicate ? <span className="tiny dim">이미 있던 것</span> : null}
        {item.sample_name ? (
          <Link className="tiny" to={`/samples/${item.sample_id}`}>
            {item.sample_name}
          </Link>
        ) : <span className="tiny dim">셀 안 붙임</span>}
      </div>
      <div className="tiny dim">
        {sweeps > 1 ? `SOC 스캔 — 스윕 ${sweeps}개` : '단일 스펙트럼'}
        {` · ${item.n_points}점`}
        {item.purpose ? ` · ${item.purpose}` : ''}
        {sweeps > 1 ? (
          <>
            {' · '}
            <Link to={`/scans/${item.sha256}`}>스캔 보기</Link>
          </>
        ) : null}
      </div>
    </div>
  )
}
