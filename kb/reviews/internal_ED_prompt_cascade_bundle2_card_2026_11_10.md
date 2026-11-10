---
title: "ED 프롬프트 (내부 반박 리뷰) — cascade 묶음 2 카드: 새 축 ④ 작동창 도펀트 행방 · ⑤ 분해 ΔV/V · ⑥ Li 쪽 산물 품질과 가중치 없는 전체 순위 (약점 순위 · 순위 벡터 Pareto 층) 가 결과 전에 잘 정의됐는가"
date: 2026-11-10
updated: 2026-11-10
tags: [review, cascade, screening, ranking, mp, internal, prompt, letter]
letter: ED
track: cascade
channel: internal
kind: prompt
status: 발송 2026-11-10 — 내부 반박 리뷰 (에이전트 · Codex 토큰 없음 · 사용자 '반박 리뷰를 에이전트 사용해서') · 회신은 `internal_ED_reply_cascade_bundle2_card_2026_11_10.md`
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = cascade (1저자 = 사용자). 묶음 1 (축 ① NCM 계면 · ② 가수분해 · ③ Li 금속 · 2026-11-05 마감) 의 재개 조건 ② 로 여는 새 묶음의 카드다. 기준 커밋 8ba25f73 (브랜치 `claude/friendly-meitner-lldvar`).
> 새 축 값은 하나도 계산하지 않았다. 도구도 아직 안 썼다 — 카드 (보고량 · 회계 · 게이트 · 순위 규칙 · 닫는 조건) 만 본다.

# 보내는 글

사용자 (cascade 1저자) 가 *"전체 다른 축으로 랭킹 뽑고 그런식으로는 안되는거야?"* · *"al2s3 al2o3 이런거에 매몰되어 있었던 생각도 들고"* 라고 했다. 그래서 91 전구체 설계를 같은 최소 kink 반응식의 새 두 열 (분해 부피 · 산물 품질) 과 우리 셀 작동창 (2.5–4.25 V vs Li) 으로 더 보고, 축 ① · ③ 과 합쳐 가중치 없는 전체 순위를 내는 카드를 썼다.

판정을 부탁한다: **GO / 조건부 GO / NO-GO — "이 카드로 도구를 쓰고 계산해도 되는가 (결과 전 정의가 충분한가)"**.

보는 범위:
- 카드 `db/properties/cascade_axes_bundle2_estimand_2026_11_10.json` · 결정 `D-2026-11-10-cascade-axes-bundle2` (proposed)
- 묶음 1: `cascade_axis_ncm_interface_estimand_2026_11_04.json` · `cascade_axis_li_anode_estimand_2026_11_04.json` · `cascade_axis_hydrolysis_estimand_2026_11_04.json` · `cascade_axes_combination_rule_2026_11_04.json` · `cascade_axes_bundle_closed_2026_11_05.json` · 판독 `cascade_axis_{ncm,li,hyd}_readout_*.json`
- 원자료 형식: `db/raw/cascade_axis_ncm_v2_2026_11_04/` · `db/raw/cascade_axis_li_2026_11_04/`
- 도구 (고칠 예정 · 지금 판): `tools/oxidation/interface_reactivity_v2.py` · `tools/oxidation/esw_grand_potential.py` · `tools/oxidation/sei_product_gaps.py` · `tools/cascade/analyze_cathode_reactivity.py` · `tools/cascade/run_axis_ncm_gabia.sh`
- 문헌 갭: `reports/황화물 분해 부피 도펀트 문헌 갭.md` (회계 넷 · 해석 충돌 · A 의 빈칸)
- 8 월 교훈: `db/properties/cascade_pareto_a3_2026_08_28.json`

특히 봐 달라:
- Q1 **축 ⑤ 회계**: SE 반응물 부피를 '호스트 아지로다이트 원자 부피 × 설계 원자 수' 로 두고, 상대 (Li0.5NiO2) 는 hull 평형 상 혼합 부피로 두는 섞인 회계가 설계 사이의 차 (δ) 를 조용히 왜곡하는가. 앵커 (호스트 + Li ΔV/V ≈ −21 % · 손 어림 · 창 −30 ~ −10 %) 가 회계 결함을 잡는가.
- Q2 **축 ④ 정의**: SE 단독 Li 열린계 8 전압에서 추적 원소 등급 → f_ins · F_win 이 pymatgen grand potential 로 잘 정의되는가 (경계 전압 처리 · 평형 상 혼합 조성의 개시). 축 ① 카드가 열린계를 버린 이유 (높은 전압에서 SE 자기 분해가 이긴다) 와 충돌하는가.
- Q3 **순위 규칙**: 동률 폭 순위 r = 1 + #(동률 폭을 넘게 나은 설계) → leximin → 순위 벡터 위 보통 지배 Pareto 층. 병리 (축 수가 늘 때 · 동률이 많을 때 · 무리 A 가 작을 때 · 모름 구간) 가 있는가. ε-지배 순환 예시 ((0,0,0) ≻ (−1.5,0.9,0.9) ≻ (−0.6,1.5,−0.5) ≻ (0,0,0) · w = 1) 가 맞는가.
- Q4 **게이트**: G3b (반응식 재현) · G4 (IQR ≥ 동률 폭) · G7 (순서대로 |ρ| < 0.8) 가 충분한가. 동률 폭 ⑤ 1 %p · ⑥ 0.01 · ④ 1/8 의 근거가 약하다는 것을 카드가 정직하게 적었는가 · 다른 선택이 필요한가.
- Q5 **맹검 · 정직성**: 축 ① · ③ 을 본 뒤 순위 규칙을 정한 것 · 1 단계 열린계 표의 Al2O3 × NCM811 줄을 본 것을 카드가 충분히 적었는가. 묶음 1 마감의 '⛔ 순위를 매겨 보려는 것은 재개 사유가 아니다' 와 이 카드가 충돌하는가.
- Q6 **금지 문장 · 닫는 조건**: 5b · 9 가 과장 (가장 좋은 도펀트 · 응력 예측 · 부동태 주장) 을 막고, 결과를 본 뒤 축 · 규칙을 더하는 길을 막는가.

회신 꼴: 판정 · P0 / P1 / P2 (무엇이 틀리는지 · 반례 · 최소 고침) · Q1–Q6 답 · 카드에 넣을 문장.
