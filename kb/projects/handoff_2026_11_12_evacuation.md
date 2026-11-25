---
title: "대피 인계 — 2026-11-12 (friendly 세션 토큰 소진 → 서브 세션 · 머지 때 충돌 0 설계 · b2o3 8 단계 gabia · li2s-3 2 단계 kgy 진행 중)"
date: 2026-11-12
updated: 2026-11-12
tags: [handoff, session, evacuation, branch, merge, b2o3, li2s, glass, md, uma, cascade, webapp]
status: 진행
kind: project
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

# 대피 인계 — 2026-11-12

> (사용자 2026-11-12 *"토큰이 3%정도 밖에 없어서 서브/대피 브랜치로 가려고 하거든? 전에 하던것처럼 다시 머지할 때 충돌없이 될 수 있게 잘 프롬프트 짜주고"*).
> 선례: `handoff_2026_11_08_evacuation.md` (대피) → `handoff_2026_11_10_return_to_origin.md` (복귀 · friendly 가 움직여서 대피 쪽에서 먼저 머지 · 충돌 0).
>
> **충돌 0 의 조건 — 대피하는 동안 이 세션은 friendly 에 쓰지 않는다.** 이 카드를 담은 커밋이 이 세션의 friendly 마지막 커밋이다.
> ⚠ 이번엔 friendly 가 **거의 확실히 움직인다** — 다른 둘이 friendly 에 직접 쓴다: ① litdb 정리 세션 (`litdb: _curation …` 커밋 · 11-11~12 에 48 개)
> ② 사용자 로컬 웹앱의 메모 저장 (`notes: 화면에서 쓴 메모·형광펜` · `db/file_comments.json` · `db/file_highlights.json`). 그래서 복귀는 ■6 의 두 번째 길이 기본이다.

## 0. 새 세션 (서브) 에 붙여 넣을 프롬프트

