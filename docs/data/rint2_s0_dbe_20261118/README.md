# kgy S0 단계 2 (DBE 두 킷) 결과 반입 — 20261118

- 원본 묶음: `6c1564e2-s0dbe_20261118.tgz` · sha256 `cc40b0bb…` (1저자 업로드) · 항목 21 (폴더 포함) · 파일 16 · python `-I` 로 풀기 · 절대 경로 · `..` · 링크 0.
- 실행: kgy · 실행 트리 = 봉인 커밋 `29643188524f4fe31f81db5eb252edaa8cbbef7c` (가지 `claude/rint2-seal-20261118`) · venv Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1 (화면 줄) · 같은 판 확인 = S0 단계 1 보고의 `code.git_head` 와 S0 수치 경로 일곱 파일 `git diff --quiet` (`SAME_VERSION_OK`).
- 명령 = `files/scripts/s0_stage2_20261118_a2.sh` — `ca_s0_census.py --stage 2 --threshold-commit 29643188524f… --plan-path` (S0 단계 1 계획 · `docs/data/rint2_s0_sbe_20261116/`) `--r-plan-path docs/data/rint2_r_plan_20261118/ca1_plan.json --r-doc docs/reviews/rint2_seal_20261118/registration_R_sealed.md` · 킷 둘 = 새 DBE `kit_DBE_sdcp1um_vgcf100` (R 런 침대) · 옛 DBE `kit_DBE` (S0 표현 대조 전용).

## 시도

| 시도 | 시각 (KST · 11-18) | 결과 |
|---|---|---|
| 1 | 04:54 → 06:53 새 침대 census · 그 뒤 옛 침대 거부 | rc 2 · `[S0] ⛔ 거부 — <V100_HOME>/sdcp/kit_DBE/run_…20260812_211730_76402: se_dump.npy 없음` (`files/logs/s0_stage2_a1*.out` · `.log`) · 출력 폴더 = `ca1_s0_dbe_a1` 로 옮겨 보존 |
| 2 | 09:27 → 11:26 새 침대 (7,139.1 s) · 11:27 → 13:36 옛 침대 (7,803.3 s) | rc 0 · 보고 둘 (요약 `files/a2/*.summary.json` · sha256 아래 표) · 화면 `files/logs/s0_stage2.log` · `s0_stage2_nohup.out` |

- 첫 시도 거부 원인 = 옛 킷의 `latest_run` 이 v100 절대 경로를 가리켜 kgy 에서 죽은 링크 · S0 `find_run_dir` 는 죽은 링크도 '있음' 으로 읽어 그 경로로 갔고 (거부 = fail-closed) · 러너 `run_arm` 이었다면 마지막 `run_*` (se_dump.npy 있음) 를 골랐다 → 원장 `S0FR-01` (P3 · open · 봉인 코드라 고치지 않음).
- 두 번째 시도 준비 = `files/scripts/s0_stage2_a2_prep_v2.sh` (1 판 `s0_stage2_a2_prep.sh` = 08-12 런에 `fibre_kind` 없음 → 발사 전 멈춤) — 옛 킷 원본에 쓰기 0 · 보기 폴더 `<HOME>/sdcp/s0view_20261118/kit_DBE` (원본 항목 전부 링크 · `latest_run` 만 러너 규칙이 고르는 런 `run_VGCF3_PTFE0.5_SDCP0.5_20260827_150029_3687585`) · 사전 점검 = 두 킷 `kit_input_record` (census 입력 단계) 통과 뒤 발사.
- **이탈 (1저자 11-18 Q2 수용)**: 옛 DBE 킷을 원본 폴더가 아닌 보기 폴더로 넣었다 — 명령 차이 = `--kit` 경로 한 곳 (`files/scripts/` 두 판 비교).  새 침대 · R 계획 · 봉인 문턱 무관.

## 결과 대조

