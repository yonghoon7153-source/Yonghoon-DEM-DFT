/** 스펙트럼 하나 — 나이퀴스트, 보드, 등가회로 피팅, 파라미터.
 *
 *  절차서의 순서를 그대로 두되 사람만 뺐다: 회로를 고르고 누르면 초기값을
 *  데이터에서 만들어 여러 번 맞추고, 파라미터와 χ² 와 **신뢰구간**을 낸다.
 *  마지막 것이 이 화면의 이유다 — 수렴한 피팅이 곧 측정은 아니고, 오차가 값을
 *  삼킨 파라미터는 숫자처럼 보일 뿐이다 (ADR 0019 §7).
 */

import { useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { CopyBar } from '../components/CopyBar'
import { DrtPanel } from '../components/DrtPanel'
import { Plot, type PlotSeries } from '../components/Plot'
import { Alert, Card, Field, KeyValues, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { cellConfigFromName, dateTime, num, seriesColor, thicknessFromName }
  from '../lib/format'
import { bodeTsv, fitParametersTsv, nyquistTsv } from '../lib/origin'
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
    if (fit?.converged && fit.fitted_z_re && fit.fitted_z_im) {
      // 서버가 같은 회로 AST 로 계산한 곡선이다.  화면이 파라미터 이름으로
      // 회로를 재구성하던 때는 L·Ws·Wo·중첩이 조용히 빠져 다른 곡선이
      // "맞춤" 으로 그려졌다 (리뷰 #6).  서버가 곡선을 못 주면 선을 그리지
      // 않고 이유(fitted_note)를 아래에 적는다.
      series.push({
        label: `맞춤 (${fit.circuit})`,
        x: fit.fitted_z_re,
        y: fit.fitted_z_im.map((value) => -value),
        color: seriesColor(1),
        width: 2,
      })
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
              record.at_cycle === null
                ? null
                : record.at_cycle === 0 ? '구동 전' : `${record.at_cycle} 사이클`,
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

      {/* 절차서의 마지막 단계가 "Copy to clipboard → 엑셀 → Origin" 이다. */}
      <div style={{ marginBottom: 12 }}>
        <CopyBar
          items={[
            {
              label: '나이퀴스트',
              title: "Z′ 와 −Z″ 두 열 — Origin 에서 -col(B) 를 다시 할 필요 없다",
              disabled: !points.data,
              build: () => (points.data ? nyquistTsv([points.data]) : ''),
            },
            {
              label: '보드',
              title: '주파수 · |Z| · 위상 세 열',
              disabled: !points.data,
              build: () => (points.data ? bodeTsv([points.data]) : ''),
            },
            {
              label: '피팅 파라미터',
              title: '이름 · 값 · 1σ — 엑셀에 붙여 넣는 표',
              disabled: !fit?.parameters.length,
              build: () => fitParametersTsv(fit?.parameters ?? []),
            },
          ]}
        />
      </div>

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

      <div style={{ marginTop: 14 }}>
        <DrtPanel spectrumId={record.id} />
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
      {fit.converged && fit.fitted_note ? (
        // 곡선을 못 그린 이유.  선이 그냥 없으면 "안 맞았다" 와 구분이 안 된다.
        <Alert kind="warn">맞춤 곡선 없음 — {fit.fitted_note}</Alert>
      ) : null}

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
    <div className="col" style={{ gap: 6 }}>
      <KeyValues
        rows={[
          ['벌크 σ', value.bulk_s_cm ? `${value.bulk_s_cm.toExponential(3)} S/cm` : '—'],
          ['입계 σ', value.grain_boundary_s_cm ? `${value.grain_boundary_s_cm.toExponential(3)} S/cm` : '—'],
          // 두 σ 의 합이 아니다 — 저항이 직렬이므로 저항을 더해서 나눈다.
          ['전체 σ', value.total_s_cm ? `${value.total_s_cm.toExponential(3)} S/cm` : '—'],
        ]}
      />
      {value.excluded?.length ? (
        // 세 번째 아크는 전극 계면일 수 있어 전해질 σ 에 넣지 않는다.
        // 조용히 빼면 회로를 바꿨을 때 σ 가 왜 움직였는지 알 수 없다.
        <div className="tiny faint">σ 합계에서 뺀 아크: {value.excluded.join(' · ')}</div>
      ) : null}
    </div>
  )
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
  // 셀 목록은 붙일 때만 필요하다.  화면을 열 때마다 받아 두면 스펙트럼만
  // 보려는 사람도 셀 전체를 한 번 받아 온다.
  const samples = useAsync(() => api.listSamples(), [])
  const [thickness, setThickness] = useState(
    record.thickness_um === null ? '' : String(record.thickness_um),
  )
  const [cycle, setCycle] = useState(
    record.at_cycle === null ? '' : String(record.at_cycle),
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

      {/* 셀에 붙이는 자리.  API 는 처음부터 됐는데 화면이 읽기만 해서, 셀
          상세의 임피던스 카드가 영영 비어 있었다 — 붙일 방법이 없으니까. */}
      <Field label="셀" hint="붙이면 셀 화면에서 함께 보입니다">
        <select
          aria-label="셀"
          value={record.sample_id ?? ''}
          disabled={busy || samples.loading}
          onChange={(event) => void save(
            event.target.value === ''
              ? { clear: ['sample_id'] }
              : { sample_id: Number(event.target.value) },
          )}
        >
          <option value="">— 안 붙임</option>
          {(samples.data ?? []).map((sample) => (
            <option key={sample.id} value={sample.id}>
              {sample.name}
            </option>
          ))}
        </select>
      </Field>

      <Field label="사이클" hint="구동 전은 0 · 비우면 안 적음 · Enter 로 적용">
        <input
          aria-label="사이클"
          type="number"
          min={0}
          value={cycle}
          disabled={busy}
          onChange={(event) => setCycle(event.target.value)}
          onBlur={() => {
            const value = cycle.trim()
            if (value === '' && record.at_cycle === null) return
            if (value !== '' && Number(value) === record.at_cycle) return
            void save(value === ''
              ? { clear: ['at_cycle'] }
              : { at_cycle: Number(value) })
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter') event.currentTarget.blur()
          }}
        />
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
