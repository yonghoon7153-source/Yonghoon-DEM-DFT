---
title: "CEI (Nd 계면) 인계 카드 — 실험 쪽 1저자에게 작업 양도 (2026-09-30)"
date: 2026-09-30
updated: 2026-09-30
tags: [handoff, cei, nd, cathode-interface, lpscl, mp-hull, band-gap]
status: 발송 대기 — 외부 리뷰 회신 CM(NO-GO) 이행판 · 사용자가 zip 으로 전달한다
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
풀려난 P 의 일부(목표 조성 x = 0.02 · 고전압 Co·Ni·NMC811 양극에서 최대 1 할)가 양극 금속 인산염 대신 **Nd 인산염**으로 가요(최종 평형 배분).
그 산물 10 종은 우리 DFT 로 전부 **넓은 갭 절연체**(PBE 2.26–5.99 eV)예요. 모든 계산은 0 K 열역학이에요.
⚠ 이건 **산물 재분배**까지예요 — 실제 양극 열화·누설·저항이 줄어드는지는 이 계산으로 판정하지 않았어요 (외부 리뷰 회신 CM · 09-30).

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
| 2 | 고전압에서 P 가 들어갈 “Li 안 쓰는 방”을 무도핑은 **양극 전이금속 인산염**(CoP₄O₁₁ · Ni(PO₃)₂ …)으로 채우고, Nd 계는 그 일부를 **Nd 인산염**(NdP₅O₁₄ 등)으로 채운다 — 최종 평형 배분이지 순서·속도가 아니다 | §2 Fig. 1·2 · `cei_x002_result_2026_09_28.json` §2 |
| 3 | 그 몫은 **Nd 수가 정한다** — x = 0.02 에서 P 의 최대 1 할(Co·Ni·NMC811 양극). LiMnO₂ 는 Nd 가 NdCl₃ 로 가서 0 %. 나머지 P 는 **4 V 이상에서** 양극 TM 인산염(LiCoO₂ 4.3 V: 10 % 대 90 %), **3 V 이하에서는 주로 Li 인산염**이라 10 : 90 을 일반화하지 않는다 | §2 표 · §2b |
| 4 | 보호율(양극 금속이 인산염으로 덜 끌려가는 몫) 예측식 min(1, k·x/(1−x)) 은 견줄 수 있는 11 열 중 **셋**에서만 잘 맞는다. x = 0.02 는 LiCoO₂ 4.3 V 10.3 % · 잴 수 있는 16 칸 전체 −3~12 % | §2b Fig. 3 · `cei_nd_protection_allcells.csv` · `cei_protection_allcells_result_2026_09_21.json` |
| 5 | 인산염을 면한 양극 금속은 반응에서 빠지지 않는다 — 보호율이 정의되고 게이트를 통과한 72 조건에서, 정규화된 TM 인산염 감소분의 합에 대한 TM 황화물 증가분의 합의 비가 **약 94 %** 다(합산 비 · 한 조건의 전환율 아님). “양극이 덜 녹는다” 가 아니다 | §2b ‘쉽게 다시 읽기’ ① · §9 |
| 6 | 판별 산물 10 종 전부 넓은 갭 절연체 (PBE 2.26–5.99 eV) — 절연성의 **필요조건**이지 부동태 증명이 아니다(반대로 작은 갭 하나로 누설을 판정하지도 않는다). NdP₅O₁₄ 는 등록 예측이 틀렸다(−0.943) — 비교한 MP 값이 r2SCAN 이라 같은 근사 비교가 아니었음은 확인, 유사 구조 GGA 참조와의 +0.003 은 **보조 비교**(원인 분해·동일 조건 재현 아님 · 인용 조건 개정 09-30 비준) | §6 · `cei_gap_results_2026_09_19.json` · `cei_gap_ndp5o14_reference_check_2026_09_30.json` |
| 7 | 치환 **자리**가 계산된 Δ 의 부호를 정한다 — Li 자리 + · P 자리 −. x = 0.02 는 평균 크기가 구분폭(±0.010) 안이라 크기를 인용하지 않고, 부호도 해소된 ‘덜/더 반응’ 이나 순위로 읽지 않는다(칸별: Li 23/23 + · P 18/22 − · 2.5 V 네 칸 +). 띠 밖인 x = 0.10 · 0.20 에서는 같은 부호가 해소된다 | 페이지 머리 표 · §S1 · `cei_site_concentration_result_2026_09_19.json` |
| 8 | Nd 는 3 가 도펀트 중 특출나지 않다 — 기전은 3 가 양이온 일반, Nd 는 대표 시연 | §5 · `trivalent_dopant_screen_verdict_2026_09_16.json` |

