---
title: "EE 프롬프트 (내부 반박 리뷰) — li2s-3 큐 v2 (재실행 · cond550) 와 판독 v2 경로: DZ 의 v1 반례를 막는가 · 섞인 판독 · cond550 연결 · 비용 · 정지가 결과 전에 잘 정의됐는가"
date: 2026-11-10
updated: 2026-11-10
tags: [review, li2s, li2s3, glass, uma, md, queue, internal, prompt, letter]
letter: EE
track: li2s
channel: internal
kind: prompt
status: 발송 2026-11-10 — 내부 반박 리뷰 (큐 v2 를 쓴 에이전트와 다른 독립 에이전트) · 회신은 `internal_EE_reply_li2s3_queue_v2_2026_11_10.md` · 회신 전에는 개정 3 을 활성하지 않는다
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = li2s (외부 1저자 · 위임 10-30). 기준 커밋 1d56d576 (브랜치 `claude/friendly-meitner-lldvar`).
> 2 단계 16 런이 kgy 의 v1 큐로 돈다 (끝 ≈ 11-14 새벽). 결과는 하나도 안 열었다. 첫 런 A11 600 K 는 고친 판독 도구로 verify valid 다 (수송값은 안 읽었다).

# 보내는 글

카드 (EB 문장 6) 가 정했다: 남은 런 · 재실행 · cond550 은 리뷰를 통과한 큐 v2 로만 돌리고, v2 리뷰는 16 런 판독 전에 끝낸다. 큐 v2 와 판독 v2 경로는 v1 판독 도구를 리뷰한 에이전트 (EB) 가 썼다. 그래서 다른 눈이 필요하다.

판정을 부탁한다: **GO / 조건부 GO / NO-GO — "큐 v2 로 재실행 · cond550 을 돌리고, 판독 v2 경로로 16 런 (과 그 뒤 런) 을 읽어도 되는가"**.

보는 범위:
- 큐 v2 `db/inputs/li2s3_dense_ensemble_2026_11_10/run_stage2_kgy_v2.sh` (sha16 15e787a166cbaf5e · 새 파일)
- 판독 도구 `tools/ionic/li2s3_stage2_readout.py` (180e43f5906fa04e · 0697c527 에서 v2 경로를 더한 판)
- v1 큐 `run_stage2_kgy.sh` (d930f9b2 · 돌고 있다 · 안 바뀌었다)
- MD 드라이버 `tools/ionic/disorder_ensemble_diffusion.py` · 러너 `glass_kgy_q_v2.sh`
- 카드 `db/properties/lpscl_glass_dense_protocol_ensemble_estimand_2026_11_10.json` (`기계_판독_값.stage2` · `개정_DZ_회신_2026_11_10` · `개정_EB_2026_11_10` · **`개정_3_큐_v2_2026_11_10`**)
- 결정 `D-2026-11-10-li2s3-dense-protocol-ensemble-amend3` (proposed)
- 회신 원문 `kb/reviews/codex_DZ_reply_li2s3_ensemble_definition_2026_11_10.md` (v1 큐의 P1 반례) · `internal_EB_reply_li2s3_dz_fixes_2026_11_10.md`

특히 봐 달라:
- Q1 **DZ P1 반례**: 완료 · 실패 · 건너뛰기 · 끊긴 상태 재개 · 비용 장부 우회 · 재시작으로 첫 런 한도 우회 — v2 가 이것들을 실제로 막는가. 막는다면 어떤 경로가 아직 열려 있는가.
- Q2 **런 직전 결속**: 카드 · 큐 · 드라이버 · 입력을 GPU 대기 뒤 런 직전에 다시 해시하는가. 런 폴더의 실행 기록 (`exec_v2_start/end.json`) 만으로 같은 verify 가 v1 · v2 런을 똑같은 강도로 결속하는가 (VERIFY_MAP).
- Q3 **섞인 판독**: v2 런이 하나라도 있을 때 v1 끝 줄 대신 거는 조건 (모든 런 valid · 잠금 풀림 · ack 안 된 정지 없음 · 결정 active) 이 충분한가. 재실행으로 옛 폴더를 `T<T>.superseded_<UTC>` 로 두는 처리가 같은 (계, 시드, T) 를 두 번 세거나 고른 것만 세는 길을 여는가.
- Q4 **cond550 연결**: 고정된 사다리 판독 (cond550 자격 참) 파일 + sha256 에 묶는 방식이 '결과를 보고 v2 를 고치는' 길을 막는가. 사다리 판독의 갈래를 '잠정' 으로, cond550 판독의 갈래를 '최종' 으로 두는 것이 카드 §7 (닫힘) 과 맞는가.
- Q5 **비용 · 정지 · 한도**: v1 장부를 이어 세는 160 GPU-h 상한 · 다음 런 어림 (max(0.013, 관측 최대 h/ps) × 길이) · 첫 런 한도 400 ps 당 8 h · 정지 ack · 비용 ack 가 사람이 실수로 우회할 수 있는 꼴인가.
- Q6 **카드 결속 규칙**: v2 런을 카드 sha 가 아니라 '런을 정하는 값' 으로 묶는 것이 조용히 틀릴 경로를 여는가 (판독 규칙 값이 바뀐 개정 · cond550 값).
- Q7 시험이 실제로 깨진 경우를 잡는가 — selftest 를 돌리고 (큐 57 · 판독 136), 일부러 깨 보고, 빠진 음성 시험을 적어 달라.

회신 꼴: 판정 · P0 / P1 / P2 (무엇이 틀리는지 · 재현 · 최소 고침) · Q1–Q7 답 · 카드에 넣을 문장.
