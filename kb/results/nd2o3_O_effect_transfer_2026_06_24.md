# Nd₂O₃-LPSCl1.6 — **O 효과 중심** 정리 (transfer용)

작성 2026-06-24. **Nd 효과는 작다**(이온 spectator·갭 좁힘=단점) → 이 문서는 **이점의 주역인 O**만 추려 transfer용으로 재정리: ① O가 한 일(설명) + ② 근거 figure + ③ MP 결과.
- 전체 종합/Nd 판정: `kb/results/nd2o3_master_findings_2026_06_18.md`, Nd-vs-O 분리설계: `kb/methodology/nd_vs_O_isolation_campaign_2026_06_18.md`.
- 조성 Li₅.₄₊₂ₓP₁₋ₓNdₓS₄.₄₋₁.₅ₓO₁.₅ₓCl₁.₆ (실험 x=0.02 / DFT x=0.2 과도핑).
- O speciation (relaxed 120-atom, 검증됨): **1×PS₂O₂ + 1×PS₃O + 8×pristine PS₄** (O가 PS₄ 코너 S를 부분 치환).

---

## 1. O가 한 일 — 3가지 이점

### ① O = host에서 가장 강한 결합 (bonding actor): P–O
- **ICOHP −8.43 eV/bond** (P–S −5.98 대비 **+41%**), d **1.571 Å** (P–S 2.064보다 0.49 Å 짧음). [`nd_icohp.json`]
- ELF midpoint **0.838** (P–S 0.870보다 낮음) = **강하지만 polar한 공유결합** (O 전기음성도가 전하를 당김). [`nd_elf_bond_quant.csv`]
- host 백본은 ±4% 불변(P–S +0.4%, Li–Cl −1.4%, Li–S +4.1%) → **O는 구조적으로 안전한 도핑**; 자기 자리(P–O)만 단단히 박힘.
- 📈 `docs/figures/nd_elf/nd_ELF_PO_vs_PS_profile.png` (P–O 빨강: 짧고 약간 낮은 plateau / P–S 초록: 길고 높은 plateau) · clean 슬라이스 `nd_elf/clean/nd_ELF_PS3O_clean.png`·`nd_ELF_PS2O2_clean.png` (O 치환 사면체) vs `nd_ELF_PS4_clean.png`.

### ② O 2p = deep spectator (전자구조 안 해침)
- O 2p bonding **~−4 eV** (VBM/CBM 아님). 산화 사면체(PS₂O₂·PS₃O)는 P–O 반결합을 위로 밀어 **frontier 상태를 gap edge에서 멀어지게** 함 → gap은 pristine PS₄(+Nd)가 결정.
- 갭 narrowing (undoped 2.184 → Nd+O 1.632, **−0.55 eV**)은 **Nd 5d/aliovalent 탓이지 O 아님**. *pure-O 도핑이면 갭 유지/확대(textbook)* — 부호 반전은 Nd co-dopant 때문. [`electronic.json` → `eigenvalue_gaps_v100_2026_06_16`]
- → **O는 전해질 전자구조에 무해** (갭 좁힘이라는 단점은 Nd 몫).
- 📈 `docs/figures/nd_dos/nd_dos_pdos_v2.png` · `docs/figures/dos_pdos_smooth/nd_PDOS.png`·`nd_DOS.png`·`nd_4f_excluded_gap.png`.

### ③ ★ O-유래 wide-gap passivation → σ_e↓ → cycle↑ (논문 central 기전)
- O 분해 산물 = **전자절연 wide-gap 상**: **Li₃PO₄ 5.73 eV**(벌크/GB), **Li₂O 5.24 eV**(Li 양극 SEI). (Nd 동반 시 NdPO₄ 5.55*.) [MP]
- 이 O-phosphate/oxide가 **입계(GB)/계면에서 전자 percolation을 끊음** → DC-pol σ_e **↓** (실험: 3.45 → **2.33** ×10⁻¹⁰ mS/cm @x=0.02 최저).
- 대조: O 없는 modelc는 **전도성 폴리설파이드/인화물**(P₂S₇·LiS₄·Li₃P 0.70·Li₂S 3.90)로 분해 → 전자 누설.
- σ_e↓ → 내부 Li⁰ 석출(dendrite)·self-discharge 억제 (Han 2019) → **cycle↑**.
- ⚠ **bulk 갭은 오히려 좁아짐**(②) → σ_e↓는 **interphase/GB(microstructure) 효과지 bulk 아님**. (GB 전자수송 직접계산 X = 추론; SSRM·XPS depth 검증 필요.)
- 📈 (新) `docs/figures/nd_sei/sei_product_gaps_O.png` — SEI 산물 band gap(MP) 막대: O-유래 wide-gap(녹색·파란테두리) vs 전도성 누설(빨강).

---

