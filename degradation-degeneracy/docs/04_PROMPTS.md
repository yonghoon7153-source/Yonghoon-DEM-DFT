# 04. PROMPTS — 단계별 실행 프롬프트 (git 연동)

> 각 Phase를 **순서대로** 실행한다. 한 Phase가 끝나면 반드시 커밋하고, 다음으로 넘어간다.
> 프롬프트는 그대로 복사해서 코딩 에이전트에 붙여넣으면 된다.

---

## git 규칙 (전 Phase 공통)

### 브랜치

```
main                          # 항상 동작하는 상태
├── phase0/scaffold
├── phase1/refactor-core
├── phase2/mode-composition
├── phase3/grid-parallel
├── phase4/fitting
├── phase5/scoring
├── phase6/objectives
└── phase7/gpu-attempt        # 실패해도 기록 남김
```

### 커밋 메시지 규약

```
<type>(<scope>): <요약>

<본문 — 왜 이렇게 했는지>

Refs: <관련 슬라이드 페이지 또는 문서>
```

| type | 용도 |
|---|---|
| `feat` | 새 기능 |
| `fix` | 버그 수정 |
| `refactor` | 동작 변경 없는 구조 개선 |
| `physics` | **물리 파라미터·수식 변경 (반드시 근거 명시)** |
| `test` | 테스트 추가 |
| `perf` | 성능 개선 |
| `docs` | 문서 |

예시:
```
physics(baseline): 완방상태 하드코딩 제거, 자동 산출로 전환

원본 코드의 36.7/3446.3/58439.9는 이전 baseline 기준 값으로,
코드 내 경고 주석에 "다시 뽑아야 함"이라 명시되어 있었음.
매 실행 시 0.05C 방전 시뮬레이션으로 산출하고 baseline 해시로 캐시.

Refs: 02_CODE_AUDIT.md C1, 32p
```

### 각 Phase 종료 시 필수

```bash
pytest tests/ -v                  # 전부 통과
git add -A
git commit -m "..."
git tag phase<N>-done
git checkout main && git merge phase<N>/...
```

---

# Phase 0 — 스캐폴딩 · 환경

## 프롬프트

```
docs/00_START_HERE.md, 01_CONTEXT.md, 02_CODE_AUDIT.md, 03_ARCHITECTURE.md를 모두 읽어라.
발표 PDF에서 21, 22, 32, 33, 34페이지를 확인하고 수식·파라미터를 대조하라.

그 다음 Phase 0을 수행한다:

1. git 저장소 초기화, .gitignore 작성
   (results/, .venv/, __pycache__/, *.parquet, *.h5, .cache/)

2. 03_ARCHITECTURE.md 1절의 디렉터리 구조를 그대로 생성.
   각 .py는 빈 파일이 아니라 docstring + 함수 시그니처만 있는 스텁으로.

3. requirements.txt 작성 (00_START_HERE.md 2.2절 기준)

4. scripts/verify_env.py 작성 및 실행.
   - pybamm 버전
   - IDAKLU 사용 가능 여부 (안 되면 casadi fallback 기록)
   - composite DFN 빌드 성공 여부
   - nproc, GPU 유무
   결과를 docs/ENV_REPORT.md에 저장.

5. configs/base.yaml 작성 — 03_ARCHITECTURE.md 3.1절 그대로.
   원본 코드(degrade_mode_sim_me.py)의 initialization() 값과
   한 줄씩 대조해서 일치하는지 확인하고, 대조 결과를 주석으로 남길 것.

6. run.sh 뼈대 작성 — 인자 파싱만. 내부는 "not implemented" 출력.
   --mode verify 만 실제 동작하게.

7. README.md 작성 — 프로젝트 목적 3줄 + 빠른 시작.

완료 후:
  ./run.sh --mode verify   가 성공해야 한다.
  git commit -m "feat(scaffold): 프로젝트 구조 및 환경 검증"
  git tag phase0-done
```

### 완료 기준
- [ ] `./run.sh --mode verify` 성공
- [ ] `docs/ENV_REPORT.md`에 IDAKLU 가용 여부 기록
- [ ] `configs/base.yaml`이 원본 `initialization()`과 값 일치

---

# Phase 1 — 코어 리팩터링

