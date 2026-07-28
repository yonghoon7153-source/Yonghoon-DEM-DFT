# Bak 2024 (Chemical Engineering Journal 483, 148913) — 바인더 z-분포 제어 다층 모델전극 + Digital-Twin

> slug `bak2024_binder_distribution_multilayer` · DOI `10.1016/j.cej.2024.148913` · type `MPM` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본 `claude/stoic-knuth-NObVQ:docs/lit_bak2024_binder_distribution_multilayer.md`.
> 단일-서랍 규칙(CLAUDE.md)에 따라 이관 — 그전까지 DFT webapp 목록에 안 떴다.


**인용:** Cheol Bak†, Kyung-Geun Kim†, Hyuntae Lee†, Seoungwoo Byun, Minhong Lim, Hyeongguk An,
Youngjoon Roh, **Jaejin Lim**, Cyril Bubu Dzakpasu, Dohwan Kim, Jongjun Lee, **Hyobin Lee**,
**Hongkyung Lee\*\***, **Yong Min Lee\***,
"Advanced multilayer model electrode for binder distribution within composite electrodes of lithium
batteries", *Chemical Engineering Journal* **483** (2024) 148913, DOI 10.1016/j.cej.2024.148913.
접수 2023-09-08, 수정 2024-01-08, 게재확정 2024-01-18, online 2024-01-29. © 2024 Elsevier B.V.
**Open Access**. †C. Bak·K-G. Kim·H. Lee 동등기여. 교신 yongmin@dgist.ac.kr (Y.M. Lee) /
hongkyung.lee@dgist.ac.kr (H. Lee). 지원: NRF (No.NRF-2021M3H4A1A02048529) + **Hyundai NGV**.
이해상충 없음. 데이터 요청 시 제공.

**소속:** **DGIST**(Daegu Gyeongbuk Institute of Science and Technology) — Department of Energy
Science and Engineering + Energy Science and Engineering Research Center. ★ **Yong Min Lee 그룹
(연세대 이전 DGIST 시절, Digital Twin Battery Lab의 2024 선행작)** — `docs/literature_yonsei_dtbl_2026.md`
의 #260–286 리스트는 2026 publication만 담아 이 2024 논문이 빠져 있었음 → 본 디제스트로 DTBL 항목에 추가.
공저 **Jaejin Lim·Hyobin Lee**는 #266/#271/#262/#286의 digital-twin 모델러진과 동일.

DB 동반 파일: 없음(생성 안 함). 주요 수치는 본 MD 본문 표에 모두 정리.
SI(Fig S1–S11 + Table S1–S2)는 디제스트 반영(비디오 없음).

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 왜 중요한가

**바인더(PVDF) 함량을 깊이(z)방향 3층(top/middle/bottom, 3×30 µm=90 µm)으로 의도적으로 다르게 깐
"다층 모델전극"**(증가 LMH / 감소 HML / 균일 MMM)을 만들어, **층별 접착강도(SAICAS) · 조성(박리 후
EDX) · 전자전도도(bulk+계면, 전극저항계) · 전기화학(rate/cycle)을 측정**하고 **digital-twin 시뮬
(GeoDict)로 상관**시켜 — **고로딩 복합전극의 최적 바인더 분포를 설계**한 논문이다. ★ **결론은 "균일
바인더 분포(MMM)가 최적"** (집전체 근처 바인더 과잉=LMH는 계면저항 폭증으로 최악; 표면 바인더
과잉=HML은 전해질 침투 방해). 즉 **"바인더가 한 곳에 몰리면(국소 과잉) 전자저항↑+전해질 차단,
국소 부재면 기계 붕괴/박리"** 라는 바인더-분포→성능 매핑을 정량화.

**이게 #286(Yoo, porosity z-구배)의 바인더 버전이다:** 둘 다 **z방향 분포(porosity vs 바인더)를
제어해 성능을 최적화**한다. 단 결론 방향이 다름 — **#286은 흑연/액체에서 "구배가 좋다", 이 논문은
NCM622/액체에서 "균일이 좋다"** (소재·물리가 달라 최적 분포가 반대). 둘을 합치면 우리 **Phase 5
graded 설계의 두 자유도(porosity-z + binder-z)**가 채워지고, **바인더 분포 → 접착/전자전도 매핑은
우리 MPM `--coh`(binder cohesion, audit E3) 레버의 published 실증**이 된다 (#271 PTFE void↓ +
#264 cross-link modulus와 수렴).

**우리 hook(가장 중요):**
1) **Phase 5 = z-band 합성에 "바인더 함량(z)" 축을 추가**할 근거(이 논문 = binder-z, #286 = porosity-z).
2) **바인더 분포 → 접착강도·전자전도 정량 매핑** = E3 `--coh` 레버가 "한 곳 과잉=저항↑+차단 / 부재=박리"
   를 재현해야 한다는 실험 타깃.
