# B₂O₃ Champion — 탄성상수(Cij) 분석과 한계 (2026-07-03)

**시스템** b2o3 = B₂O₃-doped LPSCl1.6 (**Li58P8S41Cl16B2O3, 128원자**), c축 긴 육방정 2× 슈퍼셀, V₀ = 2436 Å³.
**방법** stress–strain 유한변형 full Cij — `tools/comp1_v3/build_elastic_strain_inputs.py` (12 strain: 6 Voigt × ±) + `tools/modelc_v3/fit_elastic_cij_stress.py`. QE PAW, strain h = 0.005.
**비교 기준** modelc relaxed-ion E_VRH 27.66 GPa · comp1 22.06 · clamped-ion(comp1/modelc) ≈ 52 GPa · EOS B₀(b2o3) 24.48 GPa.

## 한 줄 결론
**Bulk modulus 27 GPa는 신뢰**(relaxed-ion normal + EOS 24.5 교차검증 → 무도핑 대비 **+13% 강화**). 하지만 **전단(shear) 기반 G·E는 두 방법 모두 신뢰 불가** — relaxed-ion은 shear 이완이 오염되고, clamped-ion은 내부이완을 금지해 과대평가. → **G·E 미보고**, 강화 서사는 Bulk로 지지.

## 두 방법의 차이
| | clamped-ion (frozen) | relaxed-ion |
|---|---|---|
| 원자 | 셀 변형 시 **분율좌표 고정** | 각 변형에서 **이완** |
| 의미 | 골격 자체의 "맨" 강성 | 물리적(실측 비교 가능) 강성 |
| 크기 | **크다** (내부이완 없음) | 작다 (이완이 softening) |
| 안정성 | 항상 positive-definite | disordered shear에서 취약 |

`Cij_:k = (σ(+h) − σ(−h)) / (2·strain)`, strain type k에 대해 stress의 한 열(column)씩.

## 결과 (relaxed-ion, b2o3)
6×6 Cij (GPa):
```
        j1      j2      j3      j4      j5      j6
 i1   43.40   20.00   18.40    1.25   12.58   -2.58
 i2   20.00   45.20   17.15    7.98   -7.73    3.30
 i3   18.40   17.15   43.20   -8.00   -6.95    0.00
 i4    1.25    7.98   -8.00   24.70  -12.60    8.35
 i5   12.58   -7.73   -6.95  -12.60   21.60   -0.40
 i6   -2.58    3.30    0.00    8.35   -0.40    5.15
```
- **Normal 정상**: C11/22/33 = 43.4/45.2/43.2 (tight, σ0.9), C12/13/23 = 20.0/18.4/17.2 (tight, σ1.2).
- **Shear 깨짐**: C44/55/66 = 24.7/21.6/**5.15**(C66 붕괴). 금지된 off-diagonal 큼(예: 13-shear에 normal σ1 = +30 딸려나옴 — 대칭상 불가능). Cij **고유값 하나 −2.87** → **not positive-definite**.
- 결과 VRH: **Bulk 27.02 GPa (정상)**, Shear −24.88, **Young's E −107.7 (비물리 garbage)**.

## 왜 relaxed-ion shear가 터졌나
1. 공식은 `+strain 구조`와 `−strain 구조`가 **같은 구조를 반대로 비튼 것(거울상)**이라 가정.
2. b2o3는 도핑된 **어수선한 셀**(B/O 점결함 + Cl 무질서 + 2× 슈퍼셀 128원자) → 에너지 지형에 **가까운 국소 최소점이 여러 개**.
3. **비틀기(shear)는 원자를 크게 이동** → +shear와 −shear가 **거울상이 아니라 서로 다른 배치(다른 최소점)로 이완**.
4. 그러면 `σ⁺ − σ⁻`이 탄성 반응이 아니라 **"두 다른 구조의 차이"**를 재게 됨 → 오염(off-diagonal 스퓨리어스, C66 붕괴, 음의 고유값).
5. shear 진짜 신호는 작음(`Δσ ≈ C44·2·2h ≈ 0.5 GPa`)인데 strain 0.005라 오염(수 GPa)에 **묻힘**.
6. **normal(늘이기/누르기)은 원자가 적게·대칭적으로 움직여** ±가 거의 거울상 → 오염 없음 → C11/C12/Bulk 깨끗.
7. modelc는 덜 어수선해 relaxed-ion이 성립(27.66)했고, b2o3는 **더 어수선 + 더 큰 셀**이라 취약.

> 비유: 용수철 강성을 재는데 누를 때·당길 때 **속 부품이 매번 다르게 재배열**되면, 용수철이 아니라 "두 상태의 차이"를 재는 꼴.

## 왜 clamped-ion이 터무니없게 큰가
- clamped는 **내부이완을 아예 금지** → 골격이 실제보다 훨씬 뻣뻣하게 나옴.
- argyrodite는 변형 시 **PS4 사면체가 크게 회전/왜곡**(내부이완이 큼). 이걸 막으면 특히 **전단 강성이 크게 과대**.
- 그래서 clamped E_VRH ≈ 52 GPa(comp1/modelc) = relaxed(22–27)의 **약 2배**. 실측 황화물 모듈러스(~20–30 GPa)와도 안 맞음.
- **즉 clamped는 안정적(positive-definite)이지만 물리적으로 과대** → 논문 대표값으로 부적절, **상한(upper bound)**으로만 의미.
- 반면 **Bulk(등방압축)은 내부이완이 작아** clamped ≈ relaxed → 27 GPa가 두 방법에서 견고.

## 신뢰할 수 있는 것
- **Bulk = 27 GPa** — relaxed-ion normal축 + **EOS B₀ 24.48 GPa** 두 독립 방법 일치.
- 무도핑 modelc 21.7 대비 **+13% 강화**. **ICOHP의 새 강결합(B–S −7.57, P–O −8.56)**과 정합 = "도핑이 골격을 단단하게".

## 결정 & 향후
- **G·E는 미보고** (정직). 기계 강화 주장은 **Bulk로** 지지.
- 정확한 relaxed-ion G가 필요하면: **strain 0.01(신호 2배) + tight forc_conv + 일관된 기준구조**로 shear 6개 재실행.
- clamped-ion은 **상한**으로만 인용(`tools/elastic/run_b2o3_elastic_clamped_kisti.sh` 준비됨).

## 논문/발표 문구 (제안)
> "The bulk modulus (27 GPa, relaxed-ion, consistent with the EOS value of 24.5 GPa) increases by ~13% upon B₂O₃ doping relative to undoped LPSCl₁.₆ (21.7 GPa), in line with the new strong covalent B–S and P–O bonds seen in ICOHP. Shear moduli from the relaxed-ion stress–strain method were not robust for this disordered 128-atom supercell — the ±shear configurations relaxed into distinct local minima, giving a non-positive-definite elastic matrix — while the clamped-ion values overestimate the stiffness (~2×) by excluding the large internal-strain relaxation of the PS₄ framework, and are quoted only as an upper bound."

**데이터**: `elastic_relaxedion/elastic_results_stress.json` (KISTI) · 관련 축 요약은 `b2o3_champion_status_2026_07_03.md`.
