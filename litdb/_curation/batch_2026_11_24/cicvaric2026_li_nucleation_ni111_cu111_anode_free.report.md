# 끝 보고 — cicvaric2026_li_nucleation_ni111_cu111_anode_free (2026-11-24 · litdb-curator)

쓴 파일: `litdb/papers/cicvaric2026_li_nucleation_ni111_cu111_anode_free.md` (448 줄 · 표 칸수 검사 0 건) · `litdb/figures/cicvaric2026_li_nucleation_ni111_cu111_anode_free/` (크롭 14 장 + figures.json — 메인 체크포인트 b60590e6 에 들어감) · 이 보고 파일.
digest 는 체크포인트 4739c5a7 뒤에 고친 몇 줄 (SI Γ 출처 문구 · k_app 오차 막대 문구 · §12 같은 배치 연결) 이 작업 폴더에만 있다 (커밋 안 함).
공유 파일 · git 은 안 건드렸다 (`litdb/figures/_sources.json` 은 추출 도구가 다시 썼다). `build_index.py --check`: 이 slug 는 "어느 인덱스에도 없음 [dft]" · "comparison_vs_ours.md 미편입" 두 곳에만 뜬다 — 아래 (a) (b) 를 넣으면 풀린다.
웹앱 확인 (읽기만): 원소 태그 Li · Cu · Ni · 기법 태그 dft · functional · pseudo · pdos · neb · 그림 주석 14 키 (f1–f10 · fS1 · fS2 · t1 · t2) 파싱됨 · PI 배지 없음.

## (a) INDEX.md 행

넣을 절: **`## ⚠ EXTERNAL (argyrodite 아님 · [우리 그룹] 아님 · 물성 4축에 *수치로* 비교 제외)`** 표 — `papers/shi2017_hbn_interfacial_layer_li_anode.md` 행 바로 아래 (같은 'Li 금속 음극 · Li 흡착 에너지 방법' 묶음: liu2022 · shi2017).
대안: 이번 배치를 `## 🧲 계면 점착 · 인터레이어 트랙` 에 모은다면 그 표 끝 — 절 머리 조건 'LPSCl 이 한쪽 면' 에 안 맞으므로 행 안 ⛔ 문구를 유지한다. 두 표 모두 3 칸이라 아래 행이 그대로 들어간다.

```
| `papers/cicvaric2026_li_nucleation_ni111_cu111_anode_free.md` 🔋**W_ad §7 ① 흡착 에너지 지표의 금속 (111) 기준점** **(본문 12 pp + SI 4 pp · 크롭 14장 = 그림 12 + 표 2 · 그림 12장 전부 실독 · 표 2장은 PDF 텍스트 · 2026-11-24)** | **[외부 · 비-argyrodite · 액체 전해질 무음극 LMB 집전체 · exp (CV · 정전위 EIS · AFM) + DFT (VASP PBE+D3(BJ))]** ✅ **Katarina Cicvarić**/L. Mannich/S. Suttor (BMW AG)/W. Hu/V. Alexandrov (Nebraska–Lincoln)/**Aliaksandr S. Bandarenka\*** (TUM), "**Electrochemical and computational insights into lithium nucleation at Ni(111) and Cu(111) surfaces for anode-free Li-metal batteries**" — ***J. Mater. Chem. A* 14, 16784–16795 (2026)**, DOI `10.1039/d6ta00180g` (OA CC BY 4.0). Cu(111) · Ni(111) 단결정 · 1 M LiPF₆ EC:EMC · −5…−25 mV 정전위 3600 s time-scan EIS → k_app = √(2D)·A_W/R_CT: **Ni 가 2–4× 낮다** (figure-read 2.2–3.9×) · AFM 입자 더 크고 매끈 (추세선 · 오차 막대 전부 겹침). **친Li 판정 = 고립 Li 원자 기준 흡착 에너지 하나 — 점착 · 젖음각 · 금속 Li 기준 · 합금 0**: hollow Cu −2.63 / Ni −2.89 eV (`Table 1`) · 1층 θ 0.04→1 Cu −2.63→−2.05 / Ni −2.89→−2.19 (`Fig. 8` — 덮임 효과 0.58/0.70 eV > Cu–Ni 차 0.12–0.28) · **둘째 층에선 순서 반전** θ 1 Cu −1.69 / Ni −1.57 (`Fig. 9`) · NEB 맨면 13/11 · 1ML 위 20/12 meV (전부 < kT · 홉 대기 ≈ 0.2 ps). ⚠ SI 표면 원자 밀도가 (111) 기하보다 ≈ 21 % 작아 UPD θ ⅓ / 1 → ≈ 0.27 / ≈ 0.77 (우리 산수) · Ni 'UPD' 2.3/2.0 V 는 논문 DFT 규모 밖 · C_SEI "두 자릿수" ↔ figure-read 10–40× · 1ML 의사형 Li 15.6/18.1 % 압축 · 표면 전처리 · 반복 실험 미기재 | **W_ad 보고서 §7 ① (흡착 에너지) 의 금속 (111) 기준점 · 대조 잡 표적 (Cu(111) fcc −2.63 eV · PBE+D3(BJ)) · §7 ② ③ 는 이 논문에 없음 · 물성 4축 수치 편입 금지** |
```

