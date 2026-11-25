<!-- digest 초판 2026-11-23 (litdb-curator · 대피 세션 — git 미사용 · 커밋은 메인 세션).
     ① PDF 34 pp 텍스트 전문 정독 (본문 pp.1–30 · 참고문헌 128 pp.30–34) · SI 없음 · 우리 그룹 아님 ·
        talk 인입 대기열 미등재 (대기열이 있는 talk 은 `talks/lee2026_skku_mlip_materials_design.md` 하나 · 이 편 행 없음 — 확인).
     ② 크롭 11 장 (그림 9 + 표 2 · 번호 공백 0 · 메인 세션이 미리 자름 · 도구 재실행 안 함).
        그림 9 장 **전부** 실독 + 확대 재크롭 13 패널 (16 장 · scratchpad 에만 · repo 에 안 넣음):
        `Fig. 2f` `Fig. 2k` `Fig. 3d` (2회) `Fig. 5c` `Fig. 5f` `Fig. 5g` `Fig. 5i` `Fig. 6e` `Fig. 7a` `Fig. 7g` `Fig. 8d` `Fig. 8e1` (3회) `Fig. 8f`.
        `Table 1` · `Table 2` 는 이미지 대신 PDF 텍스트로 전사.
     ③ figures.json: 잘린 캡션 5 개 (Fig. 2 · 3 · 5 · 7 · 8 — 도구 900 자 상한 · Fig. 5 는 p.19 로 넘어감) 를 PDF 원문으로 복원
        (caption_auto 보존 · caption_fix 사유) + 그림별 viewed / viewed_how.
     ④ 텍스트층 함정 (확인함): 본문을 뽑으면 E/S 단위가 'mL mg⁻¹' 로 나오지만 그 m 은 Symbol 글꼴 (AdvPS3F4C13) 이라
        화면에는 **μL mg⁻¹** 다 — 단위 오류가 아니다. 같은 글꼴의 'D' = Δ · 'a/b/g' = α/β/γ · AdvPS3FDD77 'z' = ≈ ·
        AdvPS40C6FB '/' = →. `Table 1` 의 '∼30 mm' 도 30 μm.
     ⑤ 이 편은 리뷰 — 자체 계산 0 · 자체 실험 0 (Data availability "no new data"). 수치는 전량 2차 소환.
        계산 조건은 범함수 'PBE' 한 번 (`Fig. 5a` 캡션) 이 전부.
     ⑥ 같은 Tiangong 그룹 (Deng · Kang) 의 짝 리뷰 `luo2026_lis_separator_crystal_engineering_review` (*Small* 2026) 와
        NSFC 과제 번호 셋 (52573089 · 52403046 · 61904123) 을 공유한다. -->

# Research on the preparation and application of multifunctional P-doped compounds in lithium–sulfur batteries — Lin et al. (*J. Mater. Chem. A* 2026, Review)

> slug `lin2026_p_doped_compounds_li_s_review` · DOI `10.1039/d6ta06590b` · type `review (자체 계산 0 · 자체 실험 0 · 액체 전해질 Li–S 양극 숙주 · 분리막/중간층의 P 도핑 문헌 정리)` · PDF `litdb/inbox/3e59ba8a-Research_on_the_preparation_and_application_of_multifunctional_P-doped_compounds_in_lithium_sulfur_batteries.pdf` (34 pp) · **SI 없음** · digested `2026-11-23` · status ✅ · 태그 **[외부]**

> elements: Li, S, P, C, N, O, B, Co, Fe, Ni, Mo, W, Ru, Ti, Ce, In, Mn, Nb, Se, Te, Zr, V, Cu
> methods: DFT, DOS, PDOS, Bader, XPS, Raman
> 🔗 **관련 (2026-11-25)**: `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` — 이 리뷰 범위 밖의 전해질 쪽 전략 (약용매화 SSE + 공용매) 1차 논문 · 흡착 · 결합에너지 보고 규약 반례 (슬랩 방법 미기재) 가 같은 결.

> **저자**: **Ruixin Lin**† · **Fan Zhang**† (공동 1저자) · **Nanping Deng\*** · **Shaoju Li\*** · Yun Luo · **Weimin Kang\*** — Tiangong University (天津工业大学) School of Textile Science and Engineering · MoE Key Lab for Advanced Textile Composite Materials (Tianjin) + Quanzhou Vocational and Technical University (School of Arts & Media · Fujian — Li) · 접수 2026-08-05 → 수락 2026-10-29 → 게재 2026-11-19 (Advance Article · 권/쪽 미배정 — 인용은 DOI) · 자금 NSFC 52573089 · 52403046 · 61904123 외 · Data availability *"No primary research results, software or code have been included and no new data were generated or analysed"* · 이해상충 없음.
>
> **구성**: §1–§6 · **그림 9** (자체 개념도 2 = `Fig. 1` 분류 바퀴 · `Fig. 9` 전망 바퀴 · 나머지 7 장은 원전 패널 재수록 모음) · **표 2** (`Table 1` 분리막 10 행 · `Table 2` 양극 9 행) · refs **128** (본문 인용 번호 1–128 전부 등장 — 위첨자 자동 집계 · 범위 표기 포함).
>
> **계보**: 같은 그룹의 짝 리뷰 `[Luo26Sep]` (*Small* 2026 · 분리막 '결정공학' · `comparison_vs_ours.md` §J-67) 다음 편. 거기서 잡은 보고 규약 결함 (흡착 배위 · 홉 수 · 작동 상태) 이 이 편에서도 반복된다.

> **본 digest 에서 실제로 본 그림**: `Fig. 1`–`Fig. 9` **9/9 장** + 확대 13 패널. **안 본 것**: `Table 1` · `Table 2` (이미지로는 안 봄 — PDF 텍스트가 더 정확).
> 그림에서만 읽은 값은 **`figure-read ≈`**, 그림 안에 글자로 찍힌 값은 **[그림 인쇄]** 로 구분했다.

---

## 0. 이 digest 를 읽는 법 — 우리 트랙과의 거리 판정 (먼저)

**판정: 황화물 SE 물성 4축 (이온 · 산화 · 기계 · 전자) 과 직접 관련 없음.** 무대는 **액체 전해질 (에테르계) Li–S 전지**의 양극 숙주 · 분리막 코팅 · 중간층에 P 를 넣는 일이다. 우리 argyrodite 와 겹치는 물성값은 0 건.

본문 전수 검색 (PDF 텍스트 · 2026-11-23): `Li6PS5Cl` 0 · `argyrodite` 0 · `thiophosphate` 0 · `sulfide electrolyte` 0 · `Li3PS4` 0 · 고체 전지 언급은 본문 3 곳 (초록 끝 'solid-state batteries' · §1 끝 'quasi- and all-solid-state' · 전망 (4) — 셋 다 '앞으로 쓸 수 있다' 꼴 · 근거 인용은 §1 의 [70] 하나) + 참고문헌 2 ([42] · [70]) · **PS₄³⁻ 는 본문 0 · 그림 라벨 1** (`Fig. 8e1`). 계산 키워드: `VASP` 0 · `vdW`/`D3` 0 · `DFT+U` 0 · `NEB` 0 · `AIMD` 0 · `solvation` 0 · `k-point` 0 · `PBE` 1 (캡션) · `barrier` 37 줄 · `d-band` 18 줄.

가져올 것은 셋이다.
1. **화학 연결 (가장 큰 소득)** — 리뷰가 'P–S 결합으로 LiPS 를 잡는다' 고 부르는 것의 열역학적 끝은 **티오인산 PS₄³⁻** 이다 = 우리 SE 의 음이온 골격. 리뷰 자신이 재수록한 `Fig. 8e1` (NiCoP/BP 셀 in situ Raman) 에 **PS₄³⁻ 띠 (figure-read ≈ 415–418 cm⁻¹)** 가 첫 방전부터 찍혀 있는데 본문은 이것을 한 번도 말하지 않는다. 그리고 XPS (`Fig. 6b1` · `Fig. 8d2`) 에서 표면 P 의 주성분은 **P–O** 다 — '촉매 P' 가 초기 상태 그대로 있지 않다는 증거가 리뷰 안에 있다.
2. **보고 규약 반면교사** — 34 쪽에 계산 조건이 사실상 0 줄인데 흡착 에너지 (≈ −1.3 ~ −4.8 eV) · '장벽' · d-band center · HOMO–LUMO · ΔG 사다리를 옮긴다. 그리고 **재수록 그림과 본문 서술이 어긋나는 곳이 18 곳**이다 (§10b) — 그중 다섯은 방향 · 정의 · 공정이 뒤집힌 것 (`Fig. 8f` · `Fig. 5i` · `Fig. 7a` · `Fig. 6e` · `Fig. 5c`).
3. **Li–S 작동 전위창 vs LPSCl 창** — 재수록 그림들의 Li–S 전위창 (figure-read ≈ 1.7–2.8 V vs Li) 은 우리 LPSCl grand-potential 창의 **양쪽 가장자리를 다 넘는다** (환원 1.717 V · 산화 2.256 V / 2.14 V — 규약은 §7). 리뷰 전망 (4) 의 'P 도핑 재료를 전고체로' 는 그 점을 모른 채 쓴 문장이다 (우리 해석 · 새 트랙 제안 아님).

---

## 1. 한 줄 요약

P 를 탄소 · 금속 화합물 · 단원자 촉매 · 흑린/적린 형태로 넣으면 액체 Li–S 전지에서 **흡착 (LiPS 고정) · 촉매 (전환 가속) · 전도 (전자 전달)** 가 한꺼번에 좋아진다는 *"adsorption–catalysis–conduction"* 틀로, 2021–2026 사례 ≈ 70 건을 네 범주 (단독 P · 공도핑 · BP/RP · P + 공공) × 두 부품 (분리막/중간층 · 양극) 으로 정리한 리뷰다.

⚠ 그 틀의 화학 근거 문장 ('P 는 전기음성도가 높다' — 10 회) 은 리뷰 자신이 적은 Pauling 값 2.19 및 'P 는 강한 전자 주개' (6 회) 와 모순이고, 정량 근거는 재수록 DFT 그림인데 그중 둘 (`Fig. 3d` · `Fig. 8f`) 은 본문과 반대 방향을 보인다.

---

## 2. 메타 / 구성 / 던지는 질문

| 항목 | 내용 |
|---|---|
| 던지는 질문 | P 도핑이 Li–S 의 다섯 문제 (S · Li₂S 절연 · ≈80 % 부피팽창 · LiPS 셔틀 · 느린 산화환원 (특히 Li₂S 산화) · Li 덴드라이트/SEI) 를 어떻게 풀며, 설계 범주는 어떻게 나뉘나 |
| P 를 고르는 리뷰의 근거 (pp.2–3) | ① '전기음성' P + 3p 비공유 전자쌍 → P–S · Li–P · P–O 극성 결합 ② 큰 원자 반경 (≈110 pm) · 다가 (+3 · +5) → 격자 왜곡 · 전하 재분배 ③ 흡착 · 촉매 · 전도 세 기능을 '원자 하나로' — "adsorption–catalysis–conduction" |
| 리뷰가 스스로 단 단서 (p.3) | 'P–Li/P–S 직접 결합' 과 '이웃 자리 간접 조절' 을 **구별해야 한다** — P-g-C₃N₄ 계산에서 고정 기전은 강해진 **Li–N** 이었다 [64] · 장점은 '도펀트 수' 가 아니라 '설계된 국소 배치' 에서 온다 |
| 도핑 경로 4 (p.3) | ① 탄소 골격 직접 (phytic acid · PPh₃ · NaH₂PO₂ 고온 소성) ② 금속 화합물 인화 (CoP · RuP₂ · NbP) ③ N 등과 공도핑 ④ 흑린/적린 나노시트 직접 사용 |
| 범주 (`Fig. 1`) | 단독 P 도핑 · P + 다른 이종원자 공도핑 · BP/RP 도핑 · P 도핑 + 공공 공학 |
| 부품 | §4 분리막 (중간층 포함) · §5 양극 숙주 — 음극 · 전해질 · 바인더는 전망 (4) 에만 |

### 2a. 절 구조 (section tree) — 그림 대응

