# Minnmann 2022 (Adv. Energy Mater. 12, 2201425) — "Designing Cathodes and Cathode Active Materials for Solid-State Batteries" (설계 Perspective)

> slug `minnmann2022_designing_cathodes_solidstate` · DOI `10.1002/aenm.202201425` · type `DEM` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본 `claude/stoic-knuth-NObVQ:docs/lit_minnmann2022_designing_cathodes_solidstate.md`.
> 단일-서랍 규칙(CLAUDE.md)에 따라 이관 — 그전까지 DFT webapp 목록에 안 떴다.


**인용:** P. Minnmann, F. Strauss, A. Bielefeld, R. Ruess, P. Adelhelm, S. Burkhardt, S. L. Dreyer,
E. Trevisanello, H. Ehrenberg, T. Brezesinski\*, F. H. Richter\*, J. Janek\*,
"Designing Cathodes and Cathode Active Materials for Solid-State Batteries," *Advanced Energy
Materials* **2022**, *12*, 2201425. DOI 10.1002/aenm.202201425. Justus-Liebig-University Giessen
(Janek 그룹) + ZfM + KIT(BELLA/IAM) + Humboldt/HZB(Adelhelm). Open Access (CC BY-NC-ND).
Received 2022-04-26 / Revised 2022-07-03 / Published 2022-07-28.

**유형:** ★ **설계 Perspective(논평/리뷰)** — *1차 데이터 논문이 아님.* 타 문헌(자기 그룹 포함)의
정성 결론을 종합해 **무기 CAM(NCM/LFP/LMO/conversion) × 무기 SE(sulfide/halide) 복합양극의 설계
가이드라인**을 제시. 본문은 **거의 전부 정성(qualitative)**: 길이척도별(cell/cathode/particle/interface)
도전과제 → 요구조건 → CAM별 설계전략 → "Guidelines in Short". **공저자에 Trevisanello**(우리가 직전
digest한 SC/PC NCM 논문 저자) **+ Bielefeld**(modeling) **+ Strauss**(SE) 포함 = 우리가 추적해온
Giessen 계보의 종합편.

**소재:** NCM(주로 NMC811) + LFP + LMO/LNMO + conversion(FeS₂/CuS/S) CAM, sulfide(LPSCl/β-Li₃PS₄) +
halide(Li₃InCl₆/Li₃YCl₆) SE. ★ **우리 LPSCl + NCM 계와 직접 같은 설계공간** (LIB 논문들과 다름).

DB 동반 파일: 본 논문은 **수치 앵커를 제공하지 않으므로** 신규 σ/porosity CSV를 만들지 않는다.
대신 `docs/data/densification_porosity_db.csv`의 `ours_minnmann` 행에 대한 **출처 정정**을 본 digest §0이
규정한다(아래).

---

## ★★★ §0. POROSITY-ANCHOR PROVENANCE 판정 (이 digest의 헤드라인) ★★★

