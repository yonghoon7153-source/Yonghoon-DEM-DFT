# Codex 5회차 회답 — RC5 / F-18 (늦은 처리, 2026-08-11)

대상: "Codex 5회차 교차검증 — RC4 수정 재검증과 Stage E/per-run 계약 (2026-08-07)"
(검증 좌표 `baa9d74f` / Codex `d7cfe7c4`).

## 0. 먼저 — 이 회차는 4일간 처리되지 않았다

사용자가 "이것도 반영이 된 건가?" 라고 물어 확인한 결과 **RC5-01~04·RR3-04·F-18 전부
미반영**이었다.  8월 7일 이후 내 추적 목록에 RC5 항목이 아예 없었고 (Heckel/MPM 쪽으로
넘어가면서 이 문서를 큐에 넣지 않았다), F-18 은 Codex 가 **자기 브랜치에서만** 고쳤다는
사실도 놓쳤다.  누락 자체가 프로세스 결함이므로 여기 적어 둔다.

## 1. 이번에 고친 것

### F-18 — Windows mpm-input 500 (수용, 이식)

`webapp/app.py` 의 `/results/<case>/mpm-input` 이 `cmd = ['python3', gen, …]` 이었다.
Codex 가 실측한 `500 → 200` 수정(`sys.executable`)을 그대로 적용했다.

회귀는 Codex 지적대로 **HTTP 코드가 아니라 인터프리터 인자**를 본다 — 리눅스에는
`python3` 가 있어서 200 이 나오므로 코드로는 false-green 이다.  `app.py` 를 AST 로 걸어
리스트 리터럴의 **첫 원소가 `'python3'` 인 것**을 전부 찾는다 (회귀 31).
일부러 되돌려 FAIL 하는 것까지 확인했다.

⚠ `scripts/` 쪽에는 bare `python3` 가 3곳 남아 있다 (`a3_binder_sweep.py:32`,
`backfill_stage_e_physics.py:91`, `rerun_network_for_missing.py:93`).  webapp route 가
아니라 CLI 도구라 Windows 500 과는 무관하지만 같은 취약점이다 — **미해결로 등재**.

### RC5-01 — partial Stage E 가 success 로 도장되던 것 (수용)

옛 판정: `any('_stage_e' in k for k in full_metrics)`.  Codex 동적 재현대로
`garbage_stage_e: null` **한 개**로도 새 parent/run/code-SHA 가 success 였다.

Codex 가 제시한 11-키 exact schema 로 교체했다.  **하드코딩 전에 그 목록이 정말
무조건 쓰이는지 코드로 검증**했다 — `run_network_full_corrections.py` 의 해당 대입이
전부 함수 최상위(4칸 들여쓰기, 조건부 블록 밖)임을 확인 (`798·809-817·865`).
loss 3필드·temperature provenance·thermal heal 은 조건부라 제외.

`pipeline_service.STAGE_E_REQUIRED_KEYS` + `stage_e_missing_keys()` 로 공유하고,
**값이 `None` 이면 없는 것으로 센다** (Codex 가 `sigma_full_mScm_stage_e: null` 도
success 인 것을 재현했으므로).  진짜 `0.0` 은 통과한다.

Codex 의 네 동적 재현을 그대로 회귀로 고정 (24~30):

| 입력 | 옛 판정 | 새 판정 |
|---|---|---|
| 완전한 11-키 | success | **통과** |
| `garbage_stage_e: null` | success | **거부** |
| `sigma_full_mScm_stage_e: null` | success | **거부** |
| `stage_e_source` 만 | failure | 거부 (유지) |
| 출력 없음 | failure | 거부 (유지) |

★ 부수 효과가 Codex 의 다른 지적을 입증했다: 계약을 엄격히 하자 **회귀 fixture 3곳이
깨졌다** (FakeRunner 가 키 하나만 썼다).  이것이 RR3-04 의 false-green 과 같은
fixture-drift 다 — fixture 를 실제 `run_one` 계약에 맞춰 고쳤다.

## 2. 2차 (같은 날) — 남은 것 전부 처리

사용자가 "시간은 많다" 고 해서 미뤄 뒀던 넷을 이어서 했다.

### RC5-04 — Physics 재솔브 결과 유실 (값이 틀리던 유일한 항목)