| 절 | 쪽 | 내용 | 그림 · 표 |
|---|---|---|---|
| §1 Introduction | 1–3 | Li–S 다섯 문제 · 되먹임 고리 · 다른 도핑 (N · S · O · I · 금속) · P 의 세 장점 · 대표 성과 2 | — |
| §2 Mechanistic insights | 3–6 | 2.1 흡착/셔틀 · 2.2 산화환원 속도 · 2.3 전도 · 이온 수송 · 2.4 덴드라이트 · 구조 안정 · 2.5 상승 전략 · 2.6 이종구조 · 2.7 고로딩 · 저 E/S | `Fig. 1` |
| §3 Computational & data-driven | 6–7 | 3.1 제1원리 선별 · 3.2 ML 서술자 · 3.3 실험 연동 고처리량 (전망) | 없음 |
| §4 Separators | 7–16 | 4.1 단독 · 4.2 공도핑 · 4.3 BP/RP · 4.4 P + 공공 | `Table 1` · `Fig. 2` · `Fig. 3` · `Fig. 4` |
| §5 Cathodes | 16–28 | 5.1 단독 · 5.2 공도핑 · 5.3 BP/RP · 5.4 P + 공공 | `Table 2` · `Fig. 5` – `Fig. 8` |
| §6 Conclusion | 28–30 | 기능 넷 · 과제 넷 · 전망 일곱 | `Fig. 9` |

---

## 3. 핵심 수치 총정리 ★ (전량 2차 소환 — 리뷰 자체 계산 · 실험 0)

> ⛔ 아래 수치는 **원전에서 리뷰를 거쳐 온 값**이다. 우리 db 값과 같은 표에 놓지 않는다 (CLAUDE.md §litdb). 원전 대조는 하지 않았다 (인용 원전 0 편 litdb 보유).

### 3a. 템플릿 물성 칸 — 우리 4축 기준

| 물성 | 값 | 조건 | 비고 |
|---|---|---|---|
| 이온전도도 σ (SE) | n/a | — | 고체 전해질 0 · 'Li⁺ 확산계수 향상' 은 액체 셀 정성 서술 [76] |
| 활성화 E Ea | n/a (SE) | — | BP 안 Li⁺ 확산 장벽 0.08 eV ([127] 경유 · 원 출처 표기 없음) — 고체 SE 아님 · 홉 수 검산 §3e |
| 산화 onset / ESW | n/a | — | 대신 Li–S 작동창 figure-read ≈ 1.7–2.8 V vs Li (§7) |
| 기계 (E/B/G) | n/a | — | — |
| 전자구조 | 'P 도핑 → 띠틈 감소' (P-g-C₃N₄ · PBE · 값 없음) · HOMO–LUMO 차 0.273 / 0.072 / 0.018 eV [그림 인쇄 · `Fig. 7a`] · d-band center −0.672 eV (P-RuSe₂) · ε_Co-d −1.279 eV (Co–Co₂P [그림 인쇄 · `Fig. 7g1`]) | 범함수 · 스미어링 · 적분 창 미기재 | §7 · §10a |
| 전자전도도 (재료) | N/P-LPC-900 **10.23 S cm⁻¹** [67] · BP ≈300 S m⁻¹ (= 3 S cm⁻¹ · 'metallic-like') [127] | 측정법 미기재 | 같은 리뷰 안에서 BP 를 'metallic-like' 와 'poor conductivity (semiconductor)' 로 동시에 부른다 (§10a-5) |

### 3b. 사례 수치 — 절별 (셀 성능 · 전부 액체 Li–S · 리뷰 재인용)

E/S 단위는 PDF 화면 기준 μL mg⁻¹ (머리 주석 ④).

| 절 | 물질 [ref] | 수치 |
|---|---|---|
| §1 · §5.2 | N/P-LPC-900 (N,P 공도핑 다공 탄소 · 900 °C · 인산칼륨 활성) [67] | 전도도 10.23 S cm⁻¹ · N 1.76 % · 'Li₂S₂ → Li₂S 의 ΔG 크게 감소' (값 없음) · in situ Raman 으로 2 단 셔틀 억제 |
| §1 · §5.2 | Co/Co₂P-NPSC (N,P,S 공도핑 탄소 나노케이지) [68] | 0.1C 초기 1291 mAh g⁻¹ (E/S ≈ 10) · 1.0C 500 사이클 후 465 · 0.087 %/사이클 · E/S 5.2 에서 0.1C 880 · ε_Co-d −1.279 eV [그림 인쇄] |
| §2.4 · §4.1 | Fe-NPC@rGO (P 도핑 Fe 단원자 촉매) [79] | Li 흡착 −1.86 → **−2.25 eV** (Fe-NC@rGO → Fe-NPC@rGO) |
| §4.1 | P-CeO₂ 나노막대 [96] | 'Li 흡착 −2.25 eV' — ⚠ [79] 와 **같은 수 · 거의 같은 문장** (§10a-4) |
| §2.7 | PNKB (P,N 공도핑 Ketjenblack) [76] | 1C 200 사이클 후 553 mAh g⁻¹ · S 4 mg cm⁻² · E/S 7 |
| §2.7 · §3.1 · §5.2 | P-RuSe₂/NC [73] | 면적 용량 7.7 mAh cm⁻² · S 8.0 mg cm⁻² · E/S 5.0 · d-band center −0.672 eV ('E_F 가까이') · '계산으로 P 를 골랐다' |
| §2.7 · §5.3 | c-FBP–NC (소수층 BP + N 도핑 탄소 공유결합) [81] | S 8.74 mg cm⁻² · E/S 5.7 · 50 사이클 후 6.37 mAh cm⁻² · 파우치 0.5C 초기 794 mAh g⁻¹ · 200 사이클 70 % (S 4 · E/S 3.5) |
| §4.1 | P-TiN 중간층 [98] | 0.1C 320 사이클 후 358 · 1C 380 mAh g⁻¹ |
| §4.1 | CoPG (P 도핑 소수층 흑연 + Co) [99] | 2.0C 300 사이클 후 694 mAh g⁻¹ (0.11 %/사이클) · 5.8 mg cm⁻² 125 사이클 92 % |
| §3.1 · §5.1 | P-g-C₃N₄ (제1원리 · PBE) [64] | 흡착 에너지 크기 **+48–77 %** (P_C 배치 · 순수 g-C₃N₄ 대비) · Li₂S 분해 장벽 **−10–18 %** (절대값 없음) |
| §5.1 | NbP/PC [114] | 1C 1150 사이클 0.04 %/사이클 · Ah 급 파우치 **451 Wh kg⁻¹** 20 사이클 · 'NbP–LiNO₃ 0.5 vs PC–LiNO₃ 0.1 eV' (⚠ 색 막대 오독 · §10b-2) |
| §5.2 | NP-PA [116] | 400 사이클 후 677.6 mAh g⁻¹ |
| §5.2 | PCS900 [117] | 1C 초기 737 mAh g⁻¹ · '0.079 % per 500 cycles' (원문 표기 그대로) |
| §5.2 | S@NPCNC@rGO [125] | S 6 mg cm⁻² · 0.39 A g⁻¹ 첫 사이클 6.7 mAh cm⁻² → 250 사이클 4.2 mAh cm⁻² |
| §5.3 | BP/N–C [108] | 0.2C 초기 1009.6 → 150 사이클 879 mAh g⁻¹ · 1C 300 사이클 626.42 mAh g⁻¹ · 평균 CE 99.8 % |
| §5.3 | NiCoP/BP [127] | BP 의 Li⁺ 확산 장벽 0.08 eV · 전도도 ≈300 S m⁻¹ |
| §5.4 | P-TiO₂₋ₓ [74] | 초기 1174.9 mAh g⁻¹ · 600 사이클 0.086 %/사이클 |
| §5.4 | P-FeS₁₋ₓ [75] | Li₂S₄ → Li₂S₂ 핵심 장벽 **> 30 %** 감소 (절대값 없음) |

### 3c. `Table 1` (분리막 10 행) · `Table 2` (양극 9 행) 전사 — PDF 텍스트

열: 물질 · 형태 (줄임) · S 로딩 [mg cm⁻²] & S 비율 [%] · 용량 / 사이클 / 전류 / 사이클당 감쇠 · rate · ref.

**`Table 1` 분리막**

| 범주 | 물질 | 형태 | S & % | 용량/사이클/C/감쇠 | rate | ref |
|---|---|---|---|---|---|---|
| 단독 P | MPC | 3D 계층 다공 나노시트 배열 | 1.5 & NA | 912/800th/1C/0.056 % | 854.1/1C | 62 |
| 단독 P | Pal@P-C | P 도핑 탄소 껍질 1D 나노막대 | 1.0–2.0 & ∼54 | 401/700th/2C/0.06 % | 401/5C | 91 |
| 단독 P | LC-CoSeP/rGO | 저결정 나노입자 on rGO | NA & NA | 897.7/1100th/1C/0.045 % | 569.4/5C | 92 |
| 단독 P | P-CoS₂/CNT | 속 빈 P-CoS₂ 나노박스 + CNT | 1.1–1.4 & ∼56 | 1027.1/580th/2C/0.066 % | 802.6/5C | 63 |
| 공도핑 | MNPG | Mo₂C in N,P 공도핑 비정질 탄소 on rGO | 1.2 & NA | 928.4/200th/0.2C/0.095 % | 802/5.0C | 40 |
| 공도핑 | BCN | B,P 도핑 g-C₃N₄ · Super P/PVDF 코팅 ∼30 μm | NA & NA | 1050/500th/1C/0.08 % | 649/3C | 93 |
| 공도핑 | P-Co₃O₄/NCNT | Co–O–P · 격자 전위 풍부 | NA & NA | 1649.6/500th/1C/0.12 % | NA | 94 |
| BP/RP | Hollow HCNS@PP | 속 빈 다공 P 도핑 탄소 나노시트 | 1.2 & NA | 601/500th/1C/0.065 % | 604/5C | 95 |
| P + 공공 | P-Ov–TiO₂/PP | (101) 면 팔면체 TiO₂ · P + O 공공 | NA & ∼64 | 1049/500th/1C/0.064 % | 871/5C | 86 |
| P + 공공 | P-Ov–In₂O₃/PP | P 도핑 In₂O₃ 나노구 · O 공공 | 1.0 & NA | 867/500th/1.0C/0.069 % | 656/5.0C | 85 |

**`Table 2` 양극**

| 범주 | 물질 | 형태 | S & % | 용량/사이클/C/감쇠 | rate | ref |
|---|---|---|---|---|---|---|
| 단독 P | P-MoTe₂/CC | 탄소천 위 P 도핑 초박 MoTe₂ | 2 & NA | 957.5/1000th/1C/∼0.031 % | 451.7/4C | 104 |
| 단독 P | TiN/PI | 전기방사 PI 나노섬유 + TiN | 1.5 & NA | 630/140th/1C/NA | NA | 105 |
| 공도핑 | NPC@CNTs | N,P 공도핑 벌집 탄소 + CNT 자립막 | NA & NA | 744.3/200th/0.3C/0.07 % | 559.2/1C | 83 |
| 공도핑 | N/P-LPC-900 | 그래핀형 다공 박막 탄소 | 1 & ∼55.3 | NA/400th/1C/NA | 610/2C | 67 |
| 공도핑 | 3D-PNMC | 3D 계층 메조/마이크로 다공 탄소 | 4.2 & ∼55.6 | NA/500th/0.5C/0.05 % | 719.2/2C | 106 |
| BP/RP | BP@FeCoO/S | 비정질 FeCoO 코팅 BP · 1–2 nm 기공 · O 공공 | 1.5 & 80 | NA/500th/1C/0.040 % | 644.3/5C | 107 |
| BP/RP | BP/N–C/S | 유채 꽃가루 유래 다공 탄소 + BP | NA & 70 | 1009.6/150th/0.2C/0.08 % | 507.5/5C | 108 |
| P + 공공 | CNT@Co₃O₄₋ₓ-P/S | CNT + 결함 Co₃O₄ · O 공공 + P | 1.8–6 & ∼47.6 | 903/200th/2C/∼0.11 % | 706/3C | 66 |
| P + 공공 | P-FeS₁₋ₓ@CNF | CNF 위 FeS₁₋ₓ · P 가 S 공공 자리를 차지 | 1.2 & ∼36.9 | 695.5/800th/1C/NA | NA | 75 |

### 3d. 표 의미 검산 (우리 산술 · 리뷰 값만 사용)

