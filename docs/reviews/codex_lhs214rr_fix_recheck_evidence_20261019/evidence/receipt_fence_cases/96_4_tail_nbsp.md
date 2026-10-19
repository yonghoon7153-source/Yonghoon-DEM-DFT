# LHS 보충 20 — 세대 2 접촉망 배치 실행 등록 (2026-10-12 · ✅ 1저자 비준 10-12 (§2 재수확 지문을 채운 판 · *"비준이야"*) · 결과 0 건)

> 1저자 10-12 **(나)** — 보충 지원 구현 + 짧은 Codex 검토 먼저 → 194 · 보충 20 **두 배치를 같은 날 연달아** 발사 → v1.3 한 번에.
> Q4 = (가) 세 번째 데이터셋 `lhss` (별도 파일 · 130 · 64 파일 = 열 · 값 그대로) · Q5 = (가) 194 와 같은 수확기 판 `1e09f661d` 로 재수확 + r2 키별 대조
> (`docs/reviews/g2rr6_fix_plan_20261011.md` §2 · §3).
> 기준 = 194 등록 `docs/reviews/lhs_network_batch_registration_20261007_g2.md` (같은 봉인 32 · 같은 실행 형식 v3 · 같은 관문) — 이 문서는 **다른 점만** 적는다.
> ⛔ 발사 = 짧은 Codex 검토 GO + 1저자 발사 승인 뒤.  Codex 재검증 7 (`docs/reviews/codex_review_gen2_network_reverify7_20261012.md`) 의 GO 는 핀 `3cedd40a5` 의 기존 194 에 한정 —
> 보충 지원 코드를 합친 핀으로 발사하면 그 GO 를 이 diff 까지 승인한 것으로 쓰지 않는다.

## 0. 순서

① ✅ WSL 재수확 (`1e09f661d` · 10-12 · 20 / 20) → ✅ 반입 · r2 와 키별 대조 (값 동일 · §2) →
② 설계 어댑터 (lhss 20 → 130 인계 스키마) · lhss 열 구성 (✅ 1저자 10-12 Q6 = (가) lhs 132 열 · volfrac_free 하중 빈칸) → ③ 인계 생성기 · 배포 생성기 214 결합 (시험 먼저) → ④ ✅ 이 등록 비준 (1저자 10-12 · 지문 채운 판) →
⑤ 짧은 Codex 검토 → GO → ⑥ 발사 핀 사전 점검 (fast16 + real4 · 깨끗한 트리 · 새 ROOT 둘 · 194 등록 §1 과 같은 단계) →
⑦ 같은 날 **194 먼저 → 보충 20** (같은 발사 커밋 · 다른 ROOT) → ⑧ 배치마다 §5 관문 → ⑨ v1.3 한 번에 (두 배치 결합 관문).

⚠ **10-12 순서 조정 (1저자)**: ⑤ 짧은 Codex 검토를 ④ 비준보다 먼저 보냈다 (발송 10-12 · 리뷰 핀 `b429c3c1d` · 요청서 `docs/reviews/codex_supp20_support_review_request_20261012.md` — 코드 검토는 §2 지문 값과 무관 · 요청서 Q6).  ④ 비준 = ① 재수확 반입 · r2 키별 대조 뒤 §2 지문을 채운 판 (1저자 10-12 *"지문 채운 뒤"* — 권고대로).  ⑥ 이후는 그대로.

## 2. 대상 · 입력 봉인

- 코호트 `lhss` = `lhss_001` … `lhss_020` (설계 `docs/data/lhs_supp_design_20261006.csv` 28 행 중 20 · sha256 `73d9a47f76f49989ddbd2c1237007c8499601d63bd5baf0e1ad11c527f21beb0`) ·
  후막 `lhst_*` 8 = **집합 밖** (1저자 10-11 — LHS 밖 · 별도 기술 보고).
- 규약 섞임 (설계 실측): **2mAh_fixed 10 행** (AM 77.5–95 wt% · 130 의 2 mAh 규칙) + **volfrac_free 10 행** (SE-rich · 64 확장 규약) · kind bimodal 14 · mono_AM_S 4 · mono_AM_P 2 ·
  `cap_adjust = volfrac` 2 (입자 수 상한 · 등록 `docs/reviews/lhs_supp_thick_registration_20261006.md` §1).
