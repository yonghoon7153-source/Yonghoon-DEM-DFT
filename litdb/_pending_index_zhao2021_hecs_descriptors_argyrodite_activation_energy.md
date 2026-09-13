# ⏳ pending — `zhao2021_hecs_descriptors_argyrodite_activation_energy` 의 INDEX / comparison 반영분
> ✅ **① INDEX.md 병합 2026-09-13** (조율 세션). ⏳ **②③ `comparison_vs_ours.md` 블록은 미병합** — 절 번호 충돌(J-11/J-12)·기존 판정 개정 요청이 섞여 있어 큐레이터 판단이 필요하다.

> 2026-09-09, litdb-curator. **이번 세션은 `INDEX.md` · `comparison_vs_ours.md` 직접 수정 금지** 지시라
> 아래 블록만 만들어 둔다. **사람이(또는 조율 세션이) 그대로 옮겨 붙이면 된다.**
> digest 본체: `litdb/papers/zhao2021_hecs_descriptors_argyrodite_activation_energy.md`
> 그림: `litdb/figures/zhao2021_hecs_descriptors_argyrodite_activation_energy/` (**PNG 12장** = 본문 Fig 1–7 + Table 1 + SI Fig S1–S4)
>
> ✅ **서지 확인함 (추정 slug 가 맞았다)**: 표지 **Q. Zhao, M. Avdeev, L. Chen, S. Shi**,
> *Science Bulletin* **66** (2021) **1401–1408**, DOI `10.1016/j.scib.2021.04.029`.
> 접수 2021-02-28 / 수정 2021-03-22 / 수락 2021-04-12 / 온라인 2021-04-23. 교신 `sqshi@shu.edu.cn`.
> ⇒ slug `zhao2021_hecs_descriptors_argyrodite_activation_energy` **그대로 확정.**
> ⚠ **화면에 있던 "인용 126" 은 확인 못 했다** (오프라인). INDEX 행에 인용수를 넣지 않았다.
> ⚠ **OA 아님** — © Science China Press + Elsevier, All rights reserved. CC 라이선스 없음.
>
> ✅ **talk 역링크 점검함**: `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` →
> `litdb/talks/lee2026_skku_mlip_materials_design.md` 하나뿐이고, **이 논문은 그 대기열(6건: MTP/SevenNet/
> GNoME/cryoTEM/BH₄/hydrolysis 계열)에 없다.** ⇒ **역링크 작업 없음.**
>
> ✅ **`litdb/properties/` 디렉터리는 존재하지 않는다** ⇒ properties 갱신 대상 없음.
>
> ⚠ **`litdb/figures/_sources.json` 은 공유 파일이라 이 slug 항목 1개만 추가**했다 (도구가 append).
> SI 는 **docx** 라 `extract_figures.py` 가 못 먹는다 → `word/document.xml` 직접 파싱 + 실제 참조된
> 이미지 4개(rId6–9)만 `fig_S1..S4.png` 로 수동 등록. `figures.json` 에 `extracted_by` 로 표시했다.
> ⛔ **이 slug 에 `extract_figures.py --clean` 을 다시 돌리면 SI 4장이 지워진다** (SI 가 PDF 가 아니라서
> 도구가 재생성 못 한다). 재실행 시 SI 4장 수동 복구 필요.
>
> ✅ **크로핑 버그 2건 점검 결과: 이번 편에는 없다.** 2단 조판 혼입 없음(Fig. 3·4 만 1097 px 단단폭인데
> 원문에서 실제로 단단 그림), 캡션 위 판형 밀림 없음(8장 전부 그림 본체 온전). **쪽 좌표 재렌더 불필요.**

---

## ① `litdb/INDEX.md` — **`## ✅ Digest 완료 (paper-level)`** 표에 추가할 행

