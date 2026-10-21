# 사전 리뷰 — 믹서 D2 결합 규칙 (기하평균 W_ij = 2√(γ_iγ_j)) · 리뷰 핀 `a76f59d0d`

**결론: HOLD (P1 0 · P2 2 · P3 5)** — 생성기가 내는 덱 값은 맞다 (독립 되읽기 9 덱 · 기본 경로 356 비교 비트 같음).
막는 것은 값이 아니라 ① 그 값을 **덱 텍스트에서 인증할 경로가 리포에 없다** (되읽기 · 대조 · 스모크 도구가 gen1 밀도 · min 규칙만 안다) ·
② **생산 경로 (lab20261014 세대 D2 덱) 의 절대 수준 · 기록을 시험이 붙잡지 않는다** (변이 셋이 143/143 으로 살아남고 리포 대조 도구도 통과).
→ Codex 에 "D2 생성기 코드" 로 내면 값 쪽 HOLD 근거는 찾지 못했다 · "D2 덱 발사 준비" 로 내면 01 · 02 가 HOLD 사유가 될 것으로 본다 (추정).

---

## 0. 범위 · 입력 · 방법

| 항목 | 내용 |
|---|---|
| 작업 트리 | `git reset --hard a76f59d0d` (fetch 없음) · 생성기 HEAD 파일 = `cb5a6a445` 판 (md5 `829a1a15…`) |
| 커밋 | `f1d7d9271` (D2 규칙 · GM①–⑫ · 벽 0.0256 · MIX-12) · `42061a3f1` (`--gm-wall-ncm` · GM⑬) · `dd161fd3f` (밀도 세대 시험 먼저) · `cb5a6a445` (밀도 세대 구현 · D2 덱 = `--dens-gen` 필수) |
| 문서 | `docs/hetero_thesis.md` §2–§4 · `docs/mixer_d2_wall_gamma_derivation_20261014.md` · `docs/mixer_devlog/v16_20261014.md` · `docs/mixer_paper_pipeline_draft_20261013.md` §4 D2 · §5 S1 · `docs/reviews/mixer_d3_se_flowability_anchor_design_20261015.md` §1-1 · §3-3 · `docs/session_20260923_progress.md` 10-14 밤 3 · 6 · 10 · 11 · 원장 `MIX-12` |
| 원문 대조 | Hare 2026 정본 카드 (`origin/claude/friendly-meitner-lldvar` 읽기만) Table 3 γ_pp 0.25 · γ_pw 0.04 J m⁻² · δ_n = a²/R* − √(4πγa/E*) 확인 · LIGGGHTS-PUBLIC `cohesion_model_sjkr.h` (공개 소스 · sha256 `3ff30925…` = 유도 문서 인용값과 같음) |
| 도구 | `scripts/mixer_deck_readback.py` · `scripts/mixer_deck_diff.py` · `scripts/mixer_smoke_blind.py` (`_expected_counts`) — 읽기 · 실행만 |
| 방법 | 내 파서 (생성기 · 리포 검사기 import 없음) 로 **인쇄된 덱 값**에서 E · ν · 템플릿 r · ρ · CED 를 되읽어 법칙을 다시 계산 · 옛 판 (`e432ec015`) ↔ HEAD 바이트 비교 · 변이 24 · 해석 반례 · 리포 도구에 D2 덱 투입 |
| 환경 차 | 생성기는 numpy 를 쓰지 않는다 (순수 Python `math`) → BLAS 경로 무관 · 기본 · `OPENBLAS_CORETYPE=Haswell` 두 번 생성 = 덱 · 메타 바이트 같음 (F5) |

## 1. 보장 목록 (자리 · 반례 · 결과)

