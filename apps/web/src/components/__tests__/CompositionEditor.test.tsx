/** 프리셋 — 한 번 눌러서 칸 여럿을 채우는 물건.
 *
 * 여기서 틀리면 조용히 틀린다.  A 셀의 질량이 B 셀의 mAh/g 분모가 되거나,
 * 손으로 지정한 역할이 다시 추론되거나, 조성 없는 프리셋이 직접 입력한
 * 활물질 wt% 를 지우거나 — 셋 다 화면에는 아무 표시도 남기지 않는다.
 */

import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { CompositionEditor, describeSettings, presetSettingsOf } from '../CompositionEditor'
import type { CompositionPreset, PresetSettings, ResolvedCell, Sample } from '../../lib/types'

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
    total_mass_mg: 31.6,
    current_collector_mass_mg: null,
    active_wt_percent: null,
    active_mass_mg: null,
    area_cm2: null,
    diameter_mm: 13,
    thickness_um: null,
    nominal_specific_capacity_mah_g: 205.9,
    reference_electrode: 'Li-In',
    reference_offset_v: null,
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

function settings(overrides: Partial<PresetSettings> = {}): PresetSettings {
  return {
    area_cm2: null,
    diameter_mm: null,
    thickness_um: null,
    nominal_specific_capacity_mah_g: null,
    reference_electrode: null,
    reference_offset_v: null,
    ...overrides,
  }
}

function preset(overrides: Partial<CompositionPreset> = {}): CompositionPreset {
  return {
    id: 7,
    name: '건식 80',
    text: 'NCM811:LPSCl:VGCF = 80:17:3',
    label: '건식 80 · NCM811:LPSCl:VGCF = 80:17:3',
    composition: [
      { name: 'NCM811', wt_percent: 80, role: 'active' },
      { name: 'LPSCl', wt_percent: 17, role: 'electrolyte' },
      { name: 'VGCF', wt_percent: 3, role: 'conductive' },
    ],
    settings: settings({
      diameter_mm: 13,
      nominal_specific_capacity_mah_g: 205.9,
      reference_electrode: 'Li-In',
    }),
    created_at: '2026-08-01T00:00:00',
    updated_at: '2026-08-01T00:00:00',
    ...overrides,
  }
}

interface Call {
  url: string
  method: string
  body: Record<string, unknown>
}

let calls: Call[] = []

function installFetch(options: { presets?: CompositionPreset[]; presetStatus?: number } = {}) {
  const spy = vi.fn(async (url: string, init?: RequestInit) => {
    const method = init?.method ?? 'GET'
    const body = init?.body ? JSON.parse(String(init.body)) : {}
    calls.push({ url, method, body })
    if (url.startsWith('/api/composition-presets')) {
      if (method === 'GET') {
        return { ok: true, status: 200, json: async () => options.presets ?? [] }
      }
      const status = options.presetStatus ?? 201
      if (status >= 400) {
        return {
          ok: false,
          status,
          statusText: 'Conflict',
          json: async () => ({ detail: '"건식 80" 프리셋이 이미 있습니다' }),
        }
      }
      return { ok: true, status, json: async () => preset() }
    }
    // PATCH /api/samples/1
    return { ok: true, status: 200, json: async () => sample({ updated_at: '2026-08-02T00:00:00' }) }
  })
  vi.stubGlobal('fetch', spy)
  return spy
}

beforeEach(() => {
  calls = []
})

afterEach(() => {
  vi.unstubAllGlobals()
})

function patches(): Call[] {
  return calls.filter((call) => call.method === 'PATCH')
}

