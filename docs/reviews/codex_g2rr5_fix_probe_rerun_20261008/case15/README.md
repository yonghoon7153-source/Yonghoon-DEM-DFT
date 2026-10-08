# G2RR5-02 · 03 수정 뒤 Codex 탐침 재실행 — case15 (10-08 밤)

- 대상 = G2RR5-02 커밋 `72879744e` + G2RR5-03 커밋 `b34a52f52` (탐침을 돌린 커밋 — 이 요약은 그다음 커밋 · 문서만 · 두 스크립트 blob:
  `scripts/wsl_network_smoke.py` 20d61d1d… · `scripts/g2_network_reread.py` 07d2830d…).  수정 계획 `docs/reviews/g2rr5_fix_plan_20261008.md` §2 · §3 ·
  판정문 `docs/reviews/codex_review_gen2_network_reverify5_20261007.md` §2 · §3.
- 탐침 = `docs/reviews/codex_gen2_network_reverify5_evidence_20261007/probes/` 의 `r5_case15` · `r5_case15_pipeline_fault` · `r5_case15_fault_reread` **바이트 그대로**.
- 드라이버 = 재현 때와 같은 스크래치 도구 (`docs/reviews/codex_gen2_network_reverify5_evidence_20261007/_README_reproduction.md` §3): `setup_repro.py` 가
  slim 묶음의 probes · fixtures · submitted 를 복사하고 소스 469 경로를 이 커밋의 `git archive` 로 만든다 (핀과 같은 460 · 다른 9 = 재현 기록의 7 (탐침 경로 밖) +
  이번 두 스크립트) · evidence 는 빈 폴더에서 시작 · `run_repro.py` = `python3 -I -X utf8 -B` (부트 = probes · source/scripts · source/webapp + 사용자 site-packages).
- 이 폴더 = 요약 둘 (이 README · `rerun_summary.json` — 핀 ↔ 고친 트리 · 변이별 · 명령 · 커밋).  원 로그 · 증거 JSON 은 넣지 않았다 (스크래치 · 경로 지움).

## 명령 (S = 스크래치 · 리포 밖)

```
python3 -I $S/r5tools/setup_repro.py $S/r5x/slim/gen2_network_reverify5_20261007 $S/g2rr5_0203/repro_A <worktree> b34a52f52
python3 -I $S/r5tools/run_repro.py $S/g2rr5_0203/repro_A r5_case15
python3 -I $S/r5tools/run_repro.py $S/g2rr5_0203/repro_A r5_case15_pipeline_fault
python3 -I $S/r5tools/run_repro.py $S/g2rr5_0203/repro_A r5_case15_fault_reread
# 보충 (표지) — 같은 커밋의 둘째 뿌리 repro_B: r5_case15 만 -O · 나머지 둘은 위와 같은 드라이버 · B2 = 입력 대체 뒤 fault_reread 한 번 더
```

## 결과 — 그대로 실행 (뿌리 A)

| 탐침 | 핀 `aa7ec7fe9` (Codex · 우리 재현 같음) | 고친 트리 |
|---|---|---|
| `r5_case15_pipeline_fault` (**G2RR5-02**) | 망 CLI 거부 1 · 검사 6/6 PASS · 실패 0 (스모크 rc 규칙 0) | 망 CLI 거부 1 · 검사 7 — 6 PASS + `case15.nc5_attempt` **TECH** (기록기: PermissionError · rc 없음 · per-mode 없음 / 망 솔버 단계 rc 1 · 산출 결손 넷 · verify_failed True) → 스모크 rc 규칙 **1** · 시도 digest = 원자료 (e140e28d… · bcb53e13…) |
| `r5_case15` (**G2RR5-03**) | positive rc 0 · 일곱 오수용 + real_failure_path rc 0 · 회귀 넷 rc 1 | 42 줄 `assert not summary['producer']['submitted_positive']['failures']` 에서 **멈춘다** (0.6 s) — 제출 WSL 10-07 case15 기록 (G2RR5-02 이전 생산자) 의 생산자 판정이 이제 ⑤ FAIL (실제 시도 증거 없음) |
| `r5_case15_fault_reread` (**G2RR5-02 → S0b**) | rc 0 · S0 · S0b PASS | 시작 못 함 — 입력 r5_case15_s0b_positive.json (묶음 evidence 폴더) 은 `r5_case15` 가 쓰는데 그 탐침이 42 줄에서 멈췄다 (FileNotFoundError) |

## 보충 (뿌리 B · 표지 — 탐침 바이트 · 입력은 그대로, 실행 방식만 다르다)

