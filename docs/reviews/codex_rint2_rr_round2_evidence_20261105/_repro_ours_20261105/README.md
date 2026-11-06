# 우리 트리 재현 — Codex Rint ② 재검토 회차 ② (11-05)

- 무엇을: 판정문 (`docs/reviews/codex_review_rint2_rr_round2_20261105.md`) §1 · §3 · §4 · §7 · §11 이 든 탐침 9 개를 **고치지 않고** 다시 돌렸다 + 상주 BAN8 시험 하나 (변이 없음).  탐침 = 반입 폴더의 원본을 다 읽은 뒤 스크래치 작업 폴더로 복사한 것 (복사본 sha256 = 원본과 같음 · `docs/reviews/codex_rint2_rr_round2_evidence_20261105/_repro_ours_20261105/build_record.json`).
- 우리 트리: 탐침이 읽는 received/repo 자리에 Codex 사본이 아니라 **우리 git 의 핀 `6917c3c9f` blob** 을 넣었다 — 경로 집합 = Codex received/repo 와 같은 617 (우리 ZIP 606 + Codex 보충 11 · `git cat-file` 로 꺼내 blob id 대조 617 / 617).  git 저장소가 아닌 평범한 폴더 (Codex 와 같은 조건 — 생산 코드의 git 신원 조회가 같은 길로 간다).  리포 HEAD `504d84e52` 의 `scripts/` 는 핀과 같다 (그 사이 커밋 = 문서 · G2c 샌드박스 기록뿐).
- 환경 (우리) = Linux 6.18 · Python 3.11.15 · numpy 2.4.6 · scipy 1.17.1 · git 2.43.0 · OPENBLAS / OMP / MKL / NUMEXPR 1 스레드 · 탐침 = `python3 -I -B` (상주 BAN8 시험만 우리 사본에서 `python3 -B`).  환경 (Codex) = Windows 11 · CPython 3.12.14 · NumPy 2.5.3 · SciPy 1.16.3.
- 탐침이 만드는 scratch Git 저장소 · 임시 폴더 = 스크래치 작업 폴더 안 (리포 밖 · 리포와 다른 작업 트리의 git 은 건드리지 않았다).
- ⚠ Linux 신원 (`/proc` stat · environ) · 프로세스 그룹 종료 · 원장 잠금 = 탐침 자신이 모의 · 대체한다 — 우리가 Linux 에서 돌렸어도 실제 SIGKILL · flock 경쟁 · `/proc` 권한 · hidepid · kgy 동작을 시험한 것이 **아니다**.

## 결과 (탐침 · Codex 기록 · 우리 · 판정값 차이)

잎 대조 = 같은 JSON 의 잎마다 형 · 값 비교 (`docs/reviews/codex_rint2_rr_round2_evidence_20261105/_repro_ours_20261105/comparison.json` · bool 과 수는 다른 형).  우리 실행이 쓴 산출 JSON 은 리포에 넣지 않았다 (sha256 = comparison.json 의 ours_sha256) · 로그 = 이 폴더 `*.ours.log`.

