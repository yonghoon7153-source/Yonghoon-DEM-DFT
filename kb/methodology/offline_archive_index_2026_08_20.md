---
title: "오프라인 백업 인덱스 — repo 밖에 있는 원자료가 어디 있나"
date: 2026-08-20
updated: 2026-08-20
tags: [archive, backup, provenance, raw-data, cube, aimd, lobster, kisti]
status: 실측 인덱스 (2026-08-20 전수조사)
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-20
verifiedBy: 전수조사 find (WSL /mnt/d) — 위치·크기만. 파일 내용·해시는 미확인
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: multi-source-primary
---

# 오프라인 백업 인덱스

> **왜 있나**: repo 는 **파생물**(csv·json·png)을 담고, **원자료**(cube·궤적·LOBSTER)는
> 용량 때문에 밖에 있다. 그 위치가 지금까지 **사람 머릿속에만** 있었고, 그래서
> `canonical_registry` 의 `provenance_open` 4건이 *"값은 맞는데 그 값을 만든 실행을
> 파일로 재현할 수 없다"* 로 떠 있었다. 이 카드가 그 연결을 만든다.
>
> ⚠ **이 카드는 목록이지 백업이 아니다.** 외장 SSD 하나에만 있으므로 **단일 실패점**이다
> (§4 참조).

## 0. 백업 두 벌 — 위치와 성격

| | 경로 (WSL) | 시점 | 용량 | 성격 |
|---|---|---|---|---|
| **A** | `/mnt/d/v100/kisti_backup_2026-07-14/` | 2026-07-14 | **47 GB** | KISTI 홈 전체 스냅숏 |
| **B** | `/mnt/d/v100, kisti 백업/` | 2026-06-11 | — | 그 이전 판 (runs 중심) |
| — | `/mnt/d/v100/li3n_drag_backup/` | — | 9.7 MB | Li₃N drag DFT 로그 |

물리 매체: **T7 Shield (D:)** 외장 SSD. Windows 경로 `D:\v100\...`.

## 1. ⭐ 백업 A — KISTI 스냅숏 (2026-07-14)

```
kgy_b2o3_eos_2026-07-14/b2o3_eos/     ← ⭐ b2o3 전자구조 원자료
kgy_lpsocl_eos_2026-07-14/lpsocl_eos/
kgy_lpscl16_site_pref_2026-07-14/
kgy_nd_doped_modelc_2026-07-14/nd_doped_modelc/1_enumerate/enum_run/
kgy_md_results_2026-07-14/md_results/
kgy_SEI_2026-07-14/SEI/
kgy_manuscript_support_2026-07-14/manuscript_support/
kgy_projects_2026-07-14/ · kgy_repo_2026-07-14/ · kgy_repo_dos_2026-07-14/
kgy_pseudo_2026-07-14/pseudo/         ← UPF 90 + upf 51
home_scripts_ · kgy_root_scripts_ · lpsocl_eos_final/
```

### 1-1. ⭐⭐ `b2o3_eos/` — **여기에 커밋 안 된 cube 가 다 있다**

| 파일 | 크기 | 무엇 |
|---|---|---|
| `b2o3_elf.cube` | 116 MB | **ELF** — `kb/results/b2o3_elf_covalency_2026_07_02.md` 가 *"cube KISTI, 커밋X"* 라 적은 그것 |
| `b2o3_cdd.cube` | 124 MB | charge density difference |
| `b2o3_rho_scf.cube` · `b2o3_rho_atomic.cube` | 116 MB ×2 | CDD 의 두 항 |
| `b2o3_chg.cube` | 116 MB | 전하밀도 |
| `BvAt0074`–`BvAt0128.cube` | 116 MB ×55 | **Bader 원자별 부피** |

⇒ **ELF 평면 재렌더 · VESTA 3D · Bader 재계산이 전부 여기서 가능**하다.
repo 의 `docs/figures/paper/elf_plane_b2o3_*.png` (라벨 없는 clean 판 5장)가 이 cube 산출물.

