---
title: "결정 레지스트리 설계 v2.1 — codex 3차 P0 반영 (MVP core 4결정)"
date: 2026-08-20
updated: 2026-08-20
tags: [policy, registry, ci, provenance, lineage, tombstone, codex, infrastructure, svp, lambda1]
status: 설계 v2.1 — codex 3차 P0 3건 닫음 (구현 착수 대상 = MVP core 4결정)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: max
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 결정 레지스트리 설계 v2.1

> **판정 이력**
> - v1 (오전) → codex 2차: **조건부 GO**. 아키텍처 4축 GO / 스키마·12시드 즉시구현 NO-GO.
> - v2 → codex 3차: **여전히 NO-GO**. 새 P0 3건 —
>   ① F9 범위가 틀렸다(9/9 부재 아님) ② registry/UI 가 `not_assessed` 를 fail 로 읽는다
>   ③ λ₁ 의 `|nᵢ|≤2` 검사는 certificate 가 아니다.
> - **v2.1 (이 판)**: 세 건을 닫았다. ②③ 은 문서가 아니라 **코드로** 닫았다(아래 §A).
>
> **한 줄**: 규약 역행을 막는 4축(판례집 · 계보 · 단일 평가기 · 래칫)은 유지. 상태 어휘는
> 엔터티별로 재배치했고, λ₁ 은 ASE 정본 Minkowski 축약으로 **exact** 가 됐다.

## A. v2.1 에서 실제로 닫은 것 (코드·데이터 — 설계 아님)

> ⚠ frontmatter 는 `unverified` 다 — **이 절의 5건은 실측 검증됐지만** 문서의 본체(§2–§10)는
> 미구현 설계라 문서 단위 상태는 미검증이 맞다. 절별 상태는 이 표가 말한다.

| 무엇 | 상태 | 근거 |
|---|---|---|
| **λ₁ exact** — `shortest_translation` 을 ASE `minkowski_reduce` 래퍼로 교체 | ✅ 완료 | codex 반례 2건이 brute force 와 **정확히 일치**: 0.401995 (n=(−1,4,0)) · 0.020000 (n=(−1,20,0)) |
| **`--selftest` 신설** (`build_neb_inputs.py`) — 22 케이스, 예외 요구 4건 + 유한-R 반례 2건 | ✅ 22/22 | 옛 구현(고정 R / R 배증)은 `codex3_earlystop` 에서 죽는다 |
| **webapp 게이트 오역** — `blocking_gate` 존재만으로 "게이트 미통과" 를 찍던 것을 `gate_outcome` 별 문구로 분기 (`_gate_prefix`, 사본 2곳 → 함수 1개) | ✅ 완료 | 화면이 이제 "게이트 미평가(실패 판정이 아니다)" 를 찍는다 |
| **b2o3 registry 정정** — 옛 β 판정 `retracted + diagnostic_unbound` 보존 / 새 판정 `not_assessed(required_artifact_set_incomplete)` / single-seed 과교정 철회 | ✅ 완료 | `validate_canonical` 28/28 · `kb lint` 0 · `convention_check` 0 |
| **선행 로스터 selftest** msd_diffusive_check · collect_neb · bench_against_dft · uma_engine_probe · extract_figures | ✅ 전부 PASS | — |

### A-2. codex **동결감사** 로 추가로 닫은 것

| 무엇 | 상태 | 근거 |
|---|---|---|
| **λ₁ unimodular 검사 실수리** — `abs(round(det))==1` 은 round 를 먼저 해 정수성 검사가 사라졌다 (det=1.4·0.6 통과, 실측). 정수성과 \|det\| 를 따로 + `rcell = op @ cell` 계약 검증 | ✅ | selftest 22→**38** |
| **scout 에 `lambda1_A`** — 판정에 쓰는 정본 지표가 산출물에 없고 면 높이만 있었다 | ✅ | — |
| **release 생성기의 옛 주장 제거** — `build_final_conductivity.py` 가 매 실행마다 "EQUIVALENT transport"/"PRESERVED" 를 되살렸다 | ✅ | 재생성 후 수치 동일 확인 |
| **webapp 단일 resolver** — `canonical.gate_outcome / gate_blocks_canonical / gate_prefix`. 소비처 5곳 이관 | ✅ | 86 passed |
| **홈 카드 자기모순** — b2o3 를 미평가로 내리자 묶음에 modelc 만 남아 "최저" 라 쓰면서 아래에선 "구분 안 됨" 이라 했다 → **순위 보류** | ✅ | 기존 테스트가 회귀를 잡았다 |
| **hash-bound carry 실구현** — `collect_neb` 이 `protocol_hash` 를 회수만 하고 이월 검사에 안 썼다 (F8 이 살아 있었다) | ✅ | selftest +6 (음성 4) |
| **protocol hash 에 ASE 판·method ID + payload 분리** | ✅ | `protocol_diff` 가 바뀐 키를 지목 |
| **assessment sidecar** — `db/governance/assessments.json`, claim 에는 `required_assessment_refs` 만 | ✅ | 옛/새 판정 **병존** |
| **판례 원장 core 5** — `db/governance/decisions.json`, 전부 `ratification.state=proposed` | ✅ | dangling edge 검사 통과 |

