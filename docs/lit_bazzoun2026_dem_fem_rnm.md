# Bazzoun 2026 (J. Power Sources 661, 238682) — DEM + FEM + RNM 이온전도도 (우리와 동일 소재/코드)

**인용:** A.M. Bazzoun, J. Piruzjam, S. Hink, L. Rubacek, A. Fill, K.P. Birke, "Integration of
DEM-based microstructure generation with FEM and RNM simulations for evaluating ionic
conductivity in composite cathodes of all-solid-state batteries", Journal of Power Sources 661
(2026) 238682 (오픈액세스 CC-BY).  Mercedes-Benz AG + Univ. Stuttgart (IPV) + Helmut Schmidt Univ.
접수 2025-09-04, 게재확정 2025-10-23.

**소재:** **Li₆PS₅Cl (LPSCl)** SE + **NMC-811** CAM (둘 다 POSCO Korea) + CNF(탄소나노섬유) + PTFE
바인더 (dry-film).  ★ **우리와 정확히 같은 소재계** (Varkey의 할라이드와 다름).

DB 동반 파일: `docs/data/bazzoun2026_sigma_ionic.csv` (실험 σ_eff,ion 앵커 + 압력 스윕 + 조성).

---

## ★ 결론 — 이건 우리 σ_ionic 파이프라인(DEM→Kirchhoff/Holm)의 독립 평행 구현이다

Varkey(할라이드, 우리 MPM이 메우는 *간극*을 인정하는 frame[1]/[2] 확증)와 **성격이 정반대**다.
Bazzoun은 **우리 transport 쪽(DEM→네트워크 솔버)의 직접 교차검증(frame[4])**이다:
- 같은 소재 (LPSCl + NMC811), 같은 DEM 코드 (LIGGGHTS), 같은 접촉저항 물리 (Holm 구속저항),
  같은 Kirchhoff 전류평형.
- **실험 EIS로 σ_eff,ion 검증** (조성 3점 + 압력 스윕) → CLAUDE.md가 "missing direct
  validation"이라 한 **LPSCl 다중압력 σ_ionic 실측**을 제공.
- 단 **이온전도만** 다룸 (σ_e / σ_thermal 없음), 입자는 구(球)만 (형상변화·소성 없음).

---

## ★ 방법 & 지배방정식

### 1. DEM (§3.1) — LIGGGHTS, 우리와 동일 코드
- 구형 CAM + SE, 법선 Hertzian spring + 접선 damping spring (= 우리 hooke/hysteresis 계열).
- 도메인: 직육면체 10D̄ × 10D̄ (측방) × 15D̄ (수직), D̄ = 큰 입자(CAM) 지름.  측방 주기경계,
  상/하 가동·고정벽.  초기 패킹 ~박스부피 75%.  최대속도 0.2 µm/µs.  **PID 제어로 일정
  단축 압축압력** 유지.  조성당 **독립 DEM 실현 10개** (평균±표준편차).
- CNF/PTFE(~3.4 wt%)는 DEM 도메인에서 제외 (eq 2 질량보정 `m_tot = (m_CAM+m_SE)/(1−(f_CNF+f_PTFE))`)
  — 부피기여·이온침투 영향 작다는 근거.  Hardware: Lenovo SR650 클러스터, LIGGGHTS.

### 2. FEM (§3.2) — SE 상(相) 연속체 기준 (우리에겐 없는 것)
SE 상을 디지털 추출·메싱 후 정상상태 확산 풀이:
```
∇·J = 0,  J = −σ∇φ   in Ω_SE        (3)     q = ∫_Γ J·dS   (4)
```
상부 φ₁=1V, 하부 φ₀=0V (Dirichlet), 나머지 절연(zero-Neumann).
거시: `∇·J̄=0, J̄=−σ_eff,ion·∇φ̄` (5) → `σ_eff,ion = qL/(A_dom·Δφ)` (6).  COMSOL GMRES.

### 3. RNM (§3.3) — = 우리 Kirchhoff/Holm 네트워크 솔버
SE 입자 = 노드, 접촉 = 저항.  **침투하는 SE만** 평가.  두 접촉입자 I,J:
```
R^IJ = (1/σ^I + 1/σ^J)/(4·r_c^IJ)   (7)   동일소재 →  R^IJ = 1/(2σ·r_c^IJ)   (8)
입자-전극:  R^I,0 = 1/(4σ·r_c^I,0)   (9)
```
★ **eq 8 = 우리 Holm 1967 구속저항 그대로** (`network_conductivity.py`).  접촉반경은 구-구
교차(eq 10) / 입자-경계는 변형깊이 δ에서 `r_c = √(r²−(r−δ)²)` (eq 11).
Kirchhoff 전류평형:
```
Σ_j (φ_i − φ_j)/R^IJ = 0   (12)     I_ij = (φ_i−φ_j)/R^IJ   (13)     q = Σ I_ij   (14)
σ_eff,ion = qL/(A_dom·Δφ)   (15)
```
고유 σ=1 S/cm 정규화 → **상대추세** (절대값은 bulk σ로 균일 스케일).  Birkholz 방법.

