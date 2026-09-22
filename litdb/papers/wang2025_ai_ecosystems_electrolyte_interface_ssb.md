<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-09-22 신규 작성. 1저자 지정 읽기축:
       ⭐ 이 논문을 구한 단 하나의 이유 = `wu2026_ml_driven_electrolyte_interface_design_review` 의
         `Fig. 10` 이 **이 논문 `Fig. 1` 의 재수록**이고, 그 digest 가 *"우리에게 제일 값있는 한 장"*
         이라고 적었다. **CEI 4조건의 원문 정의를 2차 인용이 아니라 원전에서 가져오는 것이 1번 임무.**
       ⇒ 그 외 축: hull 스크리닝 비판 · "AI ecosystem" 의 실체(논지냐 결과냐) · SEI/CEI 비대칭 ·
         Zeier 색채 · 인용 가능한 문턱값 · 우리 §D/§2b/§E 선행연구 검사.
     크로핑 10장 전부 확보(자동 크로퍼가 Fig. 1·2 를 놓쳐 손으로 bbox 지정) 중 **6장을 실제로 봤다** — 목록은 §0c. -->

# Toward AI Ecosystems for Electrolyte and Interface Engineering in Solid-State Batteries — Wang, Zeier, You (*Sci. Adv.* **11**, eaea0638 (2025))

> slug `wang2025_ai_ecosystems_electrolyte_interface_ssb` · DOI `10.1126/sciadv.aea0638` · type `review (자체 계산 0 · 자체 실험 0 — 전량 2차 인용 + 저자 제안)` · PDF `litdb/inbox/127. SciAdv_2025_Wang_Zeier_You_Toward_AI_ecosystems_electrolyte_interface_SSB_MAIN.pdf` (본문 **27 pp** · Fig 1–10 · 본문 표 0장 · refs **196** · SI = **Tables S1–S5 별도 PDF, 우리 미확보**) · digested `2026-09-22` · status ✅ · 태그 **[외부·리뷰]**

> elements: Li, P, S, Cl, Br, I, F, O, N, La, Zr, Hf, Co, Ni, Mn, Ge, Si, Ti, Sc, Nd, Y, Er, In, Al, B, H, Na, Se, C
> methods: DFT, AIMD, MD, MLIP, ESW, elastic, XPS

