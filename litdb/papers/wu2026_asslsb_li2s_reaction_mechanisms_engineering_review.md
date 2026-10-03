<!-- digest 초판 2026-10-03 (논문 에이전트 · 심층판 · 대피 세션 `claude/evac-2026-10-02` — 커밋·INDEX·comparison 합치기는 부모 세션)
     사용자 지정: "우리 연구(li2s 트랙)와 맞닿아 있어 더 자세하게". 리뷰라 자체 계산·실험이 0 이다. 그래서 이 digest 의 일은
       ① 2차 인용 수치를 ref 번호와 함께 빠짐없이 옮기고
       ② 그 수치가 서로·그림·우리 digest(원전을 이미 읽은 것)와 맞는지 감사하고
       ③ 트랙별(li2s · ESW · 기타)로 무엇을 가져오고 무엇을 막을지 정하는 것이다.
     - 그림: 크롭 20장(그림 18 + 표 2) 중 그림 13장 실독 (Fig. 1–11 · 17 · 18) + Fig. 6a–c · Fig. 11b 확대 재렌더.
       Fig. 12–16 은 캡션 기준(미실독). 표 1·2 는 크롭 PNG 대신 PDF 페이지를 렌더해 읽었다(아래 기호 문제 때문).
     - ⚠ PDF 텍스트층이 기호를 잃는다: − · × · μ(→m) · °(→1) · ∼(→B) · ≈(→E) · ≥(→Z) · <(→o) · ≤(→r) · >(→4).
       실제로 걸린 것 2건: 표 2 ref 212 수명 ">20" 이 텍스트층에서 "420", §3.5 ">5 mg cm⁻²" 가 "45". 인용한 수치 중 기호가 걸린 것은
       전부 페이지를 렌더해 다시 읽었다 (Tg −16.8/−25.5 °C · S 전자전도 ~10⁻³⁰ · ">420 Wh kg⁻¹" · "41.2 mS" · "4.6 V" 등).
     - 홉 수 검산 (`D-2026-09-27-barrier-hop-count` · active): `tools/sei/collect_neb.py::hop_check` 로 계산 (ν₀ 10¹³ s⁻¹ 가정).
     - methods 태그: DFT · ESW 만. Bader(`Fig. 6f` 의 전하 숫자) · NEB(`Fig. 6b` 의 "Transition State" 라벨) · elastic(탄성률 범위)은
       리뷰 본문이 기법으로 다루지 않거나(그림 라벨뿐) 방법 없이 범위만 옮겨서 태그하지 않았다 (본문 문자열 검색: NEB 0 · Bader 0 · AIMD 0 · MLIP 0).
     - 트랙: li2s = 외부 1저자 → 우리 캠페인 문장은 마감 원장 허용 서술에서만 가져왔다 · ESW = 사용자 1저자 · 점착 W 값은 싣지 않는다. -->

# Toward practical all-solid-state lithium–sulfur batteries: from reaction mechanisms to engineering strategies — Wu, Liu et al. (*Chem. Soc. Rev.* 2026, Advance Article)

> slug `wu2026_asslsb_li2s_reaction_mechanisms_engineering_review` · DOI `10.1039/d6cs00312e` · type `review (자체 계산 0 · 자체 실험 0 · 전량 2차 인용 · refs 226 · 그림 18 · 표 2)` · PDF `litdb/inbox/Wu 2026 - Toward practical all-solid-state lithium-sulfur batteries (Chem Soc Rev d6cs00312e).pdf` (41 pp = 본문 ≈35 + 참고문헌 ≈6 · SI 없음) · digested `2026-10-03` · status ✅ · 태그 **[외부 · 리뷰]**

> elements: Li, S, P, Cl, Br, I, O, C, N, F, B, Al, Si, Ti, V, Mn, Co, Ni, Cu, Ge, Se, Y, Ag, In, Sn, La, Zr
> methods: DFT, ESW

> **저자**: **Jinghua Wu**†\*ᵃᵇᶜ · **Tianyi Liu**†ᵃ · Wenjie Wangᵃ · **Hongli Wan**\*ᵃᵇᶜ · **Xiayin Yao**\*ᵃᵇᶜ (ᵃ Ningbo Institute of Materials Technology and Engineering, CAS · ᵇ UCAS Center of Materials Science and Optoelectronics Engineering · ᶜ Zhejiang Key Lab of Advanced Fuel Cells and Electrolyzers Technology) · † 공동 1저자 · 접수 2026-07-10 · 게재 2026-09-28 (Advance Article — 권·쪽 미정) · NSFC U25A20627·52172253·52372244 외 · *"No primary research results, software, or code have been included, and no new data were generated"* · 이해충돌 없음
> ⚠ **한양대 접점**: 교신 Xiayin Yao 의 저자 소개에 *"research fellow or visiting scholar in **Hanyang University**, South Korea (2012–2013)"* (p.2). litdb 의 한양대 접점 표시 선례는 `[Lee26Coat]`.
> **자기 인용**: 이름 일치 기준(X. Yao · H. Wan) ≈11편 — refs 23·27·42·156·158·163·196·197·208·209·217 (동명이인 가능 2편 182·190 제외). 재수록 패널 중 저자 그룹 것 = `Fig. 8c`(ref 27) · `Fig. 13f–h`(ref 196) · `Fig. 13i,j`(ref 197) · `Fig. 17e`(ref 209).
> **같은 그룹 접점**: ref 102(NiNC SAC, `Fig. 6f`)·ref 148 = `liu2026_li4sns4_mediator_low_barrier_li2s` 와 같은 UESTC 그룹(Wei Chen·Yichao Yan, 저자 이름 일치) · ref 64 의 B. Xi·J. Feng·S. Xiong = `zhang2026_anode_free_asslsb_li2s_pi3_na_current_collector` 의 Shandong 그룹.
> **관련 digest**: `cronk2026_lis_cathode_interphase_chemistry`(li2s 가설 원출처 · 이 리뷰의 ref 223 = **표 2 한 행뿐**) · `cronk2026_lis_positive_electrode_geometry_fem` · `wang2025_miec_tis2_lps_three_phase_interface_lis_assb`(ref 22) · `zhu2015_esw_grand_potential_origin`(ref 20) · `schwietert2020_redox_activity_vs_electrochemical_stability`(ref 82) · `xiao2020_interface_stability_ssb_review`(ref 66) · `doux2020_stack_pressure_assb`(ref 85) · 인용 안 된 같은 절 편: `zhang2026_…pi3…` · `liu2026_li4sns4_…` · `li2026_li_kinetic_promoter_aqueous_mn_sulfur` · `lai2020_li2s_interfacial_layer_amorphous_sulfide_cse`.
> 🎤 **관련 발표**: 없음 — `litdb/talks/*.md` 인입 대기열(유일: `talks/lee2026_skku_mlip_materials_design.md` §99-10)에 이 논문 행이 없다 (2026-10-03 grep).

> **본 digest 에서 실제로 본 그림 (2026-10-03)**: `Fig. 1` · `Fig. 2` · `Fig. 3` · `Fig. 4` · `Fig. 5` · `Fig. 6` · `Fig. 7` · `Fig. 8` · `Fig. 9` · `Fig. 10` · `Fig. 11` · `Fig. 17` · `Fig. 18` — **13장** + `Fig. 6a–c`·`Fig. 11b` 확대 재렌더. `Table 1`·`Table 2` 는 PDF 페이지 렌더로 읽었다(크롭 PNG 는 안 열었다).
> **안 본 것**: `Fig. 12`(후막 경사 설계) · `Fig. 13`(박막 SE 제조) · `Fig. 14`(Li–S 박막 SE 적용) · `Fig. 15`(유연 전해질) · `Fig. 16`(저변형 전극) — §8 에 '캡션 기준 · 미실독' 으로 표시했다.
> 그림에서만 읽은 값은 **`figure-read ≈`**, 리뷰에 없는 산수는 **(우리 산수)** 로 표시했다. 리뷰의 모든 수치는 **2차 인용** — 행마다 `ref N` 을 붙였다.

---

## 0. 이 digest 를 읽는 법

### 0-a. 트랙별 읽기축 (결정·판정을 말할 때 트랙을 먼저 쓴다)

| 트랙 | 1저자 | 이 리뷰에서 찾는 것 | 어디 |
|---|---|---|---|
| **li2s** (LPSCl@Li₂S 비정질 계면상 · 소셀 유리 MLIP-MD) | **외부 1저자** — 여기 쓰는 것은 전부 **관찰/제안** | 가설 *"LPSCl@Li₂S 볼밀 복합체의 계면에 중간 비정질상이 생겨 이온전도를 살린다"* (`cronk2026_lis_cathode_interphase_chemistry` §0) 을 **지지하는 것 / 위협하는 것 / 경쟁 기전** | §11-(i) |
| **ESW** (grand-potential 층① 산화 onset) | **사용자** | 리뷰의 "SE 가 양극에서 분해·산화환원에 참여(용량 기여)" 서술을 **축 이름**에 대응 | §11-(ii) |
| 계산 감사 (우리 DFT 기준선) | 사용자 | 2차 인용 DFT 수치의 기준상태·단위 — **장벽으로 적힌 수가 장벽인가** | §4 · §10 |
| 점착(W_ad) · DEM · CEI · 음극(E) | 각 트랙 | 배경만 (수치 없음 · 점착 W 값 미기재) | §11-(v) |

### 0-b. 이 digest 의 ESW 어휘 — 축을 안 붙이면 틀린다

- **층①** = 열역학 분해 onset (0 K grand-potential · 우리 값이 사는 곳 · [Zhu15] 원전).
- **층②** = 골격 유지 탈리튬화(intrinsic / topotactic, [Schw20]·[Schw21]) — 우리에게 값이 없다.
- **층③** = 겉보기(실용) 창 — 동역학·부동태·전자 접근을 포함한 CV/LSV·셀 관측.
- §B 축(`comparison_vs_ours.md`): **B①** 산화 onset · **B②** 반응의 *양·속도*(전자 접근·가역성 — §B `[Deng26PS]` 행의 "axis② = 반응 속도·양" 용법) · **B③** 양극(CAM\|SE) 계면 · **B④** 열·수분.
  ⚠ §B 안에는 B② 를 "구속(strain-explicit) 창" 으로 쓴 용법도 있다(`zuo2022` §7a). **이 digest 의 B② 는 '양·속도' 쪽이다.**

### 0-c. 이 리뷰를 읽을 때 늘 붙는 단서 세 개

1. **전부 2차 인용**이다. 원전을 이미 읽은 것(§12)은 그 digest 가 이긴다.
2. **전위 기준이 섞인다.** ESW 는 *"vs Li/Li⁺"* 로 적혔지만 Li–S 작동 전압(방전 ~1.5–2.1 · 충전 컷오프 ~2.6–2.8 V)은 기준전극이 없다. 전고체 Li–S 는 Li–In 셀(≈0.62 V vs Li⁺/Li, 리뷰 §4.4)이 흔하다 — 환산 없이 섞였을 수 있다.
3. **표 2 에는 온도 열이 없다** (§9 · §10-⑤).

---

## 1. 한 줄 요약

액체를 고체로 바꾸면 황 전환이 *"확산 매개"* 에서 *"고체–고체 · 계면 한정 · 수송 결합"* 반응으로 바뀐다는 틀로, ① 본질 한계(S–S 절단 · Li₂S 절연 · **Li₂S₂ 중간체**(`Eq. 1`–`Eq. 2`) · 3상계면(TPB)과 Damköhler 수 Da > 1 · SE 분해 · Li 크리프·공극)와 ② 대응(할라이드 수송공학 · 촉매 · redox mediator · MIEC · 분해의 활용 · 음극 계면), ③ 실용 장벽(S 로딩 >5 mg cm⁻² · 막 <30 µm · 저압)을 정리하고 5 우선순위 로드맵(`Fig. 18`)으로 닫는 41쪽 리뷰다. **자체 계산·실험은 0, 수치는 전부 2차 인용.** 우리에게 남는 것은 수치가 아니라 (a) li2s 가설의 **지지·위협·경쟁 기전 목록**(LPSI 비정질 계면상 · 할라이드 편석 · Li₂S–LiX 고용체 · LiI 계면 EXSY), (b) **ESW 축 미명명 사례 4건**(Cl/Nb/O 도핑 "창 확대" · Li–Al "열역학적 억제" · `Fig. 11b` HOMO/LUMO 라벨 · O 도핑 "DOS 감소"), (c) **2차 인용 DFT 수치의 감사** — *"탈리튬 장벽"* 으로 적힌 3.78/4.10/5.75 eV 는 홉 수 검산으로 장벽일 수 없다(300 K 에서 Γ ≈ 10⁻⁵¹–10⁻⁸⁴ s⁻¹). 그리고 **li2s 가설의 원출처(Cronk, ref 223)는 본문에 한 번도 나오지 않고 표 2 한 행(온도 누락)뿐**이다.

---

## 2. 메타 — 범위·구성·litdb 안의 자리

| 항목 | 내용 |
|---|---|
| 유형 | Review Article (*Chem. Soc. Rev.*) — 자체 계산·실험 0 |
| 구성 | §1 서론 · §2 기초(2.1 구성 · 2.2 고체 황 반응 기전 · 2.3 이온/전자 수송과 TPB) · §3 도전(3.1 본질 동역학 장벽 · 3.2 수송·TPB · 3.3 전해질 분해 · 3.4 음극 전기화학–기계 불안정 · 3.5 응용 지향) · §4 전략(4.1 동역학: 4.1.1 수송공학 · 4.1.2 촉매 · 4.1.3 redox mediator · 4.2 계면 구조 · 4.3 전해질 분해의 조절·활용 · 4.4 음극 계면) · §5 응용 지향 설계(5.1 후막 · 5.2 초박막 SE · 5.3 저압: 5.3.1 전해질 · 5.3.2 전극 · 5.3.3 계면) · §6 요약·전망 |
| 그림·표 | 그림 18(자체 도식 `Fig. 1`–`Fig. 4` · `Fig. 18` · 나머지는 원전 재수록) · `Table 1`(30 행) · `Table 2`(22 행) |
| 저자가 내세운 조직 원리 | *"Rather than organizing the discussion primarily by material class"* — 기전 → 수송 → 계면 → 공학 제약을 한 틀로 (p.3) |
| 할라이드 역할 지도 (§4 서두) | LiX 계면상 = 수송·접촉(4.1.1) · 할로겐 종 = 계면 동역학(4.1.2) · I⁻/I₃⁻ = 전하 매개(4.1.3) · 할라이드 SE·LiX 계면상 = SE 안정·Li 계면(4.3·4.4) · 할라이드 이온 이동 = 적응형 계면(5.3.3) |
| litdb 안의 자리 | Li–S 절의 **첫 개관 리뷰**. 같은 절 1차 논문 5편(Cronk26 · Zhang26PI3 · Wang25MIEC · Liu26Sn · Li26MnS) 중 인용되는 것은 **Wang25MIEC(ref 22) · Cronk26(ref 223, 표 2 한 행)** 둘뿐 |

---

## 3. 핵심 수치 총정리 (전량 2차 인용)

> 홉 수 검산 줄은 `D-2026-09-27-barrier-hop-count` 에 따라 Li₂S 관련 장벽 바로 아래에 단다 — **차수 검산이지 확산계수·전도도가 아니다** (ν₀ 10¹³ s⁻¹ 가정).

### 3a. 기본 상수·스케일

| 양 | 값 | ref | 비고 |
|---|---|---|---|
| Li–S 이론 에너지밀도 vs LIB | ~2600 vs ~250–300 Wh kg⁻¹ | §1 (번호 없음) | |
| 이론 용량 | Li 3860 · S 1675 mAh g⁻¹ | §1 | |
| 황화물 SE σ_RT (LPSCl · LGPS) | 10⁻³–10⁻² S cm⁻¹ | 34, 35 | |
| 산화물 LLZO σ_RT | 10⁻⁴–10⁻³ S cm⁻¹ | 36 | |
| S / Li₂S 전자전도 | **~10⁻³⁰ S cm⁻¹** | 40 | ⚠ §4.1.1 의 S₉.₃I 서술과 12.8 자릿수 어긋남 (§10-③) |
| 활물질 부피변화 | 최대 ~80 % | 41 | `cronk2026_…geometry_fem` 입자 71–75 % |
| 양극 SE 비중 | 30–60 wt% | — | |
| 탄소 퍼콜레이션 문턱 | ≈4 wt% (Li–S 는 훨씬 많이 쓴다) | 74 | |
| Li 두께 변화 | 1 mAh cm⁻² ↔ ≈4.85 µm | 47 · `Fig. 4f` | (우리 산수) 3860 mAh g⁻¹ · 0.534 g cm⁻³ → 4.85 µm ✓ |
| 스택압 | 수십–수백 MPa | 71, 85, 98 | |
| Li–In 합금 전위 | ≈0.62 V vs Li⁺/Li | §4.4 (번호 없음) | |

### 3b. 반응 기전 (§2.2)

| 양 | 값 | ref | 비고 |
|---|---|---|---|
| 액체(에테르) Li–S 두 평탄 | 1단 ~2.3–2.4 V (용량 ~20–30 %, S₈ → Li₂S₄–Li₂S₈) · 2단 ~2.0–2.1 V (~70–80 %, → Li₂S₂ → Li₂S) | 49–52 · `Fig. 2a` | |
| ASSLSB 평탄 | 단일, ~2.1 V | `Fig. 2b` | 그림의 방전 곡선은 평탄이 아니라 **경사형** |
| 단일 평탄의 해석 | Gibbs 상률: 2상 평형 = 일정 전압 → 용매 없음 = 용해 다황화물상 없음 = 2상 영역 하나 | — | |
| DFT OCV | 완전 용매화 Li₂S₄ → 2 평탄 · 비용매화 → 1 평탄 ("용매화가 약할수록 중간체 형성에너지↑") | 54 | 방법 미기재 |
| 단일 평탄의 다른 경로 | 고농도 전해질 · <2 nm 미세기공 탄소 → "merged/sloping" | 54–56 | 단일 평탄은 고체 고유가 아니다 |
| in situ TEM | S → Li₂S 직접(결정성 중간체 미검출) | 53 | 초기 견해 |
| 실제 초기 방전 용량 | "typically <1400 mAh g⁻¹" (SE 분해 기여 포함해도) | 57, 58 | ⚠ 자기 `Table 2` 에 ≥1486 인 행 4개 (§10-⑨) |
| Li₂S₂ 실험 증거 | XAS + ToF-SIMS → 방전 산물 = Li₂S₂ + Li₂S (2023) · operando 독립 확인 (2023) | 59 · 60 | |
| `Eq. 1` · `Eq. 2` | S₈(s) + 8Li⁺ + 8e⁻ → 4Li₂S₂(s) · 4Li₂S₂(s) + 8Li⁺ + 8e⁻ → 8Li₂S(s) | — | 두 단계가 별개 평탄으로 안 갈릴 수 있다고 본문이 명시 |
| "열역학적 접근 가능 준안정 중간체" | *"formation energy … far lower than that of S₈"* (first-principles, 번호 없음) | — | ⚠ S₈ 형성에너지는 정의상 0 — **hull 기준 비교가 아니다** (§10-⑪) |

