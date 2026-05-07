# 🚨 필독 — Literature Database (mirror of db/literature + kb/papers literature notes)

> **Purpose**: 새 session / 새 브랜치 진입 시 method 결정 전에 ==**여기 paper 노트 먼저 참고**==.
> 이 폴더의 ref들이 우리 paper #1 / paper #2 method/narrative 의 ==**근거 문헌**==.
> Source of truth: `db/literature/refs.json` (machine-queryable). 이 폴더는 ==**human-readable mirror + per-paper deep notes**==.

---

## 새 paper 분석 룰

1. **사용자가 PDF 텍스트 / 그림 제공** → 이 폴더에 `<author><year>.md` per-paper 노트 작성
2. **동시에** `refs.json` 에 entry 추가 (id, authors, title, journal, vol, pages, year, DOI, key_content, tags)
3. method 결정 시 우리 코드와의 차이점 (geometry, formula, constraints, sampling) 표로 정리
4. ==**우리 코드 변경 전**== 사용자에게 "이 protocol으로 갈까요?" 확인 후 진행

---

## File map

| File | Type | Content |
|---|---|---|
| `refs.json` | DB | 36 references (db mirror) — source of truth, machine-queryable |
| `verified_refs_2026_05.md` | summary | 2026-05-05 user-verified refs로 정리한 Section 2 narrative |
| `adhesion_literature_review.md` | review | adhesion 계산 literature 7편 review (DFT slab std, MLIP/MTP) |
| `narrative_with_literature_steps.md` | narrative | paper #1 Section 2-4 narrative + 인용 backbone |
| `origin_adhesion_guide.md` | guide | adhesion 계산 origin / motivation 정리 |
| `reviewer_qa_methods.md` | guide | reviewer 예상 질문 + 답변 (Methods) |
| `choi2025_adoption_guide.md` | analysis | Choi 2025 인용 가이드 |
| `zhao2025_critique.md` | critique | Zhao 2025 비판 분석 |
| `camacho_forero_2020.md` | **per-paper deep dive** | **Chem. Mater. 2020 sandwich Wadh — paper #2 v10 SLAB method 근거** |
| `komatsu2022.md` | **per-paper deep dive** | **JPCC 2022 BULK reactivity LPSCl/LiNiO2 = −424 meV/atom (most reactive NCM). Volume change −11~−34%. Reaction products. Paper #2 BULK anchor.** |
| `enaldiev2021.md` | per-paper deep dive | 2D Mater. 2021 TMD twistronic adhesion W(r0, d) binding curves + interpolation formula. **Method precedent for our Phase 1 rigid binding curves**. Different system (vdW 2D, ~0.5 J/m²) but same method. |
| `haruyama2014.md` | **per-paper deep dive** ⭐⭐⭐⭐⭐ | **Chem. Mater. 2014 PIONEER DFT+U slab paper for sulfide-SE/oxide-cathode (LCO/LPS ± LNO buffer). PRIMARY method anchor for paper #2 v5. ANTI-SANDWICH argument (Section 2.1) — predicted v10/v10b inversion. SCL mechanism backing. Adhesion LCO/LPS=0.69 J/m²; Li-vacancy formation Ev table.** |

---

## Paper #2 v10 (sandwich) 결정의 핵심 reference

| Authority | Method category | What it gives | 우리 v10 |
|---|---|---|---|
| **Camacho-Forero 2020** | ⭐ slab + AIMD + sandwich | Direct slab Wadh protocol (LPSCl/Li2S = 1.44 J/m²) | **Method anchor** |
| **Komatsu 2022** (Ong) | bulk thermodynamics | ΔED,min,mutual = −424 meV/atom for LNO/LPSCl + reaction products + volume change | Bulk anchor + chemistry expectations |
| Mo group (Zhu, Richards, Tian) | bulk thermo (general framework) | Stability framework underlying Komatsu | Methodological grandfather |
| Haruyama 2014 (Chem. Mater.) | slab + DFT+U | LiCoO2/β-Li3PS4 space-charge layer | Pending PDF (paper-quality slab anchor) |
| Lian 2020 (ACS AEM) | slab | LCO with multiple SE | Pending PDF |
| Choi 2025 (ACS AEM) | MLIP slab | adoption guide for MLIP-slab figures | Figure style |

### v10 method elements (final)
- **Geometry**: Sandwich (no vacuum, PBC z creates 2 interfaces) — Camacho-Forero
- **Wad 분모**: 2A — Camacho-Forero
- **FixAtoms**: NONE on SE side (Camacho-Forero); NCM bottom 3 atomic layers FixAtoms (literature std for layered oxide bulk reference) — hybrid
- **Sampling**: LBFGS only (UMA MD-at-interface 실패 history; Camacho-Forero AIMD는 VASP에서만 가능)
- **NCM thickness**: 3L conv (9 atomic layers, 42.57 Å) — sufficient for surface/bulk distinction
- **Cathode chemistry**: LiNiO2 (paper #1 일관성). NCM811 paper revision option.
- **Expected chemistry** (Komatsu): Ni3S2 nucleus, Li3PO4, Li2S, LiCl phase separation. Volume −11% chemical, −34% at 4.5V.

---

## 새 paper 추가 절차 (사용자 PDF 제공 시)

```
1. Read PDF text/figures 제공 받음
2. db/literature/refs.json 에 entry 추가 (id = lastname<year>)
3. 필독/literature/refs.json 동기화 (cp from db/)
4. 필독/literature/<id>.md per-paper 노트 작성 (이 README의 camacho_forero_2020.md 형식 참고)
5. 우리 코드/method와 비교 표 + action items
6. CLAUDE.md 또는 CODE_INVENTORY.md 의 "참고 문헌" 항목 업데이트 (필요 시)
7. commit + push
```

---

## 검증된 paper 목록 (refs.json id 기준, 2026-05-07 시점 36개)

### Argyrodite structure / synthesis
- deiseroth2006, kraft2018, adeli2019, famprikis2019, gautam2023, yuwagemaker2023, yuwagemaker2024_decoding

### Mechanical (B0, E, Cij)
- deng2016, sakuda2013, torii2025, ketter2025

### Conductivity / Li transport
- ohno2021, zhu2015, wilkening2019, zhang2024_ionic_potential, _DELETED_wagemaker2020_lideficient

### Interface / Adhesion / SE-cathode
- **camacho_forero_2020 ⭐** (paper #2 method anchor)
- zuo2023, sicolo2022, choi2025, zhao2025, jia2025, xiong2022

### MLIP / DFT methodology
- ong2013, ransom2023, pustorino2025, ayadi2024, damore2022, kozuka2025

### Bader / structure analysis
- bader1990, henkelman2006, shannon1976, minerals2019

### Specific compound
- wang2019_li6ps5cl0p5br0p5

### EOS
- birch1947

### Summary
- literature_summary_2026_05

---

#literature #must-read #db-mirror #per-paper-notes #paper2-adhesion #camacho-forero