원인이 **이름 규약의 오해**였다.  `--contact-mode both` 은 접미사를 **키가 아니라
파일명**에 붙인다:

```
network_conductivity_hertzian.json → {'sigma_full_mScm': …}
network_conductivity_physics.json  → {'sigma_full_mScm': …}   ← 같은 키!
network_conductivity.json          → hertzian 의 복사본 (하위호환)
```

`_run_solver` 는 legacy 하나만 읽었는데 호출부는 `res.get('sigma_full_mScm_physics')`
를 조회했고 — "같은 JSON 에 `*_physics` 짝이 있다"는 **틀린 주석까지** 달려 있었다 —
그 값은 항상 None 이라 매번 fallback 으로 샜다.

→ `scripts/network_mode_io.py` (신규, selftest 11/11) 로 두 모드를 다 읽어
`<key>` / `<key>_physics` 로 합친다.  구조화(`{hertzian, physics}`)가 더 깔끔하지만
호출부 전체를 건드려야 해서 **값이 틀리는 문제부터 최소 변경**으로 닫았다.

★ **별도 모듈로 뽑은 이유**: 원래 자리(`run_network_full_corrections.py`)가 pandas 를
import 해서 이 함수 하나를 회귀로 검증할 수 없었다.  버그가 오래 숨은 이유 중 하나가
"테스트할 수 없는 자리에 있었다" 는 것이므로 검증 가능한 자리로 옮겼다.  결손 채널은
`_modes_missing_channels` 로 반드시 드러낸다 (조용한 결손이 이 버그를 숨겼다).

### RC5-02 — 실패 복원이 overlay 뿐이던 것

Codex 권고 5단계를 그대로 구현했다: ① 현재 관리 키 **전수 제거** → ② 이전 active
overlay → ③ raw thermal `{present, value}` rollback (`snapshot_keys`/`restore_keys`
— 없던 키를 None 으로 되살리지 않는다) → ④ 이전 active 가 없으면
`failed_no_active_generation` → ⑤ 시도는 `stage_e_attempt.json` 별도 파일
(`record_stage_e_attempt`, network 의 RR2-01 과 같은 규약).

반증 확인: purge/rollback 을 옛 overlay 로 되돌리니 정확히 두 회귀가 FAIL 한다.

### RC5-03 — 누락 채널이 옛 값으로 메워지던 것

merge 가 `if k in net_data and net_data[k] is not None` 이라 새 세대가 못 낸 채널은
옛 값이 **새 run_id 아래** 살아남았다.  → merge 전에 network-owned projection 을
**전부 걷어내고** 새 세대로만 채운다.  걷힌 채널은 `network_projection_dropped` 에
기록하고 로그에 찍는다.

⚠ "thermal 누락 = network 실패인가" 는 **여기서 결정하지 않았다** — 채널이 필수인지에
대한 판단이 필요하다.  다만 누락을 조용히 옛 값으로 메우는 것만은 확실히 막았다.
(사용자 결정 대기 항목으로 남긴다.)

★ 부수 발견: 이 수정이 RC5-02 회귀 하나와 충돌했는데, **새 동작이 옳았다** —
preserve=False 경로는 새 network 세대가 먼저 돌므로 옛 thermal 이 사라지는 것이 맞고,
RC5-02 가 보장할 것은 "Stage E 가 쓴 값이 남지 않는다" 였다.  회귀 문구를 정정했다.

### RR3-04 — batch contact 존재-확인

★ **더 큰 것이 나왔다**: `run_stage(fresh=True)` 는 RV-02 에서 **구현만 하고 어느
호출부에도 배선되지 않았다** (`grep fresh=True webapp/app.py` → 0건).  batch contact 에
배선했다.  회귀에 **배선 자체를 검사하는 항목**(RR3-04d)을 넣었다 — 구현과 배선이
다르다는 것을 이번에 두 번 겪었다 (alias 를 파일에 쓴 것, 패키지를 깐 것).

⚠ 최종형은 Codex 권고대로 **빈 candidate 에서만 실행**하는 것이다.  `fresh` 는 전체
지문 비교라 **부분 쓰기**(4개 중 1개만 새로 씀)는 여전히 통과한다.

### SyntaxWarning ×2 — 정리

