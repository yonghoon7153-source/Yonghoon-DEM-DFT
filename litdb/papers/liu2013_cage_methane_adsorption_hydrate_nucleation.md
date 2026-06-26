# Effects of cage type and adsorption face on the cage–methane adsorption interaction: Implications for hydrate nucleation studies — Liu et al. (Chem. Phys. Lett. 2013)

> slug `liu2013_cage_methane_adsorption_hydrate_nucleation` · DOI `10.1016/j.cplett.2013.05.012` · type `classical-MD (GROMACS, PMF)` · PDF `fef2173b-8._Effectstudies.pdf` · digested `2026-06-26` · status ✅ (filed as EXTERNAL)

---

## ⚠ OFF-TOPIC / EXTERNAL — NOT an argyrodite / battery paper

> **이 논문은 가스 클라트레이트 수화물(gas clathrate hydrate) 논문입니다 — 물 분자 cage + 메탄(CH₄) guest, 고전적 MD/PMF.** Li₆PS₅Cl argyrodite·고체전해질·Li⁺ 전도와 **물리적으로 무관**합니다.
> - "cage" = **물 다면체 공동**(5¹², 4¹5¹⁰6² 등), guest = **메탄 분자**. 상호작용 = **수소결합 + van der Waals(분산)**.
> - "inter-cage diffusion" = **메탄이 물 cage 사이를 hop/cross**하는 것 — **Li⁺의 PS₄-cage 간 이동이 아님**.
> - 방법 = **classical force-field MD(GROMACS, TIP4P/2005 물 + OPLS-UA 메탄)로 PMF(평균력퍼텐셜) 계산** — 우리 BVSE/AIMD/NEB/DFT와 다름.
> - **이 digest는 [우리 그룹]이 아니며, argyrodite `comparison_vs_ours.md`의 물성 4축(A 이온/B 산화/C 기계/D 전자) machinery에 절대 넣지 않는다.**
> - **보관 이유 = 단 하나의 전이 가능한 *개념적 멘탈모델*** ("cage의 face/window 크기가 guest의 trap-vs-cross를 PMF 자유에너지 장벽으로 결정한다") — argyrodite Li⁺ **inter-cage 이동 장벽**을 *생각하는 방식*으로서만. 우리 재료에 대해 **아무것도 검증/입증하지 않는다**(§7 analogy-only).

---

## 0. 이 digest를 읽는 법
이 논문은 **"메탄 수화물 핵생성(nucleation)이 시작될 때, 용해된 메탄과 물 cage 사이의 인력이 *어떤 요인*에 더 민감한가 — cage의 *종류*인가, cage 면(face/window)의 *크기*인가?"** 를 묻는다. 무대는 **Cage Adsorption Hypothesis(CAH, Guo et al.)** — *물 cage가 그 면 위에 메탄을 흡착하는 것이 수화물 형성의 본질적 추동력*이라는 가설. 정량 척도는 **cage–메탄 PMF**(potential of mean force, 거리에 따른 자유에너지)이고, 흡착의 세기는 PMF의 **첫 우물 깊이**와 **활성화에너지 E_a**(첫 우물→첫 장벽 자유에너지차)로 측정한다.

핵심 결과 한 줄: **흡착 세기는 cage *종류*에는 거의 무관하고 흡착 *면의 크기*에 강하게 의존한다 — 면이 클수록(4→5→6각형) 더 세게 흡착(E_a ≈ 12→21 kJ/mol). 그러나 면이 7각형 이상이 되면 cage는 메탄을 더 이상 *흡착*하지 못하고 메탄이 그 구멍을 *통과*(cross)하게 둔다.** 이 7각형 임계가 비정질 수화물 내 **메탄의 inter-cage 확산**(cage 사이 이동) 통로를 설명한다.

