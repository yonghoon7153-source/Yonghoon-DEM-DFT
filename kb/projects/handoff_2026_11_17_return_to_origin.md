---
title: "본 세션 복귀 카드 — 대피 브랜치 claude/evac-2026-11-12 를 friendly 로 · fast-forward (2026-11-17) · litdb 정리 세션 · 로컬 웹앱 맞추기"
date: 2026-11-17
updated: 2026-11-17
tags: [merge, handoff, return, evacuation, litdb, webapp, gabia, kgy, b2o3, hyeokju]
status: 발송 대기 — 사용자가 §0 을 본 세션 (friendly) 에, §0b 를 litdb 정리 세션에 붙여 넣는다
confidence: medium
verificationStatus: verified
verifiedAt: 2026-11-17
verifiedBy: self
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: single-source
---


# 본 세션 복귀 카드 — `claude/evac-2026-11-12` → `claude/friendly-meitner-lldvar`

> 선례: `kb/projects/handoff_2026_11_10_return_to_origin.md` (fast-forward · 충돌 0) · 대피 인계 `kb/projects/handoff_2026_11_12_evacuation.md` ■5 · ■6
> (friendly 가 움직였으면 대피 브랜치에서 먼저 `--no-ff` 머지 · friendly 쪽은 ff-only).
> 실측 (2026-11-17 00:39 KST · 대피 세션):
> · merge-base = **`fb3fc7df4`** (대피 인계 카드). 그 뒤 friendly 에 **litdb 정리 세션 커밋 228 개** (끝 **`37fb17f49`** · 11-16 15:17 *'litdb: _curation status — N-82 끝 …'*) — 전부 `litdb: …` 커밋이다.
> · 대피 세션이 그 228 개를 **대피 브랜치로 먼저 `--no-ff` 머지**했다 (`9c2276537`). 충돌 1 = `litdb/figures/_sources.json` —
>   키 합집합으로 풀었다 (friendly 558 키 + 대피 새 6 키 = 564 · 겹치는 키 0 · 대피 쪽은 옛 키를 안 고쳤다 · 형식은 도구 출력과 같다).
>   두 쪽이 같이 바꾼 파일은 그것 하나다 (friendly 4047 파일 · 대피 607 파일).
> · 머지 뒤 생성 파일 다시 만들기 `6d570f45e` (kb index · reviews INDEX — 날짜 줄만 바뀜).
> · 점검 (= §0 ■2 기대값): kb lint 0 errors · 결정 193 · 판정 8 · 그래프 ✅ · 배선 일치 · 규약 0 위반 · litdb `build_index.py --check` rc 0
>   (표 칸 ⚠ comparison 69 · DEM 148 · INDEX 120 은 옛 '표 중간 빈 줄' 경고) · build_index selftest 35/0 · extract_figures selftest 117/0 · 웹앱 시험 662 passed · 1 skipped (§3 끝 줄).
> · 그래서 friendly 쪽 들이기는 **fast-forward** 다 — 단 litdb 정리 세션이 friendly 에 계속 쓰므로, 37fb17f49 뒤로 또 움직였으면 §0 ■1 경우 C.
> · `origin/main` 은 이 캠페인과 무관 — main 으로 머지하지 않는다.

## 0. 본 세션 (friendly) 에 붙여 넣을 프롬프트

