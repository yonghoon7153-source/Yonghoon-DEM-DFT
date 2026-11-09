---
title: "DW 회신 — 셀구축 v1.1 · b2o3 B·O 배치 카드 개정 1 v1.1 해제조건 확인: NO-GO · DV 묶음 1–3 닫힘 · 묶음 4 (판독기) 단계 연결 미해제 · P1 3 (단계 결속 · 파일럿 시간축 · EOS 기준 순서) · P2 비유한 기하 · P3 관측창 근사"
date: 2026-11-09
updated: 2026-11-09
tags: [review, b2o3, cell-construction, uma, readout, pilot, eos, codex, reply, letter]
letter: DW
track: b2o3
channel: codex
kind: reply
status: 회신 원문 (2026-11-09 · 사용자 붙여넣기) — NO-GO · 기준 커밋 837cc6e8 (evac 브랜치) · 생산 계산 안 함 · 재현 수치는 합성 시험 값 · 조건부 비준 ('go면 비준') 미충족
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 프롬프트 `codex_DW_prompt_cell_construction_v1_1_release_2026_11_09.md` 에 대한 Codex 회신 **원문 그대로** (사용자가 2026-11-09 대피 세션에 붙여 넣음). 고치지 않는다.
> 링크의 `C:/Users/Administrator/Documents/Codex/...` 경로는 Codex 쪽 작업 사본이다 (이 저장소 경로가 아니다).
> 맨 아래 부록 셋은 사용자가 회신과 같이 붙여 넣은 검증 기록 · 재현 스크립트 · 재현 결과 JSON 이다 — 내용 그대로 (`probe_results.json` 은 공백 · 줄바꿈만 접었다 · 파싱 확인 18 키).
> ⚠ 사용자의 조건부 비준 (*'go면 비준이야'* · 결정 원장 status_history) 은 **GO 에만** 걸려 있다 — 이 회신은 NO-GO 라 두 결정은 proposed 그대로다.

---

NO-GO — DV 묶음 1–3은 닫혔지만, 묶음 4의 판독기가 단계 사이의 입력·선택·시간을 충분히 대조하지 않습니다.

837cc6e8에 고정해 확인했습니다. 원본 저장소는 수정하지 않았고, 생산 UMA·DFT·MD는 실행하지 않았습니다. 아래 반례는 합성 구조·에너지·궤적을 사용했습니다.

자가시험은 모두 통과했습니다: 큐 5건, 어닐 27건, 생성기 40건, 판독기 21건, 포논 11건, 골격 판독·집계 24+15건. 그 상태에서도 아래 경로가 통과했습니다. 새 P0는 확인하지 않았습니다.

P1-1 · 1단계 전 필수 — 판독기가 다른 배치·시간·계획 집합을 받아 승자를 냅니다.

위치: [b2o3_bo_readout.py (line 114)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DW_20261109/source/tools/doping/b2o3_bo_readout.py:114), [247 (line 247)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DW_20261109/source/tools/doping/b2o3_bo_readout.py:247), [596 (line 596)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DW_20261109/source/tools/doping/b2o3_bo_readout.py:596).

manifest_map()은 생성본을 검증한 뒤 이름·바탕 순위·가족만 넘깁니다. 결과의 입력 해시는 그 생성본 또는 앞 단계 산출물과 대조되지 않습니다. anneal 명령에는 파일럿 판정 입력도 없습니다.

직접 확인한 경우입니다.
입력 상태	실제 판독
정상적인 128원자 생성 manifest에 이름만 같은 6원자 합성 결과 연결 — 결과 파일 해시·자체 조성은 일치	CLI 종료 0, G1 전부 통과, 승자 F_B
결과의 identity 제거	승자 출력
파일럿은 100 ps 선택, 어닐 결과는 20 ps	승자 출력
어닐 결과가 카드의 500 K 대신 1000 K	승자 출력
계획 6개 중 F_P 성공 4개	전체 합집합으로 읽으면 G1 실패
같은 결과에서 전달하는 합집합만 4개로 축소	G1 통과로 바뀌고 승자 출력


거름에도 같은 문제가 있습니다. 기대 기록 18개 중 3개만 주면 missing=15를 기록하면서도 M=1과 파일럿 구조를 내놓습니다. 경고를 붙인 미완료 결과가 다음 단계에서 계획으로 사용될 수 있습니다.

최소 수정: 기존 JSON 사이에 다음 대조를 연결하면 됩니다.
- 생성 manifest ↔ 거름 결과의 실제 입력.
- 완결된 거름 결과 ↔ 선택한 합집합·파일럿.
- 파일럿의 t_a ↔ 어닐의 시간·온도·실행 조건.
- 어닐 계획의 전체 집합 ↔ G1 분모.
각 단계가 어떤 파일에서 시작하는지도 고정해야 합니다. 원래 CIF인지, 6단계 이완본인지 선언하고 그 파일 해시를 대조하세요. 정체성 부재와 다른 배치의 결과는 거부해야 합니다. 지금처럼 결과 파일이 자기 기록과 일치하는 것만으로는 부족합니다.
P1-2 · 1단계 전 필수 — 파일럿의 시각을 사용자가 다시 붙일 수 있습니다.

