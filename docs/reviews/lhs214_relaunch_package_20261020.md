# LHS214 다시 발사 — 다섯 단계 묶음 (2026-10-20 밤 · 문서 · 계산 대조만 · 결과 0 건 · ⬜ 1저자 비준 · 발사 승인 전)

- 근거: Codex 10-20 재확인 `docs/reviews/codex_review_lhs214cx_fix_recheck_20261020.md` §5 (다섯 단계 · 새 선행 조건 없음) · 10-19 판정 `docs/reviews/codex_review_lhs214rr_fix_recheck_20261019.md` §7 끝 ·
  `docs/reviews/codex_review_lhs214s_fix_recheck_20261019.md` §6 Q5 (다섯 단계 원문) · SUPR 재확인 `docs/reviews/codex_review_supr_fix_reverify_20261014.md` §2 · §3 ·
  등록 194 `docs/reviews/lhs_network_batch_registration_20261007_g2.md` §2 · §3 · §4 · §9-7 · §9-8 · 보충 20 `docs/reviews/lhs_network_batch_registration_20261012_supp20.md` §2 · §3 · §4 · §9-1 · §9-3.
- 계산 트리 = 이 문서를 담은 커밋의 부모 (본 가지 `claude/stoic-knuth-NObVQ` · 10-20 밤).  봉인 32 · 인계 도구 2 · 배포 빌더 · 실행기 · 영수증 도구 · 스모크 도구 · 두 등록 문서 = Codex 10-20 리뷰 핀
  `34713ac96` 과 바이트 같음 (`git diff --quiet` rc 0 · 부록 A-1).  값은 저장소 함수 (`run_network_194_parallel` · `supp20_input_receipt` · `seal_s3_prerun`) 를 그대로 불러 다시 쟀다 (새 식 없음 · 부록 A).
- 권고안 기준으로 썼다 — 1저자가 정할 자리 = ⬜ 1저자 (§6 Q1–Q5).  이 문서는 등록 문서 · 코드 · 원장을 고치지 않는다 (비준 문안 = §1 의 diff 꼴만).

## 0. 이번에 닫는 것 / 닫지 않는 것

**닫는 것 (준비 · 대조 · 명령)**

| # | 무엇 | 자리 |
|---|---|---|
| ① | 비준할 문안 — 두 등록의 바뀌는 줄 표 + `git apply --check` 통과 diff · 비준 전 · 뒤를 영수증 도구 파서 · 영수증 · selftest 로 확인 | §1 |
| ② | 지문 재결합 표 — 등록 값 ↔ 계산 트리에서 저장소 함수로 다시 잰 값 · 다르면 이유 · 들어갈 자리 | §2 |
| ③ | B7 승인 핀 — 정의 · 사전 점검 · 두 manifest · `--approved-sha` 가 실리는 자리 (file:line) | §3 |
| ④ | WSL 사전 점검 명령 (새 핀 · 새 ROOT 둘 · fast16 + real4 · 완료 영수증 · 대조 · 194 손 대조 재료 · 묶음) + 결과 전 기대 | §4 |
| ⑤ | 1저자 발사 승인 전 확인표 · 구 ROOT · 실패 기록 처리 | §5 |
| — | Codex 짧은 발사 확인 요청 초안 (⬜ 1저자 Q5) | `docs/reviews/codex_lhs214_relaunch_check_request_20261020.md` |

**닫지 않는 것**

| 무엇 | 상태 |
|---|---|
| 등록 비준 | ⬜ 1저자 Q1 — 이 문서는 문안만 |
| 실제 발사 | ⛔ ⑤ 1저자 별도 승인 뒤 (§4 끝 블록 = 꼴만) |
| S3 | 별도 HOLD — S3 수치 모듈 (`seal_s3_prerun.NUMERIC_MODULES` 6) 중 `scripts/network_conductivity.py` 가 등록 §3 표 대비 바뀜 → S3 재봉인 의무 (봉인 창 09-17 닫힘 · 저자 결정) |
| v1.3 주 학습 인계 | HOLD — H0 model_limit 행 = v1.3 주 타깃 배포 HOLD (194 등록 §9-8 ⑤ · `lhs_release_build.v13_primary_model_limit_problems`) |
| `L214R-S03` · `L214R-S05` | open · 한정 유지 (Codex 10-19 §6 Q4 · 10-20 §5) |
| σ₀ 1.5 솔버 상수 | 이번 재봉인 밖 (권고 · ⬜ 1저자 Q2) |
| ⚠ **새로 찾은 것** — 영수증 도구 selftest `S0b` | 비준 문안을 넣으면 `scripts/supp20_input_receipt.py --selftest` 가 **121/122** (§1-3) · 시험 기대 한 군데의 코드 변경이 필요 → 이 문서 밖 (코드는 고치지 않았다 · ⬜ 1저자 Q3) |

## 1. ① 비준할 문안

### 1-1. 비준되면 바뀌는 줄

| 문서 · 자리 | 지금 원문 | 비준판 | 이력 표지 |
|---|---|---|---|
| 194 머리 (원문 19 줄 뒤 · 새 줄) | — | ✅ ⬜(날짜) 비준 한 줄 — §3 활성 = `2149f873…` · §5 = §9-8 ①–⑦ · 발사 승인 아님 · S3 별개 | *결과 열람 뒤 정책 개정 (10-14 실행 결과를 본 뒤)* · §9-9 |
| 194 §3 — 10-07 재등록 줄 (원문 118) · 발사 커밋 줄 (원문 124) | `` `code_fp e8b2496b…` `` (기계 구문) | 같은 값을 맨 hex 로 + *"비준 뒤 역사 · 활성 = 이 절 끝 ✅ 줄"* | 값 그대로 보존 |
| 194 §3 표 4 행 (network_conductivity · tau_flux · app · pipeline_service) | 10-07 재등록 sha256 | 행 그대로 + *"비준 뒤 = §3 끝 ✅ 줄"* | 옛 값 = 표에 전체 그대로 |
| 194 §3 끝 (새 ✅ 줄) | — | `` `code_fp 2149f873…` `` (§3 의 유일한 기계 값) · 바뀐 4 파일 새 sha256 전체 · 인계 도구 2 · 배포 빌더 sha256 전체 · 발사 커밋 = B7 · 사전 점검 화면 기대 (지연 import 92 포함) | 10-07 재등록 = 역사 (§9-9) |
| 194 §5 머리 (새 줄) | — | ✅ 비준 표지 = §9-8 ①–⑦ 활성 · 원문 1–7 그대로 | *결과 열람 뒤 정책 개정* |
| 194 §9-8 머리 · 표 머리 | *⬜ 1저자 비준 대기* · *개정 초안 (⬜ 비준 대기)* | *✅ ⬜(날짜) 1저자 비준 = §9-9 (비준 전 표지: ⬜ 1저자 비준 대기)* · *개정 (✅ … 비준 전 칸 이름: 개정 초안 (⬜ 비준 대기))* | 원 표지는 괄호 안에 보존 · *결과 열람 뒤 정책 개정* 그대로 |
| 194 §9-8 표 §3 행 | `` `code_fp_pending 2149f873…` `` (대기 선언) | 맨 hex `2149f873…` + *"✅ 비준 = §3 활성 · 대기 선언 꼴 지웠다 — 비준 전 원문: …"* | 비준 전 원문 문장 보존 |
| 194 §9-9 (신설) | — | 비준 · 변경 이력 — 바뀐 자리 넷 · 바꾸지 않은 것 · 발사 승인 아님 · S3 · v1.3 | 10-14 결과 수 (194 done 186 · 실패 8 · 보충 20 done 14 · 실패 6) 명시 |
| 보충 머리 (원문 8 줄 뒤 · 새 줄) | — | ✅ 비준 한 줄 | 같음 · §9-4 |
| 보충 §3 (원문 42) | `` `code_fp e8b2496b…` `` | 같은 줄에서 값만 `` `code_fp 2149f873…` `` (Codex `minimal_activate_section3` · 영수증 selftest S12a 꼴) + 옛 값 맨 hex | 옛 값 = 그 줄 + §9-3 표 원문 칸 |
| 보충 §3 (원문 44 줄 뒤 · 새 줄) | — | 비준 판 인계 도구 · 배포 빌더 = 194 §3 끝 ✅ 줄 | — |
| 보충 §5 머리 (새 줄) | — | ✅ 비준 표지 = §9-3 활성 | *결과 열람 뒤 정책 개정* |
| 보충 §9-3 머리 · 표 머리 · §3 행 | 194 와 같은 꼴 | 194 와 같은 꼴 (대기 선언 삭제) | 같음 |
| 보충 §9-4 (신설) | — | 비준 · 변경 이력 | 같음 |

바꾸지 않는 줄: 두 등록 §2 · §9-8 / §9-3 의 *바꾸지 않는 것* · §9-8 ⑦ 원문 (*"봉인 수치 모듈 둘"* 표현 포함 — 정확한 모듈 = §9-9 · 부록 A-5) · 10-14 기록 (194 §9-7 · 보충 §9-1 · §9-2).

### 1-2. 비준판이 지키는 세 규칙 (판정문 §5 ①)

| 규칙 | 비준판에서 |
|---|---|
| 대기 선언을 승인 지문으로 자동 취급하지 않는다 | 대기 선언 (`code_fp_pending` 꼴) 은 두 문서에서 지우고, 활성 값은 1저자 비준 표지가 붙은 §3 줄에만 둔다 (영수증 도구는 활성 §3 기계 구문만 읽는다 — L214R-04 `e6f7895d0`) |
| 역사 보존 | 옛 활성 값 `e8b2496b…` · §3 표 4 행 옛 값 · 비준 전 표지 · 비준 전 원문 문장 = 같은 자리에 맨 hex · 괄호로 남김 |
| 결과 열람 뒤 변경 이력 | §9-9 · §9-4 머리에 *"결과 열람 뒤 정책 개정 — 10-14 실행 결과 (…) 를 본 뒤"* · 10-14 ROOT · 실패 기록 보존 · 사후 성공 전환 없음 |

### 1-3. 비준 전 · 뒤를 저장소 도구로 (계산 트리 · 부록 A-12 · A-13 · A-14)

| 대조 | 지금 커밋된 문서 | 비준 사본 (1-4 · 1-5 diff 를 적용한 사본 · 스크래치) |
|---|---|---|
| 보충 `registration_values` — §3 code_fp · 대기 · 문제 | `e8b2496b…` · `2149f873…` · 없음 | `2149f873…` · None · 없음 |
| 보충 `receipt()` 컨테이너 범위 (11 칸) | rc 1 · 실패 [D1] (D1 now = `2149f873…` · registered = `e8b2496b…` — Codex 10-20 실측과 같음) | **rc 0 · 실패 없음** |
| selftest 상태 (`_selftest` 의 `fp_state` 규칙 · 줄 565–576) | pending | registered |
| 보충 `--selftest` (같은 프로세스 · 등록 문서 경로만 사본으로 · 이 컨테이너) | 122/122 rc 0 | **121/122 rc 1 — 실패 `S0b` 하나** (줄 619–623 이 등록 §3 접두 `e8b2496b…` 를 상수로 기대) |
| 194 사본 §3 (같은 파서 `_md_section` · `_one`) | 기계 값 `e8b2496b…` 하나 · 대기 선언 1 | 기계 값 `2149f873…` 하나 · 대기 선언 0 · 표 28 행 + ✅ 줄 4 행 = 계산 트리 해시 32/32 · `code_fp(…)` = `2149f873…` · ✅ 줄 인계 도구 · 배포 빌더 3/3 = 계산 트리 |
| `git apply --check` (계산 트리) | — | 194 rc 0 · 보충 rc 0 |

⇒ 비준을 문서만으로 넣으면 WSL 사전 점검의 영수증 도구 selftest 가 121/122 · rc 1 이 된다.  그 selftest 는 `check_all.sh` 밖이다 (`docs/reviews/selftest_inventory.tsv` 레인 none) — 게이트는 못 잡고 사전 점검 화면에서 처음 드러난다.  처리 = §6 Q3.

