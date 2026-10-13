---
source_url: https://github.com/catnap042/ocvfit
ingested: 2026-10-13
sha256: c5457fc3331bdffc5d31d165eb6ef8921e9f31e66087c953eeb826719f814bae
---

수집 목적: 경쟁 도구 · 판정 대상 (일일 브리핑 ② · ④ 축) — 사용자 지시 2026-10-13 "ocvfit 실험 E1 뭔가 할만하면 해보고" (entity 의 제안 실험 E1 · 버리는 venv · 운영 환경 · 저장소 산출물 · RUN_SCOPE 0).

---

# ocvfit 0.1.0 (HEAD 2b898cc6) 를 우리 PyBaMM 합성 truth 에 적용 — E1 (식별 판정 · 72 평가) + 대조군 E1-ctrl (자기 모델 합성 · 36 평가) (2026-10-13 실측)

## 조건 · 격리

- ocvfit: `catnap042/ocvfit` HEAD `2b898cc62293cb35dfe82f351fe9b0103c643d28` (0.1.0 · 릴리스 태그 없음) 의 얕은 clone 을 스크래치패드의 버리는 venv 에 `pip install --no-deps` ·
  Python 3.11.17 · numpy 2.4.6 · scipy 1.17.1 · pandas 3.0.6 · pyarrow 26.0.0 · pybamm 26.8.0.0 · pybammsolvers 0.9.1 · casadi 3.7.2 (pybamm 은 기준 곡선 재생성에만).
  운영 환경 · 저장소 · 등록부에는 설치 · 쓰기 0 (읽기만: 아래 parquet · `git archive` 사본).
- 곡선: `degradation-degeneracy/artifacts/grid_curves_v4/curves.parquet` (sha256 `b69dc7bee0bb2e32aba73b6ace91255d964bceb41f9361886de7275bf48aa8b8` — 스크립트가 시작 때 대조) ·
  noise 0 · DFN 0.05 C 방전 (과전압 포함) · `x_norm` 0 = 충전 끝 → 방전 Ah = `x_norm · q_mah / 1000`. BOL = pristine (`03ccd8aefe0b`).
- 반쪽전지 OCP: `git archive f27006370 degradation-degeneracy/src degradation-degeneracy/configs` 사본에서 `compute_halfcell_from_ocp(load_config("configs/base.yaml"))` →
  npz sha256 `9f606a6f2cce6ff589ead366489decf0edc695a5d1ebd92b582b9941f204ac39` — **2026-10-05 ampworks 실험의 npz 와 바이트 동일** (재생성 · 대조).
  PE = 화학량론 그대로 · NE = 흑연 + Si 평형 분배 (탈리튬화 가지) 의 유효 곡선 하나.
- 우리 truth 의 정의 대조 (코드 읽기): LAM_NE 는 두 음극 상의 부피분율에 같은 `(1 − lam_ne)` 를 곱한다 (`src/modes.py` LAM_NE 블록) → 유효 음극 곡선의 모양은 그대로 ·
  LLI 는 세 저장소 농도에 `(1 − lli)` → 전체 리튬이 정확히 `lli` 만큼 준다 = ocvfit 의 `n_li` (두 전극 리튬의 합) 비와 같은 정의 · LAM 은 모두 `de` 형 (죽은 활물질은 비어 있었음).
- 판정 모델: `CapacityModel(PE, NE)` — **`v_full` 없음 (x100 자유)**. 우리 곡선에는 '완충 휴지 전압' 이 없다 (방전 시작 전압은 과전압을 포함).
- 설계 (E1 본): 사례 12 × 창 3 × 기준 다리 2 = 72 평가.
  - 사례 (LLI, LAM_PE, LAM_NE): (0.04,0,0) · (0.10,0,0) · (0.16,0,0) · (0,0.04,0) · (0,0.06,0) — LAM_PE 단독은 0.06 이 격자 최대 · (0,0,0.04) · (0,0,0.10) · (0,0,0.16) ·
    (0.10,0.10,0.10) · (0.06,0.04,0.10) · (0.12,0.02,0.04) · (0.04,0.10,0.02).
  - 창: W0 전 구간 · W1 V ≥ 3.50 V (깊은 방전 끝을 자름) · W2 V ≤ 3.95 V (위쪽을 자르고 q 를 창 시작에서 0 으로). BOL · aged 같은 전압 창.
  - 기준 다리: R0 그대로 · R1 PE 기준에 +10 mV (판정 쪽 기준에만 · truth 불변 — 우리 `ocpbias` PE 다리와 같은 축 · 우리 22p 정본이 '첫 파탄' 으로 본 크기).
- 사례마다: `fit_capacity` (기본 설정) → `degradation_modes` → 모드별 프로파일 구간 (`mode_interval` 과 같은 식 · BOL 프로파일은 묶음마다 한 번 계산해 재사용 — 첫 사례에서
  `mode_interval` 원 함수와 대조해 차이를 기록) → `bias_budget` (README 예와 같이 n_draws 8 · n_starts 3 · seed 1 · 기본 ±3 mV · 2 mV) → 최종 구간 = 프로파일 ± 예산 ·
  `is_identifiable` (반폭 ≤ 1 %p) · 참값을 덮는가 · 격차 LAM_PE − LAM_NE 의 점값과 두 최종 구간을 독립으로 묶은 구간.
- 대조군 E1-ctrl: **같은 화학 · 같은 창 · 같은 판정 절차**를 ocvfit **자기 모델로 합성한** 곡선에 적용 — `v_full` 4.18 V 고정 CapacityModel · 하한 2.6 V · 300 점 · 잡음 1 mV ·
  BOL 매개 = E1 W0 · R0 BOL 적합값 (Q_pe · Q_ne · n_li · R) · aged = 그 값에 참값 비율을 곱함 → 참값이 ocvfit 정의 그대로 · 기준 다리 R0 만 · 36 평가.
  목적: E1 본의 '식별 불가' 가 정보 부족 때문인지, 모델 불일치 (SOC 따라 변하는 과전압 ↔ 상수 R) 때문인지 가른다.

- 결과 JSON (이 파일 옆 · 바이트 그대로): `2026-10-13-ocvfit-on-synthetic-truth.results.json` sha256 `d4b845b53e7c74bd425fe14b349426c05b8d3756eca2d964f7ca7ea62fadf569` (164,872 B) · `2026-10-13-ocvfit-on-synthetic-truth.ctrl.results.json` sha256 `133f90296273b1ef41191789594dc47fb6af6c867d25cdd98650fc0f88f5bda8` (70,240 B).

## 탐침 — 한 사례 시간 · 동작 (timing_probe.py 출력 원문 · 설계 전에 1 회)

```text
# 재실행 (2026-10-13 · 설계 전 첫 실행과 같은 코드 · 시간 값은 실행마다 다르다)
params ['Q_pe', 'Q_ne', 'n_li', 'R', 'x100']
fit s 3.95 2.74 rmse mV 9.905 12.74
bol {'Q_pe': 8.46800904927293, 'Q_ne': 6.387648914512144, 'n_li': 8.016353723368175, 'R': -0.008237648681840782, 'x100': 0.8821010810894087}
aged {'Q_pe': 8.457277133210088, 'Q_ne': 6.46878799589676, 'n_li': 7.191262593208781, 'R': -0.004152890353511334, 'x100': 0.7640714409889958}
modes {'LLI': 0.10292598837725953, 'LAM_PE': 0.0012673482043293882, 'LAM_NE': -0.012702495467506791, 'dn_li_Ah': 0.825091130159394, 'dQ_pe_Ah': 0.010731916062841407, 'dQ_ne_Ah': -0.08113908138461579}
intervals s 37.83 {'LLI': (0.029488571201755076, 0.17781916685739985), 'LAM_PE': (-0.17401517850433623, 0.16583607966888347), 'LAM_NE': (-0.08683247167897257, 0.04838573844812)}
rho 0.957035095963846 thr 174.9105447128997
budget s 15.54 {'LLI': 0.004888716496743495, 'LAM_PE': 0.008467491748790912, 'LAM_NE': 0.04411120265366075}
```

## E1 실행 로그 (run.log 원문)

