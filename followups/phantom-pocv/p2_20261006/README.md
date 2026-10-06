# P2 실행 기록 — 꼭대기 무거운 SOC 의존 PE 오프셋 (2026-10-06)

> **진단 전용 · smoke · 인용 금지.** 이 디렉터리의 수치는 저장소 밖 사본의 `results/_smoke/` 산출이다. 정본은 artifact +
> `degradation-degeneracy/docs/RESULTS*.md` 이고, 여기 숫자는 어느 쪽도 아니다 (planned leg · 게이트 없음 — 승인 문서 §4-7).

## 결론 한 줄

**§5 중단 — L5 원점 오염 (권고 5: 세트 중단).** tilt 효과의 해석은 하지 않았다. 앞선 검사 (캐시 · L1 원점 · 조건 집합 ·
L2 / L3 + 부호 재현) 는 모두 통과했다.

## 승인 · 범위

- 승인: `../P2_APPROVAL_REQUEST.md` §7 문구 ("다 승인" · 2026-10-06) · §4 권고 전부 · 실행 전 고정값은 같은 문서 §8.
- 사본: 저장소 `4e99a09a9` → 사본 `0ab9cd9` → `d210440` (오프셋 식 · `src/halfcell.py` 만 · `copy_patch_d210440.patch`). 저장소 코드 변경 0.
- 판정 규칙은 fit 전에 고정: `run/p2_components.py` docstring · sha 는 `run/09_rules_fixed_before_fits.txt` (19:32:00Z · 첫 fit 19:33Z).

## 순서와 결과

| 단계 | 기록 (`run/`) | 결과 |
|---|---|---|
| 환경 | `00_env.txt` | py 3.11.15 · pybamm 26.8.0.0 · numpy 2.4.6 · scipy 1.17.1 · pandas 3.0.5 |
| 완방 상태 → y_B | `01_discharged_state.*` | rc 0 · y_T 0.2699987… · y_B 0.9260882… (§8) |
| 캐시 6 `--verify` | `02`–`07` | 전부 rc 0 · 구조 true · 배열 일치 |
| 형상 점검 | `08a_failed_isolated_*` → `08_*` | 1 차 rc 1 (`python -I` 가 사용자 site-packages 를 끊어 dateutil import 실패 · 계산 0) → 재실행 rc 0 · 통과 |
| grid (L0 곡선) | `10a_gate_refused_*` → `10_grid_L0.*` | 1 차 rc 1 (사본에 `results/_smoke/` 실물이 없어 smoke 면제 실패 · 0.7 s · 계산 0) → 빈 디렉터리 생성 뒤 rc 0 · 213 s · 곡선 320 (infeasible 80 = PE-limited 설계 영역) |
| 시간 측정 | `11_timing_limit8.*` | 8 조건 18.6 s (≈ 2.3 s/조건) → 예산 안으로 판단 · 계속 |
| L0 · L1 | `20_fit_L0.*` · `21_fit_L1.*` | rc 0 · 667 s · 654 s · **L1 원점 a_ne 1.0617 / 1.0613 (통과)** |
| L2 – L6 | `22`–`26_fit_L*.*` · `legs_progress.txt` | 전부 rc 0 · 각 630–682 s · 끝 20:50:46Z |
| + 부호 판정 (L1–L3) | `30_sign_check_L1_L3.*` | **통과** — `pocv_dvdq_dqdv` 원 창 Δ(L2) · Δ(L3) 모두 + |
| 성분 분석 (전 다리) | `31_components_all.*` · `.json` | rc 1 = 중단 조건: **L5 a_ne 1.0224 (`pocv_dvdq`) · 1.0148 (`pocv_dvdq_dqdv`) ∉ [1.05, 1.08]** · 나머지 다리 원점 범위 안 · cond 집합 같음 (복원가능군 232) |
| 기존 도구 | `32_diagnose_*` · `33_analyze_*` | rc 0 · 기록만 (아래 주의) |

- 예산: 시계 19:24:56Z → 마지막 계산 20:50:46Z (1 h 26 m) · 디스크 여유 최저 ≈ 7.0 GB · 다리 재실행 0.
- **순서 주의:** 왜곡 다리의 원점 검사는 분석 단계에 두었기 때문에, L5 오염은 L6 계산이 끝난 뒤에 확인됐다 (계산은 예산 안).
- `_debug_L1.json` 은 L2 계산 중 스크립트 디버그로 L1 만 넣어 돌린 것 (판정 아님).

## 해석하지 않은 것 · 주의

- L4 · L6 의 값은 `31_components_all.json` 에 있지만, 권고 5 (세트 중단) 에 따라 **tilt vs 평균 분리의 해석은 하지 않는다**.
  이를 해석하려면 §5 의 다른 선택지 ("오염 다리만 해석 제외") 로 바꾸는 사용자 결정이 필요하다.
- `diagnose_pini_transition.py` 는 `pe_tilt_mv` 를 읽지 않는다 — tilt 다리를 "PE +N mV" (오프셋만) 로 표기한다. 표기만 틀리고 수치는 같은 fits 에서 나온다.
- `pocv_dvdq` 의 L3 는 원 창 Δ 와 허용 창 Δ 의 부호가 다르다 (판정은 §7.10 목적함수 `pocv_dvdq_dqdv` 로만 · 보고만).
- `gap_stats` 창 경계: 이 격자에서 원 창 74 행 ↔ 허용 창 (`<= 0.02 + 1e-9`) 117 행. 승인 문서 §4-6 대로 저장소는 고치지 않고 게이트 후보로만 남긴다.
- δ_eff 는 "L1 fit 이 본 창" (무왜곡 fit 의 a_pe · b_pe 역변환) 기준이다 — truth 창이 아니다 (무열화 원점 창 0.277–0.954 / 0.278–0.936 vs truth 0.270–0.926).

## 파일

- `run/` — 명령 기록 119 (meta · stdout · stderr · JSON · 스크립트 `rl.sh` · `run_legs.sh` · `cache_check.py` · `p2_components.py`).
- `manifests/` — 각 다리 `manifest.yaml` 사본 (run_spec · p_ini · halfcell_recipe · source_digest `194b1c515598d991` = 사본 코드).
- `LARGE_OUTPUTS_SHA256.txt` — fits / curves parquet 은 sha 만 (사본 76 MB · 저장소에 넣지 않음).
