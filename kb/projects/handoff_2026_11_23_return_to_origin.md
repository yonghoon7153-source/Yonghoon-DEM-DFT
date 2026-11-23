---
title: "본 세션 복귀 카드 — 대피 브랜치 claude/evac-2026-11-20 를 friendly 로 · fast-forward (2026-11-23) · litdb 정리 세션 · 로컬 웹앱 · W_ad ES 편지는 본 세션에서"
date: 2026-11-23
updated: 2026-11-23
tags: [merge, handoff, return, evacuation, litdb, webapp, gabia, kgy, b2o3, wad, hyeokju]
status: 발송 대기 — 사용자가 §0 을 본 세션 (friendly) 에, §0b 를 litdb 정리 세션에 붙여 넣는다
confidence: medium
verificationStatus: verified
verifiedAt: 2026-11-23
verifiedBy: self
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: single-source
---


# 본 세션 복귀 카드 — `claude/evac-2026-11-20` → `claude/friendly-meitner-lldvar`

> 선례: `kb/projects/handoff_2026_11_17_return_to_origin.md` · 대피 인계 `kb/projects/handoff_2026_11_20_evacuation.md` ■5 · ■6
> (friendly 가 움직였으면 대피 브랜치에서 먼저 `--no-ff` 머지 · friendly 쪽은 ff-only).
> 실측 (2026-11-23 · 대피 세션):
> · merge-base = **`6e3b12186`** (대피 인계 카드 11-20). 그 뒤 friendly 에 **litdb 정리 세션 커밋 60 개** (끝 **`7e1959c79`** ·
>   *'litdb: _curation status — N-155 끝 (5d694fff7) · N-156 도는 중 …'*) — 60 개 전부 `litdb: …` 커밋이다.
> · 대피 세션이 그 60 개를 **대피 브랜치로 먼저 `--no-ff` 머지**했다 (`b17141d58`). **충돌 0** — 두 쪽이 같이 바꾼 파일 셋
>   (`litdb/INDEX.md` · `litdb/comparison_vs_ours.md` · `litdb/figures/_sources.json`) 은 git 이 자동으로 합쳤고 `_sources.json` 은 JSON 으로 읽힌다 (606 키).
> · 머지 뒤 생성 파일 다시 만들기 (kb index 날짜 줄) · 이 카드 · open_items 머리 — 같은 커밋 ('Evacuation return card 2026-11-23').
> · 점검 (= §0 ■2 기대값): kb lint 0 errors · 결정 204 · 판정 8 · 그래프 ✅ · 배선 일치 · 규약 0 위반 · litdb `build_index.py --check` rc 0
>   (표 칸 ⚠ 은 옛 '표 중간 빈 줄' 경고) · build_index selftest 35/0 · 웹앱 시험은 §3 끝 줄.
> · 그래서 friendly 쪽 들이기는 **fast-forward** 다 — 단 litdb 정리 세션이 friendly 에 계속 쓰므로, `7e1959c79` 뒤로 또 움직였으면 §0 ■1 경우 C.
> · `origin/main` 은 이 캠페인과 무관 — main 으로 머지하지 않는다.

## 0. 본 세션 (friendly) 에 붙여 넣을 프롬프트