```text
start 2026-10-13T01:28:29Z
{"w": "W1_V_ge_3.50", "leg": "R0_exact", "truth": {"LLI": 0.04, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": -0.0019, "LAM_PE": -0.0021, "LAM_NE": -0.008}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.9}
{"w": "W1_V_ge_3.50", "leg": "R0_exact", "truth": {"LLI": 0.1, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": -0.002, "LAM_PE": -0.0026, "LAM_NE": -0.0094}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.7}
{"w": "W1_V_ge_3.50", "leg": "R0_exact", "truth": {"LLI": 0.16, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": 0.0027, "LAM_PE": -0.0056, "LAM_NE": 0.0109}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.0}
{"w": "W1_V_ge_3.50", "leg": "R0_exact", "truth": {"LLI": 0, "LAM_PE": 0.04, "LAM_NE": 0}, "err": {"LLI": 0.0052, "LAM_PE": -0.0053, "LAM_NE": 0.0282}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.7}
{"w": "W1_V_ge_3.50", "leg": "R0_exact", "truth": {"LLI": 0, "LAM_PE": 0.06, "LAM_NE": 0}, "err": {"LLI": 0.0054, "LAM_PE": -0.0053, "LAM_NE": 0.0268}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.6}
{"w": "W1_V_ge_3.50", "leg": "R0_exact", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.04}, "err": {"LLI": 0.0029, "LAM_PE": -0.0054, "LAM_NE": 0.0195}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.4}
{"w": "W1_V_ge_3.50", "leg": "R0_exact", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.1}, "err": {"LLI": 0.0014, "LAM_PE": -0.0057, "LAM_NE": 0.0139}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.3}
{"w": "W1_V_ge_3.50", "leg": "R0_exact", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.16}, "err": {"LLI": 0.0006, "LAM_PE": -0.0047, "LAM_NE": 0.0121}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.0}
{"w": "W1_V_ge_3.50", "leg": "R0_exact", "truth": {"LLI": 0.1, "LAM_PE": 0.1, "LAM_NE": 0.1}, "err": {"LLI": -0.0003, "LAM_PE": 0.0003, "LAM_NE": 0.0002}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 3.0}
{"w": "W1_V_ge_3.50", "leg": "R0_exact", "truth": {"LLI": 0.06, "LAM_PE": 0.04, "LAM_NE": 0.1}, "err": {"LLI": 0.0028, "LAM_PE": -0.0053, "LAM_NE": 0.0202}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.6}
{"w": "W1_V_ge_3.50", "leg": "R0_exact", "truth": {"LLI": 0.12, "LAM_PE": 0.02, "LAM_NE": 0.04}, "err": {"LLI": -0.0021, "LAM_PE": -0.0025, "LAM_NE": -0.0096}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.7}
{"w": "W1_V_ge_3.50", "leg": "R0_exact", "truth": {"LLI": 0.04, "LAM_PE": 0.1, "LAM_NE": 0.02}, "err": {"LLI": 0.0069, "LAM_PE": -0.0049, "LAM_NE": 0.0335}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.5}
{"w": "W1_V_ge_3.50", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.04, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": -0.0019, "LAM_PE": -0.0021, "LAM_NE": -0.008}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 3.5}
{"w": "W1_V_ge_3.50", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.1, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": -0.002, "LAM_PE": -0.0026, "LAM_NE": -0.0094}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 3.2}
{"w": "W1_V_ge_3.50", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.16, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": 0.0027, "LAM_PE": -0.0056, "LAM_NE": 0.0109}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.7}
{"w": "W1_V_ge_3.50", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0, "LAM_PE": 0.04, "LAM_NE": 0}, "err": {"LLI": 0.0052, "LAM_PE": -0.0053, "LAM_NE": 0.0282}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.3}
{"w": "W1_V_ge_3.50", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0, "LAM_PE": 0.06, "LAM_NE": 0}, "err": {"LLI": 0.0054, "LAM_PE": -0.0053, "LAM_NE": 0.0268}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.1}
{"w": "W1_V_ge_3.50", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.04}, "err": {"LLI": 0.0029, "LAM_PE": -0.0054, "LAM_NE": 0.0195}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.0}
{"w": "W1_V_ge_3.50", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.1}, "err": {"LLI": 0.0014, "LAM_PE": -0.0057, "LAM_NE": 0.0139}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.4}
{"w": "W1_V_ge_3.50", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.16}, "err": {"LLI": 0.0006, "LAM_PE": -0.0047, "LAM_NE": 0.0121}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.0}
{"w": "W1_V_ge_3.50", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.1, "LAM_PE": 0.1, "LAM_NE": 0.1}, "err": {"LLI": -0.0003, "LAM_PE": 0.0003, "LAM_NE": 0.0002}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.9}
{"w": "W1_V_ge_3.50", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.06, "LAM_PE": 0.04, "LAM_NE": 0.1}, "err": {"LLI": 0.0028, "LAM_PE": -0.0053, "LAM_NE": 0.0202}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.3}
{"w": "W1_V_ge_3.50", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.12, "LAM_PE": 0.02, "LAM_NE": 0.04}, "err": {"LLI": -0.0021, "LAM_PE": -0.0025, "LAM_NE": -0.0096}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 3.2}
{"w": "W1_V_ge_3.50", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.04, "LAM_PE": 0.1, "LAM_NE": 0.02}, "err": {"LLI": 0.0069, "LAM_PE": -0.0049, "LAM_NE": 0.0335}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.5}
{"w": "W0_full", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.04, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": 0.0, "LAM_PE": -0.001, "LAM_NE": -0.0058}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 98.7}
{"w": "W0_full", "leg": "R0_exact", "truth": {"LLI": 0.04, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": 0.0, "LAM_PE": -0.0009, "LAM_NE": -0.0055}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 100.3}
{"w": "W0_full", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.1, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": 0.0029, "LAM_PE": 0.0012, "LAM_NE": -0.013}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 27.4}
{"w": "W0_full", "leg": "R0_exact", "truth": {"LLI": 0.1, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": 0.0029, "LAM_PE": 0.0013, "LAM_NE": -0.0127}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 27.7}
{"w": "W0_full", "leg": "R0_exact", "truth": {"LLI": 0.16, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": 0.0063, "LAM_PE": -0.0052, "LAM_NE": -0.0561}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 31.8}
{"w": "W0_full", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.16, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": 0.0063, "LAM_PE": -0.0053, "LAM_NE": -0.0564}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 33.5}
{"w": "W2_V_le_3.95", "leg": "R0_exact", "truth": {"LLI": 0.04, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": 0.0104, "LAM_PE": 0.0497, "LAM_NE": 0.027}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 203.3}
{"w": "W0_full", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0, "LAM_PE": 0.04, "LAM_NE": 0}, "err": {"LLI": -0.004, "LAM_PE": -0.0119, "LAM_NE": 0.0045}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 81.7}
{"w": "W0_full", "leg": "R0_exact", "truth": {"LLI": 0, "LAM_PE": 0.04, "LAM_NE": 0}, "err": {"LLI": -0.0035, "LAM_PE": -0.0112, "LAM_NE": 0.0071}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 82.6}
{"w": "W2_V_le_3.95", "leg": "R0_exact", "truth": {"LLI": 0.1, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": 0.0357, "LAM_PE": -0.1615, "LAM_NE": 0.0898}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 49.0}
{"w": "W2_V_le_3.95", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.04, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": 0.0047, "LAM_PE": 0.0442, "LAM_NE": 0.0159}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 198.7}
{"w": "W0_full", "leg": "R0_exact", "truth": {"LLI": 0, "LAM_PE": 0.06, "LAM_NE": 0}, "err": {"LLI": -0.006, "LAM_PE": -0.021, "LAM_NE": 0.0007}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 51.8}
{"w": "W0_full", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0, "LAM_PE": 0.06, "LAM_NE": 0}, "err": {"LLI": -0.006, "LAM_PE": -0.021, "LAM_NE": 0.0004}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 53.8}
{"w": "W2_V_le_3.95", "leg": "R0_exact", "truth": {"LLI": 0.16, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": 0.0765, "LAM_PE": -0.0582, "LAM_NE": 0.1385}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": false}, "s": 37.1}
{"w": "W2_V_le_3.95", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.1, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": 0.0294, "LAM_PE": -0.1535, "LAM_NE": 0.0829}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 52.7}
{"w": "W0_full", "leg": "R0_exact", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.04}, "err": {"LLI": 0.0031, "LAM_PE": 0.0048, "LAM_NE": 0.0003}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 55.7}
{"w": "W0_full", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.04}, "err": {"LLI": 0.0035, "LAM_PE": 0.0053, "LAM_NE": 0.0021}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 57.8}
{"w": "W2_V_le_3.95", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.16, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": 0.0668, "LAM_PE": -0.0606, "LAM_NE": 0.126}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": false}, "s": 43.4}
{"w": "W0_full", "leg": "R0_exact", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.1}, "err": {"LLI": -0.0025, "LAM_PE": 0.0112, "LAM_NE": -0.0165}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 45.8}
{"w": "W0_full", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.1}, "err": {"LLI": -0.0025, "LAM_PE": 0.0112, "LAM_NE": -0.0166}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 47.0}
{"w": "W2_V_le_3.95", "leg": "R0_exact", "truth": {"LLI": 0, "LAM_PE": 0.04, "LAM_NE": 0}, "err": {"LLI": -0.0059, "LAM_PE": -0.0483, "LAM_NE": 0.0248}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 96.1}
{"w": "W0_full", "leg": "R0_exact", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.16}, "err": {"LLI": 0.0104, "LAM_PE": 0.0279, "LAM_NE": 0.0154}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 56.0}
{"w": "W0_full", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.16}, "err": {"LLI": 0.0098, "LAM_PE": 0.0262, "LAM_NE": 0.0121}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 57.8}
{"w": "W2_V_le_3.95", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0, "LAM_PE": 0.04, "LAM_NE": 0}, "err": {"LLI": -0.0067, "LAM_PE": -0.0492, "LAM_NE": 0.0352}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 90.2}
{"w": "W2_V_le_3.95", "leg": "R0_exact", "truth": {"LLI": 0, "LAM_PE": 0.06, "LAM_NE": 0}, "err": {"LLI": -0.0051, "LAM_PE": -0.0668, "LAM_NE": 0.0423}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 80.8}
{"w": "W0_full", "leg": "R0_exact", "truth": {"LLI": 0.1, "LAM_PE": 0.1, "LAM_NE": 0.1}, "err": {"LLI": 0.0008, "LAM_PE": 0.0023, "LAM_NE": -0.0033}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 58.0}
{"w": "W0_full", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.1, "LAM_PE": 0.1, "LAM_NE": 0.1}, "err": {"LLI": 0.0035, "LAM_PE": 0.0067, "LAM_NE": 0.0156}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 54.8}
{"w": "W2_V_le_3.95", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0, "LAM_PE": 0.06, "LAM_NE": 0}, "err": {"LLI": -0.0091, "LAM_PE": -0.0704, "LAM_NE": 0.0373}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 76.8}
{"w": "W2_V_le_3.95", "leg": "R0_exact", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.04}, "err": {"LLI": 0.0027, "LAM_PE": 0.002, "LAM_NE": -0.0179}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 91.0}
{"w": "W0_full", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.06, "LAM_PE": 0.04, "LAM_NE": 0.1}, "err": {"LLI": 0.0043, "LAM_PE": 0.0052, "LAM_NE": -0.0055}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 67.8}
{"w": "W0_full", "leg": "R0_exact", "truth": {"LLI": 0.06, "LAM_PE": 0.04, "LAM_NE": 0.1}, "err": {"LLI": 0.0058, "LAM_PE": 0.008, "LAM_NE": 0.001}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 71.8}
{"w": "W0_full", "leg": "R0_exact", "truth": {"LLI": 0.12, "LAM_PE": 0.02, "LAM_NE": 0.04}, "err": {"LLI": 0.0033, "LAM_PE": 0.0006, "LAM_NE": -0.0158}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 26.2}
{"w": "W0_full", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.12, "LAM_PE": 0.02, "LAM_NE": 0.04}, "err": {"LLI": 0.0033, "LAM_PE": 0.0005, "LAM_NE": -0.0161}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 27.6}
{"w": "W2_V_le_3.95", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.04}, "err": {"LLI": -0.0067, "LAM_PE": -0.006, "LAM_NE": -0.0293}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 85.9}
{"w": "W2_V_le_3.95", "leg": "R0_exact", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.1}, "err": {"LLI": 0.0088, "LAM_PE": -0.0076, "LAM_NE": 0.0173}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 64.4}
{"w": "W0_full", "leg": "R0_exact", "truth": {"LLI": 0.04, "LAM_PE": 0.1, "LAM_NE": 0.02}, "err": {"LLI": -0.0068, "LAM_PE": -0.0225, "LAM_NE": -0.003}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 51.6}
{"w": "W0_full", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.04, "LAM_PE": 0.1, "LAM_NE": 0.02}, "err": {"LLI": -0.0068, "LAM_PE": -0.0225, "LAM_NE": -0.0033}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 53.7}
{"w": "W2_V_le_3.95", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.1}, "err": {"LLI": 0.005, "LAM_PE": -0.0111, "LAM_NE": 0.0133}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 65.8}
{"w": "W2_V_le_3.95", "leg": "R0_exact", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.16}, "err": {"LLI": 0.0147, "LAM_PE": -0.0242, "LAM_NE": 0.0506}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 75.7}
{"w": "W2_V_le_3.95", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.16}, "err": {"LLI": 0.0108, "LAM_PE": -0.0279, "LAM_NE": 0.0467}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 76.3}
{"w": "W2_V_le_3.95", "leg": "R0_exact", "truth": {"LLI": 0.1, "LAM_PE": 0.1, "LAM_NE": 0.1}, "err": {"LLI": 0.0071, "LAM_PE": 0.0072, "LAM_NE": 0.0024}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 92.2}
{"w": "W2_V_le_3.95", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.1, "LAM_PE": 0.1, "LAM_NE": 0.1}, "err": {"LLI": -0.0023, "LAM_PE": -0.0018, "LAM_NE": -0.0032}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 86.5}
{"w": "W2_V_le_3.95", "leg": "R0_exact", "truth": {"LLI": 0.06, "LAM_PE": 0.04, "LAM_NE": 0.1}, "err": {"LLI": 0.0085, "LAM_PE": 0.0272, "LAM_NE": -0.0027}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 88.8}
{"w": "W2_V_le_3.95", "leg": "R0_exact", "truth": {"LLI": 0.12, "LAM_PE": 0.02, "LAM_NE": 0.04}, "err": {"LLI": 0.0358, "LAM_PE": -0.1567, "LAM_NE": 0.0814}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 46.8}
{"w": "W2_V_le_3.95", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.06, "LAM_PE": 0.04, "LAM_NE": 0.1}, "err": {"LLI": 0.0058, "LAM_PE": 0.0245, "LAM_NE": -0.0132}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 88.3}
{"w": "W2_V_le_3.95", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.12, "LAM_PE": 0.02, "LAM_NE": 0.04}, "err": {"LLI": 0.03, "LAM_PE": -0.148, "LAM_NE": 0.0754}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 49.6}
{"w": "W2_V_le_3.95", "leg": "R0_exact", "truth": {"LLI": 0.04, "LAM_PE": 0.1, "LAM_NE": 0.02}, "err": {"LLI": -0.0053, "LAM_PE": -0.0665, "LAM_NE": 0.0409}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 76.7}
{"w": "W2_V_le_3.95", "leg": "R1_PE_plus10mV", "truth": {"LLI": 0.04, "LAM_PE": 0.1, "LAM_NE": 0.02}, "err": {"LLI": -0.0092, "LAM_PE": -0.0699, "LAM_NE": 0.0359}, "flags": {"LLI": false, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 74.9}
{"wall_s": 1108.4, "n_groups": 6}
rc=0 end 2026-10-13T01:47:05Z
```

