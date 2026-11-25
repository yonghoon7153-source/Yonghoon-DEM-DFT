# Machine Learning-Assisted Crystal Structure Prediction of Solid-State Electrolytes Reveals Superior Ionic Conductivity in Metastable Edge-Sharing Phases — Ji Hoon Kim (JACS 2025)

> 🎤 **5분 발표 대본 + Figure별 예상 Q&A**: `litdb/papers/kim2025_csp_metastable_edge_sharing_sse__seminar_5min_qa.md` (2026-08-28, 발표용 — 수치 검증은 이 digest 가 정본)

> slug `kim2025_csp_metastable_edge_sharing_sse` · DOI `10.1021/jacs.5c15665` · type `CSP(USPEX+MTP active learning) + DFT + AIMD` ·
> *J. Am. Chem. Soc.* **2025, 147, 47381–47391** · 투고 2025-09-07 / 수정 2025-12-05 / 수리 2025-12-08 / 게재 2025-12-12 ·
> 본문 11 pp + SI 24 pp · digested 2026-07-28 · status ✅ (본문 + SI 전수 정독, Fig 2/3/4/5·S1–S12·Table S1–S2 전부 판독)
> · **2026-08-04 본문(11 pp) 실물 독립 검증 완료 — §19** (자기철회 2건 · 신규 적발 8건 · Q2 해소)
> · **2026-08-04 SI(24 pp) 실물 독립 검증 완료 — §20** (자기철회/정정 3건 · 신규 적발 21건 ·
>   Fig S1–S12 + Table S1–S2 전수 재판독 300–900 dpi · **MSD 원자료 40궤적 전수 전사**. ⚠ 본문 실물은 이번 회차에 없음 → §19 승계)
> · **2026-08-26 저자 데이터저장소(CSP_SSE) 실측 — §21** (MTP 학습셋 실측으로 **Q6 부분 종결** ·
>   AIMD 셀 규약 **~10 Å** 확보로 §11-9 부분 종결 · **`dynamics_Li_CSM.py` = T14 참조구현 확정** ·
>   **배포 CIF 40개 연결방식 독립 검증 36/40** → **Q9·Q10 신설**. ⛔ upstream LICENSE 없음 = 내부 전용)
> · **2026-08-26 `## 0.1 문단별 읽기 동반자` 신설** — 논문세미나용. 본문 11 pp 를 **초록·서론·방법·결과·결론
>   전 문단**(30항목) 단위로 "무슨 말인가 / 논증에서 무슨 역할인가 / 막히는 용어 / 우리가 아는 문제"로 안내.
>   SI 는 절 단위 + **본문이 SI 를 가리키는 지점마다 → 표시**.
>
> 🎤 **관련 발표**: `talks/lee2026_skku_mlip_materials_design.md` §14 (슬 **26–29**) ·
> ⛔ **그 talk 은 citable=no — 이 논문이 정본이고, 덱/구술과 어긋나면 이 논문이 이긴다.**
> (선례: 이 digest 가 덱의 `10⁻⁴ → 2.4 mS/cm` 를 부인해 인용금지가 생겼다 — §9-A.)
>
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


> elements: Al, Au, B, Ba, Bi, Br, Cl, Ga, Ge, Li, Mn, Na, O, P, Pt, S, Se, Si, Sn, Y
> methods: DFT, AIMD, MD, MLIP, phonon

<!-- 🔧 2026-08-26 태그 정정: 종전 methods 줄은 `bader, bvse, cohp, dos, elf, esw, neb, pdos …` 를
     달고 있었으나 이 논문은 그 중 **어느 것도 하지 않는다** (§13 "⛔ 없는 것" 참조 — NEB·Bader·
     COHP/ICOHP·DOS/PDOS·ELF·ESW·탄성 전부 부재). digest 본문이 "안 한다"고 적은 단어를 태그가
     긁어 간 것으로 보이며, 그대로 두면 Glossary 의 NEB/Bader/COHP/ELF/ESW 페이지에 이 논문이
     **잘못 링크된다.** 실제로 하는 것만 남겼다: DFT(PBE/PAW) · AIMD(NVT) · MD(LAMMPS+MTP) ·
     MLIP(MTP) · phonon(phonopy G(T)).
     elements 는 검증 14종에서 빠져 있던 **Ba**(LiBaGe₂)·**Ga**(LiGa(SeO₃)₂)를 추가. -->


---

## 0.1 문단별 읽기 동반자 (논문세미나용) — 2026-08-26 신설

> **쓰는 법**: 논문(본문 11 pp)을 옆에 펴 놓고, 지금 읽는 문단을 여기서 찾는다.
> 각 항목은 **쪽 번호 + 단(좌/우) + 첫 5–8단어**로 위치를 특정했다.
> ⚠ 줄은 **§9·§11·§19·§20·§21 에서 이미 확정된 판정**만 옮긴 것이다 — 새 추측은 넣지 않았다.
> ⚠ 줄이 없는 문단은 **우리가 아는 문제가 없다**는 뜻이다.
> 그림은 `litdb/figures/kim2025_csp_metastable_edge_sharing_sse/` 에 크로핑돼 있다.

### 읽는 순서 제안 — 1쪽부터 읽지 마라

**11 pp 를 앞에서부터 읽으면 논증이 제일 늦게 잡힌다.** 이 논문은 사실상 **그림 한 장(Fig. 3b–e)을
설명하는 글**이고, 서론·방법은 그 그림을 정당화하는 장치다. 세미나 발표자라면 이 순서를 권한다.

1. **Fig. 3b–e 부터 본다** (p.47385 상단, 그림). 축이 둘이다 — 마커 높이 = D_600K, 보라 막대 =
   E_rel, x = 안정성 순위. 마커 모양 3종(파란 원 corner / **주황 사각** edge / 초록 삼각 mixed)만
   읽으면 **논문의 결론이 여기서 끝난다**: 왼쪽(안정)이 바닥에 붙어 있고 오른쪽(준안정)이 떠 있다.
2. **초록** (p.47381). 단 *"higher packing efficiency"* 는 **함정**이다 — 본문은 정반대로
   *"lower α"* 라고 쓴다(§19-N2). 초록만 인용하면 뒤집힌다.
3. **§3.2 ¶5** (p.47386 좌단 하단 → 우단). 이 논문에서 **제일 많이 인용될 두 문장**이 여기 한
   문단에 같이 있다 — *"at least 2 orders of magnitude"*(자기 계산)와 *"over 3 orders of
   magnitude"*(**ref 36 Huang 의 실험 소환**). 둘을 섞으면 덱 오류가 재발한다(§9-A).
4. **§3.3 전체** (p.47387 우단 → p.47388). 기구가 여기서 **dead volume → α → Li–S₄ 부피 → CSM**
   순서로 쌓인다. **Fig. 4d · Fig. 4e · Fig. 5 를 옆에 펴 놓고** 읽어야 따라간다.
5. **§3.1 + Fig. 2** (p.47384). 검증. 여기서 🔴 SCAN 문장을 만난다. **발표에서 질문이 나온다면
   십중팔구 이 자리다** — 미리 §11-3 을 읽어 두라.
6. **§2 방법** (p.47382 우단 → p.47384 좌단). **결론을 알고 나서 읽어야** 어떤 파라미터가 결론을
   떠받치는지 보인다. 특히 §2.3 의 **종료 조건**(실험 구조를 맞히면 종료 / 없으면 400세대 소진).
7. **§1 서론 · §4 결론** (p.47381–82, p.47389). 마지막에 읽는다. 서론은 3–6 을 읽고 나면 5분이면
   되고, 결론은 §3.3 의 재진술이라 **새 정보가 0** 이다.
8. **SI 24 pp 는 전부 읽지 말고 세 곳만**: ① **eq 5–8**(MSD 정의식이 틀렸다, §20-M1)
   ② **Fig. S4–S7**(MSD 원자료 40개 — 이 논문 D 의 절반이 확산이 아니라는 증거, §20d)
   ③ **SI p 4 의 SCAN 자백 문장**(본문과 정반대로 적혀 있다, §20-M0).

---

### 초록 (p.47381 전폭, "Significant attention has been devoted to developing…")
- **뭐라고 하나**: 조성 치환에만 매달려 온 SSE 연구에 **구조 자체를 바꾸는 축**을 넣자 — MTP 기반
  CSP 로 12개 실험 구조를 재현하고, 4조성에서 **준안정 edge-sharing 상이 안정 corner-sharing 상보다
  Li 이동도가 우수**함을 보였다.
- **왜 여기 있나**: 논문 전체의 축약. **초록에만 있는 표현이 둘** 있으니 조심 — *"higher packing
  efficiency"* 와 *"This superior conductivity"*.
- **막히는 말**: **SSE**(solid-state electrolyte) · **ASSB**(all-solid-state battery) ·
  **CSP** → §17 · **MTP** → §17 · **packing ratio / Li–S₄ 부격자 / CSM** → §17.
- ⚠ **우리가 아는 문제 (2건)**:
  ① *"The metastable phases feature **higher packing efficiency**"* — α 는 **비전도 부피 분율**이고
  준안정 edge 상은 α 가 **더 낮다**. 표준 결정학의 "채움률"과 방향이 반대라 **그대로 옮기면
  주장이 뒤집힌다**(§19-N2, §16 인용규칙). **"낮은 α"로만 쓴다.**
  ② *"This superior **conductivity**"* — 논문은 **σ 를 한 번도 계산하지 않는다**. 잰 것은
  **D_600K** 뿐이다(§9-A, §11-1). 인용할 때 "확산계수 기준"을 반드시 붙인다.

---

### §1 ¶1 (p.47381 좌단, "To pursue safer and more energy-dense lithium-ion batteries…")
- **뭐라고 하나**: ASSB 가 왜 필요한가(안전·에너지밀도) → SSE 요구조건(이온전도·전기화학안정·계면정합)
  → 지금까지는 Li₆PS₅Cl·Li₇P₃S₁₁·Li₃PS₄·LGPS 에 **치환/도핑**만 해 왔다 → 그건 **바닥 결정구조를
  바꾸지 못한다** → 더 근본적인 전략이 필요하다.
- **왜 여기 있나**: **이 논문의 적(敵)을 정의하는 문단.** "조성 최적화"를 한계로 규정해야 CSP 가
  정당해진다. 앞 문단이 없으니 여기가 논증의 출발점이다.
- **막히는 말**: **argyrodite**(Li₆PS₅Cl 계열의 구조 이름) · **LGPS**(Li₁₀GeP₂S₁₂).
- ⚠ **우리가 아는 문제**: 이 문단이 한계로 지목하는 *"elemental substitution or doping with base
  materials such as **Li₆PS₅Cl**"* 가 **정확히 우리 문제설정**이다(§10a). 이 논문은 우리와 같은
  질문을 푸는 게 아니라 **우리 질문을 넘어서겠다고 선언**하는 것 — 세미나에서 이 대비를 먼저
  못 박아야 뒤가 편하다.

### §1 ¶2 (p.47381 우단, "With advancements in experimental synthesis techniques and instrumentation…")
- **뭐라고 하나**: ICSD 20만 개 + MP/OQMD/AFLOW 가 쌓였지만 **아직 안 나온 구조가 많다**(실험 발견은
  시행착오라서). CSP 는 조성에서 구조로 가는 길이고, 특히 **phase-diagram-guided CSP** 가 유망하다.
- **왜 여기 있나**: ¶1 이 "치환은 부족하다"였다면 여기는 **"DB 도 부족하다"**. 두 문단이 합쳐져
  "그러니 새로 만들어야 한다"가 된다. 깔때기의 입구를 넓히는 논증(→ §0.5).
- **막히는 말**: **ICSD/MP/OQMD/AFLOW** — 각각 실험 DB / 계산 DB 3종. **phase-diagram-guided CSP**
  = 상도(phase diagram)에서 "말이 되는 조성"을 먼저 고르고 그 조성에만 CSP 를 돌리는 것.
- ⚠ **우리가 아는 문제**: *"phase-diagram-guided"* 의 실체는 **MP 상도에서 tie-line 위 1:1 점을
  고른 것**이 전부다(§6). 방법론적 신규성이 아니라 **조성 선택의 정당화 장치**다. 그리고 그 근거
  그림(Fig. S2)은 **진짜 4원계 convex-hull 단면이 아니다**(§20-M23) — 삼각형 꼭짓점이 Ge–S–Li 인데
  Si 계 상들이 그 위에 겹쳐 찍혀 있다.

### §1 ¶3 (p.47382 좌단, "While theoretical CSP based on density functional theory (DFT)…")
- **뭐라고 하나**: DFT-CSP(입자군집·유전알고리즘·랜덤탐색)는 되긴 하는데 **비싸다** → MLIP 를
  붙이면 DFT 정확도를 싼값에 얻는다 → 예: Google 이 **220만 구조**를 훑었다.
- **왜 여기 있나**: 방법의 정당화. "왜 MLIP 를 쓰나"에 대한 답이고, **ref 35 = GNoME**(Merchant,
  *Nature* 2023, 624, 80)이 외부 앵커다(§19c).
- **막히는 말**: **particle swarm optimization**(CALYPSO 계열) · **random structure search**(AIRSS 계열)
  · **genetic algorithm**(USPEX 계열) — CSP 탐색 알고리즘 3대 계보. **MLIP** = machine-learned
  interatomic potential.
- 📎 **우리 쪽 참고**: GNoME 원문은 `litdb/inbox/70. Merchant2023_GNoME_…pdf` 로 이미 들어와 있다.

### §1 ¶4 (p.47382 좌단, "To validate the proposed MLIP-assisted CSP framework, we applied it to 14…")
- **뭐라고 하나**: 14종 기지구조로 검증해 **12종 성공** → 4조성에 적용해 각 10개 저에너지 폴리모프를
  얻고 **corner / edge / mixed** 로 분류 → 특히 **Li₂SiS₃ 의 준안정 edge 상**(Kanno 그룹이 변형
  합성조건에서 얻었고 σ 가 3자릿수 높은 그것)을 맞혔다.
- **왜 여기 있나**: **논문의 신뢰성 담보 문단.** "우리가 아는 것을 맞혔으니 모르는 것도 믿어라"는
  구조다. Li₂SiS₃ 를 주 조성으로 고른 이유가 여기서 이미 드러난다(→ §6).
- **막히는 말**: **폴리모프(polymorph)** = 조성이 같은데 구조가 다른 상. **준안정(metastable)** → §0.5.
- ⚠ **우리가 아는 문제 (2건)**:
  ① **"12 of 14" 는 관대한 판정**이다 — Li₃YCl₆ 는 참조 P-3m1 → 예측 **P1**(대칭이 완전히 깨진 것)인데
  "일치"에 들어간다(§5d). 인용할 때 이 관대함을 같이 적는다.
  ② *"approximately **3 orders of magnitude**"* 는 **이 논문의 측정이 아니라 ref 36(Huang, JACS 2022,
  144, 4989) 소환**이다(§9-A). 서론에서 이미 남의 숫자를 끌어다 쓰고 있다는 것을 표시해 두라.

### §1 ¶5 (p.47382 좌단 하단 → 우단 상단, "To evaluate the impact of discovered structural motifs on Li-ion transport…")
- **뭐라고 하나**: AIMD 를 돌려 보니 **안정 상은 corner 이고 확산이 낮았고, 준안정 edge 상이 빨랐다**
  → 그 원인을 **Li 접근가능 부피(packing efficiency)** 와 **Li–S₄ 부격자의 동적 왜곡**으로 설명한다.
- **왜 여기 있나**: **서론의 로드맵 문단** = 결과 전체의 예고편. 여기 나오는 두 개념이 §3.3 의 뼈대다.
- **막히는 말**: **AIMD**(ab initio MD — 힘을 DFT 로 계산하는 MD. 우리 UMA-MD 와 **힘 계산 축이 다르다**,
  §14) · **동적 왜곡(dynamic distortion)** = 정적 구조가 아니라 **MD 궤적 평균**으로 재는 왜곡.
- ⚠ **우리가 아는 문제**: 여기서도 *"packing efficiency—defined as the fraction of the unit cell
  volume occupied by **nonconductive** volume"* 라고 **정의는 옳게** 써 놓고, 초록에서는 방향을
  뒤집어 쓴다(§19-N2). **같은 논문 안에서 같은 양의 방향이 흔들린다** — 이게 §11 의 반복 주제다.

---

### §2.1 (p.47382 우단 → p.47383 좌단 상단, "All DFT calculations and molecular dynamics simulations were performed…")
- **뭐라고 하나**: 계산 설정 전부. **VASP 5.4.4 + LAMMPS**, **PAW + PBE(GGA)**, k-mesh **0.05 Å⁻¹ 간격**
  Monkhorst–Pack, cutoff **500 eV**, 힘 **<0.04 eV/Å**, **3d 전이금속 계만 스핀 분극**, AIMD 는
  **NVT + Nosé–Hoover**(셀·스핀·시간간격·온도는 **선행 연구 refs 46–49 승계**), USPEX **집단 100/세대**,
  자손 연산 heredity/permutation/soft mutation/lattice mutation + **antiseed**, MTP 하이퍼파라미터
  **w_e:w_f:w_s = 100:1:0.1**, **R_cut = 5 Å**, **lev_max = 20**.
- **왜 여기 있나**: 이 논문 전체에서 **재현에 필요한 숫자가 모여 있는 유일한 문단.** 세미나에서
  "그래서 뭘로 돌렸냐"는 질문의 답이 전부 여기 한 문단이다.
- **막히는 말**: **PAW**(projector augmented wave — 핵 근처를 부드럽게 처리하는 전자구조 기법) ·
  **Monkhorst–Pack**(역격자 k-점을 균일 격자로 뿌리는 표준 방식; "0.05 Å⁻¹ 간격"은 셀이 커지면
  자동으로 k 를 줄인다는 뜻) · **NVT / Nosé–Hoover**(입자수·부피·온도를 고정하는 앙상블과 그
  온도조절기) · **antiseed / soft mutation / lev_max** → §17.
