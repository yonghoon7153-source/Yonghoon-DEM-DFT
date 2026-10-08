# Codex 세대 2 재검증 5 — 반입 · 우리 트리 재현 기록 (10-08 밤)

- 판정문 = `docs/reviews/codex_review_gen2_network_reverify5_20261007.md` — slim ZIP 안 같은 이름 파일 **바이트 그대로** (22,448 B · sha256 `1de52263d64b016c32b4e27e6094bab27d93c52fb7484d3e3eeaf40dbdf63f54` · CR 0 · 덧붙인 것 없음).
- 리뷰 핀 `aa7ec7fe98e8684f1a2138665f9eba978366c229` · WSL 사전 점검 핀 `839dbac6bf6185f7bc7f1b7a08d21b6b469a04ef` (두 핀의 scripts/ · webapp/ 차이 0 — 우리 git 에서도 `git diff --stat` 0).
- 판정 = 194 생산 · v1.3 HOLD · 새 P1 없음 · P2 셋 (G2RR5-01 · 02 · 03) · P3 하나 (G2RR5-04) · 원장 = `docs/reviews/findings.json` · 수정 계획 = `docs/reviews/g2rr5_fix_plan_20261008.md`.
- 요지 (10-08 붙여 넣기 옮김) = `docs/reviews/codex_review_gen2_network_reverify5_summary_20261008.md` — 이 원본으로 **대체됨** (대조 = §2).

## 1. 받은 것 · 넣은 것

| 묶음 | 크기 · sha256 | 파일 | 확인 |
|---|---|---|---|
| Codex 원 ZIP (codex_gen2_network_reverify5_20261007.zip) | 49,805,570 B · sha256 `75d3ed51d19a8f03b7201e5e1a8af192d10de7aabd5014e2116fecc18e3ddd91` | 2,997 | 원 ZIP 은 이 컨테이너에 오지 않았다 — 크기 · sha256 = 1저자 기록 (**미확인**).  파일 수 2,997 = slim 의 PACKAGE_CONTENTS.json 행 2,996 + 그 파일 자신 (대조됨) |
| slim ZIP (1저자 WSL 재포장 10-08) = 이 폴더 `codex_reverify5_slim.zip` | 8,789,126 B · sha256 `e39797e5c360367371ce061951eadf25ed90a4fe8333fe21edbb2e5f863e7ce0` | 2,510 (풀면 41,368,281 B) | 최상위 폴더 하나 (gen2_network_reverify5_20261007) · 절대 경로 · `..` · 링크 · 특수 파일 0 (새 빈 폴더에 안전 추출) |

- 재포장 규칙 (1저자): 폴더가 아닌 항목을 전부 두되, 최상위 폴더 뒤 상대 경로 rel 이 `source/` 로 시작하거나 · `^evidence/.*/handover/[^/]+\.(csv|tsv)$` 에 맞거나 · 크기 > 2,000,000 B 이면 뺀다.
- 대조 (원 묶음 목록 = PACKAGE_CONTENTS.json · Codex `package_review.py` 가 만든 2,996 파일의 경로 · 바이트 · sha256 · 자기 자신은 목록 밖):
  위 규칙을 목록에 적용한 집합 = slim 의 2,509 파일 (+ PACKAGE_CONTENTS.json) 과 **정확히 같다** · slim 2,509 파일의 바이트 · sha256 = 목록과 **2,509/2,509 같다**.
  뺀 것 487 = source/ 469 (54,519,336 B) + 합성 배포 반례의 handover CSV/TSV 18 (4,434,183 B) + 2 MB 초과 0 (그 둘 밖에는 2 MB 넘는 파일이 없었다).
  ⚠ PACKAGE_CONTENTS.json 자신은 목록에 없어 원본 바이트와 대조할 수 없다 (재포장이 바이트를 그대로 옮겼다고 본다 — 미확인).
- source/ 를 뺀 이유 = **리포가 곧 소스**다: source_manifest.json 469 경로의 핀 blob sha1 · sha256 · 바이트 = 우리 git (`aa7ec7fe9`) **469/469 같다** ·
  PACKAGE_CONTENTS.json 의 source/ 469 행 sha256 = source_manifest **469/469 같다**.  handover CSV/TSV 18 = 탐침이 `make_g2_handover_dir` 로 다시 만드는 합성 인계표 (TEST_ONLY).
