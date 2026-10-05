# RGL 수정 재검증 판정

기준 커밋: `bf4fb6aee0b388375ddf65694ac405e63e0e381c`  
브랜치: `claude/sdcp-dem-manuscript-si-pqwtv8`  
요청: 이전 판정 §7 해제조건 1–7 및 Q1–Q7. 검토일 2026-10-05.

**판정: HOLD. 기존 P1 네 건은 원래 반례와 해당 경로 기준으로 닫혔다. 새 P1은 없으며, 해제조건 5·6에 걸리는 P2 반례 세 건이 남는다.** RGL-06과 RGL-08은 부분 닫힘이다. 이전에 공개한 WEB-03·LHS-33을 새 발견으로 세지 않는다.

이는 194건 실행·새 봉인·WSL 통합·real14 실데이터 회귀의 승인 요청이 아니다. 그 작업은 수행하지 않았다. 생산 코드·Git 상태·원장은 변경하지 않았다. 별도 검토용 사본과 소형 합성 함수/CLI 실행, 이미 커밋된 요약 자료의 검산만 수행했다.

## 1. 해제조건 판정

| 이전 §7 | 판정 | 독립 재현과 한정 |
|---|---|---|
| 1 보조 미수렴 | **닫힘** | 기존 탐침을 출력 없는 새 디렉터리에서 실행. 정상 producer rc 0·check-arm 0·R_geom 0.0 Ω·cm². wetted만, bare만, main만 CG 제한 시 각각 rc 3·정상 payload 미게시. 정상 보조 잔차 9.783687086144589e-09. 비유한 잔차도 경고·unconverged=True. |
| 2 실제 producer→stop→τ | **닫힘** | 실제 network CLI와 실제 app helper로 관통=done/OK, 비관통=done/NOT_PERCOLATING/f=0, 관통 풀이 실패=failed/NOT_COMPUTED. 일반 Stage E 경로는 별도 WEB-03으로 남는다. |
| 3 network 배치→인계 | **닫힘** | 끝-끝 시험 10/10. 130·64 기존 요약자료를 실제 build_handover에 전달해 contact와 network 상태의 표·열이 동일. 이 시험은 망 고유 τ·전력 열의 ML 인계까지 증명하지 않는다. 그 열은 아직 대상 묶음에 없다. |
| 4 required stop 거부 시 보존 | **닫힘 — 해당 실패 경로** | 정상 세대 뒤 후보 sigma_full_status를 not_computed로 변조하면 failed. 옛 네 JSON·full_metrics·active provenance **6/6 파일 SHA-256 동일**. first run 실패는 활성 세대 없음. 예외/게시 중단의 원자성까지 닫혔다는 뜻은 아니다. Q2 참조. |
| 5 G4·LW 반례 | **부분** | 기존 G4 결함 변이와 LW 반경 NaN·plate NaN·영 척도 반례는 막힘. 194행 요약 산술 유지. 그러나 실제 CSV 파서가 손상된 c_strs를 전무로 바꾸는 **RGLR-03**이 남음. |
| 6 τ 입력·세대·온도 짝 | **부분** | 기존 누락/파일 간 모순/온도 retry 반례는 막힘. 그러나 BAND_FALLBACK이 무효 σ를 가리는 **RGLR-01**, 차원·무차원 σ의 내부 불일치를 받는 **RGLR-02**가 남음. |
| 7 순위·문구 | **닫힘** | 동률 Spearman 0.5, 상수 None/constant_input. 옛 실침대 순위 값은 잠정으로 한정. 원시 18비교 모두 hex 동일; 유한 전극의 전력 몫 영향 +12.0517607674%도 독립 재현. |

### RGL 항목별

