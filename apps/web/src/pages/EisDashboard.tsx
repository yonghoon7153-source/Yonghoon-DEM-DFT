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
import { GroupFilterFields, groupPath, useGroupChoice } from '../components/GroupFilter'
import { DeleteMeasurementButton } from '../components/RelatedCell'
import { Alert, Card, Empty, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { dateTime, num } from '../lib/format'
import { useAsync } from '../lib/hooks'

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
                  {/* 이름 다음이 그룹이다.  표를 훑는 눈이 먼저 찾는 것은
                      "무엇을 잰 파일인가" 와 "어느 묶음인가" 이고, 관계셀은
                      그 다음이다 -- 셀 라이브러리와 같은 순서로 맞췄다. */}
                  <th style={{ textAlign: 'left' }}>이름</th>
                  <th style={{ textAlign: 'left' }}>그룹</th>
                  <th style={{ textAlign: 'left' }}>관계셀</th>
                  <th style={{ textAlign: 'left' }}>측정</th>
                  <th>스펙트럼</th>
                  <th>SOC 스캔</th>
                  <th>피팅</th>
                  <th style={{ textAlign: 'left' }}>회로</th>
                  <th>R₀ (Ω)</th>
                  <th>총저항 (Ω)</th>
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
                      {row.spectrum_id
                        ? <Link to={`/eis/${row.spectrum_id}`}>{row.name}</Link>
                        : (row.name || '—')}
                    </td>
                    <td className="text dim">
                      {groupPath(row.group_name, row.group_parent_name) || '—'}
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
                    <td className={row.scans ? '' : 'dim'}>{row.scans || '—'}</td>
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
                ))}
              </tbody>
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
}
