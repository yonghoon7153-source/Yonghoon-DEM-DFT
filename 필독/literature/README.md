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
| `camacho_forero_2020.md` | **per-paper deep dive** | **Chem. Mater. 2020 sandwich Wadh — paper #2 v10 method 근거** |

---

## Paper #2 v10 (sandwich) 결정의 핵심 reference

| Authority | Method element | 우리 v9 (deviating) | 권장 (v10) |
|---|---|---|---|
| Camacho-Forero 2020 | Sandwich geometry (no vacuum) | single + 30 Å vacuum | sandwich |
| Camacho-Forero 2020 | /(2A) normalization | /A | /(2A) |
| Camacho-Forero 2020 | No FixAtoms (full relax) | FixAtoms 33% bottom | drop FixAtoms |
| Camacho-Forero 2020 | AIMD 300 K × 20 ps | LBFGS only or 9 ps MQA | 5-10 ps NVT |
| Mo group (Y. Mo) | Thermodynamic SE-cathode stability | — | Lit. comparison |
| Holzwarth | Solid-state battery interface | — | Lit. comparison |
| Janek group | SE/NCM XPS-validated reactions | — | Reaction taxonomy |

==**Camacho-Forero 2020 = 우리와 가장 직접 비교 가능 (LPSCl는 comp1!)**==.

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
