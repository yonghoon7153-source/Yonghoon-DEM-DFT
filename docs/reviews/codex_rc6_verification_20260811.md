# Codex RC6 독립검증 회답 (2026-08-11) — 원문

> **보존 경위**: 사용자 붙여넣기로 받은 검증 회답.  `findings.json` 의 `verified_sha` 는
> **이 파일을 담은 커밋**을 가리켜야 하므로 (Codex 명시 요구) 여기 보존한다.
> 검증 대상: `claude/stoic-knuth-NObVQ @ 23211e25` · 검증자: codex

> 코드 대상: `claude/stoic-knuth-NObVQ @ 23211e2566e7a5561263223b28d99537a252d757`
> 기준: `8529e1140f65ab0f902893593bd56bc743eb924b`
> 요청서: `02ffcc66a3841d41c64846b118b23337458e7645:docs/codex_review_request_20260811_rc6.md`
> 검증자: `codex` (`Codex/dem-mpm-crosscheck`)
> 원칙: 구현자의 회귀 PASS와 finding 종료를 분리하고, `claimed_fixed` 9건을 각각 독립 판정했다.

## 0. 결론 — 9건 중 5건만 `verified` 전환 가능

| ID | 판정 | 원장 권고 | 핵심 근거 |
|---|---|---|---|
| **RC6-01** | **미검증** | `claimed_fixed` 유지 | 타입·finite 검사는 고쳐졌지만 `null_ok_keys`가 production 호출에 미배선이고, upstream electronic status도 없다. 실제 all-SE 경로가 `failed_no_active_generation`이 됐다. |
| **RC6-02** | **검증됨** | `verified` 가능 | H thermal 실패 시 새 세대 게시 전 차단, `OLDGEN`·옛 σ 복원, Stage E 0회. |
| **RC6-03** | **검증됨(원장 문구의 좁은 범위)** | `verified` 가능 | Physics thermal만 실패해도 H 성공에 가리지 않고 게시가 차단된다. 단, mode×channel 전체 계약은 별도 P1로 남는다. |
| **RC6-04** | **검증됨** | `verified` 가능 | 실제 H/P network→Stage E 실행에서 raw thermal 값이 전후 동일하고, 역산값은 estimate/provenance로만 생성됐다. |
| **RC6-05** | **미검증** | `claimed_fixed` 유지 | 1/4 partial-write 회귀와 4경로 배선은 통과했지만, 네 파일을 metadata-only touch하면 바이트가 전부 옛것인데 `ok=True`가 된다. |
| **RC6-06** | **미검증** | `claimed_fixed` 유지 | 실제 happy path manifest는 생성되지만 pore/PNM 실패·disabled·ionic-zero 경로가 누락된 채 top `complete`가 되는 false-green을 재현했다. |
| **RC6-07** | **검증됨** | `verified` 가능 | Windows 기본 코드페이지에서 실제 6입자 network solver가 rc=0, H/P/dual/legacy JSON 4개를 생성했다. |
| **RC6-08** | **검증됨(원 finding 범위)** | `verified` 가능 | CuPy 부재 시 실제 SciPy solve와 최종 payload 모두 `{requested: gpu, used: cpu, fallback_reason: ...}`를 기록했다. |
| **RC6-Q8** | **미검증** | `claimed_fixed` 유지 | `--open`이 Windows CP949에서 중간 종료되고, case만 바꾼 자기검증과 가짜 SHA/존재하지 않는 evidence가 검사기를 통과한다. |

전환 후보 5건: RC6-02 · RC6-03 · RC6-04 · RC6-07 · RC6-08.
`RC6-04b`·`RC6-Q7` 은 `open` 유지.

## 1. 종료를 막는 finding

### RC7-01 [P1] STEP3 manifest가 실패·미실행 component를 누락하고도 `complete`

happy path 는 실제 SciPy 실행에서 정상 (electronic/ionic/thermal/pore/pnm 전부 complete,
σ_e 1.648e-4 S/cm · σ_ion 1.823e-5 · k_eff 0.1154 W/mK · pore τ 1.004 · backend cpu).

그러나 component 하나만 적대 주입하면:

