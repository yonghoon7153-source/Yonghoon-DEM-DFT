import { ko } from '../lib/i18n'
import type { Basis, ResolvedCell } from '../lib/types'

const OPTIONS: { value: Basis; label: string }[] = [
  { value: 'mAh', label: 'mAh' },
  { value: 'mAh/g', label: 'mAh/g' },
  { value: 'mAh/cm2', label: 'mAh/cm²' },
  { value: 'mAh/cm3', label: 'mAh/cm³' },
  { value: '%', label: '% 활용률' },
]

/** Capacity-axis picker.
 *
 * An axis the sample cannot express is disabled rather than hidden, with the
 * missing input named in the tooltip -- that is the fastest route from "why
 * can't I pick mAh/g" to "because the mass is blank".
 */
export function BasisSelect({
  value,
  onChange,
  cell,
}: {
  value: Basis
  onChange: (basis: Basis) => void
  cell?: ResolvedCell | null
}) {
  return (
    <div className="segmented" role="group" aria-label="용량 기준">
      {OPTIONS.map((option) => {
        const missing = cell?.unavailable?.[option.value]
        const disabled = Boolean(cell && missing)
        return (
          <button
            key={option.value}
            type="button"
            className={value === option.value ? 'on' : ''}
            disabled={disabled}
            title={disabled ? `사용 불가 — ${ko.basisReason(missing!)}` : undefined}
            onClick={() => onChange(option.value)}
          >
            {option.label}
          </button>
        )
      })}
    </div>
  )
}
