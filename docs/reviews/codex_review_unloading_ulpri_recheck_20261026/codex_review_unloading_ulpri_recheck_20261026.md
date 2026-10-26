# DEM 언로딩 — ULPRI-01/02 표지 경계 수정 재확인

검토일: 2026-10-26 · 검토 가지: `codex/unloading-ulpri`

- 검토 핀: `4c29705fa1c4ba94737a858b206fa4f4c5bb2bde`
- 실제 코드 후보: `643344fee22a5d1131a59c8cd46bcf6c9a09d65b`
- 비교 기준: `01c1aaf5be8acdf7d1716f34cc86fc77d8e27362`
- reader SHA-256: `dfc06b8dbf53a8cab05df297890e1f8ca1d0fa038536c7c13ed8b8677e521723`
- 받은 ZIP: `codex-unloading-ulpri-4c29705fa1c4.zip` · 1,815,505 bytes
- 받은 ZIP SHA-256: `84aa1bf806d9008d17ef6fad9a730d6ce226ffe5bff4852101338aa9a1deb93c`
- 요청서: `docs/reviews/codex_dem_unloading_ulpri_recheck_request_20261024.md`
- 방식: 원격 고정 커밋 대조, 변경 함수 판독, 원 반례 재실행, 별도 경계 탐침, 실제 Python `arm` CLI, 입력 해시 대조. 물리 시뮬레이션·LIGGGHTS·MPI·WSL·스케줄러 실행 0. 대상 생산 소스·등록값·Git 상태 변경 없음.

## 1. 판정

**ULPRI-01과 ULPRI-02 모두 닫힘. 이번 범위에서 새 P1·P2는 발견하지 않았다.**

앞 판에서 정상 인증 한 건을 남겨 옛 행 5개를 제외하던 세 반례가, 수정판에서는 모두 `resume_auth=[]`, 옛 행 제외 0, `primary_status=UNIDENTIFIED`, `rho_pct=null`, `rank_eligible=false`가 된다. 정상 대조의 인증과 주 값은 그대로다. 원 입력 파일을 지우거나 고치지 않는다.

따라서 앞 판 Q2/Q3에 남겼던 **이 두 표지 경계의 무결성 HOLD는 해제**한다. 정확 정수 파싱 교정의 기존 수용도 유지한다. 이것은 임의의 모든 CSV/manifest 문법의 안전성 보증이나 실제 재개·본 R·10:0 연장·U의 실행 승인이 아니다. 그 물리 실행 자격과 기존 문법/복원 선행조건은 이 판정에서 다루지 않는다.

## 2. Finding별 종결

| ID | 기존 심각도 | 판정 | 닫힘 근거 |
| --- | --- | --- | --- |
| ULPRI-01 | P2 | **닫힘** | 원 event 셀에서 앞뒤 공백 변형을 먼저 기록하고, 정상 RESUME가 공존해도 인증 전체를 차단한다. 단일 표지 앞의 Unicode 구분자가 공용 CSV에서 사라지는 반례도 막힌다. |
| ULPRI-02 | P2 | **닫힘** | manifest의 여덟 구분자를 키 선별 전에 검사한다. 정상 `resume_from`이 따로 있어도 오류를 남기고 인증을 반환하지 않는다. |

### ULPRI-01 — 파싱 전 증거 보존과 인증 차단이 연결됨

