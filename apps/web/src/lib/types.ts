/** Mirrors of the API response shapes.  Keep in sync with apps/api/app/schemas.py. */

export type Basis = 'mAh' | 'mAh/g' | 'mAh/cm2' | 'mAh/cm3' | '%'
export type CellState = 'running' | 'finished' | 'unknown'
export type DeclaredState = 'auto' | 'running' | 'finished'
/** 기준 사이클을 누가 정했나 (ADR 0018).  `formationless` 는 스케줄에
 *  formation 이 없어 1번에 앵커했다는 뜻이다. */
export type ReferenceReason = 'user' | 'formationless' | 'default'
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
  /** 이 그룹을 담고 있는 그룹.  `null` 이면 최상위다 (ADR 0025). */
  parent_id?: number | null
  /** 상위 그룹 이름.  최상위면 빈 문자열. */
  parent_name?: string
  /** 이 그룹이 담은 소그룹 수. */
  subgroup_count?: number
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
  /** 그 그룹이 소그룹이면 그 위 그룹의 이름.  최상위면 빈 문자열. */
  group_parent_name?: string
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
  /** 실제로 쓰이는 기준 사이클과 그 이유 (ADR 0018).  formation 이 없는
   *  스케줄은 1번에 앵커하므로 `reference_cycle` 과 다를 수 있다 — 입력란은
   *  저장값을, 문구는 쓰이는 값을 보여 준다. */
  reference_cycle_effective?: number
  reference_cycle_reason?: ReferenceReason
  /** 스케줄이 말하는 formation 유무. */
  formation?: 'yes' | 'no' | 'unclear'
  declared_state: DeclaredState
  created_at: string
  updated_at: string
  run_count: number
  cycle_count: number
  /** 이 셀에 붙은 임피던스 스펙트럼 수와, 가장 잘 맞은 피팅의 전체 저항.
   *  비어 있는 것도 뜻이다: 0 이면 아직 안 쟀고, 0 이 아닌데 저항이 없으면
   *  잰 것이 아직 안 맞았다. */
  spectrum_count?: number
  impedance_ohm?: number | null
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
  /** 같은 계측을 더 길게 담은 파일의 id — 이 파일은 그것에 포함된다.
   *  목록에는 남지만 셀의 사이클 표에서는 빠진다 (ADR 0032). */
  superseded_by?: number | null
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
  /** 그 기준을 누가 정했나 (ADR 0018). */
  reference_cycle_reason?: ReferenceReason
  /** 실제로 기준으로 쓴 사이클. 요청값과 다를 수 있다 (ADR 0004). */
  reference_cycle_used?: number | null
  reference_available?: boolean
  retention_note?: string
  resolved_cell: ResolvedCell
  cycles: Cycle[]
  /** 표에서 빠진 사이클들 — 숫자가 없어서 뺀 것이지, 없는 사이클이 아니다. */
  partial_cycles?: PartialCycle[]
}

/** 기록에는 있는데 사이클 지표가 없는 사이클.
 *
 * 행을 빼는 것은 옳다 (잘린 사이클의 부분값은 측정값이 아니다).  행과 함께
 * **있다는 사실까지** 빼는 바람에, 화면이 온통 — 인 이유를 아무도 알 수 없었다.
 */
export interface PartialCycle {
  cycle: number
  run_id: number
  /** truncated | no_discharge | no_charge | no_steps | '' (이유 미상) */
  reason: string
  has_charge: boolean
  has_discharge: boolean
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
  /** 사이클 지표가 없는 사이클의 곡선인가.  곡선 자체는 실측이다. */
  complete?: boolean
  incomplete_reason?: string
}

