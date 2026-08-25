/** One line per cell: running or done, capacity, retention, initial CE, knee.
 *
 * The page that answers "3번 셀 지금 어디까지 갔지" without opening anything.
 * Each row carries a sparkline because the retention number alone cannot
 * distinguish a steady fade from a cliff.
 */

import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { ActivityFeed } from '../components/ActivityFeed'
import { DeleteSampleButton } from '../components/DeleteSample'
import { PatchNotes } from '../components/PatchNotes'
import { BasisSelect } from '../components/BasisSelect'
import { GroupFilterFields, useGroupChoice } from '../components/GroupFilter'
import { Plot, PlotLegend, type PlotSeries } from '../components/Plot'
import { Sparkline } from '../components/Sparkline'
import { Alert, Card, Empty, StateBadge, TableSkeleton } from '../components/ui'
import { api } from '../lib/api'
import { basisUnit, num, pct, seriesColor } from '../lib/format'
import { useAsync, useStickyState } from '../lib/hooks'
import type { Basis, CellState, DashboardRow } from '../lib/types'

type Filter = 'all' | CellState

const FILTERS: [Filter, string][] = [
  ['all', '전체'],
  ['running', '구동 중'],
  ['finished', '종료'],
  ['unknown', '불명'],
]

export function Dashboard() {
  const [basis, setBasis] = useStickyState<Basis>('workbench.basis', 'mAh/g')
  const [filter, setFilter] = useState<Filter>('all')
  const [hiddenSeries, setHiddenSeries] = useState<string[]>([])

  // 그룹으로 서버에서 거르지 않는다.  칩마다 개수를 보여주려면 전체가 필요하고,
  // 그룹을 누를 때마다 다시 받아오지 않아도 되므로 전환이 즉시 된다.
  const group = useGroupChoice()
  // 남이 무엇을 바꾸면 바로(`live`), 그리고 아무 편집이 없어도 30초마다
  // (`refreshMs`) 다시 읽는다.  둘 다 필요하다: 편집은 알림이 오지만, 구동 중인
  // 셀에 사이클이 붙는 것은 아무도 "편집" 하지 않으므로 알림이 오지 않는다.
  // 이전 값을 지우지 않고 갱신하므로 화면이 깜빡이지 않는다.
  const board = useAsync(() => api.dashboard({ basis }), [basis],
                         { live: true, refreshMs: 30_000 })

  const everything = useMemo(() => board.data?.rows ?? [], [board.data])
  // 상위 그룹을 고르면 그 소그룹의 셀도 남는다 -- `includes` 가 그 한 곳이다.
  const inGroup = group.includes
  const all = useMemo(
    () => everything.filter((row) => inGroup(row.group_id)),
    [everything, inGroup],
  )
  const rows = useMemo(
    () => (filter === 'all' ? all : all.filter((row) => row.state === filter)),
    [all, filter],
  )

  const counts = useMemo(
    () => ({
      all: all.length,
      running: all.filter((r) => r.state === 'running').length,
      finished: all.filter((r) => r.state === 'finished').length,
      unknown: all.filter((r) => r.state === 'unknown').length,
    }),
    [all],
  )

  const attention = useMemo(
    () => all.filter((r) => r.retention_pct !== null && r.retention_pct < 80),
    [all],
  )

  // Built from the sparkline data already in the response, so overlaying every
  // visible cell costs no extra request.
  const overlay: PlotSeries[] = useMemo(
    () =>
      rows
        .filter((row) => row.trend.length > 1 && row.trend_first_cycle !== null)
        .map((row, index) => {
          const first = row.trend_first_cycle!
          const last = row.trend_last_cycle ?? first
          // Use the cycle numbers the server sent.  Assuming even spacing draws
          // cycles 3, 4, 100 at 3, 51.5, 100, which bends the fade curve and
          // moves the knee marker onto a cycle that was never measured.
          const step = row.trend.length > 1 ? (last - first) / (row.trend.length - 1) : 1
          const x =
            row.trend_cycles?.length === row.trend.length
              ? row.trend_cycles
              : row.trend.map((_, i) => first + i * step)
          return {
            label: row.sample_name,
            x,
            y: row.trend,
            color: seriesColor(index),
            hidden: hiddenSeries.includes(row.sample_name),
          }
        }),
    [rows, hiddenSeries],
  )

  return (
    <main className="page">
      <div className="page-head">
        <div>
          <h1>대시보드</h1>
          <div className="sub">
            구동 중인 셀은 진행 중인 사이클 <strong>직전</strong> 값을, 종료된 셀은 마지막
            사이클 값을 보여 줍니다. 유지율과 초기 쿨롱효율은 각 셀의 기준 사이클(기본 3번)
            대비입니다.
          </div>
        </div>
        <span className="spacer" />
        <div className="row">
          <GroupFilterFields pick={group} compact />
          <BasisSelect value={basis} onChange={setBasis} />
        </div>
      </div>

      <Card tight>
        <div className="toolbar">
          <div className="segmented">
            {FILTERS.map(([value, label]) => (
              <button
                key={value}
                type="button"
                className={filter === value ? 'on' : ''}
                onClick={() => setFilter(value)}
              >
                {label}
                <span className="faint" style={{ marginLeft: 5, fontWeight: 500 }}>
                  {counts[value]}
                </span>
              </button>
            ))}

          </div>
          <span className="spacer" />
          {attention.length ? (
            <span className="badge warn" title="기준 사이클 대비 80% 미만">
              유지율 80% 미만 {attention.length}개
            </span>
          ) : null}
          <span className="tiny faint">
            스파크라인은 기준 사이클 대비 유지율 · 점선은 급감이 자리 잡는 지점
          </span>
        </div>

        {board.error ? (
          <div style={{ padding: 16 }}>
            <Alert kind="error">{board.error}</Alert>
          </div>
        ) : board.loading && !board.data ? (
          <TableSkeleton rows={5} columns={8} />
        ) : rows.length ? (
          <DashboardTable rows={rows} basis={basis} onDeleted={() => board.reload()} />
        ) : all.length ? (
          <Empty title="이 조건에 맞는 셀이 없습니다" icon="⌕">
            다른 상태 탭을 눌러 보세요.
          </Empty>
        ) : (
          <Empty title="아직 셀이 없습니다" icon="＋">
            <Link to="/upload">.wrd 파일을 올려</Link> 시작하세요.
          </Empty>
        )}
      </Card>

      {overlay.length > 1 ? (
        <div style={{ marginTop: 12 }}>
          <Card
            title="용량 유지율 겹쳐보기"
            actions={
              <span className="tiny faint">
                각 셀의 기준 사이클 대비 · 자세한 비교는{' '}
                <Link to="/compare">비교 화면</Link>
              </span>
            }
            tight
          >
            <Plot
              series={overlay}
              xLabel="사이클"
              yLabel="용량 유지율 (%)"
              height={260}
              markers={[{ x: 0, label: '' }].slice(0, 0)}
            />
            <PlotLegend
              series={overlay}
              onToggle={(label) =>
                setHiddenSeries((current) =>
                  current.includes(label)
                    ? current.filter((l) => l !== label)
                    : [...current, label],
                )
              }
            />
          </Card>
        </div>
      ) : null}

      {/* 두 칸은 다른 질문에 답한다.  위는 **워크벤치가** 어떻게 바뀌었는지,
          아래는 **데이터가** 어떻게 바뀌었는지.  둘이 나란히 있어야 "어제와
          화면이 다른데" 와 "이 질량 누가 고쳤지" 를 같은 자리에서 본다. */}
      <div style={{ marginTop: 12 }}>
        <Card
          title="패치노트"
          actions={<span className="tiny faint">워크벤치가 무엇이 바뀌었는지</span>}
        >
          <PatchNotes limit={8} />
        </Card>
      </div>

      {/* 한 서버를 여럿이 쓰면 제일 먼저 생기는 질문이 "이거 누가 올렸지" 다. */}
      <div style={{ marginTop: 12 }}>
        <Card
          title="최근 활동"
          actions={<span className="tiny faint">누가 무엇을 바꿨는지</span>}
        >
          <ActivityFeed limit={12} />
        </Card>
      </div>
    </main>
  )
}

