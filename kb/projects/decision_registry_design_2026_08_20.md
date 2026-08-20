---
title: "결정 레지스트리 설계 — 규약 역행을 구조로 막는다 (B-R11 Q5 답안, codex 2차 리뷰 대상)"
date: 2026-08-20
updated: 2026-08-20
tags: [policy, registry, ci, provenance, lineage, tombstone, codex, infrastructure]
status: 설계 — 구현 전 (codex 2차 GO 대기)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: max
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 결정 레지스트리 설계 — 규약 역행을 구조로 막는다

> **한 줄**: 문서 규칙(grep 금지목록·CLAUDE.md 조항)은 이미 세 번 뚫렸다. 필요한 것은
> **기계가 읽는 판례집(decision registry) + 산출물 계보 도장(method manifest) +
> 모든 화면이 같은 지위를 읽는 단일 평가기(policy evaluator) + 밀리면 돌아오지 못하는
> 래칫(CI/preflight)** 네 개다. 이 카드는 codex 제안(2026-08-20 1차 리뷰)을 이 repo 의
> 실제 규모·문화에 맞게 구체화한 **구현 전 설계**다 — 코드는 codex 2차 GO 뒤에 쓴다.

## 0. 왜 — 실패 사례 8건이 요구 조건이다

설계는 추상 원칙이 아니라 **이미 일어난 실패**에서 거꾸로 뽑는다. 전부 2026-08 실측이다.

| # | 실패 (실측) | 왜 문서 규칙으로 못 막았나 | → 요구 조건 |
|---|---|---|---|
| F1 | **철회된 지표 재사용** — 08-16 에 λ₁ 로 확정된 셀 지표를 08-19 새 도구가 면 높이로 다시 씀. docstring 이 철회된 쪽 논리를 재현 | 결정이 kb 산문에만 있었다. 새 파일을 쓸 때 아무것도 그 카드를 읽으라고 강제하지 않았다 | **R1** 결정을 기계가 조회 가능해야 하고, 도구가 자기 결정 의존을 **선언**해야 한다 |
| F2 | **화면 ≠ db** — `collect_neb` 결산표가 "✅ 인용 가능" 을 찍는데 저장값은 `citable:false`. 그 화면을 믿고 리뷰 카드 3곳에 오기 전파 | 지위 계산이 도구마다 사본이고, 출력 순서(계산→출력→하향)가 틀렸다 | **R2** 지위는 **한 함수**만 계산하고 콘솔·db·webapp·그림이 전부 그걸 읽는다 |
| F3 | **배제된 가설 재론** — COM 표류 가설(08월 초 fixcm=True 로 배제)을 다시 논증. 1저자가 끊음 | 닫힌 질문이 보고서 안 한 줄이라 검색 전에 안 보인다 | **R3** 닫힌 가설도 레지스트리 항목이다 (`kind: hypothesis`) |
| F4 | **계보 오류** — β 를 잰 궤적(`b2o3_full`, single-seed legacy)과 Ea 0.199 를 만든 궤적(3-seed reseed)이 **다른데** 연결해 "3점 중 2점 흔들림" 을 주장 | 값의 출처가 산문(provenance 문자열)뿐이라 도구가 "이 글롭이 그 값을 만든 런인가" 를 알 길이 없다 | **R4** 산출물에 **기계 계보 도장**, 값에 **run 배선**, 게이트 도구에 **값-바인딩 모드** |
| F5 | **처방이 진단을 앞섬** — 부피 +32.7 % 원인이 fmax 사다리로 이미 닫혔는데(같은 문단에 인용까지 해 놓고) stress 파인튜닝을 제안 | 닫힌 결론이 산문이라, 인용은 되는데 **결론 갱신을 강제하지 못한다** | **R3'** 닫힌 결론 조회가 코드 사다리의 **0단계**여야 한다 |
| F6 | **fallback 재구현** — λ₁ import 실패 시 `except BaseException` 으로 같은 수식을 재구현 (구현 분기 허용 구조) | "복사 금지" 는 관례였지 검사가 아니었다 | **R5** canonical 구현은 단일 출처 + **fallback 금지(hard fail)** 를 검사로 고정 |
| F7 | **selftest 실패 채로 푸시 2회** | 사람이 기억으로 돌리는 절차는 두 번 빠졌다 | **R6** 푸시 경로에 자동 관문(preflight/CI) |
| F8 | **사람 판정 이월 오염 위험** — collect_neb 가 `<root>/<tag>` 만 보고 이월 → 프로토콜이 바뀐 새 계산에 옛 판단이 붙을 수 있음 (codex 지적) | 이월 키에 정체성(해시)이 없다 | **R7** 사람 판정은 **동일 protocol_hash + input_hash** 에서만 승계 |

