# SUPR 입력 지문과 완료 영수증 재검증 자료

검토 핀 `df647d4e31224e1a270dae01dd41f91af3048361`, 비교 핀 `a9422d2e772f28417a6e0a5167aaab8d987bf27a`.

- 판정문: `codex_review_supr_fix_reverify_20261014.md`
- 독립 지문 검산: `probes/digest_probe.py`, `evidence/digest_probe/results.json` — 42건
- 독립 완료 검산: `probes/completion_probe.py`, `evidence/completion_probe/results.json` — 40건
- 자체시험 환경 진단: `probes/completion_environment.py`, `evidence/completion_environment/summary.json`
- 소스: `source/` 1,087파일, 원래 Git blob·SHA256는 `source_manifest.json`
- 변경 비교: `evidence/*.diff`; 원격 커밋·tree·compare 응답도 보존
- 최종 무결성: `evidence/final_qa.json`; 묶음 내 파일 목록·SHA256: `package_manifest.json`

원본 코드나 원장은 고치지 않았다. `baseline/`은 수정 전 두 모듈과 등록 문서이며, 이전 전체 체크아웃이 아니다. 합성 검산의 깨끗한 git·원자료 상태는 시험 입력이다. 실제 WSL 점검·생산 실행·발사 승인을 대신하지 않는다.

독립 탐침은 Python 표준 라이브러리 중심이다. 전체 자체시험에는 NumPy/SciPy 등이 필요하다. `completion_environment.py`, `release_with_deps.py`의 외부 dependency 경로는 이 Windows 검토 환경의 재현 기록이며 패키지에 과학 라이브러리를 넣지 않았다. 환경이 갖춰진 Linux/WSL에서는 원본 `source/scripts/supp20_input_receipt.py --selftest`를 실행한다.

완료 탐침은 기존 정상 증거를 덮지 않는다. 재실행은 새 복사본에서 기존 `evidence/completion_probe/`를 제외한 뒤 한다. 원본 제공 증거는 보존한다. `tmp/`, 캐시, 대량 중간 시험 폴더는 포장하지 않았다.
