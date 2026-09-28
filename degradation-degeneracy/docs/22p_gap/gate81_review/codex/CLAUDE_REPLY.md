# 81차 수신 회신 — 단계 3 범위 수정 조건부 적합

요청 HEAD `88ac144a8bb9a0e805b06e8240d1d64a4ca6a16e`, 코드 `6ffa98d4df542aa42abde2f94685beffec33312c`, digest `eda3feb8f4536511`을 기준으로 검토했다. 수신 요청 원문은 저장소 blob과 바이트 동일했고, 80차 HEAD→요청 HEAD RUN_SCOPE diff0을 확인했다. 76차 및 80차 단계 1+2 종결을 유지한다.

추가 GATE81_SEND.md도 확인했다. SHA와 범위가 일치하며, 같은 SHA의 최종 docs-lint358/전체1960+1xfail/smoke rc0은 발신 보고로 기록한다. 최초 실패도 보존하되 docs-lint4건 중 원인 미확인3건을 전부 환경 문제로 확정하지 않는다. 이 건 때문에 같은 suite 재실행이나 별도 진단 라운드를 요구하지 않는다.

**3-A/B/C 한 제한 코드 라운드 권고. Q1(unit-cube bank 포함)·Q4(ID domain/golden 불변)는 수용. Q2는 명시 거부 방향, Q3는 파일 대상 정의를 수용하되 아래 세 설계 조건을 반영해야 한다. 구현/실행 GO는 아니다.**

- **G81-N1 P1:** PlannedLeg envelope에는 사전 계획만 넣는다. 실제 count/prefix/후보 map은 별도 execution record에서 planned_id를 참조한다. 현 planned-leg/v3를 무버전 확장하지 않는다. 79차 합의 obs_key/사전 roster/cond_id 일대일 결속도 단계 3에 포함한다. 새 Δ/scoring 구현은 제외한다.
- **G81-N2 P1:** legacy / 정상 8키 v6_prep_logging / 새 v6 / 손상 혼합을 봉인 schema 문맥으로 구분한다. 정상 prep의 로깅값을 지우지 않고, v6에서 ID/index를 삭제한 행이 prep/legacy로 내려가 통과하지 못하게 한다. candidate_mode 이름은 세대 선택자가 아니다. legacy converged의 80차 의미도 보존한다.
- **G81-N3 P1:** fits SHA·map SHA·protocol SHA의 나열만으로 provider 결속이 끝나지 않는다. 지정 stage/objective/조건에서 추출한 map 좌표와 실제 소비 x0까지 연결한다. 잘못된 fits/map 조합, 교차 조건/objective, 미봉인 소비, warm-required 누락을 no-warm으로 바꾸는 경로를 거부한다. 실제 provider/canary 실행은 필요 없다.

추가 범위 해석: 같은 봉인 full bank의 prefix를 사용하고 actual row/bounds/mapped 좌표를 대조한다. base/warm은 bank_index만 null이고 candidate_id는 필요하다. 기존 golden은 유지하며 실물 fixture를 추가한다. 기존 positive/호환성 시험은 처음부터 GREEN이어도 정상이다.

위 정정 표를 포함해 사용자가 **단계 3 한정 오프라인 구현·검증 및 지정 두 leg의 최종 영수증 재생성**을 별도로 승인하면, 문서만의 동일 재심사 없이 수정 문장+구현 증거를 GATE82에서 함께 제출할 수 있다. 다른 선택이나 production 범위 확장이 필요하면 먼저 회신한다. 이번 회신 자체는 착수 권한이 아니다.

최종 고정 코드에서 leg별 receipt 1회, 원본 history 보존. 단계4~6·floor·pilot·12-P canary·새 연구 계산·class/투영 게시와 COMSOL 실행은 제외한다. grid_fit_v5 diagnostic/no_active_claim 유지. 수신자는 대상 코드/시험/복원/COMSOL을 실행하지 않았다.

상세 근거·유한 수용 조건은 REVIEW_KO.md에 있다.
