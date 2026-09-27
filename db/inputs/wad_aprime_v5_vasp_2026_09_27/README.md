# A′ V5 — VASP 단일점 외주 패키지 v3 (LPSCl | Ag(111) 작은 주기 계면)

> 상태: **준비본 (실행 미정)** · Codex CE·CF NO-GO 반영판 · 재리뷰 전 · 결정 `D-2026-09-27-wad-aprime-v5-vasp-route` **proposed**
> 원본: 봉인 S3v2 패키지 (구조 파일 sha 결박) · 이 패키지 MANIFEST.sha256 의 sha256 = `da260794745bdbda2d827f116162115af90e82e229f897aad00166aff16dcdd4` (보낼 때 메일 본문에 적는다 — 반송 검사가 이 값으로 승인본을 확인한다)

## 무엇을 하나
PBE+D3(BJ) **단일점(SCF) 18 개** — 이완 없음. 좌표는 이미 정해져 있습니다 (POSCAR 그대로).

| 잡 | 역할 | NIONS | NELECT | 셀 a×b×c (Å) | ENCUT (eV) | k (Γ) | SIGMA (eV) |
|---|---|---|---|---|---|---|---|
| `V5_li_outer_A_bound` | 표본 끝점 | 176 | 1356 | 10.055×20.110×29.566 | 520 | 3×2×1 | 0.136 |
| `V5_li_outer_A_far` | 표본 끝점 | 176 | 1356 | 10.055×20.110×29.566 | 520 | 3×2×1 | 0.136 |
| `V5_li_outer_B_bound` | 표본 끝점 | 176 | 1356 | 10.055×20.110×29.520 | 520 | 3×2×1 | 0.136 |
| `V5_li_outer_B_far` | 표본 끝점 | 176 | 1356 | 10.055×20.110×29.520 | 520 | 3×2×1 | 0.136 |
| `V5_s_outer_A_bound` | 표본 끝점 | 200 | 1452 | 10.055×20.110×32.058 | 520 | 3×2×1 | 0.136 |
| `V5_s_outer_A_far` | 표본 끝점 | 200 | 1452 | 10.055×20.110×32.058 | 520 | 3×2×1 | 0.136 |
| `V5_s_outer_A_G3_c2_bound` | G3 끝점 검사 (c+2) | 200 | 1452 | 10.055×20.110×34.058 | 520 | 3×2×1 | 0.136 |
| `V5_s_outer_A_G3_c2_far_i` | G3 끝점 검사 (c+2) | 200 | 1452 | 10.055×20.110×34.058 | 520 | 3×2×1 | 0.136 |
| `V5_s_outer_A_G3_c2_far_ii` | G3 끝점 검사 (c+2) | 200 | 1452 | 10.055×20.110×34.058 | 520 | 3×2×1 | 0.136 |
| `V5_s_outer_A_G4_e70_bound` | G4 수치 검사 (ENCUT 650) | 200 | 1452 | 10.055×20.110×32.058 | 650 | 3×2×1 | 0.136 |
| `V5_s_outer_A_G4_e70_far` | G4 수치 검사 (ENCUT 650) | 200 | 1452 | 10.055×20.110×32.058 | 650 | 3×2×1 | 0.136 |
| `V5_s_outer_A_G4_k1_bound` | G4 수치 검사 (k 4×3×1) | 200 | 1452 | 10.055×20.110×32.058 | 520 | 4×3×1 | 0.136 |
| `V5_s_outer_A_G4_k1_far` | G4 수치 검사 (k 4×3×1) | 200 | 1452 | 10.055×20.110×32.058 | 520 | 4×3×1 | 0.136 |
| `V5_s_outer_A_G4_s05_bound` | G4 수치 검사 (SIGMA ½) | 200 | 1452 | 10.055×20.110×32.058 | 520 | 3×2×1 | 0.068 |
| `V5_s_outer_A_G4_s05_far` | G4 수치 검사 (SIGMA ½) | 200 | 1452 | 10.055×20.110×32.058 | 520 | 3×2×1 | 0.068 |
| `V5_s_outer_A_p05_bound` | 표본 끝점 | 200 | 1452 | 10.055×20.110×32.058 | 520 | 3×2×1 | 0.136 |
| `V5_s_outer_B_bound` | 표본 끝점 | 200 | 1452 | 10.055×20.110×32.011 | 520 | 3×2×1 | 0.136 |
| `V5_s_outer_B_far` | 표본 끝점 | 200 | 1452 | 10.055×20.110×32.011 | 520 | 3×2×1 | 0.136 |

## 돌리는 법
1. **파일럿 2 잡 먼저** (표본 ① 두 끝점 · 반송해 주세요): `JOBS="V5_s_outer_A_bound V5_s_outer_A_far" VASP_CMD="mpirun -np <N> vasp_std" POTCAR_DIR=<PAW_PBE> bash run_all.sh`
   — 파일럿 전에 VASP 버전·PP 세트·설정·파서·실패 규칙은 고정돼 있습니다. 파일럿의 W 값을 보고 설정을 바꾸지 않습니다.
2. 확인 연락을 받으면 **나머지 16 잡**: `JOBS="<16 잡>" ... bash run_all.sh` (파일럿 두 잡은 이 패키지 sha 그대로라면 **재사용** — 다시 돌리지 않습니다).
   파일럿 뒤에 VASP 입력이 바뀌어야 하면 새 패키지 버전이 나가고, 파일럿은 구판 진단으로만 남습니다.
