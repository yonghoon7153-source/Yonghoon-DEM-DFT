---
title: "리뷰 요청 AW — DFT 웹앱 전수 감사 (실패 2건 수선 · 마감/철회 화면 반영 · 인용위험 원장 합류 · 승인 게이트 fail-open 봉인)"
date: 2026-09-01
updated: 2026-09-01
tags: [review, codex, webapp, governance, sdcp, prompt]
status: 회신 수령 — NO-GO · `kb/reviews/codex_AW_reply_webapp_audit_2026_09_01.md` · 이행 중
kind: review-request
system: repo
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 요청 AW — DFT 웹앱 전수 감사

> 대상 커밋 3개: `fa506bc3` (수선 1/2) · `7ba9fbe4` (수선 2/2) · `0b7c858c`
> (증빙 스크립트 + 승인 게이트 봉인), 브랜치
> `claude/friendly-meitner-lldvar`. C-12 리뷰 사슬(…AT→AU→AV)과는 **다른 스레드**입니다 —
> 이쪽은 번들이 아니라 **열람 화면**입니다.
> 배경 지도: `kb/results/branch_state_2026_08_31.md` (전수 조사) ·
> `kb/reviews/INDEX.md` (리뷰 사슬).

웹앱(`webapp/`, Flask)은 db/kb 를 **요청 시점에 읽는** 열람 화면입니다. 08-31 전수
조사에서 db/kb 를 고쳤으므로 화면 쪽을 감사했습니다. 감사 시작 시점 상태:
pytest **2 failed / 136 passed** + 대시보드·/sdcp 에 철회 전 서술 잔존.

## 1. 고친 것 네 묶음

### A. /benchmarks 온도스윕 절 — 존재하지 않는 스키마를 읽고 있었다

`benchmarks.html` 이 `median_abs` · `force_model.linear.intercept_eV_per_A` ·
`verdict.headline` · `date` 를 읽는데, 실물
`committee_temperature_sweep.json` 에는 `median` · `relative_median` 만 있고
`force_model` 은 **아예 없습니다**. 원인: 생성 도구
(`tools/ionic/committee_sweep_verdict.py`)가 D=a+b·F 적합(fit)을 **콘솔에만 찍고
JSON 에 넣지 않았습니다.** 템플릿은 콘솔 출력 기준의 상상 스키마로 쓰였습니다.

수선 셋:
1. 도구가 `force_model` 을 JSON 에 지속 (다음 재생성부터).
2. `data.py _sweep_view()`: **구판 JSON 이면** by_T 에 이미 있는 (힘크기, 중앙불일치)
   5점에서 같은 최소제곱으로 파생. 파생값 표시(`_derived`), 도구값이 있으면 그쪽 우선.
   실측 재현: a=+0.1017 eV/Å · R²=0.986 · n=0.687 · 기준선 바닥 32%.
3. 템플릿을 실물 키로 교정. 하드코딩 문장(원소별 순위 안정)은 5개 온도
   실데이터로 **검증 후 유지** (P>S>Li>Cl 전 온도 성립).

⚠ 트레이드오프를 알고 감수했습니다: 같은 최소제곱이 도구와 data.py **두 곳**에
있게 됩니다 (교차 주석은 달았습니다).

### B. governance 원장 dangling — 강등 사유가 자유 문자열이었다

`decisions.json` 의 두 결정(`ddE-obs` · `closure-criteria-first`)이
`superseded_by: "회신 AI 2026-08-30 §A-Q4 = C (12잡 경로)"` — 원장 `_rules` 자체가
"강등 사유도 등록된 ID" 라고 못박는데 자유 문자열이었고, 그 채택(C-12 경로)이
원장에 **노드로 없었습니다** (branch_state §3-2 의 그 구멍).

수선: `D-2026-08-30-sdcp-c12-path` 를 **proposed 로 소급 등록** (채택 자체는 08-30
커밋 390450ea 가 했고, 노드는 그때 빠진 등록의 보충이라는 논리), 두 `superseded_by`
를 그 ID 로 재배선, `decision_state` 정합화. 다음 셋은 **결정하지 않고** 노드의
`open_conflicts` 에 기록만 했습니다 — ① 프로토콜 §1 vs claim_prereg 의 명칭 충돌
② `closure-criteria-first`(systems=["*"] 일반 마감 정책)를 superseded 로 둔 것과
CLAUDE.md 현행 마감 규율의 긴장 ③ 프로토콜 잡 수 불일치(12/19 vs 16).

### C. 마감·철회를 화면에 반영

- **대시보드 SDCP 카드 교체**: 옛 카드(08-06)는 "doped 는 Li 를 뽑고 neutral 은 안
  뽑는다" 를 제목으로 걸고 ΔE_extract(부호 철회됨) · "neutral O↔Li 2.09–2.12 Å
  배위"(08-29 철회) · qe_to_vasp 외주(C-12 로 대체됨)를 본론으로 서술했습니다.
  → 08-28 마감 카드로 교체 (금지 5종 명시 · 철회 경위 · C-12 이관).
- **/sdcp 정본 md** (`kb/results/sdcp_wave1_explainer_2026_08_25.md`) 수술:
  "SDCP 가 PTFE 보다 **두 배** 세게"(금지서술 + 비교 자체 회신 P 7번 보류) ·
  "**넷 다** Li 자리 선호"(neutral 은 30 meV 해상도 **미해결**, '무선호' 금지) 교정.
  wave1.5 회신 완료(08-28 basin A) · doped 마감 · C-12 이관을 §0/§6/§8 에 반영.
  방식: **역사 절(§5–§7·§9–§10)은 당시 기록으로 보존**하고 상단 갱신 배너 +
  살아있는 결론부만 수술.
