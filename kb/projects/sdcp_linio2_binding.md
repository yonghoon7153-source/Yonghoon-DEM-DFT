# SDCP–LiNiO₂ Binding Anchoring Scan

> Status: scan setup. Files identified + uploaded; slab build + scan script not written yet.
> Owner: 안용훈 (BML Lab, Hanyang).
> Started: 2026-05-29.

## Goal
SDCP conducting binder가 LiNiO₂ (104) cathode surface 어느 site에 anchor 되는지
binding energy E(dx, dy, dz) 맵으로 찾기. **doped(self-doped anion) vs neutral(protonated acid)** 비교 →
self-doping이 cathode anchoring에 어떤 영향을 주는지 확인.

위치: Digital Twin Platform의 cathode interface 트랙 (north_star 노트 참고).

## SDCP molecules (Windows local에서 ORCA TZVP optimized)

| form | atoms | composition | E_ORCA (Ha) | source (Windows) | gabia |
|------|-------|-------------|-------------|------------------|-------|
| sdcp_doped (−SO₃⁻) | 33 | C₁₁H₁₅O₅S₂⁻ | −1600.481 | `D:\QE\6. orca_sdcp\phase1_doped\06_doped_opt_freq_v2.xyz` | `/data/work/runs/sdcp_linio2_binding/inputs/sdcp_doped/sdcp_doped.xyz` |
| sdcp_neutral (−SO₃H) | 34 | C₁₁H₁₆O₅S₂ | −1601.140 | `D:\QE\6. orca_sdcp\phase1_neutral\02_neutral_opt_freq_raman.xyz` | `/data/work/runs/sdcp_linio2_binding/inputs/sdcp_neutral/sdcp_neutral.xyz` |

차이는 정확히 H 1개 — `-SO₃H` ↔ `-SO₃⁻` 양성자 상태. 둘 다 ORCA TZVP 최적화된 final geometry.

## Infrastructure
- **gabia (kserver116-27)**: UMA-s-1p1 env, 1× A100 50GB
- **재활용 코드**:
  - `tools/build_ncm_interface.py` — LiNiO₂ slab build (NCM x_Ni=1.0 case)
  - `tools/doping/run_mlip_postproc.py` (참고용) — UMA load + single-point/relax 패턴
- **새로 작성 예정**: `tools/sdcp_binding/scan_binding.py` — grid scan + binding E 계산

## Workflow plan

```
1. LiNiO₂ (104) slab — 4×4 surface, 4 atomic layers, vacuum ≥15 Å
   bottom 2 layers freeze, top 2 layers free, dipole correction on
2. SDCP molecule placement
   - 분자 center → (x0, y0, z0=z_top_O + 4 Å)
   - 분자 orientation: sulfonate −SO₃ 다운 (cathode 방향)
3. Grid scan
   dx ∈ [0, a_surf, step=0.5 Å]     ≈ 10 points
   dy ∈ [0, b_surf, step=0.5 Å]     ≈ 10 points
   dz ∈ [2.0, 6.0, step=0.5 Å]      = 9 points
   ⇒ ~900 single points × UMA single point ≈ 5s = ~75min total
4. E_bind(x,y,z) = E_complex − E_slab_isolated − E_SDCP_isolated
   (E_slab, E_SDCP는 사전에 한 번씩)
5. Heatmap E_bind(x,y) at minimum-E dz, dz profile at minimum (x,y)
6. Top-3 anchoring sites → UMA short relax (~50 step, fmax 0.05) 확인
7. (선택) Top-1 site → DFT single-point (QE PBE+D3) 검증
```

doped/neutral 둘 다 같은 workflow → 비교.

## Status checkpoint

- [x] SDCP final TZVP-opt 구조 식별 (Windows local)
- [x] gabia upload (`/data/work/runs/sdcp_linio2_binding/inputs/{doped,neutral}/`)
- [ ] LiNiO₂ (104) slab build (UMA-relaxed)
- [ ] `scan_binding.py` 작성
- [ ] Grid scan 실행 (doped)
- [ ] Grid scan 실행 (neutral)
- [ ] Analysis + heatmap
- [ ] (선택) DFT 검증

## 다른 트랙과의 충돌

- **gabia master batch (273 cascade, PID 309933)** 가 GPU 점유 → scan 시 `kill -STOP 309933` 필요.
  현재 BaO_x002 (step 25) 진행 중. 자연 종료 후 STOP하는 게 깔끔 (compound 1개 손실 없음).
- KISTI V0 DFT (job 742201), gabia LPSCl1.6 EOS와 무관.

## 참고
- SDCP composition은 pentyl-sulfonate가 thiophene+acetal에 붙은 자기-도핑 conducting binder
  (PEDOT-S 계열). cathode/SE interface adhesion 보강 목적.
