# MPM 피복률 · AM–SE / SE–SE 계면 — 모델 설계 메모 (Rint ② 와 공통 정의 · 2026-11-03)

> **지위** — 설계 메모 (정의 · 계획만) · 코드 변경 0 · 런 0 · 결과 0 건 · 1저자 확인 전 (질문 = §4-3).  기준 작업 트리 = 커밋 `57f1b2baf` (코드 행 번호 = 이 커밋).
> **계기** — 1저자 11-03: MPM 모델 설계를 Rint ② 와 **같이** (정의 공유) · 50kg 보고 coverage 질문 뒤 피복률 개선 (메인 지시 · 리포 기록 [미확인]).  리포 기록 = 11-02 밤 2 *"MPM관련 수치들도 Rint와 함께 다 업데이트"* · *"전해질 입자 번호 … atom dump에 다 있으니까 승계"* (`docs/handoff_return_to_stoic_knuth_20261103.md` §2-1-2 · §2-1-4 ⑤) · 원장 `MPMC-01`–`03` · coverage 질문 기록 = `docs/50kg/report_y4/meeting_20261104/final_deck_20261103/README.md` 절 *"입도 ↔ coverage"*.
> **구현 시점** — Rint ② Codex 회차 ② 요청서 발송 **뒤** (1저자 지시 때) · Rint R 런을 늦추지 않는다 (§6).
> **수치 표지** — [리포] 파일 · 행 · [우리 산술] 리포 값으로 한 계산 (인용 불가) · [미확인] 출처 없음 · (추정).
> **ID** — 이 메모 안에서만: DM = DEM · MP = MPM 점 구름 · VX = 복셀 격자 · RT = Rint ② v0 · ID = 번호 운반 · O = 새 관찰 · G = 격자 한계 · T = 시험 (50kg 침대 이름 D1–D3 · 설계 §10 N1–N18 · v2 S1–S6 와 겹치지 않게).

---

## 0. 한 줄

- 피복률 · 계면 면적 = **한 정의 묶음** — ① 정체성 (AM = scaffold canonical id · SE = DEM atom id 승계 · 탄소 = fid) ② 소유 = power diagram (근축면 · ①′ 와 같은 함수) ③ 면 집합 = 주인이 다른 이웃 셀 면 ④ 면적 = 면 수 × h² + 법선 보정 · 미해상이면 ①′ 총량 정규화 ⑤ 기준 = 씨앗 상태 (같은 함수) + 강체 해석값 ⑥ 주기 = 측정은 x,y 최소 영상 · STEP3 풀이는 v0 대로 비주기.
- 피복률 주 값 = **간격 0 (닿음)** — DEM 접촉 피복과 같은 뜻 · 0.13 / 0.26 µm 띠 = 보조 "근접 띠" (이름 바꿈 · Q1).  50kg 질문 답의 *"실제 감싸기 몫은 MPM 으로"* = 이 정의의 소성 증가분 ΔC = C_끝(0) − C_씨앗(0).

## 1. 목적 · 범위

