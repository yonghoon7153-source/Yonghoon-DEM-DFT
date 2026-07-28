# Electron-conductive binder for silicon negative electrode enabling low-pressure all-solid-state batteries — Jun & Jeong et al. (Nat. Commun. 2026)

> slug `jun2026_ppma_econductive_binder_si_lowpressure_assb` · DOI `10.1038/s41467-025-66851-0` · type `exp (계산 0)` · PDF `82ea256b/7c0de1f1-PPMA_low_P_si_anode_ASSB.pdf` · digested `2026-07-15` · status ✅
> **저자**: Seunggoo Jun¹·⁴ / Minseok Jeong¹·⁴ (**공동 1저자**), Boyeong Jang, Seong-hyeon Jung, Young Joon Park, Yong Bae Song, Jisoo Park, Seungyun Jo, Du Yeol Ryu, Hanvin Kim², Sungkyung Kim², Jaewoo Lee², **Jeonghun Kim**¹·³†, **Yoon Seok Jung**¹·³† — ¹Yonsei 화공생명, ²**SK On**, ³Yonsei 배터리공학과. Nature Communications (2026) 17:156 (Received 2025-04-18 / Accepted 2025-11-18 / Published 2025-12-05, open access CC BY-NC-ND).
> ⚠ **[외부]** — **[Son](five-volt ASSB, Nat. Energy 2025)과 같은 Yonsei 정윤석(Yoon Seok Jung) 그룹** (우리 한양대 J-W. Lee 라인 아님).

---

## 0. 이 digest를 읽는 법 (+왜 argyrodite litdb에 있나)
이 논문은 argyrodite 물성 논문이 **아니다** — SE는 상용 LPSCl(Li₆PS₅Cl, POSCO JK, σ 4.2 mS/cm@30 °C)을 as-received로 쓸 뿐이고, 주제는 **ASSB Si 음극용 폴리머 바인더**다. 보관 이유는 두 가지:
1. **우리 SDCP(자가도핑 PEDOT-계 전도성 바인더, `kb/projects/sdcp_master_v2_2026_07_11.md`) 프로그램의 최근접 문헌 좌표** — "PEDOT 전도 기전은 유지하고, 폴리음이온 쪽을 개조해 제2기능(접착)을 넣는다"는 설계 논리가 우리와 정확히 평행(단 그들은 음극/습식/2상 유지, 우리는 양극/건식/1상 자가도핑).
2. **서론 내러티브 스켈레톤 템플릿** (§3) — 동료 제안: 우리 SDCP 논문 서론을 이 구조로 미러링.

⚠⚠ **명명 함정**: 이 논문의 **PPMA ≠ poly(propyl methacrylate)·PMMA(아크릴)가 아니다**. **PPMA = PEDOT:P(SSₓ-co-MA_y) = poly(3,4-ethylenedioxythiophene):poly((styrene sulfonic acid)ₓ-co-(maleic acid)_y)** — 즉 **PEDOT:PSS의 폴리음이온(PSS)에 maleic acid(MA)를 공중합해 넣은 PEDOT:PSS-계 전도성 고분자**다. PMA = poly(maleic acid).

## 1. 한 줄 요약
SE-배제 monolithic Si 음극이 실용 저압(5 MPa)에서 죽는 원인이 **탈리튬화 시 e⁻ 연결망 붕괴**임을 ex situ 3전극 e⁻ 전도도 측정으로 짚고, **PEDOT:PSS의 전도 구조(π-π stacking·분자배열)는 그대로 유지하면서 PSS에 maleic acid를 공중합(PPMA)해 접착력만 추가**한 F-free·수계 전도성 바인더로 카본 없이 이를 해결 — (Li-In)|LPSCl|Si 반쪽셀 50cyc 유지율 45→80%(vs PVDF), 풀셀 5 MPa 0.5C 105 vs 76 mAh/g, prelithiation 병용 시 134 mAh/g·0.5C·100cyc 86%, **233 mAh Si||NCM83 파우치(226 Wh/kg·792 Wh/L)** 까지 스케일 실증.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 시스템 | Si(1–5 µm 미크론, 카본 無) 음극 · LPSCl(Li₆PS₅Cl) SE · NCM70(LiNi₀.₇₀Co₀.₁₅Mn₀.₁₅O₂)/NCM83(LiNi₀.₈₃Co₀.₁₂Mn₀.₀₅O₂) 양극 · 30 °C · **5 MPa** |
| 비교 바인더 | **PVDF**(절연 기준) vs **PP**(PEDOT:PSS) vs **PPMA51/21/11**(PSS:MA 몰비 5:1/2:1/1:1) + 대조군 PAA·PP/PMA 물리혼합·PVDF+C65 |
| 질문 | 저압(수 MPa)에서 monolithic Si 전극이 열화하는 미시 원인은? 바인더로 해결 가능한가? |
| 갭 | SE-배제 Si 전극의 깃발 결과(Si/PVDF 99.9:0.1, 500cyc 80%)는 **50 MPa 고압** 전제 — 실용 압력에선 급락, 저압 특화 바인더 부재 |
| 선행(자기그룹) | ref 33 (Jun, Small 2024): Ag interlayer + prelithiation으로 저압 Si — 이번 논문은 같은 1저자의 **바인더 축** 후속 |
| 산업 연계 | SK On 공저(파우치·시트전극) + 750 g 스케일 합성 — 실용화 지향 |

## 3. ★서론 내러티브 구조 — 문단별 스켈레톤 (사용자·동료 특별 요청)
> 서론 = **정확히 4문단**. 각 문단의 *기능*(수사적 역할)을 분해하면 아래와 같다. 동료 제안 = 우리 SDCP 논문 서론을 이 뼈대로 미러링.

