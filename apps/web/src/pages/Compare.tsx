/** Overlay several cells: cycle-life curves, or the same cycle's profile. */

import { useEffect, useMemo, useState } from 'react'

import { BasisSelect } from '../components/BasisSelect'
import { Plot, PlotLegend, type PlotSeries } from '../components/Plot'
import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { basisAxis, basisUnit, seriesColor } from '../lib/format'
import { useAsync, useStickyState } from '../lib/hooks'
import type { Basis } from '../lib/types'

type Mode = 'cycles' | 'profiles'

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

export function Compare() {
  const [basis, setBasis] = useStickyState<Basis>('workbench.basis', 'mAh/g')
  const [mode, setMode] = useState<Mode>('cycles')
  const [metric, setMetric] = useState('discharge_capacity')
  const [cycle, setCycle] = useState(3)
  const [branches, setBranches] = useState<('charge' | 'discharge')[]>(['discharge'])
  const [picked, setPicked] = useState<number[]>([])
  const [groupId, setGroupId] = useState<number | null>(null)
  const [hidden, setHidden] = useState<string[]>([])
  const [truncated, setTruncated] = useState(false)

  const groups = useAsync(() => api.listGroups(), [])
  const samples = useAsync(() => api.listSamples({ group_id: groupId }), [groupId])

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
        cycle,
        basis,
        branches: branches.join(','),
      }),
    [ids, cycle, basis, branches.join(',')],
    { enabled: mode === 'profiles' && picked.length > 0 && branches.length > 0 },
  )

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
    const list = profileCompare.data?.series ?? []
    const names = [...new Set(list.map((s) => s.label.split(' · ')[0] ?? s.label))]
    return list.map((item) => {
      const name = item.label.split(' · ')[0] ?? item.label
      return {
        label: item.label,
        x: item.capacity,
        y: item.voltage,
        color: seriesColor(names.indexOf(name)),
        dash: item.branch === 'charge' ? [5, 3] : undefined,
        hidden: hidden.includes(item.label),
      }
    })
  }, [mode, cycleCompare.data, profileCompare.data, hidden])

  const loading = mode === 'cycles' ? cycleCompare.loading : profileCompare.loading
  const error = mode === 'cycles' ? cycleCompare.error : profileCompare.error

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
      for (const item of profileCompare.data?.series ?? []) {
        const name = item.label.split(' · ')[0] ?? item.label
        if (item.basis && item.basis !== basis) found.set(name, item.basis)
      }
    }
    return [...found].map(([name, seriesBasis]) => ({ name, basis: seriesBasis }))
  }, [mode, metric, basis, cycleCompare.data, profileCompare.data])

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
    mode === 'profiles' ? (profileCompare.data?.basis ?? basis) : (cycleCompare.data?.basis ?? basis)

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
    mode === 'profiles'
      ? (profileCompare.data?.series ?? []).map((item) => item.basis)
      : (cycleCompare.data?.series ?? []).map((item) => item.basis)
  const derivedMixed = new Set(seriesBases.filter(Boolean)).size > 1
  const reported =
    mode === 'profiles' ? profileCompare.data?.mixed_basis : cycleCompare.data?.mixed_basis
  const mixedBasis = reported ?? derivedMixed
  const capacityAxis = basisAxis(shownBasis) + (mixedBasis ? ' · 단위 혼재' : '')

  const yLabel =
    mode === 'profiles'
      ? '전압 (V)'
      : metric.endsWith('capacity')
        ? capacityAxis
        : (METRICS.find((m) => m.value === metric)?.label ?? '')
  const xLabel = mode === 'profiles' ? capacityAxis : '사이클'

  return (
    <main className="page">
      <div className="page-head">
        <div>
          <h1>비교</h1>
          <div className="sub">
            {fellBack.length
              ? '여러 셀을 겹쳐 봅니다. 일부 셀은 이 기준으로 정규화할 수 없어 원값으로 그렸습니다.'
              : '여러 셀을 겹쳐 봅니다. 질량이 다른 셀도 같은 기준으로 정규화되어 비교됩니다.'}
          </div>
        </div>
        <span className="spacer" />
        <div className="row">
          <div className="segmented">
            <button
              type="button"
              className={mode === 'cycles' ? 'on' : ''}
              onClick={() => setMode('cycles')}
            >
              사이클 추세
            </button>
            <button
              type="button"
              className={mode === 'profiles' ? 'on' : ''}
              onClick={() => setMode('profiles')}
            >
              충방전 프로파일
            </button>
          </div>
          <BasisSelect value={basis} onChange={setBasis} />
        </div>
      </div>

      <div className="split">
        <div className="col" style={{ gap: 14 }}>
          <Card
            title={mode === 'cycles' ? '사이클 추세' : `${cycle}번 사이클 프로파일`}
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
                  <input
                    type="number"
                    min={1}
                    value={cycle}
                    onChange={(event) => setCycle(Math.max(1, Number(event.target.value)))}
                    style={{ width: 80 }}
                    aria-label="사이클 번호"
                  />
                </div>
              )
            }
            tight
          >
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
                <Plot series={series} xLabel={xLabel} yLabel={yLabel} height={420} />
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
          <div className="col" style={{ gap: 10 }}>
            <Field label="그룹">
              <select
                value={groupId ?? ''}
                onChange={(event) =>
                  setGroupId(event.target.value ? Number(event.target.value) : null)
                }
              >
                <option value="">전체</option>
                {groups.data?.map((group) => (
                  <option key={group.id} value={group.id}>
                    {group.name} ({group.sample_count})
                  </option>
                ))}
              </select>
            </Field>

            <div className="row">
              <button
                type="button"
                className="sm"
                onClick={() => {
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

            <div className="col" style={{ gap: 3, maxHeight: 420, overflow: 'auto' }}>
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
