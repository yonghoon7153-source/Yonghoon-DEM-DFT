<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md · 형식 기준 = papers/kato2016_high_power_assb_lsipscl_superionic.md (이 Comment 의 ref 4 · 같은 날 digest)
     2026-11-10 신규 · 사용자 목록 128 번 ("이것도 논문에이전트") · 본문 4 pp (Comment) · SI 없음.
     크롭 3장 (본문 그림 3 · 표 0) 을 **전부 실제로 봤다** — 자동 크롭 3/3 그대로 썼다 (재크롭 0 · 손 크롭 0 · 번호 공백 0 · `Fig. 3` 오른쪽 삽입도는 600 dpi 로 따로 확대해 봤다).
     `Fig. 1` 의 값은 PDF 안의 **벡터 좌표**에서 읽었다 — tools/litdb/janek2016_readout.py (--selftest 양성 + 음성 경로 · 일부러 깨서 빨간불 5/5 확인) →
     litdb/figures/janek2016_solid_future_battery_development/digitized.csv (224 행 · LGPS 선 ↔ kamaya2011 벡터 판독 대조 행 포함). `Fig. 2` · `Fig. 3` 은 모식도 (래스터 타일) 라 값이 없다.
     ⛔ 이 글은 Comment (전망) 다 — 자체 측정 · 계산 0. 숫자는 전부 2 차 인용 (refs 1–29 · 셀 제조사 사양) 이거나 저자 어림 (`Fig. 2` 의 +70 % 등 · 입력 미기재) 이다.
        물성 4축 (A–D) 표에 넣지 않는다 · 우리 db 절대값과 같은 셀에 놓지 않는다 · `Fig. 1b` 판독값은 '이 Comment 가 다시 그린 선' 의 값이라 원전 값으로 인용하지 않는다. -->

# A solid future for battery development — Janek & Zeier (*Nat. Energy* **1**, 16141 (2016))

> slug `janek2016_solid_future_battery_development` · DOI `10.1038/NENERGY.2016.141` · type `Comment (전망 · 2 차 인용 전용) — 자체 실험 · 계산 0 · 그림 3 (문헌 곡선 재도식 1 · 모식도 2) · 표 0 · refs 29` · PDF `litdb/inbox/128._A_solid_future_for_battery_development.pdf` (4 pp · 업로드 `56a1e33a-128._A_solid_future_for_battery_development.pdf` · SHA-256 `6b81f3c78c71eb41…`) · digested `2026-11-10` · status ✅ · 태그 **[외부·Comment·2 차 인용 전용·⛔ 물성 4축 (A–D) 비교 전면 제외]**

> elements: Li, S, P, Ge, O, N, La, Zr, Al, Zn, Ni, Co, Mn, C, F, H
> methods: Arrhenius, ESW

> 🎤 **관련 발표**: 없음 — `litdb/talks/*.md` 의 '논문 에이전트 인입 대기열' (지금 `lee2026_skku_mlip_materials_design.md` §99-10 하나) 에 이 글이 없고, 어느 talk 에도 Janek · Zeier · "solid future" 언급이 없다 (2026-11-10 전수 grep).
> 🔗 **이 글이 인용한 litdb digest 5 편**: ref 4 = [`kato2016_high_power_assb_lsipscl_superionic`](kato2016_high_power_assb_lsipscl_superionic.md) · ref 5 = [`kamaya2011_lgps_lithium_superionic_conductor`](kamaya2011_lgps_lithium_superionic_conductor.md) · ref 8 = [`zhu2015_esw_grand_potential_origin`](zhu2015_esw_grand_potential_origin.md) · ref 11 = [`zhu2016_first_principles_interface_stability_assb`](zhu2016_first_principles_interface_stability_assb.md) (⚠ 인쇄 저자명 **'Zhou, Y.'** 는 오기 — 그 digest 표지의 1 저자는 **Yizhou Zhu** · 권 · 쪽 4, 3253–3266 은 같다) · ref 15 = [`richards2016_interface_stability_pseudobinary`](richards2016_interface_stability_pseudobinary.md).
> ⚠ ref 18 (Sakuda · Hayashi · Takigawa · Higashi · Tatsumisago, *J. Ceram. Soc. Jpn.* **121**, 946 (2013)) 은 litdb [`sakuda2013_sulfide_mechanical_property`](sakuda2013_sulfide_mechanical_property.md) (*Sci. Rep.* **3**, 2261 (2013)) 와 **같은 해 · 같은 그룹의 다른 논문**이다 — 섞지 않는다.
> 🔗 **같은 저자들이 이 글의 의제를 이어 간 litdb 편**: [`kraft2017_lattice_polarizability_argyrodite_Li6PS5X`](kraft2017_lattice_polarizability_argyrodite_Li6PS5X.md) (Zeier\* · Janek — 이듬해 · 아지로다이트) · [`zuo2022_chlorination_cathode_interface`](zuo2022_chlorination_cathode_interface.md) (Janek\* — Cl-rich 아지로다이트 × NCM85 계면 · DEMS 로 SO₂ 실측) · [`banik2022_substitutions_oxidative_stability_argyrodite`](banik2022_substitutions_oxidative_stability_argyrodite.md) (Zeier\* + Mo) · [`trevisanello2021_sc_pc_ncm_cracking_diffusion`](trevisanello2021_sc_pc_ncm_cracking_diffusion.md) · [`minnmann2021_jes_charge_transport_bottlenecks`](minnmann2021_jes_charge_transport_bottlenecks.md) · [`minnmann2022_designing_cathodes_solidstate`](minnmann2022_designing_cathodes_solidstate.md) · [`bielefeld2019_microstructural_modeling_composite_cathode`](bielefeld2019_microstructural_modeling_composite_cathode.md) · [`bielefeld2020_effective_ionic_conductivity_binder`](bielefeld2020_effective_ionic_conductivity_binder.md) (Janek 그룹 — 복합 양극) · [`schmitt2026_chemomech_stability_dry_cathode_separator_sheets`](schmitt2026_chemomech_stability_dry_cathode_separator_sheets.md) (BELLA · Janek 공저 — 건식 시트) · [`wang2026_interface_stability_kinetics_sulfide_assb`](wang2026_interface_stability_kinetics_sulfide_assb.md) (Mollenhauer\* + Zeier + Janek — 계면 pseudo-binary · ΔV/V · AIMD).
> 🔗 **이 글이 인용하지 않은 같은 시기 litdb 편**: [`ong2013_lgps_family_substitution`](ong2013_lgps_family_substitution.md) (Ceder 그룹 · *Energy Environ. Sci.* 2013 · LGPS 족 11 조성 · 2 점 grand potential + AIMD) — 이 글의 '황화물의 낮은 열역학 안정성' 은 ref 8 (Zhu 2015) 하나만 든다 · [`haruyama2014_space_charge_layer_oxide_cathode_sulfide_se`](haruyama2014_space_charge_layer_oxide_cathode_sulfide_se.md) (*Chem. Mater.* 2014 · LCO/LPS 계면 Li 고갈의 DFT 원전) — 이 글의 '정류 접촉 · Li 고갈층' 서술에 인용이 없다.
> 🔎 litdb · kb 에서 이 Comment 자체를 인용한 곳: **0** (전수 grep `solid future` · `16141` — 숫자 우연 일치 행은 뺐다).

> **저자 · 소속 (p.4 끝 저자 노트 그대로)**: **Jürgen Janek** · **Wolfgang G. Zeier** — Institute of Physical Chemistry + Center for Materials Research, Justus Liebig University Giessen (35392 Giessen). Janek 은 KIT Institute of Nanotechnology 의 **BELLA** 실험실 과학 책임자 겸임. 연락 e-mail 두 개 (p.4).
> **PUBLISHED: 8 SEPTEMBER 2016 · ARTICLE NUMBER: 16141** · *Nature Energy* Vol 1 · September 2016 · 쪽 머리 표지 **'comment'** · © 2016 Macmillan Publishers. 접수 · 수리 날짜 · 연구비 · 이해상충 · 저자 기여 문구는 PDF 에 **없다** (Article 이 아니라 Comment 라서 · 심사 여부도 적혀 있지 않다).

---

## 0. 이 digest 를 읽는 법 — 읽기축

**글 종류부터 정한다.** 1 쪽 머리 표지가 `comment` 이고, 날짜는 게재일 하나뿐이며, Methods · 자체 자료 · SI 가 없다 → 원저 (Article) 가 아니라 **Comment (의견 · 전망)** 다. 이 글의 숫자는 셋 중 하나다 — ① 인용 문헌 (refs 1–29) ② 셀 제조사 사양 (refs 20 · 21 — 웹 링크) ③ 저자 어림 (`Fig. 2` 의 +70 % · +40 % · +0 % · −10 % — 입력 미기재). ⇒ litdb 규칙대로 **2 차 인용 전용** · **물성 4축 (A–D) 비교 전면 제외** (리뷰 선례 `liang2026` · `famprikis2019` 와 같은 처리). 원고에 숫자가 필요하면 원전 (refs) 으로 간다.

글의 뼈대는 **네 질문 → 다섯 과제 → 세 결론 + 하나의 예측** 이다.
1. **네 질문** (p.1): 어떤 SE 를 쓰나 · SSB 고유의 기계 안정성 문제를 어떻게 넘나 · SSB 가 '안전한 저장' 기대를 채우나 · SE 가 Li 금속 음극을 열어 에너지 밀도를 '진짜로' 올리나.
2. **다섯 과제** (p.1–2 'Key performance measures'): 에너지 밀도 · 출력 밀도 · 장기 안정성 (사이클 · 달력 수명) · 안전 · kWh 당 비용 — *"These five challenges define the roadmap for the successful development of SSBs."*
3. **세 결론** (p.4): ① SE / 활물질 사이의 나쁜 계면 동역학 최적화 연구가 더 필요하다 ② 고체 셀의 안정 운전에는 기계 압력이 필요하고 정량 연구가 필요하다 ③ 에너지 밀도의 큰 이득은 **Li 금속 음극뿐**이다.
4. **예측** (p.4 마지막 문단): *"high voltages and high power densities will be achieved in the coming years, and while the employment of thick lithium anodes seems unlikely, SSB development may be prompted by the superior kinetics when using intercalation anodes."* — **에너지 밀도가 아니라 동역학 (출력) 이 SSB 를 밀 것** 이라는 내기다.

우리 쪽 연결은 네 갈래다 (§7 · 값이 아니라 질문의 대응).
- **cascade** (도펀트 스크리닝 · 트랙 1저자 = 사용자) — 이 글이 과제로 꼽은 *계면 반응 · 부피 변화 · 공극 · 산물의 전자 성격 (SEI 대 MCI)* 이 묶음 2 의 축 ④ (작동창 2.5–4.25 V 도펀트 행방) · ⑤ (분해 부피 ΔV/V) · ⑥ (Li 쪽 산물 품질) 과 같은 질문이다. 묶음 2 는 카드 비준 상태이고 새 축 값은 **0 건**이다 (§7e).
- **li2s** (LPSCl@Li₂S 계면상 유리 수송) — *"If a highly conductive solid electrolyte interphase is formed, long-term operation will be secured"* 가 우리 09-11 계면상 카드의 질문 그 자체다. li2s 트랙은 그 질문에 답하지 못한 채 닫혔고 (마감 기록 금지 서술 그대로), li2s-3 이 같은 축을 새 카드로 잇는 중이다 (수송 결과 0 건 · §7d).
- **b2o3 / CEI** (양극 쪽 산화) — *"oxidized at intermediate potentials … Protecting interphases are therefore required"* 는 우리 2.5–4.25 V 작동창 규칙 (*창 전체가 열역학적 산화 구간 → '안정' 은 창 안의 분해 산물 · 부동태로 판단*) 과 같은 결론이다. *"the formation of SO₂ by oxidation of the solid electrolyte"* 는 우리 CEI 산물 11 종 목록에 SO₂ (분자결정) 로 들어 있다 (§7b · §7c).
- **DEM** (후막 복합 양극) — *"an independent network of electronically conducting particles … sufficient electronic and ionic percolation … pores can form and cracking and loss of particle contact may occur … mechanical pressure"* 가 우리 DEM 트랙의 문제 정의다. 같은 그룹이 뒤에 이 축을 정량화했다 (`minnmann2021` · `bielefeld2019` · §7f).

> ⚠⚠ **그림이 본문 서술과 어긋난 곳 6 군데 (벡터 판독 · §10 상세)**
> ① 본문 p.1 *"Li₇P₃S₁₁ and Li₁₀GeP₂S₁₂ … have also been reported to have room temperature conductivities higher than typical liquid electrolytes"* ↔ 자기 `Fig. 1b` 에서 **EC:DEC:LiPF₆ (캡션이 *"the commonly used liquid electrolyte in LIB"* 라 부른 선) 가 그려진 297–236 K 전 구간에서 LGPS · Li₇P₃S₁₁ 보다 위** — 297 K 에서 LGPS −0.035 · Li₇P₃S₁₁ −0.093 dex · 253 K 에서 −0.21 · −0.31 dex. 두 황화물이 이기는 액체는 EC:PC:LiPF₆ 뿐이다 (+0.13 ~ +0.42 dex).
> ② p.1 *"with phosphates and oxides coming close"* ↔ 같은 그림의 상온 회색 띠 (299.9 K) 에서 LLZO · LAGP 는 LGPS 보다 **1.68 · 1.76 dex (≈ 48 · 58 배) 낮다**.
> ③ `Fig. 1b` 의 LGPS 선은 ref 5 (Kamaya 2011) 측정점을 그대로 옮긴 선이 아니다 — litdb `kamaya2011` 벡터 판독과 같은 1000/T 에서 358–228 K 는 **+0.003 ~ +0.105 dex** 위, 213 K 는 −0.04 · 193 K 는 **−0.27 dex** 아래 · 원전 측정 범위 (383–173 K) 의 양 끝이 잘렸다.
> ④ 본문 p.1 *"260 Wh kg⁻¹"* ↔ 캡션 *"270 Wh kg⁻¹"* ↔ 그림 2016 표지 **265.9** ↔ 우리 산수 (3.5 Ah × 3.65 V ÷ 48 g) **266.1** Wh kg⁻¹ — 본문 · 캡션이 서로 다른 쪽으로 반올림했다.
> ⑤ 캡션 *"an extrapolation (represented by the dashed curves) was made for the energy density values after the year 2004"* ↔ 그림의 점선은 **2003.00 년** 꼭짓점에서 시작한다.
> ⑥ `Fig. 2` 캡션 *"a lithium-metal anode (light yellow) that has a theoretical energy density of 3,700 mA g⁻¹"* — 양 (에너지 밀도) 과 단위 (mA g⁻¹) 가 맞지 않고, Li 금속 이론 비용량은 우리 산수로 **3,861 mAh g⁻¹** 다.

