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
import { FolderRow, useFolders } from '../components/FolderTree'
import { GroupFilterFields, groupPath, useGroupChoice } from '../components/GroupFilter'
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

/** 겹쳐 보기의 세로 범위 — 튄 곡선 하나가 나머지를 납작하게 만들지 않도록.
 *
 *  실측 2026-08-26: 한 셀의 유지율이 15,000 % 로 찍혔고, 그 한 줄 때문에 나머지
 *  27개가 바닥에 붙은 선 하나가 됐다.  그림이 아무것도 말하지 않게 된 것이다.
 *  (그런 값은 기준 사이클이 잘못 잡혔다는 뜻이다 — 그 자체가 봐야 할 신호지만,
 *  그것을 보려고 나머지를 못 보게 되면 안 된다.)
 *
 *  **다 200 % 아래면 손대지 않는다.**  자를 것이 없는데 위를 200 으로 못 박으면
 *  90~100 % 사이에서 갈리는 셀들이 아래쪽 절반에 눌린다 — 정작 읽어야 할 차이가
 *  거기 있다.  `null` 은 uPlot 에게 "네가 맞춰라" 는 뜻이다.
 *
 *  자를 때도 **잘랐다고 말한다** (§0.4).  말 없이 자르면 그 셀은 화면에서
 *  그냥 사라지고, 사라진 것은 아무 표시도 남기지 않는다.
 */
export const RETENTION_CEILING = 200

export function overlayRange(series: { y: number[]; hidden?: boolean }[]): {
  range: [number | null, number | null]
  clipped: boolean
} {
  const shown = series.filter((line) => !line.hidden)
  let top = 0
  for (const line of shown) {
    for (const value of line.y) {
      if (Number.isFinite(value) && value > top) top = value
    }
  }
  if (top <= RETENTION_CEILING) return { range: [null, null], clipped: false }
  return { range: [null, RETENTION_CEILING], clipped: true }
}

