# 탄소 접점 계면 저항 (Rint ② · VGCF · SDCP 접합) — 설계 브리프 v0

> 에이전트 초안 (2026-10-20 · 읽기 전용 조사) · 1저자 확인 · 결정 질문 비준 전 · 원문 확인 전 숫자는 [미확인] 표지 그대로 · 범위 결정 = 1저자 10-20 (PTFE 실제 부피 · 막 + SDCP 계면 + 맨 접점 R_c 보정).

> 2026-10-20 · 읽기 전용 조사 (코드 · 원장 · 리포 변경 0) · 기준 = 작업 트리 HEAD `1fe3e0a29` (브랜치 `claude/sdcp-dem-manuscript-si-pqwtv8`) · litdb = `origin/claude/friendly-meitner-lldvar` (`58dd54f13`) 읽기만.
> 정본 계약 = `docs/reviews/contact_resistance_pipeline_draft_v2_20261006.md` §3-8 (J1–J8) + `…_v3_20261006.md` §5 (J2a–J12) + `…_v3_1_20261007.md`.  이 브리프 = 그 계약을 **구현 규칙으로 옮기는 첫 안** (Codex G2 판정 Q5 · Q13-5: ② 는 J 행동 시험 등록 뒤 **별도 심사**).
> 수치 표지: [리포] 리포 기록 · [카드] litdb 정본 카드 · [우리 산술] 그 값으로 한 계산 (인용 불가) · [미확인] 출처 없음.  1저자 비준 전 문서 (보고 → 설명 → 비준 → 실행).

## 0. 한눈에

1. 지금 VGCF 셀에는 **섬유 번호가 없다** — 선분 스탬프가 fid 를 버리고 (ijk, phase) 만 남기고 (`scripts/step3_sigma.py:945–948`), pid 는 AM 구 · 브리지만 쓴다 (`:600–602` · `:616–630`).  그래서 VGCF|VGCF 막은 RINT-01 이 막아 두었다 (`:170–175` · 파서 `:228–230` · API `:255–257` · 면 규칙 `:320–321`).
2. ① r1 면 막은 VGCF|AM · SDCP|VGCF · SDCP|AM (다른 sid) 면에 **지금도 걸린다** (`--step3-rint-e` · 4 솔브 영수증) — 단 막 면적 = 면 수 × h² (격자 산물) 이라 **탐침 전용** (v2 §3-2).  ①′ AM–AM (CNC) 은 기구 구현 · 정량 채택 · 생산 HOLD.
3. 계약 J5 는 섬유에 **면 분배를 금한다** → v0 = 접합 **instance 마다 간선 하나 (R_j [Ω])** + **교차 셀 멤버십 dof** (J1) + **등록 쌍의 융합 면 절단** (J3) + **실제 그래프 가지치기** (J7 · J12).  접점은 복셀 인접이 아니라 **연속 중심선 기하**에서 찾는다 (J2a · J2c).
4. 값: 리포 · litdb 에 **VGCF 접합 저항 실측 카드가 없다** → R_j = SBE 한 점 보정 (σ* 0.347 과 같은 "모형 내부값" 지위) · DBE = SDCP · PTFE 법칙을 **결과 전에 고정한 예측 구간** · Lee 2025 PTFE 계열 = holdout 후보 (SI 재확인 뒤).
5. 권고 순서: S0 CPU census (kgy · 솔브 없음) ∥ Codex 설계 리뷰 → 반례 시험 먼저 → v0 (VGCF–VGCF 만) → 등록 → SBE 보정 · DBE 예측.  ⚠ v0 만으로는 SDCP 법칙의 **한 끝 (융합 = 젖음 상한)** 만 나온다 — 다른 끝은 v1 (SDCP–VGCF 간선 · 공동 점유).

## 1. 현재 상태

