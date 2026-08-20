---
title: "결정 레지스트리 설계 v2 — codex 2차 P0 반영 (MVP vertical slice)"
date: 2026-08-20
updated: 2026-08-20
tags: [policy, registry, ci, provenance, lineage, tombstone, codex, infrastructure, svp]
status: 설계 v2 — codex 2차 P0 반영 완료 (구현 착수 가능 범위 = MVP 4결정)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: max
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 결정 레지스트리 설계 v2

> **판정 이력**: v1(2026-08-20 오전) → codex 2차 **조건부 GO** — 아키텍처 4축은 GO,
> **현재 스키마·12시드 즉시 구현은 NO-GO**. 이 v2 는 P0 7건을 전부 반영하고,
> 범위를 **MVP 4결정 vertical slice** 로 줄인 판이다.
>
> **한 줄**: 규약 역행을 막는 것은 4축(판례집 · 계보 · 단일 평가기 · 래칫)이 맞다.
> 단 지금 구현하면 **상태 혼합**과 **잘못 넓힌 결정**을 중앙 시스템이 *더 강하게* 전파한다
> — codex 2차의 핵심 지적이고, 우리가 v1 에서 실제로 틀린 부분이다.

## 0. 왜 — 실패 사례 9건이 요구 조건이다

전부 2026-08 실측. **F9 는 이 v2 를 쓰면서 오늘 새로 확인한 것**이다.

| # | 실패 (실측) | 왜 문서 규칙으로 못 막았나 | → 요구 조건 |
|---|---|---|---|
| F1 | **철회된 지표 재사용** — 08-16 λ₁ 확정을 08-19 새 도구가 면 높이로 되돌림 | 결정이 kb 산문에만 있었다 | **R1** 기계 조회 + 도구의 의존 **선언** |
| F2 | **화면 ≠ db** — `collect_neb` 결산표 "✅ 인용 가능" vs 저장값 `citable:false`. 리뷰 카드 3곳에 오기 전파 | 지위 계산이 도구마다 사본, 출력 순서가 틀림 | **R2** 지위는 **한 평가기**만 계산 |
| F3 | **배제된 가설 재론** — COM 표류 가설 재논증. 1저자가 끊음 | 닫힌 질문이 보고서 한 줄이라 검색 전에 안 보임 | **R3** 닫힌 가설도 레지스트리 항목 |
| F4 | **계보 오류** — β 를 잰 궤적(`b2o3_full`, single-seed legacy)과 Ea 0.199 를 만든 궤적(3-seed reseed)이 **다른데** 연결 | 값 출처가 산문뿐 | **R4** 기계 계보 + 값-바인딩 |
| F5 | **처방이 진단을 앞섬** — 부피 +32.7 % 원인이 fmax 사다리로 닫혔는데 stress 파인튜닝 제안 | 닫힌 결론이 산문이라 갱신을 강제 못 함 | **R3'** 닫힌 결론 조회가 사다리 **0단계** |
| F6 | **fallback 재구현** — λ₁ import 실패 시 `except BaseException` 으로 재구현 | "복사 금지" 가 관례였지 검사가 아님 | **R5** canonical 단일 출처 + fallback hard fail |
| F7 | **selftest 실패 채로 푸시 2회** | 기억으로 돌리는 절차는 두 번 빠졌다 | **R6** 푸시/생성 경로에 자동 관문 |
| F8 | **사람 판정 이월 오염 위험** — `<root>/<tag>` 만으로 이월 | 이월 키에 정체성 없음 | **R7** 동일 protocol+input 해시에서만 승계 |
| **F9** | **⚠ 소급 게이트가 원리적으로 불가능한데 "나중에 재검사" 로 적어둠** — `run_highT_reseed.sh` 가 `--save_traj` 를 **안 넘긴다**(실측, L32–39). `disorder_ensemble_diffusion.py:238` 이 그 플래그로 `traj.xyz` 쓰기를 감싼다 → **최종 9개 궤적이 디스크에 없다.** 그런데 codex_B §0 과 canonical_registry 의 `blocking_gate` 는 "최종 궤적에 같은 검사를 돌린다" 를 후속 작업으로 기록 | 산출물이 **무엇을 잃었는지**를 스스로 기록하지 않는다. msd.json 은 남고 궤적만 없는데, 그 사실이 어디에도 기계 가독 형태로 없다 | **R8** 산출물은 **소급 가능성**을 스스로 도장한다 (`retro_gate_possible:false`). 없는 입력에 걸린 게이트는 `not_assessed(artifact_missing)` 이지 `pending` 이 아니다 |

⚠ **공통 패턴 (F1–F8)**: "정보가 없어서" 가 아니라 **"정보가 있는데 기계 경로에 없어서"**.
**F9 는 예외** — 여기서는 정보가 **정말 없다**(궤적 파일 자체가 없다). 그래서 처방도 다르다:
F1–F8 은 "적힌 것을 실행 경로에 올리자", F9 는 **"없는 것을 없다고 말하게 하자"**.
v1 이 F9 를 놓친 탓에 §8 Phase 3 이 "b2o3 lineage 배선 → `--for` 재검사" 라는 **실행 불가능한
계획**이었다. v2 에서 수정한다.

## 1. codex 2차 P0 — 반영 원장

