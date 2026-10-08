---
title: "CU 프롬프트 — P1b Ag(111)|흑연 3층 W_sep 마감 교체 (k9 넷 · 사전 규칙 REPLACE) 사후 감사: DEM 이 Ag–C 기본값으로 채택한 뒤 · 다음 DEM 편지 전 · 확인 요청 다섯"
tags: [review, wad, adhesion, agc, graphite, k-convergence, closure, dem, codex, prompt, letter]
letter: CU
date: 2026-10-07
track: wad
channel: codex
kind: prompt
status: 발송 2026-10-08 · ✅ 회신 수령 2026-10-08 → `codex_CU_reply_wad_agc_graphite_k9_closure_2026_10_08.md` (조건부 GO · 값 유지 · P1 '기판만' 정정 · P2 라벨)
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

> 트랙 = W_ad (DEM 협업 · 1저자 = 사용자). 마감은 이미 **비준됐고** DEM 이 그 값을 받아 Ag–C 기본값으로 채택했다 — 이 편지는 **사후 감사**다. 고칠 것이 나오면 다음 DEM 편지(V5 VASP 결과와 한 번에)에 정정·라벨로 싣는다.
> ⛔ 점착 W 값은 kb 문서에 싣지 않는다 (repo 규율) — 이 편지에도 숫자를 쓰지 않는다. 값은 아래 파일에서 직접 읽어 주길 바란다.
> 기준 커밋 `ac06894`. ⬇ 아래 **보내는 글**만 발송한다. 회신이 오면 `codex_CU_reply_…` 로 원문 보존.

---

**[W_ad · P1b] Ag(111)|흑연(0001) 3층 W_sep 마감 교체 — k 수렴 사전 규칙 REPLACE · 사후 감사 요청**

## 1. 무엇이 있었나

- 모형: Ag(111)|흑연 3층 · 2×2 정합 셀 (흑연 약 +1.08 % 변형 · Ag 격자) · PBE+D3(BJ) 2체 · 고정기하 분리일 W_sep (끝점 10 Å) · registry 넷 · QE (kgy).
- 첫 마감 (10-05 · `db/properties/wad_agc_graphite_closed_2026_10_05.json` · 지금 superseded): 생산 k 6×6×1 의 registry 평균을 헤드라인으로, 대표 registry 하나의 k 탐침 (9×9×1 · 12×12×1) 결과를 라벨로 붙여 닫았다. 재개 조건 ① = registry 넷을 9×9×1 로 다시 (8 잡).
- 그 8 잡 (+ 대표 G4 k9 2 잡) 이 끝났고 (회수 `db/raw/wad_agc_graphite_2026_10_02/` · SHA256SUMS), 도구의 **사전 규칙** (`tools/wad/agc_graphite.py` `k9set_reading` — 10 잡 전부 OK 일 때만 REPLACE) 이 REPLACE 를 냈다. 레포 재집계 (`k9set_collect_repo_2026_10_06.json`) = kgy 집계.
- 새 마감 `db/properties/wad_agc_graphite_closed_2026_10_06.json` + 결정 `D-2026-10-06-wad-agc-graphite-closed-k9` (active · 옛 결정은 superseded 로 재봉인). 결과 기록 `db/properties/wad_agc_graphite_result_2026_10_05.json` 키 `b_k9_넷_결과_2026_10_06`.
- 새 마감에 덧붙인 §2b — DEM 8차 표의 Ag–C 값 (Ag(111)|그래핀 1장 · V2 · k 6×6×1) 과의 관계 문장 (같은 k 끼리 비교).
- DEM 회신 9 발송 (`kb/projects/wad_dem_reply_9_send_2026_10_06.md` §5b) → **DEM 9차 회신**: 흑연 3층 값을 Ag–C 기본값으로 채택 · SE 쌍은 별도 칸 (원문 `kb/projects/wad_dem_reply_draft_2026_09_23.md` 'DEM 9차 회신' 절).

## 2. 확인 요청

- **Q-CU-1 (규칙대로였나)** — 10-05 마감의 재개 조건 ① 과 도구의 사전 규칙이 같은 것을 말하는가? 원자료에서 10 잡 OK · registry 평균 · [min, max] · 두께 판정을 다시 내면 새 마감의 §1 과 같은가? 규칙에 없는 판단이 끼어든 곳이 있는가?
- **Q-CU-2 (라벨 범위)** — 새 마감 §2 허용 서술의 k 수렴 문장 ("대표 registry 의 12×12×1 탐침으로 확인 · 넷 각각의 12×12×1 은 재지 않았다") 이 실제로 잰 범위를 넘지 않는가? 재개 조건 ② (registry 각각 12×12×1 은 요구가 있어야 연다) 가 합리적인가?
- **Q-CU-3 (§2b 관계 문장)** — 그래핀 1장 (V2) 과 흑연 3층의 같은 k 비교가 근거 파일 (`wad_aprime_pilot_result_v2_2026_09_26.json` · 결과 기록 '같은_옆_셀' 키) 의 범위와 맞는가 (끝점마다 registry 몇 개를 비교했는지 · V2 쪽 끝점 검사 미통과 · k 축 미검증 라벨)? 차이를 '기판 두께 효과' 로 읽으면 넘는 곳이 있는가?
- **Q-CU-4 (DEM 의 쓰임)** — DEM 9차 회신의 채택 방식이 마감 §3 금지 서술 (비정합 실제 계면 · 변형 없는 흑연 · 이완 포함 G_c 로 옮기지 않는다 · 라벨 없이 인용하지 않는다) 과 충돌하는가? 다음 DEM 편지에 넣을 라벨 줄 (k 수렴 범위 · 정합 셀 · 2체) 을 한두 문장으로 제안해 주길 바란다.
- **Q-CU-5 (판정)** — 이 마감 값을 다음 DEM 편지에서도 그대로 쓰는 것에 GO / 조건부 GO / NO-GO 와 P0 · P1 · P2 로 답해 주길 바란다. 정정이 필요하면 'DEM 에 이미 간 문장' 과 '앞으로 쓸 문장' 을 나눠 적어 주길 바란다.