위치: [b2o3_bo_readout.py (line 183)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DW_20261109/source/tools/doping/b2o3_bo_readout.py:183), [210 (line 210)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DW_20261109/source/tools/doping/b2o3_bo_readout.py:210).

extract는 명령행의 dt_fs × log_every를 그대로 시간축으로 사용합니다. 이를 실제 실행 기록이나 카드와 대조하지 않습니다.

재현: 실제로 1 ps 간격으로 저장한 0–10 ps 합성 궤적에 --dt_fs 20 --log_every 500을 주면, 실제 2·5·10 ps 프레임을 20·50·100 ps로 추출합니다. 오류가 없습니다.

또한 정상 스냅숏 기록에서 궤적 경로를 없는 파일로, 궤적 해시를 전부 0으로, 세 프레임 번호를 모두 0으로 바꿔도 pilot()은 t_a=100 ps를 냈습니다. 현재 검사하는 것은 주로 스냅숏 해시와 이완 입력 해시의 일치입니다. 그 스냅숏이 어느 궤적의 어느 시각인지는 확인하지 않습니다.

최소 수정: 저장 간격·실행 길이를 결속된 실행 기록에서 읽고, 선택된 파일럿 입력 → 연속 궤적 → 프레임·시각 → 스냅숏 → 이완 결과를 대조하세요. dt_fs와 log_every를 받더라도 기록·카드와 다르면 멈춰야 합니다.

max−min 규칙 자체와 0 / −0.30 / −0.02 → 100 ps 판정은 맞습니다. 그 규칙에 들어오는 세 시점의 자격이 아직 열려 있습니다.
P1-3 · DFT 단계 전 필수 — EOS 생략 판정이 보정 전 순서를 보지 않습니다.

위치: [b2o3_bo_readout.py (line 332)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DW_20261109/source/tools/doping/b2o3_bo_readout.py:332).

지금 비교하는 것은 각 보정 조합의 승자와 0.10 eV 통과 여부입니다. 보정 전 판정과의 일치, 전체 가족 순서의 일치는 검사하지 않습니다.

합성 입력 (E[eV], P[GPa], V[Å³])으로 재현했습니다.
- F_B = (-0.15, 0, 2436.33)
- F_P = (0, 2, 2436.33)
- F_free = (0.5, 0, 2436.33)
보정 전 승자는 F_B, 독립 B의 8개 조합에서 보정 후 승자는 모두 F_P인데 skip_eos=True입니다.

별도 반례에서는 승자 F_B가 유지되지만 차저·셋째의 순서가 바뀌어도 skip_eos=True였습니다. 이는 선언한 “보정 뒤에도 가족 순서·판정이 그대로”와 다릅니다.

최소 수정: 보정 전 전체 순서와 0.10 판정을 먼저 계산하고, 모든 독립 B 조합이 그것을 유지하는지 검사하세요.

이 항목은 DFT 진입 전 조건입니다. 이것만을 이유로 UMA 시작을 막을 필요는 없습니다.
P2 · 판독 전 수정 — NaN 좌표가 F_free로 분류됩니다.

위치: [b2o3_bo_readout.py (line 66)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DW_20261109/source/tools/doping/b2o3_bo_readout.py:66), [127 (line 127)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DW_20261109/source/tools/doping/b2o3_bo_readout.py:127).

유한 에너지와 일치하는 파일 해시·조성을 주되 O 좌표를 NaN으로 만든 파일에서:

verify_outputs=[] → load_ok=True → end_motif=F_free

가 나왔습니다. 생산 결과에서 발생했다는 뜻은 아닙니다. 잘못된 기하를 넣었을 때의 실제 판독 결과입니다.

최소 수정은 좌표·셀의 유한성과 셀의 비퇴화를 분류 전에 검사하는 것입니다. 실패는 invalid로 남기고 성공 수에서 제외해야 합니다. 기존의 파일 교체·삭제 방어는 정상 작동합니다.

P3 · 관측창 식의 근사 표시만 정리하면 됩니다.

[decisions.json (line 11877)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DW_20261109/source/db/governance/decisions.json:11877)의 /3은 근사입니다. 적어 둔 0.67991 eV는 정확한 분모 −ln(0.05)로 계산한 값입니다.

정확식을 쓰거나, /3에 ≈를 붙이고 0.68 eV로 쓰면 됩니다. 발사 차단 사유는 아닙니다.

Q1. DV 네 묶음은 닫혔나?
묶음	판정	확인 내용
① 큐 실패 전파	닫힘	실행/검사 (0,0),(0,1),(7,0),(7,1) → 종료 0,13,7,7
② 완료 구조·대기 뒤 입력 결속	요청된 반례는 닫힘	결과 교체·삭제 거부, 제출 뒤 입력 변경은 종료 12·실행 0회. Windows 자가시험도 통과
③ 생성 짝 검증	닫힘	기존 135구조 정상 통과. 다른 부모 자식 교환은 해시·O 자리를 맞춰도 거부. Li 후보 보고서 삭제·변경 거부
④ 판독기·음성시험	부분 이행, 미해제	G3 분모·차저 여유·파일럿 산술은 맞음. 위 단계 연결 반례가 남음


②의 수정이 무효라는 뜻은 아닙니다. 완료 기록과 파일의 결속은 고쳤고, 그 기록이 이번 판독 대상인지 확인하는 연결이 새 판독기에 빠진 것입니다.