- submitted/ (slim 안 · 반입 안 함) = 74 파일 — 73 = 리포에 커밋된 WSL 묶음 `docs/reviews/codex_gen2_network_reverify5_precheck_20261007/g2rr5_839dbac6b_1007_2224.tar.gz`
  (sha256 `41a755974d99aa0d1c8315cf3454cd15a7eeabdca31062c999f25c67118d2939` · 54,375 B · 파일 73 + 폴더 5 = 78 항목) 의 파일과 **73/73 바이트 같다** ·
  나머지 하나 request.txt (18,194 B) = 1저자가 붙여 넣은 요청서 렌더링 — 커밋된 `docs/reviews/codex_gen2_network_reverify5_request_20261007.md` 와 Markdown 기호 · 공백을 빼면 같은 글 (8,581 자).
- fixtures/observation_baseline (slim 안 · 반입 안 함) 64 파일 = 재검증 4 증거의 같은 파일 (`docs/reviews/codex_gen2_network_reverify4_evidence_20261007/` 의 fixtures/seal_baseline · evidence/receipt_path_translation 영수증) 과 **64/64 바이트 같다**.

### 1-1. 이 폴더에 둔 것 (크기 정책)

재검증 4 증거 폴더가 4.2 MB (파일 480) 인데 slim 2,510 파일을 다 풀면 41 MB 라 **풀지 않는다** — slim ZIP 한 파일 (= 받은 바이트 전부) + 작은 파일 42 (1,072,879 B · 전부 ZIP 안 바이트 그대로 · sha256 = PACKAGE_CONTENTS.json 42/42).

| 넣음 (풀어 둔 사본) | ZIP 안에만 |
|---|---|
| `README_REVIEW.md` (Codex 묶음 설명) · `PACKAGE_CONTENTS.json` (원 묶음 2,996 파일 목록 · 656,169 B) · `findings_review.json` (판정 요약 — ID · 등급 · 자리 · 범위) · `source_manifest.json` (469 경로 · 핀 blob) · `run_checks.py` · `verify_package.py` · `verify_added_source.py` | source_plan.json · prepare_source.py · package_review.py (Codex 쪽 취득 · 포장 기록 — 재검증 4 반입과 같은 처리) |
| `probes/` 10 (policy_scope · r5_case15 · r5_case15_fault_reread · r5_case15_pipeline_fault · r5_observation · r5_observation_fork · r5_observation_retry · r5_release_contract · r5_release_real_binding · submitted_verify) | notes/ 셋 (분리 검토 메모 — 판정문이 우선 · .md 둘은 자기 패키지 상대 경로가 많아 리포 문서 참조 검사에서 깨진다) |
| evidence/ 핵심 결과 25 — `evidence/submitted_verify.json` · `evidence/wsl_code_identity.json` · `evidence/runtime.json` · `evidence/source_final_verification.json` · `evidence/archive_inventory.json` · `evidence/policy_scope.json` · `evidence/r5_observation_fork.json` · `evidence/r5_observation_run2/results.json` · `evidence/r5_observation_run2/pair_missing_parse_liggghts/audit.json` · `evidence/r5_observation_retry/results.json` · `evidence/r5_release_contract/results.json` · `evidence/r5_release_real_binding/results.json` · `evidence/r5_case15_results.json` · `evidence/r5_case15_raw.json` · `evidence/r5_case15_pipeline_fault.json` (+ .log) · `evidence/r5_case15_pipeline_fault_reread.json` (+ .log) · runs_*.json 넷 · reread · publication · role 로그 | evidence/ 나머지 — 합성 감사 ROOT (r5_observation*) · 합성 배포물 (r5_release_*/…/release · TEST_ONLY_NOT_GO.md) · S0b 변이 13 의 다시 읽기 JSON (r5_case15_s0b_*) · release.log (583,915 B — Codex 171 PASS / 2 FAIL 원 로그) · 첫 실행 r5_observation (Windows 기본 인코딩 UnicodeDecodeError — 판정 미사용) |
| `_README_reproduction.md` (이 파일) · `_repro_ours_20261008.json` (우리 재현 요약 · 경로 지움 · 9 KB) | — |