> ⚠ **`methods:` 는 이 리뷰가 *소개하는* 기법이다 — 저자들은 계산을 한 건도 수행하지 않는다.**
> ⛔ **리뷰다. 이 파일의 수치는 전부 2차 인용이다.** 값마다 원 출처(ref 번호 + 저자·연도·저널)를 붙였다.
> 우리 원장(`db/properties/*`)에 이식 금지. `comparison_vs_ours.md` **물성 4축(A–D)에도 넣지 않는다** — 방법 축(J)과 §H 에만 둔다.
> ✅ **talk 역링크 점검함**: `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `lee2026_skku_mlip_materials_design.md` 하나뿐이고, 그 대기열(#1–#9, MTP/SevenNet/SKKU 계열)에 이 논문은 **없다**(`Zeier`·`AI ecosystem`·`aea0638`·`Fengqi You` 전수 0건). ⇒ 역링크 작업 없음.

> **저자**: **Zhilong Wang**¹²³, **Wolfgang G. Zeier**⁴⁵, **Fengqi You\***¹²³
> ¹ Cornell University AI for Science Institute · ² Cornell College of Engineering · ³ Cornell AI for Sustainability Initiative (CAISI), Ithaca, NY
> ⁴ Institute of Inorganic and Analytical Chemistry, University of Münster · ⁵ Institute of Energy Materials and Devices, IMD-4 Helmholtz-Institute Münster, Forschungszentrum Jülich
> 교신 `fengqi.you@cornell.edu` · 투고 **2025-06-24** / 수락 2025-10-29 / 게재 **2025-11-26** · Sci. Adv. 11(48)
> 연구비: Eric and Wendy Schmidt AI in Science Postdoctoral Fellowship (Schmidt Sciences, LLC) — **부분 지원 1건뿐**
> 다운로드 워터마크: **한양대 ERICA 학술정보관, 2026-09-21** (1저자가 받은 경로) · CC BY 4.0

---

## 0a. 이 digest 를 읽는 법 — **왜 이 논문을 구했는가**

우리는 이 논문을 **`Fig. 1` 한 장 때문에** 구했다. `wu2026_ml_driven_electrolyte_interface_design_review`
digest 가 그 그림(거기서는 `Fig. 10` 으로 재수록)을 *"이 리뷰에서 우리에게 제일 값있는 한 장"* 이라
적었고, 그 이유는 **CEI 칸이 요구하는 조건 목록이 우리 빈칸 표를 그대로 만들어 주기 때문**이다.
2차 인용으로는 그 표를 못 세운다 — 그래서 원전을 열었다.

**§1 임무의 결과부터**: 원전을 열어 보니 **세 가지가 달랐다.**

| 우리가 믿고 있던 것 | 원전 실물 (`Fig. 1` 실독) |
|---|---|
| SE 설계 **5축** | ❌ **4축**이다 — 이온-전자전도 / 전기화학안정 / 기계강도 / 공기·습도안정 |
| 4축이 **좌 SEI / 우 CEI 로 갈라진다** | ❌ **안 갈라진다.** 물결 화살표 두 개가 중앙 "Solid electrolyte design" 타원에서 좌·우로 뻗어 4 박스 사이를 **엮으며 지나갈 뿐**이고, 캡션은 *"…these factors … **to address key scientific problems associated with SEI/CEI**"* 라고 **넷 다 양쪽에 쓰인다**고 적는다. 배치는 조판이지 분할이 아니다 |
| CEI 4조건 | ✅ **맞다** — Decomposition and side reactions / Electronic leakage / Volume change / Pressure change. **단 SEI 는 4가 아니라 5** 이고 목록이 대칭이 아니다 |

⇒ **우리 §7 빈칸 표는 "CEI 4칸" 위에 세우는 것이 맞지만, 그것을 "SE 설계 5축의 우측 분지" 로
소개하면 원전과 어긋난다.** 이 정정을 `wu2026…` digest 쪽에도 남겼다(§0d).

그 외 이 digest 가 본체로 삼는 것:

1. **CEI 4조건의 "측정량" 추적** (§5) — `Fig. 1` 은 **불릿 목록일 뿐 정의가 아니다**. 네 칸 각각이
   본문 어디서 어떤 물리량으로 조작화되는지(또는 안 되는지)를 전수로 캤다. ★ 1번 임무
2. **hull 기반 열역학 스크리닝 비판** (§6) — 우리 방법이다. 이 리뷰에 **명시적 비판 문장이 있고**,
   `Fig. 7D` 가 그것을 **그림으로 증명**한다. 우리에게 유효한가까지 판정
3. **"AI ecosystem" 의 실체** (§7) — 논지인가 결과인가. **구현 사례를 분야별로 갈랐다**
4. **SEI vs CEI 비대칭** (§8) — 우리가 CEI 만 하는 선택의 근거가 여기 있나
5. **Zeier 색채** (§9) — 실험 쪽이 계산에 무엇을 요구하나. ⚠ **저자기여 표기가 이 질문의 답을 바꾼다**
6. **인용 가능한 문턱값·분류체계** (§10)
7. **우리 §D / §2b / §E 의 선행연구 검사** (§11) — ⭐ **§E 가 걸렸다**

## 0b. 🔁 중복 지도 — **이 대목은 이미 우리 digest 가 있다** (여기서 반복 서술하지 않는다)

| 이 리뷰의 대목 | 이미 다루는 우리 digest | 한 줄 |
|---|---|---|
| `Fig. 9A` 양극 코팅 스크리닝 깔때기 (ref 160) | **`xiao2019_cathode_coating_screening.md`** | **우리 digest 가 원전을 SI 까지 전수 파싱**했다 (106종 ESW 표·NEB hop 전량·할라이드 F/Cl 분기). 리뷰는 깔때기 그림 하나로 압축한다 — **원전이 압도적으로 낫다**. 여기서는 **문턱값만** 재확인한다(§10) |
| 계면 안정성 일반론 · grand-potential 원리 | `richards2016_interface_stability_pseudobinary.md` · `xiao2020_interface_stability_ssb_review.md` · `zhu2015_esw_grand_potential_origin.md` · `nolan2018_computation_accelerated_design_review.md` | **우리 축 B 의 정본 4편.** 이 리뷰는 그 계보를 **인용조차 하지 않는다**(§12-③) |
| Sendek 12,831 스크리닝 (`Fig. 4A`, ref 88·89) | `sendek2017_ml_screening_12k_conductors.md` | 원전 확보됨 |
| 계면 병목 · SEI/CEI 리뷰 | `liang2026_interface_bottleneck_solid_state_batteries.md` · `miao2023_role_of_interfaces_solid_state_batteries.md` · `kim2021_review_oxide_sulfide_se_interfaces.md` | — |
| 할로겐 화학 (Cl/Br/I 치환) | `he2023_halogen_chemistry_solid_electrolytes.md` | 리뷰는 할라이드를 스치기만 한다 |
| a-LiF 코팅 임계두께 ≈1 nm (ref 139 Hu) | `wu2026_ml_driven_electrolyte_interface_design_review.md` §10-② | **두 리뷰가 같은 원전을 인용**한다. 오차막대 비판은 그쪽 digest 에 있다 |
| MLFF 일반론 · uMLIP · 파인튜닝 | `makino2026_mlip_battery_materials_review.md` · `liu2026_finetuning_umlip_tutorial.md` · `chang2026_performance_based_mlip_selection_sse.md` 외 | 이 리뷰의 MLFF 절은 얕다 |
| 능동학습 폐루프 | `cho2025_multicompositional_argyrodite_experimental_active_learning.md` · `hu2026_foundation_model_surrogates_active_learning.md` 외 | — |
| ML 파이프라인 지형 | **`jain2026_ml_pipelines_solid_state_electrolyte_design.md`** | ⭐ **같은 그룹의 자매편이다** — V. Jain, **Z. Wang, F. You\*** (Cornell), *Mater. Horiz.* 13(1), 15–44 (2026). **제1·2저자와 교신이 겹친다.** 그쪽은 **ML 파이프라인의 4단 구조 + 6단 HTVS 깔때기**(`Fig. 3`)를 더 깊이 쓰고, 이쪽은 **계면(SEI/CEI)** 을 더 깊이 쓴다. ⚠ **두 편을 독립 근거 2건으로 세지 마라** — 같은 그룹·같은 해·겹치는 저자다 |
| dual compatibility (할라이드 코팅) | `cha2024_dualcompatible_halide_ncm_lpscl_interface.md` | ⚠ **단, 이 리뷰의 dual-compatibility 문장은 cha2024 와 다른 층위다 — §11 에서 따로 다룬다** |

⇒ **위 행들은 이 digest 에서 다시 쓰지 않는다.** 아래 §5–§12 만이 새 정보다.

## 0c. 🖼 실제로 본 그림 / 안 본 그림 (2026-09-22)

크로핑 **10장** (`litdb/figures/wang2025_ai_ecosystems_electrolyte_interface_ssb/`, 본문 그림 10장 전부 · 본문 표 0장).

> ⚠ **크로퍼 수작업 2건**: 자동 추출기가 `Fig. 1`·`Fig. 2` 를 *"영역 없음"* 으로 제외했다
> (전폭 벡터 도식이라 캡션 위 블록 높이를 못 잡는다). **손으로 bbox 를 지정해 넣었다**
> — `fig_1` (p2, clip 36,55,560,341) · `fig_2` (p3, clip 36,415,560,675). 또 `Fig. 2·4·6·8·9`
> 는 **패널 A 가 잘려 있어** 상단을 그래픽 실제 경계까지 확장해 재렌더했다. `figures.json` 에
> `note` 로 남겼다. **`--clean` 으로 재추출하면 이 5장이 다시 잘린다.**

**본 것 6장** — `Fig. 1` `Fig. 6` `Fig. 7` `Fig. 8` `Fig. 9` `Fig. 10`
(= 우리 축에 걸리는 전부: CEI 요구목록 · 기계/스크리닝 문턱 · 반응성 3분법 · E_hull–K* 공간 · 코팅 깔때기 · CEI 모델링).

**안 본 것 4장** — `Fig. 2`(리뷰 전체 구조 개념도 — 목차의 그림판) · `Fig. 3`(전통 vs AI 워크플로 개념도) ·
`Fig. 4`(고속이온전도체 발굴 3방법 — **Sendek/IonML/BV-GCN, 전부 기존 digest 또는 우리 축 밖**) ·
`Fig. 5`(미세구조/XRD/GNoME — `ou2026…`·`sendek2017…` 및 GNoME 별도 축과 중복).

그림에서만 읽은 값은 **`figure-read ≈`** 로 표시했다. 본문 서술과 **어긋난 것 3건**은 §12-①②③ 이다.

## 0d. 🔗 `wu2026_ml_driven_electrolyte_interface_design_review` 로 되돌리는 정정

그 digest §5(Figure set) 의 `Fig. 10` 행과 §8-② 는 이 그림을 *"SE 설계 5축이 좌 SEI / 우 CEI 로 갈라진다"* 로
읽었다. **원전 실독 결과 축은 4개이고 갈라지지 않는다**(§0a 표). **CEI 4칸 자체는 정확하므로
§8-② 의 자백 전략은 그대로 유효**하다 — 소개 문장만 고치면 된다. 그 digest 파일에 정정 주석을 넣었다.

---

## 1. 한 줄 요약

**Cornell 의 AI/공정시스템 그룹(Fengqi You)이 쓰고 Zeier 가 편집으로 얹힌 27 pp 리뷰**로,
SSB 의 전해질·계면 설계에 AI 를 어떻게 쓰고 있는지를 **세 가지 양식**(① 구조-물성 스크리닝 파이프라인
② MLFF 기반 MD ③ 생성모델 역설계)으로 정리한 뒤, **미해결 3 + 처방 3** 으로 닫는다.
제목의 "AI ecosystem" 은 **결과가 아니라 제안**이고 — 저자들 스스로 *"the field of SSBs still lacks
such intelligent research infrastructure"* 라고 적는다 — SSB 분야의 구현 사례는 **0 건**이다.
**우리에게 값있는 것은 딱 세 곳**: `Fig. 1` 의 CEI 요구 4칸 · ref 133 의 **"열역학 기반 판정이 물질을
불안정으로 오분류해 왔다"** 문장과 그것을 그리는 `Fig. 7D` · 그리고 우리 §E 를 이름까지 똑같이
선언해 놓은 **"dual compatibility" 한 문장**.

## 2. 메타 / 이 리뷰가 자기를 어디에 놓나

| 항목 | 내용 |
|---|---|
| 저널·형식 | *Science Advances* **Review** (ENGINEERING) · 27 pp · 본문 표 0장(전부 SI) |
| 자체 데이터 | **없다.** 계산 0 · 실험 0. 식 (1)–(8) 은 전부 **일반식 재기술**(단일/다목적 최적화, MLFF 에너지 분해, 메시지 패싱, 어텐션, 힘=−∇E, 결합손실) |
| 선행 리뷰와의 차별 선언 | **table S1**(우리 미확보)에 선행 리뷰 목록을 두고, 본문은 *"there are currently relatively few comprehensive discussions on **AI-driven** SE and interface design"* 로 자기 자리를 잡는다. 이유 2가지를 제시: ① 실험·계산 통합이 부족하고 AI 가 독립 분과로 남아 데이터가 희소 ② SSB 실험 장비가 비싸 상용화·진보를 막는다 |
| 저자 기여 (⚠ 중요) | Conceptualization **Z.W., F.Y.** · Methodology **Z.W., F.Y.** · Investigation **Z.W., F.Y.** · Visualization **Z.W.** · Supervision **F.Y.** · Writing-original draft **Z.W., F.Y.** · **Writing—review and editing: W.G.Z., F.Y.** ⇒ **Zeier 는 원고 검토·편집에만 이름이 있다.** §9 에서 이 사실이 판정을 바꾼다 |
| SI | Tables S1–S5 (S1 선행리뷰 · S2 MLFF 툴킷 · S3 생성모델 · S4 이온전도 예측모델 · S5 SEI/CEI AI 연구). **우리 미확보** — 본문이 다섯 번 참조하지만 내용은 못 본다 |

## 3. 문서 구조 (본문 절 지도)

| 절 | 쪽 | 무엇 | 우리 축 |
|---|---|---|---|
| INTRODUCTION | 1–3 | SSB 도전과제 → AI 기회 → 지식격차 | `Fig. 1` ★★★ |
| AI strategies for electrolyte and interface design | 4–7 | 식 (1)–(8) · 3 양식 선언 | `Fig. 2`·`Fig. 3` |
| — Establishing screening pipeline | 4–5 | DB·서술자·툴킷·데이터 가드레일 | — |
| — Performing MD based on MLFFs | 6 | MLFF 수식·가속비·DOAS | — |
| — Designing materials based on generative models | 6–7 | PGCGM/CDVAE/MatterGen/GPT-폴리머 | — |
| Discovery of high-performance SEs | 7–12 | 이온전도 / 기계강도·안정성 | `Fig. 4`·`Fig. 5`·`Fig. 6` |
| AI-driven optimization for SEI/CEI | 12–19 | **SEI 5 pp + CEI 3 pp** | `Fig. 7`–`Fig. 10` ★★ |
| — Advances in SEI chemistry (high-capacity anodes) | 12–16 | LASP/SSW-NN · **반응성 3분법** · XPS 예측 · K_crit · E_hull–K* | `Fig. 7`·`Fig. 8` ★★ |
| — Advances in CEI chemistry (high-voltage cathodes) | 16–19 | 코팅 요구조건 · Xiao 깔때기 · LOTF-MD · a-LiF · CALYPSO · n2p2 · M3GNet | `Fig. 9`·`Fig. 10` ★★★ |
| Limitations and potential solutions | 19–22 | 한계 3 + 방향 3 | — |
| DISCUSSION | 22–23 | 요약 + **0–2 / 2–5 / 5+ 년 로드맵** | — |

---

## 4. `Fig. 1` 전사 — **원전 실물, 한 글자도 안 바꿈** ★★★

> **실독 2026-09-22.** 캡션: *"**Fig. 1. Key scientific goals and challenges for SE and SEI/CEI design.**
> The factors that have to be considered for the SE design are demonstrated, including ionic-electronic
> conductivity, electrochemical stability, mechanical strength, and air/humidity stability, **to address key
> scientific problems associated with SEI/CEI**. This review aims to provide comprehensive AI-driven
> applications in SE design and SEI/CEI optimization. The anode, cathode, and SE are shown figuratively
> and do not represent their actual structures."*

**중앙 — "Solid electrolyte design" 타원. 그 주위에 4 박스 (2 위 / 2 아래):**

| SE 설계 축 | 불릿 (원문 그대로) |
|---|---|
| **Ionic-electronic conductivity** | • Ionic conductivity • Electronic conductivity • Disorders, strain, and glass-crystal phase |
| **Electrochemical stability** | • Thermodynamic stability • Electrochemical window • **Electronic leakage** |
| **Mechanical strength** | • Shear and bulk moduli • Compressive and tensile strength • Crack resistance |
| **Air/humidity stability** | • Hydrophilicity • Air sensitivity • Environmental stability |

**좌우 회색 타원 — 계면 문제 목록:**

| | 불릿 (원문 그대로) |
|---|---|
| **SEI** (좌, **5개**) | • Multiphase structure • Ion migration • Electronic conductivity • Volume change • Pressure change |
| **CEI** (우, **4개**) | • **Decomposition and side reactions** • **Electronic leakage** • **Volume change** • **Pressure change** |

**그림 실독에서만 나오는 관찰 3가지** (캡션·본문에 없다):

1. **SEI 5 ≠ CEI 4.** SEI 는 *구조·수송* 중심(다상구조·이온이동·전자전도), CEI 는 *반응* 중심
   (분해·부반응·전자누설). 공통은 **부피변화·압력변화** 둘뿐이다.
2. **같은 물리에 이름이 둘이다** — SEI 는 `Electronic conductivity`, CEI 는 `Electronic leakage`.
   그리고 `Electronic leakage` 는 **SE 설계축(전기화학안정)에도 들어 있다.** 즉 전자누설은
   **벌크 SE 성질이자 CEI 성질**로 두 번 센다. ⚠ 우리가 밴드갭으로 이 칸을 채운다고 말할 때
   **어느 쪽 칸인지 명시해야 한다** — 벌크 SE 갭(우리가 가진 것)과 CEI 상의 갭(우리가 없는 것)은 다르다.
3. **물결 화살표는 분할선이 아니다.** 중앙 타원에서 좌·우로 물결치며 4 박스 사이를 지나 SEI/CEI 로
   꽂힌다. 4 축 중 어느 것이 SEI 전용이고 어느 것이 CEI 전용이라는 표시는 **그림에도 캡션에도 없다**.

**서론 본문이 같은 목록을 산문으로 반복하는 대목** (p1, `Fig. 1` 직전·직후):
- *"interfacial stability, particularly at the SEI (17–20) and CEI (21, 22) (`Fig. 1`), is the key for SSBs.
  The compositions, structures, and **coupled ionic-electronic conductivities** of SEI/CEI dictate the
  electrochemical kinetics of Li⁺ transport, yet their **evolution under electrochemical cycling and
  mechanical stress** requires systematic investigation"*
- *"The formation of **space-charge layers**, **pressure-induced phase transformations**, and
  **interphase growth kinetics** further complicate Li⁺ transport, leading to nonuniform current
  distributions and potential dendrite penetration pathways."*
- *"In addition, **volumetric fluctuations at the interfaces** introduce further challenges, as local
  stress concentrations can induce mechanical failure or exacerbate interfacial instability."*

## 5. ★★★ CEI 4조건 — **"어떤 물리량으로 재는가" 를 본문 전수로 추적** (1번 임무)

> ⚠ **먼저 정직하게**: `Fig. 1` 은 **불릿 목록이지 정의가 아니다.** 네 칸 중 **본문에 조작적 정의
> (측정량 + 문턱)가 있는 것은 1번뿐**이고, 2번은 대리변수만, 3·4번은 **서술어만 있고 측정량이 없다**.
> 아래 표의 "이 논문이 실제로 주는 것" 열이 그 실상이다. **없는 것을 있는 것처럼 우리 §7 에 옮기면
> 안 된다** — 오히려 "원전도 정의하지 않은 칸" 이라는 사실이 우리 변론이 된다.

| # | CEI 조건 (원문) | 이 논문이 **실제로** 주는 조작화 | 출처 위치 | 문턱값 | 우리 현황 |
|---|---|---|---|---|---|
| **1** | **Decomposition and side reactions** | ✅ **있다, 둘.** ⓐ `ΔE_rxt` = *"the **reaction energy** of the material with the cathode or electrolyte in eV/atom"* (`Fig. 9` 캡션, LPS = Li₃PS₄ · NCM = LiNi₁ᐟ₃Co₁ᐟ₃Mn₁ᐟ₃O₂ 만충) ⓑ `ΔE_rxn` = *"**chemical mixing energy** with other battery components by DFT calculations"* (`Fig. 7D` 캡션) | `Fig. 9A` Filter 4 · `Fig. 7D` | **ΔE_rxt ≥ −0.1 eV/atom** (Xiao/Ceder 게이트) | ✅ **우리가 계산하는 유일한 칸.** comp1\|LiCoO₂ **−0.3227 eV/atom** — **게이트를 3.2배 초과해 탈락**한다 (⇒ §13-①) |
| **2** | **Electronic leakage** | 🟡 **대리변수만.** 측정량은 *"the **electronic conductivity** of the SEI determines the growth kinetics with faster growth led by more pronounced electronic transport"* (ref 151) — 즉 **σ_e** 다. 하지만 스크리닝에서는 전부 **band gap 대리**로 친다. 그리고 갭 문턱이 **본문 안에서 세 개로 갈린다**: `E_g > 0.5 eV`(`Fig. 9A` Filter 1) · `bandgap > 1 eV`(식 (1) 예시 목적함수) · `ML bandgap > 3 eV`(`Fig. 6E`) · MatterGen 문맥 `> 3.0 eV` | p.16 · `Fig. 9A` · `Fig. 6E` · 식 (1) | **0.5 / 1 / 3 eV 셋이 공존 — 합의 없음** | 🟡 **갭만 있다** (comp1 2.066 / modelc 2.099 eV, fixed-occ nscf). ⚠ **PBE 값이라 0.5·1 eV 는 통과, 3 eV 는 탈락.** 그리고 우리 갭은 **벌크 SE** 것이지 **CEI 상** 것이 아니다 — §4-② |
| **3** | **Volume change** | ❌ **측정량 없다.** 서술어만: *"**volumetric fluctuations at the interfaces** introduce further challenges, as local stress concentrations can induce mechanical failure or exacerbate interfacial instability"*(서론) · *"Silicon anodes … undergo **volume changes** during cycling, leading to SEI rupture and reformation"*(SEI 절, **양극이 아니라 Si 음극**) · `Fig. 8F` 의 ML 입력에 *"Composition, **energy, volume**"* 이 들어가지만 **CEI 부피변화와 연결하지 않는다** | 서론 · p.12 · `Fig. 8F` | **없다** | ⛔ **0 건.** 우리 EOS(V₀ 254.16 / 243.29 Å³·fu⁻¹)는 **벌크 상태방정식**이지 충·방전 부피변화가 아니다. 이식 금지 |
| **4** | **Pressure change** | 🟡 **다른 계에만 있다.** CEI 맥락 서술은 *"**pressure-induced phase transformations**"* 한 줄뿐. **정량 틀은 SEI 절에 있다** — `K_eff`(effective local moduli, GPa) vs `K_crit`(임계 모듈러스): *"When K_eff < K_crit … this SEI continues to react and grow into an unknown phase. Conversely, when K_eff > K_crit, the interface remains structurally intact"* + ML 로 예측한 `K*` | p.14 (`Fig. 8C,D`) · p.15–16 (`Fig. 8E–G`) | **K_eff vs K_crit 부등식** (절대 문턱은 계마다 다름) | ⛔ **0 건.** 우리 B₀·E_VRH(comp1 26.23 / 22.06 · modelc 21.71 / 27.66 GPa)는 **벌크 탄성**이지 계면 구속 모듈러스가 아니다. ⚠ **단 `K_eff`–`K_crit` 틀 자체는 우리가 쓸 수 있다** — §13-④ |

### 5b. 이 표에서 나오는 판정 3가지

- **⭐ 우리 빈칸은 3/4 가 아니라 "1칸 완전 + 1칸 절반 + 2칸 공백"이다.** 그리고 **2·3·4번은 원전조차
  측정량을 못 박지 않았다** — 특히 3번(부피변화)은 **CEI 맥락의 정량 틀이 이 논문에 아예 없다**.
  ⇒ 원고 §Limitations 문구는 *"우리는 3칸을 안 했다"* 가 아니라
  ***"이 4칸 중 정량 기준이 확립된 것은 분해·부반응 하나이고, 우리는 그것을 계산한다.
  전자누설은 갭 대리로 부분적이며, 부피·압력 변화는 문헌에도 CEI 용 기준량이 없다"*** 로 써야 정확하다.
- **⚠ 전자누설 칸은 "갭 하나로 채웠다" 고 말할 수 없다.** 원전의 측정량은 **σ_e** 이고, 갭은 대리다.
  게다가 문턱이 0.5/1/3 eV 로 **세 갈래** — 우리 2.07–2.10 eV 는 **고른 문턱에 따라 통과도 탈락도 한다**.
  ⛔ *"우리 갭이 문헌 기준을 만족한다"* 는 인용은 **어느 문턱인지 명시 없이는 금지**.
- **🔑 `K_eff`–`K_crit` 는 우리가 이미 가진 값으로 손댈 수 있는 유일한 빈칸이다** — 벌크 탄성이
  있으니 "구속 하의 분해" 를 보는 축으로 확장 가능. 부피변화 칸은 진짜로 새 계산이 필요하다.

---

## 6. ★★ hull 기반 열역학 스크리닝 — **이 리뷰가 우리 방법을 어떻게 평가하나**

### 6a. 명시적 비판 문장 — **한 줄이 결정적이다**

p.14, 반응성 3분법(ref 133 Lomeli/Reed/Devereaux, *ACS AMI* **16**, 51584 (2024)) 소개 중:

> *"This study identified more than **300 chemically stable SEs** and more than **780 passivating SEs**,
> **challenging previous thermodynamic-based assessments that often-misclassified materials as unstable.**
> … These findings suggest that **the pool of viable SEs may be far larger than previously anticipated**."*

⇒ **우리 방법(0 K MP hull grand-potential)이 겨냥된 문장이다.** 그리고 **편향의 방향까지 말한다**:
열역학 판정은 **불안정 쪽으로 틀린다**(false negative). 이것은 **우리에게 양날이다** — §6d.

### 6b. `Fig. 7D` — **그 비판의 그림 증명** (실독 2026-09-22)

세로축 **ΔE_rxn (eV/atom)**, 0.0 ~ −1.2. 가로축은 **50 개 SE 이름**(Li₆NBr₃ 부터 LiSO₃F 까지).
점 색 = **AIMD 로 라벨한 3분류** — 🟩 Stable · 🟧 Passivating · 🟪 Reactive. **세 군이 왼→오른쪽으로
블록 배치돼 있어 정렬된 것처럼 보이지만, 값 범위는 심하게 겹친다** (`figure-read ≈`):

| 분류 | ΔE_rxn 범위 (figure-read ≈) | 양 끝 물질 |
|---|---|---|
| 🟩 **Stable** (14점) | **0.00 → −0.40** | Li₆NBr₃·Li₂S·Li₇PN₄·Li₃N ≈ 0.00 / Li₇VGeO₈ ≈ −0.40 |
| 🟧 **Passivating** (12점) | **0.00 → −0.50** | Li₆WN₄ ≈ 0.00 / **Li₃Sc₂(PO₄)₃ ≈ −0.50** |
| 🟪 **Reactive** (24점) | **−0.16 → −1.12** | **Li₃ErCl₆ ≈ −0.16** / LiSO₃F ≈ −1.12 |

**⇒ 이 그림이 말하는 것 (본문은 이렇게까지 안 쓴다):**

1. **ΔE_rxn 은 분류를 순서짓지 못한다.** **−0.16 eV/atom 인 Li₃ErCl₆ 가 Reactive** 인데
   **−0.50 eV/atom 인 Li₃Sc₂(PO₄)₃ 는 Passivating** 이다. **부호도 크기도 결과를 못 정한다.**
2. **−0.16 ~ −0.50 eV/atom 구간에 세 분류가 전부 들어 있다.** 그 구간이 바로
   **우리 comp1\|LiCoO₂ −0.3227 eV/atom 이 앉아 있는 자리**다.
3. Li₃PS₄ ≈ −0.71 · Li₇P₃S₁₁ ≈ −0.81 · Li₁₀GeP₂S₁₂ ≈ −0.69 (전부 🟪 Reactive) —
   **황화물은 Li 금속에 대해 예외 없이 Reactive** 다. (⚠ **이 그림은 vs Li 금속이지 vs 양극이 아니다** — §6e)

### 6c. 그런데 **이 리뷰는 hull 을 버리지 않는다** — 오히려 전부 hull 위에 서 있다

| 어디 | hull 사용 |
|---|---|
| `Fig. 6E` (ref 122 Chen/Troyer, *JACS* **146**, 20009 (2024)) | **ML E_hull < 50 meV/atom** 이 3,260만 → 59만의 **1차 게이트**, 이어 **DFT E_hull < 50 meV/atom** 재검증 |
| `Fig. 6B` (ref 121 Sun/Min, *ACS AMI* **15**, 5049 (2023)) | 형성에너지 < 0.0 eV/atom |
| `Fig. 9A` (ref 160 Xiao/Ceder) | **E_hull < 0.005 eV/atom** — 우리 digest 가 이미 보유 |
| `Fig. 8E–G` (ref 137 Wang/Li, *JACS Au* **2**, 886 (2022)) | 설계공간의 **한 축이 E_hull** 자체 |
| 식 (1) 예시 | BO 목적 *"bandgap >1 eV and **energy above hull <50 meV**"* (ref 51) |

⇒ 리뷰의 입장은 ***"hull 은 필요하지만 충분하지 않다"*** 이지 *"hull 을 쓰지 마라"* 가 아니다.
Limitation 2 가 그 이유를 적는다: *"interface stability is **not solely determined by instantaneous
chemical potential** and ion/electron transport behavior but is also governed by **long-term structural
evolution**, such as element diffusion, phase transitions, and interface coarsening"* + 시간규모 간극
(*"degradation typically unfolds over **hundreds to thousands of charge-discharge cycles**, whereas
existing computational methods can only simulate **nanosecond-scale** behavior"*).

### 6d. 🔑 **이 비판이 우리에게 유효한가 — 판정**

| 비판 | 우리에게 유효? | 근거 |
|---|---|---|
| *"열역학 판정이 불안정으로 오분류한다"* | 🟡 **절반 유효 — 그리고 절반은 우리 편이다** | 편향 방향이 **불안정 쪽**이라면, **우리가 "반응이 일어나 Nd 인산염이 생긴다" 고 말하는 예측은 보수적인 쪽**이다(생긴다고 한 것이 안 생길 위험보다, 안 생긴다고 한 것이 생길 위험이 크다). ⛔ **단 뒤집어서**, 우리가 `dual compatibility` §E 에서 **"음수라서 나쁘다"** 고 탈락시킨 상들(Li₂SO₄ −0.0940 · Nd₂(SO₄)₃ −0.1470 eV/atom)은 **`Fig. 7D` 기준으로 Stable/Passivating 구간에 그대로 들어간다** ⇒ **우리 §E 의 탈락 판정이 false negative 일 수 있다.** 이것이 이 논문이 우리에게 준 **가장 아픈 지적**이다 |
| *"순간 화학퍼텐셜만으로 정해지지 않는다"* | 🔴 **유효** | 우리 grand-potential 은 **μ_Li 를 외부 스칼라(전압)로 주입**하고 공간분포·시간진화를 안 푼다. (이미 `wu2026…` §7 에 같은 항목이 있다 — 여기서는 **원전이 같은 말을 한다**는 사실만 추가) |
| *"ns vs 수백~수천 사이클"* | 🔴 **유효** | 우리는 시간축이 아예 없다(0 K). `comparison_vs_ours.md` §H 의 **"양극 CEI 의 운동학" 빈칸**과 같은 칸 |
| *"준안정상·hull 세대 의존"* | 🟡 **완화 근거 있음** | 우리 보호율 식은 hull 이 고른 **Nd 인산염의 P/Nd 비**만 쓰고 **에너지 절대값을 안 쓴다** ⇒ hull 오차에 1차적으로 둔감. (이 반론은 `wu2026…` §7 에 이미 기록. **무효화는 아니다**) |

### 6e. ⚠ **전이 금지 조항 — `Fig. 7D` 를 우리 CEI 에 그대로 못 옮긴다**

- `Fig. 7D` 의 ΔE_rxn 은 **SE vs Li 금속**(음극/SEI) 이다. 우리 −0.3227 은 **SE vs LiCoO₂**(양극/CEI) 다.
  **같은 축이 아니다.** 살아남는 논지는 *"열역학 반응에너지가 운동학 결과를 순서짓지 못한다"* 는
  **논리** 뿐이고, **숫자 대응은 성립하지 않는다**.
- ΔE_rxn 의 정의도 다르다 — `Fig. 7D` 는 *"chemical mixing energy"*, `Fig. 9A` 는 *"reaction energy …
  in eV/atom"*, 우리는 Richards/Ong pseudo-binary **최소화값**. **세 개가 같은 양이라는 보증이 없다.**
- 50 종 학습에 *"small-sample AIMD data (<10³)"* 이라고 리뷰 스스로 적고,
  *"its generalizability may face limitations due to **potential overfitting and insufficient chemical
  diversity**"* 라고 단서를 단다. ⇒ **"780종이 부동태" 를 숫자로 인용하지 마라.**

---

## 7. "AI ecosystem" 이 무엇인가 — **논지인가 결과인가** (명확히 가른다)

### 7a. 단어의 자리 = **Direction 3 (제안)**

"ecosystem" 은 본문에서 **Potential directions 의 세 번째 항목 제목**으로 등장한다:
*"**Direction 3: Building an intelligent ecosystem integrating AI, computations, and experiments.**"*
그 첫 문장이 **결론을 스스로 말한다**:

> *"The absence of an intelligent ecosystem for SSBs stems primarily from the **disjointed nature** of
> computational materials modeling, experimental research, and AI."*
> *"Unlike catalysis and drug discovery, which have already developed closed-loop platforms integrating
> AI, computational simulations, and high-throughput experimentation, **the field of SSBs still lacks
> such intelligent research infrastructure.**"*

### 7b. 구현 사례 — **분야별로 갈라 보면 SSB 는 0 건**

| 분야 | 구현 사례 (이 리뷰가 든 것) | 출처 |
|---|---|---|
| **촉매** | **Open Catalyst Project** — 대규모 큐레이션 DB 가 AI 촉매 발굴을 가능케 함 | ref 171 (Tran…Zitnick, *ACS Catal.* 13, 3066 (2023)) |
| **고체합성 일반** | **A-Lab** — 자율 실험실, 산화물·인산염 실제 합성 | ref 32 |
| **무기합성 로봇** | **224 반응 → 35 무기화합물**(일부는 전지 전극용 산화물) | ref 33 |
| **화학·재료 SDL** | MIT 계열 자율주행 실험실 · Berlinguette Pareto front | ref 189, 193–195 |
| **폴리머 전해질** | GPT/확산모델(6,024 비정질 폴리머 전해질 학습) · miniGPT 로 **14 반복단위** 생성 | ref 83, 84 |
| **SSB (무기 SE·SEI/CEI)** | ⛔ **없다.** *"this paradigm has **yet to be widely adopted** in the SSB field"* | — |

### 7c. 대신 제시되는 것 = **시간축 로드맵** (DISCUSSION)

| 기간 | 할 일 (원문 요지) |
|---|---|
| **0–2 년** | 합성·특성·보고의 **표준 프로토콜** 확립 · MLFF 로 계산 데이터셋 확장 · **벤치마크 실험 데이터셋**(합성절차·환경조건·측정기법·완전한 문서화 포함) 구축 |
| **2–5 년** | 개별 랩이 AI 연구자와 협업해 **능동학습·실험설계**로 캠페인 유도 · 다른 플랫폼 데이터 **융합**(측정 불일치 보정) · 자동화 없이도 AI 로 실험 우선순위 결정 |
| **5+ 년** | **자율 AI 유도 실험**(합성경로·계면처리까지 추천) · 공동체 표준 DB + 공유 온톨로지 → 한 랩에서 학습한 모델이 기관 간 일반화 |

⇒ **판정: "AI ecosystem" 은 제목이 약속하는 결과가 아니라 *Toward* 가 가리키는 제안이다.**
- ✅ 인용 가능: *"SSB 분야에는 촉매·신약처럼 AI-계산-실험을 잇는 폐루프 인프라가 **아직 없다**"* — **저자들 자신의 진술**
- ⛔ 인용 금지: *"AI 생태계가 SSB 연구를 바꾸고 있다"* 류 — **사례가 없다**

---

## 8. SEI vs CEI 비대칭 — **우리가 CEI 만 하는 선택의 근거가 여기 있나**

### 8a. 리뷰의 명시 진술 (CEI 절 마지막 문단, p.19)

> *"**Compared with the research on SEI, the situation of CEI may be more complicated because a variety
> of cathode materials are introduced instead of relatively simple Li metal or silicon.** Simplifying the
> problem and narrowing the materials space can make the screening of SE and cathode materials
> **independent**, and then comprehensively study the interface properties."*

### 8b. 비대칭의 실물 증거 (우리가 센 것)

| 지표 | SEI | CEI |
|---|---|---|
| 본문 분량 | pp.12–16 (**≈5 pp**) | pp.16–19 (**≈3 pp**) |
| 전용 그림 | `Fig. 7`, `Fig. 8` (**2장, 패널 12개**) | `Fig. 9`, `Fig. 10` (**2장, 패널 6개**) |
| `Fig. 1` 불릿 | **5개** | **4개** |
| 정량 틀 | ΔE_rxn 3분법 · K_crit · E_hull–K* 2D 공간 · XPS 예측(MAE 0.03 eV) | ΔE_rxt 게이트(−0.1) · μ_Li(r) · Li site energy |
| 대상 상대물 | Li 금속 · Si (**2종**) | LCO · NCM · Ni90 · LMO · LFPO … (**다종**) |

⇒ **어려운 쪽(CEI)에 분량이 덜 간다.** 그리고 리뷰는 그 이유를 *"양극 종류가 많아서"* 로 돌린다.

### 8c. 🔑 **우리 선택의 정당화 — 쓸 수 있는 형태로**

- ✅ **정당화 근거가 된다**: 리뷰 자신이 *"CEI 가 더 복잡하다"* 고 적고, 그럼에도 **덜 다룬다**.
  ⇒ 우리가 **CEI 만** 파는 것은 *"쉬운 쪽을 골랐다"* 가 아니라 *"덜 다뤄진 어려운 쪽을 골랐다"* 다.
- ✅ **리뷰가 권하는 해법이 우리 접근과 같은 방향이다**: *"Simplifying the problem and narrowing the
  materials space can make the screening of SE and cathode materials **independent**"* — 우리 §B 가
  정확히 그렇게 한다(6 조성 × 4 양극 × 6 전압을 **격자로** 돌려 각 축을 분리).
- ⚠ **단 한 가지 어긋난다**: 리뷰의 처방은 *"**universal coating materials** 를 찾아 개별 CEI 최적화를
  대체하라"* 인데, 우리는 **범용 코팅이 아니라 SE 도핑으로 제자리 보호상**을 만든다.
  ⇒ 이 차이가 우리 positioning 문장이 된다 (§13-②).

---

## 9. Zeier 색채 — **실험이 계산에 무엇을 요구하나** ⚠ **그리고 저자기여의 함정**

### 9a. ⚠⚠ 먼저 사실관계 정정 — **이것은 Zeier 그룹 논문이 아니다**

> 우리 작업지시는 *"Zeier 그룹은 우리 축 B 의 계보다"* 라고 적었다. **그것은 Zeier 그룹의 다른
> 논문들에 대해 맞는 말이지만 이 논문에는 안 맞는다.** 저자기여 표기:
> **Conceptualization / Methodology / Investigation / Visualization / Supervision / Writing-original draft 전부 Z.W. + F.Y.** ·
> **Zeier 는 `Writing—review and editing` 하나뿐**이다. 교신도 Cornell(fengqi.you@cornell.edu).
> 연구비도 Schmidt AI in Science 펠로십 하나 — **Münster/Jülich 쪽 자금 표기가 없다**.
> ⇒ **이 논문을 "Zeier 그룹의 방법론 선언" 으로 인용하면 틀린다.** 정확한 서술은
> *"Cornell 의 AI/공정시스템 그룹이 쓰고 Zeier 가 편집으로 참여한 리뷰"* 다.

### 9b. 그럼에도 **Zeier 색채가 식별되는 삽입 6곳** — 실험이 계산에 요구하는 것

| # | 삽입 문장 (원문) | 위치 | 원 출처 | 우리에게 |
|---|---|---|---|---|
| **1** ⭐⭐ | *"We emphasize that **modeling and prediction using activation energy instead of ionic conductivity may be more accurate and reliable**, as the temperature dependence is less sensitive to the absolute value of the ionic conductivity."* | p.9–10, `Fig. 5` 직후 | (저자 주장) | **우리 인용정책(2026-09-18, 1저자)과 같은 방향**. 단 우리 정책은 **Ea 도 상대차만** 이라 한 단계 더 보수적이다 |
| **2** ⭐⭐ | *"the reported ionic conductivity of argyrodites **varies by two to three times across different experiments**"* | p.20 (Limitation 3) | **ref 172 = Ohno … Zeier, *ACS Energy Lett.* 5, 910 (2020)** — 실험실 간 비교연구 | **우리 σ 절대값 인용금지 정책의 문헌 근거.** ⇒ `comparison_vs_ours.md` §J 에 등록 |
| **3** | *"**EIS measurements have combined contributions of grain boundary (GB) and in-grain processes**, resulting in the uncertainty of ionic conductivity"* + *"the lack of structural data with crystallographic information files is a problem"* | p.9–10 | (저자 주장) | 우리 MLIP-MD 는 **단결정 주기셀**이라 GB 가 아예 없다 — 실험 σ 와 층위가 다름을 말할 근거 |
| **4** | *"The **anion disorder in argyrodites represents an average disorder** but still influences the ion transport. This, in turn, affects both the **static and dynamic Li⁺ disorder**"* | p.20 (Limitation 1) | **ref 168 = Maus … Janek/Zeier/Kwade 외** | **우리 무질서 처리(modelc 단일 배열)의 급소.** 리뷰는 "평균 무질서" 와 "정적/동적 Li 무질서" 를 **다른 층**으로 가른다 |
| **5** | *"ion transport properties depend not only on the LCE … but also on **disorder factors and strain effects**"* | p.20 | **ref 166 = Faka … Zeier, *JACS* 146, 1710 (2024)** — 압력 유도 전위(dislocation)가 아지로다이트 이온수송에 미치는 영향 | ⛔ **우리 축에 전위·변형장이 없다** |
| **6** ⭐ | *"these ultralong MLFF simulations also demonstrated that the **paddle-wheel effect is absent in crystalline Li₆PS₅Cl at room temperature**, with rotating [PS₄]³⁻ polyanion groups exerting a **slight negative influence** on overall Li⁺ diffusion"* | p.10 | **ref 103 = Ding … Zeier, Delaire, *Nat. Phys.* 21, 118 (2025)** | **아지로다이트에서 패들휠 서사를 부정**하는 진술. 우리가 Li 확산 기전을 서술할 때 패들휠을 끌어오면 안 된다는 뜻 |

### 9c. **실험이 요구하는데 우리가 못 주는 것** (목록)

| 요구 | 우리 현황 |
|---|---|
| GB 와 입내(in-grain) 를 **분리한** 수송 | ⛔ 0건 (주기셀 단결정) |
| 전위·변형장 하의 수송 (ref 166) | ⛔ 0건 |
| 수백~수천 사이클 규모의 계면 진화 | ⛔ 0건 (0 K 평형) |
| **합성 메타데이터가 붙은** 벤치마크 | ⛔ 계산 전용이라 해당 없음 — 단 **우리가 그 계산 쪽 표준을 이미 갖고 있다**(`canonical_registry.json` + `citation_hazards.json`). ⇒ §13-⑤ |
| σ 대신 **Ea** 로 말하기 | ✅ **이미 그렇게 한다** (1저자 정책 2026-09-18) |

---

## 10. 인용 가능한 문턱값·수치·분류체계 ★ (전부 2차 인용 — 원 출처 병기)

### 10a. `Fig. 9A` — 양극 코팅 스크리닝 깔때기 (실독) · **원전 = ref 160 Xiao/Miara/Wang/Ceder, *Joule* 3, 1252 (2019)**

> 🔁 **우리는 이 원전 digest 를 이미 갖고 있다**(`xiao2019_cathode_coating_screening.md`, SI 전수 파싱).
> 여기서는 **문턱값만** 재확인한다 — 두 digest 가 일치한다.

```
Li 함유 화합물 (ICSD + data-mined)                       104,082
 Filter 1  초기   방사성 제외 · 전자전도체 제외 (E_g > 0.5 eV)   62,437
 Filter 2  상안정 Energy above convex hull < 0.005 eV/atom       1,600
 Filter 3  전기화학 V_red ≤ 2.7 V  and  V_ox ≥ 4.0 V               302
 Filter 4  화학   ΔE_rxt ≥ −0.1 eV/atom  (vs LPS=Li₃PS₄ & NCM)     184
 Filter 5  폴리음이온 산화물                                         66
 → 유망 양극 코팅: LiH₂PO₄ · LiTi₂(PO₄)₃ · LiPO₃