⚠ **이 표의 공통 패턴**: 여덟 건 모두 "정보가 없어서" 가 아니라 **"정보가 있는데 기계 경로에
없어서"** 였다. repo 에는 이미 답이 있었다 — kb 카드, db note, provenance 문자열.
그래서 처방은 "더 많이 적자" 가 아니라 **"적힌 것을 실행 경로에 올리자"** 다.

## 1. 설계 원칙 5개

1. **기존 인프라의 확장이지 대체가 아니다.** 이 repo 에는 이미 3개의 부분 레지스트리가 있다:
   `canonical_registry.json`(**값**의 지위) · `convention_check.py`(**수치 상수**의 일관성) ·
   `kb_wiki.py lint`(**문서** 위생). 새로 만드는 것은 **규약·판례** 층 하나이고, 나머지는
   그것을 **가리키는** enforcement 백엔드로 재배치한다. 4중 레지스트리가 아니라
   *카탈로그 1 + 백엔드 4* 구조다.
2. **레지스트리 = 판례집, kb = 심리 중 사건.** 확정(ratify)된 결정만 들어간다. 리뷰 중·잠정
   문턱(β 0.30/0.60 같은 것)은 **못 들어간다** — 들어가는 순간 자의적 상수가 법이 된다.
   미확정 규약을 쓴 산출물은 자동으로 `allowed_use: diagnostic` 도장을 받는다.
3. **fail-closed.** 레지스트리를 못 읽으면 계산하지 않는다. 모르는 결정 ID 는 실패다.
   superseded ID 선언도 실패다(후계 ID 를 알려주며). — λ₁ hard-fail 수정과 같은 원리를
   시스템 전체 기본값으로.
4. **래칫(ratchet), 빅뱅 아님.** 329개 도구를 소급하지 않는다. **새 도구와 손댄 도구**부터
   적용하고, 위반 검사는 날짜 기반으로 warn → error 로 조인다. 소급은 값이 걸린 곳
   (MD_Ea 계보)부터 수동으로.
5. **목록은 자동 유도.** 결정별 consumer 목록을 손으로 관리하면 썩는다 — lint 가
   `policy.require([...])` 선언을 스캔해 역색인을 만든다. supersede 시 옛 ID 를 아직
   선언하는 도구가 있으면 **lint 가 실패**한다 = 마이그레이션 강제 장치.

## 2. 구성요소 4개 (파일 배치)

```
db/decision_registry.json      ① 판례집 (기계 진실 — db 에 둔다. kb 카드는 인간용 근거) <!-- lint-skip-path: 설계 단계 — Phase 0/1 에서 생성 예정 (codex 2차 GO 뒤) -->
tools/policy.py                ② 단일 모듈: 조회·선언검사·도장·평가기·lint·selftest <!-- lint-skip-path: 설계 단계 — Phase 0/1 에서 생성 예정 (codex 2차 GO 뒤) -->
tools/policy_fixtures/         ③ 골든 네거티브 (과거 실패의 영구 재현 케이스) <!-- lint-skip-path: 설계 단계 — Phase 0/1 에서 생성 예정 (codex 2차 GO 뒤) -->
tools/preflight.py             ④ 로컬 관문 (selftest 로스터 + 전 lint 일괄) <!-- lint-skip-path: 설계 단계 — Phase 0/1 에서 생성 예정 (codex 2차 GO 뒤) -->
.github/workflows/policy.yml   ④' CI 래칫 (ubuntu 매 push · windows 주 1회) <!-- lint-skip-path: 설계 단계 — Phase 0/1 에서 생성 예정 (codex 2차 GO 뒤) -->
```

단일 파일 `policy.py` 로 두는 이유: 이 repo 의 도구 문화가 flat 단일 파일 + `--selftest` 다.
패키지를 만들면 그 문화 밖의 첫 예외가 되고, 예외는 관례를 깬다.

## 3. ① 판례집 — 스키마와 시드 (실물 예시)

### 3-1. 스키마