## (b) comparison_vs_ours.md

넣는다 — 단 물성 4축 표 (A–D) 에는 넣지 않는다 (계가 액체 전해질 · Cu/Ni 단결정). 두 곳:

① `## 📑 Reference key` 표 (4 칸: 약칭 | 논문 | digest/status | 유형) — `[Liu-hBN]` 행 근처:
```
| **[Cicv26NiCu]** 🔧 **금속 (111) 위 Li '친Li' 를 고립 원자 기준 흡착 에너지 하나로 판정한 사례 (점착 · 젖음 · 금속 Li 기준 0)** · ⛔ **액체 전해질 · Cu/Ni 단결정 — A–D 물성 4축 진입 금지** (§J 새 블록에만) | Katarina Cicvarić/L. Mannich/S. Suttor/W. Hu/V. Alexandrov/**Aliaksandr S. Bandarenka\*** (TUM · BMW AG · Univ. Nebraska–Lincoln) 2026 *J. Mater. Chem. A* 14, 16784 (DOI 10.1039/d6ta00180g) — "Electrochemical and computational insights into lithium nucleation at Ni(111) and Cu(111) surfaces for anode-free Li-metal batteries" | `papers/cicvaric2026_li_nucleation_ni111_cu111_anode_free.md` ✅ (2026-11-24 · 그림 12/12 실독) | exp (CV · EIS · AFM) + DFT (VASP PBE+D3(BJ) · CI-NEB) · 외부 |
```

