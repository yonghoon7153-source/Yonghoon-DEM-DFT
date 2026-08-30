---
title: "회신 AC 요청 — 원고 v6 · SI v6 대조 (Methods/Table v8)"
date: 2026-08-30
updated: 2026-08-30
tags: [review, codex, manuscript, sdcp, dem, dft, table-s1, table-s3]
status: 발송전
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

# 회신 AC 요청 — 원고 본문·SI 를 우리 정본에 대조한 결과가 맞나

## 0. 무엇을 봐 달라는 것인가

공저자에게 나갈 교체안 **`docs/manuscripts/methods_and_tables_v8_for_coauthors.md`** 를
적대적으로 읽어 달라. 이것은 계산을 새로 하자는 제안이 아니라 **이미 있는 정본과
이미 쓰여 있는 원고를 대조한 결과**다. 그래서 물어야 할 것은 하나다 —
**대조가 맞나, 그리고 고치라고 한 것을 고치면 원고가 실제로 방어 가능해지나.**

⛔ 이 리뷰가 **하면 안 되는 것**: 새 계산 제안, 새 지표 제안, "이것도 재면 좋겠다".
캠페인이 이미 그것 때문에 여덟 번 반려됐다.

## 1. 배경 — 정본이 두 브랜치에 갈려 있다

| 축 | 정본 | 브랜치 |
|---|---|---|
| DEM/MPM/복셀 수송 (Table S2·S3, Figure 4, Methods 시뮬) | `manuscript-track` 브랜치 `docs/reviews/` 안의 `table_s3_data_20260827.md` · `manuscript_state_20260830.md` | `manuscript-track` |
| DFT (Table S1, Figure 2e, Methods DFT) | `db/properties/sdcp_wave1_citable.json` · `sdcp_neutral_closed_2026_08_28.json` | `claude/friendly-meitner-lldvar` |

v8 문서는 **둘을 옮겨 적은 것**이다. 어긋나면 정본이 이긴다.

## 2. 판정해 달라 — 여덟

### Q1. **DFT 트랙이 둘이라는 진단**
v8 §4 는 *"QE(Phase-B Δ 5잡, 지금 도는 중, 0/5 수렴)와 VASP(wave1, 인용 보류)가 둘 다
살아 있고, 원고는 Figure 2e 가 어느 쪽인지 선언해야 한다"* 로 적는다.
SI v6 Table S1 은 QE 파라미터(60/480 Ry · 1e-6 Ry · AFM net 0)를 적는데,
지금까지 인용 후보로 다뤄온 값(`sdcp_wave1_citable.json`)은 VASP PAW 산출이다.
**이 진단이 맞나?** 그리고 *"둘 중 어느 쪽도 지금 Figure 2e 를 채울 수 없다"* 가
과한 판정인가?

### Q2. **금지 서술 삭제가 과잉교정인가**
본문 34 의 *"The stronger interaction expected for SDCP originates from its polar
sulfonate moieties, which can interact more effectively with exposed surface sites"* 를
**삭제**하라고 적었다. 근거: `sdcp_neutral_closed_2026_08_28.json` 의 금지 목록
(*"술포네이트가 앵커링한다" · "극성 작용기가 표면과 상호작용한다" — 기전 근거 없음.
실제 접촉은 C–H ··· 표면 O/Ni 2.44 Å*), 그리고 `O···Li 2.09 Å` 는 2026-08-29 철회
(실측 4.88–5.39 Å).
그런데 원문은 *"expected"* 로 완화돼 있고 기전 **주장**이 아니라 **동기 서술**로도 읽힌다.
**삭제가 맞나, 아니면 "가설로 명시" 가 맞나?** 후자라면 정확한 문구를 달라.

### Q3. **σ_ele 의 단위가 바뀐다**
v6 SI Table S3: `σele_eff 1.98 / 3.00 **S cm⁻¹**`.
새 정본: `72.3 / 81.3` 또는 `54.0 / 70.6` **mS cm⁻¹** — **27~40배 낮다**.
v6 값은 철회 세대(vox 0.4 µm · SDCP E 23.6 · PTFE E 0.30)의 산출이고 `quotation_ban` 등재분이다.
**v6 의 1.98/3.00 이 옳을 수 있는 독법이 하나라도 있나?** 없으면 그렇게 말해 달라 —
공저자가 "왜 갑자기 40배 줄었냐" 를 반드시 묻는다.

