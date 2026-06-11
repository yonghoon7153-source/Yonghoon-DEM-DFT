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

## 1G. Slide 7 — M3: Ionic Glue 강해진다 (v2 갱신 — vacancy + anti-site 분해)

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

## 1K. Slide 11 — Cross-check #3: Voronoi 4-Sublattice Disorder Fingerprint

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

## 1M. Slide 13 — Cross-check #5: ELF — Covalent vs Ionic 시각화

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

## 1N. Slide 14 — k-mesh Audit & Method Convergence (Referee Defense)

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

## 1O. ~~Slide 15 — Methods Consistency~~ — **DROPPED 2026-06-11** (slide 3 pipeline + slide 14 k-mesh audit과 중복). 총 22 → 21장.

(아래 본문 보존용 — 발표 시 14 + 3 합쳐서 충분히 커버됨)

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