| P0 | codex 지적 | 판정 | 반영 위치 |
|---|---|---|---|
| 1 | 5단 status 사다리가 서로 다른 개념을 한 줄에 섞음 | **전면 수용 — v1 이 틀렸다** | §3-1 (7축) · §4 |
| 2 | scope 당 active 1개는 틀림 → slot + applicability | **수용** | §3-1 · §3-2 |
| 3 | codex+self 는 ratification 아님. `unratified=[자유문자열]` 은 새 fail-open | **수용** | §3-3 |
| 4 | gate 결과를 canonical value 에 되쓰지 말 것. 5단계 DAG + assessment sidecar | **수용 + 실측 보강(F9)** | §5 |
| 5 | `_method` 도장만 있고 method manifest 없음. SHA-1·짧은 commit 금지 | **수용** | §6 |
| 6 | λ₁ 은 정의만 채택 가능. 현재 구현(고정 R=3, adaptive+경고) 둘 다 부적격 | **수용 — 단 처방은 조정**(3D 전용 exact 로 충분, Fincke–Pohst 불필요) | §7 |
| 7 | `require()` 자진신고로는 누락을 못 잡음. shell `\|\| true` 도 대상 | **수용 + 실측 확인** | §8 |

**우리가 실측으로 보강한 3건** (codex 가 스냅숏만 보고 쓴 부분):

1. **F9 (위)** — codex P0-4 의 "final 9 trajectory 가 확인되기 전에는 `diagnostic_unbound`"
   는 **아직 관대하다.** 궤적은 확인 실패가 아니라 **부재**다 → `not_assessed(artifact_missing)`.
2. **하지만 DAG 상위 4단계는 지금 배선 가능하다.** `db/properties/b2o3_vs_lpscl16_conductivity.csv`
   가 **per-seed D 9개를 이미 담고 있다**(b2o3 600/800/1000 K × s2/s3/s4, 주석 블록
   `# PER-SEED D (cm2/s): FULLY symmetric 3-seed x 3-T reseed`). 즉 `per-run D → T별 3-seed
   집계 → Arrhenius → Ea claim` 은 **오늘 배선된다.** 없는 건 그 아래 한 단(원 궤적)뿐이고,
   따라서 **골격 게이트 노드만** `not_assessed` 다. codex 의 MVP("B₂O₃ end-to-end 증명")는
   재실행을 기다리지 않고 **지금 완주 가능**하다 — 단 종점이 "gate pass" 가 아니라
   **"gate not_assessed 가 정확히 그렇게 표시되는 것"** 이다.
3. **shell `|| true` 실존 확인** — `tools/sei/run_sei_neb.sh:267` 이 정확히
   `python3 "$REPO/tools/sei/collect_neb.py" || true` 다. 같은 파일 L21 은 `set -uo pipefail`
   로 **`-e` 가 없다**. codex 지적이 맞다. (한편 `tools/` 의 나머지 `|| true` 28건은 대부분
   `unset LD_LIBRARY_PATH … || true` / `conda activate … || true` 로 **무해** — 일괄 금지가
   아니라 **정책 대상 명령 목록**에만 거는 게 맞다.)

## 2. 설계 원칙 (v1 에서 2개 교체)

1. **기존 인프라의 확장이지 대체가 아니다.** `canonical_registry.json`(값) ·
   `convention_check.py`(수치 상수) · `kb_wiki.py lint`(문서) 는 **enforcement 백엔드**로
   재배치한다. 새로 만드는 것은 **규약·판례 층 하나**. *카탈로그 1 + 백엔드 4*.
2. **레지스트리 = 판례집.** 확정된 결정만. 잠정 문턱(β 0.30/0.60 등)은 **못 들어간다**.
   미확정 규약을 쓴 산출물은 자동으로 강등 도장을 받는다 — 단 **강등 사유는 자유 문자열이
   아니라 등록된 proposed decision ID** 여야 한다 (P0-3).
3. **fail-closed.** 레지스트리를 못 읽으면 계산하지 않는다. unknown ID 는 실패.
   canonical import 실패 시 fallback 금지. 탐색 한도 초과는 **경고 후 계속이 아니라 실패**.
4. ~~날짜 기반 래칫~~ → **지위 기반 래칫** (P0/Q3 반영). 날짜 일괄 전환은 하지 않는다.
   **canonical·approved·ranking 에 쓰이는 값은 기존 항목도 즉시 차단**이고,
   display-only legacy 만 debt allowlist 로 유예한다 — **allowlist 항목에는 만료일과 사유가
   필수**(만료일 없는 allowlist 는 영구화되는 것이 기본 실패 모드다).
5. ~~consumer 목록 자동 유도(선언 스캔)~~ → **양방향 대조** (P0-7). 레지스트리가
   `applies_to` 로 **요구 집합을 역산**하고, 도구의 선언 집합과 **다르면 실패**한다.
   선언 스캔만 하면 "선언을 빠뜨린 도구" 가 정확히 안 보인다.
6. **⭐ 신설: 사람 승인이 상한, 기계는 하향만.** 평가기는 지위를 **올리지 못한다**.
   자동 승격 경로가 없어야 "게이트를 통과시키려고 게이트를 고치는" 회로가 안 생긴다.
