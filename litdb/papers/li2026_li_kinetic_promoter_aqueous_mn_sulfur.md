<!-- digest 표준 양식 (paper-level STANDALONE) · 깊이 기준 = zuo2022_chlorination_cathode_interface.md
     2026-09-27 신규 — 1저자(= 우리 DFT 기준선 트랙의 1저자) 요청: "새로 들어온 논문들인데 dft 위주로 논문 에이전트 해줘".
     ⇒ 이 digest 의 무게중심 = §4(계산 방법 전수 + 용매 모델 판정) · §5.1–5.5(DFT 결과 그림 실독) · §6("kinetic promoter" 주장 사슬 판정) · §7(우리 대조 · 0923 Li–S 세 편과 황 전환 계산 방식 비교).
     ⚠ 이 논문은 **수계(물) 전지**다 — 황화물 SE 물성 4축과 수치로 섞지 않는다 (comparison_vs_ours.md 에서도 §J-48 방법 원전 + §K-13 수계 축 연결로만 둔다).
     ⚠ 메인 세션이 두 에이전트 작업을 모아 한 번에 커밋한다 — 이 digest 작성 시점에는 커밋하지 않았다. -->

# Activating Aqueous Multivalent Metal–Sulfur Electrochemistry via Kinetic Promoter — Li, …, Fan\*, Zhao, Chao\* (*J. Am. Chem. Soc.* **2026**, ASAP)

> slug `li2026_li_kinetic_promoter_aqueous_mn_sulfur` · DOI `10.1021/jacs.6c14441` · type `mixed — exp 주(수계 전기화학 · operando 분광 · EQCM · ICP) + 계산 보조(VASP-PBE CI-NEB 1쌍 · VASP PBE-D3 클러스터 S–S 결합길이/ICOHP/PDOS · Gaussian M06-2X/def2-TZVP/SMD 착물 결합에너지 · GROMACS 고전 MD) — 전환 반응 ΔG 도표 0 · S–S 절단 전이상태 0 · Bader 0` · PDF `litdb/inbox/0927-1. JACS_2026_Li_Li_kinetic_promoter_aqueous_multivalent_Mn-S_MAIN.pdf` (본문 11 pp) + `0927-1. Sup) JACS_2026_Li_Li_kinetic_promoter_aqueous_Mn-S_SI.pdf` (SI 25 pp · Fig S1–S27 · Table S1) · digested `2026-09-27` · status ✅ · 태그 **[외부 · 수계]**

> elements: S, Li, Mn, Cl, O, H, Zn, Ni
> methods: DFT, MD, NEB, ICOHP, LOBSTER, PDOS, XPS, Raman

> **저자**: **Xinran Li** (Fudan + NTU), Tengsheng Zhang, Qitong Ye (NTU), Jin-Lin Yang (NTU), Yanyan Zhang, Xiaoyu Yu, Hongrun Jin, Junwei Zhang, Zhuo Yang, Zefang Yang, Yifeng Wang, Wanhai Zhou, **Hong Jin Fan\*** (NTU School of Physical and Mathematical Sciences), Dongyuan Zhao, **Dongliang Chao\*** (Fudan University Laboratory of Advanced Materials · Aqueous Battery Center, 상하이) · 접수 **2026-07-17** · 수정 2026-09-09 · 수락 **2026-09-10** · *J. Am. Chem. Soc.* ASAP (권·쪽 미배정, "XXXX, XXX, XXX−XXX") · 국가중점연구개발 2024YFE0101100 · NSFC U24A2060 / 22688201 / 22279023 / 22309031 외 · 방사광 BSRF 4B7A·4B9A · SSRF BL16U1·BL02U2 · **계산 자원(HPC) 사사 없음** · 데이터: *"available from the corresponding author upon reasonable request"* ⇒ **구조 파일 미공개**
>
> **대조 문서**: `comparison_vs_ours.md` Ref key `[Li26MnS]` · **§J-48** (방법 원전 — 네 계산 판정 · 황 전환 계산 방식 비교 · 가져올 것 · 금지) · **§K-13** (수계 축 스코핑 카드 C5/C7 연결) · 같은 "결합 서술자 → 장벽 추론" 형식의 짝: `[Liu26Sn]`(§J-46)
>
> **계보** (확인 안 함 — 인용 목록에서만): 같은 그룹의 선행 **Mn²⁺–S 수계 전지** — ref 12 (X. Li, T. Zhang, … *Joule* 9, 101930 (2025), *"A Mn²⁺-S redox electrochemistry for energetic aqueous manganese ion battery"*) · 수계 황 전지 총설 ref 2 (J. Liu … D. Chao … *JACS* 143, 15475 (2021)) · ref 3 (X. Yu … D. Chao, *Adv. Mater.* 2026) · 수계 알칼리 이온–황 실패 분석 ref 32 (X. Yu … *Angew.* 2025) · water-in-salt Li–S 원조 ref 28 (C. Yang, L. Suo, … *PNAS* 114, 6197 (2017)).

> **본 digest 에서 실제로 본 그림 (2026-09-27)** — **8장** (+ PDF 원본 확대 4회 · 픽셀 판독 2회): `Fig. 4`(+ `Fig. 4d` 클러스터 모델 700 dpi 확대 · `Fig. 4f` NEB 도식 확대 · `Fig. 4c` 막대·`Fig. 4g` 마커 픽셀 판독) · `Fig. S25` · `Fig. S8`(+ c·d 패널 확대) · `Fig. 2`(+ `Fig. 2c` XPS · `Fig. 2d` SXRD 확대) · `Fig. 5` · `Fig. 3` · `Fig. S10` · `Fig. S9`.
> **안 본 것 (24장)**: `Fig. 1`(셀 성능 — 값은 본문) · `Fig. S1`–`Fig. S7`(첫 사이클 곡선 · 고로딩 · 풀셀 · Zn‖S · 전해질 사진 · 전도도/Raman/UV · EPR) · `Fig. S11`–`Fig. S24`(침전 XRD · 폴리설파이드 UV · 세척액 UV · SEM/TEM · LiCl 농도 스윕 · ChCl 대조 · UV 셀 · DEMS · EQCM 보조 · 자가방전 · GITT · EIS/DRT) · `Fig. S26` · `Fig. S27`(Ni·Zn 장기 사이클 + XANES). 표 `Table S1`(MD 조성)은 PDF 텍스트로 읽었다(이미지로 안 봄).
> 그림에서만 읽은 값 = **`figure-read ≈`** · 그림 속 인쇄 글자 = **"인쇄값"** · 본문 = 쪽 번호 **p.A–K** (JACS 쪽 문자, PDF 1–11 쪽) · SI = **SI p.n**.

---

## 0. 이 digest 를 읽는 법 — 사용자 요청 축 (DFT 위주)

이 논문은 **수계 황 전지 실험 논문에 계산 네 종을 얹은 형태**다: ① Gaussian 착물 결합에너지 ② VASP 진공 클러스터의 S–S 결합길이·ICOHP·PDOS ③ VASP 벌크 MnS CI-NEB ④ GROMACS 고전 MD. **황 전환 반응 자체**(단계별 ΔG · 속도결정단계 · S–S 절단/MnS 핵생성 전이상태)는 **하나도 계산하지 않았다.** 우리가 가져올 것은 값이 아니라 **보고량 설계의 반례 몇 개와 검산 형식 하나**다.

**먼저 박아 둘 판정 여섯** (근거는 각 절):

| # | 판정 | 절 |
|---|---|---|
| ① | **초록의 *"lowers the redox barrier"* · 결론의 *"promotes their cleavage"* 의 장벽은 계산되지 않았다.** DFT 근거는 **정적 S–S 결합길이·ICOHP**(진공 클러스터 · 모델당 단일 배치)뿐이고, 계산된 유일한 장벽(CI-NEB)은 **벌크 MnS 속 Li/Mn 이동**이다 — 전환 반응이 아니다. ΔG 도표·RDS·전이상태 **0건**. `[Liu26Sn]` 과 **같은 "결합 서술자 → 장벽" 추론 형식** | §6 |
| ② | **S–S 약화의 방향이 1M20L 에서 정해지지 않는다.** LiCl₄ 옆은 약화(인쇄값 **2.19 Å · −1.99 eV**)지만, 논문 MD 가 1M20L 의 Mn 종이라 한 **Mn(H₂O)₃Cl₃ 옆은 강화**(**1.94 Å · −3.69 eV**; 완전 수화 Mn(H₂O)₆ 옆 2.08 Å · −2.72 eV 대비). 두 종이 공존하는 1M20L 의 **순효과는 계산되지 않았다** | §5.3 |
| ③ | **NEB 는 "고상 우세 전환"을 오히려 설명하기 어렵게 만든다.** `figure-read ≈` **Li 0.97 · Mn 1.19 eV** — Li 가 낮은 것은 맞지만, 절대값이면 **15 A g⁻¹ 방전(≈4 분) 동안 Li 가 ≈0.1 번 홉한다**(ν₀ = 10¹³ s⁻¹ 가정 · 우리 산수). 고율 용량은 벌크 확산이 아니라 **계면·나노·비정질·액상 경로**에서 와야 한다 — 논문은 이 긴장을 다루지 않는다 | §5.5 |
| ④ | **PDOS 서술("밴드갭이 좁아진다")이 그림과 어긋난다** — `Fig. S25` 세 곡선 모두 **E_F 에서 spin-up PDOS 가 0 이 아니다** = 어느 모델에도 갭이 안 보인다. 에너지 격자 ≈0.2 eV · 궤도(3p) 분해 없음 | §5.4 |
| ⑤ | **착물 결합에너지의 "Li⁺ 는 탈용매화가 쉽다"는 정규화에 달려 있다** — 총량으로는 LiCl₄ ≈1.78 < Mn(H₂O)₆ ≈1.83 eV(**차 0.05 eV**, `figure-read`), 리간드당으로는 **LiCl₄ ≈0.45 ≈ Mn(H₂O)₃Cl₃ ≈0.44 eV**(우리 산수). Mn²⁺(d⁵) **전하·멀티플리시티 미기재** · LiCl₄ 종을 고른 근거가 **MD 에 없다**(Li 배위 미보고) | §5.2 |
| ⑥ | **용매 처리 층위가 계산마다 다르다** — Gaussian 착물 = SMD(물) · VASP 클러스터(S–S·PDOS) = **진공** · NEB = 벌크 결정 · MD = 명시적 SPC/E. **전위·pH 처리(CHE·정전위) 0.** 수계 계면을 말하는 핵심 계산(S–S 약화)이 **용매 없이** 돌았다 | §4d |

---

## 1. 한 줄 요약

