---
title: "Zn ALZIB 세미나(2026-09-02) — 우리가 DFT/MD 로 기여할 수 있는 지점"
date: 2026-09-03
updated: 2026-09-03
tags: [zinc, alzib, zn-cu, preconditioning, scoping, dft, md, orca, collaboration]
status: 진행
kind: project
system: zn-aqueous
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: prescriptive
evidenceScope: single-source
---

# Zn ALZIB 기여 스코핑 — 2026-09-02 세미나 기반

> 출처: Kyungrok Do, "Pre-conditioning Strategy for Highly Reversible Anode-Less ZIBs",
> Weekly Report @BML, 2026-09-02 (PDF 는 repo 밖). 아래 §1 의 인용은 **발표자 슬라이드 문구**다.
> **이 문서는 제안(proposal)이다. 계산된 값은 하나도 없다.** 착수 전 §4 게이트를 통과해야 한다.

## 0. 계 요약 (발표 내용)

무음극(anode-less) Zn–I₂, N/P ~1. Cu 집전체 위 Zn plating/stripping 가역성이 전부.
**Pre-conditioning** = 10 mA cm⁻² · 0.1 mAh cm⁻² 로 ~500 사이클 예비 순환 → Cu 표면에
in-situ zincophilic + 부식억제 층 형성. 전해질 2 M ZnSO₄ (+ 0.2 M ZnI₂).

측정된 개선(발표자 값, 우리 db 와 섞지 않는다):
- Aurbach 평균 CE 0.5 mAh: bare 77.8 / 75.9 % → pre-cond 98.1 / 98.8 % (ZnSO₄ / +ZnI₂)
- CCD 10 mAh cm⁻²: bare 는 4C(ZnSO₄) · 2C(+ZnI₂) 에서 단락, pre-cond 는 10C 까지 안정
- OCV plateau: bare ~10 min → pre-cond ~3–4 h
- 풀셀 Cu‖AC: 1.48 mAh cm⁻², 600 cycle 75.0 % 유지

## 1. 발표자가 **스스로 미해결로 표시한** 구멍 (여기가 기여 지점)

| # | 슬라이드 문구 | 성격 |
|---|---|---|
| G1 | "The reflection near 43° cannot be unambiguously assigned to Zn owing to overlap with Cu … GI-XRD, XPS depth profiling is required to identify the layer composition" | **상 동정 미해결** |
| G2 | "For Cu substrate, formation of surface alloy layer exerted a greater influence than ZHS. **The Cu-specific mechanism was noted but not systematically investigated**" | 메커니즘 미규명 |
| G3 | "Further analysis is required to determine whether the deposited layer provides a high density of nucleation sites **and** limits direct Cu–electrolyte contact" | 이중기능 미분리 |
| G4 | "Voltage profiles during stripping and rest **suggest** the existence of Zn–Cu alloy" | 간접 추정만 |
| G5 | "I⁻-rich EDL reduces the **Marcus** charge transfer energy barrier of Zn ions" — 인용(Nano-Micro Lett. 2022 / EES 2024), 본인 검증 아님 | 전제 미검증 |
| G6 | ZnI₂ 는 bare Cu 에서 부식을 **가속**(OCV plateau 단축)하는데 pre-cond 후에는 가역성이 **더 좋다** | 모순 미해소 |
| G7 | "hexagonal flakes aligned parallel to the substrate" (ZnI₂ 첨가시) | 배향 원인 미규명 |

## 2. 우리가 낼 수 있는 계산 7개

각 항목: **묻는 질문 / 쓰는 기존 기계 / 이 계산이 못 하는 것**.

### C1. 상 지문표 — G1 직격, 최우선
- 질문: 43° 부근에 나올 수 있는 상은 무엇이고, GI-XRD 를 **어느 2θ 창**으로 찍어야 갈라지나.
- 계산: Cu · Zn · CuZn(β, CsCl) · Cu₅Zn₈(γ) · CuZn₅(ε) · CuI(γ-zincblende) · ZnO ·
  ZHS(Zn₄SO₄(OH)₆·xH₂O) 완전 이완 → 격자상수 → 분말 XRD 시뮬 → (hkl) 대조표 + Cu–Zn convex hull.
