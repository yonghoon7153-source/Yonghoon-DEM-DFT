/** 대칭셀 라이브러리 — 전해질만 보는 측정이 한 줄씩 (ADR 0039).
 *
 *  EIS 라이브러리와 **같은 모양**이다: 같은 거르개(그룹·소그룹·묶기·검색),
 *  같은 폴더 줄, 같은 행 꼬리표(그룹·작성자), 같은 관계셀 드롭다운, 같은
 *  지우기.  두 화면이 같은 종류의 목록이라 어휘가 갈리면 안 된다 — 한쪽에서
 *  익힌 손이 다른 쪽에서 헤매는 것이 이 저장소에서 제일 흔한 불편이었다.
 *
 *  다른 것은 **무엇을 세느냐** 뿐이다.  열에는 주파수·점 대신 **온도**와
 *  **이온전도도로 가는 길**이 선다.
 *
 *  **`묶기`/`스윕 전부` 는 EIS 라이브러리에 있는 그대로 있다.**  처음에는 여기
 *  한 줄은 늘 파일 하나라고 두었는데 (묻는 것이 "이 전해질의 활성화에너지" 라
 *  스윕 아홉 줄은 그 질문에 답을 안 한다), 그러면 **스윕 하나를 고칠 길이
 *  없어진다** — 온도를 한 칸만 고치거나, 잘못 잰 스윕 하나를 빼거나, 그 스윕만
 *  다른 셀에 붙이는 일이 실제로 있다.  기본은 묶기이고, 펴는 길을 남긴다.
 */