---

## 1. 한 줄 요약

2016 년 Giessen 의 Janek · Zeier 가 *Nature Energy* 창간 첫 해에 쓴 4 쪽 Comment 다. Li 이온 전지 (최신 18650 셀 ≈ 770 Wh l⁻¹) 가 물리화학적 한계에 다가간다는 그림 (`Fig. 1a`) 에서 출발해, 고체 전해질 (SE) 의 장점 셋 (전극 간 교차 오염 없음 · Li⁺ 만 움직여 농도 분극 없음 · 고온 안정과 덴드라이트 억제 기대) 과 **다섯 과제 (에너지 · 출력 · 장기 안정성 · 안전 · 비용)** 를 정리한다. **액체만 고체로 바꾼 셀은 부피 에너지 +0 % · 무게 에너지 −10 %, Li 금속 음극을 써야 +70 % · +40 %** (`Fig. 2` · 저자 어림) 라는 계산으로 '에너지 밀도의 큰 이득은 Li 금속뿐' 이라 못 박은 뒤, 정작 두꺼운 Li 음극은 어려울 것이라 보고 **SSB 는 삽입형 음극 + 빠른 동역학 쪽에서 먼저 길이 열릴 수 있다** 고 내다본다. 계면 (Li 쪽 SEI · 양극 코팅 · 공간전하) · 기계 압력 · 복합 전극의 이온 / 전자 percolation · 제조 공정의 *"revolutionary change"* 를 핵심 과제로 꼽았다 (`Fig. 3`). 정량 근거는 대부분 인용 문헌에 있고, 계면 · 압력 · 안전 논의에는 숫자가 하나도 없다.

## 2. 메타
| 저자 | 저널/년 | DOI | 글 종류 | 자료 |
|---|---|---|---|---|
| Jürgen Janek · Wolfgang G. Zeier (JLU Giessen · Janek 은 KIT BELLA 겸) | *Nat. Energy* **1**, 16141 (2016-09-08 게재) | 10.1038/NENERGY.2016.141 | **Comment** (전망 · 원저 아님) | 4 pp · 그림 3 · 표 0 · refs 29 · SI 없음 |

- 같은 권의 ref 4 = `kato2016` (*Nat. Energy* 1, 16030 · 2016-03 게재) 가 이 글의 **유일한 '고출력' 근거**다 — *"a recent study has shown that SSBs may well offer high power densities"* (p.1) · *"they may allow higher current densities and higher operation temperatures"* (p.2–3) · 코팅 → 고전압 (p.3, refs 4 · 16).
- 참고문헌 29: 단행본 장 1 (ref 2) · 웹 자료 2 (refs 20 · 21) · 나머지는 학술지 논문. 저자 이름이 보이는 자기 인용 = refs 2 · 3 (Janek). refs 13 · 14 는 'Wenzel, S. *et al.*' 로만 인쇄돼 있다 (ref 14 의 전체 저자 Wenzel … Zeier · Janek 은 litdb `cronau2021` 참고문헌 목록에서 확인 · ref 13 은 미확인).
- 글 안에 '아지로다이트 (Li₆PS₅X)' · 할라이드 SE 는 **0 회** 나온다 (본문 · 그림 라벨 전수). 우리 계는 이 지도에 없다 (§7h).

---

## 3. 수치 총정리 ★ (⛔ 전부 2 차 · 소환값 — 원전 대조 없이 인용 금지)

> `figure-read ≈ (벡터)` = PDF 안의 벡터 좌표를 축 눈금 최소제곱 1 차식으로 환산한 값 (`tools/litdb/janek2016_readout.py`). 그림이 **그린** 값이지 원전 값이 아니다.

### 3a. Li 이온 전지 기준선 (본문 p.1 · 그림 1 패널 a 캡션 · 벡터)
대상 그림 = `Fig. 1a` (18650 셀 에너지 밀도 연대기).

| 항목 | 본문 · 캡션 | `figure-read ≈ (벡터)` | 우리 산수 / 메모 |
|---|---|---|---|
| 18650 셀 부피 · 질량 | "approximately 16 cm³ · 48 g" (캡션) | — | 18 mm × 65 mm 원기둥 = **16.54 cm³** (이름에서 읽은 치수 · 우리 가정) |
| 최신 셀 (2016) | 3.5 Ah · 평균 3.65 V (캡션 · ref 21) | — | **12.775 Wh** |
| w_vol (2016) | 본문 "up to 770 Wh l⁻¹" · 캡션 "roughly 770" | 사각 표지 2016.03 년 · **771.2 Wh l⁻¹** | 12.775 Wh ÷ 16.54 cm³ = **772.3** (캡션의 16 cm³ 를 그대로 쓰면 798.4) |
| w_grav (2016) | 본문 **260** · 캡션 **270** Wh kg⁻¹ | 원 표지 2015.99 년 · **265.9 Wh kg⁻¹** | 12.775 Wh ÷ 48 g = **266.1** — 그림 · 산수는 266, 본문과 캡션이 서로 반대로 반올림 |
| 2012 (셀 제조사 확인) | 값 미기재 · "confirmed by cell producers [20]" | 사각 **647.3 Wh l⁻¹** · 원 **224.1 Wh kg⁻¹** | 점선 끝 (2012.00 · 650.1 / 224.0) 과 0.5 % 안 — "외삽이 맞았다" 를 그림으로 보인 자리 |
| 1991 첫 상용 셀 | "almost a factor of four" | 실선 시작 1991.01 년 · **199.7 Wh l⁻¹ · 68.8 Wh kg⁻¹** | 2016/1991 = **3.86 (부피) · 3.87 (무게)** ✓ |
| 그림 값의 자기 일관성 | — | w_vol ÷ w_grav = **2.89 (2012) · 2.90 (2016) g cm⁻³** | 48 g 이면 16.6 · 16.55 cm³ — 두 해 모두 같은 질량 · 부피 셀로 환산했다 |
| 외삽 시작 | "after the year 2004" (캡션) | 점선 첫 꼭짓점 **2003.00 년** | 1 년 어긋남 (§10-⑤) |
| 물리화학 한계 띠 | "may soon reach a limit (represented by a bar that refers to w_vol) assuming no unforeseen developments … The exact value of the limit is influenced by how the cell is designed and processed [2]" | 그라데이션 이미지 bbox **800.1–865.6 Wh l⁻¹** · 2001.2 년 – 축 오른쪽 끝 (2019.0) | 한계가 '어디서 시작하는지' 는 그림에 정의가 없다 (그라데이션) · 2016 표지는 띠 아래 끝보다 **28.9 Wh l⁻¹ (3.7 %)** 아래 |
| 축 보정 잔차 | — | 연도 0.024 년 · w_vol 1.24 Wh l⁻¹ · w_grav 0.62 Wh kg⁻¹ | 6 눈금씩 · 눈금 간격이 0.5 pt 안에서 고르지 않다 (손으로 그린 축) |

실선 · 점선 꼭짓점 (`figure-read ≈ (벡터)` · 해 : Wh l⁻¹ / Wh kg⁻¹): 1991 199.7/68.8 · 1992 211.7/72.9 · 1993 245.8/84.7 · 1994 257.8/88.8 · 1995 268.8/92.6 · 1996 277.8/95.7 · 1997 288.8/99.5 · 1998 315.8/108.8 · 1999 339.8/117.1 · 2000 384.9/132.6 · 2001 429.9/148.2 · (2002 꼭짓점 없음) · 2003 470.0/162.0 ‖ 점선 2005 540.0/186.1 · 2007 585.1/201.7 · 2010 630.1/217.2 · 2012 650.1/224.0.

### 3b. 전해질 전도도 지도 (그림 1 패널 b · 벡터) — ⛔ 문헌 곡선을 이 Comment 가 **다시 그린 선**
대상 그림 = `Fig. 1b` (Arrhenius 지도 10 선).

| 선 (ref) | 그려진 범위 (K) | log σ @ 회색 띠 (299.9 K) | @ 298.15 K | @ 273.15 K | 선 기울기 → Ea (σ 형식 · eV) | 휨 (dex) |
|---|---|---|---|---|---|---|
| Li₁₀GeP₂S₁₂ (5) | 369.0 – 192.8 | **−1.83** (14.6 mS cm⁻¹) | −1.86 (13.8) | −2.24 | 0.273 | 0.120 |
| Li₇P₃S₁₁ 유리세라믹 (24) | 305.9 – 241.9 | **−1.89** (13.0) | −1.91 (12.2) | −2.35 | 0.294 | 0.014 |
| Li₃.₂₅Ge₀.₂₅P₀.₇₅S₄ (23) | 332.6 – 232.9 | −2.37 (4.2) | −2.40 | −2.81 | 0.266 | 0.000 (한 선분) |
| EC:DEC:LiPF₆ (25) | **297.2** – 235.9 | — (띠에 안 닿는다) | — | **−2.11** | 0.246 | 0.075 |
| EC:PC:LiPF₆ (25) | **296.0** – 227.7 | — | — | −2.49 | 0.332 | 0.141 |
| P(EO)₁₂-LiTFSI (22) | 367.1 – **304.7** | — | — | — | (0.606) | **0.301** (VTF 꼴로 휜다) |
| Li₇La₃Zr₂O₁₂ (28) | 382.8 – 232.5 | −3.52 (0.30) | −3.55 | −4.04 | 0.317 | 0.000 (한 선분) |
| Li₁.₅Al₀.₅Ge₁.₅(PO₄)₃ (29) | 372.3 – 211.2 | −3.60 (0.25) | −3.64 | −4.17 | 0.361 | 0.013 |
| LiPON (26) | 357.5 – 298.2 | −6.08 (8.4×10⁻⁴) | — (298.2 K 에서 끝) | — | 0.436 | 0.003 |
| Li₃.₅Zn₀.₂₅GeO₄ (27) | 643.3 – 322.2 | — | — | — | 0.532 | 0.030 |

- **회색 띠** = 캡션 *"The vertical grey line marks room temperature"* → 벡터로 **299.9 K** (1000/T 3.334) · 25 °C (298.15 K) 와 1.8 K 차. 액체 두 선은 띠 **바로 아래 (297.2 · 296.0 K) 에서 시작**한다 — 띠 위치에는 액체 값이 그려져 있지 않다.
- **고분자 선**은 304.7 K 에서 끝난다 (상온까지 안 내려온다) — 본문 *"too low for battery operation at room temperature"* 와 같은 방향 · 353 K (80 °C) 에서 −2.13.
- **같은 그림 안 고체 − 액체 (dex · 둘 다 그려진 온도만)**: LGPS − EC:DEC = −0.035 (297 K) · −0.055 (290) · −0.10 (280) · −0.13 (273) · −0.17 (263) · −0.21 (253) · −0.19 (243) · −0.16 (236.5) ‖ Li₇P₃S₁₁ − EC:DEC = −0.093 · −0.13 · −0.19 · −0.24 · −0.27 · −0.31 · −0.32 ‖ LGPS − EC:PC = +0.27 (290) ~ +0.42 (236.5) ‖ Li₇P₃S₁₁ − EC:PC = +0.13 ~ +0.21.
- **LGPS 선 ↔ Kamaya 2011 (litdb `kamaya2011` 벡터 판독 CSV · Kamaya `Fig. 3` 꼭짓점 · 같은 1000/T)**: 358 K +0.003 · 338 K +0.017 · 318 K +0.034 · **300 K +0.068** · 288 K **+0.105** · 273 K +0.088 · 258 K +0.094 · 238 K +0.067 · 228 K +0.056 · 213 K −0.037 · **193 K −0.267** dex (+ = 이 Comment 의 선이 위) · Kamaya 측정 범위 383–173 K 중 이 선은 369–193 K 만 그렸다.
- **축 보정**: 1000/T 잔차 ≈ 0 · log σ 잔차 0.008 dex (y 눈금 간격이 20.6–21.2 pt 로 고르지 않다 → 판독 불확도를 **±0.03 dex** 로 본다) · 위 K 축 눈금 5 개를 아래 1000/T 축으로 되돌린 어긋남 ≤ 0.0099.
- **라벨 ↔ 선 짝**: 10 개 모두 라벨 글자색 = 선 색. **LLZO 와 EC:DEC 는 같은 초록** (0.07, 0.53, 0.26) 이라 점선 (LLZO) · 실선 (EC:DEC) 으로만 갈린다 — 라벨이 자기 선에 더 가까운지까지 도구가 검사했다.
- **홉 수 검산** (`D-2026-09-27-barrier-hop-count` · `tools/sei/collect_neb.py::hop_check` · ν₀ 10¹³ s⁻¹ **가정** · 298 K): 그림 선 기울기 Ea 0.273 (LGPS) · 0.294 (Li₇P₃S₁₁) eV → Γ ≈ 2.5×10⁸ · 1.1×10⁸ s⁻¹ · 평균 대기 ≈ 4 · 9 ns — '상온 초이온 전도' 서술과 차수 모순 없음 (차수 검산 · 확산계수 아님 · ⚠ 이 기울기는 원전 Ea 가 아니라 다시 그린 선의 기울기다). 고분자 선은 VTF 꼴 (휨 0.30 dex) 이라 이 검산 대상이 아니다.

### 3c. 에너지 밀도 어림 (그림 2 · p.2 — 저자 어림 · 입력 미기재)
대상 그림 = `Fig. 2` (세 셀 구조 모식 · 화살표의 에너지 밀도 변화).

