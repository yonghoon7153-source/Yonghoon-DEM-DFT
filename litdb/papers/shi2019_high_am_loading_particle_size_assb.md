<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목 -->
# 입자 크기비 λ=D_CAM/D_SE 로 고-CAM 로딩(>50 vol%) 달성 — 우리와 *같은 LIGGGHTS DEM + Hertz* 로 "작은 SE + 큰 CAM"을 모델+실험 동시 증명 — Shi (Ceder 그룹, Adv. Energy Mater. 2019/2020)

> slug `shi2019_high_am_loading_particle_size_assb` · DOI `10.1002/aenm.201902881` · type `mixed (DEM-LIGGGHTS modeling + experiment)` · PDF `Shi_2019_AdvEnergyMater_HighActiveMaterialLoading_ASSB_ParticleEngineering.pdf` · SI `aenm201902881-sup-0001-suppmat.pdf` · digested `2026-06-26` · SI 보강 `2026-09-26` · status ✅
>
> ⛔⛔ **SI 보강 2026-09-26 — 2026-06-26 digest 는 본문 9 쪽만 읽었다.** §3·§7·A.1 이 "Table S3" 를 근거로 들면서 **값은 하나도
> 옮기지 않았다** (원장 `SELF-51` 이 cronau2022 카드에서 "`[20]` 의 40 h · 1/3 은 카드에 없다 → `[미확인]`" 으로 걸었던 자리).
> SI 8 쪽 (Hertz 힘 식 · Table 1 · Table S2 · Fig. S1 · Fig. S2 · Table S3) 전수를 **§S** 에 정리했고, 본문 재대조로 드러난 오기는
> 그 자리에 ⛔ 표지로 고쳤다 (원 문장은 이력으로 남김). 요지:
> - ★ **SELF-51 판정 — "40 h → 1/3" 은 있다. 그러나 입경 축의 값이 아니다.** SI Table S3 (SI p.6): LPS **유리**(75Li₂S–25P₂S₅) 습식
>   밀링 4 시료 — 8 µm (SPEX 8000M · 5 mm · heptane · 0.5 h) **0.32** · 5 µm (SPEX · 3 mm · heptane · 1.5 h) **0.24** · 3 µm (PM200 · 3+1 mm ·
>   heptane+dibutyl ether · 15 h) **0.22** · 1.5 µm (PM200 · 1 mm · heptane+DBE · **40 h**) **0.14 mS/cm** (SI-stated, In 차단전극 EIS).
>   기준 = 밀링 전 bulk LPS **0.39** (본문 p.3) → **0.14 / 0.39 = 0.36 ≈ 1/3** (derived(ours)) ⇒ Cronau 2022 p.2 *"LWM exceeding 40 h … about 1/3"*
>   `[20,25]` 의 1차 근거가 이 표다 (`[25]` Minnmann 2021 은 10 h ×0.75 — 정본 카드). **그러나** ① 그 점의 입경은 **d̄ ≈ 1.5 µm (r ≈ 0.75 µm)** —
>   우리 `Cronau(r_SE)` 가 0.33 을 둔 **r ≤ 30 nm 와 25 배 다르고**, 우리 계수는 r = 0.75 µm 에서 **1.00** 이다 ② 입경·밀링 시간·밀·볼·용매가
>   **함께** 바뀐 4 점이라 입경 효과를 떼어낼 수 없다 ③ 재료가 **처음부터 비정질인 LPS 유리** 라 "비정질화" 기전이 설 자리가 없고, 저자
>   귀속은 *"likely because of the increased grain boundary (or particle boundary) resistance, which can be worsened by any residual solvent"*
>   (p.3) 이다 ⇒ **Shi 표는 `Cronau(r_SE)` 의 0.33 · r ≤ 30 nm 배치의 출처가 될 수 없다** (§S.4).
> - **DEM 파라미터 (SI "Table 1")**: E_SE **18.5** / E_AM **177.5 GPa** · ν 0.3/0.3 · ρ 1.87/4.85 g cm⁻³ · γ_t 50/25 ("GPa", 원문 표기) ·
>   σ_y **2 / 12.6 GPa** ⇒ §3·§4 의 *"E·ν·μ 본문 수치 미보고 = n/a"* 철회 (SI 에 있다; **μ 는 표에 없다**). E_SE 18.5 = **무연화**.
>   "σ_y" 는 실제로는 **나노압입 경도** — AM 177.5 / 12.6 은 정본 `xu2017_…` 의 **소결 NMC532 펠릿 E · H** 와 소수점까지 같다 (Shi 는 `[2]` EML 2016 에 귀속 —
>   오귀속 공산) · 힘 식에 σ_y 항이 없어 결과엔 무관 (§S.1).
> - **압밀 프로토콜**: *"Pressure was then held constant until the system reaches static equilibrium"* (p.2) = **정압 유지** — 카드의
>   *"200 MPa 도달 → 정지 (= 우리 hold)"* 는 틀렸다 (우리 hold = 변위정지).
> - **수치 오기**: θ 16 → 20 % 는 **85 wt%** (카드 80 wt%) · Fig 5b "λ 2.5 · SE 2 µm" 는 **위 축 눈금**을 데이터로 읽은 것 (점 = SE 1.5/3/5/8 µm) ·
>   Fig 5e 의 12 µm 값이 SE 크기끼리 뒤바뀜 · Fig 6 "60·70 wt% 둘 다 > 150" 은 **1.5 µm LPS 만** · Fig S2 는 **60 wt%** · λ_min(80 wt%)
>   "≈ 3–8" → 판독 θ 80 % ≈ 3.9 · 90 % ≈ 5.9 · 98 % > 8 · "θ 는 로딩보다 λ 에 훨씬 민감" → 원문 *"depends as much on the cathode volume
>   fraction as on … λ"*. 판독값 전부 `litdb/figures/shi2019_high_am_loading_particle_size_assb/digitized.csv` (`tools/litdb/shi2019_fig_digitize.py`).

> ★ **우리 "size = PACKING" 스토리의 핵심 frame[4] 앵커 + DEM 방법론 *형제*.** 이 논문은 (i) **우리와 똑같은
> LIGGGHTS DEM + Hertz 접촉**으로 cold-press 양극을 압밀하고, (ii) **NMC(NCM) + LPS**(우리 NMC811+LPSCl 에 가장
> 가까운 소재계)에서, (iii) **단 하나의 지배변수 = 크기비 λ = D̄_CAM/D̄_SE** 가 cathode utilization(=활성 CAM 분율)을
> 결정함을 *모델로 예측하고 실험으로 검증*한다. 결론: **"SE 를 CAM 보다 작게(λ↑)"** 하면 고-CAM 로딩(>80 wt% / >50 vol%)에서도
> 거의 full 용량 → 우리 Furnas-dip·12:4:1·bimodal·production-core(AM 70–85 wt%) 의 *직접 실험-모델 증거*. ⚠ 단 그들 DEM 은
> 우리처럼 **rigid-sphere + Hertz(소성 SHAPE 없음)** 이고 transport 는 **이온 percolation *연결성*(최단경로)** 까지만 — σ 실값·
> Stage-E 소성면적·삼중항·MPM morphology 는 *안 함*. 그들이 비운 칸 = 우리 novelty. ⭐ Bielefeld 2019(ref [16])·LPS 소성변형
> (ref [29])을 *명시 인용* → 우리 litdb 가 이미 가진 두 논문과 직결.
> ⛔ 정정 2026-09-26 (원문 대조) — (iii) *"단 하나의 지배변수"* 는 **원문보다 세다.** 원문 §4: *"percolation depends **as much** on the
> cathode volume fraction as on the ratio of the cathode to SE particle size (λ)"*, §3.1: *"cathode utilization is affected by **both**
> particle size ratio and cathode loading"*. λ 의 우위는 **고-로딩 영역에 한정**해서만 말한다 (Abstract *"in the regime of high cathode loading
> … highly dependent on the particle size ratio"* · §5 *"most critically dependent"*).
> ⇒ 옳은 요약: **로딩과 λ 둘 다 지배, 고-로딩에서 λ 가 가장 결정적인 손잡이.** 또 *"(>80 wt% …) 에서도 거의 full"* 도 과하다 —
> 80 wt% 에서 near-full 은 λ ≈ 8 (12 µm NMC + 1.5 µm LPS, 실험 ≈141 mAh/g = 155 의 ≈91 %, digitized) 한 점이고, **85 wt% 는 λ = 8
> 에서도 θ ≈ 20 %** (본문 p.5 stated) 다 — ">80 wt%" 는 저자가 *"possible if λ is further increased"* (sub-µm SE) 로 **전망**만 한다.
> "우리 litdb 가 이미 가진 두 논문" 도 반만 맞다 — `[16]` Bielefeld 2019 는 정본 카드가 있지만 `[29]` Choi 2018 (*ACS AMI* 10, 23740) 은 **없다** (내용 `[미확인]`).

> 데이터 CSV: `docs/data/shi2019_am_loading.csv` (이 digest 전용 — λ·로딩·porosity·용량·utilization 정밀 수치, stated vs digitized 구분).
> ⛔ 2026-09-26 — 그 CSV 는 **작업 브랜치** 파일이고 위 오기 (80↔85 wt%, Fig 5b "SE 2 µm", Fig 5e 뒤바뀜, Fig 6 70 wt%) 를 그대로 담고 있다.
> 원문 대조판 판독값의 정본은 **`litdb/figures/shi2019_high_am_loading_particle_size_assb/digitized.csv`** (181 행, 방법·불확실도는
> `tools/litdb/shi2019_fig_digitize.py` 머리말). 작업 브랜치 CSV 수정은 1저자 몫 (이 카드는 정본 브랜치라 그 파일을 고치지 않는다).



> elements: Co Li Mn O S Zr

---

## 1. 한 줄 요약 (bilingual)

**KO** — Ceder 그룹(UC Berkeley + LBNL + Samsung)이 **LIGGGHTS DEM(우리와 동일 코드) + Hertz 접촉**으로 NMC(CAM)+LPS(SE)
복합 양극을 200 MPa 로 cold-press 압밀하고, 각 CAM 입자가 SE percolation 경로로 bulk-SE(separator)에 연결되는지를 **최단경로
percolation** 으로 판정해 **cathode utilization θ_CAM**(=활성 CAM 부피분율)을 계산. 핵심 발견: **θ_CAM 은 CAM 절대-부피분율보다
*크기비 λ = D̄_CAM/D̄_SE* 에 훨씬 민감** — *고정 로딩에서 SE 입경만 줄여도(λ↑) utilization 이 20%→100% 로 극적 상승*. 따라서 **SE 를
CAM 보다 작게(λ>1)** 하면 고-CAM 로딩(>80 wt% / >50 vol%, 액체셀 수준)에서도 거의 full 용량을 *간단 혼합·가압* 으로 달성. ⚠ 그들 DEM 은
**rigid-sphere(소성 SHAPE 없음)** + transport 는 **이온 *연결성*(percolation 존재/최단경로)** 까지 — *유효 σ 실값·접촉저항·열·전자 percolation·
소성 morphology 는 안 풂*. 실험(4 SE 크기 × 3 로딩 × 2 CAM 크기) 이 모델 예측 용량과 *good agreement*.

**EN** — The Ceder group (UC Berkeley + LBNL + Samsung) uses **LIGGGHTS DEM (same code as ours) + Hertzian contact** to
cold-press (200 MPa) NMC(CAM)+LPS(SE) composite cathodes, then judges — by **shortest-path Li-ion percolation** — whether each
CAM particle is connected through the SE network to the bulk-SE (separator), giving the **cathode utilization θ_CAM** (active CAM
volume fraction). Headline finding: **θ_CAM depends far more on the *particle size ratio* λ = D̄_CAM/D̄_SE than on the absolute CAM
volume fraction** — at *fixed loading*, merely reducing the SE particle size (raising λ) lifts utilization from ~20 % to ~100 %.
Hence **keeping SE smaller than CAM (λ>1)** enables high-CAM loading (>80 wt% / >50 vol%, liquid-cell level) with near-full capacity
by *simple mixing + pressing*. ⚠ Their DEM is **rigid-sphere (no plastic SHAPE)** and transport is **ionic *connectivity* (percolation
existence / shortest path) only** — no effective-σ values, no constriction resistance, no thermal/electronic percolation, no plastic
morphology. Experiments (4 SE sizes × 3 loadings × 2 CAM sizes) show *good agreement* with model-predicted capacities.

> ⛔ 정정 2026-09-26 (KO·EN 공통) — ① *"θ_CAM 은 CAM 절대-부피분율보다 λ 에 훨씬 민감 / depends far more on λ"* → 원문은 **"as much"**
> (§4 p.6) 이다 (위 머리 정정 참조). ② *"실험 4 SE × 3 로딩 × 2 CAM"* 은 **완전 요인배치가 아니다** — 실제 셀은 세 묶음이다:
> Fig 5a (NMC 5 µm · 60 wt% · LPS 8/5/3/1.5 µm, 4 셀) · Fig 5c,d (80 wt% · LPS 3/1.5 µm × NMC 5/12 µm, 4 셀) · Fig 6 (NMC 5 µm · LPS 3/1.5 µm ×
> 60/70/80 wt%, 6 곡선 — 60 wt% 두 개와 80 wt% 두 개는 Fig 5 와 같은 조건). ③ 용량은 **0.05 mA cm⁻² · 첫 사이클** 하나의 전류에서만
> 쟀다 (p.3) — 율특성·사이클 없음.

**이 논문의 위치 (우리 기준):** **frame[4] 외부 실험 앵커이자 동시에 DEM 방법론 *형제*.** Bazzoun(같은 코드·소재·transport)이
*transport σ 솔버 형제*라면, Shi 는 *그 한 단계 앞 — 압밀 + percolation-연결성을 같은 코드로 + 실험검증* 한 형제. 우리 "size=PACKING
not overlap"(σ_ionic·σ_e 의 size-effect 가 기하 packing 이지 overlap 이 아니라는 결론)의 **가장 직접적인 모델+실험 증거**. 그들이
비운 칸(σ 실값·삼중항·Stage-E·소성·dip 깊이의 정량)이 정확히 우리 novelty.

---

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Tan Shi**¹, **Qingsong Tu**¹ (¹동등기여), Yaosen Tian, Yihan Xiao, Lincoln J. Miara², Olga Kononova, **Gerbrand Ceder*** (Dept. Materials Science & Engineering, **UC Berkeley** + **Materials Sciences Division, Lawrence Berkeley National Lab**; ²Lincoln Miara = **Advanced Materials Lab, Samsung Research America**, Burlington MA) | *Adv. Energy Mater.* **2020**, 10, 1902881 (Received 2019-09-03, Published online **2019-12-03**; 표지년 2020) | **10.1002/aenm.201902881** (open access, CC-BY) | **SE = LPS (amorphous 75Li₂S·25P₂S₅, glass)** + **CAM = NMC (Li[Ni₀.₅Mn₀.₃Co₀.₂]O₂ = NMC532, LZO-coated)** | **mixed** — DEM(LIGGGHTS) 미세구조 모델링 + percolation 분석 **+ 실험**(셀 제작·사이클 검증) |

- **소재 정밀:** SE = **amorphous 75Li₂S–25P₂S₅(LPS) glass**, ball-milled, **σ_ion = 0.39 mS cm⁻¹**(SPEX-mixed bulk). CAM = **Li₀.₅Mn₀.₃Co₀.₂O₂ → 즉 LiNi₀.₅Mn₀.₃Co₀.₂O₂ = NMC532**, **6–8 nm LZO(Li₂O–ZrO₂) 코팅**(계면반응 억제 → 입경효과만 보려고). 도전제 = **CNF(carbon nanofiber) 5 wt%**(실험엔 넣되 모델엔 명시적 미포함, prefactor 0.95 로만 보정).
- ⚠ **소재 주의 (우리 대비):** SE = **LPS glass(σ 0.39 mS/cm)** ≠ 우리 **LPSCl Li₆PS₅Cl(σ ~1–3 mS/cm, ~3–8× 높음)**. CAM = **NMC532-LZO** ≠ 우리 **NMC811**. ⇒ **σ 절대값·용량 절대값 전이 금지**; *크기비-packing-utilization 추세*만 frame[4] 앵커. (단 둘 다 황화물 SE + 층상 NMC + cold-press → *거동·추세* 전이 가능.)
- 등록/게재: 2019-09-03 / 2019-11-01(rev) / **2019-12-03**(online). DOE BES DE-AC02-05CH11231 + Samsung Advanced Institute of Technology(SAIT) 지원. LZO-coated CAM = Samsung R&D Japan(Ito et al. ref [6] 절차) 제공.
  - ⛔ 정정 2026-09-26 — Acknowledgements 원문: 연구 지원은 **SAIT** 이고, DOE 계약 DE-AC02-05CH11231 은 **Molecular Foundry (SEM) 와
    Lawrencium 클러스터** 시설 지원으로 적혀 있다 (+ UC Berkeley Savio 클러스터). 소재 줄의 *"Li₀.₅Mn₀.₃Co₀.₂O₂"* 는 카드 오타 — 원문 **LiNi₀.₅Mn₀.₃Co₀.₂O₂** (p.1).
    인쇄 표기: 본문 쪽바닥 *"Adv. Energy Mater. 2020, 10, 1902881"* · SI 머리 *"Supporting Information for Adv. Energy Mater., DOI: 10.1002/aenm.201902881"* (© 2019).
- ⭐ **우리 litdb 와의 직결 인용:** ref **[16] = Bielefeld 2019**(우리 `bielefeld2019_microstructural_modeling_composite_cathode.md`); ref **[29] = Choi et al. ACS AMI 2018** = "LPS 입자의 *소성변형* 을 실험관측" → 본문 §3.2·§4 Discussion 에서 "**입자간 접촉면적의 정확한 기술은 LPS 의 소성변형 모델링을 요구**"라고 *우리 MPM/Stage-E 의 필요성을 명시* (아래 §7·§A 참조).
  - ⛔ 정정 2026-09-26 — 그 문장은 **§4 Discussion (p.7) 에만** 있다 (§3.2 는 Fig 4 시각화 절이고 소성변형을 말하지 않는다). 또 `[29]`
    (S. Choi *et al.*, *ACS Appl. Mater. Interfaces* **2018**, *10*, 23740) 은 **정본 litdb 에 카드가 없다** — 그 논문이 무엇을 관측했는지는
    Shi 의 한 줄 요약(*"plastic deformation of LPS particles, which has been observed experimentally"*)뿐이고 내용은 `[미확인]`.
    `[29]` 는 Fig 7a 의 *"previously reported densities and composite cathode porosities"* (Φ 0.1–0.2) 의 출처이기도 하다.

---

## 3. 핵심 물성 (수치)

> ★ = stated(본문/그림 라벨에 적힌 값). digitized = Fig 곡선에서 읽음(TREND only, ±). 이 논문은 **유효 σ 실값을 안 냄** → "물성"은
> **utilization θ_CAM · 크기비 λ · 로딩 f_CAM · 용량 · porosity**. 절대 σ·용량은 LPS-glass/NMC532-LZO → *우리 소재 절대전이 금지*.

