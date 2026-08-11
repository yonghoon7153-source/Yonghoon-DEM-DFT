# RC5 전건 · thermal · STEP3 적대 교차검증 (2026-08-11) — Codex 6회차 원문

> **보존 경위**: 이 리뷰는 사용자 붙여넣기로 받아 리포에 파일이 없었다.
> `docs/reviews/findings.json` 의 `opened_in` 이 이 파일을 가리키므로 원문을 보존한다.
> (원장이 존재하지 않는 문서를 가리키면 추적이 끊긴다.)
> 회답: `docs/codex_review_request_20260811_rc6.md`

> 검증 대상: `claude/stoic-knuth-NObVQ @ 8529e114`
>
> 기준: `466926c5` (`8 commits`, `15 files`, `+843/-40` 확인)
>
> 검증 방식: 대상 commit 격리본 정적 감사 + Windows/WSL 독립 실행 + 가짜 runner 적대 주입
>
> 판정 원칙: 구현자의 회귀 PASS와 결함 종료를 같은 뜻으로 보지 않는다.

## 0. 결론

이번 수정은 **유효한 진전**이지만, RC5 전건이 닫혔다고 판정할 수는 없다.

- **F-18의 좁은 원인**인 bare `python3`는 `sys.executable`로 정확히 바뀌었다.
- **RC5-02의 child-process 실패 복원 순서**는 현재 열거된 키에 대해 맞다.
- **RC5-04의 핵심 H/P 값 유실**은 실제 solver 산출물에서도 해소됐다.
- **RR3-04의 batch 배선**은 실제로 `fresh=True`를 전달한다.
- 선언된 `71/71`, `28/28`, `11/11`, tracked Python `409/409` warning-as-error compile은 독립 재현됐다.

그러나 아래 **P1 7건 + P2 1건**이 남거나 새로 확인됐다.

| ID | 심각도 | 판정 | 핵심 |
|---|---:|---|---|
| **RC6-01** | P1 | 신규 | "11-key exact schema"가 NaN·잘못된 타입을 success로 허용하며 `valid_null` 계약과 충돌 |
| **RC6-02** | P1 | 신규 | thermal 실패를 판정하기 전에 새 network 세대를 active `success`로 게시 |
| **RC6-03** | P1 | 신규 | Physics mode 상태·완전성을 검사하지 않아 Physics 실패가 H 성공에 가려짐; legacy fallback도 과학적 성공처럼 게시 가능 |
| **RC6-04** | P1 | 잔존 | Stage E가 성공 시 network-owned raw thermal을 덮어써 이중 소유·세대 혼합 유지; live pre-purge도 crash-atomic 아님 |
| **RC6-05** | P1 | 자인 확인 | `fresh=True`가 4산출물 중 1개만 바뀌어도 통과; main/archive contact는 배선조차 없음 |
| **RC6-06** | P1 | 신규 | STEP3 thermal만 좁게 고쳤고 electronic/ionic/pore/PNM/STEP4 및 전체 STEP3 실패는 여전히 JSON에서 소실 |
| **RC6-07** | P1 | 신규 | Windows CP949에서 실제 network solver가 첫 `—` 로그에서 종료; F-18 뒤에도 Windows subprocess 경로가 안전하지 않음 |
| **RC6-08** | P2 | 신규 | `--step3-gpu`가 CPU로 fallback돼도 산출물에 실제 backend·fallback reason이 없음 |

## 1. Q1 — RC5-01의 11-key 계약

### 판정: **키 집합은 맞지만 "exact schema"는 아니다**

`run_one()`의 정상 write 경로는 다음 11개를 모두 대입한다.

- 여섯 H/P Stage E conductivity 값: `scripts/run_network_full_corrections.py:817-824`
- `stage_e_source`: `806-814`
- `stage_e_factors_used`, fracture counts, method: `825-832`
- `validation_flags`: `873-874`

`full_metrics.json` read 실패는 이 대입보다 앞에서 return하며, 그 밖의 예외는 정상 종료가 아니므로 "정상 종료의 최소 키 집합"이라는 설명 자체는 맞다.

하지만 `stage_e_missing_keys()`는 `dict.get(k) is None`만 본다
(`webapp/pipeline_service.py:127-137`). 따라서 아래 손상 레코드도 완전하다고 판정한다.

