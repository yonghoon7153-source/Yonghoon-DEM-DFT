# P:S 스윕 — 이종기술 6 mAh/cm² 재런 (2026-09-14)

랩 사양표(2026-09-14)에 맞춘 **조성 5점** LIGGGHTS 덱.  원본은
`docs/data/phase_a_6mah/in.real_4.liggghts` 이고, 생성기는
`scripts/make_ps_sweep_decks.py` 다 (재생성 멱등 — 아래 명령이 같은 파일을 낸다).

## 1. 4/21 세대와 무엇이 다른가 — **AM_P 반지름 하나**

`docs/data/kit_ps_scaffolds/` 에 이미 같은 5점이 있다 (케이스 `260421_21*`).
그 세대와 이번 것의 차이는 **AM_P 반지름 6.0 → 4.5 µm** 뿐이다.

| 항목 | 4/21 세대 | 이번 (사양표) | 근거 |
|---|---|---|---|
| AM_P radius | **6.0 µm** | **4.5 µm** | `docs/case_summary.csv` 의 `fm__R_min_um_median_AM_P-AM_P` = 6.0 (실측) ↔ 사양표 `radius(um)_P` = 4.5 |
| AM_S radius | 2.0 µm | 2.0 µm | 불변 |
| SE radius | 0.5 µm | 0.5 µm | 불변 |
| AM:SE (질량) | 81.6 : 18.4 | 81.6 : 18.4 | 불변 |
| RVE · 면용량 · 압력 | 50×50 µm · 6 mAh/cm² · 300 MPa | 동일 | 불변 |
| 시드 | real_4 의 것 그대로 | **케이스마다 독립 8자리 소수** | 아래 §4 |

⚠ **SE 영률은 사양표의 값이 아니다.**  표는 LPSCl `영률 2.40E+10 Pa`(= 24 GPa, 실bulk)를
적지만 덱에는 **1.35 GPa** (`0.135e7` = 1.35e9 × 0.001)가 들어간다.  이 리포의 모든 침대가
그 18배 연화 규약 위에 있고(`CLAUDE.md` §E_SE calibration — pure-SE Cronau 겹침 11–12 % ·
독립 MPM 이 같은 18배를 요구), 코퍼스와 비교하려면 같은 규약이어야 한다.
AM 영률은 표와 일치한다 (1.40E+11 × 0.001 = `1.4e8`).

## 2. 다섯 덱

| P:S | 파일 | 질량분율 (덱 표기) | AM_P | AM_S | SE | 합 |
|---|---|---|---:|---:|---:|---:|
| 10:0 | `in.ps_10_0_r45.liggghts` | `pts1 0.816 pts3 0.184` | 402 | 0 | 158,765 | 159,167 |
| 7:3 | `in.ps_7_3_r45.liggghts` | `pts1 0.5712 pts2 0.2448 pts3 0.184` | 282 | 1,375 | 158,765 | 160,422 |
| 5:5 | `in.ps_5_5_r45.liggghts` | `pts1 0.408 pts2 0.408 pts3 0.184` | 201 | 2,292 | 158,765 | 161,258 |
| 3:7 | `in.ps_3_7_r45.liggghts` | `pts1 0.2448 pts2 0.5712 pts3 0.184` | 121 | 3,209 | 158,765 | 162,095 |
| 0:10 | `in.ps_0_10_r45.liggghts` | `pts2 0.816 pts3 0.184` | 0 | 4,584 | 158,765 | 163,349 |

입자수는 **예측**이다 (질량분율 → 부피분율 → 개수).  사양표의 `입자수_P / 입자수_S /
전체 입자수` 칸이 비어 있어 여기서 채운다.  ⚠ **런 뒤 실제 개수와 대조할 것** — 4자릿수
어긋나면 `particledistribution/discrete` 가 **개수분율**로 읽힌 것이고, 그러면 침대가
아예 다른 물건이다.  4/21 실측이 이 예측과 맞는 것이 규약이 질량분율이라는 증거다
(10:0 AM_P 실측 175 ↔ r=6.0 예측 170 · SE 실측 158,730 ↔ 예측 158,765).

AM_P 가 2.37배 많아지는 것 = (6.0/4.5)³.  SE·AM_S 개수는 그대로라 전체 입자수는
16만 근처로 4/21 세대와 사실상 같다 — **런 비용은 비슷하다**.

