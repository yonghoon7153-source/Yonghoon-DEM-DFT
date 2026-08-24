/** Mirrors of the API response shapes.  Keep in sync with apps/api/app/schemas.py. */

export type Basis = 'mAh' | 'mAh/g' | 'mAh/cm2' | 'mAh/cm3' | '%'
export type CellState = 'running' | 'finished' | 'unknown'
export type DeclaredState = 'auto' | 'running' | 'finished'
export type Branch = 'charge' | 'discharge'

export type ComponentRole = 'active' | 'electrolyte' | 'conductive' | 'binder' | 'other'

export interface Component {
  name: string
  wt_percent: number
  role: ComponentRole
}

export interface ResolvedCell {
  active_mass_g: number | null
  active_wt_percent: number | null
  composition: Component[]
  composition_label: string
  composition_compact_label: string
  composition_problems: string[]
  area_cm2: number | null
  volume_cm3: number | null
  loading_mg_cm2: number | null
  nominal_capacity_mah: number | null
  nominal_specific_capacity_mah_g: number | null
  /** 계측기가 무엇을 기준으로 전압을 기록했는지 ('' = 환산 안 함). */
  reference_electrode?: string
  reference_offset_v?: number | null
  available_bases: Basis[]
  unavailable: Record<string, string>
  notes: Record<string, string>
}

/** 누가 무엇을 했는지 한 줄.
 *
 * `actor` 는 아무도 검증하지 않은 표시용 이름이다 (ADR 0012). 빈 문자열은
 * 이름을 대지 않은 사람이거나, 이 기능이 생기기 전에 저장된 것이다. */
export interface Activity {
  id: number
  at: string
  actor: string
  action: 'create' | 'update' | 'delete'
  entity: 'sample' | 'group' | 'preset' | 'run'
  entity_id: number | null
  /** 그때 이름.  지워진 뒤에도 읽히라고 남긴다 — 찾는 것이 정확히 그때다. */
  label: string
  fields: string[]
}

/** 패치노트 한 줄 — `docs/log.md` 의 한 항목.
 *
 * `action` 을 유니온으로 좁히지 않는다.  파일에 있는 그대로 오고, 서버가
 * 거르지 않는다 (거르면 그 항목만 조용히 사라진다).  화면은 아는 것만 색을
 * 주고 나머지는 중립으로 그린다. */
export interface ChangeNote {
  date: string
  action: string
  subject: string
  /** 커밋 메시지에 안 들어간 것.  없을 수도 있다. */
  body: string
}

export interface Group {
  id: number
  name: string
  description: string
  color: string
  created_at: string
  updated_at: string
  sample_count: number
  run_count: number
  created_by?: string
  updated_by?: string
}

export interface Sample {
  id: number
  name: string
  group_id: number | null
  group_name: string | null
  test_date: string | null
  cathode_type: string
  cathode_detail: string
  anode: string
  electrolyte: string
  process: string
  notes: string
  total_mass_mg: number | null
  current_collector_mass_mg: number | null
  active_wt_percent: number | null
  active_mass_mg: number | null
  area_cm2: number | null
  diameter_mm: number | null
  thickness_um: number | null
  nominal_specific_capacity_mah_g: number | null
  /** 계측기가 무엇을 기준으로 전압을 기록했는지 ('' = 환산 안 함). */
  reference_electrode?: string
  reference_offset_v?: number | null
  composition: Component[]
  composition_label: string
  temperature_c: number | null
  pressure_mpa: number | null
  cutoff_upper_v: number | null
  cutoff_lower_v: number | null
  c_rate: number | null
  c_rate_formation: number | null
  reference_cycle: number
  declared_state: DeclaredState
  created_at: string
  updated_at: string
  run_count: number
  cycle_count: number
  resolved_cell: ResolvedCell
  created_by?: string
  updated_by?: string
}

export interface ScheduleStep {
  index: number
  name: string
  control: string
  direction: 'charge' | 'discharge' | 'rest' | 'unknown'
  current_a: number | null
  voltage_limit_v: number | null
  taper_current_a: number | null
  loop_count: number
  loop_target: string | null
  sampling_interval_s: number | null
  cutoffs: { kind: string; condition: string; value: number; seconds: number; text: string }[]
  text: string
}

