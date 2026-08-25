/** GITT 대시보드 — GITT 를 가진 셀이 한 줄씩.
 *
 *  이 섹션의 답은 확산계수다.  그래서 한 줄의 요점도 그것이다: **낼 수 있는가,
 *  없다면 무엇이 없어서인가.**  재료 상수는 파일에 없고 사람이 넣어야 하므로
 *  (ADR 0020), "무엇이 없다" 가 곧 다음에 할 일이다.
 *
 *  D 는 범위로 보여 준다.  SOC 를 따라 자릿수로 움직이는 값이라 평균을 내면
 *  그 숫자가 아무 SOC 도 뜻하지 않는다.
 */

import { Link } from 'react-router-dom'

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
  const rows = board.data?.rows ?? []
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
      </div>

      {unattached ? (
        <Alert kind="info">
          셀에 안 붙은 GITT 기록이 {unattached}개 있습니다 —{' '}
          <Link to="/gitt/library">라이브러리</Link>에서 셀을 정해 주면 이 표에
          들어옵니다.
        </Alert>
      ) : null}

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
                  <th style={{ textAlign: 'left' }}>셀</th>
                  <th style={{ textAlign: 'left' }}>그룹</th>
                  <th>기록</th>
                  <th>펄스</th>
                  <th>계산 가능</th>
                  <th style={{ textAlign: 'left' }}>D (cm²/s)</th>
                  <th style={{ textAlign: 'left' }}>없는 것</th>
                  <th>마지막</th>
                  <th style={{ textAlign: 'left' }}>작성자</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={row.sample_id ?? row.sample_name}>
                    <td className="text">
                      <Link to={`/samples/${row.sample_id}`}>{row.sample_name}</Link>
                    </td>
                    <td className="text dim">{row.group_name || '—'}</td>
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
                    <td className="dim">{dateTime(row.measured_at)}</td>
                    <td className="text dim">{row.owner || '—'}</td>
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
