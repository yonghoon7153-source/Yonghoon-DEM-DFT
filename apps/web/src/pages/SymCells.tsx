/** 대칭셀 — 전해질만 보는 측정의 목록 (ADR 0039).
 *
 *  블로킹 대칭셀(SS|전해질|SS)을 챔버에 넣고 온도를 내리며 PEIS 를 거는 측정
 *  이다.  한 `.mpt` 안에 스윕이 아홉 개 들어 있고, 나오는 것은 온도별
 *  이온전도도와 활성화에너지 하나다.
 *
 *  EIS 라이브러리에도 여전히 보인다 — 같은 측정이고 나이퀴스트는 나이퀴스트다.
 *  여기 따로 두는 것은 **묻는 것이 달라서**다.
 */

import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { DeleteMeasurementButton } from '../components/RelatedCell'
import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { CONDUCTIVITY_PURPOSE, isConductivityScan } from '../lib/conductivity'
import { useAsync, useStickyState } from '../lib/hooks'

export function SymCells() {
  const [search, setSearch] = useState('')
  const [rowError, setRowError] = useState<string | null>(null)
  //: 기본은 대칭셀만이다.  전부 보기를 눌러 두면 다음에 와도 그대로다 —
  //  목적을 안 적고 올린 파일을 찾으러 오는 자리가 여기라서.
  const [onlySym, setOnlySym] = useStickyState('bml.symOnly', true)
  const scans = useAsync(() => api.listScans(), [], { live: true })

  const rows = useMemo(() => {
    const all = (scans.data ?? []).filter(
      (scan) => !onlySym || isConductivityScan(scan))
    if (!search) return all
    const needle = search.toLowerCase()
    return all.filter((scan) =>
      scan.name.toLowerCase().includes(needle)
      || scan.original_name.toLowerCase().includes(needle)
      || (scan.sample_name ?? '').toLowerCase().includes(needle))
  }, [scans.data, search, onlySym])

  const hidden = (scans.data ?? []).length - (scans.data ?? []).filter(
    isConductivityScan).length

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>대칭셀 · 이온전도도</h1>
          <div className="sub">
            온도를 바꿔 가며 건 PEIS 한 파일에서 온도별 이온전도도와
            활성화에너지를 냅니다. 스캔을 열고 <b>온도</b>와 <b>두께·면적</b>을
            적으면 표가 섭니다.
          </div>
        </div>
      </div>

      <Card title="거르기" tight>
        <div className="row" style={{ padding: 14, gap: 14, flexWrap: 'wrap' }}>
          <Field label="보기">
            <div className="seg">
              <button type="button" className={onlySym ? 'on' : ''}
                      onClick={() => setOnlySym(true)}>대칭셀</button>
              <button type="button" className={onlySym ? '' : 'on'}
                      onClick={() => setOnlySym(false)}>전체 스캔</button>
            </div>
          </Field>
          <Field label="검색">
            <input value={search} onChange={(event) => setSearch(event.target.value)}
                   placeholder="이름 · 파일 · 셀" />
          </Field>
          {/* 무엇이 안 보이는지 적는다.  "왜 내 파일이 없지" 가 이 화면에서
              제일 먼저 나오는 질문이고, 답은 목적이나 셀 구성이다. */}
          {onlySym && hidden > 0 ? (
            <div className="tiny dim" style={{ alignSelf: 'flex-end', paddingBottom: 6 }}>
              대칭셀이 아닌 스캔 {hidden}개는 숨겨져 있습니다 — 목적을{' '}
              <code>{CONDUCTIVITY_PURPOSE}</code> 로 적거나 셀 구성을 대칭셀로
              두면 여기 나옵니다.
            </div>
          ) : null}
        </div>
      </Card>

      <Card title={`스캔 ${rows.length}개`} tight>
        {rowError ? <Alert kind="error">{rowError}</Alert> : null}
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
                  <th style={{ textAlign: 'left' }}>목적</th>
                  <th>스윕</th>
                  <th>fitting</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((scan) => (
                  <tr key={scan.sha256}>
                    <td className="text">
                      <DeleteMeasurementButton
                        name={scan.name}
                        note={`스윕 ${scan.sweeps}개 전부`}
                        onError={setRowError}
                        onDelete={async () => {
                          await api.deleteScan(scan.sha256)
                          scans.reload()
                        }}
                      />
                      <Link to={`/sym/${scan.sha256}`}>{scan.name}</Link>
                    </td>
                    <td className="text dim">
                      {scan.sample_id
                        ? <Link to={`/samples/${scan.sample_id}`}>{scan.sample_name}</Link>
                        : '—'}
                    </td>
                    <td className="text dim">{scan.purpose || '—'}</td>
                    <td>{scan.sweeps}</td>
                    <td className={scan.fitted ? '' : 'dim'}>
                      {scan.fitted} / {scan.sweeps}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <Empty title="대칭셀 스캔이 없습니다" icon="∿">
            <Link to="/eis/upload">업로드</Link>에서 <code>.mpt</code> 를 올리고
            목적을 <code>{CONDUCTIVITY_PURPOSE}</code>, 셀 구성을 <b>대칭셀</b> 로
            두면 여기 나타납니다.
          </Empty>
        )}
      </Card>
    </main>
  )
}
