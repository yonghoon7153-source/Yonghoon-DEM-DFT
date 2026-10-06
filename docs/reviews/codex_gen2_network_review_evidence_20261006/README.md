# 접촉망 세대 2 리뷰 증거

대상 핀은 `c13da95a3d1b583e853365a93d96d55285ad91a8`이다. 결론은 `codex_review_gen2_network_20261006.md`에 있다. 대상 소스를 고친 패치나 새 DEM/MPM 캠페인 결과가 아니다.

## 구성

- `source/`: Git blob 해시로 검증한 고정 소스와 원자료 130개. 전체 저장소 복제본은 아니다.
- `source_manifest.json`: 원본 Git blob SHA와 SHA-256.
- `probes/`: 검토자 반례. 생산 코드를 수정하지 않고 실제 함수를 부른다.
- `evidence/`: 실제 계산 결과와 검사 로그. `publication/`의 다섯 폴더는 합성 생산·변이체 픽스처이지 실제 194 캠페인이 아니다.
- `bundle_manifest.json`: 전달 파일의 해시 목록. 이 파일 자체는 목록에서 제외한다.
- `verify_bundle.py`: 네트워크 접근 없는 읽기 전용 무결성 검사.

## 재현

묶음 최상위에서 `python3 verify_bundle.py`로 먼저 검증한다. Python 3와 NumPy, SciPy, NetworkX, Flask, pandas가 필요하다. 검토 환경 버전은 `evidence/environment.json`에 있다. `run_tests.py`의 외부 로컬 의존성 경로가 없어도 해당 패키지가 환경에 설치되어 있으면 실행할 수 있다.

```bash
python3 run_tests.py
python3 extra_tests.py
python3 probes/adversarial.py
python3 probes/publication.py
python3 probes/handover.py
python3 probes/real_beds.py
python3 probes/reference_checks.py
python3 probes/flux_refinement.py
```

재현은 `evidence/`의 출력을 다시 생성한다. 보존본과 비교하려면 복사본에서 실행한다. 게시 테스트의 실행 ID·시각은 재실행마다 달라질 수 있다. 값·상태·수용 여부를 비교한다. 수치 라이브러리/플랫폼에 따른 마지막 자리 차이를 비트 불일치 결함으로 읽지 않는다.

`reference_checks.json`의 `multiply_better_all=false`는 **nr=160의 10점**에 대한 값이다. s=0.05를 세분한 `flux_refinement.json`에서 nr=400·600은 곱셈이 더 가까워진다. 두 파일을 분리해 일부만 인용하지 않는다. H12 구 사슬 반례의 FV 값은 nr=100·200·400이며, 외삽 없이도 s=0.45에서 전도도 오차가 −5%를 넘는다.

전체 `check_all.sh`, 194 전수 새 배치, 세대 3·공유-코어·미구현 합집합 피복은 이 묶음의 실행/보증 범위가 아니다.
