<!-- ★★ 이 문서는 **리뷰 원문 보존본**이다.  아래에 인용된 수치 중 일부는
     `docs/reviews/claims.json` 의 `quotation_ban` 에 등재된 **철회/보류 값**이며,
     여기서는 리뷰어의 지적을 원문 그대로 남기기 위해 인용된다.  인용 금지 목록의
     정본은 `claims.json` 이고, 이 파일의 값을 원고·발표에 옮기지 말 것. -->

# Codex 5차 독립 재리뷰 — SDCP A-track `edec17a2` (2026-08-25)

**판정: 브랜치 흡수 HOLD · GPU 8팔 재실행 HOLD.**

R5 는 실제로 많이 나아졌다.  parser option 수집, top-level 미등록 manifest key 거부,
schema 3 component evidence 검사, backend `used` 권위화, occupied-surface/plate 소산 회귀,
현행 CI 배선은 독립 확인됐다.  `check_all.sh` 초록이고, 독립 Windows 적응판으로 41개
변이체가 모두 물렸다.

그러나 **이 초록을 유지한 채** 다음 production-shaped 우회가 재현됐다.

1. 허용된 `P2_EXTRA` 값 속 환경변수가 생성 스크립트에서 두 번째로 확장되어
   `--show-results` 나 후행 `--expect-physics` 를 주입한다.
2. 현행 p2 manifest 의 `schema_version` 만 `3→2` 로 낮추면 ionic/thermal/pore evidence
   누락이 `HOLD→h0` 로 바뀐다.
3. runner 의 현재 vox·구 직경·periodic·clean code SHA·실제 input digest 가
   cache/fresh/final seal 에 묶이지 않는다.
4. 8개 origin 은 개수와 유일성만 맞으면 되고, 사전등록 `{0, vox/2}³` 가 아니어도 `h0` 다.
5. 계획된 PNM·collector 는 결과 블록이 전혀 없어도 `complete` status 만으로 `h0` 다.
6. 요청서는 p1 σ 값과 SBE/DBE 비를 인용 금지하지만 정본 `claims.json` 과 `CLAUDE.md` 는
   CL-33/41/58 과 그 정량값을 계속 live/사용 가능하게 둔다.

> 따라서 이번 selftest 영수증은 "현재 등록된 검사들이 통과한다" 는 증거이지,
> **현재 runner 가 의도한 물리·코드·입력을 봉인했거나 철회된 과학값이 재인용되지
> 않는다는 증거는 아니다.**

## 증거 고정

| | |
|---|---|
| target branch | `origin/claude/sdcp-dem-manuscript-si-pqwtv8` |
| target | `edec17a22addf75e0fd8dfd3e2dcc101c78722e7` |
| base | `3da9bac81d04cc7df8d100b18a692250023ab884` |
| audit source snapshot SHA-256 | `38C754D84C8BAB7706AC46DBF269D4110F0159E5F7290CB7854D6E0353FE7525` |
| R4→R5 diff SHA-256 | `56F193CEF8EACE78FD4B65358CB7E9BB1FBB156FB5657E42208A6A73BD622B45` |
| protocol/CLI probe transcript SHA-256 | `EE68346240622A6E989F19675765FD1DC979AE7DF58D7A3AFF1888D5E4BBFD16` |

target source 는 수정하지 않았고 merge·GPU 실행도 하지 않았다.

## 신규 finding (원장 R5CX-01~11 이 정본)

P1 — R5-CX-01 `P2_EXTRA` 2단계 shell 확장 우회 · R5-CX-02 schema downgrade 로 증거 계약 OFF ·
R5-CX-03 현재 run identity 미봉인 · R5-CX-04 임의 8-origin 허용 · R5-CX-05 PNM·collector
status-only · R5-CX-06 **canonical quotation-ban 모순** · R5-CX-07 pass-mutant·harness 결함.
P2 — R5-CX-08 기각 receipt 미소비 · R5-CX-09 SWCNT plate 회귀가 생산 map 미사용 ·
R5-CX-10 blind 파생 bucket 노출 · R5-CX-11 standalone bundle 미확인.

### 실측 transcript (핵심 셋)

**schema-only downgrade** — 같은 p2 manifest, `schema_version` 만 변경:

```text
schema=3 pid=p2-56bab3833fbad9ac
 producer= 'STEP3_EVIDENCE: EVID|ionic|result| sigma_ion_eff_S_cm=None (유한한 양수여야 한다)'
 check_arm= '계획한 component 의 증거가 없다 — EVID|ionic|result| …'
 final= HOLD EVID component 증거 계약을 만족하지 않는 팔 16개
schema=2 pid=p2-56bab3833fbad9ac
 producer= None
 check_arm= None
 final= h0
```

**현재 config/SHA/input 미봉인** — HEAD `edec17a2`, runner 기본 vox 0.15 인데:

```text
stored vox_um=0.20  code_sha=deadbeef  input_digest=임의
origins= [0,0,0.00] … [0,0,0.07]   (사전등록 factorial 아님)
producer=None  check_arm=None  final= h0
```