## 1. 한 줄 요약
Classical-MD PMF로 물 cage–메탄 흡착을 정량 → **흡착 인력은 cage 타입이 아니라 흡착 *면의 크기*가 지배(E_a가 4→6각형에서 ~12→21 kJ/mol로 선형 증가, H-bond ~10 kJ/mol보다 큼 = 흡착이 핵생성 추동력일 수 있음)**; **7각형 이상 면은 흡착 대신 메탄을 통과시켜** 비정질 수화물의 cage 간 메탄 확산을 가능케 한다. → cage 정의(FSICA)의 이론적 근거 + 수화물 성장의 방향성·morphology 함의.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 저자 | Chan-Juan Liu, Zheng-Cai Zhang, Zhi-Gang Zhang, Yi-Gang Zhang, **Guang-Jun Guo**(교신, guogj@mail.igcas.ac.cn) |
| 소속 | Key Laboratory of the Earth's Deep Interior, Institute of Geology and Geophysics, **Chinese Academy of Sciences, Beijing 100029, PR China** |
| 저널/년 | **Chemical Physics Letters 575 (2013) 54–58** (Received 10 Feb 2013; final 7 May 2013; online 16 May 2013) |
| DOI | **10.1016/j.cplett.2013.05.012** |
| 시스템 | **물 클라트레이트 수화물 cage + 메탄(CH₄) 분자** (gas hydrate, *NOT* solid electrolyte) |
| 연구유형 | **classical molecular dynamics (GROMACS), 구속 MD로 PMF 계산** |
| 동기 | 선행연구(Guo et al. ref [11])는 단일 **5¹² (dodecahedral) cage**만 다뤄 **cage 종류·면 크기 효과를 분리 못 함**. 이 논문이 그 두 요인을 분리. |
| 배경 가설 | **CAH(Cage Adsorption Hypothesis, ref [11])**: 용해 메탄이 cage 면에 흡착되는 것이 수화물 핵생성의 추동력. 경쟁가설: LCH(labile cluster, Sloan), LSH(local structuring, Radhakrishnan–Trout). |
| 응용 함의 | 수화물 핵생성/성장 메커니즘, **결정질에서 깨지지 않고 inter-cage로 메탄이 확산하는 통로(7각형 구멍)**, 비정질 수화물·고압 구조전이, 메탄 morphology(바늘형·나선형 결정). |

## 3. 핵심 정량값 (수치 총정리)
> 단위 주의: 이 논문은 **kJ/mol**(에너지), **Å**(거리). σ(S/cm)·eV·Li 같은 값은 **존재하지 않음**.

### 3.1 PMF 첫 우물 깊이 / 특성 거리 (오각형 면, §3.1)
| 항목 | 값 | 비고 |
|---|---|---|
| 5¹² cage 오각형 면 첫 우물 깊이 | **−15.2 kJ/mol @ 2.8 Å** | 빈 A cage(SA[0]F5M) 제외 모든 cage 거의 동일 |
| 첫 장벽 위치 | **~5.6 Å** | |
| 둘째 우물 위치 | **7.6 Å** | (선행 ref[11]: 2.9 / 5.7 / 7.1 Å — Δr_c 3.1 Å 보정 후 일치) |
| A cage(작은 불완전 [5²6³]₅) | 첫 우물 동일, **둘째 우물 훨씬 얕음** | 큰 cage-구조 형성 능력↓ 시사 |

### 3.2 면 크기 → 활성화에너지 E_a (4¹5¹⁰6² G cage, Table 1, Fig 4) — **핵심 표**
| Case (면 종류) | 첫 우물 r (Å) | 첫 우물 PMF (kJ/mol) | 첫 장벽 r′ (Å) | 첫 장벽 PMF (kJ/mol) | 둘째 우물 r″ (Å) | 둘째 우물 PMF (kJ/mol) | **E_a (kJ/mol)** |
|---|---|---|---|---|---|---|---|
| SG[M]_F4_M (**4각형**, tetragonal) | 3.2 | −10.8 | 5.6 | 0.9 | 7.8 | −0.4 | **11.7 ± 0.4** |
| SG[M]_F5_M (**5각형**, pentagonal) | 2.8 | −15.0 | 5.6 | 1.5 | 7.6 | −0.6 | **16.5 ± 0.3** |
| SG[M]_F6_M (**6각형**, hexagonal) | 2.4 | −19.7 | 5.4 | 1.6 | 6.8 | −0.9 | **21.3 ± 0.5** |
- **E_a vs 면 정점수 N_v 선형**(Fig 4): 4→5→6각형으로 E_a ≈ **11.7 → 16.5 → 21.3 kJ/mol**. 정점 1개 추가 ≈ **+4.8 kJ/mol** 안정화.
- 비교 기준: **수소결합 1개 ≈ 10 kJ/mol** (ref [28]). 모든 면의 E_a > H-bond 1개; **6각형 면 E_a는 H-bond의 2배 이상** → cage–메탄 흡착이 핵생성 추동력일 수 있다는 정량 근거.
- **면이 클수록**: 첫 우물이 흡착면에 **더 가까워지고 더 깊어짐**(2.4 Å에서 −19.7) = 더 강한 흡착.