3) ⚠ **소재 = NCM622 + 액체전해질(LiPF₆) + PVDF 일반 LIB** — **우리 LPSCl sulfide ASSB가 아님** →
   **절대 transport/용량 값은 전이 불가**; 가져올 것은 **z-분포 설계개념 + 바인더→접착/전자전도 매핑 +
   digital-twin positioning**(수치 앵커 아님 — LPSCl σ 앵커는 `docs/lit_bazzoun2026_dem_fem_rnm.md`
   + #271).

---

## 1. 배경 / 동기 (Introduction, p.1–2)

- EV 에너지밀도 요구 → **로딩레벨(mAh/cm²)↑**이 가장 실용적 경로. 그러나 **슬러리 습식공정은 로딩
  상한**(슬러리 유변학 한계, 고형분 최대여도 한 번에 두꺼운 코팅 불가) → 중간단계로 **multi-coating
  슬러리**가 개발됨. 핵심은 **각 성분의 균일성 확보**.
- ★ **문제(핵심 동기):** 슬러리에 잘 분산돼 있던 **고분자 바인더가 건조 중 용매와 함께 이동
  (solvent evaporation-driven migration)** → **깊이방향으로 비균일 분포**가 됨. 특히 **로딩↑·바인더
  less(저바인더)일수록 분포가 더 나빠짐**(참고문헌 11–13). 건식 코팅은 더 심한 비균일을 유발(11).
- **비균일 바인더의 양면 폐해(참고문헌 14–17):**
  - **국소 과잉(locally excessive binder):** 전극 내부 **전자저항↑** + **과도한 전해질 함침으로 전극
    성분 탈리(detach)**(16).
  - **국소 부재(absence of binder):** **전극층 기계붕괴/박리(delamination)**(17).
  → 따라서 **균일 바인더 분포가 중요**(이게 통념). 그러나 기존 연구들(Muller 18=PVDF·흑연 건조온도 /
    Kim 19=LiCoO₂ / Font 20=시뮬 / Liu 21–24=slot-die 2층)은 **분포만 건조온도로 바꿔봤지, 특정
    복합전극의 *최적* 바인더 분포가 무엇인지는 결정 못함**. → **더 체계적인 실험이 필요**.
- **이 논문의 제안:** **최소 3층(three-layer) 모델전극으로 바인더 분포를 직접 제어** → 기존보다 정밀.
  세 층 모델: **증가(LMH) / 감소(HML) / 균일(MMM)**. **SAICAS 접착강도 + 박리 후 EDX F-매핑**으로
  층별 바인더 정량, **전극저항계로 bulk+계면 전자저항**, **rate/cycle 전기화학**, **digital-twin
  3D 시뮬로 전자전도·전위·전류밀도**를 묶어 → **고로딩 복합전극의 최적 바인더 분포 설계 플랫폼** 제시.

**약어 정리:** CBD = carbon-binder domain(도전재+바인더 통합상, 나노다공 매트릭스). PL = (이 논문엔
없음 — #286과 혼동 금지). H/M/L layer = 바인더 high/middle/low 층. HML/MMM/LMH = 위→아래 층순서.
Ref = 단층(single-layer) 기준전극(전층 M=93:3:4). SAICAS = Surface And Interfacial Cutting Analysis
System. EDX = Energy Dispersive X-ray spectroscopy.

---

## 2. 소재 & 제작 (Experiments §2.1–2.6, p.3)

### 2.1 모델전극 설계 (공통)
- **활물질:** **NCM622 = LiNi₀.₆Co₀.₂Mn₀.₂O₂** (양극). + **conductive carbon**(전자 도전재) +
  **PVDF**(polyvinylidene fluoride 바인더). **입경(시뮬) 10 µm**.
- **로딩/두께:** areal capacity **3.5 mAh/cm²**, 전극밀도 캘린더링 후 **3.0 g/cm³**. 단층 Ref =
  **두께 90 µm**, 4 h 건조. (SI Table S2: loading level 20.61 mg/cm² [원문 단위 mg m⁻² 오타로 추정,
  3.5 mAh/cm² 정합은 ~20 mg/cm²], 캘린더 후 두께 **68.7 µm**.)
- **단층 전극 조성(Ref, 건조온도 연구용):** NCM622 : carbon : PVDF = **93 : 3 : 4 wt%**.
- **다층 모델(핵심):** 3층, **각 층 30 µm → 총 90 µm**. 층별 조성(NCM:carbon:PVDF wt%):
  - **H layer(바인더 high):** **93 : 1 : 6** (도전재↓·바인더↑)
  - **M layer(바인더 middle):** **93 : 3 : 4**
  - **L layer(바인더 low):** **93 : 5 : 2** (도전재↑·바인더↓)
  - ⚠ **NCM 93 wt% 고정** — 바뀌는 건 **carbon↔PVDF 비율**만(총 도전재+바인더=7 wt% 고정). 즉
    "바인더 분포"는 곧 **CBD 안의 carbon:binder 비율 분포**.
  - SI Table S2의 L layer "9.3:5:2"는 오타(93:5:2가 맞음 — 본문 §2.1 명시).
- **세 분포 모델(Fig 1 하단):**
  | 모델 | top층 | middle층 | bottom층(집전체쪽) | 바인더 z-경향 |
  |---|---|---|---|---|
  | **Ref** | 93:3:4 | 93:3:4 | 93:3:4 | 균일(단층) |
  | **HML** | **93:1:6 (H)** | 93:3:4 (M) | **93:5:2 (L)** | top 과잉 → 아래로 **감소** |
  | **MMM** | 93:3:4 (M) | 93:3:4 (M) | 93:3:4 (M) | **균일**(3층 동일조성) |
  | **LMH** | **93:5:2 (L)** | 93:3:4 (M) | **93:1:6 (H)** | bottom(집전체) 과잉 → 위로 **증가** |
  - 집전체 = **Al foil**.

### 2.2 다층 전극 제작 공정 (Fig 1a, SI Fig S1)
1) 각 층 슬러리 = **NMP-기반, 고형분 70 wt%**. doctor blade **40 µm gap, 160 °C 1 h 건조** → 첫 층을
   집전체에 캐스팅. 2) 첫 층(non-calendered) 위에 **30 µm gap**으로 둘째 층 캐스팅, 같은 조건 건조.
   3) double layer 위에 **60 µm gap**으로 셋째 층 캐스팅, 같은 조건 건조. 4) 바인더 결정성 수렴 위해
   **추가 160 °C 1 h 건조**. → ★ **모든 층을 동일 160 °C로 건조**(건조온도 변수를 고정해 **분포만**
   순수 변수로 분리 — 기존 연구는 분포를 온도로 바꿔 교란).
   - 캘린더링: roll press **2 m/min**, 목표밀도 **3.0 g/cm³**.

### 2.3 건조온도 예비연구 (단층, §3 도입부, Fig 2)
- 단층 NCM622(93:3:4) 전극을 **80/120/160/200 °C** 건조 → SAICAS 접착강도 깊이프로파일 + EIS +
  결정성 측정. 목적: **"건조온도로 분포 제어"의 한계를 보이고, 본 연구의 다층(온도-고정) 접근 정당화**.

### 2.4 바인더 분포 분석법 (§2.2)
- **(1) SAICAS:** 보론나이트라이드 마이크로블레이드(폭 1 mm, rake각 20°, clearance각 10°)로 표면부터
  **10 µm 간격**으로 수직·수평 절삭(vertical/horizontal rate 0.2 / 0.1 µm/s) → 목표깊이 도달 후
  **수평 절삭(2 m/s [원문, µm/s로 추정])** 하며 **수평력(horizontal force) 측정 → 각 층 접착강도 산출**.
  M층 접착강도를 각 전극에서 **100%로 정규화** → 전극 간 비교.
