# Machine Learning-Assisted Crystal Structure Prediction of Solid-State Electrolytes Reveals Superior Ionic Conductivity in Metastable Edge-Sharing Phases — Ji Hoon Kim (JACS 2025)

> slug `kim2025_csp_metastable_edge_sharing_sse` · DOI `10.1021/jacs.5c15665` · type `CSP(USPEX+MTP active learning) + DFT + AIMD` ·
> *J. Am. Chem. Soc.* **2025, 147, 47381–47391** · 투고 2025-09-07 / 수정 2025-12-05 / 수리 2025-12-08 / 게재 2025-12-12 ·
> 본문 11 pp + SI 24 pp · digested 2026-07-28 · status ✅ (본문 + SI 전수 정독, Fig 2/3/4/5·S1–S12·Table S1–S2 전부 판독)
>
> elements: Li, Si, Ge, Sn, S, P, Cl, Br, O, Na, Y, Al
> methods: DFT, AIMD, MD, MLIP, phonon
>
> **저자** Ji Hoon Kim¹, Ji Seon Kim¹, Yong Hui Kim¹, **Byeongsun Jun²**, **Yong Jun Jang²**, **Sang Uck Lee**¹*
> — ¹성균관대 화학공학 · **²현대자동차 (화성)**
> 과제: MOTIE **P0022336** + **RS-2024-00437260** + Hyundai Motor Company
> 원자료: `10.6084/m9.figshare.29468165.v4`
>
> 🔑 **심포지엄 덱(`litdb/talks/lee2026_skku_mlip_materials_design.md`) 슬 26–29의 정본.**
> 제1저자 Ji Hoon Kim = `kim2026_hts_li3sc2po43_coating_midni_ncm` 와 동일인, 공저 Ji Seon Kim·Yong Jun Jang =
> `lee2024_multicomponent_argyrodite_mixed_oxidation_mtp` 와 겹침. **이상욱 랩 3부작의 세 번째.**
>
> ⚠ **우리 문제설정과 다른 축이다.** `kb/projects/symposium_2026_competitive_analysis.md` §"하지 않기로 하는 것"에서
> **CSP는 명시적으로 하지 않기로 한 것**이다(우리는 host 고정 개질). 이 digest의 목적은 "따라하기"가 아니라
> **(a) 덱 수치 정정 (b) 이식 가능/불가능 항목의 확정** 이다. §9–§11에 그 판정을 몰아뒀다.

---

## 1. 한 줄 요약

**조성이 구조를 결정하지 않는다**는 명제를 SSE에 밀어붙여, MTP(moment tensor potential) + USPEX 유전알고리즘 +
active learning 으로 **황화물 4조성(Li₂SiS₃, Li₂GeS₃, Li₄SiGeS₆, Li₄SiSnS₆)의 저에너지 폴리모프 각 10개씩 총 40개**를
예측하고, 이들을 **[MS₄] 다면체 연결방식**(corner / edge / mixed)으로 분류한 뒤 AIMD 60 ps @600 K로 확산을 재서
— **열역학적으로 가장 안정한 corner-sharing 상은 Li가 갇혀 거의 안 움직이고, 준안정 edge-sharing 상이 Li 확산을
2자릿수 이상 앞선다** — 는 결과를 얻고, 그 원인을 **packing ratio(α, dead volume 포함) · Li–S₄ 부격자 부피 ·
CSM(연속대칭척도, 왜곡도)** 세 기술자로 정량화한다.

---

## 2. 메타

| 항목 | 값 |
|---|---|
| 저자 | Ji Hoon Kim, Ji Seon Kim, Yong Hui Kim (SKKU) / Byeongsun Jun, Yong Jun Jang (**현대차**) / **Sang Uck Lee*** (SKKU) |
| 저널·년 | J. Am. Chem. Soc. 2025, 147, 47381–47391 |
| DOI | 10.1021/jacs.5c15665 |
| 조성 | **CSP 표적 4종**: Li₂SiS₃ · Li₂GeS₃ · Li₄SiGeS₆ · Li₄SiSnS₆ <br> **검증 14종**: Li₃PS₄, Na₃YBr₆, LiAlCl₄, Na₃PS₄, Na₃YCl₆, LiMn₂O₄, LiBaGe₂, Li₃AuO₃, Li₂BPt₃, LiBiO₃, Li₃YCl₆, Li₃PO₄, Li₁₀GeP₂S₁₂, LiGa(SeO₃)₂ |
| 연구유형 | 순수 계산 (실험 0). CSP + DFT + AIMD + phonon. 실험은 문헌 대조만 |
| 실험 대조 앵커 | ref 36 = **Huang et al., JACS 2022, 144, 4989** (Kanno 그룹, "Anomalously high ionic conductivity of Li₂SiS₃-type conductors") |

---

## 3. 핵심 수치 (소환값 — 우리 db와 섞지 말 것)

| 물성 | 값 | 조건 | 비고 |
|---|---|---|---|
| **이온전도도 σ** | **논문에 값이 없다** | — | ⛔ SI eq 8(Nernst–Einstein)은 방법 서술만 있고 **결과로 σ를 보고한 표·그림이 전무**. §9-A 참조 |
| **Li 확산계수 D_600K** | 최대 **~2.5×10⁻⁵ cm²/s** (edge), corner은 **축상 0에 붙음**(판독 불가) | AIMD **60 ps, 600 K, 단일 궤적** | Fig 3b–e. **오차막대 없음** |
| corner→edge 확산비 | *"at least **2 orders of magnitude** higher"* | Li₂SiS₃, 계산값 | 논문 본문 원문 |
| 실험 대조 (인용) | *"over **3 orders of magnitude** in ionic conductivity"* | Li₂SiS₃ corner vs edge, **ref 36 소환** | **이 논문의 자체 측정이 아님** |
| **활성화E Ea** | **보고 없음** | — | 단일 온도(600 K)만 돌려 Arrhenius를 안 함 |
| **E_rel** (최안정 예측상 대비) | **0 ~ ~0.042 eV/atom** (Fig 3 축 상한 0.05) | 0 K DFT (PBE) | ⚠ 본문 서술 수치(<0.2 / ≥0.3 / ≤0.1 / ≤0.3 eV/atom)와 **10× 불일치** — §9-B |
| **E_hull** | **0 ~ 42 meV/atom** (40 구조 전부) | Table S2 | 표준 합성가능성 컷(50 meV/atom) **전원 통과** |
| corner↔edge 자유에너지 교차온도 | Li₂SiS₃ **360 K** · Li₂GeS₃ **480 K** · Li₄SiGeS₆ **280 K** · Li₄SiSnS₆ **교차 없음(~1000 K까지)** | phonopy 조화근사 G(T) | Fig S8. ⚠ SI 본문은 "Li₂SiS₃·Li₂GeS₃ 모두 ~480 K"라 적어 Fig S8a(360 K)와 어긋남 |
| **packing ratio α** | Li₂SiS₃: corner **0.084–0.100** vs edge **0.0765–0.0805** <br> Li₄SiGeS₆: corner **0.090–0.100** vs edge **~0.083** | AIMD 600 K 60 ps 평균 | Fig 5. **네 조성 모두 edge가 낮음** |
| **dead volume** | Li₂SiS₃ corner **5.67** → edge **4.98** Å³ <br> Li₄SiGeS₆ corner **6.05** → edge **5.36** Å³ | Fig 4f / S10 | 둘 다 **Δ≈0.69 Å³ (−11~12 %)** |
| **MS₄ 다면체 부피** | Li₂SiS₃ SiS₄ corner **5.12** → edge **4.98** Å³ <br> Li₄SiGeS₆ GeS₄ corner **5.96** → edge **5.66**, SiS₄ **5.12→5.07** | Fig 4f / S10 | edge가 더 **압축**됨 |
| **Li–S₄ 부격자 부피** | Li₂SiS₃ ~6.4–8.2 Å³ (edge, 넓게 분산) vs ~7.4–7.6 Å³ (corner, 좁게 집중) | AIMD 600 K | Fig 5a |
| **CSM** | 0(이상 대칭)~6 컬러바. corner은 **2–3에 밀집**, edge는 **2–6에 분산** | AIMD 600 K | Fig 5a. ⚠ Li₄SiGeS₆에선 분리 불명확 — §11-6 |
| 산화 onset / ESW | **없음** | — | 이 논문은 전기화학 안정성 축을 아예 다루지 않는다 |
| 기계 물성 | **없음** | — | 동일 |
| 전자구조 (gap) | **없음** | — | 동일 |

> ⛔ **σ·D 절대값 인용 금지 (우리 규율)**: 이 논문은 애초에 σ를 보고하지 않고, D는 **단일 60 ps 궤적·단일 온도·
> 오차막대 없음**이다. 인용할 것은 **비율("2자릿수", "3자릿수")과 구조–물성 관계**뿐이다.

---

## 4. CSP 워크플로 전부 ★ (Fig 1 + §2.2–2.4 + SI)

우리가 CSP를 안 하기로 했더라도, **"MLIP + GA + active learning" 루프의 실물 설계값**은 T1(UMA 외삽 등급)과
직접 비교 대상이다. 그래서 전 단계를 그대로 적는다.

### 4a. 3단 구조

```
[1] 초기 학습셋 생성  →  [2] 반복 CSP 루프 (MTP↔USPEX↔active learning↔DFT query)  →  [3] fine-tuned MTP로 최종 CSP
```

### 4b. [1] 초기 학습셋 — 두 갈래를 합친다

**(i) Amorphous — melt-quench-anneal AIMD** (선행 CSP 연구 refs 71–73 = Han Seungwu 그룹 계보 승계)

| 단계 | 조건 |
|---|---|
| 가열·평형 | **4500 K, 5 ps** ("녹는점보다 훨씬 위") |
| 융해 | **2500 K, 10 ps** ("경험적 녹는점으로 가정") |
| 급랭 | 300 K까지 **200 K/ps** |
| 어닐 | **500 K, 4 ps** |

