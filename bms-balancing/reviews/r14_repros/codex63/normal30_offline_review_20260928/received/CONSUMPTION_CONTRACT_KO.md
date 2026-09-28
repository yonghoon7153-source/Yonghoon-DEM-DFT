# 정상30초와 보호중단 소비 계약

## 상태와 rc

| 관측 | 분석 결과 / rc | 부모 분류 |
|---|---|---|
| 정확 마지막30초, 모든guard0, native정상끝,필수축PASS |NORMAL_30S_DIAGNOSTIC_COMPLETE /0 |AWAITING_30S_LIMITED_EXTERNAL_ACCEPTANCE |
| 마지막에 한 개 이상guard0→1,짝/사유/이후 적분 없음,필수축PASS |PROTECTED_STOP_30S_INCOMPLETE /1 |동일한 보호중단 미완 |
| fatal/누락/수치/정리/정책/반환/시간/기록 오류 |INCOMPLETE /1 |INCOMPLETE |

어느 경우에도 overall/normal_gate=INCOMPLETE와 effective_policy=UNVERIFIED를 유지한다. 보호식이30초 정각에 발동해도 정상완료로 올리지 않는다. guard 관측이 성공한 뒤 수치검사에 실패하면 termination/diagnostic 관측과 오류를 같이 남긴다. 특히 OCP/표면 보호중단의 말단 범위 위반을 수치PASS로 완화하지 않는다. 보호 관측과 수치 미완이 공존할 수 있다.

## 필수 증거

- threshold0, 같은 전체/각domain Minimum, domain1/2/3·Lagrange5·단위,동률/근접동률 구분. 모든guard boolean,초기false,중간false. 보호중단이면t_minus<t_plus≤30와활성guard명 보존.
- 정상은 stop message0개와native Time solver 시작/끝1쌍, 보호는해당guard설명1개. native out step순번·상태수·반올림시간 범위를 CSV의정확저장시각과연결한다. fatal은rc0이어도거부. 종료뒤추가적분없음,생산완료표식1개,report failure없음.
- runtime settings의 tlist437개·기존18key 일치. Java readback0 및 checkShape상한30. `TIME_CAPS`의 모든 과거 의문이 해소됐다고 쓰지 않는다.
- 양성에도sampled_comparison/preservation/process_cleanup/policy_preservation 각PASS와 필요한표manifest/termination/native/numeric/runtime구조가 모두 있어야 한다. 요약문자열만으로부모수용불가.

## 시간 비교

정상은0–5초 원요청187개가 대상/기준에 모두 있어야 하고,5.1–30초250개는대상에있어야한다. 전체저장상태수는고정하지않는다. 보호중단은직전t_minus까지의strict요청prefix를확인한다.

`full_intersection`은 실제대상/기준 전체교집합이다. `common_stored`는그중t≤min(5,safe_prefix_end)인비교부분집합이다. 각목록·개수·처음/끝·빠진요청·비공통대상시각을보존한다. 비교가빈집합또는t=0뿐이면거부한다. 보간/최근접/시간epsilon으로공통시각을만들지않는다.1198의발동후1.8초는이구분의근거이지새30초비교에서빼야할시각이아니다.

## 수치 및 해석

ΔV≤0.001V,표면Δx≤0.0001,Li총량상대변화≤1e−6,전압항등식잔차≤1e−8V. 초기Li_N/Li_P/Li_electrolyte 각양수·기준대비상대차≤1e−6도각각확인한다. 모두기존허용치를재사용하며절대운전전압한계를새로만들지않는다.

전역/경계/guard시각동일·유한값·단위,전극별241좌표/domain,기존OCP/표면범위를유지한다. 초기Li결과를총량한개로대체하지않는다. 정확공통시각의전압과N/P표면프로파일을비교한다.

5–30초는전압,전체/각domain농도최소,guard,N/P입자평균전극평균·표면최소최대,Li각항의시작/끝/최소/최대를요약한다. native log와stored time vector는실제step/실패/간격근거로남긴다. 이구간에는이전5초기준동등성이나장기수렴을주장하지않는다.

## 부모 종료 수용 경계

고정 `-NoExit` 부모의 Python/native와analysis즉시반환rc·오류는별도로소비한다.최종수용에는 PARENT_LOCAL_DECISION,FINAL_BOUNDARY(참조해시/오류없음/시간충족),실제최종콘솔반환,사용자관측프롬프트복귀가필요하다.프로세스가종료하지않으므로외부PowerShellOSrc는null이다.프롬프트복귀를rc0으로바꾸지않는다.

부모파일기록후오류·시간초과이면마지막limited는INCOMPLETE다.FINAL_RECORD_ERROR또는마지막반환미확보는수용불가이며앞선수치성공을지우거나새실행을자동시작하지않는다. 전달예산300초의끝은로컬최종증거확보이고사용자의이후업로드시간은포함하지않는안을승인문에명시한다.
