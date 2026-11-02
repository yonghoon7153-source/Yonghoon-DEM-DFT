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
| 3 µm | 4,475,002 · 300.6 | contact 4,480,000 (멈춘 뒤 5 ms) | 294.6 | ⬜ 계산 (조각 대기) |
| 2 µm | 3,915,002 · 300.2 | contact 3,920,000 (멈춘 뒤 5 ms) | 284.9 | NCM 중앙값 340.0 · SE 126.1 MPa (벽 제외) · P_ref 275.1 (판 직후 279–290 흔들림 안) |
| 1 µm | 2,685,002 · 300.6 | 압축 체크포인트 2,600,000 에서 run 0 (시간 진행 없음 · 접촉 힘만 다시 계산 · hit) | 285.3 | ⬜ 원 `atom_2600000` stress/atom 과 대조 뒤 · 1 µm 는 멈춘 뒤 5 ms 에 136.6 MPa (contact 2,690,000) — 300 근처 contact 덤프 없음 |

- 덱 = contact 덤프는 이완 (PHASE 4) 부터만 · 압축 중 atom 덤프 (50,000 간격) 의 stress/atom = 접촉 힘 반반 나눔 (LHS-29) → NCM ↔ SE 비교에 안 쓴다.
- 1 µm 압력 급락 (300.6 → 136.6 MPa · 5 ms) 원인 = **추정** (압축 감쇠 viscous 0.5 = 입자마다 같은 γ · KG50-04) — 확인 전.
