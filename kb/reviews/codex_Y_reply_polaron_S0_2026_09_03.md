---
title: 회신 Y — 폴라론 S0 (NO-GO · P0 8 · P1 8 · Q1–Q5)
date: 2026-09-03
campaign: sdcp_polaron_S0
prompt: (채팅으로 전달 — 파일 없음. 대상 커밋 ddf1f971, 세 파일 SHA-256 제시)
verdict: NO-GO (loccheck 단독만 GO)
supersedes_reply: kb/reviews/codex_X_prompt_polaron_S0_2026_09_02.md (회신 X 이행분에 대한 재심)
---

> ⚠ **이 회신이 마지막 외부(codex) 교차리뷰다.** 1저자 결정(2026-09-03): *"sdcp 관련 리뷰는
> 우리가 독자적으로 리뷰하고 돌려야 될 듯 — codex 교체 리뷰는 이제 어려워."*
> 이후 SDCP 리뷰는 내부 적대적 리뷰(별도 컨텍스트) + 1저자 비준으로 간다.
> 아래는 회신 원문 그대로다 (고쳐 쓰지 않는다 — 이력 규율).

---

NO-GO — loccheck 단독만 GO입니다. L·L2·seeds·probe·S·analysis·restart는 아직 실행하면 안 됩니다.
제시한 세 파일의 SHA-256은 정확한 ddf1f971… 커밋과 모두 일치했습니다. calibration 자체 selftest도 14/14 통과했습니다. 그러나 통합 경로에는 아래 P0가 남아 있습니다.

## P0

1. F_out이 F_in의 하한이라는 논리가 성립하지 않습니다.
   원자별로 |∫w_A Δρ| ≤ ∫w_A|Δρ|는 맞지만, F에서는 분자와 분모가 모두 줄어들므로 비의 대소는 보장되지 않습니다. 사전등록도 한 줄에서는 이를 인정하면서 바로 다음 줄에서 "더 작은 값이라 false positive가 없다"고 반대로 결론 냅니다. prereg:48–78
   실제 반례는 간단합니다. 실공간 group 분율이 0.49/0.31/0.20이고 target 밖에서만 0.10이 상쇄되면 cancellation_ratio=0.90이지만 population target은 0.49/0.90=0.544가 되어 0.5 class 경계를 거짓으로 넘습니다.
   따라서 0.90을 통과해도 false positive가 가능합니다.
2. calibration은 현재 판정기에 연결되지 않은 고아 산출물입니다.
   build_v7c_trimer.py에는 spin_partition_calib, cancellation_ratio, S0_UNDERESTIMATED_BY_PARTITION 소비가 0건입니다. calibration 도구도 수치 JSON만 만들고 0.90/0.70 판정은 하지 않습니다. spin_partition_calib.py:351–379
   또한 ratified prereg에는 calibration 도구 SHA, cube/groups SHA, phase-S job·receipt SHA가 결박돼 있지 않습니다. 현재는 ratio가 0.031이어도 production analyzer가 기존 class를 낼 수 있습니다.
3. prereg fail-closed가 디렉터리명으로 우회됩니다.
   _pil_check_prereg()는 where 문자열에 "generate"가 포함되면 scale_actual 누락을 허용합니다. 따라서 일반 경로는 차단되지만 u_s0_generated 같은 경로에서는 같은 입력이 통과합니다. build_v7c_trimer.py:4855–4863
   더구나 main이 mutable manifest의 prereg 경로를 다시 "정본"으로 지정하므로 임의 prereg가 자기 자신과 일치하는 구조입니다. build_v7c_trimer.py:7643–7646
4. probe를 건너뛰고 S를 직접 실행할 수 있습니다.
   S)는 preflight S만 호출하고 영구적인 probe PASS 증서를 요구하지 않습니다. stage lock도 실행 중인 .lock_probe만 확인합니다. probe 미실행·실패·crash 뒤에도 직접 run_pilot.sh S가 열립니다. build_v7c_trimer.py:7495–7500
5. receipt가 실제 소비 입력과 끝까지 결박되지 않습니다.
   seed 생성은 L receipt의 존재만 확인한 뒤 L input/output/XYZ를 사용합니다. receipt 후 L 산출물을 교체해도 들어갈 수 있습니다. L2·S0P 행에는 XYZ SHA가 없고, 공통 receipt gate는 XYZ/moinp 해시가 빠지면 fail-open입니다. 첫 번째 glob XYZ만 고르는 decoy 우회도 남습니다. L receipt 확인, 실제 소비, fail-open
6. 무회전 control의 receipt 실패가 최종 block으로 전파되지 않습니다.
   control output을 baseline으로 먼저 사용하고, receipt 문제는 보조 no_rotation_controls에만 기록됩니다. 교체되거나 무증서인 control이 intervention 판정을 움직일 수 있습니다. build_v7c_trimer.py:6503–6515
7. loccheck의 ORCA identity가 L/L2에만 이어집니다.
   probe·S·restart는 다른 ORCA로 실행할 수 있고, receipt에 기록된 ORCA 필드를 analyzer가 소비하지 않습니다. 모든 단계가 loccheck 인증서의 resolved executable path·SHA와 일치해야 합니다.
