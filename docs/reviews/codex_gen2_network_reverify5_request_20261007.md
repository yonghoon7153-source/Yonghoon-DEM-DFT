# Codex 재검증 5 요청 — 접촉망 세대 2 · G2RR4-01 · 02 · 03 수정 (10-07)

- **대상**: 브랜치 `claude/stoic-knuth-NObVQ` · **이 요청서가 들어간 커밋** (핀은 1저자가 보낼 때 그 커밋 sha 로).  **발송 = 1저자**.
- **앞 판정**: `docs/reviews/codex_review_gen2_network_reverify4_20261007.md` (핀 `87f0906a2` · 194 · v1.3 HOLD · 새 P1 없음 · 새 P2 `G2RR4-01` · `G2RR4-02` · P3 `G2RR4-03`) ·
  우리 트리 재현 = 판정값 차이 0 (`docs/reviews/codex_gen2_network_reverify4_evidence_20261007/_README_import.md` §2).
- **1저자 비준**: 10-07 *"같이 병행해서 진행해용"* (반입 + 수정 병행 · 반례 먼저).  ⬜ 등록 기대를 바꾸는 제안 (§3 · 등록 §3b · §4 · §9-4) 의 비준은 **아직** — 비준 전에는 효력 없음.
- **봉인**: 32 파일 · `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` **그대로** (판정문 §7-4 — 단계 호출부 · 봉인 워커 · `webapp/app.py` · 망 솔버는 고치지 않았다 ·
  단계 기록은 봉인 워커가 이미 싣던 것을 읽는다).  고친 파일 = 실행기 (`scripts/run_network_194_parallel.py`) · 다시 읽기 (`scripts/g2_network_reread.py` · 인계 도구 지문이 바뀐다 — 발사 때 기록) ·
  배포 생성기 (`scripts/lhs_release_build.py`) · 스모크 (`scripts/wsl_network_smoke.py`) · 시험 · 등록 문서 (제안 표지 · 원문 보존).
- **이 요청에 붙일 것 (1저자 · WSL · 고친 도구로 · 각 원 프로세스 rc 와 받은 그대로의 출력 — 무엇을 받았는지 목록으로 · SELF-94)**:
  ① 기존 시범 ROOT (`~/g2pre_pilot_c3117438a_1007_1415` — 원본은 건드리지 않는다 · 감사 · 다시 읽기는 읽기만) 를 고친 실행기 `audit --json` · 고친 다시 읽기 `--launcher-root … --expect-set pilot3 --json` 로 다시 —
  기대 (제안): audit rc 0 · 시작 15 = 끝맺음 15 · 완료 시도 3 · `stage_binding` 3 (옛 실행기 시도라 지금 케이스 기록 stages 로 결합 · 케이스마다 워커 + parser · contact · coverage · network_cli) ·
  관측 문제 [] / 다시 읽기 rc 0 (상세 계약 통과).  ② 등록 §1 단계 3 · 4 (스모크 · `--smoke-root` 다시 읽기) — case15 `[음성 대조]` 넷 PASS · S0 · S0b (등록 §9-4 ③ 제안 기대).
  ③ (원하면) 새 시범 pilot3 `--observe-imports` — 시도 기록에 `stage_plan` 이 실리고 감사 결합의 출처가 그 사본인지.
  ① 의 명령 (등록 §1 단계 0 의 체크아웃 · `$PY` 뒤 · 출력 JSON 은 ROOT 밖 홈에 — audit · 다시 읽기는 `--json` 경로 말고는 쓰지 않는다):

```bash
OLD=~/g2pre_pilot_c3117438a_1007_1415; T=$(date +%m%d_%H%M)
$PY scripts/run_network_194_parallel.py audit --root "$OLD" --json ~/g2rr4_oldpilot_audit_$T.json 2>&1 | grep -v '^  lhs' | tail -12; echo "audit rc=${PIPESTATUS[0]}"
$PY -c "import json,sys; a=json.load(open(sys.argv[1])); o=a['import_observation']; b=o['stage_binding']['attempts']; print(o['n_started'], o['n_finalized'], len(o['completed_attempts']), len(b), a['import_observation_problems']); [print(k, v['plan_source'][:40], v['expected'], v['observed']) for k, v in sorted(b.items())]" ~/g2rr4_oldpilot_audit_$T.json
$PY scripts/g2_network_reread.py --launcher-root "$OLD" --expect-set pilot3 --json ~/g2rr4_oldpilot_reread_$T.json 2>&1 | tail -14; echo "reread rc=${PIPESTATUS[0]}"
```