- LiNiO₂ (104) surface는 NCM cathode의 active facet. Ni 노출 site / O 노출 site 비대칭이
  binder anchoring 결정.

## 사고 방지
- master batch와 GPU 충돌 — 항상 master STOP 확인 후 scan 시작
- SDCP는 anion(doped) 케이스에서 net charge −1 → UMA가 전하 입력 받는지 확인 필요
  (받지 못하면 neutralizing background OR doped를 H 붙여 neutral로 fallback)
- LiNiO₂는 magnetic (Ni³⁺ d⁷) — UMA가 spin handle 충분한지 확인 (cascade NCM 작업 경험 활용)


# Binding Energy Method (formalized)

## 1. Definition

```
E_bind(x, y, z) = E_complex(x, y, z) − E_slab_iso − E_SDCP_iso
```

부호: **E_bind < 0 = exothermic = favorable anchoring**. 결과 보고는 절댓값 또는 부호 그대로.

세 항 모두 **동일 cell, 동일 vacuum, 동일 UMA model(uma-s-1p1), 동일 calculator settings**로 계산
— 이게 ΔE 정합성의 첫 번째 조건.

## 2. Reference states (one-time, 사전 계산)

### E_slab_iso (LiNiO₂ (104) bare slab)
- Cell: 4×4 surface × 4 atomic layers + vacuum ≥15 Å (위쪽)
- 하부 2 layers freeze, 상부 2 layers free
- UMA relax (FIRE, fmax=0.02) → relaxed E_slab_iso
- 결과: relaxed slab geometry 저장 (.xyz) — 모든 complex가 이걸 사용

### E_SDCP_iso (각각 doped + neutral 별도)
- 같은 cell box(빈 공간) 안에 SDCP molecule 한 개만 — 주기영상과 거리 ≥ 12 Å
- UMA single-point ONLY (ORCA TZVP optimized geometry 그대로 사용 — 재최적화 X,
  ORCA quality 보존)
- 결과: E_SDCP_iso[doped], E_SDCP_iso[neutral]

**rationale**: SDCP intramolecular geometry는 ORCA TZVP optimized → UMA로 재relax하면
오히려 quality 떨어짐. UMA는 environment에서의 inter-molecular E만 담당.

## 3. Complex geometry (per grid point)

### Orientation 고정
- SDCP의 sulfonate −SO₃ group을 **slab 방향으로 향하게** (anchor가 sulfonate일 가능성 높음)
- 분자 frame: sulfur(S) of −SO₃ atom이 slab surface 정상축(z) 아래쪽 가리킴
- 분자 회전은 일단 한 가지 — 추후 Phase C에서 orientation도 sweep

### Placement
- 분자 anchor atom (sulfonate S): (x_anchor, y_anchor, z_anchor) = (dx, dy, z_top_O + dz)
  여기서 z_top_O = bare slab 가장 위쪽 O 평균 z-좌표
- 그 위치로 분자 전체를 rigid translate (orientation 보존)

### Grid
```
dx ∈ [0, a_surf)  step = 0.5 Å   ≈ a/0.5 points (~6–10)
dy ∈ [0, b_surf)  step = 0.5 Å   ≈ b/0.5 points (~6–10)
dz ∈ [2.0, 6.0]   step = 0.5 Å   = 9 points
total: ~10×10×9 = 900 points (~75 min UMA SP)
```

slab의 표면 unit cell이 작으면 (~3×3 Å) 5×5×9 = 225 points로 줄여도 됨.

## 4. Two-phase scan

### Phase A — Rigid grid scan (~1h)
- 각 (dx, dy, dz) 에서 분자+slab 좌표 합쳐서 UMA **single-point** (no relax)
- E_bind_rigid(dx, dy, dz) 계산
- 결과: 3D 데이터 → 2D heatmap(z 고정 최적층) + 1D z-profile
- Top-K (K=5~10) lowest E_bind_rigid sites 선별

### Phase B — Local relax on Top-K (~30 min)
- 선별된 K개 site 각각:
  - 하부 slab 2 layers freeze, 그 외 모두 free
  - UMA FIRE relax (fmax=0.05, max 50 steps)
- E_bind_relax(site_k) = E_complex_relaxed,k − E_slab_relaxed_top_free − E_SDCP_iso
- **참고**: E_slab_relaxed_top_free 는 isolated bare slab을 top 2 layers free로 한 번 더 relax해서
  쓰면 정확. (E_slab_iso와 거의 같지만 엄밀히 다른 값.)

### Phase C — orientation sweep on Top-1 (선택, ~10 min)
- 최저 E_bind 사이트에서 SDCP 분자를 z-축 기준 회전 (0°, 45°, 90°, 135°)
- 가장 stable orientation 확인

## 5. Charge handling (doped 케이스 — 핵심 주의사항)