### 3c. 수송·할라이드 (§4.1.1)

| 양 | 값 | ref · 그림 | 비고 |
|---|---|---|---|
| Li₂S–LiX(X = Cl, Br, I) σ_RT | "~10⁻⁶ S cm⁻¹ 수준" | 125 · `Fig. 5a` | `figure-read ≈` Li₂S(0 %) **8×10⁻⁹** · 10 mol% LiI 2.5×10⁻⁷ / LiBr 1.6×10⁻⁷ / LiCl 1.1×10⁻⁷ · 20 mol% LiI **2.2×10⁻⁶** / LiBr 4.6×10⁻⁷ / LiCl 5.6×10⁻⁷ · 30 mol% LiBr 3.3×10⁻⁶ / LiCl 2.1×10⁻⁶ S cm⁻¹ (LiI 30 % 점 없음 · 로그 눈금 ±0.1 decade) |
| 기전 (리뷰) | ① S²⁻ 자리 할라이드 치환 → Li 공공 ② 큰 반경·고분극 → Li⁺–음이온 쿨롱 약화 | 125 | |
| Li₂S 이용률 | Li₂S–LiI 만 ≈95 % + 고율 안정 ("σ 는 셋이 comparable") | 126 | `figure-read` 20 mol% 에서 LiI ≈4× (§10-⑧) |
| LiI 도메인 가역 진화 | 충전(탈리튬) → 고용체 부분 해체 · LiI-rich 미세상 / 방전 → 재편입 | 126 · `Fig. 5b` | 그림의 방전 끝 라벨은 *"Li₂S–LiI + LiI domain"* — 재편입이 다 되지 않는다 |
| S₉.₃I | 띠간격 2.92 → ≈1.65 eV · σ_e 11 자릿수 ↑ → **5.9×10⁻⁷ S cm⁻¹** · 융점 ~65 °C(열 자가치유) | 122 | 갭의 방법(광학/DFT) 미기재 |
| LiI 코팅 Li₂S + LPSCl — 2D ⁶Li EXSY | 계면 교환 활성화에너지 **Li₂S/LiI 0.142 eV · LiI/LPSCl 0.117 eV** ("LiI 고유 확산장벽에 가깝다", 값 없음) | 127 · `Fig. 5c,d` | 그림의 스펙트럼 = **Tmix 10 s · 373 K** (리뷰 본문에 측정 온도 없음) |
| | 홉 수 검산 (ν₀ 10¹³ s⁻¹ 가정 · 300 K): **0.142 eV** Γ ≈ 4.12×10¹⁰ s⁻¹ · 평균 대기 ≈ 2.4×10⁻¹¹ s / **0.117 eV** Γ ≈ 1.08×10¹¹ s⁻¹ · 평균 대기 ≈ 9.2×10⁻¹² s. 373 K · Tmix 10 s 동안 N ≈ 1.2×10¹² / 2.6×10¹² 회 | | "저저항 연속 수송" 서술과 차수 모순 없음. ⚠ EXSY Ea 는 **겉보기 교환 활성화**(전인자 미지)지 단일 홉 장벽이 아니다 — 우리 NEB·MD 장벽과 나란히 놓지 않는다 |
| 할라이드 편석 | UHS 혼합에서 아지로다이트의 Cl·Br·I 가 빠져나와 칼코겐 양극 표면에 **LiX-rich 나노 계면상** · 코팅 공정 없이 연속 Li⁺ 망 | 101 · `Fig. 5e` | 그림 라벨: S/LPSCl/C **2000 rpm 5 h** · EDS 에 Cl 테두리·P 내부 |
| Li₂S–AlI₃ | σ 최대 6×10⁻⁵ S cm⁻¹ · UV-Vis 흡수단 ~270 → ~350 nm (*"insulating → semiconducting"*) | 128 | (우리 산수) 광자에너지 ≈4.59 → ≈3.54 eV — 여전히 넓은 간격 |
| Cu⁺/I⁻ 공도핑 Li₂S | D_Li ~2 자릿수 ↑ · σ_e 9.44×10⁻¹⁴ → 10⁻⁸–10⁻⁶ S cm⁻¹ (*"5–8 orders"*) · **DFT Li⁺ 이동장벽 1.71 → 0.6 eV** | 115 | (우리 산수) σ_e 는 **5.0–7.0 자릿수** |
| | 홉 수 검산 (ν₀ 10¹³ s⁻¹ 가정 · 300 K): **1.71 eV** Γ ≈ 1.88×10⁻¹⁶ s⁻¹ · 평균 대기 ≈ 5.3×10¹⁵ s · 10 h(3.6×10⁴ s) 동안 N ≈ 6.8×10⁻¹² 회 / **0.6 eV** Γ ≈ 8.3×10² s⁻¹ · 평균 대기 ≈ 1.2×10⁻³ s · 10 h 동안 N ≈ 3×10⁷ 회 | | 🔴 **차수 모순**: 1.11 eV 차의 아레니우스 비 = 4.4×10¹⁸ (10^18.65, 300 K) 인데 실험 D 는 ~2 자릿수 · 1.71 eV 면 맨 Li₂S 는 상온에서 사실상 홉이 없는데 `Fig. 5a` 의 맨 Li₂S 는 `figure-read ≈` 8×10⁻⁹ S cm⁻¹ 로 잰다 (§10-②) |

### 3d. 촉매 — 2차 인용 DFT (§4.1.2)

| 양 | 값 | ref · 그림 | 비고 |
|---|---|---|---|
| LiI(100) 위 형성에너지/원자 | Li₂S₂ −1.01 → ≈−0.7 · Li₂S −1.59 → ≈−0.6 eV atom⁻¹ (본문 "bulk phase" → LiI 흡착) | 59 · `Fig. 6a` | `figure-read ≈` LiI 위 −0.71 · −0.60. ⚠ 그림 범례는 **"Vacuum"**, 본문은 **"bulk"**. 캡션은 "Gibbs free energy", 축은 "Energy of Formation" (§10-⑭) |
| (우리 산수) hull 로 읽으면 | 진공/벌크: Li₂S₂ 가 S₈–Li₂S 연결선(x = 0.5 에서 −1.19) **위 ≈0.18 eV/atom** = 준안정 / LiI 위: 연결선(−0.45) **아래 ≈0.26 eV/atom** = 볼록(hull 위) | `Fig. 6a` | 리뷰가 말하지 않은 **hull 역전** — LiI 가 Li₂S 를 더 많이 불안정화(≈0.99 vs 0.30 eV/atom)해 Li₂S₂ 쪽을 상대적으로 유리하게 만든다. `Table 1` ref 59 의 설계 전략 *"Regulate cutoff potential to obtain Li₂S₂"* 와 같은 방향. ⚠ 흡착계 원자당 정규화 규약 미기재 → **판정 아님** |
| Li 추출에너지 | 흡착 Li₂S₂ **+3.78** · 흡착 Li₂S **+4.10** vs 벌크 Li₂S Li 공공 형성 **+5.75 eV** → *"significantly reduced delithiation barrier"* · Li₂S₂ 가 더 쉽게 산화 | 59 · `Fig. 6b` | 그림은 이 수를 **"Transition State Li-S* + Li*"** 까지의 화살표로 그린다 · 그림에만 **0.42 eV**(본문 미언급) · 축척 없음 |
| | 홉 수 검산 — **장벽이라고 읽으면** (ν₀ 10¹³ s⁻¹ 가정 · 300 K): 3.78 eV Γ ≈ 3.2×10⁻⁵¹ s⁻¹ (평균 대기 ≈ 3×10⁵⁰ s · 10 h 동안 N ≈ 1×10⁻⁴⁶ 회) · 4.10 eV Γ ≈ 1.3×10⁻⁵⁶ s⁻¹ · 5.75 eV Γ ≈ 2.5×10⁻⁸⁴ s⁻¹ | | ⛔ **장벽일 수 없다** — 수 시간 충전에서 일어나는 반응이다. 이 수들은 **기준상태(Li 원자? Li 금속?) 미기재의 열역학 추출에너지**이고 "장벽 감소" 는 범주 오류 (§10-①) |
| Li–Se 결합에너지 (LiI-I / LiI-Li / 그래핀) | Se₈ +0.39 / −0.21 / +0.33 · Li₂Se₆ −2.00 / −0.82 / +0.16 · Li₂Se₂ −2.45 / −1.77 / ≈0 · Li₂Se −3.09 / −2.17 / −0.09 eV (`figure-read ≈` ±0.05) | 129 · `Fig. 6c` | 그래핀 위 Se₈·Li₂Se₆ 가 **양수**(불결합) — 분산 보정 여부를 알 수 없다. 황 계 수치 아님 |
| CoS₂ (S + CoS₂ + LPSCl 볼밀) | 1584 mAh g⁻¹ @0.25 mA cm⁻² · 분극 0.34 V · 474 mAh g⁻¹ @1.28 mA cm⁻² | 132 | |
| Co–N₄ SAC (AB 볼밀) | 양방향 촉매: 방전 S–S 절단 / 충전 Li–S 약화 | 24 · `Fig. 6d` | |
| Co/Mn/V SAC | 서술자 = M–S 결합 세기(M 3d–S 3p 혼성): Mn 약함 → 불완전 방전 · V 강함 → 피독 · Co 중간 = 양방향 | 123 · `Fig. 6e` | 🔴 그림의 **방전** 칸은 *"✓ dissociate / weak M-S · ✗ poison / strong M-S"* — 본문과 방전 쪽 방향이 반대 (§10-⑦) |
| NiNC | Li₂S₂ 흡착이 Ni 를 dsp² → d²sp³ 로 · Li₂S 생성 후 복귀 · *"Li₂S₂ → Li₂S 가 용량 방출의 병목"* | 102 · `Fig. 6f` | 그림의 전하 −0.86 → −0.84 · +0.86 → +0.67 은 본문 미언급 · 규약 미기재 |

### 3e. Redox mediator (§4.1.3)

| 계 | 내용 · 수치 | ref · 그림 |
|---|---|---|
| 고분자 SPE 속 안트라퀴논 유도체 | Step A: Li₂S + RMox → LiPSs + Li⁺ + RMred (화학) · Step B: RMred → RMox + e⁻ (집전체) · 첫 충전 활성화 스파이크 소멸 | 25 · `Fig. 7a,b` |
| PhSeLi (황화물 ASSLSB) | 첫 충전에 PhSe• 라디칼 → Li–S 약화 · 활성화 과전압↓ · Li₂S 이용률 ≈완전 | 139 |
| Li₂S/LiVS₂ 코어–셸 | LiVS₂ → VS₂ + Li⁺ + e⁻ · **Li₂S + 2VS₂ → 2LiVS₂ + S** · VS₂ 전위 ≈ Li₂S 산화 전위 → 자발·기생반응 없음 | 116 · `Fig. 7c` |
| LixIn₂S₃ (고에너지 볼밀 in situ) | redox 매개 + 수송 매개 | 140 |
| LBPSI (Li₂S–B₂S₃–P₂S₅–LiI 유리) | I⁻/I₂/I₃⁻ 가역 중심 · 활성 영역 TPB → SE–S 2상 계면 · 1497 mAh g⁻¹ @2C · 784 @20C · **25,000 사이클 80.2 % @5C** | 100 · `Fig. 7d,e` |
| **LPSI** (PI₃ + S₈ + Li₅.₅PS₄.₅Cl₁.₅ 기계화학) | **비정질 Li–I–S–P 계면상**: Li⁺ 경로 + 부피 완충 + 요오드·PₓSᵧ redox · 4단계(억제 → 활성 → 강화 → 안정) · 1600 사이클 93.8 % @6 mg cm⁻² · 5 mA cm⁻² · 파우치 **>420 Wh kg⁻¹** | 113 · `Fig. 7f,g` |
| 저자 경고 | 고정 매개체는 작용 범위가 짧다 · 전위·가역성 정합 필요 · **"진짜 가역 매개" 와 "희생 분해의 일시 용량" 을 구분하라** | — |

### 3f. 계면 구조·혼합전도 (§4.2)

| 계 | 내용 · 수치 | ref · 그림 |
|---|---|---|
| Nagao | Li₂S + AB + Li₂S–P₂S₅ 고에너지 볼밀 → 나노 3상 접촉 | 141 |
| Han 2016 | Li₂S + Li₆PS₅Cl + PVP 공용해 → 공침 → 550 °C Ar 탄화 → Li₂S–LPSCl–C 나노복합 | 142 · `Fig. 8a,b` |
| OMC | Li₂S/OMC/LPSC (용액 함침 · 500 °C) | 27 (저자 그룹) · `Fig. 8c` |
| CR10 | Li₂S–LiI 를 ~10 nm 기공 탄소 replica 에 + Li₆PS₅Br + 탄소섬유 | 110 |
| hCNC | point-to-point → surface-to-surface 접촉 | 26 · `Fig. 8d` |
| LLTO/C | 혼합전도로 3상점 → S–MIEC 2상 계면 | 120 · `Fig. 9a` |
| 비정질 Li–Ti–P–S MIEC | σ_e **10⁻⁴–10⁻² S cm⁻¹ @25 °C** · 추가 SE 없이 S–MIEC 2상 계면 | 22 · `Fig. 9b` · ⚠ 우리 `wang2025_…` digest: MIEC10 2.45×10⁻⁶ 은 이 범위 밖 · σ_Li ~3×10⁻⁴ |
| 경고 | MIEC 의 전자전도가 비활성 영역을 깨워 **기생반응 위험↑** | — |

### 3g. 전해질 분해·창 (§3.3 · §4.3)

| 양 | 값 | ref · 그림 | 비고 |
|---|---|---|---|
| 황화물 고유 ESW | **≈1.7–2.1 V vs Li/Li⁺** | 20, 65, 66 | = [Zhu15] 층① 의 재인용 (§11-ii) |
| Li–S 작동 | 방전 평탄 ~1.5–2.1 V · 충전 컷오프 ~2.6–2.8 V | — | 기준전극 미기재 |
| 산화 분해 | P–S 절단 → 저전도 S-rich · P 함유 종 누적 → 계면 저항 | 28 | |
| 환원 분해 (양극 안 전자망) | → Li₂S · Li₃P · LiCl ("even more problematic") | 35, 67, 68 | Li–S 특유: **양극 안에서 산화·환원 양면 노출** |
| 탄소 | "electron leakage" · 표면 작용기·결함 화학반응 · 흑연화 탄소/CNF 가 LPSCl 에 더 불활성 | 69–73 | |
| SE 의 용량 기여 | 첫 방전 용량이 이론치 초과 → SE 산화 산물(S, P₂S₅)이 Li₂S 로 환원 (희생적) · 가역화하면 "추가 redox 저장고" | 58 · 7, 75 | |
| 창 확대 도핑 | 할로겐(**Cl**) · 전이금속(Nb) · O — *"suppressing high-potential electron excitation"* | 143–145 | 🔴 축 미명명 (§11-ii) |
| Li₃YCl₅I (Li₃YCl₆ + I 기계화학) | σ 1.67×10⁻³ S cm⁻¹ · 창 **0.89–3.25 V vs Li/Li⁺** (S 양극 1.5–2.8 V 포괄) · 0.1C 100 사이클 81.5 % | 105 | 층 미기재 |
| CNG (질화탄소/N-도프 그래핀) 호스트 | 넓은 갭 → 전자 주입 제한 + 피리딘 N 이 계면 Li⁺ 고정 → **SE 첫 탈리튬(S²⁻ 산화 개시) 억제 → S–P 절단·P₂S₇⁴⁻ 생성 억제** · ~2 mAh cm⁻² 230 사이클 RT · 11.3 mAh cm⁻² **@60 °C** | 28 · `Fig. 10a,b` | 계 = Li₅.₅PS₄.₅Cl₁.₅ |
| pOMS (전자 절연·극성 실리카) vs pOMC | 전자 유발 분해 억제 + 극성 고정 | 106 · `Fig. 10c` | |
| LPSCl 부분 가역 redox | 산화 → S + P₂S₅ (Li₃PS₄ 중간체 경유 가역 환원) · 더 깊은 환원 → Li₂S + Li₃P | 67 · `Fig. 10d` | |
| LPSCB (Cl → Br 부분 치환) + MWCNT | 초기 제어 분해 → Li₂S · LiₓP · LiCl/LiBr in situ · 미분해 SE 가 이온 연속성 유지 | 146 · `Fig. 10e` | |
| Cr₂S₃ + LPSC HEBM | 기계 유도 LPSCl 분해 → 전기화학 활성 S → 추가 용량 | 57 · `Fig. 10f` | |
| 분해 3분류 (§4.3 끝) | ① 비가역 기생 ② 자기제한 계면상 ③ 진짜 가역 redox — *"초기 용량 증가나 역전류 한 번으로는 부족"*, 가역성·소모량·수송 유지·저항 추이·장기 기여를 같이 보라 | — | §11-ii 에서 B②·B③ 로 옮긴다 |

### 3h. Li 금속 음극 (§3.4 · §4.4)