| # | 보장 (주장하는 쪽) | 자리 | 반례 · 시험 | 결과 |
|---|---|---|---|---|
| G01 | 옛 팔 · 옛 덱 · deck_meta 비트 그대로 (기본 끔) | 커밋 `f1d7d9271` · `cb5a6a445` 메시지 · `make_mixer_deck.py:462-469` 디스패치 | 옛 판 `e432ec015` ↔ HEAD: 라이브러리 19 팔 × 18 설정 = **342** (덱 · CED · 경화 메타) + CLI **14** 경우 · 파일 **70** (deck_meta 는 generator_sha256 만 뺌 · 화면 출력 포함) | **342/342 · 14/14 같음** (거부 21 도 양쪽 같음 = LU637 CGF 200 · hold 없는 경화) |
| G02 | F₀_ij = F₀_SS · √(γ_iγ_j)/γ_SE · R*_ij/R*_SS (혼합쌍 · 벽) | `:571-600` | 내 파서로 인쇄된 덱 9 개 (γ 1 · 0.3 · 0.3/0.5 · 10 · Bo 0.21–637 · gen1 · lab · soft · ×20 · dt/2 · 전 정밀도) | 최대 상대 오차 **1.60e-5** ≤ 인쇄 허용 3e-5 · 통과 |
| G03 | 절대 수준 F₀_SS = Bo_SE × SE 무게 (덱 세대의 ρ_SE) | `:585` | 같은 9 덱 · SE 템플릿 r · ρ · g 로 Bo 되읽기 | 상대 오차 ≤ **9.3e-6** · 통과 (코드) — ⚠ 시험 공백 = PRE-02 |
| G04 | CED 역산 = LIGGGHTS SJKR + Hertz 의 당김힘 비를 재현 | `:598` · SJKR 소스 (구–구 교차원 면적 · 벽 π(ri²−r²)·area_ratio) | 정확 면적으로 당김힘 최대값을 수치로 찾아 비 대조 | Bo 0.21 에서 ≤ **2.5e-5** · Bo 5 (γ_AM 10) ≤ **1.7e-4** · Bo 637 (겹침 0.73–0.84 %) ≤ **2.8e-3** (유한 겹침 면적의 2 차 항) · 통과 |
| G05 | γ 비 1 의 같은 상 대각 = LC 대각 (GM①) | 셀프테스트 GM① (gen1 만) | gen1 · lab 두 세대 인쇄 CED | 비 **정확히 1.0** (두 세대 모두) · 통과 |
| G06 | 벽 γ_W/γ = 0.0256 → SE–벽 / SE–SE = 0.32 · 비코팅 NCM 묶음 → AM–벽 / AM–AM = 0.32 | `:488-495` · 유도 문서 §2 | 되읽은 비 | **0.32000** (SE · AM_P · 두 세대) · 통과 |
| G07 | 겹침 천장 = 모든 쌍 δ₀/min(r) ≤ 1 % | `:547-568` · `ced_for_deck:958-961` | γ_AM 10 · Bo 800 (혼합쌍만 넘는 경우) | HEAD 거부 ("AM_P–SE 겹침 1.418 %") · 통과 — ⚠ 시험 공백 = PRE-03 |
| G08 | 경화 ×F + hold = 새 E 로 직접 계산한 기하평균 (GM⑪) | `:939-962` | ×20 lab · gen1 덱 F₀ 비 · 리포 diff `--allow E` | 오차 ≤ **5.5e-6** · diff E PASS (gen1 · lab) · readback E PASS (gen1) · 통과 |
| G09 | 입력 fail-closed (NaN · ∞ · 0 · 음수 · bool · 문자열 · 상 누락 · 남는 상 · SE ≠ 1 · 벽 · Bo 없음) | `:499-532` · GM⑧ 17 가지 | CLI 9 가지 (F6) + 극값 (F3) | 거부 맞음 — ⚠ 1e-200 · 1e-310 · `0_3` 통과 = PRE-04 |
| G10 | CLI 배타 (--arm · --all-arms · 벽 두 방식 · 셋 필수 · --dens-gen 필수) | `:2817-2844` · GM⑫ ⑬ · DG⑥ | 변이 M14 · M20 | 둘 다 죽음 · 통과 |
| G11 | 벽 = 비코팅 NCM (같은 ρ 세계 코팅 · 비코팅 같은 벽) | 결정 Q2 · GM⑬ | ρ 와 팔 γ 를 어긋나게 (F4) | 셋 다 받아들임 = PRE-05 |
| G12 | 기록 (덱 머리 · deck_meta.adhesion_rule · dens_gen) | `:1001-1032` · `:1110-1120` | 변이 M04 · M16 → 기록 ↔ 덱 대조 (I) | HEAD 맞음 (비 1.0000013) · 변이 두 개가 셀프테스트 · 리포 diff 를 통과 = PRE-02 |
| G13 | 규칙은 CED 행렬로만 덱에 들어간다 | 덱 `fix mC … cohesionEnergyDensity` · `pair_coeff * *` · 벽 = 같은 행렬 마지막 타입 | LC → GM γ 1 (gen1 · ×20) 리포 diff 전체 출력 | CED 밖 차이 **0** · 바뀐 원소 6 (대각 3 = ×1) · 통과 |
| G14 | 결정성 · 환경 무관 | 순수 Python | 두 번 · Haswell 환경 | 바이트 같음 · 통과 |
| G15 | 커밋 메시지 수치 | 네 커밋 | 커밋마다 그 판 셀프테스트 (그 판 additives.py 와) | 123/123 (`e432ec015`) · **135/135** · **136/136** · **134/143** (FAIL 9 = GM⑫ ⑬ · DG①–⑦) · **143/143** · readback 24/24 · diff 55/55 = 메시지와 같음 · "고치기 전 123/135 · GM⑬ 실패" 는 따로 커밋된 판이 없어 재현 불가 (주장만) |
| G16 | devlog · MIX-12 수치 | devlog v1.6 표 · 원장 MIX-12 | 인쇄 덱 (LC ↔ GM γ 1 · soft) | 0.826/1.80 · 0.653/1.60 · 3.41/5.54 · 0.162/0.32 · 4.06/2.88 · 0.4516 — 두 세대 모두 재현 · 통과 |
| G17 | 논지 산술 (1.8 · 1.6 · 0.309 · 0.391) | 논지 §2-3 · GM⑤ | 위 표 | 통과 · ≈194 · ≈38 은 gen1 밀도 값 (lab = **239.5 · 47.3**) — 논지가 gen1 밀도를 적어 둬 틀린 문장은 아님 |
| G18 | 덱 검사기 ↔ 새 규칙 일관 | readback · diff · smoke | D2 덱 투입 (D · G · H) | 오수용 0 · 그러나 인증 경로 없음 = PRE-01 |
| G19 | D3 설계의 천장 수치 | D3 §1-1 · §3-3 | 두 세대로 CLI | gen1 에서만 참 = PRE-07 |