## 1. G2RR4-01 — 다시 읽기 상세 ↔ 요약 · 감사 관측 내부 ↔ 최상위 (`942e851fd`)

| 판정문 최소 해결 증거 (§2) | 구현 |
|---|---|
| ① meta/cases/checks 필수 구조 · bool · 상세 실패 재계수 = n_fail · 필수 검사 이름/범위 = 스키마 계약 (빈 checks 공집합 PASS 금지) | 계약 한곳 `g2_network_reread.launcher_detail_problems` — 생산자 상수가 곧 계약 (케이스마다 K1–K7 한 번 · 선택 K1b · meta M0 · M-plan · M-reg · M3 한 번 + 코호트마다 M1 · M2 · H1 한 번) · 항목 name 문자열 · ok **bool** · 모르는 ID 거부 · 상세 실패 재계수 = n_fail · 상세 실패 하나라도 = 문제 → `lhs_release_build.v13_reread_problems` 가 그 함수를 부른다 (사본 없음) · 기록 스키마 v3 그대로 (검사만 늘었다) |
| ② 상세 (case, cohort) 고유 집합 = 등록 194 · read_n · set_equal 일치 | 같은 함수 — 중복 쌍 · 고유 집합 = 등록 production194 쌍 · 케이스 수 = read_n · M3 칸 (expected_n · read_n · set_equal · missing · extra) = 최상위 |
| ③ 감사 관측 내부 실패 · 봉인 밖 모듈을 성공 요약이 못 덮게 · 관측 필수 배치는 관측 객체 결손도 거부 | `v13_audit_observation_problems` — 관측 객체 problems · outside = 목록 · 빈 목록 · 최상위 `import_observation_problems` 에 다 실림 · 프로세스 수 정수 · 생산 194 = 배치 manifest `observe_imports` true · 관측 객체 있음 · 프로세스 > 0 · 관측된 완료 시도 ⊇ 등록 케이스 · 단계 결합 기록 (§2) |
| ④ 정상 · 결손 · 모순을 build · check 둘 다 · 상세 없는 옛 정상 픽스처를 정상으로 두지 않는다 | 시험 정상 픽스처 = 상세 꼴 (meta 10 · 194 케이스 × K1–K7 · 관측 객체 · `stage_binding` · `observe_imports`) · build_v13 · 단계 A · check_v13 = 같은 관문 함수 |

- 시험: `scripts/test_lhs_release_v13.py` 옛 코드 137/167 → **167/167** (V18 = Codex 변이 넷 [C] + 같은 부류 18 = build 거부 · 산출 없음 · check_v13 재판정 6 (위조한 빌드 기록도) · V18a 상세 정상 대조 생성) ·
  `g2_network_reread --selftest` 17/19 → **19/19** (실 생산자 JSON — pilot3 · 합성 production194 — 가 상세 계약을 통과 · 변이 넷 = 문제).
- Codex `release_gate` 무변경 = 8 변이 **전부 거부 — control 도** (그 탐침은 모든 변이의 meta · cases 를 최소 꼴로 덮어써서 상세 계약의 필수 ID 결손) → 같은 변이를 고친 트리 상세 픽스처 위에 넣은 파생 탐침 = control **생성 · check 문제 0** · 나머지 **거부 · 산출 없음** (§4).

## 2. G2RR4-02 — 실행 단계 ↔ 관측 영수증 결합 (`4c8f84928`)