| 탐침 | Codex 기록 | 우리 | 판정값 차이 |
|---|---|---|---|
| `docs/reviews/codex_rint2_rr_round2_evidence_20261105/runtime_review/probe_runtime.py` | 311 / 311 · RR2-01 표 (정수 1 = runner_rc · resume_ok=false · RESUME_NOT_ALLOWED / false · 0.0 = parent_dead · resume_ok=true · 다음 --resume 통과) · 메모리 안 후보 고침 = false · 0.0 · 글 "0" · null → runner_rc · 정수 0 그대로 · PC6-05 (TIME_LIMIT + 첫 결과 표지 + 로그 없음) resume_ok=true | rc 0 · 311 / 311 · 같은 표 · 같은 후보 고침 결과 · PC6-05 같음 | **0** — residual_rc.json 66 / 66 잎 · candidate_fix_results.json 42 / 42 잎 같음 · residual_rc_integration.json 55 잎 중 43 같음 · 다른 12 = scratch 경로 6 + scratch Git 시각 · 폴더 지문 6 (판정 칸 = recover 반환 · 결과 줄 status / side / cause / resume_ok / by · 다음 resume 자격 = 같음) · results.json 1,409 잎 중 1,405 같음 · 다른 4 = 환경 판 2 + 원천 sha256 칸 이름의 경로 구분자 2 (값 = 같음) |
| `docs/reviews/codex_rint2_rr_round2_evidence_20261105/runtime_review/probe_self137.py` | 3 / 3 (명령줄 74 · 180 · 1000 자 · 160 자 뒤 wrapper 보존) | 3 / 3 | **0** (12 / 12 잎) |
| `docs/reviews/codex_rint2_rr_round2_evidence_20261105/graph_review/probe_graph_core.py` | RR1-02 경고 0 · 예외 0 · NOT_CERTIFIABLE · Fraction 307 사례 × 3 순열 = 921 일치 · 지문 결합 둘 | 같음 | **0** (53 / 53 잎) |
| `docs/reviews/codex_rint2_rr_round2_evidence_20261105/graph_review/probe_actual_binding.py` | 정확 비 1.0170715052190031 · 정직 = SV_DEPENDENT · 옛 main → lower 교환 = 거부 (mismatch) · 원천 없음 = SV_UNCHECKED · 선언된 Q3 위조 = 계약 통과 · 표지 없음 · 인접 count 편집 거부 | 같음 (정확 비 분수 문자열까지) | **0** — 결과 58 잎 중 50 같음 · 다른 8 = 증서 구간 끝 끝자리 (최대 상대 2.2 × 10⁻¹⁶) · 조립 행렬 1,124 / 1,124 잎 같음 · 매니페스트 넷 307 잎 중 289 – 290 같음 · 나머지 = 해 끝자리 (잔차 resid 2.5 × 10⁻¹⁶ ↔ 2.4 × 10⁻¹⁶ 만 상대 2.9 × 10⁻² · 그 밖 ≤ 1.1 × 10⁻¹⁵) |
| `docs/reviews/codex_rint2_rr_round2_evidence_20261105/graph_review/probe_source_binding.py` | 깨끗함 통과 · git 밖 · untracked · 같은 HEAD 러너 파일 바뀜 · dirty 모름 · 짧은 HEAD = 거부 · numpy 바뀜 = 코드 키 다름 · 침대 fibre · kind · settings · metrics 바뀜 = S0_REPORT_MISMATCH · 경로만 다른 사본 = 통과 | 같음 | **0** — 18 잎 중 15 같음 · 다른 3 = numpy 판 글 1 + 합성 fixture 저장소의 HEAD 번호 2 (fixture 커밋 시각이 달라 번호가 다르다) |
| `docs/reviews/codex_rint2_rr_round2_evidence_20261105/root_review/probe_reverify.py` | 1,533 / 1,533 | rc 0 · 1,533 / 1,533 | **0** — 검사 이름 · pass 1,533 / 1,533 같음 · 잎 4,716 중 4,710 같음 · 다른 6 = scratch 경로 글 3 + 파이썬 판 1 + 깊은 중첩 저장본의 보고 까닭 2 잎 (같은 경우의 검사 둘 · 아래 §) |
| `docs/reviews/codex_rint2_rr_round2_evidence_20261105/root_review/run_first_result.py` | 첫 시도 = Windows 자식 인코딩 실패 (원 로그 보존) · 자식 UTF-8 명시 뒤 9 / 9 | 9 / 9 (첫 실행부터) | **0** — CRLF → LF 뒤 Codex first_result_utf8.log 와 바이트 같음 |
| `docs/reviews/codex_rint2_rr_round2_evidence_20261105/science_review/analytic_check.py` | 닫힌 꼴 ↔ 회로 최대 상대 4.71 × 10⁻¹³ · 여섯 경우 오차 / 허용폭 최대 0.5827902… (판정문 글 = 0.58280 · 같은 JSON 값을 다섯째 자리로 줄이면 0.58279) · 반감 비 3.99278 · 151,000 점 최대 0.66642 · 단언 넷 참 | 4.18 × 10⁻¹³ · 0.5827902… · 3.99278 · 0.66642 · 단언 넷 참 | **0** — 74 잎 중 64 같음 · 다른 = 끝자리 7 (회로 잔차 비 4.71 × 10⁻¹³ ↔ 4.18 × 10⁻¹³ 포함 · 둘 다 문턱 10⁻¹¹ 아래) + 환경 판 3 |
| `docs/reviews/codex_rint2_rr_round2_evidence_20261105/science_review/geometry_mutation_check.py` | M3 (시작점) rc 1 · 실패 18 (② · ③ · ⑨) · B01 (¼ 자리) rc 1 · 실패 6 (⑨) · ④ 는 둘 다 못 잡음 | 같음 | **0** — 실패 검사 이름 (괄호 앞) 18 / 18 · 6 / 6 같음 · 다른 글 = ③ 실패 글 안의 사다리 수 끝자리 5 줄 · B01 로그 = CRLF → LF 뒤 바이트 같음 |
| 상주 `scripts/test_carbon_junction.py` 의 `--only BAN8` (변이 없음 · 우리 사본) | 34 / 34 (보충 뒤 · ban8_reviewer_exact_deps.log) | 34 / 34 | **0** — CRLF → LF 뒤 Codex 로그와 바이트 같음 |

