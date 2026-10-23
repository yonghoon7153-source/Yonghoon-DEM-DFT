# 사전 공격 리뷰 — 묶음 A (Rint ② RR · 10-23 05:41–06:41 UTC)

- 독립 에이전트 · 고친 사람 설명 (`REPORT_A.md`) 안 읽음 · 시작 SHA `2a093e5da` (코드 = `bd0e85ce6`) · 대상 = 코드 diff `49a1af626..bd0e85ce6` (15 파일) + Q9 설계 `docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` · 판정 = `PREATTACK_A.md` (코드 P1 0 · P2 1 · P3 4 · Q9 설계 P2 4 · P3 2 · 질문 1).
- 이 폴더 = 판정 + 그 에이전트가 새로 쓴 탐침 (`tools/`) + 결과 기록 (`logs/`) + 메인 재확인 (`logs/main_recheck_atk_sv.json`).
- `tools/` 의 `mkmut.py` · `mkmut6.py` · `mkmut9.py` · `runmut.py` · `py.sh` · `run_probes.sh` 는 작업 폴더 경로 한 줄만 환경 변수 `ATK_ROOT` 로 바꿨다 (나머지 그대로).  `ATK_ROOT` = 리뷰어 작업 폴더: `new_src/` = `2a093e5da` 트리 사본 · `old_src/` = `49a1af626` 트리 사본 · `mut/` = 변이 트리 (M1–M9) · `ev_new/` · `ev_old/` = 판정문 증거 폴더 사본 · `logs/` · `tmp/`.  `logs/` 원자료 안의 `/tmp/claude-0/…/atk1023/` 경로 = 그 작업 폴더로 읽는다 (원자료라 고치지 않음).
- 탐침 실행 = `RINT_REVIEW_SOURCE=<트리> OPENBLAS_NUM_THREADS=1 python3 -I -B tools/<도구>` (판정문 탐침과 같은 방식 · 출력은 표준 출력).
- 메인 재확인 (10-23 · 리포 트리 `2a093e5da` · Linux · Python 3.11.17 · NumPy 2.4.6 · SciPy 1.17.1 · BLAS 스레드 1):
  - `tools/atk_sv.py` → `logs/main_recheck_atk_sv.json` — C1 (A2) = 계약 None · 구간 [0.9999999999998652, 1.0000000000001348] · 문턱 2 에서 표지 [] (원 기록 = [10.291253935343772, 10.291253935346543] · SV_DEPENDENT) · C5 (A4 kind · rule) = 계약 None · 다른 형 · 부호화 공격 16/18 = 자기 사유 문장으로 거부 · A3 칼날 다섯 = 판정과 같음 · A1 다섯 회로 = 계약 None · 아래비 ≤ 정확 몫 · 위비 ≥ 정확 몫.
  - `tools/atk_bits.py` (`OPENBLAS_CORETYPE` 기본 · Haswell · Sandybridge) → seed0 σ 0.025659646167941766 · 0.025659646172737614 · 0.025659646164671895 · seed1 0.029640438423438248 · 0.02964043840621689 · 0.029640438412320665 = 판정 D2 의 값과 같음.
- 찾은 것의 처분 = 1저자 결정 뒤 (Codex 회차 ① 요청서의 사전 공격 리뷰 절 · 알려진 한정 절에 기록할 예정).