## 프롬프트

```
Phase 1: 원본 스크립트를 순수 함수 기반으로 이식한다.
02_CODE_AUDIT.md의 CRITICAL 항목(C1~C4)을 모두 해결한다.

구현 대상:

[src/config.py]
  - yaml 로드, 스키마 검증, config 해시 계산
  - 필수 키 누락 시 명확한 에러

[src/model.py]
  - build_model() : DFN + particle_phases ("2","1") + current sigmoid
  - 모델을 모듈 레벨에서 1회만 빌드하고 재사용 (discretisation 비용 회피)

[src/baseline.py]
  ★ C1 해결
  - get_baseline_params(config) -> dict
  - get_discharged_state(config, cache_dir) -> DischargedState
      * baseline 파라미터 해시를 키로 캐시
      * 캐시 미스 시 0.05C 방전 시뮬레이션 실행
      * 원본의 하드코딩(36.7, 3446.3, 58439.9)은 절대 사용 금지
      * 산출된 값을 로그에 출력하고 원본 값과의 차이를 경고로 표시

[src/runner.py]
  ★ C2 해결
  - build_param(baseline, overrides) -> pybamm.ParameterValues
      * 매번 새 객체 생성. 전역 param 변형 금지
  - run_one(overrides, protocol, solver_cfg) -> Solution | None
      * try/except로 감싸고 실패 시 None + 사유 반환

[src/protocol.py]
  - 원본의 experiment / experiment2를 charge_first / discharge_first로
  - mode_protocol 매핑 유지

[src/curves.py]
  - extract_curves(solution) -> dict
      * normalized capacity, PE OCP, NE OCP, full cell
      * n_trim 적용 (원본과 동일하게 끝단 3포인트)
      * 원본의 windowed_curve 로직 그대로 이식
  - to_dvdq(), to_dqdv() — savgol 스무딩 포함

[src/io.py]
  - save_parquet, load_parquet, write_manifest
  - manifest에 git commit hash, config hash, 환경 정보 기록

C3, C4 해결:
  - 모든 Windows 절대경로 제거, pathlib 사용
  - os.chdir 호출 삭제
  - matplotlib.use("Agg") 기본

테스트:
  tests/test_baseline.py — 완방상태가 재현 가능한가 (2회 실행 동일)
  tests/test_runner.py   — 동일 overrides로 2회 실행 시 결과 동일 (전역 오염 없음)

완료 후:
  git commit -m "refactor(core): 순수 함수 기반 이식, 전역 param 제거"
  git commit -m "physics(baseline): 완방상태 하드코딩 제거, 자동 산출"
  git tag phase1-done
```

### 완료 기준
- [ ] `get_discharged_state()`가 값을 산출하고 로그에 원본과의 차이 출력
- [ ] 동일 조건 2회 실행 결과가 완전 일치 (전역 오염 없음)
- [ ] 코드베이스에 Windows 경로·`os.chdir` 없음

---

# Phase 2 — 모드 중첩 · 32p 재현

## 프롬프트

```
Phase 2: 열화 모드를 파라미터로 변환하는 로직을 구현하고, 32p 그림을 재현한다.

[src/modes.py]
  ★ 03_ARCHITECTURE.md 4절의 build_overrides()를 그대로 구현
  - 적용 순서 고정: LAM_PE → LAM_NE → LLI
  - lam_pe_type, lam_ne_type ("de" | "li") 지원
  - 단일 모드일 때 원본 코드의 update_fn과 정확히 동일한 dict를 반환해야 함

[src/sweep.py]
  - run_sweep1d(mode, values, config) -> list[Solution]
  - 원본의 5개 모드 + reference를 모두 지원
  - 모드별 프로토콜 매핑 준수 (LLI/LAM_ne_li는 discharge_first, 나머지 charge_first)

[tools/plot_sweep1d.py]
  - 32p와 동일한 2×3 subplot 생성
  - Reference / LLI / LAM_ne_li / LAM_ne_de / LAM_pe_li / LAM_pe_de
  - 정규화 용량 축, PE·NE·full cell 곡선

[tests/test_modes.py]  ★ 가장 중요
  - test_single_mode_matches_original():
      각 모드 × [0, 0.1, 0.2, 0.3]에 대해
      build_overrides() 결과가 원본 update_fn 결과와 일치
  - test_zero_degradation_is_identity():
      모든 값 0이면 overrides가 비어야 함
  - test_reference_equals_lli_zero():
      원본 코드의 디버그 블록과 동일한 검증.
      reference 용량과 LLI=0 용량 차이 < 0.01 mAh
  - test_composition_order():
      LAM_NE + LLI 동시 적용 시 최종 농도가 예상값과 일치

run.sh에 --mode sweep1d 연결.

완료 후:
  ./run.sh --mode sweep1d --out results/sweep1d_v1
  → results/sweep1d_v1/figures/32p_reproduction.png 이 원본 32p와 육안 일치해야 함

  git commit -m "feat(modes): 열화모드 파라미터 변환 + 중첩 지원"
  git commit -m "test(modes): 원본 코드 회귀 검증"
  git tag phase2-done
```

