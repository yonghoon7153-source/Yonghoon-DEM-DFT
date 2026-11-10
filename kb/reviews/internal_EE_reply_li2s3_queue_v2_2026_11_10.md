---
title: "EE 회신 (내부 반박 리뷰) — li2s-3 큐 v2 · 판독 v2 경로: 조건부 GO (P0 0 · P1 3 · P2 6) — DZ 반례는 막는다 · 결과를 본 뒤 사다리 런을 다시 굴려 최종 갈래를 바꾸는 길 · 환경변수 카드 · 원장 · PHASE 로 첫 런 한도를 피하는 길이 남음"
date: 2026-11-10
updated: 2026-11-10
tags: [review, li2s, li2s3, glass, uma, md, queue, internal, reply, letter]
letter: EE
track: li2s
channel: internal
kind: reply
status: 회신 원문 (독립 리뷰 에이전트 · 2026-11-10) — 저장소 파일 안 고침 · 스텁 계산기로 실제 v1 큐 → 실제 러너 → 실제 드라이버 · 실제 v2 큐 재현 · 반영은 카드 개정 3
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = li2s (외부 1저자 · 위임 10-30). 프롬프트 `internal_EE_prompt_li2s3_queue_v2_2026_11_10.md`. 큐 v2 와 판독 v2 경로를 쓴 에이전트와 다른 에이전트가 썼다. EB 회신의 끝-끝 표는 주장으로만 보고, 내 하네스로 다시 쟀다.

# 내부 반박 리뷰 EE — li2s-3 큐 v2 와 판독 v2 경로

- **기준**: 커밋 `36d906ef` · 큐 v2 `run_stage2_kgy_v2.sh` sha16 `15e787a166cbaf5e` · 판독 `li2s3_stage2_readout.py` sha16 `180e43f5906fa04e` · v1 큐 `d930f9b209d68097`.
  - 리뷰 중 HEAD 가 `2af66f2c` → `df663eff` 로 올라갔지만 리뷰 대상 파일 (큐 · 판독 · 드라이버 · 러너 · 카드 · 원장) 은 안 바뀌었다 (`git diff 36d906ef HEAD -- <그 경로>` 빈 출력).
- **한 것**: 저장소 파일은 안 고쳤다 (`git status` 깨끗). GPU · kgy · 실제 2 단계 결과는 안 썼다.
- **재현 방법**: 스크래치의 희소 worktree (`36d906ef`) 에서 실제 v1 큐 → 실제 v1 러너 → 실제 MD 드라이버로 사다리 8 런 (600 · 650 K × 3 ps · A · B × 11 · 12) 을 만들고, 그 사본에 실제 v2 큐를 띄웠다.
  - fairchem 만 스텁 (판독 selftest 와 같은 꼴). 판독의 read_run 은 시험용 가짜 (수송 값 없음 · 게이트 경로만 본다).
  - 물리값은 의미가 없고 싣지 않는다.

---

## 1. 판정

### 조건부 GO — 지금 판 그대로는 아니다

- P0 은 없다. P1 이 셋이다. 고침은 좁다.
  - **P1-1**: 결과를 본 뒤 사다리 런을 다시 굴릴 수 있고, cond550 판독 (최종) 이 그 새 표본으로 갈래를 조용히 바꾼다. 갈래가 '축소 3 단계' → '3 단계 후보' 로 뒤집히는 것을 재현했다.
  - **P1-2**: CARD · DECISIONS 를 환경변수로 바꾸면 상한 · 첫 런 한도 · GPU 시작 문턱 · '실행 때 결정 active' 가 따라 바뀌고, 판독이 그 런을 valid 로 받는다. 지금 원장 상태 (개정 3 proposed) 그대로 재현된다.
  - **P1-3**: 첫 런 한도가 PHASE 마다다. 550 K 블록을 PHASE=rerun 으로 돌리면 한도 검사가 없다. cond550 런 하나가 실패하면 남은 550 K 런은 이 문으로만 돌 수 있다.
- 고치기 전에는:
  - 큐 v2 로 런을 띄우지 않는다 (재실행 · 남은 런 · cond550).
  - cond550 판독을 하지 않는다.
- 사다리 16 런 판독 (v1 런만) 은 v2 경로와 무관하게 선다 — v2 경로는 v1 만의 판독을 바꾸지 않는다 (판독 selftest 양성 · 내 하네스 사다리 판독 W [600, 650] · mixed False).
  - 다만 P1-1 고침이 사다리 판독 출력에 런 지문을 더한다. 그래서 사다리 판독도 고친 도구로 한 번 한다.
  - 대조 잡은 어차피 최종 도구 sha16 으로 다시 돈다 (개정 3 문장 10) — 일정 손해는 없다.
- GO 로 바뀌는 조건:
  1. P1-1 · P1-2 · P1-3 고침 + 2 절 재현을 음성 시험으로 넣기 (p1 · p2 · p4 · p8 꼴).
  2. Q7 의 초록 깨기 10 개가 빨강이 되는 시험.
  3. 고친 큐 sha16 을 카드 `stage2.queue_v2` 에 다시 고정 → 고친 도구로 대조 잡 → 허가 키 → 개정 3 활성.
  - 고친 판에 5 절 재현 스크립트를 그대로 돌려 결과가 '거부' 로 바뀌는지 보면 닫힌다고 본다.
