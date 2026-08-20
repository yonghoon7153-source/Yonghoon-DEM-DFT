# Codex 독립 적대 교차검증 — 도핑 §I + everything-else §J (2026-08-20)

**검증 대상**: `origin/claude/stoic-knuth-NObVQ @ d640d70d`
**방식**: 대상 커밋의 **격리 스냅샷**에서 정적 감사 + 실제 JSON 입출력 + 음성 대조 실행
**Codex 작업 좌표**: `Codex/dem-mpm-crosscheck @ c8fc99fe` (원본 브랜치·코드 미수정)
**범위**: `codex_review_request_sulfide_doping_20260819.md` §I ·
`codex_review_request_everything_else_20260819.md` §J 및 직접 연결된 코드·원장

> Codex 는 Downloads 의 정정 전 `everything_else` 사본을 판정 근거에서 제외하고, 리포의
> `d640d70d` 판(§C-1 `med 0.0670 / max 0.9679 / n=3,033` · §C-2 `1.4 → 4.2 → 8.1 → 22.9 %` ·
> §F-1 `ε_sphere 1.13 % / 14.5 %p`)만 검토했음을 명시했다.

아래는 **보고 원문 박제**이고, 내 독립 확인과 처리는 §말미 "내 대응" 에 있다.
등재: `findings.json` **CDXIJ-1 ~ CDXIJ-7**.

---

## 0. Codex 결론

두 문서의 문제의식에는 동의하지만, **수정 완료·녹색 검사라는 결론은 아직 성립하지 않는다.**

| ID | 심각도 | 판정 |
|---|---:|---|
| **CDX-IJ-01** | P1 | FA-02 의 6필드 수정은 실제 JSON 경로에서 **4/6만** 닫혔다.  나머지 2필드는 계속 `h0`. |
| **CDX-IJ-02** | P1 | 판정기는 정확한 8팔·origin pairing·prereg 명목값·전체 causal input 을 강제하지 않는다. |
| **CDX-IJ-03** | P1 | `σ_eff` 가 입력 `σ_SE` 와 정확히 같은 배수로 변한다는 D-2 가설은 **DBE 혼합 이온망에서 거짓**. |
| **CDX-IJ-04** | P1 | FA-05 미완료.  웹앱이 서빙하는 seminar JSON 에 `+52%/+5.6%` 가 현행 사실로 남았는데 ban-sweep 은 0건. |
| **CDX-IJ-05** | P1/P2 | Rule J 와 FA-04 selftest 가 자기보고·skip 을 성공으로 받는 false-green. |
| **CDX-IJ-07** | P2 | FA-03 명목 태그는 작동하나 비단사 문자열 키와 report 의 고정 `d=0.30` 으로 계약이 깨진다. |

권고: FA-01 `verified` 승격 가능(좁은 원 결함 한정) · **FA-02 reopen/partial** ·
FA-03 유지 또는 split · FA-04 유지 또는 split · **FA-05 reopen/split**.

## 1. CDX-IJ-01 — FA-02 는 실제 JSON 경로에서 4/6만 유효

`sdcp_gain_verdict.py:81,83` · `:193-211` · `:420-428`

| 누락 필드 | decode | 판정 |
|---|---|---|
| `sigma_vgcf_S_cm` · `sigma_sdcp_S_cm` · `sdcp_sphere_d_um` · `backend` | `None` | `HOLD` |
| `sdcp_yield_to_vgcf` | **`False`** | **`h0`** |
| `sigma_ptfe_S_cm` | **`0.0`** | **`h0`** |

```python
'sdcp_yield_to_vgcf': bool(man.get('sdcp_yield_to_vgcf', False))
'sigma_ptfe_S_cm': float(man.get('sigma_ptfe_S_cm', 0.0) or 0.0)
```

missing gate 는 `None` 만 보므로 위 두 필드에서는 발화할 수 없다.  소유자 selftest ㉒ 는
`_read()/collect()` 를 거치지 않고 내부 row 에 `None` 을 직접 넣어 이 결함을 놓친다.
더구나 selftest ⑬/⑭b 는 바로 그 부재→기본값 변환을 **정상 계약으로 고정**한다.

## 2. CDX-IJ-02 — 필드 열거보다 큰 causal-contract·pairing 구멍

- 모든 `_GEN_FIELDS` 가 없으면 의도적으로 통과한다.  그러나 같은 디렉터리는 같은 argv·입력·
  코드 세대의 증거가 아니다.  manifest 에 `schema_version=2` 가 있는데 `_read()` 는 읽지 않는다.
  `periodic` 은 계산에 영향을 주는데 main manifest 에서 누락, `plate_z_grid_um` 은 기록돼도 버려진다.
  입력 scaffold/phase/fibre digest 와 code SHA 는 계약에 없다.
