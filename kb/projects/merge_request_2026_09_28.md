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

- ⚠⚠ **1저자 요청 (09-28 · "이거 나중에 꼭 얘기해줘야돼")** — 사용자 **로컬 체크아웃이 지금 `claude/evac-2026-09-28` 에 있다** (09-28 14시 로컬 웹앱에서 §0 정정을 보려고 옮겼다). friendly 에 fast-forward 한 **직후 반드시** 사용자에게 로컬을 되돌리라고 말한다: `git switch claude/friendly-meitner-lldvar && git pull --ff-only` (로컬 웹앱 127.0.0.1:5001 은 로컬 체크아웃을 읽는다). 말하지 않으면 사용자 로컬이 evac 에 남아, 그 뒤 friendly 에 쌓이는 것이 로컬 화면에 안 보인다.
- **fast-forward 가능** (09-28 14시 확인 — friendly 에 새 커밋 **0** · 이 브랜치가 **19 커밋 앞** · 기록 커밋 포함 시 20). ⚠ 오후·저녁에 커밋이 더 붙었다(§2 아래 · 09-28 저녁 실측 **29 커밋 앞 · friendly 새 커밋 0**) — "돌아가자" 때 다시 센다.
- ⭐ **CEI 화면이 Nd x = 0.02 로 바뀌었다** (1저자 결정 · 09-28 오후) — 머지 뒤 friendly 의 로컬 웹앱에서 같은 주소로 보인다.
- 이 브랜치가 만든 **새 빨간불은 없다.** 웹앱 시험 3 건 빨강은 **09-22 부터** 이어진 cascade 매니페스트 건 (⏭-NOW-w 🔴 · §6).
- 원격 계산 셋이 돌고 있다 (§4) — 머지와 무관하게 계속 돈다.

## 1. 병합 방법

1. 사용자 허락을 받는다.
2. friendly 가 그사이 움직였는지 다시 본다: `git fetch origin claude/friendly-meitner-lldvar` → `git rev-list --count HEAD..origin/claude/friendly-meitner-lldvar` 가 **0** 이면
3. `git push origin HEAD:claude/friendly-meitner-lldvar` (**강제 없이** — fast-forward 만).
4. 움직였으면 멈추고 rebase / merge 를 사용자에게 묻는다.
5. ⚠⚠ **1저자 요청 (09-28 · "이거 나중에 꼭 얘기해줘야돼")** — 사용자 **로컬 체크아웃이 지금 `claude/evac-2026-09-28` 에 있다** (09-28 14시 로컬 웹앱에서 §0 정정을 보려고 옮겼다). friendly 에 fast-forward 한 **직후 반드시** 사용자에게 로컬을 되돌리라고 말한다: `git switch claude/friendly-meitner-lldvar && git pull --ff-only` (로컬 웹앱 127.0.0.1:5001 은 로컬 체크아웃을 읽는다). 말하지 않으면 사용자 로컬이 evac 에 남아, 그 뒤 friendly 에 쌓이는 것이 로컬 화면에 안 보인다.

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
| `349ecfa90` | **CEI x = 0.02 전환 — 사전등록(3차 개정 · 게이트 G0–G5) + 결정 + 판정 코드 (실행 전 커밋)** |
| `0de54a1fd` | 그림 생성기 x = 0.02 계열 (기본 x = 0.20 출력 바이트 동일) · ⑧ 뒤집힌 문장 정정 |
| `4e51aba3a` | (사용자 · gabia) x = 0.02 재계산 원자료 — 계면 16 조성 · ESW 9 · 도펀트 7 × 열린/닫힌 · 판정 |
| `ad3456f64` | 결과 기록 · 화면 전면 개정 · 그림 `_x002` · 시험 +6 · kb 카드 반론 동기화 · G4 진단 열 |
| `a8177e205` | **CEI G4 닫음** — 1저자 "ㅇㅇ 그렇게 해줘" · 결정 `D-2026-09-28-cei-x002-result` (active · 비준) · 결과 기록 ratified · 화면 두 곳 · 결속 시험 +1 |
| `d2870ca0f` · `d68fb1047` | li2s 발표 덱용 그림 8 장 + 생성기(`--selftest`) + CSV — 덱 자체는 아티팩트(65foANsmpCVCaVG4zHEmuM · 비공개) |
| `f1780002d` | 웹앱 `/li2s` 에 「처음 보는 분께」 절 — 요약 기록(자리표시) + `data.li2s_brief()` + 시험 9 |
| `767d10158` · `17640b9f2` | **CEI Li 장부 = 항등식** 유도·확인 (`--li_identity` · 계수 1) + **x = 0.10 곡률 사전등록 (실행 전 커밋)** · 결정 둘 (항등식 proposed · x010 active) · run.sh · 경로 정정 |
| `cf17c5542` | (사용자 · gabia) x = 0.10 곡률 원자료 — 7 조성 · 판정 G0/GI/GC 통과 |
| `ae0275cfc` | x = 0.10 결과 기록(proposed) · 사전등록 ratified · 화면 머리 2×2 곡률 문장 교체 + 결속 시험 · 도구 G0 키·칸별 목록 |
| `fc05bdf50` · (다음 커밋) | **W_ad 흑연 층간 C|C 사전등록 (실행 전)** — 덴카–덴카 · 덴카–VGCF · VGCF–VGCF · `tools/wad/cc_graphite.py` · 카드 · 결정 `D-2026-09-28-wad-cc-graphite` (active) · 입력 1단계 9 잡 + `run_v100.sh` · **litdb Wang 2015** (본문+SI · 그림) |

