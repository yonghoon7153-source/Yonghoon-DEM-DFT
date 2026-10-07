# Codex 세대 2 재검증 3 — 증거 반입 기록 (10-07)

- 판정문 = `docs/reviews/codex_review_gen2_network_reverify3_20261007.md` (ZIP 안 같은 이름 파일 **바이트 그대로** · sha256 `9a304a361aacf1c6bfee…` 같음).
- 원 ZIP = 1저자 업로드 `verify_evidence.zip` (5,993,229 B · sha256 `f858a4f8451a8bab3f678957544dc89405b11208ba2639912e909b86a26b09a4` · 1,393 항목 · 풀면 23 MB).
- 핀 = `0801d4ceb540f5a5813761b20a5e0f304ed80a03` (요청서 · 194 재등록이 들어간 커밋).

## 1. 이 폴더에 넣은 것 · 뺀 것

| 넣음 | 뺌 (원 ZIP 에만) |
|---|---|
| `README.md` (Codex 묶음 설명 원문) · `verify_evidence.py` · `run_probes.py` · `run_tests.py` · `probes/` (8 탐침) · `source_manifest.json` (432 파일 blob · sha256) · `bundle_inventory.json` | `evidence/release_gate/` 의 합성 배포 묶음 (15 MB — *"TEST_ONLY_NOT_A_GO · ML 에 넘기지 말 것"* 표지의 가짜 인계 CSV) — **각 변이체의 `build.log` 만** 넣었다 |
| `evidence/*.json` · `evidence/*.log` (탐침 · 시험 결과 전부 — 판정문 §1–§7 의 근거 표) | `evidence/acceptance/` (1.8 MB) · `evidence/branch_policy/` (1.0 MB) · `evidence/seal_paths/` (2.4 MB) — 합성 침대 · 합성 ROOT 픽스처 (탐침이 다시 만든다 · 아래 §2) |
| `evidence/new_gates/` (G2RR3-02 반례 ROOT · audit.json · 원 로그) · `evidence/scope_checks/` | `submitted/` (우리 요청서 · 등록 문서 사본 — 리포 정본과 같다) · `prepare_source.py` · `source_plan.json` · `extra_plan.json` (Codex 쪽 수집 기록) |

같이 올라온 ZIP 셋 (`reviews.zip` · `lhs_descriptors_cov_1e09f661d.zip` · `lhsx_handover_20261001.zip`) = Codex 에 준 **입력 묶음** — 파일 432 개 전부 핀 `0801d4ceb` 의 리포 파일과 바이트 같음 (120 · 207 · 105) ⇒ 반입하지 않는다.

## 2. 우리 트리 재현 (10-07 · Linux · Python 3.11.15 · numpy 2.4.6 · scipy 1.17.1 · networkx 3.6.1)

- 소스 = `source_manifest.json` 의 432 경로를 우리 git 에서 `git archive 0801d4ceb` (blob 대조 432/432 같음) · 탐침 원본 무변경 · `python3 -I run_probes.py branch_policy seal_paths new_gates release_gate` (묶음 밖 CWD).
- 결과 = **판정값 차이 0**:

| 탐침 | 대조 | Codex | 우리 |
|---|---|---|---|
| branch_policy (G2RR2-04 · 05) | 6 변이체 게시 상태 · CF 상태 · 사유 · 인계 + 숫자 143 개 | — | 숫자 차이 0 · 문자열 차이 0 |
| seal_paths (G2RR2-01 · 02) | audit rc 정상 · 원자료 SHA · + digest 삭제 · null · 옛 레코드 g2 선언 · 두 선언 삭제 | 0 · 1 · 2 · 2 · 1 · 2 | 같음 |
| 〃 | reread rc (정상 · plan 삭제 · cohorts=[] · cohorts 삭제) | 0 · 1 · 1 · 1 (n_fail 0 · 2 · 2 · 2) | 같음 |
| new_gates (**G2RR3-02**) | import 로그 없음 · **빈 파일 하나** · 봉인 밖 + 별도 로그 · 둘째 로그 소실 · 리포 밖 문자열 | rc 1 · **0** · 1 · **0** · **0** (관측 0 · 0 · 2 · 1 · 0) | 같음 |
| new_gates (**G2RR3-01**) | `v13_batch_gate_check` 수용 — 정상 · 없음 · `{` · null · {} · n_fail null · n_fail 1 · 감사 실패 · 감사 거부 | T · **T · T · T · T · T** · F · **T · T** | 같음 |
| release_gate (**G2RR3-01**) | 실제 `build_v13` → `check_v13` (8 변이체) | 정상 · 명시 실패만 거부 · 나머지 6 = 생성 · 문제 0 | 같음 |

- ⚠ 재현 첫 시도의 잘못 (기록만 · 결함 아님): 소스를 `scripts` · `webapp` 만 꺼냈더니 입력 지문 (`raw_sha256_table` · 코호트 TSV) 이 달라 audit 가 모두 rc 1 → 432 경로 전부로 다시 꺼내 같아졌다.  또 Codex 의 `evidence/seal_paths/baseline` 을 그대로 쓰면 manifest `repo_root` 가 Codex Windows 경로라 import 로그 줄이 봉인 기준 경로에 안 맞는다 — 픽스처는 탐침으로 우리 쪽에서 다시 만들어야 한다 (위 결과는 다시 만든 것).
- 원장: G2RR2-01 ~ 05 · GEN2-03 = verified (판정문 범위 그대로) · 새 `G2RR3-01` · `G2RR3-02` (P2 · open) — `docs/reviews/findings.json`.