**아직 안 닫힌 P0**: `validate_canonical` 이 새 필드를 읽지 않는다 → 이번 정정을 스스로
검증하지 못한다 (webapp 테스트는 잡지만 db 도구는 못 잡는다). Phase A 의 첫 작업.

## 0. 왜 — 실패 사례 9건이 요구 조건이다

| # | 실패 (실측) | 왜 문서 규칙으로 못 막았나 | → 요구 조건 |
|---|---|---|---|
| F1 | **철회된 지표 재사용** — 08-16 λ₁ 확정을 08-19 새 도구가 면 높이로 되돌림 | 결정이 kb 산문에만 있었다 | **R1** 기계 조회 + 도구의 의존 **선언** |
| F2 | **화면 ≠ db** — `collect_neb` 결산표 "✅ 인용 가능" vs 저장값 `citable:false` | 지위 계산이 도구마다 사본, 출력 순서가 틀림 | **R2** 지위는 **한 평가기**만 계산 |
| F3 | **배제된 가설 재론** — COM 표류 가설 재논증 | 닫힌 질문이 보고서 한 줄 | **R3** 닫힌 가설도 레지스트리 항목 |
| F4 | **계보 오류** — β 를 잰 궤적(`b2o3_full`)과 Ea 0.199 를 만든 궤적(3-seed reseed)이 다른데 연결 | 값 출처가 산문뿐 | **R4** 기계 계보 + 값-바인딩 |
| F5 | **처방이 진단을 앞섬** — 부피 +32.7 % 원인이 이미 닫혔는데 stress 파인튜닝 제안 | 닫힌 결론이 산문 | **R3'** 닫힌 결론 조회 = 사다리 0단계 |
| F6 | **fallback 재구현** — λ₁ import 실패 시 재구현 | 관례였지 검사가 아님 | **R5** canonical 단일 출처 + hard fail |
| F7 | **selftest 실패 채로 푸시 2회** | 기억으로 돌리는 절차 | **R6** 푸시/생성 경로 자동 관문 |
| F8 | **사람 판정 이월 오염 위험** | 이월 키에 정체성 없음 | **R7** 해시 일치에서만 승계 |
| **F9** | **게이트 입력이 미보존인데 "나중에 재검사" 로 적어둠** — `run_highT_reseed.sh` 가 `--save_traj` 를 안 넘겨 **high-T 6런(800·1000 K × s2/s3/s4)의 궤적이 없다** | ⚠ **정보는 있었다** — `run_arrhenius_6pt.sh` L57–59 가 *"프레임을 디스크에 안 남겨(--save_traj 없음) 소급 계산도 불가"* 라고 **이미 적어뒀고**, 그 러너는 L183 에서 고쳐졌다. **highT_reseed 만 안 고쳐졌다** | **R8** 산출물이 **소급 가능성**을 스스로 도장 (`retro_gate_possible`). 입력 부재 게이트는 `not_assessed(required_artifact_set_incomplete)` — `pending` 이 아니다 |
| **F10** | **범위 과잉 일반화 + 과교정** (v2 자체의 실패) — "최종 9개 궤적 부재" 로 적었으나 실제는 **high-T 6/6 미보존**이고 600 K 3런은 PMF 가 소비한 기록이 있다. 그 잘못된 사유를 **single-seed 항목에도 복사**했다 | 정정을 급히 쓸 때 **범위를 재확인하는 관문이 없다.** 정정도 산출물인데 계보 검사를 안 받는다 | **R9** 정정은 새 decision kind 가 아니라 **assessment correction event** 다 — `supersedes_assessment_id` + `scope` + 근거를 가진 append-only 레코드이고, 다른 항목에 사유를 복사하지 않는다 (codex 3차 확정) |

⚠ **공통 패턴 (F1–F10, 예외 없음)**: 전부 **"정보가 있는데 기계 경로에 없어서"** 다.
v2 는 F9 를 *"정보가 정말 없는 유일한 예외"* 로 적었는데 **그것도 틀렸다** — 궤적 파일은
없지만 **그 결함의 기록은 repo 안에 주석으로 있었고**, 한 러너에만 반영됐다.
처방은 하나로 돌아온다: **"적힌 것을 실행 경로에 올리자."**

## 1. codex 2·3차 P0 반영 원장