| 항목 | 상태 | 근거 (file:line) |
|---|---|---|
| ① r1 상 경계 직렬 막 (`r1-phase-boundary-series`) | 구현 · 기본 OFF 비트 동일 · CLI `--step3-rint-e/-i` · 주 · wetted · bare · 이온 4 솔브 영수증 · G1 RINT 13 건 verified (범위 = 원장 `verified_scope`) · **탐침 전용** (①′ 정량 모드와 동시 거부) | `step3_sigma.py:152–180` · `:203–331` · 배율 `:334–360` · `solve_sigma_z` `:1841–1854` · `:2042–2054` · `mpm_webapp_payload.py:1205–1213` · `:2076–2078` · `:2360–2365` · `:2505–2507` · `run_contract.py:899` |
| RINT-01 (같은 상 계면 = AM 만) | verified (`30c8205c5`) — 첨가제 스탬프가 sid 만 바꾸고 AM pid 를 남겨 한 가닥 안 가짜 계면 (σ_e 11.1111 → 0.131752) · "②③ 은 final sid 로 가린 별도 이름공간 iid 뒤" | `step3_sigma.py:170–175` · `docs/reviews/findings.json` RINT-01 |
| ①′ AM–AM 막 (청구자 power 분할 · CNC) | 기구 구현 · Codex 10-15 재실행 296/296 · `IFACE_STATUS` = mechanism_only · PROTOCOL_FIELDS 밖 · payload 미배선 | `:951–1006` · `am_iface_ledger` `:1175–1354` · `am_iface_plan` `:1454–1594` · 관문 `:1597–1649` · `_iface_label_cut` `:1698–1722` · `iface_ctx_from` `:1730–1744` · 조립 `:2005–2033` · 원장 `:2140–2172` |
| 열린 항목 | RIMPR-01 (P2 · 조인 파서가 열 수 다른 행 · 중복 열 · 꼬리 토큰을 검사 전에 버림) · RIMPR-02 (P3 · Decimal 유한 ↔ float64 inf) · RIMP-02 부분 · RINT-06/07/08/09/15/16/21 · RINTG-01/11 · RINTV-03 = open · 수정 계획 = "세미나 뒤" 미착수 | `rint_iface_join.py:222–306` · `codex_review_rint_g2_impl_fix_recheck_20261015.md` §0 |
| ② 탄소 접합 | **계약만** (J1–J12) · 구현 0 · Codex: "큰 구조 지지 · 현재 문구만으로 ② 정량 GO 아님" | v2 §3-8 (L260–274) · v3 §5 (L220–234) · `codex_review_rint_g2_design_20261006.md` Q5 (L187–197) · Q13 (L255–264) |
| 1D 섬유망 하이브리드 | CL-23 hold — 복셀 결합 (Peaceman) 이 vox 0.4 에서 거부 · vox ≳ 1 µm 에서만 → SDCP 구 스탬프 (vox ≤ 0.15) 와 양립 안 함 | `fibre_1d_network.py:1–45` · `:216` · `:256–260` |
| SDCP 앵커 v2 (원고) | σ_VGCF* 0.347 S/cm (SBE 보정) · 8 팔 SBE 1.6209 ↔ 1.63 · DBE 1.8877 ↔ 4.68 · 비 1.1646 ↔ 2.86 · S1 기울기 d lnσ_e/d lnσ_VGCF 0.39–0.40 · S1b (DBE 따로 보정) 등록 = **보정** · TLM 비 1.09–1.23 ↔ DC 2.86 불일치 (조건 확인 대상) [리포] | `docs/reviews/sdcp_sigma_e_dcp_anchor_registration_v2_20261019.md:12` · `:143–145` · `:180–182` |
| 생산 격자 · 조성 | vox 0.15 · 브리지 0.48 · VGCF 선분 · PTFE centerline · SDCP 구 Ø0.30 · 26.7 M dof / VGCF 3 wt% 공통 · SBE PTFE 1.0 · DBE PTFE 0.5 + SDCP 0.5 [리포] | 같은 문서 `:33` · `:169` · `codex_review_request_ptfe_8arm_20260824.md:15–20` |

## 2. 탄소 접점에 필요한 것

### 2-1. 섬유 정체성

