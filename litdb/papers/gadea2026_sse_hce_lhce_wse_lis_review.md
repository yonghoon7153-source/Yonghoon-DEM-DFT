<!-- digest 표준 양식 (paper-level STANDALONE) · 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md · 형식 참고 = papers/shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis.md
     2026-11-26 신규 — 논문 에이전트 (litdb-api 작업 폴더 · 배치 '11.'). 본문 11 pp 글자층 전문 정독 + 그림 5 장 원해상도 실독.
     SI · 부속 파일 없음 (논문은 'Supplementary information' 이 온라인에 있다고 적지만 이번 입력에 없다 — 내용 미확인).
     그림 폴더: tools/litdb/extract_figures.py --slug … --pdf … 로 만들었다 (그 도구가 litdb/figures/_sources.json 을 다시 쓰므로 실행 전 사본을 떠 두고 실행 직후 되돌렸다 · sha256 실행 전후 같음 3c88c1e3…5b779a).
     ⚠ 이 논문은 **액체 전해질 Li–S 리뷰**다 (sparingly solvating electrolytes = HCE · LHCE · WSE) — argyrodite SE 물성 4축 (A–D) 에 행을 만들지 않는다.
     자체 계산 0 · 자체 실험 0 · 전량 2차 인용. 우리 값은 싣지 않는다 (위치만). 새 li2s 카드 · 트랙 · 런을 제안하지 않는다 (li2s 계열 2026-11-16 닫힘).
     공유 표 (INDEX · comparison_vs_ours · _sources.json · pdf_map) 는 이번 작업 범위 밖이라 고치지 않았다 — 등록은 상위 작업이 한다. -->

# Design strategies and future directions of sparingly solvating electrolytes for lithium-sulfur batteries — Gadea, Soria-Fernández, Santiago, Carriazo & Castillo (*Commun. Mater.* 2026, 7, 9)

> slug `gadea2026_sse_hce_lhce_wse_lis_review` · DOI `10.1038/s43246-025-01026-4` · type `review (자체 계산 0 · 자체 실험 0 · 전량 2차 인용 · 참고문헌 83 · 그림 5 · 표 0 · 식 0)` · PDF `litdb/inbox/11. Design strategies and future directions of sparingly solvating electrolytes for lithium-sulfur batteries.pdf` (11 pp · sha256 `b0f17ca1…766f78`) · digested `2026-11-26` · status ✅ · 태그 **[외부 · 액체 전해질 Li–S (SSE) 리뷰 · 비-argyrodite]**
> elements: Li, S, F, N, O
> methods: XPS

> **저자**: **Sergi Gadea** · **Asier Soria-Fernández** (둘 다 CIC energiGUNE + UPV/EHU 응용화학과) · **Alexander Santiago\*** (CIC energiGUNE) · Daniel Carriazo (CIC energiGUNE + Ikerbasque) · **Julen Castillo\*** (CIC energiGUNE) — 스페인 바스크. 교신 asantiago@cicenergigune.com · jcastillo@cicenergigune.com.
> 접수 2025-03-28 · 수락 2025-11-21 (심사 ≈8 개월) · *Communications Materials* (Nature Portfolio) 7, 9 (2026) · CC BY-NC-ND 4.0 · 동료심사 파일 공개 (이번 입력엔 없음). 자금: 스페인 MICIU/AEI PID2024-162597OB-I00 · 바스크 정부 Elkartek2025 (KK2025-00054). 이해 상충 없음.
> 기여 진술: S.G. · A.S-F. 문헌 조사 / S.G. · A.S-F. · J.C. · A.S. 공동 집필 / A.S. 틀 구성 / D.C. 분석 관점 · 조언 / A.S. · J.C. 문헌 자료 분석 · 요약.
> **계보 (리뷰가 세운 줄)**: Shin 2013 *Chem. Commun.* 5 M LiTFSI 공통이온 효과 (ref 33) → Suo 2013 *Nat. Commun.* 'solvent-in-salt' 7 M (ref 34) → Lee 2017 *ACS Cent. Sci.* SSE 반응 경로 (ref 26) → Pang 2018 *Nat. Energy* G2:LiTFSI 망 구조 · 준고체 전환 (ref 39) → LHCE (TTE · OFE · TFTFE 희석제 · refs 55–58) → PFAS-free LHCE (refs 64–65) → WSE (불소화 에테르 Gao 2023 *PNAS* · THP Liao 2025 · DMM Ma 2022 · FPDMS Lu 2023 · refs 72–76) → WSE 의 LiPS 2 단 용매화 (Li 2025 *JACS* · ref 77) · 산화환원 매개 (Jin 2025 · ref 78). 같은 그룹의 전작 관점문 Soria-Fernández 2025 *Batteries Supercaps* (ref 17 · SSE + 촉매).
> 🔗 **이어 읽기 (litdb)**: SSE 개별 논문 — `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` · `liu2025_bdts_phase_mediator_cpme_quasi_solid_sulfur_lis` · `lai2026_mtbe_moderately_solvating_ether_cosolvent_lis` · `zhang2026_fpds_siloxane_dip_mediator_quasi_solid_lis` · `peng2026_er_dn_solvent_screening_csa_methf_lis` / 비교 리뷰 — `shao2026_lis_liquid_quasisolid_allsolid_comparative_review` / argyrodite 와 닿는 Li–S — `mistry2026_slei_argyrodite_ionic_liquid_quasi_solid_lis` · `yu2025_cng_host_suppress_argyrodite_oxidation_lis` · `wu2026_asslsb_li2s_reaction_mechanisms_engineering_review` — 대응은 §14.

---

## 0. 이 digest 를 읽는 법

**읽기축 (우리 트랙에서의 자리)**: 황화물 SE 논문이 아니다. 액체 Li–S 전지에서 '폴리설파이드 (LiPS) 를 덜 녹이는 전해질 (SSE)' 세 갈래 — **HCE** (고농도) · **LHCE** (국소 고농도 = HCE + 비배위 희석제) · **WSE** (약용매화 용매) — 를 개념 · 대표 사례 · 한계 · 전망 순으로 정리한 짧은 리뷰 (본문 ≈7 쪽) 다. 우리에게 쓸모는 ① 액체–준고체–전고체 Li–S 지형도에서 **SSE 가 어디 있는지** 한 장으로 잡는 것 (용어 사전 · 분류), ② litdb 에 쌓인 SSE 개별 논문 다섯 편 (§14) 의 **위계를 정리하는 표지판**, ③ 리뷰 보고 규약의 반례 (인용 저자명 오기 · 그림 수치와 본문 수치 차 · 주관 레이더) 셋이다.

**판정 요약 (§6 · §10 상세)**:

| 주장 | 판정 | 핵심 근거 |
|---|---|---|
| 용매화 구조를 SSIP → CIP/AGG 로 바꾸면 LiPS 용해가 줄고 반응이 고체–고체/준고체로 바뀌며 무기 풍부 SEI 가 생긴다 | ✅ 분야 합의를 바르게 요약 · ⚠ 정량 근거는 리뷰 안에 없다 | 전부 2차 인용 · 수치 표 0 |
| HCE 는 셔틀을 끄지만 점도 · 젖음 · 비용이 문제 | ✅ `Fig. 2` 가 받친다 | σ 1 M 12.16 → 7 M 0.91 mS cm⁻¹ · 접촉각 15.8° → 72.1° (`Fig. 2e,f`) |
| LHCE 는 HCE 의 국소 구조를 지키며 점도를 낮춘다 · 그러나 PFAS 희석제 | ✅ 개념 · ⚠ 사례 수치 일부가 그림과 다르다 | TFTFE '405 Wh kg⁻¹ · 80 cycles' 는 첫 사이클 값 — 80 사이클 끝은 figure-read ≈290 (`Fig. 3b`) |
| WSE 는 '낮은 염농도 · 희석제 없음' 으로 같은 효과를 낸다 | ⚠ 대표 그림이 반례 | `Fig. 4d` THP 파우치가 **4 M** 이다 (HCE 문턱 4–5 M 근처) |
| WSE 는 반응 동역학이 개선된다 (`Fig. 1b` 'Improved reaction kinetics') | 🔴 본문과 자기모순 | 본문은 "WSE 의 느린 LiPS 산화환원은 여전히 주요 과제" (p 7) |
| WSE 사례 다수가 셔틀 억제를 보였다 | ⚠ 교락 — 사례 셋 (THP · DMM · FPDMS) 이 **SPAN** 양극이다 | SPAN 은 원래 LiPS 를 거의 안 낸다 → 셔틀 억제 근거로 못 쓴다 |
| `Fig. 5` 레이더 비교 | ⚠ 저자 스스로 '주관적 · 정량 아님' | 축 방향 (높을수록 좋음?) 미정의 · 'Li⁺ solvation' 축 의미 모호 |
| 실용 조건 (E/S < 3 µL mg⁻¹ · S > 3 mg cm⁻² · 제한된 Li) 에서 평가해야 한다 | ✅ 옳은 권고 · ⚠ 리뷰 자신은 사례를 그 잣대로 정리하지 않았다 | 사례별 E/S · 담지량 표 없음 |