```text
[대피 세션 시작 — 2026-11-12 · 서브]

너는 Yonghoon-DEM-DFT 캠페인의 임시 대피 세션이다. 본 세션(브랜치 claude/friendly-meitner-lldvar)이 토큰을 다 써서
이 서브 브랜치로 옮겨 왔다. friendly 세션이 하던 일을 그대로 이어 간다. 나중에 사용자가 "돌아가자" 하면
이 브랜치를 friendly 로 **충돌 없이** 되돌린다 — 그 조건이 아래 ■1 · ■5 · ■6 이다.

■ 1. 브랜치 (제일 먼저)
- 이 세션 브랜치 = 너의 시스템 지시에 적힌 개발 브랜치 (아래 <이 세션 브랜치>).
- git fetch origin claude/friendly-meitner-lldvar
- git log --oneline -40 origin/claude/friendly-meitner-lldvar | grep -n "Evacuation handoff card 2026-11-12" → 이 카드 커밋이 있어야 한다
  (그 아래 어딘가에 96a8b7ec "runlogs 11-12 14:08 …" · 사이에 litdb 정리 · 메모 커밋이 끼어 있다 — 카드를 쓰는 동안에도 friendly 가 움직였다).
  카드 커밋 위에 커밋이 더 있으면 누가 올렸는지 (git log --format='%h %an %ad %s') 본다 —
  litdb 정리 세션 (`litdb: _curation …` · `litdb: <slug> 카드 추가`) 과 사용자 로컬 웹앱 메모 (`notes: 화면에서 쓴 메모·형광펜`) 는 정상이다 (알리기만).
  그 밖의 것이면 사용자에게 묻는다. 카드 커밋이 아예 없으면 멈추고 말한다.
- 이 세션 브랜치가 friendly 끝을 포함하지 않고 아직 내 커밋도 없으면 friendly 끝에서 시작한다:
    git checkout -B <이 세션 브랜치> origin/claude/friendly-meitner-lldvar
  (첫 push 가 non-fast-forward 로 거절되면 그 원격 브랜치에 내 커밋이 없는지 확인한 뒤에만 --force-with-lease.) 이미 내 커밋이 있으면 멈추고 묻는다.
- 브랜치를 옮겼으면 CLAUDE.md 를 다시 읽는다.
- ⛔ friendly 에는 push 하지 않는다. CLAUDE.md 의 "friendly 에만 커밋/푸시" 는 이 세션에서 "friendly 에는 쓰지 않는다 · 커밋 · 푸시는 <이 세션 브랜치> 에만"
  으로 읽는다 (사용자 2026-11-12 대피 지시). friendly 반영은 ■6 대로만.
- ⛔ 원격 (kgy · gabia) 붙여넣기 블록에서 git fetch · push 할 때도 <이 세션 브랜치> 를 쓴다 (friendly 로 push 하면 복귀가 꼬인다).
  지금 도는 잡의 worktree 는 이미 고정돼 있다 — 판독 블록은 그 worktree 를 그대로 쓴다 (§1 · §2).
- PR 만들지 않는다 · force-push 는 --force-with-lease 만 · 커밋 메시지에 모델 ID 를 넣지 않는다.

■ 2. 먼저 읽을 것 (큰 파일은 grep · 부분 읽기)
- kb/projects/handoff_2026_11_12_evacuation.md ← 이 인계 카드 (§1–§6 통째로)
- kb/open_items.md 머리 (6 번째 줄 · '지금 상태 — 2026-11-12' 목록 다섯 줄)
- b2o3: runlog db/properties/b2o3_bo_placement_stage1_runlog_2026_11_09.json 의 키 8b_진단_블록_v3_2026_11_10 (블록 v3 · 반드시) ·
  8단계_진행_2026_11_12_1408 · 카드 db/properties/b2o3_bo_placement_estimand_2026_11_09.json (개정 4 · active)
- li2s-3: 카드 db/properties/lpscl_glass_dense_protocol_ensemble_estimand_2026_11_10.json 의 판독_허가_2단계 ·
  runlog db/properties/lpscl_glass_dense_protocol_ensemble_runlog_2026_11_10.json 의 진행_2026_11_12_1408 · ⚠_다음_런_시작 (진행_2026_11_11_1853 안)
- 값 · 판정은 원장이 이긴다: db/governance/decisions.json · db/properties/canonical_registry.json · db/properties/citation_hazards.json

■ 3. 시작 점검 (대피 직전 friendly 실측 기대값을 옆에 적었다)
  python3 tools/kb_wiki.py lint | tail -1                 # RESULT: 0 errors
  python3 tools/db/validate_canonical.py | tail -3        # 거버넌스 결정 185 · 판정 8 · 그래프 무결성 ✅ · 배선 전부 일치
  python3 tools/convention_check.py | tail -1             # RESULT: 0 위반
  sha256sum tools/ionic/li2s3_stage2_readout.py | cut -c1-16   # 60a7ef3ce31d0bb2 (판독_허가_2단계 의 도구 sha16 과 같아야 한다)
  (웹앱 전체 시험은 필요할 때만 — 레포 루트에서 python3 -m pytest -q webapp/tests/ · 약 9 분 · 11-12 기준 662 통과 · 1 skip)

■ 4. 지금 상태와 할 일 — 인계 카드 §1–§4. 요약:
- b2o3 (트랙 b2o3 UMA-MD · 1저자 = 사용자): gabia tmux b2o3_s8 · 1 단계 8 단계 · 11-12 14:08 에 39/54 · 끝 어림 11-13 10:08.
  끝나면 runlog 8b_진단_블록_v3_2026_11_10 의 gabia 블록 v3 를 준다 (⓪ 점검 → ⓪b traj 에너지 → ① 본 판독 → ③ 추출 → ④ 이완 큐 → ④b rc → ⑤ 판정).
  ⛔ 8 단계가 끝나기 전에는 결과를 읽지 않는다 (진행 신호만 · 폴더 이름의 E 는 6 단계 값). 감시 줄의 '(20 ps 까지)' 는 옛 문구 — 실제 100 ps.
- li2s-3 (트랙 li2s · 논문 1저자 = 외부 · 위임 10-30 — 결정은 에이전트가 정해서 진행하고 원장에 '사용자 (위임 10-30)'):
  kgy tmux li2s3s2 · 2 단계 16 런 · 11-12 14:08 에 8/16 · 끝 어림 11-14 새벽. 16 런 + 큐 끝 줄이 나온 뒤에만 readout · pressure 를 한 번
  (도구는 ~/wt_li2s3_q2 · --worktree ~/wt_li2s3 · 카드 판독_허가_2단계 걸림). 큐 v1 은 런마다 GPU 합계 ≤ 6,000 MiB 를 1 h 기다린다 —
  DEM 잡 (사용자 쪽 · 같은 GPU) 이 다시 GPU 를 쓰면 종료 12 로 멈출 수 있다 → v1 은 다시 치지 않고 남은 런은 큐 v2 (run_stage2_kgy_v2.sh · 카드 개정 3) 로 · GPU 가 빈 뒤.
- cascade (1저자 = 사용자): 묶음 2 닫힘 (11-11 비준). 다음 = DFT 확인 후보 카드 — 🔔 사용자 결정 (사용자가 /cascade#bundle2 를 보고 정함 · 급하지 않음).
- 사용자 결정 대기: cascade DFT 후보 · /ro_st4.log 지우기.
- 원격: gabia = b2o3 8 단계 (GPU 1.9 GB) · kgy = li2s-3 2 단계 (esp 앱 GPU 는 그대로 둔다) · 새 계산 승인 없음.

■ 5. 머지 충돌을 안 만드는 규칙 (friendly 에 다른 둘이 계속 쓴다 — 그 파일은 건드리지 않는다)
- ⛔ 손대지 않는다: db/file_comments.json · db/file_highlights.json · db/note_images/ (사용자 로컬 웹앱이 friendly 에 쓴다) ·
  litdb/_curation/ (litdb 정리 세션). litdb 에 새 digest 를 넣어야 하면 litdb/INDEX.md · litdb/comparison_vs_ours.md ·
  litdb/figures/_sources.json · litdb/pdf_map.tsv 는 **행을 덧붙이기만** 한다 (옛 행을 고치거나 순서를 바꾸지 않는다).
- 생성 파일은 손으로 고치지 않는다 — kb/index.md (python3 tools/kb_wiki.py index) · kb/reviews/INDEX.md (python3 tools/kb_wiki.py reviews --write) ·
  litdb INDEX_DEM 등 build_index.py 산출물 (복귀 머지 뒤 도구로 다시 만든다).
- kb/open_items.md: ⏭ 머리는 2026-11-11 부터 '지금 상태' 목록 꼴이다 — 목록 줄을 고치고, 밀려난 상태는 접힌 '지난 갱신 기록' 맨 위에 한 항목으로 옮긴다.
  ⏭ 제목 줄에 이어 붙이지 않는다 · 그 밖의 절은 옛 문장을 지우거나 고쳐 쓰지 않고 '⏩ **날짜**: …' 로 덧붙인다.
- db/governance/decisions.json: 내가 다루는 결정만 고친다 · ratification 이 있는 결정은 내용을 바꾸지 않는다 (decision_digest 가 깨진다) — 새 사실은 새 결정이나 runlog 에.
- runlog · 카드 JSON 은 새 키를 끝에 덧붙인다 · indent=1 · ensure_ascii=False 형식을 지킨다.

■ 6. 복귀 (사용자가 "돌아가자" 할 때)
- 이 세션이 kb/projects/handoff_<날짜>_return_to_origin.md 를 쓴다 (선례 handoff_2026_11_10_return_to_origin.md) — §0 에 friendly 세션용 프롬프트.
- 먼저 가상 머지로 충돌을 잰다 (아무것도 안 바꾼다):
    git fetch origin claude/friendly-meitner-lldvar <이 세션 브랜치>
    git merge-tree --write-tree origin/claude/friendly-meitner-lldvar origin/<이 세션 브랜치> | tail -5   # 충돌 줄이 없어야 한다
- friendly 가 이 카드 커밋에서 안 움직였으면: friendly 쪽에서 git merge --ff-only origin/<이 세션 브랜치> 한 줄 (충돌 0).
- friendly 가 움직였으면 (기본 — litdb 정리 · 메모 커밋): 이 세션 브랜치에서 먼저 git merge --no-ff origin/claude/friendly-meitner-lldvar →
  충돌은 생성 파일이면 도구로 다시 만들고 · litdb 표 · open_items 는 양쪽 행을 다 남기고 → lint 0 · validate ✅ · 웹앱 시험 확인 → push →
  그 다음 friendly 쪽은 git merge --ff-only origin/<이 세션 브랜치> (friendly 에서 rebase · force 금지).
- 복귀 카드에 원격 상태 (b2o3 8 단계 · li2s-3 2 단계 진행 · 마지막 실측 시각) 와 이 세션에서 바뀐 원장 목록을 적는다.
- 로컬 웹앱 안내도 적는다: 로컬 127.0.0.1:5001 은 로컬 체크아웃을 읽는다 — 대피 중 로컬을 대피 브랜치로 옮겼으면
  git switch claude/friendly-meitner-lldvar && git pull --ff-only · friendly 에 있었으면 git pull --ff-only.
```

