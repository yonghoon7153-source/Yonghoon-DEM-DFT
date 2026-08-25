/** GITT 대시보드 — GITT 를 가진 셀이 한 줄씩.
 *
 *  이 섹션의 답은 확산계수다.  그래서 한 줄의 요점도 그것이다: **낼 수 있는가,
 *  없다면 무엇이 없어서인가.**  재료 상수는 파일에 없고 사람이 넣어야 하므로
 *  (ADR 0020), "무엇이 없다" 가 곧 다음에 할 일이다.
 *
 *  D 는 범위로 보여 준다.  SOC 를 따라 자릿수로 움직이는 값이라 평균을 내면
 *  그 숫자가 아무 SOC 도 뜻하지 않는다.
 */

import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { DeleteSampleButton } from '../components/DeleteSample'
import { GroupFilterFields, groupPath, useGroupChoice } from '../components/GroupFilter'
import { DeleteMeasurementButton } from '../components/RelatedCell'
import { Alert, Card, Empty, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { dateTime } from '../lib/format'
import { useAsync } from '../lib/hooks'

/** `3.2e-11`.  D 는 지수로 읽는 값이라 고정 소수점으로 쓰면 0 만 보인다. */
function scientific(value: number | null): string {
  if (value === null || !Number.isFinite(value)) return '—'
  return value.toExponential(2)
}

export function GittDashboard() {
  const board = useAsync(() => api.gittDashboard(), [], { live: true })
  const group = useGroupChoice()
  // 지우기 실패는 표 바깥에 한 번만 그린다 -- 행 안에 끼우면 열이 밀린다.
  const [deleteError, setDeleteError] = useState<string | null>(null)
  const inGroup = group.includes
  const rows = useMemo(
    () => (board.data?.rows ?? []).filter((row) => inGroup(row.group_id)),
    [board.data, inGroup])
  const unattached = board.data?.unattached ?? 0

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>GITT 대시보드</h1>
          <div className="sub">
            GITT 를 가진 셀이 한 줄씩 — 확산계수를 낼 수 있는지, 없다면 무엇이
            없어서인지
          </div>
        </div>
        <span className="spacer" />
        <GroupFilterFields pick={group} compact />
      </div>

      {unattached ? (
        <Alert kind="info">
          셀에 안 붙은 GITT 기록이 {unattached}개 있습니다 —{' '}
          <Link to="/gitt/library">라이브러리</Link>에서 셀을 정해 주면 그 셀의
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
                  {/* 이름 다음이 그룹이다 — EIS 대시보드·셀 라이브러리와
                      같은 순서.  관계셀은 그 다음이다. */}
                  <th style={{ textAlign: 'left' }}>이름</th>
                  <th style={{ textAlign: 'left' }}>그룹</th>
                  <th style={{ textAlign: 'left' }}>관계셀</th>
                  <th>기록</th>
                  <th>펄스</th>
                  <th>계산 가능</th>
                  <th style={{ textAlign: 'left' }}>D (cm²/s)</th>
                  <th style={{ textAlign: 'left' }}>없는 것</th>
                  <th style={{ textAlign: 'left' }}>목적</th>
                  <th>마지막</th>
                  <th style={{ textAlign: 'left' }}>작성자</th>
                  {/* 이름 없는 칸.  머리에 '삭제' 라고 적으면 표를 훑을 때 그
                      글자가 먼저 읽힌다 -- 셀 라이브러리와 같은 규칙이다. */}
                  <th />
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={row.attached ? `s${row.sample_id}` : `f${row.name}`}
                      className={row.attached ? undefined : 'dim'}>
                    <td className="text">
                      {/* 이름이 곧 그 측정으로 가는 길이다 -- 셀 이름만으로는
                          어느 측정인지 모른다 (파일 이름에 조건이 적혀 있다). */}
                      {row.gitt_id
                        ? <Link to={`/gitt/${row.gitt_id}`}>{row.name}</Link>
                        : (row.name || '—')}
                    </td>
                    <td className="text dim">
                      {groupPath(row.group_name, row.group_parent_name) || '—'}
                    </td>
                    <td className="text">
                      {row.attached
                        ? <Link to={`/samples/${row.sample_id}`}>{row.sample_name}</Link>
                        : <Link className="tiny" to="/gitt/library">셀 안 붙음</Link>}
                    </td>
                    <td>{row.records}</td>
                    <td>{row.pulses}</td>
                    <td className={row.ready ? '' : 'dim'}>
                      {row.ready} / {row.records}
                    </td>
                    <td className={row.diffusion_low === null ? 'dim' : 'mono'}>
                      {/* 범위다.  하나뿐이면 둘이 같으므로 한 번만 쓴다. */}
                      {row.diffusion_low === null
                        ? '—'
                        : row.diffusion_low === row.diffusion_high
                          ? scientific(row.diffusion_low)
                          : `${scientific(row.diffusion_low)} – ${scientific(row.diffusion_high)}`}
                    </td>
                    <td className="text dim">
                      {/* 이 셀에서 다음에 할 일이 곧 이 칸이다. */}
                      {row.missing.length ? row.missing.join(', ') : '—'}
                    </td>
                    <td className="text dim">{row.purposes.join(', ') || '—'}</td>
                    <td className="dim">{dateTime(row.measured_at)}</td>
                    <td className="text dim">{row.owner || '—'}</td>
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
                      ) : row.gitt_id ? (
                        <DeleteMeasurementButton
                          name={row.name}
                          onError={setDeleteError}
                          onDelete={async () => {
                            await api.deleteGittRun(row.gitt_id as number)
                            board.reload()
                          }}
                        />
                      ) : null}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <Empty title="셀에 붙은 GITT 가 없습니다" icon="↯">
            <Link to="/gitt/upload">업로드</Link>에서 <code>.wrd</code> 를 올리면서
            셀을 고르면 여기 나타납니다.
          </Empty>
        )}
      </Card>
    </main>
  )
}
