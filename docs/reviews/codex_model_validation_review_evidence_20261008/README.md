# DEM 모델 검증 설계 리뷰 — 전달 묶음

정본 판정: `codex_review_model_validation_20261008.md`.

대상 핀: `61ebd181b1ae5b47a76fe69d4400e4a3950dc8a3`.
제출 요청서와 핀 요청서는 바이트 동일하다.

## 범위

설계·추론·후처리 검토만 수행했다. DEM/MPM 시뮬레이션, 덱 생산, 스케줄러 조회/조작, 생산 코드 수정, 보정은 하지 않았다.
대기 중이라고 보고된 B 런 상태는 확인하지 않았다. 보고서의 변경 권고는 실행 지시 또는 기존 등록의 변경이 아니다.

## 내용

- `source/`: 핀에서 읽은 71개 텍스트 파일. `source_manifest.json`에 Git blob 및 SHA256.
- `submitted/`: 사용자가 첨부한 요청서.
- `probes/`: 독립 산술 반례, 실제 후처리 함수 합성 입력 시험, 이식성 시험.
- `evidence/`: 결과 JSON, 표준 출력/오류, 추가로 읽은 두 소스 파일.
- `run_review_checks.py`: 원본 신원 검사 후 6개 검산을 다시 실행한다. DEM 실행 프로그램을 호출하지 않는다.
- `BUNDLE_MANIFEST.json`: 배포 파일별 크기/SHA256. 그 자신은 목록에서 제외한다.

보조 작업 메모는 정본 혼동을 피하려고 동봉하지 않았다. 실제 pure-SE 원덤프, ibb 바이너리 및 실험 표준의 원측정은 포함되어 있지 않다. 저장 CSV/JSON 재계산을 원덤프 재구성으로 읽지 않는다.

## 재현

Python 3.12.14, NumPy 2.3.5, pandas 3.0.1, NetworkX 3.7에서 확인했다. 패키지 환경은 동봉하지 않는다. 동일 의존성이 설치된 환경에서 압축 해제 루트 기준:

```text
python -B run_review_checks.py
```

검산 6개 종료 코드 0. 실제 `plane_load_share` selftest 54/54와 별도 음성 대조를 포함한다. 스트레스 탐침 두 개는 소스/입력 11개만 담은 임시 ZIP에서 풀어 JSON 동일성도 검사했다.

`mv_softening_frozen_reweight_result.json`은 감쇠 힘을 무시하는 고정 상태 구성식의 조건부 산술 예시다. DEM 실행 결과·재평형 예측이 아니며 본문 V4의 수치 예측으로 사용하지 않았다.

Windows 검산 통합의 첫 시도는 세 스크립트의 표준 출력 cp949 인코딩 때문에 종료 코드 1이었다. UTF-8 출력을 고정한 뒤 동일 계산을 다시 실행해 전부 통과했다. 이 전달 도구의 출력 문제를 생산 코드 결함으로 분류하지 않았다.

## 추가 소스 신원

- `evidence/mv_softening_in.ps_7_3_r45_61ebd18.liggghts`: 프로젝트 핀의 원 덱, Git blob `52ed80f64bd82110a4dd9d3b1127b1d514807ba8`.
- `evidence/mv_softening_normal_model_hooke_hysteresis_3d5c00f.h`: LIGGGHTS `3d5c00f20519e6bb6eb6756f51f1ad36564e649d`, Git blob `3921ff5c767324e8825e76ff7528563e92e8efd7`.

이를 ibb 실행 바이너리와의 동일성 인증으로 확대하지 않는다.
