<!-- digest 초판 2026-10-03 (논문 에이전트 · 대피 세션 `claude/evac-2026-10-02` — 커밋은 부모 세션이 한다).
     사용자 요청 원문: "이 논문도 논문에이전트 부탁하고, 마지막 dft section 관련해서 한번 논리의 전개가 맞는지 확인해줘"
     ① 이 digest 의 제1 목적은 `## DFT 절 논리 감사` 다 — §2.4 후반(계산 해석)의 논증 사슬을 10단계로 다시 세우고 화살표마다 판정했다.
     ② 그림: 본문 6장 전부 + SI 11장 + 표 2장을 실제로 봤다 (안 본 SI 17장은 머리말에 목록).
        `Fig. 6a–c` · `Fig. S28a` 의 반응에너지는 400 dpi 재렌더 + 마커 색 중심 픽셀 판독(±0.005–0.01 eV/atom)이다.
     ③ 손작업: SI `Fig. S13`·`S16`·`S20`·`S23` 손 크롭 (도구가 번호 공백으로 놓침) · `fig_S1` 상단(SI 절 제목 혼입) · `tab_S2` 오른쪽 끝("[14, 15" 잘림) 재크롭 ·
        2배 줄간격 SI 캡션 21건 원문 복원 (`caption_fix`). 전부 figures.json 에 표지를 달았다.
     ④ 계산 조건은 SI p.5 원문을 그대로 옮겼다 — 미기재는 "미기재" 로 남겼다. pymatgen 의 무(無)엔트리 반응물 처리(hull 에너지 대체)는 우리 venv 소스(2026.9.24)로 확인했다.
     ⑤ `INDEX.md` · `comparison_vs_ours.md` 는 이 세션에서 고치지 않았다 (부모 세션 병합 대기).
     ⑥ `## Figure set` 을 §3 앞에 뒀다 — 웹 그림 주석이 파일 순서로 그림당 3 개까지만 모아서, 그림을 인용하는 소제목이 먼저 오면 표 행이 밀려난다. -->

# Deciphering and overcoming the high-voltage limitations of halide and sulfide-based all-solid-state lithium batteries — Qi et al. (*J. Energy Chem.* **103**, 926–935, 2025)

> slug `qi2025_high_voltage_limits_halide_sulfide_assb` · DOI `10.1016/j.jechem.2024.11.034` · type `exp 주 + DFT 보조 (자체 VASP-PBE DOS · MP 에너지로 닫힌계 pseudo-binary 상호반응에너지)` · PDF `litdb/inbox/Qi 2025 - Deciphering high-voltage limitations of halide and sulfide ASSLBs (J Energy Chem 103 926).pdf` (본문 10 pp) + `litdb/inbox/Qi 2025 - Sup) Deciphering high-voltage limitations of halide and sulfide ASSLBs (J Energy Chem 103 926) SI.pdf` (SI 38 pp: `Fig. S1`–`S28` · `Table S1`–`S2` · 실험·계산 방법 pp.2–5) · digested `2026-10-03` · status ✅ · 태그 **[외부]**

> elements: Li, P, S, Cl, O, Zr, Ni, Co, Mn, In, C
> methods: DFT, DOS, PDOS, ESW, XPS

> **저자**: Xiang Qi^a · Gang Wu^a · Meng Wu^a · Dabing Li^a · Chao Wang^a · Lei Gao^a · **Shichao Zhang**^b\* · **Li-Zhen Fan**^a\* (^a Beijing Advanced Innovation Center for Materials Genome Engineering · Beijing Key Laboratory for Advanced Energy Materials and Technologies, **University of Science and Technology Beijing (USTB)** · ^b School of Materials Science and Engineering, **Beihang University**) · 접수 2024-10-30 · 수정 2024-11-20 · 수락 2024-11-20 · 온라인 2024-11-28 · © Science Press / DICP (Elsevier, *all rights reserved incl. TDM·AI training* — OA 아님) · 자금: National Key R&D Program 2022YFB3803505 · NSFC U21A2080 & 22479009 · FRF-TP-22-01C2 · **CRediT**: Gang Wu = *Software, Data curation* · Lei Gao = *Software, Data curation* (계산 담당으로 읽힌다 — 추정) · Xiang Qi = 초안·방법·실험 · Li-Zhen Fan = 구상·자금.
>
> **계보**: **같은 USTB Li-Zhen Fan 연구실**의 litdb 편들 — `[Li25]` `li2025_cubr2_dualdoping_argyrodite`(G. Wu 공저) · `[LiInF]` `li2024_inf3_argyrodite_ultrathin_film`(Dabing Li·Qi·Gao 공저) · `[LiGaF]` `liyaru_gaf3_codoping_argyrodite`(Dabing Li·Qi 공저) · `[Fan26]` `fan2026_sulfide_assb_stability_review_ECERD2600097`(미출판 리뷰 초안). 이 편은 그 연구실이 **도핑 SE 가 아니라 양극 계면(4.5 V)** 을 다룬 편이다.
> **계산 방법의 계보**: 상호반응에너지 = SI 참고문헌 [8] Zhu·He·Mo *J. Mater. Chem. A* 2016 (litdb 없음) · [9] Zhu·He·Mo *ACS AMI* 2015 = `zhu2015_esw_grand_potential_origin` 의 닫힌계(chemical) 쪽. `Table S1` 의 '이론 산물' 은 본문 [48]/SI [10] **Kochetkov 2022 *EES*** (litdb 없음 — 미검증) 와 [49]/SI [11] **[Xiao19]** `xiao2019_cathode_coating_screening` 에서 **가져왔다**. 본문 [47] = 우리 `zuo2022_chlorination_cathode_interface` · [53] Zuo 2023 *ACS Energy Lett.* (LPSC 유래 Li₃PO₄+Li₂SO₄ 코팅 — litdb 없음).
>
> **관련 digest**: `richards2016_interface_stability_pseudobinary`([Rich16] 형식 원전) · `xiao2019_cathode_coating_screening`([Xiao19] — LZPO 산화한계 4.52 V 가 여기 있다) · `xiao2020_interface_stability_ssb_review` · `park2026_ml_framework_stable_interfaces_assb`([Park26ML] 인산염화 Zr) · `sundar2025_oxide_coating_screening_lpscl`([Sundar] ZrO₂ 실패) · `cha2024_dualcompatible_halide_ncm_lpscl_interface`([Cha] **우리 그룹** — LZC 코팅 4.3 V) · `yun2023_deciphering_degradation_halide_vs_sulfide`(**우리 랩** — 할라이드 vs 황화물 열화) · 코팅 축 `lee2026_lpscl_coating_thickness_ncm811`(§J-26) · `kim2025_lto_pald_conformal_coating_nca`(§J-27) · `bong2023_linbo3_thickness_uniformity_ncm523`(§J-28) · `nolan2018_…`·`nolan2019_…`·`nolan2021_…`(코팅 계산 계보).

> **본 digest 에서 실제로 본 그림 (2026-10-03)** — 크롭 **36장**(그림 34 + 표 2) 중 **19장**:
> 본문 `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 6` (**6/6**) · SI `Fig. S1` `Fig. S11` `Fig. S13` `Fig. S16` `Fig. S20` `Fig. S22` `Fig. S23` `Fig. S24` `Fig. S25` `Fig. S27` `Fig. S28` (11장) · `Table S1` `Table S2` (이미지로도 봤다 — 값은 PDF 텍스트로 전사).
> **안 본 것 (17장)**: `Fig. S2`–`S10` · `Fig. S12` · `Fig. S14` · `Fig. S15` · `Fig. S17`–`S19` · `Fig. S21` · `Fig. S26`. 이들의 수치는 **본문 문장 또는 PDF 벡터 텍스트층**(축 라벨·범례에 인쇄된 값)에서만 가져왔다.
> **손작업**: `Fig. S13`·`S16`·`S20`·`S23` 은 도구가 번호 공백으로 놓친 **벡터 그림**이다 (얇은 선 경로를 1.5 pt 미만이라 걸러 그래픽 수가 문턱 6 아래로 떨어짐 · S16 은 '영역 없음') → 손 크롭 (`manual_crop`). `fig_S1` 은 SI 절 제목이 위에 섞여 재크롭, `tab_S2` 는 Ref. 열이 `[14, 15` 로 잘려 재크롭 (`recrop`).
> **그림이 본문 서술과 어긋난 곳 (7)**: ① `Fig. 6a` — 본문 *"LiNiO₂/LZC interface was relatively stable"* 인데 그림의 ZrCl₄/LiNiO₂ 가 **패널에서 가장 깊다**(`figure-read ≈` −0.22 eV/atom) ② `Fig. 6a` vs `Fig. 6c` — −0.08 은 "moderate → 열화", −0.07 은 "low → 잠재력" ③ `Fig. 6d`(ZrO₂ 3.40 eV = "narrow → high electronic conductivity") vs `Fig. S11`(NiO 1.97 eV = 본문 §2.2 *"insulating"*) ④ 본문 *"high partial ionic conductivities"*(Li₃PO₄·Li₂SO₄) vs `Table S2` **"low"** ⑤ 본문 *"LZPO possessed high ionic conductivity"* vs `Table S2` **"medium"** ⑥ `Fig. 6g` 가운데 패널 SE 라벨이 **"LPSC₁.₅"** (이 논문 SE 는 Li₆PS₅Cl) ⑦ `Fig. S20` 캡션 *"at 0.2 C"* 인데 방전용량(`figure-read ≈` 185/181 mAh g⁻¹)은 `Fig. 4h` 의 0.1 C 예비 사이클 값과 같고 0.2 C 값(≈163–165)과 다르다 (경미).
> 그림에서만 읽은 값은 **`figure-read ≈`**, 논문에 없는 우리 계산은 **(우리 산수)** 로 표시했다.

---

## 0. 이 digest 를 읽는 법 — 왜 이 논문이고, 무엇을 확인했나

**사용자 요청**: *"마지막 DFT section 관련해서 한번 논리의 전개가 맞는지 확인해줘."* → 이 digest 의 중심은 아래 **`## DFT 절 논리 감사`** 다. 실험 부분(§3·§5)은 그 감사의 **전제**를 확인하려고 정리했다.

이 논문이 우리에게 걸리는 자리는 셋이다.

1. **우리 comp1 = 이 논문의 LPSC (Li₆PS₅Cl) 그대로**다. 양극은 NCM85(LiNi₀.₈₅Co₀.₁Mn₀.₀₅O₂) — 우리 CEI 트랙이 다루는 고-Ni NCM 과 같은 계열이다.
2. 이 논문 DFT 의 핵심 양 — **양극/전해질 "상호반응에너지"(mutual reaction energy, pseudo-binary)** — 는 우리 B③ 도구 `tools/oxidation/interface_reactivity_v2.py` 가 재는 양과 **같은 종류**다. 단 이 논문은 **닫힌계**(Li 저장고 안 엶)이고, 우리 도구의 기본은 **Li 열린계 · 전압 의존**이다 (`--closed` 를 주면 이 논문과 같은 모드가 된다).
3. 이 논문은 **PBE 밴드갭으로 산물의 전자전도도를 판정**하고 그걸로 코팅(LiZr₂(PO₄)₃, LZPO)을 고른다 — 우리 §D 규율("갭은 wide-gap 정성만 · 갭 ≠ σ_e · 갭 ≠ 분해 onset")이 정면으로 걸리는 자리다.

⚠ **트랙 구분** (CLAUDE.md): ESW·우리 DFT 기준선 = **사용자 1저자** / CEI(Nd 계면) = **실험 쪽 다른 사람이 1저자** / 할라이드 SE(Li₂ZrCl₆·Li₃InCl₆)는 **우리 계가 아니다** — 수치 대조는 안 하고 방법·논리만 본다.

⚠ **전압 기준**: 셀은 **Li–In 대극**이고 SI 는 정전류 창을 *"2.1–3.6 V / 2.1–3.9 V (vs. Li-In/Li⁺)"* 로 적는다. 본문은 전부 **vs Li/Li⁺ (= +0.6 V)** 로 적는다 (2.7–4.2 / 2.7–4.5 V). CV 도 SI 는 *"0–5 V (vs. Li-In/Li⁺)"*, `Fig. S1d` 축은 vs Li/Li⁺ 이고 데이터가 ≈0.6–5.6 V 에 걸쳐 있다 → **환산 일관 ✓**. 이 digest 의 전압은 전부 **vs Li/Li⁺** 다.

---

## 1. 한 줄 요약

