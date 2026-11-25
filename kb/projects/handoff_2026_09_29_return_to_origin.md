---
title: "origin 복귀·통합 카드 — claude/evac-2026-09-28 → claude/friendly-meitner-lldvar (2026-09-29)"
date: 2026-09-29
updated: 2026-09-29
tags: [merge, handoff, evacuation, return, gabia, li2s, cei, wad, elastic]
status: 발송 대기 — 사용자가 §0 프롬프트를 origin 세션에 붙여 넣는다
confidence: medium
verificationStatus: verified
verifiedAt: 2026-09-29
verifiedBy: self
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: single-source
---


# origin 복귀·통합 카드 — `claude/evac-2026-09-28` → `claude/friendly-meitner-lldvar`

> 짝: 대피할 때의 카드 `kb/projects/handoff_2026_09_28_evacuation.md` (origin → evac). 이 카드는 그 반대 방향이다.
> 머지 판단의 정본은 `kb/projects/merge_request_2026_09_28.md` (커밋 표 · 시험 · 원격 · 원장 변화 · 빨간불 · 다음 일).
> 실측 (09-29 01:4x KST): friendly 끝 `2be9af3a` = merge-base · friendly 에만 있는 커밋 **0** · evac 에만 **48** (+ 이 카드 커밋)
> ⇒ **fast-forward 로 충돌 0**. 충돌은 origin 세션이 머지 **전에** 뭔가를 쓰거나, 안 올린 로컬 커밋·변경이 있을 때만 생긴다.

## 0. origin 세션에 붙여 넣을 프롬프트