- DZ 의 P1 반례 (실패 · 깨진 파일을 완료로 · 실행 기록 없는 건너뛰기 · 끊긴 상태 재개 · 장부 없음 · 재시작 · 실행 직전 입력 · 설정 ≠ 카드) 는 v2 가 실제로 막는다 (Q1).

---

## 2. P0 / P1 / P2

### P0 — 없음

### P1-1 — 낡은 보류 기록으로 끝난 런을 다시 굴리고, cond550 판독이 그 표본으로 최종 갈래를 낸다

**무엇이 틀리나**
- 큐 PHASE=rerun 은 보류 기록이 그 런을 invalid · incomplete 로 적었는지만 본다 (`run_stage2_kgy_v2.sh:437-451`).
  - 그 기록 뒤에 런이 끝났는지 안 본다. '이 보류 기록 뒤 런' 판정은 옛 런의 **시작** 시각만 본다 (`:812-813`). v1 폴더는 시작 기록이 없어서 늘 '앞' 이다.
  - 사다리 판독 고정 기록이 이미 있어도 막지 않는다.
- 보류 기록은 쉽게 낡는다.
  - 판독은 런이 도는 중에도 (잠금이 쥐어져 있어도) 보류 기록을 쓰고, 그 기록은 지워지지 않는다 (`li2s3_stage2_readout.py:1280-1281` · `_hold :1248`). 상태를 보려고 readout 을 한 번 치면, 도는 런과 안 띄운 런이 incomplete 로 적힌 기록이 남는다.
  - 전역 사유 (판독 `--worktree` 오타 · v1 큐 로그 꼴 문제 — P2-6) 는 모든 런을 invalid 로 적는다. RERUN 은 그 부분집합이어도 된다.
- cond550 판독은 사다리 런을 다시 읽어 W · 갈래를 새로 낸다 (`:1272` · `:1296-1303`).
  - 사다리 판독 고정 기록과 같은 런 · 같은 도구 · 같은 카드 규칙인지 안 본다. `_cond550_gate` 는 kind · status · phase · 자격만 본다 (`:1230-1238`).
  - 사다리 판독 행에는 런 지문이 없다 (행 verify = status · reasons · runner_rc · cost · trajectory · queue_version). 비교할 것이 없다.
- 같은 (계, 시드, T) 를 두 번 세지는 않는다. 옮긴 폴더도 안 읽는다 (Q3). 문제는 **어느 표본을 읽느냐** 다.

**재현 1** (`p1_stale_hold.py`)
1. B12 650 K 가 도는 중에 판독을 한 번 시도 → 보류 기록 H0 (B12_T650 incomplete · 나머지 7 valid).
   - 그 런의 러너 끝 줄과 큐 끝 줄을 잠깐 지웠다가 되돌렸다. 도는 중의 로그 꼴과 같다.
2. v1 이 정상으로 끝남 → verify B12 650 K valid.
3. 사다리 판독 (결과를 본다): W [600] · cond550 자격 참 · 갈래 '잠정 — cond550 판독 전 · … 축소 3 단계'.
4. PHASE=cond550 (고정 사다리 판독 결속) → 550 K 네 런 · 종료 0.
5. H0 로 PHASE=rerun RERUN=B:12:650 → **종료 0**. 끝난 valid v1 런 (msd.json 있음) 을 `T650.superseded_*` 로 옮기고 새로 굴렸다.
6. cond550 판독: W [550, 600, 650] · 갈래 '3 단계 후보 = W 의 가장 낮은 셋' (확정 · 잠정 아님).
   - B12 650 K 는 사다리 판독에서 측정 가능 아님 (v1 표본) → 최종에서 측정 가능 (v2 표본).
   - 어긋남을 알리는 칸이 없다. `ladder_readout.W [600]` 이 새 W 옆에 적혀 있을 뿐이다.
- 시험용 read_run 은 v1 표본을 C2 미통과, v2 표본을 통과로 둔 것이다. 결과는 어느 쪽이든 된다. 요점은 다시 굴린 표본이 최종에 조용히 들어간다는 것이다.

**재현 2** (`p8_status_check_hold.py`) — v2 런도 같다
- cond550 이 도는 중 `readout --phase cond550` (잠금 쥐어짐) → 보류 기록 (A11_T550 incomplete).
- 큐가 끝남 → A11 550 K valid.
- 그 보류 기록으로 PHASE=rerun RERUN=A:11:550 → **종료 0** · 끝난 v2 런 (status complete · driver_rc 0) 을 옮겼다.

**최소 고침**
- 판독: 보류 기록에 런마다 그때 본 산출물 지문을 싣는다 — 큐 `outputs_sha()` 와 같은 7 파일 + 시작 · 끝 기록 sha256 (없으면 null).
- 큐: 옛 폴더를 옮기기 전에 지금 지문 = 보류 기록 지문인지 본다. 다르면 거부 (종료 16 · '그 기록 뒤 바뀐 런').
- 큐: 사다리 판독 고정 기록 (`<BASE>/readout_stage2/readout_stage2.json`) 이 있으면 사다리 온도 RERUN 을 거부한다. cond550 판독 고정 기록이 있으면 모든 RERUN 을 거부한다.
  - 사다리 판독이 났다는 것은 그때 사다리 런이 모두 valid 였다는 뜻이다. 그 뒤 재실행은 늘 다시 굴리기다.