## E1 요약 (summarize_e1.py 출력 원문)

```text
identity: {'ocvfit': '0.1.0', 'numpy': '2.4.6', 'scipy': '1.17.1', 'pandas': '3.0.6', 'parquet': '/home/user/Yonghoon-DEM-DFT/degradation-degeneracy/artifacts/grid_curves_v4/curves.parquet', 'parquet_sha256': 'b69dc7bee0bb2e32aba73b6ace91255d964bceb41f9361886de7275bf48aa8b8', 'ref_npz_sha256': '9f606a6f2cce6ff589ead366489decf0edc695a5d1ebd92b582b9941f204ac39'}
design: {"cases": [[0.04, 0, 0], [0.1, 0, 0], [0.16, 0, 0], [0, 0.04, 0], [0, 0.06, 0], [0, 0, 0.04], [0, 0, 0.1], [0, 0, 0.16], [0.1, 0.1, 0.1], [0.06, 0.04, 0.1], [0.12, 0.02, 0.04], [0.04, 0.1, 0.02]], "windows": {"W0_full": [null, null], "W1_V_ge_3.50": [3.5, null], "W2_V_le_3.95": [null, 3.95]}, "legs": {"R0_exact": 0.0, "R1_PE_plus10mV": 10.0}, "budget": {"n_draws": 8, "n_starts": 3, "seed": 1}, "model": "CapacityModel(PE, NE) without v_full (x100 free)", "identifiable_threshold": 0.01}
wall_s: 1108.4

== R0_exact · W0_full · BOL n=300 rmse=9.91 mV · x100=0.8821 · R=-8.24 mV · ρ(BOL, n_li)=0.980 · group 697 s
   truth (LLI,PE,NE)      rmse |    LLI err  hw  id cov | LAM_PE err  hw  id cov | LAM_NE err  hw  id cov |   gap err  naive-hw cov
   (0.04,0.00,0.00)      11.03 |  +0.00   9.0 n Y |  -0.09  18.9 n Y |  -0.55   9.3 n Y |   +0.46    28.1   Y
   (0.10,0.00,0.00)      12.74 |  +0.29   7.9 n Y |  +0.13  17.8 n Y |  -1.27  11.2 n Y |   +1.40    29.0   Y
   (0.16,0.00,0.00)      14.66 |  +0.63   8.5 n Y |  -0.52  24.1 n Y |  -5.61  11.2 n Y |   +5.09    35.3   Y
   (0.00,0.04,0.00)       8.54 |  -0.35   8.3 n Y |  -1.12  15.6 n Y |  +0.71  15.7 n Y |   -1.83    31.3   Y
   (0.00,0.06,0.00)       8.54 |  -0.60   9.1 n Y |  -2.10  15.6 n Y |  +0.07  24.6 n Y |   -2.17    40.2   Y
   (0.00,0.00,0.04)      10.12 |  +0.31   9.0 n Y |  +0.48  17.5 n Y |  +0.03   8.4 n Y |   +0.45    25.9   Y
   (0.00,0.00,0.10)      10.63 |  -0.25   9.3 n Y |  +1.12  17.4 n Y |  -1.65  10.4 n Y |   +2.77    27.8   Y
   (0.00,0.00,0.16)      11.33 |  +1.04   8.8 n Y |  +2.79  19.4 n Y |  +1.54  10.1 n Y |   +1.25    29.5   Y
   (0.10,0.10,0.10)      10.53 |  +0.08   8.3 n Y |  +0.23  17.4 n Y |  -0.33   8.3 n Y |   +0.56    25.7   Y
   (0.06,0.04,0.10)      10.85 |  +0.58   9.0 n Y |  +0.80  17.7 n Y |  +0.10   9.1 n Y |   +0.70    26.8   Y
   (0.12,0.02,0.04)      13.32 |  +0.33   7.7 n Y |  +0.06  17.6 n Y |  -1.58  10.5 n Y |   +1.64    28.1   Y
   (0.04,0.10,0.02)       8.60 |  -0.68   8.4 n Y |  -2.25  14.1 n Y |  -0.30  23.7 n Y |   -1.95    37.8   Y
   mode_interval 재사용 식 대조 (첫 사례): [0.0]

== R0_exact · W1_V_ge_3.50 · BOL n=210 rmse=1.47 mV · x100=0.9581 · R=1.16 mV · ρ(BOL, n_li)=0.376 · group 33 s
   truth (LLI,PE,NE)      rmse |    LLI err  hw  id cov | LAM_PE err  hw  id cov | LAM_NE err  hw  id cov |   gap err  naive-hw cov
   (0.04,0.00,0.00)       0.84 |  -0.19   1.3 n Y |  -0.21   2.0 n Y |  -0.80   8.4 n Y |   +0.59    10.5   Y
   (0.10,0.00,0.00)       0.80 |  -0.20   1.3 n Y |  -0.26   2.3 n Y |  -0.94   7.7 n Y |   +0.68    10.0   Y
   (0.16,0.00,0.00)       1.19 |  +0.27   1.5 n Y |  -0.56   3.0 n Y |  +1.09   9.3 n Y |   -1.65    12.3   Y
   (0.00,0.04,0.00)       1.41 |  +0.52   1.6 n Y |  -0.53   1.7 n Y |  +2.82   7.3 n Y |   -3.35     9.0   Y
   (0.00,0.06,0.00)       1.42 |  +0.54   1.7 n Y |  -0.53   1.8 n Y |  +2.68   7.5 n Y |   -3.21     9.2   Y
   (0.00,0.00,0.04)       1.35 |  +0.29   1.6 n Y |  -0.54   1.7 n Y |  +1.95   7.2 n Y |   -2.49     8.9   Y
   (0.00,0.00,0.10)       1.18 |  +0.14   1.7 n Y |  -0.57   1.9 n Y |  +1.39   6.9 n Y |   -1.96     8.8   Y
   (0.00,0.00,0.16)       1.00 |  +0.06   1.9 n Y |  -0.47   2.2 n Y |  +1.21   6.3 n Y |   -1.68     8.5   Y
   (0.10,0.10,0.10)       1.50 |  -0.03   1.2 n Y |  +0.03   1.3 n Y |  +0.02   5.6 n Y |   +0.00     7.0   Y
   (0.06,0.04,0.10)       1.33 |  +0.28   1.5 n Y |  -0.53   1.6 n Y |  +2.02   6.7 n Y |   -2.56     8.3   Y
   (0.12,0.02,0.04)       0.80 |  -0.21   1.3 n Y |  -0.25   2.2 n Y |  -0.96   7.5 n Y |   +0.72     9.7   Y
   (0.04,0.10,0.02)       1.43 |  +0.69   1.9 n Y |  -0.49   1.7 n Y |  +3.35   7.2 n Y |   -3.84     8.9   Y
   mode_interval 재사용 식 대조 (첫 사례): [0.0]

== R0_exact · W2_V_le_3.95 · BOL n=231 rmse=7.48 mV · x100=0.6358 · R=-54.50 mV · ρ(BOL, n_li)=0.957 · group 1059 s
   truth (LLI,PE,NE)      rmse |    LLI err  hw  id cov | LAM_PE err  hw  id cov | LAM_NE err  hw  id cov |   gap err  naive-hw cov
   (0.04,0.00,0.00)       8.61 |  +1.04   8.5 n Y |  +4.97  10.9 n Y |  +2.70  20.7 n Y |   +2.27    31.6   Y
   (0.10,0.00,0.00)      11.44 |  +3.57  10.9 n Y | -16.15  26.7 n Y |  +8.98  10.8 n Y |  -25.13    37.5   Y
   (0.16,0.00,0.00)       8.43 |  +7.65   8.5 n Y |  -5.82  17.0 n Y | +13.85   9.9 n n |  -19.67    26.9   Y
   (0.00,0.04,0.00)       8.02 |  -0.59   7.1 n Y |  -4.83  10.8 n Y |  +2.48  14.9 n Y |   -7.31    25.7   Y
   (0.00,0.06,0.00)       8.77 |  -0.51   7.1 n Y |  -6.68  10.0 n Y |  +4.23  13.1 n Y |  -10.91    23.1   Y
   (0.00,0.00,0.04)       8.17 |  +0.27   8.6 n Y |  +0.20  11.2 n Y |  -1.79  22.0 n Y |   +1.99    33.3   Y
   (0.00,0.00,0.10)       9.86 |  +0.88   9.3 n Y |  -0.76  15.1 n Y |  +1.73  13.7 n Y |   -2.49    28.7   Y
   (0.00,0.00,0.16)      10.98 |  +1.47   9.3 n Y |  -2.42  16.4 n Y |  +5.06   9.0 n Y |   -7.48    25.5   Y
   (0.10,0.10,0.10)       8.12 |  +0.71   5.8 n Y |  +0.72   8.4 n Y |  +0.24  11.2 n Y |   +0.48    19.6   Y
   (0.06,0.04,0.10)       8.04 |  +0.85   5.1 n Y |  +2.72   7.2 n Y |  -0.27  11.1 n Y |   +2.99    18.3   Y
   (0.12,0.02,0.04)      11.93 |  +3.58  10.6 n Y | -15.67  25.8 n Y |  +8.14  10.5 n Y |  -23.81    36.3   Y
   (0.04,0.10,0.02)       9.03 |  -0.53   6.6 n Y |  -6.65   9.6 n Y |  +4.09  12.6 n Y |  -10.73    22.2   Y
   mode_interval 재사용 식 대조 (첫 사례): [0.0]

== R1_PE_plus10mV · W0_full · BOL n=300 rmse=9.90 mV · x100=0.8823 · R=1.79 mV · ρ(BOL, n_li)=0.980 · group 700 s
   truth (LLI,PE,NE)      rmse |    LLI err  hw  id cov | LAM_PE err  hw  id cov | LAM_NE err  hw  id cov |   gap err  naive-hw cov
   (0.04,0.00,0.00)      11.03 |  +0.00   9.0 n Y |  -0.10  18.9 n Y |  -0.58   9.2 n Y |   +0.48    28.1   Y
   (0.10,0.00,0.00)      12.74 |  +0.29   7.9 n Y |  +0.12  17.8 n Y |  -1.30  11.1 n Y |   +1.42    29.0   Y
   (0.16,0.00,0.00)      14.66 |  +0.63   8.5 n Y |  -0.53  24.1 n Y |  -5.64  11.1 n Y |   +5.11    35.2   Y
   (0.00,0.04,0.00)       8.55 |  -0.40   8.4 n Y |  -1.19  15.4 n Y |  +0.45  14.9 n Y |   -1.64    30.3   Y
   (0.00,0.06,0.00)       8.54 |  -0.60   9.1 n Y |  -2.10  15.6 n Y |  +0.04  24.5 n Y |   -2.14    40.1   Y
   (0.00,0.00,0.04)      10.12 |  +0.35   9.0 n Y |  +0.53  17.5 n Y |  +0.21   7.7 n Y |   +0.32    25.2   Y
   (0.00,0.00,0.10)      10.63 |  -0.25   9.3 n Y |  +1.12  17.4 n Y |  -1.66  10.5 n Y |   +2.78    27.9   Y
   (0.00,0.00,0.16)      11.33 |  +0.98   8.7 n Y |  +2.62  19.2 n Y |  +1.21   9.8 n Y |   +1.41    29.0   Y
   (0.10,0.10,0.10)      10.60 |  +0.35   8.4 n Y |  +0.67  16.9 n Y |  +1.56   9.6 n Y |   -0.89    26.5   Y
   (0.06,0.04,0.10)      10.86 |  +0.43   8.8 n Y |  +0.52  17.4 n Y |  -0.55   8.3 n Y |   +1.07    25.8   Y
   (0.12,0.02,0.04)      13.32 |  +0.33   7.7 n Y |  +0.05  17.6 n Y |  -1.61  10.5 n Y |   +1.67    28.1   Y
   (0.04,0.10,0.02)       8.60 |  -0.68   8.4 n Y |  -2.25  14.3 n Y |  -0.33  23.1 n Y |   -1.92    37.3   Y
   mode_interval 재사용 식 대조 (첫 사례): [0.0]

== R1_PE_plus10mV · W1_V_ge_3.50 · BOL n=210 rmse=1.47 mV · x100=0.9581 · R=11.16 mV · ρ(BOL, n_li)=0.376 · group 33 s
   truth (LLI,PE,NE)      rmse |    LLI err  hw  id cov | LAM_PE err  hw  id cov | LAM_NE err  hw  id cov |   gap err  naive-hw cov
   (0.04,0.00,0.00)       0.84 |  -0.19   1.3 n Y |  -0.21   2.0 n Y |  -0.80   8.4 n Y |   +0.59    10.5   Y
   (0.10,0.00,0.00)       0.80 |  -0.20   1.3 n Y |  -0.26   2.3 n Y |  -0.94   7.7 n Y |   +0.68    10.0   Y
   (0.16,0.00,0.00)       1.19 |  +0.27   1.5 n Y |  -0.56   3.0 n Y |  +1.09   9.3 n Y |   -1.65    12.3   Y
   (0.00,0.04,0.00)       1.41 |  +0.52   1.6 n Y |  -0.53   1.7 n Y |  +2.82   7.3 n Y |   -3.35     9.0   Y
   (0.00,0.06,0.00)       1.42 |  +0.54   1.7 n Y |  -0.53   1.8 n Y |  +2.68   7.5 n Y |   -3.21     9.2   Y
   (0.00,0.00,0.04)       1.35 |  +0.29   1.6 n Y |  -0.54   1.7 n Y |  +1.95   7.2 n Y |   -2.49     8.9   Y
   (0.00,0.00,0.10)       1.18 |  +0.14   1.7 n Y |  -0.57   1.9 n Y |  +1.39   6.9 n Y |   -1.96     8.8   Y
   (0.00,0.00,0.16)       1.00 |  +0.06   1.9 n Y |  -0.47   2.2 n Y |  +1.21   6.3 n Y |   -1.68     8.5   Y
   (0.10,0.10,0.10)       1.50 |  -0.03   1.2 n Y |  +0.03   1.3 n Y |  +0.02   5.6 n Y |   +0.00     7.0   Y
   (0.06,0.04,0.10)       1.33 |  +0.28   1.5 n Y |  -0.53   1.6 n Y |  +2.02   6.7 n Y |   -2.56     8.3   Y
   (0.12,0.02,0.04)       0.80 |  -0.21   1.3 n Y |  -0.25   2.2 n Y |  -0.96   7.5 n Y |   +0.72     9.7   Y
   (0.04,0.10,0.02)       1.43 |  +0.69   1.9 n Y |  -0.49   1.7 n Y |  +3.35   7.2 n Y |   -3.84     8.9   Y
   mode_interval 재사용 식 대조 (첫 사례): [0.0]

== R1_PE_plus10mV · W2_V_le_3.95 · BOL n=231 rmse=7.52 mV · x100=0.6392 · R=-42.17 mV · ρ(BOL, n_li)=0.959 · group 1043 s
   truth (LLI,PE,NE)      rmse |    LLI err  hw  id cov | LAM_PE err  hw  id cov | LAM_NE err  hw  id cov |   gap err  naive-hw cov
   (0.04,0.00,0.00)       8.61 |  +0.47   6.3 n Y |  +4.42  10.2 n Y |  +1.59  13.5 n Y |   +2.83    23.7   Y
   (0.10,0.00,0.00)      11.76 |  +2.94  11.5 n Y | -15.35  28.4 n Y |  +8.29  11.4 n Y |  -23.64    39.8   Y
   (0.16,0.00,0.00)       9.01 |  +6.68   9.2 n Y |  -6.06  19.5 n Y | +12.60  10.6 n n |  -18.66    30.2   Y
   (0.00,0.04,0.00)       8.04 |  -0.67   6.5 n Y |  -4.92  10.5 n Y |  +3.52  13.3 n Y |   -8.44    23.9   Y
   (0.00,0.06,0.00)       8.77 |  -0.91   7.1 n Y |  -7.04  10.5 n Y |  +3.73  13.0 n Y |  -10.76    23.6   Y
   (0.00,0.00,0.04)       8.15 |  -0.67   9.0 n Y |  -0.60  11.4 n Y |  -2.93  22.6 n Y |   +2.33    33.9   Y
   (0.00,0.00,0.10)       9.86 |  +0.50   9.2 n Y |  -1.11  15.7 n Y |  +1.33  13.5 n Y |   -2.43    29.2   Y
   (0.00,0.00,0.16)      10.98 |  +1.08   9.4 n Y |  -2.79  17.1 n Y |  +4.67   9.0 n Y |   -7.45    26.1   Y
   (0.10,0.10,0.10)       7.98 |  -0.23   8.2 n Y |  -0.18  10.2 n Y |  -0.32  20.0 n Y |   +0.14    30.2   Y
   (0.06,0.04,0.10)       8.12 |  +0.58   5.0 n Y |  +2.45   7.9 n Y |  -1.32   8.4 n Y |   +3.77    16.3   Y
   (0.12,0.02,0.04)      12.29 |  +3.00  11.2 n Y | -14.80  27.8 n Y |  +7.54  11.0 n Y |  -22.34    38.8   Y
   (0.04,0.10,0.02)       9.03 |  -0.92   6.7 n Y |  -6.99  10.1 n Y |  +3.59  12.5 n Y |  -10.58    22.6   Y
   mode_interval 재사용 식 대조 (첫 사례): [0.0]

== 묶음별 집계 (사례 12 · 오류 사례 제외)
   leg             window        mode     id/n  cov/n  pcov/n  med|err|  max|err|  med hw  med budget  med ρ
   R0_exact        W0_full       LLI      0/12  12/12   12/12      0.34      1.04     8.6        0.56  0.964
   R0_exact        W0_full       LAM_PE   0/12  12/12   12/12      0.66      2.79    17.6        0.96  0.964
   R0_exact        W0_full       LAM_NE   0/12  12/12   12/12      0.63      5.61    10.4        4.11  0.964
   R0_exact        W0_full       GAP            12/12              1.52      5.09    28.6
   R0_exact        W1_V_ge_3.50  LLI      0/12  12/12   12/12      0.24      0.69     1.6        0.68  0.497
   R0_exact        W1_V_ge_3.50  LAM_PE   0/12  12/12   12/12      0.51      0.57     1.8        0.81  0.497
   R0_exact        W1_V_ge_3.50  LAM_NE   0/12  12/12   12/12      1.30      3.35     7.2        3.73  0.497
   R0_exact        W1_V_ge_3.50  GAP            12/12              1.82      3.84     9.0
   R0_exact        W2_V_le_3.95  LLI      0/12  12/12   12/12      0.87      7.65     8.5        1.68  0.962
   R0_exact        W2_V_le_3.95  LAM_PE   0/12  12/12   12/12      4.90     16.15    11.0        1.61  0.962
   R0_exact        W2_V_le_3.95  LAM_NE   0/12  11/12    9/12      3.39     13.85    11.9        5.13  0.962
   R0_exact        W2_V_le_3.95  GAP            12/12              7.40     25.13    26.3
   R1_PE_plus10mV  W0_full       LLI      0/12  12/12   12/12      0.38      0.98     8.6        0.52  0.964
   R1_PE_plus10mV  W0_full       LAM_PE   0/12  12/12   12/12      0.60      2.62    17.5        0.99  0.964
   R1_PE_plus10mV  W0_full       LAM_NE   0/12  12/12   12/12      0.90      5.64    10.5        4.09  0.964
   R1_PE_plus10mV  W0_full       GAP            12/12              1.53      5.11    28.5
   R1_PE_plus10mV  W1_V_ge_3.50  LLI      0/12  12/12   12/12      0.24      0.69     1.6        0.68  0.497
   R1_PE_plus10mV  W1_V_ge_3.50  LAM_PE   0/12  12/12   12/12      0.51      0.57     1.8        0.81  0.497
   R1_PE_plus10mV  W1_V_ge_3.50  LAM_NE   0/12  12/12   12/12      1.30      3.35     7.2        3.73  0.497
   R1_PE_plus10mV  W1_V_ge_3.50  GAP            12/12              1.82      3.84     9.0
   R1_PE_plus10mV  W2_V_le_3.95  LLI      0/12  12/12   12/12      0.79      6.68     8.6        1.74  0.962
   R1_PE_plus10mV  W2_V_le_3.95  LAM_PE   0/12  12/12   12/12      4.67     15.35    11.0        2.16  0.962
   R1_PE_plus10mV  W2_V_le_3.95  LAM_NE   0/12  11/12   10/12      3.56     12.60    12.7        5.83  0.962
   R1_PE_plus10mV  W2_V_le_3.95  GAP            12/12              7.95     23.64    27.7

== '식별 가능' 인데 참값을 못 덮은 경우 (위험): 없음
== 실패 사례 수: 0
```