### 완료 기준
- [ ] 32p 6-panel 그림이 육안으로 재현됨
- [ ] `test_reference_equals_lli_zero` 통과 (원본이 우려했던 오염 없음)
- [ ] 단일 모드 override가 원본과 완전 일치

---

# Phase 3 — 조합 격자 · 병렬화 ★

## 프롬프트

```
Phase 3: 조합 격자를 생성하고 병렬 실행한다. 이 프로젝트의 핵심.

[src/grid.py]
  - parse_axis(spec: str) -> np.ndarray
      "0:0.2:0.02" | "0,0.05,0.1" | "0.1" | "none" 파싱
  - build_conditions(axes: dict) -> list[Condition]
      itertools.product로 조합 생성
      각 Condition은 (lli, lam_pe, lam_ne, lam_pe_type, lam_ne_type, noise_level, seed)
  - run_grid(conditions, config, nproc, chunk_size, out_dir, resume)
      * joblib.Parallel(backend="loky")
      * chunk 단위로 parquet 저장 (메모리 폭발 방지)
      * 실패는 failed.csv에 기록하고 계속
      * resume: manifest의 완료 목록을 읽고 건너뜀
      * tqdm 진행률

  ★ 병렬 안전성:
     각 워커는 자체 param 객체를 생성해야 함 (Phase 1에서 해결한 부분)
     모델은 워커별 1회 빌드 후 재사용

[src/io.py 확장]
  - 청크 저장/병합
  - manifest에 완료 조건 목록 append (resume용)

[run.sh]
  - --mode grid 구현
  - --dry-run 필수 구현:
      조건 수, 예상 시간(샘플 5개 실측 × 조건수 / nproc), 예상 용량 출력 후 종료
  - --resume 구현

노이즈:
  - full cell 전압에 gaussian 추가: V + N(0, sigma)
  - sigma는 --noise 인자, seed 고정으로 재현성 확보
  - 노이즈 적용 전 원본 곡선도 함께 저장

성능 목표:
  coarse 격자(step 0.05, 125조합)가 nproc=8에서 5분 이내

완료 후:
  ./run.sh --mode grid --lli 0:0.2:0.05 --lam-pe 0:0.2:0.05 --lam-ne 0:0.2:0.05 --dry-run
  ./run.sh --mode grid --config configs/grid_coarse.yaml --nproc 8 --out results/grid_coarse_v1

  git commit -m "feat(grid): 조합 격자 생성 및 병렬 실행"
  git commit -m "perf(grid): chunk 저장 + resume 지원"
  git tag phase3-done
```

### 완료 기준
- [ ] `--dry-run`이 조건 수·예상시간·용량 출력
- [ ] coarse 격자 125조합이 병렬 실행되고 parquet으로 저장
- [ ] 중간에 kill 후 `--resume`으로 재개 성공
- [ ] 실패 조건이 있어도 전체가 죽지 않음

---

# Phase 4 — Fitting 이식

## 프롬프트

