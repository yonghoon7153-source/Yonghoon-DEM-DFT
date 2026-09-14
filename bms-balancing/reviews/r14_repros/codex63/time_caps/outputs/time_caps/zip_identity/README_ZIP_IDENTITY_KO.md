# PREFLIGHT ZIP 정체성과 이전 333개 파일 재검증

검사 시각: 2026-09-13 22:36–22:37 KST. ZIP 및 관련 파일을 읽고 크기·SHA-256·CRC·manifest를 대조했다. COMSOL 실행, 압축 해제, 기존 파일 변경은 하지 않았다.

**현지 PREFLIGHT ZIP과 바탕화면의 관련 압축 해제본은 manifest 및 331개 payload 내용이 일치한다. 사용자가 보고한 다른 크기·SHA의 ZIP 원본은 발견하지 못했으므로, 두 raw ZIP의 압축·메타데이터 차이와 전달 경로는 아직 확인되지 않았다.**

## 확인한 바이트와 미확인 주장

| 대상 | 직접 확인 | 결과 / 한계 |
|---|---|---|
| 현지 `outputs/COMSOL63_PREFLIGHT_HANDOFF.zip` | 전체 raw SHA, 크기, 332개 ZIP 항목의 CRC 읽기·크기·SHA | **46,999,470 bytes**, SHA-256 `3bc4e4e4d14ff815a710998ac3e538712343933cef6d460eb5845f21e7235018` |
| ZIP 내부 `PREFLIGHT_MANIFEST.json` | 실제 member 원문 | 68,579 bytes, SHA `f8de24351dd424c5e34136cdbd690e73902a05d4deb7e1db6b9513c722f9ac27`; 331개 payload를 기록 |
| `C:/Users/BML/Desktop/COMSOL63_PREFLIGHT_HANDOFF` | manifest 및 그 안에 기록된 실제 파일 331개 | 내부 manifest 원문과 SHA·크기가 동일하며 payload **331/331** 일치, 누락·불일치 0 |
| 사용자 보고 ZIP | 크기 47,006,147 bytes, SHA 약칭 `097d4b65...c3b51`을 전달받음 | 해당 raw ZIP을 찾지 못함. 전체 SHA도 이 감사에는 아직 제공되지 않음 |
| 두 raw ZIP의 관계 | 두 번째 raw 파일 부재 | **미확인**. “재압축만 달라졌다”, “메타데이터만 다르다”, “둘의 모든 내용이 같다”는 결론을 내리지 않음 |

바탕화면 압축 해제본이 어떤 raw ZIP에서 만들어졌는지는 이 파일 검사만으로 증명할 수 없다. 따라서 압축 해제본의 일치 결과를 `097d4b65...c3b51` raw ZIP 전체의 검증 결과로 대체하지 않는다. 보고된 크기끼리의 차이는 6,677 bytes이나 원인은 미확인이다.

검색 범위는 workspace의 관련 ZIP, Documents(외부 조사에서는 workspace·work·임시 폴더 제외), Downloads, Desktop의 ZIP 이름·경로·크기였다. 외부 범위에서 4개 ZIP이 발견되었으나 정확히 47,006,147 bytes인 후보는 없었다. 관련된 WINDOWS 원본 ZIP과 압축 해제 폴더 안의 VALIDATED_SHORT ZIP은 다른 파일이다. 최초 workspace 탐색에서 접근이 제한된 패키지·임시 하위 폴더는 제외했으며, PC 전체나 다른 장치에 두 번째 ZIP이 없다고 주장하지 않는다. 개인 문서 내용은 검색하지 않았다.

## 330 · 331 · 332 · 333의 의미

- **331**: PREFLIGHT 내부 manifest의 payload 파일 수. `outputs/NEXT_RUN_PLAN.md`의 당시 사본을 포함한다.
- **332**: 실제 ZIP member 수. 331개 payload + ZIP 루트의 `PREFLIGHT_MANIFEST.json` 1개이며 directory member는 없다.
- **330**: 위 payload에서 이후 갱신이 허용된 `outputs/NEXT_RUN_PLAN.md`를 제외한 이전 보존 대상.
- **333**: 위 330개 + 현지 PREFLIGHT ZIP 자체 + 외부 manifest + 원래 SHA 영수증의 3개.

외부 `outputs/COMSOL63_PREFLIGHT_MANIFEST.json`은 70,239 bytes, SHA `f5bd6cca465337692c81953412d446846349d5a98356796aeb8e70fdee0f4c25`이다. 내부 manifest와 **파싱한 JSON 내용은 같지만 원문 바이트·SHA는 다르다**. 둘을 원문 동일 파일이라고 기술하면 안 된다.

## 전달물의 독립 재검증 범위

