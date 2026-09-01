---
title: "회신 AW — 웹앱 전수 감사: NO-GO (P0 4건 · P1 6건 · 해제조건 6)"
date: 2026-09-01
updated: 2026-09-01
tags: [review, codex, reply, webapp, governance, sdcp, citation-gate]
status: 회신 수령 — 이행 중
kind: review-reply
system: repo
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-01
verifiedBy: "리뷰어가 clean LF checkout 에서 실화면 대조 + P0 별도 주입으로 재현"
explored: false
authoredBy: external
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 회신 AW — NO-GO

> 요청: `kb/reviews/codex_AW_prompt_webapp_audit_2026_09_01.md`
> 대상 커밋: `fa506bc3` · `7ba9fbe4` · `0b7c858c`

## ⛔ 가장 무거운 한 줄

> **“clean LF checkout 에서 웹앱 시험은 `139 passed, 2 skipped` 로 통과했고 canonical
> selftest 도 PASS 였습니다. 즉 기존 시험이 실패해서 내린 NO-GO 가 아닙니다.
> 시험이 모두 통과하는 상태에서 위 P0 들을 별도 주입·실화면 대조로 재현했습니다.”**

우리 시험 140건이 전부 초록인 채로 이 구멍들이 있었다. 감사에서 라우트 200 스모크와
마커 grep 은 했지만 **실화면 대조를 하지 않았다** — 그것이 이번 실패의 방법론적 원인이다.

## P0

### P0-1 `/sdcp` 가 정본의 인용 금지를 우회한다

- `webapp/data.py` `sdcp_wave1_rows()` 가 raw 결과에서 **basin 일치만으로** `valid` 를 만든다.
- `webapp/templates/doc.html` 이 교정 배너보다 **먼저** 모든 ΔE·E_ads·doped 값을 현재형으로 노출한다.
  실측: doped 4잡의 이름과 E_ads 가 전부 보이고, *“Li 자리를 좋아한다”*·
  *“더 음수일수록 세게 붙는다”*·*“초기조건과 무관하게 재현”* 도 그대로 출력된다.
- **더 나쁜 점**: `webapp/tests/test_sdcp_wave1.py` 가 raw E_ads **전건 노출을 회귀시험으로
  강제**한다. `sdcp_wave1_citable.json` 의 절대 E_ads HOLD · neutral NO_VERDICT ·
  doped 전항 비인용과 정면충돌한다.

### P0-2 감사에서 놓친 현재-facing 표면들이 철회 주장을 되살린다

| 표면 | 무엇 |
|---|---|
| `/todo` | `kb/open_items.md` 의 철회된 `O···Li 2.09 Å` · 추출 부호 |
| `/log` | `log.html` 의 “50 meV · 2-seed 0.1 meV”, 정정 없는 `journal.jsonl` 항목, 무상태 handoff 노출(`app.py`) |
| `/compare` | 철회·보류 Ea 표, superseded β 게이트, “벌크 NEB 경로 정의 불가” 서술 |
| `/glossary` | b2o3 `0.199` · LPSOCl 대비 |

> 역사를 삭제할 필요는 없지만, **각 주장 바로 옆에** `HISTORICAL/BLOCKED/SUPERSEDED` 를
> 붙여야 한다. **상단 배너 하나로는 부족하다.**

### P0-3 소급 노드 등록은 가능하지만 현재 supersession 은 정당하지 않다

C-12 노드는 아직 `proposed` 인데 **전역 closure policy** 를 이미 `superseded` 로 만들고,
자신도 SDCP 한정인지 전면 폐지인지 미정이라고 자인한다. 반면 `CLAUDE.md` 는 같은 마감
규율을 현행으로 둔다.

> **Q1 판정: 소급 `proposed` 노드 등록은 허용, proposed successor 가 전역 policy 를
> 폐기한 간선은 불허.** 전역 policy 간선을 제거하고 범위·비준을 별도 결정으로 닫을 것.

### P0-4 승인 검사기에 다른 fail-open 이 남았다

- `canonical.py` 가 상태 **필드 존재만** 보고 허용 어휘·타입을 검사하지 않는다 —
  `decision_state:"actve"` 와 `null` 을 넣으면 위반 0건.