- 판독: 사다리 판독 행에 런 지문을 싣는다 (v2 = run_id · v1 = 러너 블록 시작 시각 · 둘 다 msd.json sha256). 출력에 카드 `기계_판독_값` 해시도 싣는다.
- 판독: cond550 판독은 사다리 행 지문 · 도구 sha16 · `기계_판독_값` 해시가 사다리 판독 고정 기록과 같을 때만 한다. 다르면 거부 (Refused).
- 판독 (덤): 잠금이 쥐어져 있으면 보류 기록을 쓰지 말고 거부한다. 상태 보기는 verify 로만.

### P1-2 — CARD · DECISIONS 를 환경변수로 바꾸면 한도 · GPU 문턱 · 결정 상태가 따라 바뀌고, 판독이 그 런을 받는다

**무엇이 틀리나**
- v2 는 TEMPS · PROD 같은 값은 무시하지만, 카드와 원장의 경로는 환경변수로 받는다 (`run_stage2_kgy_v2.sh:672-673`).
  - 상한 · 첫 런 한도 · GPU 시작 문턱 · 견적은 그 카드에서 온다.
  - '실행 때 결정 active' 는 그 원장에서 읽어 큐가 시작 기록에 스스로 적는다.
- 판독 `verify_run_v2` 는 런을 정하는 값만 지금 카드와 맞춘다. 결정 상태는 시작 기록의 자기 보고를 믿는다 (`li2s3_stage2_readout.py:871-877`).
  - `card_is_repo_card` · `card_sha256` 는 적기만 하고 안 본다.
- 시작 기록에 repo HEAD · 깨끗함 · 원장 경로 · sha256 이 없다 (v1 은 큐 로그 '판 —' 줄에 HEAD 가 있다).
- DZ P1-4 가 말한 '시험 override 와 생산 경로의 분리' 가 카드 · 원장 단위에서는 안 됐다.

**재현** (`p2_card_override.py`)
- 오늘의 원장 꼴 (queue_v2 결정 proposed) 으로는 종료 6 — 맞다.
- CARD=<상한 1e9 h · 첫 런 1e9 h · GPU 문턱 999999 MiB · 런 값은 같음> · DECISIONS=<둘 다 active> · GPU 9000 MiB (카드 문턱 6000) → **종료 0** · 550 K 네 런.
- 시작 기록: card_is_repo_card False · 카드 sha256 ≠ 판독 카드 · gpu_mib_at_launch 9000 · decisions 둘 다 active.
- 판독 카드 · 원장 (뒤에 active 로 바뀐 것) 으로 verify 네 런 모두 valid · cond550 판독 W [550, 600, 650].
- 지금 원장에서 개정 3 은 proposed 다. 이 리뷰 전에 원장을 덮어 띄운 런도 활성 뒤에는 valid 로 읽힌다. kgy 는 공유 기계인데 GPU 공존 문턱도 같이 풀린다.
- 하네스에서는 판독 카드도 시험 카드라 정상 런도 card_is_repo_card 가 False 였다. 생산 경로에서는 기본 CARD 가 저장소 카드라 이 칸이 참이므로, 판독에서 보는 것이 뜻이 있다.

**최소 고침**
- 큐: `--selftest` 밖에서는 CARD · DECISIONS 가 저장소의 그 파일 (resolve) 이어야 한다. 카드 · 원장 · 큐 · 드라이버가 HEAD 와 같아야 시작한다 (`git -C REPO diff --quiet HEAD -- <넷>`).
- 큐: 시작 기록에 repo_head · repo_clean · decisions_path · decisions_sha256 을 싣는다.
- 판독: v2 런은 card_is_repo_card · repo_clean 이 참이어야 valid 다. 그 커밋의 카드 · 원장 (`git show <head>:<경로>`) 의 sha256 이 시작 기록과 같아야 하고, 그 커밋 원장에서 두 결정이 active 여야 한다.
  - 그 커밋을 못 찾으면 invalid 다 ('못 찾음' 은 '맞음' 이 아니다).
- selftest 는 시험 표지 (예 `V2_TEST=1` → 시작 기록 `test: true`) 로만 카드를 바꾼다. 판독은 test 런을 거부한다 (판독 selftest 만 허용 인수로).

### P1-3 — 첫 런 한도가 PHASE 마다라서, 550 K 블록을 PHASE=rerun 으로 돌리면 한도가 없다

