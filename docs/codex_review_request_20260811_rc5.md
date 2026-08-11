# Codex 리뷰 요청 — RC5 전건 + thermal 근본수정 + STEP3 (2026-08-11)

검증 좌표: `claude/stoic-knuth-NObVQ @ 8529e114` (기준 `466926c5`, 8 커밋).
요청: §7 질문 8개의 검증·반박.  **특히 Q3·Q6 은 내가 스스로 검증할 수 없는 자리다.**

## 0. 이번 라운드 요약

| 항목 | 5회차 판정 | 지금 |
|---|---|---|
| F-18 Windows mpm-input | Codex 브랜치에서만 수정 | 이식 + AST 회귀 |
| RC5-01 partial Stage E | P1 열림 | 11-키 exact schema |
| RC5-02 실패 복원 overlay | P1 열림 | 5단계 purge/rollback/attempt 분리 |
| RC5-03 thermal 재도장 | P1 열림 | projection clear + **근본수정**(§2) |
| RC5-04 Physics 유실 | P1 열림 | 모듈 분리 + 두 모드 병합 |
| RR3-04 batch contact | 미수정 | `fresh=True` **배선** |
| SyntaxWarning ×2 | 열림 | 0건 |

`test_pipeline_provenance` 43 → **71/71**.  전수 compile 409 files · Warning 0.

⚠ 먼저 자인: 이 회차 문서는 **4일간 처리되지 않았다**.  사용자가 "이것도 반영됐나"
라고 묻기 전까지 내 추적 목록에 RC5 항목이 없었다.  누락 자체가 프로세스 결함이다.

## 1. RC5-01 / 02 / 04 / RR3-04 — 권고를 그대로 구현

세부는 `docs/codex_round5_response_20260811.md`.  요약만:

- **RC5-01**: 제시된 11-키 exact schema.  **하드코딩 전에** 그 목록이 `run_one` 에서
  정말 무조건 쓰이는지 소스로 확인했다 (전부 함수 최상위 4칸 들여쓰기 = 조건부 밖,
  `798·809-817·865`).  `None` 은 없는 것으로 세고 `0.0` 은 통과.
- **RC5-02**: 권고 5단계 그대로 — 전수 purge → overlay → raw thermal
  `{present,value}` rollback → `failed_no_active_generation` → `stage_e_attempt.json`.
- **RC5-04**: 원인은 **이름 규약 오해**였다.  `--contact-mode both` 은 접미사를
  **키가 아니라 파일명**에 붙인다 (두 파일의 키가 동일).  `_run_solver` 가 legacy
  (=hertzian 복사본) 하나만 읽는데 호출부는 `*_physics` 를 조회 → 항상 None.
  `scripts/network_mode_io.py` (신규, 11/11) 로 분리.
  ★ **분리한 이유**: 원래 자리가 pandas 를 import 해서 이 함수를 회귀로 검증할 수
  없었다 — "테스트할 수 없는 자리에 있었다" 가 버그가 오래 숨은 이유 중 하나다.
- **RR3-04**: `run_stage(fresh=True)` 가 RV-02 에서 **구현만 되고 어느 호출부에도
  배선되지 않았다** (`grep fresh=True webapp/app.py` → 0건).  batch contact 에 배선.

## 2. ★ RC5-03 — 증상 처리에서 근본수정으로 (이번 라운드의 핵심)

5회차는 "thermal 이 이 모델의 필수 채널이라면 H/P 누락은 명시적 network failure 가
더 안전하다" 고 **조건부로** 썼다.  나는 그 조건을 사용자 결정으로 넘겼는데,
사용자가 **"thermal 누락이 안 되게 하면 되는 것 아니냐"** 고 물었고 그게 맞았다.

원인을 다시 보니 **두 개의 다른 사건이 downstream 에서 똑같이 "키 없음"** 이었다:

| 사건 | 진짜 의미 | 옛 표현 |
|---|---|---|
| 열망 미퍼콜 | κ 가 없는 것이 **물리적으로 옳은 답** | 키 없음 |
| 솔버 예외 | 값이 있어야 하는데 못 낸 **소프트웨어 실패** | 키 없음 |

