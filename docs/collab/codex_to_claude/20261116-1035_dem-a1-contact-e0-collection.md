# 11-16 밤 — 탈압 A1·F 설정 확인·E0 수집 복구

| 트랙 | 계산 | 상태 | 숫자 | 다음 |
|---|---|---|---|---|
| 탈압 A | RT1/RT2 준비 | 정적 덱 층 준비 | 원94 보존·추가13, 시험12/12, 현장0 | 러너·30열 판독·증서·fixture 20검사 연결 |
| 수영 2D | F 접촉 선택 준비 | 첫 설정 확인 | 원판4·µ0.2·grid32, 새 계산0 | 틈/거리 구현·U6(a) F Φ_m 순서 선택 |
| 믹서 E0 | 366423 기존 한 팔 | 1저자 19:1x KST 확인 RUNNING, 수집 TXT 준비 | 경과2:16:09·wall1일, 수집 합성10/10 | 종료 뒤 1저자 --collect; 새 제출 없음 |
| LHS | O1→압력 재고→§5→v1.3 | 기존 대기열 유지 | 이번 신규 결과0 | v1.3 README 한정어 유지 |
| 50kg | 기존 진행 기록 다음 | 대기 | 신규0 | Love–Weber 응력 재작업 없음 |

## 1. 가지·반입

새 가지 = codex/dem-a1-contact-1116. 바탕 = `6efb44eac2b92f49418c2d791c6ff51612a1f5e7` (앞선 release 다섯 커밋 끝). 이미 보낸 release/observations 가지에는 더 쌓지 않았다. 이 가지 변경은 새 docs 파일뿐이다. Rint 고정 가지·scripts/·공유 원장·CLAUDE.md·진행 기록·check_all.sh·docs/mpm_basics_20261116.md 변경0.

반입 순서: 앞선 release 다섯 및 observations 셋은 종전 인계대로; 그 뒤 이 묶음 `Prepare copied RT deck layer` → `Prepare terminal-only E0 collection recovery` → 이 쪽지 커밋. 정확한 원 SHA 및 패치는 ZIP README_CLAUDE.md에 기록한다. 반입·게이트는 Claude, 실행은 1저자.

## 2. 탈압·수영

- docs/reviews/p1_rt_deck_preparation_20261116/README.md: A1 정적 덱 층만 구현. 원 키트94바이트 보존, 생산RT10·작은fixtureRT2·표1 추가. RT 미구현 상태의 같은12메서드: 실패15관측/오류0 →12/12. 초기 시험의 dump 토큰 인덱스 오기를 정정한 이력 포함. 기존 봉인을 갱신하지 않았다. A1 전체와 A2는 아직 완료가 아니다.
- docs/reviews/p1_rt_deck_preparation_20261116/experimental_request_RB01.md: 같은 시료 원측정 요청표·고체량/면적 대조 준비. 값 수령·새 계산0.
- docs/reviews/dem_suyoung_contact_preparation_20261116/first_run_audit.md: 첫 F는 틈/거리 없음·4원판·µ0.2. U6(a)의50개 안팎·µ0.5·12/16셀 공통 목표점 비교와 다르다. 선택 없음. 기존 F 겹침만 병기; 응력비를 선택/해석에 쓰지 않는다. 옵션 구현·새 개발 블록은 다음 연결로 남는다.
- G2c′ 메타 회수는 이미 수령되어 반복 요청하지 않는다. B N40000 첫내용 판정 고정·등록 결론 채택false, 소비자/실패경로는 알려진 한계로 A를 막지 않는다.

## 3. 믹서 긴급 수집

1저자 수령 기록: 원격 감시가 Broken pipe로 끝나 원격 command rc255. 첫 report와 SHA256SUMS만 회수, full archive 없음. RUNNING의 ExitCode0:0을 완료로 쓰지 않는다. 첫 반환의 RETURN_RC0도 계산 완료가 아니다.

docs/reviews/mixer_e0_collect_recovery_20261116/README.md 및 prepare_collect.py: 종료 상태·원 컨트롤러 부재·첫 해시 확인 뒤 기존 returns/evidence를 packet 내부 이력 폴더로 옮겨 원바이트 보존. 새 evidence/returns에서 고정 컨트롤러 --collect만 실행. 컨트롤러 소스·승인B·예약·case는 불변. 이미 만든 이력은 덮거나 다시 돌리지 않는다. 중간 실패는 자동 복구/재수집하지 않는다.

원격 수집 작업은 nohup+setsid, stdout은 파일로 분리. 같은 TXT 재실행은 재연결/회수만 한다. 새 archive_rc0·report/full 두 파일의 해시가 필요하다. 계산 실패 상태도 증거로 받을 수 있으므로 worker/runner/return rc를 분리한다. 새로운 발사·취소·재큐 없음. 명령 TXT는 개인정보 때문에 리포 밖 전달한다.

합성10/10 중 실제 고정 컨트롤러 --collect 분기의 원 report 충돌→보존 뒤 두 새 archive 생성 시험 포함. scheduler/runtime은 모의, 외부 명령 호출은 차단. 원격 실제 자격 또는 완료 판정은 아님. TXT/내장 worker bash 문법0, 내장 Python 컴파일 통과. 이번 현장 접근·제출·엔진/MPI 실행0.

## 4. Claude 공유 기록 제안

"11-16 밤 Codex: 탈압A1 RT 정적 덱 층(94보존+13추가·12/12) 및 RB-01 원측정 요청표 준비. 첫 수영F 설정 확인(4원판·µ0.2·틈/거리 없음), U6(a) 선택 전이라 응력비 해석 없음. E0 366423 감시SSH Broken pipe 후 원 반환 보존·종료 후 --collect 전용 블록(합성10/10) 준비; 새 제출0·현장0. B 자격 잔여는 알려진 한계, N40000 반복0. 후막 보드 밖·50kg Love–Weber 재작업0. 수송 tortuosity=tau2=φ_SE σ0/σ_eff, sqrt 아님, 기존11-06 표 수정0."

새 finding 종결/verified/GO 또는 원장 직접 변경 없음. 반박 리뷰는 봉인 직전 정해진 차례로, 이번 개발 준비에 새 리뷰 관문을 추가하지 않는다.
