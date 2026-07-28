# Park 2026 (Adv. Funct. Mater. 36, e16017) — Thiol-Ene Click으로 SBR 바인더 다면 개질(접착 grafting + 가교 cross-linking), 저압 작동 ASSB ★우리 소재계(LPSCl+NCM)·BINDER-화학 중심

> slug `park2026_thiolene_sbr_binder_assb` · DOI `10.1002/adfm.202516017` · type `MPM` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본 `claude/stoic-knuth-NObVQ:docs/lit_park2026_thiolene_sbr_binder_assb.md`.
> 단일-서랍 규칙(CLAUDE.md)에 따라 이관 — 그전까지 DFT webapp 목록에 안 떴다.


**인용:** Young Joon Park, Kyu Tae Kim, Seunggoo Jun, Jong Seok Kim, Jaehyun Yoon, Cheol Bak,
**Yong Min Lee**(공저), Dong Hyeon Kim, Ji Young Kim, **Yoon Seok Jung\*** (교신),
"Multi-Faceted Binder Enhancement via Slurry-Applicable Thiol-Ene Click Chemistry for
Low-Pressure-Operable All-Solid-State Batteries", *Advanced Functional Materials* **36** (2026)
e16017, DOI 10.1002/adfm.202516017. © 2026 The Authors (Open Access, CC-BY, Wiley-VCH).
접수 2025-06-23 / 수정 2025-09-13 / online 2026-01-28. Yonsei Univ.(Chemical & Biomolecular Eng. +
Battery Conflation Eng.) + DGIST(Energy Science) + LG Energy Solution. 교신 yoonsjung@yonsei.ac.kr.
지원: LG Energy Solution + NRF Korea(RS-2024-00343349, RS-2025-25441254). 이해상충 없음.
**연세대 DTBL/Jung 그룹 #264** — `docs/literature_yonsei_dtbl_2026.md` 항목 갱신본.
★ LEAD = **Yoon Seok Jung**(Yonsei); **Yong Min Lee 공저**.

**소재계:** ★ **Li₆PS₅Cl (LPSCl) 황화물 SE + 단결정 LiNi₀.₈Co₀.₁Mn₀.₁O₂ (NCM, 단결정) CAM,
NCM∥(Li-In) 반쪽셀, 0.3 MPa 작동압.** **우리와 같은 소재계**(Bazzoun·#271과 동일, Varkey 할라이드와
다름). **그러나 본 논문의 주제는 BINDER 화학** = **SBR(styrene-butadiene rubber, 슬러리/wet 공정 바인더)**
를 **thiol-ene click**으로 개질: (i) **3MPA(3-mercaptopropionic acid)** grafting → 카르복실(-COOH)
부여 → **접착↑**; (ii) **TMPT(trimethylolpropane tris(3-mercaptopropionate), 삼관능 thiol)** cross-linking
→ 3D 망 → **modulus/탄성↑ → strain 저항**. 개시제 = **AIBN**, 용매 = **p-xylene(비/저극성)**.
도전재 = **Super C65**. SE = **LPSCl(ball-milled, 셀 분리층 d 모름)**. 음극 = **Li-In**(pressiometry는
zero-strain **LTO**).