- 등록 집합 **`supp20`** (실행기 `REGISTERED_ID_SETS` · 커밋된 lhss 수확 폴더에서 열거 → 수 · 코호트 · 지문이 같아야 쓴다 — production194 와 같은 규칙):

| 항목 | 값 |
|---|---|
| 케이스 수 | 20 (lhss 20) |
| `ids_sha256` ('case\tcohort' 줄 · (코호트, 케이스) 순 · 실행기 `ids_digest`) | `991cf1150b183f64bc69926a8b3e7c05453ec47e13b89ba3a6ad2fd2c981c694` |
| `raw_sha256_table_sha256` | `a7aaa3c8c7683f1835a096acb83ecdb055eaf5f129221f7067c5f34462807d0e` (10-12 · r3 반입 뒤 실행기 `plan_input_digest` 를 그대로 불러 계산 · 원자료 sha 결손 0 · 발사 핀 dry-run 이 같은 값을 찍어야) |
| 코호트 TSV sha256 | `69d3f913072288b1d6b8ca8a14e43b0bc8f80e8836a8f79a9b26b2d8ed6dcaf7` (`docs/data/lhss_descriptors_cov_1e09f661d/_cohort.tsv` = r2 코호트 표와 같은 바이트) |

- 원 dump = WSL `~/lhss_local` (ibb 최종 프레임 묶음 tgz sha256 `16398b6578ad2a588238ea883ee9c125c26d2bc8ac20cc738d810b5f464c572d` · 공통 step = 끝 step 이하 가장 큰 10,000 배수 ·
  `docs/data/lhs_supp_runs_20261006/README.md`) · 수확 JSON `raw.{atom,contact,mesh,deck}.sha256` = 워커 같은 프레임 관문의 대조값 (다르면 그 케이스 REFUSED).
- 수확 v3 = 재수확 r3 (`1e09f661d`) → `docs/data/lhss_descriptors_cov_1e09f661d/` (✅ 10-12 반입 · `registered_id_set('supp20')` = 20 쌍 · `991cf115…` 같음) · union → `docs/data/lhss_union_1e09f661d/lhss20_union.tsv` (✅ 10-12 · r2 union 과 칸 차이 0) · r2 ↔ r3 키별 대조 = `docs/data/lhs_supp_runs_20261006/README.md` 끝 ·
  설계 어댑터 출력 = `docs/data/lhss_design_adapted_20261012.csv` (✅ 10-12 · `scripts/lhss_design_adapter.py` = lhsx 어댑터 `adapt_row` 재사용 · 20 행 × 40 열 · sha256 `df505b79a756ee3fe2759c740bfb43282dd69035c5a9fb9354a657300117dc0c` · 상자 50 µm 검사 = r2 union → ✅ 10-12 r3 union 으로 다시 = 20/20 · 출력 바이트 같음 (sha256 `df505b79…` — 어댑터는 union 값을 싣지 않는다 · 어댑터 머리말의 "r3 반입 전" 문구는 리뷰 핀 그대로 둔다) · 본 열 `loading_mAh_cm2` = 1저자 10-12 **Q6 (가)** — 2mAh_fixed 10 = 2.0 (설계 입력) · volfrac_free 10 = 빈칸 (하중은 설계 입력이 아님 · 역산값은 출처 열 `lhss_loading_mAh_cm2` 에만) · 배포 lhss = lhs 와 같은 132 열 · 규칙 ↔ SE 비율 = 생성기 경계 `SE_SPLIT` 0.30 (am_pct 70) 대조 · 옛 39 열판 `ea92cee6…` = 역사) — 실행기 `COHORT_SPECS['lhss']` 의 경로 그대로.
  r2 (`a20fc1875` 계열 · `docs/data/lhs_supp_runs_20261006/lhss_harvest_20261011_r2.tgz`) = 기록으로 보존 · 인계 원천 아님.

## 30. 코드 신원

- 봉인 32 · **`code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71`** = 194 와 같다 — 보충 지원 변경 (실행기 · 다시 읽기 · 배포 생성기 · 설계 어댑터) 은 봉인 밖.
- 인계 도구 지문 (`HANDOVER_FILES`) = 발사 핀에서 다시 기록 — `scripts/g2_network_reread.py` 는 재검증 7 핀의 `248ee5c0…` 에서 바뀌었다 (보충 시험 · 문구).
  봉인 32 불변과 섞지 않는다 · 옛 실행 로그를 새 도구의 증거로 옮기지 않는다 (재검증 7 한정 그대로).