describe('프리셋 드롭박스', () => {
  it('이름과 조성 비율을 함께 보여 준다', async () => {
    installFetch({ presets: [preset()] })
    render(<CompositionEditor sample={sample()} onSaved={() => {}} />)

    await waitFor(() =>
      expect(
        screen.getByRole('option', { name: '건식 80 · NCM811:LPSCl:VGCF = 80:17:3' }),
      ).toBeInTheDocument(),
    )
  })

  it('저장된 것이 없으면 그렇게 말한다 — 박아 둔 목록은 없다', async () => {
    installFetch({ presets: [] })
    render(<CompositionEditor sample={sample()} onSaved={() => {}} />)

    await waitFor(() =>
      expect(screen.getByLabelText('프리셋 선택')).toBeDisabled(),
    )
    expect(screen.getByRole('option', { name: '저장된 프리셋이 없습니다' })).toBeInTheDocument()
  })

  it('고르면 조성과 셀 설정이 한 요청에 같이 간다', async () => {
    installFetch({ presets: [preset()] })
    render(<CompositionEditor sample={sample({ diameter_mm: null })} onSaved={() => {}} />)
    await waitFor(() => expect(screen.getByLabelText('프리셋 선택')).toBeEnabled())

    await userEvent.selectOptions(screen.getByLabelText('프리셋 선택'), '7')

    await waitFor(() => expect(patches()).toHaveLength(1))
    const body = patches()[0]!.body
    expect(body.diameter_mm).toBe(13)
    expect(body.nominal_specific_capacity_mah_g).toBe(205.9)
    expect(body.reference_electrode).toBe('Li-In')
    // 역할은 저장된 그대로 간다.  텍스트로 보내면 추론이 다시 돌아 손으로 고친
    // 역할이 덮인다 — 그 값이 mAh/g 분모를 정한다 (ADR 0007).
    expect(body.composition).toEqual(preset().composition)
    expect(body.clear).toEqual(['active_wt_percent'])
  })

  it('프리셋이 담지 않은 칸은 건드리지 않는다', async () => {
    const thin = preset({ settings: settings({ diameter_mm: 13 }) })
    installFetch({ presets: [thin] })
    render(<CompositionEditor sample={sample()} onSaved={() => {}} />)
    await waitFor(() => expect(screen.getByLabelText('프리셋 선택')).toBeEnabled())

    await userEvent.selectOptions(screen.getByLabelText('프리셋 선택'), '7')

    await waitFor(() => expect(patches()).toHaveLength(1))
    const body = patches()[0]!.body
    expect(body.diameter_mm).toBe(13)
    expect('thickness_um' in body).toBe(false)
    expect('reference_electrode' in body).toBe(false)
  })

  it('조성 없는 프리셋은 직접 입력한 활물질 wt% 를 지우지 않는다', async () => {
    const specOnly = preset({ composition: [], text: '', label: '13pi 셀',
                              settings: settings({ diameter_mm: 13 }) })
    installFetch({ presets: [specOnly] })
    render(<CompositionEditor sample={sample({ active_wt_percent: 80 })} onSaved={() => {}} />)
    await waitFor(() => expect(screen.getByLabelText('프리셋 선택')).toBeEnabled())

    await userEvent.selectOptions(screen.getByLabelText('프리셋 선택'), '7')

    await waitFor(() => expect(patches()).toHaveLength(1))
    // 지울 조성이 없으니 지울 이유도 없다.
    expect('clear' in patches()[0]!.body).toBe(false)
  })

  it('적용하고 나면 무엇이 채워졌는지 한 줄 남는다', async () => {
    installFetch({ presets: [preset()] })
    let current = sample()
    const { rerender } = render(
      <CompositionEditor sample={current} onSaved={(next) => { current = next }} />,
    )
    await waitFor(() => expect(screen.getByLabelText('프리셋 선택')).toBeEnabled())

    await userEvent.selectOptions(screen.getByLabelText('프리셋 선택'), '7')
    await waitFor(() => expect(patches()).toHaveLength(1))
    rerender(<CompositionEditor sample={current} onSaved={() => {}} />)

    expect(await screen.findByText(/프리셋이 채운 값/)).toHaveTextContent('전극 지름 13 mm')
    expect(screen.getByText(/프리셋이 채운 값/)).toHaveTextContent('기준전극 Li-In')
  })
})