| P0 | 지적 | 판정 | 반영 |
|---|---|---|---|
| 2-1 | 5단 사다리가 개념을 뭉갬 | 수용 | §3-1 |
| 2-2 | scope 당 active 1개는 틀림 → slot + applicability | 수용 | §3-2 |
| 2-3 | codex+self 는 ratification 아님 · `unratified` 자유문자열은 fail-open | 수용 | §3-3 |
| 2-4 | gate 결과를 canonical value 에 되쓰지 말 것 | 수용 | §5 |
| 2-5 | method manifest 필요 · SHA-1/짧은 commit 금지 | 수용 | §6 |
| 2-6 | λ₁ 구현 부적격 | 수용 | §7 — **코드 완료** |
| 2-7 | require 자진신고로는 누락을 못 잡음 | 수용 | §8 |
| **3-1** | **F9 범위 오류** — 9/9 아니라 high-T 6/9 미보존. 600 K 는 생성돼 PMF 가 소비 | **수용 — 우리가 틀렸다** | §0 F9/F10 · §5-2 |
| **3-2** | **옛 판정과 새 판정은 대체가 아니라 병존** (`retracted+diagnostic_unbound` / `not_assessed`) | **수용** | §5-1 |
| **3-3** | **registry/UI 가 `not_assessed` 를 fail 로 읽는다** | **수용 — 코드 완료** | §A |
| **3-4** | single-seed 까지 끊은 건 과교정 | **수용 — 철회 완료** | §A · F10 |
| **3-5** | `\|nᵢ\|≤2` 는 certificate 가 아니다 (상자 밖 배제 불가) | **수용 — 우리가 틀렸다** | §7 |
| **3-6** | `build_final_conductivity.py` 가 D 를 하드코딩 → `wired` 아님 | **수용 · 확인** (`json.load`/`read_text` 부재 확인) | §5-2 |

**우리가 codex 스냅숏보다 정확히 확인한 것 3건:**

1. **600 K 궤적은 3개가 아니라 4개가 소비됐다.** `b2o3_pmf_*_T600_origin.csv` 헤더:
   *"1900 frames each, 58 Li / 128 atoms … Density integral 232.0 = 58 Li × 4 seeds"* /
   *"4 trajectory/ies summed"*. 3-seed reseed(s2/s3/s4) + 기존 1런으로 읽힌다.
2. **두 세트는 서버가 다르다.** `run_arrhenius_6pt.sh` L20–23:
   600 K = **gabia** `/data/work/b2o3md/runs/b2o3_600_reseed` (200 ps) ·
   high-T = **kgy** `~/work/runs/highT_reseed/b2o3` (100 ps). 현존 확인이 두 서버에 걸친다.
3. **F9 는 "몰랐던 결함" 이 아니다** (위 §0). 같은 파일이 결함을 적고 자기만 고쳤다 —
   이게 F9 를 F1–F8 과 같은 패턴으로 되돌린다.

## 2. 설계 원칙

1. **기존 인프라의 확장.** `canonical_registry`(값) · `convention_check`(수치 상수) ·
   `kb_wiki lint`(문서) 는 enforcement 백엔드로 재배치. *카탈로그 1 + 백엔드 4*.
2. **레지스트리 = 판례집.** 확정된 결정만. 강등 사유는 자유 문자열이 아니라 **등록된
   proposed decision ID**.
3. **fail-closed.** 못 읽으면 계산하지 않는다. unknown ID 실패. canonical import 실패 시
   fallback 금지. **탐색 한도 초과는 경고 후 계속이 아니라 실패.**
4. **지위 기반 래칫** (날짜 일괄 전환 폐기). canonical·approved·ranking 값은 기존 항목도
   즉시 차단, display-only legacy 만 debt allowlist — **만료일·사유 필수**.
5. **양방향 대조.** 레지스트리가 `applies_to` 로 요구 집합을 역산하고 도구 선언과 다르면 실패.
6. **사람 승인이 상한, 기계는 하향만.** 자동 승격 경로 없음.
7. **저장된 지위는 "생성 당시" 기록.** 소비자는 **현재 레지스트리로 재평가**한다.
8. **⭐ 신설: 정정도 산출물이다** (R9/F10). 철회·정정은 범위·근거·해시가 붙은 assessment
   레코드로 남기고, **다른 항목에 사유를 복사하지 않는다.**

## 3. ① 판례집 — 스키마

### 3-1. 상태 어휘 — **엔터티별로** 나눈다 (codex R4)

v2 는 7축을 한 `status` 블록에 몰아넣었다. codex 지적: 축의 **소유자**가 다르므로 붙는
자리도 달라야 하고, 파생값을 저장하면 **stale cache** 가 생긴다.

