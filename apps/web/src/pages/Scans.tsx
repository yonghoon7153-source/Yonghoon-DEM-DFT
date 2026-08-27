/** SOC 스캔 — 파일 하나가 스펙트럼 스물인 측정 (ADR 0022).
 *
 *  EIS 목록과 나누는 이유는 셈이 다르기 때문이다.  스펙트럼 목록은 "이 셀의
 *  임피던스를 언제 쟀나" 를 셀 단위로 보여 주는데, SOC 스캔을 거기 풀어 놓으면
 *  한 파일이 스무 줄이 되어 다른 셀들이 화면에서 밀려난다.  여기서는 파일
 *  하나가 한 줄이고, 그 줄을 열면 SOC 가 x축인 그래프 하나가 나온다.
 */

import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { useAsync } from '../lib/hooks'

const CONFIG_LABEL: Record<string, string> = {
  full: '풀셀', half: '하프셀', sym: '대칭셀',
}

export function Scans() {
  const [search, setSearch] = useState('')
  const scans = useAsync(() => api.listScans(), [], { live: true })

  const rows = useMemo(() => {
    const all = scans.data ?? []
    if (!search) return all
    const needle = search.toLowerCase()
    return all.filter((scan) =>
      scan.name.toLowerCase().includes(needle)
      || scan.original_name.toLowerCase().includes(needle)
      || (scan.sample_name ?? '').toLowerCase().includes(needle))
  }, [scans.data, search])

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>SOC 스캔</h1>
          <div className="sub">
            한 파일에 임피던스 스윕이 여럿인 측정 — SOC 를 x축으로 저항이
            어떻게 움직이는지 봅니다
          </div>
        </div>
      </div>

      <Card
        title={`스캔 ${rows.length}개`}
        actions={
          <Field label="검색">
            <input
              aria-label="검색"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="이름 · 파일명 · 셀"
            />
          </Field>
        }
        tight
      >
        {scans.error ? (
          <Alert kind="error">{scans.error}</Alert>
        ) : scans.loading && !scans.data ? (
          <div style={{ padding: 20 }}><Spinner /></div>
        ) : rows.length ? (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left' }}>이름</th>
                  <th style={{ textAlign: 'left' }}>관계셀</th>
                  <th style={{ textAlign: 'left' }}>측정</th>
                  <th style={{ textAlign: 'left' }}>목적</th>
                  <th>스윕</th>
                  <th>fitting</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((scan) => (
                  <tr key={scan.sha256}>
                    <td className="text">
                      <Link to={`/scans/${scan.sha256}`}>{scan.name}</Link>
                    </td>
                    <td className="text dim">
                      {scan.sample_id
                        ? <Link to={`/samples/${scan.sample_id}`}>{scan.sample_name}</Link>
                        : '—'}
                    </td>
                    <td className="text dim">
                      {scan.kind === 'solid' ? '전고체' : '액체'}
                      {scan.cell_config
                        ? ` · ${CONFIG_LABEL[scan.cell_config] ?? scan.cell_config}`
                        : ''}
                    </td>
                    <td className="text dim">{scan.purpose || '—'}</td>
                    <td>{scan.sweeps}</td>
                    {/* 몇 개를 맞췄는지가 곧 다음에 할 일이다 — 0 이면 그래프가
                        비어 있는 이유가 여기 적혀 있다. */}
                    <td className={scan.fitted ? '' : 'dim'}>
                      {scan.fitted} / {scan.sweeps}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <Empty title="스캔이 없습니다" icon="∿">
            임피던스 스윕이 <b>셋 이상</b> 들어 있는 <code>.mpr</code> 을
            EIS 화면에서 올리면 여기 나타납니다. 두 장짜리 전·후 측정은
            스캔이 아니라 EIS 목록에서 나란히 봅니다.
          </Empty>
        )}
      </Card>
    </main>
  )
}