```text
[본 세션 복귀 — 2026-11-17 · 대피 브랜치 claude/evac-2026-11-12 들이기]

너는 Yonghoon-DEM-DFT 캠페인의 본 세션이다 (브랜치 claude/friendly-meitner-lldvar). 11-12 오후 토큰이 떨어져서 사용자가 대피 세션
(브랜치 claude/evac-2026-11-12) 으로 옮겼다. 네가 올린 마지막 커밋은 대피 인계 카드 fb3fc7df4 다. 그 뒤 friendly 에는 litdb 정리 세션의
커밋 228 개 (끝 37fb17f49) 가 올라갔고, 대피 세션이 그 228 개를 대피 브랜치로 먼저 머지해 두었다 (9c2276537 · 충돌 1 · 풀었다).
그래서 들이기는 fast-forward 다. 할 일: 대피 커밋을 충돌 없이 들이고 → 점검 → push → litdb 정리 세션과 사용자 로컬 웹앱을 맞춰 주고
(■7 · ■8) → 원장 · 기록으로 상태를 다시 맞춘 뒤 이어서 일한다.
⛔ origin/main 으로 머지하거나 push 하지 않는다 · '원래 브랜치' 는 friendly 다 · 대피 브랜치는 지우지 않는다 (기록 · 원격 worktree 가 그 해시를 쓴다).

■ 0. 아무것도 쓰기 전에 (이 순서를 어기면 충돌을 스스로 만든다)
- 파일을 고치거나 커밋하지 않는다 (open_items · 메모 · 시험 손질 모두 들인 뒤).
- 돌리고 결과를 한 줄씩 적는다:
    set -o pipefail
    git rev-parse --abbrev-ref HEAD                                       # claude/friendly-meitner-lldvar
    git status --short                                                    # 비어 있어야 한다
    git stash list | head -3
    git fetch origin claude/friendly-meitner-lldvar claude/evac-2026-11-12
    git log --oneline origin/claude/friendly-meitner-lldvar..HEAD         # 안 올린 로컬 커밋 — 0 이어야 한다
    git log --oneline -1 origin/claude/friendly-meitner-lldvar            # 37fb17f49 (litdb: _curation status — N-82 끝 …) 이거나 그 뒤 litdb 커밋
    git log --oneline -1 origin/claude/evac-2026-11-12                    # 'Evacuation return card 2026-11-17' 커밋이어야 한다
    git merge-base --is-ancestor origin/claude/friendly-meitner-lldvar origin/claude/evac-2026-11-12 && echo FF가능
  ⚠ evac 끝이 복귀 카드 커밋이 아니면 (그 뒤에 누가 올렸다) 목록을 사용자에게 보이고 그대로 들여도 되는지 묻는다.
  ⚠ FF가능이 안 나오면 (litdb 정리 세션이 37fb17f49 뒤로 또 올렸다) ■1 경우 C.
  ⚠ 컨테이너가 새로 떠서 HEAD 가 이미 friendly 원격 끝이면 그대로 경우 A.

■ 1. 들이기 — 경우를 먼저 가른다
- 경우 A (기대) — status 비었음 · 로컬 전용 커밋 0 · FF가능:
    git merge --ff-only origin/claude/friendly-meitner-lldvar      # 로컬 friendly 를 원격 끝으로 (이미 같으면 그대로)
    git merge --ff-only origin/claude/evac-2026-11-12
  → ■2 점검 → git push origin claude/friendly-meitner-lldvar      (강제 없이 · 거절되면 fetch 해서 ■0 부터 — 그 사이 litdb 정리 세션이 올렸을 수 있다)
- 경우 B — 커밋 안 한 변경이 있다: git stash push -u -m "pre-return-2026-11-17" → 경우 A → git stash pop (충돌은 ■3 · 푼 diff 를 사용자에게 보이고 허락 뒤 커밋).
- 경우 C — friendly 가 또 움직였다 (FF 불가):
    git log --format='%h %an %ad %s' origin/claude/evac-2026-11-12..origin/claude/friendly-meitner-lldvar   # 전부 'litdb: …' 인지
    git merge-tree --write-tree --name-only origin/claude/friendly-meitner-lldvar origin/claude/evac-2026-11-12   # CONFLICT 줄
  전부 litdb 정리 커밋이고 충돌이 없거나 litdb/figures/_sources.json 하나뿐이면 사용자에게 알리고:
    git merge --ff-only origin/claude/friendly-meitner-lldvar
    git merge --no-ff origin/claude/evac-2026-11-12 -m "merge claude/evac-2026-11-12 (대피 세션 11-12~11-17) — no-ff"
  (_sources.json 충돌은 ■3 규칙으로 푼다.) 그 밖의 커밋 · 충돌이면 멈추고 사용자에게 묻는다.
  ⛔ rebase · reset · force-push 하지 않는다 — evac 커밋 해시가 결정 원장 비준 (ratification.commit) · 런로그 · 원격 worktree 에 박혀 있다
     (kgy ~/wt_hj2a = dbacec12e · gabia /data/work/runs/b2o3_bo_2026_11_09 의 src).

■ 2. 점검 — 들인 뒤 (대피 세션 11-17 실측 = 기대값)
    python3 tools/kb_wiki.py lint | tail -1                            # RESULT: 0 errors
    python3 tools/db/validate_canonical.py | tail -3                   # 거버넌스 결정 193 · 판정 8 · 그래프 무결성 ✅ / ✅ 배선 전부 일치
    python3 tools/convention_check.py | tail -1                        # 0 위반
    python3 tools/litdb/build_index.py --check > /tmp/litdb_check.txt; echo rc=$?   # rc=0 (표 칸 ⚠ 69 · 148 · 120 은 옛 경고 — 숫자가 늘면 본다)
    python3 tools/litdb/build_index.py --selftest | tail -1            # selftest: 35 통과 / 0 실패
    ~/.venvs/litdb/bin/python3 tools/litdb/extract_figures.py --selftest | tail -1   # 117 통과 / 0 실패 (venv 가 없으면 건너뛰고 적는다)
    python3 tools/figures/plot_mixing_curves.py --selftest | tail -1  # selftest PASS (13 ok · 0 bad)
    python3 tools/oxidation/interface_reactivity_v2.py --selftest | tail -1   # pymatgen 있으면 'selftest PASS' (✓ 줄 178) · 없으면 '[전제]' 불통과 = 정상
    python3 -m pytest webapp/tests -q -p no:cacheprovider | tail -2    # 662 passed, 1 skipped (대피 세션 실측 7 분 42 초)
  기대와 다르면 고치기 전에 원인부터 (들이기 탓인지 · 환경 탓인지).

■ 3. 충돌이 나면 (경우 B · C) — 파일별 규칙
- litdb/figures/_sources.json — 키 합집합 (같은 키가 양쪽에서 다르면 멈추고 묻는다) ·
  저장 json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) · 끝 줄바꿈 없음 (extract_figures.py 출력과 같다).
- litdb/INDEX.md · comparison_vs_ours.md · pdf_map.tsv — 행 합집합 (옛 행 · 순서 안 바꿈) → python3 tools/litdb/build_index.py (INDEX_DEM 다시) → --check rc 0.
- db/governance/decisions.json — id 합집합 · 비준된 결정 본문은 한 글자도 고치지 않는다 (decision_digest) · json.dumps(…, ensure_ascii=False, indent=1) + "\n" · 푼 뒤 validate_canonical.py.
- kb/open_items.md — 합집합 · 머리 '최종 갱신' 은 늦은 쪽 (대피 세션 줄 2026-11-17).
- kb/index.md · kb/reviews/INDEX.md — 손으로 풀지 않는다: 아무 쪽이나 고르고 python3 tools/kb_wiki.py index · python3 tools/kb_wiki.py reviews --write → lint.
- db/file_comments.json · db/file_highlights.json · db/note_images/ (로컬 웹앱 메모) · litdb/_curation/ — 대피 세션은 안 건드렸다 · friendly 쪽 그대로.
- CLAUDE.md — 대피 세션 판이 원장과 맞다 (■4 의 다섯 곳).

■ 4. 네 기억은 11-12 에 멈춰 있다 — 들인 뒤 먼저 다시 읽는다
- CLAUDE.md 를 다시 읽는다. 대피 중 바뀐 곳 다섯:
  ① li2s 계열 전부 닫음 (11-16 · 새 li2s 카드 · 트랙 · 런을 제안하지 않는다)
  ② [혁주] 트랙 줄 — 1저자 = 혁주 (사용자 확인 11-16) · 사용자 = 계산 담당 · 계산 쪽 결정은 '사용자'
  ③ 회의록 바탕 외부 과제 문서에는 기업 이름 · 기업 얘기를 넣지 않는다 (제목 · 파일 이름 포함 · 봉인 원장은 그대로)
  ④ vc-relax 예외 목록에 [혁주] Li₂ZrO₃ 띠틈 1 잡
  ⑤ 카드 원문 절의 값을 말하기 전에 같은 파일의 ⏩_개정_* 키와 원장 amend 항목부터 본다 (11-16 b2o3 2 단계 온도 실수)
- kb/open_items.md 머리 '지금 상태' 목록 (grep -n "지금 상태" kb/open_items.md | head -2) — b2o3 · Ag–C 인터레이어 · [혁주] 줄.
- kb/projects/handoff_2026_11_17_return_to_origin.md (이 카드) §1–§4 · [혁주] 요약 kb/projects/hyeokju_lzo_interface_2026_11_16.md.

■ 5. 원장에서 바뀐 것 (대피 중 새 결정 8 · 바뀐 옛 결정 0 · 트랙을 먼저 쓴다 · 원장이 정본)
- b2o3 UMA-MD (1저자 = 사용자): D-2026-11-13-b2o3-bo-placement-amend5-dft active (9 단계 DFT).
- li2s-3 (논문 1저자 = 외부 · 위임 10-30): D-2026-11-14-li2s3-queue-endline-lost-ack · D-2026-11-16-li2s3-dense-protocol-ensemble-closed active — li2s 계열 끝 (재개 조건 없음).
- Ag–C 인터레이어 과제 (결정 = 사용자): D-2026-11-16-sdi-agc-ag2s-window active (Q2 · 결과를 본 뒤 사용자 명시 승인) · Q3 MD 보류 (카드 메모) ·
  결정 id · 카드 파일 이름의 옛 표기는 봉인 원장이라 그대로 둔다 (CLAUDE.md ③ — 문서 · 내려받기 판에서만 뺐다).
- [혁주] (1저자 = 혁주 · 계산 쪽 결정 = 사용자): D-2026-11-16-hyeokju-lzo-stage1-reactivity active (1 단계 끝 · 카드 결과_2026_11_16) ·
  D-2026-11-16-hyeokju-lzo-stage2a-li2zro3-gap active · D-2026-11-16-hyeokju-lzo-stage2a-li2zro3-gap-amend1 **proposed** · D-2026-11-16-hyeokju-lzo-md **proposed**.
  ⚠ 마지막 둘은 사용자가 11-17 00:1x 채팅으로 '승인' 했는데, 대피 세션이 원장에 비준을 쓰려 하자 세션 권한 검사가 막았다
  (채팅 한마디로 대신 승인 기록을 남기는 것은 안 된다는 판정 · 앞의 1 단계 · 2a 비준은 AskUserQuestion 답으로 기록됐다).
  → 들인 뒤 AskUserQuestion 으로 두 결정을 하나씩 물어 (2a 개정 1 = 컷오프 탐침 90/720 · P2O5 대조 잡 늘 먼저 / MD = G1 힘 MAE ≤ 0.10 eV/Å · 원소별 ≤ 0.15 · G2 상대 에너지 ≤ 5 meV/atom)
     명시 승인을 받고 기록한다. 그래도 막히면 사용자에게 권한 규칙 추가 또는 원장 proposed 유지를 묻는다. 2a 결과 판독은 개정 1 기록 뒤.

■ 6. 원격 (대피 세션 마지막 실측 · 11-17 00:13 KST)
- kgy — [혁주] 2a 띠틈 tmux hjgap (11-17 00:12:54 시작 · commit dbacec12e · R=/home/kgy/work/runs/hj_s2a_1116 · worktree ~/wt_hj2a):
  P2O5 대조 잡 vc-relax → control_gate (|Δ| ≤ 0.02 eV) → Li₂ZrO₃ 60/480 → 90/720 탐침. 감시:
    watch -n 30 'tail -5 /home/kgy/work/runs/hj_s2a_1116/run.log; nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader'
  끝나면 main/ · ecut90/ 의 gap.json · control_gate.json 을 회수해 카드 개정 1 규칙 (|ΔE_g| ≤ 0.02 eV 면 60/480 값 · 넘으면 90/720 값) 으로 판독한다.
  ⛔ 다 끝날 때까지 ~/wt_hj2a 를 지우지 않는다.
- gabia — b2o3 9 단계 기준 셀 이완 3 (11-16 09:17:51 시작 · tmux b2o3_s9rx · 잡마다 GPU 독점 · runlog 9단계_이완_시작_2026_11_16) →
  끝나면 read_relax 블록. 이어지는 순서는 open_items b2o3 줄 (read_relax → 10 고르기 → 11a 포논 → 11b 골격 열적 안정
  (개정 1 온도 300 / 600 / 800 / 1000 K · 650 / 700 은 시간 남으면 · 넣기 전에 개정) → 12a / 12b).
  [혁주] 1 단계 MP 계산은 끝났다 (gabia worktree /data/work/wt_hj 지움).
- ⚠ 이제부터 원격 회수 · push 블록은 friendly 로 보낸다 (evac 로 보내지 않는다). 메인 저장소 경로: gabia /data/work/repo · kgy /home/kgy/Yonghoon-DEM-DFT
  (~/lldvar 는 linked worktree). 원격 push 는 자격 증명을 묻는다 — Password 칸에는 GitHub 토큰 (11-16 gabia 에서 비밀번호로 한 번 실패).

■ 7. litdb 정리 세션 맞추기 (그 세션이 friendly 에 직접 쓴다)
- 들이고 push 한 뒤 사용자에게 말한다: litdb 정리 세션에 복귀 카드 §0b 를 붙여 넣어 달라고 —
  그 세션이 다음 커밋 전에 git merge --ff-only origin/claude/friendly-meitner-lldvar 로 대피 커밋을 받아야 push 가 거절되지 않는다.
- 대피 중 litdb 에 들어간 것: digest 6 편 (chen2024 · wei2026 · ahmed2026 · warren2026 · liu2026 · hu2026 — INDEX.md · comparison_vs_ours.md J-76–81 ·
  _sources · pdf_map 행 덧붙임) · tools/litdb/extract_figures.py 고침 셋 (SI 캡션 블록 빈 줄 · 원소 기호 'In' 캡션 · 아래 캡션 SI 표 · selftest 117).

■ 8. 사용자 로컬 웹앱 (127.0.0.1:5001 은 사용자 로컬 체크아웃을 읽는다)
들이고 push 한 뒤 사용자에게 직접 말한다:
- 로컬이 대피 브랜치에 있으면: git switch claude/friendly-meitner-lldvar && git pull --ff-only · friendly 에 있었으면 git pull --ff-only.
- 서버를 다시 띄운다 (용어집 등은 시작 때 읽는다).
- 메모 저장 (notes 커밋) 은 friendly 에 쓰므로, 로컬이 뒤처진 채 메모를 저장하면 push 가 거절된다 — pull 먼저.
- 볼 만한 화면: 판정 원장 (결정 193 · 대피 중 새 8 · proposed 둘) · 미결 리스트 머리 (b2o3 · Ag–C 인터레이어 · [혁주] 줄).
```