**본 digest 에서 실제로 본 그림 (2026-11-26)** — 크롭 5 장 **전부** 원해상도로 봤다: `Fig. 1` · `Fig. 2` · `Fig. 3` · `Fig. 4` · `Fig. 5`. 표는 없다. 못 본 것: 없음 (단 온라인 SI · 동료심사 파일은 입력에 없어 안 봤다). 그림에서만 읽은 값은 **`figure-read ≈`** 로 적었다 (판독 정밀도는 눈금 간격의 ≈ ±3–5 %). 그림에 숫자가 인쇄된 값 (막대 위 숫자 · 접촉각 · 평균 CE · 79.1 %) 은 '인쇄' 라고 적었다.

---

## 1. 한 줄 요약

액체 Li–S 전지의 셔틀 문제를 **전해질 용매화 구조** (SSIP 지배 → CIP/AGG 지배) 로 푸는 SSE 세 세대 — HCE (> ≈4–5 M) · LHCE (HCE + 불소 에테르 희석제) · WSE (저 DN · 입체 장애 · 불소화 용매) — 를 순서대로 놓고, 각각이 셔틀 억제 · 무기 풍부 SEI 를 주는 대신 ① 점도 · 비용 (HCE) ② PFAS · 인화성 (LHCE) ③ 느린 LiPS 동역학 · 용매 후보 부족 (WSE) 이라는 값을 치른다고 정리한다. 전망은 염 다양화 · PFAS-free 희석제 · ML 기반 용매 탐색 · operando 용매화 측정 · **실용 조건 (E/S < 3 µL mg⁻¹, S > 3 mg cm⁻², 제한된 Li) 평가** 다. 분류와 문제 지형은 바르지만, 수치 비교 표가 없고 대표 그림 몇 장이 본문 주장 (WSE = 저염 · 동역학 개선 · 셔틀 억제) 과 어긋난다.

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 대상 | 액체 전해질 Li–S 전지 (S₈ 양극 · 일부 SPAN 양극 · Li 금속 음극). 일부 사례는 Li 금속 전지 (LMB · 탄산염) 에서 가져왔다 (`Fig. 3c` PFPN) |
| 질문 | LiPS 셔틀과 희박 전해액 (lean) 운전을 어떻게 동시에 풀까 — 용매화 구조를 바꾸는 세 갈래 SSE 의 원리 · 성과 · 한계는? |
| 출발 문제 (리뷰 서술) | 통상 에테르 (≈1 M Li 염 in DME/DOL) 는 SSIP 지배 → LiPS 용해 → 셔틀 · Li 부식 · 낮은 CE. 희박 전해액에서는 LiPS 가 점도를 올려 σ 와 Li⁺ 이동도가 떨어진다 → 'E/S 를 줄일수록 성능이 무너지는' 병목 |
| 답 (리뷰 구도) | SSE = 염–음이온 결합 강화로 자유 용매를 줄여 LiPS 를 덜 녹이고 음이온 유래 SEI 를 만든다. 세 갈래는 같은 목표를 다른 재료비로 낸다: HCE (염 多) → LHCE (염 多 국소 + 희석제) → WSE (용매 자체를 약하게) |
| 리뷰의 범위 | HCE · LHCE · WSE 만. 이온성 액체 · 고분자 · 준고체 · 촉매 매개 · 산화환원 매개자는 한두 줄 (ref 78 Jin) 뿐. 레이더 `Fig. 5` 외 정량 비교 없음 |
| 연구 유형 | 리뷰 (자체 데이터 0) · 그림 5 장 중 `Fig. 1` · `Fig. 5` 는 저자 자작 개념도 · 레이더 · `Fig. 2–4` 는 원 논문 그림 재사용 |
| 우리와의 거리 | 황화물 SE 물성 4축 수치 비교 없음. 개념 (SEI 의 음이온 유래 · LUMO 논법 · 호핑 대 vehicle 수송) 과 litdb 지형 정리 쪽만 닿는다 (§7) |

## 3. 핵심 수치 총정리 ★

> 규율: 아래는 전부 **문헌 소환값 (2차 인용)** 이다 — 리뷰가 원 논문에서 옮긴 값이고, 우리 db 절대값과 한 표에 섞지 않는다. 본문 명시값 · 그림 인쇄값 · `figure-read ≈` 를 칸마다 구분했다.

### 3a. 분야 수준 숫자 (리뷰 본문)

| 양 | 값 | 출처 · 비고 |
|---|---|---|
| Li–S 이론 에너지 밀도 | 2600 Wh kg⁻¹ | p 1 (ref 5) |
| 통상 전해질 | ≈1 M Li 염 in DME/DOL · SSIP 지배 | p 2 |
| HCE 농도 문턱 | "above ~4–5 M" (CIP/AGG 전환 · LUMO 가 용매 → 음이온) | p 2 · p 4 ("often exceeding … 4–5 M") |
| LHCE 대표 희석제 가격 | TTE ≈ $75 kg⁻¹ | p 5 (ref 63) |
| 실용 조건 권고 | E/S < 3 µL mg⁻¹ · S 담지 > 3 mg cm⁻² · 제한된 Li 재고 · 시제품 규모 | p 8 (refs 81–83) |

### 3b. HCE 사례 (`Fig. 2` · 본문)

| 사례 | 값 | 출처 · 비고 |
|---|---|---|
| Shin 2013 | 5 M LiTFSI in DME/DOL — 셔틀 과충전 억제 · 사이클 개선 | ref 33 (수치 없음) |
| Suo 2013 | 7 M LiTFSI — t_Li⁺ 증가 · 균일 Li 증착 | ref 34 (수치 없음) |
| Zheng 2018 | 12 M LiFSI in DME — LiF 풍부 SEI | ref 35 |
| Nakanishi 2019 | 술폴란 HCE (고유전 · 고 DN) — LiPS 억제 · 율 개선 | ref 36 |
| Pang 2018 | G2:LiTFSI 염/용매 몰비 0.14 → 1.25 (= 7:1 → 0.8:1 · **우리 산수** 1/7 = 0.143 · 1/0.8 = 1.25) | ref 39 · ⚠ `shao2026` digest 는 0.8:1 을 **질량비**로 적었다 — 리뷰는 '몰비' 로 환산했다 (원 논문 미확인 · §10-⑦) |
| `Fig. 2a` (Pang 재사용) | 0.8:1 — 첫 figure-read ≈1265 → 20 사이클 ≈760 → 100 사이클 ≈680 mAh g⁻¹ · CE figure-read ≈99–100 % / 7:1 — 첫 ≈1000 → **24 사이클에서 끝** ≈430 mAh g⁻¹ · CE ≈95 → ≈85 % (24 번째 ≈65 %) | figure-read |
| `Fig. 2b–d` | Cu 위 Li 증착 SEM — 7:1 가는 섬유 · 1.33:1 굵은 덩어리 · 0.8:1 큰 매끈한 덩어리 (사진 삽입: 0.8:1 은 은백색 · 7:1 은 검정) | 축척 막대 **값 없음** |
| `Fig. 2e` σ (LiTFSI in DME/DOL) | 0.1 M **1.78** · 1 M **12.16** · 3 M **7.22** · 5 M **2.92** · 7 M **0.91** mS cm⁻¹ (막대 위 인쇄) | 1 M 대비 7 M ≈1/13 (**우리 산수**) · 출처 표기는 (f) 와 함께 Wu 2020 (ref 42) 로 읽힌다 |
| `Fig. 2f` 접촉각 (S 양극 · 0.06 s) | 0.1 M **15.8°** · 1.0 M **24.7°** · 3.0 M **72.1°** (인쇄) | Wu 2020 (ref 42) |

### 3c. LHCE 사례 (`Fig. 3` · 본문)

| 사례 | 값 | 출처 · 비고 |
|---|---|---|
| OFE LHCE (본문 'Zhang et al.') | 150 사이클 · 'capacity retention of 775 mAh g⁻¹' | ref 55 — ⚠ ref 55 1저자는 **Zheng** J. (2019) · 'retention' 을 용량값으로 적음 |
| OFE (Robles) | 100 사이클 65 % 유지 | ref 56 |
| TFTFE (Kim) | **405 Wh kg⁻¹** · 80 사이클 · E/S 2.0 µL mg_S⁻¹ | ref 58 (본문) — `Fig. 3b` figure-read: DME-TFTFE 첫 ≈405 → 평탄 ≈345 → 80 사이클 ≈290 Wh kg⁻¹ (≈72 %) · 대조 (DME) 첫 ≈455 → 14 사이클 ≈415 → 15 사이클에서 끝 (마지막 점 ≈275) · 10 장 적층 · 0.05D/0.05C (인쇄) → **405 는 첫 사이클 값** · 대조가 초기 에너지는 더 높다 |
| TMS-N 첨가 LHCE (He) | Li₃N–LiF 풍부 SEI · SPAN · 800 사이클 99.3 % 유지 | ref 61 |
| PFAS-free 2,5-THF + 벤조트리플루오라이드 (본문 'Cheng et al.') | SPAN · 700 사이클 · CE 99.8 % | ref 64 — ⚠ ref 64 1저자는 **Chen** L. · 제목은 Li 금속 전지 ("A 'Flexible' solvent molecule enabling high-performance lithium metal batteries") |
| 벤젠 LHCE (Hai) | 450 사이클 87.3 % · 평균 CE 98 % | ref 65 (원 제목도 Li 금속 전지) |
| PFPN 희석 LiFSI:DMC:PFPN 1:3:3 (몰) | LMB 1500 사이클 92 % · 불연 | ref 68 · Li–S 아님 (리뷰도 "LMBs 에서" 라고 밝힘) |
| `Fig. 3a` (Zhang 재사용) | 'plum pudding' 모형 — 군집 안 hopping · 군집 사이 vehicle. 오른쪽: σ vs LHCE 염농도 (가로축 ≈5 M → 0 M 역방향) — LHCE 곡선 (보라) 은 figure-read ≈3 M 근처 꼭짓점 (Δσ_h+v > 0 구간 → 묽어지면 Δσ < 0) · 파란 선은 단조 감소 · 라벨 τ, η (고농도 쪽) · n (저농도 쪽) | 축 눈금 없음 (개념도) |
| `Fig. 3c` (Zhang 재사용) | 0.3 g 씩 점화 — RCE (탄산염) 36 s 에도 연소 · HCE 18 s 에도 연소 · **PFPN-DHCE** 1 s 에 꺼짐 (인쇄) | 그림 라벨은 'DHCE' (본문은 LHCE) · 탄산염 LMB 전해질 |

