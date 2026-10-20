# 첨가제 물리 표현 — 현황 · 빠진 물리 · 구현 순서 (PTFE · VGCF · Super P · SDCP)

> 에이전트 초안 (2026-10-20 · 읽기 전용 조사) · 1저자 확인 · 결정 질문 비준 전 · 원문 확인 전 숫자는 [미확인] 표지 그대로 · 범위 결정 = 1저자 10-20 (PTFE 실제 부피 · 막 + SDCP 계면 + 맨 접점 R_c 보정).

> 2026-10-20 · 읽기 전용 조사 (코드 · 원장 변경 0 · 런 0) · 코드 기준 = 작업트리 `1fe3e0a29` · 문헌 = 정본 litdb 카드
> (`origin/claude/friendly-meitner-lldvar` @ `58dd54f`, `git show` 로 원문 줄을 확인한 것만 — 부록 A) · 그 밖의 값 = [미확인] ·
> 우리 산술 = [산술] · 추정 = (추정).  ⚠ 제출본 (10-20) 수치에는 소급하지 않는다 — 다음 세대 계획이다.

## 0. 요지 (왜 지금)

- 첨가제는 **DEM 에 없다** — 생산 압축 덱은 AM_P · AM_S · SE 세 종류뿐이고 (`dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts:107-113`),
  DEM 접촉망 전자 풀이도 AM–AM 만 푼다 (`scripts/network_conductivity.py:13`).  첨가제는 **MPM 압밀 때 동결 AM 골격의 빈 곳에 재료점으로 시딩**되고
  (`scripts/mpm3d_compaction.py:2513-2790`), **STEP3 0.15 µm 복셀에 상 σ 하나**로 찍힌다.  면은 조화평균뿐 = **접촉 저항 0** (`CL-81`).
- 그래서 지금 "첨가제를 넣은 효과" 는 ⓐ 도체 · 절연 셀의 **부피 · 위상** ⓑ **상 σ 한 숫자** 두 통로로만 나온다.  실제 첨가제 물리의 핵심
  (PTFE 의 접점 피복 · 탄소 접합 저항 · SDCP 의 접점 다리) 은 **접점에서** 일어나는데, 모델에는 그 자리가 없다.
- 신호 셋 (전부 리포 원장):
  1. SDCP 최종 16 팔 — SBE 를 DC 1.63 에 맞춘 뒤 DBE 1.8877 · 비 **1.1646** ↔ 실험 **2.86** (`docs/reviews/sdcp_sigma_e_dcp_anchor_registration_v2_20261019.md` §7 10-20 09:49).
  2. 그 보정값 σ*_VGCF **0.347 S/cm** = 융합 섬유 규약 78.54 의 **1/226** [산술] — 접점 · 피복 물리가 스칼라 하나에 다 들어갔고, DBE 는 **다른 스칼라**가
     필요하다 (S1b 진행 중 · 결과 전 어림 σ*_DBE ≈ 2.4–2.5 S/cm · 같은 문서 §7 10-20 09:41).
  3. PTFE 투여 반응 — 모델 σ_e(PTFE 1)/σ_e(PTFE 0.5) **0.840** (`docs/reviews/lee_abs_sigma_e_prereg_20260923.md` §5) ↔ Lee 2025 곡선 로그보간 0.44 ·
     Lee 2026 실측 0.70 (조성 다름) ⇒ 모델의 PTFE 로그 감도 = 문헌의 **21–49 %** [산술: ln 0.840 / ln 0.44 · ln 0.840 / ln 0.70].
- SDCP 쪽 부피 손잡이는 넷 다 효과가 작다: 이득의 주 원천 = 새 도체 부피 (`CL-44`) · 크기 0.3 → 1 µm 재압밀 a0 −2.2 % (등록 v2 §7 · 표현 부피도 같이 바뀌었을 수 있음 — P6) · σ_SDCP ×100 → 이득 +3.5 %
  (`CL-70`) · 접촉 검출 브리지가 줄인 격자 의존 = 19.7 % (`docs/reviews/a_track_verdict_20260829.md` §1).  ⇒ **빠진 손잡이는 부피가 아니라 접점이다** (해석 · 검정 아님).
- 권고 순서: **S1 PTFE 면 개구율 연산자** (Codex R18 Q6) → **S2 탄소 접합 R_j** (Rint ②) → **S3 SDCP 접점 수정자** (S2 위) → S4 Super P → S5 역학.
  공통 규칙 = 기본 끔 · 비트 동일 · 시험 먼저 · 결과 전 등록 · **SBE/DBE DC 는 holdout** · 메커니즘별 소산 몫을 같이 보고 (= "보이게" 의 계량).

## 1. 첨가제별 현황

