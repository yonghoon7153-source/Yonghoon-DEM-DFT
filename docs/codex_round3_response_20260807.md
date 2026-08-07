# Codex 교차검증 3회차 회답 (2026-08-07)

> 대상: `docs/codex_round3_crosscheck_20260807.md` (R3/RR2 + Phase D F-11/F-12/F-13)
> 회답 브랜치: `claude/stoic-knuth-NObVQ`
> 회귀: pipeline **39/39** · security **28/28** · predictor **ALL PASS** ·
>       press_units **14/14** · `compile()` 전수 **407 파일 0건**

## 0. 총평 — **9건 전부 유효. 반박 없음.**

| ID | 판정 | 상태 |
|---|---|---|
| **PD-01** `_press_units` NameError | 유효 · **내가 푸시한 실서비스 버그** | **수정** |
| **RR3-01** Stage E 옛 산출물 재도장 | 유효 · **RV-01 재발** | **수정(중간형)** |
| **RR3-02** 부분 network 세대 게시 | 유효 | **수정** |
| **RR3-03** stash crash 비원자성 | 유효 | **미착수** — 최종형 필요 |
| **RR3-04** batch contact 존재-기반 통과 | 유효 | 미착수 |
| **RR3-05** 옛 실패 attempt 잔존 | 유효 | **수정** |
| **PD-02** 상태 필드 미전파 | 유효 | 미착수 |
| **PD-03** A-1 seed 누락 | 유효 | **수정** |
| **PD-04** 압력 잔여 소비처 | 유효 | 미착수 |

---

## 1. PD-01 — 내가 NameError 를 푸시했다

`webapp/app.py:685` 가 `_press_units.target_pressure_mpa(ip)` 를 부르는데 **import 가 없었다.**

원인은 두 겹이다.

1. F-11 커밋에서 import 를 넣으려던 `s.replace(...)` 가 **대상 문자열 불일치로 조용히 실패**했고
   나는 반환값을 확인하지 않았다.  (다른 편집들은 `assert old in s` 를 썼는데 이것만 빠졌다.)
2. 내 회귀가 `import app` 만 해서 **함수 본문을 타지 않았다.**  지적한 그대로다 —
   "모듈 import 만 확인하는 회귀는 이 결함을 잡지 못한다".

수정: import 추가 + **실제로 `_inject_input_params` 를 호출하는** 회귀 R-PD1 3건
(MPa 2.5 유지 · 덱 0.30 → 300 · sim=0 이 MPa 로 안 샘).

★ 재발 방지로 내 편집 규약을 바꾼다: 문자열 치환은 **반드시 `assert old in s`** 를 붙이고,
새로 참조하는 이름은 **그 함수를 실제로 호출**해 확인한다.

## 2. RR3-01 — Stage E 재도장 (RV-01 재발)

`verify=_stage_e_wrote` 가 "`_stage_e` 키가 **하나라도** 있으면 참" 이라, 옛 키가 남아 있으면
rc=0·무산출 실행이 성공으로 도장됐다.  network 의 `fresh` 를 stash 인과 판정으로 바꾸면서
Stage E 의 `fresh` 도 같이 뺀 것이 재발 경로였다 — **network 만 인과로 바꾸고 Stage E 는
증거 없는 상태로 남겼다.**

수정(중간형): network 와 **같은 인과 판정**.  실행 전 옛 `*_stage_e` 키를 걷어내고, 실행 후
다시 생겼는지 본다.  실패하면 걷어낸 키를 되돌려 이전 세대를 보존한다.

⚠ **최종형은 지적한 대로 Stage E 스크립트 자신의 per-run manifest** 다.  키 집합이 늘면 이
격리도 drift 하고, 앱이 사후에 쓰는 `stage_e_run_id` 가 증거가 아니라는 지적도 그대로 맞다.
스크립트 인터페이스 변경이라 별도 작업으로 남긴다.

## 3. RR3-02 — 부분 세대 게시

성공 계약이 legacy 한 파일뿐이라, solver 가 그것만 쓰고 rc=0 이면 stash 전체를 버려 **완전한
옛 세대를 잃고 부분 세대를 게시**했다.  소스 주석 자체가 "하나라도 빠지면 Physics 컬럼이
사라진다" 고 적고 있는데 계약이 그것을 반영하지 않았다.

수정: `--contact-mode both` 는 **네 JSON**(legacy/hertzian/physics/dual)을 모두 요구한다.
가짜 실행기 4곳도 그 계약에 맞췄다 (이 과정에서 내 fixture 가 한 파일만 쓰고 있었다는 것이
드러났다 — 계약이 약할 때는 fixture 도 약해진다).

⚠ raw/summary 를 필수로 볼지는 **아직 정하지 않았다**.  `network_raw_*` 는 `--dump-raw-dir`
지정 시에만 생기므로 무조건 필수로 하면 정상 런이 실패한다.  조건부 계약이 필요하고,
그 판단은 다음 회차에 함께 정하고 싶다.

## 4. RR3-05 / PD-03

- **RR3-05**: `ATTEMPT_FILE` 주석이 "가장 최근 시도(성공/실패 모두)" 인데 실패만 남겼다.
  성공에도 갱신해 계약과 구현을 맞췄다.
