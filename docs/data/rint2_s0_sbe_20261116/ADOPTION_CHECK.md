# kgy S0 단계 1 다시 (SBE · 최종 핀 64e4d213e · 저장본 재기) — 결과 전 기대 E1–E4 · 문턱 T1–T3 대조 (11-17 · 본 세션)

- 기준 = 결과 전 등록 `docs/reviews/rint2_s0_store_probe_20261112/README.md` (기대 E1–E4 · 문턱 T1–T3) + 최종 핀 등록 `docs/reviews/rint2_q14_finalpin_preparation_20261113/s0_preregistration.md` (수령 때 확인할 것 · E4 허용 목록 · T 문턱 숫자 그대로) · 블록 구성 = `docs/reviews/rint2_q14_finalpin_preparation_20261113/block_manifest.json`.
- 입력 = 이 폴더 (11-16 밤 대피 세션 반입 · 원본 tgz sha256 `80e4be49ef08f70f88846dd568d98bc846d3084893c8e1e679331c2563235070` · 안 파일 16 · 원본 sha256 = `MANIFEST.tsv` · 가린 사본 둘 = kit JSON · run.log) · 실행 = 00:48:09 → 02:20:56 UTC (`files/s0log_20261116T004809Z/meta.txt` · `operator_stop_utc` 05:48:08Z = 사람이 감시 셸을 멈춘 시각) · 핀 `64e4d213e8267bafaf3ae5af00a42996cefd3f33` · PROBE 1 · TAG q14final.
- 대조 = 이 폴더 사본 읽기만 (python -I · 아무것도 실행 안 함 · npz 는 사본 없음 = `NPZ_SHA256.txt` 의 sha256 만) · σ 칸 없음 (단계 1 = 접합 census · 계획 · 저장본 재기 · 솔브 없음).
- 지위 = 단계 1 채택 확인 기록 (11-16 README 의 `ADOPT_CANDIDATE` = 도구 자동 대조 · "rc 출처는 사람이 한 번 더" → 이 문서) · R 계획의 tol 값 · S0 계획 해시의 원천 = 이 폴더 `files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json` (sha256 `6346d9ed…`) · 실행 GO 아님.
- 판정 = **E1–E4 · T1–T3 모두 기대대로**.

## 기대 E1–E4