| 엔터티 | 저장하는 축 | 누가 쓰나 |
|---|---|---|
| **Decision** | `decision_state` (proposed/active/superseded/retracted) · `ratification` | 사람 |
| **Artifact** | `artifact_integrity` (valid/incomplete/invalid) · `retro_gate_possible` | 기계(파일·해시) |
| **Lineage** | `lineage_binding` (missing/prose_only/unwired/wired/verified) · `numeric_reproduction` (none/approximate/exact) · `evidence_status` | 기계 + 사람(evidence 확정) |
| **Assessment** | `gate_outcome` (not_assessed/pass/fail/inapplicable) + `reason` | 기계(sidecar) |
| **Evaluator** | ⛔ **저장 안 함** — `release_status` · `allowed_uses` 는 **query-time 파생** | — |

- 사람이 실제로 쓰는 축은 **3개**: `decision_state` · `ratification` · `evidence_status`.
  (v2 는 "2개" 라고 썼는데 `evidence_status` 도 사람 몫이라 틀렸다 — codex R4 지적 수용.)
- ⛔ **v2.1 정정 (codex R4)**: `numerically_reproducible` 을 `lineage_status` enum 에 넣은 것은
  **5단 사다리를 폐기해 놓고 같은 자리에 사다리를 다시 만든 것**이었다. 재현 가능성과 배선
  여부는 **독립**이므로 두 축으로 쪼갠다: `lineage_binding: unwired` + `numeric_reproduction: exact`.
  b2o3 Ea 가 정확히 그 조합이다 — 9개 D 에서 값은 정확히 재현되는데
  `build_final_conductivity.py` 가 D 를 하드코딩해 기계 계보는 배선돼 있지 않다.
  ⚠ 그리고 L1 에 있는 것은 per-seed **D** 이지 per-seed **MSD** 가 아니다 — 골격 게이트는
  궤적을 요구하므로 L1 만으로는 닫히지 않는다.
- UI 배지는 `evaluate()` 반환값에서만 나온다. 저장된 배지를 읽지 않는다.

**b2o3 Ea 가 새 어휘로** (v1 사다리로는 표현 불가능했던 상태):

```jsonc
artifact_integrity: "incomplete"                 // high-T 6런 궤적 미보존
lineage_binding:    "unwired"                    // build_final_conductivity 가 D 를 하드코딩
numeric_reproduction: "exact"                  // 9개 D 에서 Ea 0.199438 정확 재현 (독립 축)
evidence_status:    "validated"                  // 3-seed x 3-T, 증거는 성숙
gate_outcome:       "not_assessed"               // reason: required_artifact_set_incomplete
→ (파생) release_status "provisional" · allowed_uses ["public_audit","comparison"]
```

### 3-2. slot / applies_to (P0 2-2)

`scope` 는 검색용 namespace. 유일성은 **slot + 겹치는 applicability** 에서만 검사한다
(`md` scope 에 창·시드정책·단일시드금지·배제가설이 **동시에** 산다).
부모/자식 scope 는 **누적 적용**. ⛔ "더 구체적인 것이 암묵적으로 이긴다" 규칙은 두지 않는다.

### 3-3. ratification (P0 2-3)

과학 결과나 허용 문장을 바꾸는 `metric·method·gate·prohibition·hypothesis` 는 **전부
human scientific owner 승인 필수**. agent 는 제안·기술검증까지.

```jsonc
"proposed_by": [{"actor_type":"agent","actor_id":"claude"}],
"reviewed_by": [{"actor_type":"agent","actor_id":"codex","verdict":"conditional_go"}],
"ratification": {"state":"ratified","actor_id":"yonghoon","role":"scientific_owner",
  "timestamp":"…Z","commit":"<full 40-hex>","evidence_digest":"sha256:…",
  "max_release_status":"approved","max_allowed_uses":["…"]}
```

⛔ `unratified: ["자유 문자열"]` 폐지 → 등록된 **proposed decision ID** 만.

### 3-4. 결정 레코드에서의 분리

`statement`(정의) ↔ `method_ref`(구현 지문) ↔ `enforcement`(강제 수단) ↔ 경험적 문턱
(**레지스트리 밖**, 별도 gate 결정). v2 에서 이미 분리했고 유지 — λ₁ 이 그 실례다
(**정의는 옳고 구현은 부적격**이었던 상태를 표현할 수 있어야 한다).

## 4. ② 평가기

```python
evaluate(subject_ref, use_case, claim_type) -> Verdict
# use_case  : public_audit | comparison | absolute_claim | ranking | manuscript
# claim_type: mechanism | magnitude | ordering | existence
```

- 같은 값이 use_case 별로 다른 답: b2o3 Ea 는 `comparison` 허용 / `ranking`·`mechanism` 거부.
- **자동 승격 없음** — `ratification.max_release_status` 를 상한으로 하향만.
- 소비처 전부 이 함수만: `collect_neb` · `webapp/data.py` · `validate_canonical` ·
  figure/manuscript 생성 스크립트.
