# `tests/` — MATLAB 쪽 파일을 **실제로 돌려 본** 검사

    ./run_all.sh            # 전부 (Octave 가 있으면 5종, 없으면 Python 2종)

2026-09-10 이전까지 `dd_eval.m` · `dd_verify.m` · `dd_shims/` 는 **한 번도
실행된 적이 없었다.** 블록 균형만 프로그램으로 셌을 뿐이고, 사용자 기계에서
`dd_verify('check')` 가 돈 것이 유일한 실행 증거였다. 그 상태로 사용자에게
`dd_eval` 을 돌리게 하면 구문 오류 하나에 왕복 한 번이 날아간다.

이 디렉터리는 그 왕복을 여기서 미리 태우기 위한 것이다. `apt-get install
octave` 로 GNU Octave 8.4 를 넣고, 규진팀 함수 자리에 합성 대역품을 끼워
`dd_eval.m` 을 끝까지 돌린다.

## 무엇을 증명하나 / 무엇을 증명 못 하나

**증명한다** (2026-09-10 실측, `run_all.sh` 재현 가능)

| # | 검사 | 결과 |
|---|---|---|
| 1 | 구문 — Octave 파서가 네 파일을 읽는가 | `dd_eval.m` · `dd_verify.m` · shim 둘 전부 통과 |
| 2 | `quantile` shim ≡ Python `matlab_quantile` | 88 케이스, 최대 \|Δ\| **0.000e+00** |
| 2 | `quantile` shim ≡ Octave 내장 `quantile`(method 5) | 최대 \|Δ\| **8.9e-16** |
| 2 | `sgolayfilt` shim ≡ Python `sgolay`(scipy, `mode='interp'`) | 8 케이스, 최대 \|Δ\| **5.9e-13**, 가장자리 **4.4e-15** |
| 2 | `findpeaks` shim ≡ scipy `find_peaks(prominence=…)` | 8 벡터 × 5 문턱 = **40/40 조합 일치** |
| 3 | `dd_eval.m` 배관 ≡ Python 전사본 | 7 조합, 앵커 16 + 8행 × 4열, 최대 상대차 **7.8e-14** |
| 4 | `--compare` 이분 판정이 갈린 단계를 짚는가 | 앵커 16개 · rmse 4열을 하나씩 어긋뜨려 전부 올바른 단계 지목 (26/26) |
| 5 | Python `verify eval` 배관 | 5 상태 × 2 반쪽전지 소스 × 8 Si 소스 전부 적재 |

②의 Octave 내장 `quantile` 일치가 중요하다. Octave 의 method 5 는 MATLAB 의
정의((i−0.5)/n plotting position)와 같으므로, 이건 **제3자 구현에 대한 확인**
이지 우리끼리의 자기일관성이 아니다.

②의 `sgolayfilt` 가장자리 일치는 `model.py` 가 `# ≠MATLAB` 으로 표시해 두고
"완전히 같은 수는 아닐 수 있다" 고 적어 둔 바로 그 자리를 닫는다 — **shim 과
scipy 사이에서는** 닫힌다.

②의 `findpeaks` 는 그렇지 않다. Octave core 에 `findpeaks` 가 없어서
(`exist('findpeaks')` → 0) **제3의 독립 구현이 없고**, shim↔scipy 2자 대조다.
그래서 이 검사가 허수아비가 아님을 **변이(mutation)로** 따로 확인했다:

| 일부러 넣은 오류 | 결과 |
|---|---|
| 평탄 꼭대기를 가운데 대신 **왼쪽 끝**으로 | 40/40 → **35/40**, `plateau` 5 조합이 정확히 지목됨 |
| prominence base 를 `max(좌,우)` → `min(좌,우)` | 40/40 → **32/40**, `noisy`·`dqdv` 에서 봉우리가 과다 검출 |

