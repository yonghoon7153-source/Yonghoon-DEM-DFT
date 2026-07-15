# Kim 2026 (Journal of Power Sources 686, 240471) — 디지털트윈 미세구조(GeoDict) → 유효물성 → 1D 전기화학(COMSOL)으로 A3D 공기극 수송 설계

**인용:** Suhwan Kim†, Seungwon Jung†, Seonyong Jo, Gwangmin Bae, Gayea Hyun, Nayeon Gang,
Seokwoo Jeon\*, Yong-Mook Kang\*, Yong Min Lee\*, "Microstructure-guided reactant transport
engineering in architected three-dimensional air electrodes for high-performance Li–O₂ batteries",
*Journal of Power Sources* **686** (2026) 240471, DOI 10.1016/j.jpowsour.2026.240471
(PII S0378-7753(26)…). MDB 2025 특별호("Progresses and Challenges"). 접수 2026-04-16, 수정
2026-05-09, 게재확정 2026-05-19, online 2026-05-28. © 2026 Elsevier.

**소속:** (1) Yonsei University — Dept. of Chemical & Biomolecular Engineering(Seoul 03722), (2)
Yonsei — Dept. of Battery Engineering, (3) Korea University — Dept. of Materials Science & Engineering
(Seoul 02841), (4) UC San Diego — Aiiso Yufeng Li Family Dept. of Chemical & Nano Engineering(La Jolla).
= 이용민 **Digital Twin Battery Lab (DTBL)** + 전석우(KU) + 강용묵(KU/UCSD). †Suhwan Kim,
Seungwon Jung 동등기여. 교신 jeon39@korea.ac.kr(전석우)·dake1234@korea.ac.kr(강용묵)·
yongmin@yonsei.ac.kr(이용민). **이해상충 없음.** 지원: NRF(NRF-2020M3D1A1110522, NRF-2022M3H4A1A0406892311).

**소재계:** ★★ **Li–O₂ 전지(LOB)의 공기극(air electrode)** — Li metal 음극, 주변 공기 중 **O₂ 가스**가
양극 활물질(cell 안에 저장 안 함), **액체 전해질(1 M LiCF₃SO₃ in TEGDME)** 중 Li⁺, 방전생성물 **Li₂O₂**.
양극 골격은 **Ni**(architected 3D, A3D) 또는 비교용 **foam(Ni)**. ★★★ **우리 LPSCl sulfide ASSB가
**전혀** 아니다** — **수송 reactant가 O₂ 가스 + 액체 Li⁺, 방전생성물이 Li₂O₂인 금속-공기 전지**.
이 그룹(연세대 DTBL)의 **#281** 논문 — `docs/literature_yonsei_dtbl_2026.md` 항목 갱신본.

DB 동반 파일: `docs/data/densification_porosity_db.csv` 등 수치 DB에는 추가하지 않음(Li-O₂ → σ/porosity
**절대앵커 아님**. σ/porosity 절대앵커는 **Bazzoun(LPSCl)·Varkey(halide)·Minnmann(LPSCl cold-press)·
#266(bimodal ASSB)**이 담당). 이 논문의 모든 수치는 본 MD 표에 정리. SI(Fig S1–S10 + Table S1–S3 +
지배방정식)는 디제스트 본문에 전부 반영. SI에 동영상/머신판독불가 자료 없음.

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 왜 중요한가

**디지털트윈으로 만든 architected-3D(A3D) 공기극 미세구조를 GeoDict로 voxel화 → 유효물성(비표면적 SSA·
porosity·유효 O₂ 확산도·유효 전자/이온전도도)을 추출 → 이를 COMSOL 1D 전기화학 모델에 직접 넣어 방전
곡선을 예측**하고, **구조 파라미터(SSA/porosity/D_eff/σ_eff)를 독립적으로 변화시켜 각각이 산소수송·반응국소화·
방전용량·과전압에 미치는 영향을 분리(decouple)**한다. 결과: 단위셀 주기(BCT period)를 줄이면 **SSA↑(반응
site↑)이지만 pore가 좁아져 유효 O₂ 확산↓ → 고율에서 용량 제한**. 따라서 **SSA↑를 유지하면서 산소수송경로를
보존하는** diamond-type 단위셀 + 표면공학(electropolishing)을 설계지침으로 제안.

**우리 hook(가장 중요 — METHODOLOGY가 가치, 화학은 외래):**
이 논문은 **#286(τ/PNM 토모 정량)·#284(분산 W_adh) 이후 이 그룹의 3번째 GeoDict 활용**이며, 핵심
파이프라인 **"미세구조 → GeoDict 유효물성(ConductoDict/DiffuDict) → 1D 전기화학(COMSOL) → 셀 성능"** 은
정확히 **우리 Phase 4 청사진의 published blueprint**다:
- **(a) GeoDict ConductoDict/DiffuDict (voxel → 유효 σ / 유효 D)** = 우리 **voxel FV 솔버
  (`scripts/voxel_conductivity.py`)와 동일 접근**(둘 다 voxel 상에 ∇·(σ∇φ)=0 / Fick 정상상태를 풀어
  유효물성 추출). MatDict(SSA) = 우리 coverage/면적 후처리 대응.
- **(b) 미세구조 → 유효물성 → 1D 전기화학(COMSOL) → 방전곡선 결합** = 우리 **Phase 4 (우리 미세구조
  σ_ionic/τ → PyBaMM DFN → 셀 성능)의 결합 템플릿**. 그들의 COMSOL 1D 모델이 effective ε/τ/σ/D를 입력으로
  받는 방식이 곧 PyBaMM `{"transport efficiency":"tortuosity factor"}` + `"... conductivity [S.m-1]"`
  주입과 1:1 대응.
- **(c) "SSA/porosity/D_eff/σ_eff를 독립 변화 → 성능 귀속(decouple)"** = 우리 **predictor(design knobs →
  metrics → performance)** 의 사고 그 자체.

**⚠ CRITICAL caveat(반복):** Li-O₂ 화학은 **외래**. **모든 절대값(용량 mAh/cm², 과전압 V, O₂ 확산도,
SSA m²/m³, Li₂O₂ 막저항)은 우리 LPSCl sulfide ASSB에 전이 불가.** 가져오는 것은 **METHODOLOGY 3종(위 a/b/c)
뿐**이다 — 수치 σ/porosity 앵커는 Bazzoun/Varkey/Minnmann/#266이 담당. 아래 §8에서 "method/concept는 전이,
Li-O₂ 절대값은 비전이"를 명확히 구분.

---

## 0. 빠른 사실표 (한눈에)

| 항목 | 값 / 내용 |
|---|---|
| 전지계 | Li–O₂ (LOB), 비수계 |
| 음극 | Li metal (모델에서 경계조건으로만 — Li/전해질 계면반응) |
| 양극(공기극) 골격 | **Ni** — architected 3D(A3D, BCT 또는 diamond 단위셀) vs **foam(Ni)** 비교 |
| 활물질 reactant | **O₂ 가스**(주변 공기에서; cell 안에 저장 안 함) + 전해질 중 Li⁺ |
| 전해질 | **1 M LiCF₃SO₃ in TEGDME**(Gittleson ref[2]: σ_ion 0.58 mS/cm, t₊ 0.92, D_O₂ 4.17e-8 cm²/s) |
| 방전생성물 | **Li₂O₂**(공기극 내부표면에 **film형**으로 성장 — Hyun ref[1] 가정 → SSA·porosity 감소·기공막힘) |
| 반응 | 방전 ORR: 2Li⁺ + O₂ + 2e⁻ → Li₂O₂ (TPB=triple-phase boundary에서) |
| 구조분석 도구 | **GeoDict 2025**(Math2Market) — STL→voxel(**voxel 0.01 µm**), ProcessGeo(Repeat)·GrainGeo(Roughen Surface)·FoamGeo·**MatDict**(SSA)·**ConductoDict**(유효 σ_e/σ_ion)·**DiffuDict**(유효 D_O₂) |
| 전기화학 모델 | **COMSOL Multiphysics 6.3** — 1D, 방전(ORR)만, 'Lithium-Ion Battery'+'Transport of Diluted Species in Porous Media'+'Domain ODEs and DAEs' 결합 |
| 모델 도메인 | 3-도메인: **separator(420 µm) | air electrode(8 µm) | GDL(192 µm)** (실험비교용 GDL 추가) |
| 인가 전류밀도 | 0.01 / 0.05 / 0.10 mA/cm² |
| BCT 단위셀 시리즈 | **B600 / B500 / B400 / B300**(in-plane 주기 600/500/400/300 nm) |
| diamond 단위셀 | **D400 / D300 / D300EP**(D300EP = electropolishing 표면거칠기) |
| A3D 전극 RVE | 단위셀을 Repeat → **7.8 × 7.8 × 8.0 µm³**(또는 8×8×8 µm) |
| foam 전극 RVE | **3000 × 3000 × 120 µm³**(voxel 8 µm, FoamGeo 확률적) |

---

## 1. 배경 / 동기 (Introduction, p.1–2)

- **Li–O₂ 전지(LOB)** = 차세대 고에너지밀도 후보. Li metal 음극 + **주변 공기 중 O₂를 cathode 활물질로**
  사용(cell 안에 양극활물질 저장 불필요) → **이론 에너지밀도가 state-of-the-art Li-ion을 능가**(원리상,
  시스템 수준). 장거리 EV·대규모 ESS에 매력적[3].
- ❗ **그러나 실용화는 심하게 제약됨:** 다공성 공기극에서 **ORR(산소환원)·OER(산소발생)이 주된 동역학
  병목** → 큰 과전압·낮은 방전용량·낮은 round-trip 효율[4–7].