- 기계: QE-GPU(gabia/kgy) 벌크 이완 + stdlib 구조인자. 외부 VASP 할당 불필요.
- **못 하는 것**: DFT 격자상수 오차 ~1 % → 2θ 오차 ~0.3–0.4°. 그보다 가까운 중첩은 못 가른다.
  열역학 안정 ≠ 상온 수초 만에 실제로 생기는 상(속도론 없음). ZHS 는 수화수 개수가 정해져야 한다.

### C2. Zincophilicity 서술자 — G3 앞쪽 절반
- 질문: "zincophilic" 을 숫자로. Zn adatom 결합에너지 순위: Cu(111)/(100), Zn(0001),
  CuZn(110), Cu₅Zn₈, CuI(111).
- 기계: C-12 슬랩 파이프라인 그대로(기하 승계 verified-carry + local-TF/저β 믹싱).
- **못 하는 것**: 결합에너지는 **핵생성 과전압이 아니다**. η 에는 탈용매화 + 표면확산 +
  고전핵생성 장벽(계면에너지)이 들어간다. 우리가 내는 건 **순위 서술자**이지 η 값이 아니다.

### C3. HER 억제 ΔG_H* — G3 뒤쪽 절반 + G6
- 질문: pre-cond 층이 정말 HER 을 죽이나. CHE(computational hydrogen electrode) ΔG_H* 를
  같은 슬랩 집합에 대해. Cu 는 HER 이 잘 되고 Zn 은 거의 안 된다 — 층이 Cu 를 덮으면
  ΔG_H* 가 0 에서 멀어진다는 게 정량 가능한 주장이 된다.
- 기계: C2 와 **같은 슬랩**, 흡착 H 하나 추가. 그림 한 장에 C2+C3 이 같이 들어간다.
- **못 하는 것**: ΔG_H* 는 Volmer 열역학 하나뿐 — Heyrovsky/Tafel 속도론, pH, 실제 EDL 전기장,
  명시적 물 없음. 진공 슬랩 근사. 필드에서 통용되는 서술자지만 그 이상은 아니다.

### C4. 갈바닉 구동력 — 부식(OCV plateau 10 min → 3–4 h)
- 질문: Cu ‖ 도금 Zn 갈바닉 커플의 구동력을 층이 줄이나. 일함수 Φ 를 같은 슬랩 집합에서.
- **못 하는 것**: 진공 Φ 차이는 2 M ZnSO₄ 안의 부식전위가 **아니다**. 수용액 이중층이 다 바꾼다.
  경향 논증으로만 쓰고, 올리려면 암시적 용매(VASPsol / CPCM) 판을 따로 세워야 한다.

### C5. Zn²⁺ 용매화/탈용매화 — G5 직격, **우리 기계와 제일 잘 맞음**
- 질문: I⁻ 가 정말 Zn²⁺ 의 전하이동을 쉽게 하나. [Zn(H₂O)₆]²⁺ vs [Zn(H₂O)₅I]⁺ vs
  [Zn(H₂O)₅(SO₄)]⁰ · 접촉이온쌍 → 리간드 교환에너지 + Marcus 재구성에너지 λ (4점법).
- 기계: **ORCA r2SCAN-3c + CPCM** — SDCP 분자 계열에서 쓰던 그대로(desktop WSL).
- **못 하는 것**: 클러스터-연속체는 실제 EDL 이 아니다. 클러스터 λ 는 외권(outer-sphere) 추정치이고,
  금속 전극에서의 실제 전달은 단순 Marcus 가 아니라 Marcus–Hush–Chidsey(금속 상태 띠) 다.
  **비교 λ 로만** 쓰고 절대 장벽으로 쓰지 않는다.

