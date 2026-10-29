# LHS214 재발사 — WSL 증거 · S0b 독립 검토

검토 핀 `bf8cf21c6466cdb9411f9320711b871c2d1c651e` / 실제 WSL·발사 핀 B7 `35f0327377a4213774010a090df4d224e50d29e1`. 읽기 전용 검토이며 실제 발사·새 WSL 실행·물리 계산·전체 selftest 재실행은 하지 않았다.

**이 범위의 결론: Q1 ②의 지문 재결합은 확인했다. Q1 ④의 사전 점검·S1 E1/E2 보완은 아래 출처 한정을 붙여 완료로 수용할 수 있다. 새 P1/P2 코드 결함은 발견하지 않았다.** 실제 194→20 실행 완료, 저자의 ⑤ 발사 승인, 실행 직전 현장 상태, 결과·§5 관문을 이 증거로 인증하지 않는다. Q2 종합 판정에서는 이 경계를 유지해야 한다.

## 1. 원문 증거 무결성과 재현

- Downloads의 원 TGZ를 직접 열어 일반 파일 18개·디렉터리 1개, 링크·절대/이탈 경로·중복/대소문자 충돌 없음 확인. 압축을 새로 풀거나 원본을 수정하지 않았다.
- TGZ `32,197 B`, SHA-256 `9c05aef7591ad10af70af52c01508b494ddc71855322b0ce367f42f67a5be0b8`.
- 원 TGZ 파일 18개 = 반입 `bundle/` 18개 = `MANIFEST.sha256` 18/18. `receipts_sha256.txt`의 네 원문 해시도 전부 일치.
- 194 전체 로그 `4,628 B` / `6aa80dc1e75673482c13f69ab52e9f8ea1e8c6318af19e7638f4b9de34d133eb`; 보충 로그 `4,390 B` / `4bceb23d9a72f6b284949695dce9488605e613434ef1f45b8e204f8a7bd27997`. 둘 다 원 receipt의 `log.sha256`·`bytes` 일치.
- **원문 receipt를 바꾸지 않고** 현재 생산 함수 `preflight_receipt_checks` 호출. 함수의 기존 같은 디렉터리 basename 탐색이 WSL 로그를 찾았으므로 `log.path`를 수정할 필요가 없었다. PIN·지문·기대값 변경 없음.
- 194 P0–P10 **11/11**, 보충 P0–P10 **11/11**. 생산 함수 `supp20_input_receipt.receipt`는 **24/24, rc 0**, `scope=preflight`. 원 bundle의 저장된 `_verify.json`·`_receipt.json`도 각각 rc 0 / 11칸·24칸이며 승인값은 정확히 B7 40자리다.

고정 ZIP에는 입력 `docs/data`가 없어 최초 직접 `receipt()` 호출은 결손 파일 때문에 rc 1이었다. 이는 제품 판정 실패가 아니라 불완전한 검토 사본이다. 저장소를 보충하거나 고치지 않고 `verification_tree/`에 리뷰 소스의 바이트 사본과 S1의 실제 입력 파일 232개를 넣었다. **232개 모두** Git blob SHA를 다시 계산했다. 최신 B7·리뷰 핀 `docs/data` 엔트리가 같은 값이고, S1 하위 tree 응답의 SHA가 그 엔트리에 연결되며, 실제 파일 blob이 해당 tree 값과 같음을 확인했다. 원격 root→docs→data 연결 확인은 병행 identity 산출물에 있다. 그 완전한 사본에서 위 11/11·24/24 결과를 얻었다.

이 232개는 descriptor·cohort·설계·보충 수확 TGZ 등의 커밋된 자료다. **WSL 원 dump 214개를 다시 읽었다는 뜻이 아니다.** `raw_sha256_table_sha256`는 descriptor에 적힌 네 raw 해시의 표를 재계산한 값이며, 원자료 실재·같은 step 메시 문제 0은 원 WSL 로그/receipt가 기록한 사실의 일치를 검증한 범위다.

## 2. Q1 ② — 지문 재결합

독립 구현으로 `CODE_FILES` 파일 바이트의 SHA-256 지도와 정렬 JSON 지문을 계산했다. 등록 문서는 전체 역사 값이 아니라 **활성 §3**만 별도로 잘라 읽었다.

| 대상 | 독립 결과 |
|---|---|
| 봉인 | 32개 / `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` |
| 두 활성 §3 | 위 64자리와 일치 / 활성 `code_fp_pending <64 hex>` 선언 없음 |
| WSL 두 receipt·로그 | 같은 code_fp, 32, 원문 SHA=B7 40자리, dirty false |
| 실행기 | `3220be53fb89cd16c81f0273c8b9f7444f262c5311d02b2017756fd94fd66ac8` |
| 영수증 도구 | `3d6110be24d24bf91ad1e71232a2e5dad580cf95178d6135b13aa6ca6de6f950` |
| 인계 도구·배포 빌더 | 현재 바이트 해시 = 원 보충 영수증 `recorded.tool_sha256` 전부 일치 |