② J 절 새 블록 (지금 마지막이 J-87 → 다음 번호):
```
### J-88. 🔧 **방법 원전 — [Cicv26NiCu] Cu(111) · Ni(111) 위 Li 초기 석출 (*J. Mater. Chem. A* 14, 16784 (2026)): '친Li' = 고립 원자 기준 흡착 에너지 하나 · 덮임 효과가 재료 차보다 크고 둘째 층에서 순서가 뒤집힌다 · 장벽은 kT 아래 · UPD 덮임 산수 오류** (2026-11-24 신설)

> 📎 출처: `papers/cicvaric2026_li_nucleation_ni111_cu111_anode_free.md` (그림 12/12 실독 · 표 2 는 PDF 텍스트). ⛔ 액체 전해질 무음극 LMB · Cu/Ni 단결정 — A–D 물성 4축에 행을 만들지 않는다. 우리 쪽 상대 = W_ad 보고서 (`docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html`) §7 '① 흡착 에너지'.

| 서술 | 논문 값 | 우리 규율로 다시 읽으면 | 판정 |
|---|---|---|---|
| 'Ni(111) 이 더 친Li' (`Table 1` · `Fig. 8`) | hollow Cu −2.63 · Ni −2.89 eV · 1층 모든 θ 에서 Ni 가 0.12–0.28 eV 더 음수 | 기준 = 고립 Li 원자 · 금속 Li 기준 (E_coh) 없음 → 젖음 · 핵생성으로 못 옮긴다 · 배위 1–3 (정상 테라스 · 결함 자리 아님) | 🔵 §7 ① 의 금속 (111) 기준점 (PBE+D3(BJ) 같은 계열) · 대조 잡 표적 |
| 덮임 의존 (`Fig. 8`) | θ 0.04 → 1 에서 +0.58 (Cu) · +0.70 eV (Ni) | 재료 차 (0.12–0.28) 보다 크다 → ① 은 자리 · 덮임 · 층을 선언한 X(상태) 로만 | 🔵 §7 ① 한정 문구의 정량 근거 |
| 둘째 층 (`Fig. 9`) | θ 1 Cu −1.69 · Ni −1.57 eV · 모든 θ 에서 Cu ≥ Ni | 순서 반전 · 1ML 의사형 Li 가 15.6/18.1 % 압축 (Li(110) 면의 1.53/1.62× 조밀, 우리 산수) — 변형 차이가 주 원인일 수 있다 | 🔴 단일 지표 순위는 층에 따라 뒤집힌다 |
| 장벽 (`Fig. 10`) | 맨면 13/11 · 1ML 위 20/12 meV | 홉 수 검산 (ν₀ 10¹³ s⁻¹ 가정 · 298 K): 평균 대기 0.15–0.22 ps · 차 8 meV = 홉률 1.37× ↔ k_app 차 2.2–3.9× | 🔴 장벽 → k_app 인과는 차수 모순 (저자도 '주 원인 아닐 수 있다') |
| UPD 덮임 (SI p.S2) | Cu ≈ ⅓ · Ni ≈ 1 ML | Γ 1.39/1.48×10¹⁵ cm⁻² 는 (111) 기하 4/(√3a²) = 1.75/1.86 보다 ≈ 21 % 작다 → ≈ 0.27 / ≈ 0.77 · Ni 300 µC = Li 조밀면 1.15–1.25 층 | 🔴 'Ni 완전 단층' 불성립 · Ni/Cu 비 (≈ 3×) 는 남음 |
| C_SEI (`Fig. 6`) | "two orders of magnitude" | figure-read 10–40× · Ni ≈ 77 µF/cm² ↔ 평판 막 ≈ 0.1 nm (ε_r 10 가정) | 🔴 '얇은 SEI → 부식 저항' 은 이 그림으로 안 선다 |

⛔ 인용 금지 — 고립 원자 기준 eV 를 우리 W (J/m²) 와 같은 줄에 두기 · "Ni 가 Li 를 더 잘 적신다" (젖음 미계산) · "Ni 에서 UPD 완전 단층" · "SEI 가 두 자릿수 얇다". 2층 Cu–Ni 차 (≤ 0.12 eV) · NEB 차 (≤ 8 meV) 는 방법 잡음 크기다 (`Table 2` ↔ `Fig. 9` Ni 0.02 eV 역전). 후속: ref 25 (같은 그룹 Cu(111) 편 · *J. Phys. Chem. C* 130, 1096 (2026)) · ref 22 Pande & Viswanathan (*ACS Energy Lett.* 4, 2952 (2019)) — litdb 미보유.
```

③ (선택) `comparison_vs_ours_DEM.md` §I 에 한 줄 — `### I-xx. cicvaric2026_li_nucleation_ni111_cu111_anode_free — (인접 축 · 점착 · 젖음 0) 금속 (111) 위 Li 흡착 에너지 · 덮임 · 둘째 층 — W_ad 보고서 §7 ① 의 기준점 (액체 전해질 · DEM 입력 아님)`. 본문은 digest §7b 표를 옮기면 된다.

## (c) pdf_map.tsv

**불필요** — 자동 매칭이 된다 (`extract_figures.py --inbox --only cicvaric2026` → `[제목 69%]` 본문 `nicu2026_li_nucleation_ni111_cu111_main.pdf` · SI `nicu2026_li_nucleation_ni111_cu111_SI.pdf`).

## (d) 추가로 먹일 만한 논문 (8 편 · 최근 것 먼저)

서지는 전부 이 논문 참고문헌 목록 (PDF 글자층으로 대조) 그대로다. litdb 유무는 2026-11-24 DOI · 제목 grep — 8 편 모두 **없음**.
⚠ Li 금속 | 기판 **점착 · 젖음** 쪽은 이 논문 참고문헌에 한 편도 없다 — 그 몫은 이번 배치의 seymour2021 · yang2021_flat · sharafi2017 · lu2026_li_ag · fuchs2023 이 이미 맡고 있다.

