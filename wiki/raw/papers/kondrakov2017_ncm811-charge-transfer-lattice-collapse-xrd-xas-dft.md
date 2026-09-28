---
title: "Kondrakov A.O., Geßwein H., Galdina K., de Biasi L., Meded V., Filatova E.O., Schumacher G., Wenzel W., Hartmann P., Brezesinski T., Janek J. 2017 — Charge-Transfer-Induced Lattice Collapse in Ni-Rich NCM Cathode Materials during Delithiation (J. Phys. Chem. C 121, 24381–24388)"
source_url: local-upload/29._Charge-transfer-induced_lattice_collapse_in_Ni-rich_NCM_cathode_materials_during_delithiation.pdf + 29._Sup_Charge-transfer-induced_lattice_collapse_in_Ni-rich_NCM_cathode_materials_during_delithiation.pdf
source_url_note: "본문 PDF 8 쪽(ACS · 그림 5 · 표 2 · 참고문헌 54 · 초록 그래픽 1) + SI PDF 13 쪽(그림 S1–S8 · 부록 1 VASP POSCAR 넷). 본문은 출판사 조판 파일(Arbortext · Distiller, 생성 2017-11-01)에 2026-09-28 내려받기 표지(iTextSharp)가 찍힌 것이고, SI 는 Word 원고를 activePDF DocConverter 가 변환한 PDF(생성 2017-09-07 = 수정본 접수일)에 같은 날 내려받기 표지가 찍힌 것 — 66호 SI(저자 Word 2010 원본) · 65호 SI(수령일 변환본)와 다르다. 그림 자동 14 장(본문 5 · SI 8 · 표 1 — 라벨 어긋남 0, fig_S7 은 (d) 아래가 잘림 · tab_2 는 본문 과대 포함) + 수동 3(Fig. S7 전체 · Table 1 · 초록 그래픽) = 17 항목 전부 열어 봤다. 수치는 PDF 원본 래스터 · SI 600 dpi 렌더 픽셀 판독, 표 · POSCAR 는 텍스트 층 정본. 3차 묶음 파일 29(2차 큐 번호와 별개) — 원장 행 '★ Kondrakov 외 2017 24381'(66호가 묶음 행에서 분리); 22호 ref 21 · 66호 [19]. 파일 31(3286)과 다른 편. 액체 반쪽전지 논문 — ASSB 아님. 원자료는 커밋하지 않는다."
source_doi: 10.1021/acs.jpcc.7b06598
source_license: "© 2017 American Chemical Society — 구독 논문(오픈액세스 표시 없음). 이 digest 는 인용 · 요약 · 재현 계산만 담는다"
pdf_sha256: fe186a38e9e9e123bc146c61d1ffc08fa5abf51b8d3126b4e05ba1d36b9e7522
si_sha256: 757dfe916f3deba285ad5000992a2fd8685325657ef7ca1399d9fc0587532a06
ingested: 2026-09-28
sha256: c29d711675fcb7b7ec3601771cb390cc95e6b17f5f0a01d2219d30f064e61109
---
# 수집 목적

`assb` 섹션 **67호** — **3차 묶음 파일 29**(3차 묶음 아홉째 편). 3차 묶음의 파일 번호는 2차 묶음 "큐 N" 번호(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-d, 큐 1–59)와
**별개**다 — 이 편은 "큐 29" 가 아니다. ⚠ **ASSB 논문이 아니다** — 액체 전해질 · Li 금속 상대극(코인 · 파우치)에서 **NCM811 한 조성**의 격자(operando XRD) · 전자 구조(operando hXAS ·
ex situ sXAS)를 재고, 기구를 **LiₓNiO₂ 모형 DFT** 로 해석한 편이다. 닻은 `questions/assb-contact-loss-vs-lampe.md`.

들어온 경로: 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 — 66호가 두 편 묶음 행에서 분리한 행) "★ **Kondrakov 외 2017** — *J. Phys. Chem. C* 121, 24381 (22호 ref 21 · 66호 [19]) |
지목 22 · 66 | **2** | Q8·Q2 | **`c` 붕괴 기구의 원전 후보** — 66호가 'interslab 수축 → `c` 감소' 를 [19] 로 위임 · 22호 digest 'Ni–O 전하이동 (refs 20, 21)' · … · 교정 `x` 축 규약(첫 사이클인가 · δ₀)도
확인할 곳". ⚠ 파일 31 = Kondrakov *JPCC* 121, **3286**(원장 ★★★ "NCM811 부피 수축 %의 원전", 지목 23 · 62 · 66)은 **다른 논문**이다 — 이 편은 3286 을 **[5]** 로 **여덟 번** 인용한다
(§인용 대조 — 무엇으로 인용했는지만 적어 파일 31 에 넘긴다; 3286 의 수치는 여기서 다루지 않는다).

지목 digest 가 이 편에 매단 명제(위키 전체를 `24381` · `Kondrakov` · `lattice collapse` · `Galdina` 로 grep — 이 편을 인용한 digest 는 **22호 · 66호 둘**이다. 다른 "Kondrakov" 는
3286(23호 ref 41 · 62호 [31] · 66호 [15])과 Koerver 2018 *EES*(27호 [40], 공저자)다. 22호 원문 PDF 는 이 세션에 없다 — 22호 digest 와 22호 그림 폴더(`fig_S3.png` — 이번에 열어 봤다)로 대조했다.
66호 원문 PDF 는 이 세션에 있어 [19] 의 서지와 표 S1 을 다시 읽었다 — 읽기만):

| 지목 | 인용 번호 | 매단 명제 (digest 자리) |
|---|---|---|
| **22호** Strauss 2018 | ref 21 | ① §2-4(:167–168) `[인쇄]`(22호) 교정 서술의 요약 "c 는 **x ≈ 0.5 까지 증가 후 급감**(**Ni–O 전하이동, refs 20, 21**), 단위포 부피 단조 감소(Fig. S4)" ② 후속 표(:576) "★ 7 — de Biasi 2017 (ref 20 / SI ref 4) · Kondrakov 2017 24381 (ref 21) \| **a·c–x 교정의 원전(c 최대의 기구)** \| Q8" |
| **66호** de Biasi 2017 | [19] | ① 서론 `[인쇄]`(66호) "charging NCM cathode materials to higher states of charge (SOC) is accompanied by more pronounced changes in lattice structure.10,13,19" ② `[인쇄]`(66호) "When most of the lithium is removed, a contraction of the interslab distance is observed and with that a decrease in lattice parameter c.19" — 66호는 "Ni–O" 를 0 회 쓰고 붕괴 기구를 이 편으로 위임했다 |

**59–66호 · 29 · 38호 SI 보강을 이어받는다.** 66호는 격자 ↔ `x` 교정의 **축이 통과 전하**(θ_ref = 1 · 부반응 0 · 전처리 결손 = 양극 Li 손실)임을 인쇄로 보였고, 같은 연구망 두 NCM622
교정(22호 첫 사이클 ↔ 66호 넷째 충전)이 같은 격자를 **x 로 ≈0.067 가로 이동**해 읽는다는 것을 `[재현]` 했다 — 원인(δ₀ 규약 · 전처리 · 사이클 번호 · 로트)은 가르지 못했다. 개념
[[nmc-lattice-li-content-calibration]] 이 그 축 규약을 모은다(유지 여부는 사용자 확인 대기 — 이 편은 **덧붙이기만** 한다). 23호는 SEM 틈 폭에서 NCM811 요구 `ΔV/V ≈3–20 %`(중앙 8–10 %)를
역산했고(원전 값 0 — 23호 G1), 62호는 NCM "volume changes of nearly 6%"[31 = 3286] 를 방향 없이 인쇄했다.

이 digest 의 일 (지시):

1. **(a) `c` 붕괴의 기구** — 무엇으로 보이는가(회절 · 분광 · 계산 중 무엇이 측정이고 무엇이 계산인가) · "Ni–O 전하이동" 이 원문의 낱말로 인쇄되는가 · 붕괴가 시작되는 `x` · 전압 · 조성 · 22호 :168 명제가 서는지.
2. **(b) `x(Li)` 축 규약** — 통과 전하 · 첫 사이클인가 · δ₀ · 화학 분석 — 66호 표 S1 · 22호 교정과 같은 조성이 있으면 같은 격자에서 비교해 66호 x 이동 ≈0.067 의 원인을 가를 수 있는가(가르면 `[재현]`, 못 가르면 이유).
3. **(c) Q8 · 부피** — 조성 · 전압별 `ΔV/V` · `Δc` · `Δa` 를 66호 표 S1 · 23호 요구치 · 62호 "nearly 6%" 와 **전압 · 기준(원형 / 사이클 첫 점)** 을 맞춰 대조(3286 의 값은 파일 31).
4. **(d) Q1 · 곱 축퇴** — 사이클 축 측정(`θ(N)` · 활성 질량 · 균열 · LAM) · 63–65호 `R`·`C` 1단계 틀 — 없으면 "해당 없음" 과 이유.
5. **(e) 셀 사양 · 회절 · 분광 셀 설계** — Q5 는 상대극에 따라.
6. Q1–Q8 · 채움표 67호 행 · 곱 축퇴 처방 쉰 번째 적용 · 보류 (가)(나)(다)(아)(자)(차)(타) 표시(결정 안 함).