```text
[본 세션 복귀 — 2026-11-23 · 대피 브랜치 claude/evac-2026-11-20 들이기]

너는 Yonghoon-DEM-DFT 캠페인의 본 세션이다 (브랜치 claude/friendly-meitner-lldvar). 11-20 밤 사용 한도에 걸려서 사용자가 대피 세션
(브랜치 claude/evac-2026-11-20) 으로 옮겼다. 네가 올린 마지막 커밋은 대피 인계 카드 6e3b12186 다. 그 뒤 friendly 에는 litdb 정리 세션의
커밋 60 개 (끝 7e1959c79) 가 올라갔고, 대피 세션이 그 60 개를 대피 브랜치로 먼저 머지해 두었다 (b17141d58 · 충돌 0).
그래서 들이기는 fast-forward 다. 할 일: 대피 커밋을 충돌 없이 들이고 → 점검 → push → litdb 정리 세션과 사용자 로컬 웹앱을 맞춰 주고
(■8 · ■9) → 원장 · 기록으로 상태를 다시 맞춘 뒤 이어서 일한다. W_ad Codex ES 편지 회신은 이 세션에서 받는다 (■7).
⛔ origin/main 으로 머지하거나 push 하지 않는다 · '원래 브랜치' 는 friendly 다 · 대피 브랜치는 지우지 않는다 (기록 · 원격 worktree 가 그 해시를 쓴다).

■ 0. 아무것도 쓰기 전에 (이 순서를 어기면 충돌을 스스로 만든다)
- 파일을 고치거나 커밋하지 않는다 (open_items · 메모 · 시험 손질 모두 들인 뒤).
- 돌리고 결과를 한 줄씩 적는다:
    set -o pipefail
    git rev-parse --abbrev-ref HEAD                                       # claude/friendly-meitner-lldvar
    git status --short                                                    # 비어 있어야 한다
    git stash list | head -3
    git fetch origin claude/friendly-meitner-lldvar claude/evac-2026-11-20
    git log --oneline origin/claude/friendly-meitner-lldvar..HEAD         # 안 올린 로컬 커밋 — 0 이어야 한다
    git log --oneline -1 origin/claude/friendly-meitner-lldvar            # 7e1959c79 (litdb: _curation status — N-155 끝 …) 이거나 그 뒤 litdb 커밋
    git log --oneline -1 origin/claude/evac-2026-11-20                    # 'Evacuation return card 2026-11-23' 커밋이어야 한다
    git merge-base --is-ancestor origin/claude/friendly-meitner-lldvar origin/claude/evac-2026-11-20 && echo FF가능
  ⚠ evac 끝이 복귀 카드 커밋이 아니면 (그 뒤에 누가 올렸다) 목록을 사용자에게 보이고 그대로 들여도 되는지 묻는다.
  ⚠ FF가능이 안 나오면 (litdb 정리 세션이 7e1959c79 뒤로 또 올렸다) ■1 경우 C.
  ⚠ 컨테이너가 새로 떠서 HEAD 가 이미 friendly 원격 끝이면 그대로 경우 A.

■ 1. 들이기 — 경우를 먼저 가른다
- 경우 A (기대) — status 비었음 · 로컬 전용 커밋 0 · FF가능:
    git merge --ff-only origin/claude/friendly-meitner-lldvar      # 로컬 friendly 를 원격 끝으로 (이미 같으면 그대로)
    git merge --ff-only origin/claude/evac-2026-11-20
  → ■2 점검 → git push origin claude/friendly-meitner-lldvar      (강제 없이 · 거절되면 fetch 해서 ■0 부터 — 그 사이 litdb 정리 세션이 올렸을 수 있다)
- 경우 B — 커밋 안 한 변경이 있다: git stash push -u -m "pre-return-2026-11-23" → 경우 A → git stash pop (충돌은 ■3 · 푼 diff 를 사용자에게 보이고 허락 뒤 커밋).
- 경우 C — friendly 가 또 움직였다 (FF 불가):
    git log --format='%h %an %ad %s' origin/claude/evac-2026-11-20..origin/claude/friendly-meitner-lldvar   # 전부 'litdb: …' 인지
    git merge-tree --write-tree --name-only origin/claude/friendly-meitner-lldvar origin/claude/evac-2026-11-20   # CONFLICT 줄
  전부 litdb 정리 커밋이고 충돌이 없거나 litdb 파일뿐이면 사용자에게 알리고:
    git merge --ff-only origin/claude/friendly-meitner-lldvar
    git merge --no-ff origin/claude/evac-2026-11-20 -m "merge claude/evac-2026-11-20 (대피 세션 11-20~11-23) — no-ff"
  (litdb 충돌은 ■3 규칙으로 푼다.) 그 밖의 커밋 · 충돌이면 멈추고 사용자에게 묻는다.
  ⛔ rebase · reset · force-push 하지 않는다 — evac 커밋 해시가 결정 원장 비준 (ratification.commit) · 런로그 · 원격 worktree 에 박혀 있다
     (kgy ~/wt_bsite_1123 = ee2a5ea4 · W_ad 빌드 기록 ⑬–⑮ · b2o3 런로그).

■ 2. 점검 — 들인 뒤 (대피 세션 11-23 실측 = 기대값)
    python3 tools/kb_wiki.py lint | tail -1                            # RESULT: 0 errors
    python3 tools/db/validate_canonical.py | tail -3                   # 거버넌스 결정 204 · 판정 8 · 그래프 무결성 ✅ / ✅ 배선 전부 일치
    python3 tools/convention_check.py | tail -1                        # 0 위반
    python3 tools/litdb/build_index.py --check > /tmp/litdb_check.txt; echo rc=$?   # rc=0 (표 칸 ⚠ 은 옛 '표 중간 빈 줄' 경고 — 숫자가 늘면 본다)
    python3 tools/litdb/build_index.py --selftest | tail -1            # selftest: 35 통과 / 0 실패
    python3 tools/doping/b2o3_site_dft.py --selftest | tail -1         # selftest PASS (36/36)
    python3 tools/wad/build_a5_vasp_package.py --selftest | tail -1    # ✅ build_a5_vasp_package selftest 279/279 (몇 분)
    python3 -m pytest webapp/tests -q -p no:cacheprovider | tail -2    # 이 카드 §3 끝 줄의 수
  기대와 다르면 고치기 전에 원인부터 (들이기 탓인지 · 환경 탓인지).

■ 3. 충돌이 나면 (경우 B · C) — 파일별 규칙
- litdb/figures/_sources.json — 키 합집합 (같은 키가 양쪽에서 다르면 멈추고 묻는다) ·
  저장 json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True) · 끝 줄바꿈 없음 (extract_figures.py 출력과 같다).
- litdb/INDEX.md · comparison_vs_ours.md · pdf_map.tsv — 행 합집합 (옛 행 · 순서 안 바꿈) → python3 tools/litdb/build_index.py (INDEX_DEM 다시) → --check rc 0.
- db/governance/decisions.json — id 합집합 · 비준된 결정 본문은 한 글자도 고치지 않는다 (decision_digest) · json.dumps(…, ensure_ascii=False, indent=1) + "\n" · 푼 뒤 validate_canonical.py.
- kb/open_items.md — 합집합 · 머리 '지금 상태' 는 대피 쪽 (2026-11-23 밤).
- kb/index.md · kb/reviews/INDEX.md — 손으로 풀지 않는다: 아무 쪽이나 고르고 python3 tools/kb_wiki.py index · python3 tools/kb_wiki.py reviews --write → lint.
- db/file_comments.json · db/file_highlights.json · db/note_images/ (로컬 웹앱 메모) · litdb/_curation/ — 대피 세션은 안 건드렸다 · friendly 쪽 그대로.

■ 4. 네 기억은 11-20 에 멈춰 있다 — 들인 뒤 먼저 다시 읽는다
- CLAUDE.md 는 대피 중 바뀌지 않았다 (다시 읽을 필요는 있다 — 압축 뒤라면).
- kb/open_items.md 머리 '지금 상태 — 2026-11-23 (밤)' · '돌고 있는 것' 줄 · '사용자 결정 대기' 줄 (grep -n "지금 상태\|돌고 있는 것\|사용자 결정 대기" kb/open_items.md | head -5).
- 이 카드 §1 (대피 중 한 것) · §2 (진행 체크).

■ 5. 원장에서 바뀐 것 (대피 중 새 결정 4 · 전부 active · 바뀐 옛 결정 0 · 트랙을 먼저 쓴다 · 원장이 정본)
- [혁주] (1저자 = 혁주 · 계산 쪽 결정 = 사용자): D-2026-11-22-hyeokju-lzo-md1-amend3 (생산 시작 때 이미 문턱 안이던 쌍은 판정에서 뺀다) →
  MD-1 판정 (P–O 개시 없음 · Zr–S 시드 하나에서만) — 문장은 카드 ⏩_2026_11_22_MD1_판정 의 허용 문장에서만.
- b2o3 UMA-MD (1저자 = 사용자): D-2026-11-23-b2o3-bo-11b-cap-continue (11b 큐가 상한 150 h 에서 서면 이어 띄우기 · RESUME=1) ·
  D-2026-11-23-b2o3-bo-placement-amend6-relax2 (9 단계 가족마다 2 번 후보 이완 셋 · 판독 규칙 (a)–(d) 결과 전 · DFT 합계 상한 200 GPU-h ·
  11b 이어 돌리기 먼저 · Codex 확인 없음 · 도구 tools/doping/b2o3_bo_dft_relax2.py 는 아직 없다).
- 우리 DFT 기준선 (B₂O₃ · 1저자 = 사용자): D-2026-11-23-b2o3-site-dft (B-P 대 B-Li DFT 형성 에너지 · 같은 출발물 (host + B₂O₃ + Li₂S/Li₃PS₄) 반응 에너지 ·
  10월 UMA 후보 + O 가 B 에 붙은 짝 (사용자 선택) · 기준상 넷 vc-relax 허락 · 판정 |D| ≥ 0.10 eV/B · 원자당 (자유 원자 기준 · Wang 2025 Fig. S3 식) 값은 안 쓴다 · 기계 kgy).

■ 6. 원격 (대피 세션 마지막 실측)
- gabia — b2o3 11b 골격 열적안정 MD (tmux b2o3_s11b · 11-23 10:01:09 발사 · 속도 29.4 ps/h 한 줄 · 어림 끝: 대조 11-25 17시 · cfg0040 11-28 02시 ·
  cfg0015 11-30 11시 · 넷째 cfg0019 는 상한 150 h 에 걸려 큐가 선다) → 서면 런로그 11b_이어돌리기_규칙_2026_11_23 의 이어 띄우기 블록
  (db/properties/b2o3_bo_placement_stage1_runlog_2026_11_09.json · 결정 cap-continue) → 그 뒤 개정 6 이완 셋 → 12a/12b.
  감시 = 같은 런로그 11b_감시_v2_2026_11_23. 그동안 gabia GPU pw.x 못 쓴다.
- kgy — B 자리 DFT 카드: O 를 B 옆으로 옮긴 조합 239 개 UMA 이완 (tmux bsite_ob0 · 11-23 22:50:20 시작 · 22:51 에 1/239 ·
  남의 python3 (PID 43160 · 7.4 GB · GPU 100 %) 와 나눠 씀 · 사용자 선택 · worktree ~/wt_bsite_1123 = ee2a5ea4 ·
  출력 ~/work/runs/b2o3_site_dft_2026_11_23/uma_ob_combos). 감시: watch -n 30 'bash $HOME/w_bsite_ob0.sh'.
  끝나면 tools/doping/b2o3_site_dft.py pick_ob (바탕마다 최저 하나 → 12) → 10월과 같은 어닐 블록 (500 K × 20 ps · SEED 20261014) →
  자리 × O 꼴 UMA 최저 셋 → DFT 메모리 프로브 (GPU 가 빈 뒤 · kgy 는 프로세스별 조회 권한이 없다 — 메모리 사용량 · 사용률로 본다) →
  단일점 12 + 기준상 넷 vc-relax. 런로그 db/properties/b2o3_site_dft_runlog_2026_11_23.json (블록 1 · 1b · 1c 와 결과).
  ⛔ B 자리 카드가 끝날 때까지 ~/wt_bsite_1123 를 지우지 않는다.
- ⚠ 들인 뒤부터 원격 회수 · push 블록은 friendly 로 보낸다 (evac 로 보내지 않는다). 메인 저장소 경로: gabia /data/work/repo · kgy ~/lldvar
  (/home/kgy/Yonghoon-DEM-DFT 의 linked worktree). 원격 push 는 자격 증명을 묻는다 (Password 칸에는 GitHub 토큰).

■ 7. W_ad a5 — Codex ES 편지 (트랙 W_ad · 1저자 = 사용자) — 회신은 이 세션에서 받는다
- 편지 kb/reviews/codex_ES_prompt_wad_a5_er_fixes_2026_11_23.md (발송 대기 · 사용자가 보내는 글 사본을 받았다) ·
  기준 cc3873047 (ER 가 본 묶음) → 고침 19ddec83c · a6b34ffa6 · 1da64d0be · 묶음 MANIFEST 50beb026… · selftest 279/279 (메인 세션 재확인) ·
  돌연변이 전체 한 번 209/210 + 살아남은 m158 은 시험 하나 더해 홀로 빨강 (편지 §5 · 빌드 기록 ⑮ 에 경위).
- 회신이 오면: 원문을 kb/reviews/codex_ES_reply_wad_a5_er_fixes_2026_11_2x.md 로 그대로 (선례 codex_ER_reply_wad_a5_eq_fixes_2026_11_23.md) ·
  첨부는 kb/reviews/codex_ES_evidence_<날짜>/ · ES 편지 status 를 '발송 · 회신 수령' 으로 · 빌드 기록 ⑯ (db/properties/wad_a5_build_log_2026_11_20.json ·
  indent 2 · 끝에 덧붙임) · python3 tools/kb_wiki.py reviews --write · index · lint.
- NO-GO 면 고침 — a5 도구 (tools/wad/build_a5_vasp_package.py · build_v5_vasp_package.py) 와 db/inputs/wad_a5_vasp_2026_11_20/ 은 이제 본 세션 것이다.
  순서는 지난 회차와 같다: 반례를 지금 도구로 selftest 에 먼저 → 고침 → 시험 · 깨기 → 묶음 재빌드 (두 번 바이트 같음) → 빌드 기록 → 다음 편지 ET.
  사용자가 W_ad 회차가 길다고 했다 — 돌연변이 전체는 마지막 한 번만.
- GO 면 업체 발송은 사용자가 정한다 · DEM 편지 10 은 a5 가 끝난 뒤 (사용자 11-20).

■ 8. litdb 정리 세션 맞추기 (그 세션이 friendly 에 직접 쓴다)
- 들이고 push 한 뒤 사용자에게 말한다: litdb 정리 세션에 복귀 카드 §0b 를 붙여 넣어 달라고 —
  그 세션이 다음 커밋 전에 friendly 를 받아야 push 가 거절되지 않는다.
- 대피 중 litdb 에 들어간 것: digest 7 편 (11-23 — baseden2014 He 원자 손 DFT · kansara2026 ASSB 실험–계산 리뷰 · pandey2026 MXene 계면 리뷰 ·
  liu2026 Li-In-S 복합 포일 · lin2026 P 도핑 Li–S 리뷰 · zhang2026 AI 다중 척도 리뷰 · sun2026 SSB 계면 전기기계 Account) — INDEX.md ·
  comparison_vs_ours.md · figures/_sources.json 에 행 · 항목 덧붙임 · tools/litdb/extract_figures.py 고침 (본문 참조 끝 번호 대조 · selftest 138).

■ 9. 사용자 로컬 웹앱 (127.0.0.1:5001 은 사용자 로컬 체크아웃을 읽는다)
들이고 push 한 뒤 사용자에게 직접 말한다:
- 로컬이 대피 브랜치에 있으면: git switch claude/friendly-meitner-lldvar && git pull --ff-only · friendly 에 있었으면 git pull --ff-only.
- 서버를 다시 띄운다 (용어집 등은 시작 때 읽는다).
- 메모 저장 (notes 커밋) 은 friendly 에 쓰므로, 로컬이 뒤처진 채 메모를 저장하면 push 가 거절된다 — pull 먼저.
- 대피 중 webapp 에서 바뀐 것: app.py 7 줄 (주간 정리 11-16~11-22 /weekly 등록) · journal.jsonl 1 줄.

■ 10. 이어서 할 것 (open_items '사용자 결정 대기' 와 같다)
- b2o3: 개정 6 도구 (relax2 · prepare · read · 대조 잡 = 같은 판독 경로로 9 단계 판정 재현 · selftest 음성 · gabia 가 비기 전에) ·
  B 자리 카드 다음 블록 (pick_ob · 어닐) · 11b 감시 → 큐가 서면 이어 띄우기.
- W_ad: ES 회신 대기 (■7).
- [혁주]: 새 날짜 공유 보고를 언제 보낼지 (사용자) · MD-1 판정 뒤 더 돌릴지 (새 개정) · 혁주 자료 대기.
```

