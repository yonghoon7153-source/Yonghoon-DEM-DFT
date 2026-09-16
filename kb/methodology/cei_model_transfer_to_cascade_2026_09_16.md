---
title: CEI 모델을 캐스케이드로 옮기기 — 무엇이 이미 배선됐고 무엇이 안 됐나
date: 2026-09-16
updated: 2026-09-16
tags: [cascade, cei, interface, screening, methodology, plan]
status: 진행
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

# CEI 모델을 캐스케이드로 옮기기

> **1저자 지시 2026-09-16**: *"지금 발전시키고 있는 이 모델을 나중에 cascade 에도 잘
> 적용하면 좋겠다. 잘 활용해보자."* · *"잊지않게 카드로 해줘용"*

이 문서는 **계획 카드**다. 실행 기록이 아니다.
⚠ `verificationStatus: unverified` — §1·§3 의 숫자·줄번호는 2026-09-16 에 **에이전트가**
실측한 것이고(파일 행수 · `kinks` 키 부재 · `MPRestError` 재현), **사람이 확인한 기록은 없다.** 오늘(2026-09-16) 양극 CEI 캠페인에서
만든 것 중 **캐스케이드에 옮길 수 있는 것과, 옮기기 전에 알아야 할 함정**을 적는다.

---

## 1. 지금 상태 — 실측

캐스케이드는 **이미 계면 반응성을 돌린 적이 있다.** 새로 만드는 게 아니라 **고쳐 쓰는** 일이다.

| 무엇 | 실측 |
|---|---|
| 후보 원장 | `db/properties/cascade_v23_all.csv` **3,616 행** · `cascade_all_302_2026_08_25.csv` 4,126 행 |
| 계면 결과 | `cascade_interface_90.jsonl` **286 행** · `cascade_interface_li.jsonl` 90 행 · `..._baseline.jsonl` 6 행 · `..._carbon.jsonl` |
| 배치 경로 | `tools/oxidation/interface_reactivity_v2.py --batch_from` (2026-08-19 신설) · JSONL 이라 `--resume` 로 이어달리기 |
| chemsys 규율 | ⛔ **한 chemsys 에 다 넣으면 안 된다** — 90종 원소 합집합이 44개. 종마다 따로 돈다. `MAX_CHEMSYS = 9` (실측: 9원소 통과 · 10원소 `MPRestError`) |

### 🔴 이미 확인한 구멍

`interface_reactivity_v2.py:225` — **캐스케이드 배치 경로는 아직 `want_kinks` 없이
`min_rxn_grand` 를 부른다.** 즉 오늘 붙인 전 kink 기능이 **캐스케이드에는 안 배선돼 있다.**
286 행 전부 **최소 kink 산물만** 들고 있다 (`kinks` 키 부재 실측 확인).
같은 파일 `:435`(4양극 경로)만 `want_kinks=True` 다.

`:218` 닫힌계 경로(`min_rxn_closed`)는 kink 개념 자체가 없다.

---

## 2. 옮길 수 있는 것 넷

### T1. 전 kink → 산물 집합이 통째로 달라진다

CEI 에서 실측: **최소 kink 36 종 → 전 kink 97 종 (+61).** 신규에 `NiO`(444회) ·
`Ni₃(PO₄)₂`(415) · `Co₃(PO₄)₂`(372) 처럼 **출현 빈도가 압도적인 상**들이 들어왔다.
최소 kink 만 보면 그것들이 **목록에 아예 없었다.**

- **캐스케이드에서 뜻**: 286 행의 산물 목록이 **같은 방식으로 좁다.** "이 도펀트가 뭘 만드나"
  를 그 목록으로 답해 왔다면 다시 세야 한다.
- **비용**: `:225` 에 `want_kinks=True` 한 줄. ⚠ 다만 **JSONL 스키마가 커진다**(조건당
  16–18 kink). 286 행 × kink → 파일 크기와 스키마 변경이라 **결정이 필요하다.**

### T2. 판별종 — 예산의 80 %가 답을 못 주는 종에 갈 뻔했다

CEI 실측: 97 종 중 **79 종(그중 전이금속 63)이 도핑 여부와 무관하게 양쪽에 나온다.**
그 79 종의 갭을 아무리 정확히 재도 *"도핑이 도움이 되나"* 에 답을 못 한다 —
양쪽 표에 같은 숫자가 두 번 적힐 뿐이다.

- **캐스케이드에서 뜻**: 90종 × 산물 로 후속(갭·NEB)을 계획할 때 **판별종부터 가른다.**
  "한쪽에만 나오는 상" 이 훨씬 작다.