| 물성 | 값 | 조건 (λ, 로딩, 입경) | stated/digitized | 비고 |
|---|---|---|---|---|
| **압밀 압력** ★ | **200 MPa**(미세구조 모델 + 양극 압밀); separator는 ~100 MPa | DEM·실험 공통 | stated | = 우리 300 MPa cold-press 계열(약간 낮음). ⛔ 2026-09-26: DEM 은 200 MPa 도달 뒤 **압력을 일정하게 유지**했다 (정압, p.2) — 변위정지가 아니다 (§4 정정). In 음극 부착에도 ≈200 MPa (p.3) |
| **porosity (모델 입력 범위)** ★ | **Φ ≈ 0.1–0.2** (그림 음영대 = 실험 보고 porosity) | SSB 양극 복합, ref [29] | stated (Fig 7a) | ⚠ *실험 보고 porosity 의 범위*로 인용 — 단일 측정값 아님; 우리 15.6 % 가 이 범위 안. ⛔ 2026-09-26: 모델 **입력이 아니다** — Fig 7a 의 wt%→vol% 환산에만 쓴 문헌값 (ref [29], 정본 카드 없음). **DEM 침대 자체의 porosity 는 보고되지 않았다 (n/a)** |
| **DEM 파라미터 (SI "Table 1")** ★ | E **18.5** / **177.5 GPa** · ν 0.3 / 0.3 · ρ 1.87 / 4.85 g cm⁻³ · γ_t 50 / 25 ("GPa", 원문 표기) · σ_y **2 / 12.6 GPa** | SE (LPS) / AM (NMC) — 문헌값 [1] McGrogan 2017 · [2] de Vasconcelos 2016 · [3] PAULING FILE · [4] Zhang–Makse 2005 | SI-stated (2026-09-26 보강) | ⭐ E_SE **무연화** (우리 DEM 1.35 = 18× 연화의 반대편). **μ · COR 은 표에 없다 (n/a)**. σ_y 가 힘 식에 어떻게 들어가는지는 기술 없음 — 값은 **나노압입 경도** (AM 177.5/12.6 = 정본 xu2017 의 소결 NMC532 **펠릿** E·H 와 동일, §S.1) |
| **cathode utilization θ_CAM** ★ | **θ_CAM = V_CAM^active / V_CAM** (활성 CAM 부피분율) | percolation 정의 | stated (Eq) | ⭐ 핵심 출력. = 우리 **f_AM^cc / dead-AM** 의 직접 대응 |
| **크기비 λ (핵심 변수)** ★ | **λ = D̄_CAM / D̄_SE** | — | stated | ⭐ 이 논문 전체의 지배 무차원수 |
| θ_CAM @ λ=1.67, f_CAM 변화 | f_CAM <70 wt% → **θ≈1**; >75 wt% → **급락** | D̄_CAM=5µm 고정 | stated (Fig 3a) | "75 wt% 위에서 percolation 약화 → utilization 감소". ⛔ 2026-09-26 판독 (Fig 3a, ±0.005): 60–71 wt% θ 0.98–1.00 · 75 → 0.92 · 76 → 0.83 · 78 → 0.64 · **80 → 0.50** · 82 → 0.33 · 85 → 0.19 · 90 → 0.13 (digitized). D̄_CAM 5 µm 는 3a 본문에 무명시 — Fig 3c 위축 표기로 추정 |
| θ_CAM @ f_CAM=70 wt%, λ 변화 | **λ<1 → θ 급락**; **λ≈1.67 → θ≈1**(full util.) | D̄_CAM=5µm | stated (Fig 3b) | ⭐ "고정 로딩서 SE 입경만 줄여(λ↑) θ 20→100%". ⛔ 판독 (Fig 3b): λ 0.33 → 0.22 · 0.42 → 0.35 · 0.625 → 0.44 · 1.0 → 0.67 · 1.67 → 0.99 · 3.33 → 1.00 · 4.0 → 1.00 (digitized). 점 7 개 — 본문 SE 목록(1.5–15 µm)은 6 개라 λ = 4 (SE 1.25 µm) 는 목록 밖 |
| **full-util. 임계 λ_min** ★ | f_CAM=70 → **λ_min=1.67**; 75 wt% → **λ_min=2.1**(98% util.) | θ_CAM 98% 기준 | stated (Fig 3d) | ⭐ **로딩↑ → 필요 λ↑** (= dip 의 조성의존을 λ 로 정량). ⛔ 2026-09-26: **기준이 섞였다** — 1.67 은 Fig 3b 의 이산 표본점("full"), 2.1 만 Fig 3d θ 98 % 곡선 (p.5 stated). Fig 3d 판독 — θ 98 %: 70 → 1.62 · 75 → 2.05 · 77 → 2.75 · 78 → 3.6 · 79 → 5.2 · **≈79.6 wt% 에서 λ = 8 (축 상한)**; θ 90 %: 75 → 1.72 · 78 → 2.97 · ≈80.2 wt% 에서 8; θ 80 %: 75 → 1.50 · 78 → 2.33 · 80 → 3.9 · ≈80.9 wt% 에서 8 (digitized, ≥79 wt% 는 수직 구간이라 f_CAM ±0.3 wt% 로 읽을 것) |
| λ_min 예시 (75 wt%, 98% util) | D̄_CAM 5µm → **D̄_SE 2.4µm**; 20µm → **9.5µm** | λ_min=2.1 | stated | 설계 지침 핵심 숫자 |
| **고-CAM 로딩 달성** ★ | **f_CAM=80 wt% ≈ 50 vol%**(=액체셀 수준) @ near-full util. | D̄_CAM=12µm + D̄_SE=1.5µm (λ=8) | stated (Fig 5d,§4) | ⭐ **"단순 혼합·가압으로 >50 vol% CAM"** = 논문 타이틀 결과. ⛔ 2026-09-26: "near full" 의 실체 = 실험 **141.1 mAh/g ≈ 155 의 91 %** (Fig 5e digitized); 50 vol% 는 Fig 7a 의 Φ 0.1–0.2 대역 **47.4–53.3 vol%** 의 가운데 (digitized) |
| utilization @ f_CAM=80, λ=8(1→8) | θ_CAM **16%→20%** (λ 1→8) | D̄_SE 3µm, D̄_CAM=5→… | stated 본문(p.5) | 80 wt%서 λ 키워도 5µm CAM 으론 미흡 → 큰 CAM 필요. ⛔ **오기 (2026-09-26)** — θ 16 → 20 % (λ 1 → 8) 는 **f_CAM = 85 wt%** 값이다 (p.5 *"at fCAM = 85 wt% increasing λ from 1 to 8 only slightly increases θCAM from ≈16% to ≈20%"*). 80 wt% 의 원문 값은 **λ 1 → 3 에서 θ ≈30 → ≈60 %** (p.4–5, Fig 3c 서술). "5 µm CAM 으론 미흡 → 큰 CAM 필요" 는 이 숫자에서 나오는 결론이 아니다 |
| utilization @ f_CAM=85 wt% | λ 1→8 → θ_CAM "only slightly" 상승 | — | stated | 고로딩 한계. (값: θ ≈16 → ≈20 %, p.5 stated) |
| visualization util. (Fig 4) | model b θ_CAM=**52%**, model c **25%** | f_CAM=80, D̄_SE 3 vs 5µm | stated (Fig 4) | 큰 SE(5µm) → 활성 CAM 절반↓. (보강: model a = 70 wt% · λ 1.67 → **98 %**, p.5 stated) |
| **SE 입경별 σ_ion(LPS)** ★ | bulk(SPEX) **0.39 mS/cm**; ball-mill 작을수록 **σ_ion 감소**(GB↑) | Table S3 | stated 본문(p.3) | ⚠ 작은 SE = σ_ion *낮아짐*(재료) 인데도 utilization↑(packing) → **"size=packing not σ"**. ⛔ 2026-09-26 SI Table S3 값 (SI-stated): **8 µm 0.32 · 5 µm 0.24 · 3 µm 0.22 · 1.5 µm 0.14 mS/cm** (밀링 0.5 / 1.5 / 15 / **40 h**, 밀·볼·용매도 함께 바뀜 — §S.4). 0.39 는 밀링 **전** 합성품. ⇒ 입경 효과로 분리 불가 · 1.5 µm ÷ bulk = **0.36** (SELF-51) |
| **실험 용량 (5µm NMC, λ 스윕)** | D̄_SE 8/5/3/1.5µm → ~**75 / 125 / >150 / >150 mAh/g**(λ↑→용량↑) | f_CAM=60 wt%, 5µm NMC | digitized Fig 5a/stated | 작은 SE(큰 λ) = 큰 용량 = θ_CAM↑ 실험검증. ⛔ 75 / 125 / >150 은 본문 p.5 **stated** 다. Fig 5b 판독 실험값: 76.1 / 122.8 / 151.4 / 152.3 mAh/g (SE 8/5/3/1.5) |
| 실험 용량 (λ=2.5→0.6, 5µm CAM) | SE 2µm→8µm → ~**155→~80 mAh/g** (모델·실험 일치) | Fig 5b | digitized Fig 5b | λ 2.5(SE 2µm) full → λ 0.6(SE 8µm) 반토막. ⛔ **오독 (2026-09-26)** — "2.5 · 1.3 · 0.8 · 0.6" 은 Fig 5b **위쪽 축 눈금** (아래 축 SE 2/4/6/8 µm 에 대응) 이지 데이터가 아니다; SE 2 µm 시료는 없다. 점 = SE 1.5/3/5/8 µm (λ 3.33/1.67/1.00/0.625): 모델 ≈155 (가려짐) / ≈155 (가려짐) / 127.9 / 87.3 · 실험 152.3 / 151.4 / 122.8 / 76.1 mAh/g (digitized ±1.5) |
| **CAM 입경 효과** ★ | 12µm CAM > 5µm CAM **용량 더 큼**(f_CAM=80, SE 3·1.5µm) | Fig 5c–e | stated | ⭐ **큰 CAM = 표면적당 SE-접촉 확률↑ → percolation↑** (반직관). ⛔ "표면적당" 은 오역 — 원문 *"Larger cathode particles have a higher surface area and therefore a higher probability of contacting a percolating SE network"* (§4 p.6) = **입자 하나의 표면적이 커서 그 입자가 망에 닿을 확률이 크다** |
| 실험 용량 (CAM 4→12µm) | 3µm SE: ~80→~140; 1.5µm SE: ~95→~130 mAh/g | f_CAM=80 wt% | digitized Fig 5e | 모델·실험 good agreement. ⛔ **오독 (2026-09-26)** — 점은 CAM **5 · 12 µm 두 개뿐** (가로축 4–12 는 그림 범위) 이고 12 µm 값이 SE 크기끼리 뒤바뀌었다. 판독: **3 µm SE** 실험 78.3 → **127.9** (모델 74.5 → 134.3) · **1.5 µm SE** 실험 96.3 → **141.1** (모델 111.1 → ≈140, 가려짐) mAh/g |
| 최대 실험용량(정규화 기준) | **155 mAh/g**(관측 최대) × θ_CAM(모델) = 모델 용량 | — | stated | 모델→용량 환산법 |
| Fig 6 (60/70/80 wt% 용량) | 60·70 wt% > **150 mAh/g**(λ≥1.67 고-util 영역); 80 wt% 급락 | 3µm & 1.5µm LPS, 5µm NMC | stated/digitized Fig 6 | f_CAM=60→70 wt% **용량 손실 없이** 증가 가능(1.5µm SE). ⛔ **과일반화 (2026-09-26)** — 원문의 "green 영역 · 둘 다 > 150" 은 **60 wt% 에 대해서만** (p.6). 70 wt% 는 **1.5 µm LPS (λ 3.33) 만** 손실 없음 (판독 154.0); 3 µm LPS (λ 1.67) 는 **137.6** (모델 153.5). 80 wt%: 78.5 (3 µm) · 96.6 (1.5 µm) (모델 ≈75 · 111.3) — digitized Fig 6b,d |
| **θ_CAM @ 80 wt% — SI Fig S1b 평탄값** | λ 3.33 → 67.7–69.5 % · λ 2.4 → 58.2–60.8 % · λ 1.67 → 47.1–49.5 % · λ 1.5 → 44.9–47.1 % | CAM:SE = 80:15, box ≥ 문턱, CAM 5·12 µm 섞임 | digitized (±0.3 %p; 세로축 라벨 오기 §S.2) | CAM 크기가 섞여도 **λ 순서 그대로** = λ-지배의 두 번째 (광고되지 않은) 증거. λ 1.67 값은 Fig 3a (0.50) · Fig 4b (0.52) 와 일치 |
| **Fig S2 — λ vs 절대 크기** | 5 µm CAM: λ 0.40 / 0.62 / 0.99 / 1.67 → θ 0.39 / 0.60 / 0.80 / 1.00 · 12 µm CAM: 0.42 / 0.63 / 1.00 / 1.67 / 3.33 → 0.36 / 0.56 / 0.78 / 0.98 / 0.99 | **f_CAM = 60 wt%** (SI 캡션) | digitized (±0.003) | 같은 λ 에서 두 CAM 크기 차 ≤ 0.035. ⚠ 본문은 Fig 3b (70 wt%) 의 확인이라 적지만 S2 는 60 wt% |
| **Fig 7a — wt% ↔ vol%** | 70 wt% → 46.3 / 41.7 / 37.1 vol% · 80 → 59.1 / 53.3 / 47.4 · 85 → 66.6 / 60.1 / 53.5 (Φ = 0 / 0.1 / 0.2) | 밀도 = SI Table 1 (LPS 1.87 · NMC 4.85); f_CAM 분모에 5 wt% CNF 포함 | digitized (±0.2 vol%) | ⚠ 우리 LPSCl·NMC811 밀도와 이원(무탄소) wt% 로는 **다시 계산**해야 한다 (§A.2 ⛔). Fig 7b 세로축은 판독 금지 (눈금 오기, §6) |
| **σ_thermal / σ_electronic** | **n/a** | — | — | 이 논문 = 이온 percolation 만. 전자전도는 *CNF 가 담당*(모델 미포함) |
| coverage / 접촉면적% | **n/a**(정량 없음) | — | — | "접촉면적 정확기술 = LPS 소성변형 모델 필요"라고 *향후 과제* 명시(§4) |
| coordination Z | **n/a** | — | — | percolation 경로(최단경로)만, 배위수 직접 측정 없음 |
| **E_SE / σ_y / ν** | **n/a (수치 미보고)** → ⛔ SI 에 있다 | LPS | — | Hertz 접촉에 탄성 파라미터 쓰지만 *본문에 값 없음*(SI S1). 소성캡 없음(rigid Hertz). ⛔ **철회 (2026-09-26)** — SI "Table 1" (SI p.2): E 18.5 GPa · ν 0.3 · σ_y 2 GPa (SE); 177.5 · 0.3 · 12.6 (AM) — 위 "DEM 파라미터" 행. "소성캡 없음" 은 그대로 (SI 힘 식에 항복 항이 없다) |
| Heckel P_y / knee | **n/a** | — | — | Heckel 분석 없음(단일압력 200 MPa, 압밀곡선 미보고) |
| **PSD (D̄ / σ)** ★ | **SE: 1.5 / 3 / 5 / 8 µm**; **CAM: 5 / 12 µm** | log-normal, SEM-matched | stated (Fig 1b, Fig 2) | ⭐ 우리 12:4:1 과 직접 비교축. λ 범위 **0.6–8**. ⛔ 보강 (SI Table S2, SI-stated) — σ (µm): CAM 5 → 1.6 · CAM 12 → 3.5 · SE 1.5 → 0.5 · SE 3 → 1.0 · SE 5 → 1.5 · SE 8 → 2.0; 절단 min / max 직경 (µm): 3.0/10.0 · 5.0/25.0 · 0.8/3.0 · 2.0/6.0 · 3.2/10.0 · 5.8/13.0. λ 범위는 **모델 0.33–8** (Fig 3b 는 SE 12·15 µm 까지) · **실험 0.625–8** |
| **box-size 수렴 규칙** ★ | **L_box = 1.5·L_min ≈ 15·D̄_max** | RVE 수렴 | stated (§2.1, SI S2) | = 우리 RVE 박스팩터(우리 ~35)와 동류 — 절대값 다름. ⛔ 보강 (SI §2): D̄_max = **가장 큰 성분의 평균 직경** (CAM 5 또는 12 µm) — 큰 오차 문턱 L < 50 µm (CAM-5) · L < 120 µm (CAM-12) = 10 × 평균 CAM 직경. SI 문장은 *"maximal particle diameter d_max"* 라 쓰지만 Table S2 최대 직경 (10 / 25 µm) 이면 100 / 250 µm 여야 한다 → 수식(D̄) 쪽이 맞다. L 은 **압밀 전 초기 입방** 한 변 (*"minimal initial box size"*), 판정 조성 80:15, 11 개 상자 |

### 핵심 5개 데이터 포인트 (외워둘 값)
- **λ = D̄_CAM / D̄_SE** — 이 논문의 지배 무차원수. **"SE 를 CAM 보다 작게(λ>1)"** 가 황금률.
- **λ_min(full util.): 70 wt% → 1.67 / 75 wt% → 2.1** — **로딩↑ → 필요 λ↑** (조성-의존 dip 을 λ 로 정량).
- **f_CAM=80 wt% ≈ 50 vol% CAM**(액체셀 수준) = **D̄_CAM 12µm + D̄_SE 1.5µm (λ=8)** 로 달성.
- **작은 SE = σ_ion(재료) *낮아짐* 인데도 utilization↑** → **size=PACKING(연결성) not σ-material**(우리 결론과 동일).
- **큰 CAM = utilization↑**(반직관) — 큰 입자가 *표면적당 percolating-SE 접촉 확률↑* (Discussion §4 명시).
- ⛔ 2026-09-26 보강 (외워둘 값을 원문으로 다시 적는다):
  - λ_min: 70 wt% → 1.67 은 Fig 3b 표본점, 75 wt% → **2.1 (θ 98 %)** 만 Fig 3d. 80 wt% 는 θ 80 % ≈ **3.9** · 90 % ≈ **5.9** · 98 % **> 8** (digitized).
  - 80 wt% ≈ 50 vol% 의 "near full" = **실험 141 mAh/g (155 의 ≈91 %)**, λ = 8 한 점. 85 wt% 는 λ 8 에서도 **θ ≈ 20 %** (stated).
  - 작은 SE 의 σ 는 **SI Table S3: 0.32 → 0.24 → 0.22 → 0.14 mS/cm** (8 → 1.5 µm) — 단 밀링 시간 0.5 → 40 h · 밀 · 용매가 같이 바뀌었다.
    용량은 **0.05 mA cm⁻²** 저전류 한 점이라 σ 벌점이 거의 안 보이는 조건이다 ⇒ *"packing 이 σ 를 이긴다"* 는 **저율 · 연결성 지배 영역**의 서술로만 (§A.1 ⛔).
  - "표면적당" → **입자당 표면적이 커서** 망에 닿을 확률↑ (원문).

---

## 4. 시뮬레이션 방법 ★

