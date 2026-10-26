---
title: "본 세션 복귀 카드 — 대피 브랜치 claude/evac-2026-10-22 (82 커밋) 를 friendly 로 · fast-forward (2026-10-26)"
date: 2026-10-26
updated: 2026-10-26
tags: [merge, handoff, return, evacuation, gabia, kgy, wad, cei, nd, li2s, li3nd, elastic]
status: 발송 대기 — 사용자가 §0 프롬프트를 본 세션 (friendly) 에 붙여 넣는다
confidence: medium
verificationStatus: verified
verifiedAt: 2026-10-26
verifiedBy: self
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: single-source
---


# 본 세션 복귀 카드 — `claude/evac-2026-10-22` → `claude/friendly-meitner-lldvar`

> 선례: `kb/projects/handoff_2026_10_05_return_to_origin.md` (대피 브랜치 → friendly · 그때는 friendly 가 움직여서 no-ff) ·
> `kb/projects/handoff_2026_10_20_return_to_origin.md` (같은 브랜치 따라잡기 · fast-forward). 머지 판단 자료는 `kb/projects/merge_request_2026_10_26.md`.
> 실측 (2026-10-26 · 대피 세션 `session_01Er41drwDRfvL6hhZbVtBiw`):
> · friendly 끝 = **`aaa275e20`** (10-22 대피 인계 카드) = merge-base · friendly 에만 **0** 커밋.
> · evac 에만 **81** 커밋 + 이 카드 커밋 = **82** (그중 9 은 사용자가 kgy · gabia 회수 블록으로 올린 커밋).
> · 대피 카드 ■5 의 조건 (대피 중 friendly 에 아무도 쓰지 않는다) 이 지켜졌다 ⇒ **fast-forward 라 충돌 0**.
> · `origin/main` 은 2026-03-25 빈 초기 커밋 (공통 조상 없음) — 이 캠페인과 무관하다. **main 으로 머지하지 않는다.**

## 0. 본 세션에 붙여 넣을 프롬프트

