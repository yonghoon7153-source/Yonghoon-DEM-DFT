# 문법 출처 · history/EXT/UC 독립 검토

핀 `eaecfba2a2dfbff6f13222f6afeb01d8ebeb5a84`. 대상 원본은 읽기만 했다. 실제 LIGGGHTS·MPI·스케줄러를 호출하지 않았고 Git 상태를 바꾸지 않았다. 아래 키트 경로는 `source/docs/data/ps45_unload_20261009/` 기준이다.

## 결론과 Q4/Q6 답

이 범위에서 새 실행 차단 결함은 찾지 않았다. 이전 ULKRR-01의 타입 오류는 입력을 세 개로 바꾸어 고쳤고 타입 음성 검사도 판별력을 보인다. 그러나 실제 ibb 실행 2 PASS는 여전히 없다. 이 범위의 남은 해제 증거는 **고정된 실제 바이너리로 얻은 문법 PASS의 원 보고 묶음 검토**다. 체크리스트 JSON 또는 모의 PASS 하나를 실제 실행 증거로 취급하면 안 된다. 다른 ULKRR 수정에 대한 최종 판단은 별도 독립 검토와 합쳐야 한다.

Q4의 자동 사전 점검은 본 R·RJ2·EXT 전에 실재한다. 동일 덱·판·바이너리를 결합하고 누락/잘못된 상태를 막는 목적에는 맞다. 러너/판독기 해시를 최신판과 무조건 같게 강제할 필요는 없다. `039abb141`의 알려진 판독 규칙과 동일 덱으로 얻은 실제 PASS를, 실패 뒤 후속 실행만 막은 새 러너 때문에 폐기할 이유가 없다. 다만 **어떤 임의 판독기라도 같은 덱이면 증거 자격이 있다는 일반화는 부당하다**. 원 보고 묶음의 당시 판독기·표 출처를 확인하거나 승인된 판독기로 원자료를 다시 읽으면 된다. 런마다 자동 재계산은 앞 판정의 최소 해제 조건이 아니었고 이 핀은 캐시된 판정을 신뢰한다고 명시했다.

Q6은 조건부 동의: 다른 독립 범위가 닫히고 실제 실행 2의 원자료·출처를 확인하면 본 R·10:0 연장의 문법 선행 조건이 채워진다. UC는 새 시도만 허용하는 구현과 문서가 맞는다. 새 폴더·`prior_attempts` 기록은 재시도 한도/먼저 나온 유효 결과의 선택을 자동 집행하는 장치가 아니며 이 판단이 1저자에게 남는다는 문서 한정은 유지해야 한다.

## 독립 실행: 타입 6건 + 출처 17건

`probes/grammar_types.py`는 실제 `make_history_decks.fix_output_problems()`를 호출했다. 현 세 입력+`f_gr_av[1]` 및 한 입력+`f_gr_av`는 문제 없음; 옛 한 입력+`[1]`, 세 입력+scalar 접근, `[4]`, `[999]`는 각각 문제로 판별했다. `GRAMMAR_INPUTS`의 덱 둘/판 STL 해시도 실제 세 파일과 모두 같았다. 결과 `evidence/grammar_types.json`.

수정 근거: `history_test/in.hist_grammar.liggghts:77–80,135`; 생성기 `:825–828,860`. 기존 고정 C++의 `fix_ave_time.cpp:350–368`은 SCALAR mode 입력 하나는 scalar, 둘 이상은 크기 nvalues의 vector이며 `variable.cpp:1198–1201`은 벡터 접근/상한을 대조한다. 이번 독립 확인은 타입 오류 수정 증거이며 실제 런 성공 증거가 아니다.

`probes/grammar_provenance.py`는 대상 history 합성 헬퍼로 양성 파일을 만들고 실제 `read_history.grammar_info()`로 PASS JSON을 만든 다음 독립 변형을 가했다. 실제 바이너리 대신 명시적으로 합성인 해시를 썼다. 실제 `ul_reader.grammar_prereq()` 호출 17건:

- 실제 현재 판독기 양성 1건: raw PASS, preflight 허용.
- 음성 11건: 다른 바이너리, 검사 누락, bool exit code, int 1 검사값, false 검사값, 다른 run_dir, GA rc1, manifest end 누락, 덱 바이트 변조, 판 바이트 변조, deck.txt 이름 오류. 모두 거부.
- 캐시 신뢰 경계 4건: PASS JSON을 그대로 두고 GA 화면 ERROR 추가, GB mesh z를 99로 바꿈, GB 화면 삭제, GB 상태 파일 값 변경. 실제 raw 판독기는 모두 FAIL이나 preflight는 모두 허용.
- 스크립트 해시 경계 1건: kit 봉인에서 runner/reader 해시만 바꾸고 manifest의 봉인 해시도 맞춤. preflight 허용. 알려진 설계의 재현이며 스크립트 동치성 증명은 아니다.

결과 `evidence/grammar_provenance.json`; 개별 입력 `evidence/grammar_cases/`. 기대 관측 17/17은 마지막 다섯 사례가 안전 거부됐다는 뜻이 아니다. **자동 관문은 raw logs를 다시 인증하지 않는다**는 재현을 포함한다. 이를 새 미고지 결함으로 올리지 않고 Q4의 명시된 제한과 실제 보고 묶음 검토 필요성을 기록한다.