## E1-ctrl 실행 로그 (run_ctrl.log 원문)

```text
start 2026-10-13T01:47:55Z
{"w": "W1_V_ge_3.50", "truth": {"LLI": 0.04, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": -0.0014, "LAM_PE": 0.0004, "LAM_NE": -0.0042}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.0}
{"w": "W0_full", "truth": {"LLI": 0.04, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": -0.0001, "LAM_PE": -0.0001, "LAM_NE": -0.0006}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.9}
{"w": "W1_V_ge_3.50", "truth": {"LLI": 0.1, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": -0.0013, "LAM_PE": 0.0006, "LAM_NE": -0.0033}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 1.8}
{"w": "W1_V_ge_3.50", "truth": {"LLI": 0.16, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": -0.0006, "LAM_PE": -0.0012, "LAM_NE": 0.0009}, "flags": {"LLI": true, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 1.7}
{"w": "W1_V_ge_3.50", "truth": {"LLI": 0, "LAM_PE": 0.04, "LAM_NE": 0}, "err": {"LLI": -0.002, "LAM_PE": -0.0009, "LAM_NE": -0.0059}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 1.7}
{"w": "W1_V_ge_3.50", "truth": {"LLI": 0, "LAM_PE": 0.06, "LAM_NE": 0}, "err": {"LLI": -0.002, "LAM_PE": -0.001, "LAM_NE": -0.0062}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 1.8}
{"w": "W0_full", "truth": {"LLI": 0.1, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": -0.0001, "LAM_PE": 0.0001, "LAM_NE": -0.0004}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 6.4}
{"w": "W2_V_le_3.95", "truth": {"LLI": 0.04, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": -0.0003, "LAM_PE": 0.0004, "LAM_NE": -0.0012}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 8.7}
{"w": "W1_V_ge_3.50", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.04}, "err": {"LLI": -0.0027, "LAM_PE": 0.0005, "LAM_NE": -0.0075}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 1.7}
{"w": "W1_V_ge_3.50", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.1}, "err": {"LLI": -0.0023, "LAM_PE": 0.0005, "LAM_NE": -0.0055}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 1.8}
{"w": "W1_V_ge_3.50", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.16}, "err": "IndexError('index -1 is out of bounds for axis 0 with size 0')", "flags": null, "cover": null, "s": 0.0}
{"w": "W1_V_ge_3.50", "truth": {"LLI": 0.1, "LAM_PE": 0.1, "LAM_NE": 0.1}, "err": {"LLI": -0.0007, "LAM_PE": -0.0004, "LAM_NE": -0.0017}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.3}
{"w": "W0_full", "truth": {"LLI": 0.16, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": -0.0004, "LAM_PE": -0.0009, "LAM_NE": 0.0001}, "flags": {"LLI": true, "LAM_PE": false, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 6.0}
{"w": "W1_V_ge_3.50", "truth": {"LLI": 0.06, "LAM_PE": 0.04, "LAM_NE": 0.1}, "err": {"LLI": -0.0006, "LAM_PE": 0.0003, "LAM_NE": -0.001}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 1.6}
{"w": "W2_V_le_3.95", "truth": {"LLI": 0.1, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": -0.0001, "LAM_PE": 0.0003, "LAM_NE": -0.0007}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 7.5}
{"w": "W1_V_ge_3.50", "truth": {"LLI": 0.12, "LAM_PE": 0.02, "LAM_NE": 0.04}, "err": {"LLI": -0.0007, "LAM_PE": -0.0005, "LAM_NE": -0.0026}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 1.8}
{"w": "W0_full", "truth": {"LLI": 0, "LAM_PE": 0.04, "LAM_NE": 0}, "err": {"LLI": -0.0004, "LAM_PE": -0.0014, "LAM_NE": -0.0003}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 3.0}
{"w": "W1_V_ge_3.50", "truth": {"LLI": 0.04, "LAM_PE": 0.1, "LAM_NE": 0.02}, "err": {"LLI": -0.0009, "LAM_PE": 0.0, "LAM_NE": -0.0032}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 1.8}
{"w": "W0_full", "truth": {"LLI": 0, "LAM_PE": 0.06, "LAM_NE": 0}, "err": {"LLI": -0.0004, "LAM_PE": -0.0006, "LAM_NE": -0.0001}, "flags": {"LLI": true, "LAM_PE": false, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 4.1}
{"w": "W2_V_le_3.95", "truth": {"LLI": 0.16, "LAM_PE": 0, "LAM_NE": 0}, "err": {"LLI": -0.0008, "LAM_PE": -0.0017, "LAM_NE": -0.0007}, "flags": {"LLI": true, "LAM_PE": false, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 7.4}
{"w": "W0_full", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.04}, "err": {"LLI": -0.0001, "LAM_PE": -0.0002, "LAM_NE": 0.0001}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.5}
{"w": "W0_full", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.1}, "err": {"LLI": -0.0001, "LAM_PE": -0.0008, "LAM_NE": -0.0003}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.4}
{"w": "W0_full", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.16}, "err": "IndexError('index -1 is out of bounds for axis 0 with size 0')", "flags": null, "cover": null, "s": 0.0}
{"w": "W0_full", "truth": {"LLI": 0.1, "LAM_PE": 0.1, "LAM_NE": 0.1}, "err": {"LLI": -0.0003, "LAM_PE": -0.0006, "LAM_NE": -0.0007}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.3}
{"w": "W0_full", "truth": {"LLI": 0.06, "LAM_PE": 0.04, "LAM_NE": 0.1}, "err": {"LLI": -0.0002, "LAM_PE": -0.0, "LAM_NE": -0.0}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 2.5}
{"w": "W2_V_le_3.95", "truth": {"LLI": 0, "LAM_PE": 0.04, "LAM_NE": 0}, "err": {"LLI": -0.0008, "LAM_PE": -0.0027, "LAM_NE": -0.0001}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 11.7}
{"w": "W0_full", "truth": {"LLI": 0.12, "LAM_PE": 0.02, "LAM_NE": 0.04}, "err": {"LLI": -0.0001, "LAM_PE": -0.0007, "LAM_NE": 0.0}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 6.6}
{"w": "W0_full", "truth": {"LLI": 0.04, "LAM_PE": 0.1, "LAM_NE": 0.02}, "err": {"LLI": -0.0001, "LAM_PE": -0.0002, "LAM_NE": 0.0}, "flags": {"LLI": true, "LAM_PE": false, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 4.5}
{"w": "W2_V_le_3.95", "truth": {"LLI": 0, "LAM_PE": 0.06, "LAM_NE": 0}, "err": {"LLI": -0.0011, "LAM_PE": -0.0012, "LAM_NE": -0.0016}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 10.6}
{"w": "W2_V_le_3.95", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.04}, "err": {"LLI": -0.0009, "LAM_PE": -0.0012, "LAM_NE": -0.0007}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 8.8}
{"w": "W2_V_le_3.95", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.1}, "err": {"LLI": -0.0004, "LAM_PE": 0.0003, "LAM_NE": -0.0007}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 9.1}
{"w": "W2_V_le_3.95", "truth": {"LLI": 0, "LAM_PE": 0, "LAM_NE": 0.16}, "err": "IndexError('index -1 is out of bounds for axis 0 with size 0')", "flags": null, "cover": null, "s": 0.0}
{"w": "W2_V_le_3.95", "truth": {"LLI": 0.1, "LAM_PE": 0.1, "LAM_NE": 0.1}, "err": {"LLI": -0.0002, "LAM_PE": 0.0002, "LAM_NE": -0.0011}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 9.2}
{"w": "W2_V_le_3.95", "truth": {"LLI": 0.06, "LAM_PE": 0.04, "LAM_NE": 0.1}, "err": {"LLI": -0.0001, "LAM_PE": 0.001, "LAM_NE": -0.0005}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 8.9}
{"w": "W2_V_le_3.95", "truth": {"LLI": 0.12, "LAM_PE": 0.02, "LAM_NE": 0.04}, "err": {"LLI": -0.0004, "LAM_PE": -0.0007, "LAM_NE": -0.0005}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": false}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 6.8}
{"w": "W2_V_le_3.95", "truth": {"LLI": 0.04, "LAM_PE": 0.1, "LAM_NE": 0.02}, "err": {"LLI": -0.0005, "LAM_PE": -0.0005, "LAM_NE": -0.0004}, "flags": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "cover": {"LLI": true, "LAM_PE": true, "LAM_NE": true}, "s": 11.8}
{"wall_s": 102.0}
rc=0 end 2026-10-13T01:49:38Z
```