```text
[origin 복귀 — 2026-09-29 · 대피 브랜치 통합]

너는 Yonghoon-DEM-DFT 캠페인의 본 세션(브랜치 claude/friendly-meitner-lldvar)이다. 09-28 새벽(KST)에 컨텍스트가 다 차서
대피 세션(브랜치 claude/evac-2026-09-28)으로 일을 넘겼고, 그 세션이 48 커밋을 쌓았다. 사용자가 통합을 요청했다
("origin쪽에 통합 … 충돌 안 일어나게 조심해서 머지되게"). 할 일은 그 커밋들을 **충돌 없이** friendly 로 들이고 이어서 일하는 것이다.

■ 0. 아무것도 쓰기 전에 — 이 순서를 어기면 충돌을 스스로 만든다
- 파일을 고치거나 커밋하지 않는다. friendly 에 커밋이 하나라도 생기면 fast-forward 가 깨진다
  (open_items ⏭ 갱신·CLAUDE.md 재독 메모 같은 것도 머지 **뒤에** 한다).
- 아래를 돌리고 결과를 한 줄씩 기록한다:
    set -o pipefail
    git status --short                                   # 비어 있어야 한다
    git stash list | head -3
    git fetch origin claude/friendly-meitner-lldvar claude/evac-2026-09-28
    git log --oneline origin/claude/friendly-meitner-lldvar..HEAD      # 내 로컬에만 있는 커밋 (안 올린 것)
    git merge-base --is-ancestor origin/claude/friendly-meitner-lldvar origin/claude/evac-2026-09-28 && echo FF가능
    git rev-list --count origin/claude/friendly-meitner-lldvar..origin/claude/evac-2026-09-28     # 49 안팎
  (대피 세션 실측 09-29 01:4x KST: friendly 2be9af3a = merge-base · friendly 에만 있는 커밋 0 → FF가능)

■ 1. 들이기 — 경우를 먼저 가른다
- 경우 A (기대하는 경우) — git status 비었음 · 로컬 전용 커밋 0 · FF가능:
    git switch claude/friendly-meitner-lldvar
    git merge --ff-only origin/claude/evac-2026-09-28
    git push origin claude/friendly-meitner-lldvar            # 강제 없이. 거절되면 멈추고 사용자에게 말한다
- 경우 B — 커밋 안 한 변경이 있다:
    git stash push -u -m "pre-evac-merge-2026-09-29"  →  경우 A  →  git stash pop
    pop 에서 충돌이 나면 ■3 규칙으로 풀되, stash 내용은 09-28 새벽 이전 기준이라 evac 이 같은 곳을 이미 고쳤을 수 있다 —
    푼 diff 를 사용자에게 보이고 허락 뒤 커밋한다.
- 경우 C — 안 올린 로컬 커밋이 있거나 friendly 가 origin 에서 움직였다 (FF 불가):
    멈추고 사용자에게 말한다. 허락을 받으면
      git switch claude/friendly-meitner-lldvar
      git merge --no-ff origin/claude/evac-2026-09-28 -m "merge claude/evac-2026-09-28 (대피 세션 48 커밋)"
    ⛔ rebase 하지 않는다 — evac 커밋 해시가 결정 원장의 비준(ratification.commit) · 기록 · gabia worktree 에 박혀 있다.
    충돌은 ■3 규칙으로 → ■2 점검 → push (강제 없이).
- 어느 경우든 evac 브랜치는 지우지 않는다 (기록이다).

■ 2. 점검 — 머지 뒤, 종료코드로 (대피 세션 기대값을 옆에 적었다)
    python3 tools/kb_wiki.py lint | tail -1                        # 0 errors
    python3 tools/db/validate_canonical.py | tail -2               # 결정 92 · 그래프 무결성 ✅ · 배선 전부 일치
    python3 tools/convention_check.py | tail -1                    # 0 위반
    python3 -m pytest webapp/tests -q -p no:cacheprovider | tail -3
        # 기대 603 passed · 3 failed · 2 skipped. 3 failed = cascade 매니페스트 셋 (09-22 부터 · 정상 경보):
        #   test_cascade_headline_comes_from_the_manifest · test_manifest_tamper_fails_closed · test_audit_figures_are_the_only_default_figures
        # 이 셋 말고 빨가면 머지로 생긴 새 문제다 — 고치기 전에 원인부터.
        # ⛔ 매니페스트 해시만 다시 박아 초록으로 만들지 않는다 (1저자: cascade v6 끝난 뒤 풀 입력 → 퍼널 → 감사 그림 → 매니페스트 순서로 한 번에).
    python3 -m pytest webapp/tests/test_interpretation_cards.py -q | tail -1     # 79 passed
    SELFTEST_PY=<numpy·ase 있는 python> bash tools/ionic/glass_main_queue_gabia.sh --selftest | tail -1   # selftest ✅ (음성 17 포함)
    <numpy·ase·dftd3 있는 python> tools/wad/cc_graphite.py --selftest | tail -1                            # 53/53

■ 3. 충돌이 나면 (경우 B·C) — 파일별 규칙
- db/governance/decisions.json — 양쪽 결정을 **전부** 남긴다 (id 합집합). 비준된 결정의 본문은 한 글자도 고치지 않는다
  (decision_digest = ratification 을 뺀 본문의 sha256 · 고치면 '승인 이후에 내용이 바뀌었다' 로 깨진다).
  evac 은 D-2026-09-28-gabia-uma-coexist-v4-li2s465 를 superseded 로 재봉인했다 (_원본_비준 보존 · superseded_by 예외 (3)) — evac 판을 쓴다.
  같은 slot 에 active 가 둘이면 검증기가 막는다 (해소는 명시적 supersedes 로만). 푼 뒤 반드시 validate_canonical.py.
- kb/open_items.md — 합집합. evac 의 ⏭-NOW-z 블록을 통째로 남기고 네 새 블록은 그 위에 얹는다. 머리 줄(최종 갱신)은 늦은 쪽.
  '시험 `test_interpretation_cards.py` **62 → N**' 의 N 은 실제 시험 수와 같아야 한다 (evac 판 79 · test_resume_block_… 이 잡는다).
  머리 줄에 굵게를 겹쳐 쓰지 않는다 (대시보드 시험이 깨진다).
- CLAUDE.md — gabia 절의 예외 줄은 evac 판이 원장과 맞다 (예외 (3) active · 09-28 예외 소멸 · 교훈 'amendment 까지 본다' · VRAM 30.6 → 40.0 GB).
  다른 절의 네 변경은 살린다.
- kb/index.md — 손으로 풀지 않는다. 아무 쪽이나 고르고 python3 tools/kb_wiki.py index 로 다시 만든 뒤 lint.
- litdb/INDEX.md · litdb/comparison_vs_ours.md — 합집합 (evac: wang2015 digest · §J-50 · maurer2015 §J-43 보류).
- webapp/tests/*.py — 양쪽 시험을 다 남긴다. 수가 바뀌면 open_items 의 62 → N 도 맞춘다.
- db/properties/cei_figs/index.html — evac 판이 최신 (§0 정정 · x = 0.02 전면 · x = 0.10 문장·행). 네 쪽 변경이 있으면 손으로 합치고 test_interpretation_cards 로 확인.
- 비준된 카드 · 리뷰 회신 원문 · 원자료(db/raw) — 어느 쪽도 내용을 고치지 않는다. 충돌이면 나중 판(evac)을 쓰고 이유를 커밋 메시지에 적는다.

■ 4. 머지 직후 사용자에게 꼭 말한다 (1저자 요청 09-28 · "이거 나중에 꼭 얘기해줘야돼")
  사용자 로컬 체크아웃이 claude/evac-2026-09-28 에 있다 (로컬 웹앱 127.0.0.1:5001 이 로컬 체크아웃을 읽는다). 되돌리게 한다:
      git switch claude/friendly-meitner-lldvar && git pull --ff-only
  (09-29 새벽 사용자가 본 CEI 화면이 09-28 오후 이전 판이었다 — 로컬이 pull 안 된 상태였다. 새 판은 머리 표가 0.02 · 0.10 · 0.20 세 행이다.)

■ 5. 원격에서 지금 도는 것 (09-29 01:26 KST 실측이 마지막) — 머지와 무관하게 계속 돈다. 건드리지 않는다.
- gabia · 탄성 modelc_2x (트랙 = 우리 DFT · 1저자 = 사용자): tmux el_mc2x_0928 · 23_p 를 BFGS 67 이력부터 재개 (09-29 00:03:30 ·
  새 out 에 'initial density is read from file' · 'Starting wfcs from file' · 첫 accuracy 3.72e-5 Ry) · pw.x 2001378 ·
  VRAM 30.6 GB(첫 SCF) → 40.0 GB(01:26) — 단계마다 다르다. 남은 순서 23_p → 23_m → 13_p/m → 12_p/m → 12/12 면 fit.
  러너 로그 /root/logs/el_modelc2x_0928.log · watch /root/logs/w_el_0928.sh ('23_p 누적 BFGS' 가 68 근처인지 · 1 이면 처음부터 — 바로 본다).
  ⛔ 러너는 worktree /data/work/wt_elastic_0928 (@7cf909446) 의 스크립트를 **읽는 중**이다 — 지우거나 다른 커밋으로 옮기지 않는다.
- gabia · li2s 본 런 나머지 (⛔ 외부 1저자 트랙 — 사용자는 기계 배정만): tmux glassq · 러너 tools/ionic/glass_main_queue_gabia.sh
  (worktree /data/work/wt_li2s_0929 · 같은 이유로 건드리지 않는다) · 큐 465:5 → 550:3 → 550:4 → 550:5 (4 런 · 런당 3.5–4.5 h) ·
  첫 런 T465 seed5 PID 2023556 (01:25:36) · 구조 판별 4/4 · run_meta = seed3 T465 판. 근거 결정 D-2026-09-29-gabia-uma-coexist-elastic-li2s-main.
  가드 (GPU 합계 > 46,000 · 우리 MD > 3,500 MiB · host < 8,192 · 탄성 새 OOM) 가 뜨면 우리 MD 만 죽고 큐가 멈춘다 —
  종료 코드 2·3·5 는 예외 닫힘 (자동 재시작 없음 · 원 규칙으로). 로그 …/lpscl_glass_md_main_2026_09_28/queue_coexist.log · TSV queue_coexist.tsv ·
  watch /root/logs/w_glassq.sh. seed1·2 네 런은 1저자 '나중에' (kgy 꺼짐).
- V100 · WAD-CC 흑연 C|C (트랙 = 점착 · 1저자 = 사용자): tmux wadcc · ~/runs/wad_cc_graphite_2026_09_28 · 1단계 CC_S33_AB_relax 09-28 22:42:45 시작 (164 k 점).
  끝나면 ~/wad_cc_graphite_2026_09_28_return.tgz → (kgy 막혀 gabia 경유) → repo db/raw/wad_cc_graphite_2026_09_28/ →
  cc_graphite.py --verify_stage2 → --collect --atm (짝 규칙 ② pairing_column) → 결과 기록 → DEM 회신 8 → 점착 DFT 마감 기록.
- kgy: 꺼짐 (사용자 09-29 01시). 켜지면 먼저 ① li2s 600 K 파일럿 (tmux gp600) 이 꺼질 때 돌고 있었는지 (끊겼으면 흔적 보존 → 재실행)
  ② cascade v6 E′ 마스터 (PID 372656 · 09-28 기준 28/40).

■ 6. 대피 세션이 한 일 — 트랙을 먼저 쓴다 (자세한 것: kb/projects/handoff_2026_09_29_return_to_origin.md §1 · merge_request §2·§5 · open_items ⏭-NOW-z)
- 점착 W_ad (1저자 = 사용자): V4 끝 → 결과 기록 (벤젠|LPSCl 0.1915 eV/조각 · G3 FAIL · ecut 미검증 · eV/조각만) · DEM 회신 7 발송 →
  DEM 7차 회신 비준 ("ㄱㄱ" · 짝 규칙 ①–④) · 우리 문구 정정 둘 · WAD-CC 흑연 C|C 사전등록·입력·V100 발사 · litdb Wang 2015 · 짝 규칙 ② 코드 결속.
- li2s (⛔ 외부 1저자): 회신 CH·CL(부분) 반영 · 600 K 편입 규칙 사전등록 · S54 내력 · 다섯 시드 전수 · 600 K 파일럿 (kgy) ·
  465 K seed3·4 → 조기확인 ✅ (D(2–50) 비 STO 1.38 · MTO 1.33 ≤ 2 배) · 본 런 나머지 gabia 공존 큐 발사 (4 런) · 발표 덱 그림 · /li2s 요약 절.
- CEI Nd (1저자 = 사용자): §0 정정 · 화면 전면 x = 0.02 전환 (G4 닫음) · Li 장부 = 항등식 (결정 proposed) · x = 0.10 곡률 (GC 통과 · 결과 ratified 09-29) ·
  머리 2×2 에 x = 0.10 행 (공통 20 칸 · Li +0.0183 · P −0.0344).
- 탄성 modelc_2x (1저자 = 사용자): 옛 러너 kill (CONT 안 함) → 새 러너로 23_p 재개 (465 K 끝난 뒤 자동) · 09-11 2차 개정(공존 조건부 허용)을 늦게 찾아 정정.
- gabia 운용 (1저자 = 사용자): 예외 (2) 소멸·재봉인 · 예외 (3) active · VRAM 교훈.

■ 7. 이어서 할 것 (순서) — merge_request §7 과 같다
1) 사용자 로컬 되돌리기 안내 2) 탄성 BFGS 68 확인 3) li2s 큐 4 런 → 끝나면 C1·C2·감김 판독 4) WAD-CC 회수·집계·결과 기록 → DEM 회신 8 → 점착 마감
5) kgy 켜지면 600 K·cascade 상태 · seed1·2 옮겨 큐 2차 6) li2s 편지 CM (외부 1저자) 7) CEI 항등식 비준 → 화면 교체 4 곳
8) cascade v6 끝 → 매니페스트 재생성 (1저자) 9) V5 VASP 외주는 1저자가 알려 줄 때만.
세션을 닫기 전에 kb/open_items.md ⏭ 절을 갱신한다 (⏭-NOW-z 위에 새 블록).

■ 8. 사용자 운영 규칙 (그대로)
- 원격 작업은 "붙여넣기 블록 → 사용자가 실행 → 출력 회수". ssh 한 줄 명령으로 주지 않는다. 블록은 bash <<'BLK' … BLK 로 감싸 exit 가 사용자 셸을 닫지 않게.
- 붙여 준 출력은 하나씩 보고 해석한다 — 앞서가지 않는다. 확실하지 않으면 원장·기록부터 본다 (사전등록은 amendment 까지).
- 큰 계산은 GPU 로만. gabia 에서 GPU pw.x 와 UMA 를 겹치지 않는다 — 살아 있는 예외 (3) 범위 안에서만.
- 프로세스는 PID 나 잡 고유 인자로만 죽인다 (pkill -f pw.x · python · 스크립트 이름 금지). watch·명령줄에 러너 이름을 넣지 않는다 (pgrep 가드가 센다).
- 봉인 카드 · 리뷰 회신 원문 · 비준된 결정은 고치지 않는다 (정정은 새 파일 · 정오 기록 · supersede 재봉인으로).
- 점착 W 값은 webapp 화면에 싣지 않는다. D·σ·Ea 는 절대값 인용 금지 (상대차만).
- 한국어 대화체로 짧게 · 그림 라벨은 영어 · 새 개념은 한 단계씩. 1저자는 트랙마다 다르다 — 결정을 쓸 때 트랙을 먼저 쓴다.

첫 답은: ■0 점검 결과 한 줄 · 경우 A/B/C 중 무엇인지 · (A 면) 머지·푸시 결과 · ■2 점검 요약 · 사용자에게 로컬 되돌리기 안내.
원격 명령 블록은 사용자가 요청할 때만 준다.
```