```
Phase 4: 33p MATLAB fitting 코드를 Python으로 이식한다.

[src/objective.py]
  ★ 34p 수식 그대로:
     J(p) = w_pocv·RMSE_pocv/scale_pocv
          + w_dvdq·RMSE_dvdq/scale_dvdq
          + w_dqdv·RMSE^w_dqdv/scale_dqdv

  - make_objective(weights, scaling, dqdv_cfg) -> callable
  - RMSE^w_dqdv : peak 구간 가중 (33p "peak weight factor")
      scipy.signal.find_peaks로 피크 검출, prominence 기준
      피크 ±window 구간에 peak_weight 배 가중
  - scale은 reference 조건의 RMSE로 정규화

[src/fitting.py]
  - windowed_curve(f_ref, x, alpha, beta)   ← 원본 그대로 재사용
  - reconstruct(p, f_pe_ref, f_ne_ref, x)   -> (pe, ne, fullcell)
      p = [a_PE, b_PE, a_NE, b_NE]
  - fit(target_curve, refs, objective, init, lb, ub, n_restarts)
      * scipy.optimize.minimize(method="L-BFGS-B") 또는 differential_evolution
      * n_restarts: 초기값을 bound 내에서 랜덤 샘플링해 여러 번 실행
        → 결과가 서로 다르면 그 자체가 축퇴 증거
      * 반환: best p, J, 모든 restart 결과, 수렴 여부

  - to_degradation_modes(p) -> dict
      LAM_PE = (1 - a_PE)
      LAM_NE = (1 - a_NE)
      LLI    = (1 - a_PE) + (b_PE - b_NE)     ← 원본 부호 규약 유지 (Birkl 2017)

  ⚠ bound 주의:
     원본 33p는 ub=[1.1, 0, 1.1, 0], lb=[1.00, -0.3, 1.00, -0.15].
     α 하한이 1.00이면 열화(α<1)를 표현할 수 없다.
     → 정규화 기준을 확인하고, 필요하면 lb를 0.5까지 확장.
       변경 시 physics 타입 커밋으로 근거를 남길 것.
     → 최적해가 bound에 붙는 경우(active constraint)를 반드시 감지해서 플래그.

[tests/test_fitting.py]
  - test_identity(): α=1, β=0으로 재구성하면 reference와 일치
  - test_recovers_known_alpha(): α_PE=0.9를 넣어 만든 곡선에서 0.9를 복원
  - test_bound_active_flagged(): bound에 붙으면 플래그가 켜짐

run.sh --mode fit 연결:
  grid 결과 parquet을 읽어 각 곡선에 fitting 수행 → fits.parquet

완료 후:
  git commit -m "feat(fitting): alpha/beta 최적화 이식"
  git commit -m "feat(objective): 34p 목적함수 (pOCV + dV/dQ + dQ/dV)"
  git tag phase4-done
```

### 완료 기준
- [ ] `test_identity` 통과 (α=1,β=0이 항등)
- [ ] 알려진 α를 복원
- [ ] bound active 감지 동작
- [ ] `--mode fit`이 grid 결과에 대해 동작

---

# Phase 5 — 축퇴 판정 · 지도

## 프롬프트

```
Phase 5: fitting 결과를 정답과 대조해 축퇴를 판정하고 지도를 만든다.

[src/scoring.py]
  ★ 03_ARCHITECTURE.md 5절 기준
  - score(truth, recovered) -> dict
      err_lli, err_lam_pe, err_lam_ne
      abs_err_max
      pe_ne_antisym : err_pe * err_ne < 0  (축퇴의 특징적 지문)
      pe_ne_gap_true vs pe_ne_gap_recovered
      degenerate : abs_err_max > TOL (기본 0.02)
      n_restarts_agree : multi-start 결과 일치 개수

  - summarize(df) -> dict
      전체 축퇴 비율
      축 별 조건부 비율 (LAM_NE가 클 때 / 작을 때 등)
      노이즈 레벨별

[src/hessian.py]
  - numerical_hessian(objective, p_opt) -> np.ndarray (4×4)
  - eigen_analysis(H) -> dict
      고윳값, 조건수, 최소 고윳값의 고유벡터
      → "α_PE와 α_NE가 같은 부호로 묶여 있는가" 확인
  - flat_direction_score : 최소 고윳값 / 최대 고윳값

[tools/plot_map.py]
  - 2D heatmap: x=LAM_PE, y=LAM_NE, color=abs_err_max
    (LLI는 슬라이스 또는 facet)
  - 축퇴 영역 경계선 표시
  - 22p 실험 조건(LAM_PE≈13%, LAM_NE≈13%, LLI≈17%)을 지도 위에 마커로 표시
    → "우리 실험 조건이 축퇴 영역 안에 있는가"를 시각적으로 답함

run.sh --mode score, --mode hessian 연결.

완료 후:
  ./run.sh --mode score --in results/grid_coarse_v1
  → degeneracy_map.parquet + figures/degeneracy_map.png

  git commit -m "feat(scoring): 축퇴 판정 및 지표"
  git commit -m "feat(hessian): 조건수 기반 flat direction 분석"
  git tag phase5-done
```

