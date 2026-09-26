# 개별 기상성장 탄소나노섬유(VGCNF) 17가닥의 탄성률 6–207 GPa 와 벽 구조 — AFM 3점 굽힘 · FIB Pt 양단고정 · HRTEM — Lawrence, Berhan, Nadarajah (ACS Nano 2008)

> slug `lawrence2008_single_vgcnf_elastic_modulus_morphology` · DOI `10.1021/nn7004427` · type `experiment (single-nanofibre AFM three-point bending, FIB Pt-clamped, + HRTEM wall morphology)` · PDF `628309c4-nn7004427.pdf` · digested `2026-09-26` · status ✅

> 본문 7 pp = ACS Nano **2**(6) (2008) **1230–1236** (접수 2007-12-21 · 승인 2008-04-28 · 온라인 2008-05-10).  **SI 없음** — 본문 7쪽 전수에서 "Supporting Information" 문구 0 건.
> **이 카드의 "p." 는 저널 쪽** (PDF 쪽 n = 저널 p. 1229 + n).
> 그림 7 + Table 1 = **8장 전부** `litdb/figures/lawrence2008_single_vgcnf_elastic_modulus_morphology/` — **8장 모두 손으로 다시 잘랐다**
> (자동 크로퍼는 Fig. 2 를 놓쳤고 · Fig. 4 윗부분을 자르고 본문 단과 합쳤고 · Table 1 은 쪽 전체를 잡았다 — §5 끝 크롭 메모).
> 서지는 PDF 원문(첫 쪽 머리·꼬리)으로 확인했다: 검색 요약의 제목 · 저자 · 권호 · DOI 와 **일치**.
>
> **계기**: 원고 SI Table S2 의 *"VGCF Young's modulus = 10 GPa"* 행에 출처가 없다 (공저자 질문).  이 값은 2026-06-24 커밋 `862a61833`
> (작업 브랜치) 에서 MPM 첨가제 재료점을 처음 넣을 때 *"VGCF medium-stiff E10/sigma_y2 (keeps fibre shape, elastic bend)"* 로 들어온
> **모델 선택**이고, 원장 `CL-42` 는 *"VGCF (10.0, 0.30) … 변경 없음"* 으로만 적는다 — 근거 문헌 없음.  정본 카드
> `endo2001_vgcf_basic_properties_battery_applications` 의 Fig. 6 영역(≈ 110–310 GPa)은 10 GPa 를 뒷받침하지 못한다.
> 검색 요약이 *"개별 탄소나노섬유 6–207 GPa"* 라고 해서, 이 논문으로 표에 *"10 GPa · Ref. [Lawrence] (측정 범위 안)"* 을 걸 수 있는지
> **원문으로 판정**하는 카드다.  ⇒ 답은 §0.

---

## 0. ★ 판정 — "10 GPa · Ref. [Lawrence]" 를 쓸 수 있나 (2026-09-26 PDF 원문 대조)

### 0-1. 확인값 표

| 질문 | 확인값 | 근거 (쪽 · 그림 · 표) | 등급 |
|---|---|---|---|
| **서지** | J. G. Lawrence, L. M. Berhan, A. Nadarajah, *"Elastic Properties and Morphology of Individual Carbon Nanofibers"*, **ACS Nano 2008, 2(6), 1230–1236**, DOI **10.1021/nn7004427** | p. 1230 머리 · 꼬리 (*"10.1021/nn7004427"*, *"VOL. 2 ▪ NO. 6 ▪ 1230–1236 ▪ 2008"*) | stated |
| **측정 범위** | **6 – 207 GPa** | 초록 p. 1230: *"…the elastic modulus which ranged from 6 to 207 GPa."* · Table 1 최소 = fibre 5 (**6 ± 0.2**) · 최대 = fibre 8 (**207 ± 1**) | **stated** — 검색 요약의 "6–207" 은 원문과 일치 |
| **몇 가닥** | **17 가닥**, 가닥마다 **≥ 6 회** 굽힘 | p. 1232: *"…multiple bend tests for 17 different nanofibers are reported in Table 1"* · *"For each individual fiber, at least six bend tests were performed"* | stated |
| **10 GPa 근처 (5–20 GPa)** | **3 가닥**: fibre 5 = **6 ± 0.2** · fibre 16 = **13 ± 0.6** · fibre 9 = **20 ± 0.4** GPa.  **5–15 GPa 는 2 가닥** (5, 16).  **10 ± 3 GPa 안은 0 가닥** | Table 1 (p. 1234) | 값 = stated · 개수 = DERIVED |
| 그 3 가닥의 형태 | **5**: D 325 · d 205 · t 60 nm · θ **58°** (측정된 14 가닥 중 최대) · t_in 50 / t_out **10** nm · t_out/t **0.17** (최소) · L 6.2 µm<br>**16**: D **470** (최대) · d 260 · t **105** nm · L 8.2 µm · θ · t_in · t_out **미측정** (Table 1 각주 a: 벽이 두꺼워 해상 불가)<br>**9**: D 260 · d 170 · t 45 nm · θ 30° · t_in 35 / t_out **10** nm · t_out/t 0.22 · L 5.9 µm | Table 1 | stated |
| 공통점 | **셋 다 D ≥ 260 nm.**  형태가 잰 둘(5, 9)은 **외벽 10 nm 로 얇고 속이 넓다** (d/D ≈ 0.63 · 0.65) | Table 1 | DERIVED |
| 분포 | 중앙값 **55** · 산술평균 65.8 · 기하평균 46.5 GPa (n = 17).  **10 GPa 보다 큰 가닥 16/17** · ≤ 100 GPa 인 가닥 **14/17** | Table 1 | DERIVED |
| **우리 섬유 직경대 (D ≤ 200 nm, n = 9)** | **23 – 207 GPa** (중앙값 81) — **10 GPa 는 이 9 가닥 전부보다 낮다** | Table 1 fibres 1 · 3 · 4 · 7 · 8 · 10 · 12 · 13 · 14 (D 115–198 nm) | DERIVED |
| **저자가 낮은 값을 설명하는 방식** | ① 외벽(무질서층)이 얇으면(t_out/t < 0.5) 벽 **전체** 단면으로 나눈 E 가 낮게 나온다 — *"the correct value of E for the load bearing parts of the nanofiber will be much larger than that reported in Table 1"* (p. 1235)<br>② t > 80 nm 두꺼운 섬유는 *"~25 GPa"* 평탄역 — *"closer to those of low grade carbon fiber"*, *"mostly consists of turbostratic graphene layers"* (p. 1235) | p. 1234–1235 | stated |
| **외벽-단독 재계산 E′ (Fig. 6b)** | 14 가닥 **≈ 23 – 234 GPa**.  fibre 5 의 6 GPa → **E′ ≈ 23 GPa**, fibre 9 의 20 → **≈ 60**.  ⇒ **저자가 더 적절하다고 한 해석에서는 10 GPa 근처 섬유가 0 이다** (fibre 16 은 t_out 미측정이라 E′ 없음) | Fig. 6b 디지털 판독 + 재구성식 (§3-3) | figure-read ≈ · 재구성 DERIVED |
| **시료** | **Pyrograf III** carbon nanofibers, *"obtained from Applied Science Inc. (Cedarville, Ohio)"* — **등급 미기재** (PR-24 는 *"thinner grade nanofibers are preferred … such as the PR-24 grade"* 라는 **예시로만** 등장, 시험 등급이라는 말 없음) · **열처리 여부 미기재** | p. 1231 · p. 1235 | stated / **n/a** |
| **구조** | **원추형(conical) 섬유**: 질서 있는 내벽(원추 그래핀) + 무질서 외벽 + 속빈 코어 (Fig. 3).  저자 서론: 원추형 섬유는 *"inner layer … perfect cone-helix structure and an outer layer … imperfect or disordered multiwall nanotube-like structure"*, **열처리하면** *"the outer layer acquires a perfect multiwall nanotube structure and the inner layer acquires a segmented stacked cone structure"* | Fig. 3 캡션 · p. 1230 | stated.  ⚠ 시료가 **비열처리(as-grown) 형태와 일치**한다는 것은 **우리 추론** |
| **측정법** | Cu **2000 mesh TEM 격자**의 사각 틈 위에 걸친 섬유 → 양끝 **FIB Pt 패드 200 nm** → AFM **3점 굽힘** (중앙 하중, 최대 90 nN, 1 µm/s, 캔틸레버 k = **5 N/m 제조사 공칭값**) → **양단고정보** 식 **F = 192EI·δ/L³** (Eq. 1) · **중공 원형 단면** 가정 · HRTEM 으로 D · d · θ · t_in · t_out (±3 nm) | p. 1231–1233 · p. 1235–1236 · Eq. 1 · Fig. 7 | stated |

