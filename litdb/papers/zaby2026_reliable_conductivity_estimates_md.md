# Lessons Learned on Obtaining Reliable Conductivity Estimates From Molecular Dynamics Simulations — Zaby et al. (*ChemPhysChem* 2026)

> slug `zaby2026_reliable_conductivity_estimates_md` · DOI `10.1002/cphc.70477` · type `MD (classical, polarizable FF)` · PDF `5e9d5f12-…pdf` (본문) + `ea0a0cb8-…pdf` (SI) · digested `2026-09-09` · status ✅
> elements: Li, N, O, F, S
> methods: MD

> ⛔ **재료계 경계 (먼저 읽어라).** 이 논문의 계는 **이온액체 [EMIm][DCA] 와 에테르 액체전해질 LiFSI/DME** 다.
> 황화물 고체전해질은 **한 번도 안 나온다**. ⇒ **방법·통계·정의는 가져오고, 값(σ·D·Haven·필요 replica 수·필요 궤적 길이)은 하나도 못 가져온다.**
> 이 문서에서 소환한 수치는 전부 **문헌 소환값**이고 우리 `db/properties/` 절대값과 같은 표에 놓지 않는다.

> 📚 **묶음 위치**: cascade 재설계 문헌 8편 중 **여덟 번째** (σ 를 MD 로 낼 때의 함정).
> 자매편 — `pranami2015_estimating_error_diffusion_coefficients_md`(단일 궤적의 통계 오류 원전),
> `maginn2019_best_practices_transport_selfdiffusivity_viscosity`(이 논문의 ref [94] = LiveCoMS 베스트프랙티스),
> `kahle2020_ht_aimd_screening`(796종을 tracer D 만으로 보고),
> `adeli2019_halide_substitution_boosting_argyrodite`(우리 계열 Haven 실측).
> ⚠ 앞의 두 편은 다른 curator 세션이 동시에 쓰는 중 — slug 만 참조하고 값은 그쪽 digest 가 정본이다.

---

## 0. 이 digest 를 읽는 법

이 논문은 물성 논문이 **아니다**. TRAVIS 라는 궤적분석 패키지에 `conduct` 모듈을 붙인 **소프트웨어 + 방법론** 논문이고,
"σ 를 MD 로 낼 때 무엇이 틀리는가"를 두 개의 액체계에서 실측으로 보여준다.
그래서 우리에게 중요한 것은 §5(실패 모드 목록)·§6(NE vs 집단·Haven)·§7(독립 궤적)·§8(적합 구간)·§9(셀 크기)이고,
**§12 가 우리 σ 파이프라인 항목별 판정**, **§13 이 Stage 10 판정**이다. 급하면 §5 → §12 → §13.

---

## 1. 한 줄 요약

**σ 는 집단(collective) 물성이라 self-diffusion 처럼 다뤄서는 안 된다** — Nernst–Einstein 은 이 논문의 두 액체계에서 참 σ 를 **1.3–2.1× 과대평가**하고(ionicity 0.48–0.76),
집단 σ 의 불확실도는 **한 궤적 안의 요동이 아니라 독립 replica 사이의 산포**에 지배되며(단일 궤적 분할은 SE 를 **1.33–1.52× 과소**),
**"MSD 의 후반부를 적합한다"** 는 흔한 관행은 자동 확산영역 검출 대비 σ 를 **최대 2.8× 낮게** 만든다.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Paul Zaby**¹, **Johannes Ingenmey**¹\*, **Tuanan C. Lourenço**²\*, **Yong Zhang**³, Juarez L. F. Da Silva⁴, Martin Brehm⁵, **Edward J. Maginn**³, **Barbara Kirchner**¹\* |
| 소속 | ¹Mulliken Center for Theoretical Chemistry, Univ. Bonn (DE) · ²UNESP Araraquara (BR) · ³Univ. Notre Dame (US) · ⁴IQSC-USP São Carlos (BR) · ⁵Univ. Paderborn (DE) |
| 저널 | ***ChemPhysChem*** 2026; **27**: e70477 · Wiley-VCH · **Open Access CC BY** |
| DOI | `10.1002/cphc.70477` |
| 날짜 | Received 2026-04-13 · Revised 2026-06-09 · Accepted 2026-06-16 |
| 키워드 | computational chemistry \| ionic liquids \| molecular dynamics |
| 계 | **[EMIm][DCA]** (이온액체, 125/250/500/1000 이온쌍) · **LiFSI/DME** (salt-in-solvent, 1.0 / 2.0 / 3.5 M) |
| 연구유형 | **고전 MD (분극 힘장) + 통계 방법론 + 소프트웨어** |
| 코드 | TRAVIS `conduct` 모듈 (`travis-analyzer.de`) · 후처리 스크립트 `github.com/kirchners-manta/conductivity_tools` · MSDiff v0.2.0 |
| 데이터 | ⚠ **"available from the corresponding authors upon reasonable request"** — 공개 저장소 없음 |

> ⚠ **서지 정정**: 1저자 기억은 "Zaby·Ingenmey·Lourenço·Zhang, 2026" 이었는데 **저자는 8명**이다.
> 특히 **Edward J. Maginn** (7번째)이 들어가 있다 — 이 논문이 인용하는 LiveCoMS 베스트프랙티스(ref [94])의 1저자와 동일인.
> 즉 이 편은 **Maginn 계열 베스트프랙티스의 "전도도 확장판"** 성격이다.

---

## 3. 핵심 수치 총정리 (전부 문헌 소환값)

### 3.1 자기확산계수 (Table 1, Table 2 · 단위 10⁻¹⁰ m² s⁻¹)

**[EMIm][DCA] @ 353.15 K** — CL&P(비분극, 전하 ×0.8) 시리즈 + CL&Pol(분극)

| 계 | 음이온 D | SE | 양이온 D | SE |
|---|---|---|---|---|
| IL¹²⁵ | 1.8807 | 0.0232 | 1.6100 | 0.0218 |
| IL¹²⁵_long (800 ns) | 1.9158 | 0.0185 | 1.6297 | 0.0152 |
| IL²⁵⁰ | 1.9755 | 0.0193 | 1.6724 | 0.0131 |
| IL⁵⁰⁰ | 2.0398 | 0.0140 | 1.7255 | 0.0109 |
| IL¹⁰⁰⁰ | 2.0452 | 0.0124 | 1.7747 | 0.0069 |
| **IL¹⁰⁰⁰_pol** | **2.4142** | 0.0143 | **2.1496** | 0.0099 |

→ 크기 의존: 음이온 **+8.8 %**, 양이온 **+10.2 %** (125→1000 쌍). 분극 힘장: **+18 % / +21 %**.

**LiFSI/DME @ 333.15 K** (LiFSI+DME 입자수 1500 고정)

| 농도 | 음이온(FSI⁻) | 양이온(Li⁺) | 용매(DME) |
|---|---|---|---|
| 1.0 M | 5.5465 ± 0.0779 | 5.0220 ± 0.0667 | 10.4773 ± 0.0449 |
| 2.0 M | 2.0822 ± 0.0214 | 2.1117 ± 0.0140 | 4.5053 ± 0.0109 |
| 3.5 M | 0.3030 ± 0.0060 | 0.3503 ± 0.0043 | 0.9117 ± 0.0134 |

→ 1.0 M 에서는 음이온이 빠르고, **3.5 M 에서 역전**(양이온이 더 빠름).

**Yeh–Hummer 유한크기 보정** (Table S4, S5 · Eq. S4 `ΔD_YH = 2.837297 k_BT / (6πηL)`)

| 계 | ΔD_YH | D 대비 비율 |
|---|---|---|
| IL¹²⁵ (η ≈ 4.7 mPa s) | 0.4813 | **+26 %** (음이온) |
| IL¹⁰⁰⁰ | 0.2407 | **+12 %** |
| LiFSI/DME 1.0 M (η ≈ 0.64) | 1.6974 | **+31 %** |
| 2.0 M (η ≈ 1.84) | 0.5967 | **+29 %** |
| 3.5 M (η ≈ 8.94) | 0.1241 | **+41 %** |

⚠ **저자는 이 보정을 보고만 하고 적용하지 않았다** — σ 에 대응하는 보정이 없어 일관성을 택했다.
그리고 점도 추정 자체가 문헌 외삽이라 "qualitative approximations" 라고 못박는다.

### 3.2 전도도 — 총괄표 (Table S6, S7 · 단위 S m⁻¹)

**[EMIm][DCA]** (실험 기준 **6.86 S m⁻¹**, Yu 2009 [98])

| 계 | EH | GK | EH-NE | GK-NE | ionicity(EH) |
|---|---|---|---|---|---|
| IL¹²⁵ | 5.184 ± 0.451 | 4.910 ± 1.800 | 6.820 ± 0.045 | 7.658 ± 0.533 | 0.760 ± 0.066 |
| IL¹²⁵_long | 4.934 ± 0.255 | 4.683 ± 1.421 | 6.793 ± 0.029 | 7.004 ± 0.223 | 0.726 ± 0.038 |
| IL²⁵⁰ | 4.753 ± 0.412 | 4.426 ± 1.282 | 7.011 ± 0.034 | 7.957 ± 0.376 | 0.678 ± 0.059 |
| IL⁵⁰⁰ | 4.473 ± 0.356 | 4.803 ± 1.119 | 7.230 ± 0.017 | 7.256 ± 0.301 | 0.619 ± 0.049 |
| IL¹⁰⁰⁰ | 5.163 ± 0.274 | 5.692 ± 1.062 | 7.350 ± 0.022 | 7.976 ± 0.282 | 0.702 ± 0.037 |
| IL¹⁰⁰⁰_pol | 4.779 ± 0.219 | 5.728 ± 1.855 | **8.820 ± 0.019** | 9.254 ± 0.241 | **0.542 ± 0.025** |

**LiFSI/DME** (실험 기준 = **내삽값** 2.14 ± 0.28 / 1.66 ± 0.22 / 0.96 ± 0.13)

| 농도 | EH | GK | EH-NE | GK-NE | ionicity(EH) | ionicity(GK) |
|---|---|---|---|---|---|---|
| 1.0 M | 2.118 ± 0.201 | 3.073 ± 0.729 | 3.473 ± 0.026 | 3.943 ± 0.132 | 0.610 ± 0.058 | 0.779 ± 0.187 |
| 2.0 M | 1.350 ± 0.091 | 1.627 ± 0.654 | 2.809 ± 0.013 | 3.807 ± 0.120 | 0.480 ± 0.033 | 0.427 ± 0.172 |
| 3.5 M | 0.420 ± 0.021 | 0.902 ± 0.243 | 0.789 ± 0.008 | 1.469 ± 0.128 | 0.532 ± 0.027 | 0.614 ± 0.174 |