| 문단 | 기능 (한 줄) | 논리 사슬 (세부) |
|---|---|---|
| **P1** | **소재의 약속 + 구체제(LE)에서의 실패 물리** | Si 이론용량 3580 mAh/g(Li₁₅Si₄)·풍부함 → LIB 에너지밀도의 실용 레버 [refs 1–3] → 그러나 >300% 부피변화 → 전기 접촉손실 + 신선 표면의 연속 전해질 분해 → 급속 fading [2,4,5] → 나노구조화·전해질 엔지니어링에도 [4,6–11] **LE 고유 한계(전해질 고갈) 잔존** [12–14]. *역할: 문제를 소재가 아니라 "전해질 시스템의 한계"로 밀어 ASSB 전환의 명분 구축.* |
| **P2** | **신플랫폼(ASSB) 궤적 + 이 논문이 딛는 전극 개념 + 깃발 결과(숨은 조건 포함)** | LE→황화물 SE 대체, Si-ASSB는 LIB 궤적을 따라 발전 [15,16] → SE 혼합 3D 복합 Si 전극(cold-press, Li₆₋ₓPS₅₋ₓCl₁₊ₓ·LiBH₄-LiI) [17–21] → 복합 전극의 한계: 부피변화 시 입자간 접촉 열화 + SE 전기화학 안정성 한계 [22–27] → **SE-배제(monolithic) Si 전극** 개념: 리튬화 시 기계적 소결 → SE층과 최소 2D 접촉, 부반응 최소 [28–31] → 깃발 결과: Si/PVDF **99.9:0.1**, 500cyc 80% — **단 50 MPa** [29]. *역할: 개선 대상 개념을 특정하고, 깃발 결과 안에 비현실 조건(고압)을 심어 P3의 갭을 예비.* |
| **P3** | **실용 조건에서의 갭 → 열화모드 3개 열거 → 요구사양(스펙) 도출 + 환경 제약** | 실용 압력(수 MPa)에서 성능 급락 [32–34] → 열화모드 **①** SE 분리층에서 박리(delamination) — 자기 그룹의 Ag interlayer 선행 해법 인용 [33] **②** lithiated Si의 연성에도 수직 균열 = 기계 열화 [34] → 고급 바인더 필요 [35–38] **③** 미크론 Si 자체 e⁻ 전도 부족 → 카본 첨가 필요 → 바인더 증량 → 이온/전자 접촉 훼손 + 에너지밀도 하락 [33] → **요구사양 문장**: "advanced binders … specifically those with **e⁻-conductive and mechanically fortified binding properties**" → 부가 제약: **F-계 폴리머 규제(PVDF 포함)** [39–41] + **NMP 유해성** [42] → F-free·수계 요구. *역할: 문제를 번호 붙인 열화모드로 분해한 뒤 해법의 필요조건(요구사양 시트)으로 변환 — 해법의 필연성 확보.* |
| **P4** | **Herein: 설계 + 기능배분 문장 + 반직관 안정성 주장 + 정량 기전 증거 + 헤드라인 성능** | PPMA 제안 → 조성 노브(PSS:PMA 비) → **기능배분 문장**("PEDOT:PSS provides the e⁻-conducting pathways, while PMA enhances the binding ability") → **반직관 주장**(LE에서 불안정하다던 PEDOT:PSS가 ASSB 고체-고체 계면에선 안정) → F-free·수계 → 기전 정량(전극 e⁻ 전도도 **36,000×**: 5.5×10⁻⁹→2.0×10⁻⁴ S/cm) → 탈리튬화 시 e⁻ 전도 저하 완화(vs PVDF) → PMA 비율 효과 예고 → 헤드라인: 풀셀 **179/134 mAh/g(0.05C/0.5C)·200cyc 72%·30 °C·5 MPa** + **233 mAh 파우치**. *역할: 설계원리 → 기전 → 검증 → 스케일 순으로 몰아침.* |

**스켈레톤 요약 공식**: `[P1 소재 약속+실패물리(구체제)] → [P2 신플랫폼 궤적+채택 개념+깃발결과(숨은 조건)] → [P3 실용조건 갭+열화모드 열거→요구사양+제약] → [P4 Herein: 설계+기능배분 1문장+반직관 주장+정량 기전+헤드라인]`
- 세부 기술: (a) P2 깃발 결과에 **일부러 비현실 조건(50 MPa)을 같이 적어** P3 갭의 씨앗으로 씀. (b) P3의 열화모드 열거는 **First/Second/Finally** 신호어로 구조화. (c) 자기 그룹 선행(ref 33)을 P3 모드①의 해법으로 심어 "우리는 이 문제의 연속 연구자"임을 표시. (d) P4의 기능배분 문장은 **성분→기능 1:1 대응**의 한 문장 — 논문 전체의 논증 지도 역할.

## 4. 폴리머 정체 + 포지셔닝 (원문 인용) ★
**정체**: PPMA = **PEDOT:P(SSₓ-co-MA_y)**. 합성 3단계 — ① NaSS(styrene sulfonic acid sodium salt) + MA(maleic acid) 자유라디칼 공중합 → P(SSₓ-co-MA_y) (몰비 1:0/5:1/2:1/1:1) ② HCl 처리로 Na→H(산성화) ③ 그 위에 EDOT 산화중합(Fe₂(SO₄)₃ + NaPS) → PEDOT:P(SSₓ-co-MA_y). PP(=PEDOT:PSS)도 동일 공정. **즉 PEDOT:PSS의 2상(전도성 PEDOT + 폴리음이온 템플릿) 구조를 그대로 두고, 폴리음이온 사슬에 -COOH(MA)를 공중합으로 심은 것.**

**포지셔닝 원문 (p.2, Herein 문단)**:
> "Herein, we demonstrate e⁻-conductive binders with reinforced mechanical properties tailored for Si negative electrodes in ASSBs. These binders are conductive polymers, poly(3,4-ethylenedioxythiophene):poly((styrene sulfonic acid)x-co-(maleic acid)y) (PEDOT:P(SSx-co-MAy)) (PPMA). By controlling the ratio of PSS and PMA in the copolymers, we achieve both good electrical conductivity and binding property. **In these polymers, PEDOT:PSS (PP) provides the e⁻-conducting pathways, while PMA enhances the binding ability.** Notably, although PEDOT:PSS has been regarded as electrochemically unstable in the negative electrode potential range within LE systems, **it demonstrates electrochemical and structural stability when applied to Si electrodes in ASSBs, owing to the solid-solid interfacial nature.**"

**"전도 기전 유지" 판정 원문 (GIWAXS 결론, p.3–4)**:
> "Thus, we concluded that **PPMAs have the same characteristics in terms of the molecular arrangement and π-π stacking of PEDOT as well-known PP.**"

**Abstract 포지셔닝**:
> "…an electrically conductive binder—PEDOT:P(SSx-co-MAy)—that is **scalable, fluorine-free, and water-processable**. This binder offers **sufficient e⁻-conductivity to eliminate carbon additives**, while ensuring strong adhesion and **electrochemical stability in contrast to conventional liquid electrolyte systems**."

