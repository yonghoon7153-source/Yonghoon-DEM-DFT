---
title: "CV 프롬프트 — CEI 쉬운 스토리 4 단계 (P 가 양극 금속을 끌어가고 Nd 가 P 를 먼저 잡는다) + 그림 여섯: 계산이 받치는 범위를 넘는가 · 확인 요청 다섯"
tags: [review, cei, nd, interface, phosphate, story, figure, manuscript, codex, prompt, letter]
letter: CV
date: 2026-10-07
track: cei
channel: codex
kind: prompt
status: 발송 대기 (사용자 2026-10-07 '쉬운 스토리 구상 해줘라')
confidence: medium
verificationStatus: verified
verifiedAt: 2026-10-07
verifiedBy: self
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = CEI → **1저자는 실험 쪽 다른 사람**이다 (사용자 = 계산 담당). 아래 스토리는 사용자가 고른 설명 순서이고 **1저자 검토 전**이다 — 이 리뷰는 1저자에게 가기 전 과잉 주장 점검이다.
> 앞선 리뷰: 회신 CM (09-30 · `kb/reviews/codex_CM_reply_cei_nd_handoff_2026_09_30.md` · NO-GO → 이행) — 그 금지(특히 P0-1 '열화 억제는 이 계산으로 말하지 않는다')가 여기서도 유효하다.
> 기준 커밋 `ac06894`. ⬇ 아래 **보내는 글**만 발송한다. 회신이 오면 `codex_CV_reply_…` 로 원문 보존.

---

**[CEI · Nd] 쉬운 스토리 4 단계 + 그림 여섯 — 실험 1저자에게 가기 전 과잉 주장 점검**

## 1. 왜 새로 썼나

실험 1저자의 두 주장 — ① 고전압에서 TM 이 인산염과 반응해 양극이 열화된다 ② Nd 함유 CEI — 에 맞춰 계산 그림을 만들었는데, TM 몫 그림을 사람들이 이해하지 못했다. 그래서 NMC811 금속별 표와 4 단계 스토리 그림으로 바꿨다. 스토리 원문: `kb/syntheses/cei_nd_manuscript_framing_2026_09_18.md` 의 '⭐ 쉬운 스토리 — 주 서술' 절 (그 아래 Thesis · 반론 · 금지는 그대로 유효).

**한 줄**: 고전압에서 전해질의 인(P)이 양극 금속을 끌어가는데, Nd 가 그 P 를 일부 먼저 가로챈다.
1. 고전압에서 전해질이 분해된다 — P 가 양극의 O 와 만나 인산염이 된다.
2. 그 인산염이 양극 금속(Ni · Mn)을 끌고 간다 — NMC811 에서 Ni 는 3.0 V 까지 전부 황화물 · 3.5 V 부터 일부 인산염 (Mn 은 늘 인산염 · Co 는 늘 황화물).
3. Nd 가 있으면 Nd 가 P 를 먼저 잡는다 — NdP₅O₁₄ 로 가져가고, 그만큼 Ni 인산염이 준다 (x = 0.02 · Li 맞춘 대조군 기준 · 효과는 작다).
4. 그 NdP₅O₁₄ 가 계면에 남는 층이 된다 — 실험 XPS 와 짝.
같이 말할 것: x = 0.02 에서 효과가 작다 (4.5 V 는 반대 부호) · 인산염을 면한 Ni 는 NiS₂ 로 간다 ⇒ '열화를 막는다' 는 말하지 않는다 · 0 K hull 산물 경로이지 속도·두께·전도가 아니다.

## 2. 근거