```jsonc
{
 "version": 1,
 "decisions": [
  {
   "id": "D-2026-08-16-defect-cell-metric",   // D-YYYY-MM-DD-slug (정렬·grep 가능)
   "kind": "metric",                          // metric | method | gate | hypothesis | prohibition
   "scope": "neb.cell_metric",                // dot-namespace. 첫 세그먼트는 화이트리스트
   "title": "점결함 이미지 거리 지표는 λ₁ — 면 높이 금지",
   "status": "active",                        // active | superseded | retracted
   "decided": "2026-08-16",
   "ratified_by": "codex+self",               // 확정 주체 (1저자 확정은 "human")
   "canonical_impl": "tools/sei/build_neb_inputs.py::shortest_translation",
   "card": "kb/methodology/defect_cell_size_metric_2026_08_16.md",   // 인간용 근거 (lint 가 존재 검사)
   "evidence": ["Li3Nd 2x2x2: 면높이 8.469 vs λ1 10.372 — 판정 반전 실측"],
   "supersedes": ["D-2026-08-16-face-height-gate"],   // 그래프 간선. 옛 항목은 삭제 아님
   "reopen_criteria": "λ1 판정이 실험/상위이론과 어긋나는 실측 1건",
   "enforcement": {                           // ⭐ 결정마다 백엔드가 다르다 — 명시한다
     "require": true,                         // 도구가 policy.require() 로 선언해야 하는가
     "tombstones": [
       {"grep": "perp_widths\\(.*\\)\\.min\\(\\)\\s*<", "paths": ["tools/**/*.py"],
        "allow": ["tools/sei/build_neb_inputs.py"],
        "reason": "면 높이를 게이트 비교식에 쓰는 코드 금지 (표시는 허용)"}],
     "convention_check": null,                // 수치 상수면 여기로 위임 (중복 구현 금지)
     "fixtures": ["tools/policy_fixtures/cell_metric_flip.json", <!-- lint-skip-path: 설계 단계 — Phase 0/1 에서 생성 예정 (codex 2차 GO 뒤) -->
                  "tools/policy_fixtures/skew_lattice_R3.json"] <!-- lint-skip-path: 설계 단계 — Phase 0/1 에서 생성 예정 (codex 2차 GO 뒤) -->
   }
  }
 ]
}
```

핵심 설계 선택:
- **`enforcement` 를 결정마다 명시** — "레지스트리에 넣었다 = 지켜진다" 는 착각을 막는다.
  백엔드 5종: `require`(런타임 선언) · `tombstones`(정적 grep 백스톱) ·
  `convention_check`(수치 상수 위임) · `fixtures`(골든 네거티브) · 평가기(지위 어휘).
  ⚠ codex 가 경고한 대로 **grep 단독은 또 뚫린다** — tombstone 은 백스톱이지 주 방어가 아니다.
- **`supersedes` 간선 + 영구 보존** — 철회는 삭제가 아니라 상태 전이. repo 의 retracted 문화 그대로.
- **`reopen_criteria` 필수** — "다시 논증하려면 무엇이 필요한가" 를 결정 시점에 못박는다.
  F3(COM 재론) 방지의 반쪽: 재론 자체를 막는 게 아니라 **재론의 입장료**를 정한다.

### 3-2. 시드 12건 (전부 이미 확정된 것만 — 잠정은 제외)