```python
bad = {k: 1.0 for k in STAGE_E_REQUIRED_KEYS}
bad['sigma_full_mScm_stage_e'] = float('nan')
bad['stage_e_source'] = 'not-a-map'
bad['validation_flags'] = []

stage_e_missing_keys(bad) == ()  # 실제 관측
```

즉 현재 회귀는 다음을 검증하지 않는다.

- 여섯 숫자의 `isinstance(number)`와 `math.isfinite`
- `stage_e_source`의 6채널 enum 구조
- factors/counts/validation flags의 객체 타입·필수 하위 키·boolean 타입
- `fracture_aware_method_full`의 non-empty string
- source와 값의 관계(예: `source=solver`인데 값이 0/None인지)

더 큰 문제는 **network와 Stage E의 sentinel 계약이 서로 모순**이라는 점이다.

- network는 `valid_null`을 물리적으로 정상인 non-percolation으로 허용한다
  (`network_conductivity.py:1160-1174`, `pipeline_service.py:404-424`).
- Stage E는 대응 값이 `None`이면 11-key 결손으로 판정한다.
- `run_one()`은 baseline·재솔브·fallback이 모두 유효 양수를 못 주면 `None`을 그대로 쓸 수 있다
  (`run_network_full_corrections.py:752-804,817-824`).

실제 SE-only 합성망을 target solver로 돌렸을 때 electronic 채널은 H/P 모두 생성되지 않았고,
`collect_modes()`는 이를 결손으로 보고했다. 이런 정당한 "not applicable/non-percolating" 케이스를
숫자 6개 무조건 non-None으로 정의하면 완전한 실행도 `partial`이 된다.

**권고**: 앱의 키 목록이 아니라 공유 versioned schema를 둔다. 최소 단위는 각 mode×channel의

```json
{"status":"computed|valid_zero|valid_null|not_computed|failed","value":null,"reason":"..."}
```

이며 `computed`만 finite number, `valid_zero`는 정확히 0, `valid_null/not_computed`는 null+reason을 요구해야 한다.

## 2. Q2 — purge/rollback/attempt 분리

### 판정: **child 실패 복원 순서는 맞지만 ownership·crash atomicity는 닫히지 않았다**

현재 실패 처리 순서

1. 현재 managed key 전수 제거
2. 이전 managed key overlay
3. raw thermal의 `{present,value}` 정확 복원
4. 이전 active 유무에 따른 상태
5. `stage_e_attempt.json` 별도 기록

는 `webapp/app.py:3063-3085`에서 구현돼 있다. 현재 `run_one()`이 쓰는 관리 키는
`is_stage_e_key()` 또는 `RAW_THERMAL_KEYS`에 잡힌다. **child가 실패하고 parent app이 살아 있는 경우**에는 올바른 순서다.

하지만 다음은 남는다.

### RC6-04a — 성공 경로의 raw thermal 이중 소유

Stage E는 여전히 `thermal_sigma_full_mScm[_physics]`를 "heal"하며 덮어쓴다
(`run_network_full_corrections.py:834-852`). 성공 시에는 rollback하지 않는다.

동적 주입 결과:

```json
{
  "stage_e_status": "success",
  "network_json_thermal": 2.0,
  "published_full_metrics_thermal": 777.0,
  "published_full_metrics_thermal_physics": 888.0
}
```

즉 같은 `network_run_id` 아래 network component JSON은 `2.0`인데 게시된
`full_metrics`의 network-owned raw 값은 Stage E가 만든 `777.0`이다. "thermal 근본수정"이라기보다
실패 rollback만 보강한 상태다.

raw H/P는 network 단독 소유·Stage E read-only로 두고, heal 값은
`thermal_sigma_*_stage_e_estimate`와 `{old,new,source,parent_digest}`로 분리해야 한다.

### RC6-04b — live pre-purge window

앱은 subprocess 전에 현재 `full_metrics.json`에서 Stage E 키를 제거한 파일을 active 위치에
실제로 게시한다(`app.py:3037-3046`). 따라서:

- 정상 실행 중에도 reader가 Stage E 키가 없는 중간 상태를 볼 수 있다.
- app process가 purge 뒤 복원 전에 죽으면 그 상태가 영구 active가 된다.
- child 실패 rollback은 이 parent crash를 복구하지 못한다.

이는 기존 RR3-03과 같은 뿌리다. candidate/manifest/pointer 전환 전에는 닫히지 않는다.

### attempt 소비처