**무엇이 틀리나**
- `phase_first()` 는 '이 PHASE 의 첫 v2 런' 을 찾는다 (`run_stage2_kgy_v2.sh:786-803`). PHASE=rerun 에 이미 첫 런이 있으면 `first_done = True` 로 시작한다 (`:836`).
- cond550 판독의 보류 기록은 아직 안 띄운 550 K 런을 incomplete ('런 폴더가 없다') 로 적는다. 그 기록으로 PHASE=rerun 이 그 런들을 돌린다 (`parse_rerun` 이 conditional.T_K 를 받는다 `:429`).
- 설계가 이 문으로 민다. cond550 런 하나가 실패하면 PHASE=cond550 은 그 폴더에서 종료 17 로 블록 전체를 세운다 (`:817-821`). 안 띄운 550 K 런도 PHASE=rerun 으로만 돌 수 있다.
- 끝 기록 없는 첫 런 (큐가 죽음 → COST_CHARGE) 은 후보가 아니다. 사람이 정한 시간이 한도를 넘어도 안 걸린다.
- 풂 판정은 그 런의 21 멈춤만 본다 — 맞다. 다만 이것을 시험이 안 잡는다 (Q7 QM7).

**재현** (`p4_first_run_phase.py` · `p7_dead_phase_zero_charge.py` · 첫 런 한도 1e-7 h 시험 카드)
- 사다리 재실행 하나 → 종료 21 → ACK (by · reason) → 섞인 사다리 판독 W [600, 650] · 자격 참.
- (a) PHASE=cond550 → 첫 550 K 런 뒤 종료 21 — 맞다.
- (b) 같은 바탕에서 cond550 판독 보류 기록 (550 K 넷 incomplete) → PHASE=rerun RERUN=550 K 넷 → **종료 0**.
  - 네 런의 벽시계 0.0011–0.0012 h 로 한도 (2e-7 h) 의 수천 배다. 새 멈춤 0.
  - cond550 판독 W [550, 600, 650].
- (c) 첫 550 K 런 실패 (turbo 못 켬 → 감시가 세움 · 종료 9) → ACK → PHASE=cond550 다시 → **종료 17**. B11 · A12 · B12 550 K 는 빈 채로 남는다.

**최소 고침**
- 첫 런을 PHASE 가 아니라 길이 블록 (`block` = ladder · cond550) 마다 판정한다. 그 블록의 v2 런 가운데 (어느 PHASE 든 · 옮긴 폴더 포함) 가장 이른 런이 첫 런이다.
- 끝 기록이 없고 비용을 정한 첫 런은 정한 시간으로 판정한다.
- PHASE=cond550 은 완료 아닌 폴더를 건너뛰고 빈 폴더를 계속 돈다 (종료 17 로 블록 전체를 세우지 않는다). 그 폴더는 보류 → PHASE=rerun.
  - 또는 안 띄운 550 K 런은 PHASE=rerun 이 받지 않게 한다 (cond550 만).
- '이미 끝났다' 판정 (`:814-816`) 은 같은 블록의 complete v2 런이면 PHASE=rerun 으로 돈 것도 받는다.

### P2 — 고치면 좋다 (판독을 조용히 틀리게 하지는 않는다)

- **P2-1 cond550 결속 판독 기록이 아무 파일이어도 된다.**
  - 재현 (`p5_p6_link_ack.py`): 사다리 판독이 없을 때, 손으로 쓴 6 키 JSON (kind · status · 자격 · measurable 둘 · base) + sha256 으로 cond550 이 떴다 (종료 0 · 네 런).
  - 뒤에 만든 사다리 판독이 자격 참이면 cond550 판독이 그 런을 받는다. 런의 결속 = fake_readout.json, 판독의 고정 기록 = readout_stage2.json 이고 서로 안 묶인다.
  - 최종 판독은 고정 기록의 자격으로 지켜진다. 그래서 P2 다. 카드의 '사다리 판독 → cond550' 순서는 강제되지 않는다.
  - 고침: READOUT_RECORD 는 `<BASE>/readout_stage2/readout_stage2.json` (resolve) 만 받는다 · 판독은 550 K 런의 link.sha256 = 그 고정 기록 sha256 을 본다.
- **P2-2 손으로 적은 풂 줄이 멈춤을 푼다.**
  - 재현: 종료 21 → `{"type":"ack","id":…}` (by · reason 없음) 한 줄 → 큐 종료 0 · 네 런 · 판독 판독 (풂 목록에 그 줄).
  - 고침: `unacked()` (`:259-262`) · `v2_queue_records()` (`:982`) 에서 by · reason 이 빈 풂은 세지 않는다.
- **P2-3 COST_CHARGE 를 폴더 경로로 묶는다.**
  - 재현 (`p3_charge_rename.py`): 큐를 죽임 → 15 → `COST_CHARGE='A/seed11/T600=0.5'` → 새 보류 → 재실행이 그 폴더를 옮기자 다음 런 앞에서 종료 15 ('비용 미확정 흔적이 생겼다 [A/seed11/T600.superseded_…]'). 같은 런을 두 번 정해야 한다 (장부 이중).
  - 0 h 도 받는다 (p7: `B/seed12/T700=0` → 장부 0.0000 h). DZ P1-3 의 '모름 = 0' 이 환경변수 한 줄로 다시 열린다.
  - 정한 행 (rc 'charge') 은 견적의 관측 h/ps 최대에 안 들어간다 (`:358`).
  - 고침: v2 흔적은 run_id 로 · v1 흔적은 (계, 시드, T, 'v1') 로 묶는다 · 0 이하 거부 · 정한 행도 h/ps 최대에 넣는다 · 정한 시간이 그 블록 첫 런 한도를 넘으면 21 (P1-3).