③·⑤에는 **degenerate fixture 방지**가 따로 들어 있다. dQ/dV 항은 보간 범위에
5 점을 못 넣으면 원본 규약대로 `1e6` 을 내는데, 그러면 **양쪽 다 1e6 이라
상대오차 0 으로 통과한다** — 경로를 아예 안 탔는데 초록불이 뜬다.
`check_e2e.py` 의 `assert_dqdv_alive` 가 (a) 1e6 이 섞였는지 (b) `n_peaks` 가
0 인지 (c) 가중과 무가중이 전부 같은지 (d) 모든 p 에서 값이 같은지를 본다.
변이 3종으로 전부 잡히는 것을 확인했다.

같은 감사를 ⑤(Python 스모크)에 넣었더니 **처음부터 FAIL 이 났다** — 합성 풀셀
전압이 매끈한 단조 곡선이라 dQ/dV 에 봉우리가 하나도 없었고(`n_peaks=0`),
피크 가중이 전부 1 이라 가중 경로가 무가중과 구별되지 않았다. 흑연 스테이지를
닮은 완만한 계단 둘을 넣어 고쳤다(`n_peaks=2`). 이 저장소에서 fixture 가
진실을 가린 것이 이번이 두 번째다 — 첫 번째는 합성 Si/Gr 이 정규화 뒤 겹쳐
γ 가 아무 효과도 없던 건.

> **2026-09-10 갱신 — ①은 실물로 닫혔다.** 사용자 기계(MATLAB R2026a,
> Windows)에서 `dd_eval` 이 **네 조합 전부 정상 실행**됐다.
>
> 그때 앵커만으로(적합 없이) 같이 확인된 것:
>
> | 검사 | 결과 |
> |---|---|
> | `dv_lo`/`dv_hi`/`dv_n` — capacity 가 0~1 정규화라 **데이터 무관 구조상수** | MATLAB `0.14929859719438879` vs Python `…76`, 상대차 **1.9e-16**; `dv_n` 350 일치 |
> | `E_NE`·`dv_NE` 가 문헌 Si 소스에만 의존하는가 | Li 3조합(반쪽전지·상태가 다름)이 **완전 동일**, Kunz 만 다름 |
> | 방향 규약 `E_PE(0.5) − E_NE(0.5,0.25)` | 3.7623 / 3.7630 / 3.7517 V — 2.5~4.5 V 안 |
> | `c_cell` | pristine 74.671 · 300_0009 63.720 — 기준과 **정확히** 일치 |
> | shim/툴박스 분리 (`-end`) | `sgolayfilt=dd_shims`, `quantile=matlab` — 의도대로 |
>
> 아직 안 닫힌 것은 **`rmse_pocv`/`rmse_dvdq` 대조**다. 원자료가 있는 기계에서
> `verify eval --compare` 를 돌려야 한다.

**증명 못 한다 — 이건 계속 열려 있다**

- ~~**MATLAB 이 이 파일들을 돌리는가.**~~ → 위 갱신 참조. `dd_eval` 은 돈다.
  `dd_verify` 의 `dump`/`profile`/`scalenoise` 는 툴박스가 없어 여전히 미실행이고,
  그 경로의 구문은 Octave 8.4 로만 확인됐다.
- ~~**MathWorks 의 진짜 `sgolayfilt`·`quantile` 과 같은가.**~~ → **쟀다**
  (2026-09-10, `FINDINGS.md` §1-7). 사용자 기계에 툴박스가 설치된 뒤 같은
  데이터를 툴박스판·shim판으로 각각 돌려 앵커 40 + rmse 64 를 댔다.
  `quantile` 은 **완전히 같고**(16 값), `sgolayfilt` 는 도함수에서
  **상대 1.33e-13** 갈린다. 그 차이는 파일이 담는 자리수보다 3200 배 작아
  rmse 64 값은 전부 같게 찍혔다. 이 컨테이너에는 여전히 툴박스가 없다.
- ~~**MathWorks 의 진짜 `findpeaks` 와 같은가.**~~ → **실제 데이터에서는
  같았다** (2026-09-10, §1-7). `n_peaks`·`w_peak_sum`·`w_peak_max` 12 값이
  툴박스판과 shim판에서 완전 동일했다 — 봉우리 위치가 하나라도 달랐으면
  가중 합이 갈렸을 것이다.
