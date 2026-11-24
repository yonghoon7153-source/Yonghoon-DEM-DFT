# 서지 확인 기록 — extra_papers_2026_11_24 → v2 (2026-11-24)

- 대상: `litdb/_curation/batch_2026_11_24/extra_papers_2026_11_24.md` (repo 파일은 안 고쳤어요) → 같은 폴더의 `extra_papers_2026_11_24_v2.md`.
- 쓴 것: **Crossref REST API (`api.crossref.org/works`) 만**. User-Agent 는 `litdb-bibliography-check/1.0` 하나 (이메일 · 이름 · 프로젝트 이름 없음).
  요청 간격은 2.5 초로 시작했고, 중간에 429 를 한 번 받아서 4 초로 늘렸어요 (429 → 30 초 쉬고 재시도).
- 요청 수: Crossref HTTP **18 번** (DOI 묶음 조회 4 번 · 서지 검색 12 번 · 초록 1 번 · 429 재시도 1 번) + arXiv API **1 건** (429 세 번 · 시간 초과 한 번 → 못 읽음).
- 받는 기준: **제목 낱말 · 첫 저자 성 · 저널 · 연도가 다 맞을 때만** 받았어요. 기억 DOI 로 물은 것도 Crossref 가 같은 레코드를 돌려줄 때만 받았어요
  (Narayanan 기억 DOI `10.1038/s41467-022-34855-x` 는 빗나가서 버리고 서지 검색으로 다시 찾았어요). 출판사 페이지 · 본문은 안 열었어요.
- 판정 표기: **채움** = 빈 칸 (DOI · 권 · 쪽 · 논문 번호 · 저자 · 제목) 을 채움 · **확인만** = 이미 있던 값이 Crossref 와 같음 ·
  ★ = 값 자체를 바로잡았거나 보고서끼리 엇갈린 걸 정리함 · **미확인** = 그대로 둠 (이유 적음) · ⚠ = 서지는 맞는데 한 줄 설명이 의심스러움.

## 집계

- Crossref 로 맞춘 논문 **42 편** — 빈 칸 채움 **38 편** · 확인만 **4 편** (Baer · Becker · Hiraoka · Sandoval 2025).
- 그중 ★ 바로잡음 · 엇갈림 정리 **7 편**: Spencer Jolly (성 · 연도) · Han (연도) · Müller (연도) · Haslam & Sakamoto (제목) · Lewis (권 · 쪽 표기) · Wang J. *Small* (제목 부제) · Packard (제목 하이픈).
- 그대로 미확인 **2 건**: Ding arXiv 2506.10944 의 저널판 · McConohy 2023 의 권 · 쪽 (Crossref 레코드에 없음).
- ⚠ 설명 의심 **1 건**: Palmer 2026 *EES* — Crossref 제목 · 요약에 Ag 층이 없어요.
- 우선순위 표 (표 1 · 표 2) 21 줄은 전부 Crossref 와 제목 · 저자 · 저널 · 권 · 쪽이 맞았어요 — 다른 연구로 바뀐 줄은 없어요.

## 표 1 · 최근 2 년

