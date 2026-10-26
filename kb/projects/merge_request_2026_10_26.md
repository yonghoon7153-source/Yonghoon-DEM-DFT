---
title: "머지 요청 — 대피 브랜치 claude/evac-2026-10-22 → claude/friendly-meitner-lldvar (2026-10-26 · fast-forward · 충돌 0)"
date: 2026-10-26
updated: 2026-10-26
tags: [merge, evacuation, handoff, wad, vasp, outsourcing, cei, nd, li2s, li3nd, elastic, weekly]
status: 최종 — 10-26 실측 (friendly 끝 = 대피 인계 카드 aaa275e20 · fast-forward 가능 · 점검 §3). friendly 세션이 kb/projects/handoff_2026_10_26_return_to_origin.md §0 프롬프트로 들인다
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


# 머지 요청 — `claude/evac-2026-10-22` → `claude/friendly-meitner-lldvar`

> 대피 카드 `kb/projects/handoff_2026_10_22_evacuation.md` ■6 절차를 따른다. 되돌아가는 쪽 프롬프트는
> `kb/projects/handoff_2026_10_26_return_to_origin.md` §0 이다. 선례: `merge_request_2026_09_28.md` (fast-forward) · `merge_request_2026_10_05.md` (no-ff · friendly 가 움직였던 경우).
> **이 문서 하나로 머지 판단이 되게** 쓴다 — 커밋 · 점검 · 원격 상태 · 원장 변화 · 알려진 것 · 다음 일.
> ⛔ 이 문서는 `/kb` 화면으로 렌더된다 — 점착 W 값 · li2s 절대 수송값 · 인용 등급이 걸린 장벽 숫자는 옮겨 적지 않는다 (위치만).

## 0. 한눈에

- **fast-forward · 충돌 0** (10-26 실측). friendly 끝 = **`aaa275e20`** (10-22 대피 인계 카드 · 10-22 00:55 UTC) = merge-base.
  - friendly 에만 **0** 커밋 — 대피 중 아무도 friendly 에 쓰지 않았다 (대피 카드 ■5 조건이 지켜졌다).
  - evac 에만 **81** 커밋 + 이 카드 커밋 = **82**. 그중 **9** 개는 사용자가 원격 기계 (kgy · gabia) 회수 블록으로 올린 커밋이다 (§2 표의 '(kgy)' · '(gabia)').
  - 1000 파일 +560,124 / −439 (대부분 원자료 `db/raw/` · 묶음 폴더 `db/inputs/wad_round2_vasp_v2–v5_2026_10_22/`).
  - ⇒ 들이기는 `git merge --ff-only origin/claude/evac-2026-10-22` 한 줄이다. 같이 바뀐 파일이 없으니 텍스트 충돌이 생길 자리가 없다.
- 점검 = evac 끝 (= fast-forward 뒤 friendly 트리) 에서 전부 다시 돌렸다 (§3). 원장 · kb · 규약 초록 · 바뀐 도구 selftest 13 개 PASS ·
  웹앱 **635 passed · 2 skipped · 실패 2 (둘 다 대피 전부터 · §6)**.
- 원격: gabia 에서 **r2 정지 → 탄성 재개** 스크립트가 evac worktree 에서 돈다 (§4). 머지와 무관하게 계속 돈다.
- ⚠ 머지 뒤 원격 회수 블록은 다시 **friendly 로** push 한다 (evac 로 보내지 않는다).

## 1. 병합 방법 (요약 — 정본은 복귀 카드 §0 ■0–■2)

1. 쓰기 전에 확인: `git status` 비었음 · 안 올린 로컬 커밋 0 · friendly 끝이 `aaa275e20` · `merge-base --is-ancestor` 통과 · evac 에만 82 (그보다 많으면 회수 커밋인지 본다).
2. `git switch claude/friendly-meitner-lldvar && git merge --ff-only origin/claude/friendly-meitner-lldvar && git merge --ff-only origin/claude/evac-2026-10-22`
3. §3 점검을 다시 돌리고 기대값과 같으면 `git push origin claude/friendly-meitner-lldvar` (**강제 없이**).
4. friendly 가 그사이 움직였으면 (FF 불가) **멈추고 사용자에게 보인다** → 허락 뒤 `git merge --no-ff` (복귀 카드 ■1 경우 C · ■3 충돌 규칙). ⛔ rebase · reset · force-push 금지 —
   evac 커밋 해시가 결정 비준 (`ratification.commit`) · 런로그 · gabia worktree 에 박혀 있다.