70:30 NCM85/SSE 복합양극을 **4.5 V** 까지 돌리면 **할라이드(Li₂ZrCl₆, LZC) 셀은 초기엔 안정(ICE 89 %)하지만 장기 붕괴**하고(*"unlimited interfacial degradation"*), **황화물(Li₆PS₅Cl, LPSC) 셀은 첫 사이클에 크게 잃고(ICE 72 %) 그 뒤 완만**하다(*"self-limited"*). 탄소(VGCF 2 wt%)는 용량은 올리지만 분해를 가속하고, **~10 nm 비정질 LiZr₂(PO₄)₃(LZPO) 코팅**을 더하면 두 셀 모두 **>195 mAh g⁻¹(0.1 C) · 600 사이클 >80 %(0.5 C) · >115 mAh g⁻¹(1 C)** 가 된다. 마지막 절의 DFT(닫힌계 상호반응에너지 + PBE DOS)는 이 차이를 *"반응에너지 크기 → 초기 안정성, 산물의 수송 성질 → 장기 안정성"* 으로 해석한다 — ⚠ 그 해석의 고리 대부분은 **계산이 지지하지 않거나 자기 그림과 어긋난다** (`## DFT 절 논리 감사`).

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 비교 쌍 | **NCM85/LZC** (catholyte Li₂ZrCl₆ · 분리막 LZC\|LPSC 이중층) vs **NCM85/LPSC** (catholyte·분리막 모두 Li₆PS₅Cl) — `Fig. S4` · 음극 Li–In |
| 일반화 시도 | **Li₃InCl₆ (LIC)** 셀 1개 (`Fig. S26`–`S28`) |
| 던지는 질문 | ① 4.5 V 에서 두 catholyte 셀이 **왜 다르게** 무너지나 ② 전극 **질량분율(탄소)** 과 **계면 조성(코팅)** 으로 어디까지 회복되나 |
| 서론의 전제 (축 미명명) | 황화물 *"low oxidation limits (~2.6 V vs. Li/Li⁺)"* (ref [7] 리뷰) · 할라이드 *"approximately 4.3 V"* (ref [12] Kim 2021 *Chem. Mater.*) — ⚠ **어느 축(층① 분해 onset? 동역학 onset?)인지 안 적는다** (§7-2) |
| 논문이 주장하는 신규성 | *"contrary to previous studies"* — 할라이드 = 무제한 열화 · 황화물 = 자기제한 열화 (초록) |
| 해법 | 질량분율 조작(VGCF 0/2/5 wt%) + 계면 조성 조작(LZPO 0/0.5/1.0/3.0 wt% 졸–겔) |
| 계산의 역할 | 마지막 절 *"Finally, combined with theoretical calculations…"* — **사후 해석**(코팅 선택은 계산 전에 문헌 [27,28]으로 이미 정해져 있다) |

---

## Figure set

> ⓘ 이 표를 §3 앞에 둔 이유: 웹 화면의 그림 주석은 파일 **순서대로 그림당 3 개까지만** 모은다 (`webapp/data.py::paper_figure_notes`). 그림을 인용하는 소제목이 표보다 앞에 오면 이 표의 행이 밀려난다.

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 70:30:0 복합양극, 4.2 V(a–c)·4.5 V(d–f) 충방전·사이클. 4.2 V ICE LZC 89.5 / LPSC 76.1 %; 4.5 V ICE 89.3 / 72.4 %; 4.5 V 200 사이클 `figure-read ≈` LZC 163→61 · LPSC 113→89(78.7 %), ≈90 사이클 교차 | DFT 절의 전제("초기 vs 장기")가 실제로 그림에 있다 ✓. 충전용량으로 x(Li) 검산(§감사 2단계) |
| 2 | VGCF 0/2 wt% 효과(4.5 V): LZC 방전 +23.7 · H2→H3 피크↑ · 장기 붕괴(2 wt% 200 사이클 `figure-read ≈`15); σ_e 1.78×10⁻⁴ → 2.86×10⁻² S cm⁻¹; GITT log D ≈ −12~−13; 모식도 i | **B② (분해 속도·양) 의 실측 사례** — 전자 경로가 초기 용량과 분해를 동시에 올린다. DEM·전극 축(VGCF 함량)의 화학 대가 앵커 |
| 3 | LZPO@NCM85: 모식도 · SEM(bare 매끈 / 코팅 흐림) · HRTEM ~10 nm 비정질 · HAADF-EDS(Zr·P 희박) · XPS O 1s/Zr 3d/P 2p | 계산 대상(결정 LZPO) ≠ 실제 코팅(비정질 ~10 nm) — §감사 5단계 근거 |
| 4 | 68:30:2, 4.5 V: bare vs LZPO 충방전(a,b,d,e) · 200 사이클(c) · 0.5 C 600 사이클(f) · 율속(g) · 26 mg cm⁻² 60 °C(h) · 레이더(i, 눈금 없음) | 코팅 효과는 LPSC 셀에서 훨씬 크다(ICE +12.7 %p vs +1.7 %p) → 황화물–산화물 화학 접촉 차단이 본체 |
| 5 | XPS 200 사이클 후: LZC 4.5 V 에 Clₓ⁻ 199.0 eV(Zr 3d 불변) · LPSC 는 섞기만 해도 P₂Sₓ, 4.5 V 에 SO₃²⁻·SO₄²⁻·PO₄³⁻; LZPO 로 약화(소멸 아님) | 4단계(LPSC 화학 비호환)의 실측 기둥 · 6단계(ZrO₂·Li₂ZrO₃ 비관측)의 근거 · 우리 B③ 산물 클래스(Li₃PO₄·Li₂SO₄)와 같은 종 |
| 6a–c | 닫힌계 상호반응에너지 (LiNiO₂ / Li₀.₂₅NiO₂ 대리). `figure-read ≈` ZrCl₄/LiNiO₂ −0.22(패널 최저) · ZrCl₄/Li₀.₂₅NiO₂ −0.21 · LiCl 0→−0.08 · LPSC −0.42 / −0.72 · P₂S₅ −0.86 · LZPO/LiNiO₂ −0.07 · LZPO/LPSC −0.03 | 🔴 본문 "LiNiO₂/LZC relatively stable" 과 모순. 우리 `interface_reactivity_v2.py --closed` 와 같은 종류의 양 — 절대값 비교 금지(양극·판본·정규화 다름) |
| 6d–f | PBE DOS: ZrO₂ 3.40 · Li₂SO₄ 6.01 · LZPO 4.06 eV (인쇄값) | 🔴 "narrow → high electronic conductivity" 는 `Fig. S11`(NiO 1.97 = 절연)과 자기모순. 우리 §D 반례 행 후보 |
| 6g | 세 계면 기전 모식도 (channel block / partially block · unlimited / self-limited) | 열역학 → 성장 법칙 비약(9단계). 가운데 패널 SE 라벨 "LPSC₁.₅" 오기 |
| S1 | LZC·LPSC XRD · 아레니우스(0.54 / 4.10 mS cm⁻¹, Ea 0.36 / 0.29 eV) · DC 분극 σ_e 3.93×10⁻⁹ / 2.46×10⁻⁸ S cm⁻¹ · CV(LPSC 개시 2.4 · 피크 3.8 V; LZC 개시 ≈3.9 · 피크 4.4 V) | B① 동역학 onset 의 또 한 점 (우리 층① 2.256 V 와 등치 금지) · §D σ_e 실측 anchor (Li₆PS₅Cl 2.46×10⁻⁸) |
| S2–S3 | LZC · LPSC SEM-EDS (안 봄 — 캡션 기준) | — |
| S4 | 두 셀 구성 모식도 (LZC 셀은 LZC‖LPSC 이중층 분리막) (안 봄 — 캡션 기준) | 할라이드 셀에도 LPSC 분리막이 있다 — LZC/LPSC 계면은 계산 안 됨 |
| S5 | 4.2 / 4.5 V 율속 (안 봄 — 본문 수치만) | — |
| S6 | 1st vs 100th EIS (안 봄 — 본문 서술만) | — |
| S7 | VGCF SEM (안 봄) | — |
| S8–S9 | 4.2 V 에서 VGCF 효과 — LZC 개선 · LPSC 악화 (안 봄 — 본문 수치) | B② 사례 보강 |
| S10 | VGCF 따라 P₂Sₓ 증가 XPS (안 봄 — 본문 서술) | 탄소가 분해를 가속한다는 직접 증거 |
| S11 | NiO 스핀 분극 DOS · 갭 1.97 eV (인쇄값) · 위/아래 채널 비대칭 = 강자성 배열로 보임 | 🔴 §2.2 "insulating" 의 근거 → 6단계 자기모순의 한쪽. +U·자기배열 미기재 |
| S12 | 5 wt% VGCF: ICE 81.7 % · 50 사이클 13.0 mAh g⁻¹ (안 봄 — 벡터 텍스트·본문) | 탄소 과잉의 극단값 |
| S13 | DC 분극: NCM85 4.26×10⁻² · NCM85/LPSC 0 wt% 1.12×10⁻⁴ · 2 wt% 1.36×10⁻² S cm⁻¹ (손 크롭) | 복합체 σ_e 는 탄소가 지배(≈120–160 배) — "LPSC 계면이 절연층" 귀속(2 배 차)은 약하다 |
| S14 | NCM85/LPSC + 2 wt% VGCF SEM (안 봄) | — |
| S15 | 고부하 26 mg cm⁻² · 60 °C 탄소 효과 (안 봄) | — |
| S16 | LZPO 0/0.5/1.0/3.0 wt%: XRD (003) 고각 이동 · 100 사이클 `figure-read ≈` bare 170→32 · 1.0 wt% 189→175 (손 크롭) | 코팅 함량 최적점(1.0 wt%)과 "미량 도핑" 자인 — 계산 대상이 순수 결정 LZPO 가 아님 |
| S17 | NCM85 SEM-EDS (안 봄) | — |
| S18–S19 | LZPO 셀 0.5 C 곡선 · 율속 (안 봄) | — |
| S20 | 고부하 LZPO 셀 첫 사이클 `figure-read ≈` 210/185 · 228/181 (손 크롭) | 캡션 "0.2 C" 와 값이 0.1 C 예비 사이클에 맞는다 (경미한 캡션 의심) |
| S21 | 100 사이클 후 EIS 4 셀 (안 봄 — 본문 서술) | — |
| S22 | in-situ EIS + DRT (LZC 셀): bare 의 τ≈2×10⁻⁴ s 봉우리 `figure-read ≈` 35→348 Ω(3.7→4.5 V), LZPO 22→118 Ω; 꺾임 4.1–4.3 V | 할라이드 계면 저항이 4.3 V 위에서 가파름 — `[Cha]`(LZC 코팅, 4.3 V 컷오프 안정)와 같은 그림 |
| S23 | 첫 사이클 4.2/4.5 V × VGCF 0/2 wt% (LZC·LPSC) — LZC 충전 175/198/199/227 · 방전 156/178/177/201 `figure-read ≈` (손 크롭) | ⭐ x(Li) 검산의 원자료: "4.2 V + 2 wt%" = "4.5 V + 0 wt%" 같은 탈리튬 깊이 → LiNiO₂ ≠ 4.2 V 상태 |
| S24 | PBE DOS: LiCl 6.22 · ZrCl₄ 3.37 · Li₂ZrO₃ 3.64 eV | 갭 문턱이 3.64 와 4.06 사이 어딘가 — 적히지 않음. LiCl(최대 갭)이 "보호 실패" 인 기준 전환 |
| S25 | PBE DOS: Li₃PO₄ 5.94 · Li₂S 3.14 · P₂S₅ 2.26 eV | 같은 연구실 Li₂S 갭 3.04(`[Li25]`)/3.14/4.2(`[LiGaF]`) — 문턱 분류가 편마다 뒤집힘 |
| S26 | LIC XRD · σ 1.83 mS cm⁻¹ · Ea 0.31 eV · σ_e 3.06×10⁻⁹ (안 봄 — 벡터 텍스트) | LIC 일반화의 교락 변수(σ 3.4 배) |
| S27 | NCM85/LIC 4.5 V: ICE 88.9 % · 100 사이클 `figure-read ≈` 182→122 | LIC 가 LZC 보다 덜 감쇠한다는 실험은 맞다 — 원인 배정만 비약 |
| S28 | LIC 상호반응(`figure-read ≈` LIC/LiNiO₂ −0.09 · LIC/Li₀.₂₅NiO₂ −0.115 · InClO −0.10 · In₂O₃ 0) + InClO 2.20 · In₂O₃ 0.76 eV DOS | LIC 는 화합물·LZC 는 원료 — 표현 교락(10단계) |
| Table S1 | 세 계면의 산물 — 실험(XPS) vs 이론(**인용**: Kochetkov [10] · `[Xiao19]` [11]) | 이론 산물이 이 논문 `Fig. 6` 에서 나온 게 아니다 · "실험 산물" ZrCl₄·LiCl 은 LZC 자신과 구분 불가 |
| Table S2 | 5 코팅 후보 정성 등급 (전자·이온·산화한계·효과) + 문헌 | 결론이 담긴 표가 결론을 "validate" — 순환. 본문과 모순 2 (이온전도 high↔low · LZPO high↔medium) |

---

## 3. 핵심 수치 총정리 ★

> 기준 전극 = **vs Li/Li⁺**. `figure-read ≈` = 그림에서 읽은 값(본문 미명시). 셀은 별도 표기 없으면 **30 °C · NCM85 10.4 mg cm⁻²**.

### 3a. 전해질 (`Fig. S1` · `Fig. S26` — 값은 그림에 인쇄된 텍스트)

