/** Everything about one cell: state, profile, cycle life, files, spec. */

import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { BasisSelect } from '../components/BasisSelect'
import { CellSpecPanel } from '../components/CellSpecPanel'
import { CompositionEditor } from '../components/CompositionEditor'
import { CyclePicker } from '../components/CyclePicker'
import { CycleTable } from '../components/CycleTable'
import { Plot, PlotLegend, type PlotMarker, type PlotSeries } from '../components/Plot'
import { KneeDetail, ReportCard } from '../components/ReportCard'
import {
  Alert, Card, Empty, Field, KeyValues, Spinner, TableSkeleton,
} from '../components/ui'
import { api } from '../lib/api'
import { basisAxis, bytes, dateTime, num, seriesColor, spread } from '../lib/format'
import { useAsync, useStickyState } from '../lib/hooks'
import { ko } from '../lib/i18n'
import type { Basis, Run, Sample } from '../lib/types'

type LifeMetric = 'discharge' | 'efficiency' | 'retention' | 'hysteresis'

const LIFE_METRICS: { value: LifeMetric; label: string }[] = [
  { value: 'discharge', label: '방전용량' },
  { value: 'retention', label: '유지율' },
  { value: 'efficiency', label: '쿨롱효율' },
  { value: 'hysteresis', label: '전압 이력' },
]

