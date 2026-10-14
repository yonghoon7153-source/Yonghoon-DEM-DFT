# 보충 20 수정 재검증 판정

작성 2026-10-14. 검토 핀 `a9422d2e772f28417a6e0a5167aaab8d987bf27a`, 기준 `b429c3c1df0956d2721861d89cc29a2d56f2b581`. 대상은 SUP20-01·02 수정과 새 입력 영수증이다. 이후 ps45 보고용 변경은 제외했다.

**결론: SUP20-01·SUP20-02는 닫힘. 새 P1은 발견하지 못했다. 새 영수증의 dry-run 증거 연결에 P2 두 건이 있어, 이것을 발사 전 증서로 사용하는 것은 HOLD다. 수정된 두 기존 결함을 다시 여는 판정은 아니다.**

수정 검증과 WSL 사전 점검 진입은 허용한다. 실제 194·보충 20 발사와 v1.3 배포의 무조건 GO는 아니다. 생산 실행·수치 재계산·원본 코드·원장 변경은 하지 않았다.

## 1. Q1 기존 두 지적의 해제

| 대상 | 판정 | 직접 검산 |
|---|---|---|
| SUP20-01 권위 ROOT 하나 | 닫힘 | 배치별 관문 ROOT만 교차 함수에 전달. 사본 ROOT는 비교 대상이며 입력이 아님 |
| 필수 ROOT 결손 거부 | 닫힘 | 결손·비문자열·없는 경로가 오류로 남음. 교차 함수 생략이 전체 PASS로 바뀌지 않음 |
| 보충 code_identity 대칭 검사 | 닫힘 | 194·보충 모두 공용 도우미 적용. 삭제·승인 없는 변경 거부 |
| build/check 반례와 정상 대조 | 닫힘 | V22 22/22 PASS. 옛 release_probe 무변경 재실행으로 기존 오수용 반례 거부. 정상 214 build/check 문제 0 |
| SUP20-02 mono 슬롯 사전 | 닫힘 | lhss 20행 + lhsx 64행 정의 대조 불일치 0. 네 문자열·자체시험 외 생성기 AST 동일 |

### SUP20-01

