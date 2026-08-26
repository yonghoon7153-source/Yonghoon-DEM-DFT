/** GITT 기록 하나 — pseudo-OCV, 확산계수, 그리고 재료 상수.
 *
 *  두 결과를 나란히 두되 **비어 있는 이유가 다르다**: pOCV 는 파일만 있으면
 *  나오고, 확산계수는 파일에 없는 값 넷을 사람이 넣어야 한다 (ADR 0020).
 *  그래서 확산계수 자리는 비어 있을 때 "무엇이 없는지" 를 말한다.
 */

import { OtherMeasurements } from '../components/OtherMeasurements'
import { RelatedCellCard } from '../components/RelatedCell'
import { useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { CopyBar } from '../components/CopyBar'
import { Plot, type PlotSeries } from '../components/Plot'
import { Alert, Card, Field, KeyValues, Spinner } from '../components/ui'
import { api } from '../lib/api'
import { dateTime, num, seriesColor } from '../lib/format'
import { diffusionTsv, pocvTsv, skippedDiffusionPoints } from '../lib/origin'
import { useAsync } from '../lib/hooks'
import type { GittRun } from '../lib/types'

type Mode = 'pocv' | 'diffusion'

/** 가로축의 단위.  GITT 는 **면적 기준을 먼저 본다**.
 *
 *  충방전 쪽은 mAh/g 이 기본이다 -- 활물질 1 g 이 얼마나 내는지가 소재의 값이고,
 *  셀 사이의 비교가 거기서 이루어진다.  GITT 는 그 반대다: 재는 것이 계면을
 *  건너는 확산이고 (`D` 의 분모가 면적의 제곱이다), 펠릿을 두껍게 눌러 만드는
 *  전고체에서는 같은 mAh/g 도 면적이 다르면 다른 전류밀도로 잰 것이 된다.
 *  그래서 랩이 실제로 쓰는 축은 mAh/cm² 다.
 */
type GittBasis = 'mAh' | 'mAh/g' | 'mAh/cm2'

const BASIS_LABEL: Record<GittBasis, string> = {
  mAh: 'mAh',
  'mAh/g': 'mAh/g',
  'mAh/cm2': 'mAh/cm²',
}

/** 그 기준으로 나누는 수 — 없으면 `null` 이고, 그러면 그 기준을 못 쓴다.
 *
 *  나눌 수가 없을 때 1 로 나누지 않는다: mAh 를 mAh/cm² 라고 부르기만 한
 *  숫자가 되고, 그것은 측정한 면적용량과 화면에서 구별되지 않는다 (§0.4).
 */
function divisor(record: GittRun, basis: GittBasis): number | null {
  if (basis === 'mAh/g') return record.active_mass_g_effective || null
  if (basis === 'mAh/cm2') return record.area_cm2_effective || null
  return 1
}

export function GittDetail() {
  const params = useParams<{ id: string }>()
  const id = Number(params.id)
  const [mode, setMode] = useState<Mode>('pocv')
  const [reloadKey, bumpReload] = useState(false)

  const run = useAsync(() => api.getGittRun(id), [id, reloadKey])
  const pocv = useAsync(() => api.gittPocv(id), [id, reloadKey])
  const diffusion = useAsync(() => api.gittDiffusion(id), [id, reloadKey])
  // 관계셀 드롭다운이 쓸 목록 -- EIS 상세와 같은 카드를 쓴다.
  const allSamples = useAsync(() => api.listSamples(), [])

  // 사람이 고른 기준.  null 이면 아직 안 골랐다는 뜻이고, 그때 면적이 있으면
  // mAh/cm² 로 연다 -- 고르지 않은 사람이 보는 첫 화면이 랩이 쓰는 축이다.
  const [picked, setPicked] = useState<GittBasis | null>(null)
  const area = run.data?.area_cm2_effective ?? null
  const mass = run.data?.active_mass_g_effective ?? null
  const basis: GittBasis = picked ?? (area ? 'mAh/cm2' : 'mAh')
  // 고른 기준을 못 쓰게 됐을 때 (면적을 지웠다) 조용히 mAh 로 떨어진다.
  const scale = run.data ? divisor(run.data, basis) : 1
  const effective: GittBasis = scale ? basis : 'mAh'
  const per = (scale && basis === effective ? scale : 1)
  const unit = BASIS_LABEL[effective]
  const axis = effective === 'mAh' ? '용량 (mAh)'
    : effective === 'mAh/g' ? '비용량 (mAh g⁻¹)' : '면적용량 (mAh cm⁻²)'

  const pocvSeries = useMemo<PlotSeries[]>(() => {
    const data = pocv.data
    if (!data) return []
    const out: PlotSeries[] = []
    // 원본을 **먼저** 넣는다: 나중 계열이 위에 그려지므로, pOCV 의 점이 선에
    // 가리지 않는다.  같은 색의 점선이라 어느 곡선의 원본인지도 분명하다.
    const raw = (trace: { capacity_mah: number[]; voltage_v: number[] } | undefined,
                 label: string, color: string) => {
      if (!trace?.capacity_mah.length) return
      out.push({
        label, x: trace.capacity_mah.map((value) => value / per), y: trace.voltage_v,
        color, width: 1, dash: [3, 3],
      })
    }
    raw(data.charge_raw, '충전 측정 전압', seriesColor(0))
    raw(data.discharge_raw, '방전 측정 전압', seriesColor(1))
    if (data.charge.length) {
      out.push({
        label: '충전 pOCV',
        x: data.charge.map((point) => point.capacity_mah / per),
        y: data.charge.map((point) => point.voltage_v),
        color: seriesColor(0),
        points: true,
        width: 1,
      })
    }
    if (data.discharge.length) {
      out.push({
        label: '방전 pOCV',
        x: data.discharge.map((point) => point.capacity_mah / per),
        y: data.discharge.map((point) => point.voltage_v),
        color: seriesColor(1),
        points: true,
        width: 1,
      })
    }
    return out
  }, [pocv.data, per])

  const diffusionSeries = useMemo<PlotSeries[]>(() => {
    // null 검사를 명시적으로 — truthy 필터는 D=0 을 버려서, 표·TSV 에는 있는
    // 점이 그래프에서만 사라지고 "가정을 통과한 펄스 없음" 이 거짓이 됐다
    // (리뷰 #32).  0 은 로그축에 못 그리므로 빼되, 아래 문구가 셈해 준다.
    const usable = (diffusion.data?.points ?? [])
      .filter((point) => point.d_cm2_s !== null && point.d_cm2_s > 0)
    if (!usable.length) return []
    return [{
      label: 'log₁₀ D (cm²/s)',
      x: usable.map((point) => point.capacity_mah / per),
      // 자릿수가 서너 개 오가므로 로그로 그린다.  선형이면 큰 값 하나가
      // 나머지를 바닥에 눕힌다.
      y: usable.map((point) => Math.log10(point.d_cm2_s!)),
      color: seriesColor(2),
      points: true,
      width: 1,
    }]
  }, [diffusion.data, per])
  const zeroDiffusion = useMemo(
    () => (diffusion.data?.points ?? [])
      .filter((point) => point.d_cm2_s === 0).length,
    [diffusion.data],
  )

  if (run.error) {
    return <main className="page"><Alert kind="error">{run.error}</Alert></main>
  }
  if (!run.data) {
    return <main className="page"><Spinner label="불러오는 중" /></main>
  }
  const record = run.data

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1 className="truncate">{record.name}</h1>
          <div className="sub">
            {[`펄스 ${record.n_pulses}개`, `${record.n_points}점`,
              record.duration_h === null ? null : `${num(record.duration_h, 3)} h`]
              .filter(Boolean).join('  ·  ')}
          </div>
        </div>
        <span className="spacer" />
        <Link className="link-btn" to="/gitt">목록</Link>
      </div>

      {record.pulse_note ? <Alert kind="warn">{record.pulse_note}</Alert> : null}

      <div style={{ marginBottom: 14 }}>
        <RelatedCellCard
          sampleId={record.sample_id ?? null}
          sampleName={record.sample_name ?? null}
          samples={allSamples.data ?? []}
          record={record}
          onSaveConditions={async (body) => {
            await api.updateGittRun(record.id, body)
            bumpReload((value) => !value)
          }}
          onPick={async (picked) => {
            await api.updateGittRun(record.id, picked
              ? { sample_id: picked }
              : { clear: ['sample_id'] })
            bumpReload((value) => !value)
          }}
        />
      </div>

      <div className="row" style={{ marginBottom: 12, gap: 10, flexWrap: 'wrap' }}>
        <div className="segmented" role="tablist">
          <button type="button" role="tab" aria-selected={mode === 'pocv'}
                  className={mode === 'pocv' ? 'on accent' : ''}
                  onClick={() => setMode('pocv')}>
            pseudo-OCV
          </button>
          <button type="button" role="tab" aria-selected={mode === 'diffusion'}
                  className={mode === 'diffusion' ? 'on accent' : ''}
                  onClick={() => setMode('diffusion')}>
            확산계수
          </button>
        </div>
        <span className="spacer" />
        <BasisPicker
          basis={basis}
          effective={effective}
          onPick={setPicked}
          area={area}
          mass={mass}
        />
      </div>

      <div style={{ marginBottom: 12 }}>
        <CopyBar
          items={[
            {
              label: 'pOCV',
              title: '용량 · 전압 두 열 — 충전과 방전을 `--` 로 갈라 쌓는다',
              disabled: !pocv.data,
              build: () => (pocv.data ? pocvTsv(pocv.data) : ''),
            },
            {
              label: '확산계수',
              title: '용량 · D · 휴지(s) · 드리프트(mV) — 숫자가 나온 점만, 증거와 함께',
              disabled: !diffusion.data?.points.length,
              build: () => diffusionTsv(diffusion.data?.points ?? []),
              skipped: skippedDiffusionPoints(diffusion.data?.points ?? []),
              // 조용히 빼면 붙여 넣은 사람이 점 수가 다른 것을 못 본다.
              skippedNote: (n) => `가정을 통과하지 못한 펄스 ${n}개는 뺐습니다 — `
                + '이유는 아래 표에 있습니다',
            },
          ]}
        />
      </div>

      {/* `grid cols-2` 는 둘을 반씩 나눠 가졌다.  왼쪽은 읽는 곡선이고 오른쪽은
          숫자 여덟 칸이라, 반씩은 곡선에 좁고 칸에 넓었다.  `split` 은 곡선에
          남는 폭을 다 주고 상수 카드를 340px 세로 줄로 세운다. */}
      <div className="split">
        <Card title={mode === 'pocv' ? '준평형 전압 곡선' : '확산계수'}>
          {mode === 'pocv' ? (
            pocv.error ? <Alert kind="error">{pocv.error}</Alert>
              : pocvSeries.length ? (
                <Plot series={pocvSeries} xLabel={axis} yLabel="전압 (V)"
                      height={420} legend />
              ) : pocv.loading ? <Spinner /> : (
                <Alert kind="info">
                  휴지 끝의 전압을 짝지을 펄스가 없습니다.
                </Alert>
              )
          ) : diffusion.error ? (
            <Alert kind="error">{diffusion.error}</Alert>
          ) : diffusion.data?.missing.length ? (
            // pOCV 와 비어 있는 이유가 다르다.  그 차이를 말한다.
            <Alert kind="info">
              확산계수를 내려면 {diffusion.data.missing.join(' · ')} 이(가)
              필요합니다 — 아래 &lsquo;재료 상수&rsquo; 에 넣어 주세요.
              추정한 값으로 계산한 D 는 그 추정의 제곱만큼 틀립니다.
            </Alert>
          ) : diffusionSeries.length ? (
            <div className="col" style={{ gap: 6 }}>
              <Plot series={diffusionSeries} xLabel={axis}
                    yLabel="log₁₀ D (cm²/s)" height={420} legend />
              {zeroDiffusion ? (
                <div className="tiny faint">
                  D=0 인 점 {zeroDiffusion}개는 로그축에 그릴 수 없어 뺐습니다 —
                  표와 클립보드에는 있습니다.
                </div>
              ) : null}
            </div>
          ) : diffusion.loading ? <Spinner /> : (
            <Alert kind="info">
              {zeroDiffusion
                ? `양수 D 가 없습니다 — D=0 인 점 ${zeroDiffusion}개는 로그축에 못 그립니다 (표에 있습니다).`
                : '가정을 통과한 펄스가 없습니다 — 아래 표의 이유를 보세요.'}
            </Alert>
          )}
        </Card>

        <Card title="재료 상수" padSmall>
          <MaterialFields record={record} onSaved={() => bumpReload((v) => !v)} />
        </Card>
      </div>

      <div style={{ marginTop: 14 }}>
        {mode === 'pocv' ? (
          <PocvTable id={id} pocv={pocv.data} per={per} unit={unit} />
        ) : (
          <DiffusionTable diffusion={diffusion.data} per={per} unit={unit} />
        )}
      </div>

      <div style={{ marginTop: 14 }}>
        <Card title="파일" padSmall>
          <KeyValues rows={[
            ['원본', record.original_name || '—'],
            ['크기', `${(record.size_bytes / 1e6).toFixed(1)} MB`],
            ['시작', record.start_time ? dateTime(record.start_time) : '—'],
            ['올린 때', dateTime(record.uploaded_at)],
          ]} />
          {/* 충방전 쪽과 같은 길.  중앙에 모아 두는 이유가 "각자 노트북에서
              원본이 사라지지 않게" 인데, 다시 못 받으면 올리는 것이 편도
              여행이 되고 아무도 원본을 안 맡긴다. */}
          <div className="row" style={{ marginTop: 8 }}>
            <a
              className="tiny"
              href={api.gittOriginalUrl(record.id)}
              title={`${record.original_name} 을(를) 그대로 내려받습니다`}
            >
              원본 .wrd
            </a>
          </div>
        </Card>
      </div>
      <div style={{ marginTop: 14 }}>
        <OtherMeasurements sampleId={record.sample_id ?? null}
                           exclude={{ kind: 'gitt', id: record.id }} />
      </div>
    </main>
  )
}

