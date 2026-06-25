# Cascade v23 — 문헌 기반 검증·novelty·reconciliation (2026-06-25)

47-dopant UMA cascade 결과를 문헌(로컬 litdb + 웹)과 대조: **무엇이 검증됐고, 무엇이 novel이며, 문헌이 어디를 교정하는가.** 데이터: `db/properties/cascade_v23_*.csv`, figures `docs/figures/cascade/`.

---

## 1. 문헌이 검증하는 우리 결과 ✅

| cascade 결과 | 문헌 근거 |
|---|---|
| **site 메커니즘** 고가전자(Si/Ge/Sn/Ti/Nb/Ta/V/Sb)→**P_4b**, RE/3가/2가→**Li-site** | `dopant_site_preference_literature.md`: Si/Sn(cited DOI 10.3390/ma16072751), Ge/Ti/Nb/Ta/V/Sb(standard isovalent→P⁵⁺); Al(cited 7.29mS/cm)·Y·Ca·Ba·Nd·La(cited)→Li. **거의 완전 일치.** |
| **Hf/Zr가 trade-off 탈출(Li-site)** | 문헌: Hf⁴⁺/Zr⁴⁺ **amphoteric**(charge→P, radius 0.71≈Li→Li). 우리 HfO₂→Li_24g·저-blocking 정확히 설명. |
| **O는 deep spectator·S_16e 자리** | Lee 2025(cited, S2405829725000790): O가 PS₄의 16e Wyckoff에 site-selective. |
| **late-TM(Fe/Co/Ni/Mn) 회피** | 문헌: 3d-TM **격자치환 미확인 — FeS/CoS/NiS 상분리 위험**. 우리 "창 붕괴"에 더해 **상분리까지 = 이중으로 나쁨**. |
| **O-doping 작동** | ACS AMI 2021(Pham, acsami.1c14573): **Li₆PS₄.₇₅ClO₀.₂₅ = 4.7 mS/cm > 무도핑 4.2**, x=0.25 최적. |
| **co-doping 방법론** | Al-Cl(Yu 2022, 7.29mS/cm)·**ZrCl₄**(Bull.KCS 2025, P-site Zr+Cl halide 이중역할)·F+I dual-anion(JPCC 2023). |

## 2. ★★ 결정적 reconciliation — 농도(x) 의존성

**우리 cascade는 전부 x=0.25(과도핑)에서 돌았다** (50-atom 셀의 1-unit 최소치). 문헌이 이걸 교정:

> **저농도(x~0.05–0.1)**: aliovalent 도펀트가 **Li vacancy 생성 → σ 향상** (문헌: "Ca²⁺/Al³⁺ at Li generates vacancies which improve Li⁺ diffusion"; Mg/Ba/Zn/Al/Y 다 σ↑).
> **고농도(x=0.25, 우리)**: 큰 immobile 양이온이 **Li 경로 차단(blocking)** 우세.

→ **우리 cascade의 blocking 랭킹은 "과도핑 regime" 거동**이고, **실험 최적(저x)에선 같은 도펀트가 오히려 σ를 올릴 수** 있다. **blocking 절대값으로 도펀트 기각 금지** — "고농도서 차단" trend만 유효. (이미 알던 x=0.25 한계 + 문헌이 메커니즘적으로 확증.)

이건 **dual-x 후속 스크린**(x=0.05 vs 0.25)으로 vacancy↔blocking 전환점을 잡으면 강력한 결과가 됨.

## 3. 우리가 기여하는 novelty 🆕

| 우리 결과 | 문헌 상태 → novelty |
|---|---|
| **Sc₂O₃·Gd₂O₃ 등 RE-oxide를 *sulfide* argyrodite에 도핑** | RE는 **halide 전해질**(Li₃TmCl₄Br₂)엔 있으나 **sulfide LPSCl 도핑 보고 없음** → **novel 스크린**. (La/Nd만 cited.) |
| **47-도펀트 × (안정성·산화창·Li이동도·기계) 동시 스크린** | 단일 논문이 4축 다 보는 건 없음 → **systematic 기여**. |
| **dual-METAL 부격자 co-doping** (Ta⊕Gd: P-site⊕Li-site) | Sn-O(양이온+음이온)·ZrCl₄(양이온+halide)는 있으나 **두 금속을 P+Li 부격자에 분리 배치**는 미보고 → **novel 설계규칙**. |
| **oxyfluoride (O+F) co-doping** | O-doping·F+I dual-anion 따로는 있으나 **O+F 조합 미보고** → novel. |