### 3.3 큰 면 cage: 흡착 → 통과 전이 (P/Q cage, Fig 5, §3.3)
| Cage / 면 | 거동 | 핵심 수치 |
|---|---|---|
| RG[0]F4/F5/F6 M (G cage, 비교용) | 흡착(우물 바깥) | 첫 우물 +쪽(흡착면 바깥) |
| RP[0]_F7_M (**7각형** 면, P cage 4¹5⁷6²7¹) | **흡착 우물이 흡착면 안(~1.6 Å)으로 이동**, 좌측 반발이 **낮은 장벽으로 퇴화** | 메탄이 면을 통과(cross); 7각형 = **지그재그 통로**(낮은 PMF 장벽이 면 중심) |
| RQ[0]_F8_M (**8각형** 면, Q cage 4⁴5⁶6³8¹) | **낮은 장벽조차 사라짐** = 메탄이 자유 통과 | 8각형은 충분히 커서 메탄 그냥 통과 |
| (P/Q cage 내부 안정 위치) | 메탄이 cage 안에 들어와 앉음 | 깊은 우물 ~−2.0 Å(면 안쪽, 음의 r = 흡착면 내부) |

→ **임계 = 7각형**: 6각형까지는 *흡착*(가둠), 7각형부터는 *통과 허용*. 이것이 **face-saturated incomplete cage analysis(FSICA, ref[17])**의 정의(3·4·5·6각 물고리 = "cage face"; 7각 이상 = "cage hole")의 이론적 정당화.

### 3.4 cage 종류 효과 (거의 없음, §3.1–3.2)
- 오각형 면 6종 cage(A/D/G/L/S/T) PMF 거의 동일 — **불완전 A cage만** 메탄에 **약간 약한** 인력(둘째 우물 얕음).
- L cage(큰 cage)는 D cage보다 미세하게 약한 인력, A cage가 최약(SI Fig S3, ab initio 교차상호작용 ref[26]으로도 확인).
- 결론: **같은 크기 면이면 cage 종류·면 위치는 흡착에 거의 무관** → 면 *크기*만 본질.

## 4. 재료 & 방법 (classical MD) ★
> 우리(DFT/AIMD/MLIP)와 **완전히 다른 계산 패러다임** — force-field 고전 MD. 비교 시 이 점 반드시 명시.

- **code**: **GROMACS** (ref [20,21], v4.0.7 manual). *(plane-wave DFT 아님, force field MD)*
- **force field(우리의 functional/pseudo 대응물)**:
  - 물 = **TIP4P/2005** (ref [22])
  - 메탄 = **OPLS-UA**(united-atom) (ref [23])
  - 물–메탄 교차상호작용 = **modified Lorentz–Berthelot**(χ = 1.07, ref [24]); 추가로 ab initio 교차상호작용(R. Sun & Z.D. Duan, ref [26]) 검증