| 양 | 값 | ref · 그림 |
|---|---|---|
| Li\|황화물 자발 환원 SEI | Li₂S · Li₃P · LiCl (`Fig. 4a`) · **Li₃P 의 전자전도 → 자기제한 실패** | 72, 80 |
| 단계적 재구성 | Li₆PS₅Cl → **Li₁₁PS₅Cl** 준안정 중간체 → Li₂S + LiCl | 81, 82 (= [Schw20]) |
| 덴드라이트 | "고탄성률이 막는다" 가정 기각 · 입계·결함·공극으로 필라멘트 (`Fig. 4b`) | 85, 86, 72 |
| 스택압 | 저압 = 공극·박리 / 고압 = 크리프 침투 (`Fig. 4c`) · 거칠기가 응력 증폭 | 85, 87, 88 |
| 내부 Li 석출 | 전자전도 높은 SE 에서 (`Fig. 4d`) | 21 |
| 임계 탈리 전류밀도 | 크리프가 부피 손실을 못 메우면 공극 누적 (`Fig. 4e`) | 89 |
| O 도입 | P–O 안정 · ESW 확대 · **전자 DOS 감소** · Li₃PO₄-rich 넓은 갭 부동태 → CCD↑ | 150–153 (🔴 축 미명명) |
| I · Cl 계면상 | LiI/LiCl-rich → 전자 누설 차단 | 154, 155 |
| 산화물 첨가·양이온 도핑 | ZnO · Sb₂O₅ · Sn · Ba | 156–160 |
| 인공 SEI | LiFSI → LiF-rich (161) · HFE → LiF (162) · H₃PO₄ → LiH₂PO₄ on Li (LGPS, 163) · 공공 풍부 β-Li₃N (164) | 161–164 |
| 합금 | Li–In 은 벌크 확산형 측면 줄무늬 석출 (165) · Ag–C ~5 µm 복합막(무음극, 166) · 선합금 Li–Sn/Al/Zn (167–170) | 165–170 |
| 설계 기준 | 높은 이온전도 · 낮은 전자전도 · **Li 대비 높은 계면에너지** → Li₃N–LiF 복합 · **>6 mA cm⁻²** 무덴드라이트 | 171 |
| LACSS | Li₉Al₄ + LiCl 복합 SEI · 금속 Li 희석 벌크 | 172 |
| Li–S 특화: 나노 LiI 층(요오드 증기) | ~1400 mAh g⁻¹ RT · 150 사이클 80.6 % · ≥1.35 mAh cm⁻² · 90 °C | 173 · `Fig. 11a` |
| Li–Al (Li₀.₈Al) | 부피변화 ~96 % (Li₄.₄Si ~320 %) · 200 사이클 93.29 % · N/P 1.125 · 541 Wh kg⁻¹ · *"LGPS 실용 안정창 안 → thermodynamically suppressing"* | 174 · `Fig. 11b` (🔴 그림과 모순, §10-④) |
| LSCI (Sn–C → Li₁₃Sn₅ + 리튬화 C) | 저압 >300 사이클 ~80 % · ~1200 mAh g⁻¹ | 175 · `Fig. 11c` |
| LixSi 전 활성 음극 | 응력 변동 ~0.7 MPa @~3 mAh cm⁻² · >500 사이클 · 1.2C ~69 % | 118 · `Fig. 11d` |
| 80LiB (Li₅B₄ 골격) + Ag@C | ~1316 mAh g⁻¹ · 60 사이클 82 % | 176 · `Fig. 11e` |

### 3i. 공학 지표 (§3.5 · §5)

| 영역 | 내용 · 수치 | ref · 그림 | 비고 |
|---|---|---|---|
| S 로딩 | 통상 1–3 vs 실용 **>5 mg cm⁻²** | 93, 94 | 텍스트층 "45" = ">5" |
| 막 기준 | **<30 µm** · 높은 σ/컨덕턴스 · 강도+유연 · roll-to-roll | 187 | |
| 후막 반응 불균일 | 중성자 영상: SE 쪽 우선 반응 · 3층 경사 → 30·100 mg cm⁻² · **LCO** 100 mg cm⁻² → 10.4 mAh cm⁻² @2.25 mA cm⁻² | 180 · `Fig. 12a` (미실독) | ⚠ Li–S 아님 |
| 경사 미세구조 | 급속충전 +34.04 % · 구조손상 −20.34 % @14.895 mA cm⁻² | 181 | |
| FAST (수직 CNT 3D 프린팅) | ~50 mg cm⁻² | 182 | |
| VL-LFP + PEO@GF | 1.52 mAh cm⁻² @LFP 10.5 mg cm⁻² | 183 | ⚠ Li–S 아님 |
| 박막 SE (일반) | LLTO 테이프캐스팅 25–160 µm · 25 µm 3점 굽힘 264 MPa (190) · LLZTO/PEO ~60 µm (191) · PI 지지 Li₆PS₅Cl₀.₅Br₀.₅ 40–70 µm · 400 °C · 29 mS @30 °C (193) · P(VDF-TrFE)/LPSCl 30–40 µm · ~1.2 mS cm⁻¹ · t⁺≈1 (194) · **PTFE 0.2 wt% + Li₅.₄PS₄.₄Cl₁.₆ 99.8 wt% → ~30 µm · 8.4 mS cm⁻¹ · ~0.35 Ω cm²** (196, 저자 그룹) · LLZTO 90 wt% ~20 µm · bulk ~10⁻⁴ S cm⁻¹ · 41.2 mS · 창 4.6 V · t⁺ 0.81 (197, 저자 그룹) | 190–197 · `Fig. 13` (미실독) | ⭐ ref 196 의 조성 = 우리 **modelc 화학량** (2차 인용 · §11-v) |
| Li–S 박막 SE | LPSCl–XNBR <50 µm · <1 MPa · S 3.54 mg cm⁻² (198) · LPS–Kevlar ~100 µm · Li₂S 7.64 mg cm⁻²(≈7 mAh cm⁻²) · 370.6 Wh kg⁻¹(집전체 제외) (199) · PEO–PAN–LiTFSI ~30 µm · 70 °C (117) | 198, 199, 117 · `Fig. 14` (미실독) | |
| 저압 — 전해질 | 산화물 탄성률 ≥100 GPa · **황화물·할라이드 ≈10–30 GPa** (번호 없음) · 고분자 σ ≤10⁻⁵–10⁻⁴ S cm⁻¹ · 탄성 공중합체 + 공융 ~2×10⁻³ S cm⁻¹ · 셀 내압 ~10²–10³ kPa(Si·LFP) (99) · 자가치유 PEU ~0.2 MPa · Li\|SPE\|Li >6000 h @0.2 mA cm⁻² (114) · LATP 70 wt% 플라스틱 세라믹 ~0.1 MPa (200) · xLiCl–GaF₃ (1 ≤ x ≤ 4) 탄성률 <1 MPa (201) · VIGLAS LiAlCl₄–75 %O / NaAlCl₄–75 %O **Tg −16.8 / −25.5 °C** · <0.1 MPa (202) | 99–202 · `Fig. 15` (미실독) | |
| 저압 — 전극 | LTO 무변형 (203) · LCO + NCM 응력 상쇄 (204) · 균질 양극 Li₁.₇₅Ti₂(Ge₀.₂₅P₀.₇₅S₃.₈Se₀.₂)₃ 부피변화 ≈1.2 % · >20,000 사이클 · ≈390 Wh kg⁻¹ · 34 mg cm⁻² @2–5 MPa (205) · Co-TPDC-MOF 음극 ~1 % · NCM811 @5 MPa · 700 사이클 ~82 % (30 °C · 1.5 mA cm⁻²) (206) | 203–206 · `Fig. 16` (미실독) | ⚠ 전부 Li–S 아님 |
| 저압 — 계면 | Ag⁺ 도핑 아지로다이트 → 입계 Ag 석출 · **7.0 mAh cm⁻² · 1312 Wh L⁻¹ @2 MPa** (207) · DPF → LiF–LiₓPᵧO_zF 계면상 · 2C **>4500 사이클 @2.5 MPa** (208) · DAI(I⁻ 이동 LiI-rich): 2400 사이클 90.7 % @1.25 mA cm⁻² · **무가압 파우치 300 사이클 74.4 %** (209, 저자 그룹) | 207–209 · `Fig. 17` | ⚠ `Fig. 17b` 는 **NCM 셀**(그림에 명기) · `Fig. 17d` 는 Ni-rich 양극 full cell(본문 문맥 · 그림에 양극 라벨 없음) — 4500 사이클 쪽 용량은 `figure-read ≈` 75 mAh g⁻¹ |

---

## 4. 계산 — 이 리뷰가 옮긴 DFT 결과의 방법 정보 감사

> 리뷰 자체: code · functional(+vdW) · pseudo/PAW · k-points · ecut · supercell/nat · DFT+U · AIMD · MLIP · 무질서 처리 = **전부 n/a**.
> 본문 문자열 검색(35 pp): `NEB`·`nudged` 0 · `Bader` 0 · `AIMD`·`molecular dynamics` 0 · `machine learning`·`MLIP`·`interatomic` 0 · `convex hull`·`grand` 0 · `COHP` 0 · `density functional` 3 · `DFT` 3 (한 문장에 둘이 같이 나오는 경우 포함) · `first-principles` 1.

| 2차 인용 계산 | ref | 계 | 리뷰가 준 방법 정보 | 판정 |
|---|---|---|---|---|
| OCV 곡선 (용매화 vs 비용매화 Li₂S₄) | 54 | Li–S 액체 vs "dry" | "DFT" 뿐 (범함수·용매 모델 0) | 정성 근거로만 |
| Li₂S₂ 준안정 서술 | 번호 없음 | Li₂S₂ · Li₂S · S₈ | 0 | 비교 기준이 S₈(=0) — hull 판정 아님 |
| 형성에너지 bulk vs LiI(100) | 59 | Li₂S₂ · Li₂S | 면 지수만 | 정규화·기준 미기재 — `Fig. 6a` hull 역전은 그림 수치로만 (§3d) |
| Li 추출에너지 3.78/4.10 · 공공형성 5.75 eV | 59 | 흡착 Li₂S₂·Li₂S · 벌크 Li₂S | 0 (Li 기준상태 미기재) | ⛔ **장벽 아님** — 홉 수 검산 (§3d) |
| 결합에너지 (Li–Se) | 129 | LiI-I · LiI-Li · 그래핀 | 0 | 그래핀 위 양수 — 분산 보정 여부 미상 |
| Li⁺ 이동장벽 1.71 → 0.6 eV | 115 | Li₂S · Cu⁺/I⁻-Li₂S | 0 (경로 · 공공 형성 포함 여부 0) | 🔴 실험 D 변화와 **18.6 자릿수** 불일치 (§10-②) |
| M 3d–S 3p 혼성 서술자 | 123 | Co/Mn/V–N₄–C | 0 | 정성 |
| Ni d 재혼성 (dsp² ↔ d²sp³) | 102 | NiNC + Li₂S₂ | 0 (`Fig. 6f` 전하 규약 미기재) | 정성 |
| "electronic DOS 감소" | 150 | O 도핑 Li₃PS₄ · Li₆PS₅X | 0 | 갭 ≠ ESW (§11-ii) |
| PBE 갭 · AIMD · ICOHP (MIEC) | 22 | Li–Ti–P–S 유리 | (리뷰엔 없음) | 우리 `wang2025_…` digest(§J-45) 가 원전 구조로 감사 완료 |

⇒ **우리 grand-potential·ICOHP·MLIP-MD 의 방법 대조를 이 리뷰로 할 수 없다.** 방법을 보려면 원전(§12)으로 간다.

---

## 5. 절별 상세

### 5.1 §1 서론 — 왜 고체인가, 그리고 왜 그것만으로는 안 되나

액체 Li–S 는 다공성 C/S · 기능성 분리막 · LiNO₃ · (국소)고농도 전해질 · 촉매로 버텨 왔지만 *"용해성 다황화물 경로"* 자체가 셔틀·부식·과잉 전해질/Li 로 에너지밀도를 깎는다. 황 화학은 본래 **고체 S ↔ 고체 Li₂S** 의 상변환인데 액체가 그 사이에 용해 경로를 끼워 넣는다는 진단이다. 고체로 바꾸면 셔틀은 사라지지만 반응이 *"diffusion-mediated → solid–solid, interface-limited, transport-coupled"* 로 바뀌면서 새 제약 다섯이 생긴다: ① 다전자 전달 · S–S 절단의 높은 장벽(refs 17, 18) ② 전자·Li⁺ 가 각각 다른 상으로 와서 국소 계면에서만 만나야 함 ③ 부피변화 → 박리·균열(ref 19) ④ SE 의 좁은 창 · 양쪽 전극과의 부반응 ⑤ 높은 스택압(refs 20, 21). 기존 리뷰와의 차별점은 *"재료군별이 아닌 기전–구조–공학 통합"* 이라고 스스로 규정한다.

### 5.2 §2.1 구성 — SE 4부류와 복합 양극

SE 4부류(황화물 · 산화물 · 할라이드 · 고분자)의 장단을 한 문단씩 정리한다. 황화물(LPSCl·LGPS)은 σ 10⁻³–10⁻² S cm⁻¹ · 가공성 좋으나 수분·H₂S · 화학 안정성 문제, 산화물(LLZO)은 10⁻⁴–10⁻³ · 취성, 할라이드(Li₃YCl₆·Li₃InCl₆)는 산화 안정 좋으나 Li 금속에 불안정, 고분자(PEO)는 유연하나 상온 σ 부족·다황화물 차단 미흡. 복합 양극은 활물질(S 또는 Li₂S) + SE(30–60 wt%) + 탄소. S/Li₂S 의 전자전도 ~10⁻³⁰ S cm⁻¹ 과 최대 ~80 % 부피변화가 설계를 강제한다. 음극 쪽은 *"액체는 젖음으로 거칠기를 메우지만 고체는 접촉 손실 → 전류 국재화 → 크리프 지배"* 로 요약하고, Li 두께 변화가 면적용량에 비례한다는 점(ref 47)을 짚는다.

### 5.3 §2.2 반응 기전 — 단일 평탄은 고체 고유가 아니고, 1단 16전자는 비현실적이다

논증 흐름이 이 리뷰에서 가장 정돈된 부분이다.
1. 액체(에테르)는 두 평탄(`Fig. 2a`), 고체는 단일 평탄(`Fig. 2b`) — Gibbs 상률로 *"2상 평형 하나 = 평탄 하나"*.
2. 그런데 단일 평탄은 고체만의 것이 아니다: DFT 로 용매화 세기를 바꾸면 2 평탄 ↔ 1 평탄이 갈리고(ref 54), 고농도 전해질·<2 nm 미세기공에서도 단일 평탄이 나온다(refs 54–56). ⇒ *"용매화가 약할수록 중간체 형성이 불리해져 직접 전환 쪽으로 간다."*
3. 실제 ASSLSB 초기 용량은 대개 <1400 mAh g⁻¹ — 16 전자 1단 전환이 실제로는 거의 안 일어난다는 정황. S₈ 고리 개환에 여러 S–S 절단이 필요하므로 *"모든 중간 상태를 건너뛰는 것은 일어날 법하지 않다"*.
4. 2023 년 두 편(ref 59 Kim: XAS + ToF-SIMS · ref 60 Cao: operando)이 **Li₂S₂ + Li₂S 공존**을 보였고, 고체에서는 Li₂S₂ 가 **갇힌 고체 중간체로 방전 끝까지 남을 수** 있으며 두 단계가 별개 평탄으로 안 갈릴 수 있다 → `Eq. 1`·`Eq. 2` 의 2단 고체 전환.
5. 열린 질문: 다른 중간체가 있나 · 그 안정성이 **SE 환경에 어떻게 의존하나** · 2상 평형이 여럿 생길 수 있나.

⚠ 4 의 "first-principles" 근거 문장은 비교 기준이 S₈(원소 = 0)이다. 준안정성을 말하려면 S₈–Li₂S 연결선(hull) 대비 거리를 말해야 한다 — 리뷰 자신의 `Fig. 6a` 수치로 그 거리는 ≈0.18 eV/atom 이다(§3d, 우리 산수). 5 의 "SE 환경 의존" 은 **li2s 가설과 정확히 같은 물음**이지만 리뷰는 답을 주지 않는다(§11-i).

### 5.4 §2.3 수송과 TPB — "가장 작은 기능 단위"

전자는 탄소망으로, Li⁺ 는 SE 로 *"서로 독립이지만 국소적으로 결합된 두 경로"* 를 타고 와서 **S(또는 Li₂S) · SE · 전자전도체가 만나는 3상계면(TPB)** 에서만 반응한다. TPB 의 *접근성* 은 두 망의 연속성과 공간 분포가 정한다. 정량 논의는 §3.2 로 넘긴다.

### 5.5 §3.1 본질 동역학 장벽

S 쪽: 강체 기질 속 다중 S–S 절단·재배열, 용매 완충 없음 → 초기 리튬화가 본질적으로 느리다(고전류·저온에서 악화). Li₂S 쪽이 더 나쁘다: 넓은 간격 이온결정 · 전자·Li⁺ 둘 다 못 나름 → 탈리튬·재구성의 큰 활성화 → **첫 산화가 평형 전위보다 훨씬 높은 전위를 요구**(ref 25). 여기에 결정상 핵생성·성장·수축의 계면에너지와 변형 페널티가 얹혀 *"rugged energy landscape"* 가 된다. ⇒ §4.1 의 촉매·매개체·전자구조 공학의 동기. **장벽 수치는 이 절에 하나도 없다.**

### 5.6 §3.2 수송·TPB 제약 — Da > 1 과 코어–셸

나노 혼합만으로는 부족하다 — **전극 두께를 가로지르는 연속 경로**가 없으면 TPB 밀도가 높아도 소용없다. 방전 중 Li₂S 가 TPB 에서 핵생성해 **저항성 생성층**이 되고 그 아래 미반응 S 를 막는 **코어–셸**(Li₂S-rich 셸 · S 코어)이 생긴다. 이를 **Damköhler 수 Da = 고유 반응속도 / 물질수송 속도**(ref 19)로 묶어, 고체 망에서 Da 가 자주 >1(수송 지배)이고 고로딩·고전류·저온에서 악화한다고 쓴다. 미세구조·입경·MIEC 로 Da 를 1 쪽으로 내리면 전환이 균일해진다. 화학–기계 결합: 방전 팽창이 SE 골격을 부수거나 전자망을 끊고, 충전 수축이 공극·접촉 손실을 낸다.

### 5.7 §3.3 전해질 분해·계면 불안정 — Li–S 에서는 양면 노출

황화물 ESW ≈1.7–2.1 V vs Li/Li⁺(refs 20, 65, 66)이 Li–S 작동 영역(방전 ~1.5–2.1 · 충전 컷오프 ~2.6–2.8 V)과 겹치므로 분해는 *"피하기 어렵다"*. 고전위에서 P–S 절단 → 저전도 S-rich·P 함유 종, 저전위에서 **양극 안 전자망 때문에** Li₂S·Li₃P·LiCl 로 환원 — NCM 양극에는 없는 *양면 노출*이다. 탄소는 이중 역할(필수 전자 경로 vs "electron leakage" 로 SE 를 국소 저전위에 노출 · 표면 작용기 반응); Li–S 는 퍼콜레이션 문턱(≈4 wt%)보다 탄소를 훨씬 많이 써서 문제가 크다. 마지막 문단: **SE 분해가 겉보기 용량을 낸다** — 첫 충전의 SE 부분 산화가 S·P₂S₅ 를 만들고 그것이 방전에서 Li₂S 로 환원(ref 58). 희생적이지만 가역화하면 *"추가 redox 저장고"* 가 될 수 있다(refs 7, 75).

### 5.8 §3.4 음극 — 화학 · 형태 · 기계의 세 실패

화학: 황화물은 Li 와 열역학적으로 비호환 → 접촉 즉시 Li₂S·Li₃P·LiCl SEI(`Fig. 4a`). 이상적으로는 전자 절연·이온 전도여야 하지만 **Li₃P 의 전자전도 때문에 자기제한이 안 된다**(refs 72, 80). LPSCl 은 **Li₁₁PS₅Cl** 같은 준안정 중간체를 거친다(refs 81, 82). 형태: 고탄성률이 덴드라이트를 막는다는 가정은 기각, 입계·결함·공극으로 필라멘트(`Fig. 4b`). 기계: 저압은 공극, 고압은 크리프 침투(`Fig. 4c`) · 전자전도 SE 의 내부 석출(`Fig. 4d`) · 임계 탈리 전류밀도(`Fig. 4e`, ref 89) · 1 mAh cm⁻² ↔ 4.85 µm(`Fig. 4f`). 고체 계면 손상은 *"대부분 비가역"*.