| 질문 | 답 | 근거 |
|---|---|---|
| fibre.npy 가 객체 번호를 담나 | 예 — 점마다 fid (−1 = SE · ≥0 = 섬유/응집체) · 첨가제 사이 전역 고유 (`_fid + _gfib`) · 의미 파일 `<fibre>_kind.npy` (ID_PATH 1 / ID_GROUP 0) · input_digest 에 포함 | `mpm3d_compaction.py:2530` · `:2675–2682` · `:4067–4074` · `additives.py:269–291` · `mpm_webapp_payload.py:1800` |
| VGCF fid 의 뜻 | 섬유 한 줄 (Ø0.15 · L 10 µm) · AM 안 점은 버려져 한 fid 에 틈 (조각) | `additives.py:94` · `:846–847` · `:851–887` |
| SDCP fid 의 뜻 | **그룹** (AM 에 붙은 것 = AM 구 번호 · 벌크 = 고유) → 입자 정체성 아님 · SDCP 입자 = 점 행 번호 | `additives.py:655–657` · `:731–741` |
| 지금 어떻게 굽나 | fid 마다 Amanatides–Woo 셀 · 틈 (gap_tol × 중앙 간격) 에서 끊고 (ijk, phase) 만 반환 — 두 섬유가 같은 셀을 지나도 sid 3 하나 | `step3_sigma.py:892–948` · `fibre_segment_raster.py` |
| 덮어쓰기 우선순위 | AM → 브리지 → VGCF(3) → SuperP → SDCP 구(5) → PTFE(7) → SWCNT(8) — PTFE 가 지나는 VGCF 셀은 **절연이 된다 (섬유 절단)** · SDCP 구는 VGCF · AM 셀을 대체 · SDCP 구는 `np.unique` 로 합쳐 입자별 소유가 없다 | `:771–800` · `:699` · `codex_review_request_ptfe_8arm_20260824.md:26` |
| 빈 곳 | ① 셀 → fid **멤버십** (교차 셀 = 여러 fid) 없음 ② 연속 기하 **접합 원장** 없음 ③ SDCP 입자 소유 없음 ④ 덮어쓰기 = "마지막 승자" — 접합 저항을 걸면 통과 섬유에 가짜 직렬 막 (J1 · RINT-01 과 같은 부류) | — |

### 2-2. 면 부류 (최종 raster 기준)

| 부류 | 판정 | v0 | v1 |
|---|---|---|---|
| VV-axial | 두 VGCF 셀이 공통 fid | bulk 그대로 (교차 셀은 fid 마다 자기 dof) | 같음 |
| VV-junction | 서로소 멤버십 · 등록 instance 쌍 | 면 절단 + instance 간선 하나 (J3) | 같음 |
| VV-unreg | 서로소 · 등록 없음 (양자화 근접 융합) | 선언 법칙 cut / fused / reject — 자동 fallback 없음 (RINT-08) · 두 끝 구간 보고 | 같음 |
| VA | VGCF ↔ AM | legacy 융합 (선언 기록) | J2b instance 간선 (중심선 ↔ 구 중심 ≤ r_f + R_AM + tol_fs) |
| SV | SDCP ↔ VGCF | legacy 융합 (= 젖음 상한 · 선언) | instance 간선 + **공동 점유** (SDCP 가 덮은 VGCF 셀의 섬유 연속 유지 — 없으면 통과 섬유에 가짜 막) |
| SA | SDCP ↔ AM | legacy 융합 | 구–구 instance (①′ 청구자 규칙 재사용 후보 · a < h 표지) |
| SS · PTFE 낀 면 | SDCP 끼리 · σ_PTFE = 0 | 그대로 (PTFE 면 = 없음) | 같음 |
| 교차 셀의 비탄소 면 · 판 결합 | 멤버십 ≥ 2 셀 | 기하 최근접 멤버십 (집합 규칙 · ε 띠 · canonical 키) · 수 기록 (J9) | 같음 |

### 2-3. 재사용

| 무엇 | 어디서 | 쓰는 법 |
|---|---|---|
| 요청 ↔ 적용 영수증 (4 솔브 · "모델 없으면 검사 생략" 금지) | `run_contract.interface_record_ok` `run_contract.py:899` | 같은 꼴 `cjunc_record_ok` |
| 계획 dict · 지문 · 변조 · vox 결합 · r1/주기 거부 | `iface_require_quantitative` `step3_sigma.py:1597–1649` · `_grid_fp` `:183` | 패턴 그대로 |
| 면 g 덮어쓰기 · 절단 tombstone | `_ifa_assemble` `:2005–2033` | 멤버십 재배선 · 간선 추가로 확장 |
| 실제 간선 그래프 연결 성분 | `_iface_label_cut` `:1698–1722` | 추가 dof · 접합 간선을 넣도록 확장 |
| 집합 소유 규칙 (ε 띠 · canonical) | `_iface_owner_select` `:1107–1141` | 교차 셀 주 멤버십 · (v1) SDCP 입자 소유 |
| 진단이 원장을 읽기 · 지문 대조 | `iface_ctx_from` `:1730–1744` · `_iface_override_g` `:1747–1758` | 같은 규칙 |
| 에너지 몫 (E4′) | `iface_face_split` `:1687` | 간선 P = g·Δφ² |
| 선분–선분 거리 · 틈 분할 · 접촉 목록 | `fibre_1d_network.py:48` · `:90` · `:115` | CL-23 hold 모듈 — 승격 금지 · J2 시험으로 재자격 |
| 직접 풀이 시험 틀 | `test_rint_g2_am_iface.py:76–85` | 그대로 |
| raster-only 원장 (census 틀) | `mpm_webapp_payload.py:2008–2050` · `rint_t41_census.py` | S0 도구 |
| 쓰지 않음 | CNC 면 분배 `iface_rface_ohm_cm2` `:1652` (J5 금지) · 단일 승자 iid (Codex 1단계 Q1) · AM pid (RINT-01) | — |