### 3d. WSE 사례 (`Fig. 4` · 본문)

| 사례 | 값 | 출처 · 비고 |
|---|---|---|
| 불소화 에테르 (Gao) | 평균 CE **99.89 %** · 0.2 C 150 사이클 **787.3 mAh g⁻¹** · 만충 30 일 보관 손실 **4.3 %** | ref 72 · `Fig. 4b` 0.1 M Li₂S₆ 사진 7 병: F6DEE · F5DEE · F4DMB · F4DEE · F3DEE · DEE · DD (왼쪽 옅음 → 오른쪽 짙음 = 용해도 증가) |
| THP (Liao) | 0–50 °C · 시제품 규모 장기 사이클 | ref 73 · `Fig. 4d` 인쇄: **4 M THP** · SPAN 5 mg cm⁻² · E/SPAN 3 µL mg_SPAN⁻¹ · C/10 (첫 사이클 C/20) · 24 cm² 파우치 · 40 사이클 **79.1 %** · figure-read 첫 ≈720 → 둘째 ≈570 → ≈510 평탄 → 40 사이클 ≈420 mAh g_SPAN⁻¹ (79.1 % 는 C/10 첫 사이클 ≈530 기준으로 보인다 · 420/0.791 ≈531 · **우리 산수**) |
| DMM (Ma) | −40 °C SPAN Li–S 첫 방전 **422.3 mAh g⁻¹** · 120 사이클 **63.8 %** | ref 74 · `Fig. 4e` 인쇄: Li‖Cu −40 °C 0.25 mA cm⁻² / 0.25 mAh cm⁻² 평균 CE 1 M LiFSI DME **40.53 %** · DMM **92.61 %** · figure-read DME 점은 0–≈122 % 로 흩어지고 ≈40 사이클에서 끝 · DMM ≈85 → ≈95 % 로 150 사이클 |
| 1,3-dioxane + DMM (Pham) | CE ≈99 % · 671 mAh g⁻¹ · 100 사이클 70 % | ref 75 (농도는 리뷰에 없음 — `shao2026` digest 는 0.4 M LiTFSI 로 적었다) |
| FPDMS (Lu) | LiF · LiNₓO_y · Li₂Sₓ 풍부 SEI · SPAN 고율 · 파우치 | ref 76 · `Fig. 4f` XPS (Li 박) figure-read: F 1s LiF ≈684.7 · S–F ≈688.2 eV / N 1s S–N ≈399.8 · LiNₓO_y ≈398.6 eV / S 2p SO₂F ≈169.5 · SOₓ ≈167.2 · S_B⁰ ≈164 · LiₓSᵧ ≈162 · Li₂S ≈160 eV |
| LiPS 2 단 용매화 (본문 'Yao et al.') | WSS 소량 → LiPS 안쪽 껍질 불변 (바깥만) · 다량 → 안쪽 침투 → 산화환원 변화 | ref 77 — ⚠ ref 77 1저자는 **Li** X.-Y. (*JACS* 2025) |
| 산화환원 매개 (Jin) | WSE 의 느린 LiPS 산화를 매개로 극복 · 고율 개선 | ref 78 (수치 없음) |

### 3e. `Fig. 5` 레이더 (저자 자작 · 주관)

| 축 (6) | Conventional | HCE | LHCE | WSE |
|---|---|---|---|---|
| Li⁺ solvation | figure-read ≈0.15 | ≈0.8 | ≈0.65 | ≈0.45 |
| Shuttle suppression | ≈0.2 | ≈0.85 | ≈0.65 | ≈0.5 |
| SEI stability | ≈0.4 | ≈1.0 | ≈0.65 | ≈0.65 |
| Viscosity | ≈0.85 | ≈0.15 | ≈0.5 | ≈0.65 |
| Ionic conductivity | ≈0.85 | ≈0.35 | ≈0.5 | ≈0.65 |
| Environmental & Cost impact | ≈0.85 | ≈0.2 | ≈0.4 | ≈0.65 |

> 값은 바깥 육각형 = 1 로 둔 반지름 비 (figure-read ≈ · 눈금 숫자 없음). 저자 스스로 "subjective comparison … not quantitatively precise" (p 7). 축 방향은 그림에 없다 — 'Viscosity' 에서 통상 전해질 (저점도) 이 높으므로 '높을수록 좋음' 으로 읽히지만, 그러면 'Li⁺ solvation' 에서 강용매화 통상 전해질이 ≈0.15 인 것이 설명되지 않는다 (§10-④). 축 이름 'Enviromental' 오타.

## 4. 리뷰의 방법 — 무엇을 근거로 비교했나 ★

| 항목 | 내용 |
|---|---|
| 문헌 선정 | 기준 · 검색어 · 기간 미기재. 참고문헌 83 개 중 2023–2025 가 다수 · 업계 보도자료 1 (ref 80 Business Wire · SES AI 'Molecular Universe') |
| 비교 방법 | 서술 + 대표 사례 그림 재사용 + 주관 레이더 (`Fig. 5`). 사례별 셀 조건 (S 담지 · E/S · 염농도 · 양극 종류 S₈/SPAN · 온도 · 율) 을 한 표로 모으지 않았다 |
| 자체 계산 | 없음 (DFT · MD · ML 전부 0). 계산은 'ML · MD 가 희석제 탐색을 가속한다' (p 4 · ref 44) · '계산 용매화 모델링' (p 7) 정도로만 언급 |
| 설계 기술자 (LHCE 희석제) | ESP_max (최대 정전기 퍼텐셜 · 희석제–음이온 상호작용 · 단일상 유지) · DN (Lewis 염기도 · 낮아야 첫 껍질을 안 흔든다) · Kamlet–Taft β (수소결합 받개 세기 · 음이온 친화 간접 지표). 리뷰 자신이 "새 희석제 다수는 이 값들이 일관되게 보고되지 않는다" 고 한계 지적 (p 4) |
| WSE 설계 두 축 | 전자 (불소 같은 전자 끌개로 배위 O 의 전자 밀도 ↓) · 입체 (고리 · 큰 치환기로 배위 원자 접근 ↓ — THP · FPDMS 의 Si–CH₃ 차폐) |

## 5. 결과 — 절별 상세 (그림 실독 포함 · 모든 수치)

### 5.1 서론 (p 1–2)
- Li–S: 이론 2600 Wh kg⁻¹ · S 의 풍부 · 저가. 걸림돌 = LiPS 셔틀 (S₈ → 긴 사슬 Li₂S₈–Li₂S₆ 용해 → Li 음극으로 확산 → 활물질 손실 · 기생 반응 · 낮은 CE) + 절연성 방전 산물 (Li₂S/Li₂S₂) + Li 덴드라이트.
- 통상 DME/DOL 은 σ 와 S 양극 상용성이 좋지만 강용매화라 LiPS 를 녹인다. 희박 전해액에선 LiPS 가 점도를 올려 σ · Li⁺ 이동도가 떨어진다 (refs 14–15) → **E/S 감축 ↔ 성능** 이 핵심 병목.
- SSE 세 구조 (HCE · LHCE · WSE) 를 "최근 종합 리뷰가 부족하다" 는 동기로 정리.

