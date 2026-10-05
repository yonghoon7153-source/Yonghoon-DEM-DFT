# REIL C6 — 판 · 환경 고정 측정 (2026-10-05 · 이 컨테이너)

승인: `docs/REIL_PREREQUISITES_STATUS_20261004.md` §8-2 (사용자 "ㄱ ㄱ"). 결과 절: 같은 문서 §10 (§9 는 부속 C 재검토 회신 접수가 먼저 썼다).
만든 것: `scripts/reil_c6_profile.py emit` (버리는 venv 의 python) · 대조: 같은 스크립트의 `check` · 변이 증명:
`scripts/reil_c6_mutation_proof.py` · 규칙 테스트: `tests/test_reil_c6_profile.py`.

**이것이 아닌 것.** Sobol 시작점 배열의 정식 봉인이 아니다 — 판에 결속하는 **식별** 기록이다. 정식 봉인은 부속 B §2-1 의 "맞춤 전
(P0 뒤 · 첫 지역 실행 전)" 에 같은 판에서 다시 만들어 아래 sha256 과 대조한다 (다르면 멈춤). REIL `LFP_Data.xlsx` · `results/*.pkl` ·
노트북 열기 0 · P0 0 · 맞춤 0 · 비용 측정 0 · max_q 에 기대는 배열 0 · label seed 배열 0 · E3b 등록 0 · 운영 환경 · 저장소 설치 0
(venv 는 스크래치패드 안).

## 파일

`MANIFEST.json` 이 아래 10 개 파일의 sha256 정본이다. `MANIFEST.json` 자체의 sha256 =
`e4adba0fed22e51de37d98067a623e2e3e9575cc9e1ea039a3a88363e2378e9f`.

| 파일 | 내용 | sha256 앞 8 자리 |
|---|---|---|
| `REIL_C6.lock.txt` | venv site-packages 의 배포판 30 개 `이름==판` + 각 RECORD 파일의 sha256 · 설치 파일 전부를 RECORD 와 대조한 수 · python · 플랫폼 · libc 줄 · 설명된 충돌 줄 | `caef8523` |
| `PROFILE.json` | Python · 플랫폼 · 주 패키지 7 개의 판 · NumPy · SciPy 빌드 의존성 (BLAS · LAPACK) · COBYQA 구현 판 | `c9449c28` |
| `COBYQA_OPTIONS.json` | 부속 A §3-1 옵션 8 개의 계획값 · 문서화 여부 · 형 · 설명 전문 · 구현 파일 4 개의 sha256 · 합성 이차 함수 호출 결과 · `accepted` | `0317d11b` |
| `SOBOL_PHASE_A.json` | Sobol 호출문 · seed 인자 이름 · 시그니처 · 상자 둘 · 배열 6 개의 sha256 (raw float64 LE · npy) · 옛 `seed=` 대조 | `88765472` |
| `sobol_unit_seed0.npy` · `sobol_unit_seed1.npy` | 단위 입방체 64 × 4 (float64 LE · `allow_pickle=False`) | `e8ca4cc0` · `870eec2c` |
| `sobol_A0_their_box_seed0.npy` · `…seed1.npy` | A0 = 그들 상자 (v2 §1-1) 로 늘린 배열 | `916ac373` · `0e8dacca` |
| `sobol_A1_A2_wide_box_seed0.npy` · `…seed1.npy` | A1 · A2 = 넓힌 상자 (v2 §4-1) 로 늘린 배열 | `2e7ba141` · `72a33726` |
| `README.md` · `C6_RUN.log` | 사람용 기록 — **봉인 밖** (MANIFEST 에 없고 `check` 도 대조하지 않는다 · 시각 · 커널 판이 들어 결정적이지 않다) | — |

## 결과 요약 (정본은 위 파일 — 여기 숫자는 사본)

- **판.** CPython 3.11.15 · Linux x86_64 · glibc 2.39. numpy 2.4.6 · scipy 1.17.1 · pandas 3.0.5 · openpyxl 3.1.5 · matplotlib 3.11.2 (승인대로
  C lock `degradation-degeneracy/requirements-validation-C.lock.txt` 와 같게 고정) · seaborn 0.13.2 · pymoo 0.6.2 (pip 가 고른 판). 의존성까지
  30 배포판 (pip 24.0 · setuptools 79.0.1 은 venv 기본 포함). C lock 과 판이 다른 전이 의존성 셋 — six 1.17.0 (C lock 1.16.0) · fonttools
  4.66.1 (4.66.0) · pyparsing 3.3.3 (3.1.1). 승인 §8-2 가 의존성 판을 고정하지 않았으므로 기록만 한다.