```python
except Exception as e:
    print(f"  Thermal solver failed: {e}")   # 삼키고 계속
...
if results_th:                                # 거짓이면 키를 아예 안 씀
```

**구분이 불가능하니 상위가 판단할 근거가 없었다** — 그래서 "실패로 볼까" 라는 질문
자체가 답할 수 없는 것이었다.  ⇒ solver 가 `thermal_status` 를 **항상** 남기게 했다
(`computed` / `valid_zero` / `valid_null` / `failed` / `no_result` + reason).
누락이라는 상태 자체를 없앴다.  파이프라인은 `thermal_channel_verdict()` 로 갈라
**`failed` 만** 단계 실패로 본다.  옛 세대(상태 필드 없음)는 `unknown` 이며
**소급 실패시키지 않는다**.

## 3. ★ STEP3 (MPM 쪽) 에도 같은 결함이 따로 있었다

사용자가 "network solver/Stage E 는 MPM 도 하잖아 (STEP3)" 라고 지적해 확인한 결과,
`scripts/mpm_webapp_payload.py` 의 STEP3 thermal 도 같은 모양이었다:

```python
except (Exception, SystemExit) as _e_th:
    print(f"  ⚠ STEP3 thermal skip: ...")     # step3['thermal'] 을 안 남긴다
```

→ status/reason 스텁을 쓰게 고쳤고, 성공 경로의 "풀 수 없음"(정상)에도 대칭으로
상태를 박았다 (`not_solvable` vs `failed`).

**여기서 나온 구조적 교훈**: 웹앱 파이프라인과 MPM 킷은 **다른 파이프라인**이라
(웹앱은 STEP3 를 부르지 않고 `run_mpm.sh` 가 부른다) 웹앱 코드리뷰의 수정이 STEP3 에
자동 적용되지 않는다.  같은 결함이 양쪽에 따로 있었던 것이 그 실례다.
CLAUDE.md frame[5] 에 이 경고를 명문화했다.

## 4. CLAUDE.md 정정 — "MPM 은 transport σ 를 못 낸다" 는 틀렸다

같은 지적에서 나온 것.  frame[1]/[5] 의 옛 문장이 STEP3 도입 후로는 사실이 아니다 —
`voxel_conductivity.py` docstring 자신이 "gives the MPM a TRANSPORT readout (it had
only mechanics) → a SECOND, independent σ" 라고 적고 있다.  4곳 정정:

| | `network_conductivity.py` | `voxel_conductivity.py`·`step3_sigma.py` |
|---|---|---|
| 이산화 | DEM 구의 **접촉망** (접촉당 Holm 협착) | MPM **복셀** (유한체적 ∇·(σ∇φ)=0) |
| 채널 | ionic · electronic · thermal | ionic · electronic · thermal |
| 실행 | 웹앱 파이프라인 | MPM 킷 |

정확한 문장: MPM 이 못 내는 것은 **접촉망 방식의 σ** 이지 σ 자체가 아니다.

## 5. 반증(falsification) 확인 — 회귀가 실제로 결함을 잡는가

회귀를 추가한 뒤 **고친 코드를 일부러 되돌려** FAIL 하는지 확인했다:

| 회귀 | 되돌린 것 | 결과 |
|---|---|---|
| F-18 (31) | `sys.executable` → `'python3'` | FAIL ✓ |
| RC5-02 (a, b) | purge/rollback → 옛 overlay | 정확히 2건 FAIL ✓ |
| RR3-04 (a vs b) | `fresh=True` 유무 | 존재확인=통과 / fresh=실패 ✓ |

⚠ **RC5-01·03·04 는 반증 확인을 하지 않았다** (회귀를 붙이며 동시에 고쳤다).

## 6. 스스로 아는 약점

1. **`fresh` 는 전체 지문 비교**라 4개 중 1개만 새로 쓰는 **부분 쓰기는 통과**한다.
   최종형(빈 candidate 실행)이 아니다.
2. **`_collect_modes` 는 평평한 병합**이다 (`<key>_physics`).  권고한 구조화
   `{hertzian, physics}` + mode×channel 완전성 검사가 아니다 — 호출부 전체를
   건드리지 않으려고 값 정확성만 먼저 닫았다.