## 0b. litdb 정리 세션에 붙여 넣을 프롬프트

```text
[litdb 정리 세션 — 대피 브랜치 들이기 뒤 맞추기 (2026-11-17)]

friendly (claude/friendly-meitner-lldvar) 에 대피 세션 (claude/evac-2026-11-12) 커밋이 fast-forward 로 들어왔다
(본 세션이 복귀 카드 kb/projects/handoff_2026_11_17_return_to_origin.md 대로 들였다). 너의 228 커밋은 그 안에 그대로 있다 (대피 세션이 먼저 머지했다).
다음 커밋 전에:
    git status --short     # 하던 카드 작업이 있으면 커밋하지 말고 git stash push -u -m "pre-pull-2026-11-17" → 받기 → git stash pop
    git fetch origin claude/friendly-meitner-lldvar && git merge --ff-only origin/claude/friendly-meitner-lldvar
    git merge-base --is-ancestor 6a90650b4 HEAD && echo 대피커밋_들어옴    # 안 나오면 본 세션이 아직 안 들였다 — 사용자에게 알리고 본 세션 push 뒤 다시 받는다
    python3 tools/litdb/build_index.py --check > /tmp/litdb_check.txt; echo rc=$?          # rc=0
    ~/.venvs/litdb/bin/python3 tools/litdb/extract_figures.py --selftest | tail -1          # 117 통과 / 0 실패
들어온 것 중 너와 겹치는 것:
- digest 6 편 — chen2024_space_charge_layer_ncm_linbo3_lpscl · wei2026_data_driven_hea_mediator_lis · ahmed2026_co_substituted_llzto_sintering_atmosphere ·
  warren2026_liquid_phase_thiophosphate_lpscl_synthesis · liu2026_in_substituted_li10snp2s12_electronic_structure · hu2026_interphase_adaptive_yb_chloride_se.
  INDEX.md · comparison_vs_ours.md (J-76–81) · figures/_sources.json · pdf_map.tsv 에 행 · 항목만 덧붙였다 — 이 행 · 항목은 고치거나 지우지 않는다.
- figures/_sources.json 은 대피 쪽에서 키 합집합으로 머지됐다 (564 키 · 너의 57 새 키와 lyu2025 · zhang2026 값 그대로).
- tools/litdb/extract_figures.py 고침 셋 — SI 캡션 블록의 빈 줄 · 원소 기호 'In' 으로 시작하는 캡션 · 캡션이 아래에 오는 SI 표. 다음 추출부터 이 판이다.
그 다음 하던 일 (N-84 …) 을 잇는다.
⛔ 대피 브랜치 (claude/evac-2026-11-12) 에 쓰지 않는다 · rebase · force 하지 않는다 · 받기 전에 push 하지 않는다.
```

