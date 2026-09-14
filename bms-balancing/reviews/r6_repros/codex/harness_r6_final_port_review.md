# R6 최종 precision / CSV 검토 — d431404

대상: `work/harness-r6-d431404/bms-balancing`, HEAD
`d4314048c63605fb4613f8b0a91859271fddda98`. 사용자 첨부 `R6_REQUEST_d431404.md`를 전체 읽었으며,
이전 `1049894`의 관측은 자동 이전하지 않고 이 대상에서 다시 실행했다. 대상 git 상태는 clean이다.

## 결론

담당 범위에서 **새로 확정한 GO 차단 반례는 없다**. R5의 `%g` 영점·decade·0자리, 선언/앵커 역할,
parameter 이름 반례 및 내부 V6-01/02/03/04/06/07의 아래 사례는 현재 코드에서 의도한 이유로 거부된다.
정상 대조군도 통과한다. 이는 이 제한된 검토 범위의 결론이지 전체 하네스나 모든 입력의 안전성 증명은 아니다.

아주 큰 유한 수에 대한 helper stress 오류는 남지만, 실제 raw-RMSE producer가 그 값을 만들 수 있음을
입증하지 못했다. 신규 P0/P1/P2 발견 수와 GO 차단 조건에서 제외한다. 세부 사항은 아래에 분리했다.

## 실제 실행 범위

```bash
python outputs/harness_r6_final_port_repros.py --target work/harness-r6-d431404/bms-balancing
python outputs/harness_r6_final_port_repros.py --libc-formats
```

- 최종 파일의 **36개 합성 사례 전부**, helper와 별도 process의 실제 `verify.main(["eval", ...])`로 실행.
  재현 script rc 0. 내부 비교 명령의 0/1/2/3은 아래에 구분한다.
- 원자료 적재·Objective 반환값·anchor는 명시적인 시험 대역이다. CSV parser, 정밀도 정책, 비교,
  CLI 종료 코드 처리는 현재 production 코드다. 실제 battery 목적함수/비공개 원자료 실행이라고 하지 않는다.
- 로컬 Python 3.12.3과 libc `snprintf`의 **533개 출력 대조: 불일치 0**.
- MATLAB은 독립 실행하지 않았다. 전체 pytest 수는 이 담당 검토에서 재측정하지 않았다.

## 닫힘을 인정한 대조군

| 축 | 실제 관측 |
|---|---|
| 전정밀도 동일 값 / `.125` vs `.1259765625` | complete/0 · model_mismatch/1 |
| R5 `%.2g`의 `0` vs `.049` | model_mismatch/1, worst_rel=1 |
| R5 `%.2g`의 `10` vs `9.6` | model_mismatch/1, 구간 초과 상대차 .0364583… |
| R5 `%.2g`의 `.0001` vs `.000096` | model_mismatch/1 |
| `%.2g`의 `10` vs `9.96` — 진짜 같은 반올림 토큰 | complete/0 |
| R5 `%.0g`의 `1` vs `4` / 정상 `1` vs `1.4` | model_mismatch/1 · complete/0 |
| fixed:10 반 단위 안/밖의 기존 두 값 | complete/0 · model_mismatch/1 |
| 중복 정밀도 선언 | invalid/2 |
| 알려진 anchor에 비숫자 값, 정상 값과 중복 | invalid/2 |
| 알려진 anchor에 비숫자 값만 + allow-partial | invalid/2; legacy 누락으로 바뀌지 않음 |
| b_PE/b_NE 헤더 이름 교환 | invalid/2, 비교 0 |
| 선언 없는 동일 값 + allow-partial | partial/3 |
| 진짜 두 열 legacy + allow-partial | partial/0, 명시된 예외 |
| V6-01 데이터 뒤의 헤더 | invalid/2 |
| V6-02 선언 없음 + sig:2 옵션 + 비정규 긴 토큰 | invalid/2 |
| V6-02 선언 없음 + sig:2 옵션 + 실제 `.12` 토큰, Python `.123` | complete/0 — 유효한 양성 대조 |
| V6-03 헤더 없음 | invalid/2 |
| V6-04 metric 열 0 + allow-partial | invalid/2 |
| V6-06 숫자 값 `# printed_format,17` | invalid/2 |
| V6-07 존재하지 않는 compare 경로 | invalid/2; traceback/갈림 rc 1이 아님 |

V6-05/08, 게시·meta·run id 및 입력 provenance는 다른 담당 범위이므로 이 표에서 독립 종결 판정하지 않는다.

## 요청 Q3 — option / declaration 정책

선언이 없으면 명시 옵션을 토큰 형식으로 검사하고, 선언이 있으면 파일 자체의 선언으로 검사한다.
현재 실행한 V6-02 양성/음성 대조에서는 신고했던 관대함의 역전이 재현되지 않았다.

