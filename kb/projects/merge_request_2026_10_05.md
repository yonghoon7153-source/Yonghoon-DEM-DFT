---
title: "머지 요청 (최종) — 대피 브랜치 claude/evac-2026-10-02 → claude/friendly-meitner-lldvar (2026-10-05)"
date: 2026-10-05
updated: 2026-10-05
tags: [merge, evacuation, handoff, wad, p1b, li2s, cascade, esw, litdb]
status: 최종 — 10-05 밤 실측 (no-ff · 가상 병합 텍스트 충돌 0 · 웹앱 637 passed). origin 세션이 kb/projects/handoff_2026_10_05_return_to_origin.md §0 프롬프트로 들인다
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

# 머지 요청 (최종) — `claude/evac-2026-10-02` → `claude/friendly-meitner-lldvar`

> 대피 카드 `kb/projects/handoff_2026_10_02_evacuation.md` ■6 절차를 따른다. 되돌아가는 쪽 프롬프트는
> `kb/projects/handoff_2026_10_05_return_to_origin.md` §0 이다. 선례: `merge_request_2026_09_28.md` (그때는 fast-forward).
> **이 문서 하나로 머지 판단이 되게** 쓴다 — 커밋 · 시험 · 원격 상태 · 원장 변화 · 알려진 것 · 다음 일.

## 0. 한눈에

- **no-ff 병합 · 텍스트 충돌 0** (10-05 밤 KST 실측). merge-base `721f9538` (10-02 대피 인계 카드 커밋).
  - friendly 에만 **2** 커밋 — `e7f425b8` · `8e3d7a5d` (DEM 쪽 litdb τ 문헌 세션 · `litdb/` 만 고침).
  - evac 에만 **64** 커밋 + 이 카드 커밋 = **65**. 529 파일 +226,973 / −101 (대부분 원자료).
  - ⇒ fast-forward 는 안 된다. **rebase 도 안 된다** — evac 커밋 해시가 결정 비준(`ratification.commit`) **13 건** ·
    원격 러너 worktree 4 곳 · 기록에 박혀 있다. 그래서 `git merge --no-ff` 다.
- 양쪽이 **같이 바꾼 파일은 `litdb/figures/_sources.json` 하나**다. `git merge-tree` 가 자동 병합했고,
  병합본 JSON 이 파싱된다 (키 349).
- **가상 병합을 실제로 돌려 봤다.** 위 병합과 같은 트리로 커밋을 만들고 (어디에도 안 올림) 임시 worktree 에 풀어 점검을 전부 돌렸다 (§3).
  - validate_canonical ✅ (결정 118) · kb lint 0 · convention 0 · litdb 인덱스 누락 0.
  - 웹앱 **637 passed · 2 skipped · 0 failed** · 다섯 화면 200 · 대피 세션 도구 selftest 7 개 PASS.
- 원격 계산 다섯 줄이 돈다 (§4). 병합과 무관하게 계속 돈다. 그중 넷은 **evac 커밋의 worktree 에서 스크립트를 읽는 중**이다.
- ⚠ 병합 뒤 원격 회수 블록은 **friendly 로** push 한다. evac 로 보내지 않는다 (§4 끝).

## 1. 병합 방법 (요약 — 정본은 복귀 카드 §0 ■0–■2)

1. 쓰기 전에 확인: `git status` 비었음 · 안 올린 로컬 커밋 0 · friendly 쪽 변경이 `litdb/` 만 · `git merge-tree` 에 CONFLICT 없음 · evac 에만 65.
2. `git switch claude/friendly-meitner-lldvar && git merge --ff-only origin/claude/friendly-meitner-lldvar`
   (로컬 friendly 를 원격 끝으로 — DEM 커밋 둘을 받는다)
3. `git merge --no-ff origin/claude/evac-2026-10-02 -m "merge claude/evac-2026-10-02 (대피 세션 10-03~10-05 · 65 커밋) — no-ff · 충돌 0"`
4. §3 점검을 병합본에서 다시 돌리고 기대값과 같으면 `git push origin claude/friendly-meitner-lldvar` (**강제 없이**).
5. 기대와 다르면 (로컬 커밋 · `litdb/` 밖 변경 · CONFLICT · 커밋 수) **멈추고 사용자에게 보인다** — 충돌 규칙은 복귀 카드 ■3.

