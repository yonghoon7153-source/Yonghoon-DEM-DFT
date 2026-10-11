# LHS 보충 20 + 후막 8 — ibb DEM 런 기록 (등록 `docs/reviews/lhs_supp_thick_registration_20261006.md`)

- `ibb_status_20261011.txt` = 1저자 ibb 상태표 그대로 (10-11) — **28 / 28 COMPLETED · Finished** · 마지막 체크포인트 이름 = `restart_compress_*` · 실행 중 0 · 대기 0 · 코어 0 / 60.
  (elapsed · np 칸은 그 표에서 비어 있다 — 실제 코어 수 · 경과는 sacct · 로그로 따로 적는다.)
- 끝 step (관찰): 보충 2,115,002 – 4,475,000 (설계 어림 `steps_est` 2.76 M) · 후막 4,480,000 – 10,335,000 (예: `lhst_036_6m` 어림 7.61 M → 8,240,000).
- ⬜ 등록 §4 의 성공 판정 = `scripts/lhs_ext_submit_gate.py` (28 ID 전부 `COMPLETED` + 덱 · 러너 sha256 = `deck_manifest.json`) — 아직 안 돌림.
  sacct 창에는 같은 기간의 다른 ibb 잡 (믹서 등) 이 섞여 게이트가 "매니페스트에 없는 잡" 으로 HOLD 를 낸다 → **이름 앞머리 `lhss_` · `lhst_` 로 좁혀** 넘긴다 (상태로 고르지 않는다).
- LHS 인계 범위 (1저자 10-11): **보충 20 만 v1.3 에** · 후막 8 은 LHS 밖 (등록 §5 ④ 짝 비교 = 별도 기술 보고).
- ✅ **10-11 등록 §4 성공 게이트 = GO** (sacct 이름 좁힘 42 줄 · `등록 ID 28개 · COMPLETED 28개` · 봉인 입력 불변 · 끝줄 "64/64" = 도구 고정 문구) — 화면 `ibb_wsl_pack_harvest_20261011.txt`.
- 계보 (같은 파일): 로그 둘 이상 = `lhss_002 · 004 · 008 · 010 · 020` (2) · `014` (3) — 여섯 다 **체크포인트 재개** (`Reading restart file` · 재개 덱 `_r1` · `_r2` 는 등록 manifest 밖 · 재개 시험 G1–G3 기록 미확인) · 처음부터 다시 돈 런 없음.
- 보충 20 최종 프레임 묶음 (ibb): 공통 step = 끝 step 이하 가장 큰 10,000 배수 20/20 · mesh 20/20 · 목록 107 (= 80 + 로그 27) · tgz 422 MB sha256 `16398b65…572d` → WSL (DESKTOP-IK8J81H · `~/lhss_local`) 전송 sha256 같음 · `-c` OK 아닌 줄 0.
- ⚠ WSL 수확 첫 시도 0/20 (BAD_NTYPES — 내 명령: 봉인기는 설계 CSV `case_id` · `block` 을 읽는데 보충 CSV 는 `id` · `block = supp` · 설계족은 `kind`) → `--refill-family` (case_id = id · block = kind · kind ↔ ntype 대조) 로 다시 = 1저자 실행 대기 · 도구 대조 lhsx_001 `mc_void_pct 7.1576249999999995` = 09-27 값과 같음.
- ✅ **10-11 WSL 수확 r2 = 20 / 20** (1저자 화면 · `--refill-family` 설계족 표 20 행 · kind ↔ ntype 대조 통과 · 수확기 `--verify-sha` 성공 20 / 20 · union 20 / 20) — union 중앙: sphere 3.11 % · union 쌍 9.15 % · 쌍 clipped 9.66 % · union 정확 9.65 % · 겹침/상자 7.12 % ·
  검산: delta 열 ↔ 좌표 최대 3.07e-04 · sphere 웹앱 ↔ dual 최대 0.0 %p · 정확 union 음수 0 · 쌍 clipped < 정확 (상한 위반) 0 · 묶음 `~/lhss_harvest_20261011_r2.tgz` sha256 `baa03b6b65d57b7850df151a011d8102b605fc15d81aa9f58969629ac9d00aff` (⬜ 리포 반입 = 1저자 첨부 대기).
  다음 = 웹앱 접촉 · coverage 단계 (194 원천과 같은 코드 — `docs/reviews/g2rr6_fix_plan_20261011.md` §2 미확인 항목) → 보충 세대 2 망 배치 (새 등록 · 관측 ON).
