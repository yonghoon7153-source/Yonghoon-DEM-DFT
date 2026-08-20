---
title: "교차리뷰 C v2.1 — cascade 깔때기는 잘 작동했나 (codex 2라운드 종료)"
date: 2026-08-20
updated: 2026-08-20
tags: [codex, review, cascade, funnel, screening, gate, volume, doping]
status: v2.1 — codex 2라운드 종료 (manifest 지적 철회 · Q3 문구 하향 · 보고 형식 확정)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 교차리뷰 C v2 — cascade 깔때기는 잘 작동했나

> **판정 이력**: v1(`a4cc9c04`) → codex **NO-GO**. 네 건이 틀렸고 그중 하나는 카드의
> 뼈대였다. codex 가 준 재현 명령을 **전부 돌려 확인**했고 숫자가 정확히 일치한다.
>
> **한 줄 답 (codex, 우리 동의)**:
> **고정된 규칙은 47종을 실제로 줄였지만, 과학적으로 검증된 후보 선발기는 아니다.**
> 47→11 은 **역사적 규칙 교집합**이고, 11→1 은 **로스터 상대 진단값**이다.
>
> ⚠ **보고 수정에는 새 계산이 필요 없다.** 다만 *현재* shortlist 를 다시 만들려면
> Stage 02 재수렴 + 재선발 + 바뀐 대표 구조의 하위 계산 갱신이 필요하다.

## A. codex 지적 재현 결과 (전부 우리가 돌렸다)

```
post: 681  중앙 22.181  [18.867, 30.122]  19–22: 309  25 이상: 77
eos : 622  중앙 20.232                     19–22: 555
fit outside ±6%: 428   (그중 아래쪽 외삽 427)
```

| codex 지적 | 판정 |
|---|---|
| 20.232 는 post-anneal 부피가 아니라 **BM3 피팅 V₀** | ✅ **맞다 — v1 이 틀렸다** |
| v1 의 "591행 95.0 %" | ✅ **틀렸다.** 실제 EOS 19–22 는 **555/622 = 89.2 %** |
| v1 의 "25 이상 0행" | ✅ **틀렸다.** post-anneal 실제 부피 기준 **77행** |
| fitted V₀ 428/622 가 ±6 % scan 밖 (427 이 아래쪽 외삽) | ✅ 재현됨 |
| G4 는 독립 수송 신호가 아니다 (blocking override) | ✅ 코드가 이미 그 분해를 한다 (§2) |
| G5 percentile 은 **nearest order statistic** (선형 아님) | ✅ `int(round(q*(n-1)))` 확인 |
| G5 sweep "0→11 전 구간" 은 과장 | ✅ 실제 `0/1/1/2/4/11`, q=1.00 은 게이트를 끈 값 |
| cathode audit 을 "G6" 라 부르면 기존 정의와 충돌 | ✅ **맞다** — 기존 `T9_interface_axes` 에 이미 있다 (§3) |
| ~~manifest 가 stale~~ | ✅ **codex 철회** (2026-08-20) — `a4cc9c04` git blob 재검사 결과 funnel 과 manifest 가 `420e218e` / 86,018 B 로 정확히 일치. 앞선 검사가 **임시 감사 폴더에서 재생성된 파일을 원본으로 오인**한 것. 우리 재현과 같은 결론이다 |

## 0. 깔때기 실측 — **분모를 명시한다**

```
47 → 47 → 43 → 25 → 11 → 1
     G1    G2    G3   G4   G5
```

⛔ v1 의 치명적 오류: `unique_kill` 을 **판정 범위 없이** 적었다. 같은 게이트라도 어디까지
거는지에 따라 값이 다르다.

| 판정 범위 | G1 | G2 | G3 | G4 | G5 |
|---|---|---|---|---|---|
| **최종 1종** (G1–G5) | 0 | 0 | 1 | 6 | 10 |
| **11종 종점** (G1–G4) | 0 | 0 | **7** | **14** | — |

