---
title: "DE 프롬프트 — W_ad 외주 2차 묶음 v5 확인: DD 재승인 최소조건 셋 (봉인 필터의 루트 감사 불가 · rc 원문 검증 · 결박 갱신) + 같은 종류 (INCAR 이스케이프 · ENCUT 숫자 꼴) · 발송 승인 여부"
date: 2026-10-22
updated: 2026-10-22
tags: [review, wad, adhesion, vasp, outsourcing, runner, checker, codex, prompt, letter]
letter: DE
track: wad
channel: codex
kind: prompt
status: 발송 2026-10-22 (사용자 · 기준 커밋 9ddfbe448 · 묶음 v5 MANIFEST 714324cc…) → 회신 수령 GO · 발송 동의 (P2 1 — codex_DE_reply_wad_outsourcing_round2_v5_2026_10_22.md)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = W_ad (DEM 협업 · 1저자 = 사용자). DD (v4 NO-GO · P1 2 · 재승인 최소조건 셋) 다음 편지다. 사용자 결정 2026-10-22 *'DC 확인 뒤 업체 (권고)'* 의 연장 — 고친 곳만 확인받고 GO 뒤 업체에 보낸다.
> ⛔ 점착 W 값은 kb 문서에 싣지 않는다 — 이 편지에도 W 숫자를 쓰지 않는다 (문턱 · 비율 · 벽시계만).
> 기준 커밋 `9ddfbe448` (브랜치 `claude/evac-2026-10-22` · 그 뒤 커밋은 kb 만). ⬇ 아래 **보내는 글**만 발송한다 (부록 A · B 포함). 회신이 오면 `codex_DE_reply_…` 로 원문 보존.

---

**[W_ad · 외주 2차] 묶음 v5 확인 — DD 재승인 최소조건 셋 + 같은 종류 · 발송 승인 여부**

## 0. 무엇을 묻나

DD 에서 v4 (MANIFEST `39522906…`) 발송 NO-GO 와 P1 둘 · 재승인 최소조건 셋을 받았다. 둘을 고쳤고, 같은 종류 (실패 기록을 뒤 단계가 거르는 곳 · `awk -v` 로 넘기는 파일 값 · awk 의 숫자 접두부 변환) 를
다시 훑어 judge 의 INCAR 값과 ⓐ WAVECAR 머리 ENCUT 비교를 같이 고쳤다. 묶음은 새 폴더로 다시 만들었다 (**v5 · MANIFEST `714324cc…`**).
이번에도 **고친 곳만** 봐 달라 — **재승인 조건마다 닫혔는가 (GO / 조건부 / NO-GO) · 고치면서 새로 생긴 구멍은 없는가 · v5 를 업체에 보내도 되는가.**
DD 에서 GO 였던 곳 (Q-DD-2 · 3 · Q-DD-5 조건부) 과 설계 · 구조 봉인 · 집계 산식 · 카드 문턱 · 잡 행렬은 다시 열지 않아도 된다.

## 1. 보는 범위 (diff)

- 기준 = DD 를 받은 커밋 `1e4d113d2` (묶음 v4 · MANIFEST `39522906…`). 그 뒤 커밋:
  - `5bec71f8d` · `31603c13c` 편지 DD · 회신 원문 보존 (kb 만)
  - `c4d0f0d39` 고침 (§2 전부 · 시험 · 깨기 목록은 커밋 메시지)
  - `9ddfbe448` 묶음 v5 빌드 · 상태 줄 · 빌드 기록
- `git diff 1e4d113d2 9ddfbe448 -- tools/wad/build_round2_vasp_package.py` (+82 −15 · 대부분 selftest). V5 · interfaces 도구는 안 바뀌었다.
- 묶음 v5 = `db/inputs/wad_round2_vasp_v5_2026_10_22/` · MANIFEST.sha256 의 sha256 `714324cca0d0f05e39966543e3ffa76956fe51109e13f192cad6dc7f8e04cfed`.
  v4 와 다른 파일은 넷 (run_all.sh · README.md 상태 줄 · jobs.json · MANIFEST.sha256) — 잡 입력은 같다. v4 폴더는 검토받은 그대로 둔다 (발송 안 함).