## 2. 커밋 (`git log --oneline aaa275e20..origin/claude/evac-2026-10-22` · 트랙별로 묶음)

> 시각은 커밋 기록 그대로다 (컨테이너 커밋은 UTC · 사용자 회수 커밋은 KST).

| 트랙 (1저자) | 커밋 | 무엇 |
|---|---|---|
| **대피 시작 · 주간** | `83b7183a0` · `0f2def59b` · `5bf9c5430` · `dfd375af6` | 사용자 결정 셋 (대피 카드 §4) · open_items ⏭-NOW-z22 와 그 갱신 |
| | `47af60bc6` | 주간 정리 10-19~10-25 (`kb/reports/weekly_2026_10_25.md` · 그림 1 · `/weekly` 최신) |
| **W_ad 외주 2차** (사용자) | `01c1cc4bd` · `90ba35b17` · `744edd949` · `c4725b51e` · `0eaa4896a` · `44b095ef9` · `b3c13f0aa` | Codex CZ 해제조건 일곱 (하나 = 커밋 하나) · 묶음 v2 |
| | `ed84da61d` · `c11446827` · `a9cf825b0` · `a551036e3` · `3d684e502` · `5726dd618` | 편지 DB 초안 · 발송 전 자체 검토 고침 셋 · v2 다시 빌드 · DB 개정 |
| | `c475bf304` · `ea3bc0093` · `4e8d0ceba` · `576a6d644` · `881580040` · `3e70329cb` | DB 회신 (NO-GO) 원문 · 해제조건 넷 + P2 · 묶음 v3 |
| | `d3f41b333` · `4c1ae1e00` · `d538279df` · `1e4d113d2` | 편지 DC · 회신 (NO-GO) · 고침 · 묶음 v4 |
| | `5bec71f8d` · `31603c13c` · `c4d0f0d39` · `9ddfbe448` | 편지 DD · 회신 (NO-GO) · 고침 · 묶음 v5 |
| | `38608b65b` · `afa7ee378` · `7d4681e4b` | 편지 DE · **GO** · 업체 zip · **업체 발송** (사용자 10-23) |
| | `f8eb678df` · `f0c8d874c` · `0289eb3eb` · `496244e36` | 파일럿 반송 검사 · 상한 재유도 제안 · AGGAC 입력 확인 (사용자 결정 D1) · D1–D3 기록 · PP 등록부 봉인 · 은 a4 결과 · **단계 1–4 해제 파일** |
| **CEI Nd** (1저자 = 실험 쪽 · 결정은 '사용자') | `296de8e98` | S 빈자리 마감 비준 (proposed → active) |
| | `25b345c1e` · `721556a06` (kgy) · `6283f33d9` · `4c046e16b` · `1fdf43b9b` (kgy) · `94b42331a` · `d6931855f` · `32536f2af` | Q1 자리: EOS 12 점 · 맞춤 · V₀ 이온 이완 · 판독 (잠정 — 카드 proposed) · 1저자 메시지 초안 |
| | `ae55a8024` · `b29b4a71d` · `d6955c120` · `804164101` (gabia) · `e9402168c` · `dac0ad04f` (gabia) · `305629d63` | Q2 분해: 결과 전 카드 · 비준 (+ CLAUDE.md EOS 조건부 규칙) · 도구 확장 · MP hull 기저 (혼합 hull 문제 → GGA_GGA+U 명시) · 기저 봉인 |
| | `875791a05` · `d11e40a89` (kgy) · `40f3a984a` · `17b2a2b73` (kgy) · `747ba5913` · `aa6b32983` | Q2: kgy 발사 · 회수 · 게이트 (Pulay 파서 고침) · k 탐침 회수 · **판독** · 1저자 메시지 초안 |
| | `fbabb8b2f` | 1저자 설명 페이지 갱신 (Q1 · Q2 · S 빈자리 · Fig. 3g 인용 범위 · 생성기 검사 ⑦–⑪) |
| **li2s** (⛔ 외부 1저자) | `93275b710` · `4a8599715` · `bc7288a58` · `de26e3be1` (kgy) | 모델 검증 QE 사슬 (sp 10 · Pulay 2 · k 2×2×2 는 3090 에서 OOM · 원인 = QE 자체 어림이 카드 한 장보다 큼) · 회수 |
| | `0e549060d` · `b4013bb03` · `a10754d1f` · `860b8226d` · `8a0abefe8` (gabia) | k 2×2×2 대조 + Γ 기계 대조를 gabia A6000 으로 (r2 잠깐 세움 · 결정 active) · 회수 |
| | `ca606895d` · `75aeb1090` · `2189141b3` | 모델 검증 판독 · 편지 DA §6 · Q-DA-7 |
| **SEI Li₃Nd** (사용자) | `0fe922f04` · `dd83fc24c` · `e479d738f` (gabia) · `8eb174749` · `e46b5f625` · `9927d8ef3` | r2 관측 둘 · 기하 추출 · 진단 · 결정 실험 · **사용자 결정 셋** (3×3×3 NEB 재실행 안 함 · 장벽은 SI 단서 문장만 · r2 지금 정지) |
| **상시 규칙** | `d5632d64e` | CLAUDE.md: 상대 차이 인용정책은 팀 전제 — 대화에서 강조하지 않는다 (사용자 10-23) |
| **마감** | (이 카드 커밋) | 머지 요청 · 복귀 카드 · open_items ⏭-NOW-z24 · kb/index.md 재생성 |