- **/sdcp 부제** "두 자기 시드 교차확인" → "realized-basin 일치분만 인용"
  (회신 P 5번 — seed 투입·독립재현 미증명).
- **NEB 카드 자기모순 제거**: 같은 대시보드에서 08-20 카드가 cc333 "이어달리기 중",
  08-27 카드가 "중단" — 전자를 08-27 판정으로 일치화.

### D. 인용위험 원장을 /governance 에 합류

`citation_hazards.json`(25건)이 웹앱 **어디에도 안 보였습니다** — "무엇을 알아냈나"
만 보이고 "무엇을 인용하면 안 되나" 가 안 보이는 화면은 이 repo 의 반복 사고
유형(낡은 인용)을 못 막습니다. /governance 를 네 원장 화면으로: 심각도 정렬
(BLOCKED 먼저) · 원장 부재 시 "0건" 이 아니라 **부재 경고**. 회귀 테스트 신설:
화면 건수 = 원장 건수, 수준 어휘가 정렬 사전 밖이면 실패.

### E. 승인 게이트의 fail-open 봉인 — 감사 **부산물**로 나온 것

월간 증빙 스크립트(`tools/reports/gabia_august_evidence.sh`, 7월판과 같은 양식)를
쓰던 중 판례 원장 출력에 상태가 `[?]` 로 찍혔습니다. 원인을 보니 **검사기 구멍**이었습니다:

`validate_governance` 의 승인 검사가 `decision_state == "active"` 만 보는데, 원장의
두 기록(polaron Fbb·S0)은 `status` 필드만 갖고 있었습니다. 즉 **그 둘은 `active` 로
올려도 어떤 검사에도 걸리지 않습니다** — 사람 승인 없이 active 가 되는 경로입니다.
(현재 값은 둘 다 `proposed` 라 실제 위반은 없었습니다. 열려 있던 것은 경로입니다.)

수선: `_dstate()` 가 `decision_state`(정본)와 `status`(별칭)를 같이 읽고, ⓐ 두 필드가
모두 없거나 ⓑ 둘이 어긋나면 그 자체를 위반으로 냅니다. 회귀시험 4건(음성 3 = 별칭
우회·필드 부재·불일치, 양성 1 = 별칭만 쓴 정상 proposed 를 오탐하지 않음).

⚠ 다만 **원장 기록 자체는 고치지 않았습니다** — 두 기록을 `decision_state` 로
정규화하는 것은 판례 파일 수정이라 1저자 판단 영역으로 두었습니다.

## 2. 확인 방법

```bash
cd webapp && python3 -m pytest tests/ -q          # 140 passed · 1 skipped
python3 tools/kb_wiki.py lint                     # 0 errors
python3 tools/convention_check.py                 # 0 위반
python3 tools/db/validate_canonical.py            # 그래프 무결성 ✅ (결정 14)
bash tools/reports/gabia_august_evidence.sh       # 증빙 217줄 · rc=0
```

## 3. 여쭙는 것

**Q1.** §B 의 소급 등록 논리가 성립합니까 — "채택은 08-30 커밋이 이미 했고, 노드는
빠진 등록의 보충" 입니까, 아니면 소급 등록 자체가 새 결정 행위라 1저자 선행 승인이
필요했습니까? 특히 `closure-criteria-first` 를 superseded 로 **유지**한 채
open_conflicts 기록으로 넘긴 처리가 맞습니까?

**Q2.** §A 의 화면 파생(`_sweep_view`)이 `D-2026-08-20-source-authority`(canonical
DB 가 원본)와 충돌합니까? "도구 지속 + 구판만 파생 + 도구값 우선" 으로 충분합니까,
아니면 JSON 재생성 전까지 그 절을 접는 것이 맞습니까?

**Q3.** §C 의 explainer 처리 방식(역사 절 보존 + 결론부 수술 + 배너)에서 **남은
금지서술**이 있습니까? 특히 E_ads 절대값 표를 "회신 기록 + 인용 시 단서 의무" 로
남긴 것이 맞습니까, 아니면 표 자체를 접어야 합니까?

**Q4.** 새 대시보드 SDCP 카드 문구가 마감 문서 준수입니까 — 특히 "이후 본류는 중성
C-12 로" 서술이 (VASP 0잡 시점에) 과합니까?

**Q5.** 화면↔원장 **일치 시험**(건수·어휘 대조)으로 충분합니까 — 화면이 원장 내용을
바꿔 말하는 드리프트를 잡는 더 싼 게이트가 있습니까?

**Q6.** 이 감사가 못 본 표면이 있습니까? 본 것: 라우트 전수 200 스모크 · 대시보드
카드 전수 판독 · /sdcp·/benchmarks·/governance·/todo·/ledger 내용 대조 · 템플릿
stale-마커 grep (`0.346` · `O···Li` · `두 시드` · 구 버전 라벨).

**Q7.** §E 의 별칭 허용(`status` 를 `decision_state` 의 별칭으로 읽는 것)이 옳은
방향입니까 — 아니면 **별칭을 아예 거부**하고 원장 기록을 정규화하도록 강제하는 쪽이
맞습니까? 지금 판단은 "읽기는 관대하게, 어긋남은 엄격하게" 인데, 관대한 읽기가 다음
드리프트를 부를 여지가 있습니다. 그리고 이런 **필드명 단위 fail-open** 이 원장
검사기의 다른 곳(assessments·artifacts·canonical entry)에도 남아 있습니까?

파일은 수정하지 않으셔도 됩니다 — **GO/NO-GO 와 P0/P1** 판정만 주십시오.