8. L2 suffix patch가 원자적이지 않습니다.
   잡별로 검증 직후 수정하므로 두 번째 잡에서 실패하면 첫 번째 잡은 이미 바뀐 채 남습니다. transition receipt는 전체 성공 뒤에만 생성되고 production consumer도 이를 검증하지 않습니다. 전건 선검증 → 임시 트리 수정 → 원자적 교체 순서가 필요합니다. build_v7c_trimer.py:7391–7443

## P1

- NO_ROTATION_NEEDED를 probe verdict는 성공으로 세지만 final analyzer는 INTERVENED가 아니면 막습니다.
- scale_actual은 34로 맞지만 초기 manifest census는 아직 31을 기록합니다.
- "probe 절반 이상 실패 시 중단"은 dead rule입니다. 실제 CLI는 하나만 실패해도 block합니다.
- stage lock은 live PID만 보며 L←loccheck PASS, analyze←S PASS 같은 완료 증서를 요구하지 않습니다.
- calibration의 min_points는 voxel 개수만 봅니다. grid spacing·경계 절단·격자 수렴·∫Δρ sanity를 확인하지 않습니다.
- Becke 한 자세로 측정한 손실을 production Hirshfeld 및 다른 basin 전체에 일반화할 근거가 없습니다.
- Becke weight underflow 시 uniform weight로 조용히 대체하는 경로도 결과 질량을 기록하거나 차단해야 합니다.
- 기본 Windows 비-UTF-8 콘솔에서는 help/selftest가 UnicodeEncodeError로 종료됩니다.

## Q1–Q5

Q1 — dry-run: 이번 한 번은 ORCA 0잡이고 결과를 보지 않았으며 공개했으므로 과학적 사전등록을 오염시킨 것으로 보지는 않습니다. 다만 임시 prereg를 스스로 ratify하는 절차는 정식 관행으로 금지해야 합니다.
정상 순서는 다음입니다.
1. proposed 상태에서도 가능한 비실행 --plan-only
2. job key·census·builder/tool SHA를 담은 PLAN.json
3. plan digest를 prereg에 봉인하고 비준
4. production 생성물이 exact plan과 일치할 때만 실행 허용
규모를 실행파일 생성 후 채우는 방식보다는 이 순서가 맞습니다.

Q2 — 중단 규칙과 판정 규칙: 개념적 구분은 맞습니다. P⁺의 "하나 이상 회수"와 "부정 결론에는 전건 정상"도 유효합니다. 다만 probe의 절반/하나 규칙은 현재 둘 다 작동하지 않습니다.
- 하나라도 실패하면 class는 즉시 NO_VALUE
- 추가 probe는 진단 목적으로만 계속할 수 있음
- 절반 실패 시 남은 진단 probe까지 중단
처럼 명시해야 합니다. 어느 경우에도 첫 실패 뒤 production S를 열어서는 안 됩니다.

Q3 — 0.90/0.70: 사전 고정했다는 점은 좋지만 class gate로는 타당하지 않습니다. <0.70 금지는 과하지 않고 오히려 불충분합니다.
cancellation_ratio는 설명용 QC로만 두고 최소한 다음을 직접 비교해야 합니다.
- F_in과 F_out의 winning group 동일
- F≥0.5 경계 통과 여부 동일
- winner–runner-up 0.10 margin 판정 동일
- 사전 고정한 max_G |F_in−F_out| 허용치 통과
가능하면 production과 같은 Hirshfeld weight로 검사해야 합니다. 한 자세 Becke 검사만 한다면 그 자세에만 class를 제한해야 합니다.

Q4 — loccheck: 실행해도 됩니다. 단,
- 정확한 ratified prereg와 ddf1f971… builder 사용
- 임시 prereg 사본 사용 금지
- 동일한 absolute ORCA executable 사용
- _loccheck, 입력·출력·.loc.gbw, LOCCHECK_PASS.json 전부 보존
- 완료 직후 중단하고 회신
조건입니다. loccheck는 H₂O L→L2의 작은 ORCA 실행 두 번이므로 이후에는 "production ORCA 0잡"은 맞지만 "ORCA 0회"는 아닙니다. loccheck PASS가 L의 자동 승인은 아닙니다.

Q5 — 구조적 해법: "새 필드 + 수동 시험"보다 typed evidence DAG가 필요합니다.
- 모든 증거에 producer·consumer·required-before-stage·schema·hash를 선언
- 다음 단계는 predecessor PASS receipt의 digest를 필수 입력으로 소비
- 임계 필드는 공통 strict accessor로만 읽기
- schema에 선언됐지만 production 경로에서 읽히지 않는 필드는 CI 실패
- 각 필드에 삭제·타입변조·stale SHA·산출물 교체 mutation test 자동 생성
- 실패 시험은 rc≠0뿐 아니라 정확한 오류코드, ORCA 호출 0회, 파일변경 0개까지 확인
현재 calibration이 "생성되지만 아무도 읽지 않는 필드"의 바로 그 재현 사례입니다.
최소 해제조건은 P0 8건 전부입니다. 특히 estimand 수학을 먼저 바로잡고, calibration→analyzer 소비와 영구 PROBE_VERDICT_PASS를 연결한 뒤 나머지 receipt 계보를 공통 verifier로 통합해야 합니다. 파일은 수정하지 않았습니다.
