# Machine Learning-Assisted Crystal Structure Prediction of Solid-State Electrolytes Reveals Superior Ionic Conductivity in Metastable Edge-Sharing Phases — Ji Hoon Kim (JACS 2025)

> slug `kim2025_csp_metastable_edge_sharing_sse` · DOI `10.1021/jacs.5c15665` · type `CSP(USPEX+MTP active learning) + DFT + AIMD` ·
> *J. Am. Chem. Soc.* **2025, 147, 47381–47391** · 투고 2025-09-07 / 수정 2025-12-05 / 수리 2025-12-08 / 게재 2025-12-12 ·
> 본문 11 pp + SI 24 pp · digested 2026-07-28 · status ✅ (본문 + SI 전수 정독, Fig 2/3/4/5·S1–S12·Table S1–S2 전부 판독)
> · **2026-08-04 본문(11 pp) 실물 독립 검증 완료 — §19** (자기철회 2건 · 신규 적발 8건 · Q2 해소. ⚠ SI 실물은 이번 회차에 없음)
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

## 0.5 처음 읽는 사람을 위한 배경 (이 논문이 전제하는 것들)

**CSP(결정구조 예측) — 깔때기의 입구를 바꾼다**
앞의 스크리닝 논문들은 전부 **이미 존재가 확인된 구조**(ICSD/COD)에서 골랐다.
CSP 는 반대다 — 조성만 정해 주고 **"이 조성이 취할 수 있는 구조를 컴퓨터가 만들어낸다"**.
그래서 아직 아무도 합성한 적 없는 후보가 나온다. 깔때기의 입구가
'DB 에 있는 것' → '있을 수 있는 것' 으로 넓어진다.

**USPEX = 진화탐색**
구조 후보를 무작위로 뿌리고, 에너지가 낮은 것들을 골라 "교배·돌연변이" 시켜 다음 세대를
만든다. 생물 진화의 비유 그대로다. 문제는 **세대마다 수백 개 구조의 에너지가 필요**하다는 것 —
DFT 로 하면 끝이 없다.

**MTP active learning = 그 비용을 없애는 장치**
MTP(moment tensor potential)는 MLIP 의 한 종류다. **능동학습(active learning)** 은
"모델이 자신 없어 하는 구조만 골라 DFT 로 계산해서 다시 학습" 하는 방식이다.
그래서 DFT 호출이 전체 구조 수가 아니라 **모델이 헷갈린 구조 수**로 줄어든다.
CSP 가 실용적이 된 건 이 조합 덕분이다.

**metastable(준안정)이 왜 중요한가 ★**
에너지가 가장 낮은 구조(바닥상)만 좋은 게 아니다. 조금 위에 있지만 실제로 만들어지고
성능이 더 좋은 상이 있다 — 이 논문의 **edge-sharing 상**이 그렇다.
- **corner-sharing** = 다면체가 꼭짓점 하나로 이어짐 (더 흔하고 보통 더 안정)
- **edge-sharing** = 모서리를 공유해 이어짐 (더 촘촘, Li 통로가 달라진다)
⚠ 대신 **준안정상이 실제로 합성되는지는 이 논문이 답하지 않는다.** 계산이 "존재 가능"
   이라고 말하는 것과 실험이 "만들어진다" 고 말하는 것은 다르다.

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
| **packing ratio α** | Li₂SiS₃: corner **0.0834–≥0.100** vs edge **0.0753–0.0796** <br> Li₄SiGeS₆: corner **0.088–≥0.100** vs edge **~0.082** | AIMD 600 K 60 ps 평균 | Fig 5. **네 조성 모두 edge가 낮음**. ⚠ 일부 막대가 축 상한 0.100에서 **클립** → 상단 판독 불가 (§19 N6·N7, 2026-08-04 재판독) |
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

## 3.5 진화탐색이 실제로 도는 방식