7. **⭐ 신설: 산출물에 저장된 지위는 "생성 당시" 기록이다.** 소비자는 그것을 그대로 믿지
   않고 **현재 레지스트리로 재평가**한다 (P0-5 후단).

## 3. ① 판례집 — 스키마 (전면 개정)

### 3-1. 다축 상태 (P0-1) — 5단 사다리 폐기

v1 의 `retracted > blocked > hold > provisional > approved` 는 **생명주기 · 사용제한 ·
사람조치 · 증거성숙도 · 사용권한 · 게이트결과를 한 줄에 뭉갰다.** 실제 우리 데이터에
그 조합이 존재한다: **b2o3 Ea 0.199 는 원자료가 유효한 3-seed 결과인데(evidence 는 성숙)
골격 게이트가 미평가라 ranking 에 못 쓴다** — v1 사다리는 이걸 `provisional` 한 칸으로
뭉개서 "증거가 약하다" 는 **틀린 신호**를 준다.

```jsonc
"status": {
  "decision_state":     "proposed | active | superseded | retracted",
  "artifact_integrity": "valid | incomplete | invalid",
  "lineage_status":     "missing | prose_only | wired | verified",
  "evidence_status":    "unassessed | provisional | validated | refuted",
  "gate_outcome":       "not_assessed | pass | fail | inapplicable",
  "release_status":     "blocked | diagnostic | provisional | approved | withdrawn",
  "allowed_uses":       ["public_audit","comparison","absolute_claim","ranking","manuscript"]
}
```

**실무 부담을 낮추는 규칙** (7축을 손으로 다 채우게 하면 아무도 안 쓴다):

- 사람이 직접 쓰는 축은 **2개뿐**: `decision_state`, 그리고 §3-3 의 `ratification`.
- `lineage_status` · `gate_outcome` · `artifact_integrity` 는 **기계가 산출**한다
  (계보 그래프·assessment sidecar·파일 존재/해시 검사에서).
- `evidence_status` 는 사람이 확정하되 **기본값 `unassessed`**.
- `release_status` 와 `allowed_uses` 는 **파생**한다 — 단 파생 결과는 `ratification` 이
  허용한 상한을 **넘지 못한다**(원칙 6).
- UI 배지(webapp 색·이모지)는 `release_status` + `allowed_uses` 에서만 파생한다.

**b2o3 Ea 가 새 어휘로 어떻게 표현되는가** (v1 사다리로는 표현 불가능했던 상태):

```jsonc
{ "artifact_integrity": "valid",        // 3-seed x 3-T, per-seed D 9개 존재
  "evidence_status":    "validated",    // 증거는 성숙하다
  "lineage_status":     "prose_only",   // 어느 run 이 이 값을 만들었는지 기계가 모른다
  "gate_outcome":       "not_assessed", // 골격 게이트: 입력 궤적 부재 (F9)
  "release_status":     "provisional",
  "allowed_uses":       ["public_audit", "comparison"] }   // ranking·absolute_claim 없음
```

### 3-2. slot / applies_to (P0-2) — scope 당 유일성 폐기

`scope` 는 **검색용 namespace** 로만 남기고, 유일성은 **slot + 겹치는 applicability** 에서
검사한다. 실제로 `md` scope 안에 MSD 창 · 시드 정책 · 단일시드 금지 · 배제 가설들이 **동시에
살아 있어야** 한다 — v1 의 `active(scope) → 1개` 규칙은 이 데이터에서 즉시 예외를 던진다.

```jsonc
{ "scope": "md.msd",                       // namespace (부모: md)
  "slot":  "msd_fit_window",               // 서로 대체되는 결정의 자리 — 여기서만 유일성
  "applies_to": { "systems": ["LPSCl-family"], "tasks": ["diffusivity"],
                  "methods": ["uma-s-1p1/omat NVT"], "use_cases": ["ranking","manuscript"] } }
```

- 유일성 검사: **같은 slot** + **applicability 가 겹치는** active 결정이 2개 이상이면 실패.
- 부모 scope 와 자식 scope 는 **누적 적용**한다.
- ⛔ **"더 구체적인 것이 암묵적으로 이긴다" 규칙은 두지 않는다** (codex). 충돌은 조용히
  해소되는 게 아니라 **드러나야** 한다 — 해소는 명시적 `supersedes` 로만.

### 3-3. ratification (P0-3) — agent 는 과학적 승격을 못 한다

v1 의 `"ratified_by": "codex+self"` 는 **독립 승인 두 표가 아니다** (같은 agent 계열이
작성·자기검토). 과학 결과나 허용 문장을 바꾸는 `metric·method·gate·prohibition·hypothesis`
는 **전부 human scientific owner 승인 필수**.

```jsonc
"proposed_by":  [{"actor_type": "agent",  "actor_id": "claude", "date": "2026-08-20"}],
"reviewed_by":  [{"actor_type": "agent",  "actor_id": "codex",  "date": "2026-08-20",
                  "verdict": "conditional_go"}],
"ratification": {
  "state": "ratified",                     // unratified | proposed | ratified | revoked
  "actor_id": "yonghoon", "role": "scientific_owner",
  "timestamp": "2026-08-__T__:__Z",
  "commit": "<full 40-hex>",               // 짧은 commit 금지 (P0-5)
  "evidence_digest": "sha256:…",           // 승인 시점에 본 근거 묶음의 지문
  "max_release_status": "approved",        // ⭐ 기계가 넘지 못하는 상한 (원칙 6)
  "max_allowed_uses": ["public_audit","comparison","ranking","manuscript"]
}
```

