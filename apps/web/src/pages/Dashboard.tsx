/** One line per cell: running or done, capacity, retention, initial CE, knee.
 *
 * This is the page that answers "3번 셀 지금 어디까지 갔지" without opening
 * anything.
 */

import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { BasisSelect } from '../components/BasisSelect'
import { Alert, Card, Empty, Metric, Spinner, StateBadge } from '../components/ui'
import { api } from '../lib/api'
import { basisUnit, num, pct } from '../lib/format'
import { useAsync, useStickyState } from '../lib/hooks'
import type { Basis, CellState, DashboardRow } from '../lib/types'

type Filter = 'all' | CellState

export function Dashboard() {
  const [basis, setBasis] = useStickyState<Basis>('workbench.basis', 'mAh/g')
  const [groupId, setGroupId] = useState<number | null>(null)
  const [filter, setFilter] = useState<Filter>('all')

  const groups = useAsync(() => api.listGroups(), [])
  const board = useAsync(
    () => api.dashboard({ basis, group_id: groupId }),
    [basis, groupId],
  )

  const rows = useMemo(() => {
    const all = board.data?.rows ?? []
    return filter === 'all' ? all : all.filter((row) => row.state === filter)
  }, [board.data, filter])

  const counts = useMemo(() => {
    const all = board.data?.rows ?? []
    return {
      all: all.length,
      running: all.filter((r) => r.state === 'running').length,
      finished: all.filter((r) => r.state === 'finished').length,
      unknown: all.filter((r) => r.state === 'unknown').length,
    }
  }, [board.data])

  return (
    <main className="page">
      <div className="page-head">
        <div>
          <h1>대시보드</h1>
          <div className="sub">
            구동 중인 셀은 진행 중인 사이클 직전 값을, 종료된 셀은 마지막 사이클 값을
            보여 줍니다. 유지율과 초기 쿨롱효율은 각 셀의 기준 사이클(기본 3번) 대비입니다.
          </div>
        </div>
        <span className="spacer" />
        <div className="row">
          <select
            value={groupId ?? ''}
            onChange={(event) =>
              setGroupId(event.target.value ? Number(event.target.value) : null)
            }
            style={{ width: 180 }}
          >
            <option value="">모든 그룹</option>
            {groups.data?.map((group) => (
              <option key={group.id} value={group.id}>
                {group.name} ({group.sample_count})
              </option>
            ))}
          </select>
          <BasisSelect value={basis} onChange={setBasis} />
        </div>
      </div>

      <div className="grid cols-4" style={{ marginBottom: 14 }}>
        <Card>
          <Metric label="전체 셀" value={counts.all} />
        </Card>
        <Card>
          <Metric label="구동 중" value={counts.running} note="마지막 사이클이 진행 중" />
        </Card>
        <Card>
          <Metric label="종료" value={counts.finished} />
        </Card>
        <Card>
          <Metric label="상태 불명" value={counts.unknown} note="근거 부족 — 수동 지정 가능" />
        </Card>
      </div>

      <Card
        title="셀 현황"
        actions={
          <div className="segmented">
            {(
              [
                ['all', '전체'],
                ['running', '구동 중'],
                ['finished', '종료'],
                ['unknown', '불명'],
              ] as const
            ).map(([value, label]) => (
              <button
                key={value}
                type="button"
                className={filter === value ? 'on' : ''}
                onClick={() => setFilter(value)}
              >
                {label}
              </button>
            ))}
          </div>
        }
        tight
      >
        {board.error ? (
          <div style={{ padding: 14 }}>
            <Alert kind="error">{board.error}</Alert>
          </div>
        ) : board.loading && !board.data ? (
          <div style={{ padding: 20 }}>
            <Spinner />
          </div>
        ) : rows.length ? (
          <DashboardTable rows={rows} basis={basis} />
        ) : (
          <Empty title="표시할 셀이 없습니다">
            <Link to="/upload">.wrd 파일을 올려</Link> 시작하세요.
          </Empty>
        )}
      </Card>
    </main>
  )
}

function DashboardTable({ rows, basis }: { rows: DashboardRow[]; basis: Basis }) {
  const unit = basisUnit(basis)
  return (
    <div className="table-wrap" style={{ maxHeight: 'none' }}>
      <table>
        <thead>
          <tr>
            <th>셀</th>
            <th style={{ textAlign: 'left' }}>상태</th>
            <th>보고 사이클</th>
            <th>방전용량 ({unit})</th>
            <th>유지율 (%)</th>
            <th>기준 사이클</th>
            <th>초기 CE (%)</th>
            <th>급감 시작</th>
            <th>로딩 (mg/cm²)</th>
            <th>완료 사이클</th>
            <th style={{ textAlign: 'left' }}>조건</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.sample_id}>
              <td className="text">
                <Link to={`/samples/${row.sample_id}`}>{row.sample_name}</Link>
              </td>
              <td className="text">
                <StateBadge
                  state={row.state}
                  confidence={row.state_confidence}
                  cycle={row.in_progress_cycle}
                />
              </td>
              <td>{row.reported_cycle ?? '—'}</td>
              <td>{num(row.discharge_capacity)}</td>
              <td>{pct(row.retention_pct, 1)}</td>
              <td>
                {row.reference_cycle ?? '—'}
                {row.reference_cycle && !row.reference_available ? (
                  <span className="badge warn" style={{ marginLeft: 4 }}>
                    대체
                  </span>
                ) : null}
              </td>
              <td>{pct(row.initial_coulombic_efficiency)}</td>
              <td title={row.knee_method ?? undefined}>
                {row.knee_cycle ? Math.round(row.knee_cycle) : '—'}
              </td>
              <td>{num(row.loading_mg_cm2, 3)}</td>
              <td>{row.cycles_complete}</td>
              <td className="text small dim">
                {[
                  row.cathode_type,
                  row.c_rate ? `${row.c_rate}C` : null,
                  row.temperature_c !== null ? `${row.temperature_c}°C` : null,
                  row.test_date,
                ]
                  .filter(Boolean)
                  .join(' · ')}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
