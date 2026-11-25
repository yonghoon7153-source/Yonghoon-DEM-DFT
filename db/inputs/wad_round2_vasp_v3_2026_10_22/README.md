# W_ad 외주 2차 — VASP 단일점 묶음 (LPSCl | 흑연 작은 모델 · C–C 대조 · 은 a4)

> 상태: **준비본 v3 — Codex CZ · DB 고침 + 발송 전 자체 검토 (S1–S9) 반영 · 발송 전** · 결정 `D-2026-10-15-wad-p2small-vasp-card` · `D-2026-10-15-wad-aprime-v5-e70-a4-rerun` (active)
> 이 묶음 MANIFEST.sha256 의 sha256 = `bf7b2ac921597f601fed3324159cf9812c1a1ff91ad4a0acf0a6ce590d9ac831` (보낼 때 메일 본문에 적는다 — 반송 검사가 이 값으로 승인본을 확인한다)

## 무엇을 하나
단일점 (SCF) 24 잡 — 이완 없음. 좌표는 정해져 있습니다 (POSCAR 그대로). 단계마다 돌립니다.

| 단계 | 잡 | 종류 | 방법 | NIONS | ENCUT | k (Γ) | SIGMA | 재시도 |
|---|---|---|---|---|---|---|---|---|
| P | `P2S_S_A_bound` | sample | pbed3 | 398 | 520 | 3×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| P | `P2S_S_A_far` | sample | pbed3 | 398 | 520 | 3×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 1 | `P2S_Li_A_bound` | sample | pbed3 | 362 | 520 | 3×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 1 | `P2S_Li_A_far` | sample | pbed3 | 362 | 520 | 3×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 1 | `P2S_S_A_p05_bound` | sample | pbed3 | 398 | 520 | 3×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 1 | `P2S_Li_A_p05_bound` | sample | pbed3 | 362 | 520 | 3×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 2 | `P2S_S_A_G3_c2_bound` | g3 | pbed3 | 398 | 520 | 3×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 2 | `P2S_S_A_G3_c2_far_i` | g3 | pbed3 | 398 | 520 | 3×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 2 | `P2S_S_A_G3_c2_far_ii` | g3 | pbed3 | 398 | 520 | 3×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 2 | `P2S_S_A_G4_k62_bound` | g4 | pbed3 | 398 | 520 | 6×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 2 | `P2S_S_A_G4_k62_far` | g4 | pbed3 | 398 | 520 | 6×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 2 | `P2S_S_A_G4_k62s2_bound` | g4 | pbed3 | 398 | 520 | 6×2×1 | 0.025 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 2 | `P2S_S_A_G4_k62s2_far` | g4 | pbed3 | 398 | 520 | 6×2×1 | 0.025 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 2 | `P2S_S_A_G4_e650_bound` | g4 | pbed3 | 398 | 650 | 3×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 2 | `P2S_S_A_G4_e650_far` | g4 | pbed3 | 398 | 650 | 3×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 3 | `P2S_S_A_optB88_bound` | optb88 | optb88 | 398 | 520 | 3×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 3 | `P2S_S_A_optB88_far` | optb88 | optb88 | 398 | 520 | 3×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 3 | `P2S_Li_A_optB88_bound` | optb88 | optb88 | 362 | 520 | 3×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 3 | `P2S_Li_A_optB88_far` | optb88 | optb88 | 362 | 520 | 3×2×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| P | `CC_S33_AB_optB88_bound` | cc | optb88 | 12 | 520 | 18×18×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| P | `CC_S33_AB_optB88_far` | cc | optb88 | 12 | 520 | 18×18×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 4 | `CC_S33_AB_pbed3_bound` | cc | pbed3 | 12 | 520 | 18×18×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| 4 | `CC_S33_AB_pbed3_far` | cc | pbed3 | 12 | 520 | 18×18×1 | 0.050 | 0 → r1 ⓐ+ⓑ → r2 ⓑ |
| P | `V5_s_outer_A_G4_e70_far_a4` | a4 | v5 | 200 | 650 | 3×2×1 | 0.136 | ⓐ+ⓑ 한 번 |

## 돌리는 법
1. **파일럿 (단계 P · 5 잡) 먼저**: `VASP_CMD="mpirun -np <N> vasp_std" POTCAR_DIR=<PAW_PBE> VDW_KERNEL=<vdw_kernel.bindat> bash run_all.sh`
   (STAGES 기본값 = P). 끝나면 `round2_return.tgz` + `.sha256` 을 보내 주세요 — 우리가 파일럿을 검사해 **등록부를 봉인**하고 **해제 파일**을 보냅니다.