- agent 는 **제안·기술검증**까지. `state: proposed` 인 결정은 조회되지만 **강제력이 없고**,
  그것을 쓴 산출물은 자동으로 `release_status: diagnostic` 이 된다.
- ⛔ **`unratified: ["자유 문자열"]` 폐지** (v1 의 fail-open). 등록된 **proposed decision ID**
  만 허용하고 unknown ID 는 **실패**한다.

### 3-4. 결정 레코드 전체 형태

```jsonc
{
 "id": "D-2026-08-16-defect-cell-metric",
 "schema_version": 2,
 "kind": "metric",                          // metric|method|gate|hypothesis|prohibition|policy
 "scope": "neb.cell_metric", "slot": "point_defect_image_distance",
 "applies_to": {"systems":["*"], "tasks":["point_defect_neb"], "methods":["*"],
                "use_cases":["ranking","manuscript"]},
 "title": "점결함 이미지 거리 지표는 λ₁ (shortest nonzero lattice translation)",
 "statement": "…",                          // 결정의 **정의**만. 구현·문턱은 여기 아님
 "status": { …§3-1 7축… },
 "proposed_by": […], "reviewed_by": […], "ratification": { … },
 "method_ref": "M-2026-08-20-lambda1-exact-3d",   // ⭐ 구현은 methods.json 이 고정 (§6)
 "card": "kb/methodology/defect_cell_size_metric_2026_08_16.md",
 "evidence": ["Li3Nd 2x2x2: 면높이 8.469 vs λ1 10.372 — 판정 반전 실측"],
 "supersedes": ["D-2026-08-16-face-height-gate"],   // 대상 노드도 **실제로 등록**되어야 함
 "reopen_criteria": "λ1 판정이 실험/상위이론과 어긋나는 실측 1건",
 "enforcement": {
   "require": true,
   "tombstones": [{"grep":"perp_widths\\(.*\\)\\.min\\(\\)\\s*<","paths":["tools/**/*.py"],
                   "allow":["tools/sei/build_neb_inputs.py"],
                   "reason":"면 높이를 게이트 비교식에 쓰는 코드 금지 (표시는 허용)"}],
   "convention_check": null,
   "fixtures": ["skew_lattice_R3","cell_metric_flip"]
 }
}
```

**핵심 분리**: `statement`(정의) ↔ `method_ref`(구현 지문) ↔ `enforcement`(강제 수단) ↔
경험적 문턱(**아예 레지스트리 밖** — 예: "10 Å 이상" 은 별개 gate 결정이고 별도 승인 대상).
v1 은 이 넷을 한 항목에 뭉쳤고, 그래서 **λ₁ 정의는 옳은데 구현이 부적격**인 현재 상태를
표현할 수 없었다 (codex P0-6 가 정확히 이 지점을 짚었다).

## 4. ② 평가기 — 문맥을 받는다 (P0-1 후단)

```python
evaluate(subject_ref, use_case, claim_type) -> Verdict
#   subject_ref : "value:MD_Ea_eV/b2o3" | "artifact:db/properties/sei_neb.json#comp1_20_29" | …
#   use_case    : public_audit | comparison | absolute_claim | ranking | manuscript
#   claim_type  : mechanism | magnitude | ordering | existence
# -> {allowed: bool, release_status, allowed_uses, reasons[], blocking_decision_ids[],
#     downgrades[], badge:{fg,bg,label}}
```

- **같은 값이 use_case 별로 다른 답을 준다** — b2o3 Ea 는 `comparison` 은 허용,
  `ranking` 은 거부. v1 의 단일 사다리로는 불가능했던 동작이고, 이게 F4 재발 방지의 본체다.
- **자동 승격 없음.** `evaluate` 는 `ratification.max_release_status` 를 **상한**으로 두고
  **하향만** 한다.
- 소비처는 전부 이 함수만 부른다: `collect_neb`(콘솔) · `webapp/data.py`(배지) ·
  `validate_canonical` · figure/manuscript 생성 스크립트.
- **내부 분리** (codex 권고): `tools/policy.py` <!-- lint-skip-path: 설계 단계 — 생성 예정 --> 는 **CLI facade** 로
  남기되, 스키마 validator · 순수 evaluator · lineage 코드는 내부 모듈로 분리한다.
  (repo 의 flat 단일 파일 문화와 충돌하지만, 여기서는 **순수 함수 테스트 가능성**이 이긴다
  — 평가기는 픽스처로 고정해야 하는 유일한 코드다.)

### 4-1. F2 의 구체 수리 — collect_neb 파이프라인 순서

```
지금:   회수 → citable 계산(L209) → 결산표 출력(L341) → 사람판정 이월+하향(L392) → 저장
수리:   회수 → 이월(해시 검증, §5-4) → evaluate() → 결산표 출력 → 원자적 저장(tmp→os.replace)
```