- 빌드 기록 `db/properties/wad_round2_build_log_2026_10_17.json` 의 `⑤-6_DD_고침_2026_10_22`.

## 2. 재승인 조건별로 한 것 (DD 재현 → 지금 막는 시험)

새 음성 시험 넷 + 기존 시험 넓힘 (판정 탐침 둘 · rc 사례 둘) — 전부 **고치기 전 판에서 빨간 것을 확인한 뒤** 고쳤다 (고치기 전 판 + 새 시험 = 180/186).
DD 재현 둘은 DD 가 적은 결과가 그대로 나왔다. 시험 이름은 `⛔음성 DD …`.

**① 봉인 필터가 루트 감사 불가를 버리지 않는다 (DD P1-1)**
- `seal_registry` 의 중단 시도 필터가 `("run_aborted", ATTEMPT_UNREADABLE)` 를 **파일럿 이름 필터보다 먼저 남긴다** → `env_audit` 가 `AUDIT_UNREADABLE` 로 봉인을 거부한다.
  루트를 못 읽었으면 파일럿 관련 중단 시도가 없다고 인증할 수 없다. 이 기록을 거르는 다른 곳은 없다 (`resolve_all` 은 모든 중단 기록을 넘긴다).
- 시험 (DD 재현): 정상 반송 + `run_aborted/P2S_S_A_bound_0_1/` (다른 빌드 OUTCAR 머리줄 · 시작 표지 · 중단 기록 · 전자 스텝 · 완료 기록 없음).
  오류 없이 읽으면 봉인 거부 (대조 · 버전 갈림) · **`os.listdir(run_aborted)` 만** EIO 또는 PermissionError (뒤 scandir 순회는 성공) → `seal_registry` 거부 (`AUDIT_UNREADABLE`) ·
  CLI `--seal_registry` (같은 프로세스 · 주입이 닿게 · V5 등록부는 시험 것) 종료 2 · 등록부 안 만듦 · 깨끗한 반송은 같은 CLI 로 봉인된다 (대조).
  (고치기 전: 봉인됨 · CLI 종료 0 · 등록부 생성 — DD 표 그대로)

**② rc 원문 검증 (DD P1-2) — 값을 변환하지 않는 전달**
- judge 가 rc · term · nrun · nelm · ediff · oit 를 **환경 변수 → awk `ENVIRON`** 으로 넘긴다 (`ENVIRON` 은 이스케이프를 풀지 않는다 · `-v` 는 푼다).
  awk 안의 기존 `rc_unknown` 가지 (`^(0|-?[1-9][0-9]*)$` 가 아니면 `SCF_UNVERIFIED`) 가 원문을 본다 → `\060` · `\061` 은 `rc_unknown`.
  DD 가 준 두 길 중 둘째 (원문 전달) 를 골랐다 — bash 쪽 검사를 되살리면 같은 이스케이프 문제가 nelm · ediff 에 남는다 (아래).
- 시험: attempt.json 의 rc 가 따옴표 없는 `\060` · `\061` → 둘 다 `SCF_UNVERIFIED` (gawk 5.2.1 · mawk 1.3.4 둘 다 selftest 를 돌린다).
  (고치기 전: `\060` → OK · `\061` → RUN_FAILED — DD 설명 그대로 · 우리 Linux 실행으로 확인)

**③ 결박 갱신** — 묶음 v5 를 새로 빌드 · jobs.json `tool_sha256` = 고친 도구 (`80ecbec3…`) · `run_all.sh` = `run_all_text()` · MANIFEST `714324cc…` (§3).