1. **초기 세대** — 주어진 조성으로 무작위 구조 수십~수백 개를 만든다(대칭을 걸어 생성).
2. **평가** — 각 구조의 에너지를 구한다. ← 여기가 병목. MLIP 가 이걸 맡는다.
3. **선택** — 에너지 낮은 것들만 남긴다.
4. **변이** — 남은 것들을 섞고(heredity) 흔들어(mutation) 다음 세대를 만든다.
5. 2–4 를 수렴할 때까지 반복.

**능동학습(active learning)이 끼는 자리는 2번이다.** MLIP 가 "이 구조는 내 학습 범위 밖" 이라고
판단하면 그것만 DFT 로 계산해서 학습에 추가한다. 그래서 DFT 호출 수가 구조 수가 아니라
**모델이 헷갈린 횟수**로 줄어든다 — CSP 가 실용적이 된 결정적 이유다.

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

## 6.5 연결방식(connectivity)이 뭔가

결정을 원자 하나하나가 아니라 **다면체(polyhedron)** 단위로 보면 구조가 훨씬 잘 읽힌다.
예: PS₄ 사면체, NiO₆ 팔면체. 그 다면체들이 서로 어떻게 이어지느냐가 **연결방식**이다.
- **corner-sharing (꼭짓점 공유)** — 원자 1개를 공유. 가장 헐겁고 흔하다.
- **edge-sharing (모서리 공유)** — 원자 2개를 공유. 다면체 중심끼리 더 가까워진다.
- **face-sharing (면 공유)** — 원자 3개 공유. 중심끼리 너무 가까워 정전기적으로 불리하다.
Li 가 지나다니는 **빈 공간의 모양과 넓이**가 이 연결방식으로 결정되므로, 연결방식이
확산을 지배한다는 이 논문의 결론이 여기서 나온다.

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

> ⚠ **[2026-08-04 실물 검증] Fig 3 캡션의 마커 오기**: 캡션은 *"edge-sharing (orange **circles**)"* 라고 적지만,
> 실제 Fig 3b–e 의 edge 마커는 **주황 사각형**이고 본문 산문(*"the metastable edge-sharing topology (**orange
> square**)"*, p 47387)과 Fig 5 캡션(*"orange squares (edge-sharing)"*)도 사각형이라 적는다. **위 표의 "주황 사각"이
> 맞고 Fig 3 캡션이 틀렸다.** 같은 캡션에 *"The **insects** depict representative crystal structures"*(insets 오타)도 있다.

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

## 7.5 '왜 빠른가' 를 설명하는 표준 어휘

확산 기구를 설명할 때 반복해서 나오는 개념 셋이다.
- **병목(bottleneck)** — Li 가 지나가야 하는 가장 좁은 목. 여기 반지름이 장벽을 지배한다.
  (우리 BVSE 채널 분석이 재는 것이 정확히 이것이다.)
- **자리 에너지 지형** — 앉는 자리(우물)와 넘는 목(장벽)이 번갈아 있는 지형.
  **우물이 너무 깊어도 안 좋다** — 갇힌다. 자리들이 **고르게 얕을 때** 가장 잘 통한다.
  (SDCP Li⁺ 지형에서 우리가 "편차 0.43 vs 1.27 eV" 를 본 것과 같은 논리다.)
- **퍼콜레이션(percolation)** — 통로가 국소적으로만 뚫려 있으면 소용없고, **결정 전체를 관통**해야
  전도가 된다. 그래서 "장벽이 낮다" 와 "전도가 된다" 는 다른 말이다.

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
| **Li₂SiS₃** (Fig 5a) | **0.0834–≥0.100** (rank 2 클립) | **0.0753–0.0796** | — | ✅ **완전 분리** (corner 최저 0.0834 > edge 최고 0.0796) |
| **Li₄SiGeS₆** (Fig 5b) | **0.088–≥0.100** (rank 1 클립) | **~0.082** (1개) | **≥0.100** (rank 7, 클립) | ✅ 분리 (단 edge 표본 1개). ⚠ mixed 와 corner rank 1 이 **둘 다 클립**이라 "mixed 가 최고" 는 단정 불가 |
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

