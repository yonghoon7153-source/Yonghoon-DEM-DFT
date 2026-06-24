# ELF로 무엇을 보는가 — modelC vs Nd₂O₃-doped (PS₄ plane)

작성 2026-06-24. ELF(Electron Localization Function, 0–1) PS₄ 평면 슬라이스에서 읽어내는 효과 정리.

## ELF 읽는 법
- **ELF→1 (빨강)**: 전자 강하게 국소화 = **공유결합 bridge · lone pair · core**
- **ELF~0.5 (초록)**: 균일 전자기체 수준(경계)
- **ELF→0 (파랑)**: 전자 결핍 = **이온결합 영역 · 원자간 빈공간**
> ELF = "전자가 *어디에 어떻게* 뭉쳐 있나"(결합 character). 세기(ICOHP)·전하(Bader)와 함께 보는 **독립 probe**.

## 이 세트에서 보이는 4가지 효과
1. **공유 P–S 백본 — 도핑에도 불변** : P–S 사이 빨강 bridge(ELF midpoint **0.870**) = 공유결합. **modelC ≈ nd pristine PS₄** → **Nd₂O₃ 도핑이 PS₄ 골격을 안 건드림**(host intact). ICOHP P–S +0.4% 불변과 정합.
2. **P–O 강·polar 공유 (= O actor)** : PS₂O₂ 패널의 P–O bridge가 **더 짧고 O쪽으로 쏠림**. ELF midpoint **0.838 < P–S 0.870** = 더 **polar**(O 전기음성도가 전자를 당김). ICOHP **−8.43**(P–S 대비 +41%) = "강하지만 이온성 섞인 공유". → **결합을 바꾸는 actor는 O**(Nd 아님).
3. **이온 Li / Cl / Nd** : Li⁺·Cl⁻ 주위 파랑(floor **0.018–0.032**) = 이온(공유 bridge 없음). Nd–X floor **0.13–0.19**(Li 0.02보다↑, P–S 0.87보다↓↓) = 약한 5d 공유 끼었으나 본질 이온 = **Nd는 이온 spectator**.
4. **S lone pair** : S 주위 빨강 lobe(핵 위 dip + 바깥 비결합 전자쌍).

## 한 줄
ELF로 보는 것 = **(a) 누가 공유결합이고 누가 이온인가 + (b) 도핑이 그 결합 character를 바꾸나.**
→ 결론: **host P–S 공유백본 불변 · O만 강·polar P–O 추가 · Nd/Li/Cl는 이온.** ICOHP(세기)·Bader(전하)와 교차검증되는 **5번째 독립 probe**이며, "**O가 결합 actor, Nd는 이온 carrier**"를 시각적으로 확정.

## ⚠ 주의 — on-Nd 4f는 ELF로 해석 불가
Nd 원자 위(그리고 Li core 일부)에 **speckle/얼룩 아티팩트** = PBE+U 4f. **on-Nd 영역은 ELF로 못 읽음** → 4f 자체는 **spin density**(QE pp.x `plot_num=6`). ELF는 **결합(P–S/P–O/lone pair) 영역만** 신뢰. (근거·교정 `kb/physics/nd_4f_doping_consolidated_corrected_2026_06_24.md` §4 C6.)

## figure / data
| 파일 | 내용 |
|---|---|
| `modelc_ELF_PS4plane.png` | **비교 baseline** — modelC pristine PS₄ (annotated) |
| `nd_ELF_PS4plane_clean.png`, `modelc_ELF_PS4plane_clean.png` | **ELF-only(clean)** 버전 (chrome 없음) |
| `clean/nd_ELF_{PS4,PS3O,PS2O2}_clean.png` | nd pristine / O 치환(PS₃O·PS₂O₂) clean |
| `clean/{comp1,modelc}_ELF_PS4_clean.png` | host 대조 |
| `nd_ELF_PO_vs_PS_profile.png` | P–O vs P–S ELF 선프로파일 |
| `nd_elf_bond_quant.csv` | 정량: P–S 0.870 · P–O 0.838 · Nd–X floor 0.13–0.19 · Li/Cl/S floor 0.018–0.032 |
> 도구: `tools/figures/plot_elf_plane.py` (`--clean`으로 ELF-only). cube: modelc/nd ELF (uploads). 같은 plane=P+최근접 2 S 자동.
