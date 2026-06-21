# 3D isosurface (VESTA) recipe — Li-density (inter-cage) & ELF (bonding)

이 deck의 3D isosurface 그림(Li 이동망 / ELF)을 재현하는 절차. cube 생성 스크립트 + VESTA 세팅.

---
## A. Li-density isosurface = inter-cage 도시 (이온전도 섹션)
"comp1=고립 cage / modelc=inter-cage 연결망"을 보여줌.

**1) cube 생성** (`tools/ionic/li_density_cube.py`, numpy만, AIMD traj 필요):
```bash
python3 tools/ionic/li_density_cube.py \
  --traj T600/traj.xyz --out comp1_Cl1.0_T600_Li.cube \
  --skip 100 --spacing 0.2 --sigma_A 0.4 --species Li
# modelc도 동일 (traj만 교체)
```
- `--skip` equilibration 프레임 버림, `--sigma_A` Gaussian smoothing, framework 원자는 평균위치로 cube에 포함.

**2) VESTA 렌더:**
- 파일 → cube 열기 → Properties → Isosurfaces.
- **Isosurface level ≈ 0.3–0.6 × max** (낮출수록 inter-cage 다리가 연결돼 보임).
- 색: comp1 파랑 / modelc 노랑 (조성 구분), transparency ~0.3.
- 원자: Li 숨기거나 작게, free-S²⁻(노랑)·Cl(초록) 보이게 → cage center / inter-cage gateway 표시.
- → comp1은 점들 고립, modelc는 Cl 쪽으로 번져 연결 = percolation.

**주석판(화살표)**: `docs/figures/elf_licl/intercage_Li_density_annotated.png` (2D 투영 + intra/inter-cage 화살표). 생성: `tools/figures/annot_intercage.py`.

---
## B. ELF isosurface = 결합 성격 (전자구조/산화 섹션, PDOS 옆)
"이온 Li / 공유 PS₄, 음이온 lone-pair"를 보여줌. (조성 무관 = 대조군)

**1) cube 생성** (QE `pp.x`, SCF out/ 사용):
```fortran
&inputpp  prefix='comp1', outdir='./out', plot_num=8 /   ! plot_num=8 = ELF
&plot  iflag=3, output_format=6, fileout='comp1_ELF.cube' /
```
`pp.x -in elf.in > elf.out` (GPU/CPU 빌드 동일).

**2) VESTA 렌더:**
- **Isosurface level 0.85** = 공유결합/lone-pair 국재 (PS₄ 주변 lobe, 음이온 lone pair).
- 낮은 level(~0.5)도 한 겹 더 = 이온 영역(Li 주변 moat) 보임.
- multicolor(gradient)로 ELF 0→1 범위 표시 가능.
- → P–S 사이 높은 ELF(공유), Li 주변 낮음(이온), S²⁻/Cl⁻ lone-pair 구름.

**주의(캡션)**: ELF는 *에너지 분해 안 됨*(core+valence+lone pair 합) → "결합 성격/전자 국재"로 표기, "VBM 전자"라 하지 말 것. 산화 onset은 PDOS·grand-potential 담당.

matplotlib 대안(서버에서 바로): `tools/modelc_v3/plot_elf_3d_iso.py --cube comp1_ELF.cube --iso 0.85`.

---
## 슬라이드 배치
- **Li-density(A)** → 이온전도 섹션, BVSE 슬라이드 뒤 (percolation/inter-cage). 2D 주석판 + 3D VESTA 같이.
- **ELF(B)** → 전자구조/산화 섹션, PDOS·DOS 옆 (결합 성격 + S²⁻ lone-pair = 산화 자리 맥락).
