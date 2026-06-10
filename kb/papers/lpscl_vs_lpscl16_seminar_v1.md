# LPSCl vs LPSCl₁.₆ Seminar — Slide Master v1

> **목적**: paper #1 (comp1 vs modelc 단독 비교) head-to-head 발표용 슬라이드 master.
> paper #2 (adhesion, doping cascade, Li₃N, Nd-doping) 모두 분리됨.
> **저장 정책**: 이 문서는 발표 자료의 single source of truth. 새 슬라이드/스크립트
> 추가될 때마다 이 파일에 append + commit.
>
> 마지막 업데이트: 2026-06-10 (slide 1 layout 확정)

---

## 0. 전체 22장 구조 (확정)

| 섹션 | 슬라이드 | 비교 축 |
|---|---|---|
| **A. Intro** | 1 Title / 2 Scope / 3 Pipeline / 4 Headline | 두 시스템 동일 protocol |
| **B. 4 Messages** | 5 전자구조 / 6 σ prefactor / 7 ionic glue / 8 vacancy paradox | 4축 직접 비교 |
| (sub) | 5a k-mesh / 6a mechanism / 6b disorder ensemble / 6c 저온 trade-off / 7a 3-probe / 7b 4d-Cl / 8a shear / 8b cross-check | 각 메시지 보강 |
| **C. Cross-check** | 9 PS₄ universal / 10 bond length / 11 Voronoi / 12 BVSE 5×5×5 / 13 ELF | 5 probe 양쪽 |
| **D. Method-defense** | 14 k-mesh audit / 15 methods / 16 summary | referee 대비 |
| **E. Robustness** | 17 3-probe convergence / 18 Oxidation 4-axis / 19 Constrained ESW | 두 시스템 multi-axis |
| **F. Referee defense** | 20 Tension audit (4 tensions) / 21 Caveats | |
| **G. Outlook** | 22 robust claims + open questions | paper #1 내적 follow-up |

발표 시간별 컷:
- **15분 (preview)**: 1–4 + 5/6/7/8 + 16 = 9장
- **25분 (표준)**: 22장 전체
- **45분 (deep)**: 22장 + SI candidate (per-bond, alpha sensitivity 등)

---

## 1. Slide 1 — Title (Layout v1)

### 페이지 배치 (16:9 가로형 기준)

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│                         [상단 여백 15%]                          │
│                                                                  │
│ ┌────────────────────────────────────────────────────────────┐  │
│ │                                                            │  │
│ │   LPSCl₁.₆가 빠르고 단단한 이유:                          │  │
│ │   ─ 전자구조가 아니라 무질서다 ─                          │  │
│ │                                                            │  │
│ │   A multi-probe DFT/AIMD comparison of                    │  │
│ │   Li₆PS₅Cl vs Li₅.₄PS₄.₄Cl₁.₆                            │  │
│ │                                                            │  │
│ └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│                                                                  │
│       ┌──────────────────────────────────────────────┐          │
│       │  Thesis (한 줄):                              │          │
│       │  "차이는 전자구조가 아니라                    │          │
│       │   Li 공공 + 4d-Cl anti-site 무질서에서 온다." │          │
│       └──────────────────────────────────────────────┘          │
│                                                                  │
│                         [중간 여백 15%]                          │
│                                                                  │
│ ─────────────────────────────────────────────────────────────── │
│                                                                  │
│   안용훈 · BML Lab (한양대) · 지도 김광범 교수                  │
│   2026년 6월 · Internal Seminar Preview                         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 시각 디자인 노트
- **제목 (1줄)**: 진한 색 (Hanyang 청색 or 검정) 36–40pt bold
- **부제 (영문 2줄)**: 회색 22pt italic, 큰 줄간격
- **Thesis box**: 연한 회색 배경, 좌측 강조선 (3px), 18–20pt
  - "전자구조가 아니라"와 "무질서에서 온다"는 색 변환 또는 굵게
- **저자 영역**: 하단 구분선 + 12–14pt
- **색조**: 1차 색 #003876 (학교 청색), 2차 #888 (그레이), 강조 #C8102E (적색, 단어 1-2개에만)
- **로고**: 하단 우측에 학교 로고 (있다면)

