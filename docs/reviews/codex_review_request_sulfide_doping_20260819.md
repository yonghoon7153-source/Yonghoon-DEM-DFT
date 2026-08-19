# Codex 교차리뷰 요청 — 황화물 SE 도핑을 우리 파이프라인에 넣는 계획

**대상 브랜치**: `claude/stoic-knuth-NObVQ` (커밋 `ce0ac5a2` 기준)
**성격**: **착수 전 설계 리뷰.**  코드는 게이트 한 곳만 고쳤고(§D-1), 도핑 자체는 한 줄도 안 짰다.
**질문의 형태**: "코드가 맞는가" 가 아니라 **"이 실험이 무엇을 말할 수 있고 무엇을 말할 수 없는가"**.
**요청자 메모**: 이 계획은 **자체 3렌즈 리뷰를 이미 한 번 통과했다.**  그 리뷰가 잡은 것은
§C 에 그대로 옮겼다 — 리뷰어는 **그것들을 신뢰하지 말고 재검증**하고, 더 중요하게는
**그 리뷰가 못 본 것**을 찾아 주면 된다.

---

## §A. 배경 30초 — 왜 도핑인가, 왜 지금인가

우리는 황화물 ASSB 복합양극의 DEM(접촉망) + MPM(소성 압밀) + STEP3(복셀 유한체적 σ) 파이프라인을
갖고 있다.  SE 는 Li₆PS₅Cl 하나로 고정돼 있고 그 이온전도도는 **한 상수**다:

```
scripts/se_material.py:81-82
    SIGMA_GRAIN_MS_CM_25C = 3.0        # mS/cm   (Cronau 2022 단결정)
    SIGMA_GRAIN_S_CM_25C  = 3.0e-3     # S/cm
→ scripts/step3_sigma.py: SIGMA_ION_SE_S_CM_25C
→ scripts/mpm_webapp_payload.py:505  --sigma-ion-se  (기본 = 위 상수)
```

litdb 정본에 **아지로다이트 도핑 카드가 7장** 있고, 그것들이 σ_ion 을 **×1.25 ~ ×1.94** 로
올린다고 보고한다.  즉 우리에게는 **런 전에 등록할 수 있는 외부 예측값**이 있고,
그것을 넣는 데 **침대 재생성이 필요 없다**(σ 는 STEP3 단계 노브다).  ⇒ 값이 싸다.

**하고 싶은 것**: `--sigma-ion-se` 를 세 배수로 돌려 σ_ion_eff 가 어떻게 움직이는지 재고,
그 결과를 **원고의 "설계 노브" 절**에 쓴다.

**⚠ 하지만 그 전에 리뷰가 필요한 이유**: 우리 자체 리뷰가 **이 트랙의 절반이 no-op 임**을
발견했다(§C-2).  no-op 인 줄 모르고 돌면 "우리 모델이 도핑에 반응한다" 는 **가짜 결과**가 나온다.

---

## §B. 증거 기반 — litdb 정본 카드 7장 (전부 리포 안, 독립 확인 가능)

정본 서랍 = `origin/claude/friendly-meitner-lldvar` 의 `litdb/papers/`.
**아래 값은 전부 카드 소환값이고 우리 계산이 아니다.**  `AG` = 아지로다이트(= 우리 계),
`HAL` = 할라이드, `LGPS` = thio-LISICON.