### 5.9 §3.5 응용 지향 도전

S 로딩 1–3 mg cm⁻²(실용 >5) · 두께가 늘면 경로가 길고 굴곡지고 TPB 가 성기며, 접촉을 위해 SE·탄소를 늘리면 S 분율이 희석되는 **에너지밀도–동역학 trade-off**. 초박막 SE 는 취성·핀홀·두께 불균일과 싸워야 하고, 수십–수백 MPa 스택압은 실험실 밖에서 비현실적(구조 복잡·무게·크리프·압력 이완·대면적 균일성).

### 5.10 §4.1.1 수송 공학 — 할라이드가 Li₂S 를 바꾸는 네 방식

(a) **Li₂S–LiX 고용체**(ref 125): LiX 로 σ 가 ~10⁻⁸ → ~10⁻⁶ S cm⁻¹ 대(`Fig. 5a`). (b) **LiI 만 특별**(ref 126): σ 가 비슷한데도 LiI 만 ≈95 % 이용률 → *"벌크 σ 로 설명 안 된다"* → 충전 중 고용체가 부분 해체되며 생기는 LiI-rich 미세상이 Li⁺ 경로이자 활성점, 방전 중 재편입(`Fig. 5b`). (c) **전자구조**: S₉.₃I(ref 122) — 갭 2.92 → ≈1.65 eV, σ_e 5.9×10⁻⁷ S cm⁻¹, 저융점 자가치유. (d) **계면층**: Li₂S 위 LiI 코팅(ref 127) — 2D ⁶Li EXSY 로 Li⁺ 가 LiI 층을 통해 이동, 두 계면 교환 Ea 0.142/0.117 eV(`Fig. 5c,d`). (e) **공정 유도 계면상**: UHS 혼합의 **할라이드 편석**(ref 101) — 아지로다이트의 할라이드가 빠져 양극 표면에 LiX-rich 나노 계면상, 추가 코팅 없이(`Fig. 5e`). (f) **할라이드 + 양이온 공도핑**: Li₂S–AlI₃(ref 128) · Cu⁺/I⁻(ref 115, D_Li ~2 자릿수 · σ_e 5–8 자릿수(→ 우리 산수 5–7) · DFT 장벽 1.71 → 0.6 eV).

### 5.11 §4.1.2 촉매 — 분극형(LiI) vs 오비탈 혼성형(TM·SAC)

두 부류로 나눈다. **LiI 의 분극 촉매**(ref 59): LiI(100) 위에서 Li₂S₂·Li₂S 형성에너지가 덜 음(`Fig. 6a`), 흡착 Li₂S₂/Li₂S 의 Li 추출에너지(+3.78/+4.10 eV)가 벌크 Li₂S 공공형성(+5.75 eV)보다 낮다 → *"탈리튬 장벽 감소"*, Li₂S₂ 가 더 쉽게 산화(`Fig. 6b`) — Li–Se 에서도 LiI 가 유사(ref 129, `Fig. 6c`). **TM 황화물**: CoS₂(ref 132) — 금속성 전자 경로 + Co–S 활성점, 1584 mAh g⁻¹ · 분극 0.34 V. **SAC**: Co–N₄(ref 24, `Fig. 6d`) 양방향 · Co/Mn/V 비교에서 M–S 결합 세기가 서술자(ref 123, `Fig. 6e`) · NiNC 의 Li₂S₂ 유도 재혼성(ref 102, `Fig. 6f`) — Li₂S₂ → Li₂S 를 병목으로 지목. 끝 경고: 촉매점에 S·Li⁺·e⁻ 가 동시에 접근해야 하고, 강흡착은 탈착을 막고, 촉매가 S 분율을 줄이며, SE 와의 부반응도 봐야 한다 — *"이론 모델·저로딩에서의 이득은 고로딩 복합 양극에서 재검증 필요."*

### 5.12 §4.1.3 Redox mediator — 액체의 확산 매개를 고체 안에서 흉내내기

정적 구조 조절(도핑·코팅·촉매) 대신 **산화상태가 바뀌는 매개체가 전하를 나른다.** 고분자 SPE 속 안트라퀴논(ref 25, `Fig. 7a,b`: Step A 화학 산화 · Step B 집전체 재산화) → PhSeLi 라디칼(ref 139) → 무기 고체로 확장: LiVS₂ 셸(ref 116, `Fig. 7c`: VS₂ 가 Li₂S 를 화학 산화) · LixIn₂S₃(ref 140) → **SE 자체를 redox 활성으로**: LBPSI 유리의 I⁻/I₂/I₃⁻(ref 100, `Fig. 7d,e`: TPB → 2상 계면) → **기계화학 계면상 LPSI**(ref 113, `Fig. 7f,g`: PI₃ + S₈ + Li₅.₅PS₄.₅Cl₁.₅ → 비정질 Li–I–S–P · 요오드와 PₓSᵧ 단위가 가역 redox · 4단계 활성화). 끝 경고: 고정 매개체는 범위가 짧고 전위·가역성이 맞아야 하며, **가역 매개와 희생 분해의 일시 용량을 구분해야** 한다.

### 5.13 §4.2 계면 구조 — 3상점에서 2상 계면으로

나노 3상(Nagao, ref 141) → 용액 bottom-up Li₂S–LPSCl–C(Han, ref 142, `Fig. 8a,b`) → 다공 호스트(OMC, ref 27, `Fig. 8c` · CR10, ref 110) → 계층 탄소(hCNC, ref 26, `Fig. 8d`) → **MIEC 로 2상 계면**(LLTO/C, ref 120, `Fig. 9a` · 비정질 Li–Ti–P–S, ref 22, `Fig. 9b`). 마지막 문장이 중요하다: MIEC 의 전자전도는 *"비활성 영역을 깨워 기생반응 위험을 키운다"* — 우리 `wang2025_…` digest 의 MIEC30 퇴화와 같은 방향.

### 5.14 §4.3 전해질 분해의 조절·활용 — 억제에서 활용으로

두 갈래 억제: (i) 조성·구조로 고유 안정성 올리기(할로겐·Nb·O 도핑, refs 143–145 — *"고전위 전자 들뜸·분해 억제"*) · (ii) 탄소망 설계로 SE–탄소 접촉 줄이기. 다음: 할라이드 SE 로 교체(Li₃YCl₅I, ref 105) · 계면 전하이동 조절(CNG, ref 28: Li⁺ 고정으로 첫 탈리튬 억제 → S–P 절단·P₂S₇⁴⁻ 억제, `Fig. 10a,b` · pOMS, ref 106, `Fig. 10c`). 그다음 방향 전환 — **분해를 활용**: LPSCl 부분 가역 redox(ref 67, `Fig. 10d`) · Br 치환 + MWCNT 로 초기 제어 분해 → LiCl/LiBr 부동태 + 미분해 SE 가 이온 연속성 유지(ref 146, `Fig. 10e`) · HEBM 으로 Cr₂S₃ 양극에 SE 유래 S(ref 57, `Fig. 10f`). 끝에 스스로 제동: *"분해가 일반적으로 이롭다는 뜻이 아니다"* — **비가역 기생 / 자기제한 계면상 / 진짜 가역 redox** 의 3분류와 판정 항목(가역성 · 소모량 · 수송 유지 · 저항 추이 · 장기 기여)을 제시한다. 이 3분류가 이 리뷰에서 우리가 가져갈 가장 쓸모 있는 틀이다(§11-ii).

### 5.15 §4.4 음극 계면 — 4 부류

(1) SE 도핑 유도 in situ(O → Li₃PO₄-rich · I/Cl → LiI/LiCl · ZnO·Sb₂O₅·Sn·Ba) — 기초 조절이지 단독으로는 부족. (2) 인공 계면상(LiF · LiI · Li₃N · 인산염; LiFSI·HFE·H₃PO₄ 유도 · 공공 풍부 β-Li₃N). (3) 합금(Li–In ≈0.62 V · 측면 줄무늬 석출 · Ag/Mg 고용체 · Ag–C ~5 µm 무음극 · 선합금 Li–Sn/Al/Zn — 용량 trade-off). (4) 다성분(Ji 의 설계 기준: 높은 이온전도 · 낮은 전자전도 · **Li 대비 높은 계면에너지** → Li₃N–LiF · LACSS). Li–S 는 S 의 큰 부피변화가 음극 Li 플럭스·응력을 흔들어 요구가 더 엄격하다 → 나노 LiI 층(`Fig. 11a`) · Li–Al(`Fig. 11b`) · LSCI(`Fig. 11c`) · LixSi(`Fig. 11d`) · 80LiB + Ag@C(`Fig. 11e`).

### 5.16 §5.1 고로딩 후막

반응 불균일의 원인을 *"두께 방향 이온·전자·반응 플럭스의 불일치"* 로 보고 경사 설계(SE 함량 경사 · 도전재·기공·입경 경사)와 저굴곡 구조(수직 CNT 3D 프린팅 · 얼음 템플릿)를 소개한다. ⚠ 대표 수치(LCO 100 mg cm⁻² · VL-LFP)는 **Li–S 가 아니다** — 이 절에는 §5.3 같은 '전이 가능성 단서' 문장이 없다.

### 5.17 §5.2 초박막 SE

기준 4개(<30 µm · σ · 강도+유연 · roll-to-roll)를 세우고 습식(테이프캐스팅 · 지지체 함침)과 건식(PTFE 섬유화 · 무용매 가소 성형)을 비교한다. 습식은 두께 제어가 좋지만 용매가 황화물 표면을 상하게 하고 유기 잔류물을 남긴다. Li–S 적용 사례(XNBR · Kevlar · PEO–PAN)는 아직 초기 단계라고 스스로 쓴다.

### 5.18 §5.3 저압 — 전해질 · 전극 · 계면

서두에 **중요한 자기 단서**: *"ASSLSB 에서 저압을 직접 다룬 연구가 제한적이라 Si·LFP·NCM 전고체 연구에서 원리를 가져오며, 이는 ASSLSB 의 직접 검증이 아니다."* 전해질(탄성 공중합체 · 자가치유 · 연성 무기 — xLiCl–GaF₃, VIGLAS) · 전극(무변형 · 부피 상쇄 · 균질 양극 · MOF 음극) · 계면(Ag 석출 친리튬 망 · DPF 부동태 · **DAI** 동적 적응 계면상). 마지막에 `Table 2` 로 실용 지표를 모으고 *"모든 실용 지표를 동시에 보인 연구는 거의 없다"* 고 인정한다.

### 5.19 §6 요약·전망 — 5 우선순위 (`Fig. 18`)

실험실 이득은 저로딩 · 많은 SE·탄소 · 두꺼운 SE · 과잉 Li · 고압이 **가린다**고 진단하고, 촉매는 후막에서 접근 불가해질 수 있고, 매개체는 액체 확산 없이 범위가 짧고, MIEC 는 전자전도가 공간 제어되지 않으면 SE 분해를 가속할 수 있다고 쓴다. 우선순위: ① 고로딩에서 균일·깊은 전환 ② **전해질·계면상 반응의 조절**(비가역 기생 / 자기제한 / 가역 redox / redox 매개 구분 — 계면상 조성·전해질 소모·임피던스·가역성·용량 기원을 장기 추적) ③ 초박막·신뢰성 막 ④ 저압/무압 안정 계면(전셀 수준 부피 상쇄) ⑤ 현실적 평가·제조(보고 항목: S 함량 · S 면적 로딩 · 면적용량 · SE 두께·면적질량 · 음극 용량/Li 과잉 · 제조압 · 운전압 · 전 구성요소 기준 셀 에너지밀도 · 파우치 검증 · H₂S 관리). 바탕: **operando 계측 + 원자–미세구조–셀 예측 모델링.** ⚠ 로드맵 그림에 **수치 목표가 없다**.

---

## 6. Post-processing · 분석 기법 (리뷰가 이름만 든 것)

| 기법 | 등장 위치 | 무엇에 | 우리에게 |
|---|---|---|---|
| XAS + ToF-SIMS | §2.2 (ref 59) | Li₂S₂ + Li₂S 공존 확인 | Li₂S 계면 조성 판독의 실험 짝 |
| operando (Cao) | §2.2 (ref 60) | S₈ → Li₂S₂ → Li₂S | — |
| in situ TEM | §2.2 (ref 53) | 직접 전환(초기 견해) | — |
| 2D ⁶Li–⁶Li EXSY NMR | §4.1.1 (ref 127) · `Fig. 5c` | 상간 Li⁺ 교환 · 교환 Ea | ⭐ **li2s 가설 검증용 측정법** (계면상이 Li⁺ 를 넘기나) |
| HAADF-STEM + EDS | §4.1.1 (ref 101) · `Fig. 5e` | Cl 표면 편석 | 밀링 계면상 조성의 직접 관측 형식 |
| UV-Vis 흡수단 | §4.1.1 (ref 128) | Li₂S–AlI₃ 간격 축소 | 광학 간격 — 우리 PBE 갭과 비교 금지 |
| in situ 중성자 영상 | §5.1 (ref 180) | 두께 방향 반응 불균일 | DEM 후막 축 배경 |
| DFT (OCV · 형성/추출/결합에너지 · 장벽 · 혼성) | §2.2 · §4.1.1–4.1.2 | §4 표 | 방법 정보 0 |
| Damköhler 수 | §3.2 (ref 19) | 반응–수송 경쟁 | DEM 축 무차원 서술자 후보 |
| 압력·변위 계측 | §6 | operando 기계 | — |

**수치화·플롯·기록 방식**: 리뷰는 원전 그림을 재수록할 뿐 재분석·재플롯이 없다. `Table 1`·`Table 2` 가 유일한 자체 정리물인데 용량 기준(S/Li₂S)·온도(표 2)·기준전극·음극 종류 열이 없다.

---

## 7. 우리 DFT 대비 (`../our_dft_baseline.md` · 원장)

> ⛔ 이 리뷰의 수치는 소환값이다 — 우리 db 절대값과 **방법 명시 없이 섞지 않는다.** 수송(σ·D·Ea)은 1저자 인용정책(2026-09-18)상 우리 쪽도 **계 간 상대차로만** 쓰고, 이 표에는 우리 수송 숫자를 **하나도 싣지 않는다.**

| 항목 | 이 리뷰 (2차 인용) | 우리 (원장) | 같은가 / 다른가 / 왜 |
|---|---|---|---|
| ESW 산화 쪽 | "≈1.7–2.1 V vs Li/Li⁺" (refs 20, 65, 66) = [Zhu15] LPSCl **2.01** · LGPS 2.14 의 재인용 | comp1 = modelc 산화 onset **2.256 V** (층① · LiS₄ 제외 GG set; 포함 시 2.14) | **같은 층 · 같은 반응식.** 산화 쪽 0.246 V 차는 **원인 미확정**(제외 상 몫 ≈0.116 V + MP 판본 후보) · ⛔ 창 **폭**은 인용하지 않는다 (`HZ-esw-reduction-limit-label`) |
| ESW 환원 쪽 | "≈1.7" | **1.717 V** (교환 0 가장자리 · 2026-09-22 라벨 정정) | [Zhu15]·[Schw21] 1.72 와 0.003 V |
| 산화 사다리 | LPSCl → Li₃PS₄ + LiCl → (산화) S + P₂S₅ (ref 67, `Fig. 10d`) · 자유 S²⁻ 탈리튬 → S–P 절단 → **P₂S₇⁴⁻** (ref 28) | 2.256 V `Li₆PS₅Cl → Li₃PS₄ + LiCl + S + 2Li⁺ + 2e⁻` → 2.385 V (P₂S₇ + S) → 3.326 V (SCl) | **같은 순서 · 같은 첫 산물** (자유 S²⁻ 먼저, 다음 P–S 골격 축합). 우리 2단 산물 종 = ref 28 이 이름 붙인 종 — 2차 인용이라 원전 확인 전 '일치' 로 쓰지 않는다 |
| 환원 산물 | Li₂S · Li₃P · LiCl (`Fig. 4a`; refs 35, 67, 68) | [Zhu15] LPSCl → Li₃P + Li₂S + LiCl · `sei_products.json` 역할: **Li₃P conductor-LEAK** · LiCl insulator · Li₂S marginal | 같은 종. 리뷰의 *"Li₃P 전자전도 → 자기제한 실패"*(refs 72, 80)는 우리 역할 분류와 **같은 방향** — `[Xiao20Rev]` 의 passivating 서술과는 갈린다 |
| Cl 과 창 | *"할로겐(Cl) 도핑이 창을 넓힌다"* (refs 143–145) | Cl 1.0 → 1.6(modelc)에서 **층① onset 불변** (2.256 V · S²⁻-limited) · `[Zuo22]` CV 피크 전위도 동일 | 🔴 **축 미명명.** 층①로 읽으면 우리·`[Zuo22]` 와 반대 · 층③(겉보기)이면 별개 |
| 갭·전자구조 | S 2.92 → S₉.₃I ≈1.65 eV (ref 122) · Li₂S "wide-bandgap" · Li₂S–AlI₃ 흡수단 270 → 350 nm | S · S₉.₃I · Li₂S–AlI₃ **계산 없음** · 갭은 PBE fixed-occ nscf 정본만 (예: comp1 2.066 · LPSOCl 2.2309 eV) | 문헌과 절대 비교 금지 — **"wide-gap" 수준만**. (우리 산수) 350 nm ≈3.54 eV 도 넓은 간격 |
| 이온 수송 (Li₂S 관련) | Li₂S–LiX ~10⁻⁶ S cm⁻¹ · EXSY Ea 0.142/0.117 eV · DFT 1.71 → 0.6 eV | **나란히 놓을 값이 없다** — li2s 유리는 마감(허용 ① · 수송 계수·Ea 미보고) · Li₂S NEB 는 `HZ-sei-neb-retracted` **BLOCKED** | 비교 불가 (있어도 상대차만) |
| 기계 | *"황화물·할라이드 탄성률 ≈10–30 GPa"* (번호 없음) · 산화물 ≥100 GPa | E_VRH (relaxed-ion · PBE) comp1 **22.06** · modelc **27.66 GPa** (canonical) | 띠 안. 리뷰 쪽 출처 없음 → **띠 확인 이상 쓰지 않는다** · functional·relaxed/clamped 명시 없이 비교 금지 |
| 결합 서술자 | M–S 결합 세기(SAC) · Ni d 혼성 | ICOHP (comp1 P–S **−5.938 eV** canonical) — M–S SAC 계산 없음 | "결합 세기 = 서술자" 발상만 공유 |
| 양극(CAM\|SE) 계면 | S/Li₂S 양극 \| SE 화학 반응성 **서술 없음** (VS₂·Cr₂S₃·MIEC 사례뿐) | B③ 은 산화물 양극만 (`oxidation_stability.json` 의 interface_reactivity) | **Li–S 판 B③ 은 우리에게도 리뷰에도 없다** → §11-iii E3 |
| MLIP/MD | 0회 (로드맵의 "predictive modeling" 만) | UMA-s-1p1 MLIP-MD (상대차만 인용) | 리뷰가 우리 방법 스택을 평가하지 않는다 |

