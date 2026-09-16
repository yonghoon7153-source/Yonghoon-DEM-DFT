/** 한 대칭셀 `.mpt` — 온도별 이온전도도와 활성화에너지 (ADR 0039).
 *
 *  슬라이드에 붙는 표 한 장이 이 화면의 목표다:
 *  `온도(°C) · 두께(mm) · 저항(Ω) · 이온전도도(mS cm⁻¹) · 활성화 에너지(eV)`.
 *  지금까지 ZView·엑셀·Origin 을 오가며 만들던 것이다.
 *
 *  **기계가 저항을 고르지 않는다.**  블로킹 대칭셀의 나이퀴스트에는 "전해질
 *  저항" 이라고 적힌 점이 없다 — 고주파는 배선 인덕턴스로 실수축 아래에 있고,
 *  아크가 닫히기 전에 블로킹 꼬리가 올라온다.  읽을 수 있는 두 수(실수축 교점,
 *  맞춤의 총저항)를 **나란히 제안으로** 띄우고, 누르는 것은 사람이다.
 *
 *  나란히 놓는 이유는 둘이 크게 어긋날 수 있어서다: 회로에 블로킹 꼬리를 담을
 *  요소가 없으면 맞춤은 `p(R1,CPE1)` 로 꼬리를 흉내내고, 실측 파일에서 그
 *  총저항이 교점의 4710~8193배로 나왔다 (60 °C 에서 4.82 Ω 대 22687 Ω).
 *  나란히 놓으면 그 어긋남이 눈에 보인다.
 */

import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

import { CopyBar } from '../components/CopyBar'
import { Plot, type PlotSeries } from '../components/Plot'
import { DeleteMeasurementButton } from '../components/RelatedCell'
import {
  Alert, Card, Field, Metric, MetricBand, Spinner,
} from '../components/ui'
import { api } from '../lib/api'
import { basisLabel, missingSentence, sourceLabel } from '../lib/conductivity'
import { num } from '../lib/format'
import { useAsync } from '../lib/hooks'
import { arrheniusTsv, conductivityTableTsv } from '../lib/origin'
import {
  describeValues, listProblem, parseValueList,
} from '../lib/valuelist'
import type { ConductivityRow, ScanConductivity } from '../lib/types'

/** 활성화에너지는 소수 셋째 자리까지 그대로 적는다.
 *
 *  `num()` 을 쓰지 않는 이유는 그쪽이 **유효숫자**를 맞추기 때문이다 — 0.3284
 *  가 `0.33` 이 되어 버리는데, 랩이 슬라이드에 적는 것은 `0.328` 이고 0.33 과
 *  0.35 를 가르는 것이 바로 셋째 자리다 (기준을 바꾸면 그만큼 움직인다).
 */
function ev(value: number | null | undefined): string {
  return value === null || value === undefined || !Number.isFinite(value)
    ? '—' : value.toFixed(3)
}

/** 맞춤 보고서의 수는 **Origin 이 적는 대로** 적는다.
 *
 *  `num()` 은 측정값을 일정한 유효숫자로 맞추는 것이라 여기서는 안 맞는다 —
 *  `R-Square (COD)` 를 `0.9932` 로 줄이면 Origin 화면의 `0.99319` 와 눈으로
 *  대조할 수 없고, 이 표가 있는 이유가 바로 그 대조다.  여섯 자리로 자르고
 *  뒤의 0 만 턴다: 7.01784 · -3.80724 · 0.4115 · 0.99319 가 그대로 나온다.
 */
function sig(value: number | null | undefined, digits = 6): string {
  return value === null || value === undefined || !Number.isFinite(value)
    ? '—' : String(Number(value.toPrecision(digits)))
}

/** 세로축을 무엇의 로그로 둘 것인가.  기본은 랩의 관행 (`ln σ`). */
const BASES = [
  { value: 'sigma', label: 'ln σ' },
  { value: 'sigma_t', label: 'ln(σT)' },
]

