# Codex 전수 스윕 회신 (2026-08-12)

핸드오프 ZIP SHA-256 **7139E285…DBAE17 검증 일치 ✓** · 기준 `4b56bcbf`.
검증 환경: 클라우드 컨테이너 (SciPy 있음, taichi/GPU 없음).

---

## 1. Codex RUNGS 실행 결과 — **7개 전부 실행** (미실행 0)

`codex_method_discipline_rungs_20260812.py` 를 SciPy 환경에서 그대로 로드해 돌렸다.

| rung | 결과 | 값 |
|---|---|---|
| `fibre_segment_raster.segment_cells` (reversal at signed boundary) | **FAIL** | forward 14 · reverse 12 · **symdiff 4** |
| `step3_sigma.solve_sigma_z` (oblique staircase) | PASS | σ=0.05 = exact |
| `step3_sigma.pore_tau` (oblique staircase) | PASS | D_rel 0.01667 · τ 2.778 = exact 1/60, 25/9 |
| `step3_sigma.am_surface_patches` (oblique staircase) | PASS | faces 18 · reaction 0.0556 |
| `voxel_conductivity.effective_sigma` (oblique staircase) | PASS | σ=0.05 = exact |
| `voxel_conductivity._densify_fibres` (oblique 3-4-12) | PASS | n=14 · gap 1..1 |
| `comsol_export.build_contacts` (oblique pair) | PASS | n=1 · δ 0.5 · a_hertz 1.2247 |

⇒ **6 PASS / 1 FAIL.**  미실행 0 건.  FAIL 1 건은 아래 #8 로 수정 완료.

---

## 2. intentional errors 판정 (9건)

| # | 항목 | 판정 | 근거 (실코드 좌표 + 실행) |
|---|---|---|---|
| **1** | `network_conductivity` thermal mode 미전달 | **CONFIRMED** | `network_conductivity.py:938-940` 의 `build_network(...)` 호출에 **`mode=` 인자가 없다** → 기본 `mode='ionic'` 고정.  `:166` 이 선언한 `mode='thermal'`(ALL contacts) 경로와 `:317-320` 의 `k_weight` 분기가 **프로덕션에서 실행되지 않는다** |
| **2** | `pore_tau.eps_connected_pct` 가 either-plate | **needs-runtime** | `:776-777` `100·res['n_dof']/s.size` 로 **DOF 수의 함수**다.  `:798` 독스트링은 "both-plate percolation" 이라 선언한다.  어느 쪽인지는 `_solve_diffusion` 의 DOF 선택을 실행해 봐야 갈린다 — 격자 픽스처 1개면 CPU 로 판정 가능 |
| **3** | `mpm3d` coverage 가 x/y/z 무조건 wrap | **CONFIRMED** | `mpm3d_compaction.py:3230,3232` `np.roll(pin_c, s, ax)` / `np.roll(occ_c, s, ax)` — periodic 여부와 무관하게 세 축 전부 toroidal.  **미수정** (§4) |
| **4** | DEM `tol_am_um` 대응 규약 부재 | **CONFIRMED** | STEP3 `rasterize` `tol_am_um=0.10`(`:185`) · econn 동일(`payload:114`) · `comsol_export.TOL_AM_UM=0.10`(`:52`) 셋은 같으나, **DEM 접촉망은 LIGGGHTS dump 의 `ca>0 or delta>0`**(`network_conductivity.py:230,237`) = **δ>0(겹침)** 이다.  "0.10 µm proximity 와 같은 계약" 은 성립하지 않는다.  S1a 실측 초과 간선: real14 **+12.3 %**(587→659) · 킷 +7.6~16.0 % |
| **5** | `viz_se_voxel_2d` AM_P/AM_S 반전 | **CONFIRMED → 수정** | `rasterize` 는 **DEM type 규약**을 받는다 (`step3_sigma.py:233` `2 if am_t[i]==1 else 1` = type 1 → sid 2).  viz `:87` 은 `where(r>=3.5, 2, 1)` 로 **sid 값**을 넣었다 → 큰 입자(AM_P)가 sid 1(AM_S)로 구워졌다.  주석이 sid 규약을 인용하며 type 인자를 채운 것이 원인.  **`where(r>=3.5, 1, 2)` 로 수정 + 실행 검증**(큰→sid 2, 작은→sid 1 PASS) |
| **6** | `sr01` `plugged_frac` xyz toroidal | **CONFIRMED → 수정** | 내 코드다.  `:103` `np.roll(am_mask, sh, axis=ax)` 가 세 축 전부 감는데 성분 라벨은 `ndimage.label` = **비주기 6-face** = 같은 그림에서 두 규약 혼합.  `spans_z` 도 solver plate 가 아니라 **carbon envelope**.  **셋 다 수정** (§3) |
| **7** | STEP3 periodic 진단이 seam/plate edge 누락 | **CONFIRMED** | 내부 스윕 S1a 가 독립 확인.  솔버는 `:442-446` 에서 x/y wrap 을 커플링하는데 `phase_current_share`(`:516`)·`carbon_se_contact_area`(`:601`)·`am_surface_patches`(`:1468`)·`pore_pnm`(periodic 인자 **부재**)·`_voxel_jmag`(`:615`) 가 그 face 를 합에서 뺀다.  seam 지배 격자 실측 **wrap face 소산 = 전체의 22.9 %, 그 100 %가 VGCF**.  **미수정** |
| **8** | segment raster 방향반전 불변성 위반 | **CONFIRMED → 수정** | 재현: forward 14 / reverse 12 / symdiff 4.  **뿌리는 부동소수 한 줄** — `2.4/0.4 = 5.999999999999999` 이라 `floor` 가 6 이 아니라 5 를 준다.  그 위에 끝점 보장 루프가 **뒤로 걸어가** 선분 위에 없는 셀 (2,3,6)·(2,3,5) 을 만들었다 = 비단조 경로.  **수정** (§3) |
| **9** | checker 예외가 warning 이라 exit 0 | **부분 CONFIRMED** | v2 에서 **rung 실행 실패는 이미 오류로 승격**했고 등록부 최소크기·교정표본 필수 id 도 걸었다.  ⚠ 그러나 **import 실패와 unknown adjacency 는 여전히 `warns`** 다 → fail-closed 아님.  **미수정** |

