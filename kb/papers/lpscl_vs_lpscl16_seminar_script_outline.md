# LPSCl vs LPSCl₁.₆ 세미나 — 발표 개요 + 통합 대본 (2026-06-11)

> `lpscl_vs_lpscl16_seminar_v1.md` (master)에서 ★ ACTIVE 스크립트만 발표 순서대로 추출한 실전용 문서.
> as-built 상태: 실제 PPT(연구실 템플릿) 기준. 수치 변경 시 master가 우선.

---

## 1. PPT 개요 (발표 순서)

| # | 슬라이드 | 핵심 메시지 | as-built | 시간 |
|---|---|---|---|---|
| 1 | Title (연구실 템플릿) | 인사 + DFT 파트 technical report | ✅ FINAL | 15s |
| 2 | Scope + Thesis | 실험 σ ~3× / E +25% → 원인은 전자구조 ✗, Li 공공 + 4d-Cl AS ✓ | ✅ FINAL | 75s |
| 3 | 3-Tier Pipeline | Rietveld 분율 → 정수 occupancy 절차 (MLIP→DFT→post) | ✅ FINAL | 90s |
| 5 | MLIP screening detail | free S²⁻가 Cl⁻ 치환 선호 → 4d-Cl AS 등장, champion 절차 | ✅ FINAL | 40s |
| 6 | DFT validation detail | BM3 EOS 11-vol, 부피 −4.3%인데 B₀↓ = decoupling 신호 | ✅ FINAL | 30s |
| 7 | Headline 표 (post-processing) | 9행 한눈 비교 + 4 messages 선언 | ✅ 검수 FINAL | 65s |
| 8 | M1: 전자구조 거의 동일 | gap Δ0.06 eV, character 동일, defect band 20× | 다음 차례 (DOS 그림 필요) | 60s |
| 9 | M2: σ = barrier↓ + prefactor↑ | Ea 0.253/0.224 (Schlem EXACT), D₀ 1.4×, 2.47×≈2.5× | 미제작 | 80s |
| 10 | M2-a: mechanism cartoon | vacancy carrier 직관 | 미제작 | 40s |
| 11 | M2-b: disorder ensemble | matched-d에서 Ea 동일 → ground truth | 미제작 | 60s |
| 12 | M2-c: 저온 no T_cross | 모든 T에서 modelc 우세, RT 4.3× (Zuo 2.4× 정합) | 미제작 | 40s |
| 13 | M3: ionic glue 강화 | Li–Cl +13% (vacancy 69% + AS 31%), 4d-Cl −2.84 eV | 미제작 | 80s |
| 14 | M4: vacancy paradox 해소 | clamped 동일 → relaxed-ion +25%, Kim 2025 정합 | 미제작 | 80s |
| 15 | M4-a: C44 +72% shear lock-in | Cij 분해, 4d-Cl pin | 미제작 | 50s |
| 16 | M4-b: 4 cross-check | B↔B₀, AFM/UPE, 600 K MLIP, method quality | 미제작 | 55s |
| 17 | CC#1: PS₄ universal backbone | 5 probe 모두 Δ≤1% + universal anchor | 미제작 | 55s |
| 18 | CC#2: 결합 길이 반직관 | Li–Cl −3% 짧아짐, per-bond vs per-anion | 미제작 | 75s |
| 19 | CC#3: Voronoi fingerprint | Li ×5.5 흔들림, S 역설적 균질화 | 미제작 | 65s |
| 20 | CC#4: BVSE bimodal | 60.2% Li +15% shift, 5.4 Li/AS | 미제작 | 65s |
| 21 | CC#5: ELF | covalent 0.95 불변 / ionic <0.1 | 미제작 | 60s |
| 22 | k-mesh audit | k=2×2×1 incident → 복구, property k-sens 표 | 미제작 | 65s |
| 23 | Summary 불변↔변화 | covalent skeleton 유지 + ionic ligament 재배치 | 미제작 | 65s |
| 24 | Robust#1: 3-probe convergence | Voronoi+BVSE+LOBSTER 같은 AS 효과 | 미제작 | 65s |
| 25 | Robust#2: Oxidation 4-axis | 축 지정해야 답 — axis 1 DRAW / 2·3 WINS / 4 LOSES | 미제작 | 80s |
| 26 | Robust#3: Constrained ESW | Cl=1.6 sweet spot, 분해반응 0.7 vs 1.75 Li, Zuo 정량 재현 | 미제작 | 80s |
| 27 | Defense#1: 4-tension audit | lit 충돌 4건 모두 method/축 분리로 해소 | 미제작 | 65s |
| 28 | Defense#2: 9-caveat | 어떤 caveat도 4 메시지 안 흔듦 | 미제작 | 50s |
| 29 | Trade-offs & Outlook | 4 trade-off 공통원인 = 4d-Cl AS 양면성 → paper #2 oxide doping | 미제작 | 75s |