| 판정문 최소 해결 증거 (§3) | 구현 |
|---|---|
| ① 완료 시도별 실행 단계 · 프로세스 계획 = 훅 밖 호출부 기록 · 실행 / 정당한 생략 구분 · 실행된 단계 = 시작 · 끝 둘 다 | 계획 = 워커 케이스 기록 `out/status.json cases[<c>].stages` (봉인 워커 `scripts/lhs_webapp_batch.py` 가 `app.run_pipeline` 의 단계 기록을 이미 싣는다) → 실행기가 시도 기록 `worker.json attempts[].stage_plan` 에 사본 · 옛 실행기 ROOT = 지금 기록을 쓴 시도 (봉인 판정 행 · record_sha 결합) 의 그 기록.  단계 이름 표 — 실행 (Parse · hybrid → `parse_liggghts` · Bimodal Contact Analysis → `analyze_contacts_bimodal` · Contact Analysis → `analyze_contacts` · Coverage Physics vs Hertzian → `coverage_physics_vs_hertzian` · Network Solver (both modes) → `network_conductivity`) / 정당한 생략 (Parse (CSV fallback) · LOCK 미획득) / 실행 프로세스 안 단계 9 / **표 밖 = 분류 밖 = 거부** |
| ② "프로세스 5 개" 금지 · 단계 · 시도 · 실행 신원 일치 · 단계별 쌍 결손 음성 대조 | 완료 시도마다 실행 단계마다 그 스크립트가 `__main__` 인 **끝맺은** 프로세스 정확히 그 수 + 워커 하나 — 모자람 (쌍 결손) · 중복 (다른 단계 결손을 못 메운다) · 계획 밖 프로세스 · 계획 없음 · 시도 사본 ≠ 지금 기록 = 문제 · 신원 (run_id · 케이스 · run · 시도) 은 G2RR3-02 그대로 · 결합 기록 = audit JSON `import_observation.stage_binding` (`np194_import_obs/stage_binding/v1`) → v1.3 배포 (생산 194) 는 결합 기록 필수 · 결합된 시도 = 관측된 완료 시도 |
| ③ 훅을 건너뛰는 실행 옵션 · 환경 제거 · fork = 금지 또는 다른 계측 | `-I` · `-E` · `-S` 로 뜬 단계 = 영수증이 없다 → ① ② 가 결손으로 거부 · fork · 프로세스 풀 API 정적 검사 (봉인 경로 · 지금 0 줄 · 있으면 발사 사전 점검 ⛔) |
| ④ Q2 예외 유지 | 완료 아닌 시도의 미최종 = 정보 · 결합하지 않는다 (시험 = 죽은 시도 + 재시도 rc 0 · 재시도만 결합) |

- 시험: 실행기 `--selftest` 옛 코드 102/112 → **114/114** (가짜 워커 = 생산 워커와 같은 단계 하위 프로세스 넷 · ㉟g = Codex 변이 그대로 5/4 · 4/4 · 2/2 · 5/5 + 분석 · 피복 쌍 · 중복으로 메우기 ·
  분류 밖 단계 · 시도 사본 ≠ 지금 기록 · 옛 실행기 ROOT 꼴 · 정당한 생략 · Q2 · ㉟g0 단계 이름 표 ↔ `webapp/app.py` 문자열 · fork 검사) · `test_lhs_release_v13` 168/173 (V19 5 FAIL) → **173/173**.
- Codex `observation_cli` 무변경 = 네 행 rc 1 — 사유 전부 "완료 시도의 실행 단계 기록이 없다" (그 합성 픽스처 = 재검증 3 의 옛 실행기 ROOT · 케이스 기록에 stages 가 없다 → 5/5 도 거부 = 단계 증거 없이 통과시키지 않는 설계) ·
  `submitted_evidence` 무변경 = 경로 번역 기준선에서 assert (그 사본 · 보충 묶음 둘 다 케이스 기록 `out/status.json` 이 없다 → 같은 사유 3).  ⇒ 단계 기록이 있는 같은 반례 = 파생 탐침 (§4) — 핀 rc 0 · 1 · **0 · 0** → 고친 트리 rc 0 · 1 · **1 · 1**.
- 관찰 (시험 아님): 10-07 14:15 WSL 스모크 기록의 같은 세 케이스 (lhs00_055 · lhs00_128 · lhsx_007 · 같은 워커 · stop_after network) 단계 목록 = 표로 전부 분류 (분류 밖 0) ·
  실행 단계 parser · contact (bimodal 2 · mono 1) · coverage · network_cli = 판정문 §3 의 케이스당 영수증 다섯 (워커 + 넷) 과 같은 모양.  실제 pilot ROOT 결합은 머리 ① 로 확인한다.

## 3. G2RR4-03 — 194 본 실행 관측 필수 · case15 음성 대조 (`36ba39070` · `a51e61b05`)

