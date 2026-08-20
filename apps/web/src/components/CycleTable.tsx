import { basisUnit, num, pct } from '../lib/format'
import type { Basis, Cycle } from '../lib/types'

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
            <th>충전 ({unit})</th>
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
              <td>{num(cycle.charge_capacity)}</td>
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
