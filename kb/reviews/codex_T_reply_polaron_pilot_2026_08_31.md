---
title: "회신 T — 폴라론 pilot phase S 착수 NO-GO (P0 4건 · 해제조건 6건)"
date: 2026-08-31
updated: 2026-08-31
tags: [review, codex, sdcp, polaron, orca, pilot, estimand, no-go]
status: 이행 중
kind: review-reply
system: sdcp
confidence: high
verificationStatus: unverified
explored: false
authoredBy: agent
claimType: prescriptive
evidenceScope: multi-source-primary
---

> codex 회신 원문. ⚠ 리뷰어는 실제 `.inp/.loc/job.json` 을 받지 못했고
> 문서의 수치·설계만 보고 판정했다 (본인이 명시). 코드 실물과 대조한 결과는
> 이 파일 맨 아래 「우리 쪽 대조」에 적는다.

(원문은 대화에서 붙여넣은 그대로 — 아래 본문)
# 회신 T 요지 (원문 대화 기록 보존)

**판정: NO-GO.** P0 4건을 고치면 **ε=1 기술적 adequacy pilot(S0)** 에 한해 조건부 GO.

- P0-1 200원자 집합을 199원자 D계에 쓰고 있다 (단일 hash 사용 불가, P/D 분리 + remap 봉인)
- P0-2 97–99% 국재는 π 폴라론 seed 의 증거가 아니다 (성격 확인 필요, "MO 480 = HOMO" 는 오표현)
- P0-3 결정론 국재화 옵션이 실제로 있다 (`%loc Random 0`), `.loc` reader 에 `Guess MORead + MOInp + GuessMode CMatrix` 필수
- P0-4 ring5 와 default 는 같은 seed 다 (고유 D• 7 · P⁺ 6 · 신규 13 SP)
- Q1 ε=1 선행 조건부 찬성 — **S0** 로 격하하고 claim ceiling 명시
- Q2 `.loc` hash 결박은 필요하지만 불충분 — `LOCALIZATION_DEPENDENT` verdict 추가
- Q3 ether O 포함은 방어 가능하나 "strict backbone" 이라 부르면 안 된다 — 네 성분 분리
- Q4 초기 국재 ≠ 최종 basin — 4층 판정 필요 (초기 intervention · 최종 target hit · 안정성 · basin clustering)
- Q5-0 beta Rotate 판단 **찬성**
- Q5 ring5 회전 생략은 맞으나 독립 seed 아님
- Q6 D⁻ 를 seed source + reference 로 겸용 **찬성** (조건 넷)
- Q7 P⁺ 364 / D• 372 인덱스 차이는 문제 아님
- Q8 해제조건 6건

## 우리 쪽 대조 (2026-08-31, 실물 코드·구조로 확인)

리뷰어는 `.inp/.loc/job.json` 을 못 받았다고 명시했다. 실물과 대조한 결과:

### ✅ 확인된 것 — 원자 수는 리뷰가 정확하다

`db/structures/sdcp_orca_gs0/dp6_gs0_neutral_final.xyz` 로 직접 계산:

| 분할 | P (중성/P⁺) | D⁻·D• |
|---|---|---|
| extended (ether O 포함) | 44 / 30 / 126 = **200** | 44 / **29** / 126 = **199** |
| ether 제외 | 32 / 30 / 138 = **200** | 32 / **29** / 138 = **199** |

리뷰가 준 네 줄과 **전건 일치**한다.

### ⚠ 정정 — 제거 H 는 124 가 아니라 **162**(1-based) / 161(0-based)

산성 H 후보(1-based)는 `[119, 134, 148, 162, 176, 190]` 이고 사전 규칙(중간 위치)이
고르는 것은 **162** 다. 따라서 인덱스 이동 경계도 다르다:
`i < 161 → i` · `161 → absent` · `i > 161 → i−1`.

### ⚠ 리뷰가 실물을 못 봐서 생긴 오차 둘

**(a) D seed 선택은 오염되지 않았다.** `pil_pick_seed_mo(pops, occ, group_idx, kill, ...)`
가 `kill` 로 remap 을 적용한 뒤 목표 집합을 만든다(`build_v7c_trimer.py:2732`).
`pilot_analyze.remap_sets()` 도 같은 remap 을 한다. 즉 **계산은 맞게 하고 있었고,
없는 것은 그 사실의 봉인**이다 — manifest 가 200원자 `atom_map` 하나와 해시 하나만
싣고 D 프레임을 런타임에 파생시킨다. P0-1 의 실질(“단일 hash 를 쓸 수 없다”)은
그대로 유효하므로 P/D 분리 + remap 해시를 봉인한다.