### 0-2. 판정

**⛔ 출처 칸에 `10 GPa · Ref. [S(Lawrence)]` — 불가.**
**△ `Assumed` 를 유지하고 각주에서 범위를 참조 — 조건부 가능.**

불가 이유 (다섯 겹):
1. **논문은 10 GPa 를 준 적이 없다.**  17 가닥 중 15 GPa 미만은 2 가닥(6 · 13)뿐이고 중앙값은 55 GPa, 10 GPa 보다 큰 가닥이 16/17.
2. **그 2 가닥은 저자 스스로 "겉보기 값이 낮게 나오는 형태" 로 분류한 섬유다** — fibre 5 는 외벽 비율 0.17 (저자: load-bearing 부분의 참값은 *"much larger"*, 외벽-단독 재계산 E′ ≈ 23 GPa) · fibre 16 은 t = 105 nm 의 두꺼운 섬유 = *"~25 GPa"* 평탄역 그룹 (저자 해석: t > 80 nm 무리는 *"mostly consists of turbostratic graphene layers"* — 가닥별 확인이 아니라 무리 전체에 대한 추정).
3. **우리 직경대와 안 겹친다** — 모델 VGCF Ø 0.15 µm 와 가까운 D ≤ 200 nm 9 가닥은 **23–207 GPa** 로, 10 GPa 는 그 전부보다 낮다.  10 GPa 근처 셋은 모두 **D ≥ 260 nm**.
4. **재료가 다르다** — Pyrograf III (Applied Science Inc.), 등급 · 열처리 미기재, 형태는 저자가 **비열처리** 원추형 섬유로 묘사하는 구조.  우리 VGCF 는 Showa Denko 제품(흑연화로 다뤄 왔으나 공급사 데이터시트 원본 대기 — §7).  저자 자신이 *"열처리하면 외벽이 완전한 MWNT 구조가 된다"* 고 적었으므로 흑연화 섬유의 하중 지지 외벽은 **여기 값보다 뻣뻣할 방향**이다 (방향만 — 이 논문은 흑연화 섬유를 재지 않았다).
5. **값의 종류가 다르다** — 이 논문의 E 는 *"중공 벽 단면을 가정한 굽힘(flexural) 겉보기 탄성률"* 이고, 우리 10 GPa 는 *"MPM 섬유 재료점 Lamé 상수의 유효 강성"* (모델 입력) 이다.

조건부 가능 이유:
- 초록의 **"6 to 207 GPa" 는 stated** 이고, 개별 VGCNF 실측값이 **한 자릿수 GPa 에서 수백 GPa 까지 형태에 따라 퍼진다**는 사실 자체는 인용할 가치가 있다.
- ★ 더 쓸모 있는 읽기: **우리 민감도 창 1–100 GPa (09-25, h0) 가 이 17 가닥 중 14 가닥을 덮는다** (DERIVED).  즉 이 논문은 10 GPa 의 **출처가 아니라**, *"결과가 E_VGCF 에 둔감하다고 보인 창이 실측 단섬유 산포의 대부분을 덮는다"* 는 **근거**로 쓴다.
- 창 밖으로 남는 것: 이 논문의 3 가닥(105 · 160 · 207 GPa) + 흑연화 VGCF 의 ≈ 10² GPa (Endo 2001 Fig. 6 영역).  ⇒ *"> 100 GPa 는 미시험 외삽"* 한정어는 **그대로 남는다**.

### 0-3. 원고 문구 제안

**(A) 권장 — 표 칸은 그대로, 각주 ᵍ 만 보강** (작업 브랜치 `docs/reviews/si_table_response_20260925.md` 의 현 ᵍ 문안을 확장):
- Table S2 행 (현행 유지): `VGCF Young's modulus · 10 · GPa · Assumedᵍ`
- 각주:
> ᵍ Effective modulus assigned to the sub-grid fibre material points in the MPM compaction (a model input, not a measured VGCF property).
> Varying it from 1 to 100 GPa changed the compacted porosity by 0.18 percentage points and the electronic conductivity by ≤ 0.25 %
> (Supplementary Table S(new)).  For reference, AFM three-point bending of individual vapour-grown carbon nanofibres gave apparent moduli
> of 6–207 GPa (median 55 GPa; 14 of the 17 fibres ≤ 100 GPa) [S(Lawrence)], and tensile moduli of graphitized vapour-grown carbon fibres
> are of order 10² GPa [S(Endo)], above the tested range.

**(A′) 짧은 판**:
> … For reference, individual vapour-grown carbon nanofibres show apparent bending moduli of 6–207 GPa [S(Lawrence)], and graphitized
> vapour-grown carbon fibres are of order 10² GPa [S(Endo)].

**(B) 표 칸에 꼭 Ref 를 넣어야 한다면 (차선)**: `Assumed (cf. 6–207 GPa for single VGCNFs [S(Lawrence)])ᵍ` — **각주 ᵍ 없이 이 칸만 쓰는 것은 금지** (범위만 보이면 "측정값" 으로 읽힌다).

참고문헌 항목 (원문 확인판):
> J. G. Lawrence, L. M. Berhan, A. Nadarajah, Elastic Properties and Morphology of Individual Carbon Nanofibers, *ACS Nano* **2** (2008) 1230–1236. https://doi.org/10.1021/nn7004427

⛔ **쓰면 안 되는 문장**:
- `10 GPa · Ref. [S(Lawrence)]` (출처 칸 단독) — 논문에 10 GPa 가 없다.
- *"The Young's modulus of VGCF was measured to be 6–207 GPa"* — 측정 대상은 Pyrograf III (등급 · 열처리 미기재) 이지 우리 VGCF 가 아니다.
- *"10 GPa lies within the measured range"* 를 한정어 없이 — 그 아래는 1 가닥(6), 우리 직경대(D ≤ 200 nm)에는 0 가닥.
- *"the modulus of (thick) vapour-grown carbon nanofibres is 25 GPa"* 를 일반값으로 — t > 80 nm **세 가닥(32 · 13 · 25 GPa)** 의 평탄역 서술일 뿐.
- *"Lawrence et al. measured fibres of ~10 GPa"* — 6 과 13 이지 10 은 없다.
- *"Lawrence et al. tested PR-24"* — 시험 등급은 적혀 있지 않다.

### 0-4. 리뷰어가 물을 때의 한 줄

> *"10 GPa is an assumed effective stiffness for the MPM fibre material points, not a measured VGCF value; individual vapour-grown carbon
> nanofibres span 6–207 GPa (Lawrence et al., ACS Nano 2008) and graphitized fibres are of order 10² GPa (Endo et al., Carbon 2001), and our
> results change by only 0.18 %p in porosity and ≤ 0.25 % in σ_e between 1 and 100 GPa — a window that covers 14 of the 17 single-fibre values."*

한국어: *"10 GPa 는 MPM 섬유 재료점의 가정 유효강성이지 VGCF 실측값이 아니다.  개별 VGCNF 실측은 형태에 따라 6–207 GPa 로 퍼지고 흑연화 섬유는
10² GPa 급이며, 1–100 GPa (그 17 가닥 중 14 가닥을 덮는 창) 에서 우리 결과는 porosity 0.18 %p · σ_e 0.25 % 이내로만 움직인다."*

---

## 1. 한 줄 요약

기상성장 탄소나노섬유(**Pyrograf III**) 를 한 가닥씩 **TEM 격자 틈 위에 걸치고 양끝을 FIB Pt 패드로 고정**한 뒤, **같은 섬유**를 AFM 으로 3점 굽힘하고
HRTEM 으로 내 · 외경 · 원추각 · 내/외벽 두께를 재서, **17 가닥의 탄성률 6–207 GPa 를 형태와 1:1 로 짝지어** 보고한 방법 논문.
외벽(무질서층) 비율이 크면(t_out/t ≥ 0.5) E 가 크고, 벽이 두꺼울수록 E 가 급감하며, t > 80 nm 에서는 ~25 GPa 로 평탄해진다 —
*"외벽 중 내벽에 가까운 더 질서 있는 층이 강성을 진다"* 는 해석.  **값 하나가 아니라 형태에 따라 두 자릿수 퍼지는 분포**를 준다는 것이 핵심이다.

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **Joseph G. Lawrence**† · **Lesley M. Berhan**‡ · **Arunan Nadarajah**†\* (†Dept. Chemical & Environmental Engineering · ‡Dept. Mechanical, Industrial & Manufacturing Engineering, **University of Toledo**, Ohio 43606; \*교신 nadarajah@utoledo.edu) | *ACS Nano* **2**(6), **1230–1236** (2008) · 접수 2007-12-21 · 승인 2008-04-28 · 온라인 2008-05-10 | **10.1021/nn7004427** | **Pyrograf III VGCNF** (Applied Science Inc.) 단섬유 — 황화물 · 전극 · 복합체 **0** | **실험** (단섬유 AFM 3점 굽힘 + FIB + HRTEM).  모델 · 시뮬레이션 **0** |

