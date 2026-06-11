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

### 발표 스크립트 (65–75초)

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

---

## 3. TODO (다음 작업)

- [x] Slide 2 (Scope) — drafted 2026-06-10
- [x] Slide 3 (Pipeline schematic) — drafted 2026-06-10
- [x] Slide 4 (Headline 표) — drafted 2026-06-10 (Tier 3 post-processing 진입)
- [x] Slide 5 (M1 — 전자구조 둔감) — drafted 2026-06-10
- [x] ~~Slide 5a (sub: k-mesh incident)~~ — **DROPPED** (slide 14 audit과 중복, 총 22→21장)
- [x] Slide 6 (M2 — σ prefactor) — drafted 2026-06-10
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
