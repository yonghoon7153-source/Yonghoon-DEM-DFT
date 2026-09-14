# `report_reruns` 97 행 — 규진팀 실험 스윕 원표

## 출처와 승인

규진팀 `main_blend_final.m` 계열로 돌린 실험 스윕 8 종. 사용자 기계의
`D:\…\degradation mode\report_reruns\*.csv` 를 **그대로** 옮겼다 (수치 변형 없음).

**공개 승인**: 2026-09-10, 사용자가 전권으로 공개를 지시. 그 전까지 이 표는
저장소 밖에 있었고, 그래서 `FINDINGS.md` §2 의 숫자는 **문서에 적힌 주장**일
뿐 재현이 안 됐다.

## 왜 올리나

§2 는 이 표에서 센 값을 근거로 쓴다. 표가 없으면 제3자가 그 숫자를 확인할 수
없다. `정본은 artifact` 라는 이 저장소의 규칙이 §2 에만 안 지켜지고 있었다.

    python3 scripts/audit97.py          # §2 의 숫자를 이 표에서 재계산
    python3 scripts/audit97.py --rows   # 행별 감사표

## 8 파일 · 97 행

| 파일 | 행 | 무엇을 바꿔 본 것인가 |
|---|---|---|
| `exp10_si_source_sensitivity.csv` | 32 | 문헌 Si 곡선 8 종 × 4 상태 |
| `exp5_peakweight_dqdv.csv` | 12 | 피크 가중 방식 3 종 (양극 피크 추가 · dQ/dV 제외) |
| `exp_abc_nodqdv.csv` | 12 | Track A/B/C (γ 없음 · γ 고정 · γ 자유) |
| `exp6_halfcell_source.csv` | 9 | 반쪽전지 소스 (GITT vs 0.05C step) |
| `exp7_fullcell_source.csv` | 8 | 풀셀 소스 (0.33C large cell vs 0.05C pouch) |
| `exp8_trackD_gain_penalty.csv` | 8 | gain penalty 유무 (σ_PE·σ_NE 가 추가 파라미터) |
| `exp9_gamma_fixed_vs_free.csv` | 8 | γ 고정 vs 자유 |
| `trackB_dqdv_compare.csv` | 8 | dQ/dV 포함(w=1) vs 제외(방법3) |

## 읽을 때 주의

- **행마다 설정이 다르다.** 파일을 가로질러 값끼리 비교하면 안 된다. 각 파일
  안에서 `state=pristine` 인 행이 그 그룹의 **기준**이고, LAM/LLI 는 전부
  그 기준 대비다.
- `exp7` 의 `0.05C_pouch` 행은 `c_cell` 단위가 다르다 (0.0088 vs 74.671).
  비율로만 들어가므로 LAM/LLI 계산에는 문제가 없지만, 절대 용량으로 읽지 말 것.
- `exp10` 의 `gamma_init` 은 **시작점**이지 적합 결과가 아니다. 경계 검사에서
  제외한다.
- `exp8` 의 `sigma_PE`/`sigma_NE` 는 다른 파라미터이고 그 상자를 우리가 모른다.
  경계 검사에서 뺐다 — 다만 `gain_penalty` 의 `300_0009` 행이 `sigma_NE = 0.3`
  으로 딱 떨어지는 것은 상한일 가능성이 있다. 규진팀에 확인할 것.