export interface Schedule {
  source_path?: string | null
  upper_cutoff_v?: number | null
  lower_cutoff_v?: number | null
  planned_cycles?: number | null
  c_rate?: number | null
  cycling_current_a?: number | null
  formation_current_a?: number | null
  nominal_capacity_mah?: number | null
  sampling_interval_s?: number | null
  steps?: ScheduleStep[]
}

export interface Run {
  id: number
  sample_id: number | null
  sample_name: string | null
  original_name: string
  sha256: string
  size_bytes: number
  uploaded_at: string
  /** 누가 올렸는지 ('' = 이름을 대지 않았거나 이 기능 이전). */
  created_by?: string
  device_model: string
  serial_no: string
  channel: number | null
  app_version: string
  firmware_version: string
  start_time: string | null
  end_time: string | null
  row_count: number
  cycle_count: number
  complete_cycle_count: number
  unit_coulomb: boolean
  data_format: number
  instrument_path: string
  schedule_path: string
  cycle_offset: number
  cycle_offset_source: 'auto' | 'manual'
  parse_error: string
  schedule: Schedule
}

export interface Cycle {
  cycle: number
  cycle_index: number
  run_id: number
  charge_capacity: number | null
  discharge_capacity: number | null
  charge_capacity_mah: number | null
  discharge_capacity_mah: number | null
  coulombic_efficiency: number | null
  energy_efficiency: number | null
  charge_energy_mwh: number | null
  discharge_energy_mwh: number | null
  mean_charge_voltage: number | null
  mean_discharge_voltage: number | null
  voltage_hysteresis: number | null
  voltage_max: number | null
  voltage_min: number | null
  retention_pct: number | null
  /** 직전 **완료** 사이클 대비 단차. 표에 보이는 열과 같은 단위다. 유지율과는
   *  다른 질문이다 — 저쪽 분모는 기준 사이클, 이쪽은 직전 사이클. */
  discharge_delta?: number | null
  charge_delta?: number | null
  discharge_delta_pct?: number | null
  /** 무엇과 비교했는가, 그리고 몇 사이클 전인가. 1 이 아니면 그 단차는 여러
   *  사이클치 열화를 한 칸에 담고 있다. */
  delta_base_cycle?: number | null
  delta_span?: number
  discharge_delta_per_cycle?: number | null
  c_rate: number | null
  temperature_mean: number | null
  duration_h: number
  n_points: number
  complete: boolean
}

export interface CycleTable {
  basis: Basis
  basis_label: string
  requested_basis: Basis
  basis_fallback_reason: string | null
  reference_cycle: number | null
  /** 실제로 기준으로 쓴 사이클. 요청값과 다를 수 있다 (ADR 0004). */
  reference_cycle_used?: number | null
  reference_available?: boolean
  retention_note?: string
  resolved_cell: ResolvedCell
  cycles: Cycle[]
}

export interface ProfileSeries {
  cycle: number
  branch: Branch
  basis: Basis
  points: number
  capacity: number[]
  voltage: number[]
  run_id: number
  label: string
  /** Why this one curve is not in the requested unit, when it is not. */
  basis_fallback_reason?: string | null
}

export interface ProfileResponse {
  basis: Basis
  basis_label: string
  requested_basis: Basis
  resolved_cell: ResolvedCell
  series: ProfileSeries[]
  /** True when the curves are not all in the same unit. */
  mixed_basis?: boolean
}

/** 한 브랜치의 dQ/dV, 그리고 무엇으로 만들었는지.
 *
 * `voltage_step` 과 `smoothing` 이 곡선을 바꾼다 — 평활은 봉우리를 낮추고
 * 넓히므로, 봉우리 *높이*는 같은 설정으로 만든 곡선끼리만 비교된다 (ADR 0013).
 *
 * 만들지 못한 곡선도 온다. `points` 가 0 이고 `reason` 이 붙어 있다. */
