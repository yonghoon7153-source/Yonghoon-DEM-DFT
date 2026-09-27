# A′ V5 — VASP 단일점 외주 패키지 (LPSCl | Ag(111) 작은 주기 계면)

> 상태: **준비본 (실행 미정)** · 설계 리뷰(Codex CE) 전 · 결정 `D-2026-09-27-wad-aprime-v5-vasp-route` **proposed**
> 원본: 봉인 S3v2 패키지 (구조 파일 sha 결박) · 이 패키지 MANIFEST.sha256 의 sha256 = `ae434e671ba74ef5851d5826a9672ee85eb56f69ecf3a27d0f6859e92ee188b9` (보낼 때 메일 본문에 적는다)

## 무엇을 하나
PBE+D3(BJ) **단일점(SCF) 18 개** — 이완 없음. 좌표는 이미 정해져 있습니다 (POSCAR 그대로).

| 잡 | 역할 | 원자 | ENCUT (eV) | k (Γ) | SIGMA (eV) |
|---|---|---|---|---|---|
| `V5_li_outer_A_bound` | 표본 끝점 | 176 | 520 | 3×2×1 | 0.136 |
| `V5_li_outer_A_far` | 표본 끝점 | 176 | 520 | 3×2×1 | 0.136 |
| `V5_li_outer_B_bound` | 표본 끝점 | 176 | 520 | 3×2×1 | 0.136 |
| `V5_li_outer_B_far` | 표본 끝점 | 176 | 520 | 3×2×1 | 0.136 |
| `V5_s_outer_A_bound` | 표본 끝점 | 200 | 520 | 3×2×1 | 0.136 |
| `V5_s_outer_A_far` | 표본 끝점 | 200 | 520 | 3×2×1 | 0.136 |
| `V5_s_outer_A_G3_c2_bound` | G3 끝점 검사 (c+2) | 200 | 520 | 3×2×1 | 0.136 |
| `V5_s_outer_A_G3_c2_far_i` | G3 끝점 검사 (c+2) | 200 | 520 | 3×2×1 | 0.136 |
| `V5_s_outer_A_G3_c2_far_ii` | G3 끝점 검사 (c+2) | 200 | 520 | 3×2×1 | 0.136 |
| `V5_s_outer_A_G4_e70_bound` | G4 수치 검사 (ENCUT 650) | 200 | 650 | 3×2×1 | 0.136 |
| `V5_s_outer_A_G4_e70_far` | G4 수치 검사 (ENCUT 650) | 200 | 650 | 3×2×1 | 0.136 |
| `V5_s_outer_A_G4_k1_bound` | G4 수치 검사 (k 4×3×1) | 200 | 520 | 4×3×1 | 0.136 |
| `V5_s_outer_A_G4_k1_far` | G4 수치 검사 (k 4×3×1) | 200 | 520 | 4×3×1 | 0.136 |
| `V5_s_outer_A_G4_s05_bound` | G4 수치 검사 (SIGMA ½) | 200 | 520 | 3×2×1 | 0.068 |
| `V5_s_outer_A_G4_s05_far` | G4 수치 검사 (SIGMA ½) | 200 | 520 | 3×2×1 | 0.068 |
| `V5_s_outer_A_p05_bound` | 표본 끝점 | 200 | 520 | 3×2×1 | 0.136 |
| `V5_s_outer_B_bound` | 표본 끝점 | 200 | 520 | 3×2×1 | 0.136 |
| `V5_s_outer_B_far` | 표본 끝점 | 200 | 520 | 3×2×1 | 0.136 |

## 돌리는 법
1. **파일럿 1 잡 먼저** (파서 확인용 · 반송해 주세요): `JOBS=V5_s_outer_A_far VASP_CMD="mpirun -np <N> vasp_std" POTCAR_DIR=<PAW_PBE> bash run_all.sh`
2. 확인 연락을 받으면 전체: `VASP_CMD=... POTCAR_DIR=... bash run_all.sh` (이미 끝난 잡도 다시 돕니다 — 파일럿 폴더는 `run/` 밖으로 옮겨 두세요)
3. 성능 태그는 `PERF_TAGS_FILE=perf.txt` 로만 (허용: NCORE NPAR KPAR NSIM LPLANE LSCALU LSCALAPACK). **INCAR·POSCAR·KPOINTS 는 고치지 마세요.**
4. 한 잡이 수렴하지 않으면 러너가 미리 정한 재시도(INCAR.r1 · AMIX 0.1 · BMIX 0.01 · NELM 300)를 **한 번만** 합니다. 그래도 안 되면 그 잡은 비워 둡니다 — 다른 설정으로 더 돌리지 마세요.

## POTCAR (업체 라이선스 보유분)
PAW_PBE **Li_sv · P · S · Cl · Ag** (PBE_54 권장 · Materials Project 와 같은 선택). 각 잡의 `POTCAR.spec` 순서대로 러너가 조립합니다.
POTCAR 파일은 **보내지 마세요** — 러너가 TITEL/ZVAL 줄과 sha256 만 남깁니다.

## 돌려받을 것
`V5_vasp_return.tgz` + `.sha256` (러너가 만듭니다): 잡별 OUTCAR · OSZICAR · INCAR(실행본) · KPOINTS · POSCAR · POTCAR.titel · POTCAR.sha256 · stdout.log · `run/status.tsv` · `run/env.txt`.
VASP 버전·컴파일러·노드/코어 수를 `run/env.txt` 에 한 줄씩 덧붙여 주세요.

## 규모 (대략 · 우리 추정)
NIONS 176–200 · NELECT 1356–1452 · 기본 NBANDS ~826 · 평면파 ~243,934/k (ENCUT 520) · 파동함수 전체 ~16.1 GB (k 4–7 개 합).
비스핀 · 금속(Ag) 슬랩 · 진공 포함 · LREAL=F. 시간은 기계마다 달라 파일럿 1 잡의 벽시계로 전체를 가늠합니다.

## English summary
18 single-point PBE+D3(BJ) SCF runs (no relaxation) on fixed geometries; PAW_PBE Li_sv/P/S/Cl/Ag; ENCUT 520 eV; ISMEAR 1, SIGMA 0.136 eV;
IVDW 12 with explicit PBE-BJ parameters; dipole correction along z (LDIPOL, IDIPOL 3, DIPOL given). Please run one pilot job first
(`JOBS=V5_s_outer_A_far`) and return it; do not edit INCAR/POSCAR/KPOINTS (performance tags only via PERF_TAGS_FILE); do not send POTCAR files.