### 1-2. ⭐ `md_results/` (761 MB) — **comp1 1×1×1 + 2×2×2 궤적 세트다**

초판은 *"시드 표기 없는 다른 계열"* 로만 적었다. 원자 수를 세어 정정한다 (2026-08-20):

| 파일 | 원자 | Lattice a | 계 | 프레임 |
|---|---|---|---|---|
| `ToBeDelete_md_{600,800,1000}K.{xyz,traj}` | **52** | 10.12 Å | **comp1 1×1×1** | 2500 |
| `ToBeDelete_md_{600,800,1000}K_v2.{xyz,traj}` | **416** | 20.24 Å | **comp1 2×2×2** | 2500 |
| `ToBeDelete_msd_*K{,_v2}.dat` | — | — | MSD + D | `T=800K D=2.332e-05 cm²/s R²=0.9884` |

⭐ **같은 계·같은 세 온도의 1×1×1 과 2×2×2 궤적이 둘 다 있다** (52×8 = 416).
이게 왜 값이 큰가:

1. **codex_A A-R4 가 지적한 "416원자 1런"** 의 **궤적 실물**이다.
2. **셀 크기 효과를 직접 볼 수 있다** — 같은 계·같은 온도·다른 셀. 우리가 여러 번 논쟁한 축이고
   문헌(Zhang npj Li₃YCl₆ 소형 vs 대형 σ)과 나란히 놓을 수 있는 유일한 자체 데이터다.
3. **comp1 골격 게이트를 잴 수 있다.** comp1 은 Li β 0.17–0.79 로 확산 게이트를 떨어진 계인데
   **골격(비-Li)은 한 번도 안 봤다.** 궤적이 있으므로 `msd_diffusive_check --framework
   --from_traj` 가 그대로 먹힌다. ⛔ 그때 **`--mto` 를 반드시 쓸 것** (§3 주의).

⚠ **`ToBeDelete_` 접두사가 붙어 있다.** 761 MB 자산에 "지울 것" 딱지가, 그것도 **유일본**
백업에 붙어 있다. 이름을 바꾸거나 최소한 이 카드가 그 사실을 기록해 둔다.

### 1-2b. ⚠ highT_reseed 는 여전히 **없다**

`md_results` 가 comp1 이므로 **b2o3/modelc 의 800/1000 K reseed 궤적은 백업에도 없다.**
kgy repo 루트의 `b2o3_traj.xyz`(160원자, c축 87 Å) · `modelc_traj.xyz`(94원자, c축 58 Å)도
**슬랩**이다(`move_mask` 있음, 진공층) — 벌크 MD 가 아니다.
⇒ **F9 의 재실행 판단이 유지된다** (2026-08-20, 백업 2벌 + kgy + gabia 전수 확인).

⚠ 확인된 위양성 후보를 기록해 둔다 — 다시 헷갈리지 않도록:
`kgy ~/work/runs/{iface_roll,interface_campaign}/*_traj.xyz`(계면 캠페인) ·
`{lpsocl_600_long,mto_pilot}/**/T{500,700,900}/traj.xyz`(다른 온도) ·
`gabia /root/work/committee_modelc_T*/snapshots.xyz`(committee 스냅숏).

## 2. ⭐ 백업 B — runs 중심 (2026-06-11)

### 2-1. AIMD 궤적 — **repo 에 없는 자산**

| 파일 | 크기 |
|---|---|
| `runs/comp1_v3/aimd_5fu/T{600,800,1000}K/traj.xyz` | 10.6 MB ×3 |
| `runs/comp1_v3/aimd_5fu/T800K_seed1_fluke/traj.xyz` <!-- lint-skip-path: 오프라인 백업 경로 (repo 아님) --> | 10.6 MB |
| `runs/comp1_v3/aimd_5fu/T*_short_12ps/traj.xyz` | 1.07 MB ×3 |
| `runs/modelC_v3/aimd/T{600,800,1000}/traj.xyz` | 10.2 MB ×3 |
| 같은 경로의 `traj.traj` (ASE) | 4.4–4.6 MB |