머리줄 *"Capacity/cycle number/current density/decay rate per cycle"* 는 '그 사이클의 용량' 으로 읽힌다. 선형 감쇠로 첫 용량을 되짚으면 C₀ = C / (1 − N·r).
- **BCN** 1050 · 500 · 0.08 % → C₀ ≈ 1750 · **LC-CoSeP/rGO** 897.7 · 1100 · 0.045 % → C₀ ≈ 1778 · **P-Co₃O₄/NCNT** 1649.6 · 500 · 0.12 % → C₀ ≈ 4124 mAh g⁻¹ — 셋 다 이론 용량 1675 (리뷰 p.1) 을 넘는다 ⇒ 이 행들의 '용량' 은 **첫 용량**이어야 한다. **BP/N–C/S** 는 본문이 직접 확인해 준다 (1009.6 = 0.2C 초기 · 150 사이클 후 879 · 감쇠 (1009.6 − 879)/1009.6/150 = 0.086 %/사이클 → 표의 0.08 %).
- 반면 MNPG · Hollow HCNS · NPC@CNTs 등은 어느 쪽으로 읽어도 가능하다 ⇒ **한 열 안에 '첫 용량' 과 '남은 용량' 이 섞였을 수 있는데 표는 구분하지 않는다.**
- **P-Co₃O₄/NCNT 1649.6 mAh g⁻¹ @1C** 는 이론 용량의 98.5 % — 첫 용량이라도 1C 값으로는 믿기 어렵다 (원전 미대조).
- **Pal@P-C** 는 사이클 열과 rate 열이 둘 다 **401** (2C 700 사이클 · 5C) — 옮겨 적기 의심 (원전 미대조).
- **TiN/PI** (ref 105) 는 본문 §5.1 에서 'P 도핑 다공 탄소 (PPC) 숙주' 로 소개되는 논문인데, 표 행의 형태는 같은 논문의 **TiN/PI 분리막** 이다 — '단독 P 도핑 양극' 범주에 P 가 없는 물질이 적혔다.
- **두 표 모두 E/S 열이 없다** — §2.7 과 전망 (6) 이 '실용 조건' 의 핵심으로 든 지표다. S 로딩도 19 행 중 NA 6 · 최대 4.2 (단일 값) / 1.8–6 (범위) mg cm⁻² — `[Wu26LiSRev]` (§J-52) 가 실용 목표로 든 > 5 mg cm⁻² 에 닿는 행은 범위 표기 하나뿐이다.

### 3e. DFT 서술자 값 (원전 2차 인용) + 규율 검산

| 값 | 출처 | 우리 규율로 다시 읽기 |
|---|---|---|
| Li₂S₆ 흡착 E_a: MNPG −2.43 · MNG −2.08 · MPG −2.39 · MG −1.59 eV [그림 인쇄 · `Fig. 3a1`] | Kim [40] | ≳ 2 eV → 배위 규칙 (`D-2026-10-05-adsorption-site-coordination`): 구조 비공개 · 그림상 Li₂S₆ 는 **도핑 탄소가 아니라 그 위 Mo 함유 슬랩 표면**에 붙는다 → 배위 미확인 · 'P 효과' 는 지지체를 거친 간접 효과 |
| MNPG 위 Li₂S −3.761 · Li₂S₂ −4.247 · Li₂S₄ −3.076 · Li₂S₆ −2.427 · Li₂S₈ −2.643 eV [그림 인쇄 · `Fig. 3a2`] | Kim [40] | 2.4–4.2 eV = 화학결합 규모 · 배위 미확인 → '그 자리의 결합 포화 에너지' 로만 · 해리 흡착 여부 불명 |
| Li₂S₆ 결합: N@C −1.8 · P@C −1.3 · WP −2.8 eV [그림 인쇄 · `Fig. 3d1`] · 막대 (`Fig. 3d2` figure-read ≈): N@C −1.8 ~ −1.97 · **P@C −1.27 ~ −1.63** · WP(211) −2.37 ~ −4.79 (Li₂S ≈ −4.55 · Li₂S₂ ≈ −4.8 · Li₂S₄ ≈ −2.4 · Li₂S₆ ≈ −2.8 · Li₂S₈ ≈ −4.3) | Li [102] | **P@C 가 다섯 종 모두 N@C 보다 약하다** — 'P 고유의 강한 화학흡착' 서술과 반대 · WP 의 Li₂S₈ (≈ −4.3) > Li₂S₆ (≈ −2.8) 비단조 → 해리 흡착일 공산 (구조 비공개 · 확인 불가) |
| Li 흡착 −1.86 → −2.25 eV | Pato [79] (+ P-CeO₂ [96] 같은 수) | 기준 상태 (고립 Li 원자 vs Li 금속) 미기재 — Li 금속 응집에너지 ≈ 1.6 eV/원자 [일반 지식 · 리뷰 밖] 만큼 뜻이 달라진다 · 배위 미확인 |
| HOMO/LUMO: FeTe₂@NC-Li₂S −4.979/−4.706 (차 0.273) · FeTe₂₋ₓ@NC-Li₂S −4.789/−4.717 (0.072) · P-FeTe₂₋ₓ@NC-Li₂S −4.762/−4.744 (0.018 eV) [그림 인쇄 · `Fig. 7a`] | Li [120] | 주기 슬랩 복합체의 'HOMO–LUMO' — 0.018–0.273 eV 는 통상 쓰는 스미어링 폭 (수십–수백 meV) 과 같은 자릿수라 순서가 스미어링 · k 에 민감하다 [우리 해석] · 캡션의 'Li₂S₆' 은 그림에서 **Li₂S** |
| d-band center: P-RuSe₂ −0.672 eV · Co–Co₂P ε_Co-d −1.279 eV [그림 인쇄 · `Fig. 7g1`] | Li [73] · Guo [68] | 적분 창 (점유만? 전체?) · 스핀 미기재 → 서로도 비교 불가 · RuSe₂ 는 반도체인데 'E_F 가까운 d-band center → 전도도↑' 는 다른 개념을 섞은 것 |
| ΔG 사다리 (`Fig. 8f` [그림 인쇄]): V@N₄-CP −1.55 / −3.10 / −1.28 / −1.25 / −0.43 / **+2.81** · Ni@N₄-CP −1.08 / −2.84 / −1.07 / −0.94 / −0.34 / **+3.49 eV** (S₈ → *S₈ → *Li₂S₈ → *Li₂S₆ → *Li₂S₄ → *Li₂S₂ → *Li₂S) | Xia [128] | 마지막 단계 (율속) 는 **V 가 낮다** — 본문 'Ni 쪽 율속 장벽이 훨씬 낮다' 와 반대 (§10b-1) · 반응식 · 전위 U · 용매화 · 기준 0 줄 · 이것은 반응 자유에너지이지 장벽이 아니다 ↓ |
| 위 +2.81 / +3.49 eV 를 장벽으로 읽으면 | — | 홉 수 검산 (ν₀ 10¹³ s⁻¹ 가정 · 298 K): **2.81 eV** Γ ≈ 3.0×10⁻³⁵ s⁻¹ · 평균 대기 ≈ 3.3×10³⁴ s · 3600 s 동안 N ≈ 1.1×10⁻³¹ 회 · **3.49 eV** Γ ≈ 9.5×10⁻⁴⁷ s⁻¹ · 평균 대기 ≈ 1.1×10⁴⁶ s · 3600 s 동안 N ≈ 3.4×10⁻⁴³ 회 (`tools/sei/collect_neb.py::hop_check`) — 실제 셀은 한 시간 안에 Li₂S 를 만든다 ⇒ '장벽' 으로 읽으면 차수가 안 맞는다 |
| BP 안 Li⁺ 확산 장벽 0.08 eV | [127] (원 출처 표기 없음) | 홉 수 검산 (ν₀ 10¹³ s⁻¹ 가정 · 298 K): Γ ≈ 4.4×10¹¹ s⁻¹ · 평균 대기 ≈ 2.3×10⁻¹² s — '빠르다' 서술과 모순 없음 |
| Li₂S 분해 장벽 −10–18 % [64] · Li₂S₄ → Li₂S₂ 장벽 −30 % 초과 [75] | — | **절대값이 없어 홉 수 검산 불가.** 속도비는 exp(f·Ea/kT) 라 Ea 를 모르면 뜻이 없다 — 예시 (Ea 1.0 eV **가정** · 298 K · ν₀ 상쇄): 10 % → ×49 · 18 % → ×1.1×10³ |

---

## 4. DFT / 계산 방법 ★ (리뷰가 옮긴 계산 조건 전부)

- **code / version**: n/a (0 회)
- **functional + vdW**: `Fig. 5a` 캡션의 *"with the PBE functional"* (P-g-C₃N₄ [64]) **1 회** 가 전부 · vdW 0 회 — LiPS/탄소 흡착은 분산 보정에 크게 기대는 양인데 표기가 없다.
- **pseudo / PAW · k · ecut · 셀 · nat**: n/a
- **DFT+U · 스핀**: n/a (0 회) — Co₃O₄ · CeO₂ · MnO₂ · Fe/Co 단원자 촉매처럼 U · 자화 상태가 흡착값을 바꾸는 계가 대부분인데 상태 선언이 없다 (회신 N 의 '선택 규칙 없는 스칼라' 위험 신호 · `[Guan26FeCo]` §J-66 과 같은 유형).
- **용매화 · 전위**: n/a — ΔG 사다리 (`Fig. 8f`) · 'ΔG of Li₂S₂ → Li₂S' 에 계산 수소 전극식 · U · 암시적 용매 언급 없음.
- **장벽 계산법**: 'energy barrier' 37 줄 · NEB 0 회 — Li₂S 분해 장벽이 어떤 경로 (Li₂S → LiS + Li 해리?) 인지 0 줄.
- **AIMD · MLIP**: 없음 (짧은 MD '무반응' 서술도 없음 → 관측창 규칙 해당 없음). ML 은 §3.2 의 두 사례 — 그래핀 단원자 촉매 데이터베이스 → *ortho*-P₂C₂ [88] · BP 위 전이금속 단원자 + **SISSO** 서술자 → Ti-BP · V-BP · ML 예측 Hf-BP [89]. 모델 · 데이터 크기 · 검증 0 줄.
- **무질서 처리**: P 자리 배치 비교는 [64] 하나 ('P–C 배치' — 그림 라벨은 P_C) · 나머지는 단일 배치로 보인다 (리뷰에 기재 없음).
- **특이사항**: §3 *'Computational and data-driven approaches'* 는 1 쪽 남짓 · 원전 다섯 편 요약 (계산 조건 0 줄) · '실험 연동 고처리량' 은 이온성 액체 36 000 종 계산 선별 + 6 종 실험 [90] 을 예로 든 제안이다.

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 §1 서론 (pp.1–3)

- Li–S: 이론 용량 1675 mAh g⁻¹ · 에너지 밀도 2600 Wh kg⁻¹ ('LIB 의 거의 6 배'). 다섯 문제 — ① S · Li₂S/Li₂S₂ 절연 ② S₈ ↔ Li₂S 부피 ≈ 80 % ③ LiPS 용해 · 셔틀 ④ 느린 산화환원 · Li₂S 의 2D 석출 → '죽은 영역' ⑤ Li 덴드라이트 · SEI. 다섯이 서로 되먹임한다 (p.2 — 마무리 문장이 두 번 연달아 인쇄됨).
- 다른 도핑: N (극성 · 전도) · S (Si–C 복합체 가교) · O (MoS₂ 층간) · I (C–I 결합 · 띠틈 감소) · 금속 원자. 그다음 P 의 '고유 장점' 셋 (§2 표).
- 'P 도핑 공학' 정의 (p.2): 격자 · 탄소 골격 · 표면에 P 를 의도적으로 넣어 전자구조 조절 · 활성 자리 · 전자/이온 전도 · LiPS 화학흡착 · 촉매를 얻는 설계 전략.
- 약속 (p.3): 황 로딩 · S 함량 · E/S · 에너지/출력 밀도 · **준고체 · 전고체 계면 매개** · 응용 (휴대 · EV · 계통) 을 다룬다 — 본문에서 실제로 다룬 것은 §2.7 한 문단과 전망 (4) 다 (§10a-7).

### 5.2 §2 기전 (pp.3–6 · `Fig. 1`)

