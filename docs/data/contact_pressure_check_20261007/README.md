# 웹앱 3D 'Stress Concentration' 의 양 점검 — 하중을 따라가나 (10-07)

- **계기**: 1저자 10-07 — ps45 7:3 (`260925_000559_082983` · 6 mAh · P:S 7:3 r4.5) 의 Stress Concentration 보기에서 *"z별로 좀더 차이가 나게 범례값을 좀 조절 가능한가?"*
  (화면: 범례 415 · 중앙값 453 · 622 MPa · AM 거의 전부 빨강) + 웹앱 Z-profile CSV (`stress_z_260925_000559_082983.csv` · 1저자가 내려받은 것 · 줄끝만 LF 로 · sha256 아래).
- **양**: 입자별 최대 접촉 압력 p = |Fn| / 덤프 접촉 면적 × scale / 1e6 (MPa) — `scripts/viewer3d_data.py` `stress_max` · 색 = log 축 · 전체 입자 p5–p95
  (`webapp/static/js/viewer3d.js` `mode === 'stress'`) · z 그림 · CSV = `scripts/plot_stress_z_distribution.py` · full_metrics `contact_pressure_mean` · `_max` 도 같은 양 (`dem_analysis_core.calc_contact_pressure`).
- **확인 방법**: real14 커밋 원자료 (`docs/data/real14_reference_20260928/` · ps45 와 같은 hooke/hysteresis 덱 계열 · scale 1000) 로 `contact_pressure_check.py` → `real14_contact_pressure.txt`.
  ps45 의 접촉 덤프는 리포에 없다 (1저자 WSL) — ps45 에 대한 문장은 **추정**이다.

## 결과

| 발견 | 숫자 (real14) |
|---|---|
| ① 압축 접촉의 p 는 쌍 유형마다 거의 일정한 **천장** — 하중을 따라가지 않는다 | PC–PC: 힘은 12.9 배 다른데 p = 4,151–4,294 MPa (p5–p95 폭 1.03 배 · 기울기 d log p / d log \|Fn\| = +0.005) · SC–SC 4,213 (중앙) · SE–SE 중앙 422 · p95 474 |
| ② 그래서 AM 은 거의 다 색 범위 위 (빨강) — 하중이 커서가 아니라 AM–AM 접촉의 천장 (≈ 4,200 MPa) 이 SE–SE (≈ 470) 의 약 9 배라서 | 입자별 최대가 p95 위: AM_P 100 % · AM_S 93.6 % · SE 3.8 % |
| ③ 가장 큰 값 (10⁴–10⁶ MPa) 은 전부 **당김 (접착) 접촉** — 겹침 δ / (r1 + r2) ≈ 1e-6–1e-5 라 면적이 거의 0 | 상위 8 개 전부 당김 · 입자별 최대 ≥ 1e4 MPa 104 개 = 압축 접촉만 세면 0 개 |
| ④ ps45 7:3 z 분포 (1저자 CSV): 칸 중앙값 446.3–456.8 MPa (±1.2 %) · p95 490–520 · 평균 · 최대의 튀는 칸 (z ≈ 25–34 · 92 µm · 최대 1.18e6 MPa) | ③ 과 같은 크기 — 튀는 칸 = 당김 접촉일 것 (**추정** · ps45 덤프로 미확인) |

- **해석 (추정)**: hooke/hysteresis 의 하중 단계는 F = k δ 이고 덤프 접촉 면적 (렌즈 원) ≈ 2πR\*δ 라 p ≈ k / (2πR\*) 에서 δ 가 약분된다 → p 는 그 접촉 유형 (k · R\*) 의 표지에 가깝다.
  천장 아래의 값 = 하중을 덜어 낸 (unloading) 접촉 · 당김 접촉.
- ⇒ **범례 (색 범위) 를 좁혀도 z 방향 하중 차이가 아니라 접촉 유형 · 하중 이력의 잡음이 보인다.**  z 차이를 보려면 하중을 따라가는 양 — 입자 응력 (Love–Weber · 대기 중인 ① 3D 보기) 이나
  접촉 힘 — 으로 칠해야 한다.  원장 `WEB-06`.
- **한계**: real14 한 침대 · 부호는 주기 경계 너머 접촉 (거리 > 1.5 (r1 + r2)) 4,529 개를 빼고 셌다 · 해석의 k · 면적 식은 LIGGGHTS 소스 대조 전 (덤프 값이 그 식과 맞는다는 관찰뿐).

## 파일

`contact_pressure_check.py` (다시 만들기: `python3 docs/data/contact_pressure_check_20261007/contact_pressure_check.py > real14_contact_pressure.txt` · 결정적) ·
`real14_contact_pressure.txt` · `stress_z_260925_000559_082983.csv` (받은 파일 = CRLF · sha256 `46801f08183e1ed837a1272c2ed951b3b32c73e6e1d741616c5ec9b9023a36c0` → 리포 = 줄끝 LF 로 정규화 (`.gitattributes` CSV eol=lf · 내용 같음) · sha256 `20ea30b9711c7e0f9df10e37e4cd383bbe672fbb7c270d7555561b6b081c13c0`).