3. **`thermal_status` 는 thermal 에만** 있다.  ionic/electronic 은 여전히 무상태다
   (권고한 6-record 행렬의 1/6 만 구현한 셈).
4. **`unknown` 을 통과시킨다** — 옛 세대를 소급 실패시키지 않으려는 선택인데,
   그 결과 상태 필드가 없는 산출물은 영원히 검사받지 않는다.
5. RC5-03 수정이 **실 코퍼스에 미치는 영향을 측정하지 않았다** — projection clear 로
   지금 게시된 케이스 중 몇 개가 채널을 잃는지 모른다.
6. STEP3 수정은 **실행해 보지 않았다** (GPU 필요).  코드 경로만 맞췄다.

## 7. 검증·반박 요청 8건

- **Q1 (RC5-01 스키마)**: 11-키가 정말 `run_one` 의 무조건 집합인가?  내가 들여쓰기로
  판단했는데 조기 return·예외 경로로 건너뛰는 분기가 있는가?  `None` 을 결손으로
  세는 규약이 **정당한 0/None 결과**를 실패로 오진할 여지는?
- **Q2 (RC5-02 순서)**: purge → overlay → raw rollback 순서가 옳은가?  `is_stage_e_key`
  가 못 잡는 관리 키가 아직 있는가 (purge 가 그만큼 새는 것)?  `stage_e_attempt.json`
  이 active 필드에서 빠지면서 **깨지는 소비처**가 있는가?
- **Q3 ★ (RC5-04 정확성)**: `<key>_physics` 평평 병합이 호출부의 조회와 **정확히**
  맞는가?  실 솔버 출력으로 확인해 달라 — 나는 fixture 로만 검증했다.
  두 모드가 **다른 키 집합**을 낼 때(한쪽에만 있는 키) 접미사 충돌은 없는가?
  `_modes_present == ['legacy']` 폴백이 조용한 열화를 만드는가?
- **Q4 (RC5-03 상태 분류)**: `valid_zero`/`valid_null` 을 ok 로 보는 것이 옳은가?
  `no_result`(예외 없이 None 반환)를 지금 **ok 도 fail 도 아닌 unknown** 으로
  흘리는데, 그것이 §6-4 의 구멍과 합쳐져 무음 통과를 만드는가?
- **Q5 (RR3-04 배선)**: `fresh=True` 를 batch contact 에만 걸었다.  archive
  reanalyze·retry 경로에도 필요한가?  fresh-dir 경로에서 거짓 실패가 나지 않는다는
  내 판단(`before` 가 비면 stale 판정 안 함)이 맞는가?
- **Q6 ★ (STEP3 대칭성)**: 웹앱 쪽에서 고친 결함 중 **STEP3 에도 같은 모양으로
  있는 것이 더 있는가**?  이번엔 thermal 하나를 사용자 지적으로 찾았는데, 나는
  두 파이프라인을 대조 점검할 체계가 없다.  (`step3_sigma.py`·`mpm_webapp_payload.py`
  의 예외 처리·결손 표현 전반)
- **Q7 (코퍼스 영향)**: §6-5.  projection clear 가 기존 게시본에 미치는 영향을
  추정할 방법이 있는가?  재분석 없이 판별 가능한가?
- **Q8 (누락 프로세스)**: §0 의 4일 누락은 코드가 아니라 프로세스 결함이다.
  리뷰 항목이 큐에서 사라지지 않게 하는 장치를 리포 안에 둘 수 있는가
  (미해결 레지스트리 + 회귀에서 참조 등)?

## 8. 검증 기록

```
webapp/test_pipeline_provenance.py   71/71 PASS   (43 → 71)
webapp/test_security_phase_a.py      28/28 PASS
scripts/network_mode_io.py           11/11 PASS   (신규)
scripts/press_units.py               14/14 PASS
scripts/summarize_jam_sweep.py       10/10 PASS
scripts/heckel_analysis.py           20/20 PASS
scripts/unpack_kit_scaffolds.py      13/13 PASS
리포 전수 compile                     409 files · SyntaxWarning 0 · SyntaxError 0
```

변경 파일 15 · +843/−40.  `git diff 466926c5..8529e114`.
