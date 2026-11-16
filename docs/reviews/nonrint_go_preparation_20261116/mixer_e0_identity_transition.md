# E0 pilot 한 팔 — SELF-170 이후 신원 전환 준비

정본 = `docs/reviews/mixer_e0_pilot_registration_20261113/registration_candidate.md` §§0·7-6·7-7·15-1. SELF-170 근거 = `docs/reviews/mixer_self170_20261113/README.md` §§1–3. B 반입 뒤 상태 = `docs/collab/claude_to_codex/20261115-1214_intake-sha-map.md`.

## 1. 지금 확인한 비결과 신원

`scripts/mixer_stage_gate.py`의 e0_record_tools는 smoke_blind·checker·reader·deckdiff 네 도구 SHA256을 묶는다. identity_map.json은 바탕 B의 Git blob을 읽어 이 네 개와 stage_gate의 신원을 고정한 기록이다. import·selftest·기록 판독·seal 생성 없이 바이트만 해시했다.

SELF-170 뒤 smoke_blind는 바뀌었다. 옛 E0 기록이 지금 네 도구 표와 같다고 간주하지 않는다. 런타임 본문 변경이 작거나 합성 selftest만 바뀌었다는 설명도 신원 불일치를 면제하지 않는다.

## 2. 재봉인 A/B 앞의 연결표

| 순서 | 준비할 근거 | 지금 | 거부/보류 |
|---|---|---|---|
| 새 소스 신원 | 고정 핀·네 도구 SHA·최종 승인 코드 목록 | 1: identity_map 작성 | 어느 도구라도 달라지면 전환표 새 판 |
| SELF-170 Linux | 같은 고정 소스의 전체 selftest 및 고정 시각 전체 사본; Windows 부분식과 구분 | 0: 이 창 수행 없음 | 부분식11/11을 전체 Linux 자격으로 대체하지 않음 |
| A/B 비활성 대조 | 원 등록 §7-6 순서·원 증거·의존 신원을 새 소스와 대응; 실패/오염·중단/회수 계획 | 1: 계획만; 사본 생성·seal 갱신 안 함 | 옛 E0 PASS가 새 소스 관문을 열면 불합격 |
| E0-R3 | historical originals 수령·정정 근거를 보존 | 2: 기존 수령 문서 참조 | 정정 사실이 운영 봉인 갱신은 아님 |
| 현장 근거 | ibb 한 설치·Linux/SLURM, 링크·권한·변경통제, binary/MPI, 자원·시간·디스크·회수 | 0/과거 관찰: 새 런 유효성 미확정 | 오래된 조회를 현재 설치 자격으로 단정하지 않음 |
| 한 팔 내부 반박 | E0 한 팔 한정 요청서·고정 ZIP·작은 반례 | 0: 아직 이 단계 아님 | 내부 예외를 N0/B쌍/first8 전체에 확대 금지 |
| 재봉인·발사 | 1저자 별도 GO | 0: 미승인 | 예약 해제·봉인 교체·제출·자동 다음 팔 없음 |

새 원장 상태를 만들지 않는다. SELF-170은 받은 처분대로 claimed_fixed다. 내부 리뷰는 Codex 아님이며, 한 팔에서 내부 반박이 반박 GO를 대신할 수 있다는 11-10 예외와 최종 발사 GO=1저자를 구분한다.

## 3. 다음 합성 준비의 음성 목록

- 옛 smoke_blind SHA만 가진 기록, 네 도구 중 하나 누락/중복, 새 핀과 다른 blob.
- 적격성 확인 뒤 소스 변경, 후보 안 증거 쓰기, 실패한 복사본의 성공 표지 재사용.
- 기존 런/예약/증서가 존재하는 목적지, 비원자 부분 공개, 예상하지 않은 링크/변경통제 위반.
- 본문 정밀도/관측 계약은 원 등록을 유지; 수치 문턱을 바꿔 현장 자격을 우회하지 않음.

이는 시험 목록이며 실행 결과가 아니다. 운영 봉인 파일이나 실제 E0 기록은 이번에 읽거나 다시 생성하지 않았다.