### 1-4. diff — 194 등록 (`⬜(날짜)` = 비준 날짜로 바꾼 뒤 `git apply`)

````diff
--- a/docs/reviews/lhs_network_batch_registration_20261007_g2.md
+++ b/docs/reviews/lhs_network_batch_registration_20261007_g2.md
@@ -17,6 +17,7 @@
   (발사 전에 적용하면 봉인 지문이 바뀌어 이 등록의 배치가 아니다 · 10-07 이 커밋 트리에서 `git apply --check` 통과).
   ⚠ 웹앱 3D 자료 패치 (`docs/reviews/webapp_load_view_deferred_20261007.patch` — #11 AM 만 칠하기 · WEB-06 압축 접촉만 범위 · 같은 봉인 파일 `webapp/app.py`) 도 **발사 뒤** ·
   v1.3 화면 패치와 같은 때 넣는다 (1저자 10-07 Q3 *"권고대로"*) · 두 패치는 순서 무관 (10-07 HEAD `afda0d7ab` 에서 `git apply --check` 양쪽 순서 통과) · 넣은 뒤 `bash scripts/check_all.sh`.
+> ★★ **✅ ⬜(날짜) 1저자 비준 — L214 개정 (§9-8 · 결과 열람 뒤 정책 개정 = 10-14 실행 결과를 본 뒤) · 변경 이력 = §9-9** — §3 활성 봉인 지문 = `2149f873…` (§9-8 의 대기 선언을 §3 으로 옮기고 선언은 지웠다 · 10-07 재등록 `e8b2496b…` = 역사) · §5 활성 개정 = §9-8 ①–⑦ · 원문은 각 자리에 그대로.  ⛔ 이 비준은 발사 승인이 아니다 (§9-8 ⑦ B7 — 새 승인 핀 사전 점검 · 1저자 별도 발사 승인) · S3 = 별개 HOLD.
 
 ## 0. 순서
 
@@ -115,13 +116,13 @@
   Codex dependency_gap: 그 사본의 K_IC 0.3 → 30 이면 multicrack 100 → 0 인데 옛 29 파일 봉인은 통과) · + `scripts/lhs_union_webapp.py` (`dem_analysis_core` 지연 import —
   τ 의 L_mc · φ_mc 를 내는 정확 union · 우리가 같은 부류로 찾음) · + `scripts/ml_design_structure.py` (`structure_predictor` 모듈 수준 `_restricted()` 안의 import —
   app 을 읽을 때마다 돈다 · 실제 import 관측이 찾음).  바뀐 봉인 파일 둘 = `scripts/tau_flux.py` · `webapp/pipeline_service.py` (G2RR2-04 · 05 `5dde71dcc`).
-  ⇒ **`code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71`** (런처 `code_fp(code_hashes())` · 이 컨테이너 194 dry-run 이 같은 값).
+  ⇒ **`e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71`** (10-07 재등록 지문 — ✅ ⬜(날짜) 비준 뒤 역사 · 활성 = 이 절 끝 ✅ 줄 · 기계 구문 `code_fp` 를 떼었다 · §9-9) (런처 `code_fp(code_hashes())` · 이 컨테이너 194 dry-run 이 같은 값).
   정적 닫힘 30 ⊆ 32 (닫힘 밖 둘 = S3 수치 모듈 그대로) · 지연 import 분류 (`lazy_import_census`) 90 · 분류 밖 0 (경로 밖 사유 `DEP_LAZY_OFFPATH` 21) ·
   실제 import 관측 (selftest ㉟d — 합성 se_am 을 실제 `run_pipeline(stop_after='network')` 로 · 단계 하위 프로세스 포함) 리포 모듈 22 ⊆ 32.
   ⚠ 관측 22 는 합성 침대의 표준 경로다 — 실침대 경로는 §1 시범의 `--observe-imports` 가 본다 · 리터럴이 아닌 동적 import 는 정적 분류가 못 본다 (관측이 메운다).
 - ⚠ **10-07 05:2x 갱신** — 요청서 핀 `2802c649e` 뒤 `webapp/app.py` 가 한 번 더 바뀌었다 (atom + 판 메시만 올린 케이스의 porosity — atoms-only 경로만 · 망 정지 경로 · 생산 · 게시 · 인계 코드 무변경 · 시험 `webapp/test_atoms_only_porosity.py` 41/41 · `test_pipeline_provenance` 284/284) ⇒ 봉인 지문 `f3f54951…` → `b313e61ab551…` (아래 값 갱신 · 런처 `code_fp(code_hashes())` 로 다시 계산 · 29 파일 중 `webapp/app.py` 한 줄만 바뀜).  발사는 이 지문의 커밋으로.
 