| # | 서지 | 왜 (우리 축) | litdb |
|---|---|---|---|
| 1 | K. Cicvarić, L. Mannich, D. Blum, W. Hu, S. Suttor, V. Alexandrov, A. S. Bandarenka, "Electrochemical and Computational Insights into Lithium Nucleation on Single Crystal Copper for Anode-free Li-metal Batteries", *J. Phys. Chem. C* 130(2), 1096–1104 (2026), DOI 10.1021/acs.jpcc.5c07557 (ref 25) | 이 논문이 넘긴 방법의 원전 — k_app 유도 · Cu(111) 덮임별 흡착 계산 | 없음 |
| 2 | M. H. Kim, D. Y. Kim, Y. Li, J. Kim, M. H. Kim, J. Seo, H. W. Lee, "Horizontal lithium growth driven by surface dynamics on single crystal Cu(111) foil", *Energy Environ. Sci.* 17(18), 6521–6532 (2024), DOI 10.1039/d4ee01766h (ref 16) | 실제 단결정 Cu 박 위 수평 성장 · 표면 확산 — 이 논문 NEB 와 "very good agreement" 라는 상대 | 없음 |
| 3 | D. Petersen *et al.*, "Anode-free post-Li metal batteries", *Mater. Horiz.* 11(23), 5914–5945 (2024), DOI 10.1039/D4MH00529E (ref 37) | 이 논문이 '친금속성 → 균일 핵생성' 의 근거로 인용한 리뷰 | 없음 |
| 4 | Y. Zhang, S. Jing, H. Shen, S. Li, Y. Huang, Y. Shen, F. Liu, "Developments, Novel Concepts, and Challenges of Current Collectors: From Conventional Lithium Batteries to All-Solid-State Batteries", *ChemElectroChem* 11(4), e202300739 (2024), DOI 10.1002/celc.202300739 (ref 8) | 전고체 쪽 집전체 요건 — 우리 셀 문맥 | 없음 |
| 5 | S. Huo, L. Wang, B. Su, W. Xue, Y. Wang, H. Zhang, X. He, "Anode-Free Li Metal Batteries: Feasibility Analysis and Practical Strategy", *Adv. Mater.* 36(47), 2411757 (2024), DOI 10.1002/adma.202411757 (ref 6) | 무음극 실현성 전반 · 집전체 선택 | 없음 |
| 6 | V. Pande, V. Viswanathan, "Computational Screening of Current Collectors for Enabling Anode-Free Lithium Metal Batteries", *ACS Energy Lett.* 4(12), 2952–2959 (2019), DOI 10.1021/acsenergylett.9b02306 (refs 22 = 50) | 금속 · 합금 집전체 DFT 스크리닝 (흡착 · 핵생성 에너지 · BEP 장벽) — §7 ① 과 '핵생성 에너지' 를 가르는 원전 · 이 논문 NEB 가 반박한 상대 (오래됐지만 핵심) | 없음 |
| 7 | G. Li, D. Shi, Z. Hao, Y. Lu, Q. Zhao, Z. Yan, J. Chen, "Computational Insights into the Crystal Facet Selectivity of Cu Current Collector for the Growth of Lithium Metal", *J. Phys. Chem. C* 127(33), 16297–16303 (2023), DOI 10.1021/acs.jpcc.3c03096 (ref 17) | 면 의존 Li 흡착 · 성장 DFT — 보고서 7-1 표면 모형 선택 | 없음 |
| 8 | K. Yan, Z. Lu, H.-W. Lee, F. Xiong, P.-C. Hsu, Y. Li, J. Zhao, S. Chu, Y. Cui, "Selective deposition and stable encapsulation of lithium through heterogeneous seeded growth", *Nat. Energy* 1, 16010 (2016), DOI 10.1038/nenergy.2016.10 (ref 36) | 기판별 Li 핵생성 과전압 + 합금 씨앗 — §7 ③ · Ag 층 쪽 실험 원전 (내용은 기억 기반 — 원문 확인 필요) | 없음 |