### 5.2 용매화 구조의 진화 (p 2 · `Fig. 1`)
- **통상 에테르**: Li⁺ 가 용매에 완전히 둘러싸인 SSIP · 음이온은 자유. 용해–석출 (solution-mediated) 경로 → S 이용률은 좋지만 LiPS 가 음극으로 간다. LiNO₃ 같은 부동태 첨가제가 없으면 과충전 · 낮은 CE · 용량 감소 (ref 21).
- **SSE**: SSIP → CIP · AGG. 자유 용매 ↓ → 음이온 환원 ↑ → 무기 SEI (LiF · Li₃N · Li₂SOₓ). 반응 경로가 용해–석출에서 **고체–고체 또는 준고체** 로 이동. 전기화학 지문: 첫 평탄 (긴 사슬 LiPS 생성) 이 줄거나 사라지고 둘째 평탄이 두드러지며 종종 **하나의 기울어진 평탄** 으로 합쳐진다 (refs 25–26). Li₂S 가 방전 초기에 핵생성하고 더 균일하게 자란다 (ref 16).
- **LUMO 논법**: LUMO 가 용매에서 염 음이온으로 옮겨 무기 SEI 를 만든다 (ref 27).
- **값 (trade-off)**: 통상 = vehicle 수송 · SSE = 배위 자리 사이 hopping → 결합 강화 · 용매화 엔트로피 감소로 σ 하락. 과도한 LiPS 억제는 고율 · 희박 조건에서 S 동역학을 늦춰 **전기촉매** 가 필요해지고, Li₂S 석출로 양극 표면 부동태 (refs 29–30).
- **`Fig. 1a`** (실독): 양극 (위 회색) – 전해질 – Li⁰ 음극 (아래) 단면. 왼쪽 방전 (초록) / 충전 (빨강) 사이클 S₈ → Li₂S₈ → Li₂S₆ → Li₂S₄ → Li₂S/Li₂S₂. 문제 라벨 넷: 'Blocked active material · Capacity decay' (양극 위 Li₂S 덩어리 · 'Li₂S deposition') · 'Polysulfide shuttle' (녹색 화살표 아래로) · 'Active material loss · Capacity decay · Low coulombic efficiency' · 'Li anode corrosion' (음극 표면 덴드라이트). 용매 분자는 Li⁺ 주위 4 개 SSIP.
- **`Fig. 1b`** (실독): 네 칸 — 각 칸 위 = 양극 반응 · 아래 = 전해질 군집 · 맨 아래 = 음극.
  - CONVENTIONAL: 'Sluggish reaction kinetics' · 'Conductivity/Viscosity deteriorated by LiPS' · 'S-L-S Conversion Mechanism' · SSIP · 셔틀 화살표 · 'LMA poisoning'.
  - HCE: 'Sluggish reaction kinetics' · 'Higher viscosity' · 'Solid-solid reaction (No LiPS)' (LiPS 에 ✕) · CIP · AGG 큰 덩어리 · 'Anion-derived SEI'.
  - LHCE: 'Sluggish reaction kinetics' · 'Lower viscosity' (초록 = 장점) · 'Solid-solid reaction (No LiPS)' · 군집을 **희석제 (파란 막대) 가 고리처럼 감싸는** 그림 · 'Anion-derived SEI'.
  - WSE: 'Improved reaction kinetics' (초록) · 'Enhanced richer anion-derived SEI' · 'LiPS dissolution controlled' (경찰관 아이콘) · 보라 '약용매화 용매' 가 군집 안 · 'Anion-derived SEI'.
  - 범례: SOLVENT (초록) · DILUENT (파랑) · SALT ANION (주황) · Li⁺ (빨강 점) · WEAKLY-SOLVATING SOLVENT (보라).
  - ⚠ 그림이 본문과 엇갈리는 두 곳: (i) HCE · LHCE 를 '**Solid-solid (No LiPS)**' 로 그렸는데 본문은 "solid–solid **or quasi-solid**" (p 2) · (ii) WSE 를 'Improved reaction kinetics' 로 칠했는데 본문은 "the sluggish LiPS redox kinetics in WSEs remain a major challenge" (p 7) — §10-①.
  - 문단 첫머리 "The strategies outlined in 'Quenched microstructure'" (p 2) 는 이 리뷰에 없는 절 이름이다 (다른 원고의 틀이 남은 것으로 보인다 · §10-⑥).

### 5.3 HCE (p 2–4 · `Fig. 2`)
- **개념**: > ≈4–5 M 에서 CIP/AGG 전환 · LUMO 가 용매 → 음이온 · 음극 환원 산물이 유기 → 무기 SEI. '전해질이 수동 매질이 아니라 용매화 열역학 · 환원 경로의 능동 조절자' 라는 인식 전환이 HCE 의 개념적 돌파라고 쓴다.
- **성과**: 양극 — LiPS 국소화로 S 이용률 · CE 개선 (ref 32). 음극 — 안정 SEI 로 덴드라이트 감소. 사례: Shin 5 M · Suo 7 M · Zheng 12 M LiFSI/DME · Nakanishi 술폴란 (§3b).
- **Pang 2018** (`Fig. 2a–d` 실독): 같은 G2:LiTFSI 계에서 염 비율만 올렸을 때 7:1 셀은 24 사이클 만에 ≈430 mAh g⁻¹ 로 끝나고 CE 가 ≈95 → ≈85 % 로 떨어지는 반면, 0.8:1 은 100 사이클 ≈680 mAh g⁻¹ · CE ≈99–100 % (figure-read). Cu 위 Li 증착은 염 비율이 오를수록 가는 섬유 → 큰 매끈한 덩어리 (축척 막대 값 없음). 리뷰 해석: 셔틀 제거 + Li 증착 개선 둘 다.
- **한계** (`Fig. 2e,f` 실독): σ 는 1 M 12.16 이 꼭짓점이고 3 M 7.22 · 5 M 2.92 · 7 M 0.91 mS cm⁻¹ 로 급락 (0.1 M 1.78 은 운반체 부족) — 7 M 은 1 M 의 ≈1/13. S 양극 위 접촉각은 0.1 M 15.8° · 1 M 24.7° · 3 M 72.1° — 두꺼운 다공 양극 · 분리막 함침이 어렵다 → 시제품 확대가 어렵다. 비용: 4–5 M 이상의 염 사용량. 공융 혼합 · 저가 염이 대안 후보로 언급만.

### 5.4 LHCE (p 4–6 · `Fig. 3`)
- **개념**: HCE 에 **비배위 희석제** (주로 불소 에테르 또는 탄화수소) 를 넣어 전체 염농도와 점도를 낮추면서 국소 CIP/AGG 를 유지. 희석제는 첫 껍질에서 배제된다 ('분자 수준의 상분리').
- **희석제 설계 기술자**: ESP_max (너무 크면 이온–쌍극자 상호작용이 용매화 구조를 바꾸고 Li⁺ 이동도를 낮춤 · 적당하면 단일상 유지 + 산화 안정성 ↑) · 낮은 DN (첫 껍질 경쟁 회피 → 무기 SEI (LiF · Li₂Sₓ)) · Kamlet–Taft β (음이온 친화 · 극성의 간접 지표). 리뷰 스스로 이 기술자의 정량값이 새 희석제에 대해 일관되게 보고되지 않아 구조–물성 관계를 세우기 어렵다고 적는다.
- **수송** (`Fig. 3a` 실독): 'plum pudding' — 군집 (용매 + 음이온 + Li⁺) 안에서는 hopping · 군집 사이는 희석제 점도가 정하는 vehicle. 오른쪽 개념 곡선: LHCE 염농도를 ≈5 M 에서 낮추면 σ 가 올라 ≈3 M 근처에서 꼭짓점 (Δσ_h+v > 0) 이고 더 묽히면 다시 떨어진다 (Δσ_h+v < 0). 대조 파란 선 (설명 없음 — 원 그림에선 HCE 를 용매로 묽힌 경우로 보인다) 은 단조 감소. 축 눈금 없음 — 원 논문 (Zhang 2024 *J. Phys. Chem. Lett.* · ref 50) 의 개념도.
- **희석제 사례**: TTE (전형 · 저 DN · 화학적 비활성) · OFE (150 사이클 '775 mAh g⁻¹ 유지' · Robles 100 사이클 65 %) · TFTFE (Kim — DME 와의 H–F 상호작용을 약화시켜 약용매화 영역 · 405 Wh kg⁻¹ · 80 사이클 · E/S 2.0). `Fig. 3b` 실독: 10 장 적층 셀 · E/S 2 · 0.05D/0.05C — DME-TFTFE 는 figure-read ≈405 → ≈345 (5 사이클 안에 ≈15 % 하락) → ≈290 Wh kg⁻¹ (80 사이클) · 대조 DME 는 ≈455 에서 출발해 15 사이클에 끝 (인쇄 '15 cyc' 옆 점 ≈275). ⚠ 본문 '405 Wh kg⁻¹ with 80 cycles' 는 첫 사이클 값과 사이클 수를 붙여 쓴 것이다.
- **염 · 첨가제**: LiTFSI · LiFSI → LiF · Li₂S · Li₂SOₓ 풍부 SEI. TMS-N (트리메틸실릴아자이드) → Li 음극 · SPAN 양극 양쪽에 Li₃N–LiF 풍부 계면 · 800 사이클 99.3 %.
- **한계**: 불소 에테르 다수가 **PFAS** (환경 잔류 · 생체 축적 · 독성 우려 · ref 62) · 비싸다 (TTE ≈$75 kg⁻¹) · 밀도가 높아 Wh kg⁻¹ 를 깎는다 (ref 63). PFAS-free 시도: 2,5-THF + 벤조트리플루오라이드 (SPAN · 700 사이클 · CE 99.8 % · 수소결합이 2,5-THF 극성을 낮춤) · 벤젠 LHCE (불소 0 · 450 사이클 87.3 % · 평균 CE 98 % · 공액 비극성 구조의 산화 · 환원 안정성). 안전: 불소 희석제 다수가 휘발 · 인화성 (TTE 저인화점 · 저비점) → 인 함유 희석제. PFPN (불소화 포스파젠) — LiFSI:DMC:PFPN 1:3:3 · LMB 1500 사이클 92 % · N 라디칼이 가연 중간체 포획 + F · P 라디칼이 연소 억제. `Fig. 3c` 실독: RCE 36 s 후에도 큰 불꽃 · HCE 18 s 후 옅은 불꽃 · PFPN-DHCE 1 s 에 소화 (각 0.3 g). 리뷰는 "같은 라디칼 기전이 LSB 에도 적용된다" 고 쓰지만 Li–S 데이터는 없다.
- **남은 문제**: LHCE 는 t_Li⁺ 는 높지만 σ 는 묽은 전해질보다 낮다 (조밀 군집 · 점도) → 고율 · 저온 수송 한계.