describe('프리셋 저장', () => {
  it('버튼이 성분별로 편집을 열지 않는다 — 열림 상태를 토글하는 컨트롤이 아니다', async () => {
    installFetch({ presets: [] })
    const { container } = render(<CompositionEditor sample={sample()} onSaved={() => {}} />)

    await userEvent.click(screen.getByRole('button', { name: '프리셋 저장' }))

    expect(container.querySelector('details')?.open).toBeFalsy()
    expect(screen.getByRole('dialog', { name: '프리셋 저장' })).toBeInTheDocument()
  })

  it('무엇이 저장되는지 먼저 보여 준다', async () => {
    installFetch({ presets: [] })
    render(
      <CompositionEditor
        sample={sample({
          composition: [
            { name: 'NCM811', wt_percent: 80, role: 'active' },
            { name: 'LPSCl', wt_percent: 20, role: 'electrolyte' },
          ],
        })}
        onSaved={() => {}}
      />,
    )
    await userEvent.click(screen.getByRole('button', { name: '프리셋 저장' }))

    const dialog = screen.getByRole('dialog', { name: '프리셋 저장' })
    expect(dialog).toHaveTextContent('NCM811:LPSCl = 80:20')
    expect(dialog).toHaveTextContent('전극 지름 13 mm')
    expect(dialog).toHaveTextContent('공칭 비용량 205.9 mAh/g')
    expect(dialog).toHaveTextContent('기준전극 Li-In')
    expect(dialog).toHaveTextContent('질량은 셀마다 다르므로 담지 않습니다')
  })

  it('질량은 절대 담지 않는다', async () => {
    installFetch({ presets: [] })
    render(
      <CompositionEditor
        sample={sample({
          total_mass_mg: 31.6,
          active_mass_mg: 25.3,
          composition: [
            { name: 'AM', wt_percent: 80, role: 'active' },
            { name: 'SE', wt_percent: 20, role: 'electrolyte' },
          ],
        })}
        onSaved={() => {}}
      />,
    )
    await userEvent.click(screen.getByRole('button', { name: '프리셋 저장' }))
    await userEvent.type(screen.getByLabelText('프리셋 이름'), '건식 80')
    await userEvent.click(screen.getByRole('button', { name: '저장' }))

    await waitFor(() =>
      expect(calls.some((call) => call.method === 'POST')).toBe(true),
    )
    const saved = calls.find((call) => call.method === 'POST')!.body
    const carried = saved.settings as Record<string, unknown>
    expect('total_mass_mg' in carried).toBe(false)
    expect('active_mass_mg' in carried).toBe(false)
    expect(carried.diameter_mm).toBe(13)
  })

  it('담을 것이 없으면 저장할 수 없다', async () => {
    installFetch({ presets: [] })
    render(
      <CompositionEditor
        sample={sample({
          diameter_mm: null,
          nominal_specific_capacity_mah_g: null,
          reference_electrode: '',
        })}
        onSaved={() => {}}
      />,
    )
    await userEvent.click(screen.getByRole('button', { name: '프리셋 저장' }))
    await userEvent.type(screen.getByLabelText('프리셋 이름'), '빈 것')

    expect(screen.getByRole('button', { name: '저장' })).toBeDisabled()
    expect(screen.getByRole('dialog')).toHaveTextContent('담을 것이 없습니다')
  })

  it('이름이 겹치면 덮어쓰기를 눌러야 바뀐다', async () => {
    installFetch({ presets: [preset()], presetStatus: 409 })
    render(
      <CompositionEditor
        sample={sample({
          composition: [
            { name: 'AM', wt_percent: 80, role: 'active' },
            { name: 'SE', wt_percent: 20, role: 'electrolyte' },
          ],
        })}
        onSaved={() => {}}
      />,
    )
    await userEvent.click(screen.getByRole('button', { name: '프리셋 저장' }))
    await userEvent.type(screen.getByLabelText('프리셋 이름'), '건식 80')
    await userEvent.click(screen.getByRole('button', { name: '저장' }))

    const first = calls.find((call) => call.method === 'POST')!
    expect(first.body.overwrite).toBe(false)
    // 거절당했으니 아직 아무것도 안 바뀐 상태로, 사람에게 한 번 더 묻는다.
    const overwrite = await screen.findByRole('button', { name: '덮어쓰기' })

    await userEvent.click(overwrite)
    await waitFor(() =>
      expect(calls.filter((call) => call.method === 'POST')).toHaveLength(2),
    )
    expect(calls.filter((call) => call.method === 'POST')[1]!.body.overwrite).toBe(true)
  })

  it('목록에서 지울 수 있다 — 오타 하나가 영구히 남으면 안 된다', async () => {
    installFetch({ presets: [preset()] })
    render(<CompositionEditor sample={sample()} onSaved={() => {}} />)
    await waitFor(() => expect(screen.getByLabelText('프리셋 선택')).toBeEnabled())

    await userEvent.click(screen.getByRole('button', { name: '프리셋 저장' }))
    await userEvent.click(screen.getByRole('button', { name: '"건식 80" 삭제' }))

    await waitFor(() =>
      expect(
        calls.some(
          (call) => call.method === 'DELETE' && call.url === '/api/composition-presets/7',
        ),
      ).toBe(true),
    )
  })
})

describe('담기는 값의 계산', () => {
  it('질량은 절대 포함되지 않는다', () => {
    const carried = presetSettingsOf(sample({ total_mass_mg: 31.6, active_mass_mg: 25.3 }))
    expect(Object.keys(carried).sort()).toEqual([
      'area_cm2',
      'diameter_mm',
      'nominal_specific_capacity_mah_g',
      'reference_electrode',
      'reference_offset_v',
      'thickness_um',
    ])
  })

  it('비어 있는 칸은 문장에 나오지 않는다', () => {
    expect(describeSettings(settings({ diameter_mm: 13 }))).toEqual(['전극 지름 13 mm'])
    expect(describeSettings(settings())).toEqual([])
  })

  it('기준전극은 단위 없이 이름 그대로', () => {
    expect(describeSettings(settings({ reference_electrode: 'Li-In' }))).toEqual([
      '기준전극 Li-In',
    ])
  })
})
