# R160 비교 기준 메타데이터 정정 기록

사용자가 승인한 현재 메타데이터 정정이다. 보존 준비 완료 알림 이후 수정 전 원문을 `before/` 아래 원래 상대 경로대로 먼저 복사했다. 원본 ZIP·ZIP 영수증·원본 package manifest·Java·MPH·원시 CSV·로그는 수정하지 않았다.

## 원인과 바로잡은 기준

`work/radial160/prepare_source.py`는 이전 단계의 비교 계약을 상속한 뒤 `baseline_name`을 R80으로 바꾸면서, 기존 `baseline_source_sha256=dbcb95...`와 `baseline_contract_path=outputs/mesh_axes/comparison_contract.json`을 남겼다. 실제 R160 생성 소스와 분석 입력은 R80을 사용했지만 계약 메타데이터에는 R80 이름과 더 오래된 Preflight 계보가 섞여 있었다.

현재 주 비교 기준은 아래 네 필드를 **하나의 `baseline_identity` 묶음**으로 저장·검증한다. 기존 flat 필드도 같은 값으로 유지한다.

| 필드 | 현재 정확한 값 |
|---|---|
| name | `Caps300R80H0500` |
| source_path | `outputs/comsol63/time_caps/Caps300R80H0500.java` |
| source_sha256 | `6ab32b93310657265906cc858af3847d662923cf7dd8964feb74ed6cbe86f2b1` |
| job_id | `72c9c6b5210a4e0d96b74290e4392423` |

직접 상속한 계약 경로는 `outputs/time_caps/comparison_contract.json`이다. `dbcb95c47abad474485fcc281fe71f30c5a2e48204c2c65614d780c203724adf`는 `PreflightMeshFine5s.java`의 **ancestor** SHA로 별도 기록한다. `outputs/mesh_axes/comparison_contract.json`도 ancestor 계약 경로로 구분한다. 기존 source_configs의 소스 생성 계보나 과거 단계의 계약·manifest에 있는 정당한 ancestor SHA는 전역 치환하지 않았다.

## 변경 및 재발 방지

- `prepare_source.py`는 `baseline_metadata.py`를 통해 이름·경로·실제 소스 SHA·job ID를 함께 설정한다. 이전 계약의 일부 필드만 덮어써서 다른 계보와 섞이는 경우를 막는다.
- `analyze_results.py`는 분석 전에 위 묶음과 별칭, 실제 config/job, 디스크의 baseline Java SHA를 교차검증한다.
- 현재 `comparison_contract.json`과 `results/analysis.json`의 복사 계약·계약 SHA를 동기화했다.
- `figures/radial160_comparison_summary.json`에서 analysis 입력 SHA 한 항목만 갱신했다. 그림의 데이터·수치·PNG/PDF는 바뀌지 않았다.
- README에 원본 archive manifest와 정정된 현재 파일의 명세가 다르다는 안내를 추가했다.

계약 SHA는 `dc03064c40ec126c7c59f2b08ccf8bf3a87ba7aaf878445c69a51813c16c20ed`에서 **`e0fb7662ff0e053fe1ef93568526692835c66c30e6367b26cf5d5b84540f6ef5`**로 바뀌었다. 정확한 파일별 전후 크기·SHA·백업 위치는 `before_after_sha256.json`에 있다.

## 바뀌지 않은 수치와 원본 archive

analysis JSON에서 계약과 계약 SHA 두 필드를 제외한 모든 데이터는 정정 전과 deep-equal이다. 표면·전압 값, 최대 시각/위치, 허용오차, 범위 guard, 수렴 판정과 원시 CSV는 변경하지 않았다. 기존 80→160 최대 전압 차이 `1.248218114 mV @0.01 s`, 표면 조성 차이 `2.091183902e-5 @0.01 s / N 52 µm`도 동일하다.

원본 `COMSOL63_RADIAL160_HANDOFF.zip`은 **226,198,096 bytes**, SHA-256 **`39ded591a29568d58b57791bf68147292a9cef06660de40b1c5e45ed16b434bc`** 그대로다. 원본 `outputs/radial160/package_manifest.json` SHA **`6ab54917edbec8eda5d19b4add2233c3daf09ff55ee2a9ef98dbb84f67cc584b`**와 원본 영수증도 유지한다. 이 manifest는 **원래 ZIP 안의 payload**를 설명하며, 정정된 현재 contract·analysis 파일의 해시 명세로 사용하면 안 된다.

정정된 현재 메타데이터 파일만의 명세는 `outputs/radial160/current_metadata_manifest.json`이다. 이는 새 전체 전달 ZIP의 manifest를 대신하지 않는다. 새 전달물 전체는 root가 생성하는 새 패키지 manifest로 별도 검증하며, 이 정정 전후 ledger와 원본 archive 식별을 함께 보존한다. self-hash를 포함시키는 순환 명세는 만들지 않았다.

## 검증

회귀 테스트 **24개 통과**: 기존 수치 분석 13개, baseline 메타데이터 11개. 잘못 상속한 이전 계약, 이름·경로·SHA·job의 개별 불일치, flat/atomic 필드 불일치, 실제 소스 digest 불일치, 파생 계약·해시 불일치를 검사한다. 격리된 합성 fixture에서 실제 `prepare_source.py`를 실행해 다시 생성한 계약이 현재 정정 계약과 같고, 생성 Java 바이트가 기존 R160 Java와 같음을 확인했다. COMSOL은 실행하지 않았다.

독립 감사에서 Windows 역슬래시 경로와 새 슬래시 경로가 같은 analysis 파일에 서로 다른 SHA를 가리키는 중간 교정 오류를 발견했다. 최종본은 원래 존재한 키의 SHA만 바꾸며, 경로 정규화 뒤 중복 키를 거부하고 모든 figure 입력 SHA를 실제 파일과 비교한다. 이 회귀 검사를 추가한 뒤 전체 24개가 통과했다.

첫 격리 fixture 시도는 Windows 제한 토큰의 Python 임시 폴더 접근 오류로 실패했다. 동일 테스트 명령을 일반 사용자 권한 예외로 실행했다. 관리자 설정이나 시스템 ACL을 변경하지 않았다. 테스트 임시 폴더는 전달 대상이 아니다.

```text
python -B -m unittest discover -s work/radial160 -p "test_*.py" -v
```

현재 메타데이터 수정은 새 물리 해석이나 수치 결과 개선을 뜻하지 않는다. 새 R160 H0250 실행의 승인·수치 결과는 별도 새 작업 기록에서 다룬다.