## 1. 대피 세션이 한 일 — 트랙별 (자세히)

### 1-1. 점착 W_ad (트랙 = 점착 · 1저자 = 사용자)

- **A′ V4 (벤젠|LPSCl S-바깥 4층 조각 모델)** — gabia 9 잡 끝 (09-28 20:36:09 · rc 0 · 피크 41,520 MiB) → 원자료 `db/raw/wad_aprime_s4_v4_2026_09_27/` ·
  결과 기록 `wad_aprime_pilot_result_v4_2026_09_28.json` (proposed): ΔE_frag **0.1915 eV/조각** (PBE 단독 −0.0618 · ΔD3 +0.2533 · s-dftd3 2체 교차 0.007 meV) ·
  ATM −18.2 meV → 0.1733 · **G3 FAIL** (직접 8→10 Å +6.73 meV > 5) · G4 k1·s05 진짜 0 (절연체 · 큰 셀) · e70 = ecut 미검증 (RESOURCE_BLOCKED) · 측방 영상 5.07 Å.
  이름: *UMA+D3 기하에서 평가한 PBE+D3(BJ) 고정기하 분리에너지* · **eV/조각만 (J/m² 환산 금지)**.
- **DEM 교환**: 회신 7 발송 → DEM 7차 초안 수령 → 우리 과장 둘 정정 (결정성·모서리·작용기는 **W 자체**를 바꾸고 곡률(R\*)·거칠기(실접촉)만 DEM 기하 ·
  덴카블랙 = 카본블랙 → *'이상 기저면 조건부'* · VGCF 바깥벽은 흑연 대리 유지) → **DEM 7차 비준** (1저자 "ㄱㄱ" · §3 짝 규칙 ①–④) ·
  원문 `kb/projects/wad_dem_reply_draft_2026_09_23.md` §DEM 7차 회신 원문 · DEM 쪽 문서 기록은 DEM 세션 몫 (최종본은 사용자에게 전달).