### Q4. **CBD 접촉 수 433 → 74 (5.8배)**
본문이 직접 인용하는 문장(*"increases from 433 for the SBE to 517 for the DBE"*)이
새 침대에서 **74 → 86** 으로 재현된다. 방향(+16.2 %)과 상대크기(v6 +19.4 %)는 정합인데
절대값이 5.8배 다르고 **v6 이 무엇을 셌는지 기록이 없다.**
게다가 규약이 이득을 바꾼다 — 절연 PTFE 를 "conductive binder domain" 에 넣으면 80 → 88 (+10.0 %).
**이 문장을 절대값과 함께 유지할 수 있나, 아니면 "denser distribution of contacts" 같은
정성 서술로 내려야 하나?**

### Q5. **Areal capacity 를 `n/a` 로 비우는 것**
근거: 두 전극이 **같은 AM scaffold**(n_AM 1271 · seed_AM_frac 45.68 % 동일)와 **같은 정지
두께**(72.534 µm)를 쓰므로 면적용량이 다를 수 없다. 면적하중은 `0.015904 g cm⁻²` 로 확정되고
여기 곱할 **비용량이 원고 어디에도 없다** (SI 의 3.11 을 재현하려면 195.5, 3.07 은 193.0 mAh g⁻¹).
**이 논증이 빈틈없나?** SI 의 두 값이 서로 다른 이유로 정당화될 여지가 있나?

### Q6. **R_ele 비를 시뮬과 대조하지 말라고 한 것**
측정 R_ele: SBE 59.68 → DBE 48.48 Ω cm² ⇒ 전도도 비 **1.231**.
시뮬 두 규약: **1.124**(PTFE 생략) · **1.308**(centerline 제외).
v8 은 *"측정값이 두 규약 사이에 든다" 로 쓰면 안 된다* 로 적었다. 근거 둘:
(ⓐ) R8 Q2 가 bracket 해석을 철회했다, (ⓑ) R_ele 는 솔버에 없는 접촉저항을 포함한 **다른 관측량**이다.
**이 금지가 옳나?** 옳다면, 본문 40 의 *"consistent with the enhanced σ_ele predicted by
the DEM simulations"* 는 어디까지 쓸 수 있나 (방향만? 그것도 안 되나?).

### Q7. **모델 대표성 — 중성 단량체 vs 도핑된 고분자** (v8 §8-1b)
분광 판정은 실물 SDCP 가 **자가도핑** 상태라고 한다 (O–H 부재 · S–O 1.495/1.498/1.496 완전등가 ·
⟨S²⟩ 0.755). 그런데 인용 가능한 흡착 모델은 **중성** `C₁₁H₁₆O₆S₂` **단량체**다.
그리고 스핀 분배가 사슬 길이에 의존한다 — SO₃ 몫이 monomer 65 % → dimer 62.3 → trimer-end 54.6
→ **trimer-mid 42.3 (백본 50.1 로 역전)**.
**이 간극이 reference-equivalence 를 고친 뒤에도 Figure 2e 를 못 쓰게 만드나?**
아니면 Table S1 각주 한 줄로 처리 가능한가? 우리 판단은 후자인데 자신이 없다.

### Q8. **우리가 놓친 것**
v6 본문·SI 를 직접 읽고, v8 이 **안 잡은** 결함을 찾아 달라. 우리가 잡은 것:
본문 62 의 복셀 문장 **중복**, *"then seeded into the pore space"*(압밀 도중이 맞다),
~10 % / 11–12 % 출처 오기, *"paired mean with its standard error"*(자유도 0),
*"reconstructed"*(토모그래피로 읽힌다), 자리표시자 3곳(`Additional text related to DFT.` ·
`(e) DFT.` · `Figure S3. DFT`).

## 3. 대조에 쓴 원문

- 원고 v6 본문: 34(DFT) · 39·40(DEM) · 59–61(Methods DFT) · 62–66(Methods DEM) · 139·143(캡션)
- SI v6: Table S1(DFT 파라미터) · S2(DEM 파라미터) · S3(구조·수송) · S4(EIS TLM)
- Methods v7 공저자용 docx (`manuscript-track:3e6aab4a` 스냅샷 — 그 뒤 커밋 10개가 더 붙었다)

## 4. 형식

Q1–Q8 각각에 **P0/P1/P2 + 한 줄 판정 + 근거**. 마지막에 GO / NO-GO 하나.
NO-GO 면 **해제조건을 번호로** 달라.
