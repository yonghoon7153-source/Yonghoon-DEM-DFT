import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'

import { BasisSelect } from '../BasisSelect'
import type { ResolvedCell } from '../../lib/types'

const cell: ResolvedCell = {
  active_mass_g: null,
  area_cm2: 1.327,
  volume_cm3: null,
  loading_mg_cm2: null,
  nominal_capacity_mah: null,
  nominal_specific_capacity_mah_g: null,
  available_bases: ['mAh', 'mAh/cm2'],
  unavailable: {
    'mAh/g': 'active mass not set',
    'mAh/cm3': 'electrode area and thickness not set',
    '%': 'active mass and nominal specific capacity not set',
  },
  notes: {},
}

describe('BasisSelect', () => {
  it('disables a basis the cell cannot express, and says why', () => {
    render(<BasisSelect value="mAh" onChange={() => {}} cell={cell} />)
    const specific = screen.getByRole('button', { name: 'mAh/g' })
    expect(specific).toBeDisabled()
    expect(specific).toHaveAttribute('title', expect.stringContaining('active mass not set'))
  })

  it('leaves an available basis selectable', async () => {
    const onChange = vi.fn()
    render(<BasisSelect value="mAh" onChange={onChange} cell={cell} />)
    await userEvent.click(screen.getByRole('button', { name: 'mAh/cm²' }))
    expect(onChange).toHaveBeenCalledWith('mAh/cm2')
  })

  it('enables everything when no cell is given', () => {
    render(<BasisSelect value="mAh" onChange={() => {}} />)
    expect(screen.getByRole('button', { name: 'mAh/g' })).toBeEnabled()
  })
})