Q2. 판독 계약의 남은 빈칸은?

1.8/2.3 Å, 가교→mixed, 보류 네 조건, 짝 n<3은 지금 선언한 운영 분류로 사용할 수 있습니다. 이번 검토에서 그 숫자를 새로 바꿀 근거는 발견하지 못했습니다.

다만 결과 전에 다음 둘은 닫아야 합니다.
- 미실행·기록 누락과 명시적 실패를 구분하세요. 누락이 있으면 거름 완료로 승격하지 않아야 합니다.
- 전부 시도했지만 한 가족의 성공이 6개 미만이면 어떻게 할지 정하세요. 현재의 “있는 것만 넣는다”는 경고가 계획 변경을 대신하면 안 됩니다. 선언한 k_f=6을 유지하려면 우선 보류가 자연스럽습니다.
G1 분모와 파일럿 선택을 완결된 거름 결과에 묶으면, 결과를 보고 표본을 줄이는 경로도 함께 닫힙니다.

Q3. 포논 빈 캐시·B 결합 분류는 충분한가?

DV가 지적한 두 구현 결함은 닫혔습니다.
- 포논: A → 캐시 비움 → B → A에서 마지막 A가 거부됩니다. B의 힘을 A의 캐시로 읽는 경로가 차단됐습니다.
- 골격: BS₃ 강체 회전은 사건 0, B–S 이탈은 B-bonded 사건으로 잡힙니다. v1/v2 혼합 집계도 거부합니다.
B 문턱을 P와 같게 두는 것은 사용자가 비준한 기하학적 사건 정의로는 가능합니다. 이 시험이 B–S/B–O의 물리적 결합 문턱까지 검증한 것은 아닙니다. 문턱과 census 판을 기록하고, 허용 서술을 선언한 사건 수 범주로 유지하세요.

이 두 수정의 통과가 후속 생산 실행 승인 전체를 뜻하지는 않습니다. 포논 입력 재이완, 1단계 판독, 골격 MD의 별도 발사 조건은 그대로입니다.

Q4. 관측창 개정안은 맞나?

맞습니다. 기대 사건 수가 1인 지점을 절대 관측 한계처럼 쓰던 오류를 바로잡았습니다.

정상 포아송 가정에서 정확한 식은:
\[
E_{a,95}=kT\ln\!\left(\frac{\nu_0tn}{-\ln(0.05)}\right)
\]
1000 K·0.8 ns·n=1로 재계산하면:
- 기대 사건 1: 0.77446 eV
- 95% 검출: 0.67991 eV
- 그 첫 장벽보다 0.10 eV 높을 때 검출 확률: 26.9%
모두 맞습니다. n은 선언한 등가 반응 기회 수이며, 원자 수를 자동 대입하거나 서로 다른 온도의 시간을 단순 합산하지 않는다는 전제를 유지하면 됩니다. 비준 전 원문·실행 문구를 보존하는 처리에도 동의합니다.

1단계 시작 전 마지막 확인 목록
1. 생성본·거름 결과·합집합·파일럿·어닐 입력을 연결하고, G1 분모와 t_a를 그 연결에서 읽게 하기.
2. 파일럿 시간축을 실제 실행 기록과 대조하고, 잘못된 간격·짧은 궤적·다른 파일럿을 거부하기.
3. 위 반례와 비유한 기하를 막는 시험을 넣되, 정상 묶음이 통과하는 양성 경로도 함께 확인하기.
4. 그 판독 계약을 포함한 유효 개정 v1.1을 사용자 비준으로 확정하기.
EOS 수정은 별도 DFT 진입 조건으로 남겨도 됩니다.

재현 자료: [검증 기록](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DW_20261109/VERIFICATION.md) · [독립 재현 스크립트](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DW_20261109/probe_dw.py) · [재현 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DW_20261109/probe_results.json).

---

## 부록 A — VERIFICATION.md (사용자 붙여넣기 · 원문)

