/** 이 셀의 다른 측정 — 세 섹션이 서로를 가리키는 한 줄.
 *
 *  섹션은 나뉘어 있다: 충방전·EIS·GITT 는 각자 대시보드와 목록과 비교를
 *  갖는다.  나눈 것은 **화면**이지 셀이 아니다.  같은 셀을 세 번 재 놓고
 *  세 화면을 따로 찾아 들어가야 한다면 그건 나눈 것이 아니라 흩어 놓은 것이다.
 *
 *  붙어 있는 것만 나온다.  이름이 비슷하다고 같은 셀로 묶지 않는다 — 이름은
 *  기록이지 관계가 아니다 (ADR 0012).  그래서 아무것도 없으면 이 카드는 아예
 *  그려지지 않는다: "다른 측정 없음" 은 셀에 대한 사실이 아니라 아직 아무도
 *  붙이지 않았다는 뜻이고, 그것을 크게 적으면 없는 정보가 정보처럼 보인다.
 */

import { Link } from 'react-router-dom'

import { Card } from './ui'
import { useAsync } from '../lib/hooks'
import { api } from '../lib/api'
import type { Measurement } from '../lib/types'

/** 어느 종류가 어디로 가는가.  한 곳에만 적는다 — 경로가 바뀌면 세 화면이
 *  같이 따라와야 하고, 갈라 두면 한쪽만 고치게 된다. */
const ROUTE: Record<Measurement['kind'], (id: number) => string> = {
  cycling: (id) => `/samples/${id}`,
  eis: (id) => `/eis/${id}`,
  gitt: (id) => `/gitt/${id}`,
}

const LABEL: Record<Measurement['kind'], string> = {
  cycling: '충방전',
  eis: 'EIS',
  gitt: 'GITT',
}

export function OtherMeasurements({
  sampleId,
  exclude,
}: {
  sampleId: number | null
  /** 지금 보고 있는 것.  자기 자신을 "다른 측정" 으로 내놓으면 안 된다. */
  exclude?: { kind: Measurement['kind']; id: number }
}) {
  const found = useAsync(
    () => (sampleId === null ? Promise.resolve(null) : api.measurements(sampleId)),
    [sampleId],
  )

  const data = found.data
  if (!data) return null

  // 목록이 없을 수 있다고 보는 것은 방어가 아니라 **층위**의 문제다.  이 카드는
  // 남의 화면에 얹히는 곁가지이고, 셀 상세·스펙트럼 상세·GITT 상세가 그
  // 화면들이다.  여기서 던진 예외는 React 가 그 화면 전체를 지우게 만든다 --
  // 곁가지 하나 때문에 사람이 보러 온 것이 사라지는 것은 옳지 않다.
  const cycling = data.cycling ?? []
  const eis = data.eis ?? []
  const gitt = data.gitt ?? []

  // cycling 은 셀 상세로 가는데, 그 셀의 run 이 여럿이어도 화면은 하나다.
  // 링크를 run 마다 만들면 같은 곳으로 가는 줄이 여러 개 생긴다.
  const rows: Measurement[] = [
    ...(cycling.length
      ? [{
          kind: 'cycling' as const,
          id: sampleId as number,
          name: data.sample_name ?? '충방전',
          detail: cycling.map((m) => m.detail).join(' · '),
          measured_at: cycling[0]?.measured_at ?? null,
        }]
      : []),
    ...eis,
    ...gitt,
  ].filter((m) => !(exclude && m.kind === exclude.kind && m.id === exclude.id))

  if (!rows.length) return null

  return (
    <Card title="이 셀의 다른 측정" tight>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th style={{ textAlign: 'left' }}>종류</th>
              <th style={{ textAlign: 'left' }}>이름</th>
              <th style={{ textAlign: 'left' }}>내용</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((item) => (
              <tr key={`${item.kind}-${item.id}`}>
                <td className="text dim">{LABEL[item.kind]}</td>
                <td className="text">
                  <Link to={ROUTE[item.kind](item.id)}>{item.name}</Link>
                </td>
                <td className="text dim">{item.detail || '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )
}