## 2. 커밋 (`git log --oneline origin/claude/friendly-meitner-lldvar..origin/claude/evac-2026-10-02` · 트랙별로 묶음)

> 시각은 커밋 기록 그대로다 (컨테이너 커밋은 UTC · kgy 회수 커밋 `d2bfb55a` · `365a53ae` 는 KST).

| 트랙 (1저자) | 커밋 | 무엇 |
|---|---|---|
| **점착 P1b** (사용자) | `cdd3a2e8` · `1ea087cc` | 기계 대조 G1 PASS (kgy = V100 · \|ΔW\| 1.0e-7) · 총 견적 (7 일 안 · kgy 유지) |
| | `d2bfb55a` (kgy) · `4d829add` | 1단계 7 relax + 2단계 31 SCF 원자료 · 결과 기록 (G4 k 축 FAIL 라벨) |
| | `afa53812` · `3bd839ac` · `9160143e` · `19bc83ed` | k12 탐침 (1저자 결정 (c)) · 비준 · 묶음 해시 정정 · START 줄 정정 |
| | `365a53ae` (kgy) · `6181d053` | k12 탐침 원자료 · 판독 **CONVERGED_AT_K9** (레포 재집계 = kgy 집계) |
| | `89c5ab62` · `691f4055` | **마감 (a′)** — 라벨로 닫기 · 비준 |
| | `bb12faa2` · `6adf297c` · `2b82d12c` | **재개 ① (b)** 나머지 넷 9×9×1 (8 잡) · 비준 · kgy 발사 기록 |
| **점착 기타** (사용자) | `e3d72a1f` | W 값 정리 PPT 생성기 (QE · UMA · 숫자는 결과 기록에서만 · 화면에 안 올림) |
| | `48c5f7d0` | V5 VASP 파일럿 반송 — `--check` 2 잡 OK · PP 등록부 봉인 (`a279d529`) |
| **li2s** (⛔ 외부 1저자) | `07e4577b` (일부) · `8e3c1490` · `a6e37f4d` · `70ce36ea` · `fa729b30` | v2 인벤토리 · 회신 CO → 판독 전 개정 · 비준 · 판독 도구 정정 (결과 전) |
| | `281eb413` · `08360365` | v2 판독 (N₅₅₀ 2/5 · N₆₀₀ 5/5 → v2-2) · 편지 CQ 초안 |
| | `629cb790` · `054c295e` · `b6084fa0` | 회신 CQ 원문 · **v2 마감** 비준 · p90² 측정 기록 |
| | `3461c778` · `b8886c26` · `8983c65b` | **대조 계 a-Li₃PS₄ 카드** · 회신 CR · 비준 |
| | `4d829add` (일부) · `c704348b` · `e79c806d` | 담금질 러너 · 중복 실행 가드 배선 정정 · kgy 발사 기록 (seed1 15:35:59) |
| | `909456dc` · `1620517d` · `621eb657` · `2280fa96` | 비용 견적 오류 (시드당 3 h → 실측 33–39 h) · 편지 CS 초안 · 발송판 · 발송 |
| | `07302e9f` · `a01f331c` · `58d1e0d3` | 회신 CS 원문 · 비용 개정 (**상한 140** · 넷이면 다섯째) · 비준 |
| | `71e7e9f0` · `7a475e4d` · `17aced0b` · `d5cda746` | gabia 공존 예외 (5) · 비준 · **예외 (4) supersede 재봉인** · gabia 발사 (seed3 20:48:40) |
| **cascade** (사용자) | `4f449f04` · `aaed9bee` (일부) · `03ce7cbe` | 편지 CP 발송 · 회신 CP 원문 + v7 개정 · 카드 + 개정 비준 |
| | `a2924895` · `06a9900d` · `6bacad49` | v7 탐침 러너 · 감시 · kgy 발사 (10-03 20:24:38) |
| | `9e4157ec` · `761d7f8a` | 800 K 탈락 (규칙) · 1000 K H0 s1 자격 통과 · 누적 21.22 / 141 GPU-h |
| **ESW** (사용자) | `07e4577b` (일부) · `2f7406cb` | E2 진단 블록 · E2b 결과 (0.246 V = MP2020 황 음이온 보정 · CONDITIONAL 유지) |
| **상시 규칙** (우리 DFT · 사용자) | `3ccb0982` | 짧은 MD '무반응' 의 관측창 한 줄 · ≳2 eV 흡착값은 결합 자리 배위수 |
| **litdb** (SE 축 · 우리 쪽) | `aaed9bee` (일부) · `7beb1f21` · `accfc252` · `74a5c592` · `b95c0393` | Wu 2026 · Nosrati 2026 · Sun 2026 · Cao 2026 · Qi 2025 |
| | `9cc9fcf2` · `ad744a06` · `30b09686` · `9fa3df94` · `9233929f` | Yuan 2026 · Kim 2026 |
| **주간·화면** | `cb8b4566` · `8ce22ec3` | 주간 정리 09-28~10-04 + 그림 · 화면 갱신 · 'webapp 반영은 복귀 머지 뒤' (사용자 10-05) |
| **마감** | (이 카드 커밋) | 머지 요청 · 복귀 카드 · open_items ⏭-NOW-z7 · kb/index.md 재생성 |