## 0b. litdb 정리 세션에 붙여 넣을 프롬프트

```text
[litdb 정리 세션 — 대피 브랜치 들이기 뒤 맞추기 (2026-11-23)]

friendly (claude/friendly-meitner-lldvar) 에 대피 세션 (claude/evac-2026-11-20) 커밋이 fast-forward 로 들어왔다
(본 세션이 복귀 카드 kb/projects/handoff_2026_11_23_return_to_origin.md 대로 들였다). 너의 60 커밋 (끝 7e1959c79) 은 그 안에 그대로 있다
(대피 세션이 먼저 머지했다 · 충돌 0).
다음 커밋 전에:
    git status --short     # 하던 카드 작업이 있으면 커밋하지 말고 git stash push -u -m "pre-pull-2026-11-23" → 받기 → git stash pop
    git fetch origin claude/friendly-meitner-lldvar && git merge --ff-only origin/claude/friendly-meitner-lldvar
      # 로컬에만 있는 커밋이 있어 ff-only 가 거절되면: git merge --no-ff origin/claude/friendly-meitner-lldvar (충돌은 행 합집합 · _sources.json 키 합집합)
    git merge-base --is-ancestor b17141d58 HEAD && echo 대피커밋_들어옴    # 안 나오면 본 세션이 아직 안 들였다 — 사용자에게 알리고 본 세션 push 뒤 다시 받는다
    python3 tools/litdb/build_index.py --check > /tmp/litdb_check.txt; echo rc=$?          # rc=0
    ~/.venvs/litdb/bin/python3 tools/litdb/extract_figures.py --selftest | tail -1          # 138 통과 / 0 실패 (venv 가 없으면 건너뛰고 적는다)
들어온 것 중 너와 겹치는 것:
- digest 7 편 — baseden2014_dft_by_hand_helium_atom · kansara2026_experiment_computation_integration_assb_review ·
  pandey2026_mxene_ion_conducting_interfaces_ssb_review · liu2026_li_in_s_composite_foil_built_in_field_li_lpscl ·
  lin2026_p_doped_compounds_li_s_review · zhang2026_ai_cross_scale_simulation_li_battery_review · sun2026_ssb_interface_electromechanical_gaps_account.
  INDEX.md · comparison_vs_ours.md · figures/_sources.json 에 행 · 항목만 덧붙였다 — 이 행 · 항목은 고치거나 지우지 않는다.
- tools/litdb/extract_figures.py — 본문 참조의 끝 번호 대조 (missing_labels ③ · ④ · 줄 끝 하이픈 잇기) · 다음 추출부터 이 판이다.
그 다음 하던 일 (N-156 …) 을 잇는다.
⛔ 대피 브랜치 (claude/evac-2026-11-20) 에 쓰지 않는다 · rebase · force 하지 않는다 · 받기 전에 push 하지 않는다.
```