export interface DqdvSeries {
  cycle: number
  branch: Branch
  basis: Basis
  points: number
  voltage: number[]
  /** mAh/V (정규화하면 (mAh/g)/V 등). 방전은 음수 — 전압이 내려가면서 용량이
   *  오르므로 그것이 답이다. */
  dqdv: number[]
  run_id: number
  label: string
  voltage_step: number
  smoothing: number
  /** 어떤 필터로, (savgol 이면) 몇 차로 평활했는가. 봉우리 *높이* 는 창·필터·
   *  차수가 모두 같은 곡선끼리만 비교된다 (ADR 0015). */
  smoother?: Smoother
  poly_order?: number
  /** 단조 필터가 뺀 표본 수 — CV 구간과 잡음성 되돌아감. */
  points_dropped: number
  reason: string
}

export interface DqdvResponse {
  basis: Basis
  basis_label: string
  requested_basis: Basis
  resolved_cell: ResolvedCell
  series: DqdvSeries[]
  voltage_step: number
  smoothing: number
  smoother?: Smoother
  poly_order?: number
  mixed_basis?: boolean
}

/** 평활 방법. `savgol` 을 차수 1 로 쓰면 내부에서 이동평균과 값이 같다 —
 *  랩 공용 스크립트가 그 설정이다 (ADR 0015). 봉우리를 살리려면 2 이상. */
export type Smoother = 'moving' | 'savgol'

export interface DvdqSeries {
  cycle: number
  branch: Branch
  basis: Basis
  points: number
  /** x 축. dQ/dV 와 반대로 여기서는 용량이 가로다. */
  capacity: number[]
  /** V/mAh (정규화하면 V/(mAh/g) 등). 방전은 음수 — dQ/dV 와 같은 이유다. */
  dvdq: number[]
  run_id: number
  label: string
  /** 격자 간격, x 축과 같은 단위로. 두 봉우리가 실제로 분해된 것인지 판단하는
   *  데 필요하다. */
  capacity_step: number
  smoothing: number
  smoother?: Smoother
  poly_order?: number
  /** 용량이 멈춘 구간에서 뺀 표본 수 — CV 홀드와 휴지. */
  points_dropped: number
  reason: string
}

export interface DvdqResponse {
  basis: Basis
  basis_label: string
  requested_basis: Basis
  resolved_cell: ResolvedCell
  series: DvdqSeries[]
  smoothing: number
  smoother?: Smoother
  poly_order?: number
  /** 호출자가 고정한 격자(mAh). null 이면 가지마다 자기 폭의 1/400 을 썼다. */
  capacity_step: number | null
  mixed_basis?: boolean
}

export type KneeStatus = 'detected' | 'insufficient' | 'none' | 'indeterminate'

export interface KneeResult {
  method: 'threshold' | 'segmented' | 'slope_ratio' | 'curvature' | 'none'
  cycle: number | null
  detected: boolean
  reason: string
  detail: Record<string, number>
  /** `insufficient` 는 "knee 없음" 이 아니다 — 아직 확인할 데이터가 없는 것이다. */
  status: KneeStatus
  /** 확정 여부와 무관하게 이 기준이 짚고 있는 사이클. */
  candidate_cycle: number | null
}

export interface KneeAnalysis {
  primary: KneeResult
  results: KneeResult[]
  reference_cycle: number
  reference_capacity_mah: number | null
  search_start_cycle: number
  n_points: number
  fade_rate_early_pct_per_cycle: number | null
  fade_rate_late_pct_per_cycle: number | null
  projected_cycle_at_80pct: number | null
  /** 기준 사이클이 요청과 다를 때 그 사유. */
  reference_note?: string
}

export interface CycleReadout {
  cycle: number
  discharge_capacity: number | null
  charge_capacity: number | null
  discharge_capacity_mah: number
  charge_capacity_mah: number
  coulombic_efficiency: number | null
  energy_efficiency: number | null
  mean_discharge_voltage: number | null
  complete: boolean
}

