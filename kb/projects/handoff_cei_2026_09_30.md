---
title: "CEI (Nd 계면) 인계 카드 — 실험 쪽 1저자에게 작업 양도 (2026-09-30)"
date: 2026-09-30
updated: 2026-09-30
tags: [handoff, cei, nd, cathode-interface, lpscl, mp-hull, band-gap]
status: 발송 대기 — 사용자가 zip 으로 전달한다
confidence: medium
verificationStatus: verified
verifiedAt: 2026-09-30
verifiedBy: self
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: multi-source-primary
---


# CEI (Nd 계면) 인계 카드 — 실험 쪽 1저자에게 작업 양도

> 이 카드는 **작업을 넘겨받는 쪽**을 위한 것이에요. 처음 읽는다면 먼저
> `kb/projects/cei_reading_guide_2026_09_30.md`(읽기 지침서)를 보세요 — 개념부터 한 단계씩 풀어 둔 문서예요.
> AI 에게 설명을 맡기려면 `kb/projects/cei_explainer_prompt_2026_09_30.md` 의 프롬프트를 붙여 넣으면 돼요.
> 기준 커밋: 브랜치 `claude/friendly-meitner-lldvar` · 이 카드가 들어간 커밋(zip 의 `MANIFEST.sha256` 머리에 적힘).

## 0. 한 줄 상태

Nd(+O) 를 넣은 황화물 고체전해질 LPSCl₁.₆ 이 **고전압 양극과 닿을 때 무엇이 생기는지**를 계산으로 따졌어요.
**전압창을 넓히지는 않고**(오히려 산화 개시 2.14 → 1.92 V 쪽), 대신 **분해 산물을 바꿔요** —
풀려난 P 의 일부(목표 조성 x = 0.02 에서 최대 1 할)가 양극 금속 인산염 대신 **Nd 인산염**으로 가요.
그 산물 10 종은 우리 DFT 로 전부 **넓은 갭 절연체**(PBE 2.26–5.99 eV)예요. 모든 계산은 0 K 열역학이에요.

## 1. 무엇을 넘기나

| 무엇 | 어디 |
|---|---|
| **읽는 화면 (송부판)** | 비공개 링크 https://claude.ai/artifact/8cxFDQ2jFcBRppF9Hu1SZ4 — 사용자가 Share 로 공유해야 열려요 |
| 같은 화면의 정본 (작업 기록 포함) | `db/properties/cei_figs/index.html` (그림 9 장이 같은 폴더) — 브라우저로 바로 열려요 |
| 그림 · Origin 용 CSV | `db/properties/cei_figs/*.png · *.csv` (열 이름 명시) |
| 숫자의 원자료 (원장) | `db/properties/*.json · *.jsonl` — 화면의 모든 숫자는 여기서 옮긴 것이에요 |
| 원고 틀 (논지 · 그림 순서 · 반론 8 개) | `kb/syntheses/cei_nd_manuscript_framing_2026_09_18.md` — **1저자 검토 전** |
| 그림 생성기 · 계산 도구 | `tools/figures/plot_cei_*.py` · `tools/oxidation/interface_reactivity_v2.py` · `esw_grand_potential.py` |
| 이전 인계 카드 (09-16 시작 당시) | `kb/projects/handoff_2026_09_16_cathode_cei.md` |

## 2. 결론과 근거 (이대로만 말해요)