- 기존 해법은 주로 **촉매**(귀금속[11,12], 전이금속산화물[9], heteroatom-doped carbon[13], soluble redox
  mediator[14]) → 과전압↓·용량↑ 보고[12,15]. **그러나 촉매활성만으로는 한계** — 셀 거동이 **다공성 양극의
  미세구조에 강하게 결합**되어 있기 때문[16,17].
- ★ 공기극은 **복잡·무작위 pore network** → 비균일 **TPB(triple-phase boundary, 기체-전해질-전자전도상이
  만나는 삼상경계)**, 비균일 방전생성물 deposition, 비균일 gas·ion 수송경로[2,18–20]. 그래서 구조효과가
  **경험적으로만(trial-and-error로)** 다뤄져 왔고, **특정 구조 파라미터가 성능을 어떻게 결정하는지는 체계적
  이해 부족.**
- ★ 본 연구의 platform 선택: **architected 3D(A3D) 공기극** — **주기적으로 반복되는 단위셀 기하**(정의된
  length scale·connectivity)[25,26] → 구조 파라미터를 **high fidelity로 정량·체계적 변화** 가능 → 모델링↔
  실험 직접비교가 가능한 **well-defined 모델 platform**. (무작위 구조는 디커플 불가가 본질적 난점.)
- **본 연구(명시):** **3D 디지털트윈 구조분석 + 1D 전기화학 모델 결합** → A3D 공기극 구조가 LOB 성능에
  미치는 영향 분석. **핵심 구조 파라미터(SSA·porosity·유효 D_O₂)를 독립 변화시켜 산소수송·반응동역학에
  미치는 영향 규명** → 그 결과로 **BCT 기반 A3D 구조를 상세 분석·성능 예측** → **고성능 LOB용 합리적 구조
  설계지침(diamond 단위셀 + 표면공학)** 제안.
- **선행연구 앵커:** Hyun et al.[25](이 논문 SI ref[1], Adv. Funct. Mater. 33 (2023) 2303059) = **3D-패턴
  Cu 전극으로 LOB의 TPB(Li⁺/e⁻/O₂ 상경계) 의의 규명** → 본 논문이 이를 디지털트윈+1D 모델로 확장(같은
  저자군). [25]가 본 논문 1D 모델의 Li₂O₂ film 성장 가정의 근거.

**약어 정리:** A3D = architected 3D(주기적 단위셀로 구성된 3차원 설계 전극). BCT = body-centered
tetragonal(체심정방, 단위셀 격자형). LOB = lithium-oxygen battery. ORR/OER = 산소환원/발생반응.
TPB = triple-phase boundary(기체-전해질-전자상 삼상경계 — 반응이 일어나는 곳). SSA = specific surface
area(비표면적, 단위 전극부피당 내부계면적 m²/m³). DOD = depth of discharge(방전심도). GDL = gas
diffusion layer(기체확산층 — 실험과 비교 위해 모델에 추가). RVE = representative volume element.
PnP = proximity-field nanopatterning(근접장 나노패터닝, A3D 제작공정 — STL이 광강도분포에서 유래).
EP = electropolishing(전해연마, D300EP의 표면거칠기 유래 공정).

---

## 2. 방법 IN DETAIL — 디지털트윈(GeoDict) + 1D 전기화학(COMSOL)

### 2.1 디지털트윈 구조분석 — GeoDict 2025 파이프라인 (§2.1 + SI Methods)

★ **이 절이 우리 voxel FV / Phase 4와 직결되는 METHODOLOGY 핵심.**

**(1) 단위셀 기하 생성 (CAD):**
- **BCT 단위셀**: 컴퓨터지원설계(CAD) 환경에서 **리소그래피 공정 파라미터 + 기존 A3D 설계**를 고려해 생성.
  (A3D는 **PnP=proximity-field nanopatterning**으로 제작 → 실제 단위셀 형상은 회절·간섭이 만드는 광강도
  분포에서 유래 → "process-relevant" 형상. self-similar가 아님.)
- **diamond-type 단위셀**: 동일 방식으로 별도 생성.
- ★ **표면거칠기(diamond, electropolishing 후)**: GeoDict **GrainGeo 모듈의 'Roughen Surface' 함수**로
  반영 → D300EP.

**(2) STL → voxel 변환 (GeoDict 2025, Math2Market):**
- 생성된 단위셀 기하를 **STL(stereolithography) 포맷으로 export** → **GeoDict 2025(finite-volume 기반
  소프트웨어)** 로 import → **voxel 기반 표현으로 변환**.
- ★ **voxel 길이 = 0.01 µm(10 nm)** — "충분한 구조정확도 + 합리적 계산비용" 타협으로 선택. (cf. 우리
  voxel FV는 n_vox=192/256으로 17.8µm/256≈0.07µm/cell — 그들은 8µm 도메인에 10nm voxel = 800 voxel/축
  → 훨씬 고해상.)

**(3) A3D 전극 RVE 조립 (ProcessGeo 'Repeat'):**
- voxel화된 단위셀을 **in-plane(면내) + through-plane(두께방향)으로 주기복제** → **약 8 µm × 8 µm × 8 µm
  도메인**(Table S1: 전극 7.8 × 7.8 × 8.0 µm³)의 A3D 전극 구조 생성. GeoDict **ProcessGeo 'Repeat' 함수.**

**(4) foam 전극 RVE (비교군, FoamGeo):**
- 대조군으로 **foam 전극**을 **GeoDict FoamGeo 모듈에서 확률적(stochastic)으로** 생성 → **3000 µm × 3000 µm
  × 120 µm 도메인**, **voxel 길이 8 µm**. (= 무작위 다공 양극, LOB에서 흔히 쓰는 conventional 구조.)

**(5) 유효물성 추출 — 3개 GeoDict 모듈 ★ (= 우리 voxel FV와 동일 원리):**
| GeoDict 모듈 | 추출 물성 | 우리 대응 |
|---|---|---|
| **MatDict** | **SSA**(specific surface area, 내부계면적/부피) | 우리 coverage/면적 후처리(Tabor·B3 coverage, A_total) |
| **ConductoDict** | **유효 전자전도도 σ_e,eff + 유효 이온전도도 σ_ion,eff** — voxel 상 양단에 **일정 전위차** 인가, ∇·(σ∇φ)=0 풀이 | ★ **우리 `voxel_conductivity.py` 그 자체**(TOP 1V/BOTTOM 0V, ∇·(σ∇φ)=0, harmonic-mean face conductance) |
| **DiffuDict** | **유효 O₂ 확산도 D_O₂,eff** — voxel 상 양단에 **일정 농도차** 인가, 정상상태 Fick 풀이 | 우리에겐 직접 대응 없음(우리는 transport σ만; D_eff는 동일 voxel FV 프레임에서 확산계수로 풀면 됨 — 이식 후보) |

- ConductoDict/DiffuDict 모두 **"constant potential/concentration difference across the domain"** 조건 →
  effective property = 균질화된 물성(우리 σ_eff = I·L/(A·ΔV)와 동일한 효과물성 정의).

### 2.2 1D 전기화학 LOB 모델 — COMSOL Multiphysics 6.3 (§2.2 + SI Methods + Fig S1)

★ **이 절이 우리 Phase 4(PyBaMM DFN) 결합 템플릿.**

**(1) 소프트웨어·도메인:**
- **COMSOL Multiphysics 6.3**(finite-element), **방전(ORR) 거동만** 시뮬. (충전/OER은 미포함 — 이유:
  Li₂O₂ 산화는 단순히 방전의 역으로 기술 못 함; morphology·결정성·전자접촉·촉매/mediator 활성·전해질/탄소
  부반응 등 추가 물리·파라미터 필요[2,27]. → 방전기반 미세구조-성능 분석에 한정.)
- 모델 도메인 = **2영역(separator + air electrode)** 기본 + 실험비교용 **GDL 추가 → 3영역
  (separator | air electrode | GDL)**(Fig S1). **Li metal은 경계로만** 표현(Li/전해질 계면반응만 고려).
- A3D 미세구조는 **디지털트윈에서 얻은 구조 파라미터(porosity, SSA, 유효 σ, 유효 D)로 표현** → ★ 이것이
  바로 "미세구조 → effective param → 1D 모델"의 결합점.

**(2) 결합 모듈 3종:**
전해질로 채워진 다공영역에서 **Li⁺·전자·O₂의 수송·반응**을 다음 COMSOL 모듈 결합으로 모델:
- **'Lithium-Ion Battery'**(전해질 Li⁺ 전하/물질, 고체상 전하),
- **'Transport of Diluted Species in Porous Media'**(용존 O₂ 확산),
- **'Domain ODEs and DAEs'**(Li₂O₂ 부피분율 진화 ODE).

**(3) 지배방정식 (Fig S1, full set) — ★ 그대로 옮김:**
4개 보존식(공기극 / GDL 각 도메인):

- **물질 보존 (Li⁺, 전해질):**
  ```
  ε_e ∂c_Li⁺/∂t + ∇·( −D_eff ∇c_Li⁺ + (t₊/F)( −κ_eff ∇φ_e + (2RT κ_eff /F)(1−t₊)(1 + ∂ln f / ∂ln c_Li⁺) ∇ln c_Li⁺ ) ) = 0
  ```
  (= 농축용액이론. **D_eff·κ_eff = effective(미세구조에서)**. t₊ = 전이수, f = 활동계수.)
- **물질 보존 (O₂, 용존):**
  ```
  ε_p ∂c_O₂/∂t + ∇·( −D_O₂,eff ∇c_O₂ ) = 0
  ```
  (= effective O₂ 확산도가 곧 디지털트윈 D_O₂,eff.)