### 완료 기준
- [ ] 축퇴 비율이 숫자로 나옴
- [ ] 지도에 22p 실험 조건 위치 표시
- [ ] Hessian 최소 고윳값의 고유벡터가 α_PE·α_NE 방향인지 확인

---

# Phase 6 — 목적함수 비교 ★ (최종 산출물)

## 프롬프트

```
Phase 6: 목적함수 4종을 같은 격자에 적용해 개선 효과를 정량화한다.
이것이 이 프로젝트의 최종 답이다.

[tools/compare_objectives.py]
  - 동일 grid 결과에 대해 objectives.yaml의 4종을 각각 적용
      pocv / pocv_dvdq / pocv_dvdq_dqdv / dqdv_only
  - 각각의 축퇴 비율 산출
  - 비교표 생성:

      | objective        | 축퇴 비율 | 평균 |err| | PE-NE 상쇄 비율 |
      |------------------|----------|-----------|----------------|
      | pocv             |   62%    |   8.1%p   |      71%       |
      | pocv_dvdq        |   41%    |   5.3%p   |      58%       |
      | pocv_dvdq_dqdv   |   18%    |   2.2%p   |      23%       |
      | dqdv_only        |   ...    |    ...    |      ...       |

  - 같은 지도를 4장 나란히 그려 시각 비교

[가중치 최적화]
  - --w-dqdv 0:2:0.25 로 sweep
  - 축퇴 비율이 최소가 되는 w 조합 탐색
  - 결과를 configs/objectives_optimized.yaml로 저장
  - "가중치를 임의로 튜닝한 것 아니냐"는 질문에 대한 근거가 됨

[docs/RESULTS.md 자동 생성]
  - 실행 조건 요약
  - 비교표
  - 핵심 결론 3줄
  - 22p 실험 조건의 축퇴 여부 판정

완료 후:
  ./run.sh --mode all --config configs/grid_fine.yaml --nproc 32 --out results/final_v1

  git commit -m "feat(compare): 목적함수 4종 축퇴 비율 비교"
  git commit -m "docs(results): 최종 결과 보고서"
  git tag phase6-done
  git checkout main && git merge phase6/objectives
```

### 완료 기준
- [ ] 목적함수 4종 비교표 완성
- [ ] "축퇴 X% → Y%" 문장이 숫자로 채워짐
- [ ] 22p 실험 조건의 축퇴 여부에 답이 나옴
- [ ] `docs/RESULTS.md` 자동 생성

---

# Phase 7 — GPU 시도 (선택 · 실패 허용)

## 프롬프트

```
Phase 7: GPU 경로를 시도한다. 실패해도 무방하며, 실패 사유를 기록하는 것이 목적이다.
03_ARCHITECTURE.md 6절 "GPU 현실론"을 먼저 읽어라.

단계적으로:

[7-1] JAX 변환 가능성 타진
  model.convert_to_format = "jax" 가 composite phases DFN에서 동작하는가?
  → 실패하면 즉시 docs/GPU_NOTES.md에 예외 메시지와 함께 기록하고 7-2로.

[7-2] 모델 하향 시도
  DFN → SPMe로 낮추고 JAX 변환 재시도.
  성공하면 DFN 결과와 SPMe 결과의 곡선 차이를 정량화 (얼마나 손실되는가).
  이 차이가 크면 GPU 경로 자체가 부적합하다는 결론.

[7-3] vmap 배치
  성공 시 jax.vmap으로 파라미터 축 벡터화.
  배치 크기 [1, 10, 100, 1000]에서 처리량 측정.
  CPU 병렬(Phase 3) 대비 속도 비교표 작성.

[7-4] 자동미분 Hessian
  JAX가 동작하면 jax.hessian으로 해석적 Hessian 계산.
  Phase 5의 수치 Hessian과 비교 — 축퇴 진단의 정확도 향상 여부.

[docs/GPU_NOTES.md]
  각 단계의 성공/실패, 예외 메시지, 벤치마크 수치를 모두 기록.
  실패 기록도 가치가 있다 — 다음 사람이 같은 시도를 반복하지 않게 한다.

run.sh --backend gpu 는 이 단계에서 실제 구현.
동작하지 않으면 명확한 경고와 함께 CPU로 fallback.

완료 후:
  git commit -m "feat(gpu): JAX 백엔드 시도 및 벤치마크"
  또는
  git commit -m "docs(gpu): JAX 경로 실패 기록 및 사유"
  git tag phase7-done
```

