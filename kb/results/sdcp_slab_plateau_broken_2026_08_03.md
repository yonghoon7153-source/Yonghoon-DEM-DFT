# SDCP 슬랩 plateau 를 깼다 — 원인은 계가 아니라 Broyden 이력 (2026-08-03)

## 한 줄
96원자 LiNiO₂(104) 슬랩이 두 달 동안 limit cycle 로 안 잡혔는데, **plateau 밀도를
`startingpot='file'` 로 물려 SCF 를 다시 시작하니 30 iteration 만에 수렴했다.**
즉 한계고리의 원인은 이 계의 물리가 아니라 **혼합 이력**이었다.

## 무엇이 철회되나
2026-08-01 에 등록한 판정 — "이 슬랩의 plateau 는 정상 거동이다, degauss 를 넓혀도
안 잡히니 수용하고 2단계로 간다" — 를 **부분 철회**한다.

- 유지되는 부분: plateau 값의 오차막대 산정(±0.0075 Ry), 그리고 **슬랩이 verdict 에서
  상쇄되므로 plateau 로도 2단계에 갈 수 있다**는 판단. 실제로 갱신값은 오차막대 안이었다.
- 철회되는 부분: "이 계는 원래 안 잡힌다"는 **원인 귀속**. 잡힌다.

## 무엇이 들었나
| 시도 | acc_end (Ry) | 결과 |
|---|---|---|
| degauss 0.05 / beta 0.10 / ndim 8 | 6.2e-3 | limit cycle |
| degauss 0.03 / beta 0.03 / ndim 8 | 5.0e-3 | limit cycle |
| 위 밀도 + `startingpot='file'` + maxstep 30 | **수렴** | `convergence has been achieved in 30 iterations` |

세 번째가 앞의 둘과 다른 점은 **밀도가 좋아진 것이 아니라 Broyden 이력이 비워진 것**이다
(밀도는 두 번째 판의 결과물 그대로다). 긴 이력이 진동을 고착시킨다는 기존 가설과
방향은 같지만, 처방이 다르다: `mixing_ndim` 을 줄이는 것만으로는 부족했고 **이력을
통째로 리셋**해야 빠져나왔다.

## 처방 (이 계 재현용)
```
1. degauss 0.03 · mixing_beta 0.03 · mixing_mode local-TF · mixing_ndim 8 로 돌린다
2. plateau 에 들어가면 (진동률 ~50%, 자화 안정) 그대로 두지 말고 **죽인다**
3. 같은 디렉터리에서 startingpot='file' 로 재시작 (밀도만 승계, wfc 아님 —
   restart_mode='restart' 는 disk_io='low' 와 충돌한다)
4. electron_maxstep 은 넉넉히. 이번엔 30 에서 정확히 걸렸다 — 한 스텝만 더 필요했으면
   미수렴으로 끝났을 값이다.
```

## 확정된 슬랩
```
!    total energy = -10563.23044425 Ry     (수렴, '!' 줄)
     total magnetization    =   0.01 Bohr mag/cell
     absolute magnetization = 110.99 Bohr mag/cell
```
- plateau 값 대비 **−30.7 meV** — 기존 오차막대 ±102 meV 안쪽. plateau 규약이 사후 검증됐다.
- E_bind 절대값은 doped −1.4937 / neutral −2.1827 eV 로 각각 +30.7 meV 이동.
- **차분 +0.6890 eV 는 한 자리도 안 변한다** (슬랩이 두 갈래에서 상쇄).

## Ni 시드 (slab_mag.json)
| 종 | n | mean (μB) | range |
|---|---|---|---|
| Ni1 | 12 | +1.020 | [+1.014, +1.028] |
| Ni2 | 12 | −1.020 | [−1.028, −1.012] |
| Li | 24 | +0.002 | [−0.047, +0.046] |
| O | 48 | −0.002 | [−1.729, +1.717] |

- **|Ni| = 1.02 μB 는 저스핀 Ni³⁺ (d⁷, t2g⁶ eg¹, S=1/2) 와 정확히 맞는다.** LiNiO₂ 에서
  기대되는 값이고, 고스핀(≈3 μB)이 아니다 → U 값과 AFM 배치가 물리적으로 맞게 앉았다.
- AFM 대칭성 Ni1+Ni2 = 0.000 μB ✓
- 시드는 관례대로 **부호만 승계하고 크기는 ±0.3 분율**(과분극 출발)을 쓴다.
  수렴값 분율은 0.102 로 더 작은데, AFM+U 는 과분극 출발이 안전하다는 관례를 따른다.

### ⚠ 미해결: O 자리 자화 산포
O 48개가 mean ≈ 0 인데 range 가 ±1.7 μB 로 **Ni(1.02)보다 크다**. 매핑 오류는 아니다
(Ni1/Ni2/Li 가 전부 좁은 산포로 자기일관적이라, 순서가 섞였으면 부호가 섞여야 한다).
LiNiO₂ 의 O 2p ligand-hole 성격으로 읽을 여지가 있으나 **크기가 크다** — 2단계가 끝난 뒤
z-층별로 분해해 볼 것. 시드에는 영향 없다(Ni 만 쓴다).

## 곁가지: tprnfor 를 껐다
SCF 수렴 후 슬랩이 멈춘 것처럼 보였는데, 실은 `tprnfor=.true.` 의 **PAW+U 힘 항**을
35분+ 100% 로 돌고 있었다 (총 elapsed 1h48m, `JOB DONE` 0, `tstress` 는 이미 .false.).
이 경로는 5개 job 전부 단일점 scf 이고 E_bind 는 총에너지 차분이라 힘을 안 쓴다
→ `TPRNFOR` 노브를 만들어 **기본 .false.** 로 바꿨다. 130/131 원자 복합체에서
그대로 뒀으면 job 마다 몇 시간을 버렸을 것이다.

## 관련 파일
- `db/properties/sdcp_v7c_phaseB_energies.csv` — `slab_slabfirst` 행 추가 + 철회 주석
- `tools/sdcp/run_phaseB_slabfirst_gabia.sh` — `TPRNFOR` 노브
- `tools/sdcp/phaseB_v7c_dft_binding.py` — `--tprnfor` (기본 .false.)
- `tools/sdcp/slab_mag_from_scfout.py` — 시드 수확
- `/data/work/runs/sdcp_linio2_binding/phaseB_v7c_slabfirst/slab_mag.json` (gabia)