| | 대조 | 결과 |
|---|---|---|
| E1 | rc 0 (`files/s0log_20261116T004809Z/rss.log` 의 `rc=` 줄 = 끝 줄 하나 `rc=0` · README rc 근거 = run2.sh 15 줄의 S0 Python 자식 rc) · 여섯 출력 다 있음 (README 표) · 반입 도구 = ADOPT_CANDIDATE · `out_sha256.txt` 6 줄 = `MANIFEST.tsv` 원본 sha256 6/6 같음 · 계획 선언 sha256 (`cjunc_plan.sha256`) = 실제 `6346d9ed5fda248b89d1e28dbcb35c90d67264f060be345673c7da63f9924520` · kit JSON `code`: git_head = 핀 (위 40 자리) · git_dirty False · Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1 · 코드 지문 7 (`file_digests`) = 핀 blob sha256 7/7 같음 (ca_s0_census · step3_sigma · mpm_webapp_payload · fibre_segment_raster · sr01_stamp_compare · carbon_junction · ptfe_face_alpha) · 감싸개 `s0_store_probe.py` sha256 `6dd477748d65b582…` = 최종 핀 `block_manifest.json` 의 감싸개 (md5 `86e9bf4b4cfb79fa6e4a63d69cb414b0` · 11-13 과 같은 바이트) · 감시 셸 `mon.sh` sha256 `01a1b0fbabe64f35…` = 같은 manifest 의 `s0_monitor.sh` (md5 `13b1babd690950db9c758506bb35d951` · 11-13 판 `81118ead…` 에서 Python 호출 둘에 `-I -B` 만 더함 = manifest `preservation`) | ✓ |
| E2 | `store_probe.json` calls 1 · n_instances 117,583 · kit JSON `junction_census.census.n_instances` 117,583 (distinct · realized 같음) · 같은 침대 · 설정 · 입력 신원 = kit JSON 508 칸 가운데 11-13 판과 다른 칸 7 이 모두 E4 허용 목록 (아래) · 배열 둘 sha256 = 11-08 · 11-13 과 같음 → 행 수 = 11-13 기록 (117,583 · 117,070) | ✓ |
| E3 | encode ok (배열 470,415 · 8.9 s) · 쓰기 `built_written` · 읽기 `hit` · 같음 strict True · registry_fp True · object_is_new True · `store_start` preloaded `[]` · error None · `code_drift` `[]` · error None · machine-id 읽음 True | ✓ |
| E4 | 배열 둘 sha256 = 11-08 (`docs/data/rint2_s0_sbe_20261108/NPZ_SHA256.txt`) · 11-13 과 같음 (`s0_junctions_kit_SBE_vgcf100.npz` `a1d435792c60e759…` · `s0_instances_kit_SBE_vgcf100.npz` `7fc40335a233c159…`) · 계획 JSON 다른 칸 1 = `source.tool_sha256` (= 핀 `scripts/ca_s0_census.py` sha256 `97b54a4948c1d599…`) — 계획 sha256 `80a6c0b2…` (11-13) → `6346d9ed…` 은 이 칸 때문뿐 (11-08 계획과도 같은 한 칸) · kit JSON 다른 칸 7 = `code.file_digests` 둘 (ca_s0_census.py · mpm_webapp_payload.py — 핀 blob) · `code.git_head` · `code.tool_sha256` · `elapsed_s` (5,575.0 → 5,562.2) · `inputs.payload_argv_sha256` (새 출력 경로) · `plan.sha256` — 모두 최종 핀 등록의 허용 목록 · 칸마다 출처 = 핀 blob · 실행 경로 · 새 계획 | ✓ |

## 문턱 T1–T3

| | 값 | 문턱 | 결과 |
|---|---|---|---|
| T1 | 쓰기 120.095 s · 읽기 86.327 s · 읽기 / 짓기 = 86.327 / 4,011.155 = 2.15 % | ≤ 600 s · ≤ 300 s · ≤ 10 % | ✓ |
| T2 | `hwm_reset` True · VmHWM(②–④) 5,596,156 kB − VmRSS(① 앞) 4,896,400 kB = 699,756 kB ≈ 0.67 GiB | ≤ 4 GiB | ✓ |
| T3 | 저장본 파일 하나 (`cjreg_45bbb136….npz`) 1,340,095,705 B ≈ 1.25 GiB · 쓰기 · 읽기 영수증 바이트 같음 | ≤ 2 GiB | ✓ |

## 시간 · 메모리 (보고)

- S0 elapsed 5,562.2 s (11-13 = 5,575.0 · 11-08 = 5,382.8) · 원장 짓기 4,011.2 s → 저장본 적중이면 R 팔마다 짓기 − 읽기 ≈ 3,925 s (≈ 65.4 분) 를 아낀다 (어림 · R 원장은 문턱이 달라 열쇠가 다르다 · 11-13 기록과 같은 한정).
- 메모리: rss.log 5 초 표본 최대 5,734,112 kB ≈ 5.47 GiB (README) · 감싸개가 잰 S0 프로세스 VmHWM (원장 짓기 끝까지 · ① 앞) 8,289,788 kB ≈ 7.91 GiB — 5 초 표본이 짧은 봉우리를 놓치는 꼴은 11-13 과 같다 [관찰].
- 이 저장본 폴더 (kgy · 재기 전용) = R 은 읽지 않는다 (최종 핀 등록 §3 끝) · R 저장본 = 기계마다 새 빈 폴더 (봉인 후보 문서 · 1저자 결정 전).