- `tools/policy.py` <!-- lint-skip-path: 설계 단계 — 생성 예정 --> 는 CLI facade,
  schema validator · 순수 evaluator · lineage 는 내부 모듈로 분리.

### 4-1. F2 수리 — collect_neb 순서

```
지금:   회수 → citable 계산 → 결산표 출력 → 사람판정 이월+하향 → 저장
수리:   회수 → 이월(해시 검증) → evaluate() → 결산표 출력 → 원자적 저장(tmp→os.replace)
```
출력 문구는 `evaluate()` 의 `badge` 만. ⛔ `run_sei_neb.sh:267` 의 `|| true` 제거 (§8-2).

## 5. ③ 계보 — 상태를 **세 갈래로** (codex R2)

### 5-1. 옛 판정과 새 판정은 병존한다

```
raw trajectory integrity  : incomplete (high-T 6/6 미보존 · 600 K 4궤적 소비기록 있음, 현존 미확인)
Ea lineage                : numerically_reproducible (wired 아님 — D 하드코딩)
framework assessment      :
    ├─ 옛: retracted + diagnostic_unbound     (b2o3_full 의 β 0.59/0.63 — 다른 run family)
    └─ 새: not_assessed(required_artifact_set_incomplete)
```

⛔ **`diagnostic_unbound` 를 `not_assessed` 로 대체하지 않는다.** 전자는 *철회된 옛 β
판정의 바인딩 상태*, 후자는 *새 판정의 결과*다. 둘 다 보존해야 감사가 성립한다
(v2 가 전자를 후자로 덮으려 한 것이 오류).

### 5-2. b2o3 계보 DAG (실제 데이터 기준)

```
L0  raw trajectories   600 K  4 소비기록(gabia, 현존 미확인)  ·  800/1000 K  0/6 (kgy, 미보존)
L1  per-run D          ✅ b2o3_vs_lpscl16_conductivity.csv  ⚠ per-run **MSD 는 없다**
L2  T별 3-seed 집계    ✅ 같은 CSV
L3  Arrhenius fit      ✅ Ea 0.199438 · D0 4.62463e-04 · σ_Ea 0.034306 (D 9개에서 정확히 재현)
L4  Ea claim           ✅ canonical entry
```

⚠ **L1 에 있는 것은 per-seed D 이지 per-seed MSD 가 아니다** (codex). 골격 게이트는
MSD/궤적을 요구하므로 **L1 만으로는 닫히지 않는다** — 이것이 "재실행 없이 게이트가 안 닫힌다"
의 정확한 이유다. 재실행 범위는 **6런**(800/1000 K × 3시드), 9런이 아니다.

각 노드 해시: `run_id` · `protocol_hash` · `input_hash` · `artifact_hash` · `endpoint_hash`.

### 5-3. assessment sidecar (append-only)

게이트 결과는 canonical value 에 **되쓰지 않고** sidecar 로만 존재하며, canonical entry 는
`required_assessment_ref` 로 **참조**한다.

```
canonical claim
  └─ required_assessment_ref
       ├─ retracted assessment  : 옛 β, diagnostic_unbound
       └─ current assessment    : not_assessed(required_artifact_set_incomplete)
```

### 5-4. 사람 판정 이월 (F8/R7)

```
이월 허용 ⟺ (root, tag) 동일 AND protocol_hash 동일 (input/endpoint 는 지문 payload 안)
불일치·한쪽 부재: "이월 거부 — 5f78… → a3c2… (바뀐 것: kpts [3,3,3] → [5,5,5])" + carry_refused
```
⛔ **구현하며 바꾼 것 (2026-08-20)**: 거부를 *"사람 판정 필드를 비운다"* 로 끝내면 안 된다.
사람이 내린 **하향까지 같이 사라져** 자동 판정이 `citable=True` 로 올려버린다 — 08-16
"0.229 가 db 에서 사라진 사고" 가 방향만 바꿔 재발한다. 거부 시 **보수적으로 잠근다**:
`citable=False` + `carry_refused{why, withheld_fields}`. fail-closed 는 "정보를 지운다" 가
아니라 **"안전한 쪽으로 떨어뜨린다"** 여야 한다.

## 6. method manifest (P0 2-5)

```
db/governance/decisions.json    판례            <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
db/governance/methods.json      방법 (immutable, versioned)   <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
db/governance/assessments.json  게이트 판정 sidecar (append-only)  <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
db/governance/schemas/          JSON Schema     <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
```

산출물 도장 필수 항목: versioned `method_id` + `method_digest` · `decision_digests` ·
`registry_digest` · **full 40-hex commit** · `git_dirty` + dirty diff hash ·
입력 **SHA-256** · UTC timestamp · `schema_version` · `retro_gate_possible` ·
`release_status_at_stamp`(⚠ 생성 당시 기록일 뿐 — 소비 시점에 재평가).