- 출력 이모지·문구는 `evaluate()` 의 `badge` 만 쓴다. `"✅ 인용 가능"` 리터럴이 평가기
  밖에 있으면 tombstone lint 가 잡는다.
- 골든 네거티브: `citable=True + scientific_status=provisional` 레코드에서 **출력 문자열과
  저장 지위가 일치**해야 통과. **수리 전 코드는 이 픽스처에서 실패한다** — 그게 픽스처가
  진짜라는 증명.
- ⛔ 호출부 `run_sei_neb.sh:267` 의 `|| true` 제거 (§8-2).

## 5. ③ 계보 — 5단계 DAG + assessment sidecar (P0-4)

### 5-1. 게이트 결과를 canonical value 에 되쓰지 않는다

v1 §5-3 은 게이트 판정을 `gate_results.framework` 로 **canonical entry 에 되썼다**.
그러면 F4 와 **같은 사고가 구조적으로 반복된다**(다른 궤적의 판정이 최종값에 붙는다).
게이트 결과는 **immutable assessment sidecar** 로만 존재하고, canonical entry 는 그것을
**참조**만 한다.

```jsonc
// db/governance/assessments.json  (append-only)   <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
{ "assessment_id": "A-2026-08-20-b2o3-framework-01",
  "claim_ref": "value:MD_Ea_eV/b2o3",
  "method_id": "M-2026-08-20-framework-gate-v2",
  "input_artifact_ids": [],                       // ⚠ 비어 있다 = 최종 궤적 부재 (F9)
  "result": "not_assessed",
  "result_reason": "artifact_missing: run_highT_reseed.sh 가 --save_traj 미전달 → traj.xyz 없음",
  "decision_ids": ["D-…-no-retro-gate-without-artifact"],
  "created": "2026-08-20T…Z", "registry_digest": "sha256:…" }
```

### 5-2. b2o3 계보 DAG (5단계, 실제 데이터 기준)

```
L0  9 trajectories            ← ⛔ 부재 (F9). run_id 는 논리적으로 정의되지만 artifact 없음
L1  per-run MSD/D             ← ✅ 존재: b2o3_vs_lpscl16_conductivity.csv 의 PER-SEED D 9개
L2  T별 3-seed 집계 (600/800/1000 K, mean±std)   ← ✅ 같은 CSV
L3  Arrhenius fit             ← ✅ Ea 0.199 ± 0.034, D0 4.625e-04
L4  Ea claim (canonical MD_Ea_eV/b2o3)           ← ✅ canonical_registry entry
```

각 노드에 별도 ID + 해시: `run_id`(논리명) · `protocol_hash`(방법 지문) ·
`input_hash`(구조·시드·조건) · `artifact_hash`(파일 바이트) · `endpoint_hash`(NEB 끝점).

⭐ **L1–L4 는 오늘 배선된다. L0 만 부재다.** 따라서 b2o3 vertical slice 의 종점은
"gate pass" 가 아니라 **`lineage_status: wired`(L1–L4) + `gate_outcome: not_assessed`
(L0 부재) + 재실행 요구가 기계 가독으로 등록됨** 이다. 이게 codex MVP 를 재실행 없이
완주 가능하게 만드는 지점이자, **F9 를 시스템이 실제로 말하게 만드는 첫 사례**다.

### 5-3. 값-바인딩 모드 (`--for`)

```
python3 tools/ionic/msd_diffusive_check.py --framework --for value:MD_Ea_eV/b2o3
```

① 계보 조회 → ② `lineage_status != wired` 면 거부. ③ `wired` 여도 **L0 artifact 가
없으면**:

```
⛔ value:MD_Ea_eV/b2o3 에 골격 게이트를 묶을 수 없다.
   계보는 배선돼 있으나(L1–L4) 게이트 입력인 L0 궤적 9개가 **존재하지 않는다**
   (run_highT_reseed.sh 가 --save_traj 미전달, 2026-07-06/07 실행분).
   → 이 게이트는 재실행 없이는 닫히지 않는다. assessment A-…-01 (not_assessed) 참조.
   자유 진단은 --diagnostic (결과는 어떤 값에도 묶이지 않는다).
```

**v1 대비 무엇이 달라졌나**: v1 은 여기서 "글롭 대신 run 목록으로 검사하고 되쓴다" 였다.
그건 **입력이 있다고 가정**한 설계다. v2 는 입력 부재를 **1급 결과**로 취급한다.

### 5-4. 사람 판정 이월 (F8/R7)

```
이월 허용 ⟺ (root, tag) 동일 AND protocol_hash 동일 AND input_hash 동일 AND endpoint_hash 동일
불일치 시: "이월 거부 — protocol_hash 5f78… → a3c2… (바뀐 것: kpts 3→5)" + carry_refused 기록
```

## 6. method manifest (P0-5) — `method_id` 만으로는 아무것도 고정되지 않는다

```
db/governance/decisions.json          판례 (§3)              <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
db/governance/methods.json            방법 매니페스트 (immutable, versioned)  <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
db/governance/assessments.json        게이트 판정 sidecar (append-only)       <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
db/governance/artifact_tombstones.json  철회된 산출물 원장                    <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
db/governance/schemas/                JSON Schema (validator 원본)            <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
```

산출물 도장에 **반드시** 들어가는 것:

