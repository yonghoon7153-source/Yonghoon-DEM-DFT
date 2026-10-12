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
- ✅ **10-11 수확 r2 묶음 반입** = `lhss_harvest_20261011_r2.tgz` (1저자 첨부 · 166,333 B · sha256 `baa03b6b65d57b7850df151a011d8102b605fc15d81aa9f58969629ac9d00aff` = WSL 화면 값 · 30 항목 전부 `lhss_out_20261011/` 아래 · 절대 경로 · `..` · 링크 없음) — 수확 기술자 20 (`descriptors_r2/`) · 첫 시도 요약 (`descriptors/`) · 코호트 TSV · 설계족 표 · union r2 · lhsx_001 대조 union.
  r2 JSON 에 `wall_near_tangent` 키 → 수확기 = `cc4210080` 이후 판 (194 수확 `1e09f661d` 와 다름 · 정확한 WSL HEAD 미확인) — 어느 판을 인계 원천으로 쓸지 = `docs/reviews/g2rr6_fix_plan_20261011.md` Q5 (⬜ 1저자).
- ✅ **10-12 1저자 Q5 = (가)** (`docs/reviews/g2rr6_fix_plan_20261011.md` §3 · Q4 = (가) `lhss` 별도 데이터셋) — 보충 20 을 **194 와 같은 판 `1e09f661d`** 로 다시 수확하고 r2 와 키마다 대조한다.
  r2 수확 체크아웃 = `a20fc1875` 계열 (첫 시도 코호트 표 머리 "도구 커밋 a20fc1875" · `wall_near_tangent` 키).  `1e09f661d` → `a20fc1875` 사이 수확 경로에서 바뀐 것 = 수확기 `scripts/lhs_descriptor_harvest.py` (+143 / −8) · union 이 부르는 `scripts/dem_analysis_core.py` (+700 / −37) · union 도구 docstring 3 줄 ·
  같은 것 = `scripts/lhs_harvest_batch.py` · `scripts/seal_area_cohort.py` (코호트 표는 r2 것을 그대로 쓴다 — 봉인기 파일이 두 판에서 같다) · `scripts/lhs_perc_extract.py` · `scripts/lens_geometry.py` · `scripts/parse_liggghts.py`.
  ⬜ 1저자 WSL (DESKTOP-IK8J81H · 몇 분 · 기존 `~/dem-audit` 체크아웃은 그대로 둔다 · 출력 폴더가 이미 있으면 멈춘다):

  ```bash
  cd ~/dem-audit && git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8
  git worktree add --detach ~/harv_1e09f661d 1e09f661d
  git -C ~/harv_1e09f661d rev-parse HEAD                    # 1e09f661d 로 시작해야 한다
  PY=$(ls ~/Yonghoon-DEM-DFT/venv/bin/python ~/Yonghoon-DEM-DFT/.venv/bin/python3 2>/dev/null | head -1); echo "PY=$PY"   # 비어 있으면 멈춘다
  O=~/lhss_out_r3_1e09f661d && mkdir "$O" && cp ~/lhss_out_20261011/_cohort.tsv ~/lhss_out_20261011/_design_family.csv "$O"/
  cd ~/harv_1e09f661d
  $PY scripts/lhs_harvest_batch.py --cohort "$O/_cohort.tsv" --out-dir "$O/descriptors_r3" --verify-sha 2>&1 | tee "$O/harvest_r3.log"
  $PY scripts/lhs_union_webapp.py --cohort "$O/_cohort.tsv" --out "$O/lhss20_union_r3.tsv" 2>&1 | tee "$O/union_r3.log"
  git -C ~/harv_1e09f661d rev-parse HEAD > "$O/harvest_head.txt"
  cd ~ && tar -czf lhss_harvest_r3_1e09f661d.tgz lhss_out_r3_1e09f661d && sha256sum lhss_harvest_r3_1e09f661d.tgz
  cp lhss_harvest_r3_1e09f661d.tgz /mnt/c/Users/Administrator/Downloads/
  ```

  ⚠ 10-12 정정 — 첫 판은 두 도구를 시스템 `python3` 로 불렀다.  10-07 같은 WSL 에서 시스템 python3 에 numpy 가 없어 실패한 기록이 있고 (`docs/data/ps45_plane_load_20261007/README.md` §2) · union 도구가 numpy 를 쓰며 · 수확 배치는 수확기를 `sys.executable` 로 부르므로 배치 venv (`$PY` · 194 등록 · v1.3 계획과 같은 줄) 로 바꿨다 (명령 · 인자는 그대로).
  → 묶음 첨부 · sha256 화면 → 반입 (이 폴더) · r2 와 키별 대조 (컨테이너) → 차이가 있으면 원인 표와 함께 보고 (r3 = 인계 원천 · r2 = 기록으로 보존).
