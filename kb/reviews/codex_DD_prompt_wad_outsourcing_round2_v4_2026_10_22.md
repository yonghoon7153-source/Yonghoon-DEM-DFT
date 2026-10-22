---
title: "DD 프롬프트 — W_ad 외주 2차 묶음 v4 확인: DC 재승인 최소조건 셋 (읽기 실패 ≠ 없음 · 장부 전체 값 · 결박 갱신) + 같은 종류 훑기 + 미등록 실행 흔적 자동 보류 · 발송 승인 여부"
date: 2026-10-22
updated: 2026-10-22
tags: [review, wad, adhesion, vasp, outsourcing, runner, checker, codex, prompt, letter]
letter: DD
track: wad
channel: codex
kind: prompt
status: 초안 — 발송 전 (기준 커밋 1e4d113d2 · 묶음 v4 MANIFEST 39522906…)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = W_ad (DEM 협업 · 1저자 = 사용자). DC (v3 NO-GO · P1 2 · 재승인 최소조건 셋) 다음 편지다. 사용자 결정 2026-10-22 *'DC 확인 뒤 업체 (권고)'* 의 연장 — 고친 곳만 확인받고 GO 뒤 업체에 보낸다.
> ⛔ 점착 W 값은 kb 문서에 싣지 않는다 — 이 편지에도 W 숫자를 쓰지 않는다 (문턱 · 비율 · 벽시계만).
> 기준 커밋 `1e4d113d2` (브랜치 `claude/evac-2026-10-22` · 그 뒤 커밋은 kb 만). ⬇ 아래 **보내는 글**만 발송한다 (부록 A · B 포함). 회신이 오면 `codex_DD_reply_…` 로 원문 보존.

---

**[W_ad · 외주 2차] 묶음 v4 확인 — DC 재승인 최소조건 셋 + 같은 종류 훑기 + 미등록 실행 흔적 · 발송 승인 여부**

## 0. 무엇을 묻나

DC 에서 v3 (MANIFEST `bf7b2ac9…`) 발송 NO-GO 와 P1 둘 · 재승인 최소조건 셋을 받았다. 둘을 고쳤고, 같은 종류 (못 읽은 것을 '없음' 으로 · 값의 앞부분만 읽기) 를
검사기와 러너에서 더 찾아 같이 고쳤고, Q-DC-6 ④ 의 미등록 실행 흔적을 자동 보류로 넣었다. 묶음은 새 폴더로 다시 만들었다 (**v4 · MANIFEST `39522906…`**).
이번에도 **고친 곳만** 봐 달라 — **재승인 조건마다 닫혔는가 (GO / 조건부 / NO-GO) · 고치면서 새로 생긴 구멍은 없는가 · v4 를 업체에 보내도 되는가.**
DC 에서 GO 였던 곳 (Q-DC-2 · 3 · 5 · Q-DC-6 ①–③) 과 설계 · 구조 봉인 · 집계 산식 · 카드 문턱 · 잡 행렬은 다시 열지 않아도 된다.

## 1. 보는 범위 (diff)

- 기준 = DC 를 받은 커밋 `3e70329cb` (묶음 v3 · MANIFEST `bf7b2ac9…`). 그 뒤 커밋:
  - `d3f41b333` · `5bf9c5430` · `4c1ae1e00` 편지 DC · 회신 원문 보존 (kb 만)
  - `d538279df` 고침 (아래 §2 전부 · 시험 · 깨기 목록은 커밋 메시지)
  - `1e4d113d2` 묶음 v4 빌드 · 상태 줄 · 빌드 기록 · 러너 bash 쪽 rc 형식 검사 제거 (awk 와 같은 검사라 깨기로 구별 안 됨 — §2 깨기)