| 카드 (`litdb/papers/*.md`) | 계 | 모체 → 최적 | **σ_ion** | **Ea (eV)** | σ_e (SE 누설) | 기계 |
|---|---|---|---|---|---|---|
| `ma2024_sb_doping_lpsc_conductivity` (263줄) | AG | Li₆PS₅Cl → x=0.05 (Sn/Sb/I) | 3.4 → **5.2 mS/cm (×1.53)** | 0.29 → **0.25** | 3.4e-9 → 2.0e-9 | **n/a** |
| `li2025_cubr2_dualdoping_argyrodite` (201줄) | AG | Li₅.₅PS₄.₅Cl₁.₅ → Cu₀.₁/Br₀.₂ | 5.3 → **10.3 mS/cm (×1.94)** | 0.295 → **0.239** | 1.02e-8 → 3.35e-9 | **E 28.2 → 28.8 GPa (DFT, ×1.02)** |
| `xu2026_ndo_codoping_argyrodite` (241줄) | AG | Li₅.₃PS₄.₃Cl₁.₇ → Nd–O x=0.025 | 6.99 → **8.75 mS/cm (×1.25)** | 0.292 → **0.278** | 4.2e-9 → 9e-10 | **n/a** |
| `wang2025_electronic_localization_yo_argyrodite` (869줄) | AG | Li₆PS₅Cl → Y–O x=0.05 | ~2.75 → **3.53 (×1.28)** | ~0.375 → **0.34** | ⚠ **인용 금지** (카드 §19.1 이 재현 실패 확정) | **n/a** |
| `deklerk2016_diffusion_site_disorder_argyrodite` (405줄) | AG | 4c-Cl 무질서 50 → 75 % | σ_J 2.56 → 5.12 S/cm **×2.00** ⚠ **AIMD 절대값** | intercage 0.18–0.27 | n/a | n/a |
| `schlem2020_li3mcl6_cation_site_disorder` (246줄) | **HAL** | Li₃ErCl₆ 앰풀 → 볼밀 | 1.7e-5 → 3.1e-4 (**×18**) | 0.49 → 0.41 | n/a | n/a |
| `zhou2026_high_entropy_lgps_multicationic` (1546줄) | **LGPS** | LGPS → 5원 high-entropy | **13.24 mS/cm @30 °C** (⚠ 25 °C 아님) | 0.313 | 1.07–1.39e-9 | n/a |

**보조 카드 3장** (도핑은 아니지만 이 계획의 경계를 정한다):
`torii2025_lpscl_mechanical_anisotropy_dft` (비도핑 LPSCl 의 C₁₁ 47.4 / C₁₂ 28.4 / C₄₄ 10.4,
E_VRH 27.4 · B 34.7 · G 10.0 · ν 0.37) · `zhu2020_air_stable_se_design_principles` ·
`richards2016_interface_stability_pseudobinary` (Li₆PS₅Cl ESW 2.06–2.32 V).

### B-1. 이 표에서 **우리가 읽은 것** (리뷰 대상)

1. **σ_ion 만 움직인다.**  기계축은 li2025 의 **+2.1 %** 하나뿐이고 나머지는 전부 `n/a`.
   ⇒ **압밀 물성(E_SE·ν·σ_y)을 건드릴 문헌 근거가 없다** → 도핑은 **σ 축 전용**으로 못 박는다.
2. **σ_e(SE 누설)은 모델링할 이유가 없다.**  카드 값 1e-9~1e-7 S/cm 는 우리 σ_VGCF 유효값
   100 S/cm 대비 **9–11 자릿수** 아래다.  ⇒ 슬롯을 안 만든다 (`_sig3[6] = 0.0` 유지).
3. **Ea 는 밴드 밖이다.**  우리 `se_material.EA_ION_EV_BAND` = {ma2024 0.29 · reisacher2023 0.41 ·
   kraft2017 0.46} 인데 위 표의 도핑 후 값은 **0.239 ~ 0.34** 다.  ⇒ 밴드를 조성별로 갈라야 하고,
   그러면 `warn_band()`(단일값 보고 금지 강제)의 의미가 바뀐다.

---

## §C. 자체 리뷰가 이미 잡은 것 — **재검증 요청**

### C-1. 판정기 게이트에 σ_ion 축이 없었다 (**고쳤다**, 커밋 `ce0ac5a2`)

`scripts/sdcp_gain_verdict.py` 의 고정-인자 게이트가 `vox · bridge_um · fibre_stamp ·
sdcp_stamp · sdcp_sphere_d_um · sdcp_yield_to_vgcf · sigma_ptfe_S_cm · sigma_vgcf_S_cm ·
sigma_sdcp_S_cm · backend` 만 봤다.  **σ_ion(SE)·σ_AM·CAM 프리셋·침대 세대는 없었다.**
더 나쁜 것은 기록 위치였다 — `step3['sigma_ion_table_S_cm']` 이 `manifest` **밖**이고
`if _res3i['n_dof']:` 안이라 **`--no-ion`(LEAN=2 = 현행 스윕의 기본 모드)에서는 아예 안 찍혔다.**

