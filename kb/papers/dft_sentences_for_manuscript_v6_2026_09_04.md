---
title: "원고 v6 DFT 문장 — 삽입안 + 기존 문장 P0 2건"
date: 2026-09-04
updated: 2026-09-04
tags: [manuscript, dft, sdcp, adsorption, self-doping, citability]
status: 1저자 확인 대기
kind: manuscript-draft
system: sdcp
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-04
verifiedBy: self
explored: false
authoredBy: agent
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 원고 v6 DFT 문장

> 대상: `Manuscript ___ v6.docx` §Results(Figure 2e 문단) · §Methods(DFT calculations)
> 근거: `db/properties/sdcp_neutral_closed_2026_08_28.json` (마감문서 · 허용/금지 서술)
> · `db/properties/sdcp_polaron_pilot_prereg_S0_2026_08_31.json` (자가도핑 명명 규율)
> · `db/properties/lpsocl_box331_...` 무관

---

## ⛔ P0-1 — Figure 2e 문단의 **기전 문장은 우리가 철회한 것**이다

**지금 원고에 있는 문장**

> "The stronger interaction expected for SDCP originates from its **polar sulfonate
> moieties, which can interact more effectively with exposed surface sites** of
> LiNi₀.₈Co₀.₁Mn₀.₁O₂ (NCM811) than non-polar PTFE.[19]"

**마감문서 `⛔_금지_서술` 에 글자 그대로 있다**

> · "'술포네이트가 앵커링한다' · **'극성 작용기가 표면과 상호작용한다' — 기전 근거 없음.**
>   실제 접촉은 C–H ··· 표면 O/Ni 2.44 Å 다"
> · "'술포네이트 O 가 표면 Li 에 배위한다' · 'O···Li 2.09 Å' — 2026-08-29 철회"

**왜 철회됐나** — 좌표를 우리가 직접 재봤다 (`db/structures/sdcp_wave1/sdcp_neutral__*.vasp` 네 자세):

| | 실측 |
|---|---|
| 술포네이트 O ↔ 슬랩 Li | **4.88 – 5.39 Å** (배위 아님) |
| 산성 O–H 의 H ↔ 슬랩 | 7.08 – 7.17 Å |
| **실제 최단 접촉** | **탄소결합 H ··· 슬랩 O/Ni 2.44 – 2.46 Å** |

회신 T P0-1 이 잡았고 우리가 독립 재현했다. **술포네이트는 표면 근처에 있지도 않다.**

⇒ 이 문장은 **고치는 게 아니라 빼야 한다.** 대체안은 아래 §1.

---

## ⛔ P0-2 — Methods 의 **자가도핑 모델 서술**이 사전등록 금지어다

**지금 원고에 있는 문장**

> "the **self-doped form** C₁₁H₁₅O₆S₂ **was obtained by removing a hydrogen atom**,
> leaving a charge-neutral unit with an oxidized backbone compensated by the tethered
> sulfonate group"

**폴라론 사전등록 `대상.⛔_이렇게_쓰지_않는다`**

> "'자가도핑된 SDCP' · '탈양성자화' — **H 원자 제거는 핵과 전자를 함께 뺀 것이고
> 자가도핑 과정 자체를 재현하지 않는다**" (회신 S P0-1)

H 를 떼면 **양성자 + 전자**가 같이 빠진다. 자가도핑은 사슬에서 **전자만** 빠지고 그 양전하를
tethered 술포네이트가 보상하는 과정이다. 둘은 다른 사건이다.

⇒ 모델 자체는 그대로 써도 된다. **"자가도핑을 재현한다" 는 함의만 빼면 된다.** 대체안 §2.

---

## ⚠ 그리고 지금은 **수치를 넣을 수 없다**

마감문서 `허용_서술_이대로만_쓴다.비교`:

> "⏳ **보류 중 — 지금은 쓰지 않는다** (회신 P 7번). reference-equivalence 복구
> (free-spin + LREAL=F 기준) 후에만 승격."

`닫는_근거_체크리스트.격차의_보수성`:

> "복구 전 허용: **'표본 자세 전부에서 SDCP 가 PTFE 보다 더 음수' 라는 부등호 방향
> 서술도 쓰지 않는다** — 절대 E_ads 자체가 보류라서"

⇒ **지금은 방향조차 못 쓴다.** wave1 값(−0.7675 vs −0.4124)이 있어도 보류 상태다.

**언제 채우나** — 그 값을 내는 것이 **C-12 v36** 이다 (2026-09-04 발송, 19잡).
C-12 는 reference-equivalence 문제를 설계로 풀었고(같은 상태선택 정책), 절대 E_ads 와
차를 **둘 다** 보고량으로 비준했다. 반송되면 아래 빈칸이 채워진다.

---

## 1. Figure 2e 문단 — 대체 문안 (빈칸 표기 `[[...]]`)

기존 두 문장(“The stronger interaction expected… than non-polar PTFE.[19] Additional
text related to DFT.”)을 **아래로 교체**한다.

