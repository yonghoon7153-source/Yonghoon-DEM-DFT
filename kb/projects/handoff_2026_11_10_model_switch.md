---
title: "모델 전환 인계 (2026-11-10 저녁) — 같은 세션 · 같은 브랜치 friendly · 돌고 있는 것 둘 (gabia b2o3 8 단계 · kgy li2s-3 2 단계) · 기한 있는 도구 둘 · 사용자 결정 대기 셋"
date: 2026-11-10
updated: 2026-11-10
tags: [handoff, b2o3, li2s, cascade, gabia, kgy, codex, litdb]
status: 진행
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: multi-source-primary
---

# 모델 전환 인계 (2026-11-10 18:15 KST)

사용자가 세션 모델을 바꾼다 (*"곧 opus로 바꿀건데 준비해용"*). 세션 · 브랜치 (`claude/friendly-meitner-lldvar`) · 작업 폴더는 그대로다. 이 문서는 바뀐 뒤 바로 이어 가기 위한 것이다. 상세는 각 원장이 정본이고 여기는 길잡이다.

## 0. 먼저 볼 것 (순서대로)

1. `kb/open_items.md` ⏭ 머리 줄과 트랙 줄 (`grep -n "b2o3 B·O 배치 UMA 재탐색 카드\|li2s-2 새 트랙 열림\|cascade v7 본 라운드 끝" kb/open_items.md`) — 통째로 읽지 말고 grep.
2. 결정 원장 `db/governance/decisions.json` 의 오늘 것: `D-2026-11-10-b2o3-bo-placement-stage1-cap` · `D-2026-11-10-b2o3-bo-placement-anneal-time-diagnostic` · `D-2026-11-10-li2s3-dense-protocol-ensemble` (셋 다 active).
3. 이 세션의 할 일 목록 (Task) 35 · 36 번.

## 1. 지금 돌고 있는 것

| 기계 | 무엇 | 시작 | 끝 어림 | 볼 것 |
|---|---|---|---|---|
| gabia | b2o3 8 단계 — 54 런 × 100 ps 어닐 (tmux `b2o3_s8` · `R=/data/work/runs/b2o3_bo_2026_11_09`) | 11-10 09:58:21 | 11-13 08:30 쯤 | 멈춤 규칙: 첫 런 2 h (통과) · 누적 85 GPU-h. 감시 화면의 '(20 ps 까지)' 는 옛 문구 (표시만). ⛔ 1 단계가 끝날 때까지 `$R/src` 를 새 판으로 올리지 않는다 · gabia 에 GPU pw.x 를 띄우지 않는다 |
| kgy | li2s-3 2 단계 — 16 런 × 400 ps (tmux `li2s3s2` · `~/work/runs/li2s3_stage2_2026_11_10` · worktree `~/wt_li2s3`) | 11-10 17:17:20 | 11-12 저녁 ~ 11-14 | 큐가 스스로 멈춘다: 첫 런 8 h (종료 21) · 누적 160 h (22). 로그 `stage2_kgy.log` · 장부 `cost_ledger.tsv`. kgy GPU 의 ≈ 4 GB 는 esp 계정 그래픽 앱이다 (우리 것 아님) |

⚠ 사용자는 gabia 창과 kgy 창을 같이 쓴다 — 오늘 kgy 블록을 gabia 에 붙여 넣은 일이 있었다 (첫 명령에서 멈춰 무해). 블록마다 어느 기계인지 첫 줄에 적는다.

## 2. 기한 있는 일 (결과를 읽기 전에 도구부터)

1. **b2o3 어닐 시간 진단 도구 — 11-13 08:30 전** (Task 36). 카드 `db/properties/b2o3_bo_placement_estimand_2026_11_09.json` 의 `개정_3_어닐_시간_진단_2026_11_10`. 할 일: 8 단계 `anneal_results.json` 의 런마다 `md.traj` 프레임 50 (= 50 ps · 저장 간격 500 걸음 × 2 fs) 을 떼어 런 기록의 `md_traj` (sha256 · 프레임 수 · 간격) 에 묶고 → 이완만 (실행기 `db/inputs/ndo_site_2026_10_14/run_uma_kgy.sh` · `TIME_PS=0` · 새 `OUTNAME`) → 판독기 `tools/doping/b2o3_bo_readout.py::anneal_judge` 를 **그대로 불러** 50 ps 시점 가족 판독 → 잠정 규칙 (두 시점에서 같은 가족이 승자일 때만 승자 문장 · 낮추기만). 새 파일로 쓴다 (예 `tools/doping/b2o3_bo_anneal_diag.py`) · selftest 음성 포함 · 판독기와 `$R/src` 는 안 건드린다. 8 단계 본 판독 명령은 런로그 · open_items 에 있다 (`b2o3_bo_readout.py anneal --verdict … --receipt … --results … --out …`).
2. **li2s-3 2 단계 판독 소비자 + MD 압력 도구 — 16 런이 끝나기 전** (Task 35). 카드 `db/properties/lpscl_glass_dense_protocol_ensemble_estimand_2026_11_10.json`. 측정 가능 = (계, T) 마다 두 시드 모두 C1 ∧ C2 ∧ 골격 통과 · 골격은 **생산 첫 프레임 대비** 읽기 (`tools/ionic/quench_ss_event.py::production_framework` 의 `criteria_vs_first_frame` · `tools/ionic/glass_v2_readout.py` 의 ①–④) · W = 두 계 공통 온도. 압력 = li2s-2 카드 §2 `MD_압력` 절차 (저장 궤적에서 1 ps 간격 단일점 virial). 도구를 고치면 과거 마감부터 재현한다 (대조 잡 · CLAUDE.md 코드 규율).
3. **Codex 회신 반영**: 편지 둘이 발송 대기다 (사용자가 보낸다 · 보내는 글은 11-10 에 파일로 전달함).
   - `kb/reviews/codex_DZ_prompt_li2s3_ensemble_definition_2026_11_10.md` (li2s-3) — 보내면 **회신 전에는 2 단계 결과를 읽지 않는다**.
   - `kb/reviews/codex_EA_prompt_b2o3_anneal_time_diagnostic_2026_11_10.md` (b2o3) — 회신이 규칙을 바꾸면 **8 단계 판독 전에** 카드 개정 4.
   - 회신은 `codex_<글자>_reply_….md` 로 원문 보존 → `python3 tools/kb_wiki.py reviews --write`.