| 장애 | 실제 결과 |
|---|---|
| `pore_tau()` RuntimeError | manifest 는 e/i 만 complete, top 도 **complete** |
| `pore_pnm()` RuntimeError | PNM record 없음, top **complete** |
| ionic `n_dof=0` + `--no-trackb` | ionic record 없음, top **complete** |
| PNM 이 `{'reason': 'no pore graph'}` 반환 | PNM 을 **complete** 로 오표기 |
| pore 결과에 NaN | top complete, `json.dump` 가 bare NaN 기록 → strict JSON parse 실패 |
| `--no-step3` | step3·manifest 자체 없음 (disabled ↔ 구세대 부재 구분 불가) |
| `--no-thermal` | thermal `disabled` record 없음 |

원인: 실행 계획의 **expected-component 집합 없이 기록된 부분집합만** 검사한다.
회귀도 문자열 존재만 보는 정적 검사다.

종료 조건: ① 실행 전 expected component 전부 등록 ② disabled/skipped/not_solvable/failed 에
reason 강제 ③ 각 component 예외를 해당 component 에 기록 ④ top status 를 expected set 전수로
계산 ⑤ PNM reason 은 not_solvable 로 분류 ⑥ recursive finite 검사 + `json.dump(allow_nan=False)`
⑦ fault matrix 를 동적 회귀로 고정.

### RC6-01 [P1] valid-null 계약은 helper만 있고 production 배선이 없다

타입·유한성 검사는 NaN/inf/bool/잘못된 mapping/빈 method 를 제대로 거부했다.  그러나 앱은
`_ps.stage_e_missing_keys(json.load(_f))` 로 기본 인자만 쓴다 (`webapp/app.py:3042-3050`).

```json
{"default_missing": ["electronic_sigma_full_mScm_stage_e"],
 "with_null_ok_keys": [], "production_stage_e_ok": false,
 "verify_failed": true, "stage_e_status": "failed_no_active_generation"}
```

또 `network_conductivity.py:1101-1115,1151-1159` 가 electronic solve 예외를 삼킨 뒤 electronic
channel status 를 항상 쓰지 않는다 — 현재 생산자 출력만으로는 호출부가 올바른 `null_ok_keys` 를
만들 수도 없다.  `network_content_verdict()` 를 **mode×channel 정규화 함수**로 바꿔
publish gate 와 Stage E verifier 가 같은 판정에서 파생돼야 한다.

### RC7-02 [P1] network 게시 gate가 thermal만 검사한다

Physics thermal masking 은 닫혔다 (H/P 각각 failed 주입 시 둘 다 차단, active OLDGEN, σ 1.0,
Stage E 0회).  그러나 `pipeline_service.py:469-504` 는 각 mode 의 `thermal_status` 만 읽는다.
electronic solve 를 예외로 만들면 electronic value/status 가 없는 결과가 gate 를 통과했다:

```json
{"thermal_status": "computed", "electronic_status_present": false,
 "electronic_value_present": false, "gate": [true, "ok: hertzian, physics"]}
```

### RC7-03 [P1] contact `fresh=True`는 stale bytes의 metadata touch를 성공으로 판정

파일별 비교와 4경로 배선은 확인됐다.  그러나 runner 가 내용은 안 쓰고 mtime 만 갱신하면:

```json
{"ok": true, "stale_outputs": [], "all_bytes_unchanged": true}
```

`(mtime_ns, size)` 는 freshness 의 인과 증거가 아니다.  content hash 만 추가해도 결정론적
byte-identical 재계산과 미실행을 구분하지 못한다.  **빈 candidate directory** 에 생성한 뒤
계약을 통과한 세대만 게시하는 것이 답이다.

### RC7-04 [P2] finding 원장이 Windows·identity·evidence 경계에서 강제력을 잃는다

`--selftest` 는 15/15 PASS 지만 Windows 기본 CP949 에서 `--open` 이 세 번째 항목에서
`UnicodeEncodeError` 로 종료(exit 1)한다.  `PYTHONUTF8=1` 이면 11건 전부 출력.
즉 "항상 화면에 뽑는다" 는 RC6-Q8 핵심 계약이 기본 Windows 실행에서 성립하지 않는다.

검사기 자체도 다음 손상 원장을 통과시켰다:

```json
{"owner": "claude", "verified_by": "Claude", "claimed_fixed_sha": "not-a-sha",
 "verified_sha": "also-not-a-sha", "evidence_tests": ["missing.py::ghost"]}
```

case 변형으로 자기검증 금지 우회 · SHA reachability 미검사 · evidence selector 실재 미검사.
현재 원장의 `webapp/test_pipeline_provenance.py::RC6-02` 도 pytest selector 가 아니다
(그 파일은 자체 `main()` 형식이라 그 문자열로 선택 불가).