### 2-4. 피해야 할 것 (원장 교훈 → v0 규칙)

| 교훈 | 원장 | v0 규칙 |
|---|---|---|
| 물려받은 번호 = 가닥 안 가짜 계면 | RINT-01 | 섬유 이름공간 = fibre.npy 경로 fid (ID_PATH · phase 2) · 최종 sid = 3 으로 가린 뒤 · pid 금지 |
| 단일 승자 셀은 교차를 못 담는다 | Codex 1단계 Q1 · J1 | 교차 셀 = fid 마다 dof |
| 총량 정규화 ≠ 위치 · 연산자 · 면 수 = 격자 산물 | RINT-06 · RINTG-02 · J5 | 면 분배 없음 · instance 간선 |
| 쌍별 ε fold 비추이 · raw 순서 의존 | RINTV-01 · 02 · RINTG-01 | 집합 규칙 · 동결 raster 위 불변만 주장 · raw 순열 = 진단 |
| 쌍 ID ≠ instance · R_j=0 = 축약 · 리드 이중계상 | RINT-08 · J2 · J4 · J6 | instance 단위 · 정량은 R_j > 0 만 (0 = 시험 전용 축약 기준) · 포트 = 셀 중심 · 반셀 미포함을 기록 (RINTG-09) |
| 셀 6-연결 라벨이 접합 · 절단을 모른다 | J7 · J12 | 실제 그래프로 가지치기 (현행 `ndimage.label` `:1957`) |
| 계획 ↔ 솔버 vox | RIMP-05 | 계획에 vox · lo · shape · fp_sid · fp_멤버십 · 입구 대조 |
| 입력 일부를 검사 전에 버림 · float64 비유한 | RIMPR-01 · 02 | fibre · kind · 점 수 정확 일치 · float64 유한 검사 · 불일치 = 거부 (현행 길이 불일치 → segment 모드 중단 `mpm_webapp_payload.py:1848–1851` · `:1926–1931` 과 같은 fail-closed) |
| 4 솔브 중 하나 누락 = 초록 | RINT-02 · 14 | 주 · wetted · bare = applied · 이온 = disabled_channel (탄소 σ_ion 0 `step3_sigma.py:121–129`) |
| Joule · STEP4 · 러너 캐시 | RINT-04 · 05 · 15 | 접합 소산 몫 따로 · STEP4 grid 저장 동시 거부 · OUTDIR 태그 · SKIP 키에 계획 해시 |

## 3. 최소 구현안 v0 (VGCF–VGCF 만)

### 3-1. 입력 · 스위치
- 입력: 최종 sid · VGCF 멤버십 (`_fibre_segment_ijk(…, return_fid=True)` opt-in → `rasterize` 셋째 반환 opt-in · 기본 반환 그대로) · VGCF 중심선 (MPM 끝 점 + fibre.npy + kind · 틈 규칙 = 스탬프와 같은 gap_tol) · R_j 표 · 법칙 선언 (unreg · 긴 접촉 · 포트 덮임 · VA/SV/SA = legacy) · 기하 문턱 tol_ff · L_par · r_port = **결과 전 1저자 숫자** (J10).
- API 3 단 (①′ 와 같은 꼴 · 기본 None): `cjunc_registry(...)` (기하만) → `cjunc_plan(registry, R_j, laws)` → `solve_sigma_z(..., cjunc=plan)`.
- 두 스위치를 따로 보고 (v2 §3-8 "기하 팔 · 값 분리"): T = 위상 (등록 접합 + 멤버십 + 절단) · V = 값 (R_j).  OFF → T + 작은 R_j → T + R_j.  T 만으로도 σ 가 바뀐다 (모서리 접촉 연결 · 근접 융합 절단) — 그 몫을 막 효과와 섞지 않는다.