- 판정문은 증거를 **자기 패키지 루트 기준** 상대 경로 (evidence/… · probes/…) 로 적는다 — 판정문 바이트는 고치지 않고 `docs/reviews/doc_refs_allowlist.tsv` 에 여덟 줄 (판정문 일곱 · 묶음 README 의 evidence/ 생략 한 줄 · 각 sha256 · 리포 사본 위치) 을 더했다.

## 2. 요지 (10-08) ↔ 원본 대조

ID · 등급 · 자리 · 직전 항목 상태 · Q1–Q8 · §7 최소 해제 목록은 **원본과 같다** (요지에 틀린 사실 없음).  요지가 뺀 것 중 뜻이 걸린 한정어:

| 자리 | 원본에 있고 요지에 없는 것 |
|---|---|
| G2RR5-01 (§1) | 생산자 자리 `scripts/run_network_194_parallel.py:615–628` · "CLI 는 잡는다 — 배포 경계가 요약과 모순되는 상세를 거르지 않는다" · "제출 시범 훼손 · σ 오답 증거 아님" · 사후 캐시 해시 검사는 새로 만드는 경로를 못 막는다 · "전체 원자료 재계산 · 전면 서명 체계 요구 없음" |
| G2RR5-02 (§2) | **"잘린 300 자 문자열을 늘려 grep 하는 것만으로 의미 계약을 대신하지 않는다"** · "제출된 WSL 실행을 무효화하지 않는다 · 수치 솔버 · 194 경계 규약 변경 근거 아님" · 무너지는 결론과 살아남는 좁은 결론 · 6/6 = 자식 정상 종료 · 원자료 SHA + 음성대조 4 |
| G2RR5-03 (§3) | 올바른 거부 행 (PASS 행 하나 FAIL · 셋만 · marker 제거 = rc 1 — 과잉차단 아님) · "G2RR5-02 를 고쳐도 소비자 구멍은 따로 남는다" · **"모든 실패 케이스 면제나 숫자 4 를 늘리는 처방은 답이 아니다"** · findings_review.json 의 줄 = 552 |
| G2RR5-04 (§4) | 코드 예외 자리 `scripts/run_network_194_parallel.py:578–628` · 재시도 표 셋 (6/5 · 1/1 rc 0 / 10/10 · 2/2 rc 0 / 10/10 · 2/1 rc 1) · **"문서 수정 항목이지 현재 감사 코드의 과잉차단은 아니다"** · 정상 중단 이력 삭제 · 성공 계산 재실행 금지 |
| 제출 증거 검산 (§5) | tar 54,375 B · 78 항목 · 단계별 stdout 10 · rc 10 전부 0 · **"옛 ROOT 전체가 다시 제공된 것은 아니며 게시 dual/full_metrics 원파일도 새 tar 에 없다 — 'WSL 원 ROOT 를 전부 재실행 · 재감사했다' 로 쓰지 않는다"** · 이온 보존 · 잔차 값 · 8 자리 기준의 반올림 반칸 = 상대 1.53e-5 · 1.38e-5 (실험 오차막대 아님 · 새 잔차 문턱 · 수치 모델 변경은 해결책 아님) |
| 시험 장부 (§8) | reread 20/20 · publication 32/32 · role 44/44 · staged audit CLI 17/17 · retry 4/4 · 제출 대조 61/61 (요지는 release 171/2 만) · "받은 WSL 자체 시험 reread20 · runner117 · smoke14/14 를 로컬에서 runner117 재실행한 것으로 쓰지 않는다" |
| §7-5 | "인계 도구 지문 변경은 기록한다" |

- 원본 머리 날짜 = 2026-10-07 (작성) · 요지 제목의 "10-08 수신" = 받은 날 — 내용 차이 아님.

## 3. 우리 트리 재현 (10-08 밤 · Linux · Python 3.11.15 · numpy 2.4.6 · scipy 1.17.1 · networkx 3.6.1 · Flask 3.1.3 · matplotlib 3.11.2)

- 소스 = 지금 브랜치 HEAD `342b18a18` 에서 source_manifest.json 의 469 경로를 `git archive` 로 (리포 밖 스크래치) — 핀 `aa7ec7fe9` 와 **462/469 같고 7 다르다**:
  docs/reviews/lhs_network_batch_registration_20261007_g2.md (머리 두 줄 · `690de79db`) · docs/reviews/selftest_inventory.tsv · scripts/check_all.sh · scripts/network_current.py ·
  scripts/plot_stress_z_distribution.py · scripts/viewer3d_data.py · webapp/static/js/viewer3d.js — 봉인 32 밖 · 이 탐침들이 부르는 경로 밖 (app.py 의 뷰어 · 보관 라우트 안 지연 import · 문서 · 셸).