- 자금: Army Research Office DAAD19-03-1-0012 · W911NF-05-1-0542.  TEM · FIB 분석 협력: Univ. Michigan EMAL (Kai Sun, Haiping Sun).
- 참고문헌 27.  원추형 섬유 구조 해석의 선행 = 같은 저자들의 HRTEM 구조변환 논문 (Ref. 10: *J. Nanopart. Res.*, 2007-12-18 온라인, DOI 10.1007/s11051-007-9341-4) · Eksioglu & Nadarajah, *Carbon* 44 (2006) 360 (Ref. 9).
- 장비: FEI Nova Nanolab FIB · JEOL 300 kV LaB₆ TEM · Digital Instruments Multimode AFM + Nanoscope IIIa (pp. 1231–32).

## 3. 핵심 물성 (수치)

### 3-1. ★ Table 1 전수 (p. 1234 · stated · 렌더 이미지와 한 칸씩 대조 완료) + 우리 유도 열

stated 열: L (지지점 간 거리) · D (외경) · d (내경) · t (벽 두께) · E · θ (원추각) · t_in · t_out · t_out/t.  치수 ± 는 전부 ±3 nm (p. 1233).
**DERIVED 열** (논문에 없음): (D−d)/2 · L/D · E′ 재구성 (§3-3) · E′ Fig. 6b 판독 · k_fibre = 192EI/L³ (중공 I, §4-5) · ±3 nm 치수오차의 E 전파(%).

| # | L (µm) | D (nm) | d (nm) | t (nm) | **E (GPa)** | θ (°) | t_in | t_out | t_out/t | (D−d)/2 | L/D | E′ 재구성 | E′ 판독 ≈ | k_fibre (N/m) | 치수오차 → E |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 4.8 | 185 | 75 | 55 | **81 ± 6** | 24 | 20 | 35 | 0.64 | 55.0 | 25.9 | 93 | 93 | 7.9 | ±6.7 % |
| 2 | 7.1 | 295 | 152 | 70 | **37 ± 3** | 44 | 35 | 35 | 0.50 | 71.5 | 24.1 | 51 | 51 | 6.9 | ±4.4 % |
| 3 | 4.9 | 170 | 73 | 50 | **93 ± 8** | 40 | 25 | 25 | 0.50 | 48.5 | 28.8 | 124 | 124 | 6.0 | ±7.3 % |
| 4 | 7.3 | 174 | 92 | 45 | **160 ± 7** | 41 | 20 | 25 | 0.56 | **41.0** | 42.0 | 221 | 219 | 3.3 | ±7.6 % |
| **5** | 6.2 | **325** | 205 | 60 | **6 ± 0.2** | **58** | 50 | **10** | **0.17** | 60.0 | 19.1 | 23 | 23 | 2.2 | ±4.5 % |
| 6 | 8.3 | 227 | 145 | 40 | **95 ± 9** | 19 | 20 | 20 | 0.50 | 41.0 | 36.6 | 142 | 142 | 3.5 | ±6.6 % |
| 7 | 4.3 | 195 | 67 | 65 | **23 ± 2** | 39 | 50 | 15 | 0.23 | 64.0 | 22.1 | 49 | 49 | 3.9 | ±6.2 % |
| 8 | 9.2 | 115 | 52 | 30 | **207 ± 1** | 20 | 10 | 20 | 0.67 | 31.5 | 80.0 | 234 | 234 | 0.42 | ±10.9 % |
| **9** | 5.9 | **260** | 170 | 45 | **20 ± 0.4** | 30 | 35 | **10** | 0.22 | 45.0 | 22.7 | 60 | 60 | 3.4 | ±5.9 % |
| 10 | 5.1 | 198 | 76 | 61 | **60 ± 4** | 40 | 22 | 39 | 0.64 | 61.0 | 25.8 | 68 | 68 | 6.4 | ±6.2 % |
| 11 | 8.3 | 230 | 80 | 75 | **37 ± 0.6** | 41 | 23 | 52 | 0.69 | 75.0 | 36.1 | 40 | 40 | 1.7 | ±5.3 % |
| 12 | 5.4 | 184 | 124 | 30 | **69 ± 5** | 40 | 20 | 10 | 0.33 | 30.0 | 29.3 | 148 | 148 | 3.8 | ±8.6 % |
| 13 | 3.7 | 176 | 84 | 46 | **105 ± 9** | 40 | 22 | 24 | 0.52 | 46.0 | 21.0 | 138 | 138 | 17.8 | ±7.2 % |
| 14 | 2.5 | 153 | 50 | 52 | **55 ± 4** | 30 | 30 | 22 | 0.42 | 51.5 | 16.3 | 74 | 74 | 18.0 | ±7.9 % |
| 15 | 5.9 | 450 | 190 | 130 | **32 ± 0.7** | — | — | — | — | 130.0 | 13.1 | — | — | **58.3** | ±2.8 % |
| **16** | 8.2 | **470** | 260 | **105** | **13 ± 0.6** | — | — | — | — | 105.0 | 17.4 | — | — | 9.8 | ±2.9 % |
| 17 | 8.3 | 315 | 65 | 125 | **25 ± 0.6** | — | — | — | — | 125.0 | 26.3 | — | — | 4.1 | ±3.8 % |

- Table 1 각주 a (stated): *"Here θ, t_in and t_out were not measured for the last three nanofibers due to large values of t which limited the resolution."*
- 굵은 행 = 10 GPa 근처 (5–20 GPa) 세 가닥.
- ⚠ fibre 4 만 **t = 45 (= t_in + t_out) ≠ (D−d)/2 = 41** — Fig. 6 은 41 자리에 찍혀 있다 (§3-3 · §8-비판 ⑧).  나머지 13 가닥은 반올림 안에서 셋이 같다.
- E 의 ± 는 **같은 섬유 ≥ 6 회 굽힘의 표준편차(반복성)** 뿐이다 — 치수 ±3 nm 가 D⁴ · d⁴ 로 전파되는 오차(맨 오른쪽 열, 2.8–10.9 %)는 **표에 반영되지 않았다** (예: fibre 8 은 207 **± 1** 로 적혔지만 직경 오차만으로 ±11 %).

### 3-2. 요약 통계 (전부 DERIVED — Table 1 에서 셈)

| 묶음 | n | E 범위 (GPa) | 중앙값 | 비고 |
|---|---|---|---|---|
| 전체 | 17 | 6 – 207 | **55** | 평균 65.8 · 기하평균 46.5 |
| t_out/t ≥ 0.5 (1, 2, 3, 4, 6, 8, 10, 11, 13) | 9 | 37 – 207 | 93 | 저자의 "고E 영역" |
| t_out/t < 0.5 (5, 7, 9, 12, 14) | 5 | 6 – 69 | 23 | *"fewer nanofibers … similar trend although … less pronounced"* (p. 1234) |
| t > 80 nm, 형태 미측정 (15, 16, 17) | 3 | 13 – 32 | 25 | 저자의 *"~25 GPa"* 평탄역 (평균 23.3) |
| **D ≤ 200 nm** (1, 3, 4, 7, 8, 10, 12, 13, 14) | 9 | **23 – 207** | 81 | ★ 우리 섬유 직경대 |
| D 227–230 nm (6, 11) | 2 | 37 – 95 | — | |
| D ≥ 260 nm (2, 5, 9, 15, 16, 17) | 6 | **6 – 37** | 22.5 | 10 GPa 근처 셋이 전부 여기 |

- 개수: E ≤ 15 GPa **2** · 5–20 GPa **3** · ≤ 25 GPa **5** · ≤ 100 GPa **14** · > 100 GPa **3** (105 · 160 · 207).
- 순위상관 (Spearman, DERIVED): **E–D −0.79** · E–t −0.65 · E–(d/D) +0.05.  log–log 기울기 E ∝ D^−1.86 (r = −0.76).
  ⚠ 저자는 *"the most important parameter is the wall thickness t"* (p. 1233) 라고 하지만, 이 17 가닥 표에서는 **외경 D 가 E 와 더 강하게 순위상관**한다.
  t 와 D 는 서로 묶여 있고 (굵은 섬유가 벽도 두껍다), n = 17 · 한 배치라 **어느 것이 원인인지 이 자료로 가를 수 없다**.