## 1. b2o3 — 1 단계 8 단계 gabia 진행 중 (트랙 b2o3 UMA-MD · 1저자 = 사용자)

- 무엇: B–O 배치 카드 1 단계 8 단계 — 54 구조 × (UMA MD 100 ps + 이완) · gabia tmux `b2o3_s8` · 11-10 09:58:21 시작 (입력 · 소스 해시 재대조 통과).
- 마지막 실측: 11-12 14:08 — 39/54 · 구조당 80 분 · 끝 어림 **11-13 10:08** (runlog `8단계_진행_2026_11_12_1408`).
- 끝나면: runlog `8b_진단_블록_v3_2026_11_10` 의 블록 v3 (worktree 70020852 → ⓪ 점검 → ⓪b traj 에너지 True/False → ① 본 판독 → ③ 추출 → ④ 이완 큐 → ④b rc → ⑤ 판정).
  카드 개정 4 (11-10 사용자 비준 · active) 대로 — 결과를 보고 규칙을 바꾸지 않는다.
- 감시: 사용자가 `watch -n 30 'bash $HOME/w_b2o3_s8.sh | sed …'` 를 쓴다 (이완 줄을 가림). 그 화면의 cascade 묶음 2 줄은 끝난 잡이라 정보 없음.

## 2. li2s-3 — 2 단계 kgy 진행 중 (트랙 li2s · 논문 1저자 = 외부 · 위임 10-30)