- 총 ≈ 30분 (Q&A 별도). **15분 컷**: 1·2·3·7 + M1·M2·M3·M4 + Summary = 9장.
- ※ as-built 4번 슬라이드(divider/목차로 추정)는 master 미기록 — 확인 필요.
- M1 표 주의: VBM/CBM은 **edge 값 (2.48/2.72, 4.24/4.54)** 사용 권장 — gap과 자기일관
  (4.24−2.48=1.76 ✓, 4.54−2.72=1.82 ✓), footnote(EF 2.45 < VBM 2.72)와도 정합.
  자동생성 PPTX의 "peak" 값(1.64/1.84, 5.44/5.72)은 DOS 봉우리 위치라 gap과 안 맞음.

---

## 2. 통합 대본 (★ ACTIVE만, 발표 순서)

### #1 Title (15s)
> "안녕하세요, 오늘 research seminar는 DFT 파트 technical report로, stoichiometric LPSCl과 Cl-rich LPSCl₁.₆ 두 argyrodite의 정면 비교를 다루겠습니다."

### #2 Scope + Thesis (70–80s)
> "비교 대상부터 보겠습니다.
> 왼쪽은 stoichiometric LPSCl, 오른쪽은 Cl-rich 변종 LPSCl₁.₆입니다. 실험적으로 **LPSCl₁.₆가 더 빠르고 더 단단하다**는 게 보고되어 있는데, 그 차이가 어디서 오는지가 이번 파트의 질문입니다.
> 결론부터 말씀드리겠습니다. **전자구조에 작은 차이는 있긴 있습니다. 하지만 그 작은 차이로는 conductivity나 stiffness의 큰 차이를 설명할 수 없습니다.** 차이의 진짜 source는 구조에 있습니다 — **Li 공공과 4d-Cl anti-site 무질서**입니다.
> 구조를 보시면 — 왼쪽 comp1은 **Li가 가득 차 있고 Cl이 전부 4a, 4d에는 free S²⁻만** 있는 깨끗한 ordered 구조입니다. 오른쪽 modelc에서 **두 가지 disorder가 동시에 등장합니다**: Li가 f.u.당 0.6개 빠지는 Li 공공, 그리고 늘어난 Cl이 S²⁻ 자리인 4d로 침입하는 anti-site.
> 두 시스템에 완전히 동일한 multi-probe 파이프라인을 paired로 적용했고, 다음 30분 동안 4개의 메시지로 풀어 드리겠습니다."

보충 멘트(정확성): "+25%는 저희 DFT relaxed-ion 결과고, 실험(Kim 2025 UPE)은 Cl↑→E↑ 경향으로 확인됩니다."