| 물성 | LZC (Li₂ZrCl₆) | LPSC (Li₆PS₅Cl) | LIC (Li₃InCl₆) |
|---|---|---|---|
| 합성 | LiCl+ZrCl₄ 볼밀 600 rpm 10 h (BPR 40:1) — **열처리 없음** | Li₂S+P₂S₅+LiCl 550 rpm 5 h → **450 °C 5 h** | LiCl+InCl₃ 500 rpm 20 h → **260 °C 5 h** |
| XRD | 넓은 혹 + 약한 피크, **Li₃YCl₆ PDF#44-0286** 로 지수 (`figure-read`) | Li₇PS₆ PDF#34-0688 형 argyrodite | PDF#04-009-9027 |
| σ (30 °C) | **0.54 mS cm⁻¹** | **4.10 mS cm⁻¹** | **1.83 mS cm⁻¹** |
| Ea (아레니우스, 20–80 °C) | 0.36 eV | 0.29 eV | 0.31 eV |
| ┗ 홉 수 검산 (우리 산수 · ν₀ 10¹³ s⁻¹ **가정** · 303 K) | Γ ≈ 1.0×10⁷ s⁻¹ · 1/Γ ≈ 97 ns | Γ ≈ 1.5×10⁸ s⁻¹ · 1/Γ ≈ 6.6 ns | Γ ≈ 7.0×10⁷ s⁻¹ · 1/Γ ≈ 14 ns |
| σ_e (DC 0.4 V · 40 min) | 3.93×10⁻⁹ S cm⁻¹ | **2.46×10⁻⁸ S cm⁻¹** | 3.06×10⁻⁹ S cm⁻¹ |
| CV 산화 (SE:VGCF 30:70 wt, 0.2 mV s⁻¹) | 개시 ≈**3.9 V** · 피크 **4.4 V** | 개시 **2.4 V** · 피크 **3.8 V** | n/a |

> ⚠ Ea 는 **전도도 아레니우스 기울기**이지 단일 홉 장벽이 아니다 — 위 검산은 "mS cm⁻¹ 급 전도와 ns 대기시간이 차수에서 모순이 없다" 는 확인뿐이다 (`D-2026-09-27-barrier-hop-count`).
> ⚠ CV 복합체 무게비는 SI 원문 *"LZC or LPSC was ball-milled with VGCF … in a weight ratio of 30:70"* — 순서대로 읽으면 **SE 30 : VGCF 70** 이다 (탄소 과잉 — 순서 모호).

### 3b. 셀 조건 (SI pp.3–5)

| 항목 | 값 |
|---|---|
| 복합양극 | NCM85 : SSE : VGCF = **70:30:0 · 68:30:2 · 65:30:5** (볼밀 300 rpm 30 min) |
| 분리막 | LZC/LIC 셀: LZC(또는 LIC) 40 mg + LPSC 80 mg 이중층 · LPSC 셀: LPSC 120 mg (100 MPa, ∅10 mm) |
| 양극 부하 | 복합체 12 mg 또는 30 mg (300 MPa) → (우리 산수) 12×0.68/0.785 cm² = **10.4** · 30×0.68/0.785 = **26.0 mg cm⁻²** ✓ (논문값과 일치) |
| 음극 | Li–In (70 MPa) · 조립 후 4 h 휴지 |
| 사이클 | 30 °C 또는 60 °C · 1 C = 180 mA g⁻¹ · **0.1 C 예비 3 사이클** 후 장기 시험 |
| GITT | 0.05 C 10 min + 휴지 1 h |
| in-situ EIS | 0.1 C 충전 중 3.7 / 3.9 / 4.1 / 4.3 / 4.4 / 4.5 V |
| ⛔ 미기재 | **사이클 중 스택압** (황화물 셀 성능에 지배적 — 다른 논문과 용량·유지율 직접 비교 금지) · 셀 수 n · 오차막대 |

### 3c. 4.2 V vs 4.5 V — 무코팅 · 70:30:0 (`Fig. 1` · `Fig. S5` · `Fig. S6`)

| 항목 | NCM85/LZC | NCM85/LPSC | 출처 |
|---|---|---|---|
| 4.2 V 1st 충/방전 | `figure-read ≈` 175 / 157 mAh g⁻¹ · **ICE 89.5 %** | `figure-read ≈` 202 / 153 · **ICE 76.1 %** | `Fig. 1a,b` |
| 4.2 V 200 사이클 (0.2 C) | `figure-read ≈` 143 → 117 | `figure-read ≈` 133 → 85 | `Fig. 1c` |
| 4.2 V 1.0 C | ≈65 mAh g⁻¹ | ≈75 | `Fig. S5a` (본문) |
| 4.5 V 1st 충/방전 | `figure-read ≈` 199 / 178 · **ICE 89.3 %** | `figure-read ≈` 212 / 153 · **ICE 72.4 %** | `Fig. 1d,e` |
| 4.5 V 초기 3 사이클 (0.1 C) | ≈180 거의 불변 | **−20.3 mAh g⁻¹** | 본문 |
| 4.5 V 200 사이클 (0.2 C) | `figure-read ≈` 163 → **61** (가속 감쇠) | `figure-read ≈` 113 → 89 = **78.7 %** (본문) | `Fig. 1f` — ⚠ 유지율 기준점은 **4번째(첫 0.2 C) 사이클** |
| 교차 | `figure-read ≈` **≈90 사이클**에서 LPSC 가 앞선다 | | `Fig. 1f` |
| 4.5 V 1.0 C | ≈75 mAh g⁻¹ (LZC > LPSC, *"lower oxidation currents of LZC"*) | | `Fig. S5b` |

### 3d. 탄소(VGCF) 효과 (`Fig. 2` · `Fig. S8`–`S10` · `Fig. S12` · `Fig. S13` · `Fig. S23`)

| 항목 | 값 | 출처 |
|---|---|---|
| LZC 4.2 V, 2 wt% | 초기 방전 **178.4** · 1.0 C ≈98 · 200 사이클 **85.7 %** | `Fig. S8` (본문) |
| LPSC 4.2 V, 2 wt% | 초기 방전·유지율 **오히려 하락** · XPS P₂Sₓ 증가 | `Fig. S9` · `Fig. S10` (본문) |
| LZC 4.5 V, 0 → 2 wt% | ICE −0.6 %p (89.3 → 88.7) · 방전 **+23.7** (`figure-read ≈` 178 → 201) · H2→H3 dQ/dV 피크 뚜렷 · **장기 붕괴** (`figure-read ≈` 200 사이클 ≈15) | `Fig. 2a–c` |
| LPSC 4.5 V, 0 → 2 wt% | `figure-read ≈` 153 → 167 · 200 사이클 ≈89 → ≈79 | `Fig. 2d–f` |
| LZC 4.5 V, **5 wt%** | 50 사이클 후 **13.0 mAh g⁻¹** · ICE 81.7 % | `Fig. S12` (본문 + 벡터 텍스트) |
| σ_e 복합체 | NCM85 단독 **4.26×10⁻²** · NCM85/LZC 0 wt% **1.78×10⁻⁴** → 2 wt% **2.86×10⁻²** (161×, 우리 산수) · NCM85/LPSC 0 wt% **1.12×10⁻⁴** → 2 wt% **1.36×10⁻²** S cm⁻¹ | `Fig. 2g` · `Fig. S13` |
| GITT D_Li (LZC 4.5 V) | `figure-read ≈` log D 2 wt% ≈ −12 ~ −13 · 0 wt% 은 ≈200 mAh g⁻¹ 부근에서 ≈ −15 로 급락 | `Fig. 2h` |
| 결론 (논문) | 탄소 = 전도망 형성(초기 용량↑) **대가** 분해 가속(장기↓) → 이후 탄소 **≤2 wt%** 로 고정 | `Fig. 2i` |

### 3e. LZPO 코팅 (`Fig. 3` · `Fig. 4` · `Fig. S16`–`S20`)

| 항목 | 값 | 출처 |
|---|---|---|
| 공정 | LiH₂PO₄ + Zr(NO₃)₄·5H₂O 에탄올 졸 → NCM85 분산 (액:고 10:1) → 80 °C 건조 → 진공 → **750 °C O₂ 2 h** · 0/0.5/1.0/3.0 wt% | SI p.2–3 |
| 구조 | R-3m 유지 · (003) 피크가 함량에 따라 고각 이동 (`figure-read ≈` 18.82° → 18.91° @3 wt%) → *"Zr⁴⁺ or PO₄³⁻ may be trace doped"* | `Fig. S16a` |
| 최적 함량 | **1.0 wt%** (100 사이클 `figure-read ≈` 189 → 175 vs bare 170 → 32) | `Fig. S16b` |
| 두께·형태 | **~10 nm 균일 비정질** (HRTEM) · EDS Zr·P·O 분포 · XPS Zr⁴⁺ (3d₅/₂ `figure-read ≈` 182.0 eV) · P⁵⁺ (2p₃/₂ ≈132.5 eV) · O 1s 표면 O(LiOH·Li₂CO₃) ≫ 격자 O | `Fig. 3f–j` |
| 4.5 V 1st (68:30:2, 0.1 C) | LZC: bare **201.3 / ICE 88.7 %** → LZPO **202.3 / 90.4 %** · LPSC: bare **166.8 / 70.2 %** → LZPO **195.3 / 82.9 %** | `Fig. 4a,b,d,e` |
| 200 사이클 (0.2 C) | LZPO/LZC **83.4 %** · LZPO/LPSC **79.5 %** (`figure-read ≈` 190→158 · 182→145) vs bare LZC ≈15 · bare LPSC ≈80 | `Fig. 4c` |
| 0.5 C 600 사이클 | 초기 ≈145 → `figure-read ≈` 122 / 117 (**>80 %**) | `Fig. 4f` |
| 율속 1.0 C | `figure-read ≈` LZC ≈116 · LPSC ≈125 (**>115**) · 0.1 C 복귀 ≈196 / ≈190 | `Fig. 4g` |
| 고부하 26.0 mg cm⁻², 60 °C, 0.2 C | **>163 mAh g⁻¹** · 200 사이클 **>75 %** (`figure-read ≈` LZC 165→135 · LPSC 163→123) | `Fig. 4h` · `Fig. S20` |
| 레이더 그림 | **눈금 없음** — 정성 | `Fig. 4i` |

### 3f. 계면 저항 (`Fig. S22` — in-situ EIS + DRT, 첫 충전, LZC 셀만)

| 항목 | bare NCM85/LZC | LZPO@NCM85/LZC |
|---|---|---|
| 4.5 V 반원 (`figure-read ≈`) | Z' ≈110 → ≈880 Ω | Z' ≈100 → ≈400 Ω |
| DRT γ(τ) 봉우리 τ ≈2×10⁻⁴ s (= 논문 R_CAM/SE) 높이 (`figure-read ≈`, 3.7/4.1/4.3/4.4/4.5 V) | 35 / 92 / 136 / 250 / **348 Ω** | 22 / 47 / 71 / 90 / **118 Ω** |
| τ ≈1–10 s (확산) | ≈240–320 Ω | ≈50–110 Ω |
| 논문 서술 | *"R_CAM/SE of bare NCM85 rose sharply, whereas that of LZPO@NCM85 increased slowly even beyond 4.3 V"* | |

> ⚠ γ(τ) 의 **봉우리 높이는 저항이 아니다**(저항은 면적). 위 값은 상대 크기만 본다. 꺾임은 **4.1 → 4.3 V 사이에서 시작해 4.3 → 4.5 V 에서 가파르다** — 할라이드 산화 개시(CV ≈3.9–4.1 V)와 같은 자리다.

### 3g. XPS (`Fig. 5` · 200 사이클 후 · 0.2 C)

| 셀 | 관측 | 해석 (논문) |
|---|---|---|
| NCM85/LZC pristine · 4.2 V | Zr⁴⁺ 3d₅/₂ **182.8 eV** · Cl⁻ 2p₃/₂ **198.5 eV** — 변화 없음 | LZC 온전 |
| NCM85/LZC 4.5 V | 새 이중선 **Clₓ⁻ 199.0 eV** (`figure-read` 넓어진 Cl 2p) · **Zr 3d 불변** | 심한 LZC 산화 |
| LZPO@NCM85/LZC 4.5 V | Clₓ⁻ 없음 | 코팅이 산화 억제 |
| NCM85/LPSC pristine (**섞기만 한** 전극) | PS₄³⁻ + **P₂Sₓ** 이중선 | NCM85–LPSC **화학적 비호환** |
| NCM85/LPSC 4.2 V | P₂Sₓ 증가 | 계면 산화 |
| NCM85/LPSC 4.5 V | **Li₃PO₄ 133.5 · Li₂SO₃ 166.8 · Li₂SO₄ 168.9 eV** (SO₃²⁻·SO₄²⁻·PO₄³⁻) | 격자 산소 관여 **산소화 분해** (ref [46,47] = Zuo) |
| LZPO@NCM85/LPSC 4.5 V | 같은 종들이 **약해졌지만 남아 있다** (`figure-read`: SO₄²⁻·SO₃²⁻·PO₄³⁻·P₂Sₓ 모두 보임) | 코팅이 부반응·격자 산소를 안정화 |