- **(2) 박리 후 표면 EDX:** SAICAS로 **10 µm씩 수평 절삭한 노출면**에서 **F(불소) 원자비 측정**
  (=PVDF 양). 전자빔 15 kV, ×1000. ★ **기존 단면 EDX(cross-sectional)는 좁은 라인(80–100 µm)만
  보고 분포가 단면이 아니라 in-plane이라 부정확** → 표면 EDX(넓은 60×100 µm² 면, F 더 많이 수집)로
  **신뢰도↑**(Fig S4). + **비캘린더 상태로 측정**(캘린더링이 secondary-particle 활물질을 파괴해
  접착강도 왜곡 — Fig S5).

### 2.5 전기화학 셀
- **Half-cell:** 2032 coin, Li 상대전극, PE separator(20 µm), 전해질 **1.15 M LiPF₆ in EC/EMC
  (3:7 v/v) + 2 wt% VC**, NCM622 양극(Ø14 mm)/흑연 음극(Ø16.2 mm, full-cell용)/Li. 36 h aging.
  formation 0.1C CC-CV(4.3 V cutoff, 0.1C 종료), discharge 0.1C(3.0 V). stabilization 0.2C 3사이클.
  rate: discharge **0.2/0.5/1/2/4/6C**(charge 0.2C 고정), 3.0–4.3 V. cycle: charge 1C / discharge 1C.
- **Full-cell:** NCM622 양극 + **흑연 음극**, 1C/1C, 동일 전압창.
- **EIS:** VSP-300(BioLogic), AC 진폭 14.1 mV, **5 mHz–10 kHz** sweep.
- **전자저항(electrode resistance meter, RM2610 Hioki):** **계면저항(interfacial) + bulk 저항률**을
  분리 측정(전류 0–1 mA, 전압 0–0.5 V). 캘린더(3.0 g/cm³) 후 측정.

### 2.6 Digital-Twin 3D 전극모델 (§2.6) — ★ positioning 대상
- **도구 = GeoDict2023 (Math2Market)**. (#266/#271/#281/#284/#286과 **동일 상용 엔진** → positioning
  `docs/positioning_vs_geodict.md` 그대로 적용 — top-down/reconstruction 도구.)
- **절차:**
  1) **GrainGeo 모듈**로 NCM 활물질을 **구형(spherical)**으로, 실험 부피분율 기반 생성 → 두께방향
     **3층(top/mid/bottom)** 분할.
  2) **CBD(carbon-binder domain)**를 각 층의 **carbon:binder 비율에 맞춰 stochastic하게 배치**
     (Fig S9). CBD는 **나노다공 매트릭스**(carbon black 입자 + PVDF, 둘 다 직경 20 nm).
  3) **ConductoDict**로 각 CBD 모델(H/M/L)의 **유효 전자전도도**를 nano-matrix 기반으로 계산
     (porosity ~30 % 가정) → 그 값을 HML/MMM/LMH 전극구조에 적용해 **전자흐름(전위·전류밀도)** 평가.
  - ⚠ **이 논문의 digital-twin은 전자전도(electronic)만** — 이온수송/전기화학 풀모델은 없음(#286의
    BESTmicro 3D 전기화학과 다름). 즉 **"바인더 분포 → CBD 전자전도 → 전극 전위/전류분포"** 폐회로.
  - SI Table S1(CBD): 도메인 300×300×400 nm³, voxel 1 nm, 입경 PVDF/carbon 20 nm, 고유전도도
    PVDF 0 / carbon **18 S/m**, pore 30 vol%; 조성 **H = PVDF 6.5 / carbon 63.5 / pore 30 vol%**,
    **M = 31.8 / 38.2 / 30**, **L = 51.5 / 18.5 / 30 vol%**.
  - SI Table S2(전극): 도메인 30×30×68.7 µm³, voxel 100 nm, NCM 입경 10 µm, true density NCM
    4.7 / PVDF 1.6 / carbon 1.78 g/cm³, NCM 고유전도도 4.5 S/m, CBD 전도도 = 시뮬 계산값.

---

## 3. 핵심 메커니즘 — 바인더 분포가 전자·이온 전도를 어떻게 가르나

전자(electron)는 **집전체(아래)에서 공급 → 전극 위로**, Li⁺은 **separator(위)에서 전해질 통해 아래로**.
바인더(PVDF, 전자절연)는 **CBD의 도전성을 떨어뜨리고 전해질 함침을 막는다**. 따라서:

**(1) 전자 경로 관점:**
- **집전체 근처(bottom)에 바인더 과잉(=LMH의 H층)** → **CC↔전극 계면에서 전자공급이 막힘** → **계면
  저항 폭증** → 전극 전체 활성화 저해(가장 나쁨).
- **집전체 근처에 바인더 부족(=HML의 L층, carbon 5%)** → 전자공급은 원활하나 **표면(top)의 H층이
  전해질 침투를 막아** 위쪽 반응 저해.
- **균일(MMM)** → 어느 층도 막힘 없음 → **계면저항 최저 + 전위구배 일정**.

**(2) 이온/전해질 관점:**
- **표면(top) 바인더 과잉(=HML의 H층)** → **전해질이 위에서 못 들어옴**(함침 방해) + 바인더 swelling이
  이온경로 더 좁힘 → 전극 내부 반응 불충분.

**(3) CBD 전자전도의 비선형성(★ digital-twin 핵심):**
- CBD의 유효 전자전도는 carbon:binder 비율에 **민감·비선형**. **바인더 과잉(H) → ~0 S/m**(도전망 끊김),
  **바인더 부족(L) → 375 S/m**(연속 도전망). → **국소 바인더 과잉 한 층이 전체 전자경로를 차단**할 수 있음.

⇒ 우리 식으로: **"바인더(절연·차단상)의 z-분포가 전자 percolation(아래서 위)과 전해질 침투(위서 아래)를
동시에 게이트한다 — 한쪽 끝에 몰리면 그 방향 수송이 막힌다."** 균일이 양쪽 모두 안 막혀 최적. 이건
**바인더 = obstacle/차단상**(우리 `additives.py` σ=0 차단 + MPM `--coh` 결합상)의 **분포 효과 실증**.

---

## 4. 섹션별 결과 — 모든 수치

### 4.1 건조온도 예비연구 (단층, Fig 2, p.3–4)
- **SAICAS 접착강도 깊이프로파일(Fig 2a):** 건조온도↑(120→160 °C) → **바인더가 표면(top)에 집중**
  (높은 건조율 → 용매대류로 바인더가 위로 = binder sedimentation 반대 방향). **80 °C는 반대로 집전체
  계면에 집중**(느린 건조 → 바인더 침강). **200 °C는 표면집중 더 심함**.
  - 접착강도 절대값(Fig 2a, N/m): 160 °C가 표면 ~110 N/m(최고)에서 깊이따라 ~50으로, 80/120 °C ~50
    근방 균일, 200 °C ~45 균일. (digitize TREND only.)