λ₁ 매니페스트에는 **ASE 버전과 tolerance** 를 기록한다 (구현이 외부 라이브러리에 있으므로).

## 7. λ₁ — exact (완료). `|nᵢ|≤2` 는 certificate 가 아니다

**codex 3차가 맞다.** 유한 상자 전수검사는 **상자 밖 최단벡터를 배제하지 못하므로**
독립 certificate 가 될 수 없다. 축약이 Minkowski 기약임을 가정해야 상자 밖이 배제되는데,
그 가정 자체가 증명 대상이면 순환이다.

**채택한 구현** — 새 알고리즘을 쓰지 않고 **ASE 정본을 얇게 감싼다**:

```python
from ase.geometry import minkowski_reduce, is_minkowski_reduced
rcell, op = minkowski_reduce(cell)      # op 는 unimodular, rcell = op @ cell
assert is_minkowski_reduced(rcell)
λ1 = norm(rcell[0]);  n = op[0]         # 3D 기약기저의 첫 벡터가 정의상 최단
```

근거: Nguyen–Stehlé 2004 — dim ≤ 4 에서 greedy 가 Minkowski-reduced 를 다항시간에 준다
(세 번째 벡터를 앞 2D 격자에 대해 exact CVP 로 축약하는 단계 포함). canonical 구현을
복제하지 않는다는 규율이 **외부 라이브러리에도 적용**된다 — 우리가 다시 쓰지 않는다.

**검증 (실측)** — brute force 와 정확히 일치:

| 셀 | 옛 구현 | exact | n |
|---|---|---|---|
| a=(10,0,0) b=(2.49,0.1,0) c=(0,0,10) | R=3 → 2.492 | **0.401995** | (−1,4,0) |
| a=(10,0,0) b=(0.5,0.001,0) c=(0,0,10) | R=3=R=6 → 0.500001 **조기종료** | **0.020000** | (−1,20,0) |

부수 규율: 준특이 셀(`|det|/(|a||b||c|) < 1e-8`)은 **hard fail** · import 실패는 **즉사**
(fallback 재구현 금지) · 문턱 비교 전 **반올림 금지**(해시 payload 의 3자리 반올림은 별개 —
지문 안정화 목적이고 게이트는 원값을 쓴다).

`--selftest` 22 케이스: 양성 3 · 유한-R 반례 2 · 면높이 판정반전 2 · 정수계수/unimodular
불변 4 · **예외 요구 4**(준특이·영벡터·NaN·잘못된 shape) · 해시 민감도 5.

## 8. consumer 자동 적용 (P0 2-7)

### 8-1. 양방향 대조

```python
require_for(__file__, operation, context) -> RequiredSet   # 레지스트리가 applies_to 로 역산
declared = policy.require([...])
if declared != required: hard fail   # "선언 누락: D-… / 불필요 선언: D-…"
```
CLI 가 `PolicyContext` 를 만들고 **산출물 writer / public boundary** 에서 재검사.
⛔ 순수 helper import 에 부작용 금지.

### 8-2. shell

- 정책 대상 명령에 `|| true` 금지 — 실측 위반 1건 `tools/sei/run_sei_neb.sh:267`.
  같은 파일 L21 `set -uo pipefail` → `set -euo pipefail`.
- ⚠ 일괄 금지 아님: `tools/` 의 `|| true` 나머지 28건은 `unset LD_LIBRARY_PATH` /
  `conda activate` 로 **무해**. tombstone 은 **정책 대상 명령 목록**에만.

### 8-3. 관문 위치

CI 는 **안전망**, 진짜 관문은 **생성 단계** — webapp 빌드 · figure 생성 ·
manuscript/release 산출 스크립트의 첫 동작이 `preflight --hard`.

## 9. 시드 판정

### 9-1. MVP core 4 (acceptance 는 이 4개로만 센다 — codex R3)

| id | kind | 내용 |
|---|---|---|
| `source-authority` | policy | canonical DB/manifest 가 log·화면보다 우선 |
| `hash-bound-carry` | policy | 해시 불일치 시 사람 판정 승계 금지 |
| `no-fallback` | policy | canonical 구현 import 실패 시 재구현 금지 |
| `defect-cell-metric` | metric | λ₁ **정의**만 (구현 = §7 매니페스트, 10 Å 문턱은 별건) |
| `no-retro-gate-without-artifact` | policy | 게이트 입력 부재 → `not_assessed`, `pending` 아님 (F9) |

⭐ **core 4 → core 5** (codex 동결감사 수용) — b2o3 가 vertical slice 이고 그 slice 가
실증하는 것이 바로 다섯 번째 결정이므로 core 에 넣는 게 정직하다.

