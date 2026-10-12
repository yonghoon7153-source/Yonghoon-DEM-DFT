# Codex 짧은 재확인 요청 — SUP20-01 · SUP20-02 수정 + 보충 20 입력 지문 영수증 (2026-10-12 · 결과 0 건 · 발송 = 1저자)

> **한 줄**: 보충 20 지원 검토 (리뷰 핀 `b429c3c1d` · **HOLD** · 새 P1 없음) 의 P2 `SUP20-01` · P3 `SUP20-02` 를 고쳤고 판정문 §5 Q6 의 입력 지문 영수증 도구를 만들었다 —
> 판정문 §5 "수정 diff + 채운 입력 봉인 / 사전 점검 영수증의 짧은 확인" 중 **컨테이너에서 할 수 있는 부분**이다.  두 결함이 닫히는지 · 발사 전에 남은 것이 무엇인지 판정해 달라.
> ✅ **1저자 10-12** — 수정 계획 `docs/reviews/sup20_fix_plan_20261012.md` Q1–Q4 = (가) 권고대로 (구현 기록 = 그 문서 §6).
> **리뷰 핀** = 이 요청서를 담은 커밋 **`a9422d2e7`** (고정 · 10-13 새벽 정정 — 원래 *"발송 때 `git rev-parse HEAD` 로 적는다"* 였으나 그 뒤 커밋 `a9fa84244` 가 `scripts/ps45_sigmae_factor_off_variant.py` (ps45 σ_e 보고 전용 실행기 · 이 검토와 무관) 를 더해, 발송 때의 HEAD 를 핀으로 적으면 §0 의 *"그 사이 다른 `scripts/` · `webapp/` 변경 0"* 이 거짓이 된다) · 수정 커밋 넷 = `4cae3a464` (SUP20-01) · `dd87e069c` (SUP20-02) · `dfee89184` (영수증 도구) ·
> `9a82bf138` (원장 · 증거) · 연장 세션 가지 병합 = `abbc63a4b` (SHA 그대로) · **기준** = 리뷰 핀 `b429c3c1d`.

## 0. 대상 · 지위

- 코드 diff = `git diff b429c3c1d <리뷰 핀> -- scripts/ webapp/` = **수정 넷의 코드뿐** — 그 사이 다른 `scripts/` · `webapp/` 변경 0 (`b429c3c1d` → `bef5bd5d7` · 병합 반대쪽
  `bd1db419d` · `33326218a` = 문서 · 자료).  파일: `scripts/lhs_release_build.py` (배포 생성기) · `scripts/test_lhs_release_v13.py` · `scripts/lhs_design_dataset.py` (인계 도구 = HANDOVER 파일) ·
  `scripts/supp20_input_receipt.py` (새 · 읽기 전용) · `scripts/check_all.sh` (주석 한 줄) · 등재 둘 (`docs/reviews/selftest_inventory.tsv` · `docs/reviews/doc_refs_allowlist.tsv`).
- 봉인 32 · `code_fp e8b2496b…` **무변경** · 수치 재계산 · 194 · 보충 20 · 시범 셋 재실행 없음 · WSL 실행 없음.  배포 도구 · 인계 도구 파일 지문은 바뀐다 (발사 manifest 에 기록).
- 판정문 = `docs/reviews/codex_review_supp20_support_20261012.md` · 반입 · 고치기 전 우리 재현 = `docs/reviews/codex_supp20_support_review_evidence_20261012/_README_import.md`.
- 원장 `docs/reviews/findings.json`: `SUP20-01` · `SUP20-02` = claimed_fixed (Codex 확인 전) · 자기 정정 `SELF-107` = open (§4-4).

## 1. 판정문 최소 해결 ↔ 수정