`stage_e_attempt.json`을 읽는 production consumer는 target tree에서 **0개**다. writer와 회귀만 있다.
따라서 기존 소비처가 깨지지는 않지만, 실패 시도는 UI/status/archive QC에서 보이지 않는 write-only evidence다.
`analyze-status` 또는 case QC payload에 `last_stage_e_attempt`를 명시적으로 노출해야 한다.

## 3. Q3 — Physics 평평 병합

### 판정: **완전한 H/P 출력에서는 정확하다. 결손·legacy에서는 fail-open이다**

SE 6개·접촉 7개의 최소망을 실제 `network_conductivity.py --contact-mode both`로 실행했다.
UTF-8 mode에서 solver는 네 JSON을 생성했고, 실제 값은 다음과 같았다.

| 채널 | Hertzian | Physics |
|---|---:|---:|
| `sigma_full_mScm` | 0.001856 | 0.002231 |
| `thermal_sigma_full_mScm` | 0.004330 | 0.005205 |

`collect_modes()` 결과도 위 값이 각각 `<key>`와 `<key>_physics`에 정확히 들어갔다.
H/P key namespace가 분리되므로 현재 solver key에 대한 접미사 충돌은 없었다. **RC5-04의 원래 값 유실은 닫혔다.**

다만 실제 SE-only 산출물에는 electronic key가 H/P 모두 없었고:

```text
_modes_present = [hertzian, physics]
_modes_missing_channels = [
  hertzian.electronic_sigma_full_mScm,
  physics.electronic_sigma_full_mScm
]
```

이 결손은 stderr warning과 metadata에만 남고 호출부는 검사하지 않는다
(`network_mode_io.py:65-94`, `run_network_full_corrections.py:469-504`).

### RC6-03 — Physics status가 H 성공에 가려진다

웹앱은 `network_conductivity.json`, 즉 legacy Hertzian 복사본만 `thermal_channel_verdict()`에 넣는다
(`app.py:2941-2979`). Physics JSON의 `thermal_status`는 검증하지 않는다.

적대 fixture에서 H=`computed`, P=`failed`로 네 파일을 만들자:

```json
{
  "network_stage_ok": true,
  "thermal_verdict": "ok",
  "network_solver_status": "success",
  "stage_e_status": "success",
  "physics_input_status": "failed"
}
```

Physics thermal 값은 null인데도 전체가 success가 됐다. H/P 양쪽의 mode×channel status를 각각
검증하기 전에는 "both" 계약이 아니다.

### legacy fallback

per-mode 파일이 전무하면 legacy H 파일을 읽어 `_modes_present=['legacy']`로 돌려준다.
그 뒤 Physics 값은 `None`이지만, 기존 `full_metrics`에 Physics baseline이 있으면 `run_one()`의
weighted fallback이 그 옛 값을 새 Stage E 값으로 만들 수 있다(`run_network_full_corrections.py:729-804`).
11키가 모두 채워지면 active success가 된다.

legacy는 "H만 존재, Physics not computed"로 명시해야 하며 새 Physics 과학값처럼 승격하면 안 된다.

## 4. Q4 — thermal 상태 분류

### 판정: `valid_zero/valid_null`은 맞지만 `no_result/unknown` 정책과 publish 순서가 위험하다

- `computed`, `valid_zero`, `valid_null`: 상태/값 관계를 검증한다는 조건에서 정상 취급 가능하다.
- `failed`: required failure가 맞다.
- **새 실행의 `no_result`, `not_run`, 알 수 없는 enum, status 결손**: legacy가 아니라 새 schema 위반이므로 실패해야 한다.

현재 `no_result`와 미등록 상태는 `unknown`이고, 앱은 `fail`만 아니면 stage `ok=True`로 둔다
(`pipeline_service.py:408-424`, `app.py:2987-2997`). 즉 §6-4의 자인대로 무음 통과한다.

### RC6-02 — 판정보다 active 게시가 먼저다

더 심각하게, 네 파일의 존재만 만족하면 앱은 stash를 버리고 active provenance를 `success`로 찍은 뒤
thermal content를 판정한다(`app.py:2884-2912` 대 `2975-2997`).

Hertzian `thermal_status='failed'` fixture의 실제 관측:

```json
{
  "required_stage_failed": ["Thermal channel verdict"],
  "active_provenance_solver_status": "success",
  "full_metrics_network_solver_status": "thermal_failed",
  "stage_e_called": false
}
```