| 판정문 요구 (§4 Q3 · §6-3(b) · §7-3) | 구현 |
|---|---|
| 본 실행 `--observe-imports` 필수 · 등록 문구 · 명령 일치 | 실행기 — 계획 큐 = 등록 production194 (커밋된 수확 폴더 열거 · 지문) 인데 관측 없음 = 발사 사전 점검 ⛔ (아무것도 안 띄운다 · `--dry-run` 에도 보인다) · 관측을 끈 생산 manifest = 감사 rc 1 (역사 형식 = 이 요구 전 실행이라 면제) · 사용 예 명령에 `--observe-imports`.  등록 §3b · §4 = **제안** (원문 보존 · ⬜ 1저자 비준) |
| 시작 직전 · 완료 뒤 manifest 확인 | 등록 §4 제안 명령 — dry-run `--observe-imports` (⛔ · fork 줄) · 본 실행 · 시작 직후 · 완료 뒤 `manifest.json` 의 `observe_imports` · `import_obs_run_id` · 감사 관측 문제 0 · `stage_binding` 194 시도 |
| 관측 필수 배포 = observe_imports false · 관측 객체 없음 거부 | §1 ③ |
| case15 = 원 실패 보존 + 변경 이력 + 지정한 실패가 실제 발화하는 음성 대조 (whitelist · 이름 PASS · 소급 수정 금지) | 등록 §9-4 변경 이력 (제안) — ① 관측 필수 ② case15 기대 = 원 실패 (§9-2) 그대로 · 사유 *"이온 단독 성공을 전체 채널 성공으로 잘못 예상했다"* (`SELF-92`) ③ 다음 사전 점검 기대 ④ 코드 신원 · 봉인 불변.  스모크 `CASE15_NEGCTL` — `[음성 대조]` 넷: ① 게시 차단 (failed · 실패 단계 = 망 솔버 · Stage E 없음 · 반환 run id 없음) ② τ 세 모드 NOT_COMPUTED · 숫자 칸 없음 ③ 원인 발화 (업로드 폴더 원덤프로 실제 `build_network` · `solve_network` — 전자 두 모드 · Hertz 열 = `boundary_overlap` · B∩T = 입자 ID 24 · 40 · 57 · 103 · Physics 열 = 음수 원자료 면적 거부 · 음수 행 둘 31–29241 · 38–29241) ④ 이온 정상 (두 모드 computed · σ_ratio 8 자리 0.00032635 · 0.00036225 · 증서 · 잔차 < 1e-6).  다시 읽기 `--smoke-root` = 음성 대조 표지 케이스만 S0 에서 빼고 S0b (게시 없음 ∧ `[음성 대조]` 판정 넷 이상 전부 PASS) · 표지 없는 failed = S0 실패 그대로 (이름 면제 없음) |

- 시험: 실행기 `--selftest` ㉟h 옛 코드 114/117 → **117/117** · `wsl_network_smoke --selftest` 11/14 → **14/14** (커밋된 case15 원자료 직접 6 조합 · 21 s) · `g2_network_reread --selftest` 19/20 → **20/20**.
- 덤 대조 (기록만 · 소급 판정 아님): 10-07 14:15 WSL 스모크의 case15 기록 (게시 차단 · τ NOT_COMPUTED) + 커밋된 원자료 직접 풀이 = 새 `[음성 대조]` 넷 PASS.  다음 WSL 스모크 실측 = 머리 ②.

## 4. Codex 탐침 — 고친 트리 재실행 (`docs/reviews/codex_g2rr4_fix_probe_rerun_20261007/`)

판정 묶음을 리포 밖 새 폴더에 다시 세워 (source = `git archive` · submitted = 리포의 사전 점검 tar) Codex 다섯 탐침을 **무변경**으로 · 파생 탐침 둘 (각 파일 머리에 다른 줄) · 회귀 넷을 돌린다 — 핀 · 고친 트리 같은 driver (README · 결과 JSON).

| 탐침 | 핀 `87f0906a2` | 고친 트리 `a51e61b05` |
|---|---|---|
| release_gate (무변경) | control 생성 · 넷 거부 · **M2 ok=false · cases=[] · 감사 관측 = 생성** | 8 전부 거부 (control 도 — 최소 꼴의 검사 ID 결손) |
| release_gate_detailed (파생 · 상세 픽스처) | — (핀 픽스처에 상세 꼴 없음) | **control 생성 · check 문제 0** · Codex 변이 7 + 같은 부류 1 (관측 객체 그대로 · 내부만 실패) = **8 거부 · 산출 없음** |
| observation_cli (무변경) | rc 0 · 1 · **0 · 0** | rc 1 · 1 · 1 · 1 (단계 기록 없음) |
| observation_cli_staged (파생 · 단계 기록만 더함) | rc 0 · 1 · **0 · 0** | rc 0 · 1 · **1 · 1** (parse_liggghts 0/1 · 단계 셋 0/1) |
| submitted_evidence (무변경) | 기준선 문제 0 | assert — 기준선 "단계 기록 없음" 3 (사본에 케이스 기록 없음) → 머리 ① |
| case15_channels · scope194 (무변경) | 판정값 = Codex 와 같음 (case15 이온 CG 끝자리만 · 반입 기록 §2) | **핀 재실행과 JSON 전체 동일** (봉인 무변경 · 같은 환경) |
| reread · publication · role · release | 17/17 · 32/32 · 44/44 · 134/1 | 20/20 · 32/32 · 44/44 · 172/1 (FAIL = V16a 만 — git archive 사본에 `.git` 없음 · checkout 에서는 173/173) |