### 3-2. 접합 원장
- J2a: 두 중심선 선분 최근접 d ≤ r_fi + r_fj + tol_ff (VGCF r 0.075 µm) · J2c: 연속한 선분 쌍 = instance 하나 (조각 경계 넘어도) · 같은 쌍의 떨어진 두 곳 = instance 둘 · 길이 > L_par = 긴 접촉 (정량 거부 · 수 기록 · J8 · J11).
- 포트: 최근접 점 → 그 fid 멤버십을 가진 최종 VGCF 셀 · 덮였으면 경로를 따라 r_port 안 최근접 · 없으면 `unrealized_overwritten` (사유 SDCP / PTFE).
- canonical 키 = (fid 쌍 정렬, 최근접 점 좌표) — 점 · 섬유 순서 무관.

### 3-3. 조립 (덮어씌움)
- dof = 기존 셀 dof + 교차 셀의 추가 멤버십 dof (n_dof + k) — 각 fid 는 자기 직경 보존 σ 로 축 연속.
- 면 재배선: 공통 fid 면 → 그 fid dof 끼리 · 서로소 VV 면 → 등록 쌍이면 절단 · 아니면 법칙 · 비탄소 면 · 판 결합 → 기하 최근접 멤버십.
- 접합 간선: instance 마다 포트 dof 사이 g_code = 1e4/R_j (코드 g = 물리 G × 1e4 · `iface_code_G_S` `:1672–1674` 의 역).
- 가지치기 = 실제 그래프 · 관통 성분 조기 반환 규칙 그대로 (`:1980–1996`).
- 원장 (E1): 간선마다 (dof_a, dof_b, instance, 쌍, R_j, g) + 지문 → 해에 싣는다 · 출력 = σ_eff · 접합 전류 · 접합 소산 몫 · 실현/미실현 수.
- v0 출력 = **σ_e 전용** (LEAN=2 와 같은 팔) · 장 · je · 분담 · Joule 진단은 원장 소비 구현 전 **거부** (fail-closed).

### 3-4. 막 법칙 · 단위 · 영수증
- G_j = 1/R_j [S] (instance 하나 · 면적 법칙 없음) → g_code = 1e4·G_j.  r_c [Ω·cm²] 로 받으려면 면적 법칙 A_c 를 함께 등록: R_j = r_c/(A_c[µm²]·1e−8) → g_code = 1e−4·A_c/r_c (RINTG-07 꼴).
- 기록: `cjunc_model` (이름 후보 `r3-carbon-junction-port`) · R_j 표 · 법칙 · 문턱 · σ_fibre · 직경 규약 (J4 — R_j 와 같이 봉인) · instance 수 (부류 · 실현/미실현 · 긴 접촉 · unreg) · 지문 (registry · plan · sid · 멤버십 · vox · lo) · 솔브별 영수증.
- 회계: `record` 축 (p2 봉인 코호트 보존) · 채택 날 PROTOCOL_FIELDS → p3 · 새 CLI (예 `--step3-cjunc`) — r1 플래그와 겹치지 않음 (D14).
- 거부: r1 표 동시 · ①′ 동시 · 주기 · `--step3-fibre-stamp point` · STEP4 grid 저장 · SDCP 브리지 진단 팔 · fibre/kind 길이 불일치 · 비유한 좌표.

### 3-5. 먼저 쓸 시험 (옛 코드 실패 확인 → 구현 · 규율 ②)