- **WAD-CC 흑연 C|C** (덴카–덴카 · 덴카–VGCF · VGCF–VGCF → DFT 에서는 셋 다 흑연 기저면|기저면): 사전등록 `wad_cc_graphite_prereg_2026_09_28.json` (ratified) ·
  결정 `D-2026-09-28-wad-cc-graphite` (active) · 도구 `tools/wad/cc_graphite.py` (stage1 → stage2 → verify_stage2 → collect · selftest 53 · 깨기 22/22) ·
  입력 `db/inputs/wad_cc_graphite_2026_09_28/` (1단계 9 relax · `run_v100.sh`) · 모델 S33_{AB,SP,AA} · M41_{AB,SP,AA} · S44_AB · M61_AB · M41_AB_V2a ·
  판정 GC S33_AB ∈ 0.31–0.47 · G3/G4 |ΔW| ≤ 0.01 · 두께 ≤ 0.02 · 이완 유효성 · 비정합 추정 W_inc 2성 (W_AA+3W_SP)/4.
  litdb `wang2015_graphite_cleavage_energy` — **0.37 ± 0.01 J/m² = 비정합 CE (직접 측정)** · 0.39 ± 0.02 = 이상 AB (= 0.37 + σ₀).
  **짝 규칙 ② (결과 전 코드 결속)**: 2체 vs 2체+ATM 중 |W_inc(S33) − 0.37| 가 `PAIR_TIE` 0.01 넘게 작은 열 · 아니면 *'구분 안 됨 → 2체'*.
  V100 발사 (09-28 22:3x · 사용자 MPM 옆 공존 · START_MAX_MIB 24000 · 1저자 '걍 돌려도돼' · 코드 전송은 gabia 경유 `git archive`).