### 3-3. 외벽-단독 재계산 E′ (Fig. 6b) — 식 재구성 (DERIVED)

- 저자 (p. 1234): *"it may be more appropriate to calculate E assuming that the load is entirely taken up by the outer wall"* — **식은 본문에 없다**.
- ★ **재구성**: **E′ = E · (D⁴ − d⁴) / [D⁴ − (d + 2·t_in)⁴]** — 벽 전체 단면의 I 로 구한 E 를 **외벽 고리(내경 d + 2t_in ~ 외경 D)** 의 I 로 다시 나눈 것.
  이 식이 **Fig. 6b 14 점 전부를 −1.8 ~ +0.3 GPa 안에서 재현**한다 (§3-1 표의 두 E′ 열).
  대안 D⁴ − (D − 2t_out)⁴ 는 fibre 4 에서 199 (판독 219) · fibre 8 에서 242 (판독 234) 로 어긋난다 — Table 1 의 t 와 (D−d)/2 가 다른 가닥에서 두 식이 갈린다.
- E′ 범위 **≈ 23 – 234 GPa** (figure-read).  낮은 쪽: fibre 5 ≈ 23 · 11 ≈ 40 · 7 ≈ 49 · 2 ≈ 51 · 9 ≈ 60 GPa.
- 저자 결론 (p. 1234): *"it is clear that the t_out/t < 0.5 data and the t_out/t ≥ 0.5 data now match more closely"* — 판독상 같은 t 에서 열린 원이 여전히 아래에 있다
  (t ≈ 45 nm: 열린 원 fibre 9 ≈ 60 vs 채운 원 fibre 13 ≈ 138).  **"더 가까워졌다"** 이지 **"겹친다"** 가 아니다.

### 3-4. 그 밖의 수치 (stated)

| 항목 | 값 | 쪽 |
|---|---|---|
| 치수 불확도 | **±3 nm** (가닥마다 ≥ 6 점 측정의 평균 변동 — 기기가 아니라 **섬유 자체의 불균일**) | p. 1233 |
| 종횡비 | 본문 *"between 10 and 20"* ⇒ 보 이론 유효 · 전단 무시 | p. 1232 |
| ↳ Table 1 로 셈 (DERIVED) | L/D = **13 – 80** — 본문 서술과 **불일치** (13/17 가닥이 20 초과) | Table 1 |
| 고하중 시험 | 두꺼운 외벽 섬유 **840 nN** 에서 접촉점 균열, 외벽 지지로 형태 유지 · 얇은 외벽 섬유 **190 nN** 에서 파단 (Fig. 5) | p. 1233 |
| 굽힘 조건 | 최대 하중 **90 nN** · 속도 **1 µm/s** · 중앙 하중 · 캔틸레버 **k = 5 N/m** *"(datum supplied by the manufacturer)"* | p. 1235 |
| 원추각 θ | **19 – 58°** (14 가닥) | Table 1 |
| 외경 D · 내경 d · 벽 t | D **115 – 470** · d **50 – 260** · t **30 – 130** nm | Table 1 |
| 지지점 간 거리 L | **2.5 – 9.2 µm** (FIB 전자빔 영상으로 측정) — **섬유 길이 아님** | Table 1 · p. 1232 |
| 인용 비교값 | SWCNT/MWCNT 이론 최대 E ≈ **1 TPa** · 인장강도 **150 GPa** · Uchida 2006 (Ref. 22) 계산 복합 E **775 GPa (완전 흑연) → 110 GPa (난층 외층)** · Nakajima 2006 (Ref. 23) TEM 내 MWCNT **1.23 TPa** | p. 1231 |

### 3-5. 섬유별 겉보기 굽힘 강성 k_fibre (DERIVED)

- Eq. 1 로 역산 k_fibre = 192EI/L³ (I = π(D⁴ − d⁴)/64): **0.42 N/m (fibre 8) ~ 58 N/m (fibre 15)**, 캔틸레버 5 N/m 대비 **0.08 ~ 11.7 배**.
- 섬유가 캔틸레버보다 훨씬 뻣뻣하면(fibre 15: 11.7 배 · 13, 14: 3.6 배) δ = ΔZ − ΔZc 가 **큰 두 수의 작은 차**가 되어 작은 오차가 증폭된다.
  논문은 이 비를 다루지 않는다 (§8 비판 ⑤).  10 GPa 근처 셋의 비는 0.45 (5) · 0.69 (9) · 1.97 (16) — **극단 영역은 아니다**.

---

## 4. 측정 방법 ★ (시뮬레이션 0 — 모든 값이 "어떤 종류의 값" 인지 가르는 자리)

### 4-1. 시료 (p. 1230–1231)
- **Pyrograf III** carbon nanofibers, *"obtained from Applied Science Inc. (Cedarville, Ohio)"* — 에탄올에 초음파 분산.  **등급 · 열처리 · 배치 정보 없음**.
- 기상성장 VGCNF 일반 (서론): *"synthesized in a continuous reactor with floating catalysts employing a variety of hydrocarbon sources"* (Refs. 1, 2) — **부동촉매 연속 반응기**.
- 구조 분류 (서론, Refs. 9, 10): **원추형(conical)** 섬유가 다수 = 내벽 *"perfect cone-helix"* + 외벽 *"imperfect or disordered multiwall nanotube-like"*;
  **대나무형(bamboo)** 은 소수 = 마디 구조, 나노튜브에 가까움.  **열처리** 시 원추형의 외벽 → 완전한 MWNT, 내벽 → *"segmented stacked cone"*.
  ⚠ *"stacked-cup / cup-stacked"* 는 **이 논문의 용어가 아니다** (Ref. 7 Endo 2002 제목에만 등장).  이 논문은 *"conical"* · *"cone-helix"* · *"stacked cone"* 을 쓴다.
- 시험 대상 = **원추형 섬유만** (p. 1231: *"Even if we restrict the study to conical nanofibers…"*, Table 1 은 원추각을 가진다).

### 4-2. 섬유 걸치기 · 고정 (pp. 1231–32, Fig. 1 · Fig. 7)
- 현탁액 한 방울을 **Cu 2000 mesh TEM 격자**에 떨어뜨림 → 광학현미경으로 **사각 틈을 가로지른 섬유**를 찾음 (Fig. 1a: 가운데 틈을 **대각선으로**).
- **FEI Nova Nanolab FIB** 로 섬유 양끝에 **200 nm 두께 Pt 패드** 증착 (Ref. 24) — *"This ensured that the suspended portion of the nanofiber was securely attached to both ends of the gap"*.
- ⇒ 경계조건 = **양단고정(clamped–clamped)** 으로 **가정** (Eq. 1).  고정의 강성 · 미끄럼을 따로 검증한 자료는 없다.
- ⚠ 기판은 **실리콘 트렌치가 아니라 TEM 격자의 틈**이다 — 그래서 **같은 섬유를 TEM 으로 볼 수 있다** (이 방법의 요점).

### 4-3. 형태 측정 (HRTEM, p. 1232–1233, Fig. 2 · Fig. 3)
- **JEOL 300 kV LaB₆ TEM**.  걸친 구간의 여러 지점에서 d · D 를 재서 평균.  원추형 섬유는 **원추각 θ · 벽 두께 t · 질서 내벽 두께 t_in · 무질서 외벽 두께 t_out** 도 측정.
- 치수 불확도 **±3 nm** — *"the uncertainty in the measurements is no longer due to the instruments, but due to nonuniformities in the nanofibers themselves"*.
- AFM 영상에서 직경을 읽는 선행법(팁 모양 합성곱 → 역합성곱 오차)을 **TEM 직접 측정으로 대체**한 것이 이 논문의 첫째 개선점.
- 지지점 간 거리 L 은 FIB 의 전자빔 영상으로 기록.

### 4-4. 3점 굽힘 (AFM, p. 1232 · p. 1235–1236, Fig. 4 · Fig. 7)
- **Digital Instruments Multimode AFM + Nanoscope IIIa**, tapping mode 로 같은 섬유를 다시 찾은 뒤 **중앙(midspan)** 을 탐침으로 누름.
- 최대 하중 **90 nN** · 하중 속도 **1 µm/s** · 캔틸레버 스프링 상수 **5 N/m** (*"datum supplied by the manufacturer"* — **이 논문에서 교정하지 않았다**).
- 힘 곡선: 캔틸레버 처짐 ΔZc vs 피에조 수직좌표 Z 를 누르기–빼기 한 주기로 기록 (Fig. 4).
  **F = k·ΔZc** · **δ = ΔZ − ΔZc** (ΔZ = 접촉점으로부터 피에조 변위의 오프셋).  δ 는 F 에 **선형**이었다고 보고.