- **전하 보존 (전해질):**
  ```
  ∇·i_e = −∇·( κ_eff ∇φ_e ) + ∇·( (2RT κ_eff /F)(1−t₊)(1 + ∂ln f /∂ln c_Li⁺) ∇ln c_Li⁺ ) = 0
  ```
- **전하 보존 (고체상, GDL/전자전도):**
  ```
  ∇·i_s = −∇·( σ_eff ∇φ_s ) = 0
  ```
  (= effective 전자전도도가 곧 디지털트윈 σ_e,eff.)
- **계면 반응 (국소 산소환원 전류밀도, Butler-Volmer형):**
  ```
  i_loc = i_0,ref (c_Li/c_Li,ref)^α_a { exp(0.5 F η /RT) − exp(−0.5 F η /RT) }
  i_loc = n F { k_a c_Li,O₂ exp(0.5 n F η /RT) − k_c (c_Li⁺)² c_O₂ exp(−0.5 n F η /RT) }
  ```
  (공기극 i_loc은 c_Li,O₂·c_O₂ 의존 환원반응; GDL i_loc도 명시.)

**(4) Li₂O₂ film 성장 + 기공막힘 (핵심 coupling) — SI ★:**
- **가정(Hyun et al. ref[1] 근거):** A3D 공기극에서 Li₂O₂는 **내부표면에 resistive film(저항막)형으로
  성장**. 이 가정 하에 **Li₂O₂ 부피분율 ε_Li₂O₂ 진화:**
  ```
  ∂ε_Li₂O₂ /∂t = (1/2F) (MW_Li₂O₂ / ρ_Li₂O₂) · a · i_loc
  ```
  (F=Faraday, MW/ρ=Li₂O₂ 분자량/밀도, **a = SSA(단위 전극부피당 계면적)**, i_loc=국소전류밀도.)
- ★ **ε_Li₂O₂ 증가 → 방전 중 SSA·porosity 감소**(=반응site·기공이 생성물로 막힘). 이 **양의 피드백**
  (Li₂O₂↑ → 국소 porosity↓·passivation↑ → 산소수송↓ → 국소반응 가속 → premature end-of-discharge)이
  방전종료를 지배(§3.2 핵심 메커니즘).

**(5) 풀이조건·BC:**
- **정전류(galvanostatic) 방전**: 공기극 경계에 **일정 전류밀도** 인가(0.01/0.05/0.10 mA/cm²).
- **O₂**: 공기극(또는 GDL) gas side에 **고정 O₂ 분압(외부)**, separator side는 **no-flux**.
- 디지털트윈/구조분석에서 **얻지 못한** 동역학·수송 파라미터(반응속도상수, 등)는 **문헌값 + BCT-A3D 실험
  방전곡선에 fit**으로 결정 → 그 다음 **동일 파라미터셋 고정**하고 **디지털트윈 구조 파라미터(BCT·diamond)만
  변화**시켜 구조-성능 관계 예측(= 깨끗한 구조변수 isolation).

**(6) 핵심 입력 파라미터 (Table S2) — 1D 모델 전체 셋업:**
| 파라미터 | 값 |
|---|---|
| 공기극 두께 | 8 µm |
| GDL 두께 | 192 µm |
| separator 두께 | 420 µm |
| 공기극 porosity | 45.6 % |
| GDL porosity (ε_GDL) | 83.2 % |
| separator porosity | 87.0 % |
| 공기극 SSA | 1.02×10⁷ m²/m³ |
| GDL SSA | 2.41×10⁷ m²/m³ |
| 공기극 유효 σ_e | 2.51×10⁵ S/cm |
| GDL 유효 σ_e | 2.0×10⁰ S/cm |
| 전해질 이온전도도 κ_EL | 5.8×10⁻⁴ S/cm [ref 2] |
| 공기극 유효 σ_ion | 1.28×10⁻⁴ S/cm |
| GDL 유효 σ_ion | κ_EL × ε_GDL^1.5 (**Bruggeman**) |
| 전이수 t₊ | 0.92 [ref 2] |
| 전해질 D_O₂ | 4.17×10⁻⁸ cm²/s [ref 2] |
| 공기극 유효 D_O₂ | 0.92×10⁻⁸ cm²/s |
| GDL 유효 D_O₂ | D_O₂ × ε_GDL^1.5 (**Bruggeman**) |
| 외부 gas O₂ 농도 | 9.46 mol/m³ |
| 전해질 O₂ 용해도 | 0.4 |
| **Li₂O₂ film 저항** | 50 Ω·m² [ref 3] |
| 초기 전해질 염농도 | 1000 mol/m³ |
| 인가 전류밀도 | 0.01 / 0.05 / 0.10 mA/cm² |

→ ★ **주목:** 공기극의 유효 σ/D는 **디지털트윈에서 직접 얻은 값**(σ_e 2.51e5, σ_ion 1.28e-4, D_O₂ 0.92e-8)
이지만, **GDL의 유효물성은 Bruggeman ε^1.5로 근사**(GDL은 디지털트윈 안 함). 즉 같은 모델 안에서 **핵심
도메인(공기극)은 측정 효과물성, 보조 도메인(GDL)은 Bruggeman 가정**을 혼용 — 우리 Phase 4 전략(핵심
전극은 우리 voxel τ/σ 주입, 나머지는 기본값)과 정확히 같은 사고.

---

## 3. 섹션별 결과 — 모든 수치 (Results & Discussion, §3, p.3–8)

### 3.1 구조분석 + 1D 모델 검증 (Fig 1, Table S1) — A3D vs foam

★ 핵심 발견 1: **디지털트윈이 A3D의 구조·수송특성을 신뢰성 있게 재현하고, A3D가 foam보다 우월함을 명시.**

**디지털트윈 vs 실측 구조 (Fig 1c,e + Table S1):**
| 물성 | A3D 전극 | foam 전극 | 비고 |
|---|---|---|---|
| **유효 σ_e (sim)** | **2.51×10⁵ S/cm** | **0.40×10⁴ S/cm** | A3D가 foam의 **6배 이상** (Fig 1c, sim↔exp 양호 일치) |
| **유효 σ_e (exp)** | (sim과 good agreement) | (sim과 good agreement) | — |
| **SSA (sim)** | **1.02×10⁷ m²/m³** | **0.88×10⁵ m²/m³** | A3D가 foam의 **~116배** (Fig 1e, 미세패턴 큰 내부표면) |
| porosity | 45.6 % | 80.2 % | (Table S1) |
| 단위셀/도메인 | unit cell 0.6×0.6×1.86, 전극 7.8×7.8×8.0 µm³ | 3000×3000×120 µm³ | — |
| intrinsic σ_e (Cu) | 6.04×10⁵ S/cm | — | (Table S1; GeoDict Material DB) |
| intrinsic σ_ion | 0.58×10⁻³ S/cm | — | 1 M LiCF₃SO₃/TEGDME[2] |
| 유효 σ_ion | 1.28×10⁻⁴ | 3.09×10⁻⁴ | (foam이 더 높음 — porosity 80%) |
| intrinsic D_O₂ | 4.17×10⁻⁸ cm²/s | — | [2] |
| 유효 D_O₂ | 0.92×10⁻⁸ | 2.22×10⁻⁸ | (foam이 더 높음 — porosity 80%) |

- ★ **A3D의 유효 σ_e가 foam의 6배↑** = 주기적 정렬 구조의 **연속·잘 연결된 전자전도망**(Fig 1d: A3D는
  높고 균일한 electron density, foam은 낮고 heterogeneous + irregular pore·고체상 연결성 빈약).
- ★ **A3D SSA = foam의 ~116배**(1.02e7 vs 0.88e5) = 미세패턴이 만드는 큰 내부표면.
- ⇒ **디지털트윈이 A3D의 구조·수송특성을 신뢰성 있게 재현 + A3D가 conventional foam 대비 구조적 이점 명시.**
- 주의: foam은 porosity가 높아(80% vs 46%) **유효 σ_ion·D_O₂는 오히려 foam이 큼**(전해질 채운 pore 많음).
  A3D의 강점은 **전자전도망 연속성 + SSA**(반응site), foam의 강점은 **개방기공(이온/산소수송)** — 이미
  여기서 A3D의 trade-off(SSA↑ vs 수송경로) 씨앗이 보임.

**1D 모델 검증 (Fig 1f) — 방전곡선 vs 실측:**
- BCT-A3D + GDL을 **0.01 / 0.05 / 0.10 mA/cm²** 3전류밀도에서 시뮬한 방전곡선이 **실측과 합리적 일치**
  (Fig 1f: V vs 용량, sim=실선·exp=원). 초기 전압강하, subsequent plateau, 수송제약·Li₂O₂ 축적에 의한
  terminal 전압 decay 재현. 전류밀도에 따른 용량·과전압 의존도 재현.
- ★ **실험비교 시 carbon paper는 GDL일 뿐 아니라 전해질침투 다공탄소상**으로서 ORR·Li₂O₂ deposition에
  기여 → 측정 areal capacity는 A3D + carbon paper 합산. 모델이 이를 GDL 추가로 반영.
- ⇒ "1D 모델 + 디지털트윈 구조 파라미터 → 실제 작동조건의 A3D 방전성능을 신뢰성 있게 예측."

### 3.2 구조 파라미터 → 방전성능 (Fig 2, Fig S3, S4, S5) — ★ decouple 분석

★ 핵심 발견 2: **SSA·porosity·D_O₂를 독립 변화시켜 각각의 역할을 분리** — 전류밀도가 핵심 modulator.
방법: baseline A3D 대비 각 구조변수를 배수(SSA 0.5/1.0/2.0×, porosity 30/45/60%, D_O₂ 0.5–2.0×)로
변화시켜 **0.01·0.05 mA/cm²**에서 galvanostatic 방전 시뮬. (전자/이온전도도는 따로 Fig S5.)