**철회된 것 (다시 꺼내지 않는다)**: “NdPO₄ 가 Li₃PO₄ 보다 깊은 P 싱크” (+1.5035 eV/P 로 양수) ·
“Δ 반응에너지가 전압과 함께 6.6 배” (Li 장부) · “O/P 응축도 하나로 정렬” · PDOS 셀 이름표 ‘Li 자리 x = 0.20’ (09-30 정정 — 실제는 n5fu · P 자리 x = 0.40 · 66 원자) ·
“Nd₂S₃(MP 0.76 eV)가 산화 쪽 산물이라 전자가 샌다 · 부동태가 아니다” (09-30 정정 — Nd₂S₃ 는 중성 조합의 상이고 산화 개시 쪽 Nd 상은 Nd₁₀S₁₉ · 갭 하나로 누설 판정 안 함) ·
“고전압 양극 계면 열화 억제” (09-30 — 계산은 산물 재분배까지 · 부제·원고 문구 교체).
전체 금지 서술 36 개는 화면 §9 에 있어요.

## 3. 열린 일 — 우선순위 순

1. **NdP₅O₁₄ 갭 ‘미재현’ — 참조 불일치는 확인 · 인용 조건 개정은 09-30 비준 · 원인 분해는 아직(선택)** —
   09-30 MP 조회로 **비교 참조가 같은 근사가 아니었다**는 것까지 확인했어요. MP 에 NdP₅O₁₄ 가 **두 엔트리**(P2₁/c `mp-4736` 갭 5.39 · Pmna `mp-560681`=`mp-aaabfxkr` 갭 6.336)로 있고,
   표적으로 쓴 Pmna 의 6.336 은 **r2SCAN 구조최적화**(task mp-2743338)의 갭, P2₁/c 의 5.39 는 **GGA 밴드 계산**(task mp-717219)이에요.
   기본 StructureMatcher 는 우리 구조를 **두 엔트리 모두와 유사**하다고 판정하지만, 이 검사는 부피를 맞춘 뒤(scale = True) 허용오차 안의 유사성만 봐요 —
   같은 셀·좌표·전자구조를 보증하지 않아요. 그래서 우리 PBE 5.393 과 그 GGA 값의 **+0.003 eV** 는 **보조 비교**예요:
   동일 구조·조건의 재현도, −0.943 차의 원인 분해도 아니고, 부피 기여도 배제하지 않아요 (외부 리뷰 회신 CM P0-2 로 범위를 줄였어요).
   (task 짝은 MP 새 ID 가 옛 번호의 26 진 표기라는 규칙으로 확정했어요 — 알려진 짝 둘로 검산. 다른 9 종 참조의 계산 종류는 확인하지 않았어요.)
   기록 `db/properties/cei_gap_ndp5o14_reference_check_2026_09_30.json` · 개정 `D-2026-09-30-cei-ndp5o14-reference-mismatch`(**active** · 09-30 사용자 비준 · 회신 CM P0-2 범위) ·
   인용위험 조건 문구를 이 범위로 바꿨어요(level CONDITIONAL 그대로). 화면 §6·머리·§9 는 개정된 조건(두 참조 병기)과 표식 `[미재현 · 참조 불일치]` 로 바꿨어요.
   비준 뒤 할 일(① 인용위험 조건 문구 ② 화면 표식 ③ 결속 시험 — `test_ndp5o14_reference_mismatch_is_recorded_and_state_consistent` 가 비준 뒤 상태를 강제해요 ④ 송부판 재게시)은 09-30 에 끝냈어요.
   원인을 더 가르려면 같은 구조·같은 근사(GGA)의 참조가 필요해요 — 예: MP 셀 고정 재계산이나 Pmna 엔트리의 GGA 밴드 계산 (계산 담당과 상의).
   ⚠ 사전등록 예측(6.33–6.46)이 틀렸다는 기록과 9 종 집계는 **그대로** 둬요 — 예측의 기준값이 r2SCAN 이었다는 사실만 덧붙였어요.