## 2. Figure set (O 관련) — transfer 목록
| figure (docs/figures/…) | 무엇을 보여주나 | O point |
|---|---|---|
| `nd_elf/nd_ELF_PO_vs_PS_profile.png` | P–O vs P–S ELF 선프로파일 | ① P–O 강·polar 공유 |
| `nd_elf/clean/nd_ELF_PS3O_clean.png`, `…PS2O2_clean.png` | O 치환 사면체 ELF 슬라이스 | ① O speciation (PS₃O·PS₂O₂) |
| `nd_elf/clean/nd_ELF_PS4_clean.png` (+comp1/modelc) | pristine PS₄ 대조 | host 백본 불변 |
| `nd_dos/nd_dos_pdos_v2.png` | DOS/PDOS (O 2p deep ~−4 eV) | ② O 무해, 갭은 Nd |
| `dos_pdos_smooth/nd_PDOS.png`·`nd_DOS.png`·`nd_4f_excluded_gap.png` | 성분별 PDOS·4f 제외 갭 | ② |
| **`nd_sei/sei_product_gaps_O.png` (新)** | SEI 산물 gap(MP) 막대 | ③ O=wide-gap passivation |

---

## 3. MP 결과 (transfer)

### 3a. SEI / 분해산물 band gap (Materials Project) — O가 만드는 wide-gap
| 산물 | gap (eV) | O유래 | 역할 |
|---|---|---|---|
| LiCl | 6.65 | | 절연(Cl) |
| **Li₃PO₄** | **5.73** | ✅O | **절연 passivation (벌크/GB)** |
| NdPO₄ | 5.55* | ✅O | 절연 passivation (cathode, Nd+O) |
| **Li₂O** | **5.24** | ✅O | **절연 passivation (Li 양극 SEI)** |
| NdOCl | 4.77* | ✅O | 절연 |
| NdCl₃ | 4.30* | | 절연 (cathode) |
| LiNdO₂ | 4.21* | ✅O | 절연 |
| Li₂S | 3.90 | | marginal |
| Nd₂O₃ | 3.81* | ✅O | marginal |
| Nd₂S₃ | 1.79* | | 전도(누설) |
| Li₃P | 0.70 | | **전도(누설)** |
| NdS | 0.00 | | 금속(누설) |

> `*` = Nd 함유 → MP 4f 하한(실제 더 넓음). **순수 O상(Li₃PO₄ 5.73·Li₂O 5.24)은 확정 wide-gap** → O 메시지는 Nd 불확실성과 무관. (tool: `tools/oxidation/sei_product_gaps.py`)

### 3b. oxophilicity (MP descriptor) — O incorporation 친화도
> oxophilicity(M) = Ef/anion(M-sulfide) − Ef/anion(M-oxide) [eV/anion, 클수록 강한 O getter].

| M | oxophilicity | 해석 |
|---|---|---|
| Al | 3.45 | 강한 getter |
| Y | 2.13 | 중간 |
| **Nd** | **1.75** | **≈ Li (특별 X)** |
| Li | 1.67 | 단순 O 운반체 |

> **Nd는 특별한 O-getter가 아님**(≈Li) → O가 들어가 만드는 이점은 "**O 효과**"이지 "Nd 효과"가 아니라는 결정적 근거. O는 어느 carrier로도 들어가나, P–O 강결합(①)이 host 안에서 O를 안정화. (tool: `tools/oxidation/oxophilicity_descriptor.py`, MP 이진산화물 proxy.)

---

## 4. 한 줄 (transfer) + caveat
> **Nd₂O₃ 도핑 이점의 주역은 O다**: P–O 강결합으로 host에 안전하게 박히고(①, 백본 불변), O 2p는 deep spectator라 전자구조에 무해하며(②, 갭 좁힘은 Nd 비용), 분해 시 **Li₃PO₄·Li₂O wide-gap 전자절연 상**을 GB/계면에 만들어 **σ_e를 낮춰** dendrite·self-discharge를 억제 → **cycle↑**(③). Nd는 O 운반·cathode 앵커·aliovalent 역할(이온 σ↓·갭↓은 Nd 비용), 과도핑(x>0.02) 역효과.

**caveat**
- GB/계면 morphology·전자수송 **미계산(추론)** → SSRM·XPS depth·ToF-SIMS 검증 필요(③은 SEI 산물 갭 + bulk-반대방향 논리 기반).
- Nd 함유 gap(*)은 MP 4f 하한. 순수 O상은 확정.
- DFT x=0.2(실험의 10×, 과도핑) → 방향·기전 robust, 절대값 주의.

**데이터 출처**: `db/properties/{nd_icohp,electronic}.json`, `docs/figures/nd_elf/nd_elf_bond_quant.csv` · `icohp_nd_vs_modelc_comp1.csv`; tools `tools/oxidation/{sei_product_gaps,oxophilicity_descriptor,esw_grand_potential}.py`, `tools/figures/plot_nd_sei_gaps.py`.