| id (slug) | kind | scope | 내용 · canonical_impl | 주 백엔드 |
|---|---|---|---|---|
| defect-cell-metric | metric | neb.cell_metric | λ₁ (`shortest_translation`) — 면높이 게이트 금지 | require+tombstone+fixture |
| neb-ci-order | method | neb.ci_order | **no-CI 수렴 → CI**. 미수렴 밴드 CI 금지 (실측: +2.3 eV 폭주) | require+fixture |
| neb-mlip-absolute | prohibition | neb.mlip_scope | MLIP 장벽 절대값 인용 금지 — 용도는 경로 선택 (Li₃Nd 1.76×) | 평가기(도장 diagnostic) |
| msd-window | method | md.msd_fit | 창 2–50 ps · 자유절편 D | **convention_check 위임** (이미 있음) |
| beta-estimator-mto | method | md.beta | 확정 β 판정은 **MTO·시드평균곡선**만 (STO 는 진단) | require |
| seed-policy | gate | md.seeds | 멀티시드 · 정지규칙 선선언 · "통과할 때까지" 금지 (SEMIFINAL 철회) | require+card |
| com-drift-closed | **hypothesis** | md.hypotheses | COM 표류 = **배제됨** (ASE Langevin fixcm=True, 08월 판정) | Step0 조회 + reopen_criteria |
| gap-eigenvalue | method | gap.reading | fixed-occ nscf eigenvalue 만. DOS-threshold retracted | tombstone("dos.*threshold" in gap tools) |
| uma-li3n-ban | prohibition | mlip.applicability | UMA 를 Li₃N 에 금지 (2026-06). ⚠ Li₃P 는 1차 통과·장벽 미검증 — 별도 결정 아님 | require |
| elastic-relaxed-ion | method | elastic.protocol | paper 값은 relaxed-ion 만 (clamped 2.3× 과대) | 평가기 |
| monroe-newman-closed | hypothesis | mech.design_rules | Monroe–Newman 을 설계 원칙으로 쓰지 않음 (무기 SE 부적용) | Step0 조회 |
| single-seed-sigma-retracted | prohibition | md.sigma | 단일시드 σ 비 인용 금지 (1.33× 철회, SEMIFINAL 2026-07-09) | 평가기+tombstone |

**들어가지 않는 것 (명시)** — 골격 게이트 문턱(0.30/0.60/MIN_N 8), `MAX_IMAGE_JUMP_EV=0.8`
(절대 문턱이 장벽 큰 계에서 오탐 — B §2-1 실측 반례), 끝점 심화 이완 기본값, Stage 02
`fmax ≤ 0.01` 게이트(codex 가 처방했지만 **아직 우리 쪽 확정 절차를 안 거침**).
전부 **codex 2차에서 확정되면 그때 D-항목 발급**. 그 전에 이 규약들을 쓴 산출물은
`policy.stamp(..., unratified=["framework_beta_thresholds"])` 로 **자동 diagnostic 강등**된다.

## 4. ② 단일 평가기 — 화면과 db 가 같은 말을 하게

### 4-1. API (tools/policy.py) <!-- lint-skip-path: 설계 단계 — 생성 예정 -->

```python
load()                          # db/decision_registry.json. 못 읽으면 RuntimeError (fail-closed) <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
query(scope_prefix) -> [행]     # Step 0 용. CLI: python3 tools/policy.py query neb <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
active(scope) -> Decision       # scope 당 active 가 1개가 아니면 그 자체로 예외 (codex 규칙)
require([ids])                  # 도구 main() 첫 줄. unknown/superseded/retracted → hard fail
                                #   superseded 면 후계 id 를 에러 메시지에 박는다
stamp(out: dict, *, method_id, decisions, inputs, unratified=()) -> dict
                                # _method 블록 삽입 + allowed_use 산정 + 원자적 저장 헬퍼
status_of_value(metric, system) -> Status      # canonical_registry 조인
status_of_artifact(record)      -> Status      # _method / citable / _do_not_cite / gate 조인
```

### 4-2. Status 계약 — 어휘를 하나로

