# Codex 재검증 요청 3 — 접촉망 세대 2 (G2RR2-01 ~ 05) · 새 실행 봉인 재등록 · S3 봉인 목록 (2026-10-07 KST)

- 직전 판정: `docs/reviews/codex_review_gen2_network_reverify2_20261007.md` (핀 `9d25757dc` · **HOLD** · 새 P1 없음 · 새 P2 G2RR2-01 ~ 04 · P3 G2RR2-05).
  Codex 증거 ZIP 은 아직 리포에 없다 — 아래 "옛 코드에서 빨강" 은 판정문의 반례 수치를 **우리 시험으로 다시 만든 것**이고, Codex 탐침 원본의 재실행이 아니다.
- 1저자 (10-07): *"자고 올게 해결해놔"* = 판정문 최소 수정 그대로.  194 발사 · v1.3 인계 = HOLD 그대로 — 판정문 §10 순서의 1 · 2 (수정 · 재봉인) 만 담았고
  3 (WSL 사전 점검 증거) 이 아직이다 (§7).  이 요청은 발사 GO 를 묻지 않는다.
- 검토 대상 = 이 요청서를 담은 커밋 (브랜치 `claude/stoic-knuth-NObVQ` · 1저자가 발송 때 sha 를 적는다).  코드 커밋 = 아래 넷 · 그 뒤 커밋 = 문서 · 원장.

## 1. 패치 (오래된 순)

| 커밋 | 원장 | 내용 | 시험 (옛 코드 + 새 시험 → 고친 뒤) |
|---|---|---|---|
| `5dde71dcc` | G2RR2-04 · 05 · §7 양성 | `tau_flux.sigma0_binding_problems` — 이온 세 가지 증서 σ₀ = 부모 `sigma_grain_S_cm` (정확히 · FULL 도) · 부모 σ₀ = 레코드 온도 규약 (`se_material` 로 다시 · 상대 1e-12) · 전자 · 열 = 채널 기준 · CF · 협착-only 차원값 재구성 = 부모 σ₀.  `tau_flux.branch_table_problems` — 정직한 실패 (숫자 없음 + 비게시 상태 + 사유) ↔ 기록 결손 (상태 키 없음 · null = 거부 · `not_computed` 로 채우지 않음).  둘 다 세대 2 계약 · 정지 계약 ⑧ (`network_sigma0_problem`) · 인계 P4 · 다시 읽기 K2 · K7 이 같은 함수 | `webapp/test_gen2_publication_handover.py` 22/32 → 32/32 (⑥0–⑥f · ⑦a–⑦d · ⑧) · `scripts/test_gen2_role_contract.py` 40/43 → 44/44 (Z1–Z4) |
| `3b2d1b91e` | G2RR2-01 · 03 | 실행기: `launch_eligibility` (run · retry · audit · merge 한 함수 · 새 형식 v3 필수 선언 · 역사 형식 = `HISTORICAL_LAUNCHES` 등록 + `--historical`) · CODE_FILES 29 → 32 (+ `fracture_model` · `lhs_union_webapp` · `ml_design_structure`) · `DEP_LAZY` 경로별 · `lazy_import_census` + `DEP_LAZY_OFFPATH` 21 · import 관측 훅 (`--observe-imports`) | `scripts/run_network_194_parallel.py --selftest` 68/79 (새 검사 11 빨강 = ㉝ 3 · ㉞ 4 · ㉟a–㉟d 4) → 81/81 (고치며 더한 2 = ㉔ 옛 형식 첫 run 역사 · 비역사 대조 · ㉟e 시범 관측 · ㉓e · ㉙ = 새 정책으로 고침) |
| `17ba65f4e` | G2RR2-02 | 다시 읽기: `--launcher-root` 등록 집합 필수 (`--expect-set production194` · `pilot3` · `--expect-case`) · 루프 전 계획 꼴 · 루프 밖 집합 대조 · JSON v2 · v1.3 생성기 = production194 전부 (기대 = 읽음 = 194 · 같음) 인 기록만 · 실행기 후속 명령이 집합 명시 · fixture 링크 symlink → 하드링크 → 사본 | `scripts/g2_network_reread.py --selftest` 9/14 → 15/15 (15 번째 = symlink 거부 환경 양성 · 이번 추가) · `scripts/test_lhs_release_v13.py` 76/80 → 80/80 · 실행기 82/82 (+ ㉛b) |
| `2d247a66f` | 판정문 §10 S3 (`GEN2-03` S3 쪽) | `seal_s3_prerun.NUMERIC_MODULES` 4 → 6 (+ `lens_geometry.py` · `se_material.py`) · `numeric_dependency_problems` = 소비자 (`run_s3_psi`) import 에서 시작한 정적 닫힘 ↔ 목록 · 봉인 발행 · 소비 둘 다 대조 · 코호트 cutoff · baseline · 봉인 창 무변경 | `seal_s3_prerun --selftest` 65/69 → 69/69 (⑮–⑮d) · `run_s3_psi --selftest` 79/83 → 83/83 (⑨h–⑨k) |