## 2. 결함 표

| ID (임시) | 등급 | 자리 | 반례 (입력 → 기대 → 실제) | 최소 해결 |
|---|---|---|---|---|
| **PRE-MIXD2-01** | **P2** | `scripts/mixer_deck_readback.py:52` `REG_DENSITY = {'AM': 4800.0, 'SE': 2000.0}` · `:46` KINDS (E · E0 · DT · B · U) · `scripts/mixer_deck_diff.py:68` ALLOW (B · A) + E · EB · U · `:539-542` 셀 이름 = E0 · LC · LH · LHx · LU 만 · `scripts/mixer_smoke_blind.py:245-248` `_expected_counts` = 세대 없는 `plan()` (gen1) · 계획 `mixer_paper_pipeline_draft_20261013.md` §5 S1 의 "새 허용목록 · 되읽기 표 · 셀 이름 · 코호트 · 정책 v5" 미구현 · 진행 기록 10-14 밤 11 ⬜ 만 (원장 행 없음) | (a) lab D2 soft → ×20 readback 표 E → 기대: 법칙 · F₀ 보존 검산 → 실제 rc 1 *"입자 템플릿이 등록 3 상 (밀도 4800 둘 · 2000 하나) 이 아니다"* (LC lab 도 같음) · (b) 같은 ρ 0.3 세계 비코팅 (γ 0.3) ↔ 코팅 (γ 1) = 바뀐 CED **7** (AM–AM ×1.4938 · AM–SE · AM–벽 ×1.2222 · SE–SE · SE–벽 같음) → diff A · B · U · E · EB **전부 rc 1** (D2 대비를 인증할 허용목록 없음) · (c) lab 계획 AM_P **143** · AM_S **699** · SE 99,158 ↔ 스모크가 기대할 gen1 176 · 859 · 98,965 · (d) D2 덱 머리 문장 *"실행 덱 검산은 scripts/mixer_deck_readback.py"* (`:995`) — 그 도구가 lab 덱을 거부 · ★ 결과: D2 법칙을 **덱 텍스트에서** 확인하는 것은 이 리뷰의 탐침뿐 (오수용은 없음 — 거부 · 통과 모두 옳은 이유) | 되읽기 표 GM (덱 텍스트만: F₀ 비 ↔ √(γγ)·R* 비 3e-5 · Bo_SE = F₀_SS/W_SE (덱 r · ρ · g) · δ₀/min r ≤ 1 % · deck_meta.adhesion_rule ↔ 덱 결합 — `probe_d2_readback.py` 의 `analyse()` 가 최소 판) · 세대별 등록 밀도 (deck_meta.dens_gen 으로 고름) · D2 대비 허용목록 (7 원소 · 배수 (γ_c/γ_u)^(1/3) · ^(1/6)) · 셀 이름 · 코호트 · 스모크 계획 수에 dens_gen · 원장 등재 |
| **PRE-MIXD2-02** | **P2** | GM② (`:2420-2439`) = `ced_matrix_geomean(a_, _dg)` 기본 밀도 (gen1) 만 · GM⑫ (`:2546-2573`) Bo = 0.21244 = `BO_BASE` · lab D2 덱의 CED 를 직접 보는 시험 없음 · deck_meta ↔ 덱 결합 시험 없음 | 변이 (셀프테스트 **143/143 그대로**): **M04** F₀_SS 에 gen1 ρ_SE → lab D2 덱 되읽은 Bo **0.6098** vs 선언 0.5 (×**1.2195** = 2.00/1.64) · **M05** 덱 경로가 밀도 안 넘김 → lab 덱 전부 (D2 · 옛 팔) gen1 밀도로 Bo↔CED · **M16** meta bo_se := BO_BASE → meta **0.21244** vs 덱 **0.5** (×2.354) · 세 덱 모두 리포 `mixer_deck_diff --allow E` **1/1 PASS** · readback 은 밀도 등록 때문에만 거부 (I) | GM② 를 lab · gen1 두 세대로 + 인쇄 덱 절대 수준 검사 · GM⑫ 를 lab · 기본값 아닌 Bo (예 0.5) · "deck_meta.adhesion_rule ↔ 덱 CED" 결합 셀프테스트 (Bo 되읽기 · γ 비) |
| PRE-MIXD2-03 | P3 | GM⑨ (`:2511-2524`) 거부 사례 = γ 1 · Bo 1e6 하나 (SE–SE 대각이 먼저 걸림) · `_assert_ceiling_pairwise:558-568` | γ_AM 10 (`--gm-wall-ncm 10`) · Bo_SE 800 · lab · soft → HEAD 거부 (AM_P–SE 1.418 %) ✓ · 변이 **M06** (혼합쌍 건너뜀) 143/143 + 덱 씀: AM_P–SE **1.4176 %** · AM_S–SE **1.363 %** (SE–SE 0.853 %) · M07 (경화 덱 대각 검사) 도 생존 — 단 soft 검사가 먼저라 F ≥ 1 에선 같은 행동 (F < 1 만 차이 · 등록 밖) | 위 사례를 GM⑨ 에 (거부 사유가 AM_P–SE 를 짚어야 PASS) |
| PRE-MIXD2-04 | P3 | `:597` `math.sqrt(g[ti] * g[tj])` · `_gm_num:499-506` (범위 없음) · CLI `float()` (`:2836`) · `_ARM_NAME_RE:496` (`$`) | (i) γ_AM_P **1e-200** 받음 → 곱 언더플로 → AM_P–AM_P CED **0** (덱 머리 행 0 · 0 · 0.0000 %) 인데 AM_P–SE 5.89e-30 · AM_P–벽 2.29e-29 = GM⑦ *"나머지 양수"* 가 받은 입력에서 깨짐 · (ii) Bo_SE **1e-310** 받음 → F₀_SS 준정규수 · 덱 씀 · (iii) `AM_P=0_3` → **3.0** (밑줄 숫자) · 전각 숫자 → 0.3 · (iv) `register_arm('GM\n', …)` 통과 → 덱에 주석 아닌 줄 `: D2 결합 규칙 …` (LIGGGHTS 가 못 읽는다 · CLI 는 'GM' 고정이라 라이브러리만) | √g_i·√g_j · 지원 범위 선언 · 강제 (예 γ · γ_W ∈ [1e-6, 1e6] · Bo ∈ [1e-6, 1e4]) · 계산 뒤 벽–벽 밖 CED 유한 > 0 · F₀ 정규수 단언 · `--gm-*` 값 = ASCII 십진 정규식 · 이름 = `fullmatch` / `\Z` |
| PRE-MIXD2-05 | P3 | `gm_wall_from_ncm:492-495` · CLI `:2840-2843` · 도움말 `:2784-2786` · 주석 `:484-485` | 결정 Q2 (벽 = 비코팅 NCM) 를 강제하지 않음: AM 0.3 · ρ **3** (γ_W 0.0768) · AM_P 0.3 / AM_S 0.6 · ρ 0.3 · AM 0.5 · ρ 0.3 — 셋 다 rc 0 (F4) · ρ ≠ 1 팔에 `--gm-gamma-wall` 도 그대로 받음 · AM_P ≠ AM_S 면 "비코팅 NCM" ρ 미정의 · 도움말 (*"ρ ≠ 1 이면 0.0256·ρ 여부 = …§5"*) · 주석 (*"어느 상에 묶을지 = 1저자 결정"*) 이 10-14 결정 뒤에도 열린 질문처럼 읽힘 | `--gm-wall-ncm` 이면 AM γ 마다 ∈ {1 (코팅), ρ (비코팅)} 또는 `--gm-role` 명시 + 메타 기록 · ρ ≠ 1 팔의 `--gm-gamma-wall` = 등록된 예외 표지 없으면 거부 · 도움말 · 주석 정정 |
| PRE-MIXD2-06 | P3 | 덱 `:1305` · `deck_meta:1087-1088` · devlog v1.6 · 셀프테스트 | D2 덱 9/9 에 *"# ★ 메시 `type 4` = 벽 전용 타입 (강철 ÷135, 점착 = 입자값 ÷ 1.842)"* — D2 벽은 기하평균 (머리 블록과 모순) · `registered` = 강성 축 사전등록 §3 (D2 덱은 "등록 전") · `schema` `mixer_deck_meta/1` 그대로 (새 키 adhesion_rule · dens_*) · `arm` = 모든 D2 덱이 "GM" · 생존 변이: **M15** 머리 표 F0/F0_SS 를 F₀ 로 · **M18** D2 팔 균일 삽입 (D11 = 층상) · **M13** ρ ↔ γ_W 대조 삭제 · devlog v1.6 CLI 줄에 뒤에 생긴 `--dens-gen` 필수 없음 (CLAUDE.md 코드 → 웹앱) | 벽 주석을 규칙에 따라 · 규칙별 `registered` · schema 판 올림 · 머리 표 · layered · ρ 대조 시험 · devlog 한 줄 |
| PRE-MIXD2-07 | P3 (문서) | D3 설계 §1-1 · §3-3 · 논지 §2-3 | D3 은 "덱 밀도 세대" 를 쓴다고 하면서 gen1 수치: 637.32 = 0.837 % (lab **0.733 %**) · 850 = 1.014 % 거부 (lab **받음**) · CGF 200 637 거부 (lab **받음**) · 상한 ≈ 8.3×10² (lab ≈ **1.01×10³**: 1010 받음 · 1020 거부 1.003 %) · 논지 ≈194 · ≈38 (lab 239.5 · 47.3 — 논지는 gen1 밀도를 적어 둬서 문장 자체는 참) | D3 수치를 세대별 표로 · 세대 미지정 수치에 gen1 표지 |

