---
title: "DC 프롬프트 — W_ad 외주 2차 묶음 v3 확인: DB 해제조건 넷 + P2 가 닫혔는지 (고친 곳 diff 만) · 발송 승인 여부"
date: 2026-10-22
updated: 2026-10-22
tags: [review, wad, adhesion, vasp, outsourcing, runner, checker, codex, prompt, letter]
letter: DC
track: wad
channel: codex
kind: prompt
status: 초안 — 발송 전 (기준 커밋 3e70329cb · 묶음 v3 MANIFEST bf7b2ac9…)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = W_ad (DEM 협업 · 1저자 = 사용자). DB (v2 NO-GO · 해제 최소조건 넷) 다음 편지다. 사용자 결정 2026-10-22: *'DC 확인 뒤 업체 (권고)'* — 고친 곳만 짧게 확인받고, GO 를 받은 뒤 업체에 보낸다.
> ⛔ 점착 W 값은 kb 문서에 싣지 않는다 — 이 편지에도 W 숫자를 쓰지 않는다 (문턱 · 비율 · 벽시계만).
> 기준 커밋 `3e70329cb` (브랜치 `claude/evac-2026-10-22` · 그 뒤 커밋은 kb 만). ⬇ 아래 **보내는 글**만 발송한다 (부록 A · B 포함). 회신이 오면 `codex_DC_reply_…` 로 원문 보존.

---

**[W_ad · 외주 2차] 묶음 v3 확인 — DB 해제조건 넷 + P2 가 닫혔는지 (고친 곳만) · 발송 승인 여부**

## 0. 무엇을 묻나

DB 에서 v2 (MANIFEST `b9450f6f…`) 발송 NO-GO 와 해제 최소조건 넷을 받았다. 넷을 고쳤고, 비차단 P2 셋도 같이 고쳤고, 묶음을 새 폴더로 다시 만들었다 (**v3 · MANIFEST `bf7b2ac9…`**).
DB 끝줄 — *"위 네 음성 사례를 배포본 검사기와 Linux 러너에서 확인"* — 도 했다 (§3).
이번에도 **고친 곳만** 봐 달라 — **해제조건마다 닫혔는가 (GO / 조건부 / NO-GO) · 고치면서 새로 생긴 구멍은 없는가 · v3 를 업체에 보내도 되는가.**
DB 에서 GO · 해제였던 곳 (Q-DB-1 · 2 · 6 · 7 · 9 · S4–S9) 과 설계 · 구조 봉인 · 집계 산식 · 카드 문턱 · 잡 행렬은 다시 열지 않아도 된다.

## 1. 보는 범위 (diff)

- 기준 = DB 를 받은 커밋 `3d684e502` (묶음 v2 · MANIFEST `b9450f6f…`). 그 뒤 커밋:
  - `c475bf304` DB 회신 원문 보존 (kb 만)
  - `ea3bc0093` 해제조건 ① ② (+ Q-DB-8 ②) · `4e8d0ceba` ③ · `576a6d644` ④ · `881580040` P2 (Q-DB-8 ① · Q-DB-9 둘)
  - `3e70329cb` 묶음 v3 빌드 · 상태 줄 · README 초 형식 · 빌드 기록
  커밋 메시지마다 고친 것 · 시험 · 깨기 목록이 있다.
- `git diff 3d684e502 3e70329cb -- tools/wad/build_round2_vasp_package.py` (+150 −28 · 대부분 selftest). V5 · interfaces 도구는 안 바뀌었다.
- 묶음 v3 = `db/inputs/wad_round2_vasp_v3_2026_10_22/` · MANIFEST.sha256 의 sha256 `bf7b2ac921597f601fed3324159cf9812c1a1ff91ad4a0acf0a6ce590d9ac831`.
  v2 와 다른 파일은 넷 (run_all.sh · README.md · jobs.json · MANIFEST.sha256) — 잡 입력 (INCAR · POSCAR · KPOINTS · POTCAR.spec) 은 같다
  (`diff -r db/inputs/wad_round2_vasp_v2_2026_10_22 db/inputs/wad_round2_vasp_v3_2026_10_22`). v2 폴더는 검토받은 그대로 둔다 (발송 안 함).
- 빌드 기록 `db/properties/wad_round2_build_log_2026_10_17.json` 의 `⑤-4_DB_고침_2026_10_22`.