- **EIS(Fig 2b):** 200·80 °C가 **최저 저항이 아님** → "균일 분포(200 °C 기대)면 저항 낮을 것"이란
  단순예측이 틀림. **원인 = 건조온도가 바인더 *결정성*을 바꿈**(Fig 2d).
- **사이클(Fig 2c):** 160 °C 건조가 최고 용량(~172 mAh/g @ 100cyc), 200 °C 최저(~165).
- **결정성(Fig 2d, XRD):** 건조온도↑ → **PVDF·CBD 필름 결정성↓** (160 °C에서 재결정 최소; 200 °C는
  PVDF 융점 165 °C 이상 재결정으로 오히려↑). **PVDF film 결정성 48→46→38→40 %**(80/120/160/200 °C),
  **CBD film 34→33→30→30 %**.
  → ★ **결론: 건조온도 제어법은 "분포"와 "결정성·전해질함침·접착"을 한꺼번에 바꿔 *최적 분포만* 분리
    불가** → **본 연구는 160 °C 고정 + 층-조성으로 분포만 제어**(깨끗한 변수 분리)가 정당.

### 4.2 바인더 분포 측정 — SAICAS + 표면 EDX (Fig 3, p.5)
4개 모델(Ref/HML/MMM/LMH) 모두 **비캘린더 + 표면 EDX(F 원자비) + SAICAS 접착강도**를 깊이별로:
| 모델 | F 원자비 깊이경향 (Fig 3a) | SAICAS 접착강도 깊이경향 (Fig 3b) |
|---|---|---|
| **Ref(i)** | 표면·계면 쪽 **약간 집중**(non-uniform, ~10–13 %) | 변동큼(~100–150 %), 표면·계면 집중 |
| **HML(ii)** | 위(top)서 아래로 **감소**(~16→10 %) | 위서 아래로 **감소**(~130→80 %) |
| **MMM(iii)** | **거의 균일**(~11–12 %, 평탄) | **거의 균일**(~100 %, 평탄) |
| **LMH(iv)** | 아래서 위로 **증가** = 위로 갈수록↑(~10→20 %) | 아래서 위로 **증가**(~80→200 %) |
- ★ **F-원자비(EDX, 바인더 양)와 접착강도(SAICAS)가 강한 상관** → **두 독립측정이 같은 분포를 줌**
  (교차검증). LMH의 분포구배가 HML보다 **약간 더 가파름**(연속 캐스팅 시 윗 슬러리가 아랫층에 부분
  침투 → 부드러운 interlayer 연결).
- Ref는 **두꺼운 단층 슬러리 건조** → 바인더가 표면·계면 양쪽으로 이동(in-plane 불균일도 큼, porosity
  표면쪽↑). MMM은 얇은 3층을 각각 건조 → 가장 균일.

### 4.3 전자저항 — bulk + 계면 (Fig 4a, 전극저항계, p.6)
- ★ **계면 전자저항(interfacial electrical resistance, mΩ·cm²):** **MMM ≈ 최저 ≪ Ref < HML(최저
  bulk지만) ≪ LMH(폭증 ~1500–1600 mΩ·cm²)**. (Fig 4a 막대: Ref ~280, HML ~10, MMM ~150, LMH ~1600
  — digitize TREND.)
  - ⚠ **bulk 전자저항률**과 **계면 전자저항**이 모델별로 다른 방향:
    - **HML(top 바인더과잉, bottom carbon 5%)** → 집전체 근처 carbon-rich → **계면저항 최저** + bulk
      도 낮음. 그러나 표면 바인더과잉이 **전해질 차단**(전기화학에선 불리, §4.4).
    - **LMH(bottom 바인더과잉)** → 집전체 근처 바인더가 전자공급 차단 → **계면저항 최고(최악)**.
    - **MMM** → 균일 → 계면저항 낮음 + 전위구배 일정.
- ★ **Digital-twin 전자전도(Fig 6, §4.5와 연결):**
  - **CBD 모델 유효 전자전도도:** **H = 0 S/m, M = 115.36 S/m, L = 375 S/m**(바인더↑ → 도전망 끊김).
    (본문은 M·H를 "L 대비 ~8.4 %·~0 %"로도 표현 — 상대% 기준이 모호하나 **절대값 0/115.36/375 S/m가
    1차 수치**.)
  - **전극 전체 유효 전자전도도:** **HML 6.94 / MMM 2.46 / LMH 3.02 S/m**. → HML이 가장 높음(bottom
    carbon-rich L층 덕). MMM·LMH는 비슷(이질구조).
  - 그러나 **전기화학 성능 최적은 MMM**(아래) — **전자전도 절대값↑(HML)이 곧 성능↑가 아님**: 표면
    바인더과잉(HML)이 전해질 침투·반응 균일성을 해쳐 net 손해. **계면저항 + 전해질 접근성 + 균일성의
    종합**이 지배.

### 4.4 전기화학 — formation·rate·cycle (Fig 5, p.6–7)
- **Formation(0.1C, Fig 5a):** 4개 모델 방전용량 **대체로 유사**. LMH만 약간 과전압.
- **0.2C stabilization(Fig 5b):** **LMH·HML 용량이 Ref·MMM보다 감소**, **LMH에서 큰 과전압**(전자저항
  추세 Fig 4와 동일).
- **★ Rate capability(Fig 5c, charge 0.2C / discharge 0.2–6C):**
  - **C/5·C/2(저율):** Ref·MMM이 최고(~mAh/g 수준).
  - **>0.5C부터** MMM의 용량감소가 Ref보다 **작음**(균일 도전망의 효과적 연결).
  - ★ **고율(≥4C):** 차이 극대 — **MMM > Ref > HML ≫ LMH(붕괴)**. **MMM(균일)이 고율 최우수**.
  - **HML**(비균일·표면과잉)은 Ref보다 초기용량↓·열화율↑. **LMH는 0.5C 넘으면 급격붕괴**(집전체
    바인더과잉 → 전자공급 차단이 고율에서 치명적).
