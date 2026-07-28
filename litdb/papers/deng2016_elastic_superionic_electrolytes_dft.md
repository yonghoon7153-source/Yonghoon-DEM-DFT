# Elastic Properties of Alkali Superionic Conductor Electrolytes from First Principles Calculations — Deng et al. (J. Electrochem. Soc. 2016)

> slug `deng2016_elastic_superionic_electrolytes_dft` · DOI `10.1149/2.0061602jes` · type `DFT (elastic full tensor, 23 SICEs)` · PDF `litdb/inbox/34. Elastic Properties….pdf` (**inbox #34, 사용자 분류 `DFT`**; 최초 digest는 업로드본 "35." 명명 — 동일 논문) · digested `2026-07-28` · **실물 감사 `2026-07-28`** (본문 9 pp = IOP 표지+A67–A74; Table I–III·methods·observations·discussion 전값 digest 일치 — 논문 자체의 LLTO E 262.4(Table II)/262.5(Table III) 반올림 불일치까지 표별 정확; §4.5 인용문 1건 교정 "two neighboring 48h"; **SI(PBE/optB88 전체값) 여전히 미보유 확정**) · status ✅ · **[외부]**
> elements: Li, Na, P, S, Cl, Br, I, O, Si, Ge, Sn, Ti, Zr, Nb, Ta, La
> methods: DFT, elastic
> **저자**: Zhi Deng, Zhenbin Wang, Iek-Heng Chu, Jian Luo, **Shyue Ping Ong*** — **UC San Diego NanoEngineering** (Ong 그룹 = pymatgen/Materials Project 계열; *우리 한양/J-W Lee/Y.M.Lee 아님 → [외부]*). J. Electrochem. Soc. **163**(2) A67–A74 (2016). Submitted 2015-08-31 / revised 2015-10-12 / published 2015-11-05. NSF DMREF 1436976 · XSEDE.

---

## 0. 이 digest를 읽는 법 — 존재 이유는 "Deng=SQS" 2차 귀속의 원문 검증
우리 kb(`kb/concepts/ordered_vs_disordered.md`)·torii2025 digest·`db/properties/elastic.json`(deng2016_reference)·comparison_vs_ours(구 [Kaur] 행)는 전부 **"Deng 2016 = SQS, Zener A=0.92"를 2차 귀속(Torii Table 1 재인용)으로만** 들고 있었다. 이 digest는 원문 8쪽 전체를 실물로 읽고 그 귀속을 판정한다.

> **🔑🔑 한 줄 판정 (먼저 결론)**:
> **(1) 이 논문에 SQS는 없다.** "special quasirandom"·ATAT·enumeration — 단어 자체가 등장하지 않는다. Li₆PS₅X는 **"only the 24g sites are occupied" 가정의 완전 질서 모델**(입방 F4̄3m 대칭 유지 — 그래서 독립 Cᵢⱼ가 3개)이고, 다른 22종도 전부 ordered/end-member 전략이다(§4.5 표).
> **(2) Zener A는 논문 어디에도 없다.** A=0.92는 **유도값**이다 — 인쇄된 PBEsol Cᵢⱼ(C₁₁ 39.9/C₁₂ 23.1/C₄₄ 7.8)로 계산하면 **A = 15.6/16.8 = 0.929 ≈ 0.93** (0.92는 절사값; Torii Table 1 표기로 추정).
> **(3) 부수 발견**: Deng PBEsol Li₆PS₅Cl **E=22.1 / G=8.1 GPa는 우리 relaxed-ion comp1(22.06/8.13)과 사실상 동일(Δ0.2/0.4 %)** — D3 없는 PBE-계열+ordered+relaxed-ion 조합의 외부 최근접 앵커. Torii(PBE-D3, +24 %)보다 우리에 훨씬 가깝다.

## 1. 한 줄 요약
VASP/**PBEsol**(PBE·optB88-vdW 벤치 후 선택)로 **23종 세라믹 알칼리 초이온 전도체(SICE)의 전체 탄성텐서 + B/G/E/ν**를 일괄 계산한 최초의 포괄 reference — **황화물(thiophosphate)이 전 물질군 중 가장 무르고(E<50, B<40, G<20 GPa) 가장 연성(G/B 최저, Li₆PS₅Cl G/B=0.28이 23종 중 최저)**이며, 물질군 순서는 thiophosphate < antiperovskite < phosphate < NASICON < garnet < perovskite, 같은 골격에서 **Na계가 Li계보다 무르다**. 응용 논의: 무른 SE=냉간가압·conformal 접촉, Monroe–Newman 단순 모델로는 전 SICE가 dendrite 차단 가능하나 실제로는 균열이 지배(Nagao).

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 계산 대상 | **23 SICE** (Li·Na) × 6 물질군: NASICON(2)·phosphate(1)·perovskite LLTO(2)·garnet(3)·antiperovskite(4)·thiophosphate(11 — β/γ-Li₃PS₄, LGPS/LSiPS/LSnPS, Li₇P₃S₁₁, **Li₆PS₅Cl/Br/I**, c/t-Na₃PS₄) |
| 갭 | 기계물성 실험은 다결정 E·K_IC만(Wolfenstine LLZO/LLTO, Jackman LATP, Sakuda 유리 E 18–25 GPa) — **full elastic tensor 부재**; 실험값은 수분·porosity·미세구조·2차상에 민감(특히 황화물). 선행 DFT는 LGPS 1건(Wang 2014)뿐 |
| 목적 | (i) functional 3종(PBE/PBEsol/optB88-vdW) 정확도 평가 (ii) 전체 텐서 + 유도 모듈러스 일괄 보고 (iii) 구조·화학 경향 도출 (iv) 제조·작동·Li-metal 함의 논의 — "향후 실험·이론 배터리 모델의 reference" |
| 조성 전략 | **"end members or undoped structures"로 한정** — 고용체·도핑은 의도적으로 배제 (물질군 대표성 확보 목적) |
| 우리와 접점 | Li₆PS₅Cl(=comp1)·Br·I 3종 argyrodite 포함 — 우리 elastic 캠페인(comp1/comp2/modelc)의 문헌 원점, Torii 2025 ref10 |

## 3. 핵심 결과 (수치 총정리)

### 3.1 Functional 벤치마크 — Table I (Li₂S / Li₂O / Na₂S vs 실험)
| 물질 | 방법 | a₀ [Å] | C₁₁ | C₁₂ | C₄₄ | B | G | E | ν |
|---|---|---|---|---|---|---|---|---|---|
| **Li₂S** | PBE | 5.721 | 83.6 | 18.9 | 33.7 | 40.4 | 33.2 | 78.2 | 0.18 |
| | PBEsol | 5.663 | 87.2 | 21.2 | 35.4 | 43.2 | 34.4 | 81.6 | 0.19 |
| | optB88-vdW | 5.693 | 88.0 | 20.9 | 36.1 | 43.2 | 35.1 | 82.6 | 0.18 |
| | **Exp** (10–15 K) | 5.689 | 95.4 | 20.9 | 31.9 | 45.7 | – | – | – |
| **Li₂O** | PBE | 4.656 | 198.6 | 18.8 | 58.6 | 78.7 | 69.6 | 161.3 | 0.16 |
| | PBEsol | 4.596 | 208.7 | 21.5 | 61.1 | 83.9 | 72.5 | 169.0 | 0.16 |
| | optB88-vdW | 4.636 | 207.0 | 25.4 | 62.8 | 85.8 | 72.8 | 170.3 | 0.17 |
| | **Exp** (293 K) | 4.606 | 202 | 21.5 | 58.7 | 81.7 | 69.8 | 162.9 | 0.17 |
| **Na₂S** | PBE | 6.571 | 54.3 | 15.5 | 17.1 | 28.4 | 18.0 | 44.5 | 0.24 |
| | PBEsol | 6.510 | 57.0 | 17.0 | 17.6 | 30.3 | 18.5 | 46.2 | 0.25 |
| | optB88-vdW | 6.521 | 55.8 | 17.2 | 18.5 | 30.0 | 18.8 | 46.7 | 0.24 |
| | **Exp** (30 K, 1977) | 6.537 | 81 | 33 | 21 | 49 | – | – | – |

- **PBE는 격자 ~0.5–1.1 % 과대 → 탄성 과소** (well-known underbinding). PBEsol·optB88-vdW가 격자·탄성 모두 개선.
- **Na₂S만 ~53 % 대괴리** — 저자 판정: 실험 오류 가능성(수분·공기 민감 물질, 1977년 데이터). 세 functional 모두 Na₂S < Li₂S ≪ Li₂O 순서는 재현.
- **→ 본문 결론: "PBEsol이 SICE 탄성 연구에 excellent choice"** — 이하 메인 결과는 전부 PBEsol (PBE/optB88-vdW 전체값은 SI로 — **SI 미보유, n/a**).

### 3.2 다결정 모듈러스 벤치 — Table II (t-LLZO / LLTO / LTP vs 실험)
| 물질 | 방법 | B | G | E | ν |
|---|---|---|---|---|---|
| t-Li₇La₃Zr₂O₁₂ | PBE / PBEsol / optB88 | 116.7 / 127.4 / 150.1 | 63.7 / 68.9 / 75.0 | 161.7 / 175.1 / 192.9 | 0.27 / 0.27 / 0.29 |
| | **Exp** (Al-안정화 **cubic** Li₆.₂₄La₃Zr₂Al₀.₂₄O₁₁.₉₈, porosity 0.03, RT) | 102.8 | 59.6 | 149.8 | 0.26 |
| Li₁/₂La₁/₂TiO₃ | PBE / PBEsol / optB88 | 170.8 / 183.5 / 196.4 | 102.2 / 104.0 / 121.2 | 255.6 / 262.4 / 301.6 | 0.25 / 0.26 / 0.24 |
| | **Exp** (Li₀.₃₃La₀.₅₇TiO₃ 고상) | 133.3 | 80.0 | 200 | 0.25 |
| LiTi₂(PO₄)₃ | PBE / PBEsol / optB88 | 92.5 / 95.0 / 115.1 | 55.6 / 57.6 / 59.6 | 139.0 / 143.7 / 152.5 | 0.25 / 0.25 / 0.28 |
| | **Exp** (Li₁.₃Al₀.₃Ti₁.₇(PO₄)₃ fine-grained) | – | – | 115 | – |

- **DFT가 전 항목 실험보다 유의하게 높음** — 저자 자신이 원인 명시: 실험=다결정(grain size·porosity) vs DFT=무결점 단결정 0 K; 조성 불일치(계산 t-LLZO vs 실험 Al-안정화 c-LLZO — cubic Li₅La₃M₂O₁₂ 계산값이 실험과 훨씬 근접, §3.5 obs.5). **"DFT 단결정 = 상한" 인식이 논문 자체에 내장** — 우리 "DFT > UPE pellet > AFM" 위계와 같은 줄.

### 3.3 메인 결과 — Table III (PBEsol, 23종) 전체 요약 ★
> 독립 Cᵢⱼ만 표기 (cubic 3개 / tetragonal 6 / rhombohedral 6 / orthorhombic 9 / monoclinic 13 / triclinic 21). B/G/E는 VRH, 단위 GPa.

| 조성 | 공간군 | 독립 Cᵢⱼ (주요값) | B | G | E | ν | G/B |
|---|---|---|---|---|---|---|---|
| **NASICON** | | | | | | | |
| LiTi₂(PO₄)₃ | R3̄c | C₁₁ 226.0·C₁₂ 86.7·C₁₃ 43.9·C₁₄ 7.9·C₃₃ 116.3·C₄₄ 48.6 | 95.0 | 57.6 | 143.7 | 0.25 | 0.61 |
| NaZr₂(PO₄)₃ | R3̄c | C₁₁ 175.2·C₁₂ 77.7·C₁₃ 51.9·C₁₄ 9.4·C₃₃ 102.4·C₄₄ 53.2 | 86.3 | 47.7 | 120.9 | 0.27 | 0.55 |
| **Phosphate** | | | | | | | |
| γ-Li₃PO₄ | Pnma | C₁₁ 116.5·C₂₂ 123.9·C₃₃ 127.4·C₁₂ 45.4·C₁₃ 36.5·C₂₃ 62.5·C₄₄ 38.9·C₅₅ 41.1·C₆₆ 53.9 | 72.5 | 40.9 | 103.4 | 0.26 | 0.56 |
| **Perovskite (LLTO)** | | | | | | | |
| Li₁/₈La₅/₈TiO₃ | Pmm2 | C₁₁ 309.6·C₂₂ 335.0·C₃₃ 295.3·C₄₄ 73.1·C₅₅ 89.8·C₆₆ 96.4 | 179.0 | 91.2 | 233.9 | 0.28 | 0.51 |
| Li₁/₂La₁/₂TiO₃ | P2/c | C₁₁ 354.2·C₂₂ 360.4·C₃₃ 351.4·C₄₄ 97.0·C₅₅ 98.2·C₆₆ 77.4 (13개) | 183.5 | 104.0 | 262.5 | 0.26 | 0.57 |
| **Garnet** | | | | | | | |
| Li₅La₃Nb₂O₁₂ | Ia3̄d | C₁₁ 176.7·C₁₂ 78.6·C₄₄ 58.9 | 111.3 | 54.8 | 141.1 | 0.29 | 0.49 |
| Li₅La₃Ta₂O₁₂ | Ia3̄d | C₁₁ 179.6·C₁₂ 78.1·C₄₄ 59.9 | 112.0 | 56.1 | 144.2 | 0.29 | 0.50 |
| t-Li₇La₃Zr₂O₁₂ | I4₁/acd | C₁₁ 196.9·C₃₃ 224.2·C₁₂ 92.7·C₁₃ 86.2·C₄₄ 80.1·C₆₆ 71.0 | 127.4 | 68.9 | 175.1 | 0.27 | 0.54 |
| **Antiperovskite** | | | | | | | |
| Li₃OCl | Pm3̄m | C₁₁ 102.9·C₁₂ 32.1·C₄₄ 46.1 | 55.7 | 41.5 | 99.7 | 0.20 | 0.74 |
| Li₃OBr | Pm3̄m | C₁₁ 91.0·C₁₂ 33.0·C₄₄ 46.6 | 52.3 | 38.5 | 92.8 | 0.20 | 0.74 |
| Na₃OCl | Pm3̄m | C₁₁ 78.1·C₁₂ 15.5·C₄₄ 20.9 | 36.4 | 24.6 | 60.2 | 0.22 | 0.68 |
| Na₃OBr | Pm3̄m | C₁₁ 70.0·C₁₂ 16.0·C₄₄ 21.5 | 34.0 | 23.6 | 57.4 | 0.22 | 0.69 |
| **Thiophosphate** | | | | | | | |
| β-Li₃PS₄ | Pnma | C₁₁ 32.1·C₂₂ 38.1·C₃₃ 51.8·C₁₂ 10.9·C₁₃ 19.7·C₂₃ 17.4·C₄₄ 10.5·C₅₅ 9.5·C₆₆ 13.7 | 23.3 | 11.4 | 29.5 | 0.29 | 0.49 |
| γ-Li₃PS₄ | Pmn2₁ | C₁₁ 53.8·C₂₂ 49.2·C₃₃ 44.9·C₁₂ 23.3·C₁₃ 23.8·C₂₃ 27.3·C₄₄ 12.3·C₅₅ 15.0·C₆₆ 11.7 | 32.9 | 12.6 | 33.4 | 0.33 | 0.38 |
| Li₁₀GeP₂S₁₂ | P4₂mc | C₁₁ 44.9·C₃₃ 51.2·C₁₂ 27.7·C₁₃ 12.6·**C₄₄ 3.5**·C₆₆ 12.4 | 27.3 | 7.9 | **21.7** | 0.37 | 0.29 |
| Li₁₀SiP₂S₁₂ | P4₂mc | C₁₁ 45.7·C₃₃ 50.4·C₁₂ 28.2·C₁₃ 13.2·C₄₄ 5.2·C₆₆ 12.2 | 27.8 | 9.2 | 24.8 | 0.35 | 0.33 |
| Li₁₀SnP₂S₁₂ | P4₂mc | C₁₁ 39.0·C₃₃ 47.7·C₁₂ 26.3·C₁₃ 8.5·C₄₄ 9.4·C₆₆ 14.5 | 23.5 | 11.2 | 29.1 | 0.29 | 0.48 |
| Li₇P₃S₁₁ | P1̄ | C₁₁ 31.8·C₂₂ 26.0·C₃₃ 49.3·C₄₄ 10.7·C₅₅ 13.6·C₆₆ 9.1 (총 21개, off-diag −2.9~+3.2) | 23.9 | 8.1 | 21.9 | 0.35 | 0.34 |
| **Li₆PS₅Cl** | F4̄3m | **C₁₁ 39.9·C₁₂ 23.1·C₄₄ 7.8** | **28.7** | **8.1** | **22.1** | **0.37** | **0.28** |
| **Li₆PS₅Br** | F4̄3m | C₁₁ 40.9·C₁₂ 23.0·C₄₄ 9.6 | 29.0 | 9.3 | 25.3 | 0.35 | 0.32 |
| **Li₆PS₅I** | F4̄3m | C₁₁ 43.6·C₁₂ 23.0·C₄₄ 11.9 | 29.9 | 11.3 | 30.0 | 0.33 | 0.38 |
| c-Na₃PS₄ | I4̄3m | C₁₁ 42.2·C₁₂ 11.1·C₄₄ 11.7 | 21.5 | 13.1 | 32.6 | 0.25 | 0.61 |
| t-Na₃PS₄ | P4̄2₁c | C₁₁ 49.8·C₃₃ 42.9·C₁₂ 11.4·C₁₃ 15.7·C₄₄ 11.1·C₆₆ 11.7 | 25.3 | 13.1 | 33.6 | 0.28 | 0.52 |

### 3.4 Argyrodite 3종 — 유도량 포함 정밀 정리 ★
| 양 | Li₆PS₅Cl | Li₆PS₅Br | Li₆PS₅I | 출처 |
|---|---|---|---|---|
| C₁₁ / C₁₂ / C₄₄ [GPa] | 39.9 / 23.1 / 7.8 | 40.9 / 23.0 / 9.6 | 43.6 / 23.0 / 11.9 | Table III (PBEsol) |
| B / G / E [GPa] | 28.7 / 8.1 / 22.1 | 29.0 / 9.3 / 25.3 | 29.9 / 11.3 / 30.0 | Table III |
| ν / G/B | 0.37 / 0.28 | 0.35 / 0.32 | 0.33 / 0.38 | Table III |
| **Pugh B/G** (유도) | **3.54** | 3.12 | 2.65 | *우리 산술* (28.7/8.1 등) |
| **Zener A = 2C₄₄/(C₁₁−C₁₂)** (유도) | **0.93** (15.6/16.8=0.929) | 1.07 (19.2/17.9) | 1.16 (23.8/20.6) | **⚠ 논문 미보고 — 우리가 인쇄 Cᵢⱼ로 유도** |

- **Cl→Br→I로 C₄₄가 7.8→9.6→11.9(+53 %), E가 22.1→25.3→30.0(+36 %)** — 큰 할라이드일수록 *단단해짐*. **⚠ 이 방향은 실험(Kraft 음속 −24 %, Kim 2025 Br→E↓)·우리 DFT(comp2 Br₀.₅ E −9 %)와 반대** — §7.4에서 정면 대조.
- Li₆PS₅Cl **G/B=0.28은 23종 전체 최저 = 가장 연성(ductile)** (차순위 LGPS 0.29). ν=0.37도 최고 동률(LGPS와).
- 유도 Zener A: Cl만 A<1, Br/I는 A>1 — 셋 다 1 근방(거의 등방).

### 3.5 관찰 6가지 (본문 번호 리스트 그대로)
1. **황화물 SICE는 매우 무르다**: E < 50, B < 40, G < 20 GPa (산화물 대비).
2. **골격 구조·음이온 화학이 1차 결정인자** — 같은 화학은 같은 모듈러스 군집. 순서: **thiophosphate < antiperovskite < phosphate < NASICON < garnet < perovskite**.
3. 산화물 중 **PO₄ 골격(NASICON·Li₃PO₄)이 garnet·perovskite보다 유의하게 무름**.
4. **같은 골격에서 Na계 < Li계 (Na가 더 무름)**: Na₃OX E~50 vs Li₃OX ~100 GPa; NaZr₂(PO₄)₃ < LiTi₂(PO₄)₃; Na₃PS₄는 B·G 모두 Li₃PS₄보다 작음(전체 E는 유사). ⚠ **c-Na₃PS₄는 기본 스텝에서 C₄₄가 음수**로 나옴 — 준안정 cubic 구조의 "collapse"로 해석, **극소 변형 δ=0.05 %로 재계산**.
5. **garnet: t-LLZO(질서) ≫ c-Li₅La₃M₂O₁₂(M=Nb,Ta)** — 계산된 cubic Li₅La₃M₂O₁₂ 모듈러스가 실험 c-LLZO(Al-안정화)와 극히 유사 → **"Li disorder와 그에 따른 구조 대칭이 탄성 모듈러스에 실질 영향" 가설**(저자). Nb/Ta 교체는 영향 미미 — La-O·Zr-O 골격 사이에서 **강한 Li-O 상호작용이 "glue"** 역할.
6. **Pugh G/B (높을수록 취성)**: thiophosphate가 전 화학군 중 최저(<0.5, 예외 c-Na₃PS₄ 0.61) = **가장 연성**; 산화물 대부분 0.5–0.6; **antiperovskite ~0.7 = 내재적 취성**.

### 3.6 Discussion 정량 포인트 (제조 / 작동 / Li-metal)
- **제조**: stiff 산화물(LLTO/LLZO)=고온 소결 필요 ↔ **무른 thiophosphate=냉간가압으로 충분히 치밀**(Sakuda 유리 E 18–25 GPa 인용). 고온 공정 잔류응력은 모듈러스 크기+**이방성**에 의존 → full tensor+EBSD 3D 배향 지도로 국소 잔류응력 평가 가능. 다층 스택=열팽창·모듈러스 차 → delamination.
- **작동**: LiCoO₂ c축 최대 +2.6 %/a,b ~−0.39 %, LiFePO₄ a축 변화 — **무른 SE가 격자변화를 수용하며 접촉 유지**; 단 단단한 산화물은 외부 충격(관통·단락)에 유리 — 트레이드오프.
- **Li-metal (Monroe–Newman)**: "shear modulus twice that of lithium (4.2 GPa)" 임계 기준 — **이 단순 모델로는 본 연구의 모든 SICE(min G=7.9)가 dendrite 기계 차단 가능**. ⚠ 문장 구조상 4.2 GPa가 G_Li인지 임계값(2×G_Li)인지 모호하나, "전 SICE 통과" 결론과 min G 7.9 GPa의 정합상 **4.2=임계값(2×G_Li, G_Li≈2.1)** 독해가 맞음. **그러나** Nagao: Li₂S–P₂S₅ 유리가 >1 mA/cm²에서 균열 + 균열 따라 dendrite 성장(LLZO도 동일 관찰) → **"강성보다 치밀·무균열이 실제 관건"** — 저자 자신이 단순 모델의 한계를 명시.
- 종합: "순수 기계 관점에서는 무른 SE가 접촉 확보·유지에 유리; stiff 산화물의 접촉 문제는 미해결 → 하이브리드(무른+단단 복합) 또는 stiff 산화물+젖음성 액체 제안".

### 3.7 명시적으로 보고 **안 된** 값 (over-claim 방지)
- **Zener anisotropy A**: n/a — §3.4의 A는 전부 우리 유도값. 논문은 이방성을 *정성*으로만(잔류응력 논의).
- **방향성 E/G 분포·ELATE류 시각화**: n/a.
- **sound velocity / Debye / hardness / K_IC**: n/a (K_IC는 문헌 실험값 소환만).
- **relaxed-ion vs clamped-ion 라벨**: n/a — 명시 없음 (§4.3에서 정황 판정).
- **PBE·optB88-vdW의 23종 전체 텐서**: SI로 넘김 — **SI 미보유 → n/a** (본문엔 벤치 3+3종만).
- **Li₆PS₅X의 격자상수**: 본문 미기재(벤치 물질만 a₀ 보고).

## 4. DFT/계산 방법 ★
- **code**: **VASP** (PAW), 전 계산 spin-polarized.
- **functional**: **PBE / PBEsol / optB88-vdW** 3종 비교 → **메인 = PBEsol** (근거: bulk moduli가 격자상수에 민감한데 PBEsol이 PBE보다 격자 재현 우수; optB88-vdW는 non-closed-packed 구조의 vdW 고려용). **D3류 dispersion 보정 없음** (optB88-vdW는 별도 vdW-DF 계열).
- **pseudo/PAW**: PAW (구체 포텐셜 세트 미명시).
- **ecut / 수렴**: **520 eV**, 전자 수렴 10⁻⁶ eV, 힘 수렴 **<0.01 eV/Å** (full relax).
- **k-points**: **grid density 1000 per reciprocal atom** (pymatgen automatic-density 관례).
- **★ 탄성텐서 산출**: **유한 변형(finite distortion) ±0.015 Å 변위 → strain-stress 관계 피팅** (VASP 구현 = Le Page–Saxe 방식, ref 60; IBRION=6 류). **Materials Project 탄성 DB(de Jong 2015)와 10종 물질(LiH·Li₂O·Na₂O·CaS·MgO·Ga₂O₃·AlN·BaZrO₃·SrLiP·Sr₄Si₄Ru — 표기 원문 그대로)로 교차검증, "excellent agreement"**.
- **후처리**: **VRH**(Voigt eqs 1–2 상한 / Reuss eqs 3–5 하한 / Hill 산술평균 eqs 6–7) → B,G; E=9BG/(3B+G) (eq 8), ν=(3B−2G)/(2(3B+G)) (eq 9). **Born 안정성 판정**(positive-definite, Mouhat–Coudert) — 전 계 만족, functional 무관. **전 분석 pymatgen**.
- **AIMD/MLIP/NEB/DOS**: 없음 — 순수 0 K static elastic.

### 4.3 relaxed-ion 여부 판정 (명시 없음 → 정황 3개로 relaxed-ion 판정)
논문은 clamped/relaxed를 구분 표기하지 않는다. 그러나:
1. **방법 계보** — Le Page–Saxe strain-stress + MP workflow(de Jong 2015)와 동일 접근·교차검증: 이 계보는 **변형 셀에서 이온 재이완 후 응력을 읽는 relaxed-ion(total) 탄성**이 표준.
2. **수치 영역** — Li₆PS₅Cl E=22.1/G=8.1은 우리 **relaxed-ion**(22.06/8.13)과 0.2–0.4 % 일치, 우리 clamped(52.31/20.12)와는 2.4× 차. argyrodite처럼 Li 부격자가 무른 계에서 clamped였다면 이 값이 나올 수 없다.
3. **c-Na₃PS₄ "collapse"** — 유한 변형에서 준안정 구조가 무너져 C₄₄<0 → 극소 변형 재계산: 변형 하에서 **이온이 움직였다**는 직접 증거.
→ **판정: 사실상 relaxed-ion (총 탄성).** 단 "논문 명시 아님"을 항상 병기할 것.

### 4.5 ★★ 무질서 처리 — SQS 아님, 전 조성 "질서 모델" 전략 (이 digest의 존재 이유)
> **논문 원문 근거 문장 (argyrodite)**: "In the argyrodite structures, Li-ions are randomly distributed in two types of sites. One of the sites (Wycoff symbol: **24g**) is located at the center of a S₃ triangle with occupancy of 0.26, with **two** neighboring **48h** sites with occupancy of 0.37. **For this work, we assume that only the 24g sites are occupied.**" *(2026-07-28 실물 감사로 교정: 초판 digest가 "three"로 오기 → 원문은 "two"(24g 양옆 48h 쌍 = doublet과 정합); "Wycoff"는 논문 원문 철자 그대로)*

| 물질군 | 실제 무질서 | Deng의 처리 | 비고 |
|---|---|---|---|
| **Li₆PS₅X** | Li 24g(occ 0.26)/48h(occ 0.37) 부분점유 + 4a/4d S/Cl site-exchange | **Li@24g 전점유 가정** (24g×1.0 = Li 24개/셀, F4̄3m 대칭 유지 → 독립 Cᵢⱼ 3개) · **음이온 4a/4d 무질서는 언급 자체 없음** = 이상 질서 배열로 추정 | **SQS 아님**. 24g는 실험상 *소수* 자리(48h가 다수) — 대칭 보존을 위한 인위적 선택 |
| LLTO | Li/La/공공 무질서 | **MP 최저에너지 ordered 구조 2종** | |
| LLZO | c-LLZO는 Li disorder (Ia3̄d) | **질서 tetragonal I4₁/acd** 사용 + 화학양론 cubic garnet Li₅La₃M₂O₁₂(M=Nb,Ta, 질서) | c-LLZO 자체는 회피 — obs.5에서 "Li disorder가 모듈러스에 실질 영향" 가설로 보완 |
| β-Li₃PS₄ | Li 4b/4c 부분점유 | **4b 전점유 가정** | |
| LGPS/LSiPS/LSnPS | Li/M 부분점유 (P4₂/nmc) | **선행 DFT의 ordered P4₂mc 구조** ("to preserve the tetragonal symmetry") | |
| c-Na₃PS₄ | Na 6b(occ 0.8)/12d | **6b 전점유 가정** | |

- **SQS·ATAT·enumeration·"special quasirandom" — 논문 전체(방법·본문·결론)에 등장하지 않음.** 조성 전략 자체가 "end members or undoped, ordered" (§2).
- 물리적 함의: Li₆PS₅Cl의 3-독립-Cᵢⱼ(완전 cubic) 텐서는 **바로 이 24g 전점유 질서 모델의 산물** — 무질서를 넣으면(우리 modelc처럼) 대칭이 깨져 triplet 산포가 생긴다.

## 5. Figure/Table set ★
| 항목 | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **Table I** | Li₂S/Li₂O/Na₂S: 3-functional vs 실험 (a₀·Cᵢⱼ·B/G/E/ν, % 오차 병기) | functional 선택 논거의 표준형 — **"격자 정확도 → 탄성 정확도" 논리** (Torii도 같은 논거로 D3 채택). 우리 PBE 선택 서술 시 "PBE 격자 과대→탄성 과소 경향" 인용처 |
| **Table II** | LLZO/LLTO/LTP 다결정 B/G/E/ν vs 실험 — DFT 계통 과대 | **"DFT 단결정=상한, 실험 다결정=porosity/GB로 하향"** 문헌 원점 — 우리 DFT 22.06 vs pellet ~23 vs AFM 15 논의의 외부 근거 |
| **Table III** | ★ 메인 데이터 — 23종 full Cᵢⱼ + B/G/E/ν/G/B (PBEsol) | **argyrodite 3종 Cᵢⱼ의 1차 출처** (Torii Table 1 ref10 값의 원본). 우리 comparison의 소환값은 전부 여기서 |
| **Figure 1** (유일한 그림) | **G vs B 산점도** (23종, 물질군별 색·기호: NASICON 파랑 원·phosphate 초록 역삼각·perovskite 빨강 삼각·garnet 청록·antiperovskite 분홍·thiophosphate 황토 사각) + **iso-E 등고선(dashed, 50–300 GPa)** + **G/B=0.5·0.6 점선 2개** | **한 장으로 "물질군=탄성 군집" 시각화** — thiophosphate가 좌하단(B 21–33, G 8–13, G/B<0.5 연성 영역), antiperovskite는 G/B>0.6 취성 쪽, 산화물은 우상단. 우리 cascade elastic 지도(mechanical_soft 테마)의 원조 포맷 — **G-B 평면 + iso-E + Pugh 선** 조합은 우리 그림에도 이식 가치 (house_style로 재구현 시) |

## 6. Post-processing ★
- **무엇**: 유한변형 strain-stress → full Cᵢⱼ → **VRH 평균**(B,G) → E·ν → **Pugh G/B**(연성/취성) → **Born positive-definite 판정**. 이방성 지표(Zener A 등)는 **산출 안 함**.
- **도구**: **VASP**(strain-stress) + **pymatgen**(전 분석) — ELATE/VESTA/LOBSTER류 없음.
- **수치화·플롯·기록**: 전체 텐서를 표로 완전 공개(재사용성 높음 — 우리가 A를 유도할 수 있었던 이유). 그림은 G-vs-B 1장에 압축. PBE/optB88 전체값은 SI.

## 7. 우리 DFT 대비 (comp1/comp2/modelc) → `../our_dft_baseline.md`, `db/properties/elastic.json`
> **방법 정렬 체크**: Deng = VASP/**PBEsol**(no D3)/PAW/520 eV/k-density 1000·atom⁻¹/**strain-stress ±0.015 Å**(relaxed-ion 정황)/**ordered Li@24g** 단일 배열. 우리 = QE/**PBE**(no D3)/USPP/52·520 Ry/k444/**strain-stress ±0.005**(relaxed-ion·clamped 둘 다)/**annealed-Li ordered** 단일 배열(comp1_v3). → **D3 없음·stress-strain·ordered 단일 배열·relaxed-ion까지 4개 축이 정렬**되고 functional(PBEsol vs PBE)·Li 배치(24g vs annealed-48h계)·k만 다름. Torii(PBE-D3)보다 우리와 방법 거리가 가깝다.

### 7.1 ★★★ "Deng=SQS" 귀속 판정 — repo 내 4곳 전부 원문과 불일치
| repo 위치 | 현재 서술 | 원문 판정 |
|---|---|---|
| `papers/torii2025_…md` §3.1 표头·§4·§10 | "선행 ref10 (Deng 2016, **SQS**)", "Deng SQS A=0.92" | **✗ SQS 아님** (ordered Li@24g). 수치(C₁₁/C₁₂/C₄₄/B/G/E/ν/B/G=3.54)는 **전부 원문 Table III와 일치 ✓**. A=0.92는 유도값(원문 미보고, 올바른 반올림 0.93) |
| `kb/concepts/ordered_vs_disordered.md` §6 표·§6 경고박스·"우리 캠페인 적용" | "Deng 2016 = **SQS** (소수파), A=0.92"; "SQS vs ordered가 A−1 부호를 뒤집는 경계 사례" | **✗ 수정 필요** — Deng도 ordered이므로 "계산 진영 전원 ordered"가 됨; A 부호 반전의 원인 후보는 SQS/ordered가 아니라 **functional(PBEsol vs PBE-D3)·Li 배치(24g vs 그 외)·수치 절사** |
| `db/properties/elastic.json` `deng2016_reference` | "comp1_**SQS**", "DFT SQS method" | **✗ 라벨 수정 필요** (값 자체는 ✓) |
| `litdb/comparison_vs_ours.md` 구 [Kaur] 행 / INDEX 계산값 #11 | "elastic **SQS** E22.1/B28.7/G8.1" (Kaur 명의) | **✗ SQS 삭제 + [Deng16]으로 이관** (Kaur는 별개 JES 2022 PDF#8, 미확인) |

> **오귀속의 발원지**: Torii 논문 Table 1가 ref10을 어떻게 라벨했는지가 관건인데 **Torii PDF는 현재 미보유**(digest만 있음) — Torii 자체의 오인용인지 우리 digest의 독해 오류인지는 Torii 재확인 필요. **어느 쪽이든 Deng 원문 기준 SQS는 사실이 아니다.**

### 7.2 ★★ Li₆PS₅Cl 수치 3자 대조 — Deng이 우리 relaxed-ion의 최근접 외부 앵커
| 양 [GPa] | **Deng 2016** (PBEsol, 24g-ordered) | **우리 relaxed-ion** comp1_v3 (PBE) | Δ(Deng/우리) | **Torii 2025** (PBE-D3) | 우리 clamped comp1_v3 |
|---|---|---|---|---|---|
| C₁₁ | 39.9 | 37.67 | +5.9 % | 47.4 | 74.23 |
| C₁₂ | 23.1 | 20.43 | +13.1 % | 28.4 | 29.23 |
| C₄₄ | 7.8 | 7.98 | −2.3 % | 10.4 | 18.98 |
| B | 28.7 | 25.51 (EOS B0 26.23) | +12.5 % | 34.7 | 43.59 |
| G | 8.1 | 8.13 | **−0.4 %** | 10.0 | 20.12 |
| E | 22.1 | 22.06 | **+0.2 %** | 27.4 | 52.31 |
| ν | 0.37 | 0.356 | +0.014 | 0.37 | 0.300 |
| Pugh B/G | 3.54 | 3.14 | — | 3.46 | 2.17 |

- **🔑 E·G·C₄₄가 사실상 동일(0.2–2 %)** — D3 없는 GGA(PBE↔PBEsol) + ordered + relaxed-ion 조합은 Li 배치(24g vs annealed)가 달라도 같은 값에 수렴. **"relaxed-ion ~22 GPa가 물리값"이라는 우리 진단의 두 번째 독립 확증** (첫째는 Torii가 clamped 52를 배제한 것; Deng은 아예 우리 값 그 자체).
- B·C₁₂만 +12–13 % — PBEsol의 격자 압축(더 작은 a₀→정수압 강성↑) 방향과 정합. functional 사다리: **PBE(우리 25.51) < PBEsol(Deng 28.7) < PBE-D3(Torii 34.7)** — B가 격자 결합 세기에 단조.
- ⚠ E·G의 0.2 % 일치는 부분적으로 우연(오차 상쇄) — C₁₁·C₁₂는 5–13 % 다른데 G를 지배하는 C₄₄·(C₁₁−C₁₂)가 거의 같아서 생긴 결과. "±수 %대 정합"으로 인용하는 게 정직.

### 7.3 Zener A 3자 정리 — 전원 ordered, 전원 A≈1
| 출처 | 방법 | A | 성격 |
|---|---|---|---|
| Deng 2016 | PBEsol·**ordered 24g** | **0.93** (유도, 절사 시 0.92) | 논문 미보고 — 인쇄 Cᵢⱼ에서 유도 |
| Torii 2025 | PBE-D3·ordered | 1.09 | 논문 보고값 |
| 우리 comp1 relaxed | PBE·ordered(annealed) | 1.144 (1st triplet) / **avg-Cᵢⱼ 0.926** | triplet 산포 1.144/0.751/0.918 |
| 우리 comp1 clamped | 〃 | 1.073 | |
| 우리 modelc relaxed | PBE·**vacancy+disorder** | **1.441** | 유일하게 1에서 벗어남 |

- **세 ordered 계산이 전부 A≈1(0.93–1.14)** — "vacancy-free LPSCl = 거의 등방" 결론은 3자 견고. A−1의 *부호*는 방법 노이즈 수준: 우리 triplet 산포(1.144↔0.751)가 문헌 간 격차(0.93↔1.09)보다 크다(elastic.json `_Zener_A_convention` 규율 그대로). **우리 avg-Cᵢⱼ A=0.926 ≈ Deng 0.929는 흥미롭지만 consistency 논거로 쓰지 말 것**(같은 규율).
- **"disorder가 A를 1에서 밀어낸다"(modelc 1.44)는 여전히 우리 고유 기여** — 오히려 강화됨: 문헌에 SQS/무질서 탄성 계산이 *하나도 없다*는 게 이번에 확정됐으므로, 무질서-탄성 지문은 문헌 공백.

### 7.4 ★ 할라이드 시리즈 경향 — Deng은 실험·우리와 *반대* (비판 축)
| 축 | Cl→Br(→I) 방향 | 출처 |
|---|---|---|
| **Deng 2016 DFT** | **단단해짐**: E 22.1→25.3→30.0 (+36 %), C₄₄ +53 % | Table III |
| Kraft 2017 실험 | **물러짐**: 음속 −24 %·Debye −22 % (Cl→Br₀.₅I₀.₅), 밀도보정 C₄₄ ~−15~30 % | [Kraft] digest |
| Kim 2025 실험 (UPE) | **물러짐**: Br↑→E↓ (12.59 GPa까지), I-rich 최저 10.68 | elastic.json literature_kim |
| **우리 DFT** comp2 | **물러짐**: E 22.06→20.03 (−9.2 %), B −18 % (Cl→Cl₀.₅Br₀.₅; Li–Br ICOHP −1.93 < Li–Cl −2.11과 정합) | elastic.json comp2_v3 |
- **판정: Deng의 halide-경향은 고립된 반대 방향** — 실험 2건(다른 그룹·다른 기법)과 우리 DFT(동일 프로토콜 comp1↔comp2 쌍)가 모두 "큰 할라이드=연화"인데 Deng만 "경화". 원인 후보(우리 추정, 검증 불가): (i) **Li@24g 고정 배치** — 실제 Li 재배치(Kraft: Cl→I에서 48h→24g 점유 이동)를 못 따라감; (ii) **음이온 무질서 0 가정** — 실험 Cl(62 % disorder)→I(0 %)의 무질서 소멸 효과가 모델엔 처음부터 없음; (iii) PBEsol 고정 프로토콜 자체는 무죄일 가능성(우리 PBE도 같은 ordered인데 연화 방향은 재현) → **(i)·(ii) Li-배치/무질서 처리 쪽이 유력**. **⚠ 인용 규칙: Deng의 Cl/Br/I *간* 경향은 인용 금지(방법 의존), Li₆PS₅Cl 단일점 절대값만 소환.**

### 7.5 Pugh·연성 — cascade mechanical_soft/ductility 테마의 문헌 좌표
- Deng: **Li₆PS₅Cl G/B=0.28 = 23종 중 최저 = 최연성**; thiophosphate 전체 <0.5; 산화물 0.5–0.6; antiperovskite ~0.7 취성. Pugh 임계(G/B 0.57 ↔ B/G 1.75) 기준 황화물 전원 연성.
- 우리: comp1 relaxed B/G=3.14(G/B 0.319)·comp2 2.79·modelc 2.21 — **전원 ductile, [Rupp]·[Kang]·Torii(3.46)와 한 줄**. Deng이 "argyrodite=전 SICE 중 가장 연성 좌표"를 주므로, cascade의 mechanical_soft/ductility 서사("무른 SE가 응력 수용")에 **정량 원점**으로 인용 가능.
- 제조 함의(냉간가압 vs 고온소결, §3.6)는 [Rupp]/[Kang] 리뷰보다 6–9년 앞선 1차 계산 근거.

### 7.6 비교 요약표
| 항목 | Deng 2016 | 우리 | 일치/차이 + 이유 |
|---|---|---|---|
| 물질 | Li₆PS₅Cl ordered (Li@24g) | comp1 ordered (annealed-Li) | 같은 조성·같은 ordered 부류, Li 배치만 다름 |
| functional | PBEsol (no D3) | PBE (no D3) | 근접 (D3 낀 Torii보다 가까움) |
| Cᵢⱼ 산출 | strain-stress ±0.015 Å (relaxed-ion 정황) | strain-stress ±0.005 (relaxed-ion 명시) | **동일 철학** |
| E / G / C₄₄ | 22.1 / 8.1 / 7.8 | 22.06 / 8.13 / 7.98 | **✅ 0.2–2 % 일치** — relaxed-ion 물리값 재확증 |
| B / C₁₂ | 28.7 / 23.1 | 25.51 / 20.43 (EOS B0 26.23) | △ +12–13 % = PBEsol 격자 압축 방향 |
| Zener A | (유도 0.93) | 1.144 (triplet) / 0.926 (avg) | 전원 A≈1; 부호는 노이즈 수준 — consistency 논거 금지 |
| 무질서 | **전 조성 ordered, SQS 없음** | ordered(comp1) + disorder(modelc)·ensemble | **✗ "Deng=SQS" 귀속 폐기**; 무질서 탄성은 우리 고유 |
| halide 경향 | Cl→I 경화 (+36 % E) | Cl→Br₀.₅ 연화 (−9 %) — Kraft/Kim 실험과 우리가 일치 | **✗ Deng 반대 방향** — 경향 인용 금지 |
| Pugh/연성 | G/B 0.28 (최연성) | B/G 3.14 (연성) | **✅ 연성 결론 동일** |
| landscape | sulfide ≪ oxide, Na < Li | [Rupp]/[Kang] 정합 | **✅** |

## 8. 적용 인사이트 (내 연구에 어떻게) — 가장 날카로운 3가지
1. **🔑 귀속 교정이 우리 서사를 *강화*한다**: "Deng=SQS"가 사라지면 litdb의 LPSCl 탄성 계산은 **전원 ordered 단일 배열**(Deng 24g·Torii·우리 comp1)이 되고, A≈1 미세지표의 문헌 간 산포(0.93 vs 1.09)는 무질서 처리가 아니라 **functional·Li-배치·절사**의 문제로 재서술된다. 동시에 **"무질서/공공이 탄성 이방성을 깬다(modelc A=1.44)"는 문헌에 전례가 없는 우리 고유 기여**임이 확정된다 — 개념 문서 §6 "경계 사례" 문단은 이 방향으로 수정 필요.
2. **🔑 functional 사다리 완성 (deck/원고용)**: relaxed-ion Li₆PS₅Cl에서 **PBE(우리) 22.06 ≈ PBEsol(Deng) 22.1 ≪ PBE-D3(Torii) 27.4 GPa** — E/G는 GGA 계열 내에서 수렴하고 D3만 +24 % 계통 이동. "우리 relaxed-ion 값이 외부 두 계산 중 D3 없는 쪽과 0.2 %로 겹친다"는 문장은 vacancy-paradox 슬라이드의 Torii 인용을 보완하는 **2호 외부 앵커**.
3. **🔑 Deng의 halide 경향은 반면교사**: ordered-단일배열 프로토콜이 절대값(단일 조성)은 잘 줘도 **치환 *경향*은 실험과 반대로 줄 수 있다**(Cl→I 경화 vs 실측 연화). 우리 cascade가 dopant *간* 경향을 주장할 때 같은 함정에 노출 — comp2가 실험 방향(Br 연화)을 재현한 것은 좋은 신호지만, **경향 주장엔 배치·무질서 민감도 체크를 항상 붙일 것**.

## 9. 인용 가능 문장 (deck/paper용)
- "The original comprehensive DFT survey of solid-electrolyte elasticity (Deng et al., PBEsol, ordered Li@24g model) reports E=22.1, G=8.1, C₄₄=7.8 GPa for Li₆PS₅Cl — within 0.2–2 % of our relaxed-ion PBE values (22.06/8.13/7.98), independently anchoring the ~22 GPa relaxed-ion regime; the D3-corrected study (Torii) sits systematically ~24 % higher."
- "Contrary to its frequent citation as an SQS study, Deng et al. used fully ordered models throughout (Li on 24g for argyrodites, 'end members or undoped structures' by design); no disorder-averaged elastic calculation of Li₆PS₅Cl exists in the literature we have surveyed — our vacancy/disorder anisotropy fingerprint (Zener A 1.14→1.44) fills that gap."
- "Deng et al. place Li₆PS₅Cl at the most ductile corner of all 23 surveyed solid electrolytes (lowest Pugh G/B=0.28), quantifying the cold-press processability that distinguishes thiophosphates (E<50, B<40, G<20 GPa) from oxides."
- "Deng's halide trend (stiffening from Cl to I, +36 % in E) is opposite to ultrasonic experiment (Kraft: −24 % sound velocity) and to our same-protocol DFT (Br softening, −9 % E) — a caution that ordered single-configuration models can invert substitution trends even when absolute values are reliable."

## 10. 주의/한계 (over-claim 방지)
- **[외부]·UCSD Ong 그룹** — 우리 그룹 아님. 수치 비교는 기계 축(C)에서만.
- **SQS 아님 (재강조)** — repo 4곳의 "Deng=SQS" 라벨은 원문 불일치(§7.1). Torii 논문이 오인용의 발원인지 여부는 Torii PDF 재확인 전까지 미정.
- **Zener A·이방성 = 논문 미보고** — 0.92/0.93은 유도값. 인용 시 "derived from their printed Cᵢⱼ" 명기.
- **relaxed-ion 라벨 = 우리 정황 판정** (§4.3) — 논문 명시 아님. 인용 시 "consistent with relaxed-ion" 수준으로.
- **Li@24g 전점유 = 인위적 배치** — 실험 다수 자리는 48h. Li 배치에 따라 B₀가 크게 흔들린다는 후속 보고 있음(INDEX 계산값 #13, Chem. Mater. 2024/25, 24g vs 48h B₀ 13.7↔29.6 — 미digest, 소환만). Deng의 E/G가 우리 annealed 배치와 일치한 것은 결과론이며 배치 둔감성의 증명은 아님.
- **halide *경향* 인용 금지** (§7.4) — 실험·우리 DFT와 반대. 단일 조성 절대값만 소환.
- **0 K·단결정·무결점** — porosity/GB/2차상 없음; 저자 자신이 Table II에서 DFT>실험 계통 편차와 그 원인을 명시. 절대값을 pellet 실험과 직접 등치 금지 (우리 "DFT > UPE > AFM" 위계로만).
- **c-Na₃PS₄ C₄₄는 δ=0.05 % 특수 처리값** — 준안정상 collapse 우회. 이 값 인용 시 각주 필수.
- **Na₂S 벤치의 실험 기준 자체가 의심** (1977, 수분 민감) — "53 % 오차"를 DFT 결함으로 읽지 말 것.
- **PBE/optB88-vdW의 argyrodite 값 = SI에만 → 미보유 n/a** — "Deng PBE로는 A가 얼마"류 질문에 현재 답 불가.
- 2015년 계산 표준 (520 eV·k1000/atom) — 현대 기준 무난하나 pseudopotential 세트 미명시, 재현 시 MP 2015 워크플로 준용이 안전.

## 11. 기법 용어 미니사전
- **SICE**: (ceramic alkali) SuperIonic Conductor Electrolyte — 이 논문의 조어. 세라믹 알칼리(Li/Na) 초이온 전도체 고체전해질.
- **Voigt–Reuss–Hill (VRH)**: 다결정 평균. Voigt=균일변형(상한, eq 1–2), Reuss=균일응력(하한, eq 3–5; compliance sᵢⱼ=C⁻¹), Hill=산술평균(eq 6–7). E=9BG/(3B+G), ν=(3B−2G)/(2(3B+G)).
- **Pugh ratio**: 이 논문은 **G/B**로 표기(낮을수록 연성; 임계 ~0.57) — Torii·우리의 **B/G**(높을수록 연성; 임계 1.75)와 역수 관계. 표 읽을 때 방향 주의.
- **Born 안정성 판정**: 탄성텐서 고유값 전부 양수(positive definite)면 zero-pressure 기계 안정 (Mouhat–Coudert 2014).
- **strain-stress (Le Page–Saxe) 탄성텐서**: 유한 변형을 가한 셀에서 응력 텐서를 읽어 Cᵢⱼ를 최소제곱 피팅 — 변형 셀 내 이온 재이완 포함 시 relaxed-ion(total) 탄성. VASP IBRION=6 계열·MP workflow의 표준.
- **k-density 1000 per reciprocal atom**: pymatgen automatic density 관례 — 셀 원자수×격자에 맞춰 Γ-센터 그리드를 자동 생성 (원자 많을수록 성긴 mesh).
- **PBEsol**: 고체 격자상수 재현을 위해 재조정된 PBE 변형 — 격자를 PBE보다 조이므로 탄성이 다소 단단하게 나옴. **D3(경험적 dispersion)와는 별개 물건.**
- **optB88-vdW**: vdW-DF 계열 비국소 상관 functional — non-close-packed 구조의 분산력 고려용. 이 논문에선 대체로 가장 단단한 값(과경화 경향).
- **Zener A = 2C₄₄/(C₁₁−C₁₂)**: cubic 이방성 지표 (A=1 등방). **이 논문은 계산 안 함** — 우리/Torii가 유도.
- **Monroe–Newman 기준**: 전착 계면 안정화에 필요한 차단층 전단탄성률 ≈ 2×G_Li. 단순 선형탄성 모델 — 균열·결정립계는 반영 안 됨(저자도 Nagao 균열 관찰로 한계 명시).
- **iso-E 등고선**: G–B 평면에서 E=9BG/(3B+G)가 일정한 곡선 — Fig 1의 점선 가족. 물질군 군집을 E 수준으로 즉독하게 해줌.