| 판정문 | 수정 |
|---|---|
| §1 ① 교차 입력 = 배치마다 검증한 관문 ROOT 하나 · 중복 저장한 batches ROOT / expect_set / datasets / n 은 권위 입력과 대조 | `v13_batch_gate_recheck` (`4cae3a464`) — 권위 = `batch_gate.batch_root` (194) · `supp_batch.batch_gate.batch_root` (보충) · 사본 `batches[이름]` 의 root (realpath 위치) · expect_set (= 배치 이름) · datasets (= `V13_BATCHES`) · n (= 등록 집합 크기 194 · 20) 대조 · ★ 빌드 기록 `cross_batch.roots` 도 권위와 대조 (같은 부류 사본) |
| §1 ② 필수 ROOT 결손 · 비문자열 · 없는 경로 = 거부 (생략 아님) | 권위 뿌리 결손 · 문자열 아님 · 없는 경로 = 문제 ("건너뛰지 않고 거부") · 사본 결손 · 없는 경로 = 사본 ≠ 권위 문제 · 교차는 권위 뿌리 둘이 다 있을 때 돌고 · 없으면 이미 문제 |
| §1 ③ 보충에도 194 와 같은 code_identity 존재 · 명시 승인 계약 | 한 도우미 `_v13_code_identity_problems` 를 194 (최상위 `code_identity`) · 보충 (`supp_batch.code_identity`) 이 부른다 (194 문구 그대로 · 보충 표지) · ★ `allowed` = 목록만 (§4-2) |
| §1 ④ 정상 / 반례를 build 와 check 에 상주 · 다른 ROOT 의 개별 관문 정상 대조 | 시험 V22 (§2) — check 반례 + **build 경로 둘** (build 는 한 뿌리로 관문 · 교차 · 사본을 적고 끝의 `check_v13` 으로 같은 대조를 받는다 — build 코드 무변경) · 대조 = 교체에 쓴 뿌리 둘 (다른 code_fp · 같은 code_fp) 자신의 관문 문제 0 |
| §2 — mono 규약 명시 · 비율 식은 bimodal 에만 · mono_AM_P = 1 · mono_AM_S = 0 · CSV · 계산 변경 불요 | `DESIGN_DEFINE` 문구 넷 (`dd87e069c` — `lhsx_w_AM_P` · `lhsx_w_AM_S` · `lhss_w_AM_P` · `lhss_w_AM_S`): P · S 슬롯 질량분율 · bimodal = AM_P · AM_S · mono (type 2 개) = 단일 AM 자리 (크기 라벨 = `*_kind`) · `ps_frac = w_AM_P / (w_AM_P + w_AM_S)` 는 bimodal 에만 · mono_AM_P → 1 · mono_AM_S → 0 · CSV · 계산 · 열 구성 무변경 |
| §5 Q6 — 한 영수증 (ID 지문 · 등록 §2 = 반입 재계산 = dry-run · 수확기 판 · 설계 / 어댑터 · union · r2 차이표 · 도구 핀 · 관측 ON · 새 ROOT 둘 · 사전 점검 · 발사 승인) | `scripts/supp20_input_receipt.py` (`dfee89184`) — §3 |

## 2. 시험 (반례 먼저)

| 시험 | 고치기 전 | 고친 뒤 |
|---|---|---|
| `scripts/test_lhs_release_v13.py` | V22 전 234/234 → V22 를 더해 **239 PASS · 17 FAIL** | **256/256** |
| └ V22 반례 17 — 판정문 · 계획 표 7 (supp_batch 만 다른 유효 뿌리로 교체 · 교체 + 사본 없는 경로 · 사본 없는 경로 (보충 · 194) · 사본 키 삭제 · 보충 code_identity 삭제 · 승인 없는 봉인 변경) + ★ 같은 부류 8 (같은 code_fp 의 다른 유효 뿌리로 사본 · 증거 교체 · 사본 expect_set · datasets · n · cross_batch.roots · `allowed` 문자열 (보충 · 194)) + build 2 (빌드가 사본 뿌리를 같은 code_fp 의 다른 뿌리 · 없는 경로로 적음) | 문제 0 · build 묶음 생성 (전부 오수용) | 전부 문제 ≥ 1 + 반례마다 사유 낱말 · build 둘 = "만든 묶음 대조 실패" · 산출 폴더 없음 |
| └ V22 회귀 · 대조 5 (정상 214 문제 0 · 다른 code_fp build 거부 · 교체 뿌리 자신의 관문 정상 · 교체 + 사본도 교체 = 교차 code_fp · 관문 뿌리 없는 경로 · 숫자 · 194 승인 없는 변경) | 통과 | 통과 |
| `scripts/lhs_release_build.py --selftest` | 31/31 | 31/31 |
| `scripts/lhs_design_dataset.py --selftest` | 389/389 → ㉛j (문구) · ㉛j2 (어댑터 CSV 실제 값 · Codex 네 행) 를 더해 390/391 (㉛j 만 FAIL) | **391/391** |
| `scripts/supp20_input_receipt.py --selftest` | 같은 시험을 accept-all 스텁 (계산 · 흐름 그대로 · 판정만 늘 같음) 에 = 6/40 | **40/40** |
| 게이트 `scripts/check_all.sh` | — | 전부 통과 (`9a82bf138` · 병합 `abbc63a4b` · 이 요청서 커밋) |

### 2-1. Codex 탐침 무변경 · 고친 트리 재실행 (`docs/reviews/codex_sup20_fix_probe_rerun_20261012/README.md`)

