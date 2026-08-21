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
import { cellNameFor, Upload } from '../../pages/Upload'
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
      if (path(url) === '/api/runs' && (init?.method ?? 'GET') === 'GET') {
        return [run({ id: 11, sample_id: null, sample_name: null })]
      }
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
  it('초기화 는 그래프와 입력란을 함께 비운다', async () => {
    // `useAsync` 는 새 응답이 올 때까지 이전 것을 들고 있다 — 키를 칠 때마다
    // 화면이 깜빡이지 않게 하려는 것인데, 요청이 꺼졌을 때도 옛 곡선이 그대로
    // 남는다.  그래서 초기화를 눌러 선택을 비워도 그래프는 여덟 사이클을
    // 계속 보여 주고 있었다.
    const drawn: string[] = []
    installFetch(
      sampleDetailHandler((url) => {
        if (path(url) !== '/api/samples/1/profile') return undefined
        drawn.push(new URL(url, 'http://x').searchParams.get('cycles') ?? '')
        return {
          basis: 'mAh',
          basis_label: 'mAh',
          requested_basis: 'mAh',
          resolved_cell: CELL,
          // 범례는 곡선이 둘 이상일 때만 그려진다.
          series: [
            {
              cycle: 1,
              branch: 'charge',
              basis: 'mAh',
              points: 2,
              capacity: [0, 1],
              voltage: [3.0, 4.2],
              run_id: 11,
              label: '1번 충전',
            },
            {
              cycle: 1,
              branch: 'discharge',
              basis: 'mAh',
              points: 2,
              capacity: [0, 1],
              voltage: [4.2, 3.0],
              run_id: 11,
              label: '1번 방전',
            },
          ],
        }
      }),
    )
    renderSampleDetail()

    expect(await screen.findByText('1번 방전')).toBeInTheDocument()
    const input = await screen.findByLabelText('사이클 선택')
    expect(input).not.toHaveValue('')

    const buttons = await screen.findAllByRole('button', { name: '초기화' })
    await userEvent.click(buttons[0]!)

    await waitFor(() => expect(screen.queryByText('1번 방전')).not.toBeInTheDocument())
    expect(input).toHaveValue('')
    // 빈 그래프는 고장처럼 보인다 — 왜 비었는지 화면이 말해야 한다.
    expect(screen.getByText('고른 사이클이 없습니다')).toBeInTheDocument()
  })

  it('충전과 방전을 둘 다 끄면 그 이유를 말한다', async () => {
    installFetch(sampleDetailHandler(() => undefined))
    renderSampleDetail()

    await userEvent.click(await screen.findByRole('button', { name: '충전' }))
    await userEvent.click(screen.getByRole('button', { name: '방전' }))
    expect(await screen.findByText('충전도 방전도 꺼져 있습니다')).toBeInTheDocument()
  })

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

// --- 업로드에서 그룹 고르기 ---------------------------------------------------
//
// 같은 실험 묶음을 열 개 올리고 나서 셀 화면에 열 번 다시 들어가 그룹을 붙이는
// 것은 실제로 아무도 안 한다. 올릴 때 정하게 한다.

