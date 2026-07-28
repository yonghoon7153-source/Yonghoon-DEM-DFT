# Trevisanello 2021 (Adv. Energy Mater. 11, 2003400) — 다결정 vs 단결정 NCM: 입자 균열·활성표면적·Li 확산

> slug `trevisanello2021_sc_pc_ncm_cracking_diffusion` · DOI `10.1002/aenm.202003400` · type `experiment` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본 `claude/stoic-knuth-NObVQ:docs/lit_trevisanello2021_sc_pc_ncm_cracking_diffusion.md`.
> 단일-서랍 규칙(CLAUDE.md)에 따라 이관 — 그전까지 DFT webapp 목록에 안 떴다.


**인용:** E. Trevisanello, R. Ruess\*, G. Conforto, F. H. Richter, J. Janek\*,
"Polycrystalline and Single Crystalline NCM Cathode Materials—Quantifying Particle
Cracking, Active Surface Area, and Lithium Diffusion," *Advanced Energy Materials*
**2021**, *11*, 2003400. DOI 10.1002/aenm.202003400. Justus-Liebig-University
Giessen (Janek 그룹) + Center for Materials Research. Open Access (CC BY-NC-ND).
Received 2020-10-27 / Published 2021-03-24.

**소재:** Li(Ni₀.₈Co₀.₁Mn₀.₁)O₂ = NCM811 (NCM 계열). **두 형태(morphology)**:
- **PC** = Polycrystalline = 다결정 2차입자 (작은 1차결정립 응집체, 내부 grain boundary 많음).
- **SC** = Single-crystalline = 단결정 monolithic 입자 (내부 GB 없음, 균열에 강함).
- **전해질 = LIQUID** (1 M LiPF₆ in EC:DEC 1:1 vol%). **고체전해질(ASSB)이 아님.** ★ 이것이 전체 전사(transfer) 해석의 핵심.

---

## ★★★ 미션 핵심 — audit #11 (σ_e 방향성) 판정: **MIS-ATTRIBUTION (오귀속)** ★★★

> **우리 σ_electronic 생산식(Stage 22.5)의 `σ_S = 10 / σ_P = 5 mS/cm`는 "Trevisanello 2021"이라고
> 주석되어 있으나, 이 논문은 _벌크 전자전도도(σ_e)를 단결정/다결정에 대해 측정한 적이 전혀 없다._**
> 이 논문이 측정한 것은 **Li⁺ 화학확산계수 D_Li, BET 활성표면적, 전하전달저항 R_ct** 뿐이며,
> 모두 **액체전해질 셀**에서다. 전자(electronic) 벌크전도도는 본 논문 어디에도 — 본문·SI·표·그림 —
> **숫자로 등장하지 않는다.**

### 세 가지 갈림(논제에서 요구한 a/b/c) 중 답:

