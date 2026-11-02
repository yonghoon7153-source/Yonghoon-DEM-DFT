# 응력 지도 — 가압 300 MPa 근처 프레임 (11-03 · 1저자 *"300MPa 되기 직전의 MPa로"* · *"webapp 질감으로"* · *"회색 빼고"*)

| 파일 | 하는 일 |
|---|---|
| `lw_frame.py` | contact 덤프 한 step → Love–Weber 입자 von Mises (`scripts/dem_analysis_core.calc_love_weber_stress` · 16쪽 값과 같은 함수 · SIM_PA_TO_MPA 1e-3) · 위치 = contact 덤프의 두 입자 위치 (그 step) · 벽 표지 z − r < 0 · z + r > 판 · P_ref (상자 평균 σzz · 웹앱 정의) |
| `make_bins.py` | 입자 CSV → 상별 float32 (x y z r 값 벽) · 판·바닥 접촉 입자 뺌 (1저자 11-03 *"회색 빼고"*) |
| `render.html` · `webtex_render.js` | 웹앱 3D 뷰어와 같은 렌더 (three.js 0.160.0 · MeshPhong · Ambient 0.4 + Directional 0.8 (1, 1.5, 1) · 원근 FOV 50 · 웹앱 기본 시점 방향 (1.2, 0.8, 1.2) · `jetColor` · 선형 `lwLinT`) — Playwright Chromium (SwiftShader) · three.js 는 리포에 없다 (`npm pack three@0.160.0` 를 풀어 render.html 옆 vendor 폴더에 둔다 · importmap 경로 그대로) |

확인 (11-03): 1 µm 이완 끝 (2,785,002) 을 이 도구로 다시 계산 = 16쪽 기록과 같은 값 (NCM 중앙값 172.13159380116218 · SE 76.0472465846845 · p10 · p90 같음 · virial 검사 checked).

## 프레임 (판 압력 = 로그 thermo)

| 침대 | 판 정지 (step · MPa) | 쓰는 프레임 | 판 압력 | 비고 |
|---|---|---|---|---|
| 3 µm | 4,475,002 · 300.6 | contact 4,480,000 (멈춘 뒤 5 ms) | 294.6 | NCM 중앙값 358.8 · SE 149.5 MPa (벽 제외) · P_ref 285.2 |
| 2 µm | 3,915,002 · 300.2 | contact 3,920,000 (멈춘 뒤 5 ms) | 284.9 | NCM 중앙값 340.0 · SE 126.1 MPa (벽 제외) · P_ref 275.1 (판 직후 279–290 흔들림 안) |
| 1 µm | 2,685,002 · 300.6 | 압축 체크포인트 2,600,000 에서 run 0 (시간 진행 없음 · 접촉 힘만 다시 계산 · hit · NP 4) | 285.3 | NCM 중앙값 172.2 · SE 72.4 MPa (벽 제외) · **P_ref 158.0** · 대조 = 원 `atom_2600000` 과 위치 · 속도 · 운동에너지 비트 같음 · stress/atom 전체 합 차 5e-5 · 입자별 중앙 2.5e-4 (setup 한 번 더 계산한 접선 이력 증분 · 추정) |

- 덱 = contact 덤프는 이완 (PHASE 4) 부터만 · 압축 중 atom 덤프 (50,000 간격) 의 stress/atom = 접촉 힘 반반 나눔 (LHS-29) → NCM ↔ SE 비교에 안 쓴다.
- ★ **압축 중 판 압력의 감쇠 항력 몫 (11-03 실측)** = γ · Σ(−v_z) ÷ 0.0025 m² (덱 `fix damp all viscous 0.5` · 판 압력과 같은 환산) — 1 µm (2,600,000 · N 168,457) **184.6 / 285.3 MPa = 65 %** · 2 µm (3,900,000 · N 22,353) 22.0 / 297.8 = 7 % · 3 µm (4,450,000 · N 7,666) 7.6 / 296.8 = 3 % (평균 v_z ≈ 판 속도 반 · 항력 ∝ 입자 수).  ⇒ 1 µm 의 "300 MPa" 는 대부분 감쇠 저항이고 입자망이 실은 평균 응력 (P_ref) 은 158 MPa — 판 정지 뒤 136.6 → 156.2 MPa 로 떨어지는 것과 같은 이유 · 1 µm NCM 지도의 위 → 아래 응력 감소가 그 흔적.  KG50-04 (같은 γ 감쇠 · γ/m 이 SE 크기에 따라 다름) 의 크기를 잰 것 — **1 µm 의 압밀 결과 (기공 · tortuosity · 응력) 는 2 · 3 µm 와 같은 입자 응력에서 압밀된 것이 아니다** (원장 반영 ⬜ 1저자).