```markdown
# DW independent verification — 2026-11-09

Target: `837cc6e8be87118bae5cd62230a3ab7ed4a3fcbc`, branch `claude/evac-2026-11-08`.
Comparison: `ad4f41b8c79920947e7f8b0b52b72a129052a537`.
Original repository unchanged. Only this review snapshot and synthetic fixtures were written.
No production UMA, DFT, or MD was executed. ASE synthetic/Lennard-Jones selftests and geometry readers were executed.

## Environment and selftests

Windows; bundled Python; ASE 3.29.0 from `../review_v37_20260907/runtime_deps`.
`run_selftest.py` redirects temporary files into the review scratch directory.

| Tool | Observed result |
|---|---|
| run_uma_kgy.sh --selftest | 5/5, exit 0; Git Bash, mock python/nvidia-smi |
| run_anneal.py --selftest | 27 assertions passed, exit 0; native Windows |
| b2o3_enumerate.py --selftest | 40/40, exit 0 |
| b2o3_bo_readout.py --selftest | 21/21, exit 0 |
| uma_phonon.py --selftest | 11 assertions passed, exit 0 |
| framework_site_census.py --selftest | 24 census + 15 aggregate, exit 0 |

Git Bash initially failed before executing the script due to MSYS named-object sandbox permissions; the identical mock selftest succeeded with the permitted sandbox override.

## Confirmed DV closures

- Queue outcomes (run, check) `(0,0),(0,1),(7,0),(7,1)` -> exit `0,13,7,7`.
- Changed submitted input -> exit 12, mock calculation invocation count zero.
- Output replacement/deletion rejected by verify_outputs and resume paths. Windows temporary-directory cleanup succeeds.
- Previous actual 45-base/135-child generation passes the new verifier.
- Previous cross-parent swap artifact, with updated child hashes and O-site declarations, now produces four problems.
- Missing and changed Li-candidate reports rejected.
- G3 2/5 versus 2/6, winner-versus-runner-up 0.01, pilot 0/-0.30/-0.02, independent-B EOS negative cases pass the supplied tests.
- Empty-cache phonon identity transition and BS3 rigid-rotation/B-S departure tests pass; mixed census versions rejected.

## Remaining reproduced findings

### P1-A: stage handoffs are not bound (UMA stage-1 release blocker)

`b2o3_bo_readout.py:114,127,152,247,596`.

- Actual valid 128-atom generated manifest + same-name synthetic six-atom results with valid output hashes -> CLI exit 0, winner F_B, all G1 true, six pairs. Identity is constructed using production run_identity and identity_sha. The reader joins names without comparing expected input fingerprints/composition.
- Missing identity also yields a winner.
- Pilot test chooses 100 ps. The anneal reader independently accepts 20 ps records; 1000 K records also pass although the card specifies 500 K. No pilot verdict is an input to this command.
- Six-base plan, four successful P-family rows: full union -> G1 fail/hold. Passing only four bases as union -> G1 true/winner without changing any energies.
- 18 expected screen records, only three supplied -> M=1 and a selected pilot, merely accompanied by warnings.

Minimum fix: bind generated manifest, screen source records, complete selected cohort, pilot receipt and expected anneal identities; reject missing/duplicate/foreign records as appropriate. G1 denominator must come from the complete pre-anneal cohort, not an unbound union list. Distinguish unrun/missing from recorded failure; preregister policy if fewer than six successful screen candidates remain.

### P1-B: pilot clock/trajectory provenance is recorded but not checked (UMA stage-1 release blocker)

`b2o3_bo_readout.py:183,210`.

- A synthetic trajectory containing frames at real 0..10 ps, one ps apart, is extracted with dt_fs=20/log_every=500. Actual 2/5/10 ps frames become labeled 20/50/100 ps without rejection.
- A valid pilot receipt changed to a nonexistent trajectory, all-zero trajectory hash, and frame zero at all times still produces t_a=100 ps.

Minimum fix: derive cadence and total duration from the bound production run record, bind the run input to the screen-selected pilot, and validate trajectory/snapshot identities and frame-time correspondence before deciding t_a. A valid snapshot-to-relax hash alone does not establish the snapshot's time/source.

### P1-C: EOS skip criterion ignores uncorrected ranking and lower ranks (DFT-stage prerequisite)

`b2o3_bo_readout.py:332-358`; protocol `9_DFT_확인` requires preservation before/after correction.

- Synthetic `(E,P,V)` values: F_B=(-0.15,0,2436.33), F_P=(0,2,2436.33), F_free=(0.5,0,2436.33). Baseline winner F_B; every independent-B corner winner F_P; skip_eos=True.
- F_B=(-5,0,2436.33), F_P=(0,2,2436.33), F_free=(0.15,2,2436.33): runner-up and third swap at corners; skip_eos=True because only winner and threshold boolean are compared.

Minimum fix: every independent-B corner must preserve the baseline full order and baseline 0.10-eV winner/runner-up decision, as declared by the protocol. Do not require EOS implementation to be fixed before UMA if it is explicitly deferred to the DFT entry gate.

### P2: nonfinite geometry is classified as free O

`b2o3_bo_readout.py:66,127`; `run_anneal.py:253`.

Finite energy, NaN O coordinates, matching output hashes/composition -> verify_outputs=[], load_ok=True, end_motif=F_free. Synthetic file fixture, not an observation of a production calculation.
Minimum fix: finite positions and finite, nonsingular cells before motif classification; invalid geometry is not successful or F_free.

### P3: observation-window approximation precision

`db/governance/decisions.json:11877`.
At 1000 K, 0.8 ns, n=1: Ea1=0.77445670096 eV; exact 95% uses -ln(0.05) and gives 0.67990829414 eV; replacing this denominator by 3 gives 0.67978561879 eV. Detection at Ea1+0.10 is 0.2690020152.
Use exact -ln(0.05), or mark /3 approximate and report 0.68 eV. No launch-blocking physical disagreement.

## Evidence artifacts

- `probe_dw.py`, `probe_results.json`: independent on-disk counterexamples and actual-generator CLI invocation.
- `probe_dw_extra.py`, `probe_extra_results.json`: nonfinite geometry, ordinary output integrity, Poisson arithmetic.
- `probes/cli_verdict.json`: actual CLI false acceptance.
- `*_selftest.log`: unmodified source selftest outputs.
- `source_hashes.json`: reviewed source SHA-256 values; `_provenance.py` Git blob is `118aab30e4bdad1b01cc48e5cee379c073a2577f`.

The independent probe scripts record observations; they are not an assertion that the failing gates are fixed. Energies and trajectories in these fixtures are synthetic and must not be used as scientific campaign results.
```