## 1. 이 대피 세션에서 한 것 (11-20 밤 ~ 11-23 밤 · 커밋 78 + 머지 1)

- **b2o3** (1저자 = 사용자): 9 단계 기준 셀 이완 판독 (F_B 최저 · 승자–차저 0.471 eV/B₂O₃ · 압력 보정 0.447–0.455 · EOS 생략) → 10 단계 (F_B UMA 어닐 최저 3) →
  11a 포논 (셋 다 STABLE) → 11b 발사 (gabia) · 상한 뒤 이어 돌리기 (실행기 RESUME · 결정 cap-continue) · 개정 6 (9 단계 2 번 후보 이완 셋 · active) ·
  B 자리 (P 대 Li) DFT 형성 에너지 새 카드 (active) + 도구 tools/doping/b2o3_site_dft.py (selftest 36 · 깨기 13) · kgy 조합 UMA 이완 발사.
  ⚠ 9 단계 DFT 실제 ≈ 100.7 GPU-h 로 개정 1 상한 60 을 넘었던 것을 개정 6 에 적었다 (새 상한 200 은 사용자 비준).
- **W_ad a5** (1저자 = 사용자): 내부 EM NO-GO 고침 → Codex EN · EO · EP · EQ · ER NO-GO 고침 (작업자 · EQ 에서 위협 범위 §1b GO ·
  EQ 고침에서 fail-closed 트리 관문 하나로 구조를 바꿈) → ES 편지 발송 대기 · 묶음 MANIFEST 50beb026….
