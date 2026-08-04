# Dopant site preference (antisite-swap, all-UMA) — 81-system screen

Method: `tools/doping/site_preference_swap.py` — same-composition M@P vs M@Li position
swap, both relaxed (UMA-s-1p1), ΔE = E(M@P) − E(M@Li). ΔE<0 → framework P site;
ΔE>0 → Li site. 81 systems (27 dopant oxides × 3 concentrations), 78 ok + 3 Li2O skip.
Per-element aggregate: `docs/figures/site_preference/site_pref_by_element.csv`.

## Headline
**Determinant = ability to be a framework former (small + high valence), not pure size.**
- **Tetravalent group-14 (Si⁴⁺, Ge⁴⁺, Sn⁴⁺) → P framework** (mean dE −0.96 eV; the ONLY
  clear P-preferrers). They substitute P⁵⁺ in the PS₄ tetrahedron.
- **Large di/tri-valent (alkaline-earth Ca/Sr/Ba, rare-earth La/Nd/Sm/Gd/Y, Na, Ag, late-TM)
  → Li site** (mean +1.57 eV for r>0.9 Å). Too large / wrong valence for the tetrahedron.
- **B, Al = borderline / flip** (mean ≈ 0–0.3). B (r 0.27) is small enough for P but B³⁺
  prefers B–O (borate) → competes between framework-P and Li/O region.
- Pearson r(ionic radius, mean dE) = **0.67** — a real but noisy size trend (valence breaks it:
  group-14 +4 are P-preferrers despite Sn being mid-size).

