/** Page-level regressions for the ways a screen can mislead.
 *
 * Every case here is one where the screen used to state something the data did
 * not support: a mixed-unit axis presented as normalised, a raw mAh row under a
 * mAh/g header, a failed fetch shown as "all attached", a stale cycle table
 * after a file was deleted, a half-typed reference cycle committed to the DB.
 */

import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

// uPlot reads matchMedia at import time to pick a pixel ratio, and jsdom has
// none; hoisted so it exists before the pages (and uPlot) are imported.
vi.hoisted(() => {
  const media = (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener() {},
    removeListener() {},
    addEventListener() {},
    removeEventListener() {},
    dispatchEvent: () => false,
  })
  globalThis.matchMedia = globalThis.matchMedia ?? (media as never)
})

import { Compare } from '../../pages/Compare'
import { Dashboard } from '../../pages/Dashboard'
import { SampleDetail } from '../../pages/SampleDetail'
import { Upload } from '../../pages/Upload'
import type { Cycle, DashboardRow, ResolvedCell, Run, Sample } from '../types'

// -- fetch double ----------------------------------------------------------

class Fail {
  constructor(
    readonly status: number,
    readonly detail: string,
  ) {}
}

type Handler = (url: string, init?: RequestInit) => unknown

function installFetch(handler: Handler) {
  const spy = vi.fn(async (url: string, init?: RequestInit) => {
    const result = handler(url, init)
    if (result instanceof Fail) {
      return {
        ok: false,
        status: result.status,
        statusText: 'Error',
        json: async () => ({ detail: result.detail }),
      }
    }
    return { ok: true, status: 200, statusText: 'OK', json: async () => result ?? {} }
  })
  vi.stubGlobal('fetch', spy)
  return spy
}

function path(url: string): string {
  return url.split('?')[0] ?? url
}

// -- fixtures --------------------------------------------------------------

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

