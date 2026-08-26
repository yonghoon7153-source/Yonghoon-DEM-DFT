/** Everything about one cell: state, profile, cycle life, files, spec. */

import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { AxisLockControl, useAxisLock } from '../components/AxisLock'
import { BasisSelect } from '../components/BasisSelect'
import { CellSpecPanel } from '../components/CellSpecPanel'
import { CellSpectra } from '../components/CellSpectra'
import { EditableName } from '../components/EditableName'
import { OtherMeasurements } from '../components/OtherMeasurements'
import { CompositionEditor } from '../components/CompositionEditor'
import { CyclePicker } from '../components/CyclePicker'
import { TestConditionsPanel } from '../components/TestConditionsPanel'
import { CycleTable } from '../components/CycleTable'
import { Plot, PlotLegend, type PlotMarker, type PlotSeries } from '../components/Plot'
import { KneeDetail, ReportCard } from '../components/ReportCard'
import { Alert, Card, Empty, Field, KeyValues, Spinner, TableSkeleton } from '../components/ui'
import { By } from '../components/WhoAmI'
import { api } from '../lib/api'
import { copyText, cycleAndEfficiencyTsv, dischargeTsv, dqdvTsv, dvdqTsv, efficiencyTsv, onlyCycles, profileTsv, skippedForCopy } from '../lib/origin'
import { basisAxis, basisUnit, bytes, dateTime, num, seriesColor, spread } from '../lib/format'
import { useAsync, useStickyState } from '../lib/hooks'
import { ko } from '../lib/i18n'
import type { Basis, Run, Sample, Smoother } from '../lib/types'

type LifeMetric = 'discharge' | 'efficiency' | 'retention' | 'hysteresis'

/** 한 그래프에 겹칠 수 없는 세 가지 축.
 *
 *  프로파일  가로 용량 · 세로 볼트
 *  dQ/dV     가로 볼트 · 세로 용량/볼트   ← 평탄부가 봉우리가 된다
 *  dV/dQ     가로 용량 · 세로 볼트/용량   ← 봉우리 *사이 간격* 이 용량이다
 *
 *  사이클 선택과 충전·방전 토글, 평활 설정은 셋이 공유한다 — 같은 것을 세
 *  방식으로 보는 것이기 때문이다. */
type CurveMode = 'profile' | 'dqdv' | 'dvdq'

/** 격자 간격을 칸에 넣을 만큼만.  mAh 와 mAh/g 는 자릿수가 서너 자리 다르다. */
function formatStep(step: number | undefined): string {
  if (step === undefined || !Number.isFinite(step)) return '—'
  if (step >= 1) return step.toFixed(2)
  if (step >= 0.01) return step.toFixed(4)
  return step.toExponential(1)
}

