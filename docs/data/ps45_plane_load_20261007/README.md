# 단면 하중 몫 — 발표 5 쪽 힘 그래프를 보존량으로 (10-07)

- **무엇**: 발표 5 쪽 "Force contribution (%)" (접촉 법선력 **크기 합**의 접촉 종류별 몫) 대신, **수평 단면을 지나는 수직 하중의 몫** — 1저자 10-07
  (리뷰 의견 *"이해하기 어렵다"* → *"힘은 보존이 되나?"* → 단면 하중 몫 권고 → *"한번 진행해봐"*).
- **왜**: 크기 합은 보존량이 아니다 — 같은 하중이 직렬로 놓인 접촉 수만큼 여러 번 세어진다 (real14: 크기 합 = 가운데 단면 하중의 **12.19 배**).
  단면 하중은 힘 평형으로 높이마다 같다 (real14: 유효 단면 21 개 최대 ÷ 최소 **1.0009**).
- **도구**: `scripts/plane_load_share.py` (읽기 전용 · 정의 · 벽 처리 · 상태 = 머리말 · `--selftest` 54/54 — 직렬 · 평행 기둥 · id 순서 · 가로 힘 · 결손 접촉 · 얇은 침대 ·
  무게 · 압력 환산 · 배치 파일 끝까지 + 10-07 Q1 · Q2 (아래 §0 · §3): 하중 가중 21 단면 평균 · 연속 극한 · 슬라이드 머리 · `--rewrite` · α 해석해 · 닫힘 · 가장자리 분해 ·
  없는 상 null · UNDEFINED · 봉인 로더 끝까지).  시험 먼저 — 고치기 전 코드 25/54 (새 시험 30 중 29 FAIL) → 54/54 · 변이 10 개 전부 잡힘.

## 0. 슬라이드 = Contribution to σ_zz (1저자 10-07 Q1 · *"Q1, Q2 reference 논문이 있음 이걸로 진행을 하자"*)

| 항목 | 값 |
|---|---|
| 축 이름 | **Contribution to σ_zz (%)** |
| 범례 (Long Name) | AM–AM contacts · AM–SE contacts · SE–SE contacts |
| 캡션 (그대로) | *Contribution of each contact type to the vertical stress, σ_zz = (1/V) Σ_c f_z l_z, evaluated as the mean over 21 horizontal planes* |
| 값 | `ps45/plane_load_share_slide.csv` = 21 단면 평균 **Σ_k F_X(z_k) ÷ Σ_k F(z_k)** (단면 하중 합의 평균끼리의 비 · 하중 가중) — 요약 CSV `(mean)` 열과 같은 값 |
| 가운데 단면 몫 | 요약 CSV `(mid)` 열에 그대로 (따로 슬라이드 파일 없음) |
| 연속 극한 | 창 [2 r_max, 판 − 2 r_max] 의 (1/V) Σ_c f_z l_z 접촉 유형 몫 (접촉마다 f_z^up × 중심 사이 가지가 창과 겹친 길이) — JSON `contribution_sigma_zz_integral_pct` · real14 에서 21 단면 평균과 ≤ 0.021 %p |