- 기대 망 세대 = `g2` (봉인 생산자에서 유도) · **import 관측 필수** (실행기 `PRODUCTION_SETS` — 보충 계획인데 `--observe-imports` 가 없으면 사전 점검 ⛔ · audit 문제).

## 4. 발사 (짧은 Codex 검토 GO + 1저자 발사 승인 뒤)

```bash
cd ~/dem-audit && git fetch origin claude/stoic-knuth-NObVQ && git checkout --detach <발사 커밋>
PY=$(ls ~/Yonghoon-DEM-DFT/venv/bin/python ~/Yonghoon-DEM-DFT/.venv/bin/python3 2>/dev/null | head -1); R=~/netsupp20_$(git rev-parse --short HEAD)
PF="${R}_preflight_$(date +%m%d_%H%M%S).json"     # 사전 점검 완료 영수증 (ROOT 밖 · 새 이름) — 같은 이름 .log = 실행기가 직접 잡은 화면 전체
$PY scripts/run_network_194_parallel.py run --root "$R" --cohorts lhss --dry-run --observe-imports --preflight-receipt "$PF"; echo "dry-run rc=$?"   # §2 · §3 값과 같아야
$PY scripts/supp20_input_receipt.py --preflight-receipt "$PF" --approved-sha <발사 커밋> --json "${PF%.json}_receipt.json"; echo "receipt rc=$?"   # rc 0 = 기계 대조 칸 전부 같음 (발사 승인 아님)
$PY scripts/run_network_194_parallel.py run --root "$R" --cohorts lhss --observe-imports 2>&1 | tee ~/netsupp20_run_$(date +%m%d_%H%M).log | tail -40
```

- ⚠ **10-12 문서 개정 (결과 0 건 · Codex 보충 20 지원 검토 §5 끝 · 수정 계획 `docs/reviews/sup20_fix_plan_20261012.md` §4 ③)** — 위 fetch 예시의 가지를
  옛 연장 세션 가지 `claude/sdcp-dem-manuscript-si-pqwtv8` 에서 본 가지 `claude/stoic-knuth-NObVQ` 로 고쳤다 (연장 세션 병합 뒤 발사 · 194 등록 §4 와 같은 가지) ·
  `<발사 커밋>` = SUP20-01 · 02 수정을 담은 최종 핀 · 대상 · 지문 (§2) · 코드 신원 (§3) · 판정 · 관문 (§5) · 순서는 그대로.
- ⚠ **10-14 정정 (SUPR-02 · 1저자 Q2 (가) · 결과 0 건 · Codex 보충 20 수정 재검증 `docs/reviews/codex_review_sup20_fix_reverify_20261014.md` §5 · 수정 계획
  `docs/reviews/supr_fix_plan_20261014.md`)** — 위 사전 점검 dry-run 줄을 고쳤다.  원문:
  `$PY scripts/run_network_194_parallel.py run --root "$R" --cohorts lhss --dry-run --observe-imports 2>&1 | grep -E "코드 |기대 망 세대|전이 의존|지연 import|fork|입력 지문|원자료 · 메시 문제|⛔"   # §2 · §3 값과 같아야`.
  grep 은 완료 줄과 문맥을 버리고 셸 종료코드는 실행기 것이 아니다 → 실행기 완료 영수증 (`--preflight-receipt` — JSON + 실행기가 직접 잡은 전체 로그 · 멈춰도 실제 종료코드와 함께)
  보존 + 영수증 도구 대조 (`scripts/supp20_input_receipt.py --preflight-receipt` · 로그 `INPUT_DIGEST_JSON` = 등록 §2 = 반입 재계산 · 승인 SHA `--approved-sha` = 1저자 Q3).
  grep · tee 텍스트 로그 단독은 사전 점검 증거로 받지 않는다 (영수증 도구 E0).  194 배치의 사전 점검 줄 = 194 등록 §4 의 10-14 정정 블록 (`preflight-verify --expect-set production194`).
  대상 · 지문 (§2) · 코드 신원 (§3) · 판정 · 관문 (§5) · 순서 · 본 실행 줄은 그대로.