> **결론 먼저:** 우리 docs가 "Minnmann"이라 귀속하는 **모든 정량 porosity/밀도/σ 앵커**
> (porosity 14 %, range 13–17 %, σ_ion_eff 0.17 mS/cm, τ_ion 2.07, pure-SE ~10 %)는
> **이 2022 AEM Perspective에 _존재하지 않는다._** 이 논문은 **porosity 수치도, 밀도-압력 곡선도,
> σ 측정값도 단 하나 싣지 않는다(전부 정성).** 그 수치들의 진짜 출처는 **두 개의 다른 1차 논문**이다:
>
> 1. **porosity 14 % (13–17 %), σ_ion_eff 0.17 mS/cm, τ_ion 2.07** → **Minnmann 2021 JES**
>    (P. Minnmann, L. Quillman, S. Burkhardt, F. H. Richter, J. Janek, *J. Electrochem. Soc.*
>    **2021**, *168*, 040537, "Editors' Choice — Quantifying the Impact of Charge Transport
>    Bottlenecks in Composite Cathodes of All-Solid-State Batteries"). **NCM-622 + LPSCl, 건식
>    단축 cold-press 380 MPa, EIS-TLM tortuosity.** ★ 이것이 우리 진짜 앵커.
> 2. **밀도 87 % @ 300 MPa (= porosity 13 %)** → **Sakuda 2013** (75Li₂S-25P₂S₅ glass, cold-press
>    밀도-압력 곡선). 우리 coverage_db의 "three_way_agreement"가 인용하는 그 곡선.
> 3. **pure-SE ~10 % @ 300 MPa** (MPM 3D champion + DEM 보정 표적) → 본질적으로 **2021 JES + Sakuda
>    가 정의한 LPSCl cold-press 치밀화 거동의 우리 보정 표적**이며, 본 2022 Perspective는 그 숫자를
>    "확인"한 적이 없다. `densification_porosity_db.csv`의 `ours_minnmann,...,pure_SE,300,10`
>    행 라벨은 **"Minnmann 2021 JES + Sakuda 2013 cold-press 거동을 우리 보정에서 ~10 %로 anchor"**로
>    재명명해야 정직하다 (2022 Perspective는 그 행의 근거가 아님).

### 갈림(논제 요구 a/b/c) 판정

| 옵션 | 판정 |
|---|---|
| (a) ~10 % pure-SE / 13–17 % composite 가 **이 2022 Perspective 안에** 있다 | ✗ **아님.** 이 논문엔 porosity 숫자가 단 하나도 없다. |
| (b) **다른 Minnmann 논문(2021 JES)**의 값이다 | ✅ **13–17 % composite + σ_ion 0.17 + τ_ion 2.07 = 2021 JES (NCM622+LPSCl, 380 MPa, EIS-TLM).** |
| (c) **Sakuda / 그 외**의 값이다 | ✅ **밀도 87 %@300 MPa(=13 %) = Sakuda 2013(75Li₂S-25P₂S₅).** pure-SE 10 %는 우리 MPM/DEM 보정 표적(2021 JES+Sakuda 거동 위에 세운 것). |

⇒ **(b)+(c) 혼합.** "이 2022 Perspective"는 (a)가 아니다. 우리 docs가 정량 앵커를 "Minnmann"이라고
**연도·논문 구분 없이** 적은 것은 **Trevisanello digest의 σ_S/σ_P 오귀속과 같은 종류의 출처 흐림**이다
(단 이번엔 *연도 혼동*; 값 자체는 실재하며 2021 JES/Sakuda에 정확히 존재). **수치를 인용할 땐 2022 AEM이
아니라 2021 JES / Sakuda 2013을 cite할 것.**

### 추가 발견 — refs.bib 버그 (정정 권고, 본 digest는 파일 미수정)

`docs/paper/refs.bib`의 `@Minnmann2021` 엔트리가 **엉뚱한 논문을 가리킨다**:
- 현재: title "quantifying the impact of charge **rate and inactive components** on cathode
  performance", pages **040502**, DOI **10.1149/1945-7111/abf3a3**.
- 우리 앵커가 필요로 하는 논문: "Quantifying the Impact of Charge **Transport Bottlenecks** in
  Composite Cathodes", pages **040537**, DOI **10.1149/1945-7111/abf8d7**.
⇒ `@Minnmann2021`은 *다른* Minnmann 2021 JES(charge rate/inactive components)를 가리키고 있어,
porosity 13–17 %·τ_ion 2.07 앵커의 인용이 잘못된 논문에 연결됨. (coverage_db.json의 `minnmann_2021_jes`
엔트리는 DOI를 abf8d7로 올바르게 적고 있음 — refs.bib만 틀림.) **본 digest는 파일을 고치지 않으며**
사용자가 paper 빌드 시 정정하도록 플래그만 남긴다.

### 이 2022 Perspective가 실제로 주는 **정량 가이드라인** (porosity가 아닌, "범위·임계" 숫자)

본 논문이 본문에 *직접* 적은 수치는 **설계 임계/범위**뿐이다(측정 데이터 아님). 이것들은 인용 가능:

| 항목 | 값 | 위치/출처 표기 |
|---|---|---|
| CAM 2차입자 최적 지름 | **3–5 µm** | §3.1 (refs 36,37 = Strauss 2018 + Bielefeld 2019 인용) |
| 이온 percolation 위한 CAM 최소분율 | **~50 vol%** (실험)·**60–70 vol%**(기하모델 최적) | §2.1 (refs 14,33–37) |
| 상업 목표 CAM 분율 | **~70 vol% 이상** | §2.1 |
| carbon-free 가능 CAM 임계 | **>60 vol%** (CAM σ_e 충분 시) | §2.1, §3.1 (refs 11,36) |
| 실험실 작동압력(스택) | **수~수십 MPa** | §2.2 ("이런 고압은 상업화 부적합"이라 명시) |
| sulfide SE σ_ion 상한(r.t.) | **~25 mS/cm** | §2 (LPS 계열 일반) |
| halide SE σ_ion (cold-pressed) | **~1 mS/cm** | §2 |
| LFP 본질 σ_e | **~10⁻⁹ S/cm** (Fe-doping 시 ~10⁻³) | §4.1 |
| LMO/LNMO σ_e | **~10⁻⁶ S/cm** | §4.1 |
| NMC811 부피변화 ΔV_max/V | **≈ −5 %** @4.3 V vs Li⁺/Li (수축) | §4.1, Fig 5 |
| conversion CAM 부피변화 | **수십~수백 %** (S 78 %, FeS₂ 65 %, CuS 163 %) | §4.3 |
| 입자크기 상한식 | **L ≤ √(3·D̃_Li / C-rate)** (이론용량 83 % 기준) | Eq (1), Fig 4 |

→ ★ porosity가 *아니라* **"CAM 60–70 vol% / SE PSD를 CAM PSD에 매칭 / 3–5 µm CAM"**가 이 논문의
설계-숫자 기여다. 이것들은 우리 AM:SE 스윕·Furnas dip·P:S 최적과 직접 대조 가능(§비교 참조).

---

## 1. 동기 / 핵심 질문 (Intro, §1)

LIB는 LiMO₂(M=Ni,Co,Mn,Al) 양극으로 성숙했으나, **SSB로 전환 시 CAM 요구조건이 달라진다** — SE의
물성(전기화학 안정성, 기계적 강성)이 LE와 다르기 때문. CAM은 (i) 셀의 유일한 에너지 저장 성분이고
(방전상태에서 리튬화 형태로 존재), (ii) 비용·에너지밀도를 좌우 → **CAM 함량 최대화(분리막 박형화,
anode-free/zero-excess-Li)가 비에너지를 결정.**

**이 논문의 질문:** 무기 CAM을 SSB에 쓰려면 (a) 미세구조/전하수송, (b) (chemo-)역학, (c) 계면화학
3개 층위에서 무엇을 설계해야 하는가, 그리고 CAM 종류별(intercalation/insertion/conversion) 전략은?

핵심 프레이밍: **CAM과 SE는 상보적으로 함께 설계해야 한다**("hard CAM + soft SE 또는 그 반대"가
§6 결론의 한 줄). 우리 frame과 공명: 미세구조가 transport를 1차 결정한다는 철학.

---

## 2. Section-by-section (모든 정성 결론 + 본문 수치)

### 2.1 SSB Cathodes — Challenges (§2) / Cathode Microstructure & Charge Transport (§2.1)

**길이척도 프레임 (Figure 1):** cell(재료분포·PSD·percolation경로) → cathode/microstructure
((chemo)역학·void형성·압력진화) → interface/nanostructure(SE 분해·interphase). ★ 우리 모델 분업과
정확히 겹치는 다층 그림: macro 압밀(DEM/MPM) / micro void·역학(MPM) / nano 계면(우리 미모델).

**핵심 trade-off(§2.1):** CAM 함량↑ → 에너지↑ 이지만 SE 함량↓ → **이온경로 tortuosity↑ → 출력↓.**
∴ "CAM 부피분율 × 전극두께"의 신중한 균형이 필요. 실험은 **~50 vol% CAM**로 이온 percolation 확보,
기하모델은 porosity·균질도에 따라 **60–70 vol% CAM**가 최적. 미래 상업셀은 **~70 vol% CAM** 목표.

**★ Figure 2 (LE vs SE tortuosity) — 우리 C(τ) 항의 직접 정당화:**
- (a) **LE**: 액체가 기공을 채워 **균일 경로 + 낮은 tortuosity**(빨간선 짧음).
- (b) **SE**: 잔류 porosity + grain boundary가 남아 **훨씬 더 tortuous + 높은 overall tortuosity**
  (빨간선 길게 우회). SE는 자체 미세구조(bulk + GB)를 가져 **"apparent tortuosity"가 기하
  tortuosity보다 큼**(전도 나쁜 GB가 추가 페널티).
- ★ 우리 매핑: 이것이 **우리 σ_ionic 식의 C(τ) = a+b·lnτ+c·(lnτ)² 항이 Bruggeman 너머로 필요한
  이유**를 정성적으로 뒷받침. SE 복합양극은 명시적 tortuosity 보정이 필수라는 정성 근거.

**기공의 이중성(§2.1):** SE 양극에서 기공은 **전자·이온 모두 비전도** → porosity는 "최소화 대상"
(LIB와 정반대; LIB는 기공을 LE가 채워 이로움). 단, 기공이 SE-CAM 활성계면적·국소수송에 미치는 영향은
표면coverage·기공크기·분포 모델에 따라 비단조적일 수 있음을 언급(ref 40).

**percolation 의존성(§2.1):** 이온·전자 percolation은 전도상 함량, **PSD**, 처리조건에 의존. **부분
전도도(partial conductivity)가 charge-transport percolation의 적절한 descriptor**라고 명시(ref
29,31,41,49,50) → ★ 우리가 σ_ionic/σ_e를 *유효 부분전도도*로 다루는 것과 정확히 일치.

### 2.2 Chemo-Mechanics during Cycling (§2.2) — Figure 3

**모든 성분이 고체+부피구속** → (de)lithiation 부피/형태 변화가 성능에 직접. **Figure 3:**
- (a) **Cracking**: CAM 입자 균열 → LE는 새 기공 침투(이로움) BUT SE는 **rigid → 침투 못 함 → 수송경로
  길어짐**(해로움). ★ Trevisanello 논문의 "균열 부호가 액체↔고체 반대"와 같은 메시지.
- (b) **Chemo-mechanics**: 큰 부피변화 → CAM-SE **접촉상실**(contact loss) → 계면저항↑.
- (c) **CAM-SE interface**: 액체는 다공표면을 적심(complete wetting), 고체는 **점접촉(point
  contacts) + GB + porosity**만 → 복잡한 CAM 표면형태에서 긴밀접촉 달성이 어려움.

**핵심:** 내부 응력/변형이 SE matrix(분리막 포함)에 균열·접촉상실 유발 → percolation 저하·용량감쇠.
**실험실은 수십 MPa 외압으로 보상하나 상업화 불가** — "Clearly, such high pressures are not suitable
for large-scale commercial applications" (직접 인용). ★ **우리 cold-press 300 MPa는 *제조* 압력이지
*작동* 압력이 아님**을 이 절이 분명히 함(작동은 수~수십 MPa). 우리 fracture/접촉상실 채널의 동기.

### 2.3 Interfacial Compatibility (§2.3)

CAM의 낮은 Li 화학퍼텐셜 → SE 산화분해 → 이온전도 나쁜 상(phosphate/sulfite/sulfate/polysulfide).
완화: (i) 안정 SE(oxide/halide), (ii) **보호 코팅**(LiNbO₃, LiTaO₃, Li₂ZrO₃ — electron-blocker +
Li⁺ conductor). Sulfide는 좁은 안정창 → 코팅 거의 필수. **Halide(Li₃InCl₆/Li₃YCl₆)는 산화안정성↑ →
무코팅 NCM 직접접촉 가능**하나 희토류/전략금속(In,Y) 비용문제. 코팅 자체도 brittle하면 부피변화로
접촉상실 가능 → 약간의 유연성 필요.

### 3. Requirements & Solutions (§3)

**§3.1 Cathode Level:** SE-CAM **PSD 상호 매칭**으로 최대 패킹밀도 + porosity 최소 + 에너지밀도↑.
- ★ **"작은 SE 입자(큰 CAM/SE 크기비) + 구형 CAM = 높은 패킹밀도에 유리"**(refs 30,55,57).
- ★ **NCM 2차입자 3–5 µm = interparticle 연결성에 유리**(비표면적↑·접촉점↑, refs 36,37).
- **CAM >60 vol% + CAM σ_e 충분 → carbon-free 가능**(refs 11,36).
- 처리: slurry tape-casting가 가장 비용효율(SE가 이미 slurry에 있음). **gradient cathode**(집전체쪽
  σ_e↑, 분리막쪽 σ_ion↑) 개념 제시(refs 40,62) — 네트워크저항 이질성 보상.
- ★ 우리 매핑: "작은 SE → 패킹↑·σ↑", "큰 CAM/SE 비 유리"는 **우리 DEM size=packing 결론 + Bazzoun
  작은-SE→σ↑와 독립 일치.** 3–5 µm CAM = 우리 NCM_P/NCM_S 크기대와 정합.

**§3.2 CAM Particle Level — Eq (1), Figure 4:**
- CAM 내부 전자·이온 둘 다 수송돼야 함. 가장 느린 과정이 율속. **L ≤ √(3·D̃_Li / C-rate)** (Eq 1,
  이론용량 83 % 기준). **Figure 4**: NCM(이온확산 한계, D̃≈10⁻¹²–10⁻¹⁰ cm²/s) vs LFP/conversion(전자
  한계, D̃≈10⁻¹⁴–10⁻¹² cm²/s)별 C-rate(0.1/1/5C)에 따른 최대 입자크기 — NCM @1C ≈ 3 µm, @5C ≈ 1 µm,
  @0.1C ≈ 10 µm.
- ★ **작은 입자 trade-off**: 율속↑·확산경로↓ BUT SE-CAM 계면↑ → CEI/열화↑. → 최적 입자크기 존재.
  이것이 우리 PSD 설계가 단순 "작을수록 좋다"가 아닌 이유.
- **Figure 5 (chemo-mechanical 부피변화)**: (a) 여러 CAM의 최대반경변화 Δr_max vs 초기반경 r₀ —
  **작은 입자일수록 절대 부피변화↓**(SE가 흡수 가능). NCM811이 가장 큰 수축. (b) NMC811 a/c축 분해:
  **c축은 4 V까지 팽창 후 수축**(이방성 변형 → 내부응력 → SC도 facet별 접촉상실 가능).

**§4 Design of Individual CAM Types — Figure 6, 7:**
- ★ **Figure 6 (CAM/SE 입자크기 4분면 + tailored PSD) — 우리 P:S 최적의 정성 지도:**

  | | **Large SE** | **Small SE** |
  |---|---|---|
  | **Large CAM** | + 계면열화↓ · − CAM분포·확산경로 | + 이온percolation · − 전자percolation(무탄소)·GB효과 · − 확산경로 |
  | **Small CAM** | + 확산경로·전자percolation · − 이온percolation | + 확산·전자·이온 모두 · − 계면열화·GB효과 |
  | **Tailored PSD(하단)** | \multicolumn{2}{c}{**+ 확산 + 전자 + 이온 percolation + 계면열화↓ + GB효과 최소**} |

  → **"tailored PSD"(bimodal/multimodal)가 모든 축에서 최적** = ★ **우리 bimodal 12:4:1 + Furnas dip의
  정성적 설계 근거.** 단 *어느 조성이 dip*인지 정량 위치는 이 논문에 없음(McGeary/de Larrard 기하가
  소유 — 우리 §비교 D).
- **Figure 7 (chemo-mech 완화전략, 전부 타 문헌 재인용):** (a) SE 선택(LYC vs LPSX)이 PC/SC NCM
  성능에 미치는 영향(0.1–4C rate); (b) PC-NCM은 사이클 중 용량감쇠(균열), **SC-NCM은 안정**(인용:
  ref 86 Han 2021, 88 % retention/200 cyc); (c) **FCG(full-concentration-gradient) rod-shaped
  primary crystallite**로 균열완화(ref 81). ★ Trevisanello 논문 메시지(SC=crack-free)와 동일 계보.
- **§4.1 Intercalation(NCM/LFP/LMO):** NCM811 ΔV/V ≈ −5 % @4.3 V → 접촉상실/균열(Eq 1 경로 길어짐).
  LFP σ_e ~10⁻⁹ S/cm(Fe-doping ~10⁻³) → 탄소 다량 필요(sulfide와 충돌). LMO/LNMO σ_e ~10⁻⁶, 고전압
  4.7 V지만 sulfide 분해 심함.
- **§4.2 Insertion / §4.3 Conversion(FeS₂ 65 %/CuS 163 %/S 78 % 부피변화):** conversion은 거대
  부피변화 + poor 전자/이온전도 → 나노화 + 다량 도전제 필요. CuS는 σ_e ~870 S/cm(전자전도성)로 특이.

### §5 Guidelines in Short / §6 Conclusions

**§5.1 Cathode:** 효과적 이온·전자 percolation + 완전 활성물질 활용 = 부분 유효전도도로 표현됨.
**CAM/SE PSD·입자형상이 이상적 close packing 허용해야**. porosity는 bare minimum으로, **결정질 SE의
유효 이온전도도는 GB 설계로 높여라**. gradient cathode 가능. ★ **이상적으로 CAM과 SE 입자크기·분포를
동시 설계** — 우리 (조성 × 크기비) 공동 최적화와 같은 처방.

**§5.2 Particle:** 입자 균열·내부 porosity 회피. 입자크기·형상을 전자·이온수송에 맞춰 조정(최적 크기
존재). gradient 입자·GB 도핑.

**§5.3 Interface:** 안정 CAM/SE 계면(코팅 or native CEI). 코팅은 Li⁺ 전도 + 충분한 전자전도(de-
lithiation 위해) + 유연성.

**§5.4 Modeling(★ 짧지만 우리에게 직격):** "보통 modeling 연구는 *개선 제안*을 안 하고 SE 최적화
(이온전도↑)에만 집중한다. **우리는 CAM을 다른 입자형상·크기·탄성·SC/conversion으로 다시 생각할 것을
권한다.** 또한 **미세구조 수준의 정교한 mechanical model을 electrochemical·thermal model과 결합**해
압력·온도 효과를 통찰해야 한다." → ★ **이것이 정확히 우리 DEM(transport) + MPM(mechanics) 분업이
지향하는 바.** 이 Perspective가 호명한 "결합된 mechanical-electrochemical-thermal 미세구조 모델"의
한 구현이 우리 작업.

**§6 결론:** CAM 설계는 **SE 성질을 고려해서만** 가능(hard CAM + soft SE 또는 반대). large-scale
ML-aided screening으로 최적 재료조합 탐색 필요. cell-level 통합효과까지.

---

## 3. Figure set ★ (전부 정성/모식 또는 타 문헌 재인용 — 측정 데이터 없음)

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **Fig 1** | 길이척도 모식(cell/cathode/particle/interface). macro→micro→nano 도전과제 | ★ 우리 모델 분업 다층그림(DEM 압밀 / MPM void·역학 / 계면 미모델)과 1:1 |
| **Fig 2** | LE(저 tortuosity, 기공=LE) vs SE(고 tortuosity, porosity+GB) 모식 | ★ **C(τ) 항 정당화** — SE 양극은 명시적 tortuosity 보정 필수(Bruggeman 너머) |
| **Fig 3** | (a)균열 (b)chemo-mech 접촉상실 (c)CAM-SE 점접촉/wetting LE vs SE 모식 | 균열 부호 액체≠고체; SE는 점접촉만 → coverage·접촉상실 동기 |
| **Fig 4** | 입자크기 상한 vs D̃_Li(Eq 1), C-rate별. NCM(이온한계)/LFP(전자한계) 영역 | NCM @1C≈3µm / @0.1C≈10µm — 우리 PSD 설계의 율속 경계 |
| **Fig 5** | (a)Δr_max vs r₀ CAM별(작을수록 변화↓, NCM811 최대) (b)NMC811 a/c축 분해 | NCM811 −5 % 수축·이방성 → 접촉상실/균열(fracture 채널 동기) |
| **Fig 6** | ★ CAM/SE 크기 4분면 + tailored PSD = 모든 축 최적 | ★ **bimodal/Furnas의 정성 설계근거** (정량 dip위치는 없음) |
| **Fig 7** | (a)SE선택 PC/SC rate (b)PC감쇠 vs SC안정 (c)FCG rod결정 — 전부 타문헌 재인용 | SC=crack-free(Trevisanello 계보); 88 %/200cyc(ref 86) |

⇒ ★ **이 논문엔 우리가 디지타이즈할 "측정 곡선"이 없다.** Fig 4/5는 *계산식 곡선*(Eq 1, 부피변화 모델),
Fig 7은 *타 논문 그림 재인용*. 따라서 σ/porosity 수치 CSV를 만들지 않음(헤드라인 §0과 일관).

---

## 4. 시뮬레이션 방법 ★

- **code / 방법:** ★ **없음 — 이 논문은 시뮬레이션을 *수행하지 않는다.*** DEM/MPM/FEM/RNM 어느 것도
  돌리지 않은 순수 설계 Perspective. 본문이 인용하는 modeling은 전부 타 문헌(FEM/voxel tomography:
  refs 30,36,37,51–57; reaction-zone model: ref 62).
- **유일한 "식":** Eq (1) `L ≤ √(3·D̃_Li / C-rate)` (입자크기 상한, 단입자 확산 기준) — 시뮬레이션이
  아니라 해석적 설계식.
- **입자 처리 ★ (DEM판 "무질서 처리"):** 해당 없음(시뮬 없음). 단 **설계 권고로 "구형 CAM이 패킹에
  유리"**(§3.1) + **§5.4에서 "비구형 입자형상을 다시 생각하라"** 명시 → ★ *형상*이 미해결 설계축임을
  이 논문도 인정(= 우리 MPM이 메우는 SHAPE 소성, 그리고 Varkey/Bazzoun이 인정한 "구=타협" 한계와
  동일 계보).
- **전달 솔버:** 없음(단 "partial conductivity가 percolation descriptor"라는 *개념틀*을 우리 σ 정의와
  공유).

→ 따라서 본 digest의 "방법" 비교는 *수치/코드*가 아니라 ***설계철학*** 차원에서만 의미가 있다.
우리가 실제로 *구현*한 것(DEM Kirchhoff/Holm + MPM J2)이 이 Perspective의 §5.4 권고의 한 실현체.

---

## 5. Post-processing ★

- **이 논문 자체:** post-processing 없음(데이터 생성 안 함).
- **인용된 방법론(우리 도구와 매핑용):** voxel/FIB-SEM/μ-CT 미세구조 재구성 + FEM(refs 30,36,37,51,
  52,55–57); EIS 기반 partial-conductivity·tortuosity 측정(refs 29,31,41,49,50 — 그 중 **Minnmann
  2021 JES = EIS-TLM tortuosity**가 우리 τ 앵커); percolation 모델(refs 33–37).
- ⇒ ★ 우리가 흡수할 *post-processing 앵커*는 이 Perspective가 아니라 **그 안에서 가리키는 Minnmann
  2021 JES(EIS-TLM τ_ion 2.07 @42 vol%, σ_ion_eff 0.17 mS/cm)**다.

---

## 6. ★ POROSITY-ANCHOR 출처 정정표 (우리 docs가 "Minnmann"이라 적은 값들)

| 우리 docs의 표기 | 실제 출처 | 정확한 값/조건 | 정정 |
|---|---|---|---|
| "Minnmann 14 % porosity" | **Minnmann 2021 JES 040537** | NCM622+LPSCl, **건식 단축 380 MPa**, avg **14 %**(range **13–17 %**), EIS-TLM | ★ 2022 AEM 아님 → **2021 JES** cite |
| "Minnmann σ_ion_eff 0.17 mS/cm / τ_ion 2.07" | **Minnmann 2021 JES 040537** | @42 vol% CAM, **σ_ion_eff 0.17**, **τ_ion 2.07**(τ_sq 4.3) | ★ **2021 JES** cite |
| "13–17 % @ 300–380 MPa (Minnmann)" | **Minnmann 2021 JES (380 MPa)** + 우리 DEM 표적 | 2021 JES 측정은 **380 MPa**(우리 300 MPa는 같은 *regime*) | 압력 명시(380 vs 300) |
| "밀도 87 % @ 300 MPa" (three_way_agreement) | **Sakuda 2013** (75Li₂S-25P₂S₅ glass) | 밀도-압력 곡선 87 %@300 MPa(=13 %), σ 회복 91 % | ★ **Sakuda** cite (Minnmann 아님) |
| "pure-SE ~10 % @ 300 MPa (Minnmann)" | **우리 MPM/DEM 보정 표적** (2021 JES + Sakuda 거동 위) | MPM 3D σ_y=0.30→**10.0 %**; 2021 JES/Sakuda는 *composite*/glass 13–14 %, 순수 LPSCl 10 %는 *우리 보정 수렴값* | ★ "2021 JES + Sakuda cold-press 거동을 우리 보정에서 ~10 %로 anchor"로 재명명 |
| `densification_porosity_db.csv` `ours_minnmann` 행 | 위와 동일 | `Li6PS5Cl,1.35,pure_SE,300,10,experiment_anchor` | note를 "Minnmann **2021 JES** + Sakuda cold-press; pure-SE 10 %는 우리 MPM 보정 수렴"으로 |

※ ★ 이 2022 Perspective의 정량 기여는 **위 어느 행에도 없다** — porosity 숫자가 아니라 **설계 임계
(CAM 60–70 vol%, 3–5 µm, 작은 SE, tailored PSD)** 뿐이다. 그것은 §0 표·§비교에 정리.

---

## 7. 비교 vs 우리 DEM+MPM (focused §)  →  `litdb/our_dem_baseline.md`

| 축 | 이 논문 (정성 설계 Perspective) | 우리 DEM+MPM (LPSCl ASSB) | 정합/긴장 — 진짜 vs method/출처 |
|---|---|---|---|
| **porosity 절대값** | ★ **없음**(정성) | pure-SE ~10 %@300, real_14 15.6 % | ★ **이 논문은 앵커 아님.** 앵커=2021 JES(13–17 %)/Sakuda(87 %@300) |
| **CAM 분율 최적** | **60–70 vol%**(기하), ≥70(상업), ≥50(percolation 최소) | AM 70–85 wt%(≈SE 30–50 % of solid)에서 우리 corpus 중심 | ★ **정량 일치 방향** — 우리 production core(AM 70–85 wt%)가 그들 60–70 vol% CAM 권고와 정합 |
| **Furnas dip / tailored PSD** | **정성**: tailored PSD가 모든 축 최적(Fig 6) | **정량**: dip @ AM 70–85 wt%, AM:SE 12:1(≫7)·4:1 | ★ **정성→정량 보완**: 그들은 "bimodal이 좋다"까지, *dip 위치/깊이*는 McGeary/de Larrard 기하(우리)가 소유. 소성 MPM은 dip 재현 못 함(frame[4]) |
| **작은 SE → σ↑ / 큰 CAM·SE 비** | **정성 권고**(§3.1, 패킹밀도↑) | DEM size=packing(작은 SE→σ↑), Bazzoun도 동일 | ★ **독립 일치**(설계권고 ↔ 우리 메커니즘) |
| **tortuosity 명시 필요** | **정성**(Fig 2: SE는 GB+porosity로 고 tortuosity) | C(τ)=a+b·lnτ+c·(lnτ)² 항(σ_ionic LOOCV 0.975) | ★ **C(τ) 항의 정성 정당화** — SE양극은 Bruggeman 너머 보정 필수 |
| **partial conductivity = descriptor** | **명시**(§2.1) | σ_ionic/σ_e/σ_thermal 유효 부분전도도 | ★ 개념틀 일치 |
| **압력: 제조 vs 작동** | ★ **작동 수~수십 MPa**, 고압 상업화 불가 명시 | 우리 300 MPa = **제조(cold-press)** 표적 | ★ **중요 구분** — 우리 300 MPa는 *제조* 압력(2021 JES 380과 같은 regime). *작동* 압력(40 MPa)과 혼동 금지 |
| **CAM 부피변화/균열** | NCM811 −5 %@4.3V, 이방성(Fig 5); 균열 SE=손실 | fracture(Auerbach) + dead-AM; AM_P 균열(92:8 8mAh 37–40 %) | ★ **부호 일치**(고체: 균열=손실). Trevisanello(액체=이득)와 반대 케이스로 우리 고체부호 재확인 |
| **σ_e: CAM 종류 의존** | LFP 10⁻⁹·LMO 10⁻⁶·CuS 870 S/cm; carbon-free >60 vol% | σ_e Stage 22.5(NCM endpoint LOCKED) | 우리는 NCM만; 그들 CAM σ_e 스펙트럼이 σ_AM 입력화의 근거(Trevisanello 권고와 같은 방향) |
| **σ_grain 상한** | sulfide ~25 mS/cm, halide ~1 mS/cm(cold-press) | σ_grain 3.0(Cronau 단결정); Bazzoun pellet 1.02 | ★ 우리 3.0(단결정)·Bazzoun 1.02(pellet)·halide 1·sulfide bulk 상한 25 = 일관된 스프레드 |
| **시뮬레이션 방법** | ★ **없음**(설계 Perspective) | DEM Kirchhoff/Holm + MPM J2 | ★ **§5.4가 호명한 "결합 mechanical-echem-thermal 미세구조 모델"의 한 구현이 우리** |
| **입자 형상** | "구형 CAM 패킹 유리" + "비구형 다시 생각" 권고(§5.4) | DEM 구만; MPM 진짜 SHAPE 소성 | ★ 형상이 미해결 설계축임을 이 논문도 인정 = 우리 MPM 가치 + frame[5] 확증 |

**전사 규칙(엄격):**
- ★ **이 2022 Perspective에서 가져올 것 = *설계 가이드라인*(정성/임계)뿐**: CAM 60–70 vol%, 3–5 µm
  CAM, 작은 SE + 큰 CAM/SE 비, tailored PSD, SE는 명시적 tortuosity 필요, partial-conductivity
  descriptor, 균열=손실(고체), 압력 제조vs작동 구분, §5.4의 결합모델 권고.
- ★ **절대 가져오지 말 것 = porosity/σ 정량 앵커.** 그건 **2021 JES(13–17 %, σ_ion 0.17, τ 2.07)
  / Sakuda 2013(87 %@300) / Cronau(σ_grain 3.0) / Bazzoun(0.137/0.101/0.065, pellet 1.02)**가
  소유. 수치를 cite할 땐 *반드시 그 1차 논문*을, *이 Perspective가 아니라*.
- ★ **dip 위치/깊이**: 이 논문엔 없음 → McGeary 1961 / de Larrard 기하(우리) 사용.

---

## 8. 적용 인사이트 (내 연구에 어떻게)

① ★ **출처 정정 = 즉시 액션.** 우리 docs/paper의 모든 "Minnmann porosity 14 %/13–17 %/τ 2.07"
   인용을 **Minnmann *2021 JES* 040537**로, "87 %@300 MPa"를 **Sakuda 2013**으로 명시. `refs.bib`의
   `@Minnmann2021`(현재 040502/abf3a3 = 엉뚱한 논문)을 **040537/abf8d7**로 정정(사용자 fold).
   `densification_porosity_db.csv` `ours_minnmann` 행 note 재명명.

② ★ **설계-숫자 흡수.** 이 Perspective의 **CAM 60–70 vol% 최적 + 3–5 µm CAM + 작은 SE/큰 CAM·SE
   비 + tailored PSD**는 우리 AM:SE 스윕·Furnas dip·P:S 최적의 **권위 있는 정성 프레임**. 우리 production
   core(AM 70–85 wt% ≈ SE 30–50 % of solid)가 그들 권고대와 정합함을 paper intro에서 cite 가능
   (단 *우리가 정량 dip 위치를 제공*한다는 차별점 강조 — 그들은 정성까지만).

③ ★ **C(τ) 항 정당화 + §5.4 호명.** Fig 2(SE 고 tortuosity)는 우리 C(τ) 항이 Bruggeman 너머로
   필요한 이유의 *문헌 권위*. §5.4는 "결합 mechanical-echem-thermal 미세구조 모델"을 *명시적으로
   요구* → **우리 DEM(transport)+MPM(mechanics) 분업이 그 권고의 직접 응답**임을 paper에서 주장 가능
   (Janek 그룹 자신의 리뷰가 우리 접근을 호명).

---

## 9. 인용 가능 문장 (deck/paper용)

- "Minnmann et al. (Adv. Energy Mater. 2022) **호명한** SSB 양극의 결합 (chemo-)mechanical–
  electrochemical 미세구조 모델 요구(§5.4)에 대해, 우리 DEM(접촉망 transport)+MPM(소성 morphology)
  분업이 한 구현을 제공한다."
- "설계 가이드라인(CAM 60–70 vol%, 3–5 µm CAM, 작은 SE + 큰 CAM/SE 비, tailored PSD)은 우리 DEM
  bimodal 12:4:1 + Furnas dip의 정성 근거이며, 우리는 그 dip의 *정량* 위치(AM 70–85 wt%)를 추가한다."
- ★ **출처 주의 문장:** "복합양극 porosity 13–17 % @ 380 MPa 및 τ_ion 2.07 앵커는 **Minnmann
  *2021 J. Electrochem. Soc.* 040537**(EIS-TLM)에서 오며, 2022 AEM Perspective는 *정량 데이터를 싣지
  않는 설계 논평*이다 — 인용 시 구분."

---

## 10. 주의/한계 (over-claim 방지)

1. ★ **이 논문은 1차 데이터가 아니다 — porosity/σ/coverage 측정값 0개(전부 정성).** 우리 정량 앵커의
   출처로 쓰면 **연도 오귀속**. 수치는 2021 JES / Sakuda / Cronau / Bazzoun에서.
2. ★ **두 Minnmann 2021이 있다:** (i) **040537 abf8d7** = "Charge Transport **Bottlenecks**"
   (= 우리 porosity/τ 앵커), (ii) **040502 abf3a3** = "charge **rate and inactive components**"
   (refs.bib가 잘못 가리키는 것). 혼동 금지.
3. **설계 임계(60–70 vol% 등)는 *범위 권고*이지 측정값 아님** — 우리 dip 위치 정량과 대조하되 "그들이
   dip을 측정했다"고 말하면 over-claim(그들은 tailored PSD가 좋다는 정성까지).
4. **압력 제조 vs 작동 구분 필수:** 이 논문의 "수~수십 MPa"는 *작동* 스택압. 우리 300 MPa(2021 JES
   380)는 *제조* cold-press. 같은 숫자 아님.
5. **Eq (1)/Fig 4/5는 해석식·모델곡선**이지 측정 데이터 아님 → 디지타이즈 불가/불필요.
6. **CAM σ_e 스펙트럼(LFP/LMO/CuS)은 NCM이 아님** — 우리 σ_e(NCM) 식에 직접 전이 금지(σ_AM 입력화의
   *동기*로만).
7. ★ **시뮬레이션 비교는 *철학* 차원** — 이 논문은 코드를 돌리지 않으므로 "방법 대조"의 수치 의미는
   없고, §5.4 권고에 우리 구현이 응답한다는 *프레임* 대조만 유효.

---

## 11. 미니 용어집 (technique glossary)

- **partial (effective) conductivity:** 복합양극에서 한 상(SE=이온, AM/탄소=전자)이 만드는 유효
  전도도. percolation·tortuosity·접촉으로 *bulk보다 낮음*. ★ percolation의 적절한 descriptor(본 논문
  명시) = 우리 σ_ionic/σ_e 정의.
- **(apparent) tortuosity τ:** 이온/전자가 우회하는 경로길이 비. SE 양극은 GB+porosity로 *geometric
  tortuosity보다 큰 apparent tortuosity*(전도 나쁜 GB 추가) → Bruggeman σ_eff = σ_bulk·φ/τ². ★ 우리
  C(τ) 항.
- **percolation threshold:** 전도상이 연결망을 이루는 최소분율. CAM 이온 percolation ~50 vol%,
  전자 percolation 전이 ~25–33 vol%(2021 JES). ★ 우리 φc(0.195–0.20).
- **PSD (particle size distribution):** D10/D50/D90. SE를 CAM에 *매칭*해 패킹밀도↑. **tailored
  (bimodal/multimodal) PSD** = Furnas/de Larrard 최적충전. ★ 우리 12:4:1.
- **chemo-mechanics:** (de)lithiation 부피변화(NCM811 −5 %)가 유발하는 응력·균열·접촉상실. SE는
  rigid라 균열을 못 채움(LE와 반대) → 손실.
- **gradient cathode:** 집전체쪽 σ_e↑·분리막쪽 σ_ion↑로 네트워크저항 이질성 보상하는 조성구배 설계.
- **Eq (1) L ≤ √(3D̃/C-rate):** 단입자 확산 기준 최대 CAM 크기(이론용량 83 %). 율속↔크기 trade-off.
- **FCG (full-concentration-gradient):** rod-shaped 1차결정을 방사배향해 이방성 부피변화 상쇄, 균열완화.
- **SC / PC NCM:** Single-/Poly-crystalline. SC=monolithic crack-free(내구), PC=내부GB·균열성.
  (Trevisanello 2021 digest 참조 — 동일 저자 계보.)

---

## 12. 우리 작업에 가장 날카로운 통찰 (Top 3)

1. ★ **헤드라인 = 출처 정정.** 우리가 "Minnmann 앵커"라 부른 porosity 13–17 %·τ_ion 2.07·σ_ion 0.17은
   **이 2022 Perspective가 아니라 Minnmann *2021 JES* 040537**(NCM622+LPSCl, 380 MPa, EIS-TLM),
   밀도 87 %@300 MPa는 **Sakuda 2013**, pure-SE 10 %는 **우리 MPM 보정 수렴값**. 이 논문은 *정량
   데이터를 안 싣는 설계 논평*. + `refs.bib @Minnmann2021`이 엉뚱한 논문(040502)을 가리키는 버그.
   → Trevisanello digest의 σ_S/σ_P 오귀속과 같은 종류(이번엔 *연도 혼동*)이며, paper 인용 정직성에
   직결. **Phase 3/paper 빌드 전 정리 1순위.**

2. ★ **설계 가이드라인이 우리 DEM 결론을 *권위 있게 정성 교차검증*.** CAM 60–70 vol% 최적 + 작은
   SE/큰 CAM·SE 비 + tailored PSD가 좋다는 Janek 그룹의 종합 권고는 — 우리 production core(AM 70–85
   wt%) + size=packing(작은 SE→σ↑) + bimodal Furnas dip과 **방향 일치**. 우리 차별점 = **그들의 정성
   "bimodal이 좋다"에 *정량 dip 위치(AM 70–85 wt%)와 깊이*를 추가**(소성 MPM은 못 하고 DEM/de Larrard
   기하가 소유, frame[4]/[5]).

3. ★ **§5.4가 우리 접근을 명시적으로 호명.** "modeling은 SE 최적화에만 머물지 말고 *CAM을 다른
   형상·크기·탄성으로 재고*하고 *미세구조 mechanical model을 echem·thermal과 결합*하라"는 이 리뷰의
   결론 = **정확히 우리 DEM(transport σ 삼중항)+MPM(소성 SHAPE morphology) 분업**. "구형 CAM 권고 +
   비구형 재고 권고"는 우리 MPM이 메우는 SHAPE 소성 간극, 그리고 Varkey/Bazzoun이 인정한 "구=타협"
   한계와 같은 계보 → **frame[5] 분업이 문헌 권위로 정당화됨**. paper intro에서 "Janek 그룹 리뷰가
   호명한 결합모델을 구현"으로 포지셔닝 가능.

---

*Digest 작성 2026-06-26. ★ 유형 = 설계 Perspective(1차 데이터 아님). ★ POROSITY-ANCHOR PROVENANCE
판정: ~10 % pure-SE / 13–17 % composite / τ_ion 2.07 / σ_ion 0.17 = **Minnmann 2021 JES 040537**(이
2022 AEM 아님); 87 %@300 MPa = **Sakuda 2013**; pure-SE 10 % = 우리 MPM 보정 수렴값. 이 2022
Perspective의 정량 기여 = 설계 임계(CAM 60–70 vol%, 3–5 µm, 작은 SE, tailored PSD)뿐. + refs.bib
@Minnmann2021 → 040537/abf8d7로 정정 권고(파일 미수정).*