### 5.5 WSE (p 6–7 · `Fig. 4`)
- **개념**: 염농도 · 희석제 대신 **저유전율 · 약한 공여능** 용매를 골라 용매화를 조절 (`Fig. 4a` 실독: 'Routine electrolytes · Solvent-rich solvation' → 'Li⁺–solvent < Li⁺–anion · Low dielectric constant · Low donor number' → 'Weakly solvating electrolytes · Anion-rich solvation' · 범례 Li⁺ · Anion · Solvent1 · Solvent2). 강용매화 용매와 비활성 희석제 사이의 '중간 · 조절 가능한' LiPS 용해도 → S 이용률과 음극 기생 반응 억제의 균형.
- **전자적 조절** (Gao · `Fig. 4b` 실독): 에테르 불소화 정도로 LiPS 용해도를 조절 — 0.1 M Li₂S₆ (S₈ + Li₂S 화학량) 병이 F6DEE (가장 옅음) → F5DEE → F4DMB → F4DEE → F3DEE → DEE → DD (가장 짙음 · 흑갈색) 로 짙어진다. 최적 불소 에테르: 평균 CE 99.89 % · 0.2 C 150 사이클 787.3 mAh g⁻¹ · 만충 30 일 보관 4.3 % 손실 — 리뷰는 '적당한' LiPS 용해도가 달력 수명의 열쇠라고 해석.
- **입체 조절** (Liao THP · `Fig. 4c,d` 실독): DME (두 자리 · 낮은 입체 장애) → THP (한 자리 · 고리 입체 장애). `Fig. 4d`: **4 M THP** · SPAN 5 mg cm⁻² · E/SPAN 3 µL mg⁻¹ · C/10 · 24 cm² 파우치 · 40 사이클 79.1 % (figure-read ≈720 → ≈420 mAh g_SPAN⁻¹ · 첫 점은 C/20). 본문은 "excellent long-term cycling … 0–50 °C" 라 쓰지만 그림은 40 사이클이다.
- **수송 · 저온** (Ma DMM · `Fig. 4e` 실독): 약한 용매–Li⁺ 결합 → 탈용매화 장벽 ↓. −40 °C Li‖Cu 평균 CE DME 40.53 % (흩어짐 · ≈40 사이클에 끝) vs DMM 92.61 % (150 사이클) · SPAN Li–S −40 °C 첫 422.3 mAh g⁻¹ · 120 사이클 63.8 %. Pham (1,3-dioxane + DMM): DME/DOL 보다 σ · 전극 동역학 우수 · LiF 풍부 SEI · CE ≈99 % · 671 mAh g⁻¹ · 100 사이클 70 %.
- **SEI** (Lu FPDMS · `Fig. 4f` 실독): Si 에 붙은 메틸이 정전기 차폐 → Li⁺ 배위 약화 → CIP/AGG. Li 박 XPS — F 1s 는 LiF (≈684.7 eV) 가 S–F (≈688.2) 보다 훨씬 큼 · N 1s 는 S–N (≈399.8) 우세 + LiNₓO_y (≈398.6) · S 2p 는 SO₂F (≈169.5) · SOₓ (≈167.2) 가 크고 S_B⁰ · LiₓSᵧ (≈162) · Li₂S (≈160) 는 작다 (figure-read). ⚠ S 2p 의 큰 성분 둘 (SO₂F · SOₓ) 은 FSI⁻ 잔류 · 분해와 겹친다 — 그림은 '무기 풍부 SEI' 보다 '음이온 유래 S–O · S–F 종 우세' 를 보여 준다.
- **WSE 의 약점 — 동역학**: Li 2025 *JACS* (본문 'Yao et al.') — 약용매화 용매 (WSS) 비율 ↑ → CE ↑ (음극 부반응 ↓) 이지만 LiPS 산화환원 ↓. WSS 소량이면 LiPS 안쪽 용매화 구조는 그대로 · 바깥만 둘러싸고, 많아지면 안쪽에 침투해 산화환원이 바뀐다 → WSS 가 주 용매인 WSE 에선 LiPS 용매화 구조를 따로 고려해야. Jin 2025: 산화환원 매개 전략으로 느린 LiPS 산화를 극복 · 고율 개선.
- **한계**: LiPS 용해도 미세 조정 (과하면 셔틀 · 부족하면 S 이용률 ↓) · 일부 WSE 는 여전히 부분 불소화 용매 (규제 · 환경) · 고안정 · 저점도 · 약용매화 · Li/S 양립을 다 만족하는 저 DN 용매 풀이 작다 · 첨단 양극과의 양립 미탐구 · 시제품 파우치 · 고담지 · 희박 전해액 조건의 계면 안정 · Li 증착 균일성 · 장기 견고성 평가가 필요. 그럼에도 '단순한 조성 · 적은 염 · 희석제 없음' 이 실용 배치에 유리하다고 결론.

### 5.6 전망 (p 7–8 · `Fig. 5`)
- **`Fig. 5`** (실독): 네 레이더 (Conventional 빨강 · HCE 파랑 · LHCE 보라 · WSE 초록) · 축 6 · 눈금 숫자 없음. 통상 = 점도 · σ · 환경/비용 쪽이 크고 용매화 · 셔틀 억제 · SEI 가 작다. HCE = 용매화 · 셔틀 억제 · SEI 최대 · 점도 · 환경/비용 최소. LHCE = 전부 중간 (≈0.4–0.65). WSE = 고르게 중상 (≈0.45–0.65) — 면적상 WSE 가 가장 '균형' 잡혀 보이게 그려졌다 (값은 §3e). 저자 단서: 문헌의 정성 경향에 기반한 주관적 비교.
- **한계 셋**: 환경 · 경제성 (염 대량 · 불소 용매) · 확대성 (고농도 · 불소 특수 용매의 대량 생산 난이도) · 점도 (특히 HCE · LHCE 도 σ 와 용매화 구조 유지 사이 trade-off).
- **연구 방향 넷**: ① **리튬염 혁신** — SSE 에서 음이온이 전해질 기능의 중심인데 연구가 LiTFSI · LiFSI (+ LiNO₃) 에 갇혀 있다. ② **저가 · 지속가능 재료** — PFAS-free 희석제 · LHCE/WSE · 재활용성 · 인화성 · 고체/하이브리드 계 양립 평가 표준 · ML/AI 로 시행착오 탈피 (refs 79–80). ③ **operando 용매화 측정** — XAS · cryo-TEM · NMR · 진동 분광 + 분자 시뮬레이션 · 다물리 모델. ④ **실용 시험 조건** — 높은 Li 과잉 · 낮은 S 담지 · 높은 E/S · 완만한 율이 실제 한계를 가린다 → E/S < 3 µL mg⁻¹ · 제한된 Li · S > 3 mg cm⁻² · 시제품 규모 · 현실적 사이클 프로토콜.
- 초록이 약속한 '하이브리드 전해질 구조 · 동적 용매화 제어' 는 전망 본문에 따로 절이 없다 — 초록에만 있다 (§10-⑤).

## 6. 메커니즘 · 논증 흐름 — 논증 사슬 판정

리뷰의 논증 사슬은 한 줄이다: **용매화 구조 (SSIP → CIP/AGG) → LiPS 용해도 ↓ + 음이온 환원 우세 → 셔틀 ↓ + 무기 SEI → 희박 전해액 사이클 ↑, 대가는 수송 · 동역학 ↓**. 세 SSE 는 그 대가를 줄이는 재료 선택의 세대 교체로 놓인다.

| 단계 | 주장 | 근거 (리뷰 안) | 판정 |
|---|---|---|---|
| ① | CIP/AGG 가 LiPS 용해를 줄인다 | 서술 · `Fig. 4b` 용해도 사진 (불소화 → 옅음) | ✅ 분야 합의 · ⚠ 리뷰 안에 용해도 수치 비교 0 (`shen2026` 의 50/80/600 mM[S] 같은 정량은 개별 논문에만) |
| ② | 반응이 고체–고체/준고체로 바뀌고 평탄이 하나로 합쳐진다 | 서술 (refs 25–26) | ✅ 서술 · ⚠ `Fig. 1b` 는 '준고체' 를 지우고 'No LiPS' 로 그렸다 — 실제 SSE 셀 (shen2026 · liu2025) 은 소량 LiPS 를 거친다 |
| ③ | LUMO 가 음이온으로 옮겨 무기 SEI | 서술 (ref 27) · `Fig. 4f` XPS | ⚠ 고립 분자/군집 LUMO 는 전극 전위에서의 환원 순서를 직접 정하지 않는다 (계면 · 동역학 · 용매화된 음이온의 환원 전위) — 정성 휴리스틱으로만 |
| ④ | SSE 는 hopping 이라 σ 가 낮다 | `Fig. 2e` (HCE) · `Fig. 3a` (LHCE 개념) | ✅ HCE 는 데이터 · LHCE 는 개념도 · WSE 는 "σ 개선" 으로 오히려 반대 서술 (Pham) — 세 갈래 수송 비교 데이터 없음 |
| ⑤ | 과도한 억제는 동역학을 늦춘다 → 촉매 · 매개 필요 | refs 29–30 · 77–78 | ✅ (litdb 의 liu2025 · zhang2026 · shen2026 이 정확히 이 문제를 푸는 논문들이다) |
| ⑥ | WSE 가 가장 균형 잡힌 다음 단계 | `Fig. 5` 레이더 · 사례 | ⚠ 레이더는 주관 · WSE 사례 다수가 SPAN (LiPS 본래 적음) · 대표 파우치가 4 M — 'WSE 우위' 는 리뷰 안 데이터로 판정 불가 |