**(A) SSA의 영향 (Fig 2a–c, Fig S3):**
- baseline SSA = **1×10⁷ m²/m³**. SSA↑ → 방전분극↓·용량↑(양 전류밀도). 이유: **전기화학 활성표면↑ →
  반응site↑ + 방전생성물 passivation 지연.**
- ★ **전류밀도가 SSA 민감도를 지배:**
  - **0.01 mA/cm²(저율):** SSA 의존 **약함**(colormap Fig 2b 따라 modest gradient). SSA를 절반으로 →
    areal capacity **8.4% 감소**; 2배로 → **4.9% 증가**만. 추가 SSA 증가는 ≤1% → **저율에선 용량이
    빠르게 saturate**. → 저율에선 SSA가 주로 **과전압**을 지배하고 용량은 산소수송·Li₂O₂ 표면passivation에
    상대적으로 둔감.
  - **0.05 mA/cm²(고율):** SSA 의존 **강함**(Fig 2c colormap 따라 뚜렷한 색구배). SSA 절반 → **용량 34.6%
    감소**(상당); 2배 → **37.9% 증가**; 추가 증가도 notable. → **고율에선 SSA(반응site)가 결정적** —
    수송제약+passivation이 지배하므로 반응면적이 critical.
- (Fig S3: DOD vs SSA 과전압 colormap, 0.01·0.05 mA/cm² — 저율은 거의 균일, 고율은 강한 구배.)

**(B) porosity의 영향 (Fig 2d–f, Fig S4):**
- porosity 변화는 **방전용량을 주로 지배, 과전압엔 무시할 영향**. → porosity는 **기공 이용도·Li₂O₂
  수용공간**을 좌우하지 intrinsic 반응동역학은 아님.
- **0.01 mA/cm²:** porosity↑ → 고용량영역이 **DOD 깊은 쪽으로 단조 확장**(Fig 2e colormap). baseline 대비
  porosity ±15%p 변화 → areal capacity **~30% 변화**(저율에서 용량의 강한 porosity 민감도). 이때 방전이
  전극 깊숙이 진행 → **총 pore 부피(Li₂O₂ 수용)가 달성용량 결정인자.**
- **0.05 mA/cm²:** porosity 의존 **약함**(고 DOD 영역에서 subtle 변화, Fig 2f). 고율에선 방전이 **산소수송
  제약 + 국소 passivation**으로 제약 → 가용 pore 부피를 다 못 쓰고 조기종료 → porosity 추가이득 미미.
  방전종료시 pore의 상당부분이 **전기화학적으로 inactive**하게 남음.
- ⇒ **porosity는 저율에서 용량 maximize에 critical(Li₂O₂ 저장), 고율에선 영향 미미(수송이 지배).**

**(C) 유효 D_O₂의 영향 (Fig 2g–i, Fig S4) — 비단조 ★:**
- baseline D_O₂ = **9×10⁻⁹ cm²/s**. D_O₂ 0.5–2.0× 변화.
- D_O₂를 baseline의 **절반으로 → 방전용량 뚜렷 손실 + 과전압 소폭↑** → **산소수송이 rate-limiting**(확산이
  크게 낮을 때).
- baseline·그 이상에서는 전압곡선 거의 겹침, 추가 D_O₂↑는 minor 변화(Fig 2h) → **threshold형 거동(저율):
  산소수송이 충분히 facilitate되면 그 이상은 둔감.**
- ★ **0.05 mA/cm²(고율)에서 비단조(qualitatively different) 거동(Fig 2i):**
  - 0.5→1.0× D_O₂: 성능 향상(예상대로).
  - **1.5× D_O₂: anomalous degradation(이상 열화)** — premature 전압decay·용량감소.
  - 2.0× D_O₂: 회복(2.0×에서 다시 좋아짐).
- **메커니즘(논문 해석):** 1.5× D_O₂에선 산소가 전극 깊이 침투하나 **전체 두께에 spatially uniform 반응을
  지속하기엔 산소공급 부족** → 반응이 **국소영역에 집중**(용존 O₂·가용 SSA 동시 favorable한 곳) → **국소
  Li₂O₂ 가속 → 국소 porosity·SSA 급감 → 양의 피드백(국소 Li₂O₂ 축적 ↔ 기공막힘 ↔ 산소수송제약)** →
  premature end-of-discharge. 2.0×에선 산소공급이 전극 전체에서 충분 → 국소고갈/passivation 완화 → 더 높은
  용량·낮은 분극. (Fig S4: DOD 50%에서 두께방향 O₂ 농도 + porosity 진화 — 0.5/1.0/1.5/2.0× 비교.)
- ⇒ ★ **고율에선 단순히 "확산↑=좋음"이 아니라, 산소 재분포·국소 ORR·Li₂O₂ 기공막힘의 결합효과**가 성능을
  지배(비단조). = "미세구조에 의한 산소수송 조절이 반응국소화·용량을 직접 지배"의 핵심 정량근거.

**(D) 전자/이온전도도의 영향 (Fig S5) — 무시:**
- σ_e(3.0/6.0/12.0×10⁴ S/cm), σ_ion(0.5/1.0/1.5/2.0×10⁴ S/cm 범위) 변화 → **방전곡선 변화 없음, 용량·
  과전압에 systematic variation 없음**(Fig S5a,b 곡선 겹침). ⇒ **전자/이온전도는 (현 조건에서) rate-limiting
  아님** — 성능 추세는 **산소수송 + Li₂O₂에 의한 porosity·SSA 진화**가 지배. (= A3D는 이미 σ_e/σ_ion이
  충분히 높아 병목이 아님; 병목은 O₂.)

### 3.3 BCT 단위셀 미세구조 분석 (Fig 3, Fig 4, Table S3, Fig S6, S7) — period 효과

★ 핵심 발견 3: **단위셀 주기↓ → SSA↑(반응site↑) but pore 좁아짐 → 유효 D_O₂↓ → 고율 용량 제한(trade-off).**

전략: 단위셀 주기를 줄여(**B600→B500→B400→B300**, in-plane 600/500/400/300 nm) 구조변화를 디지털트윈으로
정량(Fig 3a 단위셀 형상, Fig 3b 레이더플롯, Table S3) → 1D 모델로 성능예측(Fig 4).

**구조 파라미터 (Table S3) — period 의존:**
| 파라미터 | B600 | B500 | B400 | B300 | 추세 |
|---|---|---|---|---|---|
| 도메인 (µm³) | 0.6×0.6×1.86 | 0.5×0.5×0.75 | 0.4×0.4×0.4 | 0.3×0.3×0.3 | — |
| **porosity (%)** | 45.6 | **56.9** | 51.1 | 54.3 | **비단조**(B500>B300>B400>B600) |
| **SSA (×10⁷ m²/m³)** | 1.02 | 1.69 | 2.10 | **2.88** | **단조 증가**(period↓→SSA↑) |
| **유효 σ_e (×10⁴ S/cm)** | 5.92 | 1.78 | 3.42 | 0.67 | 비단조 |
| **유효 σ_ion (×10⁻⁴ S/cm)** | 1.28 | **2.08** | 1.61 | 1.82 | 비단조 |
| **유효 D_O₂ (×10⁻⁸ cm²/s)** | 0.92 | **1.67** | 1.29 | 1.46 | **비단조**(B500>B300>B400>B600) |
| intrinsic σ_e (Ni) | — | — | — | — | 1.42×10⁵ S/cm (Table S3 각주) |

- ★ **SSA는 period↓에 단조 증가**(1.02→2.88×10⁷). 그러나 **porosity·유효 D_O₂는 비단조**(둘 다
  B500 > B300 > B400 > B600 순서). 이유: BCT 단위셀이 **PnP(근접장 나노패터닝)의 비자기유사
  (non-self-similar) 형상**에서 유래 → period가 단지 크기만 바꾸는 게 아니라 **strut/node 치수·pore-throat
  연결성**까지 바꿈[40,41]. (B600–B300는 리소그래피 공정-relevant 형상을 광강도분포로 생성.)
- ★ **유효 D_O₂ 순서 = porosity 순서**(B500>B300>B400>B600) → **산소수송은 pore 부피 + pore-network
  연결성의 결합효과로 결정**, 단위셀 크기 단독이 아님.

**percolation 경로 분석 (Fig 3c + Fig S6):**
- **최대 percolation 경로 직경**(전해질상 내 용존 O₂/Li⁺의 가장 열린 연속수송채널 직경): **B500 > B600 >
  B300 > B400** 순서(Fig 3c: 약 0.09(B600)/0.10(B500)/0.05(B400)/0.06(B300) µm 부근, 디지타이즈 TREND).
  → **가장 열린 연속수송채널은 작은 단위셀일수록 현저히 좁아짐.** (Fig S6: B600–B300 각각의 최대직경
  percolation 경로 3D 시각화 — B600은 굵고 길게 관통, B300은 가늘고 짧음.)

**산소 확산플럭스 공간분포 (Fig 3d):**
- **큰 단위셀(B600·B500): O₂ 플럭스가 비교적 균일** 분포. **작은 단위셀(B400·B300): 국소 고플럭스 영역
  발달**(특히 B300·B400) → 강한 농도구배. → 좁은 채널에 플럭스 집중 → **국소 Li₂O₂ 가속·기공막힘 →
  비균일 pore/표면 진화 → premature end-of-discharge 취약**[17].

