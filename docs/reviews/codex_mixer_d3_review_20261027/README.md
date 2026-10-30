# 독립 리뷰 증거 — 2026-10-27

리포 제품 코드는 수정하지 않았습니다. snapshot/의 소스는 각 고정 pin 또는 명시된 과거 baseline의 바이트이며, 리뷰 탐침·입력·로그는 evidence/에 따로 있습니다. 제출 원본 ZIP의 실행 지시를 자동 실행하지 않았습니다. 실제 DEM, WSL, scheduler 호출은 0회입니다.

## 먼저 읽을 것

- 루트의 codex_review_mixer_*.md: 판정, 반례, 최소 해결, 직접 검증의 한계.
- 해당 d2/evidence/independent_results.json 또는 d3/evidence/independent_results.json: 새 독립 검산.
- 해당 */blob_verification.json: 받은 리포 파일과 원격 pin blob 대조.
- evidence_manifest_verification.json, gate_pin_comparison.json: 제출 증거 및 과거 gate 코드 신원 대조. 새 전체 gate 실행을 뜻하지 않습니다.

## 재현

필요 환경: Python 3.11 이상. D2 의존성 numpy/scipy 등은 같은 리포 요구를 따릅니다. 파일 길이 제한을 피하려면 짧은 디렉터리에 풉니다.

D2:
python3 -I -X utf8 -B d2/evidence/independent_probe.py
python3 -I -X utf8 -B run_existing.py d2 test_mixer_d2_consumers.py

D3:
python3 -I -X utf8 -B d3/evidence/independent_probe.py
python3 -I -X utf8 -B run_existing.py d3 test_mixer_d3_candidates.py

개별 ZIP에는 해당 D2 또는 D3만 있습니다. D2 탐침의 통과는 현 버전의 false-PASS 반례가 재현됐다는 뜻이며 제품 수용 PASS가 아닙니다. 수정 후에는 탐침의 반례 기대값을 거부로 바꾼 회귀를 작성해야 합니다. D3 CLI 재현은 매회 새 cli-replay-* 폴더를 써 덮어쓰기를 피합니다.

run_existing.py는 테스트 실행기의 Python UTF-8과 작업 임시 폴더만 조정합니다. 제품 판정·통계·파일 의미를 바꾸지 않습니다. Windows에서 구 회귀의 POSIX mode/CRLF 문제와 D3 symlink 생성 권한 제한이 있었으며 판정문에 모두 구분했습니다. 이전 실패 로그와 최종 결과를 모두 보존하므로 로그 개수나 PASS 수를 합산하지 마십시오.

## 파일 무결성

MANIFEST.sha256은 이 독립 리뷰 묶음 안의 파일 바이트 해시입니다(자기 자신 제외). 받은 ZIP 자체의 SHA는 intake.json과 판정문에 있습니다. 소스 pin은 리뷰 대상의 신원이고, 이 리뷰 묶음은 새 Git commit 또는 원격 게시물이 아닙니다.