| # | 논문 | 전 | 후 | Crossref DOI | 판정 |
|---|---|---|---|---|---|
| 1 | Baer 2026 *J. Mater. Chem. A* | 검색 확인 (RSC 메타) · 14, 20245 | 14(31), 20245–20260 · 저자 4 명 일치 | 10.1039/D6TA00922K | 확인만 |
| 2 | Chu 2026 *Energy Environ. Sci.* | 부분 — **DOI 미확인** · 저자 'Chu, Lerch, Chong 외' | 19(17), 5836–5856 · Chu H. … Janek J., Rupp J. L. M. (10 명) | 10.1039/D6EE03852B | 채움 |
| 3 | Becker 2026 *Energy Environ. Sci.* | 검색 확인 (쪽 2367–2383) | 19(7), 2367–2383 · 저자 5 명 일치 | 10.1039/D5EE07230A | 확인만 |
| 4 | Haslam 2025 *ACS Energy Lett.* | 확인 (kim2026 ref 36) · DOI 없음 | 10(5), 2285–2291 · 마지막 저자 'Sakamoto, Jeff' | 10.1021/acsenergylett.5c00149 | 채움 |
| 5 | Choi 2025 *Nat. Commun.* | 16 (**논문 번호 미확인**) | 16, **5871** · 온라인 2025-07-01 · 저자 13 명 (Choi S. H. … Choi J. W.) | 10.1038/s41467-025-61074-9 | 채움 |
| 6 | Hiraoka 2025 *J. Mater. Chem. A* | 검색 확인 (쪽 27960–27969) | 13(34), 27960–27969 · 저자 4 명 일치 | 10.1039/D5TA02406D | 확인만 |
| 7 | Sandoval 2025 *EES Batteries* | 검색 확인 (쪽 1809–1821) | 1(6), 1809–1821 · 저자 11 명 (보고서 표기와 같음) | 10.1039/D5EB00111K | 확인만 |
| 8 | Ko 2025 *Nat. Commun.* | 확인 (두 참고문헌) · DOI 없음 | 16, 1066 · Ko D.-S. … Jung C. (11 명) | 10.1038/s41467-025-55821-1 | 채움 |
| 9 | Park 2025 *Adv. Energy Mater.* | 확인 (ref 54) · DOI 없음 | 15(16), 2405129 · 온라인 2024-12-19 | 10.1002/aenm.202405129 | 채움 |
| 10 | Zhang (Kravchyk) 2026 *Energy Environ. Sci.* | (2026, advance 05-27) · **권 · 쪽 미확인** | **19(13), 4298–4310** · 저자 12 명 (Zhang H. … Kovalenko M. V., Kravchyk K. V.) | 10.1039/D6EE02327D | 채움 |
| 11 | Roach 2025 *Eur. J. Mech. A/Solids* | 확인 (shi2026 ref 43) · DOI 없음 | 113, 105710 · 저자 7 명 일치 | 10.1016/j.euromechsol.2025.105710 | 채움 |

## 표 2 · ≤ 2024

| # | 논문 | 전 | 후 | Crossref DOI | 판정 |
|---|---|---|---|---|---|
| 1 | Lee Y.-G. 2020 *Nat. Energy* | 확인 · DOI 없음 (wang2020 보고서는 기억) | 5(4), 299–308 · 제목 그대로 | 10.1038/s41560-020-0575-z | 채움 |
| 2 | Kasemchainan 2019 *Nat. Mater.* | 확인 · DOI 없음 (wang2020 보고서는 기억) | 18(10), 1105–1111 · 저자 7 명 일치 | 10.1038/s41563-019-0438-9 | 채움 |
| 3 | Xie 2024 *Adv. Energy Mater.* | 확인 · DOI 없음 | 14(10), 2302960 | 10.1002/aenm.202302960 | 채움 |
| 4 | Lepley & Holzwarth 2015 *Phys. Rev. B* | 확인 (yang2021 둘) · sharafi2017 보고서는 기억 · DOI 없음 | 92(21), 214201 · 제목 그대로 | 10.1103/PhysRevB.92.214201 | 채움 |
| 5 | Lewis 2021 *Nat. Mater.* | 확인 (yang2021_flat) · 셋은 기억 · wang2019 보고서는 권 · 쪽 깨짐 | 20(4), 503–510 — yang2021_flat 표기가 맞아요 | 10.1038/s41563-020-00903-2 | 채움 ★ |
| 6 | Sandoval 2023 *Joule* | 확인 (sandoval2025) · 제목은 기억 | 7(9), 2054–2073 · 기억 제목 그대로 | 10.1016/j.joule.2023.07.022 | 채움 |
| 7 | Wang Z. 2024 *Nat. Energy* | 확인 · DOI 없음 | 9(3), 251–262 · Wang Z. … Wang C. | 10.1038/s41560-023-01426-1 | 채움 |
| 8 | Fuchs 2024 *Nat. Mater.* | 확인 (metzler2026) · 둘은 기억 · 'Sakamoto, J.' | 23(12), 1678–1685 · 저자 메타 **'Sakamoto, Jeff'** | 10.1038/s41563-024-02006-8 | 채움 |
| 9 | Kim & Siegel 2019 *ACS AMI* | 저자 · 권 · 쪽 확인 · **제목 미확인** | "Predicting Wettability and the Electrochemical Window of Lithium-Metal/Solid Electrolyte Interfaces" · 11(43), 39940–39950 (초록은 Crossref 에 없음) | 10.1021/acsami.9b13311 | 채움 |
| 10 | Yoon 2024 *ACS AMI* | 확인 (ref 25) · DOI 없음 | 16(15), 18790–18799 · Yoon J. S. … Siegel D. J. | 10.1021/acsami.3c19034 | 채움 |