describe('업로드 그룹', () => {
  function installUpload(created: unknown[]) {
    installFetch((url, init) => {
      if (path(url) === '/api/groups')
        return [
          { id: 3, name: '고Ni', description: '', color: '', sample_count: 1, run_count: 0,
            created_at: '2026-08-20T00:00:00', updated_at: '2026-08-20T00:00:00' },
          { id: 4, name: '중Ni', description: '', color: '', sample_count: 1, run_count: 0,
            created_at: '2026-08-20T00:00:00', updated_at: '2026-08-20T00:00:00' },
        ]
      if (path(url) === '/api/samples' && init?.method === 'POST') {
        created.push(JSON.parse(String(init.body)))
        return sample({ id: 99 })
      }
      if (path(url).startsWith('/api/runs/upload')) {
        return {
          id: 501, sample_id: 99, original_name: 'a.wrd', sha256: 'a'.repeat(64),
          size_bytes: 3, row_count: 10, cycle_count: 1, complete_cycle_count: 1,
          cycle_offset: 0, cycle_offset_source: 'auto', device_model: 'X',
          serial_no: 'S', channel: 1, app_version: '', firmware_version: '',
          start_time: '2026-08-20T00:00:00', end_time: '2026-08-20T01:00:00',
          data_format: 0, unit_coulomb: false, instrument_path: '',
          schedule_path: '', schedule: null, parse_error: '',
          parsed_at: '2026-08-20T01:00:00', created_at: '2026-08-20T01:00:00',
        }
      }
      if (path(url) === '/api/samples')
        return [sample({ id: 1, name: '고Ni-01', group_id: 3 }),
                sample({ id: 2, name: '중Ni-01', group_id: 4 })]
      if (path(url) === '/api/runs') return []
      return []
    })
  }

  function renderUpload() {
    render(
      <MemoryRouter>
        <Upload />
      </MemoryRouter>,
    )
  }

  it('그룹을 고르면 기존 셀 목록이 그 그룹으로 좁혀진다', async () => {
    installUpload([])
    renderUpload()

    const attach = await screen.findByRole('combobox', { name: /기존 셀에 연결/ })
    await waitFor(() => expect(within(attach).getAllByRole('option').length).toBe(3))

    await userEvent.selectOptions(
      screen.getByRole('combobox', { name: /그룹/ }),
      '3',
    )
    await waitFor(() =>
      expect(within(attach).getAllByRole('option').map((o) => o.textContent)).toEqual([
        '연결 안 함 (나중에 지정)',
        '고Ni-01',
      ]),
    )
  })

  it('고른 그룹으로 새 셀이 만들어진다', async () => {
    const created: unknown[] = []
    installUpload(created)
    renderUpload()

    await userEvent.selectOptions(
      await screen.findByRole('combobox', { name: '그룹' }),
      '4',
    )
    await userEvent.type(screen.getByPlaceholderText('No_1_dry_0.0316g'), '중Ni-02')

    const file = new File([new Uint8Array([1, 2, 3])], 'a.wrd')
    const picker = document.querySelector('input[type="file"]') as HTMLInputElement
    await userEvent.upload(picker, file)

    await waitFor(() => expect(created).toHaveLength(1))
    expect(created[0]).toMatchObject({ name: '중Ni-02', group_id: 4 })
  })

  it('파일 이름 체크박스: 파일마다 셀 하나가 생긴다', async () => {
    const created: unknown[] = []
    installUpload(created)
    renderUpload()

    await userEvent.click(
      await screen.findByRole('checkbox', { name: /파일 이름을 셀 이름으로/ }),
    )
    await userEvent.selectOptions(screen.getByRole('combobox', { name: '그룹' }), '4')

    const picker = document.querySelector('input[type="file"]') as HTMLInputElement
    await userEvent.upload(picker, [
      new File([new Uint8Array([1])], '3.6V_1_16.4mg.wrd'),
      new File([new Uint8Array([2])], '3.8V_1_18.5mg.wrd'),
    ])

    await waitFor(() => expect(created).toHaveLength(2))
    expect(created).toEqual([
      { name: '3.6V_1_16.4mg', group_id: 4 },
      { name: '3.8V_1_18.5mg', group_id: 4 },
    ])
  })

  it('분할 파일은 한 셀로 모인다', async () => {
    const created: unknown[] = []
    installUpload(created)
    renderUpload()

    await userEvent.click(
      await screen.findByRole('checkbox', { name: /파일 이름을 셀 이름으로/ }),
    )
    const picker = document.querySelector('input[type="file"]') as HTMLInputElement
    await userEvent.upload(picker, [
      new File([new Uint8Array([1])], 'No_1_dry_60oC_011.wrd'),
      new File([new Uint8Array([2])], 'No_1_dry_60oC_012.wrd'),
    ])

    // 두 조각은 한 실험이다 — 셀이 두 개 생기면 사이클이 갈라진다.
    await waitFor(() => expect(created).toHaveLength(1))
    expect(created[0]).toMatchObject({ name: 'No_1_dry_60oC' })
  })

  it('이름을 쳐서 좁힐 수 있다', async () => {
    installUpload([])
    renderUpload()

    const attach = await screen.findByRole('combobox', { name: /기존 셀에 연결/ })
    await userEvent.type(screen.getByPlaceholderText('이름 일부…'), '중Ni')

    await waitFor(() =>
      expect(within(attach).getAllByRole('option').map((o) => o.textContent)).toEqual([
        '연결 안 함 (나중에 지정)',
        '중Ni-01',
      ]),
    )
  })
})

// --- 파일 이름을 셀 이름으로 -------------------------------------------------

describe('파일 이름 → 셀 이름', () => {
  it('.wrd 를 떼고, 분할 번호도 뗀다', () => {
    expect(cellNameFor('3.6V_1_16.4mg.wrd')).toBe('3.6V_1_16.4mg')
    expect(cellNameFor('4.0V_post_formation_18.9mg.WRD')).toBe('4.0V_post_formation_18.9mg')
    // 긴 실험의 조각들은 한 셀이다 — 떼지 않으면 실험이 둘로 갈라진다.
    expect(cellNameFor('No_1_dry_0.0316g_0.2C_60oC_011.wrd')).toBe('No_1_dry_0.0316g_0.2C_60oC')
    expect(cellNameFor('No_1_dry_0.0316g_0.2C_60oC_012.wrd')).toBe('No_1_dry_0.0316g_0.2C_60oC')
  })

  it('질량처럼 숫자로 끝나도 잘라내지 않는다', () => {
    // "_1" 은 두 자리 미만이라 분할 번호가 아니다.
    expect(cellNameFor('3.6V_1.wrd')).toBe('3.6V_1')
    expect(cellNameFor('cell_16.4mg.wrd')).toBe('cell_16.4mg')
  })

  it('이름이 통째로 사라지지 않는다', () => {
    expect(cellNameFor('_011.wrd')).toBe('_011')
  })
})