### 3h. 계산 값 — DOS 갭은 그림에 **인쇄된 값**, 반응에너지는 **`figure-read ≈`** (판독표는 `## DFT 절 논리 감사` §C)

| 상 | PBE 갭 (eV, 인쇄값) | 출처 | 논문의 분류 |
|---|---|---|---|
| NiO | **1.97** | `Fig. S11` | §2.2: *"insulating NiO-like phase"* |
| P₂S₅ | 2.26 | `Fig. S25c` | narrow (unfavorable) |
| InClO | 2.20 | `Fig. S28b` | — |
| In₂O₃ | 0.76 | `Fig. S28b` | — |
| Li₂S | 3.14 | `Fig. S25b` | narrow (unfavorable) |
| ZrCl₄ | 3.37 | `Fig. S24b` | narrow |
| **ZrO₂** | **3.40** | `Fig. 6d` | *"narrow band gap … i.e., high electronic conductivity"* |
| Li₂ZrO₃ | 3.64 | `Fig. S24c` | narrow |
| **LZPO** | **4.06** | `Fig. 6f` | *"wide band gaps"* |
| Li₃PO₄ | 5.94 | `Fig. S25a` | wide |
| Li₂SO₄ | 6.01 | `Fig. 6e` | wide |
| LiCl | 6.22 | `Fig. S24a` | (분류 없음 — "보호 실패") |

---

## 4. DFT/계산 방법 ★

> **SI p.5 원문 전문**: *"First principle calculations are adopted to calculate the density of state (DOS) using density-function theory (DFT) implemented in a plane-wave-based Vienna ab initio simulation package (VASP) [6]. Structural relaxations and static energy calculations were carried out using the generalized gradient approximation (GGA) with the Perdew, Burke, and Ernzerhof (PBE) functional [7]. The cutoff energy for the plane-wave basis is set to be 500 eV for all atoms. The ion coordinates are relaxed freely with an energy convergence threshold of 10⁻⁶ eV/atom and a force tolerance of 0.02 eV/Å on each atom. Additionally, the mutual reaction energies of potential decomposition reactions between the cathode/electrolyte interface composition were examined along the pseudobinary phase diagrams with varying reactant fractions, using the scheme proposed in previous studies and material energies obtained from the Materials Project (MP) database [8, 9]."*
>
> ⇒ **두 계산이 서로 다른 에너지 출처를 쓴다**: DOS·갭 = **자체 VASP-PBE** / 반응에너지 = **MP 데이터베이스 에너지**(MP 는 전이금속 산화물에 GGA+U 와 혼합 보정을 쓴다 — 판본 미기재).

| 항목 | 기재 | 비고 |
|---|---|---|
| code | VASP (ref Kresse–Furthmüller 1996) | 버전 **미기재** |
| functional | GGA-PBE | vdW **미기재** (없음으로 읽힌다) |
| pseudo / PAW | **미기재** | VASP 라 PAW 로 추정 · POTCAR **미기재** |
| ecut | **500 eV** | |
| k-points | **미기재** | 갭·DOS 에 직접 영향 |
| 수렴 | 에너지 10⁻⁶ eV/atom (⚠ VASP EDIFF 는 셀 단위라 단위가 어색) · 힘 0.02 eV/Å · *"ion coordinates are relaxed freely"* | 셀 이완 여부 **미기재** |
| DFT+U | **미기재** | ⚠ `Fig. S11` NiO 갭 1.97 eV 는 순수 PBE 로는 나오기 어렵다(일반 지식: PBE NiO 갭은 ≲1 eV 급) → **+U 등 미기재 설정 의심** (판정 보류) |
| 스핀 | **미기재** | `Fig. S11` NiO DOS 는 스핀 분극이고 **위·아래 채널이 비대칭** = 순자화 있는 **강자성 배열로 보인다** (`figure-read`) — 실험 바닥상태(AFM-II)와 다르다 |
| 갭 판독법 | **미기재** | 그림이 DOS 라 **DOS 가장자리 판독**일 가능성 — 우리 규율상 DOS-threshold 판독은 ~0.3 eV 과소 |
| 다형 · MP ID | **미기재** | ZrO₂(단사?) · Li₃PO₄(β/γ?) · Li₂SO₄ · P₂S₅ · LZPO(NASICON R-3c? 저온 삼사정?) 전부 모른다 |
| 상호반응에너지 형식 | Zhu–He–Mo [8,9] pseudo-binary · **닫힌계**(Li 저장고 안 엶) | 전압은 μ_Li 가 아니라 **양극 조성 두 점**(LiNiO₂ / Li₀.₂₅NiO₂)으로만 들어온다 |
| MP 판본 · 보정 체계 · 엔트리 ID | **미기재** | **재현 불가** — 우리 CEI 카드 G1 (*"기록 없는 hull 은 값이 아니다"*) 기준 탈락 |
| Li₀.₂₅NiO₂ 에너지의 출처 | **미기재** | MP 에 그 조성 엔트리가 없으면 pymatgen `InterfacialReactivity` 는 **경고 후 hull 에너지**를 쓴다 (우리 venv pymatgen 2026.9.24 소스 `_get_entry_energy` 확인). 그 경우 반응물은 '탈리튬 층상상' 이 아니라 **그 조성의 평형 혼합물**이 된다 — 논문이 pymatgen 을 썼는지조차 안 적었다 |
| 정규화 · x 정의 | y = *"Reaction energy (eV/atom)"* · x = *"Ratio of A in mixture A/B"* | 원자 정규화인지 화학식 단위인지 **미기재** |
| 최소값·산물 | 곡선만 — **꺾임 산물·반응식 보고 0** | `Table S1` 이론 산물은 **인용**(Kochetkov [10] · [Xiao19] [11]) |
| 표현 선택 | NCM85 → **LiNiO₂** (*"for ease of calculation [48]"*) · **LZC → LiCl + ZrCl₄ 분리** (*"Considering the low crystallinity of LZC"*) · LPSC·LIC·LZPO 는 **화합물 그대로** · P₂Sₓ → **P₂S₅** | §감사 1단계 |
| 열린 껍질 상태 선택 | **미기재** | LiNiO₂(Ni³⁺) · Li₀.₂₅NiO₂ 는 열린 껍질·산화환원 활성 — MP 를 썼다면 MP 의 상태 선택(GGA+U · 강자성 초기화)을 그대로 물려받는다 |
| AIMD · MLIP · NEB · Bader · COHP | 없음 | |
| 무질서 처리 | 해당 없음 (전부 질서 결정 · 실제 LZPO 코팅은 **비정질**) | |

---

## 5. 결과 서사 (본문 순서)

### 5.1 §2.1 컷오프 전압 — 4.2 V 는 LZC 우세, 4.5 V 는 엇갈린다 (`Fig. 1` · `Fig. S1`–`S6`)
- 두 catholyte 의 물성 확인(§3a) 후, **산화 한계를 고려해** 먼저 2.7–4.2 V. LZC 셀이 ICE(89.5 vs 76.1 %)·과전압·감쇠 모두 우세하지만 1.0 C 에서는 ≈65 < ≈75 mAh g⁻¹ 로 LPSC 에 진다(`Fig. S5a`).
- 2.7–4.5 V 로 넓히면: LZC 셀은 0.1 C 3 사이클 동안 ≈180 이 유지되다 0.2 C 에서 **분극 누적으로 급감**, LPSC 셀은 처음 3 사이클에 **−20.3** 잃고 그 뒤 완만(200 사이클 78.7 %) — *"The underlying reasons for this anomaly will be elaborately explained in the last section"* (= DFT 절이 이걸 설명하겠다는 약속).
- EIS(`Fig. S6`): 100 사이클 뒤 내부저항이 크게 늘고 특히 LZC 셀 — *"primarily attributed to the oxidative decomposition of catholytes and the structural transformation of CAMs [34]"*.

### 5.2 §2.2 질량분율 — 탄소는 양날의 칼 (`Fig. 2` · `Fig. S7`–`S15`)
- 70:30 복합체는 *"catholyte itself blocked the electron transport"* → VGCF 투입. 4.2 V LZC 셀은 2 wt% 로 전면 개선(178.4 · ≈98 @1 C · 85.7 %), **LPSC 셀은 오히려 악화** — XPS P₂Sₓ 증가(`Fig. S10`) = *"VGCF accelerated catholyte decomposition"*.
- 4.5 V: 2 wt% 가 초기 방전 +23.7 · H2→H3 전이 뚜렷 → *"not significantly diminished by … insulating NiO-like phase (1.97 eV, Fig. S11)"* ← ⚠ **여기서 NiO(PBE 1.97 eV)를 "절연" 이라 부른다** (§감사 6단계에서 다시 나온다). 그러나 장기 사이클은 극히 나쁘고, 5 wt% 는 50 사이클에 13.0 mAh g⁻¹.
- σ_e: NCM85 4.26×10⁻² → LZC 와 섞으면 1.78×10⁻⁴ (*"embedding of NCM85 particles into the deformed electrolyte powders"*) → 2 wt% VGCF 로 2.86×10⁻². LPSC 복합체(1.36×10⁻²)가 LZC 복합체(2.86×10⁻²)보다 낮은 것을 *"formation of insulating interphase between NCM85 and LPSC"* 로 돌린다 — ⚠ 2 배 차, 시료 1 개, 오차 없음 → 귀속은 추정.
- 고부하 26 mg cm⁻² · 60 °C(`Fig. S15`)도 같은 양상 → 결론 `Fig. 2i`: 탄소 = 초기 용량↑ · 장기 계면 안정성↓.

### 5.3 §2.3 계면 조성 — LZPO 코팅 (`Fig. 3` · `Fig. 4` · `Fig. S16`–`S22`)
- 졸–겔 LZPO, 1.0 wt% 최적(`Fig. S16b`). (003) 이동 → 미량 도핑 가능성을 **본인들이 적는다**. ~10 nm 비정질 껍질(`Fig. 3f`).
- 4.5 V 비교(§3e): ICE·초기 방전·장기·율속·고부하 전부 LZPO 우세. 개선 폭은 **LPSC 셀에서 훨씬 크다**(ICE +12.7 %p vs +1.7 %p) — 황화물–산화물 **화학 접촉 차단**이 효과의 본체라는 해석과 맞는다.
- EIS(`Fig. S21`)·in-situ EIS/DRT(`Fig. S22`): bare NCM85/LZC 의 R_CAM/SE 가 **4.3 V 위에서 급등**, LZPO 는 완만.

### 5.4 §2.4 전반 — XPS (`Fig. 5`)
- LZC: 4.2 V 무변화, 4.5 V 에 Clₓ⁻(199.0 eV) → 4.5 V 열화 = **Cl⁻ 산화**. Zr 3d 는 끝까지 불변.
- LPSC: **섞기만 해도 P₂Sₓ** → 4.2 V P₂Sₓ↑ → 4.5 V 산소화 산물(Li₃PO₄·Li₂SO₃·Li₂SO₄) = *"release of reactive oxygen ions from the surface layer of the unstable NCM lattice"*. LZPO 가 이것들을 약화(소멸 아님).

### 5.5 §2.4 후반 — 계산 해석 (`Fig. 6` · `Fig. S23`–`S28` · `Table S1`·`S2`) → **`## DFT 절 논리 감사`** 에서 단계별로 다룬다.

### 5.6 결론
*"NCM85/LZC electrodes feature unlimited interfacial degradation at 4.5 V, originating from moderate interface reactivity and unfavorable reaction products. In contrast, NCM85/LPSC electrodes feature self-limited interfacial degradation at 4.5 V, resulting from high interface reactivity and partially favorable reaction products."* — 결론의 두 원인절(*"originating from… / resulting from…"*)이 **둘 다 DFT 절에서 온다**. 그래서 DFT 절의 논리가 결론의 무게를 그대로 진다.

---

## DFT 절 논리 감사

> 범위: 본문 p.7 오른쪽 아래(*"Based on the experimental findings, theoretical calculations were employed…"*) → p.9 *"…to fully unlock the great potential of high-voltage ASSLBs."* + SI p.5 방법 + `Fig. 6` · `Fig. S11` · `Fig. S23`–`S25` · `Fig. S28` · `Table S1` · `Table S2`. p.8 은 2단 조판이라 텍스트 추출 순서가 섞여서 **쪽을 렌더해 원래 순서로 읽었다**.
> 판정 어휘: **지지**(계산이 그 결론을 직접 준다) · **부분 지지**(일부만 준다 / 조건이 붙는다) · **비약**(계산이 그 결론을 주지 않는다) · **모순**(자기 그림·표·다른 문장과 어긋난다).

### A. 이 절의 계산이 실제로 잰 것