### #3 Pipeline (~90s)
> "Cell configuration을 결정하기 전에, 저희가 처음 기준으로 삼은 건 **'DFT 상에서 가장 안정한 site 배치는 무엇인가, 그리고 그 구조의 기본 물성은 어떤가'** 였습니다.
> LPSCl의 경우 기존 Rietveld로 정해진 CIF 파일들이 있지만, 이건 **상온 측정의 시간·공간 평균**이라 한 자리에 Cl 60% / S²⁻ 40% 같은 분율 점유로 표현됩니다. DFT는 그런 분율 점유를 받을 수 없어요 — **site마다 원자 하나, 정수 occupancy**로 결정해야 합니다. 그래서 셀을 짜기 전에 '어느 site에 어느 원자를 박을지'를 결정하는 별도 파이프라인이 필요했습니다.
> 그래서 만든 게 이 3-tier pipeline입니다.
> **Tier 1, MLIP screening.** 가능한 음이온/Li 배치를 전수 나열합니다 — LPSCl은 C(8,4)=70개, LPSCl₁.₆는 C(10,2)=45개. 그 위에 Li 배치 screening, 500 K Langevin annealing까지 UMA foundation MLIP으로 몇 시간 안에 돌려서 champion을 뽑습니다.
> 여기서 강조하고 싶은 게 — **왼쪽의 ordered는 저희가 '교과서니까' 고른 게 아닙니다.** halogen 배치만 보면 mixed 2/2가 위로 올라오는데, **Li sublattice까지 풀어서 annealing 하면 ordered가 역전해서 ground state로 확정**됩니다. 같은 절차를 Cl-rich에 적용하면 이번엔 4d-Cl anti-site champion이 나옵니다. Deiseroth와 Kraft 이후 실험에서 보고된 4d-site disorder를 **가정하지 않고 절차로 재현**한 거예요. 즉 ordered도 disorder도 저희가 넣은 게 아니라 **조성이 만든 결과**입니다. 오늘 thesis의 첫 번째 근거예요.
> **Tier 2**에서 champion을 DFT 11-volume BM3 EOS로 V₀/B₀ paper-grade(<1 GPa) 확정, **Tier 3**에서 13가지 probe를 양쪽에 똑같이 적용했습니다. 다음 슬라이드부터 결과 보겠습니다."

### #5 MLIP screening detail (~40s)
> "Halogen 단계에서 free S²⁻ 자리가 Cl⁻ 치환을 선호한다는 게 결과로 나옵니다 — 이게 Cl-rich에서 4d-Cl anti-site가 등장하는 직접적 원인이에요. Li sublattice screen은 halogen이 fix된 위에서 Li/vacancy 배치를 다시 전수조사하는 단계고, 500 K annealing이 각 후보를 local ground state로 relax해서 champion을 확정합니다."

### #6 DFT validation detail (~30s)
> "보통 부피가 줄면 단단해질 거라 기대하는데 Cl-rich는 부피 −4.3%이면서 B₀는 26.2→21.7로 내려갑니다. packing과 bonding이 따로 노는 첫 신호 — M4에서 hydrostatic soft / shear +30% stiff로 완전히 풀립니다."

### #7 Headline 표 (60–70s)
> "한 페이지로 전체 결과를 미리 보여드리는 headline 표입니다.
> 가운데 두 열이 LPSCl과 LPSCl₁.₆ 결과, 오른쪽 열이 그 차이가 의미하는 메시지입니다.
> **첫째 — 밴드갭**. 1.76 vs 1.82, 거의 동일합니다. 전자구조에서 큰 차이가 없다는 첫 신호입니다.
> **둘째 — Ea와 확산**. Cl-rich가 barrier도 낮고(0.253 vs 0.224, Schlem 실험 0.25/0.22와 정확 일치) D₀ prefactor도 1.4배 큽니다 — vacancy carrier. 둘이 곱해져 600 K에서 2.5배 빠릅니다.
> **셋째 — ICOHP**. Li–Cl 결합이 13% 강해집니다. 4d-Cl anti-site가 동력입니다.
> **넷째 — Young's modulus**. relaxed-ion에서 25% 단단합니다. 흥미로운 건 B₀ — 등방 압축은 오히려 comp1이 단단해요. vacancy paradox의 핵심 단서입니다.
> 이 4개 메시지를 하나씩 풀어드리겠습니다."