## 1. 이 대피 세션에서 한 것 (11-12 오후 ~ 11-17 새벽 · 커밋 68 + 머지 1)

- **b2o3**: 1 단계 8 단계 끝 → 8b 진단 → 9 단계 DFT 도구 v1 → v6 (Codex EF–EK) · 단일점 6 · k 탐침 3 · 기준 셀 이완 3 (gabia 진행 중) · 2 단계 온도 메모 (개정 1 값 300 / 600 / 800 / 1000 K).
- **li2s-3**: 2 단계 판독 → 닫음 → li2s 계열 끝 (11-16).
- **litdb**: 6 편 · 추출기 고침 셋 · 방법 정본 SCL 표에 Chen 2024.
- **사수 11-13 세미나 검토 · 6 월 덱 유효성 대조** (`kb/results/MASTER_structure_property_logic_2026_06_21.md` 머리 배너).
- **Ag–C 인터레이어 과제**: Q1 · Q2 계산 · 그림 1–3 (`docs/figures/sdi_agc/` · CSV 는 db/properties) · 보고서 (Claude Docs 문서 + 내려받기 판
  `docs/collab/agc_interlayer_crack_calc_2026_11_16.html` — 처음 보는 대학원생용 보고서 꼴 · 기업 이름 뺌) · Q3 MD 보류.