| 계산 | 적힌 설정 | 실제로 잰 양 | 논문이 그 양에 시킨 일 |
|---|---|---|---|
| 상호반응에너지 (`Fig. 6a–c`, `Fig. S28a`) | Zhu–He–Mo 닫힌계 pseudo-binary · MP 에너지 | 두 **고정 조성** 상을 x:(1−x) 로 섞었을 때 평형 상 집합까지 내려가는 **열역학 구동력** (eV/atom, 0 K, 혼합비별) — 속도·두께·전압(μ_Li) 없음 | ① 크기 → **초기 사이클 안정성** ② 산물 vs 충전 양극 → **장기 산물 우호도** |
| PBE 밴드갭 (`Fig. 6d–f`, `Fig. S11`, `Fig. S24`, `Fig. S25`, `Fig. S28b`) | 자체 VASP-PBE · +U·스핀·k·판독법 미기재 | 완전 결정 벌크의 **KS 갭** (PBE 는 체계적 과소) | **전자전도도·전자 터널링 차단·Li⁺ 전달**의 판정 |
| `Table S1` 산물 | 실험 열 = XPS · 이론 열 = **인용** (LZC: Kochetkov [10] / LPSC: [Xiao19] [11] / LZPO@LPSC: 출처 "/") | 이 논문 `Fig. 6` 의 꺾임 산물이 **아니다** | "산물 X 가 생긴다" 는 전제 |
| `Table S2` 코팅 등급 | 5 종 × (전자전도 · 이온전도 · 산화한계 · 코팅효과) 정성 등급 + 문헌 | **계산 0** — 문헌 인용 등급표 | *"further validating the superiority of LZPO"* |

### B. 논증 사슬 — 10 단계와 화살표별 판정

| # | 단계 (원문 요지) | 근거로 든 것 | 판정 |
|---|---|---|---|
| P | 전제(실험): 4.5 V 에서 LZC 셀 = 초기 양호·장기 붕괴 / LPSC 셀 = 초기 손실·장기 완만 / LZPO 가 둘 다 고친다 / XPS 산물 (§3c–3g) | `Fig. 1`·`Fig. 4`·`Fig. 5` | ✅ 전제 자체는 그림과 맞는다 (`figure-read` 확인) |
| 1 | 모형화: NCM85 → LiNiO₂ · Li₀.₂₅NiO₂ / **LZC → LiCl + ZrCl₄** (*"low crystallinity"*) / MP 닫힌계 | SI p.5 · 본문 p.7 | 🔴 **비약** — 표현 선택 두 곳이 결론을 미리 정한다 |
| 2 | *"LiNiO₂/LZC interface was relatively stable"* → 4.2 V 우수 · 4.5 V 초기 양호 | `Fig. 6a` | 🔴🔴 **모순** + 비약 |
| 3 | *"moderate reaction energies … with the delithiated cathode (Li₀.₂₅NiO₂)"* → 4.5 V 열화 · *"As a result"* 용량↑·ICE↓ (`Fig. S23a`) | `Fig. 6a` · `Fig. S23a` | 🟡 **부분 지지** (LiCl 한 곡선만) + 마지막 문장은 비약 |
| 4 | *"higher mutual reaction energies … not thermodynamic stable"* → LPSC 초기 불량 | `Fig. 6b` | 🟢 **지지** — 이 절에서 가장 단단한 고리 |
| 5 | *"low mutual reaction energies of LZPO/NCM85 and LZPO/SSEs"* → 코팅 잠재력 · ICE↑ | `Fig. 6c` | 🟢 순위로는 **지지** · 🟡 문턱 불일치 |
| 6 | LZC 장기: 산물 LiCl·ZrO₂·Li₂ZrO₃ → LiCl·Li₂ZrO₃ 산화 취약 [50,51] · **ZrO₂ 좁은 갭 → 높은 전자전도** → LZC 산화 가속 → (XPS 로 ZrO₂·Li₂ZrO₃ **확인 못 함**) → *"Consequently"* 장기 불량 | `Fig. 6a,d` · `Fig. S24` · `Fig. 5a` | 🔴🔴 **비약 + 모순** |
| 7 | LPSC 장기: Li₃PO₄·Li₂SO₄ ≈0 vs Li₀.₂₅NiO₂ + *"high partial ionic conductivities"* + 넓은 갭 → 터널링 차단 / P₂Sₓ·Li₂S 큰 반응·좁은 갭 → *"continuous interfacial degradation"* → LPSC 가 *"relatively better"* | `Fig. 6b,e` · `Fig. S25` · [52,53] | 🟡 **부분 지지** + 🔴 표와 모순 1 |
| 8 | LZPO: *"negligible"* 반응 + *"high ionic conductivity, wide band gaps, superior oxidation stability"* → 우수 / `Table S2` 가 *"validating the superiority"* | `Fig. 6c,f` · `Table S2` | 🔴 **비약 (순환)** + 표와 모순 1 |
| 9 | 종합: LZC = 중간 반응 · 저항성 계면 · **channel block** · **unlimited** / LPSC = 큰 반응 · 부분 우호 산소화 계면 · **partially block** · **self-limited** / LZPO = 낮은 반응 · 원활 수송 | `Fig. 6g` | 🔴 **비약** (열역학 → 성장 법칙) |
| 10 | 일반화: *"also applicable to … LIC"* · *"considering the lower reactivity of the NCM85/LIC interface (Fig. S28), the capacity decay rate was slower"* | `Fig. S26`–`S28` | 🔴 **비약** (표현 교락 + 다른 변수 교락) |

### C. 판독표 — `Fig. 6a–c` · `Fig. S28a` (400 dpi 재렌더 · 마커 색 중심 · `figure-read ≈`)

> 보정: y 는 녹색 0 선과 틀 하단(= 축 최솟값)으로, x 는 x=0·1 끝점 마커 중심으로 맞췄다. 정밀도 ≈ ±0.005 eV/atom (a·c·S28a) · ±0.01 (b). x 는 논문 축 *"Ratio of A in mixture A/B"* 그대로 (정의 미기재).

| 패널 | 곡선 (A/B) | 최소 반응에너지 (eV/atom) | 최소의 x | 비고 |
|---|---|---|---|---|
| 6a | LiCl / LiNiO₂ | **0** | — | 반응 없음 |
| 6a | LiCl / Li₀.₂₅NiO₂ | **−0.08** | ≈0.10 | 탈리튬에서 **켜진다** |
| 6a | **ZrCl₄ / LiNiO₂** (방전) | **−0.22** | ≈0.48 | ⚠ **패널 최저** |
| 6a | ZrCl₄ / Li₀.₂₅NiO₂ (충전) | **−0.21** | ≈0.46 | 방전 상태와 **같은 크기** |
| 6a | ZrO₂ / Li₀.₂₅NiO₂ | 곡선이 **안 보인다** | — | 0 선(녹색) 아래 가림으로 추정 — 판독 불가 |
| 6a | Li₂ZrO₃ / Li₀.₂₅NiO₂ | −0.025 | ≈0.60 | |
| 6b | LPSC / LiNiO₂ (방전) | **≈ −0.42** | ≈0.36–0.5 (평탄) | |
| 6b | LPSC / Li₀.₂₅NiO₂ | **−0.72** | ≈0.43 | |
| 6b | Li₂S / Li₀.₂₅NiO₂ | −0.62 | ≈0.17–0.30 | |
| 6b | P₂S₅ / Li₀.₂₅NiO₂ | **−0.86** | ≈0.29–0.33 | P₂Sₓ 의 대리 |
| 6b | Li₃PO₄ / Li₀.₂₅NiO₂ | 곡선이 **안 보인다** | — | 0 선 아래 가림으로 추정 |
| 6b | Li₂SO₄ / Li₀.₂₅NiO₂ | **0** | — | |
| 6c | **LZPO / LiNiO₂** (방전) | **−0.07** | ≈0.35 | ⚠ 충전보다 **방전** 양극과 더 반응 |
| 6c | LZPO / Li₀.₂₅NiO₂ | −0.02 | ≈0.15 | |
| 6c | LZPO / LPSC | −0.03 | ≈0.26 | |
| 6c | LZPO / LiCl | 곡선이 **안 보인다** | — | 0 선 아래 가림으로 추정 |
| 6c | LZPO / ZrCl₄ | **0** | — | |
| S28a | LIC / LiNiO₂ (방전) | −0.09 | ≈0.45 | |
| S28a | LIC / Li₀.₂₅NiO₂ | −0.115 | ≈0.17 | |
| S28a | InClO / Li₀.₂₅NiO₂ | −0.10 | ≈0.17 | |
| S28a | In₂O₃ / Li₀.₂₅NiO₂ | **0** | — | |

### D. 단계별 상세

#### 1단계 — 모형화: 표현 선택 두 곳이 결론을 미리 정한다 (`Fig. 6a`)
- **LZC 를 원료 둘로 쪼갰다.** 근거 *"Considering the low crystallinity of LZC"* 는 근거가 되지 않는다: ① 볼밀 LZC 는 **단상**이다(`Fig. S1a` 가 Li₃YCl₆ 형으로 지수) — LiCl 과 ZrCl₄ 의 물리 혼합물이 아니다 ② 결정성이 낮으면 에너지가 **높아져** 반응성은 오히려 커진다 — 결정 원료 둘로 바꾸면 그 방향도 표현하지 못한다 ③ 같은 논문이 **LIC 는 화합물로** 계산했다(`Fig. S28a`) — 일관성이 없다. 결과적으로 ZrCl₄ 가 **LiCl 에 희석되지 않은 채** 양극과 단독으로 맞붙는다.
- **전압을 μ_Li 가 아니라 양극 조성 두 점으로 넣었다.** 닫힌계에서는 그 방법밖에 없지만, 두 점이 실제 전압과 어떻게 대응하는지 검산하지 않았다 → 2·3단계에서 그 대가가 나온다.
- 판정: **비약**. 계산 결과 이전에 '할라이드 쪽은 ZrCl₄ 가 지배하고, 전압 효과는 조성 두 점 차이로만 보인다' 가 구조적으로 정해진다.

#### 2단계 — *"LiNiO₂/LZC interface was relatively stable"* (`Fig. 6a`)
- 그림에는 **'LZC/LiNiO₂' 곡선이 없다.** 있는 것은 LiCl/LiNiO₂(**0**)와 ZrCl₄/LiNiO₂(**−0.22**, 패널 최저)다. LZC 의 두 성분 중 하나가 패널에서 **가장 크게** 반응하는데 "비교적 안정" 이라 쓴다 → **모순**.
- 게다가 **LiNiO₂(완전 리튬화 = 방전 상태)는 4.2 V 충전 상태가 아니다.** (우리 산수) NCM85 이론용량 275 mAh g⁻¹(M ≈ 97.47 g mol⁻¹, Li 1 개) 기준, 충전 끝 Li 함량 x 는 `1 − Q_충전/275` 이상 `1 − Q_방전/275` 이하다 (충전 용량엔 부반응이 섞여 있으므로):

| 상태 (`Fig. S23a`, LZC 셀, 0.1 C) | Q 충전 / 방전 (`figure-read ≈`) | x(Li) 범위 (우리 산수) |
|---|---|---|
| 4.2 V · 0 wt% VGCF | 175 / 156 | **0.36–0.43** |
| 4.2 V · 2 wt% VGCF | 198 / 178 | **0.28–0.35** |
| 4.5 V · 0 wt% VGCF | 199 / 177 | **0.28–0.36** |
| 4.5 V · 2 wt% VGCF | 227 / 201 | **0.17–0.27** |
| *모형 Li₀.₂₅NiO₂* | *206 (0.75 Li)* | *0.25* |

  → **4.2 V 상태는 x ≈ 0.3–0.4 로 Li₀.₂₅ 에 훨씬 가깝고 LiNiO₂(x=1)와는 멀다.** 더구나 *"4.2 V + 탄소 2 wt%"* 와 *"4.5 V + 탄소 0"* 은 **같은 탈리튬 깊이**(x ≈ 0.28–0.36)다 — 셀이 실제로 도달한 상태는 컷오프 전압만큼 전자 경로가 정한다. ⇒ `Fig. 6a` 의 두 점 대비는 **'방전 vs 충전'** 이지 **'4.2 V vs 4.5 V'** 가 아니다. 4.2 V 의 우수 사이클을 LiNiO₂ 곡선으로 설명하는 것은 **비약**이다.

#### 3단계 — 탈리튬 양극과 "moderate" 반응 → 4.5 V 열화 (`Fig. 6a`, `Fig. S23a`)
- LiCl 은 **0 → −0.08** 로 탈리튬에서 반응이 켜진다 — 실재하는 신호이고, 우리 `[Xiao19]` 행(§B③ *"탈리튬에서 반응이 켜지는 유일한 음이온 = Cl"*: 106 종 중 이 성질을 가진 7 종이 전부 Cl 함유 · LiCl·LiCsCl₂·LiRbCl₂ 는 완전 리튬화 NCM 에서 0.000 → 반리튬화 NCM 에서 −13~−17 meV/atom)과 **방향이 같다** (크기는 Li₀.₂₅ vs 반리튬화·NCM111 vs LiNiO₂·hull 세대가 달라 비교 금지).
- 그러나 ZrCl₄ 는 **−0.22 → −0.21** 로 리튬화 상태와 무관하다. *"전압이 반응을 켠다"* 는 서사가 **LiCl 한 곡선에만** 걸려 있다. 그리고 2단계 표대로 Li₀.₂₅ 는 4.2 V(2 wt%) 상태와 Δx ≈0.03 차이라 **"4.5 V 고유" 를 말하지 못한다**.
- *"As a result, the initial capacities … gradually enhanced with the increase of cutoff voltage and the introduction of VGCF, but slightly decreasing ICE (Fig. S23a)"* — 용량이 오르는 이유는 **더 깊은 탈리튬 + 전자 경로**(2단계 표)다. 반응에너지에서 나오는 결론이 아니다 → 이 문장은 **비약**(*non sequitur*).
- 판정: **부분 지지** (LiCl 의 부호 전환만).

