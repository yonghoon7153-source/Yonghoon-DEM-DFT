/** Typed client for the workbench API.
 *
 * Errors are surfaced with the server's own message: the backend already
 * explains what went wrong ("active mass not set", "could not read ..."), and
 * rewording it here would only lose detail.
 */

import type {
  CompareResponse, CompositionPreset, CycleTable, DashboardRow, Facets, Group, Meta,
  ProfileResponse, Report, Run, Sample,
} from './types'

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

type Params = Record<string, string | number | boolean | null | undefined>

function query(params?: Params): string {
  if (!params) return ''
  const search = new URLSearchParams()
  for (const [key, value] of Object.entries(params)) {
    if (value !== null && value !== undefined && value !== '') {
      search.set(key, String(value))
    }
  }
  const text = search.toString()
  return text ? `?${text}` : ''
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, init)
  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`
    try {
      const body = await response.json()
      if (body?.detail) {
        detail = typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail)
      }
    } catch {
      /* the body was not JSON; keep the status line */
    }
    throw new ApiError(detail, response.status)
  }
  if (response.status === 204) return undefined as T
  return (await response.json()) as T
}

function json(method: string, body: unknown): RequestInit {
  return {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  }
}

export const api = {
  health: () => request<{ status: string; wrdkit: string }>('/api/health'),
  meta: () => request<Meta>('/api/meta'),

  // -- groups --------------------------------------------------------------
  listGroups: () => request<Group[]>('/api/groups'),
  createGroup: (body: { name: string; description?: string; color?: string }) =>
    request<Group>('/api/groups', json('POST', body)),
  updateGroup: (id: number, body: { name: string; description?: string; color?: string }) =>
    request<Group>(`/api/groups/${id}`, json('PATCH', body)),
  deleteGroup: (id: number) => request<void>(`/api/groups/${id}`, { method: 'DELETE' }),

  // -- composition presets --------------------------------------------------
  listPresets: () => request<CompositionPreset[]>('/api/composition-presets'),
  savePreset: (body: {
    name: string
    composition?: unknown[]
    settings?: Record<string, unknown>
    overwrite?: boolean
  }) => request<CompositionPreset>('/api/composition-presets', json('POST', body)),
  deletePreset: (id: number) =>
    request<void>(`/api/composition-presets/${id}`, { method: 'DELETE' }),

  // -- samples -------------------------------------------------------------
  listSamples: (params?: Params) => request<Sample[]>(`/api/samples${query(params)}`),
  facets: () => request<Facets>('/api/samples/facets'),
  getSample: (id: number) => request<Sample>(`/api/samples/${id}`),
  createSample: (body: Record<string, unknown>) =>
    request<Sample>('/api/samples', json('POST', body)),
  updateSample: (id: number, body: Record<string, unknown>) =>
    request<Sample>(`/api/samples/${id}`, json('PATCH', body)),
  deleteSample: (id: number, deleteRuns = false) =>
    request<void>(`/api/samples/${id}${query({ delete_runs: deleteRuns })}`, {
      method: 'DELETE',
    }),

  // -- runs ----------------------------------------------------------------
  listRuns: (params?: Params) => request<Run[]>(`/api/runs${query(params)}`),
  getRun: (id: number) => request<Run>(`/api/runs/${id}`),
  uploadRun: (file: File, sampleId?: number | null) => {
    const form = new FormData()
    form.append('file', file)
    return request<Run>(`/api/runs/upload${query({ sample_id: sampleId })}`, {
      method: 'POST',
      body: form,
    })
  },
  updateRun: (id: number, body: Record<string, unknown>) =>
    request<Run>(`/api/runs/${id}`, json('PATCH', body)),
  reparseRun: (id: number) => request<Run>(`/api/runs/${id}/reparse`, { method: 'POST' }),
  deleteRun: (id: number) => request<void>(`/api/runs/${id}`, { method: 'DELETE' }),

  // -- analysis ------------------------------------------------------------
  sampleCycles: (id: number, params?: Params) =>
    request<CycleTable>(`/api/samples/${id}/cycles${query(params)}`),
  runCycles: (id: number, params?: Params) =>
    request<CycleTable>(`/api/runs/${id}/cycles${query(params)}`),
  sampleProfile: (id: number, params?: Params) =>
    request<ProfileResponse>(`/api/samples/${id}/profile${query(params)}`),
  sampleReport: (id: number, params?: Params) =>
    request<Report>(`/api/samples/${id}/report${query(params)}`),
  dashboard: (params?: Params) =>
    request<{ basis: string; basis_label: string; rows: DashboardRow[] }>(
      `/api/dashboard${query(params)}`,
    ),
  compareCycles: (params: Params) =>
    request<CompareResponse>(`/api/compare/cycles${query(params)}`),
  compareProfiles: (params: Params) =>
    request<ProfileResponse>(`/api/compare/profiles${query(params)}`),

  // -- exports (URLs, so the browser downloads them directly) --------------
  exportRawUrl: (runId: number) => `/api/export/runs/${runId}/raw.csv`,
  exportCyclesUrl: (sampleId: number, params?: Params) =>
    `/api/export/samples/${sampleId}/cycles.csv${query(params)}`,
  exportProfilesUrl: (sampleId: number, params?: Params) =>
    `/api/export/samples/${sampleId}/profiles.csv${query(params)}`,
  exportWorkbookUrl: (sampleId: number, params?: Params) =>
    `/api/export/samples/${sampleId}/workbook.xlsx${query(params)}`,
}
