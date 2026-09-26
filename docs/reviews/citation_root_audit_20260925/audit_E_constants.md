# 감사 E — 코드에서 출발한 물성·모델 상수 출처 감사

> ⛔ **기록 사본** — 2026-09-25 읽기 전용 감사 에이전트 보고 원문 (scratchpad → 리포 이전 09-26).  판정의 정본은 원장 `docs/reviews/claims.json` (`CL-90` · `CL-91`) 과 `findings.json` `SELF-51` 이다.  인용 금지 등록부의 문자열은 `⟦CL-xx …⟧` 로 바꿔 적었다.  file:line 은 감사 기준 커밋 기준이라 지금 줄 번호와 다를 수 있다.  종합 = `docs/reviews/citation_root_audit_20260925.md`.


- 기준 커밋: **`171934433`** (브랜치 `claude/stoic-knuth-NObVQ`, 2026-09-25). TSV 의 `file:line` 은 모두 이 커밋 기준이다.
- 감사 중 다른 세션이 **`b037d765c`** (15:35 UTC, SELF-51 2단계)를 커밋했다. 이 커밋은 `se_material.py` 의 σ_grain 라벨(A01)만 고쳤다. 내 대상 파일 가운데 바뀐 것은 `se_material.py` 하나라서, 나머지 행의 줄 번호는 `b037d765c` 에서도 그대로 맞다.
- 기준 문헌은 정본 litdb (`origin/claude/friendly-meitner-lldvar:litdb/papers/`, 330장, fetch 하지 않음)다. 웹 검색은 논문이 실재하는지만 확인하는 데 썼다. 검색 요약에서 나온 숫자는 **"검색 요약 — 미확인"** 이고 LIT-V 근거로 쓰지 않았다.
- 산출물: 이 문서, 그리고 기계 판독용 `audit_E_constants.tsv` (109행, 14열).

## 0. 라벨 정의

| 라벨 | 뜻 |
|---|---|
| LIT-V | 논문을 인용했고, 정본 카드가 그 값을 확인한다 |
| LIT-M | 논문을 인용했지만 카드나 논문이 그 값을 뒷받침하지 않는다 (소재·정의·물리량이 다름) |
| LIT-U | 논문을 인용했지만 정본 카드가 없다 (미검증) |
| CAL | 보정·적합값이라고 적혀 있고, 보정 기록이 docs 에 있다 (자체 측정 데이터 파일이 있는 경우도 여기에 넣고 `OWN-DATA` 로 표시) |
| CONV | 규약·가정이라고 정직하게 적혀 있다 (SI 물리상수는 `PHYS` 로 표시) |
| NONE | 출처 표기가 없다 |
| FALSE | 주석이 사실이 아닌 것을 단정한다 ("single-crystal", "LAB VALUE", "DEM", "측정값 기반" 등) |

플래그: `DRIFT` = 같은 양이 다른 값이나 다른 출처로 존재, `MEAS-NO-DATA` = "측정/실측" 을 주장하지만 리포에 데이터가 없음, `DEAD-CODE` = 호출처 없음.

## 1. 집계

| 라벨 | 전체 (109) | 생산 경로 (99) |
|---|---|---|
| FALSE | 12 | 11 |
| LIT-M | 10 | 10 |
| LIT-U | 18 | 16 |
| NONE | 19 | 18 |
| CAL | 14 | 14 |
| CONV | 24 | 21 |
| LIT-V | 12 | 9 |

생산 경로 99행 가운데 **55행 (56 %)** 이 FALSE·LIT-M·LIT-U·NONE 다. 문헌으로 **값까지 확인된 것은 9행** 뿐이다. 모두 온도 규약, 전기화학 앵커, 첨가제 what-if 앵커다 (Reisacher Eₐ · C65 표 · Kraft · Ma · kim2025 · yun2023 · Kang D_s · Hong PTFE). 반면 **기계·전도 계산의 핵심 입력 가운데 LIT-V 는 하나도 없다.**
(생산 = CLI 기본값·킷 명시값·웹앱 표시값을 포함한다. 죽은 코드, opt-in 트랙, 레거시 솔버는 제외했다.)