3. 성능 태그는 `PERF_TAGS_FILE=perf.txt` 로만 — **한 줄에 대입 하나**, 허용: NCORE NPAR KPAR NSIM (양의 정수) · LPLANE LSCALU LSCALAPACK (.TRUE./.FALSE.).
   세미콜론(;) · 역슬래시(\) · 같은 태그 두 번 · 줄 끝 주석은 거부됩니다. **INCAR·POSCAR·KPOINTS 는 고치지 마세요.**
4. 시도 폴더 `run/<잡>` 이 이미 있으면 러너가 그 잡을 **돌리지 않습니다** (지난 출력 재사용 방지). 재시도 상한은 잡마다 사전등록 1 회이고,
   **그 밖의 수동 재실행은 새 승인 없이는 하지 않습니다** — 필요해 보이면 먼저 연락 주세요.
5. 한 잡이 실행 실패·미종료·미수렴이면 러너가 미리 정한 재시도(INCAR.r1 · AMIX 0.1 · BMIX 0.01 · NELM 300)를 **한 번만** 합니다.
   그래도 안 되면 그 잡은 비워 둡니다 — 다른 설정으로 더 돌리지 마세요. 실행 상한 = 18 × 2 = **36 회** (파일럿 재사용 시).
6. 반송 묶음 포장(tar · sha256)이 실패하면 러너가 **종료코드 4** 로 끝나고 계산 결과는 `run/` 에 그대로 남습니다.
   계산을 다시 돌리지 말고 `PACK_ONLY=1 bash run_all.sh` 로 **포장만** 다시 해 주세요.
   러너 종료코드: 0 전 잡 성공 · 1 일부 잡 실패 (묶음은 만듦 — 실패도 반송) · 2 패키지·성능 파일 오류 (아무것도 안 돎) · 4 포장 실패.

## VASP 버전 · POTCAR — 이 조합으로 고정
- **VASP**: 파일럿과 본 배치가 **같은 빌드**여야 합니다 (OUTCAR 첫 줄로 확인 · 다르면 그 배치는 쓰지 않습니다). 버전·빌드를 `run/env.txt` 에 적어 주세요.
  INCAR 의 VDW_S6 는 문서상 VASP 6.6.0 부터 사용자 조정이 되지만, 값 1.0 은 PBE 기본값과 같습니다 (구버전이어도 같은 값).
- **POTCAR** PBE_54: Li_sv (`PAW_PBE Li_sv 10Sep2004`) · P (`PAW_PBE P 06Sep2000`) · S (`PAW_PBE S 06Sep2000`) · Cl (`PAW_PBE Cl 06Sep2000`) · Ag (`PAW_PBE Ag 02Apr2005`).
  파일럿에서 TITEL(날짜 포함)·종별·조립본 sha256 을 확인해 **등록부로 봉인**하고, 이후 모든 잡이 그 등록부와 같아야 합니다. 다른 PP 트리로 바꾸지 마세요.
  POTCAR 파일은 **보내지 마세요** — 러너가 TITEL/ZVAL/LEXCH 줄 · 종별 sha256 · 조립본 sha256 만 남깁니다.

## 돌려받을 것
`V5_vasp_return.tgz` + `.sha256` (러너가 만듭니다): 시도마다 OUTCAR · OSZICAR · INCAR(실행본) · KPOINTS · POSCAR · POTCAR.titel · POTCAR.sha256 · POTCAR.species.sha256 · attempt.json · stdout.log
· `run/status.tsv` · `run/env.txt`. VASP 버전·빌드·컴파일러·노드/코어 수·**잡별 peak RSS·벽시계** 를 `run/env.txt` 에 한 줄씩 덧붙여 주세요.
실패한 잡도 폴더째 보내 주세요 (실패도 기록입니다).

## 규모 (대략 · 우리 추정 — 견적은 파일럿 벽시계·peak RSS 로)
NIONS 176–200 · NELECT 1356–1452 · 기본 NBANDS ~826 · 평면파 최대 ~185,434/k (ENCUT 520) · ~243,934/k (ENCUT 650 · G4 변형 2 잡)
· 파동함수 몫만 ~16.1 GB (k 합 · **peak RSS 아님** — FFT·투영자·작업 배열·MPI 복제는 따로) · 환원 k 추정 Γ3×2×1 ≈ 4 · Γ4×3×1 ≈ 7 (IBZKPT 로 확인).
비스핀 · 금속(Ag) 슬랩 · 진공 포함 · LREAL=F · 실행 최대 36 회. KPAR 는 실제 k 수·메모리·노드 배치에 맞춰 업체가 고릅니다.

## English summary
18 single-point PBE+D3(BJ) SCF runs (no relaxation) on fixed geometries. PAW_PBE PBE_54 Li_sv/P/S/Cl/Ag (TITELs above; sealed after the pilot);
the pilot and the main batch must use the same VASP build. ENCUT 520 eV (650 eV for two G4 jobs); ISMEAR 1, SIGMA 0.136 eV; IVDW 12 with explicit
PBE-BJ parameters and explicit VDW_RADIUS/VDW_CNRADIUS; dipole correction along z (LDIPOL, IDIPOL 3, DIPOL given). Run the two pilot jobs first and
return them. Do not edit INCAR/POSCAR/KPOINTS (performance tags only via PERF_TAGS_FILE, one assignment per line, no ';'); existing attempt folders
are never overwritten; one pre-registered retry per job (max 36 runs) and no other manual reruns without approval; if packaging fails (exit 4)
rerun with PACK_ONLY=1 to repackage only. Do not send POTCAR files. Please report VASP version/build and per-job peak RSS and wall time.
