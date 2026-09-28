---
title: "Chen D., He H., Zhang D., Wang H., Ni M. 2013 — Percolation Theory in Solid Oxide Fuel Cell Composite Electrodes with a Mixed Electronic and Ionic Conductor (Energies 6, 1632–1656)"
source_url: local-upload/30._Percolation_theory_in_solid_oxide_fuel_cell_composite_electrodes_with_a_mixed_electronic_and_ionic_conductor.pdf
source_url_note: "본문 PDF 25 쪽(MDPI Energies Article · 그림 12 · 표 1 · 식 (1)–(34) 라벨 43 · 참고문헌 39) — SI 없음(보충자료 언급 0). PDF 는 출판사 조판 파일(PScript5 · Acrobat Distiller 10.1.5, 생성 2013-03-11 = 게재일) 그대로이고 내려받기 표지가 없다. 그림 자동 13 장(본문 12 · 표 1 — 라벨 어긋남 0, tab_1 은 14 쪽 거의 전체로 과대 · fig_12 는 절 제목 포함으로 약간 과대) + 수동 1(tab_1_manual_p14) = 14 항목 전부 열어 봤다. 수치는 PDF 원본 래스터(그림 6–12 PNG) 픽셀 판독, 식은 쪽 렌더로 읽고 곡선 그림 일곱 장을 인쇄식으로 다시 계산했다. 3차 묶음 파일 30(2차 큐 번호와 별개) — 원장 행 '★ Chen·He·Zhang·Wang·Ni 2013'; 22호 ref 26. SOFC 해석 모형 편 — ASSB 아님 · 실험 0. 원자료는 커밋하지 않는다."
source_doi: 10.3390/en6031632
source_license: "© 2013 by the authors; licensee MDPI, Basel, Switzerland — 오픈액세스(1 쪽 OPEN ACCESS · 25 쪽 Creative Commons Attribution 3.0 표시). 이 digest 는 인용 · 요약 · 재현 계산만 담는다"
pdf_sha256: b67d3b8c188ff0913e047c734703a0266af9b57d078a68ed186635bc563fd7d4
ingested: 2026-09-28
sha256: 446aa66f9f8aabdaf5f4e8a0bf2e3130e75bf9f9aa81cf952fdafd0f9ba677ea
---
# 수집 목적

`assb` 섹션 **68호** — **3차 묶음 파일 30**(3차 묶음 열째 편). 3차 묶음의 파일 번호는 2차 묶음 "큐 N" 번호(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-d, 큐 1–59)와
**별개**다 — 이 편은 "큐 30" 이 아니다(`ASSB_TRANSFER_NOTE.md` §6-3-c 의 "30 번 보충 데이터 ZIP" 은 옛 큐 30 = 31호 ICI 의 자료이고 이 편과 무관하다). ⚠ **ASSB 논문이 아니고 측정도 없다** —
고체산화물 연료전지(SOFC) 복합 공기극 **LSCF(혼합 전도체 · MIEC) + YSZ(순수 이온 전도체)** 의 미시구조 → 유효 성질을 **좌표수(coordination number) 평균장 식 + 퍼콜레이션 확률 경험식**으로
계산한 **해석 모형 편**이다. 닻은 `questions/assb-contact-loss-vs-lampe.md`.

들어온 경로: 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1) "★ **Chen·He·Zhang·Wang·Ni 2013** — *Energies* 6, 1632−1656 | 지목 22 | 1 | Q1 | 22호가 기댄 'percolation theory'
(SOFC) — 01호 모델과의 관계".

지목 digest 가 이 편에 매단 명제(위키 전체를 `1632` · `Chen, He` · `percolation theory` · `SOFC` · `Bertei` · `Costamagna` · `coordination number` 로 grep — **이 편을 인용한 digest 는 22호
하나**다. 01호의 "percolation theory" 문장은 Lagadec [19] · Grimmett [21] · Hoshen–Kopelman [22] 에 기대고 SOFC 해석식 인용이 digest 에 없다. 53호의 `[인쇄]`(53호) "There is yet no
experimental study that incorporates percolation theory …" 는 인용 번호가 53호 digest 에 없어 이 편인지 정해지지 않는다. 22호 원문 PDF 는 이 세션에 없다 — 22호 digest 로 대조했다; 22호
refs 13–15("전부 SOFC")의 서지도 22호 digest 에 없어 이 편과 겹치는지 모른다):

| 지목 | 인용 번호 | 매단 명제 (digest 자리) |
|---|---|---|
| **22호** Strauss 2018 | ref 26 | ① §2-5(:198–205) `[인쇄]`(22호) 결론 "in the case of medium and large NCM622, **not all of the particles are electronically connected**, which is why they cannot be addressed electrochemically. This is in agreement with **percolation theory**" (ref 26, SOFC) ② 후속 표(:575) "★ 6 — Chen, He, Zhang, Wang, Ni, *Energies* 6, 1632−1656 (2013) (ref 26) \| 저자가 기댄 'percolation theory' — **SOFC** 원전. 1호 모델과의 관계 \| Q1" |
| **01호**(지목 밖 · 호출자 지정) | — | ① `p_c` 는 유한 시료에서 **폭**(무작위 충전 배열만 바꿔도 `θ_AM` 이 ≈30 % ↔ ≈70 % 이봉) ② §3.3 `[인쇄]`(01호) "the application of percolation theory … **may allow estimating** the effective … conductivity" — 조건법, 01호는 전도도를 계산하지 않았다 ③ 식 (8) `p_c(d) = 7.83 ln(d/µm) + 36.67` vol%(AM 구 · SE 3 µm 고정) |

**59–67호 · 29 · 38호 SI 보강을 이어받는다.** 22호는 무탄소 NCM622/β-Li₃PS₄(7 : 3 w/w) 복합양극에서 **NCM 2차 입자 크기만**(d₅₀ 4.0 / 8.3 / 15.6 µm) 바꿨고, 첫 C/10 충전 뒤 ex situ XRD
두 상 정련으로 불활성 분율 `f_inactive` 를 **2 / 27 / 31 %** 로 **측정**했다(66 · 67호가 그 `x` 교정 축을 다뤘다 — `f_inactive` 자체는 상 분율이라 교정에 안 걸린다). 개념
[[composite-cathode-percolation-utilization]] 은 01호 식 (8) 이 이 조성에서 불활성을 **3–15 배 과대 예측**한다는 `[재현]`(22호 절)과 56 · 57 · 63 · 65호의 `p_c` 반례를 모은다.

이 digest 의 일 (지시):

1. **(a) 모형의 정체** — 입자 충전 · 좌표수 · 퍼콜레이션 확률 식이 무엇이고 어디서 왔나(무작위 충전 · 구형 · 크기비 · 부피 분율 · 목 · 접촉각), 이 편이 새로 한 것 ↔ 인용한 것. **한 상만 키우고
   부피 분율을 고정하면 그 상의 연결 확률이 떨어지는지**를 식으로.
2. **(b) 22호 명제의 정량 대조** (`[재현]`) — 22호 조성 · 입도로 연결 안 된 NCM 분율을 예측해 `f_inactive` 와 비교, 없는 입력(SE 입도)은 폭으로.
3. **(c) SOFC ↔ ASSB 전이 조건** — 닮은 곳과 다른 곳(`[해석]`).
4. **(d) Q1 · 곱 축퇴** — 정적 `θ₀`(신품 연결 분율; 불활성 = 1 − θ₀) 예측식이 되는가 · 반응 속도와 면적이 곱으로만 들어가는가 · 무엇을 적합했고 무엇으로 검증했나.
5. **(e) 01호 모형과의 관계** — 같은 양을 다르게 계산하는가, 해석식 ↔ 시뮬레이션 차는 어디서 오나.
6. **(f)** Q5 · Q6 · Q7 · 채움표 68호 행 · 곱 축퇴 처방 쉰한 번째 적용 · 보류 (가)(나)(다)(아)(자)(차)(타) 표시(결정 안 함).