## 3. 확인했지만 결함 아님

- 기본 끔 경로 = 옛 판과 바이트 같음 (G01 · 342 + CLI 14 · 70 파일 · 화면 출력 · 거부 문구 rc).
- 법칙 · 벽 · 절대 수준 · 경화 · dt/2 · 전 정밀도 덤프 조합 = 인쇄 덱에서 맞음 (G02–G08) · 머리 표 = 내 계산과 ≤ 1.6e-5.
- 규칙이 덱에 들어가는 자리는 CED 행렬 하나뿐 (G13) — `pair_coeff * *` · 벽 = 같은 행렬 마지막 타입 · 다른 명령 토큰 같음.
- Hare 0.0256 유도: 카드의 δ–a 식 (√(4πγa/E*) ⇒ w = 2γ) · Table 3 값 그대로 · 비에서 JKR 상수 2 배 모호성 약분 — 맞음.  비코팅 NCM 묶음은 AM–벽/AM–AM = 0.32 (Hare 그대로) 를 지킨다 (되읽기 0.32000).
- SJKR + Hertz 실제 당김힘 = (4/27)·F₀ (모든 쌍 같은 상수) → 생성기의 F₀ 비 = LIGGGHTS 당김힘 비 (작은 겹침 · 0.84 % 에서 ≤ 0.28 % 차).
- 리포 검사기 오수용 0: 세대 섞인 짝 6 = 전부 rc 1 · LC → GM = A · B · U 전부 rc 1 · gen1 D2 soft → ×20 = readback · diff E PASS (옳은 통과).
- CLI 거부: NaN · 중복 상 · 끝 쉼표 · 소문자 상 · 벽 두 방식 · `--dens-gen` 없음 · `--arm` 과 함께 (G09 · G10).
- 커밋 메시지 · devlog · MIX-12 수치 전부 재현 (G15 · G16).
- 5 상 (섬유) 라이브러리 경로도 D2 덱을 만든다 (F7 · 카탈로그 경로 · 주장 없음).

