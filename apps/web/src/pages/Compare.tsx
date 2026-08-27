/** Overlay several cells: cycle-life curves, or the same cycle's profile. */

import { useEffect, useMemo, useRef, useState } from 'react'

import { AxisLockControl, useAxisLock } from '../components/AxisLock'
import { BasisSelect } from '../components/BasisSelect'
import { CopyBar } from '../components/CopyBar'
import { GroupFilterFields, useGroupChoice } from '../components/GroupFilter'
import { Plot, PlotLegend, type PlotSeries } from '../components/Plot'
import { Alert, Card, Empty, Spinner } from '../components/ui'
import { keepInPlace } from '../lib/anchor'
import { api } from '../lib/api'
import { basisAxis, basisUnit, seriesColor } from '../lib/format'
import {
  compareCyclesWideTsv, dqdvWideTsv, dvdqWideTsv, profileWideTsv, skippedForCopy,
} from '../lib/origin'
import { useAsync, useStickyState } from '../lib/hooks'
import type { Basis, Smoother } from '../lib/types'

/** 겹쳐 볼 수 있는 네 가지.  뒤의 셋은 "한 사이클을 여러 셀에서" 라는 같은
 *  질문을 세 축으로 보는 것이라 사이클 번호와 충전·방전 토글을 공유한다. */
type Mode = 'cycles' | 'profiles' | 'dqdv' | 'dvdq'

const CURVE_MODES: Mode[] = ['profiles', 'dqdv', 'dvdq']

const MODE_LABELS: Record<Mode, string> = {
  cycles: '사이클 추세',
  profiles: '충방전 프로파일',
  dqdv: 'dQ/dV',
  dvdq: 'dV/dQ',
}

/** Matches the server's own limit (apps/api/app/routers/analysis.py: "compare
 *  at most 30 samples at a time"), so "모두 선택" only ever stops where the
 *  backend would refuse anyway — and says so when it does. */
const SELECT_ALL_LIMIT = 30

const METRICS = [
  { value: 'discharge_capacity', label: '방전용량' },
  { value: 'retention', label: '유지율' },
  { value: 'coulombic_efficiency', label: '쿨롱효율' },
  { value: 'energy_efficiency', label: '에너지효율' },
  { value: 'mean_discharge_voltage', label: '평균 방전전압' },
  { value: 'voltage_hysteresis', label: '전압 이력' },
]

/** 사이클 지정을 제목으로.  `"all"` 은 몇 번인지 여기서 알 수 없다 --
 *  고른 셀마다 다르므로 서버가 정하고, 화면은 "전체" 라고만 적는다. */
function cycleTitle(spec: string, drawn: number[]): string {
  const text = spec.trim()
  if (!text) return '3번 사이클'
  if (text.toLowerCase() !== 'all') return `${text}번 사이클`
  // 몇 번인지는 고른 셀마다 달라 요청만으로는 모른다 — 서버가 정한 것을 적는다.
  if (!drawn.length) return '전체 사이클'
  return `전체 사이클 · ${drawn[0]}–${drawn[drawn.length - 1]}번 중 ${drawn.length}개`
}