## 3. 돌린 시험 · 검증 (09-28)

| 무엇 | 결과 |
|---|---|
| `tools/db/validate_canonical.py` | ✅ 배선된 항목 전부 원자료와 일치 |
| `tools/convention_check.py` | 0 위반 |
| `tools/kb_wiki.py lint` | 0 errors |
| 웹앱 전체 `pytest webapp/tests` | **585 passed · 3 failed · 2 skipped** — 3 failed 는 §6 (이 브랜치 변경을 뺀 HEAD 에서도 같은 3 건 확인) · 09-28 오후 `ad3456f64` 에서 **591 passed · 같은 3 failed · 2 skipped** · 09-28 저녁 WAD-CC + Wang digest 뒤 **602 passed · 같은 3 failed · 2 skipped** (digest 작성 도중에 돌린 판은 `test_recent_digests_are_on_every_litdb_surface` 가 INDEX 전이라 빨강 → INDEX·비교표 채운 뒤 초록) |
| `test_interpretation_cards.py` | **77/77** (§0 시험 둘 뒤집기 + 신규 1 · x = 0.02 결속 +6 — 화면을 일부러 깨서 빨간불 6/6 · G4 마감 결속 +1 — 화면·결과 기록·원장을 깨서 빨간불 5/5) |
| `interface_reactivity_v2.py --selftest` | **139 ✓** (x002 판정 16 건 · 항등식 13 · x010 7 — 일부러 깨서 빨간불: x002 6 건 · 항등식·x010 10/10) |
| 판정 재현 | gabia 판정 파일 = 로컬 재생성 (source 필드 제외 동일) |
| hazard 시험 (`-k hazard`) | 13/13 |
| `quench_ss_event.py --selftest` | 35/35 (깨서 빨간불 6 건 확인) |
| `msd_diffusive_check.py --selftest` | 200 ok · 0 bad |
| `cc_graphite.py --selftest` (09-28 저녁) | **52/52** — 일부러 깨기 20 가지 전부 빨강 (2성 식 · G4 문턱 · smearing 치환 · SP 기준 · 면내 제약 · P0 · 층간 깃발 · ABC · 허용대 · 두께 · 누락 None · 간격 8 Å · degauss · G3 all→any · INCOMPLETE · 빌더 적층 가드 · verify 디스크·좌표·항상통과 · ATM 부호) · 실제 V2 2단계 입력과 설정 20 키 동일 · 카드 code_binding 결속 |
| `build_aprime_interfaces` · `build_aprime_s3` · `collect_aprime_s4` selftest | 26/26 · 19/19 · 25/25 (C|C 가 import 만 한다 — 봉인 도구는 안 바꿨다) |
| `test_adhesion.py` · `validate_canonical.py` | 13/13 · 결정 91 · 그래프 무결성 ✅ |

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
- **도구**: `tools/ionic/quench_ss_event.py` (`--trace_S` · `--s_census` · `identity`) · `tools/ionic/msd_diffusive_check.py` (2σ 경계 규칙) ·
  `tools/oxidation/interface_reactivity_v2.py` (`--x002` · `--x002_esw` · 빠진 `import sys`) · `tools/figures/plot_cei_nd_o_decomposition.py` (`--series x002`) ·
  `tools/figures/plot_cei_p_host_ladder.py` (`--rec/--nd_bearing/--out`).