최소 보강: identity 를 canonical actor ID enum 으로 · branch protection/CODEOWNERS ·
SHA 는 `git cat-file -e <sha>^{commit}` 확인 · evidence 를 `{command, target_sha,
expected_exit, selector}` 구조로 · CI 가 allowlist 된 command 를 실제 실행 ·
`opened_in`/evidence path 존재 검사 · Windows 출력 인코딩 명시 + `--open` 을 selftest 에.

## 2. `verified` 가능 항목의 독립 실행 근거

### RC6-02 — 게시 전 thermal gate
H 또는 Physics thermal 을 각각 failed 로 주입했을 때 모두: network stage ok=False,
verify_failed=True, active provenance OLDGEN, legacy σ 1.0 복원, full_metrics σ 1.0 유지,
Stage E 호출 0회.  둘 다 computed 인 대조군만 새 run ID·σ 999·Stage E 1회로 게시.

### RC6-03 — Physics thermal masking 의 좁은 계약
Physics JSON 만 `thermal_status=failed` 여도 H 성공에 가리지 않고 동일하게 차단됐다.
**원장 title 범위**는 검증.  ionic/electronic completeness 는 RC7-02 로 분리.

### RC6-04 — raw thermal 이중 소유 종료
실제 6-SE/7-contact 합성망 → `--contact-mode both` → Stage E `run_one()`:

```
raw before = (1.700792, 1.319051)
raw after  = (1.700792, 1.319051)
Stage E    = (1.700792, 1.319051)
run_one ok = True
```

raw 를 0.0/0.0 으로 둔 재실행에서도 raw 는 그대로였고 별도 estimate·provenance 만 생성:

```json
{"raw": [0.0, 0.0], "estimate": [1.700792, 1.319051], "loss_present": false,
 "provenance": {"source": "stage_e_inverse_weighted_factor",
                "weighted_factor_kappa": 1.0, "raw_present": false}}
```

RC6-04b 는 별개 — live pre-purge 직후 parent death 를 주입하면 active file 에서 managed
Stage E 키가 전부 사라지는 것을 재현했다.  `RC6-04 verified` 와 `RC6-04b open` 은 동시 성립.

### RC6-07 — Windows 실제 solver
Windows 기본 코드페이지 parent 에서 `run_stage()` 를 통해 실제 합성 network solver 실행:
`ok=true, rc=0, missing=[], verify_failed=false`, 네 JSON 전부 생성, stderr 비어 있음.
단순 문자 재현이 아니라 **실제 solver 의 첫 non-ASCII 로그와 네 JSON 생성까지** 확인.

### RC6-08 — CuPy 부재 시 실제 backend provenance
```json
{"cpu": {"requested":"cpu","used":"cpu","fallback_reason":null},
 "gpu_missing": {"requested":"gpu","used":"cpu",
                 "fallback_reason":"ModuleNotFoundError: No module named 'cupy'"},
 "fake_gpu_success": {"requested":"gpu","used":"gpu","fallback_reason":null},
 "fake_gpu_failure": {"requested":"gpu","used":"cpu",
                      "fallback_reason":"RuntimeError: synthetic GPU runtime failure"}}
```
다음 CPU 호출에서 이전 fallback reason 도 초기화됐다.  실제 CUDA 하드웨어 성능 검증은 아님.

## 3. 검증된 항목에서 분리할 후속 P2

### RC7-05 [P2] STEP3 backend는 마지막 전역 solve 하나만 나타낸다
`LAST_BACKEND` 는 모듈 전역이라 `_solve_cg()` 가 호출된 **마지막 component** 만 표현한다.
`solve_sigma_z()` 가 `no_conductive_voxels` 등으로 `_solve_cg()` 전에 반환하면 GPU 요청을
초기화하지 않는다:

```json
{"fresh_gpu_no_solve": {"requested": null, "used": null, "fallback_reason": null},
 "gpu_no_solve_after_cpu": {"requested": "cpu", "used": "cpu", "fallback_reason": null}}
```
backend 를 solve 반환값에 component 별로 넣고 manifest 가 집계해야 한다.
미실행은 `used=null`, `fallback_reason=not_invoked` 로.