export function Compare() {
  const [basis, setBasis] = useStickyState<Basis>('workbench.basis', 'mAh/g')
  const [mode, setMode] = useState<Mode>('cycles')
  const [metric, setMetric] = useState('discharge_capacity')
  // 사이클은 숫자 하나가 아니라 **지정**이다: "3", "3,4", "1-5", "all".
  // 한 셀의 3번과 20번을 겹쳐 놓고 열화를 보는 일이 흔한데, 숫자 칸 하나로는
  // 그것을 시킬 방법이 없었다.  문법은 내보내기 화면과 같다.
  const [cycleSpec, setCycleSpec] = useState('3')
  // 타이핑 중간의 "3," 로 요청이 나가지 않게, 칸을 떠날 때/엔터에만 옮긴다.
  const [cycleDraft, setCycleDraft] = useState('3')
  const [branches, setBranches] = useState<('charge' | 'discharge')[]>(['discharge'])
  // 비교 화면에서 평활이 특히 중요하다.  봉우리 *높이* 는 창·필터·차수가 모두
  // 같은 곡선끼리만 비교되는데(ADR 0013), 여기가 바로 사람이 높이를 눈으로 재는
  // 곳이다.  서버가 선택한 모든 셀에 같은 설정을 적용한다.
  const [smoother, setSmoother] = useStickyState<Smoother>('workbench.smoother', 'moving')
  const [smoothing, setSmoothing] = useStickyState<number>('workbench.smoothing', 5)
  const [polyOrder, setPolyOrder] = useStickyState<number>('workbench.polyOrder', 2)
  const [picked, setPicked] = useState<number[]>([])
  const [hidden, setHidden] = useState<string[]>([])
  const [truncated, setTruncated] = useState(false)
  const pickBox = useRef<HTMLDivElement>(null)

  const group = useGroupChoice()
  // 서버가 상위 그룹을 소그룹까지 펴 준다 (`deps.group_scope`) -- 여기서 다시
  // 거르지 않는다.  두 곳에서 거르면 규칙이 갈라진다.
  const samples = useAsync(() => api.listSamples({ group_id: group.effective }),
                           [group.effective], { live: true })

  // An empty comparison is never what someone came here for; start with the
  // cells in view and let them narrow down.
  const [touched, setTouched] = useState(false)
  useEffect(() => {
    if (touched || !samples.data?.length) return
    setPicked(samples.data.slice(0, 6).map((sample) => sample.id))
  }, [samples.data, touched])

  const ids = picked.join(',')
  const cycleCompare = useAsync(
    () => api.compareCycles({ sample_ids: ids, metric, basis }),
    [ids, metric, basis],
    { enabled: mode === 'cycles' && picked.length > 0 },
  )
  const profileCompare = useAsync(
    () =>
      api.compareProfiles({
        sample_ids: ids,
        cycles: cycleSpec,
        basis,
        branches: branches.join(','),
      }),
    [ids, cycleSpec, basis, branches.join(',')],
    { enabled: mode === 'profiles' && picked.length > 0 && branches.length > 0 },
  )

  const smoothingParams = {
    smoother,
    smoothing,
    ...(smoother === 'savgol' ? { poly_order: polyOrder } : {}),
  }
  const smoothingKey = `${smoother}|${smoothing}|${polyOrder}`
  const curveDeps = [ids, cycleSpec, basis, branches.join(','), smoothingKey]

  const dqdvCompare = useAsync(
    () => api.compareDqdv({ sample_ids: ids, cycles: cycleSpec, basis,
                            branches: branches.join(','), ...smoothingParams }),
    curveDeps,
    { enabled: mode === 'dqdv' && picked.length > 0 && branches.length > 0 },
  )
  const dvdqCompare = useAsync(
    () => api.compareDvdq({ sample_ids: ids, cycles: cycleSpec, basis,
                            branches: branches.join(','), ...smoothingParams }),
    curveDeps,
    { enabled: mode === 'dvdq' && picked.length > 0 && branches.length > 0 },
  )

  /** 곡선 세 모드가 쓰는 응답.  하나로 모아 두면 아래의 축 라벨·단위 경고·
   *  범례가 모드마다 갈라지지 않는다 — 갈라지면 한 모드에만 경고가 빠진다. */
  const curveCompare =
    mode === 'profiles' ? profileCompare
    : mode === 'dqdv' ? dqdvCompare
    : mode === 'dvdq' ? dvdqCompare
    : null

  /** 지금 모드가 그리는 계열들.  x/y 는 모드마다 다른 배열에서 온다. */
  const curveSeries = useMemo(() => {
    if (mode === 'profiles') {
      return (profileCompare.data?.series ?? []).map((item) => ({
        item, x: item.capacity, y: item.voltage,
      }))
    }
    if (mode === 'dqdv') {
      return (dqdvCompare.data?.series ?? [])
        .filter((item) => item.points > 0)
        .map((item) => ({ item, x: item.voltage, y: item.dqdv }))
    }
    if (mode === 'dvdq') {
      return (dvdqCompare.data?.series ?? [])
        .filter((item) => item.points > 0)
        .map((item) => ({ item, x: item.capacity, y: item.dvdq }))
    }
    return []
  }, [mode, profileCompare.data, dqdvCompare.data, dvdqCompare.data])

  const series: PlotSeries[] = useMemo(() => {
    if (mode === 'cycles') {
      return (cycleCompare.data?.series ?? []).map((item, index) => ({
        label: item.sample_name,
        x: item.points.map((p) => p.cycle),
        y: item.points.map((p) => p.value),
        color: seriesColor(index),
        hidden: hidden.includes(item.sample_name),
      }))
    }
    // 셀 이름으로 색을 준다 — 한 셀의 충전과 방전이 같은 색, 파선으로 갈린다.
    const names = [...new Set(curveSeries.map(({ item }) =>
      item.label.split(' · ')[0] ?? item.label))]
    return curveSeries.map(({ item, x, y }) => ({
      label: item.label,
      x,
      y,
      color: seriesColor(names.indexOf(item.label.split(' · ')[0] ?? item.label)),
      dash: item.branch === 'charge' ? [5, 3] : undefined,
      hidden: hidden.includes(item.label),
    }))
  }, [mode, cycleCompare.data, curveSeries, hidden])

  // 서버가 실제로 그린 사이클과, 골라 뽑았다면 그 한 줄.  `all` 은 요청만
  // 봐서는 무엇이 그려졌는지 알 수 없다 -- 고른 셀마다 다르다.
  const drawnCycles = curveCompare?.data?.cycles ?? []
  const cyclesNote = curveCompare?.data?.cycles_note ?? ''

  const loading = mode === 'cycles' ? cycleCompare.loading : (curveCompare?.loading ?? false)
  const error = mode === 'cycles' ? cycleCompare.error : (curveCompare?.error ?? null)

  // 축 고정.  여기서도 이유는 같다 — 셀을 하나 빼면 y 축이 다시 잡혀서 남은
  // 곡선이 갑자기 커 보인다.  단위가 바뀌면(모드·기준·평활) 자동으로 풀린다.
  const yLock = useAxisLock(series, 'y', `${mode}|${basis}|${metric}|${smoothingKey}`)
  const xLock = useAxisLock(series, 'x', `${mode}|${basis}|${metric}`)

  // The backend normalises each cell on its own: one without an active mass comes
  // back in raw mAh while its neighbours are in mAh/g, and only the per-series
  // `basis` says so.  Two curves in different units on one axis read as a
  // forty-times-worse cell, so the fallbacks are named before they mislead.
  const fellBack = useMemo(() => {
    const found = new Map<string, string>()
    if (mode === 'cycles') {
      if (!metric.endsWith('capacity')) return []
      for (const item of cycleCompare.data?.series ?? []) {
        if (item.basis && item.basis !== basis) found.set(item.sample_name, item.basis)
      }
    } else {
      for (const { item } of curveSeries) {
        const name = item.label.split(' · ')[0] ?? item.label
        if (item.basis && item.basis !== basis) found.set(name, item.basis)
      }
    }
    return [...found].map(([name, seriesBasis]) => ({ name, basis: seriesBasis }))
  }, [mode, metric, basis, cycleCompare.data, curveSeries])

  // 유지율은 "무엇 대비" 가 곡선의 뜻을 정한다.  기준 사이클이 없는 셀은
  // 서버가 다른 사이클로 대체하는데(ADR 0004), 그 사실이 화면에 없으면
  // 3번 대비 69% 인 셀과 201번 대비 100% 인 셀이 같은 축에서 같은 뜻으로
  // 읽힌다 — 열화된 셀이 멀쩡해 보인다.
  const rebased = useMemo(() => {
    if (mode !== 'cycles' || !metric.startsWith('retention')) return []
    return (cycleCompare.data?.series ?? [])
      .filter((item) => item.reference_available === false)
      .map((item) => ({
        name: item.sample_name,
        cycle: item.reference_cycle_used ?? null,
      }))
  }, [mode, metric, cycleCompare.data])

  // Label the axis from what came back, never from what was asked for.
  const shownBasis: Basis =
    mode === 'cycles' ? (cycleCompare.data?.basis ?? basis)
                      : ((curveCompare?.data?.basis as Basis | undefined) ?? basis)

  // Falling back is not the same as mixing.  When every selected cell lacks a
  // mass they all come back in raw mAh — one unit, one axis, a comparison that
  // is still valid.  Warning "단위 혼재" there tells the user not to trust a
  // plot that is perfectly trustworthy, so the server's own verdict decides.
  //
  // 필드가 없는 옛 응답(갱신 전 서버가 아직 떠 있는 경우)에서 `?? false` 로
  // 두면 정반대 안내가 나간다 — 실제로 단위가 섞여 있는데 "전부 같은 단위라
  // 비교가 유효합니다" 라고 말한다.  없으면 그린 곡선의 단위 집합에서 직접
  // 유도한다.
  const seriesBases =
    mode === 'cycles'
      ? (cycleCompare.data?.series ?? []).map((item) => item.basis)
      : curveSeries.map(({ item }) => item.basis)
  const derivedMixed = new Set(seriesBases.filter(Boolean)).size > 1
  const reported =
    mode === 'cycles' ? cycleCompare.data?.mixed_basis : curveCompare?.data?.mixed_basis
  const mixedBasis = reported ?? derivedMixed
  const capacityAxis = basisAxis(shownBasis) + (mixedBasis ? ' · 단위 혼재' : '')

  const yLabel =
    mode === 'profiles'
      ? '전압 (V)'
      : mode === 'dqdv'
        ? `dQ/dV (${basisUnit(shownBasis)}/V)`
        : mode === 'dvdq'
          ? `dV/dQ (V/${basisUnit(shownBasis)})`
          : metric.endsWith('capacity')
            ? capacityAxis
            : (METRICS.find((m) => m.value === metric)?.label ?? '')
  const xLabel =
    mode === 'cycles' ? '사이클'
    : mode === 'dqdv' ? '전압 (V)'
    : capacityAxis

  /** 만들지 못한 곡선이 왜 없는지 — 비교 화면은 빈 곡선을 싣지 않으므로
   *  서버가 아예 안 보낸다.  대신 "고른 셀 중 몇 개가 이 사이클을 못 낸다" 를
   *  셀 수로 말해 준다. */
  const missingCells = useMemo(() => {
    if (mode === 'cycles' || !curveCompare?.data) return 0
    const drawn = new Set(curveSeries.map(({ item }) =>
      item.label.split(' · ')[0] ?? item.label))
    return Math.max(0, picked.length - drawn.size)
  }, [mode, curveCompare?.data, curveSeries, picked.length])

  return (
    <main className="page">
      <div className="page-head">
        <div>
          <h1>비교</h1>
          <div className="sub">
            {mode === 'dvdq'
              ? '봉우리 사이의 가로 거리가 그 구간의 용량입니다 — 전극 슬리피지를 자로 재듯 읽습니다.'
              : fellBack.length
                ? '여러 셀을 겹쳐 봅니다. 일부 셀은 이 기준으로 정규화할 수 없어 원값으로 그렸습니다.'
                : '여러 셀을 겹쳐 봅니다. 질량이 다른 셀도 같은 기준으로 정규화되어 비교됩니다.'}
          </div>
        </div>
        <span className="spacer" />
        <div className="row">
          <div className="segmented">
            {(['cycles', ...CURVE_MODES] as Mode[]).map((value) => (
              <button
                key={value}
                type="button"
                className={mode === value ? 'on' : ''}
                onClick={() => setMode(value)}
              >
                {MODE_LABELS[value]}
              </button>
            ))}
          </div>
          <BasisSelect value={basis} onChange={setBasis} />
        </div>
      </div>

      {/* 그래프를 오른쪽 340px 레일에 눌리지 않게 폭 전체로 두고, 셀 선택을
          그 아래로 눕혔다.  고르는 조건이 그룹·소그룹까지 늘어나 레일에 넣으면
          체크박스 한 줄이 이름 하나도 못 담는다 -- 반대로 아래는 가로가 넓어서
          체크박스를 여러 열로 깔 수 있다. */}
      <div className="col" style={{ gap: 14 }}>
        <div className="col" style={{ gap: 14 }}>
          <Card
            title={mode === 'cycles'
              ? '사이클 추세'
              : `${cycleTitle(cycleSpec, drawnCycles)} · ${MODE_LABELS[mode]}`}
            actions={
              mode === 'cycles' ? (
                <select
                  value={metric}
                  onChange={(event) => setMetric(event.target.value)}
                  style={{ width: 170 }}
                >
                  {METRICS.map((item) => (
                    <option key={item.value} value={item.value}>
                      {item.label}
                    </option>
                  ))}
                </select>
              ) : (
                <div className="row">
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
                  <div className="row" style={{ gap: 6 }}>
                    <input
                      type="text"
                      inputMode="numeric"
                      value={cycleDraft}
                      placeholder="3,4"
                      onChange={(event) => setCycleDraft(event.target.value)}
                      onBlur={() => setCycleSpec(cycleDraft.trim() || '3')}
                      onKeyDown={(event) => {
                        if (event.key === 'Enter') event.currentTarget.blur()
                      }}
                      style={{ width: 96 }}
                      aria-label="사이클 번호"
                      title="여러 개 가능 — 3,4 또는 1-5"
                    />
                    <button
                      type="button"
                      className={cycleSpec === 'all' ? 'sm on' : 'ghost sm'}
                      onClick={() => {
                        setCycleDraft('all')
                        setCycleSpec('all')
                      }}
                      title="이 셀들이 가진 사이클 전부 — 곡선이 너무 많으면 몇 개인지 말해 줍니다"
                    >
                      전체
                    </button>
                    <span className="tiny faint">여러 개 가능 · 3,4 · 1-5</span>
                  </div>
                </div>
              )
            }
            tight
          >
            {/* Origin 으로 — 지금 보고 있는 것만 낸다.  모드마다 축이 다르므로
                복사되는 두 열의 뜻도 달라진다 (EIS·GITT 와 같은 규칙). */}
            <div style={{ padding: '12px 14px 0' }}>
              <CopyBar
                items={mode === 'cycles' ? [{
                  label: MODE_LABELS.cycles,
                  title: `사이클 · ${METRICS.find((m) => m.value === metric)?.label ?? '값'}`
                    + ' — 셀마다 두 열',
                  disabled: !(cycleCompare.data?.series ?? []).length,
                  // 열마다 어느 셀인지 이름을 얹는다.  여기서는 열 한 쌍이
                  // 저마다 다른 셀이라, 워크시트에는 그것을 적을 자리가 없다.
                  build: () => compareCyclesWideTsv(cycleCompare.data?.series ?? [], {
                    x: '사이클',
                    y: METRICS.find((m) => m.value === metric)?.label ?? '값',
                  }),
                }] : mode === 'profiles' ? [{
                  label: MODE_LABELS.profiles,
                  title: '용량 · 전압 — 곡선마다 두 열 (셀 → 사이클 순)',
                  disabled: !(profileCompare.data?.series ?? []).length,
                  build: () => profileWideTsv(profileCompare.data?.series ?? [], {
                    x: `용량 (${basisUnit(profileCompare.data?.basis ?? basis)})`,
                    y: '전압 (V)',
                  }),
                  skipped: skippedForCopy(profileCompare.data?.series ?? []),
                  skippedNote: (n) => `구동 중이라 마지막 사이클이 잘린 셀 ${n}개는 뺐습니다`,
                }] : mode === 'dqdv' ? [{
                  label: MODE_LABELS.dqdv,
                  title: '전압 · dQ/dV — 곡선마다 두 열 (셀 → 사이클 순)',
                  disabled: !(dqdvCompare.data?.series ?? []).length,
                  build: () => dqdvWideTsv(dqdvCompare.data?.series ?? [], {
                    x: '전압 (V)',
                    y: `dQ/dV (${basisUnit(dqdvCompare.data?.basis ?? basis)}/V)`,
                  }),
                }] : [{
                  label: MODE_LABELS.dvdq,
                  // dQ/dV 의 거울이라 열 순서를 헷갈리기 쉽다 -- 여기 적어 둔다.
                  title: '용량 · dV/dQ — 곡선마다 두 열 (dQ/dV 와 x 가 반대)',
                  disabled: !(dvdqCompare.data?.series ?? []).length,
                  build: () => dvdqWideTsv(dvdqCompare.data?.series ?? [], {
                    x: `용량 (${basisUnit(dvdqCompare.data?.basis ?? basis)})`,
                    y: `dV/dQ (V/${basisUnit(dvdqCompare.data?.basis ?? basis)})`,
                  }),
                }]}
              />
            </div>
            {error ? (
              <div style={{ padding: 14 }}>
                <Alert kind="error">{error}</Alert>
              </div>
            ) : !picked.length ? (
              <Empty title="비교할 셀을 오른쪽에서 고르세요" icon="⇢" />
            ) : loading && !series.length ? (
              <div style={{ padding: 20 }}>
                <Spinner />
              </div>
            ) : (
              <>
                {rebased.length ? (
                  <div style={{ padding: '12px 14px 0' }}>
                    <Alert kind="warn">
                      기준 사이클이 없어 다른 사이클을 기준으로 삼은 셀이 있습니다 —{' '}
                      {rebased
                        .map((item) =>
                          item.cycle ? `${item.name} (${item.cycle}번 대비)` : item.name,
                        )
                        .join(', ')}
                      . 곡선마다 100% 의 뜻이 다르므로 유지율을 그대로 비교하지 마세요.
                    </Alert>
                  </div>
                ) : null}
                {fellBack.length ? (
                  <div style={{ padding: '12px 14px 0' }}>
                    <Alert kind={mixedBasis ? 'warn' : 'info'}>
                      {mixedBasis ? (
                        <>
                          {basisUnit(basis)} 로 표시할 수 없어 원값으로 그린 셀이 있습니다 —{' '}
                          {fellBack
                            .map((item) => `${item.name} (${basisUnit(item.basis)})`)
                            .join(', ')}
                          . 축 단위가 셀마다 다르므로 곡선 높이를 그대로 비교하지 마세요.
                        </>
                      ) : (
                        <>
                          선택한 셀에 {basisUnit(basis)} 로 바꿀 정보가 없어 전부{' '}
                          {basisUnit(shownBasis)} 로 그렸습니다. 단위는 같으므로 비교는
                          유효합니다 — 질량·면적을 넣으면 정규화됩니다.
                        </>
                      )}
                    </Alert>
                  </div>
                ) : null}
                {cyclesNote ? (
                  <div style={{ padding: '12px 14px 0' }}>
                    <Alert kind="info">{cyclesNote}</Alert>
                  </div>
                ) : null}
                {missingCells ? (
                  <div className="tiny" style={{ padding: '8px 14px 0', color: 'var(--warn)' }}>
                    고른 셀 중 {missingCells}개는 {cycleTitle(cycleSpec, drawnCycles)}을
                    완료하지 않았거나 이 곡선을 만들지 못해 빠졌습니다.
                  </div>
                ) : null}
                <Plot
                  series={series}
                  xLabel={xLabel}
                  yLabel={yLabel}
                  xRange={xLock.range}
                  yRange={yLock.range}
                  height={420}
                  // 고른 것을 바꾸면 새 곡선이 올 때까지 옛 곡선이 그대로
                  // 서 있다.  표시가 없으면 화면이 눌린 것을 못 알아들은
                  // 것처럼 보이고, 사람은 같은 것을 한 번 더 누른다.
                  busy={loading}
                />
                {/* 셀을 하나 빼면 y 축이 다시 잡혀서 남은 곡선이 갑자기 커
                    보인다.  잠그면 눈금이 그대로 남는다. */}
                <div className="row" style={{ padding: '6px 14px 0', gap: 12, flexWrap: 'wrap' }}>
                  <AxisLockControl lock={yLock} label="세로축" />
                  <AxisLockControl lock={xLock} label="가로축" />
                </div>
                {mode === 'dqdv' || mode === 'dvdq' ? (
                  <>
                    <div className="row" style={{ padding: '8px 14px 0', gap: 10, flexWrap: 'wrap' }}>
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
                    <div className="tiny faint" style={{ padding: '4px 14px 0' }}>
                      선택한 모든 셀을 같은 격자·같은 창으로 만듭니다 — 봉우리 높이는 그래야
                      비교할 수 있습니다.
                      {smoother === 'savgol' && polyOrder <= 1
                        ? ' 차수 1 은 이동평균과 같은 값입니다 (랩 공용 스크립트 설정).'
                        : ''}
                      {mode === 'dvdq' ? ' 봉우리 사이 간격이 곧 그 구간의 용량입니다.' : ''}
                    </div>
                  </>
                ) : null}
                <PlotLegend
                  series={series}
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
        </div>

        <Card title={`셀 선택 · ${picked.length}개`}>
          {/* 고르개는 그림 밑에 있다.  체크를 하나 누르면 위쪽이 다시 그려지며
              높이가 변하고 (범례가 한 줄 늘거나 줄고, 경고가 뜨거나 사라진다)
              고르개가 그만큼 움직인다 — 다음에 누르려던 칸이 커서 밑에서
              사라진다.  누른 순간의 자리를 붙잡아 둔다 (`lib/anchor`). */}
          {/* 체크만이 아니라 그룹·소그룹도 목록의 길이를 바꾼다 — `change` 는
              거품처럼 올라오므로 상자 하나에 걸면 그 안의 무엇을 건드려도
              자리가 유지된다. */}
          <div className="col" style={{ gap: 10 }} ref={pickBox}
               onChange={() => keepInPlace(pickBox.current)}>
            <div className="grid cols-2" style={{ gap: 10 }}>
              <GroupFilterFields pick={group} hint="소그룹까지 골라 좁힐 수 있습니다" />
            </div>

            <div className="row">
              <button
                type="button"
                className="sm"
                onClick={() => {
                  // 여기가 높이를 가장 크게 바꾼다 — 한 번에 서른 줄이 붙는다.
                  keepInPlace(pickBox.current)
                  setTouched(true)
                  const all = samples.data ?? []
                  setPicked(all.slice(0, SELECT_ALL_LIMIT).map((s) => s.id))
                  setTruncated(all.length > SELECT_ALL_LIMIT)
                }}
              >
                모두 선택
              </button>
              <button
                type="button"
                className="sm ghost"
                onClick={() => {
                  keepInPlace(pickBox.current)
                  setTouched(true)
                  setTruncated(false)
                  setPicked([])
                }}
              >
                해제
              </button>
            </div>

            {truncated ? (
              <Alert kind="warn">
                앞 {SELECT_ALL_LIMIT}개만 선택했습니다 — 한 번에 비교할 수 있는 서버 상한입니다.
              </Alert>
            ) : null}

            <div className="pick-grid">
              {samples.data?.map((sample) => (
                <label
                  key={sample.id}
                  className="row small"
                  style={{ gap: 7, cursor: 'pointer' }}
                >
                  <input
                    type="checkbox"
                    checked={picked.includes(sample.id)}
                    onChange={() => {
                      setTouched(true)
                      setTruncated(false)
                      setPicked((current) =>
                        current.includes(sample.id)
                          ? current.filter((id) => id !== sample.id)
                          : [...current, sample.id],
                      )
                    }}
                    style={{ width: 'auto' }}
                  />
                  <span style={{ minWidth: 0 }}>
                    <span className="truncate" style={{ display: 'block' }}>
                      {sample.name}
                    </span>
                    <span className="tiny faint truncate" style={{ display: 'block' }}>
                      {[
                        sample.cathode_type,
                        sample.resolved_cell.composition_compact_label,
                        sample.c_rate ? `${sample.c_rate}C` : null,
                      ]
                        .filter(Boolean)
                        .join(' · ')}
                    </span>
                  </span>
                </label>
              ))}
              {samples.error ? (
                <Alert kind="error">{samples.error}</Alert>
              ) : samples.loading && !samples.data ? (
                <Spinner />
              ) : !samples.data?.length ? (
                <div className="tiny faint">셀이 없습니다.</div>
              ) : null}
            </div>
          </div>
        </Card>
      </div>
    </main>
  )
}
