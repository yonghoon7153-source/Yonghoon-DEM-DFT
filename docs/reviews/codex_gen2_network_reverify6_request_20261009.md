# Codex 재검증 6 요청 — 접촉망 세대 2 · G2RR5-01 · 02 · 03 · 04 수정 + 등록 비준 (10-09)

- **대상**: 브랜치 `claude/stoic-knuth-NObVQ` · **이 요청서가 들어간 커밋** (핀은 1저자가 보낼 때 그 커밋 sha 로).  **발송 = 1저자**.
- **앞 판정**: `docs/reviews/codex_review_gen2_network_reverify5_20261007.md` (핀 `aa7ec7fe9` · 194 · v1.3 HOLD · 새 P1 없음 · P2 `G2RR5-01` · `02` · `03` · P3 `G2RR5-04`) ·
  우리 트리 재현 = 판정값 차이 0 (`docs/reviews/codex_gen2_network_reverify5_evidence_20261007/_README_reproduction.md`).
- **1저자 비준**: 10-08 밤 *"권고대로해"* = 수정 계획 `docs/reviews/g2rr5_fix_plan_20261008.md` Q1–Q4 (+ Q5 — G2RR3-02 닫은 근거를 이 요청서에 적는다) ·
  10-09 *"비준이야"* = Q6 (결합 기록에 분류 밖 단계 칸) · Q7 (스모크 실제 case15 묶음을 `--selftest-real` 로 나눔) · Q8 (등록 §3b · §4 · §9-4 제안 + G2RR5-04 덧붙임을 한 번에 — 등록 §9-6).
- **봉인**: 32 파일 · `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` **그대로** (봉인 32 파일 무변경 · 고친 트리에서 다시 잰 지문 같음).
  고친 파일 = 실행기 (`scripts/run_network_194_parallel.py`) · 다시 읽기 (`scripts/g2_network_reread.py`) · 배포 생성기 (`scripts/lhs_release_build.py`) · 스모크 (`scripts/wsl_network_smoke.py`) · 시험 · 등록 문서.
  **인계 도구 지문 바뀜** (판정문 §7-5 "기록한다"): `scripts/g2_network_reread.py` sha256 `adecb782866a7891…1aba67` (핀 `aa7ec7fe9`) → `71945dab069f87c4…9486dd` (`8d58c9d23`) ·
  `scripts/lhs_design_dataset.py` 무변경 — 발사 때 manifest `handover_code_hashes` 에 실린다.
- **이 요청에 붙일 것 (1저자 · WSL · 고친 도구로 · 각 원 프로세스 rc 와 받은 그대로의 출력 — 무엇을 받았는지 목록으로 · `SELF-94`)** = 아래 명령 블록의 묶음 (수정 계획 Q4 범위 — 새 pilot3 · 194 는 돌리지 않는다):
  ① 도구 자체 시험 넷 (Q7 — `--selftest-real` 포함) ② 고친 스모크 (case15 실제 = 새 실제 시도 검사 포함) ③ 다시 읽기 `--smoke-root` (S0 · S0b)
  ④ 기존 시범 ROOT 둘을 고친 실행기로 **읽기 전용** 재감사 (옛 v1 결합 기록은 이제 배포 관문이 거부 — Q6) ⑤ 그 감사 JSON 을 고친 배포 관문 함수로 **읽기만** (`stage_binding` 시도별 값 · 합계).

