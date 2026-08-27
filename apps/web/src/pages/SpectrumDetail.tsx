/** 스펙트럼 하나 — 나이퀴스트, 보드, 등가회로 피팅, 파라미터.
 *
 *  절차서의 순서를 그대로 두되 사람만 뺐다: 회로를 고르고 누르면 초기값을
 *  데이터에서 만들어 여러 번 맞추고, 파라미터와 χ² 와 **신뢰구간**을 낸다.
 *  마지막 것이 이 화면의 이유다 — 수렴한 피팅이 곧 측정은 아니고, 오차가 값을
 *  삼킨 파라미터는 숫자처럼 보일 뿐이다 (ADR 0019 §7).
 */

import { OtherMeasurements } from '../components/OtherMeasurements'
import { RelatedCellCard } from '../components/RelatedCell'
import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { CopyBar } from '../components/CopyBar'
import { DrtPanel } from '../components/DrtPanel'
import { ParamName, ParamText } from '../components/ParamName'
import { EditableName } from '../components/EditableName'
import { Plot, type PlotSeries } from '../components/Plot'
import { Alert, Card, Field, KeyValues, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { areaUnit, perArea, scalesWithArea } from '../lib/areanorm'
import {
  Z_UNITS, Z_UNIT_KEY, type ZUnit, areaFor, validZUnit, zUnitLabel,
} from '../lib/zunit'
import { cellConfigFromName, dateTime, num, seriesColor, thicknessFromName }
  from '../lib/format'
import { inductiveCount, nyquistXy } from '../lib/eis'
import { isHeadline, paramMeaning } from '../lib/params'
import { bodeTsv, fitParametersTsv, nyquistTsv } from '../lib/origin'
import { useAsync, useStickyState } from '../lib/hooks'
import type {
  CellConfig, CircuitKind, CircuitPreset, EisKind, Spectrum,
  SpectrumDetail as Detail, SpectrumFit,
} from '../lib/types'
import { frequencySpan, hertz } from './Eis'

const KIND_LABEL: Record<EisKind, string> = { liquid: '액체 전해질', solid: '전고체' }

export function SpectrumDetail() {
  const params = useParams<{ id: string }>()
  const id = Number(params.id)

  const [circuit, setCircuit] = useState('')
  const [dropInductive, setDropInductive] = useState(true)
  // 맞출 주파수 창.  ZView 가 늘 하는 것이고 (ADR 0029), 여기서는 저주파 끝에
  // 오차가 몰릴 때 그것이 회로 탓인지 스윕이 일찍 끝난 탓인지를 사람이 직접
  // 재보는 자리다 — 빈 칸은 "끝까지" 다.
  const [fitLow, setFitLow] = useState('')
  const [fitHigh, setFitHigh] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [reloadKey, bumpReload] = useState(false)
  const [showFit, setShowFit] = useState<number | null>(null)

  const spectrum = useAsync(() => api.getSpectrum(id), [id, reloadKey])
  const points = useAsync(() => api.spectrumPoints(id), [id])
  const circuits = useAsync(() => api.eisCircuits(), [])
  // 관계셀 드롭다운이 쓸 목록.  아래 카드가 이 화면에서 붙이거나 뗄 수 있게.
  const allSamples = useAsync(() => api.listSamples(), [])

  const record = spectrum.data
  const kinds: CircuitKind[] = circuits.data?.kinds ?? []
  // 회로 프리셋은 **여섯 조합**을 따른다 (액체/전고체 × 풀셀·하프셀·대칭셀).
  // 아크의 이름이 이미 이 축에서 갈리므로 회로도 같이 갈린다 — 리튬 대극
  // 하프셀은 대극 계면이 아크를 하나 더 얹고, 대칭셀은 아크가 두 배다.
  const combinations = circuits.data?.combinations ?? []
  const presets: CircuitPreset[] =
    combinations.find(
      (entry) => entry.kind === record?.kind && entry.cell_config === record?.cell_config,
    )?.presets
    ?? kinds.find((entry) => entry.kind === record?.kind)?.presets
    ?? []
  const chosenCircuit = circuit || record?.last_circuit || presets[0]?.circuit || ''

  // `record?.fits ?? []` 를 그대로 두면 매 렌더마다 새 배열이라 아래 useMemo 가
  // 절대 재사용되지 않는다 — 그래프가 마우스를 움직일 때마다 다시 그려진다.
  const fits = useMemo(() => record?.fits ?? [], [record])
  const fit = useMemo(
    () => fits.find((item) => item.id === showFit) ?? fits[0] ?? null,
    [fits, showFit],
  )

  /** Ω 인가 Ω·cm² 인가 — 그리고 실제로 나눌 면적.
   *
   *  같은 전극이라도 지름 10 mm 와 16 mm 는 저항이 2.5 배 다르다.  셀끼리
   *  비교하려면 면적으로 나눈 값이라야 하고, 논문의 값도 대개 그것이다.
   *  그런데 **계측기가 준 수는 Ω 다** — ZView 결과와 대조하거나 이 셀 하나의
   *  사이클 변화만 볼 때는 안 나눈 쪽이 맞다.  그래서 고르게 두고, 고른 것은
   *  비교 화면과 **같은 열쇠**로 이 브라우저에 남는다 (`lib/zunit.ts`): 같은
   *  R₀ 가 한 화면에서 15.6, 다른 화면에서 12.3 으로 나오면 두 수가 다른
   *  단위라는 말이 축 이름에만 남고, 눈은 축까지 안 간다.
   *
   *  **모르면 안 나눈다** — 추정 면적으로 나눈 수는 실측 ASR 과 똑같이 생겼다
   *  (§0.4).  `areaFor` 가 그때 `null` 을 주고 화면은 Ω 로 그리면서 왜인지를
   *  적는다.  한 번 정해진 이 값이 네 곳을 한꺼번에 움직인다: 나이퀴스트,
   *  보드의 |Z|, 피팅 파라미터의 저항들, 그리고 DRT.
   */
  const cellArea = record?.area_cm2_effective ?? null
  //: 방금 저장한 값이 같은 파일의 스윕 몇 개까지 갔는지.  저장할 때만 뜬다.
  const [spread, setSpread] = useState<string | null>(null)
  //: 방금 한 일의 결과 한 줄 (스캔 전부 맞추기의 수렴 수 같은 것).
  const [note, setNote] = useState<string | null>(null)
  const [storedZUnit, setZUnit] = useStickyState<ZUnit>(Z_UNIT_KEY, 'ohmcm2')
  const zPick = validZUnit(storedZUnit, 'ohmcm2')
  const area = areaFor(zPick, cellArea)
  const zUnit = zUnitLabel(area ? 'ohmcm2' : 'ohm')

  const nyquist = useMemo<PlotSeries[]>(() => {
    if (!points.data) return []
    // 세로축은 −Z″ 다.  허수부를 그대로 그리면 아크가 아래로 뒤집혀서,
    // 파일이 왜 −Im(Z) 를 저장하는지가 화면에서 되풀이된다.
    const measured = nyquistXy(points.data.z_re, points.data.z_im, dropInductive,
                               (value) => perArea(value, area),
                               points.data.frequency_hz)
    const series: PlotSeries[] = [{
      label: '측정',
      x: measured.x,
      y: measured.y,
      color: seriesColor(0),
      points: true,
      width: 0,
    }]
    if (fit?.converged && fit.fitted_z_re && fit.fitted_z_im) {
      // 서버가 같은 회로 AST 로 계산한 곡선이다.  화면이 파라미터 이름으로
      // 회로를 재구성하던 때는 L·Ws·Wo·중첩이 조용히 빠져 다른 곡선이
      // "맞춤" 으로 그려졌다 (리뷰 #6).  서버가 곡선을 못 주면 선을 그리지
      // 않고 이유(fitted_note)를 아래에 적는다.
      // 맞춤 곡선도 같은 규칙으로 자른다.  회로에 L 이 있으면 이 곡선도
      // 고주파에서 유도성이라, 측정만 자르면 맞춤선 혼자 밑으로 꽂힌다.
      const fitted = nyquistXy(fit.fitted_z_re, fit.fitted_z_im, dropInductive,
                               (value) => perArea(value, area),
                               fit.fitted_frequency_hz ?? undefined)
      series.push({
        label: `fitting (${fit.circuit})`,
        x: fitted.x,
        y: fitted.y,
        color: seriesColor(1),
        width: 2,
      })
    }
    return series
  }, [points.data, fit, area, dropInductive])

  const inductive = useMemo(
    () => (points.data
      ? inductiveCount(points.data.z_im, points.data.frequency_hz) : 0),
    [points.data])

  // 보드는 두 패널이다 (리뷰 #27).  8 decade 의 주파수를 선형 x 에 놓으면
  // 10 kHz 아래 전부가 폭 1% 에 뭉치고, Ω 와 도(°)를 한 선형 y 에 겹치면
  // 위상이 바닥에 눕는다 — 내보내기 코드가 이미 "두 y 단위는 쌓을 수 없다"
  // 라고 말하는 그대로다.  x 는 log₁₀ f, |Z| 도 decade 를 넘나드니 log₁₀.
  const bodeMagnitude = useMemo<PlotSeries[]>(() => {
    if (!points.data) return []
    return [
      {
        label: `log₁₀|Z| (${zUnit})`,
        x: points.data.frequency_hz.map((value) => Math.log10(value)),
        // |Z| 도 임피던스라 같이 나눈다.  위상은 무차원이라 그대로다.
        y: points.data.magnitude.map((value) => Math.log10(perArea(value, area))),
        color: seriesColor(0),
        points: true,
        width: 1,
      },
    ]
  }, [points.data, area, zUnit])
  const bodePhase = useMemo<PlotSeries[]>(() => {
    if (!points.data) return []
    return [
      {
        label: '위상 (°)',
        x: points.data.frequency_hz.map((value) => Math.log10(value)),
        y: points.data.phase_deg,
        color: seriesColor(2),
        points: true,
        width: 1,
      },
    ]
  }, [points.data])

  // 잰 대역 — 빈 칸의 자리표시로 쓴다.  "비우면 끝까지" 가 어디까지인지를
  // 숫자로 보여 주면 창을 좁힐 때 무엇을 잘라내는지가 보인다.
  const measured = useMemo(() => {
    const f = points.data?.frequency_hz
    if (!f?.length) return null
    return { low: Math.min(...f), high: Math.max(...f) }
  }, [points.data])

  // 추천 하한·상한.  **마지막으로 맞춘 결과**에서 나온다 — 저주파 끝에
  // 오차가 몰렸는지는 맞춰 봐야 알 수 있는 것이라, 첫 피팅 전에는 하한 추천이
  // 없다 (상한은 유도성 점만 보면 되므로 늘 있다).
  const suggestion = useMemo(() => {
    const seen = (record?.fits ?? []).find((item) => item.id === showFit)
      ?? (record?.fits ?? [])[0]
    return {
      low: seen?.suggested_low_hz ?? null,
      drops: seen?.suggested_low_drops ?? 0,
      high: seen?.suggested_high_hz ?? null,
    }
  }, [record?.fits, showFit])

  /** 이 스펙트럼이 SOC 스캔의 한 스윕인가.  그렇다면 맞추기는 **스캔 단위**가
   *  기본이다 — 한 파일이고 한 셀이라 1번에 맞는 회로가 나머지에도 맞는
   *  회로이고, 스윕 열하나를 하나씩 맞추는 것이 이 화면이 생긴 이유였다. */
  const sweeps = record?.sweep_count ?? 1
  const isScanSweep = sweeps > 1

  /** 스캔의 스윕 전부를 지금 고른 회로로.
   *
   *  **상한은 서버가 스윕마다 따로 잡는다** (유도성 위쪽 끝).  한 파일 안에서도
   *  유도성 꼬리의 길이가 스윕마다 달라서, 이 화면의 상한 칸을 열한 개에
   *  그대로 쓰면 어떤 스윕은 셀을 버리고 어떤 스윕은 배선을 남긴다.
   *  **하한은 안 정한다** — 저주파 끝의 어긋남은 맞춰 봐야 아는 것이라
   *  맞추기 전에 그은 하한은 근거 없이 데이터를 버리는 것이다.
   */
  async function runScanFit() {
    if (!record?.sha256) return
    setBusy(true)
    setError(null)
    setNote(null)
    try {
      const low = Number(fitLow)
      const high = Number(fitHigh)
      const out = await api.fitScan(record.sha256, {
        circuit: chosenCircuit || undefined,
        // **화면의 설정을 그대로 보낸다.**  전에는 회로만 보내고 나머지는
        // 서버 기본값이 쓰였다: 바로 위의 '유도성 점 빼기' 체크박스와 두 주파수
        // 칸이 아무 일도 안 했고, 1–100 Hz 로 좁혀 놓고 이 단추를 누른 사람은
        // 전 대역으로 맞춘 결과를 같은 이름으로 받았다 (Codex #4).
        drop_inductive: dropInductive,
        ...(fitLow.trim() && Number.isFinite(low) && low > 0
          ? { frequency_low_hz: low } : {}),
        ...(fitHigh.trim() && Number.isFinite(high) && high > 0
          ? { frequency_high_hz: high } : {}),
        // 상한을 안 적었을 때만 스윕마다 자동으로 잡는다.
        auto_high: true,
      })
      const parts = [`스윕 ${out.converged}/${out.requested}개 수렴`]
      // 성공만 세면 반쯤 실패한 배치가 작은 배치로 읽힌다.
      if (out.failed.length) parts.push(`${out.failed.length}개 실패`)
      // 맞추기 전에 조건을 한 번 맞춘다 (1번 스윕 기준).  말없이 고치지 않는다.
      if (out.synced) parts.push(`조건을 ${out.synced}개 스윕에 함께 맞췄습니다`)
      setNote(parts.join(' · '))
      // 이제 스윕 전부가 같은 면적을 갖는다 — 그러면 Ω·cm² 로 볼 수 있다.
      if (cellArea) setZUnit('ohmcm2')
      if (out.failed.length) {
        setError(out.failed.map((row) => `#${row.spectrum_id}: ${row.detail}`).join('\n'))
      }
      const mine = out.fitted.find((one) => one.spectrum_id === record.id)
      if (mine) setShowFit(mine.id)
      bumpReload((value) => !value)
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause))
    } finally {
      setBusy(false)
    }
  }

  // 추천 하한·상한을 **자동으로 채운다.**  전에는 두 칸이 비어 있고 그 아래
  // '추천 345 kHz' 단추를 눌러야 들어갔다 — 매번 두 번 누르는 일이고, 안 누른
  // 채로 맞추면 유도성 꼬리가 첫 아크를 끌어당긴 결과가 나온다.
  //
  // **손으로 고친 칸은 안 건드린다.**  덮어쓰면 좁혀 놓은 창이 다음 피팅에서
  // 조용히 원래대로 돌아가고, 그 차이는 결과에만 나타난다.
  const [touchedLow, setTouchedLow] = useState(false)
  const [touchedHigh, setTouchedHigh] = useState(false)
  useEffect(() => {
    if (!touchedLow && suggestion.low !== null) setFitLow(String(suggestion.low))
  }, [suggestion.low, touchedLow])
  useEffect(() => {
    if (!touchedHigh && suggestion.high !== null) setFitHigh(String(suggestion.high))
  }, [suggestion.high, touchedHigh])

  async function runFit(mode?: 'auto') {
    if (!record) return
    setBusy(true)
    setError(null)
    try {
      const low = Number(fitLow)
      const high = Number(fitHigh)
      const made = await api.fitSpectrum(record.id, {
        circuit: mode === 'auto' ? 'auto' : (chosenCircuit || undefined),
        drop_inductive: dropInductive,
        // 숫자로 읽히는 것만 보낸다.  빈 칸과 오타가 0 Hz 로 둔갑하면
        // 창이 조용히 넓어지고, 그 차이는 결과에만 나타난다.
        ...(fitLow.trim() && Number.isFinite(low) && low > 0
          ? { frequency_low_hz: low } : {}),
        ...(fitHigh.trim() && Number.isFinite(high) && high > 0
          ? { frequency_high_hz: high } : {}),
      })
      setShowFit(made.id)
      bumpReload((value) => !value)
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause))
    } finally {
      setBusy(false)
    }
  }

  if (spectrum.error) return <main className="page"><Alert kind="error">{spectrum.error}</Alert></main>
  if (!record) return <main className="page"><Spinner label="불러오는 중" /></main>

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          {/* 제목이 그냥 글자라 눌러도 아무 일이 없었다 — 이름을 고치려면
              목록으로 돌아가야 했다.  셀 화면과 같은 부품, 같은 규칙. */}
          <EditableName
            name={record.name}
            label="스펙트럼 이름"
            onSave={async (name) => {
              await api.updateSpectrum(record.id, { name })
              bumpReload((value) => !value)
            }}
          />
          <div className="sub">
            {[
              KIND_LABEL[record.kind],
              record.at_cycle === null
                ? null
                : record.at_cycle === 0 ? '구동 전' : `${record.at_cycle} 사이클`,
              `${record.n_points}점`,
              frequencySpan(record),
              record.device || null,
              record.amplitude_mv ? `${record.amplitude_mv} mV` : null,
            ]
              .filter(Boolean)
              .join('  ·  ')}
          </div>
        </div>
        <span className="spacer" />
        <div className="row">
          {/* 스캔의 한 스윕이면 **형제들이 있는 자리**로 가는 길이 먼저다 —
              이 화면은 그중 하나이고, 나머지 열은 여기서 안 보인다. */}
          {record.sweep_count && record.sweep_count > 1 ? (
            <Link className="link-btn" to={`/scans/${record.sha256}`}>
              스캔 · 스윕 {record.sweep_count}개
            </Link>
          ) : null}
          {/* 여러 개를 한 회로로 한꺼번에 맞추는 자리.  스캔이 아니어도
              쓸모가 있다 (같은 셀의 사이클별 스펙트럼을 한 번에). */}
          <Link className="link-btn" to="/eis/spectra">
            여러 개 한꺼번에 맞추기
          </Link>
          <Link className="link-btn" to="/eis">
            목록
          </Link>
          {record.sample_id ? (
            <Link className="link-btn" to={`/samples/${record.sample_id}`}>
              셀 {record.sample_name}
            </Link>
          ) : null}
        </div>
      </div>

      {error ? <Alert kind="error">{error}</Alert> : null}
      {note ? <Alert kind="info">{note}</Alert> : null}
      {/* 스윕 전파는 **조용히 넘어갈 일이 아니다** — 열한 줄이 함께 바뀐다. */}
      {spread ? <Alert kind="info">{spread}</Alert> : null}

      <div style={{ marginBottom: 14 }}>
        <RelatedCellCard
          sampleId={record.sample_id}
          sampleName={record.sample_name}
          samples={allSamples.data ?? []}
          record={record}
          onSaveConditions={async (body) => {
            await api.updateSpectrum(record.id, body)
            bumpReload((value) => !value)
          }}
          onPick={async (picked) => {
            // 빈 값은 떼어내기다 -- `sample_id: null` 은 "안 보냄" 과 구별되지
            // 않아 서버가 clear 를 따로 받는다.
            await api.updateSpectrum(record.id, picked
              ? { sample_id: picked }
              : { clear: ['sample_id'] })
            bumpReload((value) => !value)
          }}
        />
      </div>

      {/* **단위는 화면 하나에 하나다.**  나이퀴스트·보드·파라미터 표·DRT 가 다
          이것을 따라가고, 클립보드도 따라간다 — 보는 수와 붙여 넣는 수가 다르면
          어느 쪽이 맞는지 확인하는 데 왕복이 든다.  그래서 그림마다 두지 않고
          여기 한 줄에 둔다 (GITT 상세의 가로축 고르개와 같은 모양). */}
      <div className="row" style={{ gap: 6, marginBottom: 10 }}>
        <span className="tiny faint">임피던스 단위</span>
        <div className="segmented" role="group" aria-label="임피던스 단위">
          {Z_UNITS.map((one) => (
            <button
              key={one}
              type="button"
              className={zPick === one ? 'on' : ''}
              // 면적이 없으면 Ω·cm² 는 **누를 수 없다.**  누르게 두면 아무 일도
              // 안 일어나거나, 더 나쁘게는 안 나눈 수에 `Ω·cm²` 만 붙는다.
              disabled={one === 'ohmcm2' && !cellArea}
              title={one === 'ohmcm2' && !cellArea
                ? '면적이 적혀 있지 않습니다 — 아래 "측정 정보" 에서 면적이나 지름을 적어 주세요'
                : undefined}
              onClick={() => setZUnit(one)}
            >
              {zUnitLabel(one)}
            </button>
          ))}
        </div>
        {/* 골라 둔 것이 이 스펙트럼에서 안 되면 **말한다.**  말없이 Ω 로
            떨어뜨리면 화면은 Ω·cm² 를 고른 채로 Ω 를 그리고 있게 된다. */}
        {zPick === 'ohmcm2' && !cellArea ? (
          <span className="tiny warn">면적이 없어 Ω 로 그립니다</span>
        ) : null}
        {area ? (
          <span className="tiny faint">
            면적 {num(cellArea, 4)} cm² 로 나눈 값입니다
          </span>
        ) : null}
      </div>

      {/* 절차서의 마지막 단계가 "Copy to clipboard → 엑셀 → Origin" 이다. */}
      <div style={{ marginBottom: 12 }}>
        <CopyBar
          items={[
            {
              label: '나이퀴스트',
              title: `Z′ 와 −Z″ 두 열 (${zUnit}) — Origin 에서 -col(B) 를 다시 할 필요 없다`,
              disabled: !points.data,
              // 화면이 Ω·cm² 로 그리고 있으면 붙여 넣는 열도 Ω·cm² 다.
              build: () => (points.data
                ? nyquistTsv([points.data], (value) => perArea(value, area)) : ''),
            },
            {
              label: '보드',
              title: `주파수 (Hz) · |Z| (${zUnit}) · 위상 (°) 세 열`,
              disabled: !points.data,
              build: () => (points.data
                ? bodeTsv([points.data], (value) => perArea(value, area)) : ''),
            },
            {
              label: 'fitting 파라미터',
              title: '이름 · 값 · 단위 · 1σ — 엑셀에 붙여 넣는 표',
              disabled: !fit?.parameters.length,
              // 화면이 면적으로 나눈 값을 보여 주고 있으면 그 값 그대로
              // 나간다.  보는 수와 붙이는 수가 다르면 어느 쪽이 맞는지
              // 확인하는 데 왕복이 든다.
              build: () => fitParametersTsv(fit?.parameters ?? [], {
                value: (parameter, raw) =>
                  perArea(raw, scalesWithArea(parameter.unit) ? area : null),
                unit: (parameter) => areaUnit(parameter.unit, area),
              }),
            },
          ]}
        />
      </div>

      <div className="grid cols-2">
        <Card title="나이퀴스트">
          {points.error ? (
            <Alert kind="error">{points.error}</Alert>
          ) : nyquist.length ? (
            <Plot
              series={nyquist}
              xLabel={`Z′ (${zUnit})`}
              yLabel={`−Z″ (${zUnit})`}
              height={360}
              legend
              // 반원이 반원으로 보여야 찌그러진 아크를 알아본다.
              equalAspect
              positiveFit
            />
          ) : (
            <Spinner />
          )}
          {/* 뺐으면 뺐다고 적는다 (ADR 0019).  스위치를 여기 또 만들지는
              않는다 -- 아래 피팅 설정의 것과 같은 뜻이고, 둘이 따로 놀면
              그림과 맞춘 곡선이 서로 다른 점 위에 서게 된다. */}
          {inductive ? (
            <div className="tiny faint" style={{ paddingTop: 8 }}>
              {dropInductive
                ? `실수축 위의 점 ${inductive}개를 뺐습니다 — 고주파에서 Z″ 가 `
                  + '양수인 구간 (케이블·셀 홀더의 인덕턴스). 아래 "고주파 유도성 점 '
                  + '빼기" 를 끄면 그대로 보입니다.'
                : `실수축 위에 점 ${inductive}개가 있습니다 — 아크 밑으로 꽂히는 `
                  + '수직선이 그것입니다. 아래 "고주파 유도성 점 빼기" 로 뺄 수 있습니다.'}
            </div>
          ) : null}
        </Card>

        <Card title="보드">
          {bodeMagnitude.length ? (
            <div className="col" style={{ gap: 6 }}>
              <Plot series={bodeMagnitude} xLabel="log₁₀ f (Hz)"
                    yLabel={`log₁₀|Z| (${zUnit})`} height={180} legend />
              <Plot series={bodePhase} xLabel="log₁₀ f (Hz)" yLabel="위상 (°)"
                    height={180} legend />
            </div>
          ) : (
            <Spinner />
          )}
        </Card>
      </div>

      <div className="fit-row" style={{ marginTop: 14 }}>
        {/* 왼쪽 기둥: 이 스펙트럼이 무엇의 것인가.  파라미터 표 바로 옆에
            있어야 "이 값이 어느 셀·어느 면적의 것인가" 를 눈만 옮겨 본다. */}
        <div className="col" style={{ gap: 14 }}>
          <Card title="셀" padSmall>
            <CellFields
              record={record}
              onSaved={(out) => {
                bumpReload((value) => !value)
                if (!out) return
                // **말없이 열한 줄을 고치지 않는다.**  한 스캔은 파일 하나·셀
                // 하나라 지름·면적·그룹이 스윕 전부에 가는 것이 맞지만, 그
                // 사실이 화면 어디에도 없으면 다른 스윕을 열어 본 사람이
                // "내가 안 적었는데 왜 들어 있지" 를 만난다.
                setSpread(out.spread_to_sweeps
                  ? `이 스캔의 다른 스윕 ${out.spread_to_sweeps}개에도 함께 적용했습니다`
                  : null)
                // 면적이 이제 있으면 Ω·cm² 로 올린다.  지름을 적는 이유가
                // 그것이고, 적어 놓고 단추를 또 눌러야 하면 적은 보람이 없다.
                if (!cellArea && out.area_cm2_effective) setZUnit('ohmcm2')
              }}
            />
          </Card>
          <Card title="측정 정보" padSmall>
            <KeyValues
              rows={[
                ['파일', record.original_name || '—'],
                ['형식', record.source_format || '—'],
                ['테크닉', record.technique || '—'],
                ['주파수', frequencySpan(record)],
                ['진폭', record.amplitude_mv ? `${record.amplitude_mv} mV` : '—'],
                ['면적', record.area_cm2_effective
                  ? `${num(record.area_cm2_effective, 4)} cm²` : '—'],
                ['올린 때', dateTime(record.uploaded_at)],
              ]}
            />
            {/* 올린 바이트 그대로 다시 받는 길.  중앙에 모아 두는 이유가
                "각자 노트북에서 원본이 사라지지 않게" 인데, 다시 못 받으면
                올리는 것이 편도 여행이 되고 아무도 원본을 안 맡긴다. */}
            <div className="row" style={{ gap: 10, marginTop: 8 }}>
              <a
                className="tiny"
                href={api.spectrumOriginalUrl(record.id)}
                title={`${record.original_name} 을(를) 그대로 내려받습니다`}
              >
                원본 .{record.source_format || 'mpr'}
              </a>
              {record.settings_name ? (
                <a
                  className="tiny"
                  href={api.spectrumSettingsUrl(record.id)}
                  title={`${record.settings_name} — 파서가 모르는 설정 줄까지 그대로`}
                >
                  설정 .mps
                </a>
              ) : null}
            </div>
          </Card>
        </div>

        <Card title="등가회로 fitting">
          <div className="col" style={{ gap: 10 }}>
            <Field label="회로" hint="비우면 이 종류의 기본 회로">
              <input
                aria-label="회로"
                className="mono"
                value={chosenCircuit}
                onChange={(event) => setCircuit(event.target.value)}
                placeholder="R0-p(R1,CPE1)-p(R2,CPE2)"
              />
            </Field>
            <div className="col preset-list" style={{ gap: 4 }}>
              {presets.map((preset) => (
                <button
                  key={preset.circuit}
                  type="button"
                  className="ghost"
                  style={{ textAlign: 'left' }}
                  onClick={() => setCircuit(preset.circuit)}
                >
                  <span className="mono">{preset.circuit}</span>
                  <span className="tiny faint"> — {preset.label}</span>
                  <div className="tiny faint">{preset.note}</div>
                </button>
              ))}
            </div>
            <label className="row" style={{ gap: 6 }}>
              <input
                type="checkbox"
                checked={dropInductive}
                onChange={(event) => setDropInductive(event.target.checked)}
              />
              <span className="tiny">
                고주파 유도성 점 빼기 — 배선이지 셀이 아닙니다
                <span className="faint"> · 위 나이퀴스트도 함께 바뀝니다</span>
              </span>
            </label>

            {/* 맞출 창.  저주파 끝 몇 점이 오차의 절반을 내는 일이 흔한데
                (스윕이 그 과정의 정점 전에 끝났을 때 — ADR 0029), 그것이
                회로 탓인지 측정 탓인지는 창을 좁혀 봐야 갈린다. */}
            <div className="grid cols-2" style={{ gap: 8 }}>
              <Field label="맞출 주파수 하한" hint="비우면 끝까지">
                <input
                  type="number"
                  inputMode="decimal"
                  aria-label="맞출 주파수 하한"
                  placeholder={measured ? `${num(measured.low, 3)}` : 'Hz'}
                  value={fitLow}
                  onChange={(event) => {
                    setTouchedLow(true)
                    setFitLow(event.target.value)
                  }}
                />
                {/* 눌러서 넣는다.  숫자를 문장 속에서 찾아 손으로 옮겨 적는
                    것이 이 칸의 실제 사용법이었는데, 경계에 선 점의 주파수를
                    한 자리 반올림해 적으면 그 점이 도로 들어간다. */}
                {suggestion.low !== null ? (
                  <button
                    type="button"
                    className="sm ghost"
                    style={{ marginTop: 5 }}
                    onClick={() => { setTouchedLow(false); setFitLow(String(suggestion.low)) }}
                  >
                    추천 {suggestion.low} Hz
                    <span className="faint">
                      {' '}· 저주파 {suggestion.drops}점을 뺍니다
                    </span>
                  </button>
                ) : null}
              </Field>
              <Field label="맞출 주파수 상한" hint="비우면 끝까지">
                <input
                  type="number"
                  inputMode="decimal"
                  aria-label="맞출 주파수 상한"
                  placeholder={measured ? `${num(measured.high, 3)}` : 'Hz'}
                  value={fitHigh}
                  onChange={(event) => {
                    setTouchedHigh(true)
                    setFitHigh(event.target.value)
                  }}
                />
                {suggestion.high !== null ? (
                  <button
                    type="button"
                    className="sm ghost"
                    style={{ marginTop: 5 }}
                    onClick={() => { setTouchedHigh(false); setFitHigh(String(suggestion.high)) }}
                  >
                    추천 {hertz(suggestion.high)}
                    <span className="faint"> · 유도성 위쪽 끝</span>
                  </button>
                ) : null}
              </Field>
            </div>
            <div className="row">
              {/* 스캔이면 **전부**가 기본이다.  한 파일이고 한 셀이라 1번에
                  맞는 회로가 나머지에도 맞는 회로다.  한 스윕만 맞춰 보는
                  길은 옆에 남긴다 — 회로를 고르는 동안에는 그쪽이 빠르다. */}
              {isScanSweep ? (
                <>
                  <button type="button" className="primary" disabled={busy}
                          title="위의 설정(유도성 빼기·하한·상한)을 그대로 씁니다 · 이 스윕의 기하·조건을 나머지에 맞춘 뒤 전부 맞춥니다 · 상한을 비워 두면 스윕마다 자동(유도성 위쪽 끝)"
                          onClick={() => void runScanFit()}>
                    {busy ? '맞추는 중…' : `스윕 ${sweeps}개 전부 맞추기`}
                  </button>
                  <button type="button" disabled={busy}
                          onClick={() => void runFit()}>
                    {busy ? '…' : '이 스윕만'}
                  </button>
                </>
              ) : (
                <button type="button" className="primary" disabled={busy}
                        onClick={() => void runFit()}>
                  {busy ? '맞추는 중…' : '맞추기'}
                </button>
              )}
              {/* 사람이 하던 일이 그대로 이것이다: 회로를 바꿔 가며 몇 번 맞춰
                  보고 χ² 를 본다.  전부 저장되므로 아래 '지난 피팅' 에서
                  나란히 볼 수 있다. */}
              <button type="button" disabled={busy}
                      title="이 조합의 프리셋을 전부 맞춰 보고 χ² 가 가장 작은 것을 보여 줍니다"
                      onClick={() => void runFit('auto')}>
                {busy ? '…' : '자동으로 고르기'}
              </button>
              {fits.length > 1 ? (
                <select
                  aria-label="지난 fitting"
                  value={fit?.id ?? ''}
                  onChange={(event) => setShowFit(Number(event.target.value))}
                >
                  {fits.map((item) => (
                    <option key={item.id} value={item.id}>
                      {item.circuit} · χ² {item.chi_squared === null ? '—' : num(item.chi_squared, 3)}
                    </option>
                  ))}
                </select>
              ) : null}
            </div>
          </div>
        </Card>

        <Card title="파라미터">
          {fit ? <FitReport fit={fit} kind={record.kind} area={area} /> : (
            <div className="tiny faint" style={{ padding: 4 }}>
              아직 맞춘 적이 없습니다.
            </div>
          )}
        </Card>
      </div>

      <div style={{ marginTop: 14 }}>
        <DrtPanel spectrumId={record.id} area={area} />
      </div>

      <div style={{ marginTop: 14 }}>
        <OtherMeasurements sampleId={record.sample_id}
                           exclude={{ kind: 'eis', id: record.id }} />
      </div>
    </main>
  )
}

