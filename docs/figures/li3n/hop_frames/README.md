# Li3N(001) hop 프레임 (VESTA 표시용)

생성: `python3 tools/neb_diffusion/li3n_hop_frames.py --min <min.vesta> --ts <ts.vesta>
--outdir docs/figures/li3n/hop_frames --to_frac 0.776701,0.231705
--xi 0,0.1667,0.3333,0.5,0.6667,0.8333,1.0`

## 무엇인가

`li3n_hop_xi***_adNa_display.vesta` 7장 = 흡착 최소점에서 **이웃 등가 자리**까지 2.107 Å를
7등분한 adatom 궤적. 기판은 최소점 구조를 고정으로 쓰고 adatom(표시용 Na 라벨)만 움직인다.
경로상 Li–N 최소 2.055 Å — N 을 관통하지 않는다.

| xi | 표면 N 배위 (Å) | 무엇 |
|---|---|---|
| 0.00 | 2.170 / 2.186 / 2.379 | 3-fold 자리 = **계산된 흡착 최소점** |
| 0.33–0.50 | 2.055 / 2.078 · 2.087 / 2.113 | N–N 다리 통과 |
| 1.00 | 2.410 / 2.499 / 2.528 | 이웃 3-fold 자리 (등가) |

`li3n_computed_min_adNa_display.vesta` · `li3n_computed_saddle_adNa_display.vesta`
= 수렴한 DFT 구조 2장 (E = −2176.44473796 / −2176.43605123 Ry, ΔE = 0.1182 eV).

## 캡션에 반드시 들어가야 하는 것

중간 5장은 **계산된 배치가 아니라 직선 보간 궤적**이다. 에너지를 붙이면 안 된다.

## 알려진 문제 (2026-08-12)

계산된 안장점은 이 hop 직선 위 **xi = 1.20**, 즉 도착지보다 0.43 Å 더 멀다. 따라서
이 2.107 Å hop 자체의 안장점(xi≈0.5 의 N–N 다리)은 계산된 적이 없다. 배경과 대응은
`kb/syntheses/li3n_barrier_revision_defense_2026_08_12.md` §C6.
