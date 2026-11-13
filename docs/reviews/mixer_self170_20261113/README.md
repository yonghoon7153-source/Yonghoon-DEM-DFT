# SELF-170 selftest canary 경계 수정 후보 (2026-11-13)

닫으려는 것 = selftest ⑮·⑯·㉓의 타임스탬프 부분문자열 오탐. 닫지 않는 것 = 전체 래퍼·Linux 권한 자격, 실제 값 유출 방어의 보편적 증명, E0 운영 봉인·발사. **전체 HOLD · 실제 결과 0.**

## 1. 최소 변경

`scripts/mixer_smoke_blind.py`의 `selftest()` 안에 `_canary_present(text, needle)`를 추가하고 세 검사만 연결했다. 정규식은 `(?<![0-9])`와 `re.escape(needle)`다. 바늘 바로 앞이 ASCII 숫자이면 타임스탬프 내부의 겹침으로 제외한다. JSON 값·음수·repr 앞자리, 시간 문자열 뒤의 실제 누출은 계속 잡는다. Unicode 숫자 앞은 보수적으로 잡는다.

이는 합성 selftest의 **고정 바늘**에만 쓰는 검사다. 임의 숫자 파서나 운영 결과 차단기로 사용하지 않는다. 다른 숫자 내부의 동일 부분문자열을 무시하는 정책도 포함하며, 모든 표현의 값 누출을 판별한다고 확대하지 않는다. 런타임 `leak_check`·투영·봉인·판독 코드는 변경하지 않았다. 모듈에서 selftest를 제외한 AST 동일을 대조했다.

## 2. 직접 확인

| 단위 | 수정 전 | 수정 뒤 | 범위 |
|---|---|---|---|
| 같은 집중 회귀 | rc1 · 11메서드 · 실패 assertion 15 · 오류 0 | rc0 · 11/11 · 오류 0 | 실제 소스에서 세 검사식과 `_now()`를 AST로 추출. 모듈 import·판독기 실행 없음. |
| 고정 시각 사본 | 오탐 재현 | 통과 | `2026-11-12T17:35:10.964312Z`; 실제 `_now()` 사본과 검사식. 위 11메서드 중 1개이며 별도 고유 시험으로 더하지 않음. |
| 제거 변이 | 해당 없음 | 경계 제거·escape 제거·항상 False 모두 rc1 | 3변이 검출. 원 소스는 보존. |
| 전체 `--selftest` | 이번 실행 0 | 이번 실행 0 | POSIX 셸·0600 권한을 포함한다. Windows에서 이를 대역으로 바꾸어 전체 통과로 만들지 않았다. Linux 합성 재현은 별도로 남음. |

증거 요약 = `synthetic_summary.json`. 테스트 파일 해시는 전후 같다. 시험 실행 명령:

```text
python3 -I -X utf8 -B scripts/test_mixer_self170_canaries.py
python3 -I -X utf8 -B scripts/test_mixer_self170_canaries.py <before-source-copy>
```

두 번째는 수정 전 바이트의 거부 회귀를 확인하는 명령이다. 실패를 기대하는 상위 래퍼로 green을 주장하지 않는다. 이번 전달의 before 사본·red/green 로그는 ZIP에 넣되, 로컬 절대경로는 자리표로 가린 사본임을 표시한다.

## 3. 남는 것

1. Linux 새 복사본에서 전체 selftest와 고정 시각 **전체 사본**을 같은 소스로 재현한다. 이번의 고정 시각 **검사식 사본**과 구분한다. 실제 호스트에서 우리가 실행하지 않는다.
2. 소스 SHA256은 `synthetic_summary.json`의 before/after 값으로 바뀐다. `mixer_stage_gate.e0_record_tools`가 이 도구 신원을 묶으므로 E0 재봉인 A/B에서 한 번에 반영한다. 운영 seal·예약·manifest는 이번 변경 0.
3. 원장에는 후보 근거만 제안한다. 내부·작성 측 합성 확인으로 verified를 만들지 않는다.
