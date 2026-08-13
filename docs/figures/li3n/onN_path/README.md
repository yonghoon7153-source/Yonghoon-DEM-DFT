# Li3N(001) on-N → bridge → on-N 궤적 (그림 전용)

```
python3 tools/neb_diffusion/li3n_hop_frames.py --onN --merge \
  --min <min.vesta> --ts <ts.vesta> --outdir docs/figures/li3n/onN_path \
  --h_top 2.10 --h_bridge 1.85 --ghost_r 0.62 --end_r 1.30 \
  --xi 0,0.1667,0.3333,0.5,0.6667,0.8333,1.0
```

**강조 3점 + 보간 4점** (큰 공 / 작은 공):

| ξ | | 자리 |
|---|---|---|
| 0.00 | ★ 큰 공 | **on-N (atop)** |
| 0.17, 0.33 | 작은 공 | 보간 |
| **0.50** | ★ 큰 공 | **N–N bridge = saddle 위치** |
| 0.67, 0.83 | 작은 공 | 보간 |
| 1.00 | ★ 큰 공 | **on-N′ (이웃 N)** |

경로 3.575 Å · 최저 Li–N 2.050 Å · N–N 짝은 **슬랩 중앙**의 것을 고른다
(adatom 최근접으로 고르면 가장자리에 붙어 렌더에서 잘린다).
`_nobond_` 는 adatom–N 결합선을 끈 것.

## ★ 표시용이다

**이 경로 위의 어떤 점도 계산된 배치가 아니다.** 표면 N 위치에서 기하로 만든 궤적이고,
높이는 `h_top` 2.10 Å / `h_bridge` 1.85 Å 대칭 프로파일이다. 에너지를 붙이면 안 된다.
수렴시킨 두 구조(ΔE = 0.118 eV)는 `../hop_frames/li3n_computed_*.vesta` 이고 자리가 다르다
— `kb/syntheses/li3n_barrier_revision_defense_2026_08_12.md` §C4 · §C6.

캡션 문안:
> Spheres mark successive lateral positions of the Li adatom along the surface
> migration coordinate; positions are illustrative and were not separately relaxed.
> Energies were evaluated only for the configurations listed in Table S2.