```bash
# ── 0. 체크아웃 (등록 §1 단계 0 그대로 · detached · 깨끗한 트리) ──
cd ~/dem-audit
git fetch origin claude/stoic-knuth-NObVQ
git checkout --detach origin/claude/stoic-knuth-NObVQ
git log -1 --oneline
echo "dirty 줄 수 = $(git status --porcelain --untracked-files=no | wc -l) (0 이어야)"
PY=$(ls ~/Yonghoon-DEM-DFT/venv/bin/python ~/Yonghoon-DEM-DFT/.venv/bin/python3 2>/dev/null | head -1)
$PY -c "import numpy, scipy, networkx; print(numpy.__version__, scipy.__version__, networkx.__version__)"
S=$(git rev-parse --short HEAD); T=$(date +%m%d_%H%M)
DL=/mnt/c/Users/Administrator/Downloads        # 다른 PC 면 /mnt/c/Users/안용훈/Downloads
O=~/g2rr6_${S}_$T; mkdir -p "$O"               # 이번 출력 전부 (ROOT 밖)
P1=~/g2pre_pilot_c3117438a_1007_1415           # 옛 실행기 시범 (10-07 14:15) — 읽기만
P2=~/g2pre_pilot_839dbac6b_1007_2224           # 새 실행기 시범 (10-07 22:24 · --observe-imports) — 읽기만
for P in "$P1" "$P2"; do find "$P" -type f -printf '%P %s %T@\n' | sort | sha256sum > "$O/$(basename "$P").before"; done

# ── 1. 도구 자체 시험 (Q7 — 스모크 실제 case15 묶음 = --selftest-real · ≈ 1–2 분) ──
$PY scripts/g2_network_reread.py --selftest > "$O/st_reread.txt" 2>&1; echo "st_reread rc=$?"; tail -2 "$O/st_reread.txt"
$PY scripts/run_network_194_parallel.py --selftest > "$O/st_runner.txt" 2>&1; echo "st_runner rc=$?"; tail -2 "$O/st_runner.txt"
$PY scripts/wsl_network_smoke.py --selftest > "$O/st_smoke.txt" 2>&1; echo "st_smoke rc=$?"; tail -2 "$O/st_smoke.txt"
$PY scripts/wsl_network_smoke.py --selftest-real > "$O/st_smoke_real.txt" 2>&1; echo "st_smoke_real rc=$?"; tail -3 "$O/st_smoke_real.txt"

# ── 2. 고친 스모크 — 실덤프 (등록 §1 단계 3 과 같은 인자 · 새 ROOT) ──
SM=~/g2pre_smoke_${S}_$T
$PY scripts/wsl_network_smoke.py --root "$SM" --skip-real14-general --lhs-case lhs00_055 --lhs-case lhs00_128 --lhs-case lhsx_007 > "$O/smoke.txt" 2>&1; echo "smoke rc=$?"; tail -40 "$O/smoke.txt"
$PY -c "import json,sys; r=json.load(open(sys.argv[1])); [print(c.get('id'), c['verdict']) for c in r['checks'] if str(c.get('name','')).startswith('case15_network:')]; print('report rc', r['rc'])" "$SM/smoke_report.json"

# ── 3. 다시 읽기 --smoke-root (S0 · S0b) ──
$PY scripts/g2_network_reread.py --smoke-root "$SM" --json "$SM/reread.json" > "$O/smoke_reread.txt" 2>&1; echo "smoke_reread rc=$?"; tail -25 "$O/smoke_reread.txt"

# ── 4. 기존 시범 ROOT 둘 — 고친 실행기 재감사 (읽기 전용 · JSON 은 ROOT 밖) ──
for P in "$P1" "$P2"; do n=$(basename "$P")
  $PY scripts/run_network_194_parallel.py audit --root "$P" --json "$O/audit_$n.json" > "$O/audit_$n.txt" 2>&1; echo "$n audit rc=$?"
  grep -v '^  lhs' "$O/audit_$n.txt" | tail -12
done

# ── 5. 고친 배포 관문 함수로 그 감사 JSON 을 읽기만 (G2RR5-01 · Q6 — 진단: 관측 필수 집합에 pilot3 를 더해 생산 194 와 같은 관측 검사를 건다) ──
$PY - "$O/gate_readonly.json" "$P1=$O/audit_$(basename "$P1").json" "$P2=$O/audit_$(basename "$P2").json" > "$O/gate_readonly.txt" 2>&1 <<'PY'
import json, os, sys
sys.path.insert(0, 'scripts')
import lhs_release_build as R
R.V13_IMPORT_OBS_REQUIRED = tuple(R.V13_IMPORT_OBS_REQUIRED) + ('pilot3',)   # 진단 — 시범 셋에도 관측 필수 검사 (stage_binding 시도별 값 · 합계)
res = {}
for pair in sys.argv[2:]:
    root, aj = pair.split('=', 1)
    a = json.load(open(aj))
    ident, ip = R.v13_batch_identity(root)
    obs = R.v13_audit_observation_problems(a, ident, 'pilot3')
    full = R.v13_audit_problems(a, root, ident=ident, expect_set='pilot3')
    sb = (a.get('import_observation') or {}).get('stage_binding') or {}
    at = sb.get('attempts') or {}
    n = os.path.basename(root.rstrip('/'))
    res[n] = dict(identity_problems=ip, observation_problems=obs, audit_problems=full, schema=sb.get('schema'), attempts=at)
    print(n, '| 신원 문제', len(ip), '| 관측 문제', len(obs), obs[:2], '| 감사 관문 문제', len(full), full[:2], '| 스키마', sb.get('schema'), '| 결합 시도', len(at))
    for k, v in sorted(at.items()):
        print('   ', k, str(v.get('plan_source'))[:22], 'expected=observed' if v.get('expected') == v.get('observed') else f'≠ {v.get("observed")}', 'unclassified', v.get('unclassified'))
json.dump(res, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
PY
echo "gate_readonly rc=$?"; cat "$O/gate_readonly.txt"
for P in "$P1" "$P2"; do find "$P" -type f -printf '%P %s %T@\n' | sort | sha256sum | diff -q - "$O/$(basename "$P").before" > /dev/null && echo "$(basename "$P") 파일 변화 없음" || echo "$(basename "$P") ⚠ 바뀜"; done

# ── 6. 묶음 (이번 출력 전부 + 스모크 보고 · 판정 JSON — 케이스 결과 원본은 빼고) ──
cp "$SM/smoke_report.json" "$SM/smoke_summary.txt" "$SM/reread.json" "$O/" 2>/dev/null; git log -1 --format='%H %cI' > "$O/commit.txt"; echo "$PY" > "$O/python.txt"
cd ~ && tar czf ~/$(basename "$O").tar.gz "$(basename "$O")" && cp ~/$(basename "$O").tar.gz "$DL/" && ls -la ~/$(basename "$O").tar.gz
```