| 원장 | 판정 | 무엇이 닫혔고 남았는가 |
|---|---|---|
| RGL-01 P1 | 닫힘 | 보조 두 솔브의 개별 수렴과 게시 거부, 공용 소비자 재검. |
| RGL-02 P1 | 닫힘 | 정상 비관통과 solve_failed의 생산 상태 분리 및 network 정지 경로. |
| RGL-03 P1 | 닫힘 | network 단계 역량 인식과 실제 인계 생성기 연결. |
| RGL-04 P1 | 닫힘 | 기존 stop 계약 거부의 선검사·복원. 예외 중 게시 문제는 이미 공개한 WEB-03으로 유지. |
| RGL-05 P2 | 닫힘 | 기존 유한성·범위·필수 근거·정규화 반례. 합법 0접촉과 반올림 경계 양성 대조도 유지. |
| RGL-06 P2 | 부분 | 직접 함수의 기존 반례는 닫힘. 파서→함수 결합에서 RGLR-03. 프레임 대응은 미인증. |
| RGL-07 P2 | 닫힘 | 옛 온도 메타가 새 σ에 남는 구체적 병합 결함. 수치 표현 간 항등식은 별도 RGLR-02. |
| RGL-08 P2 | 부분 | 전 레코드 복사 일치·실 소비자 호출은 개선. 과학적 HOLD 앞 입력 검증과 표현 간 수치 일치는 불완전. |
| RGL-09 P2 | 닫힘 | 동률·상수·top-k 경계 상태. 과거 세 JSON의 올바른 순위 값은 재계산하지 못함. |
| RGL-10 P3 | 닫힘 | 8 단언과 8 침대 구별, raw 비교와 전극 한정어 정정. |

“닫힘”은 열거한 결함의 재현 범위에 한정한다. 이 스택 전체의 무결함 인증이나 실데이터 값 인증이 아니다.

## 2. RGLR-01 P2 — 과학적 fallback이 기술적 손상을 통과시킨다

**무너지는 주장:** network 완료가 “τ 입력이 완비되고 유효하며, 남은 null은 등록된 과학적 HOLD뿐”이라는 증서라는 주장.