## 4. 못 본 것 · 이유

- LIGGGHTS 실행 (금지) — 메시 벽 접촉의 `area_ratio` 가 1 이 아닌 경우 (SJKR 이 벽 힘에 area_ratio 를 두 번 곱함) 는 추적 못 함 · 옛 덱 · D2 덱 공통 · 유도 문서도 [미확인] 으로 적어 둠.
- `webapp/test_mixer_devlog_page.py` (devlog 9/9) — 봉인 파일 `webapp/app.py` 를 import 해 폴더를 만들 수 있어 리포에 쓰지 않으려고 안 돌림.
- "고치기 전 123/135 · GM⑬ 실패" — 시험만 있는 판이 따로 커밋되지 않아 이력에서 재현 불가 (시험 먼저 판 `dd161fd3f` 의 134/143 은 재현).
- D7 (코팅 SE 를 자유 SE 에서 빼기) — 미구현 · S1 이 D2 · D7 을 묶지만 이번 범위 (D2) 밖.
- 실제 침대에서 혼합쌍 천장 1 % 의 의미 (정적 · 고립 접촉 근사) — 기존 규약 그대로라 판정 안 함.

## 5. 변이 시험 (24 · 각 1 줄 · `probe_mutations.json`)

| 결과 | 변이 |
|---|---|
| 죽음 16 | M01 산술평균 · M02 R* 빠짐 · M03 벽 R* ½ · M08 벽 γ 무시 · M09 soft 천장 없음 · M10 ρ 무시 · M11 0 허용 · M12 NaN/∞ 허용 · M14 벽 두 방식 허용 · M17 meta γ_W 상수 · M19 겹침 큰 반경 · M20 세대 필수 끔 · M21 CED 지수 · M22 F₀_SS 반경↔지름 · M23 세대 머리 끔 · M24 meta wall_rule 빠짐 |
| **생존 8** | **M04** F₀_SS gen1 밀도 · **M05** 덱 경로 밀도 안 넘김 · **M06** 천장 혼합쌍 건너뜀 · M07 경화 D2 대각 천장 (F ≥ 1 에서 동치) · M13 ρ ↔ γ_W 대조 삭제 · M15 머리 표 비 → 값 · **M16** meta bo_se 상수 · M18 D2 균일 삽입 |