- `git diff 3e70329cb 1e4d113d2 -- tools/wad/build_round2_vasp_package.py` (+316 −29 · 대부분 selftest). V5 · interfaces 도구는 안 바뀌었다.
- 묶음 v4 = `db/inputs/wad_round2_vasp_v4_2026_10_22/` · MANIFEST.sha256 의 sha256 `395229065660432afb5b9c96e518d891efd293a28f8d2e4279a5588a0ceaa321`.
  v3 와 다른 파일은 넷 (run_all.sh · README.md 상태 줄 · jobs.json · MANIFEST.sha256) — 잡 입력 (INCAR · POSCAR · KPOINTS · POTCAR.spec) 은 같다. v3 폴더는 검토받은 그대로 둔다 (발송 안 함).
- 빌드 기록 `db/properties/wad_round2_build_log_2026_10_17.json` 의 `⑤-5_DC_고침_2026_10_22`.

## 2. 재승인 조건별로 한 것 (DC 재현 → 지금 막는 시험)

새 시험 13 = 음성 12 + 대조 1. 음성 12 개는 전부 **고치기 전 판에서 빨간 것을 확인했다** (DC 재현은 DC 가 적은 결과가 그대로 나왔다 · 고치기 전 판 + 새 시험 = 169/182 —
음성 12 와 판정 탐침 rc 'NA' 를 넣은 기존 '기대 상태' 표). 아홉은 고치기 전에 썼고 셋은 고친 뒤에 더했다 — 다른 경로가 같은 정지를 내서 고침 하나를 되돌려도
초록이 남던 자리를 따로 잡으려고 (끊긴 시도의 증거 파일 · aborted_attempts 직접 · 채택 시도 검사 도중). 시험 이름은 `⛔음성 DC …`.
권한 실패는 **주입**으로 만들었다 (`os.scandir` · `os.listdir` · `open` 을 그 경로에서만 PermissionError) — 우리 시험 환경은 root 라 chmod 로 막히지 않는다 (DC 와 같은 방식 · 운영체제 권한 실험이 아니다).

**① 시도 폴더 · 증거를 읽지 못하면 감사 불가 (DC P1-1)**
- `_started()` 는 **없는 폴더 (FileNotFoundError) 만** '시작 안 함' 이다. 권한 · 입출력 · 폴더 아님 같은 다른 열거 실패는 OSError 를 올리고,
  `resolve_job` 이 그 시도를 `ATTEMPT_UNREADABLE` (무결성 등급) 로 남긴다 — 환경 증거에 `unreadable` 을 달아 `env_audit` 가 `AUDIT_UNREADABLE` 전체 정지로 올린다.
  검사 도중 읽기 실패 (sha 를 낼 파일 등) 도 같은 기록이 된다.
- 시험 (DC 재현): 다른 빌드 r1A 가 있는 반송 — 읽기 오류 없으면 `VERSION_MISMATCH` · 그 r1A 폴더 열거에만 PermissionError
  → 그 시도 `ATTEMPT_UNREADABLE` · 잡 OK 아님 · 공통 고장 `AUDIT_UNREADABLE` (collect 종료 6) · `--check` 6 · `--a4_result` 에 공통 고장.
  (고치기 전: 잡 OK · `--check` 0 · a4 OK · 공통 고장 없음 — DC 표 그대로)

**② 장부는 전체 값으로 (DC P1-2)**
- 러너 `wall_s_of` 가 `"elapsed_s": [^,}]*[,}]` — **값 전체와 끝 구분자** 를 잡은 뒤 기존 10진 검사 (`^(0|[1-9][0-9]{0,11})$`) 에 넣는다.
  4.5e5 · 1e12 · 뒤 쓰레기 · 숫자 중간에서 잘림 (끝 구분자 없음) → 미상 → 다음 잡 보류 (종료 5). 잘린 attempt.json 이 시작 표지의 미상을 덮지 못한다.
- 시험: 장부 `run_aborted/…/attempt.json` 에 넷 → 종료 5 · 다음 잡 안 뜸 · '미상' · 정상 450000 은 '누적' 상한 보류 · 정상 7200 은 뜬다.
  (고치기 전: 4.5e5 · 1e12 · 잘린 4 는 다음 잡이 떴다 · 450000x 는 450000 으로 더해 '누적' 보류)