**붙여 넣을 것** — 0 단계 세 줄 (커밋 · dirty 줄 수 · 버전) · 1–5 단계의 `rc=` 줄과 화면 끝 · 끝의 "파일 변화 없음" 두 줄 · 묶음 파일 (다운로드 폴더) 첨부.

**기대 (결과 전 등록 — 다르면 그대로 보고 · 고르지 않는다)**

| 단계 | 기대 |
|---|---|
| 0 | 커밋 = 이 요청서가 들어간 커밋 이후 · dirty 0 |
| 1 | `st_reread rc=0` (23/23) · `st_runner rc=0` (124/124) · `st_smoke rc=0` (16/16) · `st_smoke_real rc=0` (4/4) — 숫자 = 이 컨테이너 실측 (10-08 · 10-09) |
| 2 | `smoke rc=0` · case15 검사 **일곱** = `case15.proc` · `case15.raw_sha` · `case15.nc1_blocked` · `case15.nc2_tau` · `case15.nc3_cause` · `case15.nc4_ionic` · `case15.nc5_attempt` 각 한 번 · 전부 PASS (`nc5_attempt` = 이번 망 CLI 시도 1 회 · 예외 없음 · rc 0 · per-mode 둘 · 실패 채널 = 등록 넷 · 이온 computed 둘 — 등록 §9-6 ②) · real14 · LHS 셋 = 10-07 22:24 와 같은 값 (`lhs00_055` · `lhsx_007` 두 모드 computed · `lhs00_128` valid_zero) · `report rc 0` |
| 3 | `smoke_reread rc=0` — S0 (case15 = 등록 표지로 S0 에서 빠짐) · **S0b** = 등록 표지 · 필수 ID 일곱 정확히 · 전부 PASS · 공용 판정 (`case15_negctl_verdicts`) 재계산 = 기록 · 게시 없음 · 나머지 네 케이스 K1–K7 · H1 ✓ |
| 4 | 두 ROOT `audit rc=0` · SEALED 3 · 관측 줄 = 시작 15 · 끝맺음 15 · 완료 시도 3 · `✗` 줄 없음 |
| 5 | `gate_readonly rc=0` · 두 ROOT 모두 신원 문제 0 · 관측 문제 0 · 감사 관문 문제 0 · 스키마 `np194_import_obs/stage_binding/v2` · 결합 시도 3 · 시도마다 expected=observed · unclassified `[]` · 계획 출처 = `c3117438a` 시범은 지금 케이스 기록 (`out/status.json …` — 옛 실행기 ROOT 의 대체 경로 · 재검증 5 Q3) · `839dbac6b` 시범은 시도 사본 (`worker.json attempts[].stage_plan …`) · 두 ROOT "파일 변화 없음" |