수계 황 전지에서 Mn²⁺ 는 황 종을 MnS/MnS₂ 로 붙잡아 용해를 막지만 반응이 느리다. 1 m MnCl₂ 에 **LiCl 20 m** 을 넣으면(**1M20L**) S@AC 양극이 **15 A g⁻¹ 에서 1012 mAh g⁻¹**(S 질량 기준), **5 A g⁻¹ 200 사이클 동안 >900 mAh g⁻¹** 를 낸다. 저자들은 이를 **"Li⁺ = kinetic promoter"**(긴 사슬 황 종의 S–S 를 약화시키고 빨리 움직이는 보조 양이온) + **"Mn²⁺ = 앵커"**(Mn–S 고체 골격)의 분업으로 설명하고, 방전 생성물을 ICP **겉보기 평균 조성 Li₄Mn₆S₈** 의 Li–Mn–S 고상으로 본다. **실험 쪽 "고상 우세 전환" 증거(in situ UV-vis · EQCM · ToF-SIMS · 자가방전)는 서로 일관되지만, DFT 는 정적 결합 서술자 · 착물 결합에너지 · 벌크 NEB 뿐이라 "장벽을 낮춘다" 는 핵심 주장을 직접 계산하지 않았고, NEB 절대값은 오히려 벌크 고상 수송으로는 고율을 설명하기 어렵다는 쪽을 가리킨다.**

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 풀려는 문제 | 수계 황 전지(SAB)에서 전이금속 이온(Mn²⁺ · Zn²⁺ · Ni²⁺)은 황 중간체를 난용성 황화물로 가둬 셔틀을 막지만, **강한 수화 · 높은 탈용매화 장벽**으로 반응이 느리다 = **안정화 ↔ 속도의 상충** (p.A). 기존 전이금속 SAB 는 <2 A g⁻¹ · 고율에서 <500 mAh g⁻¹ (p.B, ref 27) |
| 기존 전략 (저자 요약) | 산화환원 매개체(I⁻/I₃⁻ · Fe(CN)₆⁴⁻/³⁻) · 공용매·고농도 전해질 · 촉매/극성 호스트 (p.A) |
| 제안 | **Li⁺ 를 "kinetic promoter" 로** 더해 Li⁺/M²⁺ 이중 양이온 황 전환계를 만든다 — M²⁺ 는 단쇄 황을 고정, Li⁺ 는 "local fast participant" (p.B) |
| 전해질 | 1M · 1M1L · 1M5L · 1M10L · 1M15L · **1M20L** = 1 m MnCl₂ + 0/1/5/10/15/**20 m** LiCl · 1M25L 은 용해도 한계 확인용(흰 침전) · 대조 **20L**(20 m LiCl) = "Li⁺-S", **1M** = "Mn²⁺-S" (SI p.2) |
| 일반화 | 1 m NiCl₂ (+20 m LiCl) · 1 m ZnCl₂ (+20 m LiCl) (SI p.3) · ChCl 대조(1 m MnCl₂ + 10 m LiCl + 10 m ChCl / + 20 m ChCl) = 고농도·Cl⁻-rich 만으로는 재현 안 됨 (p.E, `Fig. S17`) |
| 셀 | 3전극 Swagelok · S@AC 작업극(S:AC = 1:1 용융확산 155 °C 10 h · S@AC:KB:PTFE = 5:4:1 · Ti 메시) · AC 상대극(≈40 mg cm⁻²) · **Ag/AgCl 기준** · 전해질 200 µL · 황 로딩 1–2 mg cm⁻²(고로딩 3–5) · 용량·전류는 **S 질량 기준** (SI p.2–3) |
| 대조 시스템 | Li⁺-S(20L) · Mn²⁺-S(1M) · Li⁺/Mn²⁺-S(1M20L) 셋을 전 실험에서 나란히 |

---

## 3. 핵심 수치 총정리 ★

### 3a. 계산 수치 (전부) ★★

> ⚠ **이 논문에 없는 계산 양** (전부 0건): 황 환원 **단계별 반응 자유에너지(ΔG 도표)** · 속도결정단계 · **S–S 절단 / Li₂S·MnS 핵생성·분해 전이상태** · 폴리설파이드 흡착에너지 · Bader/전하 이동 · HOMO/LUMO · 전하밀도차 · ELF · 전위 의존(CHE/정전위) 에너지.

| 양 | 값 | 출처 | 비고 |
|---|---|---|---|
| 착물 결합에너지 \|E_b\| — **LiCl₄** | `figure-read ≈` **1.78 eV** | `Fig. 4c` (막대에 숫자 없음 · y축 *"Binding energy (−eV)"*) | 픽셀 보정 ±0.02 eV (눈금 0/2/4 eV). Gaussian M06-2X/def2-TZVP/SMD · 전하(형식상 3−)·멀티플리시티 미기재 |
| 〃 — **Mn(H₂O)₆** | `figure-read ≈` **1.83 eV** | `Fig. 4c` | 형식 2+ · Mn²⁺ d⁵ — 스핀 상태 미기재 |
| 〃 — Mn(H₂O)₅Cl | `figure-read ≈` 2.18 eV | `Fig. 4c` (구조 그림만 있고 캡션·본문에 이름 없음 — 그림에서 O₅Cl 로 읽음) | 형식 1+ |
| 〃 — Mn(H₂O)₄Cl₂ | `figure-read ≈` 2.48 eV | `Fig. 4c` (그림에서 O₄Cl₂) | 형식 0 |
| 〃 — **Mn(H₂O)₃Cl₃** | `figure-read ≈` **2.63 eV** | `Fig. 4c` | 형식 1− |
| 우리 산수 — 리간드당 | LiCl₄ **0.445** · Mn(H₂O)₆ **0.305** · O₅Cl 0.363 · O₄Cl₂ 0.413 · Mn(H₂O)₃Cl₃ **0.438 eV/리간드** | 위 값 ÷ 리간드 수 | ⚠ **총량 서열(LiCl₄ 최저)이 리간드당으로는 사라진다** — LiCl₄ ≈ Mn(H₂O)₃Cl₃ (§5.2) |
| **S1–S2 결합길이** — MnS₄ + Mn(H₂O)₆ / + Mn(H₂O)₃Cl₃ / + LiCl₄ | **2.08 / 1.94 / 2.19 Å** | `Fig. 4d` 인쇄값 | VASP PBE-D3 · 500 eV · Γ · 진공 클러스터 · 모델당 단일 배치 |
| **S1–S2 ICOHP** — 같은 순 | **−2.72 / −3.69 / −1.99 eV** | `Fig. 4e` 인쇄값 (본문엔 숫자 없음) | LOBSTER · 기저·밴드 수·spilling·적분 창 미기재 |
| 우리 산수 — ICOHP 대 결합길이 | 세 쌍의 기울기 **6.9 / 6.8 / 6.6 eV Å⁻¹** (Mn(H₂O)₆–Mn(H₂O)₃Cl₃ · LiCl₄–Mn(H₂O)₃Cl₃ · LiCl₄–Mn(H₂O)₆) | 인쇄값에서 | 세 점이 **거의 한 직선** = ICOHP 가 결합길이 이상의 정보를 주지 않는다 (§5.3) |
| 우리 산수 — 변화량 | LiCl₄ vs Mn(H₂O)₆: **+0.11 Å · ICOHP 크기 −27 %** / LiCl₄ vs Mn(H₂O)₃Cl₃: +0.25 Å · −46 % / **Mn(H₂O)₃Cl₃ vs Mn(H₂O)₆: −0.14 Å · +36 % (강화)** | 인쇄값에서 | 논문은 마지막 줄(강화)을 논의하지 않는다 |
| S 원자 PDOS (스핀 분해) — E_F 에서 | `figure-read ≈` spin-up **0.4–0.8 states eV⁻¹ (세 모델 모두 0 이 아님)** · spin-down ≈0 | `Fig. S25` (−5 ~ +5 eV) | 에너지 격자 `figure-read ≈`0.2 eV · 세 곡선의 E_F 값 서열은 선 굵기·잡음 수준이라 **확정 불가** |
| **CI-NEB 장벽 — Li** (벌크 MnS) | `figure-read ≈` **0.97 eV** (이미지 2) · 이미지 1/3 ≈0.48 / 0.48 eV | `Fig. 4g` (마커 픽셀 판독 ±0.01 eV · 눈금 0.0–1.6) | 이미지 0–4 = **중간 이미지 3개** · 대칭 경로 · 끝점 에너지 같음 |
| **CI-NEB 장벽 — Mn** (같은 경로) | `figure-read ≈` **1.19 eV** · 이미지 1/3 ≈0.64 / 0.64 eV | `Fig. 4g` | Mn 스플라인이 이미지 4 직전 `figure-read ≈` **−0.02 eV** 로 0 아래 = 보간 overshoot |
| 우리 산수 — 장벽 차 → 속도 | ΔE‡ ≈ 0.22 eV → 298 K 홉 속도비 **≈5×10³** (같은 ν₀ 가정) | 위 값 | 본문 서술("lower migration barrier")은 이 **상대차**까지만 뒷받침한다 |
| 우리 산수 — 절대 홉 수 | Γ_Li = 10¹³ · exp(−0.97/0.02569) ≈ **4×10⁻⁴ s⁻¹** → 15 A g⁻¹ 방전 시간 1012/15000 h ≈ **243 s** 동안 **≈0.1 홉** (Mn ≈2×10⁻⁵ 홉) · 243 s 에 10 홉(≈1 nm 급)이 되려면 **E‡ ≲ 0.85 eV** (ν₀ = 10¹² 이면 ≲0.79 eV) | ν₀ 10¹³ s⁻¹ · 298 K 가정 | §5.5 · §6 |
| MD — Mn–Cl 배위수 (1M / 1M20L) | `figure-read ≈` **≈0.4 / ≈2.7** · 중간 농도 곡선 ≈1.9 (⚠ 한 범례 항목에 파란 점선이 두 색조로 보여 **색 배정 불확실**) | `Fig. S8c` (확대) | 첫 봉우리 `figure-read ≈` 2.45 Å(1M) · 2.53 Å(1M20L) |
| MD — Mn–O 배위수 (1M / 1M10L / 1M20L) | `figure-read ≈` **≈5.5 / ≈4.0 / ≈3.3** | `Fig. S8d` (확대) | 첫 봉우리 `figure-read ≈`2.16 Å · 우리 산수 Mn–Cl + Mn–O ≈ **6.0**(1M20L) · ≈5.9(1M) = 팔면체 유지 |

### 3b. 전해질 · MD 조성 (`Table S1` — PDF 텍스트)

| 계 | Mn | Cl | H₂O | Li | 우리 산수 — 몰랄 농도 검산 |
|---|---|---|---|---|---|
| 1M | 70 | 140 | 3890 | — | Mn 70/(3890 × 0.018015 kg) = **1.00 m** ✓ · Cl = 2 Mn ✓ |
| 1M1L | 70 | 210 | 3890 | 70 | Li 1.00 m ✓ · Cl = 140 + 70 ✓ |
| 1M10L | 56 | 672 | 3111 | 560 | Mn 1.00 · Li **9.99 m** ✓ · Cl = 112 + 560 ✓ |
| 1M20L | 50 | 1100 | 2778 | 1000 | Mn 1.00 · Li **19.98 m** ✓ · Cl = 100 + 1000 ✓ · **물 2.78 개 / Li** |

- 계산 조성은 정확하다. ⚠ **20L(LiCl 단독) · 1M5L · 1M15L 은 MD 가 없다** → Mn 없이 Li 가 어떻게 배위되는지 비교할 수 없다. ⚠ **Li–O · Li–Cl RDF 는 어디에도 없다** (§5.1).
- 물리량 (본문): LiCl 이 늘수록 점도 ↑ · 이온전도도는 고농도에서 약간 ↓ (`Fig. S6a` — 안 봄, 값 없음) · O–H Raman 3성분(강 H결합 ≈3230 · 약 ≈3450 · 비H결합 ≈3600 cm⁻¹, SI p.9) · EPR: 1 m MnCl₂ 6선 초미세분리(I = 5/2, 고스핀 Mn²⁺) → 10·20 m LiCl 에서 **g ≈ 2.00 단일 넓은 선** = Mn²⁺ 사이 교환결합(Mn–Cl 클러스터·이온쌍) (p.C–D, `Fig. S7` — 안 봄) · UV-vis: Mn–O 띠 감쇠 + Mn–Cl 띠 출현 (`Fig. S6d` — 안 봄).

### 3c. 생성물 · 분광 (DFT 모델이 무엇이어야 하는지를 정하는 쪽)

| 양 | 값 | 출처 |
|---|---|---|
| in situ Raman | S₈ **153 · 219 · 473 cm⁻¹** → 황화물 **610 cm⁻¹** (가역) | p.D · `Fig. 2a` |
| 방전 생성물 Raman | 표준 MnS `figure-read ≈`**640 cm⁻¹**(날카로움) vs Li⁺/Mn²⁺-S 생성물 `figure-read ≈`**605 cm⁻¹**(넓고 약함, S/N 낮음) | `Fig. 2b` |
| XPS S 2p 기준선 (`Fig. 2c` 점선) | `figure-read ≈` S₈ **164.3** · MnS₂ **162.85** · MnS **162.0** · Li_xMn_yS **160.5 eV** | `Fig. 2c` (확대 판독, 눈금 168–160 eV) |
| XPS D100 성분 | `figure-read ≈` **160.6 / 161.6 eV 이중선이 지배** + 작은 MnS 성분 | `Fig. 2c` |
| XPS 표준 시료 | **Li₂S 160 · Li₂S₂ 161.8 · MnS 162 eV** (인쇄값) · ⚠ "표준 Li₂S" 스펙트럼은 **Li₂S₂ 성분이 Li₂S 성분보다 크다** (+ ≈167 eV 산화 황) = 기준 시료가 일부 산화됨 · MnS 표준에도 ≈169–170 eV 산화 황 | `Fig. S10` |
| S K-edge XANES | 본문: *"the absorption edge of the discharge product sits between those of **pristine Li₂S and MnS**"* (p.D) — ⚠ **그림에는 순수 표준 시료가 없다**: 방전된 전극 셋(Li⁺-S · Mn²⁺-S · Li⁺/Mn²⁺-S)뿐이고 Li⁺/Mn²⁺-S 곡선은 **Mn²⁺-S 와 거의 겹친다**(흡수단 `figure-read ≈` +0.2–0.3 eV 차) · Li⁺-S 전극은 `figure-read ≈`**2482.7 eV 에 거대한 황산염 백색선** | `Fig. S9a` |
| SXRD (λ = 0.6887 Å) | 기준 MnS(PDF#89-4089) 막대 `figure-read ≈` (100) **11.37°** · (002) **12.18°** · (101) **12.87°** · D50 (002) 12.18° → **D100 (002) 12.08°** (Δ ≈ −0.10°) · (100)·(101) 고정 | `Fig. 2d` (확대) · p.D |
| 우리 산수 — (002) 이동 | d(002) 3.246 → 3.273 Å = **c ≈ +0.8 %** | λ + `figure-read` 2θ |
| SXRD 고각 | (110) `figure-read ≈` 19.74°(D25) → 19.65°(D50·D100) · (103) ≈21.65° → ≈21.54° — ⚠ **(110) 은 순수 a축 반사**라 D25→D50 사이 **a ≈ +0.45 % (우리 산수)** 도 늘었다 — 본문 *"(100)·(101) stationary"* 는 D50→D100 구간 이야기다 | `Fig. S9b` |
| TEM 격자간격 | **0.299 / 0.341 / 0.322 nm = γ-MnS (101) / (100) / (002)** · SI: *"slight lattice expansion"* | SI p.16 (`Fig. S15` — 안 봄) |
| 우리 산수 — TEM vs 기준 | `Fig. 2d` 기준 막대에서 환산한 d = (100) ≈3.48 · (002) ≈3.25 · (101) ≈3.07 Å → TEM 3.41 / 3.22 / 2.99 Å 는 **−2.0 / −0.9 / −2.6 %** (판독 ±0.05° ≈ ±0.4 %) = **팽창 방향이 아니다** · SI 는 기준 d 를 제시하지 않는다 | §10-⑧ |
| 침전 대조 | 0.1 m Li₂S + MnCl₂ → **분홍 침전 = MnS**(PDF#89-4089) · S²⁻ 흡수(본문 **240 nm** · 그림 `figure-read ≈`**230 nm**) 소멸 · 1 m MnCl₂ 에서 폴리설파이드·황화물 거의 전부 제거(르샤틀리에) · S₄²⁻ 는 MnS₄ 부분 용해로 덜 잡힘 | p.D · `Fig. 2e` · `Fig. S11`·`Fig. S12`(안 봄) |
| ICP — 한 사이클 (Li : Mn 비율) | `figure-read ≈` Mn **100 → 89 → 80 → 60 %**(방전 말 = "Li₄Mn₆S₈" 라벨) → 충전 87 → 92 → 92 % | `Fig. 2f` |
| ICP — 방전 전극 1–4 사이클 | `figure-read ≈` Li **56 / 47 / 40 / 40 %** · Mn 44 / 53 / 60.5 / 60.5 % → 3 사이클 뒤 안정 | `Fig. 2g` · p.D |
| **겉보기 평균 조성** | **Li₄Mn₆S₈** — *"This formula describes the average elemental ratio of the discharged product"* (p.D) | ICP |
| 우리 산수 — 조성 | Li 4(+1) + Mn 6(+2) = +16 = S 8(−2) ✓ ⇒ **2 Li₂S + 6 MnS 와 같은 조성** · Li/(Li+Mn) = **0.40** | §10-⑧ |
| 세척액 UV-vis | 두 사이클 여러 상태 전극을 탈이온수로 세척 → 황화물·폴리설파이드 흡수 **없음** | p.D · `Fig. S13`(안 봄) |

### 3d. 속도론 · 계면 실험

| 양 | Li⁺-S (20L) | Mn²⁺-S (1M) | **Li⁺/Mn²⁺-S (1M20L)** | 출처 |
|---|---|---|---|---|
| 확산저항 R_d — SoD 0 % | `figure-read ≈` 163 Ω | ≈**464 Ω** | ≈142 Ω | `Fig. 4a` (in situ EIS + DRT) |
| R_d — SoD ≈40 % | ≈16 Ω | ≈94 Ω | ≈76 Ω | `Fig. 4a` |
| R_d — SoD 100 % | ≈21 Ω | ≈50 Ω | ≈42 Ω | `Fig. 4a` |
| 정상상태 CA | — | 느린 응답 · 더 큰 과전압 | **−0.3 ~ −0.6 V (vs Ag/AgCl) "고활성 영역"** — 전위 계단마다 전류가 빨리 평탄 · 더 큼 | `Fig. 4b` · p.G (y축 *"Current (a.u.)"* — **정량 비교 불가**) |
| in situ UV-vis | S²⁻/S₂²⁻ 강하게 지속 = 액상 경로 | S₄²⁻(≈360 nm) 초기 출현 후 소멸 = 고–액–고 | 폴리설파이드 봉우리 **강하게 억제**, S₄²⁻ 확대 삽화에서만 약하게 | `Fig. 3a–c` (곡선이 수직 오프셋 · a.u.) |
| EQCM Δm/ΔQ 이론 한계 | **Li-only 72 ng mC⁻¹** · **Mn-only ≈285 ng mC⁻¹** | | | p.F · SI p.20 |
| EQCM 실측 | — | Δm 이 사이클마다 줄어 `figure-read ≈`**−9 ~ −10 ng**(4 사이클) = 순 질량 손실 | **30 ng / 0.13 mC** − 공전극 배경 1.08 ng = **28.92 ng** → **≈222 ng mC⁻¹** → n_Li ≈ **3.94×10⁻¹⁰** · n_Mn ≈ **4.77×10⁻¹⁰ mol** = **Li : Mn ≈ 45 : 55** | `Fig. 3e,f` · SI p.20 |
| 우리 산수 — EQCM 검산 | Q/F = 1.347×10⁻⁹ mol e⁻ 에 두 식(Q = 2F·n_Mn + F·n_Li · Δm = M_Mn·n_Mn + M_Li·n_Li)을 풀면 3.94 / 4.77 ×10⁻¹⁰ mol · Li 45.2 % ✓ (논문과 일치) · ICP 방전 말 40 % 와 **대략 일치** | | | — |
| 자가방전 24 h (CE) | **< 10 %** | **< 10 %** | **> 90 %** | p.G · `Fig. S21`(안 봄) |
| DEMS H₂S | — | — | 한 사이클 동안 **거의 없음** | p.F · `Fig. S19`(안 봄) |
| ToF-SIMS 깊이 (0–100 s 스퍼터) | — | `figure-read ≈` S⁻ 5×10⁴ · **HS⁻ 5×10²** · S₂⁻ 3×10¹ counts · 지도 희박·불균일 | S⁻ 1×10⁵ · **HS⁻ 2×10⁴** · S₂⁻ 7×10² · 지도 조밀·균일 | `Fig. 3g,h` |
| 우리 산수 — ToF-SIMS 비 | | | S⁻ **≈2×** · S₂⁻ **≈20×** · **HS⁻ ≈40×** (Li⁺/Mn²⁺ 쪽이 큼) — ⚠ **HS⁻ 40× 는 본문이 언급하지 않는다** (§10-⑩) | |
| GITT | 방전 초기 급강하(가용성 생성물 → 구조 붕괴) · 충전 회복 제한 | 분극 큼 · 과전압이 줄다 늘어남(고–액–고) | 전 구간 가장 안정 | p.G · `Fig. S22`(안 봄) · 펄스 0.5 A g⁻¹ 1 min + 휴지 60 min |

### 3e. 셀 성능 (`Fig. 1` 은 안 봤다 — 전부 본문 값)

| 조건 | 값 | 출처 |
|---|---|---|
| 율속 (0.5 → 15 A g⁻¹) | Li⁺/Mn²⁺-S 가 전 구간 최고 · **15 A g⁻¹ 에서 1012 mAh g⁻¹** · 단일 이온계의 **3배 이상** | p.A · p.B (`Fig. 1c`) |
| 우리 산수 — 15 A g⁻¹ | 방전 시간 ≈**4.0 min** · S 이론용량 2F/M_S ≈ **1672 mAh g⁻¹** 대비 **≈61 %** | — |
| 사이클 (5 A g⁻¹) | **>900 mAh g⁻¹ · 200 cyc · CE ≈100 %** · 단일 이온계는 10 cyc 안에 급감 | p.C (`Fig. 1d`) |
| 풀셀 S‖LiMn₂O₄ | 방전 평탄 **0.9 V** · **10 A g⁻¹ 650 cyc** | p.C (`Fig. 1e`, `Fig. S3`) |
| 탈결합 알칼리 Zn‖S | "preliminary demonstration" · Nafion 117 · 음극액 3 m LiOH + 0.2 m Zn(OAc)₂ · 양극액 1M20L | p.C · SI p.4 (`Fig. S4`) |
| 고로딩 | 3.13 · 4.83 mg cm⁻² — 부분 용량 감소(두꺼운 전극 수송 한계) | p.B · SI p.7 (`Fig. S2`) |
| 첫 사이클 "활성화" | 0.5 A g⁻¹ 첫 충전에 **−0.6 V 부근 긴 평탄 = 앞선 방전에서 생긴 Li₂S 의 산화** — *"Mn²⁺ concentration polarization … local depletion of Mn²⁺ favors a Li⁺-S conversion route and leads to additional Li₂S"* · 0.2 · 0.1 A g⁻¹ 로 낮추면 짧아지다 소멸 | SI p.6 (`Fig. S1`) — ⚠ 고율에서의 함의는 §10-⑫ |

---

## 4. 계산 방법 ★★ — 적힌 것 전부 + 안 적힌 것 전부

> 원문은 SI p.4–5 의 **"Molecular dynamics simulations"** 한 문단 + **"DFT calculations"** 세 덩어리(VASP 주기 → Gaussian → 다시 VASP/LOBSTER)가 **전부**다. ⚠ 두 VASP 덩어리가 **어느 계산(NEB 인지 클러스터인지)에 해당하는지 논문이 대응시키지 않는다** — 아래는 우리 추정.

### 4a. 적힌 것 (SI p.4–5 원문)

| 항목 | 원문 | 우리 판정 / 단서 |
|---|---|---|
| 주기 DFT 코드 | *"Periodic spin-polarized density functional theory (DFT) calculations were performed using the Vienna Ab initio Simulation Package (VASP), version 5.4.4"* (refs 5–7) | — |
| 기저 · PP | **PAW** (ref 8 Kresse & Joubert 1999) · 평면파 | PAW 셋(Mn_pv? Li_sv?) 미기재 |
| 범함수 | **GGA-PBE** (ref 9) | ⛔ **+U 없음** — Mn²⁺ d⁵ 황화물에 PBE 단독 (§10-②) |
| 스핀 | *"spin-polarized"* | **자기 배열(FM/AFM) · 총자화 · 초기 자기모멘트 미기재** |
| NEB | *"Diffusion barriers were calculated using the climbing-image nudged elastic band (CINEB) method. The energy cutoff was set to **520 eV** for all CINEB calculations."* | 이미지 수는 `Fig. 4g` 에서 0–4 (중간 **3개**, `figure-read`) · 스프링 상수 · 힘 수렴 · k 점 · 슈퍼셀 · **결함 형태(틈새/공공)** · **이동종 전하** 미기재 |
| 분자 클러스터 코드 | *"Molecular-cluster binding-energy calculations were performed using the **Gaussian 16** software package"* (ref 10 = Rev. A.03) | — |
| 분자 클러스터 수준 | *"Structural optimizations for the complexes involving Li⁺, Mn²⁺, Cl⁻, and H₂O were conducted at the **M06-2X/def2-TZVP** level of theory, utilizing water as an implicit solvent via the **SMD** solvation model."* | **전하 · 멀티플리시티 미기재**(Mn²⁺ 고스핀이면 6중항 — EPR 이 고스핀을 말한다) · 진동수(허수 0)·ZPE·열보정 미기재 · **BSSE(counterpoise) 미기재** · M06-2X 선택 근거 미기재 |
| 결합에너지 정의 | *"\|E_b\| = \|E_complex − E_c − E_m\|, where E_complex is the total energy of the cation-solvent complex, E_c is the energy of the cation, E_m is the total energy of water molecules or anions"* | **절대값이라 부호가 사라진다** · E_m 이 리간드 **묶음 한 덩어리**인지 **개별 분자 합**인지 모호 · **리간드 수 정규화 없음** (§5.2) |
| 둘째 VASP 덩어리 | *"PAW … PBE … The cutoff energy is set to **500 eV**, and the convergence criteria for energy and force are **10⁻⁵ eV** and **0.02 eV/Å**, respectively. A **Gamma-centered 1×1×1** k-point mesh … The dispersion-corrected **DFT-D3** method (ref 12) … The projected crystal orbital Hamilton population (pCOHP) analysis is calculated using the **LOBSTER** program (ref 13) to quantify the strength of S–S bond."* | Γ 1점 + D3 + S–S pCOHP ⇒ **본문 "local atomic structural motif"(클러스터) 계산으로 추정**. ⚠ D3 **감쇠 형식 미기재** — ref 12 = Grimme 2010(zero-damping 원전)이고 BJ 원전 인용 없음 → **D3(zero) 추정**. 진공 두께 · 쌍극자 보정 · **총전하** · 자기 배열 미기재. LOBSTER **기저 · 밴드 수 · charge spilling · 적분 창** 미기재. 520 eV(NEB) vs 500 eV(클러스터) — **두 ENCUT 이 섞여 있다** |
| 고전 MD | **GROMACS** (refs 1–2) · 물 **SPC/E** · 이온 비결합 **Merz** 파라미터(refs 3–4 = Li, Roberts, Chakravorty, Merz 2013 *JCTC* 2가 · Li, Song, Merz 2015 *JCTC* 1가 = **12-6 LJ**) · **PME** · 5 nm × 5 nm × 5 nm 입방 · 최급강하(최대힘 < 1000 kJ mol⁻¹ nm⁻¹) · **NVT 10 ns → NPT 10 ns → NPT 5 ns 생산, 298 K** · VMD | 온도·압력 조절기 · dt · 컷오프 · Merz **세트(HFE/IOD/CM)** 미기재 · 전하 스케일링 언급 없음(= 고정 전하 ±1/±2 로 추정) · 생산 단계 목적 *"to analyze the free water fraction"* — **그 결과는 어디에도 없다** |

### 4b. 그림에서만 드러나는 것 (`figure-read`)

| 항목 | 드러난 것 | 출처 |
|---|---|---|
| **"MnS₄ unit" 모델의 실체** | 본문은 *"soluble intermediate MnS₄ units"* 라 부르지만, 그림의 황 클러스터는 **Mn ≈2 + S ≈8** (가려진 원자 가능) = 대략 (MnS₄)₂ 조각. 착물이 위에 얹히고 **말단 S(S1)** 와 그 이웃 S(S2)의 결합을 잰다 | `Fig. 4d` (700 dpi 확대) |
| 세 모델의 기하 | **황 클러스터 형태가 모델마다 눈에 띄게 다르다** (Mn 두 개가 위아래 vs 나란히, S 배치 상이) — "같은 모티프에 착물만 바꾼" 통제 비교가 아니다 | `Fig. 4d` |
| 착물–황 접촉 | Mn(H₂O)₆ · Mn(H₂O)₃Cl₃ 모델은 **물 분자가 S1 근처**(수소결합으로 보임), LiCl₄ 모델은 **Li–Cl 착물이 S1 에 가장 가깝게** 붙는다 (Li 와 S1 이 직접 닿는지 Cl 을 사이에 두는지는 해상도로 판정 불가) | `Fig. 4d` |
| COHP 패널 | 세 패널 **x축 범위가 다르다** (−4 ~ +2 / **−10 ~ +5** / −4 ~ +4) · y축 E − E_f −15 ~ +20 eV · 반결합(음의 −COHP) 봉우리는 세 모델 모두 **E_F 위**(`figure-read ≈` +1.5 ~ +4 eV) · 깊은 결합 봉우리 ≈ −13 eV 공통 | `Fig. 4e` |
| NEB 구조 | **실제 구조 렌더가 아니라 도식**(원 + 점선 결합)이다 — 육방 망 투영 위에 이미지 0–4 가 한 줄로 겹쳐 그려짐 · 슈퍼셀·원자 수 판독 불가 · 생성물 XRD/TEM 이 γ-MnS(섬아연석형 육방, PDF#89-4089)라 **γ-MnS 로 추정** | `Fig. 4f` (확대) |
| NEB 곡선 | 5점을 지나는 매끄러운 스플라인 · Mn 곡선이 이미지 4 직전 ≈ −0.02 eV 로 **0 아래** (보간 인공물) | `Fig. 4g` (픽셀 판독) |
| PDOS | 스핀 상(+)·하(−) · **"S atoms"**(어느 S 인지 — S1? 전체? — 미기재) · 3p 분해 없음 · 꺾은선 격자 ≈0.2 eV | `Fig. S25` |
| 착물 5종 | 캡션은 "various solvation structures" — 그림에는 **LiCl₄ · Mn(H₂O)₆ · Mn(H₂O)₅Cl · Mn(H₂O)₄Cl₂ · Mn(H₂O)₃Cl₃** 다섯이 그려져 있다 (본문은 셋만 이름을 댄다) | `Fig. 4c` |
| MD 스냅샷 | 1M20L 에서 이온이 **덩어리로 뭉친** 모습 (색 범례 없음 — 어느 구가 Li·Mn·Cl 인지 그림에 없다) | `Fig. S8a,b` |

### 4c. ⛔ 안 적힌 것 (재현 불가 목록 — 전부 n/a)

**NEB**: 슈퍼셀 크기·원자 수 · k 점 · MnS 다형(α 암염 / γ 섬아연석) · 자기 배열 · **+U** · 이동 기구(틈새/공공/교환) · **이동종 전하 처리**(중성 Li 원자를 넣었나 = 여분 전자는 어디로 · 하전 셀 + 배경 보정인가) · 스프링 상수 · 힘 수렴 · 끝점 이완 여부.
**클러스터(VASP)**: 원자 수 · **총전하**(Mn(H₂O)₆²⁺ · Mn(H₂O)₃Cl₃⁻ · LiCl₄³⁻ 를 형식대로 두면 계 전체 +2 / −1 / −3) · 진공 두께 · 쌍극자 보정 · **자기 배열**(Mn 이 2–3 개인 다핵 계) · 초기 배치 · 배치 수(**단일로 보인다**) · LOBSTER 기저·spilling · PDOS 스미어링·NEDOS.
**Gaussian**: 전하·멀티플리시티 · 진동수 확인 · ZPE/열보정(ΔE 인가 ΔG 인가) · BSSE · 착물 초기 구조 · 이성질체(시스/트랜스 · fac/mer) 선택.
**MD**: 앙상블 조절기 · dt · 컷오프 · 전하 스케일링 · Merz 세트 · 반복 수 · 오차막대 · Li 배위 · 종 분포(Mn(H₂O)₆₋ₙClₙ 의 n 분포) · free water fraction.
**공통**: 구조 파일(요청 시) · 계산 자원.

> 🔑 **"적힌 것" 과 "같은 양을 우리가 다시 재려면 필요한 것" 의 차이**가 이 논문 계산의 본질이다. 특히 **전하·스핀 상태가 하나도 적혀 있지 않은데 계가 열린 껍질(Mn²⁺ d⁵) 이다** — 우리 규율(CLAUDE.md, 회신 N)로는 상태 선언 없이 스칼라 보고량이 정의되지 않는 경우다 (§7c-4).

### 4d. 용매 모델 · 전위/pH 처리 판정 (수계 논문이라 따로) ★

| 계산 | 용매 처리 | 판정 |
|---|---|---|
| Gaussian 착물 결합에너지 (`Fig. 4c`) | **클러스터-연속체** — 1차 배위껍질은 명시적(H₂O · Cl⁻), 바깥은 **SMD(물)** | 표준적 방식. ⚠ 그러나 매질이 **20 m LiCl(물 2.78 개/Li)** 인데 SMD 파라미터는 **순수 물**이다 — 고농도 전해질의 유전 환경·이온 세기는 물과 다르다(우리 배경지식, 논문 밖) · 음이온 착물(LiCl₄³⁻)처럼 전하가 큰 종일수록 연속체 모형의 오차가 커진다 |
| VASP 클러스터 S–S · ICOHP · PDOS (`Fig. 4d,e`, `Fig. S25`) | **없음 (진공)** — VASPsol 등 언급 0 | ⛔ **수계 계면의 S–S 약화를 말하는 핵심 계산이 용매 없이 돌았다.** 전하를 띤 착물을 차폐 없이 황 클러스터 옆에 두면 분극·전하 이동이 과장될 수 있다(추정). 총전하 미기재라 판정 불가 |
| VASP NEB (`Fig. 4g`) | 해당 없음 (벌크 결정) | 계면·용매가 빠진 대신 **"계면 수송" 결론을 받치지 못한다** (§5.5) |
| GROMACS MD (`Fig. S8`) | **명시적 물 SPC/E** · 이온 12-6 LJ (고정 전하 · 비분극) | 이 논문에서 유일한 명시적 용매. ⚠ 비분극 고정전하 힘장을 **20 m** 에 쓰면 이온 응집이 과대해지기 쉽다(우리 배경지식) — 스냅샷의 덩어리(`Fig. S8b`)와 EPR 교환선폭 해석이 **같은 방향**이라는 것은 맞지만, 둘 다 정량 검증이 아니다 |
| 전극 전위 · pH | **없음** — CHE(계산수소전극)·정전위(grand-canonical)·pH 보정 0 · 황 환원의 전위 의존 에너지 0 | ⛔ 전기화학 논문인데 계산에 **전위 축이 없다** (비교: `[Wu26Zn]` 은 VASPsol + 정전위 −0.8 V vs SHE — §K-11) |

---

## 4′. 실험 방법 (DFT 해석에 필요한 만큼)

| 항목 | 조건 | 출처 |
|---|---|---|
| 셀 | 3전극 Swagelok · S@AC WE / AC CE / **Ag/AgCl RE** · 200 µL · 25 °C · NEWARE CT4008 · BioLogic VSP-3e | SI p.3–4 |
| 전위 축 | 전부 **vs Ag/AgCl** (Li/Li⁺ 환산 없음) | 본문 그림 축 |
| SXRD | SSRF BL02U2 · **λ = 0.6887 Å** · 빔 0.3 × 0.3 mm² · PILATUS3S 2M | SI p.3 |
| XAS | BSRF 4B7A·4B9A · SSRF BL16U1 | SI p.3 |
| XPS | Thermo ESCALAB Xi+ · Al Kα 1486.6 eV — **결합에너지 보정 기준 미기재** | SI p.3 |
| Raman | Dilor LabRam-1B · **633 nm** | SI p.3 |
| EQCM-D | QSense Explorer · Au 코팅 AT-cut 수정 QSX 301 (불활성 전도 기판) · Li/Mn 비는 *"apparent and semi-quantitative"* 로 명시 | SI p.3 · p.20 |
| ToF-SIMS | PHI Nano TOF 3 · Bi₃⁺ 30 keV 분석 · Ar⁺ 2 keV 100 nA 400 × 400 µm² 식각 · 분석 100 × 100 µm² | SI p.3 |
| 시료 채취 | Ar 글러브박스에서 해체 | SI p.3 |
| EIS | in situ, 0.5 A g⁻¹ 후 OCV 30 min + CA 1 h 안정화, 10 kHz – 10 mHz | SI p.4 |

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 용매화 구조 — MD (`Fig. S8`) + 분광 (본문)

- **주장** (p.D): LiCl 이 늘수록 Mn–Cl 배위수 ↑ · Mn–O ↓, *"the **Mn(H₂O)₃Cl₃ complex remains thermodynamically stable** in the 1M20L electrolyte"* → Mn²⁺ 는 완전 수화 이온이 아니라 **이온결합 상태로** 황 전환에 참여한다. EPR 6선 → 단일선(교환결합), Raman O–H 수소결합망 붕괴, UV-vis Mn–Cl 띠가 같은 그림을 그린다.
- **그림 실독** (`Fig. S8c,d` 확대): Mn–Cl 배위수 `figure-read ≈` 1M **≈0.4** → 1M20L **≈2.7** · Mn–O 1M **≈5.5** → 1M20L **≈3.3**. 합이 ≈6 이라 **팔면체 평균 Mn(H₂O)₃.₃Cl₂.₇** — "평균적으로 Mn(H₂O)₃Cl₃ 근처" 라는 말은 그림과 맞는다. ⚠ 1M 범례 한 항목에 파란 점선이 두 색조로 보이고 중간 농도 곡선이 겹쳐 **1M1L·1M10L 의 색 배정은 확정 못 했다** (≈1.9 곡선은 Mn–O ≈4.0 과 합이 ≈5.9 라 1M10L 로 보인다 — 추정).
- **판정**:
  1. **평균 배위수는 종(species) 분포가 아니다.** CN 2.7 은 Mn(H₂O)₆₋ₙClₙ 의 n = 0–4 가 섞인 평균일 수 있다. *"thermodynamically stable"* 은 자유에너지(PMF·종 분포 적분)를 요구하는데 5 ns 한 궤적의 평균 CN 만 보였다.
  2. **Li 배위가 없다.** DFT 에서 Li⁺ 를 **LiCl₄** 로 모델링한 근거가 MD 에 없다. 1M20L 은 물이 Li 당 2.78 개뿐이라 접촉이온쌍이 많겠지만, **Cl⁻ 넷만 두른 LiCl₄³⁻** 는 그중 극단 한 종이다(우리 배경지식 — 논문 밖).
  3. **힘장**: 비분극 고정전하(SPC/E + 12-6 Merz)를 20 m 에 썼다 — 응집 과대 경향이 알려진 조합이다(배경지식). Merz 세트도 미기재. `Fig. S8b` 의 덩어리는 EPR 교환선폭 해석과 **방향은 같지만** 정량 검증이 아니다.
  4. SI 가 예고한 **"free water fraction"** 결과가 없다.

### 5.2 착물 결합에너지 (`Fig. 4c`) ★

- **주장** (p.G–H): Mn(H₂O)₆ → Mn(H₂O)₃Cl₃ 로 갈수록 결합에너지 ↑ = *"Mn²⁺ becomes more strongly coordinated and less prone to desolvation under Li⁺-rich conditions"* · LiCl₄ 가 최저 = *"Li⁺ undergoes facile desolvation to preferentially participate in interfacial redox reactions"* · 따라서 Li⁺ 는 *"kinetic promoter rather than … the dominant charge carrier in the final product"*.
- **그림 실독** (픽셀 판독 ±0.02 eV): **LiCl₄ 1.78 · Mn(H₂O)₆ 1.83 · Mn(H₂O)₅Cl 2.18 · Mn(H₂O)₄Cl₂ 2.48 · Mn(H₂O)₃Cl₃ 2.63 eV**. 막대에 숫자가 인쇄돼 있지 않다.
- **판정**:
  1. **LiCl₄ 와 완전 수화 Mn²⁺ 의 차는 0.05 eV** (≈3 %) — 착물 결합에너지의 방법 불확도(범함수·기저·BSSE·용매 모형) 안이다. 서사가 실제로 기대는 비교는 **LiCl₄ 1.78 vs Mn(H₂O)₃Cl₃ 2.63 (차 0.85 eV)** 다.
  2. **리간드당으로 나누면 결론이 사라진다** (우리 산수): LiCl₄ **0.445** vs Mn(H₂O)₃Cl₃ **0.438 eV/리간드** — 같다. 리간드당으로는 **완전 수화 Mn(H₂O)₆(0.305)가 가장 약하게 묶여 있다.** 총 결합에너지는 **전부 떼어 내는** 에너지이고, 반응 속도에 걸리는 것은 보통 **첫 리간드 하나를 떼는** 단계다 — 어느 쪽도 이 그림이 주지 않는다.
  3. **정의가 부호를 지운다** (\|E_b\|), **전하가 서로 다른 종**(형식 3−, 2+, 1+, 0, 1−)을 한 축에 놓는다 — 연속체 안에서 전하가 다른 종의 총 결합에너지는 직접 비교하기 어렵다.
  4. **Mn²⁺ d⁵ 멀티플리시티 미기재** — 고스핀(6중항)이 자연스럽지만(EPR 도 고스핀), 적지 않으면 **어느 상태의 에너지인지 정의되지 않는다**(§7c-4).
  5. **"탈용매화 장벽"이 아니다** — 계산된 것은 열역학적 총 결합이고 장벽(탈착 전이상태 · 리간드 교환 속도)은 없다.
  6. 마지막 문장(*"rather than … the dominant charge carrier in the final product"*)은 결합에너지가 말할 수 없는 내용이다 — 생성물 조성은 ICP·EQCM 이 말한다(Li : Mn ≈ 40–45 : 55–60, §3c·§3d).

### 5.3 S–S 결합길이 · ICOHP (`Fig. 4d,e`) ★★ — 논문의 핵심 DFT

- **주장** (p.H): *"Upon Li⁺ incorporation, the S−S bonds in the MnS₄ unit become noticeably longer (Figure 4d), and their ICOHP values become less negative compared with the Li-free case (Figure 4e), providing quantitative evidence of weakened S−S interactions. … Li⁺ preferentially polarizes and weakens the S−S bonds, destabilizing them and increasing their susceptibility to cleavage"*.
- **값** (인쇄값): S1–S2 = **2.08 Å · −2.72 eV** (+Mn(H₂O)₆) · **1.94 Å · −3.69 eV** (+Mn(H₂O)₃Cl₃) · **2.19 Å · −1.99 eV** (+LiCl₄).
- **그림 실독** (`Fig. 4d` 700 dpi 확대): 황 클러스터는 **Mn ≈2 + S ≈8** (본문 이름 "MnS₄ unit" 보다 크다) · **세 모델의 클러스터 형태가 서로 다르다** · 착물은 클러스터 위쪽 말단 S(S1) 옆에 하나씩. `Fig. 4e` 세 패널의 x축 범위가 달라(−4 ~ +2 / −10 ~ +5 / −4 ~ +4) **곡선 모양을 눈으로 비교하면 오해한다** — Mn(H₂O)₃Cl₃ 패널만 2.5배 넓은 축이다.
- **판정**:
  1. 🔴 **"Li-free case" 가 둘인데 방향이 반대다.** 완전 수화 Mn(H₂O)₆ 대비로는 LiCl₄ 가 +0.11 Å · ICOHP 크기 −27 % (약화) 가 맞다. 그러나 **Mn(H₂O)₃Cl₃ 는 Mn(H₂O)₆ 대비 −0.14 Å · +36 % 로 S–S 를 강화**한다. 논문 자신의 MD 가 1M20L 의 Mn 종을 Mn(H₂O)₃Cl₃ 라 했으므로, **1M20L 에서는 강화하는 Mn 종과 약화하는 Li 종이 함께 있다** — 순효과는 어느 종이 황 종에 얼마나 붙는지(농도·결합 자유에너지)에 달렸고, **계산되지 않았다.** 비교 기준을 1M(Mn(H₂O)₆)로 잡으면 "Li⁺ 가 약화" 이지만, 1M → 1M20L 의 실제 변화는 **Mn(H₂O)₆ → Mn(H₂O)₃Cl₃ + LiCl₄** 다.
  2. **ICOHP 는 결합길이의 재진술이다** (우리 산수): 세 쌍의 기울기 6.9 / 6.8 / 6.6 eV Å⁻¹ — 세 점이 한 직선 위에 있다. "결합길이가 늘었다" 와 "ICOHP 가 약해졌다" 는 **독립 증거 두 개가 아니라 같은 사실 하나**다.
  3. **통제되지 않은 비교**: 모델마다 클러스터 기하가 다르고 **배치가 하나씩**이다. 대조 결합(착물에서 먼 S–S)이 없어 차이가 착물 효과인지 **이완된 국소 극소점의 차이**인지 가를 수 없다.
  4. **진공 · 전하·스핀 미기재** (§4c·§4d): 형식 전하대로면 계가 +2 / −1 / −3 으로 다르고, 중성으로 계산했다면 착물의 형식 전하와 맞지 않아 **황 쪽 전자 수가 모델마다 달라진다** — 말단 S–S 결합길이는 황 사슬의 전자 수(환원 정도)에 민감하다(배경지식). 1.94 Å 는 통상 폴리설파이드 S–S 단일결합(≈2.05 Å 안팎, 배경지식)보다 짧다. **판정 불가 — 구조·전하가 "요청 시" 다.**
  5. **절단 "장벽"은 없다** — 결합이 약해 보이는 것과 절단 전이상태 에너지가 낮은 것은 다르다. 모식도(`Fig. 5c`)의 *"bond breaking"* 언덕은 **계산된 적 없는 곡선**이다.
  6. **"긴 사슬을 선호한다(preferentially targets long-chain)"**(초록·결론)는 **단쇄 황 종에 대한 같은 계산이 없어** 비교 자체가 없다.

### 5.4 PDOS (`Fig. S25`) ★ — 본문과 그림이 어긋난다

- **주장** (p.H): *"Li⁺-solvated clusters enhance the population of S 3p states around the Fermi level and **narrow the band gap**. This would render the sulfur sites highly electronically accessible and **improve the intrinsic electronic conductivity** of the sulfur species."*
- **그림 실독**: S 원자 PDOS(스핀 상·하), −5 ~ +5 eV. **세 곡선 모두 E = 0 에서 spin-up PDOS 가 0 이 아니다**(`figure-read ≈` 0.4–0.8 states eV⁻¹), spin-down 은 ≈0. E_F 확대 삽화에서도 세 곡선이 모두 유한값으로 E_F 를 지난다. 곡선은 ≈0.2 eV 간격의 꺾은선이다.
- **판정**:
  1. **어느 모델에도 갭이 안 보인다** → "갭이 좁아진다" 는 그림으로 성립하지 않는다. 우리 갭 규율(fixed-occupation nscf 의 VBM/CBM 고유값만 · DOS 문턱 판독 금지)로도 이 그림에서 갭을 읽을 수 없다.
  2. **E_F 에 spin-up 상태만 있는 모양**은 세 모델 모두 **부분 점유된 열린 껍질**(스미어링으로 메워진 준위)이라는 뜻이다 — 계 전하·자기 배열이 안 적혀 있어서, 이것이 물리인지 **전자 수 설정의 산물**인지 판정할 수 없다 (`[Liu26Sn]` §5.2 의 "E_F 위 S 성분 빈 상태" 와 같은 부류의 경고).
  3. E_F 에서의 세 곡선 차이(≈0.2–0.4 states eV⁻¹)는 곡선의 들쭉날쭉함과 같은 크기다. "S **3p**" 라고 했지만 궤도 분해가 없다.
  4. **분자 클러스터의 PDOS 로 "고유 전자전도도" 를 말할 수 없다** — 전도도는 주기계의 띠·운반자·이동도의 양이다.

### 5.5 CI-NEB — Li⁺ 대 Mn²⁺ 이동 (`Fig. 4f,g`) ★★

- **주장** (p.H): *"Li⁺ exhibits a lower migration barrier than Mn²⁺ along the same diffusion path. Such a contrast indicates that Li⁺ can participate more rapidly in local interfacial transport and sulfur conversion than Mn²⁺"*.
- **그림 실독** (픽셀 판독 ±0.01 eV): 이미지 0–4 · **Li 0 / 0.48 / 0.97 / 0.48 / 0 eV** · **Mn 0 / 0.64 / 1.19 / 0.64 / 0 eV**. 대칭 경로, 끝점이 같은 에너지 = 동등 자리 사이 홉. `Fig. 4f` 는 **도식**이라 슈퍼셀·결함 형태를 읽을 수 없다(틈새 통로를 지나는 모양으로 그려져 있다).
- **판정**:
  1. **상대차(≈0.22 eV)는 방향으로만 쓸 수 있다** — 298 K 속도비 ≈5×10³(같은 ν₀ 가정). 그러나 +U 없음 · 자기 배열 미기재 · **이동종 전하 처리 미기재**(중성 Li 원자를 넣으면 여분 전자 1개, Mn 원자면 2개가 호스트로 간다 — PBE 는 그 전자를 비국재화하기 쉽다, 배경지식) 라 **상대차조차 방법 조건부**다.
  2. 🔴 **절대값으로는 결론과 반대 방향을 가리킨다** (우리 산수, ν₀ = 10¹³ s⁻¹): Γ_Li ≈ 4×10⁻⁴ s⁻¹ → **15 A g⁻¹ 의 1012 mAh g⁻¹ 방전(≈243 s) 동안 Li 는 평균 ≈0.1 번 홉한다.** 243 s 안에 10 홉(≈1 nm 급 이동)을 하려면 E‡ ≲ 0.85 eV 여야 한다. ⇒ **벌크 γ-MnS 속 고상 확산으로는 고율 용량을 설명할 수 없다.** 빠른 반응은 계면·나노 크기·비정질 생성물·혹은 액상 매개 단계에서 와야 한다 — 논문은 "solid-state-dominated pathway" 를 말하면서 **자기 NEB 와의 이 긴장을 다루지 않는다.**
  3. **모델이 결론의 대상이 아니다**: 벌크 MnS 이지 **계면**도 아니고 **Li–Mn–S 생성물**(Li 40 %)도 아니다. "local **interfacial** transport" 결론은 계면 모델 없이 나왔다.
  4. **"same diffusion path"** 로 Mn 을 Li 경로에 태웠다 — Mn 의 최소에너지 경로가 따로 있을 수 있다. 중간 이미지 3개로는 경로 이완 여지도 적다 (우리 SEI NEB 는 7개였다 — §7c-3).
  5. 그림 양식: 5점 스플라인이 0 아래로 overshoot(≈ −0.02 eV) — 보간 인공물이지만, 이미지 수가 적다는 것을 보여 준다.

### 5.6 생성물 Li–Mn–S 증거 (`Fig. 2`, `Fig. S9`, `Fig. S10`) — DFT 모델이 무엇이어야 했나

- **흐름** (p.C–D): XPS D50 에서 MnS₂·MnS 가 먼저(= Mn²⁺ 가 먼저 반응) → 방전이 깊어지며 낮은 결합에너지로 이동·넓어짐(Li⁺ 참여) · SXRD 는 얕은 방전에서 결정성 MnS → (002) 만 저각 이동(= Li 삽입에 의한 이방성 팽창) · XANES 흡수단이 Li₂S 와 MnS 사이 · Raman 이 넓어짐 · ICP 에서 Mn 먼저, Li 나중 → **MnS 핵생성 뒤 Li 가 들어가 Li_xMn_yS 가 된다.**
- **그림 실독과 판정**:
  1. **XPS** (`Fig. 2c` 확대 · `Fig. S10`): D100 은 `figure-read ≈` **160.6 / 161.6 eV 이중선**이 지배적이다. 표준(인쇄값) **Li₂S 160 · MnS 162 eV** — "사이" 는 맞지만 **Li₂S 에서 0.5 eV, MnS 에서 1.5 eV** 로 Li₂S 쪽에 훨씬 가깝다. 게다가 "표준 Li₂S" 스펙트럼은 **Li₂S₂(161.8) 성분이 Li₂S(160) 보다 크다** — 기준 시료가 산화돼 있다. BE 보정 기준 미기재. ⇒ XPS 만으로 "Li₂S 와 다른 새 황 환경" 을 가르기 어렵다.
  2. **XANES** (`Fig. S9a`): 본문은 *"between those of **pristine** Li₂S and MnS"* 라고 쓰지만 그림에는 **순수 표준 시료가 없다** — 방전 전극 셋뿐이다. Li⁺/Mn²⁺-S 곡선은 Mn²⁺-S 전극과 **거의 겹친다**(흡수단 ≈0.2–0.3 eV). Li⁺-S 전극은 ≈2482.7 eV 에 **거대한 황산염 백색선**(심한 산화 — 본문의 SO₄²⁻ 억제 서술과 같은 방향). ⇒ **본문–그림 불일치**.
  3. **SXRD** (`Fig. 2d` 확대): (002) 12.18 → 12.08° (Δ ≈ −0.10°, c ≈ +0.8 %). ⚠ **11.8° 부근 꺾임이 D0(황만 있는 전극)에도 있다** — 배경/검출기 이음매로 보인다 — 그리고 D100 의 (002) 봉우리가 바로 그 옆이라 **0.1° 판독이 그 인공물에 민감할 수 있다.** `Fig. S9b` 의 (110) 은 D25 → D50 에서 **a 축도 ≈0.45 % 늘었음**을 보여 주는데(우리 산수) 본문의 "이방성" 서사에는 없다.
  4. **TEM** (SI p.16): *"slight lattice expansion"* 이라 쓰지만 기준 d 가 없다. 우리가 `Fig. 2d` 기준 막대로 환산한 d 대비 TEM 값은 **−1 ~ −3 %** (§3c) — 팽창 방향이 아니다(TEM d 정확도 자체가 ±1–2 % 급이라 어느 쪽도 결론 불가).
  5. **ICP 겉보기 조성 Li₄Mn₆S₈ = 2Li₂S + 6MnS** (우리 산수) — 평균 조성은 **3원 단일상과 혼합물을 가르지 못한다.** 저자들도 *"average elemental ratio"* 라고 조심스럽게 쓴다. 3원상의 무게는 결국 (002) 0.1° 이동 · XPS 0.5 eV · XANES 0.2–0.3 eV 에 걸려 있다.
  6. ⭐ 그래도 **혼합물 가설에 불리한 증거 하나**는 있다: **탈이온수 세척액에서 황화물 흡수가 없다**(`Fig. S13` — 안 봄, 본문 p.D). Li₂S 가 따로 있었다면 물에 녹아 나왔을 것이다(Li₂S 의 수용성 — 배경지식). ⚠ 단 **ICP 전극을 세척했는지는 적혀 있지 않다.**
- **DFT 에 대한 함의**: 논문이 옳다면 전환의 속도론을 말할 모델은 **Li–Mn–S(Li 40 %) 고상 또는 그 계면**이어야 한다. 논문의 DFT 는 **벌크 MnS(NEB)** 와 **진공 Mn–S 클러스터(ICOHP)** 뿐이다.

### 5.7 고상 우세 전환 증거 (`Fig. 3`)

- **in situ UV-vis** (`Fig. 3a–c`): Li⁺-S 는 S²⁻/S₂²⁻(<300 nm)가 방전 내내 커진다(액상 경로). Mn²⁺-S 는 S₄²⁻(≈360 nm)가 중간에 나타났다 사라진다(MnS₂·MnS 형성 = 고–액–고). Li⁺/Mn²⁺-S 는 거의 평평하고 확대 삽화에서만 약한 S₄²⁻ 가 보인다. ⚠ 스펙트럼이 **수직 오프셋 + a.u.** 라 패널 사이 절대 세기 비교는 안 된다 — 그래도 (c) 의 평평함은 정성적으로 설득력이 있다.
- **EQCM** (`Fig. 3d–f`, SI p.20): Mn²⁺-S 는 Δm 이 사이클마다 줄어 `figure-read ≈` −9 ~ −10 ng (순 손실 = 셔틀). Li⁺/Mn²⁺-S 는 Q(0 ↔ −0.13 mC) 와 Δm(0 ↔ +30 ng) 이 **주기적·동기화**. 이상 한계 72(Li) / ≈285(Mn) ng mC⁻¹ 사이의 ≈222 → Li : Mn ≈ 45 : 55 (우리 검산 일치). ⚠ **양이온만 질량을 바꾼다는 모형**(Cl⁻·물·황 자체의 질량 변화 무시) — 저자들도 *"apparent and semi-quantitative"* 로 적는다. 초기 구간의 더 큰 Δm/ΔQ 는 *"loosely solvated, sulfur-rich interfacial species"* 로 해석(SI p.20).
- **ToF-SIMS** (`Fig. 3g,h`): Li⁺/Mn²⁺-S 전극 표면의 S 지도가 조밀·균일. 깊이 프로파일 `figure-read ≈` S⁻ ≈2× · S₂⁻ ≈20× · **HS⁻ ≈40×** 더 크다 — ⚠ **HS⁻(수소화 황) 신호가 40배인 것을 본문이 논의하지 않는다.** 물과 반응한 황화물(가수분해 · 양성자화 황 종)의 표지일 수 있다(추정 — 판정 불가).
- 판정: **실험 쪽 "용해 억제 · 고상 유지" 증거는 서로 일관된다** (UV-vis · EQCM · ToF-SIMS · 자가방전 CE > 90 % · DEMS H₂S 없음). 문제는 이것이 **"빠른 고상 경로"** 의 증거인지 **"용해가 억제된 경로"** 의 증거인지다 — 앞의 것은 속도론이 필요하고, 그 속도론의 계산(NEB)은 §5.5 대로 오히려 반대쪽을 가리킨다.

### 5.8 속도론 실험 (`Fig. 4a,b`)

- **R_d** (`Fig. 4a`, `figure-read`): Mn²⁺-S 가 방전 초기 ≈464 Ω 로 가장 크고 방전하며 ≈50 Ω 로 준다. Li⁺-S 는 ≈16–21 Ω(가용성 중간체가 확산을 돕는다), Li⁺/Mn²⁺-S 는 ≈142 → ≈76 → ≈42 Ω 로 **중간**. 저자 해석: Mn²⁺ 이동이 병목, Li⁺ 가 균형.
- **CA** (`Fig. 4b`): −0.3 ~ −0.6 V 에서 Li⁺/Mn²⁺-S 전류가 빨리 평탄에 닿고 크다 — *"long-chain to short-chain transformation"* 구간이 빨라졌다는 해석. ⚠ y축 a.u. — 정량 비교 불가.
- 판정: 둘 다 **겉보기 저항·전류**이고 장벽이 아니다. 온도 의존(Arrhenius) 측정 0.

### 5.9 일반화 — Ni²⁺ · Zn²⁺ (`Fig. 5`)

- `Fig. 5a`: Ni²⁺-S 3번째 사이클 — 방전 `figure-read ≈` ≈830 mAh g⁻¹ · Li⁺/Ni²⁺-S ≈1100 mAh g⁻¹. D100 XPS: Ni²⁺-S 는 **완전 방전에서도 S₈ 성분이 주(主)** + 약한 NiS, Li⁺/Ni²⁺-S 는 NiS₂(≈163) + **Li_xNi_yS(`figure-read ≈`161 eV)**.
- `Fig. 5b`: Zn²⁺-S ≈1250 · Li⁺/Zn²⁺-S ≈1450 mAh g⁻¹ (`figure-read`) · 방전 평탄 차이는 작다(≈0.03 V). D100 XPS: ZnS vs ZnS + **Li_xZn_yS(≈161 eV)**.
- `Fig. 5c` 모식도: M²⁺-S = *"shuttle effect · high diffusion barrier"*, Li⁺-promoted = *"accelerated S–S cleavage · low diffusion barrier"* — 에너지 언덕 두 개(bond breaking · diffusion). ⛔ **y축 눈금 없음 · 두 언덕 모두 계산된 적 없다**(S–S 절단 TS 0 · 확산은 벌크 NEB 0.97 eV 가 "low" 로 그려졌다).
- 판정: "Li_xM_yS" 배정은 다시 **XPS 새 성분(≈161 eV)** 하나에 기댄다 — §5.6 의 같은 약점(Li₂S 160 eV 근처).

### 5.10 셀 성능 (`Fig. 1` — 안 봄)

- 본문 값(§3e): 15 A g⁻¹ 에서 1012 mAh g⁻¹ · 5 A g⁻¹ 200 cyc >900 · S‖LMO 0.9 V 평탄 650 cyc @10 A g⁻¹. `Fig. 1f` 문헌 비교(refs 27–32)는 **전해질·로딩·전극 구성이 다른 편끼리** — 인용하지 않는다.
- 비용량은 **S 질량 기준**이고 셀은 **3전극 반쪽셀**(AC 상대극 40 mg cm⁻² 대과잉)이다 — 셀 수준 에너지밀도가 아니다. 저자도 결론에서 실용 에너지밀도는 향후 과제라 쓴다(p.H).

---

## 6. ★★ "kinetic promoter" 주장은 DFT 로 어떻게 뒷받침되나 — 사슬 판정

> **판정 요약: 실험은 "용해 억제 + Li·Mn 공동 참여" 를 잘 보인다. DFT 는 "Li⁺ 가 속도를 올린다" 는 부분을 **직접 계산하지 않았고**, 계산한 네 가지는 각각 한 칸씩 결론에 못 미친다.**

| 주장 (쪽) | DFT 근거 | 실제로 잰 것 | 지지하나 |
|---|---|---|---|
| Li⁺ 는 탈용매화가 쉬워 계면 반응에 먼저 참여 (p.H) | `Fig. 4c` | 착물 **총** 결합 크기 (SMD · 전하·스핀 미기재) | △ LiCl₄ vs Mn(H₂O)₆ 차 0.05 eV · 리간드당으로 LiCl₄ ≈ Mn(H₂O)₃Cl₃ · LiCl₄ 종 근거 없음 · 장벽 아님 |
| Li-rich 에서 Mn²⁺ 는 더 강하게 배위 (p.G–H) | `Fig. 4c` · `Fig. S8` | 같음 + 평균 CN | ○ **모델 안에서는** 방향이 맞다 (총량 1.83 → 2.63 · 리간드당 0.31 → 0.44 · CN Cl 0.4 → 2.7) |
| Li⁺ 가 S–S 를 분극·약화 → 절단 촉진 (p.H · 결론) | `Fig. 4d,e` | 진공 클러스터 말단 S–S **한 결합**의 정적 길이·ICOHP, 단일 배치 | △ LiCl₄ 최약은 맞다 — 그러나 **Mn(H₂O)₃Cl₃ 는 강화** → 1M20L 순효과 미정 · 통제 비교 아님 · TS 0 |
| Li⁺ 는 **긴 사슬** 황을 선호 (초록 · 결론) | 없음 | 단쇄 종 계산 0 | ✗ 비교 대상이 없다 |
| **"lowers the redox barrier"** (초록) | 없음 (S–S ICOHP 에서 추론) | 전자이동 재구성에너지 λ · S–S 절단 TS · 단계별 ΔG **0** | ✗ **추론** — `[Liu26Sn]` 의 "Low-Barrier" 와 같은 형식 |
| 황 자리의 전자 접근성·고유 전자전도도 향상 · 갭 축소 (p.H) | `Fig. S25` | 클러스터 S PDOS | ✗ **그림에 갭이 없다** · 차이가 잡음 수준 · 클러스터로 전도도 정의 불가 |
| Li⁺ 가 계면 수송에 더 빨리 참여 (p.H) | `Fig. 4f,g` | **벌크 MnS** Li/Mn CI-NEB | △ 상대차 ≈0.22 eV 만 · 계면 아님 · 절대 0.97 eV 로는 243 s 에 ≈0.1 홉 → **고상 벌크 수송으로 고율 설명 불가** |
| Mn(H₂O)₃Cl₃ 가 1M20L 에서 열역학적으로 안정 (p.D) | `Fig. S8` | 5 ns 평균 CN | △ 평균 CN 은 맞다 · 종 분포·자유에너지 미제시 → "thermodynamically stable" 은 MD 에서 안 나온다 |
| 반응이 고상 우세 경로로 바뀐다 (제목급 주장) | (DFT 없음 — 실험) | UV-vis · EQCM · ToF-SIMS · 자가방전 | ○ 실험상 "용해 억제" 는 일관 · **"빠른" 고상 경로의 속도론 근거는 없다** |

**논문 전체에서 0건인 계산**: 단계별 황 환원 ΔG 도표 · 속도결정단계 · S–S 절단 / MnS·Li–Mn–S 핵생성 TS · Li–Mn–S 상의 구조·형성에너지·볼록껍질(hull) · 계면 모델 · 전위 의존 에너지 · AIMD/MLIP · 온도 스윕(Arrhenius) 실험.

⇒ **허용 서술**: *"The DFT in this work supports, at most, that a model LiCl₄ complex lengthens a terminal S–S bond of a Mn–S cluster relative to a fully hydrated Mn²⁺ complex (static PBE-D3, vacuum, single configurations), and that Li migrates with a lower CI-NEB barrier than Mn in bulk MnS; no redox or S–S cleavage barrier is computed."*
⇒ **금지 서술**: "Li⁺ 가 S–S 절단 장벽을 낮춘다 (DFT)" · "DFT 로 산화환원 장벽 저하를 확인" · "Li⁺ 의 이동 장벽이 낮아 고상 전환이 빠르다 (0.97 eV)".

---

## 7. 우리 계산과의 대조 ★★ — 방법 차이 먼저, 값은 섞지 않는다

> ⛔ **문헌값은 소환값이다 — 우리 db 절대값과 한 표에 섞지 않는다** (CLAUDE.md §litdb). 그래서 **7a(문헌) · 7b(우리 원장)를 별도 표**로 두고 **7c 는 판정만** 적는다. 그리고 이 논문은 **수계**다 — 우리 황화물 SE 물성 4축(σ · ESW · 기계 · 갭)과 겹치는 값이 **0 개**다.
> 원장 조회 (2026-09-27): `db/properties/bonds.json` · `sei_neb.json` · `kb/methodology/computational_methods_canonical.md` §5 · `litdb/our_dft_baseline.md` · `kb/projects/zn_alzib_dft_md_contribution_2026_09_03.md` · `db/properties/citation_hazards.json`(`HZ-nd-icohp-june-nds-pp`).

### 7a. 이 논문 쪽 값 (소환값 — 문헌 표)

| 계 · 양 | 값 | 방법 | 출처 |
|---|---|---|---|
| 착물 \|E_b\| (LiCl₄ · Mn(H₂O)₆ · Mn(H₂O)₃Cl₃) | `figure-read ≈` 1.78 · 1.83 · 2.63 eV | Gaussian 16 · M06-2X/def2-TZVP · SMD(물) · 전하·멀티플리시티·BSSE·열보정 미기재 · \|·\| 정의 | `Fig. 4c` |
| S1–S2 결합길이 · ICOHP (+Mn(H₂O)₆ / +Mn(H₂O)₃Cl₃ / +LiCl₄) | 2.08 / 1.94 / 2.19 Å · −2.72 / −3.69 / −1.99 eV | VASP PBE-D3(감쇠 미기재) · 500 eV · Γ · 진공 클러스터 · 단일 배치 · LOBSTER 기저/spilling 미기재 | `Fig. 4d,e` 인쇄값 |
| CI-NEB (벌크 MnS) Li / Mn | `figure-read ≈` 0.97 / 1.19 eV | VASP PBE 스핀분극 · 520 eV · 중간 이미지 3 · 셀·k·+U·자기배열·전하 미기재 | `Fig. 4g` |
| MD 배위수 1M20L (Mn–Cl · Mn–O) | `figure-read ≈` 2.7 · 3.3 | GROMACS · SPC/E · Merz 12-6 · 5 ns NPT 298 K · 단일 궤적 | `Fig. S8` |

### 7b. 우리 원장 쪽 (별도 표 — 7a 와 섞지 않는다)

| 원장 항목 | 값 / 규약 | status / 표지 | 출처 |
|---|---|---|---|
| ICOHP 방법 규약 | LOBSTER · **all-PAW · ext-basis · nbnd 500 · spilling < 5 %** · ⚠ minimal-basis 교훈: modelc P–S −5.12(spilling 17 %) stale · b2o3 Li–X −0.8 artifact | 규약 | `kb/methodology/computational_methods_canonical.md` §5 |
| 우리 원장의 "S-S" | **케이지 비결합 S···S** — comp1_v3 평균 거리 **3.595 Å** · ICOHP **−0.107 eV/bond** (n = 56, *"cage, weak"*) · modelc_v3 **3.519 Å** · **−0.11** (n = 58) | 원장 파일값 · 레지스트리에 S–S 키 없음(grep 확인) | `db/properties/bonds.json` |
| TM/RE–S ICOHP 의 PP 민감도 선례 | Nd PP 만 바꾸자 Nd–S 가 크게 달라지고 **대조군 P–S·Li–S 는 그대로** | `HZ-nd-icohp-june-nds-pp` · frozen-4f 결과 `citable: false`(비율·방향만) | `db/properties/nd_icohp_frozen4f_result_2026_09_23.json` |
| 우리 NEB 관행 | CI-NEB **이미지 7** · 하전 공공 + jellium · **셀 수렴 카드** · 결과 파일 전체 `retracted` (n_citable 0) · 인용 계약 2026-08-16: 단일 셀이면 **절대값 금지**(상 사이 비교만) | ⛔ `HZ-sei-neb-retracted` BLOCKED — **값을 여기 옮기지 않는다** | `db/properties/sei_neb.json` |
| 우리 "황 전환" 계산 (산화 방향) | 0 K grand-potential ESW — comp1 onset 반응 `Li₆PS₅Cl → Li₃PS₄ + LiCl + S + 2Li⁺ + 2e⁻` (S²⁻-limited) · **층①(분해 onset)** 으로 한정 · 속도론 0 | 인용 가능 (층① 명시 조건) | `litdb/our_dft_baseline.md` |
| 갭 규율 | fixed-occupation nscf VBM/CBM 고유값만 · **DOS 문턱 판독 금지** | 규약 | CLAUDE.md §데이터 규율 |
| 열린 껍질 보고량 규율 | *"admissible state 가 여럿인데 선택·집계 규칙이 없으면 스칼라 보고량은 정의되지 않는다. 열린 껍질 · 자성 기판 · 산화환원 활성은 그 위험 신호다"* (회신 N) | 규약 | CLAUDE.md §계산 규율 · `kb/methodology/estimand_before_running_2026_08_28.md` |
| 수계 C5 (Zn²⁺ 용매화) 설계 | **ORCA r2SCAN-3c + CPCM** · 보고량 = **리간드 교환에너지 + Marcus λ(4점법)** · *"Zn²⁺·Cu 는 둘 다 d¹⁰ 닫힌껍질이라 SDCP 같은 스핀 지옥은 없다"* | 스코핑 후보 (착수 전) | `kb/projects/zn_alzib_dft_md_contribution_2026_09_03.md` C5 · §4 |
| 수계 MD 규율 | UMA 검증 영역 = LPSCl 계열 → **수계는 검증 밖 · MLIP 단독 판정 금지** | 규율 | 같은 카드 C7 · `comparison_vs_ours.md` §K-4 |

### 7c. 트랙별 판정

#### 7c-1. 황 전환 반응 계산 방식 — 0923 Li–S 세 편 + 이 편 + 우리

| 편 | 계산 층위 | 전환 반응 자체 (단계별 ΔG · 절단/핵생성 TS) | "장벽" 서술의 출처 | 용매·환경 |
|---|---|---|---|---|
| `[Zhang26PI3]` (0923-1) | CP2K AIMD 1건 (PBE-D3(BJ) · 231 원자 · 800 K 단일 궤적) | 0 | 없음 | 고체 유리 |
| `[Liu26Sn]` (0923-2) | VASP PBE-D 바닥상태 서술자 (iCOHP · 결합길이 · Bader · ELF · 분자흡착) | 0 | iCOHP 추론 + 단일온도 Tafel "상대 활성화에너지" | 고체 계면 (진공 슬랩) |
| `[Wang25MIEC]` (0923-3) | PBE 갭·DOS · AIMD Arrhenius · LOBSTER | 0 | 없음 | 고체 유리 (모델이 실험 유리와 다름) |
| **이 편 `[Li26MnS]`** | 클러스터 S–S ICOHP·PDOS (진공) · 착물 결합 (SMD) · 벌크 NEB · 고전 MD | **0** | S–S ICOHP 추론 (NEB 는 이온 이동) | **수계인데 핵심 계산은 진공** |
| 우리 ESW (사용자 1저자 트랙) | 0 K grand-potential (pymatgen 상평형) | 열역학 onset 만 · 속도론 0 | 없음 — **층①(분해 onset)** 으로 한정 | 고체 |

- **공통점**: **네 편 모두 황 전환의 속도론(전이상태)을 계산하지 않는다.** 둘(`[Liu26Sn]` · 이 편)은 **결합 서술자 → "장벽 저하"** 로 추론하고 제목·초록에 "barrier" 를 쓴다.
- **이 편만의 것**: 유일하게 **NEB 가 있다** — 그러나 전환이 아니라 **벌크 이온 이동**이고, 절대값은 오히려 결론(빠른 고상 경로)을 약하게 만든다(§5.5).
- **우리와의 차이는 계산이 아니라 서술 범위**다: 우리 ESW 도 속도론이 없지만 보고량을 **"열역학 onset(층①)"** 으로 적는다. 우리 쪽에서 이 논문처럼 "장벽" 을 쓰려면 **보고량 카드**(`kb/templates/estimand_card.md`)부터 — CLAUDE.md §계산 규율.
- 액체 Li–S 촉매 문헌에서 흔한 **단계별 ΔG 도표 · Li₂S 분해 CI-NEB** 는 네 편 어디에도 없다(우리 배경지식 — 이 문헌군의 관행 서술이고 특정 편을 인용한 것이 아니다).

#### 7c-2. ICOHP — S–S 는 우리 "S-S" 와 다른 결합이다

- **값 비교 금지.** 그들 S1–S2 는 **공유 폴리설파이드 결합(1.94–2.19 Å, −2 ~ −3.7 eV)**, 우리 원장의 "S-S" 는 아지로다이트 **케이지의 비결합 S···S(≈3.5–3.6 Å, ≈ −0.11 eV/bond)** 다 — `[Liu26Sn]` 의 "P–S" 와 같은 **이름만 같은 다른 결합** 사례.
- **방법 차이**: 그들은 LOBSTER 기저·밴드 수·spilling 을 적지 않았다. 우리 원장에는 **기저 부족으로 ICOHP 가 수십 % 틀린 선례**(minimal-basis P–S −5.12 · Li–X −0.8)와 **TM/RE PP 하나로 M–S ICOHP 가 크게 바뀐 선례**(Nd)가 있다 — Mn 3d 계는 같은 위험 부류다.
- ⭐ **가져올 것 = 설계**: 우리 Nd frozen-4f 대조군은 **"바꾼 것(Nd PP)과 안 바뀌어야 할 것(P–S·Li–S)을 같이 보였다"**. 이 편 `Fig. 4d,e` 에는 **대조 결합이 없고 출발 기하도 모델마다 다르다.** 우리가 결합 서술자를 비교할 때는 ① 같은 출발 기하 ② 효과권 밖 대조 결합 ③ 배치가 여럿이면 집계 규칙 — 셋을 결과 전에 적는다 (우리 기존 관행의 재확인 · 새 규칙 아님).
- **ICOHP ≈ 결합길이의 재진술**(세 점 기울기 6.6–6.9 eV Å⁻¹): 두 증거로 세지 않는다. 우리 원장도 결합별 ICOHP–거리 상관을 이미 기록한다(`bonds.json` `icohp_distance_correlation_eV_per_Angstrom`) — 같은 점검을 **문헌을 읽을 때도** 건다.

#### 7c-3. NEB — 규약 대조 + "장벽 → 홉 수" 검산

| 항목 | 이 편 | 우리 (SEI NEB 관행) |
|---|---|---|
| 이미지 | 중간 3 (`figure-read`) | 7 |
| 셀 수렴 | 슈퍼셀 자체 미기재 | 셀 수렴 카드 · 미시험이면 절대값 금지(인용 계약 2026-08-16) |
| 이동종 전하 | 미기재 | 하전 공공 + jellium (기록) |
| 강상관 d 전자 | +U 없음 · 자기 배열 미기재 (Mn²⁺ d⁵) | 해당 계 없음 (Li₂S · Li 금속 · Li₃Nd) |
| 인용 상태 | — | ⛔ 파일 전체 retracted — **값 비교 안 함** |

- 우리 인용 계약을 이 편에 그대로 대면: 셀 수렴 정보가 없으므로 **절대값 인용 불가 · 상대 비교만** — 1저자 인용정책(2026-09-18, *"상대 차이가 난다 이 정도로만"*)과 같은 결론이다. 그리고 그 상대차조차 +U·자기배열·전하 처리 조건부다.
- ⭐ **가져올 것 = 검산 형식** (후보 · 결정 아님): 장벽을 인용할 때 **N_hop = ν₀·exp(−E‡/k_BT)·t_exp** 를 한 줄 붙인다. 이 편은 이 한 줄로 **"0.97 eV 로는 4 분에 0.1 홉"** 이 드러나 자기 결론과 긴장한다. 새 계산 0 · 우리 NEB 가 인용 가능해질 때 보고 형식에 넣을 후보 (트랙: 우리 DFT 기준선 = 사용자 1저자 트랙이라 사용자 판단으로 채택 가능 · ⚠ li2s 트랙의 Li₂S NEB 에 붙이려면 그 트랙은 외부 1저자라 회신 필요).

#### 7c-4. 용매 · 클러스터 — 수계 축 스코핑 카드 C5 · C7 (§K)

- **C5 (용매화 · 탈용매화)**: 이 편의 **클러스터-연속체(M06-2X/def2-TZVP/SMD)** 는 우리 C5 계획(**ORCA r2SCAN-3c + CPCM**)과 **같은 계열의 방법 선례**다. 그러나:
  1. **보고량이 다르다** — 그들 = 착물 **총** \|E_b\| · 우리 = **리간드 교환에너지 + Marcus λ**. 이 편에서 총량(LiCl₄ 최저) ↔ 리간드당(LiCl₄ ≈ Mn(H₂O)₃Cl₃) 이 뒤집히는 것이 **우리 설계가 필요한 외부 반례**다.
  2. 🔴 **열린 껍질**: C5 카드는 *"Zn²⁺·Cu 는 d¹⁰ 닫힌껍질이라 스핀 지옥은 없다"* 로 면제됐다. **Mn²⁺(d⁵) · Ni²⁺(d⁸)** 로 넓히는 순간 그 면제가 사라진다 — 이 편이 멀티플리시티를 **적지 않은** 바로 그 자리다. ⇒ C5 카드에 한 줄 후보: *"대상 이온이 열린 껍질이면 전하·멀티플리시티·(다핵이면) 자기 배열을 결과 전에 선언"*. (트랙: 수계 협업 스코핑 — 후보일 뿐 · 결정 아님)
  3. 매질: SMD **물**을 20 m LiCl 에 그대로 — 우리 C5(2 M ZnSO₄ 계)도 연속체 매질 선택을 카드에 적어야 한다(같은 질문).
- **C7 (MD · 용매화 껍질 조성)**: 이 편의 고전 MD 는 **선례이자 위험 사례**다 — 비분극 고정전하 힘장 · 20 m · 5 ns 한 궤적 · Li 배위 미보고 · 종 분포 대신 평균 CN. **앵커가 아니다.** UMA 수계 검증 밖이라는 §K-4 규율은 그대로다.
- 상세 연결표는 `comparison_vs_ours.md` **§K-13**.

#### 7c-5. PDOS · 갭 — 우리 규율로 보면

- 이 편의 *"narrow the band gap"* 은 **갭이 안 보이는 스미어링된 클러스터 PDOS** 에서 나왔다. 우리 규율(fixed-occ nscf 고유값 · DOS 문턱 금지)로는 **갭 값을 읽을 수 없는 그림**이다.
- ⭐ **세 모델 모두 E_F 에 spin-up 상태**가 걸린 모양은 `[Liu26Sn]` §5.2 의 경고(계면 모델의 전하중성·틈상태)와 같은 부류다. 우리 W_ad 슬랩·계면 모델에 걸기로 한 **"E_F 근처 음이온 성분 · 부분 점유 상태 점검"**(`[Liu26Sn]` §11-② 후보)의 **두 번째 외부 반례**다.

#### 7c-6. li2s 트랙 (⚠ 외부 1저자 트랙) — 참고 정보만 (판단 아님)

- 값으로 넘길 것은 없다 (계 · 방법 · 보고량이 전부 다르다).
- 💬 **넘길 참고 정보 하나**: *"평균 조성은 3원 단일상과 혼합물을 가르지 못한다"* — 이 편의 Li₄Mn₆S₈ = 2Li₂S + 6MnS. li2s 트랙의 *"볼밀 LPSCl@Li₂S 계면상이 생기나"* 질문도 XPS·Raman 이동에 기대는 구조가 같다. 구조 민감 증거(격자상수 변화 + **혼합물 대조군**)가 필요하다는 방법론적 반례로만 쓸 수 있다 — 채택 여부는 그 트랙 외부 1저자의 판단이다.

### 7d. 요약 (5줄)

1. **값 비교 대상 0** — 수계 · 계 · 방법 · 보고량이 다 다르다. comparison 에는 `🔧 방법 원전`(§J-48) + 수계 축 연결(§K-13) 로만 둔다.
2. **황 전환 계산 방식**: 0923 세 편 + 이 편 **네 편 모두 전환 속도론 0** — 결합 서술자에서 "장벽" 을 추론한다. 우리 ESW 는 같은 한계를 **"층① 열역학 onset"** 으로 적는다는 점이 다르다.
3. **ICOHP**: 그들 S–S(공유) ≠ 우리 "S-S"(케이지 비결합). 가져올 것은 **대조 결합 + 같은 출발 기하** 설계 확인뿐.
4. **NEB**: 우리 인용 계약으로 보면 상대차만 · 그리고 **"장벽 → 실험 시간척도 홉 수"** 한 줄 검산이 이 편의 긴장을 바로 드러낸다 — 보고 형식 후보.
5. **수계 C5**: 클러스터-연속체 방법 선례이지만, **열린 껍질(Mn²⁺ d⁵) 이면 상태 선언** · **보고량은 리간드 교환에너지** — 둘 다 이 편이 반례다.

---

## 8. Post-processing ★

| 무엇 | 도구 (적힌 것 / 추정) | 수치화 · 플롯 · 기록 |
|---|---|---|
| 착물 결합에너지 | Gaussian 16 · \|E_b\| 식 | 막대 5개 + 착물 구조식, **숫자 미인쇄** · y축 *"Binding energy (−eV)"* (`Fig. 4c`) |
| 결합길이 | 미기재 (구조 렌더 — VESTA 류로 보임) | 막대 3개 + 인쇄값 · 모델 그림 위 S1/S2 화살표 (`Fig. 4d`) |
| COHP / ICOHP | **LOBSTER** (적힘) · 기저·spilling 미기재 | −COHP 곡선 3패널(**x축 범위가 패널마다 다름**) + 패널 안 세로 글씨 ICOHP 인쇄값 (`Fig. 4e`) |
| PDOS | VASP → LOBSTER 또는 VASPKIT 류(미기재) | S 원자 스핀 PDOS 3곡선 겹침 · E_F 확대 원 삽화 · 격자 ≈0.2 eV (`Fig. S25`) |
| NEB | VASP CI-NEB | 5점 + 스플라인(overshoot) · 구조는 도식으로 (`Fig. 4f,g`) |
| MD 구조 분석 | GROMACS → RDF · 누적 배위수 · VMD 스냅샷 | g(r) 실선 + CN 점선 이중축 (`Fig. S8`) · "free water fraction" 은 예고만 |
| EQCM 비율 | 자체 두 식(전하·질량 보존) | 이상 한계 72/285 ng mC⁻¹ 과 실측 222 비교 → n_Li · n_Mn (SI p.20) |
| DRT | 미기재 | R_d vs SoD 선그림 (`Fig. 4a`) |

---

## 9. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1a,b | 0.5 A g⁻¹ 충방전 곡선 · CV (Li⁺-S / Mn²⁺-S / Li⁺/Mn²⁺-S) + 반응경로 삽화 | (안 봄) — 값은 본문 |
| 1c,d | 율속 0.5–15 A g⁻¹ (15 A g⁻¹ 1012 mAh g⁻¹) · 5 A g⁻¹ 200 cyc (>900 mAh g⁻¹) | (안 봄) — S 질량 기준 · 3전극 반쪽셀 |
| 1e,f | S‖LiMn₂O₄ 풀셀 10 A g⁻¹ 650 cyc · 문헌 율속 비교 (refs 27–32) | (안 봄) — `Fig. 1f` 는 조건 혼재라 인용 금지 |
| 2a | in situ Raman 지도 — S₈(153·219·473) ↔ 황화물(≈610 cm⁻¹) 가역 | 정성 |
| 2b | 방전 생성물 Raman vs 표준 MnS (`figure-read ≈` 605 vs 640 cm⁻¹) | 넓고 약한 봉우리 = "무질서 Li–Mn–S" 해석의 근거 — S/N 낮음 |
| 2c | S 2p XPS D0–D100–C100 · 기준선 S₈ 164.3 · MnS₂ 162.85 · MnS 162.0 · Li_xMn_yS 160.5 eV (`figure-read`) | ⚠ D100 이중선 ≈160.6 eV 는 표준 Li₂S(160)에 0.5 eV — §5.6 |
| 2d | SXRD (λ 0.6887 Å) — (002) 12.18 → 12.08° (`figure-read`) | ⚠ 11.8° 배경 꺾임이 D0 에도 — 0.1° 판독 민감 |
| 2e | 0.1 m Li₂S + MnCl₂ UV-vis (S²⁻ 봉우리 `figure-read ≈`230 nm · 본문 240) + 분홍 MnS 침전 사진 | Mn²⁺ = 화학 트랩 — 방향만 |
| 2f | ICP Li/Mn 비율 한 사이클 (방전 말 Mn ≈60 % "Li₄Mn₆S₈") | ⚠ 평균 조성 = 2Li₂S + 6MnS 와 같음 |
| 2g | 방전 전극 Li/Mn 1–4 사이클 (Li 56 → 40 %) | 3 사이클 안정 |
| 3a–c | in situ UV-vis 방전 중 (Li⁺ / Mn²⁺ / Li⁺/Mn²⁺) | "용해 억제" 의 가장 직접적 그림 — 오프셋·a.u. |
| 3d | EQCM 양이온 한계 모형 식 (Q = 2F·n_Mn + F·n_Li · Δm = M_Mn·n_Mn + M_Li·n_Li) | ⭐ 두 식 연립 → 겉보기 양이온 비 — 단순·검산 가능 |
| 3e,f | EQCM Q-t · Δm (Mn²⁺: 순 손실 ≈ −10 ng · Li⁺/Mn²⁺: 0 ↔ 30 ng 주기) | 우리 검산 일치 (Li 45 %) |
| 3g,h | ToF-SIMS 깊이 프로파일 + 지도 (S⁻ · HS⁻ · S₂⁻ · F⁻) | ⚠ HS⁻ ≈40× 미논의 (§10-⑩) |
| 4a | in situ EIS-DRT 확산저항 R_d vs SoD (Mn²⁺ ≈464 → 50 Ω) | 겉보기 저항 — 장벽 아님 |
| 4b | 정상상태 CA 전위 계단 (−0.3 ~ −0.6 V 고활성) | y축 a.u. — 정량 불가 |
| 4c | 착물 결합에너지 5종 (`figure-read ≈` LiCl₄ 1.78 · Mn(H₂O)₆ 1.83 · O₅Cl 2.18 · O₄Cl₂ 2.48 · Mn(H₂O)₃Cl₃ 2.63 eV) | ⭐ **리간드당 역전의 교보재** — 우리 C5 는 교환에너지로 (§7c-4) · ⛔ 탈용매화 장벽으로 인용 금지 |
| 4d | S1–S2 결합길이 2.08 / 1.94 / 2.19 Å (인쇄값) + 클러스터 모델 (Mn ≈2 + S ≈8, `figure-read`) | ⚠ Mn(H₂O)₃Cl₃ = 강화 · 모델 기하 상이 · 대조 결합 없음 (§5.3) |
| 4e | S1–S2 −COHP 3패널 + ICOHP −2.72 / −3.69 / −1.99 eV (인쇄값) | ⚠ 패널별 x축 범위 다름 — 우리 그림은 같은 축으로 · ICOHP ≈ 결합길이 재진술 |
| 4f | MnS 속 Li⁺/Mn²⁺ 이동 경로 도식 (이미지 0–4) | 도식 — 셀 판독 불가 |
| 4g | CI-NEB 에너지 (`figure-read ≈` Li 0.97 · Mn 1.19 eV) | ⭐ **"장벽 → 홉 수" 검산 교보재** (§7c-3) · ⛔ 절대값 인용 금지 · 스플라인 overshoot |
| 5a | Ni²⁺-S vs Li⁺/Ni²⁺-S 3번째 사이클 + D100 XPS (Li_xNi_yS ≈161 eV) | 배정이 XPS 새 성분 하나에 기댐 |
| 5b | Zn²⁺-S vs Li⁺/Zn²⁺-S + D100 XPS (Li_xZn_yS ≈161 eV) | 〃 · 평탄 전위 차 작음 |
| 5c | 개념도 — bond breaking · diffusion 두 언덕 (M²⁺-S vs Li⁺ promoted) | ⛔ **y축 눈금 없음 · 두 언덕 모두 계산 안 됨** — 장벽 근거로 쓰지 않는다 |
| S1 | 첫 사이클 충방전 0.5 / 0.2 / 0.1 A g⁻¹ (−0.6 V Li₂S 산화 평탄 = Mn²⁺ 농도분극) | (안 봄) — 노트는 텍스트로 읽음 · ⚠ 고율 함의 §10-⑫ |
| S2 | 고로딩 3.13 · 4.83 mg cm⁻² 율속 | (안 봄) |
| S3 | 반쪽셀 율속 곡선 · S‖LMO 풀셀 곡선·율속 | (안 봄) |
| S4 | 탈결합 알칼리 Zn‖S 셀 (Nafion · LiOH + Zn(OAc)₂) | (안 봄) |
| S5 | Li⁺/Mn²⁺ 비율별 전해질 사진 (연주황 → 초록) | (안 봄) |
| S6 | 전해질 이온전도도·점도 · O–H Raman 3성분 · UV-vis | (안 봄) |
| S7 | EPR 1M · 1M10L · 1M20L (6선 → g ≈ 2.00 단일선) | (안 봄) |
| S8 | MD 스냅샷 1M · 1M20L + Mn–Cl · Mn–O RDF/CN (`figure-read ≈` 1M20L CN 2.7 · 3.3) | ⚠ Li 배위 없음 · 색 배정 불확실 · C7 위험 사례 (§5.1) |
| S9 | XANES (방전 전극 셋) + 고각 SXRD ((110) 19.74 → 19.65°) | ⚠ **본문 "pristine Li₂S and MnS" 와 불일치 — 표준 시료 없음** · a 축도 변함 |
| S10 | 표준 Li₂S (Li₂S 160 · Li₂S₂ 161.8) · MnS (162 eV) XPS | ⚠ 표준 Li₂S 가 Li₂S₂ 우세 = 산화된 기준 |
| S11 | Li₂S + MnCl₂ 침전 XRD (MnS) | (안 봄) |
| S12 | Li₂S₂ · Li₂S₄ · Li₂S₆ · Li₂S₈ + Mn²⁺ UV-vis | (안 봄) |
| S13 | 세척액 ex situ UV-vis (황화물 흡수 없음) | (안 봄) — 혼합물 가설에 불리한 유일한 증거 (§5.6-6) |
| S14 | 방전 전극 SEM + EDS (Mn²⁺-S vs Li⁺/Mn²⁺-S) | (안 봄) |
| S15 | TEM · HRTEM (0.299 / 0.341 / 0.322 nm = γ-MnS (101)/(100)/(002)) | (안 봄) — 값은 SI 텍스트 · 기준 d 없음 |
| S16 | LiCl 농도별 충방전 + S 2p XPS (고농도에서 SO₃²⁻/SO₄²⁻ 소멸) | (안 봄) |
| S17 | ChCl 대조 전해질 (1M+10L+10ChCl · 1M+20ChCl) | (안 봄) |
| S18 | in situ UV-vis 셀 구성도 | (안 봄) |
| S19 | in situ DEMS (H₂S 거의 없음) | (안 봄) |
| S20 | 공전극 EQCM 배경 · 4 사이클 질량 손실 | (안 봄) — 계산 노트는 텍스트로 읽음 |
| S21 | 자가방전 24 h (CE > 90 % vs < 10 %) · 48 h | (안 봄) |
| S22 | GITT 곡선·분극 비교 | (안 봄) |
| S23 | in situ EIS + DRT (방전, 세 계) | (안 봄) |
| S24 | in situ EIS + DRT (충전, Li⁺/Mn²⁺) | (안 봄) |
| S25 | S 원자 PDOS (Mn(H₂O)₆ · Mn(H₂O)₃Cl₃ · LiCl₄) | ⛔ **본문 "갭 축소" 와 불일치 — 세 곡선 모두 E_F 에서 유한** · 부분 점유 점검의 반례 (§5.4 · §7c-5) |
| S26 | Ni²⁺-S / Li⁺/Ni²⁺-S 장기 사이클 + XANES | (안 봄) |
| S27 | Zn²⁺-S / Li⁺/Zn²⁺-S 장기 사이클 + XANES | (안 봄) |
| Table S1 | MD 계 조성 (1M · 1M1L · 1M10L · 1M20L 의 Mn · Cl · H₂O · Li 개수) | 우리 검산: 몰랄 농도 전부 일치 · 20L 없음 |

---

## 10. 비판 — 이 논문의 약한 곳 ★

① **장벽 주장의 비약 (가장 크다).** 초록 *"lowers the redox barrier"* · 결론 *"weakens the S−S bonds, and promotes their cleavage"* — **산화환원·절단 장벽은 계산되지 않았다.** 근거는 정적 S–S 결합길이·ICOHP(진공 · 단일 배치)이고, 계산된 유일한 장벽은 벌크 MnS 이온 이동이다. `Fig. 5c` 의 두 언덕은 눈금 없는 모식도다. (§6)

② **+U 없음 · 자기 배열 미기재 · 전하 미기재.** Mn²⁺ d⁵ 황화물·착물에 PBE 단독을 쓰고, 다핵(Mn 2–3개) 계의 자기 배열도, 이동종·클러스터의 전하도 적지 않았다. d⁵ 황화물은 PBE 에서 전자 국재·갭이 크게 틀어질 수 있다(배경지식). NEB 의 Li 삽입에서 **여분 전자가 어디로 가는지** 가 장벽을 바꿀 수 있는데 처리 방식이 없다. 우리 규율로는 **상태 선언 없는 열린 껍질 계의 스칼라 보고량**이다. (§4c · §7c-4)

③ **"탈용매화" 를 총 결합에너지로 대리.** LiCl₄ vs Mn(H₂O)₆ **0.05 eV** · 리간드당 LiCl₄ ≈ Mn(H₂O)₃Cl₃ · \|·\| 정의 · 전하가 다른 종을 한 축에 · LiCl₄ 종 선택 근거 없음(MD 에 Li 배위 없음) · SMD 물 매질을 20 m 에. (§5.2)

④ **S–S 약화의 비통제 비교 + 불리한 결과의 침묵.** 세 모델의 클러스터 기하가 다르고 대조 결합이 없다. 무엇보다 **1M20L 의 Mn 종(Mn(H₂O)₃Cl₃)이 S–S 를 강화**한다는 자기 결과를 논의하지 않는다. ICOHP 는 결합길이의 재진술이다. (§5.3)

⑤ **PDOS 서술–그림 불일치.** "갭이 좁아진다" 인데 세 곡선 모두 갭이 없다. 궤도 분해 없이 "S 3p", 클러스터로 "고유 전자전도도". (§5.4)

⑥ **NEB 가 결론을 떠받치지 못한다.** 벌크 MnS(계면·Li–Mn–S 아님) · 중간 이미지 3 · "same path" 강제 · 그리고 **절대값 0.97 eV 로는 15 A g⁻¹ 방전 4 분 동안 ≈0.1 홉** — "빠른 고상 경로" 와 정면으로 긴장한다. (§5.5)

⑦ **계산 층위의 불일치.** Gaussian(SMD) · VASP 진공 클러스터 · VASP 벌크 · 고전 MD 가 **서로 다른 환경**에서 **서로 다른 대상**을 잰다. 한 계(예: 같은 황 종 + 같은 착물)를 여러 수준으로 교차검증한 것이 없다. 두 ENCUT(520 / 500 eV)이 어느 계산인지도 대응이 없다. (§4a · §4d)

⑧ **3원 생성물 증거가 약하다.** Li₄Mn₆S₈ = 2Li₂S + 6MnS(평균 조성으로 구분 불가) · XPS 새 봉우리 ≈160.5 eV 가 표준 Li₂S(160)에 0.5 eV 이고 **표준 Li₂S 자체가 산화(Li₂S₂ 우세)** · XANES 본문은 "pristine 표준 사이" 인데 **그림에 표준이 없다** · SXRD (002) 0.1° 이동이 D0 에도 있는 배경 꺾임 옆 · TEM "팽창" 에 기준 d 가 없고 우리 환산으론 수축 방향. 혼합물에 불리한 증거는 세척액 UV-vis 하나. (§5.6)

⑨ **MD 의 한계.** 비분극 고정전하(SPC/E + 12-6 Merz)를 20 m 에 · Merz 세트 미기재 · 5 ns 한 궤적 · 오차막대 없음 · **예고한 free water fraction 미보고** · Li 배위 미보고 · 평균 CN 을 "thermodynamically stable complex" 로. (§5.1)

⑩ **HS⁻ 40× 미논의.** ToF-SIMS 에서 Li⁺/Mn²⁺-S 전극의 HS⁻ 가 Mn²⁺-S 보다 ≈40배(`figure-read`) — 물과의 반응(가수분해·양성자화 황 종)일 수 있는데 한 줄도 없다. (§5.7)

⑪ **자잘한 불일치**: S²⁻ UV 흡수 240 nm(본문) vs `figure-read ≈`230 nm(`Fig. 2e`) · `Fig. 4e` 패널별 x축 범위 다름 · `Fig. 4c` 값 미인쇄 · NEB 스플라인 음수 overshoot · MD 스냅샷 색 범례 없음 · 착물 5종 중 둘은 그림에만 있고 이름 없음.

⑫ **고율에서 Li₂S 경로를 배제하지 않았다** (우리 추론). SI `Fig. S1` 노트는 **0.5 A g⁻¹ 에서도 Mn²⁺ 농도분극 → Li⁺-S 경로 → 추가 Li₂S** 가 생긴다고 스스로 쓴다. **15 A g⁻¹ 는 30배 전류**라 Mn²⁺ 결핍이 더 심할 것이다 — 그렇다면 1012 mAh g⁻¹ 의 상당 부분이 **Li⁺-S(Li₂S) 경로**일 가능성이 있는데, 고율에서의 생성물 분석(XPS·ICP)은 없다(생성물 분석은 저율 채취로 보인다 — 채취 전류 미기재).

⑬ **전위 축·셀 형식.** 전부 vs Ag/AgCl 3전극 반쪽셀 · AC 상대극 대과잉 · S 질량 기준 — 셀 수준 비교가 아니다(저자도 결론에서 인정).

---

## 11. 적용 인사이트 ★ (우리 작업에 — 날카로운 것 순)

① **"장벽 → 실험 시간척도 홉 수" 한 줄을 장벽 인용 형식에 넣자** (후보 · 결정 아님 · 새 계산 0). N_hop = ν₀·exp(−E‡/k_BT)·t 만으로 이 편의 "0.97 eV 인데 빠른 고상 경로" 긴장이 드러났다. 우리 NEB 는 지금 인용 대상이 없지만(`sei_neb.json` retracted), 살아날 때 **셀 수렴 + 이 한 줄**을 같이 싣는다. (트랙: 우리 DFT 기준선 — 사용자 1저자 판단)

② **열린 껍질 금속 착물은 상태부터 선언** — 수계 C5 카드는 Zn²⁺(d¹⁰)라 면제였지만, 이 편처럼 **Mn²⁺(d⁵)·Ni²⁺(d⁸)** 로 가면 전하·멀티플리시티·자기 배열 선언 없이는 결합에너지도 ICOHP 도 **스칼라가 아니다**(회신 N). C5 카드에 한 줄 후보. (트랙: 수계 협업 스코핑 — 후보)

③ **탈용매화 보고량 = 단계별 리간드 교환에너지** — 우리 C5 설계가 맞다는 외부 반례. 총량 서열이 리간드당으로 사라지는 것을 이 편 `Fig. 4c` 에서 바로 보여 줄 수 있다 (우리 카드의 "왜 교환에너지인가" 한 줄 근거로 쓸 만하다).

④ **결합 서술자 비교 = 같은 출발 기하 + 효과권 밖 대조 결합 + (배치가 여럿이면) 집계 규칙** — 우리 Nd frozen-4f 대조군 설계가 정답형이고 이 편 `Fig. 4d,e` 가 반면교사다. ICOHP 를 결합길이와 **별개 증거로 세지 않는다**.

⑤ **그림 양식 반면교사** (house style 재확인): 비교 COHP 패널은 **같은 x축** · 막대에는 **값 인쇄** · PDOS 는 **에너지 격자·스미어링·"어느 원자"** 를 캡션에 · NEB 는 **이미지 점 + overshoot 없는 보간**(또는 점만) · 구조는 도식이 아니라 실제 렌더 + 원자 수.

⑥ (li2s 외부 1저자 트랙 참고 정보 — 판단 아님) *"평균 조성 = 혼합물과 구분 불가"* → 구조 민감 증거 + 혼합물 대조군.

---

## 12. 인용 가능 문장 (영문 초안 — 조건 포함)

- *"Li et al. (2026) report that adding 20 m LiCl to a 1 m MnCl₂ aqueous electrolyte enables an S@AC half-cell to deliver 1012 mAh g⁻¹ (sulfur basis) at 15 A g⁻¹, attributing it to a Li⁺-assisted, solid-state-dominated conversion toward a Li–Mn–S product whose ICP-derived apparent average composition is close to Li₄Mn₆S₈."*
- *"Their computational support consists of static descriptors — a longer terminal S–S bond and a less negative ICOHP for a Mn–S cluster next to a model LiCl₄ complex than next to Mn(H₂O)₆ (PBE-D3, vacuum, single configurations) — implicit-solvent (SMD) cluster binding energies, and a bulk-MnS CI-NEB in which Li migrates with a lower barrier than Mn; no redox or S–S cleavage barrier is computed."* (NEB 수치는 붙이지 않는다 — `figure-read` · 셀 미기재)
- *"In the same calculations, the Cl⁻-rich Mn(H₂O)₃Cl₃ complex — the Mn species the authors' MD assigns to the Li-rich electrolyte — shortens rather than lengthens the S–S bond (1.94 vs 2.08 Å for Mn(H₂O)₆), so the net effect in the optimized electrolyte is not established by the DFT."*

---

## 13. 주의 / 한계 (인용 규율)

- ⛔ **"Li⁺ 가 S–S 절단(산화환원) 장벽을 낮춘다 (DFT)"** — 계산된 장벽이 없다.
- ⛔ **NEB 0.97 / 1.19 eV 절대값** — `figure-read` · 셀·k·+U·자기 배열·전하 미기재. 쓰려면 *"벌크 MnS · PBE(+U 없음) · 상대차 ≈0.2 eV"* 조건과 함께.
- ⛔ **S–S ICOHP 를 우리 ICOHP 와 같은 표에** — 우리 "S-S" 는 케이지 비결합 S···S 다(다른 결합) · 그들 LOBSTER 조건 미기재.
- ⛔ **\|E_b\| 를 탈용매화 에너지·장벽으로** — 총 결합 크기이고, 리간드당으로는 서열이 사라진다.
- ⛔ **PDOS "band gap narrowing"** — 그림에 갭이 없다.
- ⛔ **"Li₄Mn₆S₈ 상"** — ICP **겉보기 평균 조성**으로만 (= 2Li₂S + 6MnS 조성).
- ⛔ **XANES 를 "순수 Li₂S·MnS 표준 사이"** 로 — 그림에 표준 시료가 없다.
- ⚠ 전위는 전부 **vs Ag/AgCl**(3전극) — Li/Li⁺ 로 환산하지 않는다.
- ⚠ 용량은 **S 질량 기준 반쪽셀** — 셀 에너지밀도로 쓰지 않는다.
- ⚠ **수계** — 우리 황화물 SE 물성 4축(σ · ESW · 기계 · 갭)과 **수치로 섞지 않는다.** 방법 선례로만.
- ⚠ MD 배위수(`figure-read`)는 단일 궤적 · 비분극 힘장 — 정량 인용하지 않는다.

---

## 14. 기법 용어 미니사전

- **클러스터-연속체(cluster-continuum) 용매 모형** — 이온의 1차 배위껍질(물·음이온)은 원자로 두고, 그 바깥은 유전체 연속체(SMD·CPCM·PCM)로 근사한다. 싸고 표준적이지만, 연속체의 유전율·매개변수가 **실제 매질**(여기선 20 m LiCl)과 맞는지가 문제다.
- **SMD** — Truhlar 그룹의 용매화 모형(전하밀도 기반 연속체 + 표면장력 항). 매질을 "물" 로 지정하면 순수 물의 매개변수를 쓴다.
- **M06-2X / def2-TZVP** — M06-2X 는 HF 교환 54 % 의 혼성 메타-GGA 범함수(주족 열화학·비공유 상호작용용으로 널리 쓰인다), def2-TZVP 는 삼중제타 + 분극 가우스 기저. 전이금속 계에는 범함수 선택 근거를 적는 것이 관례다(우리 배경지식).
- **결합에너지와 BSSE** — E_complex − E_fragments. 가우스 기저에서는 조각이 이웃 기저를 빌려 쓰는 **기저 중첩 오차(BSSE)** 로 결합이 과대평가되므로 counterpoise 보정을 흔히 한다. 부호(음수 = 결합)를 지우는 \|·\| 정의는 드물다.
- **리간드 교환에너지** — [M(L)ₙ] + L′ → [M(L)ₙ₋₁L′] + L 의 반응 에너지. 한 번에 **한 리간드**를 바꾸는 양이라 탈용매화의 **첫 단계**와 직접 연결된다(총 결합에너지와 다르다).
- **멀티플리시티 (2S+1)** — 홀전자 스핀 상태. 고스핀 Mn²⁺(d⁵)는 S = 5/2 → 6중항. 계산에서 멀티플리시티를 정하지 않으면 **어느 상태의 에너지인지** 가 정의되지 않는다. 다핵 계면 각 Mn 의 스핀 정렬(FM/AFM)도 선언해야 한다.
- **DFT+U** — 국재된 d/f 전자의 자기상호작용 오차를 줄이려 Hubbard U 를 더하는 보정. 전이금속 산화물·황화물에서 갭·전자 국재·결함 에너지를 크게 바꾼다.
- **COHP / ICOHP** — 두 원자 사이 전자 상태를 결합(−)/반결합(+)으로 나눈 에너지 분해(COHP), E_F 까지 적분한 값(ICOHP, 더 음수 = 더 센 공유결합). LOBSTER 로 평면파 계산을 국소 기저에 투영해 얻고, 투영 품질은 **charge spilling**(우리 규약 < 5 %)으로 본다. 그림에선 흔히 −COHP 를 그린다.
- **PDOS 와 갭** — 원자·궤도별로 나눈 상태밀도. 스미어링을 크게 하면 작은 갭이 메워져 보인다. 우리 규율은 갭을 **fixed-occupation nscf 의 VBM/CBM 고유값**으로만 읽는다.
- **CI-NEB** — 두 끝점 사이 이미지 사슬을 이완해 최소에너지 경로와 전이상태를 찾는다. climbing image 가 꼭대기에 올라간다. 이미지가 적으면 경로가 덜 이완되고 보간 곡선이 흔들린다.
- **시도 진동수 ν₀ · 홉 속도** — 전이상태 이론의 Γ = ν₀·exp(−E‡/k_BT). ν₀ 는 보통 10¹²–10¹³ s⁻¹ 로 가정한다. 298 K 에서 E‡ 0.1 eV 차이는 속도 ≈50배 차이다.
- **water-in-salt (WiSE)** — 물보다 염이 많은(질량 기준) 초고농도 수계 전해질. 자유 물이 줄어 전기화학 창이 넓어지고 부반응(황 과산화 · H₂)이 줄어든다.
- **SPC/E · 12-6 Merz 이온 파라미터** — SPC/E 는 3점 고정전하 물 모형, Merz 파라미터는 PME 와 호환되게 맞춘 이온의 Lennard-Jones(12-6) 매개변수(수화 자유에너지·이온–산소 거리 등 목표별 세트가 있다). 비분극 고정전하라 초고농도에서 이온 응집을 과대평가하는 경향이 알려져 있다.
- **RDF g(r) · 누적 배위수** — 중심 이온에서 거리 r 에 이웃이 얼마나 있는지(g(r))와 그 적분(CN). 평균 CN 은 **종 분포**가 아니다.
- **EPR 교환 좁아짐** — 고립 Mn²⁺ 는 핵스핀(I = 5/2) 때문에 6선이 보이지만, 이웃 Mn²⁺ 끼리 교환결합이 초미세결합보다 빨라지면 6선이 한 줄로 합쳐진다.
- **S K-edge XANES** — 황 1s → 빈 3p 전이. 흡수단 위치가 황 산화상태를, 백색선 모양이 결합 환경을 반영한다. ≈2482 eV 의 강한 선은 황산염(S⁶⁺)의 지문이다.
- **γ-MnS** — 섬아연석(wurtzite)형 육방 MnS(준안정). 안정상은 암염형 α-MnS. (100)·(002)·(101) 반사가 γ 상의 지문이다.
- **EQCM (전기화학 수정진동자 저울)** — 전극 질량 변화(ng)를 공진 주파수로 잰다. Δm/ΔQ 를 이상 반응(여기선 Li-only · Mn-only)의 M/(zF) 와 비교해 무엇이 드나드는지 추정한다. 음이온·용매 공흡착을 무시하면 "겉보기" 값이다.
- **DRT (이완시간 분포)** — 임피던스를 시정수 분포로 풀어 과정별 저항을 가른다. 봉우리 넓이가 저항이다.
- **ToF-SIMS** — 표면을 이온빔으로 스퍼터링해 나온 2차 이온 질량을 잰다. 깊이 프로파일은 스퍼터 시간 축이다. 정량이 아니라 상대 세기다.
- **르샤틀리에형 이동** — 한 종(S²⁻)을 침전으로 계속 빼면 평형이 그 종을 만드는 쪽(긴 사슬 → 짧은 사슬)으로 움직인다.

---

## 15. 열린 질문 (토론용)

- Q1. 1M20L 에서 황 종 옆에 실제로 붙는 것은 LiCl₄ 류 Li 종인가, Mn(H₂O)₃Cl₃ 인가? — 둘의 결합 자유에너지(같은 수준·같은 용매 모형)를 비교하지 않으면 `Fig. 4d,e` 의 순효과가 정해지지 않는다.
- Q2. VASP 클러스터의 총전하·자기 배열은? — E_F 에 spin-up 상태가 걸린 PDOS(`Fig. S25`)와 1.94 Å 짧은 S–S 가 전자 수 설정의 산물인지.
- Q3. NEB 의 이동종은 중성 원자였나, 하전 셀이었나? +U 를 넣으면 Li/Mn 차가 유지되나?
- Q4. 15 A g⁻¹ 에서 채취한 전극의 생성물(Li : Mn 비 · XPS)은? — SI `Fig. S1` 노트대로라면 고율에서 Li₂S 경로가 커질 수 있다(§10-⑫).
- Q5. ToF-SIMS HS⁻ 40× 는 무엇인가 — 가수분해 산물(LiHS 류)이라면 "고상 Li–Mn–S" 서사와 어떻게 맞나?
- Q6. (우리) 수계 축 C5 를 Mn²⁺·Ni²⁺ 로 넓힐 일이 생기면, 카드에 **멀티플리시티·자기 배열 선언 + 리간드 교환에너지** 를 게이트로 박을 것인가? — 후보 · 결정 아님.
- Q7. (우리) "장벽 → 홉 수" 한 줄을 우리 장벽 보고 형식(NEB·MLIP-MD Ea 둘 다)에 넣을 것인가? — 사용자(DFT 기준선 1저자) 판단.