| # | 말할 수 있는 것 | 근거 (화면 절 · 원자료) |
|---|---|---|
| 1 | Nd 는 전압창을 넓히지 않는다 — 산화 개시가 2.14 → 1.92 V 쪽이고 x 와 무관하다. **0.22 V 는 정량 인용하지 않는다**(hull 오차 크기) | §0 · `cei_esw_Li_x002_2026_09_28.json` |
| 2 | 고전압에서 P 가 들어갈 “Li 안 쓰는 방”을 무도핑은 **양극 전이금속 인산염**(CoP₄O₁₁ · Ni(PO₃)₂ …)으로, Nd 계는 **Nd 인산염**(NdP₅O₁₄ 등)으로 먼저 채운다 | §2 Fig. 1·2 · `cei_x002_result_2026_09_28.json` §2 |
| 3 | 그 몫은 **Nd 수가 정한다** — x = 0.02 에서 P 의 최대 1 할(Co·Ni·NMC811 양극). LiMnO₂ 는 Nd 가 NdCl₃ 로 가서 0 % | §2 표 · §2b |
| 4 | 보호율(양극 금속이 인산염으로 덜 끌려가는 몫) 예측식 min(1, k·x/(1−x)) 은 견줄 수 있는 11 열 중 **셋**에서만 잘 맞는다. x = 0.02 는 LiCoO₂ 4.3 V 10.3 % · 잴 수 있는 16 칸 전체 −3~12 % | §2b Fig. 3 · `cei_nd_protection_allcells.csv` · `cei_protection_allcells_result_2026_09_21.json` |
| 5 | 인산염을 면한 양극 금속은 반응에서 빠지지 않는다 — **94 % 가 황화물**이 된다. “양극이 덜 녹는다” 가 아니다 | §2b ‘쉽게 다시 읽기’ ① · §9 |
| 6 | 판별 산물 10 종 전부 넓은 갭 절연체 (PBE 2.26–5.99 eV) — 절연성의 **필요조건**이지 부동태 증명이 아니다. NdP₅O₁₄ 의 ‘−0.943’ 은 r2SCAN 참조와 비교한 차이였다(같은 구조 GGA 참조와 +0.003 · 개정 비준 대기) | §6 · `cei_gap_results_2026_09_19.json` · `cei_gap_ndp5o14_reference_check_2026_09_30.json` |
| 7 | 치환 **자리**가 부호를 정한다 — Li 자리 +(덜 반응) · P 자리 −(더 반응). x = 0.02 에서는 크기가 유의폭 안이라 **부호만** | 페이지 머리 표 · §S1 · `cei_site_concentration_result_2026_09_19.json` |
| 8 | Nd 는 3 가 도펀트 중 특출나지 않다 — 기전은 3 가 양이온 일반, Nd 는 대표 시연 | §5 · `trivalent_dopant_screen_verdict_2026_09_16.json` |

**철회된 것 (다시 꺼내지 않는다)**: “NdPO₄ 가 Li₃PO₄ 보다 깊은 P 싱크” (+1.5035 eV/P 로 양수) ·
“Δ 반응에너지가 전압과 함께 6.6 배” (Li 장부) · “O/P 응축도 하나로 정렬” · PDOS 셀 이름표 ‘Li 자리 x = 0.20’ (09-30 정정 — 실제는 n5fu · P 자리 x = 0.40 · 66 원자).
전체 금지 서술 34 개는 화면 §9 에 있어요.

## 3. 열린 일 — 우선순위 순

1. **NdP₅O₁₄ 갭 ‘미재현’ — 원인 확인됨, 인용 조건 개정만 비준 대기** —
   09-30 MP 조회로 풀렸어요. MP 에 NdP₅O₁₄ 가 **두 엔트리**(P2₁/c `mp-4736` 갭 5.39 · Pmna `mp-560681`=`mp-aaabfxkr` 갭 6.336)로 있고,
   StructureMatcher 로 보면 **둘 다 우리 구조와 같은 구조**예요. 표적으로 쓴 Pmna 의 6.336 은 **r2SCAN 구조최적화**(task mp-2743338)의 갭이고,
   P2₁/c 의 5.39 는 **GGA 밴드 계산**(task mp-717219)이에요 — 우리 PBE 5.393 은 같은 근사(GGA) 참조와 **+0.003 eV** 로 재현돼요.
   (task 짝은 MP 새 ID 가 옛 번호의 26 진 표기라는 규칙으로 확정했어요 — 알려진 짝 둘로 검산.)
   기록 `db/properties/cei_gap_ndp5o14_reference_check_2026_09_30.json` · 개정안 `D-2026-09-30-cei-ndp5o14-reference-mismatch`(**proposed**) ·
   인용위험 항목에는 원인 주석만 달았어요(level CONDITIONAL 그대로). 화면 §6·머리·§9 는 “비준 대기” 상태로 이미 고쳤어요.
   **다음 걸음**: 누가 비준할지 정하고(인계 중이라 사용자 또는 1저자) → 비준하면 ① 인용위험 조건 문구 교체 ② 화면 `[미재현]` 표식 교체
   ③ 결속 시험(`test_ndp5o14_reference_mismatch_is_recorded_and_state_consistent` 가 비준 전후 상태를 강제해요) ④ 송부판 같은 링크에 재게시.
   ⚠ 사전등록 예측(6.33–6.46)이 틀렸다는 기록과 9 종 집계는 **그대로** 둬요 — 예측의 기준값이 r2SCAN 이었다는 원인만 덧붙였어요.