**GK ionicity 의 SE 는 0.135–0.239** (EH 는 0.025–0.066) — 5–8배.

### 3.3 self / cross 분해 (Table S14, S18 · S m⁻¹)

| 계 | Total | Self 합 | **Cross 합** |
|---|---|---|---|
| IL¹²⁵ | 5.184 ± 0.451 | 6.820 ± 0.045 | **−1.636 ± 0.453** |
| IL²⁵⁰ | 4.753 ± 0.412 | 7.011 ± 0.034 | **−2.258 ± 0.413** |
| IL⁵⁰⁰ | 4.473 ± 0.356 | 7.230 ± 0.017 | **−2.757 ± 0.356** |
| IL¹⁰⁰⁰ | 5.163 ± 0.274 | 7.350 ± 0.022 | **−2.187 ± 0.275** |
| IL¹⁰⁰⁰_pol | 4.779 ± 0.219 | 8.820 ± 0.019 | **−4.042 ± 0.220** |
| LiFSI 1.0 M | 2.118 ± 0.201 | 3.473 ± 0.026 | **−1.355 ± 0.203** |
| LiFSI 2.0 M | 1.350 ± 0.091 | 2.809 ± 0.013 | **−1.460 ± 0.092** |
| LiFSI 3.5 M | 0.420 ± 0.021 | 0.789 ± 0.008 | **−0.369 ± 0.023** |

**cross 항이 항상 음수**이고 그 SE 가 total 의 SE 를 사실상 결정한다 (self 항 SE 는 1/10–1/20).

### 3.4 이온 분해 (Table S15, 무게중심 좌표계 · IL)

| 계 | 양이온 self | 양이온 cross | 음이온 self | 음이온 cross | 음–양이온 cross |
|---|---|---|---|---|---|
| IL¹²⁵ | 3.143 ± 0.027 | −2.416 ± 0.068 | 3.672 ± 0.024 | −1.629 ± 0.184 | 2.413 ± 0.491 |
| IL⁵⁰⁰ | 3.332 ± 0.013 | −2.707 ± 0.051 | 3.896 ± 0.016 | −2.136 ± 0.141 | 2.086 ± 0.385 |
| IL¹⁰⁰⁰ | 3.409 ± 0.011 | −2.689 ± 0.041 | 3.939 ± 0.015 | −1.903 ± 0.110 | 2.406 ± 0.298 |
| IL¹⁰⁰⁰_pol | 4.157 ± 0.010 | −3.490 ± 0.032 | 4.661 ± 0.016 | −2.781 ± 0.087 | 2.232 ± 0.237 |

### 3.5 수송수 (transport number)

**이상(ideal) 수송수** — self-diffusion 만 (Table S10): IL 전 계에서 음이온 **0.529–0.542**, 양이온 0.458–0.471.
크기·힘장·EH/GK 무관하게 거의 불변 (정규화로 계통오차가 상쇄).

**실(real) 수송수 — 좌표계 의존** (Table S13, LiFSI/DME, EH):

| 좌표계 | 1.0 M t(Li⁺) | 2.0 M | 3.5 M |
|---|---|---|---|
| Mass-fixed (무게중심) | 0.439 ± 0.050 | 0.451 ± 0.046 | 0.373 ± 0.062 |
| Number-fixed | 0.355 ± 0.052 | 0.289 ± 0.049 | 0.168 ± 0.065 |
| **Solvent-fixed** | 0.320 ± 0.061 | 0.201 ± 0.097 | **−0.174 ± 0.278** |

→ **같은 궤적에서 좌표계만 바꾸면 t(Li⁺) 가 0.373 → −0.174 로 부호가 뒤집힌다.**

### 3.6 표본 오차 — replica vs segment (Table 3 · S m⁻¹)

| 계 | SE_across-replica | SE_within-replica | **비율** |
|---|---|---|---|
| IL¹²⁵ | 0.2522 | 0.1675 | **1.51×** |
| IL¹²⁵_long | 0.2353 | 0.1751 | 1.34× |
| IL²⁵⁰ | 0.2330 | 0.1749 | 1.33× |
| IL⁵⁰⁰ | 0.2116 | 0.1521 | 1.39× |
| IL¹⁰⁰⁰ | 0.2093 | 0.1377 | **1.52×** |
| IL¹⁰⁰⁰_pol | 0.2046 | 0.1518 | 1.35× |

**예외 없이 across > within** — 6/6.

### 3.7 적합창(fit window) 의존 (Fig. S12–S14 · LiFSI/DME EH)

| 농도 | 자동창 (검출된 구간) | σ_auto | 고정 tail (15–30 ns) | σ_tail | **배율** | 실험 기준 |
|---|---|---|---|---|---|---|
| 1.0 M | **60 ps – 24 ns** | **2.03** | 15–30 ns | **0.73** | **2.8×** | 2.14 ± 0.28 |
| 2.0 M | 60 ps – 25.5 ns | 1.34 | 15–30 ns | 0.85 | 1.6× | 1.66 ± 0.22 |
| 3.5 M | 360 ps – 16.5 ns | 0.41 | 15–30 ns | 0.22 | 1.9× | 0.96 ± 0.13 |

### 3.8 EH ↔ GK 등가성 검증 (Table S22, S23)

**Table S22** — IL¹⁰⁰⁰ CL&P 단일 10 ns 궤적, 20 fs 덤프 (**디스크 900 GB 초과**):

| max depth | σ_EH | σ_GK |
|---|---|---|
| 100 ps | 4.8084 | 4.8802 |
| 400 ps | 5.2057 | 4.9556 |
| 1000 ps | 4.5776 | 4.0158 |

**Table S23** — **같은** 10×100 ps replica (LiFSI/DME 1.0 M):

| 처리 | EH | GK |
|---|---|---|
| linear regime / plateau | 3.220 ± 0.282 | 3.073 ± 0.729 |
| tail fit / unweighted avg | 3.637 ± 1.078 | 3.767 ± 0.940 |

→ **같은 궤적·같은 처리면 EH 와 GK 가 오차 안에서 일치한다.** 본문 `Fig. 2` 의 EH–GK 차이(≈0.7 S m⁻¹)는 방법 차이가 아니라 **다른 궤적 세트를 쓴 결과**.

---

## 4. 계산 방법 ★

- **code**: **LAMMPS 23Jun2022** (MD) · **TRAVIS `conduct` 모듈** (분석, 이 논문에서 신규) · **MSDiff v0.2.0** (선형영역 검출) · PACKMOL + `fftool` + `polarizer` (박스 생성)
- **functional / pseudo / k-points / ecut**: **n/a — DFT 가 아니다.** 전부 고전 힘장.
- **힘장**:
  - **CL&Pol** (분극; Drude 입자를 비수소 원자에 부착) — 두 계 모두의 기본
  - **CL&P** (비분극, OPLS 기반; **원자전하를 0.8 배 스케일**) — [EMIm][DCA] 대조용
  - Thole 감쇠 (두 계) + **Tang–Toennies 분산 감쇠** (LiFSI/DME 만)
- **적분**: velocity-Verlet, **dt = 1.00 fs**
- **상호작용**: 단거리 + Coulomb **cutoff 1.20 nm**, 장거리 **PPPM**
- **써모스탯**: **temperature-grouped Nosé–Hoover (TGNH)**, damping T 0.10 ps / P 1.00 ps; **Drude 입자는 1.0 K, damping 0.025 ps**. 비분극 계는 일반 Nosé–Hoover.
- **온도**: IL **353.15 K** · LiFSI/DME **333.15 K** (단일 온도 — 온도 스캔·Arrhenius **없음**)
- **셀 / 원자수**: IL 125·250·500·1000 이온쌍 · LiFSI/DME 는 **LiFSI+DME 입자수 1500 고정** (150/150/1350 · 300/300/1200 · 500/500/1000)
- **평형화 프로토콜** (이 논문의 핵심 설계):
  1. PACKMOL 로 **5개** 무작위 박스 → CG 완화 → 700 K(IL)/500 K(LiFSI) **1 ns NVT** → 목표 T 로 **1 ns NpT** → **10 ns NpT** 중 마지막 5 ns 로 **평균 평형 부피** 결정
  2. **다시 10개** 새 박스를 PACKMOL 로 만들어 같은 (i)–(iii) 을 태우고, **2 ns NpT** 후 **위에서 얻은 평균 부피로 스케일**
  3. **생산: 111 ns NVT** 중 앞 11 ns 폐기 → **100 ns** (Run 1, EH 용). IL¹²⁵_long 은 811 ns → **800 ns**
  4. **GK 용 별도 생산: 0.1 ns** (Run 2, IL¹²⁵_long 은 0.2 ns)
- **덤프**: Run 1 위치만 **1000 steps = 1 ps** 마다 (IL¹²⁵_long 은 4000 steps = 4 ps) · Run 2 **위치+속도를 매 스텝(1 fs)**
- **replica**: **조건마다 10개** — *distinct initial configurations **and** velocity seeds*, **단 밀도는 공통**(위 2단계). 즉 replica 간 분산에서 밀도 항을 일부러 제거했다.
- **상관깊이(correlation depth)**: EH **30 ns = 궤적의 30 %** · GK **75 ps / 100 ps** · 10×10 분할 실험은 **3 ns = 30 %**
- **무질서 처리**: n/a (액체)
- **MLIP**: 없음
- **특이사항**: EH 와 GK 를 **의도적으로 같은 저장 프레임 수**(≈10⁵)로 맞췄다 — 다만 그 결과 **시간 규모가 1000배 달라졌고**, 그게 본문 `Fig. 2` 의 EH–GK 간극을 만든다(SI S7.10 에서 자백·교정).

---

## 5. ★★ 실패 모드 목록 — **무엇이 얼마나 어느 방향으로 틀리나**

> 이 절이 의뢰의 1번 항목이다. 저자가 "lessons learned" 로 부르는 것을 방향·크기와 함께 정리했다.
> **F1–F5 는 통계·처리 문제**(우리가 고칠 수 있다), **F6–F8 은 모델·정의 문제**(고치려면 계산을 다시 해야 한다).