```text
[본 세션 복귀 — 2026-10-26 · 대피 브랜치 claude/evac-2026-10-22 (82 커밋) 들이기]

너는 Yonghoon-DEM-DFT 캠페인의 본 세션이다 (브랜치 claude/friendly-meitner-lldvar). 10-22 에 토큰이 떨어져서 사용자가 대피 세션
(브랜치 claude/evac-2026-10-22 · session_01Er41drwDRfvL6hhZbVtBiw) 으로 옮겼다. 네가 마지막으로 올린 커밋은 대피 인계 카드 aaa275e20 (10-22 00:55 UTC) 다.
대피 세션은 friendly 에 한 줄도 쓰지 않았다 (원격 회수 커밋도 evac 로 보냈다). 그래서 들이기는 fast-forward 다.
할 일: evac 커밋을 **충돌 없이** 들이고, 네 기억 (10-22 에 멈춤) 대신 원장 · 기록으로 상태를 다시 맞춘 뒤 이어서 일한다.
⛔ origin/main 은 3 월 빈 초기 커밋이다 — main 으로 머지하거나 main 에 push 하지 않는다. 사용자가 말하는 '메인 브랜치' 는 friendly 다.

■ 0. 아무것도 쓰기 전에 — 이 순서를 어기면 충돌을 스스로 만든다
- 파일을 고치거나 커밋하지 않는다 (open_items ⏭ 갱신 · 메모 · 시험 손질 모두 들인 **뒤**).
- 돌리고 결과를 한 줄씩 적는다:
    set -o pipefail
    git rev-parse --abbrev-ref HEAD                                       # claude/friendly-meitner-lldvar
    git status --short                                                    # 비어 있어야 한다
    git stash list | head -3
    git fetch origin claude/friendly-meitner-lldvar claude/evac-2026-10-22
    git log --oneline origin/claude/friendly-meitner-lldvar..HEAD         # 안 올린 로컬 커밋 — 0 이어야 한다
    git log --oneline -1 origin/claude/friendly-meitner-lldvar            # aaa275e20 (Evacuation handoff card 2026-10-22) 여야 한다
    git log --oneline -1 origin/claude/evac-2026-10-22                    # 'Evacuation return card 2026-10-26' 커밋이어야 한다
    git merge-base --is-ancestor origin/claude/friendly-meitner-lldvar origin/claude/evac-2026-10-22 && echo FF가능
    git rev-list --count origin/claude/friendly-meitner-lldvar..origin/claude/evac-2026-10-22   # 82
  ⚠ 82 보다 많으면 복귀 카드 뒤에 누가 evac 로 올린 것이다 (원격 회수 커밋일 수 있다) — 목록을 사용자에게 보이고 그대로 들여도 되는지 묻는다.
  ⚠ friendly 끝이 aaa275e20 이 아니면 (다른 세션이 friendly 에 올렸다) ■1 경우 C.
  ⚠ 컨테이너가 새로 떠서 저장소를 새로 받았으면 HEAD 가 이미 friendly 원격 끝일 수 있다 — 그래도 ■1 경우 A 로 evac 를 들인다.

■ 1. 들이기 — 경우를 먼저 가른다
- 경우 A (기대) — status 비었음 · 로컬 전용 커밋 0 · friendly 끝 aaa275e20 · FF가능:
    git merge --ff-only origin/claude/friendly-meitner-lldvar      # 로컬 friendly 를 원격 끝으로 (이미 같으면 그대로)
    git merge --ff-only origin/claude/evac-2026-10-22
  → ■2 점검 → git push origin claude/friendly-meitner-lldvar      (강제 없이 · 거절되면 fetch 해서 ■0 부터 다시)
- 경우 B — 커밋 안 한 변경이 있다:
    git stash push -u -m "pre-return-2026-10-26"  →  경우 A  →  git stash pop
    pop 충돌은 ■3 규칙으로. stash 는 10-22 이전 기준이라 대피 세션이 같은 곳을 이미 고쳤을 수 있다 —
    푼 diff 를 사용자에게 보이고 허락 뒤 커밋한다.
- 경우 C — 안 올린 로컬 커밋이 있거나 friendly 가 움직였다 (FF 불가):
    멈추고 사용자에게 말한다 (커밋 목록 · 바뀐 파일). 먼저
      git merge-tree --write-tree origin/claude/friendly-meitner-lldvar origin/claude/evac-2026-10-22
    로 CONFLICT 줄이 있는지 본다. 허락을 받으면
      git merge --no-ff origin/claude/evac-2026-10-22 -m "merge claude/evac-2026-10-22 (대피 세션 10-22~10-26 · 82 커밋) — no-ff"
    ⛔ rebase · reset · force-push 하지 않는다 — evac 커밋 해시가 결정 원장 비준 (ratification.commit) · 런로그 ·
       gabia worktree (wt_r2el_1026 · wt_li2sk_1023) 에 박혀 있다.
    충돌은 ■3 → ■2 점검 → git push origin claude/friendly-meitner-lldvar (강제 없이).
- 대피 브랜치 claude/evac-2026-10-22 는 지우지 않는다 (기록이다). 어느 경우든 push 전에는 늘 fetch → FF 확인.

■ 2. 점검 — 들인 뒤 (대피 세션 10-26 실측 = 기대값)
    python3 tools/kb_wiki.py lint | tail -1                            # RESULT: 0 errors
    python3 tools/db/validate_canonical.py | tail -3                   # 거버넌스 결정 149 · 판정 8 · 그래프 무결성 ✅ / ✅ 배선 전부 일치
    python3 tools/convention_check.py | tail -1                        # 0 위반
    python3 -m pytest webapp/tests -q -p no:cacheprovider | tail -3    # 2 failed · 635 passed · 2 skipped (≈ 8 분)
        # 실패 둘은 대피 전부터 (대피 세션은 webapp/ · litdb/ 를 안 건드렸다 · 10-20 복귀 카드 ■2 와 같은 둘):
        #   test_v3_governance.py::test_kb_index_lists_only_ledger_referenced_docs — 비준된 결정 본문의 'kb/open_items.md ⏭-4 …' 문자열을
        #     화면이 문서 참조로 읽는다. 원장은 못 고친다 → 고치려면 화면 · 시험 쪽.
        #   test_webapp.py::test_recent_digests_are_on_every_litdb_surface — 10-14 litdb 펠릿 밀도 카드 넷이 litdb/comparison_vs_ours.md 에 없다.
        # 이 둘 말고 빨가면 들이기로 생긴 새 문제다.
    python3 -I tools/wad/build_round2_vasp_package.py --selftest | tail -1   # 194/194 (≈ 2 분 · python dftd3 1.6.0 필요)
    python3 -I tools/wad/build_v5_vasp_package.py --selftest | tail -1       # 237/237
    python3 -I tools/wad/build_aprime_interfaces.py --selftest | tail -1     # 79/79
    python3 -I tools/doping/dft_decomp_check.py --selftest | tail -1         # PASS — 66 ok, 0 bad
    python3 -I tools/doping/convex_hull_ehull.py --selftest | tail -1        # ⭕ 16 · ⛔ 0
    bash tools/doping/run_force_check_scf.sh --selftest | tail -1            # 11 통과 · 0 실패
    python3 -I tools/comp1_v3/per_site_bond_analysis.py --selftest | tail -1 # ✓ 11 · ✗ 0
    bash tools/electronic/run_nd_elf_nc_gabia.sh --selftest | tail -1        # ⭕ 55 · ⛔ 0 (≈ 3 분 · ase 필요)
    python3 -I tools/figures/build_nd_electronegativity_page.py --selftest | tail -1   # 41/41 (음성 16)
    python3 -I tools/figures/fig_li3nd_r2_geometry_2026_10_26.py --selftest | tail -1  # ✓ 5 · ✗ 0
    python3 -I tools/figures/fig_weekly_2026_10_25.py --selftest | tail -1             # ✓ 4 · ✗ 0
  기대와 다르면 고치기 전에 원인부터 (들이기 탓인지 · 환경 탓인지). 위 실패 목록 밖의 빨간불은 새 문제다.

■ 3. 충돌이 나면 (경우 B·C) — 파일별 규칙
- db/governance/decisions.json — 양쪽 결정을 전부 남긴다 (id 합집합). 비준된 결정 본문은 한 글자도 고치지 않는다
  (decision_digest = ratification 을 뺀 본문의 sha256). 대피 세션이 바꾼 것: 새 결정 6 (■5) · D-2026-10-20-nd-s-vacancy-closed proposed → active.
  같은 slot active 둘이면 검증기가 막는다. 저장은 json.dumps(…, ensure_ascii=False, indent=1) + "\n". 푼 뒤 validate_canonical.py.
- db/properties/citation_hazards.json — id 합집합 (대피 세션 새 항목은 HZ-li3nd-neb-si-conditional 하나).
- kb/open_items.md — 합집합. 대피 세션의 ⏭-NOW-z22 · z23 · z24 블록을 통째로 남기고 네 새 블록은 그 위에.
  머리 줄 (최종 갱신) 은 늦은 쪽. 머리 줄에 굵게를 겹쳐 쓰지 않는다 (대시보드 시험).
- CLAUDE.md — 대피 세션 판이 원장과 맞다 (■4 의 세 곳). 다른 절의 네 변경은 살린다.
- kb/index.md · kb/reviews/INDEX.md — 손으로 풀지 않는다. 아무 쪽이나 고르고 python3 tools/kb_wiki.py index (· reviews --write) → lint.
- JSON 런로그 — 원래 들여쓰기 그대로 다시 쓴다 (json.dumps(d, ensure_ascii=False, indent=N) + "\n" == 원문 인지 N = 1 · 2 로 먼저 본다).
- 비준된 카드 · 리뷰 회신 원문 · db/raw · 리뷰받은 묶음 폴더 (db/inputs/wad_round2_vasp_v2–v5_2026_10_22/) — 어느 쪽도 내용을 고치지 않는다.
  충돌이면 나중 판 (대피 세션) 을 쓰고 이유를 커밋 메시지에.

■ 4. 네 기억은 10-22 에 멈춰 있다 — 들인 뒤 먼저 다시 읽는다 (작업 시작 전)
- CLAUDE.md 를 다시 읽는다. 바뀐 곳 셋: ① 소통 — 상대 차이 인용정책은 팀 전제라 대화에서 강조하지 않는다 (10-23)
  ② argyrodite 이완 줄 — vc-relax 예외에 Nd Q2 분해 생성물 (비-argyrodite 기준 결정 · MP 구조에서 시작) ③ EOS 는 조건부 — 압력 어림이 먼저
  (|P| ≤ 2 GPa 이고 보정이 결론을 못 바꾸면 EOS 안 함 · 이온 이완은 빼지 않음 · 새 카드부터).
- kb/open_items.md 의 ⏭ 머리 줄 + ⏭-NOW-z22 · z23 · z24 (grep · 통째로 읽지 않는다).
- kb/projects/merge_request_2026_10_26.md — §2 커밋 (트랙별) · §4 원격 · §5 원장 · §6 알려진 것.
- 네가 10-22 에 하던 일 (W_ad CZ 고침 · Li₃Nd r2 · Nd EOS · li2s QE 사슬) 은 대피 세션에서 다 진행됐다 — 이어서 하기 전에 z22–z24 에서 지금 자리를 본다.
  특히 W_ad 는 묶음 v5 가 Codex DE GO 뒤 업체로 갔고 (10-23) 파일럿이 돌아와 단계 1–4 해제 파일까지 냈다.

■ 5. 새 결정 6 + 상태 변경 1 (원장이 정본 · 트랙을 먼저 쓴다)
- SEI Li₃Nd (1저자 = 사용자): D-2026-10-22-li3nd-r2-close-at-run-limit · D-2026-10-26-li3nd-neb-si-conditional (장벽은 SI 단서 문장으로만 ·
  인용위험 HZ-li3nd-neb-si-conditional CONDITIONAL · Li₂S 쪽은 그대로 BLOCKED) · D-2026-10-26-li3nd-r2-stop-now (전부 active)
- li2s 운용 (트랙은 ⛔ 외부 1저자 · gabia 운용 결정은 사용자): D-2026-10-23-gabia-li2s-k222-pause-li3nd (active · 두 잡 끝 — 범위 소진)
- CEI Nd (1저자 = 실험 쪽 · 결정은 '사용자'): D-2026-10-23-nd-q2-decomp-card (active) · D-2026-10-20-nd-s-vacancy-closed proposed → active ·
  D-2026-10-14-ndo-site-stability-estimand 는 아직 **proposed** (그래서 Q1 은 어디서나 '잠정')
- W_ad (1저자 = 사용자): D-2026-10-26-wad-round2-aggac-input-only (active · VASP 5.4.4 는 AGGAC 해석값을 안 찍어서 돌린 INCAR 로 확인 · '입력으로만 확인' 표지)

■ 6. 원격에서 지금 도는 것 (대피 세션 마지막 실측 · gabia 10-26 20:21 · kgy 19:11 KST) — 건드리지 않는다
- gabia tmux r2el: /root/r2stop_el_1026.sh 가 Li₃Nd r2 를 다음 BFGS 줄 직후 EXIT 로 세우고 (D-2026-10-26-li3nd-r2-stop-now) 닫는 숫자를 로그에 적은 뒤
  탄성 modelc_2x 를 다시 띄운다 (strain_13_m 은 BFGS 171 다음부터 · 그 뒤 12_p · 12_m · 러너는 GPU 32,000 MiB 가 빌 때까지 기다린다).
  로그 /root/logs/r2stop_el_1026.log · 탄성 /root/logs/el_modelc2x_1026.log · worktree /data/work/wt_r2el_1026 (evac 커밋).
  20:21 에는 r2 가 아직 돌았다 (pw.x 37,228 MiB · 13_m ⏸ · 12_p · 12_m 대기).
  ⛔ wt_r2el_1026 은 탄성이 끝날 때까지 지우거나 옮기지 않는다 (bash 가 스크립트를 조금씩 읽는다). fast-forward 뒤에는 그 커밋이 friendly 이력에 들어 있으니 그대로 둬도 된다.
- gabia tmux li3nd_r2_res_10231732: r2 재개 드라이버 (restart_qe_relax.sh --run --nstep 136 · 10-23 li2sk 러너가 건 것이라 worktree /data/work/wt_li2sk_1023 로 본다 —
  정리 전에 ps -o args 에 wt_li2sk_1023/tools/sei/restart_qe_relax.sh 가 있는지 확인) — r2 가 서면 끝난다. 그 뒤에만 wt_li2sk_1023 정리.
- kgy: 대피 세션이 아는 도는 잡 없음 (Nd Q2 k 탐침 회수 17b2a2b73 뒤 worktree 지움 · cascade v7 은 10-19 kill) — 사용자에게 확인.
- 외주 (W_ad 단계 1–4): 해제 파일 db/raw/wad_round2_vasp_2026_10_22/release_R2-REL-2026-10-26.tsv (sha d4f757b9…) 를 사용자가 업체에 보낸다.
- ⚠ 이제부터 원격 회수 블록은 friendly 로 push 한다 (evac 로 보내지 않는다). 메인 저장소 경로는 gabia /data/work/repo · kgy ~/lldvar (linked worktree).

■ 7. 이어서 할 것 (순서)
1) gabia r2el — 사용자에게 두 로그를 받는다 → r2 닫는 숫자 (마지막 BFGS · 에너지 차 · 최대 힘 · 거부 · 리셋) 를
   db/properties/li3nd_p333_control_runlog_2026_10_11.json 에 '✅_r2_닫음_<날짜>' 로 기록 → 탄성 13_m 이 이어 가는지 세 줄로 확인
   (Atomic positions and unit cell read from directory · initial density is read from file · 첫 SCF 뒤 number of bfgs steps 가 171 다음) →
   r2 드라이버 tmux 가 끝났으면 wt_li2sk_1023 정리 블록.
2) W_ad — 해제 파일 · 메일 발송 여부 (사용자) → 단계 1–4 반송 → 반송 검사 · 집계 (빌드 기록 db/properties/wad_round2_build_log_2026_10_17.json ⑦ · 해제 파일 상한) →
   은 V5 G5 집계는 DEM 회신 10 과 같이. ⛔ 점착 W 값은 kb · 화면 · 편지에 싣지 않는다.
3) CEI Nd — 1저자 송부 셋은 사용자 몫 (Q1 메시지 · Q2 메시지 kb/projects/nd_q2_message_send_2026_10_26.md · 설명 페이지 공유 — 새 Artifact 링크는
   db/properties/nd_q3_bader_elf_runlog_2026_10_19.json 의 ✅_1저자_설명_페이지_갱신_2026_10_26 · 비공개 · Share 는 사용자). Q1 카드를 사용자가 비준하면
   tools/figures/build_nd_electronegativity_page.py 를 다시 돌려 같은 링크로 다시 낸다 (다른 대화에서는 Artifact url 로 먼저 read · '잠정' 표지가 빠진다).
4) NdO-LPSCl1.6 원고 (CEI · 사용자 논문 아님 · 문장은 고치지 않고 인용 규율과 어긋나는 곳만 짚는다) — 원고 파일은 저장소에 없다 → 사용자에게 다시 받아
   같이 읽기를 이어 간다 (Introduction 1–2 문단까지 읽음 · 메모는 merge_request §6) → 4.5 DFT Methods 초안 (Fig. 3 f–h · Fig. 5 e,f).
5) li2s (⛔ 외부 1저자) — 편지 DA 발송 여부 확인 → 회신 대기.
6) litdb — 10-14 카드 넷을 litdb/comparison_vs_ours.md 에 (웹앱 실패 하나가 풀린다).
7) 그 밖은 kb/open_items.md ⏭ 절 (cascade 상한 재비준 🔔 · li2s 트랙 마감 문서 · BVSE R₀ 민감도 · Li₂S NEB 카드 · Feng/Wang ③ 🔔).
세션을 닫기 전에 kb/open_items.md ⏭ 절을 갱신한다 (⏭-NOW-z24 위에 새 블록).

■ 8. 사용자 운영 규칙 (CLAUDE.md 그대로 · 특히)
- 원격 작업은 붙여넣기 블록 → 사용자 실행 → 출력 회수. 붙여 준 출력은 하나씩 보고 해석한다 — 앞서가지 않는다.
- 인증을 묻는 명령 (git push · fetch) 뒤에는 다른 줄을 두지 않고 && 로 잇는다. 감시 블록은 watch -n 30 '…' 꼴 (따옴표 안은 $HOME).
- CPU 블록은 첫 줄에 '검사용 (메모리 프로브 · run 아님 · N 초 뒤 자동 종료)'. QE run 은 GPU 로만.
  gabia 에서 GPU pw.x 와 UMA 를 겹치지 않는다 (살아 있는 공존 예외 0 건).
- 프로세스는 PID 나 잡 고유 인자 (작업 폴더 cwd 포함) 로만 죽인다. 러너가 읽는 worktree 는 건드리지 않는다.
- 봉인 카드 · 리뷰 회신 원문 · 비준된 결정은 고치지 않는다 (정정은 새 파일 · supersede 재봉인).
- 점착 W 값 · li2s 절대 수송값은 표에도 싣지 않는다. 1저자는 트랙마다 다르다 — 결정을 쓸 때 트랙을 먼저 쓴다
  (W_ad · cascade · ESW · 탄성 · SEI = 사용자 · li2s = 외부 1저자 · CEI · Nd = 실험 쪽 다른 사람 (결정은 '사용자') · B₂O₃ · NdO 원고 = 다른 사람).
- 한국어 대화체로 짧게 · 그림 라벨은 영어 · 새 개념은 한 단계씩. "용훈 포메이션" 은 요청이 있을 때만 그 형식으로.

첫 답은: ■0 결과 한 줄씩 · 경우 A/B/C · 들인 결과 (HEAD 커밋 · push 결과) · ■2 요약 · ■6 에서 사용자에게 확인할 것 (r2el 로그 · kgy 상태 · 업체 발송).
원격 명령 블록은 사용자가 요청하거나 붙여 준 출력의 다음 한 수로만 준다.
```