## 3. 실행

```bash
cd dem_scripts/ps_sweep_6mah_20260914
mpirun --oversubscribe -np 10 liggghts -in in.ps_10_0_r45.liggghts 2>&1 | tee log_ps_10_0_r45.out
mpirun --oversubscribe -np 10 liggghts -in in.ps_7_3_r45.liggghts 2>&1 | tee log_ps_7_3_r45.out
mpirun --oversubscribe -np 10 liggghts -in in.ps_5_5_r45.liggghts 2>&1 | tee log_ps_5_5_r45.out
mpirun --oversubscribe -np 10 liggghts -in in.ps_3_7_r45.liggghts 2>&1 | tee log_ps_3_7_r45.out
mpirun --oversubscribe -np 10 liggghts -in in.ps_0_10_r45.liggghts 2>&1 | tee log_ps_0_10_r45.out
```

각 덱은 자기 이름의 `post_ps_<비>_r45/` · `restart_ps_<비>_r45/` · `plate_ps_<비>_r45.stl`
을 만든다 — 4/21 세대(`post_real_4/`)와 **겹치지 않는다**.

런이 끝나면 개수부터 대조한다:

```bash
for f in post_ps_*_r45/atom_*.liggghts; do :; done   # 마지막 덤프
awk 'NR==4{n=$1} NR>9{c[$2]++} END{printf "%s  총 %d  AM_P %d  AM_S %d  SE %d\n", FILENAME, n, c[1], c[2], c[3]}' \
    post_ps_7_3_r45/atom_0.liggghts
```

## 4. 시드 — 케이스마다 독립인 8자리 소수

| P:S | pts1(AM_P) · pts2(AM_S) · pts3(SE) · 분포 · 삽입 |
|---|---|
| 10:0 | `20000003, 21300029, 22600001, 23900027, 25200011` |
| 7:3 | `27000011, 28300001, 29600003, 30900013, 32200031` |
| 5:5 | `34000009, 35300017, 36600007, 37900039, 39200041` |
| 3:7 | `41000017, 42300001, 43600013, 44900029, 46200043` |
| 0:10 | `48000013, 49300033, 50600009, 51900019, 53200009` |

- **전부 소수**이고 **전부 다르다** (생성기 selftest 가 25개를 매번 검사한다).
- 자릿수는 원본 덱과 같은 대역(1e7–1e8)에 뒀다 — LIGGGHTS/LAMMPS 의 RanPark 가 9e8 위를
  거부하는 판이 있다.  원본의 삽입 시드 `80363` 은 5자리였다.
- **압력 스윕과 반대로 시드를 얼리지 않는다**: 조성이 바뀌면 삽입 스트림이 첫 입자부터
  갈라져 "같은 패킹" 이라는 것이 존재하지 않는다.  얼리고 싶으면 `--shared-seeds`.

## 5. 알아 둘 것 (건드리지 않은 것)

- `variable plate_z equal ${z_max}+${r_AM_P}+${plate_margin}` 는 **모든 케이스가 r_AM_P**
  를 쓴다.  0:10 은 가장 큰 입자가 AM_S(2 µm)인데도 플래튼이 4.5 mm 위에서 출발한다 =
  접근 스트로크가 2.5 mm 더 길다 (`press_speed` 0.01 → 스텝 몇 십만 개).  **결과가 아니라
  시간 비용**이고, 원본 규약이라 그대로 뒀다.
- 접촉법칙 · `coefficient*` 9종 · `dt` · `press_speed` · `target_press` ·
  `volumefraction_region` · run 스텝수 · RVE 전부 원본과 **바이트 동일**하다.

## 6. 재생성

```bash
python3 scripts/make_ps_sweep_decks.py \
    --deck docs/data/phase_a_6mah/in.real_4.liggghts \
    --ratios 10:0,7:3,5:5,3:7,0:10 --r-am-p 4.5e-3 \
    --tag-prefix ps --tag-suffix _r45 \
    --note '이종기술 6 mAh/cm² 재런 (2026-09-14 랩 사양표) — 4/21 세대 대비 AM_P 반지름 6.0 → 4.5 µm 만 변경.' \
    --out dem_scripts/ps_sweep_6mah_20260914 --mpi 10
```