## 2. 해제조건별로 한 것 (DB 재현 → 지금 막는 시험)

시험은 전부 **DB 의 재현 절차를 그대로 음성 시험으로 먼저 쓰고, 고치기 전 판에서 빨간 것 (= DB 가 적은 결과) 을 본 뒤** 고쳤다. 시험 이름은 `⛔음성 DB …`.

**① 시도 열거 (P0-1 · `ea3bc0093`)**
- `_started()` = 알려진 시도 위치 (단 0 · r1A · r1B · r2B · a4A · a4B) 의 폴더에 **파일이 하나라도** 있으면 시작이다 (attempt.start · OUTCAR · OSZICAR · stdout.log · killed.json — 이름을 가리지 않는다).
  메타 (INCAR · attempt.json) 가 없으면 `INCOMPLETE_ATTEMPT` 로 남고, 환경 증거는 계속 감사한다.
- ⓑ 는 ⓐ 의 부모 폴더라 **하위 폴더 (stageA/ · .b/) 만으로는 시작이 아니다** — 폴더가 있다는 것만으로 B 실행을 인정하지 않는다.
- 시험: 사다리 밖 r1A 에 다른 빌드 OUTCAR → INCAR 와 attempt.json 만 지움 (attempt.start · stdout · PP 기록 · OSZICAR 는 남김 · 부모에 `.b/` 도 둠)
  → r1A `INCOMPLETE_ATTEMPT` · r1B 없음 · 잡 OK 아님 · `--collect` · `--check` 종료 6 · `--a4_result` 에 common_environment_failure. (고치기 전: `--check` 0 · a4 OK)

**② 커널 부정 증거 (P1-1 · `ea3bc0093`)**
- `env_evidence(attdir, optb88)` 가 optB88 시도면 원문 (stdout.log + OUTCAR) 의 커널 상태를 **무결성 · 완결성 검사 전에** 읽는다.
  `env_audit` 는 `not_read` · `regenerated` 면 등록부 유무 · 시도 상태와 무관하게 `KERNEL_NOT_READ` 전역 정지로 올린다. 긍정 문구는 여기서 쓰지 않는다 (불완전 시도를 올리지 않는다).
- Q-DB-8 ② 권고대로 확인된 부정문 `No kernel file found` 를 좁은 예외로 (대소문자 무시 · 이 구절만) — 긍정 문구와 같이 있어도 `not_read`.
- 시험: optB88 사다리 밖 r1A (INCAR 남김 · attempt.json 없음) 의 stdout 에 `kernel differs, recalculating vdW kernel`
  → 그 시도는 `INCOMPLETE_ATTEMPT` 이면서 `KERNEL_NOT_READ` 공통 고장 (종료 6 · `--a4_result` 기록). (고치기 전: 전역 고장 없음 · a4 OK)
  · 채택 시도 stdout 에 `No kernel file found` + 긍정 문구 → `KERNEL_NOT_READ`. (고치기 전: OK)

**③ 봉인 완결성 (P1-2 · `4e8d0ceba`)**
- `check_attempt` 의 `KERNEL_UNVERIFIED` 반환을 다른 완결성 검사 (POTCAR → SYSTEM → SETTINGS → ENERGY → D3) **뒤로** 옮겼다. ⓐ 에 허용한 결측 예외는 넓히지 않았다.
- 시험: 파일럿 optB88 bound OUTCAR 에서 해석 GGA 줄 · PARAM1 줄 · TITEL 줄을 하나씩 지우고 실행 기록 sha 를 맞춤
  → 등록부 전에도 `SETTINGS_UNVERIFIED` · `SETTINGS_UNVERIFIED` · `POTCAR_UNVERIFIED` · `seal_registry` 거부. (고치기 전: 셋 다 `KERNEL_UNVERIFIED` · 봉인됨)

**④ 시간 합산 (P1-3 · `576a6d644`)**
- 러너 `secs_ok` = `^(0|[1-9][0-9]{0,8})$` 를 손으로 넣는 세 입력 (`--infra-abort` 의 WALL_S · `--infra-wall` · `--killed` 의 WALL_S) 에 — **정규화하지 않고 거부한다** (종료 2 · 업체가 스케줄러 장부에서 다시 적는다) · `0` 은 받는다.
- `wall_s_of` 는 장부 항이 `^(0|[1-9][0-9]{0,11})$` 일 때만 더하고, 아니면 (선행 0 · 13 자리 이상 · 비숫자 · 빈 값) 미상 → 다음 잡 보류 (종료 5).
  `cap_ok` 는 `wall_s_of` 실패를 UNKNOWN 으로 받고, 결과가 숫자가 아니면 보류한다.