- "옛 코드 + 새 시험" = 고치기 전 코드에 새 시험을 먼저 넣고 돌린 결과.  시험이 따로인 것 (publication · role · v1.3 생성기) = 시험 파일만 새 것 · 고칠 파일은 그 앞 커밋 바이트.
  시험이 같은 파일 안인 것 (실행기 · 다시 읽기) = 시험을 먼저 넣고 고치기 전에 돌렸다 (옛 호출 꼴은 시험이 감싼다).  S3 둘 = 새 파일에서 고친 부분만 되돌린 사본
  (목록 넷 · 닫힘 함수 없음 · 봉인 거부 없음 / 러너는 앞 커밋 봉인기 + 소비 검사 되돌림) 을 잠시 넣어 돌리고 되돌렸다 (sha256 대조).
- 실행기 selftest 숫자 정정: `3b2d1b91e` 의 커밋 메시지 초안이 "82/82" 라 적었다 — 그 시점 실측은 81/81 (㉟e 까지 · 로그 대조) 이라 푸시 전에 메시지를 고쳤다 (amend).  82 = `17ba65f4e` 의 ㉛b 뒤.

## 2. 판정문 반례 → 시험 (우리 트리 · 옛 코드에서 빨강 확인)

| 판정문 | 시험 | 옛 코드 | 고친 뒤 |
|---|---|---|---|
| §2 input_digest 삭제 · null · 옛 레코드 + 기대 세대 두 키 삭제 (audit rc 0) | 실행기 ㉝ | rc 0 (통과) | audit 비영 · retry 세대 관문 막음 · control rc 0 · 원래 한쪽 삭제 반례 rc 1 |
| §2 해결 증거 "진짜 역사 ROOT 는 역사 모드에서만" | 실행기 ㉞ (커밋된 10-05 manifest) | 기본 audit 로 읽힘 | 기본 audit 비영 · `--historical` rc 0 SEALED_LEGACY · 등록과 다른 옛 모양 비영 · retry rc 2 |
| §3 plan 삭제 · cohorts=[] · cohorts 삭제 (0 케이스 rc 0) + 한 코호트 누락 · 중복 ID · 비등록 코호트 | 다시 읽기 selftest (반례 여덟) | 0 케이스 · n_fail 0 | 전부 FAIL · 등록 없는 `--launcher-root` rc 2 · pilot3 양성 · 합성 production194 양성 |
| §4 사본 K_IC_AM_P 0.3 → 30 · multicrack 100 → 0 · code_fp 그대로 | 실행기 ㉟c | 지문 그대로 · 봉인 통과 | code_fp 바뀜 · `seal_gate` changed fracture_model · 정상 값 보존 |
| §5 CF 증서 σ₀ ×2 + σ_dim 0.117810 → 0.235619 mS/cm · FULL 증서 σ₀ ×2 · 온도 변경 | publication ⑥0–⑥e · role Z1 | 게시 · 인계 · K1–K7 통과 | 정지 · 일반 경로 failed · τ 소비자 NOT_COMPUTED · 인계 τ P4 · K2 · K4 · H1 실패 / 양성 `--temp-c 60` (σ₀ 아홉 = 60 °C 규약값 0.014355301874382767) |
| §6 CF 다섯 키 삭제 (게시 · 인계 수용 · K7 만 거부) | publication ⑦a–⑦d · role Z1 | 게시 done · 인계 통과 | 정지 · 일반 경로 failed · 인계 거부 · K7 사유 = 공용 계약 결과 |
| §7 정직한 실패 양성 | publication ⑧ (실 생산자 SciPy · H0 이온 CF 만 주입) | — (양성) | 첫 spsolve 예외 = `solve_failed` (시도 spsolve) · 사다리 셋 다 증서 불합격 = `current_conservation_failed` (spsolve · cg+jacobi · gmres+ilu) · 게시 done · FULL q 0.00400538 그대로 · 인계 · 다시 읽기 통과 |
| §10 S3 목록 | seal ⑮–⑮d · runner ⑨h–⑨k | 옛 네 모듈 봉인 소비 통과 · 닫힘 함수 없음 | 옛 네 모듈 봉인 거부 · lens_geometry · se_material 지문만 다르면 거부 · 사본 변이 (모듈 수준 새 import = 봉인 밖 · 함수 안 = 분류 밖) · 실제 import 관측 (러너 `run_case` · 합성 원자료 · `-I`): 리포 모듈 8 = 목록 6 + 도구 2 · viewer3d_data 안 읽힘 |

