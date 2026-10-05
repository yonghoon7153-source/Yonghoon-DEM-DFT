# RGL 수정 재검증 — 전달 묶음

먼저 `codex_review_rgl_reverify_20261005.md`를 읽으십시오.
판정 **HOLD**: 기존 P1 4건은 원 반례 경로에서 닫힘, 신규 P2 3건.
코드 핀: `bf4fb6aee0b388375ddf65694ac405e63e0e381c`.

이 묶음은 저장소 전체가 아니라 검토에 필요한 핀 고정 파일 432개와 독립 탐침입니다.
생산 코드는 바꾸지 않았습니다. 실제 194건 실행·WSL 통합·real14 회귀·재봉인은 하지 않았습니다.

## 읽는 순서

1. 판정문: 조건 1–7, RGL-01–10, 신규 RGLR-01–03, Q1–Q7.
2. `findings_review.json`: 저장소 원장과 별개인 신규 finding 목록.
3. `evidence/final_test_summary.json`: 의존 파일 보완 뒤의 최종 회귀 결과.
4. 각 evidence JSON 및 탐침 코드. 원문의 절대 경로는 실행 당시 기록이며 파일은 같은 상대 경로로 동봉했습니다.

초기 `baseline_*.json`에는 의존 파일 미반입 때문에 실패한 중간 기록도 있습니다.
이를 숨기지 않고 보존했습니다. 최종 판정은 `final_test_summary.json`을 따릅니다.
real14 입력 부족 1그룹은 여전히 미인증입니다. 체크 전체 통과라는 증서가 아닙니다.
망 JSON에 들어간 NaN은 결함 입력을 재현하기 위한 의도된 변이입니다.

## 재현

원 프로젝트 Python 의존성(NumPy/SciPy/pandas/Flask 등)을 설치한 환경에서:

~~~bash
python3 verify_source.py
python3 run_tests.py chain pipeline tau_flux tau_status network receipts contract spearman lhs power verdict step3 lw_labels rint_labels group grade
python3 run_probes.py new_network independent_lw original_g4 raw18 handover
~~~

`run_tests.py`는 당시 로컬 의존성 디렉터리 두 곳을 PYTHONPATH 앞에 추가합니다.
다른 기계에서는 해당 경로가 없어도 설치된 의존성 및 동봉 source를 사용합니다.

**collector 탐침 주의:** `original_g1`은 고정 출력명과 파일 존재로 게시 여부를 봅니다.
동봉된 `normal.json` 등 증거 파일을 그대로 둔 채 재실행하면 안 됩니다.
새 빈 검토 디렉터리에 `source/`, `run_tests.py`, `run_probes.py`,
`evidence_g1/probe_adversarial.py`만 복사하고 `evidence/`를 만든 뒤 실행하십시오.
기존 증거를 지우거나 덮어쓸 필요는 없습니다.

## 무결성

`source_manifest.json`은 각 파일의 핀 기준 Git blob과 SHA-256입니다.
`package_manifest.json`은 ZIP 내부 파일 SHA-256(자기 자신 제외)입니다.
ZIP 옆 `package_receipt.json`은 ZIP SHA-256과 실제 압축 해제 없이 CRC/파일 해시 대조한 결과입니다.
묶음 작성기는 최신 `network_adversarial.json`이 가리키는 실험 디렉터리만 포함합니다.
오래된 탐침 개발 임시 디렉터리·캐시·의존성 설치물은 제외합니다.

