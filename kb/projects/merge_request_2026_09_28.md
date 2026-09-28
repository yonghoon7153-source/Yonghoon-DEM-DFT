---
title: "머지 요청 (초안) — 대피 브랜치 claude/evac-2026-09-28 → claude/friendly-meitner-lldvar"
date: 2026-09-28
updated: 2026-09-28
tags: [merge, evacuation, handoff, li2s, cei, gabia, cascade]
status: 초안 — 사용자가 "돌아가자" 할 때 커밋 목록·시험을 다시 찍어 최종화한다
confidence: medium
verificationStatus: verified
verifiedAt: 2026-09-28
verifiedBy: self
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: multi-source-primary
---

# 머지 요청 (초안) — `claude/evac-2026-09-28` → `claude/friendly-meitner-lldvar`

> 대피 인계 카드 `kb/projects/handoff_2026_09_28_evacuation.md` §5 의 절차를 따른다.
> **이 문서 하나로 머지 판단이 되게** 쓴다 — 커밋 · 시험 · 원격 상태 · 원장 변화 · 알려진 빨간불 · 다음 일.

## 0. 한눈에

- **fast-forward 가능** (09-28 14시 확인 — friendly 에 새 커밋 **0** · 이 브랜치가 **19 커밋 앞** · 기록 커밋 포함 시 20).
- 이 브랜치가 만든 **새 빨간불은 없다.** 웹앱 시험 3 건 빨강은 **09-22 부터** 이어진 cascade 매니페스트 건 (⏭-NOW-w 🔴 · §6).
- 원격 계산 셋이 돌고 있다 (§4) — 머지와 무관하게 계속 돈다.

## 1. 병합 방법

1. 사용자 허락을 받는다.
2. friendly 가 그사이 움직였는지 다시 본다: `git fetch origin claude/friendly-meitner-lldvar` → `git rev-list --count HEAD..origin/claude/friendly-meitner-lldvar` 가 **0** 이면
3. `git push origin HEAD:claude/friendly-meitner-lldvar` (**강제 없이** — fast-forward 만).
4. 움직였으면 멈추고 rebase / merge 를 사용자에게 묻는다.
5. 로컬 웹앱(127.0.0.1:5001)은 로컬 체크아웃을 읽는다 — 머지 뒤 로컬에서 `git pull` 해야 화면이 바뀐다.

## 2. 커밋 (09-28 14시 · `git log --oneline origin/claude/friendly-meitner-lldvar..HEAD`)

| 커밋 | 무엇 |
|---|---|
| `3c7e2f60d` · `8756d27ab` | 브리핑 그림 둘 (점착 W_ad · 판별종 갭 10/10) |
| `3b1f9b57b` | li2s 회신 CH 원문 보존 |
| `3d09b0990` | 회신 CH 반영 — **600 K 편입 규칙 사전등록** · 2σ 경계 · digest 오기 |
| `b81d08eb6` · `a8a4724c3` · `d41477e8b` | S54 내력 (`--trace_S`) · 전건 해소 · PS₄ 보존율 ≠ 정체 |
| `9bd894631` · `06b454c35` · `73f11d80b` · `57b6304b2` | `--s_census` · 교환망 · 정체 온전율 (직산 확인) |
| `5c08a5ff2` · `31d6c5546` | 600 K 파일럿 발사 · ⛔ 초기구조 오류(원시) → relax 재발사 |
| `ccde59e15` | 회신 CL 초안 · CH 회신 수령 표시 · 본 런 지연 원인 |
| `b2be24d3a` | gabia 범위 한정 예외 (2) — 465 K seed3·seed4 ↔ V4 공존 3,500 MiB · CLAUDE.md |
| `11e0c0309` | 465 K 가드 러너 가동 (wait 모드 — V4 시작 문턱 2048) |
| `8a8407e9f` | 회신 CL (부분) — 465 K '2 배' 확정 (착수 전 커밋) · 두 문턱 해석 확정 |
| `3719b638b` | 다섯 시드 전수 — 정체 온전 P 12·12·9·5·5 |
| `948afa9b0` | CEI §0 정정 — 환원 쪽은 안 움직인다 (1.717 V 공통) · 결론 단락 셋 |

## 3. 돌린 시험 · 검증 (09-28)

| 무엇 | 결과 |
|---|---|
| `tools/db/validate_canonical.py` | ✅ 배선된 항목 전부 원자료와 일치 |
| `tools/convention_check.py` | 0 위반 |
| `tools/kb_wiki.py lint` | 0 errors |
| 웹앱 전체 `pytest webapp/tests` | **585 passed · 3 failed · 2 skipped** — 3 failed 는 §6 (이 브랜치 변경을 뺀 HEAD 에서도 같은 3 건 확인) |
| `test_interpretation_cards.py` | 70/70 (§0 시험 둘 뒤집기 + 신규 1 · 일부러 깨서 빨간불 셋 확인) |
| hazard 시험 (`-k hazard`) | 13/13 |
| `quench_ss_event.py --selftest` | 35/35 (깨서 빨간불 6 건 확인) |
| `msd_diffusive_check.py --selftest` | 200 ok · 0 bad |

## 4. 원격에 아직 도는 것 (마지막 실측)