> 🔑 **덱은 정본이 아니다** — 이 σ 수치 건(덱 `10⁻⁴ → 2.4 mS/cm` 4자릿수)은 **실제 덱 오류가 맞다**
> (2026-08-03 덱 실물 슬 28 재판독에서 그 표기를 그대로 확인). → json 정정 필요.
> ⚠ 다만 함께 인용하던 **`kim2026_hts…` 의 "17,233 Li-P-S-O" 건은 철회**됐다 — 덱 원문은
> `17,230 Li, O` 로 논문과 일치했고 틀린 쪽은 우리 전사였다(`talks/lee2026_skku_…` §15b).

### 9-B. ⚠ **E_rel 본문 서술값이 Fig 3 축 범위와 10× 어긋난다**

| 본문 서술 | Fig 3 / Table S2 실측 |
|---|---|
| Li₂SiS₃: *"relative potential energy difference … is **<0.2 eV/atom**"* | Fig 3b 최대 **~0.017 eV/atom**, E_hull 최대 **12 meV/atom** |
| Li₂GeS₃: *"edge-sharing … **E_rel ≥ 0.3 eV/atom**"* | Fig 3c edge = **~0.031, ~0.042 eV/atom**, E_hull 12·34 meV |
| Li₄SiGeS₆: *"relatively low E_rel (**≤0.1 eV/atom**)"* | Fig 3d edge = **~0.009 eV/atom**, E_hull 7 meV |
| Li₄SiSnS₆: *"relatively low E_rel (**≤0.3 eV/atom**)"* | Fig 3e edge = **~0.011, ~0.022 eV/atom**, E_hull 0·10 meV |

**Fig 3b–e의 E_rel 축 상한은 4개 패널 모두 0.05 eV/atom** 이고, Table S2의 E_hull은 **전 40구조 0–42 meV/atom**이다.
→ **그림·표는 자기들끼리 정합하고, 본문 산문만 10배 크다.** 본문 오타로 보이지만 논문에 정오표는 없다.