**빠진 축 (가장 큰 교락)**: S₈ 양극과 **SPAN 양극을 갈라 쓰지 않았다**. SPAN (황화 폴리아크릴로나이트릴) 은 S 가 고분자에 공유결합돼 탄산염에서도 고체–고체로 돌아 LiPS 를 거의 내지 않는다 (`shao2026` digest §5.6 'LEQSSM ② 공유결합 가둠'). THP · DMM · FPDMS · TMS-N · 2,5-THF 사례가 SPAN 인데, 그 셀의 '긴 수명' 은 Li 음극 SEI 개선의 증거는 될 수 있어도 **'WSE 의 LiPS 셔틀 억제'** 의 증거는 아니다.

## 7. 우리 계산 대비 ★★ (`../our_dft_baseline.md` · `db/properties/`)

> 규율: 문헌 수치는 소환값이다 — 이 리뷰의 숫자와 우리 절대값을 한 표에 놓지 않는다. 이 리뷰는 **액체 전해질** · 자체 계산 0 이라 A–D 물성 4축 비교 행이 없다. 아래는 **개념**만 맞댄다.

### 7a. 방법 대조

| 항목 | 이 리뷰 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 계산 | 없음 (ML · MD 는 '가속 도구' 로 언급만) | QE PBE · UMA MLIP-MD · BVSE (Brown BV 합) · grand-potential ESW | 비교 대상 없음 |
| 안정성 논법 | LUMO (용매 → 음이온) 로 SEI 조성 설명 | 띠틈 ≠ 안정 전압 — 우리 ESW 는 grand-potential 분해 반응 (산화 개시 S²⁻ 제한 · 층①) | 같은 '전자구조로 안정성을 말한다' 계열이지만 우리 규율은 **오비탈 에너지를 전압으로 읽지 않는다** — 리뷰의 LUMO 논법을 우리 원고에 옮겨 쓰지 않는다 |
| 수송 언어 | vehicle (용매와 같이) ↔ hopping (배위 자리 사이) | 결정 argyrodite 의 Li 는 고체 골격 사이 홉 (MLIP-MD · BVSE 채널) | 이름만 같다 — 액체 군집 hopping 과 결정 격자 홉은 다른 양이다. 수치 대조 없음 |

### 7b. 개념 대조 — 우리 계와 닿는 곳

- **준고체 (quasi-solid) 의 위치**: SSE 는 액체 Li–S 를 전고체 쪽으로 미는 첫 계단이다 — 통상 (고체–액체–고체) → SSE (준고체 · 표면에서만 잠깐 녹음) → 전고체 (녹는 중간체 없음 · S | SE | 탄소 삼상 계면). argyrodite 가 들어가는 Li–S 는 `mistry2026` (이온성 액체 + argyrodite 분리막 · 고–액 계면) · `yu2025` (전고체 · argyrodite 산화) 쪽이다. 이 리뷰는 그 둘을 다루지 않는다.
- **음이온 유래 SEI**: 리뷰의 LiF · Li₃N · Li₂SOₓ · Li₂Sₓ 는 Li 금속 | 액체 전해질 계면 산물이다. 우리 SE | Li 계면은 SE 자체 (Li₆PS₅Cl) 가 환원돼 Li₂S · Li₃P · LiCl 을 내는 다른 계다 — 'Li₂S 가 SEI 에 있다' 는 공통 라벨만 같다. 우리 SEI 트랙의 Li₂S 결정 NEB 값은 여기 싣지 않는다 (CONDITIONAL · `db/properties/citation_hazards.json` 위치만).
- **산화 쪽**: 액체 Li–S 의 충전 상한 (보통 2.8–3.0 V) 은 우리 양극 작동창 판단 (2.5–4.25 V vs Li/Li⁺ · 그 아래에서 이미 grand-potential 산화 개시) 과 겹친다 — argyrodite 촉매전해질 전고체 Li–S 에서는 SE 산화가 열역학적으로 허용되는 창에서 셀이 돈다 (`yu2025` · `cronk2026_lis_cathode_interphase_chemistry` 가 실측 쪽). 이 리뷰의 SSE 들에는 그런 '반응하는 전해질 골격' 이 없다.
- **설계 기술자의 교훈**: LHCE 희석제 기술자 (ESP_max · DN · Kamlet–Taft β) 가 "새 후보에 대해 일관되게 보고되지 않아 구조–물성 관계를 못 세운다" 는 리뷰의 자기 진단은 우리 도펀트 스크리닝 기술자 (BVSE 채널 · 산화 개시 등) 에도 같은 경고다 — 기술자는 **같은 방법으로 낸 값끼리만** 순위를 매긴다 (우리 BVSE 규율: 원본 주기셀 값만 정량 · 순위).

### 7c. 🔑 층위를 갈라 쓴 결론 (원고 · 발표용 · 내부)

> **"이 리뷰는 액체 Li–S 의 sparingly solvating 전해질을 HCE · LHCE · WSE 로 나눠 '셔틀 억제 ↔ 수송 · 동역학' 의 trade-off 를 정성적으로 정리한다. 수치 비교 · 셀 조건 표가 없고, S₈ 과 SPAN 사례가 섞여 있으며, 레이더는 저자 스스로 주관적이라 밝힌다 — 우리 원고에서는 'SSE 분류와 문제 지형' 의 배경 인용으로만 쓰고, 성능 순위 근거로는 쓰지 않는다. 우리 argyrodite 계산과 직접 맞닿는 수치는 없다."**

## 8. DFT/계산 방법 ★ (템플릿 항목별)

- **code / functional / pseudo / k-points / ecut / supercell / DFT+U / AIMD / MLIP / 무질서 처리**: 전부 **해당 없음** — 자체 계산 0.
- 리뷰가 언급한 계산 관련 대목: ML · MD 로 LHCE 희석제 후보 식별 가속 (p 4 · ref 44) · ESP_max (보통 분자 DFT 정전기 퍼텐셜 표면에서 낸다 — 방법 일반 지식 · 리뷰는 계산법 미기재) · '계산 용매화 모델링' (p 7) · 'ML · AI 를 SSE 설계 파이프라인에' (p 8 · ref 79 *Angew.* 2025 + ref 80 업계 보도자료).
- **특이사항**: 계산을 근거로 쓴 그림 0. LUMO 논법은 원 논문 인용 (ref 27) 이고 리뷰 자체 오비탈 계산은 없다.

## 9. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1a | Li–S 셀 단면 — 방전/충전 S₈ → Li₂S₈ → Li₂S₆ → Li₂S₄ → Li₂S/Li₂S₂ · Li₂S 퇴적 (활물질 차단) · 폴리설파이드 셔틀 · Li 부식 · 덴드라이트 · SSIP | 액체 Li–S 문제 지형 설명용 개념도 (발표 배경 슬라이드 후보 · 인용 필요) |
| 1b | 네 칸 비교 — Conventional (SSIP · 셔틀 · LMA poisoning) · HCE (CIP/AGG · 고점도 · 'Solid-solid (No LiPS)') · LHCE (희석제가 군집을 감쌈 · 저점도) · WSE (보라 약용매화 용매 · 'Improved reaction kinetics' · 'LiPS dissolution controlled') · 셋 다 'Anion-derived SEI' | SSE 분류 한 장 요약 · ⚠ HCE/LHCE 'No LiPS' 와 WSE '동역학 개선' 은 본문과 어긋남 (§10-①) |
| 2a | Pang 2018 G2:LiTFSI 0.8:1 vs 7:1 사이클 — 0.8:1 ≈1265 → ≈680 mAh g⁻¹ (100 cyc · CE ≈99–100 %) · 7:1 은 24 cyc 에 ≈430 으로 끝 · CE ≈95 → ≈85 % (figure-read) | HCE 셔틀 억제의 대표 데이터 (원전 = Pang 2018 *Nat. Energy*) |
| 2b–d | Cu 위 Li 증착 SEM (7:1 · 1.33:1 · 0.8:1) — 섬유 → 큰 덩어리 · 축척 값 없음 | 정성만 |
| 2e | LiTFSI DME/DOL σ — 0.1 M 1.78 · 1 M 12.16 · 3 M 7.22 · 5 M 2.92 · 7 M 0.91 mS cm⁻¹ (인쇄) | HCE 점도 대가의 숫자 (1 M → 7 M ≈1/13) |
| 2f | S 양극 접촉각 0.1 M 15.8° · 1 M 24.7° · 3 M 72.1° (0.06 s · 인쇄) | 고농도 전해질 젖음 문제 — 우리 계와 무관 (참고) |
| 3a | LHCE 'plum pudding' 모형 (군집 안 hopping · 군집 사이 vehicle) + σ vs 염농도 개념 곡선 (≈3 M 근처 꼭짓점 · 눈금 없음) | 액체 군집 수송 개념 — 결정 홉과 혼동 금지 (§7a) |
| 3b | Kim TFTFE 10 장 적층 파우치 Wh kg⁻¹ — DME-TFTFE ≈405 → ≈345 → ≈290 (80 cyc) · 대조 ≈455 → 15 cyc 끝 (E/S 2 · 0.05D/0.05C · figure-read) | 본문 '405 Wh kg⁻¹ · 80 cycles' 는 첫 사이클 값 (§10-③) |
| 3c | 점화 시험 (0.3 g) — RCE 36 s 연소 · HCE 18 s 연소 · PFPN-DHCE 1 s 소화 | 탄산염 LMB 데이터 — Li–S 근거 아님 |
| 4a | WSE 개념 — Li⁺–용매 < Li⁺–음이온 · 저유전율 · 저 DN → 음이온 풍부 용매화 | 분류 개념도 |
| 4b | Gao 불소화 에테르 7 종 0.1 M Li₂S₆ 사진 — F6DEE 옅음 → DD 짙음 | 'LiPS 용해도 조절' 의 시각 증거 (정량 없음) |
| 4c | DME (두 자리 · 낮은 입체 장애) vs THP (한 자리 · 고리 입체 장애) 구조식 | 입체 조절 설명용 |
| 4d | Liao **4 M THP** SPAN 파우치 (5 mg cm⁻² · E/SPAN 3 µL mg⁻¹ · C/10 · 24 cm²) — ≈720 (C/20) → ≈510 → ≈420 mAh g_SPAN⁻¹ · 40 cyc 79.1 % (인쇄) | 'WSE = 저염' 서술의 반례 · '장기 사이클' 이 40 cyc (§10-②) |
| 4e | Ma −40 °C Li‖Cu 평균 CE DME 40.53 % vs DMM 92.61 % (인쇄) · DME 점 흩어짐 · ≈40 cyc 끝 | 저온 약용매화 효과 (Li 금속 쪽) |
| 4f | Lu FPDMS Li 박 XPS F 1s (LiF ≈684.7 ≫ S–F ≈688.2) · N 1s (S–N ≈399.8 · LiNₓO_y ≈398.6) · S 2p (SO₂F · SOₓ 우세 · LiₓSᵧ · Li₂S 작음) (figure-read) | XPS 동정 참고 — S 2p 의 S–O/S–F 성분은 FSI⁻ 잔류와 겹침 |
| 5 | 네 전해질 레이더 (6 축 · 눈금 없음 · 저자 '주관') — HCE 셔틀/SEI 최대 · 점도/환경 최소 · WSE 고르게 중상 | 정량 비교로 인용 금지 · 축 방향 미정의 (§10-④) |

