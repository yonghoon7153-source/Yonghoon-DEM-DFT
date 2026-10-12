# 재검증 7 전달 묶음

판정 본문: `codex_review_gen2_network_reverify7_20261012.md`.

고정 핀: `3cedd40a5911d0606bf33ed2085d5cb93c4db2e0`. 읽기 전용 코드 심사 + 허용된 CPU 합성 생산/기록 재독해. DEM/MPM·WSL·194 생산은 실행하지 않았다. 보충 20 지원은 범위 밖.

## 구성

- `source/`, `source_manifest.json`, `tree.json`: 고정 핀의 필요한 573파일 및 Git blob/SHA-256 근거. 전체 Git checkout이 아님.
- `parent/scripts/`: 수정 부모의 원본 두 스크립트.
- `baseline_r6/`: 이전 리뷰의 32 봉인 파일·인계 도구·기존 일곱 입력·비교 manifest를 ZIP에 동봉. 재계산 독립성 확인용이며 현재 생산 코드가 아님.
- `submitted/request.md`: 사용자 첨부와 핀에서 바이트 동일한 요청서.
- `probes/`, `run_checks.py`: 독립 재현 코드. 생산 코드 수정 없음.
- `evidence/`: rc·stdout·실제 CLI 결과·함수 탐침·원자료 해시/접촉 재계산·환경/최종 QA.
- `notes/`: 독립 검토 세 갈래의 상세 기록. 최종 판정은 본문이 우선.
- `MANIFEST.sha256.json`: ZIP payload의 크기·SHA-256 목록. manifest 자체는 목록에서 제외.

## 재현

Python 3.12, NumPy/SciPy/NetworkX/Flask/Pandas/Matplotlib 등 저장소 분석 의존성 필요. 실행 환경의 실제 버전은 `evidence/r7_final_qa.json` 참조. `run_checks.py`의 기존 로컬 의존성 폴더가 없는 경우 표준 설치된 패키지를 사용한다. 패키지 설치·생산 실행은 자동으로 하지 않는다.

```text
python run_checks.py reread
python run_checks.py r7_cli
python run_checks.py r7_parent_cli
python run_checks.py r7_predicates r7_contract test_quality_probe
python run_checks.py r7_final_qa
```

CLI 재현은 순서대로 실행한다. `r7_parent_cli`는 직전에 만든 합성 정상 ROOT를 복사해 사용한다. `tmp/` 생성물이 필요하지만 ZIP에는 넣지 않았고 각 탐침이 새로 만든다. 원자료와 소스는 동봉되어 있다. 일부 긴 증거 경로는 Windows의 긴 경로 지원이 필요하다.

`smoke`는 Windows에서 `os.wait4` 부재로 중단했다. `smoke_real`은 실행하지 않았다. 발사 핀에서의 fast16+real4 요구를 이 묶음으로 면제하지 않는다.

초기 `harness_*_error*` 로그는 리뷰용 탐침 오류를 숨기지 않고 보존한 것이다. 수정 뒤 `run_r7_cli.json`, `run_r7_parent_cli.json`, `r7_final_qa.json`이 실제 최종 실행 결과다. 자료와 source를 수정한 실패가 아니다.