- **앙상블 / 열역학 상태**: **NPT**, Nosé–Hoover thermostat + Parrinello–Rahman barostat(둘 다 τ = 0.8 ps); **T = 258.5 K, P = 30 MPa**(메탄 수화물 상영역, state point ref [25])
- **시스템**: 직육면체 **45 × 30 × 30 Å**, cage 1개 + 메탄 2개 + 물 **1240개**
- **컷오프 / 장거리**: LJ 컷오프 **10 Å**; 장거리 정전 = **PME**(실공간 컷오프 10 Å, spline order 4, Fourier 간격 1.2 Å); PBC 전방향
- **PMF 계산(이 논문의 핵심 "post-processing"=주 방법)**:
  - **구속 MD(constrained MD)**: cage–메탄 거리를 r_c로 고정하고 구속력 F(r_c) 측정 → PMF(r₂) = −∫F(r_c)dr_c (식 1–2). **SHAKE**(거리 구속) + **COM pulling**(GROMACS)으로 두 그룹 구속력 출력.
  - **회전 엔트로피 보정**: cage+메탄 조합 회전이 엔트로피 기여 → 원 PMF에서 **2k_BT ln r_c 빼서 보정**(ref [21]).
  - **샘플링**: r_c = **1–12 Å, 0.2 Å 간격 = 56점**; 각 점 **20개 독립 시뮬 평균**(총 >10 ns/configuration); 각 run 602 ps(초기 2 ps는 0.2 fs 완화, 이후 600 ps는 1 fs, 마지막 500 ps만 F(r_c) 채택). PMF 컷오프 12 Å(선행 10.9 Å보다 보수적).
  - **RDF 도출**: RDF(r) = exp(−PMF(r)/k_BT) (식 3) — 직접 RDF는 sampling 빈약해 불가.
- **무질서 처리(우리의 SQS/enumerate 대응 없음)**: 해당 없음 — 결정 disorder가 아니라 **cage 강성(rigid) vs 유연(soft) 처리**가 변수:
  - **rigid cage** = 위치 구속 + 각도 구속(O–H 0.9572 Å, H–H 1.5139 Å, O–M 0.8712 Å, H-bond 2.82 Å; 면내 인접 O–O–O 각 = 180°×(N_v−2)/N_v).
  - **soft cage** = 거리 구속만. 7·8각 물고리 cage는 시뮬 중 붕괴 방지 위해 **rigid 강제**.
- **cage 출처**: 8종 cage를 Walsh et al.(ref [13])의 수화물 형성 MD 궤적에서 FSICA(ref [17])로 추출. 모서리 길이 2.82 Å(H-bond 평균; 선행 2.75 Å보다 약간 큼).
- **표기법**: `R/S [M/0] F4–8 M/0` — R=rigid, S=soft, 대괄호 안=cage guest(M 메탄/0 없음), 아래첨자 F4–F8=흡착면 종류(tetra/penta/hexa/hepta/octa), 끝=용해 메탄 M(또는 0). 총 **18 case** PMF 계산.

## 5. Cage 타입 (Figure 1, §2)
| Cage 라벨 | 식 (face notation) | 설명 |
|---|---|---|
| **A** | [5²6³]₅ | 정점 2개만 공유한 **불완전 cage**(5·6각 면, 메탄 용액서 핵생성 전 가장 흔, ref[17]) |
| **D** | **5¹²** | dodecahedral, **가장 흔한 cage**(12 오각형), sI 수화물 주 cage |
| **G** | **4¹5¹⁰6²** | 4·5·6각 면 모두 포함, 핵생성 시 매우 풍부 → **E_a–면크기 정량의 주역**(Table 1) |
| **L** | 5¹²6⁸ | 큰 cage 예시 |
| **P** | 4¹5⁷6²**7¹** | **7각형 면 1개** 포함 |
| **Q** | 4⁴5⁶6³**8¹** | **8각형 면 1개** 포함 |
| **S** | 4³5⁹6³ | 작은 cage(4·5·6각) |
| **T** | **5¹²6²** | sI 수화물 주 cage(tetrakaidecahedron) |