`figure1_panels.py:333` 의 LaTeX `$\sigma$` 를 raw string 으로,
`step4_rint_ladder.py` 모듈 docstring 을 raw 로 (셸 예시의 `\ ` 이스케이프).
리포 전수 재확인: **409 files · SyntaxWarning 0 · SyntaxError 0**.

## 3. 남은 것 (2차 후)

| 항목 | 상태 |
|---|---|
| "thermal 누락 = network 실패인가" | **사용자 결정 대기** |
| Stage E per-run manifest (최종형) | 스크립트 인터페이스 변경 — 별도 작업 |
| batch contact 빈-candidate 실행 (최종형) | `fresh` 로 false-green 은 닫았으나 부분 쓰기는 남음 |
| `scripts/` bare python3 ×3 | CLI 도구, webapp 500 과는 무관 |
| PD-02 sentinel · PD-04 압력 네 축 · grid convergence gate | 미착수 |

## 4. (1차 기록, 참고) 그때 미뤘던 이유 — 전부 §2 에서 해소됨

| ID | 상태 | 확인한 현재 코드 | 왜 이번에 안 했나 |
|---|---|---|---|
| **RC5-02** | 열림 | `app.py:2982-2996` 이 `_se_saved` 를 **overlay** 만 한다 (실패 후보가 새로 만든 키·raw thermal 잔존) | Codex 가 제시한 5단계(전수 purge → overlay → raw `{present,value}` rollback → `failed_no_active_generation` → attempt 분리)는 실패 경로 재설계다.  회귀 없이 손대면 지금 통과하는 RC4-01 복원을 깨뜨릴 위험이 크다 |
| **RC5-03** | 열림 | merge 가 새 JSON 에 key 가 있고 non-None 일 때만 덮어써, 누락 thermal 이 새 run_id 아래 존속 | network-owned projection 을 merge 전에 **전부 clear** 하는 것이 정답인데, 그러면 "thermal 누락 = network failure" 인지 여부를 먼저 정해야 한다 (Codex도 "필수 채널이면 명시적 실패가 안전" 이라고 조건부로 씀).  **결정이 필요한 항목** |
| **RC5-04** | 열림 | `run_network_full_corrections._run_solver()` 가 `--contact-mode both` 로 돌리고 `network_conductivity.json` **하나만** 읽어 반환 (line ~504) — Physics 결과 폐기 | 반환형을 `{hertzian, physics}` 로 바꾸는 것은 호출부 전체(`run_one` 의 `*_physics` 조회)를 함께 고쳐야 한다.  Codex 가 `500/1000/1500` 이 실제 재솔브가 아니라 옛 baseline×0.5 임을 보였으므로 **영향 범위가 넓다** — 별도 작업으로 잡는 것이 안전 |
| **RR3-04** | 열림 | batch contact 가 산출물 **존재만** 확인 | Codex 가 재현기를 보정하니 network 1회·Stage E 1회가 다시 실행됨 = 본질 미수정.  최종형은 "빈 candidate 에서만 실행" |
| SyntaxWarning ×2 | 열림 | `figure1_panels.py:333` `\s`, `step4_rint_ladder.py:12` `\ ` | 사소 |
| scripts bare python3 ×3 | 신규 등재 | 위 §1 | webapp route 아님 |

## 5. 검증 기록 (최종)

```
webapp/test_pipeline_provenance.py   65/65 PASS   (43 → 65)
webapp/test_security_phase_a.py      28/28 PASS
scripts/network_mode_io.py           11/11 PASS   (신규)
scripts/press_units.py               14/14 PASS
scripts/summarize_jam_sweep.py       10/10 PASS
scripts/heckel_analysis.py           20/20 PASS
scripts/unpack_kit_scaffolds.py      13/13 PASS
리포 전수 compile                     409 files · SyntaxWarning 0 · SyntaxError 0
```

**반증(falsification) 확인** — 회귀가 실제로 결함을 잡는지 되돌려 본 것:

| 회귀 | 되돌린 것 | 결과 |
|---|---|---|
| F-18 (31) | `sys.executable` → `'python3'` | FAIL ✓ |
| RC5-02 (a, b) | purge/rollback → 옛 overlay | 정확히 2건 FAIL ✓ |
| RR3-04 (a vs b) | `fresh=True` 유무 | 존재확인만이면 통과, fresh 면 실패 ✓ |

11-키 무조건성은 `run_one` 소스의 들여쓰기로 확인(조건부 블록 밖).
