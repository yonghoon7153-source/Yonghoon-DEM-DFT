# LHS 130 구조 디스크립터 — 재수확 (2026-09-24)

`docs/data/lhs_descriptors_20260919/` 를 **대체**한다.  옛 판은 분모 바닥이 벽보다 10 µm 아래였고 (`LHS-10`) 97 건이 원자 덤프보다
이른 메시의 플래튼을 썼다 (`LHS-11`) — porosity 가 15.8–48.6 %p (중앙 36.3) 부풀어 있었고 φ_SE 는 이 판의 0.50–0.82 배였다.

## 출처

- 코드 `4ee1038c3` (판단 J14 — 바닥은 덱 `zplane` 으로 확인 · 벽 밖 부피는 거부 대신 기록) 을 WSL `~/dem-web` 에서 돌렸다
  (인터프리터 `~/Yonghoon-DEM-DFT/venv`).
- `scripts/lhs_harvest_batch.py --verify-sha` → 성공 **130/130** · 메시 `exact` 130 · 봉인 sha (atom · contact · deck) 130 대조.
- 덱 바닥: 130/130 이 `wall/gran … primitive … zplane 0.0` 하나 — 벽 재질은 bimodal 100 건 type 3 · mono 30 건 type 2 (**둘 다 SE**).
- 교차검사 `scripts/lhs_phi_crosscheck.py` → `docs/data/lhs_descriptors_20260924/_phi_crosscheck.tsv`:
  SAME **130** · 최대 잔차 5.6e-14 %p · 바닥 틈 0 · 플래튼 − 고체 윗면 −1.21 … −0.27 µm (중앙 −0.52).
  남은 1 행은 코호트의 `perc` 행 (케이스가 아니다).

## 규약

- (가) 주 값 = 웹앱 ε_sphere — ΣV / (L_x·L_y·plate_z), 벽 z = 0.  `porosity_sphere_pct_RECORD_ONLY` · `phi_se` · `phi_am`.
  porosity 는 인계표에서 **기록 전용** (판단 J1).
- (나) = `wall_record.pushback` — 벽 밖 부피를 벽 안으로 되돌려 두께에 더한 값 (H′ = plate_z + V_out / (L_x·L_y)).
- 벽 기록 = `wall_record.floor` · `wall_record.plate` — 벽 밖 부피 · 닿은 입자 수 · 중심이 벽 밖인 입자 수 (상별) · 통째로 벽 밖인 수 ·
  가장 깊은 입자.  덱 확인 = `deck_floor`.

## 벽 기록 요약 (130 건)

| 양 | 중앙 | p90 | 최대 |
|---|---|---|---|
| 바닥 밖 부피 / ΣV (%) | 0.595 | 1.43 | 4.39 |
| 플래튼 밖 부피 / ΣV (%) | 0.081 | 0.163 | 0.214 |
| (나) − (가) porosity (%p) | 0.61 | 1.06 | 2.53 |
| (나) 두께 증가 (µm) | 0.23 | 0.41 | 1.07 |

- 설계군별 (나) − (가) 중앙: bimodal 0.60 · mono_AM_S 0.48 · **mono_AM_P 1.20** (최대 2.53).
- 가장 깊은 입자의 상: AM_P 66 · AM_S 33 · AM (mono) 29 · SE 2.
- 중심이 바닥 아래인 입자가 있는 케이스 **42** (AM_S 618 개 · SE 62 · AM 2) · 통째로 바닥 아래 15 케이스 (최대 21 개, 대부분 SE) ·
  통째로 플래튼 위 3 케이스 (SE — 009 · 120 · 129).
- 가장 깊은 입자의 겹침/반지름이 **정확히 1.98** 인 케이스 9 (r = 1 µm 7 · r = 0.5 µm 2) — 원인 미상 (`LHS-13`).

## 주의

- ⚠ ε_sphere 가 **음수**인 케이스: (가) 18 (−2.43 … −0.09 %) · (나) 16 — 입자끼리 겹침 과다다 (`LHS-15`, 판단 J6 취급 결정 대기).
- ⚠ LHS 덱의 바닥 벽 재질은 SE 다 — 생산 덱 (`docs/data/phase_a_6mah/in.real_4.liggghts`) 은 type 1 (AM_P).  AM 이 무른 바닥에
  깊게 박히는 까닭이고, 생산 코퍼스와 비교할 때 계통 차이가 된다 (`LHS-14`).
- 인계표는 이 판으로 재생성한다 — Codex 리뷰 (판단 J15) 뒤.  **배포 보류.**