| 첨가제 | 침대 (DEM · MPM) | 역학 물성 · 출처 | STEP3 전도 표현 (sid · σ · 스탬프) | 물리적으로 빠진 것 | 원장 | 근거 (file:line) |
|---|---|---|---|---|---|---|
| **PTFE** | DEM 없음 · MPM 정부피 인발 섬유 (d_i ∝ √(V_i/L_i)) — 곡률 0.40 · 부피 CV 0.6 · 탄소/AM 핵생성 0.6 · 그중 AM 몫 0.5 (§F1 hook) · 가지 0.5×fibril · 다리 0.5 · `PTFE_D 0.25` 는 **개체 수만** 정하고 실제 d_i 는 77 배 분포 · `PTFE_L 40` 무앵커 · 상자 밖 점 삭제 (주기 wrap 아님 · 길이 −10.3 %) · 처방 부피 고정 | E 1.80 GPa · ν 0.30 · σ_y 0.05 = 사용자 지정 08-18 (근거 미기재 — 비교: 원고 AFM 판독 5.6 · Lee 2025 SI Fig 10 DMA ≈150 MPa @30 °C) · 결속 = `coh_ptfe` 0.10 × binder_cap(w; 1.5) → SBE 0.093 · DBE 0.065 GPa [산술] · **압축 (J<1) 때만 등방 인력** — 인장 망 · 접착 없음 | phase 4 → sid 7 · 생산 `centerline` = 1-셀 중심선 exact-zero DOF (σ_e = σ_ion = 0 · 열 0.25 W/mK 인용 없음) · 루프 우선순위로 **탄소 · SDCP 셀을 덮어 자른다** · 표현 부피 **0.40–0.43×** · `capsule` = 예약값 · 거부 · `ptfe_block_um` = SE 셀만 sid 9 (생산 0) | 접점 · 표면 피복 (탄소–탄소 · 탄소–AM · AM–AM · SE 면) · 참 부피 (×0.4) · 직경 · 두 계층 (fibre 0.048 / rope 0.248 µm) · 인장 결속 · 저투여 구조 효과 (Lee 2026: 0.2 wt% 에서 σ_e ×2) · '자르기' 인공물 | CL-42 · CL-49 · CL-60 · CL-66 · CL-67 · CDXR2-2 · PASL-01 · Codex R18 (A·B DROP · Q6 이관) | `additives.py:96,758-901,844` · `mpm3d_compaction.py:31-42,159,800,1909-1911,2515,2565-2595,2692,2698,2958-2960` · `mpm_webapp_payload.py:780,852-870,1474-1492,1913-1915` · `step3_sigma.py:771,811-869,2366` · 러너 `sdcp_gain_vox015_8arm.sh:245-251` |
| **VGCF** | DEM 없음 · MPM 곧은 막대 Ø0.15 · L 10 (Ø 고정) · 생산 침대 = `--fibre-buckle` (Winkler λ **처방**) + `--fibre-align 0.606` (affine) + `--dilate-z 1.0719` (지지 = **처방 팽창**) · 점은 독립 재료점 (`--fibre-rod` 때만 연결 · 그때도 섬유는 압축을 거의 안 받음) · `--fibre-stiff` (강체 지지 상한) 생산 미사용 · 상자 밖 잘림 길이 −10.5 % (`CL-67`) | E 100 GPa (Lawrence 2008 · Endo 2001 Fig 6) · ν 0.30 · σ_y 2.0 근거 미기재 · SBE/DBE 침대는 옛 세대 10 GPa (override) · σ_e 가 E 에 반응하는 길 = 압밀 기하뿐 (1–100 GPa: σ_e ≤ 0.25 %) | phase 2 → sid 3 · 선분 스탬프 (Amanatides–Woo · 6-면 · AM 간극에서 끊음) · σ = 100·πd²/(4·vox²) = 78.54 @0.15 또는 덮어쓰기 (최종 16 팔 σ* 0.347) · 표현 부피 **1.91×** @0.15 · 이온 0 · 융합 면 = 접합 저항 0 | 섬유–섬유 · 섬유–AM **접합 저항** (같은 sid 면은 ① rint 불가 — pid = AM 만) · 1-셀 관 = 부피 과대 · 가짜 상호연결 · σ 재척도가 vox 의 함수 · 지지 강성 = 처방 (DEM 영역) | CL-47 (+정정 10-03) · CL-48 · CL-60 · CL-88 · CL-93 · R20-04 · R20-05 · DR3-05 · DR3-06 · SELF-13 · RINT-08 · RINT-10 | `additives.py:94` · `mpm3d_compaction.py:155-161,739,750,766,843,2481,2513` · `step3_sigma.py:121-133,175,647,892-966,2479-2537` · 러너 `:636-655` · `docs/fibre_rod_mpm_design.md:98-115` · `docs/reviews/deep_review_20260818_rve.md:91-96` |
| **Super P** | DEM 없음 · MPM 처방 n = 0.2 µm 응집체 수 → k=3 응집체 무작위 걸음 사슬 (걸음 0.7·dx_MPM = **격자에 묶임**) · AM 표면 몫 0.70 (ballmill) · handmix k 8 · 0.30 · 덩어리 4 · thinky → `coat_block` 막 (껍질 0.20 µm) · `SP_AGG 0.18` 은 안 쓰이는 상수 | E 0.50 · ν 0.30 · σ_y 0.10 근거 미기재 · ρ 1.90 ↔ Kim 2024 Super C 겉보기 0.67 g/cm³ (부피 2.8 배 차 [산술] · 같은 양인지 (추정)) | phase 3 → sid 4 · σ 10 S/cm (*frozen uncalibrated* hook) · ballmill 사슬 = 경로 → 선분 스탬프 (`*_kind.npy` 있을 때) · thinky = 그룹 → 점 스탬프 · 직경 재척도 없음 · 이온 0 | 1차 (40 nm) → 응집체 → µm 덩어리 계층 · 응집체 간 접촉 저항 · 퍼콜 문턱 재현 미검증 · 표현 부피 원장 없음 · coat_block 막의 σ 붕괴를 STEP3 가 따로 표현 안 함 · ⚠ 현 생산 조성 (SBE/DBE · Phase A · Lee) 에 없음 = 현 결과 영향 0 | SELF-13 · AUD-02 · AUD-03 · backlog A4 · F1 | `additives.py:28,95,274-292,915,934-939,1030-1076,1046` · `mpm3d_compaction.py:158,2514,2652-2671` · `step3_sigma.py:29-46,94,873-929` |
| **SDCP** | DEM 없음 · MPM Ø0.30 낱알 · AM 부착 0.5 (§F1 · 껍질 d/2) + 공극 · handmix 덩어리 3.0 · 새 DBE 침대 `--sdcp-agg-d 1.0` (덩어리당 24 · 채움 0.64 가정) · 실현 부착 몫 `realized_anchor_frac` (새 침대 ⬜ 미열람) | E 9.00 · ν 0.35 · σ_y 1.00 (rigid proxy §F1) · ρ 1.30 PROXY · `coh_sdcp` 0.10 (압축 인력 · wt% 무관) · AM 계면 γ = 무효 (wrong monomer · 재계산 대기) | phase 5 → sid 5 · σ_e 256.6 (최종 16 팔 · 기본 250 · 문헌 앵커 없음) · σ_ion 2.48e-4 (등록 v2 §3-D) · 구 스탬프 Ø0.30 (d/vox ≥ 2 게이트 · **점마다 고정 지름** — MPM 점당 부피 재분배를 안 따른다) · 표현 부피 0.986× (08-12 낱알 침대 · `CL-25`) — 08-27 · 10-19 침대 미측정 (시딩 생존 옛 DBE 0.90 · 새 1 µm 0.75 [산술] + 덩어리 안 겹침만큼 줄 수 있다 (추정)) · VGCF/SuperP/AM 셀을 **덮어 σ 상향** · PTFE/SWCNT 에 덮임 · 접촉 브리지 노브 (진단 · 생산 0) · 열 k = k_SE 가정 | **nm 접점 막** (SEM 에 안 보임 · 등록 v2 §4) → 접점 전도 향상 = **접촉 저항 없는 모델에선 원리적으로 0** · 바인더 결속 · AM/탄소 부착 에너지 · 집전체 접촉 (DC 2-전극 R 에 들어 있음) | CL-25 · CL-33 · CL-43 · CL-44 · CL-56 · CL-61 · CL-70 · CL-81 · SELF-11 · A 트랙 h0 · 등록 v2 §4 | `additives.py:28,100-114,619-756` · `mpm3d_compaction.py:160,807,832,2516,2596-2617,2703-2708` · `step3_sigma.py:94,121-133,661-761,771,792,2370-2389` · `mpm_webapp_payload.py:1324` |