## 부록 B — probe_dw.py (사용자 붙여넣기 · 원문)

```python
"""Independent DW boundary tests; synthetic structures/energies only, no UMA/DFT/MD."""
from pathlib import Path
import importlib.util, json, sys, copy, hashlib, subprocess, tempfile
import numpy as np
from ase import Atoms
from ase.io import read, write
from ase.io.trajectory import Trajectory

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'source'
OUT = ROOT / 'probes'
OUT.mkdir(exist_ok=True)
tempfile.tempdir = str(ROOT / 'scratch')
sys.dont_write_bytecode = True
sp = importlib.util.spec_from_file_location('dw', SRC/'tools/doping/b2o3_bo_readout.py')
m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
R = {}
def save(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return p
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# Actual DV generation and fault artifacts, rechecked with DW verifier.
old = ROOT.parent/'review_DV_20261109/dv_enumeration'
for key in ['actual_45x3','fault_crossbase_contents','fault_missing_li_report','fault_corrupt_li_report']:
    try: probs = m._EN.verify_manifest(old/key)
    except BaseException as e: probs = [str(e)]
    R['manifest_'+key] = probs

def toy(kind):
    b=np.array([2.,2.,2.]); p=np.array([8.,8.,8.]); u=np.eye(3)
    o=([b+1.45*d for d in u] if kind=='F_B' else
       [p-1.55*d for d in u] if kind=='F_P' else
       [np.array([5.,5.,5.])+0.8*d for d in u])
    return Atoms('BPO3S',positions=[b,p]+o+[np.array([10.,2.,10.])],cell=[12]*3,pbc=True)

# Fresh on-disk records use the production identity constructor and output schema.
def records(sub, mmap, stage='anneal_relax', time=100, temp=500, hashes=None,
            statuses=None, energies=None, wrong_inputs=False, missing_identity=False):
    dest=OUT/sub; dest.mkdir(exist_ok=True)
    rows=[]
    for n,(rank,F) in mmap.items():
        a=toy(F); ip=dest/'inputs'/f'{n}.xyz'; ip.parent.mkdir(exist_ok=True)
        write(ip,a)
        if wrong_inputs:
            a.positions[-1] += [0.33,0,0]; write(ip,a)
        work=dest/n; work.mkdir(exist_ok=True)
        for k in ['post_md','post_relax']: write(work/f'{k}.xyz',a)
        identity=m._RA.run_identity(ip,temperature_K=temp,time_ps=(0 if stage=='relax_only' else time),
            dt_fs=2,friction=.002,relax_steps=500,relax_fmax=.05,cell_relax=False,seed=20261109,model='uma-s-1p1')
        if hashes and n in hashes: identity['input_file_sha256']=hashes[n]
        st=(statuses or {}).get(n,'converged')
        e=(energies or {}).get(n, {'F_B':-.5,'F_P':0.,'F_free':-.2}[F]+.01*rank)
        rows.append(dict(name=n,status=st,converged=(st=='converged'),E_post_relax=e,
            identity=identity,identity_sha=m._RA.identity_sha(identity),
            composition=m._RA._composition(a),outputs={k:dict(rel=f'{n}/{k}.xyz',sha256=sha(work/f'{k}.xyz')) for k in ['post_md','post_relax']}))
        if missing_identity:
            rows[-1].pop('identity'); rows[-1].pop('identity_sha')
    return save(dest/'anneal_results.json',dict(results=rows))

codes={'F_B':'bo4','F_P':'distributed','F_free':'free_s'}
mm={f'cfg{b:04d}_O-{codes[F]}':(b,F) for b in range(6) for F in m.FAM_ORDER}
def brief(v):
    return {k:v.get(k) for k in ['winner','decision','n_pairs','hold_reasons']} | {
        'M':{f:x['M'] for f,x in v['families'].items()},
        'G1':{f:x['G1'] for f,x in v['families'].items()}}

base=records('anneal_good',mm)
R['positive_anneal']=brief(m.anneal_readout(mm,m.load_records(base),list(range(6))))

# Pilot requires 100 ps but downstream accepts 20 ps (and wrong temperature).
for sub,t,T in [('anneal_wrong_length',20,500),('anneal_wrong_temperature',100,1000)]:
    p=records(sub,mm,time=t,temp=T)
    R[sub]=brief(m.anneal_readout(mm,m.load_records(p),list(range(6)))) | dict(actual_time=t,actual_T=T)

# No expected input fingerprint is compared. Names alone join generation to results.
p=records('anneal_other_inputs',mm,wrong_inputs=True)
R['other_input_same_names']=brief(m.anneal_readout(mm,m.load_records(p),list(range(6))))
p=records('anneal_missing_identity',mm,missing_identity=True)
R['missing_identity']=brief(m.anneal_readout(mm,m.load_records(p),list(range(6))))

# A complete plan of six bases has four successful P-family rows -> G1 fail.
# Shrinking the unbound screen union to those four makes it pass.
statuses={f'cfg{b:04d}_O-distributed':'failed' for b in (4,5)}
p=records('anneal_incomplete',mm,statuses=statuses)
rr=m.load_records(p)
R['full_union_failed']=brief(m.anneal_readout(mm,rr,list(range(6))))
R['short_union_passed']=brief(m.anneal_readout(mm,rr,list(range(4))))

# Partial screen, with most missing, yields a usable union + selected pilot.
p=records('screen_partial',{n:v for n,v in mm.items() if v[0]<1},stage='relax_only')
R['screen_partial']=m.screen(mm,m.load_records(p))

# All three relaxation inputs are bound to snapshot hashes, but the source trajectory
# can disappear, or the receipt's frame/time fields be wrong, without affecting pilot.
traj=OUT/'pilot/md.traj'; traj.parent.mkdir(exist_ok=True)
with Trajectory(traj,'w') as tr:
    for i in range(101): tr.write(toy('F_B'))
prov=m.extract_snapshots(traj,[20,50,100],2,500,OUT/'pilot','pilot')
pm={f'pilot_t{t:03d}':(0,'F_B') for t in (20,50,100)}
hs={f'pilot_t{t:03d}':prov['snapshots'][str(t)]['sha256'] for t in (20,50,100)}
p=records('pilot_relaxed',pm,stage='relax_only',hashes=hs,
          energies={'pilot_t020':0.,'pilot_t050':-.30,'pilot_t100':-.02})
pr=m.load_records(p)
R['pilot_positive']=m.pilot(prov,pr,'pilot')
broken=copy.deepcopy(prov)
broken['traj']=str(OUT/'nonexistent.traj'); broken['traj_sha256']='0'*64
broken['dt_fs']=20; broken['log_every']=50
for s in broken['snapshots'].values(): s['frame']=0
R['pilot_bad_trajectory_and_frames']=m.pilot(broken,pr,'pilot')
save(OUT/'pilot/broken_snapshots.json',broken)

# Wrong extract cadence maps a real 10 ps trajectory to 20/50/100 labels.
shorttraj=OUT/'pilot/ten_ps.traj'
with Trajectory(shorttraj,'w') as tr:
    for i in range(11):
        a=toy('F_B'); a.info['actual_time_ps']=float(i); tr.write(a)
prov2=m.extract_snapshots(shorttraj,[20,50,100],20,500,OUT/'short_pilot','short')
R['wrong_cadence_extract']={str(t):dict(frame=prov2['snapshots'][str(t)]['frame'],
    actual_time_ps=read(OUT/'short_pilot'/prov2['snapshots'][str(t)]['file']).info['actual_time_ps']) for t in (20,50,100)}

# EOS must preserve the uncorrected ranking/decision, not just agree at corners.
for key,fam in {
  'eos_all_corners_flip_baseline':{'F_B':(-.15,0.,2436.33),'F_P':(0.,2.,2436.33),'F_free':(.5,0.,2436.33)},
  'eos_lower_ranks_change':{'F_B':(-5.,0.,2436.33),'F_P':(0.,2.,2436.33),'F_free':(.15,2.,2436.33)},
}.items():
    v=m.eos_robust(fam); order=sorted(fam,key=lambda f:fam[f][0])
    R[key]=dict(input=fam,baseline_order=order,baseline_gap=fam[order[1]][0]-fam[order[0]][0],
                **v)

# Current CLI tested against actual generated map. Full normal fixture must pass
# verification first; no production calculations are required to exercise readers.
gen=old/'actual_45x3'
if not R['manifest_actual_45x3']:
    actual_mm=m.manifest_map(gen)
    subset={n:v for n,v in actual_mm.items() if v[0] in sorted({x[0] for x in actual_mm.values()})[:6]}
    pp=records('cli_wrong_cohort',subset,time=20,temp=1000,wrong_inputs=True)
    sc=save(OUT/'cli_screen.json',dict(union_bases=sorted({v[0] for v in subset.values()})))
    proc=subprocess.run([sys.executable,'-B','-X','utf8',str(SRC/'tools/doping/b2o3_bo_readout.py'),
       'anneal','--gen',str(gen),'--results',str(pp),'--screen',str(sc),'--out',str(OUT/'cli_verdict.json')],
       text=True,capture_output=True,encoding='utf-8')
    R['actual_gen_cli_wrong_cohort']={'rc':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr}
    if (OUT/'cli_verdict.json').exists(): R['actual_gen_cli_wrong_cohort'].update(brief(json.loads((OUT/'cli_verdict.json').read_text(encoding='utf-8'))))

save(ROOT/'probe_results.json',R)
for k,v in R.items():
    if k.startswith('manifest_'): print(k, len(v),v[:1])
    elif k.startswith('eos_'): print(k,json.dumps({x:v[x] for x in ['baseline_order','baseline_gap','skip_eos']})+' corrected orders='+str(sorted(set(tuple(c['order']) for c in v['corners']))))
    elif k=='screen_partial': print(k, {x:v[x] for x in ['M','n_success_by_family','pilot_structure']},'missing',len(v['missing']))
    else: print(k,json.dumps(v,ensure_ascii=False))
```