---

## 8. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 연대표 2016 → 2025+: Han142(3상계면 액상 구축) · Hakari125(Li₂S–LiX) · Gao25(AQT 매개체) · Fujita126(LiI 도메인) · Ji118(LixSi) · Kim59(*"LiI doping lowers Li₂S₂/Li₂S conversion barrier · Li₂S₂ 확인"*) · Zhong24(Co–N₄) · Luo26(hCNC) · Jiang110 · Song100(LBPSI) · Wang22(MIEC) · Lee101(할라이드 편석) · Wang113(LPSI). 다른 그림 패널 재사용 | 원전 확보 순서표. ⚠ Kim59 칸의 "barrier" 는 장벽이 아니라 형성·추출에너지 (§10-①) |
| 2a,b | 액체 vs 고체: 자유에너지 계단(S₈ → Li₂S₈ → Li₂S₆ → Li₂S₄ → Li₂S₂ → Li₂S / 고체는 S₈ → **Li₂Sₓ?**(회색·물음표) → Li₂S₂ → Li₂S) + 전압 개형(액체 2 평탄 · 고체 단일). 축 숫자 없음 | 도식. 자유에너지 축 기준상태 없음. 본문 "단일 평탄" ↔ 그림의 **경사형** 방전 곡선 |
| 3 | 본질 한계 4칸(반응 동역학 · 수송 · 전해질 열화 · Li 음극) + 응용 3칸(저로딩 · 두꺼운 SE · 고압). 전해질 칸 라벨 *"Narrow voltage window"* | ESW 축 미명명의 대표 그림. ⚠ "L₂S" 오타 2회(동역학 칸 · TPB 삽도) |
| 4a–f | Li\|SE: (a) Li⁺ + e⁻ + SE → Li₂S + Li₃P + LiCl (b) 덴드라이트 (c) 저압 접촉손실 / 고압 크리프 침투 (d) 입계 핵생성(Li⁺ + e⁻ → Li) (e) 크리프 한정 탈리 (f) 1 mAh cm⁻² ↔ Δh 4.85 µm | (a) = 우리 환원 산물과 같은 종(§7). (f) 우리 산수로 재현 |
| 5a | Li₂S–LiX σ vs LiX mol% — `figure-read ≈` 0 %: 8×10⁻⁹ · 10 %: LiI 2.5e-7 / LiBr 1.6e-7 / LiCl 1.1e-7 · 20 %: LiI 2.2e-6 / LiBr 4.6e-7 / LiCl 5.6e-7 · 30 %: LiBr 3.3e-6 / LiCl 2.1e-6 S cm⁻¹ | li2s: *"Cl 이 Li₂S 쪽으로 들어가는 경로"* 의 크기 감각(2차). 20 % 에서 LiI ≈4× — 본문 "comparable" 과 어긋남 |
| 5b | Li₂S–LiI 고용체 → (충전) Li₂Sₓ + LiI 도메인 → (방전) **Li₂S–LiI + LiI 도메인** | 그림은 방전 뒤 LiI 도메인 잔존 — 본문 "고용체 복원" 보다 약하다 |
| 5c | 2D ⁶Li–⁶Li EXSY: mLi₂S(LiI)–mLPSC · **Tmix 10 s · 373 K** · 교차 피크 Li₂S/LPSC(≈2–2.5 ppm) ↔ LiI(≈−4.5 ppm) | ⭐ li2s 가설 검증용 **측정법** 후보. 측정 온도는 리뷰 본문에 없다 |
| 5d | Li₂S/LiI 셸 + LPSC 수송 도식 | — |
| 5e | HAADF-STEM/EDS: pristine LPSCl vs **S/LPSCl/C 2000 rpm 5 h** — Cl 테두리 · P 내부 | li2s **경쟁 가설**: 밀링 계면상이 LiX-rich 일 수 있다. 이 패널만으로는 어느 입자의 표면인지 못 가린다(P 가 안쪽) |
| 6a | 원자당 형성에너지 vs x = 2/(n+2): "Vacuum"(본문 "bulk") Li₂S₂ −1.01 · Li₂S −1.59 / LiI(100) `figure-read ≈` −0.71 · −0.60 eV | (우리 산수) bulk Li₂S₂ 는 S₈–Li₂S 연결선 **위 ≈0.18**, LiI 위에서는 **아래 ≈0.26 eV/atom** = 리뷰가 말하지 않은 hull 역전. 기준상태 미기재라 판정 아님 |
| 6b | "Transition State Li-S* + Li*" 도식: Li₂S₂_ads **3.78** · Li₂S_ads **4.10 eV** · **0.42 eV**(본문 미언급) · 축척 없음 | ⛔ **장벽으로 인용 금지** — 홉 수 검산 Γ ≈ 10⁻⁵¹ s⁻¹. 기준상태 미기재 추출에너지 |
| 6c | Li–Se 결합에너지(LiI-I / LiI-Li / 그래핀) — §3d `figure-read` 값 | 그래핀 위 Se₈·Li₂Se₆ 양수 = 분산 보정 여부 의문. 황화물 수치 아님 |
| 6d | CoN₄–S + 2Li⁺ + 2e⁻ → Li₂S–CoN₄ → 2Li⁺ + 2e⁻ + CoN₄–S | — |
| 6e | SAC: 방전 *"✓ dissociate / weak M-S · ✗ poison / strong M-S"* · 충전 *"✓ catalyze / strong M-S · ✗ idle / weak M-S"* | 🔴 본문(약한 M–S → 불완전 방전)과 **방전 칸 방향이 반대** |
| 6f | NiNC: Li₂S₂ 흡착 시 Li–S 늘어남 · 전하 −0.86 → −0.84 · +0.86 → +0.67(무엇의 전하인지 라벨 없음) · dsp² ↔ d²sp³ 순환. 일부 글자가 그림에 가려짐 | 전하 규약 미기재 — 우리 Bader 부호 규율(`[Liu26Sn]` §J-46) 상기용 |
| 7a,b | SPE 속 RM: Step A(Li₂S + RMox → LiPSs + Li⁺ + RMred) · Step B(RMred → RMox + e⁻) · 첫 충전 활성화 스파이크 소멸(도식) | 수치 없음 |
| 7c | Li₂S/LiVS₂ → Li₂S/VS₂ → 이중 코어–셸 Li₂S/S/LiVS₂ → S/VS₂ · **Li₂S + 2VS₂ → 2LiVS₂ + S** | 고체 매개체 반응식의 원형 |
| 7d,e | 재래 vs redox 매개 SE(LBPSI): 비활성 Li₂S 가 2상 계면에서 활성화 · I⁻/I₃⁻ 순환 | ESW: **설계된 B②** — SE 가 일부러 redox 에 참여 |
| 7f,g | S@LPSI/LPSC: 계면상이 접촉·수송 개선 / 4단계(Inhibition → Activation → Intensification → Stabilization · P–[S]ₙ–P 등장 · O2 경로 소멸) — 막대는 정성 | li2s: **기계화학 비정질 아지로다이트 유래 계면상**의 최근접 문헌 사례(단 I 함유 · S 양극). ⛔ 우리 유리 1 시드의 말단 P–S–S(마감 ⑧)와 **연결하지 않는다** — 모티프(가교 vs 말단)·근거(거리 기준) 다름 |
| 8a,b | Li₂S–Li₆PS₅Cl–PVP → 550 °C Ar → Li₂S–LPSCl–C · HRTEM(2 nm 막대): Li₂S 격자무늬 + LPSCl·C 영역 점선 경계 | li2s: Li₂S\|LPSCl 나노 접촉 실물 — **계면상 유무를 판정할 해상·대비가 아니다**. 550 °C 반응 여부를 리뷰가 묻지 않는다 |
| 8c | FeCl₃ + 도파민 → OMC → Li₂S/LPSC 용액 함침 → 500 °C | ref 27 = 저자 그룹 |
| 8d | AB(point-to-point · 높은 굴곡도) vs hCNC(surface-to-surface · 연속 경로) | DEM 접촉 위상 도식 |
| 9a,b | 3상 계면 vs 혼합전도 2상 계면 · 재래 vs 2상 ASSB(Dead/Active sulfur) | `[Wang25MIEC]` 원전 그림 — 우리 digest 가 정본 |
| 10a | LPSCl1.5 구조: 16e(PS₄) · **4a/4d(S/Cl 자유 음이온)** | 우리 *"자유 S²⁻ 가 먼저 산화"* 서사의 그림 짝 |
| 10b | 탄소 위 아지로다이트 "Decompose"(Li 이탈 → S) vs CNG 위 "Oxidation suppressed"(N 이 Li⁺ 고정) | **B②(속도 억제)** — 층① onset 을 옮기는 그림이 아니다 |
| 10c | pOMC/S vs pOMS/S 순환 — 분해산물(녹색) 축적 유무 | B②(전자 접근 차단) |
| 10d | LPSCl 산화환원 경로: LPSCl → Li₃PS₄ (+ LiCl) · Ox → S + P₂S₅ · Red → Li₂S + Li₃P | 우리 층① 사다리(2.256 V Li₃PS₄ + LiCl + S → 2.385 V P₂S₇ + S)와 **같은 순서 · 같은 첫 산물** |
| 10e | Li₆PS₅Cl₀.₅Br₀.₅–MWCNT "Redox layer" | — |
| 10f | Cr₂S₃ + LPSC + VGCF HEBM → 전해질 유래 S | ESW B②: 기계화학 분해 = 용량원 |
| 11a | 요오드 증기 → Li 위 LiI 층 \| LGPS | — |
| 11b | Li–Al 합금 셀 + LGPS **"Practical stability window" 0.125–2.745 V** · **"HOMO: 2.1 V / LUMO: 1.7 V"** · LiAl 은 LUMO 훨씬 아래(실용창 안) · S 는 HOMO 선 위 | 🔴 본문 *"thermodynamically suppressing"* 과 모순(그림 = 실용창 = 층③). HOMO/LUMO 라벨 = **밴드엣지 ≠ 분해 onset** 의 반례 |
| 11c | Li/LSCI/SSE/S 셀: lithiated Sn + C · 균일 Li⁺ 플럭스 · SE 분해 제한 | — |
| 11d | 복합 vs 전 활성 μ-LixSi 전극 · 탈리튬 단계 | — |
| 11e | Li 금속 vs 80LiB(LiB 골격) + Ag@C 층 | 점착 트랙 배경(Ag–C) — 수치 없음 |
| 12a–d | (캡션 기준 · 미실독) 3층 경사 양극 · 경사 미세구조 · FAST(수직 CNT) · 얼음 템플릿 VL-LFP | DEM 후막 축 배경. ⚠ LCO·LFP 사례 |
| 13a–j | (캡션 기준 · 미실독) LLTO 테이프캐스팅 25 µm · PI 지지 Li₆PS₅Cl₀.₅Br₀.₅ · LPSCl@P(VDF-TrFE) · PTFE 건식 Li₅.₄PS₄.₄Cl₁.₆ 막(13f–h) · LLZTO 건식 막(13i,j) | 13f–h 조성 = 우리 modelc 화학량 (ref 196 · 2차) |
| 14a–j | (캡션 기준 · 미실독) LPSCl–XNBR 박막 · Kevlar 보강 LPS · PEO–PAN–LiTFSI | — |
| 15a–f | (캡션 기준 · 미실독) 탄성 전해질 · 자가치유 SPE 일체 코팅 · 2LiCl–GaF₃ 성형성 · VIGLAS 응력–변형/크리프 | 기계 축 배경 |
| 16a–f | (캡션 기준 · 미실독) LCO/NCM 응력 상쇄 · 균질 양극 수송·장기 사이클 · MOF 음극 압력 변화 | ⚠ 전부 Li–S 아님 |
| 17a,b | Ag 도핑 LPSCl → 입계 Ag 석출 → Li 도금 · **SUS\|Li₅.₄Ag₀.₆PS₅Cl\|Li₆PS₅Cl₀.₅Br₀.₅\|NCM** 무음극 셀 7.0 mAh cm⁻² · `figure-read ≈` 205 → 190 mAh g⁻¹ / 50 사이클 · 첫 CE ≈90 % | ⚠ **NCM — Li–S 아님** |
| 17c,d | Li₂S 기반 SEI(친리튬 · 저 CCD) vs SREI(소리튬 · 전자차단 · 고 CCD) · DPF LPSC 2C(1C = 1.3 mA cm⁻²) · 30 °C · `figure-read ≈` 75 mAh g⁻¹ · ~90 % @4,500 · 평균 CE 99.96 % | ⚠ Ni-rich 양극 full cell(본문 문맥 · 그림엔 양극 라벨 없음) — Li–S 아님. 4500 사이클 헤드라인의 **용량 수준이 본문에 없다** |
| 17e | Li₃.₂PS₄I₀.₂ 탈리 4단계(공극 → 공극 → conformal → DAI) · I⁻ 이동 | ref 209 = 저자 그룹 |
| 18 | 로드맵: 실험실 이득 → 실용 격차(저로딩 · 두꺼운 SE · 과잉 Li · 고압 · 낮은 면적용량) → 5 우선순위 + "Reaction + transport + mechanics" + operando·예측 모델링 → 실용 ASSLSB | **수치 목표 없음** |
| Table 1 | 30 행: 양극 조성 · 설계 전략 · 가역용량 · 전류밀도 · 로딩 · 수명 · T | §9 전사. ⚠ 용량 기준(S / Li₂S / 복합) 미기재 |
| Table 2 | 22 행: 양극 · 로딩 · 면적용량 · SE · 두께 · 운전압 · 용량 · 수명 | §9 전사. ⚠ **온도 열 없음** · 텍스트층 ">20" → "420" 오독 |

---

## 9. `Table 1` · `Table 2` 행 단위 전사 (2차 인용 · PDF 페이지 렌더로 대조)

### 9a. `Table 1` — 설계 전략과 전기화학 성능 (30 행)

| ref | 양극 조성 (질량비) | 설계 전략 | 가역용량 mAh g⁻¹ | 전류밀도 mA cm⁻² | 로딩 mg cm⁻² | 수명 | T °C |
|---|---|---|---|---|---|---|---|
| 100 | S/LBPSI/KB/Super P (3:5:1:1) | LBPSI redox-mediated two-phase reaction | 823 | 9.2 | 1.1 | 25000 | 25 |
| 101 | S/Li₆PS₅Cl/KB/C45 (22.75:50:12.25:15) | Halide segregation boosts interface | 1273 | 1.4 | 4 | 450 | 25 |
| 102 | S/Li₆PS₅Cl/NiNC/VGCF (3:4:2:1) | SAC catalyzes Li₂S₂ conversion | 674.9 | 3.35 | 1 | 850 | 30 |
| 103 | S/Li₆PS₅Cl@Li₃YBr₆-0.25/CNT (2.8:5:2.2) | LPSC@LYB core–shell enhanced conduction | 550 | 6.7 | 8 | 1000 | 30 |
| 104 | S/PDS/75Li₂S–25P₂S₅/KB (2.8:0.2:4:0.6) | Triphilic PDS interface-stabilized | 1100 | 0.96 | 1.6 | 400 | 30 |
| 105 | 75S-25CNT/Li₃YCl₅I/LiI (50:40:10) | Li₃YCl₅I catholyte anti-decomposition | 475.6 | 1.2 | 1.43 | 200 | 45 |
| 106 | 70S-30pOMS₂/Li₆PS₅Cl/C65/VGCF/CNT (40:40:8:8:4) | Nonconductive polar host | 1356 | NA | 0.2 | 500 | 25 |
| 107 | (LPO@30AB/60S)/Li₇P₃S₁₁ (3:2) | ALD LPO sulfur coating | 722 | 1.35 | 1.5 | 1000 | 30 |
| 108 | S/Li₇P₃S₁₁/AB/PPy@NCNT (38:38:19:5) | Elastic conduction network | 1344 | 1.51 | 4.5 | 250 | 30 |
| 26 | S/LPS/hCNC (39:40:21) | Hierarchical carbon nanocages | 1185 | 1.04 | 3 | 200 | 30 |
| 109 | MCS-S-Co/Li₁₀GeP₂S₁₂/CNT (2:2:1) | Solid interfacial catalysis | 1174 | 1.6 | 1 | 1400 | 25 |
| 24 | S/Co@AB/Li₇P₃S₁₁ (4:2:4) | Co–N₄ single-atom AB host | 721 | 1.25 | 1.5 | 1000 | 25 |
| 59 | S/Li₁₀GeP₂S₁₂/LiI/CNT (30:40:6:24) | Regulate cutoff potential to obtain Li₂S₂ | 1069 | 1.3 | 0.65 | 1500 | 25 |
| 110 | Li₂S/LiI/CR10/Li₆PS₅Br/VGCF (30:10:10:45:5) | Liquid-phase mixed-conductivity | 650 | 0.214 | 2 | 100 | 25 |
| 111 | S@BP2000/Li₇P₃S₁₁ (2:3) | Core–shell composite | 985.3 | 2.91 | 0.584 | 1200 | 25 |
| 112 | S/Li₆PS₅Cl/CNT (35:50:15) | Dual-phase LPSC pathway formation | 1166.7 | 1 | 6 | 150 | 30 |
| 22 | S:KB:MIEC (50:10:40) | MIEC-mediated sulfur two-phase reaction | 930 | 6.7 | 2 | 1000 | 60 |
| 113 | S@CNT/CNT/Li₅.₅PS₄.₅Cl₁.₅:PI₃ (50:8:37:5) | Mechanochemical in situ LPSI as redox mediator | 1142.2 | 1.675 | 2 | 2000 | 30 |
| 114 | S@CB/CB/SPEs/PVDF (80:10:5:5) | Self-healing electrolyte | 600 | 0.63 | 2 | 700 | 30 |
| 115 | 85Li₂S-15CuI/LPSCl/VGCF (50:40:10) | Cu⁺/I⁻ activate Li₂S kinetics | 588 | 2.33 | 1 | 6200 | 25 |
| 116 | 60Li₂S-40LiVS₂/Li₅.₅PS₄.₅Cl₁.₅ (1:1) | Interfacial solid redox mediation | 475 | 1 | 2 | 1000 | 25 |
| 117 | S@BP-2000/AB/PVDF (80:10:10) | PEO–PAN crosslinked adsorptive network | 1200 | 0.168 | NA | 75 | 70 |
| 118 | S/Super C65/Li₆PS₅Cl (34:17:49) | LixSi anode for dendrite suppression | 980 | 1.44 | 3 | 500 | 25 |
| 27 | 5Li₂S-4Li₆PS₅Cl-OMC/LPSC/AB (3:5:2) | 2D mesoporous triple-phase confinement | 675 | 2.97 | 1.27 | 300 | 60 |
| 119 | PPCF/S/Li₆PS₅Cl (10:40:50) | Surface-porous carbon fibers enable SE access | 1166 | 0.53 | 3.15 | 220 | 25 |
| 120 | LLTO-S/Super P/PEO-LiTFSI (2:1:1) | LLTO/C mixed-conduction double-phase | 850 | 0.268 | 0.8 | 100 | 55 |
| 121 | Li₂S@C/Li₇P₃S₁₁/AB (3:3:1) | Electrochemically in situ densified Li₂S–C | 692 | 2 | 1.75 | 700 | 60 |
| 122 | S₉.₃I/Li₃PS₄/VGCF (4:4:2) | Healable conductive S₉.₃I | 806 | 0.48 | 2.85 | 400 | 25 |
| 28 | 30CNG-70S/Li₅.₅PS₄.₅Cl₁.₅ (1:1) | CNG Li–N bond suppresses SE oxidation | 765 | 0.57 | 3.4 | 235 | 25 |
| 123 | CoNC@S/VGCF/Li₆PS₅Cl (35:15:50) | Single-atom metal–sulfur bond regulation | 1151 | 2.7 | 1 | 500 | 60 |