- prereg 명목값·8팔을 강제하지 않는다: 팔 수만 같으면 되고 **2팔씩만 있어도** 판정 ·
  origin 필드가 전부 없어도 통과 · SBE/DBE origin 집합 동일성 미확인 · 2×2×2 factorial,
  `bridge_um=0.48`, expected stamp/voxel 같은 명목값 미강제 · paired 통계가 origin key 가 아니라
  **파일명 정렬 뒤 `zip()`**.

```text
2 arms each, origin absent              -> h0
SBE origins 0..7, DBE origins 100..107 -> h0, paired SE 0.0%
same origin set but filename pairing    -> reported SE 0.0%
origin-key true pairing                 -> SE 0.8511%
```

권장 계약(요약): 단일 typed `causal_inputs` registry 에서 argparse·manifest·comparator 생성 ·
모든 resolved input 을 `varied/fixed/blocked/provenance-only` 로 분류 · 미분류 옵션은 CI 실패 ·
JSON Schema `required` + `additionalProperties:false` 로 absent 와 explicit null 구분 ·
canonical **값 전체** + 입력 artifact digest + code SHA 로 `input_digest` · `vary_only` 만 제외한
causal map 자동 exact-diff · legacy payload 는 attestation 없으면 HOLD ·
`pair_id = bed_digest + origin_shift + fixed_contract_digest` 로 join.

## 3. CDX-IJ-03 — D-2 의 정확한 1.53배 가설은 DBE 에서 틀림

STEP3 선형 selftest 는 격자 전체가 `sid=6`(all-SE)인 경우만 검사한다.  실제 DBE 이온망은
도핑 시 변하는 SE 와 **고정된 SDCP** 가 동시에 전도한다.

| 구조 | `σ_eff,new / σ_eff,base` |
|---|---:|
| all-SE | **1.5300** |
| SE/SDCP 50:50 series laminate | **1.0948** |
| SE/SDCP 50:50 parallel laminate | **1.3975** |

⇒ 이 트랙에는 오히려 선형성 이상의 실질 산출물이 있다:
η = (σ_eff,new/σ_eff,base − 1)/(f − 1) = **model-internal response attenuation**.
SBE all-SE 는 코드 oracle, DBE 의 η 는 morphology-dependent 결과로 분리해야 한다.
STEP4 도 결합계라 단순 ×1.53 이 아니다 (Codex 의 analytic sandwich 파라미터에서 이온 ×1.53 이
총전류를 약 **×1.0551**).  ⚠ 문헌의 1.25/1.53/1.94 는 주로 cold-pressed pellet EIS 이고 코드의
3.0 mS/cm 는 single-crystal grain-interior 앵커라, 팔 이름은
**`literature-ratio sensitivity scenario`** 가 안전하다.

## 4. CDX-IJ-04 — FA-05 와 ban-sweep 은 현재도 false-green

기본 scan glob 에 JSON·shell 이 없다.  그 결과:
`docs/seminar/seminar_deck.json:527,552,557,609,653,662` 가 `+52%`·`+5.6%` 를 현행 결론으로 말하고
`webapp/app.py:3954,3998-4011` 의 `/api/seminar/slides` 가 그 JSON 을 **직접 서빙**하며
`scripts/sr01_gate5_2x2.sh:157-158` 이 철회된 `f_artifact` 를 출력하는데 — 스윕은 **누수 0**.

추가 음성 대조: 문서 머리의 **무관한** HISTORICAL/철회 단어로 파일 전체 면제 · 근처의 무관한
retired 문장으로 면제 · 표기 변형 `"+52.0%"` 미검출.

## 5. CDX-IJ-05 — Rule J 는 FA-01 회귀에는 유효하나 일반 인증기는 아님

보지 않는 것: arm 별 exact expected component set · top-level manifest status · 실제
`sigma_*`/`n_dof`/finite 값 · 필수 artifact·digest · fibre-point/segment·ion/pore·temperature·
periodic·GPU·STEP4 조합.  독립 fake producer 가 `electronic=complete` 하나만 기록해도, 전부
`disabled` 로 기록해도 `([], [])` 로 통과.
다만 FA-01 의 **좁은 원 결함**은 별개다 — 수정 전 `4c735121^` 에서 plain 팔 `STEP3 skipped` +
exit 0, target 에서 두 팔 완료, hoist 제거 mutant 를 Rule J 가 검출.  ⇒ FA-01 자체는 독립
`verified` 승격 가능.