- 컨테이너 예행 (참고 · 판정 아님 · 10-09): 재검증 5 사전 점검 묶음 (`docs/reviews/codex_gen2_network_reverify5_precheck_20261007/g2rr5_839dbac6b_1007_2224.tar.gz`) 의 `839dbac6b` 시범 사본에 4 · 5 단계를 돌렸다 —
  결합 기록 v2 · 시도 3 · 계획 출처 = 시도 사본 · expected=observed · unclassified `[]` · **관측 문제 0** · 사본 파일 변화 없음.  감사 rc 1 · 감사 관문 문제 4 는 환경 탓 (묶음에 게시 산출물 · 원자료 · 워커 체크아웃이 없다 — `not_merged` 3 · 레코드 세대 `missing` 3 · 입력 지문 2 · `code_root_changed_now` 32) — WSL 에서는 그 셋이 있다.

## 1. G2RR5-01 — 배포 관문이 `stage_binding` 의 시도별 값을 읽는다 (`8b6453671` · 잔여 `7153a7d6a`)

| 판정문 §1 최소 해결 증거 | 구현 |
|---|---|
| 공용 배포 관문에서 시도 값의 구조 · expected/observed 카운터 · bool 아닌 유효 정수 · 단계 · 개수 일치 | 생산자 계약 한 함수 `run_network_194_parallel.stage_binding_record_problems(key, rec)` (dict · 키 집합 정확히 · 계획 출처 = 실행기의 두 문자열 · `executed` = 단계 열쇠 · `in_process` 0 이상 정수 · expected · observed = {워커 · 단계 스크립트: 정수 (bool 아님)} · expected = 워커 1 + `executed` 에서 **다시 유도** · 필수 역할 워커 1 · 망 솔버 ≥ 1 · observed = expected 정확히) → `lhs_release_build.v13_audit_observation_problems` 가 시도마다 부른다 (사본 없음) + 합계 Σ observed ≤ n_finalized ≤ n_started ≤ n_processes |
| null · parser 결손 · 0 · 계획 밖 · 실제 실패 binding / 빈 요약을 build · check 둘 다 거부 · 정상 상세 통과 | 시험 V20 (build · check 각각) · 탐침 무변경 재실행 = §6 |
| 재시도 때문에 전체 started = finalized 를 강제하지 않는다 | 합계는 부등식만 (Q2 정보 = 완료 아닌 시도의 미최종 영수증) — 시험 V20c 재시도 이력 통과 |
| (잔여 · Q6) 분류 밖 단계만으로 실패한 감사의 결합 값이 자기모순 없이 맞아 요약만 비우면 통과하던 것 | 결합 기록 **v2** — 완료 시도 기록마다 `unclassified` (분류 밖 단계 이름 · 정상 `[]`) · 계약이 그 칸 (빈 목록) 을 요구 · 옛 v1 = 실행기 표 `IMPORT_OBS_STAGE_SCHEMA_RETIRED` → 배포 관문이 "고친 실행기로 감사를 다시 돌릴 것" 으로 거부 (감사 = 읽기 전용 · 계산 재실행 불요 → 머리 ④) · 감사 판정 · 사유 문구는 그대로 |