## 판정에 닿지 않는 차이 하나 — 깊은 중첩 저장본의 보고 까닭

- 검사 reverify_deep_result · report_semantics_deep_result: 저장된 결과가 `[` 2000 겹 꼴.  보고 까닭 목록이 Codex (3.12) = [unreadable, value] · 우리 (3.11) = [unreadable].  판정 (rc 1 = REVERIFY_DIFF) · 검사 pass · 원 판정 파일 그대로 = 둘 다 같다.
- 까닭 (확인한 범위): `scripts/rint_r_chain.py` 의 byte_diff_view 는 저장본을 먼저 겹친 칸 그대로 읽고, 못 읽으면 unreadable 만 적고 돌아간다 · 읽으면 값 대조 (value) 뒤 칸 순서 대조에서 재귀 한도를 넘을 때 unreadable 을 더한다 (함수 설명 그대로).  우리 3.11 에서 json.loads 가 2000 겹 배열에 RecursionError 를 내는 것은 확인했다 (첫 읽기에서 멈춤 = [unreadable]).  Codex 3.12 가 첫 읽기를 통과한 것은 그 기록으로만 본 것이다 (3.12 는 돌려 보지 않았다).
- ⇒ 다른 파이썬 판에서 다시 판정 **보고**의 까닭 목록은 달라질 수 있다 (바이트 판정은 그대로) — 판정문 §6 "보고 이유는 최종 바이트 판정을 바꾸지 않는다" 와 맞는다.

## 돌리지 않은 것

- Codex graph_review 의 상주 시험 묶음 (carbon QD… 157 · FP 19 · B6 286 · payload SG 11 · T25 4 · T24 시도) · root_review 의 B6 영수증 · science_review 의 보충 전 import 실패판 — 이번 재현 범위 밖 (돌리지 않았다).
- 실제 Linux SIGKILL · flock 경쟁 · `/proc` 권한 · hidepid · kgy 3.8.10 · SSH · GPU · 실침대 · S0 · 등록 R · 전체 게이트 — 탐침이 모의로 대신하는 부분은 우리가 Linux 에서 돌려도 시험되지 않는다.
- ZIP 안 verify_intake.py (Codex Windows 경로 고정) · verify_evidence.py — 실행하지 않았다 (매니페스트 702 줄 대조는 우리 스크립트로 · 다름 0).

⇒ **판정값 차이 0** — RR2-01 (false · 0.0 → parent_dead · resume_ok=true · 다음 resume 통과 · 후보 한 줄 고침 뒤 runner_rc) · PC6-05 (요약 있는 길 · 로그 없음 → resume_ok=true) · RR1-01 정확 비 · Q3 선언 위조 통과 · RR1-02 경고 0 · 다시 판정 1,533 · 첫 결과 표지 9 / 9 · BAN8 34 / 34 · 변이 탐지 · 해석 사다리가 우리 환경에서도 같다.
