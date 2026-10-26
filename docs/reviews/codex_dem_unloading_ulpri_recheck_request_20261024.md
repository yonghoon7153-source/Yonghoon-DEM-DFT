# DEM 언로딩 ULPRI-01/02 표지 경계 수정 재확인 요청 (2026-10-24)

**이번에 닫으려는 것:** 외부 정수 재검토가 남긴 P2 두 건의 재개 표지 무결성. **닫지 않는 것:** 실제 물리 재개·본 R·10:0 연장·U의 실행 자격, 임의의 모든 파일 문법, 새 물리값·등록 판정선. 기존 정수 반올림 교정의 수용과 이번 표지 경계 수정의 외부 재확인 대기를 구분한다.

- 외부 기준: `codex/unloading-ulpr`의 `01c1aaf5be8acdf7d1716f34cc86fc77d8e27362`, reader SHA-256 `7a395a549e8ad3eae820a9e575f094219ca7d47a4b9a07c5bc27623d7018af4b`. 이전 제출 ZIP SHA-256은 `ca2925b6044b72a7c077058c0a3cfbd00595ccc01aaa75d86daa0111da73f393`이며 변경하지 않았다.
- [외부 판정 원문](codex_review_unloading_ulpr_integer_20261024/codex_review_unloading_ulpr_integer_20261024.md): Q1 정수 파싱 교정 수용, Q2/Q3 무결성 종결 HOLD, 새 P1 없음·새 P2 `ULPRI-01/02`. 이 반례는 이전 비교 기준에도 있었고 새 물리량 오류를 입증한 것은 아니다.
- 수정 가지: `codex/unloading-ulpri`. 후보 자리: `<<sha:Reject ambiguous unloading resume markers and separators>>`. 실제 리뷰 핀은 전달 ZIP의 `PIN.txt`와 원격 전체 SHA로 확인한다. 아직 기록되지 않은 후속 전체 게이트·push 완료를 이 자리 표시로 주장하지 않는다.
- 현재 수정 reader SHA-256: `dfc06b8dbf53a8cab05df297890e1f8ca1d0fa038536c7c13ed8b8677e521723`. [증거 설명](ulpri_marker_evidence_20261024/README.md)과 [범위 한정](ulpri_marker_evidence_20261024/NOTE.md)을 함께 읽는다.

## 1. 외부 반례와 수정

| 항목 | 외부 기준의 실제 동작 | 이번 수정의 계약 |
| --- | --- | --- |
| ULPRI-01 | 정상 RESUME 옆의 `RESUME `·NBSP 변형에 k=1.49가 있어도 정상 경계만 인증, 옛 행 5개 제외, OK/rank 가능 | LF/CRLF/CR로 나눈 원 event 셀을 공용 CSV 변환 전에 검사한다. 정확한 RESUME와 앞뒤 whitespace만 다른 셀은 오류이며 정상 표지로 고치지 않는다. 오류가 있으면 정상 RESUME 공존 여부와 무관하게 `resume_auth=[]`, 옛 행 제외 0이다. |
| ULPRI-01 추가 경계 | 유일한 정상 RESUME 앞에 Unicode 줄 구분자를 붙이면 `_csv.splitlines()`가 먼저 지워, 변환 뒤 표지 검사만으로는 놓침 | 같은 원문 검사로 선행 구분자가 사라지기 전에 거부한다. 독립 검토의 8개 단일 표지 반례를 R40에 먼저 추가한 뒤 수정했다. 공용 `_csv`는 그대로다. |
| ULPRI-02 | 정상 manifest에 `note=old` + U+2028 + 잘못된 `resume_from=`을 추가하면 키 선별에서 무관한 줄로 버리고 정상 인증 유지 | manifest의 키 선별 전에 VT·FF·FS·GS·RS·NEL·LS·PS를 명시적으로 거부한다. 다른 문자열 뒤 숨은 키도 정상 기록과 함께 버려 인증하지 않는다. LF·CRLF·CR은 유지한다. |

두 음성은 실제 `arm` CLI에서 인증 없음·옛 행 제외 0·`primary_status=UNIDENTIFIED`·`rho_pct=null`·`rank_eligible=false`와 원 CSV/manifest/state 바이트 보존을 함께 확인한다. `arm`의 rc 0은 판정 JSON을 썼다는 뜻이며 승인 판정 대신 쓰지 않는다.

임의의 UNKNOWN 사건이나 소문자 사건 전체를 금지하는 새 허용목록은 도입하지 않았다. event 셀의 앞뒤 공백은 Python `str.strip()`이 공백으로 인식하는 범위다. manifest에서 거부하는 여덟 줄 구분자는 U+000B·U+000C·U+001C·U+001D·U+001E·U+0085·U+2028·U+2029다. 이를 LF로 정규화해 수용하지 않는다.

## 2. 변경 범위

기존 파일의 변경은 6개다: kit의 `ul_reader.py`, `seal_kit.py`, `active_rules.json`, `SHA256SUMS`, `README.md`와 등록 문서 §14-11의 날짜가 붙은 무결성 보충이다. 생산 동작의 수정은 `read_run`과 `_resume_auth` 두 함수이며, 같은 reader에 R40 실제 CLI 회귀와 호출을 추가했다. seal의 규칙 수는 24 그대로다.