⇒ **11종을 말하면서 G3=1 · G4=6 을 쓰면 분모가 틀린다.** v1 이 그렇게 썼다.

**추가 구조 사실**: G1 fail 은 **공집합**이고 G2 fail 4종은 **전부 G3 fail 에 포함**된다.
⇒ **11종은 사실상 `G3 ∩ G4` 만으로 똑같이 얻어진다.**

### 0-1. "장식" 은 과한 말이다 — 셋을 구분해서 부른다

v1 은 `unique_kill = 0` 인 축 셋을 뭉뚱그려 "장식" 이라 했다. 정확한 표현은
**"이 풀·이 문턱·이 gate set 에서 추가 축소 기여가 없다"** 이고, 셋의 성격이 다르다:

| 축 | 정확한 이름 |
|---|---|
| G1 structural_stability | **비변별** — 이 풀에서 아무도 안 죽인다 (풀이 이미 그 조건으로 큐레이션됨) |
| G2 electrochemical_window | **포섭된 중복 축** — fail 4종이 전부 G3 에 포함 (late-TM d-band 의 두 얼굴) |
| cathode full/half audit | **post-hoc 중복 축** — core **밖에서만** 탈락시킨다 |

## 1. ⛔ v1 §0-4 전면 철회 — "하위 축은 오염되지 않았다" 의 근거가 틀렸다

v1 은 `eos_V0_per_atom` 중앙 20.232 를 근거로 *"미수렴 셀이 하위로 흘러간 행은 0 개"*
라고 썼다. **그 값은 실제 post-anneal 구조 부피가 아니라 BM3 피팅 V₀ 다.**

원자료에서 실제 post-anneal 부피를 재구성하면:

```
V_post = V_ref × (1 + screen_dV_over_V0) × (1 + anneal_dV_pct/100),  V_ref = 27.478273

681행  중앙 22.181 Å³/atom  [18.867, 30.122]
  19–22 : 309/681 = 45.4 %
  25 이상: 77행            ← v1 은 "0행" 이라고 썼다
```

그리고 **fitted V₀ 622개 중 428개가 실제 ±6 % scan 바깥**이고, 그중 **427개가 아래쪽
외삽**이다 — EOS 최소점이 스캔 구간 안에서 식별되지 않았다는 뜻이다.

**정확한 문장 (codex 제안, 채택)**:

> Stage 04 이후 계산값은 **선택된 구조에 대해** 존재하지만, **post-anneal 수렴과 EOS
> 최소점의 scan 내 식별은 검증되지 않았다.**

**발표용 (구어체, codex 제안 채택)**:

> Stage 04 이후 계산값은 선택된 구조에 대해서는 존재합니다. 다만 **post-anneal 구조가
> 충분히 수렴했는지, EOS 최소점이 실제 계산한 부피 구간 안에서 식별됐는지는 아직
> 검증되지 않았습니다.**

⚠ 이것은 *"하위 값이 전부 틀렸다"* 가 아니다. **"오염 0 을 증명하지 못했다"** 는 뜻이다.
v1 은 증명하지 못한 것을 증명했다고 썼다.

## 2. G4 는 독립적인 수송 신호가 아니다

`build_screening_funnel.py` 가 이미 그 분해를 한다 (코드 주석 그대로):

> `transport_norm` 규약상 `blocking >= BLOCKING_GATE`(0.60) 인 종은 `GATE_FLOOR`(0.05)로
> 눌려 `TRANSPORT_CUT`(0.30)을 **자동 실패**한다.

⇒ **G4 full unique 6종의 내역**:

```
5종  : 4 Å blocking 때문에 강제 탈락  (raw BVS 를 버리고 0.05 로 강제)
1종  : B₂O₃ — BVS-only 탈락
```