공통 (표 밖 · 전 첨가제):
- STEP3 찍는 순서 = SE 먼저 (최저 우선) → AM 구 → AM 브리지 (SDCP 캠페인 0.48 · Phase A 0.24 µm) → 첨가제 루프 **VGCF < SuperP < SDCP < PTFE < SWCNT** (뒤가 이긴다 · 탄소는 AM 도 덮는다)
  (`step3_sigma.py:582-590,630-631,771`).  교차점의 물리를 **루프 순서**가 정한다 — PTFE 는 탄소를 자르고, SDCP 는 탄소를 σ 740 배로 올린다 (σ* 0.347 기준 [산술]).
- ① 계면 저항 기구 = 다른 sid 면 + 같은 sid 는 AM 만 (pid) · 기본 끔 · 값 인용 단계 아님 (`step3_sigma.py:175,203-363` · `mpm_webapp_payload.py:1205-1215` ·
  `docs/voxel_contact_free_gap.md` §8) · ①′ AM–AM 막 = 정량 채택 · 생산 HOLD (`step3_sigma.py:969-1006`) · 소산 분담에 계면 버킷 있음 (`step3_sigma.py:168,2212-2354`).
- 표현 부피 (0.15 µm): VGCF **1.91×** · SDCP 구 **0.986×** (08-12 침대 · 최근 침대 미측정 — P6) · PTFE **0.40–0.43×** · Super P 미측정 ⇒ 결속재가 많은 SBE 쪽이 더 과소 표현된다 (방향 서술).
- 실험 두께 SBE 90 · DBE 80 µm (등록 v2 §1) ↔ 모델 두 침대 정지 두께 **72.53 µm 같음** (`docs/reviews/table_s3_data_20260827.md` §1 · 등록 v2 §7 R1) — 부하량 [미확인].
- SWCNT (sid 8) 는 이 브리프 범위 밖 — `CL-63` 게이트 그대로.