> Density functional theory (DFT) calculations comparing representative SDCP and PTFE
> segments adsorbed on the AM surface are shown in Figure 2e, with the corresponding
> computational models and calculation parameters provided in Figure S3 and Table S1,
> respectively.[28] For the sulfonate-functionalized EDOT repeat unit representing SDCP,
> the calculated adsorption energy on the LiNiO₂(104) surface was **[[E_ads_SDCP]] eV**,
> compared with **[[E_ads_PTFE]] eV** for the C₁₀F₂₂ segment representing PTFE, corresponding
> to a difference of **[[ΔE_ads]] eV**. These energies are single-point values evaluated on
> geometries relaxed with a machine-learned interatomic potential rather than DFT minima,
> and they describe isolated molecular fragments on a clean surface at 0 K; they therefore
> indicate the relative affinity of the two binder chemistries for the oxide surface rather
> than an absolute interfacial binding strength or a prediction of the coverage-dependent
> behaviour in the actual electrode. **The calculated difference reflects the adsorption of
> the fragment as a whole, and the present data do not allow the enhanced affinity to be
> attributed to a specific functional group.** This stronger surface affinity is also
> reflected in the post-mixing morphology. …(이하 기존 문장 유지)

**⚠ 굵은 마지막 문장이 P0-1 의 대체다.** 술포네이트 기전을 주장하지 않으면서, 관측된 것
(조각 전체의 흡착에너지 차)만 말한다.

### 빈칸 채우는 법 (C-12 반송 뒤)

| 빈칸 | 출처 | 조건 |
|---|---|---|
| `[[E_ads_SDCP]]` | `estimand_job_keys.E_C_sdcp − E_S − E_G_sdcp` | 절대값 — **`fixed-geometry` 한정어 필수** |
| `[[E_ads_PTFE]]` | 같은 식, control | 같음 |
| `[[ΔE_ads]]` | `D = (E_C_sdcp − E_G_sdcp) − (E_C_control − E_G_control)` | **차가 절대값보다 신뢰도 높다** |

⛔ 절대값 두 개는 `BASIN_MISMATCH_SLAB` 게이트를 통과해야 쓴다. 게이트가 막으면
**차(ΔE_ads)만** 쓰고 절대값 두 칸은 비운다 — 그때 문장은 "the SDCP segment adsorbed
more strongly by **[[ΔE_ads]]** eV" 로 줄인다.

---

## 2. Methods §DFT calculations — 자가도핑 서술 교체

기존:

> "…and PTFE by a C₁₀F₂₂ segment." **앞의** 괄호 부분
> "(the self-doped form C₁₁H₁₅O₆S₂ was obtained by removing a hydrogen atom, leaving a
> charge-neutral unit with an oxidized backbone compensated by the tethered sulfonate group)"

교체:

> SDCP was represented by its sulfonate-functionalized EDOT repeat unit (C₁₁H₁₆O₆S₂).
> An oxidized model, C₁₁H₁₅O₆S₂, was constructed by removing one hydrogen atom from the
> acidic side chain, giving a charge-neutral open-shell unit in which the oxidized backbone
> is compensated by the tethered sulfonate group. **We note that removing a hydrogen atom
> removes a proton together with an electron and therefore does not reproduce the
> self-doping process itself, in which the backbone is oxidized and the resulting positive
> charge is compensated by the covalently bound sulfonate; this structure is used only as a
> representative oxidized model.** PTFE was represented by a C₁₀F₂₂ segment.

**⚠ 이 단락에는 수치를 넣지 않는다.** wave1 의 doped 항목은 `not_citable` 전건이고
(`sdcp_wave1_citable.json.not_citable`: "sdcp_doped 전 항목"), 폴라론 pilot 은 이제
phase L 이라 값이 없다.

---

## 3. 자가도핑 수치를 쓰고 싶다면 — **지금은 경로가 없다**

| 원한다면 | 필요한 것 | 지금 상태 |
|---|---|---|
| 산화형 SDCP 의 **흡착에너지** | doped 복합체 DFT — C-12 범위 **밖** | 계획 없음 |
| 산화형의 **전하 국재(spin share)** | 폴라론 S0 pilot | phase L 진행 중 · seeds·probe·S 잠김 |

⇒ v6 에서 자가도핑은 **분광학적 근거(Figure 2d FT-IR)로만** 말하는 것이 맞다.
지금 원고 §47 이 이미 그렇게 쓰고 있다 — *"The coexistence of these bands indicates that
the tethered sulfonic acid side chains are partially dissociated… consistent with the
self-doped conducting character of SDCP.[36]"* **거기까지가 근거 있는 서술이다.**
DFT 로 자가도핑을 뒷받침하려 하면 §2 의 금지에 걸린다.

---

## 4. Figure 2e 캡션

현재: "(e) DFT." — 채워야 한다.

> (e) Calculated adsorption energies of representative SDCP and PTFE segments on the
> LiNiO₂(104) surface used as a model for NCM811.

⛔ 캡션에 "sulfonate anchoring" · "polar interaction" 을 쓰지 않는다 (§P0-1).

---

## 5. 1저자가 결정할 것

1. **P0-1 문장을 뺄지** — 대체안(§1)으로 갈지, 아니면 Figure 2e 를 C-12 반송까지 미룰지
2. **P0-2 교체 문안** 수용 여부
3. C-12 반송 시 **절대값을 쓸지 차만 쓸지** — 게이트 결과에 달렸지만 방침은 미리 정하는 게 낫다