**③ 결박 갱신** — 묶음 v4 를 새로 빌드 · jobs.json `tool_sha256` = 고친 도구 (`630ac4cb…`) · `run_all.sh` = `run_all_text()` · MANIFEST `39522906…` (§3).

**같은 종류 훑기 (DC 가 짚지 않은 곳 · 우리가 찾음)**
- 검사기 — 환경 증거 파일 (OUTCAR · POTCAR.species.sha256 · attempt.json · attempt.start · optB88 이면 stdout.log) 도 없는 것만 '없음' · 못 읽으면 `unreadable` → `AUDIT_UNREADABLE`.
  특히 끊긴 시도 (attempt.json 없음) 는 검사기가 환경 증거만 읽어서 이 길이 유일한 감사다. 시험: 끊긴 r1A 에서 네 파일을 하나씩 막음 → 넷 다 `INCOMPLETE_ATTEMPT` + `AUDIT_UNREADABLE` (고치기 전: 고장 없음).
- 검사기 — `run_aborted/` 열거 · 그 안 폴더 하나의 열거 실패 → `ATTEMPT_UNREADABLE` (고치기 전: `run_aborted/` 열거 실패는 예외로 죽었고, 폴더 하나를 못 읽으면 그 안 증거를 '없음' 으로 보았다).
- 러너 judge — attempt.json 의 rc 도 전체 값으로 (`"rc": [^,}]*[,}]` 로 잡고, awk 에서 `^(0|-?[1-9][0-9]*)$` 가 아니면 `rc_unknown`). 0.5 · 1e3 · -0 · 뒤 쓰레기 → `SCF_UNVERIFIED` (승격 없음).
  고치기 전에는 0.5 → 0 → OK · 1e3 → 1 → RUN_FAILED → 다음 단이었다 (검사기는 같은 기록을 ATTEMPT_MISMATCH 로 보고 승격하지 않는다 — 러너와 갈렸다).
  파이썬 `judge_text` 도 같은 자리에 같은 가지 (판정 탐침 하나 더: rc 'NA' → 둘 다 `SCF_UNVERIFIED rc_unknown`).
- 러너 `wsha` — WAVECAR.info 의 sha 를 **정확히 64 자** 로 (고치기 전: 65 자 값의 앞 64 자를 sha 로 읽어 앞부분이 같으면 재시작 이행으로 봤다).

**Q-DC-6 ④ — 미등록 실행 흔적 자동 보류 (DC 권고대로)**
- `unregistered_traces()` — 등록 = 잡마다 사다리 단 폴더 (`RUNG_DIR`) · `run_aborted/<잡>_<단>_<k>`. 그 밖 폴더에 실행 흔적 (반송 허용 이름에서 입력 사본 INCAR · KPOINTS · POSCAR 만 뺀 것) 이 있으면
  `UNREGISTERED_ATTEMPT` — 환경 불일치로 단정하지 않고 '감사되지 않음' 으로 전체 정지 목록에 넣는다 (collect · `--check` 종료 6 · a4 공통 고장 · **봉인 거부**).
  빈 폴더 · 설명 파일 · 입력 사본만 있는 폴더는 흔적이 아니다. 반송 폴더를 못 읽으면 흔적이 있는지 모른다 → `AUDIT_UNREADABLE`.
- 시험: `run/<잡>_r3` (다른 빌드 OUTCAR + 시작 표지 — DC 재현) · `run/<잡>_r1/stageB` · `run_aborted/junk` · `run/OUTCAR` → 넷 다 보류 · `--check` 6 · a4 공통 고장 · 봉인 거부 /
  빈 폴더 · README · INCAR 만 · 정상 `run_aborted/<잡>_0_1` → 고장 없음. (고치기 전: 24 잡 OK · 고장 없음 · 봉인됨)
