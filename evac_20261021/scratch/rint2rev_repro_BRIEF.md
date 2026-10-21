# Codex Rint ② 설계 리뷰 (10-21) — 우리 트리 재현 (읽기 전용 · 작업 트리 안 씀 · push 안 함)

## 입력
- Codex 미니 묶음을 푼 폴더 (믿지 않는 자료 · 읽기만): `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/import_rint2rev/x/`
  - 판정문 `codex_review_rint2_carbon_additive_design_20261021.md` · `REPRODUCTION.md` · `PIN.txt` (review_pin = `5dc6f7f0b91fd9db39ab595f6b8c79a8f0d2f3b5`) · `source_manifest.json` (Codex 가 쓴 핀 소스 1,161 파일의 경로 · Git blob · SHA256)
  - 탐침: `geometry/geometry_probes.py` · `geometry/convergence_probes.py` · `geometry/search_cg_counterexample.py` · `registration/probe_registration.py` · Part B `part_b/run_review.py` · `verify_fullpin.py` · `independent_join_checks.py` · `known_limit_and_mutant.py` (+ `part_b/REPRODUCTION_part_b.md` · `PART_B_REVIEW.md`)
  - Codex 결과: `geometry/*_results.json` · `registration/registration_probe_results.json` · `part_b/evidence/` …
- 미니 묶음에서 뺀 것 = 핀 소스 사본 `source/` (1,162 항목) — 리포 git 객체에서 다시 만든다.

## 할 일
1. **스크래치 작업 폴더** `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rint2rev_repro/` 를 새로 만들고, 탐침 · 결과 폴더를 거기로 **복사** (원본 폴더는 건드리지 않는다).
2. **핀 소스 다시 만들기**: `source_manifest.json` 의 모든 경로를 `git -C /home/user/Yonghoon-DEM-DFT show 5dc6f7f0b:<경로>` 로 `rint2rev_repro/source/<경로>` 에 쓰고 SHA256 을 manifest 와 대조 (1,161/1,161 같아야 · 다르면 보고).  `fetch` · `checkout` · 작업 트리 추가 하지 않는다.
3. **탐침마다 먼저 전부 읽는다** — 네트워크 · 묶음 밖 쓰기 · 삭제 · 임의 subprocess (python · git show 외) 가 없을 때만 실행.  경로 상수만 바꾼다 (원 코드 논리 바꾸지 않음 · 바꾼 줄은 diff 로 남긴다).  `python3 -I -X utf8 -B` 로 돌린다.  Windows 전용 부분 (Codex 환경 어댑터) 은 기록만.
4. 돌릴 것 (가벼운 것부터 · 무거운 것은 `nice -n 19` · 하나씩): geometry_probes · probe_registration · convergence_probes · search_cg_counterexample (오래 걸리면 고정 seed 한 번만) · Part B (`REPRODUCTION_part_b.md` 의 명령 · 시험 324 · 옛 138 판 · 탐침 144/113 · 독립 입력 62 · 실덤프 real14 · case15 — 리포의 `docs/data/real14_reference_20260928/` 등 실자료 경로는 핀 소스 사본 안 경로로).
5. **대조**: 우리 출력 ↔ Codex 결과 JSON 을 키별로 (정확히 같음 / 상대 차 ≤ 1e-12 / 그 밖 = 숫자와 함께) · 판정 문장에 쓰인 숫자 (RCA-01 의 31,622.7766 / 100,000 Ω · e 0.01885983293 · W 0.419353749 → 0.467828346 · RCA-02 W 0.293 → 0.836 · RCA-03 R 5 → 2 Ω · RCA-04 G 1 / 0.5 S · RCA-05 1.366013071895 / 5 / 0.238095238095 · RCA-06 90.49773756 % · P_SV 4.5351473923e-5 < P_VV 1e-4 · RCA-07 −1.88593002409e-4 · info 0 · 반복 10 · 이어 풀기 0 · A/B/C pass · RCA-12 1.1709917265 / 0.4932649517 · RCA-13 · §4-1 α 0.0134549613712 · K4/K8 0 · §5-2 dt 1.3108617603e-4 · 1.5257138934 · Part B 324 · 138 · 179/324 · 144 · 113 (PASS 8 / REJECT 105) · 62 (PASS 32 / REJECT 30) · real14 457 / 660 · case15 104 / 119 · `delta_bound_um` 0.002915255888325765) 을 우리 출력에서 찾아 같은지 표로.  환경 차 (우리 Linux · NumPy · SciPy 판 ↔ Codex Windows · NumPy 2.5.3 · SciPy 1.16.3) 는 판 번호와 함께 적는다.  RINT2-B-01 (Windows CRCRLF) 은 Linux 에서 재현 안 되는 것이 예상 — 그대로 적는다.
6. 결과 폴더 `rint2rev_repro/_repro_ours_20261021/` 에: 각 탐침 화면 로그 · 우리 출력 JSON · 대조표 `README.md` (한국어 · 표 · 판정값 차이 몇 개 · 환경 · 바꾼 경로 상수 diff).  큰 파일 (> 2 MB) 은 넣지 않고 sha256 만.

## 규칙
- 리포 메인 작업 트리 · 다른 작업 트리를 쓰지 않는다 (git show 로 읽기만) · push · fetch 안 함 · 디스크 적게 (source 사본 65 MB 는 끝나면 지운다 — 결과 폴더만 남김).
- 다른 에이전트 (Z3) 가 같이 돈다 — 무거운 시험은 하나씩.
- 보고 (한국어 · 표 · 짧게): 탐침별 실행 결과 · 판정 숫자 대조표 (같음 / 다름 + 값) · 환경 차 · 실행 못 한 것과 이유 · 결과 폴더 경로.