## 6. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 메시지 / (우리에게 전이 가능한 개념 — analogy-only) |
|---|---|---|
| **1** | 8종 cage 구조(빨강=물 O, 회색=메탄, 노랑 막대=흡착면 H-bond). A/D/G/L/P/Q/S/T. | cage·면 어휘 정의. *개념*: "guest를 가두는 다면체 cage"라는 framing(↔ argyrodite PS₄ cage). |
| **2** | 6종 cage의 **오각형 면** cage–메탄 PMF. | **PMF가 cage 종류에 거의 무관**(A cage만 둘째 우물 얕음). 첫 우물 −15.2 @2.8 Å. *개념*: 흡착세기는 cage 정체성이 아니라 **국소 면/window**가 결정. |
| **3** | **G cage(4¹5¹⁰6²)**의 **다른 면**(4/5/6각형) PMF 비교. | **면이 클수록 첫 우물이 흡착면에 가까워지고 깊어짐** = 강한 흡착. *개념*: **window 크기 → 자유에너지 우물 깊이/장벽** 직접 대응. |
| **4** | **E_a vs 면 정점수 N_v**(4/5/6) 산점+선형 피팅. | **E_a ∝ 면 크기**(11.7→16.5→21.3 kJ/mol, 정점당 +4.8). H-bond(10) 초과. *개념*: **window가 넓을수록 흡착(가둠)이 강함** — 즉 작은 window가 통과를 막는다(↔ Li bottleneck). |
| **5** | **P(7각)·Q(8각) cage** PMF, G cage와 비교. | **7각 면 = 낮은 장벽(지그재그 통과), 8각 = 장벽 소멸(자유 통과)**. *개념*: **임계 window 크기 이상이면 guest가 cage 사이를 *cross*(inter-cage 확산)** — guest 이동의 통로 = 큰 window. |
| **SI S1/S2** | 다른 cage들의 4각·6각 면 PMF. | 오각형과 동일하게 cage 종류 무관. |
| **SI S3** | ab initio 물–메탄 교차상호작용으로 재계산한 cage 타입 PMF. | L cage 약간 약함, A cage 최약 — force field 결론 robust. |
| **SI S6**(ref[17]) | 두 개의 7각 구멍 cage가 융합 → 메탄이 구멍 통과(면 안 깨고). | 비정질 수화물 inter-cage 확산 통로 직접 시각화. |

## 7. ⭐ 개념적 유추 (NOT 같은 물리) — 보관 이유
> **이 문단이 사용자가 이 논문을 남긴 이유다. 엄격히 *멘탈모델*로만 사용 — 우리 재료를 검증하지 않는다.**

이 논문의 **핵심 발상**은 깨끗하다: **"다면체 cage의 *면(window) 크기*가, guest가 그 cage에 *갇혀-흡착*되는지 아니면 cage 사이를 *통과*하는지를 결정하고, 그 경계를 PMF 자유에너지 장벽(우물 깊이·장벽 높이·E_a)으로 정량할 수 있다."** 면이 작으면(≤6각) guest는 가두어지고(깊은 우물, 높은 E_a), 면이 임계(7각)를 넘으면 통과한다(장벽 소멸).

이것은 우리 argyrodite **Li⁺ inter-cage 이동**을 *생각하는 방식*으로 그대로 옮겨 쓸 수 있는 **순수 개념 틀**이다 — Li⁺가 PS₄ cage 사이를 hop할 때 그 **"창(window)"**(48h–48h–48h doublet 경로, 그리고 그 창을 둘러싼 free-S²⁻·halide 배치)의 **유효 크기/조임 정도가 Li⁺ hopping 장벽을 설정**한다는 직관. 작은/막힌 창 = 높은 장벽(느린 inter-cage 이동); 넓은/열린 창 = 낮은 장벽(빠른 이동). 정확히 우리 cascade의 두 BVSE/tier2 기술자가 측정하려는 그 양이다:
- **`migration_volume_fraction`** (cascade BVSE bottleneck volume) ↔ 이 논문의 "**window 크기**"의 우리 버전(BVSE iso-surface로 본 Li⁺가 통과 가능한 *부피 분율* = 유효 창 단면).
- **tier2 `dopant_blocking_fraction`** ↔ 이 논문 식으로 말하면 **"dopant가 inter-cage 창을 좁혀(↔ 면을 7각→6각→4각으로 *줄이듯*) PMF 장벽을 *올리는*"** 정도. 우리의 high-valence dopant blocking(안정성↔이동도 trade-off)을 *왜 일어나는가*로 직관화: **dopant가 inter-cage bottleneck 위/근처에 앉아 Li⁺의 "window"를 조이면 장벽↑·이동도↓** — 이 논문이 "면이 작아질수록 흡착(가둠) E_a↑"로 보여준 것과 같은 *방향의 정성 논리*.
- **tier2 `li_li_disorder_std`** ↔ 창 주변 환경의 *불균일*이 장벽 분포를 넓힌다는 그림(이 논문 Fig 2가 "cage 종류 무관, 국소 면이 지배"를 보인 것과 결이 같음 — 멀리 있는 framework가 아니라 *국소 window*가 장벽을 정한다).