⇒ **도펀트 팔과 생산 팔이 한 디렉터리에 섞여도 판정기가 통과시켰다.**
이것은 CL-43(`sdcp_yield_to_vgcf`)·CL-49(`sigma_ptfe`)에서 **두 번 고친 같은 no-op** 이다.

**수정**: 매니페스트에 `sigma_ion_se_S_cm · sigma_ion_se_ref_S_cm · sigma_ion_sdcp_S_cm ·
sigma_am_s/p_S_cm · cam · temp_c · ea_ion_ev · mpm_seed · se_E_GPa · se_nu · se_sigma_y_GPa`
를 **`--no-ion` 여부와 무관하게** 기록하고, 판정기 고정 인자에 넣었다.  옛 payload 는 값을
**추정할 수 없으므로**(σ_ion 은 `--temp-c` 로도 움직인다) 정규화하지 않고, **기록 있는 팔과
없는 팔이 섞이면 HOLD** 로 했다.  selftest 15 → **23 PASS**.

> **Q-C1**: "섞이면 HOLD, 전부 옛 payload 면 통과" 라는 절충이 정당한가?
> 동기는 진행 중인 vox 0.125 스윕(옛 payload)을 죽이지 않는 것이었다.  이것이 **원칙을
> 편의로 굽힌 것**인가, 아니면 "한 디렉터리 안에서 세대가 하나면 비교는 유효하다" 가
> 실제로 맞는 논거인가?  후자라면 **반례**를 만들 수 있는가?

### C-2. ★★ σ_grain 을 바꿔도 σ_ionic **스케일링법칙**은 정확히 안 변한다 (no-op)

리포가 이미 자기 selftest 로 증명해 두었다:

```
scripts/generate_comparison_plots.py:7506
    chk('sigma_grain(T) is absorbed by the fit intercept: predictions identical', ...)
    → np.allclose(pa, pb, atol=1e-12);  R²·LOOCV 도 1e-12 이내 동일; 절편만 −log(f) 이동
scripts/generate_comparison_plots.py:4300  (런타임 인쇄)
    "... σ_ionic form predictions / R² / LOOCV are UNCHANGED.
     It relabels, it does not re-predict."
```

이유는 폼의 구조다 — `σ = σ_grain · Cronau(r_SE) · (φ_eff)^½ · CN² · cov^½ · f_p³ · C_blend(τ)`
에서 `C_blend(τ) = exp[a + b·lnτ + c·(lnτ)²]` 의 `a` 가 **live-fit 절편**이라
σ_grain 배수를 통째로 흡수한다.

⇒ **"도펀트가 σ_ion 을 ×1.53 올린다 → 스케일링법칙에 넣는다" 는 완전한 no-op.**
유일한 길은 **코퍼스 타깃을 그 σ 로 다시 풀고 재적합**하는 것이다
(`network_conductivity.py --temp-c` 가 같은 목적의 선례).

**추가 함정**: `generate_comparison_plots.py` 에 `SIGMA_BULK = 3.0` 지역 리터럴이 **6개**
(`:1128 · :1178 · :1792 · :1875 · :2165 · :3605` — `:4305` 는 그 사실을 적은 주석이라 별개) 남아 있고 파일이 `:4305-4310` 에서 스스로
자백한다.  도펀트 런에서 그 오버레이는 3.0 인 채 프로덕션 폼만 새 값이 되어 **한 그림 안에
두 규약이 섞인다**.

> **Q-C2 (가장 중요)**: 이 절대적 흡수(atol 1e-12)가 **실제로 우리 폼에서 성립하는지** 독립
> 확인해 달라.  성립한다면 — **도핑 결론을 STEP3 복셀 σ 에서만 내는 것**이 옳은 대응인가,
> 아니면 애초에 "스케일링법칙은 σ_grain 에 대해 정보가 없다" 를 **폼의 한계로 원고에 적어야**
> 하는가?  후자라면 그 한 문장이 폼의 가치를 얼마나 깎는가?

### C-3. σ_eff 가 σ_SE 에 선형이면 이 실험은 **무엇을 새로 말하는가**