- 그림 도구 `tools/figures/plot_cei_tm_fate.py` (`--selftest` · 모드 기본 · `--nd` · `--simple` · `--ncm` · `--story`) → `db/properties/cei_figs/` 의 `cei_tm_fate_undoped` · `cei_tm_fate_nd2o3_x002` · `cei_tm_fate_nd_dose_4p3V` · `cei_tm_fate_simple_4p3V` · `cei_tm_fate_nmc811_by_metal` · `cei_story_p_pulls_ni_nd_takes_p` (.png + .csv).
- 원자료: 계면 반응성 v2 (`interface_reactivity_v2.tm_fate`) · x = 0.02 결과 `db/properties/cei_x002_result_2026_09_28.json` · Li 맞춘 대조군 규칙 (§2b) · 산화 onset `db/properties/cei_esw_Li_2026_09_16.json`.

## 3. 확인 요청

- **Q-CV-1 (단계마다 받치는가)** — 네 단계 각각을 계산이 실제로 받치는가? 특히 ② '인산염이 금속을 끌고 간다' 는 0 K 반응 산물의 몫이지 기전·순서가 아니다 — 문장이 순서·인과를 넘어 말하는가? ④ '계면에 남는 층' 은 계산이 말하는가, 실험 XPS 에 맡겨야 하는가?
- **Q-CV-2 (숫자 재현)** — CSV 에서 Ni 인산염 몫 (13 → 10 % · −1.4 ~ −3.2 %p · 4.5 V +0.6) 과 'Ni 는 3.0 V 까지 전부 황화물 · Mn 늘 인산염 · Co 늘 황화물' 을 원자료로 다시 낼 수 있는가? Li 맞춘 대조군 규칙이 모든 그림에 같게 쓰였는가?
- **Q-CV-3 (비유)** — "P 는 금속을 끌고 가는 손 · Nd 가 손 일부를 잡는다" 비유가 산물 재분배 이상을 암시하는가 (예: Nd 가 양극을 '보호' 한다)? 바꿀 표현이 있으면 제안해 주길 바란다.
- **Q-CV-4 (그림)** — 여섯 그림 중 원고·발표에 그대로 내보내면 오독될 것이 있는가 (축 · 라벨 · 몫의 분모 · x 값 표시 · 대조군 표시)? 실험 1저자가 볼 한 장을 고른다면 어느 것인가?
- **Q-CV-6 (청중용 한 장 — 사용자 10-07 *"고전압 안정성에 뭐가 좋냐, 왜? 이 정도만 직관적으로"* · x 는 0.02 고집 안 함)** — 우리가 그릴 계획: (a) 만화 — Nd 없음: 전해질 P 가 양극 금속을 잡아 TM 인산염 / Nd 있음: Nd 가 P 를 잡아 NdP₅O₁₄ 층 · (b) 4.3 V 용량 곡선 — TM 인산염 몫 vs x_Nd (0 · 0.02 · 0.05 · 0.10 · 0.15 · 0.20 · NMC811 굵게 · LCO·LNO 가늘게 · Li 맞춘 무-Nd 대조군 수평선 · 비교 게이트 미통과 점은 안 그림 · 실험 조성 x = 0.02 표시) · (c) 한 줄 '창은 안 넓어진다 — 분해 산물이 바뀐다'. ⚠ x = 0.20 하나만 보이면 LCO 는 0 (포화 · P 를 Nd 가 다 받음 · 09-29 정정 '포화점 착시') 이고 NMC811 은 x ≥ 0.10 에서 평탄 (Nd(PO₃)₃ 등장) 이라 둘 다 오독 위험 — 그래서 단일 x 대신 용량 곡선을 제안한다. 이 설계가 '고전압 안정성 개선' 을 계산이 받치는 것처럼 보이게 하는가 (인산염을 면한 Ni 는 NiS₂ 로 간다 · 열화 감소는 실험 몫)? 청중용 제목·캡션 한 줄을 제안해 주길 바란다.
- **Q-CV-5 (판정)** — 이 스토리를 실험 1저자에게 '계산 쪽 설명 순서 제안' 으로 보내는 것에 GO / 조건부 GO / NO-GO 와 P0 · P1 · P2 로 답해 주길 바란다.