- **P2-4 cond550 '이미 끝났다' 가 큐 · 드라이버 판을 안 본다** (`:814-816`).
  - 큐를 고쳐 sha16 이 바뀌면, 새 큐는 옛 판 550 K 런을 건너뛰고 판독은 invalid 로 센다 (시끄럽지만 어긋난다).
  - 고침: done 에 queue_v2_sha16 · driver_sha16 = 카드를 더한다.
- **P2-5 판독 `cost_h_total` 은 읽은 런만 더한다.**
  - 옮긴 런 · 정한 비용이 빠진다 (p1: 판독 0.0175 h · 장부 0.0191 h).
  - 고침: 장부 합계를 같이 싣고, 캠페인 비용은 장부로만 적는다.
- **P2-6 v1 큐 로그를 '사다리 시작 줄부터 끝까지' 로 읽는다** (`queue_record :292-330` · 재현 안 함 · 코드 읽기).
  - 그 뒤의 v1 호출 하나 (금지지만 가능 · v1 머리글은 PHASE=cond550 을 아직 광고한다) 가 '문지기 ✓' · '판 —' 줄을 둘로 만든다. 사다리 16 런이 전부 invalid → 전역 보류 → P1-1 의 부분 재실행 문이 열린다.
  - 고침: 사다리 블록 (시작 줄 ~ '■ 큐 끝 · PHASE ladder') 안만 보고, 그 뒤 v1 호출은 따로 보류 사유로 적는다.

### 확인한 것 (맞게 돈다)

- selftest 재현: 큐 v2 57/57 (73 s) · 판독 136/136 (84 s) — 희소 worktree `36d906ef`.
- 실행 직전 다시 해시: 카드 · 큐 파일 · 드라이버 · 입력을 GPU 대기 뒤에 본다 (`:861-868`). selftest 가 각각을 둘째 런 앞에서 잡는다.
- 큐를 죽여도 고아 드라이버가 잠금을 쥔다 (pass_fds). 끝난 뒤 끝 기록 없는 런 = 비용 미확정 (p3 에서도 15).
- 멈춤 · 재시작: 풀리지 않은 멈춤 → 14 · 멈춤 파일을 지워도 첫 런 기록에서 다시 판정 · 상한은 풀어도 다시 건다.
- 판독은 옮긴 폴더를 안 읽고 같은 런을 두 번 세지 않는다 (p1: 12 행 · 고유 12 · B_T650 n_시드 2).
- 섞인 판독의 보류: 끝 기록 없음 · 잠금 · 풀리지 않은 멈춤 · 원장 proposed · 깨진 멈춤 기록 → 보류 · 거부.

---

## 3. Q1–Q7

### Q1 — DZ P1 반례: 막는다. 열린 길이 셋 남았다.

| DZ 반례 | v2 | 근거 |
|---|---|---|
| 실패 · 깨진 파일을 완료로 | 막는다 | 종료 코드 · 필수 산출물 · config = init · 프레임 · md.log · msd 배열 (selftest b12 · b13 · b18 · b19 · 깨짐 6 — 실제 드라이버) |
| 실행 기록 없는 폴더 건너뛰기 | 막는다 | 깨진 msd.json 만 있는 폴더 → 종료 17 (b5) |
| 끊긴 상태 재개 | 막는다 | 고아 드라이버 잠금 → 10 · 끝난 뒤 → 15 (b20 · p3) |
| 비용 장부 | 막는다 | 없음 · 깨짐 · NaN · 행 없음 → 15 · 견적 = max(카드, 관측) × 길이 (b6–b9) |
| 재시작으로 첫 런 한도 | 막는다 | 멈춤 기록 · 기록에서 다시 판정 (b10 · b10b) |
| 설정 ≠ 카드 | 값은 막는다 | TEMPS · PROD · VSEED_OFFSET 무시 (b16) — 카드 · 원장 경로는 못 막는다 |

- 남은 길:
  - ① CARD · DECISIONS 환경변수 (P1-2).
  - ② PHASE=rerun 문과 비용 정함으로 첫 런 한도 피하기 (P1-3).
  - ③ 손 풂 줄 · 0 h 정함 · 경로 키 정함 (P2-2 · P2-3).

### Q2 — 런 직전 결속: 예. VERIFY_MAP 강도는 v1 과 대체로 같고, 카드 · 원장 출처만 약하다.

- GPU 대기 뒤 · 실행 직전에 카드 · 큐 파일 · 드라이버 · 입력을 다시 해시한다. 시작 뒤에는 run_meta · 실제 모드 · config = init · dt 를 감시한다.
- 원장과 결속 기록 (판독 · 보류) 은 대기 뒤 다시 안 본다. 판독이 결속 기록 sha 를 다시 보니 결과는 시끄러운 invalid 다.
- 같은 verify 가 v1 · v2 를 같은 꼴로 읽는다 (판독 selftest 12 런 · 내 하네스 p1 · p2 · p4).
- v2 가 더 센 곳: 큐 파일 sha16 결속 (v1 은 큐 파일을 ⑦ 에 적기만) · 산출물 sha256 (끝 기록 뒤 바뀜 = invalid).
- v2 가 약한 곳: 카드 · 원장의 경로와 repo HEAD 가 시작 기록에 결속되지 않는다 (P1-2).
- 둘 다 같은 곳: 결정 상태 · 패키지 판 · 파이썬 경로 (argv[0]) 는 자기 보고다 (잔여 위험 · 기록만).