- **CEI x = 0.02 (09-28 오후)**: 결정 `D-2026-09-28-cei-page-x002` (active · 1저자) · 개정문 `cathode_cei_x002_amendment_2026_09_28.json` (ratified · 실행으로) ·
  결과 `cei_x002_result_2026_09_28.json` (**ratified** — G4 는 '위반 9 · 원인 규명(반올림)' 으로 닫음 · 결정 `D-2026-09-28-cei-x002-result` active · 1저자 "ㅇㅇ 그렇게 해줘") · 원자료 `cei_interface_V_x002` · `cei_esw_Li_x002` · `dopant_iface/closed_*_x002` ·
  `cei_p_host_ladder_x002_2026_09_28.json` · 그림 `cei_figs/*_x002.*` (옛 파일은 안 덮음) · kb 카드 `cei_nd_manuscript_framing_2026_09_18.md` 반론 절.
- **CEI Li 장부 항등식 · x = 0.10 (09-28 저녁)**: 기록 `cei_li_ledger_identity_2026_09_28.json` (유도 · 수치 확인 · β 분해 · 허용/금지 서술 **제안**) · 확인 산출 `cei_li_ledger_identity_check_{x002,0919}_2026_09_28.json` · 결정 `D-2026-09-28-cei-li-ledger-identity` (**proposed** · `amends` 09-19 결정 — 비준 전엔 화면 안 바꿈) · 09-19 두 기록에 포인터 키 `⭐_유도_2026_09_28` 만 · 사전등록 `cathode_cei_x010_curvature_prereg_2026_09_28.json` + 결정 `D-2026-09-28-cei-x010-curvature` (active · 1저자 "빨리 할 수 있는 부분이면 진행하자") · 도구 `interface_reactivity_v2.py` (`li_ledger_identity` · `li_ledger_beta_decomposition` · `--li_identity` · `--x010` · li_ledger_slope 설명만 정정).
- **W_ad 흑연 C|C (09-28 저녁)**: 결정 `D-2026-09-28-wad-cc-graphite` (**active** · 1저자 '이것도 진행하자' · 실행 전 비준 도장) · 카드 `wad_cc_graphite_prereg_2026_09_28.json` (ratified) · 도구 `tools/wad/cc_graphite.py` (새 파일 — 봉인 도구 무변경) · 입력 `db/inputs/wad_cc_graphite_2026_09_28/` · litdb `papers/wang2015_graphite_cleavage_energy.md` + `figures/wang2015_graphite_cleavage_energy/` · 09-23 계획 §흑연 대조에 인입 표시.
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
4. **CEI** — ~~① G4 처리 1저자 확인~~ ✅ 09-28 오후 닫음 ('위반 9 · 원인 규명(반올림)') · **x = 0.10 곡률 실행(gabia · `db/raw/cei_x010_2026_09_28/run.sh`) → 결과 기록 · 머리 2×2 '곡률' 문장 갱신** · **항등식 결정 비준 → 화면 교체(머리 2×2 · §1 상자 · 방법 상자 · §9) + 결속 시험** · 같이 읽기 §2 부터 (x = 0.02 판).
5. **cascade v6 끝** → §6 순서로 매니페스트 재생성 (퍼널 목록 변화 확인 → 1저자).
6. (제안) ESW 산화 onset 을 canonical_registry 에 올릴지 — §0 표의 claim `cei.esw.nd_narrows_window` 가 원장 어디에도 없어 결속이 헛돈다 (위험 원장: "레지스트리 등록이 결속의 선결조건").

## 8. 이 문서가 못 하는 것

- 커밋 목록·시험 결과는 **09-28 14시 기준**이다 — "돌아가자" 때 다시 찍는다.
- 원격 상태는 사용자가 붙여 준 watch 의 마지막 실측이다 — 그 뒤 변화는 모른다.