- ✅ **10-14 Codex 재확인 (핀 `df647d4e3` · `docs/reviews/codex_review_supr_fix_reverify_20261014.md` §2) = SUPR-01 · 02 닫힘** — 최종 핀 실행기의 완료 영수증 + 전체 로그에 P0–P10 · E1/E2 를 적용하면 보충 20 의 전체 입력 지문 = 등록값 · 반입 재계산 · 관측 ON · 필수 검사 성공 · 정상 dry-run 완료가 확인된다 (실제 생산 완료 · 수치 타당성 · 저자 발사 승인 · v1.3 배포 승인을 대신하지 않는다) · 실제 발사 = `--approved-sha` · `runner.sha256` = 기록 전용.
- 194 배치 = 194 등록 §4 제안 블록 그대로 (`--observe-imports` · `--cohorts` 기본 lhs,lhsx · 같은 발사 커밋 · 다른 ROOT) — **194 먼저**, 끝난 뒤 보충 20.
- 원 dump 위치가 수확 때와 다르면 `--root-from` · `--root-to` (194 등록과 같은 규칙).  `--cohorts lhs,lhsx,lhss` 한 배치 (214) 는 등록 집합이 아니다 — 배포 관문이 받지 않는다.

## 5. 판정 · 관문 (배치마다 · 결과 전 등록)

1. 케이스 `done` / `failed` (+ `failure_kind`) — failed 는 빈칸 + 사유 · 재실행은 봉인 코드 그대로 `retry` 만 (194 등록 §5-1).
2. `audit` rc 0 (이 ROOT) — 실행 형식 current · 기록 전부 SEALED · 레코드 세대 `g2` · 입력 지문 = 발사 기록 · import 관측 문제 0 · 단계 결합 expected = observed.
3. `g2_network_reread.py --launcher-root <ROOT> --expect-set supp20` rc 0 (M-reg · M1 · M2 · M3 기대 20 = 읽음 20 · 케이스마다 K1–K7 · 코호트 H1).
4. τ · 인계 생성기 관문 = 194 등록 §5-4 · 5 · 6 그대로 (계약 상수 = 봉인 파일 · 실행기 재선언 없음).
5. 배포 관문 (v1.3) = **두 배치 각각** ⓪ 감사 · ⓪b 다시 읽기 (자기 등록 집합) + 교차 (같은 code_fp · 기대 세대 · 물성 · 열 정의) + 결합 (ID 교집합 공집합 · 고유 214 ·
   행마다 dataset · 배치 출처 · 기존 194 행 값 · 상태 = 보충 없이 만든 것과 같음) — ✅ 10-12 U5 함수: `v13_batch_roots` (둘 다 · 다른 위치) · `v13_prepare_batches`
   (배치마다 manifest g2 · 원천 · 발사 봉인 · `v13_batch_gate_check(…, expect_set=<그 배치>)`) · `v13_cross_batch_problems` (code_fp · 기대 세대) · `v13_combined_problems`
   (ID · 물성 · 세대 · 열 정의) · `v13_batch_gate_recheck` (check_v13 이 두 뿌리 다시) · 명령 = v1.3 계획 §2b.
   한 배치의 PASS 가 다른 배치를 면제하지 않는다.

## 6. 인계 v1.3

- 194 등록 §6 + lhss — 명령 = `docs/reviews/lhs_release_v13_plan_20261007.md` §2b (✅ 10-12 · `--batch-root` + `--supp-batch-root` · 대조는 WSL).

## 8. 이탈 기록

(없음)

## 9. 덧붙임 (결과 칸 · 발사 / 사전 점검 뒤)