- **2.1 흡착**: P 의 '높은 전기음성도' 와 비공유 전자쌍 → 극성 표면 → Lewis 산–염기로 LiPS 고정 · P–S · Li–P 결합. 사례: MPC (P–C · P–O · Li–P · S–P 로 '금속 같은 고정') [62] · P-CoS₂ (Co–O–P 표면 산화층 · Li–P · P–S) [63] · UiO-66@BP (P–S) [71] · CVD P 도핑 탄소 중간층 (P–S · Li–P · **Li₃PO₄**) [72].
- **2.2 속도**: SRR · SOR 의 고체–액체–고체 전이 · 율속 = 'Li₂S₄/Li₂S₄ → Li₂S₂/Li₂S' (원문 표기 그대로 — 앞쪽 Li₂S₄ 가 겹친 오기) 와 Li₂S 분해. 기전 넷: ① 비공유쌍 · d-band center 를 E_F 쪽으로 → S–S 늘림 · 끊기 ② 전이금속 인화물 (CoP · FePₓ · Co–O–P) ③ 결함 · 공공 · 저결정 → 불포화 배위 ④ Li₂S 핵생성 가속 · 산화 과전압 감소. 사례 수치는 §3b.
- **2.3 전도**: '띠틈을 좁혀 · P–C 극성 결합 · 운반자 농도↑' — N/P-LPC-900 10.23 S cm⁻¹ · P-TiO₂₋ₓ · PNKB (전해질 젖음 · Li⁺ 확산계수) · P-Fe₄N@NPG · P-RuSe₂ (d-band center).
- **2.4 덴드라이트 · 구조**: 친Li 자리 → 핵생성 과전압↓ · 분리막/중간층의 P 가 음극 쪽 계면층 유도 · P–C · P–O · P–N · M–P 결합으로 구조 안정. Fe-NPC@rGO Li 흡착 −1.86 → −2.25 eV [79] · Cu@BP (계산) [80] · c-FBP–NC (P–N) [81] · Co@PNC (전자적 금속–지지체 상호작용) [82].
- **2.5 상승**: N (Li–N 염기 자리 · 전도) + P (P–S · Li–P 극성 자리 · 촉매) · O 공공 · S 공공 안정화. NPC@CNTs [83] · PNKB [76] · P,Mo-MnO₂ (P = Li₂S 핵생성 ΔG↓ · Mo = 분해 장벽↓) [84] · P-Ov–In₂O₃ [85] · P-Ov–TiO₂ (d-band center · Ti–S) [86].
- **2.6 이종구조**: BP 나노시트 · 금속 인화물 + 탄소 · MXene · 산화물 · 황화물 → '계면 내장 전기장' 이 전하 분리를 돕는다 (근거 인용 없음 · `[Liu26LiInS]` §J-82 와 같은 꼴의 논증). UiO-66@BP 'blockage–adsorption–catalysis' [71] · P-CoSe₂/MXene (P 가 혼합상 → 순수 사방정 CoSe₂ · 인장 변형 · d-band 상향 · Se 자리 Bader 전하 증가) [87] · Co/Co₂P [68].
- **2.7 고로딩 · 저 E/S**: PNKB · P-RuSe₂/NC · c-FBP–NC 수치 (§3b) · "전해질 제약이 달라 비교할 때 주의" 단서. 여기서 `Fig. 1` 을 인용한다.
- **`Fig. 1`** (실독): 네 범주 바퀴 — 단독 P · P + 이종원자 · BP/RP · P + 공공 — 칸마다 원전 그림 썸네일 (출처 표기 없음).

### 5.3 §3 계산 · 데이터 기반 (pp.6–7 · 그림 없음)

- 3.1: P-g-C₃N₄ 배치 비교 → 'P–C 배치' 가 흡착 크기 48–77 % 증가 · "P 의 존재가 아니라 **위치**가 상호작용을 정한다" [64] · P-RuSe₂ 는 흡착과 Li₂S 전환의 **균형**으로 골랐다 [73] → "흡착 세기만이 아니라 고정과 전환을 함께 보는 선별 기준".
- 3.2: 그래핀 단원자 촉매 (금속 × 이종원자 × 배위) DFT + ML → *ortho*-P₂C₂ 가 SRR 에 유망 · 이종원자 p 궤도 ↔ 금속 d 궤도 상호작용 [88] · BP 단층 위 금속 원자 DFT + ML → Ti-BP · V-BP 유망 · Hf-BP 는 ML 예측 · SISSO 서술자가 Li₂S 분해 장벽을 금속 고유 성질과 잇는다 (치환 P 도핑과는 다른 계라는 단서 포함) [89].
- 3.3: 고처리량 실험 연동은 '앞으로의 방향' — 조성 라이브러리 · 병렬 특성분석 · 통제된 S 로딩 · E/S · Li 과잉 조건 평가 → 모델 정교화.
- **판독**: 이 절의 문장 자체는 우리 보고량 규율과 같은 말이다 ('흡착만 보지 말고 전환과 함께' · '조건을 통제해서'). 그런데 같은 리뷰의 §4–§5 는 이 기준을 사례에 적용하지 않는다 — 흡착 세기 '증가' 를 계속 장점으로 센다.

### 5.4 §4 분리막 (pp.7–16 · `Table 1` · `Fig. 2` · `Fig. 3` · `Fig. 4`)

- **4.1 단독 P** (`Fig. 2`): P 는 '3p 와 3d 궤도의 비공유쌍' 으로 강한 Lewis 염기 (⚠ §10a-2) · P-CeO₂ 나노막대 (`Fig. 2a` SEM) [96] · MPC (MgO → Mg(OH)₂ 주형 + 레조르시놀 · 포름알데히드 · phytic acid → 탄화 → HCl 식각 · `Fig. 2b`) [62] · CVD P 도핑 탄소 중간층 + PE (`Fig. 2c`) [72] · Pal@P-C (팔리고스카이트 + PPh₃ · 750 °C 2 h · `Fig. 2d`) [91] · LC-CoSeP/rGO (NaH₂PO₂ 인화 → 저결정 · 댕글링 본드 · `Fig. 2e`) [92] · P-CoSe₂/MXene (P 가 Se 치환 · `Fig. 2f`) [87] · P-CoS₂ 나노박스 (MOF 주형 → 황화 → 인화 · `Fig. 2g`) [63] · P-MoS₂ 3D 망 (NaCl 주형 · `Fig. 2h`) [97] · P-TiN 중간층 (`Fig. 2i`) [98] · Fe-NPC@rGO (`Fig. 2j` — 그림상 P 원은 **적린**) [79] · CoPG (`Fig. 2k` HRTEM) [99]. 리뷰가 든 한계: 흡착 중심 중간층은 고전류에서 Li₂S 속도를 못 따라간다 · P 함량 ↔ 전도도 상충 (과도핑 → 전하 수송 악화).
- **4.2 공도핑** (`Fig. 3`): MNPG (Mo₂C + N,P 탄소 · `Fig. 3a` DFT) [40] · Ru@PCSR (곰팡이 균사 유래 탄소) [100] · NPCNF@s-Ni₂P 저온 Li–S (`Fig. 3b` — 단면 두께 51 μm [그림 인쇄]) [101] · BCN (B,P 도핑 g-C₃N₄ · 'DFT 가 이끈 설계 + 실험 검증' · `Fig. 3c`) [93] · P,Mo-MnO₂ [84] · WP@NPC (`Fig. 3d` DFT) [102] · P-Co₃O₄/NCNT (`Fig. 3e` HAADF · EDS) [94] · CoPNC (Co–N₄ → Co–P₂N₂ · XAS · `Fig. 3f`) [65]. 결론: 공도핑은 '단순 합이 아닌 협동'.
- **4.3 BP/RP** (`Fig. 4a–c`): "BP · RP 는 그 자체로 우수한 전자 · 이온 전도체" (⚠ §10a-5) · 속 빈 HCNS (BP 주형 · 음/양 되먹임 고리 개념도 `Fig. 4a`) [95] · UiO-66@BP (P–O–Zr · `Fig. 4b`) [71] · RP–BP@G (볼밀 · 난연) [103]. 과제: BP 의 공기 불안정 · 대량 생산.
- **4.4 P + 공공** (`Fig. 4d,e`): P-Ov–TiO₂ (101) (2 상 계면 가수분해 · `Fig. 4d`) [86] · P-Ov–In₂O₃ (222) (흡착 구조만 · `Fig. 4e`) [85]. 'P 가 S–S · Li–S 결합 절단을 가속 · O 공공이 전자 축적' 정성 서술.

### 5.5 §5 양극 (pp.16–28 · `Table 2` · `Fig. 5` – `Fig. 8`)

- **5.1 단독 P** (`Fig. 5`): P-g-C₃N₄ 제1원리 (`Fig. 5a` · PBE · 0.02 e Å⁻³) [64] · P-MoTe₂/CC ('강한 전기음성도' 로 d-band center 를 E_F 쪽 · d–p band center 차 축소 · `Fig. 5b`) [104] · PCDC (CO₂ 유래 탄소 + H₃PO₄ · C₃PO · C₂PO₂ · `Fig. 5c` — ⚠ 본문의 공정 서술이 그림과 다름 · §10b-5) [109] · TiO@X-HMCFs (`Fig. 5d`) [110] · PPC + 섬유 매트 (`Fig. 5e`) [105] · P 도핑 탄소 폼 (`Fig. 5f`) [111] · 목화대 탄소 (H₃PO₄ 활성) [112] · P-NiB (B → P 전자 이동 · B 2p 점유 감소 · B–S p–p 상호작용 · operando XRD `Fig. 5g`) [113] · Li₂S@P-CNFs ‖ P-CNFs 무음극 전지 (`Fig. 5h`) [78] · NbP/PC (LiF/Li₃N 풍부 계면층 · `Fig. 5i`) [114].
- **5.2 공도핑** (`Fig. 6` · `Fig. 7`): NP-CFs [115] · NPC@CNTs (Li₂S₆ 캐솔라이트) [83] · N/P-LPC-900 (`Fig. 6a`) [67] · NP-PA (`Fig. 6b` XPS) [116] · 3D-PNMC (`Fig. 6c` EDS) [106] · PCS900 (phytic acid · `Fig. 6d`) [117] · PNKB (`Fig. 6e` 로딩–C-rate 비교) [76] · NPCF/CoS₂ (부들 섬유 · `Fig. 6f`) [118] · 달걀흰자 탄소 [119] · P-FeTe₂₋ₓ@NC (`Fig. 7a` 프런티어 궤도) [120] · P-RuSe₂/NC (Se 일부를 P 로 · d-band −0.672 eV · CV 등고선 `Fig. 7b`) [73] · P₀.₁-Mo₀.₉Ni₀.₁S₂/CNT (`Fig. 7c` SEM) [121] · Co–N₂P₂ 단원자 촉매 (P 도핑 C₃N₄ 주형 · `Fig. 7d`) [122] · Co@PNC (`Fig. 7e` XPS) [82] · PCS900@RuP₂ (`Fig. 7f`) [123] · CoP@NP-CF [124] · Co/Co₂P-NPSC (폴리포스파젠 · NaH₂PO₂ 의 PH₃ 독성 회피 · `Fig. 7g`) [68] · S@NPCNC@rGO (`Fig. 7h`) [125] · P-Fe₄N@NPG (`Fig. 7i`) [77].
- **5.3 BP/RP** (`Fig. 8a–f`): BP@FeCoO (P–Fe/Co · `Fig. 8a`) [107] · BP/N–C (꽃가루 탄소 · Li₂S 핵생성 `Fig. 8b`) [108] · c-FBP–NC (P–N 공유결합 · 'FBP 는 반도체라 전도가 나쁘다' · `Fig. 8c`) [81] · BP@C–CoP (`Fig. 8d` XPS) [126] · NiCoP/BP (Mott–Schottky 내장 전기장 · in situ Raman `Fig. 8e`) [127] · V/Ni@N₄-CP (`Fig. 8f` ΔG 사다리) [128] · Cu@BP (계산 · Cu 를 BP 반대면에 두는 '간접 조절') [80].
- **5.4 P + 공공** (`Fig. 8g–i`): P-TiO₂₋ₓ 미소구 (`Fig. 8g`) [74] · CNT@Co₃O₄₋ₓ-P (operando Raman `Fig. 8h`) [66] · P-FeS₁₋ₓ (P 가 S 공공을 메워 안정화 · operando EXAFS `Fig. 8i`) [75]. '이중 결함' 효과가 단일 결함을 '훨씬 넘는다' (대조 수치 없음).

