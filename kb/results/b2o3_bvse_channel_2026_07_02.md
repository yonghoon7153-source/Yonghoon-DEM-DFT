# B₂O₃ 도핑 → Li 채널 확장 (BVSE, b2o3 vs LPSCl1.6)

> [!warning] SUPERSEDED (2026-07-09 SEMIFINAL)
> 본 문서의 **"σ 1.33×" 및 D₀-driven 향상 서사는 철회**됐다 — 멀티시드(3-seed×3-T) 판정: σ비율 1.08/0.82/1.15 = **동등**.
> 유효하게 남는 것: **BVSE 채널 +45% 확장**(정적 기하)과 동일-Ea. 순효과는 "σ 보존"(O의 Li–O 트랩 ↔ 채널 개방 상쇄).
> 정본: kb/results/b2o3_SEMIFINAL_report_2026_07_09.md.

**날짜** 2026-07-02 · **방법** BVSE(Bond-Valence Site Energy) Li 이동 맵. `tools/comp1_v3/bvse_standalone.py`(pure numpy/scipy, CIF→맵, DFT 불필요). BVS(r)=Σ exp((R0−d)/b) over S/Cl/O, BVSE=(BVS−1)². 각 맵 자체 최소값 기준 상대비교.
**데이터** `db/properties/bvse_b2o3/`, `bvse_modelc/` · **그림** `docs/figures/cascade/bvse_channel_volume.png`, `bvse_channel_2p5d.png` · **VESTA cube** `docs/figures/bvse_cubes/*_bvse_aboveMin.cube`(min-subtract, 커밋X·gitignore)

> **한 줄.** B₂O₃ 도핑이 **Li 접근가능 채널 부피를 +45% 확장**(BVSE≤1.0 above-min에서 b2o3 **12.2%** vs LPSCl1.6 **8.4%**). MD(σ 1.33×↑)·Voronoi disorder↑와 같은 방향 — "도핑이 통로를 넓혀 전도 향상"의 **정적 기하 근거**.

## 결과
| | LPSCl1.6 | b2o3 |
|---|---|---|
| 채널 부피분율 (BVSE≤1.0) | 8.4% | **12.2%** (+45%) |
| Li_site BVS 평균 | — | 1.71 (이상 1.0) |
| BVSE percolation 장벽 | 참조 | 낮음(정적) |

## VESTA 시각화 (공정 비교)
- `*_bvse_aboveMin.cube`: 각 맵에서 **최소값을 빼서** 둘 다 0부터 시작 → VESTA에서 **동일 isolevel(~1.0)** 로 열면 절대스케일 차이 없이 공정.
- 노랑 isosurface = 낮은 BVSE = Li 채널. b2o3가 **더 넓고 연결**됨(정량 +45%와 정합).
- 2.5D(min-projection 지형)는 보조 — VESTA "질감"이 직관적.

## 연결·한계
- MD(`b2o3_vs_lpscl16_md`): σ 1.33×↑, D₀-driven. BVSE 채널 확장이 D₀(통로/attempt) 증가의 기하 근거.
- Voronoi(`b2o3_voronoi_disorder`): 전 종 disorder↑. 채널 확장과 같은 "도핑이 격자를 열었다" 서사.
- **한계**: BVSE는 경험적(valence² 단위, 절대 eV 아님). 상대비교·경향용. 절대 장벽은 MLIP-MD/NEB로.