## 3. 점검 (evac 끝 `fbabb8b2f` = fast-forward 뒤 friendly 트리 · 10-26 실측)

이 카드 커밋은 `kb/` 만 고친다 — 결과가 바뀌지 않는다 (kb lint 는 이 커밋 뒤에 다시 돌렸다).

| 무엇 | 결과 |
|---|---|
| `git merge-base --is-ancestor origin/claude/friendly-meitner-lldvar origin/claude/evac-2026-10-22` | 통과 (FF 가능) · friendly 에만 0 · evac 에만 81 (+ 이 카드) |
| `tools/kb_wiki.py lint` | RESULT: 0 errors |
| `tools/db/validate_canonical.py` | ✅ 배선된 항목 전부 원자료와 일치 · 거버넌스 결정 **149** · 판정 8 · 그래프 무결성 ✅ |
| `tools/convention_check.py` | 0 위반 |
| 웹앱 전체 `pytest webapp/tests -q -p no:cacheprovider` | **635 passed · 2 skipped · 실패 2** (둘 다 대피 전부터 — §6) · 7 분 46 초 |
| `tools/wad/build_round2_vasp_package.py --selftest` | 194/194 (1 분 44 초) |
| `tools/wad/build_v5_vasp_package.py --selftest` | 237/237 |
| `tools/wad/build_aprime_interfaces.py --selftest` | 79/79 |
| `tools/doping/dft_decomp_check.py --selftest` | PASS — 66 ok · 0 bad |
| `tools/doping/convex_hull_ehull.py --selftest` | tieline ⭕ 16 · ⛔ 0 |
| `tools/doping/run_force_check_scf.sh --selftest` | 11 통과 · 0 실패 |
| `tools/comp1_v3/per_site_bond_analysis.py --selftest` | ✓ 11 · ✗ 0 |
| `tools/electronic/run_nd_elf_nc_gabia.sh --selftest` | ⭕ 55 · ⛔ 0 (3 분 10 초 · ase 필요) |
| `tools/figures/build_nd_electronegativity_page.py --selftest` | 41/41 (음성 16) · 깨기 9/9 빨강 (대피 세션에서) |
| `tools/figures/fig_li3nd_r2_geometry_2026_10_26.py --selftest` | ✓ 5 · ✗ 0 |
| `tools/figures/fig_weekly_2026_10_25.py --selftest` | ✓ 4 · ✗ 0 |

## 4. 원격에 지금 도는 것 (마지막 실측: gabia 10-26 20:21 KST · kgy 10-26 19:11 KST — 사용자 붙여넣기)

