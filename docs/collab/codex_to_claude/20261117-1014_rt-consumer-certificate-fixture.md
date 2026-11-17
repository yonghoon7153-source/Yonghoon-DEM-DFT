| 트랙 | 준비 | 상태 | 숫자 | 다음 |
|---|---|---|---|---|
| DEM Ⓐ A2 | RT 소비자·배타 증서·fixture 판독 | 새 복사 층 구현 · 러너 실행 진입 중단 유지 | 합성20/20·8/8·9/9·8/8·7/7 (각 Windows/Linux) · 현장0 | fixture 러너·사전 점검 마지막 조립 |

# RT 소비자 · 증서 · fixture 인계 — 2026-11-17

## 1. 반입 순서

- 가지: codex/dem-rt-numeric-1117 (같은 가지, 재작성 없음).
- 직접 부모: 5d8e628ab80b66cbfddf8a8d7404dad2da1282d7. 시작 바탕 b3481336c의 뒤를 그대로 잇는다. 반입 ⑨ 미혼합.
- 이전 수령 5d8e628ab → 이번 <<sha:feat(dem): connect RT consumer certificates and fixture reader>>. 이번 추가 SHA/patch-id는 리포 밖 README_CLAUDE/HANDOFF에.
- 변경 파일은 docs/reviews/p1_rt_consumer_preparation_20261117/ 새 파일들과 이 쪽지뿐. 원94파일·앞113파일·공유 기록·Rint·운영 봉인 변경0. 새 생성 복사본122파일.

## 2. 끝난 것

정본 docs/reviews/dem_unloading_ps45_prereg_20261009.md §15-4b·§15-5·§15-5b–d를 따라 RT 단계 기술/reset/목록, 기존 검사 보존 및 G2c_cont 보고 분리, G2cp/ⓡ/ⓣ 처분, 기본 읽기 전용과 배타 최초 발행, 독립 fixture 판독20 및 신원·원자료 재판독을 구현했다.
기술/결합 모순이면 RT 값 읽기를 생략한다. 완성 증서가 공개된 직후 응답 실패 시 파일을 지우지 않고 실패를 반환한다. 완료 영수증 없이 다음 관문을 열지 않는다.

Windows와 로컬 Linux: 계약20/20·발행8/8·fixture9/9·사전대조8/8·실제 legacy 연결7/7. 앞 실패 기록·준비 중 오류·관측 수 구분은 docs/reviews/p1_rt_consumer_preparation_20261117/README.md §5 및 docs/reviews/p1_rt_consumer_preparation_20261117/validation.json에. 원천 선택 실패도 기존 실패 우선순위를 보존한다. Linux 문서 참조는 깨진 경로0·커밋0. 내부 합성 확인이며 독립 판정 아님.

## 3. 남음

fixture 전용 러너의 단계 흐름/복사 목록, 준비 러너의 새 소비자·두 문법 사전 점검 호출 마지막 조립이 남는다. 실행 진입 즉시rc2 유지; 후보 해시표는 운영 봉인 아님. 이후 완성 키트 봉인 직전 독립 반박1회, 그 뒤 현장 fixture/읽기 전용 사전 셈·실행 GO는 1저자.
이번 현장 실행0·실제 값 열람0·운영 재봉인0. 추가 비준 질문 없음. 원장 처분/verified 승격 제안 없음.

## 4. Claude 공유 기록 제안

> [DEM Ⓐ] 11-17 RT 기술/reset/목록→수치/연속성 처분, 배타 증서·읽기 전용 재판독, 소스 닫힌 fixture20검사/원자료 재판독 후보 준비. Windows/Linux 합성20·8·9·8·7 각 전부 통과. 원94·앞113파일 보존, 새 복사122파일. fixture 러너/사전 점검 마지막 조립 전, 실행 진입 중단·현장0·값0·운영 봉인/GO 없음.