```jsonc
"_method": {
  "schema_version": 2,
  "method_id": "M-2026-08-20-framework-gate-v2",   // versioned + immutable
  "method_digest": "sha256:…",                      // 매니페스트 내용 지문
  "decision_ids": ["D-…"], "decision_digests": ["sha256:…"],  // 결정 revision 지문
  "registry_digest": "sha256:…",                    // 그 시점 레지스트리 전체 지문
  "git_commit": "<full 40-hex>",                    // ⛔ 짧은 commit 금지
  "git_dirty": false, "git_dirty_diff_sha256": null,
  "inputs": [{"path":"…", "sha256":"…", "run_id":"…"}],   // ⛔ SHA-1 금지
  "retro_gate_possible": true,                      // ⭐ R8/F9
  "release_status_at_stamp": "diagnostic",          // ⚠ "생성 당시" 기록일 뿐
  "stamped_utc": "2026-08-20T21:04:00Z"
}
```

⚠ **`release_status_at_stamp` 를 소비자가 그대로 믿으면 안 된다** (원칙 7) — 소비 시점에
`evaluate()` 로 **재평가**한다. 도장은 감사 추적용이지 권한 캐시가 아니다.

## 7. λ₁ — exact 3D (P0-6). 단 Fincke–Pohst 는 필요 없다

codex 반례(재현 완료):

```
a=(10,0,0)  b=(2.49,0.1,0)  c=(0,0,10)
R=3 스캔 → 2.492 Å        실제 λ₁ = 0.402 Å  (n = (-1,4,0))
```

**동의**: 고정 `R=3` 도, adaptive `R_MAX` 후 경고 계속도 production gate 로 부적격.
**조정**: codex 는 "Gram 기반 Fincke–Pohst 또는 인증된 sphere enumeration" 을 요구했지만,
**차원이 3 으로 고정**된 우리 문제에서는 그보다 **훨씬 작은 exact 알고리즘**이 있고, 그것이
codex 가 요구한 성질(exact · integer n · unimodular invariance · hard fail)을 전부 만족한다.

```
1. degeneracy 검사:  |det| / (|a1||a2||a3|) < eps  →  hard fail (near-singular)
2. greedy(Lagrange–Gauss 3D) reduction — Nguyen–Stehlé 2004:
     차원 ≤ 4 에서 greedy 는 **Minkowski-reduced basis 를 다항시간에** 낸다
3. Minkowski-reduced 3D basis 에서 |b1| = λ₁ 이 **정확히 성립** (정의상 b1 은 최단 비영 벡터)
4. 정수 계수 n 은 누적 unimodular 변환 U 에서 복원해 **함께 저장**
5. certificate: reduced basis 위에서 |n_i| ≤ 2 (125조합) 전수 확인.
   더 짧은 것이 나오면 그것은 **구현 버그**이므로 경고가 아니라 hard fail
6. 반올림 금지: 문턱 비교는 full-precision λ₁ 원값으로
```

**비용**: 반복 수십 회 + 내적 125회 = 마이크로초. 일반 SVP 기계(격자 차원이 큰 경우의
Fincke–Pohst / 인증 열거)는 **도입하지 않는다** — 3D 전용 정답이 있는데 일반 기계를
들이는 것은 이 repo 의 코드 규율(§기존 도구 확장 > 새 파일)에도 어긋난다.

- **구현 위치**: 새 파일이 아니라 `tools/sei/build_neb_inputs.py::shortest_translation`
  **교체**(canonical 단일 출처 유지, F6 와 정합).
- **selftest(음성 경로 포함)**: ① codex 반례 → 0.402 · n=(-1,4,0) ② 랜덤 unimodular U 로
  basis 를 바꿔도 λ₁ 불변 ③ near-singular 셀 → 예외 ④ 면 높이 판정과 갈리는 Li₃Nd 실측
  ⑤ 반올림된 λ₁ 로 문턱 비교하면 실패하는 케이스.
- **결정 분리**(P0-6): `defect-cell-metric` 은 **정의만** 판례로 올린다.
  구현은 `M-…-lambda1-exact-3d` 매니페스트, "10 Å 이상" 경험 문턱은 **별개 gate 결정**
  (별도 승인 대상 — 지금은 승인하지 않는다).

## 8. consumer 자동 적용 (P0-7) — 자진신고 폐지

### 8-1. 양방향 대조

```python
require_for(__file__, operation, context) -> RequiredSet   # 레지스트리가 applies_to 로 역산
declared = policy.require([...])                            # 도구가 선언한 집합
if declared != required: hard fail  ("선언 누락: D-… / 불필요 선언: D-…")
```

- **`main()` 첫 줄만으로는 부족**(codex). CLI 가 `PolicyContext` 를 만들고, **실제 산출물을
  만드는 public boundary 와 writer** 가 그 context 없이는 실행되지 않게 한다.
- ⛔ **순수 helper import 에는 부작용을 넣지 않는다** (Q2 답: import 시점 require 반대).

### 8-2. shell 도 대상

- 정책 대상 명령에 `|| true` **금지** — 실측 위반 1건: `tools/sei/run_sei_neb.sh:267`
  `python3 …/collect_neb.py || true` (Python hard-fail 을 그대로 삼킨다).