- **Cycle(1C/1C, Fig 5d, 250cyc):** **MMM 최고 retention(~130 mAh/g 유지) > Ref(~120) > HML(~70)
  ≫ LMH(~10, 최악)**. (SI Fig S7 1C/1C·Fig S8 0.2C/0.2C도 동일 추세.)
- ★ **핵심 해석:** **집전체 근처 바인더과잉(LMH)이 표면 바인더과잉(HML)보다 훨씬 더 해롭다** —
  같은 비균일이어도 **위치가 중요**. 균일(MMM)이 전 영역에서 우월.

### 4.5 Digital-Twin 전자흐름 시뮬 (Fig 6, p.7) — ★ positioning 대상
- **(a) CBD/전극 유효 전자전도도(Fig 6a,c):** §4.3 수치(H/M/L = 0/115.36/375 S/m; 전극 HML/MMM/LMH
  = 6.94/2.46/3.02 S/m). 이질구조(HML·LMH)가 비슷한 유효 전자전도.
- **(b,c) 전위(potential) 분포(Fig 6b,c, SI Fig S11):** 집전체(bottom, φ=1 V)서 top(φ=0 V)로 전자흐름.
  Ohm 법칙상 **전위구배 ∝ 전류밀도**. ★ **MMM = 전위구배 일정(균일 도전경로)**. **HML·LMH = 큰
  전위구배**(CBD 도전경로 제한). HML은 H층이 위에 있어 **아래 ML로의 전하전달은 막히지 않음**(활성화의
  ~2/3 확보). LMH는 H층이 아래(집전체)에 있어 **전자가 위로 못 올라감 → 전 전극 활성화 저해**(LMH
  저용량의 직접원인).
- **(d–f) 전류밀도 3D맵(Fig 6d–f, ×10³ A/m², 0–300):** **MMM = 균일 전류분포**; HML·LMH = 불균일
  (바인더과잉 층 주변 전류집중/공백). → **국소 바인더과잉 = 전류 불균일 = 활성화 불균일**.
- ★ **시뮬↔실험 일치:** digital-twin 전위/전류 불균일 순서(LMH·HML 큰 구배 vs MMM 균일) = 실험
  계면저항(Fig 4a)·rate(Fig 5c) 순서와 일치 → **"바인더 분포 → CBD 전자전도 → 전극 활성화"** 인과
  폐회로 검증.

### 4.6 결론 (§4)
- 통념("균일 바인더 = 좋다")을 넘어 **바인더 분포의 다양한 패턴을 정량분석** → **국소 바인더과잉(특히
  집전체 근처=LMH)이 전극 활성화를 어떻게 저해하는지** 규명. **균일(MMM)이 최적**. + **SAICAS 표면
  접착강도 + 표면 EDX = secondary-particle 활물질 전극의 신뢰성 있는 바인더 분포 분석법**(기존 단면
  EDX 한계 보완). + **digital-twin이 분포→전자흐름 인과를 시각화**. ⇒ **고에너지·장수명 LIB의 최적
  바인더 분포 설계 플랫폼**.
- ⚠ 저자 caveat: 본 전극은 **lab-scale 중로딩(3.5 mAh/cm²)** → 분포 차이가 미묘; **상용 고로딩·후막·
  고속 R2R에서는 분포 효과가 더 커질 것**(향후). 다양한 활물질·건식공정 확장 시 차이 증폭 예상.

---

## 5. 그림 한 장씩 — 무엇을 보이고 우리가 쓸 것

### 본문 Figures
- **Fig 1 (p.2):** (상) 다층전극 제작 개요(층별 건조 → top/middle/bottom). (중) **4모델 조성도**
  (Ref 93:3:4 단층 / HML 93:1:6→93:3:4→93:5:2 / MMM 균일 / LMH 93:5:2→93:3:4→93:1:6, 각 30 µm,
  총 90 µm, Al foil). (하) 분석 흐름(SAICAS 접착강도 · 표면 EDX · 바인더 분포 프로파일 → 전기화학 +
  **digital-twin 시뮬**). → ★ **z-분포 설계 + 분석 워크플로 1장 요약**(우리 Phase 5 + E3 맥락).
- **Fig 2 (p.4):** 건조온도 단층연구 — (a) **깊이별 접착강도**(80/120/160/200 °C; 온도↑→표면집중),
  (b) Nyquist, (c) 사이클, (d) **PVDF·CBD 결정성 vs 건조온도**(48→40 % / 34→30 %). → **"온도로
  분포제어는 결정성·접착을 동시 교란"**(우리엔 직접 hook 약함, 방법론 정당화).
- **Fig 3 (p.5):** ★ **(a) 표면 EDX F-원자비 깊이프로파일** + **(b) SAICAS 접착강도 깊이프로파일**
  (i Ref / ii HML / iii MMM / iv LMH). MMM 평탄, HML 감소, LMH 증가 — **F양↔접착강도 강한 상관**.
  → ★ **바인더 z-분포의 정량 + 2-방법 교차검증**(우리 binder-z 합성 타깃 + 측정법 reference).
- **Fig 4 (p.6):** (a) **계면 전자저항 막대**(LMH ~1600 폭증 ≫ MMM·HML·Ref), (b) **full-cell
  Nyquist**(LMH 거대 반원=최대 저항). → ★ **바인더 분포 → 전자저항 매핑**(E3 `--coh` 타깃).
- **Fig 5 (p.7):** half/full-cell 전기화학 — (a) formation(유사), (b) 0.2C(LMH 과전압), (c) **rate
  0.2–6C**(고율 MMM>Ref>HML≫LMH), (d) **250cyc**(MMM>Ref>HML≫LMH). → ★ **균일이 최적 + LMH 최악**
  성능 증거.
- **Fig 6 (p.8):** ★ **digital-twin 전자흐름** — (a) CBD/전극 유효 전자전도도, (b) 전위평가 모식
  (CC bottom φ=1 → top φ=0), (c) **전극 유효 전자전도 막대(HML 6.94 / MMM 2.46 / LMH 3.02 S/m)**,
  (d–f) **HML/MMM/LMH 전류밀도 3D맵**(MMM 균일, 이질구조 불균일). → ★ **분포→전자전도→전위/전류 인과
  시뮬**(positioning: GeoDict 전자전도-only).