## 10. 비판 — 이 리뷰의 약한 곳 ★

**그림 ↔ 본문**

- ① **`Fig. 1b` 가 본문과 두 곳에서 어긋난다**: HCE · LHCE 를 'Solid-solid reaction (No LiPS)' 로 그렸지만 본문은 'solid–solid or quasi-solid' (p 2) 이고, 실제 SSE 셀은 소량 LiPS 를 거친다 (litdb `shen2026` 의 Li₂S₆ 용해도 50–80 mM[S] · XANES 2471 eV LiPS 신호). WSE 칸은 'Improved reaction kinetics' 로 초록 칠했지만 본문은 'sluggish LiPS redox kinetics in WSEs remain a major challenge' (p 7) — 그림만 보는 독자는 반대로 읽는다.
- ② **WSE 의 대표 그림이 WSE 의 정의와 어긋난다**: 리뷰는 WSE 를 "reduced salt concentrations · without diluents" (p 7) 로 HCE/LHCE 와 갈라 놓는데, `Fig. 4d` THP 파우치는 **4 M** (리뷰가 HCE 문턱으로 쓴 '≈4–5 M' 근처) 이다. 또 본문 'excellent long-term cycling, even under prototype-scale conditions' 의 그림은 **40 사이클 · 79.1 %** · 24 cm² 이다.
- ③ **TFTFE '405 Wh kg⁻¹ with 80 cycles'** (p 5): `Fig. 3b` 에서 405 는 첫 사이클 값이고 80 사이클 끝은 figure-read ≈290 (≈72 %). 대조 셀이 초기 에너지는 더 높다 (≈455). 'X Wh kg⁻¹ · N 사이클' 꼴 서술은 초기값과 수명을 붙여 쓰는 흔한 과장이다.
- ④ **`Fig. 5` 레이더의 축 방향이 정의되지 않았다**: 'Viscosity' · 'Environmental & Cost impact' 는 '높을수록 좋음 (낮은 점도 · 낮은 영향)' 으로 읽어야 통상 전해질 값이 맞는데, 그러면 'Li⁺ solvation' 에서 강용매화 통상 전해질이 최저 (≈0.15) · HCE 최고 (≈0.8) 인 것은 '용매화 세기' 도 '좋음' 도 아닌 무엇을 뜻하는지 불분명하다 (아마 '음이온 참여 · 용매화 구조 조절도'). 저자가 주관적이라고 단서를 달았지만, 면적이 큰 WSE 가 '최선' 처럼 보이는 시각 효과는 남는다.

**인용 · 표기**

- ⑤ 초록이 약속한 '하이브리드 전해질 구조 · 동적 용매화 제어' 미래 방향은 본문 전망 절에 없다 (전망 넷은 염 · 저가 재료 · operando · 실용 조건).
- ⑥ **본문 인용 저자명이 참고문헌과 다른 곳 셋 + 남은 틀**: 'Yao et al.' ↔ ref 77 **Li, X.-Y.** (*JACS* 2025 — `shao2026` digest 도 Li 2025 로 적음) · 'Zhang et al.' (OFE) ↔ ref 55 **Zheng, J.** (2019) · 'Cheng et al.' ↔ ref 64 **Chen, L.** · p 2 "The strategies outlined in 'Quenched microstructure'" — 이 리뷰에 없는 절 이름 (다른 원고 틀의 잔재로 보인다). `Fig. 3b` 캡션 'Copyright (2024)' ↔ ref 58 (2025). ref 62 (MOF 로 불소 가스 다루기 · *Science* — 표기도 'Science (1979' 로 깨짐) 를 PFAS 독성 근거로 단 것은 근거 대응이 약하다. ref 80 은 업계 보도자료다. ref 16 은 Li–SeS₂ 전지 논문이다 (Li–S 의 SSE 정의 근거로 인용).
- ⑦ **Pang 2018 비율**: 리뷰는 '염/용매 몰비 0.14 → 1.25' 라 썼는데 이는 G2:LiTFSI 7:1 · 0.8:1 을 몰비로 읽은 환산이다. litdb `shao2026` digest 는 0.8:1 을 **질량비** 로 적었다 — 둘 중 하나가 틀렸다 (원 논문 미확인 · 이 digest 에서 판정하지 않음).
- ⑧ OFE '150 cycles with a capacity retention of 775 mAh g⁻¹' — 유지율 (%) 자리에 용량을 썼다. 초기값이 없어 유지율을 못 낸다.

**구성 · 논증**

- ⑨ **S₈ 과 SPAN 을 섞었다** (§6 '빠진 축'): WSE · LHCE 사례 다섯 (THP · DMM · FPDMS · TMS-N · 2,5-THF) 이 SPAN 양극이다. SPAN 은 원래 LiPS 를 거의 내지 않아 셔틀 억제의 증거가 될 수 없다. 리뷰는 이 구분을 한 번도 하지 않는다.
- ⑩ **Li–S 가 아닌 데이터**: PFPN (`Fig. 3c` · 탄산염 LMB) · ref 64 · 65 (제목상 Li 금속 전지) 를 Li–S 의 LHCE 근거로 놓았다. 리뷰는 PFPN 만 'LMB 에서' 라고 밝힌다.
- ⑪ **실용 조건을 권고하면서 스스로 그 잣대로 정리하지 않았다**: 전망은 E/S < 3 µL mg⁻¹ · S > 3 mg cm⁻² · 제한된 Li 를 요구하지만, 본문 사례의 E/S · 담지 · N/P · 율을 모은 표가 없다. 그림에 인쇄된 것만 보면 E/S 2 (TFTFE) · E/SPAN 3 (THP) 정도이고 나머지는 알 수 없다.
- ⑫ **LUMO 논법을 무비판 인용**: '음이온으로 LUMO 가 옮겨 무기 SEI' 는 분야에서 흔한 휴리스틱이지만 고립 분자/군집 오비탈 에너지가 전극 전위에서의 환원 순서를 정한다는 보장은 없다 — 리뷰는 단서 없이 세 번 반복한다 (p 2 두 번 · p 4).
- ⑬ **수송 서술이 갈래마다 엇갈린다**: SSE 일반은 'hopping → σ ↓' (p 2) 인데 WSE 절은 '탈용매화 장벽 ↓ → 수송 가속 · σ 우수' (p 7). 둘 다 문헌 서술로는 맞을 수 있지만 같은 리뷰 안에서 조건 (농도 · 점도 · 온도) 을 갈라 주지 않아 독자가 판정할 수 없다.
- ⑭ **정량 비교 0**: 표 0 · 식 0. 세 갈래를 같은 축 (σ · t_Li⁺ · LiPS 용해도 · 밀도 · 가격 · Li CE) 으로 모은 숫자가 없다 — 비교 리뷰로서는 가장 큰 공백이다. 같은 지형의 `shao2026` 이 표 3 개 · 메타분석 그림을 낸 것과 대조된다.

## 11. 적용 인사이트 ★ (우리 연구에 어떻게)