즉 required stage는 실패했는데 active provenance는 성공이며 이전 완전 세대 stash는 이미 버렸다.
content/status/schema 검증을 모두 통과한 candidate만 active로 publish해야 한다.

legacy 허용은 `preserve_network=True`이면서 provenance가 명시적으로 legacy인 경우에만 제한하고,
force/retry/batch/archive가 방금 생성한 파일의 `unknown`은 fail-closed로 처리해야 한다.

## 5. Q5 — RR3-04 `fresh=True`

### 판정: fresh-dir 판단은 맞지만, 현재 구현은 partial write를 못 막고 배선 범위도 부족하다

`before`가 비어 있고 기대 산출물이 새로 생기면 거짓 stale로 판정하지 않는다. 이 부분은 맞다.

그러나 `_stat_sig()` 전체 dict가 전과 같은 경우에만 stale로 처리하므로
(`pipeline_service.py:544-599`), 네 파일 중 하나만 바뀌어도 통과한다.

동적 재현:

```json
{
  "ok": true,
  "stale_outputs": [],
  "unchanged_old": [
    "atoms_analyzed.csv",
    "contacts_analyzed.csv",
    "network_summary.csv"
  ]
}
```

호출 경로도 다음과 같다.

| contact 경로 | stale risk | `fresh=True` |
|---|---|---|
| batch | 기존 results 위 재실행 | 있음 |
| main `run_pipeline` standard/bimodal | 기존 results를 지우지 않고 재실행 가능 | **없음** (`app.py:3236-3238,3305-3307`) |
| archive reanalyze | 기존 archive target 위 재실행 | **없음** (`app.py:9512-9518`) |
| retry | contact를 다시 돌리지 않는 network-only 경로 | 해당 없음 |

batch 배선만으로 RR3-04 계열을 일반적으로 닫지는 못한다. 최소 중간형은 **각 expected 파일이 개별적으로
새로 생성/갱신됐는지** 확인하는 것이며, 최종형은 빈 candidate + manifest + atomic publish다.

## 6. Q6 — STEP3 대칭성

### 판정: thermal 예외 stub은 유효하지만 전체 상태 계약의 일부만 고쳤다

CPU 수치 selftest는 모두 통과했다.

- laminate/series/parallel/gap/column
- temperature
- reaction
- pore diffusion
- PNM
- SWCNT
- Track-B

따라서 아래 finding은 행렬 조립 자체가 아니라 **orchestration·결손 표현·provenance** 문제다.

### RC6-06 — STEP3의 같은 모양 결함

1. **전체 STEP3**
   - outer `except Exception`은 print만 하고 status/reason을 payload에 쓰지 않는다
     (`mpm_webapp_payload.py:1374-1377`).
   - 예외 시점에 따라 `step3`이 아예 빠지거나 성공 부분만 남는다.
   - `--no-step3`, 구세대 부재, solver 실패를 machine-readable하게 구분할 top-level status가 없다.

2. **electronic**
   - not-solvable은 generic `reason`만 쓰고 status가 없다(`752-757`).
   - 성공에도 status가 없다.
   - raster/solve/후처리 예외는 outer print로만 빠진다.

3. **ionic**
   - 성공·non-percolating·예외 모두 채널 status가 없다(`1034-1083`).
   - `n_dof=0` 사유는 Track-B stub에 우연히 남을 뿐이며 `--no-trackb`면 그 증거도 없다.

4. **thermal**
   - `not_solvable`과 `failed` 분리는 이번 수정으로 좋아졌다(`1204-1260`).
   - 그러나 정상 `computed`에는 status가 없어, "status 없는 구세대/부분 결과"와 스키마가 비대칭이다.

5. **pore/PNM/reaction/carbon-SE**
   - pore 예외, PNM 예외, reaction의 reason/예외, carbon-SE 예외는 대부분 print-only다
     (`1261-1270,1276-1310,1315-1345`).
   - key 부재가 disabled/not_applicable/not_solvable/failed 중 무엇인지 알 수 없다.

권고는 STEP3 전체 manifest와 component별 상태다. 예:

```json
{
  "schema_version": 1,
  "status": "complete|partial|failed|disabled",
  "components": {
    "electronic": {"status": "...", "reason": "..."},
    "ionic": {"status": "...", "reason": "..."},
    "thermal": {"status": "...", "reason": "..."},
    "pore": {"status": "...", "reason": "..."},
    "pnm": {"status": "...", "reason": "..."},
    "reaction": {"status": "...", "reason": "..."}
  }
}
```