> 🔧 **[2026-08-04 실물 검증 — 이 절의 정밀화]** 본문 4문장을 원문 그대로 대조하니 **성격이 서로 다르다**:
>
> | 조성 | 본문 원문 | 부등호 방향 | 판정 |
> |---|---|---|---|
> | Li₂SiS₃ | *"is **<0.2 eV/atom**"* | 상한 | 실측 0.017 → **형식상 참**(느슨할 뿐) |
> | **Li₂GeS₃** | *"relatively high formation energies (E_rel **≥ 0.3 eV/atom**)"* | **하한** | 실측 0.031·0.042 → 🔴 **정면 모순, 10× 과대** |
> | Li₄SiGeS₆ | *"relatively low E_rel (**≤0.1 eV/atom**)"* | 상한 | 실측 0.009 → **형식상 참** |
> | Li₄SiSnS₆ | *"relatively low E_rel (**≤0.3 eV/atom**)"* | 상한 | 실측 0.011·0.022 → **형식상 참** |
>
> → **엄밀한 모순은 Li₂GeS₃ 1건뿐**이다. 나머지 3건은 상한 서술이라 논리적으로 틀리지 않았다.
> **다만 4문장이 서로 비교되며**(*"significantly higher than those of Li₂SiS₃"*, *"suggesting higher experimental
> feasibility compared with Li₂GeS₃"*) **0.1–0.3 eV/atom 스케일의 자기완결적 서사**를 만드는데, 그림·표의 실제 세계는
> **0.003–0.044 eV/atom**이다. 한 자릿수 다른 두 서술이 한 논문 안에 공존한다.
> ⚠ 종전 표현("본문 산문 전부가 10× 어긋난다")은 과했다 → **위 표로 대체.** 인용 규칙(그림·표 값만 쓴다)은 그대로.

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

> 🔴🔴 **[2026-08-04 실물 검증 — 이 항목의 격상] 모순은 SI가 아니라 본문에 있다.**
> 본문 p 47384 원문: *"…four systems (Li₃PS₄, Na₃YBr₆, Na₃PS₄, and Na₃YCl₆) not only exhibited improved stability
> but also reproduced experimental structures within PBE, as shown in Figure 2b. **Their potential validity was
> confirmed through SCAN calculations, ruling out PBE-related artifacts.**"*
> — 그런데 **바로 그 4건 중 2건이 SCAN에서 양수로 뒤집힌다**(Fig 2a 재판독: Li₃PS₄ **+8**, Na₃PS₄ **+23** meV/atom).
> ΔE > 0 = 예측 구조가 참조보다 **덜** 안정. 즉 **SCAN은 "확인"한 게 아니라 절반을 반증했고, 본문은 그 반대로 적었다.**
> → 이건 SI 문장 대 그림의 문제가 아니라 **본문 대 자기 그림(Fig 2a)의 정면 모순**이다. 항목 강도 상향.
> ⚠ 인용 시: **"SCAN으로 검증됐다"는 이 논문의 주장은 인용 금지.** 인용 가능한 것은 *"SCAN 5건 중 3건에서 ΔE 부호
> 반전"* 이라는 **우리 판독**뿐이다.
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
- 이 논문은 충돌을 **인정만 하고 넘어간다**.
→ **"edge-sharing이 좋다"를 일반 명제로 인용하면 안 된다.** "황화물 4조성에서" 라는 단서 필수.

> 🔧 **[2026-08-04 실물 검증 — 부분 자기철회]** 종전 이 항목은 *"가장 자연스러운 화해(그쪽은 산화물, 이쪽은
> 황화물)조차 명시하지 않는다"* 라고 적었다. **틀렸다 — 논문은 그 문장 안에 "oxide"를 적어 놓았다**:
> *"…revealed that corner-sharing **oxide** structures achieved moderate ionic conductivities below 1 mS/cm…"*
> **남는 비판은 더 날카로운 형태로 바뀐다**: 화해의 열쇠(음이온 화학이 다르다)를 **자기 문장 안에 이미 써 놓고도**
> 그것을 근거로 삼지 않고 *"further investigation is essential"* 로 덮는다.
>
> 🆕 **그리고 더 이상한 것**: 같은 **ref 88(Jun/Ceder)** 을 **두 쪽 뒤에서는 자기 기술자의 근거로 인용한다** —
> p 47388 *"previous studies have indicated that significant polyhedral distortion reduces the activation energy…
> as shown in Figure S11b.^**88,89**"* (ref 89 = **Di Stefano et al., "Superionic diffusion through frustrated
> energy landscape", Chem 2019, 5, 2450**). **자기 결론을 반박하는 논문을 자기 기술자 ③(CSM)의 권위로 삼는 셈**이다.

### 6. **CSM 기술자의 분리가 조성에 따라 무너진다**
Fig 5a(Li₂SiS₃)에서는 edge가 더 왜곡(밝은색)된 게 보이지만, **Fig 5b(Li₄SiGeS₆)에서는 그 분리가 무너진다.**
**요약 통계(평균±표준편차)도, 상관계수도, 회귀도 논문에 없다.** 세 기술자와 D의 관계는 **전부 육안 주장**이다.
→ "predictive indicators"라는 표현은 과하다. **상관 정도만 보였고 예측력은 시험하지 않았다.**

