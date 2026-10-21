# db/structures — comp1/modelc V0 권위 구조 노트

## comp1 (Li₆PS₅Cl)
- ✅ **`comp1_V0_k444.cif` / `.xyz` = FINAL/AUTHORITATIVE V0**
  - 출처: container `comp1_v3/v3_post/k444_redo/relax_k444.out` (4×4×4 relax, k×L=40)
  - PS₄ intact (P-S 2.072±0.036 Å), V0=1016.62 Å³, a=10.0551 Å (cubic), E0=−13917.8916 eV
  - ordered: Cl ×4 + free-S²⁻ ×4가 서로 다른 자리 독점 (S/Cl mixing 없음)
  - **figure + 구조 분석 모두 이 파일 사용**
- `lpscl_F43m_24G_canonical.cif` — idealized F-43m (P 정확히 특수위치). figure용으로 깔끔하나
  V0 아님(a=10.249). 필요시 V0로 스케일해 사용 (paper_figures/comp1_V0_cubic.cif가 그 결과).
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
