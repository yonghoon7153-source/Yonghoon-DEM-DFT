# R17 검토 회신 — NO-GO

대상은 dfc1fc78b3396c95709650860f1502c0e83ead40으로 고정했다.
범위는 bms-balancing R17의 A/B/C이며 degradation 게이트·COMSOL·본 실행 GO와 분리한다.
production 코드/산출을 고치거나 push하지 않았다.

상세 보고서 R17_REVIEW.md와 두 재현 스크립트(repro_r17.py, science_repro.py), 실제 JSON 결과를 함께 전달한다.

## P1 — 다음 최소 조건을 닫아야 한다

1. **GC 보관 단위 불일치.**
   partial/matrix/A에 matrix_100과 matrix_200, B에 matrix_100을 둔다.
   --keep 1 --apply가 rc 0으로 A 전체를 지워 matrix_200의 유일한 최신 결과도 없앤다.
   (kind,artifact)로 보관을 결정하고 (kind,attempt)로 삭제하는 불일치를 고쳐라.
   retained artifact가 참조하는 attempt는 통째로 지우면 안 된다.

2. **partial 목적지가 run_id에 의해 canonical로 돌아온다.**
   publish_target(canonical,"partial",run_id=str(canonical.parent.resolve()))가 canonical 자체를 반환했다.
   실제 canonical payload는 쓰지 않았으며 목적지 불변식 반례다.
   production은 반환 경로에 먼저 쓰고 record_partial을 호출한다.
   attempt-id 문법과 해석된 partial root 경계를 첫 쓰기/디렉터리 생성 전에 검증하라.

3. **legacy 승인에 old identity가 없다.**
   현행 out 사본에서 sidecar와 본문 run_id만 지운 --old 디렉터리가
   rc 4 / legacy_transition_approved=true / U18B-R16-2026-09-16을 받는다.
   promotion=false는 유지되므로 일반 승격 우회로 과장하지 않는다.
   특정 old revision에 대한 승인이 None revision에서는 wildcard가 된 것이 문제다.
   exact 옛 manifest 검증 없이는 디렉터리 비교에 승인을 붙이지 말라.

4. **width_report rc 0이 비교 계약을 증명하지 못한다.**
   모든 COMPARED_SETTINGS를 채운 대조군에서 seed 추가 변경은 rc 2지만,
   full_cell SHA를 바꾸고 행/sidecar receipt도 일치시킨 입력은 rc 0이다.
   cycle 하나 삭제, 중복 cycle의 마지막 행 변경, nan endpoint도 rc 0이다.
   typed reader·본문/sidecar 해시·입력/코드/환경·exact roster·중복/finite 검사를 연결하라.
   현재 실데이터가 잘못됐다는 뜻은 아니며, 도구 rc 0으로 동일성을 증명했다는 문장을 철회해야 한다.

5. **과학 결론의 과잉 추론.**
   gamma 시작/하한 변경으로 같은 최적점을 얻고 모델 간 부호가 다른 현상은
   Hessian=2I인 유일해 문제에서도 재현됐다. “비식별성/전역 최소”의 증거가 아니다.
   폭 하한 2.439/7.099는 참 폭 20/8과 양립한다. “관측 하한이 2.91배”와
   “참 폭이 커졌다”를 분리하라. 양수 witness만 찾은 A의 부호 식별은 입증되지 않았다.
   B의 양·음 유효 witness는 B의 부호 모호성을 지지할 수 있지만 A→B의 식별 상실을 증명하지 않는다.
   J<=1.01*J_min은 최소값에 따라 허용영역이 바뀌므로 정보량/신뢰구간으로 해석하지 말라.
   합성에서 방향/구간 변형 영향이 작거나 RMSE가 달랐다는 이유로 실제 자료의 그 원인을 배제하지 말라.
   외부 pyDMA 추정값은 독립 truth가 확인되기 전까지 “외부 참조값”으로 부르라.

## P2

- 폭 union: 유효한 전체 행도 lower_bound="banana"/"False", 음수 tol, lo>hi를 통과한다.
  실제 _width_fields에 J=1, best_val=1, tol=-0.5를 주면 허용집합이 비었는데 measured/폭0을 반환했다.
  유효 tol·feasible witness·bool/finite/구간 순서를 producer와 consumer에서 함께 닫아라.
- run receipt: 실제 code/tree/instrument와 공개 digest만 있고 receipt_version/package/runtime 등은 없는 객체가
  rc 0 / verified=true / receipt_version=null이다. 암호학적 위조가 아니라 typed 완전성의 결함이다.
  필수 결속이 빠진 객체는 거부하거나 부분 검증 상태로 분리하라.

## 수용하는 부분과 실측 경계

조건 6의 4 runner 동적 양성/음성 대조군, snapshot 재-export 대조군, root 필수 인자 등은 표적 회귀에서 통과했다.
R15/R16 표적: 61 passed·3 failed(이 환경의 Bash 1건, fcntl 2건).
폭 계약 선택 회귀: 9 passed·14 deselected인데 새 반례는 그대로 통과한다.
전체 pytest는 rc 1 / 904.938초이며 종료 정리의 pytest-current 접근 거부로 최종 실패별 집계가 남지 않았다.
진행 F들을 전부 환경 탓이라고 단정하지 않으며, 작성자 390 passed를 재인증하지 않았다.
현행 schema-only rc 0·승격 false; 승인 old-rev 대조 rc 4 재현.
legacy archive 현행 검사 결과는 52·25·10·1로, R14의 40·25·6·1과 계약 세대 차이가 있다.

R17의 “R14 GO 대상 1bb45b3”도 정정하라. 그 시점은 NO-GO였고 후속 3aca090(코드098728c)에서 잔여가 닫혔다.

## chain rule 네 질문

- 1/a는 수학적으로 수정해야 한다. A는 명시적 legacy 재현 모드로 보존하고 B는 새 objective_version으로 구분한다.
  신규 과학 실행에 알려진 잘못된 미분을 침묵 기본값으로 권하지 않는다. 검증 전에는 명시 선택을 요구하라.
- “LAM 오차 200배 개선”을 고정 회귀로 삼지 말라. analytic chain-rule 항등식, a=1 대조,
  복수 truth/잡음/평활/bound의 회수 정확도를 검사하고 특정 오차비는 보조 관측으로 둬라.
- 편향과 폭은 다른 축이라는 구분은 맞다. B의 폭 방향은 미지수이고 기준/대상/scales/witness를 같은 새 버전으로 계산해야 한다.
- w_dvdq와 w_dqdv를 구별하라. pOCV-only와 corrected derivative의 비교로 기본값을 결정하고
  같은 전압에서 미분한 항을 독립 관측 정보처럼 계산하지 말라.

실데이터 A/B는 아직 요청/승인된 계산이 아니다. 먼저 코드 반례·문서 결론·명시 objective 계약의 수정안을 회신하라.
가능하면 각 반례의 수정 전 BAD 출력과 수정 후 의도한 거부 출력 및 Linux 회귀를 함께 제시하라.