`gap-eigenvalue` · `uma-li3n-ban` 2건은 **read-only schema fixture** 로만 동봉한다
(kind 별 스키마 동작 확인용). ⚠ consumer/preflight 에 연결하지 않으므로
**end-to-end enforcement 검증에는 안 센다** — codex R3 수용.

⭐ `supersedes` 대상인 옛 결정(`D-2026-08-16-face-height-gate`)도 **실제 node 로 등록**했다
— 첫 원장부터 dangling edge 가 생기면 그래프가 거짓말을 시작한다 (codex 3차).
전부 `ratification.state = proposed` 다: **agent 는 과학적 승격을 못 한다**(P0-3).
`decision_state=active` 로 올리려면 human scientific owner 승인이 필요하고,
그 전까지 이 결정들을 근거로 만든 산출물은 `diagnostic` 으로 강등된다.

### 9-2. 확대 대기 — entry 수리 7건

`neb-ci-order`(QE neb.x 범위) · `neb-mlip-absolute`(현 UMA scout·미검증 chemistry 범위) ·
`msd-window`(LPSCl-family UMA MD protocol 범위) · `seed-policy`(최소 시드 / 정지규칙 /
optional stopping 금지를 **3개로 분리**) · `elastic-relaxed-ion`(argyrodite quasi-static
비교 범위) · `single-seed-sigma`(1.33× artifact 철회와 일반 claim policy 분리).

### 9-3. 재승인 필요 3건

- `beta-estimator-mto` — estimator 와 문턱 **둘 다** 재승인.
- `com-drift-closed` — ⭐ **좁힌다**: "특정 `fixcm=True` run family 에서 **총 COM 표류**
  배제". **species-relative drift 가설은 open 으로 남긴다.**
  ⚠ 2026-08-20 재실행 로그에서 확인한 추가 약화 요인 — **ASE 자신이 그 근거를 경고한다**:
  *"The implementation of `fixcm=True` in `Langevin` does not strictly sample the correct
  NVT distributions … `fixcm` is deprecated since ASE 3.28.0"*. COM 표류 억제 자체는
  여전히 하지만, 우리 배제 근거가 "ASE 가 fixcm 으로 닫아준다" 였으므로 **근거가 두
  방향에서 약해진다**(codex R5 의 species-relative + ASE 의 분포 정확도). 재승인 시
  이 문구를 근거 목록에 포함할 것.
- `monroe-newman-closed` — "sole design criterion 으로 쓰지 않음" 으로 축소 + 사람 승인.

### 9-4. species-relative drift는 β 게이트가 대신할 수 없다 (codex R5)

**동의.** β 는 원소별 MSD 의 크기와 확산 **형태**만 본다 — coherent drift 와 internal
diffusion 을 **분해하지 않는다**. 별도 diagnostic 이 필요하다:

```
species mean displacement · species-mean 제거 후 internal MSD · coherent species drift
Li–framework relative displacement · PS4 골격 / cage anion 분리
```

⚠ **문턱은 승인하지 않는다 — diagnostic-only.** (이것이 v2 §9-3 에서 우리가
"골격 게이트가 그 역할" 이라고 쓴 것의 정정이다.)

### 9-5. 빠진 시드

canonical DB/manifest 우선 · 해시 불일치 승계 금지 · fallback 금지 · exact lineage 없이
값·게이트 결합 금지 · canonical softBV 와 cascade legacy Adams proxy 교차비교 금지 ·
**`no-retro-gate-without-artifact`**(F9) · **`retraction-is-an-assessment`**(F10/R9).
⭐ `supersedes` 대상 옛 결정도 **실제 node 로 등록**(dangling edge 금지, graph validator).

## 10. MVP 실행 순서

| Phase | 내용 | 비용 | acceptance |
|---|---|---|---|
| **A** | 다축 schema(엔터티별) + JSON Schema validator + graph validator + 순수 evaluator + human ratification · **`validate_canonical` 이 새 필드를 읽게** | 1.0 d | 스키마 픽스처 · 이번 b2o3 정정이 검증됨 |
| **B** | ~~exact λ₁~~ **완료** → 남은 것: λ₁ method manifest 등록 + ASE 버전 기록 | 0.2 d | selftest 22/22 (완료) |
| **C** | b2o3 L1–L4 배선 + assessment sidecar(옛/새 **병존**) + `--for` 거부 경로 | 0.5 d | `not_assessed` 가 정확히 그렇게 표시 |
| **D** | `collect_neb` + `webapp` 이 **같은 evaluator** 사용 + 원자적 저장 + `run_sei_neb.sh` `\|\| true` 제거 | 1.0 d | F2 · stale-carry 골든 픽스처 |
| **E** | 빠른 core CI **매 push (Windows + Linux)** + 무거운 suite weekly + 생성단계 preflight hard gate | 0.5 d | Q4 |
| — | §9-2/9-3 확대는 slice 통과 후 **별건** | — | 사람 승인 |

