/** Typed client for the workbench API.
 *
 * Errors are surfaced with the server's own message: the backend already
 * explains what went wrong ("active mass not set", "could not read ..."), and
 * rewording it here would only lose detail.
 */

import { noteOwnWrite } from './live'
import { actorHeader } from './who'
import type {
  Activity, ChangeNote, CircuitCombination,
  CircuitKind, CompareResponse, CompositionPreset, DqdvResponse,
  Diffusion, Drt, DrtSweep, DvdqResponse, CycleTable, DashboardRow, Facets,
  FeedbackKind, FeedbackNote,
  EisDashboard, GittDashboard, GittRun, Group, Measurements, Meta, Pocv,
  ProfileResponse, Report, Run, Sample, Scan, Spectrum, SpectrumDetail,
  SpectrumFit, SpectrumPoints,
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

/** 문이 닫혔을 때 (ADR 0014) — 암호를 묻는 한 장은 서버가 그린다.
 *
 *  여기서 한 번만 다룬다.  화면마다 401 을 따로 처리하게 두면 어딘가 하나는
 *  "불러오지 못했습니다" 로만 끝나고, 사용자는 암호를 물어보는 화면을 영영
 *  못 본 채 앱이 고장 났다고 읽는다.
 */
let asking = false

/** 401 일 때 할 일.  객체에 담아 두는 것은 테스트가 갈아끼우기 위해서다 —
 *  jsdom 의 `window.location` 은 바꿔 끼울 수 없다. */
export const unauthorized = {
  handle: (): void => window.location.reload(),
}

export function askForPassword(): void {
  // 한 화면이 요청 여럿을 동시에 보낸다.  전부 401 이라고 전부 다시 읽으면
  // 새로고침이 겹쳐서 암호 창이 뜨지도 않는다.
  if (asking) return
  asking = true
  try {
    unauthorized.handle()
  } catch {
    /* 브라우저가 아닌 곳에서는 할 일이 없다 */
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  // 이름은 모든 요청에 붙는다.  쓰기에만 붙이면 새 엔드포인트가 생겼을 때
  // 한 종류의 편집만 익명으로 기록되는데, 그건 아무 오류도 내지 않는다.
  const response = await fetch(path, {
    ...init,
    headers: { ...actorHeader(), ...(init?.headers ?? {}) },
  })
  if (response.status === 401) askForPassword()
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
  // A write echoes back on the change stream a moment later.  Remembering the
  // revision it produced lets this tab skip its own echo: the screen that made
  // the edit already has the answer in hand.
  noteOwnWrite(response)
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
  /** 데이터 판(revision)과 **떠 있는 코드**.  문 안에 있다 — `/api/health` 는
   *  문 밖이라 꼭 필요한 것만 담는다 (ADR 0014). */
  revision: () => request<{ revision: number; served_commit?: string }>('/api/revision'),
  meta: () => request<Meta>('/api/meta'),

  // -- 누가 무엇을 했는지 ----------------------------------------------------
  activity: (params?: Params) => request<Activity[]>(`/api/activity${query(params)}`),

  // -- 무엇이 바뀌었는지 (docs/log.md) ---------------------------------------
  changelog: (params?: Params) => request<ChangeNote[]>(`/api/changelog${query(params)}`),

  // -- 의견 게시판 (ADR 0033) -----------------------------------------------
  listFeedback: (params?: Params) =>
    request<FeedbackNote[]>(`/api/feedback${query(params)}`),
  createFeedback: (body: { kind: FeedbackKind; body: string }) =>
    request<FeedbackNote>('/api/feedback', json('POST', body)),
  updateFeedback: (id: number, body: {
    kind?: FeedbackKind; body?: string; resolved?: boolean
  }) => request<FeedbackNote>(`/api/feedback/${id}`, json('PATCH', body)),
  deleteFeedback: (id: number) =>
    request<void>(`/api/feedback/${id}`, { method: 'DELETE' }),
  replyToFeedback: (id: number, body: { body: string }) =>
    request<FeedbackNote>(`/api/feedback/${id}/replies`, json('POST', body)),
  deleteFeedbackReply: (noteId: number, replyId: number) =>
    request<void>(`/api/feedback/${noteId}/replies/${replyId}`, { method: 'DELETE' }),

  // -- groups --------------------------------------------------------------
  listGroups: () => request<Group[]>('/api/groups'),
  createGroup: (body: {
    name: string; description?: string; color?: string; parent_id?: number | null
  }) => request<Group>('/api/groups', json('POST', body)),
  updateGroup: (id: number, body: {
    name?: string; description?: string; color?: string; parent_id?: number | null
  }) => request<Group>(`/api/groups/${id}`, json('PATCH', body)),
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
  sampleDqdv: (id: number, params?: Params) =>
    request<DqdvResponse>(`/api/samples/${id}/dqdv${query(params)}`),
  sampleDvdq: (id: number, params?: Params) =>
    request<DvdqResponse>(`/api/samples/${id}/dvdq${query(params)}`),
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
  compareDqdv: (params: Params) =>
    request<DqdvResponse>(`/api/compare/dqdv${query(params)}`),
  compareDvdq: (params: Params) =>
    request<DvdqResponse>(`/api/compare/dvdq${query(params)}`),

  // -- 임피던스 (ADR 0019) -------------------------------------------------
  eisCircuits: () =>
    request<{ kinds: CircuitKind[]; combinations: CircuitCombination[] }>(
      '/api/eis/circuits',
    ),
  listSpectra: (params?: Params) =>
    request<Spectrum[]>(`/api/eis/spectra${query(params)}`),
  /** 스윕이 여럿인 원본만 — SOC 스캔 목록.  점은 안 실려 온다. */
  eisDashboard: () => request<EisDashboard>('/api/eis/dashboard'),
  listScans: (params?: Params) => request<Scan[]>(`/api/eis/scans${query(params)}`),
  /** 이 셀에 붙어 있는 충방전·임피던스·GITT 전부 (섹션끼리 서로를 찾는 길). */
  measurements: (sampleId: number) =>
    request<Measurements>(`/api/samples/${sampleId}/measurements`),
  getScan: (sha256: string) => request<Scan>(`/api/eis/scans/${sha256}`),
  //: 한 스캔의 **모든** 스윕의 점.  `spectraPoints` 의 열두 개 상한을
  //  안 쓴다 — 여기서 돌아오는 수는 사람이 고르는 것이 아니라 파일이
  //  정한다 (`/scans/{sha}/points` 의 주석).
  scanPoints: (sha256: string) =>
    request<SpectrumPoints[]>(`/api/eis/scans/${sha256}/points`),
  getSpectrum: (id: number) => request<SpectrumDetail>(`/api/eis/spectra/${id}`),
  spectrumPoints: (id: number) =>
    request<SpectrumPoints>(`/api/eis/spectra/${id}/points`),
  /** 여러 개를 한 번에 — 겹쳐 그리려면 동시에 있어야 축이 한 번만 잡힌다. */
  spectraPoints: (ids: number[]) =>
    request<SpectrumPoints[]>(`/api/eis/points${query({ ids: ids.join(',') })}`),
  /** 여러 개의 **가장 잘 맞은** 피팅 곡선.  안 맞춘 것은 목록에서 빠져
   *  돌아온다 — 빠진 id 가 곧 "아직 피팅 데이터가 없다" 이다. */
  spectraFits: (ids: number[]) =>
    request<SpectrumFit[]>(`/api/eis/fits${query({ ids: ids.join(',') })}`),
  uploadSpectrum: (file: File, params?: Params, settingsFile?: File | null) => {
    const form = new FormData()
    form.append('file', file)
    // `.mps` 는 곁들임이다 — 진폭도 장비 이름도 스펙트럼 안에는 없다.
    if (settingsFile) form.append('settings_file', settingsFile)
    return request<Spectrum>(`/api/eis/spectra/upload${query(params)}`, {
      method: 'POST',
      body: form,
    })
  },
  updateSpectrum: (id: number, body: Record<string, unknown>) =>
    request<Spectrum>(`/api/eis/spectra/${id}`, json('PATCH', body)),
  deleteSpectrum: (id: number) =>
    request<void>(`/api/eis/spectra/${id}`, { method: 'DELETE' }),
  fitSpectrum: (id: number, params?: Params) =>
    request<SpectrumFit>(`/api/eis/spectra/${id}/fit${query(params)}`,
      { method: 'POST' }),
  spectrumDrt: (id: number, params?: Params) =>
    request<Drt>(`/api/eis/spectra/${id}/drt${query(params)}`),
  spectrumDrtSweep: (id: number, params?: Params) =>
    request<DrtSweep>(`/api/eis/spectra/${id}/drt/sweep${query(params)}`),
  /** 한 SOC 스캔의 스윕 **전부**를 한 회로로.  상한은 스윕마다 따로 잡힌다
   *  (유도성 꼬리의 길이가 스윕마다 다르다) — 하한은 안 정한다. */
  fitScan: (sha256: string, params?: Params) =>
    request<{
      fitted: SpectrumFit[]
      failed: { spectrum_id: number; detail: string }[]
      requested: number
      converged: number
    }>(`/api/eis/scans/${sha256}/fit${query(params)}`, { method: 'POST' }),
  fitSpectra: (ids: number[], params?: Params) =>
    request<{
      fitted: SpectrumFit[]
      failed: { spectrum_id: number; detail: string }[]
      requested: number
      converged: number
    }>(`/api/eis/fit-batch${query(params)}`, json('POST', ids)),

  // -- GITT (ADR 0020) ------------------------------------------------------
  gittDashboard: () => request<GittDashboard>('/api/gitt/dashboard'),
  listGittRuns: (params?: Params) =>
    request<GittRun[]>(`/api/gitt/runs${query(params)}`),
  getGittRun: (id: number) => request<GittRun>(`/api/gitt/runs/${id}`),
  uploadGittRun: (file: File, params?: Params) => {
    const form = new FormData()
    form.append('file', file)
    return request<GittRun>(`/api/gitt/runs/upload${query(params)}`,
                            { method: 'POST', body: form })
  },
  updateGittRun: (id: number, body: Record<string, unknown>) =>
    request<GittRun>(`/api/gitt/runs/${id}`, json('PATCH', body)),
  deleteGittRun: (id: number) =>
    request<void>(`/api/gitt/runs/${id}`, { method: 'DELETE' }),
  gittPocv: (id: number) => request<Pocv>(`/api/gitt/runs/${id}/pocv`),
  gittDiffusion: (id: number) => request<Diffusion>(`/api/gitt/runs/${id}/diffusion`),

  // -- exports (URLs, so the browser downloads them directly) --------------
  /** The uploaded .wrd, byte for byte -- so the original can be fetched back
   *  from wherever the workbench is running, not only from the laptop that
   *  measured it. */
  exportOriginalUrl: (runId: number) => `/api/export/runs/${runId}/original.wrd`,
  exportRawUrl: (runId: number) => `/api/export/runs/${runId}/raw.csv`,
  /** 임피던스·GITT 원본.  중앙에 모아 두는 이유가 "각자 노트북에서 원본이
   *  사라지지 않게" 인데, 다시 못 받으면 올리는 것이 편도 여행이 된다. */
  spectrumOriginalUrl: (id: number) => `/api/export/spectra/${id}/original`,
  spectrumSettingsUrl: (id: number) => `/api/export/spectra/${id}/settings`,
  gittOriginalUrl: (id: number) => `/api/export/gitt/${id}/original`,
  exportCyclesUrl: (sampleId: number, params?: Params) =>
    `/api/export/samples/${sampleId}/cycles.csv${query(params)}`,
  exportProfilesUrl: (sampleId: number, params?: Params) =>
    `/api/export/samples/${sampleId}/profiles.csv${query(params)}`,
  exportDqdvUrl: (sampleId: number, params?: Params) =>
    `/api/export/samples/${sampleId}/dqdv.csv${query(params)}`,
  exportDvdqUrl: (sampleId: number, params?: Params) =>
    `/api/export/samples/${sampleId}/dvdq.csv${query(params)}`,
  exportWorkbookUrl: (sampleId: number, params?: Params) =>
    `/api/export/samples/${sampleId}/workbook.xlsx${query(params)}`,
}
