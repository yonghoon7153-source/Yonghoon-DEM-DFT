/** EIS 비교 — 아무 스펙트럼이나 골라 겹쳐 본다.
 *
 *  셀 상세의 `CellSpectra` 와 겹쳐 그리는 일은 같지만 **고르는 범위**가 다르다.
 *  저쪽은 한 셀 안이고 여기는 전부다 — 서로 다른 셀의 200 사이클 임피던스를
 *  나란히 놓는 것이 이 화면의 이유고, 그건 저쪽에서는 할 수가 없다.
 *
 *  나이퀴스트는 두 축의 한 단위가 화면에서 같은 길이여야 한다 (`equalAspect`).
 *  세로가 눌리면 찌그러진 아크와 이상적인 반원이 구분되지 않고, 사람이 회로를
 *  고를 때 보는 것이 바로 그 차이다.
 */

import { useCallback, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { CopyBar } from '../components/CopyBar'
import { useGroupChoice } from '../components/GroupFilter'
import { PickGrid } from '../components/PickGrid'
import { Plot, type PlotSeries } from '../components/Plot'
import { Alert, Card, Empty, Field, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { num, seriesColor } from '../lib/format'
import { useAsync, useStickyState } from '../lib/hooks'
import { TAU_AXIS_LABEL, TAU_AXIS_SHORT, tauAxisValue } from '../lib/tauaxis'
import { perArea } from '../lib/areanorm'
import { Z_UNIT_KEY, type ZUnit, validZUnit, zUnitLabel } from '../lib/zunit'
import { rememberedLambda } from '../lib/drtlambda'
import { inductiveCount, isScan, nyquistXy, sweepAt } from '../lib/eis'
import { nyquistWideTsv, seriesWideTsv } from '../lib/origin'
import type { EisKind, Spectrum, SpectrumFit, SpectrumPoints } from '../lib/types'

/** 서버의 `/api/eis/points` 겹치기 상한과 같은 수. */
const OVERLAY_LIMIT = 12

/** 파일 하나를 어떻게 부를까.  셀이 다르면 셀 이름이 먼저다 — 이 화면의 요점이
 *  서로 다른 셀을 나란히 놓는 것이라, 이름만으로는 어느 셀 것인지 모른다. */
function fileLabel(item: Spectrum): string {
  const parts = [item.sample_name, item.name].filter(Boolean)
  const tail = item.at_cycle === null ? '' : ` (${item.at_cycle}c)`
  return `${parts.join(' · ')}${tail}`
}

/** 한 곡선을 어떻게 부를까.
 *
 *  SOC 스캔은 스윕 스물이 **이름도 사이클도 같다** (한 파일이니까).  그대로
 *  두면 범례에 같은 글자가 스무 줄 서고, 그중 어느 것이 어느 SOC 인지는
 *  아무 데도 없다 — 겹쳐 보는 이유가 바로 그 차이인데.  스윕 번호를 붙이고,
 *  SOC 는 범례 꼬리표로 (`PlotSeries.note`) 단다.
 */
function label(item: Spectrum): string {
  return isScan(item) ? `${fileLabel(item)} #${item.sweep_index ?? '?'}` : fileLabel(item)
}

/** 어느 그림인가.
 *
 *  `fit` 은 나이퀴스트와 같은 축이지만 **실측 위에 맞춤 곡선을 얹은** 것이다.
 *  따로 둔 이유는 맞춤이 스펙트럼마다 있을 수도 없을 수도 있기 때문이다 —
 *  없는 것을 말없이 빼면 그림에 곡선이 하나 모자란 채로 남고, 그 그림은
 *  "안 맞췄다" 를 아무 데도 적지 않는다 (§0.4).
 */
type Mode = 'nyquist' | 'fit' | 'drt'

const MODE_TITLE: Record<Mode, string> = {
  nyquist: '나이퀴스트',
  fit: 'fitting 곡선',
  drt: 'DRT (이완 시간 분포)',
}

/** 면적이 없는 것은 Ω·cm² 그림에서 **뺀다.**
 *
 *  Ω 와 Ω·cm² 를 한 세로눈금에 섞으면 그림이 조용히 거짓말을 한다: 두 곡선의
 *  크기 차이가 재료 차이인지 단위 차이인지 볼 방법이 없다.  빼고, **뺐다고
 *  이름을 적는다** (§0.4) — 말 없이 빼면 그 스펙트럼은 화면에서 그냥 사라진다.
 */
export function splitByArea<T extends { id: number }>(
  items: T[], areaOf: (id: number) => number | null,
): { kept: T[]; dropped: T[] } {
  const kept: T[] = []
  const dropped: T[] = []
  for (const item of items) {
    const area = areaOf(item.id)
    ;(area && area > 0 ? kept : dropped).push(item)
  }
  return { kept, dropped }
}

/** 임피던스를 면적으로 곱한다 (Ω → Ω·cm²).  `null` 면적이면 그대로 둔다. */
export function scaleSpectrum(item: SpectrumPoints, area: number | null): SpectrumPoints {
  if (!area || area <= 0) return item
  return {
    ...item,
    z_re: item.z_re.map((value) => value * area),
    z_im: item.z_im.map((value) => value * area),
  }
}

export function EisCompare() {
  const [kind, setKind] = useState<EisKind | ''>('')
  const [purpose, setPurpose] = useState('')
  const [sampleId, setSampleId] = useState<number | null>(null)
  const [search, setSearch] = useState('')
  const [chosen, setChosen] = useState<number[]>([])
  // 기본은 켜기.  겹쳐 보는 화면에서는 세로 눈금이 **하나**라, 한 스펙트럼의
  // 유도성 꼬리가 −20 Ω 까지 내려가면 나머지 전부의 아크가 그만큼 납작해진다
  // -- 비교하러 온 사람이 제일 먼저 잃는 것이 그 높이다.
  //
  // 지우는 것이 아니라 접어 두는 것이다 (ADR 0019: 뺐으면 뺐다고 말한다).
  // 몇 점을 뺐는지 그림 밑에 적고, 그 자리에서 도로 켤 수 있다 — 유도성
  // 아크가 진짜인 셀(리튬 도금 같은)을 보러 온 사람이 막히지 않게.
  const [dropInductive, setDropInductive] = useState(true)
  //: Ω 인가 Ω·cm² 인가.  **기본은 Ω** — 면적이 없는 스펙트럼이 하나라도 있으면
  //  Ω·cm² 는 그것을 빼야 하고, 처음 여는 사람에게 스펙트럼이 없어져 보이는
  //  것보다 단위가 셀마다 다르다는 것이 덜 놀랍다.  (상세 화면의 기본은
  //  반대다 — 거기는 스펙트럼이 하나라 사라질 것이 없다.)
  //
  //  고른 것은 상세 화면과 **같은 열쇠**로 남는다 (`lib/zunit.ts`): 같은 R₀ 가
  //  한 화면에서 15.6, 다른 화면에서 12.3 으로 나오면 두 수가 다른 단위라는
  //  말이 축 이름에만 남고, 눈은 축까지 안 간다.
  const [storedUnit, setUnit] = useStickyState<ZUnit>(Z_UNIT_KEY, 'ohm')
  const unit = validZUnit(storedUnit, 'ohm')
  //: 어느 그림을 보고 있나.  Origin 클립보드가 이것을 따라간다 — 안 보이는
  //  그림을 복사할 수 있으면 사람은 방금 본 것을 복사했다고 믿는다.
  const [mode, setMode] = useState<Mode>('nyquist')

  const spectra = useAsync(
    () => api.listSpectra({ kind: kind || undefined }), [kind], { live: true })
  const group = useGroupChoice()
  // 어느 셀이 어느 그룹인지는 스펙트럼이 아니라 셀이 안다.  그룹으로 거르려면
  // 그 표가 필요하고, 같은 표가 "충방전으로 가는 링크" 의 근거이기도 하다.
  const samples = useAsync(() => api.listSamples(), [], { live: true })

  /** 이 스펙트럼이 붙은 셀.  안 붙어 있으면 `undefined`. */
  const cellOf = useCallback(
    (item: Spectrum) => (samples.data ?? []).find((s) => s.id === item.sample_id),
    [samples.data])

  /** 지금 데이터에 실제로 있는 목적들.  목록을 고정하지 않는 이유는 목적이
   *  자유 입력이라서다 — 랩이 새 목적을 만들면 여기에 저절로 나타난다. */
  const purposes = useMemo(() => {
    const seen = new Set<string>()
    for (const item of spectra.data ?? []) if (item.purpose) seen.add(item.purpose)
    return [...seen].sort((a, b) => a.localeCompare(b, 'ko'))
  }, [spectra.data])

  /** 셀에 붙은 것만, 그룹 안에서.  붙지 않은 스펙트럼은 그룹이 없으므로
   *  그룹을 고른 순간 후보에서 빠진다 — 없는 소속을 지어내지 않는다 (§0.4). */
  const inGroup = group.includes
  const rows = useMemo(() => {
    const needle = search.trim().toLowerCase()
    return (spectra.data ?? []).filter((item) => {
      if (purpose && (item.purpose ?? '') !== purpose) return false
      if (sampleId !== null && item.sample_id !== sampleId) return false
      // 그룹은 이제 **측정 자신의 것**이 먼저다 (ADR 0027) -- 셀에 안 붙은
      // 측정도 묶일 수 있고, `*_effective` 가 "자기 것 → 셀 것" 을 이미 편다.
      if (!inGroup(item.group_id_effective ?? null)) return false
      return !needle
        || item.name.toLowerCase().includes(needle)
        || (item.sample_name ?? '').toLowerCase().includes(needle)
    })
  }, [spectra.data, samples.data, search, purpose, sampleId, group.effective, inGroup])

  /** 드롭다운에 올릴 셀 — 스펙트럼이 하나라도 있는 것만. */
  const cells = useMemo(() => {
    const seen = new Map<number, string>()
    for (const item of spectra.data ?? []) {
      if (item.sample_id !== null && item.sample_name) seen.set(item.sample_id, item.sample_name)
    }
    return [...seen].sort((a, b) => a[1].localeCompare(b[1], 'ko'))
  }, [spectra.data])

  // 목록에서 사라진 것을 고른 채로 두면 그래프와 칩이 어긋난다.
  const selected = useMemo(
    () => chosen.filter((id) => rows.some((row) => row.id === id)), [chosen, rows])

  const points = useAsync(
    () => (selected.length ? api.spectraPoints(selected) : Promise.resolve([])),
    [selected.join(',')],
  )

  // 응답이 지금 고른 집합의 것인지.  바꾸는 사이 옛 응답이 남아 있으면 칩은
  // 꺼져 있는데 그래프와 클립보드는 켜진 집합을 말한다.
  const fresh = useMemo(() => {
    const got = (points.data ?? []).map((item) => item.id).sort().join(',')
    return got === [...selected].sort().join(',')
  }, [points.data, selected])

  const areaOf = useCallback(
    (id: number) => rows.find((row) => row.id === id)?.area_cm2_effective ?? null,
    [rows])

  // Ω·cm² 로 볼 때는 면적이 없는 것을 뺀다.  섞으면 두 곡선의 크기 차이가
  // 재료 차이인지 단위 차이인지 볼 방법이 없어진다.
  const shown = useMemo(() => {
    const all = points.data ?? []
    if (unit === 'ohm') return { kept: all, dropped: [] as typeof all }
    const split = splitByArea(all, areaOf)
    return { kept: split.kept.map((item) => scaleSpectrum(item, areaOf(item.id))),
             dropped: split.dropped }
  }, [points.data, unit, areaOf])

  const unitLabel = zUnitLabel(unit)

  // DRT 는 볼 때만 부른다.  스펙트럼마다 한 번씩 푸는 계산이라, 안 보는 동안
  // 부르면 나이퀴스트만 보려던 사람이 그 시간을 대신 낸다.
  const lambda = rememberedLambda()
  const drt = useAsync(
    () => (mode === 'drt' && selected.length
      ? Promise.all(selected.map((id) =>
          api.spectrumDrt(id, { regularisation: lambda, derivative_order: 0 })
            .then((value) => ({ id, value }))
            .catch(() => ({ id, value: null }))))
      : Promise.resolve([])),
    [mode, selected.join(','), lambda],
  )

  // 맞춤 곡선도 볼 때만 부른다.  회로를 다시 푸는 것은 아니지만 (서버가
  // 저장된 파라미터로 계산해 준다) 스펙트럼마다 곡선 하나가 더 오는 응답이라,
  // 나이퀴스트만 보려던 사람이 그 무게를 낼 이유가 없다.
  const fits = useAsync(
    () => (mode === 'fit' && selected.length
      ? api.spectraFits(selected)
      : Promise.resolve([] as SpectrumFit[])),
    [mode, selected.join(',')],
  )

  /** 이 스펙트럼의 맞춤 곡선.  없으면 `undefined`. */
  const fitOf = useCallback(
    (id: number) => (fits.data ?? []).find((item) => item.spectrum_id === id),
    [fits.data])

  /** 맞춤 곡선을 못 그린 것들.  아직 안 맞췄거나, 맞췄는데 회로를 못 그린
   *  것이다 — 어느 쪽이든 그림에 곡선이 없으므로 이름을 적는다. */
  const unfitted = useMemo(() => {
    if (mode !== 'fit' || fits.loading) return [] as Spectrum[]
    return rows.filter((row) => {
      if (!selected.includes(row.id)) return false
      const fit = fitOf(row.id)
      return !fit?.fitted_z_re || !fit.fitted_z_im
    })
  }, [mode, fits.loading, fitOf, rows, selected])

  const series = useMemo<PlotSeries[]>(() => {
    if (!fresh) return []
    if (mode === 'drt') {
      return (drt.data ?? []).flatMap(({ id, value }) => {
        if (!value) return []
        const area = unit === 'ohmcm2' ? areaOf(id) : null
        if (unit === 'ohmcm2' && !area) return []
        const row = rows.find((one) => one.id === id) ?? ({} as Spectrum)
        return [{
          label: label(row),
          // SOC 스캔이면 그 스윕이 어느 상태였는지.  `#3` 만으로는 순서밖에
          // 모르는데, 곡선을 읽는 사람이 보는 것은 순서가 아니라 SOC 다.
          note: (isScan(row) ? sweepAt(row) : '') || undefined,
          // γ 는 log₁₀ τ 위에서 읽는 것이다 — 선형 τ 로 그리면 고주파 봉우리
          // 열 개가 왼쪽 끝 한 점에 겹친다.
          x: value.tau_s.map((tau) => tauAxisValue(tau)),
          y: value.gamma_ohm.map((gamma) => (area ? gamma * area : gamma)),
          color: seriesColor(rows.findIndex((one) => one.id === id)),
          width: 1.5,
        }]
      })
    }
    return shown.kept.flatMap((item) => {
      const index = rows.findIndex((one) => one.id === item.id)
      const row = rows[index] ?? ({} as Spectrum)
      const name = label(row)
      const { x, y } = nyquistXy(item.z_re, item.z_im, dropInductive)
      const measured: PlotSeries = {
        label: name,
        note: (isScan(row) ? sweepAt(row) : '') || undefined,
        x,
        y,
        color: seriesColor(index),
        points: true,
        // 맞춤을 볼 때는 실측이 **점**이라야 한다.  선으로 두면 두 선이
        // 겹쳐서 어느 쪽이 모델이고 어느 쪽이 잰 것인지 안 보인다.
        width: mode === 'fit' ? 0 : 1,
      }
      if (mode !== 'fit') return [measured]

      const fit = fitOf(item.id)
      if (!fit?.fitted_z_re || !fit.fitted_z_im) return [measured]
      // 서버가 같은 회로 AST 로 계산한 곡선이다 — 화면은 회로를 다시 해석하지
      // 않는다.  맞춤 곡선도 실측과 같은 규칙으로 자른다: 회로에 L 이 있으면
      // 이 곡선도 고주파에서 유도성이라, 측정만 자르면 맞춤선 혼자 밑으로
      // 꽂힌다.
      const area = unit === 'ohmcm2' ? areaOf(item.id) : null
      const curve = nyquistXy(fit.fitted_z_re, fit.fitted_z_im, dropInductive,
                              (value) => perArea(value, area))
      return [measured, {
        label: `${name} fitting`,
        note: fit.circuit,
        x: curve.x,
        y: curve.y,
        color: seriesColor(index),
        width: 2,
        // 실측과 같은 색이라 짝이 보이고, 파선이라 어느 쪽이 모델인지 보인다.
        dash: [6, 4],
      }]
    })
  }, [shown, fresh, rows, dropInductive, mode, drt.data, unit, areaOf, fitOf])

  // 겹쳐 놓으면 한 스펙트럼의 유도성 꼬리가 다른 것들의 아크까지 납작하게
  // 만든다 — 세로 눈금은 하나이기 때문이다.  몇 점이 빠졌는지는 적는다.
  const inductive = useMemo(
    () => (points.data ?? []).reduce((sum, item) => sum + inductiveCount(item.z_im), 0),
    [points.data])

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>EIS 비교</h1>
          <div className="sub">
            셀을 가리지 않고 골라 한 그림에 — 서로 다른 셀의 같은 시점을
            나란히 놓는 자리입니다
          </div>
        </div>
      </div>

      {spectra.error ? <Alert kind="error">{spectra.error}</Alert> : null}
      {spectra.loading && !spectra.data ? <Spinner /> : null}

      {selected.length ? (
        <Card title="고른 것" tight>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left' }}>이름</th>
                  <th style={{ textAlign: 'left' }}>관계셀</th>
                  <th style={{ textAlign: 'left' }}>목적</th>
                  <th>사이클</th>
                  <th>점</th>
                  <th>면적 (cm²)</th>
                  <th>χ²</th>
                  <th style={{ textAlign: 'left' }}>회로</th>
                  {/* 피팅이 없는 스펙트럼은 회로 칸이 비는데, 그 빈칸은
                      "안 맞췄다" 와 "맞췄는데 못 읽었다" 를 구분해 주지
                      않는다.  말로 적는다 (§0.4). */}
                  <th style={{ textAlign: 'left' }}>fitting</th>
                  {/* 이 임피던스가 어느 충방전 곡선 옆에서 나온 것인지.  두
                      섹션은 따로 서지만 셀 하나로 이어져 있다 (ADR 0024). */}
                  <th style={{ textAlign: 'left' }}>충방전</th>
                </tr>
              </thead>
              <tbody>
                {rows.filter((row) => selected.includes(row.id)).map((row) => (
                  <tr key={row.id}>
                    <td className="text">
                      <Link to={`/eis/${row.id}`}>{row.name}</Link>
                      {/* 스캔은 스무 줄이 같은 이름이라, 번호가 없으면 표에서
                          어느 줄이 어느 곡선인지 짚을 수가 없다. */}
                      {isScan(row) ? (
                        <span className="tiny faint">
                          {' '}#{row.sweep_index ?? '?'}
                          {sweepAt(row) ? ` · ${sweepAt(row)}` : ''}
                        </span>
                      ) : null}
                    </td>
                    <td className="text dim">
                      {row.sample_id === null
                        ? '—'
                        : <Link to={`/samples/${row.sample_id}`}>{row.sample_name}</Link>}
                    </td>
                    <td className="text dim">{row.purpose || '—'}</td>
                    <td>{row.at_cycle === null ? '—' : row.at_cycle}</td>
                    <td className={row.area_cm2_effective ? '' : 'faint'}>
                      {row.area_cm2_effective ? num(row.area_cm2_effective, 4) : '없음'}
                    </td>
                    <td>{row.n_points}</td>
                    <td>{row.best_chi_squared === null
                      ? '—' : num(row.best_chi_squared, 3)}</td>
                    <td className="text dim mono">{row.best_circuit || '—'}</td>
                    <td className="text">
                      {row.fit_count ? (
                        <span className="tiny">fitting {row.fit_count}개</span>
                      ) : (
                        <span className="tiny warn">아직 fitting 데이터가 없습니다</span>
                      )}
                    </td>
                    <td className="text">
                      {cellOf(row)?.run_count
                        ? <Link className="tiny" to={`/samples/${row.sample_id}#cycles`}>
                            사이클 {cellOf(row)?.cycle_count}
                          </Link>
                        : <span className="tiny faint">
                            {row.sample_id === null ? '셀 안 붙음' : '충방전 없음'}
                          </span>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      ) : null}

      <Card
        title={MODE_TITLE[mode]}
        actions={
          <div className="row" style={{ gap: 10, alignItems: 'center' }}>
            <div className="segmented" role="group" aria-label="그림">
              <button type="button" className={mode === 'nyquist' ? 'on' : ''}
                      onClick={() => setMode('nyquist')}>나이퀴스트</button>
              <button type="button" className={mode === 'fit' ? 'on' : ''}
                      onClick={() => setMode('fit')}>fitting</button>
              <button type="button" className={mode === 'drt' ? 'on' : ''}
                      onClick={() => setMode('drt')}>DRT</button>
            </div>
            <div className="segmented" role="group" aria-label="단위">
              <button type="button" className={unit === 'ohm' ? 'on' : ''}
                      onClick={() => setUnit('ohm')}>{zUnitLabel('ohm')}</button>
              <button type="button" className={unit === 'ohmcm2' ? 'on' : ''}
                      onClick={() => setUnit('ohmcm2')}>{zUnitLabel('ohmcm2')}</button>
            </div>
          </div>
        }
      >
        {/* 클립보드는 **지금 보이는 그림**만 켠다.  안 보이는 것을 복사할 수
            있으면 사람은 방금 본 것을 복사했다고 믿는다 — 붙여 넣기 전까지
            티가 안 나고, 그때는 이 화면을 떠난 뒤다. */}
        <CopyBar
          items={[
            {
              label: '나이퀴스트',
              title: mode === 'nyquist'
                ? `스펙트럼마다 Z′·−Z″ 두 열 (${unitLabel})`
                : `${MODE_TITLE[mode]} 를 보고 있습니다 — 나이퀴스트로 바꾸면 켜집니다`,
              disabled: mode !== 'nyquist' || !fresh || !shown.kept.length,
              // 열마다 어느 스펙트럼인지.  열 한 쌍이 저마다 다른 셀이라
              // 워크시트 안에는 그것을 적을 자리가 없다.
              build: () => nyquistWideTsv(shown.kept, undefined,
                                          { x: `Z′ (${unitLabel})`, y: `−Z″ (${unitLabel})` }),
              skipped: shown.dropped.length,
              skippedNote: (n) => `면적이 없어 ${n}개를 뺐습니다`,
            },
            {
              label: 'fitting',
              // 실측과 맞춤이 **번갈아** 나온다 (측정 Z′·−Z″, 맞춤 Z′·−Z″).
              // 맞춤만 내면 Origin 에서 무엇에 맞춘 곡선인지 알 수 없고, 그
              // 판단이 이 그림을 보는 이유다.
              title: mode === 'fit'
                ? `스펙트럼마다 측정·fitting Z′·−Z″ 네 열 (${unitLabel})`
                : `${MODE_TITLE[mode]} 를 보고 있습니다 — fitting 으로 바꾸면 켜집니다`,
              disabled: mode !== 'fit' || !fresh || !series.length,
              build: () => seriesWideTsv(series,
                                         { x: `Z′ (${unitLabel})`, y: `−Z″ (${unitLabel})` }),
              skipped: unfitted.length,
              skippedNote: (n) => `아직 fitting 데이터가 없어 ${n}개는 fitting 열이 없습니다`,
            },
            {
              label: 'γ(τ)',
              title: mode === 'drt'
                ? `스펙트럼마다 ${TAU_AXIS_SHORT}·γ 두 열 (${unitLabel})`
                : `${MODE_TITLE[mode]} 를 보고 있습니다 — DRT 로 바꾸면 켜집니다`,
              disabled: mode !== 'drt' || !series.length,
              build: () => seriesWideTsv(series,
                                         { x: TAU_AXIS_LABEL, y: `γ (${unitLabel})` }),
            },
          ]}
        />

        {/* 면적이 없어 빠진 것은 **이름을 적는다.**  말 없이 빼면 그 스펙트럼은
            화면에서 그냥 사라지고, 사라진 것은 아무 표시도 안 남긴다 (§0.4). */}
        {unit === 'ohmcm2' && shown.dropped.length ? (
          <Alert kind="warn">
            면적이 적혀 있지 않아 {shown.dropped.length}개를 뺐습니다 —{' '}
            {shown.dropped.map((item) =>
              rows.find((row) => row.id === item.id)?.name ?? `#${item.id}`).join(' · ')}.
            <span className="tiny faint">
              {' '}면적을 모르는 채로 같은 눈금에 얹으면 두 곡선의 크기 차이가
              재료 차이인지 단위 차이인지 볼 수 없습니다. 스펙트럼 상세에서
              면적이나 지름을 적어 주세요.
            </span>
          </Alert>
        ) : null}
        {/* 맞춤이 없는 것도 **이름을 적는다.**  실측 점은 그대로 그려지므로
            곡선만 조용히 빠지는데, 그 그림은 "이 셀은 잘 맞았다" 처럼 보인다. */}
        {mode === 'fit' && unfitted.length ? (
          <Alert kind="warn">
            아직 fitting 데이터가 없습니다 —{' '}
            {unfitted.map((item) => item.name).join(' · ')}.
            <span className="tiny faint">
              {' '}실측 점은 그대로 그렸습니다. 스펙트럼 상세에서 회로를 골라
              fitting 하면 이 그림과 클립보드에 곡선이 함께 나옵니다.
            </span>
          </Alert>
        ) : null}
        {fits.error ? <Alert kind="error">{fits.error}</Alert> : null}
        {points.error ? <Alert kind="error">{points.error}</Alert> : null}
        {!selected.length ? (
          // 빈 그래프는 고장처럼 보인다.
          <div className="tiny faint" style={{ padding: 12 }}>
            아래 목록에서 스펙트럼을 골라 주세요.
          </div>
        ) : points.loading && !points.data ? (
          <Spinner />
        ) : series.length ? (
          <>
            {mode === 'drt' ? (
              // DRT 는 두 축의 뜻이 달라서 `equalAspect` 가 없다 — 가로는
              // 로그 초, 세로는 저항이다.
              <Plot series={series} xLabel={TAU_AXIS_LABEL}
                    yLabel={`γ (${unitLabel})`}
                    height={380} legend busy={drt.loading} />
            ) : (
              <Plot series={series} xLabel={`Z′ (${unitLabel})`}
                    yLabel={`−Z″ (${unitLabel})`}
                    height={380} legend equalAspect positiveFit
                    busy={points.loading || fits.loading || !fresh} />
            )}
            {mode === 'fit' ? (
              <div className="tiny faint" style={{ padding: '6px 0 0' }}>
                점이 측정, 파선이 fitting 입니다 — 같은 색이 한 쌍이고, 회로 이름은
                범례에 붙어 있습니다. 스펙트럼마다 가장 잘 맞은 것
                하나(χ² 최소)를 그립니다. fitting 한 주파수 구간 안에서만 그리므로,
                구간을 좁혀 맞췄으면 곡선이 실측보다 짧습니다.
              </div>
            ) : null}
            {mode === 'drt' ? (
              <div className="tiny faint" style={{ padding: '6px 0 0' }}>
                벌점 λ = {lambda.toExponential(2)} · 평활 차수 0 — 스펙트럼
                상세에서 옮긴 값을 그대로 씁니다. 두 화면이 다른 λ 를 쓰면 같은
                γ 가 다르게 생겨서, 나란히 놓는 이 화면이 곧바로 어긋납니다.
              </div>
            ) : null}
            {inductive ? (
              <label className="row small" style={{ gap: 6, padding: '8px 0 0' }}>
                <input
                  type="checkbox"
                  checked={dropInductive}
                  onChange={(event) => setDropInductive(event.target.checked)}
                  style={{ width: 'auto' }}
                />
                <span>
                  실수축 위의 점 {inductive}개 빼기
                  <span className="tiny faint">
                    {' '}— 고주파에서 Z″ 가 양수인 구간 (케이블·셀 홀더의
                    인덕턴스). 끄면 아크 밑으로 수직선이 되어 꽂히고, 세로
                    눈금이 늘어나 모든 아크가 납작해집니다.
                  </span>
                </span>
              </label>
            ) : null}
          </>
        ) : null}
      </Card>

      {/* 세 비교 화면이 같은 고르개를 쓴다 (`PickGrid`).  한 화면에서 익힌
          손이 다른 화면에서 통해야 한다 -- 예전에는 여기만 칩 줄이라
          "모두 선택" 이 없었고, 고른 수도 제목에 안 나왔다.

          그림 **밑**에 둔다.  고르개는 스펙트럼이 늘수록 아래로 자라는데,
          위에 있으면 그만큼 그림이 화면 밖으로 밀린다 -- 스무 개쯤 쌓이면
          비교하러 온 사람이 매번 스크롤부터 해야 한다. */}
      <PickGrid
        title="스펙트럼 선택"
        group={group}
        groupHint="이 측정 또는 붙은 셀의 묶음"
        limit={OVERLAY_LIMIT}
        limitNote={`한 번에 ${OVERLAY_LIMIT}개까지만 겹쳐 그립니다 — 하나를 꺼야 다른 것을 켤 수 있습니다.`}
        items={rows.map((row, index) => {
          const common = [row.kind === 'solid' ? '전고체' : '액체', row.purpose,
                          row.sample_name ? `셀: ${row.sample_name}` : null]
            .filter(Boolean).join(' · ')
          // **SOC 스캔은 파일 하나로 접는다.**  스윕 스물이 이름도 대역도
          // 회로도 같아서, 펴 두면 고르개가 그 파일 하나로 가득 찬다.  펴면
          // 스윕을 하나씩 켤 수 있다 — SOC 별 나이퀴스트는 스윕마다 다른
          // 곡선이고, 그중 셋을 겹쳐 보는 것이 이 화면의 쓰임이다.
          const scan = isScan(row)
          return {
            id: row.id,
            // 접힌 안에서는 파일 이름이 머리말 줄에 이미 있다.  줄마다 되풀이하면
            // 정작 서로 다른 것(스윕 번호와 SOC)이 잘려 안 보인다.
            name: scan ? `#${row.sweep_index ?? '?'}` : label(row),
            note: scan ? sweepAt(row) : common,
            // fitting 이 있는지는 **고르기 전에** 알아야 한다.  골라 놓고
            // 그림에서 "이건 곡선이 없네" 를 발견하면 다시 내려와야 한다.
            done: row.fit_count > 0,
            doneNote: 'fitting 완료',
            color: seriesColor(index),
            fold: scan
              ? { key: row.sha256, label: fileLabel(row), note: common }
              : undefined,
          }
        })}
        picked={selected}
        onChange={setChosen}
        empty={(
          <Empty title="고를 스펙트럼이 없습니다" icon="∿">
            <Link to="/eis/upload">업로드</Link>에서 올려 주세요.
          </Empty>
        )}
        extra={
          <>
            <Field label="관계셀" hint="이 측정이 붙어 있는 충방전 셀">
              <select
                aria-label="관계셀"
                value={sampleId ?? ''}
                onChange={(event) =>
                  setSampleId(event.target.value ? Number(event.target.value) : null)}
              >
                <option value="">전체</option>
                {cells.map(([id, name]) => (
                  <option key={id} value={id}>{name}</option>
                ))}
              </select>
            </Field>
            <Field label="목적" hint={purposes.length ? `${purposes.length}가지` : '아직 없음'}>
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
            <Field label="전해질">
              <select
                aria-label="전해질"
                value={kind}
                onChange={(event) => setKind(event.target.value as EisKind | '')}
              >
                <option value="">전체</option>
                <option value="liquid">액체</option>
                <option value="solid">전고체</option>
              </select>
            </Field>
            <Field label="검색" hint="이름 · 셀">
              <input
                aria-label="검색"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />
            </Field>
          </>
        }
      />

    </main>
  )
}