지금은 `citable` / `n_citable` / `retracted` / `scientific_status` / `absolute_citable` /
`_do_not_cite` / `provisional` 이 **파일마다 다른 조합**으로 쓰인다 (codex: "같은 retracted
의미를 섞는다"). 평가기가 이걸 **5단 사다리 하나**로 접는다:

```
retracted > blocked(게이트 미통과) > hold(사람 하향) > provisional > approved
```

- 반환: `{level, label, fg, bg, reasons[], forbidden[], decision_refs[]}` —
  webapp 배지 색까지 여기서 나온다 (`canonical_status_all` 의 로직을 **이 함수로 이관**).
- **우선순위는 코드가 아니라 이 계약이 정의**하고, 픽스처가 고정한다.
- 소비처 이관 대상 (Phase 2): `collect_neb`(콘솔 결산표) · `webapp/data.py` ·
  `validate_canonical` · 이후 watch/figure 스크립트 (래칫 목록).

### 4-3. F2 의 구체 수리 — collect_neb 파이프라인 순서

```
지금:   회수 → citable 계산(L209) → 결산표 출력(L341) → 사람판정 이월+하향(L392) → 저장
수리:   회수 → 이월(해시 검증) → status_of_artifact() → 결산표 출력 → 원자적 저장
```
- 출력 이모지는 **평가기 결과만** 쓴다. `"✅ 인용 가능"` 리터럴이 policy.py 밖에 있으면
  tombstone lint 가 잡는다.
- 저장은 `tmp → os.replace` (codex: 현재 비원자적).
- 골든 네거티브: "citable=True + scientific_status=provisional" 레코드에서
  **출력 문자열과 저장 지위가 일치**해야 통과. 수리 전 코드는 이 픽스처에서 실패한다
  — 그게 픽스처가 진짜라는 증명.

## 5. ③ 계보 도장 — F4(b2o3 사고)를 구조로 막기

### 5-1. 산출물 도장 (`_method` 블록)

값을 만드는 모든 도구가 출력 json 에 박는다 (Phase 3 부터, 새/손댄 도구 우선):

```jsonc
"_method": {
  "method_id": "framework-gate-v2",
  "decision_ids": ["D-2026-08-16-defect-cell-metric", "..."],
  "unratified": ["framework_beta_thresholds"],     // → allowed_use 자동 강등 근거
  "allowed_use": "diagnostic",                      // diagnostic | provisional | approved
  "tool": "tools/ionic/msd_diffusive_check.py",
  "git_commit": "6a6fe70e", "git_dirty": false,
  "inputs": [{"path": ".../T800/msd.json", "sha1": "…", "run_id": "b2o3_full/T800"}],
  "stamped": "2026-08-20T21:04"
}
```

`run_id` 는 새 발명이 아니다 — `build_neb_inputs.protocol_hash` 가 이미 같은 목적의 지문을
만든다. 그 패턴을 일반화한 것.

### 5-2. 값 쪽 배선 — canonical_registry 에 `lineage`

```jsonc
{ "system": "b2o3", "metric": "MD_Ea_eV", "value": 0.199,
  "lineage": {
    "status": "prose-only",            // prose-only | wired | verified
    "runs": null,                      // wired 가 되면 run_id 목록/패턴
    "prose": "3-seed x 3-T reseed 2026-07-07 (b2o3_vs_lpscl16_conductivity.csv)",
    "note": "⚠ 궤적 경로 특정이 Phase 3 의 첫 작업 — 특정이 안 된다는 사실 자체가 F4 사고의 원인"
  } }
```

`validate_canonical --audit` 이 이미 `provenance_open` 을 세니까, 거기에
`lineage.status != wired` 카운트를 추가 — **날짜 래칫**: 신설 entry 는 즉시 error,
기존 entry 는 2026-09-01 까지 warn.

### 5-3. 게이트 도구의 값-바인딩 모드 — 사고 워크스루

```
python3 tools/ionic/msd_diffusive_check.py --framework --for MD_Ea_eV/b2o3
```
동작: ① 레지스트리에서 그 값의 `lineage` 를 읽는다 → ② `wired` 가 아니면:

```
⛔ MD_Ea_eV/b2o3 의 lineage 가 미배선(prose-only)이다.
   어느 궤적이 이 값을 만들었는지 기계가 모른다 — 게이트 판정을 이 값에 묶을 수 없다.
   자유 진단은 --diagnostic 으로 가능하다 (결과는 값과 연결되지 않는다).
```

③ `wired` 면 글롭이 아니라 **run 목록을 레지스트리에서 받아** 검사하고, 판정을
`gate_results.framework` 로 **그 entry 에** 되쓴다(도장 포함).

**이 모드가 있었으면 F4 는 오류가 아니라 시끄러운 거부가 됐다** — 내가 `b2o3_full` 글롭을
검사한 것 자체는 유효한 진단이지만, 그 결과가 0.199 에 **묶이는 순간**을 기계가 막는다.

### 5-4. 사람 판정 이월 (F8/R7)

```
이월 허용 ⟺ (root, tag) 동일 AND protocol_hash 동일 AND endpoints_hash 동일
불일치 시: "이월 거부 — protocol_hash 5f78… → a3c2… (바뀐 것: kpts 3→5)" 를 찍고
           사람 판정 필드는 비운 채 `carry_refused` 기록을 남긴다
```

## 6. ④ Step 0 + 문서 단일 포인터

### 6-1. 코드 사다리에 0단계 (CLAUDE.md 수정)

```
사다리: ⓪ python3 tools/policy.py query <영역> — 그 영역의 active/superseded 결정과 <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
        canonical 구현을 먼저 본다 (superseded 를 다시 구현하는 것이 최다 실패 유형)
      → ① 이게 있어야 하나 → ② tools/ 에 이미 있나 → ③ 플래그 추가로 되나 → ④ stdlib → ⑤ 새 파일
```

### 6-2. AGENTS.md — 규칙 복사 금지, 포인터 1줄

현재 AGENTS.md 에는 코드 사다리 자체가 **없다** (실측 — Claude 와 Codex 가 다른 규칙을 읽는
구조, codex 지적 그대로). 복사해 넣으면 다음 드리프트가 생기니, 양쪽에 **같은 한 줄**만:

```
## 코드 규율
- 규약·판례는 db/decision_registry.json 이 단일 원본이다. <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
  코드를 읽거나 새 도구를 만들기 전에 `python3 tools/policy.py query <영역>` 을 먼저 본다. <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
  상세 사다리·selftest 규율: CLAUDE.md §코드 규율 (여기 복사하지 않는다 — 드리프트 방지).
```

## 7. ④' preflight + CI

### 7-1. tools/preflight.py (로컬 관문 — 푸시 전 1회) <!-- lint-skip-path: 설계 단계 — 생성 예정 -->

```
로스터(명시 목록 — 자동 글롭 금지: 무거운 도구가 CI 를 죽인다):
  selftest: msd_diffusive_check · argyrodite_cage_neb · collect_neb · uma_engine_probe ·
            bench_against_dft · extract_figures · convention_check · validate_canonical ·
            kb_wiki(lint) · policy(lint+selftest) · build_neb_inputs(→ selftest 신설이 선결)
  검사:     tombstone 스캔 · scope-당-active-1 · 골든 픽스처 · consumer 역색인(supersede 위반)
  래칫:     tools/ 에 새 .py 가 로스터에도 EXEMPT(사유 필수)에도 없으면 실패
출력: 요약 1줄/항목 (repo 의 "출력은 기본이 요약" 규율). 실패만 상세.
```

F7 의 수리이자, "selftest 를 절차로 박아야 한다(미구현)" 항목의 구현이다.

### 7-2. .github/workflows/policy.yml (스케치)

```yaml
name: policy
on:
  push: {branches: [claude/friendly-meitner-lldvar]}
  workflow_dispatch:
  schedule: [{cron: "0 18 * * 5"}]          # 주 1회 금요일 (windows 용)
jobs:
  linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5      # 3.11
      - run: pip install numpy ase pymupdf spglib
      - run: python3 tools/preflight.py --ci <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
  windows:                                  # 인코딩 회귀가 실측 실패 유형(⑤)이라 포함
    if: github.event_name != 'push'         # 매 push 는 과함 — 주 1회 + 수동
    runs-on: windows-latest
    steps: [checkout, setup-python, pip 동일, "python tools/preflight.py --ci"] <!-- lint-skip-path: 설계 단계 — 생성 예정 -->
```

의존성 실측 근거: 로스터의 selftest 는 GPU/fairchem 없이 돈다 (EMT·합성 데이터 설계 —
이미 그렇게 만들어져 있다). `pymupdf` 는 extract_figures, `spglib` 는 build_neb_inputs 용.

## 8. 도입 단계 — 비용과 순서 (래칫)

| Phase | 내용 | 비용 | 선결 |
|---|---|---|---|
| **0** | `policy.py`(query/require/lint/selftest) + 시드 12건 + 픽스처 4건(F1·F2·codex 반례 2) + CLAUDE/AGENTS 포인터 | 0.5 d | **codex 2차 GO** |
| **1** | `preflight.py` + 로스터 + `build_neb_inputs --selftest` 신설 + GitHub Actions | 0.5 d | Phase 0 |
| **2** | 평가기 이관 3곳 (collect_neb 순서 수리 → webapp → validate_canonical) + 원자적 저장 | 1 d | Phase 0 |
| **3** | `stamp()` 를 활성 생산도구 5개에 + `--for` 값-바인딩 + **b2o3 lineage 배선(최우선 실물)** + `--min_l_basis vector` 진단 강등 | 1 d | Phase 2 |
| **4** | 래칫 상시화: 날짜 기반 warn→error · 손댄 도구 이관 · lattice_metrics 정밀화(§10-Q7) | 상시 | — |

합계 ≈ 3 일. **Phase 3 의 첫 실물이 b2o3** — 이 설계가 방금 낸 사고를 실제로 막는지
그 사례로 검증한다 (kgy `highT_reseed` 궤적 존재 확인 → lineage `wired` → `--for` 재검사).

## 9. ⚠ 한계·반론 (지우지 말 것)

1. **우회를 못 막는다.** `require()` 를 안 부르는 도구는 자유다. 방어선은 preflight 래칫
   ("로스터에 없는 새 파일 = 실패")과 Step 0 문화뿐 — **강제가 아니라 비용 역전**이
   목표다(따르는 게 우회보다 싸게).
2. **레지스트리 자체가 단일 실패점이 된다.** 그래서 fail-closed(못 읽으면 정지) + 자체
   selftest + 픽스처. 그래도 **내용이 틀리면**(잘못 확정) 시스템이 오류를 전파한다 —
   `ratified_by` 와 reopen_criteria 가 완화책이지 해결책이 아니다.
3. **tombstone grep 은 원리적으로 불완전** — 이름을 바꿔 재구현하면 못 잡는다.
   주 방어는 require+픽스처, grep 은 백스톱. codex 의 "grep 만으로는 반복된다" 에 동의.
4. **산문 드리프트는 남는다.** kb 카드 두 장이 서로 다른 말을 하는 것(F5 유형)은 이
   시스템이 직접 못 잡는다 — 결정으로 **승격된 것만** 보호된다. 승격 기준(무엇이 판례가
   될 자격인가)은 사람 몫이다.
5. **브랜치 밖은 못 지킨다.** DEM 세션(공유 litdb)·gabia 로컬 상태(sei_neb.json)는 이
   레지스트리의 관할 밖이다.
6. **Windows CI 는 주 1회다** — 인코딩 회귀가 최대 6일 늦게 잡힌다. 매 push 는 러너
   비용·속도 문제. 트레이드오프로 명시.
7. **`consumers` 자동 유도는 파이썬 도구만** 본다 — sh 러너가 규약을 어기는 경로는
   (러너가 파이썬 도구를 부르는 한) 간접 방어된다.

## 10. codex 2차 리뷰에 묻는 것

| # | 질문 | 우리 초안 |
|---|---|---|
| Q1 | scope 입도 — `neb.cell_metric` 수준인가 더 굵게(`neb`)인가 | dot-namespace, active-1 검사는 **말단 scope** 단위 |
| Q2 | `require()` 를 import 시점 vs `main()` 시점 | `main()` (라이브러리 재사용·selftest 오프라인 허용) |
| Q3 | lineage warn→error 날짜 | 신설 즉시 error / 기존 2026-09-01 |
| Q4 | Windows CI 주기 | 주 1회 + dispatch. 매 push 반대 |
| Q5 | 시드 12건의 선정 — 빠진 판례? 자격 없는 항목? | §3-2 표. 특히 `com-drift-closed` 같은 hypothesis kind 의 유용성 판단 |
| Q6 | 사람(1저자) ratify 절차 — `ratified_by: human` 을 요구하는 kind 는? | prohibition 과 hypothesis 는 human 필수, method/metric 은 codex+self 허용 |
| Q7 | λ₁ exact 구현 — 수렴 탐색으로 충분한가, LLL/Fincke–Pohst 가 필요한가 | 수렴 탐색 + R_MAX 경고로 시작, 병든 셀 실측이 나오면 승격 |
| Q8 | 이 설계 자체의 과잉 여부 — 2인(1저자+에이전트) 규모에 4구성요소가 유지되나 | Phase 0–1 만으로도 F1·F3·F5·F7 은 막힌다. 2–3 은 값이 걸린 곳만 |

## 관련

- 발단: `kb/reviews/codex_B_neb_md_tools_2026_08_20.md` §5 B-R11 (Q5) + codex 1차 리뷰 답신
- 실패 사례 원장: 같은 카드 B-R10~R13 · `kb/reviews/codex_A_cascade_ml_2026_08_20.md` §2-2 철회
- 기존 인프라: `db/properties/canonical_registry.json` · `tools/convention_check.py` ·
  `tools/db/validate_canonical.py` · `tools/kb_wiki.py`
- 선례(같은 패턴의 성공): `collect_neb` 이월 로직 · `protocol_hash` · convention_check 의 EXEMPT-사유 문화
