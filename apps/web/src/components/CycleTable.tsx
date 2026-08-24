import { basisUnit, num, pct } from '../lib/format'
import type { Basis, Cycle } from '../lib/types'

/** 단차 한 칸 — 부호를 남기고, 없으면 이유가 있어서 없다는 뜻으로 비운다.
 *
 * 부호가 중요하다.  초기 사이클에는 활성화로 용량이 **오르는** 셀이 실제로
 * 있고, 절대값으로 찍으면 그것이 열화와 구분되지 않는다.  그래서 +/- 를 붙이고
 * 색으로도 갈라 준다.
 *
 * 첫 사이클과 구동 중인 사이클은 빈칸이다.  0 을 찍으면 "변화가 없었다" 로
 * 읽히는데, 실제로는 "비교할 것이 없다" 이다. */
function Delta({ value, digits = 3 }: { value: number | null | undefined; digits?: number }) {
  if (value === null || value === undefined) return <span className="faint">—</span>
  const sign = value > 0 ? '+' : ''
  return (
    <span style={{ color: value < 0 ? 'var(--discharge)' : undefined }}>
      {sign}
      {num(value, digits)}
    </span>
  )
}

export function CycleTable({
  cycles,
  basis,
  selected,
  onSelect,
  referenceCycle,
}: {
  cycles: Cycle[]
  basis: Basis
  selected?: number[]
  onSelect?: (cycle: number) => void
  referenceCycle?: number | null
}) {
  const unit = basisUnit(basis)
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>사이클</th>
            <th>방전 ({unit})</th>
            {/* 단차는 그 옆에 붙어야 뜻이 산다 — 값과 그 값의 변화는 같이 읽는다. */}
            <th title="직전 완료 사이클 대비 방전용량 변화. 유지율(기준 사이클 대비)과는 다른 질문입니다.">
              Δ방전 ({unit})
            </th>
            <th title="같은 단차를 직전 사이클 대비 백분율로">Δ (%)</th>
            <th>충전 ({unit})</th>
            <th title="직전 완료 사이클 대비 충전용량 변화">Δ충전 ({unit})</th>
            <th>CE (%)</th>
            <th>유지율 (%)</th>
            <th>평균 방전 V</th>
            <th>ΔV</th>
            <th>에너지효율 (%)</th>
            <th>C-rate</th>
            <th>시간</th>
          </tr>
        </thead>
        <tbody>
          {cycles.map((cycle) => (
            <tr
              key={`${cycle.run_id}-${cycle.cycle}`}
              className={[
                selected?.includes(cycle.cycle) ? 'selected' : '',
                cycle.complete ? '' : 'incomplete',
                onSelect ? 'clickable' : '',
              ]
                .filter(Boolean)
                .join(' ')}
              onClick={() => onSelect?.(cycle.cycle)}
            >
              <td className="text">
                {cycle.cycle}
                {referenceCycle === cycle.cycle ? (
                  <span className="badge plain" style={{ marginLeft: 5 }}>
                    기준
                  </span>
                ) : null}
                {cycle.complete ? null : (
                  <span className="badge warn" style={{ marginLeft: 5 }}>
                    진행 중
                  </span>
                )}
              </td>
              <td>{num(cycle.discharge_capacity)}</td>
              <td
                title={
                  cycle.delta_base_cycle
                    ? `${cycle.delta_base_cycle}번 대비` +
                      (cycle.delta_span && cycle.delta_span > 1
                        ? ` · ${cycle.delta_span}사이클치 (사이클당 ${num(cycle.discharge_delta_per_cycle, 4)})`
                        : '')
                    : undefined
                }
              >
                <Delta value={cycle.discharge_delta} />
                {/* 사이의 사이클이 빠져 있으면 그 단차는 한 사이클치가 아니다.
                    표시가 없으면 다섯 사이클치 열화를 한 사이클로 읽는다. */}
                {cycle.delta_span && cycle.delta_span > 1 ? (
                  <span className="badge plain" style={{ marginLeft: 4 }}>
                    ×{cycle.delta_span}
                  </span>
                ) : null}
              </td>
              <td>
                <Delta value={cycle.discharge_delta_pct} digits={2} />
              </td>
              <td>{num(cycle.charge_capacity)}</td>
              <td>
                <Delta value={cycle.charge_delta} />
              </td>
              <td>{pct(cycle.coulombic_efficiency)}</td>
              <td>{pct(cycle.retention_pct, 1)}</td>
              <td>{num(cycle.mean_discharge_voltage, 4)}</td>
              <td>{num(cycle.voltage_hysteresis, 3)}</td>
              <td>{pct(cycle.energy_efficiency, 1)}</td>
              <td>{cycle.c_rate ? `${num(cycle.c_rate, 3)}C` : '—'}</td>
              <td>{cycle.duration_h.toFixed(1)} h</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