문구는 한 가지 더 정확히 할 수 있다. `verify.py:1254`~`:1256`은 형식이 서로 다르다는 사실만으로
partial을 주는 것이 아니라, **이 비교의 실제 차이를 옵션이 선언보다 더 많이 흡수했는지**를 본다.

| `%.17g` 선언 + fixed:1 옵션 | 실제 결과 |
|---|---|
| CSV `.125`, Python `.126` | precision_conflict=True, partial/3 |
| CSV `.125`, Python `.125` | precision_conflict=True, override_looser=False, complete/0 |
| CSV `.125`, Python `.125000000001` | partial/3 |

따라서 요청문의 "충돌은 partial"은 문자 그대로의 무조건 규칙과 다르다. 다만 두 번째 사례는 더 엄격한
선언으로 직접 대조해도 실제로 완전히 일치하므로, 이 차이를 **잘못된 수치 일치 인증**으로 세지 않는다.
현재 집행 의미를 문서에 쓰거나 모든 충돌을 partial로 둘지 정책을 명확히 하면 충분하다.

## 도달성 미증명 stress — `token_excess`의 큰 수 중점 overflow

현재 `bms_balancing/verify.py:907`~`:915`는 이분법 중점을 `(lo + hi) / 2.0`으로 계산한다.
둘 다 유한한 큰 양수여도 합이 먼저 무한대가 될 수 있다. 최신 d431404에서도 다음 관측을 확인했다.

| case | 입력 | 실제 결과 | 안정적인 중점 대조 |
|---|---|---|---|
| `sig2_large_noise_overflow` | `%.2g`, CSV `1e308`, Python `1.0500000001e308` | excess=Inf, model_mismatch/1 | 유한한 경계 초과 상대차 ≤1e-9 |
| `fixed0_large_noise_overflow` | `%.0f`, CSV `1e308`, Python `1.000000000001e308` | excess=Inf, model_mismatch/1 | 경계 초과 상대차 약 9.99716e-13 |
| `exact_large_noise_control` | 같은 두 값, `%.17g` | complete/0, raw 상대차 약 9.99916e-13 | — |
| `sig2_scaled_noise_control` | 첫 사례를 1e308로 나눈 크기 | complete/0 | — |

재현 script는 두 stress에서도 실제 eval dispatcher를 호출하지만 **Objective를 교체해서 1e308을 공급**한다.
이것만으로 production 행의 도달성을 증명하지 않는다. 현재 `model.py:346`~`:373`의 raw RMSE는
제곱 잔차의 평균/가중평균을 계산한 후 `sqrt`를 취하므로, 해당 정상 유한 계산에서 1e308 크기의 RMSE를
생성하는 경로를 보이지 못했다. 따라서 이 stress로 정본 관측을 폐기하거나 GO를 막지 않는다.
선택적 견고성 개선은 overflow-safe midpoint와 형식의 지원 수치 범위 명시다.

## 형식 이식성 및 U15의 증거 수준

U15의 MATLAB 표본 두 건은 요청문에 명시된 사용자 실행 증거로만 취급한다. 그 범위를 한 판·두 표본으로
좁혀 적은 것은 타당하다. 이 검토에서 별도로 수행한 533건은 **로컬 libc 대조**이며 MATLAB 대조로 확대하지 않는다.
0/음의 0, 양·음 타이 후보, 10의 거듭제곱 인접값, 여러 `%g`/`%f` 자리수를 포함했고 불일치가 없었다.
음의 0 사례는 formatter 대조일 뿐, 요청문이 제외한 V6-09의 실제 RMSE 도달성을 재주장하는 것이 아니다.

공식 Python 문서는 `%g`형의 0자리=1자리, 지수 전환, 음의 0 표시를 명시한다.
[Python 3.12 형식 규칙](https://docs.python.org/3.12/library/string.html#format-specification-mini-language).
MathWorks 문서는 `%g`를 유효숫자 수와 trailing-zero 제거를 사용하는 형식으로 설명한다.
[MATLAB sprintf](https://www.mathworks.com/help/matlab/ref/string.sprintf.html).
이 일반 설명만으로 모든 플랫폼·MATLAB 판·반올림 타이의 바이트 동치를 증명했다고 하지는 않는다.

## 인계

현재 담당 검토는 R5/내부 V6의 확인한 닫힘을 인정한다. 보존된 192값이나 새 모델 설계의 범위가 붙은
관측을 뒤집는 새 수치 반례는 확인하지 못했다. 전체 GO/NO-GO는 다른 담당의 게시·입력·보고서 검토와 합쳐 판정한다.