2. 해제 파일을 받으면: `STAGES="1 2 3 4" RELEASE_FILE=<받은 파일> RELEASE_SHA256=<메일의 sha256> VASP_CMD=… POTCAR_DIR=… VDW_KERNEL=… bash run_all.sh`
   — 파일럿 잡은 다시 돌지 않습니다 (시도 폴더가 있으면 기록을 다시 판정만 합니다).
3. **재시도는 러너가 미리 정한 대로만** 합니다 (탄소 잡: 단 0 → r1 ⓐ (쌍극 퍼텐셜 보정 끔 · WAVECAR 남김) → r1 ⓑ (보정 켬 · ⓐ WAVECAR 에서 · AMIN 0.01) →
   r2 ⓑ (혼합 AMIX 0.1 · BMIX 0.01 · AMIN 0.01 · 같은 ⓐ WAVECAR) / 은 a4: ⓐ+ⓑ 한 번). 다음 단은 **확인된 미수렴 · 실행 실패**일 때만입니다.
   그 밖 (SCF 미확인 · ⓐ 자격 미달 · 재시작 미이행) 은 멈추고 기록만 남깁니다 — **다른 설정으로 더 돌리지 마세요.**
4. **ⓐ 의 WAVECAR 는 지우지 마세요** — 러너가 그 잡이 끝날 때 지웁니다 (반송하지 않습니다 · sha·크기·머리만 기록).
5. 0 스텝 인프라 중단 (스케줄러 취소 등으로 전자 반복 0 회) 이면: `WALL_S=<초> bash run_all.sh --infra-abort <잡> <단> <스케줄러 잡 id> <취소 UTC> <사유>` 로
   기록한 뒤 다시 돌려 주세요 (잡마다 2 회까지). `WALL_S=<초>` (스케줄러 장부의 그 시도 벽시계) 를 꼭 주세요 — 그 시간도 누적 상한 장부에 들어갑니다.
   초는 0 이상의 10진 정수로 적어 주세요 (선행 0 없이 · 9 자리 이하 — `7200` 은 되고 `07200` · `7200s` 는 거부합니다 · 종료 2).
   모르면 UNKNOWN 으로 남고, 그 뒤 잡은 `bash run_all.sh --infra-wall <run_aborted 폴더 이름> <초>` 로 장부 값을 채울 때까지 뜨지 않습니다 (종료 5).
   OSZICAR · stdout.log · OUTCAR 어디에든 전자 반복 흔적이 있으면 이 기록은 거부합니다.
   **전자 스텝이 돈 뒤 러너째 끊긴 시도** (스케줄러 시간 제한 · 노드 고장 — 그 시도 폴더에 `attempt.json` 이 없다) 는 다시 돌리지 않습니다 (값 없음 · 1저자 결정).
   러너는 그 벽시계를 모르므로 다음 잡을 띄우지 않습니다 (종료 5) — `WALL_S=<초> bash run_all.sh --killed <잡> <단> <스케줄러 잡 id> <취소 UTC> <사유>` 로
   스케줄러 장부 값을 기록한 뒤 다시 돌려 주세요. (VASP 가 스스로 오류로 끝난 실행 실패는 러너가 기록하고 정해진 사다리대로 다음 단으로 갑니다.)
6. **누적 상한**: 단계마다 P 117 h · 1 170 h · 2 586 h · 3 204 h · 4 24 h · 전체 1080 h (한 노드 벽시계 합 · 파일럿 뒤에는 해제 파일의 값). 넘으면 러너가 다음 잡을 띄우지 않고 멈춥니다 (종료 5) —
   돌던 잡은 끝까지 돕니다. 반송해 주시고 결정을 기다려 주세요.
7. **공통 환경 고장 = 전체 정지** (종료 6): VASP 빌드 · POTCAR · vdW 커널 파일이 파일럿에서 봉인한 것과 다르거나, optB88 잡에 커널이 없을 때.
   POTCAR 는 VASP 를 띄울 때마다 (끊긴 뒤 이어 돌릴 때도) 다시 확인합니다. 해제 파일의 상한 값이 양수가 아니면 시작하지 않습니다 (종료 2).