### Q3 — 섞인 판독: '끝나지 않음 · invalid' 에는 충분하다. '어느 표본인가' 에는 부족하다.

- 모든 런 valid (각자 자기 증거로) · 잠금 비어 있음 · 풀리지 않은 멈춤 없음 · queue_v2 결정 active — 이 넷이면 끝나지 않은 런이나 invalid 런은 못 들어간다.
  - v1 끝 줄을 빼도 되는 이유도 선다. v1 은 살아 있는 동안 잠금을 쥔다 (fd 8 상속).
- 두 번 세는 길은 없다. verify_all 은 `T<T>` 하나만 읽고, 옮긴 폴더는 안 읽는다.
- 고른 것만 세는 길은 있다 — P1-1 (낡은 보류 · 전역 사유 보류 + 부분 RERUN · 사다리 판독 뒤 재실행).

### Q4 — cond550 결속: 결과를 보고 고치는 길을 막지 못한다. '잠정 / 최종' 은 카드 §7 과 맞다.

- 파일 + sha256 결속은 '그 파일이 그때 그 내용' 만 보증한다.
- 사다리 판독 뒤에 아래가 바뀌어도, cond550 판독은 그것으로 최종 갈래를 낸다. 동결 조건이 없다.
  - 사다리 런 (P1-1 · 재현).
  - 판독 도구 (새 대조 잡 + 허가 키만 바꾸면 된다).
  - 카드 판독 규칙 값.
  - 큐 v2 판 (카드 queue_v2.sha16 을 바꾸면 옛 v2 런이 invalid → 다시 굴림).
- 결속 기록이 고정 경로가 아니어도 된다 (P2-1) — 순서 '사다리 판독 → cond550' 도 강제되지 않는다.
- '잠정 / 최종' 은 맞다.
  - |W| = 0 이면 600 K 가 측정 가능이 아니라 자격이 없고, 갈래 '닫는다' 가 처음부터 확정이다.
  - 600 K 가 W 에 있으면 550 K 하나가 |W| 2 → 3 을 바꿀 수 있다. li2s-2 카드 S2 · §1b 의 '결과 전에 박은 550 K 조건부 하나' 와 같다.
- 빈 곳 하나: cond550 이 상한 · 사람 정지 · 실패로 못 끝나면 '잠정' 이 영영 남는다. 카드에 그때의 규칙이 없다 (4 절 문장 7).

### Q5 — 비용 · 정지 · 한도: 사람이 실수로 우회할 수 있다.

- CARD · DECISIONS 환경변수 (P1-2) — 상한 · 첫 런 한도 · GPU 문턱이 같이 풀린다.
- PHASE=rerun 문 (P1-3) — cond550 런 하나가 실패하면 저절로 이 문으로 간다.
- 손 풂 줄 · 0 h 정함 (P2-2 · P2-3).
- 160 h 는 띄우기 전의 예상비용 검사다. 진행 중 강제 종료가 없어 한 런만큼 넘을 수 있다 — 카드에 그대로 적는다 (문장 5).
- 견적식은 맞다. 첫 런 실측 0.0128 h/ps < 0.013 이라, 800 ps 런의 어림은 카드 값 (0.013 × 800 = 10.4 h) 이 정한다.

### Q6 — 런 값 결속: 런의 정체에는 충분하다. 조용한 길은 두 곳에서 열린다.

- 런을 정하는 값 · 명령 인수 · 입력 · 드라이버 · 큐 판이 지금 카드와 어긋나면 invalid 다 (selftest 음성 · 시끄럽다).
- ① 카드 출처 (P1-2): 상한 · 한도 · 문턱 · 결정 상태는 아무 카드 · 원장에서 올 수 있다.
- ② 판독 규칙 값과 도구는 판독 시점 것이다. 사다리 판독과 cond550 판독 사이에 바뀌어도 막지도 알리지도 않는다 (P1-1 동결).
- cond550 값은 괜찮다. conditional.prod_ps 를 바꾸면 550 K 런이 invalid · T_K 를 바꾸면 그 온도 런이 없어 보류 — 둘 다 시끄럽다.
- 개정 3 문장 9 는 틀렸다. '그 값을 안 건드리는 개정은 v2 런을 무효로 만들지 않는다' — queue_v2.{sha16 · decision} · decision · md_driver_sha16 · inputs_sha256 을 바꿔도 무효가 된다.
  - 결정 id 만 바꿔도 그렇다. 시작 기록의 decisions 에 새 id 가 없어서 invalid 다 (`:871-873`). 4 절 문장 8 로 고쳐 적는다.

### Q7 — 시험: 깨면 대부분 잡는다. 겨냥한 빈칸 10 개는 못 잡는다.