- 같은 파일 L21 `set -uo pipefail` → **`set -euo pipefail`**.
- ⚠ 일괄 금지는 하지 않는다 — `tools/` 의 `|| true` 대부분은 `unset LD_LIBRARY_PATH` /
  `conda activate` 로 **무해**하다. tombstone 은 **정책 대상 명령 목록**(collect_neb ·
  convention_check · validate_canonical · policy · preflight)에만 건다.
- shell 용 policy wrapper: `policy_run <tool> …` 가 실패를 전파하고 도장 컨텍스트를 넘긴다.

### 8-3. 관문 위치 (codex 후단 지적)

> "GitHub Action 은 push 뒤 실패하면 이미 원격에 올라간 뒤다."

동의. CI 는 **안전망**이고, **진짜 관문은 생성 단계**다:
`webapp` 빌드 · figure 생성 · manuscript/release 산출 스크립트의 **첫 동작**이
`preflight --hard` 여야 한다. CI 는 그 관문을 우회한 커밋을 사후에 잡는 역할.

## 9. 시드 판정 (codex) + 우리 조정

### 9-1. MVP 에 들어가는 4결정 (codex 권고 그대로)

| id | kind | 내용 |
|---|---|---|
| `source-authority` | policy | **canonical DB/manifest 가 log·화면보다 우선**. 화면 문구는 평가기 산출물만 |
| `hash-bound-carry` | policy | protocol/input/endpoint hash 불일치 시 **사람 판정 승계 금지** |
| `no-fallback` | policy | canonical 구현 **import 실패 시 fallback 재구현 금지** (hard fail) |
| `defect-cell-metric` | metric | λ₁ **정의**만 (구현은 §7 매니페스트, 10 Å 문턱은 별건) |

여기에 codex 가 "현재 문구 그대로 registry-ready" 로 판정한 2건(`gap-eigenvalue`,
`uma-li3n-ban`)을 **함께 넣는다** — 수리가 필요 없고, 서로 다른 kind(method / prohibition)
를 하나씩 태워 **스키마가 kind 별로 동작하는지**를 MVP 안에서 검증할 수 있다. → **총 6건.**

### 9-2. 확대 대기 (entry 수리 필요 7건 — codex 판정 수용)

`neb-ci-order`(QE neb.x 범위로 한정) · `neb-mlip-absolute`(현 UMA scout·미검증 chemistry
범위) · `msd-window`(LPSCl-family UMA MD protocol 범위) · `seed-policy`(최소 시드 / 정지규칙 /
optional stopping 금지를 **3개로 분리**) · `elastic-relaxed-ion`(이번 argyrodite quasi-static
비교 범위) · `single-seed-sigma`(1.33× **artifact 철회**와 **일반 claim policy** 분리).

### 9-3. 재승인 필요 3건 (수용 — 특히 2건은 우리가 틀렸다)

- `beta-estimator-mto` — estimator(MTO)와 문턱 **둘 다** 재승인. v1 은 문턱만 제외했는데,
  estimator 선택도 방법이므로 `methods.json` + 승인 대상이 맞다.
- `com-drift-closed` — ⭐ **codex 가 맞다.** ASE Langevin `fixcm=True` 가 닫는 것은
  **총 COM 표류**뿐이고, **species-relative drift**(골격이 한 방향, Li 가 반대)는 **안 닫힌다**.
  실제로 우리가 골격 MSD 게이트를 새로 만든 이유가 정확히 그것이다 — v1 의 `com-drift-closed`
  는 **자기 도구의 존재 이유와 모순되는 결정**이었다. `특정 fixcm=True run family 에서
  총 COM 표류 배제` 로 좁혀 재승인.
- `monroe-newman-closed` — "무기 SE 부적용" 은 과대범위. **"sole design criterion 으로
  쓰지 않음"** 으로 좁히고 사람 승인.

### 9-4. 빠진 시드 (codex 5건 + 우리 1건)

canonical DB/manifest 우선 · hash 불일치 시 승계 금지 · canonical import 실패 시 fallback 금지 ·
exact lineage 없이 값·게이트 결합 금지 · canonical softBV 와 cascade legacy Adams proxy
교차비교 금지 — **그리고 F9 발 신설**:

> **`no-retro-gate-without-artifact`** — 게이트 입력 artifact 가 부재하면 결과는
> `not_assessed(artifact_missing)` 이며 `pending` 으로 적지 않는다. 프로덕션 MD 러너는
> 궤적 저장을 기본값으로 하거나, 미저장을 산출물에 `retro_gate_possible:false` 로 박는다.

⭐ `supersedes` 대상인 **옛 결정도 실제 node 로 등록**한다 (dangling edge 금지, graph validator 검사).

## 10. MVP 실행 순서 (Q8 반영 — 12시드·329도구 동시 도입 폐기)