| 옵션 | 판정 |
|---|---|
| (a) 문헌적으로 정확 (σ_S>σ_P 전자전도) | ✗ **아님.** 이 논문은 전자전도 σ를 SC/PC로 측정하지 않았다. |
| (b) **오귀속** (논문은 확산/표면적 논문, 전자 σ가 아님) | ✅ **이것이 정답.** 우리 식의 "전자전도" 숫자(10/5 mS/cm)와 그 출처(Trevisanello)는 **잘못 연결**되어 있다. 논문은 σ_e를 다루지 않는다. |
| (c) 실재하는 소재의존 방향성 (#266 W-doped poly가 합법적으로 뒤집음) | △ **부분적으로 맞음** — 단, 이 논문이 그 근거가 아니다. "SC vs PC 전자전도 방향"은 **이 논문 밖에서** 결정해야 할 열린 문제다. 이 논문은 그 질문에 **무관(silent)**하다. |

### 더 정밀하게 — 우리가 잘못 가져온 것 vs 이 논문이 실제로 주는 것

**우리 식의 두 'Trevisanello 인자':**
1. `σ_S = 10, σ_P = 5 mS/cm` (전자전도 엔드포인트, "단결정이 다결정의 2배") — **이 논문 근거 없음(오귀속).**
2. `NCM(r) = 1/(1 + (r/2µm)^1.5)` (입자크기/내부GB 보정) — **부분적으로 정당화됨** (단, _전자전도_가 아니라 _확산·동역학_ 메커니즘으로; §3-2 참조).

**이 논문이 실제로 확립하는 것** (전자전도가 아닌 동역학/확산):
- SC는 사이클 중 **균열이 거의 없다**(monolithic, crack-free) → 내구성·CE·장수명에서 SC 우위.
- PC는 1차 충전 중부터 **균열 발생** → **액체전해질이 균열로 침투** → 활성표면적 ↑, R_ct ↓, **겉보기 D_Li가 1자릿수 이상 ↑** (액체 침투의 **인공물**, 겉보기 `D̃_Li^app`).
- 액체 침투 효과를 제거한 **본질적(intrinsic)** D_Li는 SC·PC가 **동일**(같은 조성·같은 1차결정 transport).

### ASSB로의 전사(transfer) — ★ 부호가 뒤집힌다 (액체 ≠ 고체)
이 논문의 중심 메커니즘 — "PC 균열 → **액체** 침투 → 표면적↑·저항↓" — 은 **액체 고유**다.
고체전해질(우리 LPSCl)은 **내부 균열을 채울 수 없다**:
- 액체 셀: 균열 = (액체 침투로) **이득**(표면적↑, R_ct↓, 동역학↑). → 이 논문의 핵심 발견.
- ASSB: 균열 = **손실**(접촉상실 → 저항↑, dead-AM↑). **부호 반대.**

⇒ ASSB에서는 **SC의 균열저항이 내구성(durability) 승리**지만, 동시에 **SC의 낮은 활성표면적이 동역학 손실**일 수 있다 — 액체 케이스와 정반대의 트레이드오프. 우리 fracture/Auerbach 채널 + dead-AM은 이 **고체측 부호(균열=손실)**를 이미 올바르게 모델링하고 있고, 이 논문은 그 **반대 부호(액체)** 케이스이므로 — 전사할 것은 **본질적 CAM 기하(SC=monolithic·crack-free vs PC=내부GB·균열성)** 와 **SC/PC 동역학 추론**뿐, **절대 transport 값이나 액체-침투 메커니즘이 아니다.**

### 권고 (Phase 3 전):
- **σ_AM 엔드포인트(σ_S/σ_P)를 material-specific INPUT으로 전환할 것.** 현재 LOCKED된 10/5 mS/cm은
  (i) 출처가 잘못되었고(이 논문은 전자 σ를 안 줌), (ii) #266의 W-doped 다결정 NCWA가 반대 방향(poly>single)을
  실측했으므로 — 단일 LOCKED 상수는 소재 무관성을 위반한다. σ_AM(single), σ_AM(poly)를 **소재·도핑별 입력**으로
  받고, "단결정>다결정"이라는 부호 가정을 식에서 제거.
- `NCM(r)` 인자는 **유지 가능하되 의미를 재명명**: 전자전도용 GB감쇠가 아니라 **확산길이/활성표면적 보정**으로
  물리적 근거를 옮긴다(§3 참조). β=1.5는 이 논문의 정량적 fit이 아니므로(아래) "Trevisanello 정신을 따른
  경험 지수"로 정직하게 표기.

---

## 1. 동기 / 핵심 질문 (Intro)

고-Ni NCM(NMC811 등)은 고용량·고에너지지만 **빠른 성능열화**가 문제. Intro가 나열하는 열화 기구
(우리 채널과 매핑):
1. **고전위·저SOC에서의 kinetic limitation** (느린 Li 확산) → 우리 D_Li / 동역학.
2. **CEI(cathode-electrolyte interphase) 성장** → 우리 ASR/계면.
3. **비가역 상전이**(전기화학적 불활성상으로) → 우리 dead-AM.
4. **2차입자 균열에 의한 이온/전자 접촉상실** → ★ 우리 **fracture(Auerbach) + dead-AM** 채널.

기존 완화책: 2차입자 코팅, 도핑, core-shell, 액체전해질 첨가제. 최근의 큰 진전 = **SC(단결정) NCM** —
monolithic 구조라 균열이 거의 없어 부반응·접촉상실을 줄이고 CE를 크게 올림.

**그러나** SC vs PC의 **rate capability(율속)** 비교는 드물었고, SC가 (입자가 크고 표면적이 작아)
**더 느린 동역학**을 보인다는 보고도 있음. NCM의 느린 Li 확산이 방전 중 relithiation을 방해 → 재료
활용·접근가능 용량을 떨어뜨림.

**이 논문의 질문:** PC와 SC NCM811의 **D̃_Li(Li 화학확산계수)**, **R_ct(전하전달저항)**, **활성표면적**이
입자 크기·형태에 따라 어떻게 다른가, 그리고 그것이 **셀 성능**(용량·율속·CE)에 어떻게 연결되는가.

**선행연구(ref [21], 같은 그룹 Ruess 2020):** 1차 충전 중 형성된 microcrack 안으로의 **액체 침투**가
**겉보기 D_Li를 높이고 Li 확산 경로를 단축**시킴 — 활성표면적↑·유효입자크기↓와 일치. **"이 효과는 기계적으로
단단한 고체전해질로는 일어나지 않으며, 새로 생긴 공간을 채울 수 없다"** — 본 논문이 이를 명시 (★ ASSB 전사 경고의 출처).

---

## 2. Section-by-section 결과 (모든 숫자 포함)

### 2.1 Morphological Evolution (형태 진화) — Figure 1, Scheme 없음

**알려진 화학-기계 효과:** 고-Ni NCM은 **>75% Li 추출 시** 단위격자 부피의 **계단형 감소**가 일어나,
1차결정립들이 서로 다른 방향으로 수축 → 내부 응력 빌드업 → 1차입자 분리 + microcrack 성장. 2차입자에서는
**1차 충전(first charge)부터** 균열이 관찰됨. SC는 이런 식의 영향을 받지 않으며, **1000 사이클 후에도** major
crack 없음 (ref [18]).

**Figure 1 (FIB-SEM 단면, pristine → 3.8 V → 4.2 V):**
- (a–d) **PC**: pristine(a)는 치밀, 1차결정 사이 간극 없음. **3.8 V 충전(b)**에서 PC 입자 내부에 균열이
  **보이기 시작**, **4.2 V(c,d)**에서 균열이 더 심해짐 (빨간 화살표). → "bulk" cathode sheet에서도
  isolated 입자와 동일한 1차-충전 균열 발생 확인.
- (e–h) **SC**: 충전 전후 차이 **없음** — monolithic 입자의 기계적 안정성 확인. (고전위에서는 SC도 균열
  가능하나 본 연구 전위창에서는 안 보임. 단, 산소손실에 의한 결정구조 손상은 Li 확산을 저해할 수 있음.)

**우리 매핑:** PC의 "1차결정 다른방향 수축 → 내부응력 → 균열" = 우리 fracture 채널의 **다결정 내부GB가
파괴 시드**라는 물리. SC의 crack-free monolithic = 우리 **작은 AM_S(F/P_c<1, 균열 안 함, #285)**와
정성적으로 일치 (단, 그쪽은 ASSB·크기효과, 이쪽은 결정성효과 — 다른 메커니즘이 같은 "crack-free" 표현형).

### 2.1 (cont.) 표면적 측정 — Figure 2 + Figure S1, S3

**방법:** Kr physisorption(저표면적용 BET). 서로 다른 cutoff 전위까지 충전한 cathode를 회수해 BET 표면적 측정.

**Figure 2a (PC Kr isotherm):** pristine → 3.7 → 3.8 → 3.9 → 4.0 → 4.1 → 4.2 V로 갈수록 흡착부피(따라서
BET 표면적) **단조 증가**. **Figure S1**: SC는 거의 변화 없음.

**Figure 2b (BET 표면적 S_BET vs 전압):** ★ 핵심 숫자
- **PC**: pristine **≈0.2 m²/g** → **4.2 V 충전 후 ≈1.4 m²/g** (약 **7배 증가**). 증가는 이미
  **<3.9 V(저전위)부터** 시작 — 내부응력이 낮을 전위에서도 — in-situ SEM·acoustic emission이 저전위
  균열을 확인(ref [28,31,32]).
- **SC**: pristine **≈0.2 m²/g**(회색 점선, "Pristine SC")로 충전 후에도 거의 불변.

**(Experimental Section의 BET 절대값, spherical 기하 가정):** "표면적은 PC 0.17, SC 0.84 m²/g"
— ★ 주의: 이 문장은 **pristine powder의 PSD로부터 spherical 기하로 계산한 기하학적 표면적**이다
(SC가 PC보다 4배 큼 — SC가 작은 입자라서). Fig 2b의 **측정 BET**는 pristine PC≈SC≈0.2 m²/g (둘 다 binder/carbon
기여 차감). 즉 **기하 표면적(0.17/0.84)과 측정 BET(≈0.2/≈0.2)는 다른 양**이며, SC의 측정 BET가
기하 예측(0.84)보다 작은 것은 "spherical 가정의 과소추정"으로 본문이 명시. **혼동 금지.**
- pristine cathode의 carbon/PVDF 기여 = 상수 0.76 m²/g로 차감 (casted PC 0.96 → 0.2).

**Figure S3 (PC 표면적 2가지 방법 교차검증):** BET (다이아몬드) vs Warburg계수비로 구한 표면적
(파란 육각형, 식 S1). S_BET(t=0) = **1.3 m²/g** (4.2 V BET값)으로 고정. 두 방법이 잘 일치 →
PC 1차충전 중 활성표면적 유의 증가 확정.

### 2.2 Li Diffusion Coefficient D̃_Li — Figure 3, Figure 4 (★ 본 논문의 메인 결과)

**파라미터 정의:** D̃_Li = Li 화학확산계수 = CAM 내부 Li 수송을 기술하는 핵심량(표면↔core).
실험적 접근: GITT/relaxation으로 측정. 핵심 측정량 = **Warburg 계수 Z_W**, 그로부터 D̃_Li 추출.

**식 (1) (반무한 확산, relaxation 분석):**
```
V_OC(t) ≈ V_0 − (2/√π)·I·Z_W·[√t − √(t/τ)]      with   Z_W = WRT / (z³F²·A·c_0·√D̃_Li)
```
- W = thermodynamic enhancement factor = ∂ln(a_Li)/∂ln(c_Li) (V_0 vs c_Li에서 계산, morphology 무관, Fig S2b).
  **단일상 solid-solution일 때만 유효** — 2상 공존(plateau)이면 W→0이라 식(1) 사용 불가. 본 NCM811은
  대부분 전위에서 단일상이나 고전위 H2/H3 공존영역(x≈0.3, ≈4.2 V)에서 W→0 → 그 구간 D̃ 신뢰도 낮음.
- A = BET 표면적, c_0 = 폴라리제이션 전 Li 농도, z·F = 전하·패러데이상수.

**Figure 3 (Z_W vs x in LiₓNi₀.₈Co₀.₁Mn₀.₁O₂):**
- (a) **PC**: 1차 충전 중 Z_W는 x→0.6(≈3.8 V)까지 감소. 그 후 **방전에서 PC의 Z_W는 낮게 유지**(증가 안 함)
  → **비가역 변화**(균열) 발생 신호.
- (b) **SC**: 충전·방전이 **완전히 가역적**(같은 곡선) → SC 입자가 사이클 중 **온전(intact)**.
- ★ Z_W가 낮다 = (식1로) 활성표면적 A↑ 또는 D̃↑. PC의 영구적 Z_W 감소 = 표면적 증가(균열·침투)의 직접 증거.

**Figure 4 (겉보기 확산계수 D̃_Li^app vs x):** ★ 1자릿수 이상 차이의 그림
- **PC**: 1차충전 시작 시 PC·SC 비슷한 D̃ → 충전 진행하며 Li vacancy 증가로 D̃↑(ab-initio·NMR과 일치).
  PC의 **방전 D̃^app**은 충전보다 **최소 1자릿수(>10×) 높음**. ← "Apparent increase due to higher area" (화살표).
- **SC**: 충·방전 가역(같은 추세), PC만큼의 비대칭 없음.
- 두 형태 모두 **방전 시 x≈0.5(50% 활용)에서 D̃^app 최고**.

**Figure 4 해석 (§2.2.2):** Kr-physisorption이 보인 표면적 7배 증가는 식(1)의 **A²(또는 quadratic)
관계**상 D̃^app를 약 **50배** 올린다 — Fig 4의 "방전이 충전보다 ≥1자릿수 높음"과 정량 일치. ⇒ PC의
충·방전 D̃^app 불일치는 **morphology(표면적 변화)에 의한 것**이지 transport 기구 변화가 아님(조성 동일, 2상영역 없음).
**액체전해질이 균열 후 침투해 표면적을 늘린 것만이** 이 높은 겉보기 D̃를 설명. → ★ **`D̃_Li^app`은
겉보기값**이며(상수 A 가정으로 추출), 실제 본질 D̃는 PC·SC 동일.

**문헌 본질 D̃_Li 정렬(§2.2.2):** crack 없는 형태들에서 측정된 D̃_Li는 모두 **같은 범위**:
- Li₁.₂Ni₀.₈Co₀.₂O₂ thin film: 1×10⁻¹¹ cm²/s
- Li₁.₂Ni₀.₈Co₀.₁Mn₀.₁O₂ single crystal: 7×10⁻¹¹ cm²/s
- 그 single crystal + **LiPS₅Cl(고체전해질) 접촉**: **6×10⁻¹² cm²/s** ← ★ ASSB 맥락의 동일 범위 값
- 본 연구 **SC NCM**: 2×10⁻¹¹ cm²/s (x=0.4, ≈3.9 V) — 모두 같은 범위. → 본질 D̃는 형태 무관.

### 2.3 Charge-Transfer Resistance R_ct^NCM — Figure 5, Scheme 1

**방법:** 3전극 PEIS(potentiostatic EIS). 등가회로(Fig 5a): "bulk" Ohmic(separator) + anode CT/SEI +
**cathode CT(R_ct^NCM)** + Warburg(W) + CAM differential capacitance. 3전극으로 Li|LE anode 기여 분리(Fig S5,S6).

**Figure 5 (Nyquist):** (b) PC 3.65 V 적합 예, (c) PC 충/방전, (d) SC 충/방전.

**R_ct^NCM 핵심 숫자 (PC, 1차 충→방):**
- 충전 시작 **≈70 Ω** → 방전 시 **≈15 Ω**으로 **붕괴(collapse)**. ← BET 표면적 증가와 일치
  (균열로 액체 침투 → 활성 계면적↑ → R_ct↓). **이전 보고 ref [21]과 일치.**
- 이는 단지 표면적 때문만 아니라 **CAM 내부 확산길이 단축**(균열로 짧은 경로) 때문이기도 함.

**SC의 R_ct(§2.3.2):** 4.2 V 충전 후 SC의 R_ct는 PC와 매우 다르게 거동 — SC는 **고전위 표면열화(surface
degradation)·전해질 분해**로 R_ct가 **증가**(붕괴 안 함). → SC 셀의 낮은 방전용량을 설명(아래).

### 2.4 Diffusion Overpotential ΔV_diff — 식 (2)

**식 (2) (유한확산 영역 과전위):**
```
ΔV_diff(c_Li) ≈ (1/3)·I·Z_W·√(L²/D̃) = (1/3)·(I/F²)·(RT)·W·(L/(c_Li·D̃))·(L/A)
```
- L = 확산층 두께, A = charge-transfer 활성면적. **두 기여**: ① 국소 Li 수송(c_Li, W, D̃) ② **L/A 비**
  (형태/입자크기 — 표면적·확산경로). 균열·침투 → L/A↓(작은 유효입자, 큰 표면적) → 과전위↓.
- SC는 액체침투 없음(장수명에도) → 과전위 더 큼.

⇒ ★ 핵심 트레이드오프 명문화: PC 균열은 **ΔV_diff와 R_ct를 낮춰** 율속·용량에 **도움**(액체에서). SC는
crack-free라 **본질적으로 느린 NCM 확산이 율속한계**가 됨.

### 2.5 Cycling — Scheme 1, Figure 6 (★ 가장 반직관적 결과)

**Scheme 1 (kinetic test):** PC 셀 2개를 각각 **LV(3.7 V cutoff, 균열 안 생김)** 와 **HV(4.2 V cutoff,
균열 생김)** 로 충전. 동일 cathode sheet(≈1.6 mAh/cm²), CC + CP(2.6 V) 방전으로 최대 Li 인터칼레이션 보장.

**Figure 6 (PC, 1~6 사이클 전압-용량):**
- **1st cycle (a):** HV는 충전 204 mAh/g·방전 183 mAh/g. LV(3.7 V)는 충전 18 mAh/g(CC) + 4 mAh/g(CP) =
  방전 200 mAh/g 가능. **1st HV 비가역손실 ~4 mAh/g(≈2%)** — non-Faradaic 무시 가능.
- **2nd cycle (b):** 둘 다 3.7 V CC로만 충전. **HV 57 mAh/g vs LV 27 mAh/g** 전달 — ★ 같은 충전조건인데
  **균열된(HV) 셀이 더 많은 용량 접근.** CE: LV **45%** vs HV **71%**. CP step 추가 용량 LV 8 / HV 11 mAh/g.
- **3rd (c):** 둘 다 40 mAh/g 충전. HV가 여전히 LV보다 큰 방전용량. CE: LV 28% / HV 40%(galvanostatic step 후);
  전체 CE LV 60% / HV 72%.
- **4th (d):** LV 셀도 4.2 V까지 완전사이클 → 균열 형성. 이후 LV는 HV처럼 거동.
- **5th, 6th (e,f):** LV·HV 매우 유사 (4th에서 LV도 균열났으므로). CE LV 47/40% vs HV 65/62%.
- **전체 CE (CP step 포함, 1st):** LV **95%** / HV **92%**.

**해석:** **균열되지 않은(LV) PC**가 **균열된(HV) PC보다 율속·용량이 나쁘다** — composition
Li₀.₉Ni₀.₈Co₀.₁Mn₀.₁O₂ 부근에서 **확산 과전위가 가파르게 증가**해 (cutoff 도달 빨라) 용량 제한. 균열 셀은
표면적↑로 이를 완화. **모폴로지(균열 유무)가 조성보다 율속에 더 큰 영향.** Whittingham et al.(ref [7])의
같은 소재 저-D̃(<3.8 V) 보고와 일치. 단 이는 **비가역 용량손실이 아니며**(저전위 holding으로 상당부분 회수).

**§2.5.2 SC vs cracked PC:** SC NCM은 **cracked PC의 ~서브µm 1차입자 앙상블처럼 거동**(고표면적·짧은 확산경로).
문헌·본 결과: **SC의 이상적 크기는 응용 의존** — 작은 결정 = 빠른 율속, µm급 = 장수명. Kim et al.(ref [63])은
1차입자 aspect ratio·크기·도핑 최적화로 고-Ni NCM 확산한계 극복: **aspect ratio 큰 100 nm 입자 = 230 mAh/g·1st
CE 98%**, 결정립 클수록 저-SOC 동역학한계로 방전용량↓(본 결과와 일치).

---

## 3. ★ 우리 모델 인자별 정밀 대조 (NCM(r), σ_S/σ_P)

### 3-1. σ_S = 10 / σ_P = 5 mS/cm (전자전도 엔드포인트) — **오귀속, 출처 없음**

- 우리 코드(`scripts/generate_fitting_report.py`)는 "Trevisanello 2021 실측(단결정 vs 다결정 NMC811):
  ratio ≈ 2.0× 일치"라 적고 있으나, **본 논문에 단결정/다결정의 전자전도 σ 측정은 없다.** "ratio 2×"가
  대응될 만한 본 논문의 2× 양은 **기하 표면적**(SC 0.84 / PC 0.17 m²/g ≈ 5×, 방향도 우리와 반대로 SC가
  더 큼) 또는 R_ct·D̃^app(균열로 변하는 동역학)뿐 — **전자전도가 아님.**
- 절대 단위도 우연: 우리 σ_S/σ_P는 mS/cm(전자전도), 이 논문 D̃는 cm²/s(확산). **차원이 다른 양.**
- ⇒ "단결정 σ_e > 다결정 σ_e (2×)"라는 우리 가정은 **이 논문이 뒷받침하지 않으며**, 출처를 이 논문으로
  단 것은 명백한 오귀속. 전자전도 엔드포인트는 **별도 문헌**(예: 실제 σ_e 측정 논문)이나 **소재별 입력**으로 대체.
- #266(Oh 2026)이 측정한 **W-doped 다결정 NCWA σ_e=13.7 ≫ 단결정 NCM σ_e=2.45**(poly>single)는
  본 논문과 **모순되지 않는다** — 본 논문은 그 질문에 무관하기 때문. 두 데이터는 "전자전도 SC/PC 방향은
  소재·도핑 의존"임을 시사하며, 단일 LOCKED 부호(SC>PC)는 폐기 대상.

### 3-2. NCM(r) = 1/(1 + (r/2µm)^1.5) — **부분 정당화 (단, 의미는 '확산/표면적', '전자GB'가 아님)**

우리 구현(`scripts/network_conductivity.py:64-77`): **AM_P(다결정 큰 입자)에만** 적용
`σ_eff = σ_grain/(1+(r/2µm)^1.5)`, AM_S(단결정)는 1.0(감쇠 없음). r0=2 µm, β=1.5.

**이 논문이 지지하는 부분(물리 방향은 맞음):**
- "**큰 2차입자(>5 µm) PC는 작은 SC보다 표면적·유효입자크기가 불리** → 더 큰 과전위·낮은 율속" (§2.5.1).
- D̃·표면적이 **크기 의존**이며 **큰 다결정이 동역학적으로 불리**하다는 정성 방향은 본 논문 결론과 일치.
- **PSD(Fig S10)**: SC 입자반경 ≈**0.3–1.2 µm**(중앙 ~0.6–0.7 µm), PC 입자반경 ≈**1–5 µm**(중앙 ~2 µm).
  → 우리 r0=2 µm는 **PC PSD 중앙과 정합**(우연이지만 물리적으로 그럴듯). AM_S(단결정)에 감쇠 0은
  "SC는 내부GB 없어 손실 작다"는 본 논문 정성과 일치.

**이 논문이 지지하지 _않는_ 부분(정직한 한계):**
- **β=1.5라는 지수의 정량 fit이 본 논문에 없다.** 본 논문은 `1/(1+(r/r0)^β)` 형태의 식을 제시하지 않는다.
  β=1.5는 우리 σ_e 회귀에서 corpus-confirmed된 값(CLAUDE.md: locked-exponent screen에서 1.5 승,
  1.75는 −0.0008 noise)이지 Trevisanello의 측정값이 아니다. → "Trevisanello β=1.5"는 **출처 과장**.
  정직한 표기 = "Trevisanello가 보인 **'큰 다결정 = 내부GB·표면적 페널티'** 정신을 따른 경험 지수(β=1.5,
  우리 corpus fit)".
- 더 근본적으로, 본 논문의 크기효과는 **전자전도 GB감쇠가 아니라 Li확산경로/활성표면적** 효과다.
  우리가 이 인자를 **전자(σ_e) 식**에 GB감쇠로 넣은 것은 **메커니즘 오배치**일 수 있다 — 본 논문에 따르면
  크기효과는 **이온/확산** 쪽 물리. (다만 다결정 내부 GB가 전자전도에도 직렬저항을 더하는 것은 일반론으로
  타당 — 본 논문이 그것을 측정하지 않았을 뿐.)

**권고:** NCM(r) 인자는 **유지하되**, ① 출처를 "본 논문 정신(큰 PC = 동역학/내부GB 불리) + 우리 corpus
fit β=1.5"로 **정직하게 재명명**, ② 가능하면 σ_e가 아니라 **확산/표면적·dead-AM** 쪽에서 작동하도록
물리적 위치를 재검토.

### 3-3. ASSB 전사 일관성 (우리 fracture / 작은-AM_S와의 정합)
- SC = monolithic·crack-free = 우리 **작은 AM_S(F/P_c<1, 균열 안 함, #285)** 와 **표현형 일치**. 단,
  이 논문 SC는 _결정성_(내부GB 없음)으로 균열 안 하고, 우리 AM_S는 _작은 크기_(Auerbach 임계하중↑)로
  균열 안 함 — **다른 메커니즘, 같은 "crack-free"**. 우연한 일치이나 **방향은 같다**: SC/작은-AM = 내구성 우위.
- ASSB 부호: 균열 = 손실(접촉상실). 본 논문(액체) = 균열이 이득. → 우리 모델이 **고체 부호를 올바르게**
  쓰고 있음을 본 논문이 **반대 케이스로 교차확인**.

---

## 4. 모든 그림·SI 표 요약 (텍스트 + SI 기반)

| 항목 | 내용 | 우리가 쓸 것 |
|---|---|---|
| **Fig 1** | FIB-SEM 단면 pristine/3.8/4.2 V. PC(a-d) 균열 발생, SC(e-h) 무변화 | SC=crack-free, PC=1차충전부터 균열 (fracture 시드=내부GB) |
| **Fig 2a** | PC Kr isotherm, 전위↑→흡착부피↑ | PC 표면적 증가의 직접 데이터 |
| **Fig 2b** | S_BET vs V: PC 0.2→1.4 m²/g(7×), SC ≈0.2 불변 | ★ PC 7배 표면적증가 / SC 불변 |
| **Fig 3** | Z_W vs x. PC 비가역(방전 낮음), SC 가역 | PC 균열의 비가역 신호 / SC intact |
| **Fig 4** | D̃_Li^app vs x. PC 방전이 충전보다 >10×, 둘 다 x≈0.5 최고 | ★ D̃^app 1자릿수↑ = 표면적(균열·**액체침투**) 인공물 |
| **Fig 5** | Nyquist + 등가회로. PC R_ct 70→15 Ω 붕괴, SC 증가 | R_ct: PC 균열로↓(액체), SC 표면열화로↑ |
| **Fig 6** | PC LV vs HV 1~6 사이클. HV(균열)가 LV(무균열)보다 용량·CE↑ | ★ 모폴로지(균열)>조성; 1st CE LV95/HV92% |
| **Scheme 1** | kinetic test 절차(LV 3.7V/HV 4.2V) | 균열 유무 제어 실험설계 |
| **Fig S1** | SC Kr isotherm 거의 불변 | SC 표면적 안정 |
| **Fig S2** | (a) 1st 충방전 곡선(20 mA/g, 2.6-4.3 V; SC 방전용량 낮음=고전위 표면열화·R_ct↑). (b) W(thermo factor) | W→0 at H2/H3 → 그 구간 D̃ 신뢰도↓ |
| **Fig S3** | PC 표면적 BET vs Warburg비, S_BET(0)=1.3 m²/g 고정, 일치 | 표면적증가 2법 교차검증 |
| **Fig S4,S5,S6** | 3전극 polarization/relaxation·Nyquist(Li|LE 분리) | 방법(anode 기여 제거) |
| **Fig S7** | SC LV/HV 사이클 — 1st 차이가 2nd 용량에 영향 안 줌(SC는 균열無) | SC: 균열 효과 없음 대조군 |
| **Fig S8 + Table S1** | SC NCM811 XRD Rietveld: a=2.8746 Å, c=14.203 Å, c/a=4.941, V=101.64 Å³, Ni/Li disorder 2.3% | SC 상순도·격자 |
| **Fig S9** | SEM: PC(구형 응집체) vs SC(다면체 단결정) | 형태 |
| **Fig S10** | PSD(누적): **SC 반경 0.3-1.2 µm, PC 반경 1-5 µm** | ★ NCM(r) r0=2µm가 PC 중앙과 정합 |

---

## 5. 실험 조건 (Experimental Section — 정직한 한계 경계)

- **SC 합성:** 공침(NaOH+NH₄OH, pH 9.5-10.5, 60°C) → Ni₀.₈Co₀.₁Mn₀.₁(OH)₂ + Li₂CO₃ (Li/TM 2.1) →
  Ni₀.₈Co₀.₁Mn₀.₁(OH)₂ 소성(O₂, 150°C→875°C 6h hold) → 분쇄·초음파로 응집 분리 → Li₂CO₃ 제거(원심·600°C).
  PC 2차입자 = **Volkswagen AG 제공**. XRPD·SEM 확인.
- **표면적(기하, spherical 가정):** PC **0.17**, SC **0.84 m²/g** (★ pristine PSD 기반 계산값; Fig 2b의
  측정 BET와 다른 양).
- **전극:** 90:5:5 (NCM:PVDF Solef5130:Super P) in NMP, doctor blade(250 µm gap) on Al, 120°C 진공.
  **CR2032 coin**, Li metal anode(200 µm, ⌀14), 유리섬유 separator(⌀16), cathode **≈8 mg_NCM/cm²**(⌀12),
  **50 µL 액체전해질** 침투. **1 M LiPF₆ EC:DEC 1:1 vol%.**
- **3전극:** 금도금 텅스텐 wire reference(≈8 R·m²), 25°C.
- **전기화학:** GITT/relaxation으로 D̃_Li 측정. **2 h 충전(4 mA/g_NCM) + 2 h relaxation(OCV)** 반복,
  각 step 후 EIS(potentiostatic, 10 mV, 1 MHz-1 mHz, 5 pts/dec). 4.3 V까지 충전 후 4 mA/g로 2.6 V 방전.
- ★ **전부 액체전해질 LIB. 고체전해질·ASSB 데이터 없음.** D̃의 한 정렬값(SC NCM+LiPS₅Cl 6×10⁻¹² cm²/s)만
  문헌인용으로 ASSB 맥락에 등장.

---

## 6. 비교 vs 우리 DEM+MPM (focused §)

| 축 | 이 논문 (NCM, 액체 LIB) | 우리 DEM+MPM (LPSCl ASSB) | 정합/긴장 — 진짜 vs method-artifact |
|---|---|---|---|
| **σ_e 엔드포인트 σ_S/σ_P** | **측정 안 함**(확산·표면적·R_ct만) | σ_S=10>σ_P=5 mS/cm LOCKED "Trevisanello" | ★ **오귀속.** 논문에 전자 σ 없음. → 소재별 INPUT화 권고 |
| **NCM(r) GB보정** | 크기효과는 **확산/표면적** 쪽(다결정 불리 정성 ✓), β값·식은 제시 안 함 | σ_e식에 1/(1+(r/2)^1.5), AM_P만 | 방향 ✓, 지수·메커니즘 위치는 **우리 corpus fit**(논문 정신 차용) |
| **SC vs PC 균열** | SC crack-free, PC 1차충전부터 균열(내부 GB 시드) | fracture(Auerbach)+dead-AM; AM_S 균열 안 함(#285) | 표현형 ✓ — 단 SC=결정성 / AM_S=크기, 다른 메커니즘 |
| **균열의 부호** | 균열=**이득**(액체 침투→표면적↑·R_ct↓·D̃^app↑) | 균열=**손실**(접촉상실→σ↓, dead-AM↑) | ★ **부호 반대(액체≠고체).** 전사 금지. 우리 고체부호가 옳음을 반대케이스로 확인 |
| **본질 D_Li** | SC≈PC 동일(2×10⁻¹¹ cm²/s; +LiPS₅Cl 6×10⁻¹²) | (확산은 σ_ionic쪽 영역) | 본질 transport는 형태무관 — 우리 σ_e의 SC/PC 부호 가정과 무관 |
| **표면적 SC vs PC** | 기하: SC 0.84 > PC 0.17 m²/g (SC가 작아 더 큼!) | coverage(Tabor/Hertz) 별도 | ★ SC가 표면적 **더 큼** → 우리 "SC=고σ_e" 가정과도 **방향 충돌** 가능 |
| **모폴로지>조성 (율속)** | 균열 유무가 조성보다 율속 지배 | — | 정성 통찰: 미세구조가 transport 1차 결정인자 (우리 철학과 일치) |

**전사 규칙(엄격):** NCM(LIB, **액체**) ≠ LPSCl(ASSB, **고체**). 가져올 것 =
① **본질 CAM 기하**(SC monolithic·crack-free vs PC 내부GB·균열성),
② **SC/PC 동역학 추론 방향**(큰 다결정 = 확산/표면적 불리),
③ **모폴로지가 율속 지배**라는 정성 통찰.
**절대 가져오지 말 것** = 액체-침투 메커니즘, 절대 transport 값, "균열=이득" 부호, **그리고 "전자 σ_S>σ_P"라는
존재하지 않는 결론.**

---

## 7. 미니 용어집 (technique glossary)

- **D̃_Li (chemical diffusion coefficient):** 화학퍼텐셜 구배 하 Li의 collective 확산계수(self-diffusion ×
  thermodynamic factor W). transport + 열역학 결합량. cm²/s.
- **D̃_Li^app (apparent):** 상수 표면적 A를 가정해 추출한 **겉보기**값. PC에서는 균열·액체침투로 A가 실제로
  변하므로 **과대평가**(Fig 4의 방전 >10× 충전이 그 인공물).
- **Z_W (Warburg coefficient):** EIS/relaxation의 확산 임피던스 계수. Z_W ∝ 1/(A·c_0·√D̃). 작을수록
  표면적·확산↑.
- **W (thermodynamic enhancement factor):** ∂ln(a_Li)/∂ln(c_Li). 농도→활동도 변환. 단일상에서만 유의,
  2상 공존(plateau)에서 W→0.
- **R_ct (charge-transfer resistance):** 전극|전해질 계면 전하전달 저항(EIS 반원). 활성면적↑→R_ct↓.
- **BET / Kr physisorption:** 저표면적 분말의 비표면적 측정(Kr이 N₂보다 저면적 민감). m²/g.
- **GITT / polarization-relaxation:** 짧은 정전류 펄스 + OCV relaxation으로 SOC별 D̃ 측정.
- **PC / SC:** Poly- / Single-crystalline. PC = 작은 1차결정 응집한 큰 2차입자(내부GB·균열성);
  SC = 내부GB 없는 monolithic 단결정(균열저항).
- **CEI:** Cathode-Electrolyte Interphase. 고전위 분해 부산물 계면층.
- **H2/H3 phase:** 고-Ni 층상의 고전위 상(>4.2 V, x≈0.3). interlayer spacing 좁아 Li 확산 저해, 공존영역서 W→0.

---

## 8. 정직한 한계 (이 논문 자체 + 전사)

1. ★ **전자전도(σ_e) 측정 부재.** 우리 σ_S/σ_P "전자전도 엔드포인트"의 출처로 부적합 — 오귀속.
2. ★ **액체전해질 LIB.** 중심 메커니즘(균열→침투)이 ASSB로 전사 불가(부호 반대).
3. **D̃^app은 겉보기값.** PC의 1자릿수 우위는 표면적 인공물; 본질 D̃는 SC≈PC.
4. **NCM(r) 식·지수는 본 논문 산물 아님.** 크기효과 _방향_만 지지; β=1.5는 우리 corpus fit.
5. **고전위 신뢰구간:** H2/H3 공존(x≈0.3, ≈4.2 V)에서 W→0 → 그 구간 D̃ 신뢰도 낮음(논문 명시).
6. **표면적 두 정의 혼동 주의:** 기하(0.17 PC/0.84 SC) vs 측정 BET(≈0.2/≈0.2) — 다른 양.
7. **NMC811 한정·NCM 계열.** LPSCl SE는 D̃ 한 인용값으로만 등장.

---

## 9. 우리 작업에 가장 날카로운 통찰 (Top 3)

1. ★ **audit #11 = 오귀속.** 우리 `σ_S=10/σ_P=5 mS/cm "Trevisanello"` 전자전도 엔드포인트는 **이 논문에
   근거가 없다**(논문은 D_Li·표면적·R_ct만, 전자 σ 없음). #266이 본 우리와 반대 방향(poly>single)은 이 논문과
   **모순 아님** — 이 논문이 그 질문에 무관하기 때문. → **σ_AM 엔드포인트를 소재·도핑별 INPUT으로 전환**하고
   "단결정>다결정 σ_e" 부호 가정 + 출처 인용을 **제거/수정**. Phase 3 전 최우선 정리.

2. ★ **NCM(r)은 살리되 의미 재배치.** 본 논문은 "큰 다결정 = 표면적·내부GB·확산경로 불리"라는 **정성 방향**을
   확실히 준다. 식 `1/(1+(r/2)^1.5)`·β=1.5는 **우리 corpus fit**이므로 정직하게 재명명, 그리고 이 인자가
   **전자 GB감쇠**보다 **확산/활성표면적/dead-AM** 물리에 더 맞을 수 있음을 검토(본 논문은 크기효과를 이온/확산
   쪽에 둠).

3. ★ **균열 부호가 우리 모델을 교차확인.** 본 논문(액체)에서 균열=이득, 우리(ASSB)에서 균열=손실 — **부호가
   반대**라는 사실 자체가 우리 fracture/Auerbach 채널이 **고체 부호를 올바르게** 쓰고 있음을 반대 케이스로 검증.
   SC=monolithic·crack-free = 우리 작은 AM_S(균열저항, #285) 와 표현형 일치(메커니즘은 결정성 vs 크기로 다름).
   ⇒ ASSB에서 SC의 가치는 **내구성**이지 동역학이 아닐 수 있다(낮은 활성표면적 → kinetics 손실 가능) — 액체와
   정반대 트레이드오프를, 우리 coverage·dead-AM·fracture로 정량화 가능.

---

*Digest 작성 2026-06-25. 소재 = NCM811 단결정/다결정 (액체 LIB). 우리 LPSCl-ASSB와 직접 비교 금지 —
본질 CAM 기하 + SC/PC 동역학 방향 + "균열=손실(고체)" 부호 확인만 전사. ★ audit #11 = MIS-ATTRIBUTION:
σ_S/σ_P 전자전도 엔드포인트는 이 논문 근거 없음.*