| ID | 픽스처 (h 1 µm · 직접 풀이) | 기대 | 옛 코드 |
|---|---|---|---|
| C0 off_bitid | cjunc=None · return_fid 끔 | σ · φ · n_dof · 분담 · je · rasterize 비트 같음 (OFF 16 입력 대조) | 회귀 |
| C1 cross_shared | 판 ↔ 섬유 A ↔ 교차 셀 ↔ 섬유 B ↔ 판 | R = R_A + 1/G_j + R_B 해석해 (상대 1e−12) · R_j 스윕 단조 (Rayleigh) | legacy 융합 = R_j 무시 |
| C2 cross_face · cross_edge | 면 인접 · 모서리 인접 접촉 | 면: 옛 융합면 절단 + 간선 하나 · 모서리: legacy 단절 (σ 0) → v0 연결 · 가지치기가 안 지움 | 위상 효과 (기록) |
| C3 pass_through | 섬유 B 가 A 의 교차 셀 관통 | B 저항이 R_j 와 무관 · R_j → ∞ 에서도 B 연속 (J6) | 단일 승자 + 면 막 = 직렬 막 둘 (반례) |
| C4 series_chain | N 섬유 사슬 · N−1 접합 | R 이 N · R_j 에 선형 · 단위 변이 (1e4 빠짐 · ×1e8) 실패 | — |
| C5 instance | 같은 접촉을 조각 둘로 · 같은 쌍 두 곳 · 섬유 · 점 순열 · 점 역순 | instance 1 · 2 (등전위면 R_j/2) · 원장 · σ 비트 같음 | — |
| C6 energy | 작은 침대 | ΣP_bulk + ΣP_junc + ΣP_plate = I·ΔV · 접합 몫 = −∂lnσ/∂lnR_j (중심 FD) | — |
| C7 unreg · long | 틈 > tol 인데 면 인접 · 평행 긴 접촉 | 법칙 미선언 = 거부 · cut ≤ fused 구간 · 긴 접촉 정량 거부 | legacy 조용히 융합 |
| C8 guards | 솔버 vox ×2 · 원장 변조 · r1 동시 · 길이 불일치 · NaN · 주기 | 조립 전 거부 · CG 호출 0 | — |
| C9 receipts | 주 · wetted · bare · 이온 | applied ×3 · disabled ×1 · 배선 하나 지우면 계약 실패 | — |

### 3-6. 단계 · 노력

| 단계 | 산출 | 크기 | 선행 |
|---|---|---|---|
| S0 census (CPU · kgy · 솔브 없음) | SBE · DBE 킷 (+ Lee 0.5/1 wt% 침대 — 위치 · 가용성 확인 대상) 의 instance 수 (VV · VA · SV · SA) · 복셀 관계 (같은 셀 · 면 · 모서리 · 꼭짓점 · 틈) · 교차 셀 수 · unreg 면 · 긴 접촉 · 포트 덮임 (SDCP · PTFE) · PTFE 근접 분포 · 둘 이상 섬유에 닿는 SDCP 수 · 섬유당 접합 간격 ℓ_j | S–M | — |
| S1 설계서 v0 + Codex 설계 리뷰 | J 계약 대응표 · 문턱 숫자 (1저자) | S | S0 와 병렬 |
| S2 반례 시험 | §3-5 C0–C9 (옛 코드 실패 기록) | M | S1 |
| S3 원장 · 멤버십 · 포트 | `_fibre_segment_ijk` opt-in · `cjunc_registry` · `cjunc_plan` | M | S2 |
| S4 조립 · 그래프 · 원장 · 해 기록 | `solve_sigma_z(cjunc=)` | L | S3 |
| S5 payload · 계약 · 러너 키 · 웹앱 표지 (J20-l) | `--step3-cjunc` · `cjunc_record_ok` | M | S4 |
| S6 등록 → SBE R_j 사다리 → DBE 예측 | GPU — [리포] S1 · C 실측 863–3,009 s/팔 · σ_fibre 대비가 크면 더 (Q4) | 계산 | S5 + Codex 구현 리뷰 |
| v1 | VA · SV · SA 간선 · 공동 점유 · PTFE 덮인 접합 법칙 · 장 진단 | L | v0 결과 |

## 4. 값 — R_j 를 어디서 정하나