-- 발사 커밋 = 아래 **32 파일** sha256 (= 봉인 지문 `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` · 10-07 재등록 — 앞 판의 29 파일 `b313e61a…` 는 역사) 과 같은 코드를 담은 커밋 — 이 문서를 담은 커밋 또는
+- 발사 커밋 = 아래 **32 파일** sha256 (= 봉인 지문 `e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` · 10-07 재등록 — 앞 판의 29 파일 `b313e61a…` 는 역사 · ⚠ ✅ ⬜(날짜) 비준 뒤 = 이 절 끝 ✅ 줄의 32 파일 · 지문) 과 같은 코드를 담은 커밋 — 이 문서를 담은 커밋 또는
   그 뒤 **문서 · 원장만** 바뀐 커밋.  1저자가 발사 직후 §9 에 `git rev-parse HEAD` · manifest `seal.code_fp` · `expected_network_generation` 을 적는다 (지문이 이 값과 다르면 이 봉인의 배치가 아니다 ·
   추적 파일이 바뀐 트리는 실행기가 거부한다).
 - ★ 전이 의존 (판정 §7-3): 10-05 판 19 파일에 **워커의 망 정지 경로가 실제로 import 하는 리포 모듈 10** 을 더해 29 (`CODE_FILES`).  정적 닫힘 (`code_dependency_closure` — 시작점 =
@@ -133,7 +134,7 @@
 
 | 파일 | sha256 | 10-05 봉인 대비 |
 |---|---|---|
-| `scripts/network_conductivity.py` | `da9ecfefd8dc4b84e222140e347e4a718381169f27c88bf56c71ec4a7c2749be` | 바뀜 (`f3f720985` 포함 — sha256 `61f00fef…` → `da9ecfef…` 는 그 커밋 메시지) |
+| `scripts/network_conductivity.py` | `da9ecfefd8dc4b84e222140e347e4a718381169f27c88bf56c71ec4a7c2749be` | 바뀜 (`f3f720985` 포함 — sha256 `61f00fef…` → `da9ecfef…` 는 그 커밋 메시지) · **비준 뒤 = §3 끝 ✅ 줄** |
 | `scripts/plastic_coverage.py` | `cce27a34c0bf2e4f5c122e43d983aa3414a825ab461a00abd408dba02e151348` | 바뀜 |
 | `scripts/audit_constriction_deleted.py` | `180287be199ea60e6a50ba6cd0baf854c18a18568c476f7e0200c2caca3faf9d` | 바뀜 |
 | `scripts/extract_se_network_diagnostics.py` | `db7151b51252e60c42c2bc2a2b3173ae6f4b97a94226b51a97b1e357e028ea9a` | 같음 |
@@ -144,12 +145,12 @@
 | `scripts/parse_liggghts.py` | `4fe3f1f32ebc4168978c7278b7a1d37b072d64fbf00e97d0933351337d223425` | 같음 |
 | `scripts/se_material.py` | `767a6a383d4581274b07ee79146a53fbe118f1f6eb0acb9ec0a5af21c9c9930c` | 같음 |
 | `scripts/metrics_json.py` | `baa671f895dd6103cf95c25647ee45877d98306f00ab15cd3968fbe4354a7702` | 같음 |
-| `scripts/tau_flux.py` | `eb9388ec8bd2d40b1c63365ae72b6850e9fc51fd9ce0780df4e557424a1440fb` | 바뀜 (10-07 재등록: + G2RR2-04 · 05 `5dde71dcc` — 앞 판 `6bc4037c…` 대비도 바뀜) |
+| `scripts/tau_flux.py` | `eb9388ec8bd2d40b1c63365ae72b6850e9fc51fd9ce0780df4e557424a1440fb` | 바뀜 (10-07 재등록: + G2RR2-04 · 05 `5dde71dcc` — 앞 판 `6bc4037c…` 대비도 바뀜) · **비준 뒤 = §3 끝 ✅ 줄** |
 | `scripts/lhs_webapp_batch.py` | `b9d0199cc1bd23cd1ed5405a283081c2c3a31bc6ce256670c8a9b63d177b5668` | 같음 |
 | `scripts/lhs_harvest_batch.py` | `4d798c631ac893ca32018fde58145bc5c8a2e3e2a6423da61cb87bd13599148e` | 같음 |
 | `scripts/lhs_descriptor_harvest.py` | `96fa643e309aab46b2a5cbd59e2276ee16b99107a9a7514e5d9fdcaf5c2d8d9e` | 바뀜 (`cc4210080` — LHSC-08 · 분류 불변) |
-| `webapp/app.py` | `bd4c25e507e3c7a2b8e35f9b4602f22ab17d8e56fb6f8980021d33323994826b` | 바뀜 (G2RR-01 `e1dab4265` · G2RR-02 `f3f720985` · 3D 뷰어 라우트 `761e32645` · `92839aeb7` 포함) |
-| `webapp/pipeline_service.py` | `33a700300e8c650ca953e96b7faaea3010245b63e6d2035d4b73b4a61e1c7843` | 바뀜 (G2RR-01 `e1dab4265` · G2RR-02 `f3f720985` 포함 · 10-07 재등록: + G2RR2-04 `5dde71dcc` — 앞 판 `2414fb21…` 대비도 바뀜) |
+| `webapp/app.py` | `bd4c25e507e3c7a2b8e35f9b4602f22ab17d8e56fb6f8980021d33323994826b` | 바뀜 (G2RR-01 `e1dab4265` · G2RR-02 `f3f720985` · 3D 뷰어 라우트 `761e32645` · `92839aeb7` 포함) · **비준 뒤 = §3 끝 ✅ 줄** |
+| `webapp/pipeline_service.py` | `33a700300e8c650ca953e96b7faaea3010245b63e6d2035d4b73b4a61e1c7843` | 바뀜 (G2RR-01 `e1dab4265` · G2RR-02 `f3f720985` 포함 · 10-07 재등록: + G2RR2-04 `5dde71dcc` — 앞 판 `2414fb21…` 대비도 바뀜) · **비준 뒤 = §3 끝 ✅ 줄** |
 | `scripts/export_master_csv.py` | `2899dc2410ad8840dadf41993511c225d60f29f77edfdb2fac6703b25ccf767b` | 같음 |
 | `scripts/type_map_resolve.py` | `4a289c6412e4b8e1bc0fba573cb287966dfa00a053399097b587f1e14726bfe5` | 같음 |
 | `scripts/lens_geometry.py` | `891ac67f8b6c1b4c7978b5e806800ae74f5c8791928d6ece19a29e5f3b212b77` | 새로 봉인 (σ — 위 ⚠) |
@@ -178,6 +179,13 @@
   10-07 재등록: `scripts/lhs_design_dataset.py` `27c9c1a8a680945c5ba60e6717e1d77438a489549a62eb24bddb65223c0a8b29` (`5dde71dcc` — selftest 기대 표지 한 줄 · 값 경로 무변경) ·
   `scripts/g2_network_reread.py` `23a949dfe6aa09d277e0626c2c3a6db3e199de8a42872b375b4e75ae828c467b` (`5dde71dcc` K7 · `17ba65f4e` 등록 집합).
   ⚠ v1.3 의 새 열 · 표 (CLAUDE.md 10-06 밤 목록 — ML 표 · f 타깃 안내 · 재적합 · τ 표시 이름 · `se_isolated_pct`) 가 생성기를 바꾸면 이 지문이 바뀐다 → 그 커밋을 §9 에 적는다.
+- ✅ **활성 봉인 (⬜(날짜) 1저자 비준 · §9-8 L214 개정 · 결과 열람 뒤 정책 개정 = 10-14 실행 결과를 본 뒤 · 변경 이력 §9-9)** — 봉인 32 (목록 그대로) · **`code_fp 2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb`** (실행기 `code_fp(code_hashes())`) = 위 표 28 행 그대로 + 바뀐 4 행:
+  `scripts/network_conductivity.py` `a525e2db98fd044f0aa9353b028a3d5c7164c006a8e870dda24e7a0991d9751e` · `scripts/tau_flux.py` `c0a7da6e1b73bea97136f06803810dbe159bf5c4395d8d218a90217a58ef0f78` ·
+  `webapp/app.py` `3e82140f47c7e87b138f8a6f24b8f8575bc7476e91b8369b20cdf698b69b4bc1` · `webapp/pipeline_service.py` `8026169f61e8bddcceea3dfb42758bb6a4e599a28271d8159c387dfc2a79d4ef`.
+  인계 도구 (HANDOVER_FILES · 봉인 판정 밖 · 발사 manifest `handover_code_hashes` 에 기록) `scripts/lhs_design_dataset.py` `d1815155142e909200053c2d8e9de8c0a88c2dc6d3d9462ad18614a42845e1f0` · `scripts/g2_network_reread.py` `0e2ec7ef37571268b85b0d17b71f7a2858aa2a7e6bcfadf4be1c6b5416dd5cd8` ·
+  배포 빌더 `scripts/lhs_release_build.py` `3096e33fd0f1953363bcde251a77368366a0568c923447111a48a873ad4a1383` (빌드 manifest `code` 칸).
+  발사 커밋 = B7 승인 핀 (이 비준 문안이 들어간 push 된 본 가지 커밋 · 1저자가 고른 한 SHA · §9-8 ⑦) — 그 체크아웃의 194 dry-run 이 같은 code_fp 를 찍어야.  10-07 재등록 지문 `e8b2496b…` · 위 표 4 행의 옛 값 = 역사 (§9-9).
+  사전 점검 화면 기대 (이 지문의 코드 · 결과 전): 기대 망 세대 `g2` · 계약 문제 0 · 모드 hertz · physics · hertz_h12 · 전이 닫힘 30 ⊆ 32 ✓ · 지연 import 분류 92 · 분류 밖 0 ✓ (10-07 의 90 + `webapp/pipeline_service.py` 의 `channel_verdict` · `_stop_num` 안 `tau_flux` import 둘 — 대상 = 봉인 파일) · fork 0 줄 ✓ · 입력 지문 = §2 표 그대로.
 
 ## 3b. 실행 형식 v3 (10-07 재등록 · G2RR2-01 · 02 · 판정문 §2 · §3)
 
@@ -270,6 +278,8 @@
 
 ## 5. 판정 · 관문 (결과 전 등록)
 
+> ✅ **⬜(날짜) 1저자 비준 (§9-9)** — 이 절의 활성 개정 = §9-8 ①–⑦ (§5-1 모형 한계 = 레코드 게시 가능 · 결과 자격 ①–③ · 공란 의미 ④ · Hertz 주 타깃 ⑤ · 결과 보고 ⑥ · 발사 ⑦ · §5-7 허용 다름 더함) · 아래 원문 1–7 은 그대로 둔다 · 결과 열람 뒤 정책 개정 (10-14 실행 결과를 본 뒤).
+
 1. 케이스마다 `done` / `failed` (+ `failure_kind`) — failed 는 빈칸 + 사유로 싣고 고르지 않는다 (재실행은 봉인 코드 그대로 `retry` 만).
 2. `audit` rc 0 = 실행 형식 자격 current · 기록 전부 SEALED · 레코드 세대 전부 `g2` · 입력 지문 = 발사 기록.  rc 1 · 2 이면 인계하지 않는다.
 3. `g2_network_reread.py --launcher-root <ROOT> --expect-set production194` rc 0 (M0 · M-plan · M-reg · M1 · M2 · M3 기대 194 = 읽음 194 · 같음 · 케이스마다 K1–K7 ·
@@ -362,7 +372,7 @@
   **등록 §2 · §3 손 대조** (Codex 재확인 `docs/reviews/codex_review_supr_fix_reverify_20261014.md` §3 최소 기록 · 1저자 화면의 로그 `INPUT_DIGEST_JSON` 줄 · 코드 줄 ↔ 이 문서 §2 표 · §3 · 확인 = 조정자) — 여섯 칸 전부 등록 = 실측 (글자 그대로):
   n 194 · `missing_raw_sha` [] ✓ · `ids_sha256` `a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf` ✓ · `raw_sha256_table_sha256` `da7c93f9a0887145ff171e381c8608cb79779d96aea5a595a25677dc361ef784` ✓ · 코호트 TSV lhs `32f00daa8394188d1e72531fd7fda1a8b47a9c279be76311ae7f2afa024b2809` ✓ · lhsx `0b85e8589917c9a3936ce29e9f36326993985ddd113ef32353a4ff96d981cb45` ✓ · code_fp `e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` (CODE_FILES 32) ✓.
   ✅ **1저자 발사 승인 10-14** (*"나머지는 다 권고대로"* · *"이거했어"* = 실행) — 핀 `1087a9b2f4a93aa6a3b0debc698a14fffa13488d` · 194 먼저 → 보충 20 · 결과 = 9-3 칸 (완료 뒤 · ⬜).
-- 9-8 **개정 초안 — FULL 모형 한계 범주 (10-15 · L214 · ⬜ 1저자 비준 대기 · 결과 열람 뒤 정책 개정)** — 근거 = Codex LHS214 실패 검토 `docs/reviews/codex_review_lhs214_failures_20261014.md` §3 Q1–Q3 · §4 B6 ·
+- 9-8 **개정 초안 — FULL 모형 한계 범주 (10-15 · L214 · ✅ ⬜(날짜) 1저자 비준 = §9-9 (비준 전 표지: ⬜ 1저자 비준 대기) · 결과 열람 뒤 정책 개정)** — 근거 = Codex LHS214 실패 검토 `docs/reviews/codex_review_lhs214_failures_20261014.md` §3 Q1–Q3 · §4 B6 ·
   수정 계획 `docs/reviews/lhs214_fix_plan_20261014.md` (✅ 1저자 10-14 Q1–Q5 권고대로) · 수정 재확인 요청서 `docs/reviews/codex_lhs214_fix_review_request_20261015.md` · 증거 `docs/reviews/lhs214_fix_evidence_20261015/README.md`.
   ⚠ **이력 (결과 열람 뒤)** — 이 개정은 10-14 실행 결과 (194 = done 186 · 실패 8 `lhsx_051` · `053` · `054` · `060`–`064` · 보충 20 = done 14 · 실패 6 · 14 건 모두 상위 사유 `physics.ionic=fail / solve_failed` ·
   `lhsx_054` 단독 진단 q 1.5370331988867802 > 1.5 — 나머지 13 건 원인 미확정) 를 **본 뒤** 쓴 허용 정책 변경이다 (Codex §3 Q1 — 이름만 바꾸는 수정이 아니다 · 과거에 막혔던 레코드의 게시 · 인계가 가능해진다).
@@ -371,9 +381,9 @@
   **바꾸지 않는 것** (결과에 맞춰 바꾸지 않는다 · Q5 (가)): 문턱 1.5 (원 정밀도 엄격 > · q = 1.5 는 computed) · 수치 허용치 1e−6 (전류 보존 · 내부 잔차) · 풀이 사다리 · G > 0 · 병렬 상한 0 < G ≤ 1.1·Σg ·
   ID 집합 (§2 production194 `ids_sha256` `a04282d7…` · 보충 supp20 `991cf115…`) · 원 입력 (§2 원자료 표 · 코호트 TSV) · 실행 형식 v3 · 관측 필수 · §5-1–6 의 기존 차단 정책 (진짜 수치 실패 · 기하 · 세대 무효 · 잘못된 증서).
 
-  | 자리 | 원문 (보존) | 개정 초안 (⬜ 비준 대기) |
+  | 자리 | 원문 (보존) | 개정 (✅ ⬜(날짜) 비준 · §9-9 — 비준 전 칸 이름: 개정 초안 (⬜ 비준 대기)) |
   |---|---|---|
-  | §3 코드 신원 | 봉인 32 · `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` | 봉인 32 (목록 그대로) · 바뀐 봉인 파일 4 = `scripts/network_conductivity.py` (sha256 `a525e2db98fd044f…`) · `scripts/tau_flux.py` (sha256 `c0a7da6e1b73bea9…`) · `webapp/app.py` (sha256 `3e82140f47c7e87b…`) · `webapp/pipeline_service.py` (sha256 `8026169f61e8bddc…`) ⇒ **`code_fp_pending 2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb`** (대기 지문 — 비준 · 재등록 때 §3 이 이 값으로 바뀌고 이 선언은 지운다 · 그 전 발사 대조 D1 · E2 = 등록 값 그대로 — 194 쪽 = §3 손 대조 · 보충 20 영수증 도구와 같은 규칙 · 실행기 `code_fp(code_hashes())` · ★ 10-19 L214R-R04 반영 값 (10-18 R02 `755325e1…` · R01 `fca3af77…` · 10-16 L214R-09–11 `e76dbe08…` 대체) — L214R 수정 커밋마다 갱신 · 진행 기록 10-19) · 인계 도구 (HANDOVER_FILES · 봉인 판정 밖) `scripts/lhs_design_dataset.py` sha256 `d1815155142e9092…` · `scripts/g2_network_reread.py` `0e2ec7ef37571268…` · 배포 빌더 `scripts/lhs_release_build.py` `3096e33fd0f19533…` (빌드 manifest `code` 칸) · 발사 커밋 = 이 개정과 수정을 담은 본 가지 커밋 (메인 세션이 적는다) — 그 체크아웃의 194 dry-run 이 같은 code_fp 를 찍어야 |
+  | §3 코드 신원 | 봉인 32 · `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` | 봉인 32 (목록 그대로) · 바뀐 봉인 파일 4 = `scripts/network_conductivity.py` (sha256 `a525e2db98fd044f…`) · `scripts/tau_flux.py` (sha256 `c0a7da6e1b73bea9…`) · `webapp/app.py` (sha256 `3e82140f47c7e87b…`) · `webapp/pipeline_service.py` (sha256 `8026169f61e8bddc…`) ⇒ **`2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb`** (✅ 비준 = §3 활성 지문 (§3 끝 ✅ 줄) · 대기 선언 꼴 (`code_fp_pending`) 은 지웠다 — 비준 전 원문: 대기 지문 — 비준 · 재등록 때 §3 이 이 값으로 바뀌고 이 선언은 지운다 · 그 전 발사 대조 D1 · E2 = 등록 값 그대로 — 194 쪽 = §3 손 대조 · 보충 20 영수증 도구와 같은 규칙 · 실행기 `code_fp(code_hashes())` · ★ 10-19 L214R-R04 반영 값 (10-18 R02 `755325e1…` · R01 `fca3af77…` · 10-16 L214R-09–11 `e76dbe08…` 대체) — L214R 수정 커밋마다 갱신 · 진행 기록 10-19) · 인계 도구 (HANDOVER_FILES · 봉인 판정 밖) `scripts/lhs_design_dataset.py` sha256 `d1815155142e9092…` · `scripts/g2_network_reread.py` `0e2ec7ef37571268…` · 배포 빌더 `scripts/lhs_release_build.py` `3096e33fd0f19533…` (빌드 manifest `code` 칸) · 발사 커밋 = 이 개정과 수정을 담은 본 가지 커밋 (메인 세션이 적는다) — 그 체크아웃의 194 dry-run 이 같은 code_fp 를 찍어야 |
   | §5-1 케이스 판정 | done / failed (+ failure_kind) | 그대로 + 아래 ① 범주의 모형 한계는 진짜 실패가 아니므로 레코드 게시 (done) 가능 — 같은 실행의 다른 채널 · 가지에 진짜 실패가 있으면 failed 그대로 |
   | §5 결과 자격 (신설 ①–③) | — | 범주 · 공용 판정 · 예외 범위 · 우선순위 |
   | §5 공란 의미 (신설 ④) | — | τ NOT_COMPUTED + 사유 정확히 `full_over_conduction` · 배포 빈칸 코드 `NA_MODEL_LIMIT` |
@@ -393,3 +403,7 @@
      Physics · H12 · 0 · 1.5 대체 금지 · 행 삭제 금지 · 주 타깃 결측을 허용하는 마스크 부분 배포 = 별도 등록 · 1저자 결정 · 집계 · 학습 규약.  Physics · H12 만 모형 한계 = 레코드 게시 · 부록 공란.
   ⑥ **결과 보고 (C9)** — Hertz 주 타깃 가용 수와 Physics 모형 한계 수를 따로 (배포 README 상태 집계 = 모형 한계 별도 줄 · 재적합 제외 사유 `NOT_COMPUTED:full_over_conduction`) · 입력 영수증 ≠ 결과 완료 증서.
   ⑦ **발사 (B7)** — 새 code_fp 하나로 두 새 ROOT (194 · 보충 20) · fast16 · real4 · 전체 사전 점검 로그 + 완료 영수증 · §2 손 대조 · 1저자 발사 승인 · 10-14 ROOT 는 지우지 않는다.  ⚠ 이 초안은 등록 기대의 개정안이다 — 비준 · 발사 승인을 대신하지 않는다 · S3 = 별개 (봉인 수치 모듈 둘이 바뀜 → S3 재봉인 의무 · S3 HOLD 그대로).
+- 9-9 **비준 · 변경 이력 (✅ ⬜(날짜) 1저자 비준 · L214 개정 §9-8 · 결과 열람 뒤 정책 개정 — 10-14 실행 결과 (194 done 186 · 실패 8 · 보충 20 done 14 · 실패 6) 를 본 뒤)** — 대화 원문 ⬜ · 비준 커밋 = 이 줄을 담은 커밋 (메인 세션).
+  바뀐 자리 (원문 보존 · 비준 표지 · 기계 구문만 고침): ① §3 활성 봉인 지문 — 10-07 재등록 `e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` → `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` (§3 끝 ✅ 줄 · 옛 두 줄의 `code_fp` 기계 구문을 떼고 값은 그대로) · ② §3 표의 4 행 = 역사 (옛 값 = 표에 전체 그대로 · 새 값 = §3 끝 ✅ 줄) · ③ §9-8 대기 선언 (`code_fp_pending` 꼴) 삭제 · 머리 · 표 머리 비준 표지 · ④ §5 = §9-8 ①–⑦ 활성 (§5 머리 표지).
+  바꾸지 않은 것 = §9-8 '바꾸지 않는 것' 그대로 (문턱 1.5 · 허용치 1e−6 · 사다리 · G > 0 · 병렬 상한 · ID 집합 · 원 입력 · 실행 형식 v3 · 관측 필수 · §5-1–6 기존 차단) · §2 표 · 10-14 ROOT · 실패 기록 (보존 · 사후 성공 전환 없음).
+  ⛔ 비준은 등록 기대의 비준이다 — 발사 승인 아님 (§9-8 ⑦ B7 · 새 승인 핀 · 새 ROOT 둘 · 사전 점검 · 1저자 별도 승인) · S3 = 별개 HOLD (S3 수치 모듈 `scripts/network_conductivity.py` 가 바뀜 → S3 재봉인 의무) · v1.3 주 타깃 = H0 모형 한계 HOLD 그대로.
````

### 1-5. diff — 보충 20 등록

````diff
--- a/docs/reviews/lhs_network_batch_registration_20261012_supp20.md
+++ b/docs/reviews/lhs_network_batch_registration_20261012_supp20.md
@@ -6,6 +6,7 @@
 > 기준 = 194 등록 `docs/reviews/lhs_network_batch_registration_20261007_g2.md` (같은 봉인 32 · 같은 실행 형식 v3 · 같은 관문) — 이 문서는 **다른 점만** 적는다.
 > ⛔ 발사 = 짧은 Codex 검토 GO + 1저자 발사 승인 뒤.  Codex 재검증 7 (`docs/reviews/codex_review_gen2_network_reverify7_20261012.md`) 의 GO 는 핀 `3cedd40a5` 의 기존 194 에 한정 —
 > 보충 지원 코드를 합친 핀으로 발사하면 그 GO 를 이 diff 까지 승인한 것으로 쓰지 않는다.
+> ★★ **✅ ⬜(날짜) 1저자 비준 — L214 개정 (§9-3 = 194 등록 §9-8 과 같은 개정 · 결과 열람 뒤 정책 개정 = 10-14 실행 결과를 본 뒤) · 변경 이력 = §9-4** — §3 활성 봉인 지문 = `2149f873…` (대기 선언 삭제 · 10-12 등록 `e8b2496b…` = 역사 · §9-3 표 원문 칸) · ⛔ 비준은 발사 승인이 아니다 (B7).
 
 ## 0. 순서
 
@@ -39,9 +40,10 @@
 
 ## 3. 코드 신원
 
-- 봉인 32 · **`code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71`** = 194 와 같다 — 보충 지원 변경 (실행기 · 다시 읽기 · 배포 생성기 · 설계 어댑터) 은 봉인 밖.
+- 봉인 32 · **`code_fp 2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb`** = 194 와 같다 (✅ ⬜(날짜) 1저자 비준 · §9-3 · §9-4 — 10-12 등록 값 `e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` 은 역사 · §9-3 표 원문 칸) — 보충 지원 변경 (실행기 · 다시 읽기 · 배포 생성기 · 설계 어댑터) 은 봉인 밖.
 - 인계 도구 지문 (`HANDOVER_FILES`) = 발사 핀에서 다시 기록 — `scripts/g2_network_reread.py` 는 재검증 7 핀의 `248ee5c0…` 에서 바뀌었다 (보충 시험 · 문구).
   봉인 32 불변과 섞지 않는다 · 옛 실행 로그를 새 도구의 증거로 옮기지 않는다 (재검증 7 한정 그대로).
+- ✅ ⬜(날짜) 비준 판 인계 도구 · 배포 빌더 지문 = 194 등록 §3 끝 ✅ 줄 (같은 발사 핀 · 두 배치 공통 · 발사 manifest `handover_code_hashes`).
 - 기대 망 세대 = `g2` (봉인 생산자에서 유도) · **import 관측 필수** (실행기 `PRODUCTION_SETS` — 보충 계획인데 `--observe-imports` 가 없으면 사전 점검 ⛔ · audit 문제).
 
 ## 4. 발사 (짧은 Codex 검토 GO + 1저자 발사 승인 뒤)
@@ -71,6 +73,8 @@
 
 ## 5. 판정 · 관문 (배치마다 · 결과 전 등록)
 
+> ✅ **⬜(날짜) 1저자 비준 (§9-4)** — 이 절의 활성 개정 = §9-3 (194 등록 §9-8 ①–⑦ 을 배치마다 · lhss 행도 같은 범주 · 같은 공용 판정 · lhss 주 타깃 (H0) 모형 한계 = v1.3 주 타깃 배포 HOLD) · 아래 원문 1–5 는 그대로 · 결과 열람 뒤 정책 개정 (10-14 실행 결과를 본 뒤).
+
 1. 케이스 `done` / `failed` (+ `failure_kind`) — failed 는 빈칸 + 사유 · 재실행은 봉인 코드 그대로 `retry` 만 (194 등록 §5-1).
 2. `audit` rc 0 (이 ROOT) — 실행 형식 current · 기록 전부 SEALED · 레코드 세대 `g2` · 입력 지문 = 발사 기록 · import 관측 문제 0 · 단계 결합 expected = observed.
 3. `g2_network_reread.py --launcher-root <ROOT> --expect-set supp20` rc 0 (M-reg · M1 · M2 · M3 기대 20 = 읽음 20 · 케이스마다 K1–K7 · 코호트 H1).
@@ -93,17 +97,21 @@
 
 - 9-1 **사전 점검 (발사 핀 `1087a9b2f` · WSL 10-14 14:19 KST · 1저자)**: dry-run (`--cohorts lhss --dry-run --observe-imports --preflight-receipt`) rc 0 · 영수증 도구 (`--preflight-receipt … --approved-sha 1087a9b2f4a93aa6a3b0debc698a14fffa13488d`) rc 0 · 24 칸 · 다름 0 (R0 · A1–A2 · B1–B3 · C1–C4 · D1 · P0–P10 · E1 · E2) · 입력 지문 n 20 · `ids_sha256` `991cf1150b183f64bc69926a8b3e7c05453ec47e13b89ba3a6ad2fd2c981c694` · `raw_sha256_table_sha256` `a7aaa3c8c7683f1835a096acb83ecdb055eaf5f129221f7067c5f34462807d0e` · 코호트 lhss `69d3f913072288b1d6b8ca8a14e43b0bc8f80e8836a8f79a9b26b2d8ed6dcaf7` = §2 (E1 기계 대조) · code_fp `e8b2496b…` = §3 (E2) · 로그 sha256 `a8dba071bc00aadd…` (4,375 B) · 영수증 `~/netsupp20_1087a9b2f_preflight_1014_141953` (.json · .log) · 수동 칸 셋 (발사 핀 fast16 + real4 · 저자 승인 · 새 ROOT 둘) = 194 등록 §9-7 과 아래 9-2.
 - 9-2 ✅ **1저자 발사 승인 10-14** (194 등록 §9-7 과 같은 승인 · 같은 핀) — 194 끝난 뒤 보충 20 · 결과 = 완료 뒤 (⬜).
-- 9-3 **개정 초안 — FULL 모형 한계 범주 (10-15 · L214 · ⬜ 1저자 비준 대기 · 결과 열람 뒤 정책 개정)** — 194 등록 `docs/reviews/lhs_network_batch_registration_20261007_g2.md` §9-8 과 **같은 개정** (①–⑦ 그대로) ·
+- 9-3 **개정 초안 — FULL 모형 한계 범주 (10-15 · L214 · ✅ ⬜(날짜) 1저자 비준 = §9-4 (비준 전 표지: ⬜ 1저자 비준 대기) · 결과 열람 뒤 정책 개정)** — 194 등록 `docs/reviews/lhs_network_batch_registration_20261007_g2.md` §9-8 과 **같은 개정** (①–⑦ 그대로) ·
   근거 = Codex LHS214 실패 검토 `docs/reviews/codex_review_lhs214_failures_20261014.md` §4 B6 · 수정 계획 `docs/reviews/lhs214_fix_plan_20261014.md` · 수정 재확인 요청서 `docs/reviews/codex_lhs214_fix_review_request_20261015.md`.
   ⚠ **이력 (결과 열람 뒤)** — 10-14 보충 20 실행 결과 (done 14 · 실패 6 = `lhss_001` · `lhss_003` · `lhss_008` · `lhss_009` · `lhss_011` · `lhss_014` · 상위 사유 모두 `physics.ionic=fail / solve_failed` · 원인 미확정 = unknown) 를 본 뒤의 허용 정책 변경 ·
   10-14 ROOT (`~/netsupp20_1087a9b2f`) · 실패 기록 보존 · 사후 "성공" 전환 없음 · 기대 실패 수 고정 없음.
   **바꾸지 않는 것**: 문턱 1.5 · 수치 허용치 1e−6 · 사다리 · G > 0 · 병렬 상한 · 등록 집합 supp20 (`ids_sha256` `991cf115…` · 원자료 표 `a7aaa3c8…` · 코호트 TSV `69d3f913…` — §2 그대로) · 실행 형식 · 관측 필수 · §5 기존 관문.
 
-  | 자리 | 원문 (보존) | 개정 초안 (⬜ 비준 대기) |
+  | 자리 | 원문 (보존) | 개정 (✅ ⬜(날짜) 비준 · §9-4 — 비준 전 칸 이름: 개정 초안 (⬜ 비준 대기)) |
   |---|---|---|
-  | §3 코드 신원 | 봉인 32 · `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` = 194 와 같음 | 봉인 32 · **`code_fp_pending 2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb`** (대기 지문 — 비준 · 재등록 때 §3 이 이 값으로 바뀌고 이 선언은 지운다 · 그 전 발사 대조 D1 · E2 = 등록 값 그대로) = 194 개정과 같음 (한 code_fp 로 두 새 ROOT · 바뀐 봉인 파일 4 · 인계 도구 지문 = 194 등록 §9-8 표) |
+  | §3 코드 신원 | 봉인 32 · `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` = 194 와 같음 | 봉인 32 · **`2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb`** (✅ 비준 = §3 활성 지문 · 대기 선언 꼴 (`code_fp_pending`) 은 지웠다 — 비준 전 원문: 대기 지문 — 비준 · 재등록 때 §3 이 이 값으로 바뀌고 이 선언은 지운다 · 그 전 발사 대조 D1 · E2 = 등록 값 그대로) = 194 개정과 같음 (한 code_fp 로 두 새 ROOT · 바뀐 봉인 파일 4 · 인계 도구 지문 = 194 등록 §9-8 표) |
   | §5-1 케이스 판정 | 194 등록 §5-1 | 194 등록 §9-8 의 §5-1 개정 그대로 (모형 한계 = 레코드 게시 가능 · 다른 채널 진짜 실패 = failed) |
   | §5 결과 자격 · 공란 의미 · Hertz 주 타깃 (신설) | — | 194 등록 §9-8 ①–⑥ 을 **배치마다** — 보충 lhss 행도 같은 범주 · 같은 공용 판정 · lhss 의 주 타깃 (H0) 모형 한계 = v1.3 주 타깃 배포 HOLD (보충 행이라 면제되지 않는다 · `v13_primary_model_limit_problems` 가 데이터셋 lhs · lhsx · lhss 마다) · Physics · H12 만 = 부록 공란 (`NA_MODEL_LIMIT`) |
   | §5-5 배포 관문 | 두 배치 각각 ⓪ · ⓪b + 교차 + 결합 | 그대로 + 결합 뒤 주 타깃 모형 한계 관문 (빌드 · 대조 같은 함수) · 한 배치의 PASS 가 다른 배치를 면제하지 않는다 (그대로) |
 
   ⚠ 이 초안은 등록 기대의 개정안이다 — 비준 · 발사 승인 (B7 — 새 핀 사전 점검 · 영수증 · 손 대조) 을 대신하지 않는다.
+- 9-4 **비준 · 변경 이력 (✅ ⬜(날짜) 1저자 비준 · L214 개정 §9-3 · 결과 열람 뒤 정책 개정 — 10-14 실행 결과 (done 14 · 실패 6) 를 본 뒤)** — 194 등록 §9-9 와 같은 비준 · 대화 원문 ⬜.
+  바뀐 자리: ① §3 활성 봉인 지문 `e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` → `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` (§3 줄 안 값만 · 옛 값은 그 줄과 §9-3 표 원문 칸에 보존 — 영수증 도구 `registration_values` 는 활성 §3 의 기계 구문만 읽는다 · L214R-04) · ② §9-3 대기 선언 (`code_fp_pending` 꼴) 삭제 · 머리 · 표 머리 비준 표지 · ③ §5 = §9-3 활성 (§5 머리 표지) · ④ §3 에 비준 판 인계 도구 · 배포 빌더 지문 자리 (194 등록 §3 끝 ✅ 줄).
+  바꾸지 않은 것 = §9-3 '바꾸지 않는 것' 그대로 (§2 표 · 등록 집합 supp20 · 문턱 · 허용치 · 관측 필수) · 10-14 ROOT (`~/netsupp20_1087a9b2f`) · 실패 기록 보존 · 사후 성공 전환 없음.
+  ⛔ 비준은 발사 승인이 아니다 (B7 — 새 승인 핀 사전 점검 · 영수증 · 손 대조 · 1저자 별도 발사 승인).
````

### 1-6. 비준 커밋 절차 (메인 · 권고)

1. 두 diff 의 `⬜(날짜)` → 비준 날짜 · §9-9 · §9-4 의 *대화 원문 ⬜* → 1저자 원문.
2. (Q3 = (가) 이면) 영수증 도구 `S0b` 기대 변경 = **따로 먼저** (시험 먼저 꼴 — 비준 사본에서 실패 재현 → 기대를 상태별로 → 지금 문서 122/122 · 비준 사본 122/122).  ⚠ 정정 10-21 (메인 · 수정 커밋 `fe23f2b83`): 수정이 새 검사 S11g 하나를 더해 실제 = **지금 문서 123/123 · 비준 사본 123/123** (고치기 전 비준 사본 121/122 · 증거 `docs/reviews/lhs214_relaunch_s0b_evidence_20261021/`).
3. `git apply` 두 diff → 아래 넷 → 커밋 → push → 그 SHA = B7 승인 핀 후보 (§3 · Q4).

```bash
python3 -c "import sys; sys.path.insert(0, 'scripts'); import run_network_194_parallel as N; print(N.code_fp(N.code_hashes()))"     # 2149f8738bb2…c3eb
python3 -c "import sys; sys.path.insert(0, 'scripts'); import supp20_input_receipt as S; v, p = S.registration_values(); print(v['code_fp'], v['code_fp_pending'], p)"   # 2149f873… None []
python3 scripts/supp20_input_receipt.py | tail -1               # rc 0 — 대조 11 칸 · 다름 0
python3 scripts/supp20_input_receipt.py --selftest | tail -1    # Q3 처리 뒤 123/123 PASS (정정 10-21 — S11g 하나 더함 · 옛 기대 122/122)
```

## 2. ② 재결합 표 (발사 핀에 묶을 지문 — 등록 값 ↔ 계산 트리)

전체 값 = 부록 A · §1 diff 의 ✅ 줄.  *같음* = 전체 값 비교 (단, §9-8 이 접두 16 자리만 적은 칸 = 접두 비교라고 적었다).

| # | 항목 | 등록 값 (자리) | 계산 트리 (저장소 함수) | 판정 | 다르면 이유 · 들어갈 자리 |
|---|---|---|---|---|---|
| 1 | 봉인 32 `code_fp` | 194 §3 · 보충 §3 활성 `e8b2496b…` · §9-8 / §9-3 대기 `2149f873…` | `code_fp(code_hashes())` = `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` | 활성 §3 과 **다름** · 대기 값과 같음 (64 자리) | 봉인 4 파일 수정 (L214 · L214R · WEB-09) → §1 diff (§3 활성 · 대기 선언 삭제) |
| 2 | 봉인 32 파일별 | 194 §3 표 32 행 (`code_fp(표)` = `e8b2496b…` = 등록 §3 — 표 자기 일관) | `code_hashes()` | 28 같음 · 4 다름 | 4 = `scripts/network_conductivity.py` (`6d0bec3c3` · `3676a33eb` · `2e85d08eb`) · `scripts/tau_flux.py` (`6d0bec3c3` · `2450cb858` · `530ddb355` · `2e85d08eb` · `60ba39e22` · `91e732517` · `155534744`) · `webapp/app.py` (`6d0bec3c3` · `2fc138274` · `dcd06869d` · `43223d823`) · `webapp/pipeline_service.py` (`6d0bec3c3` · `60ba39e22`) — 새 sha256 = §9-8 접두 16 자리와 4/4 같음 · 전체 = §1 ✅ 줄 · 10-14 핀 `1087a9b2f` 이후 나머지 28 파일 변화 0 |
| 3 | 기대 망 세대 | `g2` · 계약 문제 0 · 모드 셋 (194 §3 · §1 단계 2) | `derive_generation` (`python -I -B` 하위 프로세스) = `g2` · 문제 [] · 모드 hertz · physics · hertz_h12 · 오류 '' | 같음 | — |
| 4 | 전이 의존 닫힘 | 30 ⊆ 32 | `code_dependency_closure` 30 · 밖 [] · 오류 [] | 같음 | — |
| 5 | 지연 import 분류 | 90 · 분류 밖 0 | `lazy_import_census` 92 · 분류 밖 [] · 낡은 항목 [] | **수 다름** · 분류 밖 0 같음 | +2 = `webapp/pipeline_service.py` 의 `channel_verdict` (`6d0bec3c3` · L214-01/02) · `_stop_num` (`60ba39e22` · L214R-11) 안 `tau_flux` import — 대상 = 봉인 파일 · 사전 점검 판정 (분류 밖 0) 무영향 · 새 기대 = §1 ✅ 줄 |
| 6 | fork · 프로세스 풀 API | 0 줄 | `fork_census` [] | 같음 | — |
| 7 | production194 ID 집합 | 194 · `a04282d7…` (§2 · 실행기 `REGISTERED_ID_SETS`) | `registered_id_set('production194')` 194 · `a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf` | 같음 | — |
| 8 | production194 입력 지문 | §2 표: n 194 · raw `da7c93f9…` · 결손 [] · lhs `32f00daa…` · lhsx `0b85e858…` | `plan_input_digest(build_plan(['lhs', 'lhsx']))` 다섯 키 전부 같음 · 계획 = 등록 생산 집합 production194 | 같음 | WSL 로그와는 손 대조 (§4 단계 5 · §5) — 실행기는 등록 값을 모른다 |
| 9 | supp20 ID 집합 | 20 · `991cf115…` | `registered_id_set('supp20')` 20 · `991cf1150b183f64bc69926a8b3e7c05453ec47e13b89ba3a6ad2fd2c981c694` | 같음 | — |
| 10 | supp20 입력 지문 | §2: raw `a7aaa3c8…` · 코호트 TSV `69d3f913…` · 결손 [] | `plan_input_digest(build_plan(['lhss']))` 같음 · 계획 = supp20 | 같음 | WSL 에서는 영수증 도구 E1 이 기계 대조 |
| 11 | supp20 설계 · 어댑터 CSV | §2 `73d9a47f…` · `df505b79…` | `sha256_file` 같음 | 같음 | — |
| 12 | supp20 묶음 (r3 · r2 · harvest_head · 반입 바이트 · r2↔r3 키) | README · §2 | `receipt()` 컨테이너 C1–C4 ✓ | 같음 | — |
| 13 | 원 dump (원자료 자체) | 수확 JSON `raw.*.sha256` (#8 · #10 의 raw 표 지문) | 이 트리 = 표 지문까지 (원자료는 WSL 에만) | — | WSL 대조 = 사전 점검 *원자료 · 메시 문제 0 건* (P8) + 발사 때 워커 같은 프레임 관문 (다르면 그 케이스 REFUSED) |
| 14 | 인계 도구 `scripts/lhs_design_dataset.py` | §3 10-07 `27c9c1a8…` · §9-8 `d1815155142e9092…` | `d1815155142e909200053c2d8e9de8c0a88c2dc6d3d9462ad18614a42845e1f0` | §9-8 과 같음 (접두) · §3 10-07 과 다름 | 10-07 값 → 10-14 핀 `ed8944dc…` (2 커밋) → 지금 (`6d0bec3c3` · `2450cb858`) — 봉인 판정 밖 · 발사 manifest `handover_code_hashes` · F6 대조 · 전체 값 = §1 ✅ 줄 |
| 15 | 인계 도구 `scripts/g2_network_reread.py` | §3 10-07 `23a949df…` · §9-8 `0e2ec7ef37571268…` | `0e2ec7ef37571268b85b0d17b71f7a2858aa2a7e6bcfadf4be1c6b5416dd5cd8` | §9-8 과 같음 (접두) · §3 10-07 과 다름 | 10-07 값 → 10-14 핀 `1487ea01…` (8 커밋) → 지금 (`6d0bec3c3`) — 같은 처리 |
| 16 | 배포 빌더 `scripts/lhs_release_build.py` | §9-8 `3096e33fd0f19533…` (빌드 manifest `code` 칸) | `3096e33fd0f1953363bcde251a77368366a0568c923447111a48a873ad4a1383` | 같음 (접두) | 10-14 핀 `729db1fa…` → 지금 (`6d0bec3c3` · `2450cb858`) · 전체 값 = §1 ✅ 줄 |
| 17 | 실행기 `scripts/run_network_194_parallel.py` | 등록 값 없음 — 영수증 `runner.sha256` = 기록 전용 | `f4048aca55b912628278dbdd7b184ac449723736cd3f4f5cdc7eeca31294921a` | (기록) | `1087a9b2f` 이후 무변경 |
| 18 | 영수증 도구 `scripts/supp20_input_receipt.py` | 없음 (영수증 `TOOL_PINS` 기록) | `2c7e0b81dbe81d0518e27c8e1781959b9cc983509a1ce66001028faa3768a2f9` | (기록) | `1087a9b2f` 이후 17 커밋 (L214 (나′) 2 · L214R 14 — S01 · S06 포함 · WEB-09 1) · Q3 이면 또 바뀐다 |
| 19 | 스모크 `scripts/wsl_network_smoke.py` | 없음 | `feb3e84b9c01d2dee28a158fbbd179e57a4c947325181c276d66d2cec1831b11` | (기록) | `1087a9b2f` 이후 무변경 |

## 3. ③ B7 승인 핀

- **정의** — 1저자 비준 문안 (§1 diff · Q3 처리 포함) 이 들어간 본 가지 `claude/stoic-knuth-NObVQ` 의 **push 된 커밋 하나** (40 자리 · ⬜ 1저자 Q4).  그 커밋에서 `code_fp(code_hashes())` = `2149f873…` = 두 등록 §3 활성 값 ·
  인계 도구 · 배포 빌더 = 194 §3 ✅ 줄 · 깨끗한 트리 · 영수증 도구 컨테이너 범위 rc 0 · 영수증 도구 selftest 전부 통과 (Q3 처리 뒤).
- 그 뒤에 문서 커밋이 더 있어도 사전 점검 · 발사는 **그 SHA 로 detached** — 두 완료 영수증의 `git.sha` · 두 발사 manifest 의 `git.sha` · 모든 `--approved-sha` 가 그 한 값.
- 핀을 고르기 전 확인 (메인) = 그 핀에서 부록 A 재현 명령 (A-1 · A-2 · A-11) 을 다시 — 봉인 32 · 인계 도구 · 배포 빌더 바이트가 계산 트리와 다르면 (비준 커밋에 다른 코드가 섞이면) 이 묶음 ② · ③ 을 다시 쓴다.
- 두 manifest 끼리 같다 (H1) 는 것만으로는 승인 증거가 아니다 — 승인 SHA 를 명시해 P10 · F7 · G7 로 대조한다 (판정문 §5 ③).  실제 `run` (본 실행) 은 `--approved-sha` 를 받지 않는다 — 승인 대조 자리 = 사전 점검 영수증 · 발사 뒤 manifest.

| 무엇 | 실리는 자리 (file:line · 계산 트리) | 대조 |
|---|---|---|
| 사전 점검 git 기록 | `scripts/run_network_194_parallel.py:1767` (preflight `git_info()`) → 영수증 `git` `:2758` · 화면 코드 줄 `:1849–1851` | P7 `:2042–2051` — dirty False · 40 자리 · 로그 짧은 sha 접두 · code_fp 로그 = 영수증 = 이 체크아웃 · CODE_FILES 32 |
| 194 승인 SHA | `preflight-verify --approved-sha` `:3196` → `cmd_preflight_verify` `:2820–2822` → P10 `:2077–2085` | 영수증 git.sha (접두) · 로그 짧은 sha — 빼면 경고만 (실패 아님 · 1저자 10-14 Q3) → ④ 명령에는 늘 넣는다 |
| 보충 승인 SHA (사전 점검) | `scripts/supp20_input_receipt.py:1413` → `receipt()` `:468` (`NP.preflight_receipt_checks(…, approved_sha=…)`) | 같은 P10 + E2 `:320` (code_fp = 등록 §3) · D1 `:455–456` |
| 발사 manifest | `run_network_194_parallel.py:2684` (`git=pf['git']`) · `:2686` (`handover_code_hashes`) · `:2687–2688` (`seal.code_fp`) | 영수증 도구 `--manifest` (F) · `--primary-manifest` (G) `:332–362`: F5 · G5 `:351` (봉인 = 등록 §3 · dirty false) · F6 `:355` (인계 도구 = 이 체크아웃) · F7 · G7 `:357–361` (git.sha = 승인 SHA) · H1 `:484–489` (두 ROOT 다름 · 같은 git.sha · 같은 봉인) |
| `runner.sha256` | `run_network_194_parallel.py:2753` | 대조 없음 = 기록 전용 (SUPR 판정 §2 한정 2) |
| 194 등록 §2 값 | 실행기는 등록 값을 모른다 | 손 대조 (SUPR §3 · 1저자 10-14 · 자동 대조 = v1.3 뒤) — §4 단계 5 · §5 표 |

## 4. ④ WSL 명령 블록 (1저자 · `~/dem-audit` · 단계마다 붙여 넣고 화면을 본다)

```bash
# ── 0. 체크아웃 = B7 승인 핀 (detached · 깨끗한 트리) · 변수 ──
cd ~/dem-audit
git fetch origin claude/stoic-knuth-NObVQ
PIN=⬜                                    # ⬜ 1저자 — B7 승인 핀 40 자리 (§3 · Q4)
git checkout --detach "$PIN" && git log -1 --oneline
[ "$(git rev-parse HEAD)" = "$PIN" ] && echo "핀 일치" || echo "⛔ 핀 다름 — 여기서 멈춘다"
echo "dirty 줄 수 = $(git status --porcelain --untracked-files=no | wc -l) (0 이어야)"
PY=$(ls ~/Yonghoon-DEM-DFT/venv/bin/python ~/Yonghoon-DEM-DFT/.venv/bin/python3 2>/dev/null | head -1); echo "PY=$PY"
S=$(git rev-parse --short=9 HEAD); D=$(date +%m%d); T=$(date +%m%d_%H%M%S)
R194=~/net194_${S}_${D}; RS=~/netsupp20_${S}_${D}                       # 새 ROOT 둘 (dry-run 은 ROOT 를 만들지 않는다 · 10-14 ROOT 는 그대로)
PF194="${R194}_preflight_${T}.json"; PFS="${RS}_preflight_${T}.json"     # 완료 영수증 (ROOT 밖 · 새 이름) — 같은 이름 .log = 실행기가 직접 잡은 전체 로그
for r in "$R194" "$RS" "$PF194" "$PFS"; do [ -e "$r" ] && echo "⛔ 이미 있다: $r"; done; echo "ROOT · 영수증 이름 확인 끝"
LOGD=~/lhs_preflight_${S}_${T}; mkdir -p "$LOGD"
DL=/mnt/c/Users/Administrator/Downloads        # 다른 PC 면 /mnt/c/Users/안용훈/Downloads

# ── 1. 관측된 의존성 — 보통 실행과 격리 실행 (-I · 세대 탐침과 같은 꼴) 이 같은 패키지를 보는가 ──
$PY -c "import sys, numpy, scipy, networkx; print('보통', sys.version.split()[0], numpy.__version__, scipy.__version__, networkx.__version__, sys.executable)" | tee "$LOGD/env.txt"
$PY -I -c "import sys, numpy, scipy, networkx; print('격리', sys.version.split()[0], numpy.__version__, scipy.__version__, networkx.__version__, sys.executable)" | tee -a "$LOGD/env.txt"

# ── 2. 도구 자체 시험 (승인 핀 그대로) — fast16 · real4 = 발사 핀 필수 ──
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
$PY scripts/wsl_network_smoke.py --selftest 2>&1 | tee "$LOGD/fast16.log" | tail -2; echo "fast16 rc=${PIPESTATUS[0]}"
$PY scripts/wsl_network_smoke.py --selftest-real 2>&1 | tee "$LOGD/real4.log" | tail -2; echo "real4 rc=${PIPESTATUS[0]}"            # case15 · ~2.5 분
$PY scripts/g2_network_reread.py --selftest 2>&1 | tee "$LOGD/reread_selftest.log" | tail -2; echo "reread rc=${PIPESTATUS[0]}"
$PY scripts/run_network_194_parallel.py --selftest 2>&1 | tee "$LOGD/runner_selftest.log" | tail -2; echo "runner rc=${PIPESTATUS[0]}"   # ~2–3 분
$PY scripts/supp20_input_receipt.py --selftest 2>&1 | tee "$LOGD/receipt_selftest.log" | tail -2; echo "receipt rc=${PIPESTATUS[0]}"
echo "dirty 줄 수 (자체 시험 뒤) = $(git status --porcelain --untracked-files=no | wc -l) (0 이어야 — 아니면 멈추고 그 줄을 붙여 넣는다)"

# ── 3. 194 사전 점검 — 실행기 완료 영수증 + 전체 로그 · 대조 (승인 SHA 포함) ──
$PY scripts/run_network_194_parallel.py run --root "$R194" --dry-run --observe-imports --preflight-receipt "$PF194"; echo "dry-run 194 rc=$?"
$PY scripts/run_network_194_parallel.py preflight-verify --receipt "$PF194" --expect-set production194 --approved-sha "$PIN" --json "${PF194%.json}_verify.json"; echo "verify 194 rc=$?"
grep -E 'INPUT_DIGEST_JSON|코드 |기대 망 세대|전이 의존 닫힘|지연 import 분류|fork · 프로세스 풀 API|원자료 · 메시 문제|⛔' "${PF194%.json}.log"

# ── 4. 보충 20 사전 점검 — 다른 새 ROOT · 같은 핀 · 영수증 도구 (P0–P10 + 등록 §2 · §3 기계 대조 E1 · E2) ──
$PY scripts/run_network_194_parallel.py run --root "$RS" --cohorts lhss --dry-run --observe-imports --preflight-receipt "$PFS"; echo "dry-run supp20 rc=$?"
$PY scripts/supp20_input_receipt.py --preflight-receipt "$PFS" --approved-sha "$PIN" --json "${PFS%.json}_receipt.json"; echo "receipt rc=$?"

# ── 5. 194 등록 §2 · §3 손 대조 재료 (자동 대조 = v1.3 뒤 · 1저자 10-14) — 전체 값 그대로 ──
grep -E 'INPUT_DIGEST_JSON|봉인 지문 code_fp' "${PF194%.json}.log" | tee "$LOGD/handcheck_194_lines.txt"
sha256sum "$PF194" "${PF194%.json}.log" "$PFS" "${PFS%.json}.log" | tee "$LOGD/receipts_sha256.txt"

# ── 6. 묶음 → 다운로드 폴더 (대화에 첨부) ──
cp "$PF194" "${PF194%.json}.log" "${PF194%.json}_verify.json" "$PFS" "${PFS%.json}.log" "${PFS%.json}_receipt.json" "$LOGD/"
git rev-parse HEAD > "$LOGD/head.txt"; git status --porcelain --untracked-files=no > "$LOGD/dirty.txt"
cd ~ && tar czf "lhs_preflight_${S}_${T}.tgz" "$(basename "$LOGD")" && sha256sum "lhs_preflight_${S}_${T}.tgz" && cp "lhs_preflight_${S}_${T}.tgz" "$DL/"; cd ~/dem-audit
```

**붙여 넣을 것** — 0 단계 (핀 일치 · dirty · PY · 이름 확인) · 1 단계 두 줄 · 2 단계 `tail` 과 `rc=` 다섯 + dirty 줄 · 3 단계 `rc=` 둘 + grep 줄 · 4 단계 `rc=` 둘 + 영수증 도구 끝줄 (`rc 0 — 대조 24 칸 · 다름 0`) · 5 단계 출력 · 6 단계 sha256 줄.
**묶음** `lhs_preflight_<S>_<T>.tgz` = `env.txt` · 자체 시험 로그 다섯 · 194 영수증 (.json · .log · `_verify.json`) · 보충 영수증 (.json · .log · `_receipt.json`) · `handcheck_194_lines.txt` · `receipts_sha256.txt` · `head.txt` · `dirty.txt` — 반입 = 메인 (`docs/reviews/` 아래 새 증거 폴더 · ⬜ 이름) · 묶음 sha256 기록.

**결과 전 기대 (다르면 그대로 보고 · 고르지 않는다)**

| 단계 | 기대 | 근거 |
|---|---|---|
| 0 | 핀 일치 · dirty 0 · 이미 있는 이름 없음 | — |
| 1 | 보통 = 격리 (같은 numpy · scipy · networkx 판 · 같은 실행 파일) | 10-14 = Python 3.12.3 · NumPy 2.5.2 · SciPy 1.18.1 · networkx 3.7 (194 §9-7) · 격리 자식이 scipy 를 못 찾으면 세대 탐침이 실패 → 사전 점검 P3 · P8 실패 (Codex 10-20 §3-3) |
| 2 | 다섯 rc 0 · 수 = 화면 그대로 — fast16 16/16 · real4 4/4 · 실행기 139/139 (마지막 기록 = 10-15 LHS214 수정 요청서 `docs/reviews/codex_lhs214_fix_review_request_20261015.md` §2 · 실행기 · 스모크 도구는 10-14 핀 뒤 무변경 · 봉인 4 파일은 그 뒤에도 바뀜 → 이 핀 첫 실측) · reread 전부 통과 (`check_all.sh` 상주) · 영수증 123/123 (**Q3 처리 뒤** — 정정 10-21: 수정이 S11g 하나를 더함 · 옛 기대 122/122 · 처리 없이 비준만이면 121/122 · `S0b`) · dirty 0 | §1-3 · 부록 A-13 |
| 3 | dry-run rc 0 · 화면: 코드 줄 `dirty=False · 봉인 지문 code_fp 2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb (CODE_FILES 32)` · 기대 망 세대 `'g2'` · 계약 문제 0 · 모드 `['hertz', 'physics', 'hertz_h12']` · 전이 의존 닫힘 30 모듈 ⊆ 32 ✓ · 지연 import 92 · 분류 밖 0 ✓ · fork 0 줄 ✓ · `INPUT_DIGEST_JSON` = 아래 줄 그대로 · 원자료 · 메시 문제 0 건 · ⛔ 없음 / verify rc 0 · 11 칸 (P0–P10) · 다름 0 | §2 #1–#8 |
| 4 | dry-run rc 0 · 영수증 도구 rc 0 · 24 칸 (R0 · A1–A2 · B1–B3 · C1–C4 · D1 · P0–P10 · E1 · E2) · 다름 0 | §2 #9–#12 · 10-14 = 24 칸 (보충 §9-1) |
| 5 | 194 줄 둘 = §5 손 대조 표의 등록 값 | §2 #1 · #8 |
| 6 | tgz 하나 · sha256 한 줄 | — |

`INPUT_DIGEST_JSON` 기대 줄 (실행기 `input_digest_json_line(plan_input_digest(build_plan(…)))` · 계산 트리 — 로그 줄의 앞 공백 두 칸 뒤):

```text
INPUT_DIGEST_JSON {"cohort_tsv_sha256":{"lhs":"32f00daa8394188d1e72531fd7fda1a8b47a9c279be76311ae7f2afa024b2809","lhsx":"0b85e8589917c9a3936ce29e9f36326993985ddd113ef32353a4ff96d981cb45"},"ids_sha256":"a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf","missing_raw_sha":[],"n":194,"raw_sha256_table_sha256":"da7c93f9a0887145ff171e381c8608cb79779d96aea5a595a25677dc361ef784"}
INPUT_DIGEST_JSON {"cohort_tsv_sha256":{"lhss":"69d3f913072288b1d6b8ca8a14e43b0bc8f80e8836a8f79a9b26b2d8ed6dcaf7"},"ids_sha256":"991cf1150b183f64bc69926a8b3e7c05453ec47e13b89ba3a6ad2fd2c981c694","missing_raw_sha":[],"n":20,"raw_sha256_table_sha256":"a7aaa3c8c7683f1835a096acb83ecdb055eaf5f129221f7067c5f34462807d0e"}
```

**⛔ ⑤ 1저자 발사 승인 뒤에만 — 꼴만 (같은 셸 · 위 변수 · 같은 핀 · 194 먼저 → 끝난 뒤 보충 20 · 등록 §4 · 보충 §4 의 본 실행 줄)**

```bash
# ⛔⛔ ⑤ 승인 뒤 — 다른 셸이면 0 단계 변수 줄을 다시 쓰되 R194 · RS · PF194 · PFS 는 사전 점검 때 이름 그대로 (영수증 root 칸)
$PY scripts/run_network_194_parallel.py run --root "$R194" --observe-imports 2>&1 | tee ~/net194_run_$(date +%m%d_%H%M).log | tail -40
grep -oE '"observe_imports": (true|false)' "$R194/manifest.json"; grep -oE '"import_obs_run_id": "[0-9a-f]{32}"' "$R194/manifest.json"
#   … 194 완료 → 194 등록 §4 완료 뒤 확인 (audit · 재시도 예외 확인 명령) → 그 뒤 보충 20
$PY scripts/run_network_194_parallel.py run --root "$RS" --cohorts lhss --observe-imports 2>&1 | tee ~/netsupp20_run_$(date +%m%d_%H%M).log | tail -40
$PY scripts/supp20_input_receipt.py --manifest "$RS/manifest.json" --primary-manifest "$R194/manifest.json" --approved-sha "$PIN" --json ~/launch_receipt_${S}_$(date +%m%d_%H%M).json; echo "launch receipt rc=$?"
```

## 5. ⑤ 1저자 확인표 (발사 승인 전)

| # | 증거 | 통과 조건 | 묶음 자리 |
|---|---|---|---|
| 1 | 승인 핀 | HEAD = PIN (40) · 두 영수증 `git.sha` = PIN · verify P10 ✓ · 영수증 도구 P10 ✓ | `head.txt` · `_verify.json` · `_receipt.json` |
| 2 | 깨끗한 트리 | dirty 0 (체크아웃 뒤 · 자체 시험 뒤) · P7 dirty False (두 영수증) | `dirty.txt` · 화면 |
| 3 | 관측된 의존성 | 보통 = 격리 (판 · 실행 파일) · P5 세 검사 ✓ (닫힘 · 지연 import · fork) · P8 세대 `g2` · 문제 0 · 유도 오류 없음 | `env.txt` · 영수증 |
| 4 | fast16 · real4 | rc 0 · 16/16 · 4/4 | `fast16.log` · `real4.log` |
| 5 | 나머지 자체 시험 | reread · 실행기 · 영수증 rc 0 (수 그대로 기록) | `*_selftest.log` |
| 6 | 194 완료 영수증 | dry-run rc 0 · verify rc 0 · 11 칸 · 다름 0 · 로그 sha256 = 영수증 `log.sha256` (P1) | `.json` · `.log` · `_verify.json` |
| 7 | 보충 완료 영수증 | dry-run rc 0 · 영수증 도구 rc 0 · 24 칸 · 다름 0 | `.json` · `.log` · `_receipt.json` |
| 8 | 194 손 대조 | 아래 표 여섯 칸 — 기대 · 실측 **전체 값** · 일치 · 확인자 (짧은 접두 눈대조 · *"P0–P10 통과"* 로 대신하지 않는다 — SUPR §3) | `handcheck_194_lines.txt` |
| 9 | 새 ROOT 둘 | R194 ≠ RS · 둘 다 없던 이름 · 10-14 ROOT 와 다름 | 0 단계 화면 |
| 10 | Codex 짧은 확인 (Q5 = 예) | GO (발사 확인 범위) | 판정문 ⬜ |

**194 손 대조 표 (사전 점검 뒤 채운다 — 영수증 경로 ⬜ · 로그 sha256 전체 ⬜ · 승인 핀 ⬜ · 확인자 ⬜)**

| 칸 | 등록 값 (전체) | 로그 실측 (전체) | 일치 |
|---|---|---|---|
| n · missing_raw_sha | 194 · [] | ⬜ | ⬜ |
| ids_sha256 | `a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf` | ⬜ | ⬜ |
| raw_sha256_table_sha256 | `da7c93f9a0887145ff171e381c8608cb79779d96aea5a595a25677dc361ef784` | ⬜ | ⬜ |
| cohort_tsv_sha256.lhs | `32f00daa8394188d1e72531fd7fda1a8b47a9c279be76311ae7f2afa024b2809` | ⬜ | ⬜ |
| cohort_tsv_sha256.lhsx | `0b85e8589917c9a3936ce29e9f36326993985ddd113ef32353a4ff96d981cb45` | ⬜ | ⬜ |
| code_fp (CODE_FILES 32 · 비준 뒤 §3) | `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` | ⬜ | ⬜ |

**구 ROOT · 실패 기록 (보존 · 덮지 않는다)**

| 대상 | 처리 |
|---|---|
| 10-14 ROOT `~/net194_1087a9b2f` (done 186 · 실패 8) · `~/netsupp20_1087a9b2f` (done 14 · 실패 6) | 그대로 둔다 — 지우지 · 옮기지 · retry · merge 하지 않는다 (새 실행 = 새 ROOT) |
| 10-14 사전 점검 영수증 `~/net194_1087a9b2f_preflight_1014_141953` · `~/netsupp20_1087a9b2f_preflight_1014_141953` (.json · .log) | 그대로 · 새 영수증 = 새 이름 (실행기가 같은 이름을 거부) |
| 옛 실패 14 건 레코드 (`physics.ionic=fail / solve_failed`) | 역사 — 사후 *"성공"* 전환 없음 · 새 214 실행이 사례마다 다시 판정 · 기대 실패 수 · case ID 허용목록 없음 (194 §9-8 이력 · Q3 (가) unknown) |
| 등록 §9 의 10-14 칸 (194 §9-3 *발사* ⬜ · §9-7 · 보충 §9-1 · §9-2) | 덮지 않는다 — 새 사전 점검 · 발사 기록 = 새 항목 (194 §9-9 · 보충 §9-4 다음) |

## 6. 1저자가 정할 것

| Q | 질문 | 권고 |
|---|---|---|
| Q1 | 194 §9-8 · 보충 §9-3 개정 + 두 §3 활성 지문 `2149f873…` 비준 (문안 = §1-4 · §1-5 diff · 날짜 · 대화 원문만 채움) | 비준 — 비준 사본은 저장소 파서 · 영수증 (rc 0) 으로 확인했다 (§1-3) |
| Q2 | σ₀ 1.5 솔버 상수 (`scripts/se_material.py` = 봉인 32) 를 이번 재봉인에 넣나 | **넣지 않음** — 넣으면 code_fp 가 바뀌어 이 묶음 ① ② ③ · A4 무영향 대조 · Codex 재검토가 다시 (10-12 권고 = 194 · 보충 20 배치 뒤 그대로 · f · 수송 tortuosity 는 σ₀ 에서 약분) |
| Q3 | ⚠ 새 발견 — 비준 문안을 넣으면 영수증 도구 selftest `S0b` 가 실패 (121/122 · 줄 619–623 의 `e8b2496b…` 상수) | **(가)** 비준 커밋 **앞에** 시험 기대만 상태별로 (pending = 등록 `e8b2496b…` + 대기 `2149f873…` · registered = 등록 `2149f873…` + 대기 없음) 바꾸는 작은 코드 커밋 — 봉인 밖 (CODE_FILES · HANDOVER 아님 · 영수증 `TOOL_PINS` 기록 칸만 바뀜) · 시험 먼저 꼴 · Codex 확인에 넣는다.  (나) 문서만 비준 → 사전 점검에 *기대 실패* 로 등록 = 비권고.  이 문서는 코드를 고치지 않았다 |
| Q4 | B7 승인 핀 고르기 | 비준 문안 (+ Q3) 이 들어간 push 된 본 가지 커밋 하나 · 그 SHA 를 §4 `PIN` 에 · 사전 점검 · 발사 = 그 SHA detached |
| Q5 | 다섯 단계 묶음을 Codex 에 한 번 보이나 | **예** — ④ 반입 뒤 짧은 확인 (`docs/reviews/codex_lhs214_relaunch_check_request_20261020.md` · 리뷰 핀 = 사전 점검 반입 커밋 · 코드 = 승인 핀과 같음 · 메인) |

## 부록 A. 사전 공격 리뷰 — 숫자 · 지문 · 전칭 ↔ 명령 출력 (이 컨테이너 · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · networkx 3.6.1 · 10-20 밤)

재현 (리포 뿌리 · 계산 트리 · 읽기 전용 — A-2 ~ A-11 은 한 번에):

```bash
git diff --quiet 34713ac96 HEAD -- $(python3 -c "import sys; sys.path.insert(0, 'scripts'); import run_network_194_parallel as N; print(' '.join(N.CODE_FILES))"); echo "sealed32 rc=$?"
git diff --quiet 34713ac96 HEAD -- scripts/lhs_design_dataset.py scripts/g2_network_reread.py scripts/lhs_release_build.py scripts/run_network_194_parallel.py scripts/supp20_input_receipt.py scripts/wsl_network_smoke.py docs/reviews/lhs_network_batch_registration_20261007_g2.md docs/reviews/lhs_network_batch_registration_20261012_supp20.md; echo "tools+registrations rc=$?"
OMP_NUM_THREADS=1 python3 - <<'PY'
import re, sys, types
sys.path.insert(0, 'scripts')
import run_network_194_parallel as N, supp20_input_receipt as S, seal_s3_prerun as S3
h = N.code_hashes(); t = open('docs/reviews/lhs_network_batch_registration_20261007_g2.md', encoding='utf-8').read()
s3, _ = S._md_section(t, 3, strip_code=True); rows = dict(re.findall(r'^\| `([^`]+\.py)` \| `([0-9a-f]{64})` \|', s3, re.M))
ch = [k for k in N.CODE_FILES if h[k] != rows.get(k)]
print('A-2', N.code_fp(h)); print('A-3', len(rows), sorted(rows) == sorted(N.CODE_FILES), N.code_fp(rows)); print('A-4', ch, {k: h[k][:16] for k in ch})
print('A-5', [m for m in S3.NUMERIC_MODULES if 'scripts/' + m in ch])
g = N.derive_generation(N.ROOT); print('A-6', g['generation'], g['problems'], g['modes'], repr(g['error']))
c = N.code_dependency_closure(); z = N.lazy_import_census(); print('A-7', len(c['files']), [f for f in c['files'] if f not in N.CODE_FILES], len(z['lazy']), z['unclassified'], z['stale'], N.fork_census())
for n in ('production194', 'supp20'):
    r = N.registered_id_set(n); print('A-9', n, len(r['pairs']), N.ids_digest(r['pairs']))
ns = types.SimpleNamespace(**{f'{a}_{b}': '' for a in N.COHORT_SPECS for b in ('harvest', 'cohort')})
for cs in (['lhs', 'lhsx'], ['lhss']):
    p = N.build_plan(cs, N.cohort_specs(ns), (), 'cost'); print('A-10', N.registered_production_set(p), N.input_digest_json_line(N.plan_input_digest(p)))
for f in ('scripts/lhs_design_dataset.py', 'scripts/g2_network_reread.py', 'scripts/lhs_release_build.py', 'scripts/run_network_194_parallel.py', 'scripts/supp20_input_receipt.py', 'scripts/wsl_network_smoke.py'):
    print('A-11', f, N.sha256_file(N.ROOT / f))
PY
```

출력 원문 (위 heredoc 을 이 문서에서 그대로 떼어 돌린 것 · 10-20 밤 · rc 0):

```text
A-2 2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb
A-3 32 True e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71
A-4 ['scripts/network_conductivity.py', 'scripts/tau_flux.py', 'webapp/app.py', 'webapp/pipeline_service.py'] {'scripts/network_conductivity.py': 'a525e2db98fd044f', 'scripts/tau_flux.py': 'c0a7da6e1b73bea9', 'webapp/app.py': '3e82140f47c7e87b', 'webapp/pipeline_service.py': '8026169f61e8bddc'}
A-5 ['network_conductivity.py']
A-6 g2 [] ['hertz', 'physics', 'hertz_h12'] ''
A-7 30 [] 92 [] [] []
A-9 production194 194 a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf
A-9 supp20 20 991cf1150b183f64bc69926a8b3e7c05453ec47e13b89ba3a6ad2fd2c981c694
A-10 production194 INPUT_DIGEST_JSON {"cohort_tsv_sha256":{"lhs":"32f00daa8394188d1e72531fd7fda1a8b47a9c279be76311ae7f2afa024b2809","lhsx":"0b85e8589917c9a3936ce29e9f36326993985ddd113ef32353a4ff96d981cb45"},"ids_sha256":"a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf","missing_raw_sha":[],"n":194,"raw_sha256_table_sha256":"da7c93f9a0887145ff171e381c8608cb79779d96aea5a595a25677dc361ef784"}
A-10 supp20 INPUT_DIGEST_JSON {"cohort_tsv_sha256":{"lhss":"69d3f913072288b1d6b8ca8a14e43b0bc8f80e8836a8f79a9b26b2d8ed6dcaf7"},"ids_sha256":"991cf1150b183f64bc69926a8b3e7c05453ec47e13b89ba3a6ad2fd2c981c694","missing_raw_sha":[],"n":20,"raw_sha256_table_sha256":"a7aaa3c8c7683f1835a096acb83ecdb055eaf5f129221f7067c5f34462807d0e"}
A-11 scripts/lhs_design_dataset.py d1815155142e909200053c2d8e9de8c0a88c2dc6d3d9462ad18614a42845e1f0
A-11 scripts/g2_network_reread.py 0e2ec7ef37571268b85b0d17b71f7a2858aa2a7e6bcfadf4be1c6b5416dd5cd8
A-11 scripts/lhs_release_build.py 3096e33fd0f1953363bcde251a77368366a0568c923447111a48a873ad4a1383
A-11 scripts/run_network_194_parallel.py f4048aca55b912628278dbdd7b184ac449723736cd3f4f5cdc7eeca31294921a
A-11 scripts/supp20_input_receipt.py 2c7e0b81dbe81d0518e27c8e1781959b9cc983509a1ce66001028faa3768a2f9
A-11 scripts/wsl_network_smoke.py feb3e84b9c01d2dee28a158fbbd179e57a4c947325181c276d66d2cec1831b11
```

| # | 주장 (이 문서) | 출력 (요지 · 전체 값은 위 명령) |
|---|---|---|
| A-1 | 봉인 32 · 인계 2 · 배포 빌더 · 실행기 · 영수증 · 스모크 · 두 등록 = `34713ac96` 과 바이트 같음 | `sealed32 rc=0` · `tools+registrations rc=0` |
| A-2 | 계산 트리 code_fp = `2149f873…` (대기 값과 같음) | `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` |
| A-3 | 194 §3 표 = 32 행 = CODE_FILES · 표 지문 = 등록 §3 | `32 True e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` |
| A-4 | 표 대비 다른 파일 = 4 · 새 값 접두 = §9-8 의 16 자리 | `['scripts/network_conductivity.py', 'scripts/tau_flux.py', 'webapp/app.py', 'webapp/pipeline_service.py']` · `a525e2db98fd044f…` · `c0a7da6e1b73bea9…` · `3e82140f47c7e87b…` · `8026169f61e8bddc…` (§9-8 표와 4/4 같음) |
| A-5 | S3 수치 모듈 중 바뀐 것 = network_conductivity 하나 (§9-8 ⑦ *"둘"* = network_conductivity · tau_flux 로 읽힌다 · tau_flux 는 `NUMERIC_MODULES` 밖 — S3 재봉인 의무 결론은 같음) | `['network_conductivity.py']` |
| A-6 | 기대 세대 g2 · 문제 0 · 모드 셋 · 격리 하위 프로세스 성공 | `g2 [] ['hertz', 'physics', 'hertz_h12'] ''` |
| A-7 | 닫힘 30 · 밖 0 · 지연 import 92 · 분류 밖 0 · 낡은 항목 0 · fork 0 | `30 [] 92 [] [] []` |
| A-8 | 지연 import +2 = pipeline_service `channel_verdict` · `_stop_num` → tau_flux (10-14 핀 트리 = 90 · 그 트리 code_fp = `e8b2496b…` · 닫힘 30 · fork 0) | `git archive 1087a9b2f scripts webapp` 의 .py 트리에 같은 함수 — `+ ('webapp/pipeline_service.py', '_stop_num', 'scripts/tau_flux.py', 'tau_flux')` · `+ (…, 'channel_verdict', …)` |
| A-9 | ID 집합 두 개 = 등록 | `production194 194 a04282d7…7b3bf` · `supp20 20 991cf115…1c694` (전체 = §2 #7 · #9) |
| A-10 | 두 계획 = 등록 생산 집합 · 입력 지문 = 등록 §2 (다섯 키 전부) | `production194 INPUT_DIGEST_JSON {…}` · `supp20 INPUT_DIGEST_JSON {…}` = §4 기대 줄 그대로 |
| A-11 | 인계 · 빌더 · 실행기 · 영수증 · 스모크 sha256 | §2 #14–#19 (인계 둘 · 빌더 = §9-8 접두 3/3 같음) |
| A-12 | 보충 영수증 컨테이너: 지금 rc 1 [D1] · 비준 사본 rc 0 [] · 비준 사본 등록 값 `2149f873…` · 대기 None · 문제 0 | `receipt()` · `registration_values(reg_doc=<사본>)` (사본 = §1 diff 적용 · 스크래치) |
| A-13 | 보충 selftest: 지금 122/122 (pending) · 비준 사본 121/122 (registered) · 실패 = `S0b` 하나 | 같은 프로세스에서 `REG_DOC` · `receipt.__kwdefaults__['reg_doc']` · `registration_values.__defaults__` 만 사본으로 바꾼 `_selftest()` — 경로만 바꾼 모의 실행 (도구 · 판정식 무변경) · 이 트리는 성긴 체크아웃이라 S10 증거 `.log` 여덟을 더 받은 뒤 (그 전 117/122 = 파일 없음 · 도구 결함 아님) |
| A-14 | 두 diff 가 계산 트리에 그대로 붙는다 · 194 사본 §3 = 기계 값 하나 · 대기 0 · 표 + ✅ 줄 = 해시 32/32 · ✅ 줄 도구 3/3 | `git apply --check` rc 0 · rc 0 · `_one(…)` = (`2149f873…`, '') · `code_fp(표 + ✅)` = `2149f873…` |
| A-15 | 이 문서가 적은 커밋은 전부 원격 본 가지 조상 | `git merge-base --is-ancestor <sha> origin/claude/stoic-knuth-NObVQ` — `34713ac96` · `1087a9b2f` · `e6f7895d0` · `6d0bec3c3` · `3676a33eb` · `2e85d08eb` · `2450cb858` · `530ddb355` · `60ba39e22` · `2fc138274` · `dcd06869d` · `91e732517` · `43223d823` · `155534744` 전부 rc 0 (이 문서를 담은 커밋 번호는 적지 않는다 — `SELF-116`) |
| A-16 | 10-14 핀 `1087a9b2f` 이후 바뀐 봉인 파일 = 4 (나머지 28 = 0) · 실행기 · 스모크 무변경 · 영수증 17 커밋 | `git diff --name-only 1087a9b2f HEAD -- <28 파일> \| wc -l` = 0 · `git log 1087a9b2f..HEAD -- <파일>` |
| A-17 | 깨진 참조 없음 | `python3 scripts/check_doc_refs.py` → `✓ 깨진 참조 없음` (이 문서 · 요청서 초안을 넣은 트리 · 커밋 전) |

한정: 이 컨테이너는 WSL 이 아니다 — 원자료 (dump) 실재 · fast16 · real4 · 실행기 selftest 는 여기서 돌리지 않았다 (무거운 시험 금지 · 실제 발사 환경 증거 = §4).  A-13 은 모의 실행 (등록 문서 경로만 바꿈) 이다 — 비준 커밋 뒤 실제 selftest 로 다시 잰다 (§1-6).