> 🔧🆕 **[2026-08-04 실물 검증 — 판독 정정 + 훨씬 날카로운 형태]**
> 종전 서술("edge rank 5가 오히려 어두운색 CSM 2–3.5, corner rank 2·3·4에 노란 점 5–5.5")은 **부정확했다.**
> Fig 5b 고배율 재판독(700 dpi):
> - **edge(rank 5) = 적/주황, CSM ≈ 3–4.5** (어두운색 아님)
> - **가장 밝은 점(흰색, CSM ≈ 5.5–6.0)은 corner rank 8·9·10 에 몰려 있다**
> - corner rank 1(최안정) = 검정 CSM ≈ 2.0–2.5 (본문의 *"exceptionally low CSM"* 주장은 여기서는 맞다)
>
> → 본문 주장 *"the edge-sharing phases in **both compositions** … their Li–S₄ sublattice volume and **CSM values
> are relatively higher**"* 은 **Li₄SiGeS₆에서 CSM에 대해 성립하지 않는다.** (Li–S₄ 부피는 성립: edge 7.25–7.8로 최상위.)
>
> 🔑 **그런데 여기서 훨씬 흥미로운 게 나온다.** CSM이 가장 높은 corner rank **8·9·10** 은, Fig 3d에서
> **corner 7개 중 D가 0이 아닌 유일한 셋**(D = 0.64 / 0.22 / 0.14 ×10⁻⁵ cm²/s)이다.
> → **CSM은 D 와는 같이 가는데 연결방식과는 같이 가지 않는다.** 즉 이 논문의 인과사슬
> `edge-sharing → 왜곡 ↑ → D ↑` 에서 **가운데 항만 독립적으로 작동**하고 첫 화살표는 Li₄SiGeS₆에서 끊긴다.
> ⭐ **우리에게는 이게 더 좋은 소식이다** — §10c에서 CSM을 채택 후보로 올린 근거가 "연결방식의 부산물"이 아니라
> **연결방식과 무관하게 D를 따라가는 독립 기술자**라는 쪽으로 강화된다. (우리 host엔 corner/edge 축이 없으니 §10b.)

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
(argyrodite in-cage size 기술자 논문 — 우리에게도 직접 관련) 을 봐야 실제 셀이 나온다.

> ✅ **[2026-07-28 해소 — ref 47 digest 완료]** → `papers/jun2022_argyrodite_ion_cage_size_descriptor.md` §3.
> 원전이 주는 값: **VASP 5.4.1 / PAW / PBE(vdW 無·U 無) / 500 eV / 완화 3×3×3·힘 < 0.02 eV/Å;
> AIMD = Γ-only · NVT Nosé–Hoover · dt 2 fs · 600–1200 K 5~6점 · 단위셀 ~52원자(24 Li 전부 24g 완전점유) ·
> 배열×온도당 ≥3 시드 앙상블평균 · 자동종료 RSD(σ)<0.25 & 유효 hop>250(He/Mo 2018) ·
> 무질서 ~100 ps vs 질서 ≥500 ps @800 K · pymatgen-diffusion 후처리.**
> ⚠ ~~**스핀만은 ref 47 원전에도 없다** → 4항목 중 **3/4 해소, spin 은 여전히 미확정**.~~
> ✅ **[2026-08-04 실물 검증 — spin 해소, 4/4 완결]** 본문 §2.1 에 규약이 있었다:
> *"**Spin-polarized calculations were performed for systems containing 3d transition metals.**"*
> → 표적 4조성(Li–Si/Ge/Sn–S)에는 **3d 전이금속이 없다 ⇒ 비스핀(non-spin-polarized)**. 검증 14종 중
> **LiMn₂O₄만 스핀 계산 대상**. AIMD도 *"same computational guidelines … including cell size, **spin**, time step"* 이라
> 했으므로 같은 규약이 승계된다. **Q2 완전 해소.**
> 또한 이 JACS 2025 의 AIMD 는 **60 ps 단일 온도(600 K)** 로, 원전이 정한 자동종료 기준(RSD<0.25 & hops>250)을
> 만족했는지 **명시하지 않는다** — 원전 기준으로도 짧을 수 있다.

### 10. **자유에너지 교차온도가 본문과 그림에서 어긋난다**
SI 본문: *"for Li₂SiS₃ and Li₂GeS₃, the edge-sharing phase becomes thermodynamically favored above ~480 K"*
Fig S8: Li₂SiS₃ = **360 K**, Li₂GeS₃ = **480 K**. → 그림 값을 쓸 것.
또 **Li₄SiGeS₆는 280 K에서 방향이 반대**다(280 K **위에서 corner이 더 안정**해진다 — 영점에너지 효과).
Li₄SiSnS₆는 1000 K까지 교차가 없다. **"고온에서 edge가 유리"는 4조성 중 2조성에만 해당한다.**