> (우리 산수) C-rate 역산(S 기준 1675 mAh g⁻¹): ref 100 = 5C · ref 22 = 2C · ref 113 = 0.5C · ref 59 ≈ 1.2C · ref 103 = 0.5C — 본문 서술과 맞는다. 단 **Li₂S 시작 양극(110 · 115 · 116 · 27 · 121)의 "mAh g⁻¹" 가 S 기준인지 Li₂S 기준인지 표가 말하지 않는다.** ref 113 은 표(2 mg cm⁻² · 2000 사이클)와 본문(6 mg cm⁻² · 5 mA cm⁻² · 1600 사이클 93.8 %)이 **다른 실험**을 인용한다.
> 우리 digest 대조: ref 22 행(S:KB:MIEC 50:10:40 · 2C · 2.025 mg cm⁻² · 1000 사이클 · 60 °C) = `wang2025_…` §3 과 일치.

### 9b. `Table 2` — 응용 지향 설계와 성능 (22 행 · **온도 열 없음**)

| ref | 양극 | 로딩 mg cm⁻² | 면적용량 mAh cm⁻² | SE | 두께 µm | 운전압 MPa | 용량 mAh g⁻¹ | 수명 |
|---|---|---|---|---|---|---|---|---|
| 177 | S | 8 | 9.2 | Li₆PS₅Cl | — | 30 | 1150 | 100 |
| 210 | S | 6 | — | Li₃PS₄–2LiBH₄ | 600 | 55 | 999.7 | — |
| 59 | S | 12 | 3 | Li₁₀GeP₂S₁₂ | 1000 | 150 | 250 | 50 |
| 211 | S | 21 | 34.9 | Li₆PS₅Cl–LiBH₄ | 492 | 40 | 1661 | 500 |
| 212 | S | 8.92 | 14 | Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃ | — | — | 1569.5 | **>20** (텍스트층 "420") |
| 213 | S | 15 | 20 | Li₆PS₅Cl | 135 | 2 | 1333 | — |
| 28 | S | 7.6 | 11.3 | Li₅.₅PS₄.₅Cl₁.₅ | — | 50 | 1486.8 | 40 |
| 214 | S | 10 | 10.4 | Li₁₀.₅₋ₓSi₁.₅P₁.₅S₁₂₋ₓIₓ | — | 81 | 1040 | 20 |
| 25 | Li₂S | 3.7 | 2.3 | PEO-LiTFSI | 10–20 | — | 622 | 15 |
| 215 | Li₂S | — | 0.005 | LiPON | 1.5 | — | — | 500 |
| 216 | S | 1.5 | — | Vr/PEO-LCSE | 10 | — | 1252 | 150 |
| 217 | Co₃S₄ | 6.37 | 3.37 | Li₆PS₅Cl | 35 | — | 529 | 100 |
| 218 | FeS₂ | 5 | 4.17 | Li₅.₈₂P₀.₉₄In₀.₀₆S₄.₇Cl₁.₁₂F₀.₁₈ + PIB | 35 | — | 834 | 100 |
| 219 | S | 0.9 | — | 54Li₃PS₄·46LiI | — | 5 | 1627 | 50 |
| 220 | S | 6.5 | 4.6 | Li₆PS₅Cl | — | 7 | 716 | 45 |
| 221 | S + WS₂ | 1.13 | — | Li₆PS₅Cl | — | 0.3 | 1005 | 50 |
| 222 | Li₂S | 5.83 | 4.66 | Li₆PS₅Cl | — | 10 | 800 | 350 |
| **223** | **Li₂S** | **4.36** | **4.7** | **Li₆PS₅Cl** | **50** | **10** | **1077** | **—** |
| 224 | FeS₂ | 2.22 | — | Li₆PS₅Cl | 90 | 15 | 615.8 | 500 |
| 225 | S | — | 4.2 | Li₆PS₅Cl | 60 | 0.005–0.01 | 1064 | — |
| 198 | S | 3.54 | — | Li₆PS₅Cl-XNBR | <50 | <1 | 484 | 50 |
| 226 | SPAN | 1–2 | — | PVDF-PU/LLZTO | 18 | — | 998.3 | 350 |

> (우리 산수) 세 값이 다 있는 13 행은 **로딩 × 용량 = 면적용량**이 전부 맞는다 ⇒ 용량은 **활물질 기준**이고, Li₂S 행(25 · 222 · 223)은 **Li₂S 기준**, S 행은 **S 기준**이다 — 같은 열에 기준이 섞였다. 예: 800 mAh g_Li₂S⁻¹ ≈ 1146 mAh g_S⁻¹ (Li₂S 의 S 질량분율 0.698).
> ⚠ ref 223(= li2s 원출처 Cronk)의 10 MPa 파우치는 **60 °C** 다 (우리 `cronk2026_…geometry_fem` §파우치 · 1077 mAh g⁻¹ 은 첫 사이클 · 사이클은 C/3 · 47 사이클 86.6 %). ref 28 의 11.3 mAh cm⁻² 도 리뷰 본문에 따르면 **60 °C**. 표에는 온도가 없다.
> ref 59 행은 SE 두께 1000 µm · 150 MPa — "응용 지향" 표에 비실용 구성이 들어 있다 (선정 기준 미기재).

---

## 10. 비판 ★

① **"탈리튬 장벽" 은 장벽이 아니다 — 범주 오류.** §4.1.2 는 흡착 Li₂S₂/Li₂S 의 **Li 추출에너지**(+3.78/+4.10 eV)가 벌크 Li₂S 의 **공공 형성에너지**(+5.75 eV)보다 낮다는 것으로 *"significantly reduced delithiation barrier"* 를 말하고, `Fig. 6b` 는 그 수를 "Transition State" 까지의 화살표로 그린다(`Fig. 1` 연대표도 "lowers … conversion barrier"). 홉 수 검산(300 K · ν₀ 10¹³ s⁻¹ 가정): 3.78 eV 면 Γ ≈ 3×10⁻⁵¹ s⁻¹ — 10 시간 충전 동안 N ≈ 10⁻⁴⁶ 회. 수 시간 안에 실제로 일어나는 반응이므로 **이 수들은 활성화 장벽일 수 없다.** 기준상태(고립 Li 원자인지 Li 금속인지)가 없는 열역학 추출에너지이고, 기준에 따라 Li 응집에너지만큼 통째로 움직인다. 같은 그림의 **0.42 eV** 는 본문에 정의가 없고, 원자 수가 다른 두 흡착계를 한 에너지축에 축척 없이 놓았다.

② **Cu⁺/I⁻ 의 "1.71 → 0.6 eV" 가 실험 수치와 차수에서 모순.** 1.11 eV 차의 아레니우스 비는 300 K 에서 **4.4×10¹⁸**(10^18.65)인데 같은 문단의 실험 D 는 *"~2 자릿수"* 증가다 — 16 자릿수 이상 어긋난다. 1.71 eV 면 맨 Li₂S 는 상온에서 홉이 사실상 없는데(Γ ≈ 1.9×10⁻¹⁶ s⁻¹ · 10 h 동안 N ≈ 7×10⁻¹²), 같은 리뷰 `Fig. 5a` 의 맨 Li₂S 는 `figure-read ≈` 8×10⁻⁹ S cm⁻¹ 로 측정된다. ⇒ 1.71 eV 가 무엇(공공 형성 포함 활성화? 특정 경로?)인지 리뷰가 안 밝힌다 — **원전(ref 115) 확인 전 인용 금지.**

③ **S 전자전도의 두 값이 12.8 자릿수 어긋난다.** §2.1 은 *"~10⁻³⁰ S cm⁻¹"*(ref 40), §4.1.1 은 S₉.₃I 가 *"11 자릿수 증가해 5.9×10⁻⁷"* — 즉 맨 S ≈ 5.9×10⁻¹⁸ 을 함의한다(우리 산수). 교과서 값과 측정 하한을 섞었다. 같은 절의 Cu⁺/I⁻ *"5–8 orders"* 도 자기 수치(9.44×10⁻¹⁴ → 10⁻⁸–10⁻⁶)로는 **5–7** 이다.

④ **ESW 서술 4곳이 축을 안 붙였다 — 그중 둘은 자기 그림·우리 데이터와 충돌.**
  (a) §4.3 *"할로겐(Cl)·Nb·O 도핑이 창을 넓힌다"*(refs 143–145): 층①(열역학 onset)로 읽으면 Cl 은 onset 을 옮기지 않는다(우리 comp1 = modelc 2.256 V · `[Zuo22]` CV 피크 동일). 층③(겉보기)이라면 별개 축이다. ✎ ref 144(Zhou … Nazar, *Nat. Energy* **7**, 83, 2022)는 우리 기억으로는 **염화물 SE** 논문이라 *"황화물에 Cl 도핑"* 근거로는 어긋난 인용일 수 있다 — **표지 미확인, 원전 확인 전 판정 보류.**
  (b) §4.4 Li–Al 이 *"LGPS 실용 안정창 안 → thermodynamically suppressing"*: 리뷰가 재수록한 `Fig. 11b` 에서 LiAl 은 **LUMO(1.7 V) 훨씬 아래**, 즉 열역학 창 밖이고 '실용창'(0.125–2.745 V) 안이다 — 억제는 **동역학·부동태(층③)** 이지 열역학이 아니다. 리뷰 본문이 자기 그림과 모순.
  (c) `Fig. 11b` 의 **"HOMO 2.1 V / LUMO 1.7 V"** 는 분해 전위(층①, = [Zhu15] LGPS 1.71–2.14)를 분자 오비탈 이름으로 부른 것 — 밴드엣지 ≠ 분해 onset (§B① 규율). 리뷰는 논평 없이 재수록.
  (d) §4.4 O 도입이 *"ESW 를 넓히고 전자 DOS 를 줄인다"*(ref 150): 갭(축 D)과 창(축 B)의 혼동 위험.

⑤ **표가 비교를 못 받친다.** `Table 2` 는 **온도 열이 없다** — ref 223(Cronk) 10 MPa 파우치는 60 °C(우리 digest), ref 28 의 11.3 mAh cm⁻² 도 60 °C(리뷰 본문). `Table 1`·`Table 2` 모두 **용량 기준**(S/Li₂S)·**음극 종류**·**전위 기준**이 없고(Li₂S 행은 Li₂S 기준 — §9b 산수), 선정 기준이 없어 SE 1000 µm · 150 MPa 행(ref 59)이 "응용 지향" 표에 들어 있다.

⑥ **"저압" 근거의 대부분이 Li–S 가 아니다.** `Fig. 17b` 는 NCM 셀(7.0 mAh cm⁻² · 1312 Wh L⁻¹ @2 MPa), `Fig. 17d` 는 본문 문맥상 Ni-rich 양극 full cell(2C 4500 사이클 — 그 용량은 `figure-read ≈` 75 mAh g⁻¹), §5.1 의 대표 수치는 LCO 100 mg cm⁻²·VL-LFP, §5.3.2 는 LTO·LCO/NCM·MOF/NCM811. §5.3 서두에 *"직접 검증이 아니다"* 라는 단서가 있지만 **그림 캡션과 `Fig. 18` 로드맵은 그 단서를 옮기지 않는다** — 그림만 보면 Li–S 성과로 읽힌다.

⑦ **그림–본문 어긋남 (실독으로 확인).** `Fig. 5b` 방전 끝 라벨이 *"Li₂S–LiI + LiI domain"* (본문: 고용체 복원) · `Fig. 6a` 범례 "Vacuum" (본문: bulk) · `Fig. 6e` 방전 칸이 *"✓ weak M–S"* (본문: 약한 M–S → 불완전 방전) · `Fig. 6b` 0.42 eV 미정의 · `Fig. 2b` 경사형 방전 곡선 (본문: 단일 평탄) · `Fig. 3` "L₂S" 오타 2회 · `Fig. 5c` 측정 온도 373 K 가 본문에 없음.

⑧ **"comparable bulk ionic conductivities" 가 자기 그림보다 강하다.** `Fig. 5a` 20 mol% 에서 LiI ≈2.2×10⁻⁶ vs LiBr ≈4.6×10⁻⁷ · LiCl ≈5.6×10⁻⁷ (`figure-read`, ≈4×). *"이용률을 σ 로 설명 못 한다"* 는 논증이 그만큼 약해진다.

⑨ **"typically <1400 mAh g⁻¹" 가 자기 표와 맞지 않는다.** `Table 2` 에 1486.8(28) · 1569.5(212) · 1627(219) · 1661(211) 행이 있고, 우리 `cronk2026_…` digest 는 1500–1694 mAh g_S⁻¹(CE 129 % = SE 용량 기여)다. "typically" 로 비켜 가지만, SE 기여를 빼고 비교하라는 자기 §3.3 경고를 표에 적용하지 않았다.

⑩ **li2s 관점의 공백 — Li₂S\|아지로다이트 화학을 다루지 않는다.** 본문에 `Li₇PS₆` 0회, "amorphous" 3회(카본블랙 · LPSI · Li–Ti–P–S)뿐, 가설 원출처 Cronk(ref 223)는 **표 2 한 행**. 550 °C 열처리(Han 2016, ref 142)나 고에너지 밀링(Cronk)처럼 Li₂S 와 LPSCl 이 반응할 수 있는 공정을 소개하면서 반응 여부를 묻지 않는다. §2.2 의 *"중간체 안정성이 SE 환경에 어떻게 의존하나"* 를 열린 질문으로 남긴 채 끝난다.

⑪ **Li₂S₂ "준안정" 논증이 hull 을 안 쓴다.** *"고체 형성에너지가 S₈ 보다 훨씬 낮다"* 는 S₈(원소 = 0)과의 비교라 무의미하다 — 준안정성은 S₈–Li₂S 연결선 대비 거리로 말해야 한다. 리뷰 자신의 `Fig. 6a` 수치로 그 거리는 bulk 에서 ≈+0.18 eV/atom(우리 산수) — "쉽게 접근 가능" 이라 부르기엔 크다. 반대로 LiI 위에서는 Li₂S₂ 가 hull 위로 올라온다(≈−0.26) — 리뷰는 이 역전을 말하지 않는다.

⑫ **2차 인용 DFT 의 방법 정보 0** (§4). 범함수·분산 보정·셀·기준상태가 하나도 없어 `Fig. 6c` 의 그래핀 위 양수 결합에너지(Se₈ ≈+0.33 eV) 같은 이상치를 판단할 수 없다.

⑬ **수치 바꿈 없는 요약 오류.** 비정질 Li–Ti–P–S MIEC σ_e *"10⁻⁴–10⁻² S cm⁻¹"* — 우리 `wang2025_…` digest 의 MIEC10(2.45×10⁻⁶)은 범위 밖이고, *"high ionic conductivity 유지"* 는 ~3×10⁻⁴ S cm⁻¹(유리 LPS 수준)이다.

⑭ **용어 부풀림.** `Fig. 6a` 캡션 "Gibbs free energy of formation" ↔ 축 "Energy of Formation"(0 K DFT) · Li₂S–AlI₃ 흡수단 ≈3.54 eV(우리 산수)를 *"semiconducting"* 으로.

⑮ **자기 인용·그림 선택.** 이름 일치 기준 ≈11편 · 재수록 패널 4개(`Fig. 8c`·`Fig. 13f–h`·`Fig. 13i,j`·`Fig. 17e`)가 저자 그룹 것이다. 리뷰로서 이례적인 양은 아니지만 `Fig. 17e`(DAI)·ref 196(PTFE 막) 같은 '저압·박막' 대표 사례가 자기 그룹이라는 점은 알고 읽는다.

⑯ **로드맵에 수치 목표가 없다.** `Fig. 18` 의 5 우선순위는 전부 정성이고, 수치 목표는 본문에 흩어진 두 개(S 로딩 >5 mg cm⁻² · 막 <30 µm)뿐 — E/S 비·N/P 비·셀 Wh kg⁻¹·운전압 목표가 없다.

---

## 11. 우리 연구 연결 (트랙별) ★★

### 11-(i) li2s — LPSCl@Li₂S 비정질 계면상 가설 (⚠ 외부 1저자 트랙 · 아래는 관찰/제안 · 판정 아님)

**가설** (`cronk2026_lis_cathode_interphase_chemistry` §0): *"LPSCl@Li₂S 볼밀 복합체의 계면에 중간 비정질상이 생겨 이온전도를 살린다."* 원출처 카드가 이미 갈라 둔 것 — *"이온전도를 살린다"* 는 Cronk 의 **S 양극** 서사에서 왔고, **Li₂S 양극**(우리 계)에 대해 Cronk 이 보인 것은 *"LPSCl 이 비정질 LPS-like 로 분해돼도 셀이 잘 돈다"* 까지다.

**우리 쪽 문장 — 허용 서술에서만** (`db/properties/lpscl_smallcell_glass_md_closed_2026_09_30.json` ① · 외부 1저자 회신 CN 확정):
> 「a-Li₄PS₄Cl 120 원자 유리 (독립 담금질 5 시드) 에서 465/550 K · 400 ps NVT MD 로 Li 확산을 쟀을 때, 사전등록 확산영역 게이트 (C1·C2 · 2σ) 를 두 온도 모두 통과한 시드는 없었다 (C2 통과 465 K 0/5 · 550 K 1/5). 400 K 는 800 ps 파일럿으로도 측정되지 않아 앞서 닫았다. 이 프로토콜(465/550 K · 400 ps · 5 시드)로는 사전등록 게이트를 만족하는 확산영역 데이터를 얻지 못했다. 따라서 이 유리의 Li 수송 계수와 활성화 에너지를 보고하지 않는다.」