- ⚠ 못 하는 것: 반송 포장이 허용 이름만 담으므로 그 밖 이름의 파일은 안 보인다 · 미등록 흔적의 내용 (빌드 · PP) 은 감사하지 않는다 (있다는 것만).

**깨기** — 고침을 한 부분씩 되돌린 사본 21 (첫 판) + 다시 셋 — 첫 판 빨강 19 · 안 잡힘 둘 — F02 (사다리 경로의 읽기 실패 감싸개: 시도 열거 쪽 try 가 같은 예외를 받아 가려졌다 → '채택 시도 검사 도중' 시험을 더한 뒤 빨강) · F15 (러너 bash 쪽 rc 형식 검사: awk 의 rc_unknown 이 같은 값을 같은 결과로 걸러 구별이 안 됨 → 뺐다 · 뺀 뒤 rc 깨기 둘 다시 빨강). 등록 집합을 비운 사본은 기대 시험 대신 파일럿 봉인에서 selftest 가 멈춰 빨강 (종료 2). 다른 빨강은 같은 고침에 기대는 시험만. 고치기 전 판에 새 시험을 넣으면 169/182 (새 음성 13 이 빨강).

## 3. 배포본 확인 (재승인 조건 ① ② 끝 · ③)

검사기 = 도구 sha `630ac4cb…` (v4 jobs.json 의 tool_sha256 과 같다) · 러너 = v4 `run_all.sh` (= `run_all_text()`). Linux · bash 5.2.21 · gawk 5.2.1 · mawk 1.3.4.

- (가) selftest **182/182** (두 awk).
- (나) 배포본 위 selftest (부록 A — 이번에는 **종료 코드가 판정**이다: 빨강이 정확히 예상한 둘이면 0 · 아니면 1 · 시험 요약과 빨강 이름을 그대로 찍는다):
  v4 사본 위 selftest 180/182 · 빨강 정확히 예상한 둘 (DIPOL 구간 · 두 번째 빌드 MANIFEST sha) · 그 밖 0 · **감싸개 종료 0** · gawk · mawk 같다.
- (다) 러너 전후 대조 — 배포 러너 v3 (DC 가 본 판) 와 v4 를 같은 반송 상태에 둠 (부록 B · 두 awk 결과 같음):

| 상황 | v3 러너 (DC 가 본 판) | v4 러너 |
|---|---|---|
| 장부 attempt.json elapsed_s 4.5e5 | 종료 1 · 다음 잡 뜸 · - | 종료 5 · 안 뜸 · 미상 |
| 장부 attempt.json elapsed_s 1e12 | 종료 1 · 다음 잡 뜸 · - | 종료 5 · 안 뜸 · 미상 |
| 장부 attempt.json elapsed_s 450000x (뒤 쓰레기) | 종료 5 · 안 뜸 · 누적 | 종료 5 · 안 뜸 · 미상 |
| 장부 attempt.json elapsed_s …: 4 (숫자 중간에서 잘림) | 종료 1 · 다음 잡 뜸 · - | 종료 5 · 안 뜸 · 미상 |
| 장부 attempt.json elapsed_s 450000 (정상 · 상한 넘음) | 종료 5 · 안 뜸 · 누적 | 종료 5 · 안 뜸 · 누적 |
| 장부 attempt.json elapsed_s 7200 (정상) | 종료 1 · 다음 잡 뜸 · - | 종료 1 · 다음 잡 뜸 · - |
| 장부 infra_abort.json wall_s 0450000 | 종료 5 · 안 뜸 · 미상 | 종료 5 · 안 뜸 · 미상 |
| 장부 infra_abort.json wall_s 0007200 | 종료 5 · 안 뜸 · 미상 | 종료 5 · 안 뜸 · 미상 |
| 장부 infra_abort.json wall_s 08 | 종료 5 · 안 뜸 · 미상 | 종료 5 · 안 뜸 · 미상 |
| 장부 infra_abort.json wall_s 18446744073709551616 | 종료 5 · 안 뜸 · 미상 | 종료 5 · 안 뜸 · 미상 |
| 장부 infra_abort.json wall_s 7200 | 종료 1 · 다음 잡 뜸 · - | 종료 1 · 다음 잡 뜸 · - |
| judge · attempt.json rc 0.5 | OK - | SCF_UNVERIFIED rc_unknown |
| judge · attempt.json rc 1e3 | RUN_FAILED rc_or_not_terminated | SCF_UNVERIFIED rc_unknown |
| judge · attempt.json rc -0 | RUN_FAILED rc_or_not_terminated | SCF_UNVERIFIED rc_unknown |
| judge · attempt.json rc 0 | OK - | OK - |
| judge · attempt.json rc -1 | RUN_FAILED rc_or_not_terminated | RUN_FAILED rc_or_not_terminated |
| wsha · 65 자 sha | 64 자 | 빈 값 |
| wsha · 64 자 sha | 64 자 | 64 자 |