**(ii) Random — USPEX 초기 집단 400개**
`random symmetric` + `topological` 생성기로 만든 **400 구조를 single-point DFT** 로 계산해 학습셋에 투입.

> 논문의 논리: melt-quench만 쓰면 "임의 좌표 공간의 PES는 넓게 덮지만, **정확한 구조 완화에 필요한 영역이
> 학습이 안 된 채 남는다**"(원문: *"may still leave untrained regions that are insufficient for accurate structural
> relaxation using MTP"*). 그래서 random 초기구조를 섞는다.
> 🔑 **이 진단은 우리 T1과 같은 문제의식**이다 — 사전학습 모델이 "우리가 실제로 지나가는 영역"을
> 덮었는지를 묻는 것.

### 4c. [2] 반복 CSP 루프 — 4단계

`MTP 학습·평가` → `USPEX 구조생성 + MTP 완화` → `active learning(불확실도)` → `DFT query 재학습`

| 파라미터 | 값 |
|---|---|
| **USPEX 세대 수 (루프 진행에 따라 증가)** | **50 → 100 → 200 → 400** |
| 초기 집단 | **400 구조** |
| 자손 생성 연산 | heredity, permutation, **soft mutation**, lattice mutation (+ random·topological 생성기), **antiseed 옵션** |
| **active learning** | 불확실도(uncertainty) 상위 = **query structure만** 선별 → **완전 완화 + single-point DFT** → 에너지·힘·응력을 학습셋에 추가 |
| **DFT query 총 횟수** | ⛔ **미보고** (Fig S3 산점도 점 개수로도 정확 판독 불가) |
| **학습셋 최종 크기** | ⛔ **미보고** |
| 종료 조건 | (a) 실험 보고 구조를 루프 안에서 예측하면 종료 / (b) 실험 구조가 없는 조성은 **400 세대 후 종료** |
| 검증 | 공간군 비교 + **RDF 비교**(Fig S9) |

### 4d. [3] 최종 CSP

fine-tuned MTP를 넣고 **400 세대 초과**로 한 번 더 전면 탐색. 실험 참조가 없는 조성은 **DFT 기반 안정성 계산으로
최종 랭킹**을 매긴다. → 즉 **최종 순위는 MTP가 아니라 DFT가 매긴다**(§11-2에서 이게 왜 중요한지).

### 4e. MTP 하이퍼파라미터 (본문 §2.1 + SI eq 1–4)

| 항목 | 값 |
|---|---|
| 가중 | **w_e : w_f : w_s = 100 : 1 : 0.1** (에너지 heavy) |
| 컷오프 | **R_cut = 5 Å** |
| moment level | **lev_max = 20** (SI eq 3: `levM_{μ,ν} = 2 + 4μ + ν`) |
| 패키지 | MLIP (Novikov/Shapeev) + **LAMMPS** 연계 |
| 선정 이유 | *"graph 기반(NequIP/M3GNet/CHGNet)은 파라미터가 많아 계산비가 크고 **fine-tune이 필수**. descriptor 기반(NNP/GAP/SNAP/MTP)은 정확도는 낮아도 **훨씬 빠르다**"* → MTP 채택 |

> 🔑 **우리와 정반대 전략**: 그들은 "조성마다 전용 MTP를 새로 학습", 우리는 "사전학습 UMA를 조성 횡단으로 사용".
> 논문 스스로 graph-uMLIP의 약점을 *"need to be fine-tuned to describe the system accurately"* 라고 못 박는데,
> **같은 랩의 `kim2026_hts…` 논문은 SevenNet 7net-0을 fine-tune 없이 그대로 쓴다.** 랩 안에서도 전략이 갈린다
> — 우리 UMA 사전학습 사용을 방어하는 데 이 불일치가 쓸 만하다.

---

## 5. 검증 — 14종 기지구조 재현 (Fig 2, Fig S1, Table S1) ★

**목적**: "CSP가 정말 맞나"를 SSE·절연체·전도체·전극에 걸쳐 검증. 대부분 MP/AFLOW/ICSD에서 취득.

### 5a. Fig 2a — ΔE (예측 − 실험 참조), meV/atom

ΔE < 0 = 예측 구조가 더 안정.

| 조성 | **PBE ΔE** | **SCAN ΔE** | 판정 |
|---|---:|---:|---|
| **Li₃PS₄** | **−26** | **+8** | ⚠ SCAN이 부호 뒤집음 |
| **Na₃YBr₆** | **−15.5** | −9 | 유지 |
| **LiAlCl₄** | **−12** | **+1.5** | ⚠ SCAN이 뒤집음 |
| **Na₃PS₄** | **−8** | **+23** | ⚠ SCAN이 크게 뒤집음 |
| **Na₃YCl₆** | **−6** | −1.5 | 유지(거의 0) |
| LiMn₂O₄ | −3.5 | — | ≈0 (일치) |
| LiBaGe₂ | −1.5 | — | ≈0 |
| Li₃PO₄ | −1 | — | ≈0 |
| Li₃AuO₃ | −0.7 | — | ≈0 |
| Li₂BPt₃ | −0.3 | — | ≈0 |
| Li₃YCl₆ | +1.7 | — | ≈0 |
| **LiBiO₃** | **PBE-fail** (+4.5) | — | ❌ 실패 |
| Li₁₀GeP₂S₁₂ | −1.7 | — | ≈0 (**50 atoms/cell 4원계 성공** — 논문이 가장 자랑하는 건) |
| **LiGa(SeO₃)₂** | **PBE-fail** (+42) | — | ❌ 실패 |

**성적**: 14 중 **12 성공**(실험 구조를 재현했거나, 더 안정한 대안을 찾음). 실패 2건.

### 5b. 실패 원인 진단 (SI, Table S1의 MAE로 사후검시)

| 실패 | MAE_a | MAE_f | 논문의 진단 |
|---|---:|---:|---|
| **LiBiO₃** (Pccn, Z=8) | 40.2 | 36.4 | *"MAE_a가 성공 계들과 비슷 → MTP 정확도 탓이 아니다."* → **400 세대로는 부족, 더 필요** |
| **LiGa(SeO₃)₂** (I-42d, Z=8, **80 atoms/cell**) | **60.1** | **114.1** | *"저에너지 영역에서 MTP 정확도 부족"* → **>80 atom 셀·복잡 배위 = 현 프레임워크 한계** |

> 🔑 **논문 스스로 규정한 적용 한계: "unit cell > 80 atoms + 복잡한 배위 환경"**. 우리 modelc(62 at)·
> B₂O₃ 챔피언(128 at) 규모를 생각하면, **이 CSP 프레임워크는 우리 셀 크기에서 이미 신뢰구간 밖**이다.

### 5c. Table S1 전문 (참조구조 출처 · Z · MTP MAE)

| 조성 | ID | 공간군 | Z | MAE_a (meV/at) | MAE_f (meV/at) | 용도 |
|---|---|---|---:|---:|---:|---|
| Li₃PS₄ | mp-2646995 | I-42m | 2 | 26.0 | 11.9 | SSE |
| Na₃YBr₆ | mp-29080 | P2₁/c | 2 | 26.8 | 10.9 | SSE |
| LiAlCl₄ | mp-22983 | P2₁/c | 4 | 33.9 | 17.2 | Insulator |
| Na₃PS₄ | mp-28782 | P-42₁c | 2 | **283.1** | 8.5 | SSE |
| Na₃YCl₆ | mp-31362 | P2₁/c | 2 | 36.8 | 6.0 | SSE |
| LiMn₂O₄ | mp-22584 | Fd-3m | 4 | 33.4 | 31.9 | Electrode |
| LiBaGe₂ | mp-13140 | Pnma | 4 | 23.6 | 20.5 | Conductor |
| Li₃AuO₃ | mp-7471 | P4₂/mnm | 4 | 21.2 | 21.4 | Semiconductor |
| Li₂BPt₃ | **mp-7471** ⚠ | P4332 | 4 | 16.6 | 16.5 | Conductor |
| LiBiO₃ | mp-29077 | Pccn | 8 | 40.2 | 36.4 | Semiconductor |
| Li₃YCl₆ | ICSD-29962 | P-3m1 | 3 | 28.4 | 8.6 | SSE |
| Li₃PO₄ | mp-13725 | Pmn2₁ | 2 | 28.5 | 6.1 | SSE |
| Li₁₀GeP₂S₁₂ | ICSD-30161 | P4₂/nmc | 2 | 30.1 | 24.5 | SSE |
| LiGa(SeO₃)₂ | mp-1198930 | I-42d | 8 | 60.1 | **114.1** | SSE |

⚠ **Table S1 오타**: Li₃AuO₃ 와 Li₂BPt₃ 가 **같은 mp-7471** 로 적혀 있다(둘 중 하나는 틀림).

### 5d. Fig S1 — 예측 공간군 vs 참조 공간군

| 조성 | 참조 SG | **예측 SG** |
|---|---|---|
| Li₃PS₄ | I-42m | **I23** |
| Na₃YBr₆ | P2₁/c | **P-31c** |
| LiAlCl₄ | P2₁/c | **P2₁/m** |
| Na₃PS₄ | P-42₁c | **P2/c** |
| Na₃YCl₆ | P2₁/c | **C2** |
| LiMn₂O₄ | Fd-3m | Fd-3m ✅ |
| LiBaGe₂ | Pnma | Pnma ✅ |
| Li₃AuO₃ | P4₂/mnm | P4₂/mnm ✅ |
| Li₂BPt₃ | P4332 | P4332 ✅ |
| LiBiO₃ | Pccn | **C2/m** ❌ |
| Li₃YCl₆ | P-3m1 | **P1** |
| Li₃PO₄ | Pmn2₁ | Pmn2₁ ✅ |
| Li₁₀GeP₂S₁₂ | P4₂/nmc | P4₂/nmc ✅ |
| LiGa(SeO₃)₂ | I-42d | **P-1** ❌ |