| `release_probe` 칸 | Codex (`b429c3c1d`) | 고친 트리 (`dfee89184`) |
|---|---|---|
| baseline_build · baseline_check · restored_check | 생성 · 문제 0 · 0 | 같음 |
| normal_build_different_fp | ReleaseError | 같음 (메시지의 합성 지문만 다름 — 시험용 축소 봉인 지도가 `scripts/lhs_release_build.py` sha256 을 싣는다 · 생산 지문 아님) |
| missing_cross_root · missing_supp_code_identity · unauthorized_supp_code_change | 문제 0 · 0 · 0 | 문제 1 · 1 · 1 |
| different_fp_gate_original_cross_roots · …_missing_cross_root | 문제 0 · 0 | 문제 4 · 4 (사본 뿌리 · 교차 code_fp · cross_batch.code_fp · cross_batch.roots) |
| different_fp_gate_matching_cross_root | 문제 2 | 문제 3 (+ cross_batch.roots) |
| 기존 경계 칸 (하중 99 · 인계표 출처 열 · τ 출처 부록 check) | 생성 · 문제 0 | 같음 (판정문 §3 Q3 · §6 — 이번에 바꾸지 않음) |

- `design_probe`: 판정값 차이 2 = `new_dictionary_claims` 의 `lhss_w_AM_P` · `lhss_w_AM_S` 새 문구뿐 · 나머지 같음 (재적합 실수 끝자리 14 키 ≤ 1e-12) · 키별 대조 = `docs/reviews/codex_sup20_fix_probe_rerun_20261012/compare_fixed.json`.

## 3. 입력 지문 영수증 — `scripts/supp20_input_receipt.py` (읽기 전용)

- 값의 정본 = 실행기 함수 (`registered_id_set` · `build_plan` · `cohort_specs` · `plan_input_digest` · `registered_production_set` · `print_followups` · `launch_eligibility` ·
  `production_observation_problem`) · 등록 문서 §2 · §3 · 수확 묶음 README — 도구에 값 사본 없음 (r2 허용 차이 두 칸만 README 끝 문장을 옮긴 상수).
- 칸: R0 (등록 문서 · README 값 — 자리 하나 · 값 하나) · A1–A2 (실행기 등록 표 = 등록 §2 · 등록 집합 성립) · B1–B3 (계획 = 등록 생산 집합 supp20 · 후속 다시 읽기 = `--expect-set supp20` ·
  입력 지문 = 등록 §2) · C1–C4 (r3 묶음 sha256 · harvest_head · 반입 파일 = 묶음 바이트 · 설계 · 어댑터 CSV sha256 · r2 ↔ r3 키별 대조) · D1 (봉인 32 code_fp = 등록 §3) ·
  (주면) E1–E6 발사 dry-run 화면 (`--dry-run-log` — dry-run 은 파일을 쓰지 않으므로 화면을 tee 로 받은 파일 · 등록 §4 grep 판도 읽는다 · 줄 꼴 = 진짜 `print_preflight`) ·
  F0–F6 / G0 · G1 · G2 · G4 · G5 실제 발사 manifest (`--manifest` 보충 · `--primary-manifest` 194) · H1 (새 ROOT 둘 · 같은 발사 커밋 · 같은 봉인 지문).
- rc 0 = 기계 대조 칸 전부 같음 · rc 1 = 다름 · 못 읽음 · 일반 계획 강등 · 등록 집합 불성립.  ⚠ rc 0 은 **발사 승인이 아니다** — 사전 점검 결과 · 저자 발사 승인 = 수동 칸 (기록만).
- **컨테이너 영수증** = `docs/reviews/codex_sup20_fix_probe_rerun_20261012/supp20_receipt_container.json` (트리 `dfee89184` · 깨끗함) = **rc 0 · 11 칸** —
  케이스 20 · ids `991cf115…` · raw 표 `a7aaa3c8…` · 원자료 결손 0 · 코호트 TSV `69d3f913…` · harvest_head `1e09f661d…` · r2 대조 = README 끝과 같음 · code_fp `e8b2496b…`.
- WSL 단계 (계획 Q4 (가) — 발사 승인 뒤 사전 점검에서): 발사 핀 `run --cohorts lhss --dry-run --observe-imports` 화면 → `--dry-run-log` · 발사 뒤 `--manifest` · `--primary-manifest`
  (명령 = 계획 §6 "영수증 쓰는 법").

## 4. 계획과 다른 점 · 자체 정정

1. **V22 가 계획 표 (반례 11 · 비준 전 초안 13 단언) 보다 넓다** — 같은 code_fp 의 다른 유효 뿌리 (교차 code_fp 로는 못 가르는 꼴) · `allowed` 문자열 · build 경로 둘 · 사유 낱말 단언 (22 단언 · 256).
2. **`allowed` 는 목록만** — Codex 최소 밖 · 같은 부류: 문자열이면 `f not in 'webapp/app.py'` 가 부분 문자열 일치로 승인했다 (**194 최상위 code_identity 에도** 있던 구멍 · 같은 도우미로
   함께 막음 · 옛 코드에서 V22 두 반례 = 문제 0).  실제 build (`v13_seal_gate`) 는 늘 목록을 적으므로 정상 기록의 판정은 그대로.  없음 · None = 승인 없음 (옛 판과 같음).