### #8 M1: 전자구조 (55–65s)
> "Message 1, 전자구조는 거의 동일하다.
> 왼쪽이 두 시스템의 DOS overlay입니다. 전체 모양이 거의 똑같습니다. VBM 부근은 양쪽 다 S 3p가 91% 이상, CBM은 S 3p + P 3s + Li 2p 조합으로 동일합니다.
> 갭은 1.76 vs 1.82 — 차이 0.06 eV로 modelc가 약간 wide합니다. 하지만 이 작은 차이로는 conductivity 2.5배, stiffness 25% 차이를 설명할 수 없습니다. 0.06 eV는 300 K kT의 2.3배 정도라 transport나 mechanical에 의미 있는 기여를 못 합니다.
> 흥미로운 게 하나 있습니다. modelc의 페르미 레벨이 VBM보다 아래에 있어요 — 2.45 vs 2.72 eV. 이 사이에 0.74개의 localized state가 있습니다. comp1은 0.037개, 20배 차이. vacancy와 4d-Cl anti-site가 만든 국소 S 3p hole의 실제 흔적 — disorder의 fingerprint입니다.
> 즉 갭은 같지만 modelc에는 disorder의 전자적 fingerprint가 분명히 있고, 그 disorder가 무엇인지가 다음 메시지입니다."

### #9 M2: σ mechanism (75–85s)
> "Message 2, σ 차이의 mechanism. 두 효과가 함께 작용합니다.
> 왼쪽 Arrhenius plot — 3점 모두 깨끗하게 직선 위, comp1 R² 0.9998, modelc 0.992.
> comp1 Ea = 0.253, modelc Ea = 0.224. **Cl-rich가 lower Ea — Minafra/Kraft '구조적 무질서가 barrier를 낮춘다' narrative와 정확히 정합**합니다. 그리고 **Schlem 2020 실험과도 정확 매칭** — LPSCl ordered 0.25, Cl-rich 0.22.
> D₀ prefactor도 4.11×10⁻⁴ vs 5.8×10⁻⁴, modelc가 1.4배 큽니다. vacancy로 carrier density가 늘어난 효과.
> σ 비율 2.5×를 분해하면 — **Ea contribution 1.75×**, **D₀ contribution 1.41×**. 둘 다 같은 방향, 거의 동등 기여. 곱하면 **2.47×, 측정값 2.5×와 거의 정확** 일치.
> 정리: **Cl-rich의 σ 향상은 barrier 감소와 carrier 증가 둘 다에서 옵니다**. 이전에 5 f.u. 인위 supercell로 측정했을 때는 comp1 Ea가 0.172로 비정상적으로 낮게 나와 'prefactor 단독'으로 잘못 해석한 적이 있는데, **자연 4 f.u. cubic으로 재측정하니 Schlem과 정확 매칭되면서 dual mechanism이 확정**됩니다."

### #10 M2-a cartoon (40s)
> "직관 그림으로 정리하겠습니다. 왼쪽 LPSCl은 Li 자리가 가득 차 있습니다. Li 하나가 hop하려면 옆자리가 비기를 기다려야 해요. 오른쪽 LPSCl₁.₆는 공공이 f.u.당 0.6개 — 빈자리가 항상 근처에 있습니다. hop 경로가 상시 열려 있고, 이게 D₀ 차이의 실체입니다."

