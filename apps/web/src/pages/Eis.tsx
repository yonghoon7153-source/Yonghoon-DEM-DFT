/** 임피던스 — 스펙트럼 목록, 올리기, 일괄 피팅.
 *
 *  액체 전해질과 전고체를 나란히 두지 않고 **탭으로 가른다** (ADR 0019).
 *  두 화면의 그림은 똑같이 반원 두 개인데 뜻이 다르다: 액체에서는 SEI 와
 *  전하이동, 전고체에서는 grain 내부와 grain boundary 이고, 뽑는 수도 저항과
 *  전도도로 다르다.  한 표에 섞어 놓으면 반드시 남의 이름이 붙는다.
 */

import { useMemo, useRef, useState } from 'react'
import { Link } from 'react-router-dom'

import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { dateTime, num } from '../lib/format'
import { useAsync } from '../lib/hooks'
import type { EisKind, Spectrum } from '../lib/types'

const KINDS: { value: EisKind; label: string; hint: string }[] = [
  {
    value: 'liquid',
    label: '액체 전해질',
    hint: '전해질 저항 + SEI 아크 + 전하이동 아크 (+ 확산 꼬리)',
  },
  {
    value: 'solid',
    label: '전고체',
    hint: '이온 블로킹 대칭셀 — 벌크 아크 + 입계 아크 + 블로킹 꼬리, 전도도까지',
  },
]