| 항목 | 값 (원문) | 근거 (원문) | 우리 산수 / 메모 |
|---|---|---|---|
| LI-SSB (흑연 음극 · 전극 속 액체 + 분리막을 SE 로) | **w_vol +0 % · w_grav −10 %** | "As SEs have a higher density than liquid electrolytes, the gravimetric energy density is lower" | 밀도 · 두께 · 공극률 입력 미기재 → **재현 불가** |
| LiM-SSB (Li 금속 음극) | **w_vol +70 % · w_grav +40 %** | "taking into account the high specific capacity of lithium metal (left, LiM-SSB) and complete replacement of the graphite and anode electrolyte" | 재현 불가 · 본문 p.2 *"an increase of up to 70% in energy density"* 와 같은 수 |
| Li 금속 '이론 에너지 밀도' | **"3,700 mA g⁻¹"** (캡션 그대로) | — | 단위 오류 — 비용량이면 mAh g⁻¹ · F/(3.6·M_Li) = **3,861 mAh g⁻¹** (M_Li 6.941 · 우리 상수) |
| 4.2 → 5 V | "an increase of more than 20% in energy density (depending on additional cathode capacity at high voltage)" | — | 전압만이면 **+19.0 %** → '20 % 넘게' 는 용량 증가를 같이 가정한 수 (괄호 단서와 맞다) |
| Li 두께 | "A 20-µm-thick lithium layer is needed to replace the much thicker standard graphite anode of a typical LIB thick-film cell" | — | 20 µm × 0.534 g cm⁻³ × 3,861 mAh g⁻¹ = **4.12 mAh cm⁻²** (치밀 Li · 우리 상수) |
| 박막 전지 | "only about 1 µm of lithium is cycled [12]" | ref 12 | **0.21 mAh cm⁻²** — 20 µm 의 1/20 |

### 3d. 셀 구조 · 공정 · 비용 (p.3 · 그림 2 캡션)
- LIB: 분리막 **≈ 10 µm** · 전극 **≈ 100 µm** 씩 (캡션) · top-of-the-range 18650 은 전해질층 **≤ 10 µm** + 다공 전극 속 액체 → **액체 부피 분율 ≈ 25 %** · 최적화 LIB 는 "a few µl of electrolyte per cm² cell" (본문).
- LIB 셀 가격 **US$145 kWh⁻¹** → 수년 안 **US$100** 전망 — 출처는 "public company reports and forecasts" (참고문헌 없음).
- US$100 kWh⁻¹ ≈ **US$30 kg⁻¹** (셀 수준 재료 + 제조) — 우리 산수로 **300 Wh kg⁻¹** 셀을 깐 환산이다 (본문의 2016 셀 260–270 Wh kg⁻¹ 이면 US$26–27 kg⁻¹).
- *"No reliable cost estimate for SSB production is available yet."*
- 고분자 SE: EV 운전 **> 80 °C** 필요 · 그래도 율속 제한 (ref 6).

### 3e. 이 글에 **없는** 것 (n/a)
전위 창 수치 (V) · 계면 저항 (Ω cm²) · 압력 (MPa) · 덴드라이트 임계 전류 · H₂S / SO₂ 양 · 공간전하층 두께 · SSB 셀 에너지 밀도의 계산 입력 — **하나도 없다**. 계면 · 압력 · 안전 · 공간전하 논의는 전부 정성이다.

---

## 4. 글의 구조 지도 (절 → 주장 → 근거)

| 절 (쪽) | 핵심 주장 | 근거 | 그림 |
|---|---|---|---|
| 도입 (p.1) | LIB 770 Wh l⁻¹ · 260 Wh kg⁻¹ (10 년 전엔 예상 못 함) · 곧 한계 · SSB 는 고에너지 + 고출력 가능 · 느린 동역학은 '아킬레스건' 이라 여겨졌지만 최근 연구가 고출력을 보였다 | refs 1–4 | `Fig. 1a` |
| Solid electrolytes (p.1) | SE 장점 셋 · 고분자는 상온 부족 · EV > 80 °C · 무기 황화물 일부 > 액체 · 그러나 **낮은 열역학 안정성** (저전위 환원 · 중간 전위 산화) → 보호 계면상 필요 · 결정질 무기 최고 · 인산염 · 산화물 근접 · 티오인산염 연성 (치밀 양극 복합체 쉽다) · 산화물 취성 (균열) | refs 4–9 | `Fig. 1b` |
| Key performance measures (p.1–2) | 다섯 과제 · LIB 는 성숙 → SSB 는 핵심 성능에서 '큰 도약' 이 있어야 경쟁자 | ref 10 | — |
| Energy density (p.2) | 액체만 교체 → +0 / −10 % · 4.2 → 5 V 는 +20 % 이상 · 산화물 / 인산염 SE 는 고전압을 견딜 것으로 **기대** · Li 금속: 대부분 SE 와 열역학 불안정 → 보호막 · SEI 필요 · 20 µm Li 의 불균일 용해 / 석출 → 기계 파괴 · 입계 덴드라이트 · 충분히 빠른 용해 / 석출 필요 · *"There is reasonable doubt whether all these problems can be solved"* · 성공하면 +70 % · 박막 전지 (1 µm Li) 는 잘 된다 | refs 8 · 11 · 12 | `Fig. 2` |
| Power density (p.2–3) | 고체 열전도 ↑ → 열 방출 · 고전도 SE 면 전극 접촉이 율속 · 고체–고체 접촉은 제조 조건 의존 · SSB 전극 동역학 자료 부족 · SE 는 탈혼합 (분극) 없음 → 고전류 · 고온 · 그러나 SE/양극 접촉이 고전위에서 **'정류 (diode) 접촉'** 가능 (SE 안 Li 고갈층) → 추가 보호 필요 · *"Whether fast kinetics turns out to be one of the key advantages of SSB is an open and inspiring question"* | ref 4 | `Fig. 3` |
| Long-term stability (p.3) | 최고 SE 도 열역학 안정 범위 좁음 · 창은 아직 연구 대상 · Li 금속과 닿으면 대부분 황화물 반응 → 계면상 · **고전도 SEI 면 장기 OK · MCI 면 급속 열화** · 양극 쪽 불안정 · 코팅이 장기 안정 · 고전압 · 고에너지를 가능하게 하는 듯 · 그러나 계면상 안정성은 여전히 과제 · 교차 오염은 막지만 부반응 산물은 계면에 남는다 · Li 음극 자체의 동역학 불안정 (방전 중 공극 · 충전 중 덴드라이트) | refs 13–16 | `Fig. 3` |
| Safety (p.3) | 산화물 세라믹만 쓰면 안전 '보장' · 그러나 최적 이온전도체는 황화물 · 손상 시 H₂S · SE 산화 시 SO₂ · 가넷 유망하나 기계적으로 단단 (soft 아님) · 입계로 덴드라이트 침투 → 단락 · 보호 기술은 제조 복잡 · 비용 ↑ → *"safety may not automatically be enhanced in SSBs"* | refs 17 · 18 | — |
| Architecture and processing (p.3–4) | 비용 US$145 → 100 · US$30 kg⁻¹ · LIB 전해질 '칵테일' · 시트 권취 / 적층 후 주입 · 액체 25 % · SSB 는 작은 SE 입자가 활물질 · 다른 SE 입자와 좋은 접촉 · **독립 전자 전도망** · 이온 · 전자 **percolation** · 부피 변화 → 기계 건전성 · 공극 · 균열 · 접촉 손실 → 계면 저항 · 과전압 · 용량 감소 · 연한 황화물 · 티오인산염 유리가 도움 · 기계 혼합 · 접촉이 기계 효과에 민감 → *"revolutionary change of production technology"* · 쌍극 직렬 적층 → 에너지 밀도 이점 | — | `Fig. 3` |
| Towards a solid future (p.4) | 세 결론 · 고체는 농도 분극 없이 고전류 → 삽입형 음극 · 양극으로도 고출력 (*"lithium-metal anodes probably do not offer high power densities"*) · 편견 · 오판 → 과한 낙관 / 비관 · 예측 | — | — |

---

## 5. 절별 상세 (본문 순서 · 그림 실독 포함)

### 5.1 도입 (p.1)
- LIB 는 에너지 · 출력 밀도 · 신뢰성 · 사이클 수명에서 효율적인 저장 장치로 증명됐다 (ref 1). 최신 LIB 는 **770 Wh l⁻¹ · 260 Wh kg⁻¹** — *"which was not expected 10 years ago"*. 그러나 기존 LIB 의 에너지 밀도는 *"will soon reach its limit"* (ref 2 · `Fig. 1a`).
- 더 높은 에너지 · 출력 밀도 수요 → SE 를 쓰는 SSB 가 둘 다 줄 수 있다 (ref 3). *"While slow kinetics is considered the Achilles' heel of solid-state systems, a recent study has shown that SSBs may well offer high power densities"* (ref 4 = `kato2016`).
- 글의 질문 넷 (§0).
- 🔎 우리 읽기: '고출력' 근거가 `kato2016` 하나다. 그 digest 는 Ragone 이 **LiCoO₂ 질량 기준**이고 셀 기준 (`Table S4`) 이면 전고체 16–33 < Li 이온 73 Wh kg⁻¹, 고출력 자료는 **100 °C** 라고 적었다 — 이 Comment 는 그 정규화 · 온도 단서를 옮기지 않았다.

### 5.2 Solid electrolytes (p.1)
- **장점 셋** — ① 전극 간 화학적 *"cross-talk"* 차단 (Li–S 의 폴리설파이드 셔틀 · LIB 의 전이금속 용출이 없다) · SE 는 Li⁺ 만 옮기고 전자전도가 무시할 만해 자가방전이 작은 '기능성 분리막' · 액체는 Li⁺ 와 음이온이 다 움직여 전류 중 염 농도 구배가 생기고 전류를 제한하지만 SE 는 Li⁺ 만 움직여 *"this bulk polarization cannot occur"* → 더 높은 전류 · 더 빠른 충전 ② 일부 무기 SE 는 고온 안정 → 안전 · 전도도는 온도와 함께 늘어 *"may even reach that of liquid electrolytes"* (ref 5) ③ 기계적 강성이 Li 전착 덴드라이트를 막아 Li 금속 음극을 쓰게 해 줄 *"may"*.
- **분류**: 무기 (결정 · 유리 · 유리세라믹) · 유기 고분자 · 나노입자 분산 '준고체'.
- **고분자**: 부피 변화를 탄 · 소성 변형으로 받아 주는 '자연스러운 선택' 이지만 상온 σ 부족 · EV 에서는 **> 80 °C** · 그래도 율속 제한 (ref 6) · 고온에서는 적절한 고분자로 Li 음극을 안전하게 돌릴 수 있다 · *"the search for stable polymer electrolytes for use with lithium-metal anodes and lithium nickel cobalt manganese oxide or lithium nickel cobalt aluminum oxide cathodes at ambient temperature at sufficient C-rates is one of the challenges"*.
- **무기**: 고전류 성능 잠재력이 최근 보였다 (ref 4) — *"pointing to a misconception that SEs are inherently poor conductors at ambient temperature"*. 삼원 · 사원 황화물 · 티오인산염 (Li₇P₃S₁₁ · Li₁₀GeP₂S₁₂, refs 5 · 7) 은 **상온 σ 가 액체보다 높다** 고 보고됐다 (→ 자기 `Fig. 1b` 와 어긋남 · §10-①).
- **단점**: *"the major drawback of many inorganic SEs is their low thermodynamic stability [8]. Most solid electrolytes are easily reduced at low potentials (for example, by lithium metal) — just like their liquid competitors — and oxidized at intermediate potentials. Protecting interphases are therefore required to stabilize the electrolyte/electrode contact [9], as happens in conventional lithium-ion batteries."*
- **계열 비교**: 결정질 무기가 최고 · *"with phosphates and oxides coming close"* (→ §10-②) · 티오인산염은 연성이라 치밀한 양극 복합체를 쉽게 만들고 산화물은 취성이라 균열로 자주 파괴된다.

### 5.3 Key performance measures (p.1–2)
LIB 는 성숙했고 시장은 kWh 당 원가 경쟁과 성능 개선이 지배한다 → SSB 는 핵심 성능 하나 이상에서 *"significant performance jump"* 를 줘야 주요 경쟁자가 된다. 보통 에너지 밀도가 최우선이지만 빠른 충전에는 출력 밀도가 중요 · 장기 안정성 (사이클 · 달력 수명) 은 SSB 전극 부피 변화가 만드는 기계적 변형 때문에 핵심 요건 · 안전은 최신 LIB 에서 덜 급하지만 에너지 · 출력을 더 올리면 SSB 에도 문제가 될 수 있다 · kWh 당 비용은 제조 기술에 크게 의존 (ref 10). → **다섯 과제 = 로드맵**.

### 5.4 Energy density (p.2) · `Fig. 2`
- 실용 에너지 밀도는 비활성 성분 (전해질 · 첨가제 · 금속 박 …) 과 활물질의 실제 용량 한계를 다 넣어 어림해야 한다.
- **액체만 SE 로** → 부피 에너지 그대로 · SE 가 더 무거워 무게 에너지는 낮아진다 (`Fig. 2` LI-SSB +0 / −10 %).
- **4.2 → 5 V** → 에너지 밀도 20 % 넘게 (추가 양극 용량에 따라) → SE 를 쓰는 이점은 **5 V 급 고전압 양극** 이나 액체와 못 쓰는 고용량 재료 (Li 금속) 를 열 때 생긴다. *"Oxide- or phosphate-based solid electrolytes are expected to chemically withstand high voltages, while liquid electrolytes are not stable at these voltages."* (→ 그 '기대' 를 이 글의 ref 8 로 다시 읽으면 §7b)
- **Li 금속**: SE 는 기계 강도로 덴드라이트를 막는 '조력자' 로 흔히 여겨지지만 *"a realistic assessment of the problems in the way of the successful integration of lithium-metal anodes is missing"*. 대부분 Li SE 는 Li 금속에 열역학적으로 불안정 (refs 8 · 11) → 보호막 또는 안정한 SEI 필요 · 18650 같은 후막 셀의 흑연을 대체하려면 Li **20 µm** 가 필요하고, 그만한 두께의 불균일 용해 · 석출은 심한 기계 변형 → 파괴 · 결정질 SE 에서는 입계를 따라 덴드라이트 → 빠른 단락 · 용해 / 석출은 수용 가능한 C 율만큼 빨라야 한다. *"There is reasonable doubt whether all these problems can be solved."* 성공하면 **+70 %** — *"serious attempts are surely worth the effort"* · 박막 전지 (면적 용량 작음 · Li ≈ 1 µm 순환) 에서는 Li 금속이 잘 된다 (ref 12).
- **`Fig. 2` 실독**: 세 셀이 같은 크기 상자로 그려져 있다 — 왼쪽 **LiM-SSB** (연노랑 Li 금속 층 + 주황 (분리막 SE) + 보라 (양극) · 짙은 주황 (전극 속 SE)) · 가운데 **LIB** (빨강 Cu 박 · 회색 흑연 입자 · 얇은 회색 분리막 띠 · 보라 양극 입자 · 회색 Al 박 · 연한 파랑 배경 = 액체) · 오른쪽 **LI-SSB** (흑연 + SE 혼합 음극 · SE 분리막 · 양극 + SE). 화살표에 **w_vol +70 % · w_grav +40 %** (← LiM-SSB) · **w_vol +0 % · w_grav −10 %** (→ LI-SSB). 상자 크기는 에너지 밀도를 나타내지 않는다 (모식도). ⚠ 두 SSB 그림에도 입자 사이에 연한 파랑 배경이 남아 있다 — 캡션은 그 색을 설명하지 않는다 (공극인지 · 그림 바탕인지 모름). 캡션: *"Using the same SE in the electrodes and the separator appears to be a natural choice, yet for stability and production reasons, a different SE might be more favourable."*

