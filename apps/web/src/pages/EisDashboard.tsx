/** EIS 대시보드 — 임피던스를 가진 셀이 한 줄씩.
 *
 *  충방전 대시보드와 같은 자리에 서는 화면이다: 셀 하나가 한 줄이고, 그 줄을
 *  보면 "몇 개 쟀고, 맞췄고, 저항이 얼마인가" 를 안다.  스펙트럼 목록은 이
 *  화면이 아니다 — 저쪽은 파일이 한 줄이고 여기는 셀이 한 줄이다.
 *
 *  맞춘 적이 없으면 저항 칸은 비어 있다.  0 이 아니다 (§0.4).
 */

import { Link } from 'react-router-dom'

import { Alert, Card, Empty, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { dateTime, num } from '../lib/format'
import { useAsync } from '../lib/hooks'

const CONFIG_LABEL: Record<string, string> = {
  full: '풀셀', half: '하프셀', sym: '대칭셀',
}

export function EisDashboard() {
  const board = useAsync(() => api.eisDashboard(), [], { live: true })
  const rows = board.data?.rows ?? []
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
      </div>

      {/* 붙이는 것은 일이고, 그 일이 남아 있다는 사실은 여기서만 보인다.
          0 이면 아무 말도 안 한다 — 할 일이 없다는 문장은 소음이다. */}
      {unattached ? (
        <Alert kind="info">
          셀에 안 붙은 스펙트럼이 {unattached}개 있습니다 —{' '}
          <Link to="/eis/library">라이브러리</Link>에서 셀을 정해 주면 이 표에
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
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={row.sample_id ?? row.sample_name}>
                    <td className="text">
                      <Link to={`/samples/${row.sample_id}`}>{row.sample_name}</Link>
                    </td>
                    <td className="text dim">{row.group_name || '—'}</td>
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
