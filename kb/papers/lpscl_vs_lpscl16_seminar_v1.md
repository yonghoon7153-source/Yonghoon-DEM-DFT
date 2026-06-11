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

## 1B. Slide 2 — Scope (두 시스템 소개)

### 페이지 배치 (16:9)
- 좌·우 panel 나란히 (동격 비교)
- VESTA 구조 그림 (cubic comp1 vs rhombo modelc, 같은 scale + viewing angle)

### 본문 텍스트

**상단**: "비교 대상: 두 argyrodite"

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

### 발표 스크립트 (40–50초)

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

### 페이지 배치 (16:9)

3개 box 세로 stack, 위에서 아래로 화살표, gradation 색 (옅은→진한 청).

### 본문 텍스트

**상단**: "Pipeline: MLIP screen → DFT confirm → multi-probe"

**Tier 1 box**:
```
Tier 1 · MLIP screening (hours)
• Halogen enumerate — 45 configs
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
> **Tier 1, MLIP screening**. argyrodite는 음이온이 어느 자리에 앉느냐, Li가 어떻게 배치되느냐가 cell 에너지에 영향을 줍니다. 특히 modelc 같은 Cl-rich에서는 4d 자리에 Cl이 들어가는 패턴이 중요해요. 이걸 DFT로 직접 enumerate하면 셀당 시간이 걸려서 4000개 조합을 다 못 돌립니다. 그래서 UMA foundation MLIP으로 합니다 — halogen enumerate 45개, Li screen top 5 × 20개, 500K annealing까지 hours 안에 끝납니다. 여기서 **champion 구조와 site occupancy**가 나옵니다.
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

---

## 1D. Slide 4 — Headline Table (4 messages preview)

### Tier 3 post-processing 진입점

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

### 페이지 배치 (16:9)
- 왼쪽: DOS overlay plot (comp1 파랑, modelc 빨강) + Fermi 점선 + VBM/CBM 음영
- 오른쪽: gap + EF + VBM/CBM character 표
- 하단: 3 bullet key points + footnote (modelc defect band)

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

## 1F. Slide 6 — M2: σ는 prefactor 우세 (vacancy carrier)

> ⚠ **HOLD (2026-06-11)** — comp1 **4 f.u. natural-cell MLIP MD** 재실행 중 (gabia GPU 단독, ETA ~12-15h).
> 현재 Ea 비교(0.172 vs 0.224)는 comp1 5 f.u. 인위 supercell 기반이라 방향이 lit (Cl-rich Ea↓ 통념)과
> 반대. matched-disorder ensemble (0.177 ≈ 0.173)에서는 동일. 4 f.u. 결과에 따라 세 가지 framing 분기:
> - 4fu Ea ≈ 0.25-0.30 → "barrier↓ + prefactor↑ 둘 다" (lit 정합)
> - 4fu Ea ≈ 0.18 → "matched-d Ea 동일, prefactor 우세" (현 v2 유지)
> - 4fu Ea ≈ 0.17 → "MLIP ordered-LPSCl bias caveat + prefactor 우세"
> **값 나오면 본문/표/스크립트 확정.** 그 전까지 아래 draft는 잠정본.

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

## 1F-1. Slide 6a — Mechanism Cartoon (carrier vs barrier)

### 페이지 배치 (16:9)
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

## 1F-2. Slide 6b — Disorder Ensemble: Ea의 ground truth ★

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

## 1F-3. Slide 6c — 저온 trade-off (조건부 ⚠ HOLD)

> slide 6 main과 연동 HOLD. 4 f.u. 결과로 A/B 시나리오 결정.

### 본문 텍스트
```
시나리오 A — clean-cell 값 (0.172 vs 0.224) 기준:
  T_cross ≈ 290 K. 그 위 modelc 우세 (prefactor), 그 아래 comp1 역전 (낮은 barrier).
  vacancy = 양날.

시나리오 B — matched-disorder 값 (0.18 ≈ 0.17) 기준:
  Ea 같음 → 교차 없음. modelc가 전 온도에서 ~3× 빠름 (D₀ 8×).
  'Cl-rich 저온 불리' 주장 소멸.

실험 단서: RT에서 modelc ~2× 우세 (Zuo) → B와 더 정합
```

### 스크립트 (35초, 선택적)
> "저온 특성 한 가지만 짚고 가겠습니다. 만약 clean-cell Ea 값을 그대로 믿으면 290 K 부근에서 두 직선이 교차해서 '심부 저온에서는 LPSCl이 역전한다'는 예측이 나옵니다. 하지만 방금 보신 matched-disorder 결과처럼 Ea가 같다면 교차 자체가 없고, modelc가 전 온도에서 빠릅니다. 실험이 RT에서 modelc 2배 우세를 보이는 건 후자와 더 정합합니다. 지금 진행 중인 4 f.u. 검증이 끝나면 어느 쪽인지 확정해서 보고하겠습니다."

### 노트
- 시나리오 B 채택 시 이 슬라이드는 "교차 없음 — vacancy 우위는 전 온도" 한 줄로 축소, SI로 이동 가능

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

## 1H-1. Slide 8a — Shear Mode Lock-in (mechanism 시각화)

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

## 1H-2. Slide 8b — Cross-Check & Referee Defense

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
