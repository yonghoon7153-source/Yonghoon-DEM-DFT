# Codex 독립검증 요청 — RC6 전건 (2026-08-11, 7회차)

검증 좌표: `claude/stoic-knuth-NObVQ @ 23211e25` (기준 `8529e114`, 21 files, +2581/−216).
요청: **`claimed_fixed` 9건을 `verified` 로 옮길 수 있는지 판정** + §5 의 질문 7개.

> **판정 원칙 채택**: 6회차의 "구현자의 회귀 PASS 와 결함 종료를 같은 뜻으로 보지
> 않는다" 를 그대로 받아, 이 문서의 모든 항목은 **`claimed_fixed` = 내 주장**이다.
> `verified` 는 독립 검증자만 붙일 수 있고, `scripts/check_review_findings.py` 가
> **자기검증(verified_by == owner)을 거부**하도록 강제한다.

## 0. 원장으로 답한다

산문 대신 기계가 읽는 단일 원장을 만들었다 (Q8):

```
docs/reviews/findings.json          — RC6 11건
scripts/check_review_findings.py    — 자기일관성 검사 (15/15), --open 으로 열린 항목 출력
```

| ID | 심각도 | 상태 | 항목 | fix SHA |
|---|---|---|---|---|
| RC6-01 | P1 | claimed_fixed | schema 가 NaN·타입 통과 + valid_null 충돌 | `7a3c44e3` |
| RC6-02 | P1 | claimed_fixed | 판정 전 active 게시 (stash 이미 폐기) | `0726edcb` |
| RC6-03 | P1 | claimed_fixed | Physics 실패가 H 성공에 가림 | `0726edcb` |
| RC6-04 | P1 | claimed_fixed | Stage E 가 raw thermal 덮어씀 | `496bd99d` |
| **RC6-04b** | P1 | **open** | pre-purge crash window | — |
| RC6-05 | P1 | claimed_fixed | fresh 부분쓰기 + 배선 범위 | `496bd99d` |
| RC6-06 | P1 | claimed_fixed | STEP3 채널 무상태 | `a31afe31` |
| RC6-07 | P1 | claimed_fixed | Windows CP949 | `0726edcb` |
| RC6-08 | P2 | claimed_fixed | GPU backend 미기록 | `a31afe31` |
| **RC6-Q7** | P2 | **open** | corpus preflight scanner | — |
| RC6-Q8 | P2 | claimed_fixed | finding 이 큐에서 사라지는 프로세스 결함 | `2713a0e8` |

## 1. ★ 증거 등급을 스스로 나눈다 — 여기가 검증의 초점

같은 "PASS" 가 아니다.  **어떤 증거로 닫았는지**를 항목별로 밝힌다.

| 항목 | 결함 사전재현 | 수정 후 반증 | 실제 실행 | 증거 등급 |
|---|---|---|---|---|
| RC6-01 | ✓ NaN·not-a-map·[] 가 통과하는 것을 실행으로 확인 | ✗ | ✓ (순수 함수) | **A** |
| RC6-02 | ✓ active=success·stash 폐기·σ999 게시 재현 | ✓ verify 제거 시 2건 FAIL | ✓ | **A** |
| RC6-03 | ✓ 같은 하네스 | ✓ 같은 반증 | ✓ | **A** |
| RC6-04 | ✗ | ✗ | ✗ **소스 계약만** | **C** |
| RC6-05 | ✓ 부분쓰기 통과 재현 | ✓ 4경우 실행 (부분/전부/무산출/빈디렉터리) | ✓ | **A** |
| RC6-06 | ✗ | ✗ | ✗ **소스 계약만** (scipy 부재) | **C** |
| RC6-07 | ✓ 기전 격리 (같은 문자 `—`, 같은 에러) | ✓ 계약 적용 시 rc=0 | 🔶 **실제 solver 는 못 돌림** | **B** |
| RC6-08 | ✗ | ✗ | ✗ **소스 계약만** | **C** |
| RC6-Q8 | — | — | ✓ | **A** |

⇒ **C 등급 3건(RC6-04·06·08)은 "고쳤다" 가 아니라 "고치도록 코드를 바꿨다" 다.**
이 컨테이너에 **scipy·pandas·taichi 가 없어** STEP3·Stage E 재솔브를 실행할 수 없다.
그 셋이 이번 검증의 최우선 표적이다.

## 2. 항목별 — 무엇을 어떻게 고쳤나

### RC6-02/03 — 게시 순서 (지적이 정확했다)

재현이 그대로 나왔다:
```
required 실패 단계 : ['Thermal channel verdict']
★ active provenance: success        ← 실패인데 성공 도장
★ 옛 세대 stash    : 없음(버려짐)
게시된 σ           : 999.0           ← 실패 세대 값
```
→ 내용 검증을 `run_stage(verify=…)` 로 **게이트 안**에 넣었다.  실패하면 기존
`restore_stash` 가 옛 세대를 되살린다.  두 mode 를 각각 본다 (RC6-03).
새로 만든 파일의 `unknown` 은 **fail-closed**(`strict=True`), 옛 세대 읽기는
`strict=False` 로 소급 실패를 만들지 않는다.

