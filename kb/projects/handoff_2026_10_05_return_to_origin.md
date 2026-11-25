---
title: "origin 복귀·통합 카드 — claude/evac-2026-10-02 → claude/friendly-meitner-lldvar (2026-10-05 · no-ff)"
date: 2026-10-05
updated: 2026-10-05
tags: [merge, handoff, evacuation, return, no-ff, wad, p1b, li2s, cascade, litdb]
status: 발송 대기 — 사용자가 §0 프롬프트를 origin 세션에 붙여 넣는다
confidence: medium
verificationStatus: verified
verifiedAt: 2026-10-05
verifiedBy: self
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: single-source
---

# origin 복귀·통합 카드 — `claude/evac-2026-10-02` → `claude/friendly-meitner-lldvar`

> 짝: 대피할 때의 카드 `kb/projects/handoff_2026_10_02_evacuation.md` (origin → evac). 이 카드는 그 반대 방향이다.
> 머지 판단의 정본은 `kb/projects/merge_request_2026_10_05.md` (커밋 표 · 시험 · 원격 · 원장 변화 · 알려진 것 · 다음 일).
> 선례 `handoff_2026_09_29_return_to_origin.md` 는 fast-forward 였다. **이번엔 no-ff 다** — 대피 중에 DEM 쪽 litdb 세션이
> friendly 에 2 커밋을 넣었다 (`litdb/` 만). 실측 (10-05 밤 KST): 같은 병합을 가상으로 만들어 돌렸고 텍스트 충돌 0 · 웹앱 637 passed.

## 0. origin 세션에 붙여 넣을 프롬프트