### #11 M2-b disorder ensemble (60s)
> "앞 슬라이드의 Ea 숫자에는 미묘한 셀 의존성이 있습니다. 그걸 정면으로 해결한 게 disorder ensemble입니다.
> 두 시스템 × 두 disorder 레벨, 2×2 매트릭스입니다.
> 왼쪽 위 — 완전히 ordered한 LPSCl을 600 K에서 돌리면 Li가 사실상 안 움직입니다. 이때 보이는 1.17 eV는 물리값이 아니라 저온 통계 부족 artifact입니다. 진짜 ordered LPSCl은 kinetically frozen이라는 것.
> 핵심은 아래 행입니다. 같은 수준의 anti-site disorder를 양쪽에 넣고 3-config 앙상블로 재면 — 0.177 대 0.173, 사실상 같습니다. 실험 ball-milled 0.16–0.25와 정합.
> 결론: matched disorder에서 per-hop barrier는 두 조성이 같고, natural cell 비교에서의 차이는 Ea와 D₀ 양쪽 — M2의 ground truth입니다."

### #12 M2-c 저온 (40s)
> "저온 특성 한 가지 짚고 갑니다. 표 — Ea와 D₀ 둘 다 modelc 우세 같은 방향. Arrhenius에서 곱하기로 작용해 T 내려갈수록 σ ratio가 커집니다. 1000 K 2×, 600 K 2.5×, RT 4.3×, 200 K 7×.
> 실험 cross-check — Zuo 2023 RT 측정 2.4× ↔ 우리 외삽 4.3×, 자릿수 정합. 결론: 저온 trade-off 없음, Cl-rich가 모든 T에서 우세."

### #13 M3: ionic glue (75–85s)
> "Message 3, ionic glue — Li와 음이온 결합 강도입니다.
> 직관적으로 'Cl 더 넣고 Li 빼면 약해진다'고 생각하기 쉬운데, 결과는 정반대. Li–Cl이 13%, Li–S가 8% 강해집니다. PS₄ covalent backbone은 1%, 불변.
> Li–Cl 13% 강화를 두 단계로 분해할 수 있습니다.
> comp1의 baseline Li–Cl는 −1.86 eV. modelc의 4a 자리 Cl는 −2.03 eV로 9% 강해집니다 — Li 공공이 들어와 ionic field가 전반 강화된 효과, modelc Cl 90%에 균일 적용.
> 그리고 modelc에만 있는 4d anti-site Cl는 −2.84 eV로 40% 강합니다. 짧은 거리 2.45 Å + tetrahedral 배위. Cl 10%에만 적용되지만 per-bond로 매우 intense.
> 합쳐서 +13% 기여도는 vacancy field 69% + anti-site 31%.
> Bader, LOBSTER, Wilkening — 세 독립 probe가 같은 방향을 가리킵니다."

### #14 M4: vacancy paradox (75–85s)
> "마지막 메시지 M4 — 기계적 성질의 paradox와 해소입니다.
> 이온 위치를 frozen으로 두는 clamped-ion DFT로 계산하면 두 시스템 Young's modulus가 정확히 같습니다. 52.31 대 52.30. 실험은 분명 LPSCl₁.₆가 더 단단하다는데 — Kim 2025가 결정적 reference — 이걸 못 잡으니 'vacancy paradox'였습니다.
> strain 시 이온이 재배치되는 relaxed-ion으로 계산하면 풀립니다. modelc 27.66, comp1 22.06 — 25% 차이. comp1의 22.06은 실험 LPSCl ~23 GPa와 거의 정확히 매칭. paradox 해소.
> 분해 표를 보면 — bulk modulus는 modelc가 오히려 8% 약합니다. vacancy가 있으니 등방 압축은 쉬워지는 게 직관에 맞아요. 그런데 shear G가 30% 단단해지고 Zener anisotropy 1.14→1.44.
> 즉 단단해진 건 shear-dominant stiffening입니다. 미시 출처는 4d-Cl anti-site — 짧고 강한 Li–Cl 결합이 특정 shear 모드를 잠가서, ionic sublattice가 강하게 저항합니다. M3의 ionic glue 강화가 mechanical로 발현된 게 M4입니다.
> B_VRH 23.4가 독립적인 BM-EOS B₀ 21.7과 3% 안에서 cross-check되는 것도 paper-grade 근거입니다."

