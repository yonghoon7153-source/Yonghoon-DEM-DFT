---
title: RQ — 앵커 대기 목록 (§F1: 앵커 없으면 훅만, 날조 금지)
created: 2026-08-11
updated: 2026-08-11
type: research-question
tags: [review, electrochem, additive]
sources: [CLAUDE.md, docs/digest_model_application_backlog.md, docs/nca_material_preset.md]
confidence: medium
explored: false
verificationStatus: unverified
author: agent
claimType: mixed
evidenceScope: multi-source-primary
anchored: assumed
scope: n-a
status: open
feedsInto: 각 항목의 배선 재개 (앵커 확보 시 해당 훅 활성화)
---

# RQ — 앵커 대기 목록

> [!question] 어떤 물리 배선이 문헌/실측 앵커 부재로 훅 상태에 멈춰 있고, 무엇이 오면 풀리는가?

## 왜 중요한가
§F1 (날조 금지) 는 값 없는 배선을 **훅**으로만 두게 한다.  대기 항목을 잃어버리면
앵커가 나타나도 배선이 재개되지 않는다 — 이 카드가 그 큐다.

## 대기 항목 (불변 목록, CLAUDE.md 2026-07-23/08-06 절)
- **Joule ΔT 앵커** — hot-spot v2 는 Eₐ-free 로 설계 (LPSCl 분해-율 Eₐ 문헌 부재를
  리서치로 확인, 날조 회피).  실측 ΔT 가 오면 맵→온도 결합.
- **코팅 √N shape 배수** — coating_presets(LNO/LZO…) 는 셀렉터만; LZO/Li₃PO₄ 배수 대기.
- **SDCP E_bind** — DFT(gabia) 대기; σ_SDCP 스윕은 완료(+0.8~+63.4 %).
- **NCA E=175 GPa** — Kang "assumed"+Koerver umbrella 로 검증이 배선 차단;
  `--cam nca` 는 σ_e 만 Amin-태그 배선 (docs/nca_material_preset.md).
- **VGCF/PTFE i0·크기 앵커류** — 첨가제 F1 잔여 (압력-형상 크기앵커 문헌 대기).
- **C_dl/R_w 실험 EIS 앵커** — v3-1 EIS/DRT 의 ASSUMED 소자.

## 가설
- H1: 각 항목은 앵커 1개(논문 표 or 실측 1점)로 풀리는 구조로 이미 배선돼 있다
  (훅 + CLI 노브) — 확보 즉시 활성화 가능.

## Evidence For / Against
- For: kim2025 R_ct(T) 앵커가 온도 i0 스케일을 실제로 활성화한 전례.
- Against: (없음)

## Status Log
- [2026-08-11] open — 목록을 위키로 승격 ([[findings-ledger]] 와 상보:
  ledger = 결함 추적, 이 카드 = 부재-앵커 추적).  새 litdb 카드가 들어올 때마다
  ([[litdb-canon]]) 이 목록과 대조할 것.
