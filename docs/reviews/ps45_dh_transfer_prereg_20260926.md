# 사전등록 — d_h 접힘의 **표본 밖** 시험: ps45 침대 5 (AM_P 4.5 µm) 를 동결 선으로 예측 (2026-09-26)

> 비준 = 사용자 09-26 밤 (*"ps45 도 5개 다 끝났거덩? 그거 추가로 mpm 할까?"* → *"다 진행"* · 동결 선 = 288/φ0.75).
> 상태: ⬜ 등록 (런 전).  결과가 나오면 §6 에 채점 JSON 을 붙이고 **판정선은 건드리지 않는다**.
> 도구: 동결 = `scripts/fit_dh_collapse.py --freeze-json` · 채점 = `scripts/score_dh_transfer.py` (selftest 12/12) · 이 문서.

## 0. 질문

`docs/se_curve_transfer_verdict_20260806.md` 의 d_h 접힘 (같은 φ 에서 log σ 가 log d_h 에 선형) 은 **다섯 침대 안에서 맞춘** 것이다 (CDX-14:
*"동결한 φ 로 새 침대와 새 격자를 예측하기 전까지는 탐색적 적합"*).  AM_P 반지름을 6.0 → **4.5 µm** 로 바꾼 새 침대 5 개 (`ps_*_r45`, 사용자의
이종기술 구성에 더 가깝다) 는 d_h 가 새 값으로 나온다 ⇒ **동결한 선이 그 σ 를 맞히는가** 가 이 시험의 전부다.
새 침대의 점은 **적합에 넣지 않는다**.

## 1. 동결 선 (런 전 고정 — `docs/data/dh_frozen_288_phi075_20260926.json`)

| 항목 | 값 | 출처 |
|---|---|---|
| 형태 | ln σ[GPa] = a + b · ln d_h[µm] | `fit_dh_collapse.loglog_fit` |
| a · b | **a = −0.68317 · b = −0.57533** | 09-26 재실행 (n_grid 288 · φ 0.75 · mach 0.03 · slope-grid 192) — 기록된 값 (기울기 −0.575 · R² 0.926 · sd 0.077 · LOO 0.155) 재현 |
| R² · 잔차 sd · LOO | 0.9260 · **0.07671** · 0.1546 | 같음 |
| 다섯 점 | 0_10 (0.4807 µm · 0.8445) · 3_7 (0.5955 · 0.6347) · 5_5 (0.7147 · 0.5834) · 7_3 (0.8795 · 0.5360 · 보간) · 10_0 (1.3997 · 0.4333) | 4 침대는 최근접점 + g192 국소기울기 보정 (verdict §⑥ 규약) |
| 한정어 (그대로 전파) | \|b\| 은 288 에서의 **하한** (비수렴, 차수 ≈ 0.10) · mach 0.03 = 준정적 위반이라 **상대 전용** · 보정 방식 혼합 (verdict 표) | verdict §⑥ · CDX-14 |

⚠ d_h 288 대등화 8 런 (§5-A) 이 끝나면 다섯 침대의 288 선은 바뀐다.  **이 시험의 채점선은 이 파일로 고정**이고, 새 선으로 다시 채점하려면
새 사전등록이다 (결과를 보고 선을 고르는 것이 CDX-14 가 막은 바로 그 일이다).

## 2. 새 침대 · 프로토콜

| | 값 |
|---|---|
| 침대 | `ps_0_10_r45` · `ps_3_7_r45` · `ps_5_5_r45` · `ps_7_3_r45` · `ps_10_0_r45` — `dem_scripts/ps_sweep_6mah_20260914/README.md`: AM_P **4.5 µm** (옛 6.0) · AM_S 2.0 · SE 0.5 · 6 mAh · 50 × 50 µm · 300 MPa · 새 시드 |
| DEM 산출 | 사용자 Windows `F:\DEM\examples\LIGGGHTS\Tutorials_public\1. ASSB\post_bimodal_real_P9\post_ps_{0_10,3_7,5_5,7_3,10_0}_r45` (WSL `/mnt/f/…`).  ⚠ r2 · r3 재시작이 덤프를 덮었다 — **최종 atom 덤프가 완주 궤적의 것인지** 로그 마지막 step 과 대조 |
| 스캐폴드 | 옛 킷과 같은 경로: 웹앱 업로드 (`parse_liggghts.py` — 최고 번호 덤프 + 덱) → `mpm_input_from_case.py` → `am_scaffold.csv` · `se_scaffold.csv`.  ⚠ 덱 이름 `in.ps_*_r45.liggghts` 는 `input*` 글롭에 안 걸려 lateral box 가 최대 x·y 로 떨어진다 → `mpm_input.json` 의 lateral 이 **0.050013** (옛 킷) 인지 확인 |
| MPM | d_h 288 대등화와 **같은 프로토콜** (`scripts/run_se_curve_batch.sh`): n_grid **288** · sub 160 · `--protocol hold --periodic --platen-mach 0.03` · `--compact-to ε` · **첨가제 없음** (옛 se_curve 런과 같음 — 킷 run_mpm.sh 의 VGCF/PTFE 는 쓰지 않는다) · 킷 이름 `kit_ps_*_r45` (fit 글롭이 옛 킷과 안 섞이게) |
| φ 점 | 침대당 **0.66 · 0.72 · 0.81** 세 점 (0.75 를 **감싼다** → 보간, 국소기울기 보정 없음) |
| 기계 | v100 (`~/Yonghoon-DEM-DFT/se_curve` · 코드 `~/dem-sk`) — d_h 288 8 런과 같은 큐 |