### 11. ~~**본문 내부 수치 불일치 2건**~~ → **1건** (2026-08-04 정정)
- ⛔ **[자기철회]** 종전 항목: *"'four candidate compositions exhibited negative ΔE' vs 'in five cases…' 로 어긋난다"*.
  **본문 실물은 처음부터 'five'다** — *"Furthermore, **five** candidate compositions exhibited negative ΔE values"*.
  뒤의 *"in five cases where CSP discovered structures with lower energy…, **four** systems (Li₃PS₄, Na₃YBr₆,
  Na₃PS₄, and Na₃YCl₆) not only exhibited improved stability but also reproduced experimental structures"* 는
  **그 5건의 부분집합(4건)을 말하는 다른 문장**이다. 빠진 1건 = **LiAlCl₄**(ΔE −12로 음수지만 예측 공간군
  P2₁/m ≠ 참조 P2₁/c라 "구조 재현"에는 못 든다 — §5d와 정합). **모순이 아니었다. 우리 전사 오류.**
- ✅ **유지**: Table S1에서 Li₃AuO₃와 Li₂BPt₃가 **같은 mp-7471** (SI 항목이라 이번 회차 미재검).

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
- ⛔ **인용 금지 (2026-08-04 추가)**: **"SCAN 계산으로 검증됐다"** — 논문 본문의 이 주장은 **자기 Fig 2a 가
  반증한다**(§11-3, §19 N1). 쓰려면 우리 판독("SCAN 5건 중 3건 부호 반전")으로만.
- ⚠ **용어 주의 (2026-08-04 추가)**: 초록·본문의 **"higher packing efficiency"** 를 그대로 옮기지 말 것.
  이 논문의 α 는 **비전도 부피 분율**이고 준안정 edge 상은 α 가 **낮다** — 표준 결정학의 "채움률"과 정반대
  방향이라 그대로 인용하면 뒤집힌다(§19 N2·N3). **"낮은 packing ratio α"** 로만 쓴다.
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
| ~~Q2~~ ✅ | ~~AIMD 셀 크기·time step·스핀은 정확히 무엇인가~~ | **닫힘.** 셀·dt·온도는 ref 47 digest(`jun2022_…`)에서, **스핀은 본문 §2.1**("3d 전이금속 계만 스핀 분극")에서 확보 — §11-9 |
| Q3 | $V_{\text{dead}}$ 의 실제 알고리즘 | figshare 원자료 `10.6084/m9.figshare.29468165.v4` 확인 |
| Q4 | corner vs edge 순위가 SCAN에서도 유지되나 | 논문에 없음. **우리가 판정할 수 없음** — over-claim 경고로만 남김 |
| Q5 | Jun 2022(Nat. Mater.) 의 corner-sharing 주장과의 관계 | ref 88 PDF 확보. **산화물 vs 황화물** 가설 검증 |
| Q6 | DFT query 총 횟수 / 학습셋 크기 | 논문·SI 미보고. 저자 문의 외 방법 없음 |

---

## 19. 🔬 본문 실물 독립 검증 (2026-08-04, 폴더 이상욱 ④)

**대상**: `litdb/inbox/4. Machine Learning-Assisted Crystal Structure Prediction…pdf` = **본문 11 pp**
(JACS 2025, 147, 47381–47391). 텍스트 전수 재추출 + Fig 2a·3b–e·4f·5a·5b **500–800 dpi 재렌더 판독**.
**방식**: digest 를 정답으로 놓지 않고 **PDF 를 원점으로 다시 읽어** 기존 서술과 대조.

> ⚠ **적용 범위**: 이번 회차 실물은 **본문뿐**이다. **SI 24 pp(Table S1·S2, Fig S1–S12, eq 1–11)는 이번에
> 재검증되지 않았다** — 2026-07-28 판독을 그대로 승계한다. SI 유래 수치(E_hull 0–42, MAE, 교차온도,
> α·CSM 정의식, 공간군 표)는 **미재검** 표시로 읽을 것.

### 19a. 자기철회 2건 — 우리가 틀렸던 것