**★ 관련도 = TIER-2 (우리 소재계지만 BINDER 화학 중심).** **σ_ionic·porosity 절대 앵커가 아니다**
(여기 σ_ionic은 바인더-disruption 특이값 — LPSCl+NCM σ 절대 앵커는 #266/#271/Bazzoun이 보유).
**유효 모델 관련성 = 중간(moderate), binder-mechanics 레버에 집중:** 본 논문의 **cross-link → modulus↑
→ 전극 무결성 유지(저압 cycling)** = 우리 **MPM 바인더-cohesion(`--coh`) 아이디어(E3 레버, 현재 #271 PTFE
void-억제로 동기)**와 **같은 물리** → MPM에 binder-cohesion/modulus 항을 넣을 근거 보강.
⚠ 단 (a) **SBR=wet/슬러리 공정**(공정 특이 — #271 NBR과 같은 부류, 우리 dry PTFE와 다름); (b) **0.3 MPa =
셀 작동/스택압이지 우리 300 MPa 제조압이 아니다**(다른 압력 축 — 명확히 구분); (c) 논문 대부분은
**thiol-ene 합성 화학**으로 우리 물리 밖.

**DB 동반:** 본 논문 σ_ionic 데이터는 **바인더-disruption 특이**(LPSCl 본질 σ가 아님) → **절대 앵커
CSV에 추가하지 않음**(densification_porosity_db.csv / hong2026_sigma_ionic.csv는 #266/#271/Bazzoun이
보유). 머신판독불가 자료(동영상 등) 없음.

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 왜 (중간 정도로) 관련되는가

**저압(0.3 MPa) 작동 황화물 ASSB에서, 슬러리 SBR 바인더를 thiol-ene click으로 (i) 접착-grafting +
(ii) 가교-cross-linking 두 갈래로 개질하니, "가교(modulus↑)가 접착보다 저압 성능에 더 결정적"이다.**
가교형 X-SBR은 Young's modulus를 SBR 0.78 → 14.31 MPa(**약 18배**)로 올려 충방전 중 NCM 부피변화에
대한 **strain 저항·전극 무결성**을 유지 → **100사이클 retention 75% vs SBR 68%**, **초기 방전 163 vs
133 mAh/g**. operando 전기화학 pressiometry(OEP)·in-situ XRD·단면 SEM이 "가교가 계면 delamination·
crack을 억제해 계면저항을 안정화"함을 입증.

**★ 우리 hook(가장 중요 — 정직하게 중간 관련도):**
이 논문은 **바인더의 기계적 망(가교 modulus)이 저압 cycling 무결성을 지배**함을 **정량**한다. 이는 우리
**MPM 바인더-cohesion 레버(`--coh`, audit E3)**가 모델링하려는 **바로 그 물리**다 — 현재 E3 레버는 #271
PTFE void-억제로 동기부여되어 있는데, **#264는 SBR(wet) 쪽에서 같은 "binder modulus → 무결성" 결론을
독립 제공**(2번째 binder-mechanics 입력원). 구체적으로:
- **(A) binder-cohesion E3 레버 보강 ★ 핵심:** "가교 modulus↑ → strain 저항 → 무결성 유지" =
  우리 `--coh`가 잡으려는 SE/바인더 응집의 역학효과. **#264는 modulus를 0.78→23.53 MPa로 sweep하며
  retention과 1:1 상관(단 X14는 agglomeration으로 하락 → 비단조)**을 보여줌 → MPM cohesion 강도를
  "단조 증가"가 아닌 "최적점 있는" 항으로 넣어야 한다는 힌트.
- **(B) SBR=wet 공정 특이(비전이):** SBR/슬러리·p-xylene·thiol-ene은 **wet 공정**(우리 dry PTFE 압축과
  다름; #271 NBR과 같은 부류). 합성 화학·습식 분포는 우리 입력에 없음 → **비전이**.
- **(C) 0.3 MPa = 작동압 ≠ 우리 300 MPa 제조압(다른 축):** 본 논문의 압력은 **셀 작동/스택 유지압**
  (저압 작동성 = 셀 운용 변수). 우리 DEM+MPM의 압력은 **제조(cold-press) 300 MPa**. **둘은 다른 압력
  축** — 같은 "압력"이라고 섞으면 안 됨. (단 70 MPa·3 MPa 비교점도 모두 작동압 영역.)
- **(D) σ_ionic는 절대 앵커 아님:** 본 논문은 σ_ionic 절대값을 거의 보고 안 함(EIS는 R₁/R₂ 계면저항
  중심). LPSCl 본질 σ는 **SI Note 1의 내성 테스트(2.6 mS/cm)** 만 — 이건 "thiol-ene 시약이 LPSCl를
  망치지 않는다"는 **공정 안전성** 데이터지 양극 σ_ionic 앵커가 아니다.

---

## 1. 배경 / 동기 (Introduction, p.1–2)

- 황화물 SE(예 LPSCl)는 높은 이온전도도 + 변형성(cold/warn press로 대면적 제조) → 차세대 ASSB. 그러나
  **변형성에도 SE 입자 간 접촉이 제한적 → 압착 후에도 상당한 void 잔존**(ref[18]) + **복합양극 내 SE의
  복잡한 공간분포 → tortuosity 악화**(ref[12,13]).
- **❗ 저압 작동성이 실전 핵심:** 실용 셀은 수 MPa로 제한되나(ref[17,28]), 학술 ASSB는 흔히 **수백 MPa의
  높은 stack 압**에 의존하는 pellet 셀(바인더 無)을 쓴다. **압력을 낮추면 충방전 중 활물질(CAM) 부피변화가
  계면 접촉을 끊어** 성능 급락 → **바인더의 역할이 결정적**으로 부상.
- **바인더 관점 두 갈래(서론 명시):**
  - **Li⁺-전도성 바인더**(저자 그룹 선행 — solvate-ionic-liquid gel polymer[ref21,23], LiTFSI-NBR[ref24])
    → 바인더-유발 Li⁺ 차단 완화.
  - **접착-강화 바인더**(ref25) → 바인더 함량↓ → 계면 Li⁺ disruption 최소화. 예: Lee et al.[ref26]은
    SBR 블록공중합체에 **carboxylic acid grafting**으로 접착↑; Li et al.[ref27]은 ethylene-methyl
    acrylate 공중합체로 극성/비극성 관능기 변조 → 얇고 유연한 고전도 SE 막.
- **❗ 미해결:** SBR 같은 슬러리 바인더를 **in-situ로 개질하면서도 슬러리 공정성을 유지**하는 것이 과제.
  단순 grafting/cross-linking 후 재용해(g-SBR/X-SBR는 p-xylene에 불용 → Fig S1)는 **균일 바인더 용액
  형성 실패**(polarity mismatch). → **본 연구의 해법: 바인더 전구체(NCM·LPSCl·SBR·AIBN·3MPA 또는 TMPT)를
  슬러리에 함께 넣고, cast/건조 시 가열로 in-situ click 반응** → 가교/grafting을 슬러리 공정 안에서 달성.

- **본 연구(명시):** SBR를 thiol-ene click으로 두 갈래 개질 — ① **3MPA grafting**(carboxylic acid →
  접착↑, SAICAS·peel로 검증) ② **TMPT cross-linking**(삼관능 thiol이 SBR의 allyl(vinyl C=C)과 결합 →
  3D 망 → modulus·탄성↑ → 국소 응력 저항·구조 무결성). **핵심 발견: 저압 성능엔 ② 가교가 ① 접착보다
  훨씬 중요.** (저자 선행 — vulcanization으로 butadiene rubber에 3D 가교망 도입해 2 MPa에서 cathode-SE
  슬립 억제[ref28]의 thiol-ene·슬러리 적용 버전.)

---

## 2. 소재 & 바인더·셀 제작 (Experimental, §4, p.9–10)

### 2.1 ★ 세 바인더 — SBR / g-SBR / X-SBR (Fig 1)
| 바인더 | 개질 | thiol 시약 | 효과 | 비고 |
|---|---|---|---|---|
| **SBR** (pristine) | 없음 | — | 기준(선형 고무) | trans+vinyl C=C 보유; vinyl/trans = **1.327** |
| **g-SBR** (grafted) | grafting | **3MPA**(단관능 thiol+COOH) | **접착↑**(COOH 수소결합) | vinyl/trans = **0.914**; p-xylene 불용(Fig S1) |
| **X-SBR** (cross-linked) | cross-linking | **TMPT**(삼관능 thiol) | **modulus·탄성↑**(3D 망) | vinyl/trans = **0.854**; p-xylene swell만(불용) |
- **thiol-ene click 기전(Fig 1a):** thiol(-SH)이 SBR의 C=C와 공유결합(-CH=CH₂ + HS- → -CH₂-CH₂-S-),
  AIBN의 열라디칼이 개시. **thiol은 vinyl C=C에 우선 반응** → 개질 후 **vinyl/trans 비 감소**(1.327→
  0.914→0.854; FTIR Fig 2a — 968 cm⁻¹ trans, 910 cm⁻¹ vinyl C=C, 698 cm⁻¹ 방향족 C-H). TMPT의 세
  thiol이 SBR allyl과 결합 → **가교 3D 망**(Fig 1a 좌).
- **X-SBR 가교 검증:** C=O(1740 cm⁻¹) + C-O(1180 cm⁻¹) peak 출현(Fig 3a). g-SBR grafting 검증:
  COOH C=O 1714 cm⁻¹ peak.
- **모식(Fig 1b):** grafting → 입자-입자/입자-집전체 접착↑; cross-linking → modulus↑(국소 응력 저항).

### 2.2 ★ X-SBR 가교밀도 series — X6 / X10 / X14 (Fig 3, Table S1)
**"X" 뒤 숫자 = TMPT/SBR 질량비(wt%).** TMPT 6→10→14 wt%로 가교밀도·modulus를 sweep.
| 시료 | TMPT (wt%) | **가교밀도 (×10⁻⁵ mol/cm³)** | **Young's modulus (MPa)** | 인장 파단 strain |
|---|---|---|---|---|
| **SBR** | 0 | — | **0.78** | 파단 없음(200%까지 고무거동) |
| **X6** | 6 | **15.7** | **6.36** | < 50% |
| **X10** | 10 | **19.5** | **14.31** | < 50% |
| **X14** | 14 | **25.6** | **23.53** | < 50% |
- ★ **X10 modulus = SBR의 약 18배**(0.78→14.31). 가교밀도↑ → modulus↑(단조). 가교밀도는 **Flory-Rehner
  용매 swelling법**(THF 3d + n-hexane 2d 추출 → 건조 → toluene swelling)으로 측정(SI §1).
- **인장(Fig 3c):** pristine SBR = 전형 고무거동, 200% strain까지 파단 無. X-SBR = **< 50% strain에서
  파단**(가교로 brittle화) — 단 modulus(초기 기울기)는 X-SBR이 훨씬 높음.
- **나노인덴테이션(Fig 3d):** 동일 50 µN 하중에서 X6/X10이 SBR보다 **얕은 침투깊이**(변형 저항↑).
  ★ **하중 제거 후 탄성회복: X10 66.3% vs SBR 38.2%**(탄성↑ → 사이클 중 부피변화 흡수·복원).
- **결론(저자):** X-SBR이 micro/macro 스케일 모두에서 **기계적 robustness·탄성 우월** → 저압 작동 시
  전극 무결성 유지에 기여.

### 2.3 ★ 접착 — SAICAS + peel-off (Fig 2b/c, Fig S2)
- **SAICAS(다이아블레이드 절삭, 깊이별 접착력, Fig 2b):** g-SBR이 **모든 깊이에서 최고 접착**:
  | 깊이 | SBR | **g-SBR** | X-SBR |
  |---|---|---|---|
  | @Al foil 계면 | 227 | **389** | 234 N/m |
  | @Bulk (25 µm) | 127 | **338** | 148 N/m |
  | @Surface (10 µm) | 151 | **363** | 152 N/m |
  → g-SBR의 우월 접착 = **grafting된 COOH의 수소결합**. X-SBR은 SBR과 비슷(가교는 접착보다 modulus를
  올림). **g-SBR이 가장 균일한 깊이별 접착 분포**(Fig S2; X-SBR도 SBR보다 균일·안정).
- **180° peel-off(Fig 2c):** SBR ≈ 6, **g-SBR ≈ 150**, X-SBR ≈ 8 N/m → g-SBR 압도(SAICAS 확증).
- ★★ **decouple의 핵심:** **g-SBR = 접착 최고**(modulus는 낮음), **X-SBR = modulus 최고**(접착은
  SBR급). 둘을 비교하면 "접착 vs modulus 중 무엇이 저압 성능을 지배하나"를 답할 수 있음(§3).

### 2.4 제작·셀 (§4, p.9–10)
- **양극(슬러리/wet):** NCM : LPSCl : Super C65 : 바인더 = **75 : 22.5 : 1.5 : 1.5** wt%. 전구체를
  **p-xylene 슬러리**에 함께 넣고 carbon-coated Al에 cast → **2단 건조**(상압 1h + 진공 80°C) → 건조 중
  in-situ thiol-ene click(가교/grafting). (SAICAS·peel·top-view SEM용은 SE 없이 **NCM:바인더 = 95:5** 막.)
- **SBR/AIBN/3MPA(또는 TMPT) 질량비 = 100 : 18 : 10**. X-SBR은 TMPT/SBR = x/10 (x=6,10,14).
- **셀 조립(ASSB 반쪽셀):** LPSCl 분말을 **370 MPa**로 펠릿화(SE 분리층) → 양극을 펠릿 위에 → Li-In
  음극(반대편) → poly(aryl-ether-ether-ketone, PEEK) 몰드(d=13 mm), Ti 집전체. **작동압 = 0.3 MPa**
  (NCM∥Li-In; 별도 비교 70 MPa = Fig S10; LTO∥Li-In = 3 MPa = Fig S11).
- **측정:** σ_ionic = Li⁺-blocking Ti∥SE∥Ti 대칭셀 AC 임피던스(10 mV, 7 MHz–10 mHz, **370 MPa**);
  cycling = 0.2C, 30°C, 3.0–4.4 V; DCIR; potential-dependent EIS(formation 중 충전 3.8/4.0/4.2/4.4 V,
  방전 동일 voltage rest 후); **OEP(operando 전기화학 pressiometry)** = zero-strain LTO 음극 + 압력센서
  (0.1 kg 분해능, BONGSHIN; 분해능 한계로 **3 MPa**에서 측정); in-situ XRD(0.05C, ~1 MPa); ex-situ
  단면 SEM(cold-polishing + Ar milling); FTIR; XPS S 2p.

---

## 3. 핵심 메커니즘 — "가교(modulus) > 접착" for 저압 (Fig 2d, Fig 4, Fig 6)

**(1) 가장 의외의 결과 — g-SBR(접착 최고)은 효과 미미, X-SBR(modulus 최고)이 압도(Fig 2d, 0.2C).**
초기 방전용량: **SBR 133 → g-SBR 138(미미↑) → X-SBR 163 mAh/g(대폭↑)**. **g-SBR은 접착이 가장 강한데도
용량 개선이 marginal**(133→138, +5 mAh/g) → **저압 성능엔 접착만으론 부족**. 반면 X-SBR은 접착이 SBR급인데도
**163 mAh/g(+30)** → **modulus/탄성(가교)이 dominant lever**임을 직접 입증.

**(2) 왜 modulus가 중요한가(저압 물리):** 저압(0.3 MPa) + 고전압(4.4 V)에서 NCM의 **부피변화가 계면
접촉을 끊기 쉬움**. 접착이 강해도 **국소 응력에 변형되는 무른 바인더(SBR/g-SBR)는 strain을 흡수 못 해**
계면이 delaminate. **가교 X-SBR은 modulus↑ → 국소 응력에 저항 → 입자 재배치·계면 분리 억제** → 무결성
유지. (저자: "cross-linked binder가 국소 응력 저항에 더 효과적 → strain 축적 최소화 → 입자 detachment 감소".)

**(3) 가교밀도 최적점 — X10(비단조!).** retention·ICE가 X6→X10까지 증가 후 **X14에서 하락**:
- retention(100cyc): **X6 66.8 → X10 72.7~75.0 → X14 71.0%**.
- ICE: **X6 67.6 → X10 70.8~73.1 → X14 71.6%**.
- ❗ **X14 하락 원인 = 과도한 가교밀도 → 입자 agglomeration**(top-view SEM Fig S6) → 분포 악화.
- ⇒ **X10이 최적**(modulus 14.31 MPa, 가교밀도 19.5×10⁻⁵). 이후 모든 비교는 **X10 vs SBR**.

**(4) X10 vs SBR — cycling·계면저항(Fig 4):**
- **초기 방전(0.2C): X10 163 vs SBR 133 mAh/g**; ICE도 X10 우월.
- **rate(Fig 4c, 0.1→1C):** X10 > SBR 전 구간(특히 고율에서 격차).
- **100사이클 retention(Fig 4d): X10 75.0% vs SBR 66.8%**(X10 방전용량도 100cyc 내내 상회).
- **계면저항(DCIR/EIS): X10 92.2 Ω vs SBR 124.5 Ω**(Fig S7) — X10이 낮음(무결성↑).

**(5) operando pressiometry + in-situ XRD — 부피변화 억제(Fig 5):**
- **OEP(Fig 5b, LTO zero-strain 음극으로 양극만 분리):** 충방전 중 ΔP(=P−P_initial) 추적. **X10이 SBR보다
  ΔP 변동이 작음**(Region 1: Li⁺ 추출 시 NCM 수축으로 ΔP 감소가 X10에서 더 작음 = 부피변화 흡수).
  방전 말(Region 3): **X10이 ΔP 회복 우수**(X-SBR 고탄성과 일치 → 가역적 충방전).
- **in-situ XRD(Fig 5e–g):** 충전 시 NCM (101) peak가 격자수축으로 고각 shift. **X10이 SBR보다 큰
  Δ(2θ) shift** → 더 높은 SOC까지 도달(저과전압) = X10의 우수한 반응성. 단 ΔP magnitude는 X10이
  Region 2에서 더 큼(고SOC 더 심한 격자수축 → ΔP↑) — 그래도 가교가 부피변화를 흡수해 계면 delamination
  억제(Region 1).
- **단면 SEM(Fig 5h–l, 100cyc 충전 후):** pristine 상태는 둘 다 치밀(void 적음). **충전 후 SBR =
  입자간 delamination + void/crack(Fig 5i, 빨간 점선)**, **X10 = crack 훨씬 적음(Fig 5k)**. ★ **균열
  면적분율 box plot(Fig 5l, 3장 평균): 충전 후 SBR ≈ 6.x% vs X10 ≈ 4.x%**(충전 전 SBR ~3.5% vs X10 ~3.5%
  유사 → 차이는 cycling으로 발생). ⇒ **가교가 NCM 부피변화로 인한 delamination·crack을 정량적으로 억제.**

**(6) 종합(Conclusion):** thiol-ene click의 두 개질 중 **grafting(접착)은 SAICAS/peel을 크게 개선하나
저압 cycling엔 marginal**, **cross-linking(modulus·탄성)이 저압 작동성·계면 무결성에 결정적**. X10이
**163 mAh/g + retention 75% @100cyc**로 SBR(133, 68%) 압도. **설계지침: 저압 ASSB 바인더는 modulus/
탄성(가교)을 우선 확보해야** 한다. (보너스 — SI Note 2: -COOH + -NH₂ 동시도입으로 self-healing 부여
가능하나 가교밀도↑면 효과 감소.)

---

## 4. 섹션별 결과 — 모든 수치 (Results & Discussion, §2, p.2–9)

### 4.1 바인더 특성화 (Fig 2a–c, Fig 3)
- **FTIR(Fig 2a):** SBR 골격(방향족 C-H 698, trans C=C 968, vinyl C=C 910 cm⁻¹). 개질 후 **vinyl/trans
  비 감소(1.327→g-SBR 0.914→X-SBR 0.854)** = thiol이 vinyl에 우선 반응(ref[48] 일치). g-SBR COOH C=O
  1714 cm⁻¹; X-SBR 가교 C=O 1740 + C-O 1180 cm⁻¹.
- **SAICAS·peel(Fig 2b/c):** §2.3 표(g-SBR 압도; X-SBR≈SBR; g-SBR 깊이분포 최균일).
- **첫 사이클 충방전(Fig 2d, 0.2C·30°C·0.3 MPa·4.4 V):** **SBR 133 / g-SBR 138 / X-SBR 163 mAh/g** →
  **§3(1)의 "접착 marginal, modulus dominant" 근거.**
- **X-SBR series 기계물성(Fig 3, §2.2 표):** 가교밀도 15.7/19.5/25.6, Young's modulus 6.36/14.31/23.53 MPa,
  탄성회복 X10 66.3% vs SBR 38.2%, 인장 파단 SBR 200%↑ vs X-SBR <50%.

### 4.2 전기화학 — X10 vs SBR (Fig 4, Fig S4–S10)
- **첫 사이클(Fig 4a, 0.2C): X10 163 vs SBR 133 mAh/g**(낮은 과전압).
- **potential-EIS(Fig 4b, 충전 3.8/4.0/4.2/4.4 V Nyquist):** flattened 반원 + Warburg tail. **X10이
  모든 전압서 계면저항(R₁) 낮음.** 단 R₁ 차이는 작고(negligible, 두 전극 LPSCl 분리층 bulk 저항 차),
  R₂(GB) 유사, ★ **R₃(계면 charge-transfer)에서 큰 차이** — 충전 진행 시 SBR R₃ 79.8→759.8 Ω(발산),
  X10 28.6→293.2 Ω(완만). NCM 부피변화로 NCM↔LPSCl 계면 delamination → R₃↑, **X10의 우수 modulus가
  strain 완화 → 계면 안정**(Table S3).
- **rate(Fig 4c, 0.1→1C):** X10 > SBR 전 구간(0.2C 복귀 시 X10 ~135, SBR ~105 mAh/g).
- **cycling(Fig 4d, 0.2C·100cyc): X10 retention 75.0% vs SBR 66.8%**, X10 용량 내내 상회, ICE도 우월.
- **DCIR(Fig S7): X10 92.2 Ω vs SBR 124.5 Ω**.
- **가교밀도 series(Fig S4): X6/X10/X14 모두 SBR 능가, X10 최적**(retention 66.8→72.7→75.0→71.0%,
  ICE 67.6→70.8→73.1→71.6%); X14 하락 = agglomeration(Fig S6).
- **고압(70 MPa) 비교(Fig S10):** 70 MPa에서는 SBR/X-SBR 차이 작음(고압이 접촉 강제) → ★ **가교 이점은
  저압(0.3 MPa)에서만 두드러짐**(고압은 압력이 무결성을 대신 확보) — "저압 작동성"이 본 논문 핵심임을 확증.

### 4.3 operando pressiometry·in-situ XRD·SEM (Fig 5)
- §3(5) 참조: OEP ΔP(Region 1 X10 변동↓·Region 3 X10 회복↑), in-situ XRD Δ(2θ)(X10 더 큰 shift = 고SOC),
  단면 SEM 균열면적(충전 후 SBR ≈6% vs X10 ≈4%, Fig 5l box plot).

### 4.4 LPSCl 내성 (SI Note 1, Fig S5, Table S2) — ★ "절대 σ 앵커 아님" 근거
- **thiol-ene 시약이 LPSCl를 망치지 않는가?** pristine LPSCl vs p-xylene 노출 vs p-xylene+TMPT+AIBN 노출
  비교(XRD·EIS·CV).
- **XRD(Fig S5a):** 노출 후 결정구조 변화 negligible(argyrodite 유지).
- ★ **EIS σ_ionic(Table S2): pristine LPSCl = 2.6 mS/cm → p-xylene 노출 1.6 mS/cm(61.5% 잔존) →
  +TMPT+AIBN도 1.6 mS/cm**. → **noticeable 악영향 없음**(약극성 p-xylene이라 부반응 적음; #271 butyl
  butyrate와 같은 "저극성 용매로 LPSCl 보호" 전략). **CV(Fig S5c)**도 전기화학 안정성 유지.
- ❗ **이 2.6 mS/cm는 "LPSCl 분말이 시약에 견디는가"의 공정 안전성 데이터**(Li⁺-blocking 대칭셀)지
  **양극 복합체의 σ_ionic 앵커가 아니다.** (#271은 양극 σ_ionic Pwd 0.087/PTFE 0.064/NBR 0.042 mS/cm를
  직접 보고 → 그게 앵커. 본 논문은 그런 양극 σ를 표로 안 줌.)

---

## 5. 그림 한 장씩 — 무엇을 보이고 우리가 쓸 것

### 본문 Figures
- **Fig 1 (p.3):** ★ (a) thiol-ene click 반응식(SBR + 3MPA→g-SBR grafting / + TMPT→X-SBR cross-linking;
  AIBN 라디칼). (b) 각 바인더 역할 모식(grafting→접착, cross-linking→Young's modulus). → 개질 화학 개요.
- **Fig 2 (p.4):** (a) FTIR(SBR/g-SBR/X-SBR; vinyl/trans 1.327/0.914/0.854). (b) **SAICAS 깊이별 접착**
  (g-SBR @interface/bulk/surface = 389/338/363 압도). (c) **peel-off**(SBR≈6/g-SBR≈150/X-SBR≈8 N/m).
  (d) ★ **첫 사이클 충방전**(SBR 133/g-SBR 138/X-SBR 163 mAh/g) → "접착 marginal, modulus dominant".
- **Fig 3 (p.5):** ★ X-SBR series 기계물성 — (a) FTIR(X6/X10/X14, C=O 1740·C-O 1180 가교 peak).
  (b) **가교밀도**(15.7/19.5/25.6 ×10⁻⁵ mol/cm³). (c) **인장**(SBR 고무 200%↑ vs X-SBR <50% 파단).
  (d) **나노인덴테이션**(X6/X10 얕은 침투 + X10 탄성회복 66.3% vs SBR 38.2%). → modulus·탄성 정량.
  Table S1: Young's modulus 0.78/6.36/14.31/23.53 MPa.
- **Fig 4 (p.6):** ★ X10 vs SBR 전기화학 — (a) 첫 사이클(163 vs 133). (b) potential-EIS Nyquist(충전
  3.8–4.4 V; X10 계면저항↓). (c) rate(0.1–1C; X10 우월). (d) **cycling 100cyc**(X10 retention 75.0% vs
  SBR 66.8% + CE). → 가교의 전기화학 이점.
- **Fig 5 (p.8):** ★★ operando·in-situ 무결성 증거 — (a) OEP 셋업. (b) **OEP ΔP**(X10 변동↓·회복↑;
  Region 1/2/3). (c) 기전 모식(SBR delamination vs X10 가교 유지). (d) 첫 사이클 V(in-situ XRD 조건).
  (e,f) **in-situ XRD (101) peak 진화**. (g) **Δ(2θ)**(X10 더 큰 shift=고SOC). (h–k) **단면 SEM**(충전 후
  SBR void/crack vs X10 clean). (l) **균열면적 box plot**(충전 후 SBR≈6% vs X10≈4%). → 가교 무결성 정량.
- **Fig 6 (Conclusion 도식):** 두 개질(접착 vs 가교)의 역할 + "가교가 저압 무결성에 결정적" 요약.

### SI Figures/Tables (핵심만)
- **Fig S1:** ★ p-xylene 용해성(SBR 완전용해 vs g-SBR/X-SBR 불용) → in-situ click 필요성 근거.
- **Fig S2:** SAICAS 깊이별 접착력-시간(X-SBR이 가장 균일·안정 분포).
- **Fig S4:** ★ X6/X10/X14 cycling(retention 66.8→72.7→75.0→71.0%, ICE 67.6→70.8→73.1→71.6%; X14 하락).
- **Fig S5:** ★ LPSCl 내성(XRD·EIS·CV; pristine vs p-xylene±TMPT+AIBN). **Fig S6:** top-view SEM(X14
  agglomeration). **Fig S7:** DCIR(X10 92.2 vs SBR 124.5 Ω). **Fig S9:** X6/X10/X14 cycling.
- **Fig S10:** ★ **70 MPa** 비교(고압선 차이 작음 → 가교 이점은 저압 특이). **Fig S11:** LTO∥Li-In 3 MPa.
- **Fig S12:** FTIR(SBR/SBR-COOH/SBR-NH₂/SBR-SH; self-healing). **Fig S13:** self-healing cycling(SBR-SH/
  X2-SH/X6-SH; 가교↑면 self-healing 효과 감소).
- **Table S1:** ★ Young's modulus(0.78/6.36/14.31/23.53 MPa). **Table S2:** LPSCl σ(2.6→1.6→1.6 mS/cm).
  **Table S3:** potential-EIS R₁/R₂/R₃ fit(SBR vs X10; 충전 시 SBR R₃ 79.8→759.8 vs X10 28.6→293.2 Ω).
- **Table S4:** ★ 저압 ASSB 문헌 비교(본 연구 = 0.3 MPa·4.4 V·163 mAh/g@0.2C·wet-sheet; coin cell
  0.1–0.3 MPa 추정). → 본 연구의 저압·고용량 경쟁력.

---

## 6. 기술 미니용어집 (우리 맥락)

- **SBR / g-SBR / X-SBR:** styrene-butadiene rubber(슬러리/wet 바인더) 원본 / 3MPA-grafted(접착↑) /
  TMPT-cross-linked(modulus↑). g=grafting, X=cross-linking. **둘은 thiol-ene click의 두 갈래 개질.**
- **thiol-ene click reaction:** thiol(-SH) + alkene(C=C) → thioether(-C-S-C-), 라디칼(AIBN) 개시,
  고수율·빠름·관용. SBR의 vinyl/trans C=C에 thiol 부가 → grafting(단관능 3MPA) 또는 cross-linking
  (삼관능 TMPT). 우리 모델 대응 없음(순수 합성 화학).
- **3MPA / TMPT / AIBN:** 3-mercaptopropionic acid(단관능 thiol + COOH → 접착) / trimethylolpropane
  tris(3-mercaptopropionate)(삼관능 thiol → 가교) / azobisisobutyronitrile(열 라디칼 개시제).
- **vinyl/trans ratio (FTIR):** SBR 백본의 vinyl(910 cm⁻¹) vs trans(968 cm⁻¹) C=C 비. thiol이 vinyl에
  우선 반응 → 개질 후 감소(1.327→0.914→0.854) = click 진행도 지표. 우리 대응 없음.
- **가교밀도(crosslinking density, Flory-Rehner):** 용매 swelling으로 측정한 단위부피당 가교점 몰수
  (×10⁻⁵ mol/cm³). TMPT↑ → 가교밀도↑ → modulus↑. ★ **우리 MPM `--coh`(SE/바인더 응집 강도)의 물리적
  대응** — 가교밀도 = "바인더 망의 강성"을 정하는 분자 변수.
- **Young's modulus / 탄성회복:** 가교밀도↑ → modulus↑(0.78→23.53 MPa). 나노인덴테이션 탄성회복(X10
  66.3% vs SBR 38.2%) = 부피변화 흡수·복원 능력. ★ **우리 MPM E_eff/σ_y(SE 역학) + `--coh`(바인더 망)
  대응**(단 SE 자체가 아닌 **바인더상 modulus**).
- **저압 작동(0.3 MPa) / 70 MPa 비교:** 셀 **작동/스택 유지압**(운용 변수). 0.3 MPa = coin-cell 수준,
  70 MPa = pellet 셀 수준. ❗ **우리 300 MPa = 제조(cold-press) 압 — 완전히 다른 축**(섞지 말 것).
- **SAICAS / peel-off:** V형 마이크로블레이드 절삭(깊이별 adhesive/cohesive 강도) / 180° 박리(접착력).
  g-SBR 압도. ★ **우리 `--coh`(SE cohesion) 측정법 대응**(#271 SAICAS와 동일 — 단 여기선 바인더 접착).
- **operando 전기화학 pressiometry(OEP) / ΔP:** zero-strain LTO 음극 + 압력센서로 충방전 중 양극 부피변화를
  ΔP(=P−P_initial)로 실시간 측정. X10 변동↓·회복↑. ★ **우리 porosity·MPM void-fill·부피변화 대응**
  (#271 Δ(ΔP)_Q와 같은 계열의 부피팽창 지표).
- **R₁ / R₂ / R₃ (potential-EIS, Table S3):** R₁(bulk LPSCl 분리층) + R₂(LPSCl GB) + **R₃(NCM↔LPSCl
  계면 charge-transfer)**. 충전 시 NCM 수축 → 계면 delamination → R₃ 발산(SBR 759.8 vs X10 293.2 Ω).
  ★ 우리 transport(저항=1/σ)에 시간상수 분해 없음 — R₃ 분리는 EIS 고유(우리 대응 없음).
- **in-situ XRD Δ(2θ):** 충전 시 NCM (101) peak의 격자수축 shift = SOC·반응성 지표(X10 더 큰 shift).
  우리 모델엔 결정 격자 축 없음(transport σ만).
- **단결정 NCM(single-crystalline LiNi₀.₈Co₀.₁Mn₀.₁O₂):** 다결정 대비 입계 균열 적은 CAM. 우리 AM_P
  (polycrystalline)와 대비되는 AM_S(single-crystalline) 계열. 단 본 논문은 입경분포·bimodal을 다루지 않음.

---

## ★ 7. 우리 DEM+MPM 비교 — 정직한 중간(moderate) 관련도, binder-mechanics 레버 중심 [frame [1]–[5]]

⚠ **대전제(★ 정직하게):** 이 논문은 **우리 소재계(LPSCl+NCM, ASSB)**지만 **주제는 BINDER 화학(thiol-ene
SBR 개질)**이다. 따라서 **#271(같은 LPSCl, 바인더 공간분포·σ_ionic 절대값)과 달리, σ_ionic·porosity
절대 앵커가 아니다**(여기 σ는 바인더-disruption/공정-안전 특이값). **유효 관련성 = 중간** = **(A) MPM
binder-cohesion 레버(E3) 보강 + (B) 같은-소재계 binder-disruption 정성 데이터**. 비전이 = (a) SBR=wet
공정, (b) 0.3 MPa=작동압≠300 MPa 제조압, (c) 합성 화학.

아래 (a)~(d)를 — **(a) binder-cohesion E3 레버, (b) modulus↔무결성 물리, (c) 압력 축 구분, (d) SBR=wet
비전이 + σ 비앵커** — 명확히.

### (a) ★★ 핵심 연결 — cross-link → modulus → 무결성 = 우리 MPM `--coh` 레버(audit E3)

**그들 핵심 발견(정량):**
- 가교밀도 0(SBR)→25.6×10⁻⁵ mol/cm³(X14)로 sweep → Young's modulus **0.78 → 23.53 MPa**(X10 = 18배).
- modulus↑ → 충방전 중 NCM 부피변화에 대한 **strain 저항·전극 무결성** → **retention 68→75%, 용량
  133→163 mAh/g, 균열면적 6→4%, 계면저항 124.5→92.2 Ω** 개선.
- ❗ **비단조: X14(modulus 23.53, 최대)는 X10(14.31)보다 retention 낮음**(agglomeration) → **최적
  modulus 존재**.

**우리 MPM 바인더-cohesion 레버(E3, `--coh`):**
- 우리 MPM은 `--coh`로 **SE/바인더 응집(cold-weld+vdW)**을 압축 중 attractive σ로 부여(현재 #271 PTFE
  void-억제로 동기). CLAUDE.md: "`--coh`(SE cohesion = SE cold-weld+vdW adhesion = attractive σ in
  compression → changes wallP but NOT porosity)".
- ⇒ **#264는 "바인더 망의 강성(가교 modulus)이 전극 무결성을 정한다"를 같은-소재계(LPSCl+NCM)에서 독립
  입증** → 우리 `--coh`/binder-modulus 항이 모델링하려는 **바로 그 물리의 실험 근거**(2번째 binder-mechanics
  입력원 — #271 PTFE void-억제와 짝). **#264 = SBR(wet) 쪽, #271 = PTFE(dry) 쪽 → 둘 다 "binder 기계물성/
  분포가 ASSB 무결성 지배"로 수렴.**

**★ 우리가 얻는 것(이식 후보):**
- **(i) cohesion 강도 = "최적점 있는" 항:** #264의 **비단조(X10 최적, X14 과가교 → agglomeration 악화)**
  는 우리가 `--coh`/binder-modulus를 **단조 증가**로 넣으면 틀릴 수 있음을 경고. **modulus↑는 무결성↑지만
  과도하면 분포 악화(brittle·agglomeration) → porosity/coverage 악화** → MPM cohesion 항에 **상한/최적
  곡선**을 두는 게 물리적. (단 #264는 작동압·cycling 결과지 제조-압축 결과가 아님 → 직접 이식은 정성.)
- **(ii) modulus는 SE가 아닌 바인더상의 변수:** 우리 E_eff=1.53 GPa(MPM)는 **SE** modulus의 softened
  proxy. #264 modulus(0.78–23.53 MPa)는 **바인더상**(SE보다 3–4 자릿수 낮음). → 우리가 바인더-cohesion을
  넣을 때 **SE modulus(E_eff)와 별개의 바인더 modulus 항**으로 분리해야(섞지 말 것).
- **(iii) "modulus > 접착" → cohesion이 adhesion보다 무결성에 중요:** #264는 **접착(g-SBR, peel 150)이
  최고여도 cycling 효과 marginal, modulus(X-SBR)가 dominant**라 했다. → 우리 MPM에서 **바인더-입자 접착
  (adhesion)보다 바인더 망 강성(cohesion/modulus)이 void-억제·무결성에 더 큰 레버**라는 우선순위를 시사
  (현재 `--coh`가 cohesion(망 강성)을 다루는 것과 방향 일치 — adhesion 별항보다 cohesion 우선이 맞음).

### (b) ★ modulus↔void/무결성 — 우리 MPM void-fill + porosity 대응(정성)

- **그들 OEP ΔP·균열면적·R₃:** X10이 부피변화를 흡수(ΔP 변동↓·회복↑) → **delamination·void·crack 억제**
  (균열면적 6→4%) → 계면저항 안정(R₃ 759.8→293.2 Ω). = "바인더 망이 void 형성을 막는다".
- **우리 MPM:** SE 소성 void-fill(porosity 24.4→15.9%, −8.5%p) + `--coh`(바인더 응집). #264의 "modulus↑
  → void↓"는 우리 **`--coh`가 void-억제에 기여**한다는 방향과 일치(단 우리 `--coh`는 porosity를 직접
  안 바꾸고 wallP만 바꾼다고 검증됨 → #264식 "바인더가 porosity/void를 줄인다"를 우리 MPM이 재현하려면
  **`--coh`를 morphology/void-fill에 연결하는 추가 작업** 필요 — 현재 GAP).
- ⚠ **단 #264 ΔP는 cycling 부피변화**(시간 축), 우리 porosity는 **제조 압축 종점**(단일 스냅샷). 둘은
  **다른 현상**(작동 중 팽창 vs 제조 시 치밀화) → 정성 대응만(절대값 비교 불가).

### (c) ★ 압력 축 — 0.3 MPa 작동압 ≠ 300 MPa 제조압 (반드시 구분)

- **#264 압력:** 0.3 MPa(NCM cycling) / 70 MPa(고압 비교) / 3 MPa(OEP, 분해능) / 370 MPa(SE 펠릿 조립·
  σ 측정). **핵심 변수 = 셀 작동/스택 유지압(0.3 MPa "저압 작동성")**.
- **우리 압력:** DEM+MPM = **제조(cold-press) 300 MPa 표적**(Minnmann anchor). 우리 porosity/σ/coverage는
  모두 "300 MPa로 눌렀을 때의 구조".
- ❗ **둘은 다른 축:** #264의 "저압 작동성"은 **다 만든 셀을 낮은 압으로 운용**(cycling 중 무결성).
  우리 300 MPa는 **셀을 만드는 압**. → **"#264가 0.3 MPa에서 성공했으니 우리도 저압"은 잘못된 매핑.**
  (#264 자체도 Fig S10에서 70 MPa 고압선에선 바인더 차이가 작다고 함 → "저압에서만 바인더 이점" = 작동압
  축 현상.) **우리가 #264에서 가져갈 건 "modulus→무결성" 물리지 압력 수치가 아니다.**

### (d) SBR=wet(비전이) + σ_ionic 절대 앵커 아님

- **SBR/슬러리/p-xylene/thiol-ene = wet 공정**(우리 dry PTFE 압축과 다름; #271 NBR과 같은 부류). 합성
  화학(grafting/cross-linking)·습식 분포는 우리 입력에 없음 → **비전이**(process-specific). vinyl/trans
  비, 가교밀도, FTIR, in-situ XRD Δ(2θ), self-healing 등은 우리 검증 앵커가 **아니다**.
- ❗ **σ_ionic 절대 앵커 아님(정직하게):** 본 논문은 **양극 복합체 σ_ionic을 표로 안 준다**. 유일한 σ는
  **SI Note 1의 LPSCl 내성 테스트(pristine 2.6 → p-xylene 1.6 mS/cm)** = "시약이 LPSCl를 망치나"의
  **공정 안전성**(Li⁺-blocking 대칭셀)이지 양극 σ_ionic이 아니다. → **LPSCl+NCM σ_ionic 절대 앵커는
  여전히 #266/#271(Pwd 0.087/PTFE 0.064/NBR 0.042)·Bazzoun(0.065–0.137)이 보유**, #264는 합류 안 함.
  (참고로 #264의 bulk LPSCl 2.6 mS/cm는 #271 pristine 1.87, Bazzoun pellet 1.02, Cronau 단결정 3.0과
  같은 자릿수 — 셋·넷 다 GB-포함 다결정~단결정 LPSCl 범위. 단 이건 σ_grain 앵커 참고지 양극 σ 앵커 아님.)

### 비교 요약표
| 축 | Park 2026 #264 (LPSCl+NCM ASSB, SBR thiol-ene) | 우리 (LPSCl ASSB, DEM+MPM) | 전이/판정 |
|---|---|---|---|
| 소재 | **LPSCl SE + 단결정 NCM** | **동일 ✓** | 소재는 같으나 주제가 binder 화학 |
| **주제** | **바인더 합성·개질(thiol-ene)** | 압축·transport 물리 | ⚠ 대부분 우리 물리 밖 |
| binder modulus → 무결성 | **0.78→14.31 MPa(18×) → retention 68→75%** | MPM `--coh`(바인더 응집) | ★★ **E3 레버 보강(핵심 연결)** |
| modulus 비단조 | **X10 최적, X14 과가교→agglomeration** | `--coh` 단조 가정 | ★ cohesion 항에 **최적/상한** 필요(힌트) |
| 접착 vs modulus | **접착(g-SBR) marginal, modulus dominant** | `--coh`=cohesion(망 강성) | ★ cohesion > adhesion 우선순위 일치 |
| void/부피변화 | OEP ΔP·균열 6→4%(cycling) | MPM void-fill·porosity(제조 스냅샷) | △ 정성 대응(다른 현상) |
| 압력 | **0.3 MPa 작동압**(70 MPa 비교) | **300 MPa 제조압** | ❗ **다른 축**(섞지 말 것) |
| σ_ionic | **양극 σ 표 없음**(LPSCl 내성 2.6 mS/cm만) | DEM ~0.04–0.18 | ⚠ **절대 앵커 아님**(앵커=#271/Bazzoun) |
| 공정 | **wet/슬러리(SBR)** | **dry 압축** | ⚠ process-specific(비전이) |
| 시간 열화 | 실측(OEP·XRD·SEM, 100cyc) | 단일 스냅샷(없음) | 공통 GAP(Phase 4 후보) |

---

## ★ 8. 우리 작업에 넣을 가장 날카로운 인사이트 3가지

1) ★★ **binder-cohesion E3 레버의 2번째 독립 근거 — "가교 modulus → 무결성"(SBR/wet 쪽).**
   #264는 같은-소재계(LPSCl+NCM)에서 **바인더 망 강성(Young's modulus 0.78→14.31 MPa, 18×)이 저압
   cycling 무결성을 지배**(retention 68→75%, 균열 6→4%, R 124.5→92.2 Ω)함을 정량. = 우리 MPM `--coh`
   (binder-cohesion, audit E3)가 모델링하려는 **바로 그 물리**. 현재 E3는 #271 PTFE(dry) void-억제로
   동기부여 → **#264가 SBR(wet) 쪽 동일 결론을 추가**(두 입력원 수렴: binder 기계물성/분포 → ASSB 무결성).
   ★ 단 SBR=wet·0.3 MPa 작동압이라 **물리(modulus→무결성)만 전이, 수치는 비전이**.

2) ★ **cohesion 항은 "단조"가 아니라 "최적점 있는" 곡선이어야 — X10 최적/X14 과가교 agglomeration.**
   #264의 비단조(modulus 최대 X14가 retention은 X10보다 낮음 — 과도한 가교 → 입자 agglomeration → 분포
   악화)는, 우리가 `--coh`/binder-modulus를 **단조 증가**로 넣으면 틀릴 수 있음을 경고. **"modulus↑ →
   무결성↑이지만 과도하면 morphology/분포 악화"** → MPM cohesion 항에 **상한/최적**을 두는 게 물리적
   (cohesion이 너무 크면 void-fill 흐름·coverage를 오히려 막음). 또 **modulus는 SE가 아닌 바인더상 변수**
   (0.78–23.53 MPa ≪ SE E_eff 1.53 GPa)라 **E_eff와 별개 항**으로 분리해야.

3) ★ **"접착보다 modulus(cohesion)" — 우선순위 확증 + 우리가 못 하는 것(시간 열화) 재확인.**
   #264는 **접착(g-SBR, peel 150 N/m)이 최고여도 cycling 효과 marginal(133→138), modulus(X-SBR)가
   dominant(→163)**라 함 → 우리 MPM이 **바인더-입자 adhesion 별항보다 바인더 망 cohesion(현재 `--coh`)을
   우선**하는 게 맞다는 방향 확증. ❗ 단 #264의 핵심 증거(OEP·in-situ XRD·100cyc 단면 SEM)는 **시간(cycling)
   축 화학-기계 열화**(NCM 부피변화→delamination)로, **우리 DEM+MPM은 단일 제조 스냅샷이라 직접 예측 불가**
   (#271과 같은 공통 GAP) → Phase 4 chemo-mechanical 확장 시 후보(우리 fracture가 균열의 첫 조각이나
   cycling-driven 부피변화 trigger는 없음).

### 보너스 실행 항목
- **#264 인덱스 갱신**(아래 완료): web-abstract 2줄 → 검증 수치(retention X-SBR 75 vs SBR 68%, 용량 163 vs
  133 mAh/g, Young's modulus 0.78/6.36/14.31/23.53 MPa, 가교밀도 15.7/19.5/25.6, vinyl/trans 1.327/0.914/
  0.854, SAICAS g-SBR 389/peel 150, 탄성회복 X10 66.3 vs SBR 38.2%, R 92.2 vs 124.5 Ω, LPSCl 내성 2.6→1.6
  mS/cm, OEP/단면 SEM 균열 6→4%, 압력 0.3 MPa 작동)로 교체.
- ⚠ **혼동 금지(역할 구분):**
  - **#264(이 논문, Park/Jung, LPSCl+NCM, SBR thiol-ene wet):** ★ **MPM binder-cohesion E3 레버 보강
    (modulus→무결성) + 같은-소재계 binder-disruption 정성 데이터**. **σ/porosity 절대 앵커 아님**;
    수치는 wet·작동압이라 비전이, **물리(modulus→무결성)만 전이**.
  - **#271(Hong S-B, LPSCl+NCM, PTFE/NBR):** ★ **σ_ionic·porosity 절대 앵커(Bazzoun에 이은 2번째) +
    PTFE void-억제(audit #5) + GeoDict positioning**. 수치 전이.
  - **두 논문 공통 메시지:** **바인더 기계물성·분포가 황화물 ASSB 무결성을 지배**(#264=SBR 가교 modulus,
    #271=PTFE confined-distribution) → 우리 binder-cohesion 레버의 쌍둥이 근거.
  - **σ/porosity 절대 앵커 = Bazzoun(LPSCl) + #271(LPSCl) + Varkey(halide) + Minnmann** — **#264는 합류
    안 함**(양극 σ 표 없음; 바인더-disruption·공정-안전 σ만).

---

## 9. comparison_vs_ours / properties 반영 메모

- **축 C(mechanics/morphology) ★ 메인:** #264 cross-link → Young's modulus 18× → strain 저항 → 무결성 =
  우리 **MPM `--coh`(binder-cohesion, E3 레버)**의 실험 근거. **modulus→무결성 물리만 전이**(수치는
  wet·작동압 비전이). cohesion 항에 **최적/상한**(X14 과가교 교훈) + **바인더 modulus를 SE E_eff와 분리**.
- **축 A(compaction/porosity):** #264 OEP ΔP·균열면적(6→4%)은 **cycling 부피변화**(우리 제조 porosity와
  다른 현상) → 정성 참고만(절대 앵커 아님). PTFE void-억제 정량 앵커는 #271이 보유.
- **축 B(transport triad):** ⚠ #264는 **양극 σ_ionic 앵커 아님**(LPSCl 내성 2.6→1.6 mS/cm = 공정 안전성).
  LPSCl+NCM σ 앵커는 #271/Bazzoun 유지.
- **축 F(what-we-can't-do-yet):** (i) wet/슬러리 바인더 공정·합성 화학, (ii) 작동압(0.3 MPa) cycling
  무결성, (iii) 시간(cycling) 화학-기계 열화(NCM 부피변화→delamination, R₃ 발산) = 현재 미모델 → Phase 4
  후보(#271과 공통 GAP).
- **압력 축 주의:** #264의 0.3 MPa는 **작동압**, 우리 300 MPa는 **제조압** — comparison에 추가할 때 반드시
  "다른 압력 축"으로 명기.

---

## ★ 10. 비판적 한계 (over-claim 금지)

- **소재는 같지만 주제가 binder 화학 → 직접 전이 매우 제한적:** 논문 분량의 대부분(thiol-ene 합성,
  vinyl/trans, FTIR, 가교밀도 측정, self-healing)은 **우리 물리(압축·transport) 밖**이다. 우리가 가져갈
  건 **단 하나 — "binder 망 modulus → 전극 무결성"이라는 정성 물리**(E3 레버 동기). 수치(modulus·retention·
  σ)는 wet 공정·작동압이라 비전이.
- **0.3 MPa ≠ 300 MPa(가장 흔한 오독 위험):** "같은 압력"이 아니다. #264 = 셀 **작동/스택압**(저압 운용),
  우리 = **제조 압**(cold-press). #264 자체가 70 MPa 고압선에선 바인더 차이가 작다고 함 → 바인더 이점은
  **작동압 영역 특이**. → "저압 성공"을 우리 제조압 모델로 끌어오면 안 됨.
- **σ_ionic 절대 앵커 아님(반복 강조):** 본 논문은 **양극 σ_ionic을 보고하지 않는다**. 2.6 mS/cm는
  "thiol-ene 시약이 LPSCl를 망치나"의 **공정 안전성 대칭셀 σ**지 양극 복합체 σ가 아니다. #271(양극 σ
  Pwd 0.087/PTFE 0.064/NBR 0.042 직접 보고)과 **역할이 다르다** — #264를 σ 앵커로 쓰면 오류.
- **binder-cohesion 이식은 정성·1방향:** #264는 **작동압 cycling 무결성**(시간 축)을 보이지 **제조 압축
  porosity**(우리 출력)를 안 준다. → 우리 `--coh`/binder-modulus 항을 #264에 **정량 fit할 수 없음**
  (modulus→retention 곡선은 cycling 결과지 압축 결과가 아님). "modulus↑→무결성↑(최적점 有)"이라는
  **방향·정성**만 차용 가능. MPM `--coh`가 현재 porosity를 안 바꾼다고 검증된 점(CLAUDE.md)과도 충돌하지
  않게(=`--coh`를 morphology/void-fill로 확장하는 건 별도 검증 필요) 주의.
- **단결정 NCM·입경 정보 부족:** 단결정 NCM이나 **입경분포·bimodal·P:S는 다루지 않음**(우리 AM_P/AM_S·
  Furnas dip 축과 무관). vol% 미명시(75 wt% NCM만) → 우리 φ_SE 축 매핑 불가.
- **modulus 단위 혼동 금지:** #264 modulus(0.78–23.53 **MPa**, 바인더상) ≠ 우리 E_eff(1.53 **GPa**, SE).
  3–4 자릿수 차 — 같은 "modulus"라고 섞으면 안 됨(바인더 vs SE 별개 상).