## 3. 돌린 시험 · 검증 (가상 병합본 · 10-05 밤 KST)

가상 병합 = `git merge-tree --write-tree origin/claude/friendly-meitner-lldvar <evac 끝 2b82d12c>` 의 트리로 만든 커밋 (부모 둘 · 어디에도 안 올림)을 임시 worktree 에 풀었다.
이 카드 커밋은 `kb/` 만 고치므로 결과가 바뀌지 않는다 (kb lint 는 이 커밋 뒤에 다시 돌렸다).

| 무엇 | 결과 |
|---|---|
| `git merge-tree --write-tree` | 종료코드 0 · `Auto-merging litdb/figures/_sources.json` 한 줄 · CONFLICT 0 |
| `litdb/figures/_sources.json` (병합본) | `json.load` OK · 최상위 dict 키 349 |
| `tools/db/validate_canonical.py` | ✅ 배선된 항목 전부 원자료와 일치 · 거버넌스 결정 **118** · 그래프 무결성 ✅ |
| `tools/kb_wiki.py lint` | RESULT: 0 errors |
| `tools/convention_check.py` | 0 위반 |
| `tools/litdb/build_index.py --check` | digest 378편 · **어느 인덱스에도 없는 것 0편** · DFT 비교 201/201 · 표 칸 수 0건 (떠 있는 표 행 ⚠ · DEM 비교 미편입 89편은 대피 전부터 — §6) |
| 웹앱 전체 `pytest webapp/tests` | **637 passed · 2 skipped · 0 failed** (6 분 26 초) |
| 다섯 화면 (테스트 클라이언트) | `/weekly` · `/li2s` · `/cascade/rebuild` · `/adhesion` · `/log` 전부 200 · `/weekly` 머리 = 주간 정리 2026-09-28 ~ 10-04 |
| `tools/wad/agc_graphite.py --selftest` | 71 통과 · 0 실패 (k9 넷 판독 배선 = 실제 2단계 원자료 · 깨기 도구 8/8 · 러너 2/2) |
| `run_quench_kgy.sh` (SELFTEST=1 · PY=python3) | selftest PASS (0 실패) — 27 (공존 14) |
| `run_cascade_v7_probe.py` · `judge_eprime.py` · `glass_v2_readout.py` · `collect_neb.py` · `cc_graphite.py` `--selftest` | 전부 PASS (cc_graphite 53/53) |

## 4. 원격에 지금 도는 것 (마지막 실측: kgy 10-05 22:49 · gabia 10-05 20:50 KST — 사용자 watch)