- `decisions()` · `assessments()` · `artifacts()` 가 **중복 ID 를 dict 변환 중 조용히 덮는다.**
  무승인 active 뒤에 같은 ID 의 proposed 를 두면 validator 는 active 기록을 잃고 통과한다.
- canonical entry 도 index/map 에서 같은 `(metric, system)` 을 마지막 값으로 덮고
  `validate()` 가 문제를 내지 않는다.

## P1

- **Q2 화면 파생 — 현재 형태로는 불허.** `_derived` 표시가 `data.py` 에만 있고 템플릿이
  숨긴다. 실제 API 에는 `force_model` 이 없는데 `/benchmarks` 에는 `a=0.1017` 이
  정본값처럼 나온다. 선형 floor 와 zero-floor power law 의 R² 가 0.9862/0.9877 로
  구분되지 않으므로 **“평형 PES 불일치” 는 과한 기전 해석**이다. JSON 재생성 전에는
  fit 절을 접거나 `screen-derived/model-dependent` 로 명시할 것.
- `committee_sweep_verdict.py` 가 signed drift 의 `max` 를 써서 `−30%, −5%` 를 `−5%` 로
  통과시킨다 → `max(abs(...))` 필요. 기준 600 K 부재 시 최저 T 로 **조용히 대체**하는 경로도 중단.
- **Q5 건수·어휘 시험만으로 부족.** hazard 시험이 헤더의 `25건` 만 확인해 **tbody 가 0행이어도
  통과**한다. 각 hazard 의 안정 ID 와 `(file, level, what, why, fix)` 를 화면과 대조할 것.
- “라우트 전수 200” 시험이 **동적 라우트를 전부 제외**한다. 실제 GET 42개 패턴 중 14개가 빠지며
  `/api/property/<name>` 과 화면 파생의 차이도 놓친다.
- **Q7 판정: 별칭은 일회성 이관 뒤 거부하는 편이 맞다.** status-only polaron 두 건은 화면에서
  상태가 **공백**이고, 미비준인데도 *digest 없음 = 일치* 로 처리돼 초록 `🔒 일치` 가 뜬다.
  **`미비준 / 결속 일치 / 결속 불일치` 3상태**로 나눌 것.
- **Q4 판정: 새 대시보드 카드는 조건부 허용.** “VASP 0잡·재생성 대기” 가 있어 결과 주장으로
  읽히진 않는다. 다만 **`n=1 wave1 표면흡착 마감`** 이라고 범위를 명시해 n=6 polaron/reopen
  캠페인과 분리할 것.

## 해제조건

1. `/sdcp` 를 citable·closure·hazard 상태에서 **파생**하고, raw 표는 접힌 역사 절에서
   행별 `citable:no` 로만 노출.
2. `/todo`·`/log`·handoff API·`/compare`·`/glossary` 의 철회 주장에 현행 상태를 **직접 결속**.
3. C-12 → 전역 closure-policy supersedes 간선 제거; 범위 결정과 비준을 별도로 완료.
4. 상태 enum/type, 중복 decision/assessment/artifact ID, 중복 canonical `(metric,system)` 을
   **fail-closed** 로 봉인.
5. 파생 fit 출처 표시·모형 의존성 명시 및 signed-drift/base-T **음성시험** 추가.
6. hazard 전행·전필드 대조와 **동적 라우트 대표 fixture** 를 회귀시험에 추가.

## 이행 기록

| | 상태 |
|---|---|
| P0-1 (1/3) 데이터 계층 — 지위를 정본에서 파생 (`_wave1_gate`·`_wave1_status`) | ✅ `1e5f3f0` 계열 |
| P0-1 (2/3) 화면 · (3/3) 시험 | ⏳ |
| P0-2 다섯 표면 상태 결속 | ⏳ |
| P0-3 거버넌스 간선 제거 | ⏳ |
| P0-4 fail-closed 봉인 | ⏳ |
| P1 6건 | ⏳ |

재제출 라벨은 **AY** 다 (AX 는 LPSOCl 600 K 개정에 이미 나가 있다).
