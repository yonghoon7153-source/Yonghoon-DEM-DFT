# SDCP 통합 마스터 문서
**Self-Doped Conducting Polymer 전도성 바인더 — 물질·계면화학·매뉴스크립트·모델·로드맵 단일 레퍼런스**
(2026-07-10 작성. 세부 원본: `docs/sdcp_manuscript_anchors.md`, `litdb/papers/kang2025_*.md`,
`litdb/papers/han2025_*.md`, backlog A4/A4′ 행. 상태 표기: ✅앵커 / 🔶INTERIM / ⚠proxy / ❌무효)

---

## 0. 한눈 요약

**SDCP** = 자가도핑 전도성 고분자 (S-PEDOT계: EDOT 백본 + ether-링크 methyl-분지 alkyl-술폰산 side chain).
**용도**: dry-process ASSB 양극(NCM+LPSCl)에서 PTFE의 3약점(전자절연·분산불량·약접착)을 보완하는
**전도성 바인더** — 매뉴스크립트 체계는 **SBE**(PTFE-only) vs **DBE**(PTFE+SDCP dual) + C-SUS(집전체 코팅).
**우리 기여(계획)**: 3D 미세구조 모델(MPM particle seeding + 전기 연결성 econn) → **Fig 4(e)
"Electrochemical modeling" 빈 패널 후보** + STEP3 σ 정량.

현재 상태 한 줄: **전극-수준 앵커 확보 ✅ / 분자-수준 E_bind 재계산 중 ❌→재작업 / 모델 구현 완료·비교셋
런 대기 (SBE/DBE 조성 필요)**.

---

## 1. 물질 — SDCP는 무엇인가

### 1.1 분자 구조 (★2026-07-10 정정)
```
monomer (neutral): C₁₁H₁₆O₆S₂
side chain:  ring–CH₂–O–CH₂CH₂–CH(CH₃)–SO₃H
             (EDOT-MeOH + methyl-sultone 개환, 매뉴스크립트 S4-S5)
```
- ❌ **이전 DFT 모델은 오분자였음**: 곧은-pentyl C₁₁H₁₅O₅S₂ (말단 1차 술폰산, ether 없음)
- 정정의 물리적 의미: ① **ether –O– 링커** = 표면 Li⁺ 배위 채널 + PEO형 Li⁺ 호핑 사이트(§3.6)
  ② **methyl-분지 2차 술폰산** = anchoring head 입체/전자환경 변화 ③ footprint/배좌 상이
- 자가도핑: backbone 산화(polaron •⁺) + −SO₃⁻ counter-ion이 **같은 분자 안** → 별도 도판트 불요.
  실제 폴리머는 [EDOT•⁺–SO₃⁻]/[EDOT–SO₃H] **혼합 상태** (도핑 레벨 <100%)

### 1.2 물성 표 (상태 구분)
| 물성 | 값 | 출처 | 상태 |
|---|---|---|---|
| **형상 (전극 내)** | **0.2–0.5 µm 분산 입자** (as-made ~3µm → 밀링) | 매뉴스크립트 S2/S3 | ✅ 앵커 |
| **E (탄성계수)** | **23.6 GPa** (PTFE 실측 5.6; long-tail ~100) | AFM 모듈러스맵 Fig2d/S6 | ✅ 앵커 — LPSCl급 강성, "soft binder" 아님 |
| σ_ion (LPSCl+SDCP pellet) | 3.57→**2.86 mS/cm (×0.80)**; PTFE는 ×0.27 | Fig2f | ✅ 앵커 (이온 저차단) |
| σ_e (LPSCl+SDCP pellet) | 0.30→**1.53 ×10⁻⁷ S/cm (×5.1)**; PTFE ×0.4 | Fig2g/S10 | ✅ 앵커 (e-부스팅) |
| ρ (밀도) | 1.3 g/cm³ | generic PEDOT | ⚠ proxy — methods 확인 대기 |
| σ_e (SDCP 필름 단독) | ~~315–1089 S/cm~~ | 웹서치 S-PEDOT | ❌ 폐기 (오귀속 위험 — 실측 필요) |
| σ_y (항복) | 1.0 GPa | rigid-proxy | ⚠ §F1 hook (미앵커; 강성 공액고분자, PTFE식 유동 없음 가정) |
| 열/구조 | XRD 무변화(S8), Raman/FTIR PEDOT+SO₃H(2b/S7) | | ✅ |