| # | 실패 모드 | **방향** | **크기 (이 논문의 계에서)** | 근거 |
|---|---|---|---|---|
| **F1** | **Nernst–Einstein 사용** (ion–ion cross 무시) | **σ 과대** | **1.31–2.08×** (ionicity 0.48–0.76). 최악: LiFSI 2.0 M **2.08×**, IL¹⁰⁰⁰_pol **1.85×** | Table S6–S9, `Fig. 2`, `Fig. S1` |
| **F2** | **MSD 후반부 고정 적합** (auto 창 대신 tail) | **σ 과소** | **1.6–2.8×** (1.0 M: 2.03 → 0.73 S m⁻¹). 동시에 SE 도 커진다 | `Fig. 6`, `Fig. S12`–`S14` |
| **F3** | **단일 긴 궤적을 토막내 통계**(독립 replica 대신) | **불확실도 과소** (평균값은 거의 안 변함) | **SE 를 1.33–1.52× 과소**, 6/6 계에서 예외 없음 | `Table 3`, `Fig. 7`, `Fig. S15`–`S16` |
| **F4** | **상관깊이를 너무 길게** | 평균 소폭 감소 + **SE 급증** | σ_EH **−8 %** (1→30 ns) 인데 **SE 는 ×3.1** (0.07→0.22). σ_NE 는 −1.8 %, SE 거의 불변 | `Fig. 8`, `Fig. S17`–`S18` |
| **F5** | **GK 적분 plateau 를 눈대중/tail 평균으로** | 분산 폭발 (편향은 계 의존) | **GK SE 가 EH SE 의 3.6–8.5×**. 1.0 M 에서 tail(50–75 ps) 3.77 vs bootstrap 3.07 (figure-read) | `Fig. 5`, `Fig. 6` 하단, SI §S6 |
| **F6** | **좌표계(reference frame) 미명시** — 분해량에만 | 부호까지 바뀜 | t(Li⁺) 3.5 M: **+0.373 → +0.168 → −0.174** (mass→number→solvent) | `Table S13`, `Fig. 4` |
| **F7** | **유한 셀 크기** | **self 는 과소**, **total 은 검출 불가** | D **+9–10 %** (125→1000쌍), YH 보정 **+12–41 %**. **total σ 는 유의한 추세 없음** — cross 항이 상쇄 | `Fig. 9`, `Table S4`–`S5`, `Table S14` |
| **F8** | **힘장(분극 유무)** | self 와 collective 가 **반대로 움직임** | D **+18–21 %** 인데 σ_EH 는 5.163 → 4.779 (**변화 없음/미세 감소**), ionicity 0.702 → **0.542** | `Table 1`, `Fig. 2`, `Fig. S1` |

### 5.1 F1 자세히 — NE 는 왜, 얼마나 틀리나

σ_NE 는 self 항만 더한다 (Eq. 1). 집단 σ 는 self + cross 다 (Eq. 4).
**cross 항이 이 논문의 모든 계에서 음수**이므로 NE 는 항상 과대다:

- IL¹⁰⁰⁰: self 7.350 → total 5.163 (**cross −2.187**, self 의 30 %)
- IL¹⁰⁰⁰_pol: self 8.820 → total 4.779 (**cross −4.042**, self 의 **46 %**)
- LiFSI 2.0 M: self 2.809 → total 1.350 (**cross −1.460**, self 의 **52 %**)

즉 **NE 가 놓치는 항이 self 항의 30–52 % 나 된다.**

⚠ **그런데 실험과 비교하면 이야기가 뒤집힌다** (§16-1 비판 참조):
실험 기준선이 있는 5개 비교 중 **3개에서 NE 가 실험에 더 가깝다** (IL CL&P: EH Δ−1.70 vs NE Δ+0.49 / IL CL&Pol: Δ−2.08 vs Δ+1.96 / LiFSI 3.5 M: Δ−0.54 vs Δ−0.17).
저자는 3.5 M 에 대해서만 *"error compensation between model, force field, and reference data"* 라고 인정하고 이온액체에 대해서는 같은 말을 하지 않는다.

### 5.2 F2 자세히 — "후반부 적합" 이 왜 그렇게 나쁜가

`Fig. S12` 를 실제로 보면 원인이 눈에 보인다 (figure-read):
**평균 CMSD 가 τ ≈ 12 ns 부터 휘기 시작해 τ ≈ 27 ns 이후에는 아예 내려간다** (≈39 → ≈35 ×10³ ps·S m⁻¹).
MSD 는 원리적으로 감소할 수 없으므로 **이 하강은 물리가 아니라 통계**다 — 긴 lag 에서 독립적인 시간원점 수가 급감해서 생긴 것.
"후반부 = 확산영역" 이라는 통념이 정확히 여기서 깨진다: **후반부는 확산영역이 아니라 표본이 마른 영역**이다.

자동창은 1.0 M 에서 **60 ps – 24 ns** 를 잡는데, 이것은 사실상 "짧은/중간 시간 전체"이고
오차가중(초기 구간 가중치 큼) 때문에 결과는 **초·중기 기울기에 가깝다**.

### 5.3 F3 자세히 — 궤적 하나로는 못 잰다

`Fig. 7` (figure-read, IL¹⁰⁰⁰):
- **파랑 "Within replica"** (한 replica 안의 10 토막 평균 = 점 하나가 replica 하나): 값이 **4.09–5.32 S m⁻¹** 로 넓게 흩어지는데 **오차막대는 ±0.08–0.22 로 작다**
- **빨강 "Between replicas"** (같은 index 의 토막을 replica 10개에 걸쳐 평균): 값은 **4.61–5.10 으로 좁은데 오차막대가 ±0.20–0.35 로 크다**

읽는 법: **한 궤적 안에서는 토막들이 서로 잘 맞는다** → 그 궤적이 내놓는 오차막대가 작다 → **그런데 그 궤적 자체가 다른 궤적과 ±13 % 다르다.**
⇒ 단일 궤적의 오차막대는 **자기가 얼마나 틀렸는지 모른다.**

`Fig. S10` (figure-read, LiFSI/DME 1.0 M CMSD): τ = 30 ns 에서 **개별 replica 가 ≈16 부터 ≈123 ×10³ ps·S m⁻¹ 까지 약 8배** 흩어진다(평균 ≈35).
`Fig. 5` 좌측 (figure-read, GK CACF 적분, 1.0 M): 개별 replica 곡선이 장시간에 **−5 ~ +12 S m⁻¹** 사이를 헤맨다 — **replica 하나만 쓰면 음의 전도도가 나올 수 있다.**

저자 결론(원문): *"several independent replicas are not only advantageous but methodically essential."*

### 5.4 F4 자세히 — 상관깊이는 길수록 좋지 않다

`Fig. 8` (figure-read, IL¹⁰⁰⁰_pol):

| 상관깊이 | σ_EH | σ_NE | σ_cross(+−) | SE(σ_EH) | SE(σ_NE) |
|---|---|---|---|---|---|
| 1 ns | ≈5.20 | ≈8.97 | ≈2.43 | ≈0.07 | ≈0.02 |
| 5 ns | ≈5.16 | ≈8.87 | ≈2.41 | ≈0.14 | ≈0.01 |
| 10 ns | ≈4.99 | ≈8.85 | ≈2.34 | ≈0.16 | ≈0.01 |
| 20 ns | ≈4.80 | ≈8.84 | ≈2.25 | ≈0.17 | ≈0.02 |
| 30 ns | ≈4.79 | ≈8.81 | ≈2.23 | ≈0.22 | ≈0.02 |

**σ_NE 는 상관깊이에 거의 무감이고 SE 가 한 자릿수 작다.** 이것이 §13(Stage 10 판정)의 핵심 근거 중 하나다.
저자 권고(원문): *"moderate maximum correlation depths (10 ns with good sampling, 10 % of the total simulation length) are sufficient."*
(⚠ 정작 본문 생산 분석은 **30 %** 를 썼다 — 권고와 실행이 다르다.)

---

## 6. ★★ Nernst–Einstein vs 집단(collective) 전도도 · Haven 비 — 절 통째로

### 6.1 세 가지 추정량의 정의

**(a) Nernst–Einstein** (Eq. 1) — self-diffusion 만:

```
σ_NE = e²/(V k_B T) · Σ_k z_k² N_k D_k = Σ_k σ_k^self
```

D_k 는 MSD 기울기(Einstein) 또는 VACF 적분(GK) 어느 쪽으로 얻어도 된다 (SI Eq. S1–S3).
저자 표현: *"well suited for dilute electrolyte solutions in which the correlated movement of ions is negligible."*

**(b) Einstein–Helfand** (Eq. 2–3) — 집단 MSD 의 장시간 기울기:

```
σ_EH = e²/(6 V k_B T) · lim(τ→∞) ∂/∂τ ⟨‖ Σᵢ zᵢ Δr⃗ᵢ(t,τ) ‖² ⟩_t
```

naive 하게는 O(N²) 인데 `Σᵢⱼ v⃗ᵢ·v⃗ⱼ = ‖Σᵢ v⃗ᵢ‖²` 항등식으로 **O(N) 로 떨어뜨린다**.
전체 분해는 `σ_tot = σ₊^self + σ₋^self + σ₊₊^cross + σ₋₋^cross + σ₊₋^cross` (Eq. 4),
종별 집단항 `σ_k^EH = σ_k^self + σ_kk^cross` (Eq. 5), 쌍 기여 `σ_kl^EH` 로부터 `σ_kl^cross = σ_kl^EH − σ_k^EH − σ_l^EH` (Eq. 8).
**전체 분해 복잡도 O(C² N T_max)** (C = 이온종 수).

**(c) Green–Kubo** (Eq. 9) — 전하전류 자기상관 적분:

```
σ_GK = e²/(3 k_B T V) ∫₀^∞ ⟨J⃗(t+τ)·J⃗(t)⟩_t dτ,   J⃗(t) = Σᵢ zᵢ v⃗ᵢ(t)
```

- EH 는 **연속(unwrapped) 좌표**가 필요하고 **긴 궤적**이 필요하다
- GK 는 unwrapped 가 필요 없지만 **fs 단위 속도 저장**이 필요하다 → **디스크가 병목** (Table S22 의 10 ns·20 fs 궤적이 **900 GB**)
- 무한시간 극한에서 **형식적으로 동등**. 유한궤적에서 갈리는 것은 **표본 품질과 plateau/창 선택 규약** 때문 (Table S23 이 이를 실증)

### 6.2 역 Haven 비 = ionicity

```
H⁻¹ = σ_tot / σ_NE        (Eq. 16)
```

저자는 이것을 **ionicity** 라 부른다. 1 이면 무상관, 1 보다 작으면 상관이 σ 를 깎는다.

**측정값** (Table S8, S9 · `Fig. S1` 로 확인):