### #15 M4-a Cij 분해 (45–55s)
> "+30% shear가 어디서 오는지 Cij로 풀어보겠습니다. C44가 8.0에서 13.7로 72% 증가합니다. G +30%의 거의 모든 출처가 C44 하나예요. C12도 18% 감소. 반면 C11은 거의 안 바뀝니다 — 그래서 B는 오히려 soft.
> 미시 그림 — 4d Cl이 인접 Li를 2.53 Å에서 강하게 잡아 Li 평면 슬라이딩형 shear 변형을 선택적으로 pin합니다. hydrostatic 압축은 모든 결합을 균등하게 줄여 pin이 안 켜져요. vacancy로 bulk soft, 4d-Cl로 shear stiff — 합쳐서 E는 stiffer."

### #16 M4-b cross-check (50–60s)
> "M4 결론을 4가지 독립 cross-check로 확인합니다.
> 첫째, B_VRH vs B₀ — 전혀 다른 두 방법이 ±10% 일치. 둘째, 실험 — 우리 22는 LPSCl ~23과 매칭, 자체 AFM과 Kim 2025 UPE도 같은 방향. 셋째, 0 K DFT vs 600 K MLIP — 같은 방향 (+13%). 넷째, method quality — spilling 1–1.5%, k×L ≥ 40 Å.
> 4개 다 정합 — relaxed-ion +25%는 robust합니다."

### #17 CC#1 PS₄ backbone (50–60s)
> "Cross-check 시작입니다. P–S 길이 2.073 vs 2.064 (0.5%), 분산은 modelc가 오히려 작고, P 배위 정확히 4.00, ICOHP 1%, ELF 0.946 vs 0.944. 5개 독립 probe 모두 'PS₄는 같다'.
> 마지막 행 — 4d free S²⁻에 붙은 Li 결합도 양쪽 −2.5로 동일한 universal anchor.
> 결론: PS₄³⁻ 단위는 chemistry-independent rigid block, 모든 조성 효과는 Li-halide ionic sublattice 안에서만 일어납니다."

### #18 CC#2 결합 길이 반직관 (70–80s)
> "'Cl이 많아지면 Li–Cl이 멀어진다'는 직관과 정반대 — 0.076 Å, 3% 짧아집니다.
> per-site로 분해하면 4a 정상 자리는 거의 안 변하고, 변화는 전적으로 4d anti-site — 2.45 Å, 4a보다 0.14 Å 짧습니다.
> 4d 자리 두 음이온을 직접 비교하면 — free S²⁻는 Li 6개 octahedral, per-bond −2.57. Cl AS는 Li 4개 tetrahedral, per-bond −2.84. per-bond로는 Cl이 살짝 강해 보입니다 — LOBSTER가 orbital overlap을 측정하기 때문.
> per-anion total로 보면 S²⁻ 6×2.57=−15.4 vs Cl 4×2.84=−11.3 — S²⁻가 36% 강합니다. q=−2의 Coulomb 직관이 회복됩니다.
> 두 양은 다른 물리량이고 paper에서 분리해 정직하게 보고합니다. Li–Cl 짧아짐의 미시 출처가 M3 +13%와 M4 shear stiffening까지 연결됩니다."

### #19 CC#3 Voronoi (60–70s)
> "Disorder가 4개 sublattice에 어떻게 들어가는지 Voronoi 부피 std로 잰 결과입니다.
> comp1에서 P, Cl std 정확히 0 — F-43m ordered 직접 증거.
> modelc로 가면 — P는 0.37로 거의 안 흔들림 (PS₄ 보존). Cl은 0.74로 두 군집 분기 (4a + 4d). Li는 1.15로 5.5배 — 가장 강한 fingerprint. S는 paper의 highlight — std가 오히려 40% 줄어듭니다, 균질화. comp1에서 PS₄-S와 free-S²⁻로 갈라졌던 split을 4d로 들어간 anti-site Cl이 메운 거예요. disorder가 기존 split을 smooth하는 dual effect.
> 이 fingerprint는 BVSE bimodal, LOBSTER ICOHP와 수렴합니다."