---

## 2. 계면 화학 (DFT/MLIP) — 히스토리와 현재 상태

### 2.1 계산 히스토리 (정직 기록)
| 단계 | 값 (doped/neutral) | 판정 |
|---|---|---|
| Phase B (bare-anion ref) | −18.17 / −6.33 eV | ❌ reference bookkeeping 과대 (진공 음이온 = 비차폐 고에너지 기준) |
| 정합-ref MLIP 재계산 (uma-s-1p1, E_slab 공유, doped=중성 radical) | **−4.797 / −3.020 eV** (Δ1.78) | ❌ **오분자로 계산됨** (2026-07-10 무효화) |
| CIF 기하 (당시): O–Li 1.83Å×2 삽입 / 2.03Å×1 부유, footprint 82.5/116.5Ų → γ 0.93/0.42 J/m² | | ❌ 동반 무효 |
| **살아남은 것** | **방향: doped ≫ neutral** | 🔶 개연 유지 — 술폰산 head 화학 + bollard 사다리(§5.1) 외부 지지. **수치는 백지** |

### 2.2 재계산 스펙 (확정)
1. **올바른 monomer**: C₁₁H₁₆O₆S₂ (neutral); doped = 중성 radical (charge 0, doublet, 술폰산 H 제거)
2. **동일-세팅 references**: E_slab 공유(양쪽 동일), 분자 ref 같은 세팅 — anion-pathology 회피 유지
3. **시작 배향에 신규 계열 포함**: sulfonate-down(기존) + **ether-O-down** + **sulfonate+ether chelation**(집게)
4. PBC-aware로 neutral 산성 H의 O–H 온전성 확인 (relax 중 격자 O 전이 여부)
5. MLIP 수렴 후 **DFT U-ramp 교차검증** (dipole corr + U + 자성, complex/slab/분자 3계산 동일 세팅)
6. footprint 재측정 → **γ = E_bind/footprint 재산출** → coh 앵커 갱신
7. (권고, 3역할 완성용) **Li⁺ 패키지**: Li⁺ 결합에너지 @SO₃⁻ 사이트 vs @ether-O 사이트 + 인접 사이트 간
   NEB 이동장벽 — "Li-hopping 역할"의 정량 근거
- **재사용 가능**: LiNiO₂(104) slab relaxation / U-ramp E_slab 작업은 **분자-무관 → 전부 유효**

---

## 3. 메커니즘 스토리 Q&A — 답변 전문 + 구조 정정 후 생존 판정 (2026-07-10)

사용자가 스크린샷으로 먹여준 질문들에 대한 답변 원문 요지와, monomer 정정
(C₁₁H₁₅O₅S₂ 곧은-pentyl → **C₁₁H₁₆O₆S₂ ether-링크 methyl-분지**) 이후의 생존 판정.

**한눈 인덱스**: 3.1 ✅ · 3.2 ✅보강 · 3.3 ✅+④추가 · 3.4 ✅ · 3.5 ✅ · 3.6 ✅+②보강 · 3.7 ✅개연(강)
— **7개 전부 생존**. 무효화된 것은 E_bind/γ **수치**(§2)뿐, 화학 스토리는 전부 head(–SO₃H/–SO₃⁻)
국소 화학이라 링커 정정의 영향을 받지 않거나 오히려 강화됨.

### 3.1 "산-염기 H⁺ transfer로 표면 OH가 생긴다?" → ✅ 유지
**답변 요지**: 술폰산(–SO₃H)은 pKa ≈ −1~−2의 강산이고, NCM 표면 격자 산소는 염기성 사이트다.
접촉 시 H⁺가 표면 O로 이동하면 ① 분자 쪽은 –SO₃⁻가 되어 표면 금속(Li⁺/Ni)과 이온성 anchoring,
② 표면 쪽은 O–H(surface hydroxyl)가 생긴다. 즉 "앵커링 자체가 표면 OH를 부산물로 만든다"는
스토리는 산-염기 화학으로 자연스럽다.
**캐비엇(원답 그대로)**: 생성량은 계면 단분자층 수준으로 극소 — 벌크 물성을 바꿀 양이 아니고,
공기 노출 NCM 표면엔 이미 OH/Li₂CO₃가 존재하므로 "SDCP가 표면 OH의 주요 공급원"이라고 주장하면
과대. DFT로 H-transfer 전후 에너지 비교가 가능한 검증 항목.
**정정 후**: head 국소 화학이라 불변. 산도에 대한 치환기 효과는 α-methyl(+I, 산도↓)과
β-ether(−I, 산도↑)가 상쇄 방향 → 강산성 결론 유지.