| 기계 | 무엇 | 식별 | 예상 |
|---|---|---|---|
| kgy | li2s **600 K 파일럿** (relax 초기구조 · 400 ps) | tmux `gp600` · PID 3367458 · 11:57 재발사 | 09-28 저녁 |
| kgy | cascade v6 E′ 40 런 | 마스터 PID 372656 · 28 끝 · 13 남음 · 164 / 320 GPU-h | 실측 기준 ~3 일 |
| gabia | W_ad **V4** 9 잡 | tmux `v4main` · 러너 PID 439244 · 6 끝 · 7 번째 G4_k1_far | 09-28 19–20 시 |
| gabia | li2s **465 K 가드 러너** (seed3·seed4) | tmux `glass465b` · wait 모드 | V4 끝나면 자동 발사 → 새벽 끝 |

⚠ 중단한 원시 600 K 런의 산출은 `…/pilot600/T600_raw_aborted_20260928` 에 **보존**했다 (지우지 않는다).

## 5. 원장에 새로 생긴 것 · 바뀐 것

- **결정**: `D-2026-09-28-lpscl-smallcell-glass-amend-ch` (**proposed** — 외부 1저자 부분 확인 기록 · Q-CL-3·4 남음) · `D-2026-09-28-gabia-uma-coexist-v4-li2s465` (**active** · 비준 도장 · 이번엔 조건 ④ 에 걸려 쓰이지 않았다).
- **db/properties 새 기록**: `lpscl_smallcell_glass_md_amendment_ch_2026_09_28.json` (개정 v3) · `lpscl_smallcell_glass_amendment_digest_erratum_2026_09_28.json` · `lpscl_smallcell_glass_s54_history_2026_09_28.json` · `db/raw/lpscl_smallcell_glass_cc_2026_09_26/census_5seeds_2026_09_28.json`.
- **바뀐 원장**: `citation_hazards.json` (`HZ-esw-reduction-limit-label` 에 화면 정정 메모) · `cei_figs/index.html` §0.
- **리뷰**: `li2s1a_CH_reply_…` (원문) · `li2s1a_CL_prompt_…` (초안 · 발송됨) · `li2s1a_CL_reply_…` (부분 · 원문).
- **도구**: `tools/ionic/quench_ss_event.py` (`--trace_S` · `--s_census` · `identity`) · `tools/ionic/msd_diffusive_check.py` (2σ 경계 규칙).
- **CLAUDE.md**: gabia 절 — "지금 예외는 없다" → 살아 있는 범위 한정 예외 1 건 + 방 계산 근거 (V4 자폭선 44,000 기준 4,762 MiB).
- **kb/open_items.md**: ⏭-NOW-z 추가 · 결속 시험 수 62 → 70.

## 6. 알려진 빨간불 — 머지 전에 알 것

- 🔴 `test_webapp.py` 셋 (`test_cascade_headline_comes_from_the_manifest` · `test_manifest_tamper_fails_closed` · `test_audit_figures_are_the_only_default_figures`) — **09-22 부터**. 원인: 커밋 `8a0e202d3` (ESW 환원한계 라벨 수정)이 파일 넷을 바꾸고 cascade 감사 매니페스트를 다시 안 만들었다 → cascade 화면 fail-closed (정상 경보). 이미 ⏭-NOW-w 🔴 (09-23) 에 기록된 건이다.
- ⛔ 해시만 다시 박지 않는다 — 순서: 풀 입력 (`rebuild_pool_inputs.py`) → `build_screening_funnel.py` → 감사 그림 → `build_cascade_audit_manifest.py`. **퍼널 통과 목록이 바뀔 수 있다** (ESW 트랙 = 1저자 = 사용자 결정).
- ✅ **1저자 09-28: cascade v6 가 끝난 뒤 한 번에 한다** (v6 결과도 같은 풀 입력으로 들어가야 해서 지금 돌리면 두 번 돈다).
- ⚠ CLAUDE.md Git 절은 "friendly 에만 커밋" 이다 — 이 세션은 대피 프롬프트에 따라 evac 브랜치에 커밋했다. 머지 뒤에는 다시 friendly 규칙이다.

## 7. 머지 뒤 friendly 에서 이어서 할 것

1. **오늘 저녁** — 600 K 결과 판독 (C1 · C2 2σ · 5 ps lag p90 MSD 의 48.88 Å² 초과분 기록 → 편입 여부는 C1·C2 로만) · V4 끝 → `collect_aprime_s4.py --v4` 집계 (+ATM 열) · 465 K 두 시드 발사 확인.
2. **새벽** — 465 K 조기확인 (seed3 · seed4 D(2–50) 비 · 문턱 2 배 · 단서 "출처는 400 K 두 런, 초기구조가 섞여 있다 — 두 런은 난수까지 같았다").
3. **li2s 다음 편지 (CM)** — 600 K · 465 K 조기확인 · 다섯 시드 전수 · "두 400 K 런의 난수가 같았다(401)" 사실 보고 · Q-CL-3·4 판정 요청 (트랙 = 외부 1저자).
4. **CEI 같이 읽기** — §2 부터 (§0 은 끝).
5. **cascade v6 끝** → §6 순서로 매니페스트 재생성 (퍼널 목록 변화 확인 → 1저자).
6. (제안) ESW 산화 onset 을 canonical_registry 에 올릴지 — §0 표의 claim `cei.esw.nd_narrows_window` 가 원장 어디에도 없어 결속이 헛돈다 (위험 원장: "레지스트리 등록이 결속의 선결조건").

## 8. 이 문서가 못 하는 것

- 커밋 목록·시험 결과는 **09-28 14시 기준**이다 — "돌아가자" 때 다시 찍는다.
- 원격 상태는 사용자가 붙여 준 watch 의 마지막 실측이다 — 그 뒤 변화는 모른다.