### 5.5 Power density (p.2–3)
- 빠른 충방전 = 고전류 → 재료 열화 · 발열 (셀 임피던스 의존) · 고체는 대개 열전도가 액체보다 커 열을 빨리 내보내고 열점을 막을 수 있다.
- 고전도 SE 로 만들면 **전극 접촉이 셀 동역학을 정한다** · 고체–고체 접촉은 제조 조건에 의존하고 동역학적 병목이 될 수 있다 · *"there is not much information available on the kinetics of electrodes in SSBs yet"*.
- SE 는 강체 구조라 탈혼합 (액체의 벌크 분극) 이 없어 더 높은 전류 밀도 · 더 높은 운전 온도를 허용할 수 있다 (ref 4).
- 반대로 *"solid electrolyte/cathode contacts may form 'rectifying' contacts with blocking kinetics in one direction (such as a diode) at high potentials, due to the formation of lithium depletion layers in the SE, and additional interface protection may be necessary."* — **인용 없음**. (litdb 에서 이 그림을 받치는 계산 원전은 이 글보다 앞선 `haruyama2014` 다 — §11-⑥)
- *"Whether fast kinetics turns out to be one of the key advantages of SSB is an open and inspiring question, and the answer could offer a completely counter-intuitive approach."*

### 5.6 Long-term stability (p.3)
- 장기 안정성은 SSB 개발의 큰 동기지만 *"far from what might naively be expected, the best solid electrolytes show relatively small thermodynamic ranges of stability [13,14] and their electrochemical window is still a subject of research."*
- *"Once in contact with lithium metal, most of the sulfides and thiophosphates react and form an interphase. If a highly conductive solid electrolyte interphase is formed, long-term operation will be secured; however, mixed conducting interphases will lead to fast deterioration of the SSB."* ← 우리 li2s 트랙의 질문 (§7d)
- 양극 쪽에도 계면 불안정 (ref 15) · 양극 입자 코팅이 장기 안정 · 고전압 운전 · 고에너지 셀을 가능하게 하는 듯 (refs 4 · 16) · *"the stability of the interphases remains challenging"*.
- SSB 도 LIB 처럼 계면 불안정 · 열화를 겪는다 — SE 가 교차 오염은 막지만 *"the unwanted products of side reactions form and stay at the interface"*.
- Li 음극 자체의 동역학적 불안정 — **방전 중 공극 (pore) 형성 · 충전 중 덴드라이트** — 도 더 연구가 필요하다.

### 5.7 Safety (p.3)
- *"If only oxide ceramic components (which are stable against lithium) were used, the safety of high-energy batteries would be guaranteed. However, the best-suited ionic conductors are unfortunately sulfides. The formation of toxic H₂S in case of battery damage or the formation of SO₂ by oxidation of the solid electrolyte may present a potential risk [17]."*
- 가넷 (LLZO) 이 더 안정해 유망 — 그러나 산화물은 *"not as mechanically soft [18]"* 이고, *"even though initially believed otherwise, dendrites may enter into polycrystalline solids along grain boundaries and lead to short-circuits and mechanical failure."* · 정교한 보호 기술이 필요할 수 있고 그것이 제조를 복잡하게 하고 비용을 올린다 → *"safety may not automatically be enhanced in SSBs, especially when the risk of mechanical failure is considered."*
- 정량 0 — H₂S · SO₂ 양 · 열폭주 조건 · 셀 시험이 없다.

### 5.8 Architecture and processing of SSB (p.3–4) · `Fig. 3`
- LIB 의 높은 원가가 EV 대량 생산의 장애 · 셀 제조사 경쟁으로 **US$145 kWh⁻¹** · 수년 안 **US$100** 전망 · SSB 원가 추정은 아직 없다 · US$100 kWh⁻¹ ≈ US$30 kg⁻¹ → *"which will not leave much room for complex materials processing in SSBs"*.
- LIB 전해질 = 유기 용매 (주로 카보네이트) + 전도염 (대개 LiPF₆) + 기능성 첨가제 '칵테일' · 전극 시트와 분리막을 권취 / 적층하고 전해질을 주입할 뿐 · 최적화 LIB 는 cm² 당 몇 µl · top-of-the-range 18650 은 전해질층 ≤ 10 µm + 다공 전극 속 액체 → 액체 ≈ 25 vol%.
- **SSB 미세구조** (`Fig. 3`): 액체는 전극 접촉 · 이온 경로를 보장하지만 SE 는 작은 입자들이 활물질 · 다른 SE 입자와 잘 닿아야 하고, **독립적인 전자 전도 입자망** 도 따로 있어야 한다 — *"solid composite electrodes ensuring sufficient electronic and ionic percolation have to be formed"*. 삽입 전극은 부피가 변하므로 복합체의 기계적 건전성이 핵심 · 액체 속 전극은 '숨 쉬며' 가역 순환하지만 고체 복합체에서는 공극 · 균열 · 입자 접촉 손실 → 계면 저항 · 과전압 · 용량 감소 · 연한 황화물 · 티오인산염 유리가 도움 · 기계 혼합이 필요하고 입자 접촉이 기계 효과에 극히 민감 → *"solid electrolyte-based batteries will probably require a revolutionary change of production technology"* · 쌍극 직접 적층 (셀 직렬 연결 · 액체 LIB 에선 불가) → 에너지 밀도 이점.
- **`Fig. 3` 실독** (자동 크롭 + 오른쪽 삽입도 600 dpi 확대):
  - 가운데 셀 모식도: 왼쪽 연노랑 Li 금속 · 주황 SE 입자 + 보라 양극 입자 복합체 · 양옆 **파란 화살표 6 개 = 기계 압력** (*"required both to avoid contact loss due to local volume changes upon lithiation/delithiation and to achieve high power density"*).
  - 왼쪽 위 삽입도: **Li metal | SEI (주황 띠) | SE 입자** — 저항 세 개가 화살표로 표시: R_SE/SEI (SEI–SE 접촉) · R_SE (입자 안) · R_SE,gb (입계).
  - 왼쪽 아래 삽입도: Li 금속에서 SE 입자 사이로 뻗은 별 모양 **'Dendrites'**.
  - 오른쪽 삽입도: 큰 주황 입자들 사이에 파란 고리 (코팅) 를 두른 두 입자 = **'Coated cathodes'** · 빨간 선 = 전위 φ 강하 (왼쪽 'Li⁺-depleted SE' 라벨에서 수평 → 코팅 고리를 가로질러 대각선 상승 → 입자 안에서 다시 수평 · 오른쪽 괄호 φ). ⚠ 이 삽입도는 양극 입자도 **주황** (= SE 색) 으로 그렸다 — 가운데 모식도 · `Fig. 2` 의 '보라 = 양극' 과 색 규약이 다르다. 그리고 '코팅' 과 '공간전하 (Li 고갈 SE)' 를 한 그림에 겹쳐 그려, 캡션의 *"could also be avoided by employing a coating"* (코팅이 공간전하를 없앤다) 와 달리 그림만 보면 코팅이 있는 입자에서 φ 가 떨어지는 것처럼 읽힌다 (§10-⑨).

### 5.9 Towards a solid future (p.4)
- 계면 반응 · 셀 구조 · 성능의 이해는 아직 초기 · 분명한 세 가지 (§0) · 고체는 농도 분극 없이 고전류를 허용 → 삽입형 음극 · 양극 SSB 로도 고출력 (*"lithium-metal anodes probably do not offer high power densities"*).
- *"SSBs as a concept are connected with prejudices and misjudgments — leading to overly optimistic or pessimistic views."* · 핵심 문제 다수가 아직 안 다뤄졌다.
- 예측 (§0-4).
- 🔎 우리 읽기: `Fig. 2` 캡션 (*"Only with a lithium-metal anode … can a significant gain in energy density be achieved"*) · 결론 ③ (*"only the lithium-metal anode really brings a major advantage to SSBs with respect to energy density"*) 과 예측 (*"the employment of thick lithium anodes seems unlikely"*) 을 합치면 이 글의 내기는 **"SSB 의 첫 가치는 에너지가 아니라 동역학"** 이다. 그 동역학의 유일한 근거가 `kato2016` (100 °C · LCO 질량 기준) 이라는 점이 이 글의 가장 얇은 고리다 (§10-⑦).

---

## 6. 논증 흐름 종합 — 어디가 근거이고 어디가 의견인가

| 주장 | 근거 종류 | 이 digest 의 판정 |
|---|---|---|
| LIB 에너지 밀도가 곧 한계 | ref 2 (단행본 장) + `Fig. 1a` 의 그라데이션 띠 (정의 없음) | 의견 + 정성 그림 |
| 황화물 상온 σ > 액체 | refs 5 · 7 | **자기 `Fig. 1b` 와 어긋남** (EC:DEC 가 위 · §10-①) |
| SE 는 낮은 열역학 안정성 · 보호 계면상 필요 | ref 8 (계산 · grand potential) | 원전 있음 (`zhu2015`) — 층① 진술 |
| 산화물 / 인산염 SE 는 고전압을 견딜 것 | **인용 없음** ('expected') | ref 8 의 층① 값과 부분 모순 (§7b) |
| 액체만 교체 → +0 / −10 % · Li 금속 → +70 / +40 % | 저자 어림 · 입력 미기재 | 재현 불가 |
| 고출력 가능 | ref 4 하나 | `kato2016` digest 의 단서 (100 °C · LCO 질량 기준) 가 빠졌다 |
| 정류 접촉 · Li 고갈층 | **인용 없음** | 정성 가설 (litdb 원전 `haruyama2014` 는 인용 안 함) |
| 고전도 SEI 면 장기 OK · MCI 면 급속 열화 | refs 13 · 14 (litdb 미보유) | 프레임 · 정량 기준 없음 |
| H₂S · SO₂ 위험 | ref 17 (litdb 미보유) | 정성 |
| 산화물은 soft 아님 · 입계 덴드라이트 | ref 18 · 인용 없음 | 정성 |
| 비용 US$145 → 100 · US$30 kg⁻¹ | "public company reports" (참고문헌 없음) | 출처 없음 |
| 복합 전극 percolation · 접촉 손실 · 제조 혁명 | **인용 없음** | 의견 (뒤 문헌이 정량화 · §11) |
| 세 결론 · 예측 | — | 의견 |

→ 이 글의 '증거' 는 인용 문헌과 `Fig. 1` (산업 자료 + 문헌 곡선) 에 있고, 나머지는 **2016 년 시점 연구 그룹의 우선순위 선언**이다. 그 선언이 뒤에 얼마나 맞았는지가 이 digest 의 실제 쓸모다 (§11).

---

## 7. 우리 DFT · 트랙과의 대조 ★★ (`../our_dft_baseline.md` · `db/properties/` · 값이 아니라 질문의 대응)

> 규율: 이 글은 **값이 없는 전망**이다 — 우리 숫자와 같은 표에 놓을 숫자가 없다. 아래는 *질문 · 층 · 정의* 만 맞댄다.
> 우리 MD 의 σ · D · Ea 절대값은 싣지 않는다 (계 간 상대 차만). cascade 는 **상대값 · 등급만** (`D-2026-11-05-cascade-axes-bundle-closed` — MP 갭 · 반응 에너지 절대값 금지) · li2s 는 마감 기록의 허용 · 금지 문장만.

### 7a. "low thermodynamic stability" — 이 글은 2016 년에 이미 **층①** 편에 섰다

| 출처 | 창을 무엇으로 봤나 | 층 |
|---|---|---|
| `kamaya2011` (ref 5 · 2011) | Li/LGPS/Au CV 에서 "−0.5–5 V 분해 전류 없음" → '넓은 창 (> 5 V)' | **겉보기** (`kamaya2011` §5.2 벡터 판독: 산화 쪽 전류 0 아님) |
| **이 Comment (2016)** | ref 8 (Zhu 2015 grand potential) 을 들어 *"easily reduced at low potentials … and oxidized at intermediate potentials"* | **층① (열역학 분해 개시)** |
| `zhu2015` (ref 8) | Li₃PS₄ · LGPS 환원 1.71 V · 황화물 산화 2–2.5 V · Li₆PS₅Cl 포함 8 황화물 계산 | 층① |
| 우리 (`our_dft_baseline.md`) | LPSCl (comp1 = modelc) 산화 개시 **2.256 V** (GG 상 집합 · LiS₄ 포함하면 2.14 V) · 환원 한계 **1.717 V** (라벨 정정 2026-09-22) | 층① |
| 우리 셀 작동창 (CLAUDE.md · 사용자 2026-11-09) | 양극 쪽 판단은 **2.5–4.25 V vs Li** — 층① 개시가 창 아래라 **창 전체가 열역학적 산화 구간** → '안정' 은 창 안의 분해 산물 · 부동태로 | 셀 · 판단 규칙 |

- **판정**: 이 글의 *"Protecting interphases are therefore required"* 와 우리 창 규칙은 **같은 결론**이다. 그리고 litdb 계보에 적어 둘 것 — 5 년 사이 분야의 해석이 Kamaya 2011 '> 5 V' (겉보기) 에서 이 글 2016 '층①' 으로 옮겨 갔다. Kamaya (Kanno 그룹) 와 이 글 (Janek 그룹) 은 다른 그룹이라 '한 그룹의 자기 정정' 이 아니라 **분야의 전환**이다 (Kanno 그룹 쪽의 전환은 `kato2016` digest §7a — 첫 효율로 LGPS 의 Li 쪽 약점을 스스로 보였다).
- 이 글의 *"their electrochemical window is still a subject of research"* 는 그 뒤 litdb 에서 둘로 갈렸다: **층① 개시는 치환으로 안 움직인다** (`banik2022` — Zeier 공저 · S 3p VBM 이 개시를 붙잡는다) · **층② (골격 유지 탈리튬화) 는 다른 양** (`schwietert2020` 2.24 V ≠ 우리 층① 2.256 V — 0.016 V 차를 일치로 쓰지 않는다 · `our_dft_baseline.md`).