## 3. 사용자 결정 대기

- **[cascade]** 사용자 11-10: *"내가 생각하기엔 cascade는 답이 없네 이런거 보니까"*. 좁아진 B 보고량 카드는 **시작하지 않았다**. 정할 것: 닫기 (권고 — 마감 기록에 v7 동등 · 축 묶음 · 갭 보고서 · digest 다섯 편) / GPU 0 짜리 양극 쪽 ΔV/V 표 하나만 보고 닫기. 갭 판정은 `reports/황화물 분해 부피 도펀트 문헌 갭.md` 의 '본문 확인 결과' 절.
- **[b2o3]** 개정 3 의 잠정 규칙 (두 시점 같은 승자) 은 에이전트 제안이다 — 사용자가 다른 말을 하거나 Codex 가 바꾸면 판독 전에 다시 개정.
- **[li2s-3]** 로그 머리 한 번 (`head -n 12 ~/work/runs/li2s3_stage2_2026_11_10/stage2_kgy.log`) — 검사 블록 결과 · 소프트웨어 판 · worktree HEAD 를 런로그 `발사_2026_11_10.미회수` 에 채우려고 요청해 둔 것 (급하지 않다).

## 4. 오늘 정한 것 · 한 것 (한 줄씩)

- 복귀: 대피 브랜치를 friendly 로 fast-forward (60 커밋) · 사용자 로컬 웹앱에서 개념 카드 확인.
- b2o3: 영수증 t_a = 100 ps → 상한 30 → 85 GPU-h (개정 2) → 8 단계 발사 → 개정 3 (어닐 시간 진단).
- li2s: li2s-2 는 1 단계에서 닫힘 (B 1/5) → 사용자 *'이어서해'* → **li2s-3** (시드 포함 규칙 하나만 바꿈: PS₄ = 1.0 선택 → 기록만 · 유리 여섯 재사용) → kgy 2 단계 발사.
- cascade: 다섯 편 (목록 120–124) digest → 갭은 서지만 좁아짐 → 사용자가 회의적.
- litdb: nolan2018 의 '3.1 배' 네 곳 · comparison 두 행에 정규화 불일치 꼬리.

## 5. 이 컨테이너에서 걸리는 것

- **다른 세션이 같은 브랜치에 litdb 커밋을 올린다** (오늘 여러 번). push 가 거부되면 `git fetch` → `git rebase origin/claude/friendly-meitner-lldvar` → push (force 금지). `litdb/pdf_map.tsv` 는 양쪽이 끝에 덧붙여 충돌하므로 **이 컨테이너의 `.git/info/attributes` 에 `litdb/pdf_map.tsv merge=union` 을 넣어 뒀다** (저장소에 없는 로컬 설정 — 컨테이너가 바뀌면 다시 넣는다).
- **비준 커밋 해시는 고정이다** — 결정의 `ratification.commit` 이 가리키는 커밋 (오늘: `e917b9e2` · `6b764d48` · `ed24b57d`) 은 이미 원격에 있다. 두 번 커밋 방식 (카드 커밋을 먼저 push → 그 해시로 비준 커밋) 을 지킨다. push 전에 rebase 로 해시가 바뀌면 비준에 적기 전이어야 한다.
- 작업 폴더를 안 건드리고 내 커밋만 원격 끝에 얹는 법 (에이전트가 파일을 쓰는 중일 때): `git merge-tree --write-tree --merge-base=HEAD~1 <원격끝> HEAD` → `git commit-tree` → `git push origin <새커밋>:refs/heads/<브랜치>` → 나중에 `git rebase` 가 중복을 떨군다.
- pytest · flask 는 `<scratchpad>/venv_web` · PyMuPDF 는 `~/.venvs/litdb/bin/python3` · 얕은 복제라 웹앱 git 날짜 시험은 `git fetch --deepen=250` 뒤에 통과한다.
- 정지 훅이 작업 폴더가 깨끗한지 본다 — 서브에이전트가 도는 동안은 중간 스냅숏 커밋으로 맞춘다.
- 커밋 메시지 끝의 귀속 줄은 그때의 시스템 안내를 따른다 (모델 ID 를 본문에 쓰지 않는다 — CLAUDE.md).

## 6. 값 규율 (이 인계에서 특히)

- li2s: 절대 수송값은 어디에도 싣지 않는다. li2s-3 는 결과를 16 런이 끝나고 판독 도구 커밋 뒤 **한 번** 읽는다. li2s-2 마감 문장은 고치지 않는다.
- b2o3: 8 단계 결과는 본 판독 (판 고정 도구) 으로만 읽고, 승자 문장은 개정 3 규칙을 거친 뒤에만 쓴다.
- cascade: 문장은 마감 파일의 허용 문장만.
