# 봉인 꼴 독립 하위검토 — Q1 · Q5 · Q6

**판정: 이 범위에서 새 P1 0, 새 P2/P3 0. 봉인본을 새 파일로 두는 꼴, stoic 참조·등록부 처분, 코드 핀 자료의 승계를 조건부 수용한다. 전체 R의 GO 판정이나 실제 봉인 완료를 뜻하지 않는다.**

리뷰 핀 `f40d005acce19b6c363e5c10c8668ec081b56f2e`, 코드 핀 `64e4d213e8267bafaf3ae5af00a42996cefd3f33`, 후보 커밋 `c80d700bdd5915da82f77f839cb96ed4a5a6582e`를 구분했다. 제출된 내부 리뷰의 PASS를 독립 판정으로 세지 않고 아래 검사를 별도로 수행했다. 요청서 §10의 알려진 한정은 새 결함으로 등록하지 않았다.

## 1. 독립 결과

| 검사 | 기대 | 실제 | 증거 |
|---|---|---|---|
| 제출 형식·명령 별도 검사 | 원본+표지 한 줄, 입력/출력 해시, 계획 꼴·S0 허용오차, 실행 문서의 등록 경로 일치 | **52/52 PASS**; sh 사슬 13+14개, S0 각 1개가 봉인본을 명시; 원본 sh 실행 0개 | `logs/audit_supplied_form.json` |
| 실제 도구로 후보 재생성 두 번 | 두 생성 결과와 제출 4파일이 바이트 단위 동일 | **동일**; 봉인본 `3787864a…`, 원본 자리 `1cf4a7b4…`, 명령 문서 `bef29b6b…`, 계획 `f09b3efb…` | `logs/probe_form_build.json` |
| 생성기 반례·경로 대조 | final의 null, 틀린 허용오차/길이법칙/SV문턱/날짜/가지 거부; fixture final과 입력파일 이동은 정상 | **11/11 PASS** | 같은 로그 |
| 실제 S0 관문 + 소형 독립 Git 역사 | 후보/원본은 거부, fixture final 새 등록 경로는 수용, 바뀐 계획 해시 및 옛 후보는 거부 | **6/6 PASS** | `logs/probe_s0_gate.json` |
| 핀·등록부·참조의 Git/JSON 독립 대조 | 코드 경계 무변경, claims의 허용 경로만 추가, q14 및 stoic 지시 객체 일치 | **19/19 PASS** | `logs/audit_pin_boundary.json` |

모든 시험값은 **시험 전용**이다. `max_ladder_points=12`, `calib_rj_ratio_max='none'`, `sv_cf_threshold=2.0`, `sv_cf_scope='all3'`를 fixture에서만 사용했으며 실제 네 미정값의 결정이나 권고로 제출하지 않는다. 마지막 해시 불일치 시험의 `sv_cf_threshold=3.0`도 시험 전용이다.

## 2. Q1 — 새 파일과 원본 경로

수용한다. 원본 자리의 해시 공란을 남기고, 새 파일에 해시와 계획 블록을 함께 넣는 구조는 두 계획의 바이트 결속을 보존한다. 생성기는 원본/명령/사슬의 핀 해시를 검사하고(`make_sealed_copy.py:249`), 정준 계획을 확인한 뒤(`:267`) 두 계획을 대조하며(`:282`), final의 필수값을 확인한다(`:288`). 생성 후 사슬의 실제 파서로 해시·블록·원본 공란을 다시 확인한다(`:346`). 후보를 두 번 실제 생성해 제출 바이트와 같음을 확인했다.

사슬의 원본 해시 공란은 `rint_r_chain.py:1145–1169`에서 `PLAN_HASH_UNREGISTERED`/`S0_PLAN_HASH_UNREGISTERED`로 거부된다. 사다리는 러너를 만들기 전 등록 해시·블록·S0 계획·필수값을 검사한다(`:6654–6659`, 러너 생성 `:6683`). 예측/합치기의 등록 검사도 각각 `:6880`, `:7347`에 있고 최종 판정은 `:7715–7735`에서 다시 읽는다. 재검증은 이전 판정에 기록된 등록 경로를 사용하고(`:8260`) JSON 두 개의 바이트를 대조한다(`:8268–8269`). 경로 이동이 자동 수용의 근거가 되지는 않는다.

S0의 새 `r_doc` 역시 임의 작업파일을 신뢰하는 방식이 아니다. 지정 커밋의 실제 문서와 계획을 읽어 해시를 검사하고(`ca_s0_census.py:943–958`, `:978–984`), 필수값과 두 계획을 대조한다(`:989–1000`). 독립 소형 Git 시험에서 후보의 새 문서는 네 null로, 원본은 S0 해시 공란으로 거부됐고, 시험값을 넣어 도구가 다시 만든 새 문서만 통과했다. HEAD가 뒤로 진행해도 옛 후보를 지정하면 여전히 거부됐다.

`ledger --init`, recover 같은 운영 단계가 등록 파서를 반드시 읽는다는 주장으로 넓히지 않는다. 중요한 것은 계산·결과 수용 단계의 관문이다. 요청서 §10의 시도/판정 폴더 소비와 원장 init 예외는 그대로 한정이며 새 결함이 아니다. 정직한 원본 누락·오래된 후보·계획 사본 불일치에서 틀린 결과를 받는 반례를 찾지 못했다.