> ⚠ **형식 — *J. Phys. Chem. C* Article 8 쪽(그림 5 · 표 2 · 참고문헌 54 · 초록 그래픽 1) + SI 13 쪽(그림 S1–S8 · 부록 1 = VASP POSCAR 넷). 1차 측정 있음 — NCM811 코인 반쪽
> 컷오프 여섯(4.1–4.6 V) × 50 사이클 · operando XRD(파우치 · 전처리 셀의 한 충전) · operando hXAS(Ni · Co · Mn K) · ex situ sXAS(O K · TM L, 표본 여덟) · NCM811/흑연 150 사이클(S1).
> 계산 — DFT(VASP · PBE · Grimme, 모형 LiₓNiO₂, x = 1 · 0.75 · 0.5 · 0.25 네 점, Bader). ASSB · EIS · 압력 · 기준극 · 사후 단면 0.**
> **반복: 셀 수 인쇄 0(어느 시험에도) · 오차 막대 0 · 괄호는 Rietveld esd · Bader 전하는 O 소수 한 자리 · Ni 두 자리.**
> 그림은 본문 · SI 모두 래스터(SI 는 Word 삽입 그림을 띠로 나눈 것) — `[도표]` 값은 PDF 원본 래스터(또는 SI 600 dpi 렌더)에서 축 눈금 라벨 중심에 선형 적합한 뒤 곡선 · 마커를 읽었다
> (§픽셀 판독). 표 값은 PDF 텍스트 층이 정본이고, SI POSCAR 좌표도 텍스트 층에서 파싱했다(§(a') — 표 2 대조).
>
> 표기: `[인쇄]` 본문 · 캡션 · SI 명시 · `[도표]` 그림에서만 읽은 값(`figure-read ≈`) · `[재현]` 지면의 숫자로 우리가 계산 · 대조한 값 · `[해석]` 우리 해석.
> `[해석]` 표시 없는 문장은 원문이 실제로 말한 것.

# 판정 먼저

| 물음 | 판정 | 한 줄 근거 |
|---|---|---|
| **(a) `c` 붕괴 — 현상** | ✅ **측정(operando XRD) — NCM811 한 조성** | `[인쇄]` `V` 101.38(1) → 94.26(2) Å³(x 1.00 → 0.25) · `c` 14.249(1) → 14.469(1)(x 0.6) → 13.732(2) · `a` 2.8661(1) → 2.8153(1) · "the significant drop in c lattice parameter and the resulting unit cell volume changes are caused by the simultaneous decrease in both slab heights at x(Li) < 0.5 (more rigorously at x(Li) < 0.45)". `[재현]` 전체 `ΔV/V` **−7.02 %** · ΔV 의 **76.8 %** 가 x ≤0.5(본문 ">70%") |
| **(a) 기구 — 무엇이 측정이고 무엇이 계산인가** | ⚠ **현상 · Ni 산화 · O 2p 혼성은 측정, "x < 0.5 에서 O → Ni 전하이동" 의 시점은 계산** | 측정: 슬랩 높이(XRD, `z_O` 첫값 = 원형 중성자) · Ni K 가장자리 연속 이동(hXAS — `[인쇄]` "nickel is continuously oxidized over the whole x(Li) range") · O K 전단 A1 증가(sXAS, TEY ≈100 Å · 손 연마 표면 — `[인쇄]` "nearly linearly"). 계산: LiₓNiO₂ **PBE(+U 0 회) 네 점**의 Bader — Ni +1.38 → +1.47(x 0.5) → +1.43(x 0.25), `[인쇄]` "break of the positive trend when x(Li) < 0.5 … indicative of charge transfer from oxygen to nickel". **전하 쪽 꺾임을 보이는 채널은 이 계산 하나** — 전자 구조 측정 둘(Ni K · O K)은 x 0.5 에서 꺾이지 않는다(`[도표]` Ni K 반높이 이동 x 당 +1.4 → +4.5 → +4.4 eV, 줄지 않는다) |
| **(a) "Ni–O 전하이동" 이 인쇄되는가** | ✅ **실질은 인쇄 · 낱말 "Ni–O" 는 0 회** | `[인쇄]` 초록 "charge transfer between O 2p and partially filled Ni eg orbitals (resulting in decrease of oxygen−oxygen repulsion)" · 본문 "charge transfer from oxygen to nickel" · 결론 "electronic mixing in nickel−oxygen states". `Ni−O`/`Ni-O` **0** · `nickel−oxygen` 1 · `charge transfer` 7 |
| **(a) 붕괴 시작 — x · 전압 · 조성** | **이 편 축 x ≈0.45–0.6 · ≈4.0–4.2 V · NCM811 한 조성(계산은 LiNiO₂)** | `[도표]` `c` 최대 14.469 @ x ≈0.555(±0.005 Å 띠 0.515–0.577; 본문 "at x(Li) = 0.6") · `h_Li-O` 최대 x ≈0.435–0.47 · `[인쇄]` dc/dE 극값 4.2 V. `[재현]`(S2 전압–scan + 선형 x) `c` 최대 ≈3.99–4.01 V · x 0.5 ≈4.06 V · x 0.45 ≈4.13–4.16 V · 4.2 V ≈ x 0.40–0.42 — 결론의 "E > 4.2 V vs Li+/Li and x(Li) < 0.5" 는 한 경계가 아니다(D12) |
| **(a') DFT 재현 — SI POSCAR ↔ 표 2** | ❌ **x = 0.25 행이 SI 기하로 재현되지 않는다 · 그 기하는 O–O 쌍 · Ni 이동을 품는다** | `[재현]` POSCAR(텍스트 층) → x = 1 · 0.75 · 0.5 는 표 2 DFT `a` · `c` · `V` 를 ≤0.36 % 로 재현 · **x = 0.25: `V` 98.63 ↔ 표 93.39 Å³(+5.6 %) · `c` 13.62–13.64 ↔ 13.37 · `a` 2.886/2.916 ↔ 2.840**. 그 기하에 **O–O 1.331 Å 두 쌍(O 24 중 4)** · **Ni 둘이 Li 슬랩 안(z 0.710, 4 배위)** — 본문 · 캡션 서술 0(`dimer` · `peroxo` · `migrat` 0 회). S7(d) 그림도 그 모양 · S8(d) DOS 에 ≈−9 eV O 상태 · t2g–eg 틈 닫힘(`[도표]`) ↔ 캡션 "Only slight changes in DOS" |
| **22호 :168 명제** | ✅ **기구 서술은 선다 · ⚠ "x ≈ 0.5" 는 축 규약 위의 값** | 세 교정이 `c` 최대를 x **0.45(66호 NCM811) · ≈0.5(22호 NCM622) · ≈0.555–0.6(이 편 NCM811)** 에 놓는다 — 전압으로는 NCM811 두 교정 모두 **≈3.99–4.0 V**(`[재현]`) |
| **(b) `x(Li)` 축** | ★★★ **통과 전하 · 전처리 셀 · 그 충전 첫 점 = 1.00(결손을 빼지 않았다) · 첫 사이클은 일부러 피했다 · 화학 분석 0** | `[인쇄]` "discuss them with respect to lithium content (estimated from current and charging time)" · "In our previous work, we found that high-Ni NCMs suffer from significant first cycle irreversibilities (up to 14%), resulting in partial active lithium loss and delayed change in lattice parameters in the initial charge cycle.5 Thus, for better correlation of the lattice parameter changes with lithium content, precycled cells (at 25 °C and C/10 between 3.0 and 4.3 V) were used here for XRD" · 표 2 XRD 행 **x(Li) = 1.00** = 전처리 셀 충전 첫 점(Fig. 2b 곡선이 x 1.0 에서 시작). 전처리 횟수 · CE · 결손 배정 미인쇄. hXAS 는 x 0.84 → 0.22(같은 조건이라는데 범위가 다르다 — D8) |
| **(b) 같은 연구망 세 규약** | **22호 첫 충전 · x₀ 1.02 / 66호 넷째 충전 · 1.02 − 전처리 CE 결손(NCM811 0.90 · NCM622 0.93) / 이 편 전처리 셀 충전 · 1.00** | 셋 다 전하 계수 · 화학 분석 0. 이 편은 22호가 쓴 **첫 사이클 교정을 피할 이유**를 인쇄한다(첫 사이클 격자 "delayed change") |
| **(b) 66호 x 이동 ≈0.067(NCM622) 의 원인** | ❌ **못 가른다 — 이 편은 NCM811 뿐 · 첫 사이클 교정 없음 · 전처리 횟수 미인쇄**. 대신 **NCM811 쌍(이 편 ↔ 66호)에서 규약 항을 전압 맞춤으로 뗐다**(`[재현]`) | 두 교정 모두 전처리 셀이라 규약 차는 1.00 − 0.90 = **0.10**: **전압 맞춤 이동 +0.096…+0.112**(66호 δ ≤0.65 · 정전압 전하 δ_CV 0; 0.02 면 +0.103…+0.132) ≈ 0.10 ✓ · **격자 맞춤 이동 +0.123…+0.133**(붕괴 구간 δ ≤0.35 — `V` · `c` 일치) ⇒ **시편 항 0 … +0.03**(1 h 정전압 전하 미인쇄 — δ_CV 0 이면 +0.015…+0.03, 0.02 면 ≈0); 충전 초반은 채널마다 +0.06(`c`) · +0.12(`a`) · +0.16…+0.19(`V`)로 갈린다. **NCM622 쌍(22호 첫 충전 ↔ 66호)에 같은 방법을 대면 전압 맞춤 이동이 +0.157 → +0.033 으로 x 따라 변한다** — 첫 충전 전압 곡선 자체가 다르다(이 편이 이름 붙인 첫 사이클 교란) ⇒ 규약 항을 못 뗀다 |
| **(c) Q8 · `ΔV/V`** | **층 하나 — NCM811 한 조성 · 기준 = 전처리 셀 충전 첫 점(원형 격자 인쇄 0)** | `[재현]` 4.6 V + 1 h(x 0.25) **−7.02 %**(표 2) · 4.3 V **−4.9…−5.4 %** · 4.2 V −2.5…−2.8 % · **−6 % ≈ x 0.29 ≈4.36–4.44 V**. 66호 NCM811 −7.35 %(첫 행) / −6.95 %(원형) · −6 % ≈4.42 V · 62호 "nearly 6%" 와 같은 자릿수 · 23호 중앙 8–10 % 는 이 편 범위 밖 · **23호 첫 충전 176 mAh g⁻¹ → 이 편 축 −4.0 % ↔ 66호 축 −1.3…−1.7 %**(축 규약만으로 ×2.4–3) |
| **(d) Q1** | **없다 — `θ(N)` 0/67** | 사이클 축은 용량 유지율(Fig. 1a 컷오프 여섯 × 50 · S1 흑연 완전지 150). `[인쇄]` "the capacity fading is virtually enhanced at such conditions because overpotentials arising during cycling, e.g., due to material fracture, lower the actual cell voltage" — 겉보기 감쇠의 `η` 몫을 저자가 이름 붙인다(측정 0) |
| **(d) 곱 축퇴 · 1단계 `R`·`C`** | **해당 없음** | EIS 0(`impedance` · `EIS` 0 회) · 면적 채널 0 · 액체 반쪽 · 사이클 축 격자 0. 처방 표 66호 경고 행에 **규약 항 ↔ 시편 항** 한 줄을 보탠다(§곱 축퇴) |
| **(e) 셀** | 인쇄 · 미인쇄가 섞인다 · **파우치 사양은 [5] 로 위임** | 코인: BASF NCM811 전극(94 wt%) · GF/D · Li 금속(Rockwood) · 1 M LiPF₆ **EC:DMC 3:7(무게)** 250 µL · 25 °C · MACCOR. operando: 파우치 · Mo Kα₁,₂ · 2θ 5–37° · "every 150 s"(`[재현]` S2 쌍축은 **175.5 s/scan** — D7) · C/20 · 충전 끝 1 h 정전압. hXAS: P65 · 투과 · "2 mm polyimide windows". sXAS: RGBL(BESSY II) · TEY · DMC 세척 · **손 연마**. 적재 · 두께 · 전극 크기 · 파우치 전해질 · 1C 정의 **0** |
| **Q5** | **해당 없음** | Li 금속 상대극 · 기준극 0 |
| **Q4** | **0/67 — 쉰아홉 번째 성질** | "전자 구조 측정 둘(Ni K · O K)이 x 0.5 에서 꺾임을 보이지 않는 자리에서 격자 붕괴의 원인과 시점을 LiNiO₂ PBE 네 점의 Bader 꺾임 하나로 정하고, 그 계산의 절대 조성을 전하로 센 상대 축(전처리 셀 충전 첫 점 = 1.00)과 같은 눈금에 놓았으며, SI 기하가 표의 x = 0.25 행을 재현하지 않는 것(O–O 쌍 · Ni 이동)을 적지 않았다" |
| **곱 축퇴 처방 쉰 번째** | **적용 불가 — 1단계 입력 없음 · 경고 행 보강 하나** | §곱 축퇴 |
| **보류 (가)(나)(다)(아)(자)(차)(타)** | **근거 0 — 결정 안 함** | (나)에 정성 메모 하나(§보류) |

# 서지

| 항목 | 값 |
|---|---|
| 제목 | Charge-Transfer-Induced Lattice Collapse in Ni-Rich NCM Cathode Materials during Delithiation |
| 저자 (11) | **Aleksandr O. Kondrakov**\*, Holger Geßwein, Kristina Galdina, Lea de Biasi, Velimir Meded, Elena O. Filatova, Gerhard Schumacher, Wolfgang Wenzel, Pascal Hartmann, **Torsten Brezesinski**\*, Jürgen Janek — 교신 둘(\*). ⚠ 66호 참고문헌 [19] 는 이 편을 **저자 열 명**(Janek 빠짐)으로 인쇄했다(66호 PDF 텍스트 층 — 읽기만) |
| 소속 | KIT Battery and Electrochemistry Laboratory(Kondrakov · de Biasi · Hartmann · Brezesinski · Janek) · KIT Institute of Nanotechnology(Meded · Wenzel) · KIT Institute for Applied Materials(Geßwein) · **BASF SE**(Kondrakov · Hartmann) · Helmholtz Institute Ulm(Geßwein) · St. Petersburg State University(Galdina · Filatova) · Helmholtz-Zentrum Berlin(Schumacher) · JLU Giessen(Janek) |
| 서지 | *J. Phys. Chem. C* **2017**, 121, 24381−24388 · doi `10.1021/acs.jpcc.7b06598` · ACS Article · "© 2017 American Chemical Society" — 구독 논문(오픈액세스 표시 0); 이 digest 는 인용 · 요약 · 재현 계산만 담는다. 호 44 는 내려받기 표지의 경로("…/121/44/24381/…")에서 |
| 일정 | 접수 2017-07-05 · 수정본 2017-09-07 · 게재 2017-10-11 — `[재현]` 접수 → 게재 **98 일**. 66호(게재 2017-10-31)보다 20 일 먼저 — 66호가 이 편을 [19] 로 인용했고, 이 편은 66호 · 22호(2018)를 인용하지 않는다(시점) |
| 자금 · COI | `[인쇄]` "This study is part of the projects being funded within the BASF International Network for Batteries and Electrochemistry." · PETRA III(DESY) · HZB 빔타임 · "The authors declare no competing financial interest." — 저자 둘 BASF SE 소속 · 전극 · 전해질 BASF 제공(`[인쇄]`) |
| 분량 | 본문 PDF 8 쪽(4,164,545 B · 625 × 818 pt) — 그림 **5** · 표 **2** · 식 0(인라인 `V = a²c sin π/3` 하나) · 참고문헌 **54** · 초록 그래픽 1(래스터 869 × 562) |
| SI | PDF 13 쪽(1,493,716 B · US Letter 612 × 792 pt) — 그림 **S1–S8** · 부록 1 = VASP POSCAR 넷(x = 1 · 0.75 · 0.50 · 0.25 — SI 7–13 쪽) · 표 0 |
| PDF 메타데이터 — 본문 | title "jp7b06598 1..8" · creator "Arbortext Advanced Print Publisher 10.0.1465/W Unicode" · producer "Acrobat Distiller 8.1.0 (Windows); modified using iTextSharp.LGPLv2.Core 3.7.4.0" · PDF 1.3 · 생성 **2017-11-01 14:18:13 −04:00** · 수정 **2026-09-28 02:33:36 +00:00** · 매 쪽 발 "Downloaded from pubs.acs.org/jpccck/article-pdf/121/44/24381/7676190/jp7b06598.pdf by HANYANG UNIV user on 28 September 2026" ⇒ 출판사 조판 파일(생성일은 게재 3 주 뒤)에 내려받기 날 표지를 찍은 것으로 읽힌다(`[해석]` — 메타데이터가 말하는 만큼; 66호 본문과 같은 형태) |
| PDF 메타데이터 — SI | title "**Microsoft Word - 2517282_File000001_43888066.docx**" · author " "(공백 한 칸) · creator "**DocConverter http://www.activepdf.com**" · producer "activePDF DocConverter; modified using iTextSharp.LGPLv2.Core 3.7.4.0" · PDF 1.5 · 생성 **2017-09-07 16:59:02 −05:00** · 수정 **2026-09-28 02:33:50 +00:00**(본문 수정 14 초 뒤) · 매 쪽 발 "Downloaded from pubs.acs.org/jpccck/article-supplement/759146/pdf/jp7b06598_si_001/ by HANYANG UNIV user on 28 September 2026" ⇒ **Word 원고를 서버형 변환기(activePDF DocConverter)가 PDF 로 만든 파일**이고 생성일이 본문의 **수정본 접수일(2017-09-07)과 같은 날**이다 — 수정본 제출 때 변환된 SI 를 출판사가 배포하고 내려받기 날 표지만 찍은 것으로 읽힌다(`[해석]` — 메타데이터가 말하는 만큼; 제목 꼴 "<번호>_File000001_<번호>.docx" 가 어느 시스템의 파일 이름인지는 메타데이터로 정해지지 않는다). **66호 SI(저자 Word 2010 원본 · author 이름 있음)와도, 65호 SI(수령일 2026-09-28 Word 변환본)와도 다르다** |
| sha256 | 본문 `fe186a38e9e9e123bc146c61d1ffc08fa5abf51b8d3126b4e05ba1d36b9e7522` · SI `757dfe916f3deba285ad5000992a2fd8685325657ef7ca1399d9fc0587532a06` — 호출자 명시값과 **일치** |

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| G1 | ★★★ **`x(Li)` 축의 출발 · 결손 처리** — "estimated from current and charging time" 뿐. 전처리 횟수 · 전처리 CE · 결손 배정 · 1 h 정전압 전하 포함 여부 · 1C 정의 미인쇄. 전처리 셀 충전 첫 점을 **1.00** 으로 둔다(표 2). 화학 분석(ICP · 적정) 0 · hXAS 는 0.84 → 0.22(출발 · 규약 미인쇄) · sXAS 표본의 x 배정 방법 미인쇄 | 교정 축 전체가 **전처리 뒤 상대 전하 좌표**다. 66호(1.02 − 결손)와 규약이 0.10 다르다(§(b)) — DFT 의 절대 조성(LiₓNiO₂, x = 1 = 완전 리튬화)과 같은 눈금에 놓을 근거가 지면에 없다 |
| G2 | ★★★ **DFT 설정** — "largely default" · PBE · Grimme · 5 × 5 × 1 k 점 · 10⁻⁵ eV. **Hubbard U · 스핀 편극 · 자기 배열 · 차단 에너지 · x 마다 Li 배열 수(하나) · Bader 격자 · 오차 0**. 모형은 LiₓNiO₂(Co · Mn 없음) · x 네 점(0.25 간격) | 기구의 **시점**(x < 0.5)을 정하는 유일한 채널이다. `[인쇄]`(SI S8 캡션) "the gaps are usually underestimated in DFT calculations involving our choice of XC functional (GGA)" — 저자도 GGA 한계를 적는다. 인용한 [17] Seo · Urban · Ceder 2015 는 TM 준위 · O 띠 보정 논문인데 이 계산은 기본 PBE 다 |
| G3 | ★★★ **SI 기하 ↔ 표 2 x = 0.25** — Bader 를 어느 기하로 셌는지 미기재 | §(a') — 표의 x = 0.25 행은 SI 기하로 재현되지 않고, SI 기하에는 O–O 쌍 · Ni 이동이 있다 |
| G4 | ★★ **operando 파우치 사양** — 전극 크기 · 전해질 · 분리막 · 적재 · 전처리 · 구속이 `[인쇄]` "elsewhere.5" 로 위임 | 파일 31(3286)에서 확인할 것 — 66호 파우치(LP47)와 같은 셀 설계인가 |
| G5 | ★★ **방전 격자 0** — `[인쇄]` "Because the lattice changes upon charge and discharge are reversible, in the following, we only focus on those occurring in the charge cycle" | 이력 수치 0(66호 G2 와 같은 공백) |
| G6 | ★★ **두 상 정련 0** — R-3m 단상 전 구간(`[인쇄]` "In agreement with literature reports, the crystal structure can be described by the space group R3̅m.6,8"). S2 의 4.52 V 패턴은 003 이 넓고 비대칭(`[도표]`) | x < 0.3 의 격자는 공존 상의 평균일 수 있다 — "붕괴" 가 한 상의 연속 변화인지 H2 → H3 같은 상 분율 변화인지 이 편은 가르지 않는다 |
| G7 | ★★ **반복 · 산포 0** — 어느 시험에도 셀 수 인쇄 0 · esd 만 | `[재현]` 슬랩 높이 곡선 잔차 RMS 0.004–0.006 Å(peak-to-peak 0.02–0.06) ↔ 인쇄 esd 0.001–0.003 Å(×2–6) |
| G8 | ★★ **sXAS 표본** — 표본별 x · 전압 · 시간 배정 미인쇄(S6 의 E–t 마커와 Fig. 5 의 x 라벨을 우리가 짝지어야 한다) · A1 세기 정의(봉우리 높이?) · TEY ≈100 Å · 손 연마 | "nearly linearly" 판정(D9)과 표면 ↔ 벌크 연결이 걸린다 |
| G9 | ★ **hXAS** — Ni⁴⁺ 기준 0(NiO · LiNiO₂ 만) · 가장자리 위치 정의 미기재(`[인쇄]` "from 8341 to 8344 eV") | "Ni(III/IV)" 판정의 기준 |
| G10 | ★ **표 1 "capacity loss per cycle" 정의** · C/2 첫 용량 · 컷오프별 셀 수 | D11 — Fig. 1a 와 비가 맞지 않는다 |
| G11 | ★ **온도 · 압력(Q6)** — 코인 · 파우치 구속 0 · XRD 25 °C · hXAS · sXAS 온도 미기재 | — |

# 그림 — 자동 14 + 수동 3 = 17 항목, 실제로 연 것 17 / 안 연 것 0

폴더 `raw/figures/kondrakov2017_ncm811-charge-transfer-lattice-collapse-xrd-xas-dft/`(`figures.json` 17 항목). **자동 크롭의 라벨 ↔ 내용 어긋남 0**(14 장 전부 열어 캡션과 대조했다).
대신 **부분 1 · 과대 1 · 누락 2**: (i) `fig_S7.png` 는 캡션 상자 윗변(y 396 pt)에서 잘려 (d) x = 0.25 판의 아래 ≈12 pt(래스터 띠 xref 140 의 끝, y 406.4 pt 까지)가 빠졌다 (ii) `tab_2.png` 는
표 전체 + 아래 ≈60 % 가 본문 (iii) 본문 **Table 1** 은 "영역 없음" 으로 제외(텍스트 표) (iv) 초록 그래픽은 캡션이 없어 대상 밖.
⇒ **수동 3**: `fig_S7_manual_p6`(전체 그림) · `tab_1_manual_p3` · `fig_TOC_manual_p1`(300 dpi 렌더 클립). 자동 파일은 지우지 않았고 `figures.json` `note` 에 적었다.
**연 것(17)**: fig_1 – fig_5 · fig_S1 – fig_S8 · tab_2 · fig_S7_manual · tab_1_manual · fig_TOC_manual. 대조를 위해 **22호 그림 하나**(`raw/figures/strauss2018_cathode-particle-size-inactive-fraction-assb/fig_S3.png`)를 열었다.
수치 판독은 크롭 PNG 가 아니라 **PDF 안의 원본 래스터**(Fig. 1 625 × 991 · Fig. 2 1814 × 1034 · Fig. 3 1000 × 442 · Fig. 4 2029 × 1460)와 **SI 600 dpi 렌더**(S2 · S6 — SI 그림은 Word 삽입이
띠로 나뉘어 렌더로 읽었다)에서, 22호 Fig. S3 는 위키 크롭(1839 × 662)에서 했다.

## Fig. 1 — 컷오프 여섯 × 50 사이클 유지율 · C/10 충방전 (봤다)

- (a) `[인쇄]` 캡션 "Capacity retention at C/2 for NCM811/Li cells charged to different cutoff voltages". `[도표]` 49 사이클: 4.1 · 4.2 V **≈95 %**(회색 4.1 V 는 빨강에 가려 따로 안 읽힌다;
  4.2 V 는 둘째 사이클 **≈106 %** 까지 올랐다 내려온다) · 4.3 V **≈80**(최대 ≈103) · 4.4 V **≈70**(최대 ≈103.5) · 4.5 V **≈61** · 4.6 V **≈46 %**(첫 점 ≈99.6).
- (b) `[인쇄]` "representative charge/discharge curves at C/10". `[도표]` 충전이 ≈3.38 V 에서 시작해 ≈3.67 V 로 뛰고 **4.60 V 에서 ≈222 mAh g⁻¹** · 방전 끝(3.0 V) **≈200–201**(표 1 4.6 V
  201 ✓) ⇒ `[재현]` CE ≈90.5 % · 결손 ≈21 mAh g⁻¹(Δx ≈0.078 — `[인쇄]` "up to 14%" 안). 곡선이 형성 사이클인지 캡션은 말하지 않는다(`[해석]` 시작 전압 · CE 로 첫 사이클로 읽힌다).

## Fig. 2 — operando XRD 등고선 · `V(x)` · `a`, `c`(x) · da/dE, dc/dE · dQ/dE (봤다)

- (a) 2θ 7–38°(Mo Kα₁,₂) × scan 0–≈920 · 반사 003 · 101 · 015 · 107 · 018 · 110 · 113 + Al(빨강). 003 이 저각으로 갔다가 scan ≈400–460 에서 고각으로 꺾이고 방전에서 되돌아온다.
- (b) `[도표]` 곡선은 **x 1.0 에서 시작**해 0.255 에서 끝난다: 101.37(x 1.0) · 100.66(0.75) · 99.68(0.50) · 94.36(0.255) Å³ ↔ 표 2 101.38 · 100.64 · 99.73 · 94.26 ✓(±0.05; 끝은 기울기가 커
  x 판독 0.003 = 0.09 Å³).
- (c) `[도표]` `a` 2.8653(x 0.995) → **2.8207(0.499)** → 최소 2.8141(≈0.31) → 2.8152(0.255) · `c` 14.252 → **최대 14.469 @ x ≈0.555** → 13.732(0.253). ⚠ 오른쪽 `c` 축 라벨 "14.5 · 14.2 ·
  14.0 · 13.7" 은 **등간격 눈금의 반올림 표기**다(참 눈금 14.5 · 14.233 · 13.967 · 13.7 — x 1.0 의 곡선 위치 14.249 가 선형 눈금으로만 맞는다; D14).
- (d) −da/dE(주황, 0–1.5 Å V⁻¹) · −dc/dE(파랑, 0–22.0 Å V⁻¹, 눈금 7.3 · 14.7 = 1/3 등분) vs E 3.6–4.6 V. `[도표]` −da/dE 는 3.65–3.8 V 에 흩어진 점(0.1–0.5, 3.65 V 에 ≈1.2 한 점) ·
  −dc/dE 봉우리 **≈4.21 V · ≈8.6**. `[인쇄]` "Examination of the da/dE profile revealed an extremum centered at 3.75 V" · "The dc/dE profile shows an extremum at 4.2 V".
- (e) `[도표]` dQ/dE: 충전 시작 ≈3.65 V 에 가시(≈1250) · 주 최대 **≈351 @ 3.77 V** · 둔덕 ≈160 @ 4.03 V · 봉우리 **≈237 @ 4.217 V**(mAh g⁻¹ V⁻¹).
- `[재현]` **연쇄 법칙** — dc/dE = (dc/dx)(dx/dE), dx/dE ∝ dQ/dE: 이 편 `c(x)`(2c)와 S2 의 E(scan)(선형 x)로 만든 −dc/dE 는 **4.22 V 에서 최대**(0.02 V 격자 ≈4 Å V⁻¹; 높이는 평활에 민감해
  판정 안 함). `[인쇄]` "These correlations indicate that the structural changes are connected to redox processes" 의 위치 일치는 공유 인자 dx/dE 에서 대부분 나온다(66호 D14 와 같은 구조 — D13).

## Fig. 3 — 층 모식 · 슬랩 높이 (봤다)

- (a) TM–O 층(회색) · Li 층(청록) · `h_TM-O` · `h_Li-O` 표지 · 단위포(흰 사각).
- (b) `[도표]` `h_TM-O` 2.095(x 0.995) → 2.004(0.7) → 1.941(0.5) → 1.875(0.35) → **≈1.806(끝 0.255)** · `h_Li-O` 2.657 → 2.804(0.7) → 2.878(0.5) → **최대 ≈2.894 @ x ≈0.435**(평활; 원 점
  최대 2.902 @ 0.47) → 2.836(0.35) → **≈2.776(끝)**. `[재현]` 끝 값 3 × (1.806 + 2.776) = **13.75 ↔ `c` 13.732 ✓**(항등식 `c = 3(h_TM-O + h_Li-O)`); 인쇄 끝 값 쌍(1.797 · 2.767)은 13.692 로
  어긋난다(D3).
- 곡선이 들쭉날쭉하다 — `[재현]` 2차 곡선 잔차(x 0.6–0.9) RMS **0.004(`h_Li-O`) · 0.006 Å(`h_TM-O`)** · peak-to-peak 0.02 · 0.06 Å ↔ 인쇄 esd (1)–(3) × 10⁻³ Å. 왼축 "2.02 · 1.88" ·
  오른축 "2.83 · 2.72" 도 등간격 눈금의 반올림 표기(참 2.017 · 1.883 · 2.827 · 2.723).

## Fig. 4 — operando Ni · Co · Mn K 가장자리 (봤다)

- 위: x = **0.84 · 0.63 · 0.43 · 0.22** 네 스펙트럼 + 전단 확대. `[도표]` Ni K 반높이(정규화 0.5) **8341.25 · 8341.55 · 8342.44 · 8343.36 eV** ⇒ `[재현]` x 당 이동 **+1.4(0.84 → 0.63) ·
  +4.5(0.63 → 0.43) · +4.4 eV(0.43 → 0.22)** — x < 0.5 에서 **줄지 않는다**. Co · Mn 은 x 0.22 에서 백색선 모양이 바뀐다(Co 최대 ≈7730 → ≈7732 · Mn ≈6559 → ≈6561 eV — `[도표]`), 전단은 그대로.
- 아래: 1차 미분 폭포(x ≈0.83 아래 → 0.2 위). Ni 미분 최대가 ≈8342 → ≈8343–8344 eV 로 서서히 옮겨 간다.
- ⚠ hXAS 의 x 범위(0.84 → 0.22)는 XRD(1.00 → 0.255)와 다르다 — `[인쇄]` "under the same cycling conditions used for XRD"(D8).

## Fig. 5 — ex situ O K 가장자리 (봤다)

- LiNiO₂ 기준(α 528 · β ≈539 eV) · Pristine · x = **0.54 · 0.30 · 0.27 · 0.25 · 0.24**(쌓아 그림). 탈리튬 표본이 **0.54 하나 뒤 0.30–0.24 에 넷**이다 — pristine 과 0.54 사이 표본 0.
  Pristine 에 ≈533.5 eV 의 작은 봉우리(`*` — `[인쇄]` "may be due to the presence of carbon black additive"; S5 의 Li₂CO₃ 기준 봉우리 ≈532.5 eV 와 `[도표]` ≈1 eV 떨어져 있다 — 판정 안 함).

## SI Fig. S1–S8 · 초록 그래픽 (전부 봤다)

- **S1** NCM811/흑연 1C 3.0–4.3 V + 2 h 정전압: `[도표]` ≈176 → ≈156 mAh g⁻¹(150 사이클 · ≈89 %) · 사이클 ≈10–20 · ≈111–120 에 **자료 빈칸**(서술 0).
- **S2** 등고선 · E–scan/시간(쌍축) · 대표 패턴 여덟(3.63 · 3.68 · 3.76 · 3.83 · 3.96 · 4.11 · 4.23 · 4.52 V) · 107–113 확대 폭포. `[도표]` 파란 마커 scan 20 · 80 · 139 · 200 · 260 · 320 ·
  379 · 439 에 **3.636 · 3.694 · 3.763 · 3.838 · 3.973 · 4.113 · 4.238 · 4.522 V**(인쇄 라벨과 ±0.015 V) · 4.6 V 도달 ≈scan 442 · 정전압 ≈20 scan · 쌍축 **scan 200 ↔ 10 h(175.5 s/scan)** ·
  scan 0 ↔ 1.13 h(D7). 4.52 V 패턴의 003 은 ≈8.9° 로 넓고 비대칭.
- **S3** Ni · Co · Mn K 방전(충전 전) ↔ 충전 + 기준(NiO · LiNiO₂ · CoO · LiCoO₂ · Mn₂O₃ · MnO₂). `[도표]` Ni 반높이: NiO ≈8339.8 < 방전 ≈8341.3 < LiNiO₂ ≈8342.4 < 충전 ≈8343.1 eV — Ni⁴⁺ 기준 없음.
- **S4** Ni · Co · Mn L 가장자리, 표본 #1–#8 · L₃/L₂ 높이 차(빨간 선) — 표본 배정은 S6.
- **S5** O K: NCM811(pristine) · LiNiO₂ · NiO · Li₂CO₃ — `[인쇄]` "indicating that the surface of the pristine cathode material is free of contaminants".
- **S6** 표본 #1–#8 O K + 전단 세기 + E–t. `[도표]` 전단: **#1 1.80 · #2 2.20 · #3 2.26 · #4 2.37 · #5 2.53 · #6 2.25 · #7 2.17 · #8 1.88**. E–t 마커(색 구역 중심): 짙은 빨강
  **4.03 V @ 12.3 h · 4.39 V @ 19.0 h · 4.61 V @ 20.6 h** · 연파랑 **4.61 V @ 23.0 h · 4.40 V @ 23.4 h · 4.31 V @ 23.8 h · 4.00 V @ 28.3 h** — **마커 자리 일곱 ↔ 표본 여덟**(짙은 빨강 하나가
  둘을 겹쳤을 수 있다 — 확대로도 판정 안 됨). 4.6 V 유지 ≈20.6 → 23.0 h(≈2.4 h — XRD 의 1 h 와 다르다) · 충전 시작 3.63 V(t 0) · 방전 끝 ≈37.5 h.
- **S7** x = 1 · 0.75 · 0.5 · 0.25 이완 기하(Li 초록 · Ni 회색 · O 빨강, 계산 칸 검정). (a)–(c) 층이 가지런하다 · **(d) O 원자가 짝 · 무리를 이루고 Ni 몇이 층 밖에 있다**(`[도표]` —
  §(a') 좌표 계산과 같다). 자동 크롭은 (d) 아래가 잘렸다 — 수동 전체 크롭으로 봤다.
- **S8** DOS(빨강 전체 · 초록 Ni · 파랑 O). (a)–(c) 모양이 비슷하다 · **(d) x = 0.25: t2g–eg 사이 틈이 닫히고 ≈−9 eV 에 O 성분 작은 봉우리가 새로 생긴다**(`[도표]`) ↔ 캡션 "Only slight changes
  in DOS as a function of lithium content are observed. The (P)DOS preserves its basic shape during delithiation"(D4).
- **초록 그래픽**(수동) — 층 판 모식 "delithiation" → 좁아진 층 · 확대 두 칸 "Ni^red · O — **charge transfer**"(O → Ni 화살표) ↔ "Ni^ox · O — **charge depletion on O atoms**". 데이터 없음.

## 본문 서술과 어긋난 그림 (요약)

Fig. 2c(`a` @ x 0.5 · `c` 최대 위치) · Fig. 3b(끝 값 · `h_Li-O` 최대 위치) · Fig. 2d/2e(공유 인자) · Fig. 4(hXAS x 범위) · Fig. 5 ↔ S6(표본 수 · "nearly linearly") · S2(scan 간격) ·
S7(d) · S8(d)(캡션 "slight changes") · Fig. 1a ↔ 표 1(손실 비).

# 픽셀 판독 (`[도표]` 전부 — 원본 래스터 · 축 눈금 라벨 중심 적합)

| 그림 | 원본 | 눈금 적합 | 읽은 것 | 검증 · 오차 |
|---|---|---|---|---|
| Fig. 1a | xref 111 · 625 × 991 | 20 % = 73.7 px(0 % = 405.8) · 10 사이클 = 103.45 px | 색별 마커 구역 중심 | 4.2 V 최대 106.2 %(c 2) → 95.0 %(c 49) · 회색(4.1 V) 가려짐 · 4.5 V 첫 10 여 점 가려짐 |
| Fig. 1b | 같은 래스터 | 0.4 V = 79.4 px · 50 mAh g⁻¹ = 103.2 px | 곡선 끝 화소 | 충전 끝 222.4 @ 4.601 V · 방전 끝 ≈200–201 ↔ 표 1 201 ✓ |
| Fig. 2b | xref 138 · 1814 × 1034 | x 0.2 = 103.4 px(1.0 = 1382 · 0.2 = 1795.5) · 1 Å³ = 48.68 px | 연속 추적(열마다 곡선 띠 중점) | 표 2 네 점과 ±0.05 Å³ |
| Fig. 2c | 같은 래스터 | x 0.2 = 103.25 px · `a` 0.02 Å = 128 px · `c` 0.2667 Å = 128 px(등간격 네 눈금) | 색 마스크(주황 · 파랑) 연속 추적 | `a`(0.749) 2.8421 = 표 ✓ · `c`(0.253) 13.732 = 표 ✓ · `a`(0.499) 2.8207 ↔ 표 2.8221(D1) |
| Fig. 2e | 같은 래스터 | 0.5 V = 172.2 px · 500 = 131 px | 열마다 곡선 윗 포락 | 3.77 · 4.03 · 4.217 V 봉우리 |
| Fig. 3b | xref 157 · 1000 × 442 | x 0.2 = 94.4 px · 좌 2.15–1.75 · 우 2.93–2.62(각 등간격 네 눈금) | 색 마스크 열 평균 | 끝 3 × 합 = 13.75 ↔ `c` 13.732 ✓ |
| Fig. 4 Ni K | xref 186 · 2029 × 1460 | 10 eV = 92.5 px · 흡광도 1 = 365 px | 정규화 0.5 행의 색별 교차 | 네 곡선 반높이 |
| S2 E–scan | SI 2 쪽 600 dpi 렌더 | scan 200 = 225.25 px · 10 h = 231 px · 1 V = 286.65 px | 파란 마커 구역 중심 + 검정 곡선 | 마커 전압 ↔ 인쇄 패턴 라벨 ±0.015 V |
| S6 전단 · E–t | SI 5 쪽 600 dpi 렌더 | 0.2 = 102.4 px · 5 h = 228.9 px · 0.5 V = 170.1 px | 마커 색 구역 중심 | 마커 자리 7 ↔ 표본 8 |
| 22호 Fig. S3 | 위키 크롭 1839 × 662 | 0.5 V = 71.5 px · 5 h = 98.8 px(scan 100 ↔ 5 h) | 검정 곡선(첫 충전) | 4.4 V 도달 12.72 h |

# 절별 해체

## 초록 · 서론 (pp. 24381–24382)

- `[인쇄]` 초록: "we investigate changes in crystal and electronic structure of NCM811 (80% Ni) at high states of charge by a combination of operando X-ray diffraction (XRD), operando hard X-ray absorption
  spectroscopy (hXAS), ex situ soft X-ray absorption spectroscopy (sXAS), and density functional theory (DFT) calculations and correlate the results with data from galvanostatic cycling in coin cells" ·
  "XRD reveals a large decrease in unit cell volume from 101.38(1) to 94.26(2) Å3 due to collapse of the interlayer spacing when x(Li) < 0.5 (decrease in c-axis from 14.469(1) Å at x(Li) = 0.6 to 13.732(2) Å
  at x(Li) = 0.25)" · "hXAS shows that the shrinkage of the transition metal−oxygen layer mainly originates from nickel oxidation" · "sXAS, together with DFT-based Bader charge analysis, indicates that the
  shrinkage of the interlayer, which is occupied by lithium, is induced by charge transfer between O 2p and partially filled Ni eg orbitals (resulting in decrease of oxygen−oxygen repulsion)" ·
  "Overall, the results demonstrate that high-voltage operation of NCM811 cathodes is inevitably accompanied by charge-transfer-induced lattice collapse."
- `[인쇄]` 서론: "(up to 200 mAh/g at 4.6 V vs Li+/Li).1" · "Recent studies have demonstrated that the capacity fading is strongly related to the mechanical disintegration of secondary particles.4,5
  The lattice changes of primary particles during (de)lithiation are anisotropic and cause mechanical strain at the grain boundaries resulting in material fracture." · "the interlayer spacing … is subjected
  to severe nonmonotonic changes at voltages above 4.0 V vs Li+/Li.5−8" · "the low X-ray scattering factor of oxygen makes determination of its unit cell position (z-coordinate) challenging" ·
  "It is believed that lithium screens the repulsion between the oxygen planes, which should result in linear expansion of the Li-O slabs during delithiation.9 However, reports on mixing (overlap) between
  TM and oxygen bands in Ni-rich lithium transition metal oxides suggest a high degree of covalency of the TM-O bond.16,17" · "Such charge variations will inevitably affect the oxygen−oxygen repulsion".

## 실험 (p. 24382)

- **전기화학**: `[인쇄]` "Both the electrolyte (1 M LiPF6 in ethylene carbonate and dimethyl carbonate, 3:7 by weight) and the NCM811-based electrodes, with 94 wt % active material, were obtained from
  BASF SE" · 25 °C 코인 · GF/D · Li 금속(Rockwood Lithium) · 250 µL · MACCOR Series 4000. 전극 지름 · 적재 · 두께 0. ⚠ 이 전해질(EC:DMC 3:7 무게)은 66호가 적은 LP30(EC:DMC 1:1) · LP47(EC:DEC 3:7)
  어느 쪽도 아니다.
- **XRD**: `[인쇄]` "Operando XRD measurements were performed at 25 °C on NCM811/Li pouch cells using a high-intensity laboratory Mo Kα1,2 diffractometer.25 Details on the setup as well as the description of
  calibration procedures can be found elsewhere.5 XRD patterns (2θ = 5−37°, Mo Kα1,2) were collected every 150 s with cycling in the voltage range between 3.0 and 4.6 V at a rate of C/20. Structural
  refinement was done with TOPAS−Academic V5 software using the previously described procedure.5"
- **hXAS**: `[인쇄]` "performed on beamline P65 at HASYLAB at DESY. The cell, equipped with 2 mm polyimide windows, was measured in transmission mode under the same cycling conditions used for XRD" · 기준 분말
  NiO · LiNiO₂ · CoO · LiCoO₂ · Mn₂O₃ · MnO₂ · Demeter.
- **sXAS**: `[인쇄]` "in total electron yield (TEY) mode at the RGBL beamline (BESSY II)" · "NCM811 cathodes were delithiated, then extracted from Li cells inside an argon-filled glovebox, washed with dimethyl
  carbonate, dried, and finally manually polished to remove surface impurities" · Au 박 광전자 스펙트럼으로 에너지 보정.
- **DFT**: `[인쇄]` "Settings used for DFT calculations were largely default, including the PBE exchange-correlation functional.28 The convergence criterion was set to 10−5 eV. A 5 × 5 × 1 Monkhorst−Pack k-points
  mesh was utilized together with Grimme correction … The construction of the geometries is based on experimental XRD data. Because exact positions for the lithium vacancies at x(Li) < 1 are not known,
  the lithium atoms were removed in such a manner that the highest possible crystal symmetry was retained. Overall, this gave a unique solution for all structures." `[재현]` POSCAR = 육방 3 f.u. 칸의
  2 × 2 × 1(12 f.u. — Li 12/9/6/3 · Ni 12 · O 24).

## 사이클 (pp. 24382–24383) · Fig. 1 · 표 1 · S1

- `[인쇄]` "The cells underwent a formation cycle at 25 °C and C/10 between 3.0 V … and either 4.1, 4.2, 4.3, 4.4, 4.5, or 4.6 V, and they were then cycled at C/2 in the chosen voltage range" ·
  "To minimize these effects, the NCM811 cathodes were cycled in half-cells without potentiostatic steps at the cutoff voltages. Nevertheless, the capacity fading is virtually enhanced at such conditions
  because overpotentials arising during cycling, e.g., due to material fracture, lower the actual cell voltage. Thus, the data shown in Figure 1a reflect the 'worst-case performance' when compared with the
  typical cyclability of NCM811/graphite cells (Figure S1), yet the Coulombic efficiency stabilized above 98% after the formation cycle" · "increasing the cutoff voltage from 4.1 to 4.2 V barely affects
  the capacity retention, but leads to an increase in specific discharge capacity from 148 to 167 mAh/g" · "The specific capacity loss per cycle is found to be 1.75, 2, 2.25, and 3 times higher for cells
  charged to 4.3, 4.4, 4.5, and 4.6 V, respectively, than those cycled between 3.0 V and 4.1 or 4.2 V" · "This plateau spreads up to 4.27 V and is characteristic of … LiNiO2" · "increasing the cutoff
  voltage on charge above 4.2 V results in large structural changes".

### 표 1 (`[인쇄]`, 텍스트 층)

| Ecutoff (V) | 첫 사이클 방전 C/10 (mAh g⁻¹) | 사이클당 손실 C/2 (mAh g⁻¹) |
|---|---:|---:|
| 4.1 | 148 | 0.4 |
| 4.2 | 167 | 0.4 |
| 4.3 | 188 | 0.7 |
| 4.4 | 197 | 0.8 |
| 4.5 | 200 | 0.9 |
| 4.6 | 201 | 1.2 |

- `[재현]` 손실 비 0.7/0.4 = 1.75 · 2.0 · 2.25 · 3.0 ✓(인쇄 비). 그러나 Fig. 1a 49 사이클 `[도표]` 유지 손실(최대점 기준, %p)은 4.2 V 11.2 · 4.3 V 22.8 · 4.4 V 33.4 · 4.5 V ≈39 · 4.6 V 53.5 —
  4.2 V 대비 **≈2.0 · 3.0 · 3.5 · 4.8**; C/2 첫 용량이 컷오프와 함께 크므로 mAh g⁻¹ 비는 더 벌어진다(D11 — 정의 미인쇄).

## 격자 (pp. 24383–24384) · Fig. 2 · 3 · 표 2 · S2

- ★★★ `[인쇄]` **축**: "In our previous work, we found that high-Ni NCMs suffer from significant first cycle irreversibilities (up to 14%), resulting in partial active lithium loss and delayed change in
  lattice parameters in the initial charge cycle.5 Thus, for better correlation of the lattice parameter changes with lithium content, precycled cells (at 25 °C and C/10 between 3.0 and 4.3 V) were used here
  for XRD." · "cycled at C/20 between 3.0 and 4.6 V, with a constant voltage step for 1 h at the end of charge" · "Because the lattice changes upon charge and discharge are reversible, in the following, we only
  focus on those occurring in the charge cycle and discuss them with respect to lithium content (estimated from current and charging time)."
- `[인쇄]` "Figure 2b shows the decrease in unit cell volume from 101.38(1) to 94.26(2) Å3 (at x(Li) = 0.25) with delithiation. This contraction occurs in a nonlinear manner. At the beginning of the charge
  cycle, the unit cell volume decreases slowly until a lithium content of x(Li) ≈0.5 is reached. Then, the volume decreases much faster, and for x(Li) < 0.4, it decreases virtually linearly and steeply" ·
  "the a lattice parameter exhibits an almost linear drop from 2.8661(1) to 2.8211(1) Å (at x(Li) = 0.5) and then levels off at 2.8153(1) Å (at x(Li) = 0.25)" · "The c lattice parameter … showing an
  initial increase from 14.249(1) to 14.469(1) Å (at x(Li) = 0.6), followed by a broad maximum and finally a steep decrease to 13.732(2) Å (at x(Li) = 0.25)" · "the unit cell volume is mainly controlled
  by the c lattice parameter when x(Li) ≤0.5" · "the large decrease in c causes the significant contraction of unit cell volume (making >70% of the total change)".
- `[인쇄]` 미분: "we took derivatives of the lattice parameters a and c with respect to E to obtain da/dE and dc/dE curves (Figure 2d) … da/dE profile revealed an extremum centered at 3.75 V. Interestingly,
  both its shape and position correlate well with the main maximum seen in the differential capacity curve (dQ/dE) in Figure 2e. The dc/dE profile shows an extremum at 4.2 V, which strongly resembles the
  second largest maximum … These correlations indicate that the structural changes are connected to redox processes" · "we like to recall the capacity retention data and note that the largest changes in
  lattice parameter c occur at the voltage corresponding to the accelerated capacity fading".
- ★★★ `[인쇄]` 슬랩: "Calculating hTM‑O and hLi‑O requires precise determination of the oxygen z-coordinate (zO), which may be prone to refinement faults (especially for data collected in short time periods)
  because of the low X-ray scattering factor of oxygen. To overcome this limitation, the initial zO value (used for refinement of the operando XRD patterns) was determined by neutron diffraction on pristine
  NCM material, as described elsewhere.5" · "The hTM‑O value decreases from 2.111(1) to 1.797(2) Å during the course of delithiation. In contrast, hLi‑O increases from 2.639(1) to 2.889(2) Å (at x(Li) = 0.5)
  and then decreases to 2.767(1) Å (at x(Li) = 0.25)" · "the expansion of the Li-O slabs is more pronounced (0.250(3) vs 0.181(3) Å)" · "the significant drop in c lattice parameter and the resulting unit
  cell volume changes are caused by the simultaneous decrease in both slab heights at x(Li) < 0.5 (more rigorously at x(Li) < 0.45)".
- `[재현]` 셈: 전체 `ΔV/V` −7.02 % · `Δc/c` +1.54 %(1.00 → 0.6) · −5.09 %(0.6 → 0.25) · `Δa/a` −1.77 % · ">70%" = **x ≤0.5 에서 ΔV 의 76.8 %**(표 2; 그림 75.8 %) · 로그 분해로 `c` 의 몫 전 구간
  50.8 % · x 0.5 → 0.25 에서 91.5 % · x 0.5 → 0.25 슬랩 감소 `h_Li-O` −0.122 · `h_TM-O` −0.120(= 14.460/3 − 2.889 → 13.732/3 − 2.767) — **`c` 감소의 절반은 TM–O 층**이다.

### 표 2 (`[인쇄]`, 텍스트 층) — `[재현]` DFT ↔ XRD 차

| x(Li) | `V` DFT | `V` XRD | `a` DFT | `a` XRD | `c` DFT | `c` XRD | O \|e\| | Ni \|e\| | `[재현]` ΔV · Δa · Δc (DFT/XRD − 1) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1.00 | 99.96 | 101.38(1) | 2.91 | 2.8661(1) | 13.63 | 14.249(1) | −1.2 | +1.38 | −1.40 % · +1.53 % · −4.34 % |
| 0.75 | 99.05 | 100.64(1) | 2.883 | 2.8421(1) | 13.76 | 14.386(1) | −1.1 | +1.43 | −1.58 · +1.44 · −4.35 |
| 0.50 | 97.84 | 99.73(1) | 2.855 | 2.8221(1) | 13.86 | 14.460(1) | −1.0 | +1.47 | −1.90 · +1.17 · −4.15 |
| 0.25 | 93.39 | 94.26(2) | 2.840 | 2.8153(1) | 13.37 | 13.732(2) | −0.8 | +1.43 | −0.92 · +0.88 · −2.64 |

- 제목 끝 "0.25⁵⁴" 의 54 = 참고문헌 [54] Tang · Sanville · Henkelman 2009(격자 기반 Bader). `[재현]` 표의 `V` 는 인쇄 `a` · `c` 로 재계산된다(DFT · XRD 모두 ±0.013). ⚠ `[인쇄]` "the unit cell volume
  of the calculated relaxed structures (VDFT) is smaller by up to 1.9% than that of the experimental structures (VXRD) However, the results are reliable" — `V` 의 ≤1.9 % 일치는 **`a` +0.9…+1.5 % 와
  `c` −2.6…−4.4 % 의 상쇄**다(D6).

## 전이금속 K 가장자리 (pp. 24384–24385) · Fig. 4 · S3 · S4

- `[인쇄]` "The positions of both the edge and pre-edge shift with decreasing x(Li) from 8341 to 8344 eV and from 8330 to 8332 eV, respectively. Overall, these shifts toward higher energy are indicative of
  nickel oxidation.13,14 The initial position is located between the nickel K-edge in NiO and LiNiO2, thus suggesting a mixed Ni(II/III) oxidation state, which evolves to Ni(III/IV) during the charge cycle
  (Figure S3)" · Co: "delithiation leads to distinct changes in Co K-edge shape. However, both the shape and position of the pre-edge remain virtually unaffected" · Mn: "differences among the sample and
  reference edge shapes do not allow unambiguous determination of the oxidation state but point at Mn(IV)" · "However, we note that our data only demonstrate clear nickel redox activity" · "Because the Ni
  content is high, we do not observe signs of exhaustion of nickel redox activity at high states of charge, as previously reported for … (NCM111).14 Instead, nickel is continuously oxidized over the whole
  x(Li) range." · "Assuming that cobalt and manganese remain in their initial oxidation states and nickel changes by 0.8 charge units, we obtain 12% difference in nickel ionic radius, which qualitatively
  agrees with the 15% decrease in hTM‑O from XRD."
- `[재현]` Shannon 6 배위(Ni²⁺ 0.69 · 저스핀 Ni³⁺ 0.56 · Ni⁴⁺ 0.48 Å) 사이를 선형으로 두면 평균 Ni 산화수 2.875 → +0.8 에서 **12.2 %** ✓. 그러나 XRD 창(Δx 0.75)을 Co · Mn 고정으로 옮기면 Ni 한 개당
  **+0.94**(= 0.75/0.8) → 14.1 % — 인쇄 "0.8 charge units" 는 창과 한 자리 어긋난다(D15, 결론에는 무해).

## 산소 K 가장자리 (pp. 24385–24386) · Fig. 5 · S5 · S6

- `[인쇄]` "It should be noted that the probing depth is limited to around 100 Å, and the results may be affected by byproducts formed in side reactions.41" · "The relative intensities are normalized to the
  continuum jump at the photon energy of 576 eV after background subtraction" · "the A1 peak intensity increases nearly linearly with decreasing lithium content due to depopulation of the 3d states of nickel
  during its oxidation (see also Figure S6)" · "The fact that A1 is strong and distinct suggests considerable mixing for the pristine NCM811 material already, like in the case of LiNiO2, and the increase in
  peak intensity further implies charge transfer between the 3d states of nickel and 2p states of oxygen. Consequently, delithiation may result in depopulation not only of the eg orbitals of nickel, but
  also of the pz orbitals of oxygen, which inevitably affects the effective charge on the oxygen atoms."
- `[해석]` S6 표본 배정(인쇄 0): 짙은 빨강 마커 자리 셋(4.03 · 4.39 · 4.61 V) + 연파랑 넷(4.61 · 4.40 · 4.31 · 4.00 V) = 일곱. 전단 값이 전압으로 짝을 이룬다 — #1(1.80) ↔ #8(1.88, ≈4.0 V) ·
  #2(2.20) ↔ #6(2.25, ≈4.4 V) ⇒ #1 = 4.03 V 충전 · #2 = 4.39 V · #3 · #4 = 4.61 V(겹친 마커) · #5 = 유지 끝 으로 읽힌다. 그러면 Fig. 5 의 탈리튬 다섯(0.54 · 0.30 · 0.27 · 0.25 · 0.24) =
  #1–#5 이고 Fig. 5 의 pristine 은 S6 밖의 스펙트럼이다. 이 배정 위에서 A1(전단) 증가는 x 0.54 → 0.30 에 +0.40(x 당 1.7) · 0.30 → 0.24 에 +0.33(x 당 5.5) — **"nearly linearly" 가 아니라
  x < 0.30(4.4 V 위 · 4.6 V 유지 중)에 몰린다**(D9).

## 산소 전하 · DFT (p. 24386) · 표 2 · S7 · S8 · 부록 1

- `[인쇄]` "LixNiO2 was chosen as a model system for NCM811, where x(Li) was varied in the range 1.0−0.25" · "The structures were based on the experimental XRD results, and the geometries were consequently
  fully optimized (including volume relaxation)" · "the nonmonotonic behavior of the lattice along the z-direction (changes in c lattice parameter) with decreasing lithium content is well reproduced by the
  calculations. Thus, implementation issues of the relaxation procedure can be ruled out."
- ★★★ `[인쇄]` "The charge on the nickel atoms increases from initially +1.38 to +1.47 at x(Li) = 0.5 and then slightly decreases to +1.43 at x(Li) = 0.25. The charge on the oxygen atoms varies from −1.2 to
  −0.8, with the change being greatest when x(Li) decreases from 0.5 to 0.25" · "The nonmonotonic change in nickel charge (break of the positive trend when x(Li) < 0.5) is indicative of charge transfer from
  oxygen to nickel at low lithium content. Accordingly, the collapse of the Li-O slabs at x(Li) < 0.5 (and the related shrinkage in interlayer spacing) can be understood in terms of the effective charge on
  the oxygen atoms" · "Overall, this indicates that the shrinkage is triggered by depletion of the negative charge on the oxygen atoms. The sXAS data establish considerable mixing between the 2p orbitals of
  oxygen and the partially filled eg orbitals of nickel. This overlap induces charge transfer, which ultimately leads to collapse of the layered NCM structure." · "Both at high states of charge and at high
  temperatures, the negative charge transfer from oxygen to nickel results in release of gaseous oxygen and formation of a stable NiO phase."
- `[인쇄]`(SI S8 캡션) "Only slight changes in DOS as a function of lithium content are observed. The (P)DOS preserves its basic shape during delithiation, thus indicating that only the occupation of the
  Li/Ni conduction bands is altered. We note that the gaps are usually underestimated in DFT calculations involving our choice of XC functional (GGA). This can possibly explain the less pronounced gap for
  x(Li) = 0.25."

## 결론 (p. 24387)

- `[인쇄]` "Galvanostatic cycling tests showed that operation of the cathode material in the high-voltage range (E > 4.2 V vs Li+/Li and x(Li) < 0.5) causes accelerated capacity degradation. X-ray
  diffraction revealed a large decrease in unit cell volume due to collapse of the layered lattice structure (severe shrinkage of the interlayer spacing) when x(Li) < 0.5." · "results from density functional
  theory calculations demonstrated that this mixing induces charge transfer resulting in depletion of the effective oxygen charge and causing collapse of the layered NCM structure. Collectively, our findings
  emphasize the importance of the electronic mixing in nickel−oxygen states for maintaining the crystalline lattice".

## 참고문헌 54 편 — 우리 축에 닿는 것

**[5] Kondrakov, Schmidt, Xu, Geßwein, Mönig, Hartmann, Sommer, Brezesinski, Janek 2017 *JPCC* 121, 3286**(파일 31 — 여덟 번 인용) · **[4] Ishidzu, Oka, Nakamura 2016 *SSI* 288, 176**(파일 34) ·
[2] Noh, Youn, Yoon, Sun 2013 *JPS* 233, 121 · [9] Van der Ven, Aydinol, Ceder, Kresse, Hafner 1998 *PRB* 58, 2975(차폐 서사 — 66호 [38]) · [17] Seo, Urban, Ceder 2015 *PRB* 92, 115118(TM 준위 · O 띠 보정) ·
[14] Petersburg … Alamgir 2012 *J. Mater. Chem.* 22, 19993(NCM111 Ni 산화환원 소진) · [7] Li J. … Dahn 2015 *Electrochim. Acta* 180, 234(operando 중성자 NCM 파우치) · [34] Croguennec … Delmas 2001
*J. Mater. Chem.* 11, 131(LiₓNi₁.₀₂O₂, x ≤0.30) · [33] Li · Reimers · Dahn 1993 *SSI* 67, 123 · [46] Chen · Freeman · Harding 2011 *PRB* 84, 085108(LiNiO₂ JT · 전하 불균등 DFT) · [51] Antolini 2003 ·
[52] Kanno 1994 · [53] Xu … Tong 2017 *JMCA* 5, 874(층상 → NiO 암염) · [41] Yoon … Yang 2007 *JPS* 174, 1015(NCA sXAS) · [25] de Biasi 2015 *CrystEngComm* 17, 6163(회절 장치) · [54] Tang 2009(Bader).

# 어휘 집계 — NFKC · 줄 끝 하이픈 복원 · 내려받기 표지 제거 · 대소문자 구분 (본문 · 캡션 | 참고문헌 | SI 산문, POSCAR 제외)

| 지문 열 | 본문 | 참고문헌 | SI | 메모 |
|---|---:|---:|---:|---|
| `Ni−O`/`Ni-O` · `nickel−oxygen` · `charge transfer` | **0** · 1 · 7 | 0 | 0 | "Ni–O" 는 22호 digest 요약 낱말 — 원문은 "O 2p ↔ Ni eg" |
| `2p` · `eg` · `mixing` · `hybridiz` · `covalen` | 10 · 7 · 7 · 2 · 1 | 0 | 0 | |
| `collapse` · `Bader` · `DFT` · `PBE` · `LiNiO2/LixNiO2` | 6 · 4 · 11 · 1 · 13 | 0 · 1 · 0 · 0 · 4 | 0 · 0 · 2 · 0 · 0 | |
| `Hubbard` · `+U` | **0** | 0 | 0 | 기본 PBE |
| `dimer` · `peroxo` · `superoxo` · `migrat` | **0** | 0 | 0 | SI x = 0.25 기하의 O–O 쌍 · Ni 이동 서술 0 |
| `rock salt`/`NiO-type` · `gaseous oxygen` | 2 · 1 | 0 | 0 | LiNiO₂ 인용 서술 |
| `identifiab` · `uncertain` · `±` · `standard deviation` · `error` | **0** | 0 | 0 | 산포 어휘 0 |
| `ICP` · `titration` · `chemical analysis` | **0** | 0 | 0 | `x` 의 화학 검증 0 |
| `current and charging time` · `precycl` · `first cycle` · `irreversib` · `calibrat` | 1 · 1 · 1 · 1 · 1 | 0 | 0 | `calibrat` 1 = 장치 교정("elsewhere.5") |
| `OCV`/`open-circuit` · `hysteres` · `two-phase` · `inactive` | **0** | 0 | 0 | |
| `contact` · `crack` · `fractur` · `disintegrat` · `particle` | **0** · 0 · 2 · 1 · 2 | 0 | 0 | |
| `pressure` · `LLI`/`LAM` · `impedance`/`EIS` | **0** | 0 | 0 | ASSB · EIS 0 |
| `indicat` · `suggest` · `demonstrat` · `inevitabl` · `establish` · `may` | 14 · 7 · 6 · 3 · 2 · 5 | — | 3 · 0 · 0 · 0 · 0 · 0 | 기구 문장이 "indicate/suggest" 와 "demonstrate/establish/inevitably" 를 섞는다 |

# Q1~Q8 판정 (닻 페이지 수집 지침)

| Q | 판정 | 근거 |
|---|---|---|
| **Q1** 접촉 손실 정량 | **없다 — `θ(N)` 0/67** | 사이클 축은 유지율뿐(Fig. 1a 50 사이클 · S1 150 사이클). `[인쇄]` "overpotentials arising during cycling, e.g., due to material fracture, lower the actual cell voltage" — 겉보기 감쇠의 `η` 몫에 이름을 붙였으나 측정 0 · 균열 · 활성 질량 · LAM 측정 0 |
| **Q2** 독립 관측 | **없다(층 하나)** | `LAM_PE` 대상 없음(액체 반쪽 · 한 충전). 층: **교정 규약 대조 재료** — 같은 연구망 세 규약 · NCM811 쌍에서 전압 맞춤 이동이 규약 항(+0.10)을, 격자 맞춤 − 전압 맞춤이 시편 항(붕괴 구간 0 … +0.03 — 정전압 전하 미인쇄)을 준다(`[재현]`) — "SOC 추종 상 분율" 채널(22호)의 `x_active` 에 붙는 불확실성의 크기 |
| **Q3** 라벨 층위 | **measured-crystallographic(단상 · esd 만 — `[재현]` 슬랩 잔차 ×2–6) + charge-counted *relative* axis(전처리 셀 충전 첫 점 = 1.00 · 결손 미배정) + measured-spectroscopic(hXAS 투과 · sXAS TEY 표면 ≈100 Å · 연마) + computed(LiₓNiO₂ PBE 네 점 · Bader — x = 0.25 행이 SI 기하로 재현 안 됨)** | 표 2 ↔ 본문 `a`(0.5) · 슬랩 끝 값 항등식 · scan 간격 · hXAS x 범위 |
| **Q4** 유일성 · 식별성 | **0/67 — 쉰아홉 번째 성질** "전자 구조 측정 둘(Ni K · O K)이 x 0.5 에서 꺾임을 보이지 않는 자리에서 격자 붕괴의 원인과 시점을 LiNiO₂ PBE 네 점의 Bader 꺾임 하나로 정하고, 그 계산의 절대 조성을 전하로 센 상대 축(전처리 셀 충전 첫 점 = 1.00)과 같은 눈금에 놓았으며, SI 기하가 표의 x = 0.25 행을 재현하지 않는 것(O–O 쌍 · Ni 이동)을 적지 않았다" | `identifiab` · `uncertain` · `±` · `error` 0 · 본문 indicate · suggest 21 회 · demonstrate · establish · inevitably 11 회 |
| **Q5** Li-In 기준 | **해당 없음** | Li 금속 상대극(액체) · 기준극 0 |
| **Q6** 압력 | **없다** | `pressure` 0 · 코인 · 파우치 구속 미기재 |
| **Q7** dead Li | **해당 없음** | Li 금속 상대극(액체) · 재고 관측 0 |
| **Q8** 화학 · OCP | **층 하나 — NCM811 구조 붕괴의 현상 · 전압 · 부피 원자료(그림 판독) + 기구 해석** | `c` 최대 ≈4.0 V · 두 슬랩 동시 감소 x < 0.45(≈4.13–4.16 V) · `ΔV/V` −7.02 %(4.6 V + 1 h) · 4.3 V −4.9…−5.4 % · dQ/dE 봉우리 3.77 · 4.217 V · 첫 사이클 방전 148–201 mAh g⁻¹(컷오프 4.1–4.6 V) · OCV 곡선 0 |

# ★ (a) `c` 붕괴의 기구 — 측정 셋 · 계산 하나

## 채널별로 무엇을 보였나

| 채널 | 측정 / 계산 | 무엇을 보였나 | x 0.5 근처의 꺾임 | 한계 |
|---|---|---|---|---|
| operando XRD — `a` · `c` · `V` | 측정(파우치, 전처리 셀의 한 충전) | `c` 최대(x ≈0.555 — `[도표]`) 뒤 급감 · `V` 의 76.8 % 가 x ≤0.5 | ✅ 현상 자체 | 단상 R-3m · esd 만 · x 는 상대 전하 좌표(§(b)) |
| operando XRD — `h_TM-O` · `h_Li-O` | 측정(`z_O` 정련 · 첫값 = 원형 중성자) | `h_TM-O` 2.111 → ≈1.80 단조 · `h_Li-O` 2.639 → 최대 ≈2.89(x ≈0.44–0.5) → 2.77 | ✅ `h_Li-O` 가 꺾인다 | `[재현]` 잔차 RMS 0.004–0.006 Å(esd 의 ×2–6) · x 0.5 → 0.25 에서 **두 슬랩이 같은 크기로(−0.122 · −0.120 Å) 준다** |
| operando hXAS — Ni · Co · Mn K | 측정(투과) | Ni 가장자리 연속 이동(`[인쇄]` "continuously oxidized") · Co · Mn 모양만 | ❌ `[도표]` 반높이 이동 x 당 +1.4 → +4.5 → +4.4 eV — 줄지 않는다 | Ni⁴⁺ 기준 0 · 가장자리 위치는 공유 결합 · 국소 구조에도 걸린다(`[해석]`) |
| ex situ sXAS — O K 전단 A1 | 측정(TEY ≈100 Å · 손 연마 표면) | A1 이 탈리튬과 함께 커진다 → O 2p–Ni eg 혼성 · O 2p 빈자리 | ❌ 표본이 pristine · 0.54 · 0.30–0.24 — 0.5 근처 해상 0 · `[인쇄]` "nearly linearly"(우리 배정으로는 x < 0.30 에 몰린다 — D9) | 표면 · 표본 배정 미인쇄 |
| DFT — LiₓNiO₂ PBE + Bader | **계산**(네 점) | Ni 전하 +1.38 → +1.47 → +1.43 · O −1.2 → −0.8 · `c` 13.63 → 13.86 → 13.37 | ✅ Ni 전하 꺾임(x 0.5 → 0.25) | 0.25 간격 · 모형이 NCM811 이 아니다 · +U 0 · **x = 0.25 행이 SI 기하로 재현 안 됨**(§(a')) |

⇒ **현상(붕괴)은 측정이다. "O 2p ↔ Ni eg 혼성" 도 측정(sXAS)이 받친다. 그러나 "x < 0.5 에서 O 가 Ni 로 전하를 넘겨 O–O 반발이 줄어 붕괴한다" 는 인과 · 시점은 계산 하나(네 점)에 달려 있다**
(`[해석]`). 측정 셋 중 x 0.5 근처의 꺾임을 보이는 것은 격자 자신뿐이고, 그것은 설명할 대상이지 설명이 아니다.

## "Ni–O 전하이동" — 22호 :168 명제

- 낱말: `Ni−O`/`Ni-O` **0 회**(본문 · SI). 인쇄된 것은 "charge transfer between O 2p and partially filled Ni eg orbitals" · "charge transfer from oxygen to nickel" · "charge transfer between the 3d states of
  nickel and 2p states of oxygen" · "electronic mixing in nickel−oxygen states". ⇒ 22호 digest 요약 "(Ni–O 전하이동, refs 20, 21)" 은 이 편 기구의 **충실한 한국어 요약**이다(66호 [20] 은 그 낱말을
  주지 않았다 — 66호 판정) — **ref 21 쪽으로 선다**.
- 위치: 22호 요약 "c 는 x ≈ 0.5 까지 증가 후 급감" — 이 편은 x ≈0.555–0.6(최대) · < 0.5(급감) · < 0.45(두 슬랩 동시 감소)를 **이 편의 x 축**(전처리 셀 충전 첫 점 = 1.00) 위에 둔다. 같은 현상을 66호
  NCM811 은 δ 0.45 에, 22호 NCM622 교정은 x ≈0.5 에 둔다 — **x 값은 교정 규약 위의 값**이고, 전압으로는 NCM811 두 교정이 같은 곳(≈3.99–4.0 V)에 놓는다(§(b)).
- 조성: **NCM811 한 조성**(실험) · LiₓNiO₂(계산). 제목의 "Ni-Rich NCM" 은 NCM811 로만 뒷받침된다. 22호 NCM622 에 옮기는 것은 22호의 일이다 — 66호 표 S1 은 여섯 조성 모두 `c` 최대 δ ≈0.45 를
  보였다(66호 판정).

## 시작 x · 전압 (`[재현]` — S2 의 E(scan) + 선형 x(scan): x(0) = 1.00 · 4.6 V 도달 scan 442 에서 x = 0.255 + δ_CV, δ_CV = 0 … 0.02)

| x(이 편 축) | E (V, C/20 통전) | 사건 |
|---|---|---|
| 0.555 | 3.99–4.01 | `c` 최대(`[도표]` 14.469) |
| 0.50 | 4.06–4.07 | `[인쇄]` "until a lithium content of x(Li) ≈0.5 … Then, the volume decreases much faster" |
| 0.45 | 4.13–4.16 | `[인쇄]` "more rigorously at x(Li) < 0.45" — 두 슬랩 동시 감소 |
| 0.435 | 4.16–4.18 | `h_Li-O` 최대(`[도표]` 평활) |
| 0.40–0.42 | 4.20 | `[인쇄]` dc/dE 극값 "4.2 V" · dQ/dE 봉우리 4.217 V(`[도표]`) |
| 0.31–0.33 | 4.30 | — |
| 0.28–0.30 | 4.40 | — |
| 0.255 | 4.6 + 1 h | 충전 끝 |

- ⇒ 결론 "(E > 4.2 V vs Li+/Li and x(Li) < 0.5)" 는 한 경계가 아니다 — 이 편 셀에서 x 0.5 는 ≈4.06 V 이고 4.2 V 는 x ≈0.40–0.42 다(D12). 표 1 의 컷오프 효과(4.2 → 4.3 V 에서 사이클당 손실 ×1.75)는
  4.2 V 위의 판단이다.

# ★ (a') DFT 재현 — SI POSCAR 로 표 2 를 다시 셈 (`[재현]`, SI 텍스트 층 좌표)

POSCAR 넷을 파싱해(각각 Li 12 · 9 · 6 · 3 + Ni 12 + O 24 — 원자 수 검사 통과) 칸 벡터 · 부피 · 최소 거리를 셌다. 계산 칸은 육방 3 f.u. 칸의 2 × 2 × 1(12 f.u.)이라 육방 칸 값 = 초칸 ÷ 4.

| x(Li) | 표 2 DFT `V` · `a` · `c` | POSCAR `V`/4 · `a`(\|a₁\|/2 · \|a₂\|/2) · `c`(\|a₃\| · 수직 높이) | 칸 각 γ · ∠(a₂,a₃) | 최소 O–O | Ni 6 배위(< 2.3 Å) |
|---|---|---|---|---|---|
| 1.00 | 99.96 · 2.91 · 13.63 | **100.09** · 2.9121 · 2.9120 · 13.6285 · 13.6285 | 119.99° · 89.96° | 2.629 Å | 12/12 |
| 0.75 | 99.05 · 2.883 · 13.76 | **99.04** · 2.8832 · 2.8828 · 13.7557 · 13.7557 | 119.98° · 90.02° | 2.560 | 12/12 |
| 0.50 | 97.84 · 2.855 · 13.86 | **98.19** · 2.8567 · 2.8657 · 13.8635 · 13.8633 | 120.10° · 90.01° | 2.498 | 12/12 |
| **0.25** | **93.39 · 2.840 · 13.37** | **98.63** · 2.8859 · 2.9161 · 13.6437 · 13.6208 | **120.64° · 86.99°** | **1.331 Å(쌍 둘)** | **8/12**(5 배위 2 · **4 배위 2**) |

- x = 1 · 0.75 · 0.5 는 표를 재현한다(x = 1 의 `V` 0.13 % 차는 표가 반올림된 `a` 2.91 로 `V` 를 셈한 탓 — 2.91 이면 99.96 ✓; x = 0.5 는 +0.36 %).
- **x = 0.25 는 재현되지 않는다**: POSCAR `V` 가 표보다 **+5.6 %**(98.63 ↔ 93.39), XRD(94.26)보다 **+4.6 %** 크다 — `[인쇄]` "VDFT is smaller by up to 1.9% than … VXRD" 와 반대(D5). POSCAR 로는
  `V` 가 x 0.5 → 0.25 에 **+0.44 % 늘어난다**(표 −4.5 % · XRD −5.5 %) · `c` 는 13.86 → 13.62–13.64(−1.6 %, 표 −3.5 %). 칸이 기울었다(∠(a₂,a₃) 86.99°).
- **그 기하의 화학**: O15–O20 · O16–O19 가 **1.331 Å**(초과산화 O₂⁻ 결합 길이 자릿수 — `[해석]`) — 한쪽 O 는 제 층(z ≈0.09), 다른 쪽은 Li 슬랩 안으로 들어갔다(z 0.051 · 0.9955). **Ni7 · Ni8 이
  z 0.710**(제 층 0.833 → Li 슬랩 안, O 4 배위). 두 번째로 짧은 O–O 는 2.325 Å.
- 그림과 맞는다: S7(d) 에 O 짝 · 무리와 층 밖 Ni 가 보이고, S8(d) 에 ≈−9 eV O 성분 봉우리(`[해석]` O–O σ 결합 상태 자리)와 t2g–eg 틈 닫힘이 보인다. 본문 · 캡션은 이 셋을 말하지 않는다
  (`dimer` · `peroxo` · `superoxo` · `migrat` 0 회 · S8 캡션 "Only slight changes").
- ⇒ `[해석]` 둘 중 하나다: (i) 표 2 의 x = 0.25 DFT 행 · Bader 전하는 SI 에 없는 다른 기하에서 나왔다 — 그러면 SI 는 그 행을 재현할 재료를 주지 않는다; (ii) SI 기하에서 나왔다 — 그러면 표의 격자값이
  틀렸고, **x = 0.25 의 "O 전하 −0.8 · Ni 전하 되돌림" 은 층상 격자 안의 전하 이동이 아니라 O–O 결합 형성 · Ni 이동이 섞인 구조의 평균**이다. 어느 쪽이든 **기구의 시점을 정하는 유일한 점(x = 0.25)이
  지면에서 재현되지 않는다**. 이 편은 O₂ 방출 · NiO 형 암염 전이를 인용 서사로 말한다(`[인쇄]` "the negative charge transfer from oxygen to nickel results in release of gaseous oxygen") — (ii) 라면 그 서사가
  자기 계산 기하 안에 이미 있는 셈이지만, 지면은 그것을 이 편의 결과로 적지 않았다.

# ★ (b) `x(Li)` 축 규약 — 세 교정 · 규약 항 ↔ 시편 항

## 무엇이 인쇄됐나 — 같은 연구망 세 교정

| 항목 | 22호(Strauss 2018) | 66호(de Biasi 2017) | **67호(이 편)** |
|---|---|---|---|
| 재료 | NCM622(NCM-M) | NCM 여섯(NCM811 포함) | **NCM811** |
| 셀 · 전해질 | 파우치 LIB · LP57 | 파우치 LIB · LP47 | 파우치 LIB · 미기재(`[인쇄]` "elsewhere.5"); 코인은 EC:DMC 3:7(무게) |
| 이력 | **첫 사이클** C/10 4.4–2.9 V | 전처리 3 사이클(3.0–4.3 V) → **넷째 충전** C/10 3.0–4.6 V + 1 h | **전처리(C/10 3.0–4.3 V, 횟수 미인쇄) → 충전 C/20 3.0–4.6 V + 1 h** |
| `x` 축 문장 | `[인쇄]`(22호) "The lithium content was calculated from the electrochemical data" | `[인쇄]`(66호) 같은 문장 + "Coulombic efficiencies of less than 100% are a result of Li loss from the cathode material only" | `[인쇄]` "lithium content (estimated from current and charging time)" |
| `x₀` | 1.02(공칭, 원형) | 1.02 − 전처리 CE 결손(NCM811 **0.90** · NCM622 0.93) | **1.00**(전처리 셀 충전 첫 점 — 결손을 빼지 않았다) |
| 첫 사이클 | 씀 | 피함(전처리) | **피함 — 이유를 인쇄**: "first cycle irreversibilities (up to 14%), resulting in partial active lithium loss and delayed change in lattice parameters in the initial charge cycle.5" |
| 화학 분석 | 0 | 0 | 0 |

⇒ **같은 연구망 · 같은 장치 계열 · 석 달 사이의 세 교정이 `x₀` 를 셋으로 둔다**(1.02 · 1.02 − 결손 · 1.00). 이 편은 22호가 쓴 첫 사이클 교정을 **피해야 할 이유**를 인쇄했다(22호는 이 편을
ref 21 로 인용하면서 첫 사이클 교정을 썼다 — `[해석]` 연구망 안의 관행 불일치).

## NCM811 쌍 — 이 편 ↔ 66호 표 S1 (`[재현]`)

두 교정 모두 전처리 셀이라 **규약 차는 1.00 − 0.90 = 0.10 으로 고정**된다(전처리 결손의 행방과 무관 — 같은 참 출발 상태를 두 규약이 다르게 부른다). 비교를 둘로 나눈다:

- **격자 맞춤** — 66호 행의 `V`(또는 `a` · `c`)와 같은 값을 이 편 곡선(Fig. 2b · 2c 판독)에서 찾아 x 를 읽는다: `x_67(격자) − δ_66` = **규약 항 + 시편(로트 · 격자 경로) 항**.
- **전압 맞춤** — 66호 행의 `U`(C/10 통전)와 같은 전압을 이 편 S2 곡선(C/20 통전, 선형 x)에서 찾는다: `x_67(전압) − δ_66` = **규약 항 − 율 분극 항**(C/20 쪽이 같은 전압에서 더 충전돼 있다 — `[해석]`).

| 66호 δ | 66호 `U` | 격자 `a` | 격자 `c`(가지) | 격자 `V` | 전압(δ_CV 0 · 0.02) |
|---|---:|---:|---:|---:|---:|
| 0.85 | 3.67 | +0.114 | +0.067 | 범위 밖 | +0.050 · +0.052 |
| 0.80 | 3.69 | +0.121 | +0.075 | +0.157 | +0.072 · +0.075 |
| 0.75 | 3.72 | +0.130 | +0.083 | +0.179 | +0.085 · +0.089 |
| 0.70 | 3.75 | +0.121 | +0.083 | +0.185 | +0.086 · +0.092 |
| 0.65 | 3.78 | +0.124 | +0.086 | +0.185 | +0.096 · +0.103 |
| 0.60 | 3.81 | +0.126 | +0.082 | +0.170 | +0.090 · +0.099 |
| 0.55 | 3.86 | +0.130 | +0.082 | +0.161 | +0.097 · +0.107 |
| 0.50 | 3.92 | +0.125 | +0.075 | +0.150 | +0.096 · +0.107 |
| 0.45 | 3.99 | +0.122 | 해 없음(14.480 > 이 편 최대 14.469) | +0.138 | +0.102 · +0.114 |
| 0.40 | 4.05 | +0.139 | 해 없음(14.475) | +0.140 | +0.105 · +0.119 |
| 0.35 | 4.12 | +0.145 | **+0.133** | **+0.133** | +0.107 · +0.122 |
| 0.30 | 4.19 | +0.155 | **+0.123** | **+0.126** | +0.111 · +0.127 |
| 0.25 | 4.24 | +0.162 | **+0.124** | **+0.126** | +0.109 · +0.126 |
| 0.20 | 4.32 | +0.155 | **+0.122** | **+0.123** | +0.103 · +0.122 |
| 0.15 | 4.50 | (평탄) | **+0.125** | **+0.126** | +0.112 · +0.132 |

- **전압 맞춤 ≈ 규약 차**: δ ≤0.65 에서 +0.096…+0.112(δ_CV 0) · +0.103…+0.132(δ_CV 0.02) — 1.00 − 0.90 = 0.10 과 같은 자릿수(δ_CV 0 이면 거의 같다). 두 셀의 **전하–전압 곡선은 규약만 빼면 같다**(율 분극 차는 작다). δ 0.85–0.70 의 +0.05…+0.09 는 충전
  첫머리 분극(통전 시작)의 차다(`[해석]`).
- **격자 맞춤 − 전압 맞춤 = 시편 항**: 붕괴 구간(δ ≤0.35)에서 `c` · `V` 가 +0.122…+0.133 으로 **서로 일치** ⇒ 시편 항 **0 … +0.03** — 1 h 정전압 전하(δ_CV, 미인쇄)를 0 으로 두면 +0.015…+0.03(이 편 격자가
  같은 전압에서 조금 더 수축), 0.02 로 두면 ≈0. 율 분극은 전압 맞춤을 0.10 아래로 당기는 방향이라(`[해석]`) 초과분이 있다면 그것을 설명하지 않는다 — 로트(원형 격자 인쇄 0) · 전해질 · 전처리 횟수가 후보. 충전 초반(δ ≥0.5)은 채널마다 +0.07(`c`) · +0.12(`a`) ·
  +0.17(`V`) 로 **갈린다** — 같은 `V` 에 두 셀의 (`a`, `c`) 쌍이 다르다(격자 경로 차; 이 편 x 1.00 의 `a` 2.8661 · `c` 14.249 ↔ 66호 δ 0.90 의 2.8669 · 14.266).
- 끝 상태: 이 편 x 0.255 `V` 94.26 ↔ 66호 δ 0.11 `V` 94.086 — 66호 셀이 더 수축한 채로 끝났다(이 편 곡선 범위 밖).

## NCM622 쌍 — 22호 첫 충전 ↔ 66호 넷째 충전, 같은 방법 (`[재현]`, 22호 Fig. S3 전압–시간 + 선형 x(1.02 → 0.31, 4.4 V 도달 12.72 h))

| 66호 δ | 66호 `U` | 22호 t(U) | x_22 | 전압 맞춤 이동 |
|---|---:|---:|---:|---:|
| 0.85 | 3.69 | 0.24 h | 1.007 | +0.157 |
| 0.80 | 3.72 | 1.18 | 0.954 | +0.154 |
| 0.75 | 3.74 | 2.51 | 0.880 | +0.130 |
| 0.70 | 3.77 | 4.23 | 0.784 | +0.084 |
| 0.65 | 3.79 | 5.15 | 0.732 | +0.082 |
| 0.60 | 3.83 | 6.50 | 0.657 | +0.057 |
| 0.55 | 3.88 | 7.48 | 0.602 | +0.052 |
| 0.50 | 3.96 | 8.51 | 0.545 | +0.045 |
| 0.45 | 4.04 | 9.45 | 0.492 | +0.042 |
| 0.40 | 4.12 | 10.36 | 0.442 | +0.042 |
| 0.35 | 4.22 | 11.35 | 0.386 | +0.036 |
| 0.30 | 4.32 | 12.30 | 0.333 | +0.033 |

- 격자 맞춤 이동(66호 `[재현]`)은 x 0.90–0.35 에서 **0.057–0.082 로 거의 일정**한데, 전압 맞춤 이동은 **+0.157 → +0.033 으로 다섯 배 변한다** — 22호 첫 충전 전압 곡선이 66호 넷째 충전 곡선과
  **모양부터 다르다**(첫 충전 초반의 높은 전압 · 이 편이 이름 붙인 첫 사이클 교란; `[해석]`). 전압 맞춤이 "규약 항" 으로 읽히려면 두 교정의 전하–전압 곡선이 규약만큼만 달라야 하는데, 첫 충전
  교정에서는 그 전제가 깨진다.
- 붕괴 구간(δ ≤0.45)만 보면 전압 맞춤 +0.033…+0.042 < 격자 맞춤 ≈0.058–0.065 — 같은 전압에서 22호 격자가 x 로 ≈0.02–0.03 더 수축해 있다(방향만; 첫 충전 전압 · 판독 ±0.01 · 두 셀 로트가 섞인다).

## 판정

**66호 x 이동 ≈0.067(NCM622) 의 원인은 이 편으로 가르지 못한다.** 이유 셋: (i) 이 편은 NCM811 뿐이다 — 22 · 66호 NCM622 쌍에 같은 조성이 없다 (ii) 이 편에 첫 사이클 교정이 없고 전처리 횟수 ·
결손이 미인쇄다 — 규약 항의 크기(22호 1.02 ↔ 66호 0.93, 전처리 결손의 행방에 따라 0 … 0.09)를 이 편이 정해 주지 않는다 (iii) 22호 교정은 첫 충전이라 전압 맞춤으로 규약 항을 떼는 방법이 서지 않는다
— 전압 곡선 자체가 사이클 번호에 걸린다.
**대신 이 편이 준 것**: ① 연구망 안의 규약이 **셋**이라는 인쇄 사실 ② 첫 사이클 교정을 **피할 이유**(격자 "delayed change" · 비가역 최대 14 %)의 인쇄 ③ 두 교정이 **모두 전처리 셀이면** 전압 맞춤
이동이 규약 항을 준다는 `[재현]`(NCM811: +0.10 ✓)과, 그때 남는 시편 항의 크기(붕괴 구간 0 … +0.03, 초반은 채널마다 +0.07…+0.17 로 갈림) — 교정을 옮겨 쓸 때 **규약 항과 시편 항을 따로 적는** 틀
([[nmc-lattice-li-content-calibration]] 67호 절).

# ★ (c) Q8 · 부피 — 전압 · 기준을 맞춘 대조 (3286 을 대신하지 않는다)

## 이 편의 `ΔV/V` (`[재현]` — 기준 = 전처리 셀 충전 첫 점 x 1.00 · `V` 101.38; 원형 격자 인쇄 0)

| 상태 | x(이 편 축) | `V` (Å³) | `ΔV/V` |
|---|---:|---:|---:|
| 4.1 V | 0.47–0.48 | 99.45–99.56 | −1.8…−1.9 % |
| 4.2 V | 0.40–0.42 | 98.51–98.84 | −2.5…−2.8 % |
| **4.3 V** | 0.31–0.33 | 95.95–96.46 | **−4.9…−5.4 %** |
| 4.4 V | 0.28–0.30 | 95.05–95.63 | −5.7…−6.3 % |
| **4.6 V + 1 h** | 0.25(표 2) | 94.26 | **−7.02 %** |
| −6 % 되는 곳 | ≈0.29 | 95.30 | ≈4.36–4.44 V |

## 대조

| 대조 대상 | 그쪽 값 · 기준 | 이 편 대응 |
|---|---|---|
| 66호 NCM811(표 S1, 넷째 충전 C/10) | 4.3 V −4.86 %(첫 행) / −4.45 %(원형) · 4.6 V + 1 h −7.35 % / −6.95 % · −6 % ≈4.42 V | 4.3 V −4.9…−5.4 % · 4.6 V + 1 h −7.02 % · −6 % ≈4.36–4.44 V — **같은 자릿수 · 같은 방향(충전 수축)**. 기준이 다르다(이 편 = 전처리 셀 첫 점, 원형 없음) |
| 62호 결론 "volume changes of nearly 6%"[31 = 3286] — 방향 0 | ≈6 % | −6 % ≈ x 0.29 ≈4.4 V(이 편) — 같은 자릿수. 3286 자신의 값 · 전압 · 기준은 **파일 31** |
| 23호 G1 · §4-2(e) — SEM 틈 폭 역산 요구(NCM811 · 등방) | 3–20 %(중앙 8–10 %) | 이 편 최대 −7.02 %(4.6 V + 1 h) — **중앙 8–10 % 는 이 편 범위 밖**(66호 NCM851005 −7.97 % 도 밖) |
| 23호 첫 충전 176 mAh g⁻¹ 을 θ = 1 로 x 에 옮기면 | 66호 축(δ₀ 1.02): δ 0.381 → **−1.3…−1.7 %**(66호 `[재현]`) | **이 편 축(x₀ 1.00): x 0.361 → −4.0 %** — **축 규약만으로 ×2.4–3**. `[해석]` 23호 셀은 신품 첫 충전이라 어느 축도 그 셀의 참 조성을 주지 않는다 — 요구치 역산은 θ(66호)와 축 규약(67호)을 둘 다 품는다 |

- `[재현]` 이방성(이 편): x 1.00 → 0.6 `Δc/c` +1.54 %(`[인쇄]` 14.469) · `Δa/a` −1.34 %(`[도표]` 2.8661 → 2.8277) · x 1.00 → 0.25 `Δc/c` −3.63 % · `Δa/a` −1.77 % — 66호 NCM811 과 같은 모양(`c` 증가 뒤 붕괴 · `a` 는 x ≈0.3 에서
  평탄).
- ⚠ 이 편은 원형 격자를 인쇄하지 않는다 — "원형 대비" 값은 이 편으로 만들 수 없다.

# ★ (d) Q1 · 곱 축퇴 — 해당 없음과 이유

- **Q1 — 없다(0/67).** 사이클 축 자료는 Fig. 1a 유지율 · 표 1 사이클당 손실 · S1(흑연 완전지 150 사이클)뿐이다. 균열 · 활성 질량 · 고립 분율 · LAM 측정 0. 접촉 어휘 0(`contact` 0 회).
- 층 하나: `[인쇄]` "the capacity fading is virtually enhanced at such conditions because overpotentials arising during cycling, e.g., due to material fracture, lower the actual cell voltage" — 액체 반쪽의
  겉보기 용량 감쇠에 **과전압(`η`) 몫**이 있다고 저자가 적는다(측정 0 · 양 0). `[해석]` 우리 3항 분해(`θ` · `η` · `LLI`)의 `η` 쪽 인쇄 표본이다.
- **곱 축퇴(`j₀` · 접촉 면적)와 63 · 64 · 65호 `R`·`C` 1단계 — 해당 없음.** EIS 0 · 면적 채널 0 · 액체 반쪽 · 사이클 축 격자 0. 억지로 채울 입력이 없다.
- 대신 처방 표 66호 경고 행("SOC 추종 상 분율 줄의 교정 조건")에 한 줄: **교정 곡선을 옮겨 쓸 때 규약 항(전압 맞춤)과 시편 항(격자 맞춤 − 전압 맞춤)을 따로 적는다 — 두 교정이 모두 전처리 셀일 때만**
  (§곱 축퇴).
- ASSB 로의 전이는 전부 `[해석]` 이다 — 이 편은 액체 반쪽 · NCM811 · BASF 전극이다.

# ★ (e) 셀 사양 · 회절 · 분광 셀 설계

| 항목 | 코인(사이클) | 파우치(operando XRD) | hXAS 셀 | sXAS 표본 |
|---|---|---|---|---|
| 양극 | BASF NCM811 전극(활물질 94 wt%) · 지름 · 적재 · 두께 **0** | 미기재([5] 위임) | 미기재 | 탈리튬 뒤 Li 셀에서 꺼낸 양극 |
| 전해질 · 분리막 | 1 M LiPF₆ EC:DMC **3:7(무게)** 250 µL · GF/D | 미기재 | 미기재 | DMC 세척 · 건조 · **손 연마** · Ar 봉입 운반 |
| 상대극 | Li 금속(Rockwood Lithium) | Li(NCM811/Li) | Li(NCM811/Li) | — |
| 온도 | 25 °C | 25 °C | 미기재 | — |
| 구속 · 압력 | 미기재 | 미기재 | 미기재 | — |
| 율 · 창 | 형성 C/10(3.0 → 4.1…4.6 V) → C/2 · 컷오프 정전압 **없음**("without potentiostatic steps") | 전처리 C/10 3.0–4.3 V(횟수 미인쇄) → C/20 3.0–4.6 V + 충전 끝 1 h 정전압 | "the same cycling conditions used for XRD" | S6 E–t: C/20 로 읽힌다(`[해석]` 충전 20.6 h) · 4.6 V 유지 ≈2.4 h |
| 측정 | MACCOR 4000 | Mo Kα₁,₂ 실험실 회절계([25]) · 2θ 5–37° · "every 150 s"(`[재현]` 쌍축 175.5 s/scan) · TOPAS-Academic V5 · `z_O` 첫값 = 원형 중성자([5]) | PETRA III P65 · 투과 · "2 mm polyimide windows" · 기준 분말 여섯 · Demeter | BESSY II RGBL · TEY(≈100 Å) · Au 박 에너지 보정 · 576 eV 연속 도약 정규화 |
| 1C 정의 | 0 | 0 | 0 | — |

- **Q5 — 해당 없음**(Li 금속 · 기준극 0).
- `[해석]` 셀 셋(코인 · 파우치 · hXAS 셀)과 표본 한 벌(sXAS)이 각각 다른 셀이다 — x 규약이 셀마다 같다는 보장이 지면에 없다(hXAS 0.84 → 0.22 · D8).

# 귀속 검사 — 22호 · 66호 · 원장 행이 이 편에 매단 것

| 인용처 | 매단 명제 | 이 편 | 판정 |
|---|---|---|---|
| **22호** ref 21 · §2-4(:168) | "c 는 x ≈ 0.5 까지 증가 후 급감(**Ni–O 전하이동**, refs 20, 21)" | 현상 ✅(`c` 최대 x ≈0.555–0.6 · 급감 < 0.5 · 두 슬랩 < 0.45 — 이 편 축) · 기구 ✅ `[인쇄]` "charge transfer between O 2p and partially filled Ni eg orbitals" · 낱말 "Ni–O" 0 회 | ✅ **선다** — ⚠ 두 단서: "x ≈ 0.5" 는 교정 규약 위의 값(세 교정이 0.45 · ≈0.5 · 0.555 에 놓는다; 전압으로는 ≈4.0 V) · 기구의 **시점**은 계산(LiNiO₂ PBE 네 점)이고 그 x = 0.25 점이 SI 로 재현되지 않는다 |
| **22호** ref 21 · 후속 표(:576) | "a·c–x **교정의 원전**(c 최대의 기구)" | 교정: NCM811 한 조성 · 22호(NCM622)는 자기 첫 사이클 교정을 썼다 — 이 편은 **첫 사이클 교정을 피해야 할 이유**를 인쇄한 쪽 · 기구: 붕괴 쪽 ✅ · 증가 쪽은 [9] Van der Ven 서사(`[인쇄]` "It is believed") | ⚠ **부분** — "c 최대의 기구" 의 원전 ✅(붕괴 쪽) · "교정의 원전" ❌ |
| **66호** [19] ① | "charging NCM cathode materials to higher states of charge (SOC) is accompanied by more pronounced changes in lattice structure.10,13,19" | `[인쇄]` "the interlayer spacing … is subjected to severe nonmonotonic changes at voltages above 4.0 V" · "increasing the cutoff voltage on charge above 4.2 V results in large structural changes" | ✅ (NCM811 한 조성) |
| **66호** [19] ② | "When most of the lithium is removed, a contraction of the interslab distance is observed and with that a decrease in lattice parameter c.19" | `h_Li-O` 2.889 → 2.767(x 0.5 → 0.25) ✅ · 그러나 같은 구간 `h_TM-O` 도 −0.120 Å(`[재현]` 항등식) — `[인쇄]` "simultaneous decrease in both slab heights" | ✅(현상) · ⚠ `c` 감소를 interslab 하나로 돌린 것은 부분 — x 0.5 → 0.25 `c` 감소의 **절반은 TM–O 층** |
| 66호 [19] 서지 | Kondrakov … Hartmann, Brezesinski(열 명) | 표제 저자 열한 명(**Janek** 마지막) | ⚠ 66호 참고문헌의 저자 누락(66호 PDF 쪽 — 우리 digest 전사는 맞다) |
| 원장 §1 행 | "`c` 붕괴 기구의 원전 후보 · Q8·Q2 · 교정 `x` 축 규약(첫 사이클인가 · δ₀)도 확인할 곳" | 기구 ✅(측정 + 계산) · 규약 ✅ 확인(전처리 셀 · 충전 첫 점 1.00 · 결손 미배정 · 첫 사이클 회피 사유 인쇄) | ✅ **흡수** — 정정 제안(wiki 밖): "원전" 은 NCM811 한 조성 · 기구의 시점은 DFT 네 점 · SI x = 0.25 기하 불일치 · 같은 연구망 세 규약 |

⚠ 시점: 이 편(2017-10-11)은 66호(2017-10-31) · 22호(2018-03)보다 앞이다 — 둘 다 이 편을 인용할 수 있고, 반대는 불가능하다.

# 인용 대조 — 우리 위키 · 원장에 원전 · 관련 digest 가 있는 것

| 이 편 인용 | 우리 호 · 원장 | 이 편이 적은 것 | 대조 · 넘길 것 |
|---|---|---|---|
| **[5] Kondrakov, Schmidt, Xu, Geßwein, Mönig, Hartmann, Sommer, Brezesinski, Janek 2017 *JPCC* 121, 3286** | 원장 ★★★(지목 23 · 62 · 66) · **3차 묶음 파일 31** | **여덟 번**: ① "capacity fading is strongly related to the mechanical disintegration of secondary particles.4,5" ② "severe nonmonotonic changes at voltages above 4.0 V vs Li+/Li.5−8" ③ "limited information on the crystallographic changes in these layers.5,10" ④ "treated only in few theoretical and experimental studies.5,9,15" ⑤ "Details on the setup as well as the description of calibration procedures can be found elsewhere.5" ⑥ "using the previously described procedure.5" ⑦ "**first cycle irreversibilities (up to 14%), resulting in partial active lithium loss and delayed change in lattice parameters in the initial charge cycle.5**" ⑧ "initial zO value … determined by neutron diffraction on pristine NCM material, as described elsewhere.5" | **지목 +1(23 · 62 · 66 · 67)** — 파일 31 에서: 첫 사이클 격자 지연의 **크기(x 로)** · operando 파우치 사양 · 교정 절차 · 중성자 `z_O` · `ΔV/V` 의 전압 · 기준(66호 넘김). 이 편은 3286 을 부피 **수치**로 인용하지 않는다 |
| [4] Ishidzu, Oka, Nakamura 2016 *SSI* 288, 176 | 원장 ★(지목 23 · 66) · **3차 묶음 파일 34** | "capacity fading is strongly related to the mechanical disintegration of secondary particles.4,5" | **지목 +1(23 · 66 · 67)** |
| [2] Noh, Youn, Yoon, Sun 2013 *JPS* 233, 121 | 원장 ☆(66호 신규) | "significant capacity fading and low structural stability at high voltages limit the stable operating range of NCM811-based cells in practical applications.2,3" | 지목 +1(66 · 67) |
| [9] Van der Ven, Aydinol, Ceder, Kresse, Hafner 1998 *PRB* 58, 2975 | 원장 0(66호 [38]) | "It is believed that lithium screens the repulsion between the oxygen planes, which should result in linear expansion of the Li-O slabs during delithiation.9" · 슬랩 높이 ↔ O 층 반발([9, 15]) | `c` 증가 서사의 근거(LiₓCoO₂ 계산) — 66호와 같은 사슬 |
| [17] Seo, Urban, Ceder 2015 *PRB* 92, 115118 | 원장 0 | "reports on mixing (overlap) between TM and oxygen bands … suggest a high degree of covalency of the TM-O bond.16,17" | 신규 후보(☆) — TM 준위 · O 띠를 보정하는 계산 방법 논문인데 이 편 계산은 기본 PBE. Bader 꺾임이 +U/혼성 범함수에서 남는지의 대조 재료 |
| [14] Petersburg … Alamgir 2012 *J. Mater. Chem.* 22, 19993 | 원장 0 | NCM111 에서 "exhaustion of nickel redox activity at high states of charge" | 저 Ni 대조(이 편은 NCM811 에서 소진 없음) |
| [7] Li J., Petibon, Glazier, Sharma, Pang, Peterson, Dahn 2015 *Electrochim. Acta* 180, 234 | 원장 0 | 비단조 층간 변화 인용(5−8) | operando **중성자**(O 위치를 직접 보는 채널) — `z_O` · 슬랩 높이의 독립 대조 후보 |
| [34] Croguennec, Pouillerie, Mansour, Delmas 2001 *J. Mater. Chem.* 11, 131 · [33] Li, Reimers, Dahn 1993 | 원장 0 | LiNiO₂ 상전이 · 고탈리튬 구조 | H2 → H3 · 붕괴의 상 분율 해석 대안 |
| [51] Antolini 2003 · [52] Kanno 1994 · [53] Xu … Tong 2017 *JMCA* 5, 874 | 원장 0 | "facile transition of layered LixNiO2 to NiO-type rock salt phases" · 산소 방출 | SI x = 0.25 기하(O–O 쌍 · Ni 이동)와 같은 방향의 인용 서사 |
| [25] de Biasi 2015 *CrystEngComm* 17, 6163 | 원장 0(66호 [20]) | 회절 장치 | 장치 원전 |
| [54] Tang, Sanville, Henkelman 2009 | 원장 0 | Bader 알고리즘 | — |

⚠ 이 편은 22호 · 66호를 인용하지 않는다(시점). 24호가 쓴 Buchberger 2015(파일 40)도 인용하지 않는다.

# 곱 축퇴 처방 — 쉰 번째 적용 (`[[assb-lampe-contact-product-degeneracy]]`)

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | EIS 0 | ❌ |
| **2단계** (18 · 25호) | + 면적을 아는 대조군 | NCM811 한 조성 · 컷오프 여섯(입자 · BET 미기재) — 면적 채널 0 | ❌ |
| **3단계-a/b** (19호) | `Ea` · `C` 상한 | 25 °C 한 점 · `C` 0 | ❌ |
| **4단계** (20호) | 시간 영역 | 0 | ❌ |
| 22호 줄 "SOC 추종 상 분율" · 66호 경고 행 | 교정 조건을 값 옆에 | **같은 연구망 세 규약 · 규약 항(전압 맞춤) ↔ 시편 항(격자 맞춤 − 전압 맞춤)** | ⚠ **경고 행 보강 한 줄** |
| 52호 줄 | 누적 결손 ↔ Li 재고 | 액체 반쪽 — Li 재고 ≫ | 해당 없음 |

⇒ **적용 불가(1단계 입력 없음).** 기록 이유: 66호 경고 행은 "교정 규약을 값 옆에 적는다" 였다. 이 편으로 그 규약의 **크기를 두 항으로 나눠 재는 방법**이 생긴다 — 두 교정이 **모두 전처리 셀**이면
전압 맞춤 이동이 규약 항(NCM811: +0.10 ≈ 1.00 − 0.90 ✓)을, 격자 맞춤 − 전압 맞춤이 시편 항(붕괴 구간 0 … +0.03, 초반 채널마다 +0.07…+0.17)을 준다. **첫 충전 교정(22호)에는 서지 않는다**
(전압 곡선 자체가 사이클에 걸린다 — 전압 맞춤 +0.157 → +0.033).

# 보류 결정 (가)(나)(다)(아)(자)(차)(타) — 이 편이 주는 근거 (결정 안 함)

원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §3-b 와 대조. **결정은 사용자 몫이다.**

| # | 결정 | 이 편 | 근거 |
|---|---|---|---|
| 가 | 29호 Q4 +0.5 유지 | 무관 | 적합 · 식별성 진단 0 |
| 나 | 38호 Q2 +0.5 유지 | **정성 메모 하나** | 38호 활성 질량 게이지는 액체 기준 곡선(전하 계수 x 축)으로 전위를 x 로 바꾼다 — 이 편 NCM811 쌍에서 **같은 연구망 두 셀의 전하–전압 곡선은 규약(0.10)만 빼면 δ ≤0.65 에서 ≈±0.01 안**(정전압 전하 0 기준)이지만(Δx 에서 상쇄), **충전 첫머리(δ 0.85–0.70)는 +0.05…+0.09 로 모양이 다르다**(상쇄 안 됨; 율 C/10 ↔ C/20 이 섞인다). 결정 재료 아님 |
| 다 | 28호 Bizeray 를 ASSB Q4 분모에 | 무관 | — |
| 아 | 35호 합성 쌍 → Roman 특징 재계산 | 무관 | ML 0 |
| 자 | 31호 ICI zenodo `R/k` 면적 소거 | 무관 | — |
| 차 | 23호 PyBaMM 면적 노브 / `j₀` 노브 분리 | 무관 | 면적 · `j₀` 채널 0 |
| 타 | Navidi 2024 digest 재점검 | 무관 | — |

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 어디 | 판정 |
|---|---|---|---|
| **D1** | ★★ `a` @ x 0.5: 본문 "2.8211(1) Å (at x(Li) = 0.5)" ↔ 표 2 **2.8221(1)** ↔ Fig. 2c `[도표]` **≈2.8207** | p. 24383 ↔ 표 2 ↔ Fig. 2c | 표 2 `V` 99.73 은 2.8221 로 재계산된다(2.8211 이면 99.66); 그림은 본문 쪽에 가깝다 — 표의 x = 0.50 행 `a` 는 그림에서 x ≈0.525 의 값 |
| **D2** | ★ `c` 최대: 초록 · 본문 "14.469(1) Å at x(Li) = 0.6" ↔ Fig. 2c 최대 14.469 @ x ≈0.555(±0.005 Å 띠 0.515–0.577) · 그림 x 0.6 은 14.459 | 초록 · p. 24384 ↔ Fig. 2c | "broad maximum" 안 — 위치 기록만 |
| **D3** | ★★ 슬랩 끝 값: 인쇄 `h_TM-O` 1.797(2) · `h_Li-O` 2.767(1) → `[재현]` 3 × 합 **13.692** ↔ `c`(0.25) **13.732(2)**(항등식 `c = 3(h_TM-O + h_Li-O)`) · Fig. 3b 끝 ≈1.806 · ≈2.776 → 13.75 ✓ · `h_Li-O` 최대 "2.889(2) Å (at x(Li) = 0.5)" ↔ 그림 최대 x ≈0.435–0.47 | p. 24384 ↔ 표 2 · Fig. 3b | 인쇄 끝 값 쌍이 같은 점의 값이 아니거나 한쪽이 최소값 — `c` 의 esd 의 20 배 |
| **D4** | ★★★ SI POSCAR x = 0.25 ↔ 표 2 DFT x = 0.25: `V` 98.63 ↔ 93.39 · `a` 2.886/2.916 ↔ 2.840 · `c` 13.62–13.64 ↔ 13.37 — 그 기하에 O–O 1.331 Å 두 쌍 · Ni 둘 Li 슬랩 안(4 배위) · S7(d) · S8(d)(−9 eV O 상태 · t2g–eg 틈 닫힘) ↔ S8 캡션 "Only slight changes in DOS … preserves its basic shape" | 표 2 · p. 24386 ↔ SI 6–13 쪽 | 기구의 시점을 정하는 점이 SI 로 재현되지 않는다(§(a')) |
| **D5** | ★★ "VDFT is smaller by up to 1.9% than … VXRD" ↔ POSCAR x = 0.25 `V` 98.63 = XRD 94.26 의 **+4.6 %** · POSCAR 로는 `V` 가 x 0.5 → 0.25 에 **+0.44 %**(실험 −5.5 %) | p. 24386 ↔ SI | D4 의 부피 판 |
| **D6** | ★★ "the results are reliable and the nonmonotonic behavior … is well reproduced … implementation issues of the relaxation procedure can be ruled out" ↔ `[재현]` `c` DFT 가 XRD 보다 2.6–4.4 % 짧고 `a` 는 0.9–1.5 % 길다 — `V` ≤1.9 % 는 상쇄 · POSCAR `c` 감소(x 0.5 → 0.25) −1.6 %(표 −3.5 % · XRD −5.0 %) | p. 24386 ↔ 표 2 · SI | 부피 일치로 신뢰를 주장했다 |
| **D7** | ★★ "XRD patterns … were collected every 150 s" ↔ S2 쌍축 `[재현]` **175.5 s/scan**(scan 0 ↔ 1.13 h) · 4.6 V 정전압 ≈20 scan 이 "1 h" 가 되려면 ≈180 s | p. 24382 ↔ S2 | 노출 150 s + 읽기 시간일 수 있다(`[해석]`) — 1C 역산에 걸린다 |
| **D8** | ★★ hXAS x **0.84 → 0.22** ↔ XRD x **1.00 → 0.255** — `[인쇄]` "under the same cycling conditions used for XRD" | Fig. 4 ↔ Fig. 2 | 출발 · 끝 x 가 다르다 — 셀 · 규약 미인쇄 |
| **D9** | ★★ `[인쇄]` "the A1 peak intensity increases nearly linearly with decreasing lithium content" ↔ S6 전단(표본 순서) 1.80 · 2.20 · 2.26 · 2.37 · 2.53 — `[해석]` 배정(#1–#5 = 0.54 · 0.30 · 0.27 · 0.25 · 0.24) 위에서 x 당 증가가 x < 0.30 에서 ×3 | p. 24386 ↔ S6 · Fig. 5 | 배정이 인쇄되지 않아 판정 보류 — "선형" 도 "비선형" 도 지면이 뒷받침하지 않는다 |
| **D10** | ★ Fig. 5 탈리튬 표본 다섯 ↔ S6 E–t 마커 자리 일곱 · 표본 여덟 · S6 4.6 V 유지 ≈2.4 h ↔ XRD 1 h | Fig. 5 ↔ S6 | 표본 · 조건 대응 미인쇄 |
| **D11** | ★★ 표 1 사이클당 손실 비 "1.75, 2, 2.25, and 3 times" ↔ Fig. 1a `[도표]` 49 사이클 유지 손실(최대점 기준) 4.2 V 대비 **≈2.0 · 3.0 · 3.5 · 4.8** | p. 24383 ↔ Fig. 1a | "capacity loss per cycle" 정의 미인쇄(G10) |
| **D12** | ★ 결론 "(E > 4.2 V vs Li+/Li and x(Li) < 0.5)" ↔ `[재현]` 이 편 operando 셀에서 x 0.5 ≈4.06 V · 4.2 V ≈ x 0.40–0.42 | p. 24387 ↔ S2 · Fig. 2 | 두 경계를 한 괄호에 넣었다 |
| **D13** | ★★ Fig. 2d/e "correlate … indicate that the structural changes are connected to redox processes" ↔ `[재현]` 연쇄 법칙 — −dc/dE = (dc/dx)(dx/dE) 가 dQ/dE 봉우리(4.217 V)에서 최대 | p. 24384 ↔ Fig. 2 | 공유 인자 dx/dE 의 상관(66호 D14 와 같은 구조) — 구조 정보는 `c(x)` 의 기울기에 있다 |
| **D14** | ★ Fig. 2c 오른축 "14.5 · 14.2 · 14.0 · 13.7" · Fig. 3b "2.15 · 2.02 · 1.88 · 1.75" / "2.93 · 2.83 · 2.72 · 2.62" 는 **등간격 눈금의 반올림 라벨**(참 14.233 · 13.967 등) | Fig. 2c · 3b | 라벨로 읽으면 `c` 를 최대 0.033 Å 잘못 읽는다 — 자료 오류는 아니다 |
| **D15** | ★ "nickel changes by 0.8 charge units … 12% difference in nickel ionic radius" ↔ `[재현]` XRD 창 Δx 0.75 · Co · Mn 고정이면 Ni 한 개당 +0.94(Shannon 선형 → 14.1 %) | p. 24385 | 결론에는 무해(15 % 와 더 가까워진다) |
| **D16** | ★ 코인 전해질 "1 M LiPF6 in ethylene carbonate and dimethyl carbonate, 3:7 by weight" — 66호의 LP30 · LP47 어느 것도 아니다 · 파우치 전해질 미기재 | p. 24382 | 기록만(교정 비교의 로트 · 전해질 항) |
| **D17** | ★ "The authors declare no competing financial interest" ↔ 저자 둘 BASF SE · 전극 · 전해질 BASF 제공 · 자금 BASF 네트워크 | p. 24387 | 선언과 소속의 병치 — 기록만(66호 D17 과 같다) |
| **D18** | ★ 66호 참고문헌 [19] 저자 **열 명**(Janek 빠짐) ↔ 이 편 표제 **열한 명** | 66호 p. 26170 ↔ 이 편 p. 24381 | 인용하는 쪽(66호)의 오기 |

# 이 편이 우리 프로젝트에 주는 것 (정리)

1. ★★★ **붕괴는 측정이고, 원인의 시점은 계산이다** — 22호가 기대는 "Ni–O(O 2p ↔ Ni eg) 전하이동" 은 이 편에 인쇄돼 있고 sXAS 가 혼성을 받치지만, "x < 0.5 에서 O → Ni" 의 **시점**은 LiNiO₂ PBE 네 점의
   Bader 꺾임 하나이고 그 x = 0.25 점은 SI 기하로 재현되지 않는다(O–O 1.331 Å · Ni 이동). 우리 쪽(Q8 · 합성 truth)에는 **현상**(NCM811 `c` 최대 ≈4.0 V · ΔV 의 77 % 가 x < 0.5 ≈4.06–4.6 V)을
   쓰고 기구 서사는 쓰지 않는다.
2. ★★★ **같은 연구망 세 교정 규약** — 22호 첫 충전 1.02 · 66호 1.02 − 결손 · 이 편 전처리 셀 1.00. 교정을 옮겨 쓸 때 **규약 항(전압 맞춤)과 시편 항(격자 맞춤 − 전압 맞춤)을 따로** 낸다 —
   NCM811 쌍: 규약 +0.10(전압 맞춤 ✓) · 시편 붕괴 구간 0 … +0.03 · 초반 채널마다 +0.07…+0.17. 첫 충전 교정(22호)에는 이 분해가 서지 않는다(전압 맞춤 +0.157 → +0.033).
   [[nmc-lattice-li-content-calibration]] 67호 절.
3. ★★ **구조 전이의 위치는 전압(같은 율 통전)으로도 적는다** — NCM811 `c` 최대는 두 교정에서 x 로 0.45 ↔ 0.555 지만 전압으로 ≈3.99–4.0 V 로 같다. 편 사이 비교는 x 보다 전압이 규약에 덜 걸린다
   (`[해석]` — 율 분극이 섞인다).
4. ★★ **`ΔV/V` 요구치의 축 규약 몫** — 23호 첫 충전 176 mAh g⁻¹ 이 66호 축으로 −1.3…−1.7 %, 이 편 축으로 −4.0 %. 66호가 보인 θ 몫(θ 0.8 → −4.2…−4.6 %)과 같은 크기라, 틈 채널로
   `ΔV/V` 를 역산할 때 θ 와 축 규약이 **같은 크기로** 섞인다.
5. ★★ **DFT 격자를 물리 사전으로 쓰지 않는다** — 이 편의 PBE LiNiO₂ 는 `V` 를 1.9 % 안에 맞추지만 `c` −4.3 % · `a` +1.5 % 의 상쇄이고, 고탈리튬 점은 O–O 결합 형성 · Ni 이동으로 이완됐다.
   합성 truth 의 양극 팽창 곡선은 측정 `V(x)`(66 · 67호)로 둔다(결정은 사용자 몫).
6. ★ **esd ≠ 산포(세 번째 표본)** — 슬랩 높이 잔차 RMS 0.004–0.006 Å ↔ esd 0.001–0.003(66호 `V` ×14–37 · 22호 D9 와 같은 방향).
7. ★ **겉보기 감쇠의 `η` 몫에 저자가 이름을 붙였다** — `[인쇄]` "overpotentials arising during cycling, e.g., due to material fracture, lower the actual cell voltage"(액체 반쪽, 양 0). 합성
   truth 에서 `θ`(고립)와 `η`(분극)를 따로 켜야 하는 이유의 인쇄 표본.
8. `[해석]` 우리 주 프로젝트(액체셀 PyBaMM)와의 접점: 반쪽전지 OCP 의 화학량 축도 통과 전하로 세고 x = 1 을 어디에 두느냐가 규약이다 — 같은 연구망 안에서 그 규약이 0.10 흔들린다는 것은,
   완전지 OCV 적합에서 양극 화학량 오프셋이 Li/P 비(곧 `LLI` 방향)로 흡수될 자리의 크기를 가늠하게 한다([[np-lip-ocv-reparametrization]] · [[fitting-degeneracy]]). 우리 쪽 수치는
   `degradation-degeneracy/docs/RESULTS*.md` 가 정본이다 — 여기서 비교하지 않는다.

# 후속 후보 (원전 우선)

참고문헌 54 편 중 우리 축(Q1 · Q2 · Q8)에 닿는 것만. **셀 열화 식별성 원전 0.**

| 서지 | ref | 왜 | 축 | 우선 |
|---|---|---|---|---|
| **Kondrakov, Schmidt, Xu, Geßwein, Mönig, Hartmann, Sommer, Brezesinski, Janek 2017 *J. Phys. Chem. C* 121, 3286–3294** | [5] | **파일 31** — 원장 ★★★ · 이 편이 여덟 번 인용: 첫 사이클 격자 "delayed change"(**크기를 x 로**) · 파우치 · 교정 절차 · 중성자 `z_O` · `ΔV/V` 의 전압 · 기준 · **지목 23 · 62 · 66 · 67** | Q1 · Q8 | ★★★(기존) |
| Ishidzu, Oka, Nakamura 2016 *Solid State Ionics* 288, 176–179 | [4] | **파일 34** — 조성별 부피 · 입자 파괴 · **지목 23 · 66 · 67** | Q8 | ★(기존) |
| Noh, Youn, Yoon, Sun 2013 *J. Power Sources* 233, 121–130 | [2] | 조성 여섯 4.3 V 사이클(66호 Fig. 10b 대조군) · **지목 66 · 67** | Q8 | ☆ |
| Seo, Urban, Ceder 2015 *Phys. Rev. B* 92, 115118 | [17] | TM 준위 · O 띠 보정 — Bader 꺾임이 +U/혼성 범함수에서 남는지 볼 방법 원전 · 원장 0 | Q8 | ☆ |
| Li J., Petibon, Glazier, Sharma, Pang, Peterson, Dahn 2015 *Electrochim. Acta* 180, 234–240 | [7] | operando **중성자** NCM 파우치 — O 위치(슬랩 높이)의 독립 채널 · 원장 0 | Q8 · Q2 | ☆ |
| Croguennec, Pouillerie, Mansour, Delmas 2001 *J. Mater. Chem.* 11, 131–141 | [34] | 고탈리튬 LiₓNi₁.₀₂O₂(x ≤0.30) 구조 — 붕괴의 상 분율 해석 대안 · 원장 0 | Q8 | ☆ |
| Petersburg, Li, Chernova, Whittingham, Alamgir 2012 *J. Mater. Chem.* 22, 19993–20000 | [14] | NCM111 O · TM 전하 보상(Ni 산화환원 소진) — 저 Ni 대조 · 원장 0 | Q8 | ☆ |

# 이 digest 가 주장하지 않는 것

- **"O 2p → Ni eg 전하이동" 기구가 틀렸다고 하지 않는다** — 측정(sXAS)이 혼성을 받친다는 것, 그리고 **시점**의 근거가 계산 네 점이라는 것까지다.
- **표 2 가 조작됐다고 하지 않는다** — SI 기하로 x = 0.25 행이 재현되지 않는다는 것까지다. Bader 전하를 어느 기하로 셌는지는 지면에 없다.
- **실제 NCM811 에서 x = 0.25 에 O–O 결합 · Ni 이동이 생긴다고 하지 않는다** — SI 에 실린 LiₓNiO₂ PBE 기하(Li 배열 하나)의 성질이다.
- **66호 x 이동(NCM622)의 원인을 정했다고 하지 않는다** — 이 편으로 못 가른다. NCM811 쌍의 규약 항 · 시편 항은 **그 쌍**의 `[재현]` 이고, 시편 항은 정전압 전하(미인쇄)에 따라 0 … +0.03 이다.
- **전압 맞춤이 늘 규약 항을 준다고 하지 않는다** — 두 교정이 전처리 셀 · 비슷한 율일 때의 근사이고(C/10 ↔ C/20 분극이 섞인다), 첫 충전 교정에는 서지 않는다.
- **S6 표본 배정 · "nearly linearly" 반박을 확정하지 않는다** — 배정은 E–t 마커와 전단 값의 짝에서 읽은 우리 추론이다(마커 자리 7 ↔ 표본 8).
- **23호 틈 요구치를 이 편 값으로 닫았다고 하지 않는다** — 액체 반쪽 · 전처리 셀 · 다른 로트이고, 23호 셀의 참 조성은 어느 축도 주지 않는다.
- **SI PDF 를 저자 원본과 같은 바이트로 보지 않는다** — 메타데이터가 말하는 것(activePDF 변환 · 2017-09-07 생성 · 2026-09-28 내려받기 표지)까지다.
- 우리 파이프라인(`degradation-degeneracy/`) 수치와 비교하지 않는다 — 우리 쪽 수치는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본이다.
- 인용 원전([5] 3286 · [4] · [2] · [9] · [17] · [7] · [14] · [34])은 열람하지 않았다. 파일 31(3286)은 이 세션 업로드 목록에 있으나 **읽지 않았다**(다음 편).
