# LHS 보충 20 + 후막 8 — ibb DEM 런 기록 (등록 `docs/reviews/lhs_supp_thick_registration_20261006.md`)

- `ibb_status_20261011.txt` = 1저자 ibb 상태표 그대로 (10-11) — **28 / 28 COMPLETED · Finished** · 마지막 체크포인트 이름 = `restart_compress_*` · 실행 중 0 · 대기 0 · 코어 0 / 60.
  (elapsed · np 칸은 그 표에서 비어 있다 — 실제 코어 수 · 경과는 sacct · 로그로 따로 적는다.)
- 끝 step (관찰): 보충 2,115,002 – 4,475,000 (설계 어림 `steps_est` 2.76 M) · 후막 4,480,000 – 10,335,000 (예: `lhst_036_6m` 어림 7.61 M → 8,240,000).
- ⬜ 등록 §4 의 성공 판정 = `scripts/lhs_ext_submit_gate.py` (28 ID 전부 `COMPLETED` + 덱 · 러너 sha256 = `deck_manifest.json`) — 아직 안 돌림.
  sacct 창에는 같은 기간의 다른 ibb 잡 (믹서 등) 이 섞여 게이트가 "매니페스트에 없는 잡" 으로 HOLD 를 낸다 → **이름 앞머리 `lhss_` · `lhst_` 로 좁혀** 넘긴다 (상태로 고르지 않는다).
- LHS 인계 범위 (1저자 10-11): **보충 20 만 v1.3 에** · 후막 8 은 LHS 밖 (등록 §5 ④ 짝 비교 = 별도 기술 보고).