- ⚠ 캐스케이드는 도펀트가 90종이라 "한쪽" 의 정의가 CEI(둘)보다 복잡하다 —
  **기준선(무도핑) 대비**로 잡는 게 자연스럽고, 그 정의를 **먼저 선언해야** 한다.

### T3. 사전 필터 — DFT 0 회로 3가 도펀트를 거른다

`esw_grand_potential.py --reaction` 으로 **M 당 수십 초**에 인산염 싱크 축을 잰다.
2026-09-16 에 11종을 돌렸다 (`dopant_screen_<M>_2026_09_16.json`).

⛔ **다만 그 카드는 개정 중이다** — `trivalent_dopant_screen_amendment_C_gate_2026_09_16`
(proposed). 게이트를 옮기기 전에 그 개정문 비준이 먼저다.

- **캐스케이드에서 뜻**: 90종 중 3가 양이온 치환을 **후속 DFT 전에** 순위 매길 수 있다.
- ⚠ **이 필터가 재는 축은 좁다** — 격자 적합성·Li 전도도·전압 의존이 없다. **거르는 용도지
  고르는 용도가 아니다.**

### T4. 결과 보기 전 문턱 — 이게 제일 옮길 값어치가 있다

CEI 에서 이 규율이 실제로 값을 했다:
- 가법성 ±0.010 을 **먼저** 박아서 잔차 +0.0005 가 판정이 됐다 (나중에 정했으면 아무 말도 못 한다)
- §C 대상 규칙을 **갭 한 줄 돌리기 전에** 정해서, 예산 80 %를 낭비할 뻔한 걸 0 원에 막았다

---

## 3. ⛔ 옮기기 전에 알아야 할 함정 여섯 — 전부 오늘 실제로 밟았다

### H1. 독립인 줄 알았던 필터가 같은 축이었다

3가 스크리닝에서 게이트를 `B<0 ∧ C>0` 로 짰는데, 대수로 빼 보니
**A − C = ½(M₂O₃ + 3Li₂S → M₂S₃ + 3Li₂O)** 였다. A·B·C 는 *"M 이 Li₃PO₄ 한테서
P 를 뺏나"* 하나를 **밀려난 Li 의 행선지만 바꿔** 잰 것이다. 두 축을 곱해 거르는 줄 알았는데
**같은 축을 두 번 곱했다.**

> **교훈**: 필터를 둘 이상 곱하기 전에 **반응식을 빼 본다.** 숫자 없이 대수만으로 확인된다.

### H2. 선언한 문턱 안에서 순위를 매겼다

*"0.30 eV/P 미만이면 순위를 매기지 않고 동급"* 을 박아 놓고 보고에서 **"Nd 4등"** 이라고 썼다.
문턱이 없다고 선언한 정밀도를 읽은 것이다.

> **교훈**: 순위표를 낼 때 **동급 구간을 시각적으로 묶어서** 낸다. 1·2·3 으로 줄 세우면
> 읽는 사람이 문턱을 무시한다.

### H3. 부호의 뜻을 반대로 적었다 — 게이트도 selftest 도 못 잡는다

`M₂S₃ + Li₃PO₄ → MPO₄ + Li₂S` 의 ΔE>0 을 *"황화물로 안 도망간다"* 라고 적었다(반대).
**기계가 아니라 의미가 틀린 것**이라 어떤 자동 검사도 못 잡는다.

> **교훈**: 반응식을 쓸 때 *"ΔE>0 이면 **왼쪽**이 안정하고, 왼쪽은 무엇인가"* 를
> **한 줄로 풀어 적는다.** 그 한 줄이 없으면 부호가 뒤집혀도 안 보인다.

### H5. 축마다 다른 1등이 나온다 — 단일 스칼라 순위가 안 선다

2026-09-16 에 3가 도펀트 7종을 **다섯 축**으로 재 봤다
(`db/properties/dopant_multiaxis_result_2026_09_16.json`).

| 축 | 1등 |
|---|---|
| B 인산염 교환 | **Al** — ⚠ AlCl₃ 불안정성 artifact |
| MPO₄ 깊이 (E_f/P) | **La** |
| 계면 Δ | **Sc** — ⚠ M 간 폭 0.008 < ±0.010, 사실상 구분 불가 |
| M-인산염 kink 비율 | **Gd** |
| 이온 반경 적합 | **Sc** |

축 간 스피어만 상관이 **−0.43 ~ +0.64** 로 흩어지고, `MPO₄ 깊이 ↔ kink 비율` 은 **+0.00** 이다 —
**LaPO₄ 가 제일 깊은데 La 의 kink 비율이 꼴등**이다.