**Li₂O₂ film 성장 가정 (Fig S7) — 30 nm uniform film:**
- A3D 골격에 **film형 Li₂O₂를 0→30 nm 두께로 uniform deposition 가정** 도입(Fig S7a 시각화: Ni 회색 +
  Li₂O₂ 노랑). film 두께↑ → **electrode porosity↓·SSA(약간 비단조)·유효 D_O₂↓·유효 σ_ion↓**(Fig S7b–e:
  B600/B500/B400/B300/D400 각각 0→30 nm 진화). 특히 **B400·B300은 높은 초기 SSA에도 좁은 percolation
  경로 때문에 Li₂O₂ 성장에 더 쉽게 막힘**(porosity·D_O₂의 더 가파른 하락). ⇒ **방전성능은 초기 반응site
  밀도·수송뿐 아니라, 방전생성물 축적 하에서 pore network가 산소·이온 수송을 보존하는 능력에 좌우.**

**BCT 방전성능 (Fig 4a–c) — period 효과:**
- **0.01 mA/cm²(저율):** 작은 단위셀(B300·B400)이 **early-to-mid 방전에서 낮은 분극**(높은 SSA 덕) +
  방전 plateau가 깊은 DOD까지 유지. B600은 일찍 종료(낮은 가용용량). DOD 100% areal capacity 최대 =
  **B500**(상대적으로 높은 porosity로 Li₂O₂ 수용 — Fig 2d–e의 "저율=porosity가 용량 결정" 추세와 일치).
- **0.05 mA/cm²(고율):** 모든 곡선이 분극↑·early termination↑. 단위셀 간 성능차 확대(수송제약 영향↑).
  ★ **최대 areal capacity = B500**(SSA 최고는 B300인데도!) — 이유: **B500이 최대 유효 D_O₂**를 가져
  anomalous-diffusion 열화영역을 벗어남(Fig 2i의 비단조성). **B300은 최대 SSA로 분극은 최소**지만, 좁은
  pore + Li₂O₂ 막힘으로 용량 제한.
- (Fig 4b 0.01 / 4c 0.05: DOD 100% 용량 + DOD 50% 과전압 막대 — B500이 용량, B300이 과전압 최소.)

**두께방향 porosity·O₂ 진화 (Fig 4d,e):**
- (Fig 4d, 0.05 mA/cm², DOD vs 전극두께 porosity colormap, B600–B300) **B600: gas side에서 저DOD에도
  급격한 porosity 감소** → 조기 국소 기공막힘 → pore 부피 다 쓰기 전 방전종료. B400·B300도 (높은 D_O₂에도)
  gas side 근처 가속 porosity 고갈. **B500: gas side 근처 porosity 고갈이 가장 억제** → 가장 깊은 반응범위.
- (Fig 4e, DOD 50%, 두께방향 O₂ 농도) **B500이 전극 두께 전체에서 가장 높은 용존 O₂ 농도 유지** → 더
  균질한 반응성·고용량(고율). ⇒ **B500이 SSA·porosity·D_O₂의 최적 균형**(period sweep에서).

### 3.4 diamond-type A3D 설계 (Fig 5, Fig S8, S9, S10) — 설계지침

★ 핵심 발견 4: **diamond 단위셀(잘 연결된 pore network) + 표면공학(electropolishing) → SSA↑를 산소수송
보존과 양립 → 성능 개선.**

**동기:** BCT period↓는 SSA↑이나 D_O₂↓를 동반(trade-off) → "SSA↑를 유지하되 산소수송경로(크고 잘 연결된
pore)를 보존"하는 구조가 필요[42]. → **diamond-type 단위셀** 제안(highly connected pore network).

**D400 (diamond, 400 nm period; Fig 5a, Fig S8, S9):**
- **잘 연결된 pore network** 덕에 **favorable 유효 D_O₂ + σ_e/σ_ion** → 400 nm period로 **B500급 구조물성**
  달성(Fig 5a 레이더). (Fig S8: D400의 최대 percolation 경로 — 최대직경 **0.22 µm로 B600~B300의 모든 BCT를
  상회**(Fig S8b: B600 0.09/B500 0.10/B400 0.05/B300 0.06 vs **D400 0.22**) = diamond가 훨씬 굵은 연속채널.)
- **균일·높은 O₂ 플럭스**(Fig S9: D400 전해질상 O₂ 확산플럭스 공간분포 — 균일) → spatially homogeneous ORR
  + 수송제약 분극↓.
- **방전(Fig 5c):** D400은 **B500과 comparable 성능**(0.01·0.05 mA/cm²). 단 **D400은 BCT 대비 SSA·porosity가
  상대적으로 낮음** → 더 높은 kinetic 과전압·낮은 용량 예상(SSA가 부족).

**D300EP (diamond 300 nm + electropolishing 표면거칠기; Fig 5b, Fig S10):**
- D400의 SSA 부족을 메우려 **period를 400→300 nm로 축소(D300)** + **electropolishing 기반 표면공학으로
  표면거칠기 도입(D300EP)**[43,44] → **SSA를 B300급으로 대폭↑ + porosity·유효 D_O₂도 동반 증가**(Fig 5b
  레이더: D300EP가 D300 대비 SSA·porosity·D_O₂ 모두 확장). (electropolishing은 solid 부피분율↓ → 유효 σ_e
  소폭↓이나, 현 조건에서 σ_e는 rate-limiting 아님이라 성능제약 안 됨.)
- ★ **D300EP = 최고 성능:** 저율에서 **분극 markedly↓**, 고율에서 **방전용량 markedly↑**(Fig 5c,
  Fig S10: D400/D300/D300EP 방전곡선 — D300EP가 가장 높은 용량·낮은 분극). 정량(Fig 5d, DOD 100% 용량 +
  DOD 50% 과전압):
  - ★ **D300EP의 areal capacity = B500·D400 대비 최대 37%↑**(고율에서 가장 큰 개선). SSA 대폭증가 →
    양 전류밀도에서 capacity 개선(고율에서 가장 두드러짐).
- ⇒ **제안된 diamond-type 단위셀 + 표면공학 = SSA↑를 산소수송경로 보존과 양립 → 실용적 고성능 A3D 설계.**

### 3.5 종합 (Fig 1b graphical, 레이더플롯 통합)
- **핵심 결론:** "rational microstructural programming(미세구조의 합리적 프로그래밍)은 촉매공학을 넘어
  LOB의 **TPB 동역학을 안정화**하는 결정적 경로"(초록). 구조변수 독립변화 → **산소수송 조절이 반응국소화·
  용량을 직접 지배** 규명 → **transport polarization 최소화 + 방전용량 증대** 설계(diamond + 표면공학) 제시.
- ★ **레이더플롯**(Fig 3b·5a·5b)이 5축(SSA·porosity·유효 D_O₂·유효 σ_ion·유효 σ_e)으로 각 구조를 한눈에
  비교 — **다목적 구조-물성 균형 시각화**(B500이 균형, D300EP가 SSA·porosity·D_O₂ 동시확장).

---

## 4. 그림 한 장씩 — 무엇을 보이고 우리가 쓸 것

### 본문 Figures
- **Fig 1 (p.3):** (a) LOB 셀구성·공기극 반응 모식(Li→Li⁺+e⁻; 2Li⁺+O₂+2e⁻→Li₂O₂; O₂확산·이온/전자수송
  zoom). (b) ★ **graphical: 1D 전기화학 모델 ↔ 3D 디지털트윈 결합 모식**(Li metal|separator|air electrode,
  지배방정식 + virtual/physical 전극). (c) A3D vs foam **유효 σ_e**(exp vs sim, A3D 2.51e5 ≫ foam 0.40e4).
  (d) A3D vs foam **전자밀도 공간분포**(A3D 높고 균일, foam 낮고 heterogeneous). (e) A3D vs foam **SSA**
  (exp vs sim, A3D 1.02e7 ≫ foam 0.88e5). (f) ★ **A3D 방전곡선 sim vs exp**(0.01/0.05/0.10 mA/cm²,
  good agreement). → ★ **디지털트윈→1D 모델 결합·검증의 1장 = 우리 Phase 4 결합도의 직접 대응.**
- **Fig 2 (p.5):** ★ **구조변수 decouple** — (a) SSA별 방전곡선, (b/c) SSA-DOD **areal capacity colormap**
  (0.01/0.05). (d) porosity별 곡선, (e/f) porosity-DOD colormap. (g) D_O₂별 곡선, (h/i) D_O₂-DOD colormap
  (★ 0.05에서 비단조). → ★ **SSA/porosity/D_O₂를 독립 변화 → 성능 귀속 = 우리 predictor(knobs→metrics→
  performance)의 published 실증.** colormap이 "전류밀도가 어느 변수를 지배하는지"를 시각화.
- **Fig 3 (p.6):** ★ **BCT 단위셀** — (a) B600–B300 단위셀 형상(1860/750/400/300 nm 높이). (b) ★ **레이더
  플롯**(5축 구조물성, B600/B500/B400/B300 각각). (c) **최대 percolation 경로 직경**(B500>B600>B300>B400).
  (d) **O₂ 확산플럭스 공간분포**(큰셀 균일 vs 작은셀 국소집중). → ★ **단위셀 period→구조물성 정량 +
  percolation/flux 시각화 = 우리 packing/percolation/transport-network 분석의 LOB 버전.**