- 시험: `scripts/test_lhs_release_v13.py` 173/173 → 반례 먼저 178 PASS · 17 FAIL → **195/195** → (잔여) 198 PASS · 7 FAIL → **205/205** ·
  실행기 `--selftest` 117/120 (㉟i) → **120/120** → (잔여) 120/124 (㉟j) → **124/124** · `scripts/lhs_release_build.py --selftest` 31/31 (무관 · 확인만).

## 2. G2RR5-02 — case15 음성 대조가 실제 망 시도를 확인한다 (`72879744e` · 봉인 밖 · 수정 계획 Q2 (가))

| 판정문 §2 최소 해결 증거 | 구현 |
|---|---|
| 독립 원자료 탐침은 유지 · 실제 시도에도 구분 가능한 결과 | 기록기 `network_cli_recorder` (음성 대조 표지일 때만 스모크 자식 `child_case`) 가 `pipeline_service._RUNNER` 를 **그대로 통과**시키며 망 CLI 호출마다 입력 CSV 둘의 digest · 예외 종류 (적고 다시 올림) · returncode · 반환 직후 per-mode 두 JSON 의 sha256 · 채널 상태 · 사유를 보고 `attempt_evidence` 에 (인자 · 결과 · 동작 무변경 · 끝나면 원래 훅) · 단계 기록에 실행 결과 구조 필드 (`missing_outputs` · `stale_outputs` · `verify_failed`) 를 그대로 |
| 지정된 입력/채널 거부와 실행 실패 (PermissionError · 실행파일 없음 · timeout · traceback) 를 별도 상태 · 후자 TECH/FAIL | `[음성 대조]` ⑤ `case15.nc5_attempt` (`case15_attempt_verdict`): 망 CLI 1 회 · 예외 없음 · rc 0 · per-mode 둘 · 실패 채널 = 등록 넷 (전자 H/P · 열 Hertz = `(boundary_overlap)` · 열 Physics = `ValueError: … ligg_area < 0 (-0.186036)` = 원자료 탐침 오류와 같은 문자열) + 이온 computed 둘 · 단계 rc 0 · 결손 0 · 내용 검증 거부 · digest = 기록기 = 원자료 탐침 → PASS / 예외 · rc ≠ 0 · per-mode 없음 = **TECH** (스모크 rc 1) / 증거 없음 · 다른 결과 · 결합 어긋남 = FAIL |
| 300 자 문자열 grep 으로 의미 계약을 대신하지 않는다 | 판정은 구조 필드 · per-mode JSON 의 채널 토큰으로 (300 자 `err` = 진단만) |
| 정상 case15 · 호출 거부 · 누락 산출물 · 다른 예외를 각각 넣어 지정 거부만 PASS | 합성 변이 10 (PermissionError · FileNotFoundError · TimeoutExpired · …) + 실제 case15 (a) 망 CLI 만 PermissionError → `nc5_attempt` TECH · 스모크 rc 1 / (b) 주입 없음 → 일곱 PASS · rc 0 (`--selftest-real`) |