> **교훈**: 캐스케이드는 `li_mobility_score` 처럼 **축을 하나의 점수로 뭉치는 열**을 갖고 있다.
> 뭉치기 전에 **축 간 상관을 먼저 본다.** 상관이 없으면 그 합계는 가중치를 고르는 사람의
> 취향이지 자료의 결론이 아니다.

### H6. 플래그가 조용히 무시될 수 있다

`interface_reactivity_v2.py --closed` 는 `run_batch` 안에서만 읽힌다. `--electrolytes` 경로로
주면 **오류 없이 열린계를 돌리고** 전압 쓸이가 찍힌 그럴듯한 출력을 낸다. 2026-09-16 에 7종을
그렇게 돌렸고 **전압줄을 보고서야** 알았다. 그날 **시작을 막는 가드 + 음성 시험**을 넣었다.

> **교훈**: 캐스케이드 배치는 플래그가 많다(`--resume` · `--limit` · `--only` · `--closed`).
> 경로마다 어떤 플래그가 **읽히는지** 확인한다 — 안 읽히는 플래그는 거짓말을 한다.

### H4. 창(ESW)과 계면은 갈린다

Nd/O 카드 §5-a 실측 — *"O 치환은 열역학 창을 전혀 안 바꾼다"* 인데도 **계면 반응성에서는
O 가 이겼다.** 2026-09-16 M 치환 ESW 도 같은 신호다: Al·Sc·Y 는 산화한계를
2.32–2.36 V 로 올리는데(무도핑 2.14) Nd 계는 1.92 로 **내린다.**

> **교훈**: 캐스케이드의 `stability_axes` 와 `cathode_reactivity` 는 **다른 양**이다.
> 하나로 순위를 매기고 다른 하나를 근거로 대면 안 된다.

---

## 4. 못 하는 것 — 이 문서가 답하지 않는 것

- **언제 할지 정하지 않는다.** 필요성은 지금 **하**다 — 양극 CEI §C 가 먼저고, GPU 줄
  (탄성 → G1 → Nd PP-swap → NdPO₄ 파일럿)이 그 앞이다.
- **T1 의 스키마 변경을 결정하지 않는다.** JSONL 이 커지는 건 결정 사안이다.
- **캐스케이드 90종의 판별종 기준선**을 정하지 않는다 — 선언이 먼저다.
- **캐스케이드 결과의 옳고 그름을 보지 않는다.** 286 행을 검증한 적 없다.

---

## 5. 다시 열 조건

- 양극 CEI §C(판별종 10종 갭)가 끝나 **모델이 한 바퀴 돌았을 때**. 반 바퀴에서 옮기면
  아직 안 굳은 것을 옮긴다.
- 또는 캐스케이드 쪽에서 *"이 도펀트가 계면에서 뭘 만드나"* 를 다시 물을 때 — 그때
  `cascade_interface_90.jsonl` 의 **최소 kink 한계**(§1 🔴)를 먼저 밝힌다.

---

## 출처

- 도구: `tools/oxidation/interface_reactivity_v2.py` (`:218` 닫힌계 · `:225` 캐스케이드 배치 ·
  `:435` 4양극) · `tools/oxidation/esw_grand_potential.py` (`--reaction` · `--formation`)
- CEI 카드: `db/properties/cathode_cei_decomposition_estimand_2026_09_16.json` ·
  `cathode_cei_gap_target_amendment_2026_09_16.json` (판별종 10종) ·
  `cathode_cei_dopant_decomposition_amendment_2026_09_16.json`
- 3가 스크리닝: `trivalent_dopant_phosphate_screen_card_2026_09_16.json` +
  개정문 `trivalent_dopant_screen_amendment_C_gate_2026_09_16.json` (**proposed**)
- 캐스케이드 자료: `db/properties/cascade_v23_all.csv` · `cascade_interface_90.jsonl` ·
  `cascade_interface_li.jsonl` · `cascade_audit_interface_axes.csv`
- 화면 보고서: [CEI 계면 반응성 — Nd/O 분해와 Li 예산](https://claude.ai/artifact/JpXxNZwwXt3QgB7f3jMpwo)
  (citable: false)
- 다축 실측: `db/properties/dopant_multiaxis_result_2026_09_16.json`
- 관련 교훈 카드: `kb/methodology/silent_wrong_path_2026_09_13.md` (조용히 틀린 경로) ·
  `kb/methodology/estimand_before_running_2026_08_28.md` (보고량 먼저)