## 4. DC 권고와 다르게 · 더 넓게 한 곳 — 이것을 특히 봐 달라

1. **같은 종류 훑기** (§2) — DC 가 짚은 두 자리 말고도 검사기 증거 파일 · run_aborted · 러너 judge rc · wsha 를 같이 고쳤다. 특히 judge 의 rc 는 러너 동작이 바뀐다
   (손상된 rc → 승격하지 않고 멈춤 — 검사기와 같은 쪽).
2. **전체 정지 목록 하나** — `AUDIT_UNREADABLE` · `UNREGISTERED_ATTEMPT` 도 기존 `common_environment_failure` 목록 (종료 6 · a4 기록 · V5 거부) 에 등급 이름을 달아 넣었다.
   환경 고장과 이름으로 구분되지만 종료 코드는 같다. 따로 종료 코드를 둬야 하는지 판단해 달라.
3. **실행 흔적의 정의** — 반송 허용 이름에서 입력 사본 셋만 뺀 것 (warn.log · PP 기록 · LOCPOT.zavg.txt 도 흔적). 좁히거나 넓혀야 하는지.

## 5. 질문

- **Q-DD-1**: 재승인 조건 ① (읽기 실패 ≠ 없음 → 검사 중단 · `--check` · a4 음성) 이 닫혔는가.
- **Q-DD-2**: 조건 ② (장부 전체 값 · 배포 Linux 러너 보류) 가 닫혔는가.
- **Q-DD-3**: 조건 ③ (도구 해시 · 러너 · MANIFEST 결박) 이 맞는가.
- **Q-DD-4**: 같은 종류 훑기 (§2) 가 맞는가 · 고치면서 새 구멍은 없는가.
- **Q-DD-5**: Q-DC-6 ④ 자동 보류 (§2 · §4 의 2 · 3) 가 맞는가.
- **Q-DD-6**: 발송 승인 — 묶음 v4 (MANIFEST `39522906…`) 를 업체에 보내도 되는가.

## 6. 바뀌지 않은 것

카드 문턱 · 잡 행렬 24 · 사다리 INCAR · 집계 산식 · 구조 봉인 · 단계 상한 값 · 결정 둘 (`D-2026-10-15-wad-p2small-vasp-card` · `D-2026-10-15-wad-aprime-v5-e70-a4-rerun` · active) ·
재시도 규칙 · 업체 명령 · README (상태 줄만).

## 7. 재현 방법

- `python3 -I tools/wad/build_round2_vasp_package.py --selftest` — DC 사례는 `⛔음성 DC`. mawk 로는 `mkdir /tmp/m && ln -s "$(command -v mawk)" /tmp/m/awk && PATH=/tmp/m:$PATH python3 -I …`.
- `python3 -I tools/wad/build_round2_vasp_package.py --build --seal db/inputs/wad_p2small_seal_2026_10_17 --out <새 폴더>` → `diff -r` · MANIFEST sha 대조.
- 부록 A · B 는 저장소 뿌리에서 돌린다 (둘 다 저장소에는 없는 검증용 스크립트 · 아래 원문 그대로).