```markdown
| `papers/zhao2021_hecs_descriptors_argyrodite_activation_energy.md` **(본문+SI docx 통합)** | **[외부·argyrodite·⛔ DFT 0건 · ⛔물성 4축 비교 제외 · ★★★ descriptor 표현(representation) 1차 원전]** **Qian Zhao**/**Maxim Avdeev**(ANSTO·Sydney)/**Liquan Chen**(IOP-CAS)/**Siqi Shi\*** (Materials Genome Institute, **Shanghai Univ**), "**Machine learning prediction of activation energy in cubic Li-argyrodites with hierarchically encoding crystal structure-based (HECS) descriptors**" (***Science Bulletin* 66 (2021) 1401–1408**, DOI `10.1016/j.scib.2021.04.029`; 본문 8 pp + **SI docx**(Fig S1–S4 + Table S1–S2); **OA 아님**). **입방 Li-argyrodite 50종**(`Li₍₇₋ₓ₊ᵧ₎(M₍₁₋ᵧ₎NᵧY(1)₄)Y(2)₍₂₋ₓ₎Xₓ`, Y=S/Se · X=Cl/Br/I · M=P/As · N=Si/Ge/Sn · 0≤x≤2)의 Ea 를 **단위셀 CIF 만으로 뽑은 32개 HECS descriptor** → **PLS(4성분)** 로 회귀. **⛔⛔ 가장 중요한 사실: 라벨 50개가 전부 BVSE 다 — 실험 0 · DFT 0 · AIMD 0 · NEB 0** (본문 §2.1.1 *"instead of density functional theory method"*), BVSE 는 **SPSE 플랫폼**(ref [28] He *Sci Data* 2020, 7, 151, 공개웹 `matgen.nscc-gz.cn/solidElectrolyte/`) 내장이고 **R₀/b/voxel/percolation 차원 전부 미기재**. ML 은 **JMP**(상용). **★ descriptor 32개 전수(Table S2)**: 조성 7(r_anion·EN_anion·PL_anion·r_cation·EN_cation·PL_cation·C_Li) · 구조 8(a·v·V[LiACE₂]·V[BE₄]·D_Li-A/B/C/E) · 전도경로 6(BN_intra/doublet/inter·D_Li-Li intra/doublet/inter) · 이온분포 7(OCC_Li-48h/24g/all·Sconf_Li/A/C/anion) · 특수이온 4(r_A·EN_A·r_C·EN_C). **"계층적"=깊은 트리가 아니라 Global(셀: 조성·구조) ⊃ Local(케이지: 경로·이온분포·특수이온) 2층 × 5범주**(`Fig. 2b` 파란/빨간 박스). **★ 중요도는 SHAP·permutation 이 아니라 PLS 의 VIP**(컷 **0.8 = JMP 기본값**; 화학계량학 표준은 1.0) → 19개 채택. `figure-read ≈` 순위: **r_anion 1.50 ⭐1위** · D_Li-B 1.40 · D_Li-E 1.32 · a 1.29 · v 1.29 · r_C 1.29 · PL_anion 1.28 · EN_anion 1.22 · EN_A 1.17 · D_Li-C 1.15 · BN_intra 1.10 · V[BE₄] 1.06 · EN_C 1.05 · BN_inter 1.01 · r_A 0.99 · EN_cation 0.98 · Sconf_A 0.90 · Sconf_C 0.85 · Sconf_anion 0.81. **⭐⭐ 이 순위표의 진짜 정보 = Li 관련 8개가 전부 컷 아래**(C_Li 0.72 · OCC_Li-48h 0.73 · OCC_Li-24g 0.64 · OCC_Li 0.60 · Sconf_Li 0.73 · D_Li-Li ×3 0.60–0.73) — 논문은 *"Li 함량은 Ea 에 영향 적음"* 이라 물리로 읽지만 **실제로는 BVSE 라벨이 Li 를 못 보는 것**(`kb/concepts/bvse.md` §8 "빈 격자 정적 프로브"). ⇒ 자기 전략 ③(협동 Li⁺ 전도)에 `Fig. 7` 예시 칸이 **비어 있다**. **★★ 설계 추천 1번이 우리 modelc 족이다 — `Li₆₋ₓPS₅₋ₓCl₁₊ₓ` (< 0.322 eV)** (그 외 `Li₆₊ₓPS₅₊ₓBr₁₋ₓ` <0.273 · `Li₆₊ₓPS₅₊ₓBr₀.₂₅I₀.₇₅₋ₓ` <0.352 · `Li₆₊₍₅₋ₙ₎ᵧP₁₋ᵧNᵧS₅I` <0.420 · `…As₁₋ᵧNᵧS₅I` <0.371 · `…As₁₋ᵧNᵧSe₅I` <0.450). ⚠ **우리 추론**: 6개 상한이 **전부 Table S1 라벨 격자값과 정확 일치** ⇒ 모델 예측이 아니라 **모체의 BVSE 라벨**이고 **새 조성의 예측 Ea 숫자는 논문에 없다**. **⚠⚠ 우리가 Table S1 원자료로 잡은 오류·미공개 5건**: ① **시험 R² 0.820 은 논문 자신의 Eq.(5)(=1−SSE/SST)를 만족 안 한다 — 정정값 0.7661**, 0.820 은 **Pearson r²(0.8203)** 다(훈련은 0.8869 로 두 정의 일치해 안 걸렸다) ② **자기 LOOCV Q²=0.65877**(`Fig. S3` 캡션)을 성분수 선택에만 쓰고 **성능으로는 한 번도 안 쓴다** — 가장 방어 가능한 일반화 수치가 그것 ③ **라벨 50개가 전부 10/1024 = 0.009766 eV 격자 위**(예외 0)이고 **서로 다른 값이 18개뿐** = 사실상 18단계 순서형인데 미언급, RMSE 0.02 eV = 격자 2.4칸 ④ **`a`↔`v` 상관 = 1.00**(`Fig. S2`, 입방이라 v=a³)인데 둘 다 "중요 6개 구조 descriptor" 로 세었다 ⑤ **시험셋 10점이 0.244–0.371 eV 에만 있다**(고-Ea 4점은 전부 훈련) ⇒ 고Ea 구간 미검증. **⚠ 추가 비판 6건**: ⑥ **`Fig. 5d` 에 데이터 최소(0.2440 eV)보다 낮은 검은 보간 영역**이 넓게 있는데 본문은 바로 그 자리를 *"optimal combination of BN"* 근거로 쓴다(등고선은 모델 부분의존도가 아니라 **원자료 2D 투영 보간**) ⑦ **`Fig. 5e` 는 비단조**(Sconf_A≈16 에 고-Ea 붉은 띠)인데 본문은 *"positive effect of larger Sconf"* ⑧ **VIP 컷 1.0(표준)을 쓰면 Sconf 3인방이 전부 탈락** — 초록 헤드라인의 "site disorder" 절반이 JMP 기본값 0.8 에 의존 ⑨ **`Fig. 2a` M/N 범례 색이 뒤바뀜**(분홍=M 인데 Si/Ge 가 분홍; `Fig. 7` 은 올바름) + **Sn 미색칠** + **Table S2 #15 `D_Li-E` 를 "Wyckoff 4d" 라 적음**(본문은 E=16e) + **#23 설명문 깨짐** ⑩ **성분수 4를 훈련셋에서 골랐는지 전체 50에서 골랐는지 한 문장도 없다**(후자면 모델선택 누수) + 근접중복 누수(무작위 80/20, group-out 아님) ⑪ **재현 불가** — **50개 조성 목록이 논문 어디에도 없다**(Table S1 은 인덱스+Ea 3열, `Fig. 2a` 는 (x,y) 격자가 아니라 **원소 팔레트**), descriptor 값 행렬·BN/Sconf 계산식·반경/분극률 표·코드·시드 전부 없음, **Data/Code availability 문구 0건**. **🔑 우리 접점 3**: ① **★1 descriptor 재현 판정 — 32개 중 🟢13 즉시가능 / 🟡11 규약필요 / 🔴8 정의부재**(BN×3·Sconf×4·V[LiACE₂]), 즉 **VIP 상위 19개 중 6개가 정의 부재/표기 충돌** ② **★5 4a/4c/16e 자리 틀이 우리 O-모티프 실측과 1:1** — `O-distributed`(P–O 1.53–1.58 Å, 3/3 결합)=**E(16e)** → `V[BE₄]`·`D_Li-E` 를 움직이고, `O-bo4`(P–O 0/3, Li 1.82–2.05·Nd 2.19–2.26 Å 케이지)=**A(4a)/C(4c)** → `r_C`·`EN_C`·`Sconf_C` 를 움직인다 ⇒ **HECS 표현은 우리 두 모티프를 구분할 수 있다**(조성만 쓰는 descriptor 는 원리적으로 불가) ③ **★3 외삽 판정 — 조성식으로는 안, 1위 descriptor 축에서는 밖.** 그들 `r_anion` 축 `figure-read` **1.84–2.00 Å**(표본은 ≈1.855/1.89/1.97/2.01 **네 세로 줄무늬**, 사이는 전부 보간)인데 표준반경 재구성으로 **comp1 1.835 · modelc 1.832 · LPSOCl 1.762** ⇒ **경계 또는 바깥**, 그리고 **O·Nd·B 는 팔레트에 아예 없다**. ⛔⛔ **결정타: 이 모델의 타깃(BVSE)이 우리 조성축에서 이미 뒤집혀 있다** — `bvse_bvlain_ev_4sys.json` comp1 E_3D **0.2734 < modelc 0.4785** 인데 MLIP-MD 는 modelc **0.197±0.032 < comp1 0.2532** (**완전 역전**, `⚠_VERDICT_ranking_forbidden`, vacancy paradox). ⇒ **descriptor 표현은 빌리되 라벨은 반드시 우리 것(MLIP-MD Ea)으로 교체한다.** 그림 판독 **12장 중 10장**(`Fig. 1`–`Fig. 7` + `Fig. S2`·`S3`·`S4`; 안 본 것 = `Fig. S1` PLS 교과서 도식 · `Table 1` 은 PDF 텍스트로 읽음) | **★★★ cascade descriptor 표현(representation) 1차 원전 · ⛔ 물성 4축(A–D) 비교 제외 · ⛔ DFT 0건** — 우리 descriptor 집합 v0 초안(digest §13)의 근거 |
```