## 2. 빠진 물리 — 우선순위 순

### P1. PTFE 접점 · 표면 피복 (+ 참 부피 · '자르기' 인공물 분리)
- **왜 (SBE↔DBE)**: SBE PTFE 1.0 · DBE 0.5 wt% — 실험 비 2.86 에 PTFE 몫이 들어 있다 (등록 v2 §4).  모델의 PTFE 투여 감도는 문헌의 21–49 % [산술].
  어림: 투여 반응이 Lee 2025 보간 · Lee 2026 실측 수준이면 비 ≈ 1.1646 × 0.840/0.44 ≈ **2.2** · × 0.840/0.70 ≈ **1.4** (추정 · SDCP 와 곱으로 분리된다는 가정 ·
  `CL-70` 교호작용 있음 · Q 0.840 은 σ_VGCF 78.54 세대 값이고 σ* 0.347 에서는 미측정) — **판정 아님**, 우선순위 근거로만.
- **0.15 µm 표현**: Codex R18 Q6 = 셀을 찍지 말고 **FV 면의 열린 면적분율 α** 를 피브릴 중심선 + 직경 (캡슐) 에서 계산해 `G = α·G0` (`docs/reviews/codex_r18_verdict_20260831.md` §Q6).
  피브릴 (0.048–0.25 µm) 이 vox 보다 얇아도 성립 · 국소 · KCL · 투여 단조 · PTFE 없으면 정확한 no-op.  적용 면 = 전자 (탄소–탄소 · 탄소–AM · AM–AM) /
  이온 (SE–SE · SE–SDCP) **플래그 분리**.  탄소 셀 덮어쓰기를 면 차단으로 바꾸면 '자르기' 인공물이 빠진다.  ⚠ R18 금지선: α 의 직경을 피브릴 물성으로 해석 ·
  펠릿 0.97 에 다시 맞추기 = calibration 이지 validation 아님.
- **앵커**: Lee 2025 Nat Commun SI Fig 5 (CAM:SSE:VGCF 80:17:3 고정 · PTFE 0.5 / 2 / 5 wt% → σ_e 34 / 4.5 / 0.011 · σ_ion 0.069 / 0.024 / 0.007 mS/cm · 75 MPa) ·
  원고 Figure 2 펠릿 (LPSCl:PTFE 9:1 wt · 이온 3.57 → 0.97 = 희석 예측의 0.31 · 전자 0.30 → 0.12 ×10⁻⁷ S/cm — `docs/reviews/sdcp_ion_calib_prereg_20260825.md` §1–2) ·
  Lee 2026 Small Table S2 (1.0/0.5 wt% σ_e 0.70 · 밀도 −4.3 %p 포함 · 조성 85:13:2) · 기하 = Lee 2025 EES (rope Ø0.248 · fibre 0.048 µm · AR ≈ 27 · rope 길이 6.689 µm) ·
  피복 = Hong 2026 (PTFE 건식 CBD 피복 5 → 9 % · 합성 트윈 · 2차 근거) · 직접 측정 후보 = 같은 조성의 FV 면 차단 면적분율 · AM–AM 접점과 PTFE 교차 비율 (R18 Q3).
  ★ Lee 조성 침대 2 (VGCF 3 / PTFE 0.5 · 1) 가 이미 있다 (`lee_abs_sigma_e_prereg_20260923.md` · v100 보존 — 지금 접근 가능 여부 [미확인]).
- **의존**: `CDXR2-2` (직경을 raster 까지 배선 — 지금은 solve 전 로드 · 길이 검사까지만 `mpm_webapp_payload.py:1854-1893`) · `CL-66/67` (L · 직경 분포 결정) · `CL-67` ③ (주기 wrap).

### P2. 탄소 접합 저항 (VGCF–VGCF · VGCF–AM) = Rint ②
- **왜**: SBE 보정 σ* 가 접점 물리 전부를 한 숫자로 삼켰고 DBE 는 다른 숫자가 필요하다 → 두 전극의 차이는 접점에 있다 (해석).  명시 접합이 있어야
  P1 (PTFE 가 접점을 덮음) · P3 (SDCP 가 접점을 이음) 이 **작용할 자리**가 생긴다.  지금 같은 sid 면 (VGCF–VGCF) 은 ① 계면 항도 못 받는다 (`step3_sigma.py:175`).