자리 남으면: M. Jäckle *et al.*, *Energy Environ. Sci.* 11(12), 3400 (2018), DOI 10.1039/C8EE01448E (ref 38 · 자기확산 장벽 서술자) · I. T. Røe, S. K. Schnell, *J. Mater. Chem. A* 9(17), 11042 (2021), DOI 10.1039/d1ta02300d (ref 18 · Cu 위 느린 표면 확산).

## (e) DEM-DFT 보고서 (W_ad §7 Li 친화성 정량화) 에 쓸 거리

쪽 = 저널 쪽 (PDF 1 쪽 = 16784). '봤다' = 크롭 그림을 Read 로 직접 봄 · 표는 PDF 글자층 + 쪽 렌더.

1. **§7 ① 흡착 에너지 — 금속 (111) 기준점.** `Table 1` (p.16790 · 표는 글자층 · 쪽 렌더로도 봄) · `Fig. 8` (p.16790 · 봤다): hollow Cu −2.63 · Ni −2.89 eV — VASP PAW 500 eV · PBE + D3(BJ) · (111) 5 층 (위 3 층 이완) · 진공 15 Å · p(5×5) Γ 5×5×1 · **고립 Li 원자 기준** · 배위 3 (정상 테라스). 같은 점: PBE + D3(BJ) · (111) 슬랩 · Γ 중심 k (셀 × k ≈ 25–27 로 밀도 일관). 다른 점: 코드 · PP (VASP PAW ↔ 우리 QE 경로) · 3 체 항 미기재 · 보고량 (eV/Li ↔ 우리 W J/m²). → 보고서 ① 의 h-BN −0.33 eV 예 옆에 금속 쪽 예로 둘 수 있다 — 기준 (고립 원자) 을 같이 적는다.
2. **§7 ① 한정 문구에 숫자 달기.** `Fig. 8` · `Fig. 9` (p.16790 · 봤다 · 막대 인쇄값): 덮임 0.04 → 1 에서 0.58 / 0.70 eV 변화 > Cu–Ni 차 0.12–0.28 eV · 둘째 층에서는 모든 θ 에서 Cu ≥ Ni (순서 반전). 보고서의 "자리와 덮임 정도에 따라 값이 바뀐다" 를 "재료 차보다 크고, 층에 따라 순서가 뒤집힌다" 로 구체화할 수 있다.
3. **§7 ② 점착 → 젖음각 — 이 논문엔 없다.** §4.4 (p.16792–16793 · 글자층 + 쪽 렌더 · pdftotext 검색 'adhesion · wetting · contact angle' 0 건): Li 금속 슬랩 · γ_Li · W 가 없다. 1ML 은 의사형 1×1 (p.16790–16791) — Cu · Ni 격자에 맞춘 Li 가 15.6 / 18.1 % 압축 · Li(110) 면의 1.53 / 1.62× 조밀 (우리 산수 · bcc Li a 3.51 Å 교과서값). → 보고서 7-1 의 "Li 면 · 셀 · 변형 · registry 를 미리 적는다" 가 왜 필요한지 보여주는 반례. 다른 점: 양 자체가 다르다.
4. **금속 Li 기준 열을 같이 낸다.** 이 논문의 빈칸 (E_coh 없음). 우리가 ① 을 낼 때 bcc Li 벌크 기준 열을 같이 실으면 UPD 전위 어림 (U ≈ −ΔE/e) · §7 ② 의 γ_Li 와 같은 기준이 된다. 우리 산수 (교과서 E_coh 1.63 eV · 논문 밖): hollow Cu ≈ −1.00 · Ni ≈ −1.26 eV (vs Li 금속) · 둘째 층 θ 1 ≈ −0.06 / +0.06 eV.
5. **§7 ③ 합금 — 없다.** Cu · Ni 는 0–3 V 에서 "electrochemically inactive" (p.16784 서론) → 비합금 기준선으로만 쓴다. Ag 와의 대비는 (d) 8 번 (Yan 2016) 쪽.
6. **대조 잡 하나.** 우리 Ag(111) 위 Li 흡착을 계산할 때 같은 설정으로 Cu(111) fcc hollow 단일 원자 한 점을 같이 돌려 −2.63 eV (`Table 1`) 와 견준다 — 허용 차이는 결과 보기 전에 정한다 (PP · 3 체 항 · 고립 원자 처리 차이를 감안).
7. **확산 장벽은 네 번째 지표로 넣지 않는다.** `Fig. 10` (p.16791 · 봤다): 11–20 meV < kT · 홉 대기 0.15–0.22 ps (`tools/sei/collect_neb.py::hop_check` · ν₀ 10¹³ s⁻¹ 가정 · 298 K). 같은 점: CI-NEB. 다른 점: 우리 보고서엔 장벽 지표가 없다 — 그대로 두기를 권한다.
8. **실험 손잡이 = UPD 덮임.** `Fig. 1` (p.16786 · 봤다) · SI p.S2 (봤다): 실험 쪽 '친Li' 관측량이다. 단 SI Γ 값이 (111) 기하보다 ≈ 21 % 작다 (θ ⅓ / 1 → ≈ 0.27 / ≈ 0.77 · 우리 산수) · Ni 2.3 / 2.0 V 'UPD' 는 논문 DFT 규모 (≲ 1.3 V) 밖 · 표면 전처리 미기재 → 보고서의 '실험과 함께 판단' 에 붙일 때 이 주의를 같이 단다.
9. **PDOS — 일함수 · 전하가 더 나은 서술자.** `Fig. 7` (p.16790 · 봤다): Li s · p 상태가 E_F 아래에 거의 없다 → 이온성 흡착. 우리가 ① 을 내면 d-band 보다 일함수 · Bader 전하를 같이 싣는 편이 낫다.
10. **핵생성 과전압 — 이 논문도 안 쟀다.** §4.2 (p.16792 · pdftotext 검색 'galvanostatic · nucleation overpotential · chronoamperometry' 0 건): "overpotential" 은 정전위 −5…−25 mV 다. → 보고서 '할 수 없는 것: 핵이 생길 때의 과전압' 의 실험 대조로 이 논문을 쓰면 안 된다.