- 시험: `scripts/wsl_network_smoke.py --selftest` 14/14 → 반례 먼저 15/19 → **19/19** → Q7 나눔 뒤 `--selftest` 16/16 (12.5 s) + `--selftest-real` 4/4 (118.7 s) (§5).
- 웹앱 시도 기록 자체의 사유 구조화 (봉인 안 · 수정 계획 Q2 (나)) 는 194 발사 뒤 `WEB-05` 와 함께 — 이번 범위 밖.

## 3. G2RR5-03 — S0b 가 공용 판정으로 다시 판정한다 (`b34a52f52`)

| 판정문 §3 최소 해결 증거 | 구현 |
|---|---|
| 등록 marker/kind/범위만 허용 | 한 곳 = 인계 도구 `scripts/g2_network_reread.py` `CASE15_NEGCTL` (표지 · `case_id` · `kind` · `stop_after`) — 등록 표지 ∧ `case15_network` ∧ kind case15 ∧ stop_after network 일 때만 S0 에서 뺀다 · 그 밖 truthy 표지 = S0 실패 + S0b "미등록 음성 대조 표지" |
| 필수 검사 = 안정 ID · 정확한 cardinality · case15 프로세스 · 원자료 신원 포함 | `CASE15_NEGCTL_IDS` 일곱 (`case15.proc` · `raw_sha` · `nc1_blocked` · `nc2_tau` · `nc3_cause` · `nc4_ionic` · `nc5_attempt`) — 기록된 그 케이스 검사 = 그 집합 정확히 · 각 1 회 · id 없음 · 모르는 ID 거부 · 전부 PASS |
| 소비자가 공유 검증 함수로 상세를 다시 판정 · 기록과 대조 | 순수 함수 `case15_negctl_verdicts(report, timing)` — 생산자 (스모크 evaluate) 가 이 함수로 일곱을 만들고, S0b 가 보고 상세 · 자식 프로세스 기록 (`timings`) 에 **다시** 돌린 판정 = 기록 (상세 결손 · 수치 모순 = 실패) |
| unknown marker · 중복 · 상세 결손 · 수치 모순 · 실제 SHA FAIL 거부 · 정상 미퍼콜 대조군 통과 | Codex 변이 일곱 · 회귀 다섯 · 신원 · ID 시험 — 숫자 4 를 바꾸지 않았다 · 실패 케이스 면제 없음 · launcher-root 경로 무변경 |

- ④ 이온 증서 잔차 = bool 아님 · 0 이상 · 1e-6 미만 (판정문 §5 "유한 · 비음수를 엄격히" — 음수 잔차가 통과하던 것).
- 시험: `g2_network_reread --selftest` 20/20 → 반례 먼저 20/23 → **23/23**.
- **옛 WSL case15 기록 (10-07 14:15 · 22:24) 은 이제 거부된다 (의도)** — 실제 시도 증거 (`attempt_evidence`) · 검사 안정 ID 가 없다.  양성 = 고친 스모크로 다시 만든 기록 (머리 ② ③).

## 4. G2RR5-04 · 등록 비준 (`5a00125d2` · 등록 §9-6)

- 등록 `docs/reviews/lhs_network_batch_registration_20261007_g2.md` §4 완료 뒤 기대에 판정문 §4 권고 문안 그대로의 **재시도 예외 덧붙임** + 확인 명령 (합계 대신 — 등록 194 · SEALED 194 · 결합 키 = 완료 시도 키 · 시도마다 expected=observed · 감사 문제 [] · 완료 아닌 시도의 미최종 = 정보 · 재시도 없을 때만 시작 = 끝맺음) · 원 주석 · 명령 보존.
- ✅ 1저자 비준 10-09 = §3b · §4 · §9-4 제안 + 위 덧붙임 한 번에 · §9-6 에 **비준 뒤 활성 명령 표** (판정문 §7-4).  비준 = 등록 기대 · 명령의 비준이지 194 발사 승인이 아니다 (§0 · 재검증 6 GO 뒤 별도).