- selftest 재현: 큐 57/57 · 판독 136/136.
- 깨기 13 개. 각각 worktree 사본에서 문자열 하나를 바꾸고 두 selftest 를 다 돌렸다.

| 깨기 | 무엇 | 큐 | 판독 | 결과 |
|---|---|---|---|---|
| QM1 | `traces()` 가 옮긴 폴더 (T<T>.superseded_*) 를 건너뜀 | 57/57 | 136/136 | 초록 |
| QM2 | 재실행 `later` 를 늘 거짓 (끝난 재실행 런을 또 옮김) | 57/57 | 136/136 | 초록 |
| QM3 | cond550 '이미 끝났다' 가 PHASE 를 안 봄 | 57/57 | 136/136 | 초록 |
| QM4 | '이미 끝났다' 가 런 값을 안 봄 | 57/57 | 136/136 | 초록 |
| QM5 | 보류 기록의 BASE 검사 뺌 | 57/57 | 136/136 | 초록 |
| QM6 | cond550 결속 기록의 phase 검사 뺌 (판독은 잡는다 · 큐 쪽 음성만 없다) | 57/57 | 136/136 | 초록 |
| QM7 | 첫 런 한도 풂 = 아무 21 멈춤의 풂 | 57/57 | 136/136 | 초록 |
| QM9 | 견적에서 카드 값 0.013 을 뺌 (관측만) | 57/57 | 136/136 | 초록 |
| QM16 | RERUN 중복 허용 (두 번째가 첫 재실행을 옮긴다) | 57/57 | 136/136 | 초록 |
| RM1 | `_cond550_gate` 가 cond550 자격을 안 봄 | 57/57 | 136/136 | 초록 |
| RM2 | 판독이 멈춤 id 를 풂으로 셈 | 57/57 | 거부로 끝남 | 빨강 |
| 대조 1 | 첫 런 한도의 길이 비례를 뺌 | 56/57 | 136/136 | 빨강 |
| 대조 2 | 갈래 '잠정' 을 끔 | 57/57 | 134/136 | 빨강 |

- 대조 둘이 빨강이라 깨기 방법은 선다. 초록 10 개는 시험이 못 잡는 자리다.
- 더할 음성 시험:
  - 사다리 판독 뒤 사다리 온도 RERUN → 거부 (P1-1).
  - 낡은 보류 기록 (그 뒤 끝난 v1 · v2 런) → 거부 (P1-1 · p1 · p8 꼴).
  - cond550 판독: 사다리 행 지문 · 도구 sha16 · `기계_판독_값` 해시가 사다리 판독과 다르면 거부 (P1-1).
  - 저장소 밖 카드 · 원장 · 더러운 트리 → 큐 거부 · 판독 invalid (P1-2).
  - 550 K 블록을 PHASE=rerun 으로 → 첫 런 한도 · 다른 블록의 풂이 한도를 덮지 않음 (P1-3 · QM7).
  - 사다리 판독이 자격 없음인데 cond550 판독 → 거부 (RM1).
  - 손 풂 줄 · 0 h 정함 · 옮긴 뒤의 정함 키 (P2-2 · P2-3).
  - 같은 보류 기록으로 두 번 · RERUN 중복 · 다른 BASE 보류 기록 (QM2 · QM16 · QM5).
  - '이미 끝났다' 의 PHASE · 런 값 · 판 (QM3 · QM4 · P2-4) · 카드 견적 값이 관측보다 클 때 (QM9) · 옮긴 첫 런 (QM1).

---

## 4. 카드에 넣을 문장

1. **재실행 범위**: "재실행 (PHASE=rerun) 은 판정 보류 기록이 그 런을 invalid · incomplete 로 적었고, 그 기록을 쓴 뒤 그 런 폴더가 바뀌지 않았을 때만 한다 (보류 기록의 런별 산출물 지문 = 지금 지문). 사다리 판독 고정 기록이 생긴 뒤에는 사다리 온도 런을 다시 돌리지 않는다 — 그때 사다리 런은 모두 valid 였으므로, 다시 돌리면 결과를 본 뒤 표본을 고르는 것이다. cond550 판독 고정 기록이 생긴 뒤에는 어떤 런도 다시 돌리지 않는다."

2. **cond550 판독의 동결**: "cond550 판독 ('끝난 뒤 한 번 더') 은 사다리 판독 고정 기록과 같은 사다리 런 (런별 지문) · 같은 판독 도구 sha16 · 같은 카드 기계_판독_값 으로만 한다. 하나라도 다르면 판독하지 않는다 (새 개정 · 사용자 결정). 사다리 판독 뒤에 바뀐 런 · 규칙 · 도구는 cond550 갈래에 들어가지 않는다."

3. **카드 · 원장 출처**: "v2 런은 저장소에 커밋된 카드 · 결정 원장으로만 띄운다. 실행 기록에 repo HEAD · 깨끗함 · 카드와 원장의 경로 · sha256 을 남긴다. 판독은 그 커밋의 카드 · 원장이 실행 기록의 sha256 과 같고, 그 원장에서 카드 결정 · queue_v2 결정이 active 였을 때만 v2 런을 받는다. 환경변수로 준 카드 · 원장으로 돈 런은 시험 런이다 — 판독에 안 쓴다."