const CURVE_TITLES: Record<CurveMode, string> = {
  profile: '충방전 프로파일',
  dqdv: 'dQ/dV',
  dvdq: 'dV/dQ',
}

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
  const [branches, setBranches] = useState<('charge' | 'discharge')[]>(['charge', 'discharge'])
  // 프로파일과 dQ/dV 는 축이 다르다 (가로 용량 vs 볼트, 세로 볼트 vs mAh/V).
  // 한 그래프에 겹칠 수 없으므로 모드로 갈라 놓고, 사이클 선택과 충전·방전
  // 토글은 둘이 공유한다 — 같은 것을 두 방식으로 보는 것이기 때문이다.
  const [mode, setMode] = useStickyState<CurveMode>('workbench.curveMode', 'profile')
  // 평활은 세 곡선이 함께 쓴다.  dQ/dV 와 dV/dQ 를 오갈 때 설정이 따라와야
  // 두 그림이 같은 처리로 만들어졌다고 말할 수 있다 (ADR 0015).
  const [smoother, setSmoother] = useStickyState<Smoother>(
    'workbench.smoother', 'moving')
  const [smoothing, setSmoothing] = useStickyState<number>('workbench.smoothing', 5)
  const [polyOrder, setPolyOrder] = useStickyState<number>('workbench.polyOrder', 2)
  const [chosen, setChosen] = useState<number[] | null>(null)
  const [hidden, setHidden] = useState<string[]>([])
  const [lifeMetric, setLifeMetric] = useState<LifeMetric>('discharge')
  // 사용자가 고르기 전에는 **primary** 를 따른다.  'dbw' 로 못박아 두면
  // dbw 가 사퇴하고 segmented 가 답인 셀에서 카드에는 knee 가 있는데 그래프에
  // 세로선이 없다 (Codex #9).
  const [kneeMethod, setKneeMethod] = useState<string | null>(null)
  const [override, setOverride] = useState<Sample | null>(null)
  const [refDraft, setRefDraft] = useState('')
  // 스치기만 한 blur 가 PATCH 를 보내지 않도록, 손으로 고친 뒤에만 커밋한다.
  // 자동으로 1번에 앵커된 셀은 blur 만으로 reference_cycle=1 이 저장되며
  // 출처가 user 로 바뀌어 -- 나중에 formation 파일이 붙어도 1 에 영원히
  // 고정된다.  고치지 않았으면 보낼 것도 없다.
  const [refDirty, setRefDirty] = useState(false)
  const [settingsError, setSettingsError] = useState<string | null>(null)

  const sampleState = useAsync(() => api.getSample(sampleId), [sampleId], { live: true })
  // `override` is what a save on this page just returned, shown immediately so
  // the panel does not flicker back to the old value while the re-fetch flies.
  // Whichever is newer wins: without that comparison the override, once set,
  // shadowed the server forever -- and on a shared instance that means the
  // moment you edit a cell you stop seeing anybody else's edits to it.
  const sample = useMemo(() => {
    const fetched = sampleState.data
    if (!override) return fetched
    if (!fetched) return override
    return fetched.updated_at >= override.updated_at ? fetched : override
  }, [override, sampleState.data])
  const stamp = sample?.updated_at

  // 이 셋도 살아 있어야 한다.  남이 이 셀에 파일을 하나 더 붙이면 사이클 표와
  // 판정이 달라지는데, 그때 sample.updated_at 은 움직이지 않는다 — 바뀐 것은
  // 셀이 아니라 run 이다.
  const cycleState = useAsync(
    () => api.sampleCycles(sampleId, { basis }),
    [sampleId, basis, stamp],
    { live: true },
  )
  const reportState = useAsync(
    () => api.sampleReport(sampleId, { basis }),
    [sampleId, basis, stamp],
    { live: true },
  )
  const runsState = useAsync(() => api.listRuns({ sample_id: sampleId }), [sampleId],
                             { live: true })

  const cycles = useMemo(() => cycleState.data?.cycles ?? [], [cycleState.data])
  //: 표에 없는 사이클들 — 잘렸거나 한쪽 브랜치가 없어서 지표를 못 내는 것들.
  //  곡선은 실측이므로 그릴 수는 있다.  기본은 끔: 완료 사이클들 사이에 잘린
  //  곡선이 아무 표시 없이 끼면 셀이 갑자기 용량을 잃은 것처럼 보인다.
  const partialCycles = useMemo(
    () => cycleState.data?.partial_cycles ?? [],
    [cycleState.data],
  )
  const [includePartial, setIncludePartial] = useState(false)
  const selected = useMemo(() => {
    if (chosen) return chosen
    const available = cycles.map((c) => c.cycle)
    return available.length ? spread(available, 5) : []
  }, [chosen, cycles])

  // 사이클 관련 복사가 **전체**인가 **고른 것**인가.  기본은 전체 — 지금까지의
  // 동작이고, 표에 보이는 것이 전체이므로 놀랄 일이 없다.
  //
  // 나눈 이유: 3·4 번만 보려고 골라 놓고 복사하면 200 사이클이 통째로 나왔다.
  // 곡선(프로파일·dQ/dV)은 이미 고른 것만 나가는데 사이클 표만 전체였다 --
  // 같은 화면에서 두 규칙이 다른 것이 그 자체로 함정이다.
  const [cycleScope, setCycleScope] = useState<'all' | 'picked'>('all')
  const copyCycles = useMemo(
    () => onlyCycles(cycles, cycleScope === 'all' ? null : selected),
    [cycleScope, cycles, selected],
  )
  const scopeNote = cycleScope === 'all'
    ? `전체 ${cycles.length}개`
    : `고른 ${copyCycles.length}개`

  const smoothingParams = {
    smoother,
    smoothing,
    ...(smoother === 'savgol' ? { poly_order: polyOrder } : {}),
  }
  const smoothingKey = `${smoother}|${smoothing}|${polyOrder}`

  const dqdvState = useAsync(
    () =>
      api.sampleDqdv(sampleId, {
        basis,
        cycles: selected.join(','),
        branches: branches.join(','),
        ...smoothingParams,
      }),
    [sampleId, basis, selected.join(','), branches.join(','), smoothingKey, stamp],
    // 모드를 켰을 때만 받아 온다.  20 MB 파일에서 400 사이클의 미분을 아무도
    // 보지 않는 동안 계산할 이유가 없다.
    { enabled: mode === 'dqdv' && selected.length > 0 && branches.length > 0 },
  )

  const dvdqState = useAsync(
    () =>
      api.sampleDvdq(sampleId, {
        basis,
        cycles: selected.join(','),
        branches: branches.join(','),
        ...smoothingParams,
      }),
    [sampleId, basis, selected.join(','), branches.join(','), smoothingKey, stamp],
    { enabled: mode === 'dvdq' && selected.length > 0 && branches.length > 0 },
  )

  const profileState = useAsync(
    () =>
      api.sampleProfile(sampleId, {
        basis,
        cycles: selected.join(','),
        branches: branches.join(','),
        include_partial: includePartial,
      }),
    [sampleId, basis, selected.join(','), branches.join(','), includePartial, stamp],
    { enabled: selected.length > 0 && branches.length > 0 },
  )

  const profileSeries: PlotSeries[] = useMemo(() => {
    // Nothing selected means nothing drawn.  `useAsync` deliberately keeps the
    // last response while a new one loads -- that is what stops the panel
    // blanking on every keystroke -- but it also means a disabled request
    // leaves the old curves on screen, so 초기화 cleared the selection and the
    // plot went on showing eight cycles.
    if (!selected.length) return []
    const series = profileState.data?.series ?? []
    const cycleOrder = [...new Set(series.map((s) => s.cycle))]
    return series.map((item) => {
      // 완료 사이클인 척하면 안 된다.  이름에 표시하고, 점선으로 그린다 --
      // 잘린 방전 곡선이 실선으로 옆에 서면 용량이 떨어진 것으로 읽힌다.
      const partial = item.complete === false
      const label =
        `${item.cycle}번 ${item.branch === 'charge' ? '충전' : '방전'}` +
        (partial ? ` (${ko.partialReason(item.incomplete_reason ?? '')})` : '')
      return {
        label,
        x: item.capacity,
        y: item.voltage,
        color: seriesColor(cycleOrder.indexOf(item.cycle)),
        dash: item.branch === 'charge' ? [5, 3] : undefined,
        // 파선은 이미 충전/방전을 가르는 데 쓰고 있으므로, 숫자 없는 곡선은
        // 가늘게 그린다.  이름표에 이유가 붙어 있어 둘이 겹치지 않는다.
        width: partial ? 1.0 : undefined,
        partial,
        hidden: hidden.includes(label),
      }
    })
  }, [profileState.data, hidden, selected.length])

  const dqdvSeries: PlotSeries[] = useMemo(() => {
    if (!selected.length) return []
    // 만들지 못한 곡선은 그릴 것이 없으므로 뺀다.  왜 없는지는 그래프 아래
    // 한 줄로 따로 말해 준다 — 범례에 빈 항목이 서 있는 것보다 낫다.
    const series = (dqdvState.data?.series ?? []).filter((item) => item.points > 0)
    const cycleOrder = [...new Set(series.map((s) => s.cycle))]
    return series.map((item) => {
      const label = `${item.cycle}번 ${item.branch === 'charge' ? '충전' : '방전'}`
      return {
        label,
        x: item.voltage,
        y: item.dqdv,
        color: seriesColor(cycleOrder.indexOf(item.cycle)),
        dash: item.branch === 'charge' ? [5, 3] : undefined,
        hidden: hidden.includes(label),
      }
    })
  }, [dqdvState.data, hidden, selected.length])

  const dvdqSeries: PlotSeries[] = useMemo(() => {
    if (!selected.length) return []
    const series = (dvdqState.data?.series ?? []).filter((item) => item.points > 0)
    const cycleOrder = [...new Set(series.map((s) => s.cycle))]
    return series.map((item) => {
      const label = `${item.cycle}번 ${item.branch === 'charge' ? '충전' : '방전'}`
      return {
        label,
        x: item.capacity,
        y: item.dvdq,
        color: seriesColor(cycleOrder.indexOf(item.cycle)),
        dash: item.branch === 'charge' ? [5, 3] : undefined,
        hidden: hidden.includes(label),
      }
    })
  }, [dvdqState.data, hidden, selected.length])

  /** 지금 모드가 보고 있는 요청.  로딩과 오류를 세 번 쓰지 않는다. */
  const curve = mode === 'dqdv' ? dqdvState : mode === 'dvdq' ? dvdqState : profileState
  const shownSeries =
    mode === 'dqdv' ? dqdvSeries : mode === 'dvdq' ? dvdqSeries : profileSeries

  /** 만들지 못한 곡선들이 왜 없는지 — 한 줄로. */
  const skipped = useMemo(() => {
    const source = mode === 'dqdv' ? dqdvState.data : mode === 'dvdq' ? dvdqState.data : null
    const bad = (source?.series ?? []).filter((item) => !item.points)
    if (!bad.length) return ''
    const reasons = [...new Set(bad.map((item) => item.reason).filter(Boolean))]
    return `${bad.length}개 곡선을 만들지 못했습니다 — ${reasons.join(' · ')}`
  }, [mode, dqdvState.data, dvdqState.data])

  // 축을 이 셀이 낸 가장 큰 용량에 고정한다.  안 그러면 사이클을 하나 넣고
  // 뺄 때마다 x 축이 늘었다 줄었다 해서, 같은 곡선이 매번 다른 폭으로 보인다.
  const capacityAxis = useMemo((): [number | null, number | null] | undefined => {
    let widest = 0
    for (const cycle of cycles) {
      if (!cycle.complete) continue
      widest = Math.max(widest, cycle.discharge_capacity ?? 0, cycle.charge_capacity ?? 0)
    }
    // 여유 3 % — 곡선 끝이 축에 딱 붙으면 잘린 것처럼 보인다.
    return widest > 0 ? [0, widest * 1.03] : undefined
  }, [cycles])

  // dQ/dV 의 x 축(전압)도 같은 이유로 셀 전체 창에 고정한다.  사이클 표가 이미
  // 사이클마다 v_min/v_max 를 들고 있으므로 공짜다 — dQ/dV 를 다시 계산할
  // 필요가 없다.
  const voltageAxis = useMemo((): [number | null, number | null] | undefined => {
    let low = Number.POSITIVE_INFINITY
    let high = Number.NEGATIVE_INFINITY
    for (const cycle of cycles) {
      if (!cycle.complete) continue
      if (cycle.voltage_min !== null) low = Math.min(low, cycle.voltage_min)
      if (cycle.voltage_max !== null) high = Math.max(high, cycle.voltage_max)
    }
    if (!Number.isFinite(low) || !Number.isFinite(high) || high <= low) return undefined
    const pad = (high - low) * 0.02
    return [low - pad, high + pad]
  }, [cycles])

  // 세로축은 공짜가 아니다.  전체 사이클의 dQ/dV 범위를 알려면 안 그릴 곡선까지
  // 전부 미분해야 하므로, 사람이 지금 눈금을 잠그는 쪽을 택했다.  단위가 바뀌면
  // (기준 변경·모드 전환·평활 변경) 잠근 숫자는 다른 축의 것이라 자동으로 풀린다.
  const yLock = useAxisLock(shownSeries, 'y', `${mode}|${basis}|${smoothingKey}`)
  const xLock = useAxisLock(shownSeries, 'x', `${mode}|${basis}`)

  /** 잠근 값이 있으면 그것, 없으면 그 모드의 기본 고정축. */
  const xRange = xLock.range ?? (
    mode === 'dqdv' ? voltageAxis
    : mode === 'dvdq' ? capacityAxis
    : capacityAxis)

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
  //
  // 입력란은 **실제로 쓰이는** 값을 보여 준다.  formation 이 없는 스케줄은
  // 1번에 앵커하는데(ADR 0018) 칸에 저장값 3 이 남아 있으면, 표의 유지율이
  // 1번 기준인데 칸은 3 이라고 말하는 화면이 된다.
  const referenceCycle = sample?.reference_cycle_effective ?? sample?.reference_cycle
  const referenceReason = sample?.reference_cycle_reason ?? 'default'
  useEffect(() => {
    if (referenceCycle !== undefined) {
      setRefDraft(String(referenceCycle))
      setRefDirty(false)
    }
  }, [referenceCycle])

  // Origin 에 바로 붙여 넣을 블록.  누른 순간 화면에 있는 것을 그대로 복사한다
  // — 그래서 붙여 넣은 그림이 여기 그림과 같다.  전체 점이 필요하면 옆의
  // CSV/XLSX 가 있다.  훅이므로 아래 이른 return 들보다 위에 있어야 한다.
  const [copied, setCopied] = useState<string | null>(null)
  const [copyError, setCopyError] = useState<string | null>(null)

  const kneeMarkers: PlotMarker[] = useMemo(() => {
    const chosen = kneeMethod ?? reportState.data?.knee?.primary.method
    const result = reportState.data?.knee?.results.find((r) => r.method === chosen)
    if (!result) return []
    if (result.detected && result.cycle !== null) {
      // DBW 는 한 사건의 앞끝과 뒷끝을 함께 준다 (ADR 0021): 이탈이 시작되는
      // onset 은 흐린 선, 급감이 자리 잡는 point 는 진한 선.
      if (result.onset_cycle != null) {
        return [
          { x: result.onset_cycle, label: `이탈 ${Math.round(result.onset_cycle)}`, tentative: true },
          { x: result.cycle, label: `급감 ${Math.round(result.cycle)}` },
        ]
      }
      return [{ x: result.cycle, label: `급감 ${Math.round(result.cycle)}` }]
    }
    // 확정이 아니어도 짚은 곳은 그린다 — 흐리게, 물음표를 달아서.  아무것도 안
    // 그리면 "안 꺾였다" 와 "아직 확인할 데이터가 없다" 가 같은 그림이 된다.
    if (result.status === 'insufficient' && result.candidate_cycle !== null) {
      return [
        {
          x: result.candidate_cycle,
          label: `급감? ${Math.round(result.candidate_cycle)}`,
          tentative: true,
        },
      ]
    }
    return []
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
    if (!refDirty) return
    const value = Number(refDraft)
    if (!Number.isFinite(value) || value < 1) {
      setSettingsError('기준 사이클은 1 이상이어야 합니다.')
      setRefDraft(String(referenceCycle ?? sample.reference_cycle))
      setRefDirty(false)
      return
    }
    // 쓰이는 값과 비교한다.  저장값과 비교하면, 자동으로 1번이 된 셀에 1 을
    // 쳐도 "같다" 며 아무 일도 안 하고 -- 사람이 고정하려던 의도가 사라진다.
    if (value === referenceCycle && referenceReason === 'user') return
    try {
      setSettingsError(null)
      setOverride(await api.updateSample(sample.id, { reference_cycle: value }))
      setRefDirty(false)
    } catch (cause) {
      setSettingsError(cause instanceof Error ? cause.message : String(cause))
      setRefDraft(String(referenceCycle ?? sample.reference_cycle))
      setRefDirty(false)
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

  async function copyBlock(what: string, text: string, skipped = 0) {
    setCopyError(null)
    if (!text) {
      setCopyError(
        skipped
          ? `복사할 ${what} 데이터가 없습니다 — 고른 곡선 ${skipped}개가 모두 아직 끝나지 않았습니다`
          : `복사할 ${what} 데이터가 없습니다`,
      )
      return
    }
    try {
      await copyText(text)
      setCopied(what)
      // 조용히 빼면 붙여 넣은 사람이 곡선 수가 다른 것을 못 본다.
      if (skipped) {
        setCopyError(`아직 끝나지 않은 곡선 ${skipped}개는 뺐습니다 — 그 마지막 값은 사이클 용량이 아닙니다`)
      }
      window.setTimeout(() => setCopied((current) => (current === what ? null : current)), 1800)
    } catch (cause) {
      setCopyError(cause instanceof Error ? cause.message : String(cause))
    }
  }

  const analysisSettings = (
    <Card title="분석 설정" padSmall>
      <div className="col" style={{ gap: 9 }}>
        {settingsError ? <Alert kind="error">{settingsError}</Alert> : null}
        <Field
          label="기준 사이클"
          hint={
            referenceReason === 'formationless'
              ? 'formation 이 없는 스케줄이라 1번에 앵커합니다 · 입력하면 고정'
              : '유지율·초기 CE·knee 탐색 기준 · Enter 로 적용'
          }
        >
          <input
            type="number"
            min={1}
            value={refDraft}
            onChange={(event) => {
              setRefDraft(event.target.value)
              setRefDirty(true)
            }}
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
  )

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <CellName sample={sample} onSaved={setOverride} />
          <div className="sub">
            {conditions.join('  ·  ') || '조건 미입력'}
            {/* 질량 하나가 이 셀의 모든 mAh/g 를 정한다.  누가 마지막으로
                건드렸는지가 "이 값 맞아?" 의 첫 단서다. */}
            {sample.updated_by || sample.created_by ? (
              <>
                {'  ·  '}
                <By
                  who={sample.updated_by || sample.created_by}
                  at={sample.updated_at}
                  verb="마지막 수정"
                />
              </>
            ) : null}
          </div>
        </div>
        <span className="spacer" />
        {/* 파일로 받는 것과 클립보드로 옮기는 것은 하는 일이 다르다.  한 줄에
            일곱 개가 서 있으면 어느 것이 파일이고 어느 것이 붙여넣기인지
            누르기 전에는 알 수 없어서, 줄을 나눴다. */}
        <div className="col" style={{ gap: 6, alignItems: 'flex-end' }}>
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
              href={api.exportDqdvUrl(sample.id, {
                basis,
                cycles: selected.join(','),
                branches: branches.join(','),
                ...smoothingParams,
              })}
              title="고른 사이클의 dQ/dV — 화면용으로 줄이지 않은 원래 격자 그대로, 지금 평활 설정으로"
            >
              dQ/dV CSV
            </a>
            <a
              className="link-btn"
              href={api.exportDvdqUrl(sample.id, {
                basis,
                cycles: selected.join(','),
                branches: branches.join(','),
                ...smoothingParams,
              })}
              title="고른 사이클의 dV/dQ — 전 해상도. 봉우리 사이 간격을 재는 표입니다"
            >
              dV/dQ CSV
            </a>
            <a
              className="link-btn"
              href={api.exportWorkbookUrl(sample.id, { basis, cycles: selected.join(',') })}
            >
              XLSX
            </a>
          </div>
          <div className="row">
            <span className="tiny faint">클립보드</span>
            {/* 하나에 하나씩.  Origin 은 열 두 개를 받아 하나를 그린다. */}
            <button
              type="button"
              className="link-btn"
              aria-label={copied === '프로파일' ? '프로파일 복사됨' : '프로파일 복사'}
              title={`그려진 곡선을 용량·전압 두 열로 — 곡선 사이는 -- 로 끊는다 · ${basisUnit(profileState.data?.basis ?? basis)}`}
              onClick={() =>
                void copyBlock(
                  '프로파일',
                  profileTsv(profileState.data?.series ?? []),
                  skippedForCopy(profileState.data?.series ?? []),
                )
              }
            >
              {copied === '프로파일' ? '복사됨 ✓' : '프로파일'}
            </button>
            <button
              type="button"
              className="link-btn"
              aria-label={copied === 'dQ/dV' ? 'dQ/dV 복사됨' : 'dQ/dV 복사'}
              disabled={mode !== 'dqdv'}
              title={
                mode === 'dqdv'
                  ? `그려진 dQ/dV 를 전압·값 두 열로 · ${basisUnit(dqdvState.data?.basis ?? basis)}/V`
                  : 'dQ/dV 모드를 켜면 복사할 수 있습니다'
              }
              onClick={() => void copyBlock('dQ/dV', dqdvTsv(dqdvState.data?.series ?? []))}
            >
              {copied === 'dQ/dV' ? '복사됨 ✓' : 'dQ/dV'}
            </button>
            <button
              type="button"
              className="link-btn"
              aria-label={copied === 'dV/dQ' ? 'dV/dQ 복사됨' : 'dV/dQ 복사'}
              disabled={mode !== 'dvdq'}
              title={
                mode === 'dvdq'
                  ? `그려진 dV/dQ 를 용량·값 두 열로 — 첫 열이 용량이다 (dQ/dV 와 반대) · V/${basisUnit(dvdqState.data?.basis ?? basis)}`
                  : 'dV/dQ 모드를 켜면 복사할 수 있습니다'
              }
              onClick={() => void copyBlock('dV/dQ', dvdqTsv(dvdqState.data?.series ?? []))}
            >
              {copied === 'dV/dQ' ? '복사됨 ✓' : 'dV/dQ'}
            </button>
            {/* 아래 세 단추(사이클 · 쿨롱효율 · 사이클+쿨롱)에만 걸린다.
                곡선 쪽은 이미 고른 것만 나가므로 여기 걸 것이 없다. */}
            <div className="segmented" style={{ marginLeft: 4 }}>
              <button
                type="button"
                aria-pressed={cycleScope === 'all'}
                className={cycleScope === 'all' ? 'on' : undefined}
                title={`사이클 복사에 전체 ${cycles.length}개를 담습니다`}
                onClick={() => setCycleScope('all')}
              >
                {/* "전체" 라고만 쓰면 이 화면에 같은 글자의 단추가 셋이 된다 --
                    사이클 고르개의 '전체 선택' 과 그래프의 '전체 범위'. */}
                전체 사이클
              </button>
              <button
                type="button"
                aria-pressed={cycleScope === 'picked'}
                className={cycleScope === 'picked' ? 'on' : undefined}
                title={selected.length
                  ? `위에서 고른 ${selected.length}개만 담습니다 (${selected.join(', ')})`
                  : '고른 사이클이 없습니다'}
                onClick={() => setCycleScope('picked')}
              >
                고른 사이클
              </button>
            </div>
            <button
              type="button"
              className="link-btn"
              aria-label={copied === '사이클' ? '사이클 복사됨' : '사이클 복사'}
              title={`사이클별 방전용량 (${scopeNote}) · ${basisUnit(cycleState.data?.basis ?? basis)}`}
              onClick={() => void copyBlock('사이클', dischargeTsv(copyCycles))}
            >
              {copied === '사이클' ? '복사됨 ✓' : '사이클'}
            </button>
            <button
              type="button"
              className="link-btn"
              aria-label={copied === '쿨롱효율' ? '쿨롱효율 복사됨' : '쿨롱효율 복사'}
              title={`사이클별 쿨롱효율 (%) · ${scopeNote}`}
              onClick={() => void copyBlock('쿨롱효율', efficiencyTsv(copyCycles))}
            >
              {copied === '쿨롱효율' ? '복사됨 ✓' : '쿨롱효율'}
            </button>
            <button
              type="button"
              className="link-btn"
              aria-label={copied === '사이클+쿨롱' ? '사이클과 쿨롱효율 복사됨' : '사이클과 쿨롱효율 복사'}
              title={`한 번에 세 열 — 사이클 · 방전용량(${basisUnit(cycleState.data?.basis ?? basis)}) · 쿨롱효율(%) · ${scopeNote}`}
              onClick={() => void copyBlock('사이클+쿨롱', cycleAndEfficiencyTsv(copyCycles))}
            >
              {copied === '사이클+쿨롱' ? '복사됨 ✓' : '사이클+쿨롱'}
            </button>
          </div>
        </div>
      </div>

      {copyError ? (
        <div style={{ marginBottom: 12 }}>
          <Alert kind="error">{copyError}</Alert>
        </div>
      ) : null}

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

        {/* 계산에 안 들어가는 값들이지만, 셀이 서른 개 쌓이면 라이브러리에서
            무엇과 무엇을 나란히 놓을지를 이것들이 정한다.  셀 상태 바로 밑에
            둔 이유는, 여기가 "이 셀이 무엇이었나" 를 읽는 자리이기 때문이다. */}
        <Card title="시험 조건" tight>
          <div style={{ padding: 'var(--s4)' }}>
            <TestConditionsPanel
              sample={sample}
              schedule={runsState.data?.find((run) => run.schedule?.c_rate)?.schedule}
              onSaved={setOverride}
            />
          </div>
        </Card>

        <div className="split">
          <div className="col" style={{ gap: 12 }}>
            <Card
              title={CURVE_TITLES[mode]}
              actions={
                <div className="row" style={{ gap: 8 }}>
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
                  {/* 모드는 배타적이다.  프로파일은 가로가 용량·세로가 볼트,
                      dQ/dV 는 가로가 볼트·세로가 mAh/V 라 한 그래프에 겹칠 수
                      없다.  충전·방전 토글과 사이클 선택은 둘이 공유한다. */}
                  <div className="segmented">
                    {([
                      ['profile', '프로파일'],
                      ['dqdv', 'dQ/dV'],
                      ['dvdq', 'dV/dQ'],
                    ] as const).map(([value, label]) => (
                      <button
                        key={value}
                        type="button"
                        className={mode === value ? 'on' : ''}
                        onClick={() => setMode(value)}
                      >
                        {label}
                      </button>
                    ))}
                  </div>
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
                  partial={includePartial ? partialCycles : []}
                />
              </div>
              {/* 숫자가 없는 사이클도 곡선은 실측이다.  실측 파일(multi-step
                  CCCV)은 방전이 아예 없어서 표가 비었는데, 2.9 → 4.25 V 로
                  올라간 충전 곡선은 볼 만했고 볼 방법이 없었다. */}
              {partialCycles.length ? (
                <div className="row" style={{ padding: '0 16px 8px', gap: 8, flexWrap: 'wrap' }}>
                  <button
                    type="button"
                    className={includePartial ? 'sm on' : 'sm ghost'}
                    aria-pressed={includePartial}
                    onClick={() => setIncludePartial((was) => !was)}
                  >
                    숫자 없는 사이클 {partialCycles.length}개도 그리기
                  </button>
                  <span className="tiny faint">
                    {partialCycles
                      .slice(0, 4)
                      .map((item) => `${item.cycle}번 ${ko.partialReason(item.reason)}`)
                      .join(' · ')}
                    {partialCycles.length > 4 ? ` 외 ${partialCycles.length - 4}개` : ''}
                    {' — 곡선은 실측이지만 사이클 용량은 나오지 않습니다'}
                  </span>
                </div>
              ) : null}
              {/* 빈 그래프는 고장처럼 보인다.  초기화를 눌러 선택을 비우면
                  충전·방전 버튼을 눌러도 아무 일이 없는데, 화면이 그 이유를
                  말해 주지 않으면 버튼이 죽은 것으로 읽힌다. */}
              {!selected.length ? (
                <Empty title="고른 사이클이 없습니다">
                  위에서 사이클을 고르거나 첫 사이클 · 마지막 · 균등 8개 · 전체를 누르세요
                </Empty>
              ) : !branches.length ? (
                <Empty title="충전도 방전도 꺼져 있습니다">
                  오른쪽 위에서 충전 또는 방전을 켜면 곡선이 그려집니다
                </Empty>
              ) : curve.loading && !curve.data ? (
                <div style={{ padding: 20 }}>
                  <Spinner label={`${CURVE_TITLES[mode]} 계산 중`} />
                </div>
              ) : (
                <>
                  {/* useAsync keeps the previous curves on a failure; without
                      this the stale plot is the only thing on screen. */}
                  {curve.error ? (
                    <div style={{ padding: '12px 16px 0' }}>
                      <Alert kind="error">{curve.error}</Alert>
                    </div>
                  ) : null}
                  <Plot
                    series={shownSeries}
                    xLabel={
                      mode === 'dqdv'
                        ? '전압 (V)'
                        : basisAxis(curve.data?.basis ?? basis)
                    }
                    yLabel={
                      mode === 'dqdv'
                        ? `dQ/dV (${basisUnit(dqdvState.data?.basis ?? basis)}/V)`
                        : mode === 'dvdq'
                          ? `dV/dQ (V/${basisUnit(dvdqState.data?.basis ?? basis)})`
                          : '전압 (V)'
                    }
                    xRange={xRange}
                    yRange={yLock.range}
                    height={400}
                  />
                  {/* 축 고정.  안 잠그면 사이클을 하나만 골랐을 때 y 축이 그
                      곡선에 맞춰 다시 잡혀, 같은 곡선이 훨씬 뚱뚱해 보인다 —
                      숫자는 하나도 안 변했는데 봉우리가 커진 것으로 읽힌다. */}
                  <div className="row" style={{ padding: '6px 16px 0', gap: 12, flexWrap: 'wrap' }}>
                    <AxisLockControl lock={yLock} label="세로축" />
                    <AxisLockControl lock={xLock} label="가로축" />
                    {!xLock.locked && xRange ? (
                      <span className="tiny faint">
                        가로축은 이 셀의 전체 범위에 맞춰 두었습니다
                      </span>
                    ) : null}
                  </div>
                  {mode !== 'profile' ? (
                    <>
                      {/* 평활이 봉우리를 낮추고 넓힌다.  무엇으로 만든 곡선인지
                          말하지 않으면 셀 사이의 봉우리 높이를 비교할 수 없다. */}
                      <div className="row" style={{ padding: '8px 16px 4px', gap: 10, flexWrap: 'wrap' }}>
                        <span className="tiny faint">평활</span>
                        <div className="segmented">
                          {([
                            ['moving', '이동평균'],
                            ['savgol', 'Savitzky-Golay'],
                          ] as const).map(([value, label]) => (
                            <button
                              key={value}
                              type="button"
                              className={smoother === value ? 'on' : ''}
                              onClick={() => setSmoother(value)}
                            >
                              {label}
                            </button>
                          ))}
                        </div>
                        <label className="tiny faint" style={{ display: 'flex', gap: 5, alignItems: 'center' }}>
                          창
                          <input
                            type="number"
                            min={1}
                            max={101}
                            step={2}
                            value={smoothing}
                            onChange={(event) =>
                              setSmoothing(Math.min(101, Math.max(1, Number(event.target.value) || 1)))
                            }
                            style={{ width: 66 }}
                            aria-label="평활 창"
                          />
                          점
                        </label>
                        {smoother === 'savgol' ? (
                          <label className="tiny faint" style={{ display: 'flex', gap: 5, alignItems: 'center' }}>
                            차수
                            <input
                              type="number"
                              min={0}
                              max={6}
                              value={polyOrder}
                              onChange={(event) =>
                                setPolyOrder(Math.min(6, Math.max(0, Number(event.target.value) || 0)))
                              }
                              style={{ width: 56 }}
                              aria-label="다항식 차수"
                            />
                          </label>
                        ) : null}
                      </div>
                      {/* 차수 1 의 SG 는 대칭 창에서 이동평균과 값이 같다 —
                          1차 항이 홀함수라 상쇄된다.  랩 공용 스크립트가 그
                          설정이라 재현용으로 열어 두지만, 그것이 "봉우리가
                          살아난다" 는 뜻은 아니라는 것을 화면이 말해야 한다. */}
                      {smoother === 'savgol' && polyOrder <= 1 ? (
                        <div className="tiny" style={{ padding: '0 16px 4px', color: 'var(--warn)' }}>
                          차수 {polyOrder} 는 이동평균과 같은 값을 냅니다 (대칭 창에서 1차 항이
                          상쇄됩니다). 랩 공용 스크립트가 이 설정입니다 — 봉우리를 살리려면 2 이상.
                        </div>
                      ) : null}
                      <div className="tiny faint" style={{ padding: '0 16px 4px' }}>
                        {mode === 'dqdv' ? (
                          <>
                            전압 격자 {Math.round((dqdvState.data?.voltage_step ?? 0.005) * 1000)}
                            {' mV · 정전압 구간은 제외됩니다 (dV=0)'}
                          </>
                        ) : (
                          <>
                            용량 격자{' '}
                            {formatStep(dvdqState.data?.series.find((s) => s.points)?.capacity_step)}
                            {' '}
                            {basisUnit(dvdqState.data?.basis ?? basis)}
                            {' · 용량이 멈춘 구간(정전압·휴지)은 제외됩니다 (dQ=0)'}
                            {' · 봉우리 사이 간격이 곧 그 구간의 용량입니다'}
                          </>
                        )}
                      </div>
                      {skipped ? (
                        <div className="tiny" style={{ padding: '0 16px 6px', color: 'var(--warn)' }}>
                          {skipped}
                        </div>
                      ) : null}
                    </>
                  ) : null}
                  <PlotLegend
                    series={shownSeries}
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
                height={280}
                markers={kneeMarkers}
              />
            </Card>

            {/* 추세 바로 밑, 폭을 맞춰 눕힌다.  판정과 그 판정을 바꾸는
                설정이 그래프에서 멀면 기준을 하나 눌러 보고 세로선이 어디로
                옮겨졌는지 확인하려고 스크롤을 오르내리게 된다. */}
            <div className="under-trend">
              {reportState.data?.knee ? (
                <Card title="용량 급감 지점" padSmall>
                  <KneeDetail
                    report={reportState.data}
                    selected={kneeMethod ?? reportState.data?.knee?.primary.method ?? ''}
                    onSelect={setKneeMethod}
                  />
                </Card>
              ) : null}
              {analysisSettings}
            </div>

            <Card
              title={`사이클 표 · ${cycles.length}개`}
              actions={
                <div className="row" style={{ gap: 8 }}>
                  <span className="tiny faint">행을 누르면 프로파일에 추가·제거됩니다</span>
                  <button
                    type="button"
                    className="sm"
                    disabled={!selected.length}
                    onClick={() => setChosen([])}
                    title="프로파일 선택을 모두 지웁니다"
                  >
                    초기화
                  </button>
                </div>
              }
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

      {/* 같은 셀의 임피던스.  충방전을 찍다가 EIS 를 찍는 일이 흔해서, 그 둘이
          한 화면에서 이어져야 한다 — GITT 는 중간에 끼우는 일이 드물어 독자
          섹션으로 둔다. */}
      <div style={{ marginTop: 14 }}>
        <CellSpectra sampleId={sample.id} />
      </div>
      {/* 임피던스는 위에서 **그려서** 보여 주고, 여기는 이 셀에 붙어 있는
          측정 전부를 한 줄씩 가리킨다 — GITT 를 포함해서.  겹치는 EIS 줄을
          빼지 않는 것은, 위 카드가 겹쳐 그리는 자리이고 이 카드는 어디로
          가면 되는지를 말하는 자리라 하는 일이 다르기 때문이다. */}
      <div style={{ marginTop: 14 }}>
        <OtherMeasurements sampleId={sample.id}
                           exclude={{ kind: 'cycling', id: sample.id }} />
      </div>
    </main>
  )
}

/** 셀 이름을 제목 자리에서 그대로 고친다.
 *
 *  본체는 `EditableName` 이다 — 임피던스·GITT 상세도 같은 것을 쓴다.  여기는
 *  그 부품에 이 화면의 저장 방법을 물려 주는 얇은 껍데기다.
 */
function CellName({
  sample,
  onSaved,
}: {
  sample: Sample
  onSaved: (updated: Sample) => void
}) {
  return (
    <EditableName
      name={sample.name}
      label="셀 이름"
      onSave={async (name) => onSaved(await api.updateSample(sample.id, { name }))}
    />
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

      {/* 같은 계측을 두 번 내려받은 파일.  목록에서 지우지 않는 이유는 원본이
          불변이기 때문이고 (CLAUDE.md §0.2), 그렇다면 왜 이 파일의 사이클이
          셀에 안 보이는지를 여기서 말해 줘야 한다 — 안 그러면 "203 사이클짜리를
          올렸는데 표에 없다" 가 된다. */}
      {run.superseded_by ? (
        <div className="tiny faint">
          <span className="badge warn">대체됨</span>{' '}
          같은 계측을 더 길게 담은 파일이 있어 이 파일의 사이클은 셀에 넣지
          않습니다. 원본은 그대로 있습니다.
        </div>
      ) : null}

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
        {/* 누가 올렸는지.  20 MB 짜리가 열 개 쌓이면 첫 질문이 이것이다. */}
        <By who={run.created_by} at={run.uploaded_at} verb="올림" />
        <span className="spacer" />
        <a
          className="tiny"
          href={api.exportOriginalUrl(run.id)}
          title={`${run.original_name} 원본을 그대로 내려받습니다`}
        >
          원본 .wrd
        </a>
        <a className="tiny" href={api.exportRawUrl(run.id)}>
          raw CSV
        </a>
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