- **code / version**: ⭐ **LIGGGHTS (open-source DEM) = 우리와 동일 코드** (refs [18–20] = Kloss/Goniva LIGGGHTS, Di Renzo, Schöpfer). + **percolation 분석**(자체, Dijkstra 류 최단경로). + **QuickSurf**(시각화, Fig 4 SE surface).
- **DEM 접촉법칙**: ⭐ **Hertz** granular contact (normal + tangential, refs [22 Zhang–Makse, 23 Sakuda]) + **damping** + **frictional yield**(마찰만, 소성 SHAPE 아님). = 우리 hooke/hysteresis 와 *같은 계열의 탄성-접촉*(우리는 hysteresis, 그들은 Hertz). **항복캡/소성흐름 없음** — rigid sphere.
  - ⛔ 정정 2026-09-26 — 참고문헌 번호가 틀렸다: 본문 p.2 *"normal and tangential interactions and damping forces**[22]** as well as the
    frictional yield … **[23]**"* 에서 **[22] = Silbert *et al.*, *Phys. Rev. E* 2001, 64, 051302** · **[23] = Zhang & Makse, *Phys. Rev. E* 2005, 72, 011301**
    (둘 다 원 목록 그대로; Sakuda 는 [7]·[10]). SI §1 의 힘 식 (SI p.2, 원문 그대로 옮김):
    `F_ij = √δ · √(R_i R_j /(R_i + R_j)) · [ (k_n δ n_ij − γ_n (v·n_ij) n_ij)  +  (k_t δ t_ij − γ_t (v·t_ij) t_ij) ]`,
    *"δ is the overlap distance … defined as δ = d − (R_i + R_j)"* (부호 규약·접선 변위를 δ 로 쓴 것 모두 인쇄 그대로) — LAMMPS/LIGGGHTS
    `gran/hertz/history` 형 (Silbert · Zhang–Makse). **식 안에 항복·소성 항이 없다** → "rigid sphere · 탄성 Hertz" 판정은 SI 가 **확인**한다.
- **재료 파라미터**: E_SE·E_CAM·ν·μ 를 SI S1 에 두되 **본문에 수치 미보고**. (Hertz 탄성 + 마찰 yield. 소성 항복응력 σ_y 캡 *없음*.)
  - ⛔ 철회 2026-09-26 — **SI "Table 1" 에 있다** (SI p.2, *"Simulation parameters used in the Hertzian contact model"*; 원문 참조 [1–4]):
    E_c **18.5** GPa (SE, [1] McGrogan 2017) / **177.5** GPa (AM, [2] de Vasconcelos 2016) · ν 0.3 / 0.3 · ρ 1.87 ([3] PAULING FILE) / 4.85 g cm⁻³ ([2]) ·
    γ_t 50 / 25 (단위 "GPa" 원문 표기 — 감쇠상수의 차원과 안 맞는다, 그대로 옮김) · **σ_y 2 / 12.6 GPa**. **μ (마찰계수) · COR · k_n · k_t 는 표에 없다 = n/a.**
    σ_y 는 표에는 있으나 힘 식에 들어가는 자리가 **기술되지 않았다** (n/a) — "σ_y 캡 없음" 은 그대로 둔다.
    ★ **"σ_y" 는 항복응력이 아니라 나노압입 경도(H) 값이다** (정본 카드 대조):
    - **AM**: E 177.5 · σ_y 12.6 은 정본 `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` 카드 (Xu 2017 *JES* 164 A3333, PDF 확인, Table 1 stated)
      의 **치밀 소결 NMC532 펠릿 E 177.5 ± 19.5 · H 12.6 ± 1.4 GPa** 와 **소수점까지 같다** (같은 Zhao 그룹). 그런데 Shi 는 이 값을 `[2]` de Vasconcelos
      2016 *EML* 에 단다 — 정본 xu2017 · `sedlatschek2026_…` 두 카드는 그 EML 논문을 **이차입자 139 GPa · H 8.9** 로 인용한다 ⇒ **Shi 의 `[2]` 귀속이
      틀렸을 공산이 크다** (EML 원문 미확인 → 판정 보류). 또 이 값은 **치밀 펠릿**이라 Shi 가 모사한 NMC **이차입자** (xu2017: 142.5 ± 11.3 · H 8.6) 보다
      E 가 1.25× 단단하다.
    - **SE**: "2 [1]" 은 정본 `so2021_dem_mold_pressure_assb_coldpress` 카드가 So 2021 Table 1 경유로 적은 McGrogan LPS **경도 H = 1.9 GPa** 와 맞는다
      (2차 인용 · McGrogan 원문 미확인).
    - ⇒ Tabor (H ≈ 3 σ_y) 로 읽으면 실제 항복응력은 이 값의 ≈1/3 이다 — 그러나 SI 힘 식에 σ_y 가 **안 들어가므로** 결과에는 영향이 없다 (쓰임새 n/a).
  - ⭐ **우리 대비 핵심**: E_SE **18.5 GPa 무연화** (우리 DEM E_eff 1.35 = real 24 의 18× 연화). 우리 틀 (*"E-강성이 porosity floor 를 정한다 ·
    강체구 floor ≈ 20 %"*) 로는 이 침대가 200 MPa 에서 실험 Φ 0.1–0.2 보다 **성길 공산이 크다** — 그러나 **DEM porosity 는 보고되지 않았다**
    (derived(ours) 추정, 값 n/a). 즉 θ_CAM(λ, f_CAM) 은 "성긴 강체구 침대의 연결성" 이고, Fig 7 의 vol% 는 **실험 porosity** 로 환산했다 —
    모델 침대와 환산 porosity 가 **다른 양**이다.
- **bond/binder 모델**: **없음.** CNF(도전제) 는 **모델에 명시적 미포함** — prefactor **0.95**(=5 wt% CNF 질량 보정)로만 f_CAM·f_SE 정의: `f_CAM = 0.95·M_CAM/(M_CAM+M_SE)`, `f_SE = 0.95·M_SE/(M_CAM+M_SE)`. SE 다공/바인더 morphology 없음.
- **MPM/continuum**: ⭐ **없음.** 입자는 *영원한 강체 구*. **소성 SHAPE 변화·void-fill 흐름 전혀 없음.** ⚠ ★ 단 §3.2·§4 에서 **"입자간 접촉면적의 정확한 기술은 LPS 의 *소성변형* 모델링을 요구하며, 그 변형 정도가 접촉면적·따라서 접촉저항을 좌우한다"** 고 *명시적으로 자기 한계를 인정*(ref [29] Choi 2018 LPS 소성관측 인용) → **정확히 우리 MPM(SHAPE 소성) + Stage-E(소성 접촉면적)가 메우는 칸**.
  - ⛔ 2026-09-26 — 그 문장은 **§4 (p.7) 에만** 있다 (§3.2 아님). 원문: *"Further refinement of the effect of λ on the ionic diffusivity … would
    require additional details, such as the Li transport properties across particle boundaries and the contact area between particles. An
    accurate description of the contact area between particles requires modeling of the plastic deformation of LPS particles, which has been
    observed experimentally.[29] The degree of the deformation will largely determine the contact area between particles and therefore the
    resistance at particle boundaries."*
- **전달 솔버 (σ)** ★: ⭐ **유효 σ 를 *안 푼다*** — **이온 percolation *연결성*** 만:
  - **CAM "active" 판정**: 한 CAM 입자가 *최소 1개 Li-percolation 경로* 로 bulk-SE(separator)에 연결되면 active(Fig 1c).
  - **네트워크**: CAM 입자를 노드로(이웃 CAM 연결), SE 입자를 **bulk-SE 경계의 target 노드**로, CAM 을 source 로 → **각 CAM 의 *최단 percolating 경로*** 추출(ref [26] Zeng–Church = 그래프 최단경로) → CAM 이 separator 에 닿는가 판정.
    - ⛔ 정정 2026-09-26 — 원문 (p.2): *"we first built networks of CAM particles by connecting each node (**CAM or SE particles**) with its
      neighbors and then defined CAM particles as source nodes and **SE particles located at the bottom boundary** as target nodes.[26]"* —
      노드는 CAM **과** SE 둘 다이고, target 은 **바닥 경계의 SE 입자**다. "이웃" 의 판정 기준 (중첩 δ > 0? 거리 문턱?) 은 **기술 없음 (n/a)**.
      알고리즘 이름도 없다 — "Dijkstra 류" 는 카드의 의역이고, `[26]` (Zeng & Church, *Int. J. Geogr. Inf. Sci.* 2009, 23, 531) 의 내용은 `[미확인]`.
  - **이온은 SE 로만**(refs [24,25]): "Li 확산이 CAM 보다 SE 에서 훨씬 빠름 → percolation 경로는 SE 입자로만" → SE=이온 backbone. **constriction/contact 저항 *없음*** — 연결성(존재)까지만.
  - ⚠ 즉 그들 "transport" = **Bielefeld 2019 와 같은 *percolation 연결성* 수준** (σ 실값 아님). 단 Bielefeld 가 *cluster 부피/면적* 이면 Shi 는 *각 CAM 의 separator 도달여부(최단경로)* → **utilization** 으로 환산.
- **입자 처리** ★ (DEM판 "무질서 처리"):
  - ⭐ **구(sphere) 만, 소성 SHAPE 없음(rigid).** AM·SE 둘 다 강체 구. *형상변화·δ-overlap-as-flow 없음* — Hertz 탄성 접촉 + 마찰. = 우리 DEM rigid-sphere 가정과 **물리적으로 동일**.
  - ⭐ **bi-disperse(이성분 크기) + log-normal PSD.** SE 4크기(1.5/3/5/8µm) × CAM 2크기(5/12µm), 각 성분 **log-normal 분포**(SEM σ 매칭, Fig 1b). λ 범위 **0.6–8**. → **우리 12:4:1 이산 다분산과 동형의 *연속-크기비* 스윕**.
    - ⛔ 보강 2026-09-26 — 모델은 SE **12 · 15 µm** 도 썼다 (Fig 3b) → 모델 λ 범위 **0.33–8**, 실험만 0.625–8. 분포 매개변수 (σ · 절단 min/max) =
      SI Table S2 (§3 표). ⚠ "우리 12:4:1 과 동형" 은 조심 — Shi 는 **CAM 단봉 × SE 단봉** (이성분) 이고 우리 AM 은 **이봉** (AM_P + AM_S) 이라
      하나의 λ 로 접히지 않는다 (§A.2 ⛔).
  - **압밀 = 재배열 + Hertz 탄성중첩** (소성흐름 아님). 평판을 위에서 prescribed-velocity 로 내려 200 MPa 도달 → 정지 → 운동E→0 까지 hold(=우리 hold protocol).
    - ⛔ **정정 2026-09-26 — 프로토콜이 반대다.** 원문 (p.2): *"moved downward at a prescribed velocity until the system reaches a specified
      pressure of 200 MPa. **Pressure was then held constant** until the system reaches static equilibrium (i.e., the kinetic energy of the
      system decayed to zero).[21]"* = **정압 유지 (stress-controlled dwell)** — 우리 MPM 의 `servo` 쪽이고, 우리 `hold` (= LIGGGHTS 식
      **변위정지** + 이완) 가 **아니다**. 정압 유지 중에는 재배열이 계속되어 침대가 더 조밀해질 수 있다 → 같은 "200 MPa" 라도 우리 변위정지
      침대와 최종 기하가 다를 수 있다 (크기 n/a). 평판 속도·정지 판정 문턱은 **보고 없음**. `[21]` = Roberts *et al.* *J. Electrochem. Soc.* 2014,
      161, F3052 (원 목록 그대로, 내용 `[미확인]`).
- **도메인/RVE / seeds / 압력범위**: 입방 V_box, **L_box = 1.5·L_min ≈ 15·D̄_max**(수렴, SI S2). 전이영역 통계 위해 **각 조건 ≥3 random initial config 평균**. 단일압력 **200 MPa**(separator ~100 MPa). 4벽 + 상하 평판 granular wall.
  - ⛔ 보강 2026-09-26 — 경계: *"Granular contact walls were placed at the bottom and all four vertical boundaries of the box. A flat surface
    was applied at the top"* (p.2) = **주기경계 없음, 벽 5 면 + 움직이는 윗면**. separator ~100 MPa 는 **실험 셀** 제작 조건이지 DEM 입력이 아니다.
    D̄_max = 가장 큰 성분의 **평균** 직경 (SI §2, §3 표 ⛔). "≥3" 은 *"at least three different random initial configurations"* — 산포 (오차막대) 는 **어느 그림에도 없다**.
- **특이사항/튜닝**: CNF prefactor 0.95; θ_CAM 환산 = (모델 θ_CAM) × (실험 관측 최대용량 155 mAh/g) = 모델 예측 용량 → Fig 5b/d 에서 실험과 직접 비교. **모델 검증을 12µm CAM 으로 반복**(Fig S2)해 "λ 효과지 SE-크기 단독 아님" 확인.
  - ⛔ 정정 2026-09-26 — Fig S2 의 조성은 **f_CAM = 60 wt%** 다 (SI 캡션 *"The CAM loading was fixed at 60 wt%"*) — 본문 p.4 는 Fig 3b
    (70 wt%) 문맥에서 S2 를 인용하지만 같은 조성이 아니다. 판독: 같은 λ 에서 5 µm · 12 µm CAM 의 θ 차 ≤ 0.035 (§3 표). 또 SI Fig S1b 의
    80 wt% 평탄값 (CAM 5 · 12 µm 혼합, λ 1.5–3.33) 도 λ 순서대로 선다 = 광고되지 않은 **두 번째** λ-지배 증거.
    모델 용량 = 155 × θ 는 *"θ shown in Figure 3c"* 에서 읽었다고 적혀 있다 (p.5) — 즉 **열지도 보간값**이다 (Fig S2 · 3b 의 표본점과 ±0.03 어긋날 수 있다: 60 wt%, λ 1 에서 S2 0.80 ↔ Fig 5b 모델 127.9/155 = 0.83).

---

## 5. 섹션별 결과 — ALL numbers

### 5.0 Abstract / Introduction (p.1–2)
- **문제:** SSB 복합양극은 보통 **SE 30–50 wt%** 필요 → **CAM 부피분율 낮음 → 에너지밀도 낮음.** 액체셀은 CAM **>90 wt% (>50 vol%)** → SSB 가 경쟁하려면 고-CAM 로딩 필수.
- **반직관 핵심 메시지:** "**고-CAM 로딩에서 utilization 은 CAM/SE 입자 크기비(λ)에 강하게 의존**" — **SE 입경↓ + CAM 입경↑(λ↑)** → **>50 vol% CAM 고-utilization 을 *단순 혼합·가압* 으로** 달성. "**가장 결정적 인자 = SE 를 CAM 보다 작게**"(by factor 2–3 → utilization 20%→100%).
- **이온 percolation 이 율속:** 결과는 "**cold-press SSB 양극에서 이온 percolation 이 limiting factor**"라는 개념과 정합.

### 5.1 Computational & Experimental Methods (p.2–3)
- **§2.1 모델링:** 무작위 삽입 구 CAM/SE → 입방 도메인. CNF 미포함(0.95 prefactor). log-normal PSD(Fig 1b, SEM 매칭). **LIGGGHTS DEM** + Hertz + 평판 200 MPa 압밀 → 정지. CAM active 판정 = 최단 percolating 경로로 separator 도달(Fig 1c). θ_CAM = V_CAM^active/V_CAM. **box 수렴 L_box=1.5L_min≈15D̄_max**, 각 조건 ≥3 config 평균.
  - ⛔ "→ 정지" 는 틀렸다 — 200 MPa 에서 **정압 유지** 후 운동에너지 → 0 (§4 ⛔). f_CAM 정의의 0.95 는 **5 wt% CNF 를 분모에 넣는 규약** —
    Shi 의 "f_CAM = 80 wt%" 는 CAM:SE:CNF = **80:15:5** (Fig 6 캡션) 이고, CAM:SE 이원비로는 **84.2:15.8** 이다 (derived(ours)).
- **§2.2 실험:** **NMC(D̄=5µm, Samsung Japan) + 대입경 NMC(D̄=12µm, MSE Supplies)**, 둘 다 **6–8 nm LZO 코팅**(Ito ref [6], 계면반응 억제 → 입경효과만). **Bulk LPS** = Li₂S(99.98%)+P₂S₅(99%) **SPEX 8000M 50mL ZrO₂, 200 min** → σ_ion **0.39 mS/cm**(ref [27] 일치). **작은 LPS** = wet ball-mill(heptane+dibutyl ether, Retsch PM200, ZrO₂ 1–10mm) → **1.5/3/5/8 µm**, ⚠ **작을수록 σ_ion *감소*** (GB/입계저항↑ + 잔류용매, Table S3). **셀:** PEEK 실린더(내경 8mm)+SS 로드 집전체; bulk LPS 35mg @~100 MPa → 양극(5mg)@~200 MPa → In 음극 @~200 MPa. **5 MPa 작동압**(스프링). Bio-Logic VMP300, 2–3.7 V vs In, 0.05 mA/cm², CCCV(5h hold @top).
  - ⛔ 정정 2026-09-26 — **본문과 SI 가 어긋난다; 밀링 조건은 SI Table S3 를 따른다.** 본문 p.3 은 작은 LPS 를 *"wet ball milling … with heptane
    and dibutyl ether using a Retsch PM200 … ZrO₂ balls ranging in size from 1 to 10 mm"* 라 적지만 SI Table S3 는 **8 · 5 µm = SPEX 8000M
    (1060 cycles/min) · heptane 만 · 볼 5 / 3 mm · 0.5 / 1.5 h**, **3 · 1.5 µm = Retsch PM200 (300 rpm) · heptane + dibutyl ether · 볼 3+1 / 1 mm ·
    15 / 40 h** 다 (볼 최대 5 mm — 10 mm 는 표에 없다). 모든 경우 50 mL ZrO₂ 자 + Y 안정화 ZrO₂ 볼 (SI-stated). σ: **0.32 / 0.24 / 0.22 / 0.14 mS/cm**
    (In 차단전극 임피던스; 펠릿 성형압 · 온도 · 두께는 **보고 없음**). 입경은 SEM 에서 ≈200 입자 평균 (p.3) — 레이저 PSD 아님. 전체 판정 §S.4.