| 기계 | 무엇 (트랙) | 식별 | 다음 |
|---|---|---|---|
| kgy | **cascade v7 탐침** (cascade · 사용자) | tmux `cv7probe` · worktree `~/wt_cv7probe_1003` @`a2924895` | 판독기가 다음 런을 고른다 · T* 또는 사다리 소진에서 멈춤 · 감시 `tools/doping/watch_cv7probe.py --loop` |
| kgy | **li2s 대조 계 B 담금질** seed1 → seed2 (⛔ 외부 1저자) | tmux `li3ps4q` · worktree `~/wt_li3ps4_1005` @`c704348b` | seed1 quench 50,000/450,000 (22:49 · 414 분) · seed3 자리 표시에서 **종료 코드 3 = 설계** |
| kgy | **P1b (b) k9 넷** 8 잡 (W_ad · 사용자) | tmux `agck9` · worktree `~/wt_agck9_1005` @`6adf297c` · 단계 시작 22:48:11 | 첫 잡 k 점 41 ✓ · 끝 어림 10-06 오후 · 상한 벽시계 30 h (다음 잡을 안 띄움) |
| gabia | **탄성 modelc_2x** (우리 DFT · 사용자) | tmux `el_mc2x_1001` | strain_13_m 진행 (20:50 out 갱신 · pw.x 41,374 MiB) |
| gabia | **li2s 대조 계 B 담금질** seed3 → 4 → 5 (⛔ 외부 1저자) | tmux `li3ps4g` · worktree `/data/work/wt_li3ps4_1005` @`17aced0b` · 공존 예외 (5) | seed3 20:48:40 시작 · 한 번에 하나 · 가드 ①–④ 가 우리 담금질만 죽이고 예외를 닫는다 |
| 외주 | **점착 V5 VASP** 16 잡 (사용자) | 건엽 씨 | 사용자가 지시 메시지를 보냈는지는 이 세션이 모른다 |

- 감시: kgy `~/w_kgy_1005.sh` (P1b k9 넷 · li2s · GPU) · gabia `/root/w_li3ps4_g.sh`.
- ⛔ 위 러너 worktree 는 **끝날 때까지 지우거나 다른 커밋으로 옮기지 않는다** (bash 는 스크립트를 조금씩 읽는다).
  쉬는 worktree (kgy `~/wt_agck12_1005` · `~/wt_agc_1002`) 는 정리해도 된다.
- ⚠ **병합 뒤 원격 회수 블록은 friendly 로 보낸다.** 형식은 그대로다 (대피 중 `365a53ae` 를 만든 블록):
  `git -C ~/lldvar fetch origin claude/friendly-meitner-lldvar` → 임시 worktree (`FETCH_HEAD`) → 원자료 `rsync` (tmp 제외) · `SHA256SUMS` → commit →
  `git push origin HEAD:claude/friendly-meitner-lldvar` → 임시 worktree 제거. **evac 로 보내지 않는다.**

## 5. 원장에 새로 생긴 것 · 바뀐 것

- **결정 107 → 118** — 새 11 건 (전부 active):
  - cascade: `D-2026-10-03-cascade-v7-amend-cp`
  - li2s: `D-2026-10-04-lpscl-smallcell-glass-md-v2-amend-co` · `D-2026-10-05-lpscl-smallcell-glass-md-v2-closed` · `D-2026-10-05-lpscl-smallcell-glass-control-li3ps4` · `D-2026-10-05-lpscl-smallcell-glass-control-cost`
  - gabia 운용: `D-2026-10-05-gabia-uma-coexist-elastic-li2s-control` (예외 (5))
  - 상시 규칙: `D-2026-10-05-md-observation-window` · `D-2026-10-05-adsorption-site-coordination`
  - 점착 P1b: `D-2026-10-05-wad-agc-kprobe12` · `D-2026-10-05-wad-agc-graphite-closed` · `D-2026-10-05-wad-agc-graphite-k9-registry`
- **상태가 바뀐 결정 3 건**:
  - `D-2026-09-30-lpscl-smallcell-glass-md-v2` proposed → active
  - `D-2026-10-01-cascade-v7-probe-card` proposed → active
  - `D-2026-09-30-gabia-uma-coexist-elastic-li2s-v2` active → **superseded** — 소멸한 예외 (4). 예외 (5) 가 supersede 했다.
    처음 비준 커밋 `7a475e4d` 는 slot 겹침으로 검증 실패 상태로 올라갔고, `17aced0b` 에서 고쳤다.
- **점착 기록**:
  - P1b: `db/properties/wad_agc_graphite_result_2026_10_05.json` (결과 기록 · `b_k9_넷_2026_10_05` 진행 중) · `db/properties/wad_agc_graphite_closed_2026_10_05.json` (마감 카드 · 봉인)
  - 원자료: `db/raw/wad_agc_graphite_2026_10_02/` (SHA256SUMS 222) · 묶음: `db/inputs/wad_agc_graphite_2026_10_02/{kprobe12,k9set}`
  - V5 VASP: `db/raw/wad_aprime_v5_vasp_2026_09_27/pilot_return_2026_10_05/` · `pp_registry_2026_10_05.json` (sha `a279d529…`)
  - 원장 로그: `db/pipelines/adhesion_pipeline.json` (log 끝에 덧붙인 줄 · W 값 없음)