#### 4단계 — LPSC 의 큰 상호반응에너지 → 초기 불량 (`Fig. 6b`)
- LPSC/LiNiO₂ ≈ **−0.42**(방전 상태에서도), LPSC/Li₀.₂₅NiO₂ ≈ **−0.72** — 할라이드 쪽 어떤 곡선(최저 −0.22)보다 **≈1.9 배 · ≈3.3 배** 깊다 (우리 산수).
- 세 증거가 같은 방향이다: ① 방전 상태와도 크게 반응한다는 계산 ② **섞기만 한 전극에서 이미 P₂Sₓ**(`Fig. 5b` pristine) ③ ICE **70–76 %** vs LZC 89 %. 이 정도면 *"NCM85/LPSC 계면은 화학적으로 비호환이고 그 손실이 첫 사이클에 몰린다"* 는 서술은 **지지**된다.
- 남는 단서: 구동력의 **크기는 속도가 아니다**. "크기 → 초기, 산물 → 장기" 라는 시간축 배정은 계산이 아니라 해석이다. 그리고 우리 비교 기준선(§7-1)과 같은 자릿수다 — 황화물–산화물 양극 계면의 문헌 기준 >300 meV/atom(`[Xiao20Rev]`) 범위.
- 판정: **지지** (이 절에서 가장 단단한 고리).

#### 5단계 — LZPO 의 낮은 상호반응에너지 → 코팅 잠재력 (`Fig. 6c`)
- **양쪽(양극·SE)을 다 본 것은 맞는 설계**다 — 코팅은 두 면 모두에서 안정해야 한다(`[Xiao19]`·Zhu/Mo 프레임). 크기도 −0.02 ~ −0.07 로 bare 쌍(−0.2 ~ −0.86)보다 한 자릿수 작다 → **순위로는 지지**.
- 그러나 ① **문턱이 정의되지 않았다**: LZPO/LiNiO₂ **−0.07** 은 "low → great potential", LiCl/Li₀.₂₅NiO₂ **−0.08** 은 "moderate → degradation" — 같은 크기를 반대로 읽는다 ② LZPO 는 충전(−0.02)보다 **방전 양극과 더 반응**(−0.07)한다 — 서술 없음 ③ 계산 대상은 **결정 LiZr₂(PO₄)₃** 인데 실제 코팅은 **~10 nm 비정질**(`Fig. 3f`) + Zr/PO₄ 일부 격자 도핑(`Fig. S16a`) ④ `Table S1` 이 LZPO@NCM85/LPSC 의 이론 산물로 **Li₃PS₄·Li₃PO₄·LiCl·ZrS₂** 를 적는다 — 반응이 0 이 아니고, XPS 도 코팅 후 산소화 산물이 **남는다**(`Fig. 5b`) ⑤ "negligible" 은 9 단계에서 *"protected the intactness of SSEs"* 로 커진다 — 계산이 준 것보다 강한 말이다.
- 독립 근거는 따로 있다: `[Park26ML]` `Fig. 7` 에서 **인산염화한 Zr**(Li₆Zr(PO₅)₂ −14 ~ −19 meV/atom)이 Zr 산화물(Li₂Zr₂O₅ −70 ~ −105)보다 황화물 SE 와 덜 반응한다 — LZPO 선택의 방향은 이 논문 계산 없이도 선다.
- 판정: 순위로는 **지지**, 서술 강도와 문턱은 **불일치**.

#### 6단계 — LZC 장기 불량의 기전: 갭 → 전자전도 → 비관측 상 위의 인과 (`Fig. 6d`, `Fig. S24`, `Fig. 5a`)
원문 순서: *"LiCl, ZrO₂, and Li₂ZrO₃ emerged as the most favorable interfacial components. However, LiCl and Li₂ZrO₃ were ineffective in protecting the CAMs, susceptible to oxidation during Li extraction at 4.5 V [50,51]. Moreover, ZrO₂ was not a Li⁺ conductor and exhibited a narrow band gap similar to Li₂ZrO₃ or ZrCl₄ (Fig. 6d and Fig. S24), i.e., high electronic conductivity, which limited interfacial Li⁺ transfer and accelerated LZC oxidation. Notably, Zr 3d XPS spectra of the cycled cathode at 4.5 V (Fig. 5a) failed to confirm the existence of ZrO₂ or Li₂ZrO₃, which was merely predicted from the calculation. Consequently, the NCM85/LZC cell exhibited poor long-cycle stability at 4.5 V…"*
1. **산물 목록이 이 논문 계산에서 나왔다는 근거가 없다** — `Fig. 6a` 는 꺾임 산물을 안 적고, `Table S1` 의 이론 산물(NiO·LiClO₄·LiCl·ZrCl₄·ZrO₂·Li₂ZrO₃)은 Kochetkov [10] **인용**이다. `Fig. 6a` 가 한 일은 *"그 산물들이 충전 양극과 또 반응하나"* 뿐이다.
2. **갭 → 전자전도도는 비약이다.** PBE 갭은 수송량이 아니다. 넓은 갭 절연체의 σ_e 는 **캐리어(결함·폴라론) 농도**가 정한다 — 우리 §D 의 외부 반례 `[Ma]`(갭 +0.52 eV 에 σ_e 1.2 배) · `[Wu26]`(갭 +0.54 eV 는 진성이면 3.4×10⁴ 배 감소 예측, 실측 6.9 배). ZrO₂ 의 PBE 3.40 eV 는 일반적 의미의 "좁은 갭" 도 아니다.
3. **🔴🔴 자기모순**: §2.2 는 *"insulating NiO-like phase (1.97 eV, Fig. S11)"* — **1.97 eV 를 절연**이라 부르고, §2.4 는 **3.40 eV 를 "high electronic conductivity"** 라 부른다. 같은 논문, 같은 방법, 1.4 eV 더 넓은 쪽이 전도체다. 암묵 문턱은 ZrO₂·Li₂ZrO₃(3.40·3.64)와 LZPO(4.06) 사이 어딘가인데 **어디에도 적혀 있지 않다**.
4. **기전의 주인공이 관측되지 않았다고 스스로 적은 직후 "Consequently"** — ZrO₂·Li₂ZrO₃ 가 *"merely predicted"* 라고 쓴 다음 문장이 그 상의 성질로 장기 불량을 결론낸다. 비관측 상 위의 인과다. (덧붙여 Zr 3d 로는 염화물–산화물 Zr⁴⁺ 구분력 자체가 약할 수 있다 — 일반 지식 · 판정 보류. 그렇다면 "비검출" 은 어느 쪽 증거도 아니다.)
5. **실제로 관측된 산물(Clₓ⁻, 199.0 eV)은 계산하지 않았다.** `Fig. 6g` 범례는 이를 *"LiClₓ"* 라는 저항성 상으로 그리지만, 그 상의 반응에너지도 갭도 없다. `Table S1` 의 '실험 산물' 열에 ZrCl₄·LiCl 이 있는데, `Fig. 5a` 의 Zr 3d·Cl⁻ 신호는 **LZC 자신과 구분되지 않는다** — 실험 산물이라 부르기 어렵다.
6. **기준이 사례마다 바뀐다**: LiCl 은 계산된 상 중 **갭이 가장 넓은데**(6.22 eV) "보호 실패"(산화 취약 — 문헌 [50,51], 계산 아님)이고, 7 단계에서 Li₃PO₄·Li₂SO₄(5.94·6.01)는 **넓은 갭이라 좋다**. 그리고 LiCl 은 LPSC 쪽 이론 산물(`Table S1`)에도 있는데 그 쪽 서사에서는 언급되지 않는다.
- 판정: **비약 + 모순**. 이 단계가 결론의 *"unfavorable reaction products"* 의 실체인데, 계산이 준 것은 "산물 후보들이 충전 양극과 반응을 거의 안 한다(ZrO₂ 0, Li₂ZrO₃ −0.025)" 뿐이다 — 오히려 **"그 산물들은 양극 쪽으로는 안정"** 이라는 반대 방향 정보다.

#### 7단계 — LPSC 장기: "부분 우호" 산물 (`Fig. 6b,e`, `Fig. S25`)
- Li₃PO₄·Li₂SO₄ 가 Li₀.₂₅NiO₂ 와 ≈0 인 것은 그림과 맞는다(Li₃PO₄ 곡선은 0 선에 가려 판독 불가). Janek [53]의 LPSC 유래 코팅도 방향이 맞다.
- ⚠ **본문–SI 모순**: 본문 *"high partial ionic conductivities [52]"* vs `Table S2` Li₃PO₄·Li₂SO₄ 이온전도도 **"low"**. ([52] Homma 2020 은 Li₃PO₄–Li₃BO₃–Li₂SO₄ **혼합물**을 ML 로 최적화한 논문 — 순수 상의 값이 아니다.)
- **절반만 계산했다**: 산물 vs **양극**만 봤고 산물 vs **LPSC 쪽**은 안 봤다. 계면층이 자기제한이 되려면 두 면 모두에서 안정해야 한다(5단계에서 LZPO 에는 그 잣대를 썼다).
- *"prevent electron tunneling"* — 터널링은 **두께**와 전극 페르미 준위 대비 **장벽 높이(밴드 정렬)** 의 문제다. 벌크 갭만으로는 정해지지 않는다.
- *"unfavorable reaction products like P₂Sₓ and Li₂S … triggered **continuous** interfacial degradation"* — 초록·결론의 ***"self-limited"*** 와 긴장한다. 이 절 자신의 마지막 말은 *"relatively better"* 다.
- P₂Sₓ 를 결정 P₂S₅ 로 대리 · 같은 연구실의 Li₂S PBE 갭이 편마다 다르다: `[Li25]` 3.04 · **이 편 3.14** · `[LiGaF]` **4.2 eV** — 이 편의 암묵 문턱(≈3.7–4.0)을 **사이에 두고 갈린다** → 갭 문턱 분류가 설정에 따라 뒤집힌다.
- 판정: **부분 지지** (산물 vs 양극 안정만) + 표와 **모순** 1.

#### 8단계 — LZPO 우위: 순환 논증 (`Fig. 6c,f`, `Table S2`)
- *"superior oxidation stability"* — **계산하지 않았다**. 우리 litdb 의 `[Xiao19]` `Table 3` 이 grand-potential 로 준다: **LiZr₂(PO₄)₃ 산화한계 4.52 V**(→ Zr₂P₂O₉ + ZrP₂O₇ + O₂) vs **Li₂ZrO₃ 3.44 V**(→ ZrO₂ + O₂). 방향은 논문과 같지만 **4.5 V 컷오프 대비 여유 0.02 V** 다 (MP-2018 hull · 0 K — 이 여유를 "우수" 로 읽을 수 없다).
- **갭 논리를 그대로 따르면 LZPO 가 셋 중 가장 나쁜 전자 절연체**다: LZPO 4.06 < Li₃PO₄ 5.94 < Li₂SO₄ 6.01 eV. `Table S2` 도 LZPO 전자전도도를 **"medium"**, Li₃PO₄·Li₂SO₄ 를 **"low"** 로 매긴다.
- **본문–SI 모순**: 본문 *"LZPO possessed high ionic conductivity"* vs `Table S2` **"medium"**. LZPO 가 Li₃PO₄·Li₂SO₄ 를 이기는 칸은 `Table S2` 에서 **이온전도 medium vs low 하나**뿐이고 그것도 문헌 등급이다.
- *"Table S2 … further validating the superiority of LZPO"* — `Table S2` 는 결론("good")이 이미 적힌 **정성 등급표**다. 결론을 담은 표가 결론을 검증할 수 없다 → **순환**.
- 판정: **비약(순환)** + 표와 **모순** 1.

#### 9단계 — 종합 `Fig. 6g`: 열역학에서 성장 법칙으로
- "self-limited / unlimited" 는 **계면층 성장 법칙**(두께-시간, 예: √t 포화 vs 선형)에 관한 말이다. 이 논문은 성장 법칙을 **재지 않았다** — 근거는 용량 궤적의 모양(`Fig. 1f`, `Fig. 4c`)과 **200 사이클 후 XPS 한 점**이다. 계산은 구동력(eV/atom)과 벌크 갭뿐이다 → 계산에서 성장 법칙으로 가는 화살표는 **비약**.
- "channel block / partially block" — 이온 수송을 계산하지 않았다(NEB·BVSE·MD 0).
- 그림 결함: 가운데 패널 SE 라벨이 **"LPSC₁.₅"** — 이 논문 SE 는 Li₆PS₅Cl 다 (`figure-read` · 다른 계 그림에서 옮긴 흔적일 가능성 · 원인 미상).
- 판정: **비약**.