⚠ **내 게이트 ③ 회귀가 #8 을 통과시킨 이유**: "끝점이 정확히 복셀 경계" 는 시험했지만
**음의 방향**을 안 밟았다.  같은 병(시험이 쉬운 경로만 밟음)의 **세 번째 재발**이다.

---

## 3. 수정 내역

### `fibre_segment_raster.segment_cells` (#8)
1. **`cell_of(p, vox)` 신설** — 경계에 놓인 좌표를 정수로 스냅한 뒤 floor (단일 소스).
2. **주 루프가 끝 셀에 닿으면 즉시 종료** — 지나친 뒤 되돌아오는 경로 소멸.
3. **방향 정규화** — 항상 사전식으로 작은 끝점에서 굽고 필요하면 뒤집어 반환.
   모서리·꼭짓점 통과 시 `argmin(tmax)` 의 동률 규칙("낮은 축부터")이 **방향 의존**이라
   스냅만으로는 부족했다 (스냅만: 무작위 4000 중 **1686 위반**).  정규화로 **구성상** 불변.

**검증**: Codex rung symdiff 4 → **0** · 무작위 4000 선분(경계-정확 끝점 다수 포함)에서
**반전불변 위반 0 · 비단조 0 · 끝점계약 위반 0** · 기존 selftest 17/17·step3 PASS·A/B 9/9 유지.

### `sr01_carbon_network` (#6)
- **`_shift(mask, axis, sh, periodic)`** — 주기축은 wrap, **비주기축은 zero-padding**.
- **z 는 어떤 경우에도 wrap 하지 않는다** (솔버가 플레이트로 막는 축).
- **성분 라벨도 같은 periodicity** — `periodic_xy=True` 면 x/y seam 성분을 union-find 로 병합.
- **`spans_z` 를 solver plate mask 기준으로** (`plate_bot`/`plate_top`); carbon envelope 는
  `--legacy` 로만, `spans_z_basis` 필드에 근거를 박는다.
- `run(..., periodic_xy=, legacy=)` + CLI `--periodic-xy` / `--legacy`.
  산출 CSV 에 `boundary` 열로 규약을 기록.
