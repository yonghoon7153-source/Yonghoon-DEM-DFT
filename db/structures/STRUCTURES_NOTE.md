# db/structures — comp1/modelc V0 권위 구조 노트

## comp1 (Li₆PS₅Cl)
- ✅ **`comp1_V0_k444.cif` / `.xyz` = FINAL/AUTHORITATIVE V0**
  - 출처: container `comp1_v3/v3_post/k444_redo/relax_k444.out` (4×4×4 relax, k×L=40)
  - PS₄ intact (P-S 2.072±0.036 Å), V0=1016.62 Å³, a=10.0551 Å (cubic), E0=−13917.8916 eV
  - ordered: Cl ×4 + free-S²⁻ ×4가 서로 다른 자리 독점 (S/Cl mixing 없음)
  - **figure + 구조 분석 모두 이 파일 사용**
- `lpscl_F43m_24G_canonical.cif` — idealized F-43m (P 정확히 특수위치). figure용으로 깔끔하나
  V0 아님(a=10.249). 필요시 V0로 스케일해 사용 (paper_figures/comp1_V0_cubic.cif가 그 결과).
  ⛔ **2026-11-17 실측 — 이 파일의 음이온 배치는 물리적으로 불가능하다. 쓰기 전에 이 줄을 본다.** Cl 이 4d (0.75,0.75,0.75) 에 있는데
  거기는 PS₄ 꼭짓점 S 넷에서 **2.36 Å** 인 빈 사면체 구멍 (Morgan 2021 type 3) 이다 (S–Cl 최소 2.356 Å · 3 Å 안 16 쌍).
  Li 24g 6 개가 2.33 Å 로 둘러싼 케이지 가운데 4c (0.25,0.25,0.25) 는 **비어 있다**. 자유 음이온 자리는 4a + 4c 여야 한다 —
  그렇게 고친 음이온 격자는 Delaunay 사면체가 정확히 **136** (= Morgan Table 1 의 4+16+48+4+16+48) · 이 파일 그대로는 179.
  추정 원인 (확인 안 함): PS₄ S x = 0.617 관례 (케이지 = 4c) 와 x = 0.383 관례 (케이지 = 4d) 를 섞었다. 4c·4d 는 둘 다 P 에서 4.44 Å 라
  P 거리로는 못 가른다 (11-17 에 내가 그걸로 갈라 'Morgan 100 % 뒤바뀐 배열' 이라고 잘못 말했다).
  같은 배치를 줄인 `paper_figures/comp1_V0_cubic.cif` 도 S–Cl 2.31 Å. DFT 정본 `comp1_V0_k444.cif` 는 S–Cl 3.66 Å 로 멀쩡하다.
  cascade 설계 base 로 쓰였고 09-12 에 UMA '가짜 basin' 으로 정본에서 내려왔다 (`db/properties/cascade_reanchor_comp1k444_2026_09_12.json`) —
  그때 최소거리 점검 (`cascade_base_strain_2026_09_12.json` §2) 은 Li–Li · Li–S · Li–Cl · S–S 만 쟀고 **S–Cl 이 없었다**.
  ⏩ **처리 (2026-11-17 · 사용자 '권고대로')** — 이 파일은 경로 · 바이트 그대로 둔다 (도구 13 · 기록 약 20 이 가리키고 cascade 기록이 md5 로 출처를 대조한다).
  · 고친 판 = `lpscl_F43m_24G_ideal_Clcage_2026_11_17.cif` (할로젠만 두고 나머지를 P 중심으로 반전 → Cl 이 Li 케이지 가운데 · S–Cl 4.23 Å ·
    음이온 사면체 136 · 이상화 좌표 · 이완 안 함 · 모든 Cl 이 케이지 자리인 정렬 모형 하나라 실제 S/Cl 무질서를 대표하지 않는다).
  · 그림용 V0 판 = `paper_figures/comp1_V0_cubic_Clcage_2026_11_17.{cif,vasp,xyz}` · 원시 셀 · B₂O₃ 도식도 같은 이름 꼴로 고쳤다.
  · 깨진 사본 넷 (`paper_figures/comp1_V0_cubic.{cif,xyz}` · `paper_figures/lpscl_primitive_1fu.cif` · `lpscl_b2o3_scheme_F43m.cif`) 은
    `*.BROKEN_Cl_in_4d_hole` 로 이름을 바꿨다 (읽는 곳 없음). 위 줄의 'paper_figures/comp1_V0_cubic.cif 가 그 결과' 는 그 사본이다.
  · 새 작업이 이 배치를 못 집게 `tools/doping/substitute_struct.py::refuse_unphysical_base` (할로젠–S < 3 Å 면 멈춤) 를
    substitute_compound · run_cathode_interface · preflight · predict_best_site 에 걸었다 (옛 기록 재현은 `--allow_unphysical_base`).
  · 기록 `db/properties/argyrodite_canonical_cif_4d_halide_2026_11_17.json` · 근거 `db/raw/argyrodite_canonical_fix_2026_11_17/`.