### 7b. "산화물 · 인산염은 고전압을 견딘다" — 이 글 자신의 ref 8 로 다시 읽기 (b2o3 · CEI 트랙)

| SE (litdb `zhu2015` = 이 글 ref 8 · 층①) | 산화 한계 (V) | 환원 한계 (V) | 이 글의 서술과 |
|---|---|---|---|
| LLZO (가넷) | **2.91** (3.30 V 부터 O₂) | **0.05** (0 V 구동력 최소 · 부동태 쉬움) | Li 쪽은 맞다 · **고전압 쪽은 아니다** (2.91 V 는 우리 창 2.5–4.25 V 안) |
| LISICON | 3.39 | 1.44 (Ge 환원) | 둘 다 아니다 |
| LLTO | 3.71 | 1.75 (Ti⁴⁺ 환원) | 둘 다 아니다 |
| LATP (NASICON 인산염) | **4.21** | 2.17 (Ti) | 고전압 쪽만 근접 |
| LAGP (NASICON 인산염) | **4.27** | 2.70 (Ge) | 고전압 쪽만 근접 |
| LiPON | 2.63 (N₂) | 0.68 | 둘 다 아니다 |

- **판정**: *"Oxide- or phosphate-based solid electrolytes are expected to chemically withstand high voltages"* 는 층① 으로는 **NASICON 인산염 (4.2–4.3 V) 에만** 맞고, *"oxide ceramic components (which are stable against lithium)"* 는 **LLZO 하나에만** 맞는다 — 이 글이 인용한 바로 그 계산 (ref 8) 이 보인 그림이다. 이 글은 그 표를 일반화했다 (§10-⑥). ('5 V 에서 분해 구동력이 작다 (≈ −0.06 eV/atom)' 는 `zhu2015` 가 LATP · LAGP 에 대해 따로 적었다 — 동역학적으로 버티는 이유 후보다.)
- **우리 쪽 (O 를 넣은 황화물 · b2o3 / CEI 맥락)**: 우리 O 단독 대조 (`o_only_03` · `kb/concepts/se_redox_frontier.md` 4 장 ④) 의 창 안 평형 산물은 **Li₃PO₄ (2.50–2.70 V) → Li₄P₂O₇ (2.70–2.91) → LiPO₃ (2.91–3.69) → P₂O₅ (3.69–4.25)** 이고 O 는 끝까지 −2 다. ⇒ '인산염이 고전압을 견딘다' 는 **P–O 골격 (O 가 산화되지 않는다)** 의 뜻으로는 맞지만, **Li₃PO₄ 라는 상** 은 이 혼합에서 창 맨 아래 0.2 V 에서만 평형이다 — 'Li₃PO₄ 계 CEI' 대신 '인산염 계 CEI' 로 읽는 우리 카드의 판단이 이 글의 2016 직관을 더 정확하게 만든 판이다.
- **b2o3 트랙** (BO-LPSC1.6 · B 자리 UMA 탐색): 이 글은 붕산염 · 산화물 첨가를 다루지 않는다 — 연결은 '황화물에 O 를 넣는 동기 (고전압 쪽)' 라는 일반 전제까지다. 값 대조 없음.

### 7c. 안전 — H₂S · SO₂ ↔ 우리 CEI 산물 목록 · cascade 축 ②
- **SO₂**: 이 글 (2016) 은 *"the formation of SO₂ by oxidation of the solid electrolyte"* 를 위험으로만 적었다 (정량 0). 같은 Giessen 그룹의 `zuo2022` (2023 *Angew.*) 가 아지로다이트 / NCM85 복합양극 셀에서 **DEMS 로 SO₂ (m/z 64) 를 실측**했고, Cl-rich (Li₅.₅PS₄.₅Cl₁.₅) 가 ≈ 5.7 배 (⚠ a.u. · 교정 몰비 아님 · 방향만) — 우리 modelc (Cl-rich) 쪽 방향의 문헌 사례다. 우리 CEI 트랙 (Nd 계면 · 1저자 = 실험 쪽 다른 사람) 의 생성물 11 종 목록에 **SO₂ (분자결정)** 가 들어 있다 (`db/properties/cei_product_gap_card_2026_10_27.json` · 분자결정은 MP 셀 고정 · 값은 여기 옮기지 않는다).
- **H₂S**: 이 글의 시나리오는 '전지 손상 (수분 노출)' 이다. 우리 cascade 축 ② (가수분해 · H₂S 몫) 는 묶음 1 에서 **G4 불통과 → 위험 표시로만** 쓰였다 (`cascade_axes_bundle_closed_2026_11_05.json` 1_확정) — 닫힌계 반응 에너지로 도펀트를 가르지 못했다는 뜻이고, 이 글의 위험 서술을 우리 축이 '정량했다' 고 쓰지 않는다.

### 7d. SEI 대 MCI — li2s 트랙 · cascade 축 ⑥
- 이 글 p.3 의 *"If a highly conductive solid electrolyte interphase is formed, long-term operation will be secured; however, mixed conducting interphases will lead to fast deterioration"* 는 우리 **09-11 계면상 카드의 질문** (*계면에 bulk Li₂S 보다 Li 이동도가 높은 상이 생기는가*) 과 같은 질문이다.
- **li2s (LPSCl@Li₂S · 소셀 유리)** 는 그 질문에 **답하지 못한 채 닫혔다** — 마감 기록 (`lpscl_smallcell_glass_track_closed_2026_10_30.json` · `D-2026-10-30-lpscl-smallcell-glass-track-closed`) 의 금지 서술 그대로: ⛔ *'이 트랙으로 LPSCl@Li₂S 계면상의 Li 이동도 · 전도도를 정했다' 류* · ⛔ *이 트랙의 D · σ · Ea 의 어떤 값도*. 뒤이은 li2s-2 (고정 밀도 창) 도 2026-11-10 닫혔고, **li2s-3** (`lpscl_glass_dense_protocol_ensemble_estimand_2026_11_10.json` · 두 유리 a-Li₄PS₄Cl / a-Li₃PS₄ 의 D 비 R(T) · 상대값만) 이 진행 중이다 — **수송 결과 0 건**.
- **cascade 묶음 2 축 ⑥** (`cascade_axes_bundle2_estimand_2026_11_10.json` · `D-2026-11-10-cascade-axes-bundle2` active) 은 같은 질문을 도펀트 수준으로 옮긴 대리량이다 — Li 금속 쪽 최소 kink 산물 중 **넓은 갭 산물의 부피 분율 φ_wide** (좋은 방향 = 클수록) · 금속성 분율 φ_met 은 **기록만**. 카드 §1c 가 *"금속성 소수상이 득인지 독인지 — MCI 대 MII 논쟁 … 두 학파를 가를 정량 문턱 없음 … 이 카드가 정하지 않는다"* 라고 적었다 ⇒ 이 글의 2016 단정 (*"mixed conducting interphases will lead to fast deterioration"*) 을 우리 카드는 **규칙으로 채택하지 않았다** (방향 미정 · 기록만). 새 축 값은 0 건이다.

### 7e. 부피 변화 · 공극 · 압력 — cascade 묶음 2 축 ⑤ · ④
- 이 글: 전극 부피 변화 → 기계 변형 (장기 안정) · 두꺼운 Li 의 불균일 용해 / 석출 → 변형 · 파괴 · 방전 중 공극 · 기계 압력 필요 (`Fig. 3` 파란 화살표). **정량 0**.
- 10 년 뒤 같은 그룹 (`wang2026` · Mollenhauer\* + Zeier + Janek · *Angew.* 2026) 이 계면 pseudo-binary 의 **ΔV/V** (그 digest 식 3) 를 내고 *"+ΔV → 응력 · 균열 · −ΔV → 계면 공극"* 으로 읽었다.
- 우리 **묶음 2 축 ⑤** = 같은 꼴 ΔV/V 를 91 설계의 최소 kink 반응식 (반충 LiNiO₂ · Li 금속 상대) 에 적용 · 동률 폭 1 %p · **위험 표시 없음** (문턱 근거가 없어서) · 카드 §1c *"응력 · 균열 · 공극 생성 — ΔV/V 는 부피 회계지 역학 예측이 아니다"* · 값 0 건.
- 우리 **묶음 2 축 ④** = 작동창 2.5–4.25 V 8 점에서 도펀트가 어느 산물로 가고 그 산물이 전자를 막는지 (f_ins · F_win) — 이 글의 *"oxidized at intermediate potentials … coating"* 을 도펀트 행방으로 옮긴 축 · 산화 개시는 음성 대조 기록만 (`banik2022`: 치환이 개시를 못 옮긴다) · 값 0 건.
- ⇒ 계보 한 줄: **2016 이 글이 과제로 이름 붙이고 → 2026 같은 그룹이 ΔV/V 기술자를 계산하고 → 우리 묶음 2 가 그 꼴을 도펀트 순위 축으로 쓴다 (결과 전)**.

### 7f. DEM 트랙 — 후막 복합 양극
> 우리 DEM 기준값은 이 브랜치에 없다 (`../our_dem_baseline.md` = 자리표시 · 값 0). 아래는 **정의 · 문헌 앵커**만이다.
- 이 글이 2016 년에 적은 문제 정의: 독립 전자망 · 이온 / 전자 percolation · 부피 변화 → 공극 · 균열 · 접촉 손실 → 계면 저항 · 과전압 · 용량 감소 · 연한 황화물이 도움 · 기계 혼합 · 압력 · 제조 혁명 · 쌍극 적층 · LIB 전극 ≈ 100 µm · 액체 25 vol%.
- 같은 그룹이 뒤에 정량화한 litdb 앵커: `bielefeld2019` (GeoDict 3D 미세구조 + percolation) → `bielefeld2020` (σ_eff + 바인더) · `minnmann2021` (EIS-TLM: **저-CAM = 전자 percolation 병목 · 고-CAM = 이온 수송 병목 · 고-CAM 이면 탄소 무첨가 가능 · SE 미세화 → 이온 tortuosity ↓**) · `minnmann2022` (설계 Perspective) · `trevisanello2021` (다결정 vs 단결정 NCM 균열) · `schmitt2026` (BELLA · PTFE 건식 시트).
- 다른 그룹: `kato2016` (308 µm) → `kato2018` (600 µm · 15.7 mAh cm⁻²) · `doux2020` (압력) · `luan2025` (graded 복합양극 · 5 Ah 파우치) · `hippauf2019` (건식 막 PTFE 0.1 wt%).
- **판정**: 이 글의 '독립 전자망이 있어야 한다' 는 `minnmann2021` 에서 **CAM 함량에 따라** 바뀌었다 (고-CAM 이면 CAM 자체가 전자망) — DEM 에서 전자 percolation 을 따로 모형화할지는 조성 구간이 정한다.

