# 재검증 5 전달 묶음

정본 판정: `codex_review_gen2_network_reverify5_20261007.md`.

- 핀 `aa7ec7fe98e8684f1a2138665f9eba978366c229`.
- WSL 증거 핀 `839dbac6bf6185f7bc7f1b7a08d21b6b469a04ef`와 scripts/webapp 차이 없음.
- 판정: HOLD. 새 수치 P1 없음; P2 G2RR5-01/02/03와 문서 P3 G2RR5-04. 생산 코드 변경·194 실행·DEM/MPM/S3 실행 없음.

## 무엇이 들어 있는가

- `source/`: 핀별 Git blob·SHA-256 검증 사본 469파일. 소스 전체 저장소가 아니라 검토 및 재현에 필요한 부분집합이다.
- `source_manifest.json`: 파일별 pin·git blob·SHA-256·바이트 수.
- `submitted/`: 전달받은 WSL 묶음의 안전한 추출본, 원 요청서. tar 원본은 source/docs/reviews/codex_gen2_network_reverify5_precheck_20261007 안에도 있다.
- `probes/`: 독립 반례 코드. `notes/`: 각 분리 검토 메모. 최종 판정이 메모보다 우선한다.
- `evidence/`: 상세 입력·출력·CLI stdout·판정 JSON. 그 안의 합성 `release/`·`TEST_ONLY_NOT_GO.md`는 관문 반례 산출물이지 실제 v1.3 배포물이나 승인서가 아니다.
- `fixtures/observation_baseline/`: 이전 검토의 합성 봉인 양성 대조군과 번역된 영수증 64파일. provenance와 SHA 기록 포함. 실제 생산194가 아니다.
- `tmp/`의 압축 해제 덤프·대형 중간 CSV는 포장하지 않았다. 원 gzip, SHA, 재현 스크립트, 판정에 필요한 결과는 보존했다.

## 읽을 순서

1. 판정문 §0·§1–4·§6–7.
2. 실제 제출 증거 검산: `evidence/submitted_verify.json` (61/61), `evidence/wsl_code_identity.json`.
3. 배포 반례: `evidence/r5_release_real_binding/results.json`.
4. 환경 오류의 음성대조 오수용: `evidence/r5_case15_pipeline_fault.json`, `r5_case15_pipeline_fault_reread.json`.
5. S0b 변이: `evidence/r5_case15_results.json`와 `r5_case15_s0b_*.json`.
6. 정상·결손·재시도: `evidence/r5_observation_run2/results.json`, `r5_observation_retry/results.json`.

## 재현

보존된 ZIP과 증거는 그대로 두고 **별도 검증 사본**에서 실행한다. Python 3.12, NumPy/SciPy/NetworkX/Flask/Matplotlib를 갖춘 환경을 사용한다. 사용된 로컬 런타임/라이브러리 버전은 `evidence/runtime.json`에 기록한다. 숫자 결과는 플랫폼 끝자리 차이가 있을 수 있다.

`run_checks.py`는 이 작업 환경의 외부 deps 폴더가 있으면 활용하며, 없으면 설치된 Python 패키지를 사용한다. 저장소 scripts/webapp는 검증 사본을 import한다. 네트워크 사용이나 시뮬레이션 발사를 하지 않는다. selftest의 launcher는 별도 WSL 수신 증거로 구분했다.

```bash
python -B run_checks.py reread publication role release
python -B run_checks.py submitted_verify policy_scope
python -B run_checks.py r5_observation -- --output-name rerun_audit
python -B run_checks.py r5_observation_retry -- --baseline-output rerun_audit --output-name rerun_retry
python -B run_checks.py r5_release_contract -- --output-name rerun_release
python -B run_checks.py r5_release_real_binding -- --output-name rerun_binding
python -B run_checks.py r5_case15
python -B run_checks.py r5_case15_pipeline_fault
python -B run_checks.py r5_case15_fault_reread
```

각 `rerun_*`은 없는 새 이름을 쓰면 기존 증거를 보존한다. case15·selftest·제출 검산은 같은 이름의 로그/결과 JSON을 다시 쓰므로 **검증용 사본에서만** 실행한다. 관문 반례 probe의 rc0은 예상된 오수용 현상을 재현했다는 뜻이지 배포 GO가 아니다. 로컬 release selftest의 V10a Windows 경로·V16a 비-Git 사본 실패 두 개는 판정문에 공개했다.

`r5_release_real_binding`은 동봉된 실제 감사 CLI 실패 JSON을 fixture에 이식해 배포 관문을 검증한다. `r5_case15_fault_reread`는 앞선 fault probe와 case15 probe의 결과를 소비하므로 순서를 지킨다. 거대한 원194 생산물이나 새194 값의 정당성을 이 묶음으로 주장하지 않는다.
