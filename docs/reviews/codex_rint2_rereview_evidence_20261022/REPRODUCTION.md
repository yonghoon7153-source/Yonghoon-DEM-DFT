# Rint ② re-review evidence — 2026-10-22

먼저 `codex_review_rint2_rereview_20261022.md`를 읽으세요. 요청한 판정·최소 해결·C1–C8·30개 미결·재현 범위가 그 파일에 있습니다.

- `source/`: 원격 고정 핀에서 읽은 검토 대상 파일. 생산 소스를 수정하지 않았습니다.
- `source_manifest.json`: Git blob와 SHA256. `integrity_final.json`: 포장 직전 전체 대조 결과.
- `registration/`, `certificate/`, `geometry/`, `probes/`: 독립 탐침. 생산 캠페인이 아닌 작은 해석/합성 시험입니다.
- `evidence/`: 소스/ZIP 대조와 S0 작은 census 본체·귀속 관문의 결과. `s0_integration_probe.json`은 실제 셸 실행 시 환경 제약 실패를 그대로 보존한 것이며, 성공한 제한 탐침은 `_fixed_argv.json`입니다.
- `delivery_manifest.json`: 포장 파일별 SHA256. 최종 ZIP SHA256는 ZIP 외부 `delivery_receipt.json`에 있습니다.

Python + NumPy + SciPy가 필요합니다. 리뷰 환경은 Python 3.12.14 / NumPy 2.5.3 / SciPy 1.16.3 / 각 BLAS 1스레드였습니다. 과거 probe의 Windows 의존성 검색 경로가 있더라도 없으면 일반 설치된 패키지를 사용합니다.

압축 푼 폴더에서:

```bash
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 registration/probe_registration_current.py
python3 certificate/probe_certificate.py
python3 certificate/run_selected_tests.py
python3 geometry/run_review.py
python3 probes/provenance_probe.py
python3 probes/s0_integration_probe.py --fixture-argv
```

작성자 트리를 대조할 때만 `RINT_REVIEW_SOURCE=/absolute/path/to/repo`를 지정하세요. 기본은 동봉 `source/`입니다. Git 밖 F1 관측은 실제 실행 경로가 Git 안이면 달라질 수 있습니다. status 실패·혼합 clean HEAD 탐침은 별도로 명시적 입력을 주므로 구분해서 읽으세요. 탐침은 기록된 결과 파일을 갱신하므로 포장 당시 증거를 보존하려면 복사본에서 재실행하세요.

전체 셸 러너·전체 회귀·S0 실침대·R 캠페인은 실행하지 않았습니다. `--fixture-argv`는 셸 인자를 고정 작은 입력으로 바꾸고 단계 2 Git 계획 선행관문을 제외하여 실제 census 본체를 시험합니다. 이것을 전체 CLI 통과로 읽지 마세요.

보고서의 새 반례는 '반례가 현재 존재함'을 재현합니다. 잘못된 동작이 관측돼도 probe 자체의 정상 종료코드는 0일 수 있습니다. 소스 수정 후에는 각 JSON의 expected bad outcome이 거부/안전한 상태로 바뀌는지 대조해야 합니다.
