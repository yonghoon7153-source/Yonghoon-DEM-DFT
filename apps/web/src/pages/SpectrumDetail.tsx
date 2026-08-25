/** 스펙트럼 하나 — 나이퀴스트, 보드, 등가회로 피팅, 파라미터.
 *
 *  절차서의 순서를 그대로 두되 사람만 뺐다: 회로를 고르고 누르면 초기값을
 *  데이터에서 만들어 여러 번 맞추고, 파라미터와 χ² 와 **신뢰구간**을 낸다.
 *  마지막 것이 이 화면의 이유다 — 수렴한 피팅이 곧 측정은 아니고, 오차가 값을
 *  삼킨 파라미터는 숫자처럼 보일 뿐이다 (ADR 0019 §7).
 */

import { OtherMeasurements } from '../components/OtherMeasurements'
import { RelatedCellCard } from '../components/RelatedCell'
import { useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { CopyBar } from '../components/CopyBar'
import { DrtPanel } from '../components/DrtPanel'
import { Plot, type PlotSeries } from '../components/Plot'
import { Alert, Card, Field, KeyValues, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { areaUnit, perArea, scalesWithArea } from '../lib/areanorm'
import { cellConfigFromName, dateTime, num, seriesColor, thicknessFromName }
  from '../lib/format'
import { inductiveCount, nyquistXy } from '../lib/eis'
import { bodeTsv, fitParametersTsv, nyquistTsv } from '../lib/origin'
import { useAsync } from '../lib/hooks'
import type { CellConfig, CircuitKind, CircuitPreset, EisKind, SpectrumDetail as Detail, SpectrumFit }
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
  // 관계셀 드롭다운이 쓸 목록.  아래 카드가 이 화면에서 붙이거나 뗄 수 있게.
  const allSamples = useAsync(() => api.listSamples(), [])

  const record = spectrum.data
  const kinds: CircuitKind[] = circuits.data?.kinds ?? []
  // 회로 프리셋은 **여섯 조합**을 따른다 (액체/전고체 × 풀셀·하프셀·대칭셀).
  // 아크의 이름이 이미 이 축에서 갈리므로 회로도 같이 갈린다 — 리튬 대극
  // 하프셀은 대극 계면이 아크를 하나 더 얹고, 대칭셀은 아크가 두 배다.
  const combinations = circuits.data?.combinations ?? []
  const presets: CircuitPreset[] =
    combinations.find(
      (entry) => entry.kind === record?.kind && entry.cell_config === record?.cell_config,
    )?.presets
    ?? kinds.find((entry) => entry.kind === record?.kind)?.presets
    ?? []
  const chosenCircuit = circuit || record?.last_circuit || presets[0]?.circuit || ''

  // `record?.fits ?? []` 를 그대로 두면 매 렌더마다 새 배열이라 아래 useMemo 가
  // 절대 재사용되지 않는다 — 그래프가 마우스를 움직일 때마다 다시 그려진다.
  const fits = useMemo(() => record?.fits ?? [], [record])
  const fit = useMemo(
    () => fits.find((item) => item.id === showFit) ?? fits[0] ?? null,
    [fits, showFit],
  )

  /** 면적이 적혀 있으면 Ω → Ω·cm².  없으면 1 배 (= 안 나눈다).
   *
   *  같은 전극이라도 지름 10 mm 와 16 mm 는 저항이 2.5 배 다르다.  셀끼리
   *  비교하려면 면적으로 나눈 값이라야 하고, 논문의 값도 대개 그것이다.
   *  **모르면 안 나눈다** — 추정 면적으로 나눈 수는 실측 ASR 과 똑같이 생겼다
   *  (§0.4).  그래서 면적을 적는 순간 세 곳이 한꺼번에 바뀐다: 나이퀴스트,
   *  보드의 |Z|, 그리고 피팅 파라미터의 저항들.
   */
  const area = record?.area_cm2_effective ?? null
  const zUnit = area ? 'Ω·cm²' : 'Ω'

  const nyquist = useMemo<PlotSeries[]>(() => {
    if (!points.data) return []
    // 세로축은 −Z″ 다.  허수부를 그대로 그리면 아크가 아래로 뒤집혀서,
    // 파일이 왜 −Im(Z) 를 저장하는지가 화면에서 되풀이된다.
    const measured = nyquistXy(points.data.z_re, points.data.z_im, dropInductive,
                               (value) => perArea(value, area))
    const series: PlotSeries[] = [{
      label: '측정',
      x: measured.x,
      y: measured.y,
      color: seriesColor(0),
      points: true,
      width: 0,
    }]
    if (fit?.converged && fit.fitted_z_re && fit.fitted_z_im) {
      // 서버가 같은 회로 AST 로 계산한 곡선이다.  화면이 파라미터 이름으로
      // 회로를 재구성하던 때는 L·Ws·Wo·중첩이 조용히 빠져 다른 곡선이
      // "맞춤" 으로 그려졌다 (리뷰 #6).  서버가 곡선을 못 주면 선을 그리지
      // 않고 이유(fitted_note)를 아래에 적는다.
      // 맞춤 곡선도 같은 규칙으로 자른다.  회로에 L 이 있으면 이 곡선도
      // 고주파에서 유도성이라, 측정만 자르면 맞춤선 혼자 밑으로 꽂힌다.
      const fitted = nyquistXy(fit.fitted_z_re, fit.fitted_z_im, dropInductive,
                               (value) => perArea(value, area))
      series.push({
        label: `맞춤 (${fit.circuit})`,
        x: fitted.x,
        y: fitted.y,
        color: seriesColor(1),
        width: 2,
      })
    }
    return series
  }, [points.data, fit, area, dropInductive])

  const inductive = useMemo(
    () => (points.data ? inductiveCount(points.data.z_im) : 0), [points.data])

  // 보드는 두 패널이다 (리뷰 #27).  8 decade 의 주파수를 선형 x 에 놓으면
  // 10 kHz 아래 전부가 폭 1% 에 뭉치고, Ω 와 도(°)를 한 선형 y 에 겹치면
  // 위상이 바닥에 눕는다 — 내보내기 코드가 이미 "두 y 단위는 쌓을 수 없다"
  // 라고 말하는 그대로다.  x 는 log₁₀ f, |Z| 도 decade 를 넘나드니 log₁₀.
  const bodeMagnitude = useMemo<PlotSeries[]>(() => {
    if (!points.data) return []
    return [
      {
        label: `log₁₀|Z| (${zUnit})`,
        x: points.data.frequency_hz.map((value) => Math.log10(value)),
        // |Z| 도 임피던스라 같이 나눈다.  위상은 무차원이라 그대로다.
        y: points.data.magnitude.map((value) => Math.log10(perArea(value, area))),
        color: seriesColor(0),
        points: true,
        width: 1,
      },
    ]
  }, [points.data, area, zUnit])
  const bodePhase = useMemo<PlotSeries[]>(() => {
    if (!points.data) return []
    return [
      {
        label: '위상 (°)',
        x: points.data.frequency_hz.map((value) => Math.log10(value)),
        y: points.data.phase_deg,
        color: seriesColor(2),
        points: true,
        width: 1,
      },
    ]
  }, [points.data])

  async function runFit(mode?: 'auto') {
    if (!record) return
    setBusy(true)
    setError(null)
    try {
      const made = await api.fitSpectrum(record.id, {
        circuit: mode === 'auto' ? 'auto' : (chosenCircuit || undefined),
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

      <div style={{ marginBottom: 14 }}>
        <RelatedCellCard
          sampleId={record.sample_id}
          sampleName={record.sample_name}
          samples={allSamples.data ?? []}
          record={record}
          onSaveConditions={async (body) => {
            await api.updateSpectrum(record.id, body)
            bumpReload((value) => !value)
          }}
          onPick={async (picked) => {
            // 빈 값은 떼어내기다 -- `sample_id: null` 은 "안 보냄" 과 구별되지
            // 않아 서버가 clear 를 따로 받는다.
            await api.updateSpectrum(record.id, picked
              ? { sample_id: picked }
              : { clear: ['sample_id'] })
            bumpReload((value) => !value)
          }}
        />
      </div>

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
              xLabel={`Z′ (${zUnit})`}
              yLabel={`−Z″ (${zUnit})`}
              height={360}
              legend
              // 반원이 반원으로 보여야 찌그러진 아크를 알아본다.
              equalAspect
              positiveFit
            />
          ) : (
            <Spinner />
          )}
          {/* 뺐으면 뺐다고 적는다 (ADR 0019).  스위치를 여기 또 만들지는
              않는다 -- 아래 피팅 설정의 것과 같은 뜻이고, 둘이 따로 놀면
              그림과 맞춘 곡선이 서로 다른 점 위에 서게 된다. */}
          {inductive ? (
            <div className="tiny faint" style={{ paddingTop: 8 }}>
              {dropInductive
                ? `실수축 위의 점 ${inductive}개를 뺐습니다 — 고주파에서 Z″ 가 `
                  + '양수인 구간 (케이블·셀 홀더의 인덕턴스). 아래 "고주파 유도성 점 '
                  + '빼기" 를 끄면 그대로 보입니다.'
                : `실수축 위에 점 ${inductive}개가 있습니다 — 아크 밑으로 꽂히는 `
                  + '수직선이 그것입니다. 아래 "고주파 유도성 점 빼기" 로 뺄 수 있습니다.'}
            </div>
          ) : null}
        </Card>

        <Card title="보드">
          {bodeMagnitude.length ? (
            <div className="col" style={{ gap: 6 }}>
              <Plot series={bodeMagnitude} xLabel="log₁₀ f (Hz)"
                    yLabel={`log₁₀|Z| (${zUnit})`} height={180} legend />
              <Plot series={bodePhase} xLabel="log₁₀ f (Hz)" yLabel="위상 (°)"
                    height={180} legend />
            </div>
          ) : (
            <Spinner />
          )}
        </Card>
      </div>

      <div className="fit-row" style={{ marginTop: 14 }}>
        {/* 왼쪽 기둥: 이 스펙트럼이 무엇의 것인가.  파라미터 표 바로 옆에
            있어야 "이 값이 어느 셀·어느 면적의 것인가" 를 눈만 옮겨 본다. */}
        <div className="col" style={{ gap: 14 }}>
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
                ['면적', record.area_cm2_effective
                  ? `${num(record.area_cm2_effective, 4)} cm²` : '—'],
                ['올린 때', dateTime(record.uploaded_at)],
              ]}
            />
          </Card>
        </div>

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
            <div className="col preset-list" style={{ gap: 4 }}>
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
                <span className="faint"> · 위 나이퀴스트도 함께 바뀝니다</span>
              </span>
            </label>
            <div className="row">
              <button type="button" className="primary" disabled={busy} onClick={() => void runFit()}>
                {busy ? '맞추는 중…' : '맞추기'}
              </button>
              {/* 사람이 하던 일이 그대로 이것이다: 회로를 바꿔 가며 몇 번 맞춰
                  보고 χ² 를 본다.  전부 저장되므로 아래 '지난 피팅' 에서
                  나란히 볼 수 있다. */}
              <button type="button" disabled={busy}
                      title="이 조합의 프리셋을 전부 맞춰 보고 χ² 가 가장 작은 것을 보여 줍니다"
                      onClick={() => void runFit('auto')}>
                {busy ? '…' : '자동으로 고르기'}
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
          {fit ? <FitReport fit={fit} kind={record.kind} area={area} /> : (
            <div className="tiny faint" style={{ padding: 4 }}>
              아직 맞춘 적이 없습니다.
            </div>
          )}
        </Card>
      </div>

      <div style={{ marginTop: 14 }}>
        <DrtPanel spectrumId={record.id} />
      </div>

      <div style={{ marginTop: 14 }}>
        <OtherMeasurements sampleId={record.sample_id}
                           exclude={{ kind: 'eis', id: record.id }} />
      </div>
    </main>
  )
}