| 계 | EH ionicity | GK ionicity | → **H_R = 1/ionicity** |
|---|---|---|---|
| IL¹²⁵ | 0.760 ± 0.066 | 0.641 ± 0.239 | 1.32 |
| IL²⁵⁰ | 0.678 ± 0.059 | 0.556 ± 0.163 | 1.47 |
| IL⁵⁰⁰ | 0.619 ± 0.049 | 0.662 ± 0.157 | 1.62 |
| IL¹⁰⁰⁰ | 0.702 ± 0.037 | 0.714 ± 0.135 | 1.42 |
| **IL¹⁰⁰⁰_pol** | **0.542 ± 0.025** | 0.619 ± 0.201 | **1.85** |
| LiFSI 1.0 M | 0.610 ± 0.058 | 0.779 ± 0.187 | 1.64 |
| **LiFSI 2.0 M** | **0.480 ± 0.033** | 0.427 ± 0.172 | **2.08** |
| LiFSI 3.5 M | 0.532 ± 0.027 | 0.614 ± 0.174 | 1.88 |

저자 관찰:
1. **전부 1 보다 한참 작다** — 단일입자 이동도의 상당 부분이 거시 전하수송에 기여하지 않는다.
2. **크기 의존 추세 없음** (IL 시리즈 0.62–0.76 사이에서 요동) — 자리 무질서/유한크기가 *비이상성의 정도* 는 크게 바꾸지 않았다.
3. **분극 힘장이 ionicity 를 크게 떨어뜨린다** (0.702 → 0.542) — 단일입자가 빨라진 만큼 상관도 강해졌다.
4. **농도 의존이 단조가 아니다** (0.61 → 0.48 → 0.53) — 저자도 3.5 M 의 재상승은 *"cleanly resolved trend"* 가 아니라 *"tendency"* 라고만 한다.
5. ionicity 의 SE 는 σ_NE 의 SE 보다 훨씬 크다 — **cross 항을 통해 들어오기 때문**.

### 6.3 ⚠⚠ 우리 계와의 **부호 충돌** (이건 내 대조지 두 논문의 주장이 아니다)

우리 쪽 규율 근거인 `adeli2019` 는 **Haven 비 H_R = D\*/D_σ ≈ 0.23–0.3** 을 argyrodite 에서 측정했다.
정의상 `H_R < 1` ⇒ `D_σ > D*` ⇒ **실측 σ 가 tracer 기반 σ_NE 보다 크다** (ionicity ≈ 3.3–4.3).
이 논문(액체)은 정반대로 **ionicity 0.48–0.76 (H_R 1.3–2.1)** ⇒ **σ_NE 가 참값보다 크다**.

⇒ **NE 오차의 부호가 재료계에 따라 뒤집힌다.**

| | ionicity = σ_tot/σ_NE | H_R = 1/ionicity | NE 는 |
|---|---|---|---|
| **이 논문** (IL·농축 액체전해질) | **0.48–0.76** | 1.3–2.1 | **과대** |
| **adeli2019** (Li₆₋ₓPS₅₋ₓCl₁₊ₓ, 실측) | ≈3.3–4.3 (환산) | **0.23–0.3** | **과소** |

⚠ 두 겹의 주의:
- adeli 의 H_R 은 **캐리어 수 규약 c = 4/cell 을 명시적 하한**으로 잡은 값이라 절대값이 규약 의존이다 (그 digest §3c). c 를 크게 잡으면 D_σ 가 작아지고 H_R 이 커진다.
- 이 논문의 ionicity 는 **전 이온이 캐리어**인 액체라 그 모호성이 없다.
⇒ 그래서 결론은 *"우리 계에서 NE 가 과소다"* 가 **아니라**, **"H_R = 1 은 근사가 아니라 미측정이고, 오차의 부호조차 우리 계에서는 확정돼 있지 않다"** 이다.
이건 `σ 절대값 인용 금지` 규율을 **강화**하는 방향이다.

### 6.4 좌표계 — 무엇이 안전하고 무엇이 아닌가

저자가 §2.2 에서 증명:
- **총 전도도는 좌표계 무관** — 전하중성 `Σᵢ zᵢ = 0` 에서 바로 나온다 (Eq. 22, 23). 기준점 이동항이 `Σᵢ zᵢ` 를 곱해 사라진다.
- **self 항은 열역학 극한에서만 무관** — 보정항이 O(1/N) (Eq. 24). 유한 셀에서는 self D 도 좌표계에 의존한다.
- **cross 항과 거기서 나오는 수송수는 열역학 극한에서도 좌표계 의존** — 안전한 양이 아니다.

⇒ **인용해도 되는 것: σ_tot, D_k(큰 N).  인용 전에 좌표계를 반드시 밝혀야 하는 것: 모든 cross 항, 모든 real transport number.**

---

## 7. ★ 독립 궤적 · 시드 — 몇 개가, 왜

### 7.1 그들이 쓴 수

**조건마다 replica 10개.** 그게 전부다 — **최소 개수를 처방하지 않는다.**
원문: *"the number of replicas, system size, simulation length, and the correlation depths, may depend on the simulated system and its thermodynamical state"*,
그리고 결론에서 *"these variables should be defined independently for every simulated material."*

### 7.2 "independent" 의 정의 (이게 중요하다)

의뢰가 인용한 문구는 §2.3.1 에 있다 — 가중평균 Eq. (25) 가 성립하기 위한 **전제**로 등장한다:

> *"assuming the different replicas are statistically independent (i.e., generated from **distinct initial configurations and/or velocity seeds**)"*

그런데 실제 프로토콜(SI §S3.2)은 그보다 강하다:
**10개의 서로 다른 PACKMOL 박스**를 만들고, 각각 700 K(또는 500 K) 융해 → 냉각 → NpT 를 태운다.
⇒ **배열도 다르고 속도도 다르다.** 다만 **밀도는 별도 5-박스 계산의 평균 부피로 통일**한다 — replica 분산에서 밀도 항을 일부러 뺐다.

> 🔑 우리에게 옮길 수 있는 설계: **"시드만 바꾼 3개"보다 "구조를 새로 만든 3개"가 훨씬 강한 replica 다.**
>
> ✅ **확인함 (2026-09-09)**: 우리 comp1 3-seed 는 **속도 시드만 다르다.**
> `tools/ionic/run_comp1_seeds.sh` 가 모든 시드에 **같은 `--v0_xyz` 구조**를 주고 `--n_configs 1 --disorder_levels 0.0` 으로
> 배열을 하나로 고정한 채 `--seed {2,3}` 만 바꾼다 (deck 궤적이 seed 1234 로 1번 역할).
> ⇒ 이 논문 기준으로 우리 3-seed 는 **"distinct velocity seeds" 조건은 만족하지만 "distinct initial configurations" 는 아니다.**
> §2.3.1 의 문구는 *"and/or"* 라 형식적으로는 통과하지만, `Fig. 7`·`Table 3` 이 보여준 **위상공간 피복 문제는 배열 다양성에서 오는 것**이므로
> 우리 오차막대는 **이 논문의 within-replica 쪽에 가깝게** 읽어야 한다.

### 7.3 왜 필요한가 — 기구(mechanism)

저자 논증:
> *"a single long trajectory is able to capture many configurations, [but] it is still constrained by the kinetics that limit finite simulations to a small part of the total phase space."*
> *"Smaller uncertainties within single replicas should therefore **not** be understood as more precise estimations but rather as an expression of the partially underestimated uncertainties and limited phase space coverage."*

그리고 집단 물성에 특히 그렇다:
> *"In particular for collective transport properties that are sensitive to rare and long-range correlated movement patterns, broad sampling of the phase space is of higher importance than refining local patterns within a single trajectory."*

### 7.4 replica 를 합치는 두 경로 (`Fig. 1` 하단 워크플로)

**(A) fit-first** — replica 마다 σ_r 과 Δσ_r 을 얻고 가중평균:

```
σ_eff = Σ_r w_r σ_r / Σ_r w_r,   w_r = 1/(Δσ_r)²          (Eq. 25)
Δσ_eff = sqrt(1/Σ_r w_r)                                    (Eq. 26)
Δσ_eff,scaled = Δσ_eff · sqrt(χ²_red),  χ²_red = Σ_r w_r(σ_r−σ_eff)²/(N_r−1)   (Eq. 27)
```

**χ²_red 재조정**이 핵심 장치다 — replica 산포가 각자의 Δσ_r 보다 크면 오차막대를 **자동으로 키운다**.

**(B) average-first** — MSD_col(τ) 를 replica 에 걸쳐 (역분산) 가중평균한 뒤 창 검출 + 가중적합.
개별 replica 의 CMSD 가 너무 시끄러워 선형영역을 못 찾을 때 우월하다.

**둘의 판정** (`Fig. 6` 상단):
- 평균값은 사실상 같다 (1.0 M: 2.14 vs 2.03 / 2.0 M: 1.35 vs 1.34 / 3.5 M: 0.42 vs 0.41)
- **차이는 오차막대에 있다.** 원문: *"Processing replicas individually or using bootstrap sampling yields a meaningful standard error, whereas processing the averaged CMSD or CACF does not."*
- **부트스트랩**(replica 복원추출)이 둘 다 개선한다. GK 는 부트스트랩이 실험 기준값에 가장 잘 맞았다.

---

## 8. 적합 구간 · 시간원점 — 권고와, **없는 것**

### 8.1 EH 창 검출 알고리즘

`d log MSD_col / d log τ` 를 슬라이딩 윈도로 계산해 **기울기가 1 에 가까운 구간을 확산영역으로 분류**하고, 최소 구간 길이를 요구한다 (MSDiff v0.2.0, Frömbgen 2025 = ref [26]).

### 8.2 GK plateau 검출 알고리즘

1. 적분곡선을 `nslice` 구간으로 나누고 **장시간 → 단시간 방향**으로 훑는다
2. `|dI/dτ| < tol` 이면 plateau 후보
3. 후보를 `incr` 만큼 **단시간 쪽으로 반복 확장** (기울기가 tol 안에 머무는 한)
4. **데이터점이 가장 많은 후보**를 채택 (동률이면 |기울기| 작은 쪽)
5. 못 찾으면 `tol` 을 키워 다시
6. 단시간 상관영역을 잘못 잡지 않도록 **첫 구간은 버린다**

⚠ **`nslice` · `tol` · `incr` 의 수치가 논문·SI 어디에도 없다.** "사용자 편향 제거" 를 표방하는데 재현에 필요한 상수를 안 준다 (§16-3 비판).

### 8.3 권고 수치 (그대로)

| 항목 | 권고 / 실행 |
|---|---|
| EH 최대 상관깊이 | **권고: 궤적의 10 %** (*"10 ns with good sampling, 10 % of the total simulation length"*) · **실행: 30 %** (30 ns / 100 ns) |
| GK 상관깊이 | 75 ps / 100 ps 궤적 |
| GK 속도 덤프 | **1 fs** (*"to be certain that no significant contributions were missed"*; 최대 허용 간격은 계 의존) |
| 자동 창 실측 | 1.0 M **60 ps–24 ns** · 2.0 M **60 ps–25.5 ns** · 3.5 M **360 ps–16.5 ns** |
| 단일 replica GK | TRAVIS 기본 = **적분의 마지막 1/3 평균** — 저자 스스로 *"crude estimate"* 이자 *"only if there is not more than one replica available"* 로 한정 |