### C6. Zn (002) 배향 — G7
- 질문: I 흡착이 Zn 표면에너지 순서를 뒤집어 (0001)/(002) 판상을 만드나.
  γ{(0001),(10-10),(10-11)} × {clean, I 흡착} → Wulff.
- **못 하는 것**: Wulff 는 평형형상, 전착은 속도론(성장속도). 흡착유도 γ 재배열 논증까지만.

### C7. MD — 맨 마지막
- (a) Zn adatom 표면확산 장벽 NEB(Cu(111) vs Zn(0001) vs 합금) → 확산律 vs 핵생성律 판별.
- (b) EDL 조성(내부층 I⁻/SO₄²⁻/H₂O 비율) — G5 의 "I⁻-rich" 를 직접 재는 유일한 길.
- **못 하는 것 / 경고**: 우리 UMA 검증 영역은 **LPSCl 계열**이다. 수계 Zn 전해질은 검증 영역 밖이고,
  Li₃N 에서 UMA 가 결정론적으로 편향됐던 선례(2026-06)가 있다. 따라서 **MLIP 단독 판정 금지 —
  MLIP 스크리닝 → DFT 앵커** 로만. (b) 는 사실상 AIMD 가 필요하고 그건 비싸다.

## 3. DFT/MD 가 **답할 수 없는 것** (먼저 말하고 들어간다)

- 왜 하필 ~500 사이클인가 — 시계가 없다. 메조스케일/속도론 영역.
- CE 절대값(77.8 → 98.1 %) — 못 낸다.
- **층이 실제로 무엇인가** — GI-XRD/XPS/TEM 이 정한다. 우리는 후보군과 그 지문만 준다.
- CCD·단락·덴드라이트 관통 — 연속체/상장(phase-field) 영역.

## 4. 착수 전 게이트 (우리 규율)

1. **estimand 카드 먼저** (`kb/templates/estimand_card.md`). Cu–Zn 표면합금은
   *조성 × 종단면 × 피복률* 이 다 자유롭다 — "합금 위 Zn 결합에너지" 는 그 셋을 선언하기 전엔
   **정의되지 않은 scalar** 다. 이게 SDCP-doped 를 여덟 번 반려시킨 그 함정이다.
   → 상태를 선언해 `X(상태)` 로 쓰거나 집계규칙(최저/앙상블/분포)을 미리 적는다.
2. **state-selection policy 를 전 계 공통으로.** 값을 맞추는 게 아니라 *정책*을 맞춘다(회신 O).
   Zn²⁺·Cu 는 둘 다 d¹⁰ 닫힌껍질이라 SDCP 같은 스핀 지옥은 없다 — 대신 **금속 smearing** 이
   그 자리를 대신한다. ISMEAR/SIGMA(또는 QE degauss)를 선언하고 T·S/atom 수렴을 게이트에 넣는다.
3. **검증 게이트를 결과 보기 전에.** 슬랩 두께·진공·k 3축 수렴을 각각 정하고 합산 예산으로.
4. `grep -rl "<양이름>" kb/` 30 초 규약 대조.

## 5. 권장 순서

**C1 → (C2+C3 한 묶음) → C6 → C5 → C7.**
C1 은 estimand 위험이 사실상 0(격자상수+구조인자)이고 상대 실험의 *다음 실험*을 바로 바꾼다 —
협업 진입점으로 가장 싸고 가장 유용하다.

## 6. 아직 안 한 것

- 계산 착수 전혀 없음. estimand 카드 미작성. `db/governance/decisions.json` 등록 없음.
- 상대(BML) 와 협업 합의 없음 — 이 문서는 **우리가 무엇을 제안할 수 있는지**의 목록이다.
- `kb/elements/Zn.json` 은 존재하나 **황화물 SE 도펀트 관점**으로만 쓰여 있다(수계 Zn 금속 음극 아님).
  수계 쪽으로 쓰려면 별도 카드가 필요하다.
