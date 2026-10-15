# LHS214 FULL 모형 한계 수정 — 증거 (2026-10-15 · 결과 0 건 · 새 214 실행 없음)

> **작업 트리 판** — 본 가지 대응 (메인 세션 대조 10-15): 시험 먼저 = `d0aa231d4` · 수정 = `6d0bec3c3` (`SHA256SUMS` 의 README 줄 = 이 채움 뒤 값으로 고침) · ★ (나′) 영수증 도구 시험 먼저 = `545d7d4fe` (§5) — 이 폴더의 로그는 격리 작업 트리에서 만든 것이다.  작업 트리 커밋 SHA 는 원격에 없어 적지 않고
> (로그 안의 그 SHA 는 `<작업트리-HEAD>` 로 가렸다 · 다른 바이트는 원문 그대로 — 해당 로그 둘 = `final/scripts__run_network_194_parallel.py_selftest.log` · `final/scripts__run_s3_psi.py_selftest.log`),
> 내용 해시로 대응시킨다 (아래 표 · `SHA256SUMS`).  기준 = 원격 본 가지 `0c557e72a` (수정 직전 · 봉인 32 `code_fp e8b2496b…` = 검토 핀 `1087a9b2f` 와 같은 봉인 · 같은 인계 도구 바이트).
> 요청서 = `docs/reviews/codex_lhs214_fix_review_request_20261015.md` · 근거 = `docs/reviews/codex_review_lhs214_failures_20261014.md` · 수정 계획 `docs/reviews/lhs214_fix_plan_20261014.md`.

## 1. 내용 해시 (본 가지 대응 = cherry-pick 뒤 같은 바이트인지 이것으로 본다)

| 자리 | 트리 digest (git tree) |
|---|---|
| 기준 `0c557e72a` 의 트리 digest | `2153e4aeb05073d2ed6d9da433b1676165a33501` |
| 시험 먼저 (작업 트리 판 ①) 의 트리 digest | `329fabb2b84d749a6416922d8a97325c976bf61b` |
| 수정 (작업 트리 판 ②) 의 트리 digest | `b461d371b8afa7b798b11f96892fc041fe0e8a3d` |

⚠ 트리 digest 는 기준 위에 그대로 올렸을 때만 같다 — 본 가지가 그 사이 움직였으면 아래 파일 sha256 으로 대조한다.

| 파일 | sha256 (작업 트리 판) | 판 |
|---|---|---|
| `scripts/network_conductivity.py` | `5bb703dbd8242938862708920f82e1e25704e905cb0b7b4e561d4688ba6cd73e` | ② 수정 (봉인) |
| `scripts/tau_flux.py` | `679967215b10fd20c15e33647e4185a8fb86cf510fff8789aad219ec13368d8d` | ② 수정 (봉인) |
| `webapp/app.py` | `1664590ea55e3ebf120be4d92cd5630c691c78f52648704f38f2f1fd9970ddd9` | ② 수정 (봉인) |
| `webapp/pipeline_service.py` | `9fe9d01794a2ecd8c12245af4469e13f1ce2d9561d92693b2f343208e72a2da4` | ② 수정 (봉인) |
| `scripts/g2_network_reread.py` | `0e2ec7ef37571268b85b0d17b71f7a2858aa2a7e6bcfadf4be1c6b5416dd5cd8` | ② 수정 (인계 도구) |
| `scripts/lhs_design_dataset.py` | `ff6af63cc11f3270c430f970e2c2ef599b23afd45db2e99a4bf3c190679dca5d` | ② 수정 (인계 도구) |
| `scripts/lhs_release_build.py` | `087b4c67b60352cddb653b6f8d36a871c39d03d48ccd728703cd52689b69105c` | ② 수정 (배포 빌더) |
| `webapp/templates/single.html` | `78be881634be85f6391b79a4a7bcebf11b7968537fe9d67bd5afb8cbb63df71c` | ② 수정 |
| `docs/reviews/selftest_inventory.tsv` | `2d7a6152622708c96a4369bf9ed01d02eaba4dabf9b870a1575a1c4c9f25167f` | ② (새 시험 등재 fast) |
| `scripts/test_lhs214_model_limit.py` | `40f75e3170337ace6f9068243da7a3b4f1efb5dffceabbb1e57cc23c2692f557` | ① 시험 먼저 |
| `webapp/test_network_handover_chain.py` | `7824616d518fdaf14db2d83486f7288c63844ff64baec1b95651512e5193c5fa` | ① 시험 먼저 |
| `scripts/test_network_solve_certificate.py` | `93e3911e58aadc209455da3ee0efd64d7a2e28e38e3a134508f20f0197dcd857` | ① 시험 먼저 |
| `scripts/test_lhs_release_v13.py` | `c1f1c27c155f10a1de422098cbe3d30a50de0eeb7d6358ba8a02c7e1c25a8242` | ① 시험 먼저 |
| `webapp/test_pipeline_provenance.py` | `df94b2558617ac39c3fa76ec4b67c07b40ae2316124fbf7a3532b7172171555f` | ① 시험 먼저 (침대 셋) |