⛔ *"이 유리는 465·550 K 에서 확산하지 않는다"* 로 읽지 않는다(금지 서술). 새 카드 v2(`lpscl_smallcell_glass_md_v2_estimand_2026_09_30.json`)는 **proposed · 잠정 · results_seen false** — 절대값·상온 전도도는 v2 에서도 안 낸다. LPSCl\|Li₂S 1층 계면상은 **닫힘**(`lpscl_li2s_layer1_closed_2026_09_15.json` · citable false): ⛔ *"볼밀에서 이 계면상이 만들어진다"* 를 이 리뷰로 받치지 않는다 — 리뷰는 그 계면을 다루지도 않는다(§10-⑩).

**⇒ 이 리뷰의 어떤 수송 수치도 우리 유리와 나란히 놓을 수 없다** (우리 쪽에 보고값이 없다).

| 리뷰 근거 (ref · 그림) | 가설에 대해 | 무게 | 왜 그 무게인가 |
|---|---|---|---|
| **S1. LPSI** (113 · `Fig. 7f,g`): PI₃ + S₈ + Li₅.₅PS₄.₅Cl₁.₅ 기계화학 → **비정질 Li–I–S–P 계면상**이 *"continuous Li⁺ transport pathways"* + 부피 완충 + redox | **방향 지지** — 기계화학으로 생긴 아지로다이트 유래 비정질 계면상이 Li⁺ 를 나른다는 *주장* 이 있다 | 약함–중간 | I 함유 · S 양극(Li₂S 아님) · 계면상 σ 수치가 리뷰에 없음 · 2차 인용 |
| **S2. LiI 코팅 + 2D EXSY** (127 · `Fig. 5c,d`): Li₂S\|LiI\|LPSCl 계면 교환 Ea 0.142/0.117 eV | **방향 지지 + 측정법** — Li₂S 와 LPSCl 사이 제3상이 계면 수송을 바꿀 수 있고, 그것을 **잴 수 있다** | 중간 | 계면상이 *의도한 LiI* 이지 LPSCl 유래 비정질상이 아님 · Ea 는 겉보기 교환값 |
| **S3. Li₂S–LiX 고용체** (125, 126 · `Fig. 5a,b`): LiX 로 Li₂S σ ≈10⁻⁸ → ≈10⁻⁶ S cm⁻¹ (`figure-read`) | **경쟁 기전** — 밀링 중 Cl 이 **Li₂S 쪽으로** 들어가도 이온전도가 오른다 | 중간 | 가설이 "비정질 LPSCl 유래 상" 과 "Cl-도핑 Li₂S" 를 가르지 않으면 같은 관측(σ↑)을 둘 다 설명한다 · 그런데 LiCl 계는 σ 가 비슷해도 이용률이 낮다(126) |
| **S4. Han 2016** (142 · `Fig. 8a,b`): Li₂S–LPSCl–C 나노복합 · 나노 3상 | 실물 접촉 사례 | 약함 | 550 °C 열처리 · HRTEM 이 계면상 판정 해상 아님 |
| **T1. 할라이드 편석** (101 · `Fig. 5e`): UHS 밀링이 아지로다이트에서 할라이드를 빼내 **LiX-rich** 나노 계면상 | **경쟁 가설** — 밀링 계면상이 '비정질 LPS-like' 가 아니라 LiX-rich 일 수 있다 | 중간–강함 | S/LPSCl/C(Li₂S 아님) · 2000 rpm 5 h(Cronk 500 rpm 1 h 와 다름) · LiX 계면상의 σ 는 리뷰에 없다 |
| **T2. 분해 산물 = 저항층** (§3.3 · refs 28, 35, 67, 68) | 가설의 *"이온전도를 살린다"* 와 **반대 방향의 일반론** | 중간 | 산화·환원 분해 일반론이지 Li₂S\|LPSCl 볼밀 계면 특정은 아님 — 다만 Cronk 의 Li₂S 복합 저주파 저항이 **밀링 1 h → 10 h** 에 1145 → 2675 Ω 로 늘어난 것(우리 digest · σ 미보고)과 같은 방향 |
| **T3. SE 가 redox 에 참여** (§3.3 · §4.3 · refs 58, 67, 146, 57) | 계면상이 **정적 이온전도체가 아니라 산화환원 활성**일 수 있다 → 보고량(σ)이 잘 정의되려면 **전위·SOC 를 선언**해야 한다 | 중간 | Cronk 도 Li₂S 셀에서 2 사이클부터 SSE-redox 숄더(우리 digest) |
| **T4. 공백** — Li₂S\|아지로다이트 반응성 미언급 (§10-⑩) | 지지도 위협도 아닌 **공백** — 이 리뷰로 가설을 받칠 수 없다 | — | 표 2 의 Cronk 행은 온도(60 °C) 누락 |
| **T5. Li₂S₂ 지속** (59, 60 · `Eq. 1`–`Eq. 2` · `Fig. 6a`) | Li₂S 계면에 Li₂S₂ 같은 중간체가 공존할 수 있다 → 계면 조성 정의가 더 복잡 | 약함 | Li₂S 시작(충전 출발) 양극에서의 의미는 리뷰가 다루지 않음 |

**리뷰가 묻지 않은 것 — 우리 원장의 유일한 수 (판정 아님)**: `lpscl_li2s_layer1_closed_2026_09_15.json` 허용 서술 「0층: Li₆PS₅Cl + Li₂S → Li₇PS₆ + LiCl, −38.4 meV/atom 은 **산술 힌트**다. hull 대조 잡이 불통과(E_above_hull 48.2 > 문턱 25)라 0층 결과를 판정으로 쓰지 않는다」. 그리고 `[Zhu15]`(우리 digest)가 적은 *"Li₆PS₅Cl 정렬 배열의 조성 평형 = Li₃PS₄ + Li₂S + LiCl (E_hull 83 meV/atom, 무질서 엔트로피를 근거로 0 처리)"* 은 Cronk 의 *"LPSCl → LPS-like"* 분해와 **같은 산물 목록**이다 — 리뷰는 이 둘 중 어느 연결도 하지 않는다. ⛔ 둘 다 가설의 근거로 올리지 않는다(외부 1저자 판단).

**외부 1저자에게 올릴 만한 관찰 (제안 · 편지 후보)**
1. 가설의 보고량이 *"계면상 σ"* 라면 **경쟁 기전 둘(T1 LiX-rich · S3 Cl-도핑 Li₂S)** 과 구분되는 관측 조건을 먼저 적어야 한다 — 같은 σ↑ 를 세 기전이 다 낸다.
2. 측정 쪽 짝은 **2D ⁶Li EXSY**(S2) — 상간 교환을 직접 센다. 계산 쪽 짝은 §11-(iii) L2.
3. 보고량에 **전위·SOC 선언**이 필요하다(T3) — SE 유래 상이 redox 활성이면 OCV 에서 잰 σ 와 사이클 중 σ 가 다른 양이다.

### 11-(ii) ESW — 리뷰의 분해 서술을 축 이름에 대응 (사용자 = 1저자)

| 리뷰 서술 (절 · ref) | 축 이름 | 우리 쪽 대응 | 판정 |
|---|---|---|---|
| §3.3 *"intrinsic ESW ≈1.7–2.1 V vs Li/Li⁺"* (20, 65, 66) | **B① · 층①** (열역학 분해 onset) — [Zhu15] LPSCl 1.71–2.01 · LGPS 1.71–2.14 재인용 | 산화 onset 2.256 V · 환원 가장자리 1.717 V (각각만 · ⛔ 폭 금지) | 같은 층·같은 화학 · 산화 쪽 0.246 V 원인 미확정 (⏩ 10-03 E2b: MP2020 황 음이온 보정으로 설명) |
| §3.3 Li–S 작동(방전 ~1.5–2.1 · 충전 컷오프 ~2.6–2.8 V) → *"분해 피하기 어렵다"* | **B①** (구동력 존재) + **B②** (양) | 충전 컷오프는 우리 2.256 V 위 · 방전 하한은 1.717 V 아래 (기준전극 확인 필요) | 방향 일치. "어렵다" 의 *양*은 B② — 우리 도구 밖 |
| §3.3 산화: P–S 절단 → S-rich · P 함유 저항 종 | **B① 사다리 화학** + B③(계면 저항) | 2.256 V (자유 S²⁻ → S) → 2.385 V (P₂S₇ + S) → 3.326 V (SCl) | **순서 같음** |
| §3.3 환원 (양극 안 전자망): Li₂S · Li₃P · LiCl | **층① 환원 가장자리 — 양극 내부** (Li–S 특유의 양면 노출) | 1.717 V · 산물 Li₃P + Li₂S + LiCl ([Zhu15]) · `sei_products` 역할 | 산물 같음. **NCM 양극에는 없는 축** — 우리 §B 에 이름이 없다 |
| §3.3 탄소 "electron leakage" | **B②** (속도·양 — 전자 접근) | 우리 계산 축 없음 (σ_e 축 부재 — §B `[Deng26PS]` 행과 같은 공백) | 우리 밖 |
| §3.3 · §4.3 SE 분해가 용량을 낸다 (58) · LPSCl 부분 가역 redox (67, `Fig. 10d`) · LPSCB (146) · Cr₂S₃ HEBM (57) | **B②** (양·가역성) — 화학은 **B①** 사다리 | 우리 onset 식의 산물 **S(와 Li₃PS₄)** 가 바로 *"전해질 유래 용량"* 의 재료 | 화학은 대응 · *얼마나·되돌아오나* 는 못 잰다 |
| §4.3 *"할로겐(Cl)·Nb·O 도핑이 창을 넓힌다"* (143–145) | 🔴 **축 미명명** | B①: Cl 증가는 onset 을 옮기지 않는다 (2.256 V · S²⁻-pin) | 층①이면 반대 · 층③이면 별개 → **축 붙이기 전 인용 금지** |
| §4.3 CNG Li⁺ 고정 (28 · `Fig. 10a,b`) | **B②** (속도 억제) · 기전 서술은 B① 순서 | 우리 *"자유 S²⁻ 3p 가 VBM — 먼저 산화"* 서사와 같은 방향 | 층① onset 을 옮기는 근거로 쓰지 않는다 |
| §4.3 pOMS 절연 호스트 (106 · `Fig. 10c`) | **B②** (전자 접근 차단) | `[Deng26PS]`·`[Qian26]` 와 같은 줄 | 방향 일치 |
| §4.3 Li₃YCl₅I 창 0.89–3.25 V (105) | 층 미기재 (할라이드) | 우리 계 아님 | 비교 안 함 |
| §4.4 O 도입 *"ESW 확대 · 전자 DOS 감소"* (150) | 🔴 **축 미명명 · 갭↔창 혼동 위험** | LPSOCl 갭 2.2309 vs comp1 2.066 eV 는 **축 D** — ESW 근거로 쓰지 않는다 | |
| `Fig. 11b` *"practical window 0.125–2.745 V"* + *"HOMO 2.1 / LUMO 1.7 V"* + 본문 *"thermodynamically suppressing"* (174) | **층③ 과 층① 혼용 + 오비탈 라벨** | §B① *"밴드엣지 ≠ 분해 onset"* | 🔴 리뷰 본문 오기 (§10-④) |
| §4.2 MIEC 전자전도 → 기생반응 | **B②** | `[Wang25MIEC]` MIEC30 퇴화 | 일치 |
| §4.3 끝 · §6 ② 분해 3분류 (비가역 / 자기제한 / 가역) | **B② · B③ 분류틀** | 우리: 산물의 전자 역할(`sei_products` insulator / marginal / conductor-LEAK)로 자기제한성을 *정성* 판정만 | ✅ **가져올 틀** |
| §6 ⑤ H₂S 관리 · 공기 안정 | **B④** (수분) | 가수분해 축 계산 0 (§B④) | — |

**🔑 이 digest 에서 ESW 트랙이 가져갈 핵심 한 줄 (리뷰가 말하지 않은 것).** `[Zhu15]`(Li₂S 2.00 ↔ LPSCl 2.01 V)와 `[Rich16]`(2.32 ↔ 2.32 V)이 두 독립 hull 에서 각각 보인 *"아지로다이트 산화 onset = Li₂S 산화 전위"* 관계(`comparison_vs_ours.md` §B① 행)를 Li–S 양극에 놓으면, **Li₂S → S 충전 반응과 SE 안 자유 S²⁻ 산화가 같은 전위에서 같은 화학으로 열린다.** ⇒ Li–S 양극에서 SE 의 redox 참여는 *"작동 전압이 좁은 창을 넘어서"* 가 아니라 **활물질 반응과 열역학적으로 겹쳐서**다. 리뷰의 "narrow window" 프레임은 이 점을 놓친다. 우리 onset 식(`Li₆PS₅Cl → Li₃PS₄ + LiCl + S + 2Li⁺ + 2e⁻`)이 내놓는 S 가 바로 SE 유래 용량의 재료다 — **B① 화학과 B② 양을 잇는 문장**. ⚠ 우리 hull 에서 그 관계가 성립하는지는 아직 안 쟀다(§11-iii E2).

**🔑 둘째 — 0.246 V 미해결이 Li–S 해석을 가른다.** ASSLSB 평탄 ~2.1 V(기준전극 확인 필요)는 우리 산화 onset 2.256 V **아래**, [Zhu15] 2.01 V **위**다. 어느 hull 을 믿느냐에 따라 *"평탄부 자체가 열역학적으로 SE 를 산화시키나"* 가 갈린다. 산화 쪽 0.246 V 의 원인(제외 상 ≈0.116 V + MP 판본 후보)이 미확정인 상태에서는 **둘 다 쓰지 않는다.** ⏩ **10-03 E2b**: 원인이 확인됐다 — MP2020 황 음이온 보정이 Li₂S 산화 전위를 0.252 V 올린다 (보정 끈 진단값이 [Zhu15] 2.00 V 와 0.01 V 안). 보정은 실험 생성엔탈피에 맞춘 것이라 우리 기준계 값은 2.256 V 쪽이다. 다만 ASSLSB 평탄과의 대조는 기준전극(Li–In)과 실측 평형 전위를 확인한 뒤에 쓴다 (`esw_e2b_li2s_correction_2026_10_03.json`).

### 11-(iii) 계산 아이디어 후보 (아이디어만 · '할 것' 아님 · 비용 감각 포함)

> 자원 제약: 큰 계산은 **GPU 한 장** (gabia A6000 48 GB · kgy 3090 24 GB 공유) · KISTI 종료. GPU 점유 현황은 최신 런북·`kb/open_items.md` ⏭ 절로 확인하고(gabia 는 GPU pw.x ↔ UMA 공존 금지 · 예외는 결정 원장에서만), **새 GPU 잡은 결정이 먼저다.** MP·pymatgen 은 gabia `uma` env(mp_api 있음) · MP REST 는 UA 헤더 필요(403 함정).

| # | 트랙 | 무엇 | 비용 | 걸림돌 |
|---|---|---|---|---|
| **E1** | ESW | **Li–S 작동창 × 우리 층① 사다리 겹침 그림** — 기존 `esw_lis4excluded.json` 단계(1.717 · 2.256 · 2.385 · 3.326 V)를 S/Li₂S 작동 전위(방전·충전 컷오프)와 한 축에 | DFT 0 · 플롯만 | ⛔ 창 폭 인쇄 금지(가장자리만) · 전위 기준(Li–In +0.62 V) 명시 |
| **E2** | ESW | **같은 hull · 같은 상 집합(LiS₄ 제외 GG set)에서 Li₂S → S + 2Li 전압** 계산 — `[Zhu15]`·`[Rich16]` 의 *"onset = Li₂S 산화 전위"* 가 우리 hull 에서도 성립하나 + 0.246 V 중 MP 판본 몫이 Li–S 이원계 에너지에서 오는지 한 번에 진단 | CPU 수 분 (pymatgen) | 결과가 0.246 V 의 원인을 바꾸면 원장(`HZ-esw-reduction-limit-label` 의 '원인 미확정' 문구) 갱신 필요 — 1저자 결정 |
| **E3** | ESW | **LPSCl\|S₈ 의사이원 반응성** (`InterfacialReactivity`) = B③ 의 Li–S 판 | CPU 수 분 | S-rich 티오인산염(Cronk 의 Li₃PS₄₊ₙ)이 MP 에 없으면 결과가 제한된다 · ⚠ LPSCl\|**Li₂S** 쪽은 li2s 트랙 — 이 줄에 넣지 않는다 |
| **E4** | ESW | **자유 S²⁻(4a/4d) 인접 vs PS₄ 인접 Li 공공 형성에너지** — ref 28 기전(첫 탈리튬 = 자유 S²⁻ 산화 개시)의 원자 수준 판 | QE-GPU 소셀 · ≈1–2 GPU-일 | 보고량 카드 먼저(기준상태 · 무질서 배열 선택 규칙 · admissible state 여럿이면 집계 규칙) |
| **L1** | li2s (제안) | **할로겐이 어디로 가나** — Li₂S + LPSCl (x = 0.778) 후보 산물 비교: Cl-도핑 Li₂S vs 비정질 LPS-like + LiCl vs Li₇PS₆ + LiCl | CPU 수 분 (0 K hull) | ⛔ 1층 마감의 0층 hull 대조 잡 불통과 — 새 hull 주장은 **새 카드 + 외부 1저자** |
| **L2** | li2s (제안) | **EXSY 아날로그 보고량** — Li₂S \| 계면상 \| LPSCl 셀의 MLIP-MD 에서 상간 Li 교환 횟수 세기 | UMA 120 원자 ≈1.5–2 GB VRAM · 런당 싸다 | 병목은 **모델 검증(G1)** — 400 원자 DFT 는 48 GB 에서 OOM 실측(1층 마감) → DFT 로 대조 가능한 크기(≈120 원자)로 설계 · 외부 1저자 규칙 |
| **L3** | li2s (제안) | **LPSCl 표면 위 Li₂S₂ / Li₂S 형성에너지** (`Fig. 6a` 의 LiI(100) 를 LPSCl 로) — *"아지로다이트 표면이 Li₂S₂ 를 hull 위로 올리나"* | QE-GPU 슬랩 · 수 GPU-일 | 슬랩을 48 GB 안에 맞춰야 한다(6층 SE 슬랩 추정 50–56 GB 로 W_ad 예외가 철회된 선례) · **기준상태(벌크/흡착 · Li 기준)를 카드에서 먼저 선언** — 리뷰가 안 한 바로 그것 |