### 8.4 ★ 시간원점(time origin) — **정량이 없다**

의뢰 4번의 *"단일 시간원점이 얼마나 나쁜지 정량"* 은 **이 논문에 없다.** 시간원점 개수를 스캔한 실험이 0건이다. 정직하게 적는다.

**대신 이 논문이 주는 것 두 가지:**

1. **다중 시간원점의 산포를 가중치로 쓴다.** §2.3.1 원문 —
   *"the weights are the inverse of the squared standard errors ΔMSD_col_r(τ), estimated from the fluctuations of MSD_col_r(τ) **over different time origins**"*
   ⇒ 시간원점이 하나면 **ΔMSD(τ) 를 만들 재료 자체가 없다** → 오차가중 적합이 불가능하고, 자동 창 검출의 신뢰구간도 정의되지 않는다.
   이것이 "단일 원점이 나쁘다"의 **구조적 근거**다 (수치가 아니라).

2. **`Fig. S12` 의 CMSD 하강** (figure-read, §5.2) — 긴 lag 에서 원점 수가 마르면 평균 MSD 가 **감소**하는 비물리가 나타난다.
   원점 수가 애초에 1이면 이 붕괴가 **모든 τ 에서** 일어나고 있는 셈인데, 곡선이 이상해 보이지 않아 **탐지되지 않는다.**

> 🔑 요약: 이 논문은 "단일 원점 = N배 나쁘다"를 안 준다. 주는 것은 **"단일 원점이면 이 논문의 권장 절차(오차가중·자동창·χ²_red)를 아예 실행할 수 없다"** 이다. 우리 파이프라인 판정에는 이걸로 충분하다.

---

## 9. ★ 셀 크기 의존

### 9.1 self 는 걸린다

- 음이온 D: **1.8807 → 2.0452** (125→1000 쌍) = **+8.8 %**, 오차막대(≈0.02)를 압도
- 양이온 D: **1.6100 → 1.7747** = **+10.2 %**
- Yeh–Hummer 보정 `ΔD_YH = 2.837297 k_BT/(6πηL)`: IL 0.4813 → 0.2407 (D 의 **26 % → 12 %**), LiFSI 는 **29–41 %**
- 이온 self 전도도도 같이 오른다: 양이온 self **3.143 → 3.409**, 총 self **6.820 → 7.350**

### 9.2 total 은 안 걸린다 (검출이 안 된다)

- IL total σ_EH: **5.184 / 4.753 / 4.473 / 5.163** (125/250/500/1000) — **단조가 아니고 오차막대가 겹친다**
- cross 합: **−1.636 / −2.258 / −2.757 / −2.187** — 크기가 커지며 (적어도 500 까지) 더 음수로
- 양이온 cross (오차막대가 작아 판정 가능): **−2.416 → −2.689** (SE 최대 ±0.07), 저자 서술 *"from around −2.4 to −2.7 S m⁻¹"*
- 양이온 self+cross: **0.62–0.73 S m⁻¹ 범위에서 추세 없음** (본문 수치)

⇒ 저자 결론: **self 의 크기 편향을 cross 가 (부분적으로) 상쇄한다** ⇒
*"possible finite size effects in the total conductivity are much harder to resolve than in the self-diffusion coefficients."*
그리고 확정하려면 *"even more extensive sampling ... is required"* 라고 스스로 유보한다.

### 9.3 ionicity 는 크기에 둔감

0.760 / 0.726 / 0.678 / 0.619 / 0.702 — **명확한 추세 없이 0.62–0.76 사이 요동**.
저자 해석: 유한크기가 남아 있어도 *"비이상성의 정도"* 자체는 크게 안 바뀐다. (단, 오차막대를 보면 더 많은 표본이 필요하다고 인정)

> ⚠ **우리에게 직접 걸리는 곳**: D 는 셀 크기에 **+9–10 %** 움직인다. 우리가 Stage 10 을 **D_tr 랭킹**으로 바꾸면
> **모든 후보계의 셀 크기(원자 수)를 동일하게 고정**하지 않는 한 이 편향이 순위에 들어온다. 새 요구사항이다.

---

## 10. Figure set ★

> **본 것 / 안 본 것을 구분한다.** 아래 표에서 **👁 = 실제로 PNG 를 Read 로 봄**, **📄 = 캡션·본문·SI 표 텍스트만**.
> 크로핑 총 **47장** = 그림 PNG **22장**(본문 8 + SI 14) + 표 PNG **25장**. 그중 **실제로 본 것은 그림 9장(논문 그림 10개)**. 자세한 내역은 §18.

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1 | 👁 (상) [EMIm]⁺·[DCA]⁻·DME·[FSI]⁻ 분자 그림 · **(하) EH 워크플로 흐름도** — replica 10개 → CMSD_r(τ)+ΔMSD_r(τ) → **(A) fit-first**(빨강, σ_r,Δσ_r → σ_eff,Δσ_eff,scaled) vs **(B) average-first**(파랑, MSD_eff → σ_avg) | **하단 흐름도가 이 논문의 실사용 산출물** — 우리 σ/D 파이프라인을 이 두 갈래 중 어디에 놓을지 결정하는 그림. 우리는 지금 (A) 도 (B) 도 아니고 "replica 1개" 다 |
| 2 | 👁 EH·GK·EH-NE·GK-NE 를 실험선(파선)과 나란히. (상) IL¹⁰⁰⁰ CL&P vs CL&Pol, (하) LiFSI/DME 3농도. **NE 막대가 항상 집단 막대보다 높다** | **F1 의 정본 그림.** ⚠ 동시에 §16-1 비판의 근거 — IL 에서는 **NE 막대가 실험선에 더 가깝다** |
| 3 | 📄 이상 수송수 (cation/anion), IL 전 계 + LiFSI 3농도, EH(민무늬)/GK(빗금) | 우리 계는 가동 이온이 Li 하나라 **직접 대응물이 없다** — 안 봤고 안 쓴다 |
| 4 | 📄 실 수송수 × 3 좌표계 × EH/GK (LiFSI/DME) | 좌표계 의존의 그림 근거. 수치는 `Table S13` 이 더 정확 |
| 5 | 👁 (fig_6.png 좌반부에 같이 잘렸다) GK CACF 적분 곡선, 1.0 M / 3.5 M. 검정=평균, 컬러=개별 replica 이동평균(200 fs 창). y축 −10~15 S m⁻¹ | **F3·F5 의 가장 강한 시각 증거** — 1.0 M 개별 replica 가 **−5 ~ +12 S m⁻¹** 를 헤맨다(figure-read). *replica 하나면 음의 σ 도 나온다* |
| 6 | 👁 (상 EH) Auto Fit→Avg / Avg→Auto Fit / **Tail Fit→Avg / Avg→Tail Fit** 4종, (하 GK) Bootstrap / Single Search / Tail Average 3종 × 3농도 | **★★ F2 의 정본.** 우리 `fit_start = n_frames//2` 가 바로 "Tail Fit" 이다 |
| 7 | 👁 IL¹⁰⁰⁰ 에서 **within-replica 평균(파랑)** vs **between-replica 평균(빨강)** 을 index 1–10 에 대해. y 4.00–5.50 S m⁻¹ | **★★ F3 의 정본.** 파랑=값 넓고 오차막대 좁음 / 빨강=값 좁고 오차막대 넓음 — *"작은 오차막대 = 정확"이 아니다* |
| 8 | 👁 IL¹⁰⁰⁰_pol, 상관깊이 1–30 ns 에 대한 σ_EH·σ_NE·σ₊₋^cross (상) 와 그 SE (하). y축 축약(break) 3단 | **★★ F4 + §13 근거.** σ_NE 는 평평하고 SE 가 한 자릿수 작다 = *"self 량이 재현 가능한 양이다"* |
| 9 | 👁 (좌) total σ 의 self/total/cross 3단 분해 vs 계 크기 125–1000, (우) 양이온 self/self+cross/cross | **★ F7 정본.** self 는 단조·오차 작음 / total 은 추세 없음·오차 큼 / cross 가 상쇄 |
| S1 | 👁 ionicity(=H⁻¹) 막대, IL 6계 + LiFSI 3농도, EH(파랑)/GK(주황) | **★★ Haven 절의 그림.** 전부 1 아래, GK 오차막대가 EH 의 3–8배 |
| S2, S4 | 📄 CACF 원곡선 (LiFSI 3농도 / IL 계열) | 필요시 참조 |
| S9 | 📄 전 계 self-diffusion 막대그래프 | 수치는 `Table 1`·`Table 2` |
| S10 | 👁 LiFSI/DME 3농도 CMSD — 개별 replica(컬러 점선) + 평균(검정) | **★★ F3 보강.** 1.0 M τ=30 ns 에서 replica 가 ≈16–123 ×10³ 로 **8배** 흩어진다(figure-read) |
| S11 | 📄 IL 계열 CMSD (replica + 평균) | 같은 메시지 |
| S12 | 👁 1.0 M CMSD 에 **Auto Fit(파랑) vs Tail Fit(빨강)** 을 겹쳐 그림 | **★★★ F2 의 기구를 보여주는 그림.** 평균 CMSD 가 τ≳27 ns 에서 **하강**(figure-read) = 후반부는 확산영역이 아니다 |
| S13, S14 | 📄 같은 그림의 2.0 M / 3.5 M 판 (수치는 캡션에) | 자동창 1.34/0.41 vs tail 0.85/0.22 |
| S15, S16 | 📄 within vs between replica (LiFSI 3농도 / IL 계열) — `Fig. 7` 의 확장 | `Table 3` 이 정량 |
| S17 | 📄 LiFSI 3농도 상관깊이 스캔 (`Fig. 8` 의 LiFSI 판) | y축 범위: 1.0 M σ_EH 2.00–2.25, SE 0–0.24 |
| S19, S20 | 📄 EH/GK 분해 vs 계 크기 (`Fig. 9` 의 확장) | 수치는 `Table S14`–`S21` |
| S3, S5–S8, S18 | ⛔ **크로핑 실패** — 추출기가 "그래픽 없음"으로 6건 제외. S18(전 계 상관깊이 종합)은 우리가 보고 싶었던 그림이라 **공백으로 남는다** | §17 에 기록 |
| `Table 1`–`Table 3`, `Table S2`–`Table S23` | 📄 표 25장은 PNG 로 안 봤다 (**PDF 텍스트가 정확**) — 수치는 §3 에 전사 | 우리 관례대로 |

