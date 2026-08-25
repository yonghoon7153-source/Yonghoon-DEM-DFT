/** EIS 라이브러리 — 잰 것이 한 줄씩.
 *
 *  대시보드는 **셀**이 한 줄이고 여기는 **측정**이 한 줄이다.  둘 다 필요하다:
 *  "이 셀 임피던스가 어떻게 되지" 와 "그 스윕 어디 있지" 는 다른 질문이다.
 *
 *  SOC 스캔이 따로 있던 화면을 여기로 접었다.  같은 `.mpr` 이고 같은 회로로
 *  맞추므로 화면을 가를 이유가 없고, 다른 것은 파일 하나가 스윕 하나냐
 *  스물이냐 뿐이라 **거르개 하나**면 된다 (ADR 0022).
 */

import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { GroupFilterFields, useGroupChoice } from '../components/GroupFilter'
import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { dateTime, num } from '../lib/format'
import { useAsync } from '../lib/hooks'
import type { EisKind, Spectrum } from '../lib/types'
import { frequencySpan } from './Eis'

type Shape = 'all' | 'single' | 'scan'

const SHAPES: [Shape, string][] = [
  ['all', '전체'],
  ['single', '단일 스펙트럼'],
  ['scan', 'SOC 스캔'],
]

const KINDS: [EisKind | '', string][] = [
  ['', '전체'],
  ['liquid', '액체'],
  ['solid', '전고체'],
]

const CONFIG_LABEL: Record<string, string> = {
  full: '풀셀', half: '하프셀', sym: '대칭셀',
}

/** 이 줄이 스캔의 일부인가.  파일이 말하는 것이지 사람이 붙인 꼬리표가 아니다. */
const isScan = (item: Spectrum) => (item.sweep_count ?? 1) > 1