- submitted/ · fixtures/ = slim 그대로 · probes/ = 무변경 · evidence/ 는 **빈 폴더에서 시작** (r5_release_real_binding 은 Codex 의 audit.json 이 아니라 우리 r5_observation 이 만든 실패 감사 JSON 을 먹는다).
- 실행 = 우리 driver (스크래치): 탐침 = `python3 -I -X utf8 -B` (부트스트랩이 probes/ · source/scripts · source/webapp + 사용자 site-packages 라이브러리 경로만 넣는다 — 묶음 폴더 · CWD 는 sys.path 에 없다) · 우리 시험 넷 = 묶음 run_checks.py 와 같은 꼴 (CWD source/ · PYTHONPATH source/scripts:source/webapp) · 차례로 (동시 실행 없음).
- ⚠ 환경 사고 한 건 (판정 미사용): 첫 r5_release_contract 실행은 `-I` 가 사용자 site-packages (이 컨테이너의 python-dateutil) 를 빼 matplotlib import 가 실패 → control 이 관문 전에 ModuleNotFoundError (gate 문제 0 · 모든 변이 '거부' 로 보임).  산출을 옆으로 치우고 라이브러리 경로를 되살려 새로 돌린 결과를 쓴다.

| 탐침 · 시험 | Codex | 우리 (HEAD) | 대조 |
|---|---|---|---|
| submitted_verify (제출 WSL 묶음 독립 대조) | 61/61 | 61/61 | 차이 0 (rc 파일 순서는 디렉터리 나열 순서라 이름으로 정렬해 비교) |
| policy_scope (production194 관측 OFF = 거부 · pilot3 선택 · fork 정적 검사) | production194 194 · flag_false 문제 · pilot3 3 · census [] | 같음 | 차이 0 |
| r5_observation (실제 audit CLI · staged) | 17/17 기대 결과 | 17/17 | 판정 · rc · 관측 문제 문자열 · stage_binding 차이 0 |
| r5_observation_retry | 4/4 (6/5 · 1/1 rc 0 / 10/10 · 2/2 rc 0 / 현재 기록 대체 rc 0 / 앞 시도 계획 없음 rc 1) | 4/4 | 차이 0 |
| r5_observation_fork | census [] · os 별칭 3 (같은 줄) · 정규식이 os.fork · multiprocessing 만 잡고 from-import · 별칭 · getattr 꼴은 못 잡음 | 같음 | 차이 0 |
| r5_release_contract (**G2RR5-01**) | control 생성 · check [] / 기존 계약 변이 11 거부 · 산출 없음 / binding null · parser 결손 · parser 0 · 계획 밖 · bool 개수 · n_finalized 0 = **생성 · check []** | 같음 | 차이 0 (거부 메시지 · 재판정 · 실제 제출 상세 계약 포함) |
| r5_release_real_binding (**G2RR5-01**) | 실패 요약 유지 = ReleaseError · 산출 없음 / **요약 하나만 [] = 생성 · check []** | 같음 (우리 audit CLI 가 만든 실패 binding: expected parser 1 · observed 없음 · 내부 problems []) | 차이 0 |
| r5_case15 (**G2RR5-03** · S0b 13 행) | positive rc 0 / marker_missing · checks_missing · checks_three · check_fail rc 1 / **marker_unknown · one_check_repeated_four · negctl_missing · tau_numeric · ionic_residual_bad · raw_sha_fail · unexpected_failure_record · real_failure_path rc 0** | 같음 | rc · n_fail 차이 0 · 다른 것 = 이온 CG 끝자리가 든 detail 문자열 11 · 합성 입력 지문 2 (개행 — 아래) |
| r5_case15 원자료 6 조합 | 원자 65,970 · 접촉 182,995 · 판 19.1455 µm · 상자 100 × 100 µm · B∩T 24 · 40 · 57 · 103 · 음수 면적 두 행 · Physics 열 ValueError · 이온 q 0.0003263508259103751 · 0.00036224724452177176 | 기하 · 행 · ID · 오류 같음 · q 0.00032635082552669387 · 0.00036224724407936984 (상대 1.2e-9 · 8 자리 같음) · 보존 1.90e-9 · 5.09e-9 (Codex 3.00e-9 · 6.32e-9) · 잔차 9.83e-11 · 9.41e-11 | CG 끝자리만 — **비트 동일 주장 안 함** (재검증 4 반입 때 우리 값과 같다) |
| r5_case15_pipeline_fault (**G2RR5-02**) | 망 CLI 호출 거부 1 · Parse · Contact · Coverage rc 0 · Network rc 1 · per-mode 없음 · τ NOT_COMPUTED · **검사 6/6 PASS** | 같음 (71.5 s) | 차이 = 실행 파일 경로 · 시도 기록 input_digests (내용 digest — Codex 65484b02… · ef0d734e… ↔ 우리 e140e28d3daf3ad7 · bcb53e13d2cc69be = **WSL 제출 기록의 digest 와 같다** — Windows 쪽 CSV 개행 차이로 추정) · 이온 CG 끝자리 |
| r5_case15_fault_reread (**G2RR5-02 → S0b**) | rc 0 · n_fail 0 · S0 · S0b PASS | 같음 | 차이 0 (8 유효 자리 같은 문자열 8) |
| g2_network_reread --selftest | 20/20 | 20/20 | 같음 |
| test_gen2_publication_handover | 32/32 | 32/32 | 같음 |
| test_gen2_role_contract | 44/44 | 44/44 | 같음 |
| test_lhs_release_v13 | 171 PASS · 2 FAIL (V10a Windows `/H/lhsx` 표기 · V16a `.git` 없는 사본) | **172 PASS · 1 FAIL** (V16a 만 — git archive 사본에 `.git` 없음 · V10a 는 Linux 에서 통과) | 환경 차이만 |