| 범위 | 필요한 실제 바이트 | 독립 검사 결과 / 제공 범위 |
|---|---|---|
| 이전 MESH_AXES ZIP 단독 | 그 ZIP 내부 파일 | 이전 333개 중 동일 경로 실제 payload **7개**만 포함·일치. 보존 ledger는 있지만 이전 PREFLIGHT ZIP은 없음. 나머지 326개는 그 ZIP만으로 재검증할 수 없음 |
| 새 전달에 추가할 네 입력 | 아래 표의 3개 원본 파일 + 이전 333 ledger | **330 ZIP member + 3 loose 파일 = 333개**를 재검증 가능. 330개의 기존 압축 해제 원본은 필요 없음 |
| 현재 PC의 새 실행 전 보존 상태 | `outputs/time_caps/preserved_before.json`과 현지 실제 468개 파일 | **468/468** 크기·SHA 일치. 이는 현지 검사이며, 468개 모두가 새 전달물에 포함된다는 뜻은 아님 |

새 전달의 재검증 구성은 네 입력만 복사한 별도 최소 fixture에서 실제 실행하여 **333/333, 191,105,291 bytes** 일치를 확인했다. 이 fixture에는 기존 330개 loose payload가 없었다. 최종 새 ZIP을 봉인한 뒤에도 수신자가 해당 네 입력을 실제로 받았는지 외부 패키지 manifest와 함께 다시 검증해야 한다.

### 수신자에게 필요한 입력 네 개

경로는 새 전달 ZIP을 해제한 루트 기준이다.

| 파일 | 역할 |
|---|---|
| `outputs/COMSOL63_PREFLIGHT_HANDOFF.zip` | 330개 보존 payload의 실제 byte stream과 ZIP 자체의 raw 정체성 |
| `outputs/COMSOL63_PREFLIGHT_MANIFEST.json` | 보존 대상인 원래 외부 manifest 원문 |
| `outputs/COMSOL63_PREFLIGHT_HANDOFF_SHA256.json` | 보존 대상인 원래 ZIP 영수증 원문 |
| `outputs/mesh_axes/preserved_before.json` | 원래 333개 경로·크기·SHA 기대값. 자체 SHA 고정 앵커 `2326bcbae80657bfb6dccce56f1272366af8fe8f9bbbc71dd57daa4c905748bb` |

`previous_333_locator.json`은 333개 각각의 이전 경로와 실제 검증 위치를 기록한다. 330개는 `archive + member`로, 3개는 원래 loose 경로로 연결된다. ZIP 안에 들어 있는 VALIDATED_SHORT ZIP도 보존 대상 byte stream으로 검증한다. COMSOL 모델을 열거나 다시 풀 필요는 없다.

### 재현 명령

Python 표준 라이브러리만 필요하다. 새 전달의 루트에서 실행한다.

```text
python work/time_caps/zip_identity_verify.py --root .
```

정상 종료 코드 0, `portable_333_verification.all_333_verified=true`, `verified_count=333`을 확인한다. ZIP·ledger의 고정 SHA, 내부 331개 manifest 대응, 전 member CRC 읽기, 크기·SHA, 외부 manifest의 JSON 대응, 원래 영수증의 raw ZIP 크기·SHA를 확인한다. 결과는 `outputs/time_caps/zip_identity/`에 쓴다. 입력이나 기존 모델·보고서는 변경하지 않는다.

`--check-local-current`는 실제 468개 현지 파일을 별도로 검사하는 선택 옵션이다. 최소 수신자 재현 명령에는 넣지 않는다. `--extracted`도 관련 압축 해제본이 있는 PC의 보조 검사용이며 필수가 아니다.

두 번째 raw ZIP을 실제 확보하면 `--second-zip`으로 해당 파일을 지정할 수 있다. 경로·payload 크기·SHA·순서·timestamp·attributes·extra fields·압축 방식·압축 크기·압축 stream SHA·archive comment를 비교한다. 실제 계산한 SHA를 사용자의 전체 SHA와 추가 대조해야 보고된 포장본의 정체성을 확정할 수 있다. 현재 결과의 상태는 `NOT_VERIFIABLE_WITHOUT_SECOND_RAW_ARCHIVE`다.

## 이번 검사 증거

- `zip_identity_verification.json`: 현지 raw ZIP, Desktop 추출본, 이전 전달의 7/333 범위, 현재 현지 468개 보존 검사.
- `previous_333_locator.json`: 333개 전체의 기대값·실제 값·수신자 검증 위치.
- `local_archive_entry_metadata.json`: 현지 ZIP 332개 member의 전체 내용·압축·메타데이터 인덱스. 전부 compression method 8(Deflate), archive comment 없음.
- `portable_fixture_verification.json`: 네 입력만 존재하는 최소 fixture의 실제 성공 결과.
- `work/time_caps/zip_identity_verify.py`: 재현 코드. 독립 정적 검토 완료.

무결성 검사는 제공된 바이트의 동일성을 확인한다. 문서의 과학적 정확도, 독립 COMSOL 재실행, 전달 출처의 진위 또는 전체 운전 프로토콜 승인을 뜻하지 않는다.