| 하는 것 | 하지 않는 것 |
|---|---|
| 지금 계산되는 피복 · 계면 양 전수 (§2) · 결함 (§3) | 코드 · 런 · 새 수치 |
| Rint ↔ MPM 공통 정의 (§4) · 시험 먼저 계획 (§5) · 일정 (§6) | **Rint ② v0 변경** — S0–S3 · 등록 R 숫자 칸 · 스위치 · 물리 (v0 범위 동결 · 설계 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` 4판 · 등록 `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md`) |
| 다음 트랙 (SE–SE 이온 계면 · 첫 침대 50kg D1–D3) 의 계약 | 입력 σ 규약 ④ (SE 3.0 = 펠릿값 · σ₀ 1.5 보고 기준) · 막 값 r 인용 |
| `MPMC-01`–`03` 고침 방향 다듬기 | 50kg AM 상 (다결정 ↔ 단결정 · STEP3 σ_e) 결정 · 활물질끼리 계면 (실험 쪽 요청 · 11-02 Q2) |

- 같은 묶음이지만 이 메모 밖 = STEP3 수치 갱신 (σ₀ 1.5 · AM 상 · 계면 항 · 11-02 밤 2).
- v0 와의 관계: 공통 정의는 v0 가 **이미 지키는 것** (SE = 번호 없는 연속체 · 설계 §3-1) 을 문서로 적고, 다음 트랙은 **끄면 v0 비트 같음** 으로만 얹힌다 (§4-2 · T10).

## 2. 지금 정의 inventory

| # | 이름 (키) | 식 · 자리 | 재는 것 | 알려진 결함 | 쓰는 곳 |
|---|---|---|---|---|---|
| DM1 | DEM 기하 피복 (`coverage_AM_*_mean`) | Σ c_cpl[22] (AM–SE) / (4πR² − Σ AM–AM) · min 100 — `scripts/dem_analysis_core.py` `calc_coverage` (244 행) | 접촉 원판 넓이 **합** 비 (기하 교차 원판 · Hertz 탄성 아님) | `L1-04` (c_cpl[22] 를 Hertz 로 읽음 · 1.9875× · claimed_fixed) · 겹침 무시 합 | 웹앱 · LHS 인계 · 50kg 덱 5장 'Hertz' 19.1 / 21.1 / 19.0 % (3 / 2 / 1 µm · `docs/data/kg50_mpm_20261102/README.md` §3 · 합 ↔ 합집합 어느 함수인지 [미확인]) |
| DM2 | DEM Physics 합집합 피복 (`*_physics_union`) | 접촉마다 AM 구면 cap (넓이 = g2 면적 · cosθ = 1 − A/(2πR²)) 합집합 ∩ 자유 표면 — `scripts/coverage_physics_vs_hertzian.py` `union_coverage_bed` (448 행) → `scripts/plastic_coverage.py` `union_cap_coverage` (705 행) | 덮인 표면 비 · **최소 영상** (상자 필수) · AM–AM cap 가림 | `GEN2-02` (완전 포함 쌍 → 침대 빈칸) · `AREA-08` (cap 넓이 = 원판 넓이로 놓음 · a = 0.8 r 에서 구면 cap 은 원판의 1.25 배) · `LHS-34` | 50kg 덱 노트 52.6 / 54.2 / 46.8 % (`docs/50kg/report_y4/meeting_20261104/values/values_D123.csv` 'AM coverage') |
| DM3 | DEM 접촉 수 · 접촉 하나 면적 | CN AM–SE · c_cpl[22] 평균 — `values_D123.csv` | 10.3 / 24.1 / 99.7 개 · 1.971 / 0.937 / 0.211 µm² | — | 50kg 덱 9장 (coverage 대신) |
| MP1 | MPM 소성 피복 (`coverage_AM_*_hertz_pct` · `_tabor_pct`) | AM 구면 Fibonacci 표본 → 가장 가까운 **변형 SE 점** 거리 < b + r_pt (b 0.13 · 0.26 µm · r_pt = ½ 중앙 NN 간격) 비율 — `scripts/mpm_webapp_payload.py` `deformed_coverage` (193 행) | 띠 근접 (닿음 아님) | `MPMC-01` · `02` · `03` · 분모 = AM 구면 전체 (AM–AM 가림 안 뺌 · 코드 읽기) · 없는 상 0.0 (`WEB-10`) | payload · 웹앱 MPM lab · 뷰어 패치 · 50kg 27.5/37.5 · 36.0/52.0 · 56.0/80.0 % |
| MP2 | MPM 강체 피복 (`coverage_AM_*_rigid_*`) | 표본 → 가장 가까운 SE **중심** 거리 − r_SE < b — 같은 파일 `geometric_coverage` (244 행) · r_SE = 첫 행 반경 하나 (252 행) | 같은 띠 · DEM 구 (씨앗) 해석 | `MPMC-01` · `03` · 다분산 SE 에서 틀림 (O3) · `AREA-08` (cap 식별 시험 아님) | payload · 50kg 24.6/32.9 · 32.2/46.4 · 51.2/76.3 % |
| MP3 | MPM 복셀 인접 미리보기 (`coverage_AM_*_pct` · mpm_metrics) | AM 표면 셀 중 SE 점유 셀 (closing 1) 을 마주보는 면 비율 — `scripts/mpm3d_compaction.py` `coverage_fraction` (1127 행) | 격자 · 밀도 묶임 | 보고 금지 (`docs/mpm_coverage_plastic_vs_rigid.md` §1) · 없는 상 0.0 (`WEB-10` 뿌리) | metrics 만 (50kg 24.1 / 28.8 / 36.0 % · 묶음 `docs/data/kg50_mpm_20261102/kg50_mpm_results_slim.tgz`) |
| VX1 | STEP3 면 걷기 피복 f_reaction (Track-B) | AM 셀 (sid 1·2) 의 비-AM 이웃 면 중 반응상 (SE 6 · SDCP 5) 비율 · 입자별 — `scripts/step3_sigma.py` `am_surface_patches` (4832 행) | **STEP4 BV 접촉면과 같은 면 집합** (AM\|SE · AM\|SDCP) | 계단 ~1.5× (비율은 상쇄 · 절대 면적 아님 · docstring) · SE 셀 = 점 하나라도 (673–678 행) = 사실상 띠 ≈ vox · `periodic_xy` False 면 seam = void | STEP4 · Track-B (50kg 입자별 벡터 = 원 payload 만 · slim 에서 빠짐) |
| VX2 | STEP3 막 r1 (탐침) | 다른 sid 면 · 같은 sid 는 pid 다른 면 — `face_rint` (362 행) · `interface_face_factor` | 면마다 r | 같은 상 계면 = AM 만 (`PID_OWNER_SIDS` {1, 2} · 224 행 · `RINT-01`) → SE\|SE 없음 · `RINT-21` | 정량 모드 거부 (탐침 전용) |
| VX3 | ①′ AM–AM 원장 | 청구자 (`_ball` ∪ 브리지) 중 power 최소 (I8′ 집합 ε 규칙) · 면 집합 S_c · r_face = r·N_c·h²/A_true · A_true = 렌즈 원판 — `am_iface_ledger` (1263 행) · `am_iface_plan` | 미해상 접점 막 총량 | `RINTG-11` (행 순서 의존) · `RINTV-03` · 생산 HOLD | 기구만 |
| VX4 | SE–SE 접촉망 실험 모드 | 변형 SE 점 → closing → **중심 Voronoi** → 다른 ID 면 수 × h² → Holm g = 2√(a/π) — `scripts/voxel_conductivity.py` `se_contact_network` (300 행) | SE–SE "소성 접촉 면적" | 과대 (Voronoi 패싯 = 공극 건너도 셈 · 스스로 EXPERIMENTAL · 311–318 행) · 비주기 · bulk 항 없음 | 쓰지 않음 (v2 §3-9 S6) |
| RT1 | Rint ② S1 PTFE 면 개구율 α | 면 위 K×K 구적점 중 캡슐 밖 비율 · g = α·g0 · 이온 채널 = SE\|SE · SE\|SDCP 면 (SE = 번호 없는 연속체) — 설계 §3-1 | 면 배율 | K = 8 거짓 절단 (설계 §3-4 F16) · 주기 = 정량 거부 (§3-3) | 등록 R (v0) |
| RT2 | Rint ② S2 VV 접합 · S3 SDCP c | instance · 포트 dof · 분산판 간선 g = 1e4/R_j′ · 멤버십 (cell, fid, branch) — 설계 §4-1 · §5 | 탄소–탄소 접합 | — (SE 와 교차 없음) | 등록 R (v0) |
| ID1 | SE 입자 번호 운반 | 씨앗 셀 → 가장 가까운 DEM SE **중심** (Voronoi) → 점 8 개 복제 — `scripts/mpm3d_compaction.py` 2351–2352 행 · 저장 `--save-se-id` (587 행) | 셀 → SE 입자 | 반경 안 봄 (다분산이면 ≠ power · v2 §3-9 S1) · KD-tree 비주기 ↔ 래스터는 x,y wrap (2097–2123 행) | 50kg 키트 런 = 안 켬 |

- 공통점: 격자 · 점 구름 피복 측정 셋 (MP1 · MP3 · VX1) 은 **사실상 띠 ≈ 격자 한 칸**이다 (점 하나라도 SE · r_pt ∝ 점 간격 · 코드 읽기) — 그 치우침을 잴 기준이 지금 없다 (`MPMC-02` 의 원인 · §4-1 "기준 셋").

## 3. 결함 목록

| ID | 결함 | 크기 · 근거 | 고침 자리 |
|---|---|---|---|
| `MPMC-01` (P2 open) | MP1 · MP2 = 띠 안 근접 비율 ≠ 닿은 면적 · 작은 SE 가 많을수록 개수만으로 커짐 | 강체 Tabor 띠 33 → 46 → 76 % ↔ DEM 합집합 52.6 → 54.2 → 46.8 % (`docs/data/kg50_mpm_20261102/README.md` §3) | §4-1 C(b) · Q1 |
| `MPMC-02` (P2 open) | "소성 − 강체" 가 씨앗 상태에서도 + — 이산화 치우침 | 씨앗 상태에서 이미 2.3 … 5.1 %p 높음 ↔ 실측 소성 − 강체 = 2.9 … 5.6 %p (원장 · kg50 README §3) — 진짜 소성 몫이 치우침 안 | §4-1 기준 셋 · T2 · T12 |
| `MPMC-03` (P2 open) | MP1 · MP2 가 x,y 주기 이미지를 안 봄 | 강체 −2.3 … −3.3 %p · 씨앗 −1.0 … −1.8 %p · 비대칭 +1.3 … +1.5 %p (원장) | §4-1 주기 · T4 |
| O1 (관찰) | 띠 값 · 이름의 출처 = 격자 유산 — 0.13 / 0.26 µm 근거 = 도움말 *"≈ DEM elastic ~0.13µm"* 뿐 (`scripts/mpm_webapp_payload.py` 1350–1354 행) · 비슷한 0.14 µm = real_14 384 격자 한 칸 (CLAUDE.md "SE-DUMP scaffold" 절 · real_14 dx 141 nm) · 16 / 49 % 는 band 0 / 0.14 를 지정한 결과 (`AREA-08`) · 키 `hertz` · `tabor` 가 DEM Hertz · Tabor 면적 피복 (DM1 · DM2) 과 이름 충돌 | 50kg h_MPM = 54.3478 / 252 = 0.2157 µm (metrics `um_box_um` · `n_grid`) → 띠 = 0.60 h · 1.21 h [우리 산술] — 침대마다 띠의 격자 뜻이 바뀐다 | Q1 · Q8 |
| O2 (코드 읽기) | 분모 차이 — MP1 · MP2 = AM 구면 전체 · DM2 = AM–AM 가림 뺀 자유 표면 | 크기 미측정 (50kg CN AM–AM 4.60 / 4.48 / 3.66 · `values_D123.csv`) | Q2 · T10 |
| O3 (코드 읽기) | MP2 의 SE 반경 = 첫 행 하나 + "가장 가까운 **중심**" — 다분산 SE 에서 표면 거리 틀림 | 50kg = 단분산 대리 입도 (`docs/50kg/report_y4/README.md` 87 행) → 50kg 무영향 · 다분산 침대 크기 미측정 | T3 |
| O4 (코드 읽기) | ID1 번호 태그 = 반경 없는 Voronoi + 비주기 KD-tree (래스터는 x,y wrap) → seam 셀 번호 오배정 가능 | 시험 전 · 50kg 영향 없음 (번호 안 켬) | Q4 · Q5 · T4 · T6 |
| O5 (관찰) | 주기 처리 사슬 불일치 — MPM 압밀 `xy=periodic` ↔ STEP3 manifest `periodic_xy` False (50kg 세 킷 · 묶음 tgz) ↔ MP1 · MP2 비주기 ↔ DM2 최소 영상 · STEP3 `_ball` 은 상자에서 자름 (v2 §3-6 `seam_unrepresented`) | seam 계면 · 반응면 크기 미측정 | Q3 |
| `WEB-10` (P3 open) + 같은 부류 | 없는 상을 측정된 0 으로 — 50kg payload `coverage_AM_P_hertz_pct` 0.0 ↔ 강체 짝 None · payload 요약 줄 = AM_P 고정 (`scripts/mpm_webapp_payload.py` 3955 행 · 50kg 로그 "AM_P plastic 0/0%") | 단일 AM = AM_S 자리 침대 전부 | Q8 · T14 |
| G1 (격자 한계) | SE 접촉이 격자 면보다 작다 | 1 µm 접촉 하나 0.093 µm² (Hertz · 접촉 부류 표기 없음 [미확인] · kg50 README §4) ↔ STEP3 면 0.16 µm² (vox 0.4) → a_eq/h 0.43 · MPM 격자 0.80 / AM–SE 0.211 µm² → 0.65 · 1.20 [우리 산술] | Q6 · T7 · T9 |
| G2 (면적 계단) | 면 수 × h² 는 곡면 · 기운 면에서 과대 (L1 = \|n_x\| + \|n_y\| + \|n_z\| 배 · 구면 평균 ~1.5) — 비율은 상쇄 · **막 r·A 절대 면적은 상쇄 안 됨** | `am_surface_patches` docstring · v2 §3-9 S3 (L1 ↔ 축별 = D11 미정) | Q6 · T7 |
| G3 (옛 실패) | VX4 Voronoi 패싯 과대를 되풀이할 위험 | σ 가 접촉 저항 뺀 값보다도 높게 (kg50 README §4 · VX4 docstring) | T8 |

## 4. 공통 정의 제안 (Rint ↔ MPM)

### 4-1. 정의 묶음

| 항목 | 정의 | Rint ② v0 에서 | MPM 피복 · SE–SE 트랙에서 |
|---|---|---|---|
| 정체성 | AM = scaffold 행 canonical id (중심 사전순 · ①′ I8′) · SE = DEM atom id (se_scaffold 행 · atom dump 승계) · 탄소 = (fid, branch) · **세 이름공간 분리** (v2 §3-1 owner 표) | AM pid · fid · SE 번호 없음 | SE 번호 켬 · 끄면 v0 비트 같음 |
| 소유 (셀 → 입자) | power p = \|x − c\|² − r² 최소 · 청구자 = 그 셀 중심을 포함하는 구 (`_ball_cells` 와 같은 식) · ε 띠 = 집합 규칙 (v3.1 I8′) · 변형 뒤 = 셀 안 점의 운반 번호 다수결 (v2 §3-9 S2) · 동률 = canonical 키 (행 번호 아님) | ①′ 그대로 | SE 에 같은 함수 (이름공간만 일반화 · 새 함수 금지 · 규율 ①) |
| 측정 격자 | MPM 계산 격자 h_MPM · SE 셀 = 점 수 × (h/2)³ / h³ = n/8 ≥ ½ (씨앗 점 부피 `spc³` · `scripts/mpm3d_compaction.py` 2311 · 2368 행 · SE 거의 비압축 가정 · 로그 K_SE 25.5 GPa) | 풀이 격자 = STEP3 vox (0.15 · 0.125) | 측정 = h_MPM · 풀이 = STEP3 vox · 옮김 = ①′ 총량 정규화 |
| 면 집합 | F_XY(i, j) = 주인 i (X) · j (Y) 인 이웃 셀 쌍의 면 · 키 = (축, 아래 셀 번호) (①′ 면 키) | VV 접합 · AM–AM 만 | AM\|SE (피복 · STEP4) · SE(i)\|SE(j) (이온 계면) |
| 면적 | A_raw = \|F\|·h² · A_n = 법선 보정 (L1 또는 축별 · D11) · 해상 = a_eq/h ≥ k (k = 시험 뒤 봉인) · 미해상 = ①′ 총량 정규화 (A_true / r 를 지지 면에 고르게 · v2 §3-4) | ①′ 미해상 꼴만 | 둘 다 · 부류 = ①′ 어휘 (contact · ambiguous · gap_bridged · unregistered · unrealized · seam_unrepresented) 재사용 |
| A_true 원천 | 씨앗 = 렌즈 원판 `scripts/lens_geometry.py` `intersection_disc_area` (= c_cpl[22]) · 변형 뒤 = MPM 측정 A_n (v2 §3-9 S4: DEM 변형 전 면적을 섞지 않는다) | DEM 덤프 · scaffold | 씨앗 대조 = 원판 · 끝 = MPM |
| 피복 C(b) | AM **자유 표면** (AM–AM 가림 · 영역 밖 뺌 = DM2 분모) 중 SE 물질까지 거리 ≤ b 인 비율 · b = 0 = **주 값** (닿음 · DM1 · DM2 와 같은 뜻) · b > 0 = 근접 띠 (보조 · 키 `near_b<µm>` 꼴 · 이름 = 구현) · 문헌 2D 단면 피복과는 다른 양 (나란히 적을 때 한정어) | — | 추정기 둘 = 면 걷기 (측정 격자 · 주) · 점 구름 KD (r_pt · 대조) |
| 기준 셋 (늘 같이) | C_강체(b) (구 해석 · 같은 분모) · C_씨앗(b) (같은 함수 · 씨앗 결정적 재생성) · C_끝(b) → **소성 증가 = C_끝 − C_씨앗** (`MPMC-02`) · 이산화 치우침 = C_씨앗 − C_강체 (보고) · 계면 면적도 같은 셋 (ΔA_ij) | — | 모든 MPM 유래 피복 · 면적 |
| 주기 | 측정 (피복 · 계면 census · SE 번호 태그) = x,y 최소 영상 · z 는 감지 않음 · STEP3 풀이 = v0 대로 비주기 → seam 을 건너는 계면 = `seam_unrepresented` 수 · 면적 따로 | 주기 정량 = 거부 (그대로) | 측정만 바뀜 · 풀이 그대로 |
| 막 · 개구율 합성 | 한 면에 RT1 α 와 SE–SE 막 r 이 같이 오면 g = α·g0·R_half/(R_half + r′) (곱 · 순서 무관 · 반셀 · 막이 같은 열린 면적으로 나뉘어 막 배율은 α 와 무관) · 단 **미해상 총량 정규화 면에는 α 를 걸지 않고 거부** (A_true 측정이 PTFE 를 이미 봤을 수 있음 = 이중 계상 · 첨가제 침대 = 이 트랙 첫 단계 밖) | α 만 (r 없음) | r 를 켜도 α 경로 비트 그대로 |
| 탄소 덮임 | 탄소 셀이 SE 계면 자리를 덮으면 그 면 = `unrealized` (①′ `remove_area` 규칙 · 수 · 면적 기록) | 해당 없음 | 50kg = 첨가제 없음 → 0 이어야 |
| 세대 | SE 번호 · 막을 켠 산출 = 새 세대 표지 (v0 `p3ca-` 와 섞지 않음 · 이름 = 구현) · 끄면 매니페스트 (코드 지문 칸 뺌) 비트 같음 | `p2-` · `p3ca-` | 새 접두 |

### 4-2. Rint ② 면 · 접합 → 공통 정의 위 자리 (v0 에서 바뀌는 것 = 없음)

| Rint ② 항목 | 공통 정의 위 자리 | 다음 트랙에서 |
|---|---|---|
| RT1 S1 face α (설계 §3) | 면 집합 위 면 배율 · 이온 = SE\|SE 면 **전체** (입자 안 + 입자 사이) | 입자 사이 면에만 막 곱 (§4-1 합성) · α 정의 · K · 지름 법칙 그대로 |
| RT2 S2 VV 접합 · S3 c (설계 §4 · §5) | 탄소 이름공간 (fid, branch) · 포트 dof · SE 와 교차 없음 | 이름공간 충돌 금지 (SE 번호 격자 = 따로 · AM pid 재사용 안 함) |
| VX3 ①′ AM–AM (v2 · v3 · v3.1) | 소유 · 면 키 · 총량 정규화 · A_true · 부류 어휘 | SE–SE 가 그대로 빌림 (v3.1 §0-2: ③ SE = 별도 진입 조건 → 이 트랙의 Codex 회차) |
| VX2 r1 탐침 `face_rint` | SE 같은 상 거부 (`RINT-01`) | 유지 — SE 막은 원장 경로로만 |
| AM\|SE 면 | 두 채널 전류 0 (v2 §3-2 "솔브에 면 없음") · STEP4 BV 면 = VX1 면 집합 | 피복 C(0) 면 걷기 = **STEP4 와 같은 면 집합** 함수 · STEP4 A_face 도 같은 씨앗 · 강체 대조로 치우침 보고 (STEP4 수치 소급 없음) |

### 4-3. 1저자가 정할 것

| Q | 질문 | 권고 (한 줄) |
|---|---|---|
| Q1 | 피복 주 값 = C(0) (닿음 · DEM 접촉 피복과 같은 뜻) + 씨앗 빼기 · 0.13 / 0.26 = 보조 "근접 띠" 로 개명 (`hertz` · `tabor` 이름 폐기) — `MPMC-01` 고침 방향 *"간격 ≤ 격자 한 칸"* 을 이 꼴로 다듬음 | **예** — 한 칸 띠는 h 에 묶여 침대마다 뜻이 바뀐다 (O1) · 한 칸 띠 값은 보조로 h 와 함께 싣는다 |
| Q2 | 피복 분모 = DM2 와 같은 자유 표면 (AM–AM 가림 · 영역 밖 뺌) | **예** — DEM 과 같은 뜻의 마지막 조건 (O2) |
| Q3 | 주기 = 측정 x,y 최소 영상 · STEP3 풀이는 v0 대로 비주기 · seam 계면 따로 셈 | **예** — 주기 정량 풀이 = 별도 등록 (v0 거부 유지) |
| Q4 | SE 소유 = power diagram (①′ 와 같은 함수 · I8′) · 변형 뒤 = 점 다수결 | **예** — 50kg 단분산이면 Voronoi 와 같은 결과 (T6) · 다분산만 갈림 |
| Q5 | 씨앗 · SE 번호 경로: (가) 측정 모듈이 씨앗 래스터 재구현 + 대조 시험 (런 로그 셀 수 · 작은 침대 mpm3d 출력 비트) · `mpm3d_compaction.py` 안 고침 / (나) FAM 봉인 처리 뒤 mpm3d 씨앗 단계 함수화 · import / (다) MPM 재실행 `--save-se-id` (Voronoi 그대로) | **(가) 지금 · (나) 봉인 뒤 정리** — mpm3d = FAM 봉인 대상 표기 (`WEB-10` note · CLAUDE.md τ 절) · (다) 는 규칙을 못 바꾸고 kgy GPU 를 쓴다 |
| Q6 | 측정 격자 = h_MPM (n/8 ≥ ½) · STEP3 로 ①′ 총량 정규화 이전 · 해상 경계 k · 법선 법칙 (D11) = T6 · T7 사다리 뒤 결과 전 봉인 | **예** — 그 전에는 census 만 (솔브 없음) |
| Q7 | SE–SE 막 솔브 · r 값 = ④ (입력 σ 내부값 규약 · σ₀ 1.5 정합 · 카드) 뒤 · 첫 산출 = 기하 원장 (census · C 셋 · ΔA) | **예** — v2 §3-9 S5 이중계상 경고 그대로 |
| Q8 | 웹앱 · 키 = 새 키 + 옛 키 읽기 호환 표지 · 없는 상 None · 요약 줄 상별 (`WEB-10` 결정 묶음 — 214 발사 10-30 끝) | **예** — J20-l 같은 묶음 (케이스 · MPM lab · 뷰어 패치 · 툴팁) |

## 5. 검증 계획 (시험 먼저 · 옛 코드 실패 확인 → 구현)

### 5-1. 보장마다 작은 해석 반례 (CLAUDE.md 사전 공격 ③)

| ID | 보장 | 반례 · 손 풀이 | 옛 코드 기대 |
|---|---|---|---|
| T1 | C_강체(0) = AM 쪽 렌즈 cap 넓이 / 자유 표면 | AM R · SE r · 중심 거리 d 한 쌍 → cap 높이 h_c = (r² − (d − R)²)/(2d) · 넓이 2πR h_c (손 풀이) · cap ↔ 원판 사상 따로 기록 (a = 0.8 r 에서 1.25 · `AREA-08`) | 단일 반경이면 통과 (해석) · 판별은 T3 |
| T2 | 씨앗 치우침 → 0 (h → 0) | 같은 쌍을 씨앗 래스터로 h 사다리 (상자 1/64 · 1/128 · 1/256) · 간격 0 < g < h 쌍 = 씨앗 거짓 닿음 (C_강체(0) = 0 인데 > 0) 이 h < g 에서 사라짐 | MP1 = 치우침 크기 기록 (실패가 아니라 측정) |
| T3 | 표면 거리 = 최소 (다분산) | SE 반경 1.0 · 0.3 둘 — 작은 구 중심이 더 가깝고 큰 구 표면이 더 가까운 표본점 | MP2 실패 (첫 행 반경 · 가장 가까운 중심) — 먼저 확인 |
| T4 | 주기 이동 불변 | 침대 전체를 x 로 L/2 이동 (wrap) · seam 을 걸친 접촉 한 쌍 → C(b) · census · SE 번호 같음 | MP1 · MP2 · ID1 실패 (`MPMC-03` · O4 재현) |
| T5 | z 는 감지 않음 | 바닥에 닿은 AM + 천장 근처 SE → 피복 0 | z wrap 변이 = 실패해야 (판별력) |
| T6 | power ↔ Voronoi | 반경 1.0 · 0.5 겹친 두 SE → 경계 = 근축면 x = (d² + r₁² − r₂²)/(2d) · 법선 보정 면적 → π a² · 같은 반경이면 둘이 같음 | ID1 (Voronoi) = r₁ ≠ r₂ 에서 다른 면 · 단분산 = 같음 확인 |
| T7 | 계단 보정 | 같은 반경 두 구 겹침 · 접촉 법선 (1,0,0) · (1,1,0) · (1,1,1) → \|F\|·h² → π a²·L1 (1 · √2 · √3) · A_n → π a² | 면 수 × h² = (1,1,1) 에서 √3 배 과대 |
| T8 | 공극 넘는 거짓 계면 없음 | 간격 ≥ 2h 두 SE → 계면 0 | VX4 (closing + 중심 Voronoi) = 면 > 0 — 실패 먼저 확인 |
| T9 | 미해상 총량 | a < h 접촉 · 지지 면 N ≥ 1 → Σ g_film = A_true / r 정확 · 지지 0 = `unrealized` (조용한 0 아님) | ①′ 시험 재사용 · SE 이름공간판 |
| T10 | 끄면 같다 | SE 번호 끔 (또는 r = 0 · 절단 없음) → σ · φ · n_dof · 매니페스트 (코드 지문 칸 뺌) 비트 같음 · α 만 켠 v0 경로와도 | — |
| T11 | Rayleigh · 합성 | r 증가 → σ 비증가 (같은 그래프 · BC) · α·막 곱 순서 무관 (비트) · 미해상 면 + α = 거부 | — |
| T12 | 무변형 = 0 | 무변형 끝 상태 (= 씨앗) → C_끝 = C_씨앗 · ΔA = 0 비트 | — |
| T13 | 번호 다시 붙이기 가드 (Q5 가) | 재생성 씨앗 ↔ 저장 끝 점: 개수 (셀 × 8 = n_pts) · 점별 변위 상한 · 무작위 순열 대조는 반드시 실패 | 셀 수 대조값 = 런 로그 (1 µm 8,343,155 × 8 = 66,745,240 · 세 킷 모두 맞음 [우리 산술]) |
| T14 | 없는 상 = None | AM_P 없는 침대 → 키 None · 요약 줄 상별 | MP1 · MP3 = 0.0 (`WEB-10`) |

- 변이 시험: 분모에서 가림 빼기 끔 · 최소 영상 끔 · power → Voronoi · 법선 보정 끔 · 씨앗 빼기 끔 — 각각 T1–T14 중 하나 이상이 실패해야 (판별력).

### 5-2. 격자 수렴 (보고 · 합격선 = 결과 전 봉인 · D12-V 꼴)

- 측정 격자 사다리 = h_MPM 에서 점 간격 (h_MPM / 2) 까지만 (더 고우면 점 구름이 성겨진다) · STEP3 vox 0.4 → 0.3 한 단계 (면 걷기 · 옮긴 막) · MPM n_grid 사다리 = GPU 예산 있을 때만 (이번 계획 밖).
- 관측 차수 · 씨앗 치우침 C_씨앗 − C_강체 의 h 의존 · a_eq/h 분포 (부류별 수) 를 같이 싣는다.

### 5-3. 실침대 첫 대상 — 50kg D1–D3 (단분산 · 첨가제 없음)

1. 씨앗 (DEM 끝 SE 중심 · CPU · 결정적 재생성): C_강체 (0 · 띠) · C_씨앗 · SE–SE census (쌍 수 · A_n · a_eq/h · 부류) ↔ DEM (CN SE–SE 3.34 / 4.04 / 4.98 · `values_D123.csv` · 렌즈 원판).  **결과 전 등록**: C_강체(0) ↔ 덱 'Hertz' 19.1 / 21.1 / 19.0 % 의 허용폭 (cap ↔ 원판 차이 · `AREA-08` · 덱 값의 함수 = [미확인] → 먼저 확인).
2. 끝 상태 (kgy 저장 끝 점 + T13 가드 · 저장 파일 종류 [미확인]) → C_끝 · ΔC · ΔA_ij.
3. STEP3 막 솔브 = Q7 (④ 뒤) · 등록 먼저.

## 6. 일정

| 시점 | 할 것 | 기계 |
|---|---|---|
| 지금 (11-03) | 이 메모 (문서만) | — |
| Rint 회차 ② 요청서 발송 뒤 · 1저자 지시 때 | §4-3 Q 답 → T1–T14 합성 시험 (시험 먼저 · 게이트 · 커밋 하나씩 push) → 50kg 씨앗 census | CPU (컨테이너 · kgy CPU) |
| R 런 창 11-22 – 29 (메인 지시 · 리포 기록 [미확인]) | kgy · gabia GPU 를 쓰지 않는다 — CPU census · 문서 · 웹앱만 · R 시간 추정 = 두 대 나눔 110.1–159.4 h · 안 나눔 196.8–290.5 h (`docs/reviews/rint2_rr_fix_evidence_20261023/q9_time_budget.json` · 추정) | — |
| GPU 가 필요해지면 (Q5 다) | MPM 재실행 ≈ 29–31 분 × 3 (50kg 런 16:17 → 16:48 · 17:17 · 17:46 KST · kg50 README [우리 산술]) — R 런 전 빈 시간 또는 다른 기계 | kgy · 1저자 |
| 끝 상태 · ΔC · ΔA 뒤 | 사전 공격 리뷰 (CLAUDE.md ①–④) → Codex 한 회차 (이온 계면 트랙 설계 + 시험 결과 · v3.1 §0-2 ③ 진입 조건) | — |

- 순서 = 50kg → Rint (1저자 10-27) 그대로 · 이 트랙은 Rint 회차 ② 다음 (인계 §2-1-4 ⑤) · 단계마다 1저자 지시 뒤 · 웹앱 = 같은 묶음 (J20-l).

## 7. 남는 것 · [미확인]

- 1 µm 접촉 0.093 µm² 의 접촉 부류 (SE–SE 문맥 · 표기 없음) · 덱 5장 'Hertz' 19.1 / 21.1 / 19.0 % 를 낸 함수 (DM1 합 ↔ 합집합) · kgy 저장 끝 점 파일의 종류 · 메모리 (6,674 만 점 KD-tree) · R 런 창 날짜의 리포 기록.
- STEP3 vox 0.4 면 걷기 (VX1) 의 50kg 평균값 — 입자별 벡터는 원 payload 에만 (slim 에서 빠짐).
- 띠 0.13 µm 의 원 근거 (*"≈ DEM elastic"*) — 출처 없음 · 이 메모는 보조 지표로만 남긴다.
- AM–SE 피복과 문헌 단면 피복 (Lee 2025 Joule 94.8 vs 83.1 % = 리뷰의 2차 인용 · 원문 미확인 · 덱 README) 의 대조 규약 — 2D 단면 · 해상도 띠를 맞춘 뒤에만 나란히.
- 50kg MPM 은 DEM 끝 좌표에서 출발 → MPM 피복 · 면적의 DEM 일치는 독립 근거가 아니다 (kg50 README §1) · 소성 증가분 ΔC · ΔA 만 MPM 고유 정보 후보.
