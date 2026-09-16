/** 대칭셀 대시보드 — 전해질 한 파일이 한 줄씩 (ADR 0039).
 *
 *  EIS 대시보드와 **같은 모양**이다: 같은 자리의 `목록`/`폴더` 단추, 같은
 *  그룹 거르개, 같은 폴더 줄, 같은 행 꼬리표.  세 대시보드가 같은 손놀림이어야
 *  한다 — 여기만 다르면 익힌 손이 안 통한다 (ADR 0035).
 *
 *  다른 것은 **한 줄이 무엇이냐**다.  EIS 대시보드는 셀이 한 줄이지만 여기는
 *  파일이 한 줄이다: 대칭셀 측정은 셀 하나에 파일 하나이고, 묻는 것이 "이
 *  전해질의 활성화에너지" 라 파일이 곧 답의 단위다.
 */

import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { FolderRow, useFolders } from '../components/FolderTree'
import { GroupFilterFields, useGroupChoice } from '../components/GroupFilter'
import { DeleteMeasurementButton } from '../components/RelatedCell'
import { GroupTag, OwnerTag } from '../components/RowTags'
import { Alert, Card, Empty, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { CONDUCTIVITY_PURPOSE } from '../lib/conductivity'
import { dateTime, num } from '../lib/format'
import { useAsync, useStickyState } from '../lib/hooks'
import type { SymDashboardRow } from '../lib/types'

/** 이름·관계셀·스윕·온도·두께·σ(최고온도)·Ea·R²·올린 때·지우기 = 10. */
const COLUMN_COUNT = 10

export function SymDashboard() {
  const board = useAsync(() => api.symDashboard(), [], { live: true })
  const group = useGroupChoice()
  const [deleteError, setDeleteError] = useState<string | null>(null)
  const inGroup = group.includes

  const rows = useMemo(
    () => (board.data?.rows ?? []).filter((row) => inGroup(row.group_id)),
    [board.data, inGroup])
  const others = board.data?.other_scans ?? 0

  // EIS·충방전 대시보드와 같은 기본 (ADR 0035): 폴더로 시작하고, `목록` 한
  // 번이면 올린 차례로 돌아온다.  기억은 화면마다 따로 둔다.
  const [folderView, setFolderView] = useStickyState('bml.symDashboardFolders', true)
  const folders = useFolders('symDashboard', rows, placeRow)

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>대칭셀 대시보드</h1>
          <div className="sub">
            전해질 한 파일이 한 줄씩 — 온도를 몇 개 적었고, 이온전도도가
            얼마고, 활성화에너지가 얼마인가
          </div>
        </div>
        <span className="spacer" />
        <div className="segmented" role="group" aria-label="보기">
          <button type="button" className={folderView ? '' : 'on'}
                  onClick={() => setFolderView(false)}>목록</button>
          <button type="button" className={folderView ? 'on' : ''}
                  onClick={() => setFolderView(true)}>폴더</button>
        </div>
        <GroupFilterFields pick={group} compact />
      </div>

      {/* 0 이면 아무 말도 안 한다 — 할 일이 없다는 문장은 소음이다. */}
      {others ? (
        <Alert kind="info">
          대칭셀로 보이지 않는 스캔이 {others}개 있습니다 — 목적을{' '}
          <code>{CONDUCTIVITY_PURPOSE} 스윕</code> 으로 적거나 셀 구성을
          대칭셀로 두면 여기 나옵니다 (
          <Link to="/sym/library">라이브러리</Link>).
        </Alert>
      ) : null}

      {deleteError ? <Alert kind="error">{deleteError}</Alert> : null}

      <Card title={`전해질 ${rows.length}개`} tight>
        {board.error ? (
          <Alert kind="error">{board.error}</Alert>
        ) : board.loading && !board.data ? (
          <div style={{ padding: 20 }}><Spinner /></div>
        ) : rows.length ? (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left' }}>이름</th>
                  <th style={{ textAlign: 'left' }}>관계셀</th>
                  <th>스윕</th>
                  <th style={{ textAlign: 'left' }}>온도</th>
                  <th>두께 (mm)</th>
                  <th>σ (mS cm⁻¹)</th>
                  <th>Ea (eV)</th>
                  <th>R²</th>
                  <th>올린 때</th>
                  <th />
                </tr>
              </thead>
              {folderView ? (
                folders.folders.filter(folders.isVisible).map((folder) => (
                  <tbody key={folder.key}>
                    <FolderRow folder={folder} view={folders} columns={COLUMN_COUNT} />
                    {folders.isFolded(folder.key) ? null : folder.items.map(row)}
                  </tbody>
                ))
              ) : (
                <tbody>{rows.map(row)}</tbody>
              )}
            </table>
          </div>
        ) : (
          <Empty title="대칭셀 측정이 없습니다" icon="∿">
            <Link to="/eis/upload">업로드</Link>에서 온도별 PEIS 가 담긴{' '}
            <code>.mpt</code> 를 올리고 목적을{' '}
            <code>{CONDUCTIVITY_PURPOSE} 스윕</code>, 셀 구성을 <b>대칭셀</b> 로
            두면 여기 나타납니다.
          </Empty>
        )}
      </Card>
    </main>
  )

  function row(item: SymDashboardRow) {
    return (
      <tr key={item.sha256}>
        <td className="text">
          <GroupTag name={item.group_name} path={groupPath(item)} />
          <OwnerTag owner={item.owner} />
          <Link to={`/sym/scan/${item.sha256}`}>{item.name}</Link>
          {' '}
          <span className="tiny dim">[스윕 {item.sweeps}개]</span>
        </td>
        <td className="text dim">
          {item.sample_id
            ? <Link to={`/samples/${item.sample_id}`}>{item.sample_name}</Link>
            : '셀 안 붙음'}
        </td>
        <td className={item.fitted ? '' : 'dim'}>
          {item.fitted} / {item.sweeps}
        </td>
        {/* 온도는 사람이 적는다.  몇 개 적었는지가 곧 다음에 할 일이다. */}
        <td className="text dim tiny">{temperatureCell(item)}</td>
        <td className={item.thickness_mm === null ? 'dim' : ''}>
          {item.thickness_mm === null ? '—' : num(item.thickness_mm, 3)}
        </td>
        {/* 가장 **높은** 온도의 σ — 어느 온도의 수인지 함께 적는다.  안 적으면
            파일마다 다른 온도의 값이 한 열에 서고, 그 열은 견줄 수 없다. */}
        <td className={item.sigma_top_ms_cm === null ? 'dim' : ''}>
          {item.sigma_top_ms_cm === null ? '—' : (
            <>
              {num(item.sigma_top_ms_cm, 3)}
              {item.temperature_high_c !== null ? (
                <div className="faint tiny">{item.temperature_high_c}°C</div>
              ) : null}
            </>
          )}
        </td>
        <td className={item.activation_energy_ev === null ? 'dim' : ''}
            title={item.reason || undefined}>
          {item.activation_energy_ev === null
            ? '—'
            : item.activation_energy_ev.toFixed(3)}
        </td>
        <td className={item.r_squared === null ? 'dim' : ''}>
          {item.r_squared === null
            ? '—' : String(Number(item.r_squared.toPrecision(6)))}
        </td>
        <td className="dim">{dateTime(item.uploaded_at)}</td>
        <td>
          <DeleteMeasurementButton
            name={item.name}
            note={`스윕 ${item.sweeps}개 전부`}
            onError={setDeleteError}
            onDelete={async () => {
              await api.deleteScan(item.sha256)
              board.reload()
            }}
          />
        </td>
      </tr>
    )
  }
}

/** 온도 칸 — 범위와, 아직 안 적은 스윕이 있으면 그 수.
 *
 *  다 적혔을 때만 범위만 적는다.  아홉 중 셋만 적힌 파일에 `60 ~ 40 °C` 만
 *  적으면 다 적은 파일과 구분되지 않는다.
 */
function temperatureCell(item: SymDashboardRow): string {
  if (!item.temperatures_written) return '아직 없음'
  const high = item.temperature_high_c
  const low = item.temperature_low_c
  const span = high === low ? `${high} °C` : `${high} ~ ${low} °C`
  return item.temperatures_written === item.sweeps
    ? span : `${span} (${item.temperatures_written}/${item.sweeps})`
}

function groupPath(item: SymDashboardRow): string {
  return item.group_parent_name
    ? `${item.group_parent_name} · ${item.group_name}` : item.group_name
}

/** 이 줄을 폴더 자리로 (ADR 0035) — EIS 대시보드의 `placeEisRow` 와 짝이다. */
const placeRow = (item: SymDashboardRow) => ({
  id: item.sha256,
  groupId: item.group_id,
  groupName: item.group_name,
  groupParentName: item.group_parent_name,
})