export interface ProfileResponse {
  basis: Basis
  basis_label: string
  requested_basis: Basis
  resolved_cell: ResolvedCell
  series: ProfileSeries[]
  /** 실제로 그린 사이클 번호들 — `cycles=all` 은 골라 뽑을 수 있다. */
  cycles?: number[]
  /** 전부를 못 그렸으면 무엇을 어떻게 골랐는지 한 줄.  비면 고른 것이 전부다. */
  cycles_note?: string
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
  /** 실제로 그린 사이클 번호들 — `cycles=all` 은 골라 뽑을 수 있다. */
  cycles?: number[]
  /** 전부를 못 그렸으면 무엇을 어떻게 골랐는지 한 줄.  비면 고른 것이 전부다. */
  cycles_note?: string
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
  /** 실제로 그린 사이클 번호들 — `cycles=all` 은 골라 뽑을 수 있다. */
  cycles?: number[]
  /** 전부를 못 그렸으면 무엇을 어떻게 골랐는지 한 줄.  비면 고른 것이 전부다. */
  cycles_note?: string
  smoothing: number
  smoother?: Smoother
  poly_order?: number
  /** 호출자가 고정한 격자(mAh). null 이면 가지마다 자기 폭의 1/400 을 썼다. */
  capacity_step: number | null
  mixed_basis?: boolean
}

export type KneeStatus = 'detected' | 'insufficient' | 'none' | 'indeterminate'