### 1-2. li2s 소셀 유리 (⛔ 트랙 = 외부 1저자 — 사용자는 실행·기계 배정)

- 회신 CH 원문 보존·반영 (600 K 편입 규칙 **사전등록** · 2σ 경계 · digest 오기) · 회신 CL (부분) — 465 K '2 배' 문턱 확정 (착수 전 커밋).
- S54 내력 (`quench_ss_event.py --trace_S` · P50 에서 109 ps 이탈 · 짝 S59) · 48 S 전수 소속-이동 (`--s_census`) · 다섯 시드 정체 온전 P **12·12·9·5·5** · PS₄ 보존율 ≠ 정체 지표.
- 600 K 파일럿 (kgy · 원시 초기구조로 던졌다가 relax 로 재발사 · 원시 산출 `…/pilot600/T600_raw_aborted_20260928` 보존) — 상태 미확인 (kgy 꺼짐).
- 465 K seed3·seed4 (gabia · V4 뒤 단독 · 20:36:15) → **조기확인 ✅** (09-29 00:02 끝): D(2–50) 비 **STO 1.38 · MTO 1.33 ≤ 2 배** · 생산 평균 T 464.4 · 467.0 K ·
  MSD@50 9.4 · 10.2 Å² — 읽기 단서 넷 (비 하나 · 눈금과 다른 양 · C1·C2·감김 판독 전 · 절대값 금지) · 기록 CH 개정 파일 `✅_본런_465K_조기확인_결과_2026_09_29`.