`scripts/step3_sigma.py:2088` selftest 가 **σ_eff ∝ σ_SE (정확히 선형)** 를 증명한다
(유한체적 라플라스가 상별 σ 에 1차 동차이므로 당연하다).

⇒ 그러면 `--sigma-ion-se ×1.53` 을 넣었을 때 **σ_ion_eff 도 정확히 ×1.53** 이 나와야 하고,
그건 **물리적 발견이 아니라 산술**이다.

> **Q-C3**: 이 트랙에서 **선형성을 넘어서는 산출물이 있는가?**  후보 셋을 우리가 적었는데
> 전부 약해 보인다 — (i) **회귀 테스트**로서의 가치(비가 1.53 이 아니면 결함 탐지), (ii) 도펀트가
> **σ_ion 만이 아니라 밀도·입경도 바꾸면** 비선형이 생긴다(단 카드가 ρ 를 **한 장도 보고하지
> 않는다** = n/a), (iii) **σ_ion 과 σ_e 의 비**가 바뀌면 STEP4 반응분포·과전압 분해가 바뀐다.
> ⇒ (iii)이 유일하게 실질적으로 보이는데, **이것이 정말 σ 선형성 밖인가?**  아니면 STEP4 도
> 같은 이유로 스케일해 버리는가?  ★ **이 질문에 "없다" 가 답이면 이 트랙은 하지 말아야 한다.**

### C-4. 도핑이 **조용히 어긋날 수 있는 자리**

- `--sigma-ion-se` 는 **STEP3 단계** 노브다.  MPM 압밀에 안 들어간다 ⇒ **같은 침대**를 두 σ 로
  다시 푸는 것은 정당한 A/B 다.
- **진짜 위험은 반대 방향**이다: 도펀트가 E/σ_y 를 바꾼다고 판단해 `mpm3d` SE 물성을 건드리면
  **침대가 새 세대**가 되는데, `_add_meta['E_anchor']` 는 **첨가제만** 찍고 SE 본체의 세대는
  어디에도 안 찍혔다 ⇒ **CL-42(ADD_E_SET 사고)의 SE 축 재현 경로**.  (C-1 수정으로 이제
  `se_E_GPa/se_nu/se_sigma_y_GPa` 가 매니페스트에 남고 게이트가 본다.)
- `additives.DENS['SE'] = 2.00` · `dem_input_values.RHO_SE = 2.0` · 덱 `density constant 2000`
  **3곳이 정렬**돼 있다.  도펀트가 ρ 를 바꾸면 셋 다 고치고 `verify_deck` 를 다시 돌려야 한다.
  ⚠ **카드 7장 중 어느 것도 도핑 후 ρ 를 보고하지 않는다 (n/a).**

> **Q-C4**: 이 목록이 완전한가?  σ_ion(SE) 하나를 바꿨을 때 **우리가 못 본 하류 의존**이 있는가?
> 특히 `sigma_ion_sdcp`(0.001 S/cm 고정)와의 **비**가 바뀌는데, SDCP 가 이온 경로에 들어가는
> 자리(`step3_sigma.py:1267 ion_m`)에서 그 비가 어떤 역할을 하는지 봐 달라.

---

## §D. 우리가 제안하는 실행 계약 (사전등록 초안 — 여기를 찢어 달라)

### D-1. 팔 설계

| 팔 | `--sigma-ion-se` (S/cm) | 근거 |
|---|---|---|
| 대조 | 3.0e-3 | 현행 생산 (Cronau 2022 단결정) |
| A | 3.75e-3 (×1.25) | `xu2026_ndo_codoping_argyrodite` |
| B | 4.59e-3 (×1.53) | `ma2024_sb_doping_lpsc_conductivity` |
| C | 5.82e-3 (×1.94) | `li2025_cubr2_dualdoping_argyrodite` |

침대: 기존 SBE/DBE **재사용**(압밀 재실행 없음).  origin 은 대조와 **동일**.
압밀 물성 **고정**(E_SE 1.53 · ν 0.49 · σ_y 0.30).  `--no-pore --no-collector`, **이온 솔브는 켠다**.

### D-2. 사전 예측 (런 전 등록)

