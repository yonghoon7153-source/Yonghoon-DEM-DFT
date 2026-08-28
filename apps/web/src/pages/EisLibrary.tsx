/** EIS 라이브러리 — 잰 것이 한 줄씩.
 *
 *  대시보드는 **셀**이 한 줄이고 여기는 **측정**이 한 줄이다.  둘 다 필요하다:
 *  "이 셀 임피던스가 어떻게 되지" 와 "그 스윕 어디 있지" 는 다른 질문이다.
 *
 *  SOC 스캔이 따로 있던 화면을 여기로 접었다.  같은 `.mpr` 이고 같은 회로로
 *  맞추므로 화면을 가를 이유가 없고, 다른 것은 파일 하나가 스윕 하나냐
 *  스물이냐 뿐이라 **거르개 하나**면 된다 (ADR 0022).
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
import { isScan, scanFit } from '../lib/eis'
import { dateTime, num } from '../lib/format'
import { useAsync, useStickyState } from '../lib/hooks'
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

export function EisLibrary() {
  const [shape, setShape] = useState<Shape>('all')
  const [kind, setKind] = useState<EisKind | ''>('')
  const [purpose, setPurpose] = useState('')
  const [search, setSearch] = useState('')

  const [reloadKey, bumpReload] = useState(false)
  // 표 바깥에 한 번만.  행 안에 끼우면 열이 밀린다 (셀 라이브러리와 같은 규칙).
  const [rowError, setRowError] = useState<string | null>(null)

  const spectra = useAsync(
    () => api.listSpectra({ kind: kind || undefined }), [kind, reloadKey],
    { live: true })
  const group = useGroupChoice()
  // 그룹은 셀의 성질이라 셀 표가 있어야 거를 수 있다 (비교 화면과 같다).
  const samples = useAsync(() => api.listSamples(), [], { live: true })

  const attach = useCallback(async (id: number, sampleId: number | null) => {
    setRowError(null)
    try {
      // 빈 값은 떼어내기다.  `sample_id: null` 은 "안 보냄" 과 구별되지 않아
      // 서버가 clear 를 따로 받는다.
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

  //: **SOC 스캔은 한 줄로 접는다** (기본).  파일 하나가 스윕 스물이면 목록의
  //  스무 줄이 같은 파일이고, 그 스무 줄은 서로 아무것도 구별해 주지 않는다 --
  //  이름도 같고 대역도 같고 회로도 같다.  훑어야 할 것은 "이 파일이 있다"
  //  하나이고, 스윕 사이의 차이는 스캔 화면이 그림으로 보여 준다.
  //
  //  펴는 길을 남겨 둔다: 스윕 하나를 지우거나 셀에 따로 붙이는 일이 있다.
  const [foldScans, setFoldScans] = useStickyState('bml.eisFoldScans', true)

  const inGroup = group.includes
  const matched = useMemo(() => {
    const needle = search.trim().toLowerCase()
    return (spectra.data ?? []).filter((item) => {
      if (shape === 'scan' && !isScan(item)) return false
      if (shape === 'single' && isScan(item)) return false
      if (purpose && item.purpose !== purpose) return false
      // 그룹은 이제 **측정 자신의 것**이 먼저다 (ADR 0027) -- 셀에 안 붙은
      // 측정도 묶일 수 있고, `*_effective` 가 "자기 것 → 셀 것" 을 이미 편다.
      if (!inGroup(item.group_id_effective ?? null)) return false
      if (needle && !(item.name.toLowerCase().includes(needle)
        || item.original_name.toLowerCase().includes(needle)
        || (item.sample_name ?? '').toLowerCase().includes(needle))) return false
      return true
    })
  }, [spectra.data, samples.data, shape, purpose, search, group.effective, inGroup])

  //: 접을 때는 **파일마다 첫 스윕만** 남긴다.  걸러진 뒤에 접는 순서가 맞다 —
  //  먼저 접으면 검색어에 맞는 스윕이 3번인데 1번만 남아 아무것도 안 걸린다.
  const shown = useMemo(() => {
    if (!foldScans) return matched
    const seen = new Set<string>()
    return matched.filter((item) => {
      if (!isScan(item)) return true
      if (seen.has(item.sha256)) return false
      seen.add(item.sha256)
      return true
    })
  }, [matched, foldScans])

  //: 접힌 줄이 대표하는 스윕들.  줄에 그 수를 적어야 "이 파일에 스물이
  //  있다" 가 보인다 -- 안 적으면 접은 것과 원래 하나인 것이 같아 보인다.
  //  그리고 fitting 칸도 이것으로 센다: 접힌 줄에 **첫 스윕의** χ² 만 적으면
  //  하나만 맞춘 파일이 맞춘 파일로 보인다 (`scanFit`).
  const sweepsOf = useMemo(() => {
    const rows = new Map<string, Spectrum[]>()
    for (const item of matched) {
      if (!isScan(item)) continue
      const seen = rows.get(item.sha256)
      if (seen) seen.push(item)
      else rows.set(item.sha256, [item])
    }
    return rows
  }, [matched])

  // 스캔은 파일 단위로 세어야 뜻이 맞는다 — 스윕 21개는 스캔 1개다.
  const scanFiles = useMemo(
    () => new Set(shown.filter(isScan).map((item) => item.sha256)), [shown])

  // 묶기 — 셀 라이브러리와 같은 어휘, 같은 모양 (`LibraryGroups`).
  // **기본이 '그룹' 이다.**  묶는 것이 이 화면의 첫 모습이어야 한다 — 폴더가
  // 다 접혀 있으므로 (ADR 0035) 그것이 곧 요약이고, `없음` 으로 시작하면 셀
  // 마흔일곱 줄이 먼저 쏟아진 뒤 사람이 매번 `그룹` 을 눌러야 한다.
  // 열쇠를 바꾼 것은 기본값이 뒤집혀서다: 옛 열쇠에 남은 `none` 은 "안 골랐다"
  // 가 아니라 "골라서 없음" 으로 읽히고, 그러면 새 기본이 영영 안 온다.
  const [groupBy, setGroupBy] = useStickyState<GroupKey>('bml.eisGroupBy.v2', 'group')
  const groupKey = validGroupKey(groupBy)
  const folders = useFolders('eis-library', shown, placeSpectrum)
  const buckets = useMemo(
    () => bucketize(shown, groupKey, bucketOf), [shown, groupKey])

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
        {/* **한 줄에 넣는다.**  `cols-4` 로 두면 일곱 칸이 두 줄이 되고, 두
            줄짜리 거르개는 그 밑의 목록을 화면 밖으로 민다.  칸마다 필요한
            폭이 크게 달라서 균등 분할도 안 맞는다: `SOC 스캔` 은 단추 두 개라
            좁아도 되고, `종류` 는 `단일 스펙트럼` 이 안 잘려야 하므로 넓어야
            한다.  그래서 폭을 손으로 나눈다. */}
        <div className="filter-row" style={{ padding: 12 }}>
          <GroupFilterFields pick={group} hint="셀에 붙은 것만 남습니다" />
          {/* 스캔을 접을지.  기본은 접기 — 스윕 스무 줄이 같은 파일이면 그
              스무 줄은 서로 아무것도 구별해 주지 않는다.  펴는 길은 남긴다:
              스윕 하나를 지우거나 셀에 따로 붙이는 일이 있다. */}
          <Field label="SOC 스캔" hint="스윕을 한 줄로 접습니다">
            <div className="segmented" role="group" aria-label="SOC 스캔">
              <button type="button" className={foldScans ? 'on' : ''}
                      onClick={() => setFoldScans(true)}>묶기</button>
              <button type="button" className={foldScans ? '' : 'on'}
                      onClick={() => setFoldScans(false)}>스윕 전부</button>
            </div>
          </Field>
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

      {rowError ? <Alert kind="error">{rowError}</Alert> : null}

      <Card
        title={`${shown.length}개${scanFiles.size ? ` · 스캔 ${scanFiles.size}개` : ''}`}
        actions={<GroupByControl value={groupKey} onChange={setGroupBy} />}
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
                  <th style={{ textAlign: 'left' }}>관계셀</th>
                  <th style={{ textAlign: 'left' }}>측정</th>
                  <th style={{ textAlign: 'left' }}>목적</th>
                  <th style={{ textAlign: 'left' }}>주파수</th>
                  <th>점</th>
                  <th>사이클</th>
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
          <Empty title="해당하는 측정이 없습니다" icon="∿">
            <Link to="/eis/upload">업로드</Link>에서 <code>.mpr</code> 을 올리면
            여기 나타납니다.
          </Empty>
        )}
      </Card>
    </main>
  )

  function row(item: Spectrum) {
    // 접혀 있을 때만 스캔 전체를 센다.  펴 놓으면 한 줄이 스윕 하나이므로
    // 그 스윕 자신의 맞춤을 적는 것이 맞다.
    const sweeps = foldScans && isScan(item) ? sweepsOf.get(item.sha256) : undefined
    const scan = sweeps ? scanFit(sweeps, item.sweep_count) : null
    return (
                  <tr key={item.id}>
                    <td className="text">
                      {/* 지우기를 **이름 앞**에 둔다.  꼬리 열이던 것을 없애면
                          표가 한 칸 좁아지고, 그만큼 가로 스크롤이 줄어든다 —
                          값을 보려고 옆으로 미는 것이 이 표들의 가장 큰
                          불편이었다. */}
                      <DeleteMeasurementButton
                        name={item.name}
                        onError={setRowError}
                        onDelete={async () => {
                          await api.deleteSpectrum(item.id)
                          bumpReload((value) => !value)
                        }}
                      />
                      {/* 그룹과 올린 사람을 이름 앞에 — 대시보드와 같은 모양이다.
                          `group_label` 은 이미 "부모 · 자식" 한 줄이라 잎만
                          칩에 적고 전체 길은 마우스로 돌린다. */}
                      <GroupTag name={leafOf(item.group_label)} path={item.group_label} />
                      <OwnerTag owner={item.created_by} />
                      <Link to={`/eis/${item.id}`}>{item.name}</Link>
                      {isScan(item) ? (
                        // 스캔의 한 줄에서 그 스캔 전체로 가는 길.  이것이
                        // 없으면 스윕 21개를 훑어야 SOC 축을 볼 수 있다.
                        //
                        // 접혀 있으면 **이 줄이 몇 개를 대표하는지**를 적는다.
                        // 안 적으면 접은 줄과 원래 하나인 줄이 같아 보인다.
                        <>
                          {' '}
                          <Link to={`/scans/${item.sha256}`} className="tiny">
                            {foldScans
                              ? `[SOC 스캔 · 스윕 ${sweepsOf.get(item.sha256)?.length
                                  ?? item.sweep_count}개]`
                              : `[스캔 ${item.sweep_index}/${item.sweep_count}]`}
                          </Link>
                        </>
                      ) : null}
                    </td>
                    <td className="text dim">
                      {/* 붙이는 일을 여기서 한다 -- 다른 화면으로 갔다 오지 않게.
                          붙지 않은 채로 두는 것도 정상이다 (§0.4). */}
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
                      {/* 맞춘 적이 없는 것과 맞췄는데 나쁜 것은 다르다.
                          접힌 스캔 줄은 이 줄이 대표하는 **스윕 전부**를 센다 —
                          첫 스윕의 χ² 는 그 파일의 상태가 아니다. */}
                      {scan ? (
                        <>
                          {scan.label}
                          {scan.detail
                            ? <div className="faint">{scan.detail}</div>
                            : null}
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

/** 이 측정을 폴더 자리로 (ADR 0035).  그룹은 **측정 자신의 것**이 먼저고,
 *  비어 있으면 붙은 셀의 것이다 (`*_effective`, ADR 0027). */
const placeSpectrum = (item: Spectrum) => ({
  id: item.id,
  groupId: item.group_id_effective ?? null,
  groupName: item.group_name_effective ?? '',
  groupParentName: item.group_parent_name_effective ?? '',
})

/** 그룹이 아닌 묶기의 값.  "" 는 값이 없다는 뜻이고 그 묶음은 맨 아래로 간다. */
function bucketOf(item: Spectrum, key: GroupKey): string {
  switch (key) {
    case 'owner': return item.created_by ?? ''
    case 'cathode': return item.cathode_type_effective || ''
    case 'process': return item.process_effective || ''
    case 'temperature':
      return item.temperature_c_effective === null
        || item.temperature_c_effective === undefined
        ? '' : `${item.temperature_c_effective}°C`
    default: return ''
  }
}

/** 폴더 줄이 표 전체 폭을 덮으려면 열 수가 맞아야 한다.  틀리면 그 줄만
 *  가로로 밀려 표가 어긋난다 — 이름·관계셀·측정·목적·주파수·점·사이클·
 *  fitting·올린 때 = 9.  지우기는 이름 칸 안으로 들어갔다. */
const COLUMN_COUNT = 9