### 5.6 §6 결론 · 전망 (pp.28–30 · `Fig. 9`)

- 기능 넷: 흡착 · 셔틀 억제 / 전자구조 · 전도 / 촉매 · 속도 / 상승 + (일부) 친Li 자리로 덴드라이트 억제.
- 과제 넷: ① BP 공기 산화 등 안정성 ② 도핑 농도 · 분포 · 결함 협동 배치 제어 → 재현성 ③ 독성 P 원료 · 고온 다단 공정 ④ 원자 수준 기전 미해명.
- 전망 일곱 (`Fig. 9` 바퀴와 1:1): ① in situ + 다중 척도 계산으로 P 활성 자리의 동적 진화 ② 농도 · 분포 · 국소 배위 정밀 제어 — 원리 (이웃 원자 조절 · 공공 짝 · 흡착 ↔ Li₂S 가역 형성/분해 균형) 는 N · O · S 도핑에도 옮길 수 있으나 그대로 베끼지 말 것 ③ 상보적 다원소 도핑 — **충분한 흡착 vs 유리한 Li₂S 핵생성 · 산화 분해의 균형** ④ 음극 · 전해질 · 바인더 · LiNO₃ 없는 실용 전략 · **준고체 → 전고체 전이에서 '촉매 중간층 · 이온전도 첨가제'** (이 문단 인용 0) ⑤ 급속 충전 ⑥ 파우치 · 고로딩 · 저 전해질 · 제한 Li · 넓은 온도 ⑦ 롤투롤 · 열 차단 등 산업화.

---

## 6. Figure set ★

| Fig | 내용 (무엇을 보여주나 — 실독) | 우리 활용 |
|---|---|---|
| 1 | 네 범주 분류 바퀴 (단독 P · P + 이종원자 · BP/RP · P + 공공) · 원전 썸네일 (출처 표기 없음) | 없음 — 범주 이름만 |
| 2 | (a) P-CeO₂ 막대 SEM (b) MPC 합성 (MgO → Mg(OH)₂ 주형 · phytic acid) (c) 유연 Li–S + P 도핑 탄소 중간층 (d) Pal@P-C (PPh₃ · 750 °C) (e) LC-CoSeP/rGO 인화 (f1) CoSe₂/MXene → P 가 Se 치환한 구조 (f2) d-band 상향 **만화 (숫자 없음)** (g) P-CoS₂ 나노박스 (h) P-MoS₂ 3D 망 (i) P-TiN 중간층 (j) Fe-NPC@rGO (P 원 = 적린) (k) CoPG HRTEM: 흑연 (002) 0.336 · Co (200) 0.177 · Co (111) 0.204 nm · 껍질 ≈3.4 nm [그림 인쇄] | ⚠ (k) 격자 무늬뿐인데 본문은 'P 도핑 성공 확인' · (f) '이론 통찰' 은 숫자 없는 그림 · Bader 값 없음 |
| 3 | (a1) Li₂S₆ 흡착 MNPG −2.43 · MNG −2.08 · MPG −2.39 · MG −1.59 eV — 흡착 자리는 **도핑 탄소 위 Mo 함유 슬랩 표면** (a2) MNPG 위 Li₂S −3.761 · Li₂S₂ −4.247 · Li₂S₄ −3.076 · Li₂S₆ −2.427 · Li₂S₈ −2.643 eV (b) NPCNF@s-Ni₂P SEM · 단면 51 μm (c) BCN TEM · SEM (d1) Li₂S₆: N@C −1.8 · P@C −1.3 · WP −2.8 eV (d2) 다섯 종 막대 — **P@C 가 전부 가장 약함** (e) P-Co₃O₄/NCNT HAADF · EDS (f) **Li‖Li 대칭 셀** 5 mA cm⁻² · 5 mAh cm⁻²: CoPNC ≈1330 h (분극 figure-read ≈ ±0.06–0.13 V) vs 맨 PP 는 ≈150 h 에서 불안정 | 흡착 배위 규율 사례 (≳ 2 eV 다수 · 배위 미확인) · (a1) 과 (d) 에서 P/N 서열이 **반대** (지지체 경유 vs 직접) · (f) 는 Li 석출 시험인데 본문은 Li₂S 분해 문단에 붙였다 |
| 4 | (a1,a2) 음/양 되먹임 고리 개념도 (b) BP → BP/Zr²⁺ (그림 라벨 · 본문은 Zr⁴⁺) → P–O–Zr → UiO-66@BP (c) RP–BP@G 기전 (d) P-Ov–TiO₂ 2 상 계면 합성 (e) Li₂S₈ … Li₂S 흡착 구조 (탄소 · In₂O₃ · Ov–In₂O₃ · P-Ov–In₂O₃ (222)) — **에너지 값 없음** | (e) 구조만으로 '단계 전환 촉진을 보였다' 는 본문은 과장 · 연결 없음 |
| 5 | (a1,a2) S₈ · Li₂Sₙ 전하 밀도 차 (g-C₃N₄ vs P_C · PBE · 0.02 e Å⁻³) — S₈ 는 두 기판 모두 등치면이 거의 없다 (b) P-MoTe₂/CC 셀 개념도 (c) CDC → PCDC 6 단계: 500 °C 2 h (CO₂ · NaBH₄) → 600 °C 기체 전환 → 700 °C 2 h (Ar) → 세척 → H₃PO₄ 함침 (5 h 교반 · 130 °C 16 h 건조) → 700 °C 40 min (Ar) → 세척 (d) TiO@HMCF 물리/화학 흡착 (e) 섬유 매트 포획 (f) PCF2 기전 — 라벨 **'Li–P' · 'O···LiSₓ²⁻'** (g) operando XRD NiB vs P-NiB — α-S₈ · β-S₈ · Li₂S · Be 창 (h) 무음극 Li₂S@P-CNFs ‖ P-CNFs (i1) 분자 4 개 정전위 지도 · 색 막대 **0.5 eV ↔ −0.1 eV** (i2) 결합 배치 (탄소 · NbP 위 NO₃⁻ · TFSI⁻) — **에너지 값 없음** | ⚠ (i) 리뷰의 'NbP–LiNO₃ 0.5 eV vs PC–LiNO₃ 0.1 eV' 는 색 막대 양 끝 · (c) 본문의 900 °C · KOH · 질산니켈 단계는 그림에 없다 · (f) 본문 'P–S · Li–O–Li' ≠ 그림 · (g) 본문의 γ-S₈ 은 그림에 없다 |
| 6 | (a) N,P 상승 개념도 (b1) NP-PA P 2p: **P–O (figure-read ≈ 134.0 eV) 가 주 · P–C (≈ 132.8 eV) 가 부** · 잡음 큼 (b2) N 1s 피리딘 · 피롤 · 흑연 N (c) S@3D-PNMC EDS (d) PCS900 합성 (멜라민 + phytic acid · N₂ 800 °C 1 h → 900 °C 3 h · S 155 °C 10 h + 280 °C 20 min) (e) 로딩–C-rate 비교: PNKB ★ (figure-read ≈ 3.9 mg cm⁻² · 1.0C · 200 사이클/553) vs 문헌 3.8–12 mg cm⁻² · 0.1–0.2C (f) NPCF/CoS₂ | P–O 우세 = P 산소 친화 (§7 · §9) · ⚠ (e) 본문 '고로딩 · 고율 사분면' 인데 PNKB 는 비교군 중 **가장 낮은 로딩 쪽** · E/S 축 없음 |
| 7 | (a) FeTe₂ / FeTe₂₋ₓ / P-FeTe₂₋ₓ @NC-**Li₂S** HOMO/LUMO (−4.979/−4.706 · −4.789/−4.717 · −4.762/−4.744 eV · 차 0.273 / 0.072 / 0.018 eV) (b1–b3) CV 등고선 (0.1–0.5 mV s⁻¹ · figure-read ≈ 1.7–2.8 V · 전류 색 0–9.4 mA) — P-RuSe₂/NC 가 가장 강함 (c) MoS₂ 계 SEM (d) Co–N₂P₂ 촉매 만화 (e) Co 2p · N 1s XPS (Li₃N 성분 표시) (f) PCS900@RuP₂ (g1) Co–Co₂P DOS · ε_Co-d −1.279 eV (비교 대상 없음) (g2) Co (Φ 4.1 eV · 금속) + Co₂P (Φ 5.0 eV · 'n 형 반도체') → **'Mott–Schottky'** (h) EDS (i) P-Fe₄N@NPG | ⚠ (a) 캡션 'Li₂S₆' ≠ 그림 'Li₂S' · 본문 'P-FeTe₂' ≠ 그림 'P-FeTe₂₋ₓ' · (g2) Φ 순서 (금속 < n 형) 면 쇼트키 장벽이 아니라 축적 접촉 — 이름과 그림이 어긋남 · (b) Li–S 창 figure-read |
| 8 | (a) BP@FeCoO@S 개념도 (b1) BP/N–C Li₂S 핵생성 전류: 정점 2380 s · 'Precipitation of Li₂S: 230.90.66 mAh g⁻¹' [그림 인쇄 · 소수점 둘 오기] (b2) SEM (c) c-FBP–NC 셀 · 'N–P covalent bond' (d1) Co 2p₃/₂: Co–P 779.1 → 779.2 · Co–O 781.2 → 781.3 · Co–N 782.8 → 783.0 · 위성 785.6 → 785.9 eV (d2) P 2p: **P–O 134.1 → 133.8** · P–Co 2p₁/₂ 130.6 → 130.4 · 2p₃/₂ 129.7 → 129.6 eV (Li₂S₆ 흡착 전 → 후 · [그림 인쇄]) (e1) NiCoP/BP in situ Raman — S₈ · Li₂Sₓ · Li₂S · **PS₄³⁻ (figure-read ≈ 415–418 cm⁻¹ · 첫 방전 줄부터 모든 줄)** · 전위 곡선 figure-read ≈ 1.7–2.8 V (e2) BP 단독 — PS₄³⁻ 표시 없음 (f) ΔG 사다리 V@N₄-CP · Ni@N₄-CP (§3e) — 율속 +2.81 (V) < +3.49 eV (Ni) (g) P-TiO₂₋ₓ 합성 (h) operando Raman (i) operando FT-EXAFS Fe–S/P · 방전 OCP → 2.18 → 2.08 → 2.06 → 1.99 → 1.73 V · 충전 2.23 → 2.24 → 2.29 → 2.38 → 2.60 V [그림 인쇄] | ★ (e1) PS₄³⁻ = 우리 SE 음이온 — P 촉매가 폴리설파이드 속에서 티오인산이 된다는 신호 (본문 0 회) · (f) 본문 'Ni 율속 장벽이 훨씬 낮다' 와 반대 · (d) 본문 'P–C 와 P–O 확인' ≠ 그림 (P–O · P–Co) · 이동 0.1–0.3 eV |
| 9 | 전망 바퀴: 1 기전 해명 · 2 정밀 설계 · 신소재 · 3 다기능 상승 설계 · 4 주류 Li–S 기술과 통합 · 5 성능 지향 최적화 · 6 실용 조건 검증 · 7 산업화 과제 (전망 7 항과 1:1) | 없음 |
| Table 1 | 분리막 10 행 (§3c) — E/S 열 없음 · '용량' 열 의미 혼재 (§3d) | 셀 수치는 인용 안 함 |
| Table 2 | 양극 9 행 (§3c) — TiN/PI 행 범주 혼선 · E/S 열 없음 | 셀 수치는 인용 안 함 |

---

## 7. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`

> ⛔ **수치 비교 행 0.** 계 (액체 Li–S 양극 숙주 vs argyrodite SE) 와 양 (흡착 · 촉매 서술자 vs 벌크 물성) 이 다르다. 아래는 '방법 규율이 같은 곳' 과 '화학이 이어지는 곳' 만 적는다. 우리 숫자는 규약이 꼭 필요한 전위창 한 줄에만 싣는다.