### 5.2 Influence of Particle Size Ratio & Cathode Loading on θ_CAM (p.4 — Fig 3, 핵심)
- **Fig 3a (λ=1.67 고정, f_CAM 60→90 wt%):** f_CAM **<70 wt% → θ_CAM=1**(full util.); **>75 wt% → θ_CAM 급락.** ⇒ "Li percolation 이 SE 양 감소(=CAM↑)로 약화." 고정 λ 에 대응하는 **최대 f_CAM(=full util. 유지)** 존재(이 경우 70 wt%).
- **Fig 3b (f_CAM=70 wt% 고정, λ=D̄_CAM/D̄_SE 변화, D̄_CAM=5µm, SE 1.5/3/5/8/12/15µm):** ⭐ **θ_CAM 이 *오직 SE 입경 변경만으로* 20%↔100% 변동.** **λ<1 → percolation 명백히 감소**(SE 가 CAM 보다 크면 나쁨). **λ≈1.67 → θ≈1.** "최소 λ 가 주어진 로딩의 full util. 에 필요." **12µm CAM 으로도 같은 결과**(Fig S2) → "효과는 λ 때문이지 SE-크기 단독 아님."
- **Fig 3c (θ_CAM heatmap, λ × f_CAM):** percolation 은 **f_CAM↓(=위→아래 SE wt%↑)** 또는 **λ↑(좌→우)** 로 *항상* 개선. ⇒ **고-로딩 고용량 = 큰 λ 필요.** **λ<1 은 어떤 경우든 악화**(SE 는 *항상* CAM 보다 작아야 — separator 의 "큰 SE 선호"와 정반대).
- **Fig 3d (full-util. 임계 λ vs f_CAM, θ_CAM=80/90/98% 곡선):** ⭐ **λ_min 이 f_CAM 에 강의존.** 예: **75 wt% 로딩서 98% util. → λ_min=2.1** → 5µm CAM 이면 **SE 2.4µm**, 20µm CAM 이면 **SE 9.5µm**. f_CAM=80 wt%서 **λ 1→3 → θ 30%→60% 두 배**; 그러나 **f_CAM=85 wt%서 λ 1→8 → θ 16%→20% (미미)** → 고로딩 한계.
  - ⛔ 2026-09-26 — 80 / 85 wt% 두 문장은 원문에서 **Fig 3c** 서술이다 (p.4–5 *"Figure 3c shows that the benefits of λ reduction [sic] are
    very dependent on the cathode loading"* — "reduction" 은 원문 그대로, 뜻은 λ 증가). Fig 3d 자체의 판독은 §3 표 (θ 98 % 곡선은
    **≈79.6 wt% 에서 λ = 8 (축 상한) 을 넘는다** ⇒ 80 wt% 에서 98 % 는 이 그림 범위 안에서 **불가능**; 80 wt% 에서 θ 80 % ≈ λ 3.9 · 90 % ≈ 5.9).
    곡선이 **65–75 wt% 에서 거의 평평 (λ 1.2–2.1)** 하다가 **77–80 wt% 에서 수직으로 선다** — "로딩↑ → λ_min↑" 는 사실상 **문턱 하나**
    (≈78 wt% ≈ 이 계의 CAM ≈ 50 vol% 근처, Fig 7a) 의 서술이다 (derived(ours)).
  - ⛔ Fig 3b 의 "12 µm CAM 으로도 같은 결과 (Fig S2)" — S2 는 **60 wt%** (§4 ⛔).

### 5.3 Visualization of Ionic Percolating Networks (p.5 — Fig 4)
- 3 모델: (a) f_CAM=70, D̄_SE=3µm; (b) f_CAM=80, D̄_SE=3µm; (c) f_CAM=80, D̄_SE=5µm (모두 D̄_CAM=5µm). gray=CAM, yellow=SE percolating network(QuickSurf), 우열=active/inactive CAM.
- **(a)→(b):** f_CAM 70→80 wt%(λ 고정 1.67) → SE 부피↓ → **percolating network 작아지고 덜 균일 → θ_CAM 98%→…감소.**
  - ⛔ 보강 2026-09-26 — 원문 값: **θ 98 % → 52 %** (p.5 stated). Fig 3a 판독 (80 wt%, λ 1.67) 은 0.50 · SI Fig S1b (80:15, λ 1.67) 평탄 47–50 % —
    서로 다른 무작위 배치의 값이라 ±2–5 %p 흔들린다 (세 수가 한 조건의 산포를 대신 보여 준다).
- **(b) vs (c):** f_CAM=80 고정, **SE 3µm→5µm(λ 1.67→1)** → **percolating network 더 작아짐** → 활성 CAM 이 separator 근처에만 → **θ_CAM = 52%(b) vs 25%(c)** (큰 SE 가 활성 CAM 절반↓). ⭐ "큰 SE → 작은 percolation network → 적은 활성 CAM."

### 5.4 Experimental Validation (p.5–6 — Fig 5, 6, 핵심 검증)
- **Fig 5a (4 cells, LPS 8/5/3/1.5µm, f_CAM=60 wt%, 5µm NMC, 1st-cycle V-curve):** **8µm·5µm LPS → 작은 용량(~75·~125 mAh/g)** vs **3µm·1.5µm LPS → full(>150 mAh/g)** → "**작은 SE(큰 λ) 이 θ_CAM↑**" 실험증명.
- **Fig 5b (실험 vs 모델 용량, λ=2.5/1.3/0.8/0.6):** 모델 용량 = (155 mAh/g)×θ_CAM(Fig 3c). **good agreement.** λ 2.5(SE 2µm)→full ~155; λ 0.6(SE 8µm)→~80 mAh/g.
  - ⛔ **오독 정정 2026-09-26** — "λ = 2.5 / 1.3 / 0.8 / 0.6" 은 **위쪽 축 눈금** (아래 축 2 / 4 / 6 / 8 µm 눈금의 λ 환산) 이고 데이터 점이 아니다.
    점 = **SE 1.5 / 3 / 5 / 8 µm (λ 3.33 / 1.67 / 1.00 / 0.625)**. 판독 (digitized ±1.5 mAh/g): 실험 **152.3 / 151.4 / 122.8 / 76.1**, 모델 ≈155 / ≈155
    (실험 원 뒤에 가려짐) / **127.9 / 87.3** mAh/g. 모델−실험 차는 SE 8 µm 에서 가장 크다 (+11, 모델 과대).
- **Fig 5c,d (5µm vs 12µm NMC, 3µm·1.5µm LPS, f_CAM=80 wt%):** **12µm CAM(검정) > 5µm CAM 용량** (양 LPS 크기 공통) → **큰 λ 가 θ_CAM 이득** 재확인.
- **Fig 5e (용량 vs CAM 크기 4→12µm):** 3µm SE·1.5µm SE 둘 다 **CAM 클수록 용량↑**, 모델·실험 일치. ⭐ "**큰 CAM = 표면적당 percolating-SE 접촉 확률↑** → θ_CAM↑"(반직관, §4 에서 해설).
  - ⛔ 정정 2026-09-26 — 점은 **CAM 5 · 12 µm 두 개** (스윕 아님). 판독: 3 µm SE (λ 1.67 → 4) 실험 **78.3 → 127.9** · 모델 74.5 → 134.3;
    1.5 µm SE (λ 3.33 → 8) 실험 **96.3 → 141.1** · 모델 111.1 → ≈140 mAh/g. ⇒ 5 µm CAM · 1.5 µm SE 에서 모델이 실험보다 **+15 과대** (80 wt% 전이대).
    "표면적당" → **입자당 표면적** (§3 표 ⛔).
- **Fig 6 (f_CAM=60/70/80 wt% 검증, 3µm·1.5µm LPS, 5µm NMC):** **60·70 wt%(λ≥1.67) 둘 다 고-util 영역(green)** → **용량 거의 동일 >150 mAh/g** → **f_CAM 60→70 wt% 를 용량손실 없이 증가 가능**(특히 1.5µm SE, λ=3.33). **80 wt%(low-θ red/purple 영역) → 급락**. 모델·실험 good agreement(Fig 6b,d).
  - ⛔ **과일반화 정정 2026-09-26** — 원문의 green · "almost identical, > 150" 문장은 **f_CAM = 60 wt% 에 대해서만** 이다 (p.6). 70 wt% 는
    *"a comparison … for f_CAM = 70 wt% … confirms that increasing λ ensures higher θ_CAM"* — 판독: 3 µm LPS (λ 1.67) 실험 **137.6** (모델 153.5) ·
    1.5 µm LPS (λ 3.33) **154.0** (모델 ≈155). 80 wt%: **78.5 · 96.6** (모델 ≈75 · 111.3). 즉 "60 → 70 wt% 무손실" 은 **1.5 µm LPS 에서만**.
    ⚠ 3 µm · 70 wt% 는 모델 (θ ≈ 0.99) 이 실험보다 **+16 mAh/g 과대** — 전이대 바로 앞에서 모델이 낙관적이라는 신호 (derived(ours), 셀 1 개).

### 5.5 Discussion (p.6–8)
- ⭐ **반직관 결과의 물리:** "큰 CAM = 긴 확산경로(불리)지만 **표면적이 커서 percolating SE 망에 접촉할 확률↑** → utilization↑. **액체셀 직관(큰 CAM 나쁨)은 SSB 에 그대로 안 통함.**" "Li percolation 이 율속" 일관.
- **f_CAM=80 wt% ≈ 50 vol%** (이전 보고 밀도·porosity 로 환산, ref [29]). near-full util. = **D̄_CAM 12µm + D̄_SE 1.5µm**. = 액체셀 수준.
- **>80 wt% 가능?** λ 더 키우면(SE sub-µm) 가능 — nano-SE 합성 동향(refs [14,15]) → 더 높은 로딩 동기. ⚠ 단 trade-off: **매우 큰 λ(아주 큰 CAM) = power density↓**(큰 CAM lithiate 느림, ref [24]); **아주 작은 SE = percolation 채널폭↓ + 입계↑ → SE 망 임피던스↑**(ref [30]) + **GB 저항(SE 선택의존)**. ⇒ **power vs energy trade-off 로 λ 최적화.**
- ⭐ ★ **접촉면적·소성변형(우리 MPM/Stage-E 직격):** "**λ 가 이온확산에 미치는 영향의 추가 정밀화는 입자간 *접촉면적* 같은 세부를 요구하며, 접촉면적의 정확한 기술은 *LPS 입자의 소성변형 모델링* 을 필요로 한다 — 이는 실험적으로 관측됐다(ref [29]). 변형 정도가 입자간 접촉면적·따라서 경계저항을 크게 좌우한다.**" → **자기 rigid-Hertz 모델의 한계를 명시 + 우리 MPM(SHAPE 소성)·Stage-E(Tabor 소성면적)·Holm constriction 이 메우는 칸을 *지목*.**
- **carbon(전자) percolation:** CNF 미포함 모델은 **이온 percolation 만** — 5 wt% CNF 가 전자 percolation 담당. "한 최근 연구(ref [13] Strauss): 도전제 없으면 *CAM 자체* 가 전자 percolation 가능" → "**전자 percolation 도 같은 입경효과 적용**"(우리 σ_e size-effect 와 동방향). carbon 추가 모델링은 입자수 10¹⁰ 초과로 계산불가(SuperP nm) → 향후.
  - ⛔ **정정 2026-09-26 — 방향이 반대로 옮겨졌다.** 원문 (p.8): *"without the conductive carbon additive, the electron percolation must be
    provided through CAM only, and becomes the limiting factor … This led to a conclusion that **a smaller CAM particle size provides better
    cathode utilization**, which seemingly contradicts with our results. However, since the electron percolation provided by the CAM particles is
    the limiting factor in this case, **decreasing the CAM particle size improves the electronic percolation** … our model applies to both
    electronic and ionic percolations."* ⇒ 같은 "도체 입자 작게" 규칙이 전자 쪽에서는 **CAM 을 작게** 로 뒤집힌다. 우리 σ_e 의
    "큰 AM 유리" (§A.3) 와 **같은 방향이라는 근거가 아니다** — 오히려 CAM 이 전자 도체일 때 Shi 의 모델은 **작은 CAM 을 편든다**.
    (탄소 도전재가 SE 를 분해한다는 보고 `[33,34]` 때문에 *"carbon nanofibers whose high aspect ratio leads to better percolation at lower volume
    fraction"* 이 선호된다는 문장도 같은 쪽 p.8 — 우리 VGCF 와 **같은 섬유형** 계열이다; 우리 선택 이유와 같다는 뜻은 아니다.)
  - ⛔ 보강 — 출력–에너지 밀도 절충의 원문 결론 (p.7): *"SSBs using cathode materials such as LiCoO₂ with good intrinsic Li mobility may be optimized
    by increasing the cathode particle size, whereas cathode materials with poorer Li-ion transport such as some NMCs may require SE particle size
    reduction"*; 산화물 SE 는 입계저항이 황화물보다 훨씬 커서 SE 를 줄이면 오히려 느려진다 `[31,32]` — 즉 "SE 를 줄여라" 는 **황화물 전제**의 처방이다.

### 5.6 Conclusion (p.8)
- **크기비 λ = D̄_CAM/D̄_SE 가 cold-press SSB 의 utilization·로딩 허용도를 지배** — 모델+실험 공통. **cathode utilization = percolation-controlled.** **큰 λ = 고-CAM 로딩 가능.** 고-로딩 regime 에서 utilization 이 *λ 에 가장 결정적.*
- ⭐ **"큰 CAM(12µm) + 작은 SE(1.5µm) 로 액체셀 수준(50 vol%) CAM 복합양극 제작 가능"** 시연. **SSB 양극 입경 최적화의 정량 가이드** 제공. (oxide SE Li₇La₃Zr₂O₁₂ 등에도 적용 가능 — 단 GB 기여는 SE 선택의존.)
  - ⛔ 2026-09-26 — 괄호 안 LLZO 문장은 결론이 아니라 **§4 (p.8)** 에 있다 (*"since the additional sintering step used in oxide SE processing
    does not dramatically change the SE percolation network morphology"* — 저자의 믿음 서술, 계산·실험 없음). 음극 복합체 (MCMB · Li₄Ti₅O₁₂) 로의 확장도 같은 문단.

---

## S. Supporting Information 전수 정리 (2026-09-26 보강 — SI 8 쪽)

> 원본 `aenm201902881-sup-0001-suppmat.pdf` — 표지 1 쪽 + 본문 7 쪽 (SI 인쇄 쪽번호 1–7 = PDF 2–8 쪽). 아래 "SI p.N" 은 **인쇄 번호**.
> 값 등급: **SI-stated** (SI 에 숫자로 인쇄) · **digitized** (그림 판독, `litdb/figures/<slug>/digitized.csv`) · **derived(ours)** (우리가 계산).

### S.0 SI 구성
| SI 쪽 | 내용 | 크롭 |
|---|---|---|
| p.1 | 제목 · 저자 (Tan Shi† · Qingsong Tu† · Yaosen Tian · Yihan Xiao · Lincoln J. Miara · Olga Kononova · Gerbrand Ceder*) · 소속 a UC Berkeley · b LBNL · c Samsung Research America | — |
| p.2 | §1 *Description of contact force during model compression* — Hertz 힘 식 + **"Table 1"** (시뮬 파라미터) | `tab_S1.png` (tS1) |
| p.3 | §2 *Benchmark tests for numerical convergence* — **Table S2** (PSD 매개변수) + 상자 크기 규칙 | `tab_S2.png` (tS2) |
| p.4 | **Figure S1** — a) 설계 vs 실제 PSD (30 µm 상자) · b) θ vs 상자 길이 (4 모델, 80:15) | `fig_S1.png` (fS1) |
| p.5 | **Figure S2** — θ vs λ, CAM 5 · 12 µm, **60 wt%** | `fig_S2.png` (fS2) |
| p.6 | ★ **Table S3** — LPS 습식 밀링 조건 · 입경 · σ_ion | `tab_S3.png` (tS3) |
| p.7 | 참고문헌 [1]–[4] | — |

### S.1 Hertz 힘 식 + Table S1 (SI p.2 · 인쇄 라벨은 "표 1") — `tab_S1.png`
- 힘 식 (원문 그대로 옮김): `F_ij = √δ · √(R_i R_j /(R_i + R_j)) · [ (k_n δ n_ij − γ_n (v·n_ij) n_ij) + (k_t δ t_ij − γ_t (v·t_ij) t_ij) ]`
  — *"δ is the overlap distance between two particles defined as δ = d − (R_i + R_j), where d is the central distance"* · v = 상대속도.
  = LAMMPS/LIGGGHTS `gran/hertz/history` 꼴 (√δ·√R_eff 곱 = Hertz). **항복 · 소성 · 점착 항 없음.**
- "Table 1" (인쇄 라벨 그대로 "Table 1" — SI 첫 표라 색인은 S1):

  | 기호 | 설명 | SE (LPS) | AM (NMC) |
  |---|---|---|---|
  | E_c (GPa) | Young's modulus | 18.5 [1] | 177.5 [2] |
  | ν | Poisson's ratio | 0.3 [1] | 0.3 [2] |
  | ρ (g/cm³) | Density | 1.87 [3] | 4.85 [2] |
  | γ_t (GPa) | Damping constant | 50 [4] | 25 [4] |
  | σ_y (GPa) | Yield stress | 2 [1] | 12.6 [2] |

  (전부 SI-stated. 캡션: *"Simulation parameters used in the Hertzian contact model"*.)
- 읽는 법 (derived(ours)):
  - **E_SE 18.5 GPa · E_AM 177.5 GPa 무연화** — 우리 DEM E_eff 1.35 (real 24 의 18×↓) 의 **반대편 극단**. 이 침대의 200 MPa 최종 porosity 는 보고되지
    않았다 (n/a) — 우리 틀로는 E 가 floor 를 정하므로 실험 0.1–0.2 보다 성길 공산 (§4 ⛔). 그래도 **λ·로딩 추세**가 실험과 맞았다 = 연결성의
    **순위**는 E 에 둔감할 수 있다는 약한 방증 (정량 검정 아님).
  - **σ_y** 는 표에 있으나 힘 식에 **들어갈 자리가 없다** — 쓰임새 n/a. 값은 **나노압입 경도(H)** 다: AM 의 177.5 / 12.6 은 정본 `xu2017_…` 카드의
    **치밀 소결 NMC532 펠릿 E 177.5 ± 19.5 · H 12.6 ± 1.4 GPa** (Xu 2017 JES, stated) 와 소수점까지 같고, SE 의 2 는 McGrogan LPS **H 1.9 GPa**
    (정본 `so2021_…` 카드 경유, 2차) 와 맞는다. ⚠ Shi 는 AM 값을 `[2]` de Vasconcelos 2016 *EML* 에 다는데, 정본 두 카드 (`xu2017_…` · `sedlatschek2026_…`)
    는 그 EML 을 **이차입자 139 GPa · H 8.9** 로 인용한다 ⇒ **귀속 오류 공산** (EML 원문 미확인 → 판정 보류). 또 펠릿 E 는 이차입자 E (142.5) 의 1.25× 다.
  - **γ_t 의 단위 "GPa"** 는 감쇠상수의 차원과 맞지 않는다 (원문 표기 그대로). γ_n · k_n · k_t · **마찰계수 μ · COR 은 어디에도 없다** (n/a) —
    본문의 *"frictional yield"* (p.2, `[23]` Zhang–Makse) 는 마찰 쿨롱 한계로 읽히지만 μ 값이 없어 재현 불가.
  - ⇒ 이 표로 **재현에 필요한 입력의 절반**만 공개됐다 (E · ν · ρ 는 있고 μ · k · 평판 속도 · 정지 문턱은 없다).