## 부록 C — probe_results.json (사용자 붙여넣기 · 내용 그대로 · 공백만 접음)

```json
{
  "manifest_actual_45x3": [],
  "manifest_fault_crossbase_contents": [
    "cfg0000_E-2256.634_O-free_s: 좌표가 부모와 다르다 (최대 11.034 Å — 부모와 다른 자식)",
    "cfg0000_E-2256.634_O-free_s: 부모와 다른 원소 자리 [31, 53, 56, 92, 115] ≠ 기록한 O 자리 [53, 56, 115] (부모와 다른 자식)",
    "cfg0001_E-2255.860_O-free_s: 좌표가 부모와 다르다 (최대 11.034 Å — 부모와 다른 자식)",
    "cfg0001_E-2255.860_O-free_s: 부모와 다른 원소 자리 [31, 56, 92, 115, 118] ≠ 기록한 O 자리 [56, 115, 118] (부모와 다른 자식)"
  ],
  "manifest_fault_missing_li_report": [
    "li_candidates: 파일 없음 li_candidates.json"
  ],
  "manifest_fault_corrupt_li_report": [
    "li_candidates: sha256 불일치 (보고서가 바뀌었다)"
  ],
  "positive_anneal": {
    "winner": "F_B",
    "decision": "승자 F_B (차저 F_free 와 0.300 ≥ 0.2)",
    "n_pairs": 6,
    "hold_reasons": null,
    "M": {"F_B": 6, "F_P": 6, "F_free": 6},
    "G1": {"F_B": true, "F_P": true, "F_free": true}
  },
  "anneal_wrong_length": {
    "winner": "F_B",
    "decision": "승자 F_B (차저 F_free 와 0.300 ≥ 0.2)",
    "n_pairs": 6,
    "hold_reasons": null,
    "M": {"F_B": 6, "F_P": 6, "F_free": 6},
    "G1": {"F_B": true, "F_P": true, "F_free": true},
    "actual_time": 20,
    "actual_T": 500
  },
  "anneal_wrong_temperature": {
    "winner": "F_B",
    "decision": "승자 F_B (차저 F_free 와 0.300 ≥ 0.2)",
    "n_pairs": 6,
    "hold_reasons": null,
    "M": {"F_B": 6, "F_P": 6, "F_free": 6},
    "G1": {"F_B": true, "F_P": true, "F_free": true},
    "actual_time": 100,
    "actual_T": 1000
  },
  "other_input_same_names": {
    "winner": "F_B",
    "decision": "승자 F_B (차저 F_free 와 0.300 ≥ 0.2)",
    "n_pairs": 6,
    "hold_reasons": null,
    "M": {"F_B": 6, "F_P": 6, "F_free": 6},
    "G1": {"F_B": true, "F_P": true, "F_free": true}
  },
  "missing_identity": {
    "winner": "F_B",
    "decision": "승자 F_B (차저 F_free 와 0.300 ≥ 0.2)",
    "n_pairs": 6,
    "hold_reasons": null,
    "M": {"F_B": 6, "F_P": 6, "F_free": 6},
    "G1": {"F_B": true, "F_P": true, "F_free": true}
  },
  "full_union_failed": {
    "winner": null,
    "decision": "승자 보류",
    "n_pairs": 4,
    "hold_reasons": ["F_P: G1 실패 (성공 4 < 5 · 탈락)"],
    "M": {"F_B": 6, "F_P": 6, "F_free": 6},
    "G1": {"F_B": true, "F_P": false, "F_free": true}
  },
  "short_union_passed": {
    "winner": "F_B",
    "decision": "승자 F_B (차저 F_free 와 0.300 ≥ 0.2)",
    "n_pairs": 4,
    "hold_reasons": null,
    "M": {"F_B": 4, "F_P": 4, "F_free": 4},
    "G1": {"F_B": true, "F_P": true, "F_free": true}
  },
  "screen_partial": {
    "k_f": 6,
    "top_bases_by_family": {"F_B": [0], "F_P": [0], "F_free": [0]},
    "union_bases": [0],
    "M": 1,
    "n_success_by_family": {"F_B": 1, "F_P": 1, "F_free": 1},
    "missing": ["cfg0001_O-bo4", "cfg0001_O-distributed", "cfg0001_O-free_s", "cfg0002_O-bo4", "cfg0002_O-distributed", "cfg0002_O-free_s", "cfg0003_O-bo4", "cfg0003_O-distributed", "cfg0003_O-free_s", "cfg0004_O-bo4", "cfg0004_O-distributed", "cfg0004_O-free_s", "cfg0005_O-bo4", "cfg0005_O-distributed", "cfg0005_O-free_s"],
    "failed": [],
    "pilot_structure": "cfg0000_O-bo4",
    "⚠": ["성공 구조가 k_f 보다 적은 가족 ['F_B', 'F_P', 'F_free'] — 있는 것만 넣었다", "입력에 없는 구조가 있다 — 거름이 완전하지 않다"]
  },
  "pilot_positive": {
    "decision": "t_a = 100 ps",
    "t_a_ps": 100,
    "spread_eV": 0.3,
    "same_end_motif": true,
    "E": {"20": 0.0, "50": -0.3, "100": -0.02},
    "end_motif": {"20": "F_B", "50": "F_B", "100": "F_B"},
    "traj_sha256": "3e382c4304e9e9cc56163c3bedb135393d4f7eea7315533cce0e36c4d562e5be",
    "⚠": "운영 규칙 (길이 고르기) — 수렴 증거가 아니다 · 파일럿의 선택된 t_a 보다 긴 결과는 다른 배치와 견주지 않는다"
  },
  "pilot_bad_trajectory_and_frames": {
    "decision": "t_a = 100 ps",
    "t_a_ps": 100,
    "spread_eV": 0.3,
    "same_end_motif": true,
    "E": {"20": 0.0, "50": -0.3, "100": -0.02},
    "end_motif": {"20": "F_B", "50": "F_B", "100": "F_B"},
    "traj_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
    "⚠": "운영 규칙 (길이 고르기) — 수렴 증거가 아니다 · 파일럿의 선택된 t_a 보다 긴 결과는 다른 배치와 견주지 않는다"
  },
  "wrong_cadence_extract": {
    "20": {"frame": 2, "actual_time_ps": 2.0},
    "50": {"frame": 5, "actual_time_ps": 5.0},
    "100": {"frame": 10, "actual_time_ps": 10.0}
  },
  "eos_all_corners_flip_baseline": {
    "input": {"F_B": [-0.15, 0.0, 2436.33], "F_P": [0.0, 2.0, 2436.33], "F_free": [0.5, 0.0, 2436.33]},
    "baseline_order": ["F_B", "F_P", "F_free"],
    "baseline_gap": 0.15,
    "robust_independent_B": true,
    "robust_common_B": true,
    "pressure_ok": true,
    "skip_eos": true,
    "corners": [
      {"B": {"F_B": 21.7, "F_P": 21.7, "F_free": 21.7}, "order": ["F_P", "F_B", "F_free"], "gap": 1.251509290634193},
      {"B": {"F_B": 21.7, "F_P": 21.7, "F_free": 32.5}, "order": ["F_P", "F_B", "F_free"], "gap": 1.251509290634193},
      {"B": {"F_B": 21.7, "F_P": 32.5, "F_free": 21.7}, "order": ["F_P", "F_B", "F_free"], "gap": 0.7857769725157533},
      {"B": {"F_B": 21.7, "F_P": 32.5, "F_free": 32.5}, "order": ["F_P", "F_B", "F_free"], "gap": 0.7857769725157533},
      {"B": {"F_B": 32.5, "F_P": 21.7, "F_free": 21.7}, "order": ["F_P", "F_B", "F_free"], "gap": 1.251509290634193},
      {"B": {"F_B": 32.5, "F_P": 21.7, "F_free": 32.5}, "order": ["F_P", "F_B", "F_free"], "gap": 1.251509290634193},
      {"B": {"F_B": 32.5, "F_P": 32.5, "F_free": 21.7}, "order": ["F_P", "F_B", "F_free"], "gap": 0.7857769725157533},
      {"B": {"F_B": 32.5, "F_P": 32.5, "F_free": 32.5}, "order": ["F_P", "F_B", "F_free"], "gap": 0.7857769725157533}
    ]
  },
  "eos_lower_ranks_change": {
    "input": {"F_B": [-5.0, 0.0, 2436.33], "F_P": [0.0, 2.0, 2436.33], "F_free": [0.15, 2.0, 2436.33]},
    "baseline_order": ["F_B", "F_P", "F_free"],
    "baseline_gap": 5.0,
    "robust_independent_B": true,
    "robust_common_B": true,
    "pressure_ok": true,
    "skip_eos": true,
    "corners": [
      {"B": {"F_B": 21.7, "F_P": 21.7, "F_free": 21.7}, "order": ["F_B", "F_P", "F_free"], "gap": 3.598490709365807},
      {"B": {"F_B": 21.7, "F_P": 21.7, "F_free": 32.5}, "order": ["F_B", "F_P", "F_free"], "gap": 3.598490709365807},
      {"B": {"F_B": 21.7, "F_P": 32.5, "F_free": 21.7}, "order": ["F_B", "F_free", "F_P"], "gap": 3.7484907093658073},
      {"B": {"F_B": 21.7, "F_P": 32.5, "F_free": 32.5}, "order": ["F_B", "F_P", "F_free"], "gap": 4.064223027484247},
      {"B": {"F_B": 32.5, "F_P": 21.7, "F_free": 21.7}, "order": ["F_B", "F_P", "F_free"], "gap": 3.598490709365807},
      {"B": {"F_B": 32.5, "F_P": 21.7, "F_free": 32.5}, "order": ["F_B", "F_P", "F_free"], "gap": 3.598490709365807},
      {"B": {"F_B": 32.5, "F_P": 32.5, "F_free": 21.7}, "order": ["F_B", "F_free", "F_P"], "gap": 3.7484907093658073},
      {"B": {"F_B": 32.5, "F_P": 32.5, "F_free": 32.5}, "order": ["F_B", "F_P", "F_free"], "gap": 4.064223027484247}
    ]
  },
  "actual_gen_cli_wrong_cohort": {
    "rc": 0,
    "stdout": "-> C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DW_20261109\\probes\\cli_verdict.json\n승자 F_B (차저 F_free 와 0.300 ≥ 0.2) \n",
    "stderr": "",
    "winner": "F_B",
    "decision": "승자 F_B (차저 F_free 와 0.300 ≥ 0.2)",
    "n_pairs": 6,
    "hold_reasons": null,
    "M": {"F_B": 6, "F_P": 6, "F_free": 6},
    "G1": {"F_B": true, "F_P": true, "F_free": true}
  }
}
```