---

## ② `litdb/comparison_vs_ours.md` — **🔧 방법 원전 블록**에 추가 (⛔ 물성 4축 표 아님)

> **왜 4축 표가 아닌가**: 이 논문의 유일한 "물성값" 은 **조성이 특정되지 않은 BVSE 라벨 50개**다.
> σ·ESW·E_VRH·gap 은 **0건**이고, Ea 는 있지만 ⓐ 우리 축과 **다른 양**(정적 BVSE vs 동역학 MLIP-MD)이고
> ⓑ **어느 조성의 값인지 논문이 안 밝힌다**. 행을 만들면 전부 `n/a` 이거나 축이 어긋난다.
> ⇒ **J-7 과 같은 성격의 `🔧 방법 원전` 블록**으로 둔다. (번호는 조율 세션이 배정 — 아래는 `J-13` 가정)

```markdown
### J-13. 🔧 방법 원전 — **descriptor 표현(representation)** · argyrodite 전용 (2026-09-09 신설)

> ⛔ **A–D 물성 4축 표에 넣지 않는다.** σ·ESW·탄성·gap **0건**, Ea 는 **BVSE 라벨**이라 우리 MLIP-MD Ea 와
> 다른 양이고 조성 귀속조차 논문에 없다. 여기 있는 것은 **"argyrodite 를 무엇으로 기술할 것인가" 의 정의 원본**이다.
> 짝 블록: **J-11 `[Basu26MFB]`** = *예산을 어디에 쓰나(탐색)*, **여기 `[Zhao21HECS]`** = *무엇으로 기술하나(표현)*.

**[Zhao21HECS] `zhao2021_hecs_descriptors_argyrodite_activation_energy`** — Q. Zhao / M. Avdeev / L. Chen / **S. Shi\*** (Shanghai Univ MGI + ANSTO), *Sci. Bull.* **66**, 1401–1408 (2021), DOI `10.1016/j.scib.2021.04.029`. **입방 Li-argyrodite 50종 · 32 descriptor · PLS 4성분 · 라벨 = BVSE(SPSE)**. ⛔ DFT·AIMD·NEB·실험 **전부 0건**.

| 항목 | [Zhao21HECS] | 우리 (현행 / 계획) | 판정 |
|---|---|---|---|
| **표현 골격** | **Global(셀: 조성·구조) ⊃ Local(케이지: 전도경로·이온분포·특수이온)** 2층 × 5범주 → 32 스칼라 (`Fig. 1`·`Fig. 2b`) | cascade 는 **descriptor 를 하나도 안 정했다** (Codex BJ NO-GO 반려사유와 별개로 표현 자체가 공백) | ⭕⭕ **이식 후보 — 이 골격을 v0 로 채택 제안** (digest §13.2) |
| **argyrodite 자리 라벨** | **A=4a 음이온 · B=4b 양이온 · C=4c(=4d) 자유음이온 · E=16e (BE₄ 의 음이온) · Li=48h/24g** — 4a·4c 를 **`special ions` 독립 범주로 승격**(r_A·EN_A·r_C·EN_C, **4개 전부 VIP>0.8**, r_C 공동4위 1.29) | 우리 O-모티프 실측(`ndo_lpscl16_o_motif_estimand_2026_09_09.json` ⑨): **P–O 결합 3/3 = E(16e)** vs **P–O 0/3, Li/Nd 케이지 = A/C** | ⭕⭕ **1:1 대응 성립.** HECS 표현이 우리 두 O-모티프를 **구분할 수 있다** — 조성-only descriptor 는 불가 |
| **무질서 처리** | ⭐ **초격자를 안 만든다.** 부분점유 CIF 를 그대로 두고 **점유율·배위엔트로피 스칼라로 압축**(OCC×3, Sconf×4) | **실제 배열을 만든다** (단일배열 또는 disorder ensemble, 예: `comp2_disorder_ensemble` d=0.50 3config) | ⚠ **정반대 노선.** 섞으면 안 된다 — 배열마다 계산해 앙상블로 낼지, 점유율에서 직접 낼지 **보고량 카드에 먼저 못박아야** 한다 |
| **입력 구조** | **실험 정련 CIF** (본문 *"to preserve the experimentally determined structure information"*) | **DFT-이완 V0 셀** (comp1_V0_k444 등) | ⛔ **다른 축.** 같은 descriptor 라도 값이 다르다 ⇒ 논문 값과 직접 비교 금지 |
| **중요도 측정** | **PLS 의 VIP**, 컷 **0.8 (JMP 기본값)**. SHAP·permutation 아님 | (미정) | ⚠ **컷 1.0(표준)을 쓰면 Sconf 3인방이 탈락** — 헤드라인이 컷 선택에 걸려 있다. 우리가 쓸 땐 **컷을 결과 보기 전에** 정한다 |
| **다중공선성** | 심각 (`Fig. S2`: **a↔v = 1.00** · r_anion↔a/v ≈0.95 · r_anion↔D_Li-B ≈0.92) → 그래서 PLS 를 골랐다고 밝힘 | — | ⚠ **VIP 를 개별 descriptor 의 인과 기여로 읽으면 안 된다.** 상위 4개가 사실상 한 변수 |
| **BN(병목 크기) 정의** | 🔴 **계산식이 없다.** 논문 서사의 중심(전략 ①"broaden bottleneck size")인데 Table S2 는 이름만. 축 범위 `figure-read` intra ≈0.44–0.72 Å · inter ≈0.487–0.62 Å (Li⁺ 반경보다 작아 **여유반경**으로 보임 — 우리 해석) | **BVSE 채널 %** (above-min ≤ iso, 0.25 Å voxel, **원본 주기셀만**, `tools/comp1_v3/`) — **정의가 문서화돼 있다** | ⭕ **우리 쪽이 낫다.** BN 자리를 우리 채널% 로 대체 |
| **Sconf 정의** | 🔴 **식·단위 규약 없음.** `figure-read` 축 0–33 J/(K·mol) 인데 per site / per f.u. / per cell 불명 | (미정) | 🔴 **우리가 못박아야** — `−R Σ pᵢ ln pᵢ` × 자리당 원자수, 규약 기록 |
| **반경·EN·분극률 표** | 🟡 **어느 표인지 안 밝힘** ("Pauling EN" 만 명시) | (미정) | ⚠ 우리가 정하면 **논문 값과 절대 비교 불가** ⇒ 내부 일관성만 |
| **검증** | 80/20 hold-out **1회**(40/10) + LOOCV(성분수 선택용). **group-out 없음 · 반복분할 없음 · 외삽 검증 0건 · 시드 미기재** | 우리 실측: **쌍 LOOCV 0.0892 → LODO −0.1805 → L2DO −0.2548** (group-out 낙차 0.27) | ⛔ **우리가 앞선다.** 그들 0.82 는 무작위 분할값이고 group-out 이면 크게 내려갈 것으로 보아야 한다 |
| **보고 성능** | R² 훈련 0.887 / 시험 **0.820** · RMSE 0.02 eV | — | ⛔ **시험 0.820 은 논문 자신의 Eq.(5) 정의를 안 지킨다 — 정정 0.7661** (0.820 = Pearson r²). **자기 LOOCV Q² = 0.65877** 이 가장 정직한 값인데 성능으로 안 쓴다 |
| **라벨** | **BVSE (SPSE)** — 파라미터 전부 미기재 | **MLIP-MD Ea** (UMA-s-1p1, 600/800/1000 K, MSD 2–50 ps) + 별도 **BVSE(bvlain)** | ⛔⛔ **여기가 결정적 결렬점** — 아래 |

**⛔⛔ 결정타 — 이 논문의 타깃이 우리 조성축에서 이미 뒤집혀 있다**

| 계 | BVSE(bvlain) E_3D | MLIP-MD Ea | 방향 |
|---|---|---|---|
| comp1 `Li₆PS₅Cl` | **0.2734 eV** | 0.2532 eV (단일시드) | |
| modelc `Li₅.₄PS₄.₄Cl₁.₆` | **0.4785 eV** | 0.197 ± 0.032 eV (3시드) | **완전 역전** |

출처 `db/properties/bvse_bvlain_ev_4sys.json` · **`⚠_VERDICT_ranking_forbidden`**: *"가족 내 랭킹은 MD와 역전 … vacancy paradox(점유-무관 지도)가 eV 단위에서도 그대로 재현된 것. → σ/Ea 순위 인용 금지."* 그리고 `kb/concepts/bvse.md` §9: **comp1→modelc 는 "채널부피 −15 % 인데 σ ×4 ↑"** 이고 원인은 **vacancy/무질서 = 점유-무관 지도의 원리적 사각**.
⇒ Zhao 의 VIP 가 **Li 관련 8개를 전부 컷 아래로 떨어뜨린 것**은 물리 발견이 아니라 **이 사각의 지문**이다.
⇒ **판정: descriptor 표현은 채택 후보, 라벨(BVSE)과 학습된 모델은 우리 Cl-rich 랭킹에 사용 금지.**

**⭕ 유일하게 방법론적으로 정당한 숫자 대조 — BVSE ↔ BVSE**
우리 comp1 BVSE E_3D **0.2734 eV** vs 이 논문 Li₆PS₅Cl BVSE **≈0.322 eV**(⚠ **우리 추론** — `Fig. 7` 상한 0.322 가 Table S1 라벨 격자값 0.322265625 와 정확 일치). 차이 **≈49 meV**. ⚠ 코드(bvlain vs SPSE)·파라미터·구조(DFT-이완 vs 실험정련)·percolation 차원 정의가 전부 달라 **"같은 자릿수" 까지만**. ⛔ 이 값을 우리 MLIP-MD Ea 와 같은 표에 넣지 않는다.

**★ 설계 추천이 우리 조성족을 이름 그대로 지목한다**
`Fig. 7` 전략 ①"작은 음이온 치환" 의 1번 예시가 **`Li₆₋ₓPS₅₋ₓCl₁₊ₓ` (Ea < 0.322 eV)** — 우리 modelc `Li₅.₄PS₄.₄Cl₁.₆` 와 **같은 족**이다. ⚠ 단 **예측 Ea 숫자는 논문에 없고**(상한은 모체 라벨값), **`r_anion` 축에서 우리 조성이 그들 훈련 범위 왼쪽 경계 밖**이다(digest §7.1) ⇒ **"문헌이 우리 조성을 유망하다고 예측했다" 는 문장은 쓸 수 없다.** 쓸 수 있는 것은 *"같은 설계 방향(Cl 증가 → r_anion 감소)을 독립적으로 제안한다"* 까지.
```