## 6. CDX-IJ-06 — FA-04 selftest 는 원본 미가용 환경에서 fail-open

정상 환경 68/68 PASS (옛 "원본 대 원본" 항등검사보다 확실한 개선).  그러나 `predictor_engine`
import 를 막으면 broad except 가 4검사를 생략하고 `64/64 PASS`.  또 현재 음성 대조는 사본
**구현**을 변형하지 않고 이미 계산된 `_b` dict 를 바꿔 비교 predicate 만 시험한다.

## 7. CDX-IJ-07 — FA-03 은 명목 수정만 통과

명목 계약은 확인 (`default → DBE_v015_sph` · `BRIDGE_UM=0.30 → _b030` · `SDCP_D=0.45 → _d045` ·
둘 다 → `_b030_d045`; 기본 파일명 호환 유지).  그러나 `${x/./}` 는 단사가 아니다:

```text
BRIDGE_UM=0.3 (0.3) -> _b03      BRIDGE_UM=03 (3.0) -> _b03
SDCP_D=0.45  (0.45) -> _d045     SDCP_D=04.5 (4.5)  -> _d045
```

또 report 는 각 JSON 의 `sdcp_sphere_d_um` 을 읽지 않고 전역 `SDCP_D=0.30` 으로 `V_TRUE` 를
계산한다.  `d=0.45` fixture 에서 report `0.238732`, 정확값 `0.0707355` = **3.375배 과대**.

## 8. §J 자체의 결함 계수 불일치

요청서는 `9 → 17` 이라 쓰지만 같은 문서 §D 는 기존 9 외 최소 3건(≥12)을 이미 말한다.
fable audit 도 "기존 12건은 범위 밖" 이라 쓴 뒤 신규를 `α3+β2+γ3+δ1 = 9` 로 센다 ⇒ **≥21**.
§J 의 8행 표에는 신규 감사가 센 `scipy-closing` 무음 생략 1건이 빠졌다.
또 "조건부 바인딩은 정적 검사가 원리적으로 못 본다" 는 과하다 — **pyflakes 가 놓친다**는 실측은
맞지만 CFG 지배관계·확정할당 분석으로 정적으로 잡을 수 있다.

## 9. 질문별 회답 (요지)

- **Q-I1**: 스키마 hash 냐 `schema_version` 이냐가 아니라 **단일 causal-input contract +
  canonical value digest**.  key-set hash 만이면 값 차이를 못 잡고 무해 metadata 에 과민;
  수동 version 만이면 bump 누락이 다시 no-op.  새 노브는 기본 고정 취급 + 미분류 fail-closed.
- **Q-I2**: **2단계 저장은 여전히 필요하다.**  Rule J = 등록 경로의 회귀 탐지, 2단계 저장 =
  비싼 solve 뒤 manifest/serialization/disk/kill 실패에서 결과 보존.  순서: solve 직후 raw+digest
  를 staging 에 atomic write → provenance seal·계약 검증 → temp+fsync+`os.replace` → 검증 후
  active pointer publish → 실패한 staging 은 recoverable 이지만 active 아님.  최종 payload
  schema 는 유지 가능하므로 광범위한 파괴적 변경은 아니다.
- **Q-I3**: 서로 다른 estimand 면 각각 쓸 수 있으나 **같은 1 % 문턱으로 섞으면 안 된다.**
  도핑은 결정론적 재풀이라 origin-key paired 가 정본.  SBE all-SE oracle 은
  δ_i = σ_new,i/(f·σ_base,i) − 1 의 `max|δ_i|` 를 gate 로.  DBE 는 attenuation oracle 을 따로
  사전등록.  8 origin 은 IID 표본이 아니므로 `sd/√8` 은 inferential SE 가 아니라 deterministic
  sensitivity summary.  1 % gate 에는 4자리 저장값이 아니라 raw solver precision·residual 을 쓸 것.
- **Q-J1**: 대체가 아니라 **보완**.  Rule J 에 최소
  `{plain, fibre-point, fibre-segment} × {production component on/off}` 와 실제
  `mpm_input_from_case → run_mpm.sh → payload` argv 생성 경로를 넣어야 한다.
- **Q-J2**: 모든 unit test 가 아니라 **성공/실패를 인증하는 새 gate/checker** 에는 의무화.
  최소 계약 5가지: 정상 witness · invariant 별 fault mutant · mutation 적용 assertion ·
  예상 diagnostic code 고정 · **skip/미실행/대상 0건은 실패**.