| # | 종전 서술 | 실물 | 조치 |
|---|---|---|---|
| **R1** | §11-11: *"본문이 'four candidate compositions exhibited negative ΔE' 라 적어 뒤의 'five cases' 와 어긋난다"* | 본문은 처음부터 *"**five** candidate compositions exhibited negative ΔE"*. 뒤의 *"four systems"* 는 **그 5건 중 실험 구조까지 재현한 부분집합**을 가리키는 별개 문장 (빠진 1건 = **LiAlCl₄**, SG P2₁/m ≠ P2₁/c) | **철회.** 모순 아님 — 우리 전사 오류 |
| **R2** | §11-5: *"산화물 vs 황화물이라는 화해조차 명시하지 않는다"* | 본문에 *"corner-sharing **oxide** structures"* 로 **명시돼 있다** | **부분 철회.** 비판을 "써 놓고도 안 쓴다"로 재서술 |

### 19b. 신규 적발 8건 — 본문 실물에서만 나오는 것

| # | 적발 | 위치 | 무게 |
|---|---|---|---|
| **N1** | 🔴 **본문이 자기 Fig 2a 를 부인한다.** *"Their potential validity was confirmed through SCAN calculations, ruling out PBE-related artifacts"* 라는데, 그 4건 중 **Li₃PS₄(+8)·Na₃PS₄(+23)** 는 SCAN 에서 부호가 뒤집힌다 | p 47384 vs Fig 2a | **§11-3 격상 (SI↔그림 → 본문↔그림)** |
| **N2** | ⚠ **초록의 용어가 기구와 반대.** 초록 *"The metastable phases feature **higher packing efficiency**"* — α 는 "비전도 부피 분율"이고 준안정 edge 상은 α 가 **더 낮다**. 본문 p 47388 도 *"edge-sharing topology with high packing efficiency"* | 초록 · p 47388 | **인용 시 "낮은 α"로만 쓸 것** |
| **N3** | ⚠ **α 정의가 한 문단 안에서 자기모순.** *"quantifies proportion of the crystal volume occupied by structural features that **hinder** Li-ion mobility"* → 바로 다음 문장 *"This parameter represents the fraction of lattice space **available** for Li-ion transport"* (정반대). 세 번째 문장 *"lower α = larger effective migration space"* 는 첫 정의와 정합 | p 47388 | **§10c 의 "α 재구현 금지" 판정 보강** |
| **N4** | ⚠ **Fig 3 캡션 마커 오기** — 캡션 *"edge-sharing (orange **circles**)"*, 실제 그림·본문·Fig 5 캡션은 **orange squares**. 같은 캡션에 *"The **insects** depict…"* 오타 | Fig 3 캡션 | 소 (교정 품질 지표) |
| **N5** | 🔑 **CSM 은 D 를 따라가되 연결방식은 따라가지 않는다.** Fig 5b 재판독: 가장 왜곡된(흰색, CSM 5.5–6.0) 점들은 **corner rank 8·9·10** 이고, 이들은 Fig 3d 에서 **corner 중 유일하게 D≠0 인 셋**(0.64/0.22/0.14) | Fig 5b × Fig 3d | **§11-6 정정 + §10c CSM 채택 근거 강화** |
| **N6** | ⚠ **α 막대가 축 상한에서 잘린다** — Fig 5a rank 2(corner), Fig 5b rank 1(corner)·rank 7(mixed) 의 초록 막대가 **0.100 에서 클립**. 그 값들은 **판독 불가(≥0.100)** | Fig 5a,b | 종전 "mixed 가 α 최고" 는 **단정 불가**(rank 1 corner 도 같이 클립) |
| **N7** | 📐 **α 수치 정밀화** (700 dpi 재판독, Li₂SiS₃): **edge = 0.0753–0.0796**(최저는 rank 9) · **corner = 0.0834–≥0.100** | Fig 5a | 종전 0.0765–0.0805 / 0.084–0.100 → **분리 결론은 유지, 범위만 갱신** |
| **N8** | ⚠ **Fig 4f 의 수치 우연이 하나 더 있다** — Li₂SiS₃ edge 의 **dead volume 4.98 = SiS₄ 다면체 부피 4.98** 로 완전히 같고, 두 조성의 **Δdead 가 둘 다 정확히 0.69 Å³**. 독립 산출량 3개가 같은 값에 떨어진다 | Fig 4f | **V_dead 알고리즘 미공개 + 재현 불가 판정 유지** |