### 4. 네트워크 지표 (§3.4) — = 우리 percolation/CN/coverage 대응
```
θ_SE  = V_SE^connected / V_SE^total          (16)   SE-이용률(침투 SE 부피분율)
R̄_SE-SE = (1/N_SE-SE)·Σ R_k^1,2             (18)   평균 SE-SE 접촉저항
Z_SE-SE = (1/N_SE)·Σ z_i                      (19)   SE-SE 배위수(coordination)
```

### 5. 소재/실험 파라미터
- **Table 3 (DEM):** E_SE = **22.1 GPa**, ν_SE = 0.37, E_CAM = 161.5 GPa, ν_CAM = 0.30,
  마찰 μ(SE-SE/CAM-CAM/CAM-SE) = 0.4, 반발계수 RC = 0.4.
- **Table 1 (밀도):** ρ_CAM 4.77, ρ_SE 1.64, ρ_CNF 1.90, ρ_PTFE 2.15 g/cm³.
- **Table 4 (PSD):** SE D10/D50/D̄/D90 = 0.71/1.49/2.00/3.80 µm; CAM = 3.90/5.50/6.00/7.62 µm.
- **Table 2 (조성, wt%→vol%):** CAM:SE:CNF:PTFE = 70:27.7:2:0.3 (45.3:52.7) / 75:22.7:2:0.3
  (52.2:45.5) / 80:17.7:2:0.3 (59.5:38.3).
- **실험:** Ar 글러브박스.  cathode = 무용매 dry-film(유성 볼밀) → ~165µm 시트.  Z-type TLM
  (RELAXIS-3) EIS 피팅.  full-blocking 대칭셀(400 MPa 조립, 25 MPa 측정 stack).

---

## ★ 우리 파이프라인과의 대응 / 차이 (핵심)

| 축 | Bazzoun 2026 | 우리 |
|---|---|---|
| 소재 | LPSCl + NMC811 | **동일 ✓** |
| DEM | LIGGGHTS, Hertz spring + damping | **동일 ✓** (hooke/hysteresis) |
| 접촉저항 | `R=1/(2σ·r_c)` (eq 8) | **= Holm 1967 동일 ✓** |
| 전류해 | Kirchhoff `Σ(φi−φj)/R=0` | **동일 ✓** |
| 네트워크 지표 | θ_SE, Z_SE-SE, R̄_SE-SE | percolation f_p, CN, coverage 대응 ✓ |
| E_SE | **22.1 GPa** | 우리 real 24 ✓ (E_eff 1.35는 연화프록시) |
| σ_grain 앵커 | bulk pellet **1.02 mS/cm** | Cronau 단결정 3.0 (pellet<단결정, GB 때문 — 일관) |
| 검증 | **실험 EIS** (조성+압력) | (우리는 solver=ground truth, 실험 직접앵커 부족) |
| FEM 연속체 기준 | **있음** (COMSOL) | 없음 (우리 MPM은 역학, 전달 FEM은 안 함) |

**그들이 앞서는 점 (우리가 흡수할 것):**
- **실험 σ_eff,ion 다중검증** (조성 3 + 압력 100–400 MPa) — 우리의 "missing direct validation".
- **FEM 연속체 σ_ionic 기준** — RNM(=우리 솔버)을 FEM continuum과 대조 → 우리 솔버 신뢰도 평가틀.
- **bulk LPSCl pellet σ=1.02 mS/cm** 실측 — 우리 σ_grain 3.0(단결정) 대비 GB-포함 하한 앵커.

**우리가 앞서는 점:**
- **σ_e + σ_thermal 삼중항** (그들은 이온만).  우리 네트워크 솔버는 전자/열까지.
- **Stage-E 소성 접촉면적** (Tabor+volume), **fracture-aware Holm** (f_intact), Auerbach 균열.
- **스케일링 법칙 압축** (σ_ionic LOOCV 0.97 등) — 그들은 원시 솔버출력만.
- **MPM morphology / 소성 void-fill** — 그들은 구만 (형상변화 없음, 그들이 명시한 한계).

**방법 차이 (해석):** 그들 RNM은 **구속저항만**(field spreading 없음) → FEM/실험 대비 **약간
과소예측**, f_CAM 높을수록 심함 (80%: RNM 0.031 ≪ exp 0.065).  우리 Stage-E는 소성 접촉면적을
별도로 키워 이 과소예측을 일부 보정하는 방향 (그들에겐 없음).  σ 정규화도 다름: 그들 σ=1 S/cm
(상대), 우리 Cronau σ_grain=3.0 + Cronau(r_SE) 인자.