- **`findpeaks` 의 평탄 꼭대기(plateau) 규약은 여전히 미검증.** 실측 dQ/dV 에
  완전 동수 구간이 없어서 그 분기를 안 탔다. 우리가 scipy 쪽(가운데 인덱스)에
  맞춰 두고 "MathWorks 와 다를 수 있다" 고 표시한 바로 그 자리다.
- **dQ/dV 두 열이 그들 식과 같은가.** `compute_dqdv_rmse_blend` 와
  `build_peak_weights_local` 은 그들 `electrode_balancing_blend.m` 의 로컬
  함수라 밖에서 못 부른다. 그래서 그 둘만은 **옮겨 적었고**, 여기 일치는
  「우리 전사 ↔ 우리 포팅」이지 「그들 코드 ↔ 우리 포팅」이 아니다.
- **`unique(v_smooth)` 가 점을 버리는 분기.** 합성 fixture 에서는
  `dq_nuniq_p1` 이 500(전부 생존)이라 그 분기가 한 번도 안 탔다. 실제
  데이터에서만 드러난다.
- **규진팀 모델이 맞는가.** ③은 그들 함수 자리에 **합성 대역품**을 끼운다
  (`synth/README_SYNTH.md`). 재는 것은 배관(인덱싱·마스크·파라미터 변환·
  RMSE 식)이지 모델이 아니다.
- **MATLAB `pchip`/`interp1` 이 scipy 와 같은 수를 내는가.** ③은 그 자리를
  일부러 우회한다. 이건 사용자 기계의 실제 실행으로만 알 수 있고, 그것이
  `dd_eval` → `verify eval --compare` 절차가 존재하는 이유다.

## 파일

| 파일 | 무엇 |
|---|---|
| `run_all.sh` | 전부 실행. Octave 없으면 4·5만 |
| `gen_shim_cases.py` · `run_shims.m` · `check_shims.py` | ② shim 3자 대조 |
| `gen_synth_data.py` · `synth/` · `oct_stubs/` · `mirror_dd_eval.py` · `check_e2e.py` · `run_e2e.sh` | ③ 배관 e2e |
| `test_compare_bisect.py` | ④ 이분 판정 |
| `gen_synth_xlsx.py` · `test_py_smoke.py` | ⑤ Python 스모크 |

### `oct_stubs/` 와 `dd_shims/` 는 목적이 다르다 — 헷갈리면 안 된다

| | `matlab/dd_shims/` | `matlab/tests/oct_stubs/` |
|---|---|---|
| 어디서 쓰나 | **사용자 기계 (MATLAB)** | **이 컨테이너 (Octave)만** |
| 왜 | 툴박스가 없어서 `sgolayfilt`·`quantile` 이 없다 | Octave 에 `contains`·`readmatrix`·`readtable` 이 없다 |
| 사용자 폴더에 복사? | **한다** (`addpath('dd_shims')`) | **절대 안 한다** — MATLAB 엔 원래 있고, 복사하면 내장함수를 가린다 |

## 알려진 차이 — 1 ULP

③에서 `dq_hi` 가 Octave `4.1435370741482966` vs numpy `4.1435370741482958`
로 갈린다 (상대차 2.1e-16). `linspace` 의 마지막 자리 반올림 차이이고 배관
버그가 아니다. 그래서 `check_e2e.py` 는 바이트가 아니라 **상대오차 1e-12** 로
본다.

이 잡음이 분위수 창 마스크를 흔들 수 있나 — **없다.** `differential` 은
`capacity_uniform2` 를 항상 `linspace(…, 500)` 으로 만들고 `quantile` 은 **그
격자 자신**의 분위수다. p=0.05·0.15·0.85·0.95 에서 `p·500` 이 정수라 경계는
언제나 격자점 **정확히 중간**에 떨어진다 (여유 = 격자간격의 0.5배 ≈ 1e-3
상대). 데이터와 무관한 기하학이고, 1e-16 잡음과는 13자리 차이다.
실측: 모든 e2e 조합에서 `dv_n` = 350 으로 동일.