## E1-ctrl 요약 (summarize_ctrl.py 출력 원문)

```text
identity: {"ocvfit": "0.1.0", "numpy": "2.4.6", "synthesis": {"v_full": 4.18, "v_min": 2.6, "n": 300, "noise": 0.001, "bol_params_from": "E1 W0_full R0_exact BOL fit", "bol_params": {"Q_pe": 8.46800904927293, "Q_ne": 6.387648914512144, "n_li": 8.016353723368175, "R": -0.008237648681840782}}, "cases": [[0.04, 0, 0], [0.1, 0, 0], [0.16, 0, 0], [0, 0.04, 0], [0, 0.06, 0], [0, 0, 0.04], [0, 0, 0.1], [0, 0, 0.16], [0.1, 0.1, 0.1], [0.06, 0.04, 0.1], [0.12, 0.02, 0.04], [0.04, 0.1, 0.02]], "windows": {"W0_full": [null, null], "W1_V_ge_3.50": [3.5, null], "W2_V_le_3.95": [null, 3.95]}}
wall_s: 102.0

== ctrl · W0_full · BOL n=300 rmse=1.01 mV · group 44 s
   truth (LLI,PE,NE)      rmse      ρ |    LLI err  hw  id cov | LAM_PE err  hw  id cov | LAM_NE err  hw  id cov
   (0.04,0.00,0.00)       0.92 -0.160 |  -0.01   0.1 Y Y |  -0.01   0.3 Y Y |  -0.06   0.5 Y Y
   (0.10,0.00,0.00)       1.01 -0.025 |  -0.01   0.2 Y Y |  +0.01   0.8 Y Y |  -0.04   0.9 Y Y
   (0.16,0.00,0.00)       1.01 -0.085 |  -0.04   0.3 Y Y |  -0.09   1.3 n Y |  +0.01   0.9 Y Y
   (0.00,0.04,0.00)       1.00 -0.086 |  -0.04   0.1 Y Y |  -0.14   0.2 Y Y |  -0.03   0.5 Y Y
   (0.00,0.06,0.00)       0.95  0.010 |  -0.04   0.2 Y Y |  -0.06   1.0 n Y |  -0.01   0.7 Y Y
   (0.00,0.00,0.04)       1.00  0.071 |  -0.01   0.1 Y Y |  -0.02   0.3 Y Y |  +0.01   0.4 Y Y
   (0.00,0.00,0.10)       0.92 -0.023 |  -0.01   0.3 Y Y |  -0.08   0.5 Y Y |  -0.03   1.0 Y Y
   (0.00,0.00,0.16)     ERROR IndexError('index -1 is out of bounds for axis 0 with size 0')
   (0.10,0.10,0.10)       1.00 -0.077 |  -0.03   0.1 Y Y |  -0.06   0.2 Y Y |  -0.07   0.3 Y Y
   (0.06,0.04,0.10)       0.94  0.043 |  -0.02   0.1 Y Y |  -0.00   0.3 Y Y |  -0.00   0.4 Y Y
   (0.12,0.02,0.04)       0.91  0.001 |  -0.01   0.2 Y Y |  -0.07   0.7 Y Y |  +0.00   0.8 Y Y
   (0.04,0.10,0.02)       0.96  0.064 |  -0.01   0.2 Y Y |  -0.02   1.0 n Y |  +0.00   0.8 Y Y

== ctrl · W1_V_ge_3.50 · BOL n=209 rmse=0.95 mV · group 20 s
   truth (LLI,PE,NE)      rmse      ρ |    LLI err  hw  id cov | LAM_PE err  hw  id cov | LAM_NE err  hw  id cov
   (0.04,0.00,0.00)       0.94 -0.095 |  -0.14   0.5 Y Y |  +0.04   0.4 Y Y |  -0.42   1.8 n Y
   (0.10,0.00,0.00)       0.97 -0.126 |  -0.13   0.7 Y Y |  +0.06   0.9 Y Y |  -0.33   2.8 n Y
   (0.16,0.00,0.00)       1.01 -0.086 |  -0.06   0.7 Y Y |  -0.12   1.6 n Y |  +0.09   4.4 n Y
   (0.00,0.04,0.00)       0.98 -0.099 |  -0.20   0.5 Y Y |  -0.09   0.3 Y Y |  -0.59   1.5 n Y
   (0.00,0.06,0.00)       0.95 -0.032 |  -0.20   0.7 Y Y |  -0.10   0.3 Y Y |  -0.62   1.9 n Y
   (0.00,0.00,0.04)       1.00  0.038 |  -0.27   0.4 Y Y |  +0.05   0.3 Y Y |  -0.75   1.3 n Y
   (0.00,0.00,0.10)       0.87 -0.101 |  -0.23   0.8 Y Y |  +0.05   0.7 Y Y |  -0.55   2.4 n Y
   (0.00,0.00,0.16)     ERROR IndexError('index -1 is out of bounds for axis 0 with size 0')
   (0.10,0.10,0.10)       1.01 -0.180 |  -0.07   0.3 Y Y |  -0.04   0.2 Y Y |  -0.17   0.9 Y Y
   (0.06,0.04,0.10)       0.95  0.046 |  -0.06   0.3 Y Y |  +0.03   0.3 Y Y |  -0.10   1.0 n Y
   (0.12,0.02,0.04)       0.90 -0.023 |  -0.07   0.7 Y Y |  -0.05   0.8 Y Y |  -0.26   2.5 n Y
   (0.04,0.10,0.02)       0.94  0.102 |  -0.09   0.6 Y Y |  +0.00   0.3 Y Y |  -0.32   1.8 n Y

== ctrl · W2_V_le_3.95 · BOL n=227 rmse=1.04 mV · group 102 s
   truth (LLI,PE,NE)      rmse      ρ |    LLI err  hw  id cov | LAM_PE err  hw  id cov | LAM_NE err  hw  id cov
   (0.04,0.00,0.00)       0.94 -0.201 |  -0.03   0.3 Y Y |  +0.04   0.6 Y Y |  -0.12   0.8 Y Y
   (0.10,0.00,0.00)       1.01 -0.023 |  -0.01   0.5 Y Y |  +0.03   0.7 Y Y |  -0.07   1.2 n Y
   (0.16,0.00,0.00)       0.97 -0.034 |  -0.08   0.7 Y Y |  -0.17   1.2 n Y |  -0.07   1.3 n Y
   (0.00,0.04,0.00)       1.00 -0.025 |  -0.08   0.3 Y Y |  -0.27   0.5 Y Y |  -0.01   0.6 Y Y
   (0.00,0.06,0.00)       0.95 -0.016 |  -0.11   0.3 Y Y |  -0.12   0.8 Y Y |  -0.16   0.6 Y Y
   (0.00,0.00,0.04)       1.01  0.090 |  -0.09   0.2 Y Y |  -0.12   0.5 Y Y |  -0.07   0.6 Y Y
   (0.00,0.00,0.10)       0.93 -0.022 |  -0.04   0.4 Y Y |  +0.03   0.9 Y Y |  -0.07   0.5 Y Y
   (0.00,0.00,0.16)     ERROR IndexError('index -1 is out of bounds for axis 0 with size 0')
   (0.10,0.10,0.10)       1.01 -0.056 |  -0.02   0.1 Y Y |  +0.02   0.4 Y Y |  -0.11   0.4 Y Y
   (0.06,0.04,0.10)       0.97  0.012 |  -0.01   0.2 Y Y |  +0.10   0.4 Y Y |  -0.05   0.4 Y Y
   (0.12,0.02,0.04)       0.93  0.026 |  -0.04   0.4 Y Y |  -0.07   0.7 Y Y |  -0.05   1.1 n Y
   (0.04,0.10,0.02)       0.97  0.024 |  -0.05   0.3 Y Y |  -0.05   0.7 Y Y |  -0.04   0.5 Y Y

== 묶음별 집계
   window        mode     id/n  cov/n  med|err|  max|err|  med hw
   W0_full       LLI     11/11  11/11      0.01      0.04     0.2
   W0_full       LAM_PE   8/11  11/11      0.06      0.14     0.5
   W0_full       LAM_NE  11/11  11/11      0.01      0.07     0.7
   W1_V_ge_3.50  LLI     11/11  11/11      0.13      0.27     0.6
   W1_V_ge_3.50  LAM_PE  10/11  11/11      0.05      0.12     0.3
   W1_V_ge_3.50  LAM_NE   1/11  11/11      0.33      0.75     1.8
   W2_V_le_3.95  LLI     11/11  11/11      0.04      0.11     0.3
   W2_V_le_3.95  LAM_PE  10/11  11/11      0.07      0.27     0.7
   W2_V_le_3.95  LAM_NE   8/11  11/11      0.07      0.16     0.6

== '식별 가능' 인데 참값을 못 덮은 경우 (위험): 없음
== 실패 사례 수: 3
```

