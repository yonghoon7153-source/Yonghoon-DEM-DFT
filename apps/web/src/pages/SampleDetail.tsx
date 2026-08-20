/** Everything about one cell: state, profile, cycle life, files, spec. */

import { useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { BasisSelect } from '../components/BasisSelect'
import { CellSpecPanel } from '../components/CellSpecPanel'
import { CyclePicker } from '../components/CyclePicker'
import { CycleTable } from '../components/CycleTable'
import { Plot, PlotLegend, type PlotMarker, type PlotSeries } from '../components/Plot'
import { KneeDetail, ReportCard } from '../components/ReportCard'
import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { basisAxis, bytes, dateTime, num, seriesColor, spread } from '../lib/format'
import { useAsync, useStickyState } from '../lib/hooks'
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

  const sampleState = useAsync(() => api.getSample(sampleId), [sampleId])
  const sample = override ?? sampleState.data

  const cycleState = useAsync(
    () => api.sampleCycles(sampleId, { basis }),
    [sampleId, basis, sample?.updated_at],
  )
  const reportState = useAsync(
    () => api.sampleReport(sampleId, { basis }),
    [sampleId, basis, sample?.updated_at],
  )
  const runsState = useAsync(() => api.listRuns({ sample_id: sampleId }), [sampleId])

  // Memoised so the derived selections below do not re-run on every render.
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
    [sampleId, basis, selected.join(','), branches.join(','), sample?.updated_at],
    { enabled: selected.length > 0 && branches.length > 0 },
  )

  const profileSeries: PlotSeries[] = useMemo(() => {
    const series = profileState.data?.series ?? []
    const cycleOrder = [...new Set(series.map((s) => s.cycle))]
    return series.map((item) => {
      const colorIndex = cycleOrder.indexOf(item.cycle)
      return {
        label: `${item.cycle}번 ${item.branch === 'charge' ? '충전' : '방전'}`,
        x: item.capacity,
        y: item.voltage,
        color: seriesColor(colorIndex),
        dash: item.branch === 'charge' ? [5, 3] : undefined,
        hidden: hidden.includes(
          `${item.cycle}번 ${item.branch === 'charge' ? '충전' : '방전'}`,
        ),
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
        color: seriesColor(0),
        points: points.length < 120,
      },
    ]
  }, [cycles, lifeMetric])

  const kneeMarkers: PlotMarker[] = useMemo(() => {
    const result = reportState.data?.knee?.results.find((r) => r.method === kneeMethod)
    if (!result?.detected || result.cycle === null) return []
    return [{ x: result.cycle, label: `knee ${Math.round(result.cycle)}` }]
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
        <Link to="/samples">셀 라이브러리로</Link>
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

  return (
    <main className="page">
      <div className="page-head">
        <div>
          <h1>{sample.name}</h1>
          <div className="sub">
            {[
              sample.group_name,
              sample.test_date,
              sample.cathode_detail || sample.cathode_type,
              sample.process,
              sample.c_rate ? `${sample.c_rate}C` : null,
              sample.temperature_c !== null ? `${sample.temperature_c}°C` : null,
              sample.cutoff_lower_v && sample.cutoff_upper_v
                ? `${sample.cutoff_lower_v}–${sample.cutoff_upper_v} V`
                : null,
            ]
              .filter(Boolean)
              .join(' · ') || '조건 미입력'}
          </div>
        </div>
        <span className="spacer" />
        <div className="row">
          <BasisSelect value={basis} onChange={setBasis} cell={sample.resolved_cell} />
          <a
            className="badge plain"
            style={{ padding: '6px 12px' }}
            href={api.exportCyclesUrl(sample.id, { basis })}
          >
            사이클 CSV
          </a>
          <a
            className="badge plain"
            style={{ padding: '6px 12px' }}
            href={api.exportProfilesUrl(sample.id, {
              basis,
              cycles: selected.join(','),
              branches: branches.join(','),
            })}
          >
            프로파일 CSV
          </a>
          <a
            className="badge plain"
            style={{ padding: '6px 12px' }}
            href={api.exportWorkbookUrl(sample.id, { basis, cycles: selected.join(',') })}
          >
            XLSX
          </a>
        </div>
      </div>

      {cycleState.data?.basis_fallback_reason ? (
        <Alert kind="warn">
          {cycleState.data.requested_basis} 로 표시할 수 없어 mAh 로 보여 줍니다 —{' '}
          {cycleState.data.basis_fallback_reason}. 오른쪽 셀 스펙에서 값을 채우면 바로
          바뀝니다.
        </Alert>
      ) : null}

      <div className="col" style={{ gap: 14 }}>
        <Card title="셀 상태">
          {reportState.loading && !reportState.data ? (
            <Spinner />
          ) : reportState.error ? (
            <Alert kind="error">{reportState.error}</Alert>
          ) : reportState.data ? (
            <ReportCard report={reportState.data} />
          ) : null}
        </Card>

        <div className="split">
          <div className="col" style={{ gap: 14 }}>
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
              <div style={{ padding: '12px 14px 0' }}>
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
                  <Plot
                    series={profileSeries}
                    xLabel={basisAxis(profileState.data?.basis ?? basis)}
                    yLabel="전압 (V)"
                    height={380}
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
                height={300}
                markers={kneeMarkers}
              />
            </Card>

            <Card
              title={`사이클 표 · ${cycles.length}개`}
              actions={<span className="tiny faint">행을 누르면 프로파일에 추가됩니다</span>}
              tight
            >
              {cycles.length ? (
                <CycleTable
                  cycles={cycles}
                  basis={cycleState.data?.basis ?? basis}
                  selected={selected}
                  referenceCycle={cycleState.data?.reference_cycle ?? null}
                  onSelect={(cycle) =>
                    setChosen(
                      selected.includes(cycle)
                        ? selected.filter((c) => c !== cycle)
                        : [...selected, cycle].sort((a, b) => a - b),
                    )
                  }
                />
              ) : (
                <Empty title="사이클이 없습니다">
                  이 셀에 <Link to="/upload">.wrd 파일을 올려</Link> 주세요.
                </Empty>
              )}
            </Card>
          </div>

          <div className="col" style={{ gap: 14 }}>
            <Card title="셀 스펙">
              <CellSpecPanel
                sample={sample}
                onSaved={(updated) => {
                  setOverride(updated)
                  sampleState.reload()
                }}
              />
            </Card>

            <Card title="분석 설정">
              <div className="col" style={{ gap: 10 }}>
                <Field label="기준 사이클" hint="유지율·초기 CE 기준">
                  <input
                    type="number"
                    min={1}
                    value={sample.reference_cycle}
                    onChange={async (event) => {
                      const value = Number(event.target.value)
                      if (value >= 1) {
                        setOverride(
                          await api.updateSample(sample.id, { reference_cycle: value }),
                        )
                      }
                    }}
                  />
                </Field>
                <Field label="상태 판정" hint="auto 는 파일 근거로 자동 판정">
                  <select
                    value={sample.declared_state}
                    onChange={async (event) =>
                      setOverride(
                        await api.updateSample(sample.id, {
                          declared_state: event.target.value,
                        }),
                      )
                    }
                  >
                    <option value="auto">자동</option>
                    <option value="running">구동 중으로 고정</option>
                    <option value="finished">종료로 고정</option>
                  </select>
                </Field>
              </div>
            </Card>

            {reportState.data?.knee ? (
              <Card title="용량 급감 지점">
                <KneeDetail
                  report={reportState.data}
                  selected={kneeMethod}
                  onSelect={setKneeMethod}
                />
              </Card>
            ) : null}

            <Card title={`파일 · ${runsState.data?.length ?? 0}개`} tight>
              <div style={{ padding: 12 }}>
                {runsState.data?.length ? (
                  <div className="col" style={{ gap: 10 }}>
                    {runsState.data.map((run) => (
                      <RunRow key={run.id} run={run} onChanged={() => runsState.reload()} />
                    ))}
                  </div>
                ) : (
                  <Empty title="연결된 파일이 없습니다">
                    <Link to="/upload">업로드</Link>
                  </Empty>
                )}
              </div>
            </Card>
          </div>
        </div>
      </div>
    </main>
  )
}

function RunRow({ run, onChanged }: { run: Run; onChanged: () => void }) {
  const [busy, setBusy] = useState(false)
  const steps = run.schedule?.steps ?? []

  return (
    <div className="col" style={{ gap: 4, fontSize: 12 }}>
      <div className="row" style={{ justifyContent: 'space-between' }}>
        <strong className="nowrap" title={run.original_name}>
          {run.original_name}
        </strong>
        <span className="faint tiny">{bytes(run.size_bytes)}</span>
      </div>
      <div className="dim tiny">
        {run.device_model} ch{run.channel} · {dateTime(run.start_time)} →{' '}
        {dateTime(run.end_time)}
      </div>
      <div className="dim tiny mono">
        {run.row_count.toLocaleString()} 샘플 · {run.complete_cycle_count}/
        {run.cycle_count} 사이클 · offset {run.cycle_offset}
        {run.cycle_offset_source === 'manual' ? ' (수동)' : ''}
      </div>
      {run.schedule?.upper_cutoff_v ? (
        <div className="dim tiny">
          {run.schedule.lower_cutoff_v}–{run.schedule.upper_cutoff_v} V
          {run.schedule.c_rate ? ` · ${run.schedule.c_rate}C` : ''}
          {run.schedule.planned_cycles ? ` · 계획 ${run.schedule.planned_cycles} 사이클` : ''}
          {run.schedule.nominal_capacity_mah
            ? ` · 공칭 ${num(run.schedule.nominal_capacity_mah)} mAh`
            : ''}
        </div>
      ) : null}
      {steps.length ? (
        <details>
          <summary className="tiny dim" style={{ cursor: 'pointer' }}>
            스케줄 {steps.length} 스텝
          </summary>
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
      <div className="row">
        <a className="tiny" href={api.exportRawUrl(run.id)}>
          raw CSV
        </a>
        <button
          type="button"
          className="ghost sm tiny"
          disabled={busy}
          onClick={async () => {
            setBusy(true)
            try {
              await api.reparseRun(run.id)
              onChanged()
            } finally {
              setBusy(false)
            }
          }}
        >
          재파싱
        </button>
        <button
          type="button"
          className="ghost sm tiny"
          disabled={busy}
          onClick={async () => {
            if (!window.confirm(`${run.original_name} 을(를) 목록에서 지울까요?`)) return
            setBusy(true)
            try {
              await api.deleteRun(run.id)
              onChanged()
            } finally {
              setBusy(false)
            }
          }}
        >
          삭제
        </button>
      </div>
      <div className="sep" />
    </div>
  )
}
