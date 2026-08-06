# 환경 검증 보고서

생성: 2026-08-05 11:03:23

```

### System
[  ] platform : Linux-6.18.5-fc-v18-x86_64-with-glibc2.39
[  ] python   : 3.11.15
[  ] nproc    : 4  -> run.sh --nproc 기본값 후보
[  ] memory   : 15.7 GB
[  ] disk free: 28.5 GB  -> fine 격자는 수 GB 필요

### Dependencies
[OK] numpy          2.4.6
[OK] scipy          1.17.1
[OK] pandas         3.0.5
[OK] matplotlib     3.11.1
[OK] yaml           6.0.3
[OK] openpyxl       3.1.5
[OK] joblib         1.5.3
[OK] tqdm           4.70.0
[  ] pyarrow        25.0.0 (optional)
[  ] pytest         9.1.1 (optional)
[  ] jax            미설치 (optional)
[  ] torch          미설치 (optional)

### GPU
[  ] nvidia-smi 없음 -> CPU 전용 경로로 진행
[  ] jax 미설치 (Phase 7에서만 필요)
[  ] 주의: PyBaMM DFN 단일 solve는 GPU로 빨라지지 않는다. docs/03_ARCHITECTURE.md 6절 참조

### PyBaMM
[OK] pybamm 26.7.1.0
[OK] IDAKLU: 사용 가능 (권장)
[OK] composite DFN 빌드 성공 (particle phases 2,1)
[OK] Chen2020_composite 파라미터셋 로드 성공
[  ] Nominal cell capacity: 5.0 A.h

### Benchmark
[OK] 1회 solve 소요: 2.41 s
[  ]   coarse (step 0.05)       125 cond / 4 proc  ≈ 1.3 min
[  ]   fine (step 0.02)        9261 cond / 4 proc  ≈ 93.0 min

### Summary
[OK] 진행 가능
[  ] 권장 실행: ./run.sh --mode grid --nproc 4 --solver idaklu
[  ] GPU 없음 — 문제되지 않음. CPU 병렬이 1차 경로
```