2. **갭 축 판정 G2/G3 의 등록** — 결과 뒤 산수로는 “Nd 판별종 최소 갭이 P₂O₅ 보다 0.30 eV 이상 작다”(상대적으로 좁을 뿐, 4.34 eV 는 넓은 갭)이고,
   등록된 G3 문구대로면 갭 축에서는 ‘상쇄 가설’ 쪽이에요. 아직 결정 원장에 없어서 **인용하지 않아요** (§6 카드).
3. **x = 0.05 를 검토할지** — 식이 맞는 LiCoO₂ 4.3 V 열에서만 “0.02 → 0.05 면 보호 2.6 배 · 조성식 Li +0.06” 이에요. 돌린다면 x = 0.02 때처럼 **게이트를 결과 전에 등록**하고 시작해요 (`cathode_cei_x002_amendment_2026_09_28.json` 이 선례).
4. **이온전도도 반론(§8b ④)은 아직 반박 못 함** — BVSE 는 중간에 세웠어요(`bvse_nd_doping_2026_09_18.json` · paused · 인용 금지). 구조는 Li 자리 x = 0.20 셀뿐이에요.
5. **목표 조성의 구조 계산(PDOS·BVSE)** — 목표 조성에 대응하는 셀이 **없어요**. 정확한 정수 점유로는 최소 **1244 원자**(Li₅₄₄Nd₂P₉₈S₄₃₇O₃Cl₁₆₀ · 100 식단위)가 필요하고, 더 작은 근사 조성 셀은 아직 정의하지 않았어요
   (옛 ‘약 618 원자’ 는 Li 자리 조성식 50 식단위의 근사로 S·O 가 반정수였어요 · 실행 가능성은 시험하지 않았어요 — 우리 큰 잡의 상한은 GPU 한 장 48 GB). 있는 것은 PDOS 용 n5fu(P 자리 x = 0.40 · 66 원자)와 BVSE 용 Li 자리 x = 0.20(120 원자)뿐이에요.
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
| D-2026-09-30-cei-ndp5o14-reference-mismatch | active | NdP₅O₁₄ ‘미재현’ — 비교 참조가 r2SCAN 이라 같은 근사 비교가 아니었음(참조 불일치 확인 · 원인 분해 아님 · +0.003 은 보조 비교) — 09-30 사용자 비준 · 인용 조건 교체됨 |

인용위험(`db/properties/citation_hazards.json`) 중 CEI 에 걸리는 것: `HZ-cei-gap-ndp5o14-unreproduced`(CONDITIONAL — 위 열린 일 1) ·
`HZ-esw-reduction-limit-label` · `HZ-esw-reduction-limit-facet-convention`(CONDITIONAL) · `HZ-dualcompat-op-single-axis-retracted`(SUPERSEDED) ·
`HZ-dualcompat-open-endpoint-degenerate`(BLOCKED) · `HZ-dualcompat-n4-permutation-p`(CONDITIONAL) · `HZ-nd-gap-mp-summoned`(CONDITIONAL).
두 원장 파일 자체는 다른 트랙 기록이 섞여 있어 zip 에는 안 넣었어요 — 필요하면 사용자에게 받으세요.

## 5. 재현하는 법

- 환경: Python 3.11 · `mp_api` · `pymatgen` · Materials Project API 키(환경변수 `MP_API_KEY`).
  ⚠ MP 데이터베이스 판이 바뀌면 끝자리가 달라질 수 있어요 — 우리 값은 원자료 JSON 에 반응식과 같이 남아 있어요.
- 최소 명령 셋(계면 반응 · 전압창 · 참조 갭)은 화면 방법 절 **“MP 에서 직접 뽑는 법”** 에 그대로 있어요.
- ⛔ **페이지 HTML(`db/properties/cei_figs/index.html`)은 손편집 정본이에요.** 생성기가 내는 `sections_new.html` 은 참고용 조각이라
  정본이나 송부판을 **대체하지 않아요** — 덮으면 갭 예측 실패 기록·현행 한정 문구가 되돌아가요. 그림·CSV 만 **별도 폴더**에서 재현해 게시본과 대조해요.