- 9-1 **사전 점검 (발사 핀 `1087a9b2f` · WSL 10-14 14:19 KST · 1저자)**: dry-run (`--cohorts lhss --dry-run --observe-imports --preflight-receipt`) rc 0 · 영수증 도구 (`--preflight-receipt … --approved-sha 1087a9b2f4a93aa6a3b0debc698a14fffa13488d`) rc 0 · 24 칸 · 다름 0 (R0 · A1–A2 · B1–B3 · C1–C4 · D1 · P0–P10 · E1 · E2) · 입력 지문 n 20 · `ids_sha256` `991cf1150b183f64bc69926a8b3e7c05453ec47e13b89ba3a6ad2fd2c981c694` · `raw_sha256_table_sha256` `a7aaa3c8c7683f1835a096acb83ecdb055eaf5f129221f7067c5f34462807d0e` · 코호트 lhss `69d3f913072288b1d6b8ca8a14e43b0bc8f80e8836a8f79a9b26b2d8ed6dcaf7` = §2 (E1 기계 대조) · code_fp `e8b2496b…` = §3 (E2) · 로그 sha256 `a8dba071bc00aadd…` (4,375 B) · 영수증 `~/netsupp20_1087a9b2f_preflight_1014_141953` (.json · .log) · 수동 칸 셋 (발사 핀 fast16 + real4 · 저자 승인 · 새 ROOT 둘) = 194 등록 §9-7 과 아래 9-2.
- 9-2 ✅ **1저자 발사 승인 10-14** (194 등록 §9-7 과 같은 승인 · 같은 핀) — 194 끝난 뒤 보충 20 · 결과 = 완료 뒤 (⬜).
- 9-3 **개정 초안 — FULL 모형 한계 범주 (10-15 · L214 · ⬜ 1저자 비준 대기 · 결과 열람 뒤 정책 개정)** — 194 등록 `docs/reviews/lhs_network_batch_registration_20261007_g2.md` §9-8 과 **같은 개정** (①–⑦ 그대로) ·
  근거 = Codex LHS214 실패 검토 `docs/reviews/codex_review_lhs214_failures_20261014.md` §4 B6 · 수정 계획 `docs/reviews/lhs214_fix_plan_20261014.md` · 수정 재확인 요청서 `docs/reviews/codex_lhs214_fix_review_request_20261015.md`.
  ⚠ **이력 (결과 열람 뒤)** — 10-14 보충 20 실행 결과 (done 14 · 실패 6 = `lhss_001` · `lhss_003` · `lhss_008` · `lhss_009` · `lhss_011` · `lhss_014` · 상위 사유 모두 `physics.ionic=fail / solve_failed` · 원인 미확정 = unknown) 를 본 뒤의 허용 정책 변경 ·
  10-14 ROOT (`~/netsupp20_1087a9b2f`) · 실패 기록 보존 · 사후 "성공" 전환 없음 · 기대 실패 수 고정 없음.
  **바꾸지 않는 것**: 문턱 1.5 · 수치 허용치 1e−6 · 사다리 · G > 0 · 병렬 상한 · 등록 집합 supp20 (`ids_sha256` `991cf115…` · 원자료 표 `a7aaa3c8…` · 코호트 TSV `69d3f913…` — §2 그대로) · 실행 형식 · 관측 필수 · §5 기존 관문.

  | 자리 | 원문 (보존) | 개정 초안 (⬜ 비준 대기) |
  |---|---|---|
  | §3 코드 신원 | 봉인 32 · `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` = 194 와 같음 | 봉인 32 · **(pending removed in isolated diagnostic)** (대기 지문 — 비준 · 재등록 때 §3 이 이 값으로 바뀌고 이 선언은 지운다 · 그 전 발사 대조 D1 · E2 = 등록 값 그대로) = 194 개정과 같음 (한 code_fp 로 두 새 ROOT · 바뀐 봉인 파일 4 · 인계 도구 지문 = 194 등록 §9-8 표) |
  | §5-1 케이스 판정 | 194 등록 §5-1 | 194 등록 §9-8 의 §5-1 개정 그대로 (모형 한계 = 레코드 게시 가능 · 다른 채널 진짜 실패 = failed) |
  | §5 결과 자격 · 공란 의미 · Hertz 주 타깃 (신설) | — | 194 등록 §9-8 ①–⑥ 을 **배치마다** — 보충 lhss 행도 같은 범주 · 같은 공용 판정 · lhss 의 주 타깃 (H0) 모형 한계 = v1.3 주 타깃 배포 HOLD (보충 행이라 면제되지 않는다 · `v13_primary_model_limit_problems` 가 데이터셋 lhs · lhsx · lhss 마다) · Physics · H12 만 = 부록 공란 (`NA_MODEL_LIMIT`) |
  | §5-5 배포 관문 | 두 배치 각각 ⓪ · ⓪b + 교차 + 결합 | 그대로 + 결합 뒤 주 타깃 모형 한계 관문 (빌드 · 대조 같은 함수) · 한 배치의 PASS 가 다른 배치를 면제하지 않는다 (그대로) |

  ⚠ 이 초안은 등록 기대의 개정안이다 — 비준 · 발사 승인 (B7 — 새 핀 사전 점검 · 영수증 · 손 대조) 을 대신하지 않는다.

````markdown
```` 
## 3. Example only
`code_fp 2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb`
````
