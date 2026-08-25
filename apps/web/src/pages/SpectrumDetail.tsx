/** 스펙트럼 하나 — 나이퀴스트, 보드, 등가회로 피팅, 파라미터.
 *
 *  절차서의 순서를 그대로 두되 사람만 뺐다: 회로를 고르고 누르면 초기값을
 *  데이터에서 만들어 여러 번 맞추고, 파라미터와 χ² 와 **신뢰구간**을 낸다.
 *  마지막 것이 이 화면의 이유다 — 수렴한 피팅이 곧 측정은 아니고, 오차가 값을
 *  삼킨 파라미터는 숫자처럼 보일 뿐이다 (ADR 0019 §7).
 */

import { useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { Plot, type PlotSeries } from '../components/Plot'
import { Alert, Card, Field, KeyValues, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { cellConfigFromName, dateTime, num, seriesColor, thicknessFromName }
  from '../lib/format'
import { useAsync } from '../lib/hooks'
import type { CellConfig, CircuitKind, EisKind, SpectrumDetail as Detail, SpectrumFit }
  from '../lib/types'
import { frequencySpan, hertz } from './Eis'

const KIND_LABEL: Record<EisKind, string> = { liquid: '액체 전해질', solid: '전고체' }

export function SpectrumDetail() {
  const params = useParams<{ id: string }>()
  const id = Number(params.id)

  const [circuit, setCircuit] = useState('')
  const [dropInductive, setDropInductive] = useState(true)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [reloadKey, bumpReload] = useState(false)
  const [showFit, setShowFit] = useState<number | null>(null)

  const spectrum = useAsync(() => api.getSpectrum(id), [id, reloadKey])
  const points = useAsync(() => api.spectrumPoints(id), [id])
  const circuits = useAsync(() => api.eisCircuits(), [])

  const record = spectrum.data
  const kinds: CircuitKind[] = circuits.data?.kinds ?? []
  const presets = kinds.find((entry) => entry.kind === record?.kind)?.presets ?? []
  const chosenCircuit = circuit || record?.last_circuit || presets[0]?.circuit || ''

  // `record?.fits ?? []` 를 그대로 두면 매 렌더마다 새 배열이라 아래 useMemo 가
  // 절대 재사용되지 않는다 — 그래프가 마우스를 움직일 때마다 다시 그려진다.
  const fits = useMemo(() => record?.fits ?? [], [record])
  const fit = useMemo(
    () => fits.find((item) => item.id === showFit) ?? fits[0] ?? null,
    [fits, showFit],
  )

  const nyquist = useMemo<PlotSeries[]>(() => {
    if (!points.data) return []
    const series: PlotSeries[] = [{
      label: '측정',
      x: points.data.z_re,
      // 나이퀴스트 세로축은 −Z″ 다.  허수부를 그대로 그리면 아크가 아래로
      // 뒤집혀서, 파일이 왜 −Im(Z) 를 저장하는지가 화면에서 되풀이된다.
      y: points.data.z_im.map((value) => -value),
      color: seriesColor(0),
      points: true,
      width: 0,
    }]
    if (fit?.converged && fit.parameters.length) {
      const curve = fitCurve(fit, points.data.frequency_hz)
      if (curve) {
        series.push({
          label: `맞춤 (${fit.circuit})`,
          x: curve.re,
          y: curve.negIm,
          color: seriesColor(1),
          width: 2,
        })
      }
    }
    return series
  }, [points.data, fit])

  const bode = useMemo<PlotSeries[]>(() => {
    if (!points.data) return []
    return [
      {
        label: '|Z| (Ω)',
        x: points.data.frequency_hz,
        y: points.data.magnitude,
        color: seriesColor(0),
        points: true,
        width: 1,
      },
      {
        label: '위상 (°)',
        x: points.data.frequency_hz,
        y: points.data.phase_deg,
        color: seriesColor(2),
        points: true,
        width: 1,
      },
    ]
  }, [points.data])

  async function runFit() {
    if (!record) return
    setBusy(true)
    setError(null)
    try {
      const made = await api.fitSpectrum(record.id, {
        circuit: chosenCircuit || undefined,
        drop_inductive: dropInductive,
      })
      setShowFit(made.id)
      bumpReload((value) => !value)
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause))
    } finally {
      setBusy(false)
    }
  }

  if (spectrum.error) return <main className="page"><Alert kind="error">{spectrum.error}</Alert></main>
  if (!record) return <main className="page"><Spinner label="불러오는 중" /></main>

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1 className="truncate">{record.name}</h1>
          <div className="sub">
            {[
              KIND_LABEL[record.kind],
              `${record.n_points}점`,
              frequencySpan(record),
              record.device || null,
              record.amplitude_mv ? `${record.amplitude_mv} mV` : null,
            ]
              .filter(Boolean)
              .join('  ·  ')}
          </div>
        </div>
        <span className="spacer" />
        <div className="row">
          <Link className="link-btn" to="/eis">
            목록
          </Link>
          {record.sample_id ? (
            <Link className="link-btn" to={`/samples/${record.sample_id}`}>
              셀 {record.sample_name}
            </Link>
          ) : null}
        </div>
      </div>

      {error ? <Alert kind="error">{error}</Alert> : null}

      <div className="grid cols-2">
        <Card title="나이퀴스트">
          {points.error ? (
            <Alert kind="error">{points.error}</Alert>
          ) : nyquist.length ? (
            <Plot
              series={nyquist}
              xLabel="Z′ (Ω)"
              yLabel="−Z″ (Ω)"
              height={360}
              legend
              // 반원이 반원으로 보여야 찌그러진 아크를 알아본다.
              equalAspect
            />
          ) : (
            <Spinner />
          )}
        </Card>

        <Card title="보드">
          {bode.length ? (
            <Plot series={bode} xLabel="주파수 (Hz)" yLabel="|Z| (Ω) · 위상 (°)"
                  height={360} legend />
          ) : (
            <Spinner />
          )}
        </Card>
      </div>

      <div className="grid cols-2" style={{ marginTop: 14 }}>
        <Card title="등가회로 피팅">
          <div className="col" style={{ gap: 10 }}>
            <Field label="회로" hint="비우면 이 종류의 기본 회로">
              <input
                aria-label="회로"
                className="mono"
                value={chosenCircuit}
                onChange={(event) => setCircuit(event.target.value)}
                placeholder="R0-p(R1,CPE1)-p(R2,CPE2)"
              />
            </Field>
            <div className="col" style={{ gap: 4 }}>
              {presets.map((preset) => (
                <button
                  key={preset.circuit}
                  type="button"
                  className="ghost"
                  style={{ textAlign: 'left' }}
                  onClick={() => setCircuit(preset.circuit)}
                >
                  <span className="mono">{preset.circuit}</span>
                  <span className="tiny faint"> — {preset.label}</span>
                  <div className="tiny faint">{preset.note}</div>
                </button>
              ))}
            </div>
            <label className="row" style={{ gap: 6 }}>
              <input
                type="checkbox"
                checked={dropInductive}
                onChange={(event) => setDropInductive(event.target.checked)}
              />
              <span className="tiny">
                고주파 유도성 점 빼기 — 배선이지 셀이 아닙니다
              </span>
            </label>
            <div className="row">
              <button type="button" className="primary" disabled={busy} onClick={() => void runFit()}>
                {busy ? '맞추는 중…' : '맞추기'}
              </button>
              {fits.length > 1 ? (
                <select
                  aria-label="지난 피팅"
                  value={fit?.id ?? ''}
                  onChange={(event) => setShowFit(Number(event.target.value))}
                >
                  {fits.map((item) => (
                    <option key={item.id} value={item.id}>
                      {item.circuit} · χ² {item.chi_squared === null ? '—' : num(item.chi_squared, 3)}
                    </option>
                  ))}
                </select>
              ) : null}
            </div>
          </div>
        </Card>

        <Card title="파라미터">
          {fit ? <FitReport fit={fit} kind={record.kind} /> : (
            <div className="tiny faint" style={{ padding: 4 }}>
              아직 맞춘 적이 없습니다.
            </div>
          )}
        </Card>
      </div>

      <div className="grid cols-2" style={{ marginTop: 14 }}>
        <Card title="셀" padSmall>
          <CellFields record={record} onSaved={() => bumpReload((value) => !value)} />
        </Card>

        <Card title="측정 정보" padSmall>
          <KeyValues
            rows={[
              ['파일', record.original_name || '—'],
              ['형식', record.source_format || '—'],
              ['테크닉', record.technique || '—'],
              ['주파수', frequencySpan(record)],
              ['진폭', record.amplitude_mv ? `${record.amplitude_mv} mV` : '—'],
              ['면적', record.area_cm2_effective ? `${num(record.area_cm2_effective, 4)} cm²` : '—'],
              ['올린 때', dateTime(record.uploaded_at)],
            ]}
          />
        </Card>
      </div>
    </main>
  )
}