## 3. 예측 (런 전)

- 규칙: 침대마다 실제 스캐폴드로 `d_h(φ 0.75) = (V_SE/0.75)/S_AM` (fit_dh_collapse 규약 · S_AM = Σ4πr², 겹침 미보정) 을 계산하고
  **σ_pred = exp(a + b · ln d_h)**.  σ_meas 는 0.66–0.81 두 점의 σ-선형 보간값 (select_at_phi).
- 설계 개수로 미리 본 자리 (실제 스캐폴드로 다시 계산 — 이 숫자는 예시): d_h ≈ 0.50 / 0.60 / 0.69 / 0.82 / 1.13 µm →
  σ_pred ≈ 0.75 / 0.68 / 0.62 / 0.57 / 0.47 GPa.  다섯 값이 동결 선의 d_h 범위 (0.48–1.40 µm) **안**이다 = 보간 영역.
- 저해상 표지: dx = 54.35/288 = 0.189 µm → d_h/dx ≈ 2.7 / 3.2 / 3.7 / 4.3 / 6.0 ⇒ **0_10 · 3_7 는 3.5 셀 미만** (verdict §⑤ 규칙).
  채점에서 빼지 않고 표지만 붙인다.  미해상 협착은 σ 를 **낮게** 내므로 이 두 침대가 밖이면 **r < 0** 이 예상 방향이다 —
  r > 0 으로 밖이면 해상도 설명이 안 된다 (그때는 접힘 자체의 문제).

## 4. 판정선 (런 전 등록 — `score_dh_transfer.py` 가 그대로 구현)

| | |
|---|---|
| 잔차 | r = ln(σ_meas / σ_pred) |
| 띠 | **±2 · sd = ±0.1534** (sd 0.07671 · 동결 선의 잔차 sd).  참고: LOO 기울기 흔들림 0.155 도 같은 크기 |
| **TRANSFERS** | 5/5 가 띠 안 |
| **PARTIAL** | 정확히 1 침대가 밖 |
| **FAILS** | 2 침대 이상 밖 |
| **HOLD** | 어느 침대라도 0.75 를 못 감싸 외삽 (method ≠ interp) 이거나 점이 없음 — 국소기울기 보정으로 구제하지 않는다 |
| 예측 | **TRANSFERS** (h1 — 접힘이 표본 밖으로 전이한다).  h0 = FAILS.  PARTIAL 은 어느 쪽도 아니라 *"한 침대 예외"* 로만 적는다 |
| 인용 규약 | TRANSFERS 여도 \|b\| 는 하한 · 상대 전용 · **"established" · "transferable" 낱말은 CDX-14 대로 새 격자 예측까지 쓰지 않는다** — 쓸 수 있는 문장: *"동결한 288/φ0.75 선이 AM_P 4.5 µm 침대 5 개의 σ 를 ±2 sd 안에서 예측했다"* |

## 5. 실행 (v100) — 순서

**A. d_h 288 대등화 8 런 (verdict §⑩ 에 08-11 등록 — 그대로)**
```
cd ~/dem-sk && git fetch origin claude/stoic-knuth-NObVQ && git checkout claude/stoic-knuth-NObVQ && git pull --ff-only && git status --short   # 깨끗해야
nvidia-smi --query-gpu=memory.used,memory.total --format=csv                                   # 288 은 ~15 GB 필요
cd ~/Yonghoon-DEM-DFT/se_curve
bash ~/dem-sk/scripts/run_se_curve_batch.sh --repo ~/dem-sk --data ~/Yonghoon-DEM-DFT \
  --kits kit_ps_0_10,kit_ps_3_7,kit_ps_5_5,kit_ps_10_0 --phi 0.66,0.72,0.81 --n-grid 288 \
  --sub 160 --mach 0.03 --gpu-mem 28 --tag eq288 --skip-existing --dry                          # 8 runs · 4 skips 여야
setsid nohup bash ~/dem-sk/scripts/run_se_curve_batch.sh --repo ~/dem-sk --data ~/Yonghoon-DEM-DFT \
  --kits kit_ps_0_10,kit_ps_3_7,kit_ps_5_5,kit_ps_10_0 --phi 0.66,0.72,0.81 --n-grid 288 \
  --sub 160 --mach 0.03 --gpu-mem 28 --tag eq288 --skip-existing > ~/eq288.log 2>&1 &
```
끝나면 (같은 다섯 침대의 새 288 선 — **이 사전등록의 채점선이 아니다**):
`python3 ~/dem-sk/scripts/fit_dh_collapse.py --dir ~/Yonghoon-DEM-DFT/se_curve --n-grid 288 --mach 0.03 --phi 0.75 --list` → `--phi 0.75` → `--phi 0.72`.

