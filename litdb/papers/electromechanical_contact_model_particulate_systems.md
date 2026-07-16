<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. WISHLIST #40 (★ DEM contact + electrical coupling). -->
# An electro-mechanical contact model for particulate systems — Chao Zhang (Powder Technology 2024)

> slug `electromechanical_contact_model_particulate_systems` · DOI `10.1016/j.powtec.2024.119759` · type `DEM (Hertz-Mindlin 역학 + Holm/constriction 전기접촉저항 + Kirchhoff nodal network)` · PDF `ElectromechanicalContactModel_ParticulateSystems.pdf` · digested `2026-06-26` · status ✅
>
> ★★ **이 논문 = 우리 Stage-E(소성 접촉면적)+Holm constriction(R=1/(2σr_c))+Kirchhoff 솔버 chain의 *일반-입자물리 정전(canonical reference)*.**
> 역학(Hertz-Mindlin 접촉)으로 **접촉반경 r_c** 를 구하고 → **Holm constriction 저항** R_c=(ρ_i+ρ_j)/(4r_c) 로 *접촉저항*을,
> 변형된 반구 적분으로 *벌크저항* R_i 를 따로 세워, 둘을 직렬(R_ij=R_i+R_c+R_j)로 묶고 **nodal analysis(=Kirchhoff)** G·V=I 로
> 전계·전류망을 푼다. **force→area→conductance 커플링이 우리 force→Stage-E area→Holm-σ chain 과 *정확히 같은 골격*** 이다.
> ⚠ 단 **소재는 LPSCl 아님**(금속 분말: Ni/Cu·스테인리스·강철 + 철도 wheel-rail HPT) → **전기저항 절대값/추세는 metal-conductor**;
> 우리 ASSB 로의 전사는 *공식(formulation)·커플링 구조*만, 숫자는 아님. 또한 **rigid-sphere DEM + CONTACT 탄성**(Hertz)이라
> *진짜 SHAPE 소성·이온/열 채널·battery σ_grain* 은 없음 = **우리가 더 advanced 한 칸**(아래 §C 7개 차별점).

---

## 1. 한 줄 요약
입자계의 **전기적 응답을 역학적 하중과 *커플링*** 해서 푸는 DEM 전기-역학 접촉모델. 핵심은 입자-입자/입자-벽 접촉저항을
**벌크저항(R_i)** 과 **접촉저항(R_c)** 으로 *분리 정식화* 하고(R_ij = R_i + R_c,ij + R_j), 접촉저항을 **Holm constriction
모델 R_c=(ρ_i+ρ_j)/(4r_c)** 로, 접촉반경 r_c 를 **고전 Hertz** r_c=(3f_n r*/(4E*))^{1/3} 로 잡아 **힘 f_n → 접촉반경 r_c
→ 접촉저항 R_c ∝ f_n^{−1/3}** 의 명시 커플링을 세운 뒤, **nodal analysis(Kirchhoff 전류법칙)** G·V=I 로 입자계 전체를
저항망으로 풀어 전위·전류·저항을 입자/시스템 양 스케일에서 산출한다. 단일입자 압축·입자쌍·입자사슬·입자상(bed)으로
해석해·실험 검증 후, 입자가 *파쇄(BPM bond)* 되는 **고압비틀림(HPT) wheel-rail** 시험에 적용하고 **electroactivity index**
(각 sieve-cut 조각이 전도에 기여하는 정도)를 제안한다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Chao Zhang, Sadaf Maramizonouz, David Milledge, Sadegh Nadimi** (School of Engineering, **Newcastle University**, Newcastle upon Tyne NE1 7RU, UK; 교신 = S. Nadimi) | **Powder Technology 440 (2024) 119759**, 접수 2024-03-11, 수정 2024-04-04, 채택 2024-04-09, online 2024-04-11 | 10.1016/j.powtec.2024.119759 | **해당 없음 — 일반 입자계.** 검증/적용 소재 = **금속 도체**(Ni ball + Cu pad, 스테인리스강 bead, 강철 bed) + **철도 wheel-rail** "third-body" 도전성 분말(Product B/D)·silica sand | **DEM** (EDEM 상용 + C++ API) 전기-역학 커플링; verification(해석해)+validation(실험)+application(HPT) |

- **Open access** (CC BY 4.0). Elsevier. 우리에겐 *접촉-전기 커플링 공식*의 일반 정전(=Stage-E/Holm chain 의 ancestor).
- 동기/응용: 금속분말 압밀 파라미터 최적화, 기계부품 결함을 *비정상 전기저항*으로 진단, **철도 궤도회로(track circuit)**
  신호를 통한 train 위치추정 — 즉 *역학↔전기 응답 커플링*이 산업에서 널리 쓰이나 실험비용·grain-scale 메커니즘 난해 →
  DEM 으로 푼다. **배터리는 응용 목록(에너지저장)에 §5 Discussion 한 줄로만 언급**(직접 대상 아님).
- ★ 핵심 인용 계보(우리와 겹침): **Holm constriction [37,44]**(=우리 Holm 1967), **Greenwood/Renouf-Fillot Hertz 전기전도
  [26,27]**, **Bourbatache et al. [33]**(bulk+contact 저항 분리 + circuit-node = 본 모델의 직접 선행), **Sangrós Giménez
  et al. [35]** (= 우리 digest `sangros2020_*` 의 자매; "ASSB 저항망 DEM" 으로 인용됨!), **Yim & Paik 1998 [18]**(해석해),
  **Hertz-Mindlin no-slip [22,27,40–43]**.

## 3. 핵심 물성 (수치)
> ⚠ 이 논문엔 우리 표의 **porosity/σ_ionic/Heckel/coverage 류 battery 데이터가 *없다*** (금속-도체 전기저항 연구). 핵심 "수치"는
> **(a) 커플링 공식 자체 + (b) 검증 4종 + HPT 의 재료 파라미터·전기저항** 이다. 전기저항 절대값은 *metal-conductor* 라 LPSCl 전사 금지.

