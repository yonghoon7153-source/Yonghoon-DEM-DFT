---
title: "EL 프롬프트 (내부 반박 리뷰) — li2s-3 카드 개정 4: 큐 끝 줄 유실 인정이 '끝 줄 하나만 빠진 완료 큐' 만 받는가 (판독 보류 처리 · 결과 전)"
date: 2026-11-14
updated: 2026-11-14
tags: [review, li2s, li2s3, glass, uma, md, queue, readout, internal, prompt, letter]
letter: EL
track: li2s
channel: internal
kind: prompt
status: 작성 2026-11-14 — 내부 반박 리뷰 (개정 4 를 쓴 에이전트와 다른 독립 에이전트) · 회신은 `internal_EL_reply_li2s3_endline_ack_2026_11_14.md` · 회신 전에는 개정 4 를 활성하지 않는다
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = li2s (외부 1저자 · 위임 10-30). 기준 = 이 프롬프트가 들어간 커밋 (브랜치 `claude/evac-2026-11-12`) · 판독 도구 `tools/ionic/li2s3_stage2_readout.py` sha16 `34f2c7340a442185` (앞 판 `60a7ef3ce31d0bb2` 와의 차이가 리뷰 대상).
> 결과는 하나도 안 열었다 — 11-14 readout 은 판정 보류 기록만 썼다 (W · 갈래 · cond550 · 압력 · 수송값 없음). kgy 의 런 데이터는 이 저장소에 없다 — 아래 사실은 사용자 붙여넣기다.

# 보내는 글

li2s-3 2 단계 16 런이 kgy 의 v1 큐로 끝났다 (11-14 03:27:12). 판독 (readout) 은 판정 보류로 멈췄다 — 사유 '큐 incomplete' = 큐 로그 `stage2_kgy.log` 에 `■ 큐 끝 · PHASE ladder` 줄이 없다. 카드가 그렇게 정했고 도구는 그대로 걸었다.

kgy 확인 블록 (읽기만 · 사용자 11-14): 큐 로그 끝 줄 = 마지막 런의 큐 줄 `[2026-11-14 03:27:12] ✅ B seed12 T750 끝 · 5.0242 h · 누적 82.1650 / 160 h` (그 앞 두 줄은 러너 줄 `✅ T750 seed12 끝 (rc 0)` · `■ 큐 끝 · 750:12:400`) · 줄 수 사다리 시작 1 · `■ 큐 끝 · PHASE ladder` 0 · 큐 ✅ 16 · 장부 `cost_ledger.tsv` 16 행 · rc 0 16 · 큐 잠금 풀림 · 마지막 수정 시각 로그 03:27:12.677 · 장부 03:27:12.673 · 보류 기록: 큐 incomplete · 큐 문제 [] · valid 아닌 런 0.

원인 판단 (증명 아님): 큐 실행기 `db/inputs/li2s3_dense_ensemble_2026_11_10/run_stage2_kgy.sh` 끝 두 줄 (`say "■ 큐 끝 · PHASE $PHASE · 누적 … h"` → `exit 0`) 의 출력은 `exec > >(tee -a stage2_kgy.log)` 로만 파일에 간다 · tmux 창이 닫히며 tee 가 끝 줄을 못 쓴 것으로 본다.

고친 것 (카드 개정 4 · 결과 전 · 결정 `D-2026-11-14-li2s3-queue-endline-lost-ack` proposed): 끝 줄이 없을 때 카드 판독 허가 안의 `큐_끝_줄_유실_인정` {결정 · by · 근거 · 사다리_블록_마지막_줄 · 사다리_블록_sha256 · 장부_sha256} 과 대조해 그 줄을 사다리 블록 끝으로 받는다 — `queue_record` → `endline_ack_check` (마지막 줄 한 번 · 블록 · 장부 sha256 · 마지막 줄 = 명단 마지막 런 ✅ · 블록 ✅ = 명단 · 장부 = 명단 · rc 0 · prod · 시간 · 잠금) · `permit_problems` (필드 여섯) · `_gate` (결정 active) · 출력 `queue.end_line` · `decisions` · 읽기만 하는 `endline_facts` 하위 명령. 판정 규칙 · 명단 · W 정의는 안 바꿨다. 로그 · 장부는 안 고친다.

시험: selftest 179/179 (앞 판 162 + 새 17) · 새 검사 하나씩 끈 변이 17 개 모두 빨강 · 첫 ✘ 가 그 검사를 겨눈 시험 17/17.

판정을 부탁한다: **GO / 조건부 GO / NO-GO — "개정 4 인정으로 이 16 런을 판독해도 되는가 · 인정이 받으면 안 되는 상태를 받지 않는가"**.

보는 범위:
- 판독 도구 `tools/ionic/li2s3_stage2_readout.py` (`git diff 538380aba -- tools/ionic/li2s3_stage2_readout.py` 가 이번 변경 전부)
- v1 큐 `run_stage2_kgy.sh` (안 바뀜 · 끝 줄 · 장부 · ✅ 줄의 꼴 · 돌림 순서)
- 카드 `db/properties/lpscl_glass_dense_protocol_ensemble_estimand_2026_11_10.json` (`판독_허가_2단계` · `개정_DZ_회신_2026_11_10` 사후_검증_v1_런 · **`개정_4_큐_끝_줄_유실_2026_11_14`**)
- 결정 `D-2026-11-14-li2s3-queue-endline-lost-ack` (proposed) · 런로그 `판독_보류_2026_11_14`

특히 봐 달라:
- Q1 **받는 꼴이 충분히 좁은가** — 인정이 받으면 안 되는데 받는 상태 (반례) 를 찾아 달라. 예: 큐가 중간에 멈춘 뒤 사람이 장부 · 로그를 맞춰 놓은 경우 · 큐를 두 번 띄운 경우 · 마지막 런이 rc ≠ 0 인데 큐가 다른 길로 끝난 경우 · 명단과 다른 순서 · 같은 (계, 시드, T) 두 번.
- Q2 **지문 결속** — 블록 · 장부 sha256 이 '인정 뒤에 파일이 바뀐 경우' 와 '인정이 다른 기지 (BASE) 의 파일에 쓰인 경우' 를 잡는가. 블록 정의 (splitlines · '\n' 이음) 가 CR · 끝 줄바꿈 · NUL 로 흔들리는가.
- Q3 **문지기 · 기록** — 결정 active (`_gate`) · 필드 (`permit_problems`) · 출력 기록이 readout · pressure 둘 다에 걸리는가. verify (문지기 없음) 가 인정을 정보로만 찍는 것이 맞는가.
- Q4 **다른 경로를 넓혔나** — 끝 줄이 있는 정상 경로 · v2 섞인 판독 (`ready_state`) · cond550 동결 · 보류 기록 · 대조 잡에 영향이 없는가.
- Q5 **시험** — selftest 를 돌리고, 일부러 깨 보고, 빠진 음성 시험을 적어 달라.
- Q6 카드에 넣을 문장 (허용 · 금지).

범위: 저장소 파일은 고치지 않는다 (재현은 임시 폴더) · 수송값을 계산하거나 읽지 않는다. 회신 꼴: 판정 · P0 / P1 / P2 (무엇이 틀리는지 · 재현 · 최소 고침) · Q1–Q6 답 · 카드에 넣을 문장.
