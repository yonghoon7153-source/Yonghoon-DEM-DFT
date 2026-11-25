# 다음에 먹일 논문 — 2026-11-24 배치 18 편 (d) 절 통합 + 최근 2 년 발견 검색

- 대상: W_ad (Li | Li₆PS₅Cl · Li | Ag · Li | C) DFT + DEM 보고서 — 친Li 성 (Young–Dupré · W ≥ 2γ_Li) · 박리 공극 · 적층압 · Li 크리프 · Cu 위 핵생성 · Ag–C 층 기전 · 탄소 종류.
- 읽은 것: 보고서 18 편의 (d) 절. 본 목록 144 건 + 차순위 · 번외 22 건 = **제안 166 건**.
  같은 논문을 합치니 **99 편** (이번 배치 논문 1 건은 뺐어요: seymour2021 보고서 #5 = 배치 `wang2020_…`). 그중 **34 편은 보고서 2 편 이상**이 제안했어요.
- litdb 대조: `litdb/papers/` 파일 이름 + 각 digest 머리 15 줄 (제목 · slug · DOI · PDF 이름) grep. 남의 digest 안에서 인용만 된 건 '없음' 으로 셌어요.
  → **제안 99 편 중 자체 digest 가 있는 건 0 편**이에요. 발견 검색으로 찾은 최근 편 14 편도 0 편 (litdb 안에서 인용조차 없음).
- 발견 검색: 주제어 + 연도로 8 번 (제목 없이) → 확인 검색 18 번. 남긴 것 14 편 (표 1 에 7 · '그 밖' 에 7).
  ⚠ **v2 (2026-11-24)**: 서지를 **Crossref REST API (api.crossref.org)** 로 다시 맞췄어요 — 출판사 페이지 (pubs.rsc.org 등) · 본문은 여전히 안 열었고, arXiv API 는 429 (Rate exceeded) 로 못 읽었어요.
  앞 판은 검색 결과 (출판사 랜딩 제목 · 메타) 로만 맞췄어요. 건별 전 → 후 · 쓴 DOI 는 같은 폴더 `verify_log.md` 에 있어요.
- 서지 확인 표기: **확인** = 보고서가 PDF 참고문헌 목록 (또는 다른 litdb 카드의 전사 참고문헌) 에서 맞춤 · **기억** = 보고서 기억 (쓰기 전 DOI 확인) ·
  **검색 확인** = 검색 결과의 출판사 메타로 제목 · 저널 · 권 · 쪽 (· DOI) 맞춤 · **부분** = 일부만 확인 (빈 칸을 적었어요) ·
  **Crossref 확인** = Crossref 메타 (api.crossref.org/works) 로 맞춤 — 제목 낱말 · 첫 저자 성 · 저널 · 연도가 다 맞을 때만 받았어요 (권 · 쪽 · 논문 번호 · DOI 도 거기서).
- 우리 점착 W 값은 싣지 않았어요.

## 표 1 · 최근 2 년 (2025–2026) — 발견 검색 + 보고서 제안

> ✅ = 2026-11-24b 묶음에서 digest 됨 (12 편 · 목록 `litdb/_curation/batch_2026_11_24b/batch.json` · 그 묶음이 새로 찾은 후보는 `litdb/_curation/batch_2026_11_24b/extra_papers_2026_11_24b.md`).

| 순위 | 논문 (저자 · 저널 권, 첫쪽 (연도)) | 왜 우리에게 (한 줄) | 출처 (어느 보고서 n 편 / 검색) | 서지 확인 |
|---|---|---|---|---|
| 1 ✅ | Baer, Shantsila, Figiel, Karasulu · *J. Mater. Chem. A* 14, 20245 (2026) — "Atomistic insights into the chemical stability and ionic transport at Li-metal/Li-argyrodite interfaces" · DOI 10.1039/D6TA00922K | 우리랑 같은 Li \| Li₆PS₅Cl 계면이에요. 저지수 종단 28 개를 훑어 낮은 셋으로 계면을 짓고 ab initio + 자체 MLIP 로 안정성 · 수송을 봐요 → 우리 슬랩 종단 선택의 직접 대조 (W_ad 를 싣는지는 원문 확인) | 검색 | Crossref 확인 (쪽 20245–20260 · DOI) · CC BY 는 RSC 메타 · 본문 안 엶 |
| 2 ✅ | Chu, Lerch, Chong … Janek, Rupp · *Energy Environ. Sci.* 19, 5836 (2026) — "Solubility-guided interlayer design toward balanced lithium metal plating and stripping in garnet solid-state batteries" · DOI 10.1039/D6EE03852B | Li 용해도를 친Li 성 대리 지표로 Cu · Au · Ag · Pt 층을 비교해요. Ag (친Li 최고) 는 도금은 고른데 **박리 때 공공 · 공극이 뭉친다** → 'W 가 클수록 좋다 (W ≥ 2γ_Li)' 를 박리 쪽에서 반박하는 자료라 W_ad 논지에 꼭 붙여야 해요 (가넷 계) | 검색 | Crossref 확인 (쪽 5836–5856 · DOI) — 앞 판은 부분 (DOI 미확인) |
| 3 ✅ | Becker, Schuster, Kremer, Fuchs, Janek · *Energy Environ. Sci.* 19, 2367 (2026) — "Microstructure of electrodeposited lithium and its evolution during cycling when using metal interlayers in 'anode-free' solid-state batteries" · DOI 10.1039/D5EE07230A | Au · Ag · Bi 층마다 석출 Li 의 결정립 · 방위 (EBSD) 가 다르고 박리하면 바뀌어요 → Li 슬랩 면 선택 근거 + Ag 층 기전. 표 2 #8 Fuchs 2024 EBSD 의 후속 | 검색 | Crossref 확인 (쪽 2367–2383 · DOI) |
| 4 ✅ | Haslam 외 · *ACS Energy Lett.* 10, 2285 (2025) — "The Effect of Alloying Interlayers on Lithium Anode Morphology and Microstructure in 'Anode-Free' Solid-State Batteries" · DOI 10.1021/acsenergylett.5c00149 · 🏷 Jeff Sakamoto | 합금 층이 Li 젖음 · 점착 · 형태를 어떻게 바꾸나 → W_ad §7 Ag 친Li 성의 실험 짝 (kim2026 이 Ag 100 nm 근거로 인용) | 보고서 1 편 (kim2026) | 확인 (kim2026 참고문헌 ref 36) · Crossref 확인 (쪽 2285–2291 · DOI · 저자 메타 'Sakamoto, Jeff') |
| 5 ✅ | Choi S. H., Baek C. H. … Choi J. W. · *Nat. Commun.* 16, 5871 (2025) — "Silver exsolution from Li-argyrodite electrolytes for initially anode-free all-solid-state batteries" · DOI 10.1038/s41467-025-61074-9 | Ag 도핑 아지로다이트 층에서 충전 때 Ag 가 빠져나와 입계 · 기공에 친Li Ag 씨앗 → Li 와 합금해 고른 도금 (2.0 MPa 파우치). LPSCl 쪽에 Ag 가 들어가는 경우라 Li \| Ag \| LPSCl 그림에 바로 걸려요 | 검색 | Crossref 확인 (논문 번호 5871 · 온라인 2025-07-01) — 앞 판은 논문 번호 미확인 |
| 6 ✅ | Hiraoka, Sakabe, Suzuki, Seki · *J. Mater. Chem. A* 13, 27960 (2025) — "Operando and ex situ Raman spectroscopies for evaluating carbon structural changes in anode-free-type sulfide-based all-solid-state Li-ion batteries" · DOI 10.1039/D5TA02406D | Ag/C 층의 **비정질 카본블랙도 충전 때 Li 를 먹어요** (D · G 띠 변화) → 탄소 종류 축에서 'Li 가 맨 탄소에 닿나 · 리튬화 탄소에 닿나' 를 가를 실험 근거 | 검색 | Crossref 확인 (쪽 27960–27969 · DOI) |
| 7 ✅ | Sandoval, Nelson, Sridhara … Dasgupta … Finegan, McDowell · *EES Batteries* 1, 1809 (2025) — "Visualizing diverse lithium growth and stripping behaviors in anode-free solid-state batteries with operando X-ray tomography" · DOI 10.1039/D5EB00111K | **LPSCl** 무음극 셀의 석출 · 박리 형태를 operando μCT 로 정량해요. 필라멘트가 원래 있던 기공을 따라 자라고 박리로 일부 되돌아가요 → DEM 공극 · 기공 조건의 대조 표적 | 검색 | Crossref 확인 (쪽 1809–1821 · DOI) |
| 8 ✅ | Ko 외 · *Nat. Commun.* 16, 1066 (2025) — "Mechanism of stable lithium plating and stripping in a metal-interlayer-inserted anode-less solid-state lithium metal battery" · DOI 10.1038/s41467-025-55821-1 | 금속 층 위치 (집전체 쪽) ↔ Li 석출 위치 · 합금 → Ag–C 층 기전의 실험 쪽 | 보고서 2 편 (lu2026 · metzler2026) | 확인 (두 참고문헌 일치) · Crossref 확인 (논문 번호 1066 · DOI) |
| 9 | Park, Naik, Vishnugopi, Mukherjee, Hatzell · *Adv. Energy Mater.* 15, 2405129 (2025) — "Lithium Kinetics in Ag–C Porous Interlayer in Reservoir-Free Solid-State Batteries" · DOI 10.1002/aenm.202405129 | Ag–C 다공 층 안 Li 수송 · 석출 위치 연속체 (기공률 ≈29 % 기준값 출처) → DEM 입력 · 대조 | 보고서 1 편 (metzler2026) | 확인 (ref 54) · Crossref 확인 (논문 번호 2405129 · DOI · 온라인 2024-12-19) |
| 10 | Zhang H., Okur F. … Kovalenko, Kravchyk · *Energy Environ. Sci.* 19, 4298 (2026) — "Suppressing dendrites via lateral lithium flux in Li metal solid-state batteries" · DOI 10.1039/D6EE02327D | Li₃Sb 모델 층 (LLZO) 에서 옆 방향 Li 흐름을 직접 재서, 층이 국부 전류를 퍼뜨려 공극을 줄인다고 해요 → '친Li 점착' 말고 '옆 수송' 기전과 갈라 볼 대조 | 검색 | Crossref 확인 (권 19 · 쪽 4298–4310) — 앞 판은 부분 (권 · 쪽 미확인 · 'advance 05-27') |
| 11 | Roach, Zhu, Vema, McMeeking, Grey, Deshpande, Fleck · *Eur. J. Mech. A/Solids* 113, 105710 (2025) — "Void growth in the lithium anode of a solid state battery" · DOI 10.1016/j.euromechsol.2025.105710 | Li 크리프로 공극 성장 · 닫힘을 푼 연속체 → DEM 압력 · 크리프 조건의 비교 기준 | 보고서 2 편 (masias2019 · shi2026) | 확인 (shi2026 참고문헌 ref 43) · Crossref 확인 (논문 번호 105710 · DOI) |

## 표 2 · 그 전 (≤ 2024) — 보고서 제안

| 순위 | 논문 (저자 · 저널 권, 첫쪽 (연도)) | 왜 우리에게 (한 줄) | 출처 (어느 보고서 n 편 / 검색) | 서지 확인 |
|---|---|---|---|---|
| 1 ✅ | Lee Y.-G. 외 (Samsung) · *Nat. Energy* 5, 299 (2020) — "High-energy long-cycling all-solid-state lithium metal batteries enabled by silver–carbon composite anodes" · DOI 10.1038/s41560-020-0575-z | **Ag–C 층 원전** (Ag : 카본블랙 1 : 3 (질량 · 11-24b 원문 확인 — 처음에 3 : 1 로 잘못 적음) · 과잉 Li 없음) — 점착 트랙의 출발점인데 카드가 없어요 | 보고서 6 편 + 차순위 3 (fuchs2023 · lee2022 · lu2026 · sharafi2017 · wang2020 · yang2021_atomistic \| metzler2025 · sandoval2025 · seymour2021) | 확인 (여러 참고문헌 · 권 · 쪽 일치) · Crossref 확인 (쪽 299–308 · DOI) |
| 2 ✅ | Kasemchainan, Zekoll, Spencer Jolly, Ning, Hartley, Marrow, Bruce · *Nat. Mater.* 18, 1105 (2019) — "Critical stripping current leads to dendrite formation on plating in lithium anode solid electrolyte cells" · DOI 10.1038/s41563-019-0438-9 | **Li \| Li₆PS₅Cl** 임계 박리 전류 · 박리 공극 → 다음 도금 덴드라이트 · 3 / 7 MPa — 우리 계 그대로 | 보고서 9 편 (chatterjee2025 · kazyak2020 · kim2026 · lee2022 · sharafi2017 · wang2019 · wang2020 · yang2021 ×2) | 확인 · Crossref 확인 (쪽 1105–1111 · DOI) |
| 3 ✅ | Xie, Diallo, Kim, Tu, Ceder · *Adv. Energy Mater.* 14, 2302960 (2024) — "The microscopic mechanism of lithiation and delithiation in the Ag/C buffer layer for anode-free solid-state batteries" · DOI 10.1002/aenm.202302960 | Ag/C 층 리튬화 미시 기전 · Li–Ag 합금 순서 (합금 구동력) → W_ad §7 ③ | 보고서 4 편 + 1 (lu2026 · metzler2025 · metzler2026 · sandoval2025 \| seymour2021) | 확인 · Crossref 확인 (논문 번호 2302960 · DOI) |
| 4 ✅ | Lepley, Holzwarth · *Phys. Rev. B* 92, 214201 (2015) — "Modeling interfaces between solids: Application to Li battery materials" · DOI 10.1103/PhysRevB.92.214201 | Li \| Li₂S · Li₃PS₄ 등 **황화물 쪽 DFT 계면 · 점착 방법 원전** — 우리 W 정의와 가장 가까워요 | 보고서 4 편 (seymour2021 · sharafi2017 · yang2021 ×2) | 확인 (yang2021 둘 참고문헌) · Crossref 확인 (논문 번호 214201 · DOI) — sharafi2017 보고서의 기억분도 이걸로 맞아요 |
| 5 | Lewis, Cortes, Liu … McDowell · *Nat. Mater.* 20, 503 (2021) — "Linking void and interphase evolution to electrochemistry in solid-state batteries using operando X-ray tomography" · DOI 10.1038/s41563-020-00903-2 | Li \| Li₁₀SnP₂S₁₂ 방전 공극을 3D 로 — 공극이 계면상보다 저항을 지배 (황화물 공극 축) | 보고서 5 편 (kazyak2020 · wang2019 · wang2020 · yang2021 ×2) | 확인 (yang2021_flat 참고문헌) · Crossref 확인 (쪽 503–510 · DOI) — 나머지 보고서의 기억 · 깨진 권 · 쪽은 이걸로 대체 |
| 6 | Sandoval 외 (McDowell) · *Joule* 7, 2054 (2023) — "Structural and electrochemical evolution of alloy interfacial layers in anode-free solid-state batteries" · DOI 10.1016/j.joule.2023.07.022 | LPSCl \| Cu 무음극에서 Au · Ag 100 nm 층이 첫 도금에서 어떻게 바뀌나 — Ag 층의 황화물 쪽 원형 | 보고서 3 편 + 1 (fuchs2023 · sandoval2025 · wang2020 \| metzler2026) | 확인 (sandoval2025 참고문헌) · Crossref 확인 (제목 · 쪽 2054–2073 · DOI) |
| 7 | Wang Z., Xia, Ji … Wang · *Nat. Energy* 9, 251 (2024) — "Lithium anode interlayer design for all-solid-state lithium-metal batteries" · DOI 10.1038/s41560-023-01426-1 | 인터레이어 설계 원리 (친Li · 소Li · 계면 에너지 · 젖음) + Li 크리프 수송 모델 — Ag–C · 공극 · 연속체 셋 다 | 보고서 3 편 (lee2022 · metzler2025 · metzler2026) | 확인 · Crossref 확인 (쪽 251–262 · DOI) |
| 8 | Fuchs, Ortmann, Becker, Haslam … Nazar, Sakamoto, Janek · *Nat. Mater.* 23, 1678 (2024) — "Imaging the microstructure of lithium and sodium metal in anode-free solid-state batteries using electron backscatter diffraction" · DOI 10.1038/s41563-024-02006-8 · 🏷 Jeff Sakamoto | 집전체 위 석출 Li 의 결정립 · 방위 — fuchs2023 이 남긴 빈칸이고 Li 슬랩 면 선택 근거 | 보고서 3 편 (fuchs2023 · metzler2026 · wang2020) | 확인 (metzler2026 참고문헌 · 저자 전체) · Crossref 확인 (쪽 1678–1685 · DOI · 저자 메타 'Sakamoto, Jeff') |
| 9 | Kim K., Siegel · *ACS Appl. Mater. Interfaces* 11, 39940 (2019) — "Predicting Wettability and the Electrochemical Window of Lithium-Metal/Solid Electrolyte Interfaces" · DOI 10.1021/acsami.9b13311 | DFT W 로 Li 접촉각을 예측한 선례 (Li \| Li₃OCl 종단별) — 우리 Young–Dupré 쓰는 법의 직접 선례 | 보고서 1 편 (seymour2021) | Crossref 확인 (제목 · 쪽 39940–39950 · DOI) — 앞 판은 제목 미확인 (참고문헌에 제목 없음) |
| 10 | Yoon J. S. 외 · *ACS Appl. Mater. Interfaces* 16, 18790 (2024) — "Thermodynamics, adhesion, and wetting at Li/Cu(-oxide) interfaces: relevance for anode-free lithium-metal batteries" · DOI 10.1021/acsami.3c19034 | Li \| Cu 점착 DFT + sessile drop · Cu₂O → Li₂O 가 젖음을 뒤집는 예 → Cu 집전체 쪽 W_ad 대조 | 보고서 1 편 (sandoval2025) | 확인 (ref 25) · Crossref 확인 (쪽 18790–18799 · DOI) |

## 그 밖 (짧게)

- **2025–2026 · 보고서 제안**: Haslam 2025 *Adv. Energy Mater.* 15, 2403614 🏷 Jeff Sakamoto (압력별 방전 · 포일 대 in situ) · Li K. 2025 *ACS AMI* 17, 3146 (압력 · 온도 크리프 공극 · 2 편) · Lin, Ruan, Wang 2025 *Adv. Sci.* 12, 2501434 (Li 점성 크리프 phase-field) · Deng (Persson · Ceder) 2025 *npj Comput. Mater.* 11, 9 (범용 MLIP 연화 — UMA 쓰는 단계 검증거리 · "Systematic softening in universal machine learning interatomic potentials" · DOI 10.1038/s41524-024-01500-6 · Crossref 확인) · Zhao (Qi) 2025 *Nat. Commun.* 16, 4283 (operando SEM · Mg–Li 가 공극을 쪼갬 · Zhao L. … Qi Y., Yao Y. · DOI 10.1038/s41467-025-59567-8 · Crossref 확인) · Cicvarić 2026 *J. Phys. Chem. C* 130, 1096 (Cu 단결정 핵생성 · 배치 cicvaric2026 의 방법 원전) · Alsaç 2025 *Chem. Rev.* 125, 2009 (관측법 리뷰) · Kwon 2025 *Adv. Funct. Mater.* 35, 2420474 (Cu 부식).
- **2025–2026 · 검색 (v2 에서 Crossref 로 다시 맞춤 · Ding 만 미확인)**: Ding … Kozinsky arXiv 2506.10944 (2025 · **미심사** · Li \| LPSCl \| Li 반응 MD 최대 300 만 원자 · **저널판 미확인** — Crossref 검색 두 번에 Ding · Kozinsky 의 Li \| LPSCl 저널 논문이 안 나왔고 arXiv API 는 429 로 못 읽었어요 · '없다' 가 아니라 '못 찾음') · Wang J. & Zhu H. *ACS Energy Lett.* 10, 2377 (2025) "Sulfide-Based Anode-Free Solid-State Batteries: Key Challenges and Emerging Solutions" (황화물 무음극 리뷰 · DOI 10.1021/acsenergylett.5c00517 · Crossref 확인 (쪽 2377–2391)) · Wang J., Liu Y., Ye M., Wang G., Xu C., Zhu H. *Small* 21, e06473 (2025) "Fundamental Understanding of 'Fresh' Lithium Nucleation and Growth in Sulfide-Based Anode-Free Solid-State Batteries: Effects of Substrate, Current Density, and Li⁺ Supply" · DOI 10.1002/smll.202506473 (Crossref 확인 · 앞 판 제목은 부제가 빠졌어요) · Packard J. S., Dai, Kang … Lin Y. *ACS Appl. Energy Mater.* (2026 · 온라인 04-03 · 권 · 쪽은 Crossref 에 아직 없음) "Dry Compressible Anode Interlayer Design Enabling All-Solid-State Batteries at Low Stack Pressure" · DOI 10.1021/acsaem.5c02931 (Ag–holey graphene 건식 층 · Crossref 확인 — 'Ag–holey graphene' 은 NASA 발표 자료 기준) · Cheng Z.-N., Huang X.-Y., Zhao C.-Z. … Zhang Q. *J. Energy Chem.* 111, 86 (2025) "Mitigating lithium void formation in all-solid-state batteries via a high lithium diffusion 3D composite interlayer" · DOI 10.1016/j.jechem.2025.07.033 (황화물 · Crossref 확인 (쪽 86–93) — '황화물' 은 검색 요약 기준) · Wang J., Zhang Y., Torres … Zhu H. *EES Batteries* 2, 1495 (2026) "Controlled lithium stripping enables a stable interface for long-cycling anode-free solid-state batteries" · DOI 10.1039/d6eb00128a (중성자 영상 · Crossref 확인 (쪽 1495–1505) · 위 *Small* · *ACS Energy Lett.* 와 같은 Wang J. … Zhu H. 그룹) · Palmer … Janek, Sakamoto, Nazar *Energy Environ. Sci.* 19, 3283 (2026) "Conformal hetero-electrolyte interface between soft oxyhalides and garnet enables low-pressure lithium-reservoir-free solid-state batteries" · DOI 10.1039/D5EE07777J 🏷 Crossref 저자 메타 'Sakamoto, Jeff' (Crossref 확인 (쪽 3283–3299) · ⚠ 제목 · 요약의 핵심은 **연한 옥시할라이드 \| 가넷 이종 전해질 계면** 이에요 — 앞 판의 'Ag 층' 은 메타에 없어서 본문 확인 전엔 Ag 층 논문으로 읽지 않아요 · 1 MPa 무저장 셀 · 우리 축과는 거리 있음).
- **≤ 2024 · 보고서 2 편 이상**: Krauskopf 2019 *ACS AMI* 11, 14463 (4 편 · 공공 확산 공극) · Krauskopf 2019 *Adv. Energy Mater.* 9, 1902568 (3+1 · Li–Mg) · Kazyak 2022 *Matter* 5, 3912 (3 · 🏷 Jeff Sakamoto · DOI 10.1016/j.matt.2022.07.020 · Crossref 확인) · Haslam 2022 *J. Power Sources* 520, 230831 (3 · 🏷) · Müller 2024 *ACS AMI* 16, 695 (2 · Au · Pt · C 씨앗층 · DOI 10.1021/acsami.3c14693 · Crossref 확인) · Doerrer 2024 *Device* 2, 100468 (2) · Haslam & Sakamoto 2023 *J. Electrochem. Soc.* 170, 040524 (2 · 🏷 · DOI 10.1149/1945-7111/accab4 · Crossref 확인) · Lee K. & Sakamoto 2024 *Adv. Energy Mater.* 14, 2303571 (2 · 🏷) · Lewis 2023 *Adv. Energy Mater.* 13, 2204186 (2) · Singh 2023 *Matter* 6, 1463 (2) · Seymour 2023 *ChemSusChem* 16, e202202215 (2 · 점착 리뷰) · Pande & Viswanathan 2019 *ACS Energy Lett.* 4, 2952 (2 · DOI 10.1021/acsenergylett.9b02306 · Crossref 확인) · Yan K. 2016 *Nat. Energy* 1, 16010 (2) · Jeong & Kim 2024 *ACS Energy Lett.* 9, 3237 (2) · Zaman 2023 *ACS AMI* 15, 37401 (2) · LePage 2019 *J. Electrochem. Soc.* 166, A89 (2) · Wang M. J. 2019 *Electrochim. Acta* 296, 842 (2 · 🏷) · Liu Z. (Qi) 2016 *J. Electrochem. Soc.* 163, A592 (2) · Krauskopf 2019 *Joule* 3, 2030 (2 · DOI 10.1016/j.joule.2019.06.013 · Crossref 확인) · Futscher 2022 *J. Mater. Chem. A* 10, 15535 (1+1 · 비정질 탄소 층) · Masias 2021 *J. Mater. Res.* 36, 729 (1+1 · 🏷) · Thomas, Behara, Van der Ven 2024 *Chem. Mater.* 36, 8936 (1+1 · Li–Ag) · Wang M. & Sakamoto 2018 *J. Power Sources* 377, 7 (1+1 · 점착 ↔ 계면 저항 · 🏷 'J. Sakamoto').
- **≤ 2024 · W_ad 방법 · 탄소 (1 편씩)**: Nagy 2019 *ACS AMI* 11, 7954 (γ_Li 면별 — 2γ 문턱 분모) · Behara 2024 *Chem. Mater.* 36, 7370 (Li 기준 물성) · Yang C.-T. (Qi) 2020 *ACS AMI* 12, 51007 (W_sep 정의 · γ_Li 출처) · Qi & Hector 2004 *Phys. Rev. B* 69, 235401 · Smith, Hong, Srolovitz 1994 *Phys. Rev. Lett.* 72, 4021 (UBER) · Gao J. 2019 *Adv. Theory Simul.* 2, 1900028 · Liao 2024 *J. Mater. Chem. A* 12, 5990 (탄소 층 · liao2025 전작) · Song 2024 *Adv. Mater.* 36, 2400165 (리튬화 탄소) · Risal 2023 *Carbon* 213, 118225 (Ag–C 리뷰).
- 나머지 단일 제안 45 편은 각 보고서 (d) 절 그대로예요 (`litdb/_curation/batch_2026_11_24/*.report.md`).

## 이미 litdb 에 있음

- 제안 99 편 · 검색 14 편 중 자체 digest 가 있는 편: **0 편**.
- 보고서들이 '이미 있다' 고 짚고 뺀 이웃 (다시 먹이지 마세요):
  - Spencer-Jolly 2023 *Joule* (Ag–흑연 층 operando XRD) → `spencerjolly2023_ag_graphite_interlayer_operando_xrd`
  - Liao 2025 *Adv. Mater.* (탄소 층 ↔ LPSCl 박리 인성) → `liao2025_interfacial_adhesion_li_plating_carbon_interlayer`
  - Kang 2026 *Adv. Energy Mater.* (Ag–C + CNF 2 층) → `kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode` (Wang Z. 2024 · Lin 2025 은 이 카드 참고문헌에만)
  - Wang M. J. 2020 *Nat. Commun.* 11, 5201 (seymour2021 보고서 #5) → 이번 배치 `wang2020_lithium_free_insitu_plating_llzo`
  - Cicvarić 2026 *J. Mater. Chem. A* (Ni(111) · Cu(111)) → 이번 배치 `cicvaric2026_…` — 표 밖 Cicvarić 2026 *J. Phys. Chem. C* 는 **다른 편**
  - 범용 MLIP 연화 리뷰 → `wang2026_umlff_review_softening_forgetting_longrange` — Deng 2025 원 논문은 **없음**

## 🏷 Jeff Sakamoto 공저 (보고서 · 확인 출처가 그렇게 말한 것만)

- 보고서가 'Jeff Sakamoto' 라고 적은 것: Haslam 2025 *ACS Energy Lett.* · Haslam 2025 *AEM* · Lee K. & Sakamoto 2024 *AEM* · Haslam & Sakamoto 2023 *JES* · Kazyak 2022 *Matter* (fuchs2023 참고문헌 저자 목록) · Haslam 2022 *JPS* · Sharafi 2017 *J. Mater. Chem. A* 5, 13475 (단일 제안).
  이 중 Haslam 2025 *ACS Energy Lett.* · Haslam & Sakamoto 2023 *JES* · Kazyak 2022 *Matter* 는 Crossref 저자 메타도 'Sakamoto, Jeff' 예요.
- 'Sakamoto, J.' 표기만 있는 것 (Jeff 로 보이지만 원문 소속 확인): Masias 2021 *JMR* · Wang M. J. 2021 *Joule* 5, 1371 · Wang M. J. 2019 *Electrochim. Acta* · Wang M. & Sakamoto 2018 *JPS* (이 넷은 Crossref 로 안 봤어요).
  Fuchs 2024 *Nat. Mater.* · (검색) Palmer 2026 *EES* 는 v2 에서 **Crossref 저자 메타가 'Sakamoto, Jeff'** 로 나왔어요 (이름까지 맞음 · 소속은 원문에서).

## 서지가 엇갈린 곳 · 기억뿐인 곳

- Jolly *ACS AMI* 12, 678 — 참고문헌 표기 2019 인데 12 권은 2020 년 권이에요 (chatterjee2025 보고서).
  → **Crossref 확인**: 첫 저자 성이 **'Spencer Jolly'** (D. Spencer Jolly) 예요 · 12(1), 678–685 · 온라인 2019-12-09 · 권호 2020-01-08 ⇒ **Spencer Jolly 2020** 으로 써요 (2019 는 온라인 날짜) · "Sodium/Na β″ Alumina Interface: Effect of Pressure on Voids" · DOI 10.1021/acsami.9b17786.
- Han *Nat. Mater.* 16, 572 — 참고문헌 표기 2016 · 16 권은 2017 년 (sharafi2017 보고서).
  → **Crossref 확인**: 16(5), 572–579 · 온라인 2016-12-19 · 권호 2017-05 ⇒ **2017** 로 써요 (2016 은 온라인 날짜) · DOI 10.1038/nmat4821.
- Müller *ACS AMI* 16, 695 — metzler2026 참고문헌이 연도를 2007 로 오기 (2024 가 맞음).
  → **Crossref 확인**: 16(1), 695–703 · 온라인 2023-12-21 · 권호 2024-01-10 ⇒ **2024** 맞아요 · DOI 10.1021/acsami.3c14693.
- Haslam & Sakamoto *JES* 170, 040524 — 제목 끝이 'Seeded Nucleation' (metzler2025) 대 'Seeded Lithium Nucleation' (metzler2026) 로 달라요.
  → **Crossref 확인**: "Stable Lithium Plating in 'Lithium Metal-Free' Solid-State Batteries Enabled by **Seeded Lithium Nucleation**" ⇒ metzler2026 쪽이 맞아요 (metzler2025 는 'Lithium' 이 빠짐) · 170(4), 040524 · DOI 10.1149/1945-7111/accab4.
- Lewis *Nat. Mater.* 20, 503 — wang2019 보고서는 권 · 쪽이 깨졌다고 했고 kazyak2020 · wang2020 · yang2021_atomistic 는 기억 → yang2021_flat 참고문헌이 기준.
  → **Crossref 확인**: 20(4), 503–510 (2021) · DOI 10.1038/s41563-020-00903-2 — yang2021_flat 참고문헌과 같아요.
- Kim & Siegel 2019 — 어느 참고문헌에도 제목이 없어요 (확인 검색도 실패).
  → **Crossref 확인**: "Predicting Wettability and the Electrochemical Window of Lithium-Metal/Solid Electrolyte Interfaces" · 11(43), 39940–39950 · DOI 10.1021/acsami.9b13311 (Crossref 에 초록은 없어요 — 'Li₃OCl 종단별' 은 seymour2021 보고서 기준).
- Kazyak 2022 *Matter* · Narayanan 2022 *Nat. Commun.* 13, 7237 · Wang Y. (Mitlin) 2023 *Adv. Mater.* 35, 2206762 — 권 · 쪽은 확인 · **제목은 기억**.
  → **Crossref 확인**: Kazyak — 기억 제목 그대로 (5(11), 3912–3934 · DOI 10.1016/j.matt.2022.07.020) · Narayanan — 기억 제목 그대로 (DOI 10.1038/s41467-022-34855-9) ·
    Wang Y. — 제목은 "Stable Anode-Free All-Solid-State Lithium Battery through Tuned Metal Wetting on the Copper Current Collector" (DOI 10.1002/adma.202206762 · Crossref 초록: Li₆PS₅Cl · Cu 위 Li₂Te · DFT + 메조 계산 — 보고서 설명과 맞아요).
- kazyak2020 보고서의 최근 4 편 (Ning 2023 *Nature* 618, 287 · McConohy 2023 *Nat. Energy* 8, 241 · Fincher 2022 *Joule* 6, 2794 · Ning 2021 *Nat. Mater.* 20, 1121) 과 wang2020 보고서 8 편은 **전부 기억** — DOI 확인 전에 인용하지 않아요.
  → **Crossref 확인 (12 편 다 DOI 받음 · 제목 · 첫 저자 · 저널 · 연도 맞음)**:
    · kazyak2020 4 편: Ning 2023 *Nature* 618, 287–293 · 10.1038/s41586-023-05970-4 · McConohy 2023 *Nat. Energy* · 10.1038/s41560-022-01186-4 (온라인 2023-01-30 · ⚠ Crossref 레코드에 권 · 쪽이 없어서 **8, 241 은 여전히 기억**) ·
      Fincher 2022 *Joule* 6, 2794–2809 · 10.1016/j.joule.2022.10.011 · Ning 2021 *Nat. Mater.* 20, 1121–1129 · 10.1038/s41563-021-00967-8.
    · wang2020 8 편: Fuchs 2024 *Nat. Mater.* 23, 1678 · 10.1038/s41563-024-02006-8 · Sandoval 2023 *Joule* 7, 2054 · 10.1016/j.joule.2023.07.022 · Kazyak 2022 *Matter* 5, 3912 · 10.1016/j.matt.2022.07.020 (🏷 가능 → Crossref 'Sakamoto, Jeff') ·
      Lewis 2021 *Nat. Mater.* 20, 503 · 10.1038/s41563-020-00903-2 · Lee Y.-G. 2020 *Nat. Energy* 5, 299 · 10.1038/s41560-020-0575-z · Krauskopf 2019 *Joule* 3, 2030–2049 · 10.1016/j.joule.2019.06.013 ·
      Kasemchainan 2019 *Nat. Mater.* 18, 1105 · 10.1038/s41563-019-0438-9 · Pande & Viswanathan 2019 *ACS Energy Lett.* 4, 2952–2959 · 10.1021/acsenergylett.9b02306.
- Deng 2025 *npj* 11 · Zhao (Qi) 2025 *Nat. Commun.* 16 · Choi 2025 *Nat. Commun.* 16 — 논문 번호가 없어요.
  → **Crossref 확인**: Deng *npj Comput. Mater.* 11, **9** · Zhao *Nat. Commun.* 16, **4283** · Choi *Nat. Commun.* 16, **5871** (DOI 는 표 1 · '그 밖' 에 적었어요).

## 검색 기록 (2026-11-24)

- 발견 (제목 없이 주제 + 연도): ① anode-free sulfide Ag carbon interlayer mechanism 2025 · ② Li6PS5Cl Li metal work of adhesion DFT 2025 · ③ lithiophilic interlayer void stripping 2026 · ④ Li creep void stack pressure sulfide 2025 · ⑤ carbon interlayer graphite defect Li nucleation anode-free 2025 · ⑥ silver lithium alloy interlayer anode-free 2026 · ⑦ Li|LPSCl MLIP MD stripping voids 2025–2026 · ⑧ Ag-C interlayer DFT carbon black anode-free 2025–2026.
- 확인 검색 18 번 (DOI · 제목 · 저자로 출판 메타 맞춤).
- 남기지 않은 것: MoS₂ 희생층 (*Nano-Micro Lett.* 2025 · 다른 전략) · LPSCl SEI 성장 (*Nat. Commun.* 2025 · SEI 쪽) · arXiv 2603.00998 (2026 · 저자 미확인) · arXiv 2412.12611 (2024-12 · 창 밖) · 황화물 anode-less 리뷰 (PMC 판 · 저널 · 연도 미확인) · Springer 2026 리뷰 (AI 요약 페이지).
- ⚠ 탄소 쪽 (흑연 basal · 결함 탄소 · CNF 와 Li 점착 DFT) 2025–2026 은 검색에 거의 안 걸렸어요 — 표 1 #6 (Raman) 이 그 축의 유일한 최근 실험 편이에요.
- **v2 Crossref 다시 맞춤 (2026-11-24)**: api.crossref.org 만 · HTTP 요청 18 번 (DOI 묶음 조회 4 번에 33 DOI → 32 건 맞음 · 서지 검색 12 번 · 초록 1 번 · 429 재시도 1 번) + arXiv API 1 건 (429 세 번 뒤 시간 초과 · 못 읽음).
  받는 기준은 제목 낱말 · 첫 저자 성 · 저널 · 연도가 다 맞을 때만이에요. 기억 DOI 로 물은 것도 Crossref 가 같은 레코드를 돌려줄 때만 받았어요 (Narayanan 은 기억 DOI 가 빗나가서 서지 검색으로 다시 찾음). 출판사 페이지 · 본문은 안 열었어요.