### S.2 상자 크기 수렴 — Table S2 · Fig S1 (SI §2, p.3–4)
- **Table S2** (SI-stated; 전부 log-normal):

  | 재료 | 평균 크기 (µm) | σ (µm) | 최소 직경 (µm) | 최대 직경 (µm) |
  |---|---|---|---|---|
  | CAM | 5 | 1.6 | 3.0 | 10.0 |
  | CAM | 12 | 3.5 | 5.0 | 25.0 |
  | SE | 1.5 | 0.5 | 0.8 | 3.0 |
  | SE | 3 | 1.0 | 2.0 | 6.0 |
  | SE | 5 | 1.5 | 3.2 | 10.0 |
  | SE | 8 | 2.0 | 5.8 | 13.0 |

  (절단 비 max/평균 ≈ 1.6–2.1 — 분포 꼬리가 잘려 있다. 모델 Fig 3b 의 SE 12 · 15 µm 분포는 **표에 없다** — n/a.)
- **Fig S1a**: 30 µm 상자에 채운 세 분포 — 설계 (빨강 점선) 대비 실제 (파랑) 가 **가장 큰 분포에서 어긋난다**; *"This deviation increased as the
  maximal particle size increased"* (SI p.3).
- **Fig S1b**: 4 모델 (CAM-5/SE-1.5 · CAM-5/SE-3 · CAM-12/SE-5 · CAM-12/SE-8), **CAM:SE = 80:15 (= f_CAM 80 wt%)**, 상자 11 개. 가로축 두 줄 —
  CAM-5: 45 … 105 µm · CAM-12: 108 … 252 µm (= 둘 다 **9 … 21 × D̄_CAM**; 점선 ≈ 10 × D̄_CAM). 평탄값 (digitized ±0.3 %p):
  **λ 3.33 (5/1.5) 67.7–69.5 %** · **λ 2.4 (12/5) 58.2–60.8 %** · **λ 1.67 (5/3) 47.1–49.5 %** · **λ 1.5 (12/8) 44.9–47.1 %**.
  작은 상자 (첫 점) 에서는 λ 큰 쪽이 **낮게**, CAM-12/SE-8 은 **높게** 나온다 (44.0 · 54.1 %) — 상자 오차는 부호가 정해져 있지 않다.
  ⚠ 세로축 제목은 인쇄본 **"f_CAM (%)"** 인데 캡션·본문은 *"active cathode ratios"* — 조성이 80:15 로 고정이고 값이 38–70 % 로 움직이므로
  **θ_CAM 의 라벨 오기**로 읽는다.
- 규칙 (SI p.3 = 본문 p.3): *"Large errors were observed for L < 50 µm for the AM-5 µm models and for L < 120 µm for the AM-12 µm models … L_min ≈ 10 D̄_max …
  L_box = 1.5 L_min ≈ 15 D̄_max"*. 수식의 **D̄ (평균)** 가 문턱 50 / 120 µm 와 맞는다 (최대 직경 10 / 25 µm 였다면 100 / 250 µm) — SI 문장의
  *"maximal particle diameter d_max"* 는 느슨한 표현이다. L 은 **압밀 전 초기** 입방 한 변.
- 우리 대비: 판정 지표가 **θ (연결성) 하나** 이고 조성은 80:15 한 점 · 시드 산포 없음. 우리 RVE 의 σ·porosity 수렴 판정 (다른 지표) 을 대신하지 못한다.
  "15 D̄_max" 를 옮길 때는 **우리 기준 D̄ (AM_P 평균 12 µm) × 15 = 180 µm** 급이라는 뜻이 된다 (derived(ours), 우리 상자 크기와의 대조는 하지 않았다).

### S.3 Fig S2 — λ 인가, 절대 크기인가 (SI p.5) — `fig_S2.png`
- 5 µm CAM: λ 0.40 / 0.62 / 0.99 / 1.67 / (3.33) → θ **0.39 / 0.60 / 0.80 / 1.00 / (≈1.00, 가려짐)**; 12 µm CAM: λ 0.42 / 0.63 / 1.00 / 1.67 / 3.33 →
  **0.36 / 0.56 / 0.78 / 0.98 / 0.99** (digitized ±0.003). 같은 λ 에서 차 ≤ 0.035 → *"utilization is controlled by λ rather than by the absolute particle sizes"*.
- ⚠ **f_CAM = 60 wt%** (SI 캡션). 본문은 Fig 3b (70 wt%) 의 확인이라 적는다 — 70 wt% 의 12 µm 결과는 **공개되지 않았다** (n/a).
- 60 wt% 에서도 λ < 1.67 이면 θ < 1 — 즉 "60 wt% 는 λ 무관 full" 이 **아니다** (λ 0.62 에서 0.60). 실험 Fig 5b (60 wt%, SE 8 µm, λ 0.625) 의 반토막 용량과 같은 이야기.