⭐ `modelC_v3/aimd/T600/traj.traj` 가 **PMF provenance 가 가리키는 그 파일**이다
(`db/properties/modelc_pmf_*_T600_origin.csv` 헤더: *"runs/modelC_v3/aimd/T600/traj.traj
(1000 frames, prod 100 ps, dt 2 fs, save 100 fs)"*).

⚠ **`T800K_seed1_fluke`** — 이름이 판정을 담고 있다. 인용 전 그 이유를 확인할 것.
⚠ **`*_short_12ps`** — 12 ps 판이 따로 있다. 문헌의 "20 ps AIMD" 와 같은 체급이고,
  우리가 그 길이로도 돌려봤다는 기록이다 (§6 문헌 대비 논증에 쓸 수 있다).

### 2-2. LOBSTER / Bader — ICOHP 원자료

```
runs/modelC_v3/COHPCAR.lobster · COOPCAR · COBICAR · bandOverlaps.lobster (8.9 MB)
runs/modelC_v3/lobster_ext/ (같은 4종)
runs/comp1_v3/v3_post/k444_props/lobster_ext/ (같은 4종, bandOverlaps 5.8 MB)
runs/modelC_v3/BCF.dat  ·  runs/comp1_v3/archive_v2_post/post_v2/BCF.dat
```

⇒ `db/properties/bonds.json`(modelc ICOHP −5.9997) 의 **원자료가 여기**다.

### 2-3. 큰 cube

```
runs/modelC_v3/V0_AEdens.cube            58 MB
runs/modelC_v3/V0_ELF.cube               28 MB
runs/comp1_v3/v3_post/k444_props/V0_AEdens.cube   39 MB
runs/comp1_v3/.../elf/V0_ELF.cube        23 MB
runs/comp1_v3/archive_v2_post/post_v2/comp1v2_charge.cube  32 MB
runs/bvse_cubic_5x5x5/{comp1,modelc}_5x5x5*/V0_BVSE.cube   14 MB ×2
work_misc/bvse_5x5x5_compare/ · bvse_5fu_compare/          (같은 것 사본)
```

⚠ **BVSE 5×5×5 cube** — CLAUDE.md 규율상 *"정량·순위는 원본 주기셀 값만"* 이고
큐빅 박스는 **표시용**이다. 이 파일들이 그 큐빅 박스 쪽이다.

### 2-4. anneal 궤적

```
runs/ens_anneal_s1–s5/anneal.traj        1.78 MB ×5
runs/anneal_0000_o{001,010,019,022}/ · anneal_0005_o007/
runs/b2o3_anneal/anneal.traj             174 KB
```

### 2-5. 그 외 디렉터리

`b2o3_dft3` · `b2o3_dft3_run` · `b2o3_Odist_cfg{0000,0005,0010,0019}` ·
`b2o3_stage{0,1,2}` · `ens_eos_s1–s5` · `comp1_v3/{eos,anneal,elastic_mlip_600K,
disorder_diffusion,archive_v2_post,v3_post}` · `modelC_v3/{dos_pdos,elastic_relaxed_ion,
elastic_static,elastic_mlip_600K,elastic_mlip_600K_clamped_backup}`

⭐ **`elastic_relaxed_ion/` 과 `elastic_mlip_600K_clamped_backup/` 이 나란히 있다** —
우리 규율 *"paper 값은 relaxed-ion 만 (clamped 2.3× 과대)"* 의 **양쪽 원자료**다.

## 3. 이 인덱스로 닫을 수 있는 미결

| 미결 | 후보 위치 | 확인 방법 |
|---|---|---|
| ✅ `gap_eV/b2o3` | 백업 A `b2o3_eos/b2o3_nscf_gap.{in,out}` | **해소** — VBM 2.4717 / CBM 4.4388 정본 일치 |
| ✅ `gap_eV/lpsocl` | **kgy** `~/work/lpsocl_v0/03b_nscf_gap.{in,out}` | **해소** — VBM 2.3870 / CBM 4.6179 정본 일치 |
| ⛔ `gap_eV/comp1` · `gap_eV/modelc` | **어디에도 없음** | 백업 2벌 + kgy + gabia **3중 수색 실패**. KISTI 원본 부재 ⇒ **영구 미해소**로 본다 |
| ELF cube 커밋 안 됨 | 백업 A `b2o3_eos/b2o3_elf.cube` | VESTA·재렌더 필요 시 여기서 |
| ICOHP 원자료 | 백업 B LOBSTER 4종 | — |
| PMF 궤적 원본 | 백업 B `modelC_v3/aimd/T600/traj.traj` | — |
| clamped vs relaxed-ion 대조 | 백업 B `elastic_*` 두 폴더 | — |

**2026-08-20 수색 종료.** 4건 중 **2건 해소 · 2건 영구 미해소**로 닫았다.
⚠ comp1·modelc 를 다시 찾지 말 것 — 백업 2벌·kgy·gabia 를 이미 전수로 훑었고,
같은 조사에서 b2o3·lpsocl 은 **찾았으므로** 수색 방법 자체는 유효했다.
가짜 후보 둘을 기록해 둔다: gabia `/root/comp1_cdd_phx/nscf.out`(gap 2.0654, **CDD용 별개
계산** — 정본 2.066 과 4자리 불일치) · `runs/{comp1,modelc}_eps/nscf.in`(**유전율용**).

## 4. ⚠ 한계 (지우지 말 것)

1. ⛔⛔ **단일 매체이자 유일본이다.** T7 Shield 외장 SSD 한 벌뿐이고 사본이 없다.
   **그리고 2026-08-20 확인 — KISTI 원본은 남아 있지 않다** (1저자). 즉 이 백업은
   *사본*이 아니라 **그 계산들의 마지막 실물**이다. 디스크가 죽으면 b2o3 ELF/CDD/Bader
   cube · AIMD 궤적 · LOBSTER 원자료가 **전부 소실**된다. 이중화가 필요하다.
2. **repo 가 이 인덱스를 검증하지 못한다.** 경로가 로컬 Windows 마운트라 CI·validator 가
   못 본다 — 파일이 옮겨지거나 지워져도 **이 카드는 조용히 낡는다.**
3. **해시가 없다.** 무결성 확인을 안 했다. 인용 전에는 해당 파일의 sha256 을 재서
   그때의 산출물과 대조해야 한다 (지금은 "있다" 까지만 확인됨).
4. **깊이 3 까지만 훑었다.** 하위 디렉터리에 더 있을 수 있다.
5. 확장자 통계의 `stl 407` · `liggghts 211` 은 **DEM 쪽 자산**이라 이 카드 범위 밖이다.
6. ⛔ **β 를 잴 때 잣대를 밝히지 않으면 이 카드의 궤적들이 무의미해진다.** kgy `arr6close`
   실측: 같은 궤적에서 **STO β 0.07–0.91 이 널뛰는데 MTO 는 0.73–0.79 로 안정**하다
   (lpsocl_new T600 s2/s3/s4). 600 K 에서 **STO/MTO 부호가 뒤집힌 사례**도 있다.
   ⇒ 이 카드의 어느 궤적으로든 β 를 잴 때 **`--mto` 를 빼지 말 것.**
   레지스트리: `db/properties/lpsocl_beta_registry.json`

## 관련

- 실측: 2026-08-20 전수조사 (`find` 기반, WSL `/mnt/d`)
- 소비처: `db/properties/canonical_registry.json` (`provenance_open` 4건) ·
  `kb/results/b2o3_elf_covalency_2026_07_02.md` (cube 커밋X 명시) ·
  `db/properties/modelc_pmf_*_T600_origin.csv` (traj.traj provenance)
- F9 판정: `kb/reviews/codex_C_funnel_2026_08_20.md` ·
  `kb/projects/decision_registry_design_2026_08_20.md`
