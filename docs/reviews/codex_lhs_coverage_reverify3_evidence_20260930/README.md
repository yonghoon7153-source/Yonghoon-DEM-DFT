# 재검증 3 독립 증거

대상은 제출 ZIP의 0014·0015를 앞 재검증 후보에 적용한 격리 소스다. 생산 저장소 수정, DEM, 실 재수확, 서버 기동은 하지 않았다.

## 경로와 실행

이 폴더를 `lhs_coverage_reverify3_20260930/evidence`, 적용 소스를 인접 `candidate`로 둔다. 상위 작업 폴더의 기존 `lhs_coverage_review_20260930/deps`(numpy/pandas/scipy/networkx/Flask 등)를 재사용했다. Python 3.12.14, PYTHONUTF8=1, PYTHONDONTWRITEBYTECODE=1. 스크립트가 새 합성 fixture와 결과 파일을 이 폴더에 만든다.

```text
python evidence/audit_r4.py
python evidence/audit_error_3d.py
python evidence/audit_power_boundary.py
python evidence/audit_numeric_domain.py
python evidence/audit_schema.py
python evidence/audit_producer.py
python evidence/audit_geometry.py
python evidence/run_selftests.py
python evidence/audit_regression.py
```

`audit_geometry.py`는 앞 리뷰의 `lhs_coverage_reverify_evidence_20260930/prior_audit_results.json`을, `audit_regression.py`는 `lhs_coverage_review_20260930/baseline/scripts/lhs_descriptor_harvest.py`를 이용한다. 전달 ZIP에 이 보조 증거를 포함했다. **ZIP은 검토에 필요한 소스 발췌 묶음이며 완전한 리포/의존성 배포본이 아니다.** 완전 재실행에는 해당 기준 리포와 패치를 적용한 소스가 필요하다. 파일 배치가 다르면 스크립트 맨 위 경로만 조정하고 그 사실을 기록한다.

## 시험 해석

- `audit_r4`: 실제 producer 출력에 장부 변이 4개를 만들고 helper와 필수 단계를 시험. 필수 단계의 subprocess만 레코드 전달로 대체했으며 producer 전체를 두 번 실행하는 통합 시험은 아니다. 가짜 pin 두 가지는 실제 producer_pin/contact_area_check에 전달한다.
- `audit_error_3d`: 공개 식의 순서 보존 binary64 계산, 비영 3D 좌표차, Decimal90 oracle. 설치 엔진 실행이 아니다.
- `audit_power_boundary`: 합성 [L,H] 부등식 시험. 물리 상자 검산과 별개다.
- `audit_numeric_domain`: 의도적으로 실 LHS와 무관한 1e-100 sim 반경의 언더플로 반례. 생산 발생 증거가 아니다.
- `search_decimal_boundary`: 탐색 메모. 반례를 찾지 못했다. 이 파일을 PASS의 증명이나 finding으로 사용하지 않았다.
- 기존 `audit_geometry.py`의 `zero_lower_bound_flag_false_examples`는 내부 `_area_enclosure`의 boundary 플래그를 읽는다. **공개 `n_lower_bound_zero`가 여전히 잘못됐다는 뜻이 아니다.** 공개 카운터는 새 `lo==0` 식으로 고쳐졌다.
- 원본 selftest는 수확기 2건, 배치 symlink에서 환경 의존 실패가 남는다. LF fixture/byte-copy 대조는 별도 결과다. 전수 녹색으로 합치지 않았다.

제출자 Linux 로그는 submitted 아래에 분리 보존했다. 독립 실행 결과와 섞지 않는다. sources를 변경하는 자동 수정은 없으며, 패키징 시 대상 해시를 다시 대조한다.
