# Session Timelog — 2026-06-04/05 (multi-track)

> 여러 트랙 동시 진행으로 헷갈림 방지용 전체 스냅샷. 머신별·트랙별 상태.
> 마지막 갱신: 2026-06-05 (작업 중)

## 머신 / 트랙 맵

| 머신 | 트랙 | GPU |
|---|---|---|
| **v100** (container 915bdbbd37ca) | comp1_v3 properties 재계산 (k-mesh 사고 복구) | 1× 32GB |
| **kserver116-27** (=gabia) | LiNiO₂ DFT+U, Li3N DFT drag | 1× A6000 48GB |
| **KISTI glogin01** | Nd-doped modelc relax (job 748804) | amd_a100nv_8 |
| (로컬 repo) | DB/문서 갱신 | — |

---

## 트랙 1: comp1_v3 (LPSCl) — k-mesh 사고 복구 + properties 재계산

### 사고 요약
- **comp1 기존 DFT 전부 k=2×2×1 (k×L=10 Å, 4배 부족)** — V0 relax, elastic, LOBSTER, DOS 모두 오염
- 발견 경위: DOS gap 1.50 eV가 literature PBE(2.15-2.45)보다 과소 → k-mesh 확인 → 2×2×1 발각
- modelc(6×6×3, k×L=42)는 영향 없음
- **methodology 문서 구멍**: "tight SCF"를 conv_thr+ecutrho로만 정의, k-mesh 미명시 → `argyrodite_mechanical_pipeline.md` Step7에 k×L≥40 기준 추가함
- 추가 발견: comp1 ecut도 52/520 (modelc 60/480과 다름) → **EOS와 일치 위해 52/520 유지**로 결정

### k444 재계산 결과 (52/520, 4×4×4, paper-grade)
| property | 상태 | 값 |
|---|---|---|
| V0 re-relax | ✅ | force 0.0066 eV/Å (이전 2×2×1 잔류 0.26의 1/40). **RMS 변위 vs old 0.003 Å — geometry 거의 안 바뀜, 오염은 전자/탄성** |
| bonds | ✅ | Cl 전부 4a (ordered), Li-Cl 2.607, Li-S(PS4) 2.511, Li-S(4d) 2.362, P-S 2.072 |
| coord/Voronoi/per-site | ✅ | Li env 1종 (완전대칭), Cl 4a×4 4d×0 |
| BVSE | ✅ | bvse_k444/ |
| Bader (AE plot_num=17) | ✅ | Li +0.874, Cl −0.925, S −1.518, P +3.270 (Li/Cl modelc와 일치; P/S 차이 — modelc 동일방법 재확인 필요) |
| DOS/gap | ✅ | **gap 1.76** (이전 1.50은 k artifact). modelc 1.82와 ≈동일 → gap은 조성 둔감. VBM S3p 91%, CBM S3p+P3s |
| LOBSTER ICOHP | ✅ | spilling **1.46%**. P-S −5.94, Li-Cl −1.86, Li-S −1.59, S-S −0.11. 4d-S²⁻ −2.57 (=modelc −2.52, universal anchor). **k444가 기존 bonds.json 값 검증 (ICOHP k-둔감)** |
| AIMD Arrhenius | ✅ | **Ea=0.172 eV, R²=0.999** (800K 재실행으로 fluke 해결). [2,50] window |
| elastic Cij (relaxed-ion) | ⏳ **밤샘 진행** | k444 12 strain relax. K_POINTS shift 버그(0 0 0 누락) sed로 수정 후 재실행. → E_VRH (vacancy paradox 재검증) |
| ELF | ⏳ 진행 | ONCV 80/320 SCF + pp.x plot_num=8 |
| bands | ⏳ 진행 | NSCF k-path (GXMGRX,MR) + bands.x, DOS density 재사용 |
| MLIP 600K 탄성 | 🔲 상태 확인 | mlip_600K_snapshot/ |

### comp1 AIMD vs modelc (둘 다 [2,50], R²~0.99)
- comp1 (LPSCl): **Ea=0.172**, D600=2.68e-6, D800=5.91e-6, D1000=1.02e-5
- modelc (LPSCl1.6): **Ea=0.224** (R²0.99), D600=7.90e-6, D800=2.05e-5, D1000=4.55e-5
- 메커니즘: comp1 barrier 낮음, modelc 빠름(prefactor↑=vacancy carrier). 둘 다 문헌 bulk 범위 (LPSCl 0.16-0.25, Cl-rich Schlem2020 0.22)

---

## 트랙 2: kserver — LiNiO₂ DFT+U (SDCP binding 검증)