| 항목 | 이 리뷰 (전량 2차 소환) | 우리 (원장) | 같음 / 다름 · 이유 |
|---|---|---|---|
| 계 | 액체 전해질 Li–S 양극 숙주 · 분리막/중간층 (P 도핑 탄소 · 금속 인화물 · 산화물 · 칼코겐화물 · 단원자 촉매 · BP/RP) | argyrodite SE 벌크 · 슬랩 (comp1 Li₆PS₅Cl · modelc Li₅.₄PS₄.₄Cl₁.₆) | 다른 계 — 비교 대상 아님 |
| 계산 조건 | PBE 1 회 · 코드 · vdW · U · 스핀 · k · 컷오프 · 용매화 0 | QE PBE · 정본 `kb/methodology/computational_methods_canonical.md` | 리뷰 쪽은 재현 불가 |
| 띠틈 · '전도도 향상' | 'P 도핑 → 띠틈 감소 → 전도도↑' (P-g-C₃N₄ · PBE · 값 없음) · `Fig. 7a` HOMO–LUMO 차 0.018–0.273 eV | 띠틈은 fixed-occupation nscf 고유값만 · DOS 문턱 판독 금지 (~0.3 eV 과소) · PBE 과소 · 금속화 주장은 스미어링 · 셀 확인 (CLAUDE.md §데이터 규율) | 같은 규율이 리뷰 서술을 거른다: ① PBE 띠틈 '감소' 는 방향만 ② 0.018–0.273 eV 는 스미어링 폭과 같은 자릿수 ③ 띠틈 ≠ 전도도 (운반자 · 이동도 · 입자 간 접촉이 따로 있다) |
| band center | d-band center −0.672 eV (P-RuSe₂) · ε_Co-d −1.279 eV (Co–Co₂P) · Δband(d–p) (값 없음) · 적분 창 0 줄 | 우리 평균류 지표 (site mean-3p) 는 그림 창과 같은 창 (−8..0 eV) 으로 계산 · 인용 | 다른 양 (금속 d vs S 3p) · 창이 없어 리뷰 값끼리도 비교 불가 |
| 흡착 ≳ 2 eV | `Fig. 3a2` 2.4–4.2 eV · `Fig. 3d2` WP ≈ −2.4 ~ −4.8 · Li −2.25 eV — 구조 비공개 | `D-2026-10-05-adsorption-site-coordination` | 배위 미확인 → '그 자리의 결합 포화 에너지' 로만 · 표면 일반 흡착 세기 · 기전 근거로 쓰지 않는다 |
| '장벽' | % 감소 (10–18 · > 30) · ΔG 단계 (+2.81 / +3.49 eV) 를 장벽으로 · BP Li⁺ 0.08 eV | `D-2026-09-27-barrier-hop-count` · 우리 Li₂S 벌크 V_Li NEB (`HZ-sei-neb-li2s-cc-cellconv` · CONDITIONAL) | ⛔ 다른 양 (표면 분자 해리 · 반응 ΔG vs 벌크 공공 홉) — 같은 표 금지 · 리뷰 쪽은 §3e 홉 수 검산으로 거른다 |
| ΔG 사다리 | `Fig. 8f` · 반응식 · U · 용매화 · 기준 0 줄 | 우리는 CHE 식 사다리를 계산하지 않는다 · 산화환원은 grand-potential (Li 화학퍼텐셜 축) | 방법 축이 다르다 — n/a |
| P–S 결합 | 'P–S 결합이 LiPS 를 잡는다' (XPS · 정성) · `Fig. 8e1` PS₄³⁻ Raman figure-read ≈ 415–418 cm⁻¹ (본문 언급 0) | PS₄³⁻ 안 P–S = 우리 SE 의 골격 결합 (LOBSTER per-bond ICOHP · `ICOHP_PS@comp1` canonical) · `[Cronk26]` 계면상 카드 (`cronk2026_lis_cathode_interphase_chemistry`): LPSCl 425.8 → S 와 밀링 420.4 cm⁻¹ · β-LPS 기준 418 | 수치 비교 아님 — **화학이 이어진다**: P 가 폴리설파이드와 'P–S 결합' 을 끝까지 만들면 티오인산 (Li₃PS₄-like · Li₃PS₄₊ₙ) 이 된다. 같은 Raman 띠 자리다 |
| P–O 선호 | XPS P 2p 주성분이 P–O (`Fig. 6b1` · `Fig. 8d2`) · CVD 중간층의 Li₃PO₄ [72] · Co–O–P 표면층 [63] · P–O–Zr [71] | B₂O₃ 도핑 모델에서 O 는 B 가 아니라 P 에 붙었다 (DFT 가 UMA 최저 배치를 뒤집음 · `kb/methodology/b2o3_doping_chemistry.md` §6e–6g) · 산화환원 경계 카드: Li₃PO₄ 는 O 의 가장 안정한 거처 (`kb/concepts/se_redox_frontier.md` §4) | 방향 일치 (정성) — P 는 O 를 문다. 'P 도핑 탄소' 의 활성 P 상당수는 P–O 다 [우리 해석] |
| 전위창 | Li–S 작동 figure-read ≈ 1.7–2.8 V vs Li (`Fig. 7b` · `Fig. 8e1` · `Fig. 8i`: 방전 끝 1.73 V · 충전 2.60 V [그림 인쇄]) | LPSCl grand-potential: **환원 가장자리 1.717 V** (Li 교환 0 · 2026-09-22 라벨 정정) · **산화 개시 2.256 V** (GG set · LiS₄ 등 제외) / **2.14 V** (LiS₄ 포함 · grand-potential 경계의 Li-rich facet 규약) — `HZ-esw-reduction-limit-label` · `HZ-esw-reduction-limit-facet-convention` (CONDITIONAL: 규약 병기 · 창 폭 1.014 V 금지) | 리뷰는 고체 전해질 0 회. **우리 해석**: 황화물 SE 를 쓰는 전고체 Li–S 라면 양극 전위가 LPSCl 열역학 창의 양쪽 가장자리를 다 넘는다 → 전망 (4) 의 'P 도핑 도전재 · 촉매 중간층을 고체 쪽에' 는 SE 분해에 전자를 대는 길도 된다 (litdb 근거: `[Cronk26]` 계면상 카드 · `[Wu26LiSRev]` §J-52) |
| 산화수 | 'P 는 +3 · +5' (p.3) | 우리 환원 계단: P⁵⁺ → P⁰ → P³⁻ (Li₃P) (`se_redox_frontier.md` §3) | 리뷰가 다룬 인화물 (CoP · Co₂P · Ni₂P · WP · NbP · RuP₂) 의 P 는 음의 산화수 — '+3 · +5' 는 탄소 · 산화물 쪽에만 맞다 |
| 고체 전해질 응용 | 초록 · §1 이 '준고체 · 전고체 계면 매개' 를 약속 · 본문은 전망 (4) 한 문단 (그 문단 인용 0) | 우리 본업 | 이 리뷰는 고체 축의 근거가 아니다 |

---

## 8. Post-processing ★ (리뷰가 재수록한 원전들의 후처리 — 도구 이름 0 회)

- **무엇 (계산)**: 전하 밀도 차 등치면 (0.02 e Å⁻³ · `Fig. 5a`) · Bader 전하 (Se 자리 증가 — 본문만 · 그림 없음 · [87]) · DOS/PDOS + d-band center (`Fig. 7g`) · d–p band center 차 ([104]) · '프런티어 궤도' HOMO/LUMO (`Fig. 7a`) · 정전위 지도 (`Fig. 5i`) · 흡착 구조 + 결합 에너지 막대 (`Fig. 3a` · `Fig. 3d`) · ΔG 사다리 (`Fig. 8f`) · SISSO 서술자 ([89]).
- **무엇 (실험)**: XPS 성분 분해 (P 2p · N 1s · Co 2p · `Fig. 6b` · `Fig. 7e` · `Fig. 8d`) · in situ / operando Raman (`Fig. 8e` · `Fig. 8h`) · operando XRD 등고선 (`Fig. 5g`) · operando FT-EXAFS (`Fig. 8i`) · CV 등고선 지도 (`Fig. 7b`) · 정전위 Li₂S 핵생성 곡선 (`Fig. 8b`) · Li‖Li 대칭 셀 (`Fig. 3f`) · 로딩–C-rate 비교 그림 (`Fig. 6e`).
- **도구**: 0 회 (VESTA · pymatgen · VASPKIT · LOBSTER 등 이름 없음).
- **수치화 · 기록 방식**: 그림 안 글자 (흡착 에너지 · HOMO/LUMO · d-band center · 단계 ΔG) 와 본문의 % 변화. 오차 · 수렴 · 배치 수 표기 0.

---

## 9. 적용 인사이트 ★ (우리 작업에)

1. **'P–S 고정' 의 끝은 티오인산이다 — 작동 상태 ≠ 초기 상태.** `Fig. 8e1` 의 PS₄³⁻ 띠 (figure-read ≈ 415–418 cm⁻¹) 는 `[Cronk26]` 가 LPSCl/S 밀링에서 본 Li₃PS₄₊ₙ · LPS 띠 (418–420 cm⁻¹) 와 같은 자리다. 즉 '촉매 P' 가 폴리설파이드 속에서 우리 SE 와 같은 음이온으로 바뀔 수 있다. 우리 해석 틀 (`se_redox_frontier.md` §3 — P–S σ\* 가 환원 전자를 먼저 받고 끝은 Li₂S + P → Li₃P) 이 이 반응의 정방향 · 역방향을 둘 다 설명한다. ⇒ 전고체 Li–S 문헌을 읽을 때 'P 도핑 촉매' 와 '티오인산 SE 분해 산물' 을 같은 화학으로 묶어 읽는다 (읽기 틀 · 새 계산 제안 아님).
2. **P 는 O 를 문다.** XPS 에서 P–O 가 주성분 (`Fig. 6b1` · `Fig. 8d2`) · Li₃PO₄ · Co–O–P · P–O–Zr — 우리 B₂O₃ 모델의 O-on-P 와 같은 방향이다. 'P 도핑 탄소' 를 계산한 논문을 볼 때 '맨 P' 모델인지 'P–O 말단' 모델인지부터 본다.
3. **보고량 규율의 외부 실례 묶음** (발표 · 리뷰 회신에서 '왜 우리는 이렇게 하나' 의 예로): ① 기준 상태 없는 흡착 에너지 (Li −2.25 eV) ② 배위 미확인 2.4–4.8 eV ③ 절대값 없는 '% 장벽 감소' ④ 반응 ΔG 를 장벽으로 (홉 수 N ≈ 10⁻³¹–10⁻⁴³) ⑤ 스미어링 폭 안의 HOMO–LUMO 차 ⑥ 창 없는 d-band center ⑦ 색 막대를 에너지로 읽음. 우리 규율 (`D-2026-10-05-adsorption-site-coordination` · `D-2026-09-27-barrier-hop-count` · 띠틈 fixed-occ · 평균 지표 창 고정) 각각이 무엇을 막는지가 한 리뷰 안에서 다 보인다.
4. **Li–S 작동창이 LPSCl 창을 감싼다** (figure-read ≈ 1.7–2.8 V vs 우리 1.717 / 2.14–2.256 V · 규약 §7). 우리 셀 작동창 규칙 (2.5–4.25 V · 산화물 양극) 과는 다른 창이라 섞지 않는다. 전고체 Li–S 를 다시 볼 일이 생기면 '도전재 · 촉매 첨가물 = SE 분해 전자 공급원' 을 먼저 묻는다 (트랙 제안 아님 — li2s 계열은 2026-11-16 닫힘).

---

## 10. 비판 — 이 리뷰의 약한 곳 ★

### 10a. 과학 내용