### 부록 A — 배포본 위 selftest 감싸개 (`python3 run_on_deployed.py db/inputs/wad_round2_vasp_v4_2026_10_22` · 종료 0 = 통과)

```python
"""배포본 확인 — 쓰는 법: (저장소 뿌리에서) python3 run_on_deployed.py <배포 묶음 폴더>   · 종료 0 = 통과 · 1 = 실패
round2 selftest 를 돌리되, 첫 build(SEAL, PKG) (주 묶음) 만 배포 묶음의 사본으로 바꾼다 — 러너 (run_all.sh) · jobs.json · MANIFEST · 잡 입력이 배포본 바이트다.
합성 시험 봉인 (SEAL) 과 대조하는 시험 둘 (DIPOL 구간 · 두 번째 빌드의 MANIFEST sha) 은 진짜 봉인으로 만든 배포본에서 빨강이 맞다 —
**빨강이 정확히 그 둘이면** 통과 (종료 0) · 하나라도 다르면 실패 (종료 1). 시험 요약 · 빨강 이름은 그대로 찍는다 (Codex DC: 종료 0 만 증거로 쓰지 말 것)."""
import contextlib, hashlib, importlib.util, io, json, os, shutil, sys
REPO = os.getcwd(); DEP = os.path.join(REPO, sys.argv[1])
EXPECTED_RED = ("묶음: DIPOL = 봉인 집합의 쌍극 구간", "결정성: 두 번 만들면 MANIFEST sha 가 같다")
spec = importlib.util.spec_from_file_location("build_round2_vasp_package", os.path.join(REPO, "tools/wad/build_round2_vasp_package.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
orig, n = m.build, [0]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()


def dep_build(seal_dir, out, *a, **k):
    n[0] += 1
    if n[0] == 1:
        shutil.copytree(DEP, out)
        return json.load(open(os.path.join(out, "jobs.json"))), sha(os.path.join(out, "MANIFEST.sha256"))
    return orig(seal_dir, out, *a, **k)


m.build = dep_build
print(f"[배포본] {sys.argv[1]} · MANIFEST sha {sha(os.path.join(DEP, 'MANIFEST.sha256'))}")
print(f"[배포본] 도구 sha {sha(os.path.join(REPO, 'tools/wad/build_round2_vasp_package.py'))[:16]} · jobs.json tool_sha {json.load(open(os.path.join(DEP, 'jobs.json')))['tool_sha256'][:16]}")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    r = m._selftest()
log = buf.getvalue(); print(log, end="")
red = [ln.strip()[2:] for ln in log.splitlines() if ln.startswith("  ✗ ")]
hit = {e: sum(x.startswith(e) for x in red) for e in EXPECTED_RED}
other = [x[:160] for x in red if not any(x.startswith(e) for e in EXPECTED_RED)]
ok = all(v == 1 for v in hit.values()) and not other and len(red) == len(EXPECTED_RED)
print(f"[배포본] 빨강 {len(red)} · 예상한 둘 {hit} · 그 밖 {len(other)} {other[:3]} · selftest 반환 {r} → {'통과' if ok else '실패'}")
sys.exit(0 if ok else 1)
```

### 부록 B — 러너 전후 대조 (`python3 runner_contract.py db/inputs/wad_round2_vasp_v3_2026_10_22 db/inputs/wad_round2_vasp_v4_2026_10_22 <빈 작업 폴더>` · mawk 는 PATH 앞에 mawk 를 awk 로)