**`P2_EXTRA` 2단계 확장**:

```text
P2_EXTRA='--step3-maxiter=$MPM_ATTACK'  MPM_ATTACK='1 --show-results'
allowlist=PASS staged=<--step3-maxiter=$MPM_ATTACK>
→ 실제 producer argv: <--step3-maxiter=1> <--show-results>
```

## 요청서의 네 공격점에 대한 답

**A. conditional parser registration** — 현재 실행 경로엔 없다.  규칙 M 이 helper 정의
`--temp-c`·`--ea-ion-ev` 포함 80개를 포착했다.  다만 **category 의미 변조**와 미래의
environment-conditional branch 는 보증하지 않는다.

**B. `MANIFEST_RESULT_KEYS` 우회 — 실제 우회가 있다.** `schema_version` 은 허용 key 인데
그 값 `2` 가 evidence validation 을 끈다.  미등록 key 를 숨기는 대신 **등록된 meta key 로
validator 세대를 낮추는** 우회다.

**C. SHA ancestry 변형** — 현행 core logic 은 tag 이름을 hex-only regex 로 거부하고
dangling/rebase·submodule commit 을 ancestry 에서 거부한다.  기록된 fixed/verified SHA
77개는 전부 target HEAD 의 ancestor 였다.  다만 git/HEAD 를 못 쓰면 `_commit_exists()` 가
**경고 없이 성공**으로 돌아가고 19b 가 skip 을 PASS 처럼 표시한다 ⇒ "git 불가 환경에서도
ancestry verified" 라고 주장하면 안 된다.

**D. `broad` 오용 — 가능하고 현재 발생한다.** broad row 가 extra failure 15개를 면제하면서
최종 요약은 `기대 밖 실패 0` 이라고 표시했다.  broad 는 무제한 wildcard 가 아니라
**정확한 허용 ID 집합과 최대 개수**로 바꿔야 한다.

## R4 finding 처분

| R4 | 처분 |
|---|---|
| R4-CX-01 blind/quarantine | still_open — 직접값 masking 개선, deferred `P2_EXTRA` 재주입·receipt 미소비·파생 bucket 남음 |
| R4-CX-02 plan/PTFE/PNM | partial — schema 3 증거는 개선, schema downgrade·PNM/collector status-only 남음 |
| R4-CX-03 runner resolved config | still_open — 현재 SHA/config/input receipt 없음 |
| R4-CX-04 backend authority | partial — production `used` 확인, `backend.across_dir` flip pass-mutant 남음 |
| R4-CX-05 registry/raw/type | partial — top-level 미등록 key 거부, schema exemption·category 불변량 남음 |
| R4-CX-06 K/harness | still_open — exact structured 결과·baseline 완주·broad·dead-control-flow 없음 |
| R4-CX-07 plate | **confirmed_fixed** — reaction sid5/signed-band·occupied-surface·plate dissipation·non-unit-vox FD 변이가 실제로 회귀를 실패시킴 |
| R4-CX-08 namespace/bundle | partial — realpath 개선, standalone bundle 미확인 |

## 독립 baseline (전부 통과)

`run_contract` 41/41 · `check_review_findings` 34/34 · `check_method_discipline` 88/88 ·
`sdcp_gain_verdict` 157/157 · phase ledger 12/12 · `sr01_stamp_compare` 81/81 ·
payload temperature PASS · step3 54 labels rc 0 · live repo checks 2/2.
`--ban-sweep` 도 12패턴 × 430파일 rc 0.
⚠ **그러나 R5-CX-06 의 실제 live 값은 그 패턴 목록 밖이라 이 초록은 정본 안전성의
충분조건이 아니다.**

## 최소 종료조건

1. `P2_EXTRA` 2단계 shell 재해석 제거 + injection 음성 대조
2. p2 schema 3 강제 또는 신뢰 가능한 producer generation/receipt 에 schema binding
3. resolved config·정확한 origin schedule·clean full SHA·actual input digest·backend 를
   담는 **단일 run receipt** 를 cache/fresh/final 에 강제
4. `{0,vox/2}³` exact factorial equality 검사
5. PNM·collector 결과/수치/domain evidence 계약과 complete 전 검증
6. CL-33/41/58 p1 값을 **정본·요약·quotation ban 전부에서** 일관되게 hold/legacy 처리
7. rejection receipt 소비 또는 외부 append-only quarantine ledger
8. exact structured mutation result · baseline 완주 · bounded broad ·
   control-flow-aware 규칙 K · declaration-independent registry/category mutant
9. 생산 phase-map helper 를 소비하는 SWCNT 상주 회귀 + blind 파생 bucket 제거
10. 위 CPU 종료조건을 **모두 독립 변이체로 닫은 뒤에만** 코드 흡수를 재심사하고,
    그 다음 새 p2 GPU 8팔을 실행한다.  **p1 과 p2 산출물은 섞지 않는다.**