## 4. ★ 우리 co-doping 가설의 직접 선례 — Sn-O dual doping

**Sn-O dual-doped argyrodite** (J. Energy Chem., S2095495620307890): **P-site Sn⁴⁺ + anion O²⁻** 동시 도핑 → **σ 향상 + Li금속 계면 적합성 강화 + dendrite 억제.** 
→ 우리 **"안정자⊕전도자"·"이중부격자" co-doping**의 **방법론적 선례**. 문헌 결론 그대로: *"dual co-doping이 σ·안정성·Li이동도를 complementary 메커니즘으로 동시 개선."* 우리 가설(Sc₂O₃⊕Li₂O, Ta₂O₅⊕Gd₂O₃)이 같은 논리 → **검증가능·합리적**.

## 5. 문헌이 준 새 descriptor

- **r/r(S²⁻) = 0.20–0.30 기준**(웹): P-site 도펀트 최적 lattice distortion 범위. r(S²⁻)=1.84 → r=0.37–0.55 Å = 소형 고가전자(Si 0.40·Al 0.535·Ge 0.53). **우리 z/r·radius 분석과 정합** + 정량 cutoff 제공.

## 6. 새 testable 예측 (cascade + 문헌 결합)

1. **dual-x 스크린(x=0.05 vs 0.25)** → vacancy↔blocking 전환 잡기. (문헌 §2 직접 검증.)
2. **Sc₂O₃·Gd₂O₃ sulfide 도핑 실측** → novel, 우리 예측(안정·산화·연성 상위) 검증.
3. **Ta₂O₅⊕Gd₂O₃ dual-sublattice 합성** → Sn-O 선례 따라 σ+안정 동시 기대.
4. **Cr₂O₃ = 코팅 한정**(blocking 0.89, 벌크 부적합) — 박막 cathode coating으로만.

---

## 인용 (citable)
| 출처 | DOI/ID | 핵심 |
|---|---|---|
| Pham et al. ACS AMI 13, 51850 (2021) | 10.1021/acsami.1c14573 | O-doping LPSCl 최적 x=0.25, 4.7 mS/cm |
| Zhao et al. SSI 401 (2023) | 10.1016/j.ssi.2023.116333 | 액상 O-doping 전기화학 안정성 |
| Yu et al. Nanomaterials 12, 4355 (2022) | 10.3390/nano12244355 | Al-Cl co-doping 7.29 mS/cm |
| Ko et al. Bull. Korean Chem. Soc. (2025) | 10.1002/bkcs.70185 | ZrCl₄ co-doping (P-site+halide 이중역할) |
| **Sn-O dual-doped argyrodite** J. Energy Chem. | S2095495620307890 | **P-site Sn + O anion → σ·Li안정·dendrite** (우리 co-doping 선례) |
| F-I dual-doped argyrodite, JPCC (2023) | 10.1021/acs.jpcc.3c00962 | dual-anion 도핑 선례 |
| Li₃TmCl₄Br₂ rare-earth halide | S0378775326004817 | RE는 halide 전해질(우리 RE-sulfide와 대조=novelty) |
| (로컬) dopant_site_preference_literature.md | — | site 메커니즘 cited/standard/analogy 14/15/24 |

> **한 줄**: cascade의 **site 메커니즘·O-doping·co-doping 방법론은 문헌 검증**, **RE-oxide sulfide 도핑·dual-metal-부격자·oxyfluoride는 novel**, 그리고 **결정적으로 우리 x=0.25는 과도핑 regime**이라 blocking은 고농도 trend일 뿐 — 저x에선 vacancy로 σ↑(문헌). **dual-x 스크린이 다음 1순위.**