#### 10단계 — LIC 일반화 (`Fig. S26`–`S28`)
- 실험 차는 크다: (우리 산수) 같은 조건(4.5 V · 0.2 C · 2 wt% VGCF · 10.4 mg cm⁻²)에서 100 사이클 유지 LIC `figure-read ≈` 182 → 122 (**≈67 %**, `Fig. S27b`) vs LZC 170 → 32 (**≈19 %**, `Fig. 4c`).
- 그러나 원인 배정이 교락돼 있다: ① **표현이 다르다** — LIC 는 화합물(원자당 값이 LiCl 로 희석), LZC 는 원료(ZrCl₄ 단독). LIC/Li₀.₂₅NiO₂ −0.115 vs ZrCl₄/Li₀.₂₅NiO₂ −0.21 의 차가 화학인지 표현인지 가를 수 없다 ② LIC 는 **σ 1.83 vs LZC 0.54 mS cm⁻¹ (3.4 배)** 이고 열처리 결정상이다 — 이온 수송 차만으로도 감쇠 속도가 달라진다(`[Zuo]` digest §3f 의 R_cat 교훈과 같은 구조) ③ 셀 1 개 · 100 사이클.
- 또 LIC/LiNiO₂(**방전** 상태) −0.09 는 이 논문 어휘로 *"moderate"*(−0.08) 급이다 — "낮은 반응성" 이 아니다.
- 판정: **비약**. *"also applicable to other halide-based cathodes"* 는 셀 1 개로 일반화한 말이다.

### E. 종합 판정 — 사용자 질문 *"논리의 전개가 맞는가"* 에 대한 답

1. **이 절은 계산이 결론을 *증명* 하는 구조가 아니라, 실험 결론에 계산을 *해석 장치* 로 덧붙인 구조다.** 결론의 세 기둥(LZC 무제한 · LPSC 자기제한 · LZPO 우위)은 용량 궤적·XPS·EIS 에서 왔고, DFT 는 그것을 설명하는 이야기를 준다.
2. **단단한 고리는 하나다** — 4단계: *LPSC–NCM85 는 화학적으로 비호환이고 손실이 첫 사이클에 몰린다* (계산·pristine XPS·ICE 세 방향 일치).
3. **무너지는 고리**: 2단계(자기 그림과 모순) · 6단계(갭 → 전도도 비약 + NiO/ZrO₂ 자기모순 + 비관측 상 위의 "Consequently") · 8단계(순환) · 9단계(열역학 → 성장 법칙).
4. **구조적 결함 둘**이 2·3·6·10단계를 같이 끌어내린다: ① LZC 를 원료 둘로 쪼갠 대리 ② 전압을 고정 조성 두 점으로 넣은 닫힌계 — 자기 충전용량으로 검산하면 두 점은 '4.2 vs 4.5 V' 가 아니라 '방전 vs 충전' 이다.
5. **표–본문 모순 둘**(Li₃PO₄·Li₂SO₄ 이온전도 high↔low · LZPO high↔medium)은 심사에서 걸렸어야 할 오류다 (접수 → 수락 21 일, 수정·수락 같은 날).
6. **재현 불가**: MP 판본·보정·엔트리 ID·Li₀.₂₅NiO₂ 출처·+U·스핀·k점·갭 판독법이 전부 미기재.

⇒ **허용 서술 범위** (이 절을 인용한다면 이 정도까지): *"닫힌계 pseudo-binary 상호반응에너지로 보면 Li₆PS₅Cl 은 LiNiO₂ 대리 양극과 할라이드보다 수 배 큰 구동력으로 반응하고(방전 상태에서도), 결정 LiZr₂(PO₄)₃ 는 양극·SE 양쪽과 한 자릿수 작은 구동력을 보인다."* 그 이상(무제한/자기제한의 기전, 산물의 전자전도, LZPO 의 산화안정 우위)은 이 논문 계산으로 말할 수 없다.

### F. 이 절을 '맞게' 하려면 필요했던 것 (우리 방법으로 번역)

| 빠진 것 | 무엇으로 | 우리 쪽 대응물 |
|---|---|---|
| LZC 를 화합물로 | MP Li₂ZrCl₆ 엔트리(또는 자체 계산) — 원료 대리 금지 | 우리 `[Cha]` 행: *"Zr 가 우리 hull 에 없어 아직 정량 못 함"* — 이 논문은 그 공백을 메우지 않는다 |
| 전압 축 | Li 열린계 grand-potential 반응성 ΔE(x, V) (Richards/Ong 2016) **또는** 측정 충전용량에 맞춘 조성 사다리(x = 1, 0.4, 0.3, 0.2 …) | `interface_reactivity_v2.py` 기본 모드 (μ_Li = μ_Li(metal) − V) |
| 꺾임 산물·반응식 | 최소 꺾임의 반응식을 표로 | 우리 도구는 `want_kinks` 로 전 꺾임 보고 · 끝점 판정(`endpoint_verdict`) |
| 산물의 양면 안정성 | 산물 vs 양극 **그리고** 산물 vs SE | `[Xiao19]` 깔때기 · LZPO 에만 한 일을 산물 전부에 |
| 산물·코팅의 산화한계 | grand-potential V_ox (`[Xiao19]` `Table 3` 형식) | `esw_grand_potential.py` 와 같은 기계 |
| 전자 쪽 | 갭은 **금속/비금속 게이트**로만 · 판정은 실측 σ_e (이 연구실은 DC 분극을 이미 한다 — ZrO₂·LZPO 박막/펠릿에 하면 된다) | 우리 `sei_electronic_class` 3분류(금속/절연체/undetermined) · CEI 카드 ⑥ *"갭이 크다는 것만으로 '부동태화된다' 고 쓰지 않는다 — 연속성·두께가 빠져 있다"* |
| hull 출처 | MP 판본 · pymatgen 판본 · 보정 체계 · 엔트리 ID | CEI 카드 G1 (`D-2026-09-16-cathode-cei-decomposition`) |
| 갭 방법 | +U·자기배열(NiO 는 AFM-II)·k점·판독법(고유값 vs DOS 가장자리) | 우리 갭 규율: fixed-occupations nscf VBM/CBM 고유값만 |

---

## 6. Post-processing ★

- **무엇**: ① 닫힌계 pseudo-binary 상호반응에너지 곡선(혼합비 x 별, 0 K) ② 원소분해 PDOS + 총 DOS, 그림 안에 "Band gap = X eV" 인쇄 ③ XPS 피팅(이중선 분해) ④ DRT(Ciucci 계열 [41]) ⑤ GITT D_Li ⑥ DC 분극 σ_e.
- **도구**: 반응에너지 = MP 에너지 + "previous studies 의 scheme"(Zhu–He–Mo) — **pymatgen 사용 여부조차 미기재**. DOS = VASP. 플롯은 Origin 양식으로 보인다(그림 양식 — 추정).
- **수치화·기록 방식**: 반응에너지는 **곡선만** 있고 표·반응식·최소값 수치가 **없다** → 우리는 픽셀로 읽었다(§감사 C). 갭은 그림 속 인쇄값만 있고 판독법 미기재. 코팅 비교는 `Table S2` 의 정성 등급(high/medium/low · good/medium/poor).
- **우리가 가져올 수 있는 형식**: `Fig. 6a–c` 처럼 **"후보 산물 vs 충전 양극"** 곡선을 **"전해질 vs 양극"** 곡선과 같은 패널에 겹쳐 그리는 표시 형식 — 2차 반응성(산물이 또 반응하나)을 한눈에 보인다. 단 우리는 꺾임 반응식과 끝점 판정을 같이 싣는다.

---

## 7. 우리 DFT 대비 (comp1 / modelc) → `our_dft_baseline.md`

> 트랙: **ESW · 우리 DFT 기준선 = 사용자 1저자** (결정이 그 자리에서 난다) / **CEI(Nd 계면) = 실험 쪽 다른 사람이 1저자** — 7-4 의 CEI 카드 언급은 그 트랙 소관이다.

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| **7-1 B③ 계면 반응 (닫힌계)** | LPSC/LiNiO₂ `figure-read ≈` **−0.42** · LPSC/Li₀.₂₅NiO₂ ≈ **−0.72 eV/atom** (MP 판본 미기재) | comp1\|LiCoO₂ **−0.3227 eV/atom** (`InterfacialReactivity(use_hull_energy=True)`, MP2026; 산물 Co₉S₈·Li₂SO₄·Li₃PO₄·Li₂S·LiCl) — `comparison_vs_ours.md` §B③ · 원자료 `db/properties/oxidation_stability.json` (`nd2o3_interface_reactivity_2026_06_17`) · ⚠ 레지스트리 미등록 = canonical 아님, 방법 대조용 | **같은 종류의 양, 다른 양극(LNO vs LCO)·판본·정규화 → 절대 비교 금지.** 구조적으로만: `[Rich16]` SI 의 혼합 몫이 LNO > LCO 라는 방향과 모순 없음 · 황화물–산화물 양극 >300 meV/atom 문헌 범위 안 |
| **7-2 B③ 전압의 표현** | 닫힌계 + 고정 조성 두 점 (LiNiO₂ / Li₀.₂₅NiO₂) | `interface_reactivity_v2.py` 기본 = **Li 열린계** (μ_Li = μ_Li(metal) − V, 전압 격자 2.5–4.5 V). `kb/results/interface_reactivity_v2_voltage_resolved_2026_06_21.md`: 4.3·4.5 V 에서 LPSCl 값이 **양극과 무관하게 같다**(CoO₂@4.3 = LiCoO₂@4.3) = **SE 자기 산화가 지배** · 도구 docstring: 열린계 끝점은 **계면량이 아니다**(SE 자체 분해) | **개념 차가 결론을 바꾼다**: 열린계에서는 고전압에서 'LiNiO₂ 냐 Li₀.₂₅NiO₂ 냐' 가 사라지고 **SE 의 산화가 주연**이 된다. 이 논문의 "탈리튬 양극이 반응을 켠다" 서사는 닫힌계 표현의 산물일 수 있다 |
| **7-3 B① 분해 onset** | 서론 *"~2.6 V"*(ref [7] 리뷰, **축 미명명**) · CV 개시 **2.4 V** · 피크 3.8 V (SE:VGCF 30:70, 0.2 mV s⁻¹) | comp1 = modelc **2.256 V** (grand-potential, LiS₄·SCl₃·Li₅PS₄Cl₂ 제외 = GG set, **S²⁻-limited, 층①**) | **등치 금지.** CV 개시는 동역학 onset(§B① *kinetic overshoot* 진영의 또 한 점, 우리보다 ≈0.15 V 위) · "~2.6 V" 는 정의 없는 소환값. ⚠ 우리 2.256 vs 문헌 계산 2.01 V 의 **0.246 V 는 원인 미확정** — 창 절대값이 문헌과 맞는다고 쓰지 않는다 (`our_dft_baseline.md`) |
| **7-4 D 갭 → σ_e** | ZrO₂ 3.40 "narrow → high σ_e" · NiO 1.97 "insulating" · LZPO 4.06 "wide" (PBE · 판독법 미기재) | comp1 **2.066** / modelc 2.099 eV (fixed-occ nscf 고유값, canonical) — **wide-gap 정성만**. 우리 CEI 카드 `D-2026-09-16-cathode-cei-decomposition` ⑥ *"갭이 크다는 것만으로 '부동태화된다' 고 쓰지 않는다"* · `sei_products.json` 의 역할 문턱(≥4 / 2–4 / <2 eV)은 **추론**이라고 그 파일 caveat 가 적는다 | **귀류**: 이 논문의 암묵 문턱(≈3.7–4.0 eV)을 그대로 쓰면 PBE ~2 eV 급인 **LPSC 자신이 "high electronic conductivity"** 여야 한다 — 그런데 그들이 잰 LPSC σ_e 는 **2.46×10⁻⁸ S cm⁻¹** 다. 갭 문턱 규칙이 자기 데이터와 안 맞는다 |
| **7-5 hull 출처** | MP 판본·보정·ID **미기재** | CEI 카드 G1: MP DB 판본·pymatgen 판본·보정 체계 기록 의무 | 우리 규율로는 **값이 아니다** (재현 불가) |
| **7-6 Zr 계 계면** | LZC 를 LiCl + ZrCl₄ 로 대리 · ZrCl₄/LiNiO₂ −0.22 | `[Cha]` 행: *"Zr 가 우리 hull 에 없어 아직 정량 못 함"* | 이 논문은 **LZC 화합물 값이 없다** → 우리 공백은 그대로다 |
| **7-7 A 이온전도 (실험)** | LPSC σ(30 °C) 4.10 mS cm⁻¹ · Ea 0.29 eV | MD 값은 **계 간 상대차로만** (1저자 인용정책 2026-09-18) | 소환값 — 우리 MD 절대값과 나란히 두지 않는다 |
| **7-8 B② 분해 속도·양** | 탄소 0→2→5 wt% 로 분해 가속 (P₂Sₓ↑, 5 wt% 붕괴) | 우리 계산에 없는 축 (`[Deng26PS]` 행: *전자 접근 차단이 산화 억제의 본체*) | 같은 물리의 실측 사례 — 우리 B① onset 은 "언제" 이고 이것은 "얼마나 빨리·많이" |

