# Li3N(001) on-N → bridge → on-N 궤적 (그림 전용) — **N28 → N32 고정**

패널 (c) 인셋(계산된 두 구조)과 **같은 영역**에 오도록 N 짝을 고정했다.
슬랩 중앙 버전(N20 → N36)은 인셋과 위치가 어긋나 폐기.

## 재생성 (항상 같은 자리)

```
python3 tools/neb_diffusion/li3n_hop_frames.py --onN --n1 N28 --n2 N32 \
  --min <min.vesta> --ts <ts.vesta> \
  --h_top 2.10 --h_bridge 1.85 --ghost_r 0.62 --end_r 1.30 \
  --xi 0,0.1667,0.3333,0.5,0.6667,0.8333,1.0 \
  --outdir docs/figures/li3n/onN_path --merge          # 필요시 --no_bonds
  # --merge 빼면 single/ 에 낱장 7장 (병합본과 좌표 동일)
```

| | 표면 N | frac |
|---|---|---|
| 시작 on-N | **N28** | (0.698387, 0.015906, 0.403020) |
| 끝 on-N′ | **N32** | (0.665328, 0.330757, 0.406483) |

`--n1/--n2` 를 빼면 자동 선택이라 기준이 바뀌면 그림이 움직인다. **항상 지정할 것.**

## 강조 3점 + 보간 4점

| ξ | | 표면 N (Å) | 자리 |
|---|---|---|---|
| 0.00 | ★ 1.30 Å | 2.100 (1개) | **on-N (atop)** |
| 0.17 / 0.33 | 0.62 Å | 2.053 / 2.236 | 보간 |
| **0.50** | ★ | **2.526 / 2.596 (2개)** | **N–N bridge = saddle 위치** |
| 0.67 / 0.83 | 0.62 Å | 2.154 / 1.959 | 보간 |
| 1.00 | ★ | 2.001 (1개) | **on-N′** |

경로 3.642 Å · 최저 Li–N 1.959 Å.

## 파일

| | |
|---|---|
| `li3n_hop_alladatoms_display.vesta` | 7위치 한 장 (결합선 있음) |
| `li3n_hop_alladatoms_nobond_display.vesta` | 7위치 한 장 (결합선 없음) |
| `single/li3n_hop_xi***_adNa_display.vesta` | 낱장 7장 |

## ★ 표시용이다

**이 경로 위의 어떤 점도 계산된 배치가 아니다.** 표면 N 위치에서 기하로 만든 궤적이고
높이는 h_top 2.10 / h_bridge 1.85 Å 대칭 프로파일이다. 에너지를 붙이면 안 된다.
수렴시킨 두 구조(ΔE = 0.118 eV)는 `../hop_frames/li3n_computed_*.vesta`.

**min → TS → 대칭끝점 직선은 못 그린다** — ξ≈0.82 에서 Li–N 이 1.29–1.35 Å 로
N 을 관통한다 (높이를 2.5 Å 까지 올려도 해소 안 됨, 2026-08-12 실측).

캡션 문안:
> Spheres mark successive lateral positions of the Li adatom along the surface
> migration coordinate; positions are illustrative and were not separately relaxed.
> Energies were evaluated only for the configurations listed in Table S2.