3. **`cross_batch.roots` 대조** — 판정문 ① 이 적은 사본 넷 (root · expect_set · datasets · n) 에 더한 빌드 기록 사본 (같은 부류).
4. **`SELF-107`** — 원장 `SUP20-02` 노트 · 계획 §2 Q2 (나) 가 전제한 "옛 인계 열 사전에도 같은 문구" 는 거짓: 커밋된 lhsx 인계 열 사전 넷의 `lhsx_w_AM_P` 행 = LREL-06 이전 일반 문구 ·
   결함 식 없음 (결함 문구는 10-06 `DESIGN_DEFINE` 이후 생성기에만) → 정정 표지 · Q2 (가) 결론 불변 (옛 사전 그대로 · 정오표 불요).
5. 영수증 칸이 계획 §3 의 ① ② 보다 넓다 (③ 수확기 판 · 묶음 · 설계 · 어댑터 · union · r2 · ④ 도구 핀 · 관측 · 새 ROOT 둘).  영수증의 일반 실행은 게이트에 걸지 않았다 (selftest 만 등재 ·
   ⬜ 일반 실행도 걸지 = 1저자).
6. 등록 §4 fetch 예시 (판정문 §5 끝) — 옛 연장 세션 가지 `claude/sdcp-dem-manuscript-si-pqwtv8` → 본 가지 `claude/stoic-knuth-NObVQ` (문서 개정 표지 · 결과 0 건 · 이 요청서 커밋 ·
   `docs/reviews/lhs_network_batch_registration_20261012_supp20.md` §4).  194 등록 §4 는 이미 본 가지.

## 5. 범위 밖 (이 요청이 묻지 않는 것)

- 194 발사 · 보충 20 발사 · v1.3 생성 · WSL dry-run 영수증 · 발사 핀 사전 점검 (fast16 + real4) · 저자 발사 승인 — 판정문 §4 최소 순서 ④–⑥ 그대로.
- 봉인 32 · `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` 무변경 · 수치 재계산 없음.
- 판정문이 기존 경계로 남긴 것 (인계표 고정 하중 칸 99 · 인계표 해시만 다름 · build 반환 `n_files` 27) · 재검증 7 의 한정 (S0b 12 자리 접두 · 평면 τ 최상위 칸 · case15 fixture) 은 그대로.

## 6. 질문

- **Q1.** `SUP20-01` (판정문 §1 최소 1–4) · `SUP20-02` (§2) 가 이 수정으로 닫히나.
- **Q2.** `allowed` 목록 강제 (194 최상위에도 걸린다) · `cross_batch.roots` 대조가 받아들일 만한가 — 정상 경로를 과잉차단하는 꼴이 있나.
- **Q3.** 영수증 도구 (컨테이너 범위 rc 0) 가 지금 단계의 Q6 증거로 충분한가, 아니면 WSL 발사 핀 dry-run 영수증 (`--dry-run-log`) 을 GO 전에 먼저 받아야 하나 (계획 Q4 (가) = 발사 승인 뒤 사전 점검에서).
- **Q4.** 새 결함이 있나 — 있으면 등급 · 반례, 없으면 이 수정 뒤 두 배치 발사 · v1.3 배포 전에 남은 조건을 적어 달라.

## 7. 재현 (리뷰 핀 · 컨테이너 Linux · Python 3.11.15)

```bash
git diff b429c3c1d <리뷰 핀> --stat -- scripts/ webapp/                 # 수정 넷의 코드 (다른 변경 0)
python3 scripts/test_lhs_release_v13.py                                # 256 PASS · 0 FAIL
python3 scripts/lhs_release_build.py --selftest                        # 31/31
python3 scripts/lhs_design_dataset.py --selftest                       # 391/391
python3 scripts/supp20_input_receipt.py --selftest                     # 40/40
python3 scripts/supp20_input_receipt.py                                # rc 0 · 11 칸 (컨테이너 범위)
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 bash scripts/check_all.sh   # ✓ 전부 통과
# Codex 탐침: 반입 묶음의 run_checks.py · probes 를 새 폴더에 · source = 리뷰 핀 체크아웃 · python3 -B run_checks.py design_probe release_probe (무변경)
```

- 윈도 스냅샷이면 판정문 §6 의 환경 실패 둘 (V10a POSIX 경로 문자열 · V16a git checkout HEAD) 은 그대로일 것이다 (V22 는 그 가정을 쓰지 않는다).