⚠ **우리 쪽 자기점검 한 줄**: 우리 `kb/results/interface_reactivity_v2_voltage_resolved_2026_06_21.md` Finding 4 도 *"LPSCl and LPSCl1.6 have ~identical band gap … -> ~identical sigma_e"* 라고 **갭에서 σ_e 를 바로 읽었다** — 이 논문과 같은 종류의 한 줄이다. 결론을 그 줄에 걸지는 않았고 뒤에 나온 CEI 카드 ⑥ 이 그 규율을 세웠다. (kb 는 이 세션에서 고치지 않았다 — 부모 세션 판단.)

---

## 8. 적용 인사이트 (내 연구에 어떻게)

1. **우리 B③ 보고에 "전압 표현 방식" 한 줄을 고정한다.** 닫힌계(고정 조성)와 열린계(μ_Li)는 고전압에서 결론이 갈린다(7-2). 문헌 값을 우리 옆에 놓기 전에 *"닫힌계인가 · 양극 조성은 무엇인가 · 그 조성이 측정 충전용량의 어느 x 인가"* 를 확인하는 30 초 검산 — 이 논문에서 그 검산(§감사 2단계 표) 하나가 서사의 절반을 무너뜨렸다.
2. **"산물 vs 양극" 2차 반응성 곡선은 좋은 표시 형식이다** — 단 산물 vs SE 를 같이 그리고, 꺾임 반응식과 끝점 판정을 같이 싣는다(우리 `endpoint_verdict`). CEI 화면(트랙: CEI · 1저자 = 실험 쪽 다른 사람)에서 쓸 때 이 논문은 **반면교사**로 인용한다.
3. **CEI 카드 ⑥ 의 외부 반례로 쓸 수 있다**: 같은 논문 안에서 1.97 eV 는 절연, 3.40 eV 는 전도 — "갭 → 전자 차단" 규칙이 왜 금지인지 한 문장으로 보여주는 사례.
4. **LZPO 를 우리 코팅 후보 축에 넣는다면 근거는 이 논문 계산이 아니라** `[Xiao19]` `Table 3`(V_ox 4.52 V — 4.5 V 대비 여유 0.02 V 라는 경고 포함) + `[Park26ML]` `Fig. 7`(인산염화 Zr 가 황화물과 덜 반응) + 이 논문의 **실험**(`Fig. 4`·`Fig. 5`)이다.
5. **DEM·전극 축 (VGCF)**: *"VGCF 2 wt% = 전자 경로 확보와 분해 가속의 교환"* 의 정량 앵커 — σ_e 1.78×10⁻⁴ → 2.86×10⁻² S cm⁻¹ 와 4.5 V 장기 붕괴가 같은 그림(`Fig. 2`)에 있다. 우리 VGCF 함유 전극 서사에서 *"전자 경로가 곧 분해 경로"* 를 말할 때 인용 가능한 실측.
6. **"충전 상태 x" 는 컷오프 전압만으로 정해지지 않는다** — `Fig. S23` 에서 "4.2 V + 탄소 2 wt%" 와 "4.5 V + 탄소 0" 이 같은 탈리튬 깊이다. 우리 계산의 양극 조성을 실험 조건에 맞출 때 **전압이 아니라 측정 충전용량**으로 맞춘다.

---

## 9. 인용 가능 문장 (deck/paper 용)

- *"Closed-system pseudo-binary calculations (MP energies, LiNiO₂ as the cathode proxy) give a mutual reaction energy of roughly −0.4 eV/atom between Li₆PS₅Cl and the discharged cathode, consistent with P₂Sₓ already present after mechanical mixing (Qi et al., J. Energy Chem. 2025)."* — ⚠ `figure-read` 값 · 닫힌계 · MP 판본 미기재를 같이 적는다.
- *"In Li₆PS₅Cl-based composites cycled to 4.5 V vs Li/Li⁺ with NCM85, oxygenated products (Li₃PO₄, Li₂SO₃, Li₂SO₄) appear in XPS after 200 cycles, and a ~10 nm LiZr₂(PO₄)₃ coating weakens but does not eliminate them (Qi et al. 2025)."*
- *"Adding 2 wt% VGCF raises the electronic conductivity of an NCM85/Li₂ZrCl₆ composite from 1.78×10⁻⁴ to 2.86×10⁻² S cm⁻¹ and the first discharge capacity at 4.5 V by 23.7 mAh g⁻¹, at the cost of accelerated catholyte decomposition (Qi et al. 2025)."*
- (반면교사 · 방법 문장) *"Bulk PBE band gaps do not determine the electronic conductivity of interphase products; in one study the same method labels a 1.97 eV phase insulating and a 3.40 eV phase electronically conducting."*

---

## 10. 주의/한계 (over-claim 방지)

1. **DFT 절은 결론을 증명하지 않는다** (§감사 E). "self-limited / unlimited" 는 용량 궤적 모양에서 온 말이다 — 계면층 성장 법칙은 측정되지 않았다.
2. **`Fig. 6a` 의 "LZC" 는 LZC 가 아니다** (LiCl + ZrCl₄ 원료 대리). 할라이드–양극 반응성 수치로 인용 금지.
3. **LiNiO₂ ≠ 4.2 V 충전 상태** — 두 점 대비는 방전 vs 충전이다.
4. **표–본문 모순 2** (이온전도 high↔low · LZPO high↔medium) · **그림–본문 모순 2** (`Fig. 6a` · NiO/ZrO₂ 갭) · 그림 라벨 오기 1 ("LPSC₁.₅") · 캡션 의심 1 (`Fig. S20`).
5. **재현 불가**: MP 판본·보정·ID·Li₀.₂₅NiO₂ 출처·+U·스핀·k·갭 판독법 미기재. NiO 1.97 eV 는 순수 PBE 서술과 맞지 않는다(일반 지식 근거 — 판정 보류).
6. **실험 쪽 한계**: 사이클 중 스택압 미기재 · n·오차막대 없음 · σ_e 비교(2 배) 단일 시료 · LIC 일반화 셀 1 개 · 레이더 그림 눈금 없음 · 유지율 기준점이 4번째 사이클.
7. **코팅 화학 불확실**: (003) 이동 = 미량 도핑 자인 → "코팅 효과" 와 "도핑 효과" 교락. 비정질 코팅 조성 미정량.

### ⛔ 인용 금지 (요약)
1. `Fig. 6a` 를 **"Li₂ZrCl₆ 와 LiNiO₂ 의 반응에너지"** 로 — 원료 대리다.
2. **"LiNiO₂/LZC 계면은 안정"** — 자기 그림(ZrCl₄/LiNiO₂ −0.22)과 모순.
3. **"ZrO₂ 는 좁은 갭이라 전자전도성"** · **"Li₃PO₄·Li₂SO₄ 는 넓은 갭이라 전자 터널링을 막는다"** — 갭 ≠ σ_e, 터널링은 두께·정렬 문제.
4. **"Li₃PO₄·Li₂SO₄ 는 부분 이온전도도가 높다"** — 자기 `Table S2` 가 "low".
5. **"LZPO 는 우수한 산화안정성"** 을 이 논문 근거로 — 계산하지 않았다. 쓰려면 `[Xiao19]` V_ox 4.52 V (4.5 V 대비 여유 0.02 V) 와 함께.
6. **`Table S2` 를 코팅 선택의 근거로** — 정성 등급·순환.
7. **"황화물 산화한계 ~2.6 V"** 를 축 이름 없이 — 우리 층① 2.256 V 와 같은 줄에 두지 않는다. CV 개시 2.4 V 도 **동역학 onset** 으로만.
8. 반응에너지 `figure-read` 값을 **우리 comp1\|LiCoO₂ −0.3227 옆에 절대값으로** — 양극·판본·정규화가 다르다.
9. **"LIC 계면은 반응성이 낮아 덜 감쇠한다"** — 표현 교락(화합물 vs 원료) + σ 3.4 배 교락.
10. 같은 연구실 편들의 **Li₂S 갭(3.04/3.14/4.2 eV)을 하나의 값으로** — 편마다 다르다.

---

## 11. 기법 미니 용어집

- **상호반응에너지 (mutual reaction energy, pseudo-binary)**: 두 상 A, B 를 x:(1−x) 로 섞은 조성이 상그림(convex hull)에서 평형 상 집합으로 내려갈 때의 에너지 변화(eV/atom). x 를 0→1 로 훑으면 꺾인 선(꺾임 = 산물 집합이 바뀌는 지점)이 나오고, 가장 깊은 꺾임이 "최대 구동력". **속도·두께·계면 구조는 없다.** (Zhu–He–Mo 2015/2016 · Richards 2016)
- **닫힌계 vs Li 열린계**: 닫힌계는 Li 가 계 밖으로 못 나간다(조성 고정) → 전압은 반응물 조성으로만 넣을 수 있다. 열린계는 Li 저장고를 열고 μ_Li = μ_Li(Li 금속) − eV 로 둔다 → 전압이 직접 변수가 되고, 고전압에서는 SE 자체 산화가 들어온다(그 끝점 값은 "계면량" 이 아니다).
- **hull 에너지 대체**: 반응물 조성에 맞는 엔트리가 없을 때 그 조성의 hull 에너지(= 평형 혼합물 에너지)를 대신 쓰는 것. 준안정 상(예: 탈리튬 층상 Li₀.₂₅NiO₂)의 반응성을 **과소** 평가하게 된다.
- **KS(PBE) 밴드갭**: 콘–샴 고유값 차. PBE 는 체계적 과소(~30–50 %). 우리 규율: fixed-occupations nscf 의 VBM/CBM 고유값만 인정, DOS 가장자리 판독 금지(~0.3 eV 과소), 문헌과는 "wide-gap" 정성만.
- **σ_e 와 갭**: 진성 캐리어만 있으면 n ∝ exp(−E_g/2kT) 지만, 실제 넓은 갭 절연체의 σ_e 는 결함·불순물·폴라론이 정한다 → 갭으로 σ_e 를 정하지 않는다.
- **DC 분극 (σ_e 측정)**: 이온차단 전극 사이에 작은 전압(여기 0.4 V)을 걸고 정상전류로 σ_e 를 구한다.
- **DRT (distribution of relaxation times)**: 임피던스를 시정수 τ 분포 γ(τ) 로 펼쳐 겹친 반원을 가르는 해석. 봉우리 **면적**이 저항, 높이는 아니다.
- **GITT**: 짧은 전류 펄스 + 휴지 반복으로 겉보기 확산계수 D_Li 를 얻는 법.
- **ICE (initial Coulombic efficiency)**: 첫 방전/첫 충전 용량. 황화물–산화물 계면처럼 첫 사이클 부반응이 크면 낮다.
- **dQ/dV H2→H3**: 고-Ni 층상 양극의 고전압 상전이 봉우리(≈4.2 V). 뚜렷하면 입자가 그 깊이까지 실제로 탈리튬됐다는 뜻.
- **NASICON LiZr₂(PO₄)₃**: Zr–O–P 3차원 골격의 Li 이온전도 인산염. 인산염 골격은 O 2p 를 끌어내려 산화한계를 올린다(`[Xiao19]`).

---

## 12. 원문 표 전사 (PDF 텍스트)

**Table S1. Reaction products of three types of cathode/electrolyte interfaces.**

| 계면 | 실험 산물 | 이론 산물 | Ref. |
|---|---|---|---|
| NCM85/LZC | ZrCl₄, LiCl, LiClₓ | NiO, LiClO₄, LiCl, ZrCl₄, ZrO₂, Li₂ZrO₃ | [10] (Kochetkov 2022) |
| NCM85/LPSC | P₂Sₓ, Li₃PO₄, Li₂SO₃, Li₂SO₄ | Ni₃S₂, Co₉S₈, MnS, Li₂S, LiCl, Li₃PO₄, Li₂SO₄ | [11] (`[Xiao19]`) |
| LZPO@NCM85/LZC | / | / | / |
| LZPO@NCM85/LPSC | P₂Sₓ, Li₃PO₄, Li₂SO₃, Li₂SO₄ | Li₃PS₄, Li₃PO₄, LiCl, ZrS₂ | / |

**Table S2. Various properties of five coating materials and their coating effects.**

| 코팅 물질 | 전자전도도 | 이온전도도 | 산화한계 | 코팅 효과 | Ref. |
|---|---|---|---|---|---|
| ZrO₂ | high | / | high | poor | [12] (Machida 2012 *SSI*) |
| Li₂ZrO₃ | high | medium | low | poor | [13] (Zhang/Ceder 2020 *AEM*) |
| Li₃PO₄ | low | low | high | medium | [14, 15] |
| Li₂SO₄ | low | low | high | medium | [14, 15] |
| LiZr₂(PO₄)₃ | medium | medium | high | good | [5] (Wang 2021 *AEM*) |

> ⚠ `Table S2` 의 근거 문헌 [12]·[13] 은 litdb 에 없다 — 각 등급이 그 문헌에 실제로 있는지 **확인하지 못했다**.