핵심 코드: `ul_reader.py:1224–1310`, 특히 JSON 검사 `:1238–1260`, run/manifest/LMP `:1261–1274`, 봉인 `:1275–1292`, 단계 rc·deck·plate `:1293–1308`. 실행 전 위치는 `run_unload.sh:93–102,123,137–138`, 잡 증거 기록 `:169`; 다음 복원 관문은 `ul_reader.py:1013–1024`의 `grammar_prereq=PASS` 줄을 요구한다. 그 줄은 사전 점검이 있었다는 잡 영수증이며 원 로그 재검산의 대체물이 아니다.

## history / EXT / UC 수정의 닫힘 범위

| 경로 | 소스 | 제출 Linux 실행 근거 | 판단 |
|---|---|---|---|
| P → GA, GA → GB | `history_test/run_history.sh:130–143` | `after_fix_82d532c60/history_read_history_selftest.log:57–58` S38/S39 | 선행 rc0과 파일 둘 다 필요. 파일을 쓴 뒤 실패한 단계로 이어 가지 않음 |
| H0–H5 P → 소비 | 같은 파일 `:154–165` | 같은 로그 `:59` S40 | 선행 rc0과 fixture 필요. 별도 PZ→CZ 대조는 계속 가능 |
| EXT 프로그램 오류 rc1 | `run_unload.sh:249–262` | `after_fix_82d532c60/ul_runner_test_selftest.log:32–33` M21/정상 rc2 대조 | rc1은 EXT2 없이 보존. rc2+끝 체크포인트만 EXT2 |
| 본 R·EXT 전 문법 | `run_unload.sh:93–102,123,137` | 같은 로그 `:34–37` M22 | 누락·FAIL·덱·LMP 다름은 실제 모의 러너에서 LMP 호출0. 양성은 현재 history 러너/판독기로 생성 |
| UC fresh-only | `run_unload.sh:54–58,157–170` | 같은 로그 `:39–40` M24 | RESUME UC가 사전 점검/복사/잡 기록 추가 전 거부. 보존된 `<JOB>.*` 디렉터리 이름을 새 manifest에 남김 |

위 로그 경로의 접두어는 `source/docs/reviews/dem_unloading_kit_reverify_fix_evidence_20261014/`. 해당 두 로그는 전문과 rc0을 포함한다. 별도 `grammar_039abb141_probe/grammar_039_probe.json`은 옛 runner/reader 조합의 모의 PASS가 새 관문을 통과함을 보여 주지만 실제 ibb PASS를 대신하지 않는다.

EXT에 관한 문구는 좁게 유지한다. `ul_reader.py:2944–2946`은 s0p의 PASS 이외 상태를 모두 rc2로 매핑하고 `:1505–1527`에는 NOT_COMPUTED/조건 미계산도 있다. 따라서 수정이 입증하는 것은 “예상 못 한 프로세스 rc1을 rc2와 구분해 멈춘다”다. rc2만으로 반드시 유효한 압력 조건이 측정되어 물리적으로 실패했다고 확대하지 않는다. 이는 이번 수정의 회귀/새 거짓 승인으로 판정하지 않았다.

## 환경 한계와 재현

WindowsApps bash는 OSError 1920, 별도 Git Bash의 무해한 `exit 0`조차 `NtCreateDirectoryObject ... 0xC0000022`, 프로세스 rc3221225794로 실패했다 (`grammar_types.json`). 따라서 이번 환경에서 Bash 러너를 독립 재실행했다고 쓰지 않는다. 셸 경로는 소스 검토와 제출된 Linux 전문/rc 증거로 확인했다.

본체 자체시험의 로컬 결과는 **157/158, R32 양성 하나 실패**로 그대로 보고해야 한다. 이를 조사한 `probes/grammar_windows_r32.py`는 실제 `_mk_gram`을 호출했다. `ul_reader.py:2044,2819–2820`은 LF가 든 UTF-8 문자열을 해시하지만 `_w`의 Windows 텍스트 쓰기는 덱/STL에 CRLF를 쓴다. P/GA/GB의 여섯 사본 모두 그 차이만 있었고, 관문은 정확히 그 여섯 해시를 거부했다. 새로 만든 검토 fixture의 여섯 파일만 LF 바이트로 쓰자 **동일한 원본 grammar_prereq가 허용, problems=[]**가 됐다. 원본 수정은 없다. 증거 `evidence/grammar_windows_r32.json`. 이는 자체시험 fixture의 Windows 이식성 결함이며 Linux 실행 결과를 부정하거나 운영 관문을 우회해야 할 이유가 아니다. 앞 독립 양성은 실제 봉인 입력을 바이트 복사해서 처음부터 PASS였다.

재현 (동봉 검토 폴더에서):

```text
python -X utf8 -B probes/grammar_types.py
python -X utf8 -B probes/grammar_provenance.py --run-id repeat1
python -X utf8 -B probes/grammar_windows_r32.py
```

출처 탐침은 기존 사례를 지우거나 덮지 않는다. 다시 실행할 때마다 새로운 run-id를 고른다. source 파일은 수정하지 않는다.
