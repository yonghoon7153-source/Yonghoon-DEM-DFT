# MPFEM 바깥 기준 — 설계 · 탐침 · 회전 시험 (2026-11-25 · 개발 자료)

[DEM 우선 (수영)] · **개발 자료 · 판정 미사용 · 결과 전 등록 아님** · 만든 곳 = 본 세션 (11-25) · 리포 반입 = 서브 세션 J27 (11-25 밤 · 인계 `handoff_20261125` 묶음 그대로 · `__pycache__` 만 뺌).
바탕 공부 = `docs/reviews/dem_redesign_direction_20261109/study_mpfem_kratos_20261125.md` (§5 Q1 · Q2 · 이 폴더의 결정 줄은 그 §5 끝).

## 무엇이 있나

| 폴더 | 무엇 | 지위 |
|---|---|---|
| `mpfem_plan/` | Kratos 10.4.4 설계 (`README.md` 한 쪽 요약 · ① `step1_kratos_onedisk.md` + 입력 `step1_inputs/` · ② `step2_registration_draft.md` 2D 원판 49 개 등록 초안 · ③ `step3_outline.md` 3D 작은 조각 개요) | 설계 문서 (② = 결과 0 건 · 1저자 비준 전 · GO 전 실행 금지) |
| `mpfem_run/` | 이 컨테이너에서 돌린 탐침 — K-1 · K-2 (`mpfem_run/k2/probe_report.json`) · 회전 진단 (`mpfem_run/rot_diag.py` → `mpfem_run/rot/rot_diag.json`) · 갱신 라그랑주 회전 시험 (`mpfem_run/ul_rot_test.py` → `mpfem_run/ul/ul_rot.json`) · 우리 MPM 갱신식 회전 시험 (`mpfem_run/mpm_rot_test.py`) | 개발 자료 (`DEVELOPMENT_ONLY` 표지) |
| `moose_wsl/` | MOOSE (WSL) 설치 + 회전 시험 블록 (`moose_wsl_block.txt` · `install_and_test.sh` · `rot_test.i` · `check_rot.py`) | 1저자 WSL 실행 (11-25 · (가-1)) |

## 결과 (개발 자료 · 판정 미사용)

회전 시험 = 한 요소를 평면 변형으로 소성까지 누른 뒤 (ly 1 → 0.85) 강체로 30° 돌리고, 되돌려 본 응력이 돌리기 전과 같은지 본다.  기준 (실행 전 고정) = R1 되돌린 응력 차 ≤ 10⁻³ σy · R2 소성 뒤 von Mises 가 σy 의 2 % 안.

| 도구 · 법칙 | 회전 걸음 | 되돌린 응력 차 / σy | R1 | R2 | 근거 |
|---|---|---|---|---|---|
| Kratos `FiniteStrainIsotropicPlasticity3DVonMisesVonMises` (TL) | 1 · 30 · 300 | 0.435 · 0.563 · 0.566 | 실패 | 통과 | `mpfem_run/rot/rot_diag.json` · `mpfem_run/ul/ul_rot.json` |
| Kratos 작은 변형 J2 + 갱신 라그랑주 요소 (`UpdatedLagrangianElement3D8N`) | 1 · 300 | 0.495 · 0.495 | 실패 | 통과 | `mpfem_run/ul/ul_rot.json` (C2) |
| Kratos 초탄성 (대조 · ly 0.99) | 1 | 4.8 × 10⁻¹⁶ | — | — | `mpfem_run/rot/rot_diag.json` |
| Kratos 유한 변형 J2 · 탄성 범위 (ly 0.999 · 항복 전) | 1 | 8.8 × 10⁻¹⁶ | — | — | `mpfem_run/rot/rot_diag.json` — 어긋남은 소성 흐름 뒤에만 생긴다 |
| MOOSE (WSL · 1저자 실행) | 300 | 2.1 × 10⁻¹² | 통과 | 통과 (σ_eq/σy 1.000000) | 1저자 화면 (11-25 · 인계 HANDOFF) |
| 우리 MPM 갱신식 | — | 걸음 수 N 에 1/N 로 줄어든다 (수렴) | — | — | 본 세션 11-25 기록 · 원 출력은 이 묶음에 없음 |

- K-1 (법칙 · 요소 · 조건 이름 등록) = 통과 · K-2 (재료점 회전 객관성) = 실패 (`mpfem_run/k2/probe_report.json` · `kratos_version` 10.4.4).
- 같은 Kratos 의 `SmallStrainJ2Plasticity3DLaw` + 갱신 라그랑주 (C3) 는 차 0 이지만 소성 뒤 응력이 0 (R2 실패) — 쓰지 않는다.

## 결정 (1저자 11-25)

- 계획 (`mpfem_plan/README.md`) Q1–Q9 = 권고대로.
- **Kratos 탈락** (K-2 회전 객관성 실패 · 갱신 라그랑주 판도 같은 꼴) · **MOOSE = 주 경로** (WSL 회전 시험 통과).
- Q9 (③ 실제 SEM 단면) = litdb 카드의 그림을 쓴다.
- DEM 회전 시험 = 하지 않는다.
- 다음 = MOOSE 1 단계 (원판 하나 · 2D 평면 변형 · 판 접촉 · 메시 m13 · m26 · P1 · P2 · P4 · C) 입력 블록 → 1저자 WSL · 우리 σy → MOOSE von Mises 환산 규칙 = 2 단계 등록 때.

## 한정

- 탐침 · 회전 시험은 한 요소 · 한 조건의 개발 자료다 — 도구의 일반 품질 판정이 아니다.
- `mpfem_plan/` 의 문서는 실행 전에 쓴 것이라 *"설치 0 · 계산 0 · 리포 쓰기 0"* 같은 머리 문장이 남아 있다 (그때의 상태).
- PhotoCraft · GitHub 조사 등 같은 날 다른 묶음은 `docs/mcp/` · `docs/reviews/mcp_skill_survey_20261125/` 에 있다.