공용 `_i`·`_csv`뿐 아니라 기존 `_resume_integer`·`_state_vars` AST도 같다. 생산 덱 64개·history 파일 16개·params는 기준 핀과 바이트가 같다. 봉인 32·공유 검사/CI·Claude 소유 파일과 원격 가지의 최종 보호 범위 감사는 root가 전체 트리에서 별도 기록한다. 기존 외부 판정문·옛 NOTE·기존 검토 ZIP은 수정하지 않았다.

정확한 decimal/scientific 정수값과 ASCII 바깥 공백의 기존 수용을 유지한다. 예를 들어 정확한 0인 `0e1000000000`은 수용되고 비정수 `3e-1000000000`은 거부된다. “큰 지수 표기는 모두 거부”라는 전칭 설명은 사용하지 않는다.

## 3. 시험과 증거의 지위

| 검사 | 현재 근거 | 범위 |
| --- | --- | --- |
| 시험 먼저 R40 | 원래 production에 새 34개 시험: 10 통과/24 실패. 1차 수정 뒤 34/34 | 당시 표지·manifest 음성과 정상 대조 |
| 원 event 경계 보강 | 8개 선행 줄 구분자 반례 추가: 1차 수정 34/42 → 원문 선행 검사 후 42/42 | 공용 CSV 변환 전에 사라지던 증거 |
| 별도 작성자 CLI | 같은 portable harness 43개: 기준 26/43 → 최종 43/43. 정상 9개 관측은 기준과 정확히 같다 | 정상 k=0/1/2/3·LF/CRLF/CR·제거 대조, 음성 34개, 입력 바이트 불변 |
| reader 전체 | 최종 reader 346/346, 그 안에 기존 R39 90개와 새 R40 42개 포함 | 내부 합성·모의 검사. 이 세 수는 더하지 않음 |
| kit 전체 직접 검사 | 13개 명령 전부 rc 0·실패 줄 0. 원본 로그·rc는 증거 폴더의 [author/kit-suite/summary.json](ulpri_marker_evidence_20261024/author/kit-suite/summary.json) | root의 공용 전체 게이트와 별도 |
| 작성자 표적 변이 | 5/5 검출, 증거 폴더의 [author/mutants/report.json](ulpri_marker_evidence_20261024/author/mutants/report.json) | 변형된 scratch source는 승인 소비자로 기록하지 않음 |
| 독립 재검토 | 동봉 독립 검토 자료와 root의 최종 인계 기록 | 작성자 검사 수와 합산하지 않음 |
| 공용 전체 게이트 | root가 최종 코드 후보에서 실행하고 영수증을 추가한다 | 이전 155/0 기록을 이번 후보의 실행으로 대신하지 않음 |

R40은 reader의 직접 자체시험에 포함된다. 현재 공용 `check_all.sh`·CI·자기검사 원장에는 이 키트 직접 검사가 배선되어 있지 않다. 공유 155개와 kit 13명령/reader 346개가 자동으로 같은 실행 범위에 들어 있다고 쓰지 않는다. 공유 파일은 이번 수정에서 고치지 않았다.

## 4. 재현과 확인 질문

고정 후보 checkout에서 다음은 합성 검사만 실행한다. 실제 LIGGGHTS·MPI·WSL·스케줄러를 호출하는 생산 명령이 아니다. 출력 경로는 새 경로를 사용한다.

```bash
python3 -I docs/data/ps45_unload_20261009/ul_reader.py --selftest
python3 -I docs/reviews/ulpri_marker_evidence_20261024/author/probe_marker_cli.py \
  --repo . --out /tmp/ulpri-marker-cli
python3 -I docs/reviews/ulpri_marker_evidence_20261024/author/run_marker_suite.py \
  --repo . --out /tmp/ulpri-kit-suite
python3 -I docs/reviews/ulpri_marker_evidence_20261024/author/mutate_markers.py \
  --repo . --out /tmp/ulpri-marker-mutants
```

1. Q1: 원 event 셀의 근접 표지가 `_csv.splitlines()`나 숫자 변환 전에 거부되는가? 정상 표지와의 공존 및 단일 표지 대체 모두 인증·옛 행 제외가 0인가?
2. Q2: manifest의 여덟 금지 줄 구분자가 키 선별 전에 거부되는가? 키 앞·뒤와 다른 문자열 뒤 위치를 포함하고, LF/CRLF/CR 정상 경계는 유지되는가?
3. Q3: 실제 arm JSON의 미식별/null·rank 불가와 입력 바이트 보존이 함께 성립하는가? 정상 k=0/1/2/3의 주 값은 중단 없는 대조와 정확히 같은가?
4. Q4: 공용 파서·기존 정수 파서·상태 파서, 생산 덱·history·params와 보호 파일의 범위 주장이 실제 diff·봉인·원본 로그와 일치하는가?
5. Q5: 정수 파싱 수용, 로컬 `ULPRI-01/02` 수정 주장, 외부 재확인 대기 및 실제 물리 실행 조건을 혼동한 문구가 남아 있는가?

이번 로컬 수정의 표지는 **claimed fixed / 외부 재확인 대기**다. 외부 HOLD 원문을 PASS로 바꾸지 않으며, 새 판의 외부 재확인과 실제 본 실행 승인은 별도다.