> ⚠ **Li₃YCl₆ 는 P-3m1 → P1** 로 예측됐는데도 Fig 2b의 "Prediction = Reference" 영역에 들어가 있다.
> P1은 대칭이 완전히 깨진 것이라, 이걸 "일치"로 세는 건 관대한 판정이다. 우리가 "12/14"를 인용할 때
> 이 관대함을 함께 적어야 한다.

---

## 6. 4조성 선정 논리 (§3.2, Fig S2)

| 조성 | 왜 선정했나 |
|---|---|
| **Li₂SiS₃** | **주 조성 = 검증 벤치마크**. 실험으로 (a) 안정 corner-sharing 상과 (b) **변형 합성조건에서 얻은 준안정 edge-sharing 상**이 둘 다 보고돼 있고(Kanno 그룹, ref 36), 후자가 σ 3자릿수 높다 → "CSP가 준안정상까지 잡아내는가"를 시험할 수 있는 유일한 계 |
| **Li₂GeS₃** | Si→**Ge** 단순 치환(둘 다 14족). Ge⁴⁺ **67 pm** > Si⁴⁺ **54 pm** → 확산 경로 확장 기대 |
| ~~Li₂SnS₃~~ | **제외**. 이미 SSE로 선행연구가 있음(ref 82 = Brant, Chem. Mater. 2015) |
| **Li₄SiGeS₆** | **4원계 확장**. MP 상도(Li–Si–S–Ge)에서 **SiS₂ ↔ Li₄GeS₄ 를 잇는 선 위, 1:1 화학량비** 지점 (= Li₂SiS₃ + Li₂GeS₃) |
| **Li₄SiSnS₆** | 동일 논리로 Li–Si–S–Sn 상도에서 선정. Sn⁴⁺ **83 pm** |

> 🔑 **"phase-diagram-guided CSP"의 실체 = MP 상도에서 안정 삼각형(Fig S2 초록 영역) 안의 tie-line 위 점을 고른 것.**
> 방법론적으로 대단한 게 아니라 **"조성을 아무렇게나 고르지 않았다"는 정당화 장치**다. 우리 pool_provenance
> 규율의 그들 버전이라고 봐도 된다.

---

## 7. 핵심 결과 — 연결방식이 확산을 지배한다 (§3.2, Fig 3)

### 7a. 분류 체계 (Fig 3a)

예측된 모든 구조를 **[MS₄] 다면체가 서로 어떻게 붙어 있는가**로 3분류:

| 분류 | 마커 | 정의 |
|---|---|---|
| **corner-sharing** | 파란 원 | 인접 MS₄가 **꼭짓점 S 1개** 공유 |
| **edge-sharing** | 주황 사각 | 인접 MS₄가 **모서리(S 2개)** 공유 |
| **mixed corner/edge** | 초록 삼각 | 둘 다 존재 |

⚠ **논문은 이 분류의 알고리즘을 제시하지 않는다.** 그림 스키마와 육안 분류만 있다. (공유 음이온 개수를 세면
자동화는 자명하지만, 컷오프·주기경계 처리 등 실무 정의는 우리가 새로 정해야 한다.)

### 7b. Fig 3b — Li₂SiS₃ (D_600K ×10⁻⁵ cm²/s, 도판 판독값)

| rank | 연결방식 | D_600K | E_rel (판독) | E_hull (Table S2) | 비고 |
|---:|---|---:|---:|---:|---|
| 1 | **corner** | ≈0.00 | 0 | 0 | **"Exp." 라벨 — 실험 안정상 재현 ✅** |
| 2 | corner | ≈0.00 | ~0.003 | 0 | |
| 3 | **edge** | **≈1.75** | ~0.004 | **0** | **"Exp." 라벨 — 실험 준안정 edge상 재현 ✅ (RDF 일치 Fig S9)** |
| 4 | edge | ≈1.15 | ~0.007 | 3 | |
| 5 | **edge** | **≈2.35** ★최고 | ~0.007 | 2 | **신규 예측 준안정상** |
| 6 | corner | ≈0.00 | ~0.008 | 4 | |
| 7 | corner | ≈0.00 | ~0.009 | 4 | |
| 8 | edge | ≈0.30 | ~0.013 | 9 | MSD가 25 ps 부근 계단 후 정체 (Fig S4) |
| 9 | edge | ≈1.75 | ~0.016 | 11 | |
| 10 | corner | ≈0.00 | ~0.017 | 12 | |

**핵심**: corner 5개 전부 D≈0(축상 구분 불가), edge 5개 전부 유한. **연결방식이 이분한다.**

### 7c. Fig 3c — Li₂GeS₃

| rank | 연결 | D_600K | E_rel | E_hull |
|---:|---|---:|---:|---:|
| 1–5 | corner ×5 | ≈0.00 | 0 ~ 0.014 | 0, 0, 10, 12, 11 |
| **6** | **edge** | **≈0.72** | **~0.031** | 12 |
| 7 | corner | ≈0.04 | ~0.036 | 25 |
| 8, 9 | corner | ≈0.00–0.01 | ~0.040 | 31, 34 |
| **10** | **edge** | **≈2.6** (축 밖) | **~0.042** | 34 |

**논문의 결론**: Li₂GeS₃의 edge상은 확산은 좋지만 **에너지 페널티가 Li₂SiS₃보다 뚜렷이 크다** → 실험적으로
Li₂GeS₃는 **보고된 구조가 전부 corner-sharing** 이고, 그래서 SSE로 못 쓴다. **"확산은 좋은데 못 만든다"의 사례.**

### 7d. Fig 3d — Li₄SiGeS₆

| rank | 연결 | D_600K | E_rel |
|---:|---|---:|---:|
| 1–4 | corner ×4 | ≈0.00 | 0 ~ 0.002 |
| **5** | **edge (유일)** | **≈1.0** ★ | **~0.009** |
| 6 | corner | ≈0.11 | ~0.025 |
| **7** | **mixed** | **≈0.02** | ~0.037 |
| 8 | corner | ≈0.64 | ~0.041 |
| 9, 10 | corner | ≈0.22, 0.14 | ~0.042, 0.044 |

**핵심 소견 2개**:
1. **edge상이 E_rel ~0.009 eV/atom(≈9 meV) 로 극히 낮다** → *"favorable experimental accessibility, making it a
   highly promising metastable SSE candidate"*.
2. **이유가 heteroelemental**: 이 edge 위상은 **Si–Ge 이종 연결**로 만들어지고 **Si–Si 동종 연결이 아니다**.
   → *"enhances structural disorder and flexibility, thereby improving overall stability."*
   🔑 **"이종 원소 혼합이 준안정상의 에너지 페널티를 깎는다"** — 이건 우리 co-doping 교호작용 논의와
   같은 계열의 주장이다(다만 그들은 기구 서술, 정량 분해는 없음).

### 7e. Fig 3e — Li₄SiSnS₆

| rank | 연결 | D_600K | E_rel |
|---:|---|---:|---:|
| 1 | corner | ≈0.00 | 0 |
| **2** | **edge** | **≈1.5** ★ | ~0.011 |
| **3** | **mixed** | ≈0.00 | ~0.013 |
| 4 | corner | ≈0.00 | ~0.016 |
| **5** | **edge** | **≈0.65** | ~0.022 |
| 6 | corner | ≈0.25 | ~0.023 |
| 7 | corner | ≈0.00 | ~0.023 |
| **8** | **mixed** | ≈0.03 | ~0.027 |
| 9 | corner | ≈0.00 | ~0.030 |
| 10 | corner | ≈0.19 | ~0.042 |

**핵심**: Sn⁴⁺(83 pm)이 커서 **결합 기하가 유연 → mixed 위상이 가장 자주 나온다**(4조성 중 최다).
그런데 **mixed 위상의 확산은 전부 바닥**이다.
논문의 해석: *"corner-sharing topologies act as bottlenecks, impeding Li-ion migration."*
→ **혼합은 "평균"이 아니라 "최악값 지배"**. 병목 하나가 경로 전체를 죽인다.

> 🔑 **이건 우리 퍼콜레이션 언어와 정확히 같다** (`kb/concepts/ordered_vs_disordered.md` §4의 F* 문턱,
> `ishikawa2025_site_percolation` digest). 수송은 평균이 아니라 **연결성의 최소 컷**이 결정한다.

### 7f. 전 조성 요약

```
안정성 순위:  corner  >  mixed  ≳  edge        (0 K DFT, 4조성 모두 일관)
확산 순위  :  edge    >>  corner ≈ mixed       (AIMD 600 K, 4조성 모두 일관)
```
논문 원문: *"the corner-sharing topologies (blue circles) consistently exhibited the highest stability across
all four compositions, likely due to their increased structural flexibility compared with their edge-sharing
counterparts."*

---

## 8. 기구 — 왜 edge가 빠른가 (§3.3, Fig 4–5)

### 8a. Li 확률밀도 + van Hove 자기상관 (Fig 4a, 4b) — 갇힘 vs 자유

AIMD **60 ps @600 K** 궤적에서:

| | Li 확률밀도 등가면 | van Hove 자기부분 $4\pi r^2 G_s(r,t)$ |
|---|---|---|
| **corner** (Li₂SiS₃, Li₄SiGeS₆) | **국소화** — 사이트에 붙어 있음 | **60 ps 내내 r < 2 Å에 단일 강피크** = 갇힘 |
| **edge** (Li₂SiS₃, Li₄SiGeS₆) | **연속 네트워크** — 3D로 이어진 붉은 관 | **첫 10 ps만 r<2 Å 피크, 이후 장거리로 넓게 분포** = 트랩 탈출 후 자유 이동 |