**유지 vs 개선 분해** (동료 질문의 직접 답):
| | 무엇 | 근거 |
|---|---|---|
| **유지(kept)** | PEDOT:PSS의 e⁻ 전도 구조 — lamellar stacking 2종(Type I/II)·PSS amorphous halo·**PEDOT π-π stacking(3.55 Å)**, benzoid-우세 backbone | GIWAXS 4피크 동일(Fig 2c,d) + Raman benzoid(사이클 후도 유지, Supp 10) + CV 후 S 2p 골격 불변(Fig 2g) |
| **개선(added)** ① | **접착력**: MA의 -COOH ↔ Si 표면 실라놀(-Si-OH) 상호작용 → peel force PP ~1 → PPMA11 **2.2 N/cm** (PVDF <0.1) | 180° peel(Supp 23)·R_int 증가 억제(Fig 4c,d)·균열 억제(Fig 4e) |
| **개선(unlock)** ② | **음극 전위 전기화학 안정성** — 폴리머를 바꿔 얻은 게 아니라 **환경(고체-고체 계면)이 열어준 것**: LE에선 <1.0 V 비가역 환원·bulk Li⁺ 도핑·접착 상실, SE에선 계면 국한 반응·5th cycle 후 안정화·골격 보존 | CV LE vs SE(Supp 6–15)·OCV 모니터링(Supp 11)·TOFSIMS Li⁺ 미침투(Supp 12)·peel 유지(Supp 13) |
| **대가(cost)** | e⁻ 전도도 하락: 필름 10.6(PP)→**5.8 S/cm**(PPMA11)·sheet resistance 15→110 kΩ/sq — 그러나 "**sufficient**"(Si 10⁻⁶ S/cm 대비 여전히 ≫) | Fig 2f·4-point probe(Supp 24)·"this level of e⁻ conductivity is sufficient" (p.7) |

→ **동료 코멘트 검증: 정확하다.** "PEDOT:PSS의 전도 기전은 지키고(구조 증거까지 제시), 성능(접착·저압 내구)을 개선"이 이 논문의 서사 그 자체. 단 "안정성 개선"의 절반은 분자 개조가 아니라 **ASSB 환경 효과**임에 주의(§16).