## 3. Q5 — 참조와 claims

수용한다. 후보의 `claims.json`을 코드 핀 것과 실제 객체로 비교했다. `claims`의 내용/상태와 모든 비-ban 최상위 칸은 동일했다. 42개 철회 패턴 가운데 두 항목의 `allowed_in`만 변했고, 각 항목에 11-13/11-16 S0 사본의 **정확한 파일 경로 두 개**가 추가됐다. 삭제·와일드카드 확대·주장 지위 변경은 없었다. 후보 blob은 제출된 stoic blob `3f83245436d927dc534880fa32a958bc99ce7ddf`와 일치한다. 이것은 철회값을 새 주장으로 되살리는 변경이 아니다.

q14 두 파일은 후보 Git blob 및 ZIP 바이트를 따로 비교해 일치했다. `block_manifest.json`=`b3e47a30d21c457136ab02b6116683e8758e899f`, `s0_preregistration.md`=`b0f35d9780e6babf71bf05807195f9e184a32abc`다. 두 파일을 넣는 처분은 측정 폴더의 결과 전 등록/블록 출처 연결을 유지한다.

3판 문서를 후보에 복제하지 않는 처분도 고정 커밋·경로·blob/tree를 함께 보존하면 수용할 수 있다. `b3481336c:docs/reviews/rint2_time_reestimate_20261111/README.md`의 blob `8e4781ac4e89b5968e788ed21d486824ed3fcf45`와 같은 커밋의 `v3` tree `b07ecf38e1fa620b3b9e81fc51b0f282670cfb1f`를 실제 로컬 Git 객체로 독립 확인했다. 원격 가지의 현재 도달 가능성을 이번 하위검토에서 새로 측정했다는 뜻은 아니다. 봉인 직전 참조 도달 확인은 남는다.

## 4. Q6 — 측정 코드 핀 승계

수용한다. 후보의 부모가 코드 핀임을 직접 확인했고 변경 83파일은 A79/M4/D0이었다. 개발 탐침 원장의 다섯 경계 경로, 사슬 `CODE_FILES` 20개, `S0_SAME_FILES` 7개에 대해 코드 핀↔후보의 Git diff가 모두 비어 있었다. 따라서 후보 문서 커밋이 탐침/조립/S0 코드를 바꿨다는 반증은 없다.

`claims.json`은 풀이 코드 경계 밖이지만 규율 검사 입력 안이라는 점은 그대로다. 독립 JSON 대조는 허용 경로 변화만 확인한다. 실제 최종 봉인 때 정해진 계획·날짜·가지·증거로 최종 게이트를 다시 수행한다는 조건을 생략할 근거가 되지는 않는다. Q11의 수치 결과 자체와 측정 채택 판단은 다른 하위검토 범위다.

## 5. 재현과 한계

작업 루트는 `<WINHOME>/Documents/Codex/rint2_seal_round2_review_20261117`이다. 입력과 `candidate_source`는 읽기만 했다. 모든 쓰기는 이 하위검토 폴더의 scripts/logs/work 또는 시스템 임시폴더에서 했다. 엔진, 실침대, 현장 기계, 실제 R 결과/σ, 실제 봉인·push를 실행하거나 열람하지 않았다.

로컬 소형 시험 환경은 Python 3.12.14 / numpy 2.3.5 / scipy 1.16.3이다. 현장 봉인 환경 3.8 / 1.24.4 / 1.10.1의 실행 확인을 대신하지 않는다. Windows의 stdout CRLF 차이를 제거하기 위해 **사슬 plan-doc의 stdout만 LF로 설정**한 뒤 원본 사슬을 실행했다. 도구/사슬 소스 및 결과 계획 바이트는 변경하지 않았다. 따라서 실제 Linux CLI 전체를 재실행했다는 주장은 하지 않는다.

```powershell
$py='C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1112-611-0_26.1112.611.0_x64__3k8sg7r9htsxt/dependencies/python/python.exe'
$review='<WINHOME>/Documents/Codex/rint2_seal_round2_review_20261117/seal_form_review'
& $py -I -B -X utf8 "$review/scripts/audit_supplied_form.py"
& $py -I -B -X utf8 "$review/scripts/audit_pin_boundary.py"
& $py -I -B -X utf8 "$review/scripts/probe_form_build.py"
& $py -I -B -X utf8 "$review/scripts/probe_s0_gate.py"
```

`work/scripts`는 후보 scripts의 바이트 사본이고, `work/deps`는 소형 시험용 scipy 1.16.3이며 배포 산출물에서 제외해도 된다. 재현 시 이 두 경로를 준비한다. `work/TEST_ONLY_final_output`은 시험 고정물이며 실제 봉인 출력으로 가져가면 안 된다. Git 호출은 해당 경로의 `safe.directory`, `GIT_NO_LAZY_FETCH=1`, `GIT_OPTIONAL_LOCKS=0`을 명시했다.

전체 사슬/e2e/저장소 게이트·실기계 복구/전송의 독립 통과로 범위를 넓히지 않는다. 요청서 §10의 미확인 사항을 이 하위검토가 닫지 않았다. 실제 봉인 GO에는 실제 네 값의 1저자 결정, `--final` 재생성, 최종 문서/계획/해시/경계/게이트 대조, 지정 봉인 커밋에서의 양 기계 확인이 여전히 필요하다.