- 결과 = **판정값 차이 0** — 네 결함 (G2RR5-01 ~ 04) 의 반례가 지금 HEAD 에서도 그대로 재현된다 (수정 전).  차이는 환경 (CG 끝자리 · 개행 · 실행 파일 경로 · `.git`) 뿐이다.
- 요약 JSON = `_repro_ours_20261008.json` (파일마다 차이 경로 · 부동소수 최대 상대 차 · 우리 결과 표).
- ⚠ 이 재현은 **Codex 탐침이 우리 트리에서 같은 판정을 낸다**는 확인이다 — 194 생산 · WSL 실덤프 · S3 · DEM/MPM 을 다시 돌린 것이 아니다 (판정문 §0 · §8 의 한정 그대로).  release_* 는 합성 인계표 · 상위 τ 재독해 대역 위 관문 시험이다.

## 4. 원장 (`docs/reviews/findings.json`)

| 항목 | 바뀐 것 | 근거 |
|---|---|---|
| G2RR5-01 · 02 · 03 (P2) · G2RR5-04 (P3) | 새로 · open | 판정문 §1–§4 · findings_review.json |
| G2RR4-01 | claimed_fixed → **open (재개방)** · 닫는 조건 = G2RR5-01 검증 | §0 표 "부분" |
| G2RR4-02 | claimed_fixed → **verified** (범위 = 감사 생산 경로 · 배포 경계는 G2RR5-01) | §0 표 "감사 생산 경로 닫힘" · §6 Q2–Q5 |
| G2RR4-03 | claimed_fixed → **open (재개방)** · 닫는 조건 = 1저자 비준 + G2RR5-02 · 03 · 04 검증 | §0 표 "코드의 관측 필수화 닫힘 / 등록 부분" · §6 Q6 |
| G2RR3-02 | open → **verified** — ⚠ 판정문 5 에 이 항목 행은 없다 · 10-07 원장에 적어 둔 닫는 조건 ("G2RR4-02 검증") 충족으로 닫음 (verified_scope 에 명시) | §0 표 G2RR4-02 |
| SELF-94 | open → **verified** (claimed_fixed_sha = `bce0f3d28` 요청서 5 §6) | §5 끝 "SELF-94 정정은 수용" |
| SELF-92 · WEB-05 | 메모 한 줄씩 (상태 그대로) | §6 Q6 · Q7 · §2 |