component가 enabled인데 status가 없으면 payload publish를 실패시켜야 한다.

### RC6-08 — GPU 요청과 실제 backend가 다를 수 있다

CuPy가 없는 환경에서 `GPU_SOLVE=True`로 실제 solve를 돌리자 로그는 GPU 시작을 출력한 뒤 CPU로 fallback했고
결과는 정상 수치였다. 그러나 반환 dict에는 `backend`, `gpu_used`, `fallback_reason`이 모두 없었다.

```json
{
  "backend": null,
  "gpu_used": null,
  "gpu_fallback_reason": null
}
```

`step3_sigma.py:80-110,309-315`의 fallback은 기능상 안전하지만 provenance상 구분 불가다.
각 component에 `backend_requested`, `backend_used`, library/CUDA version, fallback reason, CG info/residual을 남겨야 한다.

실 GPU/CuPy 실행은 이 환경에서도 하지 못했다. 따라서 GPU 수치 parity 주장은 여전히 미검증이다.

## 7. F-18 및 Windows 재검증

### F-18 판정: **좁은 수정은 맞다**

`mpm_input_package()`의 argv[0]은 `sys.executable`이다(`webapp/app.py:6729-6733`).
AST 회귀도 이를 고정한다. bare `python3` 때문에 즉시 500이 되던 원인은 코드 수준에서 닫혔다.

### RC6-07 — 별도의 CP949 차단점

그러나 실제 target `network_conductivity.py`를 Windows 기본 환경에서 실행하자:

```text
UnicodeEncodeError: 'cp949' codec can't encode character '—'
  network_conductivity.py:1092
```

return code는 1, 네 network JSON은 0개였다. `PYTHONUTF8=1`을 명시한 같은 입력은 rc=0으로 네 파일을 모두 만들었다.

원인은 solver가 `—`, `⚠` 등의 문자를 출력하고, 앱의 subprocess 경로가 `text=True`만 지정한 채
child 출력 encoding을 계약하지 않기 때문이다. 다음 두 경로에 모두 영향이 있다.

- 웹앱 main network solver (`pipeline_service.run_stage`)
- Stage E 내부 재솔브 (`run_network_full_corrections._run_solver:497-503`)

후자는 return code 1을 `None`으로 바꿔 weighted fallback으로 흐를 수도 있어 Q3의 실제 Windows 검증을 오염시킨다.

권고: 공통 subprocess wrapper에서 child에 UTF-8 mode를 주고 parent decode도 명시한다.

```python
env = {**os.environ, 'PYTHONUTF8': '1', 'PYTHONIOENCODING': 'utf-8'}
subprocess.run(..., text=True, encoding='utf-8', errors='replace', env=env)
```

또는 모든 production log를 ASCII로 제한한다. child만 UTF-8로 바꾸고 parent decode를 CP949로 두면 안 된다.

## 8. Q7 — corpus 영향 측정

### 판정: target repository만으로는 비율을 계산할 수 없다

`8529e114`의 tracked tree에는 `full_metrics.json` 또는 per-mode network result JSON이 **0개**다.
따라서 이번 검증에서 "게시본 N개 중 M개가 projection clear로 값을 잃는다"는 수치를 만들 근거가 없다.
현재 코드에도 mutation 전 read-only preflight scanner가 없다.

재분석 없이도 **위험도 분류**는 가능하다. 다음 scanner를 먼저 돌리면 된다.

1. results/archive/DB의 각 case에서 `full_metrics`, H/P/legacy JSON, provenance를 read-only로 읽는다.
2. 현재 `_NET_MERGE_KEYS` projection clear+merge를 메모리에서만 시뮬레이션한다.
3. 각 mode×channel을 다음으로 분류한다.
   - retained/computed
   - validly cleared (`valid_zero|valid_null|not_computed` + reason)
   - failed
   - legacy unknown
   - status/value contradiction
4. old value가 사라지는 case ID·field·old/new status·input hash를 CSV/JSON으로 낸다.
5. H/P 중 하나라도 `failed/unknown/contradiction`이면 실제 reanalysis와 publish를 차단한다.

`network_projection_dropped`는 mutation **후**에만 생기고 production consumer도 없으므로 사전 영향 측정의 대체물이 아니다.

## 9. Q8 — 리뷰 누락 방지 장치