### 4-1. 확인한 사실
- litdb 정본에 VGCF/CNF **섬유–섬유 접합 저항 값 카드가 없다** (`git grep` "junction resistance · 섬유-섬유 접촉 …" → patil1987 · zhang2026 의 정성 문장 두 줄뿐) → R_j = [미확인] = 보정값.
- 단섬유 σ [카드 `endo2001_vgcf_basic_properties_battery_applications`]: 흑연화 s-VGCF 1×10⁻⁴ Ω·cm (stated p.1289) · 압착분말 ≈ 0.012 Ω·cm @ 0.8 g/cm³ (그림 판독).  ⚠ 우리 VGCF 와 같은 등급인지 이 논문으로 판정 불가 (카드 §3-5 · "VGCF-H" 이름 인용 금지).  직경 보존 (`step3_sigma.py:2479–2536`) 하면 vox 0.15 에서 7,854 S/cm [우리 산술 = 1e4 × π/4].
- Lee 2025 [카드 `lee2025_corolling_dryprocess_lpscl_ptfe` · DOI 10.1038/s41467-025-59363-4 · `docs/data/lee2025_transport_anchors.csv`]: PTFE 0.5 / 2 / 5 wt% → σ_e 34 / 4.5 / 0.011 mS/cm (CAM:SSE:VGCF 80:17:3 고정 · 75 MPa · DCP · 카드 표기 "stated SI Fig. 5" · 06-24 digest).  VGCF 3 wt% = 우리와 같다 · 그러나 공정 (co-rolling) · 압력 · 측정이 달라 34 ↔ 우리 DC 1.63 · 4.68 = 7–21 배 차 → **PTFE 용량–반응의 모양만** 후보 · 쓰기 전 SI 원문 재확인 (규율 ⑥ · v2 §3-12 조건 1).
- 주의 [카드 `lee2026_unveiling_ptfe_dry_electrode_digital_twin`]: PTFE 0.2 wt% 가 σ_e 를 약 2 배 **올린다** (실측 +105 %) · 접합 저항 없는 복셀 FV 가 +101 % 로 재현 = **배치** 효과 → PTFE 효과 전부를 접합 저항에 넣으면 배치 몫과 섞인다.
- "C 안 (Lee 접점 배수 2.05 → σ 0.712 → DBE 어림 2.6)" 은 리포에 유도 기록이 없다 [미확인] (`…registration_v2_20261019.md:180`).
- 규모 감각 [우리 산술 · 인용 불가]: Holm 협착 1/(2σa) (σ_f 1e4 S/cm · a = d/4 = 0.0375 µm) ≈ 13 Ω ↔ σ* 0.347 을 섬유 사슬의 접합으로만 읽은 등가 R_j ≈ 1.3 MΩ × (ℓ_j / 1 µm) → 보정 R_j 는 협착이 아니라 막 (PTFE · 표면층 · 간극) 지배일 것 (추정) · ℓ_j 는 S0 가 잰다 → 등록 전 "결과 전 어림".
- 민감도 경고 [리포 CL-48]: 섬유를 단섬유 σ (7,854) 로 두면 (접합 저항 0) SDCP 이득 부호가 뒤집혔다 (G −0.108 · 옛 설정) — 탄소 저항이 섬유에 퍼져 있나 접합에 몰려 있나가 DBE/SBE 를 좌우한다.

### 4-2. 선택지

| 안 | 보정 (자료) | DBE | 남는 자유도 | 판정 |
|---|---|---|---|---|
| **A (권고)** | R_j,0 하나 ← SBE 1.63 (S1/S2 사다리 규칙 · ln σ_e ↔ ln R_j) | **예측 구간** = SDCP 법칙 {legacy 융합 · R_j,0 과 같음} × PTFE 법칙 {현행 표현 · 덮인 접합 = 절단} (결과 전 고정) | 법칙 → 구간 폭으로 보고 | "보정 1 점 · 예측 구간" 문장 가능 |
| B | R_j,0 ← SBE + PTFE 기울기 ← Lee 0.5 → 2 wt% 비 (Lee 조성 침대 · 2 wt% 침대 새로) | 점 예측 | 실험실 · 공정 차 · 배치 몫 | Lee 모양 이식의 정당화가 따로 필요 |
| C (현 S1b) | σ*_SBE · σ*_DBE 둘 다 보정 | 예측 아님 | — | 비교용으로 늘 함께 |
| 탐침 | r1 면 막 (SDCP\|VGCF 등) · iid 면 막 | — | 면 수 격자 산물 · 통과 섬유 가짜 막 | 원고 불가 · 정찰만 |

### 4-3. 남는 보정 · holdout
- 보정 = R_j,0 — 침대 · vox 0.15 · σ_fibre · 포트 규칙에 묶인 **모형 내부값** (σ* 와 같은 지위 · 물성 아님 · J4 de-embedding 대상 아님).
- holdout = DBE DC 4.68 (조건 확인 뒤 · TLM 불일치 해소 전에는 판정 보류) · Lee PTFE 계열 모양 (Lee 2/5 wt% 침대가 생기면) · vox 사다리 (0.15 ↔ 0.2/0.25 에서 R_j* 안정성).
- 등록 문서 먼저 (결과 0 건): 문턱 · 법칙 · 보정 자료 · holdout · 판정 문장 · 금지 문장 (v2 §3-12 조건 4 — 같은 측정으로 맞추고 맞았다고 쓰지 않는다).

## 5. 1저자 결정 (권고 한 줄)

