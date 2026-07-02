# B₂O₃ 챔피언 — ELF 결합 공유결합성 (슬라이드 19의 b2o3 판)

**날짜** 2026-07-02 · **방법** DFT ELF (QE `pp.x plot_num=8`, KISTI, 기존 `tmp/b2o3.save` SCF 재활용 → 128원자 ELF cube grid [96,96,960], mean 0.446 = 진짜 ELF) → 각 결합 중점 ELF 샘플(`tools/figures/sample_elf_bonds.py`, B 포함).
**데이터** `db/properties/b2o3_elf_bonds.csv` · **그림** `docs/figures/cascade/b2o3_elf_bond_covalency.png`(결합별 막대), `b2o3_elf_planes.png`(BS₃·PS₄ 2D 평면 slice), `b2o3_vs_lpscl16_elf_covalency.png`(LPSCl1.6 비교) · **cube** KISTI `b2o3_elf.cube`(VESTA용, 커밋X)

> **한 줄.** 중점 ELF 공유결합성 순위 **B–S(BS₃) 0.959 > P–S(PS₄) 0.945 > P–O 0.930 > Li–S 0.929 > Li–Cl 0.884 > Li–O 0.780**. **B–S가 챔피언에서 가장 공유결합적** — **삼각 BS₃ thioborate가 P–S보다도 강한 공유결합 motif**임을 전자국재로 확증.

## 결과
| 결합 | ELF_mid | std | n | d (Å) | 성격 |
|---|---|---|---|---|---|
| **B–S (BS₃)** | **0.959** | 0.003 | 6 | 1.83 | 공유(최강, NEW) |
| P–S (PS₄) | 0.945 | 0.002 | 29 | 2.07 | 공유 |
| P–O | 0.930 | 0.001 | 3 | 1.56 | 공유 |
| Li–S | 0.929 | 0.024 | 149 | 2.48 | Li–음이온 |
| Li–Cl | 0.884 | 0.027 | 78 | 2.51 | Li–음이온(이온성↑) |
| Li–O | 0.780 | 0.026 | 6 | 1.91 | Li–음이온 |

## 해석
- **B–S = 0.959로 최상위 공유결합** → **BS₃ thioborate motif이 강한 공유결합 단위**(P–S보다도 위). 결합길이(B–S 1.827±0.01, std 극소)·Bader(B +3.00)·배위(BS₃ 3배위)·phonon(고립 B–S 모드)에 이어 **전자국재(ELF)로 5번째 확증**.
- **공유 골격(B–S/P–S/P–O)은 std 0.001–0.003로 극히 좁음** = 잘 정의된 진짜 공유결합.
- **Li–음이온(Li–S/Cl/O)은 std 0.02–0.03로 넓음** → 중점 ELF가 **음이온 lone-pair 껍질 근접**에 영향받아 다소 부풀려짐(순수 공유성 아님). robust 공유결합 집합 = **B–S/P–S/P–O**.
- 툴 캘리브레이션(P–S 0.94 > Li–S 0.93 > Li–Cl 0.85)과 정확히 일치 → 값 신뢰.

## LPSCl1.6 비교 (정밀 — 둘 다 실제 ELF cube, 같은 툴)
modelc(LPSCl1.6) ELF cube(mean 0.460)에서 직접 샘플 → **골격 결합 거의 완전 동일**:
| 결합 | LPSCl1.6 | b2o3 | Δ |
|---|---|---|---|
| P–S | 0.944 | 0.945 | +0.001 (동일) |
| Li–Cl | 0.887 | 0.884 | −0.003 (동일) |
| Li–S | 0.940 | 0.929 | −0.011 |
| **B–S(BS₃)** | — | **0.959** | NEW |
| **P–O** | — | **0.930** | NEW |
- **결론: B₂O₃ 도핑이 PS₄/Li–Cl 골격 공유결합성을 그대로 보존**하고 **B–S(최강)·P–O 신규 공유 motif만 추가**. 평면 slice(`b2o3_vs_lpscl16_elf_planes.png`)에서 PS₄ 평면이 육안으로도 동일. (`db/properties/modelc_elf_bonds.csv`)

## 연결
- 슬라이드 19(LPSCl/LPSCl1.6 ELF: PS₄ 공유·Li 이온·free-S lone pair)의 **b2o3 확장** — 새 B–S/P–O 공유 지문 추가.
- `b2o3_bond_lengths_2026_06_29.md`(B–S 1.827), `b2o3_charge_bader_lowdin_2026_06_30.md`(B +3), Voronoi/배위(BS₃), `b2o3_cdd_2026_07_02.md`(같은 공유결합 축적).
- free-S²⁻(공유 파트너 없음)이 가장 먼저 산화되는 ESW 서사와 정합(free-S는 결합 ELF 아닌 lone-pair 국재).