| Phase | 내용 | 비용 | 관문 |
|---|---|---|---|
| **A** | 다축 schema + JSON Schema validator + graph validator(dangling/slot 충돌) + 순수 evaluator + human ratification 흐름 | 1.0 d | 스키마 픽스처 |
| **B** | **exact λ₁**(§7) + 반례 fixture 5종 + `build_neb_inputs --selftest` 신설 | 0.5 d | selftest 음성 경로 |
| **C** | b2o3 **L1–L4 DAG 배선** + assessment sidecar + `--for` 거부 경로 (**종점 = `not_assessed` 가 정확히 표시되는 것**) | 0.5 d | F9 픽스처 |
| **D** | `collect_neb` + `webapp` 이 **같은 evaluator 결과**를 쓰게 이관 + 원자적 저장 + `run_sei_neb.sh` `\|\| true` 제거 | 1.0 d | F2·stale-carry 골든 픽스처 |
| **E** | 빠른 core CI **매 push (Windows + Linux)** + 무거운 suite weekly + **생성 단계 preflight hard gate** | 0.5 d | Q4 |
| — | 통과 후 §9-2/9-3 확대 (별건, 이번 견적 밖) | — | 사람 승인 |

**합계 ≈ 3.5 d**. v1 의 "3 d" 와 숫자는 비슷하지만 **범위가 다르다** — v1 은 같은 3일에
12시드 + `stamp()` 5도구 + 래칫 상시화까지 넣었다(codex Q8 지적의 실체). v2 는
**6결정 · 도구 2곳 이관 · λ₁ 하나**로 줄였고, 확대는 slice 통과 이후 별건이다.

## 11. ⚠ 한계·반론 (지우지 말 것)

1. **우회를 못 막는다.** `require()` 를 안 부르는 도구는 자유다 — 다만 §8-1 양방향 대조로
   **누락이 보이게는** 된다. 목표는 강제가 아니라 **비용 역전**(따르는 게 우회보다 싸게).
2. **레지스트리 자체가 단일 실패점**이다. fail-closed + 자체 selftest + 픽스처가 완화책이지만
   **내용이 틀리면**(잘못 확정) 시스템이 오류를 *더 강하게* 전파한다 — 이것이 codex 가
   12시드 즉시 도입을 막은 이유이고, MVP 6건으로 줄인 근거다.
3. **7축 상태는 실무 부담이 크다.** §3-1 의 "사람이 쓰는 축은 2개" 규칙이 지켜지지 않으면
   6개월 뒤 축 절반이 기본값으로 썩는다. **첫 확대 시점에 이 지표를 실측**해야 한다.
4. **tombstone grep 은 원리적으로 불완전.** 이름을 바꿔 재구현하면 못 잡는다.
5. **산문 드리프트는 남는다.** 결정으로 **승격된 것만** 보호된다.
6. **브랜치 밖은 못 지킨다.** DEM 세션(공유 litdb) · gabia 로컬 상태는 관할 밖.
7. **F9 는 이 시스템이 만들어도 과거를 복구하지 못한다.** b2o3 골격 게이트는
   **재실행 없이는 영원히 `not_assessed`** 다. 레지스트리가 하는 일은 그 사실이 조용히
   `pending` 으로 위장되지 않게 하는 것뿐이다.
8. **`evidence_digest` 는 사람이 실제로 그 근거를 읽었음을 보증하지 않는다.** 승인 시점의
   바이트를 고정할 뿐이다 — ratification 의 진짜 품질은 여전히 사람에게 달려 있다.

## 12. codex 3차에 묻는 것 (범위를 좁혀서)

| # | 질문 | 우리 입장 |
|---|---|---|
| R1 | §7 의 **3D greedy/Minkowski + |n_i|≤2 certificate** 가 exact 요구를 만족하는가, 아니면 그래도 인증 열거가 필요한가 | 3D 고정이라 충분하다고 본다. 반례가 있으면 그것이 결론 |
| R2 | §5-2 의 "L0 부재 / L1–L4 배선" 분해가 `diagnostic_unbound` 보다 정확한 표현인가 | `not_assessed(artifact_missing)` 이 맞다고 본다 |
| R3 | MVP 를 6건(codex 4 + ready 2)으로 늘린 것이 slice 를 흐리는가 | kind 다양성 검증에 필요하다고 본다 |
| R4 | §3-1 "사람이 쓰는 축 2개, 나머지 파생" 이 7축의 실무 부담을 실제로 해결하는가 | 미검증 — 한계 §11-3 으로 남김 |
| R5 | `com-drift-closed` 를 "총 COM 표류만 배제" 로 좁히면, **species-relative drift** 는 어떤 결정으로 다뤄야 하는가 (골격 게이트가 그 역할인가) | 골격 게이트가 그 역할이나, 문턱 미승인 상태 |

## 관련

- 발단: `kb/reviews/codex_B_neb_md_tools_2026_08_20.md` §5 B-R11 (Q5)
- v1 → v2 판정: codex 2차 리뷰 (2026-08-20, 조건부 GO / 스키마·12시드 NO-GO) — 원장은 §1
- 실패 사례: 같은 카드 B-R10~R13 · `kb/reviews/codex_A_cascade_ml_2026_08_20.md` §2-2 철회
- F9 실측 근거: `tools/modelc_v3/run_highT_reseed.sh` L32–39 ·
  `tools/modelc_v3/disorder_ensemble_diffusion.py` L238–241, L300 ·
  `db/properties/b2o3_vs_lpscl16_conductivity.csv` (PER-SEED D 9개)
- 기존 인프라: `db/properties/canonical_registry.json` · `tools/convention_check.py` ·
  `tools/db/validate_canonical.py` · `tools/kb_wiki.py`