### 19c. 본문에만 있어 digest 에 없던 사실 4건 (추가)

| 항목 | 값 |
|---|---|
| **USPEX 집단 크기** | *"a population size of **100 per generation**"* (§2.1). §4b 의 "초기 집단 400" 은 **학습셋용 단일점 DFT 집합**으로 별개 — 두 숫자는 충돌이 아니다 |
| **spin 규약** | *"Spin-polarized calculations were performed for systems containing **3d transition metals**"* → 표적 4조성은 **비스핀**. **Q2 해소** (§11-9) |
| **ref 35 = GNoME** | Merchant et al., *Nature* **2023, 624, 80** — *"Google recently applied this approach to screen over **2.2 million** hypothetical structures"*. MLIP-CSP 정당화의 외부 앵커 |
| **ref 89** | Di Stefano et al., *"Superionic diffusion through frustrated energy landscape"*, **Chem 2019, 5, 2450** — 왜곡→평탄 지형 논거의 원전(refs 88,89). ⭐ **우리 SDCP 자리에너지 산포 언어와 같은 계열** |
| **300 K 자유에너지 (본문 문장)** | *"the Gibbs free energies at 300 K confirm that the representative corner-sharing structures remain thermodynamically more stable than the edge-sharing structures **for all compositions**"* → §11-10(교차온도 280–480 K)과 **정합**. 상온에서는 4조성 전부 corner 우세 |

### 19d. 재확인 통과 — 종전 판독이 맞았던 것

- **Fig 2a 14점 전부**(PBE −26 … +42, SCAN 5점) ✓ · **Fig 3b–e 의 D 마커·E_rel 보라막대 전부** ✓
  (Li₂SiS₃ rank 3/4/5/8/9 = 1.75/1.15/2.35/0.30/1.75; E_rel 0.003–0.018 등)
- **Fig 4f 8값 전부** (5.12/4.98 · 5.67/4.98 · 5.96·5.12/5.66·5.07 · 6.05/5.36) ✓
- **Fig 5a 연결방식 배정이 Fig 3b 와 완전 일치** (corner 1,2,6,7,10 / edge 3,4,5,8,9) ✓ — 두 그림 간 불일치 없음
- **핵심 인용문 6개** (*"at least 2 orders of magnitude"* · *"over 3 orders of magnitude"* · dead volume 정의 ·
  *"corner-sharing topologies act as bottlenecks"* · heteroelemental Si–Ge · *"most previous studies have
  overlooked these regions"*) **원문 그대로 확인** ✓
- **§9-A(σ 부재) 판정 유지** — 본문 11 pp 어디에도 σ 수치·단위(mS/cm, S/cm)가 **한 번도 등장하지 않는다** ✓
- 계산 파라미터: VASP 5.4.4 · PBE/PAW · k 간격 0.05 Å⁻¹ · 500 eV · 힘 <0.04 eV/Å · MTP 100:1:0.1 ·
  R_cut 5 Å · lev_max 20 · 세대 50→100→200→400 · melt-quench 4500 K 5 ps/2500 K 10 ps/200 K·ps⁻¹/500 K 4 ps ✓

> **총평**: 2026-07-28 digest 는 **수치 판독 정확도가 높다**(Fig 2a·3·4f 전수 일치). 이번 회차가 바꾼 것은
> **수치가 아니라 비판의 위치와 강도**다 — 모순 1건은 우리가 만든 것이었고(R1), 대신 **본문이 자기 그림을
> 부인하는 더 큰 모순(N1)** 과 **기술자 인과사슬이 끊기는 지점(N5)** 이 새로 드러났다.