**같은 종류 (우리가 찾음)**
- judge 의 nelm · ediff (INCAR 에서 읽은 값) 도 `-v` 로 넘어가 `NELM = \063\060` 이 30 으로 풀렸다 — 파이썬은 `nelm_unknown` 이라 판정이 갈렸다. `ENVIRON` 으로 같이 고쳤고 판정 탐침 둘 (`nelm_esc` · `ediff_esc`) 을 더했다 (러너 = 파이썬 = `SCF_UNVERIFIED`).
- ⓐ 자격의 WAVECAR 머리 ENCUT 비교 — awk 가 `520abc` 를 520 으로 읽어 ⓑ 를 띄울 수 있었다. 새 `enc_eq()` 는 **숫자 꼴 (러너가 `%.0f` · `%.4f` 로 쓰는 꼴) 만** 비교하고, 검사기 `a_eligible` 도 같은 꼴만 받는다
  (`5.2e2` 를 파이썬 float 이 받아 러너와 갈리던 것도 같이). 시험: `enc_eq` 아홉 사례 + `elig_A` 가 `enc_eq` 를 쓰는지 · `a_eligible` 넷.
- 나머지 `awk -v` 는 확인하고 그대로 뒀다: 잡 이름 · 단계 (알려진 값만 통과) · 해제 파일 상한 (`cap_num` 정규식 뒤) · 우리가 만든 sha · run_id · 초 (`secs_ok` 뒤).
  `--infra-wall` 의 표 (`infra_aborts.tsv`) 고치기는 정보용이다 (장부는 json 을 읽는다 · 폴더 이름은 러너가 검증된 잡 · 단 · 번호로 만든다).

**P2 두 가지 (DD 지적대로 고침)**
- 미등록 흔적 보장 범위 — `unregistered_traces` docstring 을 **"반송물에 포함되어 검사기에 도착한 실행 흔적에 대해 미등록 경로를 차단한다 · 업체 작업 트리 전체의 실행 부재를 인증하지는 않는다"** 로 고치고,
  포장의 경로 필터 (stageA 말고 다른 하위 폴더 · `run/` 바로 아래 파일은 안 담긴다) 를 한계로 적었다.
- rc=-0 — DD 편지의 '검사기는 같은 기록을 ATTEMPT_MISMATCH 로 본다' 는 -0 에서 틀렸다. 파이썬 JSON 은 -0 을 정수 0 으로 읽어 검사기는 OK · 러너는 보수적으로 `SCF_UNVERIFIED` — 보수 쪽 비대칭으로 둔다.

**깨기** — 고침을 한 부분씩 되돌린 사본 7 — 첫 판 전부 빨강, 각자 기대한 시험으로 (봉인 필터 · rc 를 -v 로 (기대 빨강 둘) · nelm 을 -v 로 · ediff 를 -v 로 · enc_eq 숫자 꼴 없음 · elig_A 가 enc_eq 를 안 씀 · a_eligible 숫자 꼴 없음).

## 3. 배포본 확인

검사기 = 도구 sha `80ecbec3…` (v5 jobs.json 의 tool_sha256 과 같다) · 러너 = v5 `run_all.sh` (= `run_all_text()`). Linux · bash 5.2.21 · gawk 5.2.1 · mawk 1.3.4.

- (가) selftest **186/186** (두 awk).
- (나) 배포본 위 selftest (부록 A · 종료 코드가 판정): v5 사본 위 selftest 184/186 · 빨강 정확히 예상한 둘 (DIPOL 구간 · 두 번째 빌드 MANIFEST sha) · 그 밖 0 · **감싸개 종료 0** · gawk · mawk 같다.
- (다) 러너 전후 대조 — 배포 러너 v4 (DD 가 본 판) 와 v5 를 같은 반송 상태에 둠 (부록 B · 두 awk 결과 같음):