| 기계 | 무엇 (트랙) | 식별 | 다음 |
|---|---|---|---|
| gabia | **r2 정지 → 탄성 재개** (SEI Li₃Nd · 사용자 / 탄성 · 우리 DFT · 사용자) | tmux `r2el` · `/root/r2stop_el_1026.sh` · 로그 `/root/logs/r2stop_el_1026.log` · 탄성 로그 `/root/logs/el_modelc2x_1026.log` · worktree `/data/work/wt_r2el_1026` (evac 커밋 — 사용자 실행 시각으로 보면 `9927d8ef3` · `git -C … log -1` 로 확인) | 20:21 에는 r2 pw.x (37,228 MiB) 가 아직 돌고 스크립트가 다음 BFGS 줄을 기다렸다 (strain_13_m ⏸ · 12_p · 12_m 대기). 그 뒤 'EXIT → ✅ 세움 → 닫는 숫자 → ▶ 탄성 재개' (결정 `D-2026-10-26-li3nd-r2-stop-now`). 탄성은 13_m 을 BFGS 171 다음부터 이어 간다 |
| gabia | r2 재개 드라이버 (10-23) | tmux `li3nd_r2_res_10231732` · `restart_qe_relax.sh --run --nstep 136` · 10-23 li2sk 러너가 건 것이라 worktree `/data/work/wt_li2sk_1023` 로 본다 (정리 전에 `ps -o args` 로 확인) | r2 가 위 스크립트로 서면 끝난다. 그 뒤에만 `wt_li2sk_1023` 정리 |
| kgy | — | 이 세션이 아는 도는 잡 없음 (Nd Q2 k 탐침 회수 `17b2a2b73` 뒤 worktree 지움 · cascade v7 은 10-19 kill) | 사용자에게 확인 |
| 외주 | **W_ad 단계 1–4** (사용자) | 해제 파일 `db/raw/wad_round2_vasp_2026_10_22/release_R2-REL-2026-10-26.tsv` (sha `d4f757b9…` · 상한 합 1430) | 사용자가 업체에 보낸다 → 반송 대기 |

- ⛔ 위 worktree 둘은 **러너가 끝날 때까지 지우거나 다른 커밋으로 옮기지 않는다** (bash 는 스크립트를 조금씩 읽는다). 탄성은 며칠 간다 — `wt_r2el_1026` 은 탄성이 끝날 때까지 둔다.
  두 worktree 의 커밋은 fast-forward 뒤 friendly 이력에 그대로 들어 있으니 detached 로 남아도 문제없다.
- ⚠ **병합 뒤 원격 회수 블록은 friendly 로 보낸다.** 형식은 그대로다: `git -C <메인 저장소> fetch origin claude/friendly-meitner-lldvar` → 임시 worktree (`FETCH_HEAD`) → 원자료 · `SHA256SUMS` → commit →
  `git push origin HEAD:claude/friendly-meitner-lldvar` → 임시 worktree 제거 (gabia 메인 = `/data/work/repo` · kgy 메인 = `~/lldvar` 는 linked worktree 라 `git -C ~/lldvar rev-parse --git-dir` 로 묻는다).

## 5. 원장에 새로 생긴 것 · 바뀐 것

- **결정 143 → 149** — 새 6 건 (전부 active):
  - SEI Li₃Nd (사용자): `D-2026-10-22-li3nd-r2-close-at-run-limit` · `D-2026-10-26-li3nd-neb-si-conditional` · `D-2026-10-26-li3nd-r2-stop-now`
  - li2s 운용 (gabia · r2 잠깐 세움): `D-2026-10-23-gabia-li2s-k222-pause-li3nd`
  - CEI Nd (결정은 '사용자'): `D-2026-10-23-nd-q2-decomp-card`
  - W_ad (사용자): `D-2026-10-26-wad-round2-aggac-input-only`
- **상태가 바뀐 결정 1 건**: `D-2026-10-20-nd-s-vacancy-closed` proposed → **active** (`296de8e98`).
- **아직 proposed 인 것 (이 세션 범위)**: `D-2026-10-14-ndo-site-stability-estimand` (Nd Q1 카드 — 그래서 Q1 은 화면 · 메시지 · 설명 페이지에서 '잠정') ·
  `D-2026-10-19-lpscl-smallcell-glass-model-check` (li2s · 외부 1저자 동의 = 편지 DA).
