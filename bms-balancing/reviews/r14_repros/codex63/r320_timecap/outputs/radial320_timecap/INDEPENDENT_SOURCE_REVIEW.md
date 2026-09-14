# R320 H0125 독립 소스 감사

**소스·출처 감사 PASS.** 고정 기준은 `Caps300R320H0250`, job `f0db6d080ad04045a2b43dc5a51d89b2`, 실제 SHA `837f8b03ff3381bb1aea6397935d0079b032f5e4aea007b32d1ebf7c40775b2e`이다. 새 `Caps300R320H0125`의 SHA는 `8d35be8fab513f5e2def316c4d00e0fdc19983a5dd3bf492f4ffe47a58248be3`, 크기 65,227 bytes, 제출 job은 `18a00b03e38d4694b9ba30d88e7008f4`이다.

607줄 전체 소스 바이트 비교에서 class/label 이름 두 곳과 cap 표현식의 실제 설정·출력 로그 두 곳만 바뀌었다. 설정은 `if(t<0.1[s],0.00025[s],0.1[s])`에서 `if(t<0.1[s],0.000125[s],0.1[s])`로 바뀐다. 물리 mesh 120/60/120과 각 전극 입자 요소 320, 0.1C, `sigma_short=1e-20 S/m`, 모든 물성/OCP 표·Li 재고·초기조건·solver scale 코드, 187개 지정 시각과 5 s 종료, 후처리·guard 코드는 그대로다. 단일 `runAll` 호출의 기존 CDI+5 s transient 구조도 같다. 정확한 차이는 `INDEPENDENT_SOURCE_DIFF.txt`에 있다.

baseline의 name/path/SHA/job 네 필드와 flat 별칭, configs, 실제 job request 및 제출 소스 해시가 일치한다. baseline을 만들 때 사용한 R160 계보는 `ancestor_source_identity`로 따로 기록돼 현재 R320 비교 기준과 섞이지 않는다. 두 실행의 worker 예산은 1,200 s, cores 2로 같다. 이 예산은 벽시계 한도이며 물리시간이 아니다.

OCP/entropy 네 함수의 외삽은 `none`이고 표면 농도/표 범위 StopCondition은 step 이후 검사다. 모든 Newton trial을 검증했다는 뜻은 아니다. 전해질 양수 검사는 **후처리 전용**이다. 같은 설정과 이 한 번의 cap 반감은 전체 시간·공간 수렴을 입증하지 않는다. 실제 native 완료·mesh·Time/Variables·accepted step은 별도 감사에서 판단한다.

사전 중복 검사에서는 기존 29개 job의 196개 파일을 해시하고 request/status/Java 및 관련 로그를 검사해 후보 0개를 확인했다. 정확한 UTC 검사 시각, 29개 ID, 경로·크기·SHA는 `DUPLICATE_CHECK_BEFORE.json`에 기록했다. 이 검사는 새 job request 생성보다 먼저 끝났다.

이전 R320 ZIP의 **현지** 원본은 429,953,577 bytes / SHA `89703ec4a1e47985ddefa9b0270cd317d0356cbe2ec7d4efe31f879703702aa0`이며 내부·외부 manifest가 같다(147 payload, 148 ZIP entries). 최신 사용자는 payload147·manifest/CRC·historical333·원시 수치를 확인했지만, 수신한 outer ZIP의 bytes/SHA를 다시 명시하지 않았다. 따라서 그 확인만으로 수신 outer ZIP의 식별까지 동일하다고 추론하지 않는다. 현재 967개 현지 보존 명세도 수신 측 전체 재검증과 구분한다. 상세 수준은 `PROVENANCE_LEVELS.json`에 있다.

본 감사는 COMSOL 실행이나 기존 파일 수정을 하지 않았다.