- **0.15 µm 표현**: 계약 J1–J8 (교차 셀 멤버십 · 접합 instance · 포트 dof · R_j 간선 · 기준면 · 0/∞ 한계 · 단일 원장 · 긴 평행 접촉 거부 —
  `docs/reviews/contact_resistance_pipeline_draft_v2_20261006.md` §3-8).  fid 경로 (중심선) 가 이미 있어 격자와 무관하게 접합을 셀 수 있다.  위상과 값 분리 ("위상 ON · R_j 0" 대조 팔).
- **앵커**: 정본 카드에 R_j 값 **없음** → [미확인] · 간접 = Endo 2001 단섬유 1×10⁻⁴ Ω·cm ↔ 압착 분말 ≈0.012 Ω·cm @0.8 g/cm³ (≈120 배 = 접촉 · 충전 · 배향 손실 ·
  분말값 자체가 밀도에 ≈300 배) → 역산 정합성 검사 (`docs/reviews/sigma_vgcf_anchoring_program_20260829.md` ②) · Reisacher 2023 퍼콜 문턱 재현 (③ 약한 형태) ·
  Lee 2026 (20.83 nm 해상 VGCF + 83 S/cm 로 σ_e 시뮬/실측 0.99 = 접합을 유효 σ 에 묶은 다른 예).
- **상태**: ① 기구 끝 (기본 끔) · ①′ AM–AM 기구 (정량 채택 · 생산 HOLD) · `RIMPR-01/02` 열림 · ② 미착수 (CLAUDE.md Rint 줄 *"수정 계획 = 세미나 뒤 → ②"*).

### P3. SDCP 접점 막 · 다리 = R_j 수정자
- **왜**: SDCP 부피 · 크기 · σ · 접촉 검출 넷 다 효과가 작다 (§0) → DBE 의 실험 이득을 못 만든다.  실제 SDCP 는 전도성 바인더 — 접점을 잇는 nm 막은
  SEM 에 안 보이고 어느 크기로도 표현되지 않는다 (등록 v2 §4).  접촉 저항이 0 인 모델에서 "접점을 좋게 하는" 역할은 **정의상 0** 이다.
- **0.15 µm 표현**: P2 의 접합 instance 마다 SDCP 근접 (구 · 덩어리 표면 거리 ≤ tol) 이면 `R_j → R_j·(1−c)` (+ SDCP 경유 병렬 항) · AM–AM 접점은 ①′ 막 r_type 수정 ·
  셀 스탬프 아님 (nm 막).  SDCP 입자 부피 · 이온 상 (2.48e-4) 은 그대로 둔다.
- **앵커**: 막 두께 · 덮임 몫 [미확인] → **시나리오 두 값** (재료 예측 아님 표지) · 음성 대조 = 원고 펠릿 LPSCl:SDCP 9:1 (전자 0.30 → 1.53 ×10⁻⁷ = 비퍼콜 · 이온 = 희석의 1.02 ·
  `sdcp_ion_calib_prereg_20260825.md` §1–2) — 새 표현이 펠릿 RVE 를 퍼콜시키면 기각 (같은 문서의 규칙 꼴) · SBE (SDCP 0) 는 셀 단위 no-op.
- **의존**: P2 필수 · σ_SDCP 256.6 의 시편 조건 [미확인] (`CL-61` · Methods 한정어).

### P4. Super P 응집체 사슬 전도 · 접촉
- **왜**: SBE/DBE 와 무관 (조성에 없음) — 플랫폼 정확성 문제: 사슬 크기가 MPM dx 에 묶임 (`additives.py:1046`) · σ 10 hook · 표현 부피 미측정 · coat_block 막의 붕괴 물리 없음.
- **0.15 µm 표현**: 응집체 = 0.2 µm 구 사슬 (걸음 = 물리 지름 · 격자 무관) + 응집체 간 접합 (P2 기계 재사용 · `ID_PATH`) 또는 셀 부피분율 유효 매질 · 겉보기 밀도 선택지 (0.67 ↔ 1.90).
- **앵커**: Reisacher 2023 (LPSCl + C65 · p_c ≈ 4 wt% · 3 / 4 / 5 wt% → 1.66×10⁻⁴ / 1.36×10⁻³ / 1.02×10⁻¹ S/cm · AM 없음) = 펠릿 RVE 의 약한 형태 표적 (문턱 · 계단 재현) ·
  Asylbekov 2023 (건식 혼합 CB 분쇄 하한 ≈ 0.2 µm) · Kim 2024 (Super C 0.67 g/cm³ · SE 1.86) · Kim 2025 (SE 코팅층에 Super P → 3.3×10⁻² → 1.0×10⁻⁵ S/cm · VGCF 는 1.4×10⁻² 회복).
- **의존**: P2 · 펠릿 RVE 의 사슬 기하 지원 (지금 `pellet_rve_sigma.py:61-100` 은 구 RSA 뿐).