## Answers to the live questions
- **B@P (PI's DFT setup)**: DEFENSIBLE but borderline. B prefers P at x005/x010 (dE −0.41/−0.21)
  yet flips to Li at x002 (+0.76). B genuinely competes between framework-P and borate(Li/O).
  → Running B@P is valid; do NOT claim "B clearly prefers P" — it is one of two motifs.
- **Nd → Li (robust)**: dE +0.33/+0.92/+2.42 across x002/005/010, all Li, mean +1.22.
  Confirms the Nd@Li / Li-channel-blocking picture (consistent with σ↓ vs modelc).
- **Y vs Nd — NOT a site difference**: Y also → Li (dE +0.47/+2.31/+2.51, mean +1.76), even
  more strongly than Nd. So the earlier "Y@P (ionic↑) vs Nd@Li (ionic↓) is a site effect"
  hypothesis is **NOT supported** here — both prefer Li. Whatever drives the Y-paper's ionic
  gain is not a clean site-preference difference from Nd in this screen.

## Honest method caveats
- **Large scatter / concentration flips**: the same element can flip P↔Li across x (Al, B, Cr,
  Ni, Sn-x005, Ge-x010). The antisite-swap ΔE is sensitive to the specific champion config and
  to which P/Li is chosen for the swap → treat as a **coarse, semi-quantitative screen**, not a
  precise per-element verdict. Robust conclusions are the **extremes** (group-14 → P; large
  RE/alkaline-earth → Li); the middle (B/Al/TM) is ambiguous.
- **Non-converged M@P** (conv=n: Al2O3_x002, Ag2O_x002/x010): big-cation-on-P is intrinsically
  high-strain and may not reach fmax → those dE are upper bounds (sign still trustworthy for
  large cations).
- Same-composition swap includes the displaced-host (P↔Li) antisite penalty — intrinsic to a
  fixed-composition comparison; the SIGN and cross-element ranking are the usable signal.
- Li2O/Li-led "dopants" skipped (anion-on-chalcogen, cation P-vs-Li N/A).

---
## 2026-08-04 추가 — 원본 78행 회수 + Wang 2025 (Angew) 와의 정면 충돌

**원본 등록**: `db/properties/site_preference_raw_78.csv` (gabia `/data/work/runs/site_preference/`
에서 회수). 계·농도별 dE/dopant·수렴여부·반경·원자가 + P→Li 순위. 이제 in-repo 재검증 가능.

### Y 자리 — 우리 vs 논문

| | Wang 2025 (Angew, Fig S3) | 우리 (78계 스크린) |
|---|---|---|
| 방법 | VASP/PBE, 정렬 스냅샷 **1쌍** | UMA antisite swap, **3농도** |
| 값 | −4.27846 vs −4.26615 **eV/atom** | dE/dopant **+0.465 / +2.306 / +2.506 eV** |
| 차이 | **0.0123 eV/atom** (~52원자면 총 **0.64 eV**, P 유리) | +0.47~+2.51 eV, **Li 유리** |
| 판정 | Y → **P (4b)** | Y → **Li** (전 농도, 예외 없음) |
| 78계 중 순위 | — | x002 25위 · x005 **67위** · x010 **72위** (1=P 최강) |

**같은 질문을 재고 답이 갈렸다.** 논문 식은 고립원자 기준이지만 두 모델이 같은 조성이라
기준항이 전부 상쇄된다 — 결국 총에너지 차/원자수이고, 우리 antisite swap 과 **방법론상
같은 비교**다. "다른 걸 재서 다르다"가 아니다.

⚠ **크기 감각**: 논문 0.64 eV(총) vs 우리 x002 0.47 eV — **크기는 같은 급, 부호만 반대**.
어느 쪽도 압도적이지 않다. 남는 변수 셋: ① DFT vs UMA ② 농도 ③ Li 자리 정의(그들 48h, 우리 24g).

### ⚠ 자기점검 — 농도는 우리도 떳떳하지 않다

| | Y 원자수 / 셀 | Y / 전체 | Y / (P+Y) 자리 |
|---|---|---|---|
| 논문 (관례셀 52원자 추정) | 1 | 1.9 at% | **25 %** |
| 우리 Y2O3_x005 champion | 2 / 47원자 | 4.3 at% | **33 %** |

논문의 "25%"는 **우리 추론**이다(그림의 이산 라벨 Y2·O70 = 정수 decorate + a≈9.848 Å
관례셀). 명목 5%(Y 0.05/f.u.)를 관례셀에 넣으면 0.2개라 정수 모델 최소가 1개 = 명목의 5배이고,
제대로 하려면 P 20개(=5× 관례셀, 260원자)가 필요하다.
**그런데 우리 x005 셀도 47원자에 Y 2개라 P 자리 환산 33%로 더 진하다** — 과도핑 비판은
쌍방에 적용된다. 우리 쪽에서 희석 극한에 가장 가까운 점은 **x002(+0.465, 여전히 Li)** 이고,
농도가 **오를수록 Li 선호가 강해지는 단조 경향**이라 희석 쪽으로 외삽해도 부호는 안 뒤집힌다.

### 결론 (인용 가능한 문장)
> 우리 스크린은 Y 를 전 농도에서 Li 자리로 판정하며(dE +0.47~+2.51 eV/dopant, 78계 중
> 25/67/72위), 이는 Wang 2025 의 Y@4b(0.0123 eV/atom, 정렬 스냅샷 1쌍)와 부호가 반대다.
> 두 값의 크기가 비슷하고 양쪽 모두 과도핑 정수 모델이므로, **어느 쪽도 확정이 아니다** —
> comp1 host 에서 동일 조성·동일 범함수로 Y@4b vs Y@24g 를 DFT 로 1쌍 계산하는 것이
> 남은 결정 실험이다.

---
## Takeaway for the paper
A clean, defensible statement: **"Tetravalent group-14 dopants enter the P (framework) site;
larger di/tri-valent cations — including all rare earths and alkaline earths — occupy the Li
site and thus impede the Li sublattice."** B is a borderline framework/borate case; Nd robustly
takes the Li site (channel-blocking). Y behaves like Nd (Li), so the Y↑/Nd↓ ionic contrast is
not explained by site preference alone.