function sample(overrides: Partial<Sample> = {}): Sample {
  return {
    id: 1,
    name: 'No_1_dry',
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

function cycle(number: number): Cycle {
  return {
    cycle: number,
    cycle_index: number - 1,
    run_id: 1,
    charge_capacity: 5.4,
    discharge_capacity: 5.25,
    charge_capacity_mah: 5.4,
    discharge_capacity_mah: 5.25,
    coulombic_efficiency: 97.2,
    energy_efficiency: 91.1,
    charge_energy_mwh: 20,
    discharge_energy_mwh: 18,
    mean_charge_voltage: 3.9,
    mean_discharge_voltage: 3.6,
    voltage_hysteresis: 0.3,
    voltage_max: 4.3,
    voltage_min: 2.5,
    retention_pct: 100,
    c_rate: 0.2,
    temperature_mean: 25,
    duration_h: 10,
    n_points: 500,
    complete: true,
  }
}

function run(overrides: Partial<Run> = {}): Run {
  return {
    id: 11,
    sample_id: 1,
    sample_name: 'No_1_dry',
    original_name: 'No_1_dry_011.wrd',
    sha256: 'abc',
    size_bytes: 1024,
    uploaded_at: '2026-08-01T00:00:00',
    device_model: 'WBCS3000',
    serial_no: 'SN1',
    channel: 3,
    app_version: '1',
    firmware_version: '1',
    start_time: '2026-07-01T00:00:00',
    end_time: '2026-07-05T00:00:00',
    row_count: 1000,
    cycle_count: 5,
    complete_cycle_count: 5,
    unit_coulomb: false,
    data_format: 0,
    instrument_path: '',
    schedule_path: '',
    cycle_offset: 0,
    cycle_offset_source: 'auto',
    parse_error: '',
    schedule: {},
    ...overrides,
  }
}

function dashboardRow(overrides: Partial<DashboardRow> = {}): DashboardRow {
  return {
    sample_id: 1,
    sample_name: 'A',
    group_id: null,
    cathode_type: '',
    c_rate: null,
    temperature_c: null,
    test_date: null,
    state: 'finished',
    state_confidence: 'high',
    in_progress_cycle: null,
    cycles_complete: 30,
    reported_cycle: 30,
    discharge_capacity: 207.7,
    discharge_capacity_mah: 5.25,
    retention_pct: 95,
    reference_cycle: 3,
    reference_available: true,
    initial_coulombic_efficiency: 88,
    knee_cycle: null,
    knee_method: null,
    basis: 'mAh/g',
    loading_mg_cm2: null,
    composition_label: '',
    trend: [100, 98],
    trend_first_cycle: 3,
    trend_last_cycle: 30,
    knee_trend_index: null,
    ...overrides,
  }
}

const META = {
  bases: [],
  states: [],
  knee_methods: [],
  default_plot_points: 2000,
  composition_presets: [],
  component_roles: [],
}

function renderSampleDetail() {
  return render(
    <MemoryRouter initialEntries={['/samples/1']}>
      <Routes>
        <Route path="/samples/:id" element={<SampleDetail />} />
      </Routes>
    </MemoryRouter>,
  )
}

beforeEach(() => {
  window.localStorage.clear()
  window.localStorage.setItem('workbench.basis', JSON.stringify('mAh/g'))
})

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

// -- dashboard -------------------------------------------------------------

describe('Dashboard capacity column', () => {
  it('marks a row the server could not normalise, so raw mAh is not read as mAh/g', async () => {
    installFetch((url) => {
      if (path(url) === '/api/groups') return []
      if (path(url) === '/api/dashboard') {
        return {
          basis: 'mAh/g',
          basis_label: 'mAh g⁻¹',
          rows: [
            dashboardRow({ sample_id: 1, sample_name: 'A', basis: 'mAh/g', discharge_capacity: 207.7 }),
            dashboardRow({ sample_id: 2, sample_name: 'B', basis: 'mAh', discharge_capacity: 5.2515 }),
          ],
        }
      }
      return []
    })

    render(
      <MemoryRouter>
        <Dashboard />
      </MemoryRouter>,
    )

    const massless = (await screen.findByRole('link', { name: 'B' })).closest('tr')
    expect(massless).not.toBeNull()
    expect(within(massless!).getByTitle('질량·면적이 없어 원값으로 표시합니다')).toHaveTextContent(
      'mAh',
    )

    const normalised = screen.getByRole('link', { name: 'A' }).closest('tr')
    expect(
      within(normalised!).queryByTitle('질량·면적이 없어 원값으로 표시합니다'),
    ).toBeNull()
  })
})

// -- compare ---------------------------------------------------------------

describe('Compare mixed bases', () => {
  it('names the cells that fell back to raw mAh instead of claiming one basis', async () => {
    installFetch((url) => {
      if (path(url) === '/api/groups') return []
      if (path(url) === '/api/samples') {
        return [
          { ...sample({ id: 1, name: 'A' }) },
          { ...sample({ id: 2, name: 'B' }) },
        ]
      }
      if (path(url) === '/api/compare/cycles') {
        return {
          metric: 'discharge_capacity',
          metric_label: 'Discharge capacity',
          basis: 'mAh/g',
          requested_basis: 'mAh/g',
          mixed_basis: true,
          y_label: 'mAh g⁻¹',
          series: [
            {
              sample_id: 1, sample_name: 'A', group_id: null, cathode_type: '',
              c_rate: null, temperature_c: null, basis: 'mAh/g',
              points: [{ cycle: 3, value: 207.7 }],
            },
            {
              sample_id: 2, sample_name: 'B', group_id: null, cathode_type: '',
              c_rate: null, temperature_c: null, basis: 'mAh',
              basis_fallback_reason: 'active mass not set',
              points: [{ cycle: 3, value: 5.2515 }],
            },
          ],
        }
      }
      return []
    })

    render(
      <MemoryRouter>
        <Compare />
      </MemoryRouter>,
    )

    expect(
      await screen.findByText(/원값으로 그린 셀이 있습니다 — B \(mAh\)/),
    ).toBeInTheDocument()
    // and the page no longer promises that every cell is on the same basis
    expect(screen.queryByText(/같은 기준으로 정규화되어 비교됩니다/)).toBeNull()
  })

  it('stays quiet when every series came back on the requested basis', async () => {
    installFetch((url) => {
      if (path(url) === '/api/groups') return []
      if (path(url) === '/api/samples') return [sample({ id: 1, name: 'A' })]
      if (path(url) === '/api/compare/cycles') {
        return {
          metric: 'discharge_capacity',
          metric_label: 'Discharge capacity',
          basis: 'mAh/g',
          y_label: 'mAh g⁻¹',
          series: [
            {
              sample_id: 1, sample_name: 'A', group_id: null, cathode_type: '',
              c_rate: null, temperature_c: null, basis: 'mAh/g',
              points: [{ cycle: 3, value: 207.7 }],
            },
          ],
        }
      }
      return []
    })

    render(
      <MemoryRouter>
        <Compare />
      </MemoryRouter>,
    )

    expect(await screen.findByText(/같은 기준으로 정규화되어 비교됩니다/)).toBeInTheDocument()
    expect(screen.queryByText(/원값으로 그린 셀이 있습니다/)).toBeNull()
  })

  it('says so when "모두 선택" could not take every cell', async () => {
    const many = Array.from({ length: 35 }, (_, i) =>
      sample({ id: i + 1, name: `cell-${i + 1}` }),
    )
    installFetch((url) => {
      if (path(url) === '/api/groups') return []
      if (path(url) === '/api/samples') return many
      if (path(url) === '/api/compare/cycles') {
        return { metric: 'discharge_capacity', metric_label: '', basis: 'mAh/g', y_label: '', series: [] }
      }
      return []
    })

    render(
      <MemoryRouter>
        <Compare />
      </MemoryRouter>,
    )

    await userEvent.click(await screen.findByRole('button', { name: '모두 선택' }))
    expect(await screen.findByText(/앞 30개만 선택했습니다/)).toBeInTheDocument()
    expect(screen.getByText('셀 선택 · 30개')).toBeInTheDocument()
  })
})

// -- upload ----------------------------------------------------------------

describe('Upload orphan card', () => {
  it('shows the fetch failure instead of asserting that everything is attached', async () => {
    installFetch((url) => {
      if (path(url) === '/api/samples') return []
      if (path(url) === '/api/runs') return new Fail(500, 'database is locked')
      return []
    })

    render(
      <MemoryRouter>
        <Upload />
      </MemoryRouter>,
    )

    expect(await screen.findByText('database is locked')).toBeInTheDocument()
    expect(screen.queryByText('모두 연결되어 있습니다')).toBeNull()
  })

  it('reports a failed attach rather than leaving the cell name showing', async () => {
    installFetch((url, init) => {
      if (path(url) === '/api/samples') return [sample({ id: 9, name: 'cell-9' })]
      if (path(url) === '/api/runs' && !init) return [run({ id: 11, sample_id: null, sample_name: null })]
      if (path(url) === '/api/runs/11') return new Fail(404, 'sample 9 not found')
      return []
    })

    render(
      <MemoryRouter>
        <Upload />
      </MemoryRouter>,
    )

    await screen.findByText('No_1_dry_011.wrd')
    const attach = screen
      .getAllByRole('combobox')
      .find((node) => within(node).queryByRole('option', { name: '셀 선택…' })) as
      | HTMLSelectElement
      | undefined
    expect(attach).toBeDefined()
    await userEvent.selectOptions(attach!, '9')

    expect(await screen.findByText('sample 9 not found')).toBeInTheDocument()
    // still orphaned, so the select must not keep showing the cell name
    expect(attach!.value).toBe('')
  })
})

// -- sample detail ---------------------------------------------------------

function sampleDetailHandler(extra: Handler): Handler {
  return (url, init) => {
    const supplied = extra(url, init)
    if (supplied !== undefined) return supplied
    if (path(url) === '/api/meta') return META
    if (path(url) === '/api/samples/1') return sample()
    if (path(url) === '/api/samples/1/cycles') {
      return {
        basis: 'mAh',
        basis_label: 'mAh',
        requested_basis: 'mAh/g',
        basis_fallback_reason: null,
        reference_cycle: 3,
        resolved_cell: CELL,
        cycles: [cycle(1), cycle(2), cycle(3)],
      }
    }
    if (path(url) === '/api/samples/1/report') return new Fail(503, 'report unavailable')
    if (path(url) === '/api/runs') return [run()]
    return []
  }
}

describe('SampleDetail', () => {
  it('surfaces a failed profile fetch instead of leaving an empty chart', async () => {
    installFetch(
      sampleDetailHandler((url) =>
        path(url) === '/api/samples/1/profile'
          ? new Fail(500, 'could not read No_1_dry_011.wrd')
          : undefined,
      ),
    )

    renderSampleDetail()

    expect(await screen.findByText('could not read No_1_dry_011.wrd')).toBeInTheDocument()
  })

  it('commits the reference cycle once, on blur, not on every keystroke', async () => {
    const patched: unknown[] = []
    installFetch(
      sampleDetailHandler((url, init) => {
        if (path(url) === '/api/samples/1' && init?.method === 'PATCH') {
          patched.push(JSON.parse(String(init.body)))
          return sample({ reference_cycle: 25 })
        }
        return undefined
      }),
    )

    renderSampleDetail()

    const input = await screen.findByRole('spinbutton', { name: /기준 사이클/ })
    await userEvent.clear(input)
    await userEvent.type(input, '25')
    expect(patched).toHaveLength(0) // nothing committed while typing
    await userEvent.tab()

    await waitFor(() => expect(patched).toEqual([{ reference_cycle: 25 }]))
  })

  it('refetches the cycle table after a file is deleted', async () => {
    const cycleCalls: string[] = []
    installFetch(
      sampleDetailHandler((url, init) => {
        if (path(url) === '/api/samples/1/cycles') cycleCalls.push(url)
        if (path(url) === '/api/runs/11' && init?.method === 'DELETE') return {}
        return undefined
      }),
    )
    vi.spyOn(window, 'confirm').mockReturnValue(true)

    renderSampleDetail()

    await screen.findByText('No_1_dry_011.wrd')
    await waitFor(() => expect(cycleCalls.length).toBeGreaterThan(0))
    const before = cycleCalls.length

    await userEvent.click(screen.getByRole('button', { name: '삭제' }))

    await waitFor(() => expect(cycleCalls.length).toBeGreaterThan(before))
  })
})

// --- 삭제 --------------------------------------------------------------------
//
// 실수로 한 번 눌러 셀이 사라지면 안 되고, 지운 뒤에는 화면이 즉시 따라와야
// 한다. 원본 .wrd 는 남는다 (불변 규칙 2) — 화면이 그렇게 약속하므로 고정한다.

describe('대시보드 삭제', () => {
  function installDashboard(deleted: string[]) {
    installFetch((url, init) => {
      if (path(url) === '/api/groups') return []
      if (init?.method === 'DELETE') {
        deleted.push(path(url))
        return {}
      }
      if (path(url) === '/api/dashboard') {
        return {
          basis: 'mAh/g',
          basis_label: 'mAh g⁻¹',
          rows: deleted.length
            ? []
            : [dashboardRow({ sample_id: 7, sample_name: '안녕', basis: 'mAh/g' })],
        }
      }
      return []
    })
  }

  function renderDashboard() {
    render(
      <MemoryRouter>
        <Dashboard />
      </MemoryRouter>,
    )
  }

  it('한 번 눌러서는 지워지지 않는다', async () => {
    const deleted: string[] = []
    installDashboard(deleted)
    renderDashboard()

    await userEvent.click(await screen.findByRole('button', { name: '안녕 지우기' }))

    expect(screen.getByRole('button', { name: '지웁니다' })).toBeInTheDocument()
    expect(deleted).toEqual([])
  })

  it('취소하면 아무것도 지우지 않는다', async () => {
    const deleted: string[] = []
    installDashboard(deleted)
    renderDashboard()

    await userEvent.click(await screen.findByRole('button', { name: '안녕 지우기' }))
    await userEvent.click(screen.getByRole('button', { name: '취소' }))

    expect(screen.queryByRole('button', { name: '지웁니다' })).toBeNull()
    expect(deleted).toEqual([])
  })

  it('확인하면 지우고 목록을 다시 읽는다', async () => {
    const deleted: string[] = []
    installDashboard(deleted)
    renderDashboard()

    await userEvent.click(await screen.findByRole('button', { name: '안녕 지우기' }))
    await userEvent.click(screen.getByRole('button', { name: '지웁니다' }))

    await waitFor(() => expect(deleted).toHaveLength(1))
    expect(deleted[0]).toBe('/api/samples/7')
    // 지운 뒤 화면이 따라온다 — 지운 셀이 남아 있으면 안 된다.
    await waitFor(() => expect(screen.queryByRole('link', { name: '안녕' })).toBeNull())
  })
})