### SI Figures (S1–S11) + Table S1–S2
- **Fig S1:** 다층전극 단계별 제작 + 전체 분석공정.
- **Fig S2:** CBD 필름(도전재+바인더, 건조조건별) **DSC** + 결정성.
- **Fig S3:** 4모델 **단면 SEM + EDX F-매핑**(a Ref / b HML / c MMM / d LMH; i SEM, ii F맵).
- **Fig S4:** 기존 단면 EDX(좁은 라인) vs **SAICAS 표면 EDX**(넓은 면) 모식 — 표면 EDX 신뢰도↑ 근거.
- **Fig S5:** Ref 전극 **비캘린더 vs 캘린더** SAICAS 후 표면 SEM(캘린더가 secondary-particle 파괴).
- **Fig S6:** 비캘린더 모델전극 **단면 SEM + pore 매핑**(i–iv) + **(b) 깊이별 porosity 분포** + (c)
  porosity 표준편차. ★ **porosity 34–37 vol%(모델) / 39 vol%(Ref, 표면쪽↑)**, Ref **porosity 표준편차
  3.1**(깊이방향), pore 종횡비 1.4–2.1. → 바인더 분포가 porosity 분포에도 영향(이 논문의 부차결과).
- **Fig S7:** NCM622/graphite full-cell **1C/1C 전압곡선**(LMH 현저 저용량).
- **Fig S8:** **0.2C/0.2C 사이클**(1C와 동일 추세).
- **Fig S9:** ★ **다층 모델전극 생성 모식**(GeoDict) — (a) NCM skeleton에 multilayer CBD 배치 +
  carbon:binder 비율 조정 → (b) L / (c) M / (d) H 모델구조 + (e) **각 CBD 유효 전자전도도 계산**.
- **Fig S10:** ★ **digital-twin 최종 (a) HML (b) MMM (c) LMH 복합전극**(CBD를 유효 전자전도도 반영해
  stochastic 배치). → 우리 Phase 5 z-band 합성과 직접대응(구조 IN은 측정/설계).
- **Fig S11:** HML/MMM/LMH **전위변화**(CC bottom 1 V → top 0 V; 전위구배 = 층별 저항률 × Ohm).
- **Table S1:** CBD 시뮬 파라미터(300×300×400 nm³, voxel 1 nm, PVDF/carbon 입경 20 nm, σ PVDF 0 /
  carbon 18 S/m, pore 30 vol%; H/M/L 조성 vol%).
- **Table S2:** 복합전극 파라미터(30×30×68.7 µm³, voxel 100 nm, NCM 입경 10 µm, true density NCM
  4.7/PVDF 1.6/carbon 1.78 g/cm³, NCM σ 4.5 S/m, 층조성 wt%).

---

## 6. 기술 미니용어집 (우리 맥락)

- **다층 모델전극(multilayer model electrode):** 바인더 함량이 다른 층을 의도적으로 적층(top/mid/bottom).
  **z-방향 바인더 분포를 직접 제어하는 실험 플랫폼** — #286의 porosity-구배 버전(거기선 자발형성, 여기선
  층캐스팅으로 강제).
- **HML / MMM / LMH:** 위→아래 바인더 high/middle/low 순서. **HML=top과잉(아래로 감소), LMH=bottom(집전체)
  과잉(위로 증가), MMM=균일**. (Ref=단층 균일.)
- **CBD(carbon-binder domain):** 도전재(carbon black)+바인더(PVDF)가 만드는 **나노다공 매트릭스**.
  유효 전자전도가 **carbon:binder 비율에 비선형 민감**(H≈0, L=375 S/m). 우리 `additives.py` CBD 상에 대응.
- **바인더 국소과잉/부재:** 과잉 → **전자저항↑ + 전해질 차단/성분탈리**; 부재 → **기계붕괴/박리**. 둘 다
  나빠 → 균일이 최적(이 논문의 핵심 매핑). 우리 MPM `--coh`(binder cohesion=결합력) + `additives.py`
  σ=0 차단의 분포 효과.
- **SAICAS:** 마이크로블레이드로 깊이별 절삭 → **접착(adhesion)·응집(cohesion) 강도** 정량. **표면 절삭
  후 EDX**로 그 깊이 바인더(F)양 측정 → 분포 프로파일. 우리 `--coh` 캘리브 + binder 분포 측정법 대응.
- **계면 vs bulk 전자저항:** 전극저항계가 **CC↔전극 계면**과 **전극 내부 bulk**를 분리 측정. **집전체
  근처 바인더가 계면저항을 지배**(LMH 폭증). 우리 σ_electronic(AM 접촉망)의 계면 항 대응(단 우리는 SE/AM).
- **Digital-twin(GeoDict ConductoDict):** voxel 구조에 ∇·(σ∇φ)=0 → 유효 전자전도 + 전위/전류분포.
  **구조는 GrainGeo로 설계해 넣어줌**(top-down/reconstruction; 우리 DEM 예측=bottom-up과 대비).
