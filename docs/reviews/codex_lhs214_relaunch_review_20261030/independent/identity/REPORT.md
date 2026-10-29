# LHS214 핀·소스·입력 동일성 독립 검토

판정: **요청된 동일성 범위 PASS. 새 발사 차단 결함 없음.** B7와 리뷰 핀 사이의 CORE40, 명시된 AST 방법의 closure78, 입력16 경로가 모두 같다. 이 결론은 발사 승인이나 생산 결과 검증이 아니다.

- B7 / 발사 핀: `35f0327377a4213774010a090df4d224e50d29e1`
- 리뷰 핀: `bf8cf21c6466cdb9411f9320711b871c2d1c651e`
- 저장소: `yonghoon7153-source/Yonghoon-DEM-DFT`
- 실행: 로컬 CPU의 표준 라이브러리 AST·해시·JSON·텍스트 대조만. 제품 모듈 import, Git checkout/fetch/ref 변경, 게이트·시뮬레이션·WSL·SLURM·생산 실행 없음.

## 독립 검증 결과

| 검사 | 실측 | 판정 |
|---|---|---|
| B7 → 리뷰 핀 계보 | ahead 73, behind 0, merge-base = B7 | PIN의 73 일치 |
| Git tree 무결성 | 15/15 객체를 원시 Git tree 직렬화로 SHA-1 재계산; 두 root는 commit.tree에 결합 | PASS |
| 전달 ZIP의 repo 파일 | 70/70 실제 바이트의 Git blob SHA가 리뷰 핀 tree entry와 일치 | PASS |
| CORE | B7 40 / 리뷰 40, 같은 경로 집합, SHA·mode·type 변경 0 | PASS |
| AST 닫힘 | B7 78 / 리뷰 78, 같은 경로 집합, SHA·mode·type 변경 0 | PASS |
| 봉인 지문 | 32개 실제 소스 SHA-256 지도에서 독립 계산 | `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` |
| 입력 경로 | 16/16 실재 및 동일: subtree 10 + blob 6 | PASS |
| check_all.sh | 추가 25줄, 삭제 0줄; 실제 run 추가 10줄 | 요청·PIN과 일치 |
| selftest_inventory.tsv | 추가 2행, 삭제 0행; kg50 도구 둘 | 요청·PIN과 일치 |
| LHS 등재 | 전체 7행 바이트 동일; 첫 4열 SHA-256 = `518404403cd14882969565c0803b25fc5b408782a49cb43b9c2c9650e4274f0e` | PIN 접두 일치 |
| fast 드라이버 | 호출 문장 동일, B7 428행 → 리뷰 453행; 드라이버 소스 blob도 동일 | PASS |
| 소스 캐시 | closure78 + 등록2 = 80개, 모두 핀의 Git blob과 대조, missing 0 | PASS |
| 이동 재현 | 외부 lhs28 캐시 없이 전달 입력만 새 위치에 복사 후 재실행 rc 0 | PASS |

GitHub의 compare 응답은 파일 목록 300개 제한에 걸리므로, 변경 목록의 부재를 동일성 근거로 쓰지 않았다. 비교 API는 계보·커밋 수에만 쓰고, 파일 동일성은 각각 고정 핀에서 가져온 완전한 비재귀 tree를 연결하여 검사했다. 두 commit의 root tree는 각각 `c7e09ebdaafcb3d993d9946541d94b17002c879b`, `53bc9f1bb39921e2d6ceb6e5fb0fb53b27023c4d`다. 따라서 저장소 전체가 같다는 판정이 아니다.

원격 근거: [B7 commit](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/commit/35f0327377a4213774010a090df4d224e50d29e1), [리뷰 commit](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/commit/bf8cf21c6466cdb9411f9320711b871c2d1c651e). 원 응답은 `metadata/`에 보존했다.

## 소스 그래프와 한정