소스: `docs/data/ps45_unload_20261009/ul_reader.py:329–349`.
[고정 핀 read_run](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/data/ps45_unload_20261009/ul_reader.py#L329)

1. 파일은 보편 개행으로 읽되 원문을 `split('\n')`으로 나눈다. 따라서 LF/CRLF/CR 이외의 구분자는 아직 남는다.
2. 첫 쉼표 앞 셀이 정확한 `RESUME`가 아니면서 `strip()` 뒤에만 같으면 `marker_pr`에 오류를 남긴다. 정상 사건명으로 덮어쓰지 않는다.
3. 이후 공용 `_csv`를 호출한다. `pr or marker_pr`이면 `_resume_auth`를 호출해 정상 부분만 고르는 대신 인증을 빈 목록으로 둔다.
4. 빈 인증으로 `_supersede`를 호출하므로 옛 행 제외가 발생하지 않는다. 남은 문제는 `arm_verdict`의 기록 무결성 검사로 이어진다(`:874–875`).

독립 행렬에서 Python 3.12가 공백으로 인식하는 문자 중 물리 개행 CR/LF를 제외한 **27종 × 앞/뒤/양쪽 × 단일/공존 = 162건**을 실제 CLI로 실행했다. 전부 ULPRI-01 사유를 남기며 인증·제외 0, 미식별/null/순위 불가다. 추가로 NBSP+탭 혼합 표지와 k=1.49도 거부했다.

이 결과는 유한 탐침의 범위이며 가능한 모든 문자 조합을 전수 시험했다는 뜻은 아니다. 임의 UNKNOWN 사건·소문자 사건 전체의 금지는 계약에 추가되지 않았고, 그 두 비대상 대조는 기존처럼 통과한다.

### ULPRI-02 — 키를 찾기 전에 잘못된 경계를 거부함

소스: `docs/data/ps45_unload_20261009/ul_reader.py:151–171`.
[고정 핀 _resume_auth](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/data/ps45_unload_20261009/ul_reader.py#L151)

VT·FF·FS·GS·RS·NEL·LS·PS 검사보다 `resume_from` 정규식이 뒤에 있다. 구분자가 있는 줄을 `continue`하더라도 오류 목록이 유지되어 `if pr or not rf: return out, pr`에서 인증 전체가 비워진다. 정상 키가 앞이나 다른 줄에 있다는 사실은 이 오류를 상쇄하지 않는다.

독립 행렬은 **8종 × 4위치 = 32건**을 실행했다. 키 앞, 값 뒤, 다른 문자열과 키 사이, 키와 무관한 note 문자열 사이 모두 거부했다. 마지막 부류까지 거부하는 것은 문서의 “manifest에서 여덟 구분자 거부”라는 계약과 일치한다. LF·CRLF·CR로 전체 입력 파일의 줄 끝을 바꾼 양성 대조 3건은 모두 통과했다.

## 3. 앞 판 반례의 실제 전후 값

두 판에 같은 `repro_boundary.py`를 실행했다. 경계는 `(k=1, step=3310000)`이다. 표의 `rho_pct`는 **합성 fixture의 판독값(%)**이며 실제 실험/DEM 언로딩 측정값이 아니다.

| 입력 | 기준 판 인증 / 제외 행 | 기준 판 주 판정 | 수정판 인증 / 제외 행 | 수정판 주 판정 |
| --- | --- | --- | --- | --- |
| 정상 대조 | 1건 / 5 | OK, 0.20260778734286913 % | 1건 / 5 | 동일 |
| 정확한 RESUME + k=1.49 | 0 / 0 | UNIDENTIFIED, null | 0 / 0 | 동일 |
| 정상 + `RESUME `, k=1.49 | 1건 / 5 | OK, 순위 가능 | **0 / 0** | **UNIDENTIFIED, null, 순위 불가** |
| 정상 + `RESUME` 뒤 NBSP | 1건 / 5 | OK, 순위 가능 | **0 / 0** | **UNIDENTIFIED, null, 순위 불가** |
| `note=old` + U+2028 + 잘못된 키 | 1건 / 5 | OK, 순위 가능 | **0 / 0** | **UNIDENTIFIED, null, 순위 불가** |
| 깨진 기록 없는 복구 대조 | 1건 / 5 | OK, 0.20260778734286913 % | 1건 / 5 | 동일 |

원 반례 여섯 개 모두 두 판에서 CLI rc=0이다. **rc=0은 JSON 출력 성공**이며, 음성 대조를 승인했다는 뜻으로 사용하지 않았다.

증거: `evidence/old6/result.json`, `evidence/new6/result.json`.

## 4. Q1–Q5 답

| 질문 | 답 | 근거와 한정 |
| --- | --- | --- |
| Q1 원 event 검사와 인증 차단 | **CONFIRMED** | 단일/공존 표지 모두 파싱 전에 오류 보존. 독립 162개 공백 행렬 통과. 정상 표지로 정규화하지 않음. |
| Q2 manifest 구분자 | **CONFIRMED** | 독립 32개 위치 조합 전부 거부. 전체 파일 LF/CRLF/CR 대조는 통과. |
| Q3 실제 JSON·원자료·정상 k | **CONFIRMED** | 별도 작성자 CLI를 이 환경에서 재실행한 43/43와 독립 208/208. 정상 k=0/1/2/3는 각 중단 없는 대조와 정확히 같은 0.20260778734286913 %. CSV·manifest·state 해시 불변. |
| Q4 범위·봉인·원본 로그 | **CONFIRMED, 아래 검증 범위 내** | 원격 두 커밋의 전체 변경 목록, ZIP blob, 기존 파일 6개 diff, kit 94개 비교. 생산 함수 변경 2개, 덱 64·history 16·params 동일. 공유 게이트 155는 제출 로그 감사이며 이번 독립 재실행 수가 아님. |
| Q5 수용/수정 주장/외부 판정/물리 실행 구분 | **혼동을 일으켜 판정을 막는 새 문구 없음** | 활성 요청서·NOTE·README의 10-24 보충은 기존 정수 교정 수용, 로컬 표지 수정, 외부 대기, 물리 실행 조건을 구분한다. 이 회신 이후 원문을 덮어쓰지 말고 새 종결 기록으로 두 P2 닫힘만 추가하면 된다. |

정상 scientific/decimal 표기 `1e0`, `1.0`도 별도 대조에서 유지됐다. 반대로 `1.00000000000000000000000000001`은 거부된다. `_resume_integer`는 바뀌지 않았으며, R39 회귀도 통과했다. `0e1000000000`까지 거부한다는 식의 확대 설명은 하지 않는다.

## 5. 시험이 우연히 초록인지를 겨냥한 변이

기준 소스를 고치지 않고 별도 scratch 사본에서 네 변경을 되돌렸다. 판정 기대는 독립 행렬에 사용한 동일한 복합 조건이다. **4/4 검출**했다.

| 변이 | 관측 | 검출 의미 |
| --- | --- | --- |
| 원 event 선행 검사 제거 | U+2028 단일 표지에서 인증 1건·제외 5·OK | `_csv.splitlines()` 전에 검사해야 한다는 조건이 실제로 필요함 |
| `marker_pr`의 인증 차단만 제거 | 인증 1건·제외 5이나 최종은 UNIDENTIFIED | 최종 미식별만 보는 시험이면 놓친다. 인증·옛 행 제외도 함께 검증하므로 검출 |
| manifest 구분자 검사 제거 | 숨은 U+2028 키에서 인증 1건·제외 5·OK | 원 ULPRI-02 재발을 검출 |
| 금지 집합에서 NEL만 누락 | NEL 숨은 키에서 인증 1건·제외 5·OK | 단일 구분자 누락도 검출 |

새 P2를 발견했다는 뜻이 아니다. **현재 수정이 잘못 되돌아갔을 때 이번 탐침이 실제로 실패한다**는 확인이다. 변이 사본은 승인 소비자가 아니며, 변이에서 나온 물리량은 결과로 인용하지 않는다.

증거: `probe_mutants.py`, `evidence/mutants/result.json`.

## 6. 변경 범위와 전달 증거

- ZIP 528개 항목의 경로·중복·symlink를 점검했다. MANIFEST의 527개 해시 불일치 0. MANIFEST 자신은 해시 대상에서 제외된다.
- SOURCES의 **524개**에 대해 길이·SHA-256·Git blob SHA-1을 실제 바이트에서 다시 계산해 불일치 0.
- 원격 후보 커밋의 파일 목록을 100개씩 끝 페이지까지 읽었다. 후보 408경로 + 최종 증거 추가 17경로 = **425경로**, 전부 ZIP에 같은 blob으로 존재한다. 나머지 **99개 지원 파일**은 앞 판에서 검증했던 로컬 기준 스냅샷과 바이트가 같다.
- 후보의 기존 파일 수정은 요청서대로 **6개**다. 마지막 핀은 코드 후보를 부모로 하며 새 증거·완료 기록만 추가한다. `scripts/`, `webapp/`, 공유 CI·검사·원장 등 다른 기존 파일의 변경은 없다.
- kit는 **94개**. 바뀐 5개는 reader·seal·활성 규칙·SHA256SUMS·README뿐이다. 여기에 사전등록 보충 1개가 더해져 총 6개다.
- reader AST 변화는 `_resume_auth`, `read_run`, 자체시험 연결 `selftest`; 새 함수는 `_resume_marker_tests`다. 따라서 **생산 동작 함수 2개**라는 설명은 맞다. `_i`, `_csv`, `_resume_integer`, `_state_vars`는 동일하다.
- 생산 덱 **64/64**, history **16/16**, `unload_params.json` 동일. 봉인 검사 **76파일**, 활성 규칙 **24**, 실패 0. 생성 문자열 대조도 생산 덱 64개와 history 덱 9개/STL에서 일치했다.
- 작성자 kit 13개 로그를 실제로 다시 읽어 해시·성공/실패 줄을 대조했다. 원본 rc 기록은 모두 0, 실패 줄 0. **이번 검토에서 Linux 13명령을 전부 다시 돌렸다는 뜻은 아니다.**
- 작성자 실행 뒤 README만 한 문장 바뀐 주장도 검산했다. 최종 README에서 그 정확한 문장 변경을 역적용하면 당시 시험 README 해시가 복원된다. 소스·봉인·등록 파일의 사후 변경은 없다.
- 공유 게이트 로그는 성공 항목 **155개 + 결론 1줄**, 실패 항목 0이다. 로그 해시는 영수증과 같다. source-manifest 836항 중 ZIP에 있는 95항의 실제 바이트 해시는 모두 일치한다. 이번에 836개 전부를 다시 받아 실행한 것은 아니다. kit 직접 검사가 공유 155 레인에 배선되지 않았다는 한정은 유효하다.

증거: `intake.json`, `remote_scope.json`, `remote_candidate_modified.json`, `remote_final_commit.json`, `scope.json`, 각 `.diff`, `receipt_audit.json`.

## 7. 실행 환경과 실패를 숨기지 않은 기록

독립 환경은 Windows, Python 3.12.14이다. 초기 기본 sandbox 임시 폴더에서 접근 오류가 발생해 작업 폴더 아래 임시 경로로 옮겼다. 이는 판독 대상의 반례가 아니며 실패 로그를 보존했다.

그 후 수정하지 않은 `--selftest` CLI는 **311통과/35실패**를 냈다. 실패 33개는 새 R40 음성에서 최종 JSON이 정확히 미식별/null인데 자식 프로세스의 콘솔 출력 rc가 1이 된 경우이고, 나머지 2개는 기존 문법 재판독 양성이다. 실제 stderr는 다음과 같다.

```
UnicodeEncodeError: 'cp949' codec can't encode character '\u2014'
```

`-I` 자식 Python은 환경변수 `PYTHONUTF8`를 무시한다. 자식 명령에 **`-X utf8`만 추가**한 진단 실행에서는 reader **346/346**, 실패 0이다. 대상 함수·판정·fixture 바이트를 수정하거나 rc를 바꾸지 않았다. 따라서 이 결과를 “원명령 그대로 Linux 346/346을 독립 재현”했다고 쓰지 않는다.

`make_unload_decks.py --check`도 같은 자식 인코딩 문제로 최초 실패했다. 같은 실행 옵션 보정 뒤 덱 64개와 봉인을 모두 통과했다. 직접 `seal --check`, seal 자체시험 12건, history 생성 대조는 원 명령에 부모 `-X utf8`를 준 상태에서 통과했다.

독립 208건 및 작성자 43건 재실행은 실제 소비자 CLI에 `-I -X utf8 -B`를 명시하여 실행했다. 판정 JSON·입력 해시·rc를 함께 확인했다. Windows 인코딩 문제는 앞 판에도 있었으며 이 표지 패치의 새 회귀 또는 Linux 생산 실패로 등재하지 않는다.

| 이번에 수행한 검사 | 결과 |
| --- | --- |
| 원 반례 6개, 앞 판/수정판 | 앞 표와 같이 전후 재현 |
| 작성자 portable CLI 43개 재실행 | 43/43 |
| 별도 작성한 경계 행렬 | **208/208**: 음성 199, 양성 9 |
| scratch 표적 변이 | 4/4 검출 |
| reader 전체, 자식 UTF-8 옵션 보정 진단 | 346/346; R39 90·R40 42 포함 |
| seal 자체시험 / check | 12/12 / 76파일·24규칙 |
| 생산 덱 생성 대조, 자식 UTF-8 보정 | 64/64 |
| history 덱/STL 대조 | 덱 9·봉인 15파일 일치 |

각 수는 중첩되는 보증이므로 합산해 “총 검증 수”로 부풀리지 않는다. 공유 155와 작성자 kit 13명령의 원본 감사도 이 독립 실행 수에 합산하지 않는다.

## 8. 우리 트리 재현 명령과 남은 경계

아래는 **합성 판독 시험**이다. 고정 핀 checkout을 `$REPO`, 이 검토 묶음 폴더를 `$REVIEW`로 놓는다. 각 출력 경로는 새 경로를 사용한다. Linux에서는 Python3로 직접 실행 가능하며 NumPy가 필요하다.

```bash
python3 -I -X utf8 -B "$REPO/docs/data/ps45_unload_20261009/ul_reader.py" --selftest
python3 -I -X utf8 -B "$REVIEW/probe_independent.py" --repo "$REPO" --out /tmp/ulpri-independent-new
python3 -I -X utf8 -B "$REPO/docs/reviews/ulpri_marker_evidence_20261024/author/probe_marker_cli.py" --repo "$REPO" --out /tmp/ulpri-author-replay-new
python3 -I -X utf8 -B "$REVIEW/repro_boundary.py" --repo "$REPO" --out /tmp/ulpri-original-six-new
python3 -I -X utf8 -B "$REPO/docs/data/ps45_unload_20261009/seal_kit.py" --check
python3 -I -X utf8 -B "$REPO/docs/data/ps45_unload_20261009/make_unload_decks.py" --check
```

검토 묶음에는 실행 당시 입력과 결과를 포함했다. `probe_mutants.py`는 묶음 안 `snapshot/`과 `evidence/matrix_v2/`를 기준으로 네 변이를 재현한다. 기존 `evidence/mutants/`를 덮어쓰지 않도록 새로 추출한 사본에서 출력 경로를 별도로 지정하거나 해당 스크립트의 출력 폴더만 새 이름으로 지정한다. `diagnose_utf8.py`와 `diagnose_deck_utf8.py`는 Windows 인코딩 문제를 분리한 진단용이며 생산 소비자 소스가 아니다.

실제 언로딩의 정확도, 실제 체크포인트 복원, U 자격화, 본 R/10:0 연장, 모든 이벤트 이름/파일 문법의 유효성은 이 회신으로 닫지 않는다. 이번 변경은 그 물리 질문의 답이나 등록 임계값을 바꾸지 않았다.

**GO — ULPRI-01/02 표지 경계 무결성 수정의 종결에 한정. 실제 물리 실행 승인은 별도.**
