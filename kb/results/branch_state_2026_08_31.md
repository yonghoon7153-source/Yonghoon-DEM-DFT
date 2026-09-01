---
title: "브랜치 현황 지도 2026-08-31 — 전수 조사 후"
date: 2026-08-31
updated: 2026-08-31
tags: [handoff, branch, status, sdcp, c12, polaron, li3nd, audit]
status: 진행
kind: result
system: repo
supersedes: kb/results/branch_state_2026_08_30.md
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-31
verifiedBy: "git log · kb/reviews 실물 짝짓기(tools/kb_wiki.py reviews) · db/properties 전수 · selftest 스윕 63건 · 에이전트 3축 교차조사"
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

# 브랜치 지도 (2026-08-31)

08-30 지도(`branch_state_2026_08_30.md`)를 **대체**한다. 그 문서는 SDCP 를 "Stage A v9"
로 적었는데, 그 뒤 캠페인이 **C-12 로 개명되고 v18** 까지 갔다.

## 0. 한 줄

**계산은 하나도 안 늘었고, 검증만 늘었다.** C-12 는 VASP 를 한 잡도 안 돌린 채 리뷰
AV 까지 갔고 P0 전건을 닫았다 — 남은 것은 v19 재생성 하나다.

## 1. 캠페인 넷

| 캠페인 | 상태 | 다음 한 수 |
|---|---|---|
| **C-12 외주 VASP** (⏭-6) | v18 봉인 · **VASP 0잡** · 회신 AV NO-GO → P0 전건 이행 (①~⑦ 닫힘) | **해제조건 ⑧** — v19 재생성 + 실물 e2e |
| **폴라론 S0** (ORCA, ⏭-7) | 번들 생성 완료 · gabia **코어 대기** · 리뷰 U 발송 대기 | 코어 나면 phase L 이 곧 smoke test |
| **Li₃Nd P0-2 control** (⏭-4) | rattle r0 ✓ · r1·r2 진행 · **r3 미착수** · GPU 점유 중 | r1~r3 회수 후 **Nd 변위 패턴** 판정 |
| **gap nscf** | comp1 ✅(2.0656 재현) · b2o3 ✅ · lpsocl ✅ · **modelc 진행** | modelc 완주 |

⚠ **"Stage A" 라는 이름이 두 캠페인에 쓰인다.**
`sdcp_stageA_closure_conditions_*` = VASP 슬랩 번들(→ C-12 로 개명, superseded).
`sdcp_stageA_conformer_rule_*` = **ORCA n=6 올리고머** conformer 캠페인(⏭-0). 다른 것이다.

## 2. 이번 전수 조사에서 고친 것

| 축 | 무엇이 썩어 있었나 | 고침 |
|---|---|---|
| **리뷰 장부** | 프롬프트 27건이 `발송 대기` 인 채였고 그 중 **17건은 회신이 이미 왔다**. lint 는 '오래됨' 만 보고 '회신 왔는데 대기' 를 못 봤다 | `kb_wiki.py reviews` 신설 (증거에서 사슬 재구성 · lint 합류) · `kb/reviews/INDEX.md` 자동생성 · 17건 status 정정 |
| **철회값 부활** | `sdcp_neutral_closed` 가 **허용 서술 칸**에 철회된 `O···Li 2.09 Å` 를 두고 세 필드 뒤에서 그것을 금지했다. `phaseB_dftu_v1` 은 그 원본을 마커 없이 긍정형으로 보관 | 허용 칸을 철회형으로 교체 · 원본에 철회 래퍼 |
| **인용 게이트 자체** | `citation_hazards` 가 **철회된 `dE_extract` 를 "인용하라"** 고 적고 있었고, 번들을 v13·14잡으로 서술 | 2건 정정 + 미등재 위험 3건 추가 (wave1 보류 · 기전 양방향 · C-12 프로토콜) |
| **죽은 selftest** | `codoping_ml.py` 의 `--selftest` 가 없는 함수를 불러 `NameError` — **한 번도 시험된 적 없었다** | 22건 작성(음성 위주) · 폐기본 `make_allF` 는 폐기 안내로 · `convention_check.py --selftests` 스윕 신설 |
| **장부** | C-12·폴라론이 **아예 없었다**. 제목이 본문과 반대인 항목 2건. 같은 파일 안에서 충돌하는 조항 1건 | ⏭-6·⏭-7 신설 · 모순 3건 정정 · β 폐기 배너 4곳 |

## 3. 🔴 아직 안 고친 것 (판단이 필요하다)

1. **C-12 번들에 모순되는 사전등록 둘이 달려 있다.**
   `sdcp_c12_protocol_2026_08_30.json` §1 은 보고량을 `adsorption energy` 라 부르고,
   `sdcp_c12_claim_prereg_2026_08_31.json` 은 그 이름을 **금지어**로 지정했다.
   `IDENTITY_v18.json` 이 둘 다 사전등록으로 나열한다.
   → 정본을 claim prereg 로 정하고 프로토콜 §1 을 낮추는 것이 맞아 보이지만, 사전등록을
   고치는 일이라 **1저자 판단**이 필요하다.
2. **C-12 estimand 가 거버넌스에 없다.** `db/governance/decisions.json` 에 `c12` 0건.
   세 파일이 "proposed — 사람이 ratify" 라 적었는데 등록 자체가 안 됐다.
3. **프로토콜의 잡 수가 실물과 다르다** (§0 12잡 · §12 19잡 vs 실물 **16잡**).
   citation_hazards 에 등재는 했지만 파일 자체는 안 고쳤다.
4. **`sdcp_wave1_citable.json` 에 `ptfe_c10_Litop` pm1 값이 없다.** 그런데 마감 문서의
   확정값과 0.346 eV 산술이 그 값(−0.4124)에 걸려 있다. 의도적 제외인지 사고인지 기록이 없다.
5. **깨진 경로 61건** (에이전트 전수 스캔). 대부분 "구현 예정" 이거나 다른 브랜치에만 있는
   도구다. 이름만 바뀐 것 9건은 고치면 되고, `db/properties/msd_window_scan_comp1_p1600.csv`
   는 **200 ps Ea 철회의 근거로 인용된 산출물인데 git 이력에도 없다** — 성격이 다르다.

## 4. 규율 — 이번에 재확인된 것

- **워처·frontmatter 는 근거가 아니라 주장이다.** 08-30 은 `alive()` 가 이틀치 사망을
  감췄고, 08-31 은 `status:` 가 17건의 회신 수령을 감췄다. 둘 다 **실물 대조**로 뒤집혔다.
- **라벨 재사용을 조심한다.** S·T·U 가 각각 두 캠페인에 쓰여, 인용 횟수 합산이
  미발송 프롬프트를 '회신 수령' 으로 오판하게 만들었다(내가 실제로 한 번 틀렸다).
  `kb_wiki.py reviews` 는 이제 재사용 라벨의 인용을 증거로 쓰지 않는다.
- **함수를 부르지 않는 selftest 는 그 함수가 죽었는지 모른다.** 폴라론에서 셋이 죽어 있는데
  40건이 통과했고, `codoping_ml` 은 시험 자체가 죽어 있었다.