Markdown 문장만으로 상태를 추적하면 다시 누락된다. 리포 안에 machine-readable 단일 원장을 둔다.

권장 파일:

```text
docs/reviews/findings.json
scripts/check_review_findings.py
```

finding 최소 필드:

```json
{
  "id": "RC6-01",
  "severity": "P1",
  "status": "open|claimed_fixed|verified|wontfix",
  "owner": "claude|codex|user",
  "opened_in": "docs/reviews/...md",
  "introduced_sha": "...",
  "claimed_fixed_sha": null,
  "verified_sha": null,
  "evidence_tests": [],
  "supersedes": [],
  "decision_note": null
}
```

CI/로컬 검사는 다음을 강제한다.

- ID 중복·누락 금지
- `claimed_fixed`에는 fix SHA와 회귀 ID 필수
- `verified`는 구현자와 다른 검증자의 evidence가 있어야 함
- 새 리뷰 요청 문서는 모든 `open|claimed_fixed` ID를 자동 열거
- 회귀 주석은 `finding: RC6-01`처럼 원장 ID를 참조
- prose에 "수정 완료"라고 써도 원장 상태는 자동 변경하지 않음

이렇게 해야 "응답 문서는 있었지만 다음 작업 목록에서 사라짐"을 CI가 잡는다.

## 10. §6 자인 약점 전수 판정

| 자인 약점 | 독립 판정 |
|---|---|
| 1. fresh partial write | **확인**. 4개 중 1개만 변경해도 `ok=True` 동적 재현 |
| 2. flat `_collect_modes` | 완전 H/P에서는 값 정확. 결손/legacy completeness를 caller가 무시해 **잔여 P1** |
| 3. thermal-only status | **확인**. network 1/6뿐이며 STEP3 e/i 등도 무상태 |
| 4. unknown 통과 | **확인**. 새 `no_result`도 required success; legacy와 새 schema 위반을 구분하지 않음 |
| 5. corpus 영향 미측정 | **확인**. tracked corpus 0, preflight scanner 없음 |
| 6. STEP3 GPU 미실행 | **확인**. CPU selftest는 통과했으나 GPU 실기는 미검증; fallback backend도 미기록 |

## 11. 독립 실행 기록

| 검증 | 결과 |
|---|---:|
| `webapp/test_pipeline_provenance.py` | **71/71 PASS** |
| `webapp/test_security_phase_a.py` | **28/28 PASS** |
| `scripts/network_mode_io.py --selftest` | **11/11 PASS** |
| `scripts/press_units.py` | **14/14 PASS** |
| `scripts/summarize_jam_sweep.py --selftest` | **10/10 PASS** |
| `scripts/heckel_analysis.py --selftest` | **20/20 PASS** |
| `scripts/unpack_kit_scaffolds.py --selftest` | Windows **12/13**, WSL **13/13** — executable-bit 검사는 POSIX에서만 성립 |
| tracked Python warning-as-error `compile()` | **409/409 PASS** |
| STEP3 CPU selftests 7종 | **전부 PASS** |
| payload temperature selftest | **PASS** |
| 실제 network solver, 기본 Windows CP949 | **FAIL** (`UnicodeEncodeError`, rc=1) |
| 같은 solver, UTF-8 mode | **PASS**, H/P/dual/legacy 4파일 생성 |
| 실제 GPU/CuPy | **미검증** |

## 12. 권장 수정 순서

1. **publish 순서 수정**: H/P mode×channel content/status/schema 검증 전에는 stash drop·active stamp 금지.
2. **Windows subprocess encoding 계약**: 공통 wrapper로 child와 parent decode를 UTF-8로 통일.
3. **공유 versioned schema**: finite/type/status/value/reason 검증; 11-key existence check 대체.
4. **Stage E raw thermal 쓰기 제거**: network raw immutable, heal은 Stage E estimate로 분리.
5. **contact candidate 실행**: main/batch/archive 동일 helper, 개별 산출물 manifest 검증.
6. **STEP3 top-level/component manifest**: disabled/not_solvable/failed/complete 구분 + 실제 backend provenance.
7. **read-only corpus preflight** 후에만 projection-clear migration.
8. **finding registry + CI**로 이번 P1들을 `claimed_fixed → independently verified` 순서로 닫기.

현재 상태에서 재분석·batch를 대규모 corpus에 실행하거나 "thermal 근본수정 완료"로 표시하는 것은 보류하는 편이 안전하다.
