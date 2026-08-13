# Li3N(001) on-N → bridge → on-N 궤적 (그림 전용)

```
python3 tools/neb_diffusion/li3n_hop_frames.py --onN --merge \
  --min <min.vesta> --ts <ts.vesta> --outdir docs/figures/li3n/onN_path \
  --h_top 2.10 --h_bridge 1.85 --ghost_r 0.62 --end_r 1.30 \
  --xi 0,0.1667,0.3333,0.5,0.6667,0.8333,1.0
```

| ξ | 표면 N 거리 (Å) | 자리 |
|---|---|---|
| 0.00 | 2.100 (1개) | **on-N (atop)** — 큰 공 |
| 0.17 | 2.034 | |
| 0.33 | 2.166 / 2.821 | |
| 0.50 | **2.411 / 2.459 (2개 같음)** | **N–N bridge = saddle 위치** |
| 0.67 | 2.111 / 2.863 | |
| 0.83 | 1.972 | |
| 1.00 | 2.036 (1개) | **다른 on-N** — 큰 공 |

경로 3.241 Å (이완된 표면 기준; 이상격자 a = 3.65 Å) · 최저 Li–N 1.972 Å.
`_nobond_` 는 adatom–N 결합선을 끈 것.

## ★ 이건 표시용이다

**이 경로 위의 어떤 점도 계산된 배치가 아니다.** 표면 N 위치에서 기하로 만든 궤적이고,
높이는 `h_top` 2.10 Å / `h_bridge` 1.85 Å 로 준 대칭 프로파일이다. 에너지를 붙이면 안 된다.
우리가 수렴시킨 두 구조(0.118 eV)는 `../hop_frames/li3n_computed_*.vesta` 이고,
그 자리는 이 궤적의 자리와 다르다 — 배경은
`kb/syntheses/li3n_barrier_revision_defense_2026_08_12.md` §C4 · §C6.

캡션 문안:
> Spheres mark successive lateral positions of the Li adatom along the surface
> migration coordinate; positions are illustrative and were not separately relaxed.
> Energies were evaluated only for the configurations listed in Table S2.