- **BLAS · LAPACK.** NumPy = scipy-openblas 0.3.31.188.0 (ILP64 · `USE64BITINT`), SciPy = scipy-openblas 0.3.30 (LP64). 한 프로세스에
  OpenBLAS 빌드가 둘 들어온다.
- **RECORD 대조.** 설치 파일 verified 7187 · unhashed 5301 · 불일치 1. 그 1 은 **설명된 충돌**: pymoo → alive-progress 3.3.0 → about-time
  4.2.1 사슬의 두 wheel 이 둘 다 venv 꼭대기 `../../../LICENSE` 를 RECORD 에 적고, 나중에 깔린 alive-progress 의 바이트가 디스크에 있다.
  첫 emit 은 이 불일치로 멈췄고 (fail-closed), 규칙 하나만 좁게 풀었다 — site-packages **밖** 경로이고 다른 배포판의 RECORD 가 디스크
  바이트와 같을 때만 기록 후 통과, 그 밖의 불일치는 전부 봉인 거부.
- **COBYQA.** SciPy 1.17.1 안의 cobyqa 1.1.3 (`scipy._lib.cobyqa`). 옵션 8 개 모두 `show_options` 에 문서화 · 합성 이차 함수 (REIL 자료
  아님) 호출 성공 · 경고 0 · 알 수 없는 옵션 경고 0 · `f_target = −∞` 수용 → `accepted = true`.
  뜻 대조 (기록만 — 부속 A §3-1 의 값은 그대로이고, 바꾸면 새 등록): `scale=True` 이고 상자가 유한하면 변수를 [−1, 1] 로 옮긴 공간에서
  돌므로 `initial_tr_radius = 1.0` · `final_tr_radius = 1e-6` 도 **그 공간의** 반경이다. 원래 단위로는 좌표마다 반경 × 그 좌표의 상자 반폭
  (A0 상자 반폭 0.25 · 0.3 · 0.2475 · 0.5 · 넓힌 상자 0.6 · 0.6 · 1.0 · 1.0). `final_tr_radius` 를 주면 `minimize` 의 `tol` 을 덮어쓴다
  (설명 전문). 설명이 권하는 초기 반경은 "변수의 최대 예상 변화의 1/10 정도" 이고, 1.0 은 스케일 공간 폭 2 의 절반이다.
- **Sobol.** SciPy 1.17.1 의 seed 인자 이름은 `rng` (시그니처에 옛 `seed=None` 도 남아 있다). **같은 정수를 `seed=` 로 주면 다른 배열이
  나온다 — 경고 없이** (seed 0 · 1 둘 다). `rng=<정수>` 는 `rng=np.random.default_rng(<정수>)` 와 같은 배열이다. → 시작점 배열은
  `SOBOL_PHASE_A.json` 의 `call` 그대로 `rng=` 로만 만든다 (맞춤 전 재생성도). 부속 A §3-1 이 경고한 "판에 따라 seed 인자 이름과 생성
  배열이 다를 수 있다" 의 이 판에서의 실측이다.

## 대조 · 변이 증명

- `<venv>/bin/python bms-balancing/scripts/reil_c6_profile.py check bms-balancing/reil_c6_20261005` → `check OK` (rc 0). 대조 = MANIFEST
  해시 + 같은 venv 에서 새로 emit 한 파일과의 바이트 비교 (MANIFEST 자체 포함 · 봉인 쪽에만 있는 파일도 다름 · 사람용 기록 둘만 제외).
  emit 은 설치 파일 전부의 RECORD 대조를 다시 하므로 venv 가 바뀌면 여기서 멈춘다.
- `<venv>/bin/python bms-balancing/scripts/reil_c6_mutation_proof.py bms-balancing/reil_c6_20261005 <없는 작업 경로>` → 12 경우 ALL PASS
  (사람용 기록만 더한 사본 rc 0 · 변이 11 개 rc 1 — lock 판 · 충돌 줄 · Sobol 배열 1 비트 · 옛 seed 사실 · COBYQA 설명 · 구현 해시 · BLAS 판 ·
  MANIFEST 해시만 · MANIFEST 항목 삭제 · 파일 삭제 + MANIFEST · 여분 파일. 대부분은 MANIFEST 까지 맞춘 일관된 위조다).
- venv 는 스크래치패드의 버리는 것이라 컨테이너와 함께 사라진다. 같은 판의 venv 재구축과 정식 봉인 대조는 그 단계 (부속 B §2-1 의 맞춤 전)
  의 승인 범위다.

경위 (첫 emit 실패 · 버린 둘째 emit · 스크립트 보강 · 미리보기 · 최종 emit) 와 시각은 `C6_RUN.log`.