// --- 이름에 적힌 질량 ---------------------------------------------------------

describe('셀 상세 질량 힌트', () => {
  it('이름이 질량을 들고 있으면 입력란 옆에 회색으로 적는다', async () => {
    installFetch(
      sampleDetailHandler((url) =>
        path(url) === '/api/samples/1'
          ? sample({ name: 'CAM_LPSCl_4.6V_1_17.5mg' })
          : undefined,
      ),
    )
    renderSampleDetail()

    // 이름이 말하는 값은 참고일 뿐 — 입력란은 그대로 비어 있어야 한다.
    // 추정값을 실측값처럼 채워 넣으면 mAh/g 가 조용히 지어진다.
    const field = (await screen.findByText(/전극 총 질량/)).closest('label') as HTMLElement
    expect(within(field).getByText('#17.5mg')).toBeInTheDocument()
    expect(within(field).getByRole('spinbutton')).toHaveValue(null)
  })

  it('이름에 질량이 없으면 아무것도 적지 않는다', async () => {
    installFetch(sampleDetailHandler(() => undefined))
    renderSampleDetail()

    const field = (await screen.findByText(/전극 총 질량/)).closest('label') as HTMLElement
    expect(within(field).queryByText(/^#/)).toBeNull()
  })
})

// --- dQ/dV ---------------------------------------------------------------------

describe('dQ/dV 모드', () => {
  function dqdvBody(overrides: Record<string, unknown> = {}) {
    return {
      basis: 'mAh',
      basis_label: 'mAh',
      requested_basis: 'mAh',
      resolved_cell: CELL,
      voltage_step: 0.005,
      smoothing: 5,
      series: [
        {
          cycle: 3, branch: 'discharge', basis: 'mAh', points: 3,
          voltage: [3.0, 3.005, 3.01], dqdv: [-1, -2, -1],
          run_id: 11, label: '3번 방전',
          voltage_step: 0.005, smoothing: 5, points_dropped: 0, reason: '',
        },
      ],
      ...overrides,
    }
  }

  it('켜기 전에는 dQ/dV 를 받아 오지 않는다', async () => {
    // 20 MB 파일에서 400 사이클의 미분을, 아무도 보지 않는 동안 계산할 이유가
    // 없다.
    const asked: string[] = []
    installFetch((url) => {
      asked.push(path(url))
      return sampleDetailHandler(() => undefined)(url)
    })
    renderSampleDetail()

    await screen.findByRole('button', { name: 'dQ/dV' })
    expect(asked).not.toContain('/api/samples/1/dqdv')
  })

  it('켜면 dQ/dV 를 받아 와서 그린다', async () => {
    // 축 이름은 uPlot 이 캔버스에 그리므로 jsdom 에서 볼 수 없다.  대신 모드가
    // 정말 바뀌었는지를 두 가지로 본다: 다른 엔드포인트를 물었는가, 그리고
    // dQ/dV 에서만 나오는 설정 줄이 떴는가.
    const asked: string[] = []
    installFetch((url) => {
      asked.push(path(url))
      return sampleDetailHandler((inner) =>
        path(inner) === '/api/samples/1/dqdv' ? dqdvBody() : undefined,
      )(url)
    })
    renderSampleDetail()

    await userEvent.click(await screen.findByRole('button', { name: 'dQ/dV' }))

    await waitFor(() => expect(asked).toContain('/api/samples/1/dqdv'))
    expect(await screen.findByText(/전압 격자 5 mV/)).toBeInTheDocument()
  })

  it('돌아오면 프로파일이다 — 두 모드가 같이 켜져 있지 않다', async () => {
    installFetch(
      sampleDetailHandler((url) =>
        path(url) === '/api/samples/1/dqdv' ? dqdvBody() : undefined,
      ),
    )
    renderSampleDetail()

    await userEvent.click(await screen.findByRole('button', { name: 'dQ/dV' }))
    expect(await screen.findByText(/전압 격자 5 mV/)).toBeInTheDocument()

    await userEvent.click(screen.getByRole('button', { name: '프로파일' }))
    await waitFor(() =>
      expect(screen.queryByText(/전압 격자 5 mV/)).not.toBeInTheDocument(),
    )
  })

  it('무엇으로 만든 곡선인지 말한다 — 평활은 봉우리를 낮춘다', async () => {
    installFetch(
      sampleDetailHandler((url) =>
        path(url) === '/api/samples/1/dqdv'
          ? dqdvBody({ voltage_step: 0.01, smoothing: 9 })
          : undefined,
      ),
    )
    renderSampleDetail()

    await userEvent.click(await screen.findByRole('button', { name: 'dQ/dV' }))
    expect(await screen.findByText(/전압 격자 10 mV · 평활 9점/)).toBeInTheDocument()
  })

  it('만들지 못한 곡선이 있으면 왜인지 말한다', async () => {
    installFetch(
      sampleDetailHandler((url) =>
        path(url) === '/api/samples/1/dqdv'
          ? dqdvBody({
              series: [
                {
                  cycle: 3, branch: 'charge', basis: 'mAh', points: 0,
                  voltage: [], dqdv: [], run_id: 11, label: '3번 충전',
                  voltage_step: 0.005, smoothing: 5, points_dropped: 40,
                  reason: 'only 1 samples move in voltage',
                },
              ],
            })
          : undefined,
      ),
    )
    renderSampleDetail()

    await userEvent.click(await screen.findByRole('button', { name: 'dQ/dV' }))
    // 그냥 빈 그래프면 고장으로 읽힌다.
    expect(await screen.findByText(/1개 곡선을 만들지 못했습니다/)).toBeInTheDocument()
  })

  it('dQ/dV 복사는 모드를 켜야 눌린다', async () => {
    installFetch(
      sampleDetailHandler((url) =>
        path(url) === '/api/samples/1/dqdv' ? dqdvBody() : undefined,
      ),
    )
    renderSampleDetail()

    // 꺼져 있을 때 눌러도 복사할 곡선이 없다 — 빈 것을 복사해 놓고 성공했다고
    // 하면 사람은 Origin 에서 알게 된다.
    expect(await screen.findByRole('button', { name: 'dQ/dV 복사' })).toBeDisabled()

    await userEvent.click(screen.getByRole('button', { name: 'dQ/dV' }))
    await waitFor(() =>
      expect(screen.getByRole('button', { name: 'dQ/dV 복사' })).toBeEnabled(),
    )
  })
})

// --- Origin 붙여넣기 -----------------------------------------------------------

describe('클립보드 복사', () => {
  function installClipboard() {
    const written: string[] = []
    Object.defineProperty(navigator, 'clipboard', {
      configurable: true,
      value: { writeText: (text: string) => (written.push(text), Promise.resolve()) },
    })
    Object.defineProperty(window, 'isSecureContext', { configurable: true, value: true })
    return written
  }

  it('사이클 표를 화면에 보이는 단위로 복사한다', async () => {
    const written = installClipboard()
    installFetch(sampleDetailHandler(() => undefined))
    renderSampleDetail()

    await userEvent.click(await screen.findByRole('button', { name: '사이클 복사' }))

    // 이름도 단위도 없이 숫자만 — 붙여 넣은 헤더는 Origin 에서 도로 잘라내야
    // 하는 두 줄이다.  이 픽스처의 용량은 5.25 mAh (활물질 질량이 없어 mAh 로
    // 떨어진다).
    expect(written[0]!.split('\n')).toEqual(['1\t5.25', '2\t5.25', '3\t5.25'])
    // 확인 표시는 눈에만 보이면 안 된다 — 접근성 이름도 같이 바뀐다.
    expect(await screen.findByRole('button', { name: '사이클 복사됨' })).toBeInTheDocument()
  })

  it('쿨롱효율은 따로 나온다 — 버튼 하나에 열 두 개', async () => {
    const written = installClipboard()
    installFetch(sampleDetailHandler(() => undefined))
    renderSampleDetail()

    await userEvent.click(await screen.findByRole('button', { name: '쿨롱효율 복사' }))
    expect(written[0]!.split('\n')[0]).toBe('1\t97.2')
  })

  it('복사할 것이 없으면 조용히 성공한 척하지 않는다', async () => {
    installClipboard()
    installFetch(
      sampleDetailHandler((url) =>
        path(url) === '/api/samples/1/cycles'
          ? {
              basis: 'mAh',
              basis_label: 'mAh',
              requested_basis: 'mAh',
              basis_fallback_reason: null,
              reference_cycle: 3,
              resolved_cell: CELL,
              cycles: [],
            }
          : undefined,
      ),
    )
    renderSampleDetail()

    await userEvent.click(await screen.findByRole('button', { name: '사이클 복사' }))
    expect(await screen.findByText('복사할 사이클 데이터가 없습니다')).toBeInTheDocument()
  })
})