- README 5 번 항목과 영어 요약에 초 형식 (10진 · 선행 0 없이) 을 적었다 (`3e70329cb`).
- 시험: §3 (다) 표 — 배포 러너 v2 · v3 를 같은 상태에 둔 결과.

**P2 (비차단 · 같이 함 · `881580040`)**
- 재시작 regex 글자 검사를 `fullmatch` 로 (`'reading WAVECAR\n'` 거부).
- `parse_zavg`: 격자 · c_z 를 같은 try 안에서 읽고, 유한 · 양수 · `z_k = k·c_z/nz` (허용 2e-6 — 러너가 둘 다 `%.6f` 로 쓴다) 가 아니면 예외 없이 `{bad}`. 시험 = 머리 결함 여섯 (c_z 글자 · nan · 0 · 음수 · 격자 0 · z 간격).
- `collect`: 면평균 머리 run_id 가 채택 시도와 다르면 값 배열 없이 `{bad, run_id_matches: false}`.

**기존 시험에서 바꾼 기대값 (이유)** — 자체 검토 S7 의 stdout 재생성 문구 위조 시험: 이제 그 시도는 `ATTEMPT_MISMATCH` 이고 **잡은 `KERNEL_NOT_READ`** 다 (② — 무결성 실패 시도의 커널 재생성 원문도 전역 정지).

**깨기** — 고침을 한 부분씩 되돌린 사본 20 (①② 6 · ③ 1 · ④ 6 · P2 6 · README 1) — 전부 자기 시험이 빨강.

## 3. 배포본 확인 (DB 끝줄)

검사기 = 도구 sha `67908ae5…` (v3 jobs.json 의 tool_sha256 과 같다) · 러너 = v3 `run_all.sh` (= `run_all_text()` — 인자 없는 정적 텍스트라 시험 묶음의 러너와 바이트가 같다).
Linux · bash 5.2.21 · gawk 5.2.1 · mawk 1.3.4.

- (가) selftest **169/169** (두 awk).
- (나) 같은 selftest 를 **배포된 v3 폴더 사본 위에서** — 첫 `build()` 만 그 사본을 돌려주는 감싸개 (부록 A) 라서 러너 · jobs.json · MANIFEST · 잡 입력이 배포본 바이트다: **167/169** · 두 awk 같다.
  빨강 둘은 합성 시험 봉인과 대조하는 시험 (DIPOL 구간 · 두 번째 빌드의 MANIFEST sha) 이라 진짜 봉인으로 만든 배포본에서는 빨강이 맞다. **DB 음성 사례는 전부 초록.**
- (다) 러너 ④ **전후 대조** — 배포 러너 v2 (DB 가 본 판) 와 v3 를 같은 반송 상태에 둠 (가짜 POTCAR · 커널 · `VASP_CMD=false` · 다음 잡 `P2S_S_A_far` · 단계 P 상한 117 h = 421,200 초 · 부록 B). 두 awk 결과가 같다.

| 상황 | v2 | v3 |
|---|---|---|
| 장부 항 `wall_s` = `0450000` (10진 450,000 초 > 상한 · bash 8진이면 151,552 초) | 다음 잡 뜸 | 미상 → 안 뜸 (종료 5) |
| 장부 항 `0007200` | 뜸 | 안 뜸 (종료 5) |
| 장부 항 `08` (bash 산술 오류) | 뜸 | 안 뜸 (종료 5) |
| 장부 항 `18446744073709551616` (2⁶⁴ → bash 0) | 뜸 | 안 뜸 (종료 5) |
| 장부 항 `7200` | 뜸 | 뜸 (정상) |
| `--infra-abort` · `--killed` 에 `WALL_S=0007200` · `08` | 그대로 기록 (종료 0) | 거부 (종료 2 · 기록 없음) |
| `--infra-wall … 0007200` · `08` | 그대로 기록 (종료 0) | 거부 (종료 2 · UNKNOWN 그대로) |
| 세 입력에 `0` · `7200` | 기록 | 기록 (같다) |