### RC7-06 [P2] Stage E estimate provenance가 관리 키가 아니다
`thermal_baseline_estimate_provenance` 를 `is_stage_e_key()` 가 잡지 않는다.
webapp pre-purge 재실행 시 estimate 값은 제거되지만 옛 provenance 만 남고, CLI 직접 재실행 시
둘 다 stale 로 남는다.  raw 가 다시 유효해진 뒤에도 `raw_present=false` 인 옛 provenance 가
남는 것을 확인했다.

## 4. §5 질문 답변

- **Q1**: RC6-04 검증됨 · RC6-06 **반증됨**(false-complete 재현) · RC6-08 검증됨.
- **Q2**: 정당한 non-percolating/all-SE 케이스는 여전히 partial/failed.  helper 만으로는
  안 닫힌다.  결선은 `network_content_verdict()` 가 쓰는 **동일 mode×channel matrix** 에서
  만들어야 하며, 먼저 **electronic status producer** 가 필요하다.
- **Q3**: 넓은 의미로는 **절반만** 닫혔다.  좁은 finding 은 verified, RC7-02 를 P1 추가.
- **Q4**: `(mtime_ns, size)` 도 content hash 도 부족.  빈 candidate directory 에서 생성 여부·
  schema·finite·lineage 를 검증한 뒤 게시하는 것이 답.  그 전까지 RC6-05 는 닫지 않는다.
- **Q5**: 세 러너의 기본 MACH=0.03 이 모두 `--allow-fast-platen` 을 자동으로 붙여 production
  에서는 기본 우회된다.  `quasistatic_violation=true` 를 검사하는 소비자 코드가 없어 충분한
  안전망이 아니다.  권고: 절대값 기본을 `--platen-mach 0.01` 로 · 빠른 상대비교는 사용자가
  `--relative-only` 를 명시해야 허용 · campaign manifest 에 동일 Mach/protocol 기록 ·
  grade/rank/export 가 violation=true 를 절대값 근거로 쓰는 것을 거부.
- **Q6**: 자기일관성만으로 부족.  CI 에서 canonical reviewer identity · reachable SHA ·
  실재 test target · 실제 command exit/artifact 를 묶어야 한다.  Windows `--open` 도 CI matrix 에.
- **Q7**: **Q7 scanner 를 아주 짧은 read-only 선행 커밋으로 먼저** 두는 판단에 동의.  다만 그
  뒤에 다른 기능을 끼우지 말고 RC6-04b 를 즉시 진행할 것.  권장 순서:
  ① read-only corpus scanner ② 결과를 migration fixture·shadow 기준으로 고정
  ③ Stage E exact `--case-dir` + candidate/manifest ④ active flat 을 먼저 purge 하지 않고
  candidate 완결 ⑤ fsync + atomic composite pointer publish 로 RC6-04b 종료.
  **scanner 가 빠르다는 이유로 P1 crash window 를 장기 보류해서는 안 된다.**

## 5. 실행 기록

| 검증 | 결과 |
|---|---:|
| `webapp/test_pipeline_provenance.py` | **103/103 PASS** |
| `webapp/test_security_phase_a.py` | **28/28 PASS** |
| `scripts/mpm3d_compaction.py --selftest` | **97/97 PASS** |
| `scripts/network_mode_io.py --selftest` | **11/11 PASS** |
| `scripts/check_review_findings.py --selftest` | **15/15 PASS** |
| `scripts/check_review_findings.py --open` (CP949) | **FAIL — UnicodeEncodeError** |
| 같은 `--open` (`PYTHONUTF8=1`) | **PASS — 11건 출력** |
| Python 전수 `compile()` + SyntaxWarning error | **412/412 PASS** |
| 실제 network solver, Windows parent | **rc=0, 4 JSON** |
| 실제 STEP3 tiny payload | **happy path complete + strict JSON** |
| STEP3 component fault matrix | **false-complete 다수 재현** |

## 6. 원장에 반영할 권고안

```yaml
verification_target: 23211e2566e7a5561263223b28d99537a252d757
verified_by: codex
eligible_for_verified: [RC6-02, RC6-03, RC6-04, RC6-07, RC6-08]
remain_claimed_fixed: [RC6-01, RC6-05, RC6-06, RC6-Q8]
remain_open: [RC6-04b, RC6-Q7]
add: [RC7-01, RC7-02, RC7-03, RC7-04, RC7-05, RC7-06]
```

`verified_sha` 는 **이 회답 문서를 담은 실제 커밋 SHA** 로 채워야 하며 PENDING·임의 문자열·
검증 대상 코드 SHA 를 중복 기입해서는 안 된다.