- **PTFE 탈불소화:** (이 논문엔 없음 — PVDF 사용. #286이 PTFE/탈불소화. 혼동 금지.)

---

## ★ 7. 비교 vs 우리 DEM+MPM (frame [1]–[5])

⚠ **대전제(맨 먼저):** 이 논문은 **NCM622 양극 + 액체전해질(1.15 M LiPF₆) + PVDF 일반 LIB**다 — 우리
**LPSCl sulfide ASSB(고체전해질, 무전해질 contact-network)**가 **아니다**. 따라서:
- **절대 transport·용량·저항 값은 전이 불가.** 그들 σ_e(전극 6.94/2.46/3.02 S/m)는 **CBD 나노매트릭스
  연속체** 전도이고, 우리 σ_electronic은 **AM 입자 접촉망**의 Kirchhoff/Holm 전도다. 그들 계면저항은
  **전해질-매개 + CBD** 물리 — 우리 SE-network와 다름. 용량·rate는 흑연/NCM622/액체 셀.
- 가져올 것은 **(a) z-분포 설계개념(binder-z) — #286 porosity-z의 짝, (b) 바인더 분포→접착·전자전도
  매핑(E3 `--coh` 타깃), (c) digital-twin positioning** — **수치 앵커가 아니다**. (LPSCl 수치 앵커는
  `docs/lit_bazzoun2026_dem_fem_rnm.md` + #271 `docs/lit_hong2026_sulfide_cathode_binder_digitaltwin.md`.)

### (a) Phase 5 z-layer — ★ 가장 강한 연결: BINDER-z (=#286 porosity-z의 짝)
- **그들:** **바인더 함량을 z방향 3층(H/M/L)으로 제어** → SAICAS·EDX로 두께방향 바인더 프로파일 정량
  (Fig 3) + digital-twin으로 **층별 CBD 전자전도 → 전극 전위/전류** 시뮬(Fig 6, Fig S10).
- **#286(Yoo):** **porosity를 z방향으로 구배**(top porous, bottom dense) → 토모로 두께방향 porosity
  프로파일. → **두 논문이 z방향 분포의 두 자유도(porosity vs binder)를 각각 제어**.
- **우리:** Phase 5 = layered composite cathode(z-stacking, smooth interface). `extract_2d_microstructure.py`
  는 이미 **z-band stratified placement(K=8 bands, line ~668)** + tortuosity-driven pore elongation 보유.
  현재 z-band는 **균일 porosity·균일 조성** 가정.
- ★ **ACTION (두 논문 결합):**
  1) **#286 → z-band별 다른 *porosity*** 합성(top 다공·아래 치밀).
  2) **이 논문 → z-band별 다른 *바인더/CBD 함량*** 합성(carbon:binder 비율을 band마다). → 우리 합성
     입력에 **"바인더(z) 프로파일"** 축을 추가하고, **층별 CBD 전자전도(우리 voxel σ_e) + 계면저항**을
     출력해 **HML/MMM/LMH 형태의 전위/전류 불균일**을 재현. → **Phase 5 = porosity-z + binder-z 동시
     graded 설계**(이 논문 + #286이 양 축의 published 실증).
  - ⚠ **소재차이 — 최적 분포 방향이 반대:** #286(흑연/액체)은 **구배가 최적**(porosity-z↑ → tortuosity↓
    → 급속충전↑); 이 논문(NCM622/액체)은 **균일(MMM)이 최적**(국소 바인더과잉이 전자/전해질 차단).
    ⇒ **"z-분포가 설계 자유도"라는 메타-교훈은 둘 다 같지만, 최적값은 소재·물리·축마다 다름** → 우리
    Phase 5는 **균일 vs 구배를 둘 다 합성·비교**할 수 있어야 함(한 방향 고정 금지). ASSB에서의 최적
    binder-z는 우리가 DEM+MPM으로 따로 풀 문제(흑연/NCM 흉내 금지).

### (b) 바인더 분포 → 접착·전자전도 매핑 = E3 `--coh` 레버 (cross-ref #271 + #264)
- **그들:** **바인더 국소과잉 → 전자저항↑(CBD 도전망 끊김, H≈0 S/m) + 전해질 차단/성분탈리**;
  **국소부재 → 기계붕괴/박리**(Intro 참고문헌 16,17). SAICAS로 **접착강도가 바인더(F)양에 비례** 정량.