## 1. 대피 세션이 한 일 — 트랙별 (자세한 것은 `kb/open_items.md` ⏭-NOW-z22 · z23 · z24 · 커밋은 머지 요청 §2)

- **W_ad 외주 2차 (1저자 = 사용자)** — Codex CZ 해제조건 일곱 → 자체 검토 고침 셋 → DB · DC · DD (NO-GO 셋 · 고침마다 새 묶음 폴더 v2–v5) → **DE GO** →
  업체 발송 (사용자 10-23) → 파일럿 반송 검사 → 사용자 결정 D1–D3 (AGGAC 입력 확인 · S_A far 진단 · 단계 상한) → PP 등록부 봉인 · 은 a4 결과 (미수렴 — 사전 규칙대로) ·
  **단계 1–4 해제 파일** (사용자가 업체에 보낸다).
- **CEI Nd (1저자 = 실험 쪽 · 결정은 '사용자')** — S 빈자리 마감 비준 · Q1 자리 (EOS 12 점 → V₀ 이온 이완 → 판독 · 카드 proposed 라 잠정 · 메시지 초안) ·
  Q2 분해 (결과 전 카드 · MP hull 기저 봉인 · kgy 6 잡 · 게이트 · k 탐침 · 판독 · 메시지 초안) · 1저자 설명 페이지 갱신 (새 Artifact 링크).