| 상황 | v4 러너 (DD 가 본 판) | v5 러너 |
|---|---|---|
| 장부 attempt.json elapsed_s 4.5e5 | 종료 5 · 안 뜸 · 미상 | 종료 5 · 안 뜸 · 미상 |
| 장부 attempt.json elapsed_s 1e12 | 종료 5 · 안 뜸 · 미상 | 종료 5 · 안 뜸 · 미상 |
| 장부 attempt.json elapsed_s 450000x (뒤 쓰레기) | 종료 5 · 안 뜸 · 미상 | 종료 5 · 안 뜸 · 미상 |
| 장부 attempt.json elapsed_s …: 4 (숫자 중간에서 잘림) | 종료 5 · 안 뜸 · 미상 | 종료 5 · 안 뜸 · 미상 |
| 장부 attempt.json elapsed_s 450000 (정상 · 상한 넘음) | 종료 5 · 안 뜸 · 누적 | 종료 5 · 안 뜸 · 누적 |
| 장부 attempt.json elapsed_s 7200 (정상) | 종료 1 · 다음 잡 뜸 · - | 종료 1 · 다음 잡 뜸 · - |
| 장부 infra_abort.json wall_s 0450000 | 종료 5 · 안 뜸 · 미상 | 종료 5 · 안 뜸 · 미상 |
| 장부 infra_abort.json wall_s 0007200 | 종료 5 · 안 뜸 · 미상 | 종료 5 · 안 뜸 · 미상 |
| 장부 infra_abort.json wall_s 08 | 종료 5 · 안 뜸 · 미상 | 종료 5 · 안 뜸 · 미상 |
| 장부 infra_abort.json wall_s 18446744073709551616 | 종료 5 · 안 뜸 · 미상 | 종료 5 · 안 뜸 · 미상 |
| 장부 infra_abort.json wall_s 7200 | 종료 1 · 다음 잡 뜸 · - | 종료 1 · 다음 잡 뜸 · - |
| judge · attempt.json rc 0.5 | SCF_UNVERIFIED rc_unknown | SCF_UNVERIFIED rc_unknown |
| judge · attempt.json rc 1e3 | SCF_UNVERIFIED rc_unknown | SCF_UNVERIFIED rc_unknown |
| judge · attempt.json rc -0 | SCF_UNVERIFIED rc_unknown | SCF_UNVERIFIED rc_unknown |
| judge · attempt.json rc 0 | OK - | OK - |
| judge · attempt.json rc -1 | RUN_FAILED rc_or_not_terminated | RUN_FAILED rc_or_not_terminated |
| judge · attempt.json rc \060 | OK - | SCF_UNVERIFIED rc_unknown |
| judge · attempt.json rc \061 | RUN_FAILED rc_or_not_terminated | SCF_UNVERIFIED rc_unknown |
| judge · INCAR NELM = \063\060 | OK - | SCF_UNVERIFIED nelm_unknown |
| judge · INCAR EDIFF = \061E-6 | OK - | SCF_UNVERIFIED ediff_unknown |
| wsha · 65 자 sha | 빈 값 | 빈 값 |
| wsha · 64 자 sha | 64 자 | 64 자 |

## 4. 이것을 특히 봐 달라

1. **② 의 길** — bash 쪽 검사를 되살리지 않고 `ENVIRON` 으로 원문을 넘겼다. 같은 이유로 judge 의 다른 값도 다 `ENVIRON` 이다. `ENVIRON` 값도 `-v` 처럼 숫자처럼 보이면 숫자 문자열로 다뤄져 (POSIX) 비교 결과가 같다 —
   판정 탐침 44 개가 두 awk 에서 파이썬과 같다.
2. **ENCUT 숫자 꼴** — 러너와 검사기가 같은 꼴만 받는다. 러너가 쓰는 머리 (`%.0f` · `%.4f`) 와 OUTCAR 의 `ENCUT = 520.0 eV` 는 이 꼴이다.

## 5. 질문

- **Q-DE-1**: 재승인 조건 ① (봉인 필터 · listdir 만 실패하는 CLI 봉인 음성) 이 닫혔는가.
- **Q-DE-2**: 조건 ② (rc 원문 검증 · `\060` · `\061` 양쪽 awk 보류) 가 닫혔는가.
- **Q-DE-3**: 조건 ③ (도구 해시 · 러너 · MANIFEST 결박) 이 맞는가.
- **Q-DE-4**: 같은 종류 (INCAR 이스케이프 · ENCUT 숫자 꼴) 와 P2 두 문구가 맞는가 · 고치면서 새 구멍은 없는가.
- **Q-DE-5**: 발송 승인 — 묶음 v5 (MANIFEST `714324cc…`) 를 업체에 보내도 되는가.