- ⚠ **우리가 아는 문제 (3건)**:
  ① *"Based on our previous work, we used the same computational guidelines … including **cell size,
  spin, time step**"* — **AIMD 의 핵심 파라미터를 본문에 안 적고 refs 46–49 로 떠넘긴다**(§11-9).
  ref 47 = `papers/jun2022_argyrodite_ion_cage_size_descriptor.md` 를 봐야 실제 값이 나온다
  (**dt 2 fs · Γ-only · 단위셀 ~52원자 · 배열×온도당 ≥3 시드**). 🆕 **셀 크기는 2026-08-26 에
  데이터저장소로 부분 종결** — *"supercell … lattice dimension as close as possible to **~10 Å**"*(§21c).
  ② **스핀은 이 문장으로 해소된다** — 표적 4조성(Li–Si/Ge/Sn–S)에는 3d 전이금속이 없으니 **비스핀**.
  검증 14종 중 스핀 대상은 **LiMn₂O₄ 하나뿐**이다(§19c, Q2 종결).
  ③ **"집단 100/세대"와 §2.2 의 "초기 집단 400" 은 충돌이 아니다** — 앞은 USPEX 세대 크기, 뒤는
  **학습셋용 단일점 DFT 집합**이다(§19c). 세미나에서 자주 헷갈리는 지점.
- → **SI 로 넘어가는 곳**: 문단 끝 *"Further details of the MTP are provided in Supporting
  Information"* → **SI eq 1–4**(MTP 기저 정의). 실제 학습된 퍼텐셜의 헤더는 **§21b 에 실측**해 뒀다.

### §2.2 ¶1 (p.47383 좌단, "Figure 1 illustrates the workflow of CSP with MTP, which consists of three main stages…")
- **뭐라고 하나**: 워크플로는 3단(초기 학습셋 → CSP 루프 → 최종 예측). 새 구조를 찾는 게 목적이라
  **기존 DB 를 학습셋으로 못 쓴다**(데이터 기근) → 그래서 **amorphous** 를 만든다:
  **4500 K 5 ps 가열 → 2500 K 10 ps 융해 → 200 K/ps 로 300 K 급랭 → 500 K 4 ps 어닐**.
- **왜 여기 있나**: **"학습 데이터를 어디서 구하나"** 라는, MLIP-CSP 의 진짜 병목에 대한 답의 전반부.
- **막히는 말**: **PES**(potential energy surface — 원자 배치마다의 에너지 지형) ·
  **melt-quench-anneal** → §17. **데이터 기근(data scarcity)** = 아직 존재하지 않는 구조라 라벨이 없다.
- 📎 **Fig. 1 을 여기서 본다**: 좌상단 "Initial structures" 상자가 이 문단이다. 참고로 그림 안의
  MTP–DFT 산점도는 표적 4조성이 아니라 **검증 조성 Li₃AuO₃** 의 것이다(범례 Initial/50/100/200 Gen).

### §2.2 ¶2 (p.47383 우단, "Although these structures provide a broad coverage of the potential energy surface (PES)…")
- **뭐라고 하나**: melt-quench 만으로는 **"정확한 구조 완화에 필요한 영역이 학습이 안 된 채 남는다"**
  → 그래서 USPEX **초기 집단 400 구조**를 단일점 DFT 로 계산해 학습셋에 섞는다.
- **왜 여기 있나**: ¶1 의 약점을 스스로 지적하고 메우는 문단. **두 갈래(amorphous + random)를 합치는
  설계**의 근거가 여기다.
- **막히는 말**: **single-point DFT** = 구조를 움직이지 않고 그 배치의 에너지·힘·응력만 한 번 계산.
- 🔑 **우리 쪽 접점**: *"may still leave untrained regions that are insufficient for accurate
  structural relaxation"* — 이 진단은 **우리 T1(UMA 외삽 등급)과 같은 문제의식**이다(§4b). "사전학습
  모델이 우리가 실제로 지나가는 영역을 덮었나"를 묻는 것. 세미나에서 우리 얘기로 넘어가기 가장
  좋은 다리다.

### §2.3 ¶1 (p.47383 우단, "Based on the combined training data set, we conducted an iterative CSP loop comprising four major steps…")
- **뭐라고 하나**: 루프 4단계 = **MTP 학습·평가 → USPEX 구조생성 + MTP 완화 → active learning →
  query DFT**. 초기에는 **50세대**로 돌린다. 다만 초기 학습셋이 amorphous+random 뿐이라 **전역최소
  근처를 정확히 완화하지 못한다** → 그래서 세대마다 나온 새 구조를 학습에 넣어야 한다 → 그런데
  DFT 라벨 만들기가 병목이다.
- **왜 여기 있나**: **문제 제기 문단.** 다음 문단의 active learning 을 도입하기 위한 무대 설치다.
- **막히는 말**: **완화(relaxation)** = 힘이 0 이 될 때까지 원자·격자를 움직이는 것.
  **전역최소(global minimum)** = 그 조성에서 에너지가 가장 낮은 구조.
- 📎 **Fig. 1 하단 "CSP loop" 사각형**이 정확히 이 4단계다.

### §2.3 ¶2 (p.47383 우단 하단 → p.47384 좌단 상단, "To mitigate this issue, we adopted an active learning approach…")
- **뭐라고 하나**: 불확실도가 큰 구조(**query structure**)만 골라 **완전 완화 + 단일점 DFT** 를 돌려
  학습셋에 넣는다 → 세대 수를 **100 → 200 → 400** 으로 올린다 → 종료 조건은
  **(a) 실험 보고 구조를 루프 안에서 예측하면 종료**, **(b) 실험 구조가 없으면 400세대 소진**.
  검증은 **공간군 비교 + RDF 비교**.
- **왜 여기 있나**: **비용 문제의 해법 문단** = MLIP-CSP 가 실용적이 된 이유. §0.5 의 3문단이 여기 대응.
- **막히는 말**: **active learning / query structure** → §17. **불확실도(uncertainty)** = MTP 가
  "이 구조는 내 학습 범위 밖"이라고 스스로 판단하는 지표(MLIP 패키지의 extrapolation grade).
  **공간군(space group)** = 결정의 대칭을 분류한 230개 유형.
- ⚠ **우리가 아는 문제 (2건)**:
  ① **DFT query 총 횟수도 최종 학습셋 크기도 보고하지 않는다**(§4c). 이 논문에서 **"active learning
  이 비용을 얼마나 아꼈나"를 검증할 방법이 없다.** 🆕 **2026-08-26 데이터저장소 실측으로 종결** —
  학습셋은 **863 / 1,391 / 1,038 / 1,104 배열**이다(§21b). 예상보다 **작다**.
  ② **종료 조건 (a)/(b) 가 조성별로 다르게 걸렸다** — Fig. S3 범례를 보면 **Li₂SiS₃ 만 200 Gen 까지**
  있고 나머지 3조성은 400 Gen 이 있다(§20-M19). 즉 **Li₂SiS₃ 는 조기 종료(맞혔으니까), 나머지 3조성은
  수렴 확인 없이 400세대를 소진하고 끝났다.** "400세대면 충분하다"는 근거는 논문에 없다.

### §2.4 (p.47384 좌단, "With the fine-tuned MTP integrated into the CSP workflow, the final round…")
- **뭐라고 하나**: 미세조정된 MTP 로 **400세대 초과** 전면 탐색을 한 번 더. 실험 참조가 있으면
  공간군·RDF 로 대조하고, **없으면 DFT 안정성 계산으로 최종 랭킹**을 매긴다.
- **왜 여기 있나**: 루프의 출구. **"최종 순위는 MTP 가 아니라 DFT 가 매긴다"** 는 이 한 문장이
  §11-4 의 비판을 반쯤 막아 준다 — 세미나에서 반드시 짚어야 할 방어선이다.
- ⚠ **우리가 아는 문제**: 그래도 **어떤 구조가 DFT 까지 올라오느냐는 MTP 가 정한다.** MTP 의
  저에너지 영역 오차(MAE_f)가 **13.2 / 27.4 / 29.8 / 33.3 meV/atom** 인데 판별 대상인 E_hull 전 범위가
  **0–42 meV/atom** 이다 — **놓친 저에너지 상이 있을 가능성은 정량화되지 않았다**(§11-4).

---

### §3.1 ¶1 (p.47384 좌단, "Although previous studies have combined USPEX with MTP for CSP, their efforts primarily focused on unary or binary…")
- **뭐라고 하나**: 선행 USPEX+MTP 연구는 **1원계·2원계나 고압 조건**에 머물렀다 → SSE 는 이동 이온이
  있고 이온·공유 결합이 섞여 PES 가 복잡하니 더 넓게 검증해야 한다 → **14종**(절연체·전도체·전극·SSE)
  에 적용 → **Fig. 2a** 의 ΔE(예측 − 실험), **음수 = 예측이 더 안정** → **12종 성공**, **5종은 ΔE 음수**.
- **왜 여기 있나**: 검증의 본문. **ΔE 부호 규약이 여기서 정의**되므로 놓치면 Fig. 2a 를 거꾸로 읽는다.
- **막히는 말**: **1원계/2원계(unary/binary)** = 원소 종류 수. **ΔE** = E(예측 최안정) − E(실험 참조).
- ⚠ **우리가 아는 문제**: *"**five** candidate compositions exhibited negative ΔE"* 와 다음 문단의
  *"in five cases … **four** systems"* 는 **모순이 아니다** — 뒤의 4는 앞 5의 부분집합(구조까지
  재현한 것)이고 빠진 1건은 **LiAlCl₄**(ΔE 음수지만 공간군 P2₁/m ≠ 참조 P2₁/c). 종전 digest 가
  이것을 모순이라 적었던 것은 **우리 전사 오류였고 철회했다**(§19-R1). 세미나에서 이걸 "논문 오류"로
  발표하면 안 된다.

### §3.1 ¶2 (p.47384 좌단 하단 → 우단, "Despite its outstanding performance, the CSP method failed to reproduce…")
- **뭐라고 하나**: **LiBiO₃ 와 LiGa(SeO₃)₂ 는 실패**. 진단은 MAE_a(전체) vs MAE_f(저에너지)로 —
  LiBiO₃ 는 MAE_a 가 성공 계와 비슷하니 **세대가 더 필요**한 것이고, LiGa(SeO₃)₂(**80 atoms/cell**)는
  **MAE_f 가 커서 저에너지 영역 정확도가 부족**하다. 그리고 성공한 5건 중 4건은 SCAN 으로도 확인했고,
  **LGPS(50 atoms/cell 4원계)를 맞힌 것**이 확장성의 증거다.
- **왜 여기 있나**: **실패를 스스로 해부하는 문단** = 논문의 가장 정직한 대목이자, **동시에 가장 큰
  문제가 숨어 있는 대목**이다.
- **막히는 말**: **MAE_a / MAE_f** → §17 (MAE_f = 최저에너지에서 0.2 eV/atom 이내만 걸러 낸 오차).
- ⚠ **우리가 아는 문제 (2건)**:
  ① 🔴🔴 **본문이 자기 Fig. 2a 를 부인한다.** *"Their potential validity was **confirmed** through
  SCAN calculations, **ruling out PBE-related artifacts**"* 라는데, 그 4건(Li₃PS₄·Na₃YBr₆·Na₃PS₄·Na₃YCl₆)
  중 **Li₃PS₄ 는 −26 → +8**, **Na₃PS₄ 는 −8 → +23 meV/atom** 으로 SCAN 에서 **부호가 뒤집힌다**
  (ΔE>0 = 예측이 참조보다 **덜** 안정). 즉 SCAN 은 확인한 게 아니라 **절반을 반증했다**(§19-N1, §11-3).
  더구나 **SI p 4 는 정반대로 자백한다** — *"Although SCAN **corrected the mischaracterization** for
  Li₃PS₄, LiAlCl₄, and Na₃PS₄…"*(§20-M0). **본문과 SI 가 같은 계산을 두고 반대로 쓴다.**
  ⛔ *"SCAN 으로 검증됐다"* 는 **인용 금지**. 쓰려면 **논문 자신의 SI 문장**을 인용한다(§16).
  ② **본론 4조성에는 SCAN 을 아예 안 돌렸다.** corner vs edge 의 E_rel 차가 **3–42 meV/atom** 인데
  functional 하나로 그 크기의 역전이 이미 관측됐으니, **"corner 이 더 안정"이라는 순위 자체가
  방법 의존일 수 있다**(§11-3). 우리 규율 언어로 **real difference 가 아니라 method-dependent claim**.
- → **SI 로 넘어가는 곳**: *"A detailed analysis of both energetically improved predictions and
  unsuccessful cases is provided in Supporting Information"* → **SI p 3–4**. ★ **여기가 SCAN 자백
  문장이 있는 자리다.** 세미나 준비라면 이 두 쪽은 반드시 실물로 읽으라.

### §3.2 ¶1 (p.47384 우단, "The CSP approach has proven to be an effective tool for exploring novel crystal structures in SSEs…")
- **뭐라고 하나**: CSP 는 최안정 하나만 주는 게 아니라 **준안정 상을 무더기로 준다**, 그중에 고전도
  상이 있을 수 있다 — 그래서 탐색 공간이 넓어진다.
- **왜 여기 있나**: **논문 제목의 "metastable" 을 정당화하는 문단.** §3.1(검증)에서 §3.2(본론)로
  넘어가는 경첩이고, 여기서부터 "안정 = 좋다"는 통념을 흔들기 시작한다.
- **막히는 말**: 없음(전부 앞에서 나온 말).

### §3.2 ¶2 (p.47384 우단 하단 → p.47385 좌단, "To systematically predict promising SSE structures, Li2SiS3 was selected as the primary composition…")
- **뭐라고 하나**: 4조성을 왜 골랐나. **Li₂SiS₃ = 검증 벤치마크**(안정 corner 상과 준안정 edge 상이
  **둘 다 실험 보고**된 유일한 계) · **Li₂GeS₃ = Si→Ge 단순 치환**(Ge⁴⁺ 67 pm > Si⁴⁺ 54 pm 이라
  통로가 넓어질 것) · **Li₂SnS₃ 는 선행연구(ref 82)가 있어 제외** · **Li₄SiGeS₆·Li₄SiSnS₆ 는 상도에서
  SiS₂ ↔ Li₄[Ge,Sn]S₄ 를 잇는 선 위의 1:1 지점**(Fig. S2).
- **왜 여기 있나**: **조성 선택의 정당화** = "아무거나 고르지 않았다"를 보이는 문단. 우리
  pool_provenance 규율의 그들 버전이다(§6).
- **막히는 말**: **tie-line** = 상도에서 두 상을 잇는 직선. 그 위의 점은 두 상의 혼합으로 표현된다.
  **이온반지름(pm)** = Shannon 반지름, 배위수에 따라 값이 달라진다.
- 📎 **Fig. S2 를 여기서 본다**(상도). ⚠ 단 그 그림은 **도식이지 정량 근거가 아니다**(§20-M23).