- **인용위험 44 → 45**: `HZ-li3nd-neb-si-conditional` (CONDITIONAL — Li₃Nd 2×2×2 장벽은 SI 단서 문장으로만 · 본문 · Li₂S 와의 순위 금지). 나머지 NEB 값은 기존 BLOCKED 항목 그대로.
- **리뷰 회신** (`kb/reviews/INDEX.md`): Codex DB · DC · DD (NO-GO) · DE (GO) — W_ad 외주 2차 묶음 v2–v5.
- **CLAUDE.md** (세 곳 · 덧붙임만):
  - 소통: 상대 차이 인용정책은 팀 전제 — 대화에서 강조하지 않는다 (10-23).
  - argyrodite 이완 줄: vc-relax 예외에 Nd Q2 분해 생성물 (비-argyrodite 기준 결정 · `D-2026-10-23-nd-q2-decomp-card`) 추가.
  - **EOS 는 조건부** — 압력 어림이 먼저 (|P| ≤ 2 GPa 이고 보정이 결론을 못 바꾸면 EOS 안 함 · 이온 이완은 빼지 않음 · 새 카드부터).
- **W_ad 기록**: 빌드 기록 `db/properties/wad_round2_build_log_2026_10_17.json` (⑤ … ⑦) · 발송 기록 `db/properties/wad_round2_vasp_handoff_v5_2026_10_22.json` ·
  개정 `db/properties/wad_round2_amendment_aggac_input_only_2026_10_26.json` · 파일럿 반송 `db/raw/wad_round2_vasp_2026_10_22/` (PP 등록부 · a4 결과 · 해제 파일).
- **CEI Nd 기록**: Q1 `ndo_site_dft_runlog_2026_10_15.json` · `ndo_site_dft_v0_readout_2026_10_23.json` · `ndo_site_eos_fit_2026_10_23.json` /
  Q2 `nd_q2_decomp_estimand_2026_10_23.json` · `nd_q2_decomp_runlog_2026_10_23.json` · `nd_q2_decomp_readout_2026_10_26.json` /
  메시지 초안 `kb/projects/nd_q2_message_send_2026_10_26.md` (Q1 초안은 Q1 런로그) / 설명 페이지 `db/properties/cei_figs/cei_nd_electronegativity.html` (+ Origin CSV 8).
- **li2s 기록**: `lpscl_glass_model_check_runlog_2026_10_19.json` · 편지 DA (`kb/reviews/` · §6 · Q-DA-7).
- **SEI Li₃Nd 기록**: `li3nd_p333_control_runlog_2026_10_11.json` (r2 관측 · 기하 · 결정 실험 · 사용자 결정) · 그림 `tools/figures/fig_li3nd_r2_geometry_2026_10_26.py`.
- **화면 (webapp 코드 변경 없음)**: `/weekly` 가 10-19~10-25 판을 읽는다. `webapp/` 아래 파일은 하나도 안 바뀌었다.

## 6. 알려진 것 — 머지 전에 알 것

- 웹앱 실패 둘은 **대피 전부터** 있었다 (10-20 복귀 카드 ■2 에 이미 적혀 있다 · 대피 세션은 `webapp/` · `litdb/` 를 안 건드렸다):
  - `test_v3_governance.py::test_kb_index_lists_only_ledger_referenced_docs` — 비준된 결정 본문의 'kb/open_items.md ⏭-4 …' 문자열을 화면이 문서 참조로 읽는다. 원장은 못 고친다 → 고치려면 화면 · 시험 쪽.
  - `test_webapp.py::test_recent_digests_are_on_every_litdb_surface` — 10-14 litdb 펠릿 밀도 카드 넷 (`tron2023_lpscl_ccd_ambient_pressure` · `beutl2024_round_robin_coin_cell_sulfide_assb` ·
    `wang2024_hot_pressed_lpscl_pressure_invariant_conductivity` · `larson2025_hot_pressing_argyrodite_low_stack_pressure_conductivity`) 이 `litdb/INDEX.md` 에는 있고 `litdb/comparison_vs_ours.md` 에 없다 (`984e5be42`).