export function Eis() {
  const [kind, setKind] = useState<EisKind>('liquid')
  const [reloadKey, bumpReload] = useState(false)
  const [search, setSearch] = useState('')
  const [chosen, setChosen] = useState<number[]>([])
  // 올릴 때 셀을 정해 두면 나중에 하나씩 붙일 일이 없다.  대부분 한 셀의
  // 초기·200 사이클을 함께 올리므로, 파일마다 고르게 하지 않는다.
  const [attachTo, setAttachTo] = useState('')
  // 목적은 올릴 때 적어 두는 것이 가장 정확하다 — 나중에 21개 행을 하나씩
  // 고치는 것보다.  SOC 스캔은 파일이 스스로 말하므로 비워 둬도 된다.
  const [purpose, setPurpose] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [note, setNote] = useState<string | null>(null)
  const fileRef = useRef<HTMLInputElement>(null)

  const samples = useAsync(() => api.listSamples(), [])
  const spectra = useAsync(
    () => api.listSpectra({ kind, search: search || undefined }),
    [kind, search, reloadKey],
    { live: true },
  )
  const shown = useMemo(() => spectra.data ?? [], [spectra.data])
  const selected = useMemo(
    () => chosen.filter((id) => shown.some((item) => item.id === id)),
    [chosen, shown],
  )

  const reload = () => bumpReload((value) => !value)

  async function upload(files: FileList | null) {
    if (!files || !files.length) return
    setBusy(true)
    setError(null)
    setNote(null)
    // `.mps` 는 짝이 되는 데이터 파일에 붙여 보낸다.  따로 올라온 설정 파일은
    // 그 자체로는 스펙트럼이 아니라서 서버가 거절한다.
    //
    // EC-Lab 은 채널 접미사를 **데이터 파일에만** 붙인다: `A_C01.mpr` 의 짝은
    // `A.mps` 다.  접미사를 안 떼고 비교하면 맞는 짝이 항상 빠지고, "하나씩
    // 이면 그냥 붙인다" 는 예비 규칙이 남의 실험 조건을 측정 조건으로 저장
    // 했다 (리뷰 #13).  정규화한 이름이 정확히 하나 맞을 때만 붙는다.
    const settings = [...files].filter((file) => file.name.toLowerCase().endsWith('.mps'))
    const data = [...files].filter((file) => !file.name.toLowerCase().endsWith('.mps'))
    const stemOf = (name: string) => name.replace(/\.[^.]+$/, '').replace(/_C\d+$/i, '')
    const pairs = data.map((file) => {
      const matches = settings.filter((s) => stemOf(s.name) === stemOf(file.name))
      return { file, matches }
    })
    const ambiguous = pairs.filter((pair) => pair.matches.length > 1)
    if (ambiguous.length) {
      setError(
        ambiguous
          .map(
            (pair) =>
              `${pair.file.name} 에 맞는 설정 파일이 여럿입니다: ` +
              pair.matches.map((m) => m.name).join(', '),
          )
          .join('\n') + '\n하나만 남기고 다시 올려 주세요.',
      )
      setBusy(false)
      if (fileRef.current) fileRef.current.value = ''
      return
    }
    let added = 0
    let already = 0
    try {
      for (const { file, matches } of pairs) {
        const out = await api.uploadSpectrum(
          file,
          { kind, sample_id: attachTo || undefined,
            purpose: purpose.trim() || undefined },
          matches[0] ?? null,
        )
        if (out.duplicate) already += 1
        else added += 1
      }
      const used = new Set(pairs.flatMap((pair) => pair.matches.map((m) => m.name)))
      const orphans = settings.filter((s) => !used.has(s.name))
      const parts: string[] = []
      if (added) parts.push(`${added}개 올렸습니다`)
      // "올렸습니다" 와 "이미 있었습니다" 는 다른 일이다 (리뷰 #22) — 같은
      // 파일을 다시 올린 사람은 새 항목이 안 생긴 이유를 알아야 한다.
      if (already) parts.push(`${already}개는 이미 있던 파일입니다`)
      if (orphans.length)
        parts.push(`짝을 못 찾은 설정 파일: ${orphans.map((s) => s.name).join(', ')}`)
      setNote(parts.length ? parts.join(' · ') : '올릴 데이터 파일이 없습니다')
      reload()
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause))
    } finally {
      setBusy(false)
      if (fileRef.current) fileRef.current.value = ''
    }
  }

  async function fitSelected() {
    if (!selected.length) return
    setBusy(true)
    setError(null)
    setNote(null)
    try {
      const result = await api.fitSpectra(selected)
      // 성공만 세면 반쯤 실패한 배치가 작은 배치로 읽힌다.
      const parts = [`${result.converged}/${result.requested}개 수렴`]
      if (result.failed.length) parts.push(`${result.failed.length}개 실패`)
      setNote(parts.join(' · '))
      if (result.failed.length) {
        setError(result.failed.map((row) => `#${row.spectrum_id}: ${row.detail}`).join('\n'))
      }
      reload()
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause))
    } finally {
      setBusy(false)
    }
  }

  const active = KINDS.find((entry) => entry.value === kind)!

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>임피던스 (EIS)</h1>
          <div className="sub">{active.hint}</div>
        </div>
        <span className="spacer" />
        <div className="row">
          <input
            ref={fileRef}
            type="file"
            multiple
            accept=".mpr,.mpt,.mps"
            aria-label="스펙트럼 파일"
            onChange={(event) => void upload(event.target.files)}
            style={{ display: 'none' }}
          />
          <Field label="목적" hint="비우면 파일이 말하는 대로 (SOC 스캔은 자동)">
            <input
              aria-label="목적"
              list="eis-upload-purposes"
              value={purpose}
              placeholder="예: SOC별, 200 사이클"
              onChange={(event) => setPurpose(event.target.value)}
            />
            <datalist id="eis-upload-purposes">
              <option value="SOC별" />
              <option value="사이클별" />
              <option value="200 사이클" />
              <option value="구동 전" />
              <option value="온도별" />
            </datalist>
          </Field>
          <Field label="셀에 붙이기" hint="비우면 안 붙임">
            <select
              aria-label="셀에 붙이기"
              value={attachTo}
              onChange={(event) => setAttachTo(event.target.value)}
            >
              <option value="">— 안 붙임</option>
              {(samples.data ?? []).map((sample) => (
                <option key={sample.id} value={sample.id}>
                  {sample.name}
                </option>
              ))}
            </select>
          </Field>
          <button
            type="button"
            className="primary"
            disabled={busy}
            onClick={() => fileRef.current?.click()}
          >
            파일 올리기
          </button>
          <button
            type="button"
            disabled={busy || !selected.length}
            onClick={() => void fitSelected()}
          >
            고른 {selected.length}개 맞추기
          </button>
        </div>
      </div>

      {/* 두 세계를 탭으로 가른다.  같은 표에 섞으면 전고체 결과에
          '전하이동 저항' 이라는 이름이 붙는다 (ADR 0019). */}
      <div className="segmented" role="tablist" style={{ marginBottom: 12 }}>
        {KINDS.map((entry) => (
          <button
            key={entry.value}
            type="button"
            role="tab"
            aria-selected={kind === entry.value}
            className={kind === entry.value ? 'on accent' : ''}
            onClick={() => {
              setKind(entry.value)
              setChosen([])
            }}
          >
            {entry.label}
          </button>
        ))}
      </div>

      {error ? <Alert kind="error">{error}</Alert> : null}
      {note ? <Alert kind="info">{note}</Alert> : null}

      <Card
        title={`스펙트럼 ${shown.length}개`}
        actions={
          <div className="row" style={{ gap: 6 }}>
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
        {spectra.error ? (
          <Alert kind="error">{spectra.error}</Alert>
        ) : spectra.loading && !spectra.data ? (
          <div style={{ padding: 20 }}>
            <Spinner />
          </div>
        ) : shown.length ? (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th style={{ width: 30 }} />
                  <th style={{ textAlign: 'left' }}>이름</th>
                  <th style={{ textAlign: 'left' }}>셀</th>
                  <th>사이클</th>
                  <th style={{ textAlign: 'left' }}>셀 구성</th>
                  <th>두께</th>
                  <th>점</th>
                  <th>주파수</th>
                  <th>피팅</th>
                  <th>χ²</th>
                  <th style={{ textAlign: 'left' }}>회로</th>
                  <th>올린 때</th>
                </tr>
              </thead>
              <tbody>
                {shown.map((item) => (
                  <Row
                    key={item.id}
                    spectrum={item}
                    checked={selected.includes(item.id)}
                    onToggle={() =>
                      setChosen((current) =>
                        current.includes(item.id)
                          ? current.filter((id) => id !== item.id)
                          : [...current, item.id],
                      )
                    }
                  />
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <Empty title="아직 스펙트럼이 없습니다" icon="↑">
            EC-Lab 이 남긴 <code>.mpr</code> 를 그대로 올리면 됩니다. 이미 내보낸
            <code> .mpt</code> 도 읽습니다.
          </Empty>
        )}
      </Card>
    </main>
  )
}

const CONFIG_LABELS: Record<string, string> = {
  sym: '대칭셀',
  full: '풀셀',
  half: '하프셀',
}

function Row({
  spectrum,
  checked,
  onToggle,
}: {
  spectrum: Spectrum
  checked: boolean
  onToggle: () => void
}) {
  return (
    <tr>
      <td>
        <input
          type="checkbox"
          checked={checked}
          onChange={onToggle}
          aria-label={`${spectrum.name} 고르기`}
        />
      </td>
      <td className="text">
        <Link to={`/eis/${spectrum.id}`}>{spectrum.name}</Link>
      </td>
      <td className="text dim">
        {spectrum.sample_id ? (
          <Link to={`/samples/${spectrum.sample_id}`}>{spectrum.sample_name}</Link>
        ) : (
          '—'
        )}
      </td>
      {/* 초기와 200 사이클을 비교하는 것이 목적이므로 번호가 데이터의 일부다.
          없으면 올린 순서로 정렬돼 파일을 끌어다 놓은 순서가 그림의 순서가 된다. */}
      <td>{spectrum.at_cycle === null ? '—' : spectrum.at_cycle}</td>
      {/* 아크의 이름과 전도도가 이 두 칸에 걸려 있다.  표에서 비어 있는 것이
          보여야 채우러 들어간다. */}
      <td className="text dim">{CONFIG_LABELS[spectrum.cell_config] ?? '—'}</td>
      <td className="dim">{spectrum.thickness_um ? `${spectrum.thickness_um} µm` : '—'}</td>
      <td>{spectrum.n_points}</td>
      <td className="dim">{frequencySpan(spectrum)}</td>
      <td>{spectrum.fit_count || '—'}</td>
      <td>{spectrum.best_chi_squared === null ? '—' : num(spectrum.best_chi_squared, 3)}</td>
      <td className="text dim mono">{spectrum.best_circuit || '—'}</td>
      <td className="dim">{dateTime(spectrum.uploaded_at)}</td>
    </tr>
  )
}

/** "7 MHz → 10 mHz".  자릿수가 아홉 개 차이 나므로 접두어로 쓴다. */
export function frequencySpan(spectrum: {
  frequency_start_hz: number | null
  frequency_end_hz: number | null
}): string {
  const { frequency_start_hz: start, frequency_end_hz: end } = spectrum
  if (start === null || end === null) return '—'
  return `${hertz(start)} → ${hertz(end)}`
}

export function hertz(value: number): string {
  if (!Number.isFinite(value)) return '—'
  const units: [number, string][] = [
    [1e6, 'MHz'],
    [1e3, 'kHz'],
    [1, 'Hz'],
    [1e-3, 'mHz'],
  ]
  for (const [scale, unit] of units) {
    if (Math.abs(value) >= scale) {
      const scaled = value / scale
      return `${scaled >= 100 ? scaled.toFixed(0) : scaled.toFixed(scaled >= 10 ? 1 : 2)} ${unit}`
    }
  }
  return `${value.toExponential(1)} Hz`
}