- **Q1 범위 · 순서** — v0 = VGCF–VGCF 만 · S0 census ∥ Codex 설계 리뷰 → 시험 먼저 → 구현?  권고: 예 (② 별도 심사 = Codex Q13-5).
- **Q2 매개변수** — 섬유 접합 = R_j [Ω] / instance · r_c [Ω·cm²] 는 A_c 법칙을 등록할 때만?  권고: R_j.
- **Q3 접점 원천 · 문턱** — 연속 중심선 (MPM 끝 점 + fibre.npy) · tol_ff · L_par · r_port 숫자는 1저자?  권고: 예 · census 기하 분포를 본 뒤 (σ 보기 전) 고정.
- **Q4 σ_fibre** — Endo 단섬유 (1e4 → 7,854 S/cm) + ÷10 무감도 확인 · CG 대비 (AM 0.0041 ↔ 7,854 ≈ 2e6) 가 비싸면 AMG (CPU) 또는 maxiter 상향?  권고: Endo 값 · 무감도 시험을 등록에 넣는다.
- **Q5 덮어쓰기** — PTFE 의 VGCF 절단 · SDCP 의 VGCF 대체를 v0 에서 현행대로?  권고: 유지 (비트 같음 기반) · census 로 수 기록 · 공동 점유는 v1 (SV 간선에 필수).
- **Q6 값 규약** — 안 A (SBE 한 점 보정 · DBE 예측 구간)?  권고: A · C (S1b) 는 보정으로 함께 보고.
- **Q7 SDCP 법칙** — 구간 두 끝 = {legacy 융합 (젖음 상한) · R_j,0 과 같음 (젖음 효과 없음)} · DBE 로 맞추지 않음?  권고: 예.
- **Q8 PTFE 법칙 (v1)** — 연속 기하 "덮인 접합" (PTFE 중심선 거리 ≤ r_P + r_f + tol_P) 두 끝 {영향 없음 · 절단}?  권고: 예 · Lee 모양은 holdout (B 안 = Lee 2/5 wt% 침대 + SI 재확인 뒤에만).
- **Q9 동시 사용** — ①′ · r1 과 함께 켜기를 v0 에서 거부?  권고: 거부 (이중 막 · 해석 혼선).
- **Q10 실험 표적** — DC 2.86 ↔ TLM 1.09–1.23 조건 확인을 등록 전에?  권고: 예 (holdout 이 흔들리면 예측 판정이 무의미).

## 6. Codex 설계 리뷰 질문 초안

1. 멤버십 dof (교차 셀) + instance 간선 + 등록 쌍 면 절단을 기존 FV 위 덮어씌움으로 넣는 v0 구조가 J1 · J3 · J7 · J12 를 충족하나?  비탄소 면 · 판 결합을 "기하 최근접 멤버십 (집합 규칙)" 에 주는 것으로 J9 가 충분한가?
2. 접점 원천 = MPM 끝 점 중심선 (틈 분할 = 스탬프 규칙) · J2a/J2c · 긴 접촉 정량 거부 — 등록 전에 더 고정할 것은?
3. 위상 (T) ↔ 값 (V) 분리 보고 + "정량은 R_j > 0 · R_j = 0 축약은 시험 전용 기준" 이 J6 을 만족하나?
4. 포트 = 셀 중심 · 반셀 미포함 · 보정 R_j 를 de-embedding 없이 "모형 내부값" 으로 두는 것이 J4 와 양립하나?
5. v0 에서 PTFE · SDCP 덮어쓰기 (섬유 절단 · 대체) 를 legacy 로 두고 수만 기록해도 되나?  v1 공동 점유 계약에 빠진 것은?
6. 안 A (SBE 한 점 보정 · SDCP/PTFE 법칙 두 끝의 DBE 구간) 를 "예측" 으로 부를 수 있나?  금지할 문장은?
7. σ_fibre 단섬유값의 CG 대비 (≈ 2e6) — 무감도 시험 · AMG · 섬유 내부 축약 중 무엇을 요구하나?
8. `cjunc` 영수증 (주 · wetted · bare applied · 이온 disabled) · record 축 · 러너 SKIP 키 해시로 RINT-02 · 14 · 15 부류가 닫히나?
9. census (S0) 기하 분포를 본 뒤 (σ 열람 전) 문턱 · 법칙을 정하는 것이 결과 전 등록 원칙과 충돌하나?
10. RIMPR-01 · 02 (조인 파서) 를 이 트랙 전에 닫아야 하나, 병행해도 되나?
