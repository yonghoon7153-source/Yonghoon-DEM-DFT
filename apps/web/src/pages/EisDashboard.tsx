/** EIS 대시보드 — 임피던스를 가진 셀이 한 줄씩.
 *
 *  충방전 대시보드와 같은 자리에 서는 화면이다: 셀 하나가 한 줄이고, 그 줄을
 *  보면 "몇 개 쟀고, 맞췄고, 저항이 얼마인가" 를 안다.  스펙트럼 목록은 이
 *  화면이 아니다 — 저쪽은 파일이 한 줄이고 여기는 셀이 한 줄이다.
 *
 *  맞춘 적이 없으면 저항 칸은 비어 있다.  0 이 아니다 (§0.4).
 */

import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { DeleteSampleButton } from '../components/DeleteSample'
import { FolderRow, useFolders } from '../components/FolderTree'
import { GroupFilterFields, groupPath, useGroupChoice } from '../components/GroupFilter'
import { GroupTag, OwnerTag } from '../components/RowTags'
import { DeleteMeasurementButton } from '../components/RelatedCell'
import { Alert, Card, Empty, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { dateTime, num } from '../lib/format'
import { useAsync, useStickyState } from '../lib/hooks'
import type { EisDashboardRow } from '../lib/types'

const CONFIG_LABEL: Record<string, string> = {
  full: '풀셀', half: '하프셀', sym: '대칭셀',
}

export function EisDashboard() {
  const board = useAsync(() => api.eisDashboard(), [], { live: true })
  const group = useGroupChoice()
  // 지우기 실패는 표 바깥에 한 번만 그린다 -- 행 안에 끼우면 열이 밀린다.
  const [deleteError, setDeleteError] = useState<string | null>(null)
  const inGroup = group.includes
  const rows = useMemo(
    () => (board.data?.rows ?? []).filter((row) => inGroup(row.group_id)),
    [board.data, inGroup])
  const unattached = board.data?.unattached ?? 0
  // 충방전 대시보드와 **같은 기본, 같은 손놀림** (ADR 0035): 폴더로 시작하고,
  // `목록` 한 번이면 올린 차례로 돌아온다.  기억은 화면마다 따로 둔다 -- 세
  // 대시보드가 거르는 것이 서로 달라서 (여기는 임피던스를 가진 셀만), 같은
  // 기억을 나눠 쓰면 한쪽에서 걸러진 셀이 다른 쪽에서 '지워졌다' 로 세어진다.
  const [folderView, setFolderView] = useStickyState('bml.eisDashboardFolders', true)
  const folders = useFolders('eisDashboard', rows, placeEisRow)

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>EIS 대시보드</h1>
          <div className="sub">
            임피던스를 가진 셀이 한 줄씩 — 몇 개 쟀고, 맞췄고, 저항이 얼마인가
          </div>
        </div>
        <span className="spacer" />
        {/* 충방전 대시보드와 같은 자리, 같은 낱말 (ADR 0035).  세 대시보드가
            같은 손놀림이어야 한다 — 여기만 다른 이름이면 익힌 손이 안 통한다. */}
        <div className="segmented" role="group" aria-label="보기">
          <button type="button" className={folderView ? '' : 'on'}
                  onClick={() => setFolderView(false)}>목록</button>
          <button type="button" className={folderView ? 'on' : ''}
                  onClick={() => setFolderView(true)}>폴더</button>
        </div>
        <GroupFilterFields pick={group} compact />
      </div>

      {/* 붙이는 것은 일이고, 그 일이 남아 있다는 사실은 여기서만 보인다.
          0 이면 아무 말도 안 한다 — 할 일이 없다는 문장은 소음이다. */}
      {unattached ? (
        <Alert kind="info">
          셀에 안 붙은 스펙트럼이 {unattached}개 있습니다 —{' '}
          <Link to="/eis/library">라이브러리</Link>에서 셀을 정해 주면 그 셀의
          줄로 합쳐집니다 — 그전까지는 아래에 이름만으로 나옵니다.
        </Alert>
      ) : null}

      {deleteError ? <Alert kind="error">{deleteError}</Alert> : null}

      <Card title={`셀 ${rows.length}개`} tight>
        {board.error ? (
          <Alert kind="error">{board.error}</Alert>
        ) : board.loading && !board.data ? (
          <div style={{ padding: 20 }}><Spinner /></div>
        ) : rows.length ? (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  {/* 그룹·작성자는 이름 칸 안의 이름표다 (아래를 보라). */}
                  <th style={{ textAlign: 'left' }}>이름</th>
                  <th style={{ textAlign: 'left' }}>관계셀</th>
                  <th style={{ textAlign: 'left' }}>측정</th>
                  <th>스펙트럼</th>
                  <th>SOC 스캔</th>
                  <th>fitting</th>
                  <th style={{ textAlign: 'left' }}>회로</th>
                  <th>R₀ (Ω)</th>
                  <th>총저항 (Ω)</th>
                  <th style={{ textAlign: 'left' }}>목적</th>
                  <th>마지막</th>
                  {/* 이름 없는 칸.  머리에 '삭제' 라고 적으면 표를 훑을 때 그
                      글자가 먼저 읽힌다 -- 셀 라이브러리와 같은 규칙이다. */}
                  <th />
                </tr>
              </thead>
              {folderView
                ? folders.folders.filter(folders.isVisible).map((folder) => (
                  <tbody key={folder.key}>
                    <FolderRow folder={folder} view={folders} columns={COLUMN_COUNT} />
                    {folders.isFolded(folder.key) ? null : folder.items.map(eisRow)}
                  </tbody>
                ))
                : <tbody>{rows.map(eisRow)}</tbody>}
            </table>
          </div>
        ) : (
          <Empty title="셀에 붙은 임피던스가 없습니다" icon="∿">
            <Link to="/eis/upload">업로드</Link>에서 파일을 올리면서 셀을 고르면
            여기 나타납니다.
          </Empty>
        )}
      </Card>
    </main>
  )

  function eisRow(row: EisDashboardRow) {
    return (
                  <tr key={row.attached ? `s${row.sample_id}` : `f${row.name}`}
                      className={row.attached ? undefined : 'dim'}>
                    <td className="text">
                      {/* 그룹과 작성자를 이름 앞에 이름표로 — 충방전 대시보드와
                          같은 모양이다.  열로 따로 두면 이름과 "누구의 어느
                          묶음인가" 가 표 폭만큼 떨어져, 한 줄을 읽는 데 눈이
                          세 번 움직인다. */}
                      <GroupTag name={row.group_name}
                                path={groupPath(row.group_name, row.group_parent_name)} />
                      <OwnerTag owner={row.owner} />
                      {/* 이름이 곧 그 측정으로 가는 길이다 -- 셀 이름만으로는
                          어느 측정인지 모른다 (파일 이름에 조건이 적혀 있다). */}
                      {/* 스캔이면 **1번 스윕**으로 간다 (서버가 그것을 골라
                          보낸다).  거기가 조건을 적어 넣는 자리이고, 적은 것이
                          스윕 전부에 퍼진다.  겹쳐 보는 화면은 그 페이지 머리의
                          `스캔 · 스윕 N개` 로 한 번 더 가면 되고, 아래 `SOC
                          스캔` 칸도 같은 곳으로 간다. */}
                      {row.spectrum_id
                        ? <Link to={`/eis/${row.spectrum_id}`}>{row.name}</Link>
                        : (row.name || '—')}
                    </td>
                    <td className="text">
                      {/* 셀 칸이 비어 있다는 것 자체가 이 줄의 정보다: 아직
                          붙일 일이 남아 있다는 뜻이고, 그 일은 라이브러리에서
                          한다 (§0.4 — 없는 소속을 지어내지 않는다). */}
                      {row.attached
                        ? <Link to={`/samples/${row.sample_id}`}>{row.sample_name}</Link>
                        : <Link className="tiny" to="/eis/library">셀 안 붙음</Link>}
                    </td>
                    <td className="text dim">
                      {/* 한 셀에 액체와 전고체가 섞여 있으면 서버가 종류를
                          비워 보낸다.  둘을 한 줄로 요약하면 그 줄이 거짓말을
                          한다 (ADR 0019) — 여기서도 지어내지 않는다. */}
                      {row.kind ? (row.kind === 'solid' ? '전고체' : '액체') : '섞임'}
                      {row.cell_config
                        ? ` · ${CONFIG_LABEL[row.cell_config] ?? row.cell_config}`
                        : ''}
                    </td>
                    <td>{row.spectra}</td>
                    {/* 스윕을 한 그림에 겹쳐 보는 자리로 가는 길.  이름은
                        1번 스윕(조건을 적는 자리)으로 가므로, 겹쳐보기는
                        이 칸이 맡는다. */}
                    <td className={row.scans ? '' : 'dim'}>
                      {row.scans && row.scan_sha256
                        ? <Link to={`/scans/${row.scan_sha256}`}>{row.scans}</Link>
                        : (row.scans || '—')}
                    </td>
                    <td className={row.fitted ? '' : 'dim'}>
                      {row.fitted} / {row.spectra}
                    </td>
                    <td className="text dim tiny">{row.last_circuit || '—'}</td>
                    <td className={row.series_resistance_ohm === null ? 'dim' : ''}>
                      {row.series_resistance_ohm === null
                        ? '—' : num(row.series_resistance_ohm, 4)}
                    </td>
                    <td className={row.total_resistance_ohm === null ? 'dim' : ''}>
                      {row.total_resistance_ohm === null
                        ? '—' : num(row.total_resistance_ohm, 4)}
                    </td>
                    <td className="text dim">{row.purposes.join(', ') || '—'}</td>
                    <td className="dim">{dateTime(row.measured_at)}</td>
                    <td>
                      {/* 셀을 기록에서 내린다.  원본 파일은 남는다 (불변 규칙 2) --
                          같은 바이트를 다시 올리면 sha256 이 같아 되살아난다. */}
                      {/* 붙은 줄은 셀을 지우고 (그 셀의 측정이 다 딸려
                          간다), 안 붙은 줄은 그 측정 하나를 지운다.  줄이
                          가리키는 것이 다르므로 지우는 것도 다르다. */}
                      {row.attached && row.sample_id !== null ? (
                        <DeleteSampleButton
                          sampleId={row.sample_id}
                          sampleName={row.sample_name}
                          onDeleted={() => board.reload()}
                          onError={setDeleteError}
                        />
                      ) : row.spectrum_id ? (
                        <DeleteMeasurementButton
                          name={row.name}
                          onError={setDeleteError}
                          onDelete={async () => {
                            await api.deleteSpectrum(row.spectrum_id as number)
                            board.reload()
                          }}
                        />
                      ) : null}
                    </td>
                  </tr>
    )
  }
}