- blocking override 를 제거하면 **6종 중 5종이 역사적 0.30 컷을 넘긴다.**
- B₂O₃ 의 **조성 수준 onset 은 유효**하지만, **species 수준 "B₂O₃ 도펀트 효과" 귀속은
  Cl-rich 때문에 unresolved** 다.
- blocking 컷만 0.50→1.00 으로 움직여도 **core 생존자가 6→21종**으로 변한다.

⇒ 11 에 대해 말할 수 있는 최대는:
**"역사 47종에 legacy BVS 와 4 Å foreign-center 규칙을 적용한 산술 교집합."**
**승인 shortlist 가 아니다.**

## 3. "G6" 라는 이름을 철회한다 — 기존 정의와 충돌

`db/properties/cascade_stability_axes_verdict.json` 의 `T9_interface_axes` 에 **이미** 있다:

| 축 | kill | core unique |
|---|---|---|
| `cathode_full` | 2 (Sb₂O₅·TiF₄) | **[]** |
| `cathode_half` | 3 (BaO·MnO·Na₂O) | **[]** |
| `SE_LPSCl` | 29 | **6종** |
| Li anode | 35 | **6종** |

같은 파일이 **G6 = SE**, **G7 = Li** 로 부른다. 그런데 새 cathode verdict 는
"G6 로 편입" 이라 써서 **충돌한다.**

⚠ 그리고 v1 이 오늘 cathode audit 을 **"신규"** 라 부른 것도 부정확하다 — 축 자체는
2026-07-28 에 이미 등록돼 있었고, 오늘 새로 나온 것은 **94쌍 반응식 전수와 Li 흡수 분석**이다.

**정리 (채택)**:

```
historical funnel      : G1–G5, 5개
cathode full/half      : post-hoc cathode audit
SE / Li axes           : 별도 post-hoc interface diagnostics
```

⇒ **셋을 하나의 G6 로 묶거나 현재 funnel 에 편입하지 않는다.**

## 4. G5 — 방향은 맞았고 표현이 과장이었다

실제 sweep (`threshold_sensitivity.G5_mechanical`):

```
q        .25   .40   .50   .60   .75   1.00
E_cut   43.4  45.9  46.9  48.1  49.6   58.2
survive    0     1     1     2     4     11
```

- v1 의 *"0→11 전 구간"* 은 **과장**이다. q 0.40–0.60 에서 1–2로 안정적이고,
  **q=1.00 은 E_cut 이 최대값이라 사실상 게이트를 끈 값**이다.
- **컷은 core 11종이 아니라 전체 47종에서 계산된다.**
  47종 median → **WO₃ 1종** / core 11종 median → **CaO·MgF₂·SnO₂·WO₃ 4종**.
- 구현은 선형 percentile 이 아니라 **nearest order statistic** (`int(round(q*(n-1)))`).

⇒ **G5 를 선발 gate 에서 뺀다.** E–G/B 연속축 또는 2D 민감도 패널로만 보여준다.

⭐ **추가로 방향 충돌이 있다** (codex): upstream champion 선정은 **높은 E 를 보상**했는데
G5 는 **낮은 E 를 요구**한다. stiff configuration 을 대표로 뽑아 놓고 soft 하지 않다고
버리는 셈이다.

## 5. 120 순열 강건성은 강건성 증거가 아니다

v1 은 "게이트가 정적 boolean 이라 최종 집합이 순서 불변" 을 **자체 감사 성과**로 적었다.
**고정 Boolean AND 의 교환법칙상 자명하다** — 증거가 아니다.
오히려 **중간 waterfall 이 100종류였다**는 사실이 *단계별 탈락 귀속이 서사 선택*임을 보여준다.
그쪽이 보고할 값이다.

## 6. Q1–Q9 — codex 답 (전부 채택)