- **우리(audit E3, `docs/stage2_model_audit_vs_literature.md` #5/E3):** MPM `--coh`(binder cohesion)는
  binder가 **결합력을 부여**해 void-fill·무결성에 기여하는 레버. 현재 우리 `additives.py`의 binder/PTFE
  상은 **σ=0 차단 + 기계/부피**만 — **분포 의존성(한 곳 과잉=저항↑+차단)**은 미반영.
- ★ **수렴하는 3개 입력원(E3 보강):**
  - **이 논문:** "바인더 국소과잉→전자저항↑+전해질차단 / 부재→박리" + **접착강도↔바인더양 정량**(SAICAS).
  - **#271(Hong, LPSCl ASSB):** PTFE confined fibril = **최소 coverage → void↓·σ_ionic 유지**; NBR
    광범위 coverage = **Li⁺ 차단 + void 성장**(바인더 *분포/coverage*가 dominant).
  - **#264(Park, LPSCl ASSB):** cross-link로 **modulus↑ → 전극 무결성↑**("가교가 접착보다 결정적").
  - ⇒ **세 논문이 "바인더의 기계물성·공간분포가 전극 무결성·수송을 지배"로 수렴** → E3 `--coh`를
    **(i) cohesion 값 + (ii) 공간분포(국소과잉 패널티: 저항↑·차단↑ / 부재 패널티: 무결성↓)** 두 축으로
    확장할 강한 근거. 이 논문은 그중 **"분포→전자전도/접착 정량 매핑"**을 제공(나머지 둘은 ASSB σ/void).
- ⚠ **비전이:** PVDF(액체 LIB)·계면저항(전해질-매개)·NCM622 = 우리 LPSCl SE-network와 다른 물리 →
  **매핑의 *방향·구조*(과잉=차단/부재=붕괴)만 이식, 절대 σ/저항값은 아님**.

### (c) digital-twin positioning — GeoDict(전자전도-only), top-down
- **그들:** **GeoDict2023 GrainGeo(NCM 구) + stochastic CBD + ConductoDict(유효 σ_e)** → 전위/전류분포.
  구조는 **설계해 넣음**(GrainGeo로 구형 생성). **이온/전기화학 풀모델 없음 — 전자전도만**(#286의
  BESTmicro 3D 전기화학과 다른, *더 가벼운* digital-twin).
- **우리:** `voxel_conductivity.py`(voxel σ_e/σ_ionic FV)가 ConductoDict에 상응(무료 복제) + DEM이
  **구조를 *예측***(GeoDict은 구조를 줘야 함, `docs/positioning_vs_geodict.md`). 이 논문은 GeoDict 논문
  목록(#266/#271/#281/#284/#286)에 **2024 선행작 1개 추가** → positioning 서사 강화(top-down/reconstruction
  vs 우리 bottom-up/formation, Kim 2024 ACS EL taxonomy).
- ★ **이식 포인트:** 그들 **"층별 CBD 전자전도 → 전극 전위/전류 불균일맵"**(Fig 6d–f)은 우리
  `voxel_conductivity` + `viz_mpm_continuum` 출력에 **z-band별 σ_e + 전류밀도 localization 맵**으로
  추가 가능(우리 StageE coverage/force-chain 대응 시각지표 — #285와 동일 이식 후보). 단 **우리 DEM은
  구조를 예측**하므로 그들보다 입력단 상향.

### (d) porosity 분포 부차결과 (SI Fig S6)
- **그들:** 비캘린더 모델전극 **porosity 34–37 vol%**(Ref 39, 표면쪽↑), Ref **깊이방향 porosity 표준편차
  3.1**, pore 종횡비 1.4–2.1. → 바인더 분포가 **porosity 분포에도 영향**(부차적; #286만큼 구배 강조는 아님).
- **우리:** porosity(z) 프로파일은 #286이 main, 이 논문은 보조. 그래도 **"바인더 분포 ↔ porosity 분포
  상호작용"** = 우리 Phase 5에서 **binder-z와 porosity-z가 독립이 아님**을 시사(MPM 압축 시 binder
  cohesion이 local densification에 영향 → coupled). → binder-z·porosity-z를 **coupled하게** 합성 고려.

### (e) frame[5] 분업 재확인 + 우리 우위
- 그들은 **고정 미세구조(GeoDict GrainGeo로 설계 IN) + 연속체 전자전도 시뮬 + 실험 SAICAS/EIS**.
  **입자스케일 압축역학 예측 없음**(구조를 측정/설계로 줌), **이온/열 σ triad 없음**(전자만), **소성
  morphology·fracture 없음**. → **출력단(검증·전자전도 시뮬) 도구**.
- 우리 DEM+MPM은 **압력·조성·입경·첨가제 → 미세구조 예측(입력단) + 접촉 σ triad(ionic/e/thermal) +
  Stage-E 소성접촉 + fracture(Auerbach) + MPM 소성 morphology/void-fill**. ⇒ **이상 워크플로 = 우리가
  binder-z/porosity-z 미세구조를 생성/예측 → (그들식) GeoDict/voxel 유효 σ_e + 전위/전류 검증 → (#286식)
  3D 전기화학으로 분극 닫기.** 이 논문은 우리 파이프라인의 **binder-z 설계 + 전자전도 검증 청사진**이지
  입력단 경쟁자가 아니다.

### 비교 요약표
| 축 | Bak 2024 (NCM622/액체) | 우리 (LPSCl ASSB) | 이식/교훈 |
|---|---|---|---|
| 소재 | NCM622 + 액체전해질 + PVDF | LPSCl SE + NMC811 | ⚠ 절대값 전이불가 |
| z-분포 | **binder-z** 3층(HML/MMM/LMH) 강제 | Phase 5 z-band(미실증) | ★ binder-z 축 추가(#286=porosity-z의 짝) |
| 최적분포 | **균일(MMM)** 최적(국소과잉 차단) | (ASSB는 우리가 풀 문제) | ⚠ 최적방향 소재의존(#286은 구배 최적) |
| 바인더효과 | 과잉→전자저항↑+전해질차단 / 부재→박리 | `--coh` cohesion(분포 미반영) | ★ E3 `--coh` 분포축 보강(+#271/#264 수렴) |
| digital-twin | GeoDict ConductoDict(전자-only), 구조 IN | voxel FV + DEM 구조예측 | positioning(top-down vs bottom-up) |
| 전기화학 | rate 0.2–6C·250cyc 실측 | Phase 4(PyBaMM 예정) | 흑연계 reference(흡수 주의) |
| 우리 고유 | (없음) | DEM 접촉 σ triad + MPM 소성 + fracture | 그들엔 입자스케일 예측 없음 |

---

## ★ 8. 우리 작업에 넣을 가장 날카로운 인사이트 3가지

1) **Phase 5에 "바인더(z) 분포" 축을 추가 — #286(porosity-z)과 짝.** 이 논문은 z방향 분포를 제어하는
   **두 번째 자유도(바인더)**를 정량화했다(#286=porosity). ⇒ 우리 z-band 합성(K=8)은 **band마다 (i)
   porosity + (ii) carbon:binder 비율**을 둘 다 받도록 확장하고, 출력에 **"바인더(z) 프로파일 +
   층별 σ_e/계면저항 + 전류 localization 맵"**을 추가. ★ **단 최적 분포 방향은 소재의존** — #286(흑연)은
   구배가, 이 논문(NCM622)은 균일이 최적 → 우리 Phase 5는 **균일·구배를 둘 다 합성·비교**(ASSB 최적
   binder-z는 우리 DEM+MPM으로 별도 도출, 흑연/NCM 흉내 금지).

2) **바인더 분포 → 접착·전자전도 매핑은 E3 `--coh`의 실험 타깃 — #271/#264와 3-입력원 수렴.**
   "국소 바인더과잉 → 전자저항↑+전해질차단(CBD 도전망 H≈0 S/m) / 부재 → 박리" + SAICAS "접착강도↔바인더양"
   정량은, 우리 MPM `--coh`를 **(i) cohesion 값 + (ii) 공간분포 패널티(과잉=차단·저항↑ / 부재=무결성↓)**
   로 확장할 근거다. #271(PTFE coverage→void↓), #264(cross-link modulus→무결성)와 합쳐 **"바인더 기계
   물성·분포가 무결성·수송을 지배"**가 세 논문에서 수렴 → E3가 단일 cohesion 스칼라를 넘어 **분포-인지
   레버**가 돼야 함을 강하게 지지(이 논문이 그중 "분포→전자/접착 정량" 담당).

3) **frame[5] + positioning 재확인 — 우리 우위 명확.** GeoDict로 **구조를 설계해 넣고 전자전도만** 푸는
   2024 선행작이 하나 더 추가됐다(top-down/reconstruction). 우리 DEM+MPM은 **압력·조성에서 binder-z
   미세구조를 *예측*(bottom-up)** 하고 **σ triad + 소성 morphology + fracture**까지 간다. ⇒ 이상
   워크플로 = **우리가 binder-z/porosity-z 미세구조 생성/예측 → 그들식 GeoDict/voxel 전자전도·전위/전류
   검증 → #286식 3D 전기화학으로 분극 닫기.** 이 논문은 **출력단(binder-z 검증) 청사진**이지 입력단
   경쟁자가 아니다.

### 보너스 실행 항목
- **`literature_yonsei_dtbl_2026.md`에 본 논문을 DTBL 항목으로 추가**(아래 완료) — 2024 CEJ, binder-z,
  #286(porosity-z) + E3 cross-link.
- **우리 z-band 합성 입력 스키마에 `binder_frac(z)` / `carbon_binder_ratio(z)` 필드 추가** 후보(Phase 5).
- ⚠ **혼동 금지:** Bak 2024(#이 논문, NCM622, **binder-z + 균일최적**)와 #286 Yoo(흑연, **porosity-z +
  구배최적**)는 **둘 다 z-분포 설계 청사진**이나 **축(바인더 vs porosity)·최적방향(균일 vs 구배)이 다름**.
  둘 다 **수치 앵커가 아니라 설계개념·방법·매핑** 공급원(LPSCl σ 앵커는 Bazzoun/#271).
