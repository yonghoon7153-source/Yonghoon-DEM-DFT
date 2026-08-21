/** 셀 라이브러리의 묶기.
 *
 * 그룹은 사람이 만들어 붙이는 것이라, 그룹을 만들기 전에는 "같은 조건 세 번
 * 돌린 것" 을 나란히 볼 방법이 없었다. 이름으로 묶으면 그 전에도 보인다.
 *
 * 틀릴 수 있는 방식이 둘이다. 서로 다른 셀을 한 묶음에 넣거나(그러면 세 배로
 * 보이는 반복 실험이 실은 다른 조건이다), 같은 것을 갈라 놓거나.
 */

import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { Library } from '../../pages/Library'
import type { ResolvedCell, Sample } from '../types'

const CELL: ResolvedCell = {
  active_mass_g: null,
  active_wt_percent: null,
  composition: [],
  composition_label: '',
  composition_compact_label: '',
  composition_problems: [],
  area_cm2: null,
  volume_cm3: null,
  loading_mg_cm2: null,
  nominal_capacity_mah: null,
  nominal_specific_capacity_mah_g: null,
  available_bases: ['mAh'],
  unavailable: {},
  notes: {},
}

function sample(id: number, name: string, overrides: Partial<Sample> = {}): Sample {
  return {
    id,
    name,
    group_id: null,
    group_name: null,
    test_date: null,
    cathode_type: '',
    cathode_detail: '',
    anode: '',
    electrolyte: '',
    process: '',
    notes: '',
    total_mass_mg: null,
    current_collector_mass_mg: null,
    active_wt_percent: null,
    active_mass_mg: null,
    area_cm2: null,
    diameter_mm: null,
    thickness_um: null,
    nominal_specific_capacity_mah_g: null,
    composition: [],
    composition_label: '',
    temperature_c: null,
    pressure_mpa: null,
    cutoff_upper_v: null,
    cutoff_lower_v: null,
    c_rate: null,
    c_rate_formation: null,
    reference_cycle: 3,
    declared_state: 'auto',
    created_at: '2026-08-01T00:00:00',
    updated_at: '2026-08-01T00:00:00',
    run_count: 1,
    cycle_count: 5,
    resolved_cell: CELL,
    ...overrides,
  }
}

const SAMPLES = [
  sample(1, '4.6V_1_17.5mg', { process: 'dry' }),
  sample(2, '4.6V_2_18.1mg', { process: 'dry' }),
  sample(3, '4.0V_post_formation_18.9mg', { process: 'wet' }),
]

function installFetch(samples: Sample[] = SAMPLES) {
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string) => {
      const path = url.split('?')[0] ?? url
      const body =
        path === '/api/samples'
          ? samples
          : path === '/api/samples/facets'
            ? {
                cathode_type: [], cathode_detail: [], process: [], electrolyte: [],
                anode: [], c_rate: [], temperature_c: [], test_date: [], bases: [],
              }
            : []
      return { ok: true, status: 200, statusText: 'OK', json: async () => body }
    }),
  )
}

function renderLibrary() {
  return render(
    <MemoryRouter>
      <Library />
    </MemoryRouter>,
  )
}

/** 구분 줄들, 화면에 있는 순서대로. */
function sections(): string[] {
  return [...document.querySelectorAll('tr.section th')].map((node) =>
    (node.textContent ?? '').trim(),
  )
}

beforeEach(() => {
  window.localStorage.clear()
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('라이브러리 묶기', () => {
  it('처음에는 안 묶는다 — 셋을 한 줄씩', async () => {
    installFetch()
    renderLibrary()

    await screen.findByText('4.6V_1_17.5mg')
    expect(sections()).toEqual([])
  })

  it('이름으로 묶으면 반복 실험이 한 덩어리가 된다', async () => {
    installFetch()
    renderLibrary()
    await screen.findByText('4.6V_1_17.5mg')

    await userEvent.click(screen.getByRole('button', { name: '이름' }))

    // `_1_17.5mg` 과 `_2_18.1mg` 은 같은 조건을 두 번 돌린 것이다.
    await waitFor(() => expect(sections()).toEqual(['4.0V_post_formation · 1개', '4.6V · 2개']))
  })

  it('묶어도 셀이 사라지지 않는다', async () => {
    installFetch()
    renderLibrary()
    await screen.findByText('4.6V_1_17.5mg')

    await userEvent.click(screen.getByRole('button', { name: '이름' }))

    await waitFor(() => expect(sections()).toHaveLength(2))
    for (const item of SAMPLES) {
      expect(screen.getByText(item.name)).toBeInTheDocument()
    }
  })

  it('값이 없는 묶음은 맨 아래로 — 빈 칸이 목록의 첫인상이 되면 안 된다', async () => {
    installFetch([
      sample(1, 'A', { process: 'dry' }),
      sample(2, 'B'),                       // 공정 미입력
      sample(3, 'C', { process: 'wet' }),
    ])
    renderLibrary()
    await screen.findByText('A')

    await userEvent.click(screen.getByRole('button', { name: '공정' }))

    await waitFor(() => expect(sections()).toEqual(['dry · 1개', 'wet · 1개', '미입력 · 1개']))
  })

  it('고른 기준이 다음에도 남는다', async () => {
    installFetch()
    const first = renderLibrary()
    await screen.findByText('4.6V_1_17.5mg')
    await userEvent.click(screen.getByRole('button', { name: '이름' }))
    await waitFor(() => expect(sections()).toHaveLength(2))
    first.unmount()

    renderLibrary()
    await screen.findByText('4.6V_1_17.5mg')
    await waitFor(() => expect(sections()).toHaveLength(2))
  })

  it('묶은 표와 안 묶은 표가 같은 열을 쓴다', async () => {
    // 머리와 데이터가 한 칸씩 밀리는 것은 눈에 잘 안 띄는데, 밀린 채로 읽은
    // 로딩이나 C-rate 는 다른 셀의 값이다.
    installFetch()
    renderLibrary()
    await screen.findByText('4.6V_1_17.5mg')
    const flat = document.querySelectorAll('thead th').length

    await userEvent.click(screen.getByRole('button', { name: '이름' }))
    await waitFor(() => expect(sections()).toHaveLength(2))

    expect(document.querySelectorAll('thead th')).toHaveLength(flat)
    const [first] = [...document.querySelectorAll('tr.section th')]
    expect(first?.getAttribute('colspan')).toBe(String(flat))
  })

  it('한 줄에 한 셀 — 묶어도 데이터 행 수는 그대로다', async () => {
    installFetch()
    renderLibrary()
    await screen.findByText('4.6V_1_17.5mg')

    await userEvent.click(screen.getByRole('button', { name: '이름' }))
    await waitFor(() => expect(sections()).toHaveLength(2))

    const table = document.querySelector('table') as HTMLTableElement
    const dataRows = within(table).getAllByRole('row').filter(
      (row) => row.querySelector('td') !== null,
    )
    expect(dataRows).toHaveLength(SAMPLES.length)
  })
})