### #20 CC#4 BVSE (60–70s)
> "BVSE bond-valence mapping, paired 5×5×5 supercell — 격자·grid·cutoff 완전 동일, 차이는 chemistry 하나.
> comp1은 단일 좁은 peak — 3000 Li가 1.60–1.64. modelc는 bimodal — 39.8%는 comp1-like, 60.2%는 +15% shifted, anti-site 주변 그룹.
> 정량 cross-check — 1626 high-BVS Li / 300 AS Cl = 5.4 Li per AS, Li–Cl 1차 배위 4–6과 정합. BVSE +15%는 ICOHP +40%의 또 다른 정량.
> AS 37.5%는 cubic 5×5×5의 stoichiometry 필연 — 실험 25–50% 범위 내."

### #21 CC#5 ELF (55–65s)
> "ELF, 결합 character의 공간 가시화입니다. 0이면 이온성, 1이면 국소화.
> 두 시스템 동일 패턴 — PS₄ 주위 0.95 적색 maxima (covalent 직접 증거), Li 주위 0.07 (강한 ionic depletion).
> P–S bridge ELF 양쪽 0.95 동일 — covalent character 조성 무관. Li basin floor 양쪽 0.07 — ionic glue 동일.
> 종합 — covalent PS₄ backbone + ionic Li-anion glue가 공존하고, 조성 변화는 ionic 쪽만 재배치합니다."

### #22 k-mesh audit (60–70s)
> "Method-defense입니다. 가장 중요한 건 comp1 k-mesh incident와 복구 스토리.
> 초기에 comp1을 k=2×2×1로 잘못 돌려 gap 1.50이 나왔고, Δgap 0.32가 '조성 효과'로 오해될 뻔했습니다. k=4×4×4 (k×L=40)로 재계산하니 1.76, Δgap 0.06으로 정정 — M1의 정확한 근거. structure RMS 0.003 Å — k 오염은 전자 property만, 구조는 robust.
> property별 k-sensitivity 정리 — B₀·ICOHP robust, gap·elastic·DOS sensitive라 paper-grade 재계산. spilling 1–1.5%, AIMD window 동일 protocol R² 0.99+.
> referee가 method를 물을 모든 지점을 미리 차단합니다."

### #23 Summary (60–70s)
> "Summary — 불변과 변화의 깔끔한 분리.
> 왼쪽 '불변': PS₄ covalent backbone, 밴드갭, Li–S(4d) universal anchor, per-anion Coulomb 직관. 오른쪽 '변화': Li carrier, ionic glue +13%, shear G +30%, 4d-Cl anti-site 새 결합 family.
> Thesis 한 문장 — 'LPSCl → LPSCl₁.₆ 변화는 전자구조가 아니라 구조적 무질서, Li 공공 + 4d-Cl anti-site에서 온다.'
> 4 메시지와 5 cross-check가 모두 같은 그림 — 'covalent skeleton 유지 + ionic ligament 재배치'가 paper #1의 한 문장입니다."

### #24 Robust#1 3-probe (60–70s)
> "4d-Cl anti-site 효과를 세 개의 완전 독립 post-processing이 측정했습니다.
> Voronoi (공간/기하): Cl std 0→0.74, Li ×5.5. BVSE (이동/path): 60.2% Li +15% shift. LOBSTER (결합/chemistry): 4d AS −2.84, +40%.
> 정량 정합 — 5.4 Li/AS = Li–Cl 1차 배위, 60.2% = 5.4×300/2700. 단일 method artifact가 아닌 robust 물리 현상입니다."