- 본 런 나머지 8 런 → gabia 탄성 옆 한 번에 하나씩 (예외 (3)) · **첫 4 런 발사 09-29 01:25:36** · seed1·2 는 1저자 '나중에'.
- 발표 덱 그림 8 장 + 생성기 + CSV · 웹앱 `/li2s` 「처음 보는 분께」 절.
- 다음 편지 CM (미발송): 600 K · 465 K 조기확인 · 다섯 시드 · 두 400 K 런의 난수가 같았다(401) · 기계 배정 사실 · Q-CL-3·4.

### 1-3. CEI Nd (트랙 = 우리 CEI · 1저자 = 사용자)

- §0 정정 — 환원 쪽은 안 움직인다 (네 조성 모두 1.717 V) · 결론 단락 셋.
- **화면 전면 x = 0.02 전환** — 사전등록 3차 개정 · 결정 `D-2026-09-28-cei-page-x002` · gabia 16 조성 재계산 · G0–G5 · G4 는 *'위반 9 · 원인 규명(반응식 계수 반올림)'* 으로 닫음
  (결정 `D-2026-09-28-cei-x002-result` · 1저자 "ㅇㅇ 그렇게 해줘") · 그림 `_x002` (옛 파일 안 덮음).
- **Li 장부 기울기 = 항등식** (계수 1) — 결정 `D-2026-09-28-cei-li-ledger-identity` **proposed** (1저자 비준 → 화면 교체 4 곳).
- **x = 0.10 곡률** — 사전등록 · gabia · GC 두 자리 통과 (자리별 유효칸 Li +0.0004 · P +0.0008 ≤ 0.005) · 결과 기록 **ratified 09-29** ·
  머리 2×2 에 **x = 0.10 행** (여섯 조성 공통 20 칸 = 09-19 의 같은 20 칸 · Li +0.0183 (20/20) · P −0.0344 (16/20) · 09-19 네 값 재현 차 5e-6) · Nd 카드 §8 · 결속 시험.