| 항목 | 값 |
|---|---|
| S0 계획 sha256 (두 보고) | `6346d9ed5fda248b89d1e28dbcb35c90d67264f060be345673c7da63f9924520` (= S0 단계 1 계획) · 출처 `commit:29643188524f…` |
| R 계획 sha256 · s_min | `d8595a52…` · 0.0 µm (화면 · 보고) |
| 새 침대 보고 | `e69894817ea9aded81ff8484d7fff4eea51cb950bcde613e984811fba7ee568b` (6,289,510 B) |
| 옛 침대 보고 | `1122d6d1e66e3dd923dbe0d669545a243699d76bfeb91b58a321a2ed94d7b4f6` (6,276,317 B) |
| 결정성 (새 침대 · 시도 1 ↔ 2) | npz 둘 · payload 로그 sha256 같음 · 보고 JSON 차이 = `elapsed_s` 한 칸 (7140.9 ↔ 7139.1) — `DETERMINISM.json` |
| 두 기계 사본 | gabia 새 침대 보고 sha256 = 같음 · gabia S0 단계 1 보고 사본 `c9307cfc…` (6,286,674 B = 원본) · R 시작 0 단계에서 두 기계가 세 해시 (R 계획 · 새 침대 보고 · 단계 1 보고) 기대대로 — `docs/data/rint2_r_start_20261118/` |

- 새 침대 census 요약 (화면): VV 117,575 · 자기 후보 0 · 긴 접촉 30,261 · 배율 합 128,491 · 미실현 covered_SDCP 2,137 · 캡슐 부피 비 0.6327 (밴드 안) · tol_ff 0.0738125 (점 간격 중앙 0.147624 µm) · 같은 셀 비연속 재방문 853 쌍 (s 최대 0.1889 µm).  R 사슬이 이 보고의 봉인 계획 해시를 지금 계획과 정확히 대조한다 (`S0_REPORT_MISMATCH` · 등록 R §2-1 끝) — 이 기록은 판정이 아니다.
- 등록 R §2-1b 결과 전 기술 보고 (R 결과 보고에 옮겨 적을 값): 새 DBE 침대 자기 후보 0 · 그중 s ≤ (π/2)·D (0.3516 µm) 0 — 자기 접합 후보 진단으로만 적는다 (0 이어도 DBE 전체 분류가 같다고 선언하지 않는다 · 봉인본 ⑤′).
- σ 없음 (S0 = 구조 census · 풀이 없음).

## 원장 · 사본

- `SELF-184` (P3 · open) — 봉인 뒤 두 기계 현장 확인 목록에 S0 단계 2 의 둘째 킷 (옛 kit_DBE) 을 넣지 않아 그 킷의 죽은 `latest_run` 을 발사 4 h 뒤 첫 시도 거부로 알았다 (영향 = 시간 · 값 무관).
- `S0FR-01` (P3 · open) — 위 거부 원인.
- 가림: 홈 경로 → `<HOME>` (kgy) · `<V100_HOME>` (v100 · 죽은 링크 글) · `listing.txt` 의 소유자 · 묶음 → `<USER>` · 가린 곳 수와 원본 sha256 = `MANIFEST.tsv`.
- 사본 없음: npz 넷 (sha = `files/SHA256_kgy_outputs.txt`) · 첫 시도 새 침대 보고 JSON (`c7a772c3…` · 차이 = `DETERMINISM.json`) · 두 번째 시도 보고 JSON 둘 = 요약만 (`files/a2/*.summary.json` = 긴 목록은 길이만 · 나머지 칸 그대로 · 원본 sha256 = `MANIFEST.tsv`) — 전체 사본은 철회값 스윕이 접합 목록의 숫자 속 부분 일치 10 건 (`mult` 1.1232… · `Lc_um` 1.2228413…) 을 잡아 넣지 않았다 (원본 = kgy · 새 침대 보고 사본 = gabia).
- 이 폴더 바이트 = `SHA256SUMS`.  묶음 파일은 읽기만 했고 실행하지 않았다.