## 스크립트 (실행한 그대로)

### make_ref.py (sha256 `4411919f26d1def4990561db21169c59ca9fb428f9f4db39b9d79ec130cebecb`)

```python
"""반쪽전지 OCP 기준 npz 재생성 — ampworks 실험 (2026-10-05) 과 같은 코드 스냅샷 (git archive f27006370) · 같은 호출.

  사용: venv/bin/python make_ref.py <code_root/degradation-degeneracy> <out.npz>
저장소에는 쓰지 않는다 (코드 사본은 스크래치패드).
"""
import hashlib
import os
import sys

root, out = sys.argv[1], sys.argv[2]
os.chdir(root)
sys.path.insert(0, root)

import numpy as np  # noqa: E402

from src.config import load_config  # noqa: E402
from src.halfcell import compute_halfcell_from_ocp  # noqa: E402

ref = compute_halfcell_from_ocp(load_config("configs/base.yaml"))
np.savez(out, y_pe=ref.y_pe, u_pe=ref.u_pe, z_ne=ref.z_ne, u_ne=ref.u_ne)
print({"out": out, "sha256": hashlib.sha256(open(out, "rb").read()).hexdigest(),
       "y_pe": [float(ref.y_pe.min()), float(ref.y_pe.max()), int(ref.y_pe.size)],
       "z_ne": [float(ref.z_ne.min()), float(ref.z_ne.max()), int(ref.z_ne.size)]})
```

### timing_probe.py (sha256 `af397f6d37ac4d751ccc993088a45f4946ccb09bfffc12945641dac77bb87662`)

```python
"""ocvfit 시간 · 동작 탐침 (한 사례) — E1 설계용. 저장소에 쓰지 않는다.

  사용: venv/bin/python timing_probe.py <halfcell_ocp_ref.npz>
"""
import sys
import time

import numpy as np
import pandas as pd

import ocvfit as of

P = "/home/user/Yonghoon-DEM-DFT/degradation-degeneracy/artifacts/grid_curves_v4/curves.parquet"
ref = np.load(sys.argv[1])
pos = of.OCPCurve(ref["y_pe"], ref["u_pe"], name="PE")
neg = of.OCPCurve(ref["z_ne"], ref["u_ne"], name="NE")
cols = ["cond_id", "lli", "lam_pe", "lam_ne", "noise", "q_mah", "x_norm", "v_full"]
df = pd.read_parquet(P, columns=cols)


def curve(lli, pe, ne):
    c = df[(df.noise == 0) & np.isclose(df.lli, lli) & np.isclose(df.lam_pe, pe) & np.isclose(df.lam_ne, ne)]
    r = c[c.cond_id == c.iloc[0].cond_id].sort_values("x_norm")
    q = r.x_norm.to_numpy() * float(r.iloc[0].q_mah) / 1000.0
    return q, r.v_full.to_numpy()


model = of.CapacityModel(pos, neg)
print("params", model.param_names)
qb, vb = curve(0, 0, 0)
qa, va = curve(0.10, 0, 0)
t = time.time(); bol = of.fit_capacity(model, qb, vb); t_b = time.time() - t
t = time.time(); aged = of.fit_capacity(model, qa, va); t_a = time.time() - t
print("fit s", round(t_b, 2), round(t_a, 2), "rmse mV", round(1e3 * bol.rmse, 3), round(1e3 * aged.rmse, 3))
print("bol", bol.param_dict)
print("aged", aged.param_dict)
print("modes", of.degradation_modes(bol, aged))
t = time.time(); iv = {k: of.mode_interval(bol, aged, k) for k in ("LLI", "LAM_PE", "LAM_NE")}; t_i = time.time() - t
print("intervals s", round(t_i, 2), iv)
pr = of.profile_interval(aged, "n_li"); print("rho", pr.rho, "thr", pr.threshold)


def refit(positives, negative):
    m = of.CapacityModel(positives[0], negative)
    b = of.fit_capacity(m, qb, vb, n_starts=3)
    a = of.fit_capacity(m, qa, va, n_starts=3)
    return of.degradation_modes(b, a)


modes = of.degradation_modes(bol, aged)
t = time.time(); bud = of.bias_budget(refit, [pos], neg, {k: modes[k] for k in iv}, n_draws=8, seed=1); t_bb = time.time() - t
print("budget s", round(t_bb, 2), bud)
```

### e1_run.py (sha256 `7baf84724c7903278823c7f5b3b6e0f0a931bac976d9cf0f8645a02ab4c80039`)