**왜 이것이 *검증이 아니라 유추뿐*인가 (정직한 경계):**
1. **시스템이 다르다**: 물-cage / 중성 CH₄ vs PS₄-cage / Li⁺ 양이온. 가두는 주체·통과하는 주체가 물리적으로 다른 종.
2. **상호작용이 다르다**: 여기 인력 = **수소결합 + van der Waals(분산)** (kJ/mol 규모, 인력 우물). 우리 Li⁺ = **이온 결합/정전 + 격자 변형** (BVSE bond-valence 미스맷·정전 장벽). 부호·기원이 다름 — 메탄은 *흡착*(인력)이 핵심, Li⁺는 *반발 장벽 통과*가 핵심.
3. **방법이 다르다**: classical force-field MD PMF(258.5 K, 30 MPa, GROMACS) vs 우리 BVSE(정전 bond-valence)·AIMD/MLIP(UMA)·NEB. PMF 자유에너지(엔트로피 포함, 유한 T)와 우리 BVSE(0 K 정전 landscape)·AIMD(유한 T MSD)는 *직접 등가가 아님*.
4. **수치 전이 0**: 이 논문의 11.7–21.3 kJ/mol(≈0.12–0.22 eV)이 *우연히* 우리 Li Ea(~0.22–0.25 eV) 스케일과 비슷해 보여도 **완전히 무관한 양**(메탄 흡착 자유에너지 vs Li hop 장벽). **절대 같은 표에 놓거나 "일치"라 말하지 말 것.**

> **한 줄 결론**: 이 논문은 우리 재료에 대해 *아무것도 입증하지 않지만*, **"face/window 크기 → inter-cage 전이 장벽"** 이라는 **전이 가능한 사고 틀**을 준다 — 우리 `migration_volume_fraction`(창 크기)과 `dopant_blocking_fraction`(창을 좁히는 dopant)이 *왜* Li⁺ inter-cage 이동도를 좌우하는지 *말로 설명*할 때 쓰는 비유로만.

## 8. 결론 (논문 자체)
1. cage–메탄 흡착 세기는 **cage 종류엔 거의 무관**(불완전 A cage만 약간 약함), **흡착 *면 크기*에 강하게 의존**(4→6각형 E_a 11.7→21.3 kJ/mol, 선형).
2. **면이 클수록 첫 우물이 흡착면에 가까워지고 깊어짐** → **5¹²(작은 면) 외의 *큰 면* cage가 핵생성 시 메탄을 더 잘 흡착** → 수화물 성장에 **방향성**(preferential direction) 존재 시사(바늘·나선 결정 morphology 설명 가능성).
3. **7각형 면이 임계**: 6각까지는 흡착(가둠), 7각부터는 메탄을 **통과**(cross)시킴(7각=지그재그 낮은 장벽, 8각=장벽 소멸). → cage란 "**guest를 가두려면 self-enclosed(3–6각 면만, 구멍 없이)여야 한다**"는 FSICA 정의의 **이론적 근거**.
4. **함의**: 결정질 수화물에서 메탄 inter-cage 확산은 5·6각 면이 *깨져야* 가능하나, **비정질 수화물은 7각 구멍 cage를 포함해 면을 깨지 않고 메탄이 확산**할 수 있다 → 비정질 중간상·고압 구조전이 이해에 기여.
5. (후속 예고) 다른 guest(CO₂·H₂·C₂H₆·C₃H₈·THF·불활성기체 He/Ne/Ar/Kr/Xe)의 cage-guest 흡착으로 확장 예정.