export function Dashboard() {
  const [basis, setBasis] = useStickyState<Basis>('workbench.basis', 'mAh/g')
  const [filter, setFilter] = useState<Filter>('all')
  const [hiddenSeries, setHiddenSeries] = useState<string[]>([])

  // 그룹으로 서버에서 거르지 않는다.  칩마다 개수를 보여주려면 전체가 필요하고,
  // 그룹을 누를 때마다 다시 받아오지 않아도 되므로 전환이 즉시 된다.
  const group = useGroupChoice()
  // **기본이 폴더다.**  예전에는 목록이 기본이었다 — 이 표의 기본 차례가
  // "방금 올린 것이 위로" 이고 폴더로 묶으면 그 차례가 폴더 안으로 들어가기
  // 때문이었다.  그런데 셀이 마흔을 넘으면서 그 차례보다 **어느 묶음이
  // 움직였나** 가 먼저 보고 싶은 것이 됐고, 폴더는 다 접혀 있으므로 첫 화면이
  // 곧 요약이다 (ADR 0035).  차례는 `목록` 한 번이면 돌아온다.
  const [folderView, setFolderView] = useStickyState('bml.dashboardFolders.v2', true)
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
  const everyCurve: PlotSeries[] = useMemo(
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
            // 어느 묶음의 곡선인지.  이름만으로는 네 곡선이 한 실험의 조건
            // 넷인지 서로 다른 실험 넷인지 알 수 없고, 그 둘은 같은 그림을
            // 전혀 다르게 읽게 한다.  이름에 이어 붙이지 않는 이유는
            // `PlotSeries.note` 에 적어 두었다.
            note: groupPath(row.group_name, row.group_parent_name) || undefined,
          }
        }),
    [rows, hiddenSeries],
  )

  //: **쉰 개를 겹치면 아무것도 안 보인다.**  실측: 51 곡선에 범례가 51 조각.
  //: 그림이 "무엇이 어떻게 늙는가" 대신 색 뭉치가 된다.
  //:
  //: 그래서 기본은 **최근 열 개**다.  차례는 표와 같은 것을 쓴다 (`rows` 가
  //: 이미 그 차례다) — 표에서 위에 있는 열 줄이 그림에도 있어야, 표를 보다
  //: 그림을 볼 때 눈이 다시 찾지 않는다.  "최근" 의 뜻도 거기서 온다:
  //: 시험일을 안 적은 것이 먼저(올린 때 최신순), 그다음이 시험일 최신순.
  //:
  //: **열 개 이하면 단추 자체가 없다.**  누를 것이 하나뿐인 단추는 화면만
  //: 차지하고, 그때는 이미 다 보이고 있다.
  const [allCurves, setAllCurves] = useStickyState('bml.dashboardAllCurves', false)
  const limited = !allCurves && everyCurve.length > OVERLAY_LIMIT
  const overlay = useMemo(
    () => (limited ? everyCurve.slice(0, OVERLAY_LIMIT) : everyCurve),
    [everyCurve, limited],
  )

  // 튄 곡선 하나가 나머지를 납작하게 만들지 않게 위를 잘라 준다.  범례에서
  // 끈 곡선은 안 센다 — 사람이 이미 안 보겠다고 한 것이 범위를 정하면 안 된다.
  //
  // **그리는 것만 센다.**  안 그린 곡선이 세로 범위를 정하면 그림이 제 곡선들
  // 위아래로 빈 칸을 크게 남긴다 -- 보이지 않는 것 때문에.
  const span = useMemo(() => overlayRange(overlay), [overlay])

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
          {/* 폴더는 **끄고 시작한다.**  이 표의 기본 차례는 "방금 올린 것이
              위로" 이고, 폴더로 묶으면 그 차례가 폴더 안으로 들어가 버린다 —
              들어와서 무엇이 새로 왔는지 보는 것이 이 화면의 첫 용도다.
              켜 두면 이 브라우저에 남는다 (ADR 0035). */}
          <div className="segmented" role="group" aria-label="보기">
            <button type="button" className={folderView ? '' : 'on'}
                    onClick={() => setFolderView(false)}>목록</button>
            <button type="button" className={folderView ? 'on' : ''}
                    onClick={() => setFolderView(true)}>폴더</button>
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
          <DashboardTable rows={rows} basis={basis} folders={folderView}
                          onDeleted={() => board.reload()} />
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

      {/* **한 개도 그린다.**  예전에는 둘 이상일 때만 그렸다 — "겹쳐보기" 니까
          겹칠 것이 있어야 한다는 생각이었는데, 그룹을 좁혀 한 셀만 남기는 것이
          이 화면에서 가장 흔한 동작이다.  그때 그림이 통째로 사라지면 화면은
          "이 그룹에는 볼 것이 없다" 로 읽히지만, 정작 그 한 셀의 열화 곡선이
          보고 싶어서 좁힌 것이다 (실측 2026-08-27: 이종기술 (1)).
          0 개일 때만 안 그린다 — 빈 그래프는 고장처럼 보인다. */}
      {overlay.length ? (
        <div style={{ marginTop: 12 }}>
          <Card
            title={overlay.length > 1 ? '용량 유지율 겹쳐보기' : '용량 유지율'}
            actions={
              <span className="row" style={{ gap: 10, alignItems: 'center' }}>
                {everyCurve.length > OVERLAY_LIMIT ? (
                  <div className="segmented" role="group" aria-label="그릴 곡선">
                    <button type="button" className={allCurves ? '' : 'on'}
                            onClick={() => setAllCurves(false)}>
                      최근 {OVERLAY_LIMIT}개
                    </button>
                    <button type="button" className={allCurves ? 'on' : ''}
                            onClick={() => setAllCurves(true)}>
                      전부 {everyCurve.length}개
                    </button>
                  </div>
                ) : null}
                <span className="tiny faint">
                  각 셀의 기준 사이클 대비 · 자세한 비교는{' '}
                  <Link to="/compare">비교 화면</Link>
                </span>
              </span>
            }
            tight
          >
            <Plot
              series={overlay}
              xLabel="사이클"
              yLabel="용량 유지율 (%)"
              height={260}
              yRange={span.range}
              markers={[{ x: 0, label: '' }].slice(0, 0)}
            />
            {/* **캡처만 보는 사람이 속으면 안 된다.**  단추는 화면에 있지만
                그림만 잘라 붙이면 "이 그룹에는 열 셀뿐" 으로 읽힌다 — 잘린
                그림에 잘렸다고 적는 것은 이 저장소가 이미 부분 사이클에서
                한 번 배운 것이다. */}
            {limited ? (
              <div className="tiny faint" style={{ padding: '0 var(--s4) var(--s3)' }}>
                {everyCurve.length}개 중 <strong>최근 {OVERLAY_LIMIT}개</strong>만
                그렸습니다 — 표의 위 열 줄과 같은 것입니다. 나머지는 위의{' '}
                <strong>전부</strong> 로.
              </div>
            ) : null}
            {span.clipped ? (
              <div className="tiny faint" style={{ padding: '0 var(--s4) var(--s3)' }}>
                {RETENTION_CEILING} % 위는 잘랐습니다 — 그 위로 튄 곡선 하나가
                나머지를 납작하게 만듭니다. 그런 값은 대개 기준 사이클이 잘못
                잡힌 것이니, 해당 셀을 열어 기준을 확인해 보세요.
              </div>
            ) : null}
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
  folders: folderView,
  onDeleted,
}: {
  rows: DashboardRow[]
  basis: Basis
  folders: boolean
  onDeleted: () => void
}) {
  // 폴더는 라이브러리와 **같은 기억**을 쓰지 않는다.  두 화면이 거르는 것이
  // 서로 달라서 (여기는 상태 탭, 저기는 날짜·양극재), 같은 기억을 나눠 쓰면
  // 한쪽에서 걸러진 셀이 다른 쪽에서 "지워졌다" 로 세어진다.
  const folders = useFolders('dashboard', rows, placeRow)
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
          </tr>
        </thead>
        {folderView ? folders.folders.filter(folders.isVisible).map((folder) => (
          <tbody key={folder.key}>
            <FolderRow folder={folder} view={folders} columns={COLUMN_COUNT} />
            {folders.isFolded(folder.key) ? null : folder.items.map(cellRow)}
          </tbody>
        )) : <tbody>{rows.map(cellRow)}</tbody>}
      </table>
      {deleteError ? (
        <div style={{ padding: '10px 14px 0' }}>
          <Alert kind="error">{deleteError}</Alert>
        </div>
      ) : null}
    </div>
  )

  function cellRow(row: DashboardRow) {
    return (
            <tr key={row.sample_id}>
              <td className="text">
                {/* 지우기를 **이름 앞**에 둔다.  꼬리 열이던 것을 없애면 표가
                    한 칸 좁아지고, 그만큼 가로 스크롤이 줄어든다 — 값을 보려고
                    옆으로 미는 것이 이 표들의 가장 큰 불편이었다.  붙박이
                    첫 열(`pin-first`) 안이라 옆으로 밀어도 늘 손이 닿는다. */}
                <DeleteSampleButton
                  sampleId={row.sample_id}
                  sampleName={row.sample_name}
                  onDeleted={onDeleted}
                  onError={setDeleteError}
                />
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
            </tr>
    )
  }
}

/** 대시보드 줄을 폴더 자리로 (ADR 0035).  라이브러리의 `placeSample` 과 짝이다. */
const placeRow = (row: DashboardRow) => ({
  id: row.sample_id,
  groupId: row.group_id,
  groupName: row.group_name ?? '',
  groupParentName: row.group_parent_name ?? '',
})

/** 폴더 줄이 표 전체 폭을 덮으려면 열 수가 맞아야 한다.  틀리면 그 줄만
 *  가로로 밀려 표가 어긋난다 — 셀·상태·보고 사이클·용량·유지율·추세·급감·
 *  초기 CE·기준·로딩·조건 = 11.  지우기는 이름 칸 안으로 들어갔다. */
const COLUMN_COUNT = 11

/** 겹쳐 그릴 곡선의 기본 상한.
 *
 *  열 개는 색으로 가를 수 있는 대략의 한계이자, 범례가 한두 줄에 들어가는 수다.
 *  실측 51개에서는 그림도 범례도 읽히지 않았다.
 */
const OVERLAY_LIMIT = 10