- Nd 설명 페이지의 Artifact 링크가 바뀌었다 — 10-20 링크는 이 계정에서 'not found' 라 같은 자리에 못 덮었다. 새 링크는 런로그 `nd_q3_bader_elf_runlog_2026_10_19.json` 의 `✅_1저자_설명_페이지_갱신_2026_10_26` (비공개 · 1저자 공유는 사용자가 Share 로).
- NdO-LPSCl1.6 원고 (CEI · 1저자 = 실험 쪽 · 사용자 논문 아님) 파일은 **저장소에 없다** (사용자가 대피 세션에 올린 업로드). Methods 초안 일을 이어 가려면 사용자에게 파일을 다시 받는다.
  같이 읽기는 Introduction 1–2 문단까지 했다 (우리 계산값 없음 · 짚을 인용 문제 없음 · 메모: Fig. 5e,f 자리에 '[Specify the reaction pathways …]' 빈칸 · Intro 가 '전자가 새는 계면상' 을 문제로 깔았는데 우리 분류에서 Li₃Nd 는 금속 — Fig. 3 읽을 때 같이 본다).
- CLAUDE.md Git 절은 'friendly 에만 커밋' 이다. 대피 세션은 대피 프롬프트에 따라 evac 에 커밋했다 — **병합 뒤에는 다시 friendly 규칙**이다.

## 7. 머지 뒤 friendly 에서 이어서 할 것 (순서)

1. **사용자 로컬 갱신 안내** — `git switch claude/friendly-meitner-lldvar && git pull --ff-only`. 웹앱 코드는 안 바뀌었으니 서버 재시작은 필요 없다 (`/weekly` 등은 새 데이터를 읽는다).
2. **gabia r2el** (SEI · 탄성) — 사용자에게 `/root/logs/r2stop_el_1026.log` · `/root/logs/el_modelc2x_1026.log` 를 받아:
   r2 닫는 숫자 (마지막 BFGS · 에너지 차 · 최대 힘 · 거부 · 리셋) 를 `li3nd_p333_control_runlog_2026_10_11.json` 에 `✅_r2_닫음_<날짜>` 로 기록 →
   탄성 13_m 이 이어 가는지 세 줄로 확인 (*Atomic positions and unit cell read from directory* · *initial density is read from file* · 첫 SCF 뒤 `number of bfgs steps` 가 171 다음) → 그 뒤 `wt_li2sk_1023` 정리 블록.
3. **W_ad** — 사용자가 해제 파일 + 메일을 업체에 보냈는지 → 단계 1–4 반송 → `--check` → 집계 (빌드 기록 ⑦ · 상한 = 해제 파일) · 은 V5 G5 집계는 DEM 회신 10 과 같이 · W 값은 결과 기록에만.
4. **CEI Nd** (결정은 '사용자') — 1저자 송부 셋 (Q1 메시지 · Q2 메시지 · 설명 페이지 공유) 은 사용자 몫 · Q1 카드 비준 여부 (비준하면 설명 페이지를 다시 만들어 같은 링크로 — 다른 대화에서는 `url` 로 먼저 read).
5. **NdO 원고** — 파일을 다시 받아 같이 읽기 이어서 → 4.5 DFT Methods 초안 (Fig. 3 f–h · Fig. 5 e,f · Li₃Nd 는 SI 단서 문장 · Li₂S 장벽은 인용 금지 · Fig. 3h 갭 출처).
6. **li2s** (⛔ 외부 1저자) — 편지 DA 발송 여부 확인 (사용자) → 회신 대기.
7. **litdb 비교표** — 10-14 카드 넷을 `comparison_vs_ours.md` 에 (§6 실패 하나가 풀린다).
8. 그 밖은 `kb/open_items.md` ⏭ 절 (cascade 상한 재비준 🔔 · li2s 트랙 마감 문서 · BVSE R₀ 민감도 · Li₂S NEB 카드 · Feng/Wang ③ 🔔).

## 8. 이 문서가 못 하는 것

- 점검은 **10-26 evac 끝** 기준이다. friendly 세션이 들이기 직전에 다시 센다 — friendly 나 evac 가 그사이 움직였을 수 있다 (다른 세션 · 회수 커밋).
- 원격 상태는 사용자가 붙여 준 마지막 출력이다 (gabia 20:21 · kgy 19:11 KST). r2 가 실제로 섰는지 · 탄성이 다시 떴는지는 아직 모른다.
- W_ad 해제 파일을 업체에 보냈는지 · li2s 편지 DA 를 보냈는지 · Nd 메시지를 보냈는지는 이 세션이 모른다.