근거는 `scripts/lhs_release_build.py:2453,2488–2552`와 `scripts/test_lhs_release_v13.py:2133–2261`이다. [고정 소스](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/a9422d2e772f28417a6e0a5167aaab8d987bf27a/scripts/lhs_release_build.py#L2488)

옛 탐침을 바꾸지 않고 현재 소스에서 실행한 결과:

| 탐침 | 기준 핀 문제 수 | 수정 핀 문제 수 |
|---|---:|---:|
| 정상 build 후 check | 0 | 0 |
| 사본 교차 ROOT가 없는 경로 | 0 | 1 |
| 보충 code_identity 삭제 | 0 | 1 |
| 보충 승인 없는 봉인 변경 | 0 | 1 |
| 다른 지문인 정상 보충 관문으로 교체, 사본은 원래 | 0 | 4 |
| 위 교체 + 사본 없는 경로 | 0 | 4 |
| 위 교체 + 사본도 교체 ROOT | 2 | 3 |

교체용 ROOT 자신의 배치 관문은 문제 0이다. 결손 fixture를 만들어 실패시킨 것이 아니다. 다른 지문의 ROOT를 정상 build에 넣으면 종전처럼 거부하며, 정상 build의 기존 194 projection 8파일은 보충을 추가하기 전과 바이트가 같다. τ 재독해만 제출 시험과 같은 합성 대역을 사용했고 build/check·개별 관문·교차 함수는 실제 함수를 실행했다. 실제 g2 수치 검증으로 확대하지 않는다.

별도 `release_extra.py`는 실제 prepare/seal/관문 함수를 사용한 추가 27개 대조가 모두 기대와 일치했다. 이 관문 단독 탐침에는 τ 대역도 필요 없다.

### SUP20-02

`scripts/lhs_design_dataset.py:2263–2265,2278–2281`의 P/S 슬롯 정의는 `scripts/lhsx_design_adapter.py:73–86`의 실제 변환과 맞는다. [수정 사전](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/a9422d2e772f28417a6e0a5167aaab8d987bf27a/scripts/lhs_design_dataset.py#L2263)

lhss_001·002·003·020은 각각 P=0.300·0.300·0.300·0.375, S=0이다. 무조건 비율 식은 전부 1이지만 실제 `ps_frac`는 전부 0이며, 수정 사전은 이들을 mono_AM_S로 정확히 설명한다. lhsx mono_AM_S 8행도 같은 검산을 통과했다.

설계 CSV·변환 CSV·어댑터 계산은 불변이다. `df505b79a756ee3fe2759c740bfb43282dd69035c5a9fb9354a657300117dc0c`의 변환 CSV를 그대로 유지해도 된다. SELF-107은 이번 스냅샷의 v1.2 사전 한 사례에서도 뒷받침됐지만, 역사 사전 4개 전수를 재검증했다고 주장하지 않는다.

## 2. Q2 목록 강제와 ROOT 사본 대조

**둘 다 동의한다. 검산한 정상 경로에서 과잉차단은 발견하지 못했다.**

- 실제 `v13_seal_gate`는 승인 경로를 정규화한 목록을 만든다. 정확한 경로, `./`가 붙은 경로, 역슬래시 경로는 공용 재검사를 통과했다. 변경이 없을 때 `allowed` 누락/null도 종전처럼 수용했다.
- 문자열·더 긴 문자열·다른 파일명에 대한 부분문자열 승인은 194와 보충에서 모두 거부했다. JSON 생산물의 목록을 강제하는 것이므로 tuple/set을 거부하는 일을 정상 경로 손상으로 보지 않는다.
- 같은 위치의 `.`·끝 구분자·슬래시 철자 차이는 통과했다. 같은 code_fp라도 다른 정상 디렉터리로 사본만 바꾸면 거부했다.

범위는 **동일한 기록 계약과 사본 일관성**이다. 모든 증거를 다른 정상 ROOT의 일관된 증거로 함께 바꾸거나 승인 목록 자체를 위조하는 것을 외부 진위 인증 없이 식별한다는 뜻은 아니다. 기존 공개 한계를 새 결함으로 중복 등재하지 않는다.

## 3. Q3 컨테이너 영수증은 어디까지 충분한가

**반입 입력과 등록 지문의 대조에는 충분하다. WSL 발사 핀의 사전 점검을 대신하기에는 불충분하다.**

고정 스냅샷에서 기본 영수증을 실행해 rc=0, 11칸 전부 일치를 재현했다. 별도 계산으로도 다음을 확인했다.

| 항목 | 독립 대조 결과 |
|---|---|
| 수치 봉인 | 32/32 파일이 기준과 바이트 동일, `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` |
| ID 20개 | `991cf1150b183f64bc69926a8b3e7c05453ec47e13b89ba3a6ad2fd2c981c694` |
| raw SHA 표 | `a7aaa3c8c7683f1835a096acb83ecdb055eaf5f129221f7067c5f34462807d0e` |
| cohort TSV | `69d3f913072288b1d6b8ca8a14e43b0bc8f80e8836a8f79a9b26b2d8ed6dcaf7` |
| r3 반입 | descriptor 20/20·요약·cohort·union이 묶음과 바이트 동일 |
| r2/r3 대조 | 공통 키 차이는 pin_file 경로뿐. r2 전용 wall_near_tangent 잎 키는 mono 각 28개, bimodal 각 42개. r3 전용 키 0. union·cohort 바이트 동일 |

이것은 수확 JSON에 들어 있는 원자료 SHA **표**를 재계산한 것이며, WSL 원 atom/contact/mesh/deck 80파일을 다시 읽어 해시한 것은 아니다. `harvest_head`도 묶음에 적힌 판의 대조이지 당시 실행을 독립 관측한 증거는 아니다.

기존 두 수정의 닫힘을 위해 WSL 증거를 먼저 요구할 필요는 없다. 그러나 **실제 발사 허용 전**에는 발사 핀의 WSL 점검과 입력 대조가 필요하다. 저자 승인을 그보다 먼저 기록하려면 다음처럼 조건부로 한정해야 한다.

> 수정본의 사전 점검 착수를 승인한다. 실제 생산 발사는 최종 핀의 fast16+real4, 깨끗한 트리, 두 새 ROOT, import 관측 ON, 전체 입력 지문 일치와 정상 dry-run 완료가 모두 확인된 뒤에만 허용한다.

현재 `--dry-run-log`의 rc=0만을 이 마지막 증거로 쓰면 안 된다. 다음 두 반례 때문이다.

## 4. 새 P2 SUP20R-01 실행 로그의 TSV 지문이 연결되지 않음

**심각도 P2. 무너지는 결론은 “WSL dry-run의 전체 입력 지문이 등록·반입본과 같다”이다.** 기본 컨테이너 입력 검증과 기존 ROOT 수정, 수치 봉인 불변은 무너지지 않는다.

위치:

- `scripts/run_network_194_parallel.py:1815–1817`: 출력하는 입력 지문에 `cohort_tsv_sha256`이 없음.
- `scripts/supp20_input_receipt.py:197–201`: E1은 n·ID·raw 표·결손 수만 비교.
- 같은 파일 `:214–216`: 코호트 줄도 이름·개수만 비교하며 파일 해시는 비교하지 않음.

[실행기 출력](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/a9422d2e772f28417a6e0a5167aaab8d987bf27a/scripts/run_network_194_parallel.py#L1815) · [영수증 E1](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/a9422d2e772f28417a6e0a5167aaab8d987bf27a/scripts/supp20_input_receipt.py#L197)

### 검산

실제 TSV의 첫 행 `deck_sha256` 한 글자를 바꾼 별도 파일로 실제 `plan_for`/`build_plan`과 `plan_input_digest`를 호출했다. ID·raw 표는 그대로이고 cohort 해시만 다음처럼 바뀌었다.

- 정본: `69d3f913072288b1d6b8ca8a14e43b0bc8f80e8836a8f79a9b26b2d8ed6dcaf7`
- 변이: `8d5dcbd28061327f7c4f8c1a0b8915647c368236a78ced0c5ed7c3693100f1d4`

실제 `print_preflight`가 만든 로그를 로컬 정본 입력을 읽는 영수증에 전달하면 **전체 로그도 rc=0, 등록 §4의 grep 로그도 rc=0**이다. 정상/변이의 grep 로그는 바이트 단위로 같다. 전체 로그에 다른 파일 경로가 있어도 비교되지 않는다.

대조군으로 변이 TSV를 영수증 자체의 `cohort` 인자로 주면 rc=1, B3·C2가 실패한다. 로컬 TSV 검사는 작동하지만, 외부 실행 로그와 로컬 입력 사이 연결이 빠졌다는 반례다.

### 최소 해결과 해제 증거

1. 발사 사전 점검이 실제 사용한 `INPUT_DIGEST_KEYS` 전부, 특히 코호트별 TSV SHA를 기계가 읽는 출력에 포함한다.
2. 영수증이 그 값과 등록값·현재 반입 재계산값을 모두 비교한다. 부재는 거부한다.
3. 같은 20 ID/raw 표에서 TSV만 바꾼 로그를 반드시 거부하는 상주 시험과 정상 로그 통과를 둔다. 단순 파일 경로 문자열 비교로 대체하지 않는다.

발사 뒤 F3는 전체 `INPUT_DIGEST_KEYS`를 비교하므로 이 특정 차이를 잡을 수 있다. **발사 뒤 검사가 발사 전 입력 동등성 증거의 누락을 소급해 채우지는 않는다.**

## 5. 새 P2 SUP20R-02 잘린 로그가 정상 사전 점검 증거로 통과

**심각도 P2. 무너지는 결론은 “중단 없이 완결된 dry-run을 이 영수증이 확인했다”이다.** 생산 러너가 관측 OFF를 실제로 통과시킨다는 뜻은 아니다.

위치:

- `scripts/supp20_input_receipt.py:210–213`: ⛔/✗가 없는지만 검사. 필수 검사 줄의 존재·성공과 실행 완료를 요구하지 않음.
- `scripts/run_network_194_parallel.py:1818–1823`: 중단 사유는 앞선 정상처럼 보이는 지문 줄 뒤에 출력.
- 같은 파일 `:2381–2387`: 실제 CLI는 stop이 있으면 rc=2, 정상 dry-run이면 완료 줄을 출력하고 rc=0. 영수증은 이 완료/종료 상태를 확인하지 않음.

[영수증 E5](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/a9422d2e772f28417a6e0a5167aaab8d987bf27a/scripts/supp20_input_receipt.py#L210)

### 검산

실제 `production_observation_problem({'plan': plan, 'observe_imports': False})`의 거부 사유를 사전 점검 fixture에 넣고 실제 `print_preflight`로 출력했다.

| 입력 로그 | 영수증 결과 |
|---|---|
| 정상 전체 로그 | rc=0 |
| 관측 OFF 사유까지 보존한 전체 로그 | rc=1, E5 실패 |
| 같은 거부 로그를 마지막 안내·⛔ 전에 자른 prefix | **rc=0, E1–E6 통과** |
| 정상 로그에서 전이 의존·지연 import·fork 줄 셋 삭제 | **rc=0** |

사전 점검의 시스템·원자료 상태는 합성 fixture이며 실제 WSL preflight를 실행한 결과가 아니다. 여기서는 로그 생산·파싱 함수와 실제 관측 OFF 정책을 시험했다. 실제 러너의 OFF 차단은 소스와 전체 로그에서 유지된다.

### 최소 해결과 해제 증거

1. 필수 검사 세 항목과 `observe_imports=true`의 **명시적인 성공 값**을 요구한다. 줄이 없으면 실패 또는 미완료로 처리한다.
2. 하나의 사전 점검 실행에 결합된 완료 상태와 정상 종료를 요구한다. 중간 출력만으로 완결된 증서를 발행하지 않는다. 가능하면 사람이 읽는 grep 텍스트 대신 완료 시점에 기록하는 구조화 영수증을 사용한다.
3. 원본 전체 로그·실행 인자·출력 해시·실행 종료코드를 보존한다. 셸의 tee/grep 종료코드를 러너 종료코드로 오인하지 않는다.
4. 위 OFF 전체/잘린 prefix/필수 줄 결손 반례와 정상 대조를 상주화한다.

로그를 무제한 편집하는 공격을 암호학적으로 막으라는 요구가 아니다. 부분 캡처·중단·누락을 성공 증거로 오독하지 말라는 요구다. 현 등록 grep은 완료 줄과 일부 문맥을 버리므로, 완료 증거를 도입할 때 등록 명령도 함께 정정해야 한다.

## 6. Q4 남은 발사와 배포 조건

새 P1 없음. 새 P2 두 건은 위 영수증 경로로 한정한다. 최소 순서는 다음과 같다.

1. SUP20-01·02는 verified로 닫을 수 있다. 이 결함 때문에 수치 재계산을 요구하지 않는다.
2. SUP20R-01·02 수정 또는 같은 요구를 충족하는 별도 입력·완료 대조 절차를 확정한다. 현 dry-run 영수증 rc=0 단독은 수용하지 않는다.
3. 최종 발사 핀을 명시하고 그 핀에서 fast16+real4 및 WSL 원자료 점검을 완료한다. 수치 32 봉인뿐 아니라 실행기·인계·배포 도구 지문도 기록한다. 검토 핀 이후 관련 변경은 별도로 대조한다.
4. 같은 최종 핀·깨끗한 트리, 각각 새 ROOT, 등록집합 `production194`/`supp20`, g2, 관측 ON, 전체 입력 지문, 정상 dry-run 완료를 묶어 확인한다. `--expect-case` 일반 계획으로의 강등은 허용하지 않는다.
5. 위 조건이 충족됐다는 증거를 확인한 뒤 저자의 실제 발사 승인으로 194 → 보충 20을 진행한다. 미리 받은 승인은 3–4의 조건부 승인으로만 쓴다.
6. 발사 뒤 manifest 대조, 배치별 audit·정확한 expect-set 다시 읽기·τ/인계 관문을 각각 통과시킨다. 합성 시험이 이 단계를 면제하지 않는다.
7. v1.3 결합 관문으로 고유 214·교집합 없음·배치별 출처·같은 수치 봉인과 세대·기존 194 projection 보존을 확인한 뒤 build/check한다.

추가 범위 주의: E2는 로그의 git short를 파싱하지만 승인된 최종 SHA와 대조하지 않는다. H1도 두 manifest SHA의 상호 일치이지 승인 핀과의 일치가 아니다. `scope=launch`는 실제 생산 감사를 뜻하지 않는다. 또한 194의 HANDOVER 파일 해시를 현재 파일과 비교하는 G6는 없고 F6는 보충에만 있다. 이번에는 이를 기존 수동 핀 확인·배치 감사의 면제로 쓰지 않는 조건을 명시하며, 별도의 수치 오류나 새 P1로 확대하지 않는다.

## 7. 실행 증거와 한정

| 실행 | 로컬 결과 |
|---|---|
| release 전체 | 254 PASS / 2 FAIL — V10a POSIX 경로 문자열, V16a Git checkout HEAD. 직전과 같은 Windows/부분 스냅샷 가정 실패 |
| V22 부분 | 22/22 PASS |
| builder 자체시험 | 31/31 PASS |
| dataset 자체시험 | 391/391 PASS |
| receipt 자체시험 | 40/40 PASS |
| 기본 receipt | rc=0, 11/11칸 일치 |
| 옛 design_probe / release_probe 무변경 | 둘 다 rc=0. 수정된 반례 거부 및 정상 대조 확인 |
| release_extra | 27개 기대 결과 일치 |
| design_extra | 정의·AST·해시·묶음 대조 일치 |
| receipt_extra | 위 P2 두 건 및 양성 대조 재현 |

Linux `check_all.sh`, WSL fast16+real4, 실제 194/20 계산은 실행하지 않았다. 따라서 제출자의 Linux 256/256·전체 게이트 결과를 독립 재현했다고 쓰지 않는다. 로컬 소스 1,053파일을 Git blob/SHA로 확인했으며 시험 후 원본 바이트 변경 0이다.

옛 두 탐침은 요청대로 바이트 그대로 실행해서 결과 JSON의 고정 `pin` 문자열이 기준 핀으로 남아 있다. 실제 실행 대상은 이 폴더의 `source/`이며, 현 핀 증거는 `source_manifest.json`과 `evidence/final_qa.json`이다. 옛 문자열을 새 핀으로 고쳐 증거를 재작성하지 않았다.

독립 반례 재현은 증거 폴더에서 다음과 같다. 시험용 출력만 쓰며 생산 실행은 없다.

```bash
python -X utf8 -B run_checks.py design_probe release_probe receipt_extra
python -X utf8 -B probes/release_extra.py
python -X utf8 -B probes/design_extra.py
python -X utf8 -B run_receipt.py
python -X utf8 -B verify_evidence.py
```

직접 오수용을 보려면 `source/`에서 실행한다.

```bash
python scripts/supp20_input_receipt.py --dry-run-log ../evidence/receipt_extra/wrong_tsv_full_log.log
python scripts/supp20_input_receipt.py --dry-run-log ../evidence/receipt_extra/observation_off_truncated_before_stop.log
```

둘 다 현 핀에서 rc=0이다. 대조군 `observation_off_full_log.log`는 rc=1이다. 수정 후에는 잘못된 두 입력도 거부해야 한다.

**최종: SUP20-01·02 닫힘 / 사전 점검 진입 허용 / 현 dry-run 영수증으로 실제 발사 승인 및 v1.3 배포 확정은 HOLD.**