bash 가 없는 환경이면 (나) · (다) 는 우리 실행 결과로 읽어 달라 — 부록 A 는 selftest 전체라 러너 부분에 bash 가 필요하고, 부록 B 는 bash 로 러너를 돌린다.

## 4. DB 권고와 다르게 · 더 넓게 한 곳 — 이것을 특히 봐 달라

1. **시작 판정 = '흔적 이름 목록' 이 아니라 '파일이 하나라도'.** 이름을 적으면 또 빠지는 이름이 생긴다 (S1 고침의 빈틈이 그것이었다).
   대가: 알려진 시도 위치에 업체가 아무 파일이나 두면 그 시도가 `INCOMPLETE_ATTEMPT` 가 되어 잡이 OK 가 아니게 된다 — 거짓 OK 가 아니라 보류 쪽이다.
2. **④ 는 정규화가 아니라 거부.** 손으로 적은 `0007200` 의 뜻을 러너가 짐작하지 않는다 — 업체가 스케줄러 장부에서 다시 적는다.
3. **자릿수 상한** — 손 입력 9 자리 (≈ 31 년) · 장부 항 12 자리. attempt.json 의 `elapsed_s` (러너가 씀) 도 같은 검사를 지나며, 시도 수백 개를 더해도 2⁶³ 에 한참 못 미친다.
4. **범위 밖으로 둔 것** — 러너가 만들지 않는 폴더 (예 `run/<잡>_r3`) 의 실행 흔적은 열거하지 않는다. DB 가 '알려진 시도 위치' 로 한정했고, README 가 손 실행을 금지하며, 알려진 시도는 각자 감사된다.
   반송 포장은 `(run|run_aborted)/<폴더>/(stageA/)?<허용 파일>` 을 담으므로 그런 폴더가 있으면 반송에 들어온다 (stageA 말고 다른 하위 폴더는 안 담긴다). 이것도 전역 정지로 올려야 하는지 판단해 달라.

## 5. 질문

- **Q-DC-1 … Q-DC-4**: 해제조건 ① – ④ 가 닫혔는가 — GO / 조건부 / NO-GO · 남으면 최소 수정.
- **Q-DC-5**: P2 셋이 맞는가 (비차단).
- **Q-DC-6**: §4 의 넷 — 특히 1 의 대가와 4 의 범위.
- **Q-DC-7**: 발송 승인 — 묶음 v3 (MANIFEST `bf7b2ac9…`) 를 업체에 보내도 되는가.

## 6. 바뀌지 않은 것

카드 문턱 · 잡 행렬 24 · 사다리 INCAR · 집계 산식 (Δ_C · G3 · G4 · G5 · 80 % 발동 · δ 규칙) · 구조 봉인 · 단계 상한 값 · 결정 둘 (`D-2026-10-15-wad-p2small-vasp-card` · `D-2026-10-15-wad-aprime-v5-e70-a4-rerun` · active) ·
재시도 규칙 (끊긴 시도는 다시 안 돈다 · 0 스텝 중단만 같은 단을 다시) · 업체 명령 (초 형식만 엄격해졌다).

## 7. 재현 방법

- `python3 -I tools/wad/build_round2_vasp_package.py --selftest` — DB 사례는 `⛔음성 DB`.
  mawk 로는 `mkdir /tmp/m && ln -s "$(command -v mawk)" /tmp/m/awk && PATH=/tmp/m:$PATH python3 -I …` (gawk 도 같은 식).
- `python3 -I tools/wad/build_round2_vasp_package.py --build --seal db/inputs/wad_p2small_seal_2026_10_17 --out <새 폴더>` → `diff -r` · MANIFEST sha 대조.
- 부록 A · B 는 저장소 뿌리에서 돌린다 (둘 다 저장소에는 없는 검증용 스크립트 · 아래 원문 그대로).

### 부록 A — 배포본 위 selftest 감싸개 (`python3 run_on_deployed.py db/inputs/wad_round2_vasp_v3_2026_10_22`)