- 봉인 32 `code_fp` = `acc7bfa335ec8fa8a7b76eb981135f16994b084ce0746476c5d05f61488af2ed` (`code_fp_report.log` · 재봉인 아님).

## 2. 무엇이 어디에

| 파일 · 폴더 | 내용 |
|---|---|
| `before/` | ① 시험 먼저 판 (기준 코드 + 새 시험) 에서 돈 다섯 — 고치기 전 실패 확인 (13/54 · 27/28 · 21/34 · 255/256 · 284/284) |
| `final/` | ② 수정 판 깨끗한 트리 — 핵심 · 무거운 시험 · 규율 검사 (`final/final_core_summary.log` = 핵심 21 실행의 요약) |
| `final/sweep/` · `final/sweep_summary.log` | 회귀 묶음 47 실행 (스크립트 13 · 웹앱 34) — 전부 rc 0 |
| `before_napr/` · `final/scripts__supp20_input_receipt.py_selftest.log` | ★ (나′) 영수증 도구 selftest — 시험 먼저 81/99 (고치기 전 도구 + 옛 초안 꼴) → 고친 뒤 99/99 (§5) |
| `rc.tsv` | 명령 · 종료코드 · 초 · 결과 · 로그 (한 줄 = 한 실행) |
| `a4_no_impact.py` · `a4_no_impact.log` · `a4_no_impact.json` | A4 무영향 대조 (기준 `0c557e72a` ↔ 고친 트리 · 읽기 전용 · 32/32 통과) |
| `code_fp_report.py` · `code_fp_report.log` | 봉인 CODE_FILES 32 · HANDOVER_FILES 지문 (기준 ↔ 고친 트리) |
| `SHA256SUMS` | 이 폴더 파일의 sha256 (이 README 포함 · 자기 자신 제외) |

## 3. 명령 (전부 `OMP_NUM_THREADS=1` · 한 번에 하나 · 컨테이너 Linux · Python 3.11)

```bash
# 시험 먼저 (고치기 전 코드 + 새 시험) — ① 판을 체크아웃한 깨끗한 트리
python3 scripts/test_lhs214_model_limit.py --selftest      # rc 1 · 13/54
python3 scripts/test_network_solve_certificate.py          # rc 1 · 27/28 (G4b)
python3 webapp/test_network_handover_chain.py              # rc 1 · 21/34 (⑤ 13 FAIL)
python3 scripts/test_lhs_release_v13.py                    # rc 1 · 255/256 (V2b)
python3 webapp/test_pipeline_provenance.py                 # rc 0 · 284/284 (침대만 더함)
# 고친 뒤 (② 판 · 깨끗한 트리) — 위 다섯 + rc.tsv 의 final 줄 · 무거운 셋은 맨 끝에 하나씩
python3 scripts/run_network_194_parallel.py --selftest     # 139/139
python3 scripts/wsl_network_smoke.py --selftest            # 16/16
python3 scripts/wsl_network_smoke.py --selftest-real       # 4/4 — case15 음성 대조 계속 거부
python3 docs/reviews/lhs214_fix_evidence_20261015/a4_no_impact.py --json docs/reviews/lhs214_fix_evidence_20261015/a4_no_impact.json   # A4 PASS 32/32
python3 docs/reviews/lhs214_fix_evidence_20261015/code_fp_report.py
```

## 4. 결과 요지

| 묶음 | 고치기 전 | 고친 뒤 |
|---|---|---|
| `scripts/test_lhs214_model_limit.py --selftest` (신설 · A2) | 13/54 | 55/55 |
| `webapp/test_network_handover_chain.py` (A3 끝-끝 ⑤a–⑤k) | 21/34 | 34/34 |
| `scripts/test_network_solve_certificate.py` (G4 · G4b) | 27/28 | 28/28 |
| `scripts/test_lhs_release_v13.py` (V2b) | 255/256 | 256/256 |
| `webapp/test_pipeline_provenance.py` | 284/284 | 284/284 |
| A4 무영향 (`a4_no_impact.log`) | — | N 16 · T 6 · R 2 · W 2 = 비트 같음 · W 의도 변경 6 쌍 = Physics · Δ 칸만 (행 · 이름 · Hertz 칸 불변) |