export function SampleDetail() {
  const params = useParams<{ id: string }>()
  const sampleId = Number(params.id)

  const [basis, setBasis] = useStickyState<Basis>('workbench.basis', 'mAh/g')
  const [branches, setBranches] = useState<('charge' | 'discharge')[]>([
    'charge',
    'discharge',
  ])
  const [chosen, setChosen] = useState<number[] | null>(null)
  const [hidden, setHidden] = useState<string[]>([])
  const [lifeMetric, setLifeMetric] = useState<LifeMetric>('discharge')
  const [kneeMethod, setKneeMethod] = useState('segmented')
  const [override, setOverride] = useState<Sample | null>(null)
  const [refDraft, setRefDraft] = useState('')
  const [settingsError, setSettingsError] = useState<string | null>(null)

  const sampleState = useAsync(() => api.getSample(sampleId), [sampleId])
  const sample = override ?? sampleState.data
  const stamp = sample?.updated_at

  const cycleState = useAsync(() => api.sampleCycles(sampleId, { basis }), [sampleId, basis, stamp])
  const reportState = useAsync(() => api.sampleReport(sampleId, { basis }), [sampleId, basis, stamp])
  const runsState = useAsync(() => api.listRuns({ sample_id: sampleId }), [sampleId])

  const cycles = useMemo(() => cycleState.data?.cycles ?? [], [cycleState.data])
  const selected = useMemo(() => {
    if (chosen) return chosen
    const available = cycles.map((c) => c.cycle)
    return available.length ? spread(available, 5) : []
  }, [chosen, cycles])

  const profileState = useAsync(
    () =>
      api.sampleProfile(sampleId, {
        basis,
        cycles: selected.join(','),
        branches: branches.join(','),
      }),
    [sampleId, basis, selected.join(','), branches.join(','), stamp],
    { enabled: selected.length > 0 && branches.length > 0 },
  )

  const profileSeries: PlotSeries[] = useMemo(() => {
    const series = profileState.data?.series ?? []
    const cycleOrder = [...new Set(series.map((s) => s.cycle))]
    return series.map((item) => {
      const label = `${item.cycle}번 ${item.branch === 'charge' ? '충전' : '방전'}`
      return {
        label,
        x: item.capacity,
        y: item.voltage,
        color: seriesColor(cycleOrder.indexOf(item.cycle)),
        dash: item.branch === 'charge' ? [5, 3] : undefined,
        hidden: hidden.includes(label),
      }
    })
  }, [profileState.data, hidden])

  const lifeSeries: PlotSeries[] = useMemo(() => {
    const complete = cycles.filter((c) => c.complete)
    if (!complete.length) return []
    const pick = (cycle: (typeof complete)[number]): number | null => {
      switch (lifeMetric) {
        case 'discharge':
          return cycle.discharge_capacity
        case 'retention':
          return cycle.retention_pct
        case 'efficiency':
          return cycle.coulombic_efficiency
        case 'hysteresis':
          return cycle.voltage_hysteresis
      }
    }
    const points = complete
      .map((cycle) => ({ x: cycle.cycle, y: pick(cycle) }))
      .filter((p): p is { x: number; y: number } => p.y !== null)
    return [
      {
        label: LIFE_METRICS.find((m) => m.value === lifeMetric)!.label,
        x: points.map((p) => p.x),
        y: points.map((p) => p.y),
        color: lifeMetric === 'discharge' ? 'var(--discharge)' : seriesColor(2),
        points: points.length < 120,
        width: 1.8,
      },
    ]
  }, [cycles, lifeMetric])

  // The reference cycle is the denominator of retention, initial CE and the
  // knee search, so it is typed into local state and committed once — a PATCH
  // per keystroke commits every half-typed number ("2" on the way to "25").
  const referenceCycle = sample?.reference_cycle
  useEffect(() => {
    if (referenceCycle !== undefined) setRefDraft(String(referenceCycle))
  }, [referenceCycle])

  const kneeMarkers: PlotMarker[] = useMemo(() => {
    const result = reportState.data?.knee?.results.find((r) => r.method === kneeMethod)
    if (!result?.detected || result.cycle === null) return []
    return [{ x: result.cycle, label: `급감 ${Math.round(result.cycle)}` }]
  }, [reportState.data, kneeMethod])

  if (sampleState.loading && !sample) {
    return (
      <main className="page">
        <Spinner label="셀 정보를 불러오는 중" />
      </main>
    )
  }
  if (sampleState.error || !sample) {
    return (
      <main className="page">
        <Alert kind="error">{sampleState.error ?? '셀을 찾을 수 없습니다.'}</Alert>
        <p>
          <Link to="/samples">셀 라이브러리로</Link>
        </p>
      </main>
    )
  }

  const lifeYLabel =
    lifeMetric === 'discharge'
      ? basisAxis(cycleState.data?.basis ?? basis)
      : lifeMetric === 'hysteresis'
        ? '전압 이력 ΔV (V)'
        : lifeMetric === 'retention'
          ? '용량 유지율 (%)'
          : '쿨롱효율 (%)'

  const conditions = [
    sample.group_name,
    sample.test_date,
    sample.cathode_detail || sample.cathode_type,
    sample.process,
    sample.resolved_cell.composition_compact_label,
    sample.c_rate ? `${sample.c_rate}C` : null,
    sample.temperature_c !== null ? `${sample.temperature_c}°C` : null,
    sample.cutoff_lower_v && sample.cutoff_upper_v
      ? `${sample.cutoff_lower_v}–${sample.cutoff_upper_v} V`
      : null,
  ].filter(Boolean)

  const commitReference = async () => {
    const value = Number(refDraft)
    if (!Number.isFinite(value) || value < 1) {
      setSettingsError('기준 사이클은 1 이상이어야 합니다.')
      setRefDraft(String(sample.reference_cycle))
      return
    }
    if (value === sample.reference_cycle) return
    try {
      setSettingsError(null)
      setOverride(await api.updateSample(sample.id, { reference_cycle: value }))
    } catch (cause) {
      setSettingsError(cause instanceof Error ? cause.message : String(cause))
      setRefDraft(String(sample.reference_cycle))
    }
  }

  // Deleting, reparsing or renumbering a run changes the cycles without
  // touching sample.updated_at, which is what everything else refetches on.
  const runChanged = () => {
    runsState.reload()
    cycleState.reload()
    reportState.reload()
    profileState.reload()
    setChosen(null) // a deleted run's cycles must not stay selected
  }

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1 className="truncate">{sample.name}</h1>
          <div className="sub">{conditions.join('  ·  ') || '조건 미입력'}</div>
        </div>
        <span className="spacer" />
        <div className="row">
          <BasisSelect value={basis} onChange={setBasis} cell={sample.resolved_cell} />
          <a className="link-btn" href={api.exportCyclesUrl(sample.id, { basis })}>
            사이클 CSV
          </a>
          <a
            className="link-btn"
            href={api.exportProfilesUrl(sample.id, {
              basis,
              cycles: selected.join(','),
              branches: branches.join(','),
            })}
          >
            프로파일 CSV
          </a>
          <a
            className="link-btn"
            href={api.exportWorkbookUrl(sample.id, { basis, cycles: selected.join(',') })}
          >
            XLSX
          </a>
        </div>
      </div>

      {cycleState.data?.basis_fallback_reason ? (
        <div style={{ marginBottom: 12 }}>
          <Alert kind="warn">
            {cycleState.data.requested_basis} 로 표시할 수 없어 mAh 로 보여 줍니다 —{' '}
            {ko.basisReason(cycleState.data.basis_fallback_reason)}. 오른쪽 셀 스펙에서 값을
            채우면 바로 바뀝니다.
          </Alert>
        </div>
      ) : null}

      <div className="col" style={{ gap: 12 }}>
        <Card title="셀 상태" tight>
          {reportState.loading && !reportState.data ? (
            <div style={{ padding: 16 }}>
              <Spinner />
            </div>
          ) : reportState.error ? (
            <div style={{ padding: 16 }}>
              <Alert kind="error">{reportState.error}</Alert>
            </div>
          ) : reportState.data ? (
            <ReportCard report={reportState.data} />
          ) : null}
        </Card>

        <div className="split">
          <div className="col" style={{ gap: 12 }}>
            <Card
              title="충방전 프로파일"
              actions={
                <div className="segmented">
                  {(['charge', 'discharge'] as const).map((branch) => (
                    <button
                      key={branch}
                      type="button"
                      className={branches.includes(branch) ? 'on' : ''}
                      onClick={() =>
                        setBranches((current) =>
                          current.includes(branch)
                            ? current.filter((b) => b !== branch)
                            : [...current, branch],
                        )
                      }
                    >
                      {branch === 'charge' ? '충전' : '방전'}
                    </button>
                  ))}
                </div>
              }
              tight
            >
              <div className="toolbar">
                <CyclePicker
                  cycles={cycles}
                  value={selected}
                  onChange={setChosen}
                  basis={cycleState.data?.basis ?? basis}
                />
              </div>
              {profileState.loading && !profileState.data ? (
                <div style={{ padding: 20 }}>
                  <Spinner label="프로파일 계산 중" />
                </div>
              ) : (
                <>
                  {/* useAsync keeps the previous curves on a failure; without
                      this the stale plot is the only thing on screen. */}
                  {profileState.error ? (
                    <div style={{ padding: '12px 16px 0' }}>
                      <Alert kind="error">{profileState.error}</Alert>
                    </div>
                  ) : null}
                  <Plot
                    series={profileSeries}
                    xLabel={basisAxis(profileState.data?.basis ?? basis)}
                    yLabel="전압 (V)"
                    height={400}
                  />
                  <PlotLegend
                    series={profileSeries}
                    onToggle={(label) =>
                      setHidden((current) =>
                        current.includes(label)
                          ? current.filter((l) => l !== label)
                          : [...current, label],
                      )
                    }
                  />
                </>
              )}
            </Card>

            {/* 추세와 knee 판정은 같은 것을 두 방식으로 본다.  판정이 오른쪽
                레일 아래에 있으면, 기준을 바꿔 그래프의 세로선이 어디로
                옮겨졌는지 보려고 스크롤을 오르내리게 된다. */}
            <div className="trend-split">
            <Card
              title="사이클 추세"
              actions={
                <div className="segmented">
                  {LIFE_METRICS.map((metric) => (
                    <button
                      key={metric.value}
                      type="button"
                      className={lifeMetric === metric.value ? 'on' : ''}
                      onClick={() => setLifeMetric(metric.value)}
                    >
                      {metric.label}
                    </button>
                  ))}
                </div>
              }
              tight
            >
              <Plot
                series={lifeSeries}
                xLabel="사이클"
                yLabel={lifeYLabel}
                height={280}
                markers={kneeMarkers}
              />
            </Card>

            {reportState.data?.knee ? (
              <Card title="용량 급감 지점" padSmall>
                <KneeDetail
                  report={reportState.data}
                  selected={kneeMethod}
                  onSelect={setKneeMethod}
                />
              </Card>
            ) : null}
            </div>

            <Card
              title={`사이클 표 · ${cycles.length}개`}
              actions={<span className="tiny faint">행을 누르면 프로파일에 추가·제거됩니다</span>}
              tight
            >
              {cycleState.loading && !cycleState.data ? (
                <TableSkeleton rows={6} columns={9} />
              ) : cycles.length ? (
                <>
                {cycleState.data?.reference_available === false ? (
                  <div style={{ padding: '0 0 10px' }}>
                    <Alert kind="warn">
                      {cycleState.data.retention_note
                        ? ko.cellNote(cycleState.data.retention_note)
                        : `기준 사이클 ${cycleState.data.reference_cycle} 번이 없어 ` +
                          `${cycleState.data.reference_cycle_used} 번을 기준으로 삼았습니다.`}
                    </Alert>
                  </div>
                ) : null}
                <CycleTable
                  cycles={cycles}
                  basis={cycleState.data?.basis ?? basis}
                  selected={selected}
                  // 요청한 값이 아니라 서버가 실제로 기준으로 쓴 사이클.
                  // 3번이 없어 다른 사이클로 대체됐는데 표에는 3번이라고
                  // 적혀 있으면, 유지율이 무엇 대비인지 알 수 없다 (ADR 0004).
                  referenceCycle={
                    cycleState.data?.reference_cycle_used ??
                    cycleState.data?.reference_cycle ??
                    null
                  }
                  onSelect={(cycle) =>
                    setChosen(
                      selected.includes(cycle)
                        ? selected.filter((c) => c !== cycle)
                        : [...selected, cycle].sort((a, b) => a - b),
                    )
                  }
                />
                </>
              ) : (
                <Empty title="사이클이 없습니다" icon="＋">
                  이 셀에 <Link to="/upload">.wrd 파일을 올려</Link> 주세요.
                </Empty>
              )}
            </Card>
          </div>

          <div className="rail">
            <Card title="전극 조성" padSmall>
              <CompositionEditor
                sample={sample}
                onSaved={(updated) => {
                  setOverride(updated)
                  sampleState.reload()
                }}
              />
            </Card>

            <Card title="질량 · 면적" padSmall>
              <CellSpecPanel
                sample={sample}
                onSaved={(updated) => {
                  setOverride(updated)
                  sampleState.reload()
                }}
              />
            </Card>

            <Card title="분석 설정" padSmall>
              <div className="col" style={{ gap: 9 }}>
                {settingsError ? <Alert kind="error">{settingsError}</Alert> : null}
                <Field label="기준 사이클" hint="유지율·초기 CE·knee 탐색 기준 · Enter 로 적용">
                  <input
                    type="number"
                    min={1}
                    value={refDraft}
                    onChange={(event) => setRefDraft(event.target.value)}
                    onBlur={() => void commitReference()}
                    onKeyDown={(event) => {
                      if (event.key === 'Enter') event.currentTarget.blur()
                    }}
                  />
                </Field>
                <Field label="상태 판정" hint="자동은 파일 근거로 판정">
                  <select
                    value={sample.declared_state}
                    onChange={async (event) => {
                      try {
                        setSettingsError(null)
                        setOverride(
                          await api.updateSample(sample.id, {
                            declared_state: event.target.value,
                          }),
                        )
                      } catch (cause) {
                        setSettingsError(cause instanceof Error ? cause.message : String(cause))
                      }
                    }}
                  >
                    <option value="auto">자동</option>
                    <option value="running">구동 중으로 고정</option>
                    <option value="finished">종료로 고정</option>
                  </select>
                </Field>
              </div>
            </Card>

            <Card
              title={`파일 · ${runsState.error ? '—' : `${runsState.data?.length ?? 0}개`}`}
              padSmall
            >
              {runsState.error ? (
                <Alert kind="error">{runsState.error}</Alert>
              ) : runsState.loading && !runsState.data ? (
                <Spinner />
              ) : runsState.data?.length ? (
                <div className="col" style={{ gap: 10 }}>
                  {runsState.data.map((run) => (
                    <RunRow key={run.id} run={run} onChanged={runChanged} />
                  ))}
                </div>
              ) : (
                <Empty title="연결된 파일이 없습니다" icon="↑">
                  <Link to="/upload">업로드</Link>
                </Empty>
              )}
            </Card>
          </div>
        </div>
      </div>
    </main>
  )
}