두 입력 지문은 생산자의 `build_plan` 결과에만 기대지 않고, 검증된 descriptor 디렉터리를 직접 열거하여 `case\tcohort` 및 `case\tcohort\tatom\tcontact\tmesh\tdeck` 표를 독립 작성하고 원 cohort TSV 바이트를 해시했다. 독립 값 = 생산 검사기의 재구성 = WSL receipt = 로그 한 줄 = 등록 문서 값이다.

| 입력 | 194 | 보충 20 |
|---|---|---|
| n / missing_raw_sha | 194 / [] | 20 / [] |
| ids_sha256 | `a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf` | `991cf1150b183f64bc69926a8b3e7c05453ec47e13b89ba3a6ad2fd2c981c694` |
| raw_sha256_table_sha256 | `da7c93f9a0887145ff171e381c8608cb79779d96aea5a595a25677dc361ef784` | `a7aaa3c8c7683f1835a096acb83ecdb055eaf5f129221f7067c5f34462807d0e` |
| cohort TSV | lhs `32f00daa8394188d1e72531fd7fda1a8b47a9c279be76311ae7f2afa024b2809`; lhsx `0b85e8589917c9a3936ce29e9f36326993985ddd113ef32353a4ff96d981cb45` | lhss `69d3f913072288b1d6b8ca8a14e43b0bc8f80e8836a8f79a9b26b2d8ed6dcaf7` |

로그의 g2/문제 0, 30⊆32, 지연 import 92/분류 밖 0, fork 0과 receipt의 대응 기록을 확인했다. 이것은 원 WSL 실행의 기록을 검증한 것이며 이번 Windows 검토에서 그 환경의 import 관측을 새로 실행했다는 주장은 하지 않는다.

## 3. Q1 ④ — S1 E1/E2와 증거의 구분

**E1은 보완됨.** 다섯 raw 로그 끝은 fast16 16/16, real4 4/4, reread 전부 통과(검사 ✓ 29개 + 종료 문구 ✓ 1개), runner 139/139, receipt 123/123이다. 다섯 명령의 바깥 셸 종료코드는 이 raw 로그 18개 묶음 안에는 여전히 없다. `runner_selftest.log` 안의 작업별 rc=0/1·음성시험 ✗를 바깥 자체시험 셸 종료코드나 전체 시험 실패로 잘못 읽지 않았다.

새 `step2_screen_paste_1028_1736.txt`에는 다섯 개 이름 각각 `rc=0`과 시험 뒤 dirty 0이 있다. SHA-256은 `49d1716cc9d700863ee196f7d1c39df593523c429ea3f1bd0cdd5f87d191c67d`. **대화에 붙여 넣어 커밋한 운영자 화면 전사**이며 원 TGZ/MANIFEST 안의 기계 로그가 아니다. 해당 파일 자체에는 독립적으로 인증된 캡처 시각이 없으므로 파일명의 17:36을 검토자가 관측한 시각으로 승격하지 않는다. S1은 바로 이런 당시 화면 기록을 회수하면 재실행 불요라고 했으므로 이 명시적 보완 방식을 수용할 수 있다. raw PASS 출력에서 rc를 추론해 채운 것이 아니다.

**E2는 출처 연결 범위에서 보완됨.** 체크리스트 3행은 반입 폴더·화면 전사·S1 독립 대조를 연결하고, 예전 표의 “미수령”은 10-24 상태임을 밝혔다. 요청서 115–126행의 채운 표는 194 여섯 칸, 원 receipt/log 해시, B7 및 “1저자 10-28 밤” 확인 기록을 연결한다. 이번 독립 대조도 여섯 칸 전부 일치한다. 확인자의 정확한 시각은 요청서 스스로 미기록이라고 밝혔으며 임의로 채우지 않았다. 인용된 “ㅇㅇ 권고대로 해”는 운영자 확인 기록으로 접수한 것이고, 검토자가 현장 손 대조 행위를 직접 목격했다는 증거는 아니다. S1 검토자 대조와 WSL 작업자 확인은 계속 다른 출처로 남는다.

단계 3·4는 별도로 receipt의 `exit_code=0`·`completed=true`, 로그 마지막 완료 표지, 검증 JSON의 `rc=0`이 모두 있다. 이 기록까지 E1의 다섯 selftest 셸 종료코드 누락과 혼동하지 않는다.

**EVID-BOUND-01 (증거 한정, 새 코드 결함 아님): 단계 0의 이름 부재 화면은 없다.** `step0.txt` 1–10행은 날짜·PIN·PY·네 경로·LOGD와 구 ROOT 두 이름을 기록한다. `head.txt`와 끝의 빈 `dirty.txt`, 두 receipt의 dirty false는 존재하지만 시작 dirty 출력과 네 이름의 당시 비존재 화면을 추가로 만들어 주지는 않는다. 구 ROOT 이름이 `ls -d`로 출력된 것은 당시 그 경로가 있었다는 범위이지 내용 불변 증명이 아니다. 요청서 106·171행이 이를 공개했다. 따라서 Q1 ④를 “모든 단계 0 사실이 원문 기계 로그로 입증됨”으로 읽으면 안 된다. 원래 절차의 실행 직전 핀·환경·dirty·새 ROOT 확인이 그대로 남는다. 이 한정만으로 이미 일치한 dry-run과 다섯 selftest 전체를 재실행할 필요는 없다.