---

## ★ 결과 — 실험 앵커 & 추세 (우리가 쓸 데이터)

### 실험 σ_eff,ion (400 MPa, EIS) — 직접 앵커
| f_CAM (wt%) | σ_eff,ion (mS/cm) | vol% CAM:SE |
|---|---|---|
| 70 | **0.137** | 45.3 : 52.7 |
| 75 | **0.101** | 52.2 : 45.5 |
| 80 | **0.065** | 59.5 : 38.3 |
→ CAM↑ → SE침투↓ → σ↓ (우리 φ_AM/φ_SE 추세와 일치).  bulk LPSCl pellet = 1.02 mS/cm.

### σ_eff,ion vs 압력 (RNM, Fig 8a; 100·400 MPa는 본문 Δ에서 유도, 중간 디지타이징)
| f_CAM | 100 MPa | 400 MPa | Δ (본문) |
|---|---|---|---|
| 70 | ~0.068 | ~0.135 | +0.067 (+98%) |
| 75 | ~0.035 | ~0.079 | +0.044 (+126%) |
| 80 | ~0.008 | ~0.031 | +0.023 (+291%) |
→ 압력↑ → θ_SE↑, Z↑, R̄↓ → σ↑.  절대증가 최대 = 70%, **상대증가 최대 = 80%** (초기 빈약망이
가장 이득).  **~400 MPa 이후 포화** (수확체감).  ← 우리 Heckel knee(P_y 138 MPa) / 다중압력
검증과 직접 비교 가능.

### SE 입자크기 효과 (Fig 7, 400 MPa)
**작은 D̄_SE → σ_eff,ion↑** (표면적·패킹밀도↑ → 접촉수↑·θ_SE↑·Z↑; 개별 R̄는 작은접촉이라
커지지만 병렬경로 증가가 압도).  f_CAM 높으면 stiffer CAM이 응력을 SE에서 빼앗아(Ohashi)
SE 치밀화·접촉 저해 → R̄↑.  ★ 우리 "작은 SE → σ↑" 및 size=packing 결론과 **독립 일치**.

### RNM vs FEM vs 실험
- f_CAM 70%: RNM ≈ FEM ≈ 실험 (잘 맞음).  75–80%: RNM이 점점 과소 (FEM이 실험에 더 가까움).
- **RNM이 FEM 대비 32–98× 빠름** (Table 5: FEM 2551–3352 s vs RNM 26–105 s) — 우리 솔버가
  연속체 대비 갖는 속도이점과 같은 논거.  RNM은 구속저항만이라 약간 과소 = 알려진 trade-off.

---

## ★ Frame[4]/[5] 의의
- **Frame[4] (독립 교차검증):** 우리와 무관하게 보정된 **같은 소재·코드·물리**의 DEM→RNM이
  σ_ionic의 **조성·크기·압력 추세를 우리와 동일하게** 재현 + 실험으로 검증.  우리 Kirchhoff/Holm
  접근의 강한 외부 확증.
- **Frame[5] (분업):** 그들은 **이온 transport** 쪽 (= 우리 DEM 절반)에 머물고, 입자 형상변화·
  소성·σ_e·σ_thermal은 없음 — **우리 DEM의 전자/열 확장 + MPM morphology가 그들보다 넓다**.
  동시에 그들의 FEM 연속체 + 실험검증은 우리가 보강할 점.

## 실행 항목
1. **실험 앵커 도입:** σ_eff,ion 0.137/0.101/0.065 @ f_CAM 70/75/80 (400 MPa) + bulk 1.02 mS/cm
   → 우리 σ_ionic 폼/솔버의 **절대 검증점**으로 (현재 우리는 solver=ground truth라 외부 실측앵커
   부족).  단 그들 vol% CAM:SE(45/53→60/38)을 우리 φ_SE 정의로 매핑 필요.
2. **다중압력 검증:** 그들 σ-vs-P(100–400 MPa, 포화@400) ↔ 우리 Heckel P_y 138 + σ_ionic-vs-ε.
3. **RNM↔우리 솔버 대조:** 둘 다 Holm+Kirchhoff인데 그들은 구속만(과소), 우리는 Stage-E 소성면적
   보정 → 같은 구조에서 σ 차이가 Stage-E 기여를 정량화하는지 비교 연구.
4. **σ_grain 재검토(선택):** 그들 pellet 1.02 vs 우리 단결정 3.0 — GB 인자가 우리 Cronau(r_SE)에
   이미 포함되는지 점검 (이중계상 주의).