- 빼기 곡선의 초기 구간이 누르기와 어긋남 = 탐침–섬유 **점착** (Ref. 25) — 그 뒤로는 두 곡선이 겹침 ⇒ **탄성 변형**.
- 가닥당 **≥ 6 회** 굽힘, 시험 후 TEM 으로 손상 · 압흔 없음 확인.

### 4-5. 모델 식과 가정 (p. 1232 · p. 1236)
- **Eq. 1 (양단고정보, 중앙 집중하중; Gere & Timoshenko, Ref. 27)**:  **F = (192·E·I / L³) · δ**
- 단면: *"prismatic beams of hollow circular cross-section"* — I 식 자체는 본문에 없다.  표준 중공 원형 단면 **I = π(D⁴ − d⁴)/64** 로 읽는다 (DERIVED · 표준식; §3-3 재구성이 이 읽기와 정합).
- E = 하중–처짐 곡선 **접촉점 이후 구간의 선형 적합** 기울기에서.
- Euler–Bernoulli 보 (종횡비 → 전단 무시).  **벽 전체가 하중을 진다**는 가정 (Fig. 6a) · **외벽만 진다**는 대안 (Fig. 6b).
- ⚠ 비교: 단순지지보면 계수가 **48** (양단고정 192 의 1/4) — 실제 고정이 완전하지 않으면 같은 곡선에서 **E 가 낮게 나온다** (§8 비판 ①).

### 4-6. 오차 요인 — 저자가 다룬 것 / 다루지 않은 것

| 저자가 다룬 것 | 어떻게 |
|---|---|
| 치수 측정 오차 | AFM 역합성곱 대신 HRTEM 직접 측정, ±3 nm |
| 탐침 점착 | 빼기 곡선 초기 구간 제외, 누르기 곡선에서 적합 |
| 탐침 손상 · 압흔 | 시험 후 TEM 확인 (고하중 대조 시험 Fig. 5) |
| 반복성 | 가닥당 ≥ 6 회, 표준편차 보고 |
| 형태 의존 | 같은 섬유의 TEM 형태를 E 와 짝지음 |

| 다루지 않은 것 (우리 읽기) | E 편향 방향 |
|---|---|
| ① Pt 패드 · 격자 지지의 유연성 (완전 고정 가정) | **과소평가** (최대 4 배: 192 → 48) |
| ② 중공 섬유의 탐침 아래 국부 변형(단면 찌그러짐)이 δ 에 더해짐 | **과소평가** |
| ③ 캔틸레버 k 공칭값 (미교정) | E ∝ k — **전 가닥 같은 배율**로 이동 (상대 경향은 불변) |
| ④ 치수 ±3 nm 의 D⁴ · d⁴ 전파 (2.8–10.9 %) | 양방향 — 표의 ± 에 **미포함** |
| ⑤ k_fibre/k 가 큰 가닥 (15: 11.7 배) 의 δ 소차 증폭 | 양방향 (지지 유연성과 겹치면 과소) |
| ⑥ 다층 벽의 층간 미끄럼 (벽 전체 강체 단면 가정) | 굽힘 겉보기 E 과소 쪽 — 저자는 E′ 로 **부분적으로만** 다룸 |

⇒ **①②⑥ 은 한 방향(과소)** 이다.  그리고 그 영향이 가장 클 형태가 바로 **10 GPa 근처의 굵고 · 외벽 얇고 · 속 넓은 섬유**다.
즉 가장 낮은 두 값(6 · 13 GPa)은 **"진짜 무른 섬유"** 인지 **"겉보기 값이 낮게 나온 섬유"** 인지 이 논문으로 가를 수 없다 — 저자 자신도 fibre 5 를 후자로 읽었다.

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** (p. 1232) | (a) 광학 — Cu 격자의 가운데 사각 틈을 **대각선으로** 가로지른 섬유, 양끝 Pt 패드 · (b) 같은 섬유의 AFM 높이 영상 (축척 2 µm) | 걸친 길이 L 이 격자 틈(수 µm)으로 정해진다 — Table 1 의 L 2.5–9.2 µm 는 **지지점 간 거리**이지 섬유 길이가 아니다 |
| **2** (p. 1232) | HRTEM — 외경 D · 내경 d 화살표, 원추 **반각 θ/2** 를 그려 표시 (5 nm 축척) | 캡션의 원추각 θ = 그림에 그린 반각의 2 배.  속빈 코어가 넓다 (이 영상에서 d/D 가 큼) |
| **3** (p. 1233) | HRTEM — **Hollow Core / Inner layer / Outer layer** 경계를 선으로 표시.  무질서 외벽 + 질서 원추 내벽.  삽입 = 저배율 섬유 전체 (축척: 본 그림 5 nm · 삽입 500 nm) | 섬유가 **균질 연속체가 아니다** — 벽 안에 강성이 다른 두 층.  우리 MPM 재료점(균질 · 중실)과의 표현 차이 |
| **4** (p. 1233) | 주 그림: ΔZc (0–50 nm) vs Z (0–40 nm), 누르기 · 빼기 곡선 — Z ≲ 30 nm 에서 두 곡선 겹침, Z ≈ 30–37 nm 에서 빼기 곡선이 아래로 처짐(점착), Z ≳ 33 nm 평탄 ≈ 14 nm.  삽입: F (0–100 nN) vs δ (0–20 nm) 누르기 곡선 — **선형** | ⚠ **figure-read**: 주 그림 기울기 ≈ **1.0** (ΔZc ≈ 44.1 @ Z = 1 → ≈ 19.8 @ Z = 25) · 삽입 F ≈ 90 → 0 nN over δ ≈ 0 → 15 nm (기울기 ≈ 6 N/m).  논문 식(F = kΔZc, k = 5, δ = ΔZ − ΔZc)을 그대로 적용하면 주 그림은 δ ≈ 0 · F ≈ 150 nN 이 되어 **삽입과 맞지 않는다** — 삽입이 다른 시험인지 · 축에 적지 않은 오프셋/교정이 있는지 **논문이 밝히지 않는다** (§8 비판 ⑦).  어느 가닥의 곡선인지도 미기재 |
| **5** (p. 1234) | 고하중 시험 TEM — (a) 두꺼운 외벽: 탐침 접촉점(삼각형)에 **균열**, 섬유는 형태 유지 (840 nN) · (b) 얇은 외벽: **파단** (190 nN) (축척 100 nm) | 외벽이 하중을 진다는 해석의 정성 증거.  파단 **힘**만 있고 **응력 · 형상 치수는 없어** 강도로 못 바꾼다 (n/a) |
| **Table 1** (p. 1234) | 17 가닥 L · D · d · t · E · θ · t_in · t_out · t_out/t | ★★ **이 카드의 모든 수치 판정의 원천** (§3-1 전수) |
| **6** (p. 1235) | (a) 벽 전체 가정 E vs t — 열린 원 t_out/t < 0.5 · 채운 원 ≥ 0.5.  채운 원이 207 GPa (t ≈ 31) 에서 t 증가로 급감, t > 80 nm 에서 13–32 GPa.  (b) 외벽 단독 E′ vs t (t > 80 nm 세 가닥 제외) | ★★ 판정의 핵심 그림.  **디지털 판독** (§6-2): (a) 17 점이 Table 1 E 를 0.3 GPa 안에서 재현 (x 위치 = (D−d)/2) · (b) 14 점 E′ ≈ 23–234 GPa.  ⚠ (a) 에서 **t_out 을 못 잰 fibres 15–17 이 채운 원(≥ 0.5)** 으로 그려져 있다 (§8 비판 ⑨) |
| **7** (p. 1235) | 3점 굽힘 모식도 — 지지 격자 · Pt 패드 · 섬유 · AFM 탐침 · 지지 간 거리 L | 경계조건 = 패드로 **양끝 고정**된 보.  **고정의 유연성은 그림에도 식에도 없다** |

**크롭 메모** (`litdb/figures/lawrence2008_single_vgcnf_elastic_modulus_morphology/figures.json`):
- 자동 크로퍼(`tools/litdb/extract_figures.py`)는 8 개 중 7 개를 잡았지만 ① **Fig. 2 누락** (캡션 위 영역을 못 찾음) ② **Fig. 4 는 윗부분이 잘리고 오른쪽 본문 단이 섞임** ③ **Table 1 은 쪽 전체** (bbox y 55.6–755.5) ④ Fig. 1 · 3 · 5 는 여백 · 저널 측면 띠 포함.
- ⇒ **8 장 전부 손으로 다시 잘랐다**: 그림 7 장은 각자 **내장 래스터의 배치 사각형 + 1.5 pt**, Table 1 은 **"TABLE 1" 캡션 ~ 각주 a 띠** (텍스트 표).  300 dpi.  8 장 모두 **Read 로 열어 확인** (`viewed: true`).
- 캡션은 PDF 원문 그대로 (합자 · 기호 복원: ΔZc · δ · θ · E′ · ≥).