- 그림 다시 뽑기 (zip 최상위에서 — 폴더 구조가 repo 와 같아서 상대경로가 그대로 맞아요). **출력은 전부 `review_output/` 아래로** 보내요 —
  생성기의 출력 이름에는 계열 꼬리(`_x002`)가 없어서, 게시 폴더(`db/properties/cei_figs/`)에 쓰면 **x = 0.20 이력 그림을 덮어요**
  (09-30 부터 두 생성기가 그 경우 멈춰요 · 외부 리뷰 회신 CM P0-7):
  - `python3 tools/figures/plot_cei_nd_o_decomposition.py --series x002 --out review_output/fig_x002` → Fig. 1 · S1 · 4–8 + CSV (+ 참고 조각 `sections_new.html`)
  - `python3 tools/figures/plot_cei_p_host_ladder.py --rec db/properties/cei_p_host_ladder_x002_2026_09_28.json --nd_bearing ndo_li_002,nd_p_002_asused --out review_output/fig2_x002` → Fig. 2
  - `mkdir -p review_output/fig3 && python3 tools/figures/plot_cei_nd_protection.py --out review_output/fig3/cei_nd_protection.png` → Fig. 3
  - 대조: 산출 `X.png · X.csv` ↔ 게시 `X_x002.png · X_x002.csv` (Fig. S1 은 `cei_nd_o_decomposition_si.png` ↔ `cei_nd_o_decomposition_x002_si.png` · Fig. 3 은 같은 이름).
    09-30 실측: 세 명령의 x002 산출이 게시본과 **바이트까지 같았어요**(matplotlib 3.11.1). 판이 다르면 PNG 는 달라질 수 있으니 CSV 로 대조해요.
    게시 파일을 새로 쓸 때만 이름을 명시해서 옮기고(`plot_cei_p_host_ladder.py` 는 `--suffix _x002`) 해시를 다시 적어요.
- 원자료를 새로 뽑는 계산(`interface_reactivity_v2.py`)은 MP 에서 엔트리를 받아 hull 을 푸는 데 몇 분이면 돼요(CPU).

## 6. 이 작업의 규칙 (이어서 할 때)

1. **결과를 보기 전에 판정 기준을 적어 둔다** (사전등록 JSON 을 먼저 커밋). 결과를 보고 문턱을 옮기지 않아요 — 틀린 예측은 틀렸다고 남겨요.
2. **화면의 숫자는 원자료에서만** 와요. 화면이 숫자를 따로 보관하지 않아요.
3. **절대값을 다른 논문 값과 나란히 놓지 않는다** — MP 보정 눈금이 산화물(+U)·황화물(GGA) 혼합이라 우리 계들끼리의 차이(Δ)만 써요.
   Δ 도 보정이 전부 상쇄된다고 보장하지는 않아요 — 반응물·산물 조합이 다르면 잔여 보정이 남을 수 있어요(크기는 재지 않았어요).
4. x = 0.02 의 계면 Δ 는 평균 크기가 구분폭(±0.010 eV/atom) 안이라 **크기를 인용하지 않아요**. 계산된 부호는 보고하되, 그걸 해소된 ‘덜/더 반응한다’ 나 순위로 바꾸지 않아요.
5. **0 K 열역학**이에요 — “생기고 싶어 한다” 까지이지 속도 · 두께 · 연속성은 말하지 않아요.
6. 새 서술을 쓰기 전에 **§9 금지 서술 36 개**를 한 번 봐요.
7. **세 층을 섞지 않아요** — ① 계산값(예: TM 인산염 분율 감소) ② 원장에 따른 판정(active 결정이 인정한 서술) ③ 실험 기전 해석(예: 열화 억제 — 이 계산이 판정하지 않은 층).
   숫자에는 파일·필드, 조건(양극·전압·농도·자리), 분모, 상태(active/proposed/철회)를 같이 붙여요.

## 7. 역할

- 이 트랙의 1저자는 **실험 쪽**이에요. 계산 담당(사용자)은 09-30 까지의 계산·화면을 만들었고, 그 결정들은 위 표에 있어요.
- 계산을 새로 돌려야 하는 일(열린 일 1·3·4·5)은 계산 담당과 상의해요 — 우리 기계 제약(단일 GPU 48 GB)이 걸려요.
- 원고 틀 카드의 반론 8 개와 그림 순서는 **1저자 검토 전**이에요. 검토 뒤 바뀐 것은 카드에 먼저 적고 화면을 맞춰요.
  단 원고 틀은 **제안**이에요 — 숫자는 원자료에서, 인용 허용 범위는 active 결정과 인용위험 조건에서 와요. 카드가 그 범위를 넓히지 못하고, proposed 나 옛 자료에 숫자가 있다는 이유로 인용이 허락되지 않아요 (09-30 · 회신 CM P1-5 — 전에는 카드와 화면이 부딪히면 카드가 우선한다고 적었어요).