- **[혁주]**: 트랙 정의 · 1 단계 열역학 끝 (그림 `docs/figures/hyeokju_lzo/`) · 2a 띠틈 (kgy 도는 중) · MD 카드 (proposed).
- **도구**: `interface_reactivity_v2.py` 조회 캐시 (chemsys 마다 한 번) · `plot_li_uptake_profile.py` · `plot_mixing_curves.py` (새).

## 2. 사용자가 정할 것 (넘겨받는 질문)

- [혁주] 2a 개정 1 · MD 문턱 — 명시 승인 기록 (§0 ■5).
- [혁주] LZO (Li₂ZrO₃) 안정 전압 계산을 따로 할지 — 1 단계 열린계에서 LZO 가 3.5 V 부터 자체 분해 쪽이었다 (카드 밖 관찰 · 기록만).
- [혁주] 혁주 자료 대기 — 정확한 조성 · 전압 기준 (Li–In 인지) · 화성 충전 용량 · 요청 문서 4 쪽.
- Ag–C: '왜 Li 에 닿으면 0 V 인가' 설명 상자를 보고서 2 절에 넣을지.
- cascade DFT 확인 후보 · `/ro_st4.log` 지우기 (옛 대기).

## 3. 복귀 체크리스트

- [x] `git merge-tree --write-tree` 로 가상 머지 → 충돌 1 (`_sources.json`) → 대피 브랜치에서 먼저 `--no-ff` 머지 (`9c2276537`) · 키 합집합
- [x] 머지 뒤 생성 파일 다시 만들기 (`6d570f45e`) · lint 0 · validate ✅ · 규약 0 · litdb `--check` rc 0 · build_index 35/0 · extract_figures 117/0
- [x] 웹앱 시험 — 아래 줄
- [ ] friendly 쪽 `git merge --ff-only origin/claude/evac-2026-11-12` (본 세션 · §0)
- [ ] litdb 정리 세션 받기 (§0b) · 사용자 로컬 웹앱 pull (§0 ■8)
- [ ] [혁주] 비준 둘 기록 (§0 ■5) · 2a 결과 판독 · b2o3 read_relax

웹앱 시험 (대피 세션 · 머지 뒤 · 11-17): **662 passed · 1 skipped · rc 0** (`python3 -m pytest -q -x -p no:cacheprovider webapp/tests/` · 461.8 초).
