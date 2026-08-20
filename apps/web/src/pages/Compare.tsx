/** Overlay several cells: cycle-life curves, or the same cycle's profile. */

import { useEffect, useMemo, useState } from 'react'

import { BasisSelect } from '../components/BasisSelect'
import { Plot, PlotLegend, type PlotSeries } from '../components/Plot'
import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { basisAxis, seriesColor } from '../lib/format'
import { useAsync, useStickyState } from '../lib/hooks'
import type { Basis } from '../lib/types'

type Mode = 'cycles' | 'profiles'

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

  const yLabel =
    mode === 'profiles'
      ? '전압 (V)'
      : metric === 'discharge_capacity'
        ? basisAxis(basis)
        : (METRICS.find((m) => m.value === metric)?.label ?? '')
  const xLabel = mode === 'profiles' ? basisAxis(basis) : '사이클'

  return (
    <main className="page">
      <div className="page-head">
        <div>
          <h1>비교</h1>
          <div className="sub">
            여러 셀을 겹쳐 봅니다. 질량이 다른 셀도 같은 기준으로 정규화되어 비교됩니다.
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
                  setPicked((samples.data ?? []).map((s) => s.id).slice(0, 12))
                }}
              >
                모두 선택
              </button>
              <button
                type="button"
                className="sm ghost"
                onClick={() => {
                  setTouched(true)
                  setPicked([])
                }}
              >
                해제
              </button>
            </div>

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
              {!samples.data?.length ? (
                <div className="tiny faint">셀이 없습니다.</div>
              ) : null}
            </div>
          </div>
        </Card>
      </div>
    </main>
  )
}