- **li2s (⛔ 외부 1저자)** — 모델 검증 QE 사슬 (kgy) · k 2×2×2 대조를 gabia 로 (r2 잠깐 세움) · 판독 · 편지 DA §6 · Q-DA-7 (발송은 사용자).
- **SEI Li₃Nd (1저자 = 사용자)** — r2 관측 · 기하 진단 (흔든 시작 구조 복원 · Nd 끼리 붙는 재배열) · 결정 실험 (NEB 끝점이 크게 재배열) →
  사용자 결정 셋 (3×3×3 NEB 재실행 안 함 · 2×2×2 장벽은 SI 단서 문장만 · r2 지금 정지 → 탄성 재개).
- **그 밖** — 주간 정리 10-19~10-25 · CLAUDE.md 세 곳 · NdO 원고 같이 읽기 시작 (Introduction 1–2 문단).

## 2. 왜 충돌이 안 나나 · 언제 나나

- friendly 끝 (`aaa275e20`) 이 evac 끝의 조상이다 — `--ff-only` 로 그대로 앞으로 간다. 파일 수준 충돌이 생길 자리가 없다.
- 충돌은 본 세션에 **커밋 안 한 변경** (경우 B) · **안 올린 로컬 커밋** 이 있거나 **다른 세션이 friendly 에 올렸을 때** (경우 C) 만 생긴다.
  대피 기간에 많이 바뀐 공용 파일은 `db/governance/decisions.json` (+458 줄) · `kb/open_items.md` · `kb/index.md` · `kb/reviews/INDEX.md` · `db/properties/citation_hazards.json` · `CLAUDE.md` (7 줄) —
  본 세션이 이 파일들을 로컬에서 고쳐 두었다면 ■3 규칙으로 푼다.
- 사용자 로컬 체크아웃 (웹앱 127.0.0.1:5001 이 읽는 곳) 이 friendly 에 있으면 `git pull --ff-only` 로 맞춘다 — 안 하면 화면이 10-22 판이다.
  웹앱 코드는 안 바뀌었으니 서버 재시작은 필요 없다.