- **Fig 4 (p.7):** **BCT 방전·진화** — (a) B600–B300 방전곡선(0.01/0.05). (b/c) DOD100% 용량 + DOD50%
  과전압 막대(0.01/0.05; B500 용량·B300 과전압 최소). (d) **두께방향 porosity colormap**(DOD vs depth,
  B600–B300). (e) **DOD50% 두께방향 O₂ 농도**(B500 최고 유지). → ★ **두께방향(depth-resolved) porosity·O₂
  진화 = 우리 z-구배(#286 Phase 5)·depth-resolved transport 대응.**
- **Fig 5 (p.8):** ★ **diamond 설계** — (a) D400 단위셀 + 레이더(B500급 물성). (b) D300EP 단위셀 + 레이더
  (SSA·porosity·D_O₂ 확장). (c) B500/D400/D300EP 방전곡선(0.01/0.05). (d) DOD100% 용량 + DOD50% 과전압
  막대(D300EP 최고용량·최저분극, +37%). → ★ **구조최적화 설계지침의 결론(우리 predictor→synth 설계
  최적화 사고와 동형).**

### SI Figures (S1–S10) + Tables (S1–S3)
- **Fig S1:** ★ **1D 모델 도메인 + 지배방정식 + BC 전체**(Li metal|separator|air electrode|GDL, 물질/전하
  보존 + 계면반응식). → ★ **우리 Phase 4 PyBaMM 방정식셋업 비교 reference.**
- **Fig S2:** **디지털트윈 구조** — (a) A3D 전극(unit cell 1860 nm → Repeat → 8 µm 큐브), (b) foam 전극
  (3000×3000×120 µm, top/cross-sectional view). → ★ **STL→voxel→RVE(Repeat) 파이프라인 = 우리 voxel
  입력 생성 대응.**
- **Fig S3:** **과전압 colormap**(DOD vs SSA, 0.01/0.05) — 저율 균일·고율 강한 구배(SSA가 고율 과전압 지배).
- **Fig S4:** (a) DOD50% 두께방향 **O₂ 농도**(0.5/1.0/1.5/2.0× D_O₂) + (b) **porosity 진화 colormap**
  (DOD vs depth, 0.05 mA/cm²) → ★ **비단조 D_O₂(1.5× 이상열화)의 메커니즘 시각화(국소고갈·기공막힘).**
- **Fig S5:** σ_e(a)·σ_ion(b) 변화 방전곡선 — **곡선 겹침(전도도 rate-limiting 아님).**
- **Fig S6:** **BCT 최대직경 percolation 경로 3D**(B600–B300, full/cross/pathway) — 작은셀일수록 좁고 짧음.
- **Fig S7:** ★ **film형 Li₂O₂ 성장**(a, 0→30 nm 시각화 Ni+Li₂O₂) + (b)porosity (c)SSA (d)D_O₂ (e)σ_ion의
  film 두께 의존(B600–D400) → **방전생성물 축적 하 구조물성 진화 = 우리가 안 다루는 deposition-진화 축.**
- **Fig S8:** diamond D400 **최대 percolation 경로**(a 3D + b 최대직경 0.22 µm로 BCT 전부 상회).
- **Fig S9:** D400 **O₂ 확산플럭스 공간분포**(균일).
- **Fig S10:** D400/D300/D300EP **방전곡선**(0.01/0.05; D300EP 최고).
- **Table S1:** ★ A3D vs foam 구조물성(domain/porosity/SSA/intrinsic+effective σ_e·σ_ion·D_O₂).
- **Table S2:** ★ **1D 모델 전체 파라미터셋**(두께·porosity·SSA·유효 σ·κ_EL·t₊·D_O₂·O₂농도·용해도·
  Li₂O₂막저항·전류밀도) — §2.2(6) 표.
- **Table S3:** ★ B600/B500/B400/B300 구조물성(porosity·SSA·유효 σ_e·σ_ion·D_O₂) — §3.3 표.

---

## 5. 기술 미니용어집 (우리 맥락)

- **A3D (architected 3D electrode):** 주기적 단위셀(BCT/diamond)로 구성된 정렬 다공전극. 무작위 foam과
  달리 **구조 파라미터를 정의·정량·독립변화** 가능 → 모델링↔실험 직접비교 platform. (우리 입장: 우리는
  DEM/MPM으로 무작위 입자패킹을 만들지만, 둘 다 "미세구조 → 유효물성" 추출이라는 점에서 동형.)
- **GeoDict 모듈(우리 voxel FV 대응):** **MatDict**(SSA/면적), **ConductoDict**(voxel에 ∇·(σ∇φ)=0 →
  유효 σ_e·σ_ion = 우리 `voxel_conductivity.py`), **DiffuDict**(voxel에 정상상태 Fick → 유효 D = 우리
  voxel FV의 확산 버전, 아직 우리엔 없음), **ProcessGeo 'Repeat'**(단위셀 주기복제 RVE 조립),
  **GrainGeo 'Roughen Surface'**(표면거칠기), **FoamGeo**(확률적 foam).
- **SSA (specific surface area):** 단위 전극부피당 내부계면적(m²/m³ = 반응이 일어나는 TPB의 총량 대용).
  Li-O₂에선 **반응site·Li₂O₂ 저장표면**. 우리 대응 = **coverage/접촉면적(A_total, Tabor·B3)** — 단,
  Li-O₂의 SSA는 "전해질-기체-전자상이 만나는 면적"이고 우리 coverage는 "SE가 AM을 덮는 면적"이라 **물리
  의미가 다름**(개념적 대응만).
- **TPB (triple-phase boundary):** 기체(O₂)-전해질(Li⁺)-전자전도상(Ni)이 동시에 만나는 삼상경계 = ORR이
  실제 일어나는 곳. **우리 ASSB엔 기체상이 없어 TPB 개념 부재**(우리는 SE-AM 이상경계 contact). Li-O₂
  특유 — 비전이.
- **유효 D_O₂(effective oxygen diffusivity):** 다공구조에서 균질화된 용존 산소 확산도 = D_O₂,intrinsic ×
  (ε/τ). 우리 transport σ의 확산 대응. 우리에겐 **D_eff 추출이 없으나 voxel FV 프레임에 확산계수만 넣으면
  동일하게 풀린다**(이식 후보).
- **Li₂O₂ film 성장 + 기공막힘:** 방전생성물 Li₂O₂가 내부표면에 **저항막(50 Ω·m²)형으로 성장 → SSA·
  porosity 감소 → passivation·기공막힘 → 방전종료.** 우리엔 **deposition/시간진화 축 없음**(우리는 압축종점
  단일구조). = 우리가 미구현한 **방전 중 구조진화** 메커니즘.
- **DOD (depth of discharge):** 방전심도(0=만충, 1=완전방전). colormap의 y축으로 "방전 어느 단계에서
  어느 구조변수가 지배"를 보여줌.
- **BCT period / diamond unit cell:** 단위셀 면내 주기(600→300 nm). period↓ → SSA↑·pore↓·D_O₂↓(trade-off).
  diamond = 잘 연결된 pore network로 trade-off 완화. = 우리 packing 최적화(Furnas) 사고의 정렬-구조 버전.
- **electropolishing (EP):** 전해연마 표면공학 → 표면거칠기↑ → SSA↑(D300EP). 우리 표면거칠기 B3 coverage
  대응(표면거칠기가 유효접촉/면적을 바꿈).

---

## ★ 6. 비교 vs 우리 DEM+MPM + Phase 4 (frame [4]/[5]) — METHODOLOGY가 가치

⚠ **대전제(맨 먼저):** 이 논문은 **Li–O₂ 전지(금속-공기, 액체전해질, O₂ 가스 reactant, Li₂O₂ 생성물)**다 —
우리 **LPSCl sulfide ASSB(고체전해질, 무전해질, SE-AM contact-network, 무기체)**가 **전혀 아니다**. 따라서:
- **모든 전기화학·구조 절대값은 전이 불가.** 용량(mAh/cm²)·과전압(V)·O₂ 확산도·SSA(m²/m³)·Li₂O₂ 막저항·
  유효 σ는 **Li-O₂/액체계**의 값이고, 우리 σ_ionic/e는 **SE/AM 입자 접촉망의 Kirchhoff/Holm 전도**다 —
  물리 메커니즘 자체가 다름(전해질-매개 O₂/Li⁺ 확산 + Li₂O₂ film vs solid contact 전도). **수치 σ/porosity
  앵커는 Bazzoun(LPSCl)·Varkey(halide)·Minnmann(LPSCl cold-press)·#266(bimodal ASSB)이 담당** — 이 논문에서
  가져오지 않는다.
- 가져올 것은 **METHODOLOGY 3종**: (a) GeoDict ConductoDict/DiffuDict (voxel→유효물성) = 우리 voxel FV,
  (b) 미세구조→유효물성→1D 전기화학→성능 결합 = 우리 Phase 4 청사진, (c) 구조변수 decouple→성능 귀속 =
  우리 predictor. 아래 1:1 매핑.

### (a) ★ GeoDict ConductoDict/DiffuDict ↔ 우리 voxel_conductivity FV (가장 직접적 대응)
- **그들 ConductoDict:** voxel 상에서 도메인 양단에 **일정 전위차** 인가 → ∇·(σ∇φ)=0 풀어 **유효 σ_e·σ_ion**
  추출(공기극 σ_e 2.51e5, σ_ion 1.28e-4 S/cm). **DiffuDict:** 일정 농도차 인가 → 정상상태 Fick 풀어 **유효
  D_O₂**(0.92e-8 cm²/s).
- **우리 `scripts/voxel_conductivity.py`:** MPM phase grid(void/SE/AM/VGCF/SuperP)에 per-voxel σ 할당 →
  **TOP 1V / BOTTOM 0V**, ∇·(σ∇φ)=0(finite-volume, harmonic-mean face conductance, 측벽 insulating) →
  **σ_eff = I·L/(A·ΔV)**. = **수학적으로 동일한 effective-property FV 솔버**(그들 GeoDict의 in-house 버전).
- ✅ **같은 접근의 독립 평행구현:** 둘 다 "voxel 미세구조 → ∇·(σ∇φ)=0/Fick → 균질화 유효물성"이다. 차이는
  (i) **그들 voxel=10 nm 고해상**(8µm 도메인에 800 voxel/축) vs **우리 0.07µm/cell**(n_vox=256); (ii) 그들은
  **정렬 단위셀**(strut/node 잘 정의) vs 우리는 **무작위 입자패킹**(점접촉 constriction이 본질).
- ★ **우리가 이미 검증한 한계가 여기서도 그대로 적용**(`docs/voxel_conductivity_crossvalidation.md`):
  voxel FV는 **접촉넥이 voxel로 resolvable할 때만** constriction을 잡는다. 그들 A3D는 **strut/node가 수십
  voxel 폭(잘 연결된 연속 골격)** → constriction이 resolvable → ConductoDict 유효 σ가 σ_full에 수렴(우리
  electronic이 AM 큰 넥에서 σ_full=11.75에 수렴한 것과 동형). **만약 그들 구조가 우리 SE처럼 sub-voxel
  점접촉이었다면** GeoDict도 contact-free 상한을 줄 것 — 즉 **voxel FV의 적용성은 "넥이 voxel로 보이느냐"에
  달렸고, 정렬-연속 골격(A3D/AM)에는 맞고 granular 점접촉(우리 SE)에는 DEM Holm이 필요**(frame[5]).
- ★ **이식 후보 — DiffuDict 대응(유효 D_eff):** 그들은 같은 voxel FV 프레임에서 **확산계수**를 풀어 유효
  D_O₂를 얻는다. 우리 voxel FV는 현재 σ(전도)만 푸나, **동일 코드에 D를 넣으면 유효 확산도(↔τ)** 가 바로
  나온다 → **우리 τ(현재 Laplace/Dijkstra contact-network τ)의 voxel-continuum 교차검증**(frame[4]) 도구
  추가 가능. (단 ASSB엔 O₂ 가스가 없으니 **Li⁺ 유효확산/τ**에 적용.)

### (b) ★ 미세구조→유효물성→1D-COMSOL ↔ 우리 미세구조→유효물성→PyBaMM (Phase 4 결합 템플릿) — 가장 큰 가치
- **그들 결합:** 디지털트윈 GeoDict 유효물성(ε=45.6%, SSA=1.02e7, σ_e=2.51e5, σ_ion=1.28e-4, D_O₂=0.92e-8)
  → **COMSOL 1D 전기화학 모델의 입력**(Table S2) → 방전곡선 예측(Fig 1f). **핵심 도메인(공기극)은 측정
  effective 물성, 보조 도메인(GDL)은 Bruggeman ε^1.5 근사**를 혼용.
- **우리 Phase 4(`docs/stage4_electrochem_research.md`):** **우리 미세구조 유효물성(τ_Laplace,eff·σ_ionic/e·
  porosity·particle radius·thickness) → PyBaMM DFN 입력** → CC/CV·EIS·GITT·방전곡선. ★ **THE BRIDGE:**
  PyBaMM `{"transport efficiency":"tortuosity factor"}` + `"... tortuosity factor (electrolyte)"` 로
  **측정/계산 τ를 직접 주입**(Bruggeman ε^1.5 추정 대신) + `"... conductivity [S.m-1]"`로 σ 주입.
- ✅ **이 논문 = 우리 Phase 4의 published blueprint:** "미세구조 → effective ε/τ/σ/D → 1D 다공전극
  전기화학 모델 → 셀 성능"의 **결합 방식·입력 정의가 정확히 우리가 PyBaMM으로 하려는 것**이다. 그들의
  COMSOL 1D = 우리의 PyBaMM DFN. 그들의 Table S2(effective 물성 주입) = 우리의 ParameterValues τ/σ 주입.
- ★ **직접 채택할 결합 디테일 3가지:**
  1. **"핵심 전극은 측정 effective 물성, 보조 도메인은 Bruggeman"** 혼용 = 우리 전략 그대로(양극은 우리
     voxel τ/σ, separator/anode는 기본/Bruggeman). 그들이 이 혼용을 검증된 모델로 publish → 우리 접근의 근거.
  2. **"구조에서 못 얻는 동역학 파라미터는 문헌+실험fit, 그 다음 구조변수만 변화"** = 우리 Phase 4의 깨끗한
     구조-isolation 프로토콜(반응속도상수 등은 Chen2020 등에서, 우리 τ/σ만 바꿔 미세구조 효과 분리).
  3. **방전(환원)만 모델, 충전은 추가물리 필요로 분리** = 우리도 1차로 방전/discharge부터(OER/충전의 추가
     degradation은 Phase 3 fracture와 별도). 그들의 "Li₂O₂ 산화는 단순 역방전 아님" 논리 = 우리 충전측
     degradation을 별도 취급할 근거.
- ⚠ **비전이(주의):** 그들 1D 모델의 **방정식·파라미터는 Li-O₂ 특유**(O₂ 용존확산, Li₂O₂ film 50 Ω·m²,
  TPB ORR Butler-Volmer, t₊=0.92 액체). 우리 ASSB PyBaMM은 **단일이온 SE(t₊≈1, 무대류·무O₂), 접촉저항,
  mechano-electrochemical 결합**으로 적응 필요(`stage4_electrochem_research.md` §0 이미 명시). **결합
  프레임(미세구조→effective→1D→성능)은 이식, 방정식/물성은 우리 ASSB로 교체.**

### (c) ★ 구조변수 decouple → 성능 귀속 ↔ 우리 predictor(design knobs → metrics → performance)
- **그들:** **SSA·porosity·D_O₂·σ를 독립적으로 배수변화 → 각각이 용량·과전압·반응국소화에 미치는 영향을
  분리·귀속**(Fig 2 colormap: 전류밀도가 어느 변수를 지배하는지까지). 예: "저율=porosity가 용량 지배,
  고율=SSA가 지배, D_O₂는 비단조."
- **우리 predictor(Phase 3):** **design knobs(P:S·AM%·압력·입경·CBD) → 전체 metric set(σ_ionic/e/thermal·
  porosity·coverage·τ·CN) → (Phase 4)성능**을 학습. = **구조변수→metric→성능의 귀속을 ML로** 하는 것.
- ✅ **사고 동형:** 그들의 "구조변수 독립변화 → 성능 attribution"이 곧 우리 predictor의 목적이다. 차이:
  그들은 **물리모델(COMSOL)로 1변수씩 sweep**(해석적 귀속), 우리는 **ML로 다변수 동시학습**(통계적 귀속).
- ★ **이식 후보 — colormap 귀속 시각화:** 그들의 **"(구조변수 × DOD) → 성능 colormap"**(어느 조건에서 어느
  변수가 지배하는지)은 우리 predictor 출력에 직접 채택 가능 = **"(우리 knob × 작동조건) → metric 민감도
  히트맵"**. 우리 σ_ionic/e가 어느 design 영역에서 어느 변수(φ_SE·CN·τ)에 민감한지 시각화 → 그들 Fig 2식
  귀속맵. (우리는 이미 ablation/Spearman으로 항별 기여를 봄 — colormap은 그 작동조건 의존 버전.)
- ★ **이식 후보 — 레이더플롯(다축 구조-물성 균형):** 그들 Fig 3b/5a/5b 5축 레이더(SSA·porosity·D_O₂·σ_ion·
  σ_e)는 **여러 구조를 다목적 물성공간에서 한눈에 비교**. 우리 design point(real_9/real_14/S_1 등)를
  **5–6축 레이더(porosity·σ_ionic·σ_e·κ·coverage·CN)**로 그리면 **trade-off 시각화**에 유용(우리 predictor
  출력·case 비교 대시보드에 추가 후보).

### (d) frame[5] 분업 — 우리 우위 명확화
- **그들:** **디지털트윈 구조분석(GeoDict effective 물성) + 1D 전기화학(COMSOL) 결합** — 강력하지만:
  **입자스케일 압축역학 예측 없음**(단위셀 형상은 CAD/리소그래피로 주어진 고정 미세구조), **압력→미세구조
  예측 없음**(A3D는 PnP 제작물; 우리처럼 압력 sweep으로 porosity가 emergent하지 않음), **소성 morphology·
  void-fill 없음**, **접촉 σ triad 중 전자/이온만**(thermal 없음; granular constriction 없음 — 정렬골격이라
  불필요). voxel-continuum이라 **pore-scale heterogeneity·미세구조-resolved deposition은 명시적으로 못
  잡음**(논문 p.7 자인: "1D framework relies on volume-averaged effective properties... cannot explicitly
  capture pore-scale heterogeneities and microstructure-resolved deposition"). 그래서 그들도 **거시 방전성능
  (effective 물성지배)에 한정**하고 pore-scale 진화는 향후 microstructure-resolved 모델에 위임.
- **우리 DEM+MPM:** **압력→미세구조→σ(ionic/e/thermal triad) 예측**(Kirchhoff/Holm 접촉망) + **MPM 소성
  morphology·void-fill·strain field** + **voxel FV로 carbon network·유효물성 교차검증** + **fracture(Auerbach)**
  + **granular 점접촉 constriction**(그들 정렬골격엔 없는, 우리 SE의 본질).
- ⇒ **이상 워크플로:** 우리 DEM+MPM이 **압력하 미세구조를 생성/예측**(그들은 못 함) → GeoDict식
  effective 물성(우리 voxel FV) 추출 → 그들식 **1D 전기화학(우리 Phase 4 PyBaMM)** 결합으로 셀 성능. 이
  논문은 **우리 파이프라인의 출력단(effective→1D→성능) 결합 청사진 공급원**이지 입력단(구조생성) 경쟁자가
  아니다. (frame[5] 재확인 — 그들엔 입자스케일 압축예측·접촉 σ triad·granular constriction이 없음.)

### 비교 요약표
| 축 | Kim 2026 (Li-O₂·A3D·액체) | 우리 (LPSCl ASSB, DEM+MPM) | 이식/판정 |
|---|---|---|---|
| 소재/reactant | Li-O₂, O₂ 가스 + 액체 Li⁺, Li₂O₂ | LPSCl SE + NMC811, solid contact | ⚠ **모든 절대값 전이불가**(용량·과전압·SSA·D_O₂·σ) |
| 미세구조 생성 | CAD/리소그래피 정렬 단위셀(고정) | DEM 압력→입자패킹(emergent) | 우리 우위(압력→구조 예측; 그들은 고정) |
| voxel→유효물성 | **GeoDict ConductoDict/DiffuDict** | **voxel_conductivity FV** | ✅ **동일 접근**(∇·(σ∇φ)=0/Fick); D_eff는 이식 후보 |
| SSA/coverage | MatDict SSA(TPB 대용) | Tabor·B3 coverage·A_total | 개념 대응(물리의미 다름: TPB vs SE-AM) |
| constriction | 정렬골격→resolvable(불필요) | granular 점접촉→DEM Holm 필수 | frame[5]: voxel은 정렬골격, DEM은 granular |
| 1D 전기화학 결합 | **미세구조→effective→COMSOL 1D→방전** | **미세구조→effective→PyBaMM DFN→성능(Phase 4)** | ✅ **Phase 4 published blueprint**(결합 디테일 3종 이식) |
| 구조변수 귀속 | 1변수 sweep + DOD colormap(해석적) | predictor ML(다변수 통계적) | ✅ 사고 동형; colormap·레이더 시각화 이식 |
| 방전생성물 진화 | Li₂O₂ film→SSA/porosity↓(시간진화) | (없음 — 압축종점 단일구조) | 우리 미구현 축(deposition); 그들 고유 |
| 우리 고유 | (없음) | DEM 접촉 σ triad + MPM 소성 + fracture + 압력→구조 | frame[5] 분업 재확인 |
| 그들 고유 | TPB ORR·O₂확산·Li₂O₂ film 1D 전기화학 | (없음 — Phase 4가 채울 자리) | Phase 4 결합 템플릿 공급원 |

---

## ★ 7. 우리 작업에 넣을 가장 날카로운 인사이트 (Phase 4 / voxel 파이프라인)

1) ★★★ **이 논문 = 우리 Phase 4의 published blueprint — "미세구조 → effective 물성 → 1D 전기화학 → 성능"
   결합이 검증된 형태로 존재.** 그들 COMSOL 1D(effective ε/τ/σ/D_O₂ 주입 → 방전곡선)는 정확히 우리 PyBaMM
   DFN(우리 voxel τ/σ 주입 → 셀 성능)이 하려는 것이다. **직접 채택할 결합 디테일 3종**: (i) **핵심 전극은
   측정 effective 물성, 보조 도메인은 Bruggeman ε^1.5 혼용**(그들 공기극=GeoDict / GDL=Bruggeman → 우리
   양극=voxel τ/σ / separator·anode=기본), (ii) **구조에서 못 얻는 동역학 파라미터는 문헌+실험fit 후 고정,
   구조변수만 변화**(깨끗한 미세구조-isolation), (iii) **방전부터 모델, 충전/OER은 추가물리로 분리.** →
   우리 `stage4_electrochem_research.md`에 이 3종을 결합 프로토콜로 명문화.

2) ★★ **GeoDict ConductoDict/DiffuDict = 우리 voxel_conductivity FV의 상용판 → 접근 검증 + DiffuDict
   (유효 D_eff/τ) 이식.** 그들 ConductoDict(voxel ∇·(σ∇φ)=0 → 유효 σ_e·σ_ion)는 우리 voxel FV와
   **수학적으로 동일**(이 그룹의 3번째 GeoDict 활용 — #286 τ, #284 W_adh 다음). ✅ 우리 voxel FV 접근이
   상용 표준과 같음을 확증. ★ **DiffuDict(같은 프레임의 확산버전)는 우리에게 없다** → 우리 voxel FV에
   **확산계수 모드를 추가**하면 **유효 D_eff(↔τ)를 voxel-continuum으로** 얻어 **우리 contact-network
   τ(Laplace/Dijkstra)와 frame[4] 교차검증** 가능(ASSB는 Li⁺ 유효확산에 적용). 단 우리가 이미 정리한
   voxel 한계(점접촉 sub-voxel → constriction 못 잡음, `voxel_conductivity_crossvalidation.md`)가 D_eff에도
   동일 적용 — **정렬골격엔 맞고 granular SE엔 DEM Holm 필요**(frame[5]).

3) ★★ **구조변수 decouple + DOD colormap/레이더 = 우리 predictor 출력 시각화 이식.** 그들 Fig 2의 "(구조변수
   × DOD) → 성능 colormap"(전류밀도가 어느 변수를 지배하는지)과 Fig 3b/5 5축 레이더(다목적 구조-물성 균형)는
   우리 predictor에 직접 채택 가능: **"(우리 knob × 작동조건) → metric 민감도 히트맵"** + **case별 5–6축
   레이더(porosity·σ_ionic·σ_e·κ·coverage·CN)** → trade-off·민감도를 한눈에. 우리는 이미 ablation/Spearman
   으로 항기여를 보지만, **colormap은 그 작동조건-의존 버전, 레이더는 다축 균형 버전**.