```python
"""배포 러너 전후 대조 — 쓰는 법: (저장소 뿌리에서) python3 runner_contract.py <옛 묶음> <새 묶음> <빈 작업 폴더>   (awk 는 PATH 의 것)
두 묶음의 run_all.sh 를 같은 반송 상태에 두고 (가짜 POTCAR · 커널 · VASP_CMD=false · 다음 잡 P2S_S_A_far · 단계 P 상한 117 h = 421,200 초)
종료 코드 · 다음 잡이 떴는지 · 보류 사유 (미상 / 누적) 를 찍는다. judge 의 rc · wsha 는 그 러너에서 함수만 떼어 돌린다."""
import importlib.util, json, os, re, shutil, subprocess, sys
REPO = os.getcwd(); OLD, NEW, OUT = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3])
spec = importlib.util.spec_from_file_location("r2", os.path.join(REPO, "tools/wad/build_round2_vasp_package.py"))
m = importlib.util.module_from_spec(spec); sys.path.insert(0, os.path.join(REPO, "tools/wad")); spec.loader.exec_module(m)
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
POT = os.path.join(OUT, "pot")
for e in m.SPECIES_ORDER:
    os.makedirs(os.path.join(POT, m.POTCAR_MAP[e]), exist_ok=True)
    open(os.path.join(POT, m.POTCAR_MAP[e], "POTCAR"), "w").write(f"   VRHFIN =X: s p\n   TITEL  = {m.PP_EXPECTED_TITEL[e]}\n   POMASS =   1.000; ZVAL   = {m.ZVAL[e]:8.3f}    mass and valenz\n")
KER = os.path.join(OUT, "vdw_kernel.bindat"); open(KER, "wb").write(b"KERNEL" * 100)
PK = {"old": OLD, "new": NEW}


def fresh(v, name):
    d = os.path.join(OUT, f"{v}_{name}")
    shutil.copytree(os.path.join(REPO, PK[v]), d, ignore=shutil.ignore_patterns("run", "run_aborted", "round2_return*"))
    return d


def run(pk, args=(), **kw):
    env = dict(os.environ, VASP_CMD="false", POTCAR_DIR=POT, VDW_KERNEL=KER, WATCH_S="1")
    env.update({k: v for k, v in kw.items() if v is not None})
    r = subprocess.run(["bash", os.path.join(pk, "run_all.sh"), *args], capture_output=True, text=True, env=env, timeout=600)
    return r.returncode, r.stdout + r.stderr


def ledger(v, fname, body):                     # run_aborted/P2S_S_A_bound_0_1/<fname> 하나를 장부에 두고 다음 잡을 띄워 본다
    pk = fresh(v, f"led_{abs(hash(fname + body))}"); d = os.path.join(pk, "run_aborted", "P2S_S_A_bound_0_1"); os.makedirs(d)
    open(os.path.join(d, fname), "w").write(body)
    rc, log = run(pk, JOBS="P2S_S_A_far")
    why = "미상" if "미상" in log else ("누적" if "누적" in log else "-")
    return f"종료 {rc} · {'다음 잡 뜸' if os.path.isdir(os.path.join(pk, 'run', 'P2S_S_A_far')) else '안 뜸'} · {why}"


def fn_text(v, names):                          # 러너에서 함수 정의만 떼어낸다 (한 줄 함수 '… ; }' 는 그 줄 · 아니면 첫 '\n}\n' 까지)
    t = open(os.path.join(REPO, PK[v], "run_all.sh"), encoding="utf-8").read()
    out = []
    for nm in names:
        i = t.index(f"\n{nm}(){{") + 1
        first = t[i:t.index("\n", i)]
        out.append(first + "\n" if re.search(r";\s*\}\s*(#.*)?$", first) else t[i:t.index("\n}\n", i) + 3])
    return "".join(out)


rows = []
J0 = '{"job": "P2S_S_A_bound", "attempt": "0", "stage": "P", '
for lab, body in (("4.5e5", '"elapsed_s": 4.5e5, "rc": 0}\n'), ("1e12", '"elapsed_s": 1e12, "rc": 0}\n'), ("450000x (뒤 쓰레기)", '"elapsed_s": 450000x, "rc": 0}\n'),
                  ("…: 4 (숫자 중간에서 잘림)", '"elapsed_s": 4'), ("450000 (정상 · 상한 넘음)", '"elapsed_s": 450000, "rc": 0}\n'), ("7200 (정상)", '"elapsed_s": 7200, "rc": 0}\n')):
    rows.append((f"장부 attempt.json elapsed_s {lab}", ledger("old", "attempt.json", J0 + body), ledger("new", "attempt.json", J0 + body)))
for w in ("0450000", "0007200", "08", "18446744073709551616", "7200"):
    b = json.dumps({"job": "P2S_S_A_bound", "rung": "0", "wall_s": w})
    rows.append((f"장부 infra_abort.json wall_s {w}", ledger("old", "infra_abort.json", b), ledger("new", "infra_abort.json", b)))
for v in ("old", "new"):
    open(os.path.join(OUT, f"judge_{v}.sh"), "w").write("set -u\n" + fn_text(v, ["incar_val", "judge"]) + 'judge "$1" "$2"\n')
    open(os.path.join(OUT, f"wsha_{v}.sh"), "w").write(fn_text(v, ["wsha"]) + 'wsha "$1" "$2"\n')
row = lambda i, de, dp: f"DAV: {i:4d}   -0.67E+03   {de}   {dp}  9016   0.341E-03\n"
okrows = "".join(row(i, "-0.1E-02", "-0.1E-03") for i in range(1, 25)) + row(25, "-0.31E-07", "-0.12E-07")
outcar = " vasp.5.4.4 x\n" + "".join(f" Iteration      1( {i:3d})\n" for i in range(1, 26)) + " General timing and accounting\n"
for rv in ("0.5", "1e3", "-0", "0", "-1"):
    d = os.path.join(OUT, "rc", f"rc_{abs(hash(rv))}"); os.makedirs(d)
    for f, t in (("OSZICAR", okrows), ("OUTCAR", outcar), ("INCAR", "NELM = 30\nEDIFF = 1E-6\n"), ("attempt.json", '{"job": "x", "attempt": "0", "rc": ' + rv + ', "elapsed_s": 1}\n')):
        open(os.path.join(d, f), "w").write(t)
    res = {v: (subprocess.run(["bash", os.path.join(OUT, f"judge_{v}.sh"), d, ""], capture_output=True, text=True).stdout.split() or ["(없음)"]) for v in ("old", "new")}
    rows.append((f"judge · attempt.json rc {rv}", " ".join(res["old"][:1] + res["old"][4:5]), " ".join(res["new"][:1] + res["new"][4:5])))
wi = os.path.join(OUT, "wavecar_info.json"); open(wi, "w").write(json.dumps({"sha256": "a" * 64 + "b", "src_sha256": "a" * 64}) + "\n")
for k in ("sha256", "src_sha256"):
    res = {v: subprocess.run(["bash", os.path.join(OUT, f"wsha_{v}.sh"), wi, k], capture_output=True, text=True).stdout.strip() for v in ("old", "new")}
    rows.append((f"wsha · {'65 자' if k == 'sha256' else '64 자'} sha", f"{len(res['old'])} 자" if res["old"] else "빈 값", f"{len(res['new'])} 자" if res["new"] else "빈 값"))
aw = subprocess.run(["awk", "-W", "version"], capture_output=True, text=True); aw = (aw.stdout or aw.stderr).splitlines()[0] if (aw.stdout or aw.stderr) else "?"
if "mawk" not in aw:
    aw = subprocess.run(["awk", "--version"], capture_output=True, text=True).stdout.splitlines()[0]
print(f"# bash {subprocess.run(['bash', '-c', 'echo $BASH_VERSION'], capture_output=True, text=True).stdout.strip()} · awk {aw} · 옛 {OLD} · 새 {NEW}")
print("| 상황 | 옛 | 새 |\n|---|---|---|")
for r in rows:
    print(f"| {r[0]} | {r[1]} | {r[2]} |")
```