### 3.2 "자가도핑(self-doping)이 실제 상태라는 근거는?" → ✅ 유지 + 보강
**답변 요지**: doped 상태가 참조용 가정이 아니라 실물의 기본 상태라는 실험 근거 3종 —
① Raman: –SO₃⁻ 대칭 신축(~1060 cm⁻¹)과 polaron성 C=C 밴드 공존, ② 외부 도판트 없이 전도성
발현(자가도핑 정의 그 자체), ③ UV-Vis polaron 흡수. 따라서 실제 폴리머는
[EDOT•⁺–SO₃⁻]/[EDOT–SO₃H] 혼합 상태(도핑 레벨 <100%)이고, 계산에서 doped/neutral을 나눠 보는
것은 이 실재 혼합의 양 끝을 잡는 것.
**정정 후**: 오히려 **보강** — 이 근거들은 전부 실물(= ether 포함 진짜 분자)에 대한 실험이므로
오분자 이슈와 무관하게 성립. ⚠ 단, 내가 돌린 시뮬레이션 Raman은 오분자 기반 → 재계산 필요하고,
정정 구조의 ether C–O–C 신축(~1100 cm⁻¹)이 1060 영역과 겹칠 수 있어 피크 배정 재확인 항목.

### 3.3 "NCM에 어떻게 앵커링되나 (시나리오)" → ✅ 유지 + ④ 신규
**답변 요지(원답 3종)**:
① **H-transfer 경로**: 3.1의 산-염기 반응 후 –SO₃⁻ ↔ 표면 Li⁺/Ni 이온성 결합
② **직접 배위**: 탈양성자 없이/이미 도핑된 unit의 –SO₃⁻ 산소가 표면 Ni(d⁷, Lewis acid)에 배위
③ **bidentate 브리징(가장 현실적)**: –SO₃⁻의 산소 2개가 표면 금속 사이트 2곳에 다리 걸침 —
   단좌보다 결합 강하고 술폰산-산화물 계면의 표준 모티프
**정정 후**: ①②③ 전부 head 화학이라 유지 + 정정 구조가 **④ ether-보조 chelation**을 추가로
연다 — side chain의 ether O가 sulfonate와 함께 집게(pincer)처럼 표면 Li⁺를 물 수 있는 기하.
④는 §2.2 재계산 시작 배향 계열에 포함됨 (sulfonate-down / ether-O-down / chelation).

### 3.4 "SO₃H와 SO₃⁻ 둘 다 안정하다는 게 말이 되나?" → ✅ 유지
**답변 요지**: 둘 다 각자의 환경에서 안정한 local minimum이다 — 고립/건조 상태의 –SO₃H는
자발 해리하지 않고, 도핑 상태의 –SO₃⁻는 backbone polaron이 상쇄 전하를 제공해 안정.
전환에는 trigger가 필요하다: (a) 산화 중합/도핑 이벤트(backbone 산화 → H⁺ 방출) 또는
(b) 표면 acid-base 반응(3.1). "어느 쪽이 진짜냐"가 아니라 "trigger 유무에 따라 공존"이 정답.
**정정 후**: head 열역학, 링커 무관 → 그대로 유지.

### 3.5 "실제는 혼합 폴리머인데 계면에선 어떻게 되나?" → ✅ 유지
**답변 요지**: 실물은 doped unit(–SO₃⁻)과 neutral unit(–SO₃H)의 혼합 사슬. NCM 계면에 닿으면 —
이미 도핑된 unit은 **직접 배위**(3.3-②/③), 미도핑 unit은 **H⁺ 전달 후 배위**(3.3-①). 경로만
다르고 종착지는 같으므로 **"도핑 레벨과 무관하게 모든 SO₃ unit이 계면 형성에 기여한다"** —
논문에 그대로 쓸 수 있는 수렴 문장.
**정정 후**: 문장 그대로 유효. 뒷받침하는 정량(경로별 E_bind 차)만 §2.2 재계산 이후 채움.