### 본문 텍스트 (PPT 직접 복붙용)

**제목**:
```
LPSCl₁.₆가 빠르고 단단한 이유:
─ 전자구조가 아니라 무질서다 ─
```

**부제 (영문)**:
```
A multi-probe DFT/AIMD comparison of
Li₆PS₅Cl vs Li₅.₄PS₄.₄Cl₁.₆
```

**Thesis box**:
```
차이는 전자구조가 아니라
Li 공공 + 4d-Cl anti-site 무질서에서 온다.
```

**저자 footer**:
```
안용훈 · BML Lab (한양대) · 지도 김광범 교수
2026년 6월 · Internal Seminar Preview
```

### 발표 스크립트 (45–60초)

> "안녕하세요. 오늘 paper #1 progress preview 드리겠습니다.
>
> 주제는 stoichiometric LPSCl, 즉 Li₆PS₅Cl과 Cl-rich 변종인 LPSCl₁.₆, Li₅.₄PS₄.₄Cl₁.₆의 head-to-head 비교입니다.
>
> 실험에서는 LPSCl₁.₆가 더 빠르고 더 단단한 걸로 보고되는데, **왜 그런가**가 우리가 답할 질문입니다.
>
> 결론부터 말씀드리겠습니다. **차이는 전자구조에서 오는 게 아닙니다**. PS₄ 골격, 밴드갭, 궤도 character — 다 동일합니다. **차이는 구조적 무질서 — 구체적으로 Li 공공과 4d 자리 Cl anti-site — 에서 옵니다**. 이게 오늘 발표의 thesis입니다.
>
> 다음 약 30분 동안 4개의 메시지로 풀어드리겠습니다. 시작하겠습니다."

### 보조 노트 (Q&A 대비)
- "왜 LPSCl₁.₆를 골랐나?" → 실험 σ가 LPSCl보다 ~3× 빠르고 paper #1에 modelc로 등록된 cell이라 직접 비교 가능
- "왜 두 시스템만?" → controlled head-to-head: same protocol, same pipeline, paper #1 핵심 비교
- "thesis가 너무 단정적이지 않나?" → 4 messages + tension audit (slide 20)에서 정직하게 풀어드림

---

## 2. 변경 이력

| 버전 | 날짜 | 변경 |
|---|---|---|
| v1 | 2026-06-10 | 초안 — 전체 22장 구조 + Slide 1 layout 확정. paper #2 분리. adhesion 제외. |

---

## 3. TODO (다음 작업)

- [ ] Slide 2 (Scope) 본문 + script + layout
- [ ] Slide 3 (Pipeline schematic) — 다이어그램 텍스트
- [ ] Slide 4 (Headline 표) — 색 강조 4행 디자인
- [ ] Slide 5–8 (4 메시지 헤더) — 각 슬라이드 본문 + script + figure source
- [ ] Slide 5a, 6a–6c, 7a–7b, 8a–8b (sub) — 보강 슬라이드들
- [ ] Slide 9–13 (Cross-check) 본문 + script
- [ ] Slide 14–16 (Method-defense)
- [ ] Slide 17–19 (Robustness, NEW)
- [ ] Slide 20–21 (Referee defense, NEW)
- [ ] Slide 22 (Outlook, REVISED — paper #1 only)
- [ ] (Optional) SI candidate slides

---

## 4. Cross-link

- 결과 source: `kb/results/lpscl_vs_lpscl16_v3_comparison.md`
- 4 messages: 동 문서 Part I.2
- Tension audit: `db/properties/literature_tensions_audit.json`
- σ + disorder ensemble: `db/properties/li_transport.json`
- Oxidation 4-axis: `db/properties/oxidation_stability.json`
- Elastic relaxed-ion: `db/properties/elastic.json`
- Voronoi 4-sublattice + BVSE bimodal: `db/compositions/modelc_v3.json` (v3_postprocess_pipeline_v2_8 section)
- Bonds per-site: `db/properties/per_bond_json/{bonds_comp1_k444.json, bonds_modelc_k663.json}`
- DOS / bands / ELF: `db/properties/electronic.json`
- B0 BM3: `db/properties/eos.json`