export interface KneeResult {
  method: 'threshold' | 'segmented' | 'slope_ratio' | 'curvature' | 'dbw' | 'none'
  cycle: number | null
  detected: boolean
  reason: string
  detail: Record<string, number>
  /** `insufficient` 는 "knee 없음" 이 아니다 — 아직 확인할 데이터가 없는 것이다. */
  status: KneeStatus
  /** 확정 여부와 무관하게 이 기준이 짚고 있는 사이클. */
  candidate_cycle: number | null
  /** 완만한 이탈이 시작되는 knee-onset (ADR 0021). dbw 만 채운다; `cycle` 은 knee-point. */
  onset_cycle?: number | null
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
  /** 게이트의 문턱값.  "1.3배였는데 1.5배가 필요합니다" 를 쓰려면 필요한 쪽
   *  숫자도 있어야 하는데, 여기에 베껴 두면 서버가 문턱을 바꾼 날 화면만 옛
   *  숫자를 말하게 된다 — 그래서 서버가 준다. */
  thresholds?: Record<string, number>
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
  reference_cycle_reason?: ReferenceReason
  reference_available: boolean
  retention_pct: number | null
  retention_note: string
  /** 완료된 사이클이 하나도 없을 때, 왜 없는지.  있으면 빈 문자열. */
  no_complete_reason?: string
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
  /** 이 셀의 파일 중 가장 최근에 올린 것의 시각 — 표의 기본 정렬.
   *  아직 파일이 없는 셀은 `null` 이고 맨 아래로 간다. */
  uploaded_at: string | null
  group_id: number | null
  group_name?: string
  /** 그 그룹이 소그룹이면 그 위 그룹의 이름.  최상위면 빈 문자열. */
  group_parent_name?: string
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
  /** 이탈이 시작되는 곳 — dbw 가 두 전환을 분해했을 때만 (ADR 0021). */
  knee_onset_cycle?: number | null
  knee_onset_trend_index?: number | null
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


// -- 임피던스 (ADR 0019) ----------------------------------------------------

/** 같은 두 반원이 무엇으로 불릴지를 정하는 것. */
export type EisKind = 'liquid' | 'solid'
/** 무엇을 쟀나.  전해질이 무엇이냐와는 다른 질문이고, 아크의 뜻을 바꾼다 —
 *  전고체 대칭셀의 두 아크는 벌크와 입계지만 풀셀의 두 아크는 아니다. */
export type CellConfig = 'sym' | 'full' | 'half'

export interface Spectrum {
  /** 무엇을 보려고 잰 측정인가 (자유 입력). */
  purpose?: string
  /** 한 파일 안에서 몇 번째 스윕인지와 전부 몇 개인지 (ADR 0022). */
  sweep_index?: number
  sweep_count?: number
  /** 그 스윕의 셀 상태 — SOC 스캔의 x축. */
  potential_v?: number | null
  capacity_mah?: number | null
  /** 이번 업로드가 같은 바이트의 기존 항목을 돌려준 것인가 (서버 dedup). */
  duplicate?: boolean
  id: number
  sample_id: number | null
  sample_name: string | null
  name: string
  kind: EisKind
  /** 빈 문자열은 "아직 안 정함" 이다. */
  cell_config: CellConfig | ''
  original_name: string
  sha256: string
  size_bytes: number
  source_format: string
  /** 함께 올라온 .mps 의 원래 이름.  빈 문자열이면 안 올라왔다. */
  settings_name?: string
  uploaded_at: string
  n_points: number
  frequency_start_hz: number | null
  frequency_end_hz: number | null
  amplitude_mv: number | null
  device: string
  technique: string
  /** 몇 번째 사이클의 임피던스인가. null 은 "안 적음", 0 은 "구동 전". */
  at_cycle: number | null
  measured_at: string | null
  thickness_um: number | null
  area_cm2: number | null
  /** 원형 펠릿의 지름 (mm).  면적이 비어 있으면 면적이 여기서 나온다. */
  diameter_mm?: number | null
  /** 실제로 쓰이는 면적 (자기 값 → 지름에서 → 셀의 것).  `null` 이면 모른다 —
   *  비교 화면은 그때 Ω·cm² 로 안 바꾸고 뺀 이름을 적는다. */
  area_cm2_effective?: number | null
  /** 이 측정 자신의 조건 (ADR 0027).  셀에 안 붙어 있어도 쓸 수 있다. */
  group_id?: number | null
  test_date?: string
  cathode_type?: string
  process?: string
  temperature_c?: number | null
  /** 실제로 쓰이는 값 — 자기 것이 비어 있으면 붙은 셀의 것. */
  group_id_effective?: number | null
  group_label?: string
  /** 폴더 트리가 쓰는 두 조각 (ADR 0035) — `group_label` 을 갈라 쓰면
   *  이름에 `·` 가 든 그룹에서 조용히 틀린다. */
  group_name_effective?: string
  group_parent_name_effective?: string
  test_date_effective?: string
  cathode_type_effective?: string
  process_effective?: string
  temperature_c_effective?: number | null
  /** 위 값 중 셀에서 빌려 온 칸들.  화면이 "이건 셀에서 온 값" 이라고 적는다. */
  inherited?: string[]
  last_circuit: string
  parse_error: string
  created_by?: string
  updated_by?: string
  updated_at: string
  fit_count: number
  best_chi_squared: number | null
  best_circuit: string
}

/** EIS 대시보드 한 줄 — 임피던스를 가진 셀 하나. */
export interface EisDashboardRow {
  sample_id: number | null
  sample_name: string
  /** 이 줄의 원래 이름 — 붙은 줄은 가장 최근 스펙트럼의, 안 붙은 줄은 그 파일
   *  자신의 것.  파일 이름에 조건이 적혀 있는 일이 많다. */
  name: string
  /** 그 이름이 가리키는 스펙트럼 — 눌러서 가고, 안 붙은 줄은 여기서 지운다. */
  spectrum_id: number | null
  /** 셀에 붙어 있는가.  안 붙은 것도 줄로 나온다. */
  attached: boolean
  /** 그룹·소그룹으로 거르려면 id 가, "부모 · 자식" 으로 적으려면 이름 둘이
   *  필요하다 (ADR 0025). */
  group_id: number | null
  group_name: string
  group_parent_name: string
  owner: string
  /** 한 셀에 액체와 전고체가 섞여 있으면 빈 문자열이다 — 둘은 아크 이름부터 다르다. */
  kind: EisKind | ''
  cell_config: CellConfig | ''
  spectra: number
  /** 스윕이 여럿인 **파일**의 수.  스윕 21개는 스캔 1개다. */
  scans: number
  fitted: number
  purposes: string[]
  last_circuit: string
  last_at_cycle: number | null
  /** 맞춘 적이 없으면 `null`.  0 과는 다른 말이다. */
  series_resistance_ohm: number | null
  total_resistance_ohm: number | null
  measured_at: string | null
  /** 이 줄에 딸린 것 중 가장 늦게 올라온 때 — 표의 기본 정렬 (내림차순).
   *  잰 때와 다르다: 지난달에 잰 파일을 오늘 올릴 수 있다. */
  uploaded_at: string | null
}

export interface EisDashboard {
  rows: EisDashboardRow[]
  /** 셀에 안 붙은 스펙트럼의 수.  붙이는 것은 일이고, 남아 있다는 사실은
   *  여기서만 보인다. */
  unattached: number
}

/** GITT 대시보드 한 줄 — GITT 를 가진 셀 하나. */
export interface GittDashboardRow {
  sample_id: number | null
  sample_name: string
  /** EIS 대시보드와 같은 셋 — 안 붙은 기록도 이름으로 한 줄 나온다. */
  name: string
  gitt_id: number | null
  attached: boolean
  group_id: number | null
  group_name: string
  group_parent_name: string
  owner: string
  /** 이 셀의 GITT 기록들에 적힌 목적들 (자유 입력). */
  purposes: string[]
  records: number
  pulses: number
  /** D 를 낼 수 있는 기록의 수 — 재료 상수가 다 있는 것. */
  ready: number
  /** 아직 없는 재료 상수의 이름들.  이 셀에서 다음에 할 일이 곧 이것이다. */
  missing: string[]
  /** 낼 수 있는 D 의 최소·최대 (cm²/s).  평균이 아닌 이유는 D 가 SOC 를 따라
   *  자릿수로 움직여서 한 숫자가 아무 SOC 도 뜻하지 않기 때문이다. */
  diffusion_low: number | null
  diffusion_high: number | null
  measured_at: string | null
  /** `EisDashboardRow.uploaded_at` 과 같은 뜻 — 표의 기본 정렬. */
  uploaded_at: string | null
}

export interface GittDashboard {
  rows: GittDashboardRow[]
  unattached: number
}

/** 한 셀에 붙어 있는 측정 하나 — 세 종류를 한 모양으로. */
export interface Measurement {
  kind: 'cycling' | 'eis' | 'gitt'
  id: number
  name: string
  /** 그 종류에서만 뜻이 있는 한 줄 (사이클 수 · 주파수 범위 · 펄스 수). */
  detail: string
  measured_at: string | null
}

export interface Measurements {
  sample_id: number
  sample_name: string
  cycling: Measurement[]
  eis: Measurement[]
  gitt: Measurement[]
}

/** 한 스윕과, 그 스윕에서 가장 잘 맞은 피팅의 값들 (ADR 0022). */
export interface ScanPoint {
  spectrum_id: number
  sweep_index: number
  name: string
  capacity_mah: number | null
  potential_v: number | null
  fit_id: number | null
  circuit: string
  chi_squared: number | null
  /** 파라미터 이름 → 값.  **미결정 파라미터는 여기 없다** — 서버가 뺀다 (§0.4). */
  values: Record<string, number>
  labels: Record<string, string>
}

/** 파일 하나에서 나온 스윕들 — SOC 스캔 하나. */
export interface Scan {
  sha256: string
  name: string
  original_name: string
  kind: EisKind
  cell_config: CellConfig | ''
  purpose: string
  sample_id: number | null
  sample_name: string | null
  sweeps: number
  fitted: number
  parameters: string[]
  /** 목록에서는 비어 있다.  한 스캔을 열었을 때만 채워진다. */
  points: ScanPoint[]
}

export interface FitParameter {
  name: string
  value: number
  unit: string
  stderr: number | null
  /** 오차가 값의 절반을 넘으면 false — 그 숫자는 측정된 것이 아니다. */
  determined: boolean
  relative_error?: number | null
}

export interface FitArc {
  parameter: string
  label: string
  note: string
  value_ohm: number
  determined: boolean
}

export interface SpectrumFit {
  /** 서버가 같은 회로 AST 로 계산한 맞춤 곡선.  화면은 회로를 다시 해석하지 않는다 (#6). */
  fitted_frequency_hz?: number[] | null
  fitted_z_re?: number[] | null
  fitted_z_im?: number[] | null
  fitted_note?: string
  id: number
  spectrum_id: number
  circuit: string
  /** 피팅 당시의 종류. `kind_now` 와 다르면 이름이 달라졌다는 뜻이다. */
  kind: EisKind
  kind_now: EisKind
  converged: boolean
  chi_squared: number | null
  reason: string
  parameters: FitParameter[]
  arcs: FitArc[]
  conductivity: {
    bulk_s_cm?: number | null
    grain_boundary_s_cm?: number | null
    total_s_cm?: number | null
    total_ohm?: number
    missing?: string[]
    /** σ 합계에서 뺀 아크들 (세 번째부터 — 전극 계면일 수 있어서). */
    excluded?: string[]
  }
  dropped_inductive: number
  dropped_out_of_range: number
  /** 오차가 저주파 끝에 몰렸을 때 하한에 적을 값. null 이면 안 몰렸다는 뜻. */
  suggested_low_hz?: number | null
  suggested_low_drops?: number
  /** 유도성 점을 뺀 뒤의 최고 주파수 — 상한에 적을 값. */
  suggested_high_hz?: number | null
  frequency_low_hz: number | null
  frequency_high_hz: number | null
  starts: number
  starts_converged: number
  created_at: string
  created_by?: string
}

export interface SpectrumDetail extends Spectrum {
  settings: Record<string, unknown>
  thickness_cm: number | null
  area_cm2_effective: number | null
  fits: SpectrumFit[]
}

export interface SpectrumPoints {
  id: number
  name: string
  kind: EisKind
  at_cycle: number | null
  frequency_hz: number[]
  /** z_im 은 허수부 자체다. 나이퀴스트 세로축은 그 음수. */
  z_re: number[]
  z_im: number[]
  magnitude: number[]
  phase_deg: number[]
}

export interface CircuitPreset {
  circuit: string
  label: string
  note: string
}

export interface CircuitKind {
  kind: EisKind
  label: string
  presets: CircuitPreset[]
}

/** 액체/전고체 × 풀셀·하프셀·대칭셀 여섯 조합.  아크의 이름과 기본 회로가
 *  같은 축에서 갈리므로, 화면에서도 한 번에 고른다. */
export interface CircuitCombination {
  kind: EisKind
  cell_config: string
  label: string
  presets: CircuitPreset[]
}


export interface DrtPeak {
  tau_s: number
  frequency_hz: number
  gamma_ohm: number
  /** 봉우리 아래 넓이 — 그 과정이 감당하는 저항. */
  resistance_ohm: number
  tau_low_s: number
  tau_high_s: number
}

export interface Drt {
  spectrum_id: number
  /** 이 답을 만든 벌점 가중치. 결과의 일부다 — λ 가 답을 정한다. */
  regularisation: number
  derivative_order: number
  tau_s: number[]
  gamma_ohm: number[]
  r_inf_ohm: number
  inductance_h: number | null
  chi_squared: number
  residual_norm: number
  penalty_norm: number
  peaks: DrtPeak[]
  total_polarisation_ohm: number
  dropped_inductive: number
}

export interface DrtSweep {
  spectrum_id: number
  results: Drt[]
  /** L 곡선 모서리가 가리키는 자리. 없으면 -1 이고 이유가 붙는다. */
  suggested_index: number
  suggested_reason: string
}


// -- GITT (ADR 0020) --------------------------------------------------------

export interface GittRun {
  /** 어느 셀의 것인가.  `null` 은 아직 안 붙였다는 뜻이고 정상 상태다. */
  sample_id?: number | null
  sample_name?: string | null
  id: number
  name: string
  original_name: string
  sha256: string
  size_bytes: number
  uploaded_at: string
  n_points: number
  n_pulses: number
  duration_h: number | null
  start_time: string | null
  molar_volume_cm3: number | null
  molar_mass_g: number | null
  active_mass_g: number | null
  /** 저울이 읽는 전극 전체와 그 안의 활물질 비율. 활물질 질량을 안 적었으면
   *  이 둘의 곱이 쓰인다 — 적어 넣은 값이 늘 이긴다. */
  electrode_mass_g?: number | null
  active_wt_percent?: number | null
  area_cm2: number | null
  /** 캘리퍼가 읽는 지름. 면적을 안 적었으면 여기서 나온다. */
  diameter_mm?: number | null
  /** 실제로 계산에 들어가는 두 값 (적은 것 → 계산한 것 순). */
  active_mass_g_effective?: number | null
  area_cm2_effective?: number | null
  /** 이보다 짧은 휴지는 평형으로 치지 않는다. 0 이면 전부 쓴다. */
  min_rest_s: number
  /** 무엇을 보려고 잰 기록인가 (자유 입력).  비어 있는 것이 정상이다. */
  purpose?: string
  /** 이 측정 자신의 조건 (ADR 0027).  셀에 안 붙어 있어도 쓸 수 있다. */
  group_id?: number | null
  test_date?: string
  cathode_type?: string
  process?: string
  temperature_c?: number | null
  /** 실제로 쓰이는 값 — 자기 것이 비어 있으면 붙은 셀의 것. */
  group_id_effective?: number | null
  group_label?: string
  /** 폴더 트리가 쓰는 두 조각 (ADR 0035) — `group_label` 을 갈라 쓰면
   *  이름에 `·` 가 든 그룹에서 조용히 틀린다. */
  group_name_effective?: string
  group_parent_name_effective?: string
  test_date_effective?: string
  cathode_type_effective?: string
  process_effective?: string
  temperature_c_effective?: number | null
  /** 위 값 중 셀에서 빌려 온 칸들.  화면이 "이건 셀에서 온 값" 이라고 적는다. */
  inherited?: string[]
  parse_error: string
  /** 펄스와 휴지 길이에 대한 관찰 한 줄. 판정이 아니다. */
  pulse_note: string
  created_by?: string
  updated_by?: string
  updated_at: string
  /** 확산계수를 내려면 아직 무엇이 필요한가. 비어 있으면 낼 수 있다. */
  missing_for_diffusion: string[]
}

export interface PocvPoint {
  capacity_mah: number
  voltage_v: number
  rest_s: number
  /** 휴지 마지막 1/10 구간의 전압 변화. 0 에 가까울수록 평형이다. */
  drift_mv: number
}

/** pOCV 곡선 밑에 깔리는 실제 측정 전압.  같은 x 축이다. */
export interface RawTrace {
  capacity_mah: number[]
  voltage_v: number[]
}

export interface Pocv {
  gitt_id: number
  charge: PocvPoint[]
  discharge: PocvPoint[]
  /** 위 두 곡선의 원본 — 점선으로 겹쳐 그린다.  각 점에 **어떻게** 도달했는지
   *  (펄스의 분극과 그 뒤의 완화) 가 보인다. */
  charge_raw?: RawTrace
  discharge_raw?: RawTrace
  skipped_charge: number
  skipped_discharge: number
  skipped_reasons: string[]
}

export interface DiffusionPoint {
  capacity_mah: number
  voltage_v: number
  d_cm2_s: number | null
  delta_es_v: number
  delta_et_v: number
  pulse_s: number
  /** √t 직선성 — Weppner-Huggins 의 가정이 곧 이것이다. */
  sqrt_t_r_squared: number
  reason: string
  /** ΔE_s 가 기대는 휴지의 길이(s)와 그 끝의 잔여 드리프트(mV) — D 의 증거다. */
  rest_s?: number | null
  drift_mv?: number | null
}

export interface Diffusion {
  gitt_id: number
  points: DiffusionPoint[]
  missing: string[]
  molar_volume_cm3: number | null
  molar_mass_g: number | null
  mass_g: number | null
  area_cm2: number | null
  usable: number
  total: number
}


// -- 의견 게시판 (ADR 0033) --------------------------------------------------

/** `issue` 불편한 점 · `question` 궁금한 것 · `idea` 이러면 좋겠다.
 *  셋으로 나누는 이유는 답이 다르기 때문이다: 불편은 고치고, 질문은 답하고,
 *  아이디어는 정한다. */
export type FeedbackKind = 'issue' | 'question' | 'idea'

export interface FeedbackReply {
  id: number
  note_id: number
  created_at: string
  created_by: string
  body: string
}

export interface FeedbackNote {
  id: number
  created_at: string
  /** 항목이 마지막으로 움직인 때 — 답글이 붙은 것도 움직인 것이다.
   *  알림 점이 이 값으로 판정한다. */
  updated_at: string
  created_by: string
  kind: FeedbackKind
  body: string
  /** null 이면 아직 열려 있다. */
  resolved_at: string | null
  resolved_by: string
  replies: FeedbackReply[]
}