### 3.6 "한 분자가 3역할(앵커/Li⁺ 호핑/전자전도)을 한다?" → ✅ 유지 + ② 크게 보강
**답변 요지(원답)**: 하나의 SDCP 사슬에서 ① NCM 쪽 –SO₃⁻는 anchoring, ② 계면에서 떨어진
중간 –SO₃⁻들은 Li⁺가 딛고 가는 hopping site, ③ 공액 backbone은 polaron 전자 전도 — 즉
접착·이온·전자 3기능이 한 분자에 동거. (PTFE는 3개 중 0개, bollard-PC는 ①만.)
**정정 후 — ②가 정량적으로 강해짐**: 정정 구조는 반복단위당 Li⁺ 배위 사이트가 **2개**
(–SO₃⁻ + ether –O–, PEO형 사이트) → 사슬을 따라 `SO₃⁻ → ether-O → SO₃⁻` **사다리**가 생겨
호핑 간격이 절반으로. ICEP(Han 2025, AMPS 술폰산 + PEO ether 조합이 σ_ion 0.135 mS/cm) =
정확히 이 조합의 실험 선례(§5.2).
**정밀화 2건(원답의 과대 방지)**: (a) 이 역할은 연속 interlayer가 아니라 **앵커된 0.2–0.5 µm
입자가 만드는 NCM|SE 접촉 둘레**에서 작동 — 우리 particle 시딩 배치와 자기일관.
(b) pellet σ_ion ×0.80(Fig2f)은 "PTFE(×0.27)보다 덜 차단한다"의 증거이지 SDCP 자체가 Li을
잘 전도한다는 증거가 아직 아님 — 그 칸은 §2.2-7 Li⁺ 패키지(사이트별 결합에너지 + NEB 장벽)가 채움.

### 3.7 "NCM 주위에 SDCP가 cluster처럼 붙어 있을 수 있나?" (사용자 가설) → ✅ 개연(강)
**답변 요지**: 물리적으로 그럴 수 있음, 두 근거 —
① **ordered/interactive mixing**(분체공학 표준): 0.3 µm guest가 5 µm host 표면에 붙으면
부착력(vdW+정전)이 자중을 수십 배 이상 압도 → 미세 guest는 조대 host를 "장식(decorate)"하는
게 기본 거동. 건식 혼합에서 SDCP 입자가 NCM 표면에 무리지어 붙는 것이 오히려 자연스럽다.
② **화학 선택성**: 술폰산 head는 산화물(NCM) 표면과 산-염기/배위 상호작용(§3.1-3.3)이 있지만
황화물(LPSCl) 표면과는 그런 채널이 없음 → NCM 쪽으로 편향 부착.
**반증주의 캐비엇**: 매뉴스크립트 S3 시야는 SE 영역 위주라 "NCM 주위 클러스터"를 직접
확인/반박할 수 없음 → **판별 실험 = SBE/DBE 런의 payload 근접분석(SDCP→AM 최근접 거리 분포)
+ 실물 SEM/EDS(S 원소 맵이 NCM 입자 윤곽을 따라가는지)**.
**모델 반영**: `--sdcp-surface-frac`(AM-앵커 몫) + `--sdcp-clump`(기본 1 = S3-충실 분산;
>1 = 이 가설 시험용 클러스터 시딩) — 가설을 켜고 끌 수 있는 스위치로 구현되어 있음(§6).

### 3.8 "doped −4.8 eV 강한 화학흡착 — 스토리로 맞나?" → 🔶 방향만 유지
**답변 요지(당시)**: doped(−SO₃⁻, 이온성+배위) ≫ neutral(−SO₃H, H-bond 수준)의 강한 화학흡착
스토리가 맞고, neutral/doped를 나눠 보고하는 것도 좋다 — 혼합 실물(3.2/3.5)의 양 끝점이므로.
**정정 후**: **수치(−4.797/−3.020 eV)는 오분자 계산이라 무효**(§2.1). 살아남은 것은
방향성(doped ≫ neutral)뿐이며, 이는 head 화학 + Kang 2025 bollard의 이온성≫극성≫vdW 사다리
(§5.1)가 외부에서 지지. 절대값은 §2.2 재계산 전까지 백지.