## 그 밖 · 2025–2026

| 논문 | 전 | 후 | Crossref DOI | 판정 |
|---|---|---|---|---|
| Deng 2025 *npj Comput. Mater.* | 11 · 논문 번호 없음 · 제목 없음 | 11, **9** · "Systematic softening in universal machine learning interatomic potentials" · Deng B. … Persson K. A., Ceder G. | 10.1038/s41524-024-01500-6 | 채움 |
| Zhao (Qi) 2025 *Nat. Commun.* | 16 · 번호 없음 | 16, **4283** · Zhao L. … Qi Y., Yao Y. (11 명) · 제목은 lu2026 보고서 표기 그대로 | 10.1038/s41467-025-59567-8 | 채움 |
| Ding … Kozinsky arXiv 2506.10944 | 미심사 · 저널판 모름 · 제목 없음 | **그대로** — Crossref 서지 검색 2 번 (주제어 · 저자+주제어) 에 Ding · Kozinsky 의 Li \| LPSCl 저널 논문이 없었고, arXiv API 는 429 로 메타를 못 읽었어요. '저널판 없음' 이 아니라 '못 찾음' 이에요 | — | 미확인 |
| Wang J. & Zhu H. 2025 *ACS Energy Lett.* | 10, 2377 · DOI 는 남의 참고문헌에서 봄 · 제목 없음 | 10(5), 2377–2391 · "Sulfide-Based Anode-Free Solid-State Batteries: Key Challenges and Emerging Solutions" | 10.1021/acsenergylett.5c00517 | 채움 |
| Wang J. … Zhu H. 2025 *Small* | (2025) · **권 · 쪽 미확인** · 제목이 '…Solid-State Batteries' 에서 끝남 | **21(42), e06473** · 저자 6 명 (Wang J., Liu Y., Ye M., Wang G., Xu C., Zhu H.) · 부제 ': Effects of Substrate, Current Density, and Li⁺ Supply' 까지 | 10.1002/smll.202506473 | 채움 ★ |
| Packard … Lin 2026 *ACS Appl. Energy Mater.* | (2026) · NASA 발표 자료로만 확인 · 제목 'All Solid-State' | 온라인 2026-04-03 · **권 · 쪽은 Crossref 에 아직 없음** (ASAP) · Packard J. S. … Lin Y. (11 명) · 제목 **'All-Solid-State'** | 10.1021/acsaem.5c02931 | 채움 ★ |
| *J. Energy Chem.* 2025 "Mitigating lithium void formation…" | **저자 · 권 미확인** | Cheng Z.-N., Huang X.-Y., Zhao C.-Z. … Zhang Q. (10 명) · **111, 86–93** (권호 2025-12) | 10.1016/j.jechem.2025.07.033 | 채움 |
| *EES Batteries* 2026 "Controlled lithium stripping…" | **저자 미확인** | Wang J., Zhang Y., Torres … Zhu H. (11 명) · **2(5), 1495–1505** — 위 *Small* · *ACS Energy Lett.* 와 같은 그룹 | 10.1039/d6eb00128a | 채움 |
| Palmer 2026 *Energy Environ. Sci.* | 19, 3283 · 제목 · DOI 없음 · 'J. Sakamoto' · 설명 '가넷 + Ag 층' | 19(10), 3283–3299 · "Conformal hetero-electrolyte interface between soft oxyhalides and garnet enables low-pressure lithium-reservoir-free solid-state batteries" · 저자 메타 **'Sakamoto, Jeff'** · Crossref 요약 한 줄 = 'Soft oxyhalide electrolytes enable low hetero-electrolyte resistance with garnet at low stack pressures…' (Ag 언급 없음) | 10.1039/D5EE07777J | 채움 ⚠ |

