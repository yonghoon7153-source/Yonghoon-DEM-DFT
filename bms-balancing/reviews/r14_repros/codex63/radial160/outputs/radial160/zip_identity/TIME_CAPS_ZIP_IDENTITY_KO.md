# TIME_CAPS 생성본과 수신본의 확인 수준

2026-09-14 KST. 이번 감사는 파일·ZIP을 읽어 크기, SHA-256, CRC와 manifest를 대조했다. COMSOL 실행, 모델 열기, 기존 파일 변경 또는 압축 해제는 하지 않았다.

**현지 생성 ZIP의 무결성과 이전 333개 보관 바이트를 직접 재검증했다. 수신자는 다른 raw ZIP 크기·SHA와 검증 통과를 보고했으나, 그 raw ZIP은 이번 현지 검색에서 찾지 못했다. 따라서 두 포장본의 압축·메타데이터 차이나 크기 차이의 원인은 미확인이다.**

## 양쪽의 확인 수준

| 대상 | 크기 / SHA-256 | 확인 주체와 범위 |
|---|---|---|
| 현지 `outputs/COMSOL63_TIME_CAPS_HANDOFF.zip` | **325,347,218 bytes** / `beac1f1df18c2a2613cc5b9da711f1f742aced4f13b79d44d03ca084463f0268` | 이번 감사에서 raw 바이트, 전 ZIP 항목 CRC, 201개 payload의 크기·SHA와 manifest를 직접 확인 |
| 사용자가 보고한 수신 ZIP | **325,367,172 bytes** / `74aa78d2659ed0f4a915a9a4150ccacf4a7f8976a5ad4dd4d38e48c6ace6d0b7` | 사용자는 **201개 payload + manifest 검증 통과**, **333개 보관 바이트 독립 확인**을 명시함. 이 감사가 raw 수신 파일을 직접 확인한 것은 아님 |
| 바탕화면의 관련 추출본 | `C:/Users/BML/Desktop/COMSOL63_TIME_CAPS_HANDOFF` | manifest 원문과 실제 payload **201/201**이 현지 ZIP과 동일. 누락·해시 차이 0. 어떤 raw ZIP에서 추출됐는지는 이 파일 검사만으로 증명하지 못함 |

두 보고 크기의 차이는 **19,954 bytes**이며 보고된 raw SHA도 다르다. 이것만으로 내용 손상, 전송 오류 또는 재압축을 결론 내릴 수 없다. 현지 검증은 통과했고 수신자도 통과를 보고했다. Desktop 추출본의 일치 결과를 수신 raw ZIP의 정체성 검증으로 대체하지 않는다.

검색은 workspace outputs, Documents(별도 검색에서는 workspace/work/temp/.git 제외), Downloads, Desktop의 ZIP 이름·경로·크기에 한정했다. 보고된 크기의 raw TIME_CAPS ZIP 후보는 발견되지 않았다. 다른 경로·장치나 원격 첨부에 파일이 없다는 뜻은 아니다. 개인 문서 내용은 읽지 않았다.

## 현지 ZIP에서 직접 확인한 내용

- 총 **202개 member = 201개 payload + `outputs/time_caps/package_manifest.json`**. directory member는 없으며 모두 compression method 8(Deflate), archive comment는 비어 있다.
- manifest는 **42,396 bytes**, SHA-256 `e7646aedf322195545744ee718275ae2cfaa3e5c0bf92bd15115896f99732a3f`이다. Desktop 추출본의 manifest도 원문 바이트까지 같다.
- 전 member를 끝까지 읽어 CRC를 검사했고, 201개 payload의 이름·크기·SHA가 manifest와 일치했다. 검사 전후 현지 ZIP raw SHA도 동일하다.
- ZIP 안의 **네 입력**(이전 PREFLIGHT ZIP, 원래 외부 manifest, 원래 영수증, 이전 333개 ledger)만 읽어 **330개 내부 ZIP member + 3개 바깥 member = 333개**, **191,105,291 bytes**를 재검증했다. 이전 330개 loose 원본 파일은 사용하지 않았다.
- 위 네 입력은 Desktop에서 비교한 201개 payload에 포함된다. 따라서 Desktop 추출본에도 직접 검증한 현지 ZIP과 같은 역사적 보관 바이트가 있다. 이는 추출본의 원래 raw ZIP SHA를 증명하는 것과는 다르다.

## 333개 보관 범위와 663개 현지 보존 범위

| 검사 | 실제 검증 대상 | 이번 결과 |
|---|---|---|
| TIME_CAPS ZIP 자체에서 재검증 가능한 이전 보관물 | nested PREFLIGHT의 330개 + outer member 3개 | **333/333** |
| radial160 실행 전 현지 보존 목록 | `outputs/radial160/preserved_before.json`이 가리키는 PC의 실제 파일 | **663/663** 크기·SHA 동일 |

663개 현지 보존 통과는 663개 모두가 새 전달 ZIP에 들어 있다는 뜻이 아니다. 수신자가 다시 검증할 수 있는 범위는 새 묶음에 실제 포함한 파일과 locator에 따라 별도로 판정해야 한다. 현재 ledger SHA-256은 `97c10f122e2c5bc073526d37c684af4d3badb14c68952667b6f6ce54946a0dc1`이다.

## 증거와 재현

- `time_caps_zip_identity_verification.json`: 현지 생성본, 사용자 보고 수신본, Desktop 추출본 및 663개 현지 검사 결과를 구분한다.
- `local_time_caps_entry_metadata.json`: 202개 member의 payload SHA·크기, 압축 크기·압축 stream SHA, 순서·timestamp·attributes·extra fields·local header를 기록한다. 다른 raw ZIP을 확보했을 때의 비교 기준이며, 현재는 원인을 판정하지 않는다.
- `historical_333_from_time_caps.json`: outer ZIP에서 직접 읽어 검증한 역사적 333개 경로·크기·SHA와 inner/outer 출처.
- `work/radial160/zip_identity_time_caps.py`: 이번 읽기 전용 감사 스크립트. 기존 `work/time_caps/zip_identity_verify.py`의 고정 SHA를 확인한 후 ZIP 검사 helper를 사용한다.

workspace에서 재현하려면 Python 표준 라이브러리로 다음을 실행한다. 결과 JSON만 새 `outputs/radial160/zip_identity` 폴더에 쓴다.

```text
python work/radial160/zip_identity_time_caps.py
```

실제 raw 수신 ZIP을 확보하면 `--second-zip <파일>`을 추가한다. 스크립트는 실제 raw 크기·SHA가 사용자가 보고한 값과 일치하는지부터 확인하고, 두 ZIP의 payload와 압축·메타데이터를 비교한다. 현재 그러한 직접 비교는 수행되지 않았다.

파일 무결성 및 보관 바이트 동일성은 과학적 정확도, 독립 COMSOL 재실행, 장시간 운전 승인 또는 전체 수렴 판정과 별개다.