### P5. 역학 역할 (PTFE 결속 · VGCF 지지 · SDCP 바인더 · 공정 구조 효과)
- **왜**: 실험 두께 90 / 80 µm ↔ 모델 72.53 / 72.53 µm — 결속재 차이로 치밀화가 달라지는 길이 모델에 없다 (부하량 미확인이라 원인 분리 전).
  Lee 2026: PTFE 0.2 wt% 가 LPSCl 을 NCM 위에 코팅 (NCM 표면 LPSCl 몫 35 → 59 %) 해 σ_e ×2 — 공정이 만든 **배치** 효과는 STEP3 연산자로 못 만든다.
- **표현**: 동결 AM MPM 은 AM 재배열 불가 (frame[5]) · PTFE 인장 망 = `--fibre-rod` XPBD 확장 (`mpm3d_compaction.py:739-749`) 또는 DEM 공동 압축 (믹서 덱의 결합 사슬 꼴 ·
  `dem_scripts/mixer_20260919/README.md` 규격표) · VGCF 지지 = `--fibre-stiff` 상한 (`mpm3d_compaction.py:766-774`) · 현행 `--dilate-z` 처방 유지.
- **앵커**: Lee 2025 인장 (SSE 0.049 · 전극 0.441 · co-rolled 0.510 N/cm) · DMA (≈150 → 50 MPa) · Cho 2024 Table S2 (CA 유무 porosity +0.01) · E 민감도 약함 (`CL-93`).
- **의존**: 연구 트랙 · σ_e 에 대한 효과는 작다 (E 1–100 GPa → ≤ 0.25 %) ⇒ **우선순위 낮음** (두께 차의 원인이 확인되면 재평가).

### P6. 표현 회계 — 모든 단계의 바탕 (값은 안 바꾼다)
- 상별 표현 부피 원장에 Super P 추가 · **우선순위로 덮인 셀 수** (PTFE → VGCF/SuperP/SDCP · SDCP → VGCF/AM) · PTFE 가 끊은 VGCF 경로 수 — raster-only (솔브 없음 ·
  기존 원장 틀 `mpm_webapp_payload.py:2009-2060`).
- SDCP 구 스탬프는 살아남은 점마다 Ø0.30 고정 (`step3_sigma.py:661-699`) — MPM 은 떨어진 점의 부피를 생존 점에 다시 싣지만 (`mpm3d_compaction.py:2692` ·
  `additives.py:619-756` docstring), STEP3 표현 부피는 **생존 점 수**를 따른다.  새 1 µm DBE 침대는 시딩 116,532 / 목표 154,452 (옛 DBE 138,988 · 등록 v2 §7 R1 · R2)
  ⇒ 옛 ↔ 새 DBE 의 −2.2 % 는 "크기" 와 "표현 부피" 가 섞였을 수 있다 (추정) → S0 원장에서 두 침대의 SDCP 셀 × vox³ / vol_um3 를 먼저 잰다.
- σ* 0.347 에서 SDCP 가 VGCF 셀을 덮는 σ 상향 채널의 몫 = 미측정 → `--step3-sdcp-yield-to-vgcf` 진단 1 팔 (`CL-43/44` 틀 · LEAN=2) 로 바로 잴 수 있다.
- 메커니즘별 소산 몫 (`phase_current_share` 의 계면 버킷 확장: PTFE 차단 면 · 접합 · SDCP 수정 접합) = "물리가 보이게" 의 계량 · 웹앱 표지 (J20-l).

## 3. 구현 순서 (전부 기본 끔 · 비트 동일 · 시험 먼저)