```text
[origin 복귀 — 2026-10-05 · 대피 브랜치 claude/evac-2026-10-02 통합 · no-ff]

너는 Yonghoon-DEM-DFT 캠페인의 본 세션(브랜치 claude/friendly-meitner-lldvar)이다. 10-02 밤(KST)에 토큰이 다 차서
대피 세션(브랜치 claude/evac-2026-10-02)으로 일을 넘겼고, 그 세션이 10-03 ~ 10-05 에 65 커밋을 쌓았다. 그동안 friendly 에는
DEM 쪽 litdb 세션이 2 커밋을 넣었다 (e7f425b8 · 8e3d7a5d — litdb/ 만). 사용자가 복귀를 요청했다
("이제 다시 origin 대시보드/브랜치로 복귀 … 예전처럼 충돌되지 않고 잘 머지되게").
할 일: evac 커밋을 **no-ff 병합으로, 충돌 없이** friendly 로 들이고 이어서 일한다. 근거 문서는 병합 뒤 레포에 있다:
kb/projects/merge_request_2026_10_05.md · kb/projects/handoff_2026_10_05_return_to_origin.md · kb/open_items.md ⏭-NOW-z7 · z6.

■ 0. 아무것도 쓰기 전에 — 이 순서를 어기면 충돌을 스스로 만든다
- 파일을 고치거나 커밋하지 않는다 (open_items ⏭ 갱신 · 메모 · INDEX 재생성 같은 것도 병합 뒤에).
- 아래를 돌리고 결과를 한 줄씩 사용자에게 보인다:
    set -o pipefail
    git status --short                                   # 비어 있어야 한다 (아니면 ■1 경우 B)
    git stash list | head -3
    git fetch origin claude/friendly-meitner-lldvar claude/evac-2026-10-02
    git switch claude/friendly-meitner-lldvar
    git log --oneline origin/claude/friendly-meitner-lldvar..HEAD      # 안 올린 로컬 커밋 — 비어야 한다 (아니면 경우 D)
    git merge --ff-only origin/claude/friendly-meitner-lldvar          # 로컬 friendly 를 원격 끝으로 (DEM 커밋 둘을 받는다)
    F=origin/claude/friendly-meitner-lldvar; E=origin/claude/evac-2026-10-02; MB=$(git merge-base $F $E)
    git log -1 --format='%h %s' $MB | cut -c1-60        # 721f9538 대피 인계 카드 2026-10-02 …
    git rev-list --count $MB..$F                         # friendly 에만: 2 (DEM 세션이 더 넣었으면 그만큼 더)
    git rev-list --count $MB..$E                         # evac 에만: 65
    git log -1 --format='%s' $E | cut -c1-40             # 대피 세션 마감 — 복귀 카드 …
    git diff --name-only $MB $F | grep -v '^litdb/' | head            # 비어야 한다 (friendly 쪽 변경은 litdb/ 만)
    MT=$(mktemp); git merge-tree --write-tree --name-only --messages $F $E > $MT; echo "merge-tree rc=$?"; grep -c CONFLICT $MT; sed -n '2,12p' $MT
        # 기대: rc=0 · CONFLICT 0 · 'Auto-merging litdb/figures/_sources.json' 한 줄
        # (git < 2.38 이라 --write-tree 가 없으면 이 줄은 건너뛰고, ■1 병합이 충돌로 서면 git merge --abort 후 사용자에게)
  대피 세션 실측 (10-05 밤): friendly 8e3d7a5d · merge-base 721f9538 · friendly 에만 2 · evac 에만 65 · friendly 쪽 litdb/ 밖 변경 0 ·
  merge-tree rc 0 · CONFLICT 0. 같이 바꾼 파일은 litdb/figures/_sources.json 하나 (자동 병합 · 병합본 JSON 파싱 OK).

■ 1. 들이기 — 경우를 먼저 가른다
- 경우 C (기대하는 경우) — git status 비었음 · 안 올린 로컬 커밋 0 · friendly 쪽 변경이 litdb/ 만 · CONFLICT 0 · evac 에만 65:
    git merge --no-ff origin/claude/evac-2026-10-02 -m "merge claude/evac-2026-10-02 (대피 세션 10-03~10-05 · 65 커밋) — no-ff · 충돌 0"
    → ■2 점검 → git push origin claude/friendly-meitner-lldvar      (강제 없이)
  이 경우는 사용자가 요청한 그대로다 — 따로 묻지 않고 진행한다.
  push 가 non-fast-forward 로 거절되면 (DEM 세션이 그새 push) 사용자에게 알리고, 허락이면
  git fetch → git merge --no-ff origin/claude/friendly-meitner-lldvar → ■2 → push. (rebase 하지 않는다)
- 경우 A — friendly 에만 있는 커밋이 0 이면 (DEM 커밋이 사라졌을 리는 없으니 드물다): git merge --ff-only origin/claude/evac-2026-10-02 → ■2 → push.
- 경우 B — 커밋 안 한 변경이 있다: 내용을 사용자에게 보이고 묻는다. 허락이면
    git stash push -u -m "pre-evac-merge-2026-10-05"  →  경우 C  →  git stash pop
  pop 에서 충돌이 나면 ■3 규칙으로 풀되, stash 는 10-02 밤 이전 기준이라 evac 이 같은 곳을 이미 고쳤을 수 있다 —
  푼 diff 를 보이고 허락 뒤 커밋한다.
- 경우 D — 기대와 다르다 (안 올린 로컬 커밋 · friendly 쪽에 litdb/ 밖 변경 · CONFLICT · evac 에만 ≠ 65):
  멈추고 무엇이 다른지 사용자에게 보인다. 허락 뒤 경우 C 로 들이고 충돌은 ■3 규칙으로.
- ⛔ rebase · squash · cherry-pick 으로 들이지 않는다 — evac 커밋 해시가 결정 원장의 비준(ratification.commit · 13 건) ·
  기록 · 원격 러너 worktree 4 곳에 박혀 있다.
- evac 브랜치는 지우지 않는다 (기록이다). 병합 뒤 evac 에는 아무것도 push 하지 않는다.

■ 2. 점검 — 병합 뒤 · push 전 · 종료코드로 (대피 세션이 같은 병합을 가상으로 만들어 돌린 기대값을 옆에 적었다)
    python3 tools/db/validate_canonical.py | tail -3          # 거버넌스 결정 118 · 그래프 무결성 ✅ · '배선된 항목은 전부 원자료와 일치'
    python3 tools/kb_wiki.py lint | tail -1                    # RESULT: 0 errors
    python3 tools/convention_check.py | tail -1                # 0 위반
    python3 tools/litdb/build_index.py --check | head -2       # '어느 인덱스에도 없는 것 0편'
        # 떠 있는 표 행 ⚠ · DEM 비교문서 미편입은 대피 전부터 있던 상태다 (이번 병합과 무관)
    python3 -c "import json; json.load(open('litdb/figures/_sources.json')); print('sources ok')"
    python3 -m pytest webapp/tests -q -p no:cacheprovider | tail -2      # 637 passed · 2 skipped · 0 failed (6–7 분)
    python3 tools/wad/agc_graphite.py --selftest | tail -1                # 71 통과 · 0 실패 ✅
    SELFTEST=1 PY=python3 bash db/inputs/lpscl_glass_control_li3ps4_2026_10_05/run_quench_kgy.sh | tail -1   # selftest PASS (0 실패)
    python3 tools/doping/run_cascade_v7_probe.py --selftest | tail -1     # selftest PASS (0 실패)
    python3 -c 'import sys; sys.path.insert(0, "webapp"); from app import app; c = app.test_client(); [print(p, c.get(p).status_code) for p in ("/weekly", "/li2s", "/cascade/rebuild", "/adhesion", "/log")]'
        # 다섯 다 200 · /weekly 머리 = 주간 정리 2026-09-28 ~ 10-04 (대피 세션이 쓴 것)
  하나라도 기대와 다르면 push 하지 않고 원인부터 가른다 — 병합 때문인지, friendly 쪽 새 커밋 때문인지.
  ⛔ litdb/INDEX_DEM.md 를 병합 커밋에서 재생성하지 않는다. 재생성하면 날짜 줄 + DEM 논문 5편의 그림 수만 바뀐다
     (friendly 안에서 이미 낡아 있던 것 · DEM 세션 영역). 할 거면 따로 커밋한다.
  병합 뒤 CLAUDE.md 를 다시 읽는다 — 대피 세션이 gabia 예외 (5) 줄 · 상시 규칙 둘 (관측창 · 흡착 배위수) 을 더했다.

■ 3. 충돌이 나면 (경우 B·D) — 파일별 규칙
- litdb/figures/_sources.json — 양쪽 키 합집합 (같은 키에 값이 다르면 멈추고 묻는다) · 저장 뒤 json.load 로 확인.
- litdb/INDEX_DEM.md — 손으로 풀지 않는다. 아무 쪽이나 고른 뒤 python3 tools/litdb/build_index.py 로 다시 만든다 (생성물).
- litdb/INDEX.md · litdb/comparison_vs_ours.md (SE 축 · evac 이 신간 7편 추가) · litdb/comparison_vs_ours_DEM.md (DEM 세션) — 합집합.
  표 칸 수는 build_index.py --check 로 본다.
- db/governance/decisions.json — friendly 는 건드리지 않았다 (evac 판이 정본). 그래도 충돌이면 id 합집합 · 비준된 결정의 본문은 한 글자도
  고치지 않는다 (decision_digest = ratification 을 뺀 본문의 sha256) · 같은 slot 에 active 가 둘이면 검증기가 막는다 (해소는 supersedes 로만) ·
  저장은 json.dumps(d, ensure_ascii=False, indent=1) + "\n" · 푼 뒤 validate_canonical.py.
- kb/open_items.md — 합집합. evac 의 ⏭-NOW-z7 · z6 블록을 통째로 남기고 네 새 블록은 그 위에 얹는다. 머리 줄에 굵게를 겹쳐 쓰지 않는다
  (대시보드 시험이 깨진다).
- kb/index.md — 손으로 풀지 않는다. python3 tools/kb_wiki.py index → lint.
- CLAUDE.md — gabia 절 · 데이터 규율 절은 evac 판이 원장과 맞다. 다른 절의 네 변경은 살린다.
- db/pipelines/adhesion_pipeline.json — log 는 합집합 (끝에 붙인 줄) · 저장 indent=1 · 끝 줄바꿈 없음.
- 비준된 카드 · 리뷰 회신 원문 · 원자료(db/raw) — 어느 쪽도 내용을 고치지 않는다. 충돌이면 evac 판을 쓰고 이유를 커밋 메시지에 적는다.

■ 4. push 직후 사용자에게 꼭 말한다
- 사용자 로컬 (로컬 웹앱 127.0.0.1:5001 은 로컬 체크아웃을 읽는다):
      git switch claude/friendly-meitner-lldvar && git pull --ff-only
  그다음 웹앱 서버를 껐다 켠다 — webapp/app.py 가 바뀌었다 (/log 빈 구간 주석).
- 사용자는 10-05 에 로컬을 evac 로 옮기지 않기로 했다 ("또 혼선이 올 수 있으니까 webapp에는 나중에 반영하자"). 그래서 대피 세션 일
  (주간 정리 09-28~10-04 · /li2s v2 · cascade 재건 §17–19 · 점착 P1b 로그) 은 이 pull 뒤에야 로컬 화면에 뜬다.
  같이 볼 다섯 화면: /weekly · /li2s · /cascade/rebuild · /adhesion · /log.
- Render 배포본이 어느 브랜치를 따라가는지는 render.yaml 에 없다 (Render 대시보드 설정). friendly 를 따라가면 push 뒤에 뜬다.

■ 5. 원격에서 지금 도는 것 (마지막 실측: kgy 10-05 22:49 · gabia 10-05 20:50 KST) — 병합과 무관하게 계속 돈다. 건드리지 않는다.
- kgy (3090 24 GB · 프로세스별 GPU 정보 막힘):
  · cascade v7 탐침 (트랙 cascade = 사용자 1저자) — tmux cv7probe · worktree ~/wt_cv7probe_1003 @a2924895 · 10-03 20:24:38 발사 ·
    판독기가 다음 런을 고른다 · T* 또는 사다리 소진에서 멈춤 · 감시 tools/doping/watch_cv7probe.py --loop (러너 worktree 를 안 건드리고 git show).
    마지막 기록 (10-04): 800 K 탈락 · 1000 K H0 s1 자격 통과 · 누적 21.22 / 141 GPU-h.
  · li2s 대조 계 B 담금질 (⛔ 트랙 li2s = 외부 1저자 · 사용자는 실행 승인만) — tmux li3ps4q · worktree ~/wt_li3ps4_1005 @c704348b ·
    kgy 몫 seed1·2 · seed1 quench 50,000/450,000 (22:49 · 414 분) · seed3 자리 표시 파일에서 종료 코드 3 으로 멈추는 것이 설계다.
  · P1b (b) 나머지 넷 9×9×1 (트랙 W_ad = 사용자 1저자) — tmux agck9 · worktree ~/wt_agck9_1005 @6adf297c · 단계 시작 22:48:11 ·
    8 잡 한 잡씩 · 상한 벽시계 30 h (넘으면 다음 잡을 안 띄움) · 첫 잡 AGC_N3_top_hcp_K9_bound k 점 41 (8 잡 다 41 이어야) · 끝 어림 10-06 오후.
    결정 D-2026-10-05-wad-agc-graphite-k9-registry (active · 판독 규칙 결과 전 고정 · 10 잡 전부 OK 면 REPLACE · 아니면 마감 (a′) 그대로).
  · watch: ~/w_kgy_1005.sh (P1b k9 넷 · li2s · GPU).
- gabia (A6000 48 GB):
  · 탄성 modelc_2x (트랙 우리 DFT = 사용자 1저자) — tmux el_mc2x_1001 · strain_13_m 진행 (20:50 out 갱신 · pw.x 41,374 MiB).
  · li2s 대조 계 B 담금질 seed3 → 4 → 5 (⛔ 외부 1저자) — tmux li3ps4g · worktree /data/work/wt_li3ps4_1005 @17aced0b · MACHINE=gabia ·
    공존 예외 (5) D-2026-10-05-gabia-uma-coexist-elastic-li2s-control (active · 이 3 시드만 · 한 번에 하나 · 가드 ①–④ 가 우리 담금질만 죽이고
    예외를 닫는다) · seed3 20:48:40 시작 · watch /root/w_li3ps4_g.sh.
- 외주: 점착 V5 VASP 16 잡 (건엽 씨 · 파일럿 2 잡 OK · PP 등록부 봉인 a279d529) — 사용자가 지시 메시지를 보냈는지는 대피 세션이 모른다.
- ⛔ 위 러너 worktree 는 끝날 때까지 지우거나 다른 커밋으로 옮기지 않는다 (bash 는 스크립트를 조금씩 읽는다). 쉬는 것 (kgy ~/wt_agck12_1005 ·
  ~/wt_agc_1002) 은 정리해도 된다.
- ⚠ 병합 뒤 원격 회수 블록은 friendly 로 보낸다 — 형식은 대피 중 그대로 (kgy: git -C ~/lldvar fetch origin claude/friendly-meitner-lldvar →
  임시 worktree (FETCH_HEAD) → 원자료 rsync (tmp 제외) · SHA256SUMS → commit → git push origin HEAD:claude/friendly-meitner-lldvar →
  임시 worktree 제거). evac 로 보내지 않는다.

■ 6. 대피 세션이 한 일 — 트랙을 먼저 쓴다 (자세한 것: merge_request_2026_10_05 §2·§5 · open_items ⏭-NOW-z7·z6)
- 점착 W_ad (1저자 = 사용자): P1b Ag(111)|흑연 3층 — 기계 대조 G1 PASS (kgy = V100) · 1단계 7 relax · 2단계 31 SCF · G4 k 축 FAIL →
  k12 탐침 CONVERGED_AT_K9 → 마감 (a′) 라벨로 닫기 (D-2026-10-05-wad-agc-graphite-closed active) → 재개 ① (b) 나머지 넷 9×9×1 진행 중 ·
  V5 VASP 파일럿 반송 OK · PP 등록부 봉인 · W 값 정리 PPT 생성기 (숫자는 결과 기록에서만 · 화면에 안 올림).
- li2s (⛔ 외부 1저자): v2 회신 CO → 판독 전 개정 → 판독 (v2-2) → 회신 CQ → v2 마감 (active) · 대조 계 a-Li₃PS₄ 카드 (회신 CR · active) ·
  담금질 러너 · 비용 견적 오류 → 편지 CS → 회신 CS → 상한 140 · 넷이면 다섯째 (active) · gabia 공존 예외 (5) (active · 예외 (4) superseded) ·
  두 기계 발사 (A 담금질과 같은 시드–기계 대응 kgy 1·2 · gabia 3·4·5).
- cascade (1저자 = 사용자): 편지 CP → 회신 → v7 카드 + 개정 (active) · 판독기 온도 결속 · 탐침 러너·감시 · kgy 발사.
- ESW (1저자 = 사용자): E2b — 0.246 V 의 원인 = MP2020 황 음이온 보정 (인용위험 문구 · 등급 CONDITIONAL 유지).
- 상시 규칙 둘 (우리 DFT 기준선 · 사용자): 짧은 MD 관측창 · ≳2 eV 흡착값은 결합 자리 배위수부터 (CLAUDE.md 데이터 규율).
- litdb (SE 축 · 우리 쪽): 신간 7편 (wu2026 · nosrati2026 · sun2026 · cao2026 · qi2025 · yuan2026 · kim2026) · INDEX.md · comparison_vs_ours.md.
- 주간 정리 09-28~10-04 (/weekly) · 화면 갱신.

■ 7. 이어서 할 것 (순서) — merge_request_2026_10_05 §7 과 같다
1) ■4 사용자 로컬 안내 (pull · 서버 재시작 · 다섯 화면)
2) P1b (b) — kgy 8 잡이 끝나면 회수 (friendly 로) → tools/wad/agc_graphite.py --k9set_collect 레포 재집계 = kgy 집계 확인 →
   판독 REPLACE 면 새 마감 결정 (D-2026-10-05-wad-agc-graphite-closed 를 supersede · 같은 slot) / KEEP_A_PRIME 이면 (a′) 그대로 →
   DEM 회신 (회신 9 초안에 붙일지 따로 낼지 사용자에게 묻는다 · 라벨 동반)
3) li2s 대조 계 (외부 1저자) — 시드 진행·회수 → 시드 게이트 · 밀도 · T₅₀ · 장부 (kgy 등분 · gabia pmon · 벽시계 병기) → 600 K MD 러너 (B) ·
   판독 대조 모드 (600 K 결과 전에) · 다음 편지 (기계 배정 변경 · gabia 점유 표본 정의)
4) cascade v7 탐침 감시 → T* 또는 사다리 소진이면 카드대로
5) 탄성 modelc_2x 남은 strain → fit
6) V5 VASP 최종 반송 → --collect (PP 등록부 + UMA) → G5
7) webapp 반영 (사용자 '나중에') — 대피 세션 일을 화면에 · /governance 에 점착 W 값이 결정 문장으로 뜨는 것을 가릴지 사용자에게 묻는다
   (대피 전부터 있던 결정 문장 + 대피 세션이 쓴 P1b 마감 결정 제목 · 비준 본문은 못 고친다 · merge_request §6)
8) 그 밖은 kb/open_items.md ⏭ 절
세션을 닫기 전에 kb/open_items.md ⏭ 절을 갱신한다 (⏭-NOW-z7 위에 새 블록).

■ 8. 사용자 운영 규칙 (그대로)
- 원격 작업은 "붙여넣기 블록 → 사용자가 실행 → 출력 회수". ssh 로 명령을 주지 않는다. 붙여 준 출력은 하나씩 보고 해석한다 — 앞서가지 않는다.
- 원격 명령 블록은 사용자가 요청할 때나 붙여 준 출력의 다음 한 수로만 준다.
- 블록은 기계 가드로 시작하고, 가드 뒤 명령은 전부 { …; } 로 감싼다:
    kgy   [ "$(whoami)" = kgy ] || { echo "⛔ 여기는 kgy 가 아니다 — $(whoami)@$(hostname)"; false; } && { …; }
    gabia [ -x /data/apps/miniforge3/envs/uma/bin/python ] || { echo "⛔ 여기는 gabia 가 아니다"; false; } && { …; }
- ⛔ 인증을 묻는 명령(git push) 뒤에는 다른 줄을 두지 않는다 — 뒤에 할 일은 같은 줄에 && 로.
- 큰 계산은 GPU 로만. gabia 에서 GPU pw.x 와 UMA 를 겹치지 않는다 (예외는 원장 active 결정만 — 지금 예외 (5)). kgy 는 프로세스 정보가 막혀 있다.
- 프로세스는 PID 나 잡 고유 인자로만 죽인다 (pkill -f pw.x · python · 스크립트 이름 금지).
- 돌고 있는 러너의 worktree 를 다른 커밋으로 옮기거나 지우지 않는다.
- 봉인 카드 · 리뷰 회신 원문 · 비준된 결정은 고치지 않는다 (정정은 새 파일 · supersede 재봉인으로).
- 점착 W 값은 webapp 화면 · 원장 로그 · open_items 에 싣지 않는다 (결과 기록 · 마감 카드에만). 결정 제목·문장과 kb 카드에도 쓰지 않는다
  (/governance 와 /kb?path= 가 그대로 렌더한다).
- 1저자는 트랙마다 다르다 — 결정을 쓸 때 트랙을 먼저 쓴다 (점착 · cascade · ESW · 탄성 = 사용자 · li2s = 외부 1저자 · CEI = 실험 쪽 다른 사람).
- 커밋은 validate_canonical.py 통과 뒤에만 (대피 중 7a475e4d 가 검증 실패 상태로 올라갔다).
- MP_API_KEY 는 gabia 환경변수에만 둔다 — 출력·에코하지 않는다.
- 한국어 대화체로 짧게 · 그림 라벨은 영어 · 새 개념은 한 단계씩.

첫 답은: ■0 결과 한 줄씩 → 경우 판정 → (경우 C 면) 병합 · ■2 점검 · push 결과 → ■4 안내.
```