---

## 11. Post-processing ★

- **무엇**: 집단 MSD(CMSD) 선형회귀(EH) · 전하전류 자기상관 FFT + 수치적분 plateau(GK) · self/cross 분해 · 수송수 · 역 Haven 비 · 좌표계 변환. **NEB·Bader·COHP·DOS·ELF·ESW 는 전부 없다** (전자구조 계산 자체가 없다).
- **도구**:
  - **TRAVIS `conduct` 모듈** (신규) — `.lmp`/`.gro`/`.xyz` 를 읽고 **좌표계 변환을 on-the-fly** 로 처리 (전처리 불필요). 단일 궤적 최적화.
  - **MSDiff v0.2.0** — 로그기울기 기반 선형영역 검출
  - **자체 Python 스크립트** (`kirchners-manta/conductivity_tools`) — replica 여러 개를 합치는 부분 (TRAVIS 가 단일 궤적용이라)
  - **LAMMPS 23Jun2022**, PACKMOL, `fftool`, `polarizer`
- **수치화 방식**:
  - CACF 는 **FFT** 로 계산
  - **GK 단일궤적 SE**: 적분값을 유한차분 `D_i = I_{i+1} − I_i` 으로 재표현하고, `D_i` 의 **표본 자기공분산 γ_D(h)** 로 평균의 분산을 조립 (SI Eq. S5–S9). 가중치 `w_i = (n−i)/n`.
    ```
    Var(Ī) = γ_D(0) Σᵢ wᵢ² + 2 Σ_h γ_D(h) c_h ,  c_h = Σᵢ wᵢ wᵢ₊ₕ
    ```
    가정: `I₁` 은 상수 오프셋, `D_i` 는 2차 정상(second-order stationary).
  - **replica 결합**: 역분산 가중평균 + **χ²_red 재조정**(Eq. 27) + **부트스트랩**(복원추출)
  - **대안 언급만**: Cesàro 합, KUTE 의 불확실도 가중 running-integral, STACIE 류 zero-frequency 파워스펙트럼 — **비교 실험은 안 함**
- **기록**: 본문 그림 9장 + SI 그림 20장 + SI 표 23개. 원시 데이터는 **저장소 공개 없이 요청 시 제공**.

---

## 12. ★★★ 우리 σ 파이프라인 항목별 판정

> 우리 규약(CLAUDE.md): UMA-s-1p1(omat) · Langevin NVT · dt 2 fs · friction 0.02 · equil 5 ps / prod 200 ps ·
> **MSD 창 2–50 ps 자유절편** · 시드 3 · Arrhenius 600/800/1000 K · **σ = Nernst–Einstein(H_R=1)** · σ 절대값 인용 금지.
> 실행 코드: `tools/doping/run_md_sigma.py` (§L136 `fit_start = n_frames // 2`).

| 우리 요소 | 이 논문 기준 | **판정** |
|---|---|---|
| **σ = NE, H_R = 1** | 이 논문 계에서 NE 는 **1.31–2.08× 과대**, 그 인자가 조성/힘장에 따라 **0.48–0.76** 으로 변동 | 🟡 **부분 생존.** ⛔ *"우리 σ 는 NE 라 x배 과대"* 는 **못 쓴다**(재료계 다름 + adeli 는 반대 부호). ✅ 쓸 수 있는 것은 **"H_R=1 은 보정이 아니라 미측정이고 오차의 부호도 우리 계에서 미확정"** — 우리 `σ 절대값 인용 금지` 를 **강화** |
| **`fit_start = n_frames//2`** (후반 절반 적합) | **정확히 이 논문이 반증한 "Tail Fit"** (`Fig. 6`, `Fig. S12`) | 🔴 **직격.** 방향은 **과소**. ⛔ 단 **2.8× 라는 크기는 못 가져온다** — 그건 *집단* MSD 값이고, 우리 것은 *self* MSD 다(§16-2). 크기 미상, 방향만 확정 |
| **단일 시간원점** (`msd = ⟨‖r(t)−r(0)‖²⟩`) | 그들은 다중 원점 + **그 산포를 가중치로** | 🔴 **죽는다.** 정량 페널티는 이 논문에 없지만(§8.4), **오차가중 적합·자동창·χ²_red 를 실행할 재료가 아예 없다.** 게다가 `linregress` 의 SE 는 점들이 강하게 상관돼 있어 의미가 없다(→ `pranami2015` 가 정본) |
| **MSD 창 2–50 ps 고정** (정본 규약) | 고정창도 *"may still yield acceptable estimates if the chosen window appropriately captures the diffusive regime"* — 단 *"the optimal window location is system dependent"* | 🟡 **조건부 생존.** 창을 계마다 검증하지 않는 것이 문제다. **최소 처방: 계마다 `d log MSD / d log τ ≈ 1` 을 한 번은 확인** |
| ⚠ **정본 규약(2–50 ps)과 실행 코드(후반 절반)의 불일치** | — | 🔴 **이 논문과 무관하게 우리 내부 결함 — 그리고 경로마다 다르다.** ✅ 확인: **이온 캠페인 경로**(`run_comp1_seeds.sh` → driver)는 `--fit_window_ps 2 50` 으로 **정본 창을 쓴다.** 어긋난 것은 **도핑/σ 경로**(`tools/doping/run_md_sigma.py:136`)뿐이다. ⇒ 같은 repo 안에서 **두 개의 D 정의가 공존**한다. `tools/convention_check.py` 대상 |
| **prod 200 ps** | EH 100 ns (500×), GK 100 ps + 1 fs 덤프 | 🔴 **집단 σ 는 불가.** 200 ps 로 CMSD 확산영역을 잡는 것은 이 논문 기준 논외. 🟡 **tracer D 는 다른 이야기** — 그들 데이터에서 self 량은 훨씬 빨리 수렴(§5.4) |
| **시드 3** (600 K 만) | replica **10개**, 그리고 단일 궤적 분할은 SE 를 **1.33–1.52× 과소** | 🟡 **self 량이면 부분 생존, 집단 σ 면 사망.** ✅ 확인: 우리 3-seed 는 **같은 구조 + 속도 시드만** 다르다 (`run_comp1_seeds.sh` — 동일 `--v0_xyz`, `--n_configs 1`) → 이 논문의 *"distinct initial configurations"* 조건 미충족 ⇒ **우리 오차막대를 낙관치로 읽어야 한다**(§7.2) |
| **modelc 3-seed Ea 0.197 ± 0.032 eV** | χ²_red 재조정 같은 장치 없음 | 🟡 **오차막대의 방향만 지적 가능.** 3 점이면 χ²_red 도 통계가 부족하다. ⛔ 이 논문으로 우리 Ea 를 재계산하거나 오차를 재산정할 근거는 없다 |
| **Langevin NVT (friction 0.02)** | 그들은 전부 **Nosé–Hoover 계열** (TGNH) | ⚠ **이 논문이 다루지 않는 위험.** Langevin 은 **운동량을 보존하지 않는다** → 집단 전하전류 J⃗ 에 열욕이 직접 개입한다. **⚠ 이건 내 지적이지 논문 주장이 아니다.** self MSD 에는 영향이 훨씬 작다 ⇒ **우리가 집단 σ 로 가려면 먼저 풀어야 할 문제** |
| **dt 2 fs** | dt 1 fs, GK 는 1 fs 저장 | 🟡 self D 에는 무해. **GK 를 하려면 fs 급 속도 저장이 필요**한데 우리 파이프라인은 그걸 안 남긴다 |
| **셀 크기 고정 여부** | D 가 **125→1000 쌍에서 +9–10 %**, YH 보정 +12–41 % | 🔴 **새 요구사항.** 도펀트 랭킹을 D 로 하려면 **후보계 원자 수를 통일**해야 한다. 지금 이 제약이 명시돼 있지 않다 |
| **σ 절대값 인용 금지** | NE 오차 1.3–2.1× + 힘장 오차 25–30 % + **실험 기준값 자체가 ±13 %** | ✅ **강하게 지지.** 이 논문 저자들도 σ 절대값을 실험과 맞추는 데 실패했고 그것을 힘장 탓으로 돌린다 |
| **비율도 멀티시드 판정만** | replica 간 산포가 계통 차이를 압도할 수 있음(`Fig. 7`: ±13 %) | ✅ **지지** |
| **UMA / MLIP** | MLIP 를 서론에서 언급만 (ref [66,67]) — **비교 실험 없음** | 중립. 이 논문은 MLIP 의 σ 를 검증하지 않는다 |
| **아레니우스 600/800/1000 K** | 온도 스캔 **없음** (단일 온도) | 중립. 이 논문은 Ea 를 다루지 않는다 |

---

## 13. ★★★ Stage 10 판정 — σ 를 랭킹 축에서 빼고 D_tr(600 K) 로 갈 것인가

**결론: 이 논문은 그 전환을 *지지한다* — 단 근거의 모양이 우리가 기대한 것과 다르다.**

### 지지하는 근거 (3개)

**① self 량이 집단 량보다 압도적으로 재현 가능하다 — 이 논문이 직접 잰다.**
`Fig. 8` (figure-read): 상관깊이 1→30 ns 에서 σ_EH 는 −8 % 움직이고 SE 가 **×3.1**(0.07→0.22) 인데,
σ_NE 는 −1.8 % 이고 SE 가 **≈0.02 로 평평**하다. 즉 **self 기반 양의 SE 가 집단 양의 1/10**.
`Fig. 9` 도 같다 — self 항은 오차막대가 작아 크기 추세를 **판정할 수 있고**, total 은 **판정할 수 없다**.
⇒ **"랭킹을 하려면 판정 가능한 양으로 해야 한다"** 는 요구에 대해 이 논문은 self/tracer 쪽 손을 든다.

**② NE 보정 인자가 조성에 따라 변한다 — 랭킹에 계통편차가 섞인다.**
ionicity 가 IL 0.542–0.760, LiFSI 0.480–0.610 로 **같은 물질계 안에서도 힘장·농도에 따라 1.4배 범위**로 움직인다.
이것은 `adeli2019` 의 *"Cl 함량 x=0→0.5 에서 H_R 이 1.34배 변한다"* 와 **같은 종류의 논증을 계산 쪽에서 반복**한 것이다.
⇒ H_R=1 로 고정한 σ 로 도펀트를 줄 세우면, **순위 차이 안에 미지의 조성 의존 인자가 들어 있다.**
(⚠ 1.4배·1.34배라는 *수치* 는 각각 그 논문의 계 값이고 우리 계 값이 아니다 — **논증 구조만** 가져온다.)