### 완료 기준
- [ ] `docs/GPU_NOTES.md`에 각 단계 결과 기록
- [ ] 성공/실패 무관하게 `--backend gpu`가 안전하게 동작 (fallback 포함)

---

# 부록 A — 한 번에 넘길 때의 통합 프롬프트

여러 Phase를 한 번에 진행시키려면:

```
docs/ 아래 00~04 md를 모두 읽고, 업로드된 발표 PDF의 21·22·32·33·34p를 확인하라.
degrade_mode_sim_me.py를 분석하되, 02_CODE_AUDIT.md에 이미 정리된 문제점을 참고하라.

Phase 0부터 Phase 3까지 순차 진행한다.
각 Phase 종료 시 pytest 통과를 확인하고, 04_PROMPTS.md의 git 규칙대로 커밋·태그하라.

절대 원칙:
1. 물리 파라미터를 임의로 바꾸지 않는다. 변경 시 physics 커밋 + 근거 명시.
2. 하드코딩된 완방상태값(36.7, 3446.3, 58439.9)을 사용하지 않는다. 자동 산출한다.
3. 모드↔프로토콜 매핑을 보존한다.
4. 각 Phase 완료 기준 체크리스트를 만족하지 못하면 다음으로 넘어가지 않는다.
5. GPU를 무리하게 적용하지 않는다. CPU 병렬이 1차 목표다.

Phase 3까지 끝나면 멈추고, coarse 격자 실행 결과와 함께 보고하라.
```

---

# 부록 B — 진행 상황 추적

```markdown
## Progress

- [ ] Phase 0 — 스캐폴딩 · 환경          `phase0-done`
- [ ] Phase 1 — 코어 리팩터링             `phase1-done`
- [ ] Phase 2 — 모드 중첩 · 32p 재현      `phase2-done`
- [ ] Phase 3 — 조합 격자 · 병렬화        `phase3-done`
- [ ] Phase 4 — Fitting 이식              `phase4-done`
- [ ] Phase 5 — 축퇴 판정 · 지도          `phase5-done`
- [ ] Phase 6 — 목적함수 비교             `phase6-done`
- [ ] Phase 7 — GPU 시도 (선택)           `phase7-done`
```

---

# 부록 C — 자주 막히는 지점

| 증상 | 원인 | 대응 |
|---|---|---|
| `initialization()` 안 했더니 결과가 이상 | 전역 param 오염 | Phase 1에서 이미 해결됨. 순수 함수 확인 |
| LAM 조합 시 porosity > 1 | 중첩 시 porosity 누적 | `porosity + vf·i ≤ 1` 검증 추가 |
| 완방상태 농도가 음수/발산 | `/(1−i)` 에서 i→1 | i 상한을 0.9로 제한 |
| fitting이 항상 bound에 붙음 | 33p bound가 α≥1.0 | lb 확장 검토, physics 커밋 |
| grid 실행 중 메모리 폭발 | 모든 Solution을 메모리에 보관 | chunk 저장, Solution은 곡선만 추출 후 폐기 |
| 조건마다 모델 재빌드로 느림 | discretisation 반복 | 워커별 모델 1회 빌드 후 재사용 |
| parquet 파일이 수 GB | 시계열 전체 저장 | 정규화 격자 300점으로 리샘플 후 저장 |