## 6. Post-processing ★

### 6-1. 저자가 한 것
- **무엇**: AFM 힘 곡선 → F = kΔZc, δ = ΔZ − ΔZc → 접촉점 이후 **F–δ 선형 적합** → Eq. 1 + 중공 원형 I 로 **E** → 가닥당 ≥ 6 회 평균 ± 표준편차.
  HRTEM 으로 D · d (여러 지점 평균) · θ · t_in · t_out.  **t_out/t = 0.5 로 두 무리 분할** (Fig. 6 의 열린/채운 원).  **외벽 단독 E′ 재계산** (Fig. 6b).
- **도구**: 장비명만 (FIB · TEM · AFM, §2).  적합 소프트웨어 · 원자료 공개 **없음** (SI 없음).
- **기록 방식**: Table 1 (가닥별 형태 + E) + Fig. 6 (E · E′ vs t, 오차막대).  **E′ 는 표에 없고 그림에만** 있다.

### 6-2. 우리가 한 것 (재현 가능하게 적는다)
- **Table 1 전사** — PDF 텍스트 추출(± · θ · µ 가 깨짐)을 **220 dpi 렌더 이미지와 한 칸씩 대조**.  내부 정합 검사: t_in + t_out = t (14 가닥 전부) · t_out/t 재계산 = 표값 (14 가닥 전부) · (D−d)/2 ≈ t (fibre 4 만 45 vs 41).
- **Fig. 6 디지털 판독** — 내장 래스터 **834 × 1030 px** (PDF 에 **반전 저장** — 렌더 시 뒤집힘) 를 반전 후:
  축 보정: **t = 20 + (x − 95.5)/6.4 nm** (주 눈금 x = 223.5 / 351.5 / 479.5 / 607.5 / 735.5 px = 40–120 nm) ·
  **(a) E = (472.5 − y)/2.14 GPa** (눈금 44.5 / 151.5 / 258.5 / 365.5 px = 200–50) · **(b) E′ = (955.5 − y)/2.015 GPa** (눈금 552.5 / 653.5 / 754.5 / 855.5 px = 200–50).
  표지 검출: 채운 원 = 7 × 7 침식 후 연결성분 중심 · 열린 원 = 반경 7–8 px 고리 점수 ≥ 0.85 + 속 빔.  범례 · 눈금 글자 영역 제외.
  **검증**: (a) 17 점의 E 가 Table 1 값을 **0.3 GPa 안에서** 재현 ⇒ 보정 정확.  판독 불확도 ≈ ±1 GPa (표지 중심 ±2 px).
- **E′ 식 재구성** (§3-3) — 14 점 전부 −1.8 ~ +0.3 GPa.
- **Fig. 4 판독** — 같은 방식으로 주 그림 곡선을 Z = 1 … 39 nm 에서 추출 (§5 Fig. 4 행).

## 7. 우리 DEM+MPM 대비 (frame[4] · frame[5])  →  `our_dem_baseline.md` (⛔ 자리표시 — 우리 값은 아래 원장 · 작업 브랜치 문서에서)

> ⚠ **이 논문에는 DEM · MPM · 미세구조 모델이 하나도 없다.**  frame[4] 교차검증 상대가 **아니라 상(phase) 입력 앵커**다.
> frame[5] 로는 **역학 쪽 한 칸**에만 걸린다 = MPM 섬유 재료점의 E_VGCF.  **전달 쪽(σ_e) 정보는 0** — VGCF σ 앵커는 `endo2001_…` 카드 몫.
> 접촉망 · percolation · 섬유–섬유 접촉저항 · 섬유 길이 분포 **전부 없다**.

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| **E_VGCF** | 17 가닥 **6–207 GPa**, 중앙값 55 (겉보기 굽힘 · 벽 단면 기준) · 외벽 단독 E′ ≈ 23–234 | **10 GPa** `Assumed` — `mpm3d_compaction.py` `ADD_E_NU['VGCF'] = (10.00, 0.30)` · 원장 `CL-42` (근거 미기재) · 도입 커밋 `862a61833` (2026-06-24) *"medium-stiff E10/sigma_y2 (keeps fibre shape, elastic bend)"* | 10 GPa 는 **16/17 가닥보다 낮다**.  "측정 범위 안" 은 **fibre 5 한 가닥** 덕분이고 그 가닥은 저자가 과소평가 쪽으로 읽은 형태 (§0-2) |
| **값의 종류** | 중공 벽 단면 · 양단고정보 가정의 **굽힘 겉보기** 탄성률 | MPM 섬유 재료점 Lamé 상수 (σ_y 2.0 GPa ≫ 가압 0.3 GPa ⇒ 탄성만) | 다른 양.  중공관을 중실 재료점으로 바꿀 때 축강성 환산 인자 1 − (d/D)² = 이 표에서 **0.55–0.96**, 굽힘 1 − (d/D)⁴ = 0.79–1.00 (DERIVED) — **55 → 10 의 간격을 메우지 못한다** |
| **직경** | D **115–470 nm** | 모델 **0.15 µm** (SI Table S2 `Measured` — SEM 원본 대기, 작업 브랜치 `si_table_response_20260925.md` §3) · 그룹 실험 VGCF = Showa Denko **~150 nm × ~10 µm** (`kim2025_conductive_agent_se_coating_cathode`) | 낮은 끝만 겹친다.  **D ≤ 200 nm 9 가닥 = 23–207 GPa** |
| **구조 · 열처리** | 원추형 (질서 내벽 + 무질서 외벽, 속빈 코어), 열처리 미기재, 형태는 **비열처리형과 일치** (추론) | 흑연화 VGCF 로 다뤄 옴 — ⚠ **"VGCF-H · 흑연화" 는 공급사 데이터시트 원본 대기** (`endo2001_…` §3-5) | 저자: 열처리 → 외벽이 완전한 MWNT ⇒ 흑연화 섬유는 **더 뻣뻣할 방향** (이 논문은 흑연화 섬유를 안 쟀다) |
| **표현** | 섬유 = 두 층 벽을 가진 **중공** 보 | 섬유 = **sub-grid 재료점** (중공 · 층 표현 없음) | 형태 의존(외벽 비율) 을 우리 모델은 담지 못한다 — **단일 E 는 단순화** |
| **파단** | 190 nN (얇은 외벽) · 840 nN 균열 (두꺼운 외벽) — 응력 환산 불가 | 섬유 파단 모델 **없음** | 건식 혼합 · 압연 중 섬유 절단은 우리 축 밖 (§H 혼합 공정 축) |
| **민감도** | — | 09-25 **h0**: E_VGCF 1 / 10 / 100 GPa → porosity 14.749 / 14.889 / 14.929 % · σ_e 59.27 / 59.15 / 59.30 mS/cm (Δε 0.18 %p · Δσ_e ≤ 0.25 %) — 작업 브랜치 `docs/data/vgcf_e_sensitivity_20260925/summary.tsv` | ★ **이 논문의 17 가닥 중 14 가닥이 시험 창 1–100 GPa 안**.  창 밖: 3 가닥(105 · 160 · 207) + 흑연화 ≈ 10² GPa (Endo) ⇒ *"> 100 GPa 미시험 외삽"* 은 유지 |
| 강성 대비 (섬유 : SE) | 실재료로 보면 (Lawrence 중앙값 55 · 최대 207) : (LPSCl 22–24) ≈ **2.3 – 9.4** | 모델 10 : **1.53** (MPM champion E_SE) = **6.5** | DERIVED · 해석 후보 (§8 ③) — 우리 대비는 실재료 대비 범위 **안**에 있다 |

**frame[2] 정직성 메모**: SE 의 E_eff 1.53 GPa (MPM) · 1.35 GPa (DEM) 는 실 E_SE ≈ 22–24 GPa 를 **입자 재배열 등 빠진 기구의 대리로 연화**한 값이다.
VGCF 10 GPa 는 그런 보정 논리로 정해진 값이 **아니다** — 06-24 에 *"섬유 형태 유지 · 탄성 굽힘"* 이 되도록 고른 값이다.  그러니 이 논문과의 비교는
"보정" 이 아니라 **"모델 입력이 실측 산포의 어디에 있나"** 의 위치 확인이다.

## 8. 적용 인사이트 (내 연구에 어떻게)