| 단계 | 내용 | 시험 먼저 (요지) | 노력 (사람·일) | Codex |
|---|---|---|---|---|
| S0 | 표현 원장 확장 (P6) — raster-only · `record` 축 · 옛/새 DBE 침대 SDCP 표현 부피 포함 | 교차 fixture 셋 (PTFE×VGCF · SDCP×VGCF · CB 사슬) 셀 수 손계산 대조 · 기존 팔 비트 동일 | 1–1.5 | 단독 불요 · S1 회차 동봉 |
| S0b | `CDXR2-2` 직경을 raster 입력까지 배선 (소비만 · 스탬프 불변) | 길이 불일치 · 결측 = 거부 · `off` / `centerline` 비트 동일 | 1 | S1 과 같은 회차 |
| S0c | σ 치환 채널 진단 1 팔 (`--step3-sdcp-yield-to-vgcf` @σ*) | 기존 진단 경로 · 새 코드 없음 | 0.5 (+ GPU ≈1 h) | 불요 |
| S1 | PTFE 면 개구율 연산자 (`--ptfe-stamp capsule` 을 Q6 꼴로 실현) · 전자/이온 플래그 분리 · 차단 면적 원장 (면 부류별) | R18 종료조건 8 (α=1/0 극한 · 상호성 · KCL · 회전/반사 · 주기 seam · 고정 기하 격자 조임 · origin 불변 · 투여 단조) + PTFE 없음 no-op + 부피 보존 | 4–6 | ✅ 설계 (런 전) |
| S1r | 등록 문서 (결과 0 건): 보정 1 점 (Lee 2025 한 투여 또는 원고 펠릿) · holdout = 다른 투여 · Lee 2026 · **SBE/DBE DC** · σ* 재보정 절차 포함 | — | 1 | ✅ S1 과 같은 회차 |
| S2 | Rint ② 탄소 접합 (J1–J8 · fid 멤버십 격자 · R_j 간선) — `RIMPR-01/02` 수정 먼저 | v2 등록 시험 T1-6 · T1-7 · T1-8 · T2-3 · "위상 ON · R_j 0" = 축약 그래프와 같음 | 8–12 | ✅ (D9 · 이미 요구) |
| S3 | SDCP 접점 수정자 (P3) | SBE 셀 단위 no-op · c=0 비트 동일 · c 단조 · 펠릿 RVE 비퍼콜 유지 | 3–5 | ✅ |
| S4 | Super P — 물리 걸음 사슬 · 응집체 접합 · 겉보기 밀도 선택지 · 펠릿 RVE (Reisacher 약한 형태) | 사슬 길이 격자 불변 · 표현 원장 · 문턱 재현 판정선 런 전 고정 | 4–6 | 주장에 쓸 때 |
| S5 | 역학 설계 문서 (결속 망 · 지지 · DEM 공동 압축) | — | 설계 2–3 (구현 2–4 주) | ✅ 설계 |
| S6 | 웹앱 표지 — 각 단계와 같은 묶음 (J20-l) | 표지 문구 시험 | 단계당 0.5 | — |

- **σ* 재보정 고리**: S1 (또는 S2) 을 켜면 SBE 손실 일부를 새 물리가 설명하므로 σ* 가 바뀐다 (오를 것 (추정)) → SBE 재보정 뒤 DBE 는 **예측**이 된다.  이 절차를 S1r 에 미리 적는다.
- 생산 규약 (`centerline` · σ* · 브리지 0.48) 은 등록 · 1저자 비준 전까지 그대로 · 결과는 `physics_protocol_id` 새 세대로 갈라 섞지 않는다 (`mpm_webapp_payload.py:780-801`).

## 4. 1저자가 정할 것

- **Q1** 새 첨가제 물리에서 SBE/DBE DC (1.63 · 4.68) 의 지위 — 보정 표적인가 holdout 인가?  → 권고: **holdout** (보정은 Lee 2025 투여곡선 또는 원고 펠릿 한 점) — 그래야 "보이게" 가 예측이 된다.
- **Q2** S1b 의 DBE 전용 σ* 를 어떻게 부르나?  → 권고: 보정값과 함께 **"묶인 접점 배수 σ*_DBE/σ*_SBE"** 로 보고하고, P1–P3 가 설명할 대상으로 등록 (그 값에 다시 맞추지 않음).
- **Q3** 순서 S1 (PTFE 면) → S2 (Rint ②) → S3 (SDCP) 로 가나?  → 권고: 예 — S1 은 ② 와 독립이고, S3 은 ② 없이는 효과가 정의상 0.
- **Q4** PTFE 면 연산자의 직경 — (가) rope Ø0.248 단일 + 부피 보존 길이 (나) 시더 d_i (77 배 분포) (다) 두 집단 0.048/0.248.  → 권고: (가) 주 · (다) 민감도 · (나) 안 씀.
- **Q5** PTFE 차단을 이온 면에도 거나?  → 권고: 예, 단 전자 · 이온 플래그를 따로 등록 (R18 P1-3 의 결합 회피) — 원고 펠릿 (이온 0.31×) · Lee 2025 (둘 다 하락) 이 근거.
- **Q6** centerline 의 '탄소 자르기' (루프 우선순위) 를 고치나?  → 권고: 지금은 S0 원장으로 크기만 재고, 생산 규약 (`CL-60`) 변경은 S1 등록 때 함께 결정.
- **Q7** Super P 를 지금 하나?  → 권고: 아니오 — 현 조성에 없음 · 원장과 사슬 걸음 결함 기록만 · 본 구현은 S2 뒤.
- **Q8** 역학 (결속 망 · DEM 공동 압축) 은?  → 권고: 보류 — 먼저 두 시편 부하량 (mg/cm²) 으로 90 / 80 µm 차이의 원인을 가른다.
- **Q9** DC 2-전극 R 의 접촉 · 벌크 분리 (같은 조성 두께 2–3 개)?  → 권고: 가능하면 — 모델에는 집전체 접촉 항이 없고 (① 은 판 결합 범위 밖) SDCP 가 그 접촉을 바꿀 수 있다 (해석).
- **Q10** SDCP 막 두께 · 덮임 값은?  → 권고: 앵커 없음 = 시나리오 두 값 · "재료 예측 아님" 표지 · 결과 보고 뒤 다시 고르지 않는다.
- **Q11** Codex 시점?  → 권고: S0b + S1 + S1r 한 회차 (런 전) · S2 는 `RIMPR` 수정과 같은 회차 · S3 은 S2 뒤.