- ❌ `lpscl_relaxed_conv_52atoms.cif.BROKEN_PS4_dissociated` — **사용 금지**.
  conventional-cell 변환 사고로 PS₄ 해리 (각 P가 S 1~2개만 ≤2.5Å, 나머지 4.3Å). k-mesh 무관, CIF 변환 버그.

## modelc (Li₅.₄PS₄.₄Cl₁.₆)
- `modelC_DFT_EOS_V0.cif` — EOS v100 점(V=1204.22) 구조. V0(1216.44)로 스케일해 사용.
  rhombohedral 초격자, Cl-rich + Li 공공 (disordered). figure는 rhombohedral 그대로.
  ⚠ EOS 구조와 LOBSTER(k663) property 구조가 Cl 4a/4d 배치가 다를 수 있음 — per-site ICOHP는
  property 구조(bonds_modelc_k663.json) 기준.
  ✅ **2026-10-21 확인 — '다를 수 있음' 은 이 cif 에만 해당한다.** 실제 B₀ 21.71 GPa 를 낸 EOS 입력
  (백업 B `runs/lpscl16_verify_20260520/modelC_v2_eos_v100.in` · `v101.in`) 은 `modelC_v3/V0_relax.in`
  (= `modelc_V0_k663.xyz`) 과 **같은 음이온 배치**다 (자유 S 두 자리 0.01 Å 안 · 사용자 WSL 실행).
  반면 이 cif (`modelC_DFT_EOS_V0.cif`, V = 1204.22) 는 V₀ 구조와 **자유 음이온 한 자리에서 S↔Cl 가 바뀌어 있다**
  ⇒ v2 EOS 의 점이 아니라 다른 (옛) 판의 구조다. 이 cif 를 'modelC 기준 구조' 로 쓰는 도구
  (`tools/doping/tier_cascade.sh` NCM_BASELINE_MODELC · `tools/cascade/uma_relax_check.py` · `tools/neb_diffusion/argyrodite_cage_neb.py`)
  는 논문 V₀ 구조와 배치가 하나 다른 구조를 쓰고 있다 — 논문 값과 맞대려면 `modelc_V0_k663.xyz` 를 쓴다.

## sdcp_wave1/ (2026-08-28 추가)

wave1 VASP 회수 드롭의 `static/OUTCAR.gz` 에서 **계산에 실제로 들어간 기하**를 되꺼낸 것.
조각 3종(ptfe_c10 · ptfe_dimer · sdcp_neutral) × 자세 × 시드 = **16 세트**,
각각 `.xyz` + `.vasp` + `.vesta`. 자세한 설명은 `db/structures/sdcp_wave1/README.md`.

- ⚠ **이완된 DFT 최소점이 아니다** — MLIP(UMA, freeze 0.85) 기하 위의 단일점(NSW=0).
- ⚠ 기하는 **자세당 하나**다. pm1/net4 도, static/dense 도 좌표가 완전히 같다(실측).
  두 시드 파일의 차이는 `.vesta` 의 **AFM 부격자 색(NiA/NiB)** 뿐이다.
- 에너지 표는 `db/properties/sdcp_wave1_job_energies_2026_08_28.csv` (+ `.json`).
- 생성: `python3 tools/sdcp/scfin_to_struct.py --outcar … --out db/structures/sdcp_wave1`

마지막 갱신: 2026-10-21