doped SDCP는 **net charge −1 (anion)**. 처리 옵션:

| 방법 | 장점 | 단점 |
|------|------|------|
| **A. Li⁺ counterion 추가** | 전하 균형, 물리적 (cathode에 항상 Li 풍부) | counterion 위치도 변수로 들어감 |
| **B. UMA neutral 모드 + 보정** | 빠름 | E_bind 절댓값 부정확 (~수십 meV 오차) |
| **C. doped → H 추가해서 neutral로 통일** | 단순 | 비교 의미 (self-doping 효과) 사라짐 |

**추천 = A (Li counterion)**. Li⁺를 SDCP의 −SO₃⁻ 산소에 ~2.0 Å 거리로 미리 배치 →
전체 complex는 neutral. doped/neutral 비교 시 doped 측에 Li 1개 추가, 양쪽 atom 수가
달라도 E_bind 정의(separated reference) 자체는 self-consistent.

E_bind 계산 시:
- E_complex = E[slab + SDCP + Li⁺]
- E_SDCP_iso = E[SDCP + Li⁺] (둘이 묶인 isolated pair)
- E_slab_iso = E[bare slab]

doped/neutral 비교는 **|E_bind| 차이**가 아니라 **anchoring site 위치 + 결합거리**가 1차 결론,
|E_bind| 정량 비교는 2차 (오차 막대 함께 보고).

## 6. Convergence + sanity checks

매 phase 끝마다 확인:

| check | 기준 | 행동 |
|-------|------|------|
| Vacuum 충분? | slab–image 거리 ≥15 Å, complex top → top vacuum boundary ≥10 Å | 부족하면 cell 키워서 다시 |
| Lateral periodic image | a, b 방향 SDCP–SDCP 거리 ≥10 Å | 부족하면 supercell 키우기 |
| Bare slab relax 수렴 | fmax < 0.02 eV/Å, energy < 1 meV/atom 변동 | 안 되면 step 늘리거나 mixer 바꿈 |
| SDCP isolated geometry preserve | UMA SP 결과 force 평균 < 0.1 eV/Å | 크면 ORCA geom이 UMA에 안 맞는 것 → 짧은 UMA relax 한 번 |
| Top-K rigid vs relaxed ranking 일치 | top-1 rigid ≈ top-1 relax (or in top-3) | 크게 바뀌면 step C 추가 또는 grid 세분화 |
| E_bind 부호 | best site에서 E_bind < −0.2 eV (binder 의미 있으려면) | 양수 또는 너무 약하면 reference state / orientation 의심 |

## 7. Output schema

각 phase 결과를 JSON으로 저장 (cascade 패턴 따라):

```json
{
  "provenance": {"date": "...", "uma_model": "uma-s-1p1", "git_sha": "..."},
  "system": {
    "form": "doped" | "neutral",
    "slab": {"facet": "104", "supercell": "4x4x4", "vacuum_A": 15.0},
    "SDCP": {"n_atoms": 33|34, "charge": -1|0}
  },
  "reference": {
    "E_slab_iso_eV": ...,
    "E_SDCP_iso_eV": ...
  },
  "phase_A_rigid": {
    "grid": {"dx": [...], "dy": [...], "dz": [...]},
    "E_complex_eV": [[[...]]],  // 3D array
    "E_bind_eV":    [[[...]]],
    "min_idx": [i, j, k],
    "min_E_bind": ...
  },
  "phase_B_relax": {
    "top_K": [
      {"site_xyz": [...], "E_complex_relax": ..., "E_bind_relax": ...,
       "anchor_atom_slab": "O_idx_142", "S_O_distance_A": ...},
      ...
    ]
  }
}
```

## 8. Plan visualization
- 2D heatmap: `E_bind(dx, dy)` at z* = argmin_z (matplotlib pcolormesh, colorbar)
- 1D z-profile: `E_bind(z)` at (dx*, dy*)
- Top-3 site overlay on slab (ASE plot)
- doped vs neutral: 같은 heatmap 옆에 나란히 (subplot)

## 9. DFT 검증 (선택, post-scan)
- Top-1 site complex → QE PBE+D3 single-point (no relax)
- Reference E_slab, E_SDCP도 QE 같은 settings로 한 번씩
- E_bind_DFT = E_complex_QE − E_slab_QE − E_SDCP_QE
- UMA vs DFT ΔE 비교 → 우리 UMA 결과 신뢰성 quantify

## 10. 다음 작업 우선순위
1. LiNiO₂ (104) slab build + UMA relax (1회) → 기준 slab
2. SDCP isolated single-point (각각 doped/neutral, 1회씩)
3. `scan_binding.py` 작성 (Phase A grid + Phase B Top-K relax)
4. 작은 grid로 sanity check (4×4×3 = 48 points)
5. 본 grid scan 실행
6. 분석 + heatmap + report
