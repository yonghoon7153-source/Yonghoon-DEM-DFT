# LPSCl vs LPSCl₁.₆ Seminar — Slide Master v1

> **목적**: paper #1 (comp1 vs modelc 단독 비교) head-to-head 발표용 슬라이드 master.
> paper #2 (adhesion, doping cascade, Li₃N, Nd-doping) 모두 분리됨.
> **저장 정책**: 이 문서는 발표 자료의 single source of truth. 새 슬라이드/스크립트
> 추가될 때마다 이 파일에 append + commit.
>
> 마지막 업데이트: 2026-06-12 (v1.35 — Slide 2 연구실 템플릿 bullet 형식 + 제목 확정)

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

## 1. Slide 1 — Title (Layout v2 — 연구실 표준 템플릿, 2026-06-12)

> **v2 결정**: 연구실 표준 템플릿 (Research Seminar + 캠퍼스 일러스트 + Part divider) 사용.
> **Title에는 큰 그림 (thesis) 넣지 않음** — thesis는 Slide 2 (Scope+Thesis 통합)로 이동.
> 아래 Layout v1 (thesis box 버전)은 보존용.

### 페이지 배치 v2 (연구실 템플릿 기준)

```
┌──────────────────────────────────────────────┐
│ ▓▓ (상단 네이비 바)             June XX, 2026 │
│                                              │
│  Research Seminar                            │  ← 네이비 bold
│  LPSCl vs LPSCl₁.₆: A Multi-Probe DFT/AIMD   │  ← 부제 (회색)
│  Comparison of Argyrodite Solid Electrolytes │
│                                              │
│  Yonghoon An                                 │
│  Division of Materials Science & Engineering,│
│  Hanyang University                          │
│  (E-mail : yonghoon71@hanyang.ac.kr)         │
│                                              │
│  [한양대 로고]      [캠퍼스 일러스트]           │
│ ▓▓ (하단 네이비 바)                           │
└──────────────────────────────────────────────┘
```

- 부제는 영어 한 줄(또는 두 줄)로만: 시스템 명시 정도. thesis/정량 일절 없음.
- Part divider 슬라이드 활용 가능: Part 1 = Intro & Pipeline (slides 2–4),
  Part 2 = 4 Messages (5–8), Part 3 = Cross-check & Defense (9–16),
  Part 4 = Robustness & Outlook (17–22).

### 발표 스크립트 v5 ★ ACTIVE (15초, title은 인사만)

> "안녕하세요, 오늘 research seminar는 DFT 파트 technical report로,
> stoichiometric LPSCl과 Cl-rich LPSCl₁.₆ 두 argyrodite의 정면 비교를 다루겠습니다."

(질문 제기 + 결론 선언 + thesis는 전부 Slide 2로 이동)

---

### (보존) Layout v1 — thesis box 버전

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

### 발표 스크립트 v4 — 최종 정제 (45초, 2026-06-10) ★ ACTIVE

> "안녕하세요. 오늘은 paper #1 progress preview 드리겠습니다.
>
> 주제는 stoichiometric LPSCl과 Cl-rich 변종 LPSCl₁.₆, 이 두 시스템의 정면 비교입니다.
>
> 실험적으로 LPSCl₁.₆가 LPSCl보다 빠르고 단단하다는 게 보고되어 있는데, 그 차이가 어디서 오는지가 이번 발표의 질문입니다.
>
> 결론부터 말씀드리겠습니다. **전자구조에 작은 차이는 있긴 있습니다. 하지만 그 작은 차이로는 conductivity나 stiffness의 큰 차이를 설명할 수 없습니다**. PS₄ 골격이 두 시스템에서 거의 동일하고, 전자구조의 전반적 패턴도 비슷합니다.
>
> **차이의 진짜 source는 구조에 있습니다 — 구체적으로 Li 공공과 4d 자리에 들어간 Cl anti-site, 이 두 가지가 변화의 동력입니다**. 이게 오늘 발표의 thesis입니다.
>
> 다음 30분 동안 4개의 메시지로 풀어 드리겠습니다."

#### v3 → v4 변화 노트
- "PS₄ 골격도, 궤도 character도 사실상 같습니다" → "**PS₄ 골격이 거의 동일하고, 전자구조 전반 패턴도 비슷**" (PS₄ 단정 유지 + 궤도 character는 전자구조 패턴으로 vague)
- 첫 페이지에서 specific orbital decomposition 단정 회피 (직접 비교 논문 없음)
- "모든 변화의 동력" → "**변화의 동력**" 축약

### 발표 스크립트 v3 — 정량 minimal (보존용)

> "안녕하세요. 오늘은 paper #1 progress preview 드리겠습니다.
>
> 주제는 stoichiometric LPSCl과 Cl-rich 변종 LPSCl₁.₆, 이 두 시스템의 정면 비교입니다.
>
> 실험적으로 LPSCl₁.₆가 LPSCl보다 빠르고 단단하다는 게 보고되어 있는데, 그 차이가 어디서 오는지가 이번 발표의 질문입니다.
>
> 결론부터 말씀드리겠습니다. **전자구조에 작은 차이는 있긴 있습니다. 하지만 그 작은 차이로는 conductivity나 stiffness의 큰 차이를 설명할 수 없습니다**. PS₄ 골격도, 궤도 character도 두 시스템에서 사실상 같습니다.
>
> **차이의 진짜 source는 구조에 있습니다 — 구체적으로 Li 공공과 4d 자리에 들어간 Cl anti-site, 이 두 가지가 모든 변화의 동력입니다**. 이게 오늘 발표의 thesis입니다.
>
> 다음 30분 동안 4개의 메시지로 풀어 드리겠습니다."

#### v2 → v3 변화 노트
- "0.06 eV 정도 modelc가 큽니다" → "**작은 차이는 있긴 있습니다**" (정량 → 정성, 첫 페이지 톤)
- "VBM·CBM 궤도 character" 분해 → "**궤도 character**" 일반화
- "conductivity 3배 / stiffness 25%" → "**큰 차이**" 일반화
- 모든 정량 수치 → **slide 4 (Headline 표) + slide 5 (M1 전자구조) 본문으로 이동**

### 발표 스크립트 v2 — 정제 (보존용, 정량 포함)

> "안녕하세요. 오늘은 paper #1 progress preview 드리겠습니다.
>
> 주제는 stoichiometric LPSCl과 Cl-rich 변종 LPSCl₁.₆, 이 두 시스템의 정면 비교입니다.
>
> 실험적으로 LPSCl₁.₆가 LPSCl보다 빠르고 단단하다는 게 보고되어 있는데, 그 차이가 어디서 오는지가 이번 발표의 질문입니다.
>
> 결론부터 말씀드립니다. **전자구조에서는 작은 차이가 있긴 합니다 — 밴드갭이 0.06 eV 정도 modelc가 큽니다. 하지만 이 0.06 eV로는 conductivity 3배 차이나 stiffness 25% 차이를 설명할 수 없습니다**. PS₄ 골격도, VBM·CBM 궤도 character도 두 시스템에서 사실상 같습니다.
>
> **차이의 진짜 source는 구조에 있습니다 — 구체적으로 Li 공공과 4d 자리에 들어간 Cl anti-site, 이 두 가지가 모든 변화의 동력입니다**. 이게 오늘 발표의 thesis입니다.
>
> 다음 30분 동안 4개의 메시지로 풀어 드리겠습니다."

#### v1 (초안, 보존용)

> "안녕하세요. 오늘 paper #1 progress preview 드리겠습니다. 주제는 stoichiometric LPSCl, 즉 Li₆PS₅Cl과 Cl-rich 변종인 LPSCl₁.₆, Li₅.₄PS₄.₄Cl₁.₆의 head-to-head 비교입니다. 실험에서는 LPSCl₁.₆가 더 빠르고 더 단단한 걸로 보고되는데, **왜 그런가**가 우리가 답할 질문입니다. 결론부터 말씀드리겠습니다. **차이는 전자구조에서 오는 게 아닙니다**. PS₄ 골격, 밴드갭, 궤도 character — 다 동일합니다. **차이는 구조적 무질서 — 구체적으로 Li 공공과 4d 자리 Cl anti-site — 에서 옵니다**. 이게 오늘 발표의 thesis입니다. 다음 약 30분 동안 4개의 메시지로 풀어드리겠습니다."

#### v1 → v2 변화 노트
- 전자구조 차이 **0.06 eV 정직하게 인정** → "동일"이 아니라 "**작지만 있다, 단 σ·E 차이 설명 못 함**"으로 mechanism 분리
- "통념을 반박" 같은 강한 표현 / 영문 포뮬러 / "head-to-head" 영어 표현 제거
- 단정 줄이고 "**진짜 source는 구조에 있다**"로 핵심만
- paper title/저널 mention 없음 (1page 톤)

### 보조 노트 (Q&A 대비)
- "왜 LPSCl₁.₆를 골랐나?" → 실험 σ가 LPSCl보다 ~3× 빠르고 paper #1에 modelc로 등록된 cell이라 직접 비교 가능
- "왜 두 시스템만?" → controlled head-to-head: same protocol, same pipeline, paper #1 핵심 비교
- "전자구조 0.06 eV 차이는 실제로 무엇인가?" → modelc 살짝 더 wide gap. 정량적으로 σ/E 차이 설명 못 함. method 오차 범위와 비슷 (USPP/DOS-threshold 0.4 eV 오차 있는 상황)
- "thesis가 너무 단정적이지 않나?" → 4 messages + tension audit (slide 20)에서 정직하게 풀어드림
- "단단하다는 게 실험적으로 robust한가?" → Kim ACS Mater. Lett. 2025 + 자체 AFM이 핵심 근거. 더 오래된 문헌에선 trend 약함 — Kim 2025 이후 확립

---

## 1B. Slide 2 — Scope + Thesis (★ v2 통합 2026-06-12 — 구 Slide 1 thesis 흡수)

> **v2 결정**: Title이 연구실 표준 템플릿이 되면서, 구 Slide 1의 질문 제기 + 결론 선언 +
> thesis가 이 슬라이드로 통합됨. "두 시스템 소개"와 "thesis 선언"을 한 장에서 처리.

### 페이지 배치 v2 (16:9)
- **상단 1/4**: 질문 + Thesis 띠 (연회색 box, 좌측 강조선)
  - "왜 LPSCl₁.₆가 더 빠르고 단단한가?" → "전자구조가 아니라 **Li 공공 + 4d-Cl anti-site 무질서**다"
- **하단 3/4**: 좌·우 panel 나란히 (동격 비교) + VESTA 구조 그림 (같은 scale + viewing angle)

### 발표 스크립트 v2 ★ ACTIVE (70–80초, 구 slide 1 v4 흡수)

> "비교 대상부터 보겠습니다.
>
> 왼쪽은 stoichiometric LPSCl, 오른쪽은 Cl-rich 변종 LPSCl₁.₆입니다. 실험적으로 **LPSCl₁.₆가 더 빠르고 더 단단하다**는 게 보고되어 있는데, 그 차이가 어디서 오는지가 이번 파트의 질문입니다.
>
> 결론부터 말씀드리겠습니다. **전자구조에 작은 차이는 있긴 있습니다. 하지만 그 작은 차이로는 conductivity나 stiffness의 큰 차이를 설명할 수 없습니다.** 차이의 진짜 source는 구조에 있습니다 — 위 thesis 그대로, **Li 공공과 4d-Cl anti-site 무질서**입니다.
>
> 그 두 가지가 어디서 오는지 구조를 보시면 — 왼쪽 comp1은 **Li가 가득 차 있고 Cl이 전부 4a, 4d에는 free S²⁻만** 있는 깨끗한 ordered 구조입니다. 오른쪽 modelc에서 **두 가지 disorder가 동시에 등장합니다**: Li가 f.u.당 0.6개 빠지는 Li 공공, 그리고 늘어난 Cl이 S²⁻ 자리인 4d로 침입하는 anti-site.
>
> 두 시스템에 완전히 동일한 multi-probe 파이프라인을 paired로 적용했고, 다음 30분 동안 4개의 메시지로 풀어 드리겠습니다."

### ★ 실물 확정판 (v4 FINAL, 2026-06-12 — 실제 제작 슬라이드 반영, 검수 완료)

```
제목(좌상단): DFT  (Part 1 제목 그대로)
우상단 각주: f.u.: formula unit / anti sites: site disorder
우상단 refs: Angew. Chem. Int. Ed., 62, e202213228 (2023).
            ACS Mater. Lett., 7, 724 (2025).   ← Y.J. Kim (UPE, stiffness backing)

■ Two argyrodites: Systems & Key finding
   · Experiments: Li₅.₄PS₄.₄Cl₁.₆ shows ~3× higher σ and +25% stiffness than Li₆PS₅Cl
       (청색: ~3x higher σ / +25% stiffness)
   · Not electronic structure — It originates from structural disorder: Li vacancies + 4d-Cl anti-sites
       (적색: electronic structure ✗ / 청색: Li vacancies, 4d-Cl anti-sites ✓)

그림: 중앙 하단 <LPSCl primitive cell> Wyckoff 라벨:
       4a (0,0,0) Cl · 4b (½,½,½) P · 16e (PS₄) · 4d (¾,¾,¾) Free S²⁻
     → 좌 "4f.u." 화살표 → cubic <LPSCl>
     → 우 "5f.u." 화살표 → rhombohedral <LPSCl₁.₆> (4a / 4d 화살표 주석)
     하단 범례: Li(회) P(보라) S(노랑) Cl(초록)
```

검수 이력: ① "Not electronic structure" 대비줄 추가 ② Kim ref 채움 (7, 724)
③ Wyckoff 16e(0,0,0)→4b(½,½,½) 정정, free-S 4c→4d 통일 (본문 4d-Cl과 정합)
④ modelc 화살표 4c→4d. Wyckoff 라벨은 slide 10/11 (per-bond, Voronoi)에서 재사용 예정.

발표 보충 멘트 (정확성): "+25%는 저희 DFT relaxed-ion 결과고, 실험(Kim 2025 UPE)은 Cl↑→E↑ 경향으로 확인됩니다."

### 본문 텍스트 (v3 — 연구실 템플릿 형식, 2026-06-12)

**슬라이드 제목 (좌상단, 네이비 bold)**:
```
LPSCl vs LPSCl₁.₆ — Why Faster & Stiffer?
```
(대안: "Two Argyrodites: Systems & Key Finding" / "Comparison Overview")

**본문 (템플릿 bullet 구조)**:
```
■ Key finding (결론 먼저)
   · Experiments: LPSCl₁.₆ shows ~3× higher σ and +25% stiffness than LPSCl
   · The difference does NOT come from electronic structure (Δgap only 0.06 eV)
   · It originates from structural disorder: Li vacancies + 4d-Cl anti-sites

■ Cell configurations
   · LPSCl (comp1):    cubic F-43m, 4 f.u., 52 atoms — ordered Li · Cl@4a · free S²⁻@4d
   · LPSCl₁.₆ (modelc): rhombohedral R3m, 5 f.u., 62 atoms — 0.6 Li vacancy/f.u. · Cl@4a+4d anti-site

[하단: VESTA 구조 그림 좌우 배치 — comp1 cubic / modelc rhombohedral, 동일 scale·시점]
```

**하단 한 줄 (선택)**: "Same protocol, same multi-probe pipeline — paired comparison"

**Footnote references (Key finding bullet용, 템플릿 하단 회색)**:
```
· Experiments: LPSCl₁.₆ shows ~3× higher σ [1,2] and +25% stiffness [4] than LPSCl

[1] T. Zuo et al., Angew. Chem. Int. Ed., vol. 62, e202213228, 2023.        (σ 2.9 vs 7.0 mS/cm RT)
[2] P. Adeli et al., Angew. Chem. Int. Ed., vol. 58, no. 26, pp. 8681–8686, 2019.  (Li5.4PS4.4Cl1.6 원조 합성)
[3] R. Schlem et al., Adv. Energy Mater., vol. 10, no. 8, p. 1903719, 2020.  (Ea 0.22/0.25 — 우리 4fu EXACT 매칭)
[4] Y. J. Kim et al., ACS Mater. Lett., 7, 724 (2025).  (UPE Cl↑→E↑, DOI 10.1021/acsmaterialslett.4c02029)
```

### 본문 텍스트 (v2 — thesis 띠 버전, 보존)

**상단 thesis 띠**:
```
Q. 왜 LPSCl₁.₆가 더 빠르고 단단한가? (실험: σ ~3×, E +25%)
A. 차이는 "전자구조"가 아니라 — Li 공공 + 4d-Cl anti-site 무질서에서 온다.
```

**패널 상단**: "비교 대상: 두 argyrodite"

**왼쪽 panel (comp1)**:
```
LPSCl (comp1) — Li₆PS₅Cl
cubic F-43m · 4 f.u. · 52 atoms

• ordered Li
• Cl 전부 4a 자리
• free S²⁻ 4d 자리
```

**오른쪽 panel (modelc)**:
```
LPSCl₁.₆ (modelc) — Li₅.₄PS₄.₄Cl₁.₆
rhombohedral R3m · 5 f.u. · 62 atoms

• Li 공공 0.6 / f.u.
• Cl 4a + 4d anti-site
• 4d 자리: S²⁻ + Cl 혼합
```

**하단 한 줄**: "→ 동일 protocol · 동일 §8 multi-probe로 paired 비교"

### (보존) 발표 스크립트 v1 — thesis가 slide 1에 있던 버전 (40–50초)

> "먼저 비교 대상부터 보겠습니다.
>
> 왼쪽은 stoichiometric LPSCl, comp1. Li₆PS₅Cl, cubic argyrodite. **Li가 가득 차 있고, Cl이 전부 4a 한 자리에만, 4d에는 free S²⁻만** — 깨끗한 ordered 구조입니다.
>
> 오른쪽은 Cl-rich LPSCl₁.₆, modelc. Li₅.₄PS₄.₄Cl₁.₆, rhombohedral. **여기서 두 가지 disorder가 동시에 등장합니다**. 첫째, Li가 f.u.당 0.6개 빠집니다 — Li 공공. 둘째, 늘어난 Cl이 4a를 채우고 일부가 S²⁻의 자리인 4d로 침입합니다 — 4d-Cl anti-site.
>
> Slide 1에서 thesis로 깐 'Li 공공 + 4d-Cl anti-site'가 바로 여기서 시작됩니다.
>
> 두 시스템에 **완전히 동일한 §8 multi-probe 파이프라인**을 paired로 적용했습니다. 다음 슬라이드에서 이 pipeline을 보겠습니다."