**③ 우리 예산으로는 집단 σ 가 애초에 정의되지 않는다.**
집단 σ 를 제대로 내려면 이 논문이 요구하는 것: **독립 replica 10개 × 100 ns + 자동 확산영역 검출 + 다중 시간원점 오차가중 + χ²_red/부트스트랩**.
우리는 **replica 1개(온도당) × 200 ps + 후반 절반 고정창 + 단일 시간원점**이다.
⇒ 보고량 규율(`kb/methodology/estimand_before_running_2026_08_28.md`) 언어로: **집계 규칙이 없는 상태에서 스칼라 σ 를 보고하고 있다.**

### 반대/중립 요소 (정직하게)

- **이 논문은 σ 를 버리라고 하지 않는다.** 정반대로 **σ 를 제대로 내는 도구를 만든** 논문이다.
  ⇒ 우리가 이걸 근거로 쓸 때는 **"σ 가 나쁜 양이다"가 아니라 "우리 예산에서 σ 는 정의된 보고량이 아니다"** 로만 써야 한다. 그 구분을 흐리면 over-claim 이다.
- **D_tr 도 공짜가 아니다.** 셀 크기에 **+9–10 %**, YH 보정이 **12–41 %** 다.
  ⇒ D_tr 랭킹으로 가면 **후보계 원자 수 통일**이라는 새 제약이 생긴다. 지금 cascade 에 그 제약이 없다.
- **재료계가 다르다.** 이 논문의 self/집단 대비는 **액체 · 두 종의 가동 이온 · 353/333 K** 에서 얻은 것이다.
  우리는 **결정 골격 안의 Li 단일 가동종 · 600–1000 K** 다. 골격이 고정된 계에서는 cross 항의 구조가 다르다
  (그들 계에서는 반대 부호 이온이 함께 움직여 σ 를 깎는데, argyrodite 에서는 Li–Li 협동 이동이 σ 를 **키울** 수 있다 — 그게 adeli 의 H_R<1 이다).
  ⇒ **"NE 가 과대"를 우리 계로 옮기면 안 된다.**

### 한 줄 판정

> **지지 (조건부).** 이 논문은 *"σ 를 쓰지 마라"* 가 아니라 *"σ 는 집단량이라 이만큼의 통계 예산을 요구한다"* 를 말한다.
> 우리 Stage 10 은 그 예산의 **1/500 (200 ps vs 100 ns) · 1/10 (replica 1 vs 10)** 이고 게다가 **반증된 tail 적합 + 단일 시간원점**을 쓴다.
> ⇒ **σ 를 랭킹 축에서 빼는 결정을 이 논문이 뒷받침한다.** 다만 문장은
> *"NE 가 틀려서"* 가 아니라 ***"우리 계산 예산에서 σ 는 정의된 보고량이 아니고, 같은 궤적에서 D_tr 은 정의된다"*** 여야 한다.

---

## 14. 적용 인사이트 (계산 0회로 지금 되는 것부터)

**T0 — 코드 한 줄 (계산 0회).**
`tools/doping/run_md_sigma.py:136` 의 `fit_start = n_frames // 2` 는 이 논문이 반증한 **Tail Fit** 이다.
정본 규약(2–50 ps)과도 어긋난다. **최소 조치**: 정본 창으로 통일하고 `tools/convention_check.py` 로 갈라짐 확인.

**T0b — 진단 한 장 (계산 0회, 기존 궤적 재분석).**
이미 저장된 `msd_<T>K.dat` 로 **`d log MSD / d log τ` 를 그려서 β ≈ 1 구간을 확인**한다.
우리에게 `tools/ionic/msd_diffusive_check.py` 와 `msd_refit_window.py` 가 이미 있다 — 새 도구를 만들 필요가 없다.
이 논문이 주는 것은 그 그림의 **판정 기준**(기울기 1 근방 + 최소 구간 길이)이다.

**T1 — 다중 시간원점 (재분석, MD 재실행 불필요).**
저장된 궤적으로 `⟨‖r(t+τ)−r(t)‖²⟩_t` 를 여러 원점에 걸쳐 다시 만들면
**(a) MSD 가 안정되고 (b) ΔMSD(τ) 가 생겨 오차가중 적합이 가능해진다.**
⚠ `tools/ionic/msd_origin.py` 는 **이름과 달리 "Origin 그래프용 CSV" 도구**다 — 시간원점 도구가 아니다. 확장 대상은 그쪽이 맞다(코드 규율 §사다리 ③).

**T2 — replica 정의 강화.**
이 논문의 replica 는 **구조를 새로 만든** 것이다(§7.2). 우리 3-seed 가 속도만 바꾼 것이라면
그 오차막대는 이 논문 기준 **1.33–1.52× 낙관**이다. ⇒ 최소한 **"우리 seed 가 어떤 종류인지"를 문서에 명시**해야 한다.

**T3 — 집단 σ 는 하지 않는다 (판정).**
EH 를 하려면 100 ns 급 + replica 10, GK 를 하려면 fs 급 속도 저장(그들의 10 ns 궤적이 **900 GB**).
게다가 우리 **Langevin 열욕이 집단 전하전류를 오염**시킬 위험이 있다(§12).
⇒ **집단 σ 는 우리 자원에서 열지 않는다.** 대신 §13 의 D_tr 전환.

---

## 15. 인용 가능 문장 (deck/paper 용)

- "Zaby et al. 은 이온액체와 농축 에테르 전해질에서 Nernst–Einstein 근사가 참 전도도를 **1.3–2.1배 과대평가**함을 보였고(ionicity 0.48–0.76), 그 인자가 힘장·농도에 따라 변한다는 점에서 **NE 기반 σ 는 조성 간 순위 비교에 계통편차를 남긴다**." *(자기 계 값임을 반드시 병기)*
- "집단 전도도의 불확실도는 한 궤적 내부의 요동이 아니라 **독립 replica 사이의 산포**에 지배되며, 긴 단일 궤적을 토막내 얻은 표준오차는 **1.33–1.52배 과소평가**된다 (Zaby 2026, `Table 3`)."
- "집단 MSD 의 **후반부를 적합하는 관행**은 자동 확산영역 검출 대비 전도도를 **최대 2.8배 낮게** 만든다 (Zaby 2026, `Fig. 6`·`Fig. S12`)." *(집단 MSD 에 대한 진술임을 명시)*
- "총 전도도는 좌표계에 무관하지만 cross 항과 수송수는 그렇지 않으며, LiFSI/DME 3.5 M 에서 t(Li⁺) 는 좌표계에 따라 **+0.373 에서 −0.174 까지** 부호가 바뀐다 (Zaby 2026, `Table S13`)."
- "self-diffusion 은 계 크기에 **9–10 % (125→1000 이온쌍)** 반응하지만, 총 전도도의 크기 의존은 cross 항의 상쇄로 **오차 안에서 검출되지 않는다** (Zaby 2026, `Fig. 9`)."
- "분극 힘장은 self-diffusion 을 18–21 % 높이면서도 집단 전도도는 높이지 않았다 — **단일입자 이동도가 거시 수송으로 번역되지 않는다** (Zaby 2026)."

## ⛔ 이 논문에서 인용하면 **안 되는** 것

- **어떤 σ·D 절대값도 우리 계로 옮기는 것.** 계가 이온액체/에테르 액체전해질이고 힘장은 고전 CL&P(ol) 다.
- **"NE 는 σ 를 과대평가한다"를 argyrodite 에 적용하는 것.** `adeli2019` 실측은 **반대 부호**다(§6.3).
- **"2.8배 과소"를 우리 self-MSD D 에 적용하는 것.** 그 수치는 **집단 MSD** 값이다(§16-2).
- **"replica 10개가 필요하다"를 규칙으로 쓰는 것.** 저자가 명시적으로 계마다 다르다고 못박는다.
- **"권고 상관깊이 = 10 %"를 우리 2–50 ps 창의 근거로 쓰는 것.** 그들 궤적은 100 ns 이고 우리는 200 ps 다. 비율만 옮기면 우리 창은 20 ps 가 되는데, 그 산술에는 물리적 근거가 없다.
- **ionicity 0.48–0.76 을 "액체의 보편값"으로 쓰는 것.** 계 2종·온도 1점의 값이다.
- **이 논문을 "MLIP 로 낸 σ 의 검증"으로 쓰는 것.** MLIP 를 서론에서 언급만 하고 실험은 0건이다.

---

## 16. 주의 / 한계

### 16-A. 저자가 스스로 적은 한계

1. *"observed trends should not be interpreted as general trends until more extensive investigations across different systems are carried out"* — **계 2종에서 얻은 교훈이다.**
2. 크기 효과 확정에는 *"even more extensive sampling in the form of additional replicas and/or even longer simulations is required"* — **§9.2 는 미결이다.**
3. 실험과의 불일치는 *"inherent limitations of the underlying force fields and the inaccuracy of the reference data"* 탓 — **분석법 검증이 아니라고 선을 긋는다.**
4. Yeh–Hummer 보정은 *"qualitative approximations"* (점도가 문헌 외삽).
5. LiFSI/DME 실험 기준값이 **직접 측정이 아니라 내삽**이다 — 분리가능성 가정 `σ(c,T) ≈ f(T₀→T)·σ(c,T₀)` + VFT 적합, 불확실도 **±13 %**.
6. 순수 이온액체의 수송수는 *"carry no additional physicochemical meaning"* (좌표계 선택에 따라 질량·부피 분율로 붕괴).
7. GK 단일 replica 자동 plateau 검출은 *"unlikely to return a meaningful time window"*.
8. 이상적인 EH/GK 비교 궤적은 **900 GB 초과**라 replica 를 만들 수 없었다.
9. 데이터가 **저장소에 없다** (요청 시 제공).

### 16-B. 우리가 짚는 한계 (저자 미언급)

1. **★ NE 가 실험에 더 가까운 경우가 다수인데 그것을 이온액체에서는 말하지 않는다.**
   실험 기준선이 있는 5개 비교 중 **3개에서 NE 가 실험에 더 가깝다** (IL CL&P Δ+0.49 vs EH Δ−1.70 / IL CL&Pol Δ+1.96 vs Δ−2.08 / LiFSI 3.5 M Δ−0.17 vs Δ−0.54).
   저자는 **3.5 M 에서만** 오차상쇄를 인정하고, `Fig. 2` 상단에서 똑같이 보이는 현상에는 침묵한다.
   ⇒ 논문의 주장은 *"NE 가 부정확하다"* 가 아니라 정확히는 ***"NE 는 다른 양을 재는 추정량이다"*** 로 읽어야 한다. 정확도 논증으로 읽으면 이 데이터가 안 받쳐준다.