1. **SSE 지형 표지판으로만 쓴다**: litdb 에 쌓인 SSE 개별 논문 (shen2026 THF/CPME · liu2025 BDTS 매개자 · lai2026 MTBE · zhang2026 FPDS · peng2026 용매 스크리닝) 을 이 리뷰의 세 갈래에 매달면 위계가 선다 — 다섯 편 모두 'WSE 의 느린 동역학 (§5.5 마지막 문단) 을 어떻게 푸나' 라는 같은 질문의 답이다 (§14).
2. **인용 규율 반례 셋** — 우리 원고 · 리뷰 프롬프트 작성 때 같은 실수를 안 하려고 적어 둔다: (a) '초기값 + 사이클 수' 붙여 쓰기 (TFTFE 405 Wh kg⁻¹ · 80 cycles), (b) 본문 인용 저자명 ↔ 참고문헌 번호 대조 (세 곳 어긋남), (c) 주관 레이더에 축 방향 · 눈금 정의 없음 — 우리 그림 하우스 스타일 (축 라벨 · 단위 명시) 로 막힌다.
3. **기술자 일관성 경고**: '기술자가 일관되게 보고되지 않아 구조–물성 관계를 못 세운다' 는 리뷰의 자기 진단 (LHCE 희석제) 은 우리 도펀트 · 계면 스크리닝 표에 그대로 걸린다 — 방법이 다른 값을 한 순위표에 섞지 않는다 (§7b).

## 12. 인용 가능 문장 (영문 초안 · 랩 표기 *Commun. Mater.*, 7, 9 (2026))

- "Sparingly solvating electrolytes for Li–S batteries are commonly grouped into highly concentrated, localized high-concentration, and weakly solvating electrolytes, all of which shift the Li⁺ solvation structure from solvent-separated ion pairs toward contact ion pairs and aggregates to suppress polysulfide dissolution." (*Commun. Mater.*, 7, 9 (2026))
- "Suppressing polysulfide solubility trades shuttle mitigation against slower sulfur redox kinetics and lower ionic conductivity." (같은 출처 — 정성 서술로만)
- "Evaluation under practical conditions, including lean electrolyte (< 3 μL mg⁻¹), high sulfur loading (> 3 mg cm⁻²), and limited lithium inventory, has been proposed as a prerequisite for assessing commercial viability." (같은 출처)
- ⛔ 쓰지 않을 문장: 'WSEs offer the best overall balance' (`Fig. 5` 주관 레이더) · 'WSEs operate at reduced salt concentration' 을 THP 사례와 함께 (4 M) · 개별 사례 수치 (원 논문을 직접 인용한다).

## 13. 주의 / 한계 (인용 규율)

- 전량 2차 인용이다 — 사례 수치는 **원 논문을 직접** 확인하고 인용한다 (특히 §10-③ · ⑥ · ⑦ · ⑧ 에서 리뷰 표기가 원전과 어긋날 수 있음을 봤다).
- `Fig. 5` 는 정량 비교로 인용 금지 (저자 단서).
- 액체 전해질 리뷰다 — 우리 argyrodite 물성 (σ · Ea · ESW · 띠틈 · 탄성) 과 같은 표에 놓지 않는다. 우리 값은 이 digest 에 싣지 않았다.
- 온라인 SI · 동료심사 파일은 입력에 없어서 확인하지 않았다.

## 14. 이어 읽기 — litdb 의 관련 digest

| digest | 이 리뷰에서의 자리 | 무엇을 더 주나 |
|---|---|---|
| `shen2026_thf_cpme_cosolvent_quasi_solid_sulfur_lis` | WSE (CPME) + 중간 용매화 공용매 (THF 22:3) — §5.5 'WSE 의 느린 동역학' 을 공용매로 푸는 시도 | 용해도 50/80/600 mM[S] · PITT · operando XRD/XANES 정량 · AIMD 용매화 보고 규약 감사 |
| `liu2025_bdts_phase_mediator_cpme_quasi_solid_sulfur_lis` | WSE (CPME) + 표면 국소 '상 매개자' 분자 — 같은 문제의 분자 해법 (Pang 그룹 · `shao2026` 이 WSE-CPME 사례로 인용) | 준고체 반응 동역학 측정 세트의 원형 |
| `lai2026_mtbe_moderately_solvating_ether_cosolvent_lis` | '중간 용매화 (moderately solvating)' — 이 리뷰의 '조절 가능한 중간 LiPS 용해도' (§5.5 첫 문단) 를 저밀도 MTBE 로 구현 · Manthiram 그룹 (THP Liao 와 같은 그룹) | DOSY · DRT · 분극 분해 · 저밀도 → Wh kg⁻¹ 관점 |
| `zhang2026_fpds_siloxane_dip_mediator_quasi_solid_lis` | 실록산 약용매화 용매 (FPDMS 계열과 같은 Si 차폐 개념 · §5.5) + 매개자 — Jin (ref 78) 의 '산화환원 매개' 와 같은 줄 | 셔틀 전류 · 자가방전 · operando XRD |
| `peng2026_er_dn_solvent_screening_csa_methf_lis` | 용매 스크리닝 (DN 등 기술자) — §5.4 '기술자 일관성' 문제와 §5.6 '저 DN 용매 풀 부족' 의 직접 답 | DN · 유전율 기반 선별 절차 |
| `shao2026_lis_liquid_quasisolid_allsolid_comparative_review` | 상위 지형 리뷰 — 이 리뷰의 세 갈래가 거기선 LEQSSM ③ 하나로 들어간다 · SPAN (LEQSSM ②) 을 따로 둬서 §10-⑨ 교락을 피한다 | 표 3 개 · 레이더 · IQSSE (argyrodite) 절 · Pang 2018 비율을 '질량비' 로 적음 (§10-⑦ 대조) |
| `mistry2026_slei_argyrodite_ionic_liquid_quasi_solid_lis` | 이 리뷰 밖 — 액체 (이온성 액체) + **argyrodite** 분리막 준고체 Li–S | 고–액 전해질 계면 (SLEI) 분해 · 우리 계와 가장 가까운 '준고체' |
| `yu2025_cng_host_suppress_argyrodite_oxidation_lis` | 이 리뷰 밖 — 전고체 Li–S 에서 argyrodite 산화 | 우리 축 ① (산화) 실측 쪽 |
| `wu2026_asslsb_li2s_reaction_mechanisms_engineering_review` | 이 리뷰 밖 — 전고체 Li–S 기전 리뷰 | 녹는 중간체가 없는 끝 지점 (§7b) |
| `guan2026_feco_vs_in2s3_li2s_electrocrystallization` · `wei2026_data_driven_hea_mediator_lis` | 리뷰 §5.2 '전기촉매가 필요해진다' (refs 29–30) 의 개별 사례 (액체 Li–S 촉매 · 매개) | Li₂S 전기결정화 판정 감사 |
| `lee2026_eecfp_dnn_electrolyte_ce_lmb` · `ma2025_active_learning_electrolyte_solvent_screening_anodefree` | 리뷰 §5.6 'ML · AI 를 SSE 설계에' (refs 79–80) 의 Li 금속 쪽 실제 사례 | 전해질 ML 스크리닝 방법 |

## 15. 기법 용어 미니사전

| 용어 | 뜻 |
|---|---|
| SSE (sparingly solvating electrolyte) | LiPS 를 조금만 녹이는 전해질의 총칭. ⚠ 우리 문서의 'SE (solid electrolyte)' 와 다르다 |
| HCE | 고농도 전해질 (> ≈4–5 M) — 자유 용매가 거의 없어 음이온이 Li⁺ 첫 껍질에 들어간다 |
| LHCE | HCE + 비배위 희석제 — 국소는 고농도 구조 · 전체는 묽고 덜 끈적 |
| WSE / WSS | 약용매화 전해질 / 약용매화 용매 (저유전율 · 저 DN · 입체 장애 · 불소화) |
| SSIP · CIP · AGG | 용매 분리 이온쌍 (음이온이 첫 껍질 밖) · 접촉 이온쌍 (음이온 1 개가 Li⁺ 하나에 직접) · 응집체 (음이온이 여러 Li⁺ 를 잇는 덩어리) |
| DN (donor number) | 용매의 Lewis 염기도 (SbCl₅ 와의 반응 엔탈피 · kcal mol⁻¹) — 클수록 Li⁺ 를 세게 잡는다 |
| ESP_max | 분자 표면 정전기 퍼텐셜의 최댓값 — 희석제가 음이온과 얼마나 끌리는지의 지표 |
| Kamlet–Taft β | 용매의 수소결합 받개 세기 (용매 극성 척도의 하나) |
| E/S | 전해액 부피 / S 질량 (µL mg⁻¹) — 작을수록 희박 (lean) · 실용 목표 < 3 |
| SPAN | 황화 폴리아크릴로나이트릴 — S 가 고분자에 공유결합 · 고체–고체 전환 · LiPS 거의 없음 |
| PFAS | 과불화 · 다불화 알킬 물질 — 잔류성 · 규제 대상 (TTE 등 불소 에테르 희석제 다수) |
| vehicle / hopping | Li⁺ 가 용매화 껍질째 움직임 / 배위 자리 사이를 건너뜀 (액체 군집 맥락) |
| LUMO 논법 | 최저 비점유 오비탈이 낮은 성분이 먼저 환원된다는 휴리스틱 — 전극 전위에서의 실제 환원 순서와 같지 않을 수 있다 |
| plum pudding 모형 | LHCE 를 '희석제 바다 속 이온 군집 (건포도)' 으로 보는 그림 |