## 5. 질문

- **Q1 (G2RR4-01).** 상세 계약 = 생산자 상수 (검사 ID 목록) 를 그대로 계약으로 — 모르는 ID 거부 · K1b 만 선택.  생산자가 검사를 더하면 계약도 같이 바뀐다 (한곳).  판정문 §2 ①–④ 를 닫나?
- **Q2 (G2RR4-02 ①).** 단계 계획의 출처 = 봉인 워커가 이미 싣던 케이스 기록 `stages` (실행기는 시도 기록에 사본만).  "훅 바깥의 호출부 기록" 으로 충분한가 — 우리 판단: 영수증 동시 소실 부류
  (판정문 §3) 는 닫지만, 워커가 거짓 단계 기록을 쓰는 경우는 판정문이 범위 밖으로 둔 "모든 기록을 고친다" 부류로 남는다.
- **Q3 (옛 실행기 ROOT).** 기존 pilot3 재감사는 지금 케이스 기록 (봉인 판정 행의 시도 = record_sha 결합) 으로 결합한다 · 새 ROOT 는 시도 사본 ↔ 지금 기록 대조까지.  이 대체 경로를 받나?
- **Q4 (표 밖 = 거부).** 표는 194 실행기 경로 (stop_after='network') 만 담는다 — 스모크 일반 경로 대조군의 'Stage E (literature-grounded grain corrections)' 는 실행기 경로가 아니라 표에 없다 (나오면 거부).  이 한정에 동의하나?
- **Q5 (§3 ③).** fork 정적 검사 (multiprocessing · os.fork · ProcessPoolExecutor · posix_spawn · os.spawn* · pty.fork 문자열 · 봉인 경로) + 훅 우회 단계 = 영수증 결손으로 거부 — 충분한가?  하위 프로세스 (subprocess) 는 결합이, 동적 import 는 관측 (봉인 밖 모듈 = 문제) 이 잡는다.
- **Q6 (G2RR4-03).** 등록 제안 (§3b · §4 · §9-4) 을 1저자가 비준하면 판정문 §7-3 이 닫히나 — 남는 것이 있으면 목록.
- **Q7 (case15 음성 대조).** `[음성 대조]` 넷의 범위 · 기준 (③ 원인 = 업로드 폴더 원덤프 직접 풀이 — 파이프라인 시도 기록은 끝 300 자라 (`WEB-05`) 원인을 다 못 담는다 · ④ 이온 = 8 자리 반올림 + 증서 잔차 1e-6) 이 적절한가?
- **Q8 (발사 전).** 머리 ①–③ 의 WSL 재확인 · 1저자 비준 뒤 194 발사 전에 남는 것 — 판정문 §7-5 · 7-6 (저자 발사 승인 · 새 ROOT · 완료 뒤 SEALED194 · production194 상세 재독해 · 인계/배포 검사) 밖에 있나?

## 6. 정정 (`SELF-94`)

- 재검증 4 요청서 §4 끝 줄의 *"전체 출력 (판정문 §8-4) … 보충 묶음 = ✅ 받음"* 은 과장이었다 — 보충 묶음이 채운 것 = 자체 시험 전문 둘 · 시범 3 워커 로그 · 영수증 · run 기록.
  전체 dry-run 원 stdout · 전체 스모크 stdout · 게시된 dual/full_metrics 원파일 일체는 받지 않았다 (판정문 §5).  요청서 4 는 발송본 그대로 두고, 사전 점검 README §4 · §5
  (`docs/reviews/codex_gen2_network_reverify4_precheck_20261007/README.md`) · 등록 §9-2 에 정정 표지를 달았다 (원문 보존).
- 사전 점검 README §2 · 등록 §9-2 의 case15 음수 면적 **한 행** 서술 (−0.186036 µm² 간선) 도 **두 행** (31–29241 −0.186036 · 38–29241 −0.186264 µm² · Physics 는 첫 행에서 멈춘다 ·
  판정문 §6-1) 으로 정정 표지 (원문 보존).