```

⭐ **`ΔE_rxt ≥ −0.1 eV/atom` 이 이 digest 에서 우리에게 가장 값있는 단일 숫자다** — 분야가 합의한
*"코팅으로 쓸 만한 반응성" 의 합격선*이고, 우리 **comp1\|LiCoO₂ = −0.3227 eV/atom** 은 **3.2배 초과**다.

### 10b. `Fig. 6E` — 클라우드 HPC 깔때기 (실독) · **원전 = ref 122 Chen … Troyer, *JACS* 146, 20009 (2024)**

```
32,598,079 → (ML E_hull < 50 meV/atom) → 589,609
 Li mole fraction ≥ 0.1        197,744
 ML bandgap > 3 eV               8,795
 ML E_red < 1.0 V, E_ox > 3.0 V    771
 DFT E_hull < 50 meV/atom          583
 ML MD diffusivity                 147
 ─── 실전지 기준 ───
 Cost                                74
 ML K_VRH, G_VRH < 30 GPa            64      ← ⭐ 우리 축 C
 ρ < 2.5 g/cm³                       23
 기지 조성 제외                      18
```

⭐ **`K_VRH, G_VRH < 30 GPa` = "실전지용 SE 는 물러야 한다"** 는 문턱. 우리 comp1 B₀ **26.23** ·
modelc **21.71 GPa** 는 **둘 다 통과**한다 ⇒ **우리 축 C 의 "무른 것이 좋다" 서사에 외부 문턱을 붙일 수 있다.**
⚠ **단 `K_VRH` 와 우리 `B₀`(EOS BM3)는 같은 양이 아니다** — 하나는 탄성계수 VRH 평균, 하나는 상태방정식 적합.
같은 표에 놓되 **정의를 명시**해야 한다.

### 10c. `Fig. 6C` — ML 탄성 예측 MAE (실독) · **원전 = ref 119/196**

| 모델 | MAE K_VRH (GPa) | MAE G_VRH (GPa) |
|---|---|---|
| **LGBM** (리뷰가 "최고 일치") | **21.580** | **16.048** |
| CGCNN | 50.364 | 19.047 |
| MEGNet | 55.722 | 32.763 |
| MPNN | 37.487 | 19.833 |
| SchNet | 166.044 | 36.278 |

⚠⚠ **이 표는 리뷰의 서술과 반대로 읽힌다.** `Fig. 6D` 의 검증 가넷 10종은 **K_VRH 47–124 GPa**
(figure-read ≈ Li₇Nd₃B₂O₁₂ 47.5 / Li₇Tm₃Te₂O₁₂ 124) 인데, **최고 모델 MAE 가 21.6 GPa** 다.
우리 황화물 B₀ **21.7–26.2 GPa** 는 **그 MAE 와 같은 크기**다 ⇒ **ML 탄성 예측은 우리 계에서
쓸 수 없다.** §13-③ 에서 이것을 우리 강점으로 뒤집는다.

### 10d. `Fig. 6F` — COSNet 정확도 (실독) · **원전 = ref 35**

| 물성 | MAE | **R²** |
|---|---|---|
| Li⁺ conductivity (S/cm) | 0.924 | **0.44** |
| Bandgap (eV) | 0.46 | **0.24** |
| Refraction index | 0.43 | 0.52 |
| Formation energy (eV/atom) | 0.102 | 0.58 |

⚠ **R² 0.24 (밴드갭) · 0.44 (전도도)** 인데 본문은 *"superior performance compared to conventional
single-modal models"* 라고 쓴다. §12-② 참조. ⚠ 전도도 MAE 0.924 는 **단위가 로그인지 안 밝힌다**
(캡션은 "S/cm" 라고만) — **인용 금지**.

### 10e. `Fig. 7C,D,E` — **반응성 3분법** (실독) · **원전 = ref 133 Lomeli … Sendek/Reed/Devereaux, *ACS AMI* 16, 51584 (2024)**

| 분류 | 본문 정의 | `Fig. 7C` 패널 라벨 (조작적 기준) |
|---|---|---|
| **Stable** | *"minimal atomic rearrangement at the SEI"* | *"**Nearly zero crossing of non-Li atoms**"* |
| **Passivating** | *"limited atomic diffusion within the SE sublattice"* | *"**Limited change in SE sublattice atoms**"* |
| **Reactive** | *"structural reorganization"* | *"**SE sublattice atoms far from interfaces**"* |

- 학습셋 **50종 SEI 구조** (Li₆NBr₃/Li · Li₂S/Li · Li₇PN₄/Li 등), AIMD 로 라벨
- 분류기 **2개**(stable 모델 / reactive 모델)를 이어 3분류 (`Fig. 7E`)
- 산출: **>300 chemically stable · >780 passivating** · 유망 후보 **LiB₁₃C₂ · LiB₁₂PC**
- ⛔ *"small-sample AIMD data (<10³)"* + *"potential overfitting and insufficient chemical diversity"*
  ⇒ **숫자 인용 금지, 분류체계만 인용**

⭐ **이 3분법은 `wu2026…` §4.3 의 3분법(진짜 불활성 / 부동태 / 활성)과 같은 것**이고,
**여기가 원전 계보에 더 가깝다** (`wu2026…` 은 이것을 재인용한다). **우리 주장이 겨냥하는 칸 =
"Passivating"** 임을 선언할 때 **이 정의 문장(*"limited atomic diffusion within the SE sublattice"*)** 을 쓴다.

### 10f. `Fig. 8` — 기계 구속 축 (실독) · **원전 = ref 136 Fitzhugh … X. Li, *EES* 14, 4574 (2021) · ref 137 Wang … X. Li, *JACS Au* 2, 886 (2022)**

- **`Fig. 8C` SEI 3 국면**: ⓐ *Chemical relaxation/initial SEI formation* (초기계면 → 초기 SEI)
  ⓑ *Electrochemical cycling/SEI growth* (초기 SEI + Li → **2차 SEI**) ⓒ *Electrochemical cycling/**SEI
  maintenance*** (초기 SEI → 초기 SEI, **변화 없음**) ⇒ **ⓒ 가 부동태의 기계적 판본**
- **판정식**: *"When the effective local modulus (K_eff) remains below a critical threshold
  (**K_eff < K_crit**, defined by the interfacial materials), this SEI continues to react and grow into an
  unknown phase. Conversely, when **K_eff > K_crit**, the interface remains structurally intact."*
- 규모: **>80,000 SEI 조성** (MP 전자절연체 >20,000 × 세라믹-황화물 SE 4종: LGPS·LSPS·L₇P₃S₁₁·Na₇P₃S₁₁),
  랜덤포레스트로 K_crit 예측 (`Fig. 8D`, 결정트리 **50개 앙상블**)
- **`Fig. 8E–G`**: **E_hull–K\* 2 파라미터 공간**. **124,497 종**의 K\* 산출.
  본문: *"pristine **Li₅.₅PS₄.₅Cl₁.₅** (LPSCl), LGPS, and **Li₅.₅PS₄.₅Cl₁.₅₋ᵧXᵧ** (X = F, Br, I;
  **y = 0.4 for F, 0.15 for Br and I**) all exhibit **high K\* (>20 GPa) and E_hull values (>150 meV)**"*
  ⇒ 그대로는 동적 안정성이 최적이 아님. ML 로 최소화한 shell 조성은 **Li rich · S deficient**.
  `Fig. 8G` figure-read ≈ : core(LPSCl/LGPS/LPSCl-X) **K\* ≈ 27–28, E_hull ≈ 2.5×10² meV/atom** ·
  LGPS-min(K\*)-shell **≈ 21, 1.2×10²** · LPSCl-X-min(K\*)-shell **≈ 9.5, 4×10¹** ·
  **LPSCl-min(K\*)-shell ≈ 9, 2–3×10⁰ meV/atom**
- ⭐ `Fig. 8G` 삽화는 **코어–쉘 SE 입자** 도식이다 (core = 순수 LPSCl, shell = min(K\*) 조성,
  Cathode ↔ Li-graphite 사이 Li⁺ 화살표). ⇒ **"외부 코팅이 아니라 SE 자체의 조성을 표면에서 바꾼다"**
  는 발상의 **선행 사례**다 — 단 **음극/덴드라이트 축**이고 우리는 양극/CEI 축이다 (§11-③)

### 10g. 본문에 흩어진 인용 가능 수치

| 값 | 맥락 | 원 출처 |
|---|---|---|
| **MLFF 가속 10³–10⁶×** (GGA-DFT 대비, 계 크기·모델 의존) | MLFF 절 | ref 68, 69 |
| **DFT 한계: <1000 원자 · <1 ns** | Limitation 2 | (저자 진술) |
| **Li₆PS₅Cl 의 Li⁺ 전도도는 Cl⁻ 이 4c 자리의 25 % 를 점유할 때 최대** (무질서 최대인 50 % 가 아니라) — **6,500 원자 · 25 ns** MLFF-MD | MLFF 절 | **ref 71 = Lee, Ju, Hwang, You, Jung, Kang, **Han** (서울대), *ACS AMI* 16, 46442 (2024)** ⭐ **우리 무질서 축 직결** |
| Li₃ErCl₆ 의 **비선형 아레니우스** — AIMD 가 전도도를 과대평가하는 이유 (σ 0.05–0.3 mS/cm) | MLFF 절 | ref 68, 101 |
| Li₇P₃S₁₁ **1 μs** MLFF — [P₂S₇]⁴⁻ 사슬 내 [PS₄]³⁻ 4개는 회전, 고립 [PS₄]³⁻ 는 정지 | MLFF 절 | ref 102 |
| **패들휠은 상온 결정 Li₆PS₅Cl 에 없다**; [PS₄]³⁻ 회전은 Li⁺ 확산에 **약한 음의 영향** | MLFF 절 | **ref 103 = Ding … Zeier, Delaire, *Nat. Phys.* 21, 118 (2025)** |
| **BO 14 회 반복**으로 4,183 물질 공간에서 `gap>1 eV & E_hull<50 meV` 후보 발견 | 전략 절 | ref 51 |
| ML 유도 탐색이 무작위 대비 **2.7× 높은 확률**로 고속 Li 전도체 발견 | 이온전도 절 | ref 89 (Sendek 2019) |
| IonML 고속이온전도체 분류 **정밀도 90.4 %**, 144,000 종에서 **126 종** 발굴, **8 종 실험 확인** | 이온전도 절 | ref 67 |
| 가넷 전자전도 스크리닝 **>20,000 조성** | 스크리닝 절 | ref 66 |
| 무감독 XRD 군집 → **16 종** 미탐색 고속전도체 (10⁻⁴–10⁻¹ S/cm) | 이온전도 절 | ref 95 |
| GNoME: 기존 48,000 안정결정 → **220만 구조**가 현 hull 아래; 중간구조 포함 시 분류오차 **~5 %** | `Fig. 5C` | ref 39 |
| DP 모델 정확도 (LiCoO₂/a-LiF/Li₆PS₅Cl): **에너지 RMSE 2.5 meV/atom · 힘 RMSE 109.7 meV/Å** | CEI 절 | ref 139/161 |
| a-LiF 코팅 — **최적 1 nm 문턱** 초과 시 규칙적 도메인이 생겨 Li⁺ 전도 방해; a-LiF 는 Li₆PS₅Cl 의 P–S 사면체는 지키지만 **S₂ 이량체 형성은 못 막는다** | CEI 절 | ref 139 (Hu, *AFM* 34, 2402993 (2024)) — 🔁 `wu2026…` 중복 |
| Ni90\|SE 계면 Li 자리에너지: **Ni90-LZO · Ni90-LIC 는 증가폭 작고**, Ni90-Li₂S · Ni90-Li₃PO₄ 는 큰 장벽. 원인 = Li₃PO₄ 는 **격자부정합 ~5 %**, Li₂S 는 **음이온 배위환경 불일치**(Li₂S 쪽 S²⁻ vs Ni90 쪽 O²⁻); LIC 는 Cl⁻ 입방 충전으로 **구조 유연성** | CEI 절 | ref 86/165 (M3GNet, Chen & Ong) ⭐ |
| LCO\|LLZO: **Li-deficient 계면은 심한 무질서 + 양이온 혼합 + Co 상호확산**, Li-sufficient 는 무질서 적음; Co 는 LLZO **입계에 보편적으로 축적** (tilt 축·무질서·농도 무관) | CEI 절 | ref 55 (n2p2) |
| LCO\|β-Li₃PS₄: 반응층에 **Co-P-O-S 배위 혼합**; **높은 μ_Li(r) 계면 자리가 충전 개시 시 동적 Li⁺ 고갈을 유도해 SE 산화분해를 촉발** | CEI 절 | ref 140 (Gao, Jalem, Tateyama, *Chem. Mater.* 32, 85 (2020)) ⭐⭐ |
| XPS C1s 코어준위 이동 예측 **XGBoost MAE 0.03 eV · RMSE 0.04 eV** | SEI 절 | ref 135 |
| SSW-NN 설계 Li₂MCl₆ (M=Zr,Hf): σ ~1 mS/cm, **대칭셀 4,000 h** | SEI 절 | ref 145 |
| SEI 전자전도도가 **성장 속도**를 결정; 치밀한 SEI(날카로운 계면·정연한 GB)가 전자 부동태에 유리 | SEI 절 | ref 151, 152 |
| LATP + Li → **Ti⁴⁺ → Ti³⁺ 환원 → 혼합 이온-전자 전도 계면상** | Limitation 2 | ref 170 |

### 10h. 코팅 물질이 만족해야 하는 **6조건** (CEI 절 서두, 원문 요지)

> *"For coating materials to be viable in SSB applications, they must exhibit several key attributes:*
> ① *high ionic conductivity, to facilitate efficient Li⁺ transport across the coating without introducing resistance;*
> ② *chemical stability, to prevent undesirable side reactions with **both the cathode and SEs**;*
> ③ *balanced ionic and electronic conductivities, to improve the charge transfer kinetics without including the decomposition of SEs;*
> ④ *mechanical robustness, to withstand stress and deformation during repeated charge-discharge cycles;*
> ⑤ *uniformity and strong adhesion, to ensure **continuous and defect-free coverage** over the electrode or electrolyte interface;*
> ⑥ *and **processability**, to enable scalable manufacturing and seamless integration into practical battery architectures."*

⚠ **②가 `dual compatibility` 의 씨앗이고, ⑤가 우리 보호율(피복분율)의 씨앗이다** — 둘 다
**요구조건으로 이름만 적혀 있고 정량화되지 않았다**. §11 참조.

---

## 11. ★★ 선행연구 점검 — **우리 §D · §2b · §E 가 여기 있나** (1저자 지정 최우선 보고)

### ⭐ ① **§E `dual compatibility` — 있다. 이름까지 같다.** 🔴

CEI 절 마지막 문단(p.19):

> *"**Identifying universal coating materials using AI offers a promising alternative to separately
> optimizing CEI interfaces.** By leveraging high-throughput screening and generative models, **AI can
> predict materials with dual compatibility, ensuring both interfacial stability with SEs and
> electrochemical/structural compatibility with cathodes.** Such AI-driven materials discoveries could
> streamline battery manufacturing, reduce interfacial degradation, and enhance overall SSB longevity."*

**판정:**

| 항목 | 이 리뷰 | 우리 §E |
|---|---|---|
| 용어 | **"dual compatibility"** (그대로) | "dual compatibility" |
| 양쪽 제약 | **전해질 계면안정 + 양극 전기화학/구조 적합성** | **전해질 적합성 + V_ox** — **같은 두 축** |
| 형태 | **한 문장 제안**. 계산 0 · 데이터 0 · 수식 0 | **닫힌계 0 V 20 쌍 실행**, 단조 4점, ρ = −1, 사전등록 단측 p = 0.042 |
| 발견 | 없음 (제안뿐) | **V_ox ↔ 전해질 적합성이 정면 충돌** (4.193/0.0000 → 5.013/−0.0434) · 황산염이 계급으로 나쁨 |

⇒ **우리 §E 는 이 리뷰가 *이름만 붙여 놓고 하지 않은 일*을 실행한 것이다.**
- ✅ **인용은 필수다.** 원고에서 *"dual compatibility"* 를 쓸 때 **이 문장을 인용하지 않으면
  용어 선취 시비가 난다.** 정확한 서술: *"Wang, Zeier, You 가 AI 로 dual-compatible 코팅을 찾자고
  제안했으나 [ref], 우리가 아는 한 그 양쪽 제약을 **격자로 돌려 충돌을 정량화한 보고는 없다**."*
- ⚠ **"우리가 처음 제안했다" 는 주장은 이제 불가능하다.** 가능한 것은 *"처음 **실행**했다"* 다.
- 🔁 `cha2024_dualcompatible_halide_ncm_lpscl_interface.md` 와 **층위가 다르다** — cha2024 는
  **특정 할라이드 한 계**의 실험적 dual compatibility, 이 리뷰는 **범용 코팅 탐색 전략**으로서의 선언.
  **우리 §E 는 세 번째 층위**(다수 상의 두 축 동시 스크리닝)다. **셋을 구분해 인용해야 한다.**

### ② **§2b 보호율 식 `min(1, k·x/(1−x))` — 없다.** ✅ (선취 위험 없음)

- 피복·두께 개념은 **요구조건으로만** 나온다: §10h-⑤ *"uniformity and strong adhesion, to ensure
  **continuous and defect-free coverage**"* · *"critical design parameters such as **coating thickness,
  uniformity, and adhesion** must be meticulously optimized"*.
- 정량 모델은 **두께 축 하나뿐**이고 그것도 재인용이다 — a-LiF **≈1 nm 임계두께** (ref 139).
- **피복 *면적분율* 을 도펀트 농도 x 의 함수로 예측하는 식은 이 리뷰 어디에도 없다.**
- ⇒ **§2b 는 선행연구에 걸리지 않는다.** ⚠ **단 두께 축이 없다는 우리 모델의 한계는 그대로다**
  (`wu2026…` §10-② 와 동일한 지적).

### ③ **§D "Li 를 안 쓰는 인산염 경로" — 없다. 다만 *인접한 반대방향* 논의가 둘 있다.** 🟡

| 이 리뷰의 인접 논의 | 방향 | 우리 §D 와의 관계 |
|---|---|---|
| `Fig. 10A` (ref 140 Gao/Jalem/Tateyama): *"**high μ_Li(r) interfacial sites induce dynamic Li⁺ depletion** during charge initiation, **triggering SE oxidation decomposition**"* | **Li 고갈 → 산화분해** | **우리와 반대 방향의 인과**다. 우리는 *"싱크가 Li 를 안 쓰면 유리하다"*, 저들은 *"계면이 Li 를 잃으면 분해가 시작된다"*. **모순은 아니다 — 같은 "Li 예산" 물리의 두 얼굴**이지만, **우리 §D 의 논증(NdPO₄ 는 P 하나당 Li 0, Li₃PO₄ 는 3; Li/P ≈ 1.67 에서 부호 반전)은 여기 없다** |
| ref 55 (n2p2 LLZO\|LCO): **Li-deficient 계면 vs Li-sufficient 계면**의 무질서·양이온혼합 차이 | **Li 가용성이 계면 무질서를 정한다** | 같은 "Li 가용성" 축. **인산염 화학량론 논증 없음** |
| `Fig. 8G` core–shell (ref 137): shell 조성이 **"Li rich and S deficient"** | **Li 를 더 넣는 쪽** | 우리 §D 와 정반대 방향의 처방 — **단 축이 다르다**(음극 덴드라이트 vs 양극 CEI). ⛔ 같은 표에 놓지 말 것 |

⇒ **§D 의 기전(Li 를 소모하지 않는 인산염 싱크)은 선행연구에 없다.** 다만 **"계면 Li 예산" 이라는
*문제틀* 자체는 이미 문헌에 있으므로**, 우리 문장은 *"Li 예산이라는 축은 알려져 있으나 [ref 140, 55],
**싱크 상의 Li 화학량론이 그 예산의 부호를 뒤집는다**는 점은 보고된 바 없다"* 로 써야 정확하다.

### ④ 부수 발견 — **인산염이 이 분야의 수렴점이다** (우리 레인이 붐빈다)

| 어디 | 인산염 |
|---|---|
| `Fig. 9A` 최종 추천 3종 | **LiH₂PO₄ · LiTi₂(PO₄)₃ · LiPO₃** — 전부 Li 인산염 |
| `Fig. 9B` LOTF-MD 최우수 코팅 | **Li₃Sc₂(PO₄)₃** · Li₃B₇O₁₂ |
| `Fig. 7D` 유일한 "Passivating" 인산염 | **Li₃Sc₂(PO₄)₃** (≈ −0.50 eV/atom, figure-read) |
| Ni90 계면 Li 자리에너지 | Li₃PO₄ 는 **나쁜 쪽**(격자부정합 ~5 %) |

⇒ ✅ **"인산염 CEI" 는 분야가 이미 수렴한 답**이라 우리 결론의 **방향은 지지**된다.
⛔ **그러나 "인산염이 좋다" 자체는 새롭지 않다.** 우리 차별점은 **① 희토류(Nd) 인산염
② 밖에서 바르지 않고 SE 도핑으로 제자리 생성 ③ 전압-의존 상 사다리(k=1→4→5)** 세 가지뿐이다.
⚠ 그리고 **Li₃PO₄ 는 Ni90 계면에서 나쁘다**는 결과(ref 86/165)가 있으므로,
*"인산염이면 다 좋다"* 로 쓰면 반례를 맞는다 — **어느 인산염인지 명시**할 것.

---

## 12. 비판 — **이 논문의 약한 곳** ★ (본문↔그림 불일치 3건 포함)

### ① 🔴 `Fig. 10C` — *"confirm the high accuracy"* 가 그림과 안 맞는다 (본문↔그림 불일치)

본문: *"The RMSE of energies and forces, as depicted in `Fig. 10C`, **confirm the high accuracy** of the
training MLFFs."* 그림을 보면 (축: Energy RMSE 5–30 meV/atom × Force RMSE 0.12–0.30 eV/Å, `figure-read ≈`):

| 구조군 | Energy RMSE (meV/atom) | Force RMSE (eV/Å) |
|---|---|---|
| LLZO (cubic) — 가장 좋음 | **≈ 4.5** | **≈ 0.135** |
| LCO | ≈ 8 | ≈ 0.19 |
| LLZO (amorphous) | ≈ 11 | ≈ 0.19 |
| Co-doped LLZO | ≈ 20 · 28 | ≈ 0.24 · 0.28 |
| **LLZO-LCO interfaces** | **≈ 15.5 · 18** | **≈ 0.27 · 0.26** |
| LLZO-LCO mixtures | ≈ 22–28.5 | ≈ 0.26–0.29 |
| LLZO-LCO mixtures (unseen) | ≈ 22–26 | ≈ 0.26–0.28 |

⇒ **정작 연구 대상인 계면에서 힘 RMSE 가 벌크 결정의 ≈2배, 에너지 RMSE 가 ≈3.5배**다.
**정확도가 계면에서 계통적으로 무너진다** — 그림이 말하는 것은 "high accuracy" 가 아니라
**"정확도가 벌크 → 비정질 → 도핑 → 계면/혼합 순으로 단조 악화한다"** 다.
⛔ **"MLFF 가 계면을 정확히 잡는다" 의 근거로 인용 금지.** (우리 UMA 계면 적용에도 같은 경고가 적용된다.)

### ② 🔴 `Fig. 6F` — R² 0.24 를 *"superior performance"* 라고 부른다 (본문↔그림 불일치)

본문: *"COSNet has demonstrated **superior performance** compared to conventional single-modal models …
in predicting Li⁺ conductivity, electronic conductivity, refractive index, and formation energy."*
그림: **밴드갭 R² = 0.24 · Li⁺ 전도도 R² = 0.44.** R² 0.24 는 **사실상 예측력 없음**이다.
또 캡션은 네 물성을 *"Li⁺ conductivity (S/cm), bandgap (eV), refractive index, and formation enthalpy
(eV/atom)"* 라 적는데, **전도도 MAE 0.924 의 단위가 로그인지 선형인지 밝히지 않는다**.
⇒ **이 표의 어떤 값도 인용하지 마라.** "다중모드가 단일모드보다 낫다" 는 상대 비교까지만.

### ③ 🟠 `Fig. 8G` — *"moderate E_hull"* 인데 그림은 **가장 낮은** E_hull 을 가리킨다

본문: *"By directing material compositions toward **moderate E_hull values** and minimized K\*, this
approach paves the way for the rational design of dendrite-resistant SEs."*
`Fig. 8G` (figure-read): 최적화된 **LPSCl-min(K\*)-shell 이 E_hull ≈ 2–3 meV/atom** 으로
**세로축 최하단**에 있다. core (≈250 meV/atom) 대비 **두 자릿수 감소**다.
"moderate" 라는 단어가 그림과 안 맞거나, 아니면 리뷰가 원논문의 논리(적당한 분해 구동력을
남겨 둬야 동적 안정성이 생긴다)를 **한 문장으로 압축하다 잃었다**.
⇒ **이 문장을 우리 원고 논리에 쓰지 마라 — 원전(ref 137 *JACS Au* 2, 886) 확인 필요.**

### ④ 🔴 **우리 축 B 의 계보를 한 번도 인용하지 않는다**

refs 196 개 중 **Richards 2016 · Zhu 2015 · Zhu 2016 · Xiao 2020 리뷰 · Nolan 2018 이 전부 없다.**
있는 것은 Xiao 2019 (ref 160, 코팅 스크리닝) · Ong 2013 (ref 63, pymatgen) · Jain 2013 (ref 57, MP) 뿐.
즉 **grand-potential 계면 반응성 방법 자체를 소개하지 않는다** — `Fig. 9A` 의 `ΔE_rxt` 를 쓰면서도
그 양이 **어떻게 정의되는지(pseudo-binary 최소화)** 를 한 줄도 안 적는다.
⇒ **이 리뷰는 우리 방법의 계보 문헌이 아니다.** 축 B 를 논할 때 **이 논문을 방법 근거로 인용하면
안 된다** — 근거는 `richards2016…` · `zhu2015…` · `xiao2020…` 이다. (§0b 참조)

### ⑤ 🟠 **밴드갭 문턱이 한 문서 안에서 세 개다**

`E_g > 0.5 eV` (`Fig. 9A`) · `bandgap > 1 eV` (식 (1) 예시) · `ML bandgap > 3 eV` (`Fig. 6E`) ·
MatterGen 문맥 `> 3.0 eV`. **네 자리 모두 "전자절연" 을 뜻한다고 적는다.**
문턱이 6배 차이 나는데 **그 차이를 논평하지 않는다.** 전자누설 칸이 이 리뷰에서 얼마나 얕은지의 증거다.
⇒ 우리가 갭으로 §7 빈칸을 채울 때 **반드시 문턱을 명시**해야 하는 이유.

### ⑥ 🟠 **자기 인용이 눈에 띈다**

ref 72 = **Z. Wang, F. You** (생성모델 주기성 인식) · ref 64 = **AlphaMat** (Z.W. 계열 툴킷) 등.
리뷰가 자기 툴킷을 "대표 materials informatics toolkit" 목록에 DeepChem·Matminer·Pymatgen 과
나란히 놓는다. **치명적이진 않지만 목록의 대표성은 할인해서 읽어야 한다.**

### ⑦ 🟡 **"critically review" 라고 하는데 비판이 거의 없다**

초록은 *"we **critically** review"* 라 적지만, 본문에서 개별 연구의 한계를 지적하는 대목은
**ref 133 의 소표본 과적합 한 곳뿐**이다. 나머지는 전부 *"transformative"*, *"remarkable"*,
*"unprecedented"* 다. 위 ①②③ 이 전부 **그림을 봐야만 보이는** 불일치인 것이 그 결과다.

### ⑧ 🟡 **SI 를 못 봤다 (우리 쪽 한계)**

Tables S1–S5 는 별도 PDF 이고 우리는 본문만 받았다. 특히 **table S5 (SEI/CEI AI 연구 목록)** 는
우리 CEI 축의 선행연구 목록일 가능성이 높다. ⇒ §14 에 확보 항목으로 올림.

---

## 13. 적용 인사이트 (우리 연구에 어떻게) ★

### ① ⭐⭐ **우리 −0.3227 eV/atom 을 문헌 게이트에 대면 "탈락" 이다 — 이것을 먼저 말해야 한다**

Xiao/Ceder 게이트 **ΔE_rxt ≥ −0.1 eV/atom** vs 우리 comp1\|LiCoO₂ **−0.3227**. **3.2배 초과.**
⇒ **이것은 우리 이야기의 *약점*이 아니라 *출발점*이다.** 정확한 서술 순서:

> *"Li₆PS₅Cl 은 LiCoO₂ 에 대해 −0.32 eV/atom 으로, 문헌이 코팅 물질에 요구하는 합격선
> (−0.1 eV/atom [Xiao 2019])을 3배 초과해 반응한다. 즉 **이 계는 코팅 없이는 성립하지 않는다**.
> 우리 질문은 '코팅을 밖에서 바를 것인가' 가 아니라 '**SE 자체가 제자리에서 그 코팅을 만들 수
> 있는가**' 다."*

⚠ **단 게이트와 우리 값이 같은 양인지 확인이 필요하다** — Xiao 의 `ΔE_rxt` 는 vs Li₃PS₄ & 만충 NCM,
우리는 vs LiCoO₂. `xiao2019…` digest 에 원전 정의가 있으니 **원고 전에 1:1 대조**할 것.

### ② **positioning 문단이 이 리뷰 두 문장으로 완성된다**

> ⓐ *"**Identifying universal coating materials** using AI offers a promising alternative to separately
> optimizing CEI interfaces … materials with **dual compatibility**"* (p.19)
> ⓑ *"Simplifying the problem and narrowing the materials space can make the screening of SE and
> cathode materials **independent**"* (p.19)

우리 위치 = **ⓐ 의 "universal coating" 을 *외부 코팅* 이 아니라 *SE 도핑으로 제자리 생성* 으로
치환한 것**, 그리고 **ⓑ 를 실제로 격자(6×4×6)로 실행한 것**. ⛔ 두 문장 다 **인용 표기 필수**.

### ③ ⭐ **`Fig. 6C` 를 우리 강점으로 뒤집는다**

ML 탄성 예측의 최고 MAE 가 **K_VRH 21.58 GPa** 인데 우리 계의 B₀ 는 **21.7–26.2 GPa** 다.
⇒ ***"현행 ML 대리모델의 탄성 오차가 황화물 SE 의 탄성값과 같은 크기이므로, 이 계에서는
first-principles 탄성이 대체 불가능하다"*** 를 **숫자로** 말할 수 있다.
이것은 우리 `comparison_vs_ours.md` §C 에 붙는 **새 논거**다.
⚠ K_VRH ≠ B₀(EOS) 이므로 **정의 각주** 필수.

### ④ **`K_eff` vs `K_crit` 틀을 §7 의 "압력변화" 빈칸에 쓴다 — 새 계산 없이**

우리는 이미 C_ij · B₀ · E_VRH 를 갖고 있다. `Fig. 8C` 의 판정식
(*K_eff < K_crit → 계속 반응·성장 / K_eff > K_crit → 구조 유지*)은 **우리 값으로 최소한 정성 서술이
가능한 유일한 CEI 빈칸**이다. 최소 실행: *"본 연구는 압력/구속 축을 직접 다루지 않으나, 계면
구속 모듈러스 판정 틀 [ref 136,137] 에서 요구하는 벌크 탄성 입력은 산출했다"* 로 §Limitations 를
채우고, 확장 시 **Nd 인산염 상들의 K_VRH** 를 같이 내면 칸이 실제로 채워진다.

### ⑤ **σ 절대값 금지 정책에 *문헌 근거* 가 생겼다**

**ref 172 = Ohno … Zeier, *ACS Energy Lett.* 5, 910 (2020)** — *"아지로다이트 보고 전도도가 실험실
간 **2–3배** 변동"*. ⇒ 우리 1저자 정책(2026-09-18, 상대차만)을 원고·리뷰 회신에서 **변호할 때
이 인용을 쓴다**. 함께: *"activation energy 로 모델링하는 것이 더 정확·신뢰할 수 있다"* (저자 진술).
⚠ 우리 정책은 **Ea 도 상대차만** 이라 한 단계 더 보수적이다 — 정책을 완화하는 근거로 쓰지 말 것.

### ⑥ **무질서 축에 외부 기준점 하나** — ref 71 (Lee … Han, *ACS AMI* 16, 46442 (2024))

**Li₆PS₅Cl 의 Li⁺ 전도도는 Cl⁻ 이 4c 자리의 25 % 를 점유할 때 최대** (무질서 최대인 50 % 가 아니라),
**6,500 원자 · 25 ns** MLFF-MD. ⇒ 우리 modelc(Cl-rich, 단일 배열)가 **어느 자리 점유율에 해당하는지**
확인할 수 있는 좌표계다. ⚠ `wu2026…` digest 가 인용한 *"최적창 37.5–50 %"* [80] 과 **숫자가 다르다** —
**같은 양인지 확인 전에는 둘을 나란히 쓰지 마라** (정의: 4c 자리 점유율 vs 전체 무질서도일 수 있다).

### ⑦ **"Passivating" 의 정의 문장을 확보했다**

*"**passivating** (limited atomic diffusion within the SE sublattice)"* — 우리 주장이 겨냥하는 칸을
**AIMD 관측량으로 정의한** 문장이다. 우리는 그 관측을 **안 한다**(0 K). ⇒ 원고에서
*"부동태 보호상을 만든다"* 고 쓸 때, **이 정의로는 아직 증명하지 않았다**는 것을 자백하거나,
UMA-MD 로 **SE 부격자 원자 변위**를 재면 그 칸이 실제로 채워진다. **후자는 기존 궤적으로 가능하다.**

---

## 14. 우리 원장 매핑 / 추가로 구해야 할 논문

### 14a. `comparison_vs_ours.md` 갱신 (이 digest 가 실제로 넣은 것)

| 축 | 넣은 것 |
|---|---|
| **§J (방법론)** | 🔧 **방법 원전 블록** — 이 논문은 **물성값 0** 이므로 물성 4축(A–D)에 넣지 않는다. hull 비판 · dual-compat 선행 · σ 2–3배 · ML 탄성 MAE · ΔE_rxt 게이트 |
| **§H (못 하는 것)** | **CEI 4조건 빈칸 표** (§5 표를 그대로) + `K_eff`/`K_crit` 확장 경로 |
| ⛔ **§B** | **넣지 않는다** — 이 논문에 산화 onset·ESW 수치가 **한 건도 없다** |

### 14b. ⭐ 추가로 구해야 할 논문 (우선순위)

| # | 논문 | 왜 |
|---|---|---|
| **1** 🔴 | **ref 133 = E. G. Lomeli, B. Ransom, A. Ramdas, D. Jost, B. Moritz, A. D. Sendek, E. J. Reed, T. P. Devereaux, "Predicting reactivity and passivation of solid-state battery interfaces", *ACS Appl. Mater. Interfaces* 16, 51584–51594 (2024)** | **우리 방법을 정면으로 때리는 문장의 원전.** *"열역학 기반 판정이 물질을 불안정으로 오분류해 왔다"* · 3분법 정의 · `Fig. 7D` 원본. **우리 §E 의 탈락 판정이 false negative 인지 여기서만 답할 수 있다** |
| **2** 🔴 | **ref 137 = Y. Wang, L. Ye, X. Chen, X. Li, "A two-parameter space to tune solid electrolytes for lithium dendrite constriction", *JACS Au* 2, 886–897 (2022)** | `Fig. 8E–G` 원본. **코어–쉘 SE 입자**(= 제자리 표면 조성 변경)의 선행. §12-③ 의 "moderate E_hull" 모순도 여기서 풀린다. LPSCl·LPSCl-X 가 **이름으로** 나온다 |
| **3** 🟠 | **ref 140 = B. Gao, R. Jalem, Y. Ma, Y. Tateyama, "Li⁺ transport mechanism at the heterogeneous cathode/solid electrolyte interface in an all-solid-state battery via the first-principles structure prediction scheme", *Chem. Mater.* 32, 85–96 (2020)** | **μ_Li(r) 계면 지도 + Li 고갈 → SE 산화분해.** 우리 §D "Li 예산" 축의 최근접 선행. **LCO\|β-Li₃PS₄ = 우리 계와 같은 짝** |
| **4** 🟠 | **ref 86/165 = P. Lu 외, *ACS Nano* 18, 7334 (2024) (Ni90 계면) + C. Chen, S. P. Ong, *Nat. Comput. Sci.* 2, 718 (2022) (M3GNet)** | **Li₃PO₄ 가 Ni90 계면에서 나쁘다**(격자부정합 ~5 %)는 반례. 우리 인산염 서사가 반드시 마주친다 |
| **5** 🟡 | **본 논문 SI (Tables S1–S5)** | **table S5 = SEI/CEI AI 연구 목록** — 우리 CEI 축 선행연구 목록일 개연성 |
| **6** 🟡 | **ref 71 = J. Lee, S. Ju, S. Hwang, J. You, J. Jung, Y. Kang, S. Han, "Disorder-dependent Li diffusion in Li₆PS₅Cl investigated by machine-learning potential", *ACS AMI* 16, 46442 (2024)** | **4c 자리 25 % 최적**. 우리 무질서 축 직결. 서울대 한승우 그룹 |
| **7** 🟡 | **ref 172 = S. Ohno … W. G. Zeier 외 (23인), "How certain are the reported ionic conductivities of thiophosphate-based solid electrolytes? An interlaboratory study", *ACS Energy Lett.* 5, 910–915 (2020)** | **σ 절대값 금지 정책의 문헌 근거**. 원문 확보하면 "2–3배" 의 정확한 조건을 인용할 수 있다 |
| **8** ⬜ | ref 136 Fitzhugh 외 *EES* 14, 4574 (2021) (K_crit 원전) · ref 139 Hu 외 *AFM* 34, 2402993 (2024) (a-LiF 1 nm — `wu2026…` 와 공통) | 압력/두께 축 확장 시 |

---

## 15. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| **1** | **SE 설계 4축(이온-전자전도 · 전기화학안정 · 기계강도 · 공기/습도안정) + 좌 SEI 5불릿 / 우 CEI 4불릿.** 캡션은 4축이 **양쪽 모두**를 위한 것이라 못박는다 | ⭐⭐⭐ **본 그림 · 이 논문을 구한 이유.** CEI 4칸 = **분해·부반응 / 전자누설 / 부피변화 / 압력변화**. 우리 §7 빈칸 표의 원전. **⚠ 4축이지 5축이 아니고, SEI/CEI 로 갈라지지 않는다** (§0a 정정) |
| 2 | 리뷰 전체 구조 개념도 (3 전략 → 2 응용 → 3 한계/3 처방, 원자→거시 4 스케일 띠) | ⛔ **안 봄** — 목차의 그림판 |
| 3 | (A) 전통 SE 설계 루프 (B) AI 가속 루프 4부분(표현·예측모델·물성예측·자동스크리닝) | ⛔ **안 봄** — 개념도 |
| 4 | 고속이온전도체 발굴 3방법: (A) Sendek LR 12,831 (B) IonML HMFP+능동학습 (C) BV+GCN 다중그래프 | ⛔ **안 봄** — (A) 는 `sendek2017…` 보유, (B)(C) 는 우리 축 밖 |
| 5 | (A) LLZTO 미세구조 ResNet-18 3등급 (B) XRDMatch 준지도 (C) GNoME | ⛔ **안 봄** — `ou2026…` 및 GNoME 별도 축과 중복 |
| **6** | (A) 탄성 ML 흐름 (B) 가넷 5329→10 깔때기 (C) **모델별 K_VRH/G_VRH MAE** (D) 최종 10종 K–G 산점 (E) **3,260만 → 18 클라우드 HPC 깔때기** (F) COSNet 정확도 | ⭐ **본 그림.** **C: 최고 MAE 21.58 GPa = 우리 B₀ 와 같은 크기 ⇒ 우리 축 C 의 새 논거** · **E: `K_VRH,G_VRH < 30 GPa` 실전지 문턱 + `ML bandgap > 3 eV`** · **F: R² 0.24/0.44 — §12-② 불일치** |
| **7** | (A) LASP/SSW-NN 워크플로 (B) Li-Zr/Hf-Cl\|Li 모델 (C) **Stable/Passivating/Reactive 3분법 + 조작적 기준** (D) **50종 ΔE_rxn 산점, 분류 색** (E) 2단 분류기 | ⭐⭐ **본 그림.** **D 가 "열역학은 운동학을 순서짓지 못한다" 의 그림 증명** — Li₃ErCl₆ −0.16 은 Reactive, Li₃Sc₂(PO₄)₃ −0.50 은 Passivating (figure-read). **C 의 "passivating" 정의 문장을 우리가 쓴다** |
| **8** | (A) XPS 특징생성 (B) 4모델 MAE/RMSE (C) **SEI 3 국면(형성/성장/유지)** (D) K_crit 결정트리 (E) **Hull(x,K_eff) 개념도** (F) ML 흐름 (G) **E_hull–K\* 공간의 LPSCl/LGPS core–shell** | ⭐ **본 그림.** **C 의 "maintenance"(변화 없음) = 부동태의 기계적 판본** · **G 는 코어–쉘 SE 입자 도식 = 제자리 표면개질의 선행** (⚠ 음극 축) · §12-③ 본문↔그림 불일치 |
| **9** | (A) **Xiao 코팅 깔때기 104,082 → 66 (5 필터)** (B) LOTF-MD 흐름 (C) DP 능동학습 + 4 계면 모델(SE/Cathode, SE/Coating, Cathode/Coating, Cathode/Coating/SE) | ⭐⭐ **본 그림** (상단 재크롭). **A 의 `ΔE_rxt ≥ −0.1 eV/atom` 이 이 digest 최고의 단일 숫자.** 🔁 원전 digest `xiao2019…` 보유 |
| **10** | (A) **CALYPSO PSO 로 LCO(104)/LPS(010) 계면구조 예측** (B) n2p2 클래스 상속 + LLZO\|LCO Li-sufficient/deficient (C) **에너지/힘 RMSE 산점** | ⭐ **본 그림.** **A = 우리 계와 같은 짝(LCO\|Li₃PS₄)의 μ_Li 지도 · §D 최근접 선행** · **C 는 계면에서 정확도가 계통적으로 무너짐을 보인다 — §12-① 본문↔그림 불일치** |

## 16. Post-processing ★ — **이 리뷰가 소개하는 도구 목록** (우리 대조용)

| 범주 | 도구 (ref) | 우리 |
|---|---|---|
| 구조·물성 DB | ICSD (56) · **Materials Project** (57) · NOMAD (58) · AFLOW (59) · OQMD (60) | ✅ MP 사용 |
| 서술자·인포매틱스 | DeepChem (61) · Matminer (62) · **Pymatgen** (63) · AlphaMat (64) · MAST-ML (65) | ✅ pymatgen |
| 대칭·배위 분석 | **Spglib** (181) · Pymatgen 배위분석 | 🟡 부분 |
| MLFF 엔진 | **DeePMD-kit** (161) · **n2p2** (163) · **LASP/SSW-NN** (144) · **LAMMPS** (164) · M3GNet (165) · GNoME (39) | ⚠ **UMA 없음** — `wu2026…` 와 같은 결과 |
| 구조탐색 | **CALYPSO** (162) — PSO 기반 계면구조 예측 | ⛔ 없음 |
| 해석가능성 | attention · integrated gradients · **SHAP** (182) | ⛔ 없음 |
| 물리제약 학습 | PINN (178,179) + **Butler-Volmer** (180) · 상장(phase-field) (174) | ⛔ 없음 |
| 문헌 마이닝 | **MatSciBERT** (186) · MaterialsBERT (187) · **BatteryBERT** (188) | 🟡 우리 litdb 가 사람 큐레이션 판본 |
| 실험 최적화 | MFBO (190) · FDI (191) · PGN/DQN (192) · SDL (189,193–195) | ⛔ 해당 없음 |

⛔ **UMA(FAIR-Chem)·MACE·SevenNet·CHGNet 이 전부 없다** — 이 리뷰의 MLFF 목록은
**DeePMD/n2p2/LASP 세대**에 머물러 있다. 2025-06 투고라는 시점을 감안해도 얕다.

## 17. 인용 가능 문장 (deck / 원고용)

> ⚠ 전부 **2차 인용**이다. 원고에 넣을 때는 **리뷰가 아니라 원전을 인용**하는 것이 원칙이고,
> 리뷰를 인용하는 것은 *"지형을 이렇게들 본다"* 를 말할 때뿐이다.

- *"The compositions, structures, and coupled ionic-electronic conductivities of SEI/CEI dictate the
  electrochemical kinetics of Li⁺ transport, yet their evolution under electrochemical cycling and
  mechanical stress requires systematic investigation."* (서론) → **CEI 4칸의 근거 문장**
- *"Identifying universal coating materials using AI offers a promising alternative to separately
  optimizing CEI interfaces … AI can predict materials with **dual compatibility**, ensuring both
  interfacial stability with SEs and electrochemical/structural compatibility with cathodes."* (p.19)
  → ⭐ **우리 §E 의 선행 선언. 인용 필수**
- *"Compared with the research on SEI, the situation of CEI may be more complicated because a variety of
  cathode materials are introduced instead of relatively simple Li metal or silicon."* (p.19)
  → **우리가 CEI 를 고른 것의 정당화**
- *"[This] challeng[es] previous **thermodynamic-based assessments that often-misclassified materials as
  unstable** … the pool of viable SEs may be far larger than previously anticipated."* (p.14, ref 133)
  → **우리 방법의 한계를 우리가 먼저 말하는 문장** (⚠ 원전 Lomeli 2024 를 인용할 것)
- *"Interface stability is not solely determined by instantaneous chemical potential and ion/electron
  transport behavior but is also governed by long-term structural evolution, such as element diffusion,
  phase transitions, and interface coarsening … [which] typically unfolds over hundreds to thousands of
  charge-discharge cycles, whereas existing computational methods can only simulate nanosecond-scale
  behavior."* (Limitation 2)
- *"We emphasize that modeling and prediction using **activation energy instead of ionic conductivity**
  may be more accurate and reliable, as the temperature dependence is less sensitive to the absolute
  value of the ionic conductivity."* (p.9–10) → **우리 인용정책 변호**
- *"The reported ionic conductivity of argyrodites varies by **two to three times** across different
  experiments."* (p.20, 원전 ref 172 Ohno…Zeier 2020) → **σ 절대값 금지의 문헌 근거**
- *"The **paddle-wheel effect is absent** in crystalline Li₆PS₅Cl at room temperature, with rotating
  [PS₄]³⁻ polyanion groups exerting a **slight negative influence** on overall Li⁺ diffusion."*
  (p.10, 원전 ref 103 Ding…Zeier/Delaire, *Nat. Phys.* 2025) → **패들휠 서사 금지**
- ⛔ **쓰지 말 것 1**: *"AI 생태계가 SSB 개발을 가속하고 있다"* 류 — **SSB 구현 사례 0건**, 저자들 자신이 부재를 선언
- ⛔ **쓰지 말 것 2**: *"MLFF 가 계면을 정확히 재현한다"* — `Fig. 10C` 가 반대를 보인다 (§12-①)
- ⛔ **쓰지 말 것 3**: COSNet·ML 탄성의 어떤 절대값도 (§12-②, §10c)

## 18. 주의 / 한계 (인용 규율)

1. ⛔ **물성 수치가 0 이다.** 산화 onset·ESW·밴드갭·Ea·D 어느 것도 이 논문에 없다.
   `comparison_vs_ours.md` **물성 4축(A–D)에 넣지 않는다** — §J(방법) 과 §H(빈칸)에만.
2. ⛔ **"Zeier 그룹 논문" 으로 인용 금지** — 저자기여상 Zeier 는 `Writing—review and editing` 뿐 (§9a).
3. ⛔ **우리 축 B 의 방법 근거로 인용 금지** — Richards 2016 · Zhu 2015 · Xiao 2020 을 **인용조차 안 한다** (§12-④).
4. ⚠ **`Fig. 7D` 는 vs Li 금속(SEI)이다** — 우리 −0.3227(vs LiCoO₂, CEI)과 **숫자 대조 금지**.
   살아남는 것은 *"열역학이 운동학을 순서짓지 못한다"* 는 **논리**뿐 (§6e).
5. ⚠ **ΔE_rxt / ΔE_rxn / 우리 pseudo-binary 최소값이 같은 양이라는 보증이 없다** —
   게이트(−0.1 eV/atom)를 우리 값에 대기 전에 `xiao2019…` digest 의 정의와 **1:1 대조** 필수.
6. ⚠ **`K_VRH` ≠ 우리 `B₀`(EOS BM3)** — `< 30 GPa` 문턱을 인용할 때 정의 각주 필수.
7. ⚠ **밴드갭 문턱 0.5 / 1 / 3 eV 가 공존**한다 (§12-⑤). 어느 문턱인지 명시 없이 인용 금지.
   그리고 우리 갭은 **PBE 과소평가**이고 **벌크 SE** 것이지 CEI 상의 것이 아니다.
8. ⚠ **>300 stable / >780 passivating 숫자 인용 금지** — 리뷰 자신이 소표본(<10³)·과적합 위험을 단다.
9. ⚠ **SI(Tables S1–S5) 미확보.** 본문이 다섯 번 참조하는 목록을 우리는 못 봤다 — "이 리뷰에 없다" 는
   판정은 **본문 기준**이다.
10. ⚠ **figure-read 값 전부**(`Fig. 7D` ΔE_rxn · `Fig. 8G` E_hull/K\* · `Fig. 10C` RMSE ·
    `Fig. 6D` K/G 범위)는 **픽셀 판독**이다. 원고에 옮기려면 원전에서 재확인.

## 19. 기법 용어 미니사전 (이 논문을 읽는 데 필요한 것만)

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **E_hull** (energy above convex hull) | 그 조성의 최안정 상 조합 대비 초과 에너지. 0 이면 열역학적으로 안정, 클수록 준안정 | 게이트로 **0.005 / 50 meV/atom** 두 값이 쓰인다 |
| **ΔE_rxt / ΔE_rxn** | 두 물질을 섞었을 때의 반응(혼합) 에너지, eV/atom. 음수 = 반응이 유리 | 합격선 **≥ −0.1 eV/atom** |
| **V_red / V_ox (E_red / E_ox)** | 전기화학 안정창의 환원·산화 한계, V vs Li/Li⁺ | 코팅 게이트 `V_red ≤ 2.7 & V_ox ≥ 4.0` |
| **K_eff / K_crit / K\*** | 계면의 유효 국소 모듈러스 / 그것을 넘으면 SEI 성장이 멈추는 임계 모듈러스 / ML 로 예측한 임계값 (GPa) | `Fig. 8`. **기계 구속이 화학 분해를 멈춘다**는 틀 |
| **K_VRH / G_VRH** | Voigt–Reuss–Hill 평균 체적/전단 탄성률 | 실전지 문턱 `< 30 GPa` |
| **MLFF / MLIP** | 기계학습 힘장(퍼텐셜). DFT 를 대체해 MD 를 10³–10⁶× 가속 | DeePMD·n2p2·LASP·M3GNet·GNoME |
| **LOTF-MD** (learning-on-the-fly) | MD 중에 힘장을 실시간 갱신하며 진행 | `Fig. 9B`. 코팅 후보 스크리닝용 |
| **SSW-NN** | Stochastic Surface Walking + 전역 신경망 퍼텐셜. 전역 구조탐색 | `Fig. 7A` LASP |
| **CALYPSO / PSO** | 입자군집최적화 기반 결정구조 예측. 여기서는 **이종 계면 구조** 탐색 | `Fig. 10A` |
| **DOAS** (density of atomistic states) | 무질서 배열들의 에너지 분포를 상태밀도처럼 본 것 | frustrated 물질 설계 (ref 70) |
| **LCE** (local chemical environment) | 배위수·전자구조 등 국소 화학환경 | 이온수송 서술자 |
| **BO / MFBO** | 베이즈 최적화 / 다중충실도 베이즈 최적화 | 14 회로 4,183 공간 탐색 |
| **HMFP** | hybrid multisource fingerprint — 구조+조성+자리 정보 결합 서술자 | IonML |
| **COSNet** | composition-structure bimodal network — 조성(텍스트)+구조(그래프) 이중모드 | `Fig. 6F` |
| **LMBTR** | local many-body tensor representation. XPS 코어준위 예측용 국소 서술자 | `Fig. 8A` |
| **PINN** | physics-informed neural network. 손실함수에 물리 제약(Butler–Volmer, 질량보존)을 박음 | Direction 2 |
| **SDL** | self-driving laboratory — 로봇 합성+측정+AI 판단 폐루프 | 촉매·신약엔 있고 **SSB 엔 없다** |
| **Stable / Passivating / Reactive** | AIMD 관측 기반 계면 3분법. 각각 *비-Li 원자 교차 거의 0* / *SE 부격자 원자 변화 제한적* / *SE 부격자 원자가 계면에서 멀리 감* | `Fig. 7C`. **우리 주장이 겨냥하는 칸 = Passivating** |