### 11-(iv) 인용하면 안 되는 것 (이 리뷰에서)

1. `Fig. 6b` · §4.1.2 의 **3.78 / 4.10 / 5.75 eV 를 장벽으로** — 홉 수 검산으로 불가능(§10-①). 쓰려면 *"기준상태 미기재 Li 추출에너지(2차 인용 · ref 59)"* 로만.
2. **Cu⁺/I⁻ 의 Li⁺ 이동장벽 1.71 → 0.6 eV** — 같은 문단 실험과 18.6 자릿수 모순(§10-②) · 원전 확인 전 금지.
3. **S 전자전도 ~10⁻³⁰ 와 "11 자릿수 → 5.9×10⁻⁷" 를 한 문장에** (§10-③) · Cu⁺/I⁻ *"5–8 orders"* (→ 5–7).
4. *"황화물 ESW 1.7–2.1 V"* 를 **실험 창**으로 — 층① 계산값([Zhu15])의 재인용이다.
5. *"Cl 도핑이 창을 넓힌다"* · *"O 도입이 창을 넓히고 DOS 를 줄인다"* — **축 없이** (§10-④).
6. *"Li–Al 이 열역학적으로 환원을 억제한다"* · `Fig. 11b` 의 **HOMO/LUMO 라벨** (§10-④).
7. `Table 2` 행을 **온도 없이** 비교 (ref 223 · ref 28 = 60 °C) · `Table 1`·`Table 2` 의 "mAh g⁻¹" 를 **기준(S/Li₂S) 없이** 비교.
8. `Fig. 17` · §5.1 · §5.3.2 의 저압·후막 수치를 **Li–S 성과로** (NCM · LCO · LFP · LTO 셀).
9. *"Li₂S–LiCl/Br/I 의 σ 는 comparable"* — `figure-read` 로 LiI ≈4× (§10-⑧).
10. EXSY 계면 Ea **0.142 / 0.117 eV 를 단일 홉 장벽처럼** 우리 NEB·MD 장벽과 나란히.
11. *"Li₂S₂ 는 열역학적으로 쉽게 접근 가능한 준안정 중간체"* — hull 기준 아님 (§10-⑪).
12. **우리 쪽**: li2s 유리의 σ·D·Ea(어떤 형태로도 — 마감 금지 서술) · Li₂S NEB(`HZ-sei-neb-retracted` BLOCKED) · 우리 ESW **창 폭**(`HZ-esw-reduction-limit-label`) · 점착 W 값(어디에도 숫자로 싣지 않는다).
13. **이 리뷰의 인용번호를 원전 재확인 없이** — 특히 ref 144(✎ 염화물 SE 논문일 수 있음) · `Fig. 10f` 캡션의 ref 57 은 "Copyright 2025" 인데 참고문헌은 2024.

### 11-(v) 기타 트랙 메모 (배경만)

- **점착(W_ad) · 사용자**: Ag–C 인터레이어 문헌 두 편(ref 166 Oh 2022 *ACS Energy Lett.* — ~5 µm Ag–C 무음극 · ref 176 Chen 2022 — 80LiB + Ag@C)과 Ji 의 *"Li 대비 높은 계면에너지"* 설계 기준(ref 171)이 2차 인용으로 나온다. **수치 없음** — 계획서의 실측 앵커 목록에 원전 확인 대상으로만.
- **DEM**: Damköhler 수(ref 19 · *Nat. Chem. Eng.* 2024)를 TPB 밀도 vs 퍼콜레이션 논의의 무차원 서술자 후보로 · 후막 경사 설계(refs 180, 181)는 Li–S 가 아니다. ⇒ `comparison_vs_ours_DEM.md` 반영은 부모 판단.
- **CEI (외부 실험 1저자)**: §6 ② 의 *"좋은 계면상 = Li⁺ 전도 · 전자 차단 · 구조 유지 · 소모 정지"* 4칸 — `[WangZeierYou25]`(§J-23) CEI 요구 4칸과 같은 틀 · Nd 언급 없음.
- **음극 (§E)**: *"Li₃P 의 전자전도 → 자기제한 실패"*(refs 72, 80)가 우리 `sei_products` 역할 분류(Li₃P conductor-LEAK)와 같은 방향 — `[Xiao20Rev]` 의 passivating 서술과 문헌끼리 갈리는 자리에 **한 목소리 추가**(2차 인용).
- **이온전도 (§A)**: ref 196 의 **Li₅.₄PS₄.₄Cl₁.₆**(= 우리 modelc 화학량) 건식 30 µm 막 σ 8.4 mS cm⁻¹ — 2차 인용이고 원전 확인 전에는 §A 행을 만들지 않는다. 확인하면 *"modelc 조성의 실측 σ (막 형태)"* 후보.
- **기계 (§C)**: *"황화물·할라이드 ≈10–30 GPa"* 는 출처 없는 띠 — 우리 E_VRH 가 띠 안이라는 정도만.

---

## 12. 원전 대조 — 이미 digest 한 것 / 꼭 읽어야 할 빠진 원전

### 12a. 리뷰가 인용했고 우리가 이미 digest 한 것

| ref | 원전 | 우리 slug | 이 리뷰의 쓰임 |
|---|---|---|---|
| 20 | Zhu, He, Mo, *ACS AMI* **7**, 23685 (2015) | `zhu2015_esw_grand_potential_origin` | §3.3 ESW 1.7–2.1 V 의 출처 |
| 22 | D. Wang … D. Wang, *Nat. Mater.* **24**, 243 (2025) | `wang2025_miec_tis2_lps_three_phase_interface_lis_assb` | §4.2 MIEC · `Fig. 9b` · `Table 1` |
| 66 | Xiao … Ceder, *Nat. Rev. Mater.* **5**, 105 (2020) | `xiao2020_interface_stability_ssb_review` | §3.3 ESW |
| 82 | Schwietert … Wagemaker, *Nat. Mater.* **19**, 428 (2020) | `schwietert2020_redox_activity_vs_electrochemical_stability` | §3.4 Li₁₁PS₅Cl 중간체 |
| 85 | Doux … Meng, *Adv. Energy Mater.* **10**, 1903253 (2020) | `doux2020_stack_pressure_assb` | §3.4 · §3.5 스택압 |
| 223 | Cronk … Meng, *Nat. Commun.* **17**, 3298 (2026) | `cronk2026_lis_cathode_interphase_chemistry` (+ `…_geometry_fem`) | **`Table 2` 한 행뿐** (본문 0회 · 온도 누락) |

### 12b. 꼭 읽어야 할 빠진 원전 (트랙 · 우선순위 순)

| 우선 | ref | 원전 (리뷰 참고문헌 표기) | 트랙 | 왜 |
|---|---|---|---|---|
| 1 | 113 | M. Wang, H. Su, F. Zhao, Y. Zhong, X. Wang, C. Gu, J. Tu, *Adv. Mater.* **38**, e13336 (2026) | li2s | **기계화학 비정질 아지로다이트 유래 계면상**(LPSI)의 최근접 사례 — 계면상 조성·σ·생성 조건을 원전에서 확인 (S1) |
| 2 | 101 | J. Lee … K. Amine, G.-L. Xu, *Science* **388**, 724 (2025) | li2s | **경쟁 가설**(할라이드 편석 LiX-rich 계면상) — 밀링 조건·계면상 정체·σ (T1) |
| 3 | 127 | M. Liu … M. Wagemaker, *Nat. Commun.* **12**, 5943 (2021) | li2s | Li₂S\|LiI\|LPSCl **2D EXSY** — 계면상 수송을 재는 법 · Ea 의 정의(단일 홉인가 겉보기인가) (S2) |
| 4 | 18 | M. L. Holekevi Chandrappa, J. Qi, C. Chen, S. Banerjee, S. P. Ong, *JACS* **144**, 18009 (2022) — "Thermodynamics and Kinetics of the Cathode–Electrolyte Interface in All-Solid-State Li–S Batteries" | li2s · 방법 | Li–S 양극\|SE 계면의 **MLIP(MTP + 능동학습) 원자 모델** — 우리 `wu2026_ml_driven_electrolyte_interface_design_review` 표에 *"S₈\|β-Li₃PS₄ · >1000 원자"* 로, `kim2026_li_argyrodite_sei_reactive_md` 에 계보로만 등장 · **litdb 미 digest**. li2s MLIP-MD 프로토콜의 가장 가까운 외부 대조 |
| 5 | 28 | Z. Yu, B. Singh, Y. Yu, L. F. Nazar, *Nat. Mater.* **24**, 1082 (2025) | ESW | Li₅.₅PS₄.₅Cl₁.₅(우리 modelc 계열)의 **자유 S²⁻ 분포 · 첫 탈리튬 · P₂S₇⁴⁻** — 우리 사다리 2단 종과 대조 (§7) |
| 6 | 58 | S. Ohno, C. Rosenbach, G. F. Dewald, J. Janek, W. G. Zeier, *Adv. Funct. Mater.* **31**, 2010620 (2021) | ESW | SE redox 의 **용량 기여** 정량 — B② 의 외부 앵커 |
| 7 | 67 | D. H. S. Tan … Y. S. Meng, *ACS Energy Lett.* **4**, 2418 (2019) | ESW | `Fig. 10d` LPSCl 산화환원 경로 원전 — 우리 B① 사다리 화학의 실험 짝 (`[Zuo22]` digest 가 2차로만 언급) |
| 8 | 59 | J. T. Kim … X. Sun, *Nat. Commun.* **14**, 6404 (2023) | li2s · 계산 감사 | 3.78/4.10/5.75 eV 의 **기준상태** 확인 · Li₂S₂ 실험 근거 · `Fig. 6a` hull 역전 |
| 9 | 115 | J. Gao … J. Wu, *Small* **20**, 2404171 (2024) | 계산 감사 | 1.71 → 0.6 eV 가 무엇인지 (§10-②) |
| 10 | 142 | F. Han … C. Wang, *Nano Lett.* **16**, 4521 (2016) | li2s | Li₂S–LPSCl–C 550 °C — 반응 여부를 원전이 봤나 |
| 11 | 222 | J. Park … Y. S. Meng, *Adv. Energy Mater.* **16**, e04272 (2026) | li2s | Li₂S + LPSCl 양극 @10 MPa (`Table 2`: 5.83 mg cm⁻² · 800 mAh g⁻¹ · 350 사이클) — Cronk 와 같은 Meng 그룹(저자 이름 일치)의 Li₂S 양극 편 |
| 12 | 125 · 126 | Hakari 2017 *Adv. Sustainable Syst.* · Fujita 2022 *ACS Appl. Energy Mater.* | li2s | Li₂S–LiX 고용체 σ 와 LiI 도메인 (S3) |
| 13 | 174 | H. Pan … H. Zhou, *Sci. Adv.* **8**, eabn4372 (2022) | ESW | `Fig. 11b` "practical window" 정의 원전 |
| 14 | 144 | L. Zhou, T.-T. Zuo, … J. Janek, L. Nazar, *Nat. Energy* **7**, 83 (2022) | ESW | §10-④(a) 인용 적합성 확인 |
| 15 | 19 | J. T. Kim … Y. Li, *Nat. Chem. Eng.* **1**, 400 (2024) | DEM | Damköhler 수 원전 |

---

## 13. 인용 가능 문장 (영문 초안)

- (ESW · 사용자 트랙) "Reviews of all-solid-state Li–S batteries commonly quote the intrinsic electrochemical window of sulfide electrolytes as ≈1.7–2.1 V vs Li/Li⁺ (e.g., Wu et al., *Chem. Soc. Rev.* 2026); this is a thermodynamic decomposition-onset window derived from grand-potential phase diagrams (Zhu et al., 2015), not an experimentally measured window."
- (ESW) "Because the oxidation onset of argyrodite electrolytes coincides with the oxidation potential of Li₂S in independent hull constructions (Zhu et al. 2015; Richards et al. 2016), electrolyte participation in the redox of Li–S composite cathodes is thermodynamically co-incident with the active-material reaction rather than an excursion beyond a narrow window." ⚠ 우리 hull 에서의 확인(§11-iii E2) 전에는 문헌 귀속으로만.
- (ESW) "Halogen enrichment does not shift the thermodynamic oxidation onset of argyrodites (S²⁻-limited); statements that Cl doping 'widens the electrochemical window' must specify whether the thermodynamic onset or the apparent, kinetically limited window is meant."
- (계산 감사) "Lithium-extraction energies of 3.8–5.8 eV reported for adsorbed Li₂S₂/Li₂S and bulk Li₂S are thermodynamic quantities with an unstated reference state; read as activation barriers they would imply rates of ~10⁻⁵¹ s⁻¹ at 300 K and cannot describe a charging reaction that proceeds within hours."
- (li2s 트랙 — ⚠ 외부 1저자 판단 전 사용 금지) "Current reviews do not address the chemical compatibility of Li₂S with argyrodite catholytes; the closest reported analogues are a mechanochemically formed amorphous Li–I–S–P interphase and halide-segregated LiX-rich interphases formed during high-speed mixing."

---

## 14. 주의 / 한계 (인용 규율)

- ⛔ **모든 수치는 2차 인용** — `(2차 인용 · ref N)` 을 붙이고, 원전을 digest 했으면 그 digest 를 인용한다(§12a).
- ⛔ **A–D 물성 4축에 이 리뷰로 행을 만들지 않는다** (자체 계산·실험 0).
- ⛔ 전위 기준 혼재 — ESW 는 vs Li/Li⁺ 로 적혔지만 Li–S 작동 전압은 기준 미기재(Li–In 이면 +0.62 V).
- ⛔ `Table 2` 는 온도 없음 · `Table 1`·`Table 2` 의 용량 기준 혼재 · 텍스트층 기호 손실(">20" → "420", ">5" → "45").
- ⛔ `figure-read` 값(`Fig. 5a` · `Fig. 6a,c` · `Fig. 17b,d`)은 재수록 그림의 재판독 — 원전 값이 아니다(±0.1 decade / ±0.05 eV 급).
- ⚠ (우리 산수) — `Fig. 6a` hull 거리 · C-rate 역산 · Li₂S 기준 환산 · UV-Vis 광자에너지 · 아레니우스 비 · 홉 수 검산은 **차수·정합 검산**이지 물성값이 아니다.
- ⚠ li2s 관련 줄은 전부 **관찰/제안** — 외부 1저자 트랙. 우리 캠페인 문장은 마감 원장 허용 서술(①, 1층 마감 0층 문장)만 옮겼다.
- ⚠ ✎ 표시(ref 144 성격)는 기억 기반 — 표지 확인 전 판정 보류.
- ⚠ 미실독 그림(`Fig. 12`–`Fig. 16`)의 내용은 캡션 기준이다.

---

## 15. 기법 용어 미니사전

- **ASSLSB**: all-solid-state lithium–sulfur battery. 양극 S(또는 Li₂S) + SE + 탄소, 음극 Li(또는 합금).
- **TPB (triple-phase boundary, 3상계면)**: 활물질 · Li⁺ 전도체(SE) · 전자 전도체(탄소)가 동시에 만나는 곳. 고체 Li–S 반응이 일어날 수 있는 *최소 단위*.
- **MIEC (mixed ionic–electronic conductor)**: Li⁺ 와 전자를 함께 나르는 상. S 와 닿기만 하면 3상점 없이 **2상 계면**에서 반응이 된다. 대가는 SE 분해 가속.
- **Damköhler 수 (Da)**: 고유 반응속도 / 물질수송 속도. Da > 1 이면 수송이 병목 → 바깥부터 반응하는 코어–셸이 생긴다.
- **Gibbs 상률과 평탄**: 2상이 평형이면 조성 자유도가 없어 전압이 일정 → 평탄 하나 = 2상 평형 하나. 액체 Li–S 의 두 평탄 = 두 2상 영역.
- **Li₂S₂**: S₈ 와 Li₂S 사이의 짧은 사슬 중간체. 고체에서는 갇힌 채 방전 끝까지 남을 수 있다는 것이 2023 년 증거.
- **Redox mediator (RM)**: 산화상태가 바뀌며 떨어진 두 지점 사이에서 전하를 나르는 분자·이온·상. 고체에서는 움직이지 못해 범위가 짧다. "진짜 가역 매개" 와 "희생 분해 용량" 을 구분해야 한다.
- **SAC (single-atom catalyst)**: 탄소에 원자 하나씩 박힌 금속(M–N₄). 서술자 = M 3d–S 3p 혼성(M–S 결합 세기) — 너무 약하면 활성화 실패, 너무 강하면 피독.
- **dsp² / d²sp³**: 사각평면 / 팔면체 배위의 혼성 궤도 표기. NiNC 에서 Li₂S₂ 가 붙으면 Ni 가 전자적으로 활성인 d²sp³ 로 바뀐다는 주장.
- **2D EXSY NMR**: 혼합 시간(Tmix) 동안 서로 다른 화학 환경의 Li 가 자리를 바꾸면 대각선 밖에 교차 피크가 생긴다. 온도를 바꿔 교환 속도의 겉보기 활성화에너지를 얻는다 — **단일 홉 장벽과는 다른 양**.
- **HAADF-STEM + EDS**: 원자번호 대비 영상 + 원소 지도. 입자 테두리의 Cl 농축 같은 나노 편석을 본다.
- **UHS / HEBM**: ultrahigh-speed mixing / high-energy ball milling — 기계화학 반응(분해·편석·비정질화)을 일으킬 만큼 센 혼합.
- **Li 추출에너지 vs 활성화 장벽**: 앞의 것은 처음과 끝 상태의 에너지 차(열역학 · 기준상태에 의존), 뒤의 것은 그 사이 고개의 높이(동역학). 3–6 eV 를 장벽으로 읽으면 상온 반응이 영원히 안 일어난다 — 홉 수 검산이 그 차이를 잡는다.
- **층① / 층② / 층③ 창**: 열역학 분해 onset / 골격 유지 탈리튬화(intrinsic) / 겉보기(실용 · 동역학·부동태 포함). `Fig. 11b` 의 "practical stability window" 는 층③, "HOMO/LUMO" 로 이름 붙은 1.7–2.1 V 는 층①.
- **CCD (critical current density)**: 덴드라이트 단락 없이 버티는 최대 전류밀도. **임계 탈리 전류밀도**는 크리프가 탈리의 부피 손실을 못 메워 공극이 쌓이기 시작하는 전류밀도.
- **DAI (dynamically adaptive interphase)**: 탈리 중 전기장에 끌려온 I⁻ 가 Li 계면에 LiI-rich 층을 계속 다시 만들어 공극을 메우는 계면상.
- **N/P 비**: 음극 용량 / 양극 용량. 1 에 가까울수록 과잉 Li 가 적어 셀 에너지밀도가 높다.
- **VIGLAS / Tg**: 점탄성 무기 유리 전해질 / 유리전이 온도. Tg 가 상온 아래면 상온에서 크리프로 흘러 계면을 메운다.