**≈ 3.2 d** (core 4결정 · 도구 2곳 이관). λ₁ 이 선반영돼 B 가 줄었다.

## 11. ⚠ 한계·반론 (지우지 말 것)

1. **우회를 못 막는다.** 목표는 강제가 아니라 **비용 역전**.
2. **레지스트리가 단일 실패점**이고, **내용이 틀리면 오류를 더 강하게 전파한다** —
   codex 가 12시드 즉시 도입을 막은 이유. MVP core 4 로 줄인 근거.
3. **다축 상태는 실무 부담이 크다.** 사람이 쓰는 축이 3개로 늘었다(2개가 아니었다).
   첫 확대 시점에 "축이 기본값으로 썩는 비율" 을 실측해야 한다.
4. **tombstone grep 은 원리적으로 불완전.**
5. **산문 드리프트는 남는다** — 승격된 것만 보호된다.
6. **브랜치 밖은 관할 밖** (DEM 세션 · gabia 로컬 상태).
7. **F9 는 과거를 복구하지 못한다.** b2o3 골격 게이트는 **high-T 6런 재실행 없이는
   영원히 `not_assessed`** 다. 시스템이 하는 일은 그 사실이 `pending` 으로 위장되지
   않게 하는 것뿐이다.
8. **`evidence_digest` 는 사람이 그 근거를 실제로 읽었음을 보증하지 않는다.**
9. **⭐ v2 자체가 F10 을 만들었다.** 정정을 급히 쓰면서 범위를 과잉 일반화하고 다른
   항목에 복사했다. **이 설계가 만들려는 관문이 없으면 정정조차 오염된다** —
   R9 는 그 자기지시적 교훈이다.

## 12. 원고에 지금 쓸 수 있는 최대 문장 (codex 권고 수용)

> 동일한 집계 규약에서 Li tracer Ea 는 0.199 ± 0.034 와 0.197 ± 0.032 eV 로 구분되지
> 않았다. 다만 B₂O₃ high-temperature raw trajectories 가 보존되지 않아 비-Li 구조 상태는
> 검증하지 못했다.

⛔ `transport preserved/equivalent` · ranking · mechanism 까지 말하려면 **high-T 6런
재실행**이 필요하다. 선결: **600 K 세(네) 궤적의 현존·해시 확인** (gabia).

## 13. codex 4차에 묻는 것

| # | 질문 | 우리 입장 |
|---|---|---|
| S1 | `lineage_status` 에 `numerically_reproducible` 등급을 신설한 것이 맞는가, 아니면 `prose_only` 의 하위 속성인가 | 별도 등급 — 재현 가능성과 배선 여부는 독립이다 |
| S2 | F10(정정의 과교정)을 R9 로 승격한 것 — 판례 kind 로 `retraction` 을 따로 둘 것인가 | assessment 의 한 종류로 본다 |
| S3 | 600 K 궤적이 **4개**(3-seed + 기존 1런)라면 집계 규약이 3-seed 인데 PMF 는 4개를 썼다 — 이 불일치가 별도 결정 대상인가 | PMF 는 dF_perc 용이라 다른 use_case 로 본다. 확인 필요 |
| S4 | §9-4 species-relative diagnostic 을 **문턱 없이** 도입하는 절차 — diagnostic-only 산출물도 도장을 받는가 | 받는다 (`release_status: diagnostic`) |
| S5 | MVP acceptance 를 core 4 로 세면 `no-retro-gate-without-artifact`(F9)는 어디에 드는가 — core 인가 확대인가 | b2o3 slice 가 그것을 실증하므로 core 편입을 제안 |

## 관련

- codex 2차/3차 리뷰 원장: 이 카드 §1
- 발단: `kb/reviews/codex_B_neb_md_tools_2026_08_20.md` §5 B-R11 (Q5)
- F9/F10 실측 근거: `tools/modelc_v3/run_highT_reseed.sh` L32–39 ·
  `tools/modelc_v3/disorder_ensemble_diffusion.py` L238–241, L300 ·
  `tools/ionic/run_arrhenius_6pt.sh` L20–23, L57–59, L183 ·
  `db/properties/b2o3_pmf_profile_T600_origin.csv` (헤더) ·
  `db/properties/b2o3_vs_lpscl16_conductivity.csv` (PER-SEED D 9개) ·
  `tools/ionic/build_final_conductivity.py` (D 하드코딩)
- λ₁ exact: `tools/sei/build_neb_inputs.py::shortest_translation_full` (`--selftest`)
- 기존 인프라: `db/properties/canonical_registry.json` · `tools/convention_check.py` ·
  `tools/db/validate_canonical.py` · `tools/kb_wiki.py` · `webapp/data.py::_gate_prefix`
