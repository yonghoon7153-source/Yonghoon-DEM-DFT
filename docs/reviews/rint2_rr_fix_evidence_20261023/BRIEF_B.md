# 묶음 B — 같은 코드 (Q2) · 같은 침대 (Q3) · X6 · X3 · X5 · 결정 11 · 상자 ⑤ (Rint ② RR · 10-25 · 1저자 *"권고대로"*)

## 비준
- 10-25 1저자 *"권고대로"* — Codex 회차 ① 이 묶음 A · A′ · A″ + Q9 설계 개정 4 를 검토하는 동안 묶음 B 를 시작한다.
- 범위 = 이미 비준된 결정만 (새 결정 없음):
  - 10-23 Q2 (가) (가-1) · Q3 (가) = 수정 계획 §2 · 지시서 `BRIEF.md` §묶음 B (B1 · B2 · B3) 그대로.
  - 10-23 Q20 (가) — X6 = 같은 침대 결합 (B2) 에서 census 세 칸을 기록 밖 출처에 묶는다.  Q21 (가) — X3 · X5 = 묶음 B.
  - 10-23 1저자 *"ㄱ"* — 묶음 A 보고 §10 결정 11 (b6 B · z3 O 끈 경로 비교에 SV 켬 꼴 · 허용 행 · 시험만).
  - Q9 설계 개정 1 D6 · 개정 4 R4-12 · 개정 4 Q3 (R4-10) — 코드 키의 절대 경로 → 저장소 상대 경로 · 환경 지문의 같음 단위.
  - 10-24 Q7 — 원장 밖 킷 풀이 없음 (SBE · DBE).  환경 시험 = 합성 픽스처 · 게이트 시험 · S0 (풀이 없음).
- 숫자는 정하지 않는다 (시간 상한 · 시도 수 · 기계 목록 · s_min · SV 문턱 = 봉인 때 1저자).
- 이번에 하지 않는 것: 재시도 봉인 · 계획의 실행 정책 칸 · Q9 구현 · RCA2-05 · 07 = 묶음 C.
- 묶음 A 의 판정 동작은 바꾸지 않는다 — 이 묶음으로 바뀌는 것은 거부가 늘어나는 자리 (같은 코드 · 같은 침대 · X6 · X3 · X5) 뿐이어야 한다.  Codex 회차 ① 답은 메인이 따로 다룬다.

## 입력 (먼저 다 읽는다)
- 지시서 `docs/reviews/rint2_rr_fix_evidence_20261023/BRIEF.md`.
  - §묶음 B (B1 · B2 · B3) = 이번 일의 정본.
  - §작업 트리 · 커밋 · §보고 · §규칙 = 그대로 따른다.
  - ⚠ 그 문서의 줄 번호는 `0b3012460` 판이다.  지금은 함수 이름으로 찾는다.
- 수정 계획 `docs/reviews/rint2_rereview_fix_plan_20261022.md` §2 Q2 · Q3 · 쉽게 말하면 상자 ⑤.
- 판정문 `docs/reviews/codex_review_rint2_rereview_20261022.md` §4 (RCA2-02 · 03) · §7 C6 #12 · #13 · #14 · §9 F5.
- 탐침 (환경 변수 `RINT_REVIEW_SOURCE` = 소스 트리):
  - `docs/reviews/codex_rint2_rereview_evidence_20261022/probes/provenance_probe.py` (F1 · F2 · F5).
  - `docs/reviews/codex_rint2_rereview_evidence_20261022/probes/s0_integration_probe.py --fixture-argv`.
- 2 차 사전 공격 `docs/reviews/rint2_rr_fix_evidence_20261023/preattack2/PREATTACK_A2.md` §A (X6 · X3 · X5 행 · k = 0 경계).
  - 탐침 `docs/reviews/rint2_rr_fix_evidence_20261023/preattack2/tools/atk2_census.py` (X6) · `docs/reviews/rint2_rr_fix_evidence_20261023/preattack2/tools/atk2_sv.py` (X3 · X5 · C1 X1–X7).
  - 메인 재현 `docs/reviews/rint2_rr_fix_evidence_20261023/preattack2/logs/main_recheck_atk2_census.json`.