| # | 답 |
|---|---|
| Q1 | G1·G2·cathode audit 을 **메인 funnel 단계에서 뺀다.** 옆에 `non-discriminating` / `contained` / `post-hoc` 배지로 둔다 |
| Q2 | **G5 를 선발 gate 에서 제거.** 11종도 **"historical conditional set"** 으로만 보고 |
| Q3 | 하위 계산은 **선택된 구조에 대한 잠정값으로 남길 수 있다.** 다만 **post-anneal 수렴은 미검증**이며, **species 최적 구조나 대표 물성을 보장하지 않는다** (v2 초판의 "조건부로 의미가 있다" 는 §1 과 어긋나 낮춤 — codex 2차) |
| Q4 | 역사 감사·보고 수정에는 **재계산 불필요.** *현재* selection 을 복구할 때만 Stage 02 재수렴 → 재선발 → 바뀐 대표 구조의 하위 계산 갱신 |
| Q5 | G4 unique 6 = **blocking 5 + BVS 1**. 두 독립 수송 신호의 합치가 **아니다** |
| Q6 | 게이트를 더 붙이지 않는다. cathode · SE · Li · Li scavenging 을 **적용범위가 적힌 별도 진단축**으로 둔다 |
| Q7 | 본문은 **47 → G3∩G4 → 11** 까지만. G5 민감도는 별도 패널, 전체 waterfall 은 appendix |
| Q8 | WO₃ 는 *"나쁜 물질"* 의 증거가 아니라 **기존 funnel 이 Li inventory 위험을 놓쳤다는 coverage counterexample** 이다 |
| Q9 | fmax·잔류 force/stress 미기록은 **물리적 원인이 아니라 구조적 관측성 결함**이다. 실제 원인은 **느슨한 수렴 규약**이고, 로깅 누락은 **발견을 늦춘 것** |

## 7. 발표 문장 (확정, codex 제안 채택)

> 큐레이션된 역사 47종에 고정 규칙을 적용하면 산화 안정성과 Li-환경 프록시의 교집합으로
> 11종이 남습니다. 다만 이 수치는 **당시 선택된 구조와 로스터에 조건부인 사후 분류**이며,
> **발견 성능이나 승인 shortlist를 뜻하지 않습니다.** 기계 축은 문턱 민감도로만 보고하고,
> **현재 승인 ranking은 0으로 유지합니다.**

⛔ 금지: "우리 깔때기의 최종 승자" · "47→1 로 걸러냈다" · G5 를 선발 단계로 그리기 ·
`unique_kill` 을 판정 범위 없이 인용 · cathode/SE/Li 를 하나의 G6 로 묶기.

## 8. 남은 것

- **보고·그림 개정** (새 계산 0): 깔때기 그림에서 G1·G2·cathode 를 옆 배지로, 종점 11,
  G5 별도 패널. → 세미나 18·24장.
- **현재 shortlist 복구** (선택): Stage 02 를 `fmax ≤ 0.01` 로 재수렴 → 재선발 →
  대표 구조 하위 계산 갱신. **무겁다. 지금 할 필요는 없다.**
- **Q9 처방**: Stage 02 산출물에 `fmax_setting` · 잔류 force/stress 기록
  (`uma_relax_check.py` L136–139 가 이미 하는 것을 이식).
- ⚠ **manifest 는 우리 repo 에서 일치**한다 — codex 환경 재생성 이슈로 보이나,
  `cascade_screening_funnel.json` 을 다시 만들면 실제로 stale 이 되므로 재생성 시 갱신 필요.

## 관련

- 깔때기 원자료: `db/properties/cascade_screening_funnel.json`
- 기존 인터페이스 축: `db/properties/cascade_stability_axes_verdict.json` (`T9_interface_axes`)
- cathode 상세: `db/properties/cathode_reactivity_verdict.json`
- 부피 판정: `kb/projects/cascade_pipeline_fixes_2026_08_19.md` §5-3 · §6
- G4 분해 코드: `tools/cascade/build_screening_funnel.py` (blocking/BVS 분할 · `pct()`)
- 세미나 소비처: `kb/seminars/cascade_dopant_screening_story_2026_08.md` 18·24장 (미작성)