- ① **SI Table S2 각주 ᵍ 에 이 논문을 "범위 참조" 로 넣는다** (§0-3 (A)) — 표 칸은 `Assumed` 그대로.  출처 칸에 단독으로 넣지 않는다.
- ② ★ **민감도 창의 정당화가 강해진다** — 지금까지 창 1–100 GPa 의 문헌 위치는 *"문헌값(Endo ≈ 110–310 · Ozkan 180–245 [미확인]) 은 창 밖"* 뿐이었다.
  이 논문으로 *"개별 섬유 실측 산포 6–207 GPa 의 14/17 이 창 안"* 이 추가된다.  ⇒ 리뷰어의 *"왜 1–100 만 봤나"* 에 대한 답의 절반.
  나머지 절반(> 100 GPa) 은 여전히 **외삽**이고, 1→10 GPa +0.14 %p · 10→100 GPa +0.04 %p 의 **체감** 이 그 외삽의 근거다 (새 런 요구 아님 — h0 판정 그대로).
- ③ **(저자 판단 필요) 대비-보존 논리 후보** — MPM 에서 섬유 형태 유지를 정하는 것은 E_VGCF 의 절대값보다 **기질(SE) 과의 강성 대비**일 수 있다.
  모델 대비 10 : 1.53 = **6.5** 는 실재료 대비 (Lawrence 중앙값 55 ~ 최대 207) : (LPSCl 22–24) ≈ **2.3–9.4** 안에 있다 (DERIVED).
  같은 연화 배수(22–24 / 1.53 ≈ 14.4–15.7)를 거꾸로 적용하면 10 GPa ↔ 실재료 **≈ 144–157 GPa** 에 대응 — Lawrence 범위 안이고 Endo 영역(≈ 110–310) 안.
  ⚠⚠ **이것은 사후 합리화 후보이지 도입 근거가 아니다** (06-24 커밋은 이런 계산을 하지 않았다).  원고에 쓰려면 저자가 채택을 결정하고 *"post hoc"* 을 밝혀야 한다.
  SE 연화가 섬유에도 같은 배수로 적용돼야 할 물리적 이유는 **없다** (SE 연화는 분말 재배열의 대리 — frame[2]).
- ④ **섬유 강성은 한 수가 아니다** — 같은 배치 안에서 외벽 비율 · 벽 두께 · 직경에 따라 **35 배** (6 → 207) 퍼진다.
  섬유를 단일 E 로 두는 우리 표현의 한계를 원고 한계 절에 한 줄로 적을 근거 (*"single effective modulus for a morphologically heterogeneous filler"*).
- ⑤ **Ozkan 2010 (Carbon 48, 239; 리포 문서의 180–245 GPa) 은 이 카드로 확인되지 않는다** — 웹 검색 기준 · PDF 미확보 그대로 `[미확인]`.
  이 논문은 그 값을 인용하지 않는다 (2008 년 논문).

## 9. 인용 가능 문장 (deck / 원고용)

- (EN, 각주) *"For reference, AFM three-point bending of individual vapour-grown carbon nanofibres gave apparent moduli of 6–207 GPa (median 55 GPa;
  14 of the 17 fibres ≤ 100 GPa) [Lawrence 2008]."*
- (EN, 한계 절) *"Single vapour-grown carbon nanofibres show bending moduli spanning more than an order of magnitude (6–207 GPa) depending on
  wall morphology [Lawrence 2008]; our model assigns a single effective modulus to the fibre phase."*
- (EN, 방법 요약) *"Lawrence et al. suspended individual Pyrograf III nanofibres across TEM-grid gaps, clamped both ends with FIB-deposited Pt,
  and combined AFM three-point bending (fixed–fixed beam, F = 192EIδ/L³) with HRTEM measurement of the same fibres."*
- (KR, 발표) *"같은 배치의 기상성장 탄소나노섬유도 외벽 구조에 따라 6 에서 207 GPa 까지 퍼진다 (Lawrence 2008) — 우리 10 GPa 는 측정값이 아니라
  가정값이고, 1–100 GPa 에서 결과가 안 움직인다는 것으로 방어한다."*
- ⛔ 쓰면 안 되는 문장 = §0-3 끝 목록.

## 10. 주의 / 한계 (over-claim 방지)

- **한 배치 · 등급 미기재 · n = 17 · 비열처리형(추론)** — 흑연화 섬유 **0**.  우리 VGCF 로 값이 **옮겨지지 않는다** (방향만: 흑연화는 더 뻣뻣할 쪽).
- **겉보기 굽힘 탄성률**이다 — 양단고정 · 중공 균질 단면 · 벽 전체 하중 가정.  인장 탄성률(Endo Fig. 6) 과 **같은 양이 아니다**.
- **E′ 식은 본문에 없다** — 우리 재구성 (14 점 재현) 이지 저자 명시가 아니다.  E′ 값은 **figure-read ≈**.
- **캔틸레버 k 미교정** (제조사 공칭 5 N/m) — 절대 척도 전체가 k 에 비례.  **표의 ± 는 반복성뿐** (치수 · k · 경계조건 오차 미포함).
- 두 영역 주장(t_out/t 분할) 의 근거는 **9 대 5 가닥**, *"~25 GPa 평탄역"* 은 **3 가닥** (13 · 25 · 32).
- *"wall thickness t 가 가장 중요"* 는 저자 판단 — 이 표에서는 D 와의 순위상관이 더 강하다 (§3-2).  원인 분리 불가.
- **2D/3D · 할라이드 · 강체구 floor** 같은 우리 축의 전형적 전이 경고는 해당 없음 — 대신 **재료 전이(Pyrograf III → Showa Denko 흑연화)** 와
  **양의 종류(굽힘 겉보기 → MPM 재료점)** 가 이 카드의 통제 경고다.
- 파단 시험(Fig. 5) 은 **힘**만 — 강도로 환산할 형상 치수 없음.

### 10-1. 논문 내부 불일치 · 비판 목록 (우리 읽기, 번호 = §0 · §4 참조용)

| # | 무엇 | 어디 | 영향 |
|---|---|---|---|
| ① | 양단고정 가정 — 패드 · 격자 지지 유연성 검증 없음 | Eq. 1 · Fig. 7 | E 과소 (최대 4 배) — 낮은 값일수록 의심 |
| ② | 중공 섬유 국부 변형 무시 | §4-5 | E 과소 |
| ③ | k 공칭값 | p. 1235 | 전 가닥 동일 배율 |
| ④ | 치수오차 미전파 | Table 1 ± | 표의 ± 가 실제 불확도보다 작다 (예: fibre 8 ±1 vs 직경만 ±11 %) |
| ⑤ | k_fibre/k 0.08–11.7 — 뻣뻣한 가닥의 δ 소차 | Table 1 + Eq. 1 (DERIVED) | fibres 13–15 의 신뢰도 |
| ⑥ | 층간 미끄럼 (벽 강체 가정) | §4-5 | E 과소 쪽 — E′ 로 부분 대응 |
| ⑦ | **Fig. 4 주 그림 ↔ 삽입 불일치** (figure-read): 주 그림 기울기 ≈ 1.0 이면 δ ≈ 0 · F ≈ 150 nN 인데 삽입은 F ≈ 90 nN · δ ≈ 15 nm | Fig. 4 | 방법 예시 그림으로 강성 수치를 **독립 검산할 수 없다** — 원인 미상, 해석 보류 |
| ⑧ | fibre 4 t = 45 (= t_in + t_out) ≠ (D−d)/2 = 41 · Fig. 6 은 41 에 찍힘 | Table 1 · Fig. 6 | 작음 (E′ 식 선택에만 영향) |
| ⑨ | t_out 미측정 fibres 15–17 이 Fig. 6a 에서 **채운 원(t_out/t ≥ 0.5)** 으로 표시 | Fig. 6a (figure-read) | 두 영역 그림의 분류가 **표와 다르다** |
| ⑩ | 종횡비 *"between 10 and 20"* vs 표 L/D 13–80 | p. 1232 · Table 1 | 보 이론 유효성에는 오히려 유리 (더 가늘다) — 서술 오류 |

## 11. 논증 흐름 (절별 — 이 절만 읽어도 논문을 따라갈 수 있게)

1. **서론 (p. 1230–1231)** — VGCNF 는 SWCNT 만큼 완전하지 않지만 비슷한 열 · 기계 물성이 기대되고 부동촉매 연속 반응기로 싸게 대량 생산된다 → 고분자 복합재 필러 수요.
   그러나 구조가 복잡하다: 원추형(다수: 완전 cone-helix 내벽 + 무질서 외벽) · 대나무형(소수), 열처리하면 원추형이 흑연화 변환.
   ⇒ **나노튜브와 달리 직경 하나로 강도를 말할 수 없고** 내 · 외벽 두께 · 원추각까지 필요 — *"attempts to measure only the elastic modulus of nanofibers without the corresponding morphology are of little value."*