## 6. 산출 · 재실행 (모두 이 폴더 · `python3 -I -B` · 리포에 쓰지 않음)

| 탐침 | 내용 | 결과 파일 |
|---|---|---|
| `probe_byteident.py` | G01 옛 판 ↔ HEAD | `probe_byteident.json` |
| `probe_d2_readback.py` | G02–G06 · G08 인쇄 덱 되읽기 (독립 파서 · 정확 SJKR 당김힘) | `probe_d2_readback.json` |
| `probe_claims.py` | G05 · G16 · G17 수치 | `probe_claims.json` |
| `probe_tools.py` · `probe_crossgen.py` · `probe_contrast.py` | G18 · PRE-01 · PRE-07 (리포 검사기 · 대비 7 원소 · 천장 세대별) | `probe_tools.json` · `probe_crossgen.json` · `probe_contrast.json` · `evidence_diff_LC_vs_GM1_gen1.txt` · `decks/cgf200_*.log` |
| `probe_mutations.py` | 변이 24 | `probe_mutations.json` · `mut/` |
| `probe_edges.py` | F1–F7 (PRE-02–05) | `probe_edges.json` |
| `probe_meta_binding.py` | 기록 ↔ 덱 결합 (PRE-02) | `probe_meta_binding.json` |
| `run_verify_counts.sh` | G15 커밋별 셀프테스트 | `verify/*/selftest.txt` |

```
P=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2
W=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a876633abb3bfa519      # a76f59d0d
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/heavy.sh
cd $P
bash $H python3 -I -B probe_byteident.py > byteident.log 2>&1          # 60 s 넘을 수 있음
bash $H python3 -I -B probe_mutations.py $W > mutations.log 2>&1      # 셀프테스트 24 회
python3 -I -B probe_d2_readback.py ; python3 -I -B probe_claims.py
python3 -I -B probe_tools.py $W ; python3 -I -B probe_crossgen.py $W ; python3 -I -B probe_contrast.py $W
python3 -I -B probe_edges.py ; python3 -I -B probe_meta_binding.py $W  # mut/ 가 있어야 (probe_mutations 뒤)
bash run_verify_counts.sh
```
