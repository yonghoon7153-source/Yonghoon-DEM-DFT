# Codex 판정 — r_int G1 · LHS 응력/전력/인계 · network 정지 경로

작성: 2026-10-05 · 판정: **HOLD — 현재 스냅샷으로 194건 망 배치·인계를 개시하지 말 것.**

대상: yonghoon7153-source/Yonghoon-DEM-DFT, 브랜치 claude/sdcp-dem-manuscript-si-pqwtv8, 고정 커밋 **30c8205c5efb3873ae6fa856881fa184bd041d4d**. 사용자 제공 요청서의 10-05 보강판을 포함했다. 브랜치 끝을 따라가지 않았다.

생산 코드·Git 상태·기존 배포본을 바꾸지 않았다. 재봉인, WSL/194건 배치, 실침대 대형 재풀이, DEM/MPM/GPU 캠페인을 실행하지 않았다. 취득한 독립 소스 사본에서 소형 CPU 시험, 실제 함수 호출, 입력 변이 및 프로세스 내부의 일시적 CG 반복수 제한만 수행했다.

## 0. 결론과 증거 범위

**새 P1 4건이다.** 그중 하나는 잘못된 수치의 승인, 둘은 생산–소비 연결의 실행 차단, 하나는 필수 관문 실패 후에도 실패 후보가 활성 성공 세대로 남는 게시 순서 결함이다. P1이 모두 “194개 숫자가 틀렸다”는 뜻은 아니다.

| ID | 심각도 | 무너지는 결론 |
|---|---|---|
| RGL-01 | P1 | wetted/bare 적용 영수증 통과 ⇒ collector 보정과 jb가 수치적으로 유효 |
| RGL-02 | P1 | 정상 비관통 침대도 새 network 정지점에서 정상 완료할 수 있음 |
| RGL-03 | P1, 인계 실행 차단 | 새 network 배치 결과를 기존 ⑤⑥⑦ 인계 생성기가 소비할 수 있음 |
| RGL-04 | P1 | 새 필수 관문 실패 후보는 활성 성공 세대를 차지하지 않음 |
| RGL-05 | P2 | ⑤⑥⑦ 관문 통과 ⇒ 유한·범위 내·필수 근거 완비·0/N/A 일관 |
| RGL-06 | P2 | Love–Weber status=OK ⇒ 입력 기하·요약·영 하중 검사가 정상 |
| RGL-07 | P2, 재시도/기존 자료 경로 | τ 도우미 통일 ⇒ σ와 σ₀의 실제 세대·온도 짝도 통일 |
| RGL-08 | P2 | network 정지 계약 통과 ⇒ τ/전력 인계 입력 완비 및 파일 간 정합 |
| RGL-09 | P2 | RINT-03 도구의 Spearman이 동률·상수 벡터에도 올바름 |
| RGL-10 | P3, 증거 표현 | GOLD 8 = 실침대 8개에서 원시 비트 동일 |

반대로 **AM 최종 상 마스크 수정, I²R 가중 협착 전력 몫의 정의, 검사한 경계 규칙 추출, 정상 입력의 반올림 반폭/명시 제외 규칙은 지지한다.** HOLD가 그 수정들을 되돌리라는 뜻은 아니다.

### G1–G6 판정

| 게이트 | 판정 | 유지되는 부분 | 최소 해제 조건 |
|---|---|---|---|
| G1 r_int | **HOLD** | 13건의 원래 적용·소유권·라벨 처방은 대부분 닫힘 | RGL-01의 독립 wetted/bare 수렴 검증과 소비자 전파. 순위 수치를 증거로 사용할 경우 RGL-09도 수정 |
| G2 Love–Weber | **HOLD** | branch tensor·부호·대칭부 VM은 명시한 접촉 응력 지표로 타당 | RGL-06 입력/영 분모 실패와 frame/벽 가정의 증거 범위를 정리 |
| G3 전력 몫·경계 추출 | **GO, 이 변경 자체에 한정** | 같은 FULL 해의 물리 간선 전력 몫, 시험한 추출 중립성 | RGL-10 문구 정정. G5 게시·상태 연결이 풀리기 전 배치 GO로 확대하지 말 것 |
| G4 ⑤⑥⑦ 인계 | **HOLD** | 정상 194행 요약표 산술·명시 제외·반올림 규칙 | RGL-03과 RGL-05의 실제 build_handover 통합 회귀 |
| G5 network→τ 배치 | **HOLD** | Stage E 앞 정지·보존 모드 거부·대부분 기존 게이트 | RGL-02/03/04/08 해소 → 게이트 → 적용 가능한 재봉인 절차 → 배치 |
| G6 τ 등급/COMSOL | **HOLD, end-to-end 짝 보증** | 올바르게 짝지어진 입력의 식·모드 라벨 통일 | RGL-07 온도 세대 병합/재시도 회귀. 깨끗한 25 °C 신규 LHS 전체가 틀렸다는 판정은 아님 |

### 어떤 증거인가

- 고정 커밋에서 취득한 소스·문서·텍스트 자료 **223파일 모두 원 Git blob SHA-1과 일치**했다. SHA-256도 함께 기록했다. 완전한 Git 체크아웃은 아니다.
- 실제 수치 함수 재현: RGL-01, RGL-02, RGL-06, 전력 회로와 경계 구식/신식 비교.
- 실제 인계 함수에 입력을 바꾼 반례: RGL-03/05.
- 실제 웹앱 helper·머지·판정기·소비자를 실행하되 solver의 파일 생성만 작은 fixture로 대신한 계약 반례: RGL-04/07/08. RGL-04는 RGL-02의 **실제 수치 생산 결과**로도 재현했다.
- 194행 검산은 커밋된 요약 CSV의 산술 검산이다. 194개 원 DEM dump 재분석도, 194건 전체 인계 재생성도 아니다.
- 실침대 r_int NPZ 셋과 real14 압축 dump 둘은 독립 재실행하지 못했다. 저자의 크기 수치를 독립 측정값으로 승격하지 않았다.
- 원장 findings.json은 이 취득 경로에서 본문을 확보하지 못했다. 빈 파일을 대신 만들어 쓰지 않았으며, 본 판정은 요청서·고정 코드·재현 증거에 근거한다.

증거/명령은 §5, 환경 예외는 §6, 실행 전 최소 목록은 §7에 모았다. 각 finding의 “재현 성공”은 **현재 결함을 다시 발생시켰다**는 뜻이지 생산 코드 PASS라는 뜻이 아니다.

## 1. 새 finding

### RGL-01 · P1 — 보조 CG가 미수렴이어도 collector complete·check-arm PASS