## (f) 그림 크롭 요약

- 크롭 **14 장** = 본문 그림 10 (`Fig. 1`–`Fig. 10`) + SI 그림 2 (`Fig. S1` · `Fig. S2`) + 표 2 (`Table 1` · `Table 2`) · `missing_labels` [] (번호 공백 · 놓친 캡션 0) · 오탐 0 · 손 크롭 0 — 도구 결과 그대로.
- 실독: **그림 12 / 12** (AFM `Fig. 3` · `Fig. 4` 포함) · 표 2 장은 PDF 글자층 (쪽 렌더로도 봄).
- 본문과 어긋난 그림 3: `Fig. 6` ("two orders of magnitude" ↔ figure-read 10–40×) · `Fig. 5` (Cu–Ni 차이 주장 ↔ 오차 막대 전부 겹침) · `Fig. 2c` (y 축 "single site" ↔ 다른 패널 "average site").
- 임시 파일 충돌 점검: 처음에 scratchpad 루트에 공용 이름 `main.txt` · `SI.txt` 를 썼다 (11:39:07). slug 폴더로 다시 뽑아 `cmp` 동일 · 첫 줄 제목 · 저자 · 쪽 번호 (16784–16795) 일치 · pdftotext 로 부정 검색 (표면 전처리 · 반복 실험 · 쌍극자 · 스미어링 · 핵생성 과전압 · 젖음 · 점착) 다시 해도 0 건 → **digest 글자는 이 논문 것이다**. 그 두 파일은 내 글자임을 `cmp` 로 확인한 뒤 지웠다. ⚠ 11:39:07 전에 같은 이름을 쓴 다른 에이전트가 있었다면 내가 덮었을 수 있다 (덮였다면 그 파일 첫 줄이 *"Electrochemical and computational insights into lithium nucleation at Ni(111)…"*). 소문자 `si.txt` (11:31:03) 는 내 것이 아니라 그대로 뒀다.

## (g) Jeff Sakamoto 저자 여부

**아니다.** 저자 6 명 = Katarina Cicvarić · Lars Mannich · Susana Suttor · Wang Hu · Vitaly Alexandrov · Aliaksandr S. Bandarenka (교신). INDEX 행에 🏷 를 안 붙였고, digest 저자 줄 아래에 "(Jeff Sakamoto 는 저자가 아니다.)" 한 줄을 뒀다.