2. **갭 축 판정 G2/G3 의 등록** — 결과 뒤 산수로는 “Nd 판별종 최소 갭이 P₂O₅ 보다 0.30 eV 이상 작다”(상대적으로 좁을 뿐, 4.34 eV 는 넓은 갭)이고,
   등록된 G3 문구대로면 갭 축에서는 ‘상쇄 가설’ 쪽이에요. 아직 결정 원장에 없어서 **인용하지 않아요** (§6 카드).
3. **x = 0.05 를 검토할지** — 식이 맞는 LiCoO₂ 4.3 V 열에서만 “0.02 → 0.05 면 보호 2.6 배 · 조성식 Li +0.06” 이에요. 돌린다면 x = 0.02 때처럼 **게이트를 결과 전에 등록**하고 시작해요 (`cathode_cei_x002_amendment_2026_09_28.json` 이 선례).
4. **이온전도도 반론(§8b ④)은 아직 반박 못 함** — BVSE 는 중간에 세웠어요(`bvse_nd_doping_2026_09_18.json` · paused · 인용 금지). 구조는 Li 자리 x = 0.20 셀뿐이에요.
5. **목표 조성의 구조 계산(PDOS·BVSE)** — x = 0.02 셀은 약 618 원자라 우리 기계(단일 GPU 48 GB)로 못 돌려요. 있는 것은 PDOS 용 n5fu(P 자리 x = 0.40 · 66 원자)와 BVSE 용 Li 자리 x = 0.20(120 원자)뿐이에요.
6. **보호율 곡선의 단조성 게이트** — 단조롭지 않은 열 셋(LiMnO₂ 3.0 V 등)을 걸러낼 규칙은 **다음 라운드 사전등록 후보**로만 적혀 있어요.
7. **x = 0.20 의 Li 맞춤 가산성**은 안 쟀어요 (필요할 때만).
8. **전압창 도구의 환원 한계 규칙** — 인용위험 `HZ-esw-reduction-limit-label` (CONDITIONAL). 화면은 올바른 1.717 V 를 써요. 도구 자체 수정은 계산 쪽 일이에요.
9. **Fig. 7 그림 파일** — 패널 (b) 제목 “Sulfates are worse than every phosphate” 는 10 종 안에서만 맞아요. 캡션은 고쳤고, 원고에 쓸 땐 그림을 다시 뽑아야 해요.

## 4. 결정 원장 · 인용위험 (CEI 몫)

결정은 `db/governance/decisions.json` 에 있어요. **active 만 유효**하고 proposed 는 아직 판정이 아니에요.
⚠ 09-17~29 의 CEI 결정은 **계산 담당(사용자)** 이 내렸어요 — 원장에 “1저자” 로 적힌 것도 그 뜻이에요(비준된 항목은 봉인이라 안 고쳤어요). 앞으로는 1저자가 결정해요.

| 결정 | 상태 | 한 줄 |
|---|---|---|
| D-2026-09-16-cathode-cei-decomposition | active | 전압별 분해 산물과 전자 부동태화 — 보고량 정의 |
| D-2026-09-16-cei-dopant-decomposition-amendment | active | 대조 조성 둘로 Nd·O 효과를 가른다 |
| D-2026-09-16-cathode-cei-gap-target | active | 갭 대상 = 판별종 10 종 (전이금속 상 제외) |
| D-2026-09-16-trivalent-dopant-phosphate-screen | active | 3 가 도펀트 스크리닝 (게이트 B < 0) |
| D-2026-09-17-cei-p-host-li-ladder | proposed | P 수용상 Li:P 사다리 (사후 관찰) |
| D-2026-09-17-cei-tm-phosphate-exchange | proposed | Nd 는 Li 인산염에 지고 전이금속 인산염을 이긴다 |
| D-2026-09-17-pairwise-exchange-resolution-limit | proposed | 2 상 교환으로 hull 의 선택을 예측하지 않는다 |
| D-2026-09-19-cei-site-vs-concentration | active | 치환 자리와 농도를 갈라 본다 (부호는 자리) |
| D-2026-09-28-cei-page-x002 | active | 화면 조성을 x = 0.02 로 옮긴다 |
| D-2026-09-28-cei-x002-result | active | x = 0.02 결과 확정 (G4 는 ‘위반 9 · 반올림으로 원인 규명’) |
| D-2026-09-28-cei-li-ledger-identity | active | 전압 기울기 = 방출 Li — 계산 구성의 항등식 |
| D-2026-09-28-cei-x010-curvature | active | x = 0.10 도 0.02–0.20 직선 위 |
| D-2026-09-29-cei-limatched-additivity | active | Li 를 맞춰도 Nd·O 효과가 더해진다 |
| D-2026-09-30-cei-ndp5o14-reference-mismatch | **proposed** | NdP₅O₁₄ ‘미재현’ 원인 = 참조 계산 종류 불일치 — 비준하면 인용 조건 교체 |