1. **전기음성도 모순 (틀의 화학 근거).** P 를 'highly/strongly electronegative' 로 **10 회** 부른다 (초록 · p.2 · p.4 ×2 · p.5 · p.17 · p.19 · p.20 · p.22 · p.28). 같은 문장 (p.2) 에 적은 Pauling 값 **2.19** 는 C 2.55 · S 2.58 · N 3.04 · O 3.44 보다 낮다 [P 값만 리뷰 인쇄 · 나머지는 일반 지식]. 리뷰 스스로도 두 번은 *'lower electronegativity than C'* (p.3) · *'weakly electronegative atoms such as sulfur, phosphorus or boron'* (p.13) 라 쓰고, *'strong electron donation/donating'* 은 **6 회**다 (p.4 ×2 · p.11 ×2 · p.19 · p.22). 탄소 골격 안에서 '전기음성' 과 '강한 전자 주개' 는 반대말이다. P–C 결합에서 P 는 δ+ 쪽이고, 그래서 산소를 쉽게 무는 것 (§9-2) 과 맞는 쪽은 '주개' 다.
2. **'비어 있는 3d 궤도의 비공유쌍'** (p.7): *"The 3p orbitals and unoccupied 3d orbitals of P contain lone electron pairs"* — 비어 있는 궤도는 전자쌍을 담을 수 없다. 같은 쪽의 *'lone pairs of electrons on the 3p and 3d orbitals'* 도 같은 오류다.
3. **흡착 세기를 장점으로만 센다.** 자기 §3.1 · 전망 (3) 은 '흡착과 전환의 균형' 을 말하면서, §4–§5 는 흡착 크기 증가 (48–77 % · −2.25 eV · 2.4–4.8 eV) 를 계속 '향상' 으로 적는다. 너무 강한 흡착 (해리 · 자리 피독) 은 한 번도 다루지 않는다.
4. **같은 수 −2.25 eV 가 두 물질에.** Fe-NPC@rGO [79] (−1.86 → −2.25 eV) 와 P-CeO₂ [96] (§4.1 *'Li adsorption energy reaches −2.25 eV'*) — 두 문단의 문장도 거의 같다 (*'charge density and interfacial electron transfer capability'* · 'uniform lithium nucleation'). [96] 의 제목은 폴리설파이드 차단 분리막이다 → 옮겨 적기 오류 의심 (원전 미대조).
5. **BP/RP 전도성 서술이 서로 어긋난다.** §4.3 'BP · RP 는 그 자체로 우수한 전자 · 이온 전도체' · §5.3 머리 'BP 의 높은 고유 전도도' · [127] *'metallic-like (≈300 S m⁻¹)'* = 3 S cm⁻¹ ↔ §5.3 c-FBP–NC *'FBP 는 반도체라 전자 전도가 나쁘다'*. 3 S cm⁻¹ 은 같은 리뷰의 N/P-LPC-900 (10.23 S cm⁻¹) 보다 낮다. 적린은 보통 전자 절연체로 다룬다 [일반 지식 · 리뷰 밖].
6. **'d-band center 가 E_F 에 가까우면 전도도↑'** (P-RuSe₂ · §2.3 · §5.2) — d-band center 는 흡착 서술자 (Hammer–Nørskov) 이지 전도도 지표가 아니다. RuSe₂ 는 반도체다.
7. **약속과 내용의 간극.** 초록 끝 · §1 이 '준고체 · 전고체 계면 매개' 와 '나트륨 · 칼륨 · 고체 전지 · 전기촉매에도' 를 내세우지만, 고체 전해질 내용은 전망 (4) 한 문단이고 그 문단에 인용이 없다. 황화물 SE · 티오인산 · argyrodite 0 회.
8. **계산 조건 0.** §3 *'Computational and data-driven approaches'* 가 있어도 계산 조건이 없다 (§4). U · 스핀이 결정적인 Co · Fe · Mn · Ce 계, 분산 보정이 결정적인 탄소 위 흡착, 전위 · 용매화가 결정적인 ΔG 사다리 — 셋 다 무기재.
9. **% 로만 적은 장벽.** 'Li₂S 분해 장벽 10–18 % 감소' [64] · '30 % 초과 감소' [75] — 속도는 장벽 차의 지수에 비례하므로 절대값 없이는 뜻이 없다 (§3e).
10. **'이중 결함 효과가 단일 결함을 훨씬 넘는다'** (§5.4) — 같은 조건 대조 수치 없이 단정.
11. **화학 · 표기 작은 오류**: NaH₂PO₂ 를 *'inorganic phosphates'* 로 (차아인산염 · p.25) · 'Li₂S₄/Li₂S₄ → Li₂S₂/Li₂S' (p.4) · 'University of Oslo-66' (UiO = Universitetet i Oslo) · Ni 붕소화물 [113] 을 *'covalent metal boron nitride (MB)'* 로 (p.19) · NP-PA 를 'polyacetylene' 으로 (ref [116] 제목은 polyacenes) · 'carbonized black phosphorus (CP)' ↔ ref [128] 제목 'black phosphorus carbide' · *'0.079 % per 500 cycles'* · *'capacity retention rate was 626.42 mAh g⁻¹'* (단위) · *'lithiophilic sites … can be **reduced** by heteroatom doping to lower the nucleation overpotential'* (p.19 — introduced 의 오기로 보임) · p.2 마무리 문장 중복.

### 10b. 그림 · 캡션 · 본문 불일치 (재수록 그림 실독으로 확인 · 18 곳)

| # | 위치 | 본문 · 캡션 | 그림이 보여 주는 것 | 무게 |
|---|---|---|---|---|
| 1 | `Fig. 8f` | "율속 단계 장벽이 **Ni@N₄-CP** 에서 훨씬 낮다" | 율속 (마지막 *Li₂S₂ → *Li₂S) **V +2.81 < Ni +3.49 eV** [그림 인쇄] — 반대. 이 값은 반응 ΔG 이지 장벽도 아니다 (원전의 다른 결과를 가리켰을 가능성은 원전 미독이라 열어 둔다) | 🔴 방향 반대 |
| 2 | `Fig. 5i` | "결합 배치에 상호작용 세기를 나타내는 에너지 값 · NbP–LiNO₃ **0.5 eV** vs PC–LiNO₃ **0.1 eV**" | (i2) 에 에너지 값 없음 · 그림의 에너지 글자는 (i1) **정전위 색 막대 양 끝 0.5 eV / −0.1 eV** 뿐 (부호도 빠짐) · 캡션은 NbP–LiNO₃ 를 두 번 적고 PC–LiNO₃ 를 빠뜨림 | 🔴 정의 오독 |
| 3 | `Fig. 7a` | 캡션 *'catalyst–**Li₂S₆** complexes'* · 본문 'FeTe₂, **P-FeTe₂** 와 Li₂S₆ 조합' | 세 복합체 모두 **Li₂S** · 계는 FeTe₂ / **FeTe₂₋ₓ** / **P-FeTe₂₋ₓ** (공공 대조가 있고 P 단독은 없다) | 🔴 종 · 계 오기 |
| 4 | `Fig. 6e` | PNKB 가 '고로딩 · 고율 사분면' · '저 전해질 조건의 장점' | PNKB ★ figure-read ≈ 3.9 mg cm⁻² — 비교군 (3.8–12) 중 **가장 낮은 쪽** · 고율 (1C) 만 맞다 · E/S 축 없음 (본문 E/S 7) | 🔴 과장 |
| 5 | `Fig. 5c` | "900 °C Ar 1 차 열처리 → 700 °C 2 차 → 세척 → **KOH 활성 → 질산니켈 · 에탄올 함침** → 700 °C 3 차" | 500 °C 2 h (CO₂ · NaBH₄) → 600 °C 기체 전환 → 700 °C 2 h (Ar) → 세척 → **H₃PO₄ 함침** → 700 °C 40 min (Ar) → 세척 — 900 °C · KOH · 질산니켈 없음 (다른 공정을 서술한 것으로 보임) | 🔴 공정 불일치 |
| 6 | `Fig. 3d` | WP@NPC 문단: 'P 도핑이 친Li 자리를 넣어 Li–P 결합으로 LiPS 를 고정' · 리뷰 전체: 'P 의 강한 화학흡착' | **P@C 가 다섯 종 모두 N@C 보다 약하다** (figure-read ≈ −1.27 ~ −1.63 vs −1.8 ~ −1.97 eV) | 🟠 서사와 반대 |
| 7 | `Fig. 3a1` | 캡션 '여러 **도핑 탄소** 위 Li₂S₆ 흡착' | Li₂S₆ 는 도핑 탄소 위 **Mo 함유 슬랩 표면**에 붙음 — P 는 아래 탄소에 · 간접 효과. 이 그림에선 MPG (−2.39) > MNG (−2.08) 로 #6 과 P/N 서열이 반대인데 리뷰는 정리하지 않음 | 🟠 |
| 8 | `Fig. 8d` | 'P–C 와 P–O 결합 형성 확인' · '전하 이동 확인' | P 2p 성분은 **P–O · P–Co** (P–C 없음) · 이동 0.1–0.3 eV [그림 인쇄] — 대전 보정 · 피팅 불확실도와 같은 자릿수 | 🟠 |
| 9 | `Fig. 5f` | 'P–S 결합과 Li–O–Li 상호작용 형성' | 라벨은 **'Li–P'** 와 **'O···LiSₓ²⁻'** | 🟠 |
| 10 | `Fig. 8e1` | 'S₈ · Li₂S₆ · Li₂S₄ · Li₂S 봉우리' | 그 밖에 **PS₄³⁻** 선 (figure-read ≈ 415–418 cm⁻¹) 이 첫 방전부터 모든 스펙트럼에 — 본문 언급 0 | 🟠 누락 (우리에겐 가장 중요한 띠) |
| 11 | `Fig. 2k` | 'HRTEM 이 원자 수준 구조와 **P 도핑 성공**을 확인' | 흑연 (002) 0.336 · Co 0.177 / 0.204 nm 격자 무늬뿐 — HRTEM 은 P 를 보여 주지 않는다 | 🟠 과장 |
| 12 | `Fig. 3f` | CoPNC 'Li₂S 분해 장벽 감소' 문단 끝에 '5 mA cm⁻² · 5 mAh cm⁻² 사이클 성능' | 전압 ±0.1 V 의 **Li‖Li 대칭 셀** (Li 석출 · 덴드라이트 시험) — 셀 종류를 밝히지 않음 | 🟠 |
| 13 | `Fig. 4e` | '도입한 P · O 공공이 LiPS → Li₂S 단계 전환을 촉진함을 보여 준다' | 흡착 구조만 · 에너지 0 | 🟠 과장 |
| 14 | `Fig. 7g` | '계면의 전하 재분배 · 최적화된 전자구조' (원전 그림 그대로 전달) | Φ 금속 Co 4.1 < 'n 형' Co₂P 5.0 eV 면 전자가 Co → Co₂P 로 가서 축적 (오믹) 접촉 — 그림의 띠 굽힘도 그렇게 그렸는데 이름은 'Mott–Schottky' (n 형 쇼트키 장벽 조건은 Φm > Φs) · Co₂P 를 n 형 반도체로 둔 근거 없음 | 🟡 원전 그림의 내부 모순 전달 |
| 15 | `Fig. 5g` | 'α-S₈ · β-S₈ · **γ-S₈**' | α · β 만 표시 | 🟡 |
| 16 | `Fig. 5d` | 'TiO₂@HMCF/S 와 HMCF/S · 위 패널은 구조 변화 · 아래 패널은 확대' | 그림 라벨은 **TiO**@HMCFs/S (TiO₂ 아님 — 리뷰 본문 다른 곳도 'TiO@X-HMCFs') · 위 줄 = TiO@HMCFs/S · 아래 줄 = HMCFs/S · 확대는 오른쪽 | 🟡 |
| 17 | `Fig. 4b` | 본문 'BP 와 **Zr⁴⁺**' | 그림 라벨 'BP/**Zr²⁺**' (원전 그림) | 🟡 |
| 18 | `Fig. 2f` | '격자 변형 · 전하 국재화의 이론적 통찰' · 'Se 자리 Bader 전하 증가' | 구조 모형 + 숫자 없는 띠 만화 · Bader 값 없음 | 🟡 |

### 10c. 인용 감사 (제목 수준)

- 본문 인용 번호 1–128 이 모두 등장한다 (위첨자 자동 집계 · 범위 표기 포함).
- 역할 어긋남 후보 (원전 미독 · 제목만): [48] (S 도핑 SiOC = **Li 이온 전지 음극**) 을 Li–S 의 'sulfur doping' 사례로 · [80] (Cu@BP — 제목 *'Fast Kinetic Li–S'*) 을 §2.4 'Li 석출 경로 최적화' 근거로 · [105] 하나를 표 2 'TiN/PI' 와 본문 'PPC 숙주' 두 물질로 · [96] 에 [79] 의 Li 흡착 값.
- 고체 쪽 참고문헌은 [42] (Li/황화물 전고체 · *Adv. Mater.* 2020) 와 [70] (준고체 · 전고체 Li–S 계면 매개 · *Research* 2025) 둘 — 둘 다 §1 의 일반 서술 근거로만 쓰였고 전망 (4) 에는 인용되지 않았다. litdb 미보유.

---

## 11. 인용 가능 문장 (영문 초안)