⚠ **판정 기준을 한 번 잘못 썼다가 고쳤다**: 처음엔 "복구 후 `solver_status != success`"
를 요구했는데, 복구된 **옛** provenance 가 success 라고 적는 것은 **옳다** (그 세대는
실제로 성공했다).  올바른 기준은 "새 실패 세대가 게시됐는가" 다.

### RC6-01 — schema

타입·유한성까지 본다.  숫자 여섯은 finite number(**bool 명시 배제** — int 서브클래스라
`sigma=True` 가 통과하면 안 된다), 매핑 넷은 dict, method 는 비어 있지 않은 문자열.

★ `valid_null` 충돌은 `null_ok_keys` 인자로 풀었다 — **상류 상태를 알고 있을 때만**
완화한다 (모르면 종전대로 결손).  지적하신 "network 는 valid_null 을 정상으로 보는데
Stage E 는 결손으로 본다" 가 이 인자로 닫힌다.  ⚠ 다만 **호출부가 아직 그것을 채워
넣지 않는다** — 함수는 준비됐고 배선은 안 됐다 (§5-Q2).

### RC6-04 — raw thermal 이중 소유

역산값을 `thermal_sigma_*_stage_e_estimate` + `thermal_baseline_estimate_provenance`
로 분리.  raw 키에 쓰는 코드를 **제거**했다.  화면은 estimate 를
`⚠baseline=유도추정` 라벨과 함께 쓴다 (옛 동작은 추정치를 raw 자리에 넣어 network
측정값처럼 보이게 했다).

★ **부수 발견**: heal 된 baseline 으로 계산한 thermal loss% 는 **항등식**이다 —
`raw = σ_E/f_k` 로 만든 뒤 `loss = 1 − σ_E/raw = 1 − f_k` 라 가중인자를 되읊을 뿐
정보가 0 이다 (수치 확인: f_k 0.62 → loss 38.00 % = (1−f_k)·100).  raw 를 안 만들면
loss% 가 정직하게 생략되고 그것이 옳다.

### RC6-05 — fresh

**파일별** 판정으로 바꿨다.  네 경우 실행 확인:
```
부분 쓰기(1/4)  ok=False  stale=[atoms_analyzed, contacts_analyzed, network_summary]
전부 새로 씀     ok=True   stale=[]
아무것도 안 씀   ok=False  stale=[4개]
빈 디렉터리      ok=True   stale=[]     (거짓 실패 없음)
```
배선도 batch → **batch·bimodal·standard·archive 4경로**.

★ 이 수정이 기존 회귀 하나를 깨뜨렸는데 **그것이 옳았다** — 그 테스트의 writer 가
1개만 쓰는 부분 쓰기였다 (= 지적하신 바로 그 패턴).

### RC6-06/08 — STEP3

`_s3mark(component, status, reason)` 로 통일하고 electronic·ionic·thermal·pore·pnm +
바깥 예외를 등록, `step3['manifest']`(schema_version + status + components)로 박았다.
`step3_sigma.LAST_BACKEND` 에 `{requested, used, fallback_reason}` 를 남겨 manifest 로
흘려보낸다.

⚠ **실행 검증 못 함** (scipy 부재).  제안하신 6-record 행렬 전체가 아니라
component 단위 status 까지다.

### RC6-07 — Windows CP949

실제 solver 는 못 돌렸다(scipy).  대신 **기전을 격리**했다 — solver 1092행이 찍는
문자를 그대로 쓰는 최소 자식을 옛 계약으로 CP949 에서 실행:
```
UnicodeEncodeError: 'cp949' codec can't encode character '—' in position 35
rc=1, JSON 0개                                    ← 관측하신 것과 같은 문자·같은 에러
utf8_subprocess_kwargs 적용 → rc=0, JSON 생성      (env 에 cp949 를 미리 박아둬도)
```
두 호출 지점(`run_stage` · Stage E 재솔브)에 같은 계약.

## 3. 이번 라운드에서 **새로** 발견한 것 (지적 밖)

1. **platen 결함 문서의 상태가 낡았다** — "구현 대기" 라고 적혀 있었으나
   §7-1 동결-프로브(`--stop-freeze-probe`)와 §7-2 감속(`--platen-mach`)은 **둘 다
   구현돼 있었다**.  못 쓰는 이유는 따로다: 얼린 AM 의 wallP 기여가 실측 **0.0 %** 라
   정지 판독이 SE 만 보고, SE 는 실험 공극률에서 목표의 12 % 뿐이라 **정지 조건이
   성립하지 않는다**.  코드가 이미 거부로 막고 있다.
   ⇒ 남은 것은 "처방 구현" 이 아니라 **처방을 켤 수 있게 만드는 것**이고 그 열쇠가
   f_AM 규약(6회차 Q2) 또는 am_jam 케이스-독립성이다.
2. **준정적 한계를 게이트로 바꿨다** — 옛 코드는 `V/c_P > 0.01` 을 print 로만 경고했다.
   이제 `--allow-fast-platen` 없으면 거부하고, 승인하면 metrics JSON 에
   `quasistatic_violation: true` 가 **박힌다** (로그는 보존되지 않는다).