> 🔑🔑 **van Hove 자기상관은 우리 MSD 파이프라인에 없는 진단**이고, `lee2024` digest §3c에서 이미
> **T12**로 등록한 항목이다. **이 논문은 그 사용법의 두 번째 실증**이고, 특히 **"corner vs edge"처럼
> MSD 기울기로는 둘 다 '거의 0'이라 구분이 안 될 때 갇힘의 성격 자체를 보여준다**는 점이 유용하다.
> → **T12 우선순위를 올릴 근거가 하나 더 생겼다.**

### 8b. dead volume — 논문의 개념적 신규성 (Fig 4c, 4d)

**관찰**: 연결된 다면체 **사이의 틈**(corner이든 edge이든)에서는 **Li 이동이 전혀 관측되지 않는다.**

**해석**: 그 틈은 다면체 중심 양이온(Si⁴⁺/Ge⁴⁺/Sn⁴⁺)의 **정전 반발**로 Li가 접근 못 하는
**pseudopolyhedron void** 다. 논문은 이걸 **dead volume** 이라 명명한다.

> 원문: *"These regions inevitably form pseudopolyhedron voids due to the repulsive forces between the
> cations at the polyhedron centers (Si⁴⁺, Ge⁴⁺, and Sn⁴⁺) and the Li ions, effectively hindering Li-ion
> diffusion. These volumes, referred to as 'dead volume,' appear as empty regions within the crystal
> structure and are inaccessible for Li-ion migration."*

**핵심 주장**: *"previous studies have overlooked these [dead] volumes"* — 즉 "빈 공간 = 확산 경로"라는
통념을 깨는 것이 이 논문의 개념적 기여다. **빈 공간에도 죽은 빈 공간이 있다.**

### 8c. 왜 edge가 dead volume이 작은가 (Fig 4e, 4f)

두 단계 논증:

1. **기하**: edge-sharing은 두 다면체 중심 양이온 사이 거리가 짧다 — **d_c > d_e** (Fig 4e).
   → 다면체 사이 틈(=dead volume)이 **작다**.
2. **정전**: edge에서는 공유 음이온 각각이 **두 이웃 양이온의 정전 인력을 동시에 받는다**
   → 다면체가 **더 압축** 되어 **다면체 부피 자체도 작아진다**.

**정량 (Fig 4f / Fig S10)**:

| | Li₂SiS₃ corner | Li₂SiS₃ edge | Li₄SiGeS₆ corner | Li₄SiGeS₆ edge |
|---|---:|---:|---:|---:|
| MS₄ 다면체 부피 (Å³) | 5.12 (SiS₄) | **4.98** | 5.96 (GeS₄) / 5.12 (SiS₄) | **5.66 / 5.07** |
| **dead volume (Å³)** | **5.67** | **4.98** | **6.05** | **5.36** |
| Δ dead volume | — | **−0.69 (−12 %)** | — | **−0.69 (−11 %)** |

> 논문 결론: *"the superior Li-ion mobility of the edge-sharing phase can be attributed to a reduction in the
> polyhedron volume, while the notable decrease in dead volume contributes to an expanded Li-ion migration
> space within the crystal structure."*
> ⚠ **두 조성 모두 Δ = 0.69 Å³ 로 정확히 같은 것**은 우연일 수도, 산출 방식의 인공물일 수도 있다.
> 판단 불가 — 원자료(figshare) 없이는 확인 못 함.

### 8d. 세 기술자 — 정의식 (SI eq 9–11) ★★ 여기가 우리가 볼 곳

#### (1) Packing ratio α — SI eq 9

$$\alpha=\frac{V_{\text{polyhedron}}+V_{\text{dead}}}{V_{\text{unit cell}}}$$