위치: [scripts/mpm_webapp_payload.py:2309](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/mpm_webapp_payload.py#L2309), [scripts/mpm_webapp_payload.py:2313](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/mpm_webapp_payload.py#L2313), [scripts/mpm_webapp_payload.py:2318](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/mpm_webapp_payload.py#L2318), [scripts/mpm_webapp_payload.py:2334](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/mpm_webapp_payload.py#L2334), [scripts/mpm_webapp_payload.py:2359](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/mpm_webapp_payload.py#L2359), [scripts/run_contract.py:765](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/run_contract.py#L765), [scripts/run_contract.py:802](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/run_contract.py#L802), [scripts/step3_sigma.py:1176](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/step3_sigma.py#L1176).

실제 payload producer의 작은 raster를 사용했다. wetted 또는 bare 호출 동안만 CG_MAXITER=1로 제한하고 즉시 원복했다. σ, residual, receipt 결과를 임의로 꾸미지 않았다.

| 경우 | 보조 σ, S/cm | CG info / residual | producer / collector / check-arm | R_geom, Ω·cm² |
|---|---:|---|---|---:|
| 정상 | wetted=bare=0.0009486874831110222 | 0 / 9.783687086144589e-9 | 게시 / complete / rc 0 | 0 |
| wetted만 반복 1회 | 0.007178713043478262 | 1 / 0.3464101615137754 | **게시 / complete / rc 0** | **3.8** |
| bare만 반복 1회 | 0.007178713043478262 | 1 / 0.3464101615137754 | **게시 / complete / rc 0** | 0으로 clip |
| main만 반복 1회 | 미수렴 | 실제 미수렴 | **producer rc 3, 정상 게시 안 함** | — |

잘못된 보조 σ는 정상의 **7.57배**다. 보조 변이에서 main σ=0.0010352120036449418 S/cm, residual=9.561089107260143e-9는 그대로다. 전자 세 영수증은 applied·solved=true·3816개 계면 face이며 공용 계면 검사도 통과한다. bare의 미수렴 φ로 입자 jb도 생성된다.

원인: collector 분기는 reason/σ의 부호만으로 R_geom을 만들고, 공용 component 검사에서는 “collector에는 CG가 없다”는 전제로 다른 component의 conv_ok를 건너뛴다. 요청표가 실제 솔브에 적용되었다는 증거와, 그 솔브가 수렴했다는 증거는 다르다.

- 무너짐: 네 솔브 영수증을 결과 전체의 수치 유효성 증서로 해석하는 것.
- 유지: 요청 누락·잘못된 계면 표 적용을 잡는 RINT-02 처방, 주 솔브의 기존 미수렴 차단, AM 소유권 수정.
- 범위: r_int OFF에도 존재하는 collector 경로 결함이다. same-sid 법칙 자체의 새 오류가 아니다. 최종 코호트 판정 전체는 돌리지 않았지만 producer와 실제 check-arm까지 실행했고 최종 판정기의 공용 component 소비 경로도 확인했다.

최소 수정: wetted와 bare 각각 cg_info·유한 residual·unconverged를 보존하고 모두 수렴해야 R_geom/jb/complete를 게시하라. producer뿐 아니라 공용 소비자 증거 검사를 고친다. 두 보조 솔브의 독립 실패, 누락/상충 tuple, 비유한 residual, 정상 main 대조를 회귀에 넣는다.

재현: §5의 probe_adversarial.py. 증거: evidence_g1/adversarial_results.json, wetted_unconverged_solver_records.json, wetted_unconverged_check_arm.log.

### RGL-02 · P1 — 정상 비관통을 생산자는 not_computed로 내고 새 관문은 거부한다

위치: [scripts/network_conductivity.py:94](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/network_conductivity.py#L94), [scripts/network_conductivity.py:589](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/network_conductivity.py#L589), [scripts/network_conductivity.py:1226](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/network_conductivity.py#L1226), [webapp/pipeline_service.py:655](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/webapp/pipeline_service.py#L655), [webapp/pipeline_service.py:696](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/webapp/pipeline_service.py#L696).

실제 망 생산 함수를 14개 노드·10개 간선의 끊긴 SE 합성망에 실행했다. 두 모드 모두:

- sigma_full=None, sigma_full_status=not_computed
- percolating_fraction=0.0, calc_percolation=0.0, boundary_rule=L0
- 협착 전력 몫=None, 사유=no percolating FULL solution

그 **실제 결과**를 실제 _network_and_stage_e 정지 helper로 연결하면, 앞의 solver/채널 관문은 통과하지만 새 required 단계가 두 모드의 not_computed 때문에 **failed**가 된다. 같은 결과에 tau_flux는 **NOT_PERCOLATING, f=0, τ²/τ 빈칸**을 반환한다. 이 통합 fixture의 별도 장부에는 basis_check=mismatch:0.2707도 남으므로, 전체 τ 장부의 정상 인증으로 읽으면 안 된다. 비관통 생산 상태와 stop 관문의 모순은 그 진단과 별개로 재현된다.

이는 누락된 입력을 억지로 만든 반례가 아니다. test_tau_flux의 기존 **K3도 “not_computed, valid_zero 아님”을 기대하며 35/35에 포함**돼 있다. 반면 새 T12d는 mock에 valid_zero를 써서 이 연결 불일치를 놓친다. 두 검사군이 각각 초록이어도 생산 상태 계약은 모순된다.

- 무너짐: “not_computed를 거부하면 못 푼 침대만 failed로 남는다.”
- 유지: 정말 못 푼 침대를 완료 처리하지 않겠다는 정책. 비관통에서 전력 **몫**이 None이라는 규칙.
- 규모 한정: 130행 기존 요약표에는 비관통 24행이 있으나, 이를 새 망 배치의 정확한 실패 수로 단정하지 않는다. 동일 boundary 정의와 실제 dump까지 재분석하지 않았다.

최소 수정: 수치 생산자에 **증명된 no-through 상태/사유**를 명시하고 정지 계약·tau 계약이 같은 상태를 소비하게 하라. 모든 not_computed 허용 또는 모든 None→0은 오답이다. 관통 실패의 원인, solver 관통, 독립 calc_percolation, 채널 상태가 함께 맞아야 한다. conductivity/f의 물리적 0과 I²R 몫의 0/0 미정의를 분리한다.

재현: §5의 probe_actual_zero.py 및 probe_network_independent.py. 증거: evidence_g56/actual_zero_results.json. 이 통합 시험의 원자/접촉 입력 파일은 helper I/O를 위한 최소 fixture이고 수치 레코드는 실제 함수 산출이다. 전체 analyze_contacts CLI를 실행한 실침대 시험이라고 해석하지 말 것.

### RGL-03 · P1, 인계 실행 차단 — network 배치를 ⑤⑥⑦ 생성기가 받지 않는다

위치: [scripts/lhs_design_dataset.py:1212](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/lhs_design_dataset.py#L1212), [scripts/lhs_design_dataset.py:1993](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/lhs_design_dataset.py#L1993).

실제 build_handover를 정상 selftest fixture로 호출했다.

- stop_after=contact, groups=f1,fracture,area → 성공.
- **다른 값은 그대로, stop_after만 network** → FillRefusal.
- 오류는 “--webapp-groups network의 부분집합”을 요구하지만 network는 유효 WA_GROUPS 이름도 아니다.

WA_STAGE_GROUPS가 contact/coverage만 알고 있다. 새 정지점이 접촉 산출물을 실제 포함해도 허용 단계 매핑이 그것을 부정한다.

P1을 붙이는 이유는 새로 요청한 **배치→인계 기능 전체의 일률적 실행 차단**이다. 기존 contact 인계의 계산 오류, 네트워크 솔버 실패, 기존 194행 수치 오염이라는 뜻은 아니다.

최소 수정: network가 보장하는 기존 묶음의 단계 역량을 명시하고, network 배치 status를 실제 build_handover에 넘기는 양성 통합 시험을 추가한다. contact/coverage/network 사이 부분집합·금지 묶음 음성 대조도 유지한다.

재현: §5의 probe_g4.py, probe_results.json의 baseline_g4_groups ↔ network_stage_contact_groups.

### RGL-04 · P1 — 새 필수 관문은 게시 뒤 실행되고, 실패 후보는 성공 세대로 남는다

위치: [webapp/app.py:3178](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/webapp/app.py#L3178), [webapp/app.py:3190](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/webapp/app.py#L3190), [webapp/app.py:3238](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/webapp/app.py#L3238), [webapp/app.py:3298](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/webapp/app.py#L3298).

실제 순서는 다음과 같다.

1. 이전 channel-content 검사 통과 → 옛 네트워크 stash 삭제.
2. 새 run_id를 success로 stamp하고 최근 시도도 success.
3. full_metrics에 새 수치·run_id·network_solver_status=success 게시.
4. **그 뒤** 새 network_stop_verdict 실행.
5. 실패해도 failed stage를 붙여 return할 뿐 이전 세대 복구/후보 무효화/실패 시도 기록 없음.

입력 변이 physics boundary_rule=L9에서 실제 helper의 summary는 올바르게 **failed**다. 그러나 active provenance는 success/valid, full_metrics는 success, 옛 세대 marker는 사라졌다. RGL-02의 정상 생산 비관통 결과로도 동일한 게시 상태를 재현했다.

**“실패했는데 done으로 표시된다”는 반례가 아니다.** 배치 앞문은 빨갛지만, 다른 소비자가 읽는 활성 결과와 성공 증서는 실패 후보로 교체됐다는 반례다. L9는 현재 정상 boundary 생산자가 내는 값이 아니라 계약 변이이며, 정상 생산 경로의 발화 예는 앞의 비관통 상태 충돌이다.

최소 수정: 임시 후보의 파일·머지 결과·채널 상태·새 정지 계약까지 전부 검사한 후 활성 세대를 한 번에 승격한다. rollback 대상은 네 망 JSON만 아니라 full_metrics와 provenance도 포함한다. 실패 시 옛 성공 세대를 보존하고 최신 attempt만 failed로 기록한다. batch status를 바꾸는 것만으로는 부족하다.

재현: §5의 probe_contracts.py와 probe_actual_zero.py. 증거: contract_results.json의 stop_gate_failure_after_publication, actual_zero_results.json.

### RGL-05 · P2 — ⑤⑥⑦ 관문의 비유한·필수키·0/N/A 누락 경로

위치: [scripts/lhs_design_dataset.py:1701](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/lhs_design_dataset.py#L1701), [scripts/lhs_design_dataset.py:1708](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/lhs_design_dataset.py#L1708), [scripts/lhs_design_dataset.py:1744](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/lhs_design_dataset.py#L1744), [scripts/lhs_design_dataset.py:1752](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/lhs_design_dataset.py#L1752), [scripts/lhs_design_dataset.py:1762](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/lhs_design_dataset.py#L1762), [scripts/lhs_design_dataset.py:1819](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/lhs_design_dataset.py#L1819), [scripts/lhs_design_dataset.py:2130](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/lhs_design_dataset.py#L2130).

모두 실제 build_handover로 최종 출력까지 확인했다.

| 변이 | 실제 결과 | 실패해야 하는 이유 |
|---|---|---|
| fracture %/index 또는 양수 접촉 면적 mean/total에 NaN | NaN 출력, 해당 2행 검사 수 유지 | abs(NaN)>tol은 False라 잔차 검사 우회 |
| eff_area_perc=-1 | 출력 -1 | 비음수 범위 위반 |
| pulverization=-0.004 % / index=-0.00004 | 허용 | 반올림 반폭 안이어도 물리 범위 밖 |
| f1 h_spread=inf | 허용 | 양수 검사가 유한성 검사를 대신함 |
| se_se_cn 삭제 + aug=-999, f1만 선택 | -999 출력, checked=1/2 | 필요한 독립 근거가 없자 식 검사를 생략 |
| 비관통 행의 percolation_pct 삭제 + eff_area_perc=0.4 | 0.4 출력, area checked=2/2 | A5 판정 근거 누락을 허용 |
| AM_P–AM_P count만 삭제, total=0, mean=0.01 | 최종 count=0, total=0, mean=0.01; 모든 묶음 checked=2 | 검사 뒤 count를 0으로 채워 0접촉 평균 N/A 규칙을 파괴 |

마지막 사례는 count를 **명시적으로 0**으로 남기면 정상적으로 거부된다. 따라서 0접촉 규칙 자체가 아니라 **검사 전 누락→검사 후 0 채움** 순서의 빈틈이다. am_am_n_contacts 누락 시 R3, 선택된 eff_area 자체 누락 시 A4도 생략된다.

- 무너짐: checked 표시를 완비·유한·정합 인계 증서로 해석하는 것.
- 유지: 정상 입력의 식, 반올림 반폭, path_hop_area/상쌍별 파괴/physics 면적의 명시 제외.
- 실제 기존 194행에 NaN 변이가 있다는 주장은 하지 않는다.

최소 수정: 선택 묶음의 원천 근거 열을 먼저 요구하고, 숫자를 유한성→형/범위→식 순서로 검사한다. 개수는 비음수 정수, %는 [0,100], index는 [0,1], 면적은 비음수 등 각 정의를 적용한다. count/mean/total을 함께 정규화한 **최종 레코드도** 검증한다. 상 부재·접촉 0·비관통·기술적 결측을 서로 다른 상태로 유지한다.

재현: §5 probe_g4.py. 세부 결과 키는 evidence_g4/findings.txt와 probe_results.json에 있다. 서로 다른 경로를 한 ID 아래 모았으므로, NaN 하나를 막았다고 전체를 닫으면 안 된다.

### RGL-06 · P2 — Love–Weber 입력 기하와 영 분모가 거짓 정상/거짓 실패를 만든다

위치: [scripts/dem_analysis_core.py:1274](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/dem_analysis_core.py#L1274), [scripts/dem_analysis_core.py:1289](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/dem_analysis_core.py#L1289), [scripts/dem_analysis_core.py:1293](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/dem_analysis_core.py#L1293), [scripts/dem_analysis_core.py:1320](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/dem_analysis_core.py#L1320), [scripts/dem_analysis_core.py:1349](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/dem_analysis_core.py#L1349), [scripts/dem_analysis_core.py:1361](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/dem_analysis_core.py#L1361).

실제 analyze_contacts.load_atoms_raw로 세 입자 CSV를 읽고 실제 LW 함수에 넘겼다. 정상 AM_P 두 입자의 VM은 각각 **0.2148591731740587**(합성 입력 힘/길이² 단위)이고 고립 SE 한 입자의 반경만 NaN이다.

- 반환 status=OK, vm_cv=0.0.
- AM_P mean은 0.2148591731740587인데 ratio=0.0.
- SE mean=NaN인데 ratio=0.0.
- 별도 plate_z=NaN/source=mesh도 OK, plate 접촉 수 0, nowall 요약을 만든다.
- F=0, Fn+Ft=(0,0,-1)인데 힘 분해 오차를 0으로 보고 OK.
- 반대로 진짜 F=0과 c_strs=0의 일치에는 virial 오차=∞, FAILED.

접촉 벡터만 유한 검사하고 원자 위치/반경/부피/판 높이는 빠져 있다. NaN>0이 False여서 요약의 분모 분기가 “0”으로 넘어간다. 영 하중에 상대 오차만 쓰는 것도 양쪽으로 틀린다.

최소 수정: 유한 위치, 양수 유한 반경/부피, 사용하는 periodic 길이/plate 높이를 계산 전에 검증한다. 비유한 tensor/VM에서 정상 통계값을 발행하지 않는다. 힘·virial 검사는 영 척도 분기를 포함한 절대+상대 오차 규약을 두고, 진짜 무하중의 CV/ratio 미정의를 별도 상태로 정의한다.

추가 한정 — **전체 virial 합 1% 검사는 프레임 일치 증서가 아니다.** 동일 기하 AM_P dimer와 SE dimer의 접촉 힘 1,3을 맞바꿔도 합의 오차는 1.23e-16, status=OK지만 AM_P ratio는 0.5→1.5, SE는 1.5→0.5다. 이는 전체 부호/척도 검사의 필요성을 부정하지 않고, 공간·상별 배분을 버린 검사의 증명 범위를 한정한다. atom/contact timestep·원본 hash를 보존하라. 수치적 짝 검사를 강화한다면 구식 50/50 per-atom virial을 접촉력에서 별도로 재구성해 비교할 수 있다. **새 LW와 옛 c_strs를 입자별로 직접 같게 강제하면 안 된다.**

재현: §5 probe_lw_independent.py, 실제 입력 atoms_nan_radius.csv, 최종 로그 probe_lw_independent.parser.stdout.txt. 이 반례는 실침대가 실제로 잘못 짝지어졌거나 NaN이라는 주장과 다르다.

### RGL-07 · P2 — σ만 새로 병합하고 온도 짝은 남겨 τ가 2배가 된다

위치: [webapp/pipeline_service.py:83](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/webapp/pipeline_service.py#L83), [webapp/app.py:3238](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/webapp/app.py#L3238), [scripts/se_material.py:251](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/se_material.py#L251), [scripts/tau_flux.py:94](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/tau_flux.py#L94), [webapp/app.py:6390](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/webapp/app.py#L6390).

NET_MERGE_KEYS는 baseline temperature_provenance와 sigma_grain_S_cm을 소유하지 않는다. 새 망 σ를 병합해도 기존 full_metrics의 온도 factor는 남는다. 공용 τ helper는 그 factor를 새 σ의 짝으로 읽는다.

실제 helper·merge·grade 호출, 새 raw dual은 25 °C/σ₀=3 mS/cm/σ=0.15 mS/cm/φ=0.3로 동일하고, 기존 full_metrics에 factor=4만 남긴 대조:

| 경우 | grade의 짝 σ₀, mS/cm | grade τ² | grade τ | raw dual 기반 τ |
|---|---:|---:|---:|---:|
| 깨끗한 입력 | 3 | 6 | 2.449489742783178 | 2.449489742783178 |
| 옛 factor=4 생존 | **12** | **24** | **4.898979485566356** | 2.449489742783178 |

network stop은 done이다. 실제 retry_network는 contact를 다시 쓰지 않고 이 helper를 부르며, 생성 명령에는 --temp-c가 없어 새 망은 기본 온도 규약이다. 따라서 기존 온도 자료→room-temperature 재시도는 의미 있는 경로다. fixture의 factor=4는 오류를 정량화하기 위한 입력이며 실제 코퍼스에서 그 값을 관측했다는 뜻은 아니다.

**범위 제한:** 깨끗한 신규 LHS는 앞의 contact 분석이 full_metrics를 다시 쓰므로 이 stale 조건을 194건 전부에 적용할 근거는 없다. 식 자체는 맞다. 일반 웹앱/기존 코퍼스 재시도까지 “항상 짝 σ₀”라고 보증하는 부분이 무너진다.

최소 수정: baseline σ·σ₀·온도·모드·세대 정보를 하나의 소유 단위로 지우고 병합하라. 두 모드 짝도 대조한다. 온도→기본 온도 retry와 정상 신규 입력을 실제 helper로 시험한다. 상수 3을 무조건 쓰거나 온도 보정을 제거해 조용하게 만드는 것은 해결이 아니다.

재현: §5 probe_contracts.py의 healthy ↔ stale_temperature_factor4.

### RGL-08 · P2 — network 완료 계약의 입력 집합·파일 대조·null 사유가 불완전하다

위치: [webapp/pipeline_service.py:629](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/webapp/pipeline_service.py#L629), [webapp/pipeline_service.py:696](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/webapp/pipeline_service.py#L696), [webapp/pipeline_service.py:707](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/webapp/pipeline_service.py#L707), [scripts/tau_flux.py:141](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/tau_flux.py#L141), [scripts/tau_flux.py:185](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/tau_flux.py#L185), [scripts/tau_flux.py:198](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/tau_flux.py#L198), [scripts/tau_flux.py:208](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/tau_flux.py#L208).

실제 helper에 소형 solver-output fixture를 제공한 계약 변이 세 종류:

| 변이 | 실제 결과 |
|---|---|
| 모든 망 레코드에서 sigma_full(무차원)·percolating_fraction·temperature_provenance·sigma_grain_S_cm 삭제, dimensional σ는 유지 | network **done**, 이후 tau_flux 두 모드 **NOT_COMPUTED/missing_input** |
| 별도 physics JSON은 σ=99 mS/cm, dual physics는 0.15 mS/cm | network **done**. full_metrics는 dual에서 복사한 0.15 |
| 양수 σ/관통 상태, power share=None, 사유=internal_solver_exception | network **done** |

현재 정상 수치 생산자는 위 입력을 대체로 쓴다. 따라서 이 표는 정상 solver가 현재 99를 만든다는 증거가 아니라 **계약의 누락/불일치 내성 반례**다. 특히 null+임의의 비어 있지 않은 사유 허용은 요청서 §5-2④를 그대로 구현한 결과이므로, 그 항목은 구현 일탈이 아니라 현 명세 자체의 승인 조건 부족이다.

network 완료가 모든 τ를 숫자 OK로 보증해야 한다는 뜻도 아니다. 등록된 BAND_FALLBACK, NOT_PERCOLATING, 연속체 하한 진단 등의 과학적/해석적 HOLD는 허용될 수 있다. **기술적 입력 결손/내부 예외를 그들과 같은 “사유 있음”으로 받으면 안 된다.**

full_metrics↔dual 값 일치는 필요한 복사 검산이다. 그러나 full_metrics를 방금 dual에서 복사했으므로 독립적인 동일 세대 증명은 아니다. 기존 lock/stash/입력 digest/run_id의 의미를 부정하는 것은 아니며, 그것에 mode별 내용 일치를 추가해야 한다.

최소 수정: τ에 필요한 장부와 solver 입력의 의존 집합을 요구하고, 각 상태가 요구하는 값·percolation·전력 사유의 조합을 검사한다. 모든 정상 물리적 null을 금지하지 말고 내부 예외와 구별하라. legacy/Hertz/per-mode/dual 공통 필드를 승격 전에 대조하고 canonical source를 명시한다.

재현: §5 probe_contracts.py의 missing_tau_inputs, permode_vs_dual_disagree, percolating_power_missing.

### RGL-09 · P2 — Spearman의 동률 처리와 상수 벡터 보호가 틀렸다

위치: [scripts/rint03_je_compare.py:57](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/rint03_je_compare.py#L57), [scripts/rint03_je_compare.py:97](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/rint03_je_compare.py#L97).

현재 double argsort는 동률에 평균 순위가 아니라 서로 다른 순위를 준다.

- [1,1,2] vs [1,2,2] → 실제 **1.0**, 평균 순위 Spearman은 **0.5**.
- [0,0,0,0,0] vs 같은 벡터 → 실제 **0.9999999999999999**, Spearman은 **미정의**.
- 현행 selftest 9/9는 그대로 통과한다.

입자 전류의 0·동률은 합법적 입력이다. “순위 유지” 증거를 과대평가할 수 있다. 과거 세 JSON에는 전체 벡터/동률 수가 없어 저자 보고 0.270/0.954가 실제로 틀렸다고 확정하지는 않는다.

최소 수정: 평균 동률 순위 또는 검증된 Spearman 함수를 사용하고 상수 입력은 null+상태로 표시한다. top 10%도 경계 동률 처리 규약을 정한다. 기존 세 순위 수치를 계속 인용하려면 동률 여부를 검산할 자료를 남긴다. AM 마스크 결함과 수정의 논리적 타당성은 이 통계에 의존하지 않는다.

재현: §5 probe_adversarial.py, adversarial_results.json.

### RGL-10 · P3 — “GOLD 8 침대, 비트 동일”은 기존 시험의 증거보다 강하다

위치: [scripts/test_network_boundary_rule.py:53](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/test_network_boundary_rule.py#L53), [scripts/test_network_boundary_rule.py:88](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/test_network_boundary_rule.py#L88).

GOLD 8/8은 **단언 8개**다. 수치 golden은 합성 chain 3개×모드 2개이며 소수 8자리 반올림 후 비교다. 이것만으로 실침대 8개나 원시 bitwise 동일을 주장할 수 없다.

별도로 구식 eedada5d3 원본을 취득해 검사했다. solve_network의 AST는 같고, L0/L1/L2×Hertz/Physics×FULL/bulk-only/constriction-only **18개 비교의 원시 float.hex가 일치**했다. FULL에서 field 산출을 켠 경로도 비교했다. 따라서 시험한 범위에서는 추출 중립성을 지지한다. 실제 전 코퍼스와 물리 모델 검증으로 확대할 수는 없다.

최소 조치: “합성 3종·2모드, 단언 8개”로 시험 설명을 고치고 원시 값 비교를 회귀에 포함한다. 194실침대가 동일했다는 수치는 새로 만들어 쓰지 말 것.

재현: §5 probe_network_independent.py와 그 stdout. 구식 blob SHA-1=2e0c4a47721cd8593b039fe1e189419bbb2eea64.

## 2. RINT claimed_fixed 13건 재판정

“닫힘”은 원래 지적한 결함의 범위다. 모든 인접 물리/숫자 경로가 인증됐다는 뜻이 아니다.

| 원장 | 판정 | 근거·남은 범위 |
|---|---|---|
| RINT-01 | 닫힘 | same-sid 소유 상을 AM_P/AM_S로 파서·API·face 경로에 강제. 비AM의 물려받은 pid를 계면 입자 정체성으로 받지 않음 |
| RINT-02 | **적용 누락 부류 닫힘 / 결과 승인 부분 열림** | 요청에서 기대 표를 만들고 네 솔브별 영수증을 공용 검사. RGL-01은 적용이 아니라 독립 보조 수렴 누락 |
| RINT-03 | 소유권 수정 닫힘 | 최종 sid=AM와 유효 pid의 교집합. 과거 실침대 크기/순위/수렴 증거 한정은 아래 Q2와 RGL-09 |
| RINT-04 | 범위 표지 닫힘 | bulk-only 지도와 계면/plate 제외를 표시. 전체 Joule 지도 구현 완료라는 뜻은 아님 |
| RINT-05 | 명시적 배제 방식으로 닫힘 | r-ON STEP4 저장 거부, reaction solve 비활성. 그 소비자에 계면 물리를 구현했다는 뜻은 아님 |
| RINT-11 | 닫힘 | 새 정의에서 OFF↔zero-table σ/n_dof/je bit 동일. 옛↔새 je는 의도한 세대 예외 |
| RINT-12 | 닫힘 | sid/r 형 검증·bool/문자열 묵시 변환 차단 |
| RINT-13 | 검사한 배선에서 닫힘 | 두 계면 축의 모델 파생, compare-dirs 축 비교, 공용 evidence 소비. 전체 캠페인 판정 재실행은 안 함 |
| RINT-14 | 닫힘 | 모순된 CLI·비활성 채널 요청 거부 |
| RINT-17 | 명명 범위 닫힘 | 단자 R_int와 면적비저항 r_int 구분 |
| RINT-18 | 검사한 라벨 범위 닫힘 | bulk/reaction/phase-interface 범위 설명. 브라우저 시각 QA는 안 함 |
| RINT-19 | 의도한 맥락 재사용 범위 닫힘 | 최종 sid/pid/σ 지문, sid·σ 바꾼 직접 반례 모두 거부. 전체 payload 위조의 인증 경계는 아님 |
| RINT-20 | 닫힘 | 전체 통합시험 49/49 중 실제 off/e_on/ei_on/rxn_on/joule_on/e_zero 6종 manifest 분류 검사 포함 |

주요 소스: [scripts/step3_sigma.py:175](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/step3_sigma.py#L175), [scripts/step3_sigma.py:180](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/step3_sigma.py#L180), [scripts/step3_sigma.py:1216](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/step3_sigma.py#L1216), [scripts/mpm_webapp_payload.py:1376](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/mpm_webapp_payload.py#L1376), [scripts/mpm_webapp_payload.py:1384](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/mpm_webapp_payload.py#L1384), [scripts/mpm_webapp_payload.py:2946](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/mpm_webapp_payload.py#L2946), [scripts/run_contract.py:883](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/run_contract.py#L883). 세부 개별 검사와 라인은 evidence_g1/g1_review.md에 보존했다. 열린 RINT-06–10/15/16의 면적·물리 설계는 이번 판정 범위 밖이다.

## 3. Q1–Q11 답

### Q1. 영수증이 네 AST 변이만 닫는가?

**그 넷보다 넓은 적용 누락/불일치 부류를 닫는다.** 요청표에서 기대값을 파생하고 각 named solve의 실제 적용 영수증을 공용 검사하므로 한 솔브의 정상 model 문자열로 다른 솔브 누락을 덮지 못한다. 다만 “wetted/bare의 모든 실패”를 닫지는 않는다. RGL-01에서 적용은 사실인데 수치 해가 미수렴이다. 요청·적용·수렴·게시 네 계약을 분리해야 한다.

### Q2. r-OFF에서도 je를 바꾸는 예외는 정당한가? 옛 소비자는?

**정당하다.** AM 전류 진단이 최종 AM이 아닌 셀의 전류를 평균하는 것은 계면 모델 ON/OFF와 다른 소유권 오류다.

독립 소형 raster에서 실제 옛 평균은 [0.03831624353328062, 0.037756103759881546], 새 함수는 [0.0003027511154070284, 0.00031217396939968564]. 옛/새=**126.5602, 120.9457배**이며 새 값은 직접 최종 AM mask로 계산한 값과 bit 동일했다. 최종 σ/φ OFF 불변량과 je 정의 세대 전환을 분리해 보존하면 된다.

검사한 step4_dyn은 입자 je/jb를 입력으로 쓰지 않고 grid로 자기 전류를 계산한다. viewer는 v2/legacy/unknown과 A/B 정의 불일치 경고를 갖는다. 단, 입자 CSV export에는 je_definition metadata를 함께 실어야 외부에서 경고를 잃지 않는다. 일부 pre-existing “wetted je” 표시도 main에서 온 canonical je와 맞춰 명명해야 한다. 이는 마스크 수정을 철회할 이유가 아니다.

실침대 보고는 방향과 맞지만 **본 리뷰의 독립 실측은 아니다.** 원본 NPZ 없이 42.6배/97.4%를 재인증하지 않았다. 여기서 “전류 질량”은 합산 cell-current proxy이지 전하/재료 질량이 아니다. 옛 로그에 경고가 없다는 사실은 유한 residual+info=0+unconverged=false tuple을 보존한 증서와 같지 않다. 현재 도구의 비유한/고 residual 차단은 지지하지만 그 보증을 과거 JSON으로 소급하지 말 것. 마스크 수정 정당화를 위해 먼저 대형 세 런을 재실행할 필요는 없고, **과거 정량·순위 수치를 인용할 때** 원본 hash·벡터·수렴 tuple 근거를 보강하면 된다.

### Q3. LW 벽/virial 검사와 대칭부 처리가 충분한가?

**접촉 응력 지표의 정의로는 지지, 자료 승인 관문으로는 아직 불충분하다.**

구현은 id1에 b1⊗F, id2에 b2⊗(-F)를 더한다. 인장 양수 부호에서 압축이 음수이고 대칭부 VM은 올바르다. x/y 최소영상 및 접선 성분 소형 시험도 통과했다. 구식 equal-half virial을 크기 다른 입자에 나눌 때와 달라지는 것은 의도한 정의 전환이다. 이 부호/분배는 공개 LIGGGHTS의 [pair force 생산](https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/master/src/pair_gran.cpp), [virial 집계](https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/master/src/pair.cpp), [stress/atom](https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/master/src/compute_stress_atom.cpp) 경로와 교차 대조했다. 다만 upstream master 확인이 사용한 실제 binary/deck의 버전 증명은 아니다.

대칭부 VM을 쓸 수 있으나 중앙 비대칭 0.0105는 모든 입자의 회전평형·couple stress 부재를 증명하지 않는다. 이름은 **입자 접촉력 기반 대칭 응력의 VM**으로 한정한다. kinetic/wall/couple를 포함한 전체 동적 응력으로 쓰지 않는다.

바닥 z=0·평면 mesh plate·xy periodic인 실제 덱이라면 현재 wall mask는 그 가정과 맞다. 그러나 함수가 덱을 검증하지 않는다. wall 입자 제외는 결측 wall force를 복원하는 것이 아니라 **선별 모집단**을 만든다. contact dump의 pair/mesh wall 범위도 다르므로 [공개 compute 문서](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/master/doc/compute_pair_gran_local.txt)와 실제 dump 생성 명령을 연결해야 한다.

전체 diagonal virial 1%는 전역 부호/척도 검사로 남기되 frame 대응 증명이라고 부르지 말 것. RGL-06의 입력·영 분모 문제를 먼저 닫는다. real14 CV=120.7%/AM_P=2.737은 본 리뷰에서 재생산하지 못했다.

### Q4. 전극 간선 제외와 비관통 None은?

**동의.** 추정량이 “같은 FULL 해에서 물리 간선 내부의 협착 소산 몫”이면 가상 전극 간선의 소산을 분자·분모 모두에서 빼는 것이 맞다. 관통이 없으면 이 몫은 0/0이므로 None+사유이고 0%가 아니다.

독립 두 병렬 경로 (Rb,Rc)=(1,9),(1,0), 서로 다른 양 끝 물리 노드에서 actual=**0.09167871335514417**, 유한 전극 연결까지 포함해 같은 전류를 구한 해석값=**0.0916787133551442**였다. 물리 간선 소산 0.9094044479454131 + 전극 소산 0.06007501223551508 = 입력 0.9694794601809258 (저항 Ω·주입 1 A인 합성 회로에서 W).

한정: **전극 소산 제외 ≠ 전극 조건에 무관.** 이상 전극 극한은 9/110=0.08181818181818182이고 현재 값은 그보다 12.05% 크다. 전극 저항이 물리 간선의 전류 배분을 바꾼다. C1c의 일반적 “boundary-independent” 표현은 줄이고 FULL boundary에 조건부라고 명시하라. 이것은 새 power-share 식의 오류는 아니다.

### Q5. GOLD 8만으로 추출 중립성이 충분한가?

**그 설명대로는 아니다.** 8은 침대 수가 아니고 반올림값 비교다. RGL-10의 추가 원시 18/18 비교와 변경 전후 코드 구조는 검사 범위에서 중립성을 뒷받침한다. 수치 모듈 hash가 바뀌었다는 사실은 남으므로 재봉인 의무가 사라지지 않는다.

L0는 입자별 반경을 쓰므로 기록한 r_max 기반 band_frac는 단일 균일 slab의 실제 두께가 아니라 상한형 진단이다. L1/L2 fallback 표지는 유지해야 한다. 검증 범위를 전 코퍼스/물리 정확도로 확대하지 말 것.

### Q6. 반올림 반폭·0접촉·명시 제외는 충분한가?

**정상 정의와 제외는 지지하지만 승인 관문은 RGL-05 때문에 HOLD다.**

- 0.005 %p와 5e-5는 각각 round(...,2), round(...,4)의 반폭이다. 실제 경계는 통과, 0.005001 및 0.00005001은 거부했다.
- 독립적으로 검증된 접촉 0은 total=0, mean=N/A가 맞다. **상 자체가 없음**은 total도 N/A로 구별한다.
- 선별 path_hop_area를 전체 접촉 면적으로 쓰지 않는 것, max(n,1) 분모의 상쌍 파괴·physics 면적을 이번 인계에서 제외하는 것은 타당하다. census에서 승인해도 WA_EXCLUDED가 먼저인 10개 음성 대조를 통과했다.
- 위 규칙은 필수키 누락/NaN/부분 0채움 모순을 허용할 근거가 아니다.

### Q7. 정지 위치·내용 계약·동일 세대 판정은 충분한가?

위치는 맞다. 실제 기존 227/227 회귀는 Stage E/후속 분석을 돌리지 않는 것, full 실행 앞부분과 명령 인자가 같은 것, atoms-only 차단·mode 보존 금지를 확인한다.

내용과 게시 순서는 **충분하지 않다**. RGL-02의 생산 상태 모순, RGL-03 후속 생성기, RGL-04 게시 순서, RGL-08 입력/파일 정합성부터 풀어야 한다. 값 일치는 복사 검사이고 generation 증명 전체가 아니다. 원 run_id/digest/lock을 유지하면서 canonical 모드 기록·짝 σ₀·장부·상태 일관성을 함께 검사한다. τ가 물리적으로 미정의인 경우와 기술적으로 못 만든 경우를 분리한다.

### Q8. 재봉인 순서는?

**수정 → 통합 게이트 → 필요한 등록 개정/봉인 → 그 봉인으로 배치** 순서에 동의한다. 배치를 먼저 돌리면 결과가 선언된 numeric module hash에 연결되지 않거나, 나중에 바뀐 봉인을 이미 본 결과에 소급하는 문제가 생긴다. 지금 G5 HOLD인데 봉인만 새로 만든다고 닫히지 않는다.

주의: [scripts/seal_s3_prerun.py:430](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/seal_s3_prerun.py#L430), [scripts/seal_s3_prerun.py:516](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/30c8205c5efb3873ae6fa856881fa184bd041d4d/scripts/seal_s3_prerun.py#L516)에는 **2026-09-17 23:59 KST cutoff와 frozen inventory** 규칙이 있다. 현재는 10-05다. “재봉인”을 이유로 날짜를 옮기거나 --now 시험 인자를 써 새 코호트를 조용히 만드는 절차를 권하지 않는다. 기존에 허용된 frozen inventory/기준선의 연속성을 유지하고, 현 규약으로 재봉인이 안 되면 **저자 승인된 별도 amendment**로 code hash 전환과 결과 열람 시점을 남겨라. 이번 리뷰에서는 봉인 명령을 실행하지 않았다.

### Q9. τ/COMSOL 통일은 닫히는가?

올바른 입력에서 **등급/COMSOL 해당 기준의 수식·getter 통일은 닫힌다**. 이 기준에서 f=σ_mode/σ₀, τ²=φσ₀/σ_mode, τ=√τ²이고 σ와 σ₀를 함께 ×4하면 f·τ²는 불변이다. 별도의 tau_flux 인계 f에는 L_gap/L_mc 장부에 따른 길이 기준 변환이 있으므로 모든 f 열이 이 단순식으로 같다는 주장은 아니다. 두 mode row를 구별하고 Stage-E에 τ 이름을 붙이지 않으며 짝 아님을 경고한 구성은 지지한다. σ_P가 없을 때 Hertz 복사가 일어나지 않는 시험도 통과했다.

하지만 실제 producer→full_metrics 온도 짝은 RGL-07에서 무너진다. 한 helper를 쓴다는 사실만으로 서로 다른 세대의 σ와 σ₀가 같은 세대가 되지는 않는다. 따라서 결정 6의 식 정리는 완료, 일반 배포 경로의 완전 닫힘은 HOLD다. COMSOL/브라우저를 직접 실행해 사용자의 입력 오용까지 검증한 것은 아니며, 코드·export 경로·시험의 범위다.

### Q10. 그 밖의 P1은?

RGL-01–04 네 건이다. 특히 “새 관문에 실패했으므로 안전하다”는 반론은 RGL-04에 답이 되지 않는다. 실패 표시와 활성 수치 세대가 서로 어긋나는 것이 문제다. P2인 온도 혼합도 재시도에서 실제 과학 수치를 바꾸지만, 요청된 깨끗한 신규 LHS194 경로에 대한 일반화를 피하려고 이번 표에서는 P2로 한정했다.

### Q11. not_computed 거부 / preserve_network 금지

- (가) **현행 일괄 거부에 반대.** 못 풂을 거부하는 목표는 맞지만 producer의 not_computed에 정상 no-through도 들어간다. RGL-02처럼 생산자부터 상태를 세분하고 검증된 비관통만 받아라. 빈 문자열 사유 하나나 valid_null 자기 표지만으로 받지 않는다.
- (나) **동의.** 이번 실행의 새 망을 요구하는 stop_after=network에서 preserve_network를 금지하는 것은 run_id 계약과 정합한다. 보존 전용 점검을 원하면 별도 읽기 전용 검증 동작으로 명시하면 되고, fresh 실행인 것처럼 섞지 않는다.

## 4. 실제 커밋 194행의 제한적 산술 검산

원자료: 고정 커밋 docs/data/lhs_webapp_contact_d1ec42fba/metrics_flat.csv 및 lhsx_webapp_contact_d1ec42fba/metrics_flat.csv. 읽기 전용으로 실제 G4 helper를 호출했다.

| 검산 | LHS 130 | LHSX 64 |
|---|---:|---:|
| 관문 통과 | 130/130 | 64/64 |
| 단계 % 최대 절대 잔차, %p | 0.004996359898939318 | 0.004978165938864687 |
| fracture index 최대 절대 잔차 | 4.935064935064626e-5 | 4.8484848484848034e-5 |
| F1 최대 상대 잔차 | 2.178081687703956e-16 | 2.0539004373289635e-16 |
| A4 최대 상대 잔차 | 1.8874990180689866e-12 | 2.2096496364960295e-12 |
| 명시 0접촉 쌍 사례 수 | 3 | 6 |
| 비관통 행 수 | 24 | 0 |

force_total=am_am_n_contacts는 194/194 일치. 130의 N_SE는 별도 descriptor JSON과 130/130 대조했다. 64의 N_SE는 생산 CSV 열이며 독립 원 dump 계수가 아니다. r_SE는 화면 반올림값이 아니라 inp.r_SE×10⁶/meta.scale로 복원했다.

이 검산은 **현재 저장된 정상 표의 산술은 맞는다**는 증거다. 반례 입력을 관문이 차단한다는 증거와 다르며, RGL-05를 상쇄하지 않는다. 194행을 새로 수확하거나 값을 배포하지 않았다.

## 5. 재현 명령과 증거

아래는 이 리뷰 폴더 기준 Windows PowerShell 명령이다. 패키지를 옮기면 R/W/P와 의존성 경로만 조정한다. Python 3.12, NumPy/SciPy 및 웹앱/plot 의존성이 필요하다. 소스 snapshot은 Git checkout이 아니며 git checkout/fetch 없이 검증했다.

~~~powershell
$W='C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20'
$R="$W/rint_g1_lhs_network_review_20261005"
$P='C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONPATH="$W/lhs_coverage_review_20260930/deps;$W/audit_review_evidence_20260909/pydeps;$R/source/scripts;$R/source/webapp"
$env:MPLCONFIGDIR="$R/evidence_g56/mplcache"

# 원 소스 223파일의 Git blob + SHA-256 검증
& $P "$R/verify_snapshot.py"

# RGL-01/09, r-OFF AM 마스크. 실제 작은 payload producer + check-arm
& $P "$R/evidence_g1/probe_adversarial.py"

# G2 LW 입력/virial, G3 전력/비관통/18개 구식·신식 비교
& $P "$R/evidence_g23/probe_lw_independent.py"
& $P "$R/evidence_g23/probe_network_independent.py"

# RGL-03/05: 실제 build_handover 입력 변이
& $P "$R/evidence_g4/probe_g4.py"
# G4 baseline + 커밋된 194행 요약표 helper 검산
& $P "$R/evidence_g4/replay_g4.py"

# RGL-04/07/08: 실제 helper/merge/grade, solver 파일 작성만 fixture
& $P "$R/evidence_g56/probe_contracts.py"
# RGL-02/04: 실제 작은 비관통 망 산출을 위 helper에 전달
& $P "$R/evidence_g56/probe_actual_zero.py"
~~~

probe_g4 결과는 길다. 전체 입력·출력·예외는 probe_results.json, 식별별 요약은 evidence_g4/findings.txt에 있다. 모든 반례는 정상 양성 대조와 분리했다. 운영 원자료에 변이를 심지 않았다.

기존 시험 재현:

~~~powershell
& $P "$R/evidence_g1/run_baselines.py"
& $P "$R/evidence_g56/run_baselines.py"

# 아래 둘은 환경 적응판임을 명시 — native/WSL 실행 증서가 아니다
& $P "$R/evidence_g56/environment_adapters.py" labels
& $P "$R/evidence_g56/environment_adapters.py" batch
~~~

G2/G3의 원 CLI 명령·환경·최종 stdout은 evidence_g23/test_run_metadata.final.json에, G4는 evidence_g4/cli_metadata.json에 있다. source 아래의 원 test 파일은 수정하지 않았다. 운영 deps를 새로 설치하지 않았다.

## 6. 원 시험 재실행 결과 — 초록과 미확인을 분리

환경: Windows 11, Python 3.12.14, NumPy 2.3.5, SciPy 1.16.3, Flask 3.1.3. plot 의존성은 별도 기존 환경에서 가져오되 NumPy/SciPy 검색 순서를 고정했다.

| 원 시험 | 결과 | 한정 |
|---|---|---|
| step3_sigma --selftest-rint | 90 OK / PASS | 작은 수치/계면 회귀 |
| test_rint_receipts | 49/49 | 원 4개 적용 누락 변이 포함 |
| rint03_je_compare --selftest | 9/9 | 동률 반례는 기존 시험 밖 |
| test_love_weber_stress | **37/38 실행 단언** | real14 입력 부재로 한 그룹 실패. 그 그룹은 원래 5개 단언으로 확장되므로 42/42를 재인증하지 못함 |
| test_constriction_power_share | 16/16 | 독립 회로 검산 추가 |
| test_network_boundary_rule | 8/8 | “8개 침대” 아님 |
| lhs_stress_constriction_audit --selftest | 9 PASS | 합성 시험 |
| test_stress_lw_labels | 33/33 | 라벨 검사 |
| test_constriction_power_labels | 21/21 | 라벨 검사 |
| lhs_design_dataset --selftest | 233/233 | 새 독립 입력 변이에서는 RGL-03/05 발생 |
| test_s567_labels | 13/13 | 라벨 검사 |
| test_tau_flux | 35/35 | K3 생산 상태가 새 stop 관문과 충돌 |
| test_tau_grade_unify | 19/19 | 짝진 입력의 식/소비자 통일 |
| test_tau_handover_status | 16/16 | 추가 라벨·상태 시험 |
| grade_engine --selftest | PASS | 출력이 고정 단언 총수를 제공하지 않음 |
| test_pipeline_provenance | 227/227 | 독립 새 관문/게시 순서 반례는 기존 시험 밖 |
| test_tau_labels | native 39 PASS/4 FAIL → **환경 적응판 43/43** | 아래 설명 |
| lhs_webapp_batch --selftest | native 환경 오류 → **환경 적응판 39 PASS** | 아래 설명 |

환경 예외를 생산 결함으로 세지 않았다.

1. real14 atom/contact gz는 연결 도구가 바이너리 본문을 주지 못했다. 파일을 빈 값으로 대체하지 않았다. 기대 Git blob은 atom ee206e15b9ff9457d0547d099c9249054b7171d2, contact a3e41f709cce79a5ef5e058d6bb8d39cd9c3ff81이다. 해당 실제 fixture 회귀는 사용자 환경에서 남아 있다.
2. standalone snapshot에는 .git가 없어 라벨 검사의 HEAD:columns.tsv 네 바이트 비교만 실패했다. 프로세스 안에서 **네 원본 blob hash를 먼저 대조한 파일 바이트**로 그 읽기만 대체하니 43/43이었다. 실제 저장소 HEAD가 이 커밋임을 검증한 시험이라고 부르지 않는다.
3. batch 시험은 Windows symlink 권한 WinError 1314 때문에 멈췄다. 임시 불변 파일의 symlink 생성만 hardlink로 바꾼 적응판에서 39 PASS였다. native symlink/WSL 차이는 검증하지 못했고 WSL 접근도 E_ACCESSDENIED였다. 실제 WSL 양성 시험이 별도로 필요하다.
4. 위 대체는 리뷰 harness 프로세스 안에서만 이루어졌고 고정 소스는 바꾸지 않았다. 초기에 의존 파일 부족으로 실패했던 로그와 최종 재실행을 혼동하지 말 것. final/adapter 로그를 기준으로 한다.

따라서 “전부 초록을 독립 재현했다”는 문장은 쓰지 않는다. **원 시험이 초록인 범위에서도 이번 반례는 살아 있다.**

## 7. 실행 전 최소 해제 목록

1. wetted/bare의 실제 미수렴을 각각 producer와 공용 check-arm이 거부하고, 정상 대조는 통과할 것. 주 솔브 PASS만으로 대체하지 말 것.
2. **실제 producer→stop gate→tau**로 관통·정상 비관통·수치 실패를 구별할 것. valid_zero 문자열을 손으로 넣은 양성 fixture만으로 닫지 말 것.
3. 새 network 배치 status를 실제 build_handover에 넘겨 ⑤⑥⑦ 인계가 성공하고, 금지 묶음/누락/잘못된 상태는 거부할 것.
4. required stop 관문 실패 시 옛 네 JSON·full_metrics·active provenance를 보존하고, latest attempt만 실패로 남길 것. first run 실패에서는 활성 success가 없어야 한다.
5. G4의 비유한/범위/필수 근거/부분 null 변이와 LW의 원자 기하·plate·영 분모 반례를 모두 막을 것. 정상 194행 요약표 산술 대조도 유지할 것.
6. τ 입력의 완비성과 상태 조합, per-mode↔dual 일치, σ↔σ₀ 온도·세대의 소유/병합을 보증할 것. 깨끗한 신규 run과 옛 온도→기본 온도 retry를 구분해 시험할 것.
7. 기존 순위 수치의 사용 범위를 정하고 Spearman 동률 오류를 수정할 것. “GOLD 8 침대” 및 “전극 영향 없음” 표현을 정정할 것.
8. 실제 WSL 환경의 작은 양성/음성 통합 회귀와 사용 가능한 real14 fixture 회귀를 마친 뒤, 기존 frozen inventory/cutoff를 침범하지 않는 봉인 절차를 적용할 것. **이 판정은 194건 실행 또는 새 봉인 생성을 승인하지 않는다.**

한 번에 새 물리 모델·계수·코호트를 바꾸라는 요구가 아니다. 현재 요청의 핵심인 **정의 → 생산 상태 → 게시 → 인계 소비의 연결**을 같은 작은 실제 함수 경로로 닫으면 된다.

## 8. 산출물 안내

- 본문: codex_review_rint_g1_lhs_network_20261005.md
- source_manifest.json: 223파일 원 Git blob/SHA-256 확인과 미확보 바이너리 명세.
- evidence_g1/: r_int 실 producer·check-arm, 마스크·순위 반례, baseline.
- evidence_g23/: LW parser/함수 반례, 전력 회로·경계 비교, 구식 원본/취득 증거.
- evidence_g4/: 인계 반례·194행 산술·원 test 로그.
- evidence_g56/: 실제 정지 helper·게시·τ 짝 반례 및 환경 적응판.
- package_manifest.json: ZIP에 넣은 파일별 SHA-256. ZIP 자체 무결성은 ZIP 옆 package_receipt.json에 별도 기록.
- findings_review.json: 이 리뷰의 finding ID/등급/게이트. **리포의 원장을 수정한 것이 아니다.**

검토용 사본·재현 도구·로그만 작성했다. 생산 수정/실행은 하지 않았다.

**최종: HOLD.**
