# 🎯 우리 DFT 기준값 (comp1 / modelc) — 모든 문헌 비교의 기준점

> 출처: Excel "DFT 관련" 시트 [본 연구] 0-1 / 0-2 + 세션 결과. 문헌 digest의 §7은 항상 이 표와 대조.
>
> ⚠ **방법 라벨 주의 (2026-07-27 정정)**: 우리 Ea·D 는 **AIMD 가 아니라 MLIP-MD**(UMA-s-1p1, omat)다.
> 진짜 AIMD 논문과 대조할 땐 '둘 다 AIMD라 직접 비교' 식으로 쓰지 말 것 — 힘 계산 축이 다르다.
> gap 2.099 는 fixed-occ nscf 고유값(canonical). 2.098 은 lobster_nscf 교차검증값이라 헤드라인에 쓰지 않는다.
> 그리고 comp1/modelc Ea 는 **온도당 단일 궤적**이다 — 멀티시드 비교엔 modelc 3-seed 0.197±0.032 를 쓴다.

| 물성 | **comp1 = Li₆PS₅Cl** | **modelc = Li₅.₄PS₄.₄Cl₁.₆** | 방법 |
|---|---|---|---|
| Band gap | 2.066 eV | **2.099** eV | DFT PBE · **fixed-occ nscf VBM/CBM 고유값** (DOS-threshold 금지) |
| E_F / VBM / CBM | 3.724 / 2.128 / 4.194 eV | 3.487 / 2.445 / 4.544 eV | DFT |
| E_VRH (relaxed-ion) | 22.06 GPa | **27.66 GPa** | DFT elastic (C_ij) |
| B₀ | **26.23 GPa** | 21.71 GPa | EOS BM3 (V0 254.16 / 243.29 Å³·fu⁻¹) |
| Ea (활성화에너지) | 0.253 eV | **0.224 eV** | **MLIP-MD** (UMA-s-1p1) Arrhenius · ⚠단일 궤적(오차막대 없음) |
| D(600 K) | 3.09×10⁻⁶ cm²/s | **7.90×10⁻⁶ cm²/s** | **MLIP-MD** (UMA-s-1p1), MSD 2–50 ps |
| ICOHP(Li–Cl) | −1.86 | −2.10 | LOBSTER |
| 산화 onset (grand-potential) | **2.256 V** (LiS4 포함 시 2.14) | **2.256 V** (LiS4 포함 시 2.14) | get_element_profile, LiS4/SCl3/Li5PS4Cl2 제외 = GG set |
| 환원 한계 / OCV | 1.242 V / 1.717 V | 1.242 V / 1.717 V | grand-potential |

### ESW 상세 (LiS4 제외, 2026-06-23 gabia 재계산 — `esw_lis4excluded.json`)
> LiS4(현 MP id `mp-aaaceqmj`)·SCl3·Li5PS4Cl2 제외(Gil-González 2022 phase set). **두 조성 onset 동일 2.256 V (S²⁻-limited).**
- **comp1 onset (2.256 V)**: `Li6PS5Cl → Li3PS4 + LiCl + S + 2 Li⁺ + 2 e⁻` ← **Zuo Eq1과 정확히 일치** (원소 S, 2 e⁻)
- **modelc onset (2.256 V)**: `Li5.4PS4.4Cl1.6 → Li3PS4 + 1.6 LiCl + 0.4 S + 0.8 Li⁺ + 0.8 e⁻` (Cl-rich: 전자 적게·LiCl 많이 = Zuo Eq2 거동)
- 이후 단계: 2.385 V(P₂S₇+S), 3.326 V(SCl); modelc만 3.388 V(PCl₅).
- GG K_eff=0 anodic 2.40 V와 격차 **0.14 V**(LiS4 포함 시 0.26). 환원/OCV(1.242/1.717) 불변.

## 핵심 발산 (comp1 → modelc, Cl 증가 효과)
- **이온전도**: D↑(2.6×), Ea↓ — Cl-rich가 더 빠름 (disorder·vacancy)
- **기계적**: B₀↓ (26.2→21.7, Coulomb 응집 약화) ↔ E_VRH↑ (22→27.7, C44↑/disorder) — **방향 반대**
- **전자구조**: gap·VBM character 거의 불변 (둘 다 VBM=S 3p)
- **산화 onset**: 동일(S²⁻-limited) — Cl는 onset이 아니라 *분해 양·산물·계면*에 작용

## 비교 시 주의 (방법 의존성)
- **band gap**: PBE는 과소평가(실험·HSE 대비 ~1 eV↓). 무질서 배열·k-mesh로 ±0.2–0.3 eV 흔들림 → 문헌과 절대 gap 직접 비교 금지, "wide-gap insulator" 수준만.
- **mechanical**: relaxed-ion vs clamped-ion, PBE vs PBEsol/D3 로 E/B/G 크게 달라짐 → functional 명시 후 비교.
- **ESW**: 0-pressure grand-potential은 S-limited라 조성 무관 onset만 봄. 무질서 metastability·기계 구속·계면은 별도 축.