### S.4 ★ Table S3 — SE 습식 밀링 ↔ σ_ion (SI p.6) — `tab_S3.png` — **원장 `SELF-51` 판정 근거**
- 원문 그대로 (SI-stated; *"In all cases, 50-mL ZrO₂ ball-mill jars and Y-stabilized ZrO₂ milling balls were used. Ionic conductivities were determined by
  conducting impedance measurements using In metal as blocking electrodes."*):

  | 평균 크기 (µm) | 밀 | 볼 (mm) | 속도 | 용매 | 시간 (h) | σ_ion (mS cm⁻¹) | ÷ bulk 0.39 (derived) | ÷ 8 µm 0.32 (derived) |
  |---|---|---|---|---|---|---|---|---|
  | 8 | SPEX 8000M | 5 | 1060 cycles/min | heptane | 0.5 | **0.32** | 0.82 | 1.00 |
  | 5 | SPEX 8000M | 3 | 1060 cycles/min | heptane | 1.5 | **0.24** | 0.62 | 0.75 |
  | 3 | Retsch PM200 | 3 and 1 | 300 rpm | heptane + dibutyl ether | 15 | **0.22** | 0.56 | 0.69 |
  | 1.5 | Retsch PM200 | 1 | 300 rpm | heptane + dibutyl ether | **40** | **0.14** | **0.36** | 0.44 |

  기준 bulk LPS 0.39 mS/cm = Li₂S + P₂S₅ 를 SPEX 8000M 에서 **200 min 건식** 볼밀한 합성품 (본문 p.3, *"consistent with previous reports [27]"*) —
  습식 밀링 **전**. 펠릿 성형압 · 두께 · 온도 · 반복수 · 오차는 **보고 없음** (n/a). 입경 = SEM ≈200 입자 평균 (p.3).
- 저자 귀속 (본문 p.3): *"We note that the ionic conductivities of the LPS decrease with smaller particle sizes. This is **likely** because of the increased
  grain boundary (or particle boundary) resistance, which can be worsened by any residual solvent from the wet ball milling process."* — 검증 실험 없음.
  Discussion (p.7) 도 같은 축: *"Reduction of the SE particle size brings … a smaller percolation channel width and an increased number of particle/grain
  boundaries that may increase the impedance within the SE network.[30] … Some oxide SEs show much larger grain boundary resistance compared to the
  sulfide SEs used in the current study"*. **비정질화는 언급하지 않는다** — 재료가 처음부터 **비정질 유리**다.
- **판정표 (SELF-51 질문에 대한 답)**:

  | 질문 | 답 | 근거 등급 |
  |---|---|---|
  | 이 논문에 밀링 시간 ↔ σ 데이터가 있나 | **있다** — Table S3 4 점 (+ 본문 bulk 0.39) | SI-stated (SI p.6) · stated (p.3) |
  | 재료 | **75Li₂S–25P₂S₅ 비정질 유리** (LPS) — argyrodite Li₆PS₅Cl 아님; 밀링 전후 결정도 (XRD) 측정은 **없다** | stated (p.1 · p.3) |
  | "40 h" 조건 | Retsch PM200 · 300 rpm · 1 mm Y-ZrO₂ 볼 · 50 mL 자 · heptane + dibutyl ether (습식) | SI-stated |
  | 40 h 시료의 입경 | **d̄ ≈ 1.5 µm** (r ≈ 0.75 µm) | SI-stated · stated |
  | "1/3" 성립? | **성립** — 0.14 / 0.39 = **0.36** (밀링 전 bulk 기준). 0.5 h 습식 시료 기준이면 0.44 | derived(ours) |
  | Cronau 2022 p.2 문구와 일치? | 뜻은 맞다 — Cronau: *"LWM exceeding 40 h … about 1/3 … increased particle boundary resistances and inclusion of residual solvent"* `[20,25]`. 차이: Shi 는 **정확히 40 h** (exceeding 아님), 행성밀 300 rpm 을 Cronau 가 "LWM" 으로 부른 것 · `[25]` Minnmann 은 10 h ×0.75 라 "1/3" 의 몫은 **Shi 쪽** | SI-stated + 정본 `cronau2022_…` §2-2 · `minnmann2021_…` |
  | σ 저하의 원인을 저자는? | **입자(입계) 경계 저항 증가 + 잔류 용매** ("likely") — 입경에 묶인 기전 + 공정 오염. 밀링 손상 · 비정질화는 **언급하지 않는다** (검증 실험도 없다) | stated (p.3) |
  | 입경 효과를 밀링 효과와 분리할 수 있나 | **없다** — 입경 · 시간 (0.5 → 40 h) · 밀 (SPEX → PM200) · 볼 (5 → 1 mm) · 용매 (heptane → +DBE) 가 **모두 같이** 바뀐 4 점 | derived(ours) |
  | `Cronau(r_SE)` 의 0.33 @ **r ≤ 30 nm** 의 근거가 되나 | **아니다** — Shi 의 최소 입경은 r ≈ 0.75 µm (25× 크다) 이고 sub-µm 데이터가 0 이다. 우리 계수는 r = 0.75 µm 에서 **1.00** — 표를 입경 법칙으로 억지로 읽으면 벌점이 **마이크론 영역**에 떨어져 우리 배치와 **정반대**다 (그러나 교란 때문에 어느 쪽도 교정 못 한다) | derived(ours) |

- ⇒ **결론**: Cronau 2022 가 옮긴 "40 h → 1/3" 은 Shi SI Table S3 에서 **재현된다** (×0.36). 그러나 그것은 **LPS 유리 · d̄ 1.5 µm · 공정 교란된 4 점**의 관측이고,
  우리 코드가 그것을 **r ≤ 30 nm 의 입경 계수 0.33** 으로 둔 것에는 **원문 근거가 없다** (Cronau 2022 에도 없음 — 정본 `cronau2022_…` 카드).
  작업 브랜치 `scripts/run_network_full_corrections.py` 의 docstring (읽기 전용 확인, 2026-09-26) 이 *"r_SE ≤ 30 nm → 0.33 ✓ high (Cronau extreme-milling limit)"* ·
  *"Cronau 2022's 1/3 reduction is at extended ball-milling, primarily affecting D50 < 0.3 μm"* 라 적는데, **"D50 < 0.3 µm" 은 두 원문 어디에도 없다**
  (Shi 1.5 µm · Cronau ≥ ≈1 µm). ⛔ 인용 금지 후보: *"1/3 reduction … D50 < 0.3 µm"* · *"Cronau extreme-milling limit (r ≤ 30 nm)"*.
- 우리에게 남는 쓸모: **공정 이력 인자**의 크기 선례 (습식 밀링 → 펠릿 σ ×0.36–0.82 vs 밀링 전, LPS 유리). 정본의 두 동료값 —
  `cronau2022_…` (gc-Li₅.₅PS₄.₅Cl₁.₅, LWM 50 h → 0.36 / 2.5 = **×0.14**, 본문 stated 값으로 계산) · `minnmann2021_…` (LPSCl, 10 h 습식 **×0.75**) — 과
  함께 "밀링 이력 벌점" 한 축을 이룬다. 재료 · 밀 · 기준점이 다 달라 한 곡선으로 모으지 않는다; 공통 결론은 **입경 함수가 아니라 공정 변수 함수**라는 것
  (`comparison_vs_ours_DEM.md` B 절 [Cronau22] 블록과 같은 결론, 이번에 [Shi20] 블록 추가).

### S.5 SI 참고문헌 (SI p.7, 원 목록 그대로 — 제목 없음)
| # | 서지 (원문) | SI 에서 쓰인 자리 | 정본 카드 |
|---|---|---|---|
| [1] | F. P. McGrogan, T. Swamy, S. R. Bishop, E. Eggleton, L. Porz, X. Chen, Y. Chiang, K. J. Van Vliet, *Advanced Energy Materials.* 2017, 7(12), 1602011. | E_SE 18.5 · ν_SE 0.3 · σ_y,SE 2 | 없음 → `[미확인]` (2차: `famprikis2019_…` E ≈ 20 / G ≈ 7 · `so2021_…` H 1.9) |
| [2] | L. S. de Vasconcelos, R. Xu, J. Li, K. Zhao, *Extreme Mechanics Letters.* 2016, 9, 495-502. | E_AM 177.5 · ν_AM 0.3 · ρ_AM 4.85 · σ_y,AM 12.6 | 없음 → `[미확인]`. ⚠ 177.5 / 12.6 은 정본 `xu2017_…` (Xu 2017 JES) 의 **소결 펠릿 E · H** 와 동일; 이 EML 은 정본 두 카드가 **이차입자 139 · H 8.9** 로 인용 → 귀속 오류 공산 |
| [3] | P. Villars, PAULING FILE in: Inorganic Solid Phases, Springer Materials, Springer Materials. 2012. | ρ_SE 1.87 | 없음 → `[미확인]` |
| [4] | H. Zhang, H. Makse, *Physical Review E.* 2005, 72(1), 011301. | γ_t 50 / 25 (= 본문 [23]) | 없음 → `[미확인]` |

---

## 6. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | (a) 초기 입방→압밀 모식(L_box→두께 T, 200 MPa); (b) **PSD log-normal**(SE 1.5/3/5/8µm + CAM 5/12µm); (c) **CAM 2개의 이온 percolating 경로**(검은 점선, separator 까지) | ⭐ (b) = 우리 12:4:1 직접 비교축; (c) = 우리 percolation 최단경로/f_perc 와 *같은 그림*. 압밀모식 = 우리 DEM 평판압밀과 동일. ⛔ 2026-09-26: 캡션 기호는 "height L" (두께 T 아님); (a) 모델 = f_CAM 80 wt% · D̄_SE = D̄_CAM = 5 µm (λ 1). "평판압밀과 동일" 은 **정압 유지** 차이를 빼고 (§4 ⛔). (b) 세로축 = volume ratio (%), 분포 매개변수 = SI Table S2 |
| **2** | (a–d) LPS SEM 8/5/3/1.5µm + (e,f) LZO-NMC 5/12µm SEM | 실측 PSD 근거; 우리 입력 PSD 의 실험 대응 |
| **3** ★★ | (a) θ_CAM vs f_CAM @λ=1.67; (b) **θ_CAM vs λ @f_CAM=70**; (c) **θ_CAM heatmap(λ×f_CAM)**; (d) **임계 λ vs f_CAM(80/90/98% util.)** | ⭐⭐ **이 논문의 심장.** (b)=고정로딩서 λ↑→util.↑(size=packing); (c)=우리 porosity-조성-크기비 3D 스윕의 *utilization 판*; (d)=**dip 의 조성의존을 λ_min(f_CAM) 로 정량** |
| **4** | 3 모델 percolating SE network 시각화(QuickSurf): (a)70/3µm (b)80/3µm θ=52% (c)80/5µm θ=25% | 큰 SE→작은 network→적은 활성 CAM. = 우리 dead-AM 시각화의 대응(단 그들=이온망, 우리=σ 망) |
| **5** ★ | (a) V-curve 4 LPS크기(60 wt%); (b) **실험 vs 모델 용량(λ)**; (c,d) 5 vs 12µm NMC V-curve; (e) **용량 vs CAM크기(4→12µm) 모델·실험** | ⭐ **frame[4] 실험검증.** (b)(e) = 모델 utilization → 실험 용량 *직접 비교* = 우리 σ→용량 예측의 검증 템플릿. ⛔ 2026-09-26: (b) 위쪽 λ 축 눈금 (2.5/1.3/0.8/0.6) 은 **아래 축 눈금의 환산** — 점은 SE 1.5/3/5/8 µm; (e) 점은 CAM **5 · 12 µm 둘뿐**. 판독값은 §3 표 · digitized.csv. 조건당 셀 1 개 (오차막대 없음) |
| **6** | (a,c) V-curve 60/70/80 wt%(3µm·1.5µm LPS); (b,d) 실험 vs 모델 용량 | f_CAM 60→70 wt% 용량손실 없이 증가(1.5µm SE) — 우리 production-core(70–85 wt%) 상한의 실험. ⛔ 3 µm LPS 는 70 wt% 에서 137.6 (모델 153.5) — "무손실" 은 1.5 µm 만. (d) 가로축 라벨은 "f_CAM (%)" (b 는 wt%) — 원문 그대로 |
| **7** | (a) **CAM vol% loading vs f_CAM(wt%)**, 음영=실험 porosity Φ=0.1–0.2; (b) θ_CAM heatmap(λ×CAM vol%) | ⭐ **wt%↔vol% 환산표(porosity 0.1–0.2 대역)** = 우리 wt%/vol% 매핑 직접 사용. 80 wt%≈50 vol%. ⛔ 2026-09-26: "직접 사용" 불가 — 밀도가 **LPS 유리 1.87 · NMC532 4.85** (SI Table 1) 이고 f_CAM 분모에 **CNF 5 wt%** 가 들어 있다 → 우리 LPSCl · NMC811 · 이원 wt% 로는 다시 계산. ⛔ (b) 세로축 눈금이 **60 · 70 · 80 · 80** (맨 위 중복) 에 제목은 vol% — Fig 3c 의 wt% 눈금 자리와 같고 (a) 로는 80 wt% ≈ 47–59 vol% 라 모순 ⇒ **(b) 세로축 정량 판독 금지** |
| **S1** | (SI p.4) (a) 설계 vs 실제 PSD, 30 µm 상자 — 가장 큰 분포가 어긋남; (b) 4 모델 (CAM-5/SE-1.5 · 5/3 · 12/5 · 12/8, **80:15**) 의 활성 CAM 비 vs 초기 상자 길이 (CAM-5 45–105 µm · CAM-12 108–252 µm, 점선 ≈ 10 D̄_CAM) | ⭐ 상자 규칙 L_min ≈ 10 D̄_max 의 근거 그림. 평탄값이 λ 순서 (3.33 > 2.4 > 1.67 > 1.5) 로 선다 = λ-지배의 **두 번째** 증거. ⚠ 세로축 라벨 "f_CAM (%)" 는 θ 의 오기 (§S.2) |
| **S2** | (SI p.5) θ vs λ — 5 µm · 12 µm CAM 두 계열이 겹친다, **f_CAM 60 wt%** | λ vs 절대 크기 분리의 유일한 직접 증거 (차 ≤ 0.035). ⚠ 본문은 70 wt% (Fig 3b) 의 확인처럼 인용 |
| **Table S1** | (SI p.2, 인쇄 라벨 "Table 1") Hertz 접촉 모델 파라미터: E 18.5/177.5 GPa · ν 0.3/0.3 · ρ 1.87/4.85 · γ_t 50/25 "GPa" · σ_y 2/12.6 GPa | ⭐ 우리 DEM 입력과 직접 대조: E_SE **무연화** (우리 1.35). μ · COR 없음 (§S.1) |
| **Table S2** | (SI p.3) log-normal PSD 매개변수 — 평균 · σ · 최소 · 최대 직경, CAM 5/12 · SE 1.5/3/5/8 µm | 우리 PSD 입력 (12:4:1) 과 분포 폭 비교용 (§S.2) |
| **Table S3** ★★ | (SI p.6) LPS 습식 밀링 조건 (밀 · 볼 · 속도 · 용매 · 시간) ↔ 입경 ↔ σ_ion — 0.32 / 0.24 / 0.22 / 0.14 mS/cm | ★ **원장 SELF-51 판정 근거**: 40 h → 0.14 (= bulk 0.39 의 0.36 ≈ 1/3) 는 **d̄ 1.5 µm · LPS 유리 · 공정 교란** — `Cronau(r_SE)` 0.33 @ r ≤ 30 nm 의 근거가 아니다 (§S.4) |

> 모든 transport 그림이 **utilization(θ_CAM, %) 또는 용량(mAh/g)** — **유효 σ(mS/cm) 곡선 없음.** ⇒ 우리 σ_ionic 0.04–0.18·Bazzoun 0.137 과 *σ 직접 비교 불가*. 비교 가능 = *utilization·percolation·λ-효과·용량 추세*.
> ⛔ 2026-09-26 — 유일한 σ 숫자는 SI Table S3 의 **순수 LPS 펠릿** σ (0.14–0.32, 밀링 전 0.39 mS/cm) 다 — 재료값이지 복합체 σ_eff 가 아니다.
> 크롭 12 장 (본문 7 · SI 5) 은 2026-09-26 에 전부 다시 잘랐다 — 본문 7 장은 옛 PNG 가 256 색 양자화 결함 (열지도 Fig 3c · 7b 색띠 계단화) 이었고
> 캡션 5 개에 본문 문단이 섞여 있었다 (`figures.json` 의 `recrop` · `caption_fix`). SI 표 3 장은 자동 추출이 못 잡아 수동 크롭.

---

## 7. Post-processing ★

- **무엇**:
  - **cathode utilization θ_CAM = V_CAM^active/V_CAM** — 각 CAM 입자가 최단 Li-percolation 경로로 separator(bulk-SE)에 닿으면 active. = **percolation 연결성 → 활성분율**. (우리 **f_AM^cc / dead-AM** 의 정확한 대응 — 단 우리는 σ-가중, 그들은 *존재만*.)
  - **최단경로 percolation**: CAM 노드 그래프 + SE-경계 target → Dijkstra 류 최단경로(ref [26] Zeng–Church) → separator 도달 판정. **저항/전류/전위 없음 — 연결성만.**
  - **모델→용량 환산**: 예측용량 = θ_CAM(모델) × 155 mAh/g(실험 관측 최대) → Fig 5b/d/6b/d 에서 실험과 직접 대조.
  - **box-size 수렴**: L_box=1.5·L_min≈15·D̄_max (SI S2). 전이영역 ≥3 config 평균.
  - **σ_ion(LPS) vs 입경 측정**(재료, Table S3): bulk 0.39 → 작을수록 감소(GB↑). ⇒ utilization↑이 σ_material↑ *아님* 을 증명(packing).
    - ⛔ 2026-09-26 — "증명" 은 과하다. ① Table S3 는 입경 **과** 밀링 공정이 함께 바뀐 4 점 (0.32 → 0.14) 이고 ② 용량은 **0.05 mA cm⁻²** 한 전류에서만 쟀다 —
      이 저율에서는 σ_SE 가 ×0.44 떨어져도 옴 강하가 용량을 거의 못 깎으므로, "σ 가 떨어졌는데 용량이 올랐다" 는 **연결성이 용량을 정하는 영역**
      이라는 것을 보일 뿐 σ 와 packing 의 크기 비교가 아니다 (derived(ours)). 고율에서 두 효과가 어떻게 맞서는지는 **데이터 없음 (n/a)** —
      Cronau 2022 (정본 카드) 가 바로 그 역전 (λ 이득 vs σ 손실 → 2 h 최적) 을 0.6 C 에서 본 논문이다.
  - ⛔ 보강 — **그림 판독 도구 (우리)**: `tools/litdb/shi2019_fig_digitize.py` → `litdb/figures/shi2019_high_am_loading_particle_size_assb/digitized.csv`
    (Fig 3a/3b/3d · 5b/5e · 6b/6d · 7a · S1b · S2, 181 행, stated 값 4 개와 대조 행 포함 — 2.05 vs 2.1 · 0.499 vs 0.52 · 76.1 vs ≈75 · 122.8 vs ≈125).
- **도구**: **LIGGGHTS**(압밀 DEM), 자체 percolation/최단경로 코드, **QuickSurf**(Gaussian SE-surface 시각화, Fig 4), 실험 = SEM(Zeiss Gemini Ultra-55, ~200입자 평균 PSD)·Bio-Logic VMP300.
- **수치화·플롯·기록**: θ_CAM heatmap(λ×f_CAM, Fig 3c·7b), 임계-λ 곡선(Fig 3d), 실험-vs-모델 용량 산점(Fig 5b/e·6b/d), wt%↔vol% 환산(Fig 7a, porosity 음영대 0.1–0.2). **모든 종축 = θ_CAM(%) 또는 용량 — σ 아님.**

---

## 8. 우리 DEM+MPM 대비 → `our_dem_baseline.md`

> ⭐ 이 표가 핵심 — Shi 는 우리와 **같은 코드(LIGGGHTS)·같은 접촉계열(Hertz/탄성)·가장 가까운 소재(황화물+NMC)** 라 *방법-수준 직접 대조*가 가능한 드문 논문.

| 항목 | 이 논문 (Shi 2019/2020) | 우리 | 차이 / 이유 (rigid·plastic / 소재 / 2D·3D / 연결성·σ실값) |
|---|---|---|---|
| **DEM 코드** | ⭐ **LIGGGHTS** (refs 18–20) | **LIGGGHTS** | **동일.** 우리 DEM 방법론의 *직접 동료* (Bazzoun 과 함께) |
| **접촉법칙** | **Hertz** + damping + 마찰 yield, **소성 SHAPE 없음** | **hooke/hysteresis** + adhesion, **소성 SHAPE 없음** | 둘 다 *탄성-접촉 rigid-sphere*(Hertz vs hysteresis 차이만). **둘 다 δ-overlap 프록시, 진짜 흐름 아님** → 우리 18× 연화·그들 무연화(단일압력)는 *같은 rigid 한계* 다른 처리 |
| **DEM 입력 (SI Table S1, 2026-09-26 보강)** | E_SE **18.5** · E_AM **177.5 GPa** · ν 0.3 · ρ 1.87 / 4.85 · γ_t 50 / 25 "GPa" · σ_y 2 / 12.6 GPa; **μ · COR 없음** | E_SE,eff **1.35** (real 24 의 18× 연화) · E_AM 140 (출처 재확인 중 — 원장 `SELF-51`) · ν 0.3 (stoic-knuth CLAUDE.md 기준 — 정본 `our_dem_baseline.md` 는 자리표시) | ⭐ **연화 축의 양 끝.** 그들은 real-E 강체구로 200 MPa 까지 누르고 porosity 를 **보고하지 않는다** — 우리 틀 (E 가 floor 를 정함) 로는 그 침대가 실험보다 성길 공산 (n/a). 같은 코드인데 **입력 철학이 정반대** 라는 것이 이 대조의 핵심 |
| **압밀 프로토콜 (2026-09-26 정정)** | 평판 정속 하강 → 200 MPa → **압력 일정 유지** → 운동에너지 0 (p.2) | DEM: 변위정지 + 이완 (`hold`) · MPM: `servo`(정압) / `hold` 선택 | ⛔ 카드 옛 서술 *"= 우리 hold"* 는 틀렸다 — Shi 는 **정압 (= 우리 servo 쪽)**. 정압 유지 중 재배열이 더 진행될 수 있어 같은 공칭압에서도 최종 기하가 다를 수 있다 (크기 n/a) |
| **입자 모델** | **구, rigid, log-normal bi-disperse** (SE 1.5–8 × CAM 5/12µm, λ 0.6–8) | **구, rigid, bimodal 12:4:1** + 18× 연화 | **거의 같음** — 둘 다 형상 안 변함. 그들 λ-연속스윕 = 우리 이산 12:4:1 의 *연속판* |
| **압밀 압력** | **200 MPa 단일** (separator 100) | **300 MPa**(제조) | 같은 cold-press 계열(약간 낮음). 둘 다 *제조압*(작동압 아님; 그들 작동 5 MPa) |
| **porosity** | **입력/환산 Φ=0.1–0.2**(실험 보고 범위, Fig 7a) | **15.6 %(DEM)/16.7 %(MPM)** real_14 | ⭐ **우리 15.6 % 가 그들 0.1–0.2 대역 *정중앙*** → 같은 자릿수 cross-check. 단 그들 porosity 는 *측정 안 함*(환산용 음영대) → 절대 동일시 금지, *대역 일치*만 |
| **transport** | ⭐ **이온 percolation *연결성*(최단경로 → utilization)** — **σ 실값 없음, constriction 없음, 전자·열 없음** | **Kirchhoff + Holm constriction σ_ionic/e/thermal 삼중항**(실값, LOOCV 0.975/0.953/0.903) | ⭐⭐ **우리가 한 층 위.** 그들 = "CAM 이 연결됐나(active?)"; 우리 = "그래서 σ 가 얼마 + constriction 으로 얼마 깎이나". = 우리 transport novelty 의 *정확한 좌표* |
| **utilization vs dead-AM** | **θ_CAM = V_active/V_CAM**(존재 기준) | **f_AM^cc / dead-AM**(σ-가중 연결분율) | **같은 개념** — 그들 θ_CAM 이 우리 dead-AM 의 *순수 기하 percolation 판*. 우리는 σ·fracture 가중 |
| **접촉면적** | **n/a — "정확기술엔 LPS 소성변형 모델 필요"라 *명시 향후과제*(§4, ref 29)** | **Stage-E Tabor+volume 소성 접촉면적** | ⭐ **그들이 *지목한* 칸을 우리가 채움.** Shi 가 직접 "소성변형이 접촉면적·경계저항 좌우"라 인정 = frame[5] 분업의 *그들 측 인정* |
| **소성/morphology** | **없음**(rigid Hertz) | **MPM 진짜 SHAPE 소성**(SEM 일치)·void-fill·Σdg | morphology = 우리 MPM 고유. 그들 rigid-구 한계를 우리 MPM 이 메움(frame[1]/[2]) |
| **크기비 효과** | ⭐ **λ=D_CAM/D_SE 가 utilization 지배(λ↑→util↑)** — *작은 SE → σ_material↓에도 util↑* | **"size=PACKING not overlap"**(σ_ionic·σ_e size-effect=기하) | ⭐⭐ **결론 *동일*.** Shi 실험: 작은 SE = σ_ion(LPS)*낮아짐* 인데도 utilization↑ → **순수 packing/연결성** = 우리 결론의 *모델+실험 증거* |
| **큰 CAM 효과** | ⭐ **큰 CAM = utilization↑**(표면적당 SE-접촉 확률↑, 반직관) | DEM: 큰 AM = AM-AM 접촉↑·packing(σ_e φ_AM⁴·√A) | **같은 방향** — 큰 CAM 이 percolation 유리. Kang2025 "큰 입자 균열" caveat 과 결합(packing 이득 ↔ 균열 대가) |
| **Furnas dip** | ⭐ **dip 의 *조성의존*을 λ_min(f_CAM) 로 정량**(70→1.67, 75→2.1) | **dip @ AM 70–85 wt%**(de Larrard/McGeary 기하); **소성 MPM 재현 못 함** | ⭐ **상보.** 우리 dip(porosity 최저 조성) ↔ 그들 λ_min(util.=1 유지 한계). **"로딩↑→필요 λ↑"가 우리 dip 의 조성-크기비 결합의 *실험판*** |
| **검증** | ⭐ **실험 4 SE×3 로딩×2 CAM 셀, 모델 용량 good agreement** | solver=ground truth + Bazzoun/Minnmann/Cronau 외부앵커 | ⭐ **Shi = 우리 σ→용량 예측의 *검증 템플릿*** (그들이 직접 모델→용량→실험 닫음) |
| **소재** | **LPS glass(σ 0.39) + NMC532-LZO** | **LPSCl(σ ~1–3) + NMC811** | ⚠ **σ·용량 절대전이 금지.** 둘 다 황화물+층상NMC+cold-press → *추세*만 frame[4] 앵커 |

**핵심 차이 3줄:** (1) ⭐ **같은 LIGGGHTS+Hertz rigid-구로 압밀+percolation 까지는 우리와 *형제*** — 단 그들은 **이온 percolation *연결성*(utilization)** 까지, 우리는 그 위에 **σ 실값(Holm constriction)+삼중항** 을 *solve*; (2) ⭐ **결론이 같다: "작은 SE+큰 CAM(λ↑) → utilization↑"이 우리 "size=PACKING not overlap"의 모델+실험 증거**; (3) ⭐ **그들이 직접 "LPS 소성변형 모델 필요"라 지목한 칸(접촉면적·morphology)을 우리 MPM/Stage-E 가 채움** = frame[5] 분업의 *그들 측 명시 인정*.

> ⛔ **2026-09-26 표 정정 · 신선도 점검** (원 행은 이력으로 둔다):
> - **porosity 행**: Shi 의 Φ 0.1–0.2 는 **모델 입력도 측정도 아니다** — Fig 7a 환산에만 쓴 `[29]` 문헌 대역. DEM 침대 porosity = n/a.
>   우리 쪽 "16.7 % (MPM)" 은 DEM 골격·SE 씨앗을 공유하는 scaffold 값이라 **독립 확인이 아니고** (stoic-knuth CLAUDE.md 2026-09-09 정정 · CDX-16),
>   관례 오프셋 1.251 %p 가 겹쳐 있다 — 이 표에서는 **DEM 15.6 % 만** 쓴다. 대역 일치 (같은 자릿수) 이상의 주장은 없다.
> - **크기비 효과 행**: "순수 packing/연결성 = 우리 결론의 모델+실험 증거" 는 **저율 (0.05 mA cm⁻²) · 연결성 지배 영역**에서만 성립하는 서술이다 (§7 ⛔).
>   그리고 "작은 SE → σ_material↓" 의 σ 저하 (SI Table S3, 0.32 → 0.14) 는 **밀링 공정과 교란**되어 있다 (§S.4).
>   ⚠ 우리 σ_ionic 폼의 `Cronau(r_SE)` 는 원장 `SELF-51` 로 **출처 없는 모델 가정**이 됐고, 이 논문 (Table S3) 도 그 계수의 **근거가 아니다** (§S.4).
>   σ_grain 3.0 은 Cronau 2021 SI Fig S2c 의 **µC-Li₆PS₅Cl 펠릿** 값 (원장 `CL-91`) — 단결정 라벨 금지.
> - **큰 CAM 효과 행**: "표면적당" → **입자당 표면적**; "우리 σ_e 와 같은 방향" 은 Shi 가 **이온** 연결성에 대해서만 한 말이다 — CAM 이 전자 도체일 때
>   Shi 의 모델은 **작은 CAM** 을 편든다 (§5.5 ⛔, ref [13]).
> - **Furnas dip 행**: λ_min 판독 — 80 wt% 에서 θ 80 % ≈ 3.9 · 90 % ≈ 5.9 · 98 % > 8 (§3 표). 곡선은 ≈78 wt% 에서 **수직**이 된다 (문턱 하나).
> - **검증 행**: "4 SE × 3 로딩 × 2 CAM" 은 요인배치가 아니다 — 셀 약 10 개, 조건당 1 개, 오차막대 없음 (§1 ⛔).
> - **우리 쪽 기준값의 지위**: 정본 브랜치의 `our_dem_baseline.md` 는 **값이 0 개인 자리표시**다 (2026-09-09). 이 표의 "우리" 칸은 2026-06-26 당시
>   stoic-knuth CLAUDE.md 에서 옮긴 것이고, 인용하려면 원장 (`claims.json` · CLAUDE.md 최신 블록) 에서 다시 확인해야 한다.

---

## A. 우리 DEM+MPM 대비 (comparison vs ours) — 심층

### A.1 ⭐ "size = PACKING not overlap" — Shi 의 실험이 우리 결론의 *직접 증거*
우리 CLAUDE.md 의 가장 반복되는 결론 중 하나: **σ_ionic·σ_e 의 입경 효과는 *기하 packing*(Furnas) 이지 *overlap*(δ) 이 아니다.**
(예: "Overlap (δ/R ≈ size-scale-invariant at fixed P) can't flip with composition → the size-ordering is geometric Furnas
packing; overlap only sets the absolute level." / Minnmann2021 "fine SE → σ_ion,eff↑ = packing/τ 효과".)

**Shi 가 이걸 *실험으로* 못박는다:**
- Table S3: **작은 LPS 입자 = σ_ion(재료) 가 *낮아짐*** (입계저항↑ + 잔류용매). 즉 *재료* 관점에선 작은 SE 가 불리.
- 그런데 Fig 3b·5a: **작은 SE(큰 λ) = cathode utilization↑ → 용량↑.** ⇒ **utilization 이득은 σ_material 이 아니라 *packing/연결성*(작은 SE 가 CAM 간극을 채워 percolation 망을 촘촘히)** 에서 온다.
- ⭐ **이것이 정확히 우리 결론.** 우리 σ_ionic 의 size-effect 가 Cronau(r_SE) (재료 GB) 와 packing(φ_eff·CN²·cov) *둘 다* 를 담고, **packing 항이 size-ordering 을 지배**한다는 것 — Shi 가 "재료 σ↓ vs utilization↑" 의 *상반 부호* 로 **packing 이 이긴다** 를 실험분리. → **우리 σ_ionic 폼의 size 처리(packing-dominant)의 frame[4] 실험 정당화.**
- ⚠ 단 *방향(부호)* 만 전이: 그들 LPS-glass σ 0.39, 우리 LPSCl ~1–3. 절대 σ·utilization 숫자 전이 금지.
- ⛔ **정정 2026-09-26 (SI 대조) — 이 절은 세 군데서 무너진다. 결론 방향은 살아남지만 "실험분리" 라는 말은 못 쓴다.**
  1. **Table S3 는 입경 단독 효과가 아니다** — 0.32 → 0.24 → 0.22 → 0.14 mS/cm 는 입경 8 → 1.5 µm 와 **밀링 0.5 → 40 h · SPEX → PM200 · 볼 5 → 1 mm ·
     heptane → heptane+DBE** 가 함께 움직인 결과이고, 저자 스스로 원인을 *"likely"* 입자경계 저항 + **잔류 용매** 로 둔다 (§S.4). "재료 관점에서 작은 SE 가
     불리" 는 **공정 관점에서 오래 간 SE 가 불리** 로 읽어야 한다.
  2. **"packing 이 이긴다" 는 크기 비교가 아니다** — 용량은 0.05 mA cm⁻² 한 전류에서만 쟀고, 그 저율에서는 σ_SE ×0.44 의 옴 벌점이 용량을 거의 안 깎는다.
     Shi 가 보인 것은 *"이 조건에서는 연결성이 용량을 정한다"* 이다 — σ_eff 의 packing 몫 vs 재료 몫을 **분리 측정한 것이 아니다**.
  3. **우리 σ_ionic 폼의 "Cronau(r_SE) (재료 GB)" 항은 이 논문으로 정당화되지 않는다** — 원장 `SELF-51`: 그 계수는 **출처 없는 모델 가정**이고 (Cronau 2022 에 구간값 없음),
     Shi 의 유일한 관련 데이터 (Table S3) 는 벌점을 **r ≈ 0.75 µm (d̄ 1.5 µm)** 에 두어 우리 계수 (r ≥ 0.5 µm → 1.00) 와 **자리가 어긋나며** 교란돼 있다.
  ⇒ 쓸 수 있는 문장: *"Shi et al. show, at low rate, that a smaller SE raises cathode utilization even though the milled SE's pellet conductivity is lower
  (SI Table S3, process-confounded) — consistent with a connectivity-limited regime."* — "experimental separation of packing vs material σ" 는 쓰지 않는다.

### A.2 ⭐ 크기비 λ ↔ 우리 12:4:1·Furnas dip — *연속 λ 스윕* vs *이산 크기비*
- **우리:** AM:SE = **12:4:1**(D̄_CAM_P:D̄_CAM_S:D̄_SE ≈ 12µm:4µm:1µm) bimodal → **Furnas dip @ AM 70–85 wt%**(porosity 최저). 우리 표현: "AM_P:SE=12:1(≫7=McGeary 임계, dip 깊음), AM_S:SE=4:1(<7, 부분충전)".
- **Shi:** **λ = D̄_CAM/D̄_SE 연속 스윕(0.6–8)**, **λ_min(full util.) = f(f_CAM)** (70 wt%→1.67, 75→2.1, 80 wt%→매우 큼).
- ⭐ **대응:** 우리 12:4:1 을 λ 로 풀면 **AM_P/SE λ=12, AM_S/SE λ=4** → *둘 다 Shi 의 "λ>1, 좋은 영역"*. 즉 **우리 12:4:1 은 Shi 의 high-utilization 설계와 정합** — 우리 production-core(AM 70–85 wt%)에서 λ=4~12 이면 Shi Fig 3d 의 λ_min(70 wt%=1.67, 75=2.1, 80≈3–8) 을 *충족하거나 상회*. ⇒ **우리 12:4:1·production-core 가 Shi 가 실험증명한 "고-CAM 고-utilization" 영역 안에 있다**(우리 설계의 외부 검증).
- ⭐ **dip 의 조성의존 = Shi 의 λ_min(f_CAM):** 우리 dip 이 *조성에 따라 깊이/위치가 변하는* 이유(AM_P-rich 서 깊고 AM_S-rich 서 얕음)를, Shi 의 **"로딩↑ → 필요 λ↑"**(Fig 3d) 가 *transport 측에서* 보강. 우리 dip = *porosity 최저* 조성, Shi λ_min = *utilization=1 유지* 한계 — **둘은 다른 양**(packing porosity vs ionic 연결성)이지만 *같은 크기비-조성 결합의 두 면*. → **우리 porosity 관계식의 "크기비 항"(McGeary 7:1 기하)에 더해, *utilization 측 λ 항*도 별개로 존재**함을 Shi 가 보임.
- ⚠ **frame[4] 비교 주의:** 우리 dip 은 *기하 porosity*(McGeary/de Larrard, 소성 MPM 재현불가), Shi λ_min 은 *이온 percolation 연결성*. **dip(porosity)↔λ_min(utilization) 직접 등치 금지** — 둘 다 "크기비가 조성에 따라 packing/연결성을 지배"라는 *공통 물리*의 다른 측정.
- ⛔ **정정 2026-09-26 — "우리 production-core 가 Shi 고-util 영역 안" 은 상단에서 성립하지 않는다.** 네 가지를 빠뜨렸다:
  1. **wt% 규약** — Shi 의 f_CAM 은 분모에 **CNF 5 wt%** 를 넣는다 (f = 0.95 · M_CAM /(M_CAM + M_SE)). 우리 이원 AM:SE wt% 를 옮기면
     **70 → 66.5 · 75 → 71.3 · 80 → 76.0 · 82 → 77.9 · 85 → 80.8** (Shi 규약, derived(ours)). 게다가 percolation 은 **부피**로 정해지는데 (p.8)
     밀도가 다르다 (Shi: LPS 유리 1.87 · NMC532 4.85, SI Table 1 — 우리 LPSCl · NMC811 값으로 **다시 환산**해야 한다; 이 카드에서는 안 했다).
  2. **λ_min 의 실제 값** (Fig 3d 판독, Shi 규약 f_CAM): 76 wt% → θ 98 % 에 **2.3** · 77.9 → **≈3.5** (90 % ≈2.9 · 80 % ≈2.3) · 80.8 → 98 %·90 % 는 **λ ≤ 8 로 불가**, 80 % 도 **≈6–8**.
     ⇒ 우리 82:18 은 λ ≥ 3.5 면 들어가지만, **우리 85 wt% 모서리는 Shi 모델에서 λ = 8 로도 90 % 에 못 간다** (85 wt% Shi 규약이면 θ ≈ 20 %, p.5 stated).
  3. **이봉 AM 은 하나의 λ 가 아니다** — Shi 는 CAM 단봉이다. 우리 AM_S/SE = 4 는 77.9 wt% (Shi 규약) 의 98 % 문턱 (≈3.5) 바로 위, 80.8 wt% 의 문턱 (> 8) 아래다;
     AM_P/SE = 12 는 Fig 3d 범위 (λ ≤ 8) **밖**이다. 이봉 혼합의 "유효 λ" 는 Shi 가 정의하지 않았다 (n/a).
  4. **Shi 의 λ_min 은 모델값**이다 — 실험이 확인한 점은 80 wt% · λ 8 (≈91 %) · λ 4 (≈83 %, 12 µm NMC/3 µm LPS) · λ 3.33 (≈62 %) 등 몇 개뿐이고,
     그 침대는 **E 18.5 GPa 무연화 강체구 · porosity 미보고** 다.
  ⇒ 옳은 문장: *"우리 core 의 하단 (≤ 80 wt% 이원, ≈ 76 wt% Shi 규약) 은 Shi 모델의 고-util 영역과 정합하고, 상단 (85 wt%) 은 Shi 모델 기준으로 연결성
  한계 쪽에 있다 — 밀도 환산 전 잠정."*

### A.3 ⭐ "큰 CAM = utilization↑" (반직관) — 우리 σ_e 큰-AM 효과 + Kang2025 균열 caveat
- **Shi (§4):** 큰 CAM 은 *확산경로 길어 불리* 하지만 **표면적이 커서 percolating-SE 망에 접촉할 확률↑ → utilization↑.** "액체셀의 '큰 CAM 나쁨' 직관이 SSB 엔 안 통함."
- **우리 σ_e (Stage 22.5):** σ_e ∝ φ_AM⁴·**√A_AM-AM**·NCM(r) — 큰 AM 은 AM-AM 접촉수·면적↑ → σ_e↑(같은 방향, *전자* 측). Shi 는 *이온* utilization 측에서 같은 "큰 CAM 유리" 를 보임.
  - ⛔ 정정 2026-09-26 — Shi 는 **전자** 쪽에 대해 반대로 말한다: 탄소 없이 CAM 이 전자를 날라야 하면 **작은 CAM 이 유리** (ref [13] Strauss 결과를 자기 모델로
    해석, p.8). 즉 Shi 의 규칙은 "**도체 입자를 작게**" 이고, 이온 쪽에서는 SE 가 · 전자 쪽에서는 CAM 이 그 도체다. 우리 σ_e 폼의 "큰 AM → σ_e↑" 와
    **같은 방향이라는 근거로 Shi 를 쓰면 안 된다** (우리 폼의 입경 항 부호는 우리 코퍼스 적합의 결과 — Shi 와 독립). 또 "표면적당" 이 아니라 **입자당 표면적**.
- ⭐ **단 Kang2025(랩 자체논문) caveat 결합:** Kang 은 **큰 입자(10µm)가 사이클 균열↑**(유지 47.7% vs 67.3%@100cyc, c_Li 구배 ~10×) → **packing/utilization 이득(Shi) ↔ 사이클 균열 대가(Kang)** 의 trade-off. ⇒ **우리 모델은 둘 다 표현해야:** Shi 의 "큰 CAM packing/utilization↑"(우리 σ·porosity packing) + Kang 의 "큰 CAM 균열↑"(우리 Auerbach/fracture-Holm 의 *입경-스케일링* — 큰 AM_P 일수록 fracture↑). Shi(압밀-시점 packing 이득) + Kang(사이클 균열 대가)이 **우리 fracture-aware σ 의 입경-의존을 양방향으로 정의**.

### A.4 ⭐ 그들 "percolation 연결성" vs 우리 "Kirchhoff/Holm σ 실값" — novelty 의 정확한 좌표
Shi 의 transport 는 **Bielefeld 2019 와 같은 *percolation 연결성* 층**: "각 CAM 이 최단경로로 separator 에 닿는가?"(Fig 1c) → utilization.
**저항·전류·전위 없음.** 본문이 직접 인정(§4): "**λ 효과의 추가 정밀화는 입자간 접촉면적 같은 세부를 요구**" — 즉 *연결성*에서 멈췄음을 자인.

우리는 *그 위 한 층* 을 더 간다:
- DEM 접촉망의 **각 SE–SE 접촉을 R=1/(2σ·r_c)(Holm 1967)** 로 환산(r_c = 소성변형 깊이),
- **Kirchhoff Σ(φ_i−φ_j)/R=0** 를 풀어 **σ_eff,ion/e/thermal 실값**,
- **Stage-E(Tabor+volume)** 로 r_c(=접촉면적)를 *소성변형* 으로 재유도 — **Shi 가 "LPS 소성변형 모델 필요"라 지목한 바로 그것.**
- ⇒ **Shi(+Bielefeld 2019) = connectivity / utilization; 우리 = conductivity with constriction physics + 삼중항.** **이게 우리 transport novelty 의 정확한 위치**, 그리고 *같은 Ceder/Janek 계열이 스스로 인정한 빈 칸*(Shi §4 "소성변형 모델 필요" + Bielefeld "constriction=future, Greenwood").
- ⭐ **Bazzoun 2026(같은 LIGGGHTS+LPSCl) = 그 RNM/Holm σ 솔버를 *실제로 추가*** → **Bielefeld 2019(percolation) → Shi 2019(percolation+압밀+실험, 같은 코드) → Bazzoun 2026(RNM/Holm σ) → 우리(σ 삼중항+Stage-E+MPM)** 라는 *field 진화*의 자연스러운 끝.

> 대응 매핑: Shi **θ_CAM(active)** ↔ 우리 **f_AM^cc/dead-AM**; Shi **최단 percolation 경로** ↔ 우리 **f_perc_x/y/z + Dijkstra τ**; Shi **λ=D_CAM/D_SE** ↔ 우리 **r_AM/r_SE 크기비(12:4:1)**; Shi **"접촉면적=소성변형 필요"(미실현)** ↔ 우리 **Stage-E 소성 접촉면적(실현)**.

### A.5 porosity 의 의미 차이 (절대 동일시 금지)
- Shi porosity **Φ=0.1–0.2** = *실험 보고 porosity 의 범위*(Fig 7a 음영대, wt%↔vol% 환산용) — 그들이 *측정/예측한 단일값 아님*.
- 우리 **15.6 %(DEM)/16.7 %(MPM)** = *압밀로 예측/측정한 단일값*.
- ⇒ **우리 15.6 % 가 그들 0.1–0.2 대역 정중앙** = 같은 자릿수 cross-check(LPS-glass·NMC532 ≠ LPSCl·NMC811 이라 *대역 일치* 까지만). **그들 0.1–0.2 ≠ 우리 단일 15.6 %** 동일시 금지. (CSV Block 에 명시.)

---

## B. 적용가능성 (applicability to our LIGGGHTS DEM model)

### B.1 ⭐ frame[4] 외부 실험 앵커 — *utilization·용량 vs 크기비/로딩* (소재-매치 caveat)
Shi 는 **우리가 못 갖던 *모델→실험 닫힌 검증*** 을 제공: **모델 utilization → ×155 mAh/g → 실험 용량과 good agreement**(Fig 5b/e·6b/d).
우리도 σ→용량을 예측하지만 *직접 실험검증이 부족* → **Shi 의 "λ↑→util↑→용량↑" 추세를 우리 σ_ionic·dead-AM·percolation 의 frame[4] 외부 앵커로 채택**:
- **anchor 1 (size=packing):** "작은 SE = σ_material↓ 인데도 utilization↑" → 우리 σ_ionic size-effect 가 *packing-dominant* 임을 실험정당화 (A.1).
- **anchor 2 (λ_min vs 로딩):** **f_CAM 70→1.67, 75→2.1, 80 wt%→≈3–8** (full util.) → 우리 production-core(AM 70–85 wt%)·12:4:1(λ=4–12) 가 *Shi 의 고-util 영역 안* 임을 확인 (A.2).
- **anchor 3 (porosity 대역):** Φ=0.1–0.2 ⊃ 우리 15.6 % → 같은 자릿수 (A.5).
- ⚠ **material-match caveat:** σ·용량 *절대값* 은 LPS-glass(σ 0.39)·NMC532-LZO → **추세/부호만** 전이. 절대 σ 앵커는 LPSCl 쪽 **Minnmann(0.17)·Bazzoun(0.137)·Cronau(3.0)** 소유.
- ⛔ 정정 2026-09-26 — anchor 1 은 **"저율 · 연결성 지배 영역에서 방향 정합"** 으로 격하 (A.1 ⛔ 세 가지). anchor 2 의 "80 wt% → ≈3–8 (full util.)" 은
  판독값 θ 80 % ≈3.9 · 90 % ≈5.9 · **98 % > 8** 로 바꾸고, 우리 wt% 는 **CNF 규약 (×0.95) · 밀도** 환산 뒤에만 겹쳐 본다 — 상단 85 wt% 는 영역 **밖** (A.2 ⛔).
  anchor 3 의 Φ 0.1–0.2 는 Shi 의 측정이 아니라 `[29]` 의 문헌 대역. "Cronau(3.0)" 은 Cronau **2021** SI Fig S2c 의 µC-Li₆PS₅Cl **펠릿** 값
  (원장 `CL-91`; 단결정 아님).
- ⭐ **새 앵커 (SI 보강으로 생김)**: ① SI Table 1 = **같은 코드의 real-E 입력 선례** (E_SE 18.5 · E_AM 177.5 GPa) — 우리 연화 (1.35) 와 나란히 놓고
  "같은 LIGGGHTS 인데 입력 철학이 반대" 를 보일 때 인용 가능 (값은 SI-stated, 원전 [1][2] 미확인). ② SI Table S3 = **습식 밀링 이력 벌점의 선례**
  (LPS 유리 ×0.36–0.82) — `Cronau(r_SE)` 를 입경 함수에서 **공정 변수 함수**로 바꿀지 논의할 때의 자료 (1저자 결정 사항, §S.4).

### B.2 우리 composition/size predictor 로의 매핑
| 우리 predictor 입력/출력 | Shi 대응 | 인용/적용 |
|---|---|---|
| **크기비 r_AM/r_SE (12:4:1)** | **λ = D̄_CAM/D̄_SE (0.6–8)** | 우리 12:4:1 = λ 4·12 → Shi 고-util 영역. 우리 size-스윕의 *연속 λ* 외부맵. ⛔ 모델 λ 범위는 0.33–8 (λ 12 는 Shi 그림 밖) · 이봉 AM 의 유효 λ 미정의 · 상단 조성에서는 영역 밖 (A.2 ⛔) |
| **dead-AM / f_AM^cc** | **θ_CAM utilization** | Shi θ_CAM(λ,f_CAM) heatmap = 우리 dead-AM(조성,크기비)의 실험검증 trend. ⛔ heatmap 은 **모델** (실험 검증점은 약 10 셀); 그 침대는 E 18.5 GPa 무연화 · porosity 미보고 |
| **σ_ionic size-effect (packing)** | **작은 SE→util↑ (σ_material↓에도)** | A.1 — packing-dominant 실험 정당화. ⛔ 격하 — 저율 · 연결성 지배 영역의 방향 정합 (A.1 ⛔). `Cronau(r_SE)` 근거 아님 (§S.4) |
| **production-core AM 70–85 wt%** | **f_CAM 60→70 wt% 용량손실 0**(1.5µm SE, Fig 6) | 우리 core 상한의 실험; 70 wt% 안전, 80 wt% 는 λ≥3 필요. ⛔ 2026-09-26: **"80 wt% 는 λ≥3" 은 틀렸다** — 80 wt% · λ 3.33 (5 µm NMC / 1.5 µm LPS) 실험은 **96.6 mAh/g (≈62 %)**, near-full (≈91 %) 은 **λ 8** 에서만 (Fig 5e). 70 wt% 무손실도 1.5 µm LPS (λ 3.33) 만 (3 µm 는 137.6) |
| **wt% ↔ vol% 환산** | **Fig 7a (Φ=0.1–0.2 음영대)** | 우리 wt%/vol% 매핑에 직접 사용(80 wt%≈50 vol%). ⛔ 직접 사용 불가 — LPS 유리 1.87 · NMC532 4.85 g cm⁻³ 밀도 (SI Table 1) + CNF 5 wt% 규약. 우리 소재로 재계산할 것 |
| **Furnas dip 조성의존** | **λ_min = f(f_CAM) (Fig 3d)** | dip 의 조성-크기비 결합의 *utilization 측* 대응(직접 등치 금지) |
| **Stage-E 소성 접촉면적** | **§4 "LPS 소성변형 모델 필요"(미실현)** | 그들이 지목, 우리가 실현 → novelty 인용 |

### B.3 ⭐ 우리 모델이 Shi 에 *더하는* 것 (그들 빈 칸 = 우리 novelty)
1. **σ 실값 + Holm constriction** (그들=percolation 연결성/utilization 만, σ 없음).
2. **삼중항(σ_ionic+σ_e+σ_thermal)** (그들=이온 percolation 만; 전자는 CNF 가 담당하나 *모델 미포함*, 열 전무).
3. **Stage-E 소성 접촉면적** — *그들이 직접 "필요하다"고 지목한* 칸(§4, ref 29).
4. **MPM 진짜 SHAPE 소성·void-fill·morphology** (그들=rigid Hertz).
5. **fracture-aware**(Auerbach/Holm) — Shi packing 이득 + Kang 균열 대가의 입경-스케일링.
6. **Furnas dip 의 *porosity* 정량**(de Larrard/McGeary) — Shi 는 utilization-λ 만, porosity-dip 미측정.
7. **solver→scaling-law LOOCV→predictor**(연속 예측 함수) — Shi 는 이산 스윕.

---

## C. ★ frame[4] 위치 (experimental anchor) — 실험은 *경쟁* 아니라 *앵커*

> frame[4]: DEM·MPM 은 각각 *실험에* 보정(서로가 아님). Shi 는 **실험(+같은-코드 DEM)** 이므로 우리 SIMULATION 의 *경쟁자가 아니라
> 외부 검증 앵커*. 우리 시뮬은 *그들이 실험한 packing/utilization 을 σ 로 예측하고, 그들이 못 한 σ-실값·소성·삼중항을 추가*.

- **Shi = 실험 앵커:** 모델(같은 LIGGGHTS) + **실험 셀**(4 SE×3 로딩×2 CAM)로 **"λ↑ → utilization↑ → 용량↑"** 을 *측정*. 이건 우리 σ_ionic·dead-AM·percolation·size=packing 결론이 *맞아야 할 실험 trend*.
- **우리 SIMULATION 이 더하는 것:** Shi 가 *utilization(연결성)* 까지면, 우리는 그 위에 **(i) σ_eff 실값(Kirchhoff/Holm constriction), (ii) σ_e+σ_thermal 삼중항, (iii) Stage-E 소성 접촉면적(=Shi 가 지목한 칸), (iv) MPM SHAPE 소성 morphology, (v) fracture, (vi) porosity-dip 정량, (vii) predictor 연속함수.** ⇒ **우리는 Shi 가 실험한 packing/utilization 을 *σ 로 정량 예측* 하고, 그들이 명시적으로 비운 칸을 채운다.**
- ⚠ **transferability caveat (반드시 병기):**
  - **소재:** SE = **LPS glass(σ_ion 0.39 mS/cm)** ≠ LPSCl(~1–3, ~3–8×↑); CAM = **NMC532-LZO** ≠ NMC811. → **σ·용량 절대값 전이 금지**, *크기비-utilization-packing 추세*만.
  - **transport 깊이:** 그들 = **연결성(percolation 존재/최단경로)** ; 우리 = **σ 실값**. → utilization↔σ *직접 수치 비교 불가*(우리 σ_ionic 0.04–0.18 ↔ 그들 θ_CAM% 는 *다른 양*).
  - **rigid-sphere:** 둘 다 소성 SHAPE 없음 — *packing/연결성 추세*는 공유하나, *소성 morphology·접촉면적 절대값*은 둘 다 없음(우리 MPM/Stage-E 가 우리 측에서 보강).
  - **porosity:** 그들 Φ=0.1–0.2 = *환산용 대역* ≠ 우리 측정 15.6 % → *대역 일치*만.
  - **압력:** 그들 200 MPa(제조)·5 MPa(작동) vs 우리 300 MPa(제조). 제조압 계열 동일, 절대 동일시 주의.
  - ⛔ (2026-09-26 추가) **DEM 입력·프로토콜:** 그들 E_SE **18.5 GPa 무연화** · 200 MPa **정압 유지** (SI Table 1 · 본문 p.2) vs 우리 E_eff 1.35 연화 · 변위정지 —
    "같은 코드" 이지만 **같은 모델이 아니다**. 그들의 DEM porosity 는 보고되지 않았으므로 두 침대의 기하를 맞춰 볼 방법이 없다.
- **포지셔닝 한 줄:** "Shi 2019/2020 (Ceder, same LIGGGHTS + Hertz, NMC+LPS) experimentally + computationally proves that the particle
  size ratio λ=D_CAM/D_SE — not absolute loading — governs cathode utilization (small SE + large CAM → >50 vol% CAM at near-full
  capacity). This is the direct model+experiment anchor for our 'size = packing, not overlap' conclusion and our 12:4:1 / AM 70–85 wt%
  production core. We add what they explicitly defer (§4, 'accurate contact area requires modelling plastic deformation of LPS'): the
  Kirchhoff/Holm constriction-resistance *conductivity* solve (full ionic/electronic/thermal triad), Stage-E plastic contact area,
  and MPM plastic morphology."
- ⛔ 정정 2026-09-26 — 포지셔닝 한 줄의 *"— not absolute loading —"* 는 원문과 반대 (*"depends as much on the cathode volume fraction as on … λ"*),
  *"direct model+experiment anchor for our 'size = packing' … and our 12:4:1 / AM 70–85 wt% production core"* 는 A.1 · A.2 ⛔ 로 약화된다.
  수정판: *"Shi et al. (same LIGGGHTS + Hertz, NMC532 + LPS glass, unsoftened E_SE 18.5 GPa) show by modelling and low-rate experiments that cathode
  utilization is controlled jointly by CAM loading and the size ratio λ = D̄_CAM/D̄_SE, with λ the decisive lever at high loading (≈50 vol% CAM at ≈91 %
  of the maximum capacity with λ ≈ 8). We add what they explicitly defer (§4) …"* (이하 동일).

---

## 9. 적용 인사이트 (내 연구에 어떻게)

- ① ⭐ **"size=packing not overlap"의 frame[4] 실험 앵커 확보:** Shi Table S3(작은 SE=σ_material↓) + Fig 3b/5a(작은 SE=utilization↑) = **재료 σ↓ 인데도 utilization↑** → packing 이 σ-material 을 이김. 우리 σ_ionic·σ_e 의 *packing-dominant size 처리* 를 paper/deck 에서 이 *상반-부호 실험분리* 로 정당화(이중 결론: 우리 결론 + Shi 실험).
- ② ⭐ **우리 12:4:1·production-core 가 Shi 고-util 영역 안:** λ_min(70→1.67, 75→2.1, 80 wt%→≈3–8) vs 우리 λ=4–12(12:4:1) → **우리 설계가 Shi 가 실험증명한 "고-CAM 고-utilization" regime 충족.** 우리 composition/size predictor 의 *외부 sanity-check*.
- ③ ⭐ **dip 의 조성의존 = Shi λ_min(f_CAM):** 우리 Furnas dip(porosity, McGeary 7:1 기하) 에 더해 **utilization 측 λ_min 항** 이 별개로 존재 — "로딩↑→필요 λ↑"(Fig 3d) 를 우리 porosity-조성-크기비 결합의 *transport 보강* 으로 인용(직접 등치 금지). 우리 porosity 관계식 = E-stiffness 항(Varkey) + 기하 크기비 항(McGeary) + *utilization-λ 항*(Shi).
- ④ ⭐ **"큰 CAM 유리 ↔ 균열 대가" trade-off:** Shi(큰 CAM=packing/utilization↑) + Kang2025(큰 CAM=사이클 균열↑) → **우리 fracture-aware σ 의 입경-스케일링**(큰 AM_P 일수록 Auerbach fracture↑)을 *양방향*으로 정의. 큰 CAM 의 power-density 한계(ref 24)도 우리 설계제약에 기록.
- ⑤ ⭐ **그들이 *지목한* 칸을 우리가 채움(§4):** Shi 가 "정확한 접촉면적엔 LPS 소성변형 모델 필요"라 *자인* → **우리 MPM(SHAPE 소성)+Stage-E(Tabor 소성면적)+Holm constriction** 이 *그 칸*. **frame[5] 분업의 *그들 측 명시 인정*** 으로 우리 novelty positioning 강화(Varkey "구=타협" + Bielefeld "constriction=future" + Shi "소성변형 필요" = 3편이 *같은 빈 칸*을 지목).
- ⑥ **wt%↔vol% 환산(Fig 7a, Φ=0.1–0.2):** **80 wt%≈50 vol%** 등 우리 wt%/vol% 매핑에 직접 사용. 우리 production-core(AM 70–85 wt%) = CAM ~45–55 vol%.
- ⛔ **2026-09-26 SI 보강 후 고쳐 쓴 적용 인사이트** (① ② ⑥ 은 위 문장 그대로 쓰지 말 것):
  - ①′ "상반-부호 실험분리" → **저율 · 연결성 지배 영역에서 방향 정합** 까지만 (Table S3 공정 교란 · 0.05 mA cm⁻² 단일 전류, A.1 ⛔).
  - ②′ production-core 는 **하단만** Shi 모델 고-util 영역과 정합 (CNF 규약 ×0.95 · 밀도 재환산 전 잠정). 85 wt% 모서리는 λ 8 로도 90 % 에 못 간다 (A.2 ⛔).
  - ⑥′ Fig 7a 는 LPS 유리 · NMC532 밀도 + CNF 5 wt% 규약 — "우리 core = CAM 45–55 vol%" 는 **Shi 밀도로 계산한 값**이다 (Fig 7a 판독: 70 wt% → 37–46 · 85 wt% → 54–67 vol%;
    이원 → Shi 규약 ×0.95 를 먼저 적용하면 더 낮아진다). 우리 소재로 다시 계산해야 한다.
  - ⑦ (신설) **real-E 대조**: 같은 LIGGGHTS 가 E_SE 18.5 GPa (무연화) 로 돈 선례 — 우리 18× 연화 논증 (frame[2]) 의 대척점. 그들이 porosity 를
    **보고하지 않았다**는 사실 자체가 논점: real-E 강체구로는 porosity 를 실험에 맞출 수 없어서 **연결성 순위만** 썼을 공산 (derived(ours) 해석, 저자 진술 아님).
  - ⑧ (신설) **SELF-51**: `Cronau(r_SE)` 의 "1/3" 계보가 이 논문 SI Table S3 로 닫혔다 — 값은 재현 (×0.36) 되나 **d̄ 1.5 µm · 공정 교란** 이라 r ≤ 30 nm 배치는
    근거가 없다 (§S.4). 폼을 바꿀지는 1저자 결정 (동결 규약과 충돌).

---

## 10. 인용 가능 문장 (deck/paper용)

- "Using the same LIGGGHTS DEM and Hertzian contact as ours, Shi et al. (Ceder group, Adv. Energy Mater. 2020) demonstrate — by
  both modeling and experiment, in an NMC+LPS composite — that the *particle size ratio* λ = D̄_CAM/D̄_SE, not the absolute cathode
  loading, governs cathode utilization: keeping the SE smaller than the CAM (λ>1) lifts utilization from ~20 % to ~100 % at fixed
  loading and enables >50 vol% CAM (liquid-cell level) by simple mixing and pressing."
- "Shi's result that *smaller SE particles raise utilization even though their intrinsic σ_ion decreases* (Table S3) is the direct
  experimental evidence for our conclusion that the size effect on σ_ionic/σ_e is geometric *packing/connectivity*, not contact
  *overlap* — packing wins over the material-σ penalty."
- "Their full-utilization threshold λ_min(f_CAM) (1.67 at 70 wt%, 2.1 at 75 wt%) places our 12:4:1 design (λ = 4–12) and AM 70–85 wt%
  production core squarely inside the experimentally-validated high-utilization regime."
- "Shi's model resolves transport only to ionic-percolation *connectivity* (utilization via shortest path), and the paper explicitly
  states that an accurate description of inter-particle contact area 'requires modelling the plastic deformation of LPS particles'
  (§4). Our Kirchhoff/Holm constriction-resistance conductivity solve, Stage-E plastic contact area, and MPM plastic morphology fill
  exactly that deferred gap — the same gap the Janek group's Bielefeld 2019 (constriction = future work, Greenwood 1966) also names."
- ⛔ **2026-09-26 — 위 1–3 번째 문장은 그대로 쓰지 말 것.** 1번: *"not the absolute cathode loading"* 는 원문과 반대 (*"as much"*); *">50 vol%"* 는
  초록 표현 (*"over 50 vol%"*) 이지만 본문 §4 · 결론은 **≈50 vol%** 이고 Fig 7a 대역은 47–53 vol% (Φ 0.2–0.1, digitized) 라 "over" 는 Φ < 0.15 에서만 선다.
  2번: *"intrinsic σ_ion decreases"* 는 공정 교란된 펠릿 σ 이고 (SI Table S3), *"direct experimental evidence … packing wins"* 는 저율 한 점의 방향 정합이다.
  3번: 70 wt% 의 1.67 은 이산 표본점, *"squarely inside"* 는 상단 (85 wt%) 에서 거짓, *"experimentally-validated"* 는 λ_min 곡선이 **모델**이라 과하다.
  대체 문장 (원문·SI 로 확인한 범위):
  - "Shi et al. (Adv. Energy Mater. 2020, 10, 1902881), using LIGGGHTS with Hertzian contact and unsoftened moduli (E_SE = 18.5 GPa, E_CAM = 177.5 GPa;
    SI Table 1), find that cathode utilization in cold-pressed NMC532–LPS composites depends as much on CAM loading as on the size ratio λ = D̄_CAM/D̄_SE,
    and that at high loading λ is the decisive lever: ≈50 vol% CAM reached ≈91 % of the maximum observed capacity with λ ≈ 8 (12 µm NMC, 1.5 µm LPS)."
  - "In their low-rate (0.05 mA cm⁻²) cells, smaller LPS raised the first-cycle capacity even though the wet-milled LPS pellet conductivity fell from 0.32 to
    0.14 mS cm⁻¹ (SI Table S3; milling time, mill and solvent co-varied) — consistent with connectivity-limited utilization, not a measured separation of
    packing and material effects."
  - (SELF-51) "The '≈1/3' conductivity loss after ~40 h of wet milling quoted by Cronau et al. (2022) traces to Shi et al., SI Table S3: amorphous 75Li₂S–25P₂S₅,
    40 h planetary wet milling, d̄ ≈ 1.5 µm, 0.14 vs 0.39 mS cm⁻¹ (×0.36), attributed by the authors to particle-boundary resistance and residual solvent."

---

## 11. 주의/한계 (over-claim 방지)

- **σ 절대 비교 *불가*.** 이 논문은 **유효 σ 를 *안 푼다*** — 이온 percolation *연결성*(최단경로 → utilization θ_CAM)·용량(mAh/g)까지. 우리 σ_ionic 0.04–0.18·Bazzoun 0.137 과 *수치 직접 비교 금지*(utilization% 와 σ 는 *다른 양*). 비교 가능 = *λ-효과·utilization·percolation·용량·porosity-대역 추세*.
- **소재 절대전이 금지.** SE = **LPS glass(75Li₂S·25P₂S₅, σ_ion 0.39 mS/cm)** ≠ 우리 **LPSCl(σ ~1–3)**; CAM = **NMC532-LZO** ≠ **NMC811**. → σ·용량 절대값 끌어오기 금지. 우리 소재계 절대 σ 는 Minnmann/Bazzoun/Cronau/Lee 소유. *추세/부호만* frame[4].
- **rigid-sphere + Hertz, 소성 SHAPE 없음.** 우리 DEM 과 *같은 rigid-구 한계* — δ-overlap·Hertz 중첩은 소성 프록시지 *진짜 흐름 아님*. 단일압력 200 MPa(Heckel·압밀곡선·연화 없음). 우리 18× 연화·MPM 소성이 우리 측에서 보강(그들엔 없음). **그들이 직접 "LPS 소성변형 모델 필요"라 자인**(§4) — rigid-Hertz 의 접촉면적 한계를 *논문이 인정*.
- **transport = *연결성*(존재) 까지.** constriction/contact 저항 없음(Bielefeld 2019 와 같은 층). 전자 percolation 은 *CNF 가 담당하나 모델 미포함*; σ_thermal 전무. ⇒ 우리 삼중항·Holm·Stage-E 가 더하는 칸.
- **porosity = 환산용 대역(Φ=0.1–0.2), 측정/예측 단일값 아님.** Fig 7a 음영대 = *실험 보고 porosity 범위*(ref 29). 우리 15.6 % 와 *대역 일치*만(같은 자릿수); **단일값 동일시 금지.**
- **utilization vs porosity-dip 직접 등치 금지.** Shi λ_min(utilization=1 유지) ≠ 우리 Furnas dip(porosity 최저, 기하). 둘 다 "크기비-조성 결합"의 *다른 면*(이온 연결성 vs 기하 packing). 소성 MPM 이 우리 dip 못 재현하는 frame[4] 논점과 별개 — Shi 의 λ-utilization 은 *연결성* 이라 *우리 dip(porosity)* 와 다른 양.
- **digitized vs stated:** λ_min(1.67/2.1)·θ 정의·f_CAM 임계(70/75/80 wt%)·porosity 대역(0.1–0.2)·λ 범위·PSD·box 규칙·80 wt%≈50 vol% = 모두 *본문 stated*. Fig 5/6 의 *용량 정확값*(75/125/150/155 mAh/g 등)·Fig 5e CAM-크기 곡선 = *digitized 추세*(±). CSV 에 source_type 으로 구분.
  - ⛔ 정정 2026-09-26 — **≈75 · 125 · > 150 · 155 mAh/g 는 본문 stated** 다 (p.5). digitized 는 Fig 5b/5e/6b/6d 의 개별 점 (digitized.csv, ±1.5 mAh/g).
    PSD 의 σ · 절단값 · SE 밀링 σ · DEM 입력 = **SI-stated** (Table S2 · S3 · "Table 1"). λ_min 80 wt% 값 · Fig 3a 곡선 · Fig 7a vol% · S1b 평탄 · S2 = **digitized**.
    "λ 범위 0.6–8" 은 **실험** 범위이고 모델은 0.33–8.
- ⛔ **추가 한계 (SI 보강 2026-09-26)**:
  - **DEM porosity 미보고** — E_SE 18.5 GPa 무연화 강체구 침대의 연결성이고, 그 침대가 실험 Φ 0.1–0.2 에 맞는지는 알 수 없다 (n/a).
  - **재현 불가 입력** — μ · COR · k_n · k_t · 평판 속도 · 정지 문턱 · "이웃" 판정 기준이 없다. σ_y 는 표에만 있고 쓰임새가 없다.
  - **통계** — 조건당 ≥ 3 배치 평균이라 적었지만 어느 그림에도 산포가 없다; 실험은 조건당 셀 1 개 · 첫 사이클 · 0.05 mA cm⁻² 한 전류.
  - **본문 ↔ SI 불일치** — 밀링 방법 (본문 "PM200 + heptane/DBE, 볼 1–10 mm" ↔ SI: 8 · 5 µm 는 SPEX + heptane, 볼 ≤ 5 mm) · Fig S2 조성 (본문 문맥 70 wt% ↔ SI 60 wt%) ·
    Fig S1b 세로축 라벨 (f_CAM ↔ θ) · Fig 7b 세로축 눈금 (60/70/80/80 "vol%").
  - **SE 밀링 σ 의 교란** — 입경 효과로 인용 금지 (§S.4). 특히 우리 `Cronau(r_SE)` 의 출처로 쓰지 말 것.
- **2D/3D:** 그들 모델은 **3D**(우리 DEM·MPM-3D 와 동일 차원) — 2D-3D caveat 은 우리 MPM-2D 챔피언에만 해당, Shi 비교엔 무관(둘 다 3D).
- **CNF/바인더 morphology 없음.** 도전제 5 wt% CNF = prefactor 0.95 로만 — 우리 CBD(VGCF/PTFE) morphology·σ-블로킹(Lee2025·Bielefeld2020) 효과 없음. *전자 percolation 정량* 은 우리(+그 논문들) 소유.

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
