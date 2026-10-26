# 외부 ULPR 정수 파싱 판정·선별 증거 반입 (2026-10-24 KST)

[원문 판정의 LF 사본](codex_review_unloading_ulpr_integer_20261024.md)을 먼저 읽는다. **정수성 교정 수용, Q2·Q3 무결성 종결 HOLD; ULPRI-01·02 P2 열림**이라는 외부 판정을 보존한다. 이후 수정·후속 검토의 상태는 별도 요청서에 기록하며 이 원문을 고치지 않는다.

검토 핀은 `01c1aaf5be8acdf7d1716f34cc86fc77d8e27362`, 비교 기준은 `8347d32ea678c0174bd77d4c79cfbd7b0591e4a3`이다. 원 ZIP `codex_unloading_ulpr_integer_review_20261024.zip`은 8,618,679바이트, SHA-256 `530a3eff236e6ffef3823e76305c0e3b2443d43fa989f8360129c26a4031dc20`이다. 원본은 작업 첨부/외부 산출물로 보존하며, 이 디렉터리는 ZIP 전체 복사본이 아니다.

원 보고서 SHA-256은 `34a6bf923969b719760f429813161bd9bf77c057850f450d4cfcb5cca8fff7f8`이다. 저장한 사본 SHA-256은 `84cd720707e16f0ce244d4bc239a1b8ed26e13f7dd4750c6d940d2042385c2d3`이다. CRLF 184개를 LF로 바꾼 것 외에는 한 바이트도 바꾸지 않았다. LF를 CRLF로 되돌리면 원문 바이트와 정확히 일치한다. 원문 파일·원 ZIP·변환본의 크기와 해시는 [PROVENANCE.json](PROVENANCE.json)에 기록했다.

## 선별 범위

- `evidence/boundary/`: 현재 핀의 정상·literal 소수 음성·ASCII 공백·NBSP·Unicode 중간 삽입·복구 대조 6사례의 원본 입력과 실제 reader/CLI 출력 전체. 1바이트 restart 파일은 합성 fixture이며 실물 체크포인트가 아니다.
- `evidence/boundary_baseline/result.json`: 기준판의 같은 6사례 결과. 기준판 fixture 전체는 원 ZIP에 있다.
- `evidence/independent/`의 결과 JSON, `windows_diagnostic/` 원로그/결과, `mutations_replayed/` 결과/원로그, 신원·범위·기존 게이트 재계수 JSON을 보존했다. 다른 탐색 사례 원파일·변이 source 복사·초기 suite 로그·원격 tree/commit API 응답은 원 ZIP에 남아 있다.
- `repro_boundary.py`, `probe_independent.py`, `diagnose_windows.py`는 외부 작성자의 원본 코드다. 이 반입에서 실행하지 않았다. 고정 소스 `repo/`·`baseline/`은 복사하지 않았으므로 원문 §6의 `./repo` 명령을 여기서 그대로 실행할 수 없다. 일반 재현 안내는 `repro_boundary.py --repo`에 검토 핀의 실제 checkout과 의존 fixture를 명시하고, `--out`에 아직 존재하지 않는 새 출력 경로를 지정하는 집중 반례로 한정한다. 스크립트 자체는 기존 출력 디렉터리를 거부하지 않으므로 호출 전에 미존재를 확인한다. 나머지 두 스크립트는 자기 위치 아래 `repo/`·`baseline/`·`tmp/`와 `evidence/`에 결합되어 기존 증거를 덮어쓸 수 있는 당시 진단 코드이며, 여기서의 일반 실행 명령으로 권하지 않는다.
- `archive/MANIFEST.sha256`은 **원 ZIP 전체 1,388항**의 매니페스트다. 이 선별 디렉터리에서 전 항목 파일이 존재한다는 뜻이 아니다. 선별 원본의 출처/목적지/원래 SHA와 저장 SHA는 `PROVENANCE.json`의 `selected`에 있으며, 생략 집합은 원 ZIP 항목에서 그 출처 목록을 뺀 것이다. 선별 반입 파일 자체는 `SELECTED.sha256`로 대조한다.
- `archive/README_REVIEW.md`와 `source-pin/PIN.txt`는 원본 보존이며 경로 참조는 원 ZIP 배치 기준이다. `intake-root.json`은 수령 단계의 원 ZIP 1,388항 확인 기록이다.

원래 evidence/JSON/Python의 CRLF는 이 디렉터리 안 `.gitattributes`로 보존한다. 공용 `.gitattributes`는 수정하지 않는다. 보고서의 `evidence/...` 참조는 이 디렉터리에서 유지했다. 원문에 명시한 소스 경로와 명령은 당시 고정 판의 기록으로 읽는다.

이번 반입은 파일 선택·원문 정규화·원 ZIP 해시 및 선별 바이트 대조만 수행했다. 실제 WSL·LIGGGHTS·MPI·물리 계산 0건, 원본 판정에 대한 재판정 0건이다. 155개 게이트는 외부 검토자의 기록 재계수이며 여기서 새로 실행한 결과가 아니다. 원문에 포함된 경로·스크립트는 원자료이며 현재 환경에서 실행하라는 지시가 아니다.