**(b) `default` 는 `.loc` 를 읽지 않는다.** `moread=(None if sd == "default" else gbw)`
이라 default 는 `%moinp` 도 `Guess MORead` 도 없는 **fresh guess** 다 — ring5 와
같은 초기 determinant 가 아니다. 리뷰의 전제("같은 `.loc`를 읽고 회전을 생략한다면")가
실물에는 해당하지 않는다.
⛔ 다만 **job 레코드가 default 에도 `orbitals_from`·`loc_sha256` 를 찍는다** —
읽지도 않는 파일을 출처로 기록한 것이고, 리뷰가 그렇게 읽은 것도 무리가 아니다.
레코드를 고치고 `seed_equivalence_class` 를 명시한다.

### ⛔ 가장 아픈 것 — `GuessMode CMatrix` 부재 (P0-3)

현재 `.loc` reader 는 `%moinp` + `Guess MORead` 만 있다. `GuessMode` 기본값은
에너지 기준 정렬을 전제하는데 **국재 궤도에는 물리적 에너지 순서가 없다.**
그러면 ORCA 가 읽으면서 MO 를 재정렬할 수 있고, 우리 seed 는 `.loc` 인구표의
**인덱스**로 목표를 지정하므로 `Rotate {j, 480}` 이 **엉뚱한 궤도를 돈다.**
리뷰가 든 셋 중 이것이 결과를 조용히 틀리게 만드는 유일한 항목이다.

## 이행 결과 (2026-08-31)

| 항목 | 상태 | 어디에 |
|---|---|---|
| P0-1 P(200)/D(199) 프레임 분리 + remap 봉인 | 완료 | `pilot_atom_manifest` |
| P0-2 선택 MO 의 π / O-nonbonding 성격 확인 | 완료 | `pil_mo_character` · `pil_character_verdict` |
| P0-3 `%loc Randomize 0` + `GuessMode CMatrix` | 완료 | `PIL_LOC_KW` · `_pil_inp` |
| P0-4 seed 중복 판정 + job census 재봉인 | 완료 | `seed_equivalence_class` |
| Q3 네 성분 분할 (bb_core / ether_O / sulfonate / other) | 완료 | `pilot_components` · `F_components` |
| Q4 4층 실현 판정 | 완료 | `pil_target_hit` · `pil_stability_layer` · `pil_basin_cluster` · `pilot_restart` |
| Q1 S0 격하판 사전등록 | 완료 | `db/properties/sdcp_polaron_pilot_prereg_S0_2026_08_31.json` |
| Q2 `LOCALIZATION_DEPENDENT` 판정어 | 완료 | S0 사전등록 §판정어 |

### ⛔ 이행하면서 드러난 것 — 세 경로가 전부 죽어 있었다

리뷰가 "23 PASS 는 문자열 selftest 이지 e2e 증명이 아니다"(회신 R2)라고 한 것이
**이 캠페인에서 그대로 재현**됐다. 회신 T P0 1~3 을 고치면서 들어간 회귀 셋:

1. `pilot_generate` — `_loc_rand` 를 선언 **전에** 써서 `UnboundLocalError`.
   `--polaron_pilot` 이 아무것도 만들지 못하고 죽었다.
2. `pilot_seeds` — `pil_parse_mopop` 의 4-튜플을 3개로 언팩해 `ValueError`,
   그리고 `_sy_j`·`_po_j`(성격 판정용 원소·좌표)가 아예 정의되지 않았다.
3. `pilot_analyze` — `_spin_block` 은 **리스트**를 돌려주는데 Q3 네 성분 코드가
   `hir.values()`·`hir.get(i)` 로 dict 처럼 써서 `AttributeError`.
   그리고 목표 링 이름을 `"ring" + "B_ring0"[2:]` = `"ringring0"` 으로 조립해
   2층 명중이 **영원히 False** 였다.

그런데 selftest 40건은 전부 통과했다 — **순수 헬퍼만 부르고 세 함수를 한 번도
실행하지 않았기 때문**이다. CLAUDE.md 의 "양성만 있는 selftest" 그 자체다.

이제 합성 다이머(26원자·링 2·SO₃ 2)로 phase L/L2/S/probe 산출물을 만들어
세 경로를 **실제로 돌린다**. selftest 150건 — 음성 경로에 무작위 국재화 표지·
`GuessMode` 누락·MOPOP 부재·면내 σ MO·비정상 종료·출력 삭제·`.loc` 삭제·
프레임 바꿔치기·구판 manifest·개입 실패·probe 결측·링 미분해·불안정 미재판정·
`StabPerform` 미수행·`.gbw` 없는 재계산 요청이 들어 있다.

### ⚠ 아직 못 한 것

- **실물 ORCA 검증이 없다.** `%loc` 출력 형식, `Rotate {j,nbeta,90,1,1}` 의 실제
  동작, `NoIter` probe 가 스핀 인구를 찍는지 — 전부 미검증이다. selftest 픽스처는
  *우리 판독기가 받는 형식*의 재현이지 ORCA 출력이 아니다. phase L 첫 실행이
  곧 smoke test 다.
- ε_dry_polymer 값 미정 (litdb 근거 필요) · torsion-diverse 거리 척도 미정.