---

## 4. 전극 수준 (매뉴스크립트 Figures_v7 앵커)

- **체계**: SBE(PTFE-only) / **DBE(PTFE+SDCP)** / DBE@C-SUS(+SDCP/graphene 200nm 집전체 코팅)
- **S12 (결정적)**: SDCP 단독 = dough 형성 불가 → **PTFE fibrillation web 필수 = dual-binder가 물리**
  → SDCP-단독 시뮬런은 비물리 (비교셋에서 제외)
- **Fig 3a**: DBE에서 **PTFE 분산 균일화** (SBE F-map 응집 → DBE 균일 점) — SDCP가 PTFE 뭉침 억제
  (우리 fibrillation/분산 축과 연결 후보)
- 역학: elastic recovery 0.69→0.82 (nanoindent, Fig3c-d)
- 전기: R_ele 59.7→48.5 Ω·cm² (EIS Fig4c), c-AFM 저저항 면적↑ (Fig4b)
- 셀: 1000cyc@2C 유지 (SBE는 100→62 감쇠, Fig6d); **저압 5MPa에서 격차 최대** (Fig7); R_int 사이클후
  110/46/30 (SBE/DBE/@C-SUS, Fig6e); SBE만 contact-loss+crack (Fig6f)
- **Fig 4(e) "Electrochemical modeling" 빈 패널 + Fig 7(c,d) placeholder** = 우리 기여 목표 슬롯
- **미확보**: SBE/DBE 조성 wt%·로딩 (methods 텍스트) ← **비교셋 사전등록의 유일한 블로커**

---

## 5. 문헌 맥락 (litdb 62편 중 binder 3각)

### 5.1 Kang(Jihyeon) 2025 AM — bollard-anchored binder (PAA-g-CMC + PTFE)
- **흡착 사다리**: 이온성(Na⁺-매개 −2.24 eV) ≫ 중성 극성(−0.37) ≫ vdW(−0.09) = **우리 doped≫neutral
  방향의 외부 확인** (절대값 비교 금지 — fragment/facet/코드 상이)
- **hybrid 7:3 최적** + **PTFE dough 하한: anchor 有 0.6wt% / 단독 2wt%** → `--ptfe-fibril` 미앵커
  magnitude의 첫 실험앵커 후보 + "앵커가 rope 필요량을 줄인다" = DBE 구조 논리
- 분산→성능 산포 (STD 16.52→4.28, ballmill×3) = A5 dispersion-CV 첫 정량앵커
- ⚠ 전이 금지: 액체 LIB (porosity 부호 역전), 필름 E(MPa)/peel(N/cm) 층위

### 5.2 Han 2025 AM — ICEP 이온전도 탄성 바인더 (AMPS+PEO)
- **전도-binder σ_ion 수렴**: ICEP 0.135 ≈ bollard PC 0.131 mS/cm (~0.13 클래스; 둘 다 액체-swollen
  개연 → 건식 절대값 이식 금지)
- **AMPS = 술폰산 앵커** (DFT −1.82~−2.24 vs PVDF −0.70) — 술폰산-계 anchoring 3각측량 완성
- coh σ-스케일: binder flow stress **~2.7 MPa**; SAICAS ~270 N/m (비율만)
- ★ **전극 나노압입 E 1.57 GPa ≈ 우리 MPM champion E_eff 1.53** — "벌크 수십 GPa → 전극 O(1 GPa)"
  서사의 외부 실측 동반자
