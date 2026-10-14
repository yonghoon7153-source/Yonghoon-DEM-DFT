# LHS214 실패 분류안 검토 증거

판정문: `codex_review_lhs214_failures_20261014.md`

검토 핀: `1087a9b2f4a93aa6a3b0debc698a14fffa13488d`

## 내용

- `submitted/`: 사용자 요청서, 원 tgz, 안전하게 추출한 60파일
- `source/`, `source_manifest.json`: 고정 핀 소스와 Git blob/SHA256 목록
- `probes/`: 실제 함수 소형 반례 및 실행 기록 독립 대조
- `evidence/`: 재계산 결과·소스 비교·입력 목록
- `notes/`: 수치 경로, 소비 경로, 원 실행 증거별 상세 검토
- `package_manifest.json`: 검토 패키지 각 파일의 SHA256

생산·실침대 실행, 대상 코드 수정, 원장 변경, Git 상태 변경은 하지 않았다. 자료에 포함된 명령은 재현 설명이며 생산 발사 승인이 아니다.

## 재현

Python 3.12, NumPy/SciPy 필요. 검토 실행은 NumPy 2.5.3/SciPy 1.16.3을 사용했다. 세 도구는 검토 폴더의 `evidence/`만 갱신하며, solver 탐침의 함수 치환은 메모리에서만 일어나고 복원된다.

```text
python -B probes/evidence_audit.py
python -B probes/solver_probe.py
python -B probes/consumer_contracts.py
```

프로브에는 이 작업 폴더의 기존 과학 계산 의존성 경로가 선택적으로 추가되어 있다. 외부 환경에서는 해당 경로가 없어도 일반 Python 환경에 설치된 NumPy/SciPy로 임포트할 수 있다. 원 tgz의 모든 개별 파일 해시는 `evidence/input_inventory.json`, 재계산 집계는 `evidence/evidence_recomputed.json`에 있다.

주의: 별도 `lhsx_054` 진단의 입력 digest/원 실행 provenance와 나머지 13건의 하위 수치 증서는 제출되지 않았다. 상세 판정의 이 한정을 제거하지 말 것.