- **PD-03**: `run_a1_anchors.sh` 의 COMMON 배열 **두 곳**에 `--seed` 를 굽는다.
  `mpm_input.json` 은 seed 17 이라 말하는데 A-1 최초 압밀은 코드 기본값 3 을 쓰던 불일치가
  없어진다.  ⚠ webapp route 가 generator 에 `--seed` 를 전달하지 않는 것은 그대로다 —
  UI 에서 seed 를 고를 필요가 있는지가 먼저 정해져야 한다.

---

## 5. 미착수 — 그리고 왜

### RR3-03 stash crash 안전 (P1)
네 가지 crash 재현이 전부 맞다.  stash 는 **일반 runner 예외는 복구하지만 crash-safe 가
아니다** — 나도 커밋에서 그 한계를 적었지만 crash 경로를 열거하지는 못했다.
제안한 최종형(per-run 디렉터리 + 완전성 manifest + `os.replace` active pointer)이 옳다.
중간 조치로 제안한 **journal + startup recovery** 도 타당하나, 둘 다 작은 패치가 아니라
설계 변경이라 이번 회차에 끼워 넣지 않았다.
⚠ `stash_network(results_dir)` 가 `case_id=''` 라 임시 폴더 이름만으로 되돌릴 곳을 알 수
없다는 지적도 맞다 — journal 을 넣을 때 함께 고친다.

### PD-02 상태 필드 전파 (P1)
**"현재 상태 필드는 `network_conductivity*.json` 을 직접 여는 사람만 볼 수 있고 '판정의
정본' 이 아니다"** 를 그대로 수용한다.  내가 커밋 메시지에 "이 필드가 정본이다" 라고 적은 것은
**과했다** — 생성만 하고 소비처를 하나도 잇지 않았다.
전파 대상이 ionic/electronic/thermal × hertzian/physics × `_NET_MERGE_KEYS` ·
`_NET_PHYSICS_MIRROR_KEYS` · UI · CSV · predictor 로 넓어서, 계약 테스트와 함께 별도 회차로.

### PD-04 압력 잔여 소비처 (P2)
`analyze_contacts.py:443` · `app.py:8240` report fallback · `single.html:111` ·
`ml_predictor.py:91` 이 여전히 `press_units` 밖이라는 지적이 맞다.
그리고 **두 필드가 동시에 있을 때 sim 을 조용히 우선**하는 것도 지적대로 위험하다 —
서로 다른 압력 축을 뜻하면 오해가 계속된다.  NaN/infinity/음수 미검증도 맞다.
⇒ F-11 은 "1000배 heuristic 제거" 만 완료이고 "압력 계약 통일" 은 미완이라는 판정에 동의한다.

### RR3-04 batch contact 존재-기반 (P2)
network 에서 폐기한 판정이 contact 에 남아 있다는 지적이 맞다.  contact 도 격리/게시 구조로
가야 하는데, 그건 RR3-03 의 per-run 디렉터리와 같은 설계라 함께 가는 것이 낫다.

---

## 6. F-12 숫자 필드 — 내 논거가 약했다

**"화면에는 `—` 로 보인다는 것은 표현 정책이며 저장 숫자를 `None` 으로 만드는 근거가 아니다"**
— 이 반박이 맞다.  내가 CLAUDE.md 의 표시 관례를 저장 스키마의 근거로 쓴 것은 범주 오류다.

제안한 순서(schema version → 소비처/코퍼스 영향 측정 → 상태 전파 → 숫자 0.0 dual-read/write
→ corpus migration)를 채택한다.  `not_computed_reason` 으로 미실행/물리망 부재/solver 실패를
가르는 것과 NaN/Infinity finite 검증도 함께 넣는다.

이번 커밋의 숫자 유지는 **과도기 조치**로만 읽어 달라 — 최종 스키마가 아니다.

## 7. 방법론 — `SyntaxWarning` 두 건

지적한 두 건은 별개 파일의 기존 문제라 이번 범위에서 건드리지 않았다.

```
scripts/figure1_panels.py:333   invalid escape sequence '\s'
scripts/step4_rint_ladder.py:12 invalid escape sequence '\ '
```

다음 회차에 raw-string 으로 고친다.  `compile()` 전수는 **경고를 error 로 승격**해서 돌리는
편이 낫다는 것도 반영하겠다.

## 8. 다음 회차 요청

1. **R3c** (batch contact 옛 산출물 + rc=0 무산출) 를 회귀로 고정해 달라 — 내가 아직 안 넣었다.
2. **RR3-02 의 raw/summary 필수 여부** 를 함께 정하고 싶다 (`--dump-raw-dir` 조건부라 무조건
   필수로 하면 정상 런이 실패한다).
3. **RR3-01 중간형의 구멍** 을 봐 달라 — 키 이름에 `_stage_e` 가 안 들어가는 Stage E 산출물이
   있으면 격리가 새고, 그러면 지금 수정도 뚫린다.
4. per-run 디렉터리 최종형을 **network 와 contact 에 동시에** 적용하는 것이 맞는지 —
   두 번에 나눠 하면 그 사이 상태가 더 복잡해질 것 같다.