function FitReport({ fit, kind, area }: {
  fit: SpectrumFit
  kind: EisKind
  /** 면적이 있으면 저항 파라미터를 Ω·cm² 로 (없으면 null). */
  area: number | null
}) {
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
                      {/* 저항만 나눈다.  CPE 의 S·sⁿ 는 오히려 곱해야 하고 그
                          규칙이 지수 n 에 따라 달라서, 여기서 조용히 처리하면
                          틀린 수가 맞는 수와 같은 모습으로 나온다 (§0.4). */}
                      {num(perArea(parameter.value, scalesWithArea(parameter.unit)
                        ? area : null), 4)} {areaUnit(parameter.unit, area)}
                      {parameter.determined ? null : (
                        // 숫자처럼 보이는 것이 문제이므로 숫자 옆에 붙인다.
                        <span className="tiny warn"> 미결정</span>
                      )}
                    </td>
                    <td className="dim">
                      {parameter.stderr === null ? '—' : num(
                        perArea(parameter.stderr,
                                scalesWithArea(parameter.unit) ? area : null), 2)}
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
  const [area, setArea] = useState(
    record.area_cm2 === null ? '' : String(record.area_cm2),
  )
  const [diameter, setDiameter] = useState(
    record.diameter_mm === null || record.diameter_mm === undefined
      ? '' : String(record.diameter_mm),
  )
  const [cycle, setCycle] = useState(
    record.at_cycle === null ? '' : String(record.at_cycle),
  )
  const [purpose, setPurpose] = useState(record.purpose ?? '')

  /** 지름이 말하는 면적.  화면에만 쓴다 -- 저장은 raw(지름)만 한다 (§0.1). */
  const diameterArea = useMemo(() => {
    const value = Number(diameter.trim())
    if (!diameter.trim() || !Number.isFinite(value) || value <= 0) return null
    const radiusCm = value / 20
    return Math.PI * radiusCm * radiusCm
  }, [diameter])

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

      {/* 액체/전고체 × 풀셀·하프셀·대칭셀 — 여섯 조합을 한 번에 고른다.
          둘을 따로 고르게 두면 "액체 · 미정" 같은 반쯤 정해진 상태가 남는데,
          아크의 이름도 기본 회로도 두 축이 **함께** 정해져야 나온다.  종류를
          바꾸면 기존 피팅에는 옛 종류가 남는다 (그 사실은 아래가 말한다). */}
      <Field
        label="측정 구성"
        hint="아크의 이름과 기본 회로가 여기서 정해집니다"
        note={
          namedConfig && namedConfig !== record.cell_config ? (
            <span title="파일 이름에 적힌 값">#{CONFIG_LABEL[namedConfig]}</span>
          ) : undefined
        }
      >
        <select
          aria-label="측정 구성"
          value={`${record.kind}|${record.cell_config}`}
          disabled={busy}
          onChange={(event) => {
            const [kind, cellConfig] = event.target.value.split('|')
            void save({ kind, cell_config: cellConfig })
          }}
        >
          {(['liquid', 'solid'] as const).map((kind) =>
            CONFIG_OPTIONS.map((option) => (
              <option key={`${kind}|${option.value}`} value={`${kind}|${option.value}`}>
                {kind === 'liquid' ? '액체' : '전고체'} ·{' '}
                {option.value === '' ? '구성 미정' : CONFIG_LABEL[option.value]}
              </option>
            )),
          )}
        </select>
      </Field>

      {/* 무엇을 보려고 잰 측정인가.  자유 입력이되 흔한 것은 한 번에 —
          랩이 새 목적을 계속 만들어서 목록을 고정하면 그때마다 코드를
          고쳐야 한다.  SOC 스캔처럼 파일이 스스로 말하는 것은 업로드가
          채워 둔다 (§0.3). */}
      <Field label="목적" hint="무엇을 보려고 잰 측정인가 · Enter 로 적용">
        <input
          aria-label="목적"
          list="eis-purposes"
          value={purpose}
          disabled={busy}
          placeholder="예: SOC별, 200 사이클, 온도별"
          onChange={(event) => setPurpose(event.target.value)}
          onBlur={() => {
            if (purpose.trim() === record.purpose) return
            void save({ purpose: purpose.trim() })
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter') event.currentTarget.blur()
          }}
        />
        <datalist id="eis-purposes">
          <option value="SOC별" />
          <option value="사이클별" />
          <option value="200 사이클" />
          <option value="구동 전" />
          <option value="온도별" />
        </datalist>
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

      {/* 지름이 먼저다.  캘리퍼로 재는 것은 지름이고 면적은 거기서 나오는
          수인데, 면적만 물어 보면 사람이 매번 πd²/4 를 손으로 계산해서 넣는다.
          비어 있는 면적은 이 값에서 나오고, 면적을 직접 적으면 그것이 이긴다
          (원이 아닌 전극이 있다). */}
      <Field
        label="지름"
        hint={diameterArea === null
          ? 'mm · 원형 펠릿 · 면적이 여기서 나옵니다'
          : `mm · 면적 ${num(diameterArea, 4)} cm²`}
      >
        <input
          aria-label="지름"
          type="number"
          min={0}
          step="any"
          value={diameter}
          disabled={busy}
          onChange={(event) => setDiameter(event.target.value)}
          onBlur={() => {
            const value = diameter.trim()
            const now = record.diameter_mm ?? null
            if (value === '' && now === null) return
            if (value !== '' && Number(value) === now) return
            void save(value === ''
              ? { clear: ['diameter_mm'] }
              : { diameter_mm: Number(value) })
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter') event.currentTarget.blur()
          }}
        />
      </Field>

      <Field
        label="면적"
        hint={area.trim() === '' && diameterArea !== null
          ? 'cm² · 지금은 지름에서 나옵니다 · 적으면 그것이 이깁니다'
          : 'cm² · 전도도의 분모 · 비우면 지름이나 붙은 셀의 것'}
      >
        {/* 전도도 안내는 "셀이나 스펙트럼에 면적을 적으라" 고 하는데, 정작
            여기에 입력란이 없어 셀 없이 올린 스펙트럼은 그 안내를 따를 수
            없었다 (리뷰 #28). */}
        <input
          aria-label="면적"
          type="number"
          min={0}
          step="any"
          value={area}
          disabled={busy}
          onChange={(event) => setArea(event.target.value)}
          onBlur={() => {
            const value = area.trim()
            if (value === '' && record.area_cm2 === null) return
            if (Number(value) === record.area_cm2) return
            void save(value === ''
              ? { clear: ['area_cm2'] }
              : { area_cm2: Number(value) })
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter') event.currentTarget.blur()
          }}
        />
      </Field>

      <div className="tiny faint">
        {record.kind === 'solid' && record.cell_config !== 'sym'
          ? '전도도는 이온 블로킹 대칭셀에서만 냅니다 — 풀셀의 저주파 아크는 계면입니다.'
          : '전도도는 조회할 때 계산합니다 — 두께·면적을 고치면 바로 따라옵니다.'}
      </div>
    </div>
  )
}
