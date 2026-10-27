# 묶음 C (코드) — C1 재시도 봉인 · C2 예측 12 단위 (Rint ② RR · 10-27)

> 반입 = 메인 (10-27) · 작업 트리 에이전트에게 준 지시 원문 (실행 중 · 결과 = `REPORT_C.md` 로 옮긴다) · 원문의 로컬 절대 경로만 뺐다.

## 비준 (1저자 10-27 원문)
- *"Rint는 권고대로 해도돼"* — 묶음 C 계획 Q1 = 지금 시작 · 에이전트 둘 (코드 = 이 지시서 · 문서/웹앱 = 따로) · 시험 먼저 · 숫자 칸은 봉인 때.
- *"11월 전체를 full로 사용할 수 있게 되어서 더 확실하게 하면 좋겠어 / 그렇다고 너무 늘리지는 말고"*.
  - 뜻 = **범위는 그대로** (BRIEF.md 묶음 C 의 C1 · C2 + Q9 설계 개정 1–5 + Codex 회차 ① §7 의 판단 · 인수 조건 ①②③).  새 기능 · 새 규칙 · 새 숫자를 만들지 않는다.
  - "더 확실하게" = **시험의 깊이** (아래 §더 확실하게).  범위를 넓히는 뜻이 아니다.

## 입력 (먼저 다 읽는다)
- `docs/reviews/rint2_rr_fix_evidence_20261023/BRIEF.md` — 전체 (작업 트리 · 커밋 · 보고 · 규칙 절) · **묶음 C 절의 C1 · C2 · C4**.
- `docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` — 개정 1–5 전부 (§2 · §3 · §4 · §5 · §7 · §8 · §10).  §8 = 시험 목록 (음성 · 양성 · 끈 경로).
- `docs/reviews/codex_review_rint2_rr_round1_20261026.md` — §7 (Q-A – Q-M 판단 + ① 같은 프로세스 문구 · ② 부모 사망 뒤 종료 확인 · ③ `REVERIFY_DIFF`) · §3 (끝 증서 귀속) · §10.
- `docs/reviews/rint2_rr1_fix_plan_20261026.md` (Q4 · Q7 순서) · `docs/reviews/rint2_rereview_fix_plan_20261022.md` Q4 (RCA2-05) · `docs/reviews/codex_review_rint2_rereview_20261022.md` (RCA2-05 · §6 C5 · C6 #14 · #15 · #30).
- 묶음 B · B″ 가 만든 칸 · 원천 · 회귀 목록 · 끈 경로 비교법 = `docs/reviews/rint2_rr_fix_evidence_20261023/REPORT_B.md` · `docs/reviews/rint2_rr_fix_evidence_20261023/REPORT_B2.md`.
- 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` — **읽기만** (고치는 것은 문서 에이전트 · 메인).
- 원장 `docs/reviews/findings.json` — RCA2-05 · RCA2-07 (open) — **읽기만** (C4 원장 변경 = 메인).
- 개발 탐침 원장 `docs/reviews/rint2_dev_probe_ledger_20261026.md` (§3-5 금지의 유일한 예외 · 읽기만).

## 시작
- 시작 SHA = `5288ff3c4` (메인 · 전체 SHA 는 `git rev-parse 5288ff3c4`).  먼저 `git rev-parse HEAD` 가 그것과 같은지 본다.  다르면 `git checkout -B rr-fix-c 5288ff3c4`.
- 가지 이름 = `rr-fix-c`.

## 범위
- **C1 = BRIEF.md 묶음 C 의 C1 그대로** (RCA2-05 · 계획 JSON 실행 정책 칸 · 같은 봉인 · `--max-hours` 대조 · 최대 시도 수 · 결과 전 멈춤만 재시도 · 같은 설정 요건 · 처음 완주 채택 · `attempt_<n>` 폴더 보존 · 팔마다 기계 이름 (빈 이름 금지 · 계획 허용 목록 안) · 문서 숫자 생성기 + 정확 대조 (fixture 계획으로 시험 · 등록 본문 숫자 칸은 "SBE 탐침 뒤 봉인" 그대로) · 값은 넣지 않는다 · 봉인 전 계획 = R 진입 거부).
- **C2 = BRIEF.md 묶음 C 의 C2 + Q9 설계 §3 · §8 · §10** (12 단위 · 세 명령 · 합치기 · 넘침 런 · 시도 원장 · 첫 풀이 끝 표지 · 러너 프로세스 그룹 · payload 를 처음부터 시도 폴더 안 `.unchecked/` · 판 봉인 + 풀기 전 대조 · 새 순서 (origin 표본 전부 → 이른 단조 → 넘침 origin8 → 끝 단조) · no-op = 사다리 단계 끝 · 같은 사슬 부모의 동결 환경 · 판정 단계 (`_replay_ladder` · `_replay_predict`) 같은 묶음 · 개정 5 ① ② ③).
  - Codex §7 의 한정을 지킨다: Q-D (그림자 런 · 모든 사본 일관 편집까지 막는다고 쓰지 않는다) · Q-G (플랫폼 무관 판정 보장이라 쓰지 않는다) · Q-I (이전 사슬과 모든 STOP 우선순위가 같다고 쓰지 않는다) · Q-J (payload 없으면 결정성 가정) · Q-K (종료된 그룹의 snapshot).
  - 이름: Q9 설계 §7 에 이미 있는 이름 (`UNIT_MISSING` · `UNIT_EXTRA` · `UNIT_PROVENANCE_MISMATCH` · `MACHINE_NOT_ALLOWED` · `ATTEMPT_LEDGER_MISMATCH` · `ATTEMPT_ORDER_MISMATCH` · `RESUME_MISMATCH` · `ATTEMPT_AFTER_ADOPTED` · `RESUME_NOT_ALLOWED` · `EXPANSION_NEEDED` · `unused_runs` · `REVERIFY_DIFF`) 을 그대로 쓴다.  설계가 "구현 때 정하는 꼴" 이라 둔 이름 (CLI · 거부 기록) 만 새로 짓고 보고 표에 낸다.
- RCA2-07 의 **구현 주석** 한 자리 (`scripts/rint_r_chain.py` 의 연장 단계 주석 = "각 연장 단계 비 ≤ 100 · 총 팽창 상계 없음") — 같은 파일이라 이 에이전트가 한다.  등록 R 본문 쪽은 문서 에이전트.

## 하지 않는 것
- 등록 R · Q9 설계 · README · 웹앱 · 원장 (`findings.json`) 고치기.  Q9 설계 §7 의 등록 개정 = 구현 이름이 나온 뒤 메인이 한다 → 보고에 **"등록 개정에 쓸 이름 표"** (CLI · 멈춤 · 상태 · 칸 · 거부 기록 · 폴더 꼴) 를 낸다.
- 숫자 (시간 상한 · 최대 시도 수 · 기계 목록 · s_min · 문턱) 넣기.  기본값 숫자 금지.
- push · fetch · `scripts/check_all.sh` · GPU · 킷 풀이 (SBE · DBE · 원장 밖 금지 = Q9 §3-5 · 1저자 10-24 Q7) · 봉인 32 파일 (`scripts/run_network_194_parallel.py` CODE_FILES).
- 문서에 너의 커밋 SHA 를 적지 않는다 (메인 반입 때 SHA 가 바뀐다 · `SELF-116`) — SHA 는 보고에만.
- 등록이 정하지 않은 자리를 만나면 고르지 말고 "결정 필요" 로 보고한다.

## 더 확실하게 (1저자 10-27) — 시험의 깊이
1. **시험 먼저** — 항목마다 고치기 전 판에서 새 시험이 **옳은 이유로** 실패하는지 확인 → 구현 → 통과.  보고 = 고치기 전 → 뒤 수 (시험 판 이름과 같이).
2. **실제 경로 시험** (Codex 회차 ① 표 끝 "정상·음성 실경로 시험" · `SELF-86` 교훈 = mock 만으로 계약을 시험하지 않는다): 실제 러너 · 실제 payload 프로세스 (합성 픽스처 · 작은 격자 · 풀이 몇 초) · 실제 프로세스 그룹으로 —
   - 러너만 SIGKILL · 사슬 부모 SIGKILL (부모가 죽은 뒤 살아남은 자식이 표지를 늦게 쓰는 꼴 = Codex ② 반례) · 시간 초과 · 표지 앞 · 뒤 사망.
   - supervisor / recovery 가 그룹 종료를 확인한 뒤에만 표지 · payload · 폴더 해시 확정 · 확인 못 하면 미확인 · 다음 시도 채택 거부.
   - 러너만 죽이는 시험과 사슬 부모를 죽이는 시험을 나눈다 (Q9 §10 · Codex ②).
3. **변이** — 새 가드마다 그 가드를 끄는 변이를 만들어 시험이 잡는지 본다 (변이 표 · 목표 = 생존 0 · 생존하면 이유와 함께 보고).
4. **끈 경로** — `--stage predict` 한 번 = 묶음 C 의 한 기계 사슬과 비트 같음 (Q9 §8 끝 줄 · 개정 4 R4-06 (a) 의 좁힌 문장 그대로) · 그 밖의 기존 경로 = 시작 SHA 와 비트 같음 (REPORT_B · B2 의 회귀 목록 전부 다시).
5. **kgy 판** — `bash scripts/setup_kgy_py38.sh` 뒤 `bash scripts/check_kgy_py38.sh` (Python 3.8 · numpy 1.24.4 · scipy 1.10.1) 에서 새 코드 · 새 시험이 돈다 (3.8 에 없는 문법 · API 금지 = `SELF-132`).
6. **기계 간 결정성** (Q9 §8 · Codex Q-E) — 두 환경 (이 컨테이너의 3.11 판 ↔ kgy 3.8 판) 에서 합성 SBE o0 · DBE o0–7 꼴의 SID_GRID 대조 · 이 컨테이너에서 못 하는 것은 한정으로 보고.
7. 중간에 멈춰야 하면 (시간 · 맥락) 반쯤 만든 가드를 남기지 말고 마지막으로 온전한 커밋까지에서 멈추고, 한 것 / 남은 것을 보고한다.

## 커밋
- 항목마다: 시험 커밋 → 구현 커밋 (BRIEF.md 와 같은 꼴).  메시지에 `author 10-27 approved bundle C` · 끝 두 줄:
  - `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
  - `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`
- 새 시험 파일을 만들면 `scripts/check_all.sh` 에 단계 줄을 넣고 (돌리지는 않는다) `--selftest` 꼴이면 `docs/reviews/selftest_inventory.tsv` 에 줄을 넣는다 (시간 = 실측).
- 각 커밋 전에 `python3 scripts/check_doc_refs.py` · `python3 scripts/check_review_findings.py` rc 0.

## 보고 (마지막 메시지 · 표 위주 · 메인이 이 폴더의 `REPORT_C.md` 로 옮긴다 (반입 때 생긴다))
- 커밋 목록 (SHA · 무엇).
- 시험 수 고치기 전 → 뒤 (시험 파일마다).
- 회귀 표 (시작 SHA ↔ 끝 · 끈 경로 비트 대조 방법과 결과).
- 변이 표 · 실경로 kill 시험 표 · kgy 판 결과 · 기계 간 결정성 결과.
- `S0_SAME_FILES` (`scripts/rint_r_chain.py`) 일곱 중 바뀐 파일.
- 등록 개정에 쓸 이름 표 (CLI · 멈춤 · 상태 · 칸 · 거부 기록 · 폴더 꼴 · 실행 정책 칸 이름).
- 결정 필요 (고르지 않은 자리) · 한정.
- 숫자 · 전칭 ("전부" · "무변경" · "N/N" · "비트 같음") 은 실행 출력으로만 · 범위와 시험 판을 같이 (`SELF-124`).

## 규칙
- BRIEF.md "규칙" 절 그대로 (python `-I` · `nice -n 19` · `OPENBLAS_NUM_THREADS=1` · OMP · MKL · NUMEXPR 도 1 · 디스크 = 사본은 다 쓴 뒤 지운다 · 남은 디스크가 적다 (약 6 GB) — 큰 사본을 만들지 않는다).
- 메인 checkout  은 건드리지 않는다 (게이트가 돈다).  너의 작업 트리에서만.
- 다른 호스트 (ibb · hit · kgy · gabia · v100) 에 접속하지 않는다.