```python
"""배포본 확인 — 쓰는 법: (저장소 뿌리에서) python3 run_on_deployed.py db/inputs/wad_round2_vasp_v3_2026_10_22
round2 selftest 를 돌리되, 첫 build(SEAL, PKG) (주 묶음) 만 배포된 v3 폴더의 사본으로 바꾼다.
러너 (run_all.sh) · jobs.json · MANIFEST · 잡 입력이 배포본 바이트 그대로다. 합성 봉인 (SEAL) 과 대조하는 시험 · 두 번째 빌드 재현 시험은 여기서는 빨강이 맞다 (배포본은 진짜 봉인으로 만들었다)."""
import hashlib, importlib.util, json, os, shutil, sys
REPO = os.getcwd(); DEP = os.path.join(REPO, sys.argv[1])          # 저장소 뿌리에서 돌린다
spec = importlib.util.spec_from_file_location("build_round2_vasp_package", os.path.join(REPO, "tools/wad/build_round2_vasp_package.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
orig, n = m.build, [0]
def dep_build(seal_dir, out, *a, **k):
    n[0] += 1
    if n[0] == 1:
        shutil.copytree(DEP, out)
        print(f"[배포본] 주 묶음 = {DEP} 사본 · MANIFEST sha {hashlib.sha256(open(os.path.join(out, 'MANIFEST.sha256'), 'rb').read()).hexdigest()}", flush=True)
        return json.load(open(os.path.join(out, "jobs.json"))), hashlib.sha256(open(os.path.join(out, "MANIFEST.sha256"), "rb").read()).hexdigest()
    return orig(seal_dir, out, *a, **k)
m.build = dep_build
print("[배포본] 도구 sha", hashlib.sha256(open(os.path.join(REPO, "tools/wad/build_round2_vasp_package.py"), "rb").read()).hexdigest()[:16],
      "· jobs.json tool_sha", json.load(open(os.path.join(DEP, "jobs.json")))["tool_sha256"][:16], flush=True)
r = m._selftest()
print("[배포본] _selftest 반환", r)
```

### 부록 B — 러너 ④ 전후 대조 (`python3 runner_p13.py <빈 작업 폴더>` · mawk 는 PATH 앞에 mawk 를 awk 로)

