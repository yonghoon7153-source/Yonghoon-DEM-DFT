---
title: "인수인계 — 2026-09-16 세션 (양극 CEI §A–§E · 도펀트 스크리닝 · dual compatibility)"
date: 2026-09-16
updated: 2026-09-16
tags: [handoff, session, cathode, cei, nd, dopant, dual-compatibility, interface]
status: 진행
kind: project
system: cathode_cei
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-16
verifiedBy: agent
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

# 인수인계 — 2026-09-16 세션

> 이 세션은 **원격 GPU 를 한 번도 안 건드렸다.** gabia 에서 돌린 것은 전부
> **CPU·MP-API 계산**(pymatgen hull, 초 단위)이다. 탄성·G1·PP-swap 등 GPU 줄은
> 손대지 않았고 상태 그대로다 — ⏭-NOW-j / ⏭-NOW-i 를 보면 된다.
>
> 한 일은 하나다: **양극 CEI 트랙을 §A 에서 §E 까지 끌고 갔다.**

## 0. 먼저 (붙여넣기)

```bash
cd ~/Yonghoon-DEM-DFT
git fetch origin claude/friendly-meitner-lldvar
git pull origin claude/friendly-meitner-lldvar
python3 tools/kb_wiki.py lint | tail -2               # 0 errors
python3 tools/db/validate_canonical.py | tail -2      # 그래프 무결성 ✅
python3 tools/convention_check.py | tail -2           # 0 위반
python3 -c "import sys;sys.path.insert(0,'.');from webapp.canonical import validate_hazards;print(len(validate_hazards()),'건')"   # 0 건
```

세션 끝 커밋 **`7d122db6b`**. 오늘 커밋 60 개. 트리 깨끗.

## 1. 30초에 현재 상태 잡는 법