4) ★ **"미세구조에 의한 산소수송 조절이 반응국소화·용량을 지배"(그들의 핵심 물리) = 우리 "미세구조에 의한
   τ/contact 조절이 σ_ionic·균질성을 지배"와 동형 메시지.** 그들은 **D_O₂를 1.5×로 올리면 오히려 국소집중→
   기공막힘→조기종료(비단조)**를 보임 = "단순히 수송↑이 항상 좋은 게 아니라, 수송·반응·생성물막힘의 결합이
   지배." → 우리도 **"σ_ionic을 단순 최대화"가 아니라 균질성·percolation·packing의 결합**을 봐야 한다는
   서사강화(우리 Furnas dip·균질 전자망 논의와 같은 결).

5) ★ **frame[5] 재확인 + 우리 우위:** 이 논문은 **고정 미세구조(CAD/리소그래피)에 GeoDict+1D 전기화학을
   결합**하는 강력한 출력단 파이프라인이나, **압력→미세구조 예측·입자스케일 압축역학·소성 morphology·접촉 σ
   triad·granular constriction·pore-scale deposition이 없다**(논문도 자인). 우리 DEM+MPM은 **입력단(압력→
   미세구조 emergent)**을 채운다. ⇒ **이상 워크플로 = 우리 DEM+MPM이 미세구조 생성/예측 → GeoDict식
   effective(우리 voxel FV) → 그들식 1D 전기화학(우리 Phase 4)**. 이 논문은 우리 파이프라인의 **출력단
   결합 청사진**이지 입력단 경쟁자가 아니다.