function retentionClass(value: number | null): string {
  if (value === null) return ''
  if (value >= 90) return 'good'
  if (value >= 80) return 'mid'
  return 'low'
}

function DashboardTable({
  rows,
  basis,
  onDeleted,
}: {
  rows: DashboardRow[]
  basis: Basis
  onDeleted: () => void
}) {
  // 지우기 버튼은 셀 라이브러리와 공유한다 (DeleteSampleButton) — 무엇이
  // 지워지는가를 설명하는 문구가 두 화면에서 갈라지면 안 된다.
  const [deleteError, setDeleteError] = useState<string | null>(null)
  return (
    <div className="table-wrap tall">
      <table>
        <thead>
          <tr>
            <th>셀</th>
            <th style={{ textAlign: 'left' }}>상태</th>
            <th>보고 사이클</th>
            <th>방전용량 ({basisUnit(basis)})</th>
            <th>유지율 (%)</th>
            <th style={{ textAlign: 'center' }}>추세</th>
            <th>급감 (이탈→정착)</th>
            <th>초기 CE (%)</th>
            <th>기준</th>
            <th>로딩 (mg/cm²)</th>
            <th style={{ textAlign: 'left' }}>조건</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.sample_id}>
              <td className="text">
                {row.group_name ? (
                  <span
                    className="group-tag"
                    style={row.group_color ? { background: row.group_color } : undefined}
                    title={`그룹: ${row.group_name}`}
                  >
                    {row.group_name}
                  </span>
                ) : null}
                {/* 누구 셀인지.  한 서버를 여럿이 쓰면 남의 셀과 내 셀이 이
                    표에서 섞이는데, 이름이 없으면 열어 봐야 안다 (ADR 0012). */}
                {row.owner ? (
                  <span className="owner-tag" title={`만든 사람: ${row.owner}`}>
                    {row.owner}
                  </span>
                ) : null}
                <Link to={`/samples/${row.sample_id}`} style={{ fontWeight: 550 }}>
                  {row.sample_name}
                </Link>
                {row.composition_label ? (
                  <div className="tiny faint truncate" style={{ maxWidth: 210 }}>
                    {row.composition_label}
                  </div>
                ) : null}
              </td>
              <td className="text">
                <StateBadge
                  state={row.state}
                  confidence={row.state_confidence}
                  cycle={row.in_progress_cycle}
                />
              </td>
              <td>
                {row.reported_cycle ?? '—'}
                <span className="faint"> / {row.cycles_complete}</span>
              </td>
              <td style={{ fontWeight: 600 }}>
                {num(row.discharge_capacity)}
                {/* The server normalises row by row and falls back to raw mAh
                    when a cell has no mass or area, so one column header cannot
                    speak for every row. */}
                {row.basis && row.basis !== basis ? (
                  <span
                    className="badge warn"
                    style={{ marginLeft: 4 }}
                    title="질량·면적이 없어 원값으로 표시합니다"
                  >
                    {basisUnit(row.basis)}
                  </span>
                ) : null}
              </td>
              <td className="bar-cell">
                {pct(row.retention_pct, 1)}
                {row.retention_pct !== null ? (
                  <span className="bar">
                    <i
                      className={retentionClass(row.retention_pct)}
                      style={{ width: `${Math.max(0, Math.min(100, row.retention_pct))}%` }}
                    />
                  </span>
                ) : null}
              </td>
              <td style={{ textAlign: 'center', padding: '2px 8px' }}>
                <Sparkline
                  values={row.trend}
                  markIndex={row.knee_trend_index}
                  // 서버는 이탈 시작 자리도 함께 보낸다 (ADR 0021).  그림에
                  // point 만 긋고 옆 칸에 "96→131" 이라고 적으면, 두 수 중
                  // 어느 쪽이 선인지 볼 수가 없다.
                  onsetIndex={row.knee_onset_trend_index}
                  title={
                    row.trend.length
                      ? `사이클 ${row.trend_first_cycle}–${row.trend_last_cycle} 유지율`
                      : '데이터 없음'
                  }
                />
              </td>
              <td title={row.knee_method ?? undefined}>
                {/* onset 이 있으면 둘 다 적는다.  point 하나만 적어 놓고 열
                    머리말이 "급감 시작" 이면 화면이 거짓을 말한다. */}
                {row.knee_cycle
                  ? row.knee_onset_cycle
                    ? `${Math.round(row.knee_onset_cycle)}→${Math.round(row.knee_cycle)}`
                    : Math.round(row.knee_cycle)
                  : '—'}
              </td>
              <td>{pct(row.initial_coulombic_efficiency)}</td>
              <td>
                {row.reference_cycle ?? '—'}
                {row.reference_cycle && !row.reference_available ? (
                  <span className="badge warn" style={{ marginLeft: 4 }} title="기준 사이클이 없어 대체했습니다">
                    대체
                  </span>
                ) : null}
              </td>
              <td>{num(row.loading_mg_cm2, 3)}</td>
              <td className="text small dim">
                {[
                  row.cathode_type,
                  row.c_rate ? `${row.c_rate}C` : null,
                  row.temperature_c !== null ? `${row.temperature_c}°C` : null,
                  row.test_date,
                ]
                  .filter(Boolean)
                  .join(' · ') || '—'}
              </td>
              <td style={{ whiteSpace: 'nowrap' }}>
                <DeleteSampleButton
                  sampleId={row.sample_id}
                  sampleName={row.sample_name}
                  onDeleted={onDeleted}
                  onError={setDeleteError}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {deleteError ? (
        <div style={{ padding: '10px 14px 0' }}>
          <Alert kind="error">{deleteError}</Alert>
        </div>
      ) : null}
    </div>
  )
}