```python
"""ocvfit E1 (2026-10-13 · 사용자 "ocvfit 실험 E1 뭔가 할만하면 해보고") — 우리 PyBaMM 합성 truth 에서 ocvfit 의 식별 판정을 잰다.

입력 (읽기만):
  곡선  degradation-degeneracy/artifacts/grid_curves_v4/curves.parquet (시작 때 sha256 대조 · noise 0 · DFN 0.05 C 방전 · 과전압 포함)
  기준  halfcell_ocp_ref.npz — git archive f27006370 의 compute_halfcell_from_ocp(base.yaml) (ampworks 실험과 같은 바이트 · sha 대조)
설계:
  사례 12 (BOL = pristine) × 창 3 (W0 전 구간 · W1 V ≥ 3.5 V · W2 V ≤ 3.95 V, q 를 창 시작에서 0 으로) × 기준 다리 2 (R0 그대로 · R1 PE 기준 +10 mV — 기준에만)
  CapacityModel(PE, NE) — v_full 없음 (x100 자유 · 우리 곡선에 '완충 휴지 전압' 이 없다)
  사례마다: fit_capacity → degradation_modes · 모드별 프로파일 구간 (ocvfit mode_interval 과 같은 식 · BOL 프로파일은 묶음마다 1 회 계산해 재사용 — 첫 사례에서 mode_interval 과 대조) ·
           bias_budget (README 예와 같이 n_draws 8 · n_starts 3 · seed 1) · 최종 구간 = 프로파일 ± 예산 · is_identifiable (반폭 ≤ 1 %p) · 참값 덮음 여부 ·
           격차 LAM_PE − LAM_NE 의 점값 · 두 최종 구간을 독립으로 묶은 구간
쓰는 곳: argv[2] (스크래치패드) 의 JSON 하나. 저장소 · 운영 환경에는 쓰지 않는다.

  사용: venv/bin/python -I e1_run.py <halfcell_ocp_ref.npz> <out_dir>
"""
import hashlib
import json
import sys
import time
import traceback
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

import ocvfit as of
from ocvfit.uncertainty import MODE_PARAMETERS

PARQ = Path("/home/user/Yonghoon-DEM-DFT/degradation-degeneracy/artifacts/grid_curves_v4/curves.parquet")
PARQ_SHA = "b69dc7bee0bb2e32aba73b6ace91255d964bceb41f9361886de7275bf48aa8b8"
REF_SHA = "9f606a6f2cce6ff589ead366489decf0edc695a5d1ebd92b582b9941f204ac39"
MODES = ("LLI", "LAM_PE", "LAM_NE")
CASES = [(0.04, 0, 0), (0.10, 0, 0), (0.16, 0, 0), (0, 0.04, 0), (0, 0.06, 0), (0, 0, 0.04), (0, 0, 0.10), (0, 0, 0.16),
         (0.10, 0.10, 0.10), (0.06, 0.04, 0.10), (0.12, 0.02, 0.04), (0.04, 0.10, 0.02)]
WINDOWS = {"W0_full": (None, None), "W1_V_ge_3.50": (3.50, None), "W2_V_le_3.95": (None, 3.95)}
LEGS = {"R0_exact": 0.0, "R1_PE_plus10mV": 10.0}

REF_PATH = Path(sys.argv[1])
OUT = Path(sys.argv[2])


def load():
    raw = PARQ.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PARQ_SHA, "곡선 파일 sha256 불일치"
    assert hashlib.sha256(REF_PATH.read_bytes()).hexdigest() == REF_SHA, "기준 npz sha256 불일치"
    df = pd.read_parquet(PARQ, columns=["cond_id", "lli", "lam_pe", "lam_ne", "lam_pe_type", "lam_ne_type", "noise", "q_mah", "x_norm", "v_full"])
    return df[df.noise == 0], np.load(REF_PATH)


def curve(df, lli, pe, ne, window):
    c = df[np.isclose(df.lli, lli) & np.isclose(df.lam_pe, pe) & np.isclose(df.lam_ne, ne)]
    cid = c.iloc[0].cond_id
    r = c[c.cond_id == cid].sort_values("x_norm")
    q = r.x_norm.to_numpy() * float(r.iloc[0].q_mah) / 1000.0         # 완충에서 방전한 Ah (x_norm 0 = 충전 끝)
    v = r.v_full.to_numpy()
    lo, hi = window
    keep = np.ones(v.size, bool)
    if lo is not None:
        keep &= v >= lo
    if hi is not None:
        keep &= v <= hi
    q, v = q[keep], v[keep]
    if hi is not None:
        q = q - q[0]                                                  # 위쪽을 자르면 측정은 창 시작에서 0 부터 센다
    return {"cond_id": str(cid), "q": q, "v": v, "q_mah": float(r.iloc[0].q_mah), "n": int(v.size),
            "types": (str(r.iloc[0].lam_pe_type), str(r.iloc[0].lam_ne_type))}


def curves_for(ref, pe_mv):
    pos = of.OCPCurve(ref["y_pe"], ref["u_pe"] + pe_mv / 1000.0, name="PE")
    neg = of.OCPCurve(ref["z_ne"], ref["u_ne"], name="NE")
    return pos, neg


def profiles(fit):
    out = {}
    for m, par in MODE_PARAMETERS.items():
        pr = of.profile_interval(fit, par)
        out[m] = {"param": par, "interval": [float(pr.interval[0]), float(pr.interval[1])], "rho": float(pr.rho), "threshold": float(pr.threshold)}
    return out


def mode_iv(pb, pa, m):
    b_lo, b_hi = pb[m]["interval"]
    a_lo, a_hi = pa[m]["interval"]
    return 1 - a_hi / b_lo, 1 - a_lo / b_hi                              # ocvfit mode_interval 과 같은 식


def group(args):
    wname, lname = args
    t0 = time.time()
    df, ref = load()
    pos, neg = curves_for(ref, LEGS[lname])
    model = of.CapacityModel(pos, neg)
    bol_c = curve(df, 0, 0, 0, WINDOWS[wname])
    bol = of.fit_capacity(model, bol_c["q"], bol_c["v"])
    pb = profiles(bol)
    rec = {"window": wname, "leg": lname, "bol": {"cond_id": bol_c["cond_id"], "n": bol_c["n"], "rmse_mV": 1e3 * float(bol.rmse),
           "params": {k: float(v) for k, v in bol.param_dict.items()}, "profiles": pb}, "cases": []}
    checked = False
    for (lli, pe, ne) in CASES:
        t1 = time.time()
        item = {"truth": {"LLI": lli, "LAM_PE": pe, "LAM_NE": ne}}
        try:
            ac = curve(df, lli, pe, ne, WINDOWS[wname])
            aged = of.fit_capacity(model, ac["q"], ac["v"])
            modes = of.degradation_modes(bol, aged)
            pa = profiles(aged)
            iv = {m: mode_iv(pb, pa, m) for m in MODES}
            if not checked:                                              # 재사용 식 = ocvfit mode_interval (한 번 대조)
                ref_iv = {m: of.mode_interval(bol, aged, m) for m in MODES}
                item["mode_interval_check_max_abs_diff"] = float(max(abs(a - b) for m in MODES for a, b in zip(iv[m], ref_iv[m])))
                checked = True

            def refit(positives, negative):
                mm = of.CapacityModel(positives[0], negative)
                b = of.fit_capacity(mm, bol_c["q"], bol_c["v"], n_starts=3)
                a = of.fit_capacity(mm, ac["q"], ac["v"], n_starts=3)
                return of.degradation_modes(b, a)

            bud = of.bias_budget(refit, [pos], neg, {m: modes[m] for m in MODES}, n_draws=8, seed=1)
            res = {}
            for m in MODES:
                lo, hi = iv[m]
                flo, fhi = lo - bud[m], hi + bud[m]
                half = 0.5 * (fhi - flo)
                t = item["truth"][m]
                res[m] = {"est": float(modes[m]), "err": float(modes[m] - t), "profile_iv": [float(lo), float(hi)], "budget": float(bud[m]),
                          "final_iv": [float(flo), float(fhi)], "half_width": float(half), "identifiable": bool(of.is_identifiable(half)),
                          "covers_truth": bool(flo <= t <= fhi), "profile_covers_truth": bool(lo <= t <= hi)}
            g_est = modes["LAM_PE"] - modes["LAM_NE"]
            g_t = pe - ne
            g_lo = res["LAM_PE"]["final_iv"][0] - res["LAM_NE"]["final_iv"][1]
            g_hi = res["LAM_PE"]["final_iv"][1] - res["LAM_NE"]["final_iv"][0]
            item.update({"cond_id": ac["cond_id"], "n": ac["n"], "types": ac["types"], "rmse_mV": 1e3 * float(aged.rmse),
                         "params": {k: float(v) for k, v in aged.param_dict.items()}, "rho": {m: pa[m]["rho"] for m in MODES},
                         "modes": res, "gap": {"est": float(g_est), "truth": float(g_t), "err": float(g_est - g_t), "naive_iv": [float(g_lo), float(g_hi)],
                                               "covers_truth": bool(g_lo <= g_t <= g_hi)}, "seconds": time.time() - t1})
        except Exception as e:                                           # 실패는 기록하고 다음 사례로 (0 이나 PASS 로 바꾸지 않는다)
            item.update({"error": repr(e), "traceback": traceback.format_exc(), "seconds": time.time() - t1})
        rec["cases"].append(item)
        print(json.dumps({"w": wname, "leg": lname, "truth": item["truth"], "err": {m: round(item["modes"][m]["err"], 4) for m in MODES} if "modes" in item else item.get("error"),
                          "flags": {m: item["modes"][m]["identifiable"] for m in MODES} if "modes" in item else None,
                          "cover": {m: item["modes"][m]["covers_truth"] for m in MODES} if "modes" in item else None, "s": round(item["seconds"], 1)}), flush=True)
    rec["seconds"] = time.time() - t0
    return rec


def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    load()                                                               # 입력 대조를 먼저 (실패면 시작하지 않는다)
    jobs = [(w, l) for l in LEGS for w in WINDOWS]
    with Pool(4) as p:
        groups = p.map(group, jobs)
    import scipy
    out = {"identity": {"ocvfit": of.__version__, "numpy": np.__version__, "scipy": scipy.__version__, "pandas": pd.__version__,
                        "parquet": str(PARQ), "parquet_sha256": PARQ_SHA, "ref_npz_sha256": REF_SHA,
                        "design": {"cases": CASES, "windows": WINDOWS, "legs": LEGS, "budget": {"n_draws": 8, "n_starts": 3, "seed": 1},
                                   "model": "CapacityModel(PE, NE) without v_full (x100 free)", "identifiable_threshold": 0.01}},
           "groups": groups, "wall_s": time.time() - t0}
    (OUT / "e1_results.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"wall_s": round(out["wall_s"], 1), "n_groups": len(groups)}))


if __name__ == "__main__":
    main()
```

### summarize_e1.py (sha256 `d24cb3564f90ca2c4ccface8de7806c457fbdcc06aa36c912b7b7c9d4e056fd2`)

```python
"""E1 결과 요약 — e1_results.json 을 읽어 표로 출력한다 (읽기만).

  사용: venv/bin/python -I summarize_e1.py <e1_results.json>
"""
import json
import sys
from statistics import median

R = json.load(open(sys.argv[1], encoding="utf-8"))
MODES = ("LLI", "LAM_PE", "LAM_NE")
pp = lambda x: 100.0 * x  # noqa: E731

print("identity:", {k: v for k, v in R["identity"].items() if k != "design"})
print("design:", json.dumps(R["identity"]["design"], ensure_ascii=False))
print("wall_s:", round(R["wall_s"], 1))
print()

danger = []
for g in R["groups"]:
    b = g["bol"]
    print(f"== {g['leg']} · {g['window']} · BOL n={b['n']} rmse={b['rmse_mV']:.2f} mV · x100={b['params']['x100']:.4f} · R={1e3 * b['params']['R']:.2f} mV · "
          f"ρ(BOL, n_li)={b['profiles']['LLI']['rho']:.3f} · group {g['seconds']:.0f} s")
    print(f"   {'truth (LLI,PE,NE)':<20} {'rmse':>6} | " + " | ".join(f"{m:>6} err  hw  id cov" for m in MODES) + " |   gap err  naive-hw cov")
    for c in g["cases"]:
        t = c["truth"]
        lab = f"({t['LLI']:.2f},{t['LAM_PE']:.2f},{t['LAM_NE']:.2f})"
        if "error" in c:
            print(f"   {lab:<20} ERROR {c['error']}")
            continue
        cells = []
        for m in MODES:
            r = c["modes"][m]
            cells.append(f"{pp(r['err']):+6.2f} {pp(r['half_width']):5.1f} {'Y' if r['identifiable'] else 'n'} {'Y' if r['covers_truth'] else 'n'}")
            if r["identifiable"] and not r["covers_truth"]:
                danger.append((g["leg"], g["window"], lab, m, pp(r["err"]), pp(r["half_width"])))
        gp = c["gap"]
        ghw = 0.5 * (gp["naive_iv"][1] - gp["naive_iv"][0])
        print(f"   {lab:<20} {c['rmse_mV']:6.2f} | " + " | ".join(cells) + f" | {pp(gp['err']):+7.2f} {pp(ghw):7.1f}   {'Y' if gp['covers_truth'] else 'n'}")
    if any("mode_interval_check_max_abs_diff" in c for c in g["cases"]):
        print("   mode_interval 재사용 식 대조 (첫 사례):", [c["mode_interval_check_max_abs_diff"] for c in g["cases"] if "mode_interval_check_max_abs_diff" in c])
    print()

print("== 묶음별 집계 (사례 12 · 오류 사례 제외)")
print(f"   {'leg':<15} {'window':<13} {'mode':<7} {'id/n':>5} {'cov/n':>6} {'pcov/n':>7} {'med|err|':>9} {'max|err|':>9} {'med hw':>7} {'med budget':>11} {'med ρ':>6}")
for g in R["groups"]:
    ok = [c for c in g["cases"] if "modes" in c]
    for m in MODES:
        rs = [c["modes"][m] for c in ok]
        print(f"   {g['leg']:<15} {g['window']:<13} {m:<7} {sum(r['identifiable'] for r in rs):>2}/{len(rs):<2} {sum(r['covers_truth'] for r in rs):>3}/{len(rs):<2} "
              f"{sum(r['profile_covers_truth'] for r in rs):>4}/{len(rs):<2} {median(abs(pp(r['err'])) for r in rs):9.2f} {max(abs(pp(r['err'])) for r in rs):9.2f} "
              f"{median(pp(r['half_width']) for r in rs):7.1f} {median(pp(r['budget']) for r in rs):11.2f} {median(c['rho'][m] for c in ok):6.3f}")
    gs = [c["gap"] for c in ok]
    print(f"   {g['leg']:<15} {g['window']:<13} {'GAP':<7} {'':>5} {sum(x['covers_truth'] for x in gs):>3}/{len(gs):<2} {'':>7} {median(abs(pp(x['err'])) for x in gs):9.2f} "
          f"{max(abs(pp(x['err'])) for x in gs):9.2f} {median(pp(0.5 * (x['naive_iv'][1] - x['naive_iv'][0])) for x in gs):7.1f}")
print()
print("== '식별 가능' 인데 참값을 못 덮은 경우 (위험):", danger if danger else "없음")
n_err = sum(1 for g in R["groups"] for c in g["cases"] if "error" in c)
print("== 실패 사례 수:", n_err)
```