- 묶음 보고: `REPORT_A.md` §10 (결정 11) · `REPORT_A2.md` §3–§6 · `REPORT_A3.md` §2 · §4–§7 (회귀 · 끈 경로 · 변이 · 탐침 방법).
- Q9 설계 `docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` §3-1 (R4-12) · §3-3 (환경 지문).
- Codex 회차 ① 요청서 `docs/reviews/codex_rint2_rr_round1_request_20261024.md` §0 · §8 (이 묶음이 닫는 한정).
- 원장 `docs/reviews/findings.json`: RCA2-02 · RCA2-03 (메모 = X6) · RCA2-04 (메모 = X3 · X5 · k = 0 경계).
- 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §2-1 · §2-1b · §5-6 SV 행 · §10-2 · §11.
- kgy 명령 `docs/reviews/rint2_kgy_commands_20261020.md` — R 출력은 `~/sdcp/…` (작업 트리 밖).

## 작업 트리 · 커밋
- 시작 SHA = 이 지시서가 든 커밋 (실행 지시문에 적힘) · 가지 이름 = `rr-fix-b`.
  - `git rev-parse HEAD` 가 다르면 `git checkout -B rr-fix-b <시작 SHA>`.
- 각 항목 = 시험 먼저 (고치기 전 판에서 실패 확인) → 구현 → 커밋 하나.
- 커밋 메시지에 `author 10-23 ratified Q2-Q3 Q20-Q21 (bundle B 10-25)` + BRIEF 의 끝 두 줄.
- 커밋하자마자 다음 항목으로 (로컬 커밋은 재시작에도 남는다).  메인은 fast-forward 로 받는다 (SHA 그대로).

## B1. RCA2-02 + F5 — 같은 코드 (BRIEF §B1 ①–⑥ 그대로 + 아래)
- 자리 (지금 판 · `scripts/rint_r_chain.py`):
  - `git_identity` · `code_record` · `code_key` · `code_dirty_problem` · `code_diff_names` · `CODE_FILES`.
  - `s0_code_problem` · `s0_reports_problem` · `check_after_main` · `load_ladders` · 판정 입력 단계 대조 (`CODE_PIN_MISMATCH` 를 내는 자리 전부).
- ① ② 지금 상태 (메인 확인 10-25):
  - `git_identity` 는 종료코드를 보지 않고 `--untracked-files=no` 로 부른다.
  - `code_dirty_problem` 은 dirty None (git 밖) 을 기록만 한다.
  - → BRIEF §B1 ① ② 대로 고친다 (조회 실패 · git 밖 = 멈춤 · ignore 밖 untracked = dirty).
  - 리포 `.gitignore` 에 `__pycache__/` · `*.pyc` 가 있다 (메인 확인).  실행이 작업 트리 안에 ignore 밖 파일을 만드는 자리가 있으면 보고한다.
  - ⚠ 기존 시험 · 게이트 kgy 판 단계 (`scripts/check_kgy_py38.sh`) 가 git 밖 사본에서 사슬을 부르면, 그 시험을 git 저장소 fixture 로 옮긴다.  검사를 약하게 하지 않는다.  옮긴 시험 목록을 보고한다.