3. **fixture-drift 가 다섯 번 났다** — 계약을 엄격히 할 때마다 fixture 가 깨졌다.
   마지막에 `_healthy_stage_e()` 헬퍼로 한 곳에 모았다.
4. **검사기가 만들자마자 자기 규약을 거부했다** — ID 정규식이 좁아 `RC6-04b`·`RC6-Q7`
   을 형식 오류로 찍었다.

## 4. 아직 안 한 것 (원장 open + 최종형)

| 항목 | 왜 |
|---|---|
| **RC6-04b** pre-purge crash window | candidate/manifest/pointer 전환 전에는 안 닫힌다 (RR3-03 과 같은 뿌리) |
| **RC6-Q7** corpus preflight | tracked corpus 0 이라 이 리포만으로는 비율 계산 불가.  read-only 시뮬레이터가 필요 |
| Stage E per-run manifest | 스크립트 인터페이스 변경 |
| contact **빈 candidate** 실행 | fresh 로 partial 은 닫았으나 최종형 아님 |
| 6-record 행렬 (ionic/electronic) | thermal + STEP3 component 까지만 |
| `scripts/` bare python3 ×3 | CLI 도구 (webapp route 아님) |

## 5. 검증·반박 요청 7건

- **Q1 ★ (증거 C 등급)**: RC6-04·06·08 은 **소스 계약만** 걸었다.  실제 실행에서
  ① Stage E 가 정말 raw thermal 을 안 건드리는가 ② STEP3 manifest 가 실제 payload 에
  나오는가 ③ CuPy 없는 환경에서 `backend.used == 'cpu'` + `fallback_reason` 이 채워지는가.
- **Q2 ★ (배선 누락 자인)**: `null_ok_keys` 는 함수만 준비되고 **호출부가 안 채운다**.
  지금 상태에서 정당한 non-percolating 케이스가 여전히 partial 이 되는가?  채우려면
  Stage E 호출 시점에 network 의 mode×channel status 를 읽어야 하는데, 그 결선이
  RC6-03 의 `network_content_verdict` 와 중복되지 않게 하려면 어디에 두어야 하는가.
- **Q3 (RC6-02 게이트 완전성)**: `verify` 는 thermal status 만 본다.  ionic/electronic
  이 `failed` 인 경우는 여전히 게시된다 — 이것이 RC6-03 의 절반만 닫은 것인가?
- **Q4 (RC6-05 잔여)**: 파일별 판정이 `(mtime_ns, size)` 라 **같은 크기로 덮어쓰면**
  1 ns 해상도 안에서 못 잡을 수 있다.  실무적으로 유효한가, 아니면 content hash 가
  필요한가 (RR2-02 에서 해시 단독은 기각됐었다)?
- **Q5 (준정적 게이트)**: `--allow-fast-platen` 을 러너 3개가 자동으로 붙인다
  (상대비교 목적).  이것이 게이트를 무력화하는가?  metrics 의
  `quasistatic_violation` 기록만으로 충분한 안전망인가?
- **Q6 (원장 설계)**: `check_review_findings.py` 의 강제 규칙이 충분한가?
  특히 "claimed_fixed 인데 evidence_tests 가 **실재하지 않는 테스트**를 가리키는"
  경우를 못 잡는다 (문자열만 본다).  CI 에서 실제 실행까지 묶어야 하는가?
- **Q7 (다음 순서)**: RC6-04b(publish 재설계)와 Q7(코퍼스 스캐너) 중 어느 쪽이
  먼저인가?  내 판단은 **Q7 먼저** — 04b 는 재설계라 크고, Q7 은 read-only 라
  기존 코퍼스를 건드리지 않으면서 04b 재설계의 영향 범위를 미리 재 준다.

## 6. 검증 기록

```
webapp/test_pipeline_provenance.py   103/103 PASS   (43 → 103)
webapp/test_security_phase_a.py       28/28
webapp/test_seminar_page.py           28/28  (신규 — /seminar 개편)
scripts/mpm3d_compaction.py           97/97
scripts/heckel_analysis.py            20/20
scripts/check_review_findings.py      15/15  (신규)
scripts/unpack_kit_scaffolds.py       13/13
scripts/press_units.py                14/14
scripts/network_mode_io.py            11/11
scripts/seminar_deck_extract.py       11/11  (신규)
scripts/summarize_jam_sweep.py        10/10
리포 전수 compile                      409 files · SyntaxWarning 0 · SyntaxError 0
```

**반증 확인** (회귀가 실제로 결함을 잡는지 되돌려 본 것):

| 회귀 | 되돌린 것 | 결과 |
|---|---|---|
| RC6-02/03 | `verify=_verify_content` 제거 | 정확히 2건 FAIL |
| RC6-05 | (사전재현) 부분 쓰기 통과 | ok=True, stale=[] |
| RC6-07 | 옛 subprocess 계약 + CP949 | rc=1, JSON 0개 |
| RC6-01 | (사전재현) NaN·not-a-map·[] | 전부 통과했었다 |

⚠ RC6-04·06·08 은 반증을 하지 않았다 (실행 불가).
