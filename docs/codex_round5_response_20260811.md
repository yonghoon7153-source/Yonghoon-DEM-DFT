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

## 2. 고치지 않은 것 — 상태와 이유

| ID | 상태 | 확인한 현재 코드 | 왜 이번에 안 했나 |
|---|---|---|---|
| **RC5-02** | 열림 | `app.py:2982-2996` 이 `_se_saved` 를 **overlay** 만 한다 (실패 후보가 새로 만든 키·raw thermal 잔존) | Codex 가 제시한 5단계(전수 purge → overlay → raw `{present,value}` rollback → `failed_no_active_generation` → attempt 분리)는 실패 경로 재설계다.  회귀 없이 손대면 지금 통과하는 RC4-01 복원을 깨뜨릴 위험이 크다 |
| **RC5-03** | 열림 | merge 가 새 JSON 에 key 가 있고 non-None 일 때만 덮어써, 누락 thermal 이 새 run_id 아래 존속 | network-owned projection 을 merge 전에 **전부 clear** 하는 것이 정답인데, 그러면 "thermal 누락 = network failure" 인지 여부를 먼저 정해야 한다 (Codex도 "필수 채널이면 명시적 실패가 안전" 이라고 조건부로 씀).  **결정이 필요한 항목** |
| **RC5-04** | 열림 | `run_network_full_corrections._run_solver()` 가 `--contact-mode both` 로 돌리고 `network_conductivity.json` **하나만** 읽어 반환 (line ~504) — Physics 결과 폐기 | 반환형을 `{hertzian, physics}` 로 바꾸는 것은 호출부 전체(`run_one` 의 `*_physics` 조회)를 함께 고쳐야 한다.  Codex 가 `500/1000/1500` 이 실제 재솔브가 아니라 옛 baseline×0.5 임을 보였으므로 **영향 범위가 넓다** — 별도 작업으로 잡는 것이 안전 |
| **RR3-04** | 열림 | batch contact 가 산출물 **존재만** 확인 | Codex 가 재현기를 보정하니 network 1회·Stage E 1회가 다시 실행됨 = 본질 미수정.  최종형은 "빈 candidate 에서만 실행" |
| SyntaxWarning ×2 | 열림 | `figure1_panels.py:333` `\s`, `step4_rint_ladder.py:12` `\ ` | 사소 |
| scripts bare python3 ×3 | 신규 등재 | 위 §1 | webapp route 아님 |

## 3. 다음 우선순위 (Codex §10 을 우리 사정에 맞춰)

1. **RC5-04** — Physics 결과 유실은 **값이 틀리게 나오는** 유일한 항목이다 (나머지는
   세대/도장 무결성).  `_run_solver` 반환 구조화 + 호출부.  ★ 먼저.
2. **RC5-03** — 그 전에 "thermal 누락 = network 실패인가" 결정 필요.
3. **RC5-02** — 실패 경로 전수 purge/rollback + attempt 분리.
4. **RR3-04** — batch contact 를 빈 candidate 에서 실행.
5. PD-02 sentinel · PD-04 압력 네 축 · grid convergence gate.

## 4. 검증 기록

```
webapp/test_pipeline_provenance.py   55/55 PASS   (43 → 55; RC5-01 7건 + F-18 1건 추가)
webapp/test_security_phase_a.py      28/28 PASS
scripts/press_units.py               14/14 PASS
compile (app, pipeline_service)      OK
F-18 회귀 반증 확인                   되돌리면 FAIL, 복원하면 PASS
11-키 무조건성                        run_one 소스에서 들여쓰기로 확인 (조건부 아님)
```