인용위험(`db/properties/citation_hazards.json`) 중 CEI 에 걸리는 것: `HZ-cei-gap-ndp5o14-unreproduced`(CONDITIONAL — 위 열린 일 1) ·
`HZ-esw-reduction-limit-label` · `HZ-esw-reduction-limit-facet-convention`(CONDITIONAL) · `HZ-dualcompat-op-single-axis-retracted`(SUPERSEDED) ·
`HZ-dualcompat-open-endpoint-degenerate`(BLOCKED) · `HZ-dualcompat-n4-permutation-p`(CONDITIONAL) · `HZ-nd-gap-mp-summoned`(CONDITIONAL).
두 원장 파일 자체는 다른 트랙 기록이 섞여 있어 zip 에는 안 넣었어요 — 필요하면 사용자에게 받으세요.

## 5. 재현하는 법

- 환경: Python 3.11 · `mp_api` · `pymatgen` · Materials Project API 키(환경변수 `MP_API_KEY`).
  ⚠ MP 데이터베이스 판이 바뀌면 끝자리가 달라질 수 있어요 — 우리 값은 원자료 JSON 에 반응식과 같이 남아 있어요.
- 최소 명령 셋(계면 반응 · 전압창 · 참조 갭)은 화면 방법 절 **“MP 에서 직접 뽑는 법”** 에 그대로 있어요.
- 그림 다시 뽑기 (zip 최상위에서 — 폴더 구조가 repo 와 같아서 상대경로가 그대로 맞아요):
  - `python3 tools/figures/plot_cei_nd_o_decomposition.py --series x002` → Fig. 1 · S1 · 4–8 + CSV (출력은 `/tmp/claude-0/cei_fig/x002/`, `--out` 으로 바꿔요)
  - `python3 tools/figures/plot_cei_p_host_ladder.py --rec db/properties/cei_p_host_ladder_x002_2026_09_28.json --nd_bearing ndo_li_002,nd_p_002_asused` → Fig. 2
  - `python3 tools/figures/plot_cei_nd_protection.py` → Fig. 3
- 원자료를 새로 뽑는 계산(`interface_reactivity_v2.py`)은 MP 에서 엔트리를 받아 hull 을 푸는 데 몇 분이면 돼요(CPU).

## 6. 이 작업의 규칙 (이어서 할 때)

1. **결과를 보기 전에 판정 기준을 적어 둔다** (사전등록 JSON 을 먼저 커밋). 결과를 보고 문턱을 옮기지 않아요 — 틀린 예측은 틀렸다고 남겨요.
2. **화면의 숫자는 원자료에서만** 와요. 화면이 숫자를 따로 보관하지 않아요.
3. **절대값을 다른 논문 값과 나란히 놓지 않는다** — MP 보정 눈금이 산화물(+U)·황화물(GGA) 혼합이라 우리 계들끼리의 차이(Δ)만 써요.
4. x = 0.02 의 계면 Δ 크기는 유의폭(±0.010 eV/atom) 안이라 **부호만** 써요.
5. **0 K 열역학**이에요 — “생기고 싶어 한다” 까지이지 속도 · 두께 · 연속성은 말하지 않아요.
6. 새 서술을 쓰기 전에 **§9 금지 서술 34 개**를 한 번 봐요.

## 7. 역할

- 이 트랙의 1저자는 **실험 쪽**이에요. 계산 담당(사용자)은 09-30 까지의 계산·화면을 만들었고, 그 결정들은 위 표에 있어요.
- 계산을 새로 돌려야 하는 일(열린 일 1·3·4·5)은 계산 담당과 상의해요 — 우리 기계 제약(단일 GPU 48 GB)이 걸려요.
- 원고 틀 카드의 반론 8 개와 그림 순서는 **1저자 검토 전**이에요. 검토 뒤 바뀐 것은 카드에 먼저 적고 화면을 맞춰요 (화면 §8b 는 “충돌하면 카드가 이긴다”).