**EVID-BOUND-02 (범위, 새 코드 결함 아님): 실제 launch 증거는 없음.** 저장·재검증한 보충 영수증 모두 `manifest=null`, `primary_manifest=null`, `scope=preflight`다. 새 ROOT 둘의 실제 manifest·같은 실제 발사 SHA·F/G/H 열·두 배치 완료/audit/등록 §5 통과를 24/24로 대신할 수 없다.

## 4. S0b 강화 판정

영수증 도구 바이트는 S1에서 123/123을 확인한 판과 동일하다. 중복된 전체 selftest를 새로 돌리지 않고 현재 `_selftest`의 `fp_state`(565–576행)와 `s0b_fp`(612–629행) AST를 **수정 없이** 추출하여 좁은 CPU 탐침을 수행했다. 실행한 범위와 S1/WSL의 123/123 기록은 별도다.

- 실문서 사본의 지문 토큰만 변경하고 실제 `registration_values()`로 읽는 원 7형: **7/7 기대 일치**. registered와 pending 두 정상형만 참. 보충만 비준, pending인데 194 활성 다름, 비준 후 대기 잔류, 194 상충 대기, undeclared는 거짓.
- 같은 두 helper에 추가 경계를 포함한 12형: **12/12 기대 일치**. 앞 63자리가 같고 마지막 자리만 틀린 두 등록, 마지막 자리만 틀린 pending, 194 활성 없음, 둘 다 활성 없음, 체크아웃 지문 없음도 거부.
- 메모리에서 보호절 하나씩 지운 4변이: **4/4 탐지**. undeclared, registered+pending 잔류, 194 파서 오류, 두 등록 동등성 각각의 가드를 없애면 겨냥한 반례가 잘못 참이 되어 탐침이 잡는다. 제품 파일은 변경하지 않았다.

**따라서 앞자리 두 상수를 제거한 변경은 정상 비준을 허용하면서 전체 64자리와 두 등록의 관계를 더 엄격하게 확인한다. 시험 약화로 볼 근거가 없다.** pending이 selftest 상태로 허용된다는 것은 발사를 허용한다는 뜻이 아니다. 실제 receipt의 D1·E2·F5·G5는 계속 활성 등록 지문만 비교한다(`supp20_input_receipt.py` 304–323, 332–361, 455–457행). S0b의 옛 입력 지문 prefix 검사도 단독 보증으로 사용하지 않았다. 같은 selftest의 S0 및 생산 B3가 전체 입력 지문을 검사하며 이번 재현은 전체 값을 직접 대조했다.

요청서가 언급한 `codex_review_lhs214_preflight_20261023.md`는 고정 ZIP에 없어 그 문서의 개별 주장을 새로 검증했다고 쓰지 않는다. 요청서가 이를 “작업 세션 사전 검토, 외부 GO 아님”으로 제한한 지위는 타당하다. 위 신규 독립 탐침이 S0b의 현재 코드 판정 근거다.

## 5. 재현 명령과 산출물

Python 3.12.14에서 실행 종료코드 0. Bash/WSL 없이 다음처럼 실행한다(경로는 옮긴 위치에 맞춰 지정).

```text
python -I -X utf8 -B verify_evidence.py --repo <fixed-review-repo> --s1 <lhs28> --identity-metadata <lhs30/independent/identity/metadata> --tgz <original-preflight.tgz> --out <output-folder>
```

`--out` 아래에만 쓴다. 검토 코드, 입력 자료, TGZ 원문은 읽기 전용이다. `verification_tree/`는 재구성용 사본이므로 최종 ZIP에 넣지 않아도 되며, 명령이 바이트 검증 후 다시 만든다. 재현에 필요한 S1 실제 자료/하위 tree metadata와 현재 identity metadata는 인자로 제공해야 한다. NumPy 등 저장소의 일반 import 의존성이 갖춰진 Python을 사용한다.

- `evidence_results.json`: 18개 raw 파일·로그·영수증·독립 지문·S0b 전체 결과 및 실제 경로.
- `verified_input_inventory.json`: 재사용 입력 232개 각각의 SHA-256, Git blob, 연결된 하위 tree.
- `production194_reverified.json`, `supp20_reverified.json`: 실제 생산 preflight 검사기 원 출력.
- `supp20_full_reverified.json`: 실제 생산 receipt 함수 24칸 출력.
- `registration_variants/`: S0b의 실제 파서 7형에 쓴 검토용 사본. 실제 WSL 자료로 사용하지 않는다.

참고: 새 `supp20_full_reverified.json`의 `recorded.git`은 Git checkout이 아닌 검토 사본의 관측이며 발사 B7 증거가 아니다. 승인 B7 대조 대상은 원 WSL receipt의 원문 `git.sha`이며 이 구분을 유지했다.