- **li2s 기록**:
  - v2: `lpscl_smallcell_glass_md_v2_*` (개정 CO · 판독 · 마감)
  - 대조 계: `lpscl_smallcell_glass_control_li3ps4_*` (카드 · 개정 CS) · `lpscl_glass_control_li3ps4_runlog_2026_10_05.json` (발사 · 비용 오류 · 기계 배정 · kgy 동시 잡 구간)
  - 리뷰: `kb/reviews/li2s1a_{CO,CQ,CR,CS}_*` (원문) · `INDEX.md`
  - 템플릿: `kb/templates/estimand_card.md` §4-c (비용 견적은 같은 캠페인의 실측 장부와 대조)
- **cascade 기록**: `kb/reviews/codex_CP_*` · v7 카드·개정 · `judge_eprime.protocol_binding_errors` (온도 일곱 곳 결속)
- **도구** (새 것 또는 고친 것):
  - `tools/wad/agc_graphite.py` (`--kprobe_*` · `--k9set_*` · `_k_swap`)
  - `tools/doping/run_cascade_v7_probe.py` · `tools/doping/watch_cv7probe.py` · `tools/doping/judge_eprime.py`
  - `tools/ionic/glass_v2_readout.py` · `tools/sei/collect_neb.py` (`observation_window`)
  - 러너: `db/inputs/lpscl_glass_control_li3ps4_2026_10_05/run_quench_kgy.sh` · `db/inputs/wad_agc_graphite_2026_10_02/run_kgy.sh`
  - 그림·슬라이드: `tools/figures/fig_weekly_2026_10_04.py` · `tools/figures/slide_wad_w_table_2026_10_05.js`
- **화면**: `/weekly` (주간 정리 09-28~10-04) · `/li2s` (v2 잠정) · cascade 재건 §17–19 · 점착 P1b 로그 · `webapp/app.py` (`/log` 빈 구간 주석 · 6 줄) · `webapp/tests/test_li2s.py` (+53 줄).
- **CLAUDE.md**:
  - gabia 절: 예외 (5) 줄 · 예외 (4) 소멸 기록
  - 데이터 규율: 상시 규칙 둘 (관측창 · 배위수)
- **kb/open_items.md**: ⏭-NOW-z6 (대피 세션 블록 + ⏩ 덧붙임) · ⏭-NOW-z7 (마감) · 머리 줄 (굵게 한 겹).
- **litdb** (SE 축 · 우리 쪽):
  - 신간 7편 — wu2026 · nosrati2026 · sun2026 · cao2026 · qi2025 · yuan2026 · kim2026
  - `litdb/INDEX.md` · `litdb/comparison_vs_ours.md` · `litdb/figures/_sources.json`
  - DEM 쪽 파일 (`INDEX_DEM.md` · `comparison_vs_ours_DEM.md` · DEM 카드) 은 안 건드렸다.

## 6. 알려진 것 — 머지 전에 알 것

- ⚠ **`/governance` 에 점착 W 값이 결정 문장으로 뜬다.** 결정 화면이 제목·문장을 그대로 보여 준다.
  (이 카드는 `/kb?path=…` 로 화면에 렌더되므로 숫자를 옮겨 적지 않는다 — 위치만 적는다.)
  - 대피 전부터 있던 것: `D-2026-09-26-wad-aprime-v2-report` · `D-2026-09-30-wad-cc-dem-input-both-scenarios` · SE|SE 경보 결정 둘의 문헌값.
  - 대피 세션이 하나 더했다: `D-2026-10-05-wad-agc-graphite-closed` 의 제목·문장에 P1b 헤드라인 숫자를 적었다. 대피 세션의 실수다.
  - 비준된 결정은 본문을 고칠 수 없다 (지문). 화면에서 가릴지는 **사용자 결정**이다 — 복귀 뒤 webapp 반영 때 정한다.
  - 앞으로 결정 제목·문장에는 W 값을 쓰지 않는다. 값은 결과 기록·마감 카드 경로로만 가리킨다.