- binder 형상 3분류 완성: **coat**(ICEP 7nm)/**aggregate**(PVDF)/**fibril**(PTFE) + **particle**(SDCP)

### 5.3 Novelty 포지셔닝 (SDCP 논문)
앵커-바인더 개념 자체는 bollard 선례 존재 → 주장은 **(i) 앵커가 스스로 전자전도하는 3기능 단일분자**
(bollard PC는 절연 2기능) **(ii) 앵커 에너지의 입자스케일 역학 매핑 (γ→coh→MPM, 우리 파이프라인)**.
bollard/ICEP은 방향·실효성의 인용처.

---

## 6. 우리 모델 구현 (전부 커밋됨)

| 축 | 구현 | 상태 |
|---|---|---|
| **시딩** | `kind='particle'`: AM-앵커 몫(`surface_frac`, bm/thinky 0.5·handmix 0.3 — §F1 hook) seed_coat(shell=입자반지름) + 나머지 bulk 균일(in_am drop). **`--sdcp-clump`**(기본 1=S3-충실; handmix 3; >1 = §3.7 cluster 가설 시험) | ✅ (리뷰 2회 통과) |
| **역학** | E=23.6 GPa ✅앵커 + **CFL dt 가드**(additive E > SE 스택 시 dt 캡; VGCF 10 소급) / σ_y=1.0 rigid-proxy ⚠ / coh_sdcp=bulk 필름 무결성(variant-무관 — γ-비율은 미래 boundary 항) | ✅ |
| **variant** | `--sdcp-neutral`: STEP3 σ-가중용 provenance (econn에선 AM급 도체 유지 — 절연 취급은 13자릿수 오분류) | ✅ |
| **전기 연결성 (econn)** | AM-AM 접촉 ∪ AM-[VGCF/SuperP/SDCP]-AM 다리 → 집전체 percolation → 연결/고립 (SE·PTFE 제외). 풀해상도 계산(payload step2), per-particle `econn` + summary | ✅ (S런 검증: AM골격 82% + carbon 다리→100%) |
| **STEP3 예고** | SDCP = 스택 최초 **이중-전도 상** (e ×5.1 + Li⁺ ×0.80 pellet 앵커) — network solver에 σ_e·σ_ion 동시 배정 | 설계노트 |
| metadata | morphology/E_anchor/variant/clump/coat/`anchor_status: INVALID_WRONG_MONOMer_recompute_pending` | ✅ 자기문서화 |
| 파이프라인 | 웹앱 UI(SDCP wt%)·route·zip·payload 채널·viewer 배선 | ✅ |

**A4 (coat-seeding) 마감 상태**: SDCP=particle ✓ / SuperP thinky coat_block ✓ (thinky≢ballmill 경계
CSV 기록) / VGCF coat_embed **은퇴**(섬유는 코팅 불가 — 물리 확정) / **남은 관문 1: SuperP 2wt% thinky
divergence 런** (사전등록: porosity 11.94 동일 / SE-cov↓ / add-cov≫35.8 / coat 메타) → PASS 시 CLOSED.

---

## 7. 로드맵 (남은 작업, 독립 병렬 3갈래)

1. **DFT 재계산** (사용자 서버): §2.2 스펙 — correct monomer + chelation 배향 + Li⁺ 패키지.
   slab/U-ramp 재사용. 완료 시: E_bind·γ 앵커 복구 → coh 갱신 → §3 스토리 정량 완성
2. **A4 마지막 관문** (kgy): SuperP 2wt% thinky zip 1런 → A4 CLOSED
3. **비교셋** (블로커: SBE/DBE 조성 wt%): SBE(PTFE x) vs DBE(PTFE x+SDCP y) → 사전등록 → kgy 런 →
   **econn 연결성 지도(한양대 slide-19 문법) = Fig 4(e) 후보 그림** + SDCP→AM 근접분석(§3.7 판별)
4. (이후) STEP3: 이중-전도 SDCP σ 배정 → σ_e/σ_ion 정량 → Fig 4(e) 완성판

## 8. 파일 맵
- 이 문서: `docs/sdcp_master.md` (통합 뷰 — 갱신 시 여기부터)
- 상세 앵커/판정 로그: `docs/sdcp_manuscript_anchors.md`
- 문헌: `litdb/papers/kang2025_bollard_anchored_binder_dry_electrode.md`, `litdb/papers/han2025_icep_conductive_elastic_binder.md` (+ 각 CSV: `docs/data/*_anchors.csv`)
- 작업 추적: `docs/digest_model_application_backlog.md` A4/A4′ 행
- 코드: `scripts/additives.py` (SDCP_D/process rows/seed_coat), `scripts/mpm3d_compaction.py` (particle 분기·flags·metadata), `scripts/mpm_webapp_payload.py` (econn), `webapp/` (UI/route)