- **의미**: 단위셀 부피 중 **Li가 못 쓰는 부분의 비율**. **낮을수록 좋다.**
- $V_{\text{polyhedron}}$ = MS₄ (M = Si, Ge, Sn) 다면체 부피 합
- $V_{\text{dead}}$ = Li 접근 불가 dead volume
- ⛔ **$V_{\text{dead}}$ 의 알고리즘 정의가 논문 어디에도 없다.** 문장 정의(*"unoccupied regions that are
  inaccessible to Li-ion migration due to the electrostatic repulsion exerted by the surrounding polyhedra"*)와
  Fig 4d 스키마뿐. 반발 컷오프도, 이온반경 규약도, voxel/해석기하 여부도 없다. → **재현 불가**.

#### (2) Li–S₄ 부격자 부피

- Li 주위 S 4개가 만드는 사면체의 부피. **클수록 Li–S 정전 인력이 약해져 이동 유리.**
- Fig S11a: Li–S₄ 사면체의 인력 개념도. Fig S11b: 왜곡 시 "long distance + large volume".
- **AIMD 궤적에서 평균**해 산출(정적 구조가 아니라 동적 평균).

#### (3) CSM — 연속대칭척도 (SI eq 10, 11)

$$\mathrm{CSM}=\min\frac{\sum_{k=1}^{N}|Q_k-P_k|^2}{\sum_{k=1}^{N}|Q_k-Q_0|^2}\times 100,
\qquad Q_0=\frac{1}{N}\sum_{k=1}^{N}Q_k$$

- $Q_k$ = 실제 다면체 꼭짓점 좌표, $P_k$ = 완벽 대칭 이상 다면체의 대응 좌표, $Q_0$ = 무게중심
- **CSM ↑ = 왜곡 ↑**. 논문 논리: 왜곡 → Li–음이온 상호작용 지형이 **평탄해짐** → 활성화에너지 ↓
- 출처 refs 22–23 (SI) = Lee & Ok 2013 (Inorg. Chem.) + **Jun et al., Nat. Mater. 2022, 21, 924**

#### 세 기술자의 실측 (Fig 5, Fig S12)

| 조성 | corner α | **edge α** | mixed α | 분리 |
|---|---|---|---|---|
| **Li₂SiS₃** (Fig 5a) | 0.084–0.100 | **0.0765–0.0805** | — | ✅ **완전 분리** (corner 최저 0.0835 > edge 최고 0.0805) |
| **Li₄SiGeS₆** (Fig 5b) | 0.090–0.100 | **~0.083** (1개) | **0.100** (최고!) | ✅ 분리 (단 edge 표본 1개) |
| **Li₂GeS₃** (Fig S12a) | 대부분 ≥0.100 (축 상한 클립) | **~0.085 / ~0.082** | — | ✅ 분리 |
| **Li₄SiSnS₆** (Fig S12b) | ~0.099–0.12 | **~0.093** 등 | — | ○ (축 범위 다름, 일부 판독 불가) |

- **α**: 4조성 전부에서 edge가 낮다. **가장 깨끗한 기술자.**
- **Li–S₄ 부피**: Li₂SiS₃에서 edge가 넓고 크게 분산(6.4–8.2 Å³) vs corner은 좁게 집중(7.4–7.6 Å³).
- **CSM**: Li₂SiS₃에서 corner은 어두운색(2–3)에 밀집 = *"pronounced structural rigidity and negligible
  Li-ion displacement"*, edge는 밝은색(최대 6)까지 분산. **단 Li₄SiGeS₆에서는 이 분리가 안 보인다** (§11-6).
- **mixed 위상이 α 최고**(Li₄SiGeS₆ rank 7 = 0.100) → mixed의 저확산과 정합.

---

## 9. ★★ 덱 수치 정정 — 3건

### 9-A. ⛔ **σ 값 (10⁻⁴ → 2.4 mS/cm, "4자릿수 상승")은 이 논문에 없다**

`db/properties/external_benchmarks_symposium_2026.json` → `reproduction_targets.csp_metastable_conductivity`
에 등록된 값:

| 등록값 | 실물 |
|---|---|
| "Li2SiS3 corner-sharing sigma = **0.0001 mS/cm**" | **논문에 없음.** 논문은 σ를 어떤 조성·어떤 상에도 보고하지 않는다 |
| "Li2SiS3 edge-sharing sigma = **2.4 mS/cm**" | **논문에 없음** |
| "corner→edge = **4 orders of magnitude**" | **논문에 없음.** 논문의 두 수치는 아래 |

**논문이 실제로 말하는 것**:
1. **계산값**: *"the Li-ion diffusivity of this edge-sharing structure is **at least 2 orders of magnitude**
   higher than that of the corner-sharing structure"* — **확산계수 D_600K 기준, 2자릿수**
2. **실험 소환**: *"aligning well with experimental observations reporting an enhancement of **over 3 orders
   of magnitude** in ionic conductivity"* — 각주 **36 = Huang et al., JACS 2022, 144, 4989**(Kanno 그룹).
   **이 논문의 측정이 아니라 인용이다.**

**정정 결론**:
- 덱의 "4자릿수"는 논문의 2자릿수(계산)도 3자릿수(인용 실험)도 아니다. 출처 불명.
- 0.0001 / 2.4 mS/cm 라는 구체 수치는 **Huang 2022 원문에 있을 가능성이 높으나 우리는 그 PDF를 보유하지 않았다**
  → **판독 불가. 확인 전까지 인용 금지.**
- ✅ **인용 가능한 형태**: *"CSP로 찾은 준안정 edge-sharing 상이 안정 corner-sharing 상보다 600 K 확산계수가
  2자릿수 이상 높다[Kim 2025]"* / *"동일 조성 Li₂SiS₃에서 연결방식만 다른 두 상의 실험 σ 차이가 3자릿수를
  넘는다[Huang 2022, Kim 2025 재인용]"*

> 🔑 **`kim2026_hts…` digest 때와 같은 사례가 또 나왔다** (덱: 17,233 Li-P-S-O → 실물: 17,230 Li-O).
> **덱은 정본이 아니다** 는 우리 규율의 두 번째 실증. → json 정정 필요.

### 9-B. ⚠ **E_rel 본문 서술값이 Fig 3 축 범위와 10× 어긋난다**

| 본문 서술 | Fig 3 / Table S2 실측 |
|---|---|
| Li₂SiS₃: *"relative potential energy difference … is **<0.2 eV/atom**"* | Fig 3b 최대 **~0.017 eV/atom**, E_hull 최대 **12 meV/atom** |
| Li₂GeS₃: *"edge-sharing … **E_rel ≥ 0.3 eV/atom**"* | Fig 3c edge = **~0.031, ~0.042 eV/atom**, E_hull 12·34 meV |
| Li₄SiGeS₆: *"relatively low E_rel (**≤0.1 eV/atom**)"* | Fig 3d edge = **~0.009 eV/atom**, E_hull 7 meV |
| Li₄SiSnS₆: *"relatively low E_rel (**≤0.3 eV/atom**)"* | Fig 3e edge = **~0.011, ~0.022 eV/atom**, E_hull 0·10 meV |

**Fig 3b–e의 E_rel 축 상한은 4개 패널 모두 0.05 eV/atom** 이고, Table S2의 E_hull은 **전 40구조 0–42 meV/atom**이다.
→ **그림·표는 자기들끼리 정합하고, 본문 산문만 10배 크다.** 본문 오타로 보이지만 논문에 정오표는 없다.

**우리 인용 규칙**: **Fig 3 / Table S2 값을 쓰고, 본문 산문 수치는 쓰지 않는다.**
(공교롭게도 **정정하면 논문 주장이 더 강해진다** — "20 meV/atom 준안정"은 "200 meV/atom 준안정"보다
훨씬 합성 가능하다.)

### 9-C. ⚠ **"3 기술자"의 목록이 덱과 논문에서 다르다**

| 덱 슬 29 (우리 등록본) | 논문 결론부 + SI eq 9–11 |
|---|---|
| ① dead volume | ① **packing ratio α** (eq 9) — dead volume은 α의 **구성요소** |
| ② distance of cation (d_c > d_e) | ② **Li–S₄ sublattice volume** |
| ③ Li–S₄ distortion | ③ **CSM** (eq 10–11) — = Li–S₄ distortion의 정량 이름 |

논문 결론 원문: *"the packing ratio (α), Li–S₄ sublattice volume, and CSM of the Li–S₄ sublattice are
established as predictive indicators of high Li-ion diffusivity."*

→ 덱의 ①·②는 **기술자가 아니라 기구(mechanism)**다. `d_c > d_e`는 "왜 edge의 dead volume이 작은가"를
설명하는 기하 논증이고(Fig 4e), 정의식도 수치표도 없다. **덱 목록을 그대로 인용하면 논문에 없는
기술자 2개를 만들어내는 셈**이 된다. → json 정정 필요.

---

## 10. 우리 문제설정과의 관계 — 정직하게 ★★★

### 10a. 문제설정이 다르다 (다시 못 박기)

| | 이 논문 | 우리 |
|---|---|---|
| 질문 | **"이 조성의 최적 구조는 무엇인가"** (구조 탐색) | **"이 host를 어떻게 개질하는가"** (조성·계면 개질) |
| host | 없음 — 조성만 주고 구조를 찾는다 | **Li₆PS₅Cl 고정** |
| 대상 | Li₂SiS₃ 등 **신조성 4종** | LPSCl + **도펀트/코팅 47종 × 3농도** |
| 자유도 | 격자·공간군·연결방식 전부 | **argyrodite 골격 고정**, 자리 점유·치환만 |
| 출력 | 준안정 폴리모프 랭킹 | σ·Ea·C_ij·gap·ESW·계면반응성 6축 |

**`kb/projects/symposium_2026_competitive_analysis.md` §"하지 않기로 하는 것"**:
> *"CSP(신조성 탐색) — 문제설정이 다르다(우리는 host 고정 개질). 흉내내면 둘 다 얕아진다."*

**이 판정은 유지된다.** 아래 §10b–10d는 "그럼에도 이식 가능한 것"의 목록이다.

### 10b. ❌ 이식 **불가** — corner/edge 연결방식 자체

**argyrodite의 PS₄³⁻ 사면체는 서로 연결되지 않는다.** ortho-thiophosphate 구조라 PS₄는 **고립된 섬**이고,
그 사이를 Li·free-S²⁻(4a)·Cl⁻(4d)가 채운다. **P–S–P 다리가 아예 없다.**

→ **corner-sharing / edge-sharing / mixed 라는 축이 우리 host에는 정의되지 않는다.**
이 논문의 **중심 구조 축이 우리 계에 옮겨지지 않는다**는 것이 가장 정직한 한 줄이다.

> ⚠ 이걸 "우리도 edge-sharing을 만들면 된다" 식으로 읽으면 안 된다. argyrodite에서 PS₄가 연결되기 시작하면
> 그건 이미 argyrodite가 아니라 Li₄P₂S₆·Li₇P₃S₁₁ 계열이다.

### 10c. ⭕ 이식 **가능(변형)** — 세 기술자, 개별 판정

| 기술자 | 우리 47종에 계산 가능한가 | 판정 | 비용 |
|---|---|---|---|
| **① packing ratio α** (eq 9) | ❌ **그대로는 불가** — $V_{\text{dead}}$ 알고리즘 정의가 논문에 없다. 우리가 새로 발명해야 하고, 그러면 그들 값과 비교 불가 | **재구현 금지** | — |
| **① ′ 대체: BVSE 채널 %** | ✅ **이미 갖고 있다** — `tools/comp1_v3/` BVSE 맵의 above-min ≤ iso 채널 비율(~0.25 Å voxel)이 **"Li가 실제로 쓸 수 있는 부피 비율"**을 **정전 퍼텐셜에서** 산출. α보다 **정의가 명확하고 물리적으로 우월** | ✅ **채택 — 우리 것이 낫다** | 0 (기존) |
| **② Li–S₄ 부격자 부피** | ✅ **가능(변형 필요)** — 우리 host에서 Li 1차 배위는 S와 Cl 혼합이라 **Li–(S,Cl)₄** 로 정의해야 한다. 기존 UMA-MD 600 K 궤적을 그대로 후처리(pymatgen CrystalNN/VoronoiNN + ConvexHull) | ✅ **채택 후보** | **소** (궤적 재사용) |
| **③ CSM** (eq 10–11) | ✅ **가능** — pymatgen `chemenv` 에 CSM 기계가 있고, eq 10은 직접 구현도 쉽다. 같은 궤적에 얹으면 됨 | ✅ **채택 후보** | **소** |
| **④ corner/edge 자동분류** | ❌ host에 정의 안 됨 (§10b) — **단 아래 ④′ 변형은 신규성 있음** | 변형만 | — |
| **④ ′ 도펀트–PS₄ 연결방식** | 🆕 **우리 계에서만 되는 변형**: 도펀트 양이온(B in B₂O₃, Sc in Sc₂O₃, W in WO₃…)이 만드는 MOₓ/MSₓ 다면체가 **PS₄와 S를 몇 개 공유하는가**(0=고립 / 1=corner / 2=edge)를 세는 것. 자명하게 자동화 가능하고, **47종을 가르는 새 구조 기술자**가 될 수 있다 | 🆕 **T13 후보** | 소 |

**종합 판정**: **3 기술자 중 2개(Li–S₄ 부피, CSM)는 오늘이라도 계산 가능**하고, 1개(α)는 **우리가 이미 더
나은 것을 갖고 있다**. 계산 자체는 전부 **기존 UMA-MD 궤적 후처리**라 새 시뮬레이션이 필요 없다.

⚠ **단 심각한 caveat 하나**: 그들의 세 기술자는 **"같은 조성 안의 폴리모프 10개를 줄 세우는"** 도구로만
검증됐다. **조성이 다른 47종을 가로질러 비교한 적이 없다.** 우리가 47종에 얹으면 그건 **논문이 검증하지
않은 사용법**이다. (α는 특히 조성 간 비교가 무의미하다 — MS₄ 부피 자체가 화학이 바뀌면 달라진다.)
→ **쓴다면 "조성별 상대 지표"로만.**

### 10d. ⭕ 이식 가능 — 기구·방법론 항목

| 항목 | 이식 형태 |
|---|---|
| **van Hove 자기상관** | **T12 강화**. MSD가 둘 다 ~0일 때 "갇힘의 성격"을 가르는 유일한 진단. 우리 disorder ensemble의 "ordered frozen" 판정에 직결 |
| **dead volume 개념** | **"빈 공간에도 죽은 빈 공간이 있다"** — 우리 BVSE 채널 % 해석의 언어를 강화한다. 지금 우리는 "채널 %"라고만 쓰는데, **"above-min iso 밖의 공동은 dead volume"** 이라고 명명하면 물리가 선명해진다 |
| **heteroelemental 안정화** | Si–Ge 이종 연결이 준안정상의 E_rel을 깎는다 → **co-doping 교호작용의 구조적 기구 후보**. 우리 1081쌍 ML 교호작용 항에 붙일 물리 해석 |
| **mixed = 최악값 지배** | corner이 병목이라 mixed는 corner만큼 느리다 → **우리 퍼콜레이션 프레임과 정확히 동형**. 인용 가능 |
| **>80 atom 셀에서 CSP 붕괴** | 그들 프레임워크의 한계 자백(§5b). 우리가 CSP를 안 하는 판단의 **외부 근거** |

### 10e. `kb/concepts/ordered_vs_disordered.md` 와의 관계 ★

우리 개념 노트의 뼈대는:
> **"0 K DFT는 E를, 합성온도 결정은 F = E − TS_config 를 최소화한다. 양마다 맞는 구조가 다르다."**

이 논문은 **같은 명제의 다른 사례**다. 대응은 이렇다:

| `ordered_vs_disordered.md` | 이 논문 |
|---|---|
| 0 K 최소 = **질서상** / 합성 T 최소 = **부분 무질서상** | 0 K 최소 = **corner-sharing** / 고온 최소 = **edge-sharing** |
| 구동력 = **배치 엔트로피 $S_{\text{config}}$** | 구동력 = **진동 엔트로피 $S_{\text{vib}}$** (phonopy $F_{\text{vib}}$, Fig S8) |
| 교차: 합성 550 °C에서 무질서 $x^*(T)$ | 교차: **Li₂SiS₃ 360 K, Li₂GeS₃ 480 K, Li₄SiGeS₆ 280 K** |
| 실험이 재는 것은 **급랭 동결된 고온 배치** | 실험이 재는 것은 **변형 합성조건으로 얻은 준안정 edge상** (Kanno) |
| 수송은 **무질서상**이 옳다 | 수송은 **edge상**이 옳다 |

> 🔑🔑 **우리 노트에는 없던 축이 여기 있다: $S_{\text{vib}}$.**
> 우리 §1은 *"엄밀히는 $S = S_{\text{config}} + S_{\text{vib}}$이지만 … 여기선 $S_{\text{config}}$만 쓴다
> (진동항은 정량 보정 — 특히 무른 Li 부격자에선 $\Delta S_{\text{vib}}$가 0이 아닐 수 있다)"* 라고
> **유보만 달아뒀다.** 이 논문은 그 유보가 **실제로 상 순서를 뒤집을 만큼 크다**는 것을 보인다
> (Li₄SiGeS₆에서는 **영점에너지만으로도 0 K 상대안정성이 바뀐다** — SI 원문).
> → **`ordered_vs_disordered.md` §9(한계 고백)에 이 사례를 추가할 것.**

**단 차이도 분명하다**: 그들의 준안정은 **폴리모프**(다른 공간군), 우리 무질서는 **같은 골격 안의 자리 점유**다.
"준안정이 더 좋을 수 있다"는 명제는 공유하지만 **작동 자유도가 다르다.**

---

## 11. 주의 / 한계 (over-claim 방지) ★

### 1. **σ를 한 번도 계산하지 않고 제목에 "Superior Ionic Conductivity"를 썼다**
논문이 잰 것은 **D_600K** 뿐이다. σ로 가려면 Nernst–Einstein(SI eq 8)과 Arrhenius 외삽(eq 7)이 필요한데
**둘 다 결과에 등장하지 않는다**. SI의 확산 방법론 절(eq 5–8)은 **쓰이지 않은 보일러플레이트**다.
→ 제목·초록의 "ionic conductivity"는 **D의 대리 서술**이다. 인용할 때 반드시 "확산계수 기준"을 붙일 것.

### 2. **오차막대가 전혀 없다 — 그런데 통계 분산 논문을 인용한다**
- AIMD: **단일 궤적, 60 ps, 단일 온도(600 K)**. 시드 반복 없음.
- 방법 절에서 **ref 46 = He, Zhu, Epstein, Mo, "Statistical variances of diffusional properties from ab initio
  molecular dynamics simulation", npj Comput. Mater. 2018** 을 인용한다. 그 논문의 결론이 정확히
  **"짧은 AIMD의 D는 분산이 크다"** 인데, **그 처방을 적용하지 않았다.**
- `lee2024` digest §6(Table S1)이 보여줬듯 AIMD는 Li₆PS₅I에서 실험 대비 **840배**까지 틀렸다.
→ **rank 3 vs rank 4 처럼 D가 1.75 vs 1.15로 갈리는 차이는 통계적으로 의미 없을 가능성이 높다.**
  살아남는 주장은 **"corner ≈ 0, edge = 유한"** 이라는 **이분법**뿐이다.

### 3. **PBE 단독 — SCAN 검증이 오히려 PBE를 흔든다**
검증 14종에서 SCAN을 돌린 5건 중 **3건(Li₃PS₄, Na₃PS₄, LiAlCl₄)에서 ΔE 부호가 뒤집힌다**(−26→+8, −8→+23,
−12→+1.5). 즉 **"CSP가 실험보다 안정한 구조를 찾았다"는 PBE 결론이 SCAN에서 무효화**된다.
그런데 **SI 본문은 *"the newly identified low-energy structures remained more stable than their reference
counterparts"* 라고 적어 자기 Fig 2a와 모순된다.**
🔴 **그리고 본론 4조성(Li₂SiS₃ 등)에는 SCAN을 아예 안 돌렸다.** corner vs edge의 E_rel 차이가 3–42 meV/atom
인데 functional 하나로 그 크기의 역전이 관측됐으니, **"corner이 더 안정하다"는 순위 자체가 방법 의존일 수 있다.**
→ **우리 규율 언어로: 이건 real difference가 아니라 method-dependent claim이다.**

### 4. **MTP 오차가 판별하려는 에너지 차와 같은 크기**
MAE_f (저에너지 영역): Li₂SiS₃ **13.2** / Li₂GeS₃ **27.4** / Li₄SiGeS₆ **29.8** / Li₄SiSnS₆ **33.3** meV/atom.
Table S2의 E_hull 전 범위가 **0–42 meV/atom**. → **MTP 단독으로는 폴리모프 순위를 못 가린다.**
최종 랭킹이 DFT로 다시 매겨져서 결과는 방어되지만, **어떤 구조가 DFT까지 올라오느냐**는 MTP가 정하므로
**놓친 저에너지 상이 있을 가능성**은 정량화되지 않았다. 또 4조성 중 **3조성에서 MAE_f > MAE_a**
(저에너지 영역을 오히려 더 못 맞춘다) — CSP 용도로는 나쁜 징후다.

### 5. **선행연구(Jun 2022, Nat. Mater.)와 정면 충돌하는데 해소하지 않았다**
본문: *"a recent study using high-throughput screening … revealed that **corner-sharing** oxide structures
achieved moderate ionic conductivities below 1 mS/cm … **This observation contradicts the results obtained
by this study**, and further investigation is essential."*
- ref 88 = **Jun, K. et al., "Lithium superionic conductors with corner-sharing frameworks", Nat. Mater. 2022, 21, 924**
  (Ceder 그룹) — **corner-sharing이 좋다**는 정반대 주장.
- 이 논문은 충돌을 **인정만 하고 넘어간다**. 가장 자연스러운 화해(그쪽은 **산화물**, 이쪽은 **황화물**)조차
  명시하지 않는다.
→ **"edge-sharing이 좋다"를 일반 명제로 인용하면 안 된다.** "황화물 4조성에서" 라는 단서 필수.

### 6. **CSM 기술자의 분리가 조성에 따라 무너진다**
Fig 5a(Li₂SiS₃)에서는 edge가 더 왜곡(밝은색)된 게 보이지만, **Fig 5b(Li₄SiGeS₆)에서는 edge(rank 5)가
오히려 어두운색(CSM 2–3.5)** 이고 corner rank 2·3·4 쪽에 노란 점(CSM 5–5.5)이 많다.
**요약 통계(평균±표준편차)도, 상관계수도, 회귀도 논문에 없다.** 세 기술자와 D의 관계는 **전부 육안 주장**이다.
→ "predictive indicators"라는 표현은 과하다. **상관 정도만 보였고 예측력은 시험하지 않았다.**

### 7. **표본이 얇다**
- edge-sharing 구조: Li₂SiS₃ 5개, Li₂GeS₃ 2개, Li₄SiGeS₆ **1개**, Li₄SiSnS₆ 2개. **총 10개.**
- Li₄SiGeS₆의 "edge가 최고"라는 결론은 **단일 구조**에 기반한다.

### 8. **합성 논의가 "E_hull < 50 meV/atom" 한 줄뿐**
Table S2 전원이 컷을 통과하지만, 이건 **열역학적 접근성 상한**일 뿐 합성 경로가 아니다.
Li₂SiS₃ edge상만 실제 합성 선례(Kanno, 변형 조건)가 있고 **나머지 9개 edge 구조는 합성 보고 0**이다.
Li₂GeS₃는 논문 스스로 **"보고된 구조가 전부 corner-sharing"** 이라 인정한다.

### 9. **AIMD 셀 크기·스핀·time step이 본문에 없다**
*"Based on our previous studies, we used the same computational guidelines … including cell size, spin, time
step, and simulation temperature"* (refs 46–49). **refs 47 = Jun, B.; Lee, S. U., JMCA 2022, 10, 7888**
(argyrodite in-cage size 기술자 논문 — 우리에게도 직접 관련) 을 봐야 실제 셀이 나온다. **미보유.**
→ **AIMD 파라미터는 이 논문만으로는 재현 불가.**

### 10. **자유에너지 교차온도가 본문과 그림에서 어긋난다**
SI 본문: *"for Li₂SiS₃ and Li₂GeS₃, the edge-sharing phase becomes thermodynamically favored above ~480 K"*
Fig S8: Li₂SiS₃ = **360 K**, Li₂GeS₃ = **480 K**. → 그림 값을 쓸 것.
또 **Li₄SiGeS₆는 280 K에서 방향이 반대**다(280 K **위에서 corner이 더 안정**해진다 — 영점에너지 효과).
Li₄SiSnS₆는 1000 K까지 교차가 없다. **"고온에서 edge가 유리"는 4조성 중 2조성에만 해당한다.**

### 11. **본문 내부 수치 불일치 2건**
- "four candidate compositions exhibited negative ΔE" vs "in **five** cases where CSP discovered structures
  with lower energy" — Fig 2a는 **5개**(Li₃PS₄, Na₃YBr₆, LiAlCl₄, Na₃PS₄, Na₃YCl₆).
- Table S1에서 Li₃AuO₃와 Li₂BPt₃가 **같은 mp-7471**.

### 12. **비용·자원 축이 없다**
Ge·Sn 기반 황화물의 원료비·독성·대기안정성(Li₂SiS₃류는 H₂S 발생 우려 대상) 논의가 전무하다.
우리 cascade의 `cost_tier`·`air_hsab` 축이 여기에도 없다 — 이상욱 랩 3부작 전체의 공통 공백.

---

## 12. Figure set ★

| Fig | 내용 | 우리가 쓸 것 |
|---|---|---|
| **1** | CSP 워크플로 전도(초기구조 → CSP 루프 → 최종 CSP). 좌하단에 MTP-vs-DFT 상관 산점도(Initial/50/100/200 Gen 색분), 우측 GA 연산 아이콘, 하단 RDF 검증 | **T1 설계 참고**: active learning 루프의 표준 도해. 우리 UMA는 이 루프의 "query DFT" 부분이 없다는 게 그림 하나로 보인다 |
| **2a** | ΔE(예측−실험) 14조성, PBE(파란 원) vs SCAN(초록 삼각), PBE-fail(빨간 X) | **§11-3 근거.** functional 하나로 부호가 뒤집히는 실증 — 우리 "method-dependence 먼저 의심" 규율의 외부 사례 |
| **2b** | 벤 도해: `ΔE_pred < ΔE_ref`(파랑) ∩ `Prediction = Reference`(빨강). 구조 썸네일 14개 | 검증 성적 요약. ⚠ Li₃YCl₆(P-3m1→P1)이 "일치"에 들어간 관대함 확인용 |
| **3a** | corner / edge / mixed 연결방식 3분류 도해 (단위셀 안 S²⁻·양이온 배치) | **④′ 도펀트–PS₄ 연결방식 기술자**의 시각적 원형 |
| **3b–e** | 4조성 × (rank 1–10) 이중축: 마커=**D_600K**, 보라 막대=**E_rel** | ⭐ **덱 슬 28의 원본.** "안정성 순위 ↔ 확산"이 **역상관**임을 한 장에 보이는 양식. **우리 disorder ensemble 배열별 D 플롯에 그대로 이식 가능한 도표 문법** (rank vs D + E 막대) |
| **4a** | corner상 Li 확률밀도 등가면 + van Hove(2조성) — **"Li trapped"** | T12. 갇힘의 시각화 |
| **4b** | edge상 동일 — **"Li diffuse"**, 흰 점선으로 장거리 확산 표시 | T12. **MSD로는 못 가르는 걸 가른다** |
| **4c** | edge상 Li 경로 확대 + **다면체 사이 틈에 Li 없음(✕)** | dead volume의 직접 증거 |
| **4d** | **dead volume 형성 스키마** — 두 다면체 사이 pseudopolyhedron void, Li 접근 ✕ | **개념 그림. 우리 BVSE 해석 언어에 이식** |
| **4e** | corner(d_c) vs edge(d_e) 중심간 거리 비교 스키마, **d_c > d_e** | 기하 논증 |
| **4f** | 다면체 부피 / dead volume 분포 (Li₂SiS₃, Li₄SiGeS₆) — 파랑=corner, 주황=edge | **정량 근거.** Δdead ≈ −0.69 Å³ 양쪽 |
| **5a,b** | rank 1–10 × {초록막대=α, 원 높이=Li–S₄ 부피, 원 색=CSM} **3정보 1축** | ⭐ **세 기술자 동시 표시 양식.** 우리 47종 6축 플롯에 참고할 만한 다중부호화. 단 §11-6의 판독 한계 |
| **S1** | 14조성 참조 vs 예측 구조 + 공간군 | §5d 표의 원본 |
| **S2** | Li–Si–S–[Ge, Sn] 상도 (MP), 초록 안정영역 + 빨간 조성 경로 + ★ | "phase-diagram-guided"의 실체 |
| **S3** | 4조성 MTP vs DFT 상관 (상: 전체 train/valid, 하: 세대별 색분) + MAE_a/MAE_f | **§11-4 근거.** 세대가 진행되며 저에너지 영역 점이 채워지는 게 보임 |
| **S4–S7** | 4조성 각 rank 1–10 구조 + **MSD 원자료**(Li/M/S 분해) | ⭐ **MSD 원자료 공개.** rank 8(Li₂SiS₃)의 25 ps 계단, rank 6(Li₂GeS₃)의 45 ps 이후 급상승 등 **60 ps가 짧다는 증거가 그림 안에 있다** |
| **S8** | G(T) 0–1000 K, corner vs edge, 4조성. 교차온도 표시 | ⭐ **$S_{\text{vib}}$ 축.** `ordered_vs_disordered.md` §9 보강 |
| **S9** | Li₂SiS₃ RDF (Li/Si/S 각 쌍) 보고구조 vs 예측구조, corner·edge 각각 | 구조 동일성 검증 방식. **우리 disorder config 비교에도 쓸 수 있는 값싼 검증** |
| **S10** | Fig 4f의 전체 범위판(축 5–12 Å³) + 확대. Li₄SiGeS₆ corner에 **~11.7 Å³ 이상치 1개** | 이상치 존재 확인 |
| **S11** | Li–S₄ 사면체 인력(a) / 왜곡 시 long distance·large volume(b) 개념도 | 기술자 ②③의 물리 그림 |
| **S12** | Fig 5의 Li₂GeS₃ / Li₄SiSnS₆ 판 | α 분리의 4조성 일반성 확인 |

---

## 13. Post-processing ★

- **무엇**: (a) **다면체 연결방식 분류**(수동), (b) **RDF** 비교(구조 동일성), (c) **공간군** 분석,
  (d) **MSD → D** (AIMD 60 ps @600 K), (e) **Li 확률밀도 등가면**, (f) **van Hove 자기상관** $4\pi r^2 G_s(r,t)$,
  (g) **다면체 부피 / dead volume**, (h) **packing ratio α**, (i) **CSM**, (j) **phonon → $F_{\text{vib}}$ → G(T)**,
  (k) **E_hull** (convex hull)
- **도구**: **VASP 5.4.4**(DFT·AIMD) · **LAMMPS**(MTP-MD/완화) · **USPEX**(GA) · **MLIP 패키지**(MTP) ·
  **phonopy** · **pymatgen**(*"The overall process for CSP was supported by PyMatGen"*)
- **수치화·기록**: D는 Fig 3에 `×10⁵ cm²/s` 스케일로 마커, E_rel은 같은 축에 보라 막대(이중축).
  α·Li–S₄ 부피·CSM은 Fig 5에서 **막대 높이 / 원 높이 / 원 색**으로 3중 부호화.
  **원자료 figshare 공개** (`10.6084/m9.figshare.29468165.v4`) — ⚠ 우리는 미확인.
- ⛔ **없는 것**: NEB, Bader, COHP/ICOHP, DOS/PDOS, ELF, ESW/grand-potential, 탄성, 계면 반응성.
  **이 논문은 순수하게 "구조 ↔ 확산" 한 축이다.**

---

## 14. 우리 DFT 대비 (`our_dft_baseline.md`)

| 항목 | 이 논문 | 우리 (comp1 / modelc) | 차이 / 이유 |
|---|---|---|---|
| code / functional | VASP 5.4.4 · **PBE** · PAW | QE · PBE | ✓ 같은 계열 |
| k-mesh | **0.05 Å⁻¹ 간격** Monkhorst–Pack | 조성별(52 at ordered / 62 at single-config) | 규약 다름, 비교 가능 |
| ecut | **500 eV** (=36.7 Ry) | (우리 표준값 별도) | 형식 동일 |
| 힘 수렴 | **< 0.04 eV/Å** | — | ✓ `kim2026_hts…`와 동일 문턱 |
| **동역학 엔진** | **AIMD**(VASP, NVT Nosé–Hoover) | **MLIP-MD**(UMA-s-1p1, Langevin NVT) | ⚠ **힘 계산 축이 다르다.** "둘 다 MD"로 뭉뚱그리지 말 것 |
| 온도 | **600 K 단일** | **600 / 800 / 1000 K** (400·500 K 제외 판정) | **우리가 더 넓다** — 그들은 Arrhenius를 못 한다 |
| 시간 | **60 ps** | equilib 5 ps + prod **200 ps**, MSD 창 **2–50 ps** | **우리가 3배 이상 길다** |
| 시드 | **1** (명시 없음, 반복 언급 없음) | **3-seed** (modelc Ea 0.197±0.032) | **우리 우위 — 오차막대가 있다** |
| D 보고 | 절대값, 오차막대 없음 | 절대값 인용 금지 규율 | **우리 규율이 더 보수적** |
| σ 보고 | **없음** | NE(Haven=1), 절대값 인용 금지 | — |
| Ea 보고 | **없음** | 0.253 (comp1) / 0.224 (modelc) eV | 우리만 있음 |
| **무질서 처리** | **없음** — 예측된 단일 배열(폴리모프)을 그대로 | **disorder ensemble + 배열간 분산 오차막대** | **문제설정이 다르다.** 그들 자유도는 공간군, 우리 자유도는 자리 점유 |
| 합성가능성 | **E_hull < 50 meV/atom** (Table S2) | **없음** (host 대비 상대 Δe만) | ⚠ **우리 공백 = T10** (`lee2024` digest에서 이미 등록). **두 논문이 같은 컷을 쓴다** |
| 자유에너지 | **phonopy $F_{\text{vib}}$, G(T) 0–1000 K** | **없음** (0 K DFT만) | ⚠ **우리 공백.** `ordered_vs_disordered.md`의 $S_{\text{vib}}$ 유보를 닫을 도구 |
| 기계 | 없음 | E/B/G, 전 C_ij, EOS | **우리 우위** |
| 전자구조 | 없음 | canonical gap 4개(fixed-occ nscf) | **우리 우위** |
| ESW / 계면 | 없음 | grand-potential onset 2.256 V, M6 94쌍 | **우리 우위** |
| 수송 대리지표 | **α + Li–S₄ 부피 + CSM** (구조 기하) | **BVSE 채널 %** (정전 퍼텐셜) | 같은 목적, 다른 물리. **α는 정의가 불완전** (§10c) |
| MLIP 전략 | **조성마다 MTP 신규 학습** | **UMA 사전학습 횡단** | 정반대. 같은 랩 `kim2026_hts…`는 SevenNet 사전학습 그대로 — **랩 내부에서도 갈린다** |

---

## 15. 채택 / 실행 항목

| # | 항목 | 근거 | 비용 | 우선 |
|---|---|---|---|---|
| **A** | **`external_benchmarks_symposium_2026.json` 정정** — `csp_metastable_conductivity` 의 σ 3값 삭제(논문에 없음), 기술자 3개를 **α / Li–S₄ 부피 / CSM** 로 교체, 논문 실제 수치(2 orders 계산 · 3 orders 인용) 기입 | §9-A, §9-C | 소 | **1** |
| **B** | **T12(van Hove) 승격** — 두 논문(`lee2024`, 본 논문)이 독립적으로 같은 진단을 쓴다. 특히 "MSD가 둘 다 ~0일 때" 가르는 유일한 도구 | §8a | 소 | **1** |
| **C** | **Li–(S,Cl)₄ 부피 + CSM 을 기존 UMA-MD 궤적에 후처리** — 새 시뮬레이션 0. 47종/농도별로 계산해 BVSE 채널 %와 **교차검증**. 두 지표가 어긋나는 도펀트 자체가 결과 | §10c | 소 | **2** |
| **D** | **④′ 도펀트–PS₄ 연결방식 기술자 (신규, T13)** — 도펀트 다면체가 PS₄와 공유하는 S 개수(0/1/2)를 47종에 세기. **우리 계에서만 정의되는 변형**이고 문헌 선례 없음 | §10c | 소 | 3 |
| **E** | **`ordered_vs_disordered.md` §9에 $S_{\text{vib}}$ 사례 추가** — Fig S8(교차온도 280–480 K), Li₄SiGeS₆의 **영점에너지만으로 0 K 순위 반전** | §10e | 소 | **2** |
| **F** | **T10(E_hull 합성가능성 필터) 재확인** — `lee2024`(<50 meV/atom)와 본 논문(<50 meV/atom)이 **같은 컷**. 우리 G1이 vacuous한 근본 원인의 두 번째 외부 근거 | §14 | 중 | 3 |
| **G** | **BVSE 해석 언어에 "dead volume" 도입** — "채널 %" 대신 "Li-accessible volume vs dead volume"으로 서술 | §8b | 0 | 3 |
| ❌ | **α(eq 9) 재구현** | $V_{\text{dead}}$ 정의 부재 → 재현 불가, 우리 BVSE가 더 낫다 | — | **안 함** |
| ❌ | **CSP 도입** | 문제설정 다름. + 논문 스스로 **>80 atom 셀 한계** 자백 | — | **안 함** |

---

## 16. 인용 가능 문장 (deck/manuscript용)

- "조성이 같아도 [MS₄] 다면체 연결방식이 corner-sharing이냐 edge-sharing이냐에 따라 600 K Li 확산계수가
  **2자릿수 이상** 갈린다 — 열역학적으로 가장 안정한 상이 이온전도에서는 최악이다[Kim 2025]."
- "다면체 사이의 빈 공간이 모두 전도 경로인 것은 아니다. 중심 양이온의 정전 반발로 Li가 접근할 수 없는
  **dead volume**이 존재하며, edge-sharing 위상은 이 dead volume이 corner-sharing 대비 약 **11–12 % 작다**[Kim 2025]."
- "corner-sharing과 edge-sharing이 섞인 mixed 위상은 두 성질의 평균이 아니라 **corner이 병목으로 작용해
  전체 확산을 지배한다**[Kim 2025]." (⭐ 우리 퍼콜레이션 프레임과 동형)
- "CSP로 예측된 40개 폴리모프가 전부 **E_hull ≤ 42 meV/atom** 안에 들어, 준안정 고전도상이 합성 접근
  가능한 에너지 범위에 다수 존재함을 보인다[Kim 2025, Table S2]."
- "이종 원소 연결(Si–Ge)로 형성된 준안정 위상은 동종 연결(Si–Si) 대비 구조적 유연성이 커서
  상대 에너지 페널티가 작다[Kim 2025]." (⚠ 정성 서술, 정량 분해 없음)
- "MLIP 기반 CSP는 단위셀 **80 원자·복잡 배위**를 넘으면 저에너지 영역 정확도가 무너진다
  (LiGa(SeO₃)₂에서 MAE_f 114 meV/atom)[Kim 2025 SI]." (⭐ 우리가 CSP를 안 하는 판단의 외부 근거)
- ⛔ **인용 금지**: "Li₂SiS₃ 준안정상이 σ를 4자릿수 올린다" — **이 논문에 그런 수치가 없다**(§9-A).
- ⛔ **인용 금지**: 본문 산문의 E_rel 값(<0.2 / ≥0.3 / ≤0.1 / ≤0.3 eV/atom) — Fig 3·Table S2와 10× 어긋난다(§9-B).
- ⚠ **단서 필수**: "edge-sharing이 좋다"는 **황화물 4조성**에 한정. 산화물에서는 Jun 2022(Nat. Mater.)가
  **corner-sharing이 좋다**고 하고, 이 논문은 그 충돌을 해소하지 않았다(§11-5).

---

## 17. 기술 용어 미니 사전 (이 논문을 읽는 데 필요한 것만)

| 용어 | 뜻 | 이 논문에서의 역할 |
|---|---|---|
| **CSP** (crystal structure prediction) | 조성만 주고 결정구조를 계산으로 찾는 것 | 전체 프레임워크 |
| **USPEX** | 진화(유전) 알고리즘 기반 CSP 코드. 자손을 heredity/mutation으로 만들고 에너지로 선택 | 구조 생성기 |
| **antiseed** | 이미 찾은 구조 주변에 가상 페널티를 얹어 **같은 곳을 반복 탐색하지 않게** 하는 USPEX 옵션 | 다양성 유지 |
| **soft mutation** | 가장 무른(저주파) phonon 모드 방향으로 원자를 밀어 새 구조를 만드는 변이 | 자손 생성 연산 |
| **MTP** (moment tensor potential) | descriptor 기반 MLIP. 국소 환경을 moment tensor로 전개(SI eq 1–4) | 에너지·힘 대리 모델 |
| **lev_max** | MTP basis의 전개 차수 상한(`2+4μ+ν`). 클수록 정확·비쌈 | =20 |
| **active learning** | 모델이 **불확실하다고 판단한 구조만** 골라 DFT를 돌리고 재학습 | DFT 비용 절감 |
| **query structure** | active learning이 고른, DFT를 돌릴 구조 | — |
| **melt-quench-anneal** | 고온 융해 → 급랭 → 어닐로 amorphous를 만들어 PES를 넓게 표본화 | 초기 학습셋 |
| **corner-sharing / edge-sharing** | 두 다면체가 꼭짓점 1개 / 모서리(꼭짓점 2개)를 공유 | 핵심 분류축 |
| **dead volume** | 다면체 사이의 빈 공간 중, 중심 양이온 정전 반발로 **Li가 못 들어가는** 부분 | 이 논문의 신조어 |
| **packing ratio α** | (다면체 부피 + dead volume)/셀 부피. **낮을수록 Li가 쓸 공간이 많다** | 기술자 ① |
| **Li–S₄ 부격자** | Li 하나를 둘러싼 S 4개가 만드는 사면체 | 기술자 ②의 대상 |
| **CSM** (continuous symmetry measure) | 실제 다면체가 이상 대칭 다면체에서 얼마나 벗어났는지의 0–100 척도 | 기술자 ③ |
| **van Hove 자기상관** $G_s(r,t)$ | 시각 t에 **같은 입자가** 처음 위치에서 거리 r에 있을 확률밀도. `r<2 Å` 단일 피크 = 갇힘 | 갇힘/자유 판별 |
| **E_rel** | 같은 조성의 **최안정 예측 구조 대비** 상대 퍼텐셜에너지 | Fig 3 보라 막대 |
| **E_hull** | convex hull **위로** 얼마나 떠 있나. <50 meV/atom = 합성 가능성 통설 | Table S2 |
| **phonopy / $F_{\text{vib}}$** | 조화 phonon으로 진동 자유에너지를 계산 → G(T) = E_DFT + F_vib + pV | Fig S8 |
| **MAE_a / MAE_f** | MTP 에너지 오차: 전체 학습셋(a) / **최저에너지에서 0.2 eV/atom 이내**로 거른 것(f) | Fig S3, Table S1 |
| **RDF** | 방사분포함수 g(r). 예측 구조와 보고 구조가 같은지 값싸게 검증 | Fig S9 |

---

## 18. 이 digest가 남긴 열린 질문

| # | 질문 | 닫는 방법 |
|---|---|---|
| Q1 | 덱의 `0.0001 / 2.4 mS/cm` 는 어디서 왔나 | **Huang et al., JACS 2022, 144, 4989** PDF 확보 (ref 36) |
| Q2 | AIMD 셀 크기·time step·스핀은 정확히 무엇인가 | **Jun, B.; Lee, S. U., JMCA 2022, 10, 7888–7895** (ref 47) PDF 확보 — argyrodite in-cage size 기술자 논문이라 **우리에게 이중으로 필요** |
| Q3 | $V_{\text{dead}}$ 의 실제 알고리즘 | figshare 원자료 `10.6084/m9.figshare.29468165.v4` 확인 |
| Q4 | corner vs edge 순위가 SCAN에서도 유지되나 | 논문에 없음. **우리가 판정할 수 없음** — over-claim 경고로만 남김 |
| Q5 | Jun 2022(Nat. Mater.) 의 corner-sharing 주장과의 관계 | ref 88 PDF 확보. **산화물 vs 황화물** 가설 검증 |
| Q6 | DFT query 총 횟수 / 학습셋 크기 | 논문·SI 미보고. 저자 문의 외 방법 없음 |