### 7g. C 축 (기계) — "thiophosphates are ductile … oxides are brittle"
- 우리 쪽은 **상대 진술만**: comp1 → modelc 에서 B₀ ↓ · E_VRH ↑ — 방향이 반대 (`our_dft_baseline.md` '핵심 발산') · 절대값은 이 digest 에 옮기지 않는다.
- litdb: `sakuda2013` (*Sci. Rep.* — 상온 가압 치밀화 · 황화물 유리 Young's modulus) 는 **이 글의 ref 18 이 아니다** (같은 저자 · 같은 해 다른 논문) · `doux2020` (LPSCl 은 공극을 가진 다공성 매질 · creep 주체는 Li).
- 이 글의 진술은 정성이라 우리 C 축 값과 맞댈 숫자가 없다.

### 7h. 우리 계 (아지로다이트) 는 이 지도에 없다
- 본문 · 그림에 Li₆PS₅X 0 회. 아지로다이트 원전 ([`deiseroth2008_li6ps5x_argyrodite_high_li_mobility`](deiseroth2008_li6ps5x_argyrodite_high_li_mobility.md) · *Angew. Chem. Int. Ed.* 47, 755 (2008) · 사용자 목록 127) 은 이 글보다 8 년 앞섰고, 이 글의 ref 8 (`zhu2015`) 은 이미 **Li₆PS₅Cl 을 8 황화물 중 하나로** 계산했다 (Deiseroth 2008 구조 · E_hull 83 meV/atom → 0 으로 규약 · 그 digest 표).
- 이듬해 같은 저자들 (`kraft2017` · Zeier\* · Janek) 이 Li₆PS₅X 격자 분극성 논문을 냈고, 그 뒤 `banik2022` (Zeier\*) · `zuo2022` (Janek\*) · `wang2026` (Li₆PS₅Cl 포함 7 황화물) 로 이어졌다 — litdb 기록 기준으로 **이 글 이후 저자들의 주력 계열이 우리 계가 됐다**.
- ⇒ 이 글은 우리에게 **분야의 과제 틀** 을 주지 물질 정보를 주지 않는다.

### 7i. 층위 표 (원고 · 발표용 요약)

| 이 글의 서술 | 층 / 축 | 우리 쪽 대응 | 쓸 수 있는 꼴 |
|---|---|---|---|
| 저전위 환원 · 중간 전위 산화 · 보호 계면상 필요 | 층① (ref 8) | ESW 층① (2.14–2.256 / 1.717 V) · 2.5–4.25 V 창 규칙 | "as already pointed out in 2016" + 원전 Zhu 2015 |
| 산화물 / 인산염 고전압 견딤 | '기대' (인용 없음) | ref 8 층① 표 · 우리 O 단독 대조 (인산염 응축) | ⛔ 일반화로 인용 금지 — NASICON 만 |
| 고전도 SEI vs MCI | 프레임 (refs 13 · 14) | li2s (닫힘 · 미답) · cascade 축 ⑥ (값 0 · φ_met 기록만) | 질문 틀로만 |
| 부피 변화 · 공극 · 압력 | 정성 | cascade 축 ⑤ (값 0) · DEM 압밀 | 과제 목록으로만 |
| SO₂ · H₂S | 정성 (ref 17) | CEI 산물 SO₂ · cascade 축 ② (G4 불통과) | 위험 언급으로만 · 정량은 원전 (`zuo2022`) |
| 복합 전극 percolation | 정성 | DEM (값 없음) · `minnmann2021` 정량 | 문제 정의 인용 |

---

## 8. DFT / 계산 방법 ★

**없다.** code · functional · pseudo / PAW · k-points · ecut · supercell / nat · DFT+U · AIMD · MLIP · 무질서 처리 — 전부 **n/a** (Comment).
- 이 글의 '계산' 은 셀 에너지 밀도 어림 (`Fig. 2` · 입력 미기재) 과 18650 사양 환산 (`Fig. 1a` 캡션) 뿐이다.
- 이 글이 기대는 계산 원전 = ref 8 (`zhu2015` · grand potential · MP) · ref 11 (`zhu2016` · 계면 pseudo-binary) · ref 15 (`richards2016` · pseudo-binary) — 방법은 그 digest 들에 있다.

**Post-processing** — 원문에는 없다. 이 digest 가 한 것:
- `Fig. 1` 벡터 경로 판독 (`tools/litdb/janek2016_readout.py`): 축 눈금 최소제곱 보정 (잔차 문턱) · 표지 중심 · 꺾은선 꼭짓점 · 그라데이션 띠 bbox · 라벨 글자색 ↔ 선 색 · 라벨–선 거리 · 선 안 보간 (외삽 안 함) · x 균등 재표본 60 점 최소제곱 기울기 · 직선 이탈 최대 (휨) · 고체 − 액체 짝 · LGPS 선 ↔ `kamaya2011` 판독 CSV.
- 본문 · 캡션 산수 (상수 계산) · 홉 수 검산 (`tools/sei/collect_neb.py::hop_check`).
- 출력 `litdb/figures/janek2016_solid_future_battery_development/digitized.csv` (224 행 · 열 `figure, series, quantity, value, unit, note` · 없는 값은 `—`).

---

## 9. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1a | 18650 LIB 셀 w_vol (파랑 · 왼축 0–1,000 Wh l⁻¹) · w_grav (빨강 · 오른축 0–500 Wh kg⁻¹) vs 연도 1990–2019 · 실선 1991–2003 (ref 19) · 점선 외삽 2003–2012 · 채움 표지 2012 (647.3 / 224.1) · 2016 (771.2 / 265.9) · 'Physicochemical limit' 그라데이션 띠 ≈ 800–866 Wh l⁻¹ (`figure-read ≈ 벡터`) | 서론의 'LIB 한계' 그림 — 값은 산업 자료 (refs 19–21) 원전으로 · ⚠ 띠는 정의 없는 정성 표시 · 본문 260 · 캡션 270 · 그림 266 Wh kg⁻¹ 불일치 |
| 1b | Arrhenius 지도 log σ (−6.7 ~ 0) vs 1000/T (1.5–5.5) · 위 축 T (K) · 상온 회색 띠 299.9 K · 고체 7 (LGPS · Li₇P₃S₁₁ · thio-LISICON · LISICON · LLZO · LAGP · LiPON) + 고분자 1 + 액체 2 선 (refs 5 · 22–29) | 'SE 지도' 서론 그림의 원형 · ⛔ 선 값 인용 금지 (다시 그린 선 · LGPS 는 Kamaya 와 −0.27 ~ +0.11 dex 차) · ⚠ EC:DEC 가 LGPS · Li₇P₃S₁₁ 위 — '황화물 > 액체' 근거로 쓰지 않는다 · 아지로다이트 없음 |
| 2 | 셀 구조 모식 세 개 — LiM-SSB (Li 금속) ← LIB → LI-SSB (흑연) · 화살표 w_vol +70 % / w_grav +40 % · w_vol +0 % / w_grav −10 % | 'Li 금속이어야 에너지 이득' 의 상징 그림 · 저자 어림 (입력 미기재 · 재현 불가) · 캡션 '3,700 mA g⁻¹' 단위 오류 · DEM 후막 전극 서론 그림 후보 (구조 비교만) |
| 3 | SSB 과제 모식 — Li 금속 · SEI · SE 입자 · 저항 R_SE/SEI · R_SE · R_SE,gb · 덴드라이트 · 코팅 양극 + Li⁺ 고갈 SE (전위 강하 φ) · 파란 화살표 = 기계 압력 | 우리 트랙 지도로 쓸 만한 그림 — 왼쪽 위 = li2s (계면상 수송) · 오른쪽 = CEI / b2o3 (양극 계면) · 화살표 = DEM 압밀 · ⚠ 오른쪽 삽입도의 색 규약 (양극 = 주황) 과 φ 선 위치가 캡션과 어긋나게 읽힌다 |

---

## 10. 비판 — 이 글의 약한 곳 ★

① **자기 그림과 본문이 어긋난다 (황화물 vs 액체).** 본문 p.1 은 Li₇P₃S₁₁ · LGPS 의 상온 σ 가 *"higher than typical liquid electrolytes"* 라 쓰는데, 자기 `Fig. 1b` 에서 EC:DEC:LiPF₆ — 캡션이 *"the commonly used liquid electrolyte in LIB"* 라고 이름 붙인 선 — 가 그려진 **297–236 K 전 구간에서 두 황화물 위**다 (LGPS −0.035 ~ −0.21 · Li₇P₃S₁₁ −0.09 ~ −0.32 dex). 황화물이 위인 것은 EC:PC:LiPF₆ 에 대해서뿐이다. 297 K 차 (0.035 dex ≈ 8 %) 는 판독 불확도 (±0.03 dex) 와 같은 크기라 상온에서는 **'비슷하다'** 가 이 그림이 지지하는 말이다 — `kamaya2011` digest 가 Kamaya 자신의 그림에서 같은 결론을 냈다 (그 digest §5: 초록의 'exceeding' 은 실온에서는 '비슷하다' 가 정확하고 −10 °C 아래에서만 분명). 이 Comment 는 그 표현을 더 세게 옮겼다.

② **"phosphates and oxides coming close"** — 같은 그림의 상온 띠에서 LLZO · LAGP 는 LGPS 보다 **1.68 · 1.76 dex** (≈ 48 · 58 배) 낮다. 두 자릿수 가까운 차를 '근접' 이라 부른 것은 그림과 맞지 않는다.

③ **`Fig. 1b` 는 원전 측정점이 아니라 다시 그린 선이다.** LGPS 선은 `kamaya2011` 벡터 판독 대비 300 K +0.068 · 288 K +0.105 · 193 K −0.267 dex · Kamaya 측정 범위 (383–173 K) 의 양 끝을 잘랐다. 선 기울기 Ea 0.273 eV 는 Kamaya 본문 24 kJ mol⁻¹ (0.249 eV) · 그 digest 재적합 0.253 eV 보다 가파르다. Li₇P₃S₁₁ 선은 298 K 에서 12.2 mS cm⁻¹ · 기울기 0.294 eV 인데, litdb 의 2 차 인용 (`nosrati2026` 리뷰가 옮긴 Seino 2014 값 17 mS cm⁻¹ · 0.18 eV) 과도 다르다 (⚠ Seino 원문은 litdb 미보유 — 원전 대조 아님 · 방향만). 이 그림의 선 값을 원전 값처럼 인용하면 안 된다.

④ **본문 · 캡션 · 그림의 무게 에너지 밀도가 셋 다 다르다** — 260 (본문) · 270 (캡션) · 265.9 (그림) Wh kg⁻¹ · 캡션의 입력 (3.5 Ah × 3.65 V ÷ 48 g) 으로 다시 내면 266.1. 반올림 차이라 결론은 안 바뀌지만, '770 Wh l⁻¹ · 260 Wh kg⁻¹' 짝을 이 글에서 옮겨 쓰면 캡션과 어긋난다.

⑤ **외삽 시작 연도** — 캡션 *"after the year 2004"* ↔ 그림 점선의 첫 꼭짓점 **2003.00** (2002 꼭짓점 없음). 사소하지만 '그림이 무엇을 그렸나' 와 '캡션이 무엇이라 하나' 가 다른 사례.

⑥ **"Oxide- or phosphate-based solid electrolytes are expected to chemically withstand high voltages" · "oxide ceramic components (which are stable against lithium)"** — 둘 다 인용이 없고, 이 글이 바로 앞에서 인용한 ref 8 (`zhu2015`) 의 층① 표와 부분 모순이다: 산화 쪽 4 V 를 넘는 것은 NASICON 인산염 (LATP 4.21 · LAGP 4.27 V) 뿐이고 LLZO 는 2.91 V · LiPON 2.63 V · LLTO 3.71 V 다 · Li 쪽 안정은 LLZO (0.05 V) 뿐이고 LiPON (0.68) · LATP (2.17) · LAGP (2.70 V) 는 환원된다. 계열 일반화가 자기 근거보다 넓다 (§7b).

⑦ **'고출력' 의 근거가 한 편 (ref 4) 이고, 그 한 편의 단서를 옮기지 않았다.** `kato2016` 의 고출력 자료는 **100 °C** 이고 Ragone 은 **LiCoO₂ 질량 기준** — 셀 기준이면 전고체가 Li 이온보다 낮다 (16–33 < 73 Wh kg⁻¹ · 그 digest). 결론의 내기 (*"SSB development may be prompted by the superior kinetics"*) 가 바로 이 근거 위에 서 있다.

⑧ **`Fig. 2` 의 +70 % · +40 % · +0 % · −10 % 는 재현할 수 없다.** 밀도 · 두께 · 공극률 · 용량 입력이 하나도 없다. 같은 캡션의 Li 금속 *"theoretical energy density of 3,700 mA g⁻¹"* 는 양 · 단위 오류이고 값도 우리 산수 (3,861 mAh g⁻¹) 와 4 % 다르다.

⑨ **`Fig. 3` 오른쪽 삽입도** — 양극 입자를 SE 와 같은 **주황**으로 그렸다 (가운데 모식도 · `Fig. 2` 는 양극 = 보라). 그리고 '코팅 양극' 과 'Li⁺ 고갈 SE 의 전위 강하 φ' 를 한 그림에 겹쳐, 캡션 (*"could also be avoided by employing a coating"*) 과 달리 그림만 보면 코팅이 있는 입자에서 φ 가 떨어지는 것처럼 읽힌다 (600 dpi 확대로 확인 · 모식도라 결론에는 영향 없음).

⑩ **정류 접촉 · Li 고갈층 서술에 인용이 없다.** 이 글보다 2 년 앞선 계산 원전 (`haruyama2014` · *Chem. Mater.* 26, 4248 — LCO(110) 능선 O 의 Li 흡착 → LPS 쪽 Li 공공 형성 에너지 하락 · LiNbO₃ 버퍼가 흡착 자리를 없앤다) 이 있었는데 인용하지 않았다. 'diode 같은 정류' 거동 자체를 잰 자료는 litdb 에 없다.

⑪ **참고문헌 오기 · 혼동 위험** — ref 11 저자 **'Zhou, Y.'** → 실제 Yizhou **Zhu** (`zhu2016` 표지) · ref 8 의 학술지명 *"ACS Appl. Mater. Interface"* (정식은 Interfaces) · 본문 Li₇P₃S₁₁ 근거는 ref 7 (Minami 2006) 인데 그림의 Li₇P₃S₁₁ 선은 ref 24 (Seino 2014) — 본문과 그림의 출처가 다르다 · ref 18 은 litdb `sakuda2013` 과 다른 논문.

⑫ **비용 수치에 출처가 없다** — US$145 → US$100 kWh⁻¹ 은 *"public company reports and forecasts"* 뿐 · US$30 kg⁻¹ 환산은 300 Wh kg⁻¹ 셀을 깔고 있는데 (우리 산수) 같은 글의 2016 셀은 260–270 Wh kg⁻¹ 이다.

⑬ **안전 · 계면 · 압력 · 공간전하 논의에 숫자가 0 이다.** 전망 글이라 당연하지만, 그래서 이 글로는 *무엇이 얼마나* 를 하나도 인용할 수 없다 — 이 글을 원고에서 쓸 자리는 '과제 틀' 문장뿐이다.

⑭ **2016 년의 지도에서 아지로다이트가 빠졌다.** 이 글의 ref 8 이 Li₆PS₅Cl 을 이미 계산했는데도 본문 · `Fig. 1b` 에 없다 — 1 년 뒤 같은 저자들의 주력 계열이 된다 (§7h). 지도는 당시 '기록 보유자' (LGPS · Li₇P₃S₁₁) 중심이었다.

---

## 11. 2016 의 예측 · 제안 → 뒤 litdb 문헌 ★★ (litdb 에 있는 것만 · 추측하지 않는다)

> 판정 기호: ✅ 확인 · 🔵 정교화 (방향은 맞고 조건이 붙었다) · 🔴 반박 (litdb 안에서) · ⚪ 판정 불가 (litdb 에 직접 자료 없음). '(2 차)' = 그 litdb digest 자체가 원전을 옮긴 리뷰 기록이다.

| # | 2016 이 글의 주장 (쪽) | 뒤 litdb (slug · 연도) | 그 digest 가 기록한 것 | 판정 |
|---|---|---|---|---|
| ① | 대부분 SE 는 저전위 환원 · 중간 전위 산화 → 보호 계면상 필요 (p.1 · ref 8) | `zhu2016` (2016) · `banik2022` (2022 · Zeier 공저) · 우리 ESW | 전극–SE 계면 pseudo-binary · 치환이 산화 개시를 못 옮긴다 (S 3p VBM) · 우리 층① 2.14–2.256 / 1.717 V · 창 2.5–4.25 V 전체가 산화 구간 | ✅ + 🔵 (층① · 층② 를 갈라 말해야 한다) |
| ② | 산화물 · 인산염 SE 는 고전압을 견딜 것 (p.2 · 인용 없음) | `zhu2015` (이 글의 ref 8 자신) | 층① 산화 한계 LLZO 2.91 · LISICON 3.39 · LLTO 3.71 · LiPON 2.63 · **LATP 4.21 · LAGP 4.27 V** | 🔵 / 🔴 일부 — NASICON 인산염에만 맞다 |
| ③ | 산화물 세라믹은 Li 에 안정 (p.3) | `zhu2015` | 환원 한계 LLZO 0.05 V (부동태 쉬움) · LiPON 0.68 · LATP 2.17 · LAGP 2.70 V (환원) | 🔵 — LLZO 에만 맞다 |
| ④ | Li 금속 + 황화물 → 계면상 · 고전도 SEI 면 장기 OK · MCI 면 급속 열화 (p.3 · refs 13–14) | `zhu2015` · `wang2022_resistive_decomposing_interfaces_se_alkali_metal` (2022) · `chaney2024_two_step_sei_growth_argyrodite_li_metal` (2024) · `li2026_mci_vs_sei_na3ps4_na_mlip_md` (2026) · 우리 li2s · cascade 묶음 2 카드 | 부동태 조건 = 전자절연 Li 이원 산물 · Ge · Ti 계 = MCI · 분해 이원상 / 알칼리 금속 계면 20 개 접합일 + 계면별 MTP MD · SEI 성장의 2 단계 · SEI↔MCI 를 MLIP-MD 로 가르는 세 표지 · 우리 li2s 는 '계면상이 bulk Li₂S 보다 빠른가' 를 **답 못 하고 닫힘** · 묶음 2 카드: 금속성 소수상 득 / 독 (MCI 대 MII) 정량 문턱 없음 | ✅ 프레임은 표준이 됐다 · ⚪ '고전도 SEI' 의 정량 기준은 litdb 안에서도 미정 |
| ⑤ | 양극 계면 불안정 · 코팅이 장기 안정 · 고전압 · 그러나 계면상 안정성은 과제 (p.3 · refs 4 · 15 · 16) | `kato2016` (2016) · `zhu2016` · `zuo2022` (2023 · Janek) · `qi2025_high_voltage_limits_halide_sulfide_assb` (2025) | 2016 고출력 셀 전부 LiNbO₃ 코팅 · 양극 ≈ 2.5–4.25 V vs Li · Cl-rich 아지로다이트 × 코팅 언급 없는 NCM85: 정전압 홀드에서는 Cl-rich 우위 · 갈바노 사이클 · DEMS 셀에서는 우위가 사라지거나 뒤집힘 · Li₆PS₅Cl · NCM85 · 4.5 V 할라이드 / 황화물 계면 | ✅ 코팅은 기본이 됐다 · ✅ '계면상 안정성은 과제' 도 맞았다 (조건 의존) |
| ⑥ | SE/양극 정류 접촉 · Li 고갈층 (공간전하) · 코팅으로 회피 (p.3 · 인용 없음) | `haruyama2014` (2014 · 이 글보다 앞 · 인용 안 됨) · `minnmann2021` | LCO(110) 능선 O 에 Li 흡착 → LPS 쪽 Li 공공 형성 에너지 하락 (고갈 이전에 '빨려간다') · LiNbO₃ 버퍼가 흡착 자리 제거 · 복합 양극 τ 식은 공간전하를 무시한다고 저자가 명시 | ⚪ 정류 거동을 잰 자료 없음 · 🔵 계산 근거는 2014 에 이미 있었다 |
| ⑦ | 기계적 강성으로 덴드라이트를 막는다는 기대는 틀렸다 · 결정질 SE 입계로 침투 (p.2–3) | `doux2020` (2020) · `liang2026` (2026 리뷰 · 2 차) | 거의 완벽히 조밀한 단결정 산화물 SE (LLZO) 에서도 수 사이클에 침투 · 단락 (doux2020 서론) · Han 2019: *"high electronic conductivity, rather than mechanical properties, is the root cause of internal dendrite formation"* (2 차) | ✅ + 🔵 원인이 기계에서 전자 쪽으로 (2 차 · 원문 미보유) |
| ⑧ | Li 음극: 방전 중 공극 · 기계 압력이 필요하고 정량 연구가 필요 (p.3–4) | `doux2020` · `tron2023_lpscl_ccd_ambient_pressure` (2023) · `deysher2022_transport_mechanical_aspects_assb_review` (2 차) · `cronau2021_stack_pressure_ionic_conductivity` (2021) | 낮은 적층압 (≈ 5 MPa) 에서 Li 금속 1000 h+ · ≥ 25 MPa 는 Li 가 SE 공극으로 creep → 단락 (기계적 현상) · < 5 MPa 에서 stripping 공극 증가 (tron2023 의 ref 31) · Kasemchainan 2019 임계 stripping 0.2 mA cm⁻² (3 MPa) / 1.0 (7 MPa) (2 차) · σ 측정값 자체가 적층압에 의존 | ✅ 정량 연구가 실제로 나왔다 · 🔵 압력 창은 양쪽에 벽이 있다 (너무 낮으면 접촉 · 공극 · 너무 높으면 creep 단락) |
| ⑨ | 복합 전극: 독립 전자망 · 이온 / 전자 percolation · 공극 · 균열 · 접촉 손실 (p.3) | `bielefeld2019` · `bielefeld2020` · `minnmann2021` · `trevisanello2021` (Janek 그룹) · `deysher2022` (2 차) | 3D 미세구조 percolation · σ_eff · 저-CAM 전자 / 고-CAM 이온 병목 · 고-CAM 이면 탄소 무첨가 · 다결정 NCM 균열 vs 단결정 · Koerver: 370 MPa 재가압으로 잃은 용량 회복 (2 차) | ✅ 같은 그룹의 연구 축이 됐다 · 🔵 '독립 전자망 필수' 는 CAM 함량 의존 |
| ⑩ | 고체 전지는 *"revolutionary change of production technology"* 가 필요 (p.3) | `hippauf2019` · `schmitt2026` (BELLA) · `frankenberg2024_dem_high_intensity_mixer_assb` · `luan2025_graded_cathode_400whkg_pouch` | PTFE 0.1 wt% 건식 막 · 건식 시트 vs 펠릿 (시트가 첫 방전 · 율속 우위 · 계면 분해는 더 큼) · 고강도 믹서 DEM · 건식 graded 전극 | 🔵 건식 공정이 실제 경로가 됐다 (진행 중) |
| ⑪ | 안전: 손상 시 H₂S · 산화 시 SO₂ (p.3 · ref 17) | `zuo2022` · 우리 CEI · cascade 축 ② | DEMS 로 SO₂ (m/z 64) 실측 · Cl-rich ≈ 5.7 배 (a.u.) · 우리 CEI 산물 목록에 SO₂ · cascade 축 ② 는 도펀트를 못 가름 (G4 불통과) | ✅ SO₂ 생성 확인 · ⚪ 위험도 정량은 없음 |
| ⑫ | SE 는 농도 분극이 없어 고전류 · 고출력 (ref 4 · p.2–4) | `kato2016` · `kato2018_thick_electrode_assb_cycle_tortuosity` (2018) | Li 이온 셀만 확산 한계 (≈ 22 mA cm⁻²) · **t ∼ 1 은 가정 (측정 없음)** · 600 µm · 15.7 mAh cm⁻² · t₊ ≈ 1 → 농도 구배 없음 → 옴 한계 반응대 모형 | 🔵 셀 수준 정황은 쌓였다 · t₊ = 1 은 여전히 가정 |
| ⑬ | 에너지 큰 이득은 Li 금속뿐 · 두꺼운 Li 음극은 어려울 것 · 삽입형 음극 + 동역학으로 갈 것 (p.2 · 4) | `luan2025` (2025) · `doux2020` · `kato2018` | 5 Ah 파우치 **404 Wh kg⁻¹ — 순수 Si 음극** · 분모는 stack 수준 (파우치 필름 · 탭 제외) · Li 금속 음극 1000 h+ · 풀셀 > 200 사이클 (≈ 5 MPa) · 후막 삽입형 셀 | 🔵 / ⚪ — 이 글의 '흑연 vs Li 금속' 이분법이 **합금 (Si) 음극** 을 빠뜨렸다 · 두꺼운 Li 음극 실용화는 litdb 로 판정 불가 · ⚠ 404 를 18650 (캔 포함) 266 과 같은 줄에 놓지 않는다 |
| ⑭ | LIB 에너지 밀도 곧 한계 (`Fig. 1a` 띠 ≈ 800–866 Wh l⁻¹) | — | litdb 에 그 뒤 18650 자료 없음 | ⚪ |
| ⑮ | 고분자: 상온 부족 · EV > 80 °C (p.1) | — | 직접 대조 digest 없음 | ⚪ |
| ⑯ | 황화물 상온 σ > 액체 · '고체는 나쁜 전도체' 는 오해 (p.1) | `kamaya2011` · 이 글 `Fig. 1b` 자체 | Kamaya 그림: 상온은 '비슷' · −10 °C 아래에서만 LGPS 가 분명히 위 · 이 그림: EC:DEC 가 두 황화물 위 | 🔵 '오해' 는 맞고 '액체보다 높다' 는 과장 — '비슷하다' 가 정확 |
| ⑰ | (지도에 없던 것) 아지로다이트 | `kraft2017` (2017) · `banik2022` · `zuo2022` · `wang2026` | 같은 저자들의 이후 주력 계열 (Li₆PS₅X 격자 분극성 · 산화 안정 · Cl-rich 양극 계면 · 계면 열역학 + 동역학) | — (이 글 이후의 이동) |

---

## 12. 우리 원장 매핑 (요약표)

| 이 글의 항목 | 우리 원장 위치 | 상태 |
|---|---|---|
| 층① 창 (환원 · 산화) | `litdb/our_dft_baseline.md` ESW 행 · `kb/concepts/se_redox_frontier.md` 4 장 ④ | 값 있음 (층①) — 이 글과 숫자로 맞대지 않는다 (이 글에 숫자 없음) |
| 2.5–4.25 V 작동창 | CLAUDE.md 데이터 규율 (사용자 2026-11-09) | 규칙 |
| SO₂ (CEI 산물) | `db/properties/cei_product_gap_card_2026_10_27.json` (`D-2026-10-27-cei-product-gaps` + 개정 1) | 산물 목록 · 값 미인용 |
| H₂S (가수분해) | `db/properties/cascade_axis_hyd_readout_2026_11_04.json` · `cascade_axes_bundle_closed_2026_11_05.json` | G4 불통과 → 위험 표시만 |
| SEI 대 MCI | `db/properties/lpscl_smallcell_glass_track_closed_2026_10_30.json` (li2s 닫힘) · `lpscl_glass_dense_protocol_ensemble_estimand_2026_11_10.json` (li2s-3 · 진행) · `cascade_axes_bundle2_estimand_2026_11_10.json` 축 ⑥ | 미답 · 값 0 |
| 분해 부피 · 공극 | `cascade_axes_bundle2_estimand_2026_11_10.json` 축 ⑤ (`D-2026-11-10-cascade-axes-bundle2` + 개정 1 active) | 값 0 (결과 전) |
| 작동창 도펀트 행방 | 같은 카드 축 ④ | 값 0 |
| 복합 전극 percolation · 압밀 | `litdb/comparison_vs_ours_DEM.md` · `our_dem_baseline.md` (자리표시) | 값 없음 |
| 기계 (C 축) | `our_dft_baseline.md` (상대 진술: B₀ ↓ · E_VRH ↑) | 상대 진술만 |

---

## 13. 적용 인사이트 ★

① **우리 트랙 넷을 한 그림으로 설명할 때 `Fig. 3` 이 지도가 된다.** 왼쪽 위 (Li | SEI | SE 저항) = li2s · 왼쪽 아래 (덴드라이트) = Li 금속 쪽 cascade 축 ③ · ⑥ · 오른쪽 (코팅 양극 · 전위 강하) = CEI · b2o3 · 축 ④ · 파란 화살표 (압력) = DEM 압밀. 발표 서론에서 "2016 년 분야가 꼽은 과제 → 우리가 그중 어디를 재는가" 순서로 쓸 수 있다 (그림을 쓸 땐 원전 표기 · 색 규약 단서 §10-⑨).

② **'산화물 / 인산염은 고전압을 견딘다' 를 우리 원고에서 쓰지 않는다.** 쓸 일이 있으면 층① 표 (`zhu2015`) 로 '어떤 인산염이 · 몇 V 까지' 를 적고, 우리 O 단독 대조의 '인산염 응축' (Li₃PO₄ → Li₄P₂O₇ → LiPO₃ → P₂O₅ · O 는 −2) 으로 'P–O 골격이 버틴다' 는 뜻임을 밝힌다. b2o3 · CEI 원고 같이 읽기 때 이 일반화가 나오면 짚을 자리다 (b2o3 · CEI 원고는 사용자가 1저자가 아니다 — 고치지 않고 짚기만).

③ **'SEI 대 MCI' 를 규칙으로 쓰지 않은 우리 카드의 판단이 옳았다는 문헌 쪽 근거는 아직 없다 — 반대도 없다.** 이 글 (2016) 의 단정은 정량 문턱이 없는 프레임이다. cascade 묶음 2 가 φ_met 을 '기록만' 으로 둔 것은 이 글과 다른 선택이고, 그 차이를 원고에 적을 때는 "the 2016 view that mixed-conducting interphases lead to fast deterioration" 를 프레임으로만 인용한다.

④ **`Fig. 1b` 같은 '문헌 곡선 모음' 그림은 인용 전에 원전과 대조한다** — 이 그림의 LGPS 선이 원전 (Kamaya) 과 −0.27 ~ +0.11 dex 다르고, Li₇P₃S₁₁ 선은 litdb 2 차 인용값과도 다르다. 우리 발표의 '전도도 지도' 를 만들 때 이런 2 차 그림을 베끼지 말고 원전 값을 쓴다 (`liang2026` digest 의 교훈과 같다 — 리뷰가 다시 그린 그림 대신 원전 `qian2025` 를 인용했다).

---

## 14. 인용 가능 문장 (영문 초안 — 과제 틀로만 · 숫자 없이)

- "As early as 2016, the development of solid-state batteries was framed around five challenges—energy density, power density, long-term stability, safety, and cost (*Nat. Energy*, 1, 16141 (2016))."
- "Most solid electrolytes are reduced at low potentials and oxidized at intermediate potentials, so protective interphases are required to stabilize the electrolyte/electrode contacts (*Nat. Energy*, 1, 16141 (2016); thermodynamic origin: *ACS Appl. Mater. Interfaces*, 7, 23685 (2015))."
- "Whether the interphase formed against lithium metal is a well-conducting solid electrolyte interphase or a mixed-conducting interphase was identified as decisive for long-term operation (*Nat. Energy*, 1, 16141 (2016))." — 프레임만 · 우리 li2s 결과와 잇지 않는다 (마감 금지 서술).
- "Solid composite electrodes must provide both electronic and ionic percolation, and their mechanical integrity under volume changes requires stack pressure (*Nat. Energy*, 1, 16141 (2016))." — DEM 서론.
- ⛔ 쓰지 않는 문장: "Sulfide solid electrolytes conduct better than liquid electrolytes at room temperature" (이 글 `Fig. 1b` 와도 어긋난다) · "Oxide and phosphate solid electrolytes withstand high voltages" (일반화 · §10-⑥) · 이 글의 +70 % · +40 % · 3,700 · 260 / 270 Wh kg⁻¹ · `Fig. 1b` 선 값.
- 표기는 랩 표준 (*저널 약칭*, 권, 첫 쪽 (연도)) — 이 글의 '첫 쪽' 자리는 article number 16141.

---

## 15. 주의 / 한계 (인용 규율)

1. **2 차 인용 전용** — 이 글의 숫자는 원전이 아니다. 원고 · 발표에 숫자를 쓸 때는 원전 (refs) 으로 간다 · litdb 에 원전 digest 가 있는 것은 refs 4 · 5 · 8 · 11 · 15 다섯뿐.
2. **물성 4축 (A–D) 표에 넣지 않는다** — 값이 없는 전망이다 (`comparison_vs_ours.md` 에는 리뷰 판정 블록 §J-75 로만).
3. `Fig. 1b` 판독값 (figure-read ≈) 은 **다시 그린 선**의 값 — 원전 값으로 인용 금지 · 기울기 Ea 는 원전 Ea 가 아니다.
4. `Fig. 2` 의 에너지 밀도 변화는 저자 어림 · 재현 불가 — 'Li 금속 +70 %' 를 인용할 때는 그 사실을 같이 적는다.
5. 참고문헌 오기 (ref 11 'Zhou') · ref 18 ≠ litdb `sakuda2013` — 옮겨 쓸 때 고친다.
6. 이 글과 우리 트랙의 연결은 **질문의 대응**이다 — cascade 묶음 2 (값 0) · li2s (닫힘 · 미답) · li2s-3 (진행 · 결과 0) 의 '결과' 처럼 쓰지 않는다.
7. 판정 표 (§11) 의 '뒤 문헌' 은 **litdb 에 있는 것만**이다 — litdb 밖의 2016 이후 문헌 (이 글을 인용한 수많은 논문) 은 보지 않았다. ⚪ 는 '틀렸다' 가 아니라 'litdb 로는 모른다' 다.

---

## 16. 참고문헌 29 대조표 (원문 순서)

| # | 서지 (원문 그대로 · 축약) | 이 글에서 받치는 서술 | litdb digest |
|---|---|---|---|
| 1 | Goodenough & Park, *J. Am. Chem. Soc.* 135, 1167 (2013) | LIB 는 효율적 저장 장치로 증명 | — |
| 2 | Adelhelm & Janek, *Handbuch Lithium-Ionen-Batterien* Ch. 16 (Springer, 2013) | LIB 에너지 밀도 곧 한계 · 한계값은 셀 설계 · 공정에 의존 (`Fig. 1a`) | — |
| 3 | Robinson & Janek, *MRS Bull.* 39, 1046 (2014) | SSB 는 고에너지 + 고출력 가능 | — |
| 4 | Kato *et al.*, *Nat. Energy* 1, 16030 (2016) | 고출력 · 고전류 · 고온 · 코팅 → 고전압 · 고에너지 | ✅ `kato2016_high_power_assb_lsipscl_superionic` |
| 5 | Kamaya *et al.*, *Nat. Mater.* 10, 682 (2011) | σ 가 액체에 닿을 수 있다 · LGPS 상온 σ · `Fig. 1b` LGPS 선 | ✅ `kamaya2011_lgps_lithium_superionic_conductor` |
| 6 | Stephan & Nahm, *Polymer* 47, 5952 (2006) | 고분자 율속 제한 · 빠른 충전 불가 | — |
| 7 | Minami, Hayashi & Tatsumisago, *Solid State Ionics* 177, 2715 (2006) | Li₇P₃S₁₁ 상온 σ (본문) | — |
| 8 | Zhu, He & Mo, *ACS Appl. Mater. Interface(s)* 7, 23685 (2015) | 낮은 열역학 안정성 · Li 금속에 불안정 | ✅ `zhu2015_esw_grand_potential_origin` |
| 9 | Luntz, Voss & Reuter, *J. Phys. Chem. Lett.* 6, 4599 (2015) | 보호 계면상이 전해질 / 전극 접촉을 안정화 | — |
| 10 | Troy *et al.*, *Appl. Energy* 169, 757 (2016) | kWh 당 비용은 제조 기술에 의존 | — |
| 11 | **'Zhou'** (= Zhu), He & Mo, *J. Mater. Chem. A* 4, 3253 (2016) | 대부분 Li SE 는 Li 금속에 열역학적으로 불안정 | ✅ `zhu2016_first_principles_interface_stability_assb` (저자명 오기) |
| 12 | Li, Ma, Chi, Liang & Dudney, *Adv. Energy Mater.* 5, 1401408 (2015) | 박막 전지 Li ≈ 1 µm 순환 | — |
| 13 | Wenzel *et al.*, *Solid State Ionics* 286, 24 (2016) | 최고 SE 도 좁은 열역학 안정 범위 | — |
| 14 | Wenzel *et al.*, *Chem. Mater.* 28, 2400 (2016) | 같음 (저자 Wenzel … Zeier · Janek — `cronau2021` 참고문헌 목록에서 확인) | — |
| 15 | Richards, Miara, Wang, Kim & Ceder, *Chem. Mater.* 28, 266 (2016) | 양극 쪽 계면 불안정 | ✅ `richards2016_interface_stability_pseudobinary` |
| 16 | Oh, Hirayama, Kwon, Suzuki & Kanno, *Chem. Mater.* 28, 2634 (2016) | 코팅 → 장기 안정 · 고전압 · 고에너지 | — |
| 17 | Muramatsu, Hayashi, Ohtomo, Hama & Tatsumisago, *Solid State Ionics* 182, 116 (2011) | H₂S · SO₂ 위험 | — |
| 18 | Sakuda, Hayashi, Takigawa, Higashi & Tatsumisago, *J. Ceram. Soc. Jpn.* 121, 946 (2013) | 산화물은 기계적으로 soft 아님 | ⚠ litdb `sakuda2013_sulfide_mechanical_property` 는 **다른 논문** (*Sci. Rep.* 3, 2261) |
| 19 | Broussely & Archdale, *J. Power Sources* 136, 386 (2004) | `Fig. 1a` 2012 까지 자료 + 2004 뒤 외삽 | — |
| 20 | Panasonic NCR18650B specifications (2012) · 웹 | `Fig. 1a` 2012 확인값 | — |
| 21 | 웹 링크 (go.nature.com) | `Fig. 1a` 2016 값 | — |
| 22 | Edman, Ferry & Doeff, *J. Mater. Res.* 15, 1950 (2000) | `Fig. 1b` P(EO)₁₂-LiTFSI 선 | — |
| 23 | Kanno & Murayama, *J. Electrochem. Soc.* 148, A742 (2001) | `Fig. 1b` Li₃.₂₅Ge₀.₂₅P₀.₇₅S₄ 선 | — |
| 24 | Seino, Ota, Takada, Hayashi & Tatsumisago, *Energy Environ. Sci.* 7, 627 (2014) | `Fig. 1b` Li₇P₃S₁₁ 유리세라믹 선 | — (값은 `nosrati2026` 리뷰에 2 차로만) |
| 25 | Stallworth *et al.*, *J. Power Sources* 81–82, 739 (1999) | `Fig. 1b` EC:DEC · EC:PC LiPF₆ 선 | — |
| 26 | Yu *et al.*, *J. Electrochem. Soc.* 144, 524 (1997) | `Fig. 1b` LiPON 선 | — |
| 27 | Bruce & West, *J. Solid State Chem.* 44, 354 (1982) | `Fig. 1b` Li₃.₅Zn₀.₂₅GeO₄ 선 | — |
| 28 | Buschmann *et al.*, *Phys. Chem. Chem. Phys.* 13, 19378 (2011) | `Fig. 1b` LLZO 선 | — |
| 29 | Francisco, Stoldt & M'Peko, *Chem. Mater.* 26, 4741 (2014) | `Fig. 1b` LAGP 선 | — |

---

## 17. 기법 용어 미니사전

- **Comment (Nature 계열)** — 연구 논문이 아니라 짧은 의견 · 전망 글. 자체 자료 · Methods 가 없고 인용 문헌으로 논지를 세운다. litdb 에서는 리뷰와 같이 '2 차 인용 전용' 으로 다룬다.
- **w_vol · w_grav** — 셀 부피 · 질량당 에너지 (Wh l⁻¹ · Wh kg⁻¹). 셀 질량 · 부피를 무엇까지 넣느냐 (캔 · 파우치 · 탭) 에 따라 같은 셀도 값이 달라진다 (`luan2025` 의 stack 수준 404 vs 18650 의 캔 포함 266).
- **LI-SSB · LiM-SSB** — 이 글의 이름: 흑연 같은 삽입형 음극을 그대로 둔 고체 전지 · Li 금속 음극 고체 전지.
- **층① · 층②** (우리 명명) — 층① = 열역학 분해 개시 (grand potential) · 층② = 골격을 유지한 채 Li 만 빠지는 산화환원 (`schwietert2020`). 겉보기 창 (CV) 은 둘 다 아닌 셀 · 동역학 지표.
- **SEI · MCI** — 고체 전해질 계면상 (전자 절연 · 이온 전도 → 스스로 멈춤) · 혼합 전도 계면상 (전자도 흘러 분해가 계속 진행). Janek 그룹의 in-situ XPS 연구가 고체 전해질에 쓴 구분 (`zhu2015` 가 그 연구를 자기 ref 15 로 들어 'Janek in-situ XPS 의 MCI' 와 정합한다고 적었다 · 이 글의 ref 14 (Wenzel … Zeier · Janek 2016) 도 같은 그룹).
- **정류 접촉 · 공간전하층 (space charge layer)** — 계면 양쪽의 Li 화학 퍼텐셜 차 때문에 SE 쪽 Li⁺ 가 빠진 얇은 층이 생겨 한 방향 전류가 막히는 (다이오드 같은) 거동의 가설. 코팅 (LiNbO₃ 등) 이 완충한다고 본다.
- **percolation (스며듦 연결)** — 복합 전극 안에서 이온 · 전자 경로가 끝에서 끝까지 이어진 연결망이 생기는 조건. 성분 부피 분율 문턱 근처에서 전도가 급변한다.
- **쌍극 적층 (bipolar stacking)** — 한 집전체의 양면에 양극 · 음극을 붙여 셀을 직렬로 바로 쌓는 구조. 액체 전지는 셀 사이 전해질이 이어져 단락되므로 못 한다.
- **VTF (Vogel–Tammann–Fulcher)** — 고분자 · 유리 전해질의 σ 가 Arrhenius 직선이 아니라 휘는 꼴 (σ ∝ exp[−B/(T−T₀)]). `Fig. 1b` 고분자 선의 휨 0.30 dex 가 그 모양.
- **dex** — 상용로그 한 자리 (log₁₀ 단위). 0.3 dex ≈ 2 배.

---

## 18. 판독 기록 (재현)

**크롭** — `python3 tools/litdb/extract_figures.py --slug janek2016_solid_future_battery_development --pdf "litdb/inbox/128._A_solid_future_for_battery_development.pdf" --clean` → 그림 3 장 (`fig_1.png` 2239×843 · `fig_2.png` 1492×466 · `fig_3.png` 1460×634 · 300 dpi) · 번호 공백 · 놓친 캡션 후보 **0** (`missing_labels` 빈 목록) · 표 0.
- 실제로 본 것: **3/3** — `Fig. 1` (패널 a · b · 두 축 · 10 라벨 다 들어옴) · `Fig. 2` (세 셀 · 화살표 · 수치 라벨) · `Fig. 3` (세 삽입도 · 화살표 · φ) + `Fig. 3` 오른쪽 삽입도 600 dpi 확대 (scratch 렌더 · 저장 안 함). 재크롭 0 · 손 크롭 0 · 오탐 0.
- ⚠ 이 도구는 돌 때마다 `litdb/figures/_sources.json` 을 그 체크아웃의 figures.json 들로 통째로 다시 쓴다 — 이번에도 그랬다 (sparse 체크아웃이라 1 편만 남음). HEAD 판으로 되돌리고 이 논문 항목 하나만 더했다 (473 → **474**).

**벡터 판독** — `python3 tools/litdb/janek2016_readout.py` (기본 `--pdf litdb/inbox/128._…pdf` · `--kamaya_csv litdb/figures/kamaya2011_lgps_lithium_superionic_conductor/digitized.csv`) → `digitized.csv` 224 행.
- `--selftest`: 합성 PDF (실제 CFG 의 띠 · 범위) 로 양성 12 · 음성 8 (연도 눈금 하나 빠짐 · w_vol 눈금 3 pt 어긋남 · 사각 표지 3 개 · 한계 띠 없음 · 위 K 축 2 pt 어긋남 · 선 하나 없음 · 라벨 글자색 ≠ 선 색 · 같은 색 두 선의 라벨이 남의 선에 더 가까움) · kamaya CSV 3 (없음 → None · 같은 1000/T 차 · 형식 바뀜 → 멈춤) · CSV 0 과 없음 구분 1 · 산수 3 — **전부 통과**.
- **일부러 깨기 5/5 빨간불** (CLAUDE.md 코드 규율): ① 보정 잔차 문턱 무시 → 'w_vol 눈금 3 pt 어긋남' 이 멈추지 않음 ❌ ② 선 밖 외삽 → 'B 는 띠에 안 닿는다' ❌ ③ `_fmt` 를 `"—" if not v` 로 → 0.0 이 '—' 로 둔갑 ❌ ④ 라벨–선 거리 부호 뒤집기 → 양성 경로가 '짝이 뒤바뀐다' 로 멈춤 ❌ ⑤ 점선 판정 항상 False → 곡선 후보 2 개로 멈춤 ❌.
- 도구가 **못 하는 것** (docstring): `Fig. 2` · `Fig. 3` (모식도) · 그라데이션 띠의 '한계선' 정의 · 원전 값 복원 (다시 그린 선이다) · 베지어 곡선.
- ⚠ 이 sparse 체크아웃에는 `kamaya2011` 그림 폴더가 없어 HEAD 의 같은 파일 (`git show HEAD:…/digitized.csv`) 을 scratch 로 꺼내 `--kamaya_csv` 로 줬다 — 내용은 저장소 판과 같다. 전체 체크아웃에서는 기본 경로로 같은 결과가 나온다 (파일이 없으면 CSV 에 '대조 건너뜀' 행을 남기고 멈추지 않는다).

**텍스트** — `pdftotext` (raw · layout) 로 본문 4 쪽 전문 대조 · 본문 인용문은 전부 그 텍스트에서 옮겼다.