import { useCallback, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { FolderRow, useFolders } from '../components/FolderTree'
import { GroupFilterFields, useGroupChoice } from '../components/GroupFilter'
import {
  BucketRow, GroupByControl, type GroupKey, bucketize, validGroupKey,
} from '../components/LibraryGroups'
import { DeleteMeasurementButton, RelatedCellSelect } from '../components/RelatedCell'
import { GroupTag, OwnerTag, leafOf } from '../components/RowTags'
import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { CONDUCTIVITY_PURPOSE } from '../lib/conductivity'
import { isScan, scanFit } from '../lib/eis'
import { dateTime, num } from '../lib/format'
import { useAsync, useStickyState } from '../lib/hooks'
import type { Spectrum } from '../lib/types'

/** 이 측정이 대칭셀 파트의 것인가.
 *
 *  둘 중 하나면 된다: 목적에 `이온전도도` 가 적혀 있거나, 셀 구성이 대칭셀
 *  이거나.  **숨기지 않는 쪽으로 넉넉하게 잡는다** — 여기 안 보이는 파일은
 *  사람이 찾을 자리가 없고, 잘못 들어온 파일은 눈에 띄면 그만이다.
 */
function isSymMeasurement(item: Spectrum): boolean {
  return (item.purpose ?? '').includes('이온전도도') || item.cell_config === 'sym'
}

export function SymCells() {
  const [onlySym, setOnlySym] = useStickyState('bml.symOnly', true)
  //: 기본은 묶기 — 파일 하나가 스윕 아홉이면 아홉 줄이 서로 아무것도 구별해
  //  주지 않는다.  펴는 길을 남기는 이유는 위 주석에 있다.
  const [foldScans, setFoldScans] = useStickyState('bml.symFoldScans', true)
  const [purpose, setPurpose] = useState('')
  const [search, setSearch] = useState('')
  const [reloadKey, bumpReload] = useState(false)
  // 표 바깥에 한 번만.  행 안에 끼우면 열이 밀린다 (EIS 라이브러리와 같은 규칙).
  const [rowError, setRowError] = useState<string | null>(null)

  const spectra = useAsync(() => api.listSpectra(), [reloadKey], { live: true })
  const group = useGroupChoice()
  const samples = useAsync(() => api.listSamples(), [], { live: true })

  const attach = useCallback(async (id: number, sampleId: number | null) => {
    setRowError(null)
    try {
      await api.updateSpectrum(id, sampleId
        ? { sample_id: sampleId }
        : { clear: ['sample_id'] })
      bumpReload((value) => !value)
    } catch (cause) {
      setRowError(cause instanceof Error ? cause.message : String(cause))
    }
  }, [])

  const purposes = useMemo(() => {
    const seen = new Set<string>()
    for (const item of spectra.data ?? []) if (item.purpose) seen.add(item.purpose)
    return [...seen].sort((a, b) => a.localeCompare(b, 'ko'))
  }, [spectra.data])

  const inGroup = group.includes
  const matched = useMemo(() => {
    const needle = search.trim().toLowerCase()
    return (spectra.data ?? []).filter((item) => {
      // 스윕이 하나뿐인 파일은 온도 스윕이 아니다 — 여기 세울 표가 없다.
      if (!isScan(item)) return false
      if (onlySym && !isSymMeasurement(item)) return false
      if (purpose && item.purpose !== purpose) return false
      if (!inGroup(item.group_id_effective ?? null)) return false
      if (needle && !(item.name.toLowerCase().includes(needle)
        || item.original_name.toLowerCase().includes(needle)
        || (item.sample_name ?? '').toLowerCase().includes(needle))) return false
      return true
    })
  }, [spectra.data, onlySym, purpose, search, inGroup])

  //: 접을 때는 **파일마다 첫 스윕만** 남긴다.  걸러진 뒤에 접는 순서가 맞다 —
  //  먼저 접으면 검색어에 맞는 스윕이 3번인데 1번만 남아 아무것도 안 걸린다
  //  (EIS 라이브러리와 같은 규칙).
  const shown = useMemo(() => {
    if (!foldScans) return matched
    const seen = new Set<string>()
    return matched.filter((item) => {
      if (seen.has(item.sha256)) return false
      seen.add(item.sha256)
      return true
    })
  }, [matched, foldScans])

  //: 접힌 줄이 대표하는 스윕들 — fitting 칸과 온도 칸이 이것으로 선다.
  //  첫 스윕만 보면 하나만 맞춘 파일이 맞춘 파일로 보인다 (`scanFit`).
  const sweepsOf = useMemo(() => {
    const rows = new Map<string, Spectrum[]>()
    for (const item of matched) {
      const seen = rows.get(item.sha256)
      if (seen) seen.push(item)
      else rows.set(item.sha256, [item])
    }
    return rows
  }, [matched])

  const hidden = useMemo(() => {
    const files = new Set<string>()
    for (const item of spectra.data ?? []) {
      if (isScan(item) && !isSymMeasurement(item)) files.add(item.sha256)
    }
    return files.size
  }, [spectra.data])

  const [groupBy, setGroupBy] = useStickyState<GroupKey>('bml.symGroupBy', 'group')
  const groupKey = validGroupKey(groupBy)
  const folders = useFolders('sym-library', shown, placeSpectrum)
  const buckets = useMemo(
    () => bucketize(shown, groupKey, bucketOf), [shown, groupKey])

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>대칭셀 라이브러리</h1>
          <div className="sub">
            온도를 바꿔 가며 건 PEIS 한 파일이 한 줄씩 — 열면 온도별
            이온전도도와 활성화에너지가 섭니다
          </div>
        </div>
      </div>

      <div className="row" style={{ marginBottom: 10, gap: 8 }}>
        <Link className="link-btn" to="/eis/spectra">여러 개 한꺼번에 맞추기</Link>
        <Link className="link-btn" to="/eis/upload">업로드</Link>
      </div>

      <Card title="거르기" tight>
        <div className="filter-row" style={{ padding: 12 }}>
          <GroupFilterFields pick={group} hint="셀에 붙은 것만 남습니다" />
          <Field label="보기" hint="대칭셀이 아닌 스캔도 볼 수 있습니다">
            <div className="segmented" role="group" aria-label="보기">
              <button type="button" className={onlySym ? 'on' : ''}
                      onClick={() => setOnlySym(true)}>대칭셀</button>
              <button type="button" className={onlySym ? '' : 'on'}
                      onClick={() => setOnlySym(false)}>스캔 전부</button>
            </div>
          </Field>
          {/* 펴면 스윕이 한 줄씩 — 온도를 한 칸만 고치거나, 잘못 잰 스윕
              하나를 빼거나, 그 스윕만 다른 셀에 붙일 때 쓴다. */}
          <Field label="스캔" hint="스윕을 한 줄로 접습니다">
            <div className="segmented" role="group" aria-label="스캔">
              <button type="button" className={foldScans ? 'on' : ''}
                      onClick={() => setFoldScans(true)}>묶기</button>
              <button type="button" className={foldScans ? '' : 'on'}
                      onClick={() => setFoldScans(false)}>스윕 전부</button>
            </div>
          </Field>
          <Field label="목적" hint="올릴 때 적어 둔 것">
            <select
              aria-label="목적"
              value={purpose}
              onChange={(event) => setPurpose(event.target.value)}
            >
              <option value="">전체</option>
              {purposes.map((one) => (
                <option key={one} value={one}>{one}</option>
              ))}
            </select>
          </Field>
          <Field label="검색" hint="이름 · 파일 · 셀">
            <input
              aria-label="검색"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="이름 · 파일 · 셀"
            />
          </Field>
        </div>
        {/* 무엇이 안 보이는지 적는다.  "왜 내 파일이 없지" 가 이 화면에서 제일
            먼저 나오는 질문이고, 답은 목적이거나 셀 구성이다. */}
        {onlySym && hidden > 0 ? (
          <div className="tiny dim" style={{ padding: '0 12px 12px' }}>
            대칭셀이 아닌 스캔 {hidden}개는 숨겨져 있습니다 — 목적을{' '}
            <code>{CONDUCTIVITY_PURPOSE}</code> 로 적거나 셀 구성을 대칭셀로 두면
            여기 나옵니다.
          </div>
        ) : null}
      </Card>

      <Card
        title={`스캔 ${shown.length}개`}
        tight
        actions={<GroupByControl value={groupKey} onChange={setGroupBy} />}
      >
        {rowError ? <Alert kind="error">{rowError}</Alert> : null}
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
                  <th style={{ textAlign: 'left' }}>관계셀</th>
                  <th style={{ textAlign: 'left' }}>목적</th>
                  <th>스윕</th>
                  <th style={{ textAlign: 'left' }}>온도</th>
                  <th style={{ textAlign: 'left' }}>fitting</th>
                  <th>올린 때</th>
                </tr>
              </thead>
              {groupKey === 'group' ? (
                folders.folders.filter(folders.isVisible).map((folder) => (
                  <tbody key={folder.key}>
                    <FolderRow folder={folder} view={folders} columns={COLUMN_COUNT} />
                    {folders.isFolded(folder.key) ? null : folder.items.map(row)}
                  </tbody>
                ))
              ) : buckets ? (
                buckets.map(([label, items]) => (
                  <tbody key={label || '(none)'}>
                    <BucketRow label={label} count={items.length} columns={COLUMN_COUNT} />
                    {items.map(row)}
                  </tbody>
                ))
              ) : (
                <tbody>{shown.map(row)}</tbody>
              )}
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

  function row(item: Spectrum) {
    const sweeps = sweepsOf.get(item.sha256) ?? [item]
    const total = item.sweep_count ?? sweeps.length
    //: 접힌 줄은 **그 파일 전부**를 대표하고, 편 줄은 **그 스윕 하나**다.
    //  fitting 칸도 지우기도 그 단위를 따라간다 — 한쪽만 따라가면 화면이
    //  스스로 모순된다 (줄에는 스윕 하나가 적혀 있는데 지우면 아홉이 사라진다).
    const scan = foldScans ? scanFit(sweeps, total) : null
    return (
      <tr key={foldScans ? item.sha256 : `${item.sha256}#${item.sweep_index}`}>
        <td className="text">
          {/* 지우기를 이름 앞에 — EIS 라이브러리와 같은 자리다. */}
          <DeleteMeasurementButton
            name={item.name}
            note={foldScans ? `스윕 ${total}개 전부` : `스윕 ${item.sweep_index}/${total} 만`}
            onError={setRowError}
            onDelete={async () => {
              if (foldScans) await api.deleteScan(item.sha256)
              else await api.deleteSpectrum(item.id)
              bumpReload((value) => !value)
            }}
          />
          <GroupTag name={leafOf(item.group_label)} path={item.group_label} />
          <OwnerTag owner={item.created_by} />
          <Link to={`/sym/scan/${item.sha256}`}>
            {foldScans ? scanName(item) : item.name}
          </Link>
          {' '}
          {/* 나이퀴스트로 가는 길 — 같은 파일의 다른 보기다.  편 줄에서는
              그 스윕 하나의 화면으로 간다 (거기서 고친다). */}
          {foldScans ? (
            <Link to={`/scans/${item.sha256}`} className="tiny">[나이퀴스트]</Link>
          ) : (
            <Link to={`/eis/${item.id}`} className="tiny">
              [스윕 {item.sweep_index}/{total}]
            </Link>
          )}
        </td>
        <td className="text dim">
          <div className="col" style={{ gap: 3, minWidth: 0, width: 200 }}>
            <RelatedCellSelect
              value={item.sample_id}
              samples={samples.data ?? []}
              label={`${item.name} 관계셀`}
              onPick={(sampleId) => void attach(item.id, sampleId)}
            />
            {item.sample_id ? (
              <Link className="tiny truncate" to={`/samples/${item.sample_id}`}>
                셀 화면 →
              </Link>
            ) : null}
          </div>
        </td>
        <td className="text dim">{item.purpose || '—'}</td>
        <td>{foldScans ? total : `${item.sweep_index}/${total}`}</td>
        {/* 온도는 **사람이 적는다** (ADR 0039).  안 적혔으면 그렇게 적는다 —
            비어 있는 것이 정상이고, 그것이 다음에 할 일이다.  편 줄에서는 그
            스윕 자신의 온도 하나다. */}
        <td className="text dim tiny">
          {foldScans
            ? temperatureSpan(sweeps, total)
            : (item.temperature_c === null || item.temperature_c === undefined
                ? '아직 없음' : `${item.temperature_c} °C`)}
        </td>
        <td className="text dim tiny">
          {scan ? (
            <>
              {scan.label}
              {scan.detail ? <div className="faint">{scan.detail}</div> : null}
            </>
          ) : item.fit_count
            ? `${item.best_circuit} χ²=${num(item.best_chi_squared, 3)}`
            : '—'}
        </td>
        <td className="dim">{dateTime(item.uploaded_at)}</td>
      </tr>
    )
  }
}

/** 스윕 번호를 뗀 이름.  목록의 한 줄이 파일이므로 `#1` 은 뜻이 없다. */
function scanName(item: Spectrum): string {
  return item.name.replace(/\s*#\d+$/, '')
}

/** 이 파일이 걸친 온도 — `60 ~ -20 °C`.  하나도 안 적혔으면 그렇게 말한다.
 *
 *  걸러져 안 보이는 스윕이 있을 수 있으므로 **파일이 말하는 스윕 수**와 견준다.
 *  걸러진 수로 "3/3 적음" 이라고 적으면 아홉 중 셋만 적힌 파일이 다 적힌
 *  파일로 보인다.
 */
function temperatureSpan(sweeps: Spectrum[], total: number): string {
  const written = sweeps
    .map((one) => one.temperature_c)
    .filter((one): one is number => one !== null && one !== undefined)
  if (!written.length) return '아직 없음'
  const high = Math.max(...written)
  const low = Math.min(...written)
  const span = high === low ? `${high} °C` : `${high} ~ ${low} °C`
  return written.length === total ? span : `${span} (${written.length}/${total})`
}

/** 이 측정을 폴더 자리로 (ADR 0035) — EIS 라이브러리와 같은 규칙. */
const placeSpectrum = (item: Spectrum) => ({
  id: item.id,
  groupId: item.group_id_effective ?? null,
  groupName: item.group_name_effective ?? '',
  groupParentName: item.group_parent_name_effective ?? '',
})

function bucketOf(item: Spectrum, key: GroupKey): string {
  switch (key) {
    case 'owner': return item.created_by ?? ''
    case 'cathode': return item.cathode_type_effective || ''
    case 'process': return item.process_effective || ''
    // 이 화면에서 `온도` 묶기는 뜻이 얕다 — 스윕마다 온도가 다르고 이 줄은
    // 1번 스윕을 대표로 세우기 때문이다.  그래도 남겨 둔다: 챔버를 한 온도로
    // 두고 잰 다른 스캔이 섞여 있을 수 있다.
    case 'temperature':
      return item.temperature_c_effective === null
        || item.temperature_c_effective === undefined
        ? '' : `${item.temperature_c_effective}°C`
    default: return ''
  }
}

/** 이름·관계셀·목적·스윕·온도·fitting·올린 때 = 7. */
const COLUMN_COUNT = 7