## 부록 A. 정본 카드에서 확인한 값 (`git show origin/claude/friendly-meitner-lldvar:litdb/papers/<slug>.md`)

| slug | 확인한 값 (카드 표기 그대로) |
|---|---|
| `lee2025_corolling_dryprocess_lpscl_ptfe` (Nat. Commun. 16, 4200) | SI Fig 5: PTFE 0.5 / 2 / 5 wt% → σ_e 34 / 4.5 / 0.011 · σ_ion 0.069 / 0.024 / 0.007 mS/cm (CAM:SSE:VGCF 80:17:3 · 75 MPa) · SI Fig 10 DMA ≈150 → 50 MPa (30 → 120 °C) · 인장 0.049 / 0.441 / 0.510 N/cm |
| `lee2025_dual_fibrous_ptfe_dry_electrode` (EES · D5EE03240G) | rope Ø 0.248 µm (N=100) · fibre Ø 0.048 · AR 26.96 / 26.97 · rope 평균 길이 6.689 µm (최장 14.257) |
| `lee2026_unveiling_ptfe_dry_electrode_digital_twin` (Small · smll.75974) | 0.2 wt% PTFE: σ_e 시뮬 0.92 → 1.85 · 실측 0.93 → 1.91 ×10⁻² S/cm · NCM 표면 LPSCl 35 → 59 % · 1.0/0.5 wt% σ_e 0.70 (밀도 −4.3 %p) · GeoDict VGCF 83 S/cm · 화소 20.83 nm |
| `hong2026_sulfide_cathode_binder_digitaltwin` (ESM 86, 104930) | PTFE (건식) = 국한된 피브릴 망 · CBD 피복 Pwd 5 → PTFE 9 % (GrainGeo 합성 트윈 · σ_ion 보정) |
| `endo2001_vgcf_basic_properties_battery_applications` (Carbon 39, 1287) | 단섬유 1×10⁻⁴ (흑연화) · 1×10⁻³ Ω·cm (탄화) stated · 압착 분말 ≈0.012 Ω·cm @0.8 g/cm³ (Fig 7 판독) · ≈1 → ≈0.0034 Ω·cm (0.13 → 2.0 g/cm³) · 인장탄성률 ≈110–310 GPa (Fig 6 영역) |
| `lawrence2008_single_vgcnf_elastic_modulus_morphology` (ACS Nano 2, 1230) | 17 가닥 6–207 GPa · D ≤ 200 nm 9 가닥 23–207 GPa (중앙 81) |
| `reisacher2023_percolation_sulfide_carbon_matrix` (Batteries 9, 595) | LPSCl + C65 · p_c ≈ 4 wt% · 3 / 4 / 5 wt% → 1.66×10⁻⁴ / 1.36×10⁻³ / 1.02×10⁻¹ S/cm · LPSCl 0.43 mS/cm |
| `kim2025_conductive_agent_se_coating_cathode` (Battery Energy 4, e70044) | 코팅층 σ_e: SE@CAM 3.3×10⁻² · SE-SP@CAM 1.0×10⁻⁵ · SE-VGCF@CAM 1.4×10⁻² S/cm |
| `kim2024_carbon_volumetric_occupation_se_domain` (AFM 34, 2409318) | ρ Super C 0.67 · LPSCl 1.86 g/cm³ (Archimedes) · SC ↔ CF σ_ion 0.087 / 0.105 · σ_e 5.08 / 5.18 mS/cm (1 wt% 건식) |
| `asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing` (Energy Technol. 11, 2200867) | 건식 고강도 혼합 CB 분쇄 하한 x_lim ≈ 0.2 µm |
| `zhang2026_dryprocess_electrode_architecture_cell_level` (Nat. Energy) | VGCF–PTFE 전단 결합 → CBD 최대 연결 분율 17.1 → 61.2 % · 섬유–섬유 접촉 저항은 다루지 않음 (융합) |
| `cho2024_conflicting_roles_conductive_additive` (Electrochim. Acta) | Table S2 porosity CA 없음 / 있음 0.14 / 0.15 (low f_AM) · 0.18 / 0.19 (high f_AM) |

리포 안 실측 (litdb 아님 · 원고 자체 데이터): 원고 Figure 2 펠릿 (`docs/reviews/sdcp_ion_calib_prereg_20260825.md` §1–2) · 전극 DC 분극 SBE 7.016 Ω / 90 µm · DBE 2.178 Ω / 80 µm ·
지름 10 mm (등록 v2 §1 · 2-전극 · n = 1) · 원고 TLM R_ele 비 1.09–1.23 (등록 v2 §7 · 조건 확인 대상).  R_j (탄소 접합) · SDCP 막 두께 · PTFE 면 차단 면적분율 = 정본 카드에서 찾지 못함 [미확인].