function RunRow({ run, onChanged }: { run: Run; onChanged: () => void }) {
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const steps = run.schedule?.steps ?? []
  const schedule = run.schedule ?? {}

  return (
    <div className="col" style={{ gap: 5 }}>
      <div className="row" style={{ justifyContent: 'space-between', gap: 8 }}>
        <strong className="truncate small" title={run.original_name}>
          {run.original_name}
        </strong>
        <span className="tiny faint nowrap">{bytes(run.size_bytes)}</span>
      </div>

      <KeyValues
        rows={[
          ['장비', `${run.device_model} ch${run.channel ?? '—'}`],
          ['기간', `${dateTime(run.start_time)} → ${dateTime(run.end_time)}`],
          ['샘플', run.row_count.toLocaleString()],
          [
            '사이클',
            `${run.complete_cycle_count}/${run.cycle_count}${
              run.cycle_offset ? ` · offset ${run.cycle_offset}` : ''
            }${run.cycle_offset_source === 'manual' ? ' (수동)' : ''}`,
          ],
          ...(schedule.upper_cutoff_v
            ? ([
                ['컷오프', `${schedule.lower_cutoff_v}–${schedule.upper_cutoff_v} V`],
                [
                  '프로토콜',
                  [
                    schedule.c_rate ? `${schedule.c_rate}C` : null,
                    schedule.planned_cycles ? `${schedule.planned_cycles} 사이클` : null,
                    schedule.nominal_capacity_mah
                      ? `공칭 ${num(schedule.nominal_capacity_mah)} mAh`
                      : null,
                  ]
                    .filter(Boolean)
                    .join(' · '),
                ],
              ] as [string, string][])
            : []),
        ]}
      />

      {steps.length ? (
        <details>
          <summary>스케줄 {steps.length} 스텝</summary>
          <div className="step-list" style={{ marginTop: 4 }}>
            {steps.map((step) => (
              <div key={step.index}>
                <span className="n">{step.index}</span>
                <span className={step.direction}>{step.text}</span>
              </div>
            ))}
          </div>
        </details>
      ) : null}

      <div className="row" style={{ gap: 4 }}>
        <a className="tiny" href={api.exportRawUrl(run.id)}>
          raw CSV
        </a>
        <span className="spacer" />
        <button
          type="button"
          className="ghost sm"
          disabled={busy}
          title="원본에서 다시 읽습니다"
          onClick={async () => {
            setBusy(true)
            try {
              setError(null)
              await api.reparseRun(run.id)
              onChanged()
            } catch (cause) {
              setError(cause instanceof Error ? cause.message : String(cause))
            } finally {
              setBusy(false)
            }
          }}
        >
          재파싱
        </button>
        <button
          type="button"
          className="danger sm"
          disabled={busy}
          onClick={async () => {
            if (!window.confirm(`${run.original_name} 을(를) 목록에서 지울까요?`)) return
            setBusy(true)
            try {
              setError(null)
              await api.deleteRun(run.id)
              onChanged()
            } catch (cause) {
              setError(cause instanceof Error ? cause.message : String(cause))
            } finally {
              setBusy(false)
            }
          }}
        >
          삭제
        </button>
      </div>
      {error ? <Alert kind="error">{error}</Alert> : null}
      <div className="sep" style={{ margin: '2px 0' }} />
    </div>
  )
}
