/** GITT 기록 하나 — pseudo-OCV, 확산계수, 그리고 재료 상수.
 *
 *  두 결과를 나란히 두되 **비어 있는 이유가 다르다**: pOCV 는 파일만 있으면
 *  나오고, 확산계수는 파일에 없는 값 넷을 사람이 넣어야 한다 (ADR 0020).
 *  그래서 확산계수 자리는 비어 있을 때 "무엇이 없는지" 를 말한다.
 */

import { OtherMeasurements } from '../components/OtherMeasurements'
import { useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { CopyBar } from '../components/CopyBar'
import { Plot, type PlotSeries } from '../components/Plot'
import { Alert, Card, Field, KeyValues, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { dateTime, num, seriesColor } from '../lib/format'
import { diffusionTsv, pocvTsv, skippedDiffusionPoints } from '../lib/origin'
import { useAsync } from '../lib/hooks'
import type { GittRun } from '../lib/types'

type Mode = 'pocv' | 'diffusion'

export function GittDetail() {
  const params = useParams<{ id: string }>()
  const id = Number(params.id)
  const [mode, setMode] = useState<Mode>('pocv')
  const [reloadKey, bumpReload] = useState(false)

  const run = useAsync(() => api.getGittRun(id), [id, reloadKey])
  const pocv = useAsync(() => api.gittPocv(id), [id, reloadKey])
  const diffusion = useAsync(() => api.gittDiffusion(id), [id, reloadKey])

  const pocvSeries = useMemo<PlotSeries[]>(() => {
    const data = pocv.data
    if (!data) return []
    const out: PlotSeries[] = []
    // 원본을 **먼저** 넣는다: 나중 계열이 위에 그려지므로, pOCV 의 점이 선에
    // 가리지 않는다.  같은 색의 점선이라 어느 곡선의 원본인지도 분명하다.
    const raw = (trace: { capacity_mah: number[]; voltage_v: number[] } | undefined,
                 label: string, color: string) => {
      if (!trace?.capacity_mah.length) return
      out.push({
        label, x: trace.capacity_mah, y: trace.voltage_v,
        color, width: 1, dash: [3, 3],
      })
    }
    raw(data.charge_raw, '충전 측정 전압', seriesColor(0))
    raw(data.discharge_raw, '방전 측정 전압', seriesColor(1))
    if (data.charge.length) {
      out.push({
        label: '충전 pOCV',
        x: data.charge.map((point) => point.capacity_mah),
        y: data.charge.map((point) => point.voltage_v),
        color: seriesColor(0),
        points: true,
        width: 1,
      })
    }
    if (data.discharge.length) {
      out.push({
        label: '방전 pOCV',
        x: data.discharge.map((point) => point.capacity_mah),
        y: data.discharge.map((point) => point.voltage_v),
        color: seriesColor(1),
        points: true,
        width: 1,
      })
    }
    return out
  }, [pocv.data])

  const diffusionSeries = useMemo<PlotSeries[]>(() => {
    // null 검사를 명시적으로 — truthy 필터는 D=0 을 버려서, 표·TSV 에는 있는
    // 점이 그래프에서만 사라지고 "가정을 통과한 펄스 없음" 이 거짓이 됐다
    // (리뷰 #32).  0 은 로그축에 못 그리므로 빼되, 아래 문구가 셈해 준다.
    const usable = (diffusion.data?.points ?? [])
      .filter((point) => point.d_cm2_s !== null && point.d_cm2_s > 0)
    if (!usable.length) return []
    return [{
      label: 'log₁₀ D (cm²/s)',
      x: usable.map((point) => point.capacity_mah),
      // 자릿수가 서너 개 오가므로 로그로 그린다.  선형이면 큰 값 하나가
      // 나머지를 바닥에 눕힌다.
      y: usable.map((point) => Math.log10(point.d_cm2_s!)),
      color: seriesColor(2),
      points: true,
      width: 1,
    }]
  }, [diffusion.data])
  const zeroDiffusion = useMemo(
    () => (diffusion.data?.points ?? [])
      .filter((point) => point.d_cm2_s === 0).length,
    [diffusion.data],
  )

  if (run.error) {
    return <main className="page"><Alert kind="error">{run.error}</Alert></main>
  }
  if (!run.data) {
    return <main className="page"><Spinner label="불러오는 중" /></main>
  }
  const record = run.data

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1 className="truncate">{record.name}</h1>
          <div className="sub">
            {[`펄스 ${record.n_pulses}개`, `${record.n_points}점`,
              record.duration_h === null ? null : `${num(record.duration_h, 3)} h`]
              .filter(Boolean).join('  ·  ')}
          </div>
        </div>
        <span className="spacer" />
        <Link className="link-btn" to="/gitt">목록</Link>
      </div>

      {record.pulse_note ? <Alert kind="warn">{record.pulse_note}</Alert> : null}

      <div className="segmented" role="tablist" style={{ marginBottom: 12 }}>
        <button type="button" role="tab" aria-selected={mode === 'pocv'}
                className={mode === 'pocv' ? 'on accent' : ''}
                onClick={() => setMode('pocv')}>
          pseudo-OCV
        </button>
        <button type="button" role="tab" aria-selected={mode === 'diffusion'}
                className={mode === 'diffusion' ? 'on accent' : ''}
                onClick={() => setMode('diffusion')}>
          확산계수
        </button>
      </div>

      <div style={{ marginBottom: 12 }}>
        <CopyBar
          items={[
            {
              label: 'pOCV',
              title: '용량 · 전압 두 열 — 충전과 방전을 `--` 로 갈라 쌓는다',
              disabled: !pocv.data,
              build: () => (pocv.data ? pocvTsv(pocv.data) : ''),
            },
            {
              label: '확산계수',
              title: '용량 · D · 휴지(s) · 드리프트(mV) — 숫자가 나온 점만, 증거와 함께',
              disabled: !diffusion.data?.points.length,
              build: () => diffusionTsv(diffusion.data?.points ?? []),
              skipped: skippedDiffusionPoints(diffusion.data?.points ?? []),
              // 조용히 빼면 붙여 넣은 사람이 점 수가 다른 것을 못 본다.
              skippedNote: (n) => `가정을 통과하지 못한 펄스 ${n}개는 뺐습니다 — `
                + '이유는 아래 표에 있습니다',
            },
          ]}
        />
      </div>

      <div className="grid cols-2">
        <Card title={mode === 'pocv' ? '준평형 전압 곡선' : '확산계수'}>
          {mode === 'pocv' ? (
            pocv.error ? <Alert kind="error">{pocv.error}</Alert>
              : pocvSeries.length ? (
                <Plot series={pocvSeries} xLabel="용량 (mAh)" yLabel="전압 (V)"
                      height={340} legend />
              ) : pocv.loading ? <Spinner /> : (
                <Alert kind="info">
                  휴지 끝의 전압을 짝지을 펄스가 없습니다.
                </Alert>
              )
          ) : diffusion.error ? (
            <Alert kind="error">{diffusion.error}</Alert>
          ) : diffusion.data?.missing.length ? (
            // pOCV 와 비어 있는 이유가 다르다.  그 차이를 말한다.
            <Alert kind="info">
              확산계수를 내려면 {diffusion.data.missing.join(' · ')} 이(가)
              필요합니다 — 아래 &lsquo;재료 상수&rsquo; 에 넣어 주세요.
              추정한 값으로 계산한 D 는 그 추정의 제곱만큼 틀립니다.
            </Alert>
          ) : diffusionSeries.length ? (
            <div className="col" style={{ gap: 6 }}>
              <Plot series={diffusionSeries} xLabel="용량 (mAh)"
                    yLabel="log₁₀ D (cm²/s)" height={340} legend />
              {zeroDiffusion ? (
                <div className="tiny faint">
                  D=0 인 점 {zeroDiffusion}개는 로그축에 그릴 수 없어 뺐습니다 —
                  표와 클립보드에는 있습니다.
                </div>
              ) : null}
            </div>
          ) : diffusion.loading ? <Spinner /> : (
            <Alert kind="info">
              {zeroDiffusion
                ? `양수 D 가 없습니다 — D=0 인 점 ${zeroDiffusion}개는 로그축에 못 그립니다 (표에 있습니다).`
                : '가정을 통과한 펄스가 없습니다 — 아래 표의 이유를 보세요.'}
            </Alert>
          )}
        </Card>

        <Card title="재료 상수" padSmall>
          <MaterialFields record={record} onSaved={() => bumpReload((v) => !v)} />
        </Card>
      </div>

      <div style={{ marginTop: 14 }}>
        {mode === 'pocv' ? (
          <PocvTable id={id} pocv={pocv.data} />
        ) : (
          <DiffusionTable diffusion={diffusion.data} />
        )}
      </div>

      <div style={{ marginTop: 14 }}>
        <Card title="파일" padSmall>
          <KeyValues rows={[
            ['원본', record.original_name || '—'],
            ['크기', `${(record.size_bytes / 1e6).toFixed(1)} MB`],
            ['시작', record.start_time ? dateTime(record.start_time) : '—'],
            ['올린 때', dateTime(record.uploaded_at)],
          ]} />
        </Card>
      </div>
      <div style={{ marginTop: 14 }}>
        <OtherMeasurements sampleId={record.sample_id ?? null}
                           exclude={{ kind: 'gitt', id: record.id }} />
      </div>
    </main>
  )
}

function PocvTable({ id, pocv }: { id: number; pocv: import('../lib/types').Pocv | null }) {
  if (!pocv) return null
  const skipped = pocv.skipped_charge + pocv.skipped_discharge
  return (
    <Card title={`pOCV 점 ${pocv.charge.length + pocv.discharge.length}개`}>
      <div className="col" style={{ gap: 10 }}>
        {skipped ? (
          // 조용히 버리면 잘린 파일과 정상 파일이 곡선에서 구분되지 않는다.
          <Alert kind="warn">
            휴지가 뒤따르지 않아 뺀 펄스 {skipped}개
            {pocv.skipped_reasons.length ? ` — ${pocv.skipped_reasons.join(' · ')}` : ''}
          </Alert>
        ) : null}
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th style={{ textAlign: 'left' }}>방향</th>
                <th>용량 (mAh)</th>
                <th>전압 (V)</th>
                <th>휴지</th>
                <th>잔류 드리프트</th>
              </tr>
            </thead>
            <tbody>
              {[...pocv.charge.map((point) => ['충전', point] as const),
                ...pocv.discharge.map((point) => ['방전', point] as const)]
                .map(([branch, point], index) => (
                  <tr key={`${id}-${branch}-${index}`}>
                    <td className="text dim">{branch}</td>
                    <td>{num(point.capacity_mah, 4)}</td>
                    <td>{num(point.voltage_v, 4)}</td>
                    <td className="dim">{num(point.rest_s, 4)} s</td>
                    {/* 짧은 휴지의 전압은 OCV 가 아니다.  얼마나 아닌지. */}
                    <td className="dim">{num(point.drift_mv, 3)} mV</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </div>
    </Card>
  )
}

function DiffusionTable({
  diffusion,
}: {
  diffusion: import('../lib/types').Diffusion | null
}) {
  if (!diffusion) return null
  return (
    <Card title={`펄스 ${diffusion.total}개 · 숫자가 나온 것 ${diffusion.usable}개`}>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>용량 (mAh)</th>
              <th>D (cm²/s)</th>
              <th>ΔE_s (V)</th>
              <th>ΔE_t (V)</th>
              <th>펄스</th>
              <th>휴지</th>
              {/* 휴지 끝에서 전압이 아직 움직인 양.  D 는 그 휴지가 평형이라는
                  가정 위에 있고, 이 증거 없이 숫자만 있으면 실제보다 확실해
                  보인다 (ADR 0020). */}
              <th>드리프트 (mV)</th>
              <th>√t R²</th>
              <th style={{ textAlign: 'left' }}>왜 안 나왔나</th>
            </tr>
          </thead>
          <tbody>
            {diffusion.points.map((point, index) => (
              <tr key={index}>
                <td>{num(point.capacity_mah, 4)}</td>
                <td>{point.d_cm2_s === null ? '—' : point.d_cm2_s.toExponential(3)}</td>
                <td className="dim">{num(point.delta_es_v, 4)}</td>
                <td className="dim">{num(point.delta_et_v, 4)}</td>
                <td className="dim">{num(point.pulse_s, 4)} s</td>
                <td className="dim">
                  {point.rest_s == null ? '—' : `${num(point.rest_s, 4)} s`}
                </td>
                <td className={point.drift_mv != null && point.drift_mv > 5 ? 'warn' : 'dim'}>
                  {point.drift_mv == null ? '—' : num(point.drift_mv, 2)}
                </td>
                {/* Weppner-Huggins 의 가정이 곧 이 값이다. */}
                <td className={point.sqrt_t_r_squared >= 0.98 ? 'dim' : 'warn'}>
                  {num(point.sqrt_t_r_squared, 4)}
                </td>
                <td className="text tiny faint">{point.reason || '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )
}

const FIELDS: { key: keyof GittRun; label: string; hint: string }[] = [
  { key: 'molar_volume_cm3', label: '몰부피 V_M', hint: 'cm³/mol · 활물질' },
  { key: 'molar_mass_g', label: '몰질량 M_B', hint: 'g/mol · 활물질' },
  { key: 'active_mass_g', label: '활물질 질량', hint: 'g · 이 전극의' },
  { key: 'area_cm2', label: '계면 면적 S', hint: 'cm² · 전극/전해질' },
  { key: 'min_rest_s', label: '최소 휴지', hint: 's · 0 이면 전부 씁니다' },
]

/** 파일에 없는 값들.  D 는 이 넷의 조합의 제곱에 비례한다 (ADR 0020). */
function MaterialFields({
  record,
  onSaved,
}: {
  record: GittRun
  onSaved: () => void
}) {
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const [draft, setDraft] = useState<Record<string, string>>(() =>
    Object.fromEntries(FIELDS.map((field) => {
      const value = record[field.key]
      return [field.key, value === null || value === undefined ? '' : String(value)]
    })),
  )

  async function commit(key: string) {
    const text = (draft[key] ?? '').trim()
    const current = record[key as keyof GittRun]
    if (text === '' && (current === null || current === undefined)) return
    if (text !== '' && Number(text) === current) return
    setBusy(true)
    setError(null)
    try {
      await api.updateGittRun(record.id,
                              text === '' ? { clear: [key] } : { [key]: Number(text) })
      onSaved()
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="col" style={{ gap: 9 }}>
      {error ? <Alert kind="error">{error}</Alert> : null}
      {FIELDS.map((field) => (
        <Field key={field.key} label={field.label} hint={field.hint}>
          <input
            aria-label={field.label}
            type="number"
            min={0}
            value={draft[field.key] ?? ''}
            disabled={busy}
            onChange={(event) =>
              setDraft((current) => ({ ...current, [field.key]: event.target.value }))
            }
            onBlur={() => void commit(field.key)}
            onKeyDown={(event) => {
              if (event.key === 'Enter') event.currentTarget.blur()
            }}
          />
        </Field>
      ))}
      <div className="tiny faint">
        D 는 이 값들의 조합의 제곱에 비례합니다 — 추정한 값을 넣으면 그만큼
        틀린 숫자가 나오고, 측정한 것과 똑같이 생겼습니다.
      </div>
    </div>
  )
}