### e1_ctrl.py (sha256 `d9d3bf7577501bd757e67afe7d4a8056baea6d6fe77d4eb38d3aa1ce5cd108e0`)

```python
"""ocvfit E1 대조군 (E1-ctrl) — 같은 화학 (우리 반쪽전지 OCP) · 같은 창 · 같은 판정 절차를, ocvfit 자기 모델로 합성한 곡선에 적용한다.

목적: E1 본 실험 (DFN 0.05 C 곡선) 에서 '식별 불가' 가 무엇 때문인지 가른다 — 정보 부족인가, 모델 불일치 (SOC 따라 변하는 과전압 ↔ 상수 R) 인가.
합성: v_full 고정 CapacityModel (완충 휴지 전압 4.18 V · 하한 2.6 V · 300 점 · 잡음 1 mV · 사례마다 seed) — BOL 매개 = E1 의 W0 · R0 BOL 적합값
      (Q_pe · Q_ne · n_li · R) · aged = Q_pe(1−LAM_PE) · Q_ne(1−LAM_NE) · n_li(1−LLI) · R 동일 → 참값이 ocvfit 정의 그대로다.
판정: E1 과 같은 함수 (x100 자유 CapacityModel 적합 · 모드 구간 · bias_budget 8 회 · 1 %p) · 기준 다리 R0 만.
쓰는 곳: argv[3] 의 JSON 하나 (스크래치패드).

  사용: venv/bin/python -I e1_ctrl.py <halfcell_ocp_ref.npz> <e1_results.json> <out_dir>
"""
import json
import sys
import time
import traceback
from multiprocessing import Pool
from pathlib import Path

import numpy as np

import ocvfit as of
from ocvfit.uncertainty import MODE_PARAMETERS

REF = np.load(sys.argv[1])
E1 = json.load(open(sys.argv[2], encoding="utf-8"))
OUT = Path(sys.argv[3])
MODES = ("LLI", "LAM_PE", "LAM_NE")
CASES = [tuple(c) for c in E1["identity"]["design"]["cases"]]
WINDOWS = {k: tuple(v) for k, v in E1["identity"]["design"]["windows"].items()}
V_FULL, V_MIN, N, NOISE = 4.18, 2.6, 300, 1e-3
g0 = next(g for g in E1["groups"] if g["window"] == "W0_full" and g["leg"] == "R0_exact")
BOLP = {k: g0["bol"]["params"][k] for k in ("Q_pe", "Q_ne", "n_li", "R")}

pos = of.OCPCurve(REF["y_pe"], REF["u_pe"], name="PE")
neg = of.OCPCurve(REF["z_ne"], REF["u_ne"], name="NE")
SYN = of.CapacityModel(pos, neg, v_full=V_FULL)      # 합성용 (같은 완충 휴지 전압까지 충전한 셀)
FIT = of.CapacityModel(pos, neg)                     # 판정용 (E1 과 같음 · x100 자유)


def synth(lli, pe, ne, seed, window):
    p = [BOLP["Q_pe"] * (1 - pe), BOLP["Q_ne"] * (1 - ne), BOLP["n_li"] * (1 - lli), BOLP["R"]]
    q, v = of.synthesize_discharge(SYN, p, v_min=V_MIN, n=N, noise=NOISE, seed=seed)
    lo, hi = window
    keep = np.ones(v.size, bool)
    if lo is not None:
        keep &= v >= lo
    if hi is not None:
        keep &= v <= hi
    q, v = q[keep], v[keep]
    if hi is not None:
        q = q - q[0]
    return q, v, p


def profiles(fit):
    return {m: list(map(float, of.profile_interval(fit, par).interval)) for m, par in MODE_PARAMETERS.items()}


def group(wname):
    t0 = time.time()
    qb, vb, pb_true = synth(0, 0, 0, 0, WINDOWS[wname])
    bol = of.fit_capacity(FIT, qb, vb)
    pb = profiles(bol)
    rec = {"window": wname, "bol": {"n": int(vb.size), "rmse_mV": 1e3 * float(bol.rmse), "params": {k: float(v) for k, v in bol.param_dict.items()},
                                    "true_params": pb_true}, "cases": []}
    for i, (lli, pe, ne) in enumerate(CASES, start=1):
        t1 = time.time()
        item = {"truth": {"LLI": lli, "LAM_PE": pe, "LAM_NE": ne}}
        try:
            qa, va, pa_true = synth(lli, pe, ne, i, WINDOWS[wname])
            aged = of.fit_capacity(FIT, qa, va)
            modes = of.degradation_modes(bol, aged)
            pa = profiles(aged)
            iv = {m: (1 - pa[m][1] / pb[m][0], 1 - pa[m][0] / pb[m][1]) for m in MODES}

            def refit(positives, negative):
                mm = of.CapacityModel(positives[0], negative)
                b = of.fit_capacity(mm, qb, vb, n_starts=3)
                a = of.fit_capacity(mm, qa, va, n_starts=3)
                return of.degradation_modes(b, a)

            bud = of.bias_budget(refit, [pos], neg, {m: modes[m] for m in MODES}, n_draws=8, seed=1)
            res = {}
            for m in MODES:
                lo, hi = iv[m]
                flo, fhi = lo - bud[m], hi + bud[m]
                half = 0.5 * (fhi - flo)
                t = item["truth"][m]
                res[m] = {"est": float(modes[m]), "err": float(modes[m] - t), "profile_iv": [float(lo), float(hi)], "budget": float(bud[m]),
                          "final_iv": [float(flo), float(fhi)], "half_width": float(half), "identifiable": bool(of.is_identifiable(half)),
                          "covers_truth": bool(flo <= t <= fhi), "profile_covers_truth": bool(lo <= t <= hi)}
            pr = of.profile_interval(aged, "n_li")
            item.update({"n": int(va.size), "rmse_mV": 1e3 * float(aged.rmse), "rho_aged_n_li": float(pr.rho), "true_params": pa_true,
                         "params": {k: float(v) for k, v in aged.param_dict.items()}, "modes": res, "seconds": time.time() - t1})
        except Exception as e:
            item.update({"error": repr(e), "traceback": traceback.format_exc(), "seconds": time.time() - t1})
        rec["cases"].append(item)
        print(json.dumps({"w": wname, "truth": item["truth"], "err": {m: round(item["modes"][m]["err"], 4) for m in MODES} if "modes" in item else item.get("error"),
                          "flags": {m: item["modes"][m]["identifiable"] for m in MODES} if "modes" in item else None,
                          "cover": {m: item["modes"][m]["covers_truth"] for m in MODES} if "modes" in item else None, "s": round(item["seconds"], 1)}), flush=True)
    rec["seconds"] = time.time() - t0
    return rec


def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    with Pool(3) as p:
        groups = p.map(group, list(WINDOWS))
    out = {"identity": {"ocvfit": of.__version__, "numpy": np.__version__, "synthesis": {"v_full": V_FULL, "v_min": V_MIN, "n": N, "noise": NOISE,
                        "bol_params_from": "E1 W0_full R0_exact BOL fit", "bol_params": BOLP}, "cases": CASES, "windows": WINDOWS},
           "groups": groups, "wall_s": time.time() - t0}
    (OUT / "e1_ctrl_results.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"wall_s": round(out["wall_s"], 1)}))


if __name__ == "__main__":
    main()
```

### summarize_ctrl.py (sha256 `e30958aec3ea64bbb7aded6ece78d0ef7552757b65c0eebb1e2831589ffbb25c`)

```python
"""E1-ctrl 결과 요약 (읽기만).

  사용: venv/bin/python -I summarize_ctrl.py <e1_ctrl_results.json>
"""
import json
import sys
from statistics import median

R = json.load(open(sys.argv[1], encoding="utf-8"))
MODES = ("LLI", "LAM_PE", "LAM_NE")
pp = lambda x: 100.0 * x  # noqa: E731
print("identity:", json.dumps(R["identity"], ensure_ascii=False))
print("wall_s:", round(R["wall_s"], 1))
danger = []
for g in R["groups"]:
    b = g["bol"]
    print(f"\n== ctrl · {g['window']} · BOL n={b['n']} rmse={b['rmse_mV']:.2f} mV · group {g['seconds']:.0f} s")
    print(f"   {'truth (LLI,PE,NE)':<20} {'rmse':>6} {'ρ':>6} | " + " | ".join(f"{m:>6} err  hw  id cov" for m in MODES))
    for c in g["cases"]:
        t = c["truth"]
        lab = f"({t['LLI']:.2f},{t['LAM_PE']:.2f},{t['LAM_NE']:.2f})"
        if "error" in c:
            print(f"   {lab:<20} ERROR {c['error']}")
            continue
        cells = []
        for m in MODES:
            r = c["modes"][m]
            cells.append(f"{pp(r['err']):+6.2f} {pp(r['half_width']):5.1f} {'Y' if r['identifiable'] else 'n'} {'Y' if r['covers_truth'] else 'n'}")
            if r["identifiable"] and not r["covers_truth"]:
                danger.append((g["window"], lab, m, pp(r["err"]), pp(r["half_width"])))
        print(f"   {lab:<20} {c['rmse_mV']:6.2f} {c['rho_aged_n_li']:6.3f} | " + " | ".join(cells))
print("\n== 묶음별 집계")
print(f"   {'window':<13} {'mode':<7} {'id/n':>5} {'cov/n':>6} {'med|err|':>9} {'max|err|':>9} {'med hw':>7}")
for g in R["groups"]:
    ok = [c for c in g["cases"] if "modes" in c]
    for m in MODES:
        rs = [c["modes"][m] for c in ok]
        print(f"   {g['window']:<13} {m:<7} {sum(r['identifiable'] for r in rs):>2}/{len(rs):<2} {sum(r['covers_truth'] for r in rs):>3}/{len(rs):<2} "
              f"{median(abs(pp(r['err'])) for r in rs):9.2f} {max(abs(pp(r['err'])) for r in rs):9.2f} {median(pp(r['half_width']) for r in rs):7.1f}")
print("\n== '식별 가능' 인데 참값을 못 덮은 경우 (위험):", danger if danger else "없음")
print("== 실패 사례 수:", sum(1 for g in R["groups"] for c in g["cases"] if "error" in c))
```