2. **선행 비판** — Uchida 2006 계산(완전 흑연 775 → 난층 외층 110 GPa) 은 내벽을 단일 그래핀 탄성률로 가정해 층간 약결합을 무시 → 신뢰 못 함.
   AFM 굽힘 선행법들(막 · 실리콘 기판 · 홈) 은 막 연마 · 약한 점착 · **AFM 영상 직경의 팁 합성곱** 문제.  Nakajima 2006 TEM 내 나노로봇(MWCNT 1.23 TPa) 은 특수 장비.
   ⇒ **흔한 장비(AFM + TEM + FIB) 조합**으로 형태와 E 를 같은 섬유에서 잰다.
3. **방법 (pp. 1231–32)** — Cu 격자 걸치기 → FIB Pt 고정 → HRTEM 치수 · 형태 → FIB 로 L → AFM tapping 으로 재발견 → 3점 굽힘.
4. **탄성 확인** — 초기 빼기 구간(점착) 외에는 누르기 · 빼기 곡선 일치 (Fig. 4), 종횡비로 보 이론 · 전단 무시, 선형 적합, 17 가닥 · ≥ 6 회, 시험 후 손상 없음.
5. **형태 측정 정확도 (p. 1233)** — TEM 직접 측정이라 불확도는 섬유 불균일 ±3 nm.  고하중 대조 시험(Fig. 5): 두꺼운 외벽 840 nN 균열 · 얇은 외벽 190 nN 파단 — **탐침 손상을 이 방법으로 잡을 수 있다**는 시연.
6. **형태 의존 (p. 1233–1234)** — E 는 원추각 · 내벽 두께 · 외벽 비율에 의존해 보이나 **가장 중요한 것은 벽 두께 t**.  t_out/t 로 **두 영역**: > 0.5 에서 훨씬 크다 — fibres 4 (160) 와 9 (20) 는 t 가 같아도 **거의 한 자릿수** 차이.
7. **Fig. 6a** — t_out/t ≥ 0.5 에서 E 는 t 에 반비례해 207 GPa 에서 급감, *"~25 GPa"* 에서 바닥 · 매우 두꺼운 섬유도 그 값 — *"counterintuitively, thinner fibers have greater strength"*.  t_out/t < 0.5 무리도 비슷한 경향(덜 뚜렷).
8. **외벽 지배 (p. 1234)** — 외벽이 내벽보다 얇으면 E 가 크게 떨어진다 ⇒ **외벽이 강성을 진다**.  fibre 5 (t_out/t 0.17) 는 6 GPa 까지 → 외벽 단독 하중으로 재계산하면 (Fig. 6b) 두 무리가 **더 가까워진다**.
   이유: 내벽의 나선 그래핀 면 사이 상호작용이 약해 하중을 못 진다 (Ref. 10).
9. **t 증가에 따른 E 감소의 해석** — 외벽이 두꺼우면 뻣뻣해야 할 텐데 반대 → 층이 더해질수록 **외벽의 불완전성 증가** (Fig. 3), 더해진 층은 하중을 안 진다 ⇒ 벽 전체 가정의 E 가 낮아짐.
   얇은 등급(예: PR-24)이 응용에서 선호된다는 일화와 일치.  *"If this is valid then the correct value of E for the load bearing parts … will be much larger than that reported in Table 1, and may approach those reported for MWCNTs."*
10. **두꺼운 섬유 (p. 1235)** — t > 80 nm 에서 E 가 t 와 거의 무관한 *"~25 GPa"* — 나노 물성에서 **벌크 거동으로의 전이**, 저급 탄소섬유 쪽, 대부분 난층 그래핀.
11. **요약** — 재현성 있는 방법 · 정확한 치수 · 고하중 아니면 무손상 · 두 경향 · *"the more ordered layers of the outer wall, closest to the inner wall, are mostly responsible for the nanofiber strength"* ·
    t > 80 nm 에서 ~25 GPa · 원추형 섬유는 SWCNT · MWCNT 값에 못 미치지만 *"could be as high as 200 GPa or larger"*.
12. **Methods (p. 1235–1236)** — 90 nN · 1 µm/s · k 5 N/m · F = kΔZc · δ = ΔZ − ΔZc · Eq. 1.

## 12. 용어 미니 사전

| 용어 | 뜻 |
|---|---|
| **VGCNF / VGCF** | vapor-grown carbon (nano)fiber — 탄화수소를 촉매 입자 위에서 기상 분해해 키운 탄소섬유.  이 논문은 VGCNF, 우리 리포는 VGCF 라 부른다 (같은 계열, **다른 제품**) |
| **Pyrograf III** | Applied Science Inc. (Ohio) 의 VGCNF 제품군.  등급(예: PR-24) 은 직경 · 처리로 나뉜다 — 이 논문은 시험 등급을 **적지 않았다** |
| **원추형(conical) / cone-helix** | 그래핀 면이 섬유 축에 비스듬히 원뿔처럼 쌓인 내벽 구조.  원추각 θ (Fig. 2 는 그 반각 θ/2 를 그려 표시) |
| **대나무형(bamboo)** | 마디로 나뉜 속빈 구조 — 나노튜브에 가까움 (소수) |
| **stacked cone / cup-stacked** | 열처리 후 내벽의 마디진 원뿔 적층 (저자 용어 *"segmented stacked cone"*).  "cup-stacked" 는 이 논문 용어 아님 |
| **turbostratic (난층)** | 흑연 판이 쌓였지만 층간 정렬(AB 적층)이 없는 상태 |
| **t_in / t_out** | 질서 있는 내벽 두께 / 무질서 외벽 두께.  t = t_in + t_out |
| **3점 굽힘** | 양끝 지지 보의 가운데를 눌러 힘–처짐 기울기에서 E 를 구하는 시험 |
| **양단고정(clamped–clamped) vs 단순지지** | 끝의 회전까지 막으면 강성 계수 192, 회전 허용이면 48 — 가정이 E 를 4 배 바꾼다 |
| **단면 2차 모멘트 I** | 굽힘 강성을 정하는 단면 기하량.  중공 원: π(D⁴ − d⁴)/64 |
| **굽힘(flexural) vs 인장(tensile) 탄성률** | 균질 재료면 같지만, 층상 · 중공 · 결함 섬유에서는 굽힘이 바깥층과 층간 전단에 민감해 다를 수 있다 |
| **E′** | 외벽만 하중을 진다고 보고 다시 계산한 탄성률 (Fig. 6b) |
| **FIB Pt 증착** | 집속 이온빔으로 백금을 국소 증착해 섬유 끝을 기판에 붙이는 기법 |
| **tapping mode** | AFM 탐침을 진동시켜 표면을 가볍게 두드리며 영상화 — 섬유 위치 재확인용 |
| **ΔZc / Z** | 캔틸레버 처짐 / 피에조 수직 변위.  F = k·ΔZc, δ = ΔZ − ΔZc |
| **sub-grid 재료점 (우리)** | MPM 격자 한 칸보다 작은 섬유를 재료점 줄로 표현한 것 — 중공 · 층 구조는 표현 안 됨 |

## 13. 관련 카드 (litdb 내부 교차참조)

- `endo2001_vgcf_basic_properties_battery_applications` — ★ 짝 카드.  흑연화 submicron VGCF 의 **인장탄성률 ≈ 110–310 GPa (Fig. 6 개략 영역)** · σ_e 단섬유 1e4 · 압분체 ≈ 80 S/cm.  이 카드와 합치면 E_VGCF 각주의 문헌 위치가 **"개별 섬유 굽힘 6–207 (Lawrence) · 흑연화 인장 ≈ 10² (Endo)"** 두 줄로 선다.
- `kim2025_conductive_agent_se_coating_cathode` — 우리 그룹 실험 VGCF (Showa Denko, ~150 nm × ~10 µm).
- `kim2026_charge_engineered_cnf_binder` · `koo2026_swcnt_sheath_thick_electrode` — 다른 1D 탄소 (CNF · SWCNT).
- `lee2025_corolling_dryprocess_lpscl_ptfe` · `zhang2026_dryprocess_electrode_architecture_cell_level` · `matthews2024_ptfe_nanofibril_network` — 건식 전극의 VGCF–PTFE 섬유망.
- `sun2026_dem_extrusion_recirculation_dry_electrode` — 섬유 해상도 실패 사례 (§H-7).
- `song2025_porous_argyrodite_modulus_fracture_toughness` · `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` — 다른 상(SE · AM) 의 탄성률 입력 앵커 (§8 ③ 의 강성 대비 계산에 쓰는 SE 쪽 값의 계열).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