### §3.2 ¶3 (p.47385 우단, "Figures 3b−e shows the relative stabilities, polyhedral connectivity types, and Li-ion diffusivities…")
- **뭐라고 하나**: 결과 요약. **corner 이 4조성 모두에서 가장 안정**하고(*"likely due to their
  increased structural flexibility"*), **그럼에도 edge 가 확산이 훨씬 빠르다**.
- **왜 여기 있나**: **논문의 중심 문장이 들어 있는 문단.** 여기 두 줄이 제목과 초록의 근거 전부다.
- **막히는 말**: **polyhedral connectivity** → §6.5 (corner/edge/face 가 각각 꼭짓점 1개/2개/3개 공유).
- ⚠ **우리가 아는 문제 (2건)**:
  ① *"**consistently** … across all four compositions"* 는 **확산 쪽에서 과하다.** "2자릿수 이분법"이
  깨끗한 것은 **Li₂SiS₃·Li₂GeS₃ 뿐**이고, **Li₄SiGeS₆ 는 최고 corner(r8, D 0.64) vs 유일 edge(r5, 1.0)
  = 1.6배**, **Li₄SiSnS₆ 는 2.6배**다(§20-M6). 인용할 때 조성을 명시한다(§20g).
  ② *"likely due to their increased structural **flexibility**"* — **같은 단어가 §3.2 ¶6 에서는
  edge 의 안정성 근거로 쓰인다**(§11-13). 한 논문 안에서 "유연해서 corner 이 안정하다"와 "유연해서
  edge 가 안정하다"가 같이 나온다. **설명력이 없는 자유 변수**로 취급해야 한다.
- → **SI 로 넘어가는 곳**: *"the mean square displacement (MSD) results … are shown in Figures
  S4−S7"* → ★ **이 논문에서 가장 값나가는 SI 자료다**(§20d 에 40 궤적 전수 전사).
  *"consistency between MTP and DFT … Figure S3"* → MAE 8값(§20-R3).

### §3.2 ¶4 (p.47385 우단 하단 → p.47386 좌단, "To enable a thermodynamic comparison of the phases at 300 K beyond the 0 K DFT calculations…")
- **뭐라고 하나**: 0 K DFT 만으로는 부족하니 **Gibbs 자유에너지**를 계산했다 → **300 K 에서도 4조성
  전부 corner 이 더 안정**(Fig. S8) → 그리고 **E_hull 이 40구조 전부 50 meV/atom 미만**(Table S2)이라
  합성 가능성이 높다.
- **왜 여기 있나**: **"준안정 상을 실제로 만들 수 있나"에 대한 유일한 답변 문단.** 논문의 실용성
  주장이 전부 이 두 문장(300 K 자유에너지 + E_hull)에 걸려 있다.
- **막히는 말**: **Gibbs 자유에너지 G(T)** = E_DFT + F_vib + pV. 여기서 **F_vib = 진동 자유에너지**
  (phonon 으로 계산, → §17 phonopy). **E_hull** → §17 (convex hull 위로 뜬 높이; <50 meV/atom 이면
  합성 가능하다는 통설).
- ⚠ **우리가 아는 문제 (3건)**:
  ① **SI 본문과 Fig. S8 의 교차온도가 어긋난다** — SI 산문은 *"Li₂SiS₃ 와 Li₂GeS₃ 모두 ~480 K 위"*
  라는데 Fig. S8a 는 **360 K** 다. **그림 값을 쓴다**(§11-10).
  ② **"고온이면 edge 가 유리"는 4조성 중 2조성뿐이다.** Li₄SiGeS₆ 는 **방향이 반대**(280 K **위에서
  corner 이 역전** — 영점에너지 효과), Li₄SiSnS₆ 는 **1000 K 까지 교차가 없다**(§20-M13).
  ③ **phonon 의 supercell·q-mesh·허수모드 점검이 SI 어디에도 없다**(§20-M15). **준안정상 논문인데
  동역학적 안정성을 한 번도 보고하지 않는다** — phonopy 를 돌렸으니 스펙트럼은 갖고 있는데도.
  합성 논거가 *"E_hull < 50 meV/atom"* 한 줄뿐인 것(§11-8)과 같은 공백이다.
  ※ 문단 끝 *"highly **like** to be experimentally synthesizable"* 는 likely 의 오타(§11-13).
- → **SI 로 넘어가는 곳**: **Fig. S8**(G(T) 4패널) · **Table S2**(E_hull 40값 — §20c 에 전수 전사).

### §3.2 ¶5 (p.47386 좌단 하단 → 우단, "Specifically, the CSP framework accurately reproduced the experimentally reported corner-sharing structure…")
- **뭐라고 하나**: ★ **논문에서 가장 많이 인용될 문단.** Li₂SiS₃ 에서 (i) 실험 안정 corner 상을
  **rank 1** 으로 재현, (ii) 실험 준안정 edge 상을 **rank 3** 으로 회수(RDF 로 확인, Fig. S9),
  (iii) 그 edge 상의 확산이 corner 대비 **"at least 2 orders of magnitude"** 높고, (iv) 이는 실험의
  **"over 3 orders of magnitude"**(ref 36) 와 정합하며, (v) 두 위상의 E_rel 차가 **<0.2 eV/atom** 이라
  합성 가능하다.
- **왜 여기 있나**: **검증(§3.1)과 발견(§3.2)이 만나는 지점.** "아는 것을 맞혔다 → 그러니 모르는
  것도 믿어라"의 완성.
- **막히는 말**: **RDF** → §17 (방사분포함수 g(r) — 두 구조가 같은지 값싸게 대조하는 도구).
  **E_rel** → §17 (같은 조성의 **최안정 예측 구조 대비** 상대 퍼텐셜에너지. **생성에너지가 아니다**).
- ⚠ **우리가 아는 문제 (3건)**:
  ① **"2자릿수"(계산)와 "3자릿수"(실험)를 섞지 마라.** 뒤는 **ref 36 = Huang, JACS 2022, 144, 4989
  소환**이고 이 논문의 측정이 아니다. 덱의 *"10⁻⁴ → 2.4 mS/cm = 4자릿수"* 는 **둘 다 아니고 출처
  불명**이다(§9-A). ⛔ 그 σ 수치는 **인용 금지**.
  ② **RDF 일치는 Si·S 만이다.** Fig. S9 의 edge 행에서 **Li 쌍**은 predicted 에 reported 에 없는
  peak 가 **r ≈ 3.05 Å** 에 서 있다(§20-M17). **이온전도 논문에서 하필 Li 부격자가 안 맞는다** —
  *"예측 edge 상 = 실험 edge 상"* 은 **"골격은 같고 Li 배열은 다르다"** 로 고쳐 읽는다.
  ③ *"**<0.2 eV/atom**"* 은 Fig. 3b 실측 **~0.017 eV/atom** 과 한 자릿수 다르다. 상한 서술이라
  형식상 거짓은 아니지만, 본문 4문장이 **0.1–0.3 eV/atom 스케일의 자기완결적 서사**를 만드는 반면
  그림·표의 실제 세계는 **0.003–0.044 eV/atom** 이다(§9-B). ⛔ **본문 산문의 E_rel 값은 인용 금지,
  Fig. 3 / Table S2 값만 쓴다.**

### §3.2 ¶5 후반 = Li₂GeS₃ (p.47386 우단 끝 → p.47387 좌단, "Figure 3c exhibits a similar trend for Li2GeS3…" → "ologies. However, despite their promising ionic mobility…")
> ※ **한 문단이 쪽을 넘어가며 잘린 것**이라 따로 뽑았다. 종이에서는 p.47386 마지막 줄과 p.47387
> 첫 줄을 이어서 읽어야 한다.
- **뭐라고 하나**: Li₂GeS₃ 도 edge 가 빠르지만 **E_rel 이 높아(≥0.3 eV/atom) 실험적으로 어렵다**
  → 그래서 **실제로 보고된 Li₂GeS₃ 구조는 전부 corner-sharing** 이고 SSE 로 못 쓴다.
- **왜 여기 있나**: **"확산은 좋은데 못 만든다"의 사례 문단.** 논문의 서사를 단조롭지 않게 만드는
  장치이고, 동시에 §3.2 ¶6(Li₄SiGeS₆ 는 반대로 만들기 쉽다)의 대조군이다.
- **막히는 말**: 없음.
- ⚠ **우리가 아는 문제 (3건)**:
  ① 🔴 **이 논문에서 유일하게 엄밀한 수치 모순이 여기다.** *"relatively high formation energies
  (E_rel **≥ 0.3 eV/atom**)"* 는 **하한 서술**인데 Fig. 3c 실측은 **0.031·0.042 eV/atom** 이다 —
  **정면 모순, 10× 과대**(§9-B). 다른 3문장은 상한 서술이라 형식상 참이지만 이건 아니다.
  ② ⚠ **E_rel 을 "formation energy" 라 부른다.** E_rel 은 **같은 조성의 최안정 예측 구조 대비
  상대 퍼텐셜에너지**이지 생성에너지가 아니다(§11-13). 용어가 표류한다.
  ③ 🆕 **이 문단의 대상인 Li₂GeS₃ 가, 저자들이 공개한 구조 파일과 어긋난다.** 배포된 10개 CIF 를
  독립 판정하니 **edge-sharing 은 #7(C2/m, Ge–Ge 3.23 Å) 하나뿐**이고 **#6·#10 은 corner-sharing
  사슬**이다 — Fig. 3c 는 6·10 을 edge 로 찍는다(§21e, **Q9 신설**). **어느 쪽이 맞는지 우리는 판정
  못 한다.** 다만 **배포 CIF 로 Li₂GeS₃ 를 재현하려 하면 Fig. 3c 와 안 맞는다**는 것은 확정이다.

### §3.2 ¶6 (p.47387 좌단, "Figure 3d,e highlight the exceptional Li-ion transport properties of the metastable edge-sharing topologies…")
- **뭐라고 하나**: 4원계 둘. **Li₄SiGeS₆ 의 edge 상은 E_rel 이 ≤0.1 eV/atom 로 낮아 가장 유망**하고,
  그 이유는 **이종원소(Si–Ge) 연결**이라 *"구조적 무질서와 유연성이 커져 안정성이 좋아진다"*.
  **Li₄SiSnS₆ 는 Sn⁴⁺(83 pm)이 커서 결합 기하가 유연해 mixed 위상이 가장 자주 나오는데**,
  **mixed 는 확산이 전부 바닥**이다 — *"corner-sharing topologies act as **bottlenecks**"*.
- **왜 여기 있나**: 본론의 마무리. **"edge 만이 고전도와 합성가능성을 동시에 준다"** 는 결론이 여기서 난다.
- **막히는 말**: **이종원소/동종원소 연결(hetero-/homoelemental linkage)** = 이어진 두 다면체의 중심
  원자가 다른 원소냐 같은 원소냐. **bottleneck(병목)** → §7.5.
- 🔑 **우리 쪽 접점 (2건)**:
  ① *"corner-sharing topologies act as bottlenecks"* → **mixed 는 두 성질의 평균이 아니라 최악값
  지배**다. 이건 **우리 퍼콜레이션 프레임과 정확히 동형**이다(§7e, `kb/concepts/ordered_vs_disordered.md`
  §4 의 F* 문턱). 세미나에서 우리 얘기로 넘어가기 두 번째로 좋은 다리.
  ② **이종원소 혼합이 준안정상의 에너지 페널티를 깎는다** → 우리 **co-doping 교호작용**의 구조적
  기구 후보(§10d). 단 논문은 **정성 서술뿐이고 정량 분해가 없다**.
- ⚠ **우리가 아는 문제 (2건)**:
  ① **Li₄SiGeS₆ 의 "edge 가 최고"는 구조 1개에 기반한다** — 이 조성의 edge 표본은 **rank 5 하나뿐**
  (§11-7). 그리고 그 조성의 최고 corner(rank 8)는 **MSD 28 Å² 로 edge(32)에 육박**한다(§20-M6).
  ② 여기 나오는 *"enhances structural disorder and **flexibility**, thereby improving overall
  stability"* 가 **§3.2 ¶3 의 "corner 이 유연해서 안정하다"와 정면으로 같은 어휘·반대 방향**이다
  (§11-13).

---

### §3.3 ¶1 (p.47387 좌단 하단 → 우단 상단, "So far, we performed CSP on four sulfide electrolyte compositions, revealing that…")
- **뭐라고 하나**: 지금까지를 요약하고 **"왜 하필 edge 인가는 아직 불분명하다"** 고 인정한다.
  그리고 **선행 고속스크리닝 연구(ref 88)는 corner-sharing 산화물이 좋다고 한다** —
  *"This observation **contradicts** the results obtained by this study, and further investigation
  is essential."*
- **왜 여기 있나**: **§3.3(기구) 전체의 동기 문단.** 그리고 **논문에서 가장 취약한 자리**다.
- **막히는 말**: **고속스크리닝(high-throughput screening)** = 이미 있는 DB 를 대량으로 훑는 방식
  (CSP 와 반대 — 있는 것 중 고르기).
- ⚠ **우리가 아는 문제 (2건)**:
  ① **ref 88 = Jun, K. et al., "Lithium superionic conductors with corner-sharing frameworks",
  *Nat. Mater.* 2022, 21, 924 (Ceder 그룹)** — **정반대 주장**이다. 논문은 충돌을 **인정만 하고
  넘어간다**. ⚠ 그러므로 **"edge-sharing 이 좋다"를 일반 명제로 인용하면 안 된다** —
  **"황화물 4조성에서"** 라는 단서가 필수다(§11-5).
  ② 🔑 **더 이상한 것**: 화해의 열쇠(**그쪽은 oxide, 이쪽은 sulfide**)를 **자기 문장 안에 이미
  써 놓고도**(*"corner-sharing **oxide** structures"*) 그것을 근거로 삼지 않는다. 그리고 **두 쪽
  뒤에서는 같은 ref 88 을 자기 기술자 ③(CSM)의 권위로 인용**한다(§11-5, §20-M21). **자기 결론을
  반박하는 논문을 자기 도구의 근거로 쓰는 셈**이다.

### §3.3 ¶2 (p.47387 우단, "To address this, the Li-ion migration behavior in the most stable corner-sharing phase…")
- **뭐라고 하나**: Li₂SiS₃ 와 Li₄SiGeS₆ 의 corner/edge 대표 상에서 **Li 확률밀도 등가면**과
  **van Hove 자기상관**을 봤다(**Fig. 4a,b**, 60 ps @600 K). corner 은 **r < 2 Å 에 단일 강피크가
  60 ps 내내** = **갇힘**. edge 는 **첫 10 ps 만 그 피크, 이후 장거리로 넓게 분포** = **탈출 후 자유 이동**.
- **왜 여기 있나**: **기구 논증의 1단계 = "무엇이 다른가"를 눈으로 보이는 문단.**
- **막히는 말**: **등가면(isosurface)** = 3차원 스칼라장에서 값이 같은 면. 여기서는 "Li 가 있을
  확률이 이 값 이상인 영역"의 껍질. **van Hove 자기상관 $4\pi r^2G_s(r,t)$** → §17
  (시각 t 에 **같은 입자가** 출발점에서 거리 r 에 있을 확률밀도).
- 🔑🔑 **우리 쪽 접점**: **van Hove 자기상관은 우리 MSD 파이프라인에 없는 진단**이고 이미
  **T12** 로 등록돼 있다(§8a). 특히 **MSD 기울기로는 둘 다 "거의 0"이라 구분이 안 될 때 갇힘의
  성격 자체를 보여준다**는 게 값이다. `lee2024` 에 이어 **두 번째 실증** → T12 우선순위 근거.
  ⚠ 단 판정력이 있는 것은 **self-part 뿐이다** — distinct-part 는 σ 가 10⁴ 배 다른 배열들도
  육안 구별이 안 된다(`jun2022` §20-N6, 3건 연속 같은 경고).
- 📎 **Fig. 4a,b 를 실제로 볼 것**: x축이 **0–~57 ps**(60 이 아니다), y축 r = 0–10 Å. edge 패널의
  흰 점선 상자가 *"Li diffuse"* 라벨 구간이다. **Li₄SiGeS₆ edge 는 Li₂SiS₃ edge 보다 눈에 띄게
  약하다** — D 가 1.0 vs 2.35 인 것과 정합한다.

### §3.3 ¶3 (p.47387 우단, "From the Li-ion transport analysis, no significant Li-ion migration was observed in the interstitial spaces…")
- **뭐라고 하나**: ★ **이 논문의 개념적 신규성.** 연결된 다면체 **사이의 틈**에서는 corner 이든
  edge 든 **Li 이동이 전혀 관측되지 않는다**(Fig. 4c) → 그 틈은 중심 양이온(Si⁴⁺/Ge⁴⁺/Sn⁴⁺)의
  **정전 반발**로 Li 가 못 들어가는 **pseudopolyhedron void** 이고, 이것을 **dead volume** 이라
  부른다(Fig. 4d) → *"most previous studies have **overlooked** these regions."*
- **왜 여기 있나**: 기구 논증의 2단계 = **"빈 공간에도 죽은 빈 공간이 있다"**. 통념("빈 공간 =
  전도 경로")을 깨는 자리이고, 뒤의 기술자 ①(α)이 여기서 태어난다.
- **막히는 말**: **interstitial space(틈새 공간)** = 원자가 차지하지 않은 부분. **pseudopolyhedron
  void** = 진짜 다면체는 아닌데 다면체처럼 둘러싸인 빈 공간. **dead volume** → §17.
- 🔑 **우리 쪽 접점**: 이 언어를 **우리 BVSE 해석에 이식**하면 좋다(§10d, §15-G). 지금 우리는
  "채널 %"라고만 쓰는데, **"above-min iso 밖의 공동 = dead volume"** 이라고 명명하면 물리가 선명해진다.
- 📎 **Fig. 4d 를 반드시 볼 것**: 두 다면체가 꼭짓점을 공유하고, **그 사이를 둘러싼 S 들이 이루는
  회색 다각형**이 "Dead volume" 이라 적혀 있고 양쪽에서 Li 가 ✕ 로 막힌다. **즉 스키마는 "이웃한
  S 들의 볼록 다면체"를 시사한다** — 다만 **어느 S 를 꼭짓점으로 잡는지의 규칙이 없어** 여전히
  재현 불가다(§21f 의 Q3 정밀화).

### §3.3 ¶4 (p.47387 우단, "Figure 4e demonstrates that the edge-sharing topology features a shorter distance…")
- **뭐라고 하나**: 왜 edge 의 dead volume 이 작은가, 두 단계. ① **기하** — edge 는 두 중심 양이온
  거리가 짧다(**d_c > d_e**) → 틈이 작다. ② **정전** — edge 에서는 공유 음이온이 **두 이웃 양이온의
  인력을 동시에** 받아 다면체가 **압축**된다 → 다면체 부피도 작아진다. 실측은 **Fig. 4f / S10**.
- **왜 여기 있나**: 기구 논증의 3단계 = **"왜 그런가"의 물리.** 여기까지가 정성 논증이고 다음
  문단부터 정량 기술자로 넘어간다.
- **막히는 말**: **d_c / d_e** = corner / edge 에서의 중심–중심 거리. 우리 §21e 의 **M–M 거리**가
  정확히 이 양이다(실측: edge **2.96–3.28 Å** vs corner **3.46–4.01 Å**, 완전히 갈린다).
- ⚠ **우리가 아는 문제 (2건)**:
  ① **Δdead volume 이 두 조성 모두 정확히 −0.69 Å³** 이고, **Li₂SiS₃ edge 의 dead volume 4.98 =
  SiS₄ 다면체 부피 4.98** 로 완전히 같다(§19-N8). **독립 산출량 3개가 같은 값에 떨어진다** — 우연일
  수도, 산출 방식의 인공물일 수도. **원자료 없이는 판정 불가.**
  ② **각 범주의 표본이 3개뿐**이고, **Fig. S10 의 확대판이 이상치를 잘라낸다** — Li₄SiGeS₆ corner
  dead volume 에 **~11.75 Å³ 짜리가 하나** 있어서, 넣으면 평균이 6.05 가 아니라 **7.96** 이다
  (§20-M12). **인용값 6.05 는 평균이 아니라 최빈값**이다.
- 📎 **Fig. 4f 를 볼 것**: 세로축 5.0–6.2 Å³. 파랑=corner, 주황=edge. **점이 각 무리마다 3–4개뿐인
  것이 눈으로 보인다** — 이게 위 ②의 근거다.

### §3.3 ¶5 (p.47387 우단 하단 → p.47388 좌단, "Based on the dead volume concept, we aimed to systematically analyze the key structural factors…")
- **뭐라고 하나**: 빈 공간이 많은 것만으로는 부족하고 **"Li 가 실제로 쓸 수 있는" 부피**를 정량해야
  한다 → 그래서 **packing ratio α** 를 도입한다. **α 가 낮을수록 유효 이동공간이 크고 전도가 좋다.**
  다만 α 는 **국소 환경**을 못 그리므로 Li 동역학 쪽 분석이 따로 필요하다.
- **왜 여기 있나**: **기술자 ①의 도입 문단**이자 기술자 ②③으로 넘어가는 다리.
- **막히는 말**: **packing ratio α = (V_다면체 + V_dead)/V_셀** → §17.
  ⚠ **표준 결정학의 "충전율"과 이름은 같고 뜻이 반대**라는 것을 여기서 확실히 해 두라.
- ⚠ **우리가 아는 문제 (2건)**:
  ① ⚠ **α 의 정의가 한 문단 안에서 자기모순이다.** *"quantifies proportion of the crystal volume
  occupied by structural features that **hinder** Li-ion mobility"* → 바로 다음 문장 *"This parameter
  represents the fraction of lattice space **available** for Li-ion transport"* — **정반대**다.
  세 번째 문장(*"lower α = larger effective migration space"*)은 첫 정의와 정합한다(§19-N3).
  ✅ **SI 쪽 정의는 일관되므로, 정의를 인용해야 하면 SI 를 인용한다**(§20-M11).
  ② ⛔ **V_dead 의 알고리즘이 문서 어디에도 없다.** 본문은 *"as detailed in Supporting Information"*
  으로 SI 에 넘기고, **SI p 7 은 *"provided in the main text"* 로 본문에 되돌린다** — **순환 위임**
  (§20-M10). 그래서 **α 는 재구현 금지**이고, 우리는 **BVSE 채널 %** 라는 더 나은 것을 이미 갖고
  있다(§10c). 🆕 **저자 공개 스크립트에도 V_dead 는 없다**(§21d) — 이제 문서가 아니라 **코드로도
  확인된 부재**다.
- → **SI 로 넘어가는 곳**: *"as detailed in Supporting Information"* → **SI eq 9**(α 정의).

### §3.3 ¶6 (p.47388 좌단, "To this end, the investigation focused on the Li−S4 sublattice, which is a fundamental structural moiety…")
- **뭐라고 하나**: 기술자 ②③의 도입. **Li–S₄ 부격자**(Li 하나를 S 4개가 사면체로 둘러싼 것)를 본다.
  **Li–S 거리가 멀수록(부피가 클수록) 정전 인력이 약해 이동 유리**(Fig. S11a). 그리고 **다면체
  왜곡이 크면 Li–음이온 상호작용 지형이 평탄해져 활성화에너지가 낮아진다**(Fig. S11b, refs 88·89)
  → 그 왜곡을 **CSM** 으로 정량한다.
- **왜 여기 있나**: **α(전역 부피) 로는 못 보는 국소 환경**을 채우는 문단. 세 기술자가 여기서 완성된다.
- **막히는 말**: **moiety(구조 단위)** = 구조 안에서 반복되는 덩어리. **CSM(연속대칭척도)** → §17
  (실제 다면체가 이상적 대칭 다면체에서 얼마나 벗어났나, 0=완벽).
  **"평탄한 지형"** → §7.5 (우물이 너무 깊어도 안 좋다 — 자리들이 고르게 얕아야 잘 통한다).
- 🔑 **우리 쪽 접점**: **ref 89 = Di Stefano et al., "Superionic diffusion through frustrated energy
  landscape", *Chem* 2019, 5, 2450** — **우리 SDCP 자리에너지 산포 언어와 같은 계열**이다(§19c).
- ⚠ **우리가 아는 문제**: **ref 88 은 §3.3 ¶1 에서 자기 결론을 반박하던 그 Jun/Ceder 논문**이다
  (§20-M21). 두 쪽 만에 적에서 권위로 바뀐다.
- → **SI 로 넘어가는 곳**: *"Further information on CSM is provided in Supporting Information"*
  → **SI eq 10–11**. 🆕 단 **실제로 돌린 것은 eq 10–11 을 손으로 구현한 게 아니라 pymatgen
  chemenv 의 `T:4` CSM 이다**(§21d) — 우리가 같은 수를 내려면 그 함수를 불러야 한다.

### §3.3 ¶7 (p.47388 좌단 하단 → 우단, "Figure 5 presents the packing ratio (α), Li−S4 sublattice volume, and CSM for the 10 most stable…")
- **뭐라고 하나**: **Fig. 5a(Li₂SiS₃)** 판독. edge 상이 **α 가 뚜렷이 낮고**(dead volume 이 작아서),
  **Li–S₄ 부피와 CSM 은 높다** → 이동 유리. 반대로 corner 은 α 가 높고 부피·CSM 이 좁은 범위에
  갇혀 있으며, **최안정 corner 상은 CSM 이 유난히 낮아**(*"exceptionally low CSM"*) 강직하고
  Li 가 거의 안 움직인다 — Fig. 4a 및 실험의 극저 전도도와 정합.
- **왜 여기 있나**: **세 기술자를 실제 데이터에 붙이는 문단** = 기구 논증의 결론부.
- **막히는 말**: **Fig. 5 는 한 축에 정보 3개를 얹는다** — **초록 막대 높이 = α**(오른쪽 축),
  **원의 높이 = Li–S₄ 부피**(왼쪽 축), **원의 색 = CSM**(컬러바 2.0–6.0). 원 하나가 **Li 자리 하나**의
  **궤적 평균**이다(§21d 로 확정).
- ⚠ **우리가 아는 문제 (2건)**:
  ① *"the structural characteristics of the edge-sharing topology with **high packing efficiency**"*
  — 또 뒤집힌 표현이다. **α 는 낮다**(§19-N2). 같은 쪽 우단에서는 *"significantly **lower** α"*
  라고 옳게 쓴다. **한 쪽 안에서 두 번 방향이 바뀐다.**
  ② **α 막대 40개 중 16개(40 %)가 축 상한에서 잘려 값을 읽을 수 없다**(§20-M8). Fig. 5a 는 rank 2,
  Fig. 5b 는 rank 1·7 이 **0.100 에서 클립**된다. **"predictive indicator" 주장의 실제 데이터 기반은
  40점이 아니라 24점**이다.
- 📎 **Fig. 5a 실측**(우리 판독): **edge = 0.0755–0.0797**(rank 3,4,5,8,9) vs **corner = 0.0834–≥0.100**
  (rank 1,2,6,7,10) → **완전 분리**. 이건 **가장 깨끗한 기술자**다.

### §3.3 ¶8 (p.47388 우단, "Contrasting trends between the corner- and edge-sharing phases appear consistently in Figures 5b and S12…")
- **뭐라고 하나**: **Fig. 5b·S12** 에서도 같은 대비가 나타난다 — edge 는 **α 가 낮고 Li–S₄ 부피와
  CSM 은 높다**. 그래서 세 기술자를 **"이온전도 예측 지표(predictive indicators)"** 로 확립한다.
  그리고 곧바로 논문 전체의 결론 문장으로 넘어간다.
- **왜 여기 있나**: **결과부의 마지막 문단이자 제목의 근거.** §4 결론은 이 문단의 재진술이다.
- **막히는 말**: 없음.
- ⚠ **우리가 아는 문제 (3건)**:
  ① *"the edge-sharing phases in **both compositions** … CSM values are relatively higher"* 는
  **Li₄SiGeS₆ 에서 CSM 에 대해 성립하지 않는다**(§11-6). Fig. 5b 재판독: edge(rank 5)는 **적/주황
  CSM ≈ 3–4.5** 이고, **가장 밝은 점(흰색, CSM 5.5–6.0)은 corner rank 8·9·10 과 mixed rank 7** 에
  몰려 있다. (Li–S₄ 부피 쪽은 성립한다.)
  ② 🔑 **그런데 여기서 더 좋은 게 나온다** — CSM 이 가장 높은 corner rank **8·9·10** 은 Fig. 3d 에서
  **corner 7개 중 D 가 0 이 아닌 유일한 셋**(0.64/0.22/0.14)이다. 즉 **CSM 은 D 를 따라가는데
  연결방식은 안 따라간다**(§19-N5). 인과사슬 `edge → 왜곡↑ → D↑` 에서 **가운데 항만 독립적으로
  작동**하고 첫 화살표가 끊긴다. ⭐ **우리에게는 이게 오히려 좋은 소식**이다 — 우리 host 에는
  corner/edge 축이 없으니(§10b), CSM 이 **연결방식과 무관한 독립 기술자**라면 그대로 쓸 수 있다.
  ③ ⭐ **"predictive indicator" 는 과한 표현이다.** **요약 통계(평균±표준편차)도, 상관계수도,
  회귀도 논문에 없다.** 세 기술자와 D 의 관계는 **전부 육안 주장**이다(§11-6). 상관을 보였을 뿐
  예측력을 시험한 적이 없다.
- ⭐ **우리 판독이 찾은 규칙(논문의 주장이 아니다)**: **D > 0 ⟺ (Li–S₄ 부피 ≳ 7 Å³) ∧ (CSM ≳ 3)**
  — **둘 다 커야 움직인다.** 결정적 반례가 **Li₄SiSnS₆ rank 9**(CSM 최고 ≈6 인데 **D = 0**, 부피가
  5.0–5.7 로 최저)이고, **Fig. 5b 의 mixed rank 7 이 세 번째 사례**다(부피가 5.9–8.3 로 극단적으로
  퍼져 있어 **한 자리도 두 조건을 동시에 만족하지 못한다** → D = 0.02). → **우리 47종에 얹을 때
  단일 지표 회귀로 가면 반드시 깨진다. 결합 기준(2차원 격자)으로 설계한다**(§20e, 채택항목 H).
- → **SI 로 넘어가는 곳**: **Fig. S12**(Li₂GeS₃·Li₄SiSnS₆ 판) — α 분리의 4조성 일반성 확인.

---

### §4 결론 (p.47389 좌단, "This study aimed to predict novel SSE structural phases to overcome the limitations…")
- **뭐라고 하나**: 전체 재진술. 12조성 재현 → 4조성 CSP → **corner 은 안정하나 D 가 극히 낮고 edge 는
  준안정이나 수송이 좋다** → dead volume 이 원인 → **α · Li–S₄ 부피 · CSM 을 예측 지표로 확립**.
- **왜 여기 있나**: 요약. **새 정보가 없다** — 시간이 없으면 건너뛰어도 되는 유일한 절이다.
- ⚠ **우리가 아는 문제 (2건)**:
  ① **여기 적힌 기술자 3종이 "정본"이다** — **α / Li–S₄ 부격자 부피 / CSM**. 우리 덱 슬 29 는
  이것을 **dead volume / distance of cation / Li–S₄ distortion** 이라 적었는데 **앞 둘은 기술자가
  아니라 기구**다(§9-C). 덱 목록을 그대로 인용하면 **논문에 없는 기술자 2개를 만들어내는 셈**이다.
  ② 결론에서도 **σ 는 한 번도 나오지 않는다.** 제목의 *"Superior Ionic Conductivity"* 는
  **D 의 대리 서술**이다(§11-1).

### ASSOCIATED CONTENT / Data Availability (p.47389 좌단 하단)
- **뭐라고 하나**: 원자료는 **figshare `10.6084/m9.figshare.29468165.v4`**.
- ⚠ **우리가 아는 문제**: 🆕 **논문은 GitHub 코드 저장소를 밝히지 않는다.** 그러나 실제로는
  `github.com/jhkimmmmm/CSP_SSE` 에 **MTP 퍼텐셜·구조 CIF·CSM 분석 스크립트**가 올라와 있고
  (우리가 확보 → §21), **LICENSE 가 없다.** ⛔ **재배포·우리 결과로 제시 금지, 내부 분석 전용.**

---

### SI 24 pp — 절 단위 안내 (문단별로 읽지 마라)

> **SI 는 §20 에서 이미 전수 검증했다**(Fig S1–S12 + Table S1–S2 + MSD 궤적 40개). 여기서는
> **본문에서 넘어가는 지점**과 **실제로 읽을 가치가 있는 세 곳**만 표시한다.

| SI 위치 | 무엇 | 읽을 가치 | 우리 판정 |
|---|---|---|---|
| **eq 1–4** (p 1–3) | MTP 기저(moment tensor) 정의 | 낮음 — 원전(Shapeev 2016)이 낫다 | 실제 퍼텐셜 헤더는 **§21b 실측** |
| **p 3–4** | 검증 성공/실패 상세 | ★★★ **높음** | **SCAN 자백 문장이 여기 있다**(§20-M0). 본문과 정반대 |
| **eq 5–8** (p 4–5) | MSD·D·Arrhenius·Nernst–Einstein | ★★ **높음(반면교사)** | 🔴 **eq 5 가 "제곱의 차"로 틀렸다**(§20-M1). eq 7–8 은 **쓰이지 않은 보일러플레이트**(§11-1) |
| **F_vib / G(T)** (p 5–6) | 자유에너지 절 | 중간 | ⚠ **supercell·q-mesh·허수모드 미보고**(§20-M15) |
| **eq 9** (p 6–7) | packing ratio α | 중간 | ✅ **정의는 SI 가 일관**(§20-M11). ⛔ 단 **V_dead 알고리즘은 본문으로 되돌린다**(§20-M10) |
| **eq 10–11** (p 7) | CSM | 중간 | 🆕 실제 계산은 **pymatgen chemenv `T:4`**(§21d) |
| **Fig. S1 · Table S1** | 14종 공간군·MAE | 중간 | §5c–5d 에 전수 전사됨 |
| **Fig. S2** | 상도 | 낮음 | ⚠ **진짜 hull 단면이 아니다**(§20-M23) |
| **Fig. S3** | MTP–DFT 상관 + MAE | 중간 | ⚠ 단위 오기 **"eV/atom"→실제 meV** 8군데 · **Li₂SiS₃ 만 400 Gen 부재**(§20-M18·M19) |
| **Fig. S4–S7** | ★ **MSD 원자료 40 궤적** | ★★★ **가장 높음** | 🔴 **감소 구간 2건 · 42 ps 궤적 1건 · 계단형에 D 부여 6건**(§20-M2·M3·M4). **§20d 에 전수 표** |
| **Fig. S8** | G(T) 교차온도 | ★★ 높음 | **360/480/280/없음** — 산문(~480 K)과 어긋난다. **Li₄SiGeS₆ 는 방향 반대**(§20-M13) |
| **Fig. S9** | RDF 검증 | ★★ 높음 | ⚠ **Si·S 는 맞고 Li 가 안 맞는다**(§20-M17) |
| **Fig. S10** | 부피 분포 전체범위판 | 중간 | ⚠ **이상치 11.75 Å³ 를 확대판이 잘라낸다**(§20-M12) |
| **Fig. S11** | Li–S₄ 개념도 | 낮음 | 기술자 ②③의 그림 설명 |
| **Fig. S12** | Fig. 5 의 나머지 2조성 | ★★ 높음 | **α 4조성 전부 완전 분리** 확정(§20-R5·M9). 단 **막대 40 % 클립**(§20-M8) |
| **Table S2** | E_hull 40값 | ★★ 높음 | **0–42 meV/atom 전원 통과** — §20c 전수 전사 |

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
| **DFT query 총 횟수** | ⛔ **미보고** (Fig S3 산점도 점 개수로도 정확 판독 불가) — **여전히 미해소**(배열 수 ≠ DFT 호출 수) |
| **학습셋 최종 크기** | ~~⛔ 미보고~~ → **✅ 종결 2026-08-26 · 데이터저장소 실측**: train **863 / 1,391 / 1,038 / 1,104** + valid **96 / 158 / 110 / 90** (Li₂SiS₃ / Li₂GeS₃ / Li₄SiGeS₆ / Li₄SiSnS₆). **논문·SI 에 없다는 사실은 그대로다** — §21b |
| **MTP 파일 실측** (신규) | `MTP1m` v1.1.0 · `RBChebyshev` · `radial_basis_size 8` · `radial_funcs_count 5` · `alpha_moments_count 1352` · **`max_dist 5.000 Å` = 본문 `R_cut 5 Å` 와 일치 ✅** · `min_dist` 1.0954/1.1310/1.1033/**1.6873** (⚠ Li₄SiSnS₆ 만 홀로 크다 — §21b-4) |
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
| 3 | **edge** | **≈1.75** | ~0.004 | **0** | **"Exp." 라벨 — 실험 준안정 edge상 재현 ✅** (⚠ RDF 일치는 **Si·S 만**, Li 는 불일치 — §20-M17) |
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
| **Li₂GeS₃** (Fig S12a) | **8개 전부 ≥0.100** (축 상한 클립) | **0.0847 (r6) / 0.0820 (r10)** | — | ✅ 분리 (단 corner 값은 전부 판독 불가) |
| **Li₄SiSnS₆** (Fig S12b) | **0.0978 (r10) · 0.1009 (r6) · 0.1026 (r1) · ≥0.12 ×3** | **0.0912 (r2) / 0.0879 (r5)** | **≥0.12 ×2** (r3, r8 클립) | ✅ **완전 분리** (edge 최고 0.0912 < corner 최저 0.0978) |

> 🔧 **[2026-08-04 SI 실물 검증 — §20-R5·M8·M9]** 아래 두 줄은 Fig S12 **750 dpi 재판독**으로 갱신됐다.
> ① Li₄SiSnS₆ 판정을 **○ → ✅ 완전 분리**로 격상 — α 의 4조성 일반성은 오히려 강해진다.
> ② 그러나 **α 막대 40개 중 16개(40 %)가 축 상한에서 잘려 값 자체를 읽을 수 없다**
> (Li₂GeS₃ 8 · Li₄SiSnS₆ 5 · Li₂SiS₃ 1 · Li₄SiGeS₆ 2). **"predictive indicator" 의 실제 데이터 기반은 24점.**

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
**놓친 저에너지 상이 있을 가능성**은 정량화되지 않았다.

> 🔧 **[2026-08-04 SI 실물 검증 — 정정, §20-R3]** 종전 *"4조성 중 **3조성**에서 MAE_f > MAE_a"* 는 **틀렸다.**
> Fig S3 실측 8값: **MAE_a** = 28.8 / 25.0 / 29.5 / 35.2, **MAE_f** = 13.2 / 27.4 / 29.8 / 33.3 meV/atom
> (Li₂SiS₃ / Li₂GeS₃ / Li₄SiGeS₆ / Li₄SiSnS₆). → MAE_f > MAE_a 는 **Li₂GeS₃·Li₄SiGeS₆ 2조성뿐**이고,
> Li₂SiS₃(13.2 ≪ 28.8)·Li₄SiSnS₆(33.3 < 35.2)은 반대다. **비판의 방향은 유지** — 2조성에서 저에너지
> 영역이 더 나쁘고, Li₄SiSnS₆ 도 개선폭이 5 % 뿐이며, **네 값 모두 Table S2 의 E_hull 전 범위(0–42 meV/atom)와
> 같은 크기**다. ⚠ Fig S3 은 이 값들의 단위를 **"eV/atom"** 이라 적는다(실제 meV/atom, §20-M18).

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
>
> 🔧 **[2026-08-26 데이터저장소 — 셀 크기 부분 종결, §21c]** 종전 *"AIMD 셀은 ref 47 참조라 재현 불가"* 는
> **부분적으로 닫힌다.** `UPSTREAM_README.md` 가 규약을 적는다: *"a supercell was generated to have a
> **lattice dimension as close as possible to ~10 Å**"*. 배포 원 CIF 가 24원자·460–544 Å³ 이므로
> ~10 Å 큐브면 **대략 2배 = 40–50 원자** — **ref 47 의 "~52원자"와 같은 자릿수**이고 본문의
> *"same computational guidelines … including cell size"* 와 정합한다.
> ⛔ **완전 종결은 아니다** — 조성·rank 별 실제 supercell 배수는 여전히 없다.
> 🆕 그리고 **60 ps 는 연속 1회 실행이 아니다** — 저자 스크립트가 `run001/`, `run002/` … 의 vasprun 을
> 범위로 이어 붙인다(**chained restart**, §21d). 논문·SI 어디에도 없는 사실이고, **§20-M2(MSD 감소)·
> M3(42 ps 궤적)** 를 이해하는 데 직접 관련된다 — 이어 붙이는 지점의 시간원점 처리를 알 수 없다.

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

### 13. **핵심 어휘가 표류한다** 🆕 (2026-08-26, 본문 재독)

세 건이고, 셋 다 **같은 성격**이다 — 논문이 한 단어를 서로 다른(때로 반대) 뜻으로 쓴다.

1. ⚠ **"flexibility" 가 corner 의 안정성 근거이자 edge 의 안정성 근거로 동시에 쓰인다.**
   - p 47385: *"the **corner**-sharing topologies … consistently exhibited the highest stability …
     likely due to their **increased structural flexibility** compared with their edge-sharing counterparts."*
   - p 47387: *"this [**edge**-sharing] polyhedral topology is formed through heteroelemental (Si−Ge)
     linkages … which enhances structural disorder and **flexibility, thereby improving overall stability**."*
   → **"유연해서 corner 이 안정하다"와 "유연해서 edge 가 안정하다"가 두 쪽 간격으로 나온다.**
   두 문장 다 정량 근거가 없고(진동 엔트로피도, 탄성 상수도 계산하지 않았다), 방향이 반대다.
   **설명력이 없는 자유 변수로 취급하고 인용하지 않는다.**
   ⚠ 더구나 §3.3 의 기술자 ③(CSM)은 **edge 가 더 왜곡됐다**고 말하는데, 왜곡과 유연성과 안정성의
   관계를 논문은 한 번도 정의하지 않는다.
2. ⚠ **E_rel 을 "formation energy" 라 부른다** (p 47387: *"relatively high **formation energies**
   (E_rel ≥ 0.3 eV/atom)"*). E_rel 은 §2 에서 **같은 조성의 최안정 예측 구조 대비 상대 퍼텐셜에너지**로
   정의됐고, 생성에너지(원소 기준 상태 대비)가 **아니다**. §9-B 의 수치 모순이 하필 이 문장에
   붙어 있어 더 헷갈린다.
3. ⚠ **"packing efficiency" 의 방향이 세 번 바뀐다** — 초록(높다) → §1 ¶5(정의는 옳게: nonconductive
   volume) → p 47388 좌단(*"high packing efficiency"*) → p 47388 우단(*"significantly **lower** α"*).
   §19-N2·§20-M11 과 같은 사안이고, **여기서는 "한 쪽 안에서 두 번 뒤집힌다"는 점**만 추가한다.
   ※ 같은 문단에 *"highly **like** to be experimentally synthesizable"*(p 47386, likely 오타)도 있다.

> 🔑 **왜 이걸 항목으로 세우나**: 세미나에서 *"왜 edge 가 안정성 페널티가 작냐"* 는 질문이 나오면
> 논문의 답은 **"유연해서"** 인데, **같은 논문이 corner 에도 같은 답을 준다.** 대답할 수 없다는 것을
> 미리 알고 있는 편이 낫다. 인용할 때는 **정량이 있는 항목(E_rel 수치·E_hull·G(T) 교차온도)만** 쓴다.

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

> ➕ **추가 항목**: **H·I·J·K → §20f** (SI 회차) · **L·M·N → §21g** (데이터저장소 회차).
> 특히 **L 이 위 항목 C 를 대체·확정한다** — T14 의 구현 선택이 *"chemenv 냐 eq 10 직접이냐"* 에서
> **"저자가 부른 그 함수(`chemenv` `T:4`)를 부른다"** 로 닫혔다(§21d).

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
| ~~Q3~~ ⛔ | ~~$V_{\text{dead}}$ 의 실제 알고리즘~~ | **닫힘(부정형, 2026-08-04 SI).** SI p 7 이 *"Further details … are provided in the main text"* 로 본문에 떠넘기고, 본문은 Fig 4d **스키마**뿐 — **문서 어디에도 없다**(§20-M10). figshare 원자료 확인 외 방법 없음 |
| Q4 | corner vs edge 순위가 SCAN에서도 유지되나 | 논문에 없음. **우리가 판정할 수 없음** — over-claim 경고로만 남김 |
| Q5 | Jun 2022(Nat. Mater.) 의 corner-sharing 주장과의 관계 | ref 88 PDF 확보. **산화물 vs 황화물** 가설 검증 |
| ~~Q6~~ ✅ | ~~DFT query 총 횟수 / 학습셋 크기~~ | **부분 종결 2026-08-26 · 데이터저장소 실측** — 학습셋 train **863/1,391/1,038/1,104** (§21b). ⚠ **query 횟수는 여전히 미보고** |
| **Q9** 🆕 | 배포 CIF 의 **Li₂GeS₃ 연결방식 3건**이 Fig. 3c·S5 와 어긋난다 | §21e. figshare 원자료 또는 저자 문의 |
| **Q10** 🆕 | Li₄SiSnS₆ MTP 의 `min_dist 1.687 Å` 이 그 조성의 품질 저하와 관련 있나 | §21b-4. 가설 보유만 |

> 🔎 **최신 상태는 §21f 를 볼 것** (3차 갱신본).

---

## 19. 🔬 본문 실물 독립 검증 (2026-08-04, 폴더 이상욱 ④)

**대상**: `litdb/inbox/4. Machine Learning-Assisted Crystal Structure Prediction…pdf` = **본문 11 pp**
(JACS 2025, 147, 47381–47391). 텍스트 전수 재추출 + Fig 2a·3b–e·4f·5a·5b **500–800 dpi 재렌더 판독**.
**방식**: digest 를 정답으로 놓지 않고 **PDF 를 원점으로 다시 읽어** 기존 서술과 대조.

> ⚠ **적용 범위**: 이 회차 실물은 **본문뿐**이었다. **SI 24 pp 는 뒤이은 §20 에서 별도로 실물 검증됐다**
> (2026-08-04 2차) — SI 유래 수치(E_hull 0–42, MAE, 교차온도, α·CSM 정의식, 공간군 표)의 최종 판정은 **§20 을 볼 것.**

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

---

## 20. 🔬 SI(24 pp) 실물 독립 검증 (2026-08-04 2차, 폴더 이상욱 ④-SI)

**대상**: `litdb/inbox/4. Sup) Machine Learning-Assisted Crystal Structure Prediction…pdf` = **SI 24 pp**
(`ja5c15665_si_001`). **방식**: 텍스트 전수 재추출(24 pp) + **Fig S1–S12 전부 300–900 dpi 재렌더 판독**,
**Table S1(14행)·Table S2(40값) 전수 전사**, **Fig S4–S7 의 MSD 궤적 40개 전수 판독**.
digest 를 정답으로 놓지 않고 SI 를 원점으로 다시 읽었다.

> ⚠ **적용 범위**: 이번 회차 실물은 **SI 뿐**이다. 본문 11 pp 는 §19(2026-08-04 1차)를 승계한다.
> 본문 유래 수치(Fig 2a·3b–e·4f·5a·5b)는 §19 판정이 최종이다.
>
> 🔑 **결론 먼저**: SI 는 **본문보다 정직하다** — SCAN 반전 3건을 이름까지 대고 인정하고(20a-R4),
> α 정의도 SI 쪽이 일관된다(20b-M16). 대신 **SI 에서만 보이는 방법론 결함이 크게 나온다** —
> **MSD 정의식 오류·MSD 감소 구간·40 궤적 중 1개는 42 ps·계단형 궤적에 D 부여·α 막대 40 %가 축에서 잘림.**

### 20a. 자기철회 / 정정 3건 — 우리가 틀렸던 것

| # | 종전 서술 | SI 실물 | 조치 |
|---|---|---|---|
| **R3** | §11-4: *"4조성 중 **3조성**에서 MAE_f > MAE_a (저에너지 영역을 오히려 더 못 맞춘다)"* | Fig S3 실측 8값: **MAE_a** 28.8 / 25.0 / 29.5 / 35.2, **MAE_f** 13.2 / 27.4 / 29.8 / 33.3 → MAE_f > MAE_a 는 **Li₂GeS₃(27.4>25.0)·Li₄SiGeS₆(29.8>29.5) 2조성뿐.** Li₂SiS₃(13.2≪28.8)·Li₄SiSnS₆(33.3<35.2)은 반대 | **정정 — 3 → 2조성.** 비판의 방향은 유지(2조성에서 저에너지 영역이 더 나쁘고, 나머지도 개선폭이 미미) |
| **R4** | §11-3: *"**SI 본문**이 '…remained more stable…' 이라 적어 자기 Fig 2a와 모순된다"* | SI 원문(p 4)은 **모순을 절반 자백한다**: *"**Although SCAN corrected the mischaracterization for Li₃PS₄, LiAlCl₄, and Na₃PS₄**, the newly identified low-energy structures remained more stable than their reference counterparts."* — **반전 3건을 이름까지 대고 인정**한다 | **부분 철회 + 근거 강화.** ⭐ **우리 Fig 2a 판독(정확히 그 3건)이 SI 산문으로 독립 확인됐다.** 모순의 위치가 재배치된다 → **20b-M0** |
| **R5** | §8d 표: Li₂GeS₃ *"corner 대부분 ≥0.100"* · Li₄SiSnS₆ *"○ (일부 판독 불가)"* | Fig S12 750 dpi 재판독: Li₂GeS₃ **corner 8개 전부** 축 상한 클립 · Li₄SiSnS₆ **edge 0.0879·0.0912 < corner 최저 0.0978** | **격상.** Li₄SiSnS₆ 도 **✅ 완전 분리** — α 의 4조성 일반성은 오히려 강해진다 |

### 20b. 신규 적발 21건 — SI 실물에서만 나오는 것

#### ① 모순의 재배치 (가장 무거운 것)

| # | 적발 | 위치 | 무게 |
|---|---|---|---|
| **M0** | 🔴🔴 **SI 는 반전 3건을 인정하는데, 본문은 그 반대로 적는다.** SI: *"Although SCAN **corrected the mischaracterization** for Li₃PS₄, LiAlCl₄, and Na₃PS₄…"* ↔ 본문 p 47384: *"Their potential validity was **confirmed** through SCAN calculations, **ruling out PBE-related artifacts**."* — 같은 계산을 두고 **SI 는 "고쳐졌다", 본문은 "확인됐다"** 고 쓴다. 게다가 SI 도 자백 뒤 곧바로 *"the newly identified low-energy structures **remained more stable**"* 로 뒤집어, **한 문장 안에서 자기모순**한다 | SI p 4 ↔ 본문 p 47384 ↔ Fig 2a | **§11-3 / §19-N1 최종 확정.** ⛔ *"SCAN 으로 검증됐다"* 인용 절대 금지. 인용 가능한 것은 **논문 자신의 SI 문장**("SCAN corrected the mischaracterization for Li₃PS₄, LiAlCl₄, Na₃PS₄") 뿐 |

#### ② MSD·확산 — SI 원자료가 드러내는 것 ★★ 여기가 이번 회차의 본체

| # | 적발 | 근거 | 무게 |
|---|---|---|---|
| **M1** | 🔴 **MSD 정의식(eq 5)이 틀렸다.** SI: $MSD=\frac{1}{N}\sum_i\langle[r_i(t+t_0)]^2-[r_i(t_0)]^2\rangle$ — **제곱의 차**. 올바른 MSD 는 **차의 제곱** $\langle[r_i(t+t_0)-r_i(t_0)]^2\rangle$. 두 양은 같지 않다(등방 확산에서 전자는 원점 선택에 따라 0 이 될 수도 있다) | SI p 4, eq 5 | 조판 오류일 개연성이 높지만 **정오표 없음**. 방법 절을 그대로 이식하면 안 된다 |
| **M2** | 🔴 **MSD 가 감소하는 구간이 있다.** Li₂SiS₃ rank 5: 52 ps **78 Å²** → 58 ps **72 Å²**. Li₄SiSnS₆ rank 5: 12 ps **4.5** → 16 ps **2.0**. **앙상블/다중 시간원점 평균 MSD 는 단조증가여야 한다** | Fig S4 (r5), Fig S7 (r5) | ⭐⭐ **단일 궤적·단일 시간원점의 직접 증거.** 우리가 2026-08-04 에 `tools/ionic/msd_refit_window.py` 로 **다중 시간원점 평균**을 넣은 것의 **외부 정당화 사례** |
| **M3** | 🔴 **40 궤적 중 1개는 60 ps 가 아니다.** **Li₄SiSnS₆ rank 5 (edge)** 의 Fig S7 x축은 **0–~42 ps**(눈금 0/10/20/30/40). 나머지 39 패널은 전부 0–60 | Fig S7 rank 5 (900 dpi 재판독) | 본문·Fig S12 캡션은 전부 *"AIMD simulations at 600 K **over 60 ps**"*. **하필 4조성 중 edge 표본이 2개뿐인 조성의 edge 하나**가 30 % 짧다 |
| **M4** | 🔴 **"확산"이라 부를 수 없는 궤적에 D 를 매겼다.** 계단형(1회 hop 후 정체) 6건: Li₂SiS₃ **r8**(22–30 ps 계단 → 8.5 Å² 정체) · Li₂GeS₃ **r7**(22–32 ps 계단 → 13 정체) · Li₄SiGeS₆ **r6**(5 ps·22 ps 두 계단 → 5.5 정체)·**r7**(10 ps 에 3.5 도달 후 **50 ps 완전 정체**) · Li₄SiSnS₆ **r6**(30 ps 이후 정체)·**r8**(22 ps 계단 → 2.5 정체) | Fig S4–S7 | ⭐ **§11-2 의 결정적 보강.** 특히 Li₄SiGeS₆ r7(mixed)은 확산이 아니라 **초기 완화**다. Fig 3 의 작은 D 값(0.02–0.3×10⁻⁵)은 **전부 이 부류** — 순위를 매길 양이 아니다 |
| **M5** | 🔴 **끝에서 급상승하는 궤적 2건** — Li₂GeS₃ **r6**(50→60 ps 에 8 → 15.5, 즉 **최종 10 ps 가 전체 변위의 절반**) · Li₄SiSnS₆ **r10**(50 ps 이후 가속) | Fig S5, S7 | **60 ps 가 짧다는 증거가 그림 안에 있다.** 이 궤적들은 아직 정상상태에 들지 않았다 |
| **M6** | ⚠ **"2 자릿수" 이분법은 4조성 중 2조성에서만 성립한다.** Li₂SiS₃·Li₂GeS₃ 는 깨끗(corner 전원 진동 수준). 그러나 **Li₄SiGeS₆**: 최고 corner **r8 (D 0.64)** vs 유일 edge **r5 (1.0)** = **1.6배**. **Li₄SiSnS₆**: 최고 corner **r6 (0.25)** vs 약한 edge **r5 (0.65)** = **2.6배** | Fig S6·S7 MSD + Fig 3d·3e | **§7f 의 *"4조성 모두 일관"* 은 과하다.** 인용 시 *"2자릿수는 Li₂SiS₃·Li₂GeS₃"*, 4원계는 *"수배"* 로 |
| **M7** | 🔑 **MSD 끝점 → D 환산이 Fig 3 을 재현한다** (아래 20d 표). 14개 비-0 값 중 **13개가 ±40 % 안**. 유일 예외 **Li₂GeS₃ r7: SI MSD 13 Å²/60 ps ⇒ D ≈ 0.36×10⁻⁵ 인데 우리 Fig 3c 판독은 0.04 (9×)** | 20d 표 | ⭐ **Fig 3 의 D 가 "전 구간 원점통과 MSD/6t" 임이 사실상 확정.** r7 1건은 **본문 실물 없이는 판정 불가 → Q7 신설** |

#### ③ α(packing ratio) — 기술자의 데이터 기반

| # | 적발 | 근거 | 무게 |
|---|---|---|---|
| **M8** | 🔴 **α 막대 40개 중 16개(40 %)가 축 상한에서 잘려 값을 읽을 수 없다.** Li₂GeS₃ **8/10**(corner 전원) · Li₄SiSnS₆ **5/10**(r3,4,7,8,9) · Li₂SiS₃ **1/10**(r2) · Li₄SiGeS₆ **2/10**(r1,7) ← 뒤 두 줄은 §19-N6 승계 | Fig S12 + Fig 5 | ⭐⭐ **"predictive indicator" 주장의 실제 데이터는 40점이 아니라 24점.** Li₂GeS₃ 패널은 *"edge < 0.085, corner > 0.100"* 이상을 말하지 못한다 |
| **M9** | 📐 **α 수치 정밀화 (750 dpi)** — **Li₂GeS₃**: edge r6 **0.0847**, edge r10 **0.0820**, corner 8개 전부 **≥0.100**. **Li₄SiSnS₆**: edge r2 **0.0912**, edge r5 **0.0879**; corner r10 **0.0978**, r6 **0.1009**, r1 **0.1026**, 나머지 5개(r3,4,7,8,9) **≥0.12** | Fig S12a,b | §8d 표 갱신 → 4조성 **전부 완전 분리** 확정 |
| **M10** | ⛔ **V_dead 알고리즘: SI 가 본문으로 떠넘긴다.** SI p 7: *"Further details about the concept of dead volume are **provided in the main text**."* 그런데 본문에는 Fig 4d **스키마**와 문장 정의뿐 | SI p 7 ↔ 본문 Fig 4d | **순환 위임 확정.** §10c 의 **"α 재구현 금지"** 판정은 이제 추정이 아니라 **문서로 확인된 사실** |
| **M11** | ✅ **α 정의는 SI 가 옳다 — 자기모순은 본문 전용이다.** SI eq 9 절은 일관된다: *"the fraction of unit cell volume occupied by **non-conductive** volume"* → *"A **smaller** α value indicates a **greater** volume available for Li-ion transport"* | SI p 6–7 vs 본문 p 47388 | **§19-N3 정밀화.** 정의를 인용해야 하면 **SI 를 인용**한다. (본문 p 47388 의 뒤집힌 문장은 여전히 인용 금지) |
| **M12** | ⚠ **Fig S10 의 이상치 11.75 Å³ 를 확대판이 잘라낸다.** Li₄SiGeS₆ **corner dead volume** 표본이 {6.06, 6.06, **11.75**} 라면 평균은 **7.96**, 인용값 6.05 는 평균이 아니라 최빈값. 또 **각 범주 표본이 3개뿐** | Fig S10 좌패널 vs 확대패널 | Δdead = −0.69 Å³ 는 **잘라낸 창 안에서만** 성립. (이상치를 포함하면 논문 주장은 오히려 강해지지만, **dead volume 분포가 매우 불균질**하다는 사실이 드러난다) |

#### ④ 자유에너지·상 안정성

| # | 적발 | 근거 | 무게 |
|---|---|---|---|
| **M13** | 🔴 **"고온에서 edge 가 유리"는 4조성 중 2조성뿐이고, 1조성은 방향이 반대다.** Fig S8: (a) Li₂SiS₃ **360 K** 위 edge 우세 · (b) Li₂GeS₃ **480 K** 위 edge 우세 · (c) Li₄SiGeS₆ **280 K — 아래에서 edge 가 더 안정, 위에서 corner 이 역전**(영점에너지 효과) · (d) Li₄SiSnS₆ **1000 K 까지 교차 없음** | Fig S8 (300 dpi) | **§11-10 확정 + 강화.** SI 결론문 *"metastable edge-sharing phases become thermodynamically accessible at higher temperatures"* 는 **절반만 맞다** |
| **M14** | 🔑 **Fig S8 이 대표구조의 rank 를 밝힌다** — corner = **전부 rank 1**, edge = Li₂SiS₃ **3rd** / Li₂GeS₃ **6th** / Li₄SiGeS₆ **5th** / Li₄SiSnS₆ **2nd** | Fig S8 곡선 라벨 | **Fig S4–S7 연결방식 라벨 및 우리 Fig 3 판독과 100 % 일치** — 3중 교차검증 통과 |
| **M15** | ⚠ **phonon 계산의 supercell·q-mesh·허수모드 점검이 SI 어디에도 없다.** 준안정상 논문인데 **동역학적 안정성(허수 진동수 유무)을 한 번도 보고하지 않는다** — phonopy 를 돌렸으니 스펙트럼은 갖고 있다 | SI p 5–6 | ⭐ **준안정상 주장의 가장 표준적인 검증을 건너뛰었다.** "합성 가능" 논거가 E_hull < 50 meV/atom 한 줄뿐인 것(§11-8)과 같은 공백 |
| **M16** | 🔑 **Li₂SiS₃ 준안정 edge 상의 실험적 실현 방법이 SI 에 명시돼 있다** — *"the metastable edge-sharing structure can be realized through **heat treatment**"* (ref 21 = Huang, JACS 2022) | SI p 6 | 종전 digest 의 *"변형 합성조건"*(§6)을 **열처리**로 구체화 |

#### ⑤ 검증·인용·조판

| # | 적발 | 근거 | 무게 |
|---|---|---|---|
| **M17** | ⚠ **RDF 검증이 하필 Li 부격자에서 깨진다.** Fig S9 edge 행: **Li** 의 predicted 에 reported 에 없는 뚜렷한 peak가 **r ≈ 3.05 Å** 에 서 있고 4.05 Å 주피크 높이도 다르다. **Si·S 는 잘 맞는다** | Fig S9 (450 dpi) | ⭐ **골격은 재현했지만 Li 배열은 다르다.** 이온전도 논문에서 *"예측 edge 상 = 실험 준안정 edge 상"* 을 RDF 로 주장하려면 **Li 쌍이 맞아야 한다.** §7b 의 rank 3 *"RDF 일치"* 는 **"Si·S 일치, Li 불일치"** 로 고쳐 읽을 것 |
| **M18** | ⚠ **Fig S3 의 단위 오기 — MAE 를 "eV/atom" 이라 적는다**(4패널 × 2 = **8군데**). 실제는 **meV/atom**(Table S1 은 같은 양을 meV/atom 으로 적는다) | Fig S3 | 소 (교정 품질). 우리 §11-4 는 meV 로 옳게 읽었다 |
| **M19** | ⚠ **Fig S3 Li₂GeS₃ 범례에 "200 Gen" 이 두 번**(보라·주황, 색이 다름). 그리고 **Li₂SiS₃ 만 400 Gen 이 없다**(Initial/50/100/200) | Fig S3 하단 | 🔑 **종료규칙과 정합**: 실험 보고구조가 있는 유일 조성이라 **200세대에서 조기 종료**. ⚠ **역으로 나머지 3조성은 400세대 소진 종료 = 수렴 확인 없이 끝났다** |
| **M20** | ⚠ **SI 가 본문 Figure 2 를 "Figure S2" 로 두 번 오인용**한다 — p 3 *"As shown in **Figure S2**, our CSP approach successfully identified … for 12 of the 14 systems"*, p 4 *"(green triangles in **Figure S2**)"*. Figure S2 는 **상도**다. 또 p 5 는 **eq 7 을 "equation (3)"** 이라 인용(eq 3 은 levM 정의) | SI p 3, 4, 5 | 소. 단 §5a 근거를 인용할 때 **Fig 2a(본문)** 로 적어야 한다 |
| **M21** | ⚠ **CSM 근거 ref 23 = Jun/Ceder, *Nat. Mater.* 2022, 21, 924** — **본문 ref 88 과 동일한, corner-sharing 우월을 주장하는 그 논문**이다. **SI 에서도 자기 결론을 반박하는 논문을 기술자의 권위로 쓴다**(§11-5 재확인). 🆕 그리고 **ref 22 = Lee & Ok, *Inorg. Chem.* 2013, 52, 5176 — "AGa(SeO₃)₂ (A = Li, Na, K, Cs)"** 로, **CSP 가 실패한 두 계 중 하나인 LiGa(SeO₃)₂ 의 원논문**이다 | SI refs 22, 23 | 인용 계보의 자기잠식. 우연이지만 기록해 둔다 |
| **M22** | ⚠ **Fig S8c 패널 라벨 오기 — "Li₄SiGe**S₃**"** (Li₄SiGeS₆ 여야 함) | Fig S8c | 소 |
| **M23** | ⚠ **Fig S2 는 진짜 4원계 convex-hull 단면이 아니다.** 삼각형 꼭짓점이 **Ge–S–Li**(우: Sn–S–Li)인데 **Si 계 상들(SiS₂·Si·LiSi·Li₁₃Si₄·Li₁₅Si₄·Li₂SiS₃)이 그 위에 겹쳐 찍혀 있다** — Si 가 Ge–Li 변 위에 놓인다 | Fig S2 | 초록 "stability domain" 은 **도식**이지 정량 근거가 아니다. §6 의 *"tie-line 위 1:1 지점"* 이라는 우리 해석은 **여전히 유효**(SiS₂ ↔ Li₄GeS₄ 붉은 선 + 중점 ★ 확인) |

### 20c. 재확인 통과 — 종전 판독이 맞았던 것

- **Table S1 14행 전수** ✓ (ID·공간군·Z·MAE_a·MAE_f·용도). **Li₃AuO₃ 와 Li₂BPt₃ 가 같은 mp-7471** 오기도 **실물 확인** ✓ (§11-11 유지)
- **Table S2 40값 전수** ✓ — 0/0/0/3/2/4/4/9/11/12 · 0/0/10/12/11/12/25/31/34/34 · 0/0/0/1/7/23/35/39/41/42 · 0/0/3/4/10/11/11/16/17/29 (meV/atom). **최대 42, 전원 50 meV 컷 통과** ✓
- **Fig S1 14 × 2 공간군 전수** ✓ (§5d 표와 완전 일치. **Li₃YCl₆ P-3m1 → P1** 포함 — "관대한 일치 판정" 근거 실물 확인)
- **Fig S4–S7 연결방식 라벨 40개 전수** ✓ — Li₂SiS₃ C,C,**E,E,E**,C,C,**E,E**,C / Li₂GeS₃ C,C,C,C,C,**E**,C,C,C,**E** / Li₄SiGeS₆ C,C,C,C,**E**,C,**C+E**,C,C,C / Li₄SiSnS₆ C,**E**,**C+E**,C,**E**,C,C,**C+E**,C,C → **§7b–7e 와 40/40 일치**
- **Fig S10 8값** ✓ (SiS₄ 5.12/4.98 · dead 5.68/4.98 · Li₄SiGeS₆ GeS₄ 5.97→5.67, SiS₄ 5.12→5.07 · dead 6.06/5.35). **Li₂SiS₃ edge 의 dead volume ≡ SiS₄ 부피 ≈ 4.98 동일** 도 실물 확인(§19-N8)
- **MAE_f 4값** 13.2 / 27.4 / 29.8 / 33.3 ✓ (§11-4 인용값 정확)
- **eq 1–4 (MTP)·eq 6–8 (D, Arrhenius, Nernst–Einstein)·F_vib·eq 9 (α)·eq 10–11 (CSM)** 서술 전부 ✓
- **σ 부재** ✓ — **SI 24 pp 어디에도 σ 수치·단위(mS/cm, S/cm)가 없다.** eq 8 은 방법 서술뿐 → §9-A 최종 확정
- **교차온도 360 / 480 / 280 / 없음** ✓, **SI 산문의 *"for Li₂SiS₃ and Li₂GeS₃ … above ~480 K"* 오기** ✓ (§11-10)
- **Li₄SiGeS₆ 영점에너지 서술** ✓ — *"the inclusion of zero-point energy slightly alters the relative stability at 0 K due to its smaller lattice volume and higher bond stiffness"*
- **>80 atom 한계 자백** ✓ — *"suggesting a limitation of our current framework for systems with large unit cells (>80 atoms) and complex coordination environments"* (§5b, 우리가 CSP 를 안 하는 외부 근거)
- **CSM 대상이 Li–S₄ 임** ✓ (Fig S12 캡션: *"CSM reflects the degree of distortion in the **Li–S₄** polyhedron"*) — MS₄ 가 아니다

### 20d. ★ MSD 원자료 전수 (Fig S4–S7) — 우리가 만든 표

**MSD_end** = Li MSD 의 궤적 끝값(Å²) · **D_calc** = MSD_end/(6·t_end), 1 Å²/ps = 10⁻⁴ cm²/s ·
**D_fig** = 우리 Fig 3 판독값(§7b–7e, ×10⁻⁵ cm²/s) · "진동" = 계단·기울기 없이 진폭만 (D ≈ 0)

| 조성 | rank | 연결 | MSD_end (Å²) | t_end | **D_calc** | **D_fig** | 궤적 성격 |
|---|---:|---|---:|---:|---:|---:|---|
| **Li₂SiS₃** | 1 | C | ~0.45 진폭 | 60 | ≈0 | 0.00 | 순수 진동 |
| | 2 | C | ~0.35 | 60 | ≈0 | 0.00 | 순수 진동 |
| | **3** | **E** | **68** | 60 | **1.89** | 1.75 | 준선형 ✅ |
| | 4 | E | 58 | 60 | 1.61 | 1.15 | 30–45 ps 정체 후 재상승 |
| | **5** | **E** | **72** (52 ps 78 최고) | 60 | **2.00** | 2.35 | ⚠ **끝에서 MSD 감소** |
| | 6 | C | ~0.45 | 60 | ≈0 | 0.00 | 순수 진동 |
| | 7 | C | ~0.50 | 60 | ≈0 | 0.00 | 순수 진동 |
| | 8 | E | 8.5 | 60 | 0.24 | 0.30 | 🔴 **22–30 ps 계단 1회 후 정체** |
| | 9 | E | 57 | 60 | 1.58 | 1.75 | 35–48 ps 정체 후 급상승 |
| | 10 | C | ~0.70 | 60 | ≈0 | 0.00 | 순수 진동 |
| **Li₂GeS₃** | 1–5 | C ×5 | 0.3–1.2 | 60 | ≈0 | 0.00 | 순수 진동 |
| | **6** | **E** | **15.5** | 60 | **0.43** | 0.72 | 🔴 **50–60 ps 에 8→15.5 (변위 절반이 최종 10 ps)** |
| | 7 | C | 13 | 60 | **0.36** | **0.04** ⚠ | 🔴 계단(22–32 ps) 후 정체. **9× 불일치 → Q7** |
| | 8 | C | ~0.35 | 60 | ≈0 | 0.00 | 순수 진동 |
| | 9 | C | ~0.70 | 60 | ≈0 | 0.01 | 순수 진동 |
| | **10** | **E** | **97** ★전체 최고 | 60 | **2.69** | 2.6 | 선형 ✅ **논문 전체 최고 D** |
| **Li₄SiGeS₆** | 1–4 | C ×4 | 0.3–0.6 | 60 | ≈0 | 0.00 | 순수 진동 |
| | **5** | **E** | **32** | 60 | **0.89** | 1.0 | 준선형 ✅ (유일 edge) |
| | 6 | C | 5.5 | 60 | 0.15 | 0.11 | 🔴 계단 2회(5 ps·22 ps) 후 정체 |
| | 7 | **C+E** | 3.5 | 60 | 0.10 | 0.02 | 🔴 **10 ps 도달 후 50 ps 완전 정체 = 초기 완화** |
| | **8** | **C** | **28** | 60 | **0.78** | 0.64 | ⚠ **corner 인데 edge(32)에 육박** |
| | 9 | C | 12 | 60 | 0.33 | 0.22 | 30 ps 이후 정체 |
| | 10 | C | 6 | 60 | 0.17 | 0.14 | 25 ps 이후 정체 |
| **Li₄SiSnS₆** | 1 | C | ~0.40 | 60 | ≈0 | 0.00 | 순수 진동 |
| | **2** | **E** | **58** | 60 | **1.61** | 1.5 | 선형 ✅ |
| | 3 | C+E | ~0.45 | 60 | ≈0 | 0.00 | 순수 진동 |
| | 4 | C | ~0.80 | 60 | ≈0 | 0.00 | 순수 진동 |
| | **5** | **E** | **14** | **~42** 🔴 | **0.56** | 0.65 | 🔴 **궤적 42 ps** + **12→16 ps MSD 감소** |
| | 6 | C | 11.5 | 60 | 0.32 | 0.25 | 30 ps 이후 정체 |
| | 7 | C | ~0.40 | 60 | ≈0 | 0.00 | 순수 진동 |
| | 8 | C+E | 2.5 | 60 | 0.07 | 0.03 | 🔴 22 ps 계단 후 정체 |
| | 9 | C | ~0.45 | 60 | ≈0 | 0.00 | 순수 진동 |
| | 10 | C | 11 | 60 | 0.31 | 0.19 | 50 ps 이후 가속 |

**읽는 법 3줄**

1. **살아남는 주장은 이분법뿐** — "순수 진동"(D ≈ 0)과 "준선형"(D ≳ 0.5×10⁻⁵) 사이에 **계단형/정체형이 대거 끼어 있고, 그 구간의 D 는 순위를 매길 양이 아니다.** §11-2 결론 유지·강화.
2. **D_calc ↔ D_fig 가 14 중 13에서 ±40 % 안** → Fig 3 의 D 는 **전 구간 원점통과 MSD/6t**. 우리 규율(2–50 ps **고정 창** + 다중 시간원점)과 정면으로 다르다.
3. **corner/edge 이분이 깨끗한 것은 Li₂SiS₃·Li₂GeS₃뿐.** Li₄SiGeS₆ 는 corner r8(28 Å²)이 유일 edge r5(32 Å²)와 **거의 같다**.

### 20e. ★ SI 가 시사하는 새 규칙 — **두 인자 결합(conjunction)**

Fig S12(α·Li–S₄ 부피·CSM) 를 Fig 3 의 D 와 rank 별로 겹쳐 읽으면, **논문이 한 번도 말하지 않은 패턴**이 나온다.
**CSM 단독으로도, Li–S₄ 부피 단독으로도 D 를 예측하지 못하고, 둘이 동시에 클 때만 Li 가 움직인다.**

| 조성 | rank | 연결 | Li–S₄ 부피 (Å³) | CSM (색) | D_fig | 판정 |
|---|---:|---|---|---|---:|---|
| **Li₂GeS₃** | 6 | E | **7.4–8.0** (최고) | 2.5–4 (적/주황) | 0.72 | 부피 高 ∧ CSM 中 → 中 |
| | **10** | **E** | 7.0–7.95 | **4.5–6** (황/백) | **2.6** ★ | **부피 高 ∧ CSM 高 → 최고** |
| | 7 | C | 6.4–7.55 (낮고 분산) | 5.5–6 (백) | 0.04 | **CSM 高 ∧ 부피 低 → ≈0** |
| | 9 | C | 7.2–7.5 | 백+적 혼재 | 0.01 | 경계 → ≈0 |
| | 1–5 | C | 7.35–7.75 | **1–2** (흑) | 0.00 | CSM 低 → 0 |
| **Li₄SiSnS₆** | 2 | E | 7.3–7.75 | 2–5 | 1.5 ★ | 둘 다 高 → 高 |
| | 5 | E | 7.35–8.05 | 3–5 | 0.65 | 둘 다 高 → 中 |
| | 6 | C | 7.2–8.05 | 3–5 (주황/황) | 0.25 | 둘 다 高 → **corner 인데 유한** |
| | 10 | C | 7.0–7.65 | 4–6 | 0.19 | 둘 다 高 → **corner 인데 유한** |
| | **9** | **C** | **5.0–5.7** (최저) | **~6** (전부 백, 최고) | **0.00** | 🔑 **CSM 최고인데 D = 0 — 부피가 없다** |
| | 4, 7 | C | 7.15–7.9 | **1–2** (흑) | 0.00 | 부피 高 ∧ CSM 低 → 0 |

> 🔑🔑 **Li₄SiSnS₆ rank 9 가 결정적이다.** 이 논문의 인과사슬은 `왜곡 ↑ → 지형 평탄 → Ea ↓ → D ↑` 인데,
> **CSM 이 가장 높은 구조가 D = 0** 이다. 차이는 **Li–S₄ 부피(5.0–5.7 vs 7+)**.
> → 경험 규칙: **D > 0 ⟺ (Li–S₄ 부피 ≳ 7 Å³) ∧ (CSM ≳ 3)**. 이 표본에서 **예외는 Li₄SiSnS₆ rank 3(mixed, 경계) 1건.**
>
> ⚠ **강도 표시**: 이건 **우리 판독이지 논문의 주장이 아니다.** 표본 ~20 구조·육안 색 판독·상관계수 없음.
> **가설로만 쓰고, 우리 47종에서 검증한 뒤에 주장한다.**
>
> ⭐ **우리 실행에 직결**: §10c 채택항목 **C(Li–(S,Cl)₄ 부피 + CSM 후처리)** 를 **두 지표를 따로 보는 상관분석이
> 아니라 결합 기준(둘 다 문턱 초과)으로 설계**해야 한다. 단일 지표 회귀는 rank 9 같은 표본에서 반드시 깨진다.
> §19-N5(“CSM 은 D 를 따라가고 연결방식은 안 따라간다”)의 **다음 단계**가 이것이다.

### 20f. 채택 / 실행 항목 — §15 에 추가

| # | 항목 | 근거 | 비용 | 우선 |
|---|---|---|---|---|
| **H** | **§15-C 재설계 — Li–(S,Cl)₄ 부피 × CSM 을 *결합 기준*으로.** 두 지표를 각각 D 와 회귀하지 말고 **(부피 문턱) ∧ (CSM 문턱)** 2차원 격자로 47종을 분류. 문턱은 우리 host 에서 새로 잡는다 | §20e | 소 (궤적 재사용) | **1** |
| **I** | **MSD 규율의 외부 정당화 사례로 §20d·M2 를 `kb/` 에 기록** — "문헌 최상위 저널의 AIMD 도 MSD 가 감소한다(단일 시간원점)". 우리 `tools/ionic/msd_refit_window.py`(다중 시간원점 + 2–50 ps 고정창) 방어 근거 | M2·M7 | 0 | **1** |
| **J** | **`ordered_vs_disordered.md` §9 의 $S_{vib}$ 사례를 M13 형태로 쓸 것** — "교차온도 280–480 K" 가 아니라 **"방향이 조성마다 다르다(2 유리 / 1 반대 / 1 없음)"**. 종전 §15-E 를 이 형태로 교체 | M13 | 소 | **2** |
| **K** | **T10(E_hull 합성가능성) 근거표 확보** — Table S2 40값 전수를 이 digest 에 전사 완료. 인용 가능 | 20c | 0 | 3 |
| ❌ | **α 재구현** | **M10 으로 확정** — SI 가 본문으로, 본문이 스키마로 떠넘긴다. 알고리즘이 문서 어디에도 없다 | — | **안 함** |
| ❌ | **이 논문의 D·MSD 파이프라인 이식** | M1(정의식 오류)·M2(감소)·M3(42 ps)·M4(계단에 D 부여) | — | **안 함** |

### 20g. 인용 규칙 — §16 에 추가

- ⛔ **인용 금지 (2026-08-04 SI 추가)**: **"AIMD 60 ps"를 4조성 40 구조 전체에 적용해 서술하지 말 것** —
  **Li₄SiSnS₆ rank 5(edge) 는 ~42 ps** 다(M3). 쓰려면 *"대부분 60 ps"*.
- ⛔ **인용 금지**: 이 논문의 **MSD 정의식(SI eq 5)** — 제곱의 차로 적혀 있다(M1).
- ⚠ **단서 필수**: **"2 자릿수"는 Li₂SiS₃·Li₂GeS₃ 한정.** 4원계(Li₄SiGeS₆·Li₄SiSnS₆)에서는 최고 corner 와
  최고 edge 가 **1.6–6배** 차이다(M6).
- ⚠ **단서 필수**: **"고온에서 edge 가 유리"는 4조성 중 2조성.** Li₄SiGeS₆ 는 **방향이 반대**(280 K 위에서 corner 우세),
  Li₄SiSnS₆ 는 **1000 K 까지 교차 없음**(M13).
- ⚠ **"예측 edge 상이 실험 준안정 edge 상과 RDF 로 일치한다"** → **"Si·S 쌍은 일치, Li 쌍은 불일치"** 로만(M17).
- ✅ **인용 가능 (신규)**: *"MLIP-CSP 로 예측된 준안정 edge 상은 진동 자유에너지를 넣으면 조성에 따라 상 순서가
  뒤집히며, Li₄SiGeS₆ 에서는 영점에너지만으로 0 K 상대안정성이 바뀐다[Kim 2025 SI, Fig S8]."*
- ✅ **인용 가능 (신규)**: *"논문 자신의 SI 는 SCAN 이 Li₃PS₄·LiAlCl₄·Na₃PS₄ 세 계의 오분류를 교정했다고
  적는다[Kim 2025 SI]"* — 본문의 *"SCAN 으로 검증됐다"* 대신 **이 문장을 쓴다**(M0).

### 20h. 열린 질문 갱신

| # | 질문 | 상태 |
|---|---|---|
| ~~Q3~~ | ~~V_dead 의 실제 알고리즘~~ | **닫힘(부정형).** SI 가 본문으로 떠넘기고 본문은 스키마뿐 → **문서상 존재하지 않는다.** figshare 원자료 확인 외 방법 없음 (M10) |
| **Q7** 🆕 | **Li₂GeS₃ rank 7 (corner)**: SI Fig S5 의 MSD 60 ps 끝값 13 Å² ⇒ D ≈ 0.36×10⁻⁵ 인데 우리 Fig 3c 판독은 0.04×10⁻⁵ — **9× 불일치** | 본문 실물 재확보 후 Fig 3c 를 700 dpi 재판독. 우리 판독 오류 / 논문 내부 불일치 둘 다 가능 |
| **Q8** 🆕 | **phonon supercell·q-mesh·허수모드** — 준안정상의 동역학적 안정성은 확인됐나 | 논문·SI 미보고 (M15). 저자 문의 외 방법 없음 |
| Q1 | 덱의 `0.0001 / 2.4 mS/cm` 출처 | **유지** — ref 36 = Huang, JACS 2022, 144, 4989 (SI ref 21 로도 확인) PDF 확보 필요 |
| Q6 | DFT query 총 횟수 / 학습셋 크기 | ~~**유지 (SI 에도 없음 확인).**~~ → **부분 종결 2026-08-26 · §21b** (학습셋 실측). **논문·SI 에 없다는 사실은 유지**, 값만 저장소로 확보. 세대 상한이 조성별로 다르다는 것(Li₂SiS₃ 200, 나머지 400 — M19)은 **학습셋 크기 비대칭과 정합**한다 |

> **총평 (SI 회차)**: 2026-07-28 의 SI 판독은 **표·공간군·연결방식·부피값에서 사실상 전수 정확**했다
> (Table S1 14행, Table S2 40값, Fig S1 28개 공간군, Fig S4–S7 연결방식 40개, Fig S10 8값 — 오류 0).
> 이번 회차가 새로 준 것은 **표의 값이 아니라 그림 안의 원자료**다 — **MSD 궤적 40개를 실제로 보니
> 이 논문의 D 절반가량이 확산이 아닌 것에 붙은 숫자**였고(M4·M5), **MSD 가 감소하고**(M2), **한 궤적은
> 42 ps**였다(M3). 동시에 SI 는 본문보다 정직해서, **SCAN 반전 3건을 이름까지 대고 인정**한다(M0) —
> 우리가 §19 에서 "본문이 자기 그림을 부인한다"고 적은 것의 **논문 자신에 의한 확증**이다.
> 그리고 §20e 의 **두 인자 결합 규칙**은, 우리가 47종에 CSM 을 얹을 때 **단일 회귀로 가면 안 되는 이유**를
> 미리 알려준 것이라 이번 회차에서 가장 실무적으로 값이 나간다.

---

## 21. 🗃 저자 데이터저장소(CSP_SSE) 실측 (2026-08-26, 3차)

**대상**: `db/external/kim2025_csp_sse/` — upstream `github.com/jhkimmmmm/CSP_SSE` @ `e4a6fd4`.
확보물: `mtp_provenance.json` · `mtp/*_pot.mtp` ×4 · `structures/<조성>/{1..10}_stable.cif` ×40 ·
`scripts/dynamics_Li_CSM.py` · `UPSTREAM_README.md`.

> ⛔ **LICENSE 가 없다.** 재배포 금지 · 우리 결과로 제시 금지 · **내부 분석 전용.**
> ⚠ **논문은 이 저장소를 밝히지 않는다** — Data Availability 는 figshare 만 적는다(§0.1 ASSOCIATED CONTENT).
> 그래서 이 저장소의 내용물은 **논문의 주장과 같은 지위가 아니다.** 어긋나는 곳은 그렇게 적었다.
>
> 🔑 **이 회차가 하는 일**: §19·§20 이 *"미보고 → 재현 불가"* 라고 닫아 둔 항목들을 **실물 파일로
> 다시 여는 것**이다. 3건이 닫혔고(**Q6 종결 · AIMD 셀 부분종결 · T14 참조구현 확보**),
> 1건이 새로 열렸다(**Q9**).

### 21a. 무엇이 들어 있고 무엇이 없나

| 있는 것 | 없는 것 (upstream 에도) |
|---|---|
| 조성별 **최종 MTP 퍼텐셜** `pot.mtp` ×4 | **중간 세대 퍼텐셜** — active learning 의 궤적을 볼 수 없다 |
| **10 most stable 구조 CIF** ×40 | **AIMD 궤적**(vasprun/XDATCAR) — MSD 재계산 불가 |
| **Li–S₄ 부피 + CSM 분석 스크립트** 1개 | **V_dead / packing ratio α 계산 코드** ⛔ (아래 21d) |
| `UPSTREAM_README.md` (디렉터리 규약) | **query 선별 로그 · extrapolation grade 기준값** |
| (upstream) train.cfg / valid.cfg 배열 수 | **DFT query 총 횟수** — 학습셋 최종 크기는 알지만 **몇 번 물어봤는지는 여전히 모른다** |

### 21b. ★ 학습셋 크기 실측 — **Q6 부분 종결**

> §4c 표의 *"**학습셋 최종 크기** ⛔ 미보고"* · §20h 의 *"Q6 DFT query 횟수 / 학습셋 크기 — 논문·SI 미보고"*
> → **✅ 종결 2026-08-26 · 데이터저장소 실측** (기존 문장은 지우지 않는다 — 논문 본문에 없다는 사실 자체는 유효)

| 조성 | train 배열 | valid 배열 | 합 | `species_count` | `min_dist` (Å) | `max_dist` (Å) |
|---|---:|---:|---:|---:|---:|---:|
| **Li₂SiS₃** | **863** | 96 | 959 | 3 | **1.0954** | **5.000** |
| **Li₂GeS₃** | **1,391** | 158 | 1,549 | 3 | **1.1310** | **5.000** |
| **Li₄SiGeS₆** | **1,038** | 110 | 1,148 | 4 | **1.1033** | **5.000** |
| **Li₄SiSnS₆** | **1,104** | 90 | 1,194 | 4 | **1.6873** | **5.000** |

공통: `potential_name = MTP1m` · `version = 1.1.0` · `radial_basis_type = **RBChebyshev**` ·
`radial_basis_size = 8` · `radial_funcs_count = 5` · `alpha_moments_count = 1352` ·
`alpha_index_basic_count = 295` · `alpha_scalar_moments = 288`.

**판정 4건**

1. ✅ **`max_dist = 5.000 Å` 는 본문 서술 `R_cut = 5 Å` 와 정확히 일치한다**(§2.1, §4e).
   **논문이 적은 MTP 하이퍼파라미터 중 파일로 검증 가능한 것은 이것 하나이고, 통과했다.**
   (`lev_max = 20` 은 `alpha_*` 필드로 간접 표현돼 있어 파일만으로는 역산 불가 — 미검증.)
2. ⚠ **학습셋이 생각보다 작다.** 조성당 **약 900–1,550 배열**이다. 이 안에는 melt-quench-anneal
   AIMD 스냅샷과 USPEX random 400 구조(§2.2)가 **이미 포함**돼 있으므로, **active learning 이
   추가한 query 는 많아야 수백 규모**다. → **"MLIP-CSP 가 DFT 비용을 없앤다"는 주장의 실제 규모가
   처음으로 숫자로 잡혔다.** ⚠ 단 **query 횟수 자체는 여전히 모른다**(완전 완화 1회 = 이온 스텝
   수십~수백 번의 DFT 이므로, 배열 수 ≠ DFT 호출 수).
3. 🔑 **학습셋 크기가 조성마다 1.6배 차이나고, MTP 정확도 순서와 맞지 않는다.**
   Li₂GeS₃ 가 **가장 큰 학습셋(1,391)인데 MAE_f 는 27.4**(두 번째로 나쁨), Li₂SiS₃ 는 **가장 작은
   학습셋(863)인데 MAE_f 13.2 로 압도적 1위**다(§20-R3). → **데이터를 더 넣어서 좋아진 게 아니다.**
   Li₂SiS₃ 만 **실험 구조가 있어 200세대에서 조기 종료**된 조성이라는 것(§20-M19)과 함께 읽으면,
   **"쉬운 계는 적은 데이터로 일찍 끝났고, 어려운 계는 데이터를 더 먹고도 못 맞혔다"** 가 된다.
4. 🆕⚠ **Li₄SiSnS₆ 의 `min_dist` 만 홀로 크다 — 1.687 Å vs 나머지 1.095–1.131 Å.**
   MTP 의 Chebyshev 반경기저는 `[min_dist, max_dist]` 위에 정의되므로, `min_dist` 는 사실상
   **"학습셋에서 관측된 최단 원자간 거리"** 다. 즉 **Li₄SiSnS₆ 의 학습셋에는 1.69 Å 보다 가까운
   접촉이 한 번도 없었다** — 다른 셋은 1.10 Å 까지 봤는데.
   → **그 계의 퍼텐셜은 근접 충돌 영역이 미학습**이고, 진화탐색은 무작위 조밀 구조를 계속 만들어
   낸다. **하필 그 조성이 MAE_a 최악(35.2)이고**(§20-R3), **40 궤적 중 유일하게 42 ps 짜리가 나온
   조성**이며(§20-M3), **mixed 위상이 가장 많이 나온 조성**이다(§7e).
   ⚠ **강도 표시: 이건 상관이지 인과가 아니다.** 우리 판독이고 논문의 주장이 아니다. 다만
   **"조성마다 전용 MTP 를 새로 학습"하는 전략의 품질이 조성마다 고르지 않다**는 직접 증거로는 쓸 수 있다.
   🔑 **우리 UMA 사전학습 횡단 전략을 방어할 때 이 비대칭이 유용하다**(§14 마지막 행).

### 21c. AIMD 셀 규약 — **§11-9 "재현 불가" 부분 종결**

`UPSTREAM_README.md` 원문:
> *"XXX.cif : The crystal structure used for ab initio molecular dynamics (AIMD) simulations.
> For each structure, **a supercell was generated to have a lattice dimension as close as possible
> to ~10 Å** to balance computational cost and accuracy."*

- ✅ **셀 크기 규약 확보 — "각 격자 방향을 ~10 Å 에 최대한 가깝게"**. 배포된 원 CIF 가
  **24 원자 / 460–544 Å³** 이므로(21e), ~10 Å 큐브(≈1000 Å³)로 맞추면 대략 **2배 = 40–50 원자**
  규모가 된다. → **ref 47(`jun2022_…`)의 "단위셀 ~52원자"와 같은 자릿수**이고, 본문의
  *"same computational guidelines … including cell size"*(§2.1)와 **정합**한다.
- ⛔ **여전히 재현 불가인 것**: **조성·rank 별 실제 supercell 배수**(2×1×1? 1×2×2?)는 적혀 있지
  않고, AIMD 용 CIF 자체는 `csp/<조성>/AIMD/` 에 있다는데 **우리가 확보한 범위에 없다**.
  → §11-9 는 **"셀 크기 규약은 알지만 구조별 셀은 모른다"** 로 격하. **완전 종결 아님.**
- 🆕 **AIMD 는 여러 번의 VASP 실행을 이어 붙여 만들었다.** `dynamics_Li_CSM.py` 가
  `run%03d/vasprun.xml(.gz)` 를 **범위로 받아 이어 붙인다**(21d) → **60 ps 는 연속 1회 실행이
  아니라 chained restart** 다. 논문·SI 어디에도 없는 사실이고, **§20-M2(MSD 감소)·M3(42 ps)**
  같은 이상을 이해하는 데 직접 관련된다 — **이어 붙이는 지점에서 시간원점 처리가 어떻게 됐는지
  알 수 없다.**

### 21d. ★★ `dynamics_Li_CSM.py` 정독 — **T14 의 참조 구현**

> **T14** = *"Li–(S,Cl)₄ CSM 을 기존 UMA-MD 궤적에 후처리, 구현은 pymatgen chemenv 또는
> SI eq 10 직접(≈30줄)"*. → **이제 그들의 실제 스크립트가 있다. 둘 중 어느 쪽인지 확정됐다.**

**입력·출력**

| | |
|---|---|
| 입력 | `run<start>..<final>/vasprun.xml(.gz)` — **여러 AIMD 실행을 이어 붙인 구조열** |
| 출력 | `csm_ave.csv` · `vol_ave.csv` — **Li 자리 하나당 값 하나씩** (프레임 평균) |
| 의존 | pymatgen(`Vasprun`, `chemenv`), scipy(`ConvexHull`), pandas, tqdm |

**알고리즘 5단계 (실제 코드 흐름)**

1. **Li 를 뺀 S-only 껍질을 만든다** — `non_elements()` 는 **S 를 제외한 모든 원소를 제거**한다
   (Li 도, Si/Ge/Sn 도). → **"Li–S₄"의 S 는 문자 그대로 S 뿐**이고, Li–Li·Li–M 이웃은 **정의상 배제**된다.
2. **문제의 Li 하나를 그 껍질에 도로 꽂는다** — `site_env()` 가 해당 Li 를 프랙셔널 좌표로
   `append` 하고 `get_sorted_structure()` 로 정렬(전기음성도 순 ⇒ Li 가 index 0).
3. **반경을 1.0 → 4.0 Å 로 701 스텝(0.0043 Å 간격) 키우며 이웃 S 를 센다** —
   `<4` 면 계속 키우고, **정확히 4 면 확정**, **5 면 앞 4개만 취하고**, **>5 면 루프를 깬다**.
4. **CSM** = `LocalGeometryFinder().get_coordination_symmetry_measures()['**T:4**']['csm']`
   → ★ **pymatgen chemenv 의 "이상적 사면체(T:4)" CSM 이다.** SI eq 10–11 을 손으로 구현한 게 아니다.
5. **Li–S₄ 부피** = `ConvexHull(neigh_coords).volume` — **이웃 S 4개의 데카르트 좌표로 만든
   사면체 부피**(주기 이미지 좌표를 쓰므로 PBC 는 올바르게 처리된다).
6. **프레임은 `j % 50 == 0` 로 50개마다 하나만** 쓴다. **Li 자리별로 모아 산술평균** → CSV.

> 🔑 **이걸로 Fig. 5 의 정체가 확정된다.** Fig. 5 의 **원 하나 = Li 자리 하나의 궤적 평균**이고,
> 세로 산포는 **시간 산포가 아니라 Li 자리 간 산포**다. §20e 의 결합 규칙("어떤 Li 자리가 두 조건을
> 동시에 만족하는가")을 **자리 단위로 읽는 것이 옳았다는 뜻** — 우리 해석이 코드로 뒷받침됐다.

**⛔ V_dead / packing ratio α 는 이 스크립트에 없다 — Q3 는 그대로 닫힌 채다**

- 스크립트 전체에 `dead`·`packing`·`alpha` 어떤 이름도 없고, 계산하는 양은 **CSM 과 사면체 부피 둘뿐**이다.
- `UPSTREAM_README.md` 도 이 디렉터리를 **`Li-S4_volume_CSM`** 이라 이름 붙이고 산출물을
  *"XX-cms.csv"* 하나로만 적는다. **α 를 만드는 코드는 저장소에도 없다.**
- → **§20-M10 의 "순환 위임" 판정 유지 + 강화**: 이제 **문서에도 없고 코드에도 없다.**
  **Q3 는 부정형으로 닫힌 채 두고**, §10c 의 **"α 재구현 금지"** 는 최종 확정한다.
- 🔧 **단 §19-N8·§20-M12 를 §0.1(Fig. 4d 판독)과 합치면 힌트는 있다** — Fig. 4d 스키마는
  **"이웃한 S 들이 이루는 볼록 다면체"** 를 그린다. 즉 **`ConvexHull` 계열의 기하 구성**일
  개연성이 높다(같은 스크립트가 Li–S₄ 에 이미 `ConvexHull` 을 쓴다). ⚠ **그러나 어느 S 를
  꼭짓점으로 고르는지의 규칙이 없어 여전히 재현 불가**다. → Q3 상태는 *"부정형 종결"* 유지,
  기술만 *"알고리즘 부재"* → *"알고리즘 부재 + 볼록다면체 계열로 추정"* 으로 정밀화.

**⚠ 코드 결함 5건 (우리가 이식할 때 고쳐야 할 것)**

| # | 결함 | 왜 문제인가 |
|---|---|---|
| **C1** | **5-이웃일 때 `neigh[:4]`** — pymatgen `get_neighbors` 는 **거리순이 아니다.** 즉 **가장 가까운 4개가 아니라 리스트 앞 4개**를 쓴다 | 5배위 경계 자리에서 **어느 S 4개를 잡는지가 임의**가 된다. Sn 계처럼 5번째 S 가 0.05 Å 밖에 안 떨어진 경우(21e) **결과가 흔들린다** |
| **C2** | **`>5` 에서 `break` 하면 `lists` 가 빈 채 반환** → 호출부 `tmp_lists[0]` 에서 IndexError | 조밀한 프레임에서 **조용히 죽는 게 아니라 시끄럽게 죽는다** — 다행이지만 그 자리는 통계에서 빠진다 |
| **C3** | **chemenv 예외 경로에서 `csm_value`/`site_volume` 가 초기화되지 않는다** — `except` 가 print 만 하고 **직전 자리의 값을 그대로 append** | 🔴 **가장 위험하다.** "사면체로 인식 못 하는 자리"의 값이 **이전 자리 값으로 대체**돼 조용히 섞인다. 로그를 안 보면 알 수 없다 |
| **C4** | **`with_li.sites[0]` 가 Li 라고 가정**(정렬이 전기음성도 순이라 우연히 맞음) | pymatgen 정렬 규칙이 바뀌면 **말없이 엉뚱한 원자**를 중심으로 잡는다 |
| **C5** | `LocalGeometryFinder()` 를 **최내곽 루프에서 매번 새로 만든다**(자리 × 반경스텝마다) | 정확도 문제는 아니고 **매우 느리다**. 우리 200 ps 궤적에 그대로 쓰면 못 끝난다 |

**T14 재정의 (§15 에 항목 L 로 추가)**

- ✅ **채택**: `chemenv` 의 **`T:4` CSM** + **4-이웃 `ConvexHull` 부피** — **그들과 같은 양**을 낸다.
  SI eq 10–11 직접 구현은 **하지 않는다**(그들도 안 했다).
- 🔧 **우리 host 용 변형 1줄**: `non_elements()` 에서 **S 뿐 아니라 Cl 도 남긴다** → **Li–(S,Cl)₄**.
  ⚠ 그러면 배위 다면체가 이종 음이온 혼합이 되므로 **`T:4` CSM 은 여전히 정의되지만
  "이상적 사면체" 기준이 물리적으로 같은 뜻인지는 우리가 따로 논증해야 한다.**
- 🔧 **반드시 고칠 것**: C1(거리순 정렬 후 4개) · C3(예외 자리는 **버리고 카운트**) · C5(finder 재사용).
- 🔧 **입력 어댑터**: `Vasprun` 대신 **우리 UMA/ASE 궤적 리더**. 나머지 로직은 그대로 쓸 수 있다.
- ⚠ **프레임 간격**: 그들은 `%50`. 우리 MSD 규율(**2–50 ps 창**)과 맞추려면 **창 안에서만 표본**해야
  하고, 간격은 우리 dt(2 fs)와 저장 간격에 맞춰 새로 정한다 — **그들 숫자를 그대로 옮기지 않는다.**

### 21e. ★ 배포 구조 40개 독립 검증 — 연결방식·공간군·부피

**방법**(재현 스크립트는 일회용, `tools/` 에 남기지 않았다): CIF 를 직접 파싱(두 포맷이 섞여 있어
대칭연산을 적용해 전개) → 각 M(Si/Ge/Sn) 의 **최근접 S 4개**를 **주기 이미지까지 구분해** 잡고,
두 다면체가 **같은 이미지의 같은 S** 를 몇 개 공유하는지 센다(1=corner, 2=edge, 둘 다=mixed).
교차검증으로 **기준 없는 지표인 최근접 M–M 거리**를 따로 쟀다.

**결과 1 — M–M 거리가 완벽하게 이분된다**

| | 최근접 M–M (Å) |
|---|---|
| **edge-sharing 로 판정된 구조** | **2.96 – 3.28** |
| **corner-sharing 로 판정된 구조** | **3.46 – 4.01** |

→ **경계에 아무것도 없다(3.28 | 3.46).** 이 논문의 중심 분류축은 **컷오프 선택에 의존하지 않는
견고한 축**임이 독립적으로 확인된다. 그리고 이 양이 곧 **Fig. 4e 의 d_c > d_e** 다 — 논문이
스키마로만 그린 것을 **우리가 처음으로 수치화**했다.

**결과 2 — 논문 라벨과 36/40 일치**

| 조성 | 일치 | 불일치 |
|---|---|---|
| Li₂SiS₃ | **10/10** ✅ | — |
| Li₄SiGeS₆ | **10/10** ✅ | — |
| Li₄SiSnS₆ | **9/10** | #8 (우리 E vs 논문 C+E) — ⚠ **우리 쪽이 불확실**: 5번째 S 가 4번째보다 **0.05 Å** 밖에 안 멀어 Sn 이 사실상 5배위다. **논문 판정이 맞을 수 있다**(#3 도 gap 0.11 Å 로 같은 사정) |
| **Li₂GeS₃** | **7/10** | **#6 · #7 · #10 — 여기는 애매하지 않다** |

**결과 3 — 🆕 Li₂GeS₃ 3건은 판정이 명확한데 어긋난다 → Q9 신설**

| rank | 배포 CIF 공간군 | 최근접 M–M | 4↔5번째 S 간격 | **우리 판정** | **논문(Fig. 3c·S5)** |
|---:|---|---:|---:|---|---|
| **6** | P-1 | **3.77 Å** | 1.84 Å | **corner** (corner 링크 4, edge 0) | **edge** |
| **7** | **C2/m** | **3.23 Å** | 1.98 Å | **edge** (Ge₂S₆ 이량체 2쌍) | **corner** |
| **10** | P2₁2₁2₁ | **3.81 Å** | 2.11 Å | **corner** (corner 링크 4, edge 0) | **edge** |

- **4↔5번째 S 간격이 1.8–2.1 Å** 이므로 GeS₄ 껍질은 **전혀 애매하지 않다**. 컷오프를 어떻게 잡아도
  판정이 안 바뀐다.
- **정리하면: 배포된 Li₂GeS₃ 10개 중 edge-sharing 은 #7 하나뿐이고, Fig. 3c 는 두 개(6·10)를 요구한다.**
  **개수 자체가 안 맞으므로 단순한 순서 뒤바뀜으로는 설명되지 않는다.**
- **읽기 2가지, 우리는 어느 쪽인지 판정 못 한다**:
  (i) **배포 폴더의 번호가 Fig. 3c 랭킹과 다르다** — 그러면 6↔7 만 바꾸면 2건이 맞지만 **#10 은 여전히 안 맞는다**.
  (ii) **Fig. 3c/S5 의 Li₂GeS₃ 연결방식 마커가 잘못 배정됐다** — 그러면 이 조성의 결론이 **뒤집힌다**
  (가장 빠른 두 구조 D 2.6·0.72 가 corner 이 되고, 유일한 edge 가 D 0.04–0.36 이 된다).
- 🔑 **하필 여기가 Q7 자리다.** 40 궤적 중 **D 판독이 9× 어긋나는 유일한 표본이 바로 Li₂GeS₃ rank 7**
  이다(§20-M7·Q7). 배포 CIF 는 그 rank 7 을 **edge** 라고 말한다 — edge 라면 MSD 13 Å²(D≈0.36)가
  자연스럽고 Fig. 3c 의 0.04 쪽이 이상해진다. ⚠ **정황일 뿐 증거가 아니다.**
- ⚠ **강도 표시**: **사실**은 "배포 CIF 3개의 연결방식이 그림과 다르다"까지다. **"논문이 틀렸다"는
  주장이 아니다.** 저장소는 논문이 밝히지도 않은 비공식 자료다.
- ✅ **그래도 확정되는 실무 결론 하나**: **배포 CIF 로 이 논문의 Li₂GeS₃ 결과를 재현하려 하면
  Fig. 3c 와 대응이 안 맞는다.** 다른 3조성은 안전하다.

**결과 4 — 🆕 40개 예측 폴리모프의 공간군 (논문이 어디에도 안 적은 것)**

CIF 두 포맷 중 **Materials Studio 로 저장된 것만 진짜 공간군을 갖는다.** 나머지는 pymatgen 이
`P 1` 로 쓴 것이라 **"대칭이 없다"가 아니라 "대칭을 안 적었다"** 이다 — 혼동 금지.

| 조성 | 공간군이 실제로 적힌 구조 |
|---|---|
| **Li₂GeS₃** (10/10 전부) | 1 **Cmc2₁**(#36, = 실험 보고 corner 상 ✓) · 2 Cc(#9) · 3 Pnma(#62) · 4 P1 · 5 P2₁/c(#14) · 6 P-1(#2) · **7 C2/m(#12)** · 8 Abm2(#39) · 9 P1 · 10 P2₁2₁2₁(#19) |
| **Li₄SiGeS₆** | 5 **Cm**(#8) — **유일한 edge 상**이 여기다 |
| **Li₄SiSnS₆** | 2 **P2/m**(#10) — edge 상 |
| **Li₂SiS₃** | 전부 `P 1` 표기(= 미기재) |

→ ✅ **Li₂GeS₃ rank 1 = Cmc2₁ 는 실험 보고 구조와 일치**한다. 논문의
*"all reported Li₂GeS₃ structures … limited to corner-sharing"*(§0.1 §3.2¶5후반)과도 정합.
**배포 폴더의 rank 1 앵커는 신뢰할 수 있다** — 그래서 위 Q9 가 더 이상해진다.

**결과 5 — 🆕 셀 부피/원자 (edge 상이 오히려 "성기다")**

40개 CIF 전부 **24 원자**(Li₈M₄S₁₂, Z=4)로 통일돼 있어 직접 비교가 된다.

| 조성 | corner 평균 V/atom (Å³) | **edge 평균 V/atom** | mixed |
|---|---:|---:|---:|
| Li₂SiS₃ | 20.27 (n=5) | **21.43** (n=5) | — |
| Li₂GeS₃ | 21.15 (n=8) | **21.40** (n=2) | — |
| Li₄SiGeS₆ | 20.83 (n=8) | **21.60** (n=1) | 21.13 (n=1) |
| Li₄SiSnS₆ | 21.15 (n=6) | **22.42** (n=2) | 21.17 (n=2) |

🔑 **4조성 모두 edge 상의 셀이 더 크다(+1.2 ~ +6 %).** 논문은 edge 에서 **다면체가 압축되고
dead volume 이 준다**고 했는데(§8c), **셀 전체는 오히려 팽창한다.** 두 진술은 모순이 아니라
**같은 이야기의 두 항**이다 — α = (V_다면체 + V_dead)/V_셀 에서 **분자가 줄고 분모가 커지므로
α 가 양쪽에서 내려간다.**
→ ⭐ **논문이 한 번도 말하지 않은, 그러나 논문 주장을 강화하는 관찰**이다.
⚠ 단 **이건 0 K DFT 셀이고 α 는 600 K AIMD 평균**이라 직접 대입은 안 된다. **방향만 인용한다.**

### 21f. 열린 질문 갱신 (3차)

| # | 질문 | 상태 |
|---|---|---|
| ~~Q6~~ ✅ | ~~DFT query 총 횟수 / 학습셋 크기~~ | **부분 종결 2026-08-26 · 데이터저장소 실측.** 학습셋 = **863/1,391/1,038/1,104 (train)** + 96/158/110/90 (valid) → §21b. ⚠ **DFT query 횟수는 여전히 미보고** (배열 수 ≠ 호출 수) |
| ~~Q3~~ ⛔ | ~~V_dead 알고리즘~~ | **부정형 종결 유지 + 강화** — 문서(§20-M10)에 이어 **코드에도 없다**(§21d). 기술만 정밀화: *"알고리즘 부재"* → *"부재 + Fig. 4d 스키마상 볼록다면체 계열로 추정"* |
| **Q9** 🆕 | **배포 CIF 의 Li₂GeS₃ 연결방식이 Fig. 3c·S5 와 3건 어긋난다** (#6·#10 은 corner, #7 은 edge). 배포 번호가 랭킹과 다른 것인가, 그림 마커가 잘못 배정된 것인가 | **우리는 판정 못 한다.** figshare 원자료(AIMD 입력 CIF)를 받아 Fig. S5 썸네일과 대조하거나 저자 문의. ⚠ 그 전까지 **배포 CIF 로 Li₂GeS₃ 를 재현하지 말 것** |
| **Q10** 🆕 | **Li₄SiSnS₆ 의 `min_dist` 만 1.687 Å 인 것이 그 조성의 MTP 품질 저하(MAE_a 35.2)·42 ps 궤적과 관련 있나** | 중간 세대 퍼텐셜·train.cfg 원본 필요. 우선순위 낮음 — **가설로만 보유** |
| Q7 | Li₂GeS₃ rank 7 의 D 9× 불일치 | **유지, 그러나 Q9 와 얽혔다** — 배포 CIF 는 rank 7 을 edge 라 말하고, edge 라면 MSD 13 Å²(D≈0.36)가 자연스럽다. **두 질문을 같이 닫아야 한다** |
| Q1 · Q4 · Q5 · Q8 | 덱 σ 출처 · SCAN 하 순위 · Jun 2022 충돌 · phonon 허수모드 | **변동 없음** |

### 21g. 채택 / 실행 항목 — §15 에 추가

| # | 항목 | 근거 | 비용 | 우선 |
|---|---|---|---|---|
| **L** | **T14 를 저자 구현에 맞춰 확정** — `chemenv` **`T:4` CSM** + 4-이웃 **`ConvexHull` 부피**, 입력만 우리 궤적 리더로 교체. **결함 C1·C3·C5 는 고쳐서 이식**(§21d) | §21d | 소 | **1** |
| **M** | **§21e 의 M–M 거리 이분(2.96–3.28 vs 3.46–4.01 Å)을 T13(④′ 도펀트–PS₄ 연결방식)의 문턱 근거로 쓴다** — 우리 계는 M 이 P·도펀트 양이온이라 값은 다르겠지만, **"공유 음이온 수 세기"보다 "중심–중심 거리"가 컷오프에 덜 민감**하다는 것이 확인됐다 | §21e | 소 | 2 |
| **N** | **`db/external/kim2025_csp_sse/` 에 LICENSE 부재 경고를 README 로 박아 둔다** — 6개월 뒤 누가 이 CIF 를 그림에 쓰는 사고 방지 | §21a | 0 | **1** |
| ❌ | **배포 CIF 를 Li₂GeS₃ 재현에 사용** | **Q9** — Fig. 3c 와 대응이 안 맞는다 | — | **안 함** |
| ❌ | **α 재구현** | **최종 확정** — 문서에도 코드에도 없다 | — | **안 함** |

> **총평 (저장소 회차)**: 이 회차는 **새 물리를 준 게 아니라, 우리가 "미보고라서 못 한다"고
> 닫아 둔 칸 몇 개를 실물로 열었다.** 가장 값나가는 것은 **`dynamics_Li_CSM.py`** 다 — T14 가
> *"chemenv 로 할까 eq 10 을 손으로 짤까"* 에서 **"그들이 부른 바로 그 함수(`T:4`)를 부르면 된다"**
> 로 확정됐고, 덤으로 **Fig. 5 의 원 하나가 Li 자리 하나**라는 것이 확인돼 §20e 의 결합 규칙 해석이
> 코드로 뒷받침됐다. 반대로 **α 는 이제 변명의 여지 없이 닫혔다** — 문서에도 없고 코드에도 없다.
> 그리고 **Li₂GeS₃ 3건의 어긋남(Q9)** 은, 이 논문에서 우리가 제일 자주 인용하는 *"2자릿수"* 가
> 걸린 두 조성 중 하나에 붙은 것이라 **가볍게 넘길 수 없다** — 다만 **저장소는 논문이 밝히지도
> 않은 비공식 자료**이므로, 우리 판정은 *"논문이 틀렸다"* 가 아니라
> *"이 조성은 배포 자료로 재현하지 말라"* 까지다.