> ⚠ **형식 — *Energies* Article 25 쪽(MDPI · 그림 12 · 표 1 · 번호 식 (1)–(34) · 라벨 43 · 참고문헌 39). SI 없음. 1차 측정 0 · 셀 0 · 검증 자료 0** —
> 식 (2) · (20)–(23) 의 타당성은 선행 편([11, 15, 17])의 **컴퓨터 시뮬레이션 대조로 위임**된다(`[인쇄]`). 이 편 안의 결과는 전부 계산 곡선(그림 6–12, 곡선 넷씩)과 계산 예 하나다.
> **반복: 오차 · 산포 · 문턱 · 폭 · 적합의 낱말 0**(`error` · `uncertain` · `±` · `threshold` · `fit` · `measur` 0 회 — §어휘 집계).
> 그림 6–12 는 PNG 래스터(669 × 525 등)라 `[도표]` 값은 **PDF 안의 원본 래스터**에서 축 테 · 안쪽 눈금에 선형 적합한 뒤 색별 마커 무게중심(3 × 3 침식 뒤)으로 읽었다(§픽셀 판독). 식은
> 텍스트 층이 아래첨자를 흩어 놓아 **쪽 렌더(130–300 dpi)**로 읽었다. 그리고 **인쇄된 식으로 곡선 그림 일곱 장(6–12)을 전부 다시 계산했다**(§(a') — 세 군데에서 인쇄식과 그림이 다르다).
>
> 표기: `[인쇄]` 본문 · 캡션 · 식 명시 · `[도표]` 그림에서만 읽은 값(`figure-read ≈`) · `[재현]` 지면의 식 · 숫자로 우리가 계산 · 대조한 값 · `[해석]` 우리 해석.
> `[해석]` 표시 없는 문장은 원문이 실제로 말한 것.

# 판정 먼저

| 물음 | 판정 | 한 줄 근거 |
|---|---|---|
| **(a) 모형의 정체** | **좌표수 평균장(Suzuki–Oshima 계열 식 (2), `Z̄ = 6`) + 퍼콜레이션 확률 경험식 `P(Z)`([31] Bertei & Nicolella 2011) + 접촉 기하(목 반경 `r_c = min(r) sin θ`) — 무작위 충전 강체구 · 해석식 · 무한계** | `[인쇄]` 식 (2) `Z_k,ℓ = 0.5(1 + r_k²/r_ℓ²) Z̄ (ψ_ℓ/r_ℓ)/Σ(ψ_k/r_k)` · "Z̄ … widely assumed to be 6 for random close packing of rigid spherical particles [10,12,30]" · 식 (5)/(6)/(23) `P = 1 − ((4.236 − Z)/2.472)^3.7` · MIEC 배정 `P^i_LSCF = 1` · `P^e_LSCF = P_LSCF`(A 클러스터). 새로 한 것 = MIEC 배정 · 노출 LSCF 표면 자리 식 (9)/(26) · LSCF–YSZ 입자간 이온 전도도의 `min(r)` 수정 식 (18) · 무차원 곡선 |
| **(a) 한 상만 키우면** | ✅ **그 상의 연결 확률이 떨어진다 — 식에서 나온다(`[재현]`) · ⚠ 지면은 그 경우를 말하거나 그리지 않았다** | `[재현]` 식 (2)·(21)·(24): `Z_NN = 6ψρ/(ψρ + 1 − ψ)`, `ρ = r₃₂(SE)/r₃₂(CAM)`(수 분포의 ⟨r³⟩/⟨r²⟩ — 두 상 폭이 같으면 분포 폭은 약분된다). `ρ` ↓ ⇒ `Z_NN` ↓ ⇒ `P` ↓. `P = 0` 문턱 `ρ_c = 1.764(1−ψ)/(4.236ψ)` · `P = 1` 은 `ρ_1 = 4.236(1−ψ)/(1.764ψ)` · **`ρ_1/ρ_c = (4.236/1.764)² = 5.77`(ψ 무관)**. 지면의 크기비는 `r̄_YSZ/r̄_LSCF` = **1 · 2.5 두 점**(이온 전도체가 같거나 큰 쪽)뿐 — "larger YSZ" 가 LSCF 문턱을 0.29 → 0.14 로 내린다는 것까지 |
| **(a') 인쇄식 ↔ 그림** | ❌ **세 곳에서 다르다 — 곡선 그림 일곱 장(6–12)은 모두 인쇄식으로 재현되지만, 고쳐서야 된다** | `[재현]` ① 그림 6 · 8 은 인쇄식 `P` 가 아니라 **`√P`** 로 계산돼 있다(그림 8 적색 ψ 0.37–0.49: 판독 0.806 · 1.030 · 1.228 · 1.399 ↔ `√P` 0.806 · 1.031 · 1.227 · 1.399 ↔ 인쇄 `P` 0.586 · 0.865 · 1.116 · 1.333) ② 식 (24) 분자가 `Z_LSCFk,YSZℓ`(LSCF–YSZ)로 인쇄 — 그대로면 문턱이 거꾸로(ψ > 0.706 에서 `P = 0`) · 그림은 `LSCFℓ` 판 ③ 그림 7 은 식 (26) 의 `P^e P^i` **없이** 그렸다(ψ 0.29 에서 0.528 — 인쇄식은 0). 그리고 그림 9 · 10 의 이름표는 자기 곡선 값의 재현과 어긋난다(D4) |
| **22호 :198–205 명제** | ⚠ **방향만 선다 · 정량은 안 선다** | 방향: 위 (a) — CAM 이 SE 보다 커지면 CAM–CAM 좌표수가 줄어 연결 분율이 준다. 지면: 그 경우의 서술 · 그림 0. 정량: 아래 (b) |
| **(b) 22호 정량 대조** | ❌ **저자 배정 읽기로는 세 점을 동시에 못 맞춘다 — SE 입도를 어떻게 두어도, 어느 P 꼴로도 · 상한 읽기로는 M 의 불활성이 거의 전부 전자 밖이 된다** | `[재현]` ψ 0.479–0.498(7 : 3 w/w 고상 기준) · SE 입도 미인쇄(폭). 한 점씩은 맞는다 — S 는 d_SE ≈4.6–5.6 · M ≈4.9–6.5 · L ≈8.9–11.6 µm(`d_SE = ρ × d₅₀` — d₅₀ 를 Sauter 지름으로 본 환산 · 인쇄 `P` · `√P` · ψ 양끝). **S · M 을 같이 맞추면(d_SE ≈4.9–6.5) L 은 100 % 비연결**(측정 31 %) · **셋 최소제곱(d_SE ≈8.5–11.1) = S/M/L 0 / 2.6–3.6 / 34.8 %**(측정 2 / 27 / 31, RMSE 13.7–14.3 %p). 모형에서 1 − P 가 27 → 31 % 로 가는 데 크기비 ×1.04–1.05 면 되는데 22호 M → L 은 ×1.88(같은 로트) — **M ≈ L 의 평탄은 이 식의 함수족 밖**. 01호 SE(3 µm)를 넣으면 S 13–30 · M 100 · L 100 %. **상한 읽기**(`f_inactive ≥ 1 − θ^elec`)로는 모순 없는 영역이 d_SE ≥8.9–11.6 µm 이고 거기서 모형 전자 비연결은 S 0 · **M 2–3** · L ≤31 % — M 의 27 % 중 ≥89 % 가 전자 밖(22호 배정과 반대) |
| **(c) SOFC ↔ ASSB** | **구조는 닮고(전자+이온 혼합 전도체 + 이온 전도체) 물리는 다섯 곳에서 갈린다** | `[해석]` 소결 목(`θ` 29.5°) ↔ 압착 접촉 · `Z̄ = 6`(강체구 RCP, 공극 ≈36 %) ↔ 치밀 압착(공극 수 %–20 %, 소성 SE) · 600–800 °C ↔ 25 °C · 반응 자리 TPB(기체–LSCF–YSZ) ↔ 2상 CAM\|SE 계면(식의 Assumption 1 이 그 짝) · 부피 변화 0 ↔ NCM 2–8 %. 그리고 **SOFC 식에는 용량 칸이 없다** — 끊긴 LSCF 는 반응 자리만 잃지만 끊긴 NCM 은 용량을 잃는다. `P^i_LSCF = 1`(MIEC 가 이온 경로도 맡음)은 NCM 에 옮기면 안 되는 배정 |
| **(d) Q1** | **없다 — `θ(N)` 0/68 · 층 하나: 정적 `θ₀` 닫힌 식 후보** | 시간축 0 · 열화 0. `θ₀ = P^e(Z_NN(ψ, ρ))` 는 **신품 통째 연결 분율의 예측식**(불활성 = 1 − θ₀)이 된다 — 그러나 입력 `ρ`(SE 입도)가 ASSB 에서 잘 정의되지 않고(SE 는 연속 기질) 22호 세 점의 패턴을 못 맞춘다(저자 배정 읽기) |
| **(d) 곱 축퇴** | **반응 자리 밀도가 기하 인자의 곱이다 — 동역학 상수는 이 편에 없다** | `[인쇄]` 식 (7) `λ^V = γ · n^V · Z_LSCF,YSZ · P^e · P^i`. `[재현]` Assumption 1(2상 접촉 면적 `γ = π r_c²`, ASSB 쪽 짝)로 쓰면 `λ^V = (3ε_p/R) · [Z_NS sin²θ (min r/r_N)²/4] · P^e · P^i` — P2D 의 `a_s · A_eff` 자리에 **`A_eff ≙ (Z sin²θ/4)·P^e·P^i`**. 어떤 `j₀` 를 붙여도 `j₀ · sin²θ · Z · P^e` 한 곱. 적합한 것 0 · 검증 자료 0(선행 편 시뮬레이션 위임) |
| **(e) 01호와의 관계** | **같은 양(전자 퍼콜레이팅 클러스터 소속 분율)의 다른 계산 — 크기 효과의 기구도 다르다** | 01호 = 복셀(0.2 µm) 무작위 충전 + Hoshen–Kopelman · 유한 도메인 · 10 배열 폭 · 집전체 면 출발 / 68호 = 평균 좌표수 한 값의 결정론적 경험식 · 무한계 · 폭 0. `[재현]` SE 3 µm 에 대면 문턱(θ = 40 %)이 d 3 → 15 µm 에서 01호 45.3 → 57.9 vol%(전체 부피) ↔ 68호 34.7 → 72.7 %(고상, 인쇄 `P`) · 31.3 → 69.5 %(`√P`) — **크기 민감도 ×3**. `[해석]` 01호의 AM 배치는 SE 와 독립이라(01호 digest §4.2) 01호의 d 의존은 크기비가 아닌 이산화(복셀 접촉 거리 0.2 µm/d · 도메인/d) 쪽일 가능성 — 01호는 원인을 말하지 않는다 |
| **Q5 · Q6 · Q7** | **해당 없음 · 없다 · 해당 없음** | SOFC(Li 0 · 기준극 0) · `pressure` 0(접촉각 한 값 29.5° — 소결 목 전제, `sinter` 본문 0 회) · 무음극 아님 |
| **Q4** | **0/68 — 예순 번째 성질** | "퍼콜레이션 확률을 평균 좌표수 하나의 결정론적 경험식으로 두고 인쇄한 식과 다른 함수(√P)로 그림을 그렸으며, 입도비 두 점 · 폭 두 점의 무차원 곡선을 '일반해' 로 내놓으면서 문턱 · 산포 · 검증 자료를 한 번도 적지 않았다" |
| **곱 축퇴 처방 쉰한 번째** | **적용 불가 — 1단계 입력 없음 · 대신 해석식 안의 면적 곱을 적어 둔다** | §곱 축퇴 |
| **보류 (가)(나)(다)(아)(자)(차)(타)** | **근거 0 — 결정 안 함** | (차)에 정성 메모 하나(§보류) |

# 서지

| 항목 | 값 |
|---|---|
| 제목 | Percolation Theory in Solid Oxide Fuel Cell Composite Electrodes with a Mixed Electronic and Ionic Conductor |
| 저자 (5) | **Daifen Chen**\*, Huanhuan He, Donghui Zhang, Hanzhi Wang, Meng Ni — 교신 하나(\*, dfchen@mail.ustc.edu.cn) |
| 소속 | School of Energy and Power Engineering, **Jiangsu University of Science and Technology**(Zhenjiang — Chen · He · Zhang · Wang) · Building Energy Research Group, Department of Building and Real Estate, **The Hong Kong Polytechnic University**(Ni) |
| 서지 | *Energies* **2013**, 6, 1632–1656 · doi `10.3390/en6031632` · ISSN 1996-1073 · MDPI Article · 1 쪽 "OPEN ACCESS" · 25 쪽 `[인쇄]` "© 2013 by the authors; licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution license (http://creativecommons.org/licenses/by/3.0/)" — **CC BY 3.0** |
| 일정 | 접수 2012-12-06 · 수정본 2013-02-26 · 수락 2013-03-06 · 게재 2013-03-11 — `[재현]` 접수 → 게재 **95 일**, 수정본 → 수락 **8 일** |
| 자금 · COI | `[인쇄]` National Science Foundation of China (21106058 · 11204107) · China National Petroleum Corporation (OG 11080101) · Jiangsu University of Science and Technology (35011005) · Hong Kong Research Grant Council (PolyU5238/11E). 이해상충 진술 **없음**(`conflict` · `competing` 0 회) |
| 분량 | PDF 25 쪽(1,738,556 B · A4 595.2 × 842 pt) — 그림 **12**(1–5 모식 · 6–12 계산 곡선) · 표 **1** · 번호 식 (1)–(34) — 가지 식 8a–c · 12a–b · 18a–b(+ 18) · 28a–c · 33a–c 를 세면 **식 라벨 43** · 참고문헌 **39** · 명명법 표 1 쪽(2 쪽) |
| SI | **없음** — 보충자료 언급 0 |
| 원 래스터 | 그림 1 · 2 · 3 JPEG(1297 × 985 · 724 × 577 · 435 × 356) · 그림 4 · 5 PNG(751 × 483 · 708 × 173) · **그림 6–12 PNG**(669 × 525 · 608 × 478 · 672 × 535 · 614 × 475 · 607 × 497 · 729 × 568 · 609 × 482) — 벡터 0 |
| PDF 메타데이터 | title "Percolation Theory in Solid Oxide Fuel Cell Composite Electrodes with a Mixed Electronic and Ionic Conductor" · author "Daifen Chen, Huanhuan He, Donghui Zhang, Hanzhi Wang, Meng Ni" · subject = 초록 전문 · keywords "solid oxide fuel cell; percolation theory; mixed electron and ion conductor; LSCF; coordination number; three-phase-boundary sites; electrochemically active sites" · creator "**PScript5.dll Version 5.2.2**" · producer "**Acrobat Distiller 10.1.5 (Windows)**" · PDF 1.4 · 생성 **2013-03-11 18:27:53 +08:00** · 수정 **2013-03-11 18:30:55 +08:00**(3 분 뒤) · XMP 같은 값 · startxref/%%EOF 각 3(증분 갱신) · 암호 0 · **내려받기 표지 0**(쪽 발 · 메타데이터 어디에도 수령 기관 · 날짜 없음) ⇒ Windows 인쇄 드라이버(PScript5)로 PDF 를 만든 **출판 당일(게재일과 같은 날) 조판 파일 그대로**로 읽힌다(`[해석]` — 메타데이터가 말하는 만큼; 65–67호의 ACS 파일처럼 2026-09-28 표지가 찍힌 판이 아니다) |
| sha256 | `b67d3b8c188ff0913e047c734703a0266af9b57d078a68ed186635bc563fd7d4` — 호출자 명시값과 **일치** |

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| G1 | ★★★ **검증 자료 0** — `[인쇄]` "the validity of Equation (2) has been tested by comparing the calculated results with computer simulated results [11,15]" · "In our previous paper [17], the validity of Equations (20–23) were carefully checked by comparing the calculated results with computer simulation results that were obtained using the random packing reconstruction model [9]". 이 편 안의 실험 · 시뮬레이션 대조 · 오차 크기 0 | 모든 곡선이 **모형 대 모형**의 위임 검증 위에 있다. `[인쇄]` "sufficiently accurate in the prediction of electrode properties from the microstructure parameters" 의 근거가 지면에 없다 |
| G2 | ★★★ **퍼콜레이션 확률 식의 출처 · 꼴** — 식 (5) 는 [31] 에서 왔다고만 쓴다. 인쇄된 꼴 `1 − ((4.236 − Z)/2.472)^3.7` 이 [31] 의 식 그대로인지, 바깥 지수가 있는지 이 지면으로 확인되지 않는다 | §(a') — 그림 6 · 8 은 인쇄식이 아니라 `√P` 로 계산돼 있다. 어느 쪽이 [31] 인지는 [31] 을 열어야 정해진다(미열람) |
| G3 | ★★ **문턱 · 폭 · 유한 크기** — `threshold` 0 회. 무한계 식이라 전극 두께 · 집전체 면 · 배열 산포가 들어올 자리가 없다 | 01호(유한 도메인 · 10 배열 · 이봉)와 같은 양을 비교할 때 폭 0 의 결정론적 값이 된다 |
| G4 | ★★ **접촉각 `θ = 29.5°` 의 출처** — 계산 예 · 그림 7 에만 값이 나오고 인용 · 근거 0(소결 조건 서술 0) | 반응 자리 밀도가 `sin θ`(TPB) · `sin²θ`(면적)로 곱해진다 — 곱 축퇴의 한 인자 |
| G5 | ★★ **`a_YSZ,YSZ`(접촉 하나당 면적)의 식** — 식 (15)–(18) 에 쓰이나 정의식이 인쇄되지 않는다 | `[재현]` `a = π min(r)² sin²θ`(Assumption 1 의 `γ`)로 두면 그림 9–11 곡선 값이 전부 재현된다 — 그것이 저자의 정의인지는 지면에 없다 |
| G6 | ★★ **그림 12 의 공극률** — 캡션 · 본문에 값 0. 계산 예의 `φ_g = 40 %` 만 인쇄 | `[재현]` `φ_g = 0.40` 으로 (1, 0, 0) 선 0.267 = (2/3)·0.4 가 맞는다 |
| G7 | ★ **전자 전도도 식** — `[인쇄]` "the effective electronic conductivity that is based on the geometry would equal the effective electronic intra-particle conductivity of the LSCF particles network" 로 끝나고, 입자내 전도도 식은 "effective relative density … and … tortuosity [35]" 로 위임 | 22호가 잰 것(전자 전도도 10⁻³ → 10⁻⁶ S cm⁻¹)과 **같은 양의 식이 이 편에 없다** |
| G8 | ★ **Table 1 이산화의 근거** — ±(8√2/9)ϑ̃ 범위 · 9 등분을 [17] 로 위임 | `[재현]` 정규분포의 중앙 ≈79 % 만 덮는다(±1.257σ) · ϑ̃ < 0.795 여야 가장 작은 반경이 양수 |

# 그림 — 자동 13 + 수동 1 = 14 항목, 실제로 연 것 14 / 안 연 것 0

폴더 `raw/figures/chen2013_sofc-miec-composite-electrode-percolation-theory/`(`figures.json` 14 항목). **자동 크롭의 라벨 ↔ 내용 어긋남 0**(13 장 전부 열어 캡션과 대조했다). 대신
**과대 2**: (i) `tab_1.png` 는 bbox [44.7, 42.1, 554.0, 766.6] — **14 쪽 거의 전체**(식 (20)–(23) 본문 포함) (ii) `fig_12.png` 는 아래끝이 '5. Conclusions' 절 제목(y 329.4–342.7 pt)을 품는다
(그림 자체는 온전). 누락 0(초록 그래픽 없음 · SI 없음). ⇒ **수동 1**: `tab_1_manual_p14`(캡션 + 표 본체, 300 dpi 렌더 클립). 자동 파일은 지우지 않았고 `figures.json` `note` 에 적었다.
**연 것(14)**: fig_1 – fig_12 · tab_1 · tab_1_manual. 식은 쪽 렌더(2 · 6–22 쪽, 130 dpi; 식 (24) 는 300 dpi 클립)로 읽었다 — 1 · 3–5 · 23–25 쪽(초록 · 서론 · 참고문헌)은 텍스트 층으로. 수치 판독은 크롭 PNG 가 아니라 **PDF 안의 원본 래스터**에서 했다.
곡선 그림(6–12)은 모두 곡선 넷 — 범례 `(r̄_YSZ/r̄_LSCF, ϑ̃_LSCF, ϑ̃_YSZ)` = (1, 0, 0) · (1, 0.6, 0.6) · (2.5, 0, 0) · (2.5, 0.6, 0.6), 마커는 ψ_LSCF = 0.01 + 0.04k(`[도표]` 무게중심이
0.33 · 0.37 · 0.41 … 에 ±0.004 로 놓인다). **색 규약**은 그림 6 · 7 · 8 · 11 의 이름표에서 적색 (1, 0, 0) · 청색 (1, 0.6, 0.6) · 흑색 (2.5, 0, 0) · 자홍 (2.5, 0.6, 0.6) 이다.

## Fig. 1 — 평판형 SOFC 적층 모식 (봤다)
연결판 · 공기극 집전체 · 중간층 · 전해질 · 중간층 · 연료극 지지체 · 연결판 + 맨 아래 이름 없는 판. 공기 · 연료 흐름 화살표 · e⁻ 화살표. 본문 "seven distinct layers: (a) … (f)" 는 글자가 여섯(f 에 둘) — 사소(D13). 데이터 없음.

## Fig. 2 — 단전지 미시구조 · 물리 과정 모식 (봤다)
공기극: 청색 LSCF · 황색 YSZ 입자(비슷한 크기) · O²⁻ 경로(자홍 화살표)가 LSCF · YSZ 둘 다를 지난다 · 연료극: 회색 Ni · 황색 YSZ(더 큰 입자). 캡션과 맞다. 데이터 없음.

## Fig. 3 — 두 성분 무작위 충전 · A/B/C 클러스터 모식 (봤다)
황색 YSZ 사슬이 전해질 ↔ 연결판을 잇는 A 둘 · 전해질에만 붙은 B · 고립 C. `[인쇄]` Costamagna [12] 명명. ⚠ `[해석]` 모식의 입자는 **격자처럼 줄 선 같은 크기 구**다 — 식의 가정(무작위 충전 강체구)을
그린 것이지 실제 소결 전극이 아니다.

## Fig. 4 — 반응 자리 가정 넷 (봤다)
(a) 두 입자 교차면(원판 `π r_c²`, 적색 빗금) (b) 교차 원주(`2π r_c`) (c) 교차선에서 폭 `w` 안의 두 구면 띠 (d) 이웃과 겹친 모자를 뺀 노출 LSCF 표면. `r_c` · `θ` 표시. ⚠ (a) 의 `θ` 는 **YSZ
중심**에 그려져 있다(YSZ 가 약간 크다) — 본문 `r_c = min(r_LSCF, r_YSZ) sin θ` 는 작은 입자 쪽 각이다(사소, 기록만).

## Fig. 5 — LSCF–YSZ 입자간 이온 전도도의 두 계산법 (봤다)
(a, b) 작은 입자층 기준 (c) 큰 YSZ 입자층 기준(작은 LSCF 여럿이 한 층 안). 적색 파선 = 층 경계. 식 (18) "smaller particle layer" 선택의 모식. 데이터 없음.

## Fig. 6 — 퍼콜레이팅 TPB 길이 `λ̃^V`(Assumption 2) vs ψ_LSCF (봤다 · ★ 재현)
`[도표]` (1, 0, 0) 은 ψ ≈0.295 에서 **수직에 가깝게** 솟아 ψ 0.53–0.57 에서 ≈2.20 최대 · (1, 0.6, 0.6) 같은 문턱 · 최대 ≈1.28 · (2.5, 0, 0) 은 ψ ≈0.14 에서 솟아 최대 ≈0.78(ψ ≈0.39–0.41) ·
(2.5, 0.6, 0.6) 최대 ≈0.52. `[인쇄]` "maximum … when ψ_LSCF = 0.55" · "from 0.55 to 0.39" · "42% lower" · "decreases 34%". `[재현]` 식 (2)·(4)·(8b)·(21)·(23)–(25)·(30):
monodisperse 크기비 1 에서 `λ̃ = 9ψ(1−ψ)·P` — **인쇄 `P` 로는 최대 2.169 @ ψ 0.56–0.57, 문턱 바로 위가 완만**(ψ 0.33 에서 0.571) · **`√P` 로는 2.197 @ 0.55 · 수직 출발**(0.33 에서 1.066).
판독(적색 마커): 0.37 1.561(표지선 겹침) · 0.41 **1.838** · 0.45 **2.029** · 0.49 **2.146** · 0.53 **2.198** · 0.57 **2.195** — `√P` 1.829 · 2.027 · 2.144 · 2.193 · 2.188 ↔ 인쇄 `P` 1.537 · 1.845 ·
2.043 · 2.146 · 2.169. 흑 · 자홍(크기비 2.5)도 같다(자홍 0.17 · 0.21 · 0.25: 판독 0.247 · 0.368 · 0.440 ↔ `√P` 0.229 · 0.356 · 0.433 ↔ 인쇄 0.135 · 0.290 · 0.397). 42 % · 34 % 는 두 꼴 모두 재현
(1 − 1.261/2.169 = 0.419 · 1 − 0.518/0.781 = 0.337 — 비가 기하 인자에서 온다). ⇒ **그림은 `√P` 로 그려졌다**(D1).

## Fig. 7 — 노출 LSCF 표면 반응 자리 `S̃^V_es,per`, θ = 29.5° (봤다 · ★ 재현)
`[도표]` 네 곡선 모두 **원점에서 시작하는 거의 직선** — ψ 0.97 에서 (1, 0, 0) 1.775 · (1, 0.6, 0.6) 1.536 · 흑은 적보다 조금 위(ψ 0.49 에서 +8 %) · 자홍은 청과 거의 겹친다. **문턱이 없다.** `[재현]` 식 (26) 을 **`P^e P^i` 없이** 계산하면 판독과
≤0.005 로 맞는다(적색 0.29 **0.528** ↔ 0.532 · 0.49 **0.894** ↔ 0.898 · 0.97 **1.775** ↔ 1.778 · 흑색 0.09 **0.199** ↔ 0.200 · 청색 0.05 **0.075** ↔ 0.079). 인쇄식대로 `P^e` 를 곱하면 적색은
ψ < 0.294 에서 0, 0.49 에서 0.815 다 ⇒ **"percolated LSCF surface" 라는 캡션 · 명명법과 달리 퍼콜레이션을 적용하지 않은 그림**(D3). `[인쇄]` "appears to be insensitive to the particle size
ratio" — `[재현]` ψ 0.49 에서 1 → 2.5 가 +7.9 %(0.898 → 0.969) · "slightly decreases" — 폭 0.6 이 −13 %.

## Fig. 8 — 전해질 면 퍼콜레이팅 TPB 길이 `λ̃^S` (봤다 · ★ 재현)
`[도표]` (1, ·, ·) 둘은 ψ ≈0.295, (2.5, ·, ·) 둘은 ≈0.14 에서 출발 · ψ 1 에서 (1, 0, 0) ≈2.97 · 폭 0.6 ≈2.27. `[재현]` 식 (11)·(12b)·(27)·(32): `λ̃^S = 3ψ(r̄/r₃₂)·P` —
**판독이 `√P` 와 ±0.005 로 맞는다**: 적색 0.37 **0.806** ↔ `√P` 0.806 ↔ 인쇄 0.586 · 0.41 **1.030** ↔ 1.031 ↔ 0.865 · 0.45 **1.228** ↔ 1.227 ↔ 1.116 · 0.49 **1.399** ↔ 1.399 ↔ 1.333 ·
흑색 0.21 **0.515** ↔ 0.509 ↔ 0.413 · 0.25 **0.688** ↔ 0.688 ↔ 0.630 · 청색 0.41 **0.788** ↔ 0.787 ↔ 0.660. ⚠ 캡션은 "`λ̃^V_TPB,per`"(y 축은 `λ̃^S`) · 본문은 "TPB **area** per unit electrolyte
surface area"(Assumption 2 이면 길이/면적) — D8.

## Fig. 9 — YSZ–YSZ 입자간 이온 전도도 `σ̃^i,ter,eff_YSZ-YSZ` (봤다 · ★ 재현 · 이름표 어긋남)
`[도표]` ψ 0.01: 흑 21.8 · 자홍 19.1 · 적 8.8 · 청 7.75 · ψ 1 로 0. 이름표(표지선): **흑 = (2.5, 0.6, 0.6) · 자홍 = (2.5, 0, 0) · 적 = (1, 0.6, 0.6) · 청 = (1, 0, 0)**. `[재현]` 식 (28a)·(33a)
(`a = π min(r)² sin²θ` — G5)로 곡선 값을 계산하면 **흑 = (2.5, 0, 0) 21.63 · 자홍 = (2.5, 0.6, 0.6) 19.05 · 적 = (1, 0, 0) 8.81 · 청 = (1, 0.6, 0.6) 7.73**(ψ 0.25: 9.21 · 8.12 · 5.07 · 4.44 ↔
판독 9.21 · 8.09 · 5.05 · 4.44) — **색 규약(그림 6 · 7 · 8 · 11)과 같은 배정이 값을 재현하고, 인쇄된 이름표는 폭(ϑ̃)을 뒤바꿨다.** `[인쇄]` "A larger σ̃_YSZ-YSZ can be obtained by using broader
particle size distribution materials" 는 이 이름표를 따른 문장 — 재현으로는 폭 0.6 이 **−12 %**(8.82 → 7.75) (D4).

## Fig. 10 — LSCF–LSCF 입자간 이온 전도도 (봤다 · ★ 재현 · 이름표 어긋남)
`[도표]` ψ 0.97: 흑 ≈8.65(눈 — 적과 겹쳐 마커 분리 불가) · 적 8.46 · 자홍 7.59 · 청 7.42. 이름표: **흑 = (1, 0.6, 0.6) · 적 = (2.5, 0.6, 0.6) · 자홍 = (1, 0, 0) · 청 = (2.5, 0, 0)**. `[재현]` 식 (28b)·(33b): 적 = (1, 0, 0)
8.48 · 청 = (1, 0.6, 0.6) 7.43 · 자홍 = (2.5, 0.6, 0.6) 7.58 · 흑 = (2.5, 0, 0)(0.89 에서 7.63 ↔ 판독 7.62) — 여기서도 **색 규약 배정이 값을 재현**하고 이름표는 다르게 섞였다(D4). 본문 "weak effects
from r̄_YSZ/r̄_LSCF, ϑ̃_LSCF and ϑ̃_YSZ" 는 어느 배정이든 선다.

## Fig. 11 — LSCF–YSZ 입자간 이온 전도도 (봤다 · ★ 재현)
`[도표]` (1, 0, 0) 최대 ≈4.50 @ ψ 0.5 · (1, 0.6, 0.6) ≈3.94 · (2.5, 0.6, 0.6) ≈2.33 @ ≈0.4 · (2.5, 0, 0) ≈1.56 @ ≈0.4. x 축이 **1.1 까지**(다른 그림은 1.0) · y 라벨 아래첨자가 "LSCF-YS" 로
잘려 있다(원 래스터 그대로). `[재현]` 식 (18)·(28c)·(33c): 크기비 1 monodisperse `σ̃ = 18ψ(1−ψ)` → 4.50 ✓ · 네 곡선 모두 이름표 = 색 규약으로 ±0.03 재현. ⚠ `[인쇄]` "for the specific volume
fraction ψ_LSCF = 0.5, σ̃_LSCF-YSZ decreases with increasing r̄_YSZ/r̄_LSCF, ϑ̃_LSCF and ϑ̃_YSZ" ↔ 같은 그림의 크기비 2.5 쌍은 폭 0.6 이 **더 높다**(`[재현]` ψ 0.49 에서 2.242 ↔ 1.504) — D5.

## Fig. 12 — 수력 반경 `r̃_g` (봤다 · 재현)
`[도표]` (1, 0, 0) 수평선 ≈0.27 · (1, 0.6, 0.6) 수평선 ≈0.35 · (2.5, 0, 0) 0.66 → 0.27 · (2.5, 0.6, 0.6) 0.87 → 0.35. `[재현]` 식 (29)·(34), `φ_g = 0.40`(G6): (2/3)·0.4 = 0.267 ·
×r₃₂/r̄(ϑ̃ 0.6 → 1.309) = 0.349 · 크기비 2.5 의 ψ → 0 끝 0.667 · 0.873 ✓. 본문과 맞다.

## Table 1 — 9 분할 반경 · 확률 (`tab_1.png` 과대 · `tab_1_manual_p14.png` 봤다)
`[인쇄]` `r_k/r̄ = 1 + (2√2 j/9)ϑ̃`(j = −4 … 4) · `p` = 6.77 · 9.53 · 12.2 · 14.1 · 14.8 · 14.1 · 12.2 · 9.53 · 6.77 % — `[재현]` 정규 밀도를 z = 0.314 j 에서 정규화하면 6.74 · 9.52 · 12.19 ·
14.13 · 14.85 %(≤0.03 %p 차) · 덮는 범위 ±1.257σ(정규 질량의 ≈79 %) · `p` 는 **수(개수) 확률**이다(식 (21) 이 `p r³` 로 부피 분율을 만든다).

## 본문 서술과 어긋난 그림 (요약)

- **그림 6 · 8** — 인쇄식 (23) 의 `P` 가 아니라 `√P` 로 계산됐다(수직 출발 · ψ 0.55 최대) (D1).
- **그림 7** — 식 (26) 의 `P^e P^i` 없이 그렸다 · 캡션 · 명명법의 "percolated" 와 어긋난다 (D3).
- **그림 9 · 10** — 이름표가 자기 곡선 값의 재현 · 다른 그림의 색 규약과 어긋난다 · 그림 9 본문 문장이 그 이름표를 따른다 (D4).
- **그림 11** — 본문 "decreases with … ϑ̃" 가 크기비 2.5 쌍에서 반대 (D5).
- **그림 8** — 캡션 기호 `λ̃^V` ↔ 축 `λ̃^S` · 본문 "area" (D8).
- 그림 1 · 2 · 3 · 4 · 5 · 12 · 표 1 — 본문과 맞다(그림 1 층 글자 수 · 그림 4 (a) 각 표시 위치는 사소).

# 픽셀 판독 (`[도표]` 전부 — 원본 래스터 · 축 테 · 안쪽 눈금 적합 · 색별 마커 무게중심)

| 그림 | 원 래스터 | 축 테(px) | 눈금 → 값 | 판독 방법 |
|---|---|---|---|---|
| 6 | 669 × 525 | x 93 → 651 · y 440 → 5 | x 0 → 1.0(주눈금 55.8 px/0.1) · y 0 → 2.5(`[재현]` 적합 y = −174.14 v + 440.56, 부눈금 0.15) | 적 R > 190 · G, B < 110 / 청 · 자홍 · 흑 마스크 → 3 × 3 침식 → 무게중심(≥6 px) |
| 7 | 608 × 478 | x 83 → 591 · y 401 → 4 | x 0 → 1.0 · y 0 → 1.9(부눈금 0.1 = 20.9 px) | 같음 |
| 8 | 672 × 535 | x 93.5 → 653 · y 451.5 → 14.5 | x 0 → 1.0 · y 0 → 3.2(0.2 = 27.3 px) | 같음 |
| 9 | 614 × 475 | x 102 → 598 · y 400.5 → 12.5 | x 0 → 1.0 · y 0 → 22.56(2.5 = 43 px) | 같음 |
| 10 | 607 × 497 | x 74 → 590 · y 418 → 14 | x 0 → 1.0 · y 0 → 10.0(1.0 = 40.4 px) | 같음 |
| 11 | 729 × 568 | x 105 → 711 · y 478 → 4.5 | x 0 → **1.1** · y 0 → 5.2(0.25 = 22.8 px) | 같음 |
| 12 | 609 × 482 | — | 눈으로(수평선 둘 · 양끝 넷) | — |

- x 교정 검사: 마커 무게중심이 ψ = 0.01 + 0.04k 에 ±0.004 로 놓인다(그림 6 적 0.3306 · 0.4106 · 0.4504 · 0.4900 · 0.5305 …).
- 판독 오차: 마커 무게중심 y ≈±0.5 px(그림 6 에서 ±0.003). **문턱 바로 위 첫 마커는 가파른 선분이 무게중심을 끌어올린다**(그림 6 · 8 의 ψ 0.33 판독이 `√P` 보다 0.03–0.07 높다) —
  그래서 `√P` 판정은 ψ ≥0.37 점(그림 8 은 0.806/0.806 · 1.030/1.031 · 1.228/1.227 · 1.399/1.399)에 기댄다. 표지선이 지나는 마커(그림 6 적 0.37 · 흑 0.15 · 0.31 · 0.35)는 뺐다.
- 바깥 지수 β(`P^β`) 를 판독에서 역산하면 그림 8 적 ψ 0.37–0.49 에서 **0.49–0.50**, 그림 6 적 0.41–0.49 에서 0.48–0.49 — 0.4 를 넣으면 같은 점에서 +0.014…+0.05 높다(`[재현]`).

# 절별 해체

## 초록 · 명명법 (pp. 1632–1634)

- `[인쇄]` "Percolation theory is generalized to predict the effective properties of specific solid oxide fuel cell composite electrodes, which consist of a pure ion conducting material (e.g., YSZ or GDC)
  and a mixed electron and ion conducting material (e.g., LSCF, LSCM or CeO2)." 계산 대상: MIEC 입자의 전자 · 이온 경로 소속 확률 · 퍼콜레이팅 TPB 자리(가정 여럿) · 노출 LSCF 표면 자리 ·
  입자간 이온 전도도 수정식 — 변수: LSCF 부피 분율 · 두 상의 평균 반경 · 무차원 표준편차 · 공극률.
- `[인쇄]` "Finally, all of the calculated results are presented in non-dimensional forms to provide generality for practical application. Based on these results, the relevant properties can be easily
  evaluated". `[해석]` "일반해" 의 범위는 크기비 **1 · 2.5** · 폭 **0 · 0.6** 네 조합이다.
- 명명법(2 쪽 — 한 쪽 전체): `P_mat`(A 클러스터 소속 확률) · `P^i_mat` · `P^e_mat` · `ψ_k`(**고상 부피 분율**) · `φ_g`(공극률) · `θ`(접촉각) · `r_c`(목 반경) · `δ`(입자간 계면 두께) 등.

## 1. 서론 (pp. 1634–1635)

- SOFC 복합 전극의 요건 여섯 — 열팽창 · 기계 강도 · **퍼콜레이팅 기공 · 전자 · 이온 경로** · 반응 자리. `[인쇄]` "The term 'percolated' is defined as the contiguous connection through the whole
  electrode structure".
- 연구 흐름 셋 `[인쇄]`: 실험(입체학 · FIB-SEM [5, 6, 13, 14]) · 무작위 충전 재구성 [7–9] · 퍼콜레이션 이론 [10–12] — "the percolation micro-models use the percolation theory and coordination
  number theory to represent the microstructure of a composite electrode developed by the random packing reconstruction methods [11]". 좌표수 경험식 Bouvard [16] · Suzuki [15] → Costamagna [12]
  → 자기 선행 [11](접촉 수 보존) · [17](다분산) · Bertei [18](기공 형성제).
- `[인쇄]` "To the best of our knowledge, most of the previous theory models … were developed for a composite electrode that consists of a pure electron conducting material (e.g., Ni or LSM) and a pure
  ionic conducting material (e.g., YSZ)." ⇒ 이 편의 새 자리 = **MIEC + 순수 이온 전도체**.
- ⚠ `[인쇄]` "A composite cathode with a mixed electron and ion conducting conductor … has been found to exhibit great performance [23–28]" — [28] 은 CdSe 나노결정 표면 플라즈몬 발광 논문이고 [26] 은 [4] 와
  같은 서지다(D10 · D11).

## 2. 단전지 모식 (pp. 1635–1636) · 그림 2

공기극 반응 자리 = (기체–LSCF–YSZ) TPB **또는 공기에 드러난 LSCF 표면**(MIEC 이라서). `[인쇄]` "Both the YSZ and LSCF particles contribute to the ion conducting path within the cathode."

## 3. 퍼콜레이션 이론 (pp. 1636–1647)

- `[인쇄]` "Percolation theory can be considered as an extension application of the random packing reconstruction method and is **sufficiently accurate** in the prediction of electrode properties from
  the microstructure parameters." 두 부분: 좌표수 이론 + 미시 모형.

### 3.1 좌표수 (p. 1637)

```
Z_k       = Σ_ℓ Z_k,ℓ                                                      (1)
Z_k,ℓ     = 0.5 (1 + r_k²/r_ℓ²) · Z̄ · (ψ_ℓ/r_ℓ) / Σ_m (ψ_m/r_m)           (2)   Z̄ = 6
n^V_k Z_k,ℓ = n^V_ℓ Z_ℓ,k                                                  (3)   접촉 수 보존
n^V_k     = (1 − φ_g) ψ_k / (4π r_k³/3)                                    (4)
```

`[인쇄]` "Z̄ is the average coordination number of all of the particles, which is widely assumed to be 6 for random close packing of rigid spherical particles [10,12,30]" · "Equation (2) is considered a
more reasonable expression … than the previous equation [15]" · "the validity of Equation (2) has been tested by comparing the calculated results with computer simulated results [11,15]".
`[재현]` 식 (2)·(4) 는 (3) 을 만족한다(`n_k Z_k,ℓ ∝ ψ_kψ_ℓ(r_k² + r_ℓ²)/(r_k³ r_ℓ³)` 대칭). ⚠ `[해석]` `Z̄ = 6` 은 **공극률 · 크기 분포와 무관한 상수**다 — 공극 ≈36 % 의 강체구 RCP 값을 모든
`φ_g` 에 쓴다.

### 3.2.1 두 성분 — 클러스터 · 확률 (pp. 1638–1639) · 그림 3

- A(전해질 ↔ 집전체를 잇는) · B(전해질에만) · C(고립) — Costamagna [12] 명명. `[인쇄]` "Generally, the probability of a YSZ particle belonging to an A cluster can be evaluated using [31]:"

```
P_YSZ = 1 − ((4.236 − Z_YSZ,YSZ) / 2.472)^3.7                              (5)
P^i_YSZ = 1 ,  P^i_LSCF = 1 ,  P^e_LSCF = 1 − ((4.236 − Z_LSCF,LSCF)/2.472)^3.7    (6)
```

- `[인쇄]` "Obviously, P^i_LSCF is different from the percolated probability of the particle belonging to the A cluster, P_LSCF. However, P^e_LSCF = P_LSCF because the LSCF particles are the only
  material that contributes to the electron conducting path." — **이것이 이 편의 핵심 새 배정**: MIEC 는 이온 경로에 무조건(1), 전자 경로에는 A 클러스터 확률로.
- `[재현]` 식 (5) 의 `P = 0` 은 `Z = 4.236 − 2.472 = 1.764`, `P = 1` 은 `Z = 4.236`. 그 밖의 값(밑 > 1 · < 0)의 처리는 인쇄되지 않는다(그림은 [0, 1] 로 자른 모양). 낱말 "threshold" 는 0 회.

### 3.2.2 부피당 반응 자리 (pp. 1639–1641) · 그림 4

```
λ^V_TPB,per = γ_LSCF,YSZ · n^V_LSCF · Z_LSCF,YSZ · P^e_LSCF · P^i_YSZ      (7)
γ = π r_c²      (8a, Assumption 1 — 2상 교차 면적, m⁻¹)   r_c = min(r_LSCF, r_YSZ) sin θ
γ = 2π r_c      (8b, Assumption 2 — TPB 원주, m⁻²)       ← 이 편 그림은 전부 이것
γ = 2π r_LSCF²[cos θ_LSCF − cos(w/r_LSCF + θ_LSCF)] + 2π r_YSZ²[…]   (8c, Assumption 3 — 폭 w 띠)
S^V_es,per = 2π r_LSCF² n^V_LSCF [2 − (1−cos θ_LSCF) Z_LSCF,LSCF − (1−cos θ_LSCF) Z_LSCF,YSZ] P^e_LSCF P^i_LSCF   (9, Assumption 4)
```

`[인쇄]` "It is generally accepted that the global reaction rate will be governed by many multiple elementary chemical steps … There is some controversy regarding the actual pathway and nature of the
electrochemical reaction sites [12]." · 활성 영역: "the electrochemical reaction sites are only potentially electrochemically active. The percentage of these sites that are electrochemically active
depends on the ability of the ions to be transported … the thickness of the composite electrode and the particular working conditions" [32]. ⇒ 이 편은 **자리의 수**까지이고 반응 속도 · 활성 비율은
다루지 않는다.

### 3.2.3 전해질 면 자리 (pp. 1641–1642)

`λ^S = γ_LSCF,ele · n^S_LSCF · P^e_LSCF`(10) · `n^S = (1−φ_g)ψ_LSCF/(2π r²/3)`(11) · `γ_ele = π r² sin²θ`(12a) · `2π r sin θ`(12b).

### 3.2.4–3.2.5 유효 전도도 (pp. 1642–1644) · 그림 5

- 층 직렬 · 층 안 병렬: `σ^i,eff = [1/(σ^tra_YSZ + σ^tra_LSCF) + 1/(σ^ter_YSZ-YSZ + σ^ter_LSCF-LSCF + σ^ter_LSCF-YSZ)]⁻¹`(13) — 입자내(tra)는 "effective relative density of the percolated
  material and … the tortuosity of the conducting path [35]" 로 위임(식 0).
- 입자간: `R^ter = L/(S σ^ter,eff) = L^ter/(S^ter σ^ter,0)`(14) · `S^ter = a (2rS) n^V (Z/2) P^i`(15) · `σ^ter,eff = σ^ter,0 · 2a r² n^V Z P^i / δ`(16, 17) · LSCF–YSZ 는 두 가지(18a · 18b)가 보존
  원리를 어긴다며 **작은 입자층 기준** `4a min(r)² n^V Z P^i P^i / δ`(18). `[인쇄]` σ^ter,0_YSZ-YSZ = 0.05 S m⁻¹ @ 800 °C [10] · δ ≈5 nm [37].
- ⚠ `[인쇄]` `L^ter` = "the product of the number of particle layers **L/r_YSZ** and the thickness … δ" ↔ `[재현]` 식 (16) 의 앞계수 2 는 층 수 **L/(2r)** 일 때 나온다(D7).
- `[인쇄]` 전자 전도: "the electronic inter-particle conductivity is essentially negligible compared with the intra-particle conductivity … the effective electronic conductivity … would equal the effective
  electronic intra-particle conductivity of the LSCF particles network." — **전자 전도도의 식은 없다**(G7).

### 3.2.6 수력 반경 (p. 1644)

`r_g = (2/3)(φ_g/(1−φ_g))(ψ_LSCF/r_LSCF + ψ_YSZ/r_YSZ)⁻¹`(19) — dusty-gas 모형용 [38].

### 3.3 다분산 (pp. 1644–1647) · 표 1

- 정규분포(20) 를 9 등분(표 1) · `r_k = r̄(r_k/r̄)` · `ψ⁰_k = p_k r_k³/Σ p r³`(21) · `ψ_k = ψ⁰_k ψ_mat`(22) · 확률은 두 성분과 같음(23).
- `[인쇄]` "P^e_LSCFk can be described by a function of the average coordination number of all of the LSCF particles [11,39]" — 식 (24) 가 그 평균인데 **분자에 `Z_LSCFk,YSZℓ` 가 인쇄됐다**(D2 — 300 dpi
  렌더로 확인).
- 식 (25)–(29): (7)·(9)·(10)·(16)–(19) 의 9 × 9 합. `[인쇄]` "In our previous paper [17], the validity of Equations (20–23) were carefully checked by comparing the calculated results with computer
  simulation results that were obtained using the random packing reconstruction model [9]."
- `[재현]` **(24)(분자를 `LSCFℓ` 로)·(2)·(21) 을 합치면 `Z_LSCF,LSCF = 6 A_L/(A_L + A_Y)`, `A = ψ/r₃₂`, `r₃₂ = Σp r³/Σp r²`** — 두 상 ϑ̃ 가 같으면 폭은 약분되고 **크기는 Sauter 반경 비로만
  들어간다**(n 가중 평균 ⟨r²⟩ = A/B 항등식). ϑ̃ 0.6 의 `r₃₂/r̄` = **1.309** · 0.3 = 1.087.

## 4. 결과 (pp. 1647–1653) · 그림 6–12

- 식 (1)–(19) = monodisperse · (20)–(29) = 다분산. 모든 그림은 **Assumption 2**(TPB 길이). 무차원화: `λ̃^V = λ^V/((1−φ_g) sin θ/r̄²_LSCF)`(30) · `S̃ = S/((1−φ_g)/r̄_LSCF)`(31) ·
  `λ̃^S = λ^S/((1−φ_g) sin θ/r̄_LSCF)`(32) · `σ̃ = σ/(σ⁰ r̄_LSCF sin²θ (1−φ_g)/δ)`(33a–c) · `r̃_g = r_g/(r̄_LSCF/(1−φ_g))`(34).
- `[인쇄]` 그림 6: "The volume fraction loading ψ_LSCF should be chosen to fall within the range of 0.3 to 1 during the composite electrode fabrication process. Under this constraint, both percolated
  electron and ion conducting paths can be formed throughout the whole cathode structure. Because both the YSZ and LSCF particles are ionic conductors, the percolated ion conducting path can be formed at
  any volume fraction loading." — ⚠ 0.3 은 크기비 1 의 문턱이다(크기비 2.5 는 0.14, D12).
- `[인쇄]` 계산 예: "ψ_LSCF = 0.42, the mean particle radii of the LSCF and YSZ materials are **r̄_YSZ = 200 nm and r̄_YSZ = 40 nm** and ϑ̃_YSZ = ϑ̃_LSCF = 0.6 … approximately **9.3 × 10¹³ m⁻²** when the
  contact angle θ = 29.5° and the porosity φ_g = 40%." — `[재현]` 9.3 × 10¹³ 은 **(2.5, 0.6, 0.6) · r̄_LSCF = 40 nm**(곧 r̄_YSZ = 100 nm)로 나온다(9.56 × 10¹³, +2.8 %) · 크기비 5(200/40)면
  5.1 × 10¹³ — "200 nm" 는 지름이거나 오기(D6).
- 그림 7–12 의 본문 명제와 그 재현은 §그림.

## 5. 결론 (p. 1653)

`[인쇄]` "Percolation theory is extended to predict the effects of the microstructure parameters, such as the volume fraction of an LSCF material, particle size distributions … and **the porosity**, on the
effective properties" — ⚠ `[재현]` 공극률은 `(1−φ_g)` 앞계수(무차원화로 약분)와 수력 반경에만 들어간다; 좌표수 · 확률은 `φ_g` 무관(`Z̄ = 6` 고정) — D16.

## 참고문헌 39 편 — 우리 축에 닿는 것

[31] Bertei & Nicolella 2011 *Powder Technol.* 213, 100(식 (5) 원전) · [39] Bertei, Choi, Pharoah, Nicolella 2012 *Powder Technol.* 231, 44(소결 무작위 충전의 퍼콜레이션 — 식 (24)) · [11] Chen,
Lin, Zhu, Kee 2009 *JPS* 191, 240(식 (1)–(4) · (19) · A/B/C 적용) · [17] Chen, Lu, Li, Yu, Kong, Zhu 2011 *JPS* 196, 3178(다분산 · 표 1 · 식 (20)–(23) 검증) · [15] · [30] Suzuki & Oshima 1983 ·
1985 *Powder Technol.*(좌표수 · `Z̄`) · [16] Bouvard & Lange 1991 *Acta Metall. Mater.* 39, 3083(이성분 분말의 퍼콜레이션 ↔ 좌표수) · [12] Costamagna, Costa, Antonucci 1998 *Electrochim. Acta* 43,
375 · [9] Kenney … Karan 2009 *JPS* 189, 1051(무작위 충전 재구성 — 검증 대상 모형) · [18] Bertei & Nicolella 2011 *JPS* 196, 9429(공극률 · 입도 분포). 전부 **SOFC · 분말 충전** — 전지 0.

# 어휘 집계 — NFKC · 줄 끝 하이픈 복원(8 곳) · 대소문자 무시 (본문 · 캡션 · 명명법 | 참고문헌)

⚠ 텍스트 층이 식의 아래첨자를 낱말로 흩어 놓아 `LSCF`(본문 465) · `YSZ`(375) 같은 기호 수는 식 조각을 포함한다 — 아래는 산문 낱말 위주다.

| 지문 열 | 본문 | 참고문헌 | 메모 |
|---|---:|---:|---|
| `percolated` · `percolation theory` · `coordination number` · `cluster` | 66 · 13 · 22 · 14 | 0 · 2 · 0 · 0 | |
| `threshold` | **0** | 0 | 그림 6 · 8 의 수직 출발(ψ 0.294 · 0.143)을 이름 붙이지 않는다 |
| `experiment` · `simulat` · `valid` · `compar` | 3 · 2 · 3 · 6 | 1 · 0 · 0 · 1 | `experiment` 셋은 전부 서론(남의 연구 · "expensive and time consuming") · `valid` 둘 = 선행 편 시뮬레이션 대조 위임 |
| `measur` · `fit` · `error` · `uncertain` · `±` · `identifiab` | **0** | 1 · 0 · 0 · 0 · 0 · 0 | 산포 · 적합 어휘 0 |
| `assum` · `reasonable` · `should` · `generally` · `obviously` · `widely` | 26 · 7 · 8 · 11 · 4 · 3 | 0 | "sufficiently accurate" 1 · "carefully checked" 1 |
| `contact angle` · `29.5` · `neck` · `sinter` | 6 · 3 · 2 · **0** | 0 · 0 · 0 · 1 | 소결은 [39] 제목에만 |
| `porosity` · `thickness` · `finite` · `current collector` | 8 · 9 · 2 · 3 | 1 · 0 · 1 · 0 | `finite` 둘 = Assumption 3 의 "finite distance" |
| `temperature` · `800` · `time` | 2 · 1 · 1 | 0 | `time` 1 = "time consuming" — **시간축 0** |
| `exchange current` · `Butler` · `overpotential` · `current density` · `kinetic` | **0** | 0 · 0 · 0 · 0 · 1 | 반응 속도식 0 |
| `battery` · `lithium` · `degradation` · `aging` · `cycl` · `pressure` | **0** | 0 | 전지 · 열화 · 압력 어휘 0 |
| `conflict` · `competing` | **0** | 0 | 이해상충 진술 없음 |

# Q1~Q8 판정 (닻 페이지 수집 지침)

| Q | 판정 | 근거 |
|---|---|---|
| **Q1** 접촉 손실 정량 | **없다 — `θ(N)` 0/68 · 층 하나: 정적 `θ₀` 닫힌 식 후보** | 시간 · 열화 0. `[재현]` 통째 비연결 분율 `1 − P^e(Z_NN)`, `Z_NN = 6ψρ/(ψρ + 1 − ψ)` — 22호 세 점 대조에서 기각(§(b)) · 인쇄식 ↔ 그림 꼴 차(`P` ↔ `√P`) |
| **Q2** 독립 관측 | **없다** | 실험 0 · 자기 측정 0 — 검증은 선행 편의 시뮬레이션 대조로 위임 |
| **Q3** 라벨 층위 | **computed-analytic(좌표수 평균장 + [31] 경험식) — 검증 위임 · 오차 0 · 인쇄식과 그림이 세 곳에서 다른 함수** | 그림 6 · 8 = `√P` · 식 (24) 분자 오기 · 그림 7 = `P` 미적용 · 그림 9 · 10 이름표 ↔ 값(§(a')) |
| **Q4** 유일성 · 식별성 | **0/68 — 예순 번째 성질** "퍼콜레이션 확률을 평균 좌표수 하나의 결정론적 경험식으로 두고 인쇄한 식과 다른 함수(√P)로 그림을 그렸으며, 입도비 두 점 · 폭 두 점의 무차원 곡선을 '일반해' 로 내놓으면서 문턱 · 산포 · 검증 자료를 한 번도 적지 않았다" | `threshold` · `error` · `±` · `fit` 0 · "sufficiently accurate" · "carefully checked" 1 씩 |
| **Q5** Li-In 기준 | **해당 없음** | SOFC · Li 0 · 기준극 0 |
| **Q6** 압력 | **없다** | `pressure` 0 · 접촉각 29.5° 한 값(목 크기의 대리 — 출처 0) |
| **Q7** dead Li | **해당 없음** | 무음극 아님 · Li 0 |
| **Q8** 화학 · OCP | **해당 없음 · 층 하나** | LSCF/YSZ · 크기비 1 · 2.5 · 폭 0 · 0.6 · `φ_g` 0.4 · OCP · 용량 0 |

# ★ (a) 모형의 정체 — 인용한 것 · 새로 한 것 · 가정 · 크기비의 방향

## 인용한 것 ↔ 새로 한 것

| 층 | 식 | 출처 (`[인쇄]`) | 이 편이 한 일 |
|---|---|---|---|
| 좌표수 | (1)–(4) | [11](자기 2009 — Suzuki–Oshima [15] 식을 접촉 수 보존에 맞게 수정) · `Z̄ = 6` [10, 12, 30] | 그대로 사용 |
| 퍼콜레이션 확률 | (5) | **[31] Bertei & Nicolella 2011**(무작위 강체구 충전의 퍼콜레이션 비교 · 확장 이론) | 그대로 인쇄 — ⚠ 그림은 다른 꼴(§(a')) |
| **MIEC 배정** | (6) · (23) | — | ★ **새로**: `P^i_LSCF = 1` · `P^e_LSCF = P_LSCF`(A 클러스터) |
| TPB 자리 | (7) · (8a–c) | [11, 12, 20, 22, 34] | 가정 셋을 나란히 · 그림은 (8b) 만 |
| 노출 MIEC 표면 자리 | (9) · (26) | — | ★ **새로**(인용 0) — ⚠ 그림 7 은 `P` 없이 |
| 전해질 면 자리 | (10)–(12) | [11, 20] | 그대로 |
| 입자간 이온 전도도 | (13)–(17) | [10, 11, 35–37] | 그대로 |
| **LSCF–YSZ 입자간 전도도** | (18) | — | ★ **새로**: 두 계산법 비교 → 작은 입자층 `min(r)` |
| 수력 반경 | (19) · (29) | [11, 38] | 그대로 |
| 다분산 | (20)–(22) · 표 1 · (24) | [17] · [11, 39] | 그대로 — ⚠ (24) 분자 오기 |
| 무차원화 · 그림 | (30)–(34) · 그림 6–12 | — | ★ **새로**(곡선 넷씩) |

## 가정 (지면에 있는 것 · 없는 것)

- **무작위 충전 강체구**(`[인쇄]` "a multi-component mixture of randomly packed spherical particles") · **`Z̄ = 6`**("random close packing of rigid spherical particles") — 공극률 · 크기 분포와 무관한 상수.
- **목(neck) = 접촉각 한 값**: `r_c = min(r_LSCF, r_YSZ) sin θ` · 계산 예 · 그림 7 에 `θ = 29.5°`(출처 0). 소결은 낱말로 나오지 않는다(`sinter` 0) — `[해석]` 목이 있는 **소결 전극**을 전제한 기하다.
- **크기 분포**: 수(개수) 정규분포를 ±1.257σ 로 잘라 9 등분(표 1) · 두 상 각각 `(r̄, ϑ̃)`.
- **부피 분율 ψ 는 고상 기준**(명명법 "solid volume fraction") · 공극률 `φ_g` 는 `n^V` 의 `(1−φ_g)` 로만.
- **무한계**: 확률 식이 무한 클러스터 소속 분율의 경험식 — 전극 두께 · 집전체 면 · 배열 산포 0. `[인쇄]` A 클러스터를 "extends throughout the entire thickness … from the dense electrolyte to the
  electrode current collector" 로 정의하지만 두께는 식에 없다.
- **LSCF 전 크기 부류가 같은 `P^e`**(식 (24) 의 평균 좌표수 하나) — 큰 입자와 작은 입자의 연결 확률이 같다.

## 한 상만 키우면 그 상의 연결 확률은? — 닫힌 식 (`[재현]`, 식 (2) · (21) · (24) · (23))

```
Z_NN = Z̄ · ψ ρ / (ψ ρ + 1 − ψ) ,   ρ = r₃₂(이온 전도체) / r₃₂(MIEC)     (r₃₂ = Σ p r³ / Σ p r² — 두 상 ϑ̃ 가 같으면 r₃₂/r̄ 가 약분)
P^e  = 1 − ((4.236 − Z_NN)/2.472)^3.7        (인쇄 식 (23))       ·   그림 6 · 8 은 √P^e
P^e = 0 ⇔ ρ ≤ ρ_c = 1.764 (1−ψ) / (4.236 ψ)      P^e = 1 ⇔ ρ ≥ ρ_1 = 4.236 (1−ψ) / (1.764 ψ)      ρ_1/ρ_c = (4.236/1.764)² = 5.77   (Z̄ = 6)
```

- ✅ **방향**: `∂Z_NN/∂ρ > 0` — 이온 전도체를 고정하고 MIEC(= NCM 짝)만 키우면 `ρ` 가 줄어 `Z_NN` · `P^e` 가 준다. 부피 분율을 고정해도 그렇다. 22호 명제의 **방향**은 이 식에서 나온다.
- **크기 효과는 비(比)뿐이다** — 두 상을 같이 키우면 아무것도 안 변한다(척도 불변). 절대 크기는 `λ` · `S` · `σ` 의 차원 인자(1/r̄², 1/r̄, r̄)로만 들어간다.
- **전이 폭**: 연결 분율 1 → 0 이 크기비 ×5.77 안에서 끝난다(ψ 무관). ψ 0.49 에서 `ρ_c` 0.433 · `ρ_1` 2.50 — 크기비 1 에서 문턱 ψ 0.294(`[재현]` 1.764/6), 2.5 에서 0.143(그림 6 · 8 과 일치).
- ⚠ 지면은 **MIEC 가 이온 전도체보다 큰 경우(ρ < 1)를 그리지도 말하지도 않는다** — 그림의 크기비는 1 · 2.5 이고 서술은 "When larger YSZ particles are used … will shift" 까지다.

# ★ (a') 재현 — 인쇄식으로 곡선 그림 일곱 장(6–12)을 다시 계산 (`[재현]`)

`r̄_LSCF = 1` · `(1−φ_g)` · `sin θ` 는 무차원화로 약분 · 그림 7 만 `θ = 29.5°` · 그림 12 만 `φ_g = 0.40` · `a = π min(r)² sin²θ`(G5). 파이썬 스크립트(스크래치)로 식 (2)·(4)·(21)–(29)·(30)–(34)를
9 × 9 부류 그대로 합산했다.

| 그림 | 인쇄식 그대로 | 고치면 | 재현 정도 |
|---|---|---|---|
| **6** `λ̃^V` | 문턱 위가 완만 · 최대 2.169 @ 0.56–0.57 | **`P^e` → `√P^e`** | ψ ≥0.41 네 곡선 ±0.01(§그림) |
| **7** `S̃` | 문턱 아래 0 | **`P^e P^i` → 1** | 전 구간 ≤0.005 |
| **8** `λ̃^S` | ψ 0.37 에서 0.586 | **`√P^e`** | ψ ≥0.37 ±0.005 · 흑 · 자홍 · 청 포함 |
| **9 · 10** `σ̃` | 값은 그대로 맞음 | **이름표를 색 규약으로** | ±0.03(30 여 마커) |
| **11** `σ̃_LSCF-YSZ` | 그대로 | — | ±0.03 · 이름표 일치 |
| **12** `r̃_g` | 그대로 (`φ_g` 0.4) | — | 일치 |
| 식 (24) | 분자 `Z_LSCFk,YSZℓ` → 문턱이 거꾸로(ψ > 0.706 에서 `P = 0`) | **`Z_LSCFk,LSCFℓ`** | 그림 6 · 8 의 출발 0.294 · 0.143 은 고친 식으로만 |
| 계산 예 | r̄_YSZ 200 nm · 40 nm(크기비 5 → 5.1 × 10¹³) | **(2.5, 0.6, 0.6) · r̄_LSCF 40 nm** | 9.56 × 10¹³ ↔ 인쇄 9.3 × 10¹³(+2.8 %) |

⇒ **이 편의 모형은 지면의 식만으로 완전히 복원된다 — 단 세 군데를 고쳐야 한다.** 그 셋 중 둘(√P · 그림 7 의 P 미적용)은 **퍼콜레이션 인자 자체**에 걸린다: 인쇄식대로면 문턱 바로 위의
연결 확률이 그림의 ≈½–⅔ 이다(ψ 0.33 에서 0.287 ↔ 0.536). `√P` 가 [31] 원식의 바깥 지수인지, 코드의 차이인지는 [31] 을 열어야 정해진다(G2 · 미열람) — `[해석]` 우리가 이 편의 식을 쓸 때는
**두 꼴을 모두 계산해 폭으로 둔다**.

# ★ (b) 22호 명제의 정량 대조 (`[재현]` — 입력은 22호 digest 사본, 모형은 이 편 식)

## 입력 — 있는 것 · 없는 것

| 입력 | 22호 값 | 이 편 식에서의 자리 | 판정 |
|---|---|---|---|
| NCM 입도 | d₅₀ **4.0 / 8.3 / 15.6 µm**(d₉₀ 4.8 / 13.0 / 26.1) · 측정법 미기재 · L = M 을 체로 거른 것(22호 D2) | `r₃₂(NCM)` — 식은 **수 분포 Sauter 반경**을 본다 | ⚠ d₅₀(부피 가중일 가능성) → r₃₂ 환산 불가 — **d₅₀ 을 Sauter 지름으로 둔다**(가정) |
| 조성 | 7 : 3 w/w · 무탄소 · 무바인더 → NCM **48–50 vol%**(고상; 22호 digest 밀도비 2.35–2.45 → 48.8–49.8 · 문헌 밀도 4.75/1.87 → 47.9) | ψ = **0.479–0.498**(고상 기준 — 식이 요구하는 바로 그 기준) | ✅ 공극률(미측정)은 이 식의 `P` 에 안 들어간다 — **공극률 없이도 비교가 선다** |
| **SE 입도** | **미인쇄**(β-Li₃PS₄ THF 습식 합성 · NCM 과 ZrO₂ 볼 140 rpm 30 분 밀링) | `r₃₂(SE)` — 크기비 `ρ` 의 분자 | ❌ **폭으로 둔다** — d_SE 0.5–20 µm |
| 분포 폭 | 미인쇄(d₉₀/d₅₀ 만) | 두 상 ϑ̃ 가 같으면 약분 · 다르면 `r₃₂` 비로만 | 폭은 `ρ` 에 흡수 — 따로 폭을 두지 않는다 |
| 좌표수 | — | `Z̄ = 6`(강체구 RCP 가정) | ⚠ 375 MPa 압착 복합체에는 가정 밖(§(c)) — 아래 표는 식 그대로 |
| `P` 꼴 | — | 인쇄 `P`(β = 1) · 그림 꼴 `√P`(β = 0.5) | 둘 다 계산 |
| 측정 | `f_inactive` **2 / 27 / 31 %**(XRD 두 상 · 첫 C/10 충전 뒤 · 집전체 면 표층 가중) · 용량만의 상한 **≤3 / ≤39 / ≤44 %** | 모형 쪽 = 통째 전자 비연결 `1 − P^e` | 22호 digest §5-1-b: `f_inactive ≥ 1 − θ^elec`(같은 자리 · 합집합 상한) |

## SE 입도를 훑으면 — 예측 비연결 분율 S / M / L (%, `[재현]`)

| d_SE (µm) | β = 1 · ψ 0.479 | β = 1 · ψ 0.498 | β = 0.5 · ψ 0.479 | β = 0.5 · ψ 0.498 |
|---|---|---|---|---|
| 1 | 100 / 100 / 100 | 100 / 100 / 100 | 100 / 100 / 100 | 100 / 100 / 100 |
| 2 | 82 / 100 / 100 | 70 / 100 / 100 | 58 / 100 / 100 | 45 / 100 / 100 |
| 3 | 30 / 100 / 100 | 24 / 100 / 100 | 16 / 100 / 100 | 13 / 100 / 100 |
| 4 | 11 / 89 / 100 | 8 / 76 / 100 | 6 / 67 / 100 | 4 / 51 / 100 |
| 5 | 4 / 54 / 100 | 3 / 45 / 100 | 2 / 33 / 100 | 1 / 26 / 100 |
| 6 | 1 / 34 / 100 | 1 / 27 / 100 | 1 / 18 / 100 | 0 / 14 / 100 |
| 8 | 0 / 13 / 78 | 0 / 9 / 66 | 0 / 7 / 53 | 0 / 5 / 42 |
| 10 | 0 / 5 / 47 | 0 / 3 / 38 | 0 / 2 / 27 | 0 / 2 / 21 |
| 12 | 0 / 2 / 28 | 0 / 1 / 22 | 0 / 1 / 15 | 0 / 0 / 12 |
| 15 | 0 / 0 / 13 | 0 / 0 / 9 | 0 / 0 / 7 | 0 / 0 / 5 |
| **측정** | **2 / 27 / 31** | ← | ← | ← |

⇒ **SE 입도를 모르면 한 크기의 예측은 0–100 % 전 구간으로 퍼진다** — 한 점 비교로는 아무것도 기각되지 않는다. 기각은 **세 점의 패턴**에서만 선다.

## 두 읽기 — 저자 배정 읽기 · 상한 읽기

**① 저자 배정 읽기**(22호 `[인쇄]` "not all of the particles are electronically connected" — `f_inactive` = 전자 비연결):

| | β = 1 | β = 0.5 |
|---|---|---|
| 한 점씩 맞추는 d_SE | S 5.2–5.6 · M 6.0–6.5 · **L 10.7–11.6 µm** | S 4.6–5.0 · M 4.9–5.3 · **L 8.9–9.6 µm** |
| S · M 을 같이(d_SE 6.0–6.5 / 4.9–5.3) | **S/M/L = 0.7 / 27.1 / 100 %** | **1.4 / 27.0 / 100 %** |
| 셋 최소제곱(d_SE 10.3–11.1 / 8.5–9.2) | **0.0 / 2.6 / 34.8 %** · RMSE 14.3 %p | **0.0 / 3.6 / 34.8 %** · RMSE 13.7 %p |

- **S → M(2 → 27 %)은 재현된다**(d_SE ≈5–6.5 µm). **그 크기에서 L 은 100 % 비연결** — 측정 31 % 도, 22호 **용량만의 상한 ≤44 %** 도 넘는다(용량은 벌크 평균이라 표층 가중과 무관한 대조다).
- **구조적 이유**: 이 식에서 비연결 27 % → 31 % 는 크기비 ×**1.04–1.05** 안에서 지나간다(`[재현]` β = 1 · ψ 0.49: ρ 0.744 → 0.711). 22호 M → L 은 같은 로트에서 크기 ×**1.88** — **"M ≈ L" 의 평탄은
  이 함수족 밖이다.** `Z̄` 를 바꿔도(8 이면 ×1.04) · 두 상 폭을 달리해도(`r₃₂` 비로 흡수) · `√P` 로 바꿔도 같다.
- 01호 SE(3 µm)를 그대로 넣으면 **S 13–30 · M 100 · L 100 %** — 01호 식 (8) 의 ≈23–40 / 95 / 95–97 %(개념 페이지 22호 절)보다도 멀다.

**② 상한 읽기**(22호 digest §5-1-b · 개념 페이지 — `f_inactive ≥ 1 − θ^elec`, 합집합 · 표층):

- 세 측정을 **상한**으로 두면 모형과 모순 없는 영역은 **d_SE ≥ 10.7–11.6 µm(β = 1) · ≥ 8.9–9.6 µm(β = 0.5)** — SE 의 Sauter 지름이 **NCM-M d₅₀ 보다 커야** 한다. 그 경계에서 모형 전자 비연결은
  **S 0 · M 2.0–3.0 · L 31 %**(용량 상한만 쓰면 d_SE ≥ 7.9–10.2 · M 4.2–5.1 %).
- ⇒ 이 읽기에서 **M 의 27 % 중 전자 비연결은 ≤3 %p(≤11 %)** — 나머지 ≥89 % 는 이온 경로 · SE 접촉 없음 · 2차 입자 내부 · 율(22호 digest §5-1-b 의 합집합 항)이어야 한다. **22호의 "medium and
  large … not electronically connected" 와 반대 배정이다.**

## 판정

**어느 읽기로도 22호 명제의 정량은 이 식으로 서지 않는다** — ① 전자 배정 그대로면 세 점 동시 재현 불가(L 100 %), ② 상한으로 읽으면 M 의 불활성이 거의 전부 전자 밖이 된다. 서는 것은 **방향**(CAM 이
SE 에 비해 커지면 전자 연결이 준다)뿐이고, 그 방향은 01호 복셀 모형도 준다(기구는 다르다 — §(e)).

⚠ 대조의 한계(`[해석]`): (i) d₅₀ ↔ `r₃₂` 환산 미상 (ii) **압착 복합체의 "SE 입자 크기" 는 잘 정의되지 않는다** — SE 는 소성 변형해 연속 기질이 된다(55호 `μ_SE` 5.2 µm · k 1.54) (iii) `Z̄ = 6` · 무한계 —
22호 L 전극(≈90 µm)은 `[재현]` d₅₀ 기준 **≈5.8 입자 두께**, M 10.8 · S 22.5 — 유한 두께에서는 집전체에 닿은 유한 클러스터(B 형)도 전자를 받는다 (iv) 22호 NCM-S 는 다른 로트(22호 G7) —
깨끗한 크기 대조는 M ↔ L 쌍이고, 모형이 가장 크게 틀리는 곳이 바로 그 쌍이다 (v) `f_inactive` 는 첫 C/10 충전 한 점 · 표층 가중.

# ★ (c) SOFC ↔ ASSB 전이 조건 (`[해석]` — 이 편은 ASSB 를 한 번도 말하지 않는다)

| 축 | 이 편(SOFC 공기극) | 무탄소 NCM + 황화물 SE 복합양극 | 전이 |
|---|---|---|---|
| 상 구성 | MIEC(LSCF: e⁻ + O²⁻) + 순수 이온 전도체(YSZ: O²⁻) + 기공 | CAM(NCM: e⁻ + 고체 내 Li⁺) + 순수 이온 전도체(SE: Li⁺) + void | ✅ **구조가 닮았다** — 22호가 이 편을 고른 이유로 읽힌다 |
| MIEC 의 이온 경로 | `[인쇄]` `P^i_LSCF = 1` — LSCF 가 입자 사이 이온 경로를 맡는다 | NCM 입자 사이 Li⁺ 전달은 경로로 치지 않는다(01호: AM 이온 전도도 5–6 자릿수 낮음 가정) | ❌ **옮기면 안 되는 배정** — NCM 은 SE 접촉이 이온 조건이다 |
| 접촉 | 소결 목 · 접촉각 한 값 29.5° | 냉간 압착(22호 375 MPa) · SE 소성 변형 · 목 없음 · 운전 압력(55 MPa) 의존 | ❌ `r_c = min(r) sin θ` 는 압력 · SE 연성의 함수가 된다 |
| 충전 · 좌표수 | 강체구 RCP `Z̄ = 6`(공극 ≈36 %) | 공극 수 %–20 %(14호 XRM 4.5–9.8 vol% 등) — 강체구로는 도달 불가(RCP 한계) → 변형 · `Z̄ > 6` | ❌ **좌표수가 커지는 쪽**으로 틀린다 — 연결 과소 예측(=비연결 과대) 방향. (b) 의 L 100 % 와 같은 쪽 |
| "SE 입자" | 구형 YSZ 입자 | 연속 기질(55호) — 입자 크기 정의가 흐리다 | ❌ `ρ` 의 분자가 측정 가능한 양인지부터 문제 |
| 운전 온도 | 600–800 °C(σ⁰ @ 800 °C 인용) | 25 °C | 전도도 절대값 · 입자간 계면 항(δ 5 nm)은 옮길 수 없다 — **연결 확률 `P` 는 온도 무관 기하** |
| 반응 자리 | (기체–LSCF–YSZ) TPB + 기체에 드러난 LSCF 표면 | **2상 CAM\|SE 계면**(기체 없음) — void 는 반응물 통로가 아니라 죽은 부피 | ✅ 짝은 **Assumption 1**(2상 교차 면적 `π r_c²`) — 이 편은 인쇄만 하고 그리지 않았다 |
| 부피 변화 | 운전 중 치수 안정(열팽창만) | NCM `ΔV/V` 2–8 %(66 · 67호) · 충방전마다 | ❌ **시간축 0** — 정적 `θ₀` 까지만 |
| **용량** | **없다** — 끊긴 LSCF 는 **반응 자리만** 잃는다 | 끊긴 NCM 은 **용량을 잃는다** | ❌★ `1 − P^e` 가 들어가는 칸이 다르다(아래 (d)) |
| 크기 | 수십 nm – µm(계산 예 r̄ 40 nm) | NCM 2차 입자 d₅₀ 4–16 µm(내부 다공 · 다결정) · 전극 두께 ≈6–22 입자 | ⚠ 무한계 식의 전제가 L 에서 약하다 |

⇒ `[해석]` **닮은 것은 "두 전도 네트워크가 한 상에서 겹친다" 는 위상 구조뿐이다.** 이 편의 식에서 ASSB 로 옮길 수 있는 것은 **좌표수 → 연결 확률의 사상(寫像) 한 줄과 "크기 효과는 비" 라는 형태**이고,
`Z̄` · 접촉각 · MIEC 이온 배정 · 무한계는 전부 다시 정해야 한다. 22호가 "in agreement with percolation theory" 로 기댄 것은 그 **형태(방향)** 이다.

# ★ (d) Q1 · 정적 `θ₀` · 곱 축퇴

## 정적 `θ₀` 의 예측식이 되는가

- `[재현]` 된다 — **`θ₀ = P^e(Z_NN(ψ, ρ))`**, 통째 전자 연결 분율의 닫힌 식(불활성 = 1 − θ₀). 입력 셋: 고상 CAM 분율 ψ · 크기비 `ρ = r₃₂(SE)/r₃₂(CAM)` · `P` 의 꼴. 공극률 · 온도 · 전극 두께는 안 들어간다.
- 그러나 (b) 에서 22호 세 점을 동시에 못 맞추고, (c) 에서 `Z̄` · `ρ` 가 ASSB 에서 정의 · 값이 흔들린다. **Q1 칸 이동 없음 — `θ(N)` 0/68.** 시간축 0 · 열화 0 · `time` 1 회("time consuming").

## 곱 축퇴 — 반응 자리 밀도가 기하 인자의 곱이다

`[인쇄]` 식 (7) `λ^V = γ · n^V_LSCF · Z_LSCF,YSZ · P^e_LSCF · P^i_YSZ`. `[재현]` ASSB 쪽 짝인 Assumption 1(`γ = π r_c²`, `r_c = min(r_N, r_S) sin θ`)로 풀면

```
λ^V(면적/부피) = [3 (1−φ_g) ψ_N / r_N] · [ Z_NS · sin²θ · (min(r_N, r_S)/r_N)² / 4 ] · P^e_N · P^i_S
             =        a_s(= 3ε_p/R)      ·            φ_cov(부분 피복)                 · P^e  · P^i
```

- 9호 P2D 의 `j = I/(A_eff · a_s · A · L)` 과 대면 **`A_eff ≙ φ_cov · P^e · P^i`** — 부분 피복 `φ_cov = Z_NS sin²θ/4`(`[재현]` ψ 0.5 · 크기비 1 · θ 29.5° 에서 0.18)와 통째 연결 `P^e` 가
  **한 곱**이다. 반응 속도 상수(`j₀` 또는 TPB 길이당 교환전류)를 어떤 꼴로 붙여도 `j₀ · sin²θ · Z_NS · P^e · ε_p/R` 로만 전류에 들어간다 ⇒ **곱 축퇴의 기하 판** — 이 편은 그 곱의 **기하 쪽 인자를
  따로따로 적은 해석식**(우리 위키에서 처음)이지만, 동역학 상수가 없어 곱을 가르지 않는다.
- ★ **SOFC 에는 용량 칸이 없다** — 그래서 이 편에서 `P^e` 는 **반응 자리(동역학) 칸에만** 들어간다. ASSB 로 옮기면 끊긴 NCM 은 용량도 잃으므로 `P^e` 는 **`ε_p` 자리(용량 + 동역학 분모)** 로 가야
  한다 — `ε_p → P^e ε_p`. 그러면 통째 비연결은 **`LAM_PE` 와 같은 파라미터**가 된다(27 · 28 · 37 · 58호가 이미 본 구조 — [[assb-synthetic-truth-contact-loss-requirements]] R1). 반대로 `φ_cov` 는
  `A_eff` 자리(`j₀` 와 곱)에 남는다 — **이 편의 식 안에서 R7(통째 `u = 1 − P^e` ↔ 부분 피복 `φ`)이 두 인자로 이미 갈라져 있다.** 둘 다 정적이다.
- **무엇을 적합했나: 없다.** 식 (5) 의 상수(4.236 · 2.472 · 3.7)는 [31] 의 경험식(무작위 충전 시뮬레이션에 맞춘 것으로 읽힌다 — [31] 미열람) · `Z̄ = 6` · `θ = 29.5°` 는 가정 · 곡선은 전부 순방향.
  **검증 자료: 이 편 안에 0** — 선행 편의 시뮬레이션 대조 위임(G1).

# ★ (e) 01호 모형과의 관계 — 같은 양, 다른 계산

| 항목 | **01호** Bielefeld 2019 | **68호** 이 편 |
|---|---|---|
| 양 | `θ_AM = V_c/V_ν` — 집전체 면에서 자란 **전자 클러스터에 속한 AM 부피 분율** | `P^e_LSCF` — MIEC 가 **A 클러스터(무한 클러스터)** 에 속할 확률 |
| 계산 | 복셀(0.2 µm) 3D 무작위 충전 + Hoshen–Kopelman · 도메인 80 × 80 × 140 µm · 전이 구간 10 배열 | 평균 좌표수 한 값 → 경험식 `P(Z)` · 무한계 · 결정론 |
| 연결 판정 | 복셀 인접(간격 ≲0.2 µm) · 겹침은 AM 에 배정 | 접촉 = 좌표수(강체구 RCP 평균장) |
| 폭 | ★ 같은 거시 파라미터에서 θ ≈30 ↔ ≈70 % 이봉 · `p_c` 는 구간 | **0** — 결정론적 한 값 |
| 크기 | AM 구 단분산 3–15 µm · **SE 3 µm 고정** — 01호 digest §4.2: AM 을 SE 와 **따로** 배치(겹침 제거) | 두 상 크기비 · 분포 폭 — **크기는 비로만** |
| 부피 축 | `g^V_AM`(**전체 부피** · 공극 포함) | ψ(**고상**) · `Z̄` 가 공극률과 무관 |
| 문턱 정의 | 10 배열 평균 θ = **40 %** 인 `g^V_AM` | 식의 `P = 0`(Z 1.764) — 이름 0 |
| 크기 효과 `[재현]`(SE 3 µm · θ/P = 0.4) | d 3 → 15 µm: **45.3 → 57.9 vol%**(식 (8)) | **34.7 → 72.7 %**(인쇄 `P`) · **31.3 → 69.5 %**(`√P`) — 기울기 ×3 · d ≈5.5–7 µm 에서 교차 |
| 22호 대조 | 3–15 배 과대(개념 페이지 22호 절) | 저자 배정 읽기에서 세 점 동시 불가 · 01호 SE 로는 S 13–30 · M · L 100 % |

- `[해석]` **크기 효과의 기구가 다르다.** 68호는 크기비 `ρ` 로만 크기를 본다(척도 불변). 01호는 AM 구를 SE 와 독립으로 배치하므로 연속체 극한에서는 같은 크기 구의 연결이 부피 분율만의 함수여야 하는데
  `p_c` 가 d 에 따라 움직인다 — 그렇다면 01호의 d 의존은 **이산화 쪽**(복셀 접촉 거리 0.2 µm 가 d 에 대해 3 µm 에서 6.7 %, 15 µm 에서 1.3 % · 도메인 폭이 d 의 27 배 ↔ 5.3 배)일 가능성이 있다.
  01호는 원인을 말하지 않는다 — **가설이고 검증하지 않았다**(01호를 다른 해상도로 다시 돌리면 가를 수 있다).
- `[해석]` 둘 다 22호 L 을 크게 과대 예측한다 — 서로 다른 두 모형 계열(해석 평균장 · 복셀 시뮬레이션)이 **강체 · 무작위 · 변형 없음** 이라는 공통 가정에서 같은 쪽으로 틀린다. 실재 압착 복합체의
  CAM–CAM 망이 두 모형보다 잘 이어진다는 22호 digest §5-2 의 추론과 같은 방향이다.
- 01호 §3.3 "may allow estimating the effective … conductivity"(조건법)에 대해: SOFC 쪽에는 **이온** 유효 전도도를 좌표수로 계산한 선례가 있다(이 편 식 (13)–(18), 무차원) — 그러나 **전자** 전도도는
  이 편도 식이 없다(G7). 22호가 잰 전자 전도도 3 자릿수 하락과 대질할 식은 여전히 없다.
- 01호의 "`p_c` 는 유한 시료에서 폭" 은 이 편에 **대응물이 없다** — 무한계 평균장이라 폭이 구조적으로 0 이다. 합성 truth 에 이 편의 식을 쓰면 01호가 경고한 폭(±20 %p)이 지워진다.

# (f) Q5 · Q6 · Q7 — 인쇄된 대로

- **Q5 해당 없음** — SOFC, Li · In · 기준극 0.
- **Q6 없다** — `pressure` 0. 접촉은 접촉각 한 값(29.5°, 출처 0)으로 대리한다. `[해석]` ASSB 에서는 이 자리가 압력의 함수다.
- **Q7 해당 없음** — 음극 · 무음극 0.

# 귀속 검사 — 22호 · 01호 · 원장 행이 이 편에 매단 것

| 인용처 | 매단 명제 | 이 편 | 판정 |
|---|---|---|---|
| **22호** ref 26 · §2-5(:198–205) | "in the case of medium and large NCM622, not all of the particles are electronically connected … This is in agreement with percolation theory" | MIEC 전자 경로 = A 클러스터 확률(식 (6)) ✅ · 크기 방향 = 식 (2) · (23) 에서 `[재현]` ✅ · 지면 서술 · 그림은 크기비 1 · 2.5(이온 전도체가 같거나 큼)뿐 · 22호 조성에 대면 세 점 동시 불가(저자 배정 읽기) · 상한 읽기에서는 M 이 거의 전부 전자 밖 | ⚠ **방향만 선다** — "agreement" 는 정성 일치의 표현이고, 이 편의 식으로 정량 일치는 안 된다 |
| **22호** 후속 표(:575) | "저자가 기댄 'percolation theory' — SOFC 원전. 1호 모델과의 관계 · Q1" | SOFC 원전 ✅(LSCF + YSZ · 소결 목 · 800 °C 인용값) · "원전" 의 성격 = **좌표수 평균장 해석식**(시뮬레이션 · 실험 아님) · 01호와의 관계 = 같은 양의 다른 계산(§(e)) | ✅ **흡수** — 정정 제안(wiki 밖): "해석식 · 무한계 · 크기는 비로만 · 인쇄 `P` ↔ 그림 `√P` · 22호 세 점 동시 불가" |
| **01호**(호출자 지정) | `p_c` 폭 · §3.3 "may allow estimating the effective … conductivity" | 폭 대응물 0(결정론) · 이온 유효 전도도 식은 있다 · 전자 전도도 식 0 | 관계만 기록 — 01호는 이 편을 인용하지 않는다(01호 digest 기준) |
| 원장 §1 행 | "22호가 기댄 'percolation theory' (SOFC) — 01호 모델과의 관계 · Q1" | 위와 같음 | ✅ 흡수 — 지목 22 · 1 그대로(위키에 다른 인용 0) |

⚠ 시점: 이 편(2013-03)은 01호(2019) · 22호(2018)보다 앞이다. 이 편은 전지를 한 번도 말하지 않는다.

# 인용 대조 — 우리 위키 · 원장에 원전 · 관련 digest 가 있는 것

| 이 편 인용 | 우리 호 · 원장 | 이 편이 적은 것 | 대조 · 넘길 것 |
|---|---|---|---|
| **[31] Bertei, Nicolella 2011 *Powder Technol.* 213, 100–108** "A comparative study and an extended theory of percolation for random packings of rigid spheres" | 원장 0 · 위키 0 | 식 (5) `P(Z)` 의 출처 | **신규 후보(★)** — 인쇄식 ↔ 그림 `√P` 차를 가르는 곳(바깥 지수) · 해석식 ↔ 시뮬레이션 **오차 크기**가 있을 수 있다(비교 연구 — 제목 기준 `[해석]`) |
| [39] Bertei, Choi, Pharoah, Nicolella 2012 *Powder Technol.* 231, 44–53 "Percolating behavior of sintered random packings of spheres" | 0 | 식 (24) 의 근거([11, 39]) | ☆ — 목(접촉각) · 소결이 문턱을 얼마나 옮기나 — ASSB 압착 접촉의 대리 변수 후보 |
| [17] Chen D., Lu, Li, Yu, Kong, Zhu 2011 *JPS* 196, 3178–3185 | 0 | 표 1 · 식 (20)–(23) 의 "carefully checked" 검증 | ☆ — 이 편이 위임한 **유일한 검증 자리**(무작위 충전 재구성 [9] 대조) |
| [11] Chen D., Lin, Zhu, Kee 2009 *JPS* 191, 240–252 | 0 | 식 (1)–(4) · (19) · 3 성분 | ☆ |
| [15] · [30] Suzuki, Oshima 1983 *Powder Technol.* 35, 159 · 1985 44, 213 | 0 | 좌표수 원식 · `Z̄ = 6`([10, 12, 30]) | ☆ — `Z̄` 의 공극률 의존이 원전에 있는지 |
| [16] Bouvard, Lange 1991 *Acta Metall. Mater.* 39, 3083–3090 | 0 | 좌표수 경험식의 계보 | ☆ — 이성분 분말 퍼콜레이션 ↔ 좌표수(제목) |
| [12] Costamagna, Costa, Antonucci 1998 *Electrochim. Acta* 43, 375–394 | 0 | A/B/C 명명 · TPB 식 | ☆ |
| [9] Kenney, Valdmanis, Baker, Pharoah, Karan 2009 *JPS* 189, 1051–1059 | 0 | 무작위 충전 재구성 — 검증 기준 모형 | ☆ — 01호 · 2호 같은 **시뮬레이션 계열의 SOFC 판** |

⚠ 이 편은 전지 논문을 하나도 인용하지 않는다. 22호 · 01호 · 53호 어느 편도 이 편의 [31] · [39] 를 인용하지 않는다(digest 기준).

# 곱 축퇴 처방 — 쉰한 번째 적용 (`[[assb-lampe-contact-product-degeneracy]]`)

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | 전기화학 측정 0 | ❌ |
| **2단계** (18 · 25호) | + 면적을 아는 대조군 | 면적은 **계산**(식 (7)–(9)) — 측정 0 | ❌ |
| **3단계-a/b** (19호) | `Ea` · `C` 상한 | 0 | ❌ |
| **4단계** (20호) | 시간 영역 | 0 | ❌ |
| 22호 줄 "SOC 추종 상 분율" | `θ·ε_p` 를 뗀다 | 해당 없음 | — |
| 52호 줄 | 누적 결손 ↔ Li 재고 | 해당 없음 | — |

⇒ **적용 불가(입력 없음).** 기록 이유: 이 편의 반응 자리 식은 **면적 인자를 기하로 분해해 적은 해석식**이다(우리 위키에서 처음) — `[재현]` Assumption 1 판 `A_eff ≙ (Z_NS sin²θ/4)(min r/r_N)² · P^e · P^i`. 곱 안의
각 인자(접촉각 · 좌표수 · 크기비 · 연결 확률)에 **물리 이름이 붙어 있어도** 반응 속도 상수가 붙는 순간 한 곱이다. 그리고 SOFC 식은 용량 칸이 없어 `P^e` 를 동역학 자리에만 둔다 — ASSB 로 옮길 때
`P^e` 를 `ε_p` 자리로 옮기지 않으면 **통째 비연결이 `j₀` 와 곱이 되는 모형**이 되고, 옮기면 `LAM_PE` 와 같은 파라미터가 된다(합성 truth R1 · R7).

# 보류 결정 (가)(나)(다)(아)(자)(차)(타) — 이 편이 주는 근거 (결정 안 함)

원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §3-b 와 대조. **결정은 사용자 몫이다.**

| # | 결정 | 이 편 | 근거 |
|---|---|---|---|
| 가 | 29호 Q4 +0.5 유지 | 무관 | 적합 · 식별성 진단 0 |
| 나 | 38호 Q2 +0.5 유지 | 무관 | 측정 0 |
| 다 | 28호 Bizeray 를 ASSB Q4 분모에 | 무관 | — |
| 아 | 35호 합성 쌍 → Roman 특징 재계산 | 무관 | ML 0 |
| 자 | 31호 ICI zenodo `R/k` 면적 소거 | 무관 | — |
| 차 | 23호 PyBaMM 면적 노브 / `j₀` 노브 분리 | **정성 메모 하나** | 면적 노브를 기하 인자(`Z_NS · sin²θ · P^e`)로 매개화하는 해석식이 있다 — 그러나 `j₀` 와의 곱은 그대로라 노브 **분리의 근거는 아니다**. 결정 재료 아님 |
| 타 | Navidi 2024 digest 재점검 | 무관 | — |

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 어디 | 판정 |
|---|---|---|---|
| **D1** | ★★★ 식 (5) · (6) · (23) `P = 1 − ((4.236 − Z)/2.472)^3.7` ↔ 그림 6 · 8 은 **`√P`** 로 계산됨(`[재현]` 그림 8 적 ψ 0.37–0.49 판독 0.806 · 1.030 · 1.228 · 1.399 ↔ `√P` 0.806 · 1.031 · 1.227 · 1.399 ↔ 인쇄 0.586 · 0.865 · 1.116 · 1.333 · 역산 지수 0.49–0.50) · 본문 "maximum … ψ_LSCF = 0.55" 도 `√P` 쪽(인쇄 `P` 면 0.56–0.57) | pp. 1638–1639 · 1645 ↔ 그림 6 · 8 | 문턱 바로 위 연결 확률이 인쇄식으로 그림의 ≈½–⅔(ψ 0.33: 0.287 ↔ 0.536). 어느 쪽이 [31] 인지는 미열람(G2) |
| **D2** | ★★ 식 (24) 분자 `n^V_LSCFk Z_LSCFk,YSZℓ` ↔ 좌변 `Z_LSCF,LSCF` · 본문 "coordination numbers among the same-sized LSCF_k particles … and … neighboring LSCF particles" | p. 1646 | 인쇄식대로면 문턱이 거꾸로(ψ > 0.706 에서 `P = 0`) — 그림은 `LSCFℓ` 판 |
| **D3** | ★★ 그림 7 캡션 "percolated … surface electrochemical reaction site" · 명명법 "exposed surface sites of the **percolated** LSCF particles" · 식 (9) · (26) 의 `P^e P^i` ↔ 그림은 `P` 없이(`[재현]` ≤0.005) — ψ 0.29(문턱 아래)에서 0.528 | p. 1649 ↔ 그림 7 | 노출 표면 자리가 전자 퍼콜레이션 문턱 아래에서도 0 이 아니다 |
| **D4** | ★★ 그림 9 · 10 이름표 ↔ 곡선 값: `[재현]` 값은 색 규약(적 (1, 0, 0) · 청 (1, 0.6, 0.6) · 흑 (2.5, 0, 0) · 자홍 (2.5, 0.6, 0.6) — 그림 6 · 7 · 8 · 11)으로 30 여 마커 ±0.03 재현 · 그림 9 이름표는 ϑ̃ 를 뒤바꾸고 그림 10 은 다르게 섞였다 · 본문 "A larger σ̃_YSZ-YSZ can be obtained by using broader particle size distribution materials" 는 이름표를 따른다(재현은 −12 %) | p. 1651 ↔ 그림 9 · 10 | `a` 의 식이 인쇄되지 않았다는 조건(G5) 위 — 그러나 한 `a` 로 네 그림 · 넷 곡선이 모두 맞는다 |
| **D5** | ★ 그림 11 본문 "for … ψ_LSCF = 0.5, σ̃_LSCF-YSZ decreases with increasing … ϑ̃_LSCF and ϑ̃_YSZ" ↔ 같은 그림 크기비 2.5 쌍: 폭 0.6 이 더 높다(`[재현]` 2.242 ↔ 1.504) | p. 1652 | 크기비 1 에서만 선다 |
| **D6** | ★★ 계산 예 "r̄_YSZ = 200 nm and r̄_YSZ = 40 nm" → "≈9.3 × 10¹³ m⁻²" ↔ `[재현]` (2.5, 0.6, 0.6) · r̄_LSCF 40 nm(곧 r̄_YSZ 100 nm) = 9.56 × 10¹³ · 크기비 5 면 5.1 × 10¹³ · 크기비 0.2 면 0 | p. 1649 | "200 nm" 는 지름이거나 오기 · 기호 둘 다 YSZ |
| **D7** | ★ `L^ter` = "the number of particle layers L/r_YSZ" × δ ↔ 식 (16) 의 앞계수 2 는 L/(2r) 층일 때(`[재현]`) | p. 1643 | 식이 맞고 산문이 틀렸다(또는 반대) — 값에는 ×2 |
| **D8** | ★ 그림 8 캡션 `λ̃^V_TPB,per` ↔ 축 `λ̃^S_TPB,per` · 본문 "TPB **area** per unit electrolyte surface area" ↔ Assumption 2(길이 · m⁻¹) | p. 1650 | 기호 · 낱말 |
| **D9** | ★ 3.2.4 제목 "The Effective **Electric** Conductivity" ↔ 내용은 이온 전도도 식만 · 전자는 "would equal the … intra-particle conductivity" 한 문장 | pp. 1642–1644 | 전자 전도도 식 0(G7) |
| **D10** | ★ 참고문헌 [4] ↔ [26] 같은 서지(Chen J. … Jian 2010 *JPS* 195, 5201) | pp. 1654–1655 | 중복 |
| **D11** | ★ [28] Lu L., Chen D., … 2010 *JPCC* 114, 18435("surface-plasmon-mediated emission from CdSe nanocrystals")를 "composite cathode with a mixed … conductor … great performance [23–28]" 에 인용 | p. 1635 | 제목 기준 무관(`[해석]` — 원문 미열람) · 공저자 겹침 |
| **D12** | ★ "ψ_LSCF should be chosen to fall within the range of 0.3 to 1 … both percolated electron and ion conducting paths can be formed" ↔ 크기비 2.5 의 문턱은 0.143(그림 6 · 8) | p. 1648 | 크기비 1 조건을 떼고 일반화 |
| **D13** | ★ 그림 1 "seven distinct layers: (a) … (f)" — 글자 여섯 · 그림의 맨 아래 판은 이름 없음 | p. 1634 | 사소 |
| **D14** | ★ 그림 11 y 라벨 아래첨자 "LSCF-YS"(잘림) · x 축 1.1 까지(다른 그림 1.0) | 그림 11 | 원 래스터 그대로 — 사소 |
| **D15** | ★★ "sufficiently accurate in the prediction of electrode properties" · "carefully checked" ↔ 이 편 안의 대조 · 오차 0 | p. 1636 · 1646 | 검증 위임(G1) |
| **D16** | ★ 결론 "the effects of … **the porosity** … on the effective properties" ↔ 좌표수 · 확률은 `φ_g` 무관(`Z̄ = 6`) · 무차원 곡선은 `φ_g` 약분 · `φ_g` 가 남는 곳은 수력 반경과 차원 앞계수뿐 | p. 1653 | 공극률 효과는 스케일 인자 |
| **D17** | ★ 그림 4(a) 의 `θ` 가 YSZ(큰 쪽) 중심에 표시 ↔ `r_c = min(r) sin θ`(작은 쪽 각) | 그림 4 ↔ p. 1640 | 사소 |

# 이 편이 우리 프로젝트에 주는 것 (정리)

1. ★★★ **22호가 기댄 "percolation theory" 의 실체는 좌표수 평균장 해석식이고, 22호 명제는 방향만 받는다** — 식으로 `[재현]` 하면 CAM 이 SE 보다 커질 때 연결 분율이 준다. 그러나 22호 조성 · 입도로
   세 점을 동시에 맞추는 SE 입도는 없고(M ≈ L 평탄이 함수족 밖), 측정을 상한으로 읽으면 M 의 불활성은 거의 전부 전자 밖이다. [[composite-cathode-percolation-utilization]] 68호 절.
2. ★★★ **해석식을 쓰기 전에 그림으로 재현한다** — 인쇄식 `P` ↔ 그림 `√P` · 식 (24) 오기 · 그림 7 `P` 미적용. 이 편의 식을 합성 truth 의 `θ₀` 사전으로 쓸 때 **두 `P` 꼴을 폭으로** 둔다(문턱
   근처 ×2 차).
3. ★★★ **크기 효과는 비다** — `ρ = r₃₂(SE)/r₃₂(CAM)` · 고상 ψ 만으로 `P^e` 가 정해지고, 1 → 0 전이가 ×5.77 안에서 끝난다. **SE 입도를 모르면 한 크기의 예측은 0–100 %** — CAM 입도 스윕
   실험(22호 · 3차 묶음 파일 39 Shi 2019 — 미흡수)과 대질하려면 **SE 입도(가능하면 복합체 안 SE 영역 크기)를 같이 적어야** 한다.
4. ★★ **SOFC 식에는 용량 칸이 없다** — `1 − P^e` 가 반응 자리에만 들어간다. ASSB 로 옮기면 `P^e` 는 `ε_p` 자리(= `LAM_PE` 와 같은 파라미터)로, 부분 피복 `φ_cov = Z sin²θ/4` 는 `A_eff`
   자리(`j₀` 와 곱)로 간다 — 합성 truth R1 · R7 의 두 변수가 이 식 안에 이미 따로 있다([[assb-synthetic-truth-contact-loss-requirements]]). 둘 다 정적이다.
5. ★★ **01호와 이 편은 같은 양의 두 계산이고, 크기 효과의 기구가 다르다** — 01호 `p_c(d)` 의 d 의존이 이산화에서 올 수 있다는 가설(`[해석]`) · 둘 다 22호 L 을 과대 예측 — 강체 무작위 충전의
   공통 가정이 압착 복합체의 연결을 과소 평가하는 쪽.
6. ★ **평균장 `P` 에는 폭이 없다** — 01호의 이봉(±20 %p)을 지운다. DEM 라벨 계획의 "폭을 붙여라" 규율은 해석식 쪽에서 오히려 더 필요하다.
7. `[해석]` 우리 주 프로젝트(액체셀 PyBaMM)와의 접점: 액체셀에서는 전해질이 입자 둘레를 다 적셔 퍼콜레이션이 전자 쪽(탄소)에만 걸린다 — 이 편의 "MIEC 가 두 망에 동시에" 구조는 우리 truth 에
   없다. 우리 쪽 수치는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본이다 — 여기서 비교하지 않는다.

# 후속 후보 (원전 우선)

참고문헌 39 편 중 우리 축(Q1 · `θ₀` · 01호 관계)에 닿는 것만. **전지 논문 0 · 셀 열화 식별성 원전 0.**

| 서지 | ref | 왜 | 축 | 우선 |
|---|---|---|---|---|
| **Bertei, Nicolella 2011 *Powder Technol.* 213, 100–108** — "A comparative study and an extended theory of percolation for random packings of rigid spheres" | [31] | 식 (5) `P(Z)` 원전 — **인쇄식 ↔ 그림 `√P` 차의 판정처** · 해석식 ↔ 시뮬레이션 오차 크기(비교 연구) · 원장 0 | Q1 · Q3 | ★ |
| Bertei, Choi, Pharoah, Nicolella 2012 *Powder Technol.* 231, 44–53 — "Percolating behavior of sintered random packings of spheres" | [39] | 목 · 소결이 문턱을 옮기는 크기 — ASSB 압착 접촉의 대리 변수 후보 · 원장 0 | Q1 · Q6 | ☆ |
| Chen D., Lu, Li, Yu, Kong, Zhu 2011 *J. Power Sources* 196, 3178–3185 | [17] | 이 편이 위임한 검증(무작위 충전 재구성 대조)의 자리 · 표 1 원전 · 원장 0 | Q3 | ☆ |
| Suzuki, Oshima 1983 *Powder Technol.* 35, 159–166 · 1985 44, 213–218 | [15] · [30] | 좌표수 식 · `Z̄ = 6` 원전 — 공극률 · 압착에 따른 `Z̄` 가 있는가 · 원장 0 | Q1 | ☆ |
| Bouvard, Lange 1991 *Acta Metall. Mater.* 39, 3083–3090 | [16] | 이성분 분말의 퍼콜레이션 ↔ 좌표수 원형 · 원장 0 | Q1 | ☆ |
| Kenney, Valdmanis, Baker, Pharoah, Karan 2009 *J. Power Sources* 189, 1051–1059 | [9] | 무작위 충전 재구성(시뮬레이션 계열)의 SOFC 판 — 01 · 02호와 같은 방법 계열 · 원장 0 | Q1 | ☆ |

# 이 digest 가 주장하지 않는 것

- **22호 명제("M · L 의 불활성은 전자 비연결")가 틀렸다고 하지 않는다** — 이 편의 식으로 정량 재현되지 않는다는 것, 그리고 상한 읽기에서는 반대 배정이 나온다는 것까지다. 식 쪽 가정(`Z̄ = 6` ·
  강체구 · 무한계 · d₅₀ = Sauter)이 22호 복합체와 다르다.
- **SE 입도가 8.9–11.6 µm 라고 하지 않는다** — 그것은 "상한 읽기에서 모형과 모순 없는 조건" 이지 예측이 아니다. 22호 SE 입도는 인쇄되지 않았다.
- **√P 가 옳은 식이라고 하지 않는다** — 그림이 그 꼴로 계산됐다는 `[재현]` 까지다. [31] 은 열람하지 않았다.
- **그림 9 · 10 의 이름표가 틀렸다고 단정하지 않는다** — `a` 의 식이 인쇄되지 않았다(G5); 한 `a` 로 모든 곡선이 색 규약대로 맞는다는 것까지다.
- **01호 `p_c(d)` 가 이산화 인공물이라고 하지 않는다** — 01호 digest 의 배치 절차에서 나온 가설이고 검증하지 않았다.
- **ASSB 에 `A_eff = φ_cov · P^e · P^i` 가 성립한다고 하지 않는다** — 이 편의 Assumption 1 식을 P2D 의 자리에 맞춰 본 대수다.
- 이 편은 SOFC 이론 편이다 — ASSB 측정 · 전지 수치와 한 표에 놓은 것은 전부 `[재현]`(식 대입) 또는 `[해석]` 이다.
- 우리 파이프라인(`degradation-degeneracy/`) 수치와 비교하지 않는다 — 우리 쪽 수치는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본이다.
- 인용 원전([31] · [39] · [17] · [11] · [15] · [30] · [16] · [12] · [9])은 열람하지 않았다. 22호 원문 PDF 는 이 세션에 없어 22호 digest 로 대조했다.