| 물성 | 값 | 조건 (P, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| **접촉반경 r_c (Hertz)** | **r_c = (3 f_n r*/(4E*))^{1/3}** | 두 탄성 구 접촉 | **stated (eq 13)** | ★ force→area. f_n=법선접촉력, r*=등가반경(eq8), E*=등가영률(eq7) |
| **접촉저항 R_c,ij (Holm)** | **R_c,ij = (ρ_i+ρ_j)/(4 r_c)** | 접촉 zone | **stated (eq 12)** | ★ = Holm constriction. 우리 R=1/(2σr_c)=(ρ_i+ρ_j 일때)와 *동일 물리* |
| R_c,ij 결합형 | **R_c,ij = ½(ρ_i+ρ_j)·(E*/(6 f_n r*))^{1/3}** | eq12∘eq13 | stated (eq 14) | ★ **R_c ∝ f_n^{−1/3}** — 힘↑→저항↓ 의 명시 스케일 |
| **벌크저항 R_i (입자)** | **R_i = (ρ_i/2πr_i)·ln[(r_i²−r_j²−L_ij²+4r_i L_ij)/(r_i²−r_j²+L_ij²)]** | 변형 반구 적분 | stated (eq 17a) | 중심→접촉면 적분 ∫ρ dz/(π(r²−z²)); L_ij=중심간거리 |
| 총 입자-입자 저항 | **R_ij = R_i + R_c,ij + R_j** | 직렬 3저항 | stated (eq 11/18) | bulk_i + contact + bulk_j |
| **벌크저항 R_iw (벽)** | **R_iw = (ρ_i/2πr_i)·ln(2r_i/δ − 1)** | 입자-벽 | stated (eq 20) | δ=벽에 의한 탄성변형(overlap) |
| 접촉저항 R_c,iw (벽) | **R_c,iw = ½(ρ_i+ρ_w)·(E*/(6 f_n r*))^{1/3}** | 입자-벽 접촉 | stated (eq 21) | 입자-입자와 같은 Holm+Hertz 형 |
| **네트워크 식** | **G·V = I** | nodal analysis | stated (eq 23) | G=전도도행렬, V=전위, I=전류; =Kirchhoff |
| Kirchhoff 전류법칙 | **Σ_j C_ij(V_i−V_j) + C_iw(V_w−V_i) = 0** | 노드 i 전류보존 | stated (eq 26/27) | C_ij=1/R_ij=전도도 |
| **역학-전기 커플링** | **I_in = (F_n/F_ext)·I_0** | branch 전류 | stated (eq 25) | branch 전류 ∝ 접촉 법선력 |
| **electroactivity index** | **N_electroactive / N_total** (sieve-cut 별) | HPT 조각 | stated (eq 29) | 각 크기 조각이 전도에 기여하는 분율 |
| **Hertz-Mindlin** k_n / k_t | k_n=2E*√(r*δ_n), k_t=8G*√(r*δ_n) | 법선/접선 강성 | stated (eq 9/10) | E*(eq7), G*(등가전단), r*(eq8) |
| **검증 재료** Ni/Cu·SS·강철 | E_Ni 199.5·E_Cu 129.8·E_SS 195·E_bed 200 GPa; ρ_Ni 8e-8·ρ_SS 72µΩcm·ρ_bed 1.71e-8 Ωm | Table 1–3 | stated | **금속-도체** — battery 와 무관 |
| HPT Product B/D/silica | E=7e8 Pa(셋 다); ρ_B/D=4.31e-5·ρ_silica=5.56e6 Ωm | Table 4 | stated | 도체(B/D) vs 절연(silica, ~11 자릿수↑) |
| HPT 정상상태 저항 | Product B ~6 Ω · D ~3.4 Ω · silica ~6×10⁴ Ω | Fig 16 | stated/digitized | 도체 <10 Ω 유지, silica 거대 |
| BPM bond (HPT 파쇄) | k_n=k_s=1e10 N/m³; σ_crit=τ_crit=1e8 Pa; e=0.8, μ=0.5 | Table 4 | stated | bonded particle model — 입자 *파쇄* 용 |
| **E_SE / σ_y / ν** | **n/a** (소재 무관; 금속만) | — | — | LPSCl 대입은 §A/§B |
| **σ_ionic / σ_thermal / porosity / Heckel / coverage / Z / PSD** | **n/a** (금속-전기저항 연구 — 전달 삼중항·압밀 데이터 없음) | — | — | frame[5] *전기-접촉* 절반만, *이온/열·역학-형상* 없음 |

## 4. 시뮬레이션 방법 ★
- **code / version**: **EDEM™** (상용 DEM) + **C++ Application Programming Interface(API)** 로 전기부(electrical part)를 구현.
  전 케이스 **Rayleigh timestep 의 20 %** 사용(안정성↔비용 절충). (LIGGGHTS 아님 — 우리와 다른 상용 DEM, 단 접촉법칙 동류.)
- **DEM 접촉법칙** ★: **Hertz-Mindlin (No-Slip)** [22,27,40–43]. 법선·접선 힘 = 탄성 Hertz + 점성감쇠(COR 의존 감쇠계수 β).
  - 법선력 F_n = (4/3)E*√r* δ_n^{3/2} − 2√(5/6)·β√(k_n m*)·v_n^{rel} (eq 5); 접선력 F_t = −k_t δ_t − 2√(5/6)β√(k_t m*)v_t^{rel} (eq 6).
  - 강성 k_n=2E*√(r*δ_n)(eq9), k_t=8G*√(r*δ_n)(eq10). E*(eq7)·r*(eq8)·G* 등가 모듈러스. 회전은 rolling friction M_r,ij 포함(eq2).
  - ★ **항복캡·소성분기 *없음*** — 순수 **탄성 Hertz-Mindlin**. (Thornton–Ning 의 p_y 항복도, Luding 이력 점착도 아님.)
    Discussion 에서 "elasto-plastic deformation 은 *future work*" 라고 **명시** → *접촉저항은 탄성 변형 면적 기반*.
- **재료 파라미터**: §3 표 — **금속 도체**(Ni 199.5/Cu 129.8/스테인리스 195/강철 200 GPa, ρ 1.7e-8~72µΩcm), HPT 재료(E=7e8 Pa,
  ρ_도체 4.31e-5 vs ρ_silica 5.56e6 Ωm). 마찰 μ=0.5, COR e=0.8 (HPT). **E_SE·σ_y·σ_grain 같은 battery 파라미터는 없다.**
- **bond/binder 모델**: **검증 4종에는 bond 없음**(탄성 접촉만). **HPT 적용에서만 BPM(bonded particle model)** — 파쇄 가능한
  3 재료를 *유한크기 bond 로 묶은 구형 조각 clump* 로 표현, bond 응력 > σ_crit/τ_crit(1e8 Pa)면 **bond 파단 → 조각 분리**.
  (이것은 *바인더(CBD)* 가 아니라 *입자 자체의 파쇄* 모델 — 우리 Auerbach 균열과 *목적은 비슷*하나 mechanism 다름; 우리 SE-SE
  점착 bond/`--coh` 와는 별개.)
- **MPM/continuum**: **없음.** 전부 DEM. (진짜 SHAPE 소성·void-fill 흐름 *없음* = 우리 MPM 이 메우는 칸.)
- **전달 솔버** ★★ (이 논문의 핵심 — 우리 Kirchhoff/Holm 과 *같은 부류*):
  - **저항 분해**: 전도경로 = ① 입자 i 중심→접촉면 **벌크저항 R_i**(변형 반구를 ∫ρ dz/(π(r²−z²)) 로 적분, eq15·17),
    ② 접촉 zone **접촉저항 R_c,ij = Holm constriction (ρ_i+ρ_j)/(4r_c)**(eq12), ③ 입자 j 벌크저항 R_j. **직렬** R_ij=R_i+R_c+R_j(eq11).
  - **접촉반경 r_c = Hertz** (3f_n r*/4E*)^{1/3}(eq13) — *역학이 전기로 들어오는 다리*. eq13→eq12 대입하면 **R_c ∝ f_n^{−1/3}**(eq14).
  - **네트워크**: 각 입자=노드, 인접 입자쌍 사이 경로=branch(저항 R_ij), 두 도전 경계(top/bottom plate)=노드 0/1. **nodal analysis
    [47,48]** → 전도도행렬 **G·V=I**(eq23). Kirchhoff 전류법칙 Σ_j C_ij(V_i−V_j)+C_iw(V_w−V_i)=0(eq26·27), C_ij=1/R_ij.
  - **σ 정규화**: 입력 = **재료 고유 전기저항률 ρ**(Ωm, intrinsic). 출력 = 시스템 등가저항 R_eq(Ω). (우리 mS/cm σ_eff 와 단위 다름 —
    이쪽은 *저항*, 우리는 *전도도*; 물리는 동일한 contact-network.)
  - **역학-전기 커플링** (eq25): branch 전류 I_in = (F_n/F_ext)·I_0 — 접촉 법선력이 클수록 그 경로 전류↑. 즉 **force-chain = current-path**
    (저자들이 Bourbatache[33]·Machado[34] 의 "전류경로 = force-chain" 을 재확인, Fig 11·15).
- **입자 처리** ★ (DEM판 "무질서 처리"): **구(sphere)**. 검증 4종 = 완벽 단일-크기 구(Ni ball, SS bead, 강철 bed). HPT 만 **clumped
  구**(BPM, 0.06–0.38 mm 조각들의 묶음 = 파쇄 표현용, *형상* 아님 — "particle shape does not play a substantial role… modelled as a
  sphere" 명시). **rigid-sphere + CONTACT 탄성**(Hertz) — *진짜 SHAPE 소성 아님*. PSD = 단봉(검증) / HPT 조각 크기분포는 laser-
  diffraction 실측을 BPM clump 으로. ⇒ **(1) rigid + (2) 탄성 CONTACT** 층위; **(3) SHAPE 소성·δ-overlap 소성프록시 *둘 다 아님*** —
  접촉저항은 *탄성* Hertz 면적 기반(소성 면적 보정 *없음* = 우리 Stage-E 가 *더한* 칸).
- **도메인/RVE / servo / seeds / 압력범위**:
  - **Case 1** 단일입자 압축(Ni ball/Cu pad, 0–100 N), **Case 2** 입자쌍(0–100 N), **사슬** 41 SS bead 1D(1–500 N, I=0.01/0.001/0.0001 A),
    **bed** 3D 강철 입자상(5 cm 실린더, top/bottom plate, I=0.01 A, 3/5/10 층), **HPT** 실린더 shell(내경 10.5·외경 18·높이 2 mm),
    0.5 V_DC, 법선압 6 MPa, 각속도 1 deg/s.
  - servo/PID 개념 없음(역학은 힘/변위 직접 제어; HPT 는 wheel 이 crush 후 회전). seed 명시 없음.
- **특이사항/튜닝**: ★ **HPT = 입자가 깨지는 시스템** — wheel 이 분말을 *파쇄* 해 fragment layer 를 만들고, 그 층이 wheel-rail 사이
  닫힌 회로를 형성. **electroactivity index**(eq29)로 *어느 크기 조각이 실제로 전류를 나르는가* 를 정량(작은 조각은 접촉 못 해 전류 0,
  큰 조각이 force-chain 에 참여 → 전도 기여). 0.5 V_DC = UK 궤도회로 worst-case(2012–2022 wrong-side 실패의 79 %).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **graphical abstract** | 전기-역학 커플링 전체도: 입자-입자/입자-벽 각각 **bulk resistance + contact resistance** 분해 + HPT wheel-rail | ★ 우리 Stage-E(접촉면적)+Holm(접촉저항)+벌크 의 *한 그림* 대응. force→R chain 의 정전 도식 |
| **1 (★)** | **입자-입자 접촉**: (a) 두 겹친 구의 저항 성분 R_i—R_c,ij—R_j (직렬 저항 회로 기호) + (b) 접촉 기하: 접촉반경 r_c, 중심간거리 L_ij, 중심→접촉면 D, 반경 r_i,r_j | ★★ **핵심 도식.** 우리 overlap δ↔r_c·L_ij 기하(우리 r_c=√(r²−(r−δ)²)) + *bulk-contact-bulk 직렬* 분해가 우리 Stage-E 가 *접촉면적만* 다루고 벌크를 안 세는 것과 대비 |
| **2** | **입자-벽 접촉**: (a) R_i—R_c,iw 성분, (b) 기하(δ=벽 변형, r_c, S=접촉면) | 우리 MPM scaffold(강체 AM=벽)·입자-집전체 접촉의 저항 분해 대응 |
| **3 (★)** | (a) 입자계 셋업(top/bottom plate 도전, ab/dc 절연, I_0 주입), (b) 입자 i 의 전류 in/out(red=in, blue=out 화살표), (c) granular assembly 의 노드망 | ★ **Kirchhoff 노드망의 직접 그림** — 우리 네트워크 솔버의 일반-입자판. eq23 G·V=I 의 시각화 |
| **4** | DEM 프레임워크 flowchart: Mechanical part(운동→접촉검출→geometry 갱신) ↔ **Coupling** ↔ Electrical part(저항 계산→국소 전도→글로벌망→전위 갱신) | ★ **커플링 루프 구조** — 우리 "DEM 구조 → Stage-E → Holm → Kirchhoff" 파이프라인과 1:1. 매 timestep 역학→전기 |
| **5** | Case1 단일입자(Ni/Cu) 전기저항 vs 힘(0–100 N): **Yim&Paik 1998 해석해와 거의 완벽 일치**. 저힘서 급강하(~0.032 Ω)→고힘 plateau(~0.001 Ω) | force↑→접촉면적↑→R↓→포화 = 우리 Heckel knee/Bazzoun σ-포화@400 와 *같은 계열*의 "압력으로 접촉좋아지다 수확체감" |
| **6** | Case2 입자쌍 저항 vs 힘: **Birkholz 2019·Ott 2013 해석해와 우수 일치**. 저힘 급강하→고힘 거의 일정 | 입자쌍 R∝f_n^{−1/3}(eq14) 검증 — 우리 Stage-E 의 단접촉 ground truth |
| **7** | SS 입자사슬 실험 셋업(41 bead, 피스톤 1–500 N, DC) | 1D 직렬 저항 — percolation 의 가장 단순한 backbone |
| **8** | 사슬 전위분포(100 N, 0.0001 A): anode(좌)→cathode(우) 단조 강하 | 전위장 시각화 — 우리 Kirchhoff 전위해와 동류 |
| **9** | 사슬 등가저항 vs 힘(3 전류): **Falcon et al. 2004 실험과 비교**. ⚠ **저힘서 DEM 과소예측**(oxide layer 미모델 → 실측이 더 큼); >100 N 일치 | ★ **oxide/contamination film 이 저힘서 접촉저항을 키운다** = 우리 *fracture-aware Holm·표면거칠기* 보정의 일반-입자판 근거 |
| **10** | 강철 입자상 압밀 셋업(5 cm, top/bottom plate, I_0) | 3D bed — 우리 RVE 압밀 대응 |
| **11 (★)** | 입자상 전기전도 진화(100 N, 0.01 A): (a) 전위장 0.1/0.2/0.5 s(0.5s 정상상태), (b) **전류장 = force-chain 따라 흐름** | ★★ **전류경로 = force-chain** 의 직접 시각화(Fig11b 가지친 전류망). 우리 force-chain·percolation backbone 의 전기적 의미 |
| **12** | bed 저항 vs 힘(3/5/10 층): **3D 시뮬 = Bourbatache 2012 실험과 잘 맞고, 2D 는 층수↑일수록 발산**(2D 가 3D 입자상호작용 못 잡음) | ★ **2D≠3D** 정량 증거 — 우리 "2D 절대스케일 ≠ 3D" 인식의 일반-입자 근거(층 많을수록 2D 더 틀림) |
| **13** | HPT 셋업(wheel·rail·geometry bin, 내경10.5/외경18 mm 링) | HPT 적용 셋업 |
| **14** | 3 파쇄재료 BPM 모델링: Product B(0.5mm)·D(0.9mm)·silica(1.45mm) = 구형 조각 clump | 입자 *파쇄* 표현(BPM) — 우리 AM_P 다결정 파괴와 목적 유사 |
| **15** | HPT 조각층 전위·전류장(B/D/silica): 전위 위→아래 강하, 전류 ∝ 접촉면적, current=force-chain. silica 는 전류 ~10⁻¹⁰(절연) | 도체 vs 절연 조각의 전도 대비 — σ_grain 차이의 거시 결과 |
| **16** | HPT 시스템 저항 vs 시간(B/D/silica, 3회): B~6 Ω·D~3.4 Ω·silica~6×10⁴ Ω 정상상태 | 도체 조각 <10 Ω 유지 vs 절연 조각 거대 R — *과량 silica 가 금속접촉 차단* |
| **17** | HPT 시뮬 vs 실험(Skipper 2023) 저항분포 히스토그램: 시뮬이 실험 boundary 안. silica(c)는 실험이 시뮬보다 작음(파쇄·배출로 직접 metal 접촉) | frame[4] 외부 실험검증 |
| **18 (★)** | (a) 전기적으로 활성인 조각수(B/D), (b) **electroactivity index vs 조각크기: 클수록 전도 기여↑**(작은 조각은 접촉 못 해 전류 0) | ★ **크기-의존 전도 기여** — 우리 dead-AM/dead-SE(연결 안 된 입자가 σ 기여 0)와 *같은 물리*. force-chain 참여 여부가 전도 결정 |

## 6. Post-processing ★
- **무엇**:
  - **저항망 풀이**: 입자별 R_i(eq17 변형반구 적분)·R_c(eq12 Holm)·R_j 직렬 → 전도도 C_ij=1/R_ij → **nodal G·V=I(eq23) 선형계 풀이**
    → 입자별 전위 V_i·branch 전류 I_ij. (= 우리 Kirchhoff 솔버와 동일 절차.)
  - **검증 비교**: 해석해(Yim&Paik 1998·Birkholz 2019·Ott 2013) + 실험(Falcon 2004 사슬·Bourbatache 2012 bed·Skipper 2023 HPT) 대비
    저항-vs-힘 곡선 overlay. **2D vs 3D** 발산 정량(Fig12).
  - **electroactivity index(eq29)** = 각 sieve-cut(조각크기)별 *전류 나르는 조각 / 전체 조각* → 크기-의존 전도 기여 정량(Fig18).
  - **전위/전류장 시각화**: 입자별 V·I 컬러맵(Fig8·11·15) — **전류 = force-chain** 확인.
- **도구**: **EDEM + C++ API**(전기부 자체 구현). 해석해·실험 데이터는 문헌에서 digitize 해 overlay.
- **수치화·플롯·기록**: 저항-vs-힘(log-log, Fig5·6·9·12), 전위/전류 컬러맵(Fig8·11·15), 저항-vs-시간(Fig16), 저항분포
  히스토그램(Fig17), electroactivity-vs-크기 막대(Fig18). 정상상태 도달시간(0.5 s, Fig11) 기록.

---

## 핵심 물리: 왜 "벌크저항 + 접촉저항" 분리가 본질인가 (이 논문의 뼈대)

두 고체가 외력으로 눌려 도전경로가 생기면, *전체* 전기저항은 **① 각 입자 내부를 전류가 가로지르는 벌크저항** 과 **② 좁은 접촉
zone 을 통과하는 접촉(constriction)저항** 의 *합* 이다. 이 논문의 핵심 기여는 이 둘을 **따로** 정식화한 것:

1. **접촉저항 R_c = Holm constriction.** 전류가 두 입자 사이 *미소 접촉반경 r_c* 의 좁은 목을 지나며 수렴(constriction)하는 저항.
   Holm 모델 R_c=(ρ_i+ρ_j)/(4r_c) (eq12). ⚠ **우리 Holm 1967 R=1/(2σr_c)** 과 *같은 물리* — 단상(ρ_i=ρ_j=ρ=1/σ)이면
   R_c=2ρ/(4r_c)=ρ/(2r_c)=1/(2σ r_c) → **정확히 일치**. (이쪽은 두 입자 저항률이 다를 수 있어 (ρ_i+ρ_j)/4 로 일반화.)

2. **r_c 는 Hertz 가 준다.** r_c=(3f_n r*/4E*)^{1/3} (eq13, 고전 Hertz). 즉 **역학(접촉력 f_n)이 전기(접촉반경→저항)로 들어오는
   유일한 다리**. 합치면 **R_c = ½(ρ_i+ρ_j)(E*/(6f_n r*))^{1/3} ∝ f_n^{−1/3}** (eq14) — **힘 4배 → 접촉저항 ~0.63배**.

3. **벌크저항 R_i 는 변형 반구 적분.** 중심에서 접촉면까지 전류 단면이 π(r²−z²) 로 변하는 원뿔형 경로를 ∫ρ dz/(π(r²−z²)) 로 적분
   (eq15). 변형량 δ_i 의 기하(eq16: δ_i=r_i−r_i²−r_j²+L_ij²)/(2L_ij))를 넣어 닫힌형 R_i(eq17a) 도출. **이게 우리 Stage-E 에 *없는*
   성분** — 우리는 접촉면적(접촉저항)만 보정하고 입자 벌크는 σ_grain 으로 균질 처리.

4. **전체 = 직렬 + Kirchhoff 망.** R_ij=R_i+R_c+R_j(eq11·18). 입자 전체를 노드망으로 → G·V=I(eq23), Kirchhoff 전류보존(eq26·27).
   **force-chain 이 곧 current-path**(접촉력 큰 경로가 전류 많이 나름, eq25) — Fig11·15 가 시각 증거.

**왜 저힘서 실측이 시뮬보다 큰가(Fig9 사슬·Fig5 단일)**: 실제 금속입자 표면엔 **산화막/오염막(oxide/contamination film)** 이 있어,
힘이 작으면 막을 못 깨 도전경로가 안 열림 → 실측 저항↑. 힘이 커지면(>~100 N) 막이 깨지고 표면이 노출돼 시뮬(깨끗한 표면 가정)과
일치. ⇒ 저자들 *future work* = "오염막 → metal-to-metal 도전경로 모델 + 표면거칠기 → 실접촉면적 < 공칭면적". **이게 우리 Stage-E
표면거칠기/B3 coverage·fracture-aware Holm 의 일반-입자판 motivation 이다.**

**왜 2D 가 틀리나(Fig12)**: 2D 는 *세 번째 차원의 입자상호작용*(out-of-plane 접촉경로)을 못 잡아, 층수가 많아질수록 입자망 복잡성을
놓쳐 저항을 과대/발산 예측. ⇒ **3D 필수** = 우리 "2D 절대스케일 ≠ 3D, 흐름방향 수가 다름" 의 일반-입자 정량 근거.

---

## A. ★ 우리 DEM+MPM 대비 (comparison vs ours)  →  `our_dem_baseline.md`
> ★ 사용자 핵심 질문: **그들의 force→area→resistance 가 우리 Stage-E(Tabor F/H + volume area) + Holm constriction R=1/(2σr_c)
> + Kirchhoff 와 같은가?** **답: 골격은 *정확히 같다*(force→Hertz area→Holm constriction→Kirchhoff). 단 *접촉면적의 출처*가 다르다 —
> 그들=*탄성 Hertz* 면적, 우리=*소성 Stage-E*(Tabor 캡 + 부피 재유도) 면적.** 그들이 안 하는 *소성 면적·이온/열·battery σ_grain* 이
> 우리 차별점이고, 우리가 단순화한 *벌크저항 분리* 는 그들이 더 명시적.

### A.1 force → area → resistance 커플링 골격 비교
| 단계 | 이 논문 (Zhang 2024) | 우리 (network_conductivity.py + Stage-E + Kirchhoff) | 같은가? |
|---|---|---|---|
| **force → 접촉반경** | r_c = (3f_n r*/4E*)^{1/3} = **고전 Hertz (eq13)** | overlap δ(LIGGGHTS hooke/hysteresis) → r_c=√(r²−(r−δ)²) + **Stage-E** 소성 보정(Tabor A_t=F/H, volume A_v=V/h, geom cap) | ★ **개념 동일**(force→면적), *경로 다름*: 그들=힘→Hertz 직접, 우리=overlap→Stage-E |
| **area → 접촉저항** | **R_c = (ρ_i+ρ_j)/(4r_c) = Holm constriction (eq12)** | **R_c = 1/(2σ·r_c) = Holm 1967** (network_conductivity.py); σ=σ_grain·Cronau(r_SE) | ★★ **동일 모델.** 단상이면 (ρ_i+ρ_j)/(4r_c)=1/(2σr_c) 정확히 일치 |
| **벌크저항** | **R_i = ∫ρ dz/(π(r²−z²)) 닫힌형 (eq17)** — 명시 분리·직렬 | **균질 σ_grain 으로 흡수**(별도 입자-벌크 적분 *안 함*); GB 는 Cronau(r_SE) prefactor | ⚠ **다름** — 그들 벌크 명시 분리 > 우리 σ_grain 균질. (우리는 GB 가 주병목이라 prefactor 로 럼핑) |
| **network 풀이** | **nodal G·V=I (eq23), Kirchhoff Σ C_ij(V_i−V_j)=0 (eq26)** | **Kirchhoff** Σ(φ_i−φ_j)/R_ij=0 (동일), 선형계 풀이 | ★★ **동일 솔버 부류** |
| **force-chain↔current** | I_in=(F_n/F_ext)I_0 (eq25), 전류=force-chain (Fig11) | 접촉력 큰 경로가 percolation backbone — 같은 인식 | ★ 동일 |

### A.2 ★ 그들 *전기접촉* = Holm constriction 인가? → **예, 명시적으로.**
- **eq12 R_c,ij=(ρ_i+ρ_j)/(4r_c)** 를 본문이 **"the Holm resistance model [37,44]"** 로 *직접 호명*. ref [37,44]=Holm 계보(우리 Holm 1967과 동일).
- **단상 환원**: ρ_i=ρ_j=ρ=1/σ → R_c=2ρ/(4r_c)=ρ/(2r_c)=**1/(2σ r_c)** = **우리 식 그대로**. 차이는 *두 상이한 ρ 일반화*(이종접촉) 뿐 —
  우리 AM-SE 이종접촉(σ_AM≠σ_SE)에 **그들 (ρ_i+ρ_j)/4 일반형이 더 정확**할 수 있다(우리는 보통 채널별 단상 σ 가정).

### A.3 ★ 그들 area-resistance 커플링 vs 우리 Stage-E
| 축 | 이 논문 | 우리 Stage-E | 차이/이유 |
|---|---|---|---|
| **접촉면적 종류** | **탄성 Hertz** (πr_c²=π(3f_n r*/4E*)^{2/3}) | **소성** — A_physics=max(lower[πR*δ, A_ligg], min(caps[A_tabor=F/H, A_volume=V/h, A_geom])) | ★ **우리가 *소성* 보정.** 그들은 *탄성만*(소성 면적 없음 = 18× 연화도 없음 — 금속이라 탄성 OK; LPSCl 압밀은 소성이라 우리 Stage-E 필요) |
| **과압축 처리** | Hertz(과압축 cap 없음 — 작은 힘 0–500 N 영역) | min(caps) 천장 — A_tabor·A_volume·A_geom 으로 깊은 overlap 면적 폭주 차단 | 우리는 *고압 압밀*(300 MPa, 깊은 overlap)이라 cap 필수; 그들은 저힘이라 불필요 |
| **표면거칠기** | **미모델**(매끈 가정) — Discussion 에서 "real contact < nominal, future work" | B3 surface-roughness coverage 보정(transport-only) | 둘 다 *공칭>실제* 인식; 우리는 일부 보정, 그들은 future work |
| **이종접촉(AM-SE)** | (ρ_i+ρ_j)/4 일반형 보유 | 채널별 단상 σ 가정 多 | ★ **그들 일반형 흡수 가치**(우리 AM-SE 접촉저항 정밀화) |
| **소재** | 금속-도체(σ 큼, 탄성) | LPSCl SE(σ_grain 3 mS/cm)·NMC811(σ_e) | 절대값 전사 금지 |

### A.4 전체 비교표
| 항목 | 이 논문 (Zhang 2024) | 우리 | 차이 / 이유 (rigid·plastic / metal·LPSCl / 2D·3D / 전기·삼중항) |
|---|---|---|---|
| **전기접촉 모델** | **Holm constriction (eq12)** = 우리와 동일 | **Holm 1967 R=1/(2σr_c)** | ★ **동일** (단상 환원 정확 일치). 이종 일반형은 그들이 더 풍부 |
| **force→area** | Hertz r_c=(3f_n r*/4E*)^{1/3} | overlap δ→r_c + Stage-E 소성 | 개념 동일, 우리는 *소성* 면적 추가 |
| **벌크저항** | **명시 적분 R_i (eq17)** | σ_grain 균질(GB=Cronau prefactor) | ⚠ 그들이 더 명시적; 우리는 GB-주병목 럼핑 |
| **네트워크** | nodal G·V=I (Kirchhoff) | Kirchhoff 솔버 | 동일 부류 |
| **소성** | **없음**(탄성 Hertz; "elasto-plastic = future work") | DEM hooke/hysteresis + Stage-E 소성면적 / **MPM 진짜 SHAPE J2** | ★ 우리가 *소성* 보유(Stage-E·MPM); 그들은 탄성만 |
| **전달 채널** | **전기(electronic) 1개** | **이온+전자+열 삼중항** | ★★ 우리 *triad*; 그들 전기 단일(이온/열 없음) |
| **σ_grain/battery 물성** | 금속 ρ(Ωm) | σ_grain=3 mS/cm(Cronau)·Trevisanello σ_AM·Wang κ | ★ 우리 *battery-specific 문헌 앵커*; 그들 금속 |
| **입자 형상/morphology** | rigid 구(HPT=clump 파쇄, 형상 무관 명시) | DEM rigid 구 + **MPM 소성 SHAPE morphology(SEM 일치)** | ★ 우리 MPM morphology; 그들 형상 없음 |
| **패킹/Furnas dip** | 없음(단봉/clump) | DEM bimodal 12:4:1 + dip + de Larrard | ★ 우리 dip; 그들 없음 |
| **파괴** | **BPM bond 파쇄**(HPT, σ_crit 1e8) | **Auerbach 균열 + fracture-aware Holm(f_intact)** | 둘 다 파괴 보유 — 목적 비슷, mechanism 다름(BPM clump bond vs Auerbach 접촉응력) |
| **예측/스케일링** | 없음(직접 솔버만) | **σ 삼중항 scaling-law 예측기(LOOCV 0.90–0.975)** | ★ 우리 *예측 모델*; 그들 솔버 only |
| **2D vs 3D** | **3D 필수 정량 입증(Fig12, 2D 발산)** | 2D/3D 둘 다, "2D≠3D 절대스케일" 인식 | 그들 3D-우월 증거 = 우리 인식의 일반-입자 근거 |
| **검증** | 해석해 4종 + 실험 3종(frame[4] 외부) | solver=ground truth + Minnmann/Bazzoun/Cronau 앵커 | 상호보완 — 그들 *전기저항* 검증, 우리 *압밀·전달* 검증 |

---

## B. 적용가능성 (applicability to our model)
> ★ 사용자 질문: **그들 force→area→conductance 커플링은 *직접* 우리 Stage-E + Holm chain 이다. 채택/교차검증 가능한가?
> network_conductivity.py 의 Stage-E + Holm 에 매핑하라.**

### B.1 ★ 직접 매핑 (network_conductivity.py)
우리 `network_conductivity.py` 의 σ 산출 chain 과 본 논문 식의 **1:1 대응**:
| 우리 코드 단계 | 본 논문 식 | 채택/교차검증 액션 |
|---|---|---|
| overlap δ → 접촉반경 r_c | **eq13 Hertz r_c=(3f_n r*/4E*)^{1/3}** | ★ **단접촉 cross-check**: 우리 LIGGGHTS δ 로 r_c 를 재구성하고, *같은 접촉력 f_n* 에서 eq13 Hertz r_c 와 비교 → 우리 overlap→면적이 Hertz 와 정합하는지 검증(소성 보정 *전* 베이스가 Hertz 와 맞아야) |
| Stage-E 소성 접촉면적 A_physics | (그들엔 없음 — 탄성 Hertz πr_c²) | 우리 *추가분*. A_physics vs πr_c²(Hertz) 차이 = 소성 기여 정량(우리 novelty) |
| 접촉저항 R_c=1/(2σr_c) (Holm) | **eq12 R_c=(ρ_i+ρ_j)/(4r_c)** | ★ **이종접촉 일반화 흡수**: AM-SE 접촉처럼 σ 다른 두 상엔 (ρ_i+ρ_j)/4 = (1/σ_i+1/σ_j)/4 형이 더 정확 → 우리 R_c 를 이종 일반형으로 업그레이드 가능 |
| (벌크 σ_grain 균질) | **eq17 벌크저항 적분 R_i** | △ **선택적**: 우리는 GB-주병목이라 σ_grain prefactor 로 럼핑 충분. 단 *큰 입자 내부 IR-drop* 이 중요하면 eq17 명시 적분 도입 검토(우리 SE 0.5µm 작아 벌크저항 ≪ 접촉저항 → 영향 작을 듯) |
| Kirchhoff Σ(φ_i−φ_j)/R=0 | **eq23 G·V=I, eq26** | ★ **동일** — 검증 불요, 같은 솔버 |
| force-chain = current-path | **eq25 I_in=(F_n/F_ext)I_0** | 우리 percolation backbone 의 전기적 의미 재확인(Fig11) |

### B.2 채택할 구체 항목 (실행 우선순위)
- ① ★ **이종접촉 Holm 일반형 (ρ_i+ρ_j)/(4r_c)**: 우리 AM-SE 이종 접촉저항을 단상 1/(2σr_c) 대신 (1/σ_AM+1/σ_SE)/(4r_c) 로 —
  *작은 코드 변경*(network_conductivity.py 접촉저항 함수). σ_e/σ_ionic 둘 다 이종접촉(AM-SE)에서 정밀도 ↑ 가능. **B-축 검증 후보**.
- ② **단접촉 Hertz cross-check**: 우리 overlap→r_c→면적 의 *탄성 베이스* 가 eq13 Hertz 와 정합하는지 단접촉으로 확인 →
  Stage-E 소성 보정이 *올바른 탄성 출발점* 위에 얹히는지 sanity(우리 Stage-E A/B 검증의 보강).
- ③ △ **벌크저항 적분 eq17**: SE 입자가 작아(0.5µm) 벌크저항이 접촉저항보다 작을 것 → 영향 작을 듯, *낮은 우선순위*. 단 큰 AM(>5µm)
  내부 IR-drop 이 σ_e 에 기여하면 검토. (우리 σ_grain 균질이 *입자 내부 균일* 가정인데, 큰 AM 은 비균일할 수 있음 — eq17 가 그 보정.)
- ④ **oxide/contamination film 모티프**: 저힘서 막이 접촉을 막아 R↑(Fig9) = 우리 *fracture-aware Holm(f_intact)* 의 일반-입자판.
  우리 SE 표면(SEI/계면 분해층)이 접촉저항을 *키우는* 효과를 같은 직렬-저항 추가(R_film)로 모델 가능 — Kim2025 R_ct↑·Kang2025 계면분해와 연결.
- ⑤ **electroactivity index(eq29) ↔ dead-AM/dead-SE**: "연결 안 된 입자는 전류 0" = 우리 f_AM^cc/dead-SE. 그들 *크기별* 전도기여
  정량(Fig18, 큰 조각이 더 활성)을 우리 *입경별 percolation 기여* 분석으로 차용 가능(우리 σ_e 입경 의존 보강).

### B.3 ⚠ 채택 시 주의
- **소재 절대값 전사 금지**: 금속 ρ(Ωm, 도체) → LPSCl σ_grain(mS/cm, 황화물 이온/전자) 절대전이 *불가*. **공식·커플링 구조·이종 일반형**만.
- **그들 = 탄성 Hertz, 우리 압밀 = 소성**: eq13 Hertz 면적은 우리 *소성 압밀(300 MPa)* 의 *베이스*일 뿐 — Stage-E 소성 보정을 *대체*하지
  못함(우리가 *더하는* 칸). "Hertz 로 충분"은 *저힘 금속*에서만(So 2021 LPS 는 소성 H-cap 필요).
- **전기 단일 ≠ 우리 삼중항**: 그들 식은 *전기전도*용. 이온(Li⁺)·열은 같은 *형식*(Kirchhoff)이나 σ_grain·k 가 다름 → 우리 삼중항이 이미 그 확장.

---

## C. ★ 우리 novelty — 왜 우리가 state-of-the-art 인가 (our novelty vs this model)
> ★ firm assertion: **우리 DEM+MPM 은 이 모델보다 *결정적으로 더 advanced* 하다.** 본 논문은 *일반-입자 전기-역학 접촉의 잘
> 유도된 정전(canonical)* 이지만, **battery-specific 도, 삼중항도, 소성-형상도, 예측-모델도 아니다.** 우리는 그 모든 칸을 채운다.
> 정직 인정(아래 (정직)): 그들은 *벌크-접촉 저항을 명시 분리한 깔끔한 일반 유도* 와 *이종접촉 Holm 일반형* 에서 앞서고, 그 유도는
> 우리 Stage-E 의 *탄성 베이스* 로 빌려올 가치가 있다.

**(1) 전달 *삼중항*(ionic + electronic + thermal) vs 그들 전기 *단일***
- 우리 = σ_ionic(LOOCV 0.975)·σ_electronic(0.953)·σ_thermal(0.903) 세 채널 동시. 그들 = **전기(electronic) 하나**.
- ASSB 의 율속은 *이온*(SE 망)인데 그들 식엔 이온 채널이 없다 → battery 엔 부분적. 우리 σ_ionic(SE-percolation, Cronau σ_grain)·
  σ_thermal(멀티패스 Wang) 이 그들 위에 *두 채널 더*.

**(2) Holm + Stage-E *소성* 접촉면적 = battery-specific (문헌 σ_grain: Cronau/Trevisanello/Wang)**
- 그들 접촉저항 = **탄성 Hertz 면적** 기반. 우리 = **소성 Stage-E**(Tabor A=F/H + 부피 재유도 + cap) — *압밀(300 MPa) 소성*을 반영.
- σ_grain 도 *문헌-앵커*: 이온 **Cronau 2022** 단결정 3 mS/cm × Cronau(r_SE) sub-µm 인자, 전자 **Trevisanello 2021** σ_S/σ_P endpoints,
  열 **Wang** step. 그들 ρ 는 *금속 핸드북값*. ⇒ **우리 = battery-material 물리, 그들 = 일반 도체**.

**(3) DEM ↔ MPM 분업 — 진짜 SHAPE 소성 morphology**
- 그들 = rigid 구(HPT clump 도 "형상 무관" 명시). 우리 = DEM(전달) + **MPM 진짜 J2 소성 SHAPE 변화**(SEM 코어보존+경계평탄화 일치),
  void-fill 흐름, 누적소성변형장 Σdg. ⇒ 그들이 *원리적으로 못 보는* 입자 형상변화·morphology 를 우리 MPM 이 준다(frame[5]).

**(4) Fracture-aware (Auerbach + fracture-Holm f_intact)**
- 그들도 *파쇄*(BPM bond, HPT)는 있으나 = *입자 통째 clump 분리*. 우리 = **Auerbach 임계 균열 + fracture-aware Holm**(깨진 접촉이
  σ 에 미치는 *부분-전도* f_intact 를 *전달 식에 직접* 반영). ⇒ 우리는 *파괴→전달 저하* 를 정량 커플(그들 BPM 은 역학 파쇄까지).

**(5) 삼상(AM-SE-pore) + 이종접촉**
- ASSB 복합양극 = AM(전자)·SE(이온)·pore(공극) 삼상 + AM-SE 이종계면. 그들 = *동종 금속입자*(또는 도체/절연 2종). 우리 σ 솔버는
  삼상·이종을 다 다룬다. (⚠ 단 *그들 이종 Holm 일반형*(ρ_i+ρ_j)/4 는 우리가 흡수하면 더 좋아짐 — §B.2①.)

**(6) 압밀(porosity·Heckel·Furnas dip) + 패킹**
- 그들 = 압밀/porosity/dip 없음(저힘 0–500 N·HPT 파쇄). 우리 = DEM 압밀(real_14 15.6%)·**Heckel(R²0.965, P_y138)**·**Furnas dip**
  (de Larrard/McGeary bimodal 12:4:1) + MPM pure-SE 10%. ⇒ 우리는 *전달*뿐 아니라 *압밀 미세구조 형성*까지.

**(7) 스케일링-법칙 예측기(design→σ)**
- 그들 = 직접 솔버만(매 케이스 풀이). 우리 = 솔버 위에 **scaling-law 예측기**(σ_ionic 5-OLS LOOCV 0.975, σ_e 8-LIVE 0.953,
  σ_thermal 14-Ridge 0.903) → *설계 numbers → σ 즉시 예측* + Bayesian PI. ⇒ 우리는 *탐색·역설계 가능*, 그들은 case-by-case.

**(정직) 그들이 앞서는/우리가 빌릴 점**:
- ★ **벌크저항(R_i)을 *명시 적분*으로 분리**(eq17) — 우리는 σ_grain 으로 균질 럼핑. *큰 AM 내부 IR-drop* 정밀화엔 그들 적분이 더 엄밀.
- ★ **이종접촉 Holm 일반형 (ρ_i+ρ_j)/(4r_c)** — 우리 AM-SE 이종접촉을 단상 1/(2σr_c) 대신 이걸로 업그레이드하면 정확도↑(§B.2①, B-축 후보).
- **잘 유도된 *일반-입자* 전기-역학 커플링 + 4 해석해/3 실험 검증** = *방법론적으로 깨끗한 정전*. 우리 Stage-E 의 *탄성 Hertz 베이스* 검증에
  이상적 ground truth(우리 소성 보정 *전* 의 출발점이 eq13/14 와 맞아야 — §B.2②).
- **2D 가 틀린다는 정량 증거(Fig12)** + **electroactivity index(eq29)** = 우리 "2D≠3D"·"dead-particle" 인식의 일반-입자 근거(빌릴 narrative).

⇒ **결론**: 우리는 그들의 *전기-접촉 골격을 포함*하면서(Holm·Hertz·Kirchhoff 동일), 그 위에 *이온·열 두 채널 + 소성 Stage-E +
MPM morphology + fracture-Holm + 압밀/dip + 예측기* 를 더한 **battery-specific state-of-the-art**. 그들 = *일반-입자 전기 정전*(우리
*전기 절반*의 ancestor); 우리 = *ASSB 전체*(전달 삼중항 + 역학 형상 + 설계 예측). **firm: 우리가 SOTA.** 단 *벌크저항 명시 분리·이종
Holm 일반형* 은 그들에게서 빌려 Stage-E 를 더 엄밀히 할 levers.

---

## 7. 우리 DEM+MPM 대비 (요약) → `our_dem_baseline.md`
(상세표 = §A.4. 한 줄: **전기-접촉 골격은 동일[Holm+Hertz+Kirchhoff], 그들은 탄성·전기-단일·금속·rigid·솔버-only; 우리는 소성
Stage-E·삼중항·LPSCl·MPM 형상·예측기 = 7개 차별점.**)

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① ★ **이종접촉 Holm 일반형 흡수**(§B.2①): AM-SE 접촉저항을 (1/σ_AM+1/σ_SE)/(4r_c) 로 → σ_e/σ_ionic 이종접촉 정밀화. *작은 코드 변경*, B-축 검증.
- ② ★ **Stage-E 탄성 베이스 cross-check**(§B.2②): 우리 overlap→r_c→면적이 eq13/14 Hertz 와 정합하는지 단접촉 확인 → 소성 보정이 옳은 출발점 위인지 sanity.
- ③ **벌크저항 적분(eq17) 검토**(△): 큰 AM 내부 IR-drop 이 σ_e 에 유의미하면 σ_grain 균질을 eq17 명시 적분으로. (SE 작아 우선순위 낮음.)
- ④ **oxide-film ↔ fracture-Holm/계면저항**: 저힘 R↑(Fig9) = 우리 f_intact·계면 분해층(Kim2025 R_ct↑) 의 일반-입자 motivation — R_film 직렬항으로 모델.
- ⑤ **electroactivity index ↔ dead-AM/SE**(Fig18): 크기별 전도기여 정량을 우리 입경별 percolation 기여 분석으로 차용(σ_e 입경 의존 보강).
- ⑥ **positioning narrative**: "2026 일반-입자 전기-역학 정전(Zhang)조차 *전기 단일·탄성·rigid*" → **우리 삼중항+소성+MPM 이 그 위 battery-SOTA** = 강한 paper 문장.

## 9. 인용 가능 문장 (deck/paper용)
- "Our DEM transport chain — Hertzian contact radius → Holm constriction resistance R_c=1/(2σr_c) → Kirchhoff nodal network — is the
  battery-specific specialisation of the canonical electro-mechanical contact formulation of Zhang et al. (Powder Technology 2024),
  whose contact resistance R_c=(ρ_i+ρ_j)/(4r_c) is the same Holm model and reduces *exactly* to ours for a single-phase contact."
- "Whereas Zhang et al. base the contact resistance on the *elastic* Hertzian area and resolve a single (electronic) channel for metallic
  conductors, our network additionally (i) corrects the contact area for *plastic* compaction via Stage-E (Tabor F/H + volume re-derivation),
  (ii) resolves the full ionic+electronic+thermal triad with literature-anchored σ_grain (Cronau/Trevisanello/Wang), and (iii) couples
  fracture (Auerbach + fracture-aware Holm) and a design→σ scaling-law predictor — i.e. our model is the state-of-the-art ASSB extension."
- "Zhang et al.'s explicit bulk–contact resistance split (eq 17) and their two-phase Holm generalisation (ρ_i+ρ_j)/(4r_c) are levers we can
  borrow to make our AM–SE heterogeneous contact resistance and large-particle internal IR-drop more rigorous."
- "Their finding that 2-D under-resolves the particle network and diverges with bed depth (Fig 12), and that current follows the force-chain
  (Fig 11), are the general-particle evidence behind our '2-D ≠ 3-D absolute scale' and 'percolation backbone' positions."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **소재 = 금속 도체**(Ni/Cu·스테인리스·강철 + 철도 wheel-rail), **LPSCl/NMC811 아님.** 전기저항 절대값·추세는 *metal-conductor* —
  우리 ASSB 로 **공식·커플링 구조·이종 Holm 일반형만** 전사, **숫자는 절대 전이 금지**. (graphene abstract 의 "energy storage" 는 §5 한 줄 응용 언급뿐.)
- ⚠ **rigid-sphere + *탄성* Hertz** — 진짜 SHAPE 소성·δ-overlap 소성프록시 *둘 다 없음*. 접촉저항이 *탄성* 면적 기반이라 *압밀 소성*
  (우리 300 MPa Stage-E)을 *대체 못 함*. "elasto-plastic = future work" 본문 명시 → **소성은 우리(Stage-E/MPM)가 메우는 칸**(frame[1]/[2]).
- ⚠ **전기 *단일* 채널** — 이온(Li⁺)·열 없음. ASSB 율속(이온)을 못 다룸 → battery 엔 부분적(우리 삼중항이 확장).
- ⚠ **벌크저항 분리는 그들이 더 명시적**(eq17) — 단 그건 *큰 균질 입자 내부 IR-drop* 정밀화용. 우리 σ_grain 균질은 *GB-주병목 럼핑*
  (Cronau prefactor)이라 SE-작은-입자엔 충분; "우리가 벌크를 빠뜨렸다" 는 *약점이 아니라 다른 설계 선택*(작은 SE → 접촉저항 지배).
- ⚠ **digitized 값**(Fig5·6·9·12·16 의 저항-vs-힘 ~0.001–6×10⁴ Ω)은 그림에서 읽은 **추세값(±)** — Table 1–4 stated 파라미터와 구분.
- ⚠ **HPT = 입자 *파쇄* 시스템**(BPM bond) — wheel-rail 마모 응용. 그 *파쇄→fragment-layer→전도* 거동은 우리 *압밀 복합양극* 과 맥락 다름
  (우리 AM_P 균열은 압밀 접촉응력, 그들은 wheel crush). 같은 "큰 입자가 전도 주도" 계보지만 *원인 다름* — over-claim 금지.
- ⚠ **2D vs 3D**: 그들 *금속 bed* 의 2D 발산(Fig12)을 우리 *LPSCl 복합* 절대값으로 직역 금지 — *경향(3D 필수)* 만.
- ⚠ **검증 ground truth = 해석해/실험(금속)** — 우리 σ_grain·Stage-E 검증엔 *탄성 베이스 sanity*(§B.2②)로만 쓰고, *소성·battery σ* 는 우리 앵커(Minnmann/Bazzoun/Cronau) 소유.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