8. 성능 태그는 `PERF_TAGS_FILE` 로만 (V5 와 같은 규칙) — **INCAR · POSCAR · KPOINTS 는 고치지 마세요.** ⓐ·ⓑ 는 같은 랭크·NCORE·KPAR 로 돌려야 합니다 (NBANDS 가 같아야 WAVECAR 를 읽는다).
9. 반송 묶음은 러너가 허용 목록만 담습니다 (POTCAR 본문 · WAVECAR · CHGCAR · vdw_kernel.bindat 는 넣지 않습니다). 포장이 실패하면 (종료 4) `PACK_ONLY=1 bash run_all.sh`.
   보내는 것: 종료 0 · 1 · 5 · 6 뒤 `sha256sum -c round2_return.tgz.sha256` 까지 통과한 쌍.
10. 지원 환경: Linux · bash ≥ 4 · GNU coreutils (find sort grep cmp sha256sum od stat) · GNU tar · awk.

## VASP · POTCAR · vdW 커널
- **VASP**: V5 와 같은 빌드 (vasp.5.4.4.18Apr17-6-g9f103f2a35) — 은 a4 는 반드시 같은 빌드·같은 PP 여야 합니다.
- **POTCAR** PBE_54: Li_sv · P · S · Cl · Ag (V5 와 같은 파일) + **C** (`PAW_PBE C 08Apr2002` 예상 — 보유본으로 확인 · 파일럿 뒤 봉인).
- **optB88-vdW**: `vdw_kernel.bindat` (VASP 5.4.4 배포본) 경로를 `VDW_KERNEL` 로 주세요. 러너가 sha256 · 크기를 기록합니다 (파일럿 뒤 봉인).

## 돌려받을 것
`round2_return.tgz` + `.sha256` — 시도마다 OUTCAR · OSZICAR · INCAR · KPOINTS · POSCAR · IBZKPT · POTCAR.titel · POTCAR.sha256 · POTCAR.species.sha256 · attempt.json · stdout.log · WAVECAR.info · warn.log · infra_abort.json · LOCPOT.zavg.txt · attempt.start · killed.json (있는 것만) · `run/status.tsv` · `run/env.txt` · `run/infra_aborts.tsv` · `MANIFEST.sha256`.
VASP 빌드 · 노드/코어 · **잡별 peak RSS · 벽시계** 를 `run/env.txt` 에 한 줄씩 덧붙여 주세요.

## English summary
24 jobs; 25 VASP executions when nothing fails (the silver a4 job is a two-stage run), up to 94 under the registered retry ladder, excluding separately
recorded infrastructure retries. All are single-point SCF runs (no relaxation) on fixed geometries, in stages: P (pilot: 5 jobs) first, then 1–4 only after
we send a release file.
Carbon jobs: Gaussian ISMEAR 0, SIGMA 0.05 eV (0.025 eV for one check), ENCUT 520 eV (650 eV for one check), PBE+D3(BJ) with explicit parameters, or
optB88-vdW (GGA = BO, PARAM1/PARAM2, AGGAC 0, LUSE_VDW, Zab_vdW, IVDW 0; needs vdw_kernel.bindat via VDW_KERNEL). Dipole correction along z.
The runner applies a pre-registered retry ladder automatically (rung 0 → r1 stage A without dipole potential correction, then stage B restarting from that
WAVECAR with AMIN 0.01 → r2 stage B with AMIX 0.1/BMIX 0.01/AMIN 0.01); the silver a4 job is a single two-stage run. Convergence is judged from the last
electronic row of OSZICAR (|dE| and |d eps| ≤ EDIFF), never from OUTCAR wording. Please do not edit INCAR/POSCAR/KPOINTS, do not delete stage-A WAVECARs,
and do not rerun anything by hand; record zero-step infrastructure aborts with WALL_S=<scheduler wall seconds> and --infra-abort (seconds as a plain
decimal integer without leading zeros; an unknown wall time
is recorded as UNKNOWN and holds the next job until --infra-wall fills it from the scheduler log); a run killed after electronic steps (no attempt.json) is not
retried and holds the next job until its scheduler wall time is recorded with WALL_S=<seconds> --killed. Cumulative wall-time caps stop the runner (exit 5);
a VASP build, POTCAR or vdW-kernel change stops everything (exit 6). Return the round2_return.tgz pair after `sha256sum -c`.