- 무엇: 조밀 프로토콜 앙상블 카드 2 단계 — 16 런 (A · B 계 × 시드 × 온도 · 400 ps) · kgy tmux `li2s3s2` · 큐 v1.
- 마지막 실측: 11-12 14:08 — 8/16 · A seed11 T700 56 % · ≈ 79.5 ps/h (DEM 잡이 GPU 를 안 쓰는 동안) · 16 런 끝 어림 **11-14 새벽**
  (runlog `진행_2026_11_12_1408`). 대조 잡 v3 same = True (sha256 머리 63fb4bb1e65a0509 = 카드 `판독_허가_2단계` 와 같다).
- 끝나면: 16 런 + 큐 끝 줄 확인 → readout · pressure **한 번** (도구 `tools/ionic/li2s3_stage2_readout.py` sha16 60a7ef3ce31d0bb2 · 카드 `판독_허가_2단계` 가 대조 잡 출력 · 트리 깨끗함 · 도구 sha 를 다시 본다).
- 위험: 큐 v1 의 시작 문턱 (GPU 합계 ≤ 6,000 MiB · 1 h 대기 · 넘으면 종료 12) — DEM 잡이 다시 GPU 를 쓰면 멈출 수 있다.
  멈추면 v1 은 다시 치지 않고 남은 런은 큐 v2 (`run_stage2_kgy_v2.sh` · 카드 개정 3) 로 GPU 가 빈 뒤 (runlog 11-11 18:53 `⚠_다음_런_시작`).

## 3. cascade (1저자 = 사용자)

- 묶음 2 닫힘 (`D-2026-11-11-cascade-axes-bundle2-closed` · 11-11 사용자 비준 · 마감 `db/properties/cascade_axes_bundle2_closed_2026_11_11.json`).
- 화면: `/cascade` 맨 위 '묶음 2 · 원소별 효과' 패널 (Pareto 그림 · 호스트 대비 표 · 판독 sha16 결속).
- 다음: DFT 확인 후보 카드 — 🔔 사용자 결정 (급하지 않음). 계산 없음.

## 4. 웹앱 · 기타

- 11-11 ~ 11-12 웹앱: 판정 원장 결정 행 · 인용 위험 표 두 칸 꼴 · 미결 리스트 접기 (`<details>` 줄 · 접힌 지난 세션 인계 53 절은 대시보드 '대기' 에서 뺌) ·
  Dashboard 긴 핵심값 본문 글씨 · 표 칸 쪼그라듦 막기 (`.card td .mono{overflow-wrap:break-word}` · `|pathwrap`) · 브라우저 배치 시험 `webapp/tests/table_layout.test.mjs` (pytest 가 부른다).
- 사용자 결정 대기: `/ro_st4.log` 지우기 (어디 있는지는 open_items 의 앞 기록 · 사용자가 정함).

## 5. 이 세션이 대피 직전에 한 것 (11-11 ~ 11-12)

- cascade 묶음 2: G2 멈춤 → 개정 2 (비준) → gabia 재실행 → 판독 → 마감 (비준) · `/cascade#bundle2` 패널.
- li2s-3: 대조 잡 v3 same = True → 카드 `판독_허가_2단계` · 진행 기록 (11-11 13:16 · 18:53 · 11-12 14:08).
- b2o3: 8 단계 진행 기록 (11-11 13:15 · 11-12 14:08).
- 웹앱 가독성 (`528b7c3e` · `20744e36`) · 인계 카드 `handoff_2026_11_11_token_limit.md` (토큰 한도 대비 · 이 카드가 대신한다).

## 6. 복귀 체크리스트 (복귀 카드에 옮길 것)

- [ ] `git merge-tree --write-tree` 로 가상 머지 충돌 0 확인 → friendly 가 움직였으면 대피 브랜치에서 먼저 `--no-ff` 머지 · friendly 쪽은 ff-only
- [ ] 머지 뒤 생성 파일 다시 만들기 (kb index · reviews INDEX · litdb build_index 산출물) · lint 0 · validate ✅ · 웹앱 시험
- [ ] b2o3 8 단계 판독 (블록 v3) · li2s-3 2 단계 readout · pressure 가 대피 중 끝났으면 그 결과 · 원장 변경 목록
- [ ] 로컬 웹앱 되돌리기 안내 (위 ■6 끝 줄)
