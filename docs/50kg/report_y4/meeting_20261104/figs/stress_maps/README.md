# 응력 지도 (Love–Weber von Mises · 웹앱 질감 · 판·바닥 접촉 입자 뺌) — 11-03

만든 도구 = `docs/50kg/report_y4/meeting_20261104/tools/stress_prerelax/` (16쪽 값과 같은 함수 · 웹앱 3D 뷰어와 같은 렌더러 · 색 = jet · NCM 0–600 MPa · SE 0–300 MPa 선형 고정).  PNG = 투명 배경 · 알파 범위로 자름.  `summary_*.json` = 그 프레임의 중앙값 · p10 · p90 · 판 압력 · P_ref · 입력 덤프 sha256.

## A. 영률 장 (덱에 넣는 것 · 1저자 11-03 *"응력 부분은 영률 이 부분에서만"*) — 2 µm · 이완 끝

| E_SE (덱 표기) | 프레임 | 판 압력 | NCM 중앙값 | SE 중앙값 | 그림 |
|---|---|---|---|---|---|
| 11 GPa (E × 0.5) | atom · contact 4,485,002 (같은 step · virial 검사 checked) | 278.5 MPa | 352.75 MPa | 84.73 MPa | `modulus_11GPa_{NCM,SE}.png` |
| 22 GPa (기본) | atom · contact 4,015,002 (같은 step · checked) | 279.79 MPa | 334.85 MPa (16쪽 기록과 끝자리까지 같음) | 125.96 MPa | `modulus_22GPa_{NCM,SE}.png` |
| 33 GPa (E × 1.5) | 3,665,002 (같은 step · checked) | 280.1 MPa | 325.98 MPa | 151.51 MPa | `modulus_33GPa_{NCM,SE}.png` |

## B. 입도 장 (지금 덱에서 뺌 — 나중에 넣을 때를 위한 기록 · 1저자 11-03 *"나중에 혹시 넣어야될 때를 대비해서 기록해둬"*) — 가압판 300 MPa 직전

| D_SE | 프레임 | 판 압력 | P_ref (접촉망 상자 평균 σzz) | NCM 중앙값 | SE 중앙값 | 그림 |
|---|---|---|---|---|---|---|
| 3 µm | contact 4,480,000 (판 멈춘 뒤 5 ms) | 294.6 MPa | 285.2 MPa | 358.8 MPa | 149.5 MPa | `prerelax_3um_{NCM,SE}.png` |
| 2 µm | contact 3,920,000 (판 멈춘 뒤 5 ms) | 284.9 MPa | 275.1 MPa | 340.0 MPa | 126.1 MPa | `prerelax_2um_{NCM,SE}.png` |
| 1 µm | 압축 체크포인트 2,600,000 run 0 (판 이동 중 · 원 atom 덤프와 위치 · 속도 비트 같음) | 285.3 MPa | **158.0 MPa** | 172.2 MPa | 72.4 MPa | `prerelax_1um_{NCM,SE}.png` |

⚠ **넣을 때 반드시 붙일 한정** — 1 µm 는 압축 중 판 압력의 65 % (R_drag_signed 0.647) 가 감쇠 항력 상당이고 접촉망이 실은 평균 응력은 158 MPa 다 (2 µm 0.074 · 3 µm 0.026) · 원인 확정 아님 (원장 `KG50-20` 11-03 메모) → 1 µm 의 낮은 응력은 SE 입도 효과로 읽지 않는다 · 1 µm NCM 지도의 위 → 아래 응력 감소 = 그 흔적.  같은 이유로 1 µm 의 기공 · tortuosity 도 2 · 3 µm 와 같은 접촉망 응력에서 굳은 값이 아니다.