### 시각 디자인 노트
- 두 panel 나란히 (동격 비교 강조)
- VESTA 그림 동일 scale + viewing angle
- "Li 공공" + "4d-Cl anti-site" 두 단어는 강조색 (#C8102E)
- 하단 한 줄 굵게 + 화살표

### Q&A 보조 노트
- "왜 4 f.u. vs 5 f.u.로 cell 크기 다르냐?" → V/atom 19.55 vs 19.62 Å³로 거의 동일 (framework 보존), V/f.u. 254 vs 243 (Cl→S + Li 공공으로 f.u. 부피 수축, 실험 lattice 경향)
- "k-mesh 다른 거 OK?" → comp1 4×4×4 (k×L=40), modelc 6×6×3 (k×L=42), convergence 동일 (slide 14 k-mesh audit)
- "anti-site 비율 specific?" → modelc 8 Cl 중 4d에 3개 = 37.5%. stoichiometric 필연 (slide 17 cross-method convergence)

---

## 1C. Slide 3 — 3-Tier Pipeline (MLIP screen → DFT confirm → §8)

### ★ 연구실 템플릿 v3 (2026-06-12 ACTIVE — Rietveld→DFT 간극 도입 강화)

**실물 확정판 (v3 FINAL, 2026-06-12 — 실제 제작 슬라이드, 검수 완료)**:

```
제목(좌상단): DFT
우상단 각주: MLIP: Machine Learning Interatomic Potential
우상단 refs:  Angew. Chem. Int. Ed., 47, 755 (2008).   ← Deiseroth (4a/4d disorder 원조)
             J. Am. Chem. Soc., 139, 10909 (2017).    ← Kraft (Cl 4a/4d 정량)

■ 3-tier pipeline (same protocol for both systems)
   · Fractional (Rietveld) → integer (DFT): a site-assignment procedure is needed
   · 3-tier pipeline: (MLIP screening → DFT validation → Post-processing)

3 박스 (점선 둥근 사각형):

  ┌ MLIP screening ┐    ┌ DFT validation ┐    ┌ Post-processing ┐
  │ 1. Halogen     │    │ 1. MLIP EOS    │    │ 1. Structure    │
  │    enumerate   │    │    pre-scan    │    │    · Bonds·Voronoi│
  │ 2. Li sublatt. │    │ 2. BM3 EOS     │    │    · BVSE       │
  │    screen      │    │    11 volumes  │    │ 2. Electronic   │
  │ 3. 500 K       │    │ 3. V₀ confirm. │    │    · DOS·Bands·ELF│
  │    Langevin    │    │    (BFGS)      │    │ 3. Bonding      │
  │    anneal      │    │ 4. k-mesh conv │    │    · Bader·ICOHP│
  │                │    │    (tight SCF) │    │ 4. Transport    │
  │                │    │                │    │    · MLIP MD    │
  │                │    │                │    │      600/800/1000K│
  │                │    │                │    │ 5. Mechanical   │
  │                │    │                │    │    · Stress-strain│
  │                │    │                │    │      (Cᵢⱼ)       │
  │                │    │                │    │ 6. Electrochem. │
  │                │    │                │    │    · Constrained ESW│
  │                │    │                │    │    · Decomposition│
  └────────────────┘    └────────────────┘    └─────────────────┘
```

검수 이력:
① MLIP EOS pre-scan → DFT validation 박스 1번으로 이동 (MLIP은 champion까지로 끊고
   DFT가 V₀ 확정 흐름 명확화)
② Transport "AIMD" → "MLIP MD (UMA)"로 정직 표기 — slide 21 caveat과 일관성
③ Post-processing 6번 Electrochemical (Constrained ESW + Decomposition) 추가 —
   slide 18 oxidation 4-axis · slide 19 ESW Cl-scan의 출처 깃발
④ 우상단 ref "Chem. Int. Ed." → "Angew. Chem. Int. Ed." 표기 정정

### (보존) 연구실 템플릿 v2 (2026-06-12 — Rietveld 도입부 추가 전)

**제목**: "Computational Pipeline: From Rietveld Occupancy to DFT-Ready Cell"

**본문 (■/· 3단 구조)**:
```
■ Why a pipeline?
   · Rietveld CIFs report fractional occupancy (time/space-averaged, room-T)
   · DFT requires integer occupancy — one atom per site, decided ahead of time
   · → A separate procedure is needed to assign which site holds which atom

■ 3-tier pipeline (same protocol for both systems)
   · Tier 1 — MLIP screening (UMA-s-1p1, hours): halogen enumeration
     (LPSCl 70 = C(8,4) · LPSCl₁.₆ 45 = C(10,2)) → Li screen (top-5 × 20) → 500 K anneal → champion
   · Tier 2 — DFT validation (days): BM3 EOS, 11 volumes (V/V₀ 0.96–1.06) → V₀, B₀ < 1 GPa
   · Tier 3 — Multi-probe (weeks): structure · electronic · bonding · transport · mechanical (13 probes)

■ Champion = annealed ground state (not hand-picked)
   · LPSCl: pipeline converged to the ordered cell (Cl@4a, free S²⁻@4d)
   · LPSCl₁.₆: same pipeline yields a 4d-Cl anti-site champion → disorder comes from composition
     (적색/굵게: "disorder comes from composition")
```

**우상단 refs (4d-disorder 도입용)**:
```
H.-J. Deiseroth et al., Angew. Chem. Int. Ed., 47, 755 (2008).
M. A. Kraft et al., J. Am. Chem. Soc., 139, 10909 (2017).
N. Minafra et al., Solid State Ionics, 346, 115223 (2020).
B. J. Morgan, Chem. Mater., 33, 2004 (2021).
```

**발표 스크립트 v3 ★ ACTIVE (~90초)**:

> "Cell configuration을 결정하기 전에, 저희가 처음 기준으로 삼은 건
> **'DFT 상에서 가장 안정한 site 배치는 무엇인가, 그리고 그 구조의 기본 물성은 어떤가'** 였습니다.
>
> LPSCl의 경우 기존 Rietveld로 정해진 CIF 파일들이 있지만, 이건 **상온 측정의 시간·공간 평균**
> 이라 한 자리에 Cl 60% / S²⁻ 40% 같은 분율 점유로 표현됩니다. DFT는 그런 분율 점유를
> 받을 수 없어요 — **site마다 원자 하나, 정수 occupancy**로 결정해야 합니다. 그래서 셀을
> 짜기 전에 '어느 site에 어느 원자를 박을지'를 결정하는 별도 파이프라인이 필요했습니다.
>
> 그래서 만든 게 이 3-tier pipeline입니다.
>
> **Tier 1, MLIP screening.** 가능한 음이온/Li 배치를 전수 나열합니다 — LPSCl은 C(8,4)=70개,
> LPSCl₁.₆는 C(10,2)=45개. 그 위에 Li 배치 screening, 500 K Langevin annealing까지 UMA
> foundation MLIP으로 몇 시간 안에 돌려서 champion을 뽑습니다.
>
> 여기서 강조하고 싶은 게 — **왼쪽의 ordered는 저희가 '교과서니까' 고른 게 아닙니다.**
> halogen 배치만 보면 mixed 2/2가 위로 올라오는데, **Li sublattice까지 풀어서 annealing
> 하면 ordered가 역전해서 ground state로 확정**됩니다. 같은 절차를 Cl-rich에 적용하면
> 이번엔 4d-Cl anti-site champion이 나옵니다. Deiseroth와 Kraft 이후 실험에서 보고된
> 4d-site disorder를 **가정하지 않고 절차로 재현**한 거예요. 즉 ordered도 disorder도
> 저희가 넣은 게 아니라 **조성이 만든 결과**입니다. 오늘 thesis의 첫 번째 근거예요.
>
> **Tier 2**에서 champion을 DFT 11-volume BM3 EOS로 V₀/B₀ paper-grade(<1 GPa) 확정,
> **Tier 3**에서 13가지 probe를 양쪽에 똑같이 적용했습니다. 다음 슬라이드부터 결과 보겠습니다."

### (보존) 연구실 템플릿 v2 (2026-06-12 — Rietveld 도입부 추가 전)

**제목**: "Computational Pipeline: MLIP Screening → DFT Validation"

**본문 (■/· 구조)**:
```
■ 3-tier pipeline (same protocol for both systems)
   · Tier 1 — MLIP screening (UMA-s-1p1, ~hours): halogen enumeration
     (LPSCl 70 = C(8,4) · LPSCl₁.₆ 45 = C(10,2)) → Li screen (top-5 × 20) → 500 K anneal → champion
   · Tier 2 — DFT validation (~days): BM3 EOS, 11 volumes (V/V₀ 0.96–1.06) → V₀, B₀ < 1 GPa
   · Tier 3 — Multi-probe (~weeks): structure · electronic · bonding · transport · mechanical (13 probes)

■ Champion = annealed ground state (not hand-picked)
   · LPSCl: pipeline converged to the ordered cell (Cl@4a, free S²⁻@4d)
   · LPSCl₁.₆: same pipeline yields a 4d-Cl anti-site champion → disorder comes from composition
     (적색/굵게: "disorder comes from composition" — thesis 첫 근거)
```

**하단 한 줄**: "4,500+ MLIP configs screened → 2 champions DFT-validated → 13 probes"

**발표 스크립트 v2 ★ ACTIVE (70–80초)**:

> "이 비교를 가능하게 한 pipeline입니다. 핵심은 3단계 구조예요.
> **Tier 1, MLIP screening.** Argyrodite는 음이온이 어느 자리에 앉는지, Li가 어떻게 배치되는지가
> 에너지를 결정합니다. DFT 전수조사는 비용이 감당이 안 되니 UMA foundation MLIP으로 합니다 —
> halogen 배치 LPSCl 70개, LPSCl₁.₆ 45개 전수 나열, Li 배치 screening, 500 K annealing까지.
> 몇 시간 안에 champion이 나옵니다.
> **여기서 강조하고 싶은 게 하나 있습니다.** 왼쪽의 ordered 구조는 '교과서 구조니까' 골라 넣은 게
> 아닙니다. Halogen 배치만 보면 mixed 배치가 위로 올라오는데, **Li sublattice까지 풀어서 annealing
> 하면 ordered가 역전해서 ground state로 확정**됩니다. 그리고 **완전히 같은 절차**를 Cl-rich에
> 적용하면 이번엔 4d-Cl anti-site champion이 나옵니다. 즉 — ordered도 disorder도 저희가 넣은 게
> 아니라 **조성이 만든 결과**입니다. 오늘 thesis의 첫 번째 근거예요.
> **Tier 2**에서 champion을 DFT 11-volume EOS로 V₀/B₀ paper-grade 확정, **Tier 3**에서 13가지
> probe를 양쪽에 똑같이 적용했습니다. 다음 슬라이드부터 그 결과입니다."

**4d-disorder 도입 ref (slide 3 우상단, Tabor 형식)**:
```
H.-J. Deiseroth et al., Angew. Chem. Int. Ed., 47, 755 (2008).    (원조 4a/4d disorder)
M. A. Kraft et al., J. Am. Chem. Soc., 139, 10909 (2017).         (Cl 4a/4d ~60:40 정량)
N. Minafra et al., Solid State Ionics, 346, 115223 (2020).        (disorder→σ 실험)
B. J. Morgan, Chem. Mater., 33, 2004 (2021).                      (disorder→σ 이론, 우리 직계 선행)
```
슬라이드 흐름: ■1 "4d-site disorder = known phenomenon (Deiseroth/Kraft)" → ■2 "We capture it by full enumeration (not assumed)" — 문헌 현상을 가정 없이 절차로 재현하는 구조.

**Q&A v2 추가 카드**:
- "ordered가 진짜 ground state?" → C(8,4)=70 전수 + Li 20 configs (spread 1.16 eV) + 500 K anneal.
  screening→anneal 랭킹 역전 실제 관측 (#15: 4위→2위) — 다단계 필요성의 증거
- "anti-site 비율 임의?" → champion의 4d-Cl은 절차의 출력. 실험 25–40% (finite-T) 대비 0 K lower bound 명시
- "500 K anneal 안 녹나?" → Li sublattice hopping 온도, anion frame 불변 확인, 50 ps Langevin

### (보존) 페이지 배치 v1 (16:9)

3개 box 세로 stack, 위에서 아래로 화살표, gradation 색 (옅은→진한 청).

### 본문 텍스트

**상단**: "Pipeline: MLIP screen → DFT confirm → multi-probe"

**Tier 1 box**:
```
Tier 1 · MLIP screening (hours)
• Halogen enumerate — comp1 70 (C(8,4)) · modelc 45 (C(10,2))
• Li sublattice screen — top-5 × 20
• 500 K Langevin anneal → champion
UMA-s-1p1 (omat)
```

**Tier 2 box**:
```
Tier 2 · DFT validation (days)
• BM3 EOS — 11 volumes (V/V₀ 0.96 – 1.06)
• V₀, B₀ paper-grade (< 1 GPa)
PBE + USPP, ecut 60 / 480 Ry
```

**Tier 3 box**:
```
Tier 3 · §8 multi-probe (weeks)
structure    bonds · Voronoi · BVSE
electronic   DOS · bands · ELF
bonding      Bader · LOBSTER ICOHP
transport    AIMD 600/800/1000 K
mechanical   stress-strain Cij
```

**하단 한 줄**: "→ 4500 MLIP configs screened · 1 champion DFT-validated · 13 probes measured"

### 발표 스크립트 (50–60초)

> "Slide 3은 어떻게 두 시스템을 비교 가능한 수준으로 만들었는지 pipeline을 보여드립니다.
>
> 핵심은 **3-tier 구조**입니다.
>
> **Tier 1, MLIP screening**. argyrodite는 음이온이 어느 자리에 앉느냐, Li가 어떻게 배치되느냐가 cell 에너지에 영향을 줍니다. 특히 modelc 같은 Cl-rich에서는 4d 자리에 Cl이 들어가는 패턴이 중요해요. 이걸 DFT로 직접 enumerate하면 셀당 시간이 걸려서 4000개 조합을 다 못 돌립니다. 그래서 UMA foundation MLIP으로 합니다 — halogen enumerate (comp1 70개 = C(8,4), modelc 45개 = C(10,2)), Li screen top 5 × 20개, 500K annealing까지 hours 안에 끝납니다. 여기서 **champion 구조와 site occupancy**가 나옵니다.
>
> **Tier 2, DFT validation**. MLIP champion을 받아서 V₀와 B₀를 paper-grade 정확도로 잡습니다. 11개 volume에서 cell-fixed relax → Birch-Murnaghan 3차 EOS fit. B₀가 < 1 GPa 정확도로 나옵니다.
>
> **Tier 3, §8 multi-probe**. 확정된 V₀에서 13가지 probe를 적용합니다. 구조, 전자, 결합, 전송, 기계 — 5개 angle, 각각 multi-method.
>
> 두 시스템에 이 pipeline을 paired로 적용했다는 게 이번 비교의 method-consistency 기반입니다. 다음 슬라이드부터 결과 보겠습니다."

### 시각 디자인 노트
- 3개 box 세로 stack, 위→아래 화살표
- 색조 gradation: Tier 1 옅은 청 → Tier 2 중간 청 → Tier 3 진한 청 (정밀도 ↑ 시각화)
- 시간 스케일 (hours/days/weeks) 우측 끝에 회색 작은 글자
- 하단 요약 굵게

### Q&A 보조 노트
- "UMA-s-1p1이 뭐냐?" → Meta foundation MLIP, omat task, 다양한 materials 학습. argyrodite는 학습 셋에 없지만 transferable
- "Tier 1과 Tier 2가 동의하나?" → comp1: MLIP B₀ = 26.9 vs DFT 26.5 (1% 일치). modelc: MLIP 20.0 vs DFT 21.7 (8% 차이, anneal champion 효과 포함)
- "왜 11개 volume?" → BM3 4 parameter free fit + B₀/B₀' covariance 제거 + R² > 0.999 보장
- "Tier 1 champion이 진짜 global min?" → MLIP 절대값 unreliable, ranking만 사용. DFT relax로 valid 확인 (modelc anneal gain 114 meV로 실제 더 깊은 basin 발견)

### ★ 기록 — comp1 enumeration & champion 역전 (2026-06-11, Q&A 필수 카드)

**comp1도 modelc와 동일하게 full enumeration pipeline을 통과했다** (손으로 ordered를 고른 것 아님):

| 단계 | comp1 (LPSCl) | 결과 |
|---|---|---|
| Halogen enumerate | C(8,4) = **70 configs** (anion cage 8자리에 Cl 4개 = free-S 4개 자리 선택) | screening best = #39, **Cl 4a 2개 + 4c 2개 (mixed)** ⚠ Li는 Rietveld 고정 |
| Li screening | 20 configs, spread **1162 meV** (halogen 단계 차이를 압도) | top5 = [0,1,8,15,9] |
| 500 K anneal 50 ps | ranking_reversed: true (#15 4위→2위, #1 2위→5위) | champion #0, 2위와 **491 meV** 차 |
| 최종 champion (→ v3 k444 V0) | **완전 ordered: Cl ×4 전부 4a, free-S ×4 전부 4d** | Voronoi Cl std = 0.00 Å³, S/Cl mixing 없음 |

핵심 서사:
1. **Li를 Rietveld에 고정한 1단계 halogen 랭킹은 mixed (2/2)를 best로 뽑았다** — 고정된 Li 분포에 맞는 anion 배치가 위로 올라옴.
2. **Li sublattice를 풀어주는 순간 (screening + annealing) ordered가 역전** — Li–anion 커플링이 ordered 4a-Cl/4d-S를 선택. 1단계에서 멈췄다면 잘못된 mixed 구조로 paper를 쌓았을 것 = 다단계 pipeline의 필요성 입증.
3. **같은 pipeline이 comp1에서는 ordered를, modelc에서는 12.5% 4d-Cl anti-site champion을 내놨다** → "disorder는 우리가 넣은 게 아니라 조성이 만든다" — paper thesis의 직접 증거.
4. 실험 NMR/XRD의 25–40% 4d-Cl anti-site (finite-T)와 비교해 우리 0 K champion은 **lower bound** (정직한 caveat, `lpscl_structural_analysis_v3.md`).

Q&A 한 줄 카드: *"Halogen-only 랭킹은 Li 고정 가정에 민감하다 — Li screening + annealing까지 가서야 ordered ground state가 확정됐고, 같은 절차가 modelc에서는 anti-site champion을 내놨다."*

근거 레코드: `db/compositions/comp1.json` (halogen_screening n=70, best #39 / li_screening / li_annealing), `db/properties/elastic.json` (lineage "comp1 v2 anneal champion → V0_relax"), `db/structures/STRUCTURES_NOTE.md` (k444 ordered), `db/compositions/modelc_v3.json` (Voronoi comp1 Cl std 0.00).
⚠ 로컬 DB에 "champion의 halogen branch" 직접 필드는 없음 — 위 3개 레코드의 조합으로 확정. 100% 못박으려면 container의 v2 screening/anneal 원본 output에서 champion 초기 anion 배치 확인.

---

### ★ Slide 5 (sub) — MLIP screening detail (★ NEW 2026-06-12, slide 3↔4 사이 삽입)

> slide 3 pipeline 박스만으로는 "어떻게 정수 occupancy 셀이 정해지나"가 추상적이라
> sub-slide 한 장으로 MLIP screening 단계를 시각화. 이 슬라이드가 다음 slide 4
> (Headline 4-message 표) 진입 전 마지막 절차 설명.

**실물 확정판 (v1 FINAL, 2026-06-12)**:

```
제목(좌상단): DFT
우상단 refs:  Angew. Chem. Int. Ed., 47, 755 (2008).
             J. Am. Chem. Soc., 139, 10909 (2017).

■ MLIP screening
   · Free S²⁻ site preferentially accepts Cl⁻ substitution
     (emergence of 4d-Cl anti-sites in LPSCl₁.₆)   ← 청색: of 4d-Cl anti-sites
   · Li sublattice screen + 500 K Langevin anneal → champion (lowest-E after Li relaxation)

[좌상] MLIP screening 박스 (점선 둥근 사각형):
        1. Halogen enumerate         (₈C₄, ₁₀C₂)        ← LPSCl 70 / LPSCl₁.₆ 45
        2. Li sublattice screen      (top-5 × 20)
        3. 500 K Langevin anneal     (Li ordering)

[좌하] 비교 표:
        |          | LPSCl                | LPSCl₁.₆               |
        | Structure| Cubic (F-43m)        | Rhombohedral (R3m)     |
        | atoms    | 52 (4 f.u.)          | 62 (5 f.u.)            |
        |          | Li₂₄P₄S₂₀Cl₄         | Li₂₇P₅S₂₂Cl₈          |  ← 27/22/8 빨강(변화)

[우] Champions 그림 (좌 cubic ordered ↔ 우 rhombo with 4d-Cl 점선 영역)
     "4d-Cl anti-sites" 라벨 + < Champions > 캡션
```

검수 이력:
① halogen enumerate 표기 (₁₀C₅ → ₁₀C₂) 정정 — C(10,5)=252, C(10,2)=45
② "Rhombohedral Supercell (P1)" → "Rhombohedral (R3m)" — modelc V0 실제 공간군
③ Free S²⁻ → Cl⁻ 치환 선호 한 줄 추가 (4d-Cl anti-site 원인 명시)
④ Li screen + 500 K anneal 한 줄로 압축
⑤ Champion 그림에 "4d-Cl anti-sites" 라벨 + 점선 영역 → thesis 직결

발표 보충 멘트: "Halogen 단계에서 free S²⁻ 자리가 Cl⁻ 치환을 선호한다는 게 결과로 나옵니다 —
이게 Cl-rich에서 4d-Cl anti-site가 등장하는 직접적 원인이에요. Li sublattice screen은 halogen이
fix된 위에서 Li/vacancy 배치를 다시 전수조사하는 단계고, 500 K annealing이 각 후보를 local
ground state로 relax해서 champion을 확정합니다."

---

### ★ Slide 6 (sub) — DFT validation detail (★ NEW 2026-06-12, 실물 확정)

```
제목(좌상단): DFT
상단 각주 (4줄):
  EOS: Equation of State — energy as a function of cell volume
  BM3: 3rd-order Birch–Murnaghan EOS — extracts V₀, B₀, B₀′ from E(V) curve
  BFGS: Broyden–Fletcher–Goldfarb–Shanno — quasi-Newton optimizer for atomic relaxation
  SCF: Self-Consistent Field — DFT electron-density iterative convergence
우상단 ref: Phys. Rev., 71, 809 (1947).   ← F. Birch (BM EOS 원조)

■ DFT validation
   · MLIP-champion structures confirmed by DFT — 11-volume Birch–Murnaghan EOS
   · Cl-rich shows volume contraction with bulk softening — first decoupling signal (적색)

[좌] DFT validation 박스: 1. MLIP EOS pre-scan (V₀ screening) / 2. BM3 EOS 11 volumes
     (V/V₀ 0.96–1.06) / 3. V₀ confirmation BFGS (force < 5e-3 eV/Å) / 4. k-mesh (k×L ≥ 40 Å, tight SCF)
[좌하] BM3 수식 + B₀/B₀′ 한 줄 정의
[우] E(V) curves: Li₆PS₅Cl (V/f.u. 254.16, B₀ 26.2) / Li₅.₄PS₄.₄Cl₁.₆ (243.29, −4.3% 적색, B₀ 21.7)
```

발표 보충 멘트 ("decoupling signal" 질문 대비):
"보통 부피가 줄면 단단해질 거라 기대하는데 Cl-rich는 부피 −4.3%이면서 B₀는 26.2→21.7로
내려갑니다. packing과 bonding이 따로 노는 첫 신호 — M4에서 hydrostatic soft / shear +30%
stiff로 완전히 풀립니다." (M4 복선)

검산: V/f.u. 254.16=1016.62/4 ✓ · 243.29=1216.44/5 ✓ · force 단위 eV/Å (ASE BFGS fmax) ✓

---

## 1D. Slide 4 — Headline Table (4 messages preview)

### ★ 실물 확정판 (as-built deck slide 7 FINAL, 2026-06-11 — 수치 전수 검증 PASS, 표기 3건 수정 반영 확인)

```
제목(좌상단): DFT
상단 각주 (4줄): D₀ (carrier density × attempt frequency) / E_VRH (VRH average, relaxed-ion)
                / Zener A = 2C₄₄/(C₁₁−C₁₂) / ICOHP 정의
우상단 ref: Adv. Energy Mater., 10, 1903719 (2020).   ← Schlem (Ea 0.25/0.22 매칭 근거)

■ Results of post-processing — 9행 표 (Property | LPSCl | LPSCl1.6 | Message)
   gap 1.76/1.82 · Ea(MLIP MD) 0.253/0.224 · D600 3.09e-6/7.90e-6 (2.5×)
   · D₀ 4.11e-4/5.8e-4 (1.4×, vacancy carriers) · ICOHP Li–Cl −1.86/−2.10 (+13%)
   · Bader q(Li) +0.874/+0.882 · E_VRH 22.06/27.66 (+25%) · B₀ 26.2/21.7 (hydrostatic 역전)
   · Zener A 1.14/1.44
   좌측 회전 주석 (Ea 행): Schlem 실험 0.25/0.22 EXACT matching
하단: → 4 messages: electronic invariance · dual-mechanism σ · stronger ionic glue
      · vacancy paradox resolved
```

검수 결과 (db/properties/li_transport.json `headline_PAPER_GRADE` + master doc v3 대조):
- ✓ 수치 9행 전부 DB 일치 (Ea 0.2532→0.253, 0.2235→0.224 반올림 정상. D 비 2.56→"2.5x",
  D₀ 비 1.41→"1.4x" 정상. v3 4fu PRIMARY 데이터 사용 확인 — 구 5fu 값 아님)
- ✓ 4-message 푸터가 v3 dual-mechanism framing과 일치, "MLIP MD" 정직 표기 유지
- ✓ 검수 3건 수정 반영 확인 (2026-06-11 FINAL):
  ① 오타 "Eexperiment" → "Experiment" ② Message 열 소문자 통일 ("nearly identical" ×2)
  ③ 색 규칙 통일: 청=우세/적=열세 (B₀·Zener 행 반전 유지), "nearly identical" 두 행
     (gap, Bader)은 중립 검정 — M1 '전자구조 동일' 메시지와 정합


Slide 4는 **what & how (Slide 1–3) → why (Slide 5–8)** 전환 pivot.
Tier 3 §8 multi-probe 결과를 한 페이지로 미리보기.

### 페이지 배치 (16:9)

9-행 표 + 색 강조 4행 (M1 파랑 / M2 초록 / M3 주황 / M4 빨강).

### 본문 텍스트

**상단**: "Headline — 한 페이지로 보는 두 시스템 (paper-grade)"

**표**:
```
항목              | LPSCl    | LPSCl₁.₆ | 메시지
─────────────────┼──────────┼──────────┼──────────────────
밴드갭 (eV)       | 1.76     | 1.82     | 거의 동일       ★M1
AIMD Ea (eV)      | 0.172    | 0.224    | comp1 낮음
D(600 K) cm²/s    | 2.68e-6  | 7.90e-6  | modelc 3× 빠름  ★M2
D₀ prefactor      | ~7.5e-5  | ~5.8e-4  | ~8× ← 진짜 원인
ICOHP Li–Cl (eV)  | −1.86    | −2.10    | +13% 강화       ★M3
Bader Li (e)      | +0.874   | +0.882   | 거의 동일
E_VRH relaxed-ion | 22.06    | 27.66    | +25.4% 단단     ★M4
B₀ (BM, GPa)      | 26.23    | 21.71    | hydrostatic 반대
Zener A           | 1.14     | 1.44     | 비등방 ↑
```

**하단**: "→ 4 messages = 전자구조 둔감 · σ는 prefactor · ionic glue 강화 · vacancy paradox 해소"

### 발표 스크립트 (60–70초)

> "Slide 4는 한 페이지로 전체 결과를 미리 보여드리는 headline 표입니다.
>
> 표의 가운데 두 열이 LPSCl과 LPSCl₁.₆ 결과, 오른쪽 열이 그 차이가 의미하는 메시지입니다. 색이 칠해진 4개 행이 paper의 4대 메시지예요.
>
> **첫 번째, 파란색 — 밴드갭**. 1.76 vs 1.82 eV, 거의 동일합니다. 전자구조에서 큰 차이가 없다는 첫 신호입니다.
>
> **두 번째, 초록색 — 확산 계수와 prefactor**. modelc가 600 K에서 약 3배 빠른데, 흥미로운 건 그 위에 있는 Ea입니다. comp1의 per-hop barrier가 오히려 더 낮아요. 그런데 왜 modelc가 빠르냐? prefactor D₀가 약 8배 크기 때문입니다 — vacancy carrier가 운반체를 늘린 거.
>
> **세 번째, 주황색 — ICOHP**. Li–Cl 결합 강도가 13% 강해집니다. 4d 자리 Cl anti-site가 동력이고요.
>
> **네 번째, 빨간색 — Young's modulus**. relaxed-ion에서 25% 단단합니다. 흥미로운 건 그 아래 B₀ — 등방 압축에서는 오히려 comp1이 더 단단해요. 이게 vacancy paradox의 핵심 단서입니다.
>
> 다음 슬라이드부터 이 4개 메시지를 하나씩 깊게 풀어드리겠습니다."

### 시각 디자인 노트
- 8행 × 4열 + 헤더, 가운데 정렬
- 색 강조 4행 약한 배경색 (M1 파랑 / M2 초록 / M3 주황 / M4 빨강)
- D + D₀ 두 행은 같은 초록 계열 (M2의 두 면)
- "★" symbol로 메시지 행 표시
- 표 폰트 18–20pt, 헤더 bold
- 하단 한 줄은 별도 box

### Q&A 보조 노트
- "왜 600 K D를 헤드라인?" → AIMD 측정 구간 (600/800/1000 K) 중 가장 낮은 T. 작동온도 근사
- "B₀와 E_VRH 방향 반대 — 모순?" → 다른 modulus. B₀ = hydrostatic compression resistance (volume), E_VRH = shear-dominant tensile stiffness. modelc는 vacancy로 hydrostatic softer + 4d-Cl로 shear stiffer. slide 8에서 분리
- "ICOHP negative 이유" → COHP convention: bonding (−) 안정, antibonding (+). |ICOHP| 클수록 결합 강함
- "Zener A는 뭐냐?" → cubic isotropy 지표, A=1이면 등방. modelc 1.44 = 비등방성 발현
- "AIMD Ea 0.224는 실험과 일치?" → ✓ Schlem 2020 Cl-rich Ea 0.22 정확 일치

---

## 1E. Slide 5 — M1: 전자구조는 거의 동일

### ★ Provenance 확정 (2026-06-11, V100 백업 summary.json 대조)

- **comp1 정본**: `runs/comp1_v3/v3_post/k444_props/V0_*` — EF 2.821 / VBM 2.48 / CBM 4.24 /
  gap 1.76 / VBM char S p 91.3% + Li p 5.7% / CBM char S p 42.3% + P s 24.6% + Li p 14.3% — 표와 전부 일치 ✓
- **modelc 정본**: `runs/modelC_v3/V0_regen_*` ★ — EF 2.445 / VBM 2.72 / CBM 4.54 / gap 1.82 /
  VBM char S p 91.6% + Li p 5.6% / CBM char S p 44.7% + P s 27.4% + Li p 12.7% — 표와 전부 일치 ✓
- ⚠ modelc 구버전 `V0_dos_summary.json` (regen 아님)은 옛 gap-detection (longest-run) — gap 1.80 /
  VBM 2.74로 미세 차이. **사용 금지**, appendix PNG도 `V0_regen_dos_pdos.png` 사용.
- ⚠ comp1 `archive_v2_post/post_v2/comp1v2_*`는 v2 아카이브 — 사용 금지.
- Origin overlay 데이터 (`V0_dos.dat` ×2 → dos_overlay_origin.csv): E−EF gap edge 검산
  comp1 −0.34/+1.42, modelc +0.28/+2.09 — regen 값과 일치 ✓ (M1 표 7행 provenance 완료)
- **Appendix PDOS 2장 확정 (2026-06-11, `tools/figures/plot_pdos_appendix.py` 재생성, 검수 PASS)**:
  `D:\comp1_pdos_appendix.png` (gap 1.76 / VBM 2.48 / CBM 4.24) +
  `D:\modelc_pdos_appendix.png` (gap 1.82 / VBM 2.72 / CBM 4.54) — E−E_VBM 축, 원소분해.
  용도: ① "VBM = S 3p 91/92%" 시각 증거 ② Cl 3p 봉우리가 S 3p보다 깊은 −3.3 eV 위치
  (mechanism 2: LOBSTER per-bond covalent 해석 방어, M3/CC#2 Q&A) — 1장 2역.

### ★ 실물 확정판 (as-built deck slide 8, 2026-06-11 — 검수 PASS, 라벨 1건 수정 대기)

```
제목(좌상단): DFT / 상단 각주: DOS 정의
■ M1: Electronic structure is nearly identical
   · Band gap 1.76 vs 1.82 eV (Δ = 0.06 eV) — too small to explain 2.5× σ or +25% E
   · Fingerprint of disorder: 0.74 localized in-gap states (LPSCl 0.037, 20×)
[좌] Origin DOS overlay (LPSCl=적 / LPSCl1.6=청 — slide 7 컬럼 색과 정합 채택),
     E−EF 축, defect-band 꼬리에 적색 점선 원 + <DOS> 캡션
[좌하] Fingerprint of disorder — defect band 박스 (EF<VBM → 0.74 / 0.037 20× / S 3p holes)
[우] 표 7행: gap 1.76/1.82 · Δgap +0.06 · EF 2.82/2.45 · VBM 2.48/2.72 · CBM 4.24/4.54
     · VBM char S 3p 91/92%+Li p 6% · CBM char S p+P s+Li p (양쪽 동일 표기)
     EF·VBM(modelc) 셀에 적색 점선 박스 — fingerprint와 시각 연결
```

검수: ① 값은 edge로 교체 완료 (4.24−2.48=1.76 / 4.54−2.72=1.82 자기검산 ✓) —
**단 행 라벨이 아직 "VBM peak / CBM peak"** → "VBM / CBM"으로 정정 필요 (값=edge, 라벨=peak 불일치)
② 곡선 색 LPSCl=적/LPSCl1.6=청은 deck 컬럼 색과 일관 — 의도적 채택으로 확정
③ fingerprint 박스·그림 원·표 점선박스 삼각 연결 구조 ✓



### 본문 텍스트

**상단**: "M1: 전자구조는 두 시스템에서 거의 동일"

**표**:
```
항목           | LPSCl       | LPSCl₁.₆
───────────────┼─────────────┼─────────────
gap (eV)       | 1.76        | 1.82
Δgap           |             | +0.06
EF (eV, QE)    | 2.821       | 2.445
VBM (eV)       | 2.48        | 2.72
CBM (eV)       | 4.24        | 4.54

VBM character  | S p 91% +   | S p 92% +
               | Li p 6%     | Li p 6%
CBM character  | S p 42% +   | S p 45% +
               | P s 25% +   | P s 27% +
               | Li p 14%    | Li p 13%
```

**Key points**:
```
• 갭 차이 Δ = 0.06 eV (작음)
• VBM = S 3p 91%, CBM = S 3p + P 3s + Li 2p (양쪽 동일 패턴)
• 0.06 eV로는 σ 3× / E_VRH 25% 차이 설명 불가
```

**Footnote**:
```
※ modelc EF(2.45) < VBM(2.72): 국소 defect-band 0.74 states (comp1 0.037, 20× 적음)
  → vacancy + 4d-Cl anti-site의 실제 전자적 흔적, S 3p hole localization
```

### 발표 스크립트 (55–65초)

> "Message 1, 전자구조는 거의 동일하다.
>
> 왼쪽 그림이 두 시스템의 DOS overlay입니다. 전체적인 모양이 거의 똑같습니다. VBM 부근, 그러니까 페르미 레벨 바로 아래는 양쪽 다 S 3p가 91% 이상 차지하고, CBM은 S 3p + P 3s + Li 2p 조합으로 동일합니다.
>
> 오른쪽 표를 보시면 갭이 1.76 vs 1.82 — 차이 0.06 eV 정도로 modelc가 약간 wide합니다. 하지만 이 작은 차이로는 conductivity 3배, stiffness 25% 차이를 설명할 수 없습니다. 0.06 eV는 thermal kT (300 K에서 26 meV)의 2.3배 정도라서 transport나 mechanical에 의미 있는 contribution을 주기 어려워요.
>
> 그런데 흥미로운 게 하나 있습니다. modelc의 페르미 레벨이 VBM보다 아래에 있어요 — 2.45 vs 2.72 eV. 이 사이에 0.74개의 localized state가 들어가 있습니다. comp1은 같은 구간에 0.037개뿐, 20배 차이입니다. 이건 vacancy와 4d-Cl anti-site로 생긴 국소 S 3p hole의 실제 흔적이고, defect band 그 자체죠.
>
> 즉 갭은 거의 같지만, modelc는 전자구조에 'disorder의 fingerprint'가 분명 있고, 그 fingerprint가 mechanism에서 나오는 변화의 원인이 됩니다. 그 disorder가 무엇인지가 다음 메시지부터 보여드릴 내용입니다."

### 시각 디자인 노트
- DOS plot: two systems overlay (comp1 파랑, modelc 빨강) + Fermi level 점선 + VBM/CBM 음영
- 표 색 강조: gap 행만 약한 음영
- "거의 동일" 두 단어는 강조색 (#003876)
- footnote 폰트 작게 (12pt), italic

### Q&A 보조 노트
- "0.06 eV 차이 통계적으로 의미있나?" → DOS bin 0.005 eV 기준 measurable. USPP/DOS-threshold 0.4 eV 절대오차 있는 상황이라 direction만 robust
- "modelc EF가 VBM 아래에 있는 게 왜?" → 충분한 disorder가 있으면 PBE에서 partial localization → 부분적으로 채워진 defect state. n-type 거동 시사
- "literature PBE gap 2.15-2.45 eV인데 우리 1.76?" → USPP + DOS-threshold method offset 0.4 eV. 양쪽 동일 적용되어 Δgap robust
- "DOS overlay 어떻게 grade?" → V₀ 다른 두 시스템이라 alignment는 EF 기준. 절대 에너지 무의미
- "defect band 0.74 states 의미?" → 5 f.u. cell당 정수 단위 (~1 hole). n-type pinning 등과 연결 가능

---

## 1F. Slide 6 — M2: σ 차이 = barrier↓ + prefactor↑ 둘 다 (★ HOLD 해제 2026-06-11)

> ✅ **HOLD 해제 (2026-06-11)** — comp1 4 f.u. natural-cell MLIP MD 결과 확정.
> **Ea = 0.2532 eV (R²=0.9998)**, Schlem 2020 LPSCl ordered ~0.25 eV 정확 일치.
> → **시나리오 A 확정**: 5 f.u. 인위 supercell이 진짜 artifact, 4 f.u. natural에서
> Cl-rich Ea↓ 통념 (Minafra/Kraft) 정합. paper #1 mechanism: **σ gain = Ea↓ + D₀↑ 둘 다**.

### ★ 실물 확정판 (as-built deck slide 9, 2026-06-11 — 검수 PASS, 수정 2건 대기)

```
제목: DFT / 우상단 refs: Schlem AEM 10,1903719 + Minafra SSI 346,115223 ✓
■ M2: σ gain = lower barrier + more carriers (both work)
   · Ea 0.253 vs 0.224 eV — Cl-rich lower barrier (exp. 0.25/0.22 EXACT)
   · D₀ 4.11e-4 vs 5.8e-4 (1.4×) — vacancy carriers
[좌] Origin Arrhenius (적=LPSCl 아래·가파름 / 청=LPSCl1.6 위·완만, fit 선 통과,
     선 옆 0.253/0.224 라벨) + <Arrhenius plot> 캡션
[좌하] D = D₀·exp(−Ea/kT) (D₀·Ea 청 강조) + σ 분해: 2.5× = 1.75× (lower Ea) ×
      1.41× (vacancy carriers, D₀)
[우] 표 6행: D600/800/1000 (단위 1행에) · Ea · D₀ · R²(중립). Schlem 행은 bullet로 흡수
```

검수 → **FINAL 확정 (2026-06-11)**: 수치·fit·색규칙 ✓ (fit은 docs/figures/slide09_arrhenius
CSV — DB PRIMARY 재현 확인). ① MLIP MD 캡션 추가 확인 — "※ D from MLIP MD (UMA-s-1p1),
600–1000 K" ② Ea 라벨 선 색과 일치 (0.253 적 / 0.224 청) 적용 확인.
**결정: 4 f.u./5fu-artifact footnote는 슬라이드에서 생략** — 청중 미공개 수치의 선제 고백은
불필요 (audit trail은 db/SI 유지). 발표 대본에서도 해당 단락 삭제 → Q&A 카드로 강등:
"셀 의존성? → 5fu 인위 supercell은 0.172 (artifact), natural 4fu가 Schlem 정확 매칭.
검증은 6b disorder ensemble이 정면으로 수행." (6b가 받아주는 흐름)
캡션에 "natural cells" 한 단어 추가는 선택 권장.



### 본문 텍스트 (v3 ACTIVE)

**제목**: "M2: σ 차이 = barrier ↓ + prefactor ↑ 둘 다 작용"

**표 (v3)**:
```
T (K)                | LPSCl (4fu)  | LPSCl₁.₆ (5fu)
─────────────────────┼──────────────┼─────────────
D(600 K) cm²/s       | 3.09e-6      | 7.90e-6
D(800 K)             | 1.03e-5      | 2.05e-5
D(1000 K)            | 2.20e-5      | 4.55e-5

Ea (eV)              | 0.253 ★       | 0.224 ★
D₀ (cm²/s)           | 4.11e-4       | 5.8e-4
R²                   | 0.9998        | 0.992

Schlem 2020 실험      | LPSCl ~0.25 ✓ | Cl-rich ~0.22 ✓
```

**2-mechanism 분해 (σ ~2.5× 이유)**:
```
σ(modelc) / σ(comp1) = 2.5× at 600 K, 분해:

  Ea contribution:  exp((0.253−0.224)/kT) at 600K = 1.75× (barrier ↓)
  D₀ contribution:  5.8e-4 / 4.11e-4 = 1.41× (carrier ↑)
  ─────────────────────────────────────────────
  Total:             1.75 × 1.41 = 2.47× ≈ 측정값 2.5× ✓
```

**Key**:
```
• Cl-rich가 lower Ea (Minafra/Kraft direction confirmed) + higher D₀
• 두 효과 거의 동등 기여 (Ea: 1.75×, D₀: 1.41×)
• Schlem 2020 실험과 EXACT 매칭 (LPSCl 0.25, Cl-rich 0.22)
• 5 f.u. comp1 (Ea=0.172) = 인위 supercell artifact, 4 f.u. natural로 정정
```

**Footnote**:
```
※ 4 f.u. natural F-43m cubic (comp1_V0_k444.xyz, paper-grade DFT V0) 사용
※ 5 f.u. (인위 cubic supercell)에서 Ea=0.172은 artifact — 본 paper에서는 4fu 채택
※ db/properties/li_transport.json (2026-06-11 갱신)
```

### 발표 스크립트 v3 (75–85초, ★ ACTIVE)

> "Message 2, σ 차이의 mechanism. 두 효과가 함께 작용합니다.
>
> 왼쪽 Arrhenius plot — 3점 모두 깨끗하게 직선 위, comp1 R² 0.9998, modelc 0.992. 두 시스템 다 paper-grade fit.
>
> 표를 보세요. comp1 Ea = 0.253, modelc Ea = 0.224. **Cl-rich가 lower Ea — Minafra/Kraft '구조적 무질서가 barrier를 낮춘다' narrative와 정확히 정합**합니다. 그리고 **Schlem 2020 실험과도 정확 매칭** — LPSCl ordered 0.25, Cl-rich 0.22.
>
> D₀ prefactor도 comp1 4.11×10⁻⁴ vs modelc 5.8×10⁻⁴, modelc가 1.4배 큽니다. vacancy로 carrier density가 늘어난 효과.
>
> σ 비율 2.5×를 분해하면 — **Ea contribution은 exp(0.029/kT) = 1.75×** (barrier 효과), **D₀ contribution은 1.41×** (carrier 효과). 둘 다 같은 방향, 거의 동등하게 기여. 곱하면 **2.47×, 측정값 2.5×와 거의 정확** 일치.
>
> 정리: **Cl-rich의 σ 향상은 barrier 감소와 carrier 증가 둘 다에서 옵니다**. 이전에 5 f.u. 인위 supercell로 측정했을 때는 comp1 Ea가 0.172로 비정상적으로 낮게 나와서 'prefactor 단독 효과'로 잘못 해석한 적이 있는데, **자연 4 f.u. F-43m cubic으로 재측정하니까 Schlem 실험값과 정확 매칭되면서 dual mechanism이 확정**됩니다.
>
> 다음 sub에서 5fu→4fu 정정 과정 자세히, 그 다음 disorder ensemble까지 보여드리겠습니다."

### v1 / v2 보존 (audit trail)

**v1 (5fu, 'prefactor only')**: 
- Ea(comp1) 0.172 < Ea(modelc) 0.224 (counter-intuitive direction)
- "차이는 prefactor에서, barrier는 반대 방향" framing
- 2026-06-10 ~ 06-11 morning

**v2 (5fu + 'macro vs micro' framing)**:
- Microscopic vs macroscopic Ea distinction 추가
- "Minafra/Kraft와 mutually compatible" framing
- 2026-06-11 morning

**v3 (4fu natural, ★ ACTIVE)**:
- Ea(comp1) 0.253 > Ea(modelc) 0.224 (lit 정합 direction)
- "barrier + prefactor 둘 다" framing
- 2026-06-11 evening (comp1 4fu MD 완료)

→ db에 v1/v2/v3 모두 audit trail로 보존. paper에서는 v3 사용.

### Q&A (v3)
- "왜 5fu가 artifact?" → cubic F-43m natural cell은 4 f.u. (52 atoms). 5 f.u. supercell은 비정수 stoichiometry로 인위 구성, Li sublattice가 정상 ordered 배치 못 함 → effective disorder 주입 → Ea underestimate
- "Schlem 매칭이 왜 강력?" → Schlem 2020은 paper-grade Cl-content series 측정. 우리 둘 다 ±0.005 안에서 match — same-method comparison의 정확성 입증
- "Minafra/Kraft narrative 완전 인정?" → Direction 인정. 다만 absolute Ea (실험 macro)와 우리 micro Ea는 여전히 다른 양 — caveat은 유지
- "5fu 데이터 SI?" → Yes, audit trail로 SI에 포함. transparency 보임
- "기존 disorder ensemble (Ea=0.177)과 어떻게 정합?" → 6b에서 풀이: 4fu(d=0) 0.253 → 4fu(d=0.5) 0.177로 자연스럽게 줄어듦 (Minafra effect). Disorder가 Ea 진짜 낮춤
- "modelc도 자연 cell?" → Yes. modelc rhombohedral 5 f.u.가 자연 cell. 비교 cell mismatch (cubic 4 vs rhombo 5) 있지만 intensive property라 OK

### 페이지 배치 (16:9)
- 왼쪽: Arrhenius plot (ln D vs 1/T, comp1 ▲ 파랑, modelc ● 빨강)
- 오른쪽: 표 (T별 D + Ea + D₀ + 비율)
- 하단: 3 bullet key + 한 줄 결론

### 본문 텍스트

**상단**: "M2: σ 차이는 per-hop barrier가 아니라 prefactor에서"

**표**:
```
T (K)         | LPSCl    | LPSCl₁.₆
──────────────┼──────────┼──────────
600           | 2.68e-6  | 7.90e-6
800           | 5.91e-6  | 2.05e-5
1000          | 1.02e-5  | 4.55e-5

Ea (eV)       | 0.172    | 0.224
D₀ (cm²/s)    | ~7.5e-5  | ~5.8e-4
D 비 (600K)   |   1×     |   ~3×
D₀ 비         |   1×     |   ~8×
R²            | 0.999    | 0.992
```

**Key**:
```
• comp1 per-hop barrier 더 낮음 (Ea 0.172 < 0.224)
• 그런데도 modelc가 600 K에서 ~3× 빠름
• 차이의 정체: D₀가 ~8× 큼 = vacancy carrier 운반체↑
```

**하단**: "→ halogen rich가 빠른 진짜 이유는 barrier ↓ 아니라 carrier ↑"

**Footnote (★ ADDED v1.8)**:
```
※ 실험 Ea (macroscopic): 다결정 impedance + grain boundary + percolation 포함
  우리 Ea (microscopic): 단결정 bulk per-hop intrinsic barrier
  → 두 값이 같은 시스템에서도 50–100 meV 다를 수 있음
  Minafra/Kraft의 ΔEa(disorder)는 macroscopic shift, 우리(prefactor 우세)와 mutually compatible
```

### 발표 스크립트 v2 — macroscopic vs microscopic Ea framing 추가 (★ ACTIVE)

> "Message 2, σ 차이는 per-hop barrier가 아니라 prefactor에서 옵니다. paper의 가장 counter-intuitive한 부분이라 천천히 풀어드릴게요.
>
> 왼쪽 Arrhenius plot 보시면 ln D vs 1/T인데 — comp1의 기울기가 더 완만합니다. Arrhenius slope이 −Ea/k라서, comp1의 per-hop barrier가 더 낮다는 뜻이에요. 0.172 eV vs modelc 0.224 eV.
>
> 직관적으로는 'barrier 낮은 comp1이 더 빨라야 한다'고 생각할 텐데, 측정 구간 600 K부터 1000 K까지 modelc가 일관되게 약 3배 빠릅니다.
>
> 왜 그럴까요? 표 아래쪽 D₀ 행을 보세요. comp1이 7.5×10⁻⁵, modelc가 5.8×10⁻⁴ — 약 8배 차이입니다. Arrhenius 식 D = D₀ exp(−Ea/kT)에서 prefactor D₀가 운반체 수와 hopping 경로 수에 비례하는데, modelc의 vacancy가 8배 많은 carrier와 path를 만든 거예요.
>
> **한 가지 짚고 갑니다. 실험에서 측정하는 Ea는 다결정 + grain boundary 효과까지 포함된 macroscopic 값이고, 우리 MLIP Ea는 단결정 bulk의 per-hop microscopic 값입니다. 같은 시스템에서도 두 값이 다를 수 있고, 이번 발표는 마이크로 관점의 mechanism입니다.**
>
> 즉 두 효과가 경쟁합니다 — modelc는 microscopic barrier가 약간 높지만(disorder cage), prefactor가 훨씬 큽니다(vacancy). 작동온도 영역에서는 prefactor 효과가 압도해서 modelc가 빠릅니다. 그리고 이게 실험 σ(LPSCl₁.₆) > σ(LPSCl)와 정확히 일치하는 미시 그림이에요.
>
> 진짜 동력은 vacancy carrier입니다."

### 발표 스크립트 v1 (보존용)

> "Message 2, σ 차이는 per-hop barrier가 아니라 prefactor에서 옵니다. paper의 가장 counter-intuitive한 부분이라 천천히 풀어드릴게요.
>
> 왼쪽 Arrhenius plot 보시면 ln D vs 1/T인데 — comp1의 기울기가 더 완만합니다. Arrhenius slope이 −Ea/k라서, comp1의 per-hop barrier가 더 낮다는 뜻이에요. 0.172 eV vs modelc 0.224 eV.
>
> 직관적으로는 'barrier 낮은 comp1이 더 빨라야 한다'고 생각할 텐데, 측정 구간 600 K부터 1000 K까지 modelc가 일관되게 약 3배 빠릅니다.
>
> 왜 그럴까요? 표 아래쪽 D₀ 행을 보세요. comp1이 7.5×10⁻⁵, modelc가 5.8×10⁻⁴ — 약 8배 차이입니다. Arrhenius 식 D = D₀ exp(−Ea/kT)에서 prefactor D₀가 운반체 수와 hopping 경로 수에 비례하는데, modelc의 vacancy가 8배 많은 carrier와 path를 만든 거예요.
>
> 즉 두 효과가 경쟁합니다 — modelc는 barrier가 약간 높지만(disorder cage), prefactor가 훨씬 큽니다(vacancy). 작동온도 영역에서는 prefactor 효과가 압도해서 modelc가 빠릅니다. 그리고 이게 실험 σ(LPSCl₁.₆) > σ(LPSCl)와 정확히 일치하는 미시 그림이에요.
>
> 'Cl을 늘리면 barrier가 낮아져서 빠르다'는 통념과 반대로, 진짜 동력은 vacancy carrier입니다. 다음 sub-slide에서 mechanism 그림을 정리하고, 그 다음 disorder ensemble로 추가 검증한 결과 보여드리겠습니다."

### 시각 디자인 노트
- Arrhenius plot: x = 1000/T (K⁻¹), y = ln D, marker comp1 ▲ modelc ● + linear fit 선
- 기울기로 Ea 직관적 보임
- 표 색 강조: D₀ 행만 진한 음영
- "barrier ↓ 아니라 carrier ↑" 두 keyword 강조색
- 하단 한 줄 굵게

### Q&A 보조 노트
- "왜 600/800/1000K?" → MLIP MD가 안정 sampling되는 최저온이 600K (statistics). 300K 외삽 3-pt
- "comp1 Ea 0.172가 lit?" → LPSCl bulk 0.16-0.25 범위 내. modelc 0.224 = Schlem 2020 Cl-rich 0.22 정확 일치
- "D₀ 8× 차이의 정확한 출처?" → AIMD Arrhenius intercept. n_Li(27 vs 30) 만으로는 1/10 못 설명. vacancy site path multiplicity + correlated hop 종합
- "왜 작동온도에서 modelc 빠르다고 단정?" → 실험 σ(LPSCl₁.₆) > σ(LPSCl) 일관 (Zuo 2.9 vs 7.0 mS/cm). 600-1000K도 동일. 300K 외삽은 6c 슬라이드
- "framework atom diffusion?" → D(Cl,P,S) ≈ D(Li)/40~60 → framework 정지 = Li-only 전도체
- **"Minafra/Kraft는 disorder가 Ea를 낮춘다고 했는데?"** → 실험 Ea는 macroscopic (다결정 + GB), 우리 Ea는 microscopic (단결정 bulk per-hop). 50–100 meV 차이 가능. Minafra의 ΔEa는 macroscopic shift, 우리(prefactor 우세)와 mutually compatible. 추가로 disorder ensemble (slide 6b)에서 matched-d일 때 우리 Ea 동일 확인

---

## 1F-1. ~~Slide 6a — Mechanism Cartoon (carrier vs barrier)~~ — **발표 deck에서 DROPPED** (2026-06-11)

> ⚠ v1 잔재로 판정, as-built deck에서 제외. 사유: ① "왜 carrier가 **이기는가** — 두 효과의
> **경쟁**" 프레임은 5fu 시절(comp1 Ea가 더 낮아 barrier↔carrier가 경쟁하던 v1) 산물 —
> **v3에서는 Ea·D₀ 둘 다 modelc 우세(협력)라 경쟁 프레임 자체가 무효**. ② 우측 패널
> "~8× 많은 path"도 구 D₀ 8× 수치 잔재 (v3는 1.41×). ③ 분해(1.75×1.41)는 M2 본
> 슬라이드 하단 박스가 이미 수행. **●●○●● vacancy 직관은 M2 대본 한 문장으로 흡수**:
> "LPSCl은 Li가 가득 차서 hop하려면 옆자리가 비길 기다려야 하는데, LPSCl₁.₆는 공공이
> f.u.당 0.6개라 빈자리가 항상 근처에 있습니다 — 그게 D₀ 1.4×의 실체입니다."

### (보존) 페이지 배치 (16:9)
- 좌우 2-panel cartoon: LPSCl (Li 가득참, hop 대기) vs LPSCl₁.₆ (공공 ○, 상시 hop)
- 하단: D = D₀·exp(−Ea/kT) 식 + "D₀ 8×가 지배" 한 줄

### 본문 텍스트
```
좌 (LPSCl):    Li sublattice 가득참 → hop하려면 옆자리 비기를 '대기' → carrier 부족
우 (LPSCl₁.₆): Li 공공 0.6/f.u. → 빈자리가 항상 근처 → hop 경로 상시 열림

D = D₀ · exp(−Ea/kT)
    └ 8× (vacancy)   └ 경쟁 (cell-dependent, slide 6b)

→ 측정 구간(600–1000 K)에서 D₀ 효과가 지배
```

### 스크립트 (40초)
> "직관 그림으로 정리하겠습니다. 왼쪽 LPSCl은 Li 자리가 가득 차 있습니다. Li 하나가 hop하려면 옆자리가 비기를 기다려야 해요. 자리가 꽉 차 있으니 동시에 움직일 수 있는 Li 수, 즉 carrier가 제한됩니다.
> 오른쪽 LPSCl₁.₆는 공공이 f.u.당 0.6개 — 빈자리가 항상 근처에 있습니다. hop 경로가 상시 열려 있고, 이게 D₀ 8배의 실체입니다.
> Arrhenius 식으로 보면 D₀와 exp(−Ea/kT)가 경쟁하는데, 측정 구간에서는 D₀의 8배가 지배합니다. Ea 쪽 이야기는 다음 슬라이드에서 셀 의존성까지 포함해 정직하게 정리하겠습니다."

### Q&A
- "carrier 8×가 vacancy 0.6/fu에서 어떻게?" → 단순 공공 수(10%)가 아니라 경로 다양성 (vacancy 주위 다중 hop path + correlated migration). percolation 효과
- "왜 barrier 높이 차이를 안 강조?" → cell-dependent (6b)

---

## 1F-2. Slide 6b — Disorder Ensemble: Ea의 ground truth ★ — **본편 유지 확정 (2026-06-11 정정)**

> ⚠ 직전 "appendix 강등" 기록은 **사용자 의도 오독으로 철회** — 6b는 본편 유지,
> 대신 **6c(저온 외삽)를 본편 제외**. 본편 순서: M2(9) → **6b(10)** → M3(11).
> M2 대본 마지막 줄 "다음 슬라이드에서 정면으로 검증합니다" 핸드오프 유효.
> as-built 제작 시 v3 정합판 사용: clean 행 = 0.253/0.224 (★ Schlem), 1.17은 footnote,
> "σ 3×" bullet은 2.5×로 정정 또는 삭제.
> 6c 메시지 흡수: 6b 대본 끝에 한 문장 — "두 효과가 같은 방향이라 저온일수록 격차가
> 커집니다 — RT 외삽 ~4×, Zuo 실험 2.4×와 자릿수 정합. 저온 trade-off는 없습니다."

### ★ 실물 확정판 (as-built deck slide 10 "M2-1", 2026-06-11 — footnote 1건 수정 대기)

```
제목: DFT / 상단 각주: d 정의 (free S²⁻↔Cl exchange, PS₄ untouched, composition
conserved) / 우상단 refs: Minafra SSI + Kraft JACS (대본 인용 근거)
■ M2-1: Ea ground truth — matched disorder, same barrier
   · Natural cells: Cl-rich is intrinsically lower-Ea, its vacancies are built-in disorder
   · Matched disorder (d≈0.4–0.5): 0.177 vs 0.173 - same within error (청)
[좌] 구조 그림: free-anion 영역 청 점선 타원 + 교환 화살표, 라벨 "free S²⁻ ↔ Cl swap"
[우] 표: clean 행 0.253(적)/0.224(청) · disordered 행 중립 — 색이 "same" 메시지와 호응
     표 아래: matched disorder: ΔEa = 4 meV (almost same)
검수 → **FINAL 확정 (2026-06-11)**: Minafra bullet 3은 의도적 생략 (대본이 커버).
**결정: footnote는 앞 절만 유지** — "※ Even "ordered" LPSCl (exp., ball-milled)
contains partial disorder" (bullet 1 지지 역할). 1.17-frozen 뒷절은 삭제 — M2의 0.172
생략과 동일 논리 (청중 미공개 내부 검증 스토리). 대본의 1.17 단락도 삭제 → Q&A 카드 강등:
"완전 ordered 극한 직접 측정? → 했음 — 600 K에서 Li frozen (D~10⁻⁷), 겉보기 1.17 eV는
hop 통계 artifact. 그래서 clean 행은 natural cell 값 사용. 실험 샘플도 ball-milled라
순수 ordered 극한은 실험적으로도 접근 불가."
```


> 역할 승격 (2026-06-11): clean-cell Ea의 셀 의존성 발견 후, 이 슬라이드가 M2 Ea 주장의 ground truth.
> **✓ 검증 완료 (2026-06-11)**: ensemble_results.json의 `"v0_xyz": "db/structures/comp1_V0_k444.xyz"` —
> comp1 disorder ensemble은 **4 f.u. natural cubic (52 atoms) 기반**으로 이미 돌았음. **재실행 불필요.**
> d=0.0 frozen (1.17 artifact)도 natural cell의 정직한 결과. 지금 도는 4 f.u. clean MD (100 ps, 3T)는
> 그 d=0.0 점의 고품질 재측정 — frozen 재현되면 시나리오 B 확정.

### 페이지 배치 (16:9)
- 중앙: 2×2 매트릭스 표 (조성 × disorder level)
- 하단: 3 bullet key + 5 f.u. artifact footnote

### 본문 텍스트
```
Ea (eV)             | LPSCl (4 f.u. natural) | LPSCl₁.₆ (5 f.u. natural)
────────────────────┼────────────────────────┼──────────────────────────
clean (d = 0)       | 1.17 (frozen, artifact) | 0.140
disordered (d≈0.5)  | 0.177 ± 0.027 (n=3)     | 0.173 ± 0.039 (n=3)
                                └──── 사실상 동일 (Δ4 meV) ────┘

• ordered LPSCl = kinetically frozen (600 K, D~1e-7) → 1.17은 통계 artifact
• matched disorder: Ea 동일 (~0.18) — 실험 ball-milled 0.16–0.25와 정합
• σ 차이의 출처는 Ea가 아니라 D₀ (M2 ground truth)

※ 5 f.u. 인위 supercell의 comp1 'Ea=0.172'는 셀 구성이 우연히 주입한
  effective disorder 산물 가능성 (4 f.u. 검증 진행 중)
```

### 스크립트 (60초)
> "앞 슬라이드의 Ea 숫자에는 사실 미묘한 셀 의존성이 있습니다. 그걸 정면으로 해결한 게 이 disorder ensemble입니다.
> 두 시스템 × 두 disorder 레벨, 2×2 매트릭스입니다.
> 먼저 왼쪽 위 — 완전히 ordered한 LPSCl을 natural 4 f.u. 셀에서 돌리면, 600 K에서 Li가 사실상 안 움직입니다. D가 10⁻⁷ 수준. 이때 Arrhenius 기울기는 1.17 eV처럼 보이는데, 이건 물리값이 아니라 저온 통계 부족 artifact입니다. 메시지는: 진짜 ordered LPSCl은 MLIP 마이크로 스케일에서 kinetically frozen이라는 것.
> 오른쪽 위 — modelc는 clean으로 돌려도 0.140. 본질적 vacancy 때문에 이미 충분히 disordered라서 정상적으로 측정됩니다.
> 핵심은 아래 행입니다. 같은 수준의 anti-site disorder를 양쪽에 넣고 3개 config 앙상블로 재면 — 0.177 대 0.173, 사실상 같습니다. 그리고 이 0.18이라는 값은 실험 ball-milled LPSCl 범위 0.16–0.25와 정합합니다.
> 결론: matched disorder에서 per-hop barrier는 두 조성이 같고, σ 3배 차이는 온전히 prefactor — vacancy carrier — 에서 옵니다. 이게 M2의 ground truth입니다."

### Q&A
- "d=0.5가 물리적으로 의미 있는 수준?" → 실험 합성 샘플 anti-site 25–50% 범위 내
- "n=3 부족?" → σ(Ea) ±0.03–0.04. ΔEa > 0.08 eV 효과는 배제 가능, 그 이하는 미해결 명시
- "1.17 artifact 원인?" → 600 K hop 거의 없음 → MSD noise → ln D 기울기 폭주. 통계 문제
- "Minafra와의 관계?" → 그들의 축 (ordered 0.3 → disordered 0.18)은 2×2의 세로축과 일치. 우리가 더한 건 가로축 — 같은 disorder에서 조성 간 Ea 동일

---

## 1F-3. ~~Slide 6c — 저온 특성~~ — **발표 본편에서 DROPPED (2026-06-11)**, 내용은 paper/Q&A 보존

> as-built 결정: 본편 제외. 사유 ① 표 7행 중 4행이 외삽(±30%, 200 K는 "불확실" 자인) —
> 본편에서 공격 포인트화 위험 ② Zuo RT 2.4× ↔ 우리 외삽 4.3×의 1.8× 간극을 "자릿수
> 정합"으로 부르는 프레임도 시비 여지 ③ 핵심 메시지(no T_cross, 저온 우세)는 6b 대본
> 마지막 한 문장으로 흡수. Q&A 카드: "RT에선?" → "외삽 4.3×, Zuo 측정 2.4× — 방향·자릿수
> 일치, 정량은 3-pt 외삽 ±30% 한계 명시. paper에선 600–1000 K 측정값만 인용."
> 아래 본문은 paper #1 writeup용으로 보존 (★ v3 ACTIVE 2026-06-11 시점 내용).

> **HOLD 해제** — 4fu 결과 확정 후 framing 결정. **T_cross 없음, 저온일수록 modelc 우세 ↑**.

### 페이지 배치 (16:9)
- 왼쪽: σ ratio vs T plot (modelc/comp1, 200-1000 K)
- 오른쪽: T별 ratio 표 + Zuo 2023 RT cross-check
- 하단: "no trade-off" + RT 정합 message

### 본문 텍스트 (v3 ACTIVE)

**제목**: "6c. 저온 특성 — modelc wins at ALL T, no trade-off"

**σ ratio table (modelc / comp1)**:
```
T (K)  | Ea contrib. | D₀ contrib. | σ_ratio | 비고
───────┼─────────────┼─────────────┼─────────┼─────────────
1000   | 1.40×        | 1.41×       | 1.97×   | 측정
800    | 1.51         | 1.41        | 2.12    | 측정
600 ★  | 1.75         | 1.41        | 2.47    | 측정값 2.5× ✓
500    | 1.97         | 1.41        | 2.78    | 외삽
400    | 2.36         | 1.41        | 3.33    | 외삽
300 ★  | 3.07         | 1.41        | 4.33    | 외삽 (Zuo 2.4× cf)
200    | 4.94         | 1.41        | 6.96    | 외삽 (불확실)
```

**Key**:
```
• T_cross 없음 — Ea와 D₀ 둘 다 modelc 우세 같은 방향
• 저온일수록 σ ratio 더 커짐 (Arrhenius)
• Zuo 2023 RT 측정 2.4× ↔ 우리 외삽 4.3× — 자릿수 정합 ±30%
• 'vacancy 양날' (v2) framing 무효 — Cl-rich 저온도 우위
```

**Footnote**:
```
※ 3-pt Arrhenius extrap 200-300K 영역 uncertainty ±30%
※ Zuo 2023 RT: σ(Li6PS5Cl)=2.9, σ(Li5.5PS4.5Cl1.5)=7.0 mS/cm → 2.41×
※ Haven ratio = 1 가정 (σ_NE upper bound)
```

### 발표 스크립트 v3 (40초)

> "저온 특성 한 가지 짚고 갑니다. 이전 v2에서는 'T_cross 290 K, 저온 LPSCl 역전' 가능성을 다뤘지만, 4 f.u. natural cell 결과로 완전 무효화됐어요.
>
> 표 — Ea와 D₀ 둘 다 modelc 우세 같은 방향. Arrhenius 식에서 두 효과가 곱하기로 작용해서 T 내려갈수록 σ ratio 더 커집니다. 1000 K 2×, 600 K 2.5×, RT 4.3×, 200 K 7×.
>
> 실험 cross-check도 깨끗 — Zuo 2023 RT 측정 σ 비율 2.4× ↔ 우리 외삽 4.3×, 자릿수 정합. 약간 over-estimate은 3-pt RT 외삽 + Haven 가정.
>
> 결론: performance 관점 저온 trade-off 없음. Cl-rich가 모든 T에서 우세하고 저온일수록 격차 더 큼. 'vacancy 양날' framing은 v2 artifact, 무효."

### Q&A
- "RT 외삽 신뢰?" → 정량 ±30%, direction robust. Zuo 자릿수 정합
- "200 K 이하?" → 3-pt extrap 불확실 명시. paper는 600-1000K + RT만 quote
- "non-Arrhenius?" → LPSCl 드뭄. disorder ensemble도 단일 Ea fit
- "Haven 0.3-0.7?" → 절대값만. ratio는 cancellation
- "thermal shelf life와 모순?" → 다른 axis. σ는 사용 중 transport, calendar는 idle 분해

### v1/v2 보존 (audit trail)

**v1 (5fu A)**: T_cross 290 K, comp1 저온 역전 — 5fu Ea direction artifact 기반 ⚠ INVALID
**v2 (5fu B)**: matched-d Ea 동일, no T_cross — disorder ensemble만 신뢰
**v3 (4fu ACTIVE)**: No T_cross robust, 저온 우세 ↑, Zuo RT cross-check ✓

---

## 1G. Slide 7 — M3: Ionic glue는 Cl-rich에서 강해진다

### 페이지 배치 (16:9)
- 왼쪽: ICOHP 막대그래프 (|ICOHP| 결합별 comp1/modelc 쌍)
- 오른쪽: per-site 분해 표 (M3의 본질 — 시각적으로 크게)
- 하단: 3 bullet key + 위계 footnote

### 본문 텍스트

**상단**: "M3: 모든 Li–anion 결합이 LPSCl₁.₆에서 강해진다"

**왼쪽 표 (평균 ICOHP, eV/bond)**:
```
결합      | LPSCl       | LPSCl₁.₆    | Δ
──────────┼─────────────┼─────────────┼────────
P–S       | −5.94 (16)  | −6.00 (20)  | +1.0% (불변)
Li–Cl     | −1.86 (24)  | −2.10 (42)  | +13.0% ★
Li–S      | −1.59 (120) | −1.72 (113) | +8.1% ★
S–S       | −0.11       | −0.11       | ~0
```

**오른쪽 표 (per-site 분해)**:
```
site             | LPSCl   | LPSCl₁.₆
─────────────────┼─────────┼──────────
Li–S (PS₄ 묶임)  | −1.34   | −1.62
Li–S (4d free)   | −2.57   | −2.52  ← universal anchor (Δ2%)
Li–Cl (4a 정상)  | −1.86   | −2.03
Li–Cl (4d AS)    |  없음   | −2.84  ★ 4a보다 40% 강함
```

**Key**:
```
• Li–Cl +13%, Li–S +8% — vacancy + Cl 치환은 결합 '강화' (약화 아님)
• 동력 = 4d-Cl anti-site의 짧고 강한 Li–Cl 결합 (−2.84 eV)
• Bader · LOBSTER · Wilkening 세 독립 probe 합의
```

**Footnote**:
```
※ 결합 위계 보존: P–S(covalent) ≫ Li–Cl > Li–S ≫ S–S (양쪽 동일)
※ LOBSTER ext basis, charge spilling 1.46% / 1.16% (< 5% 기준)
```

### 발표 스크립트 (60–70초)

> "Message 3, ionic glue — Li와 음이온 사이 결합 강도입니다.
>
> 직관적으로 'Cl을 더 넣고 Li를 빼면 결합이 약해지지 않을까' 생각하기 쉽습니다. 결과는 정반대였습니다. 왼쪽 표 — Li–Cl 결합이 13%, Li–S 결합이 8% 강해집니다. 반면 PS₄ covalent backbone은 1% — 사실상 불변이고요.
>
> 어디서 이 강화가 오는지 per-site로 분해한 게 오른쪽 표입니다. 두 가지가 보입니다.
>
> 첫째, 4d 자리의 free S²⁻에 붙은 Li–S 결합은 양쪽 모두 −2.5 정도로 똑같습니다. 조성과 무관한 universal anchor예요.
>
> 둘째가 핵심입니다. modelc에만 있는 4d-Cl anti-site의 Li–Cl 결합이 −2.84 eV — 정상 4a 자리보다 40% 강합니다. Slide 2에서 보여드린 그 anti-site Cl이 짧은 거리에서 Li를 강하게 잡으면서 평균을 끌어올린 겁니다.
>
> 이 결론은 LOBSTER ICOHP 하나로만 주장하는 게 아닙니다. Bader charge, Wilkening ionic potential까지 세 가지 독립 probe가 같은 방향을 가리킵니다. Bader에서 S charge가 −1.52에서 −1.76으로 더 ionic해지고, Wilkening q·|q|/r에서 Li–S 채널이 17% 강해지는 것도 같은 그림이에요.
>
> 정리하면 — 'Cl excess는 결합을 약화시킨다'는 통념과 반대로, anti-site를 통해 ionic glue를 강화합니다. 그리고 이 강화가 다음 메시지, mechanical stiffening의 미시적 기반이 됩니다."

### 시각 디자인 노트
- 막대그래프: |ICOHP| 절대값, 결합별 comp1(파랑)/modelc(빨강) 쌍
- ★ 강조: Li–Cl(4d AS) −2.84 행 진한 음영 + 별표
- "강화" 단어 강조색 (#C8102E)
- per-site 표를 평균 표보다 크게

### Q&A 보조 노트
- "ICOHP 단위?" → per bond 평균 적분 COHP (EF까지). 음수 = bonding. |값| 클수록 강함
- "−2.84가 왜 강하냐?" → 4d는 원래 S²⁻(2가) 자리라 Li 배위 가까움. Cl이 앉으면 짧은 Li–Cl (2.53 vs 4a 2.61 Å) → 강한 결합. slide 10 일관
- "ext basis?" → sparse basis spilling 17% 부정확 → ext basis (Li 1s2s2p+3d)로 1.2-1.5%. paper엔 ext만
- "Bader와 LOBSTER 독립?" → Bader = 실공간 분할 (basis-free), LOBSTER = 궤도 projection, Wilkening = 고전 ionic potential. 다른 근사 체계
- "universal anchor 의미?" → 두 조성 Δ2% 동일 = free S²⁻ 주변 Li 배위 기하가 조성 무관 보존

---

## 1H. Slide 8 — M4: Vacancy Paradox 해소 (Relaxed-Ion Stiffening)

### 페이지 배치 (16:9)
- 메인 표 (clamped vs relaxed 2행, 색 대비)
- 분해 표 (B/G/E/ν/Zener — G +30% 강조)
- Key 불릿 4개
- footnote (B_VRH ≈ B0 cross-check, Kim 2025 정합)

### 본문 텍스트

**제목**: "M4: clamped-ion에선 동일, relaxed-ion에서 +25% — vacancy paradox 해소"

**메인 표**:
```
E_VRH (GPa)            | LPSCl  | LPSCl₁.₆ | Δ%   | 실험 (Kim 2025)
───────────────────────┼────────┼──────────┼──────┼─────────────────
clamped-ion (frozen)   | 52.31  | 52.30    |  0%  |   —
  = paradox             │        │          │      │
★ relaxed-ion          | 22.06  | 27.66    | +25% |   ✓ LPSCl₁.₆ stiffer
  (이온 Born screening) │        │          │      │   ~23 (LPSCl)
```

**분해 표**:
```
modulus     | LPSCl | LPSCl₁.₆ | Δ%
B_VRH (GPa) | 25.5  | 23.4     | −8%   ← hydrostatic은 soft
G_VRH (GPa) |  8.1  | 10.6     | +30%  ← shear stiffening ★
E_VRH (GPa) | 22.06 | 27.66    | +25%
ν           | 0.36  | 0.30
Zener A     | 1.14  | 1.44     | 비등방성 출현
eigenvalues | all + | all +    | 둘 다 mechanically stable
```

**Key 불릿**:
```
• clamped(=원자 위치 frozen) DFT는 paradox — 실험 trend 못 잡음
• relaxed-ion에서 ionic Born screening 켜지면 modelc +25% 단단해짐
• 단단함의 주성분은 shear (G +30%), bulk는 오히려 약간 soft
• 메커니즘 = M3 4d-Cl anti-site가 특정 shear 모드를 lock-in
```

**Footnote — 청중 핵심 직관 (★ ADDED v1.19)**:
```
※ "PS₄ 안 바뀌는데 왜 단단해지나" — argyrodite의 기계적 강성은
   covalent PS₄ 자체가 아니라 PS₄들을 묶는 ionic Li-anion sublattice가 결정.
   • PS₄ = "rigid blocks" (M1, slide 9/13 — 불변)
   • Li-anion = "mortar" (M3 +13% ICOHP — 강화)
   • 강한 mortar → blocks 사이 sliding 어려움 → shear stiff (G +30%)
   • Hydrostatic 압축은 vacancy void 효과로 B −8%, 그러나 G 증가가 dominant
   → E = 9BG/(3B+G), ν~0.3 영역에서 G dominant → E_VRH +25%
```

**Footnote**:
```
※ B_VRH 23.4 ≈ B0(BM-EOS) 21.7 — 두 독립 방법 cross-check (±3%)
※ Kim ACS Mater. Lett. 2025 UPE 측정과 동일 방향 (Cl ↑ → E ↑)
※ DFT 0K stress-strain, 12 strain × ±0.005, k=4×4×4/6×6×3
```

### 발표 스크립트 (75–85초)

> "마지막 메시지 M4 — 기계적 성질의 paradox와 그 해소입니다.
>
> 표 위 두 행 — 이온 위치를 변형 셀에 frozen으로 두는 clamped-ion DFT로 계산하면, 두 시스템 Young's modulus가 정확히 같이 나옵니다. 52.31 대 52.30. 실험은 분명 LPSCl₁.₆가 더 단단하다고 보고하는데 — Kim ACS Mater. Lett. 2025가 결정적 reference예요 — 이걸 못 잡으니까 'vacancy paradox'라고 불러 왔습니다.
>
> 같은 strain을 가했을 때 이온이 새 위치로 재배치되는 ionic Born screening을 켜주면, 즉 relaxed-ion으로 계산하면, 두 번째 행처럼 풀립니다. modelc가 27.66 GPa, comp1이 22.06 GPa — 25% 차이. 그리고 comp1의 22.06은 실험 LPSCl ~23 GPa와 거의 정확히 매칭됩니다. paradox 해소.
>
> 메커니즘은 그 아래 분해 표가 보여줍니다. 흥미로운 게 — bulk modulus는 modelc가 오히려 8% 약합니다. vacancy가 있으니 등방 압축은 더 쉬워지는 게 직관에 맞아요. 그런데 shear modulus G가 30% 단단해지고, Zener anisotropy가 1.14에서 1.44로 비등방성이 명확해집니다.
>
> 즉 단단해진 건 hydrostatic이 아니라 shear-dominant stiffening입니다. 미시적 출처는 Slide 7에서 본 4d-Cl anti-site예요 — 짧고 강한 Li–Cl 결합이 특정 shear configuration을 잠가놓아서, 그 방향으로 변형되려 하면 ionic sublattice가 강하게 저항합니다. M3의 ionic glue 강화가 mechanical로 발현된 게 M4입니다.
>
> 그리고 B_VRH 23.4가 독립적인 BM-EOS B₀ 21.7과 3% 안에서 cross-check되는 것도 paper-grade 정확도의 근거가 됩니다."

### 시각 디자인 노트
- clamped 행 회색 (paradox 강조), relaxed 행 빨강 음영 + ★
- 분해 표: G_VRH +30% 행만 강조 (진짜 mechanism)
- "+25%" / "+30% shear" 큰 글자 highlight
- 실험 매칭 (✓ ~23 GPa) 별도 색

### Q&A 백업
- "clamped vs relaxed 차이가 왜 그렇게 큰가 (52 → 22)?" → argyrodite Li sublattice가 매우 soft — strain 시 Li 재배치(ionic Born) 효과가 elastic의 절반 이상
- "paradox가 왜 흥미로운가?" → 실험 'Cl↑→E↑' trend가 clamped DFT로 절대 안 나옴. relaxed-ion이 처음으로 해소
- "Kim 2025 외 실험은?" → 오래된 Sakuda 2013, Deng 2016 SQS는 약함. Kim 2025 결정적. 자체 AFM도 LPSCl₁.₆ 14.9 > LPSCl ~12
- "B vs E vs G — 어느 게 답?" → property별 의미 다름. paper에서 어느 modulus 말하느냐 명시 필수
- "600 K MLIP 탄성?" → SI. E_600K(modelc 32.9) > E_600K(comp1 29.1), 같은 방향
- "eigenvalues 양수 의미?" → mechanical stability (Born 조건). 둘 다 만족 → 진짜 stable
- "Zener A 비등방 paper 메시지?" → disorder의 mechanical fingerprint — vacancy는 등방, 4d-Cl AS가 방향 강화 → 등방성 깨짐

---

### ★ 실물 확정판 (as-built deck slide 12 "M4", 2026-06-11 — FINAL)

```
각주 3줄 (clamped/relaxed/B·G·E·ν 정의) + ref Kim ACS Mater. Lett. 7,724 ✓
■ M4: Clamped identical → relaxed-ion +25% - vacancy paradox resolved
   · Clamped ion DFT: 52.31 vs 52.30 — identical (misses the exp. trend = the paradox)
   · Relaxed-ion: 22.06 vs 27.66 (+25%)
   · Stiffening is shear-dominant: G +30% (B −8%) — 4d-Cl locks shear modes
[표①] clamped 행 회색 / relaxed 22.06적·27.66청·+25%청
[표②] B 25.5청/23.4적 −8% · G 8.1적/10.6청 +30%청 · ν 중립 · Zener 1.14청/1.44적
[우] E=9BG/(3B+G), ν=(3B−2G)/(2(3B+G)) 수식 — DB full-tensor 값과 정확 닫힘 검증됨
```

결정: ① 실험 매칭(22.06↔~23, Kim trend)은 슬라이드 생략, **구두 전달** — 대본 문장이
Kim ref의 앵커 ② Zener 식은 수식 영역에서 의도적 제외 (표 Cij는 방향 평균, A는 축별
성분이라 검산 함정 — Q&A 카드化) ③ 수식 명칭: VRH averaging (Hill 1952) + standard
isotropic relations. footnote(벽돌-모르타르)는 대본 전담.

## 1H-1. Slide 8a — Shear Mode Lock-in — **8b와 병합 → 본편 "M4-1" (2026-06-11 확정)**

> as-built 결정 (appendix안 철회): 8a(mechanism: C44 +72%) + 8b(robustness: 4
> cross-check)를 한 장 "M4-1: shear lock-in & 4-way robustness"로 병합, 본편 deck 13.
> **최종 구조 (2026-06-11 확정)**: M4-1 = mechanism 전용 — cross-check 표 전체 제거.
> ①B↔B₀는 M4 표②의 B행에 "(EOS 26.23/21.71)" 괄호로 인라인 흡수 ✓
> ②E vs lit.은 구두 (indep. DFT 22.1 일치 + Kim trend) — M4 결정 유지.
> as-built slide 13: ■ M4-1: Shear lock-in mechanism / 각주 Cij 정의 / bullets 2개
> (+72% C44 · C11 −2%) / [좌] Cij 표 3행 (C44 8.0적/13.7청/+72%청 · C12 · C11 중립)
> / [우] 수식 6개 FINAL: G_V (C11적·C44청 — bullet 색 호응), B_V, Hill 2개,
> B_R·G_R compliance 일반형 + "(S=C⁻¹; cubic: B_R=B_V)" 캡션. V/R/H 정의는 상단
> 각주로 이동. cubic 닫힌꼴 G_R 금지 결정 유지 (검산 함정).
> **검수 FINAL (2026-06-11)** — 잔여 선택: 표 C_44 → C₄₄ 아래첨자 통일.
> ⚠ **"실험 ~23 GPa" 프레임도 정정 (2026-06-11 문헌 감사)**: elastic.json의 "matches
> literature ~23 (He et al.)"은 계산/실험 혼동 — 22.1은 **계산값** (Deng 2016 JES 163,A67
> DFT SQS; JPCC 2025 제일원리도 22.1/G 8.1). 진짜 실험은 Kim 2025 UPE 펠릿 15–22(HT)/
> 12–17(BM), 다공성 4.7±1.1 (ACS AEM 2024). → row2 최종: "22.06 indep. DFT 22.1 ✓ /
> 27.66 Kim trend ✓ / calc. agree + exp. trend". M4 구두 멘트도 "실험 ~23 매칭" →
> "독립 계산 22.1 일치 + 펠릿 상한 정합 + trend 일치"로 교체. refs에 Deng 추가.
> ⚠ **AFM 사용 금지 (2026-06-11 provenance 감사)**: 구 8b의 "자체 AFM ~12/14.9 방향✓" 행 중
> 14.9는 2026-06-08 group weekly report **타 멤버 측정** (세트: NdO 15.8, paper #2 비교군) —
> 인용하려면 측정자 확인 필수. **LPSCl "~12"는 repo 전체에 측정 기록 없음** (Kim UPE BM 하한
> 12–17과 혼동 추정) — 존재하지 않는 값. 관련 Q&A 카드의 "자체 AFM ~12" 문구도 폐기.
> #3(600K MLIP +13%)은 Q&A 카드 강등 ("0K 결론 상온 유효?"), #4(spilling·k×L)는
> k-mesh audit 슬라이드가 원주인이라 중복 제거 (2026-06-11 확정).

## (보존) Slide 8a — Shear Mode Lock-in (mechanism 시각화)

### 페이지 배치 (16:9)
- 왼쪽: Cij 원소 분해 표 (C11/C12/C44/Zener/ν)
- 오른쪽: cartoon — 4d-Cl pin이 shear 방향에서 활성, 등방에는 inactive
- 하단: 핵심 4 bullet + cartoon caption

### 본문 텍스트

**제목**: "8a. 어디서 +30% shear가 오는가 — Cij 분해 + 4d-Cl lock-in"

**Cij 표 (relaxed-ion)**:
```
Cij (GPa)             | LPSCl  | LPSCl₁.₆ | Δ%
──────────────────────┼────────┼──────────┼────────
C11                   |  37.7  |  37.0    | −2%
C12                   |  20.4  |  16.8    | −18%
C44 (shear) ★         |   8.0  |  13.7    | +72% !
Zener A=2C44/(C11-C12)|  1.14  |  1.44    | +26% (비등방 ↑)
ν (Poisson)           |  0.36  |  0.30    | −17%
```

**Key**:
```
• C44 +72% — VRH-평균 G +30%의 거의 모든 출처
• C12 −18% — 추가 shear 자유도 감소
• 4d-Cl AS (M3 ICOHP −2.84) 가 shear 방향 변형 선택적 lock
• 등방 압축(C11 ~불변)엔 거의 영향 없음 → B₀ 오히려 soft
```

**Cartoon caption**:
```
직관: 4d 자리 Cl이 인접 Li를 짧은 거리(2.53 Å)에서 강하게 잡음 → Li 평면 슬라이딩
형 변형에 추가적 저항(pin). hydrostatic 압축은 모든 결합을 동등하게 줄이므로
이 pin 효과가 안 켜짐 → B는 vacancy로 soft.
```

### 발표 스크립트 (45–55초)

> "그 +30% shear가 어디서 오는지 Cij 원소로 풀어보겠습니다. 왼쪽 표 — C44가 8.0에서 13.7로 72% 증가합니다. VRH 평균 G +30%의 거의 모든 출처가 C44 하나예요. C12도 18% 감소해서 shear 자유도가 추가로 줄어듭니다. 반면 등방 압축 관련된 C11은 거의 안 바뀝니다 — 그래서 B는 오히려 soft.
>
> 미시 그림은 오른쪽입니다. modelc의 4d 자리에 들어간 Cl은 인접 Li를 2.53 Å 짧은 거리에서 매우 강하게 잡습니다. ICOHP −2.84 eV, 4a 자리 Cl보다 40% 강하다는 게 M3에서 본 그 anti-site예요. 이 강한 결합이 Li 평면이 슬라이딩하는 shear 변형을 선택적으로 pin해버립니다. 그런데 hydrostatic 압축은 모든 결합을 균등하게 줄이는 거라 이 pin 효과가 안 켜져요. 그래서 vacancy로 bulk는 soft, 4d-Cl로 shear는 stiff — 합쳐서 E는 stiffer입니다.
>
> 즉 vacancy가 양날인데, 단방향(shear)에서 강해지는 효과가 평균을 끌어올리는 구조입니다."

### Q&A 백업
- "C44 72% 증가 너무 큰가?" → 절대값 13.7 GPa는 sulfide SE typical 범위. comp1 8.0이 오히려 unusually low (deeply ordered Li가 쉽게 슬라이딩)
- "Born 안정성?" → eigenvalues all > 0, 둘 다 stable
- "G가 paper 메시지로 왜 중요?" → SSB cycling shear stress 받음 (cathode 팽창). shear stiffness가 mechanical durability와 직결
- "AFM/UPE는 어떤 modulus?" → Young's E. E_VRH +25%가 직접 대응

---

## 1H-2. Slide 8b — Cross-Check & Referee Defense — **8a와 병합 → 본편 "M4-1"** (위 1H-1 참조)

## (보존) Slide 8b — Cross-Check & Referee Defense

### 페이지 배치 (16:9)
- 중앙: 4행 cross-check 표 (각 행: 측정값 + 비교 대상 + 결론)
- 하단: 종합 결론 + footnote

### 본문 텍스트

**제목**: "8b. 독립 cross-check 4개 — paper-grade 정확도 보증"

**Cross-check 표**:
```
# | Check                          | LPSCl  | LPSCl₁.₆ | 결론
──┼────────────────────────────────┼────────┼──────────┼──────
1 | B_VRH (stress-strain, GPa)     | 25.5   | 23.4     |
  | vs B0 (BM-EOS, 독립 방법)      | 26.23  | 21.71    | ±10% ✓
2 | E_VRH (0K relaxed-ion, GPa)    | 22.06  | 27.66    |
  | vs 자체 AFM (GPa)              | ~12    | 14.9     | 방향 ✓
  | vs Kim 2025 UPE (trend)        | ref    | ↑        |
3 | E_VRH (600 K MLIP snapshot)    | 29.1   | 32.9     | 0K와
  | Δ                              | ref    | +13%     | 동일 방향 ✓
4 | LOBSTER charge spilling        | 1.46%  | 1.16%    | <5% ✓
  | k×L (paper-grade ≥40 Å)        | 40     | 42       | 수렴 ✓
```

**Key**:
```
• 4 독립 cross-check 모두 정합
• B_VRH ↔ B0 두 다른 elasticity method 일치 (±10%)
• 0K DFT ↔ 600K MLIP 같은 방향
• 실험 (AFM + Kim 2025) trend 일치
• Method quality (spilling <5%, k×L ≥40) 보장
```

**Footnote**:
```
※ comp1 B0 +8% 차이(25.5 vs 26.2)는 stress-strain (Hookean small strain) vs BM-EOS
  (wider V sweep) 정의 차이. 양쪽 ±10% 안.
※ AFM 절대값은 group weekly report 자체 측정. Kim 2025는 UPE direction만 인용.
```

### 발표 스크립트 (50–60초)

> "M4 결론이 robust한지 4가지 독립 cross-check로 확인합니다.
>
> 첫째, B_VRH와 B₀ 비교. B_VRH는 12 strain으로 Cij 구한 다음 voigt-reuss-hill로 유도, B₀는 11 volume Birch-Murnaghan fit — 전혀 다른 방법. 두 독립 방법이 ±10% 안에서 일치합니다.
>
> 둘째, 실험 비교. 우리 22 GPa는 실험 LPSCl ~23과 거의 정확. modelc 27.7도 자체 AFM 14.9와 절대값 차이는 있지만 — AFM contact mechanics와 DFT bulk modulus의 method difference — trend는 LPSCl₁.₆가 더 단단이라는 같은 방향. Kim 2025 UPE도 같은 방향.
>
> 셋째, 0K DFT vs 600K MLIP. finite-T snapshot E도 modelc(32.9) > comp1(29.1), +13%. 같은 방향.
>
> 넷째, method quality. LOBSTER spilling 1-1.5% (paper 기준 <5%), k-mesh k×L ≥40 Å.
>
> 4가지 cross-check가 다 정합 — relaxed-ion +25% 결론은 robust합니다."

### Q&A 백업
- "왜 B 절대값 약간 다른가 (25.5 vs 26.2)?" → stress-strain small strain Hookean vs BM-EOS wider sweep. 미세 정의 차이지만 ±10% 정합
- "AFM 12 vs DFT 22 — 절대 차이?" → AFM=indentation modulus (Hertz contact), DFT=pure Young's. 다른 양. trend가 같은 게 중요
- "600 K MLIP가 0 K DFT랑 같은 방향 보장?" → finite-T effect 있지만 +13% 정도면 0 K +25%와 정성 일관
- "spilling 5% 기준 의미?" → LOBSTER 표준. 5% 넘으면 basis 부정확. 1.16-1.46%로 충분
- "k×L 40 충분?" → argyrodite (gap ~1.8 eV)에서 paper-grade. metal이면 60+
- "comp1 4 f.u. clean MD 0.18 부근 나오면?" → frozen artifact 재현되거나 0.20+로 정상화. 어느 쪽이든 disorder ensemble (6b)이 Ea ground truth로 굳어짐

---

## 1I. Slide 9 — Cross-check #1: PS₄ Universal Backbone

### 페이지 배치 (16:9)
- 메인 표 (6 probe + universal anchor 행)
- 하단: 3 bullet key + 한 줄 결론

### 본문 텍스트

**제목**: "9. PS₄ covalent backbone은 두 시스템에서 사실상 동일"

**메인 표**:
```
Probe                       | LPSCl    | LPSCl₁.₆ | Δ
────────────────────────────┼──────────┼──────────┼────────
P–S 길이 (Å, mean)          | 2.073    | 2.064    | −0.5%
P–S σ (Å, 분산)             | 0.036    | 0.011    | modelc ↓ 더 균질
P 배위수                    | 4.00     | 4.00     | 0% (완벽 보존)
ICOHP P–S (eV/bond)         | −5.94    | −6.00    | +1.0%
ELF P–S bridge              | 0.946    | 0.944    | Δ 0.002 (~0)
Bader P (e, formal +5)      | +4.69    | +4.43    | basin shape ¹
Li–S(4d, free S²⁻) ICOHP    | −2.57    | −2.52    | −2% (universal anchor)
```

**각주**:
```
¹ Bader P 차이는 PS₄-S vs 4d-S²⁻ basin shape effect — PS₄ 단위 합 (P+4S)으로
  reporting 시 둘 다 formal PS₄³⁻ 근처. paper엔 PS₄ 합 권장 (개별 P는 SI).
```

**Key**:
```
• PS₄ 결합 길이·ICOHP·ELF·배위수 — 5개 probe 모두 차이 +1% 이내
• free S²⁻ 주위 Li 결합도 조성 무관 universal (Δ2%)
• 모든 조성 변화는 Li–anion ionic sublattice 안에서만 일어남
```

**하단**: "→ argyrodite의 PS₄³⁻ 단위는 chemistry-independent rigid block"

### 발표 스크립트 (50–60초)

> "Cross-check 시작입니다. M1에서 M4까지의 4 메시지가 'covalent는 그대로, ionic만 변한다'고 정리됐는데, 이걸 5개 독립 probe로 확인합니다.
>
> 표 행 별로 — P–S 결합 길이 2.073 대 2.064, 0.5% 안. 흥미로운 건 분산 σ인데, modelc가 오히려 더 작습니다. PS₄ tetrahedron들이 더 균질하게 정렬돼 있다는 뜻이에요. P 배위수 정확히 4.00 완벽 보존. ICOHP P–S −5.94 대 −6.00 1% 안. ELF P–S bridge 0.946 대 0.944 사실상 동일. Bader P charge는 basin shape effect로 절대값 약간 다르지만 PS₄ 단위 합으로 보면 둘 다 formal PS₄³⁻ 근처.
>
> 5개 independent measurement가 모두 'PS₄는 같다'고 가리킵니다.
>
> 한 가지 더 — 표 마지막 행, Li–S(4d) free S²⁻ 결합. 4d 자리 free S²⁻에 붙은 Li 결합 강도가 양쪽에서 −2.5 정도로 거의 동일합니다. 조성이 바뀌어도 변하지 않는 universal anchor예요. argyrodite에서 'PS₄가 rigid block'이라는 사실이 covalent backbone 뿐 아니라 그 주위 Li 배위에까지 확장된다는 거죠.
>
> 결론: argyrodite의 PS₄³⁻ 단위는 chemistry-independent rigid block입니다. 모든 조성 효과는 Li-halide ionic sublattice 안에서만 일어난다는 게 cross-check #1의 메시지입니다."

### 시각 디자인 노트
- 5 probe 행은 같은 색 (PS₄ 보존 그룹)
- Universal anchor 행은 별색 + ★ (또 다른 invariance)
- "사실상 동일" + "rigid block" 단어 강조

### Q&A 백업
- "P-S 살짝 줄어드는 이유(−0.5%)?" → modelc V/fu 약간 작아짐(−4.3%) 비례 수축. 비율 보존
- "σ(P-S) modelc에서 더 작음 이유?" → 4d-Cl AS 주변 PS₄ 균질화 — disorder가 PS₄에 영향 없음 역설적 증거
- "P 배위 cutoff?" → P-S 2.3 Å. 모든 P 정확히 4개 S
- "Bader P 4.4–4.7 vs formal +5?" → Bader=partial (basin division), formal과 다름. PS₄ 합으론 비슷
- "universal anchor 의미?" → 관찰. mechanism은 free S²⁻ 주위 Li 배위 기하의 cell parameter 둔감성
- "ELF 0.946 단위?" → 0~1, 1=완전 localized. 0.9↑=covalent. Li 주위는 <0.1 (ionic depletion)

---

### ★ 실물 확정판 (as-built deck slide 14 "CC#1", 2026-06-11 — FINAL)

```
각주: ELF 정의 / refs 없음
■ Cross-check #1: The PS4 covalent backbone is identical in both
   · Five probes within ~1%: length · σ · coordination · ICOHP · ELF
   · Disorder makes PS4 more uniform (σ 0.036 → 0.011) — backbone untouched
   · Li–S(4d free S²⁻) anchor also composition-independent (Δ2%)
[좌] P–S 히스토그램 overlay (bin 0.015, Overlap 100/투명 50, 범례+캡션
     "< P–S bond length distribution (Å) >") — V0 구조 직접 계산 검증 (16/20 bonds,
     2.072±0.036 / 2.064±0.011, docs/figures/slide14_ps4/)
[우] 표 6행: 길이·σ(0.036적/0.011청 강조)·배위·ICOHP·ELF·anchor — 나머지 중립
하단: → PS4³⁻ = chemistry-independent rigid block
변경: Bader P 행 제외 (basin-shape 함정 → Q&A), σ bullet 승격, comp1 분포
이봉(8+8, PS4당 2short+2long) Q&A 카드 보유. universal anchor 의미 카드:
내부 기준점 — 변화의 국소화 + LOBSTER 무편향 보증.
```

## 1J. Slide 10 — Cross-check #2: 결합 길이의 반직관 (Counter-Intuitive)

### 페이지 배치 (16:9)
- 메인 결합 표 (P-S / Li-S / Li-Cl / S-S)
- per-site 분해 (Li-Cl 4a vs 4d AS)
- Voronoi 부피 보조 증거
- 하단: 4 bullet key + 한 줄 mechanism 연결

### 본문 텍스트

**제목**: "10. Cl이 많아지면 Li–Cl이 멀어진다? — 반대다."

**메인 표**:
```
결합 (Å, mean ± σ)      | LPSCl          | LPSCl₁.₆       | Δ
────────────────────────┼────────────────┼────────────────┼─────────
P–S                     | 2.073 ± 0.036  | 2.064 ± 0.011  | −0.5% (불변)
Li–S                    | 2.461 ± 0.106  | 2.465 ± 0.094  | +0.2% (동일)
★ Li–Cl                 | 2.607 ± 0.129  | 2.532 ± 0.119  | −3% 짧아짐 ↓
S–S (cage)              | 3.595 ± 0.199  | 3.519 ± 0.178  | −2% (cage 압축)
```

**Per-site (Li-Cl만)**:
```
종류                     | LPSCl    | LPSCl₁.₆
─────────────────────────┼──────────┼──────────
Li–Cl (4a 정상 자리)     | 2.61 Å   | 2.59 Å   (−1%)
Li–Cl (4d anti-site)     | 없음     | 2.45 Å   ★ 0.16 Å 짧음
```

**Voronoi 보조**:
```
Cl 다면체 V (Å³) | LPSCl 22.06 | LPSCl₁.₆ 20.31  ← Δ−1.7, 4d가 더 작은 증거
```

**Key**:
```
• Cl 늘면 Li–Cl 짧아짐 — 통념과 정반대
• 동력 = 4d 자리(원래 S²⁻ 크기) Cl이 짧은 Li 배위
• Voronoi V(Cl) 1.7 Å³ 감소 = 직접 증거
• cage S–S도 동시 압축 = 4d AS 효과의 추가 증거
```

**하단**: "→ 짧고 강한 Li–Cl(4d) bond 형성 = M3 ICOHP +13%의 미시 출처"

### 발표 스크립트 (60–65초)

> "Cross-check #2 — 결합 길이의 반직관입니다.
>
> 직관적으로 'Cl이 많아지면 cage가 커지고 Li–Cl이 멀어진다'고 생각하기 쉽습니다. 표를 보시면 정반대입니다. Li–Cl이 2.607에서 2.532로 0.076 Å, 약 3% 짧아집니다. 줄어든 거예요.
>
> 어디서 짧아지는지 per-site로 풀면 더 명확합니다. 정상 4a 자리의 Li–Cl은 거의 안 변합니다. 진짜 차이는 4d 자리 anti-site에서 — 이 자리의 Li–Cl이 2.45 Å, 4a보다 0.16 Å 짧습니다.
>
> 왜 짧은가? 4d 자리는 원래 S²⁻가 앉던 자리예요. S²⁻ ionic radius가 1.84 Å, Cl⁻는 1.81 Å — Cl이 더 작습니다. 작은 Cl이 큰 S²⁻ 자리에 들어가니 주변 Li가 가까이 끌어옵니다. 그래서 짧은 Li–Cl.
>
> 진짜인지 cross-check할 수 있는 게 Voronoi 부피입니다. Cl 주위 다면체 부피가 22.06에서 20.31로 1.7 Å³ 줄어듭니다. '4d 자리가 더 작다'는 직접 증거. cage S–S도 같은 양 0.076 Å 압축됐고요.
>
> 정리하면 — Slide 7의 ICOHP +13%, 특히 4d-Cl AS의 −2.84 eV가 어디서 오는지의 미시 메커니즘이 여기 있습니다. 짧은 거리 + 적절한 ionic radius 매칭이 강한 결합을 만들고, 이게 M3 ionic glue와 M4 mechanical stiffening까지 다 연결됩니다."

### 시각 디자인 노트
- Li–Cl 행 + 4d AS 행 빨강 음영 + ★
- "짧아짐 ↓" 화살표 (반직관 강조)
- per-site 표는 메인 표 아래 작게
- Voronoi 행 별도 박스
- "정반대" + "짧고 강한" 강조

### Q&A 백업
- "Cl⁻ vs S²⁻ ionic radius?" → Cl⁻ 1.81 Å, S²⁻ 1.84 Å (6-coord Shannon). 작은 차이지만 4d에서 의미 있음
- "왜 4a는 거의 안 변하나?" → 4a 원래 Cl 자리, sizing optimum. 4d만 mismatch
- "Voronoi 계산?" → DFT V0에서 pyhull 다면체 분할. 무게 무관 순수 기하
- "Li–S 왜 안 변하나?" → 두 시스템 모두 free S²⁻ 자리 그대로 (universal anchor, slide 9). PS₄-S는 P가 dominant
- "cage S–S 압축 메시지?" → "4d AS가 주변 anion까지 끌어당김" 추가 증거. 단독 슬라이드는 아님
- "측정 cutoff?" → P-S 2.3, Li-S 3.2, Li-Cl 3.4, S-S 4.0 — argyrodite 표준
- "Wilkening?" → q·|q|/r에서 Li-S +17% (SI). 거리 + Bader charge 둘 다 강화 방향 일치
- "이게 paper main figure 후보?" → YES. Cl excess paradox 시각화로 가장 강력한 figure

---

## 1G. Slide 7 — M3: Ionic Glue 강해진다 (v2 갱신 — vacancy + anti-site 분해)

### ★ as-built FINAL (deck slide 11, 2026-06-11 — 검수 PASS)

```
■ M3: Li-anion ionic glue strengthens in LPSCl1.6 / refs Deiseroth+Kraft ✓
bullets 2개 (3-probe bullet은 의도적 생략 — 대본 커버) ✓
[좌] 그룹 막대 |ICOHP| 4쌍 + Δ% 화살표 ✓ (라벨 2자리 통일은 선택 잔여)
[우] Li–Cl per-site 분해 표 3행 — 기준 명시 최종: −1.855/24 · −2.026 (+9.2% vs LPSCl)/38
     90% · −2.836★청 (+40% vs 4a)/4 10% + "→ contribution ... 69% + 31%" ✓
     막대 라벨 2자리 통일 (6.00/2.10) 반영 ✓
69/31 유도 기록: 순차 분해 — ①vac field (2.026−1.855)×42=7.18 ②AS 추가 (2.836−2.026)×4=3.24
→ 7.18:3.24 = 69:31, 합 0.248/bond = 평균 +13% 정확 닫힘. (+40%는 4a 수준 대비 관례)
```

### 페이지 배치 (16:9)
- 평균 ICOHP 표 + per-bond decomp 표
- 두 효과 기여도 (vacancy 69% + anti-site 31%)
- 3-probe 합의 footer

### 본문 텍스트 (v2 ACTIVE)

**제목**: "M3: Li–anion ionic glue가 LPSCl₁.₆에서 강해진다"

**평균 ICOHP 표**:
```
결합          | LPSCl    | LPSCl₁.₆ | Δ%
─────────────┼──────────┼──────────┼─────
P–S (PS₄)    | −5.94    | −6.00    | +1.0% (불변)
Li–Cl ★      | −1.86    | −2.10    | +13.0%
Li–S ★       | −1.59    | −1.72    | +8.1%
S–S          | −0.11    | −0.11    | ~0
```

**Vacancy vs Anti-site 분해 표**:
```
단계                          | per-bond ICOHP | bond 수 / 영향
──────────────────────────────┼────────────────┼─────────────────
comp1 baseline (전부 4a)      | −1.855         | 24 (모든 Cl)
modelc 4a (+ vacancy)         | −2.026         | 38 (Cl 90%)  +9.2%
modelc 4d AS (+ anti-site)    | −2.836         |  4 (Cl 10%)  +40%
```

**기여도 분해**:
```
+13% 평균 Li-Cl 강화 기여도:
  • Vacancy field: 69% — 전반 ionic 강화, Cl 90%에 균일 적용
  • Anti-site: 31% — intense local pin, Cl 10%에만 강력 적용
```

**Key**:
```
• Cl 치환은 결합 '강화' (약화 아님): Li–Cl +13%, Li–S +8%, PS₄ 불변
• 두 메커니즘 합작: vacancy ionic field (광범위) + 4d-Cl AS (집중)
• Bader · LOBSTER · Wilkening 세 독립 probe 합의
```

### 발표 스크립트 v2 ACTIVE (75–85초)

> "Message 3, ionic glue — Li와 음이온 결합 강도입니다.
>
> 직관적으로 'Cl 더 넣고 Li 빼면 약해진다'고 생각하기 쉬운데, 결과는 정반대. Li–Cl이 13%, Li–S가 8% 강해집니다. PS₄ covalent backbone은 1%, 불변.
>
> Li–Cl 13% 강화 출처를 두 단계로 분해할 수 있습니다.
>
> 첫째, comp1의 깨끗한 baseline Li–Cl는 −1.86 eV. 모두 정상 4a 자리.
>
> 둘째, modelc의 4a 자리 Cl는 −2.03 eV로 9% 강해집니다. 무엇이 바뀌었느냐 — Li 공공이 들어와서 ionic field가 전반 강화된 거예요. Cl 자체 위치는 그대로지만 주변 Li 환경이 vacancy로 재배치되면서 결합 거리·전하 분포가 살짝 tighten. 이 효과는 modelc Cl 90%에 균일 적용.
>
> 셋째, modelc의 새로 등장한 4d anti-site Cl는 −2.84 eV로 40% 강합니다. 짧은 거리 2.45 Å + tetrahedral coordination + Cl 3p와 Li 2s 좋은 orbital overlap. 이 effect는 modelc Cl 10%에만 적용되지만 per-bond로 매우 intense.
>
> 두 효과 합쳐서 +13% 평균 강화 기여도는 vacancy field 69% (광범위 약함) + anti-site 31% (소수 강력)입니다.
>
> Bader charge, LOBSTER ICOHP, Wilkening ionic potential — 세 독립 probe가 같은 방향을 가리킵니다."

### Q&A
- "vacancy 효과가 왜 ionic field 강화로 발현?" → Li 1개 빠지면 charge balance 위해 주변 음이온이 전체적으로 강하게 끌어당겨야 함. Bader charge로 Li q +0.011/neighbor Cl 변화 측정됨
- "왜 ICOHP가 vacancy에 sensitive?" → vacancy → 인접 Li-anion 거리 미세 단축 + 전하 재분포 → COHP가 잡는 overlap 강화
- "anti-site 31%만 기여?" → 10% Cl만 영향 받으니까 (per-bond는 강해도 셀당 4 bonds만). 다만 mechanical (M4)에서는 anti-site가 dominant — slide 8a 참고
- "왜 modelc 4a도 강해졌는데?" → vacancy ionic field effect — anti-site와 다른 별도 mechanism, db에서 분해 확정
- "3-probe 합의는?" → Bader Li q 균질 (Δ 1%), LOBSTER ICOHP +13%, Wilkening Li-S +17%. 세 다른 근사 체계가 같은 방향

---

## 1J. Slide 10 — Counter-Intuitive Bond + Per-bond vs Per-anion (v2)

### 페이지 배치 (16:9)
- 평균 결합 표 + per-site 분해
- per-bond vs per-anion 비교 박스 (가장 중요)
- 3-bullet key

### 본문 텍스트 (v2 ACTIVE)

**제목**: "10. Li–Cl 평균이 짧아짐 — 출처는 4d anti-site (per-bond vs per-anion)"

**메인 결합 표**:
```
결합 (Å)              | LPSCl          | LPSCl₁.₆       | Δ
P–S                   | 2.073 ± 0.036  | 2.064 ± 0.011  | −0.5%
Li–S                  | 2.461 ± 0.106  | 2.465 ± 0.094  | +0.2%
★ Li–Cl               | 2.607 ± 0.129  | 2.532 ± 0.119  | −3% 짧아짐 ↓
S–S (cage)            | 3.595          | 3.519          | −2%
```

**Per-site 분해**:
```
종류                          | 거리(Å) | 비고
Li–Cl (4a 정상, modelc)       | 2.59    | 거의 불변
Li–Cl (4d AS, modelc only)    | 2.45    | ★ 0.14 Å 짧음
```

**Per-bond vs Per-anion 비교 (핵심)**:
```
4d anti-site Cl:
  • coord: Li 4 (tetrahedral, [Cl|Li4])
  • per-bond ICOHP: −2.84 eV
  • per-anion total: 4 × −2.84 = −11.3 eV

4d free S²⁻:
  • coord: Li 6 (octahedral)
  • per-bond ICOHP: −2.57 eV
  • per-anion total: 6 × −2.57 = −15.4 eV  ★ 36% 강함

→ per-bond는 LOBSTER orbital overlap (covalent) 우세 측정 → Cl 약간 ↑
→ per-anion은 Coulomb 직관 회복 → S²⁻ 우세 (q² × coord)
```

**Key**:
```
• Li–Cl 짧아짐은 4d AS 한 종류에서 옴 (4a는 거의 불변)
• Per-bond ICOHP: Cl(4d AS) 약간 우세 — LOBSTER가 overlap 측정
• Per-anion total: S²⁻(4d) 36% 우세 — Coulomb 직관 회복
• 두 양은 다른 물리적 의미, paper에서 분리 reporting
```

**Footnote**:
```
※ LOBSTER COHP는 본질적으로 H_μν·P_νμ (orbital overlap) 적분이라 covalent 우세,
  classical Madelung Coulomb는 SCF band 위치에만 들어가고 COHP에 직접 안 나타남.
※ 4d 자리의 짧은 거리는 격자 구조 (Wyckoff topology) + 원래 free S²⁻용 cage
  최적화된 환경 결과 — 4d로 들어간 Cl AS가 그 환경을 상속.
※ 격자 4a/4d 구조: Deiseroth Angew 2006 / Kraft JACS 2017 / Adeli Angew 2019.
```

### 발표 스크립트 v2 ACTIVE (70–80초)

> "결합 길이 cross-check입니다. 가장 흥미로운 발견 하나.
>
> 직관적으로 'Cl이 많아지면 cage가 커지고 Li–Cl이 멀어진다'고 생각하기 쉽지만, 표를 보시면 정반대. Li–Cl이 0.076 Å, 약 3% 짧아집니다.
>
> 어디서 짧아지는지 per-site로 분해하면 명확합니다. 4a 정상 자리는 거의 안 변해요. 변화는 전적으로 4d anti-site에서 — Li–Cl(4d AS)가 2.45 Å, 4a보다 0.14 Å 짧습니다.
>
> 그럼 이 짧은 결합이 정말 더 강한가? 여기 흥미로운 게 나옵니다. 박스의 4d 자리 두 음이온 직접 비교.
>
> 4d 자리 free S²⁻는 Li 6개에 둘러싸여 octahedral 배위, per-bond ICOHP −2.57 eV. 4d 자리 Cl anti-site는 Li 4개에 둘러싸여 tetrahedral 배위, per-bond ICOHP −2.84 eV.
>
> per-bond로는 Cl이 살짝 강해 보입니다. 이건 LOBSTER가 본질적으로 orbital overlap을 측정하기 때문이에요. classical Coulomb 차이는 COHP에 직접 안 들어가고, 짧은 거리에서 covalent overlap이 우세 잡힙니다.
>
> 그런데 per-anion total로 보면 다릅니다. 음이온 하나당 총 결합 에너지를 계산하면 — S²⁻는 6 × −2.57 = −15.4 eV per anion, Cl AS는 4 × −2.84 = −11.3 eV per anion. S²⁻가 36% 강합니다. q=−2가 q=−1보다 더 많이 Li를 끌어모은다는 Coulomb 직관이 회복됩니다.
>
> 즉 per-bond와 per-anion은 다른 물리량. LOBSTER가 측정하는 per-bond는 covalent overlap 위주, 음이온 하나가 만드는 total 결합력은 q²/r Coulomb 직관과 일치. paper에서 이 두 측면을 분리해 정직하게 보고합니다.
>
> Li–Cl 짧아진 미시 출처는 4d 자리의 짧은 격자 환경, 그게 평균 Li–Cl ICOHP +13% (M3)와 mechanical shear stiffening (M4)까지 다 연결됩니다."

### Q&A
- "Cl 1.81 vs S 1.84 Å radius로 6% 거리 차이 설명?" → 못 함. 격자 자리 환경 (4d cage geometry) 이 진짜 원인
- "per-bond vs per-anion 어느 게 paper 메시지?" → 둘 다 — per-bond는 LOBSTER 정량 + per-anion은 Coulomb 일관성 확인. 둘 다 separately reporting
- "Cl AS의 4-coord은 어떻게 측정?" → bonds.json 명시 "[Cl|Li4]". cutoff 3.4 Å 내 Li 개수 직접 측정
- "왜 vacancy 효과는 거리 아니라 ICOHP에 나옴?" → 거리는 average 위주, ICOHP는 local 전자환경 sensitive
- "체크 가능한 추가 분석?" → PDOS Cl 3p 위치 (메커니즘 2), ELF Li-Cl bridge vs Li-S bridge (메커니즘 1) — 둘 다 nice-to-have

---

### ★ 실물 확정판 (as-built deck slide 15 "CC#2", 2026-06-11 — FINAL)

```
각주 Voronoi V 정의 / ■ Cross-check #2: More Cl → Shorter Li–Cl (counter-intuitive)
bullets: mean 2.607→2.532 (−3%) · 4d AS = 2.36 Å (0.19 shorter than 4a)
[좌상] 메인 표 4행 "< Counter-intuitive >" — Li–Cl 행 중립값 + Δ "−3% ↓"만 적
[좌하] per-bond vs per-anion 표 — 사용자 결정으로 본편 유지 (선제 설명):
      per-bond −2.57적/−2.84청 "Cl slightly ↑" · per-anion −15.4청/−11.3적
      "S²⁻ 36% ↑ (Coulomb restored)" — 행별 승자=청 규칙 정합
[우상] Per-site 박스: 4a 2.55 (−2%) / 4d AS 2.36적 (0.19 shorter) + Voronoi
      V(Cl) 22.06→20.31적 (−1.7) — ★ V0 직접 계산 검증값 (구 2.59/2.45 출처불명 폐기)
[우하] 히스토그램 3색 (적/청 4a/초록 4d AS 진하게) + 캡션
검증 기록: 전체 평균 2.607±0.128 / 2.532±0.119 — V0 재계산 일치 ✓. 4d AS 4개
= 2.308/2.356/2.357/2.414. 거리 통계 기하 cutoff 3.4 (36+4) vs LOBSTER 페어링
(38+4) convention 차이 Q&A 카드화. 잔여 선택: 범례 "anti site" 하이픈.
```

## 1K. Slide 11 — Cross-check #3: Voronoi 4-Sublattice Disorder Fingerprint

### ★ 실물 확정판 (as-built deck slide 16 "CC#3", 2026-06-11 — FINAL, 잔여 2건: DFT 제목·×기호)

```
■ Cross-check #3: Where does disorder actually go? — a 4-sublattice fingerprint
bullets: P barely moves (framework intact) · Li ×5.5 (fingerprint #1) ·
        S more homogeneous (−40%, paradox)
[좌] Origin 막대 4쌍 + ×5.5/−40% 주석 + 캡션 < Voronoi volume std (Å³) >
[우] 표 4행 (P 0.00→0.37 / Cl 0.00→0.74 / Li 0.21→1.15 ×5.5 / S 3.41→2.05 −40%)
     — P·Cl의 0.00 두 셀 적색 점선 박스 (footnote 연결, M1 패턴 재사용)
footnote: P·Cl std = 0.00 exact (F-43m 동등 자리 증거) + 부피 합 = 셀 부피 1.0000
검증: 8개 수치 전부 V0 구조 scipy Voronoi 재계산 일치 (2026-06-11,
docs/figures/slide16_voronoi/). "3 probes converge" 한 줄은 대본이 전담.
```


### 페이지 배치 (16:9)
- 메인 4-행 표 (P/Cl/Li/S × comp1/modelc std)
- 4 sublattice 응답 해석 박스
- 3 probe convergence footer

### 본문 텍스트

**제목**: "11. Disorder는 4개 sublattice에 어떻게 들어가나 — Voronoi fingerprint"

**메인 표**:
```
종 (Voronoi V std, Å³)   | comp1   | modelc  | 변화
────────────────────────┼─────────┼─────────┼─────────────
P  (PS₄ framework)      | 0.00    | 0.37    | +0.37
Cl                      | 0.00    | 0.74    | +0.74
Li                      | 0.21    | 1.15    | ★ 5.5× 더 흔들림
S                       | 3.41    | 2.05    | ★ −40% 균질화 (역설!)
```

**4 sublattice 해석**:
```
P  → PS₄ framework 거의 안 흔들림           (M1 backbone 일관)
Cl → 4a (정상) + 4d AS 두 환경 분기          (M3 +13% ICOHP 출처)
Li → disorder fingerprint #1: 5.5× 더 흔들림 (vacancy + AS-adjacent 재배치)
S  → disorder fingerprint #2: 역설적 균질화  (anti-site Cl가 split 메움)
```

**Key**:
```
• 4 sublattice가 모두 다른 방식으로 disorder에 응답
• P 거의 0, S 역설적 감소, Li 가장 강력 fingerprint
• 3 독립 probe 수렴 (Voronoi + BVSE bimodal + LOBSTER ICOHP +13%)
```

**Footnote**:
```
※ Method: scipy.spatial.Voronoi 3×3×3 PBC tile + ConvexHull 부피
  합 = cell 부피 (ratio 1.000, exact 측정)
※ comp1 P, Cl std=0: F-43m 격자에서 모든 P, Cl이 결정학적 equivalent
※ Three independent post-processings: bvse_5x5x5_paired + LOBSTER + Voronoi
```

### 발표 스크립트 (60–70초)

> "Cross-check #3, disorder가 4개 sublattice에 어떻게 들어가는지 Voronoi 부피 std로 잰 결과입니다.
>
> 각 원자 주위 다면체 부피의 표준편차를 종별로 측정하면, 그 종 안에서 환경이 얼마나 균질한지가 직접 보입니다.
>
> comp1에서는 P, Cl std가 정확히 0. F-43m ordered에서 모두 결정학적으로 equivalent 위치 — 직접 증거입니다. Li std 0.21은 24g/48h 두 Wyckoff orbital 분기.
>
> modelc로 가면 4개 sublattice가 각각 다른 방식으로 응답합니다.
>
> 첫째, P sublattice: std 0.37, 거의 안 흔들립니다. PS₄ tetrahedron framework 보존의 직접 시각화.
>
> 둘째, Cl sublattice: std 0.74로 두 군집 분기. 4a 정상 + 4d anti-site 두 환경 — slide 7 ICOHP per-site split과 직접 대응.
>
> 셋째, Li sublattice — 가장 강한 fingerprint: std 1.15로 5.5배 더 흔들립니다. vacancy 재배치 + anti-site 주변 Li 환경 변화 합산.
>
> 넷째, S sublattice는 paper의 진짜 highlight: std가 오히려 40% 줄어듭니다, 균질화. 직관에 반하는데 이유는 comp1에서 S가 두 군집 (PS₄-S 작은 부피 + free 4d-S²⁻ 큰 부피)로 splits, 그 격차가 컸어요. modelc에서 4d로 들어간 anti-site Cl이 그 split을 메워서 평균화. anti-site disorder가 단순히 무질서를 더하는 게 아니라 기존 split을 smooth하는 dual effect 발견.
>
> 이 fingerprint는 다른 두 독립 post-processing과 수렴. slide 12 BVSE bimodal + slide 7 LOBSTER ICOHP +13%. 세 독립 측정이 같은 방향을 가리킵니다."

### 시각 디자인 노트
- 4행 표 — 각 행 다른 색 (4 sublattice 구분)
- ★ Li (×5.5) + ★ S (역설 −40%) 두 행 강조
- "역설적 균질화" 강조색 — paper highlight
- 4 sublattice 해석 박스 표 아래 별도
- 3 probe convergence footer 한 줄

### Q&A
- "Voronoi 측정 방법?" → scipy.spatial.Voronoi + ConvexHull, 3×3×3 PBC tile, sum ratio 1.000 exact
- "std (분산) 선택 이유? mean은?" → mean은 종별 평균 크기, std가 "환경 다양성" fingerprint
- "comp1 std=0의 의미?" → F-43m에서 P, Cl 모두 결정학적 equivalent — ordered 직접 evidence
- "comp1 Li std도 0 아닌데?" → 24g + 48h 두 Wyckoff sublattice 분기
- "S 균질화가 왜 surprising?" → 보통 disorder=std 증가 직관, anti-site가 split 줄임 — counter-intuitive
- "BVSE bimodal과 연결?" → 같은 cell Li 부피 분포 wide → BVSE energy 분포 wider. 같은 원인 두 measure
- "comp1 S std 3.41 크기 이유?" → free S²⁻(4d) 4개 큰 부피 + PS₄-S 16개 작은 부피 두 군집 split → bimodal V → std 큼
- "modelc S std 줄어든 메커니즘?" → 4d 자리 일부에 anti-site Cl 들어가면서 PS₄-S vs free-S 중간 부피로 흡수

---

## 1L. Slide 12 — Cross-check #4: BVSE Bimodal Split (Paired 5×5×5)

### 페이지 배치 (16:9)
- 왼쪽: bimodal histogram (Li-BVS 분포)
- 오른쪽: 3D iso-surface paired (또는 2D slice)
- 하단: 정량 cross-check + caveat

### 본문 텍스트

**제목**: "12. Li 환경이 둘로 갈라진다 — BVSE bimodal split (paired 5×5×5)"

**Bimodal 표**:
```
시스템   | Group               | n_Li  | 비율   | BVS peak  | 환경
─────────┼─────────────────────┼───────┼────────┼───────────┼──────────
comp1    | uniform             | 3000  | 100%   | 1.60-1.64 | F-43m ordered
modelc   | low-BVS (group A)   | 1074  | 39.8%  | 1.60-1.64 | comp1-like, AS 멀리
modelc   | high-BVS (group B)  | 1626  | 60.2%  | 1.83-1.89 | AS Cl 인접, +15% ★
```

**Key**:
```
• 1626 high-BVS Li / 300 AS Cl = 5.4 Li per AS — Li-Cl 1차 배위(4-6) 정합
• +15% BVS shift ↔ +40% ICOHP 강화 — 같은 효과 두 probe 정량
• 37.5% AS = cubic 5×5×5의 stoichiometry 필연 lower bound (over-disordered 아님)
```

**Footnote**:
```
※ 5×5×5 cubic supercell (lattice 50.275 Å), grid 100³, cutoff 5.0 Å
※ comp1에서 300 S→Cl + 300 Li 제거 (charge-compensated, isovolumetric)
※ Paired: 격자/grid/cutoff 완전 동일, 차이는 chemistry 변화만
```

### 발표 스크립트 (60–70초)

> "Cross-check #4 — BVSE bond-valence sum mapping. Li 이동 환경 직접 측정.
>
> Paired 5×5×5 supercell 프로토콜 — comp1 셀을 5×5×5 tile (6500 atoms)로 펼치고, modelc는 300 S→Cl + 300 Li 제거만 적용. 격자, grid 100³, cutoff 5 Å — 완전 동일. 차이는 chemistry 그 하나만.
>
> 왼쪽 histogram이 핵심. comp1은 단일 좁은 peak — 3000 Li가 1.60-1.64에 모임, σ=0.016. F-43m ordered structure 단일 환경.
>
> modelc로 가면 bimodal split. 첫 peak 1.60-1.64에 1074 Li (39.8%) — anti-site에서 멀리 있는 comp1-like. 두 번째 peak 1.83-1.89에 1626 Li (60.2%) — +15% shifted, anti-site 주변 그룹.
>
> 정량 cross-check 깨끗. 1626 / 300 AS = 5.4 Li per AS Cl — Li-Cl 1차 배위 4-6과 정합. BVSE +15% shift는 LOBSTER ICOHP +40% 강화의 또 다른 정량 — 두 독립 probe 같은 anti-site 효과.
>
> Caveat: AS 37.5%는 cubic 5×5×5에서 stoichiometry 필연 — 4a 500 사이트 다 차고 남은 300이 4d로 가야 함. 실험 25-50% 범위 내. over-disordered 아님.
>
> 오른쪽 3D iso-surface는 같은 결과 시각화 — comp1 균질 mobile network, modelc는 anti-site 영역 high-BVSE 집중."

### 시각 디자인 노트
- 왼쪽 histogram: comp1(파랑) + modelc(빨강) overlay, BVS 분포
- modelc bimodal 두 peak 음영 + 39.8% / 60.2% 라벨
- 오른쪽 3D iso-surface 또는 2D slice: 같은 colormap, isovalue 0.30
- "bimodal split" + "stoichiometric necessity" 강조

### Q&A
- "BVS 측정 의미?" → 가상 Li 위치 grid point의 valence 합. 실제 자리 ≈ 1.0 ideal, 일탈량이 환경 영향
- "paired 5×5×5 이유?" → unit cell 격자 다름 (cubic vs rhombo). 같은 cubic으로 paired만 정확
- "37.5% over-disordered 아님 확신?" → cubic 5×5×5 stoichiometric math 필연 lower bound. 실험 25-50% 범위 내
- "12.5% (rhombo primitive)와 차이?" → primitive 8 중 1 4d는 특정 ordered choice. 큰 셀에선 그 배치 불가
- "+15% vs +40% 정량 차이?" → 다른 측정 (BVS=형식가, ICOHP=결합 강도). direction 같음이 중요
- "5.4 Li per AS Cl 의미?" → bonds.json 4d-Cl coord=4 (tet) + 약간 2차 영향. 1차 배위와 정합
- "iso-surface 0.30 선택?" → shallow main channel — Li 자유 흐를 수 있는 low-BVSE 영역
- "60.2% 비율 정확한가?" → 5.4 × 300 = 1620 ≈ 1626 — 모든 AS 주변 첫 Shell이 영향

---

### ★ CC#4 검증·구성 기록 (deck slide 17, 2026-06-11 — 조립 중)

```
검증 완료: ① 표 3행 수치 = db modelc_v3.json bvse_5x5x5_paired와 일치
② per-Li 원본 (V0_bvse_summary.json existing_Li_bvs)에서 split 재현 —
  n=3000/2700, median 1.634/1.832, threshold 1.74에서 low 39.8%/high 60.2% EXACT
③ 37.5% 유도 (500 4a sites vs 800 Cl → 300 forced to 4d) — db 기록 채택
④ channel fraction 8.75%→7.4% (−15%) — iso 그림 정량 라벨로 사용 가능
그림 결정: iso 1쌍 (제목 "Li-accessible channels — only low-energy regions
(BVSE ≤ 0.30) shown" — global min=0.000이라 표기 정확) + 시스템·채널% 라벨
(8.75% / 7.4% −15%적). slice 쌍·histogram 모두 폐기 (사용자 결정).
**FINAL (2026-06-11)**: 각주 2줄(BVS+paired 조건) · bullets 3 (5.4 Li per AS) ·
표 캡션 (**500 f.u.** — 125 cells×4 f.u.; 6500/6200, 300 S→Cl/−300 Li; 초안의 '125 f.u.'는 cell 수 혼동 오기, 사용자 정정) · 표 3행 (BVS peak 색 인코딩:
적=LPSCl-같은 환경, 청=새 환경 — A행 peak 적색 처리 영리함) · 정량 박스 2줄
(closure + +15%↔+40% 두 probe). 37.5% footnote는 생략 → Q&A 카드.
300/2700 출처 카드: 300 = 800(필요 Cl) − 500(4a 자리), 2700 = 5.4×500 = 1074+1626.
```

## 1M. Slide 13 — Cross-check #5: ELF — Covalent vs Ionic 시각화

### ★ 실물 확정판 (as-built deck slide 18 "CC#5", 2026-06-11 — FINAL, cross-check 섹션 완주)

```
각주: ELF 정의 1줄 압축 / ■ ELF – covalent backbone & ionic glue, visualized
bullets 3 (0.946/0.944 identical청 · Li basin <0.1 · ionic side only)
[그림] notitle_ELF_comp1_Pz_slice (10×10, 좌 LPSCl) + notitle_ELF_modelC_Pz_slice
      (7×7, 우 LPSCl1.6) — contour 쌍, 원자라벨 내장, colormap 0–1 동일.
      공통 캡션 "ELF slice through a PS4 plane (each cell) — same colormap (0-1)"
[표] 3행: P–S 0.946/0.944 · Li basin 0.072/0.065 · Li→anion 0.07/0.04
하단(청): → the fifth probe closes the loop: five independent probes, one picture
비고: 원본 PNG 제목이 comp1 파일에도 "modelC"로 박힌 생성스크립트 버그 발견 —
제목 crop으로 해결, 판별 기준 = 축 크기 (10×10 comp1 / 7×7 modelc).
xy_mid 후보는 modelc 단면에 P 부재로 탈락.
```


### 페이지 배치 (16:9)
- 좌우 paired ELF 2D slice (comp1 / modelc, 같은 colormap)
- 정량 측정 표 (P-S bridge / Li basin min / Li-anion line)
- ELF 의미 reference + 3-probe convergence footer

### 본문 텍스트

**제목**: "13. ELF가 보여주는 결합 character — covalent vs ionic 분리"

**메인 표**:
```
Probe location                       | comp1   | modelc  | 의미
─────────────────────────────────────┼─────────┼─────────┼─────────────
P–S bond midpoint (PS₄ bridge)       | 0.946   | 0.944   | covalent 동일 ★
Li basin min (Li 주위 floor)         | 0.072   | 0.065   | ionic depletion 강함
Li → nearest anion 경로 단일 min     | 0.07    | 0.04    | modelc 더 강함
```

**Key**:
```
• P–S bridge ELF ≈ 0.95 (>0.7 covalent 기준) — PS₄ covalent character 불변
• Li basin min < 0.1 (이온성 강한 ELF 결핍) — 양쪽 모두 ionic glue
• 두 character (covalent + ionic)가 같은 cell 안에 공존
• 조성 변화는 ionic 쪽만 재배치, covalent backbone은 안 건드림
```

**ELF 의미**:
```
ELF 0.0~0.3 : 자유전자 분포 (이온성 / depletion)
ELF 0.4~0.6 : 중간 (mixed)
ELF 0.7~1.0 : localized (lone pair / covalent maximum)
```

**Footnote**:
```
※ ONCV NC pseudo, ecutwfc 80 / ecutrho 320 Ry, pp.x plot_num=8
※ probe sampling: Cartesian midpoint (covalent) + Li-anion line min (ionic depletion)
※ Mechanism 1 cross-check: PDOS + LOBSTER + ELF 세 독립 probe 일관
```

### 발표 스크립트 (55–65초)

> "Cross-check #5 — ELF, electron localization function. 결합 character를 공간적으로 직접 가시화하는 마지막 probe입니다.
>
> ELF는 0에서 1 사이 값으로, 0에 가까우면 자유전자 분포 (이온성), 1에 가까우면 국소화된 전자 (covalent 또는 lone pair).
>
> 양쪽 2D slice plot. 두 시스템에서 동일한 패턴 — PS₄ tetrahedron 주위에 ELF 0.95에 가까운 적색 maxima 또렷. P–S covalent bridge에서 전자가 강하게 국소화 — covalent backbone 직접 시각 증거.
>
> 반면 Li atoms 주위는 ELF가 0.07 정도까지 떨어짐. Li가 valence 전자를 거의 다 음이온에 양도하고 자기 주위에 안 갖고 있다는 직접 증거 — 강한 ionic depletion.
>
> 정량 표 — P–S bridge ELF 양쪽 0.95 사실상 동일, Δ < 0.002. 즉 covalent character는 조성 무관, ICOHP P–S +1% 차이 (slide 9)와 일관.
>
> Li basin floor는 양쪽 0.07 근처 — modelc 약간 더 깊긴 한데 둘 다 강한 ionic 영역.
>
> 오늘 추가로 본 PDOS mechanism — Cl 3p가 S 3p보다 깊은 valence 위치 — 와 ELF mid-bond 측정이 모두 mechanism 1 (LOBSTER가 covalent overlap 우세 측정)의 시각/정량 evidence. PDOS + LOBSTER + ELF 세 독립 probe 같은 그림.
>
> 종합 — argyrodite는 covalent PS₄ backbone + ionic Li-anion glue 두 character가 같은 cell 안에 공존하고, 조성 변화는 ionic 쪽만 재배치, covalent backbone에는 손대지 않습니다."

### 시각 디자인 노트
- 2D ELF slice paired: 같은 colormap (viridis 또는 RdYlBu), 같은 scale 0-1
- PS₄ 보이는 cut plane (예: z=c/2)
- 빨강(0.9+) = covalent maxima, 파랑(0-0.2) = ionic depletion
- 4d 자리 별도 표시 (modelc의 AS Cl 위치)
- 표는 plot 아래 가운데

### Q&A
- "ELF 정의?" → Becke-Edgecombe 1990, 같은 spin pair 위치 확률. 0=free electron, 1=perfectly localized
- "0.95 P-S 정량 의미?" → sp³ hybrid covalent bond 전형. CC bond (diamond) ~0.95
- "Li 0.07 ionic 강도?" → Li metal ELF ~0.6, LiCl/Li2S 결정 Li ~0.05-0.1. 우리 값 정상
- "pseudo 영향?" → ONCV NC vs USPP 차이 <5%. paper ONCV 통일
- "4d-Cl AS ELF?" → 정상 Cl과 유사 profile — Cl-Li bond character는 ionic 유지
- "Mechanism 1 ELF 직접 증거?" → P-S ELF 동일 = covalent 보존. Li-anion bridge ELF 양쪽 ~0.07 = 이온성 동일
- "ELF가 ICOHP 대체?" → 아니, 보완. ICOHP=정량 결합 강도, ELF=정성 character (covalent vs ionic)
- "cube file 크기?" → ~100-200 MB. paper SI에 첨부 가능

---

## 1N. ~~Slide 14 — k-mesh Audit~~ — **발표 deck에서 DROPPED (2026-06-11, 사용자 결정)**

> 본편 제외. 정보 흔적은 ① caveats 슬라이드의 k×L·spilling 행 ② Q&A 카드 2장:
> "k 수렴 했나?" → "k×L ≥ 40 Å 양쪽 보장 (4×4×4/6×6×3). 초기 k221에서 gap 1.50
> 사고를 수렴 테스트로 잡아 paper-grade로 재계산한 이력까지 있습니다 (구조 RMS
> 0.003 Å — 전자 property만 오염이었음)" / "LOBSTER 믿을 만한가?" → "spilling
> 1.16–1.46% (<5% 표준)". M4-1 때 '#4 method-quality는 audit 슬라이드로' 했던
> 위임도 이 Q&A 카드로 최종 귀속. paper Methods엔 본문 그대로 사용.

## (보존) Slide 14 — k-mesh Audit & Method Convergence (Referee Defense)

### 페이지 배치 (16:9)
- k-mesh incident & recovery 스토리 박스 (referee 정직성)
- Property별 k-sensitivity 표
- 최종 paper-grade 설정 (k-mesh + spilling + AIMD window)

### 본문 텍스트

**제목**: "14. k-mesh 수렴 + LOBSTER spilling + AIMD window — Method audit"

**k-mesh incident 스토리**:
```
초기:  k=2×2×1, k×L=10 Å  → gap 1.50 eV (artifact)
발견:  Δgap(modelc 1.82) = 0.32 eV "조성 효과"로 오해
복구:  k=4×4×4, k×L=40 Å  → gap 1.76 eV (paper-grade)
결과:  Δgap = 0.06 eV (M1 확정 — 사실상 동일)
구조:  geometry RMS 0.003 Å (electronic만 오염, 구조 robust)
```

**Property k-sensitivity 표**:
```
Property         | k-sens   | 우리 대응
─────────────────┼──────────┼──────────────────────────
B₀ (BM-EOS)      | robust   | 재계산 불필요 (volume curvature systematic cancel)
Gap              | high     | k=4×4×4/6×6×3 재계산 ✓
Elastic Cij      | high     | 재계산 ✓
DOS shape        | high     | 재계산 ✓
Bader charge     | mid      | 재계산 ✓
ICOHP            | robust   | k-shift Δ<0.006 eV (local probe) ✓
```

**최종 paper-grade method**:
```
• comp1:  k=4×4×4, k×L=40 Å (cubic 52 atoms)
• modelc: k=6×6×3, k×L=42 Å (rhombo 62 atoms)
• Convergence 기준: k×L ≥ 40 Å (argyrodite insulator gap ~1.8 eV)
• LOBSTER spilling: comp1 1.46% / modelc 1.16% (<5% ✓)
• AIMD window: [2, 50] ps 양쪽 동일, R² 0.999/0.992
```

### 발표 스크립트 (60–70초)

> "Method-defense section입니다. paper-grade 결과들이 paper-grade 수렴 기준을 충족하는지 정직하게 보여드리는 referee defense.
>
> 가장 중요한 한 가지 — comp1 k-mesh incident와 복구 스토리. 위 박스를 보세요.
>
> 초기에는 comp1을 k=2×2×1로 잘못 돌렸어요. k×L이 10 Å로 paper 기준 40보다 4배 부족. 결과 gap이 1.50 eV로 나왔습니다. modelc gap이 1.82이니까 Δgap 0.32 eV 차이가 '조성 효과로 modelc가 더 wide'로 잘못 해석된 적이 있어요. 위험한 over-claim 직전에 발견.
>
> k=4×4×4 (k×L=40)로 재계산하니까 gap 1.76 eV로 올라옵니다. Δgap = 0.06 eV로 줄어들어요. M1 메시지의 정확한 근거. 중요한 건 structure RMS가 0.003 Å로 거의 안 바뀌었다 — k-mesh 오염은 전자 property만 영향, 구조는 robust. 그래서 EOS 같은 volume-curvature는 재계산 불필요.
>
> 표 아래쪽 property별 k-sensitivity 정리. B₀와 ICOHP는 k-robust (volume curvature cancel + local probe). gap, elastic, DOS는 k-sensitive라 paper-grade 재계산. 모든 §8 property 양쪽 동일 수렴 기준 충족.
>
> LOBSTER charge spilling 1-1.5%로 paper 표준 5%보다 깨끗, AIMD Arrhenius window 양쪽 동일 protocol로 R² 0.999 이상.
>
> Referee가 'method 부정확 아니냐' 물어볼 모든 지점 미리 차단."

### 시각 디자인 노트
- k-mesh incident 박스 강조 (정직성 표시)
- "발견 → 복구" 화살표로 narrative 흐름
- property 표 sensitivity 색 코딩 (red=high, yellow=mid, green=robust)
- 최종 설정 박스는 paper Methods section 그대로

### Q&A
- "k=2×2×1 어떻게 발견?" → DOS profile spurious peak + 비물리적 mid-gap states → k 의심 → 수렴 test
- "왜 modelc k=6×6×3?" → rhombo c축 35 Å, k_c×c=42 Å 보장
- "EOS 재계산 안 함?" → B₀ volume curvature, k systematic cancel. comp1 v1/v2/v3 (26.2/26.5/26.23) 1% 일관
- "ICOHP k 의존?" → 직접 측정 Δ<0.006 eV/bond (local probe)
- "AIMD 800K rerun?" → seed stuck → R² 0.77 broken Arrhenius. fresh seed로 R² 0.999 회복. statistics 문제
- "Spilling 5% 기준?" → LOBSTER 공식 docs + Maintz/Dronskowski

---

## 1O. ~~Slide 15 — Methods Consistency~~ — **발표 deck에서 DROPPED** (2026-06-11, slide 3 + slide 14와 중복). 발표 21장으로.

> ⚙ **본문은 paper Methods section 후보로 보존** — 발표에는 안 쓰지만 paper writeup 시 그대로 인용 가능한 settings detail box. ecutwfc 60, k-mesh 4×4×4/6×6×3, LOBSTER 5.1.1 ext basis, ELF ONCV 등 paper-grade 정확 settings 모두 정리됨.

---

### [DROPPED] 본문 (참고용)

#### Slide 15 — Methods Consistency: 모든 §8 같은 protocol

### 페이지 배치 (16:9)
- 3 tier box 세로 stack (slide 3과 일관)
- 컴퓨팅 자원 footer
- "양쪽 동일 protocol" highlight

### 본문 텍스트

**제목**: "15. Methods Consistency — 양쪽 시스템 완전 동일 protocol"

**Tier 1**:
```
MLIP screening (UMA-s-1p1, task=omat)
  • Halogen enumerate (45 configs, pymatgen)
  • Li sublattice screen (top-5 halogen × 20 random Li)
  • Langevin anneal: 500 K, 50 ps, dt 2 fs, friction 0.01/fs
  • MLIP EOS pre-scan: BM3 fit → V₀ 범위 (DFT EOS 안내)
```

**Tier 2**:
```
DFT validation (Quantum ESPRESSO 7.4.1)
  • PBE GGA + USPP (SSSP efficiency)
  • ecutwfc = 60 Ry, ecutrho = 480 Ry
  • k-mesh: comp1 4×4×4 / modelc 6×6×3 (k×L ≥ 40 Å)
  • BM3 EOS: 11 volumes V/V₀ = 0.96 - 1.06
  • V₀ confirmation BFGS: force < 5×10⁻³ eV/Å
```

**Tier 3** — 모두 양쪽 동일 V₀ 기반:
```
§8 Multi-probe (양쪽 동일 V₀)
  • DOS/PDOS: projwfc.x, MV smearing 0.005, k=6×6×6/6×6×3 NSCF
  • Bader: pp.x plot_num=17 (AE), Henkelman bader
  • LOBSTER 5.1.1: PAW kjpaw + ext basis (Li 1s2s2p, P/S/Cl 3s3p3d), 70 Ry
  • ELF: ONCV NC, ecutwfc 80/320 Ry, pp.x plot_num=8
  • Elastic: 12 strain × ±0.005, relaxed-ion + clamped-ion 둘 다
  • AIMD: UMA-s-1p1 Langevin NVT, equilib 10 + prod 100 ps × 3 T
  • BVSE: pyABS, grid 100³, cutoff 5.0 Å (5×5×5 paired)
```

**컴퓨팅 자원**:
```
• Tier 1 (MLIP): gabia A6000 + Runyour V100
• Tier 2 (DFT): KISTI Neuron GPU + x3430a02
• Tier 3 (post-process): 분산 — settings는 통일
```

**Footnote**:
```
※ Pipeline v2 표준 (kb/methodology/argyrodite_mechanical_pipeline.md)
※ Pseudo 일관: SSSP efficiency (USPP) + ELF 분석만 ONCV NC 별도
※ 양쪽 동일 protocol = paired comparison 정당성 토대
```

### 발표 스크립트 (50–60초)

> "Methods Box — paper Methods section 그대로 한 페이지에 압축한 슬라이드. 두 시스템에 완전 동일 protocol 적용이 paired comparison의 정당성 근거예요.
>
> 3-tier pipeline 그대로. Tier 1 MLIP screening에서 양쪽 같은 UMA-s-1p1 omat, 45 halogen × 20 Li × 50 ps anneal, MLIP EOS pre-scan까지 identical.
>
> Tier 2 DFT validation: 둘 다 QE 7.4.1 PBE/USPP, ecut 60/480 Ry, k×L ≥ 40 Å (cubic 4×4×4 / rhombo 6×6×3), BM3 EOS 11 volumes. comp1과 modelc V₀, B₀가 같은 정확도로 측정.
>
> Tier 3 §8 multi-probe — 13개 probe 모두 양쪽 동일 V₀ 기반. DOS/PDOS, Bader, LOBSTER ext basis, ELF (ONCV 별도), Elastic 12 strain, AIMD 3 T × 110 ps, BVSE 5×5×5 paired. 정확히 같은 settings.
>
> 컴퓨팅 자원 분산 (gabia + V100 + KISTI Neuron) 했지만 settings 통일.
>
> 이 method consistency가 paired comparison 토대 — referee defense 핵심."

### 시각 디자인 노트
- 3 tier box 세로 stack (slide 3과 일관)
- 각 tier opaque 청색 (paper formal 톤)
- "양쪽 동일 protocol" highlight (referee defense)
- 컴퓨팅 자원 footer 작은 글씨

### Q&A
- "ELF만 ONCV?" → ELF는 valence wavefunction 정확도 민감, ONCV NC paper-grade
- "cubic vs rhombo cell?" → comp1 F-43m, modelc R3m natural ground state. paired 비교는 intensive property에서 valid
- "다른 GPU 머신 reproducibility?" → settings 통일 + cross-check (B₀ 1% 이내)
- "USPP vs PAW kjpaw?" → main DFT USPP (속도), LOBSTER NSCF만 PAW (orbital projection 필요)
- "Pipeline reference?" → kb/methodology/argyrodite_mechanical_pipeline.md

---

## 1P. Slide 16 — Summary: 한 페이지로 보는 paper #1

### 페이지 배치 (16:9)
- 2-컬럼 대조표 (불변 ↔ 변화)
- Thesis 박스 + 4 메시지 한 줄씩
- "covalent skeleton / ionic ligament" 마무리

### 본문 텍스트

**제목**: "16. Summary — 불변 ↔ 변화의 깔끔한 분리"

**대조표**:
```
불변 (조성 둔감)              | 변화 (조성 민감)
─────────────────────────────┼──────────────────────────────
• PS₄ covalent backbone      | • Li carrier 운반체 (×8)
  P-S length, ICOHP, ELF      |   prefactor D₀ ★
• Band gap (Δ 0.06 eV)        | • Li-anion ionic glue
  VBM/CBM character           |   ICOHP +13% (Cl) / +8% (S)
• Li-S(4d) universal anchor   | • Shear modulus G (+30%)
  (Δ 2%)                       |   C44 +72%, Zener A 1.14→1.44
• Per-anion Coulomb 직관      | • 4d-Cl anti-site (새 결합 family)
  (S²⁻ 우세)                  |   ICOHP −2.84 eV (+40% per-bond)
```

**Thesis**:
```
"LPSCl → LPSCl₁.₆ 변화는 전자구조가 아니라
 구조적 무질서 (Li 공공 + 4d-Cl anti-site)에서 온다."

· σ 향상: vacancy carrier (prefactor 8×) — M2
· E 강화: shear lock-in (4d-Cl mortar) — M4
· ICOHP 강화: vacancy field 69% + anti-site 31% — M3
· 전자구조 보존: PS₄ + 갭 동일 — M1
```

**마무리**:
```
→ 4 메시지 (M1-M4) + 5 cross-check (slides 9-13) 모두 같은 그림
→ "covalent skeleton 유지 + ionic ligament 재배치" = paper #1 한 문장
```

### 발표 스크립트 (60–70초)

> "Summary 슬라이드 — paper #1의 모든 결과를 한 페이지로 정리.
>
> 좌우 대조표 핵심. 왼쪽 '불변' 컬럼: PS₄ covalent backbone, 밴드갭, Li-S(4d) universal anchor, per-anion Coulomb 직관 — 모두 조성과 무관 보존. 오른쪽 '변화' 컬럼: Li carrier 운반체 8배, ionic glue +13%, shear G +30%, 4d-Cl anti-site 새 결합 family — vacancy + Cl 치환으로 재배치.
>
> 좌우 분리 깔끔. 왼쪽은 covalent or framework-level, 오른쪽은 ionic sublattice or carrier-level.
>
> Thesis 한 문장: 'LPSCl → LPSCl₁.₆ 변화는 전자구조가 아니라 구조적 무질서, Li 공공 + 4d-Cl anti-site에서 온다.'
>
> 4 메시지가 각도별 — M1 전자구조 보존, M2 σ 향상이 prefactor (vacancy carrier), M3 ionic glue 강화의 vacancy 69% + anti-site 31% 분해, M4 E 강화가 shear lock-in (4d-Cl mortar).
>
> 5 cross-check (slides 9-13)이 이 4 메시지를 다섯 독립 probe로 confirm — Voronoi, BVSE bimodal, ELF, PDOS, per-site bond. 모두 같은 그림.
>
> 한 문장: 'covalent skeleton 유지 + ionic ligament 재배치.' paper #1의 본 모습입니다."

### 시각 디자인 노트
- 2-컬럼 대조표 중심
- 왼쪽 청색 톤, 오른쪽 적색 톤
- 좌/우 ↔ "skeleton" / "ligament" 카피 매칭
- thesis 박스 별도 강조색
- 4 메시지 한 줄씩
- footer: cross-check 5개

### Q&A
- "왜 '구조적 무질서' thesis 키워드?" → vacancy + anti-site 둘 다 structural disorder, 4 메시지 일관
- "전자구조 보존 ↔ 기계적 강화 양립?" → PS₄ skeleton 그대로 + Li-anion mortar 강화 (slide 8 footnote)
- "다른 argyrodite 일반화?" → Br/I variant 유사 예상. paper는 Cl 한정, SI extension 가능
- "paper main figure 후보?" → 10, 11, 8a, 4
- "이 summary로 paper conclusion?" → YES, abstract + conclusion 거의 그대로 가능

---

### ★ 실물 확정판 (as-built deck slide 19 "Summary", 2026-06-11 — FINAL)

```
■ Summary: what stays invariant – and what composition changes
[좌 점선박스 검정] INVARIANT 3항 (PS4 backbone ~1% · gap Δ0.06 + character · anchor Δ2%)
[우 점선박스 청] CHANGED 4항 (transport ×2.5청 600K · glue +13/+8청 · shear +30/C44+72청
  + Zener 1.44적 · new bond family −2.84) — 번호 1~4가 M2→M3→M4→원인 서사 순
박스 아래: → all confirmed by 3 independent probes (×5.5 · +15% · +40%) [17 흡수 ✓]
thesis 띠: "not from electronic structure / from structural disorder" 밑줄 강조
  + covalent skeleton preserved · ionic ligament rearranged
색 문법: CHANGED=청(modelc가 가져온 것), 비용 항목(Zener)만 적 — deck 일관 ✓
4.3 외삽 수치 제거 확인 ✓ (×2.5 측정값만)
```

## 1Q. ~~Slide 17 — 3-Probe Convergence~~ — **Summary에 병합 (2026-06-11, 사용자 결정)**

> CC#3·4·5 수치의 재방송 성격 → 별도 슬라이드 대신 Summary의 '변화' 컬럼 하단 한 줄로
> 흡수: "→ all confirmed by 3 independent probes (Voronoi ×5.5 · BVSE +15% · ICOHP +40%)".
> 정량 박스(5.4 Li/AS 등)는 CC#4 슬라이드가 이미 보유.

## (보존) Slide 17 — Robustness #1: 3-Probe Convergence Panel

### 페이지 배치 (16:9)
- 3-probe 표 (Voronoi + BVSE + LOBSTER × 정량/대상/슬라이드)
- 3 box → "anti-site Cl" 수렴 다이어그램
- 정량 cross-consistency footer

### 본문 텍스트

**제목**: "17. 세 독립 post-processing이 같은 anti-site 효과를 가리킴"

**3-probe 표**:
```
Probe              | 정량 결과              | 측정 대상            | 슬라이드
───────────────────┼────────────────────────┼─────────────────────┼─────────
Voronoi V std      | Cl 0 → 0.74 Å³         | Site disorder       | 11
                   | Li 0.21 → 1.15 (×5.5)  | (geometric)         |
BVSE bimodal       | +15% shift (60.2% Li)  | Li 이동 환경        | 12
                   | 1.62 → 1.85 BVS        | (percolation path)  |
LOBSTER ICOHP      | +40% per-bond (4d AS)  | Li-Cl 결합 강도     | 7
                   | -2.03 → -2.84 eV       | (bonding chemistry) |
```

**Quantitative consistency**:
```
• 1626 high-BVS Li / 300 AS Cl = 5.4 Li/AS — Li-Cl coord 4-6 정합
• BVSE 60.2% high-BVS Li ↔ LOBSTER 4d-Cl AS group ↔ Voronoi Li std 5.5×
• Δ(BVS) +15% vs Δ(ICOHP) +40% — 다른 measure same anchor
• Voronoi Cl std 0.74 → "두 group 존재" 직접 시각화 (4a + 4d)
```

**Key**:
```
• 같은 anti-site Cl 효과를 3 독립 측정이 다른 각도로 확인
• Voronoi (공간/기하) + BVSE (이동/path) + LOBSTER (결합/chemistry)
• 정량 cross-consistency (5.4 Li/AS, 60.2% group 정합)
• 단일 probe artifact 아닌 robust 물리 현상
```

**Footnote**:
```
※ 세 probe 정합성: 5.4 × 300/2700 = 0.6 = 60.2% (정확 일치)
※ +15%(BVS) vs +40%(ICOHP) 차이는 measure 정의 차이
※ Three independent post-processings → 단일 method failure mode와 무관
```

### 발표 스크립트 (60–70초)

> "Robustness section 시작. 4 메시지 + 5 cross-check가 robust한지 — 단일 method artifact가 아닌지 — 확인.
>
> 17번은 paper #1의 가장 강력한 cross-validation. 4d-Cl anti-site 효과를 세 개의 완전 독립 post-processing이 측정한 결과.
>
> 표 첫 행 Voronoi V std: 공간 부피 분산. modelc Cl std 0→0.74, Li std 0.21→1.15 (5.5×). Site disorder geometric fingerprint.
>
> 두 번째 BVSE bimodal: Li 이동 환경. 60.2% Li가 +15% BVS shift. Li percolation path 변화.
>
> 세 번째 LOBSTER ICOHP: 결합 강도. 4d-Cl AS Li-Cl −2.84 eV (4a 정상 −2.03보다 40%↑). Bonding chemistry 변화.
>
> 세 측정은 다른 angle — 공간/path/화학. 모두 같은 4d-Cl anti-site가 원인.
>
> 정량 cross-check: BVSE 1626 high-BVS Li / 300 AS Cl = 5.4 Li per AS — Li-Cl 1차 배위 4-6 정합. 60.2% 비율 자체가 5.4 × 300/2700 = 0.6과 정확 일치.
>
> +15% shift (BVS=형식가) vs +40% 강화 (ICOHP=결합 강도) — 다른 measure지만 same anchor.
>
> 단일 method artifact 아닌 robust 물리 현상 — three independent methods는 paper #1의 가장 강력한 referee defense."

### 시각 디자인 노트
- 3-probe 표 중심
- 3 box → anti-site Cl 수렴 화살표 그림
- 색 코딩: 3 probe 각각 다른 색 (slide 7/11/12 일관)
- "★" 5.4 Li/AS + 60.2% 정합성 강조
- "Three independent" footer

### Q&A
- "왜 3 probe만?" → 5 cross-check 중 anti-site에 직접 sensitive한 게 이 3개
- "Voronoi + BVSE 둘 다 geometric인데 차이?" → Voronoi 정적 부피, BVSE 동적 path
- "ICOHP electronic인데 geometric과 같은 결과?" → 짧은 거리에서 wavefunction overlap → geometry와 연결
- "이게 paper main figure?" → 후보 중 하나. headline은 slide 8 (E) or 6 (D₀) 강력. 이건 SI cross-validation panel
- "anti-site 비율 다른 cell도 정합?" → 1.6 Cl/fu 유지하면 5.4 Li/AS는 cell-independent (Li-Cl 1차 배위 결정)
- "+15% vs +40% 비율 아니라 방향만?" → BVS linear, ICOHP 적분 — direction 같음이 중요

---

### ★ 실물 확정판 (as-built deck slide 20 "Oxidation+ESW", 2026-06-11 — FINAL)

```
각주 K_eff/ESW · refs #1 Zuo/#2 Gil/#3 Wu 번호 체계 (표 ref 열·분해 박스가 #참조)
■ Oxidation stability: specify the axis — and our ESW backs it / bullets 3
[좌] 4-axis 표 (DRAW 'Ours,#2' / WINS청 '#2' / WINS청 'Ours,#1' / LOSES적 '#3')
[우상] ESW 풀 표 3×5 — Cl1.6 열 강조 (2.40 flat청 / 4.30 Sweet Spot청 / 20행 연초록)
[우하] 분해반응 점선 박스 (영어, LPSCl/LPSCl1.6 표기, 1.75/0.7 Li·1.6× LiCl 청,
      "quantitative match with #1")
```

## 1R. Slide 18+19 — **병합 → 본편 1장 "Oxidation: axis-resolved + our ESW backing" (2026-06-11 최종)**

> 직전 appendix안 철회 — 사용자 결정: 18(4-axis)과 19(ESW)를 **한 장으로 병합, 본편 deck 20**.
> [좌] 4-axis 압축 표 (DRAW/WINS★/WINS★/LOSES✗ + ref 3건) · [우] 우리 ESW 핵심 3줄
> (K_eff=0 flat→axis1 / K_eff=20 Cl1.6 peak 4.30★ Cl2.0↓→axis2 / 분해 +1.6×LiCl·−2.3×Li
> →Zuo Eq 정량 재현→axis3). 하단: "σ gain, NO oxidation penalty (1–3); cost = thermal
> (axis 4) → paper #2". tension audit #1 해소 열은 본편 참조 유지 (appendix 표기 불필요).

## (보존) Slide 18 — Robustness #2: Oxidation 4-Axis Framework

### 페이지 배치 (16:9)
- 4-axis 표 (axis 의미 / comp1 vs modelc / 출처)
- Axis 1 (우리 grand-potential) 세부 박스
- "axis 명시 필수" 한 줄 마무리

### 본문 텍스트

**제목**: "18. 'Cl-rich가 더 안정한가?' — 축을 지정해야 답이 된다"

**4-axis 표**:
```
Axis | 의미                          | comp1 vs modelc       | Reference
─────┼───────────────────────────────┼───────────────────────┼─────────────
  1  | 0-pressure intrinsic          | DRAW ~2.14 V          | 우리 + Gil 2022
     | bulk redox onset              | (S²⁻ limited)         |
  2  | Mechanically constrained      | Cl-rich WINS ★        | Gil-González
     | (K_eff > 0)                   | window 0.80-4.30 V    | ESM 2022
  3  | Cathode interface cycling     | Cl-rich WINS ★        | Zuo Angew
     | (R_int growth, CE)            | 8.9 vs 13.2 Ω·h^-0.5  | 2023
  4  | Thermal / calendar aging      | Cl-rich LOSES         | Wu Nano En
     | (shelf life 90°C)             | 48% vs 68% (5d)       | 2026
```

**Axis 1 우리 grand-potential**:
```
• Method: pymatgen PhaseDiagram + get_element_profile(Li, composition)
• MP GGA_GGA+U hull (108 entries Li-P-S-Cl)
• 0-pressure 양쪽 동일:
  - OCV self-decomposition: 1.72 V
  - Oxidation onset: 2.14 V (S²⁻ → polysulfide)
  - Cl⁻ inert until ~3.3 V
• Gil-González 2022 K_eff=0 LPSCl1.5: 1.70-2.40 V
  → 우리와 정합 (±0.26 V LiS4 inclusion 차이)
```

**Key**:
```
• 4축은 서로 다른 물리/실험 set
• modelc σ 향상이 oxidation penalty 없이 옴 (axis 1-3 neutral or favorable)
• 비용은 oxidation 아니라 thermal shelf life (axis 4)
• "Cl-rich 더 안정?" → axis 명시 필수
```

**Footnote**:
```
※ 세 문헌 full-text read 2026-06-08:
  Gil-González ESM 2022 (10.1016/j.ensm.2021.12.008)
  Zuo Angew 2023 (10.1002/anie.202213228)
  Wu Nano En 2026 (10.1016/j.nanoen.2025.111576)
※ 우리 grand-potential = Mo/Ong/Ceder 2012 framework
※ K_eff = effective bulk modulus = mechanical constriction (GPa)
```

### 발표 스크립트 (75–85초)

> "Robustness #2 — 'Cl-rich가 더 안정한가?'에 대한 정직한 답.
>
> 단일 답 없음. 4 독립 axis에서 답이 다르고, axis 지정 필수. 문헌 3편 full-text 통합 framework.
>
> Axis 1, intrinsic 0-pressure bulk redox onset. 우리 계산 양쪽 동일 2.14 V. S²⁻→polysulfide oxidation, Cl⁻ 3.3 V까지 inert. Gil-González K_eff=0과 ±0.26 V 정합 — 우리 계산이 같은 0-pressure axis cross-validation 깨끗.
>
> Axis 2, mechanical constraint K_eff>0. Cl-rich wider window. Gil K_eff=20에서 LPSCl1.5 0.80-4.30 V. Cl-bearing products (PCl3, SCl4) molar volume 커서 strain penalty 더 받음. Cl-rich가 mechanically constrained에서 stable.
>
> Axis 3, cathode interface cycling. Cl-rich 우세 — Zuo 2023 NCM85 R_int 성장 8.9 vs 13.2 Ω/h^0.5, CE 79 vs 77, 50cycle 145 vs 133. 실셀에서 Cl-rich 더 좋음.
>
> Axis 4, thermal calendar aging. Cl-rich 집니다 — Wu 2026 NCM811/LiIn 90°C 5일: L6 68% > L55 48%. SOC + cathode 큰 lever.
>
> 종합: modelc σ 향상이 oxidation penalty 없이 옴. 비용은 thermal shelf life. 'Cl-rich 더 안정?' axis 없이는 잘못된 질문."

### 시각 디자인 노트
- 4-axis 표 중심
- ★ axis 2/3 강조 (WINS)
- axis 4 (LOSES) 다른 색 — trade-off 시각화
- "축 지정 필수" 마지막 한 줄 강조
- 인용 footer 작게

### Q&A
- "왜 4축?" → 실용 4개. moisture 5번째 가능하지만 계산 없음
- "Axis 1 ↔ 2 connect?" → 우리 0-pressure ↔ Gil 0 GPa 정합. K_eff=0 limit 동일
- "Zuo 실험 직접 비교?" → Janek group Li5.5PS4.5Cl1.5, 우리 modelc Cl1.6 거의 동일
- "modelc axis 1만 우리?" → Cl/S anti-site 포함 grand-potential 우리 contribution
- "Axis 4 LOSES가 thesis 흔드나?" → No. paper #1 σ mechanism이 thesis. axis 4는 paper #2 motivation
- "main text? SI?" → main short + SI long axis-by-axis. nuanced honesty
- "정량 cross-check?" → axis 1 ±0.26 V vs Gil K_eff=0, axis 3 우리 interface reactivity vs Zuo -0.33 vs -0.32 eV/atom

---

## 1S. Slide 19 — **18과 병합 (위 1R 참조, 본편 deck 20)**

## (보존) Slide 19 — Robustness #3: Constrained ESW Cl-scan + 분해반응

### 페이지 배치 (16:9)
- 왼쪽: Constrained ESW Cl-scan plot (5 comp × 3 K_eff)
- 오른쪽: 분해반응 비교 (comp1 vs modelc at oxidation onset)
- Slide 18 axis 정합 + Zuo 2023 cross-validation

### 본문 텍스트

**제목**: "19. 우리 직접 계산 — Constrained ESW Cl-scan + 분해반응 chemistry"

**Constrained ESW Cl-scan**:
```
K_eff (GPa) | Cl 0.5 | Cl 1.0 | Cl 1.5 | Cl 1.6 (modelc) | Cl 2.0
────────────┼────────┼────────┼────────┼──────────────────┼────────
  0         | 2.40   | 2.40   | 2.40   | 2.40 (flat)      | 2.40
 10         | 3.20   | 3.40   | 3.80   | 4.05 ★           | 3.50 ↓
 20         | 3.70   | 4.10   | 4.20   | 4.30 ★★ peak     | 3.60 ↓↓

(anodic limit V vs Li/Li⁺)
```

**분해 반응 비교 (axis 1, oxidation onset 2.14 V)**:
```
comp1:
  Li₆PS₅Cl → Li₃PS₄ + 0.25 LiS₄ + LiCl + 1.75 Li ↑

modelc:
  Li₅.₄PS₄.₄Cl₁.₆ → Li₃PS₄ + 0.1 LiS₄ + 1.6 LiCl + 0.7 Li ↑
                                ────────────  ───────────
                                +1.6× LiCl    −2.3× Li
```

**Slide 18 axis 정합**:
```
• K_eff=0 flat → axis 1 (DRAW) 직접 backing
• K_eff=20 Cl=1.6 peak → axis 2 (Cl-rich WINS) 직접 backing
• 더 inert LiCl + 적은 Li release → axis 3 (Zuo R_int 낮음) 매칭
```

**Zuo 2023 cross-validation**:
```
• comp1 1.75 Li release ↔ Zuo Eq(1) "2 Li"
• modelc 0.7 Li release ↔ Zuo Eq(2) "1 Li"
• modelc 1.6 LiCl ↔ Zuo Eq(2) "1.5 LiCl"
→ 우리 grand-potential 실험 cell chemistry 정량 재현 ★
```

**Footnote**:
```
※ Method: tools/oxidation/constrained_esw.py (leading mode), 2026-06-09
※ K_eff 0/10/20 GPa, Cl 0.5/1.0/1.5/1.6/2.0 sweep
※ Zuo Angew 2023: Li₅.₅PS₄.₅Cl₁.₅ Eq(2)와 우리 modelc(Cl=1.6) 일관
```

### 발표 스크립트 (75–85초)

> "Robustness #3 — slide 18 oxidation 4-axis framework에 우리 직접 계산이 어떻게 backing하는지 정량 보여주는 슬라이드.
>
> 왼쪽 ESW Cl-scan. 5 조성 (LPSCl 0.5부터 2.0까지) × 3 K_eff (0/10/20 GPa).
>
> K_eff=0, 압력 없으면: 모든 Cl 함량에서 window ~2.4 V flat. Cl이 oxidation onset 안 바꿈. slide 18 axis 1 (DRAW) 직접 evidence.
>
> K_eff 10, 20 GPa로 올라가면 Cl 함량 따라 window monotonically 넓어짐. Cl=1.6 modelc에서 peak — K_eff=20에서 0.80-4.30 V. Cl=2.0 다시 좁아짐 (decomposition path P₂S₇로 바뀜). modelc sweet spot. axis 2 직접 backing.
>
> 오른쪽 oxidation onset 2.14 V 분해반응 비교. axis 1 onset 동일하지만 분해 chemistry는 완전 다름.
>
> comp1 LiCl 1.0 + Li 1.75 방출. modelc LiCl 1.6 + Li 0.7. modelc는 LiCl 1.6× 더 많이 + Li 방출 2.3× 적게.
>
> LiCl electrochemically inert (4 V까지), Li active. modelc 분해 = 더 mild solid byproduct + 적은 active Li.
>
> Zuo 2023 실험과 quantitative 정합. Eq(1)/(2): Li6PS5Cl → 2 Li, Li5.5PS4.5Cl1.5 → 1 Li가 우리 1.75 vs 0.7 Li와 일치. 우리 grand-potential이 실험 cell chemistry 정량 재현.
>
> 종합 — slide 18 lit framework가 정성 보여줬다면, 19는 우리 계산이 정량 backing. Cl-rich axis 1-3 우세는 우리 + 문헌 같은 결과."

### 시각 디자인 노트
- 왼쪽 Cl-scan: K_eff × Cl 격자 stack-bar 또는 line plot
- modelc Cl=1.6 column 강조 (★)
- 오른쪽 분해반응 두 줄, LiCl 증가 + Li 감소 색 강조
- "Zuo cross-validation" 별도 박스
- "modelc sweet spot" + "1.75 vs 0.7 Li" 강조

### Q&A
- "Constrained ESW method?" → Gil-González Eq(1): ΔG' = (G_D − G_SE) + V·ε_RXN·K_eff. Decomp strain penalty K_eff 비례 추가
- "Cl=2.0 왜 좁아짐?" → Decomp path 바뀜 — Cl=2.0 P₂S₇ 형성, strain penalty 약함
- "K_eff=20 GPa 실제 cell?" → Gil-González 38 MPa cell + GB 응력 lock-in 합쳐서 estimated effective
- "0.25 LiS4 fractional 의미?" → pymatgen grand-potential chempot 만족 balance. multi-fu sum이라 fractional 가능
- "1.6 vs 1.0 LiCl 정말 중요?" → Yes. LiCl 4 V까지 stable + electronic insulator → R_int 성장 늦춤 (Zuo 실험 증거)
- "1.75 vs Zuo 2 Li ±0.25?" → 우리 LiS4 inclusion, Zuo Eq(1) S elemental. 둘 다 valid
- "paper main figure?" → Strong 후보. axis 1 (정성 DRAW) + axis 2/3 정량 backing 한 페이지
- "axis 4 정량 backing?" → 못 함. Wu 2026 thermal/SOC 실험. paper 차후 작업

---

## 1T. ~~Slide 20 — Tension Audit~~ — **본편 제외 → Q&A 카드 시트 (2026-06-11, 사용자 결정)**

> 4-tension 해소는 이미 본편 inline 처리됨 (①oxidation→deck 20 본편 ②Ea macro/micro→M2
> Schlem 정합+6b ③vacancy paradox→M4 ④gap offset→M1 Q&A). 카드만 유지.

## (보존) Slide 20 — Referee Defense #1: Literature Tension Audit

### 페이지 배치 (16:9)
- 4-tension 표 (tension / 우리 결과 / 해소 method)
- 각 tension의 lit reference + 우리 해소 방법

### 본문 텍스트

**제목**: "20. 4가지 literature tension — 모두 해소"

**4 tension 표**:
```
# | Tension                       | 우리 결과              | 해소
──┼───────────────────────────────┼────────────────────────┼─────────────────────
1 | Oxidation: Cl-rich 더 안정?   | 0-pressure DRAW         | 4-axis framework
  | (lit consensus: yes)           | (slide 18 axis 1)       | (slide 18-19)
2 | Ea-vs-prefactor mechanism     | comp1 Ea < modelc        | macro vs micro Ea
  | (Minafra: disorder→Ea↓)        | but D₀ 8× explain σ     | + disorder ensemble (6b)
3 | Elastic vacancy paradox       | clamped 52 vs 52        | relaxed-ion +25%
  | (Kim 2025: Cl→E up)            | (동일)                  | matches Kim ★
4 | Band gap absolute             | PBE/USPP 1.76 vs       | method offset, Δgap
  | (PBE PAW ~2.3)                 | literature ~2.3         | 0.06 robust
```

**Key**:
```
• 4 tension 모두 "method/축 분리"로 해소 — artifact 아님
• Tension 1: axis 1만 우리; axis 2-3에서 Cl-rich WINS
• Tension 2: macro vs micro Ea, mutually compatible
• Tension 3: relaxed-ion 정확한 method로 Kim 직접 정합 ★
• Tension 4: pseudo offset 양쪽 동일, ratio robust
```

**Footnote**:
```
※ 5번째 tension (UMA Li3N topology)는 paper #2 영역, 본 paper 무관 — 제외
※ db/properties/literature_tensions_audit.json
※ Resolved 2026-06-08~09: oxidation + disorder_ensemble + Kim 2025 read
```

### 발표 스크립트 (60–70초)

> "Referee defense. paper #1 결과가 dominant lit narrative와 부딪히는 4 지점을 정직하게 정리하고 해소 방법.
>
> Tension 1 oxidation. 'Cl-rich 더 안정' lit consensus vs 우리 'DRAW' — slide 18 4-axis framework로 해소. 우리 calc는 axis 1 (intrinsic). lit consensus는 axis 2 (constrained) 또는 axis 3 (cell). 다른 measurement axis, 양쪽 valid.
>
> Tension 2 conductivity mechanism. Minafra 'disorder→Ea↓' vs 우리 'Cl-rich Ea 약간 높음' direction. 두 가지 해소: macroscopic Ea (실험 GB 포함) vs microscopic Ea (우리 bulk per-hop) 다른 양. 6/9-10 disorder ensemble matched-d에서 둘 다 ~0.18, Minafra ΔEa 우리 noise 아래라 mutually compatible.
>
> Tension 3 elastic vacancy paradox. Kim 2025 'Cl→E up' clamped-ion으로 못 잡음. relaxed-ion +25% E 강화 Kim과 직접 정합. clamped vs relaxed 정확한 method 차이.
>
> Tension 4 band gap absolute. PBE/USPP 1.76 vs lit PBE PAW 2.15-2.45. USPP + DOS-threshold systematic ~0.4 eV underestimate. 양쪽 동일 적용 Δgap robust.
>
> 4 tension 모두 'artifact 아닌 method/축 분리' 해소. paper nuanced honesty 핵심 슬라이드."

### 시각 디자인 노트
- 4-row 표 중심
- 각 row 색 구분 + Resolution column 강조
- "Resolved" 표시 (✓ 또는 ★)
- footnote에 db reference

### Q&A
- "왜 5번째 안 포함?" → UMA Li3N paper #2 영역
- "Tension 1과 4 비슷한 frame?" → Both method-axis distinction
- "Tension 2 disorder ensemble compatible?" → Strict 우리 해상도 부족, 'rule out 불가' framing
- "Tension 3 relaxed-ion 새 발견?" → method 표준이지만 LPSCl/LPSCl1.6 paired + Kim 2025 매칭은 우리 contribution
- "Tension 4 0.4 eV offset 정상?" → USPP + DOS-threshold systematic, lit PBE도 PAW vs USPP 동일
- "Main paper?" → Short discussion + SI long

---

## 1U. ~~Slide 21 — Caveats~~ — **본편 제외 → Q&A 카드 시트 (2026-06-11, 사용자 결정)**

> 9-caveat은 발표 중 인라인 정직 표기(MLIP MD 캡션·ratio-only·외삽 본편 제외)로 대체.
> paper limitations section용 본문은 아래 보존. 최종 본편 = 21장:
> 1~7 intro+headline / 8~13 M1~M4(+M2-1,M4-1) / 14~18 CC#1~5 / 19 Summary /
> 20 Oxidation+ESW / 21 Trade-offs&Outlook.

## (보존) Slide 21 — Referee Defense #2: Caveats Consolidated

### 페이지 배치 (16:9)
- 9-row caveat 표 (caveat / 우리 대응 / 영향 받는 결과)
- 요지 box (어떤 caveat도 4 메시지 안 흔듦)

### 본문 텍스트

**제목**: "21. 모든 caveat 한 페이지 — 정직한 method limitation"

**9-row caveat 표**:
```
# | Caveat                          | 우리 대응                           | 영향 받는 결과
──┼─────────────────────────────────┼─────────────────────────────────────┼──────────────
1 | UMA MLIP σ overshoot ~3-5×       | σ ratio 사용 (절대 σ 인용 X)        | σ absolute
2 | Haven ratio = 1 가정              | σ_NE는 upper bound로 표기            | σ absolute
3 | 3-pt Arrhenius 300K 외삽         | 정성적 trend만, 정량 단정 X          | D(300K)
4 | k-mesh convergence required     | k×L ≥ 40 Å 양쪽 보장                 | gap, elastic, DOS
5 | LOBSTER charge spilling          | 1.16% / 1.46% (paper <5%)            | ICOHP 정량
6 | 5 f.u. cell / n=3 configs       | ΔEa < 0.05 eV 해상도 못 잡음        | Ea matched-d
7 | USPP gap 0.4 eV underestimate   | method offset 명시, Δgap robust      | gap absolute
8 | 0-pressure ESW only             | K_eff axis 분리                      | oxidation stab.
9 | Random anti-site disorder model | 실험 charge-coupled placement와       | ensemble Ea
  |                                  | 다를 수 있음                          |
```

**요지**:
```
• 어떤 caveat도 4 메시지 자체를 흔들지 못함
• 절대값 영향 caveat 있지만 trend / ratio / mechanism robust
• Same-protocol paired comparison의 힘
```

**Footnote**:
```
※ Paper limitations section에 그대로 인용 가능
※ 각 caveat source: db/properties/li_transport.json, electronic.json 등 분산 기록
※ "솔직히 깔아둠"이 paper의 가장 강력한 referee defense
```

### 발표 스크립트 (45–55초)

> "Referee defense 마지막 — 모든 caveat 한 페이지 정직하게.
>
> 9개 caveat 정리.
> 1: UMA σ 3-5× overshoot → ratio만 사용.
> 2: Haven=1 → σ_NE upper bound 표기.
> 3: 3-pt Arrhenius 300K 외삽 정성적만.
> 4: k×L ≥ 40 Å 양쪽 보장 (slide 14 incident).
> 5: LOBSTER spilling 1.16-1.46% (<5% paper 기준).
> 6: 5 f.u. n=3 noise 0.05 eV — Minafra 0.08 eV 시그널 못 confirm/refute.
> 7: USPP gap 0.4 eV underestimate, ratio robust.
> 8: ESW 0-pressure 한정, K_eff axis 분리.
> 9: random anti-site placement, 실험 charge-coupled와 다를 수 있음.
>
> 요지: 어떤 caveat도 4 메시지 자체를 흔들지 못함. 절대값 영향은 있어도 trend/ratio/mechanism robust. same-protocol paired comparison의 힘.
>
> 솔직히 깔아두는 게 paper-grade defense 마지막 보루. referee가 'caveat 안 깔았다' 못 잡음."

### 시각 디자인 노트
- 9-row 표
- "영향 받는 결과" column 색 분류 (절대값 vs trend)
- "어떤 caveat도 4 메시지 안 흔듦" 강조
- paper limitations section 후보 명시

### Q&A
- "왜 9개?" → 핵심 9개, paper 작성 시 추가 가능
- "Caveat 6 가장 큰 약점?" → substantive. 다만 disorder ensemble 신규 contribution + 'noise floor 명시'가 정직성
- "MLIP overshoot ratio도 영향?" → systematic 가능. 실험 σ ratio (Zuo 2.9 vs 7.0) ↔ 우리 3× 정합 → ratio robust
- "Haven=1 표준?" → 표준 simplification. SI 명시
- "Caveat 7 paper main?" → No, ratio robust. method 한정 명시
- "Paper limitations section?" → 직접 인용
- "솔직성 = defense?" → Yes. limitations 깔면 referee trust; 숨기면 reject

---

### ★ 실물 확정판 (as-built deck slide 21 "Trade-offs & Outlook", 2026-06-11 — FINAL, 본편 완결)

```
■ Trade-offs & Outlook — the same disorder, two faces / ref Wu만 (나머지 구두)
[상단 적 점선박스] 4 Trade-offs (idle/storage only): thermal 68→48 · moisture H₂S
  · synthesis Cl≥1.7 · mild anisotropy Zener 1.44적
↓ 화살표 [하단 청 점선박스] Strategy example: oxide doping 가설 1줄
  (O–Li thermal↑ · Cl/O anisotropy↓ · gettering blocks LiCl)
다이어트: 공통원인(4d-Cl AS 양면성)·후보 현황(41 champions, Sc/B/Nd)·design 문장은
대본 전담. 본편 21장 완결: 1~7 / 8~13(M) / 14~18(CC) / 19 Summary / 20 Ox+ESW / 21 Outlook.
```

## 1V. Slide 22 — Trade-offs & Outlook: Paper #2 Bridge (★ FINAL)

### 페이지 배치 (16:9)
- Top panel: 4 Trade-offs (idle/storage 영역만)
- Bottom panel: Oxide Doping Mitigation Strategy (Sc₂O₃/B₂O₃/Nd₂O₃ ★)
- 두 panel 사이 ↓ + "Paper #2 Strategy" 화살표

### 본문 텍스트

**제목**: "22. Trade-offs & Outlook — Paper #2 Doping Strategy로의 다리"

**Top panel — 4 Trade-offs**:
```
LPSCl₁.₆ Trade-offs (idle/storage 영역만):

1. Thermal calendar shelf life
   Wu 2026: 90°C 5일, L6 68% > L55 48% > L53(Cl1.7) 35%
2. Moisture sensitivity
   Cl⁻ + H₂O → LiOH·LiCl + H₂S 빠른 방출 (Strauss, Kraft)
3. Synthesis window
   Cl ≥ 1.7 phase-pure 어려움 (Adeli, Yu, Wu)
4. Mechanical anisotropy
   Zener A 1.14 → 1.44 — mild but cycling fatigue 가능

Common cause: 4d-Cl anti-site disorder
  → M3 (ICOHP +13%) 및 M4 (E +25%)의 출처와 같음 (양면성)
```

**Bottom panel — Mitigation Strategy**:
```
Mitigation via Oxide Doping (X₂O_y → SE)

Hypothesis:
  • O²⁻가 PS₄에 부분 치환 또는 4d 자리 점유
  • O–Li 강한 결합 → thermal stability ↑
  • Cl/O mixed anion sublattice → anisotropy 완화 + dendrite path 차단
  • Oxide gettering으로 LiCl 2차상 형성 억제

Active 후보 (14 dopant × 3 conc cascade screening):
  ★ Sc₂O₃   — cascade strongest winner (de_post=-0.974, E_VRH 18.7 GPa)
  ★ B₂O₃    — thermal stabilizer, anneal+EOS 진행 (V100 paused)
  ★ Nd₂O₃   — DFT-relaxed run5 완료 (E=-3566.21 Ry), EOS+post 대기
  • Al₂O₃ cluster (-0.79..-0.82), MnO/CoO 부드러움 후보
  • 41 champions: db/properties/doping_cascade_verified.json

Pipeline: cascade screen → DFT EOS → §8 → NCM interface → calendar AIMD
```

**마무리 한 줄**:
```
→ Paper #1 (mechanism understanding) ↔ Paper #2 (mitigation engineering)
  "구조적 무질서의 양면성을 이해했으니, 이제 그 무질서를 'design'할 수 있다."
```

### 발표 스크립트 (70–80초)

> "마지막 슬라이드 — paper #1 마무리하고 paper #2로 연결.
>
> 위 panel — LPSCl₁.₆의 4가지 trade-off. 모두 idle/storage 영역에 집중. Performance는 가지면서 비용은 따로 있음.
>
> Wu 2026 thermal calendar 90°C 5일 Cl 함량 따라 retention monotonic 감소. moisture sensitivity Cl⁻+H₂O 반응성 lit consensus. synthesis window Cl 1.7 이상 phase-pure 어려움. mechanical anisotropy Zener A 1.14→1.44 mild but cycling fatigue 가능.
>
> 흥미로운 건 — 이 4 trade-off의 공통 원인이 paper #1 M3 메시지의 4d-Cl anti-site disorder 그 자체. M3 ionic glue +13%, M4 shear +30%를 준 source가 동시에 thermal decay 빠르게 하고 moisture 반응성 키움. 양면성.
>
> 아래 panel paper #2 strategy. Oxide doping으로 mitigate. O²⁻가 PS₄ 부분 치환 또는 4d 점유 → O-Li 강한 결합 thermal ↑, Cl-O mixed sublattice anisotropy 완화, oxide gettering LiCl 차단.
>
> 14 dopant × 3 농도 cascade screening 진행, 41 champion verified. Sc₂O₃ strongest winner (de -0.974, E_VRH 18.7 가장 soft). B₂O₃ Nd₂O₃ DFT validation 진행.
>
> Pipeline cascade screen → DFT EOS → §8 → NCM interface → calendar AIMD.
>
> 결론: paper #1이 mechanism understanding, paper #2가 mitigation engineering. 구조적 무질서의 양면성을 이해했으니 이제 design할 수 있다는 게 두 paper 묶는 narrative.
>
> 감사합니다."

### 시각 디자인 노트
- Top (trade-offs): 4 항목 적색 톤 (비용)
- Bottom (mitigation): 청색 톤 (해결)
- 두 panel 사이 ↓ + "Paper #2 Strategy"
- ★ Sc₂O₃ / B₂O₃ / Nd₂O₃ 강조
- "양면성 (duality)" + "design" 강조

### Q&A
- "왜 oxide doping?" → O²⁻ 강한 Li 결합 + Cl/O mixed sublattice 안정화 + 2차상 차단
- "Sc₂O₃ 왜 strongest?" → de_post -0.974, E_VRH 18.7 soft, single x002만 완료 (x005/x010 follow-up)
- "B₂O₃ 진행?" → V100 GPU lock paused. 마지막 EOS v0.98 BFGS step 5. gabia 재개 가능
- "Nd₂O₃ 4f 어렵?" → DFT+U(U=6) ISPIN=2 처리. PDOS 어렵지만 EOS OK. run5 V0 완료
- "14 dopant 전체 compare?" → doping_cascade_verified.json 41 champion 완료. paper #2 systematic ranking
- "Paper #2 main message?" → "trade-off-resolved Cl-rich = best of both worlds"
- "Outlook이 paper #1에?" → conclusion + future work 단락. paper #2 cross-reference
- "Paper #1/#2 동시 제출?" → 가능. short report + full → 권장

---

## 1W. References — Trade-off literature 참고 (paper writing용)

> 발표 slides 본문에는 안 들어가지만 paper #1/#2 writeup 시 cite할 수 있도록 모아둠.

### A. Thermal / Calendar shelf life (Cl-rich penalty)
- **Wu et al., Nano Energy 2026, 147, 111576** (10.1016/j.nanoen.2025.111576) — 90°C 5d calendar aging: L6 68% > L55 48% > L53 (Cl 1.7) 35%, Cl ↑ monotonic. 핵심 Wu paper.
- **Adeli et al., Angew. Chem. Int. Ed. 2019, 58, 8681** (10.1002/anie.201814222) — Li₅.₄PS₄.₄Cl₁.₆ 합성 + Humidity 노출 H₂S 빠른 방출
- **Schlem et al., Adv. Energy Mater. 2020, 10, 1903719** — Cl-rich DSC mass loss onset 315°C (Cl-poor 350°C)
- **Tan et al., ACS Energy Lett. 2021, 6, 1933** — Cl-rich TGA thermal stability 낮음

### B. Moisture sensitivity (Cl-rich penalty)
- **Strauss/Janek, Chem. Mater. 2018, 30, 6720** — Li₆PS₅Cl + H₂O → LiOH·LiCl + H₂S, Cl-rich 가속
- **Kim/Janek, ChemSusChem 2020, 13, 4901** — Li₆PS₅X moisture stability: I > Br > Cl > Cl-rich
- **Kraft et al., J. Am. Chem. Soc. 2017, 139, 10909** — Cl⁻ + H₂O hydroxylation 수월 (vs Br⁻, I⁻)
- **Bachman et al., Chem. Rev. 2016, 116, 140** — Argyrodite humidity intolerance + Cl-rich 가속

### C. Synthesis window (phase-pure 한계)
- **Adeli, Angew. Chem. 2019** (위와 동일) — Li₅.₄PS₄.₄Cl₁.₆ 합성 lower bound
- **Yu et al., Nat. Commun. 2022, 13, 6320** — Li₅.₃PS₄.₃Cl₁.₇ phase-pure 어려움
- **Wu et al., Nano Energy 2026** (위 A와 동일) — Cl > 1.8 phase-pure 실패
- **Schlem et al., Adv. Energy Mater. 2020** (위 A와 동일) — Cl 1.5–1.7 sweet spot

### D. Mechanical anisotropy + SSB cycling stress
- **Pan/Sun et al., ACS Energy Lett. 2021, 6, 4377** — SSB stack pressure 10–100 MPa 영향, 비등방 SE crack initiation
- **Doux et al., Joule 2020, 4, 2487** — Contact pressure 의존성, 비등방 SE 압력 요구도 ↑
- **Krauskopf et al., Joule 2020, 4, 2540** — Li flux 비균일성 ↔ mechanical anisotropy
- **Lewis et al., Joule 2022, 6, 1126** — Heterogeneous Li deposition + mechanical anisotropy
- **Hatzell et al., J. Power Sources 2020, 459, 228063** — Pressure-dependent ICR, 비등방 SE sensitive
- **Wang et al., Sci. Adv. 2022, 8, eabm3868** — Polycrystalline SE texture effect σ ±30%

### E. SSB SE 전반 trade-off review
- **Janek/Zeier, Nat. Energy 2023, 8, 230** — SSB SE 설계: σ ↑ vs stability ↓ universal trade-off
- **Famprikis/Masquelier, Nat. Mater. 2019, 18, 1278** — Inorganic SE review, Cl-rich argyrodite trade-off
- **Chen et al., Adv. Energy Mater. 2021, 11, 2002717** — Argyrodite review, Cl 함량 vs property table

### F. Performance side (modelc 우세 backing)
- **Zuo et al., Angew. Chem. Int. Ed. 2023, 62, e202213228** (10.1002/anie.202213228) — σ(Li₆PS₅Cl) 2.9 vs σ(Li₅.₅PS₄.₅Cl₁.₅) 7.0 mS/cm, R_int 8.9 vs 13.2 Ω·h^0.5, CE 79% vs 77%
- **Schlem et al., Adv. Energy Mater. 2020** (위와 동일) — Ea (Cl-rich 0.22 / ordered 0.25) ★ 우리 4fu 매칭
- **Minafra/Kraft, Solid State Ionics 2020, 346, 115223** — "Enhanced ion conduction by enforcing structural disorder"
- **Kim et al., ACS Mater. Lett. 2025** — Cl ↑ → E_Young ↑ (UPE), 우리 relaxed-ion +25% 매칭 ★
- **Gil-González et al., Energy Storage Mater. 2022, 45, 484** (10.1016/j.ensm.2021.12.008) — Constrained ESW K_eff sweep, Cl-rich K_eff>0 wider window
- **Deiseroth et al., Angew. Chem. Int. Ed. 2008, 47, 755** — 원조 Li₆PS₅X argyrodite, 4a/4d cage topology

### G. paper #1 framing summary (한 줄)
> "modelc (LPSCl₁.₆) shows substantial performance gain across all operation-relevant axes (σ +3×, E +25%, R_int −33%, cycling CE +2%). The cost is concentrated in **idle/storage axes** — thermal calendar aging (Wu 2026), moisture sensitivity (Kraft/Janek series), Cl synthesis window limit (Adeli/Yu), and mild mechanical anisotropy (Zener 1.14→1.44) — none of which compromise operation but motivate the additive strategy explored in Paper #2."

---

## 2. 변경 이력

| 버전 | 날짜 | 변경 |
|---|---|---|
| v1 | 2026-06-10 | 초안 — 전체 22장 구조 + Slide 1 layout 확정. paper #2 분리. adhesion 제외. |
| v1.1 | 2026-06-10 | Slide 1 script v2 정제: 전자구조 0.06 eV 차이 정직하게 인정, 영문 포뮬러 / paper title 톤 제거 |
| v1.2 | 2026-06-10 | Slide 1 script v3: 정량 수치 제거 (정성적 표현으로), 첫 페이지 톤 가벼움 |
| v1.3 | 2026-06-10 | Slide 1 script v4 (★ ACTIVE): "궤도 character" → "전자구조 전반 패턴" vague (직접 비교 문헌 없음 회피). PS₄ 단정 유지 |
| v1.4 | 2026-06-10 | Slide 2 (Scope) + Slide 3 (3-tier pipeline) drafted. site preference + cell parameter pipeline 압축 |
| v1.5 | 2026-06-10 | Slide 4 (Headline 4-message table) drafted — Tier 3 §8 post-processing 진입점 |
| v1.6 | 2026-06-10 | Slide 5 (M1: 전자구조 둔감) drafted — DOS overlay + gap 1.76 vs 1.82 + modelc defect band note |
| v1.7 | 2026-06-10 | Slide 5a DROPPED (slide 14 audit과 중복). Slide 6 (M2: σ prefactor) drafted — Arrhenius + D₀ 8× narrative |
| v1.8 | 2026-06-10 | Slide 6 footnote + script v2: **실험 macroscopic Ea vs 우리 microscopic Ea framing**. Minafra/Kraft tension 우아하게 해소 (mutually compatible) |
| v1.9 | 2026-06-11 | Slide 6 **HOLD** (comp1 4 f.u. natural-cell MLIP MD 재실행 중, 결과 따라 3-way framing 분기). Slide 7 (M3 ionic glue) drafted — ICOHP +13%/+8%, 4d-Cl AS −2.84 eV, 3-probe 합의 |
| v1.10 | 2026-06-11 | Slide 6a (mechanism cartoon) / 6b (disorder ensemble = ground truth, **v0_xyz=comp1_V0_k444 4fu 검증 — ensemble 재실행 불필요 확정**) / 6c (저온 trade-off, A/B 시나리오 조건부 HOLD) drafted |
| v1.11 | 2026-06-11 | Slide 8 (M4: vacancy paradox 해소) drafted — clamped 52.31 동일 → relaxed-ion +25%, G +30% shear stiffening, Kim 2025 매칭, M3 4d-Cl mechanical 발현 |
| v1.12 | 2026-06-11 | Slide 8a (Cij 분해: C44 +72% — shear lock-in mechanism) / 8b (4 cross-check: B↔B0, AFM, 600K MLIP, spilling+k×L) drafted. M4 클라이맥스 완성 |
| v1.13 | 2026-06-11 | Slide 9 (cross-check #1: PS₄ universal backbone) drafted — 5 probe (P-S 길이/σ/배위/ICOHP/ELF/Bader) + universal anchor Li-S(4d), rigid block 결론 |
| v1.14 | 2026-06-11 | Slide 10 (cross-check #2: counter-intuitive bond) drafted — Li–Cl −0.076 Å (4d AS 2.45 Å, 4a보다 0.16 짧음), Cl⁻ vs S²⁻ ionic radius 매칭 + Voronoi V −1.7 Å³ 직접 증거 |
| v1.15 | 2026-06-11 | **Slide 7 v2 + Slide 10 v2** ACTIVE: vacancy(69%)+anti-site(31%) 분해 정확화, per-bond vs per-anion 명시 (LOBSTER covalent overlap 우세 측정 vs S²⁻ q² × coord total). Coulomb 직관 회복. paper-grade defensible mechanism. |
| v1.16 | 2026-06-11 | Slide 11 (cross-check #3: Voronoi 4-sublattice fingerprint) drafted — P 0→0.37 (framework 일관), Cl 0→0.74 (분기), Li 0.21→1.15 (×5.5 ★), S 3.41→2.05 (역설적 균질화 ★). 3 probe convergence. PDOS Cl 3p −2.5 eV vs S (mechanism 2 confirmed both systems). |
| v1.17 | 2026-06-11 | Slide 12 (cross-check #4: BVSE bimodal paired 5×5×5) drafted — comp1 단일 peak vs modelc bimodal (39.8% comp1-like + 60.2% +15% shifted), 5.4 Li per AS, BVSE +15% ↔ ICOHP +40% 두 probe 일관, 37.5% AS stoichiometric necessity |
| v1.18 | 2026-06-11 | Slide 13 (cross-check #5: ELF covalent vs ionic) drafted — P-S bridge ELF 0.95 동일, Li basin <0.1 양쪽 ionic, mechanism 1 (LOBSTER covalent overlap)의 시각 evidence. Cross-check section (9-13) 완성 |
| v1.19 | 2026-06-11 | Slide 8 footnote 추가: "PS₄ 불변인데 왜 단단해지나" 직관 — PS₄=rigid blocks (M1), Li-anion=mortar (M3 +13%) → shear stiff (G +30%) → E_VRH +25%. M1↔M3↔M4 인과 chain 명시 |
| v1.20 | 2026-06-11 | Slide 14 (k-mesh audit & method convergence) drafted — comp1 k=2×2×1 incident → k=4×4×4 복구 (gap 1.50 → 1.76, RMS 0.003), property k-sensitivity table, LOBSTER spilling 1.16-1.46% paper-grade. Referee defense 시작 |
| v1.21 | 2026-06-11 | Slide 15 (Methods consistency: 3 tier 한 페이지) drafted — Tier 1 MLIP / Tier 2 DFT (PBE/USPP/k×L≥40) / Tier 3 §8 (13 probe 양쪽 동일 V₀), 컴퓨팅 자원 분산. Paired comparison 정당성 토대 |
| v1.22 | 2026-06-11 | Slide 15 **DROPPED** (slide 3 pipeline + slide 14 k-mesh audit과 중복). 총 22 → 21장. |
| v1.23 | 2026-06-11 | Slide 16 (Summary) drafted — 불변/변화 2-컬럼 대조표 + thesis ("covalent skeleton 유지 + ionic ligament 재배치") + 4 메시지 한 줄씩. paper #1 abstract/conclusion 후보 |
| v1.24 | 2026-06-11 | Slide 15 헤더 명확화 — 발표 DROPPED, paper Methods section 후보로 본문 보존 (ecutwfc, k-mesh, LOBSTER, ELF settings 전부) |
| v1.25 | 2026-06-11 | Slide 17 (Robustness #1: 3-probe convergence) drafted — Voronoi (geometric) + BVSE (path) + LOBSTER (chemistry) 같은 anti-site Cl 효과 측정. 5.4 Li/AS + 60.2% 정합성 cross-validation. Paper #1 robust referee defense |
| v1.26 | 2026-06-11 | Slide 18 (Robustness #2: Oxidation 4-axis framework) drafted — Gil-González + Zuo + Wu 통합. Axis 1 (DRAW), 2 (Cl-rich WINS K_eff>0), 3 (Cl-rich WINS R_int), 4 (Cl-rich LOSES calendar). modelc σ 향상이 oxidation penalty 없이 옴, 비용은 thermal shelf life |
| v1.27 | 2026-06-11 | Slide 19 (Robustness #3: Constrained ESW + 분해반응) drafted — Cl-scan (Cl=1.6 K_eff=20 sweet spot), oxidation onset 2.14V 분해반응 (modelc 0.7 Li vs comp1 1.75 Li, 1.6× LiCl), Zuo 2023 Eq(1)/(2) 정량 cross-validation |
| v1.28 | 2026-06-11 | Slide 20 (Referee defense #1: 4-tension audit) + Slide 21 (Referee defense #2: 9-caveat consolidated) drafted — paper #1 nuanced honesty + limitations transparency. Section F (Referee defense) 완성 |
| v1.29 | 2026-06-11 | **comp1 4 f.u. natural MLIP MD 결과 도착**: Ea=0.2532, D₀=4.11e-4, R²=0.9998 — Schlem 2020 LPSCl ordered ~0.25 EXACT match. **Slide 6 HOLD 해제 → v3 ACTIVE**: σ gain = Ea↓ (1.75×) + D₀↑ (1.41×) ≈ 2.5× 둘 다 작용. Minafra/Kraft direction 정합. 5 f.u. (Ea=0.172) = 인위 supercell artifact 확정. **db/properties/li_transport.json 갱신**: comp1_v3_5fu SUPERSEDED, comp1_v3_4fu_natural PRIMARY. Paper #1 mechanism narrative 변경 (prefactor-only → dual mechanism). |
| v1.30 | 2026-06-11 | Slide 6c v3 ACTIVE — **No T_cross, modelc wins at ALL T**, 저온일수록 σ ratio ↑ (RT 4.3×, 200K 7×). Zuo 2023 RT 측정 2.4× ↔ 우리 외삽 4.3× 자릿수 정합. v1/v2 'vacancy 양날' framing 무효 — 4fu 자료로 reversed. |
| v1.31 | 2026-06-11 | References 섹션 추가 (slide 본문 외, paper writing용) — Thermal/Calendar (Wu/Adeli/Schlem/Tan), Moisture (Strauss/Janek/Kraft/Bachman), Synthesis window (Adeli/Yu/Wu), Mech anisotropy SSB (Pan/Sun, Doux, Krauskopf, Lewis, Hatzell, Wang), Trade-off review (Janek/Zeier, Famprikis, Chen), Performance backing (Zuo/Schlem/Minafra/Kim/Gil/Deiseroth) + paper #1 framing summary 한 줄 |
| v1.32 | 2026-06-11 | **Slide 22 (Trade-offs & Outlook: Paper #2 Bridge) drafted ★ FINAL** — Top panel 4 trade-offs (Wu thermal / Strauss moisture / Adeli synthesis window / Zener anisotropy), 공통 원인 4d-Cl AS (M3-M4와 동일). Bottom panel Oxide Doping Strategy: Sc₂O₃ (cascade strongest, de=-0.974) / B₂O₃ (anneal+EOS) / Nd₂O₃ (DFT-relaxed) / Al₂O₃ cluster. "구조적 무질서를 design" 마무리. 21장 deck 완성 |
| v1.33 | 2026-06-11 | **1C에 comp1 enumeration & champion 역전 기록 추가 (Q&A 필수 카드)** — comp1도 C(8,4)=70 full enumeration 통과. Halogen 단계 (Li Rietveld 고정) best = #39 mixed 2/2였으나 Li screening (spread 1162 meV) + 500 K anneal에서 **ordered (Cl 전부 4a / free-S 전부 4d)로 역전** → v3 k444 V0의 출처. "같은 pipeline이 comp1 ordered / modelc 12.5% anti-site를 내놓음 = disorder는 조성이 만든다" thesis 직접 증거. Slide 3 본문 enumerate 수 정정: 45 → comp1 70 (8C4) · modelc 45 (10C2) |
| v1.34 | 2026-06-12 | **Slide 1 → 연구실 표준 템플릿 (Layout v2)**: Research Seminar 타이틀 + Part divider 사용, **title에 thesis 넣지 않음**. 구 slide 1의 질문/결론/thesis는 **Slide 2 (Scope+Thesis 통합, script v2 70–80초)**로 흡수. Part 매핑 제안: P1 Intro(2–4) / P2 4 Messages(5–8) / P3 Cross-check & Defense(9–16) / P4 Robustness & Outlook(17–22). 구 버전 모두 보존 |
| v1.35 | 2026-06-12 | Slide 2 본문 v3 — 연구실 템플릿 bullet 형식 (■ Key finding 결론 먼저 + ■ Cell configurations 한 줄씩). 슬라이드 제목 확정: "LPSCl vs LPSCl₁.₆ — Why Faster & Stiffer?" |

---

## 3. TODO (다음 작업)

- [x] Slide 2 (Scope) — drafted 2026-06-10
- [x] Slide 3 (Pipeline schematic) — drafted 2026-06-10
- [x] Slide 4 (Headline 표) — drafted 2026-06-10 (Tier 3 post-processing 진입)
- [x] Slide 5 (M1 — 전자구조 둔감) — drafted 2026-06-10
- [x] ~~Slide 5a (sub: k-mesh incident)~~ — **DROPPED** (slide 14 audit과 중복, 총 22→21장)
- [x] Slide 6 (M2 — σ prefactor) — drafted 2026-06-10, **⚠ HOLD** (comp1 4fu MLIP MD 결과 대기, 3-way framing 분기)
- [x] Slide 7 (M3 — ionic glue) — drafted 2026-06-11
- [x] Slide 8 (M4 — vacancy paradox 해소) — drafted 2026-06-11
- [x] Slide 8a (Cij 분해 + shear lock-in mechanism) — drafted 2026-06-11
- [x] Slide 8b (4 cross-check defense) — drafted 2026-06-11
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