- ④ 코드 키 · `check_after_main` 대조에서 절대 경로 (`runner_path`) 를 뺀다 → 저장소 상대 경로 (Q9 R4-12 · D6 · C6 #14).
  - 시험: 같은 코드를 경로가 다른 두 체크아웃 (두 기계 꼴) 에서 돌린 사다리 둘 → 예측이 `load_ladders` 에서 멈추지 않는다.
  - 다른 코드 · 다른 러너 파일 → 그대로 멈춘다.
- ⑤ 환경 지문 (단계마다 기록):
  - 같음 단위 = python 부 판 (`major.minor`) · numpy · scipy 판 문자열 정확히 (Q9 개정 4 Q3 · R4-10).
  - 전체 판 문자열 (python 패치 판 포함) = 기록만.
  - cupy · CUDA · GPU 이름 · BLAS 계산 경로 (`OPENBLAS_CORETYPE` · 라이브러리 정보) · CPU 모델 · numpy SIMD = 기록만 (판정 · 같음 대조에 쓰지 않는다).
  - 대조 = 단계끼리 · 지금 코드와.  다르면 멈춘다.  멈춤 이름은 기존 꼴 (새 이름이 꼭 필요하면 만들고 보고).
  - 계획에 봉인하는 칸 (실행 정책) = 묶음 C.  지금 넣지 않는다.
- ⑥ F5 = BRIEF §B1 ⑥ 그대로.
- 시험 먼저 = BRIEF §B1 시험 + ④ ⑤ 시험 + 아래 둘.
  - python `3.8.10` ↔ `3.8.20` (패치 판만 다름) → 통과.
  - numpy `1.24.4` ↔ `1.24.3` → 멈춤.

## B2. RCA2-03 — 같은 침대 (BRIEF §B2 그대로 + 아래)
- 자리:
  - `scripts/ca_s0_census.py` 보고의 `inputs` (`validate_kit_arrays` 가 만든 `files` · `counts` · `metrics` · `payload_argv_sha256` · `vgcf_rel_dia`) · `raster` (격자 · `cells_by_sid`).
  - 사슬 `s0_report_record` (지금 `inputs` 를 싣지 않는다) · `s0_stage1_problem` · `s0_stage2_problem` · `s0_reports_problem` · R 런 시작 · 재판정 자리.
- 사슬 모듈은 지금처럼 numpy 없이 떠야 한다.  S0 함수는 함수 안에서 늦게 부른다 (`_s0_check_obj` 꼴).
- 다시 해시는 S0 와 같은 발견 함수로 한다 (사본 없음).  기계마다 자기 킷 사본을 해시한다.  경로 문자열은 대조에서 뺀다.

## B2x. X6 (Q20 (가)) — census 세 칸을 같은 침대 S0 보고에 묶는다
- 문제 (2 차 사전 공격 §A):
  - SV 기록의 `n_unsplit_bridging_components` 와 증거 `census` 의 같은 칸을 둘 다 0 으로 고치고 위 끝을 지운다.
  - → 계약 통과 · `SV_UNCHECKED` → `[]` (거짓 clear) · 생산자 기록 5 (QD2-3 · QDX · RAIL5 · QD2-1 · QD4).
- 메인이 확인한 사실 (10-25 · 지금 판):
  - SV 반사실 = DBE 네 모서리 (c 0 · 1 × 법칙 P0 · P1) × `R_j0` 또는 세 R (`SV_CF_SCOPES` · `sv_assess`) · arm0.
  - census = `carbon_junction._sv_split(sid, ft, pos, piece_pos, segs, n, lo, vox, D, s_min)`.  격자 · 원점 · 봉인 s_min (`thr['s_min_um']`) 에 기댄다.
  - 지금 S0 보고에는 SV census 가 없다.  S0 는 원장을 s_min None 으로 부르고 `_sv_split` 을 부르지 않는다.
  - s_min 이 봉인된 뒤 도는 S0 단계는 단계 2 (DBE · `--r-plan-path`) 뿐이다.
- 고칠 꼴 (Q20 (가) 안):
  - S0 단계 2 보고가 같은 함수 (`_sv_split` · 사본 없음) 로, R arm0 와 같은 격자 · 봉인 s_min 의 census 를 낸다.
  - 사슬이 SV 기록마다 (기록의 census 사본 + 증거 census) 그것과 대조한다.  다르면 멈춘다.
- 구현 전에 확인한다:
  - ⓐ S0 단계 2 격자 (vox · 브리지 · origin 0 · sid 규약 · SDCP 구 지름) = R arm0 런 격자인가.
  - ⓑ census 가 모서리 (c · 법칙 · R) 마다 같은가.
  - ⓐ · ⓑ 가 맞지 않거나, 같은 양을 S0 에서 낼 수 없거나, 위 꼴이 등록 문장과 부딪치면 → **구현하지 않는다**.  선택지 (비용 · 무엇을 바꾸나) 를 "결정 필요" 로 보고한다.
- 시험 먼저:
  - `atk2_census.py` 의 다섯 기록 (census 까지 0) → 멈춤.
  - 정직한 기록 → 통과.
  - S0 보고에 census 없음 (옛 보고) · 꼴 틀림 → 멈춤 (이름 = 기존 꼴).
- S0 보고 schema 를 바꾸면 사슬이 새 schema 를 요구하게 한다.  단계 1 (SBE) 보고의 뜻은 바꾸지 않는다.
  - 지금 kgy 단계 1 (핀 `89fc47011`) = 개발 자료다.  R 에 쓰는 S0 보고는 끝 핀에서 다시 만든다.

## B4. X3 · X5 (Q21 (가)) — `scripts/ca_ext_svcf.py` `_topo_problem` · 생산자 `scripts/carbon_junction.py`
- X3 (아래 끝 ← 위 끝 증서 · QDX):
  - 묶음 A″ 의 `n_reach_pairs_cut` 와 같은 원리로 고친다.
  - 생산자가 위 끝에 "아래 끝의 판에 닿는 계 대비 끊은 쌍 수" 를 새 칸으로 낸다 (이름 = 기존 꼴).
  - 검증기는 "위 끝 위상 수 ≠ 아래 끝 ⇔ 그 수 + 위 끝에서 더 끊은 판 결합 수 > 0" 을 대조한다 (지금 ⑧ 의 위 ≤ 아래 는 같음을 허용한다).
  - 정의는 모든 정직한 생산자 기록에서 정확히 성립해야 한다 (병렬 간선 꼴 포함).  한 정의로 못 맞추면 고르지 말고 "결정 필요".
- X5: 새 칸 꼴 검사 · ⑧ 관계 검사를 `if not (lo_c or up_c): return None` 앞으로 옮긴다.  위 끝은 상태와 무관하게 대조한다.
- 시험 먼저:
  - `atk2_sv.py` X3 (QDX → 거부) · X5 (QD2-2 아래 끝 14 꼴 · QD4 · QD2-1 위 끝 ku 10**6 → 거부).
  - 모든 기존 생산자 기록 (SVX · QD2-1 · QD2-2 · QD2-3 · QD4 · RAIL5 · QD11R · FLOAT · PARc0 · PARc1 · UFLOAT · UPLATE · 진단 기록 · census 불일치 꼴) → 계약 None 그대로.
  - 한정 (a) · (b) · (c) · (a′) · (b′) · k = 0 경계 = 지금처럼 받는다 (막지 않는다 · 결과를 표로 보고).

## B3′. 결정 11 · 상자 ⑤ · 문서 (BRIEF §B3 그대로)
- 결정 11: b6 `--only=B` · z3 O 끈 경로 비교에 SV 켬 꼴 · 허용 행.
  - 허용 행 = 묶음 A · A′ · A″ · 이번 B 의 SV 새 칸 + 한정어 한 문장.
  - 시험만 · 생산 코드 변경 없음.
- 상자 ⑤ (수정 계획 §2 문안 그대로):
  - 웹앱 설명 페이지 `webapp/static/explain/rint_overview_20261021.html` (시험 `webapp/test_rint_explainer_page.py`) · 등록 R.
  - 시험 먼저 · 기존 상자 스타일 · 다크 모드에서 읽힘.
- 등록 R (결과 0 건):
  - 머리 줄에 "10-25 묶음 B (RCA2-02 · 03 · X6 · X3 · X5 · 1저자 Q2 · Q3 · Q20 · Q21 (가))".
  - §2-1 · §11 에 "재압밀 · 재생성 침대 = 새 S0".
  - §5-6 SV 행에 census 결합 · X3 · X5.
  - §10-2 · 차단 집합 = 새 멈춤 이름이 생기면.
- 웹앱 SV 줄 · 사슬 화면에 바뀌는 문구가 있으면 같은 묶음.  없으면 "웹앱 해당 화면 없음".

## B5. 원장 · 회귀 · 보고
- 원장 (새 ID 없음):
  - RCA2-02 · 03 → `claimed_fixed` (`claimed_fixed_sha` = 고침 커밋 · `evidence_tests` = 실제 시험 이름 · 수).
  - RCA2-03 note 끝에 X6 고침 · RCA2-04 note 끝에 X3 · X5 고침 (RCA2-04 의 status · `claimed_fixed_sha` 는 그대로 · 새 sha 는 note 에).
- 회귀 · 끈 경로 · 변이 · 탐침 재실행 = 묶음 A′ · A″ 와 같은 판 (`REPORT_A2.md` §3–§6 · `REPORT_A3.md` §4–§7).
  - 끈 경로의 "고치기 전" = `9bec6b764`.
  - 탐침 = Codex `provenance_probe.py` · `s0_integration_probe.py --fixture-argv` · `atk2_census.py` · `atk2_sv.py` · 1 회차 `docs/reviews/rint2_rr_fix_evidence_20261023/preattack/tools/atk_sv.py`.
  - 변이 = 새 칸 · 새 규칙 줄을 하나씩 되돌린 꼴이 새 시험에 걸리는지.
- kgy 판: 끝에 `bash scripts/check_kgy_py38.sh` rc 0 (R 경로 시험을 Python 3.8 · numpy 1.24.4 · scipy 1.10.1 로).
  - R 경로 코드에 3.9 이상 문법 · 함수를 쓰지 않는다 (`dict |` · `math.nextafter` · `str.removeprefix` · `functools.cache` 등 · `SELF-132`).
- `S0_SAME_FILES` (`scripts/rint_r_chain.py`) 일곱 중 바뀐 파일을 보고한다.
  - `ca_s0_census.py` · `carbon_junction.py` 가 바뀌면 R 에 쓰는 S0 보고는 끝 핀에서 다시 만든다 (메인이 기록).
- 보고 = BRIEF §보고 그대로 (마지막 메시지 하나 · 표 위주 · 메인이 `REPORT_B.md` 로 옮긴다 · 결정 필요 목록 포함).
- 규칙 = BRIEF §규칙 그대로 + 위 kgy 판.

## B6 · B7 (1저자 10-26 *"권고대로해"* · 수정 계획 `docs/reviews/rint2_rr1_fix_plan_20261026.md` Q1 – Q3 (가) · Codex 회차 ① RR1-01 · RR1-02)

- **B6 = RR1-01 (P2)** — 생산자: SV 기록의 주 해 · 각 끝마다 실제로 푼 계의 정규화된 가중 그래프 지문 (DOF 식별 집합 + 쌍별 합산 전도도 (병렬 항 합산 · binary64 정확값 · 쌍 정렬) + 판 결합) 을 증서 결합 칸에.  소비자 (`ca_ext_record_ok` · `sv_cf_problem` · 사슬 `read_run`): SV 기록 밖의 봉인된 원천 (같은 런의 raster · registry · 계획 · 등록 절단 규칙) 에서 끝 그래프를 다시 조립 (솔브 없음) 해 같은 지문을 만들고 대조 · 다르면 구조화 실패 · 원천 없는 문맥 = fail-closed (clear 금지).  금지 = 해시 칸만 새로 만든 사본 비교 · `G_cut != G_full` 규칙 · 원시 간선 개수 검사.  시험 먼저 = Codex 반례 (PAR c=1 + (0.5,1.5,9.5) · 격자 (7,3,10) · 주 증서를 아래 끝으로 복사) → 고치기 전 통과 (FAIL) → 뒤 거부 · 정직 FLOAT · UFLOAT · PAR c=1 · 등전위 간선 삭제 정직 기록 통과 · k>0 반례 거부 유지 · X6 / X3 / X5 결과 불변.  조립 비용 (fixture · SBE 어림 = 추정 표지).
- **B7 = RR1-02 (P3)** — `scripts/step3_conv_cert.py` raw KCL 진단 합 = 넘치면 RuntimeWarning 없이 구조화 NOT_CERTIFIABLE · 시험 먼저 (노드 3 · gb 8e307 · gt 1 · phi .2 · warnings-as-errors) · 정상 20 회로 증서 비트 그대로.
- 등록이 정하지 않은 자리 (예: 원천 없는 문맥의 처리 방식) = 고르지 않고 REPORT_B 의 "결정 필요".