function FitReport({ fit, kind, area }: {
  fit: SpectrumFit
  kind: EisKind
  /** 면적이 있으면 저항 파라미터를 Ω·cm² 로 (없으면 null). */
  area: number | null
}) {
  const arcs = new Map(fit.arcs.map((arc) => [arc.parameter, arc]))
  // 문장 속에서 첨자로 바꿀 이름들.  **이 피팅이 실제로 가진 것만** 넘긴다 —
  // 이름처럼 생긴 조각을 정규식으로 고르면 같은 문장의 회로 문자열
  // (`L1-R0-p(R1,CPE1)-TL1`)까지 잘라 놓는다.
  const paramNames = fit.parameters.map((parameter) => parameter.name)
  return (
    <div className="col" style={{ gap: 10 }}>
      {!fit.converged ? (
        <Alert kind="error">
          맞추지 못했습니다 — <ParamText text={fit.reason} names={paramNames} />
        </Alert>
      ) : null}
      {fit.kind !== fit.kind_now ? (
        <Alert kind="warn">
          이 피팅은 {KIND_LABEL[fit.kind]} 로 맞춘 것입니다. 지금 이름은{' '}
          {KIND_LABEL[fit.kind_now]} 기준으로 붙어 있습니다 — 다시 맞추면 확실합니다.
        </Alert>
      ) : null}
      {/* 문장 속 이름도 표와 같은 모습이어야 한다 — 한 화면에서 같은 것이
          두 모습으로 나오면 다른 것으로 읽힌다. */}
      {fit.converged && fit.reason ? (
        <Alert kind="warn"><ParamText text={fit.reason} names={paramNames} /></Alert>
      ) : null}
      {fit.converged && fit.fitted_note ? (
        // 곡선을 못 그린 이유.  선이 그냥 없으면 "안 맞았다" 와 구분이 안 된다.
        <Alert kind="warn">fitting 곡선 없음 — {fit.fitted_note}</Alert>
      ) : null}

      <div className="row tiny faint" style={{ gap: 12, flexWrap: 'wrap' }}>
        <span className="mono">{fit.circuit}</span>
        <span>χ² {fit.chi_squared === null ? '—' : num(fit.chi_squared, 4)}</span>
        <span>
          시작점 {fit.starts_converged}/{fit.starts}
        </span>
        {fit.dropped_inductive ? <span>유도성 {fit.dropped_inductive}점 뺌</span> : null}
        {/* 창을 좁혀 맞췄으면 몇 점이 밖에 남았는지.  이 수가 없으면 같은
            회로의 두 χ² 가 왜 다른지 화면에 단서가 없다. */}
        {fit.dropped_out_of_range
          ? <span>창 밖 {fit.dropped_out_of_range}점 뺌</span> : null}
        {fit.frequency_low_hz && fit.frequency_high_hz ? (
          <span>
            {hertz(fit.frequency_high_hz)} → {hertz(fit.frequency_low_hz)}
          </span>
        ) : null}
      </div>

      {fit.parameters.length ? (
        // 첫 열을 붙여 둔다.  가로로 굴려도 **어느 파라미터의 줄인지**를 잃지
        // 않는다 — 잃으면 값만 남고 그 값이 무엇인지 모르게 된다.
        <div className="table-wrap pin-first">
          <table>
            <thead>
              <tr>
                <th style={{ textAlign: 'left' }}>파라미터</th>
                <th style={{ textAlign: 'left' }}>뜻</th>
                <th>값</th>
                <th>± 1σ</th>
              </tr>
            </thead>
            <tbody>
              {fit.parameters.map((parameter) => {
                const arc = arcs.get(parameter.name)
                // 서버의 아크 이름이 먼저다 — 그 저항이 이 셀에서 무엇인지는
                // 셀 구성에 달렸고 그것은 서버가 안다.  없을 때만 회로 원소의
                // 일반적인 뜻으로 받는다.
                const meaning = arc?.label ?? paramMeaning(parameter.name)
                // 보고서에 옮겨 적는 값만 굵게.  전부 굵으면 아무것도 굵지 않다.
                const headline = isHeadline(parameter.name) && parameter.determined
                return (
                  <tr key={parameter.name}>
                    {/* 첨자로 그리되 **원래 이름을 잃지 않는다** — 회로
                        칸에 쳐 넣는 것은 `CPE1_Q` 이지 `CPE₁,Q` 가 아니다. */}
                    <td className="text mono" title={parameter.name}>
                      <ParamName name={parameter.name} />
                    </td>
                    {/* 설명이 길다.  `nowrap` 이면 이 한 칸이 값 열을 화면
                        밖으로 밀어낸다 — 정작 보러 온 것이 값인데.  폭을
                        묶고 줄바꿈을 허용한다. */}
                    <td className="text dim" title={arc?.note ?? meaning}>
                      <span className="cell-wrap">{meaning || '—'}</span>
                    </td>
                    <td className={
                      parameter.determined ? (headline ? 'headline' : '') : 'faint'}>
                      {/* 저항만 나눈다.  CPE 의 S·sⁿ 는 오히려 곱해야 하고 그
                          규칙이 지수 n 에 따라 달라서, 여기서 조용히 처리하면
                          틀린 수가 맞는 수와 같은 모습으로 나온다 (§0.4). */}
                      {num(perArea(parameter.value, scalesWithArea(parameter.unit)
                        ? area : null), 4)} {areaUnit(parameter.unit, area)}
                      {parameter.determined ? null : (
                        // 숫자처럼 보이는 것이 문제이므로 숫자 옆에 붙인다.
                        <span className="tiny warn"> 미결정</span>
                      )}
                    </td>
                    <td className="dim">
                      {parameter.stderr === null ? '—' : num(
                        perArea(parameter.stderr,
                                scalesWithArea(parameter.unit) ? area : null), 2)}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      ) : null}

      {kind === 'solid' ? <Conductivity fit={fit} /> : null}
    </div>
  )
}

function Conductivity({ fit }: { fit: SpectrumFit }) {
  const value = fit.conductivity ?? {}
  if (value.missing?.length) {
    return (
      <Alert kind="info">
        전도도를 내려면 {value.missing.join(' · ')} 이(가) 필요합니다 — 셀이나
        스펙트럼에 적어 주세요.
      </Alert>
    )
  }
  return (
    <div className="col" style={{ gap: 6 }}>
      <KeyValues
        rows={[
          ['벌크 σ', value.bulk_s_cm ? `${value.bulk_s_cm.toExponential(3)} S/cm` : '—'],
          ['입계 σ', value.grain_boundary_s_cm ? `${value.grain_boundary_s_cm.toExponential(3)} S/cm` : '—'],
          // 두 σ 의 합이 아니다 — 저항이 직렬이므로 저항을 더해서 나눈다.
          ['전체 σ', value.total_s_cm ? `${value.total_s_cm.toExponential(3)} S/cm` : '—'],
        ]}
      />
      {value.excluded?.length ? (
        // 세 번째 아크는 전극 계면일 수 있어 전해질 σ 에 넣지 않는다.
        // 조용히 빼면 회로를 바꿨을 때 σ 가 왜 움직였는지 알 수 없다.
        <div className="tiny faint">σ 합계에서 뺀 아크: {value.excluded.join(' · ')}</div>
      ) : null}
    </div>
  )
}

const CONFIG_OPTIONS: { value: CellConfig | ''; label: string }[] = [
  { value: '', label: '— 안 정함' },
  { value: 'sym', label: '대칭셀' },
  { value: 'full', label: '풀셀' },
  { value: 'half', label: '하프셀' },
]

const CONFIG_LABEL: Record<string, string> = {
  sym: '대칭셀', full: '풀셀', half: '하프셀', '': '안 정함',
}

/** 셀 구성과 두께 — 아크의 이름과 전도도가 여기에 걸려 있다.
 *
 *  이름에 대개 적혀 있지만(`..._70um_sym_01`) 채워 넣지는 않는다.  이름은
 *  누군가 그렇게 부르기로 한 것이지 기록이 아니고, 오타에서 나온 전도도는
 *  측정된 것과 똑같이 생겼다.  활물질 질량과 같은 방식으로 `#` 참고 표시만
 *  옆에 둔다.
 */
function CellFields({
  record,
  onSaved,
}: {
  record: Detail
  /** 저장된 결과를 그대로 넘긴다 — 부모가 "스윕 열에 함께 적용" 을 적고,
   *  면적이 생겼으면 단위를 Ω·cm² 로 올린다. */
  onSaved: (out?: Spectrum) => void
}) {
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  // 셀 목록은 붙일 때만 필요하다.  화면을 열 때마다 받아 두면 스펙트럼만
  // 보려는 사람도 셀 전체를 한 번 받아 온다.
  const samples = useAsync(() => api.listSamples(), [])
  const [thickness, setThickness] = useState(
    record.thickness_um === null ? '' : String(record.thickness_um),
  )
  const [area, setArea] = useState(
    record.area_cm2 === null ? '' : String(record.area_cm2),
  )
  const [diameter, setDiameter] = useState(
    record.diameter_mm === null || record.diameter_mm === undefined
      ? '' : String(record.diameter_mm),
  )
  const [cycle, setCycle] = useState(
    record.at_cycle === null ? '' : String(record.at_cycle),
  )
  const [purpose, setPurpose] = useState(record.purpose ?? '')

  /** 지름이 말하는 면적.  화면에만 쓴다 -- 저장은 raw(지름)만 한다 (§0.1). */
  const diameterArea = useMemo(() => {
    const value = Number(diameter.trim())
    if (!diameter.trim() || !Number.isFinite(value) || value <= 0) return null
    const radiusCm = value / 20
    return Math.PI * radiusCm * radiusCm
  }, [diameter])

  const namedThickness = thicknessFromName(record.name) ?? thicknessFromName(record.original_name)
  const namedConfig = cellConfigFromName(record.name) ?? cellConfigFromName(record.original_name)

  async function save(body: Record<string, unknown>) {
    setBusy(true)
    setError(null)
    try {
      const out = await api.updateSpectrum(record.id, body)
      onSaved(out)
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="col" style={{ gap: 9 }}>
      {error ? <Alert kind="error">{error}</Alert> : null}

      {/* 액체/전고체 × 풀셀·하프셀·대칭셀 — 여섯 조합을 한 번에 고른다.
          둘을 따로 고르게 두면 "액체 · 미정" 같은 반쯤 정해진 상태가 남는데,
          아크의 이름도 기본 회로도 두 축이 **함께** 정해져야 나온다.  종류를
          바꾸면 기존 피팅에는 옛 종류가 남는다 (그 사실은 아래가 말한다). */}
      <Field
        label="측정 구성"
        hint="아크의 이름과 기본 회로가 여기서 정해집니다"
        note={
          namedConfig && namedConfig !== record.cell_config ? (
            <span title="파일 이름에 적힌 값">#{CONFIG_LABEL[namedConfig]}</span>
          ) : undefined
        }
      >
        <select
          aria-label="측정 구성"
          value={`${record.kind}|${record.cell_config}`}
          disabled={busy}
          onChange={(event) => {
            const [kind, cellConfig] = event.target.value.split('|')
            void save({ kind, cell_config: cellConfig })
          }}
        >
          {(['liquid', 'solid'] as const).map((kind) =>
            CONFIG_OPTIONS.map((option) => (
              <option key={`${kind}|${option.value}`} value={`${kind}|${option.value}`}>
                {kind === 'liquid' ? '액체' : '전고체'} ·{' '}
                {option.value === '' ? '구성 미정' : CONFIG_LABEL[option.value]}
              </option>
            )),
          )}
        </select>
      </Field>

      {/* 무엇을 보려고 잰 측정인가.  자유 입력이되 흔한 것은 한 번에 —
          랩이 새 목적을 계속 만들어서 목록을 고정하면 그때마다 코드를
          고쳐야 한다.  SOC 스캔처럼 파일이 스스로 말하는 것은 업로드가
          채워 둔다 (§0.3). */}
      <Field label="목적" hint="무엇을 보려고 잰 측정인가 · Enter 로 적용">
        <input
          aria-label="목적"
          list="eis-purposes"
          value={purpose}
          disabled={busy}
          placeholder="예: SOC별, 200 사이클, 온도별"
          onChange={(event) => setPurpose(event.target.value)}
          onBlur={() => {
            if (purpose.trim() === record.purpose) return
            void save({ purpose: purpose.trim() })
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter') event.currentTarget.blur()
          }}
        />
        <datalist id="eis-purposes">
          <option value="SOC별" />
          <option value="사이클별" />
          <option value="200 사이클" />
          <option value="구동 전" />
          <option value="온도별" />
        </datalist>
      </Field>

      {/* 셀에 붙이는 자리.  API 는 처음부터 됐는데 화면이 읽기만 해서, 셀
          상세의 임피던스 카드가 영영 비어 있었다 — 붙일 방법이 없으니까. */}
      <Field label="셀" hint="붙이면 셀 화면에서 함께 보입니다">
        <select
          aria-label="셀"
          value={record.sample_id ?? ''}
          disabled={busy || samples.loading}
          onChange={(event) => void save(
            event.target.value === ''
              ? { clear: ['sample_id'] }
              : { sample_id: Number(event.target.value) },
          )}
        >
          <option value="">— 안 붙임</option>
          {(samples.data ?? []).map((sample) => (
            <option key={sample.id} value={sample.id}>
              {sample.name}
            </option>
          ))}
        </select>
      </Field>

      <Field label="사이클" hint="구동 전은 0 · 비우면 안 적음 · Enter 로 적용">
        <input
          aria-label="사이클"
          type="number"
          min={0}
          value={cycle}
          disabled={busy}
          onChange={(event) => setCycle(event.target.value)}
          onBlur={() => {
            const value = cycle.trim()
            if (value === '' && record.at_cycle === null) return
            if (value !== '' && Number(value) === record.at_cycle) return
            void save(value === ''
              ? { clear: ['at_cycle'] }
              : { at_cycle: Number(value) })
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter') event.currentTarget.blur()
          }}
        />
      </Field>

      <Field
        label="두께"
        hint="µm · 전도도의 분자 · Enter 로 적용"
        note={
          namedThickness !== null && namedThickness !== record.thickness_um ? (
            <span title="파일 이름에 적힌 값">#{namedThickness}µm</span>
          ) : undefined
        }
      >
        <input
          aria-label="두께"
          type="number"
          min={0}
          value={thickness}
          disabled={busy}
          onChange={(event) => setThickness(event.target.value)}
          onBlur={() => {
            const value = thickness.trim()
            if (value === '' && record.thickness_um === null) return
            if (Number(value) === record.thickness_um) return
            void save(value === ''
              ? { clear: ['thickness_um'] }
              : { thickness_um: Number(value) })
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter') event.currentTarget.blur()
          }}
        />
      </Field>

      {/* 지름이 먼저다.  캘리퍼로 재는 것은 지름이고 면적은 거기서 나오는
          수인데, 면적만 물어 보면 사람이 매번 πd²/4 를 손으로 계산해서 넣는다.
          비어 있는 면적은 이 값에서 나오고, 면적을 직접 적으면 그것이 이긴다
          (원이 아닌 전극이 있다). */}
      <Field
        label="지름"
        hint={diameterArea === null
          ? 'mm · 원형 펠릿 · 면적이 여기서 나옵니다'
          : `mm · 면적 ${num(diameterArea, 4)} cm²`}
      >
        <input
          aria-label="지름"
          type="number"
          min={0}
          step="any"
          value={diameter}
          disabled={busy}
          onChange={(event) => setDiameter(event.target.value)}
          onBlur={() => {
            const value = diameter.trim()
            const now = record.diameter_mm ?? null
            if (value === '' && now === null) return
            if (value !== '' && Number(value) === now) return
            void save(value === ''
              ? { clear: ['diameter_mm'] }
              : { diameter_mm: Number(value) })
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter') event.currentTarget.blur()
          }}
        />
      </Field>

      <Field
        label="면적"
        hint={area.trim() === '' && diameterArea !== null
          ? 'cm² · 지금은 지름에서 나옵니다 · 적으면 그것이 이깁니다'
          : 'cm² · 전도도의 분모 · 비우면 지름이나 붙은 셀의 것'}
      >
        {/* 전도도 안내는 "셀이나 스펙트럼에 면적을 적으라" 고 하는데, 정작
            여기에 입력란이 없어 셀 없이 올린 스펙트럼은 그 안내를 따를 수
            없었다 (리뷰 #28). */}
        <input
          aria-label="면적"
          type="number"
          min={0}
          step="any"
          value={area}
          disabled={busy}
          onChange={(event) => setArea(event.target.value)}
          onBlur={() => {
            const value = area.trim()
            if (value === '' && record.area_cm2 === null) return
            if (Number(value) === record.area_cm2) return
            void save(value === ''
              ? { clear: ['area_cm2'] }
              : { area_cm2: Number(value) })
          }}
          onKeyDown={(event) => {
            if (event.key === 'Enter') event.currentTarget.blur()
          }}
        />
      </Field>

      <div className="tiny faint">
        {record.kind === 'solid' && record.cell_config !== 'sym'
          ? '전도도는 이온 블로킹 대칭셀에서만 냅니다 — 풀셀의 저주파 아크는 계면입니다.'
          : '전도도는 조회할 때 계산합니다 — 두께·면적을 고치면 바로 따라옵니다.'}
      </div>
    </div>
  )
}