- ⚠ `/adhesion` 에도 같은 질문이 걸린 줄이 둘 있다. 둘 다 대피 전부터 있었다.
  - V2 2체 교차 (QE 대 s-dftd3) 줄 — 커밋 `66a320e0`.
  - UMA+D3 미리보기 줄 (`wad_aprime_s4_uma_env_xcheck_2026_09_26.json` 인용).
- `litdb/INDEX_DEM.md` — 병합본에서 생성기를 다시 돌리면 **날짜 줄과 DEM 논문 5편의 그림 수만** 바뀐다.
  - friendly 안에서 이미 낡아 있던 것이라 병합 때문이 아니다. DEM 세션 영역이다.
  - ⇒ 병합 커밋에 섞지 않는다. 할 거면 따로 커밋한다.
- `build_index.py --check` 의 경고 둘은 대피 전부터 있던 상태다. 이번 병합과 무관하다.
  - 떠 있는 표 행: INDEX.md 96 · comparison_vs_ours.md 66 · comparison_vs_ours_DEM.md 148.
  - DEM 비교문서 미편입 89편.
- li2s 대조 계 kgy 장부 (등분) 의 단서:
  - cascade v7 탐침이 런 사이에 쉬는 빈 구간은 kgy 에서 안 보인다.
  - 그런 구간이 있으면 등분이 우리 몫을 **과소평가**한다 (보수 방향이 아님). 시드 끝 장부에서 cv7 런 기록과 맞춘다.
- CLAUDE.md Git 절은 'friendly 에만 커밋' 이다. 대피 세션은 대피 프롬프트에 따라 evac 에 커밋했다 — **병합 뒤에는 다시 friendly 규칙**이다.

## 7. 머지 뒤 friendly 에서 이어서 할 것 (순서)

1. **사용자 로컬 갱신 안내** — `git switch claude/friendly-meitner-lldvar && git pull --ff-only`.
   - 그다음 웹앱 서버를 재시작한다 (`app.py` 가 바뀌었다).
   - 다섯 화면을 같이 본다 — /weekly · /li2s · /cascade/rebuild · /adhesion · /log.
2. **P1b (b) k9 넷** (kgy · 끝 어림 10-06 오후):
   - 회수 → **friendly 로** push.
   - `--k9set_collect` 로 레포 재집계 → kgy 집계와 같은지 본다.
   - 판독 REPLACE 면 새 마감 결정을 쓴다 (`D-2026-10-05-wad-agc-graphite-closed` 를 supersede · 같은 slot). KEEP_A_PRIME 이면 (a′) 그대로.
   - DEM 회신을 낸다. 회신 9 초안에 붙일지 따로 낼지 사용자에게 묻는다.
   - W 값은 결과 기록·마감 카드에만.
3. **li2s 대조 계** (⛔ 외부 1저자 · 사용자는 실행 승인만):
   - 시드 진행: kgy seed1·2 · gabia seed3·4·5.
   - 회수 → 시드 게이트 · 밀도 · T₅₀ · 장부 (kgy 등분 · gabia pmon · 벽시계 병기).
   - 600 K MD 러너 (B) · 판독 대조 모드 (600 K 결과 전에 넣는다).
   - 다음 편지: 기계 배정 변경 · gabia 점유 표본 정의.
4. **cascade v7 탐침** — 감시 · T* 또는 사다리 소진 → 카드대로.
5. **탄성 modelc_2x** — 남은 strain → fit.
6. **V5 VASP** — 최종 반송 → `--collect --pp_registry db/raw/wad_aprime_v5_vasp_2026_09_27/pp_registry_2026_10_05.json --pp_registry_sha256 a279d529… --uma uma.json` → G5.
7. **webapp 반영** (사용자 '나중에') — 대피 세션 일을 화면에 올린다. §6 의 W 값 질문을 사용자에게 묻는다.
8. 그 밖은 `kb/open_items.md` ⏭ 절.

## 8. 이 문서가 못 하는 것

- 시험 결과는 **10-05 밤 가상 병합본** 기준이다. origin 세션이 들이기 직전에 다시 센다 — friendly 가 그사이 움직였을 수 있다 (DEM 세션).
- 원격 상태는 사용자가 붙여 준 마지막 watch 다 (kgy 22:49 · gabia 20:50). 그 뒤 변화는 모른다.
- V5 VASP 외주 지시를 보냈는지 모른다.