export function EisLibrary() {
  const [shape, setShape] = useState<Shape>('all')
  const [kind, setKind] = useState<EisKind | ''>('')
  const [purpose, setPurpose] = useState('')
  const [search, setSearch] = useState('')

  const spectra = useAsync(
    () => api.listSpectra({ kind: kind || undefined }), [kind], { live: true })
  const group = useGroupChoice()
  // 그룹은 셀의 성질이라 셀 표가 있어야 거를 수 있다 (비교 화면과 같다).
  const samples = useAsync(() => api.listSamples(), [], { live: true })

  const purposes = useMemo(() => {
    const seen = new Set<string>()
    for (const item of spectra.data ?? []) if (item.purpose) seen.add(item.purpose)
    return [...seen].sort((a, b) => a.localeCompare(b, 'ko'))
  }, [spectra.data])

  const inGroup = group.includes
  const shown = useMemo(() => {
    const needle = search.trim().toLowerCase()
    const byId = new Map((samples.data ?? []).map((s) => [s.id, s]))
    return (spectra.data ?? []).filter((item) => {
      if (shape === 'scan' && !isScan(item)) return false
      if (shape === 'single' && isScan(item)) return false
      if (purpose && item.purpose !== purpose) return false
      if (group.effective !== null) {
        const cell = item.sample_id === null ? undefined : byId.get(item.sample_id)
        if (!cell || !inGroup(cell.group_id)) return false
      }
      if (needle && !(item.name.toLowerCase().includes(needle)
        || item.original_name.toLowerCase().includes(needle)
        || (item.sample_name ?? '').toLowerCase().includes(needle))) return false
      return true
    })
  }, [spectra.data, samples.data, shape, purpose, search, group.effective, inGroup])

  // 스캔은 파일 단위로 세어야 뜻이 맞는다 — 스윕 21개는 스캔 1개다.
  const scanFiles = useMemo(
    () => new Set(shown.filter(isScan).map((item) => item.sha256)), [shown])

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>EIS 라이브러리</h1>
          <div className="sub">
            잰 것이 한 줄씩 — 스윕이 여럿인 파일은 스윕마다 한 줄이고, 그 묶음이
            SOC 스캔입니다
          </div>
        </div>
      </div>

      {/* 여러 개를 한 회로로 한꺼번에 맞추는 자리로 가는 길.  SOC 스캔은
          스윕이 스물이 넘으므로 이 길이 없으면 하나씩 맞춰야 한다. */}
      <div className="row" style={{ marginBottom: 10, gap: 8 }}>
        <Link className="link-btn" to="/eis/spectra">여러 개 한꺼번에 맞추기</Link>
        <Link className="link-btn" to="/eis/upload">업로드</Link>
      </div>

      <Card title="거르기" tight>
        <div className="grid cols-4" style={{ padding: 12, gap: 10 }}>
          <GroupFilterFields pick={group} hint="셀에 붙은 것만 남습니다" />
          <Field label="종류" hint="파일이 말하는 것 — 스윕 수로 갈립니다">
            <select
              aria-label="종류"
              value={shape}
              onChange={(event) => setShape(event.target.value as Shape)}
            >
              {SHAPES.map(([value, label]) => (
                <option key={value} value={value}>{label}</option>
              ))}
            </select>
          </Field>
          <Field label="전해질">
            <select
              aria-label="전해질"
              value={kind}
              onChange={(event) => setKind(event.target.value as EisKind | '')}
            >
              {KINDS.map(([value, label]) => (
                <option key={value} value={value}>{label}</option>
              ))}
            </select>
          </Field>
          <Field label="목적">
            <select
              aria-label="목적"
              value={purpose}
              onChange={(event) => setPurpose(event.target.value)}
            >
              <option value="">전체</option>
              {purposes.map((value) => (
                <option key={value} value={value}>{value}</option>
              ))}
            </select>
          </Field>
          <Field label="검색" hint="이름 · 파일명 · 셀">
            <input
              aria-label="검색"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </Field>
        </div>
      </Card>

      <Card
        title={`${shown.length}개${scanFiles.size ? ` · 스캔 ${scanFiles.size}개` : ''}`}
        tight
      >
        {spectra.error ? (
          <Alert kind="error">{spectra.error}</Alert>
        ) : spectra.loading && !spectra.data ? (
          <div style={{ padding: 20 }}><Spinner /></div>
        ) : shown.length ? (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left' }}>이름</th>
                  <th style={{ textAlign: 'left' }}>셀</th>
                  <th style={{ textAlign: 'left' }}>측정</th>
                  <th style={{ textAlign: 'left' }}>목적</th>
                  <th style={{ textAlign: 'left' }}>주파수</th>
                  <th>점</th>
                  <th>사이클</th>
                  <th style={{ textAlign: 'left' }}>피팅</th>
                  <th>올린 때</th>
                </tr>
              </thead>
              <tbody>
                {shown.map((item) => (
                  <tr key={item.id}>
                    <td className="text">
                      <Link to={`/eis/${item.id}`}>{item.name}</Link>
                      {isScan(item) ? (
                        // 스캔의 한 줄에서 그 스캔 전체로 가는 길.  이것이
                        // 없으면 스윕 21개를 훑어야 SOC 축을 볼 수 있다.
                        <>
                          {' '}
                          <Link to={`/scans/${item.sha256}`} className="tiny">
                            [스캔 {item.sweep_index}/{item.sweep_count}]
                          </Link>
                        </>
                      ) : null}
                    </td>
                    <td className="text dim">
                      {item.sample_id
                        ? <Link to={`/samples/${item.sample_id}`}>{item.sample_name}</Link>
                        : '— 안 붙임'}
                    </td>
                    <td className="text dim">
                      {item.kind === 'solid' ? '전고체' : '액체'}
                      {item.cell_config
                        ? ` · ${CONFIG_LABEL[item.cell_config] ?? item.cell_config}`
                        : ''}
                    </td>
                    <td className="text dim">{item.purpose || '—'}</td>
                    <td className="text dim tiny">{frequencySpan(item)}</td>
                    <td>{item.n_points}</td>
                    <td className="dim">
                      {item.at_cycle === null ? '—' : item.at_cycle}
                    </td>
                    <td className="text dim tiny">
                      {/* 맞춘 적이 없는 것과 맞췄는데 나쁜 것은 다르다. */}
                      {item.fit_count
                        ? `${item.best_circuit} χ²=${num(item.best_chi_squared, 3)}`
                        : '—'}
                    </td>
                    <td className="dim">{dateTime(item.uploaded_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <Empty title="해당하는 측정이 없습니다" icon="∿">
            <Link to="/eis/upload">업로드</Link>에서 <code>.mpr</code> 을 올리면
            여기 나타납니다.
          </Empty>
        )}
      </Card>
    </main>
  )
}