- 같은 부류로 우리가 찾은 것 (판정문에 없음): `lhs_union_webapp` (τ 의 L_mc · φ_mc · `dem_analysis_core` 지연 import) · `ml_design_structure` (app import 때 `structure_predictor._restricted()` 안 · 관측이 찾음) — 둘 다 봉인에 넣었다.
- 194 v1.2 역사 레코드 194/194 = 새 σ₀ 대조 통과 (inferred_legacy · 25 °C) — v1.2 수치 철회 없음.

## 3. 회귀 (이 컨테이너 · Linux · 커밋 뒤 트리)

| 진입점 | 결과 |
|---|---|
| `webapp/test_gen2_publication_handover.py` | 32/32 |
| `scripts/test_gen2_role_contract.py` | 44/44 |
| `scripts/run_network_194_parallel.py --selftest` | 82/82 (76 s) |
| `scripts/g2_network_reread.py --selftest` | 15/15 |
| `scripts/test_lhs_release_v13.py` | 80/80 |
| `scripts/seal_s3_prerun.py --selftest` · `scripts/run_s3_psi.py --selftest` | 69/69 · PASS (83) |
| `scripts/wsl_network_smoke.py --selftest` (깨끗한 트리) | 11/11 |
| `webapp/test_pipeline_provenance.py` · `webapp/test_network_handover_chain.py` · `scripts/lhs_design_dataset.py --selftest` | 284/284 · 19/19 · 385/385 |
| `scripts/test_network_solve_certificate.py` · `scripts/test_tau_flux.py` · `webapp/test_tau_handover_status.py` · `scripts/test_reread_v12.py` | 27/27 · 55/55 · 41/41 · 22/22 |
| `webapp/test_gen2_stamp_record.py` · `webapp/test_psi_generation_stamp.py` · `scripts/test_network_generation2.py` · `scripts/test_network_boundary_rule.py` | 24/24 · 18/18 · 18/18 · 11/11 |
| `webapp/test_tau_grade_unify.py` · `webapp/test_tau_labels.py` | 20/20 · 46/46 |

- `check_all.sh` 전체는 돌리지 않았다 (메인 세션 몫).  Windows · WSL 원형 실행 아님.

## 4. 새 실행 봉인 (재등록 `docs/reviews/lhs_network_batch_registration_20261007_g2.md` — 결과 0 건에서 다시 등록)