### #25 Robust#2 Oxidation 4-axis (75–85s)
> "'Cl-rich가 더 안정한가?' — 단일 답 없음. 4 독립 axis에서 답이 다르고, axis 지정이 필수입니다.
> Axis 1, intrinsic 0-pressure: 양쪽 동일 2.14 V, DRAW. Gil-González K_eff=0과 정합.
> Axis 2, mechanical constraint: Cl-rich WINS — K_eff=20에서 0.80–4.30 V.
> Axis 3, cathode interface cycling: Cl-rich WINS — Zuo R_int 8.9 vs 13.2.
> Axis 4, thermal calendar: Cl-rich LOSES — Wu 2026, 90°C 5일 68% vs 48%.
> 종합: modelc σ 향상은 oxidation penalty 없이 오고, 비용은 thermal shelf life에 있습니다."

### #26 Robust#3 ESW Cl-scan (75–85s)
> "우리 직접 계산이 그 framework를 정량 backing합니다.
> K_eff=0이면 모든 Cl 함량에서 window flat — axis 1 직접 evidence. K_eff 올라가면 Cl 따라 window가 넓어지고 Cl=1.6에서 peak — modelc sweet spot. Cl=2.0은 분해 경로가 바뀌어 다시 좁아짐.
> 분해반응 — comp1은 LiCl 1.0 + Li 1.75 방출, modelc는 LiCl 1.6 + Li 0.7. 더 inert한 LiCl을 더 많이, active Li를 2.3배 적게.
> Zuo 2023 Eq(1)/(2)의 2 Li / 1 Li와 정량 일치 — 우리 grand-potential이 실험 cell chemistry를 재현합니다."

### #27 Defense#1 tension audit (60–70s)
> "paper #1이 문헌과 부딪히는 4 지점을 정직하게 정리합니다.
> ① Oxidation 'Cl-rich 안정' consensus vs 우리 DRAW — 4-axis 분리로 해소. ② Minafra 'disorder→Ea↓' — macro vs micro Ea + disorder ensemble로 mutually compatible. ③ vacancy paradox — clamped vs relaxed method 차이, Kim 2025 직접 정합. ④ gap 절대값 — USPP offset 0.4 eV, 양쪽 동일 적용이라 Δgap robust.
> 4건 모두 'artifact가 아니라 method/축 분리'로 해소됩니다."

### #28 Defense#2 caveats (45–55s)
> "모든 caveat 한 페이지. UMA σ overshoot은 ratio만 사용, Haven=1은 upper bound 표기, 300 K 외삽은 정성, k×L 보장, spilling <5%, n=3 해상도 한계 명시, USPP offset, 0-pressure ESW 한정, random AS placement.
> 요지 — 어떤 caveat도 4 메시지를 흔들지 못합니다. 절대값 영향은 있어도 trend·ratio·mechanism은 robust. 솔직하게 깔아두는 게 가장 강한 referee defense입니다."

### #29 Trade-offs & Outlook (70–80s)
> "마지막 — paper #1을 마무리하고 paper #2로 연결합니다.
> LPSCl₁.₆의 4가지 trade-off는 모두 idle/storage 영역입니다 — thermal calendar (Wu 2026), moisture, synthesis window, mild anisotropy. 흥미로운 건 공통 원인이 M3·M4를 만든 그 4d-Cl anti-site라는 것 — 양면성입니다.
> 전략은 oxide doping — O²⁻의 강한 Li 결합으로 thermal ↑, Cl/O mixed sublattice로 anisotropy 완화. 14 dopant × 3농도 cascade에서 41 champion verified — Sc₂O₃ strongest, B₂O₃·Nd₂O₃ DFT validation 진행.
> paper #1이 mechanism understanding, paper #2가 mitigation engineering — '무질서의 양면성을 이해했으니 이제 design할 수 있다'는 게 묶는 narrative입니다. 감사합니다."