## 5. Q7 — 스모크 selftest 나눔 (`7928ff0de` · 시험 약화 없음)

- `--selftest` (fast · 게이트 fast 레인) = 판정 C1–C3 · 참조 침대 · case15 판정 변별 · G2RR5-02 합성 변이 10 · 기록기 · G2RR5-03 한 곳 · 합성 침대 실제 파이프라인 = 16 검사.
- `--selftest-real` (slow · WSL 사전 점검 단계 1) = G2RR4-03 원자료 직접 6 조합 · G2RR5-02 실제 case15 (a) TECH · rc 1 / (b) 일곱 PASS · rc 0 · (b) ROOT → `--smoke-root` rc 0 = 4 검사.
- 무변경 확인 (AST): `chk(…)` 호출 20 개의 이름 · 조건 식 = 나눔 전과 같다 (16 + 4) · 옮긴 픽스처 = 옛 중첩 정의와 AST 같다.  등재 `docs/reviews/selftest_inventory.tsv`.

## 6. Codex 탐침 — 고친 트리 무변경 재실행 (`docs/reviews/codex_g2rr5_fix_probe_rerun_20261008/`)

| 탐침 | 핀 `aa7ec7fe9` | 고친 트리 |
|---|---|---|
| `r5_release_contract` (상세 194 픽스처) | control 생성 · binding 변이 여섯 **생성 · check []** · 캐시 위조 재판정 문제 0 | control 생성 · check [] · 여섯 **거부 · 산출 없음** · 캐시 위조 재판정 1 · 1 · 1 · 2 · 1 · 1 · 기존 11 거부 그대로 (`8b6453671` · `7153a7d6a` 같음) |
| `r5_release_real_binding` (실제 audit CLI 실패 binding) | 요약 유지 거부 · **요약만 [] = 생성** | 두 행 거부 |
| `r5_observation` (감사 CLI · 수정 밖) | 17/17 | 17/17 · rc · 사유 문자열 바이트 같음 · 결합 기록 = 스키마 v1 → v2 + `unclassified` 칸만 다름 · 분류 밖 둘 (`unknown_stage` · `stage_e_out_of_scope`) 의 결합 + 요약 [] → 관문 문제 1 (`7153a7d6a` · `8b6453671` 에서는 0) |
| `r5_case15_pipeline_fault` | 망 CLI 거부 1 · 검사 6/6 PASS · 스모크 rc 0 | 검사 7 = 6 PASS + `case15.nc5_attempt` **TECH** (PermissionError · per-mode 없음 · 단계 rc 1 · 결손 넷 · verify_failed) → 스모크 rc 1 |
| `r5_case15` | positive rc 0 · 일곱 오수용 | 42 줄 자기 assert 에서 멈춘다 — 제출된 10-07 case15 기록의 생산자 판정이 이제 ⑤ FAIL (실제 시도 증거 없음 · §3 끝 줄) · 보충 `-O` 실행 = S0b 변이 전부 rc 1 (`marker_unknown` · 중복 · 상세 결손 · τ 수치 · 이온 잔차 · 원자료 SHA · 실패 기록 · 합성 입력) |
| `r5_case15_fault_reread` | rc 0 · S0b PASS | 입력 (`r5_case15` 산출) 이 없어 시작 못 함 · 입력 대체 보충 (표지) = S0b ✗ rc 1 |

- 한정: 탐침 재실행은 배포 · 다시 읽기 관문 증거의 수용 · 거부만 본다 — 194 생산 · S3 · DEM/MPM 이 아니다.  핀 = Codex 원본 JSON (Windows) · 고친 쪽 = 컨테이너 (Linux · Python 3.11).

## 7. G2RR3-02 — 닫은 근거 (수정 계획 Q5 · 원장 `verified`)