위치: [pipeline_service.py:815](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/webapp/pipeline_service.py#L815)·[동일 파일:877](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/webapp/pipeline_service.py#L877), [tau_flux.py:192](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/scripts/tau_flux.py#L192)·[동일 파일:208](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/scripts/tau_flux.py#L208).

실제 producer로 L1 밴드 침대를 계산한 뒤, 모드 파일·legacy·dual의 같은 필드를 모두 함께 변조했다. 파일 간 불일치로 쉽게 잡히는 반례가 아니라 **같은 잘못된 레코드가 소비자들에 전달되는 경우**다.

| 변이 | 실제 stop 결과 | τ 결과 |
|---|---|---|
| 정상 L1, sigma_full=0.00089265 | done | BAND_FALLBACK |
| sigma_full=None | **done** | BAND_FALLBACK |
| sigma_full=NaN | **done** | BAND_FALLBACK |
| sigma_full=-1 | **done** | BAND_FALLBACK |
| percolating_fraction=2 | **done** | BAND_FALLBACK |

앞의 네 경우에서 차원 σ는 모두 0.002678 mS/cm이고 상태는 computed다. 정상 L1은 받아야 한다. 하지만 computed인 동일 레코드의 무차원 σ가 없거나 음수·비유한인 경우까지 “과학적 HOLD”로 받으면 안 된다.

원인: stop 검사는 sigma_full 키의 존재와 차원 σ의 양수를 보고, tau_flux가 반환한 BAND_FALLBACK을 허용한다. 소비자는 L1/L2에서 즉시 반환하므로 뒤의 무차원 σ 검증에 도달하지 않는다. 관통 분율도 현재는 >0만 검사하여 2를 받는다. 따라서 소비자 호출 자체가 전체 입력 검증을 대신하지 못한다.

**최소 처방:** 밴드 판정과 독립적으로 기술적 유효성 검사를 먼저 한다. computed의 두 σ는 유한 양수, 관통 분율은 (0,1], 증명된 비관통은 기존 valid_zero 조합이어야 한다. L1/L2라는 이유로 무효값 검사를 생략하지 않는다. 등록된 과학적 HOLD의 허용 자체는 유지한다. tau_flux의 과학적 게이트 순서를 무단으로 바꾸기보다 공용 입력 validator를 앞에 두는 방법도 가능하다.

**해결 증거:** 정상 L1·L2와 정상 비관통은 통과, 위 None/NaN/음수/분율>1 각각은 게시 전 거부, retry에서는 옛 세대 보존. 정지 helper와 독립 tau 소비 양쪽 시험이 필요하다.

재현: `python3 run_probes.py new_network` → `evidence/network_adversarial.json`의 `band_*` 레코드.

한정: 현 운영 코퍼스에 이 손상이 존재한다는 증거는 아니다. 명시한 입력 계약을 실제 경로가 보증하지 못한다는 반례다.

## 3. RGLR-02 P2 — 같은 세대에도 두 σ 표현이 서로 다른 값을 말할 수 있다

**무너지는 주장:** σ₀·온도·파일 복사 일치만으로 화면/등급 τ와 인계 τ가 같은 물리량을 표현한다고 보증할 수 있다는 주장.

위치: 생산 식 [network_conductivity.py:1259](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/scripts/network_conductivity.py#L1259), 소비 [tau_flux.py:75](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/scripts/tau_flux.py#L75)·[동일 파일:212](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/scripts/tau_flux.py#L212), 검사 [pipeline_service.py:818](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/webapp/pipeline_service.py#L818)·[동일 파일:890](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/webapp/pipeline_service.py#L890).

실제 L0 관통 생산본에서 sigma_full만 네 JSON 전체에 걸쳐 4배로 만들었다. sigma_full_mScm·sigma_grain_S_cm·온도·상태·파일 간 일치는 그대로다.

| 양 | 정상 | 변이 후 |
|---|---:|---:|
| sigma_full 무차원 | 0.00400388 | 0.01601552 |
| sigma_full_mScm | 0.012012 mS/cm | 0.012012 mS/cm |
| σ₀ | 3.0 mS/cm | 3.0 mS/cm |
| 인계 tau2_ion_hertz | 10.984918916215548 | **2.746229729053887** |
| 화면/등급 공용 tau2_from_metrics | 10.984589697866410 | **10.984589697866410** |
| stop 결과 | done | **done** |

정상 두 τ의 미세 차이는 등록된 8자리/6자리 반올림 차이다. 변이 후 약 4배 차이는 그 차이가 아니다. 이 침대는 L_gap=L_mc이고 같은 φ 장부를 쓰므로 두께 기준 차이도 아니다.

생산자는 같은 해에서
`σ_dim[mS/cm] = sigma_full × sigma_grain_S_cm × 1000`
을 만든다. 새 검사는 파일 사본들의 동일성과 σ₀ 메타의 동일성을 검사할 뿐 이 표현 간 식을 검사하지 않는다. 복사 검사는 독립 수치 검산이 아니다.

**최소 처방:** 반올림 구간을 고려한 표현 간 항등식 검사. q=sigma_full, s₀=sigma_grain_S_cm라면 현재 저장 정밀도에서 우선
`abs(σ_dim − 1000*s₀*q) ≤ 5e-7 + 1000*abs(s₀)*5e-9 + 부동소수 여유`
라는 절대 오차 경계가 성립해야 한다. 이는 현재 생산자의 소수 6자리·8자리 반올림에 대한 경계이며, 새 물리 허용오차를 도입하는 제안이 아니다. s₀가 별도 반올림되는 세대라면 그 오차항도 따로 포함해야 한다.

**해결 증거:** 원 생산본의 작은 σ와 온도 변환 양성 대조가 통과하고, ratio만/차원값만 변조한 두 방향이 거부될 것. 두 모드를 모두 검사할 것. 단순히 두 τ를 항상 exact equality로 맞추면 반올림·기준 변환을 오차로 오인한다.

재현: 같은 `new_network` 탐침의 `positive`와 `ratio_times4`.

한정: σ 풀이값 자체를 잘못 계산한다고 증명한 것은 아니다. 이번 요청의 “완료 증서가 소비자 간 일관성을 보증한다”는 범위의 잔여 결함이다.

## 4. RGLR-03 P2 — 존재하지만 손상된 c_strs가 파서에서 없어져 LW 검사가 꺼진다

**무너지는 주장:** c_strs가 제공된 입력은 전부/전무·유한성 검사를 반드시 거친다는 주장.

위치: [analyze_contacts.py:39](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/scripts/analyze_contacts.py#L39)·[동일 파일:50](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/scripts/analyze_contacts.py#L50), [dem_analysis_core.py:1286](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/scripts/dem_analysis_core.py#L1286)·[동일 파일:1342](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/scripts/dem_analysis_core.py#L1342)·[동일 파일:1420](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/scripts/dem_analysis_core.py#L1420).

두 구의 실제 CSV를 load_atoms_raw로 읽고 calc_love_weber_stress에 전달했다. 일관된 임의의 sim 단위에서 반경 1, 중심 간격 1.8, 힘 크기 1인 합성 dimer다. 올바른 입자별 z virial은 -0.9(힘×길이 단위)다.

| 입력(특기 외 실제 CSV) | 실제 결과 |
|---|---|
| c_strs=(0,0,-0.9), 두 입자 | OK, virial 상대 잔차 1.2335811384723962e-16 |
| c_strs=(0,0,-2.7), 두 입자 | FAILED, virial 상대 잔차 약 **0.6666666667** |
| c_strs=(NaN,0,-2.7), 두 입자 | **OK**, virial_status=`unavailable (no c_strs in atom dump)` |
| c_strs 첫 열이 문자열 invalid | **OK**, 똑같이 전부 없는 것으로 처리 |
| c_strs 첫 열이 Inf | FAILED, non_finite c_strs |
| sigma 세 키가 모두 없는 직접 dict 양성 대조 | OK, unavailable — 이 호환 규약 자체를 반박하는 것은 아님 |

문자열은 pd.to_numeric(errors='coerce')에서 NaN이 된다. 첫 성분이 NaN이면 파서는 세 sigma 키를 모두 쓰지 않는다. 이후 함수는 모든 입자에서 세 키가 없다고 판단하여 “입력 없음” 분기로 간다. 잘못된 virial -2.7을 -0.9와 대조하던 검사조차 꺼진다.

직접 dict 입력에서도 모든 입자에서 sigma_xx만 지우고 나머지 둘을 남기면 has_cs가 전부 False가 되어 같은 우회가 생긴다. has_cs=`all(세 키)`만으로는 “아무 키도 없음”과 “불완전한 튜플”을 구별하지 못한다.

**최소 처방:** 원 CSV의 열 존재·행 결측·파싱 실패를 보존한다. 세 원천 열이 전부 없을 때만 미제공으로 분류하고, 일부만 있거나 열이 있는데 유한 수치가 아니면 invalid_input으로 거부한다. 함수 직접 호출도 any-present와 all-complete를 별도로 검사한다. 진짜 열 전무인 옛 입력을 손상 입력과 함께 금지할 필요는 없다.

**해결 증거:** CSV→실 파서→LW로 정상/원천 열 전무/일부 열/NaN/문자열/Inf를 시험할 것. 수치 튜플을 손으로 만들어 함수만 호출하는 회귀로는 이 경로가 닫히지 않는다.

재현: `python3 run_probes.py independent_lw` → `evidence/lw_replay.json`의 `finite_wrong_virial`·`nan_hides_wrong_virial`.

한정: 이 반례에서 접촉력으로 계산한 LW 값이 자동으로 틀려지는 것은 아니다. 손상된 독립 대조 입력을 숨겨 `checks_v2 / OK`를 받는 것이 결함이다. LHS-33의 옛 stress_cv=0 문제와 별개로 새 LW 경로에도 영향을 준다.

## 5. Q1–Q7 답

### Q1 일반 경로의 관통 풀이 실패

**거부해야 한다.** 비관통/상 부재와 관통 풀이 실패는 서로 다른 상태다. 이온뿐 아니라 실제로 계산하도록 요청한 전자·열 채널도 같은 원칙으로 정리해야 한다. 관통 실패를 valid_null로 만들어 필수 단계 success를 유지하지 말 것.

실제 network CLI에 spsolve 예외를 넣으면 정지 경로는 failed지만 일반 helper의 사전 게이트는 통과한다. 탐침에서 일반 경로는 Stage E를 테스트 대역으로 바꿨고, 그때 helper는 done·network success·τ NOT_COMPUTED가 되었다. **실 Stage E 수치 결과를 재현했다는 뜻은 아니다.** 실패 망이 Stage E 앞에서 차단되지 않는다는 검증이다. 위치: [network_conductivity.py:1440](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/scripts/network_conductivity.py#L1440), [app.py:3265](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/webapp/app.py#L3265).

이미 공개한 WEB-03의 확인이며 새 P1로 세지 않는다. 새 연구설계가 아니라 실패 상태 계약을 일치시키는 일이다.

### Q2 실패 처리 두 갈래와 게시 중 예외

**상태 모델을 하나로 맞추는 것을 권고한다.** 마지막 유효 세대는 값·도장·성공 상태를 함께 보존하고, 이번 실패는 별도 attempt에 stage/reason/입력 ID와 함께 기록하는 모델이 더 명확하다. 화면은 “이전 성공 값, 최근 재계산 실패”를 둘 다 표시해야 한다.

현재 solver rc 실패는 full_metrics.network_solver_status를 failed로 바꾸고, 후보 계약 거부는 바이트를 보존한다. 이 차이를 소비자마다 추측하게 하면 안 된다. 호환성 때문에 당장 통일하지 못하면 active_status와 latest_attempt_status를 분리해 혼동을 금지할 것.

또한 “한 번에 승격”은 아직 다중 파일 원자성을 뜻하지 않는다. [app.py:3412](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/webapp/app.py#L3412)에서 provenance·attempt success를 먼저 쓰고 full_metrics를 나중에 쓴다. 그 마지막 쓰기에 OSError를 주입하니 예외가 전파되고, **새 provenance ID와 옛 full_metrics ID가 달랐다.** 함수가 done을 반환한 반례가 아니라 예외 후 디스크의 세대 혼합 반례다. 현재 except는 LockUnavailable뿐이다.

이 역시 요청서가 공개한 WEB-03의 예외/크래시 창이다. 기존 RGL-04의 정상 계약 거부 복원은 닫되 전체 transactional publication이 닫혔다고 표현하지 말 것. 최소한 동기 예외 rollback과 latest attempt 실패 기록, 궁극적으로 세대별 candidate 디렉터리+단일 active pointer 또는 복구 가능한 commit protocol이 필요하다. 쓰기 순서만 뒤집으면 다른 중간 상태가 생긴다.

### Q3 전력 몫의 zero와 nonfinite 사유

**진단용으로 나누는 것은 좋지만 둘을 허용 사유로 등록할 근거는 없다.** 유한 양수 전도 해에서 물리 간선의 총 소산이 0이면 전력 원장/해/정규화 문제를 조사해야 한다. 비유한 소산은 수치 실패다. 비관통은 이미 별도 no-through 상태로 다룬다.

권고 상태는 예컨대 unexpected_zero_dissipation과 nonfinite_dissipation이며 둘 다 실패. 문자열을 둘로 나눴다는 이유만으로 valid_null로 승격하지 않는다. 현재 fail-closed 처분에 동의한다.

### Q4 옛 collector payload

**동의한다.** collector를 계획했는데 wetted/bare 각 수렴 3필드가 없으면 blind다. 요청 표의 적용 영수증, 주 솔브 수렴, 파일 존재는 보조 해의 수렴 증거가 아니다. 누락 값을 0/False/0으로 채우지 말 것.

다만 collector 미계획인 합법 LEAN 팔은 이 필드 때문에 거부하면 안 된다. 과거 payload는 “수렴 증거 없는 역사 자료”로 볼 수는 있어도 검증 완료 판정 입력으로 자동 이월할 수 없다.

### Q5 전역 virial과 프레임 대응

**전역 합은 전역 부호·척도 검사로만 충분하다. 입자별 대조를 강제로 관문으로 삼지 않는 판단에는 동의한다. 프레임 인증을 대체한다는 주장에는 반대한다.**

독립 두 dimer 예제를 재실행했다. 두 접촉의 힘 1과 3을 맞바꾸면 전역 virial 검사는 여전히 약 기계정밀도 안에서 통과하지만 AM_P 상대 응력은 **0.5→1.5**, SE는 **1.5→0.5**가 된다. 전역 합으로 입자·상 배분을 증명할 수 없다. 새 한정어는 이를 올바르게 인정한다.

TIMESTEP은 [parse_liggghts.py:19](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/scripts/parse_liggghts.py#L19)에서 산출 CSV 메타로 보존되지 않고, atom/contact/mesh는 [동일 파일:290](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/scripts/parse_liggghts.py#L290)부터 각각 선택한다. CSV 해시는 “이 파일을 읽었다”는 증거이지 같은 프레임 증거가 아니다.

이번 **수치 가드 재검증 범위 밖의 별도 작업으로 분리하는 것은 가능**하다. 대신 그동안 LW에는 frame_unverified를 유지하고 “검증된 상별 실측/학습 타깃” 인용 승인을 주지 않는다. 194건에서 LW까지 배포하려면 원 dump의 TIMESTEP·선택 파일·타입 매핑·벽 기하 대응을 먼저 봉인해야 한다. 194건의 승인 범위가 ⑤⑥⑦·망 τ뿐이라면 LW를 명시적으로 제외한 제한 인계가 가능하다.

새 LW와 옛 c_strs를 입자별로 무조건 같게 강제하는 것은 배분 정의 차이를 지우므로 해법이 아니다. 동일 프레임의 옛 50/50 virial 재구성 불일치 원인도 아직 미확인이다.

### Q6 후속 순서

**조건부 동의. 지금은 코드 GO가 아니다.** RGLR-01–03 수정·반례 회귀를 먼저 닫은 뒤:

1. 실제 WSL의 소형 관통/비관통/수치 실패, collector 계획/미계획 통합 및 real14 fixture 회귀.
2. 일반 경로와 LW 프레임 미인증의 허용 범위를 저자가 명시. 실패 게시 동작도 구별해 시험.
3. 변경된 수치 모듈을 저자 승인 amendment로 재봉인. 기존 09-17 cutoff·frozen inventory를 소급 변경하지 않음.
4. 승인된 194건 network 배치.
5. τ 관문을 다시 검사. 기술적 실패와 과학적 HOLD를 분리하고, 실패 행을 조용히 제외하거나 0으로 채우지 않음.
6. 실제 망 산출 숫자까지 들어간 인계 v1.2의 양성/음성 왕복검사.

현재 끝-끝 시험은 “실 stop 상태→실 배치→기존 접촉 행” 시험이다. 정직한 제한이지만 τ·전력 몫이 ML 인계까지 도달했다는 시험은 아직 아니다.

### Q7 옛 stress_cv의 무효값

**수정은 필요하나 “기존 계약과 전혀 충돌하지 않는다”라고 말하면 안 된다.** 저장된 0을 null로 바꾸는 것은 문자 그대로 값 변경이다. 따라서 “정상 입력의 정의·수치·키는 불변, 무효/미정의 입력만 null+reason으로 정정”이라는 좁은 amendment로 승인받는 것이 맞다.

원본 역사 파일은 보존하고 새 계약/출력 세대로 구분한다. 정상 zero CV(동일한 양의 VM인 균일 분포)는 유지해야 하며, zero load의 0/0이나 NaN·입력 결손을 그 정상 zero와 혼동하지 않는다. 등급 소비자는 invalid/undefined를 최고 등급으로 읽지 않게 별도 상태를 따라야 한다. 현재 grade의 옛 축은 [grade_engine.py:906](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf4fb6aee0b388375ddf65694ac405e63e0e381c/scripts/grade_engine.py#L906)에서 stress_cv 숫자를 직접 읽으므로 producer만 고치는 것으로 끝내지 말 것.

## 6. 양성 대조와 기존 반례의 독립 재현

G4는 원 탐침을 새 소스에 그대로 연결했다. NaN·Inf·음수·누락·부분 null의 기존 결함 변이는 거부되고, 전체 묶음/⑤⑥⑦ 기준선·network 단계·합법 접촉 0은 수용됐다. 비율 잔차 +0.004999/+0.005 %p와 지수 +4.999e-5/+5e-5는 허용, 각 반폭을 넘는 +0.005001 %p/+5.001e-5는 거부됐다. 미검토 금지 열 제외도 유지됐다.

커밋된 요약 CSV에서 생산 가드와 별도로 직접 산술을 다시 계산했다:

| 요약 코호트 | 행 | 단계 비율 최대 잔차 | 파괴지수 최대 잔차 | AM–AM 평균×개수=총합 최대 상대차 | contact/network 인계 동일 |
|---|---:|---:|---:|---:|---|
| LHS130 | 130 | 0.004996359899 %p | 4.9350649351e-05 | 2.5603803837e-16 | 예 |
| 확장64 | 64 | 0.004978165939 %p | 4.8484848485e-05 | 2.4421544290e-16 | 예 |

쌍별 면적 항등식도 817+394개 비영 접촉 쌍에서 최대 상대차 2.5613963026e-16 이하였다. **이는 이미 커밋된 요약표의 산술 검산이며 새 194건 실행이나 원 dump 재분석이 아니다.**

원시 수치 보존은 별도 검산했다. 검증된 eedada5d3 원본과 현재 코드의 L0/L1/L2 × Hertz/Physics × FULL/CF/CONSTR 총 18경우에서 (G, σ_ratio)의 float.hex와 경계 집합이 동일했다. 8개 단언을 8개 독립 침대로 세지 않았다. 유한 전극 예제는 물리 간선 소산 몫 0.0916787133551 대 이상 전극 0.0818181818182, 상대 +12.0517607674%였다. 전극 열을 분모에서 빼는 것과 전극이 해를 바꾸지 않는 것은 다르다.

## 7. 실행한 회귀와 미확인 범위

환경: Windows 11·Python 3.12.14·NumPy 2.3.5·SciPy 1.16.3·Flask 3.1.3. 고정 소스/자료 **432파일 Git blob 및 SHA-256 확인**. 초기 누락 의존 파일을 정확한 핀에서 보완했고, 아래는 최종 결과다.

| 시험 | 결과 |
|---|---|
| test_network_handover_chain | 10/10 |
| test_pipeline_provenance | 250/250 |
| test_tau_flux / test_tau_handover_status | 37/37 · 27/27 |
| network_conductivity selftest | 30/30 |
| test_rint_receipts / run_contract | 102/102 · 124/124 |
| sdcp_gain_verdict | 177/177 |
| rint03_je_compare | 14/14 |
| lhs_design_dataset / test_s567_labels | 277/277 · 13/13 |
| test_constriction_power_share | 17/17 |
| test_stress_lw_labels / test_rint_scope_labels | 48/48 · 31/31 |
| test_closed_param_groupview / test_tau_grade_unify | 44/44 · 19/19 |
| step3_sigma --selftest-rint | PASS |
| test_network_boundary_rule | 8/8, ⑨는 .git 없는 사본에서 SKIP. 위 독립 raw18 비교로 별도 재현 |
| test_love_weber_stress | 68/69 실행 단언. real14 fixture 부재로 한 그룹 실패; 요청서의 전체 76/76은 재인증하지 않음 |

`check_all.sh` 전체를 독립 재인증했다고 주장하지 않는다. WSL·real14·봉인·194건 실제 실행은 요청 범위 밖이다. 작은 CLI를 쓴 network 재현과 일반 경로의 Stage E 대역 사용도 위에서 구별했다.

이전 탐침의 주의점도 수용한다. collector 탐침은 옛 payload가 없는 디렉터리에서 시작했다. LW는 새 FAILED 반환에 배열이 없는 것을 정상 거부로 관찰하도록 별도 탐침을 작성했다. 사라진 사설 _wa_area_prep를 임의 복구하지 않고 실제 build_handover 경로를 재검증했다. 소스는 수정하지 않았다.

## 8. 재현과 증거 묶음

ZIP을 풀고 검토 폴더에서, NumPy·SciPy·pandas·Flask 등 원 프로젝트 의존성이 있는 Python으로 실행한다:

~~~bash
python3 verify_source.py
python3 run_tests.py chain pipeline tau_flux tau_status network receipts contract spearman lhs power verdict step3 lw_labels rint_labels group grade
python3 run_probes.py new_network independent_lw original_g4 raw18 handover
~~~

원 collector 탐침은 고정 출력명을 쓴다. 동봉된 옛 산출물을 둔 채 다시 돌려 파일 존재를 판정하지 말 것. 재실행은 별도 빈 검토 폴더에서 `source/`·`run_tests.py`·`run_probes.py`·`evidence_g1/probe_adversarial.py`만 복사하고 evidence 디렉터리를 만든 뒤 `python3 run_probes.py original_g1`로 한다. 본 검토는 처음부터 빈 evidence_g1에서 실행했다.

핵심 증거:

- `evidence/network_adversarial.json`: 실제 CLI·게이트·τ, 게시 복원·예외 후 세대, RGLR-01/02.
- `evidence/lw_replay.json`: 기존 LW 반례 및 실제 CSV 파서 우회 RGLR-03.
- `evidence_g1/adversarial_results.json`: 원 collector·Spearman 탐침.
- `evidence_g4/probe_results.json`: 원 인계 변이 전체 입력·출력·거부.
- `evidence/handover_replay.json`: 194개 기존 요약행 산술.
- `evidence/raw18.json`: 원시 18비교와 유한 전극 검산.
- `source_manifest.json`: 정확한 핀과 파일별 Git blob/SHA-256.
- `findings_review.json`: 이 검토의 신규 항목. 저장소 원장에는 쓰지 않았다.
- `package_manifest.json`·ZIP 옆 `package_receipt.json`: 묶음 파일 및 ZIP 무결성.

검토문은 기존 저장소의 Markdown 형식을 유지했다. 문서 작성 지침에 따라 관측·권고·미확인을 분리했다. 문서 자체가 생산 승인이나 새 봉인이 되지 않는다.

## 9. 이번 범위의 최소 잔여 해제조건

1. RGLR-01: BAND_FALLBACK 앞 기술적 입력 검증. 정상 fallback을 과잉차단하지 않는 양성 대조 포함.
2. RGLR-02: 차원/무차원 σ 항등식의 저장 정밀도 기반 검증. 작은 σ·온도 변환의 양성 대조 포함.
3. RGLR-03: 원 CSV의 미제공/부분/손상 구별을 LW까지 전달. 실제 파서 경로 음성 대조 포함.

위 셋을 먼저 닫고 §7-8로 넘어갈 수 있는지 다시 판정한다. 이미 닫힌 P1 수정과 G4 수용성을 되돌릴 필요는 없다. WEB-03·LHS-33·LW 프레임 미인증은 그 범위를 숨기지 않고 별도 결정·검증을 유지한다.

**HOLD**