## 2. 가장 결과적인 문제 10 (생산 상수 · FALSE / LIT-M / LIT-U / NONE)

1. **`SIGMA_AM_ELECTRONIC = 0.05 S/cm` (50 mS/cm) — NONE** (`network_conductivity.py:57`)
   - 주석은 `"NCM811 grain interior, discharged"` 인데 인용이 없다.
   - 접촉망 전자 σ 의 절대 스케일이 이 값이다: `sigma_full_mScm = σ_rel × 0.05 × 1000`. 그래서 코퍼스 σ_e 타깃과 Stage 22.5 폼, 웹앱 σ_e 가 모두 이 값 위에 서 있다.
   - 정본 `wang2018` 카드는 리포에서 유일한 NMC811 단상 펠릿 σ_e 측정으로 **4.1 mS/cm @20 °C** 를 준다. 50 은 그 12배이고, 측정 구간(−20…100 °C, 0.76–32 mS/cm) 밖에 있다.
   - 뿌리: import `660600a44`.

2. **Stage E 파괴 σ 인자 `FRACTURE_STAGES` 1.00 / 0.85 / 0.40 / 0.10 / 0.02 — LIT-M** (`run_network_full_corrections.py:93`)
   - 주석은 `"(Stage D, Lawn 1998 + Trevisanello 2021) … literature-realistic central estimate"` 이다.
   - Trevisanello 카드에는 σ 손실 측정이 없다 (확산·BET·R_ct 뿐, audit #11 "MIS-ATTRIBUTION"). Lawn 은 교재다.
   - 생산 σ_e_stage_e 를 최대 3배 깎는다 (CLAUDE.md 기록: 8mAh_real_13 에서 11.2 → 3.5).
   - 뿌리: `ceee1d812` (04-30).

3. **파괴 판정 문턱 P_c = A·K_IC²·R/E\* 의 입력 — LIT-U, 서지 의심** (`fracture_model.py:61-72`)
   - K_IC 단결정 1.0: `"Liu 2020 Nat. Energy 5, 304"`. 검색 요약(미확인)에 따르면 그 권·쪽은 Lee 외 Ag–C 음극 논문(pp. 299–308)이다.
   - K_IC 다결정 0.3: `"Quinn 2020 Joule 4, 2466"`. 그런 서지는 찾지 못했다.
   - `A_AUERBACH = 200`: `"Lawn 1998 §3.4 default (low-flaw 50, rough 500)"`. 교재 속 표라서 검증할 수 없다.
   - P_c ∝ A·K_IC² 이므로 이 셋이 2번의 파괴 단계를 직접 정한다.
   - 뿌리: `b1c8262fe` (04-29). 같은 커밋에서 지어진 "Wang 2020" 인용(CL-90)도 들어왔다.

4. **Stage E AM σ_e 결정/크기 인자 0.75 / 0.65 / 0.55 / 0.45 — LIT-M** (`run_network_full_corrections.py:139`)
   - 주석: `"return 0.65  # Trevisanello 2021 reference"`, `"Wang 2021 measured single-crystal NMC at 1-5 μm"`.
   - Trevisanello 는 σ_e 를 측정하지 않았다. Wang 2021 은 카드가 없다.
   - 솔버 내부의 NCM(r) 인자(D05)와 곱해져 AM_P 가 두 번 감쇠된다.
   - 뿌리: `e241675f1` (04-30).

5. **Physics 접촉면적 상수 (Stage-E Physics σ·κ, coverage_physics)** (`plastic_coverage.py:34-50`)
   - `E_REAL_SE = 24 GPa`, 주석 `"LPSCl … (LAB VALUE: 24 GPa)"` / `"experimental consensus"` — **FALSE**. 24 GPa 는 Sakuda 2013 의 75Li₂S·25P₂S₅ 유리값이다.
   - `H_REAL_SE = 0.85 GPa`, 주석 `"sulfide glass range 0.5-1.0 per Sakuda"` — **LIT-M**. Sakuda 는 경도를 재지 않았다. 리포 안에서 같은 값에 출처가 6가지로 붙어 있다.
   - `H_FILM_MIN = 5 nm`, 주석 `"Sakuda 2013 discussion"` — **LIT-M** (L1-08).
   - `POISSON_SE = 0.30` — **NONE**. 정본 카드 값은 0.37 이다.
   - 뿌리: 넷 모두 import `660600a44`. `b037d765c` 이후에도 그대로 남아 있다.

6. **MPM σ_y = 0.30 GPa 의 보정 표적 — LIT-M** (`mpm3d_compaction.py:608`)
   - 주석: `"pure-SE ~0.10 porosity @ 0.30 GPa (Minnmann)"`.
   - minnmann2021 카드: *"이 논문은 pure-SE porosity 를 별도 측정하지 않는다."* minnmann2022 카드: *"우리 보정 표적 … 확인한 적이 없다."*
   - 따라서 MPM 기계 보정에 쓰인 유일한 절대 앵커가 실험값이 아니다.
   - 뿌리: `02b669e1b` (06-15).

7. **σ_grain = 3.0 mS/cm 의 "단결정" 라벨 — FALSE**
   - `b037d765c` 는 `se_material.py` 만 고쳤다. 다음 다섯 곳에는 거짓 라벨이 남아 있다:
     - `step3_sigma.py:76` `"(Cronau)"`
     - `mpm_webapp_payload.py` `--sigma-ion-se` help `"Cronau — production σ_grain anchor"`
     - `group.html:1298` `"Cronau 2022 Li₆PS₅Cl ⟦CL-91 단결정 라벨⟧ … HIGH confidence"`
     - `single.html:2422` `"Cronau 문헌 상수"`
     - `build_literature_reference.py` `"Sakuda 2013 — Li6PS5Cl single-crystal ultrasonic"`
   - ★ **신화의 기원은 `0a040f2b0` (04-29)** 의 Sakuda 귀속이다 (같은 날 `f68b9a1ff` 의 σ_disk 주석도 같다). SELF-51 2단계 커밋 메시지의 뿌리 분석은 이 커밋을 놓쳤다.

8. **Cronau(r_SE) 계단 인자 1.00 / 0.90 / 0.65 / 0.33 — LIT-U + DRIFT** (Stage E `:110`, T1 `_cronau_factor` `:4342`)
   - Cronau 2022 는 카드가 없다. 정본 2021 카드는 이 breakpoint 들이 측정된 적이 없다고 판정했다.
   - `"SPS data (ScienceDirect 2023)"` 는 서지가 아니다.
   - 문서(CLAUDE.md, group.html)는 3-시그모이드(0.5 µm 에서 0.95)라고 적지만, 생산 코드는 계단(0.5 µm 에서 1.00)이다.

9. **열전도 상수 — LIT-U / NONE**
   - `K_SE_THERMAL = 0.7 W/mK "(Ketter 2025)"` 는 카드가 없다 (09-22 에 뼈대 삭제).
   - research-agent 볼트 노트(원문 기반이라고 표기, 원문은 미확인)는 Ketter 를 **LPSCl 0.32 · NCM83 0.71** 로 적는다. 이것이 맞다면 0.7 은 Ketter 의 NCM 값이다.
   - `K_AM_THERMAL = 4` 는 출처가 없다. 그 결과 열 채널 k_ratio 가 5.7 이 되는데, Ketter 수치로 계산하면 약 2.2 다.
   - `thermal_conductivity_derivation.md:298` 의 서지 "Ketter, F. … Thermal conductivity of LPSCl argyrodite" 는 실제 논문(L. Ketter 외, Nat. Commun. 16, 1411)과 저자 이니셜·제목이 모두 다르다.

10. **Phase A 킷이 명시하는 PTFE 바인더 상수**
    - `--coh-ptfe 0.10 GPa` — **NONE**. Hong 2026 은 기공 방향(−6.4 %p)만 준다.
    - `--binder-opt-wt 1.5`, 주석 `"Hong ~1 wt% optimal"` — **LIT-M**. Hong 은 1 wt% 단일 조건만 썼고 최적 조성을 탐색하지 않았다.
    - 현재 주력인 Phase A 킷 5종이 모두 이 두 값을 명시한다.
    - 뿌리: `947f4f24a` (06-30).

다음 순위:

- 웹앱 문헌 참조 CSV (`build_literature_reference.py`, `0a040f2b0`) — **FALSE**
  - `"Minnmann 2021 Adv. Energy Mater. — DEM with relaxation"`: 실제로는 JES 실험 논문이고 DEM 이 없다.
  - `"Bielefeld 2020 — relaxation-included DEM, max overlap 5%"`: GeoDict 기하 모델이고, AM 최대 겹침은 약 1 vol% 다.
- `SHAPE_FACTOR` 1.40 / 1.10 — LIT-U. 웹앱 툴팁이 이를 `"직접 측정값 기반"` 이라고 적는다. SE 1.05 는 "quenched glass (Sakuda)" 로 적혀 있어 LIT-M 이다.
- LNO `cei_suppress = 15` — LIT-M. kim2025 의 R_ct 비(13–20×)를 CEI 성장 억제 배수로 옮겨 적었다.
- 웹앱 E_SE 배지 — FALSE. 가시 라벨 `"(bulk LPSCl: 24 GPa)"` 가 같은 요소 툴팁의 정정문과 모순되고, 툴팁의 "실험 porosity 10 %" 도 거짓이다.

## 3. 같은 양, 다른 값·다른 출처 (drift)

| 양 | 공존하는 값과 출처 |
|---|---|
| σ_grain 3.0 | 출처가 Sakuda 2013 "Li6PS5Cl single-crystal ultrasonic" (04-29) → Cronau 2022 (05-28) → Cronau 2021/2022 (07-28) → "출처 없음" (`b037d765c`, se_material 만) 순으로 바뀌었다. 진단 플롯에 3.0 사본 12곳이 se_material 을 거치지 않는다. fft_homogenize 는 7.0 을 쓴다 (SELF-39) |
| Cronau(r_SE) | Stage E 헤더 (0.5 µm → 0.70, 1.0 → 0.85) ≠ 함수 (0.5 → 1.00) ≠ selftest 주석 (`wf = 0.70`) ≠ CLAUDE.md·nested_cv_sat 3-시그모이드 (0.95). 웹앱은 "3-sigmoid" 라고 표시한다 |
| H_SE 0.85 GPa | 출처 6갈래: Sakuda (코드 주석, lit README) / Koerver 2018 (코드 DB 주석, single.html) / Cheng 2017 (Reviewer_Defence_Notes, Tabor_framework_reference) / Brake 2012 (paper_brittle_caveat) / contact_mechanics_db 의 순환 정의 (σ_y = H/2.8, H = 2.8σ_y) |
| E_SE | "LPSCl LAB VALUE 24" (plastic_coverage) vs 배지 "(bulk LPSCl: 24)" vs 같은 배지 툴팁 "유리값, LPSCl DFT ≈ 22" vs 정본 카드: DFT 22.1 / 27.4 · 나노압입 28.0 · 다공 펠릿 4.7 |
| ν_SE | 0.30 (plastic_coverage · DEM 덱) vs 0.37 (Deng · Torii · Bazzoun 카드) vs 0.49 (MPM 보정값, 역할이 다름) |
| σ_AM (전자) | 50 mS/cm (접촉망 · `_SIGMA_AM_E` · 예측기 · 레거시 복셀) vs 10 / 5 (Stage 22.5 · STEP3) vs 6.0 (fft_homogenize) vs 정본 측정 4.1 (Wang 2018) |
| κ_SE / κ_AM | 0.7 (접촉망 · STEP3 "Ketter") vs ~0.5 (Stage E docstring) vs 0.5 (fft) / 4 vs "단결정 5–8" (Stage E) · Ketter 볼트 노트 0.32 / 0.71 |
| 퍼콜 φc | 0.185 (예측기 FORM X · 플롯) · 0.19 · 0.20 (예측기 v12 · 플롯) · 0.200 / 0.195 (T1 생산) |
| σ_ion 폼 | 예측기 = 은퇴한 v12 (CN^1.5 · cov^0.4 · φc 0.20) ≠ 생산 T1 (φ_eff · CN² · cov_Hertz^½ · Cronau · P2 · f_intact) |
| ρ_SE | 2.0 (규약) vs 1.6 (`dem3d_plastic.py:178`) · 실제 결정밀도 1.85–1.88 |
| x100 | 0.9084 (킷 · 웹앱) vs 0.8540 (`step4_curve_from_log.py:21` 폴백) |
| PTFE_D 0.25 | 코드는 RSC D5EE03240G · Front. Energy 를 인용하지만, 원장 CL-66 은 Lee 2025 로 앵커했다. PTFE_L 40 µm 는 출처가 없다 (CL-66). 실측 끝점거리는 4.13 µm 다 (CL-67) |
| σ_y,SE 0.30 | Tabor 유도값 (H/2.8) 과 MPM J2 보정값이 같은 숫자지만 뜻이 다르다 |
| F · R · T | step4 는 정확한 SI 값을 쓰고, `pybamm_predictor.py:172` 는 96485 / 8.314 / 298 로 반올림한다 |

## 4. 데이터 없이 "측정 · 실측 · lab value · experimental" 이라고 주장하는 곳

- `plastic_coverage.py:34` `"LAB VALUE: 24 GPa"`, `:336` `"experimental consensus"` — 둘 다 거짓이다.
- `run_network_full_corrections.py:155` `"Wang 2021 measured single-crystal NMC…"` — 카드가 없다.
- `single.html:2404` `"Cronau 2022 … 측정값 기반"` — breakpoint 는 측정된 적이 없다.
- `single.html:2134` / `:2140` 형상 인자 `"직접 측정값 기반"` / `"측정값 기반"` — 리포에 데이터가 없다.
- `single.html:25` `"실험 porosity 10% endpoint"` — 실제로는 우리 보정 표적이다.
- `mpm_input_from_case.py:166` x100 `"NMC811 vs-Li GITT 실측 max"` — 데이터가 리포 밖(pybamm Chen2020)에 있다.

## 5. 뿌리 커밋 연표 (문제 행 기준, 저자는 전부 Claude)

| 날짜 | 커밋 | 들어온 것 |
|---|---|---|
| 04-24 | `660600a44` (import, 이전 이력 없음) | E_SE "LAB VALUE" · H_SE Sakuda/Koerver · h_film 5 nm · ν_SE · E_AM 140 · σ_AM 50 · κ 4 / 0.7 "Ketter" · Tabor 툴팁 |
| 04-29 | `b1c8262fe` · `0a040f2b0` · `f68b9a1ff` · `00368b5ea` | K_IC Liu/Quinn · Lawn A = 200 · Wang 2020 · Xu PRX / 문헌표 Sakuda "단결정 σ" · Minnmann/Bielefeld "DEM" / σ_disk Sakuda 단결정 / SHAPE_FACTOR |
| 04-30 | `ceee1d812` · `e241675f1` · `f2f214d54` · `573a07187` | Stage E: Cronau 2022 · Lawn + Trevisanello 파괴인자 · Trevisanello 0.65 · Wang 2021 · Wang 2022 · "SPS ScienceDirect 2023" · "직접 측정값" 툴팁 |
| 05-28~29 | `63adb1727` · `38931e3e7` · `50c60cb00` · `35170117d` | Cronau 인자가 T1 폼으로 들어감 · σ_grain 을 "Cronau ⟦CL-91 단결정 라벨⟧" 으로 재귀속 · "HIGH confidence" · σ_AM "literature-range" |
| 06-15 | `02b669e1b` · `76b0a6b3c` | σ_y "(Minnmann)" · `--e-am` 140 |
| 06-30 | `947f4f24a` · `a2ff03cb6` | coh_ptfe 0.10 · binder_opt "Hong ~1 wt% optimal" · "calibrated" curl |
| 07-09~28 | `9d8b0a0e4` · `fbde84c4d` · `1b633d93d` · `d66fd1448` · `df398e3db` | payload "Cronau 앵커" · LNO "CEI 13–20×" · STEP3 "Ketter" · se_material / step3 "Cronau" · "Cronau 문헌 상수" |

⇒ 거짓이거나 의심스러운 서지의 대부분은 **04-29~04-30 이틀**과 **import** 에 몰려 있다. 그 뒤의 커밋은 대개 그 라벨을 옮기거나 넓혔다.

## 6. 원장 대비

이미 등재된 항목: SELF-51 · CL-90 (Wang 2020, σ_grain, 24 GPa 문서층) · L1-08 (h_film) · R20-04 / SELF-13 (σ_VGCF 등 hook) · SELF-39 (fft 상수) · AUD-02 · CL-66 / 67.

**신규 또는 미등재 (제안):**

- σ_AM 50 mS/cm 의 무출처 (Wang 2018 대비 12×)
- Stage E 파괴·결정 인자의 Trevisanello 오귀속
- K_IC 서지 불일치 (Liu / Quinn) 와 Lawn "§3.4 / Table 3.4"
- H_SE Sakuda 오귀속 — 09-09 audit1 [15] 에서 지적됐지만 원장에 없다
- MPM σ_y 표적의 Minnmann 오귀속
- Ketter κ 값 뒤바뀜 의심
- PTFE coh / binder_opt (Phase A)
- 문헌 CSV 의 거짓 "DEM" 두 행
- σ_grain 잔존 라벨 5곳과 기원 커밋 `0a040f2b0`
- 웹앱 E_SE 배지의 자기모순
- SHAPE_FACTOR "측정값" 주장
- Cronau 계단 vs 3-시그모이드 drift
- 예측기 v12 폼 drift

## 7. 방법과 한계

- 방법: 대상 파일마다 `UPPER_CASE = 수치`, argparse 수치 기본값, 재료 dict, LIGGGHTS `property/global` 줄을 grep 으로 뽑고 주석·docstring·help 를 인용했다. 인용된 논문은 정본 카드와 대조했고, 문제 행은 `git log -S` 로 뿌리 커밋을 찾았다. 추가로 `additives.py` · `grade_engine.py` · `dem_analysis_core.py` · `build_literature_reference.py` · `mpm_input_from_case.py` 를 봤다. 앞의 셋은 생산 경로가 import 하고, 뒤의 둘은 웹앱 표시값과 킷 기본값을 만든다.
- 한계:
  - 출판사 원문은 모두 차단됐다 (nature.com · PMC).
  - Ketter 수치는 정본이 아닌 research-agent 볼트 노트와 서로 엇갈리는 검색 요약에만 근거한다.
  - Liu 2020 · Quinn 2020 · Cronau 2022 판단은 검색 요약이다.
  - Lawn 교재 속 절·표 번호는 확인하지 못했다.
  - 모든 argparse hook (섬유 형상, 공정표 등) 을 전수로 보지는 않았다. 첨가제 형태 hook 은 대표 행으로만 넣었다.
- 작업 사고 1건: 생성 스크립트를 리포 경로에서 실행해 `audit_E_constants.tsv` 가 리포 루트에 **추적되지 않는 파일**로 약 10초 동안 생겼다. 즉시 스크래치패드로 옮겼고 `git status` 가 깨끗한 것을 확인했다. 커밋이나 다른 변경은 없었다.

## 8. TSV 열

`id · group · quantity · code_name · value_unit · file_line@171934433 · used_by · production · provenance_as_written · label · flags · judgment · root_commit · related_ids`