function PocvTable({ id, pocv, per, unit }: {
  id: number
  pocv: import('../lib/types').Pocv | null
  /** 용량 열을 나누는 수와 그 이름 -- 그래프와 **같은** 기준이어야 한다.
   *  둘이 어긋나면 그래프에서 읽은 자리를 표에서 찾을 수 없다. */
  per: number
  unit: string
}) {
  if (!pocv) return null
  const skipped = pocv.skipped_charge + pocv.skipped_discharge
  return (
    <Card title={`pOCV 점 ${pocv.charge.length + pocv.discharge.length}개`}>
      <div className="col" style={{ gap: 10 }}>
        {skipped ? (
          // 조용히 버리면 잘린 파일과 정상 파일이 곡선에서 구분되지 않는다.
          <Alert kind="warn">
            휴지가 뒤따르지 않아 뺀 펄스 {skipped}개
            {pocv.skipped_reasons.length ? ` — ${pocv.skipped_reasons.join(' · ')}` : ''}
          </Alert>
        ) : null}
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th style={{ textAlign: 'left' }}>방향</th>
                <th>용량 ({unit})</th>
                <th>전압 (V)</th>
                <th>휴지</th>
                <th>잔류 드리프트</th>
              </tr>
            </thead>
            <tbody>
              {[...pocv.charge.map((point) => ['충전', point] as const),
                ...pocv.discharge.map((point) => ['방전', point] as const)]
                .map(([branch, point], index) => (
                  <tr key={`${id}-${branch}-${index}`}>
                    <td className="text dim">{branch}</td>
                    <td>{num(point.capacity_mah / per, 4)}</td>
                    <td>{num(point.voltage_v, 4)}</td>
                    <td className="dim">{num(point.rest_s, 4)} s</td>
                    {/* 짧은 휴지의 전압은 OCV 가 아니다.  얼마나 아닌지. */}
                    <td className="dim">{num(point.drift_mv, 3)} mV</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </div>
    </Card>
  )
}

function DiffusionTable({
  diffusion,
  per,
  unit,
}: {
  diffusion: import('../lib/types').Diffusion | null
  per: number
  unit: string
}) {
  if (!diffusion) return null
  return (
    <Card title={`펄스 ${diffusion.total}개 · 숫자가 나온 것 ${diffusion.usable}개`}>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>용량 ({unit})</th>
              <th>D (cm²/s)</th>
              <th>ΔE_s (V)</th>
              <th>ΔE_t (V)</th>
              <th>펄스</th>
              <th>휴지</th>
              {/* 휴지 끝에서 전압이 아직 움직인 양.  D 는 그 휴지가 평형이라는
                  가정 위에 있고, 이 증거 없이 숫자만 있으면 실제보다 확실해
                  보인다 (ADR 0020). */}
              <th>드리프트 (mV)</th>
              <th>√t R²</th>
              <th style={{ textAlign: 'left' }}>왜 안 나왔나</th>
            </tr>
          </thead>
          <tbody>
            {diffusion.points.map((point, index) => (
              <tr key={index}>
                <td>{num(point.capacity_mah / per, 4)}</td>
                <td>{point.d_cm2_s === null ? '—' : point.d_cm2_s.toExponential(3)}</td>
                <td className="dim">{num(point.delta_es_v, 4)}</td>
                <td className="dim">{num(point.delta_et_v, 4)}</td>
                <td className="dim">{num(point.pulse_s, 4)} s</td>
                <td className="dim">
                  {point.rest_s == null ? '—' : `${num(point.rest_s, 4)} s`}
                </td>
                <td className={point.drift_mv != null && point.drift_mv > 5 ? 'warn' : 'dim'}>
                  {point.drift_mv == null ? '—' : num(point.drift_mv, 2)}
                </td>
                {/* Weppner-Huggins 의 가정이 곧 이 값이다. */}
                <td className={point.sqrt_t_r_squared >= 0.98 ? 'dim' : 'warn'}>
                  {num(point.sqrt_t_r_squared, 4)}
                </td>
                <td className="text tiny faint">{point.reason || '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )
}

/** 가로축 기준 고르개.
 *
 *  못 쓰는 기준을 지우지 않고 **막아 놓고 이유를 적는다**: 버튼이 사라지면
 *  "이 화면은 mAh/g 을 못 낸다" 로 읽히지만, 실제로는 질량 한 칸이 비어 있을
 *  뿐이고 그 칸이 바로 옆에 있다.
 */
function BasisPicker({
  basis, effective, onPick, area, mass,
}: {
  basis: GittBasis
  /** 실제로 그려지는 기준.  고른 것과 다르면 나눌 수가 없어진 것이다. */
  effective: GittBasis
  onPick: (value: GittBasis) => void
  area: number | null
  mass: number | null
}) {
  const why: Record<GittBasis, string | null> = {
    mAh: null,
    'mAh/g': mass ? null : '활물질 질량이 없습니다',
    'mAh/cm2': area ? null : '계면 면적이 없습니다',
  }
  return (
    <div className="row" style={{ gap: 6 }}>
      <span className="tiny faint">가로축</span>
      <div className="segmented">
        {(['mAh', 'mAh/cm2', 'mAh/g'] as GittBasis[]).map((value) => (
          <button
            key={value}
            type="button"
            className={effective === value ? 'on' : ''}
            disabled={why[value] !== null}
            title={why[value] ?? undefined}
            onClick={() => onPick(value)}
          >
            {BASIS_LABEL[value]}
          </button>
        ))}
      </div>
      {basis !== effective ? (
        <span className="tiny warn">{why[basis]} — mAh 로 그립니다</span>
      ) : null}
    </div>
  )
}

/** 재료 상수 칸들.
 *
 *  `derive` 가 있는 칸은 **비워 두면 계산된다**: 면적은 지름에서, 활물질 질량은
 *  전극 질량 × wt% 에서.  둘 다 잰 것이 다른 값이라 그렇다 -- 캘리퍼는 지름을
 *  읽고 저울은 전극 전체를 읽는다.  그래도 적어 넣은 값이 늘 이긴다: 원이 아닌
 *  전극이 있고, 활물질만 따로 단 경우가 있다.  계산된 값은 힌트에 적어서, 빈
 *  칸이 "없다" 가 아니라 "여기서 나온다" 로 읽히게 한다.
 */
const FIELDS: {
  key: keyof GittRun
  label: string
  hint: string
  derive?: (record: GittRun) => string | null
}[] = [
  { key: 'molar_volume_cm3', label: '몰부피 V_M', hint: 'cm³/mol · 활물질' },
  { key: 'molar_mass_g', label: '몰질량 M_B', hint: 'g/mol · 활물질' },
  {
    key: 'active_mass_g',
    label: '활물질 질량',
    hint: 'g · 이 전극의',
    derive: (record) => (record.active_mass_g || !record.active_mass_g_effective
      ? null
      : `전극 질량 × wt% 에서: ${num(record.active_mass_g_effective, 4)} g`),
  },
  { key: 'electrode_mass_g', label: '전극 질량', hint: 'g · 활물질 질량을 비우면 이것 × wt%' },
  { key: 'active_wt_percent', label: '활물질 wt%', hint: '% · 조성에서' },
  { key: 'diameter_mm', label: '지름', hint: 'mm · 면적을 비우면 여기서 나옵니다' },
  {
    key: 'area_cm2',
    label: '계면 면적 S',
    hint: 'cm² · 전극/전해질',
    derive: (record) => (record.area_cm2 || !record.area_cm2_effective
      ? null
      : `지름에서: ${num(record.area_cm2_effective, 4)} cm²`),
  },
  { key: 'min_rest_s', label: '최소 휴지', hint: 's · 0 이면 전부 씁니다' },
]

/** 파일에 없는 값들.  D 는 이 넷의 조합의 제곱에 비례한다 (ADR 0020). */
function MaterialFields({
  record,
  onSaved,
}: {
  record: GittRun
  onSaved: () => void
}) {
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const [draft, setDraft] = useState<Record<string, string>>(() =>
    Object.fromEntries(FIELDS.map((field) => {
      const value = record[field.key]
      return [field.key, value === null || value === undefined ? '' : String(value)]
    })),
  )

  async function commit(key: string) {
    const text = (draft[key] ?? '').trim()
    const current = record[key as keyof GittRun]
    if (text === '' && (current === null || current === undefined)) return
    if (text !== '' && Number(text) === current) return
    setBusy(true)
    setError(null)
    try {
      await api.updateGittRun(record.id,
                              text === '' ? { clear: [key] } : { [key]: Number(text) })
      onSaved()
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="col" style={{ gap: 9 }}>
      {error ? <Alert kind="error">{error}</Alert> : null}
      {FIELDS.map((field) => (
        <Field key={field.key} label={field.label}
               hint={field.derive?.(record) ?? field.hint}>
          <input
            aria-label={field.label}
            type="number"
            min={0}
            value={draft[field.key] ?? ''}
            disabled={busy}
            onChange={(event) =>
              setDraft((current) => ({ ...current, [field.key]: event.target.value }))
            }
            onBlur={() => void commit(field.key)}
            onKeyDown={(event) => {
              if (event.key === 'Enter') event.currentTarget.blur()
            }}
          />
        </Field>
      ))}
      <div className="tiny faint">
        활물질 질량과 계면 면적은 비워 두면 각각 <b>전극 질량 × wt%</b> 와
        <b> 지름</b>에서 계산합니다 — 적어 넣으면 그 값이 이깁니다.
      </div>
      <div className="tiny faint">
        D 는 이 값들의 조합의 제곱에 비례합니다 — 추정한 값을 넣으면 그만큼
        틀린 숫자가 나오고, 측정한 것과 똑같이 생겼습니다.
      </div>
    </div>
  )
}