- `r5_case15` 를 `-O` 로 (assert 문 제거) — 42 · 62 · 91 줄을 지나 변이 12 행을 기록한다.  ⚠ 91 줄 `assert reread('positive', base)['rc'] == 0` 은 **호출까지** assert 안이라
  `-O` 에서 실행되지 않는다 → positive 행 · `r5_case15_s0b_positive.json` 없음.  이 경로의 리포 모듈에는 assert 문이 없다 (있는 두 곳은 `plastic_coverage._audit_l1` ·
  `mpm_lab_register._selftest` — 탐침 경로 밖) · 파이프라인 하위 프로세스는 `-O` 를 물려받지 않는다.

| S0b 변이 (`--smoke-root`) | 핀 rc · S0 / S0b | 고친 트리 (-O) rc · S0 / S0b |
|---|---|---|
| positive (제출 WSL 기록 그대로) | 0 · ✓ / ✓ | (기록 없음 — 위 ⚠) · 같은 기록의 생산자 판정 = ⑤ FAIL |
| marker_missing | 1 · ✗ | 1 · ✗ |
| marker_unknown | **0** · ✓ / ✓ | 1 · ✗ / ✗ (미등록 표지) |
| checks_missing · checks_three · check_fail | 1 · ✓ / ✗ | 1 · ✓ / ✗ |
| one_check_repeated_four | **0** · ✓ / ✓ | 1 · ✓ / ✗ |
| negctl_missing · tau_numeric · ionic_residual_bad | **0** · ✓ / ✓ | 1 · ✓ / ✗ |
| raw_sha_fail | **0** · ✓ / ✓ | 1 · ✓ / ✗ |
| unexpected_failure_record | **0** · ✓ / ✓ | 1 · ✓ / ✗ |
| real_failure_path_synthetic_input | **0** · ✓ / ✓ | 1 · ✓ / ✗ |

- B2 — `r5_case15_fault_reread` 를 한 번 더: 그 탐침이 입력 JSON 에서 쓰는 것은 `cases` 의 정상 게시 폴더 셋뿐이라, 같은 실행의 `marker_missing` 다시 읽기 JSON
  (같은 폴더 셋 · K1–K7 · H1 통과) 을 그 자리에 복사했다 (입력 대체 · 표지).  결과: 탐침 rc 0 · 출력 "Actual child-case PermissionError reread **rc 1**" —
  S0 ✓ (정상 셋) · **S0b ✗**: 기록된 `case15.nc5_attempt` = TECH · 공용 판정 재계산 `case15.proc` = FAIL (탐침이 만든 보고에 `timings` 없음).  핀 = rc 0 · S0b PASS.

## 해석

- **옛 기록은 이제 통과하지 못한다 (의도)**: 제출 WSL 10-07 case15 기록 · 그 기록으로 만든 positive 는 실제 시도 증거 (`attempt_evidence`) 와 검사 안정 ID 가 없다 →
  생산자 ⑤ = FAIL · S0b = ID 집합 불일치 + 재계산 불일치.  수정 계획 §3 표의 "positive (제출 기록 그대로) rc 0" 기대는 이 필수 검사로 **대체됐다** — 고친 스모크로
  case15 를 다시 돌린 기록이 양성이다 (WSL 사전 점검 3).
- 탐침이 직접 만든 스모크 보고는 `timings` 를 싣지 않는다 — 소비자는 자식 프로세스 검사를 다시 판정할 상세가 없으니 실패로 본다 (상세 결손 = FAIL · 실제 `run_smoke` 보고는
  늘 `timings` 를 싣는다).  그래서 변이마다 **제 사유로** 거부되는지는 탐침 대신 시험이 보인다:
  `scripts/g2_network_reread.py --selftest` (양성 = 실제 case15 값의 기록 + 고친 스모크 생산자 evaluate 의 검사 일곱 · timings — Codex 변이 일곱 · 회귀 다섯 · 신원 · ID 넷 ·
  23/23) · `scripts/wsl_network_smoke.py --selftest` 마지막 묶음 (실제 case15 (a) 망 CLI 만 PermissionError = TECH · rc 1 / (b) 주입 없음 = rc 0 · 7/7 → 이 도구
  `--smoke-root` rc 0 · 20/20).
- 판정 근거 · 범위: 이 재실행은 **Codex 탐침이 고친 트리에서 어떻게 끝나는가**의 확인이다 — 194 생산 · WSL 실덤프 · S3 · DEM/MPM 을 다시 돌린 것이 아니다 · 봉인 32 무변경.