## 5. 핵심 수치 총정리
| 물성 | 값 | 조건/출처 |
|---|---|---|
| 바인더 필름 σ_e | PP **10.6** → PPMA51/21 (중간) → PPMA11 **5.8 S/cm** | 4-point probe, **무용매(DMSO/EG 無)** — 용매 첨가 문헌치 450 S/cm 대비 의도적 저스펙 (refs 52,53) |
| 바인더-SE 복합 σ_e | ~10⁻³–10⁻² S/cm(그림 판독); **전극 내 바인더 자체 σ_e 추정 10⁻¹–10⁻² S/cm** | "Binder-SE (ASSB)" 구성, Fig 2f; CV 후 ~1자릿수 감소 |
| Si 전극 σ_e (pristine) | Si/PVDF **5.5×10⁻⁹** vs Si/PPMA **2.0×10⁻⁴ S/cm** = **36,000×** | ex situ 3전극(Ni mesh), 5 MPa; Si 분말 자체 ≈10⁻⁶ |
| σ_e (lithiation 중) | 둘 다 >2.0×10⁻³ S/cm 로 상승(monolith 형성; PPMA 소폭 우위) | Fig 3e 좌 |
| σ_e (delithiation 중) | PVDF **2.0×10⁻³→4.3×10⁻⁵ 급락** vs PPMA **유지(말미 소폭 감소)** | Fig 3e 우 — **논문의 기전 헤드라인** |
| 유효 Li⁺ 전도 σ_Li(on-eff) | Si/PPMA11 7.4 vs Si/PVDF 25.5 mS/cm ("comparable" 주장, 3.4× 차) | (Li-In)\|SE\|Si\|SE\|(Li-In) 대칭셀, lithiated (Supp 18) |
| 접착(180° peel) | PVDF **<0.1** / PP ~1 / PPMA51 1.5 / **PPMA11 2.2 N/cm** | Cu 집전체 위 Si 전극 (Supp 23) |
| Sheet resistance | PPMA11 1420(5 wt%)→**110 kΩ/sq**(10 wt%); PP 15 kΩ/sq | 4-point probe (Supp 24); 110도 "sufficient" |
| 반쪽셀 초기용량 | PPMA **2380** vs PVDF **2010 mAh/g** | (Li-In)\|LPSCl\|Si, 0.2C(1C=3500 mA/g), 30 °C, 5 MPa, 카본 無, Si:binder 90:10 vs 97:3 |
| 반쪽셀 유지율 | **80 vs 45%** @50cyc | 같은 조건 (Fig 3b) |
| PVDF 압력 의존 | 0.2C 용량 2490(70 MPa)→1820 mAh/g(5 MPa) | Supp 1 — 문제 정의 수치 |
| R_int @50cyc | PP 29.6 / PPMA51 34.4 / PPMA21 **19.6** / PPMA11 **17.5 Ω** | EIS 피팅 (Fig 4c,d); R_bulk는 4종 비슷 |
| 풀셀(NCM70, 5 MPa) 0.05C | PPMA11 158(ICE 72%) ≈ PVDF 157 mAh/g(73%) | np 1.6·Si 63% 활용·2.00–4.29 V |
| 풀셀 0.5C 1st | PPMA11 **105** vs PVDF **76 mAh/g** | Fig 5b,d |
| 풀셀 0.5C @**70 MPa** | PPMA11 131 vs PVDF **142 mAh/g** (**역전**) | Fig 5d — 고압에선 PVDF 우위 |
| Prelithiation(4.0 µm Li≈23% SOC) | 반쪽셀 ICE 66→79% / 풀셀 ICE 73→**83%**·157→**179 mAh/g**·100cyc 72→**86%**·**200cyc 72%**(0.5C 134 mAh/g) | 열증착 Li, ⁷Li MAS-NMR로 자발 합금화 확인 (Fig 5e,f) |
| 파우치(Si\|LPSCl\|NCM83, 7×10 cm²) | 충/방 297/**233 mAh**(256/201 mAh/g_NCM83)·ICE 78.3%·평균 3.43 V·**226 Wh/kg·792 Wh/L**(집전체 포함, stack 141 µm, 49.3 mg/cm²) | 0.05C 형성 후 0.2C 사이클(~140cyc 표시, 유지율 % 본문 미기재), 30 °C·5 MPa; warm isostatic press 450 MPa·80 °C |
| SE | LPSCl(POSCO JK) σ **4.2 mS/cm @30 °C** (Ti\|SE\|Ti AC) | =우리 comp1 조성 상용분말 anchor |
| 층두께(파우치 단면) | Al 15 / NCM83 62 / SE막 38 / Si 8 / Cu 18 µm | Fig 5h |
| GIWAXS 피크 | q=0.31(d 20.27 Å, lamellar I)/0.62(10.13, II)/1.26(4.99, PSS halo)/**1.77 Å⁻¹(3.55 Å, PEDOT π-π)** — PP·PPMA **공통** | PAL 9A, λ=1.240 Å (Fig 2c,d) |
| XPS S 2p₃/₂ | PSS 168 / PEDOT 164 eV — CV 후 marginal 변화(골격 보존) | Fig 2g |
| 기계(나노인덴테이션) | 경도·영률 "PVDF·PAA와 comparable" (수치 SI만) | Supp 22 |

## 6. 재료 & 방법
- **합성**: §4 참조. 스케일: 1-L 이중자켓 반응기에서 **750 g** 생산(Fig 1c) + 1 L 용액 대량화(Supp 4). PSS 상세 — NaSS 30.000 g(0.145 mol)/DI 260 mL, N₂ 3 h 탈기, NaPS 650 mg 개시, 80 °C 20 h, HCl로 산성화, THF 침전·60 °C 진공건조. PEDOT화 — 폴리음이온 160 g/600 mL, **폴리음이온:EDOT = 2.5:1 질량비**, Fe₂(SO₄)₃ 0.078 g + NaPS 1.532 g, 중합 후 이온교환수지 + 초음파 분산.
- **전극**: Si(1–5 µm 99.9%) + PP/PPMA를 **탈이온수 슬러리**로 Cu 18 µm 위 캐스팅(80 °C 진공건조), 1.2–1.3 mg/cm², 카본 無. Si/PVDF는 NMP 공정(대조군). 양극: pellet형 NCM:LPSCl:C65 70:30:3; **sheet형(SK On)** NCM70 75.0:22.0:1.5:1.5 / NCM83 80:18:1:1(benzyl acetate 용매, Al 15 µm); LPSCl 막 97:3(p-xylene+butyl butyrate).
- **셀**: LPSCl 150 mg→~700 µm 펠릿(70 MPa) / WE 부착 / CE Li₀.₅In-LPSCl 200 mg(270 µm) / 전체 370 MPa 압착 / **작동은 목표 압력(5 또는 70 MPa)을 load cell(BONGSHIN)로 실측 유지**. 13 mm PEEK 몰드·Ti 집전. LE 대조: 2032 코인, 1 M LiPF₆ EC:DMC 1:1.
- **ex situ e⁻ 전도도(자체 고안, refs 56,57)**: 3전극 — Si 전극과 SE층 사이 **Ni mesh** 삽입; 채널1 = 정상 충방전(350 mAh/g 단위 + 2 h rest 반복), 채널2 = 집전체-Ni mesh 간 DC(0.1/0.01 V, 30 min) → **충방전 깊이별 전극 e⁻ 전도도 곡선**(Fig 3c–e).
- **OEP(operando electrochemical pressiometry)**: 가압 셀 내 0.1 kg 분해능 압력센서, Δ(ΔP)/Q_discharge 지표(ref 33 방법).
- **분광/구조**: GIWAXS(PAL 9A)·¹H-NMR(D₂O)·⁷Li MAS-NMR(400 MHz, 밀폐 캡슐)·FTIR(KBr)·Raman(532 nm, 1 mW)·TOFSIMS(30 keV Bi⁺, airtight shuttle)·XPS(Al Kα, 500 eV 120 s 에칭)·GPC(Pullulan 표준)·AFM(상분리 검사)·180° peel(0.5 mm/s, 2 kg 롤러)·cryo 단면 밀링(−50 °C)·SEM/EDXS.
- **prelithiation**: 열증착 Li 4.0 µm(≈23% SOC) on Si 전극 → 자발 합금화(⁷Li MAS-NMR).
- **파우치**: NCM83 시트(16.5 mg/cm², 7×10 cm²) + LPSCl 막 전사 + Si 전극 적층 → Al-laminate 진공 밀봉 → **warm isostatic pressing 450 MPa·80 °C·5 min**.

## 7. 결과 — 섹션별 상세

### 7.1 문제 정의: 저압에서 PVDF-Si가 죽는다 (Supp 1, Fig 1a)
Si/PVDF 97:3 반쪽셀, 70→5 MPa 감압 시 0.2C 용량 2490→1820 mAh/g — 입자간 접촉손실로 인한 e⁻ 저항 증가로 귀속. Fig 1a 도식: 리튬화 = 팽창·병합(monolith), 탈리튬화 = 수축 → 저압이면 균열/공동 → **절연 바인더는 여기서 e⁻ 경로가 끊기고, 전도성 바인더는 다리를 유지**한다는 가설 제시(이후 절에서 검증).

### 7.2 합성·스케일 (Fig 1b,c)
3단계 합성(§4)·750 g 배치. F-free·수계·무용매(전도도 향상용 DMSO/EG 미사용 — ASSB 적합성 때문이라 명시).

### 7.3 공중합체 확인 (Fig 2a,b + Supp 3)
¹H-NMR: 6.1–7.8 ppm para-치환 벤젠(PSS), 2.3–2.9 ppm -COOH(MA) — 몰비 4종 정량(Supplementary Table 1). FTIR: 1170(-SO₃ asym)/1118·1000(-SO₃ sym) 모두 보존 + **1710 cm⁻¹ C=O**(MA)만 추가. GPC 분자량(SI).

### 7.4 GIWAXS — "전도 구조 보존"의 구조 증거 (Fig 2c,d)
PP·PPMA51/21/11 필름 4종 모두 동일 4피크(§5 표): lamellar stacking 2형 + PSS amorphous halo + **PEDOT π-π 3.55 Å**. → "PPMAs have the same characteristics … as well-known PP" — **"기전 유지" 주장의 구조적 근거**. (Cu 위 캐스팅 후 AFM에서도 상분리 없음, Supp 5.)

### 7.5 전기화학 안정성: LE vs SE의 체계 대조 (Fig 2e,g + Supp 6–15) — **"환경이 안정성을 만든다"**
- PEDOT:PSS는 LE계에서 2.5–4.0 V(vs Li/Li⁺)만 안정, 음극 전위에선 불안정으로 알려짐(ref 49) → 0.01–1.00 V 창에서 LE/SE 양쪽 체계 비교.
- **LE**: <1.0 V 비가역 환원(LE 반응+SEI)·사이클마다 지속·**OCV 모니터링상 폴리머 bulk로 Li⁺ 도핑**·TOFSIMS Li 침투·**peel 접착 급락**.
- **SE**: 전류 낮음·**5th cycle 후 안정화·가역 산화환원**·bulk Li⁺ 도핑 없음(계면 국한)·TOFSIMS Li 미침투·peel 유지.
- 첫 사이클 음극 피크는 PMA↑일수록 커짐 = **-COOH의 H⁺→Li⁺ 치환**(Li 1s XPS, refs 54,55), 1 V 복귀 시 산화전류 없음 = 비가역. 그러나 CV 후 **S 2p(PSS 168/PEDOT 164 eV) marginal 변화** = 골격 보존; Raman benzoid 유지; σ_e 감소 ~1자릿수.
→ 결론: **관능기(-COOH→-COOLi)는 소모성 반응을 하지만 전도 골격은 산다. 그리고 그 생존은 고체-고체 계면(반응 국한·Li⁺ 접근 제한) 덕분.**

### 7.6 e⁻ 전도도 2-영역 정량 (Fig 2f)
"Film (LIB)"(필름 4-point) vs "Binder-SE (ASSB)"(절연 SE 매트릭스에 바인더 혼합) 2단 플롯, pristine(빈 기호) vs after-CV(채운 기호). 필름 10.6→5.8 S/cm(PMA↑) / 복합 ~10⁻³–10⁻²; CV 후 양쪽 다 ~1자릿수 감소 → **전극 내 바인더 σ_e 10⁻¹–10⁻² S/cm 추정** — Si(10⁻⁶)의 배선재로 충분하다는 "sufficiency" 논증.

### 7.7 PPMA vs PVDF + ex situ e⁻ 전도도 (Fig 3) — **기전 헤드라인**
- 초기 전압곡선(Fig 3a): PVDF는 리튬화 개시 직후 0 V 아래로 꺼지는 급락(large overpotential, 절연) — PPMA는 매끈. 초기 탈리튬화 2380 vs 2010 mAh/g, 50cyc 80 vs 45%(Fig 3b).
- **Fig 3e (백미)**: pristine 5.5×10⁻⁹(PVDF) vs 2.0×10⁻⁴(PPMA, **36,000×**) → 리튬화 중 둘 다 >2×10⁻³(Li_x Si 자체가 도체, monolith) → **탈리튬화에서 갈림**: PVDF 2.0×10⁻³→4.3×10⁻⁵ 급락 vs PPMA 유지.
- 해석: 수축→공동/균열(단면 SEM, Supp 21)로 접촉이 끊길 때 PPMA가 e⁻ 다리 유지. 탈리튬화 후 PVDF는 SE·집전체 양쪽 계면에서 박리, PPMA는 무박리.
- 보조: PPMA는 슬러리 용매에 **불용·분산형**이라 conformal 코팅이 아니라 **입자간 간극(interstitial voids)에 위치** → 입자 직접 접촉·monolith 형성·Li⁺ 경로 보존(σ_Li(on-eff) 7.4 vs 25.5 mS/cm "comparable" 주장).

### 7.8 PMA 분율 효과 + 대조군 3종 (Fig 4 + Supp 22–32) — **바인더 비교 설계의 핵심**
- 12전극 매트릭스(4 바인더 × 5/10/15 wt%): 최적 10 wt%; PPMA11 최고 2380 mAh/g.
- 100cyc(Fig 4b): PPMA11·21 > PP·PPMA51 — **sheet resistance 110 kΩ/sq(PPMA11) ≫ 15(PP)인데 성능은 PPMA11 우위** → "이 수준 e⁻ 전도면 충분, 그 너머는 접착이 결정" (전도-접착 트레이드오프의 sufficiency 논증).
- EIS: R_bulk 4종 유사·소변화 / **R_int**가 분화(§5 표) — -COOH↔실라놀 접착이 부피변화 응력을 견뎌 계면 유지. SEM(Fig 4e): PP·PPMA51 균열 뚜렷, PPMA21·11 억제.
- **대조군 설계 (우리 벤치마크 설계에 참고)**: ① **Si/PAA** — 같은 -COOH를 가진 절연 바인더: PPMA11이 우위 → "접착만으론 부족, e⁻ 전도 병행 필요" (Supp 28) ② **PP/PMA 물리 블렌드** — copolymer 대비 성능 급락 + SEM/EDXS 상분리 → "**나노스케일 균일 분포는 공중합으로만**" (Supp 31) ③ **Si/PVDF/C65 90:5:5** — 카본 첨가로도 PVDF 구제 불가(far inferior) (Supp 32).

### 7.9 풀셀 Si||NCM70 + 압력·prelithiation (Fig 5a–g)
- 설계: NCM 11.0/Si 1.2 mg/cm², **np 1.6 = Si 용량의 63%만 사용**(수명 마진; 반쪽셀 63% SOC ICE 69% vs NCM 반쪽셀 82% → 풀셀 방전 종지는 Si가 결정).
- 0.05C: 158≈157 (저율속에선 차이 없음 — 정직 보고) / **0.5C: 105 vs 76** / rate(Fig 5c): ≥0.5C에서 PPMA11 우위, 2C까지.
- **압력 반전(Fig 5d)**: 70 MPa에선 131 vs 142로 PVDF 우세 — PPMA 이점은 **저압 전용**. 장기 과전압 거동도 "외부 압력이 지배, 바인더 고유 불안정 아님"(70 vs 5 MPa 비교, Supp 33/36).
- OEP(Supp 37): PPMA11이 압력 응답 일관 + 베이스라인 안정 = **가역적 electrochemo-mechanical 거동·SOC 균질화** ([Kang] 리뷰 어휘와 동일 프레임).
- prelithiation 시너지: §5 표 수치. **PreLi-Si/PPMA11@5 MPa ≈ Si/PVDF@70 MPa** — "고압을 바인더+PreLi로 대체" 프레임(Fig 5f).
- **Fig 5g**: x축을 **C-rate/작동압(C MPa⁻¹)** 로 정규화한 벤치마크 산점도 — 저압 성능 비교의 영리한 지표(This work 별표 2개).

### 7.10 파우치 Si||NCM83 (Fig 5h–l)
NCM83 16.5 mg/cm²·7×10 cm²·warm isostatic press. §5 표 수치(233 mAh·226 Wh/kg·792 Wh/L). 자평: C-Ag interlayer 무음극 파우치(ref 67, 삼성 계열)와 "nearly on par"; 기존 pouch형 Si-ASSB 대비 얇은 SE막·**무 prelithiation**으로 용량·수명 우위(Fig 5l, Supp Table 6). ⚠ 0.2C 유지율 %는 본문 미기재(~140cyc 곡선만).

## 8. 메커니즘 종합
1. **왜 죽나**: 저압 + 탈리튬화 수축 → 공동/균열 → **e⁻ 연결망 붕괴**(PVDF: 2.0×10⁻³→4.3×10⁻⁵ S/cm) → 활물질 고립 → 용량 급락. (Li⁺ 경로가 아니라 e⁻ 경로가 1차 병목 — σ_Li는 두 바인더 "comparable".)
2. **왜 사나**: PPMA = 간극 위치 전도성 다리(끊긴 접촉 위 e⁻ 우회로) + -COOH↔실라놀 접착(균열 자체 억제·계면 유지·R_int 억제) — **전도(살아있는 경로)와 접착(경로가 덜 끊김)의 이중 작용**.
3. **왜 안정한가**: ASSB 고체-고체 계면이 반응을 계면에 국한(LE처럼 bulk Li⁺ 도핑·용매 공격 없음) → PEDOT:PSS계의 음극 전위 사용이라는 통념 밖 공간이 열림. -COOH→-COOLi 1회성 소모는 있으나 골격 보존.
4. **조성 최적**: PMA↑ = 전도↓·접착↑ → PPMA11(1:1)이 "충분 전도 + 최대 접착"의 스윗스팟(10 wt%).

## 9. 전체 논증 흐름
Supp1(저압서 PVDF 급락) → Fig1(가설 도식+합성) → Fig2(공중합 확인→**GIWAXS 전도구조 보존**→LE/SE 안정성 대조→σ_e 2-영역) → Fig3(반쪽셀 우위 + **ex situ σ_e로 기전 확정**) → Fig4(PMA 분율 = 접착 레버; 대조군 3종으로 전도·접착·공중합 각각의 필요성 분리) → Fig5(풀셀 저압 우위→압력 반전으로 "저압 전용" 정직화→PreLi 시너지→**파우치 스케일 실증**) → Discussion(친환경·무카본·설계원리 일반화).

## 10. DFT/계산 방법 ★
**없음 — 계산 0** (DFT·MD·결합에너지·시뮬레이션 일절 없음; Methods에 계산 섹션 자체가 없음). 모든 기전 주장은 ex situ/operando 실험(3전극 σ_e·XPS·TOFSIMS·OCV·Raman·GIWAXS·OEP)으로 지탱.
- **무질서 처리 / k-points / functional 등**: n/a.
- → **우리 기회**: "왜 -COOH가 실라놀에 붙나(결합에너지)", "왜 π-π/polaron 전도가 폴리음이온 개조에도 사는가(스핀/전자구조)", "바인더 fragment 수준 비교(우리 PTFE C₄H₂F₈/C₁₀F₂₂ 벤치마크 설계)"는 이 논문 계열에 **전무한 계산 공백** — 우리 SDCP DFT가 채우는 자리.

## 11. Figure set ★
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1a | PVDF vs 전도성 바인더 리튬화/탈리튬화 도식(균열·e⁻ 다리) | 가설 도식을 논문 맨 앞에 — 우리 SDCP 도식(폴라론 경로+앵커링)도 Fig1a 슬롯에 |
| 1b,c | 합성 스킴 + 750 g 반응기 사진 | "scalable" 주장은 사진 1장으로 — 실용성 어필 기법 |
| 2a,b | ¹H-NMR·FTIR 조성 시리즈(1:0→1:1) | 조성 노브의 스펙트럼 지문 — 우리 v7c IR/Raman 배정표와 같은 역할 |
| 2c,d | **GIWAXS 2D + out-of-plane 프로파일 4종 동일** | **"기전 유지"의 구조 증거 프레임** — 우리는 Loewdin 스핀/폴라론 분포가 이 슬롯의 계산판 |
| 2e | CV 0.01–1.00 V(첫 사이클 -COOH→Li⁺ 비가역) | 관능기 소모 vs 골격 보존 분리 논증 |
| 2f | **σ_e 2-영역(Film-LIB vs Binder-SE-ASSB) pristine/after-CV** | 바인더 전도도 벤치마크 플롯 포맷 — SDCP vs PTFE vs PEDOT:PSS 비교 그림에 차용 가치 큼 |
| 2g | ex situ S 2p XPS before/after CV 4종 | 골격 보존 판정 = S 2p 불변 — 우리 XPS anchor 사고방식과 동일 |
| 3a,b | 반쪽셀 곡선(PVDF 초기 급락 화살표)+사이클 | 절연 바인더의 signature(개시 과전압)를 곡선에서 읽는 법 |
| 3c–e | **ex situ 3전극 σ_e vs 용량 (lithiation/delithiation)** | **논문 기전 헤드라인** — "언제 e⁻ 망이 끊기나"의 직접 정량; 방법 자체(Ni mesh 3전극)도 차용 후보 |
| 4a–e | PMA 분율 시리즈: 사이클·EIS(R_bulk/R_int 분해)·SEM | 조성-기능 매핑 + R_int만 갈리는 패턴 = 접착 효과의 임피던스 지문 |
| 5a–d | 풀셀 + **70 vs 5 MPa 막대(역전 포함)** | 정직한 조건 의존성 공개 — 주장 범위 한정 기법 |
| 5e,f | prelithiation 전후 곡선·수명 | 보조 기술 시너지 배치법(바인더 주장을 흐리지 않게 별도 절) |
| 5g | **용량 vs C-rate/압력(C MPa⁻¹) 정규화 벤치마크 산점도** | 자기 조건에 유리한 정규화 지표 발명 — 우리도 "성능 per 압력/per 바인더함량" 지표 고려 |
| 5h–l | 파우치: 적층 도식+단면 SEM+사진+곡선+사이클+파우치 벤치마크 | 스케일 실증 세트 구성(도식→단면→사진→데이터→좌표) |

## 12. Post-processing ★ (실험 정량화 방식 — 우리 도구 대응)
- **ex situ σ_e(3전극+Ni mesh)**: 충방전 깊이(350 mAh/g 간격)별 DC 저항 → σ_e-용량 곡선. 기록 = S/cm vs mAh/g. *우리 대응: 계산으로는 percolation/전도 경로 모델 없음 — 개념만.*
- **4-point probe**: 필름 σ_e·전극 sheet resistance(kΩ/sq). 바인더 wt% 시리즈.
- **EIS 등가회로**: R_bulk(고주파 절편)/R_int(반원) 분해, 1st vs 50th. 기록 = Ω 막대.
- **180° peel**: N/cm (첫 최대 직후~30 mm 평균). 접착 정량 표준.
- **XPS(500 eV 에칭)·TOFSIMS(airtight)·Raman·GIWAXS(d=2π/q)**: 골격 보존·Li 침투·상구조. *우리 ORCA ΔSCF XPS·IR/Raman 배정과 관측량 겹침.*
- **OEP**: Δ(ΔP)/Q_discharge — 전극 부피변화 가역성의 압력 지문.
- **⁷Li MAS-NMR**: prelithiation 합금화 상 확인(밀폐 캡슐).

## 13. 우리 대비 ★ — (1) SDCP 프로그램 (주 비교축) / (2) argyrodite baseline 접점
### 13.1 vs 우리 SDCP (자가도핑 전도성 바인더, `kb/projects/sdcp_master_v2_2026_07_11.md`)
| 항목 | Jun 2026 (PPMA) | 우리 (SDCP v7c) | 판정 |
|---|---|---|---|
| 설계 논리 | PEDOT 전도 유지 + **폴리음이온(PSS)에 MA 공중합**으로 접착 추가 — 2상(PEDOT:polyanion) 유지 | PEDOT-계 전도 유지 + **술폰산을 티오펜 side chain에 공유 결합(자가도핑)** — **별도 PSS 상 제거**, 1상 | **같은 설계 철학의 두 구현**: 그들은 "폴리음이온을 개조", 우리는 "폴리음이온을 백본에 흡수". 우리가 한 단계 더 급진적(절연상 자체 제거) |
| "전도 유지" 증거 | GIWAXS π-π 3.55 Å·lamellar 동일 + Raman benzoid + S 2p 불변 (**구조 증거, 실험**) | Loewdin 스핀: 백본 폴라론 지분 n=1 35% → n=2 33%(두 링 균등 분할) → n=3 50.1%(mid-doped; interior site 선호 71 meV; H-제거 비용 n↑에 따라 감소) (**전자구조 증거, 계산**) | **상보적** — 그들은 "구조가 같으니 전도도 같다"(간접), 우리는 "폴라론이 백본에 실재"(직접, 단 계산). 우리 논문에서 이 대비 자체가 셀링 포인트 |
| 전도-기능 트레이드오프 | 전도 희생(10.6→5.8 S/cm·sheet R 15→110 kΩ/sq)하고 접착 취득 → "**sufficient**" 논증으로 방어 | PSS 절연상 제거로 **전도 손실 없이**(오히려 상 순도↑ 기대) 앵커링 취득이 우리 피치 — 단 polaron 지분 35–50%는 완전 편재 아님 | 그들의 sufficiency 논증 프레임("이 수준이면 충분, 그 너머는 제2기능이 결정")은 우리 폴라론 지분 수치 방어에 그대로 재사용 가능 |
| 표면 앵커링 화학 | **-COOH ↔ Si-OH(실라놀)** 수소결합/상호작용 + 첫 사이클 H⁺→Li⁺ 치환(-COOLi, 비가역·소모성) | **-SO₃⁻/-SO₃H ↔ NCM 표면**: E_bind(doped) **−1.52 eV**(QE Phase-B preview, neutral 대기; UMA 클린슬랩 챔피언 −5.196 eV, S–O 1.51 Å 공유 앵커) + **H↔Li 교환 에너지학**(operando SO₃Li 논거, master §3.9) | **직접 평행**: "산성 관능기가 표면과 결합 + 작동 중 H→Li 교환" — 그들의 Li 1s XPS 증거(-COOLi)는 우리 SO₃Li operando 논거의 실험 전례로 인용 가능 |
| 공중합 vs 블렌드 | **PP/PMA 물리 블렌드 대조군 → 상분리·성능 급락** = "나노스케일 통합은 공유결합(공중합)으로만" (Supp 31) | 자가도핑 = 도판트를 아예 **같은 분자에** — 블렌드(PEDOT+PSS 2상)의 극한 반대편 | **우리 서사의 실험 근거로 최상급**: "물리 혼합 < 공중합(그들) < 자가도핑(우리)"의 사다리 논증 구성 가능 |
| 적용 전극 | **음극(Si)**, 0.01–1.0 V vs Li/Li⁺ | **양극(NCM)**, 고전압 산화 측 | 다름 — 그들의 저전위 안정성 논거(고체계면 국한)는 우리 산화 측에 자동 이전 불가 |
| 공정 | **수계 슬러리**(습식), F-free | **건식(dry-process)**, PTFE 병용(SBE vs DBE) — PTFE는 F-계(그들이 배격하는 대상) | 다름 — 단 "F-free" 환경 프레임(PFAS 규제 refs 39–41)은 우리도 PTFE 저감 서사로 활용 가능 |
| 안정성 논거 | **환경 기반**: ASSB 고체-고체 계면이 분해를 계면 국한 (분자 개조 아님) | **분자 기반**: 자가도핑 상태의 안정성(분광 판정 완료)·폴라론 화학 | 다름 — 슬롯(반직관 안정성 주장)은 미러링하되 내용은 독립 정당화 필요 |
| 계산 | **0** | ORCA r2SCAN-3c(v7c opt+freq·IR/Raman 대조)·UMA·QE DFT+U Phase-B·PTFE fragment 벤치마크(C₄H₂F₈ 문헌 fragment + C₁₀F₂₂ parity fragment, gabia 대기) | **우리 차별화 공간** — 이 계열 최고 저널 논문도 기전을 전부 실험으로만 지탱 → 계산 기전 규명의 신규성 유효 |

### 13.2 vs argyrodite baseline (`../our_dft_baseline.md`) — 접점만 (이 논문은 SE 물성 미탐구)
| 항목 | 이 논문 | 우리 | 비고 |
|---|---|---|---|
| LPSCl σ | **4.2 mS/cm @30 °C** (상용 POSCO JK, Ti\|SE\|Ti AC) | comp1 AIMD RT 외삽 ~3.35 mS/cm (동일 조성) | ✓ 같은 10⁻³ 차수 — comp1 조성 상용분말의 외부 anchor 1건 (문헌 2.9~4.9 범위 내) |
| SE = 절연 매트릭스 가정 | "electronically insulating SEs"를 바인더 σ_e 측정 매트릭스로 사용 | comp1/modelc PBE gap 2.066/2.099 eV = **wide-gap 절연체** 프레임 | ✓ 정성 일치 (절대 gap 비교 금지 규율 유지) |
| SE 환원 안정성 @Si 전위 | **미논의** — 0.01–1.0 V에서 SE셀 CV 전류를 바인더 거동으로만 해석 | grand-potential 환원한계 **1.242 V** → 0.01–1.0 V에선 LPSCl 자체도 열역학적 환원 영역 (자기제한 SEI로 kinetic 안정화가 통설) | ⚠ **우리 관점의 비판점**: SE셀 CV 전류·"5th cycle 후 안정화"에는 바인더 반응 + **SE 환원(SEI 형성)** 이 섞여 있을 가능성 — 논문은 분리 안 함 (우리 추론, 논문 주장 아님) |
| 산화 onset/기계/전자구조 | n/a (음극 논문·SE 미분석) | axis ①–④·elastic·gap | 비교 불가 — comparison 4축 표에 수치로 넣지 않음 |

## 14. 적용 인사이트 (우리 SDCP 논문에 어떻게)
1. **서론 미러링 (동료 제안 판정: 적합, 부분 개작)** — §3 스켈레톤은 우리 스토리에 잘 맞는다: P1 dry-process ASSB 양극의 약속 + PTFE 3약점(전자절연·분산불량·약접착) / P2 전도성 바인더 궤적 + **이 논문(Jun 2026)을 깃발 결과로 인용**(숨은 조건 = 음극·습식·2상 PEDOT:PSS 유지) / P3 건식 양극 조건에서의 요구사양 열거(e⁻ 전도 + NCM 화학 앵커링 + 무용매/건식 호환 + 절연 PSS 상 문제) / P4 Herein: SDCP + 기능배분 문장 + 반직관 주장("PSS 상을 제거해도 폴라론 전도가 산다" — Loewdin n-시리즈) + E_bind 정량 + PTFE 벤치마크. **주의 2가지**: (a) 우리는 셀 헤드라인이 없으므로 P4의 마지막 슬롯은 계산 결과(폴라론 보존+앵커링+벤치마크)로 채워야 함, (b) 그들의 반직관 주장은 환경 기반이므로 문장 구조만 빌리고 근거는 우리 분광/스핀 증거로 독립 구성.
2. **기능배분 1문장 템플릿**: "In these polymers, X provides the e⁻-conducting pathways, while Y enhances Z." → 우리판: "the conjugated thiophene backbone provides the polaron-conducting pathways, while the covalently tethered sulfonate self-dopes the backbone and chemically anchors the binder to the NCM surface."
3. **사다리 논증**: 물리 블렌드(상분리, 그들 Supp 31) < 공중합 폴리음이온(PPMA) < **자가도핑(측쇄 공유결합, 우리)** — "기능 통합의 공유결합 수준을 한 단계 더 올림"으로 신규성 위치 지정. PEDOT:PSS의 잔여 문제(절연 PSS 과잉상·상분리 가능성·수계 공정)를 P3 갭으로 사용.
4. **sufficiency 논증 재사용**: 그들이 전도 희생(10.6→5.8)을 "충분" 프레임으로 방어했듯, 우리 폴라론 지분(35–50%)도 "전도에 충분한 백본 비편재 + 나머지는 앵커링에 쓰이는 산소-중심 라디칼"로 positive 프레임.
5. **-COOLi 전례**: 그들의 -COOH→-COOLi(Li 1s XPS) = 우리 H↔Li 교환(operando SO₃Li) 논거의 게재 전례 — 인용해 "산성기→Li염 전환은 전도성 바인더에서 관찰된 바 있다"로 방어.
6. **figure 차용**: Fig 2f(2-영역 바인더 전도 벤치마크)·Fig 3e(상태별 성질 추적)·Fig 5g(조건 정규화 산점도) 포맷 + 바인더 비교표(§5 스타일: 물성 | PVDF | PP | PPMA 열) → 우리 PTFE/PEDOT:PSS/SDCP 비교표 포맷.
7. **계산 공백 = 우리 자리**: NC급 바인더 논문도 결합에너지·전자구조 계산이 0 — 우리 fragment 벤치마크(C₄H₂F₈/C₁₀F₂₂)와 폴라론 해부는 이 문헌 계열에 없는 층위.

## 15. 인용 가능 문장 (deck/paper용)
- "Jun et al. retained the PEDOT:PSS conduction motif (identical GIWAXS π-π stacking) while copolymerizing maleic acid into the polyanion for adhesion; our SDCP takes the next step of covalently tethering the sulfonate dopant to the thiophene backbone itself, removing the insulating PSS phase altogether."
- "Their blend-control experiment (phase-segregated PP/PMA mixture underperforming the copolymer) experimentally supports the design ladder physical blend < copolymerized polyanion < self-doped single chain."
- "Ex situ three-electrode measurements identified delithiation-stage electron-network collapse (2.0×10⁻³ → 4.3×10⁻⁵ S cm⁻¹ for PVDF) as the low-pressure failure mode; an e⁻-conductive binder maintains the network — evidence that binder electronic conductivity, not Li⁺ transport, is the first bottleneck at 5 MPa."
- "The carboxyl protons irreversibly exchange to Li⁺ (-COOLi) in the first cycle while the conjugated backbone survives (invariant S 2p) — a published precedent for our operando SO₃H→SO₃Li exchange argument."

## 16. 주의/한계 (over-claim 방지, critical)
- **조성 교란**: 36,000×·반쪽셀 비교는 Si:binder **90:10(PPMA) vs 97:3(PVDF)** — 바인더 정체와 함량이 동시에 변함(각자 최적화 조성이라는 방어는 있으나 순수 재료 비교 아님).
- **저압 전용 이점**: 70 MPa에선 PVDF 142 > PPMA11 131 mAh/g로 **역전** — "PPMA가 항상 우월"로 인용 금지; 주장 범위 = 실용 저압(≈5 MPa).
- **"comparable" σ_Li**: 7.4 vs 25.5 mS/cm는 3.4× 차이 — soft claim. Li⁺ 수송 무손실이라 단정 금지.
- **전극 내 바인더 σ_e 10⁻¹–10⁻²**: 측정값이 아니라 **추정**(필름 감소율을 복합에 이식).
- **SE셀 "안정성"**: 0.01–1.0 V는 LPSCl의 열역학적 환원 영역(우리 grand-potential 1.242 V) — SE셀 CV 전류에 SE 자체 SEI 형성 기여가 섞였을 가능성을 논문은 다루지 않음(§13.2).
- **-COOLi = Li 재고 소모**: PMA↑일수록 첫 사이클 비가역 피크↑ — 바인더의 Li 소모 페널티를 정량(ICE 분해)하지 않고 prelithiation으로 우회.
- **파우치 유지율 % 미기재**(본문): "improved retention"만; NCM83 파우치의 높은 비용량은 양극 교체(NCM70→83) 기여분 포함 — 바인더 효과와 분리 안 됨.
- **환경 기반 안정성**: PEDOT:PSS의 음극 안정성은 ASSB 환경 효과 — 폴리머 자체가 저전위 안정해진 게 아님. 다른 셀 화학/온도로 일반화 금지.
- **필름 전도도는 의도적 저스펙**(무용매): 문헌 450 S/cm와 직접 비교 금지 — 저자들이 먼저 명시.
- **NCM 양극 복합엔 여전히 C65(0D) 사용** — "carbon-free"는 Si 음극 한정 ([KimCA]의 0D CA 경고와 교차 참조 시 주의).

## 17. 기법 용어 미니사전
- **GIWAXS**: 스침각 광각 X선 산란 — 박막 고분자의 면내/면외 stacking(π-π, lamellar) 상관 해석. d=2π/q.
- **4-point probe**: 접촉저항 배제 필름 전도도/sheet resistance(kΩ/sq) 측정.
- **ex situ 3전극 σ_e**: 전극-SE 사이 Ni mesh를 제3전극으로 삽입, 충방전을 멈춘 상태서 집전체-mesh 간 DC로 전극층 e⁻ 전도도만 분리 측정.
- **σ_Li(on-eff)**: (Li-In)|SE|전극|SE|(Li-In) 대칭셀로 잰 전극층 유효 Li⁺ 전도도.
- **OEP(operando electrochemical pressiometry)**: 정압 셀 내 압력 변동을 충방전 중 기록 — 부피변화 가역성·SOC 균질성 지표(Δ(ΔP)/Q).
- **180° peel test**: 전극-집전체 접착력(N/cm).
- **TOFSIMS**: 이온빔 스퍼터 + 2차이온 질량분석 — 폴리머 내 Li 침투 깊이/분포.
- **⁷Li MAS-NMR**: 고체 Li 화학환경 — Li_xSi 합금상 동정.
- **np ratio**: 음극/양극 면적용량비(여기선 1.6 = Si 63%만 사용).
- **ICE**: 초기 쿨롱효율. **PreLi**: 열증착 Li prelithiation.
- **warm isostatic pressing(WIP)**: 파우치 온간 등방압(450 MPa·80 °C) 치밀화.
- **benzoid/quinoid**: PEDOT 골격 공명구조 — benzoid-우세 = 무처리(용매 후처리 없음) 상태의 지문.