## 그 밖 · ≤ 2024 · 엇갈린 곳 · 기억뿐인 곳

| 논문 | 전 | 후 | Crossref DOI | 판정 |
|---|---|---|---|---|
| Spencer Jolly 2020 *ACS AMI* 12, 678 | 'Jolly' · 참고문헌 2019 대 12 권 = 2020 | 첫 저자 성 **'Spencer Jolly'** · 12(1), 678–685 · 온라인 2019-12-09 · 권호 2020-01-08 ⇒ **2020** 으로 씀 · 제목 "Sodium/Na β″ Alumina Interface: Effect of Pressure on Voids" | 10.1021/acsami.9b17786 | 채움 ★ |
| Han 2017 *Nat. Mater.* 16, 572 | 참고문헌 2016 대 16 권 = 2017 | 16(5), 572–579 · 온라인 2016-12-19 · 권호 2017-05 ⇒ **2017** (2016 은 온라인 날짜) | 10.1038/nmat4821 | 채움 ★ |
| Müller 2024 *ACS AMI* 16, 695 | metzler2026 참고문헌 2007 오기 · 2024 가 맞다고 적음 | 16(1), 695–703 · 온라인 2023-12-21 · 권호 2024-01-10 ⇒ **2024** 맞음 | 10.1021/acsami.3c14693 | 채움 ★ |
| Haslam & Sakamoto 2023 *JES* 170, 040524 | 제목 끝 'Seeded Nucleation' (metzler2025) 대 'Seeded Lithium Nucleation' (metzler2026) | **'…Enabled by Seeded Lithium Nucleation'** ⇒ metzler2026 이 맞음 · 170(4), 040524 · 'Sakamoto, Jeff' | 10.1149/1945-7111/accab4 | 채움 ★ |
| Kazyak 2022 *Matter* 5, 3912 | 제목 기억 · DOI 없음 (wang2020 보고서 '🏷 가능') | 기억 제목 그대로 · 5(11), 3912–3934 · 'Sakamoto, Jeff' | 10.1016/j.matt.2022.07.020 | 채움 |
| Narayanan 2022 *Nat. Commun.* 13, 7237 | 제목 기억 · DOI 없음 | 기억 제목 그대로 (Crossref 는 'lithium∣Li6PS5Cl') · Narayanan S. … Pasta M. | 10.1038/s41467-022-34855-9 | 채움 |
| Wang Y. (Mitlin) 2023 *Adv. Mater.* 35, 2206762 | 제목 없음 ('원문 확인 필요') | "Stable Anode-Free All-Solid-State Lithium Battery through Tuned Metal Wetting on the Copper Current Collector" · 35(8) · Crossref 초록: Li₆PS₅Cl · Cu 위 Li₂Te · DFT + 메조 계산 (보고서 설명과 맞음) | 10.1002/adma.202206762 | 채움 |
| Pande & Viswanathan 2019 *ACS Energy Lett.* | 기억 (wang2020) · DOI 없음 | 제목 그대로 · 4(12), 2952–2959 | 10.1021/acsenergylett.9b02306 | 채움 |
| Krauskopf 2019 *Joule* 3, 2030 | 기억 (wang2020) · DOI 없음 | 제목 그대로 · 3(8), 2030–2049 | 10.1016/j.joule.2019.06.013 | 채움 |
| Ning 2023 *Nature* 618, 287 | 기억 (kazyak2020) | 제목 그대로 · 618(7964), 287–293 · Ning Z. … Bruce P. G. | 10.1038/s41586-023-05970-4 | 채움 |
| McConohy 2023 *Nat. Energy* 8, 241 | 기억 (kazyak2020) | 제목 · 첫 저자 · 저널 · 연도 (온라인 2023-01-30) 맞음 · **권 · 쪽은 Crossref 레코드에 없어서 8, 241 은 여전히 기억** | 10.1038/s41560-022-01186-4 | 채움 (권 · 쪽 미확인) |
| Fincher 2022 *Joule* 6, 2794 | 기억 (kazyak2020) | 제목 그대로 · 6(12), 2794–2809 · Fincher C. D. … Chiang Y.-M. | 10.1016/j.joule.2022.10.011 | 채움 |
| Ning 2021 *Nat. Mater.* 20, 1121 | 기억 (kazyak2020) | 제목 그대로 · 20(8), 1121–1129 | 10.1038/s41563-021-00967-8 | 채움 |