- **h0**: σ_ion_eff 비 = σ_SE 비 (선형), |편차| ≤ **1 %**.
- **h1**: 편차 > 1 % → **결함 또는 미발견 비선형** (둘 다 조사 대상, 발견 아님).
- ⚠ **h0 이 "성공" 이다** — 이 실험은 **가설검정이 아니라 회귀 테스트 + 값 측정**이다.
  그렇게 등록한다 (prereg §7: 결과 보고 창을 나중에 옮기면 무효).

### D-3. **쓰지 않을 것** (미리 못 박는다)

- 스케일링법칙 재적합 (C-2 — no-op 이고, 하려면 코퍼스 전체 재계산이 별도 프로젝트다)
- Ea 밴드 수정 (B-1-3 — `warn_band()` 규약이 바뀌므로 별건)
- 압밀 물성 변경 (B-1-1 — 문헌 근거 없음)
- σ_e(SE) 슬롯 신설 (B-1-2 — 9~11 자릿수 아래)

> **Q-D**: 이 계약이 **결과를 본 뒤 해석을 고를 여지**를 남기는가?
> 특히 D-2 의 "h1 = 결함 또는 비선형" 이 **무엇이 나와도 설명 가능한 서술**이 아닌가?
> 그렇다면 어떻게 좁혀야 하는가?

---

## §E. 리뷰가 답해 줬으면 하는 것 (우선순위 순)

1. **★★ Q-C3 — 이 트랙에 선형성을 넘는 산출물이 있는가.**  "없다" 면 그렇게 말해 달라.
   우리는 **하지 않는 것**도 결론으로 받는다.
2. **★★ Q-C2 — σ_grain 흡수의 독립 확인**, 그리고 그것을 원고에 **폼의 한계로 적어야 하는지**.
3. **★ Q-C1 — 세대 게이트의 절충**이 원칙을 굽힌 것인가.
4. **Q-C4 — 못 본 하류 의존.**
5. **Q-D — 사전등록이 사후 해석 여지를 남기는가.**
6. **자유 항목**: 위 §B 표에서 **우리가 잘못 읽은 값**이 있으면 지적해 달라.
   카드는 전부 리포 안에 있고 줄 수까지 적어 두었다.

---

## §F. 리포 컨텍스트 (독립 확인용 경로)

| 무엇 | 경로 |
|---|---|
| σ_SE 상수·Ea 밴드 | `scripts/se_material.py:81-91` |
| STEP3 σ 표·이온 마스크 | `scripts/step3_sigma.py` (`SIGMA_ION_SE_S_CM_25C` · `:1267 ion_m` · `:2088` 선형성 selftest) |
| CLI 노브·매니페스트 | `scripts/mpm_webapp_payload.py:505` · `:1773-` (manifest) |
| 판정기 (이번 수정) | `scripts/sdcp_gain_verdict.py` (`_GEN_FIELDS` · 세대 혼합 게이트 · `--seed-ensemble`) |
| σ_grain 흡수 증명 | `scripts/generate_comparison_plots.py:7506` (selftest) · `:4300` (런타임 경고) |
| 원장 | `docs/reviews/claims.json` — **CL-50**(σ_AM 라벨) · **CL-47**(σ_VGCF 유효-망 상수) · CL-46(절대 σ_e 문헌 앵커) |
| 도핑 카드 7장 + 보조 3장 | §B 표의 슬러그, 정본 브랜치 `origin/claude/friendly-meitner-lldvar` 의 `litdb/papers/` |
| 선행 규약 | `CLAUDE.md` — σ_ionic T1 절(폼 정의·**"DO NOT re-screen φc"**) · frame[4](DEM↔MPM 교차적합 금지) · §F1(앵커 없는 값 금지) |

---

## §G. 이 리뷰에서 **기대하지 않는 것**

- 코드 스타일·리팩터링 제안 (이 트랙의 병목이 아니다)
- 코팅 트랙 (별건 — 그쪽은 착수 전 `δ_max < 2t` 측정이 관문이다)
- "더 많은 도펀트 카드를 읽어라" (7장이면 배수 밴드는 충분하고, 병목은 **배수가 아니라 §C-3** 이다)