export interface Report {
  sample_id: number
  sample_name: string
  state: CellState
  state_confidence: 'high' | 'medium' | 'low'
  state_summary: string
  evidence: { signal: string; detail: string; points_to: string }[]
  cycles_observed: number
  cycles_complete: number
  planned_cycles: number | null
  in_progress_cycle: number | null
  reference_cycle_requested: number
  reference_available: boolean
  retention_pct: number | null
  retention_note: string
  basis: Basis
  basis_label: string
  reported: CycleReadout | null
  reference: CycleReadout | null
  first_cycle: CycleReadout | null
  knee: KneeAnalysis | null
  resolved_cell: ResolvedCell
}

export interface DashboardRow {
  sample_id: number
  sample_name: string
  group_id: number | null
  group_name?: string
  group_color?: string
  cathode_type: string
  c_rate: number | null
  temperature_c: number | null
  test_date: string | null
  state: CellState
  state_confidence: string
  in_progress_cycle: number | null
  cycles_complete: number
  reported_cycle: number | null
  discharge_capacity: number | null
  discharge_capacity_mah: number | null
  retention_pct: number | null
  reference_cycle: number | null
  reference_available: boolean
  initial_coulombic_efficiency: number | null
  knee_cycle: number | null
  knee_method: string | null
  /** 확정 knee 가 아니어도 무엇인지 구분된다 — `null` 하나로 접지 않는다. */
  knee_status?: KneeStatus | null
  knee_candidate_cycle?: number | null
  knee_reason?: string
  basis: Basis
  loading_mg_cm2: number | null
  composition_label: string
  /** 이 셀을 만든 사람 ('' = 이름을 대지 않았거나 이 기능 이전). */
  owner?: string
  /** Retention against the reference cycle, thinned for a sparkline. */
  trend: number[]
  /** 각 점이 실제로 속한 사이클 번호. 균등 간격을 가정하면 안 된다. */
  trend_cycles?: number[]
  trend_first_cycle: number | null
  trend_last_cycle: number | null
  knee_trend_index: number | null
}

export interface CompareSeries {
  sample_id: number
  sample_name: string
  group_id: number | null
  cathode_type: string
  c_rate: number | null
  temperature_c: number | null
  /** The basis this series is actually in — empty for non-capacity metrics. */
  basis: string
  /** Set when this cell could not be normalised and fell back to raw mAh. */
  basis_fallback_reason?: string | null
  /** 이 곡선의 유지율이 실제로 어느 사이클 대비인지. 셀마다 다를 수 있다. */
  reference_cycle_used?: number | null
  reference_available?: boolean
  retention_note?: string
  points: { cycle: number; value: number }[]
}

export interface CompareResponse {
  metric: string
  metric_label: string
  basis: Basis
  requested_basis?: Basis
  /** True when the series are not all in the same unit. */
  mixed_basis?: boolean
  y_label: string
  series: CompareSeries[]
}

/** Cell settings a preset carries.  `null` = this preset does not carry it,
 *  so applying leaves that field alone rather than clearing it.
 *
 *  No masses, deliberately: those are measured per cell (ADR 0010). */
export interface PresetSettings {
  area_cm2: number | null
  diameter_mm: number | null
  thickness_um: number | null
  nominal_specific_capacity_mah_g: number | null
  reference_electrode: string | null
  reference_offset_v: number | null
}

export interface CompositionPreset {
  id: number
  name: string
  created_by?: string
  updated_by?: string
  /** `AM:SE:VGCF = 80:17:3` */
  text: string
  /** What the dropdown shows: `이름 · AM:SE:VGCF = 80:17:3` */
  label: string
  composition: Component[]
  settings: PresetSettings
  created_at: string
  updated_at: string
}

export interface Meta {
  bases: { value: Basis; label: string }[]
  states: string[]
  knee_methods: { value: string; label: string }[]
  default_plot_points: number
  component_roles: { value: ComponentRole; label: string }[]
}

export interface Facets {
  cathode_type: string[]
  cathode_detail: string[]
  process: string[]
  electrolyte: string[]
  anode: string[]
  c_rate: number[]
  temperature_c: number[]
  test_date: string[]
  bases: Basis[]
}