(wang2020 보고서 8 편 중 Fuchs 2024 · Sandoval 2023 · Lewis 2021 · Lee 2020 · Kasemchainan 2019 는 위 표 2 줄에 같이 적었어요.)

## 🏷 Jeff Sakamoto 표기

- 'Sakamoto, J.' 만 있던 Fuchs 2024 *Nat. Mater.* · Palmer 2026 *EES* → Crossref 저자 메타가 **'Sakamoto, Jeff'** (이름까지 · 소속은 여전히 원문에서).
- 이미 🏷 이던 Haslam 2025 *ACS Energy Lett.* · Haslam & Sakamoto 2023 *JES* · Kazyak 2022 *Matter* 도 Crossref 가 'Sakamoto, Jeff' 라 맞아요.
- Masias 2021 *JMR* · Wang M. J. 2021 *Joule* · Wang M. J. 2019 *Electrochim. Acta* · Wang M. & Sakamoto 2018 *JPS* 넷은 이번 범위 밖이라 Crossref 로 안 봤어요 (그대로).

## 요청 목록 (원본 응답 = scratchpad `cr_raw/<이름>.json`)

| 이름 | 물은 것 | 결과 |
|---|---|---|
| q01_knowndois | 파일에 이미 있던 DOI 9 개 묶음 | 9 / 9 |
| q02_classicsA | 기억 DOI 10 개 (kazyak2020 · wang2020 · 표 2) | 10 / 10 |
| q03_classicsB | 기억 DOI 10 개 (엇갈림 · 기억 제목) | 9 / 10 (Narayanan 빗나감) |
| q04_narayanan | 서지 검색 | 맞음 |
| q05_chu · q06_jec · q07_small · q08_zhao · q09_palmer | 서지 검색 각 1 번 | 다 맞음 |
| q10_arxiv | arXiv API id_list=2506.10944 | 429 ×3 → 시간 초과 · 못 읽음 |
| q11_ding · q12_ding_author | 저널판 서지 검색 (주제어 · 저자+주제어) | 없음 |
| q13_abstracts | Palmer · Kim & Siegel · Wang Y. 초록 | Palmer · Wang Y. 있음 · Kim & Siegel 없음 |
| q14_tablerows | 기억 DOI 4 개 (Park · Roach · Xie · Lepley) | 4 / 4 |
| q15_haslam_el · q16_ko · q17_wangz · q18_yoon | 서지 검색 각 1 번 (q16 은 429 뒤 재시도) | 다 맞음 |
