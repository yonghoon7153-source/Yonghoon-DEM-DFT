---
title: 회신 BF — C-12 v29 VASP 외주 번들 (실행 NO-GO · P0 4 · P1 4 · Q1–Q3)
date: 2026-09-03
updated: 2026-09-03
tags: [review, codex, sdcp, c12, vasp, reply]
status: 회신반영
kind: review-reply
system: sdcp
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-03
verifiedBy: "회신 원문 (마지막 codex 리뷰 · P0 4건 + P1 이행 커밋 c895bbb4)"
campaign: sdcp_c12_vasp_handoff
target: v29 번들 (원격 add4951e…) · 생성기 tools/sdcp/vasp_handoff_bundle.py
verdict: 실행 NO-GO — 현재 실물 무결성 PASS · "잘못 생성된 다음 번들도 fail-closed 로 막는가" NO-GO
---

> ⚠ **이 회신이 C-12 의 마지막 외부(codex) 리뷰다.** 1저자 지시(2026-09-03): *"이제 codex 리뷰 못 받아 —
> 너가 NO-GO 판단해야 돼."* 이후 C-12 도 내부 적대적 리뷰 + Claude 의 GO/NO-GO 판정 + 1저자 비준으로 간다.
> 아래는 원문 그대로다 (경로는 리뷰어 로컬 감사 사본 기준).

---

실행 NO-GO — v29의 현재 실물은 정상이나, "맞는 양·맞는 잡을 게이트가 보증한다"는 목표에는 P0 4건이 남았습니다. VASP는 실행하지 않았습니다.

| 판정 대상 | 결과 |
|---|---|
| 현재 ZIP·16잡 입력의 무결성 | PASS |
| 잘못 생성된 다음 번들도 fail-closed로 막는가 | NO-GO |

확인된 사항:
- ZIP·MANIFEST·배포 파일 SHA가 모두 일치하고, 115개 결박 파일의 누락·추가·변경은 없습니다.
- 현재 estimand는 실제로 b00/pm1·box24를 가리키며, vac c1/c2·gas box20/24·k 쌍도 올바릅니다.
- 분석기 selftest는 390/390 PASS입니다.
- 원격 add4951e…의 생성기, protocol, prereg, poses, decisions을 직접 대조했고 제시 SHA와 일치했습니다.
- .SELFTEST_FIXTURE 단독 우회, estimand fallback, 대안 k-pair, J_f=0 오해는 닫혔습니다.

## P0

1. 추정량이 비준된 정확한 b00 경로에 결박되지 않았습니다.
   분석기:6424 는 누락·빈 role을 primary로 간주하고, 6439행은 planned.meta가 존재할 때만 비교합니다.
   SDCP b12를 넣고 job/planned metadata를 함께 primary로 바꾸면 semantic block 없이 통과했습니다. ratified protocol은 정확한 b00 네 경로를 이미 고정합니다(protocol:353).
   해제조건: estimand_job_keys == ratified protocol의 exact map을 직접 대조하고, role 기본값을 없애며 planned의 kind/fragment/role/seed/basin_id를 전부 필수화해야 합니다.
2. vacuum 검사가 절대 셀과 full c-vector를 보지 않습니다.
   분석기:5730 은 a·b와 c[2][2]의 차만 봅니다. 다음 두 경우가 모두 PASS했습니다.
   - 실제 셀을 46.6551→50.6551 Å로 바꾸고 Δc=4 Å만 유지
   - c2를 (0.25, 0, 40.6551)로 기울임
   해제조건: c1/c2의 절대 3×3 cell matrix, exact primary key, Cartesian 좌표 및 원자별 3축 selective-dynamics flag를 직접 비교해야 합니다.
3. gas 검사가 상대 이동만 보며 static-only도 강제하지 않습니다.
   분석기:6467 은 셀 +4 Å와 좌표 +2 Å만 봅니다. 두 상자를 함께 중심 밖으로 옮기거나 둘 다 더 큰 상자로 바꿔도 통과합니다. 6957행은 fixed_geometry_static=true를 믿을 뿐 실제 phases == ["static"]를 요구하지 않습니다.
   해제조건: 실물에서 질량 COM=(0.5,0.5,0.5), 절대 box margin, 내부기하를 재계산하고 phase 집합을 정확히 static 하나로 강제해야 합니다.
4. provenance/governance 폐포가 아직 fail-open입니다.
   provenance={"clean":true,"dirty":[],"unknown_git_state":[]}만 남겨도 --check_governance가 rc 0입니다. 인용 판정:1382 와 preflight:7671 이 필수 입력 집합·개별 SHA·개수·schema를 검사하지 않기 때문입니다.
   또한 decision digest는 ratification을 제외하고(27행), 비준 검사는 사실상 state=="ratified"만 봅니다. actor_id/role/timestamp/commit이 없어도 통과합니다.
   해제조건: 필수 provenance 집합과 SHA를 코드에 고정하고, ratification record의 필수 필드·타입 및 bundled-source 경로의 번들 내부 containment까지 검증해야 합니다.

## P1

- rc 3 구현 미폐쇄: stage 2 잡 실패로 fail=1이어도 run_staged.sh:396 이후 이를 확인하지 않고 분석합니다. sensitivity 잡 누락은 경고라서 실제 미완주인데 417행이 "계산 완주"라고 출력할 수 있습니다.
- phase POTCAR 결박 미폐쇄: 복사·해시:229 과 실행:313 사이 변경을 검출하지 못합니다. 분석기도 반환된 POTCAR 실물을 다시 해시하지 않고 receipt 문자열만 믿습니다.
- bundled_sources의 ../ 이탈, 문자열 "false"의 truthy 처리, malformed ratification의 예외 종료가 남았습니다.
- 실행 예시는 mpirun을 선택하지만 필수 LAUNCHER_BIN을 적지 않아 문서 그대로 실행하면 즉시 중단됩니다(README:33, runner:63).

## Q1–Q3

- Q1: 이번 v29 실물에는 외부 원본 대조가 실제로 완료됐습니다. 일반 설계에서는 외부 anchor가 필요하지만 governance SHA 네 개를 각각 요구할 필요는 없습니다. 인증된 EXPECT_MANIFEST_SHA256 하나가 files_sha256 전체를 고정하면 전이적으로 충분합니다. 단, 이는 내부 provenance 완전성 검사를 대체하지 않습니다.
- Q2: 계산 완료·분석 성공·원고 인용 가능을 분리하는 개념은 맞습니다. 그러나 rc 3은 OS·스케줄러 관점에서는 비영 종료, 즉 실패 상태입니다. 특히 현재는 stage-2 실패까지 "완주"로 오인합니다. 먼저 $fail==0을 강제한 뒤 rc 3을 문서화된 별도 terminal status로 쓰거나, 기본 분석은 rc 0으로 끝내고 --require-citable에서만 rc 3을 내는 편이 안전합니다.
- Q3: 1e-4 Å는 충분합니다. 더 조일 필요가 없습니다. 현재 문제는 허용오차가 아니라 절대 셀·full vector·COM·box margin·phase 불변식 자체가 빠진 것입니다.

재승인 최소조건은 위 P0 네 건의 음성 회귀시험과, stage-2 실패를 "완주"로 부르지 않는 수정입니다. 현재 첨부 원본은 건드리지 않았습니다.