2. **★ 2.8× 라는 숫자는 집단 MSD 에만 해당한다.** self MSD 는 cross 항이 없어 훨씬 매끈하고, 저자 자신의 `Fig. 8` 이 self 량의 창 둔감성을 보여준다.
   ⇒ 우리 tracer D 로 **크기를 옮기는 것은 금지**, 방향만.
3. **★ 자동창 알고리즘의 상수(`nslice`·`tol`·`incr`)가 논문·SI 어디에도 없다.**
   "사용자 편향 제거" 를 표방하면서 재현에 필요한 수를 안 준다. 게다가 선택 규칙이 **"데이터점이 가장 많은 후보"** 라 **길이 최대화 편향**이 내장돼 있다.
4. **★ 자동창이 사실상 "초·중기 적합" 이다.** 1.0 M 에서 검출된 창은 **60 ps – 24 ns** 로 상관깊이의 80 % 를 덮고, 오차가중이 초기를 강하게 편든다.
   `Fig. S12` 를 보면 파랑 Auto Fit 선이 τ ≳ 12 ns 부터 검정 평균곡선 **위로 벗어난다**(figure-read).
   ⇒ 자동창이 실험과 잘 맞는 이유의 일부는 *"장시간을 안 봤기 때문"* 일 수 있다. **저자는 CMSD 하강이 통계 탓인지 진짜 sub-diffusion 인지 구분하지 않는다.**
5. **본문 `Fig. 2` 의 EH–GK 간극은 방법 비교가 아니다.** 서로 다른 궤적 세트(100 ns vs 0.1 ns)를 비교한 것이고, SI §S7.10 에서 스스로 무효화한다.
   그런데 그 사실이 **초록·결론에는 안 들어간다** — 인용될 때 오해되기 좋은 배치다.
6. **replica 밀도를 통일한 것이 replica 분산을 축소한다.** 모든 replica 를 공통 평균 부피로 스케일했으므로, NpT 요동에서 오는 밀도 분산이 오차막대에 안 들어간다.
   실제 물질의 불확실도는 이보다 클 수 있다. 저자는 이것을 *"totally independent"* 의 근거로 제시하지만, 밀도 축에서는 오히려 **덜** 독립이다.
7. **온도 의존이 0이다.** Ea 도, Arrhenius 도 없다. 우리 축(600/800/1000 K 외삽)에 대해서는 아무 말도 하지 않는다.
8. **써모스탯이 집단 전하전류에 미치는 영향을 다루지 않는다.** 전부 Nosé–Hoover 계열이라 문제가 안 됐지만,
   Langevin/확률 열욕을 쓰는 계(우리)로 옮길 때의 경고가 없다.
9. **계 2종 × 온도 1점 × 힘장 2종.** "lessons learned" 라는 제목의 일반성 주장에 비해 표본이 얇다.

---

## 17. 기법 미니 용어집

| 용어 | 뜻 (이 논문 용법) |
|---|---|
| **NE (Nernst–Einstein)** | σ 를 각 이온의 self-diffusion 합으로 근사. ion–ion 상관을 **무시**. Eq. 1 |
| **EH (Einstein–Helfand)** | **집단 MSD** 의 장시간 기울기로 σ. unwrapped 좌표 필요, 긴 궤적 필요. Eq. 2–3 |
| **GK (Green–Kubo)** | **전하전류 자기상관(CACF)** 의 시간적분으로 σ. fs 급 속도 필요, 디스크가 병목. Eq. 9 |
| **CMSD** | collective MSD = `⟨‖Σᵢ zᵢ Δr⃗ᵢ‖²⟩`. 개별 MSD 의 합이 아니라 **부호를 넣어 더한 뒤 제곱** |
| **CACF** | charge current autocorrelation function, `⟨J⃗(t+τ)·J⃗(t)⟩` |
| **self / cross 항** | `i=j` 항(self, D 에 비례) vs `i≠j` 항(cross, 상관). 이 논문 계에서 cross 는 **항상 음수** |
| **ionicity = H⁻¹** | 역 Haven 비 `σ_tot/σ_NE`. 1 = 무상관, <1 = 상관이 σ 를 깎음. Eq. 16 |
| **Haven ratio H_R** | `D*/D_σ` (adeli 규약). `H_R = 1/ionicity`. **부호 주의 — §6.3** |
| **ideal / real transport number** | ideal = self 항만(Eq. 14) · real = cross 포함(Eq. 15). **real 만 좌표계 의존** |
| **reference frame** | mass-fixed(무게중심) / number-fixed / solvent-fixed. σ_tot 은 무관, cross·수송수는 의존 |
| **correlation depth** | 상관함수·MSD 를 계산하는 최대 lag τ. 궤적 길이의 몇 % 로 정한다 |
| **χ²_red 재조정** | replica 산포가 각자의 오차보다 크면 오차막대를 `sqrt(χ²_red)` 배 키우는 장치. Eq. 27 |
| **bootstrap** | replica 를 복원추출해 σ 분포를 만들고 그 산포를 오차로. GK 에서 특히 권장 |
| **Yeh–Hummer 보정** | 주기경계에서 self-diffusion 의 유한크기 편향 보정 `2.837297 k_BT/(6πηL)`. 점도 η 필요 |
| **CL&P / CL&Pol** | OPLS 기반 이온액체 힘장 / 그 Drude 분극판. CL&P 는 전하 0.8 배 스케일이 관행 |
| **TGNH** | temperature-grouped Nosé–Hoover — Drude 입자를 별도 저온(1 K)으로 유지하는 써모스탯 |
| **TRAVIS `conduct`** | 이 논문이 추가한 모듈. EH·GK·분해·좌표계 변환을 궤적 하나에서 |
| **MSDiff** | 로그기울기로 MSD 선형영역을 자동 검출하는 도구 (v0.2.0, ref [26]) |

---

## 18. ⚠ 못 한 것 / 확인 못 한 것 (필수 절)

**본 그림 / 안 본 그림**
- 크로핑 산출 **47장** = 그림 PNG **22장** + 표 PNG **25장**.
- **실제로 Read 로 본 것: 그림 PNG 9장** (`fig_1`, `fig_2`, `fig_6`, `fig_7`, `fig_8`, `fig_9`, `fig_S1`, `fig_S10`, `fig_S12`)
  → 논문 그림으로는 **10개**다. `fig_6.png` 하나에 **`Fig. 5` 와 `Fig. 6` 이 같이 잘려** 들어갔기 때문
  (`Fig. 5` 캡션이 p.12 에서 `Fig. 6` 캡션 아래에 있어 추출기가 별도 슬롯을 못 만들었다 — 결과적으로 손실은 없다).
  본 것: `Fig. 1`, `Fig. 2`, **`Fig. 5`**, **`Fig. 6`**, **`Fig. 7`**, **`Fig. 8`**, `Fig. 9`, **`Fig. S1`**, `Fig. S10`, **`Fig. S12`**.
- **안 본 것**: `Fig. 3`, `Fig. 4`(수송수 — 우리 계는 가동종이 Li 하나라 대응물 없음), `Fig. S2`, `S4`, `S9`, `S11`, `S13`, `S14`, `S15`, `S16`, `S17`, `S19`, `S20`.
  이들은 캡션 + 대응 SI 표의 텍스트로만 처리했고, 그 수치는 표에서 왔으므로 신뢰도가 높다.
- **표 25장(`tab_*.png`)은 이미지로 안 봤다** — 우리 관례대로 PDF 텍스트에서 전사했다.

**크로핑 실패 (도구가 "그래픽 없음"으로 제외한 6건)**
`Fig. S3`(CACF 적분, LiFSI) · `Fig. S5`(CACF 적분, IL) · `Fig. S6`–`S8`(plateau 식별법 비교) · **`Fig. S18`(전 계 상관깊이 종합)**.
⚠ 이 중 **`Fig. S6`–`S8` 은 GK plateau 검출법 비교**라 F5 를 더 정량화할 수 있었고, **`Fig. S18` 은 크기별 상관깊이 종합**이라 F4+F7 을 이었을 그림이다. **둘 다 공백으로 남는다.**

**본문–그림 불일치를 못 찾았다**
본 10개 그림에서 **본문 서술과 어긋나는 것은 없었다.** 수치도 표와 일치했다.
다만 `Fig. 2` 에서 **본문이 말하지 않는 것**(NE 가 실험선에 더 가까움)이 보였고, 그건 §16-B-1 로 옮겼다 — 불일치가 아니라 **누락**이다.

**확인 못 한 것**
1. **`nslice`/`tol`/`incr` 수치** — 논문·SI 에 없다. TRAVIS 소스나 `conductivity_tools` 저장소를 봐야 한다(안 봤다).
2. **원시 데이터** — 공개 저장소가 없다. Table S6–S23 의 수치를 재계산해 검증하지 못했다.
3. **ref [26] Frömbgen 2025** (같은 그룹의 선행 "Lessons Learned on Obtaining Reliable **Dynamic Properties** for Ionic Liquids", *ChemPhysChem* 26: e202401048) — **미확보.** 자동창 알고리즘의 정본은 사실 그쪽이다.
4. **ref [94] Maginn 2019 LiveCoMS** — 우리 litdb 에 `maginn2019_best_practices_transport_selfdiffusivity_viscosity` 로 **동시 작업 중**. 이 편과의 중복·충돌은 그 digest 가 나온 뒤 대조해야 한다.
5. **ref [45] Kubisiak & Eilmes 2020** (*JPCB* 124, 9680) — *"how to invest the computational effort"* 로 replica vs 길이 트레이드오프를 다룬 편. **미확보.** replica 개수의 정량 근거는 그쪽에 있을 가능성이 높다.
6. ~~우리 3-seed 가 "속도만" 인지~~ → ✅ **확인 완료**: 속도 시드만 다르다 (§7.2·§12).
7. **Langevin 열욕이 집단 전하전류에 주는 영향** — 이 논문에 없고, 나도 문헌으로 확인하지 않았다. §12 의 그 줄은 **가설 표시**로 남긴다.
8. **`run_md_sigma.py` 가 실제로 cascade Stage 10 에서 호출되는 경로인지** — 파일만 읽었고 호출 그래프는 안 봤다.
   (확인한 것: 이 파일이 `fit_start = n_frames//2` 를 쓴다는 것과, **이온 캠페인 경로는 `--fit_window_ps 2 50` 을 쓴다**는 것.)
9. **modelc·b2o3·LPSOCl 등 다른 계의 σ 경로가 어느 창을 쓰는지** — comp1 경로 하나만 확인했다.
10. **`tools/ionic/msd_refit_window.py` 와 `msd_diffusive_check.py` 의 실제 기능** — 이름과 docstring 한 줄만 봤고 열어보지 않았다.
    §14 T0b 의 *"새 도구 불필요"* 판단은 그 전제 위에 있다.