- **목적**: SDCP binder anchoring DFT 검증 (MLIP Phase A-C 완료: doped −18 eV vs neutral −6.3 eV)
- **문제**: LiNiO₂ Ni³⁺ 자성 SCF 발산 (abs_mag 52 high-spin, 3일 막힘)
- **원인**: U=6.2는 있었으나 starting_mag±0.3 약함 + beta0.3 공격적
- **해결책 (작동 확인)**: `tot_magnetization=0` (AFM 강제) + starting_mag±1.0 + beta0.1 + degauss0.02 → total_mag→0 ✓, abs_mag 52→34.6 하강 (24 목표 수렴 궤도)
- **사고들**: ① libgomp:TODO (conda env가 nvhpc QE 충돌 → run_dft_neb.sh의 nvhpc HPCX env로 해결) ② ecutrho 600 OOM (Li3N drag와 동시) → 480으로 낮춤
- **현재**: ecutrho 480 단독/재시작 필요 (Li3N drag와 메모리 경쟁). 자성 fix는 검증됨
- 입력: reference_dft_v2/scf.in (U6.2, tot_mag=0, calc=scf single-point)

## 트랙 3: kserver — Li3N adatom 확산 (anode 계면)

- **목적**: Li3N(001) 표면 Li adatom 확산 barrier (레퍼런스 Cui ACS Nano 2023 = 0.133 eV)
- **LiC6는 성공**: UMA NEB 0.241 eV (깨끗, graphene 비활성)
- **Li3N는 UMA 실패 (6가지 시도 전부)**: adatom이 Li3N에 과결합(incorporation −1.5~−3.3 eV) → 표면확산 NEB 붕괴. rigid만 깨끗(0.786, 과대). = UMA-oc20의 Li3N lithiophilicity 과대평가 (레퍼런스 핵심 주장과는 일치)
- **해결책 = DFT drag** (레퍼런스 방법): adatom xy 9점 고정 + 기판 relax → dive 불가. `tools/neb_diffusion/dft_drag.py` 작성
- **현재**: drag p0 진행 중 (relax, 느림 — 점당 오래). 9점 = 길 수도. 너무 느리면 `--mode rigid`로 전환 검토
- adatom 결합 −1.9 eV(vs bulk)≈−3.5(vs atom)≈레퍼런스 −3.44 ✓

## 트랙 4: KISTI — Nd-doped modelc relax (job 748804)

- **목적**: Nd-doped LPSCl1.6 EOS V0 DFT relax (nat=120, Nd 4f AFM, U Nd-4f 8.0)
- **한 달 묵은 문제 원인 발견**: `relax_run4.in`이 `restart_mode='from_scratch'`로 이전 relaxation 무시하고 처음부터 → 첫 SCF 발산 (iteration #*** 2000+, beta0.05)
- **진짜 진행분**: `relax.out`이 **BFGS 29 step** 갔음 (relax_run4.out은 0). tmp/에 BFGS29 charge density 살아있음 (126MB)
- **수정 중**: relax.out의 BFGS29 최종좌표를 텍스트로 추출(ASE는 Nd1/Nd2 못 읽음) → relax_run4.in ATOMIC_POSITIONS에 주입 → 좌표+density 일치하면 from_scratch여도 빨리 수렴
- **SLURM**: 748804 PENDING (amd_a100nv_8, 65 대기, 예상시작 6/6 13:18, 2일 walltime, 2 GPU). 좌표 주입 후 재제출 예정

---

## 즉시 할 일 (다음 세션 시작점)

1. **KISTI**: relax_run4.in 좌표 주입 검증 → `scancel 748804; sbatch sbatch_run4_fresh.sh`
2. **v100**: elastic 12/12 → `fit_elastic_cij_stress.py` → E_VRH (vacancy paradox). ELF/bands plot
3. **kserver**: LiNiO₂ ecutrho480 단독 재시작 (Li3N drag와 순차) / Li3N drag 진행도 (느리면 rigid)
4. **DB**: elastic 결과 → elastic.json, ELF/bands → 비교 md

## 도구 (이번 세션 작성/수정)
- `tools/modelc_v3/plot_dos.py` — DOS+PDOS, gap+orbital character (paper-grade)
- `tools/modelc_v3/analyze_defect_band.py` — per-atom PDOS in E window
- `tools/comp1_v3/kconv_scan.py` — k 수렴 스캔 (E/atom, stress 비등방)
- `tools/neb_diffusion/adatom_diffusion.py` — binding-site discovery + CI-NEB (--rigid/--constrain_z)
- `tools/neb_diffusion/dft_drag.py` — DFT drag scan (레퍼런스 방법)
- ⚠ `build_elastic_strain_inputs.py`, `build_lobster_paw_inputs.py` — `--kpoints` shift(0 0 0) 누락 버그 (sed 우회 중, 나중에 고칠 것)