### 1-4. 탄성 modelc_2x (트랙 = 우리 DFT · 1저자 = 사용자)

- 1저자 *'이거 다시 진행하자 가드 풀고'* (09-28 23시) → 옛 러너 248598 `kill -9` (**CONT 안 함** — 옛 코드는 23_p 를 unconverged 로 읽고 23_m 으로 넘어가며 UMA 옆에 바로 pw.x 를 띄웠을 것) ·
  새 worktree `/data/work/wt_elastic_0928` (@7cf909446 · 재개 고침 c181c2f3 포함) · DRY_RUN 물리 설정 11 줄 = 09-26 판 · 대기 러너가 465 K 끝 + GPU 빔 2 회 연속을 보고 exec (00:03:29).
- 23_p 이력 승계 확인 (density·wfc from file · 첫 accuracy 3.72e-5 Ry) · BFGS 68 확인은 남음.
- ⚠ 정정: 09-28 밤 *'공존하면 탄성 사전등록상 무효'* 라고 말했다 — 09-11 2차 개정 (`D-2026-09-11-elastic-conv-threshold`) 으로 이미 **조건부 허용**이었다
  (대신 탄성 잡이 하나라도 OOM·비정상 종료면 modelc_2x 처음부터). 23_p EXIT 통제 정지는 그 '중단' 이 아니다 (1저자 09-29).

### 1-5. gabia 운용 (트랙 = 우리 · 1저자 = 사용자)

- 예외 (2) `D-2026-09-28-gabia-uma-coexist-v4-li2s465` — 쓰이지 않고 소멸 → superseded 재봉인.
- 예외 (3) `D-2026-09-29-gabia-uma-coexist-elastic-li2s-main` (active) — 러너 `tools/ionic/glass_main_queue_gabia.sh`:
  구조 값 판별 (120 원자 · 단일 프레임 · 최단 P–S ±0.003 · PS₄ · ρ ±0.001) · 설정 대조 (seed3 T465 run_meta · dt) · 가드 ①–④ · flock · 중단 흔적 `_aborted_` 보존 · 종료 코드 0/2–10.
- VRAM 교훈: 탄성 pw.x 30.6 GB (첫 SCF) → 40.0 GB (01:26) — 한 시점 값으로 '보통' 을 말하지 않는다.

## 2. 왜 충돌이 안 나나 · 언제 나나

- 대피 뒤 friendly 에는 아무도 커밋하지 않았다 (merge-base = friendly 끝 `2be9af3a`) → evac 이 friendly 의 **순수한 뒤쪽 연장**이다 → `--ff-only` 로 파일 단위 병합 자체가 일어나지 않는다.
- 충돌이 나는 경우는 셋뿐이다: ① origin 세션이 머지 전에 friendly 에 커밋 ② origin 세션의 커밋 안 한 변경 (stash pop 때) ③ 안 올린 로컬 커밋.
  셋 다 §0 ■0 점검이 먼저 드러낸다. 가장 부딪히기 쉬운 파일은 `kb/open_items.md` · `db/governance/decisions.json` · `CLAUDE.md` · `kb/index.md` 다 (§0 ■3 규칙).

## 3. 이 카드가 못 하는 것

- 09-29 01:4x KST 이후 friendly · evac · 원격의 변화를 모른다 — origin 세션이 §0 ■0 으로 다시 본다.
- origin 세션 로컬에 무엇이 남아 있는지 모른다 (커밋 안 한 변경 · 안 올린 커밋) — 그래서 경우 B·C 절차를 적었다.
- kgy 가 꺼질 때 돌던 잡(600 K 파일럿 · cascade v6)의 상태를 모른다.
