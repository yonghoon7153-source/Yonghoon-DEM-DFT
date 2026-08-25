/** 이 셀의 임피던스 — 셀 상세 아래에 붙는다.
 *
 *  전고체 과제는 구동 전과 200 사이클 뒤를 재서 **둘을 비교**한다.  그 비교가
 *  목적이므로 두 나이퀴스트를 한 그림에 겹쳐 볼 수 있어야 하고, 고르는 방식은
 *  전압 곡선에서 사이클을 고르는 것과 같다.
 *
 *  GITT 는 여기 없다.  충방전을 찍다가 EIS 를 찍는 일은 흔하지만 GITT 를 중간에
 *  끼우는 일은 드물어서, 그쪽은 독자 섹션으로 둔다.
 */

import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { CopyBar } from './CopyBar'
import { Plot, type PlotSeries } from './Plot'
import { Alert, Card, Empty, Spinner } from './ui'
import { api } from '../lib/api'
import { num, seriesColor } from '../lib/format'
import { nyquistTsv } from '../lib/origin'
import { useAsync } from '../lib/hooks'

//: 서버의 /api/eis/points 겹치기 상한과 같은 수.
const OVERLAY_LIMIT = 12

export function CellSpectra({ sampleId }: { sampleId: number }) {
  const [chosen, setChosen] = useState<number[] | null>(null)
  const spectra = useAsync(() => api.listSpectra({ sample_id: sampleId }),
                           [sampleId], { live: true })
  const rows = useMemo(() => spectra.data ?? [], [spectra.data])

  // 처음에는 켤 수 있는 만큼 켠다.  둘을 비교하려고 들어온 화면에서 아무것도
  // 안 켜져 있으면, 켜는 법을 찾기 전에 그래프가 비어 있는 이유부터 찾게
  // 된다.  단 서버는 한 번에 12개까지만 겹쳐 주므로 13개째부터는 꺼 둔다 —
  // 전부 보내면 첫 화면부터 422 다 (리뷰 #30).
  useEffect(() => {
    if (chosen === null && rows.length) {
      setChosen(rows.slice(0, OVERLAY_LIMIT).map((row) => row.id))
    }
  }, [rows, chosen])

  const selected = useMemo(
    () => (chosen ?? []).filter((id) => rows.some((row) => row.id === id)),
    [chosen, rows],
  )
  const points = useAsync(
    () => (selected.length ? api.spectraPoints(selected) : Promise.resolve([])),
    [selected.join(',')],
  )
  // 응답이 지금 고른 집합의 것인지.  선택을 바꾸는 사이 옛 응답이 남아
  // 있으면 칩은 꺼져 있는데 그래프와 클립보드는 켜진 집합을 말한다 (#30).
  const fresh = useMemo(() => {
    const got = (points.data ?? []).map((item) => item.id).sort().join(',')
    return got === [...selected].sort().join(',')
  }, [points.data, selected])

  const series = useMemo<PlotSeries[]>(() => {
    if (!fresh) return []
    const data = points.data ?? []
    return data.map((item) => ({
      label: spectrumLabel(item),
      x: item.z_re,
      // 나이퀴스트 세로축은 −Z″ 다.
      y: item.z_im.map((value) => -value),
      // 색은 행 순서로 — 곡선을 하나 꺼도 남은 곡선의 색이 칩과 같아야 한다.
      color: seriesColor(rows.findIndex((row) => row.id === item.id)),
      points: true,
      width: 1,
    }))
  }, [points.data, fresh, rows])

  if (spectra.error) {
    return (
      <Card title="임피던스 (EIS)">
        <Alert kind="error">{spectra.error}</Alert>
      </Card>
    )
  }
  if (!rows.length) {
    return (
      <Card title="임피던스 (EIS)">
        <Empty title="이 셀에 붙은 스펙트럼이 없습니다" icon="∿">
          <Link to="/eis/upload">EIS 업로드로 가기</Link>
        </Empty>
      </Card>
    )
  }

  return (
    <Card
      title={`임피던스 (EIS) ${rows.length}개`}
      actions={
        <div className="row" style={{ gap: 6 }}>
          <button type="button"
                  onClick={() => setChosen(rows.slice(0, OVERLAY_LIMIT).map((row) => row.id))}>
            {rows.length > OVERLAY_LIMIT ? `처음 ${OVERLAY_LIMIT}개` : '전부'}
          </button>
          <button type="button" onClick={() => setChosen([])}>
            비우기
          </button>
          <Link className="link-btn" to="/eis">
            EIS 섹션
          </Link>
        </div>
      }
    >
      <div className="col" style={{ gap: 10 }}>
        <div className="chips">
          {rows.map((row, index) => {
            const on = selected.includes(row.id)
            return (
              <button
                key={row.id}
                type="button"
                className={on ? 'chip on' : 'chip'}
                aria-pressed={on}
                onClick={() =>
                  setChosen((current) => {
                    const now = current ?? rows.slice(0, OVERLAY_LIMIT).map((item) => item.id)
                    if (now.includes(row.id)) return now.filter((id) => id !== row.id)
                    if (now.length >= OVERLAY_LIMIT) return now  // 안내는 아래 문구가
                    return [...now, row.id]
                  })
                }
              >
                <span className="dot" style={{ background: seriesColor(index) }} />
                {spectrumLabel(row)}
              </button>
            )
          })}
        </div>

        {rows.length > OVERLAY_LIMIT ? (
          <div className="tiny faint">
            한 번에 {OVERLAY_LIMIT}개까지만 겹쳐 그립니다 — 나머지는 칩을 꺼서
            바꿔 켜 주세요.
          </div>
        ) : null}

        <CopyBar
          items={[{
            label: '나이퀴스트',
            title: '고른 곡선을 Z′·−Z″ 두 열로 쌓아서',
            // 고른 집합의 응답이 아직 안 왔으면 옛 집합을 복사하게 된다.
            disabled: !fresh || !points.data?.length,
            build: () => nyquistTsv(points.data ?? []),
          }]}
        />

        {points.error ? <Alert kind="error">{points.error}</Alert> : null}

        {selected.length === 0 ? (
          // 빈 그래프는 고장처럼 보인다.
          <div className="tiny faint" style={{ padding: 12 }}>
            고른 스펙트럼이 없습니다.
          </div>
        ) : points.loading && !points.data ? (
          <Spinner />
        ) : series.length ? (
          <Plot
            series={series}
            xLabel="Z′ (Ω)"
            yLabel="−Z″ (Ω)"
            height={320}
            legend
            equalAspect
            positiveFit
          />
        ) : null}

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th style={{ textAlign: 'left' }}>이름</th>
                <th>사이클</th>
                <th style={{ textAlign: 'left' }}>종류</th>
                <th>점</th>
                <th>χ²</th>
                <th style={{ textAlign: 'left' }}>회로</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.id}>
                  <td className="text">
                    <Link to={`/eis/${row.id}`}>{row.name}</Link>
                  </td>
                  <td>{row.at_cycle === null ? '—' : row.at_cycle}</td>
                  <td className="text dim">
                    {row.kind === 'solid' ? '전고체' : '액체'}
                    {row.cell_config ? ` · ${CONFIGS[row.cell_config]}` : ''}
                  </td>
                  <td>{row.n_points}</td>
                  <td>
                    {row.best_chi_squared === null ? '—' : num(row.best_chi_squared, 3)}
                  </td>
                  <td className="text dim mono">{row.best_circuit || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </Card>
  )
}

const CONFIGS: Record<string, string> = { sym: '대칭셀', full: '풀셀', half: '하프셀' }

/** "0 사이클" · "200 사이클" · 번호가 없으면 이름 그대로.
 *
 *  범례에 파일 이름이 그대로 들어가면 두 곡선의 이름이 열두 글자쯤 같고 끝만
 *  다르다.  비교하려고 겹쳐 놓은 그림에서 그것은 이름이 없는 것과 같다. */
export function spectrumLabel(spectrum: {
  name: string
  at_cycle: number | null
}): string {
  if (spectrum.at_cycle === null) return spectrum.name
  return spectrum.at_cycle === 0 ? '구동 전' : `${spectrum.at_cycle} 사이클`
}
