# LHS214 발사 확인 검토 — 증거 재현

리뷰 핀 `bf8cf21c6466cdb9411f9320711b871c2d1c651e`, 실행 승인 핀 B7 `35f0327377a4213774010a090df4d224e50d29e1`.

이 묶음의 명령은 보존 자료·고정 코드의 검증만 수행한다. 생산·WSL·시뮬레이션·발사 명령은 포함하지 않는다. 저장소를 checkout하거나 Git 상태를 바꾸지 않는다.

## 구성

- `codex_review_lhs214_relaunch_20261030.md`: 통합 한국어 판정문.
- `VERDICT.json`: GO의 범위와 제외 항목을 기계가 읽을 수 있게 기록.
- `repo/`: 수령 ZIP의 70개 원본 리포 파일. 제품 수정 없음.
- `input/`: 원 ZIP·원 WSL TGZ·핀·수령 무결성 기록.
- `independent/identity/`: pinned Git API tree·commit 메타데이터, 80개 소스/등록 바이트, 게이트 자료, 독립 대조 코드와 결과.
- `independent/evidence/`: 원문·영수증·입력 지문·S0b 독립 검증 코드와 결과.
- `independent/launch/`: 실제 함수에 넣은 SHA 경계 10형·형식 상태 3형.
- `support/s1/`: Git blob을 대조한 기존 입력 232개와 연결된 하위 tree, 이전 receipt 소스. WSL 원 dump 214개를 담은 폴더는 아님.
- `MANIFEST.sha256`: 파일별 SHA-256. 목록 자체와 묶음 밖의 `PACKAGE_CHECK.json`은 제외.

원 ZIP을 보존하고 **새 폴더에 푼 사본**에서 아래 명령을 실행한다. 작업 위치는 이 README가 있는 폴더다. 검토 스크립트가 결과 JSON을 쓰므로 재현 뒤의 파일 지문은 최초 배포 MANIFEST와 달라질 수 있다. Python 3.12와 저장소의 일반 import 의존성(NumPy·SciPy·NetworkX 등)이 있는 환경을 사용한다. 이번 검토 환경은 Windows Python 3.12.14다.

## 1. 고정 tree·소스 동일성

```text
python -I -X utf8 -B independent/identity/audit_identity.py
```

기대: tree 15개 해시 연결, ZIP 리포 70/70 blob 일치, CORE40/closure78/input16 동일, missing0, code_fp `2149f873…c3eb`. 게이트 +25/0, 등재 +2/0, LHS7행 동일.

이 스크립트는 네트워크와 Git 명령을 호출하지 않는다. 같은 폴더의 보존 메타데이터를 읽는다. `sources/`가 완비되어 외부 `lhs28` 캐시는 필요하지 않다. 이동 사본 검사 결과는 `portable_result.json`에 있다. AST78을 가능한 모든 런타임 의존성의 실행 증명으로 해석하지 않는다.

## 2. 보존 WSL 자료·실제 검사기·S0b

```text
python -I -X utf8 -B independent/evidence/verify_evidence.py --repo repo --s1 support/s1 --identity-metadata independent/identity/metadata --tgz input/lhs_preflight_35f032737_1028_173239.tgz --out rerun_evidence
```

기대: 원문 18/18, 입력 232개 blob 일치, 두 preflight 각각11/11, 보충24/24 rc0, S0b 실제 파서7/7·helper12/12·가드 제거4/4 탐지.

이 명령은 `rerun_evidence/verification_tree/`에 별도 소스·입력 사본을 만들고 그 사본의 **읽기 전용 검사 함수**만 호출한다. 원 receipt의 log.path·승인 SHA·기대값은 수정하지 않는다. 전체 자체시험·run·solver를 호출하지 않는다. 이 결과를 새 WSL 실행 기록이나 실제 발사 영수증으로 사용하지 않는다.

## 3. 승인 SHA 경계

```text
python -I -X utf8 -B independent/launch/check_launch_validators.py --repo repo --out rerun_launch
```

기대: 정확한40자리 승인 일치만 F7 통과, SHA+LF 및 마지막 자리 오값은 full40 승인에서 F7 거부. 짧은7자리는 마지막 자리 오값을 허용하고, 승인 생략은 F7을 만들지 않는다는 기존 경계도 재현한다. `current`가 생산 완료를 뜻하지 않는 상태3형도 별도다.

이 좁은 합성 fixture에는 수확 자료가 없으므로 F2 실패가 예상된다. F1/F7만 겨냥한 경계 결과를 전체 launch receipt PASS로 보고하지 않는다. F7/G7은 같은 함수이고, 실제 전체 사전 점검24/24는 위 2번에서 별도로 확인한다.

## 증거 출처와 한정

수령 원 ZIP SHA-256:
`f784b6b7352ba1336afc3dfabf069100e08641f008e40ce255a1fd007e36aadf`

원 WSL TGZ SHA-256:
`9c05aef7591ad10af70af52c01508b494ddc71855322b0ce367f42f67a5be0b8`

다섯 selftest 종료코드 전사는 TGZ 밖에서 보완된 자료다. 실물 raw dump 전체를 재해시한 것, 새 Bash/WSL 실행, 현재 현장의 핀/환경/ROOT 상태 확인, 저자 발사 승인, 실제 214 완료, v1.3·S3 GO는 이 증거 묶음이 생성하지 않는다.