## 6. 바뀌지 않은 것

카드 문턱 · 잡 행렬 24 · 사다리 INCAR · 집계 산식 · 구조 봉인 · 단계 상한 값 · 결정 둘 (`D-2026-10-15-wad-p2small-vasp-card` · `D-2026-10-15-wad-aprime-v5-e70-a4-rerun` · active) ·
재시도 규칙 · 업체 명령 · README (상태 줄만).

## 7. 재현 방법

- `python3 -I tools/wad/build_round2_vasp_package.py --selftest` — DD 사례는 `⛔음성 DD`. mawk 로는 `mkdir /tmp/m && ln -s "$(command -v mawk)" /tmp/m/awk && PATH=/tmp/m:$PATH python3 -I …`.
- `python3 -I tools/wad/build_round2_vasp_package.py --build --seal db/inputs/wad_p2small_seal_2026_10_17 --out <새 폴더>` → `diff -r` · MANIFEST sha 대조.
- 부록 A · B 는 저장소 뿌리에서 돌린다 (둘 다 저장소에는 없는 검증용 스크립트 · 아래 원문 그대로).

### 부록 A — 배포본 위 selftest 감싸개 (`python3 run_on_deployed.py db/inputs/wad_round2_vasp_v5_2026_10_22` · 종료 0 = 통과)

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

### 부록 B — 러너 전후 대조 (`python3 runner_contract.py db/inputs/wad_round2_vasp_v4_2026_10_22 db/inputs/wad_round2_vasp_v5_2026_10_22 <빈 작업 폴더>` · mawk 는 PATH 앞에 mawk 를 awk 로)

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
for rv in ("0.5", "1e3", "-0", "0", "-1", "\\060", "\\061"):
    d = os.path.join(OUT, "rc", f"rc_{abs(hash(rv))}"); os.makedirs(d)
    for f, t in (("OSZICAR", okrows), ("OUTCAR", outcar), ("INCAR", "NELM = 30\nEDIFF = 1E-6\n"), ("attempt.json", '{"job": "x", "attempt": "0", "rc": ' + rv + ', "elapsed_s": 1}\n')):
        open(os.path.join(d, f), "w").write(t)
    res = {v: (subprocess.run(["bash", os.path.join(OUT, f"judge_{v}.sh"), d, ""], capture_output=True, text=True).stdout.split() or ["(없음)"]) for v in ("old", "new")}
    rows.append((f"judge · attempt.json rc {rv}", " ".join(res["old"][:1] + res["old"][4:5]), " ".join(res["new"][:1] + res["new"][4:5])))
for lab, inc in (("NELM = \\063\\060", "NELM = \\063\\060\nEDIFF = 1E-6\n"), ("EDIFF = \\061E-6", "NELM = 30\nEDIFF = \\061E-6\n")):   # INCAR 값의 이스케이프 (awk -v 가 풀면 30 · 1E-6 이 된다)
    d = os.path.join(OUT, "inc", f"inc_{abs(hash(lab))}"); os.makedirs(d)
    for f, t in (("OSZICAR", okrows), ("OUTCAR", outcar), ("INCAR", inc), ("attempt.json", '{"job": "x", "attempt": "0", "rc": 0, "elapsed_s": 1}\n')):
        open(os.path.join(d, f), "w").write(t)
    res = {v: (subprocess.run(["bash", os.path.join(OUT, f"judge_{v}.sh"), d, ""], capture_output=True, text=True).stdout.split() or ["(없음)"]) for v in ("old", "new")}
    rows.append((f"judge · INCAR {lab}", " ".join(res["old"][:1] + res["old"][4:5]), " ".join(res["new"][:1] + res["new"][4:5])))
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