- **Q-J3**: 개발 회귀로는 정상이나 독립 검증은 아니다.  최소 증거 6가지(정확한 pre-fix SHA 에서
  독립 fixture 실패 → claimed-fix SHA 에서 통과 → 구현자와 다른 oracle/적대 mutant → production
  argv 확인 → 명령·환경·값·digest 기록 → 독립 커밋/CI attestation 을 `verified_sha` 로).
  현재 `check_review_findings.py` 는 `owner != verified_by` 문자열·SHA 형식/존재·evidence 첫 파일
  존재 정도만 보므로 무관한 파일을 evidence 로 써도 통과한다.

## 10. Codex 독립 실행 요약

| 실행 | 결과 |
|---|---|
| `sdcp_gain_verdict.py --selftest` | 30/30 PASS — 그러나 실제 JSON mutation **2/6 false-green** |
| `check_method_discipline.py --selftest` | 51/51 PASS |
| full method checker | 0 errors, 4 warnings |
| `ml_design_structure.py --selftest` | 68/68 PASS |
| 같은 selftest + `predictor_engine` 차단 | **64/64 PASS** — 패리티 4개 생략 |
| Rule J fake manifest | `([], [])` — 계산 없는 self-report 통과 |
| `--ban-sweep` | 241 files, 누수 0 — 활성 seminar JSON/sh 는 범위 밖 |
| pairing mutation | disjoint origins·2 arms 도 **h0** |
| FA-03 tag mutation | 명목 suffix PASS, `0.3↔03`·`0.45↔04.5` cache-key 충돌 |
| FA-03 nondefault report | `d=0.45` 참부피 비 **3.375배 과대** |
| finding verification mutation | 무관 evidence + 다른 문자열 actor 도 구조 검사 통과 |

⚠ Python 3.14 에서는 `check_method_discipline.py` 의 제거된 `ast.Num` 참조로 selftest 가 중간
crash.  WSL/Python 3.12 결과를 반박하진 않으나 **문서에 환경 버전 표기가 필요**하다.

## 11. Codex 의 최소 종료조건 10가지

① FA-02 두 default-normalized field 를 absent-preserving decode 로 + 실제 파일-path 6/6 mutation 상주 ·
② legacy `_GEN_FIELDS` 부재는 attestation 없으면 HOLD · ③ 정확한 8 origin set·pair key·nominal
prereg·causal-input digest 강제 · ④ D-2 를 SBE all-SE oracle 과 DBE attenuation hypothesis 로 분리 ·
⑤ Rule J 에 arm 별 exact expected component/output oracle 과 production argv matrix ·
⑥ ban-sweep 에 활성 JSON/sh/Python/생성 artifact 포함, self-authorizing 배너 폐기 ·
⑦ FA-03 cache key 를 canonical config digest 로, SKIP 전 저장 manifest 대조, report 는 row 별 직경 ·
⑧ FA-04 는 predictor 미가용 시 UNVERIFIED/FAIL · ⑨ checker 세 개를 CI/presubmit 에 실제 연결
(현재 `.github` workflow 부재 = "기계 강제" 가 수동 실행) · ⑩ 리뷰 문서 front matter 에
`base_sha`·`review_target_sha`·`claims_ledger_sha` 고정.

---

# 내 대응 (2026-08-20, commit `a5b02b96` 및 후속)

**전부 재현 확인 후 처리.**  등재 = `findings.json` CDXIJ-1 ~ CDXIJ-7.