| 묻는 것 | 어디 |
|---|---|
| **지금 뭘 이어서 하나** | `kb/open_items.md` **⏭-NOW-k** (양극 CEI 가 논문 축) |
| **CEI 결과 한 장** | 아티팩트 **[보고서 v12](https://claude.ai/artifact/JpXxNZwwXt3QgB7f3jMpwo)** — §1~§9, 배경 없이 읽는 설명 포함 |
| **인용해도 되나** | `db/properties/citation_hazards.json` — 이번 세션 3 건 추가(`HZ-dualcompat-*`) |
| **어떤 판정이 섰나** | `db/governance/decisions.json` (`decision_state: active` 만) |

## 2. 이번 세션이 세운 것 — §A ~ §E

### §A·§B — 전압별 계면 반응성 (끝)
`db/properties/cei_interface_V_2026_09_16.json`. 6 조성 × 4 양극 × 6 전압.
**전 kink 를 남긴다**(종전엔 최소 하나만 남기고 버렸다) — 그래서 Richards/Ong 식
*반응에너지 vs x* 곡선이 통째로 그려진다.

### §C — Nd/O 효과 분해 (끝, 가법적)
대조 조성 둘(`nd_only` · `o_only_03`)을 추가해 축을 갈랐다.
**Nd 효과와 O 효과가 정확히 합만큼**(잔차 +0.0005, 문턱 0.010 의 1/20).
저전압은 O, 고전압은 Nd — 교차점 약 3 V.

### §D — 기전 (한 번 틀렸다가 고쳤다)
⛔ **"NdPO₄ 가 Li₃PO₄ 보다 깊은 P 싱크" 는 철회됐다** (+1.5035 eV/P, 양수).
고친 기전: **Nd 는 Li 를 안 쓰는 인산염 경로를 연다** (NdPO₄ 는 P 하나당 Li 0,
Li₃PO₄ 는 3). Li/P ≈ 1.67 에서 부호가 뒤집힌다. 밀려난 Li 의 행선지도 부호를 바꾼다
(Li₂O vs LiCl 이 2.01 eV/P).

### §E — dual compatibility (이번 세션 마지막, 신규)
cha2024 를 읽고 찾은 **"우리가 안 한 검사"** — §B 는 전해질 vs 양극만 봤는데
CEI 는 양쪽에 닿아 있다. 닫힌계 0 V 20 쌍.
- ⭐ **V_ox ↔ 전해질 적합성이 정면 충돌한다.** 4.193/0.0000 → 4.319/−0.0167 →
  4.980/−0.0388 → 5.013/−0.0434 **완전 단조**, ρ = −1, 사전등록 단측 p = 1/24 = 0.042.
- 🔴 **황산염이 계급으로 나쁘다** — Li₂SO₄ −0.0940 · Nd₂(SO₄)₃ −0.1470, 모든 인산염보다
  음수. 그런데 **Li₂SO₄ 는 §B 인구조사 1 위(65 회)** 다. 불리한 발견이다.
- **NdPS₄ 가 양쪽에서 나온다** → §C(갭) 우선순위 상향 근거. mp-id 확보돼 있다.

### 도펀트 스크리닝 (M 11 종)
`dopant_multiaxis_result_2026_09_16.json`. **여섯 축이 네 개의 다른 1등을 냈다**
(Al·La·Sc·Gd). **Nd 는 어느 축에서도 1등도 꼴등도 아니다.**
⇒ 쓸 수 있는 문장은 *"Nd 는 Gd·Y·Sc·La 와 구분되지 않는다"* 까지다.

## 3. ⛔ 이 세션이 **철회**한 것 (원장에 등록돼 있다)

원장을 믿어라 — 아래는 사람용 요약이고 충돌하면 `citation_hazards.json` 이 이긴다.

| id | level | 무엇 |
|---|---|---|
| `HZ-dualcompat-op-single-axis-retracted` | SUPERSEDED | "O/P **하나로** 전해질 반응성이 정렬된다" — Li₄P₂O₇ 가 반례 |
| `HZ-dualcompat-open-endpoint-degenerate` | BLOCKED | 열린계 dual-compat 실행 **전량** + 그 산물 목록 |
| `HZ-dualcompat-n4-permutation-p` | CONDITIONAL | ρ=−1 / p=0.042 — 허용 서술을 못박음 |

그 밖에 화면(§9 "말하면 안 되는 것")에도 실려 있다:
"6 종 동급군"(동급은 추이적이 아니다) · "Al 이 최고의 인산염 형성체"(AlCl₃ 아티팩트) ·
"Nd 가 최적의 3가 도펀트" · 축 간 상관 −0.43~+0.64 인용(n=7 임계 0.750).

## 4. ⭐ 이 세션에서 **배운 함정** (다음 사람이 다시 밟지 말 것)

1. **`--closed` 가 조용히 무시되고 있었다.** `run_batch` 안에서만 읽히는데
   `--electrolytes` 경로로 주면 오류 없이 **열린계를 돌려 놓고** 전압 쓸이를 찍었다.
   → 하드 가드 + 음성 selftest 2 건.
2. **열린계 끝점 퇴화.** 상대가 이미 산화가 끝난 안정한 상이면 최소 kink 가 x=0 으로
   가서 **전해질 자체분해를 계면 반응인 척** 내놓는다. 여섯 상대에서 숫자가 글자 그대로
   같았다. → `is_endpoint()` / `endpoint_meaning(closed)` / 인구조사 제외.
   ⚠ **닫힌계 끝점은 정상 판정**이다(상호반응 없음) — 한 깃발로 읽으면 멀쩡한 판정을 버린다.
3. **`LAB` 딕셔너리 하나를 matplotlib 과 HTML 양쪽에 썼다** → §4 표에
   `LPSCl$_{1.6}$` 가 날것으로 나갔다. 오류 없음·그림 멀쩡·**화면만 깨짐**.
   → `LAB_HTML` 분리 + 생성 HTML 에 mathtext 남으면 **쓰기 전에 죽는** assert.
4. **μ 와 V 를 섞었다.** `*_mu_eV` 키를 집어 "전부 4.5 V 미달" 로 읽을 뻔했다.
   **V = μ_ref − μ**, μ_ref = −1.9089 eV/atom.
5. **`entry_id` 가 dict 로 온다** (mp_api). `_entry_id_str()` 로 정규화.
6. **한 생성기가 두 절의 유일한 소스일 때 손으로 고치면 지워진다** —
   `plot_cei_nd_o_decomposition.py` 가 §3·§4·§5·§7 의 유일한 소스다.
   실제로 손으로 넣은 비유 박스 4 개를 재생성에서 잃었다. docstring 에 경고 박아 뒀다.
7. **n 이 작으면 상관계수를 쓰지 마라.** n=7 정확순열 임계 |ρ| ≥ 0.750,
   n=4 최소 p = 1/24, n=3 최소 p = 1/6(α=0.05 도달 불가).

## 5. 🔴 다음 사람이 할 것 — 우선순위대로

### ① **1저자 결정 — 원고를 어느 축 위에 세울 것인가** (가장 급함)
여섯 축 중 하나를 골라야 한다. 조건은 `dopant_multiaxis_result_2026_09_16.json` §8 에
축마다 적혀 있다. **내 추천은 산물 정체 축**(도펀트가 *무엇을 만드는지* 를 바꾼다) —
§E 가 그 축에 **반대쪽 제약**까지 붙여 줬기 때문이다: 양극이 원하는 상(축합)과
전해질이 원하는 상(ortho)이 같은 축의 양 끝이다.
⚠ 1저자는 2026-09-16 에 *"순위가 안 좋아도 이 기전으로 끌고 가도 되고"* 라고 했다.

### ② **§C 갭 계산 착수 — NdPO₄ 파일럿** (GPU, gabia 줄 뒤)
대상 **판별종 10 종(신규 9)**, 규칙은 `cathode_cei_gap_target_amendment_2026_09_16`
(ratified, 결과 보기 전 봉인) · 결정 `D-2026-09-16-cathode-cei-gap-target` (active).
mp-id 3 종 확보: `gap_targets_mpid_2026_09_16.json`
(Nd₂(SO₄)₃ mp-aaaabrhp · Nd₃PO₇ mp-aaacqmbf · **NdPS₄ mp-aaaaafmc**).
⚠ **밴드갭은 fixed-occupations nscf 의 VBM/CBM 만 인정** — DOS-threshold 판독 금지.
⚠ gabia GPU 줄 순서: **탄성 → Li₂S G1 15 초 시험 → Nd PP-swap vc-relax → NdPO₄**.

### ③ 오래된 미결 (이 세션이 안 건드림)
- NEB `collect_neb --merge` (kgy) → `sei_neb.json` 커밋
- 원고 v6 Figure 2e 문단 교체 + [19] 재배치
- Li₂S 4×4×4 셀수렴 — 1저자 승인은 받았고 **메모리 실측(P1)이 아직 게이트**
- cascade `want_kinks` 배선 (`interface_reactivity_v2.py:225`) — **§C 한 바퀴 뒤**.
  계획 카드 `kb/methodology/cei_model_transfer_to_cascade_2026_09_16.md`
- litdb 274 편 중 **6 편만 읽음**. 남은 이름: aykol2016 · anderson2024 · yun2023 ·
  lu2024 · kim2021

## 6. ⏰ 예약된 것 (조건이 차면 자동으로 할 일)

- **gabia 탄성이 끝나면** → b2o3 로 가기 전에 **Li₂S G1 을 15 초 시험**한다
  (1저자 지시 2026-09-15). 상세는 ⏭-NOW-j.
- **§C 가 한 바퀴 돌면** → cascade 이관(`want_kinks`) 착수. 반 바퀴에서 옮기면
  아직 안 굳은 것을 옮긴다.
- **결과를 보고 상을 더 넣지 않는다.** §E 의 2 인자 가설을 검증하려면 같은 O/P 의
  Li/Nd 쌍이 더 필요한데, **예측을 먼저 박은 새 카드** 없이는 돌리지 않는다.

## 7. 이 repo 에서 지켜지는 규율 (CLAUDE.md 요약 아님 — 이번에 실제로 물린 것들)

- **계산 전에 보고량 카드**(`kb/templates/estimand_card.md`)를 채운다. 리뷰에 보내는 건
  번들이 아니라 그 카드의 §1–3.
- **결과를 보기 전에 문턱·예측을 박는다.** 이번 §E 가 그걸로 값을 했다 —
  P1 이 반증되면서 단일 축 주장을 버리고 2 인자 구조를 찾았다.
- **새 도구엔 `--selftest`, 음성 경로 포함.** 그리고 **일부러 깨서 빨간불을 본다.**
  이번에 6 번 했고 전부 해당 시험만 빨갛게 떴다.
- **없는 값을 0 으로 그리지 않는다** (`or 0.0` → `—`).
- **화면에 안 실리면 사람은 화면을 인용한다** — 금지·철회는 카드뿐 아니라
  아티팩트 §9 와 `citation_hazards.json` **양쪽**에 싣는다. 이번에 원장 등재를
  한 번 빠뜨렸다가 마지막에 채웠다.