export function SymCellDetail() {
  const { sha256 = '' } = useParams()
  const navigate = useNavigate()
  const [basis, setBasis] = useState('sigma')
  const [pageError, setPageError] = useState<string | null>(null)

  const scan = useAsync(() => api.getScan(sha256), [sha256])
  const cond = useAsync(
    () => api.scanConductivity(sha256, { basis }), [sha256, basis])

  if (scan.error) {
    return <main className="page"><Alert kind="error">{scan.error}</Alert></main>
  }
  if (!scan.data || !cond.data) {
    return <main className="page"><Spinner /></main>
  }
  const head = scan.data
  const data = cond.data
  const activation = data.activation

  return (
    <main className="page">
      <div className="page-head">
        <div style={{ minWidth: 0 }}>
          <h1>{head.name}</h1>
          <div className="sub">
            <Link to="/sym/library">대칭셀</Link>
            {' · '}
            <Link to={`/scans/${sha256}`}>나이퀴스트로 보기</Link>
            {head.purpose ? ` · ${head.purpose}` : ''}
            {head.sample_id ? (
              <>
                {' · '}
                <Link to={`/samples/${head.sample_id}`}>{head.sample_name}</Link>
              </>
            ) : null}
          </div>
        </div>
        <DeleteMeasurementButton
          name={head.name}
          note={`스윕 ${head.sweeps}개 전부`}
          onError={setPageError}
          onDelete={async () => {
            await api.deleteScan(sha256)
            navigate('/sym/library')
          }}
        />
      </div>

      {pageError ? <Alert kind="error">{pageError}</Alert> : null}

      <MetricBand>
        <Metric label="스윕" value={head.sweeps} />
        <Metric
          label="활성화에너지"
          value={activation.activation_energy_ev === null
            ? '—'
            : `${ev(activation.activation_energy_ev)} eV`}
          muted={activation.activation_energy_ev === null}
        />
        <Metric
          label="직선에 쓴 점"
          value={`${activation.points_used} / ${data.sweeps}`}
          muted={activation.points_used === 0}
        />
        <Metric
          label="R²"
          value={sig(activation.fit?.r_squared)}
          muted={!activation.fit}
        />
      </MetricBand>

      {data.missing.length ? (
        <Alert kind="info">{missingSentence(data)}</Alert>
      ) : null}

      {/* 사람이 적는 것 셋 — 온도·기하·저항.  계측기는 셋 다 모른다. */}
      <ValueRow
        title="온도"
        hint="스윕 차례대로. 일일이 써도 되고, 등간격이면 (처음, 끝, 개수) 로 줄여도 됩니다."
        example="예: 60, 50, 40, 30, 20, 10, 0, -10, -20  ·  (60, -20, 9)"
        unit="°C"
        what="온도"
        sweeps={data.sweeps}
        current={data.rows.map((row) => row.temperature_c)}
        onSave={(values) => api.writeScanTemperature(sha256, values)}
        onSaved={() => cond.reload()}
      />

      <Geometry rows={data.rows} onSaved={() => cond.reload()} />

      <ValueRow
        title="전해질 저항"
        hint="ZView 에서 읽은 값을 스윕 차례대로. 비어 있으면 이온전도도도 비어 있습니다."
        example="예: 9.69, 10.21, 14.56 …  ·  아래 단추로 읽은 값을 채울 수 있습니다 (제안일 뿐입니다)"
        unit="Ω"
        what="저항"
        sweeps={data.sweeps}
        current={data.rows.map((row) => row.resistance_ohm)}
        suggestions={[
          { label: '실수축 교점으로', values: data.rows.map((row) => row.crossing_ohm) },
          { label: 'fitting 총저항으로', values: data.rows.map((row) => row.fit_ohm) },
        ]}
        onSave={(values) => api.writeScanResistance(sha256, values)}
        onSaved={() => cond.reload()}
      />

      <Card
        title="표"
        tight
        actions={
          <CopyBar items={[
            {
              label: '표',
              title: '슬라이드의 다섯 열 — Origin 에 그대로 붙습니다',
              build: () => conductivityTableTsv(data.rows, activation),
            },
            {
              label: '직선',
              title: '1000/T 과 ln σ — Origin 에서 직접 Linear Fit 을 눌러 볼 때',
              build: () => arrheniusTsv(activation),
              disabled: !activation.inverse_temperature.length,
            },
          ]} />
        }
      >
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>스윕</th>
                <th>온도 (°C)</th>
                <th>두께 (mm)</th>
                <th>면적 (cm²)</th>
                <th>저항 (Ω)</th>
                <th style={{ textAlign: 'left' }}>어디서</th>
                <th>이온전도도 (mS cm⁻¹)</th>
              </tr>
            </thead>
            <tbody>
              {data.rows.map((row) => (
                <tr key={row.spectrum_id}>
                  <td className="dim">{row.sweep_index}</td>
                  <td className={row.temperature_c === null ? 'dim' : ''}>
                    {row.temperature_c === null ? '—' : num(row.temperature_c, 1)}
                  </td>
                  <td className={row.thickness_mm === null ? 'dim' : ''}>
                    {row.thickness_mm === null ? '—' : num(row.thickness_mm, 3)}
                  </td>
                  <td className={row.area_cm2 === null ? 'dim' : ''}>
                    {row.area_cm2 === null ? '—' : num(row.area_cm2, 4)}
                  </td>
                  <td className={row.resistance_ohm === null ? 'dim' : ''}>
                    {row.resistance_ohm === null ? '—' : num(row.resistance_ohm, 4)}
                  </td>
                  {/* 어디서 온 저항인지 — 한 열에 섞인 채로 슬라이드에 붙으면
                      그 구분은 영영 사라진다. */}
                  {/* 읽을 수 있는 두 수를 나란히 — 어긋나면 눈에 보인다.
                      실측에서 맞춤 총저항이 교점의 4710배였던 적이 있다.
                      한 문자열로 만든다: 조각으로 나누면 화면에서는 같아
                      보여도 골라 복사할 때 끊긴다. */}
                  <td className="text dim tiny">{readings(row)}</td>
                  <td className={row.sigma_ms_cm === null ? 'dim' : ''}>
                    {row.sigma_ms_cm === null ? '—' : num(row.sigma_ms_cm, 3)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      <Card
        title="활성화에너지"
        tight
        actions={
          <div className="seg">
            {BASES.map((one) => (
              <button
                key={one.value}
                type="button"
                className={basis === one.value ? 'on' : ''}
                onClick={() => setBasis(one.value)}
              >
                {one.label}
              </button>
            ))}
          </div>
        }
      >
        <div style={{ padding: 14 }}>
          {activation.reason ? (
            <Alert kind="warn">{activation.reason}</Alert>
          ) : null}
          <div className="tiny dim" style={{ marginBottom: 8 }}>
            {basisLabel(activation.basis)} · 기울기에 −1000·k<sub>B</sub> 를 곱한 것이
            활성화에너지입니다. 같은 점을 다른 기준으로 맞추면 다른 수가 나오므로
            (실측 0.329 ↔ 0.354 eV) 어느 쪽인지 함께 적어 두세요.
          </div>
          <ArrheniusPlot data={data} />
          {activation.fit ? <FitReport data={data} /> : null}
        </div>
      </Card>
    </main>
  )
}

/** Arrhenius 그림 — 점과 맞춘 직선.
 *
 *  직선은 점의 x 범위 **안에서만** 긋는다.  밖으로 늘이면 재지 않은 온도에서의
 *  전도도를 그림이 주장하게 된다.
 */
function ArrheniusPlot({ data }: { data: ScanConductivity }) {
  const activation = data.activation
  const series = useMemo<PlotSeries[]>(() => {
    const x = activation.inverse_temperature
    const y = activation.log_sigma
    if (!x.length) return []
    const out: PlotSeries[] = [
      { label: '측정', x, y, points: true, width: 0 },
    ]
    const fit = activation.fit
    if (fit) {
      const low = Math.min(...x)
      const high = Math.max(...x)
      out.push({
        label: '맞춘 직선',
        x: [low, high],
        y: [fit.intercept + fit.slope * low, fit.intercept + fit.slope * high],
        dash: [6, 4],
      })
    }
    return out
  }, [activation])

  if (!series.length) {
    return (
      <div className="tiny dim" style={{ padding: 20, textAlign: 'center' }}>
        온도와 이온전도도가 모두 적힌 스윕이 둘 이상이어야 직선이 섭니다.
      </div>
    )
  }
  return (
    <Plot
      series={series}
      xLabel="1000/T (K⁻¹)"
      yLabel={activation.basis === 'sigma_t' ? 'ln(σT)' : 'ln σ (S cm⁻¹)'}
      height={300}
      legend
      pngName={`${data.name}-arrhenius`}
      pngTitle={`${data.name} — Arrhenius`}
      pngCaption={[
        basisLabel(activation.basis),
        activation.activation_energy_ev === null
          ? null
          : `Ea = ${ev(activation.activation_energy_ev)} eV`,
      ].filter(Boolean).join(' · ')}
    />
  )
}

/** Origin 의 Linear Fit 보고서 — 그 회색 표 그대로.
 *
 *  기울기만 적으면 사람은 이 표를 만들려고 Origin 을 다시 연다.
 */
function FitReport({ data }: { data: ScanConductivity }) {
  const fit = data.activation.fit
  if (!fit) return null
  const ea = data.activation
  const rows: [string, string][] = [
    ['Equation', 'y = a + b*x'],
    ['Weight', 'No Weighting'],
    ['Intercept', pm(fit.intercept, fit.intercept_stderr)],
    ['Slope', pm(fit.slope, fit.slope_stderr)],
    ['Residual Sum of Squares', sig(fit.rss)],
    ["Pearson's r", sig(fit.pearson_r)],
    ['R-Square (COD)', sig(fit.r_squared)],
    ['Adj. R-Square', sig(fit.adj_r_squared)],
    ['Number of Points', String(fit.n_points)],
    ['Degrees of Freedom', String(fit.dof)],
    ['Prob>|t| (Slope)', fit.slope_p === null ? '—' : fit.slope_p.toExponential(4)],
    ['활성화에너지', ea.activation_energy_ev === null ? '—'
      : `${ev(ea.activation_energy_ev)}`
        + `${ea.stderr_ev === null ? '' : ` ± ${ea.stderr_ev.toFixed(3)}`} eV`],
  ]
  return (
    <div className="table-wrap" style={{ marginTop: 12 }}>
      <table>
        <tbody>
          {rows.map(([label, value]) => (
            <tr key={label}>
              <td className="text dim" style={{ width: 200 }}>{label}</td>
              <td className="text">{value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

/** 이 줄의 저항이 어디서 왔는지, 그리고 아직이라면 읽을 수 있는 수들. */
function readings(row: ConductivityRow): string {
  const source = sourceLabel(row.resistance_source)
  if (source) return source
  const offered: string[] = []
  if (row.crossing_ohm !== null) offered.push(`교점 ${num(row.crossing_ohm, 3)}`)
  if (row.fit_ohm !== null) offered.push(`fitting ${num(row.fit_ohm, 3)}`)
  return offered.length ? offered.join(' · ') : '—'
}

function pm(value: number, stderr: number | null): string {
  if (stderr === null) return sig(value)
  return `${sig(value)} ± ${sig(stderr)}`
}

/** 두께와 면적 — 스윕 하나에 적으면 나머지가 따라간다 (`SCAN_SHARED_FIELDS`).
 *
 *  **mm 로 받고 µm 로 저장한다.**  캘리퍼가 읽는 것도 슬라이드에 적힌 것도 mm
 *  이고(0.79 mm), DB 의 칸은 예전부터 µm 다.  바꾼 값을 옆에 되읽어 준다 —
 *  이 자리에서 천 배 틀리면 이온전도도가 천 배 틀린다.
 */
function Geometry({ rows, onSaved }: {
  rows: ConductivityRow[]
  onSaved: () => void
}) {
  const first = rows[0]
  const [thickness, setThickness] = useState('')
  const [area, setArea] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [said, setSaid] = useState('')

  useEffect(() => {
    setThickness(first?.thickness_mm === null || first?.thickness_mm === undefined
      ? '' : String(first.thickness_mm))
    setArea(first?.area_cm2 === null || first?.area_cm2 === undefined
      ? '' : String(first.area_cm2))
  }, [first?.thickness_mm, first?.area_cm2])

  const micro = Number(thickness) > 0 ? Number(thickness) * 1000 : null

  async function save() {
    if (!first) return
    setBusy(true)
    setError(null)
    try {
      const body: Record<string, unknown> = {}
      const clear: string[] = []
      if (thickness.trim() === '') clear.push('thickness_um')
      else body.thickness_um = Number(thickness) * 1000
      if (area.trim() === '') clear.push('area_cm2')
      else body.area_cm2 = Number(area)
      if (clear.length) body.clear = clear
      await api.updateSpectrum(first.spectrum_id, body)
      setSaid(`스윕 ${rows.length}개에 적용했습니다`)
      onSaved()
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause))
    } finally {
      setBusy(false)
    }
  }

  return (
    <Card title="두께와 면적" tight>
      <div className="row" style={{ padding: 14, gap: 14, flexWrap: 'wrap',
                                    alignItems: 'flex-end' }}>
        <Field label="두께 (mm)" hint={micro ? `= ${num(micro, 0)} µm 로 저장` : 'mm 로 적습니다'}>
          <input type="number" min={0} step="0.01" value={thickness} disabled={busy}
                 aria-label="두께 (mm)"
                 onChange={(event) => setThickness(event.target.value)} />
        </Field>
        <Field label="면적 (cm²)" hint="σ 의 분모 · 스윕 전부에 함께 적용됩니다">
          <input type="number" min={0} step="0.0001" value={area} disabled={busy}
                 aria-label="면적 (cm²)"
                 onChange={(event) => setArea(event.target.value)} />
        </Field>
        <button type="button" disabled={busy || !first} onClick={() => void save()}>
          적용
        </button>
        {said ? <span className="tiny dim">{said}</span> : null}
        <div className="tiny dim" style={{ flexBasis: '100%' }}>
          σ = 두께 / (저항 × 면적). EC-Lab 이 `.mpt` 에 함께 적어 둔 전도도 열은
          쓰지 않습니다 — 머리말의 <code>Electrode surface area : 0.001 cm2</code> 는
          아무도 안 고친 기본값이라, 실제 면적이 0.85 cm² 면 850배 틀립니다.
        </div>
      </div>
      {error ? <Alert kind="error">{error}</Alert> : null}
    </Card>
  )
}

/** 스윕 차례대로 한 줄에 적는 칸 — 온도와 저항이 같은 모양을 쓴다.
 *
 *  **되읽어 준다.**  `(60, -20, 9)` 가 무엇으로 펼쳐졌는지 눈으로 보이지 않으면,
 *  아홉 개를 적었다고 믿는 채로 여덟 개가 들어가는 일이 생긴다.
 */
function ValueRow({
  title, hint, example, unit, what, sweeps, current,
  suggestions = [], onSave, onSaved,
}: {
  title: string
  hint: string
  example: string
  unit: string
  what: string
  sweeps: number
  current: (number | null)[]
  /** 눌러야 들어가는 읽기들.  값이 하나도 없는 것은 단추가 안 선다. */
  suggestions?: { label: string; values: (number | null)[] }[]
  onSave: (values: (number | null)[]) => Promise<unknown>
  onSaved: () => void
}) {
  const [text, setText] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [said, setSaid] = useState('')

  //: 이미 적혀 있는 것을 칸에 미리 넣어 둔다 — 고치러 온 사람이 다시 치지
  //  않게.  하나도 없으면 빈칸으로 둔다 (`—, —, —` 은 적은 것처럼 보인다).
  //
  //  배열이 아니라 **적힌 한 줄**을 의존성에 둔다.  배열은 렌더마다 새로
  //  만들어져 항상 달라 보이고, 그러면 사람이 치는 중에도 이 효과가 돌아 칸을
  //  서버 값으로 되돌린다.
  const written = current.some((one) => one !== null)
    ? current.map((one) => (one === null ? '-' : String(one))).join(', ')
    : ''
  useEffect(() => setText(written), [written])

  const list = useMemo(() => parseValueList(text), [text])
  const problem = listProblem(list, sweeps, what)

  const offered = suggestions.filter(
    (one) => one.values.some((value) => value !== null))

  return (
    <Card title={title} tight>
      <div className="col" style={{ padding: 14, gap: 8 }}>
        <div className="row" style={{ gap: 10, flexWrap: 'wrap', alignItems: 'center' }}>
          <input
            aria-label={`${title} 목록`}
            style={{ flex: 1, minWidth: 280 }}
            value={text}
            disabled={busy}
            placeholder={hint}
            onChange={(event) => setText(event.target.value)}
          />
          <button
            type="button"
            disabled={busy || !!problem || !list.values.length}
            onClick={async () => {
              setBusy(true)
              setError(null)
              try {
                await onSave(list.values)
                setSaid(`${list.values.length}개를 적었습니다`)
                onSaved()
              } catch (cause) {
                setError(cause instanceof Error ? cause.message : String(cause))
              } finally {
                setBusy(false)
              }
            }}
          >
            적용
          </button>
          {offered.map((one) => (
            <button
              key={one.label}
              type="button"
              className="ghost tiny"
              disabled={busy}
              title="제안입니다 — 눌러야 들어갑니다"
              onClick={() => setText(one.values
                .map((value) => (value === null
                  ? '-' : String(Number(value.toPrecision(4)))))
                .join(', '))}
            >
              {one.label} 채우기
            </button>
          ))}
          {said && !problem ? <span className="tiny dim">{said}</span> : null}
        </div>
        {/* 회색 예시 — 형식을 외우게 하지 않는다. */}
        <div className="tiny faint">{example}</div>
        {list.expanded && !problem ? (
          <div className="tiny dim">
            펼치면 <b>{describeValues(list.values, unit)}</b> 입니다.
          </div>
        ) : null}
        {problem ? <Alert kind="warn">{problem}</Alert> : null}
        {error ? <Alert kind="error">{error}</Alert> : null}
      </div>
    </Card>
  )
}
