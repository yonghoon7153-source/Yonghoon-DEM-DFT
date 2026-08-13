# Li3N(001) on-N → bridge → on-N 궤적 (그림 전용) — **위치 고정**

## 재생성 (항상 같은 자리)

```
python3 tools/neb_diffusion/li3n_hop_frames.py --onN --n1 N20 --n2 N36 \
  --min <min.vesta> --ts <ts.vesta> \
  --h_top 2.10 --h_bridge 1.85 --ghost_r 0.62 --end_r 1.30 \
  --xi 0,0.1667,0.3333,0.5,0.6667,0.8333,1.0 \
  --outdir docs/figures/li3n/onN_path --merge          # 병합 (필요시 --no_bonds)
  # --merge 빼면 single/ 에 낱장 7장
```

`--n1 N20 --n2 N36` 이 **자리를 못 박는다.** 빼면 셀 중앙 기준으로 자동 선택되는데,
기준을 조금만 바꿔도 그림이 움직인다 (2026-08-12 사용자 지적).

| | 표면 N 사이트 | frac |
|---|---|---|
| 시작 on-N | **N20** | (0.341465, 0.341931, 0.408080) |
| 끝 on-N′ | **N36** | (0.668337, 0.668095, 0.407142) |

## 파일

| 경로 | 무엇 |
|---|---|
| `li3n_hop_alladatoms_display.vesta` | 7위치 한 장 (결합선 있음) |
| `li3n_hop_alladatoms_nobond_display.vesta` | 7위치 한 장 (결합선 없음) |
| `single/li3n_hop_xi***_adNa_display.vesta` | 낱장 7장 — 병합본과 좌표 동일 (검증됨) |

## 강조 3점 + 보간 4점

| ξ | | 표면 N (Å) | 자리 |
|---|---|---|---|
| 0.00 | ★ 큰 공 1.30 Å | 2.100 (1개) | **on-N (atop)** |
| 0.17 / 0.33 | 작은 공 0.62 Å | 2.050 / 2.224 | 보간 |
| **0.50** | ★ 큰 공 | **2.573 / 2.592 (2개 같음)** | **N–N bridge = saddle 위치** |
| 0.67 / 0.83 | 작은 공 | 2.247 / 2.075 | 보간 |
| 1.00 | ★ 큰 공 | 2.127 (1개) | **on-N′** |

경로 3.575 Å · 최저 Li–N 2.050 Å · BOUND zmax 는 adatom 위로 자동 확장됨.

## ★ 표시용이다

**이 경로 위의 어떤 점도 계산된 배치가 아니다.** 표면 N 위치에서 기하로 만든 궤적이고
높이는 h_top 2.10 / h_bridge 1.85 Å 대칭 프로파일이다. 에너지를 붙이면 안 된다.
수렴시킨 두 구조(ΔE = 0.118 eV)는 `../hop_frames/li3n_computed_*.vesta` 이고 자리가 다르다
— `kb/syntheses/li3n_barrier_revision_defense_2026_08_12.md` §C4 · §C6.

캡션 문안:
> Spheres mark successive lateral positions of the Li adatom along the surface
> migration coordinate; positions are illustrative and were not separately relaxed.
> Energies were evaluated only for the configurations listed in Table S2.