- **회귀 6건 추가** (selftest 14 → **20**): seam-건너 plugged 가 비주기 0 / 주기 1 ·
  **z 는 주기라도 0** · 라벨 periodicity 일치 · plate 기준 spans_z 가 짧은 기둥을 거부 ·
  legacy 가 같은 기둥을 관통으로 봄(판별력 낮음 실증).

### `viz_se_voxel_2d` (#5)
`am_t = where(r>=3.5, 2, 1)` → **`where(r>=3.5, 1, 2)`**.  실행 검증 PASS.

---

## 4. CL-05 / CL-08 재판정 — 진행 중

- **생산 STEP3 기본은 비주기**(`MPM_PERIODIC_SIGMA` 미설정, `mpm_input_from_case.py:969`)
  → corrected 계산은 `periodic_xy=False` (모든 축 zero-padding, z 포함).
- **`kit_ps_7_3` corrected 완료**:

| | legacy (혼합 규약) | **corrected** | Δ |
|---|---|---|---|
| point `plugged_frac` | 0.9436 | **0.9420** | −0.0016 |
| segment `plugged_frac` | 0.9945 | **0.9941** | −0.0004 |
| point `largest_mass_frac` | 0.3747 | 0.3747 | 0 |
| point `span_mass_frac` | 0.3747 | 0.3747 | 0 |

⇒ **CL-05 의 결론(경로 강제, 단절 아님)은 정정 후에도 유지된다.**  toroidal wrap 이
더하던 몫은 **0.16 %p** 로, 4.6 M 셀 격자에서 seam 이 차지하는 비율만큼이다.
`largest_mass_frac` 은 비주기 라벨이 원래와 같아 **변화 없음** → **CL-08 불변 예상**.
`span_mass_frac` 이 안 변한 것은 이 킷들의 탄소가 침대 두께를 거의 다 채워 carbon envelope
와 solver plate 가 사실상 일치하기 때문이다 (판별력 개선은 얇은/국소 탄소 케이스에서 발현).

- 나머지 4 킷 corrected 스윕 **실행 중** → 완료 시 `sr01_carbon_network_corrected.csv`.
- **처리 방침** (요청 1·2 반영):
  - `CL-05.evidence_state = hold` — corrected 5킷 완료 전까지 verified 증거로 인용 금지.
  - `plugged_frac = 0.944` 는 **철회하지 않고** `legacy mixed-boundary measurement` 로 보존,
    **기전 증거로 사용 금지** 라벨.

---

## 5. 아직 남은 것

| | |
|---|---|
| **#3** mpm3d coverage `np.roll` 무조건 wrap | 미수정.  같은 원칙(비주기 zero-pad · 주기 x/y only · z 항상 zero-pad) 적용 + 기존 coverage 숫자 영향범위 재계산 필요 |
| **#7** STEP3 periodic 진단 5종 | 미수정 |
| **#9** import 실패·unknown adjacency 가 warns | 미수정 (rung 예외는 이미 오류) |
| **#2** `pore_tau` either/both-plate | needs-runtime — 격자 픽스처 1개로 판정 가능 |
| checker 강화 | `symbol+output` 단위 registry · solver 양방향 검사 · grid/origin/BC/periodicity/phase/stamp 구조화 비교 · `--selftest` 가 실제 RUNGS 실행 · schema validation 과 `expected_violations` 분리 |
| claims 병합 | `claims_codex_sweep_additions_20260812.json` 17건 — 기존 CL-01~08 과 **ID 충돌 없음**(CDX-* 계열) 확인 후 병합 판정 |

---

## 6. 회귀 현황

| | |
|---|---|
| `fibre_segment_raster --selftest` | **17/17 PASS** |
| `sr01_carbon_network --selftest` | **20/20 PASS** (14 → 20) |
| `sr01_realbed_ab --selftest` | 9/9 PASS |
| `step3_sigma --selftest` | PASS |
| `check_method_discipline --selftest` | 23/23 PASS |
| `check_method_discipline` full | 0 errors |
| Codex RUNGS | **6/7 PASS** (FAIL 1 = #8, 수정 후 PASS) |
| 무작위 반전불변 (신규) | 4000/4000 |