---

## ③ 축 J 안의 상호참조 (INDEX 행과 함께 반영)

- **J-9 `[Cho25AL]`·`[Ma25AL]`** = 능동학습 루프 — **오라클(라벨)을 어떻게 고르나**
- **J-10 `[Jain26Rev]`** = 깔때기 모양 — **무엇을 어떤 순서로 자르나** (⚠ 리뷰라 2차 인용)
- **J-11 `[Basu26MFB]`** = 각 단의 판정 계약 + fidelity 전환 규칙 (⚠ preprint·단독저자)
- **J-13 `[Zhao21HECS]`(이 편)** = ⭐ **표현(representation) — 후보를 무엇으로 기술하나.**
  argyrodite 전용 descriptor 목록으로는 **우리 corpus 유일**이고, **자리(4a/4b/4c/16e/48h) 분해**가 있는 것도 이것뿐이다.
  ⚠ 단 **DFT 0건 · 라벨이 BVSE · 재현 불가** — "원전" 은 *표현*에 한정된다.

**확보 후보 (이 논문의 참고문헌, 우리 미보유)**

| ref | 서지 | 왜 필요한가 |
|---|---|---|
| **[28]** | He B, Chi S, Ye A, et al., **"High-throughput screening platform for solid electrolytes combining hierarchical ion transport prediction algorithms"**, *Sci. Data* **7**, 151 (2020) | ⭐⭐ **이 논문 라벨 50개 전부의 출처.** BVSE 설정(R₀·b·voxel·percolation 정의)이 여기 있을 가능성이 높다 — Zhao 본문에는 **하나도 없다**. 공개 웹 `matgen.nscc-gz.cn/solidElectrolyte/` |
| **[30]** | Farrés M, Platikanov S, Tsakovski S, et al., **"Comparison of the variable importance in projection (VIP) and of the selectivity ratio (SR) methods"**, *J. Chemometr.* **29**, 528 (2015) | VIP 컷오프(0.8 vs 1.0)와 상관군 안 중요도 분배의 규범 문헌. 우리가 VIP 를 쓸 거면 **컷을 결과 전에 정하는** 근거로 필요 |
| **[38]** | Wang Z, Shao G, **"Theoretical design of solid electrolytes with superb ionic conductivity: alloying effect on Li⁺ transportation in cubic Li₆PA₅X chalcogenides"**, *J. Mater. Chem. A* **5**, 21846 (2017) | argyrodite 합금화의 **계산(DFT) 축** — Zhao 가 BVSE 로만 다룬 같은 조성공간을 DFT 로 본 편 |

**이미 보유한 인용 관계 (역링크만 걸면 됨)**

| ref | 우리 digest |
|---|---|
| [20] Fujimura 2013 | `papers/fujimura2013_ml_conductivity_origin.md` |
| [25] Sendek 2017 | `papers/sendek2017_ml_screening_12k_conductors.md` (⭐ 소표본 방어 절차는 Sendek 이 우월 — Zhao 는 X-randomization·부트스트랩 **0건**) |
| [34] Deiseroth 2008 | (미보유 — argyrodite 원전) |
| [35] Kraft 2017 | `papers/kraft2017_lattice_polarizability_argyrodite_Li6PS5X.md` (⭐ `PL_anion` descriptor 의 물리 근거) |