**B. ps45 스캐폴드 (사용자 WSL — 웹앱과 같은 경로)**
```
# 침대마다 (post_ps_<P>_<S>_r45): 최종 atom 덤프 번호 = 로그 마지막 step 인지 먼저 확인
ls -1 "/mnt/f/DEM/examples/LIGGGHTS/Tutorials_public/1. ASSB/post_bimodal_real_P9/post_ps_7_3_r45" | sort -V | tail -3
# 웹앱 업로드 (atom_* · contact_* · *.stl · 덱 in.ps_*_r45.liggghts) → 케이스 id 확인 → 스캐폴드
python3 scripts/mpm_input_from_case.py --results webapp/results/<case_id> --out /tmp/kit_ps_7_3_r45
python3 -c "import json;print(json.load(open('/tmp/kit_ps_7_3_r45/mpm_input.json')).get('lateral_box'))"      # 0.050013 이어야
```
이미 웹앱에 있는 케이스: ps_10_0 `260922_092001_0853b1` · ps_0_10 `260925_000001_0bee25` · ps_3_7 `260925_000448_bd85f9` — 5_5 · 7_3 은 업로드.
다섯 킷 (`am_scaffold.csv` · `se_scaffold.csv` · `mpm_input.json`) 을 v100 `~/Yonghoon-DEM-DFT/se_curve/kit_ps_<P>_<S>_r45/` 로 (scp).
사전 계산 (GPU 불요): `python3 scripts/phase_a_precompute.py --am <am.csv> --se <se.csv> --thickness-um <h> --lateral-um 50.013 --out <json>`
→ d_h/dx 를 §3 표지와 대조 (이 도구는 dx = lateral/n 규약이라 8.7 % 후하다 — 표지는 verdict 규약 54.35/n 으로).

**C. ps45 15 런 (v100 · A 뒤)**
```
cd ~/Yonghoon-DEM-DFT/se_curve
bash ~/dem-sk/scripts/run_se_curve_batch.sh --repo ~/dem-sk --data ~/Yonghoon-DEM-DFT \
  --kits kit_ps_0_10_r45,kit_ps_3_7_r45,kit_ps_5_5_r45,kit_ps_7_3_r45,kit_ps_10_0_r45 --phi 0.66,0.72,0.81 \
  --n-grid 288 --sub 160 --mach 0.03 --gpu-mem 28 --tag eq288r45 --dry                         # 15 runs 여야
setsid nohup bash ~/dem-sk/scripts/run_se_curve_batch.sh --repo ~/dem-sk --data ~/Yonghoon-DEM-DFT \
  --kits kit_ps_0_10_r45,kit_ps_3_7_r45,kit_ps_5_5_r45,kit_ps_7_3_r45,kit_ps_10_0_r45 --phi 0.66,0.72,0.81 \
  --n-grid 288 --sub 160 --mach 0.03 --gpu-mem 28 --tag eq288r45 > ~/eq288r45.log 2>&1 &
```
**D. 채점 (결과를 보기 전에 명령을 그대로)**
```
python3 ~/dem-sk/scripts/score_dh_transfer.py --frozen ~/dem-sk/docs/data/dh_frozen_288_phi075_20260926.json \
  --dir ~/Yonghoon-DEM-DFT/se_curve --kit-root ~/Yonghoon-DEM-DFT/se_curve \
  --kits kit_ps_0_10_r45,kit_ps_3_7_r45,kit_ps_5_5_r45,kit_ps_7_3_r45,kit_ps_10_0_r45 --n-grid 288 --mach 0.03 \
  --out ~/ps45_score_$(date +%Y%m%d).json
```
채점 JSON · 15 개 `xfer_eq288r45_*.json` · 다섯 킷 스캐폴드를 리포 `docs/data/ps45_dh_transfer_20260926/` 에 커밋 (원자료).

## 6. 결과 (런 뒤 — 판정선 불변)

(비어 있음)