function FitReport({ fit, kind }: { fit: SpectrumFit; kind: EisKind }) {
  const arcs = new Map(fit.arcs.map((arc) => [arc.parameter, arc]))
  return (
    <div className="col" style={{ gap: 10 }}>
      {!fit.converged ? (
        <Alert kind="error">맞추지 못했습니다 — {fit.reason}</Alert>
      ) : null}
      {fit.kind !== fit.kind_now ? (
        <Alert kind="warn">
          이 피팅은 {KIND_LABEL[fit.kind]} 로 맞춘 것입니다. 지금 이름은{' '}
          {KIND_LABEL[fit.kind_now]} 기준으로 붙어 있습니다 — 다시 맞추면 확실합니다.
        </Alert>
      ) : null}
      {fit.converged && fit.reason ? <Alert kind="warn">{fit.reason}</Alert> : null}

      <div className="row tiny faint" style={{ gap: 12, flexWrap: 'wrap' }}>
        <span className="mono">{fit.circuit}</span>
        <span>χ² {fit.chi_squared === null ? '—' : num(fit.chi_squared, 4)}</span>
        <span>
          시작점 {fit.starts_converged}/{fit.starts}
        </span>
        {fit.dropped_inductive ? <span>유도성 {fit.dropped_inductive}점 뺌</span> : null}
        {fit.frequency_low_hz && fit.frequency_high_hz ? (
          <span>
            {hertz(fit.frequency_high_hz)} → {hertz(fit.frequency_low_hz)}
          </span>
        ) : null}
      </div>

      {fit.parameters.length ? (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th style={{ textAlign: 'left' }}>파라미터</th>
                <th style={{ textAlign: 'left' }}>뜻</th>
                <th>값</th>
                <th>± 1σ</th>
              </tr>
            </thead>
            <tbody>
              {fit.parameters.map((parameter) => {
                const arc = arcs.get(parameter.name)
                return (
                  <tr key={parameter.name}>
                    <td className="text mono">{parameter.name}</td>
                    <td className="text dim" title={arc?.note}>
                      {arc?.label ?? '—'}
                    </td>
                    <td className={parameter.determined ? '' : 'faint'}>
                      {num(parameter.value, 4)} {parameter.unit}
                      {parameter.determined ? null : (
                        // 숫자처럼 보이는 것이 문제이므로 숫자 옆에 붙인다.
                        <span className="tiny warn"> 미결정</span>
                      )}
                    </td>
                    <td className="dim">
                      {parameter.stderr === null ? '—' : num(parameter.stderr, 2)}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      ) : null}

      {kind === 'solid' ? <Conductivity fit={fit} /> : null}
    </div>
  )
}

function Conductivity({ fit }: { fit: SpectrumFit }) {
  const value = fit.conductivity ?? {}
  if (value.missing?.length) {
    return (
      <Alert kind="info">
        전도도를 내려면 {value.missing.join(' · ')} 이(가) 필요합니다 — 셀이나
        스펙트럼에 적어 주세요.
      </Alert>
    )
  }
  return (
    <KeyValues
      rows={[
        ['벌크 σ', value.bulk_s_cm ? `${value.bulk_s_cm.toExponential(3)} S/cm` : '—'],
        ['입계 σ', value.grain_boundary_s_cm ? `${value.grain_boundary_s_cm.toExponential(3)} S/cm` : '—'],
        // 두 σ 의 합이 아니다 — 저항이 직렬이므로 저항을 더해서 나눈다.
        ['전체 σ', value.total_s_cm ? `${value.total_s_cm.toExponential(3)} S/cm` : '—'],
      ]}
    />
  )
}

/** 맞춘 회로를 측정 주파수 위에 다시 그린다.
 *
 *  서버가 곡선을 보내지 않고 파라미터만 보내므로 여기서 계산한다.  회로 문자열을
 *  다시 해석하지 않고 **아크 목록**을 쓰는 것은, 화면이 회로 파서를 하나 더
 *  갖게 되면 서버와 조용히 어긋나기 때문이다.  지원하는 모양은 서버가 프리셋으로
 *  내주는 것들 — 직렬 R 과 R‖CPE 들, 그리고 끝의 CPE 나 W.
 */
function fitCurve(fit: SpectrumFit, frequency: number[]):
  { re: number[]; negIm: number[] } | null {
  const values = new Map(fit.parameters.map((p) => [p.name, p.value]))
  const names = fit.parameters.map((p) => p.name)
  const plainR = names.filter((name) => !name.includes('_') && name.startsWith('R'))
  const cpeStems = names
    .filter((name) => name.endsWith('_Q'))
    .map((name) => name.slice(0, -2))
  if (!plainR.length && !cpeStems.length) return null

  const hasSeries = fit.circuit.trim().startsWith('R') && !fit.circuit.trim().startsWith('p(')
  const seriesR = hasSeries ? values.get(plainR[0]!) ?? 0 : 0
  const arcRs = hasSeries ? plainR.slice(1) : plainR

  const re: number[] = []
  const negIm: number[] = []
  for (const hz of frequency) {
    const w = 2 * Math.PI * hz
    let zr = seriesR
    let zi = 0
    for (let i = 0; i < arcRs.length; i += 1) {
      const r = values.get(arcRs[i]!) ?? 0
      const stem = cpeStems[i]
      const q = stem ? values.get(`${stem}_Q`) ?? 0 : 0
      const n = stem ? values.get(`${stem}_n`) ?? 1 : 1
      const [pr, pi] = parallelRCpe(r, q, n, w)
      zr += pr
      zi += pi
    }
    // 남은 CPE (전고체의 블로킹 꼬리) 는 직렬로 붙는다.
    for (let i = arcRs.length; i < cpeStems.length; i += 1) {
      const stem = cpeStems[i]!
      const [cr, ci] = cpe(values.get(`${stem}_Q`) ?? 0, values.get(`${stem}_n`) ?? 1, w)
      zr += cr
      zi += ci
    }
    const warburg = names.find((name) => !name.includes('_') && name.startsWith('W'))
    if (warburg) {
      const sigma = values.get(warburg) ?? 0
      zr += sigma / Math.sqrt(w)
      zi -= sigma / Math.sqrt(w)
    }
    re.push(zr)
    negIm.push(-zi)
  }
  return { re, negIm }
}

/** CPE 임피던스: `1 / (Q (jw)^n)` — 극형식으로 풀어 쓴다. */
function cpe(q: number, n: number, w: number): [number, number] {
  if (!q || !w) return [0, 0]
  const magnitude = 1 / (q * Math.pow(w, n))
  const angle = -(n * Math.PI) / 2
  return [magnitude * Math.cos(angle), magnitude * Math.sin(angle)]
}

function parallelRCpe(r: number, q: number, n: number, w: number): [number, number] {
  if (!q) return [r, 0]
  // Y = 1/R + Q(jw)^n, then Z = 1/Y.
  const yr = (r ? 1 / r : 0) + q * Math.pow(w, n) * Math.cos((n * Math.PI) / 2)
  const yi = q * Math.pow(w, n) * Math.sin((n * Math.PI) / 2)
  const denominator = yr * yr + yi * yi
  if (!denominator) return [0, 0]
  return [yr / denominator, -yi / denominator]
}


const CONFIG_OPTIONS: { value: CellConfig | ''; label: string }[] = [
  { value: '', label: '— 안 정함' },
  { value: 'sym', label: '대칭셀' },
  { value: 'full', label: '풀셀' },
  { value: 'half', label: '하프셀' },
]

const CONFIG_LABEL: Record<string, string> = {
  sym: '대칭셀', full: '풀셀', half: '하프셀', '': '안 정함',
}

/** 셀 구성과 두께 — 아크의 이름과 전도도가 여기에 걸려 있다.
 *
 *  이름에 대개 적혀 있지만(`..._70um_sym_01`) 채워 넣지는 않는다.  이름은
 *  누군가 그렇게 부르기로 한 것이지 기록이 아니고, 오타에서 나온 전도도는
 *  측정된 것과 똑같이 생겼다.  활물질 질량과 같은 방식으로 `#` 참고 표시만
 *  옆에 둔다.
 */
function CellFields({
  record,
  onSaved,
}: {
  record: Detail
  onSaved: () => void
}) {
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const [thickness, setThickness] = useState(
    record.thickness_um === null ? '' : String(record.thickness_um),
  )

  const namedThickness = thicknessFromName(record.name) ?? thicknessFromName(record.original_name)
  const namedConfig = cellConfigFromName(record.name) ?? cellConfigFromName(record.original_name)

  async function save(body: Record<string, unknown>) {
    setBusy(true)
    setError(null)
    try {
      await api.updateSpectrum(record.id, body)
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

      <Field
        label="셀 구성"
        hint="아크의 이름을 정합니다"
        note={
          namedConfig && namedConfig !== record.cell_config ? (
            <span title="파일 이름에 적힌 값">#{CONFIG_LABEL[namedConfig]}</span>
          ) : undefined
        }
      >
        <select
          aria-label="셀 구성"
          value={record.cell_config}
          disabled={busy}
          onChange={(event) => void save({ cell_config: event.target.value })}
        >
          {CONFIG_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </Field>

      <Field
        label="두께"
        hint="µm · 전도도의 분자 · Enter 로 적용"
        note={
          namedThickness !== null && namedThickness !== record.thickness_um ? (
            <span title="파일 이름에 적힌 값">#{namedThickness}µm</span>
          ) : undefined
        }
      >
        <input
          aria-label="두께"
          type="number"
          min={0}
          value={thickness}
          disabled={busy}
          onChange={(event) => setThickness(event.target.value)}
          onBlur={() => {
            const value = thickness.trim()
            if (value === '' && record.thickness_um === null) return
            if (Number(value) === record.thickness_um) return
            void save(value === ''
              ? { clear: ['thickness_um'] }
              : { thickness_um: Number(value) })
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter') event.currentTarget.blur()
          }}
        />
      </Field>

      <div className="tiny faint">
        {record.kind === 'solid' && record.cell_config !== 'sym'
          ? '전도도는 이온 블로킹 대칭셀에서만 냅니다 — 풀셀의 저주파 아크는 계면입니다.'
          : '전도도는 조회할 때 계산합니다 — 두께를 고치면 바로 따라옵니다.'}
      </div>
    </div>
  )
}