CORE40을 PIN 문장으로 복사하지 않고 실행기 AST의 `CODE_FILES` 32개와 `HANDOVER_FILES` 2개에서 구성했다. 여기에 빌더·실행기·영수증·스모크 4개와 등록 문서 2개를 더했다. [실행기 198–208행 및 252행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf8cf21c6466cdb9411f9320711b871c2d1c651e/scripts/run_network_194_parallel.py#L198)

closure78은 봉인32 + 도구6을 시작점으로 모든 함수 안까지 AST를 걷고, `import`, 절대 `from ... import`, 리터럴 인수의 `.import_module(...)`를 scripts → webapp의 최상위 `.py` 파일에 해석하는 요청서의 정확한 방법을 두 핀에 각각 적용했다. 결과는 32 + 6 + 40 = 78개이며 해석된 내부 의존 간선은 280개, 복수 후보 모듈 이름은 0개다. 소스를 하나도 읽지 않고 문서의 추가40 목록만 대조한 결과가 아니다. [실행표 A-C 375–408행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf8cf21c6466cdb9411f9320711b871c2d1c651e/docs/reviews/lhs214_relaunch_exec_sheet_20261027.md#L375)

다만 이 78개를 모든 런타임 경로의 완전한 닫힘이라고 확대하지 않는다. 해당 방법은 상대 import, 변수로 정하는 import 이름, `spec_from_file_location`, 하위 프로세스·셸 실행, 외부 패키지를 일반적으로 풀지 않는다. 이번 소스에는 별도 기록한 동적 호출 17개와 상대 import 구문 2개가 있다. 예를 들어 `make_mixer_deck.py:3130`은 경로로 `make_mixer_baffles.py`를 읽지만 그 파일은 이 78개에 포함되지 않는다. 이는 정해진 78 동일성을 깨지 않으며, 믹서의 다른 경로까지 검증했다고 주장할 근거도 아니다. 실행기 자체도 변수 경로의 동적 적재는 정적으로 풀지 않는다고 명시한다. [실행기 1169–1173행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf8cf21c6466cdb9411f9320711b871c2d1c651e/scripts/run_network_194_parallel.py#L1169)

`identity_results.json`의 closure.graph에는 두 핀의 경로·간선·해석되지 않은 이름·동적 구문을 모두 보존했다. 78 동일성은 이번 메타데이터·AST 검증이고, 실제 생산 import 관측의 성공은 별도의 런타임 증거다.

## 입력16의 의미

16개 목록은 요청서 부록 B의 IN 경로를 파싱하고 각 경로의 Git tree/blob 객체를 대조했다. tree SHA 동일성은 그 하위에 Git으로 추적되는 전체 내용의 동일성을 포함한다. 각 경로의 전체 SHA는 `input16.json`에 있다. 목록은 세 코호트의 `COHORT_SPECS`에서 사용하는 수확·코호트·union·설계 경로를 포함하며, 영수증 도구의 보충 실행 묶음·설계도 포함한다. [요청서 248행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf8cf21c6466cdb9411f9320711b871c2d1c651e/docs/reviews/codex_lhs214_relaunch_check_request_20261028.md#L248), [실행기 160–171행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf8cf21c6466cdb9411f9320711b871c2d1c651e/scripts/run_network_194_parallel.py#L160), [영수증 도구 65–69행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf8cf21c6466cdb9411f9320711b871c2d1c651e/scripts/supp20_input_receipt.py#L65)

이것은 실행기가 읽을 수 있는 모든 경로나 WSL 원 dump의 현재 바이트를 독립 재측정했다는 뜻이 아니다. `plan_input_digest`는 수확 JSON에 기록된 raw의 atom/contact/mesh/deck SHA를 묶는다. 실제 raw 파일 대조는 생산 워커 쪽 계약이다. 이번 검토에는 그 외부 raw 파일을 읽는 동작이 없다. 요청 대조표도 입력16을 전 경로 증명으로 보지 않는다고 한정한다. [실행기 1245–1259행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf8cf21c6466cdb9411f9320711b871c2d1c651e/scripts/run_network_194_parallel.py#L1245), [대조표 61행 주장](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/bf8cf21c6466cdb9411f9320711b871c2d1c651e/docs/reviews/codex_lhs214_relaunch_check_request_20261028_claimcheck.md#L41)

## 다른 트랙 변경과 수의 범위

scripts/와 webapp/ 바로 아래의 `.py` 변경은 정확히 11개이며 모두 closure78 밖이다:

```text
scripts/kg50_q5_branches.py
scripts/kg50_q5_verdict.py
scripts/rint_first_result.py
scripts/rint_r_chain.py
scripts/test_ca_ext_runner.py
scripts/test_ca_s0_census.py
scripts/test_resume_ckpt.py
scripts/test_rint_first_result.py
scripts/test_rint_r_chain.py
scripts/test_rint_r_chain_e2e.py
webapp/test_rint_explainer_page.py
```

11은 이 소스 디렉터리 범위의 수다. docs 아래에 새로 반입된 재현 스크립트 등까지 포함한 저장소 전체 `.py` 변경 수로 인용하면 안 된다. 추가 게이트는 믹서2 + ULPRI5 + rint1 + kg50 2 = 10줄이며, LHS 등재7행과 fast 드라이버 내용은 그대로다. 새 게이트를 실행하거나 그 다른 트랙 기능의 옳음을 판정하지 않았다.

## 재현과 파일

전달 폴더에서 다음을 실행한다. 표준 Python만 필요하며 네트워크와 Git이 필요 없다. 제품 소스를 실행하지 않는다.

```text
python -I -X utf8 -B independent/identity/audit_identity.py
python -I -X utf8 -B independent/identity/portable_check.py
```

첫 명령은 `repo/`와 이 폴더의 metadata/, sources/, gate_inputs/를 읽고 결과 JSON을 갱신한다. 두 번째는 이 입력만 임시 위치로 복사하여 같은 검사를 수행한 뒤 임시 복사본을 정리한다. 원 증거를 보존하려면 전달 폴더의 사본에서 재실행한다.

- `summary.json`: 짧은 최종 수치.
- `identity_results.json`: 70개 전달 파일·CORE40·closure78·80개 소스 해시·입력16·간선·범위 밖 변경 전체.
- `gate_results.json`: 게이트 추가25줄, 등재 추가2행, LHS7행과 드라이버 원문.
- `metadata/`: 고정 핀 원격 commit/tree/compare 응답. 원격 compare의 파일목록은 전수 아님.
- `sources/`: 80개 검증된 소스·등록 바이트와 추가 취득본의 base64 응답.
- `gate_inputs/`: 두 핀의 게이트와 등재 원문·base64 응답. 재현에 포함해야 한다.
- `portable_result.json`: 외부 이전 검토 캐시 없는 이동 재현 rc 0, stderr 빈값.

이 검토는 역사상 마지막 등록 커밋 → B7의 37개 소스 변경 수, 저자 승인 대화의 진위, WSL에서 생산 파일을 다시 읽은 결과, 214 실행 결과를 별도로 판정하지 않는다.