4. **첫 런 한도**: "첫 런 한도 (400 ps 당 8 h) 는 PHASE 가 아니라 길이 블록 (사다리 · 조건부 550 K) 마다, 그 블록의 첫 v2 런 (어느 PHASE 로 돌았든 · 옮긴 폴더 포함) 으로 판정한다. 끝 기록이 없어 비용을 사람이 정한 첫 런은 정한 시간으로 판정한다. 한 블록의 멈춤을 푼 것이 다른 블록의 한도를 풀지 않는다."

5. **상한**: "160 GPU-h 상한은 런을 띄우기 전의 예상비용 검사다 — 누적 (장부 전체 · 옮긴 런 · 정한 비용 포함) + max(0.013, 관측 최대 h/ps) × 그 런 길이. 진행 중 강제 종료는 없어 한 런만큼 넘을 수 있다. 캠페인 비용은 장부 합계로만 적는다 (판독의 cost_h_total 은 읽은 런만이다)."

6. **멈춤 풂 · 비용 정함**: "멈춤은 by · reason 이 있는 풂 기록으로만 풀린다 — 손으로 적은 줄도 같다. 비용 미확정 흔적에 사람이 정하는 시간은 0 보다 커야 하고, 그 런의 실행 기록 (run_id) 에 묶는다 (폴더를 옮겨도 따라간다)."

7. **cond550 미완결**: "cond550 이 상한 · 사람 정지 · 실패로 끝나지 못하면 cond550 판독은 없다. 그때는 사다리 판독의 갈래를 최종으로 쓰고 550 K 는 '미완결' 로 적는다. 잠정 표시를 지운다는 사실을 마감 기록에 남긴다."

8. **결속 문장 9 정정**: "v2 런은 런을 정하는 값 (온도 · 블록 · 길이 · 평형 · 난수 오프셋 · 저장 · dt · 원자 수) 과 카드의 decision · md_driver_sha16 · inputs_sha256 · queue_v2.{sha16 · decision} 에 묶인다. 이 가운데 하나라도 바꾸는 개정은 그 전 v2 런을 무효로 만든다. 상한 · 한도 · 견적 · GPU 문턱은 묶지 않는다. 판독 규칙 값은 판독 시점의 카드에서 오며, 사다리 판독 뒤에는 바꾸지 않는다 (문장 2)."

---

## 5. 재현에 쓴 스크래치 파일

**selftest 재현 로그**
- /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/q2_selftest.log — 큐 v2 57/57
- /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/ro_selftest.log — 판독 136/136

**하네스 (실제 v1 큐 → 러너 → 드라이버 · 실제 v2 큐 · fairchem 스텁)**
- /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/h_setup.py — 사다리 8 런 · 시험 카드 (허가 · v2 값) · 원장 둘 (active · proposed)
- /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/h_lib.py — 사본 · v2 큐 호출 · 가짜 read_run · 판독 호출
- /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/h — 바탕과 재현 런 트리 (runs/p1 … p8)

**재현 스크립트 · 출력**
- /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/p1_stale_hold.py · /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/p1.log — P1-1 (낡은 보류 · 갈래 뒤집힘)
- /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/p8_status_check_hold.py · /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/p8.log — P1-1 (상태 보기 보류 → 끝난 v2 런 옮김)
- /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/p2_card_override.py · /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/p2.log — P1-2
- /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/p4_first_run_phase.py · /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/p4.log — P1-3
- /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/p7_dead_phase_zero_charge.py · /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/p7.log — P1-3 (c) · P2-3 (0 h)
- /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/p3_charge_rename.py · /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/p3.log — P2-3 (경로 키)
- /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/p5_p6_link_ack.py · /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/p56.log — P2-1 · P2-2

**깨기**
- /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/mut_ee.py · /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/mut_ee.log — 13 개 (921 s)
- /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/mut — 깨기마다 큐 · 판독 selftest 로그

**worktree**
- 희소 worktree (`36d906ef`) 는 끝나고 지웠다 (`git worktree remove`). 스크립트를 다시 돌리려면 같은 자리에 다시 만든다: `git worktree add --no-checkout --detach /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EE/wt 36d906ef` → `tools/ionic` · `tools/modelc_v3` · `db/inputs/li2s3_dense_ensemble_2026_11_10` · `db/raw/lpscl_glass_md_v2_2026_09_30` · 카드 둘 · `db/governance/decisions.json` 희소 체크아웃 → `python3 h_setup.py`.
- review_EB 폴더의 스텁 · 표는 쓰지 않았다 (스텁은 판독 도구 안의 것을 썼다).

### 하지 않은 것 · 못 본 것

- 실제 fairchem · GPU · kgy 로그 · 실제 런은 안 봤다.
- W · 갈래는 시험용 read_run 으로만 냈다. 게이트 · 결속 경로를 본 것이지 수송 판정을 본 것이 아니다.
- 하네스의 출처 기록은 깨끗함을 강제로 참으로 두었다 (판독 selftest 와 같다). 첫 런 한도 시험은 아주 작은 한도 (1e-7 h) 로 했다.
- P2-6 은 코드만 읽었다 (재현 안 함).