## 9. 인용 가능 문장 (analogy framing 전용 — 절대 "materials comparison"으로 인용 금지)
- *(개념 비유로만)* "A clathrate-hydrate MD study (Liu 2013) provides a transferable mental model — the *size of a cage face/window* sets, via a PMF free-energy barrier, whether a guest is trapped-and-adsorbed or can cross between cages; by loose analogy this is how we *describe* (not compute) why our BVSE `migration_volume_fraction` (effective inter-cage window) and `dopant_blocking_fraction` (a dopant narrowing that window) govern Li⁺ inter-cage hopping in argyrodite — different system, bonding, and method; no quantitative transfer."
- *(논문 자체)* "Cage–guest adsorption strength scales with the *adsorption-face size* (E_a ≈ 12→21 kJ/mol from 4- to 6-membered faces), and a ≥7-membered face stops trapping the guest and instead lets it cross — defining the window threshold between confinement and inter-cage transport."

## 10. 주의/한계 (over-claim 방지)
- **이 논문은 argyrodite·고체전해질·Li⁺ 전도와 물리적으로 무관**. §7의 연결은 **순수 개념 유추**이며 우리 재료/수치를 *검증하지 않음*.
- 단위·양이 전혀 다름: kJ/mol 메탄 *흡착 자유에너지* vs eV Li *hop 장벽*. **수치 대조·"일치" 주장 금지.**
- classical force-field MD(TIP4P/2005+OPLS-UA)는 **전자구조 없음** — 우리 DFT/MLIP과 방법론적으로 다른 층위.
- 단일 cage + 2 메탄 + 1240 물의 **묽은-용액 흡착** 모델 — bulk 수화물 결정의 협동적 핵생성·격자 전체는 직접 다루지 않음(저자도 명시).
- PMF는 특정 state point(258.5 K, 30 MPa)·특정 cross-interaction(χ=1.07)에 의존 — force field/state 민감.
- "preferential direction / 큰 면이 더 흡착"은 *흡착 자유에너지* 논거이지 *핵생성 속도* 직접 측정이 아님(가설 정량 지지 수준).

## 11. 기법 용어 미니사전
- **Clathrate hydrate(가스 수화물)**: 물 분자 수소결합 망이 만드는 다면체 공동(cage)에 작은 기체 분자(guest)가 갇힌 결정. 메탄 수화물 = 영구동토·해저에 대량 존재, 잠재 에너지원.
- **Cage / face(window)**: 물 O 다면체 cavity / 그 면을 이루는 물고리(4·5·6·7·8각). 면이 흡착·통과 게이트.
- **Guest**: cage 안/면에 흡착되는 분자(여기선 메탄 CH₄).
- **PMF (potential of mean force)**: 반응좌표(여기 cage–메탄 거리)에 따른 *자유에너지* 곡선. 우물=안정, 장벽=전이상태. 본문 핵심 척도.
- **E_a(흡착)**: PMF 첫 우물→첫 장벽 자유에너지차. cage–메탄 흡착 세기 정량(↔ H-bond ~10 kJ/mol 기준).
- **Constrained MD / SHAKE / COM pulling**: 거리 r_c 고정 후 구속력 측정 → 적분해 PMF. SHAKE=결합/거리 구속 알고리즘, COM pulling=무게중심 끌기.
- **CAH (Cage Adsorption Hypothesis)**: cage가 면에 guest를 흡착하는 것이 수화물 핵생성 추동력이라는 가설(Guo et al.). 경쟁가설 LCH·LSH.
- **FSICA (face-saturated incomplete cage analysis)**: 3–6각 물고리=cage face, 7각 이상=cage hole로 정의해 cage를 식별하는 방법(ref[17]). 이 논문이 그 정의를 이론적으로 뒷받침.
- **TIP4P/2005 · OPLS-UA**: 각각 물·메탄의 고전 force field 모델(전자구조 없는 경험 퍼텐셜).
- **rigid vs soft cage**: cage 물분자에 위치+각도 구속(rigid) vs 거리만(soft). 7·8각 cage는 붕괴 방지 위해 rigid.

---
*(EXTERNAL/off-topic 보관. argyrodite 물성 4축·[우리 그룹]·comparison_vs_ours machinery에 포함하지 않음. §7 연결은 analogy-only.)*