## 1. 왜 이렇게 했나

- **no-ff 인 이유**: 대피 카드 ■1 은 '대피 중 friendly 에 아무도 쓰지 않으면 fast-forward' 였다. 그런데 DEM 쪽 litdb 세션
  (`session_01H191Ni4xzj9H5ftstAm7Ft`) 이 friendly 에 직접 쓰는 세션이라 10-03 에 2 커밋이 들어갔다. 그 세션이 고친 것은 `litdb/` 뿐이고
  대피 세션은 그쪽 파일을 안 건드렸다 (대피 카드 ■5). 그래서 텍스트 충돌은 `_sources.json` 한 곳의 자동 병합뿐이다.
- **가상 병합을 먼저 돌린 이유**: 텍스트 충돌이 0 이어도 생성물이 낡거나 JSON 이 깨질 수 있다. 그래서 병합 트리를 그대로 커밋으로 만들어
  임시 worktree 에서 원장 검증 · kb lint · litdb 인덱스 점검 · 웹앱 전체 시험 · 다섯 화면 · 도구 selftest 를 다 돌렸다.
  결과는 merge_request §3 에 있다. 이 카드의 기대값은 그 실측이다.
- **rebase 금지**: evac 커밋 13 개에 결정 비준이 결속돼 있다 (`ratification.commit`). 원격 러너 worktree 4 곳도 evac 커밋에 있다.
  해시가 바뀌면 비준이 '없는 커밋에 결속' 으로 보이고, 원격 worktree 의 기록과 레포가 끊긴다.

## 2. 이 카드가 못 하는 것

- 기대값은 10-05 밤 실측이다. origin 세션이 들일 때 DEM 세션이 friendly 에 더 썼으면 수가 달라진다 — 그래서 ■0 이 먼저 센다.
- 원격 상태는 사용자가 붙여 준 마지막 watch (kgy 22:49 · gabia 20:50) 다.
- 병합은 이 세션이 하지 않는다 (대피 규칙: friendly 에 쓰지 않는다). origin 세션이 한다.