- **문헌 틀** [원문 미확인 — litdb 카드 전 · 검색 단계 · 제목 · 권호 · 값을 원문으로 확인하지 않았다 (CLAUDE.md 규율 ⑥)]:
  평균 응력 텐서의 접촉 유형별 분할 σ_ij = (1/V) Σ_c f_i l_j — Minh · Cheng · Thornton 2014 (Granular Matter · DOI 10.1007/s10035-013-0455-3) ·
  간극 입도 흙 DEM 의 굵은–굵은 / 굵은–가는 / 가는–가는 분할 (Shire · O'Sullivan 그룹) · 응력 감소 계수 α = (한 분율이 진 응력) ÷ (전체 응력) —
  Shire · O'Sullivan · Hanley · Fannin 2014 (J. Geotech. Geoenviron. Eng. · DOI 10.1061/(ASCE)GT.1943-5606.0001184 · Skempton–Brogan 개념).
- ⛔ **정정**: 앞서 (10-07 대화) 제안한 축 이름 *"Load-bearing fraction"* 은 문헌에 없는 **지어낸 이름**이었다 — 철회 (원장 기록 = 본 세션 `SELF-96`).
- ⚠ **요약 `(mean)` 열의 정의가 바뀌었다** (10-07 첫 판 = 단면 몫의 단순 평균 → 지금 = Σ_k F_X ÷ Σ_k F).  둘은 단면 하중이 높이에 따라 다를 때만 다르다 —
  ps45 다섯 조성 차 최대 **0.029 %p** (10:0 AM–AM 56.943 → 56.914) · real14 0.0005 %p.  단순 평균은 JSON `share_group_mean_over_cuts_pct` 에 그대로 남는다.

## 1. real14 로 확인 (`real14_validation/` · 커밋된 덤프 · 같은 hooke/hysteresis 모델의 다른 침대)

| 양 | AM–AM | AM–SE | SE–SE |
|---|---|---|---|
| 접촉 수 몫 | 0.6 % | 29.4 % | 70.0 % |
| 법선력 크기 합의 몫 (옛 5 쪽 방식) | 33.0 % | 34.6 % | 32.3 % |
| **Contribution to σ_zz — 21 단면 평균** (σ_zz 263.14 MPa · 슬라이드 값) | **74.60 %** | 21.94 % | 3.46 % |
| 연속 극한 (창 잘린 적분 · σ_zz 263.14 MPa) | 74.58 % | 21.96 % | 3.46 % |
| 가운데 단면 하중 몫 (z 15.14 µm · 263.17 MPa) | 74.0 % | 22.8 % | 3.2 % |
| 유효 단면 21 개 범위 (12.0–18.3 µm) | 71.5–77.4 % | 19.3–24.6 % | 2.9–4.4 % |

- 검사: 입자 힘 평형 (벽에서 2 r_max 밖 입자 · 힘 가중 알짜 힘) **2.3e-4** · 원자 없는 접촉 0 · 힘 = 덤프 `fx·fy·fz` (법선 + 접선).
- 다시 만들기: `python3 scripts/parse_liggghts.py <atom_2060000> <contact_2060000> <mesh_2060000.stl> -o real14_res` (덤프 = `docs/data/real14_reference_20260928/` 를 푼 것) →
  그 폴더의 input_params.json = `{"box_x": 0.05, "box_y": 0.05}` · meta = `{"type_map_resolved": "1:AM_P,2:AM_S,3:SE", "scale": 1000}` (둘 다 `echo '…' >` — 입력 sha256 다섯 = JSON 과 같음) →
  real14_res 가 있는 폴더에서 `python3 <리포>/scripts/plane_load_share.py --case real14_res --meta real14_meta.json --label real14 --out <폴더>`
  (JSON 의 results_dir · meta = 그 상대 이름 · code_sha256 = 실행한 스크립트 파일).  단면 CSV 는 10-07 첫 판과 바이트 같다.
- 관찰 (기록만): real14 덤프에 중심이 바닥 (z = 0) 아래인 입자 122 개 · 판 위 3 개 — 새어 나간 입자 (가운데 단면 값에는 무관 · 원인 미확인).
- **접선력** (`real14_validation/tangential_share.txt`): 접선 ÷ 법선 (합) = 0.25 · 0.27 · 0.26 (AM–AM · AM–SE · SE–SE) · 쿨롱 한계 (μ 0.5) 의 미끄럼 접촉 21–27 % ·
  크기 합 몫을 합력 |Fn + Ft| 로 바꿔도 차이 ≤ 0.05 %p — 단면 하중 몫은 처음부터 합력 z 성분을 쓴다.
- α · 교차 대조 = §3.

## 2. ps45 다섯 조성 (✅ 1저자 WSL 10-07 · 코드 `d581154be` · 원자료 `raw/ps45_plane_load_20261007.tgz` sha256 `71f1a2a7311d6c927b991400041a2e2350158a0b67e45f99cc5f5c8d90f48913` · 푼 것 `ps45/`)

```bash
cd ~/dem-audit && pgrep -af "run_network_194_parallel|lhs_webapp_batch" || echo "실행 중인 배치 없음"
git fetch -q origin claude/stoic-knuth-NObVQ && git checkout -q --detach FETCH_HEAD && git log --oneline -1
PY=$(ls ~/Yonghoon-DEM-DFT/venv/bin/python ~/Yonghoon-DEM-DFT/.venv/bin/python3 2>/dev/null | head -1)   # 시스템 python3 에는 numpy 가 없다 (10-07 첫 실행 실패)
$PY scripts/plane_load_share.py --selftest | tail -1
$PY scripts/plane_load_share.py --batch ~/ps45_network_20261006 --out ~/ps45_plane_load_20261007; echo "rc=$?"
tar -czf ~/ps45_plane_load_20261007.tgz -C ~ ps45_plane_load_20261007 && sha256sum ~/ps45_plane_load_20261007.tgz
```

- 입력 = 망 배치 폴더의 `work/results/<id>/` (atoms.csv · contacts.csv · mesh_info.json · input_params.json) + `work/uploads/<id>/meta.json` (type map · scale) — 읽기만 한다.
- 출력 (첫 판) = 슬라이드 (가운데 단면 몫) · 요약 · 단면별 CSV · JSON — 원본 그대로 `raw/` tgz 에 있다.
- ★ **10-07 Q1 다시 쓰기**: `ps45/plane_load_share_slide.csv` · `ps45/plane_load_summary.csv` = 이 도구의 `--rewrite` 출력 (덤프 없이 `ps45/plane_load.json` 의 단면 기록에서 —
  `ps45/plane_load.json` 은 tgz 의 것과 바이트 같다 · sha256 `0f65a06b3ab6060f19992cc8a09bbf4236e26d72cdbcc496e325b2770040707f`) · 단면 CSV 다섯 = 바이트 그대로 ·
  출처 (원 JSON · 코드 · 쓴 파일 sha256) = `ps45/plane_load_rewrite.json`.  α 는 덤프가 있어야 나오므로 아직 없다 (§4 WSL 다시 실행).
  다시 만들기: `python3 scripts/plane_load_share.py --rewrite docs/data/ps45_plane_load_20261007/ps45/plane_load.json --out <빈 폴더>` → 같은 바이트.
- ⚠ 한정: 이 프레임은 압축 뒤 이완 단계 (7:3 판 압력 165 MPa) · 단면 하중 몫은 그 프레임의 하중 경로 — 판 하중 분담 (CLAUDE.md f_AM 절) 과 같은 계열이지만 같은 정의는 아니다.
  같은 폴더 `ibb_damping_drag_20261007.txt` = 원장 `DEMP-01` 의 1저자 ibb 기록 (압축 **중** 프레임의 감쇠 저항 434.3 N = 판 목표의 57.9 % — 이 표의 이완 프레임과 다른 단계).

### 결과 (슬라이드 = 21 단면 평균 · `ps45/plane_load_share_slide.csv`)

| PC:SC | **Contribution to σ_zz** AM–AM · AM–SE · SE–SE (%) | 가운데 단면 AM–AM · AM–SE · SE–SE (%) | 크기 합 몫 (옛 5 쪽) | σ_zz (21 단면 평균 · MPa) | 가운데 하중 (MPa) | 상태 |
|---|---|---|---|---|---|---|
| 0:10 | **59.56** · 31.01 · 9.43 | 64.38 · 25.92 · 9.70 | 33.1 · 37.2 · 29.7 | 158.25 | 158.25 | CHECK (보존 1.0222) |
| 3:7 | **54.63** · 34.66 · 10.71 | 55.56 · 34.62 · 9.82 | 25.4 · 38.3 · 36.3 | 159.93 | 159.93 | OK |
| 5:5 | **52.37** · 36.22 · 11.41 | 51.48 · 35.72 · 12.80 | 21.2 · 37.9 · 40.9 | 164.44 | 164.47 | OK |
| 7:3 | **48.46** · 39.14 · 12.39 | 46.36 · 39.46 · 14.18 | 17.0 · 36.4 · 46.6 | 167.14 | 167.14 | OK |
| 10:0 | **56.91** · 32.95 · 10.13 | 51.99 · 36.73 · 11.28 | 19.8 · 30.5 · 49.6 | 175.48 | 175.49 | OK |

- 슬라이드 CSV 소수 넷 자리: 0:10 59.5622 · 31.0083 · 9.4294 / 3:7 54.6349 · 34.6600 · 10.7051 / 5:5 52.3717 · 36.2192 · 11.4092 / 7:3 48.4639 · 39.1441 · 12.3920 /
  10:0 56.9144 · 32.9541 · 10.1315 (= 요약 `(mean)` 열).
- 읽기 (모델 안 · 이완된 프레임): AM–AM 접촉 (전체 접촉의 0.14–1.6 %) 이 σ_zz 의 48–60 % (21 단면 평균 · 가운데 단면은 46–64 %) · SE–SE 9–12 % ⇒
  크기 합 기준 해석 *"SE 망이 힘 경로의 중심"* 은 하중 기준으로 틀렸다 (`SELF-95`) · 7:3 = 다섯 조성 중 AM–AM 몫 최소 · AM–SE · SE–SE 몫 최대
  (가운데 단면 · 21 단면 평균 둘 다 · 크기 합 몫의 7:3 최소와 같은 자리).  10:0 은 가운데 단면 (52.0 %) 과 21 단면 평균 (56.9 %) 차가 가장 크다.
- 입자 힘 평형 1.65–2.26e-4 (다섯 모두 통과).
- **보존 CHECK (0:10) = 침대 무게** (확인 · 10-07 단면별 CSV): 단면 하중이 높이에 따라 **직선으로** 준다 — 기울기 −0.029 ~ −0.034 MPa/µm · 직선에서의 잔차 최대 0.009–0.023 % ·
  기울기 ÷ (g × 1e-6) = 유효 침대 밀도 2.9–3.4 g/cm³ (축척 덱: 길이 × 1000 · 응력 ÷ 1000 → 무게 ÷ 응력이 실제의 10⁶ 배 · 110 µm 침대에서 ≈ 2 %).
  교차 대조: 7:3 압밀 로그의 이 프레임 판 압력 165.30 MPa (`docs/data/ps73_compaction_curve_20261006/curve/pressure.csv` step 3,220,000) ↔ 가장 위 단면 (102 µm) 165.59 MPa.
  ⇒ 몫 값은 무관 (21 단면 평균은 무게 기울기만큼 하중 가중) · 검사를 "무게 직선을 뺀 잔차" 로 바꿀지 = ⬜ 1저자 (이 README 첫 판의 Q2 — §3 α 와 다른 질문).

## 3. α — 상별 응력 감소 계수 꼴 (1저자 10-07 Q2)

| 항목 | 내용 |
|---|---|
| 정의 | α_X = ⟨σ_zz⟩_X ÷ ⟨σ_zz⟩_all · ⟨·⟩ = 부피 가중 평균 Σ V_p σ_zz,p ÷ Σ V_p · 입자 = 중심이 단면 창 [2 r_max, 판 − 2 r_max] 안 · X = AM_P · AM_S · SE · AM (= AM_P ∪ AM_S) |
| 입자 응력 | Love–Weber σ_p = (1/V_p) Σ_c (x_c − x_p) ⊗ f_c — 봉인 `scripts/dem_analysis_core.py` `calc_love_weber_stress` (return_arrays) 의 입자 텐서 그대로 (읽기 전용 · 입력 = 봉인 `scripts/analyze_contacts.py` 로더) |
| 닫힘 | Σ_X (V_X/V_all) α_X = 1 (정의상 정확 · 어기면 FAILED) |
| 보조 | α_p = 평균 응력 p = tr σ / 3 의 같은 비 |
| 없는 상 | null (CSV 빈칸 · 0 아님) — 상이 침대에 없거나 창 안에 중심이 없을 때 · ⟨σ_zz⟩_all = 0 이면 UNDEFINED |
| 슬라이드 | stress_reduction_slide.csv (Origin 머리 세 줄: PC:SC · α AM_P · α AM_S · α SE · α AM · 단위 - · 주석 = *α = ⟨σ_zz⟩_phase / ⟨σ_zz⟩_all (부피 가중 · Love–Weber 입자 응력 · 단면 창 안 입자) — α < 1 = 평균보다 덜 눌림*) |
| 그림 힌트 | **α = 1 에 점선** (평균선) — 위 = 평균보다 더 눌림 · 아래 = 덜 눌림 |
| 한정어 (필수) | **모델 내부 비교 — 입자 응력 기준틀 미인증 (Codex 10-05 Q5)** |
| ps45 값 | ✅ 아래 *ps45 다섯 조성* (1저자 WSL 10-07 밤 · 코드 `afda0d7ab` · `ps45_v2/`) |

### real14 (`real14_validation/stress_reduction_slide.csv` · 같은 JSON 의 `alpha`)

| | AM_P | AM_S | SE | AM | 전체 |
|---|---|---|---|---|---|
| **α (σ_zz)** | **1.536** | **0.642** | **0.201** | 1.265 | (1) |
| α_p (평균 응력) | 1.440 | 0.784 | 0.273 | 1.241 | (1) |
| ⟨σ_zz⟩ (압축 · MPa) | 532.0 | 222.2 | 69.5 | 438.1 | 346.3 |
| 창 안 입자 수 | 8 | 94 | 6,578 | 102 | 6,680 |
| 창 안 고체 부피 몫 | 0.523 | 0.228 | 0.249 | 0.751 | 1 |

- 닫힘 Σ (V_X/V_all) α_X = 1 (1 − 1e-16) · Love–Weber 검사 (봉인 함수) = 힘 분해 1.4e-6 · 접촉점 ÷ 반경 1.00014 · 전체 virial ↔ c_strs 5.0e-5 (전역 부호 · 척도 검사 — 상 배분의 증명 아님).
- ⚠ real14 의 창은 **6.28 µm** (12.0–18.3 µm) 로 AM_P 지름 12 µm 보다 얇다 → AM_P 값은 창 안 **8 개**가 정한다 (표본 작음 · 같은 침대의 다른 높이에서는 다를 수 있다).

### ps45 다섯 조성 (`ps45_v2/stress_reduction_slide.csv` · 같은 JSON 의 `alpha` · ✅ 1저자 WSL 10-07 밤 · §4)

| PC:SC | α PC (AM_P) | α SC (AM_S) | α SE | α AM | α_p SE (평균 응력) | 창 (µm) | 창 안 입자 PC · SC · SE |
|---|---|---|---|---|---|---|---|
| 0:10 | — | 1.291 | **0.448** | 1.291 | 0.516 | 4.0–113.2 | — · 4 331 · 146 309 |
| 3:7 | 1.329 | 1.245 | **0.486** | 1.270 | 0.568 | 9.0–105.4 | 104 · 2 735 · 131 664 |
| 5:5 | 1.403 | 1.132 | **0.484** | 1.270 | 0.574 | 9.0–103.4 | 175 · 1 917 · 131 060 |
| 7:3 | 1.336 | 1.086 | **0.505** | 1.261 | 0.591 | 9.0–102.1 | 239 · 1 162 · 131 308 |
| 10:0 | 1.316 | — | **0.384** | 1.316 | 0.472 | 9.0–103.6 | 350 · — · 130 989 |

- 닫힘 Σ (V_X/V_all) α_X = 1 (다섯 모두 1.000000000) · Love–Weber 검사 상태 OK (봉인 함수 · 전역 부호 · 척도 검사).
- ⟨σ_zz⟩ 는 입자 **안** 평균 (부피 가중 · 고체만) — 단면 하중 (판 압력) ÷ 창 안 고체 부피 몫과 같은 수준 (예 7:3 고체 평균 195.6 MPa ↔ 21 단면 평균 167.1 MPa).

**상별 수직 하중 몫 = 창 안 고체 부피 몫 × α** (합 100 % · 1저자 10-07 *"직관적"* 질문에 낸 꼴):

| PC:SC | 고체 부피 몫 AM / SE (%) | 수직 하중 몫 AM / SE (%) | 그중 PC · SC (%) | 그림 1 σ_zz 기여 AM–AM · AM–SE · SE–SE (%) | (AM 몫 − AM–AM) ÷ AM–SE |
|---|---|---|---|---|---|
| 0:10 | 65.5 / 34.5 | **84.5 / 15.5** | — · 84.5 | 59.6 · 31.0 · 9.4 | 0.81 |
| 3:7 | 65.6 / 34.4 | **83.3 / 16.7** | 26.3 · 57.0 | 54.6 · 34.7 · 10.7 | 0.83 |
| 5:5 | 65.6 / 34.4 | **83.4 / 16.6** | 46.9 · 36.4 | 52.4 · 36.2 · 11.4 | 0.86 |
| 7:3 | 65.4 / 34.6 | **82.5 / 17.5** | 61.3 · 21.3 | 48.5 · 39.1 · 12.4 | 0.87 |
| 10:0 | 66.1 / 33.9 | **87.0 / 13.0** | 87.0 · — | 56.9 · 33.0 · 10.1 | 0.91 |

- 읽기: **SE 는 창 안 고체 부피의 34 % 인데 수직 하중은 13.0–17.5 % 만 진다** (모델 안).  α_SE = 두 몫의 비 (예 7:3 17.5 ÷ 34.6 = 0.505).
  AM 의 α 가 1.26–1.32 로 평평한 것은 AM 이 부피의 65 % 라 닫힘 때문에 1/0.655 = 1.53 을 넘을 수 없어서다 — 조성에 따른 변화는 SE 쪽에서 본다.
- 산술 대조 (관찰 · 관문 아님): 마지막 열 = AM–SE 접촉 기여 가운데 AM 입자 몫으로 간 비 = **0.81 (SC 만) … 0.91 (PC 만)** ≈ r_AM ÷ (r_AM + r_SE) = 2.0/2.5 = 0.80 · 4.5/5.0 = 0.90
  (덱 `dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts` r_AM_P 4.5 · r_AM_S 2.0 · r_SE 0.5 µm) — Love–Weber 는 접촉 쌍극 l ⊗ f 를 가지 (중심 → 접촉점) 길이대로 두 입자에 나눈다 ⇒
  그림 1 (접촉 종류별) 과 이 표 (상별) 는 같은 σ_zz 의 두 분해다 (섞인 침대 0.83–0.87 = 두 크기의 혼합).
  ⚠ 이 상별 몫은 FAM 의 f_AM 두 규약 ((a) AM–AM 만 · (b) stress/atom 50/50 — CLAUDE.md f_AM 절 · FAM 등록 §12-2) 과 **다른 세 번째 꼴** (가지 길이 배분) 이다 — FAM 등록 값으로 쓰지 않는다 (기록만).
- 한정어 (필수): **모델 내부 비교 — 입자 응력 기준틀 미인증 (Codex 10-05 Q5)**.

### 교차 대조 — LW 창 합 ↔ 21 단면 평균 (보고 · 관문 아님)

| 항 (real14 · MPa) | LW 창 합 −Σ_창 V σ_zz ÷ (A·H) | 창 잘린 적분 (= 21 단면 평균의 연속 극한) | 접촉 수 |
|---|---|---|---|
| 창 안 두 입자 접촉 | 42.86 | 42.86 (같다) | 18,509 |
| 한 입자만 창 안 (가장자리) | **262.02** (그 입자 → 접촉점 가지 전체) | **209.49** (중심 사이 가지가 창과 겹친 길이) | 6,691 |
| 두 입자 모두 창 밖 · 창 전체를 걸침 | 0 | **10.80** | 2 |
| 합 | **304.88** | 263.15 (21 단면 평균 263.14 · 비 0.9999986) | |

- **LW 창 합 ÷ 21 단면 평균 = 1.1586** — 원인 = 창이 얇다 (6.28 µm < AM_P 지름 12 µm): 창 안 AM_P 의 가지 (최대 6 µm) 가 창 밖으로 나가 가장자리 항 +52.5 MPa ·
  창을 통째로 걸친 접촉 2 개 −10.8 MPa.  항등식 잔차 1.9e-16 · 2.2e-16 (분해가 봉인 텐서 합 · 단면 적분을 정확히 다시 만든다).
- 벽 접촉 (접촉 덤프에 없음) 은 무관: 창 안 입자 중 벽에 닿는 것 **0** (창 = 벽에서 2 r_max 밖이라 구조상 0).
- ps45 는 창이 93 µm (판 111 µm · r_max 4.5 µm) 라 가장자리 몫이 작다 — 비 ≈ 1 일 것 (추정 · §4 실행 뒤 확인).
  ✅ **확인 (10-07 밤)**: LW 창 합 ÷ 21 단면 평균 = 1.0037 · 0.9969 · 1.0056 · 1.0006 · 1.0150 (0:10 · 3:7 · 5:5 · 7:3 · 10:0) — 가장자리 LW ↔ 적분 3.63 ↔ 3.04 … 10.73 ↔ 8.10 MPa · 창 전체 걸침 0 (`wsl_rerun_v2_20261007.txt`).

## 4. WSL 다시 실행 (새 코드 · α 포함 — 1저자)

✅ **실행 10-07 밤 (1저자 WSL · 코드 `afda0d7ab` · selftest 54/54)** — rc 2 = 기대대로 (0:10 보존 CHECK 1.0222 = 침대 무게 · 첫 판과 같다) · 다섯 α 상태 OK · 닫힘 1 ·
슬라이드 = 커밋본과 같은 바이트 · 단면 CSV 같은 바이트 · 요약 CSV = α 칸만 채워짐 · 묶음 `raw/ps45_plane_load_20261007_v2.tgz` (sha256 `97f97cdb9b209555e3478ec3d1f094a45b67e4f54b6562a3fbd85993abeabec8` · 9 파일) → `ps45_v2/` · 화면 `wsl_rerun_v2_20261007.txt`.

```bash
cd ~/dem-audit && pgrep -af "run_network_194_parallel|lhs_webapp_batch" || echo "실행 중인 배치 없음"
git fetch -q origin claude/stoic-knuth-NObVQ && git checkout -q --detach FETCH_HEAD && git log --oneline -1
PY=$(ls ~/Yonghoon-DEM-DFT/venv/bin/python ~/Yonghoon-DEM-DFT/.venv/bin/python3 2>/dev/null | head -1)   # 시스템 python3 에는 numpy 가 없다
$PY -c "import numpy, pandas, networkx; print('의존 OK')"     # α 는 봉인 dem_analysis_core (networkx) 를 부른다
$PY scripts/plane_load_share.py --selftest | tail -1           # plane_load_share selftest 54/54
$PY scripts/plane_load_share.py --batch ~/ps45_network_20261006 --out ~/ps45_plane_load_20261007_v2; echo "rc=$?"
diff ~/ps45_plane_load_20261007_v2/plane_load_share_slide.csv docs/data/ps45_plane_load_20261007/ps45/plane_load_share_slide.csv && echo "슬라이드 = 커밋본 (같은 바이트)"
tar -czf ~/ps45_plane_load_20261007_v2.tgz -C ~ ps45_plane_load_20261007_v2 && sha256sum ~/ps45_plane_load_20261007_v2.tgz
```

- 새 폴더 (`_v2`) 로 낸다 — 첫 판 (`~/ps45_plane_load_20261007`) 은 그대로 둔다.  첫 판과 같은 덤프면 단면 값이 같으므로 슬라이드는 커밋본과 **같은 바이트**여야 한다 (위 diff).
- 기대 (추정 · 확인 전): rc = 2 가 정상 (0:10 보존 CHECK = 침대 무게 · 첫 판과 같다 — 종료 코드는 단면 하중 상태만 따르고 α 는 안 본다) ·
  화면의 α 줄 다섯 = 상태 OK · 닫힘 1 · LW ÷ 21 단면 ≈ 1.  α 상태가 NOT_COMPUTED (contacts.csv 접촉점 열 · networkx 없음) 면 그 사유를 그대로 보낸다.
- 올릴 것 = 위 tgz (+ sha256).  케이스당 수십 초 (봉인 로더 = 파이썬 dict · 160 k 원자 · 56 만 접촉 — 추정).
- **ps73 B 가지 (`docs/data/ps73_damping_branch_20261007/README.md` §6 3)) 명령은 그대로 돈다** — `--case` 한 케이스 경로 · 출력 폴더마다 슬라이드 (21 단면 평균) ·
  stress_reduction_slide.csv · 요약 α 열이 더 생긴다 · 멈춘 step (보존 CHECK 예상) 도 값은 낸다 · 종료 코드 규칙 같음.