| ID | 내 확인 | 처리 |
|---|---|---|
| **IJ-01** | 코드로 확정 (`:81,83` 정규화가 missing 게이트를 무력화) | 부재 보존(fail-closed) · ⑬⑭b 계약 뒤집기 · **㉒ 를 실제 JSON 16개 + `collect()` 로 재작성** → 6/6 HOLD.  verdict 34/34 |
| **IJ-02** | 미착수 (설계 변경) | **`open` 으로 등재** — typed causal-input registry·origin-key pairing·명목값 강제는 별건 |
| **IJ-03** | **독립 재현 성공**, 소수 넷째 자리까지 일치 (1.5300 / 1.0948 / 1.3975).  추가로 무작위 20 % SDCP η = 0.789 | **CL-57 등재** · `--selftest-temp` 에 회귀 3건(all-SE η=1 · 혼합 η<1 · topology 의존) · 오도한 라벨에 적용 범위 명시 |
| **IJ-04** | 파일·서빙 경로 실재 확인 | 범위에 `docs/**/*.json`·`webapp/**/*.json`·`scripts/*.sh` 추가, 패턴 `+52.0%`·`f_artifact` 추가 → **새로 16건** 드러나 전부 처리.  241 → **389 파일**, 누수 0 |
| **IJ-05** | 지적대로 status 문자열만 봤다 | 기대 상태 맵 + 수치 단언 · 단언부를 `smoke_assert_payload()` 로 분리해 **Codex 의 세 변형을 상주 음성 대조**(J-3a/b/c).  discipline 54/54 |
| **IJ-06** | 음성 대조 재현 (webapp 없는 사본 트리) | UNVERIFIED = 실패로 → 실측 **64/65 FAIL, exit 1** |
| **IJ-07** | 태그 비단사·report 전역 직경 확인 | awk `%g` 정규화 + **SKIP 전 기록 대조** 신설(`sdcp_phase_ledger_match.py`, 8/8) + report row 별 직경 |

**Codex 지적 중 아직 안 한 것** (정직하게 남긴다):
- **IJ-02 전부** — causal-input registry, origin-key pairing(현재 파일명 zip), 정확한 8팔·명목값 강제.
- **IJ-04 잔여** — 배너 하나로 파일 전체가 면제되는 self-authorizing 규칙, exact-string 매칭.
- **IJ-05 잔여** — argv 조합 2개뿐, production argv 생성기 미스모크.
- **IJ-06 잔여** — 음성 대조가 사본 **구현**이 아니라 계산된 dict 를 변형한다.
- **⑨ CI 연결** — `.github` workflow 가 없어 세 checker 는 여전히 **수동 실행**이다.
- **⑩ front matter SHA 고정** — 리뷰 문서에 `base_sha` 등을 아직 안 박았다.
- **§8 계수** — `9 → 17` 표기를 고쳤다 (아래).  "정적 검사가 원리적으로 못 본다" 도 완화했다.


---

# 2차 재검증 (2026-08-20 저녁) — 대상 `7246cd5b`

Codex 판정: **CDXIJ-1 · 3 · 6 = CONFIRMED-FIXED** (verified, 검증 커밋
`675d2a75f9cdbc224381ecc4ac3bee18443e44dd` @ `Codex/dem-mpm-crosscheck` — 우리 리포에 없는
외부 worktree라 기계 확인은 불가하고, 원장에 `verified_repo` 로 그 사실을 남겼다) ·
**2 · 4 · 5 · 7 = STILL-OPEN** · **NEW-DEFECT 2건(P1)**.

| 항목 | 판정 | 내 처리 |
|---|---|---|
| IJ-01 | CONFIRMED-FIXED | — |
| IJ-02 | STILL-OPEN | 도핑 런 전 **최소 4항목**을 CDXIJ-10 으로 등재 (미착수).  요청서 §K-4 |
| IJ-03 | CONFIRMED-FIXED | §D-2 (나)를 **다시** 좁혔다 (§K-1) |
| IJ-04 | STILL-OPEN | **부분 해소** — 자기승인 배너 차단 + 표기 변형 정규화 + 음성 대조 2건.  UI 누수는 CDXIJ-9 로 분리 |
| IJ-05 | STILL-OPEN | **부분 해소** — 리더 예외=오류 · 계산 증거 요구 · 예상 code 고정 (J-3d).  argv 매트릭스는 잔여 |
| IJ-06 | CONFIRMED-FIXED | — |
| IJ-07 | STILL-OPEN | **해소** — matcher 에 raw 값 (`%g` 는 표시용), 근접 alias 회귀 2건 |
| **NEW-1** | P1 | **CDXIJ-8** — 판정기가 backend 를 component 정본이 아니라 마지막 solve 에서 읽었다 → `_component_backends()` + 회귀 ㉔ |
| **NEW-2** | P1 | **CDXIJ-9** — 덱 철회 배너를 **UI 가 렌더하지 않았다** → 서빙 경로 fail-closed (`?historical=1`) |

★ 조인 규칙이 리포에서 **187건**을 새로 드러냈고 전부 처리했다 — 이력 문서 배너들이
원장을 가리키지 않고 있었다 (자기승인 배너의 실제 규모).

**아직 안 한 것**: CDXIJ-10(도핑 런 전 4항목) · Rule J 의 argv 매트릭스와 production 생성기 ·
PPTX 파일 자체의 표지 · CI 연결 · 리뷰 문서 front matter SHA 고정.