/** EIS 대시보드 줄을 폴더 자리로 (ADR 0035).  충방전의 `placeRow` 와 짝이다.
 *
 *  **아직 셀에 안 붙은 줄도 폴더에 들어간다.**  그 줄은 `sample_id` 가 없어서
 *  열쇠를 파일 이름으로 만든다 -- 전부 `null` 로 두면 서로 구별이 안 되어
 *  "하나 들어오고 하나 나갔다" 가 0 으로 보인다.  그런 줄은 그룹도 없으므로
 *  `그룹 없음` 폴더로 모이는데, 그 자리가 맞다: 붙이는 것이 남은 일이고
 *  (화면 위의 안내가 그 말이다) 한군데 모여 있어야 그 일이 보인다.
 */
const placeEisRow = (row: EisDashboardRow) => ({
  id: row.attached && row.sample_id !== null ? row.sample_id : `f:${row.name}`,
  groupId: row.group_id,
  groupName: row.group_name ?? '',
  groupParentName: row.group_parent_name ?? '',
})

/** 폴더 줄이 표 전체 폭을 덮으려면 열 수가 맞아야 한다.  틀리면 그 줄만
 *  가로로 밀려 표가 어긋난다 — 이름·관계셀·측정·스펙트럼·SOC 스캔·fitting·
 *  회로·R₀·총저항·목적·마지막·(지우기) = 12. */
const COLUMN_COUNT = 12