```python
"""배포본 러너에서 DB P1-3 음성 사례 — v2 (DB 검토본) 와 v3 를 같은 반송 상태에 두고 rc · 로그 끝 줄 · 다음 잡이 떴는지를 찍는다.
쓰는 법: (저장소 뿌리에서) python3 runner_p13.py <빈 작업 폴더>  (awk 는 PATH 의 것 — mawk 로는 PATH 앞에 mawk 를 awk 로 둔다)"""
import importlib.util, json, os, shutil, subprocess, sys
REPO = os.getcwd(); OUT = os.path.abspath(sys.argv[1])          # 저장소 뿌리에서 돌린다
spec = importlib.util.spec_from_file_location("r2", os.path.join(REPO, "tools/wad/build_round2_vasp_package.py"))
m = importlib.util.module_from_spec(spec); sys.path.insert(0, os.path.join(REPO, "tools/wad")); spec.loader.exec_module(m)
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
POT = os.path.join(OUT, "pot")
for e in m.SPECIES_ORDER:
    os.makedirs(os.path.join(POT, m.POTCAR_MAP[e]), exist_ok=True)
    open(os.path.join(POT, m.POTCAR_MAP[e], "POTCAR"), "w").write(f"   VRHFIN =X: s p\n   TITEL  = {m.PP_EXPECTED_TITEL[e]}\n   POMASS =   1.000; ZVAL   = {m.ZVAL[e]:8.3f}    mass and valenz\n")
KER = os.path.join(OUT, "vdw_kernel.bindat"); open(KER, "wb").write(b"KERNEL" * 100)
PK = {"v2": "db/inputs/wad_round2_vasp_v2_2026_10_22", "v3": "db/inputs/wad_round2_vasp_v3_2026_10_22"}
def fresh(v, name):
    d = os.path.join(OUT, f"{v}_{name}"); shutil.copytree(os.path.join(REPO, PK[v]), d, ignore=shutil.ignore_patterns("run", "run_aborted", "round2_return*")); return d
def run(pk, args=(), **kw):
    env = dict(os.environ, VASP_CMD="false", POTCAR_DIR=POT, VDW_KERNEL=KER, WATCH_S="1")
    env.update({k: v for k, v in kw.items() if v is not None})
    for k in [k for k, v in kw.items() if v is None]:
        env.pop(k, None)
    r = subprocess.run(["bash", os.path.join(pk, "run_all.sh"), *args], capture_output=True, text=True, env=env, timeout=600)
    lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    return r.returncode, lines
def fake_att(pk, job, files):
    d = os.path.join(pk, "run", job); os.makedirs(d, exist_ok=True)
    shutil.copy(os.path.join(pk, "jobs", job, "INCAR"), os.path.join(d, "INCAR"))
    for f, t in files.items():
        open(os.path.join(d, f), "w").write(t)
rows = []
# ⓐ 장부 항 (run_aborted/…/infra_abort.json 의 wall_s) — 단계 P 상한 117 h = 421,200 초 · 다음 잡 P2S_S_A_far 가 뜨는가
for w in ("0450000", "0007200", "08", "18446744073709551616", "7200"):
    for v in ("v2", "v3"):
        pk = fresh(v, f"led_{w[:12]}"); d = os.path.join(pk, "run_aborted", "P2S_S_A_bound_0_1"); os.makedirs(d)
        json.dump({"job": "P2S_S_A_bound", "rung": "0", "wall_s": w}, open(os.path.join(d, "infra_abort.json"), "w"))
        rc, ls = run(pk, JOBS="P2S_S_A_far")
        launched = os.path.isdir(os.path.join(pk, "run", "P2S_S_A_far"))
        hold = next((l for l in ls if "⏸" in l), "")
        rows.append(("장부 항 wall_s=" + repr(w), v, rc, "다음 잡 뜸" if launched else "안 뜸", hold[:150]))
# ⓑ 손으로 넣는 초 — --infra-abort (WALL_S) · --infra-wall · --killed (WALL_S)
for v in ("v2", "v3"):
    for w in ("0007200", "08", "0", "7200"):
        pk = fresh(v, f"in_{w}"); fake_att(pk, "P2S_S_A_bound", {})
        rc, ls = run(pk, ("--infra-abort", "P2S_S_A_bound", "0", "SGE-1", "2026-10-22T00:00Z", "node", "lost"), WALL_S=w)
        f = os.path.join(pk, "run_aborted", "P2S_S_A_bound_0_1", "infra_abort.json")
        rows.append((f"--infra-abort WALL_S={w}", v, rc, "기록 wall_s=" + (repr(json.load(open(f)).get("wall_s")) if os.path.isfile(f) else "없음"), (ls[-1] if ls else "")[:150]))
        pk = fresh(v, f"iw_{w}"); fake_att(pk, "P2S_S_A_bound", {})
        run(pk, ("--infra-abort", "P2S_S_A_bound", "0", "SGE-1", "2026-10-22T00:00Z", "node", "lost"), WALL_S=None)
        rc, ls = run(pk, ("--infra-wall", "P2S_S_A_bound_0_1", w))
        f = os.path.join(pk, "run_aborted", "P2S_S_A_bound_0_1", "infra_abort.json")
        rows.append((f"--infra-wall … {w}", v, rc, "기록 wall_s=" + (repr(json.load(open(f)).get("wall_s")) if os.path.isfile(f) else "없음"), (ls[-1] if ls else "")[:150]))
        pk = fresh(v, f"kl_{w}")
        fake_att(pk, "P2S_S_A_far", {"attempt.start": json.dumps({"job": "P2S_S_A_far", "attempt": "0", "stage": "P", "run_id": "20261022T000000-1-1", "t_start": 0, "kernel_sha256": ""}) + "\n",
                                     "OSZICAR": "DAV:   1   -0.1E+04   -0.1E+04   -0.1E+02  100   0.1E+02\n"})
        rc, ls = run(pk, ("--killed", "P2S_S_A_far", "0", "SGE-2", "2026-10-22T01:00Z", "wall"), WALL_S=w)
        f = os.path.join(pk, "run", "P2S_S_A_far", "killed.json")
        rows.append((f"--killed WALL_S={w}", v, rc, "기록 wall_s=" + (repr(json.load(open(f)).get("wall_s")) if os.path.isfile(f) else "없음"), (ls[-1] if ls else "")[:150]))
aw = subprocess.run(["awk", "-W", "version"], capture_output=True, text=True); aw = (aw.stdout or aw.stderr).splitlines()[0] if (aw.stdout or aw.stderr) else "?"
if "mawk" not in aw:
    aw = subprocess.run(["awk", "--version"], capture_output=True, text=True).stdout.splitlines()[0]
print(f"# bash {subprocess.run(['bash', '-c', 'echo $BASH_VERSION'], capture_output=True, text=True).stdout.strip()} · awk {aw}")
for r in rows:
    print(" | ".join(map(str, r)))
```