> 이 리뷰는 2차 인용 모음이라 **값을 인용하지 않는다.** 아래는 '분야가 이렇게 정리한다' 는 서술 인용이거나 우리 판독 문장이다. 출처 표기는 권 · 쪽이 아직 없어 DOI 로 쓴다.

- *"Phosphorus-doping strategies for liquid-electrolyte Li–S cathodes and separators are commonly rationalized by a combined 'adsorption–catalysis–conduction' effect."* — *J. Mater. Chem. A*, DOI 10.1039/d6ta06590b (2026). 서술 인용 (리뷰의 틀 이름).
- *"Such compilations typically report adsorption energies and 'barriers' without the computational settings (functional, dispersion correction, Hubbard U, spin state, or electrode potential) needed to compare them."* — 우리 판독 (방법 서론 · 보고 규율의 동기).
- *"Phosphorus incorporated into carbon hosts is frequently detected as P–O species by XPS, and P-containing catalysts can form thiophosphate (PS₄³⁻) species in polysulfide-rich environments."* — ⚠ 근거가 이 리뷰의 **재수록 그림** (`Fig. 6b1` · `Fig. 8d2` · `Fig. 8e1`) 이라 원전 ([116] · [126] · [127]) 을 확인한 뒤에만.

---

## 12. 주의 / 한계 (인용 규율)

- ⛔ 리뷰의 흡착 · 결합 에너지 (−1.3 ~ −4.8 eV) · d-band center · HOMO/LUMO · ΔG 단계 · % 장벽 변화를 우리 값 옆에 두지 않는다 (계 · 정의 · 조건이 다르고 2차 인용이다).
- ⛔ `Fig. 8f` 의 +2.81 / +3.49 eV 를 '장벽' 으로 · 'Ni 가 낫다' 로 인용하지 않는다 (그림은 반대 · 정의는 반응 ΔG).
- ⛔ 'NbP–LiNO₃ 0.5 eV vs PC–LiNO₃ 0.1 eV' 를 상호작용 에너지로 인용하지 않는다 (색 막대).
- ⛔ 'P 는 전기음성도가 높다' 를 기전 문장으로 옮기지 않는다.
- ⛔ 리뷰의 Li₂S '분해 장벽' 을 우리 Li₂S 벌크 V_Li NEB (`HZ-sei-neb-li2s-cc-cellconv`) 와 같은 줄에 두지 않는다 — 이름만 비슷한 다른 양이다.
- ⛔ 우리 LPSCl 창 값 (1.717 · 2.14 · 2.256 V) 을 인용할 땐 규약을 같이 적는다 (`HZ-esw-reduction-limit-label` · `HZ-esw-reduction-limit-facet-convention` · CONDITIONAL) · 창 폭 1.014 V 는 쓰지 않는다. Li–S 작동창 (figure-read) 은 우리 셀 작동창 규칙 2.5–4.25 V (산화물 양극) 와 다른 창이다.
- ⚠ 표 두 장의 셀 수치는 '용량' 열 의미가 섞여 있다 (§3d) — 행별 원전 확인 없이 옮기지 않는다.
- ⚠ PDF 텍스트를 다시 뽑아 쓸 사람: E/S 'mL mg⁻¹' 는 μL mg⁻¹ 이다 (Symbol 글꼴 · 머리 주석 ④).

---

## 13. 기법 용어 미니사전 (한 단계씩)

- **LiPS · 셔틀**: S₈ 이 방전하며 Li₂S₈ → Li₂S₆ → Li₂S₄ (액체 전해질에 녹는다) → Li₂S₂ → Li₂S (고체) 로 간다. 녹은 중간체가 음극까지 헤엄쳐 가서 Li 와 반응하고 돌아오는 것이 셔틀이다 — 활물질을 잃고 쿨롱 효율이 떨어진다.
- **SRR · SOR**: 황 환원 반응 (방전) · Li₂S 산화 반응 (충전). Li–S 의 '촉매' 는 이 두 방향의 속도를 올린다는 뜻으로 쓴다 ('양방향 촉매').
- **S 로딩 · E/S · 면적 용량**: 전극 면적당 S 질량 (mg cm⁻²) · 전해질 부피 / S 질량 (μL mg⁻¹ · 작을수록 실용 · '희박 전해질') · 면적당 용량 (mAh cm⁻²). mAh g⁻¹ 은 S 1 g 기준이라 로딩이 낮으면 쉽게 커진다.
- **사이클당 감쇠율**: (첫 용량 − 마지막 용량) / 첫 용량 / 사이클 수. 첫 용량을 무엇으로 잡느냐 (저율 활성화 뒤? 첫 사이클?) 에 따라 달라진다.
- **흡착 (결합) 에너지**: E_ads = E(기판 + 분자) − E(기판) − E(분자). 음수면 붙는 쪽이다. ① 기준 상태 (고립 원자 · 분자 · 벌크) 를 바꾸면 값의 뜻이 바뀐다 ② 2 eV 를 넘으면 물리흡착이 아니라 화학결합 규모다 — 그 자리가 원래 덜 채워진 결합 (댕글링 본드 · 저배위 금속) 을 채우는 에너지일 수 있다 → 우리 규칙은 결합 자리 배위수부터 센다.
- **전하 밀도 차 (Δρ)**: ρ(전체) − ρ(기판) − ρ(분자). 등치면 (예 0.02 e Å⁻³) 에서 전자가 모인 곳 · 빠진 곳을 색으로 그린다. 등치면 값을 바꾸면 그림 크기가 달라진다 — 그림만으로 '전하 이동량' 을 말할 수 없다.
- **Bader 전하**: 전자 밀도의 '골짜기' 로 원자 부피를 나눠 원자마다 전자 수를 센다. 기준 (중성 원자 원자가 전자 수) 과 코어 처리에 따라 절대값이 흔들려서, 같은 계산 안의 상대 비교로만 쓴다.
- **d-band center (Hammer–Nørskov)**: 금속 원자 d 상태 밀도의 무게중심. E_F 에 가까울수록 반결합 상태가 덜 차서 흡착이 강해진다는 **흡착 서술자**다 — 전도도 지표가 아니다. 적분 창 (점유 상태만 · 전체 d 띠 · 상한) 에 따라 수백 meV 움직이므로 창을 적어야 한다 (우리 site mean-3p 도 같은 이유로 그림 창 −8..0 eV 에 고정한다).
- **d–p band center 차**: 촉매 금속 d 중심과 S 3p 중심의 차 — 작을수록 궤도가 잘 섞여 흡착 · 활성화가 세다는 서술자 (P-MoTe₂ [104]).
- **HOMO / LUMO (주기계)**: 분자에서는 최고 점유 · 최저 비점유 궤도다. 주기 슬랩에서는 띠 가장자리라서 k 점 · 스미어링에 기댄다. 스미어링 폭보다 작은 '차' (0.018 eV) 는 사실상 금속이라 순서를 말하기 어렵다.
- **정전위 지도 (ESP)**: 분자 등밀도면 위에 정전 퍼텐셜을 색으로 칠한 그림. 색 막대 양 끝 값은 **색의 범위**이지 결합 에너지가 아니다 (`Fig. 5i`).
- **ΔG 사다리 (계산 수소 전극식)**: 단계마다 G(생성물) − G(반응물) 을 계산해 계단으로 그린다. Li 를 Li 금속 (0 V) 기준으로 두고, 전위 U 에서는 전자 하나당 −eU 를 더한다. 가장 높은 오르막을 '율속 단계' 라 부르지만 **열역학 값**이지 장벽 (전이 상태) 이 아니다. 반응식 · 전자 수 · U · 용매화 · 기준이 없으면 다시 그릴 수 없다.
- **장벽 · 홉 수 검산**: 장벽 Ea 는 전이 상태까지의 에너지다 (보통 CI-NEB). 우리 규칙은 Γ = ν₀ exp(−Ea/kT) (ν₀ 10¹³ s⁻¹ 가정) 로 '얼마나 자주' 를 차수로 보고, '빠르다' 같은 서술과 모순인지 본다. '% 감소' 는 절대값이 없으면 이 검산을 못 한다.
- **SISSO**: 기본 물성 (전기음성도 · 반경 · d 전자 수 …) 을 수학 연산으로 조합해 목표값 (예: Li₂S 분해 장벽) 을 가장 잘 맞추는 식 하나를 고르는 서술자 탐색법.
- **일함수 · Mott–Schottky 접합**: 일함수 Φ = 진공 준위 − E_F. 두 물질이 닿으면 Φ 가 작은 쪽에서 큰 쪽으로 전자가 간다. n 형 반도체에 Φ 가 **더 큰** 금속이 닿으면 반도체 쪽 전자가 빠져 장벽 (쇼트키) 이 생기고, Φ 가 **더 작은** 금속이면 전자가 쌓여 오믹 접촉이 된다 (`Fig. 7g` 점검 근거).
- **XPS 결합에너지 이동**: 원자 주변 전자가 빠지면 내각 전자의 결합에너지가 오른다. 0.1–0.3 eV 이동은 대전 보정 · 피팅 불확실도와 같은 자릿수라 단독 근거로는 약하다.
- **in situ / operando Raman · XRD · EXAFS**: 셀을 돌리면서 S₈ (≈ 152 · 218 · 473 cm⁻¹) · Li₂S (≈ 375 cm⁻¹) · 폴리설파이드 · 티오인산 (PS₄³⁻ ≈ 418–426 cm⁻¹) 의 생성 · 소멸을 본다 [띠 자리는 일반 지식 + `[Cronk26]` 카드]. EXAFS 는 특정 원자 (Fe) 주변 결합 거리 분포를 준다.
- **Li₂S 정전위 핵생성 시험**: Li₂S₈ 용액에서 일정 전위로 Li₂S 를 석출시키며 전류 정점 시간 · 적분 용량을 본다 (`Fig. 8b`: 2380 s).
- **단원자 촉매 · M–N₄ / M–N₂P₂**: 탄소 안 금속 원자 하나를 N 넷이 잡은 자리. N 일부를 P 로 바꾸면 대칭이 깨지고 금속의 전자 상태가 바뀐다 (Co–P₂N₂ [65] · Co–N₂P₂ [122]).
- **Lewis 산–염기**: 전자쌍을 받는 쪽 (Li⁺ = 산) 과 주는 쪽 (N · O · P 의 비공유쌍 = 염기). LiPS 의 Li⁺ 는 염기 자리에, Sₓ²⁻ 는 산 자리 (금속) 에 붙는다.
- **전기음성도 · 전자 주개**: 결합에서 전자를 끌어당기는 정도 (Pauling 척도). P (2.19) 는 C 보다 낮아서 탄소 안에서는 전자를 **내주는** 쪽이다 — '전기음성 P' 와 '전자 주개 P' 는 같은 자리에서 함께 참일 수 없다.

---

## 14. 후속 추적 참고문헌 (필요할 때만 · 전부 litdb 미보유)

| 우선 | 원전 | 왜 |
|---|---|---|
| 1 | [127] Zhao *Small Methods* 8, 2300610 (2023) — NiCoP/BP | `Fig. 8e1` PS₄³⁻ 띠의 원래 해석 (P 촉매 → 티오인산?) — 우리 화학 연결의 1차 근거 |
| 2 | [128] Xia *J. Colloid Interface Sci.* 630, 317 (2023) — V/Ni@N₄-CP | `Fig. 8f` 사다리 방향 (§10b-1) · 반응식 · 전위 |
| 3 | [64] Chen *Molecules* 29, 2746 (2024) — P-g-C₃N₄ 제1원리 (OA) | 리뷰 전체에서 유일하게 범함수가 적힌 계산 · Li₂S 분해 장벽 절대값 |
| 4 | [114] Wang *Angew. Chem. Int. Ed.* 64, e202502255 (2025) — NbP | `Fig. 5i` '0.5 vs 0.1 eV' 의 원래 뜻 |
| 5 | [79] Pato *Small* 21, 2503596 (2025) · [96] Liu *Chin. Chem. Lett.* 36, 110369 (2025) | −2.25 eV 귀속 · Li 흡착 기준 상태 |
| 6 | [109] Park *Chem. – Asian J.* 20, e00840 (2025) — PCDC | `Fig. 5c` 공정 (§10b-5) |
| 7 | [70] Wang (Brezesinski 공저) *Research* 8, 0949 (2025) — 준고체 · 전고체 Li–S 계면 매개 | 리뷰가 고체 쪽으로 든 유일한 최근 문헌 |
