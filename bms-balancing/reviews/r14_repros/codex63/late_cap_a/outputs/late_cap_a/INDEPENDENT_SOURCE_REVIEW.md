# Candidate A 독립 소스·제출 식별 감사

**PASS.** 기준 `Caps300R320H0125` / job `18a00b03e38d4694b9ba30d88e7008f4` / SHA `8d35be8fab513f5e2def316c4d00e0fdc19983a5dd3bf492f4ffe47a58248be3`와 새 `Caps300R320LateCapA5s` / job `c40c05d3cfb643a4b706345637b00f57` / SHA `a03abb905454de63b34b55e314ed09f3cb6414d58444e8b605962166a872531f`를 고정했다. 새 소스는 65,281 bytes, 607줄이다.

전체 바이트 비교에서 class·label 이름 두 곳과 cap 실제 설정·동일 출력 로그 두 곳만 바뀌었다. 새 식은 `if(t<0.1[s],0.000125[s],if(t<1[s],0.005[s],0.025[s]))`다. 물리 메시 120/60/120, 입자 320/320, 물성·OCP 표·Li 재고·초기화·허용오차·scale·187 요청 시각·전극별 241좌표·보호/내보내기 코드가 그대로다. 기존 단일 `runAll`의 CDI+5초 구조다. 상세 차이는 [INDEPENDENT_SOURCE_DIFF.txt](INDEPENDENT_SOURCE_DIFF.txt)에 있다.

baseline의 원자적 name/path/SHA/job과 별칭, configs의 두 source 해시·경로·시간식, contract의 세 cap 구간·네 비교 구간·판정 기준을 대조했다. 실제 두 request와 제출 Java 해시도 일치한다. 이전 H0250은 계보이며 현재 기준은 H0125다.

실행 자원은 **기준 2코어/벽시계 1200초 → 새 요청 16코어/벽시계 1800초**로 다르다. 벽시계 예산은 물리시간 5초나 solver 설정이 아니다. 코어 변경으로 병렬 부동소수점 효과가 포함될 수 있으므로 전체 실행 조건이 cap만 다르다고 주장하지 않는다. 실제 COMSOL 사용 코어 수와 native 완료·속성·accepted interval은 후속 독립 감사 대상이다.

사전 중복 검사는 기존 30개 job의 request/status/Java/log 233파일을 모두 해시하고 후보 0개·진행/불명 상태 0개를 확인했다. 검사 종료가 새 request 생성보다 앞서며, 현재 native ID의 추가분은 `c40c05d3cfb643a4b706345637b00f57` 하나다. 20코어 요청의 도구 검증 거절은 root 기록에 따라 job 생성 전 사건으로 구분하며 실행 횟수로 세지 않는다. 기존 233파일의 최종 불변 검사는 별도 수행한다.

0.1초 및 1초 도착/출발 interval을 분리하고 실제 상한·분포 감소를 확인해야 한다. 1–5초 차이에는 앞 구간의 상태 차이가 누적될 수 있다. OCP 외삽 금지·고체표면/OCP step 이후 StopCondition을 유지했고 전해질 양수는 후처리 전용이다. 이번 비교는 전체 수렴이나 참값 오차를 증명하지 않는다. Candidate B·재시도·추가 해석은 승인되지 않았다. 본 감사는 COMSOL 실행 또는 기존 파일 수정을 하지 않았다.