- 분모 54 ↔ 55: 고치기 전 코드에서는 예외로 멈춘 묶음 하나가 FAIL 하나로 세진다 (`_guard`).
- ⚠ **첫 고친 실행 뒤 바꾼 것 (투명성)** — ⓐ 내 오기 하나: 증서 판정 안 상수 이름 (`_Q_REC_TOL` → 정의된 `_Q_REC_REL_TOL`) — NameError 로 신설 시험 13/17 에서 멈춤 → 한 줄 고친 뒤 55/55 ·
  ⓑ 시험 기대 정정 둘 (결과로 맞춘 것이 아니라 기존 설계 · 의도 어휘에 맞춤): 체인 ⑤f2 기대 {K2 · K4} → {K4 · K6} (K2 세대 계약은 0b 공용 기술 검사를 못 넘은 레코드를 그 검사에 맡긴다 — G2RR-02 이후 설계 · 위조 q 는 K4 · K6 이 잡는다 · 거부라는 결과는 같다) ·
  v1.3 V2b 닫힌 빈칸 어휘에 `NA_MODEL_LIMIT` (의도된 어휘 확장 — Codex Q3).  둘 다 ① 시험 먼저 판에 넣고 고치기 전 코드에서 다시 쟀다 (위 표의 "고치기 전" = 그 판).
- 작업 트리 판의 더러운 트리에서 `seal_s3_prerun` · `run_s3_psi` selftest 가 "작업트리가 수치 모듈을 고치고 있다" 로 거부한 것은 설계대로 (봉인 신원 관문) — ② 커밋 뒤 깨끗한 트리에서 통과 (`final/`).

## 5. ★ (나′) 봉인 지문 대기 선언 (1저자 10-15 Q1 (나′) · 요청서 §9)

- 계기 — 본 가지 합친 게이트에서 `scripts/supp20_input_receipt.py --selftest` 실패: 보충 20 등록 초안 §9-3 이 새 지문 `acc7bfa3…` 를 등록 값과 같은 꼴 (`code_fp <hex>`) 로 적어
  등록 §3 을 못 읽음 (R0 · D1) · S0 실패 · S0b AttributeError.
- 결정 — 두 등록 초안 (194 §9-8 · 보충 20 §9-3) 의 새 지문 = 대기 지문 선언 `code_fp_pending acc7bfa3…` · 발사 대조 (D1 · E2 · F5 · G5) = 등록 §3 값만 그대로 · 시험만 선언된 대기 상태를
  정확한 실패 집합으로 받는다 (컨테이너 {D1} · 사전 점검 영수증 {D1 · E2} · 합성 발사 manifest 둘 {D1 · F5 · G5}).
- 도구 = `registration_values()` 의 선택 항목 `code_fp_pending` (값 둘 이상 · 등록과 같음 = R0 문제) · D1 상세에 `pending` 만 · 판정식 무변경 — 고친 판 sha256
  `18ce78ca4930545084a47d1361832faf28b6ab235d5ce10e941f75df0b27b772` (봉인 32 · HANDOVER 밖 · code_fp 무관) · `docs/reviews/selftest_inventory.tsv` = 영수증 줄 메모만 더함 →
  sha256 `5ce4ab22bc6f54d08beb5feb74635f7f37cec533deab65de0ca624e1fd5df803` (§1 표의 `2d7a6152…` = ② 판 그대로 기록).

| 실행 | 판 | 결과 | 로그 |
|---|---|---|---|
| `python3 scripts/supp20_input_receipt.py --selftest` | 시험 먼저 `545d7d4fe` (고치기 전 도구 + 옛 초안 꼴 등록 문서 · 상태 undeclared) | rc 1 · **81/99** (FAIL 18) | `before_napr/scripts__supp20_input_receipt.py_selftest.log` |
| 같은 명령 | 고친 뒤 (도구 + 대기 선언 꼴 등록 문서 · 상태 pending) | rc 0 · **99/99** | `final/scripts__supp20_input_receipt.py_selftest.log` |

- 두 로그 = 원문 그대로 (가린 곳 없음) — 실패 사유 출력은 지문 값만 싣는다 (E2 상세의 로그 코드 줄 = git 짧은 sha 를 시험이 출력하지 않는다) · 둘 다 `OMP_NUM_THREADS=1` · 컨테이너 Linux · Python 3.11.
