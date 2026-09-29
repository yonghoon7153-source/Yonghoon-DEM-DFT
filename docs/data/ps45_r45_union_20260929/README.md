# r4.5 P:S 침대 5 개 — union porosity (2026-09-29)

계기: 동료 (작은태영) 요청 09-29 16:25 — *"면6 · Poly 9 µm 의 porosity"* → 1저자 *"porosity union 으로 해서 보내줘야 될듯"*.
COMSOL 커플링 담당에게 넘기는 인계문 = [`HANDOVER_COMSOL.md`](HANDOVER_COMSOL.md).

## 무엇

- 침대 = 이종기술 6 mAh/cm² P:S 스윕 r4.5 세대 (`dem_scripts/ps_sweep_6mah_20260914/README.md` — AM_P r 4.5 µm · AM_S r 2.0 · SE r 0.5 · AM:SE 질량 81.6 : 18.4 · 50 × 50 µm · 300 MPa).
- 프레임 = 웹앱 케이스의 업로드 덤프 그대로 (ps45 사전등록 `docs/reviews/ps45_dh_transfer_prereg_20260926.md` §5-B 킷 표와 같은 케이스 · 같은 step).
- 값 = [`r45_union_summary.tsv`](r45_union_summary.tsv) (사용자 WSL 출력 전사 · 전 열 TSV 는 WSL `~/r45_union_20260929/r45_union.tsv` — ⬜ 반입하면 상별 union 부피 열 `mc_*` 도 붙는다).

| P:S | union 정확 (%) | ± MC 1σ | union 쌍 렌즈 (웹앱) | 구 부피 합 (웹앱 기본) | 두께 (µm) |
|---|---|---|---|---|---|
| 10:0 | **16.90** | 0.02 | 16.90 | 15.82 | 112.6 |
| 7:3 | **16.49** | 0.02 | 16.45 | 14.95 | 111.1 |
| 5:5 | **17.67** | 0.02 | 17.66 | 16.20 | 112.4 |
| 3:7 | **18.67** | 0.02 | 18.63 | 17.16 | 114.4 |
| 0:10 | **20.59** | 0.02 | 20.60 | 19.16 | 117.2 |

## 실행 · 검산 (09-29 오후 · WSL `DESKTOP-IK8J81H` · `~/dem-web` @ `a7350572f`)

```
REPO=~/dem-web ~/Yonghoon-DEM-DFT/venv/bin/python3 ~/dem-web/scripts/lhs_union_webapp.py \
  --scan-root ~/r45_union_20260929 --n-types 3 --family ps45_r45 --out ~/r45_union_20260929/r45_union.tsv
```
(`<root>/<case>/post` = 웹앱 `uploads/<case_id>` 심볼릭 링크 · 다섯 케이스 모두 같은 step 의 atom · contact · mesh 가 있었다)

- selftest PASS · status OK 5 / 5 · 정확 union 음수 0 · 쌍 clipped < 정확 (상한 위반) 0 · sphere 웹앱 ↔ dual 차 0.
- 접촉 덤프 `delta` 열 ↔ 좌표 겹침 최대 **1.99e-03** (문턱 1 % 의 1/5 — LHS 코호트 3.9e-4 보다 크나 통과).
- 중앙 겹침 / 상자 = **1.45 %** (= union 과 구 부피 합의 차).

## 한정어

- **조성마다 침대 1 개 (시드 1 개)** — MC 오차 (0.02 %p) 는 있지만 **침대 간 산포는 재지 않았다**.  7:3 이 다섯 중 가장 낮은 것 (10:0 보다 0.40 %p) 은
  MC 오차의 20 배지만 시드 산포보다 큰지는 모른다 (순수 SE 두 시드 차 = 0.03–0.05 %p · 복합체는 미측정).
- union = 강체 구를 겹친 그대로 합친 **형상**의 빈 부피다.  웹앱 기본 (구 부피 합 · ε_sphere) 은 겹침을 두 번 세고, CLAUDE.md 규약상 소성 압밀의
  재료 보존 공극으로는 ε_sphere 가 생산 규약이다 — 둘은 **병기**한다 (LHS 인계 J19 와 같은 규칙).