### 보너스 실행 항목
- **#281 인덱스 갱신**(아래 완료): web-abstract(★★) → 검증 수치/방법(GeoDict 5모듈, voxel 10nm, A3D vs foam
  σ_e 2.51e5 vs 0.40e4·SSA 1.02e7 vs 0.88e5, B600–B300 Table S3, D300EP +37%, 1D 모델 Table S2 전체셋,
  비단조 D_O₂, Li₂O₂ film 50 Ω·m²)로 교체. ★ **#263(Phase 4-5 blueprint)에 준하는 위상으로 승격**(명시적
  미세구조→1D-전기화학 결합이 #263의 2D→3D-합성보다 우리 Phase 4 결합단계에 더 직접 대응).
- ⚠ **혼동 금지(이 그룹 다른 논문과 역할 구분):**
  - **#281(이 논문, Li-O₂·A3D):** ★ **Phase 4 결합 blueprint(미세구조→effective→1D 전기화학→성능) +
    GeoDict ConductoDict/DiffuDict(=우리 voxel FV) + 구조변수 decouple(=predictor)** 공급원. **수치 σ/porosity
    앵커 아님**(Li-O₂ 외래).
  - **#263(separator, 2D→3D):** Phase 4-5 **합성(2D→stochastic-3D)** blueprint.
  - **#286(흑연, z-구배):** Phase 5 z-layer + 토모 정량(τ/PNM) + BESTmicro 전기화학시뮬 workflow.
  - **#284(SiOx/흑연):** CBD ion/electron trade-off 독립확증 + 분산 측정(SSRM/W_adh) + balance point.
  - **#285(단결정 NCMA):** rigid-AM 역학검증 + 점탄성 spring-back 미구현 한계.
  - **#266(bimodal ASSB):** P:S 7:3 + Furnas dip 실험앵커(★ ASSB 수치앵커).
  - **σ/porosity 절대앵커는 Bazzoun(LPSCl)·Varkey(halide)·Minnmann(LPSCl cold-press)·#266이 담당** — 이
    넷과 혼동 금지.
- **Stage-2 audit 영향 없음:** Stage-2 audit(`docs/stage2_model_audit_vs_literature.md`)은 **transport
  검증(σ_ionic 절대값·τ·CBD·E_eff 등)** 문서다. 이 논문은 **Li-O₂(외래 화학) + Phase-4 결합 방법론**이라
  Stage-2의 transport 판정(✅#1 σ_ionic 정합 등)에 **새 벤치마크를 더하지 않는다** → Stage-2 audit 갱신
  불필요(이 논문은 Phase-4 청사진 축). 단 **Phase 4 결합 프로토콜**(인사이트 1)은 `stage4_electrochem_research.md`
  에 반영 가치 — Stage-2가 아니라 Stage-4 문서.
- **DiffuDict 이식**(인사이트 2)을 `voxel_conductivity.py`의 향후 항목으로 — 확산계수 모드 추가 → 유효 D_eff
  /τ를 voxel-continuum으로 → contact-network τ와 frame[4] 교차검증(ASSB Li⁺ 유효확산).