- `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` (CODE_FILES 32 · 이 컨테이너 194 dry-run 같은 값) · 닫힘 30 ⊆ 32 · 지연 import 90 · 분류 밖 0 ·
  기대 세대 `'g2'` · 계약 문제 0 · ids `a04282d7…` · 원자료 표 `da7c93f9…` (§2 · 판정문 §8 재계산과 같음).  옛 `f3f54951…` · `b313e61a…` = 역사 (승인값 아님).
- 인계 코드 지문: `lhs_design_dataset.py` `27c9c1a8…` · `g2_network_reread.py` `23a949df…`.
- ⚠ 컨테이너 dry-run 의 "원자료 · 메시 문제 582 건" = 이 컨테이너에 원덤프가 없어서다 (`--allow-missing-raw`) — WSL 기대 0.
- v1.3 화면 패치 (`docs/reviews/lhs_release_v13_display_deferred_20261007.patch` — `webapp/app.py` = 봉인 파일을 바꾼다) 는 발사 뒤에만 적용 (재등록 머리).

## 5. 한계 (그대로 둔 것)

1. 도장 · 레코드 · 모든 사본 · 증서 · manifest 를 한 실행 안에서 일관되게 함께 바꾼 전면 위조는 재계산 없이 못 잡는다 (판정문의 한정 그대로).
2. 역사 모드는 등록된 옛 manifest 모양 · 발사 출처 (git sha · 19 파일 지문 · 키 집합) 를 대조한다 — 그 ROOT 의 입력 지문은 옛 형식에 없어 대조하지 않는다.
3. 정적 분류는 리터럴 import 만 본다 · 관측 22 (㉟d) 는 합성 se_am 의 표준 경로다 — 실침대 경로는 WSL 시범 `--observe-imports` (재등록 §1) 가 본다.
4. production194 양성은 합성 (194 링크가 한 게시 폴더) — 진짜 194 다시 읽기는 발사 뒤.
5. S3 실행은 별도 HOLD — 새 S3 봉인은 창 (09-17 23:59 KST) 이 닫혀 저자 결정 없이는 못 낸다.  이번 변경은 코드 신원 목록과 그 일치 검사뿐.
6. 실행기 selftest 가 실제 파이프라인 관측 (㉟d · ㉟e) 으로 76–86 s — 인벤토리 등급 `fast` 는 그대로 두었다 (재분류 = 별건).

## 6. 묻는 것

- Q1 (G2RR2-01) 필수 선언 + 역사 등록 + `--historical` 로 판정문 §2 해결 증거가 충족되는가 (네 우회 비영 · 역사 ROOT 는 역사 모드에서만 · 정상 · 원래 반례 유지).
- Q2 (G2RR2-02) 등록 집합 (production194 지문 · pilot3 · 명시 케이스) + 루프 전 · 밖 검사 + v1.3 생성기 집합 요구로 충분한가.
- Q3 (G2RR2-03) 32 파일 · 분류 · 관측으로 충분한가 — WSL 시범 `--observe-imports` 기록을 발사 전 필수 증거로 둘지.
- Q4 (G2RR2-04 · 05) 증서 σ₀ = 부모 σ₀ (정확 일치) · 부모 σ₀ ↔ 온도 규약 (상대 1e-12) · 전자 · 열 = 채널 기준 · 기록 결손 거부 — 정책 · 문턱 이의 여부.
- Q5 (S3) `se_material` 을 목록에 넣었다 (network_conductivity 모듈 수준 import · σ_bulk 기본값과 온도 규약 — S3 의 비 σ_eff/σ_bulk 에서 σ_bulk 는 약분될 것으로 보이나
  시험하지 않았다 · 소비자 경로 위라 넣음) — 동의 여부 · S3 실행 전 남은 것.

## 7. WSL 사전 점검 (아직 · 1저자)

재등록 §1 명령 그대로 (바뀐 곳: 2 단계 grep 에 `지연 import` · 5 단계 시범 `--observe-imports` · 다시 읽기 `--expect-set pilot3` · manifest 의 `launch_format` 줄).  붙여 넣을 것 = 각 단계 끝줄과 원 프로세스 `rc=` (판정문 §10-3).  결과는 재등록 §9-2 에 적는다.