- 판정문 5 에 이 항목 행이 없다.  원장 `docs/reviews/findings.json` G2RR3-02 `verified_scope` = 감사 생산 경로의 import 관측 완결성 — 빈 · 잘린 로그 · 시작만 있는 완료 프로세스 · 다른 신원 · 망 솔버 누락 (재검증 4 §0 표에서 닫힘) +
  보조 단계 영수증 쌍 동시 결손 (재검증 4 가 G2RR4-02 로 넘긴 남은 부분 — 재검증 5 §0 표 G2RR4-02 = 감사 생산 경로 닫힘).  배포 경계 (`stage_binding` 내용) = G2RR5-01 (§1).
- ⇒ 미리 적은 닫는 조건이 충족돼 원장에서 닫았다 — **확인 요청 (Q5)**.

## 8. 질문

- **Q1 (G2RR5-01).** 생산자 계약 한 함수를 배포 관문이 시도마다 부르고 (사본 없음) 합계는 부등식만 — 판정문 §1 최소 해결 증거를 닫나?  옛 v1 결합 기록 = "감사를 다시" 거부 (머리 ④ 가 실제 ROOT 에서 v2 를 만든다) 도 받나?
- **Q2 (G2RR5-02).** 실제 시도 증거를 봉인 밖 스모크 기록기 (`pipeline_service._RUNNER` 통과 · 동작 무변경) 로 잡고, 웹앱 시도 기록의 구조화 (봉인 안) 는 194 뒤 `WEB-05` 로 미룬다 — 판정문 §2 를 이 범위에서 닫나?
- **Q3 (G2RR5-03).** S0b = 등록 표지 · 안정 ID 일곱 정확히 · 공용 판정 재계산 = 기록 · 게시 없음.  `r5_case15` 의 positive 가 이제 자기 assert 에서 멈추는 것 (제출 옛 기록 거부) 을 의도된 변화로 받나 — 새 양성 = 머리 ② ③?
- **Q4 (G2RR5-04 · 등록).** 등록 §9-6 비준 (활성 명령 표) 으로 판정문 §7-4 가 닫히나?
- **Q5 (G2RR3-02).** §7 의 닫은 근거를 확인해 줄 수 있나?
- **Q6 (Q6 잔여).** 결합 기록 v2 의 `unclassified` 칸으로 "분류 밖 단계만으로 실패한 감사 + 요약만 []" 가 막혔나 — 감사 판정 · 사유 문구는 그대로다.
- **Q7 (Q7 나눔).** 실제 case15 시험을 `--selftest-real` (slow · WSL 단계 1) 로 옮긴 것이 시험 약화가 아닌가 (AST 같은 조건 · 게이트 fast 레인 밖).
- **Q8 (발사 전).** 머리 ①–⑤ 의 WSL 결과 · 이 판정 뒤, 194 발사 전에 판정문 §7-5 · 7-6 (별도 발사 승인 · 새 ROOT · 관측 ON · 완료 뒤 SEALED194 · 결합 · 감사 · production194 상세 재독해 · 인계/배포 관문) 밖에 남는 것이 있나?

## 9. 한정 · 정정

- 이번 수정은 검사 도구 · 등록 문서뿐 — 봉인 32 · 망 수치 · σ 상수 · 모형 변경 없음 · 194 · S3 미실행 (S3 = 별도 HOLD).
- 수정 계획 §3 표의 *"positive (제출 기록 그대로) rc 0"* 기대는 필수 검사 (실제 시도 증거 · 안정 ID) 로 **대체됐다** (`docs/reviews/codex_g2rr5_fix_probe_rerun_20261008/case15/README.md` 해석) — 옛 기록 양성을 주장하지 않는다.
- 기존 시범 ROOT 의 `seal_audit.json` (ROOT 안 · v1 또는 결합 전) 은 이제 배포 관문이 거부한다 — 이번 재감사는 ROOT 밖 JSON 으로만 쓴다 (ROOT 원본 무변경 확인 = 머리 끝 줄).