- **[혁주]** (1저자 = 혁주): MD-1 판독 (개정 3 · 판정).
- **litdb**: digest 7 편 · 추출기 끝 번호 누락 고침.
- **주간 정리** 11-16~11-22 (kb/reports/weekly_2026_11_22.md · /weekly 웹앱 등록).
- **정리**: 작업자 worktree 지움 · /tmp 의 옛 시험 폴더 지움 (디스크 여유 13 GB).

## 2. 복귀 진행 체크

- [x] friendly 의 litdb 정리 커밋 60 을 대피 브랜치로 먼저 머지 (`b17141d58` · 충돌 0)
- [x] 머지 뒤 점검 — lint 0 · 결정 204 · 판정 8 · 그래프 ✅ · 배선 일치 · 규약 0 · litdb --check rc 0 · build_index selftest 35/0 · 웹앱 시험 (아래 줄)
- [x] 이 카드 · open_items 머리 · kb index (같은 커밋)
- [ ] 본 세션 들이기 (§0)
- [ ] litdb 정리 세션 받기 (§0b) · 사용자 로컬 웹앱 pull (§0 ■9)

## 3. 웹앱 시험

웹앱 시험 (대피 세션 · 머지 뒤 · 11-23): 도는 중 (머지 뒤 시작 · 결과가 나오면 이 줄을 고친다 — 마지막 커밋 'Evacuation return card 2026-11-23')
