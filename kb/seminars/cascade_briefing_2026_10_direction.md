---
title: "cascade 진행 브리핑 (2026-10) — 08-18 덱 판정 · 13장 구성 · 현재 상황 · 방향 · 참고문헌"
date: 2026-10-12
updated: 2026-10-12
tags: [seminar, cascade, briefing, direction, references, dopant-screening, lpscl]
status: 진행
kind: seminars
system: cascade
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-mixed
---

# cascade 진행 브리핑 (2026-10) — 방향 문서

> **트랙 cascade · 1저자 = 사용자.** 이 문서는 **제안**이다. 구성·방향은 사용자가 정한다.
> 계기: 사용자 10-12 *"cascade 관련해서 간단한 진행 브리핑을 연구세미나에서 … 이 내용 아직 유지해도 되나? 10~15pg … 현재 상황이랑 앞으로의 방향성 … 확실하게 방향성을 잡아줘봐"* ·
> *"litdb 도 많아졌으니까 reference 할 수 있는 논문들 있으면 확실하게 다 갖다쓰고"*.
> 대상 덱: 사용자 업로드 `2026.08.18 … .pptx` (19장 · "Technical Report on DFT Screening: Dopants in Li6PS5Cl" · repo 밖).
> 8월 꾸러미(출처표·용어 규약·예상 질문)는 `kb/seminars/Research_Seminar_2026_08_cascade_final_*` — 이 문서는 그 위에 08-18 이후 바뀐 것을 얹는다.
>
> ⚠ **2026-10-12 정정 (원장 정독 뒤 · `kb/seminars/cascade_db_reading_2026_10_12.md`)** — 이 문서의 첫 판에 틀린 것이 둘 있었다.
> ① **"89 scored · As₂S₃ (구조 0) · AlI₃ 미완"** 은 낡은 `cascade_pool_accounting.csv` 를 그대로 옮긴 것이다. As₂S₃ · AlI₃ 는 **08-20~25 재실행(`as2s3_recover` · 60 구성)** 으로 채워져
>    **91 전부 완화 · 3,675 구성** 이다. 89 는 재실행 **전에** 만든 게이트 평가 · 별도 상 표의 수이고, 안정창 · 계면 표는 90 이다 (As₂S₃ 없음).
> ② **9월 재건(주 보고량 D_rel · 설계 목록 237 · S1 생성 규칙 · 대표 = ΔE 중앙값 — 09-12 비준 · S3 순위 규약 09-19 제안)** 이 빠져 있었다.
>    지금 도는 v7 은 그 재건 위의 파일럿이다. 실제 덱은 19장(11장 = September audit)이고, 구성의 정본은 `…_storyline_ko.md` 다.
> 아래 표의 해당 줄은 고쳐 두었고 (10-12 표시), 고치지 않은 §2 13장 구성안은 **첫 판의 제안 기록**으로 남긴다.

## 0. 한 줄 결론

**그대로는 못 쓴다.** 08-18 뒤에 다섯 가지가 바뀌었다.

1. v23 스크리닝 전체가 **탐색 자료로 강등**됐다 (09-19 · `db/properties/cascade_v23_demoted_2026_09_19.json` · *"승인된 도펀트 랭킹은 0건이다"*).
2. ESW 창 정의가 바뀌었다 (09-22 정정 A · 10-01 *OCV 빈칸 = 안정창 없음* · `D-2026-10-01-cascade-esw-no-stable-window` active).
3. 계면 산물 갭이 **HOLD** 다 (09-23 · `HZ-cascade-product-gaps-nonground-polymorph`).
4. 수송 축은 600 K 파일럿 (v6) 이 **방법상 무효로 마감**됐고 (10-01 · 자격 0/40), 1000 K 본 라운드 (v7) 가 **도는 중**이다 (10-12 · 12/40).
5. 덱의 "47" 은 8월 용어 규약에서도 틀린 읽기다 (47 = 06-25 O/F 스냅샷 · 완주 수가 아니다).
6. (10-12 추가) **9월 재건**: 주목적을 `D_rel(설계, 호스트)` 내부 비교 하나로 고정하고 (09-12) · 설계 목록 237 (조성 단위) · S1 생성 계약 · 대표 = ΔE 중앙값을 비준했다. 순위 불확실성 규약(S3)은 제안 상태로 δ 가 비어 있고, 실행 범위(#7)는 파일럿 뒤다.

⇒ 발표의 축을 **"파이프라인 기술 보고"** 에서 **"스크린이 무엇을 말할 수 있나 → 지금 무엇을 시험하나 → 어떻게 결정으로 바꾸나"** 로 옮긴다.
한 줄 메시지 (영문 슬라이드용): ***"No dopant ranking yet — the screen proposes, the pre-registered tests decide."***

## 1. 08-18 덱 슬라이드별 판정

출처 경로 약어: `P` = `db/properties/` · `SEM` = `kb/seminars/`.

| S | 내용 | 판정 | 지금 쓸 문장 / 할 일 | 근거 |
|---|---|---|---|---|
| 1 | 표지 | 유지 | 날짜·부제만 바꾼다 | — |
| 2 | Part 1 간지 | 뺀다 | 13장 구성에선 간지가 필요 없다 | — |
| 3 | 결합된 실패 모드 | **유지** | 그대로 (Kang 2026) | litdb `kang2026_…` |
| 4 | 표준 경로 vs 스크리닝 · "47 completed all three axes" | **고침** | (10-12 정정) "91 planned · **91 relaxed** (As₂S₃ · AlI₃ 는 08-20~25 재실행) · 뒤 단계 표 90 / 89" | CSV p06 · p07 (원장에서 셈) |
| 5 | 선행 (1) 깔때기 둘 | 합침 | S7 표 위 한 줄로 | Xiao 2019 · Kahle 2020 |
| 6 | 선행 (2) 모델 되먹임 | 합침 | 〃 | Sendek 2017 |
| 7 | 선행 (3) 무엇을 바꾸나 (표) | **고침** | this work 행: n = **91** (10-12 정정) · mechanical axis = "included; noise-dominated in the screen (within/between 1.104), DFT B₀ separately" · 'Li 19 / P 1 / changes with x 6' 은 유지 | `P/cascade_label_scatter_audit.json` · `P/seminar_table_site_preference.csv` |
| 8 | 후보 91종 7족 | **유지** | (10-12 정정) "All 91 relaxed — As₂S₃ and AlI₃ in an August re-run" 한 줄 · 큐레이션 목록이지 전수 탐색이 아니다 | CSV p06 |
| 9 | 원소별 최고 점수 주기율표 | **뺀다** | 점수에 옛 창 (`red_V`) 과 잡음 축 (E) 이 들어 있다 · 'block structure' 와 'Fe–Cu' 는 더 못 쓴다 | 강등 기록 §4 · `HZ-esw-reduction-limit-label` |
| 10 | 치환 자리 vs 이온 반경 | **유지** | 그대로 · UMA 상대에너지라는 라벨 · 라벨 숫자 (0.02/0.05/0.10) 는 말하지 않는다 | `P/seminar_table_site_preference.csv` |
| 11 | 배치 30개 · 3,615 · 음이온 자리 비슷 | **고침 → 백업** | "**3,615 generated structures (+60 in the August re-run = 3,675), one dopant level**" (설계 수가 아니다) · '30 average' → 항목당 중앙 30 (범위 15–120) · '고른 몫' 은 챔피언 270 행에서만 | 강등 기록 §4 · `P/seminar_table_site_grid.csv` |
| 12 | MLIP 부피 게이트 100 / 3,615 | **뺀다 → S8 감사 장으로** | 결과가 아니라 **게이트 민감도**: 기준 부피를 이 조성의 DFT 평형 (19.55 Å³/atom) 으로 바꾸면 같은 25 % 문턱이 100 대신 **1,284** 를 거른다 | `P/cascade_reanchor_comp1k444_2026_09_12.json` (산술 유지 · 해석은 가설) |
| 13 | 종마다 1구조 · "top-3 spread 0.037" | **고침 → S8 로** | 'top-3' 이 아니라 **세 명목 라벨의 챔피언** · ΔE 축 신호/잡음 0.205 (탐색) | 이야기 문서 L555–566 · scatter audit |
| 14 | 짧은 담금질 681/681 · "top ten unchanged" | **뺀다** (681 은 백업 가능) | 'top ten unchanged' 는 금지 (Top-N) · 풀 크기 맞추면 순위가 중앙 17칸 움직인다 | 강등 기록 §4 · `kb/results/champion_pool_size_bias_2026_08_18.md` |
| 15 | BVSE 지형 (무도핑 vs B₂O₃) | **유지 → 백업** | 정성 그림 · 단위 valence² · DFT B₂O₃ 셀과 cascade 'B₂O₃' 챔피언을 잇지 않는다 | 이야기 문서 L697–713 |
| 16 | DFT EOS B₀ | **유지** | 26.2 / 21.7 GPa · V/f.u. 254.16 / 243.29 Å³ (−4.3 %) — **f.u. 당으로만** · B₀′ 은 싣지 않는다 | `canonical_registry.json` (canonical) · `HZ-eos-v0-extensive` |
| 17 | 산화 창 · "five < 0.05 V" | **다시 만든다** | 정의 = 산화 한계 − OCV · 교환 0 구간 없으면 창 없음 · 호스트 **0.423 V** (MP 헐 · 0 K) · 게이트 깔때기 **89 중 21** 창 없음 (안정창 표는 90 전구체) · **새 그림 필요** | `P/oxidation_stability_cascade_v3_pinned.json` · 결정 10-01 |
| 18 | "Two designed stages produced no evidence" + 주기율표 4장 | **다시 만든다** | 그림은 **Sundar 2025 Fig. 2** 다 — 덱에 인용이 없다 (Results 장에 남의 그림) · 캡션·둘째 bullet 은 S17 복붙 · "MD 안 돌렸다" 는 이제 틀림 (v6·v7) | litdb `sundar2025_…` fig_2 (봤다) |
| 19 | Thank you | 유지 | — | — |

**덱 자체 결함 (내용과 별개)**
- 본문 글상자 (y 1.08–3.20 in) 가 그림과 **0.3–0.7 in 겹친다**: S7 · S8 · S9 · S10 · S13 · S14 · S15 · S17 · S18. LibreOffice 렌더에선 둘째 bullet 끝 줄이 그림 밑에 숨는다 (S10 · S13 · S14 · S15 · S17 · S18). 글꼴이 '-윤고딕340' 이라 렌더가 대체 글꼴이다 — **PowerPoint 에서 확인**. 고치는 법: bullet 을 한 줄로 줄이거나 그림을 0.5 in 내린다.
- S18 캡션·둘째 bullet 이 S17 과 같은 문장이다 (복붙).
- S7 의 Miara 2015 는 litdb digest 가 없다 — "via Anderson 2024" 로 인용하거나 PDF 를 넣는다.

## 2. 새 구성 — 본문 13장 (+ 백업)

각 장 = 메시지 하나. 영문 슬라이드 문구 · 그림 · 숫자 (§5 허용 목록만) · 참고문헌.

| # | 제목 (영문) | 메시지 | 그림·출처 | 참고문헌 (핵심) |
|---|---|---|---|---|
| 1 | Technical Report on DFT Screening (II): Dopants in Li₆PS₅Cl — status and next steps | — | 표지 | — |
| 2 | Where we are, in one slide | "No dopant ranking yet — the screen proposes, the pre-registered tests decide." 세 상태 카드: **Screen** 89/91 scored · exploratory · approved ranking 0 / **Stability axes** ESW corrected · interface products on hold / **Transport** 600 K pilot closed · 1000 K round 12/40 | 카드 3개 | — |
| 3 | Why a multi-axis screen | 실패 모드가 결합돼 있어 한 축만 고치면 다른 축이 나빠진다 (S3) | S3 그림 | Kang 2026 Chem. Commun. · Famprikis 2019 · Bucci 2017 |
| 4 | Prior screens and what this work varies | 선행 깔때기들 vs 우리: **전구체 화합물 하나가 두 자리를 동시에 채운다** (S5–S7 합침 · 표 갱신) | S7 표 + 새 행 셋 | Xiao 2019 · Kahle 2020 · Sendek 2017 · Anderson 2024 (Miara 2015 via) · Lee 2024 · **Jung 2026** · **Park 2026** · **Muy 2025** |
| 5 | Candidate set: 91 precursors, 89 scored | S8 표 + "89 scored · 2 gaps unfinished, not screened out" · 전구체 공치환 선례 | S8 표 | Taklu 2021 (CuCl) · Liu 2023 (MgF₂) · Jang 2023 (ZnO) · Yang 2025 (La₂O₃) · Xu 2026 (Nd–O) |
| 6 | The pipeline at a glance | 자리 열거 → 3,615 structures (all x = 0.25) → UMA relax → short anneal → BVSE → DFT EOS → grand-potential ESW · 엔진 라벨 (UMA vs DFT) 을 단계마다 | 흐름도 1장 (S4·S10–S16 압축) | UMA 2026 (Wood) · Rao 2011 · Zhu 2015 |
| 7 | Results that hold | 왼쪽 치환 자리 (S10) · 오른쪽 DFT EOS (S16) | S10 · S16 그림 | Muy 2025 · Deng 2016 · Torii 2025 (같은 양이 아니다 — 방법 앵커로만) |
| 8 | What the screen can and cannot decide | 축별 신호/잡음 (within/between): ΔE **0.205** 신호 · E **1.104** · BVSE **2.807** 잡음에 잠김 · 라벨은 농도가 아니다 (전부 x = 0.25) · 부피 게이트는 기준에 민감 (100 → 1,284) ⇒ **exploratory · approved ranking 0** | 막대 3개 (비율) | He 2018 · Ohno 2020 |
| 9 | Stability axes after the correction | ESW 정의 정정 · 호스트 0.423 V (MP hull, 0 K) · 21/89 no stable window · 계면: Sundar 2025 방식 (인용) · 우리 산물 갭은 on hold (바닥상태 다형으로 재생성 대기) | **새 ESW 그림** (정정 창) + Sundar Fig. 2 (인용) | Zhu 2015 · Xiao 2020 (Nat. Rev. Mater.) · Schwietert 2020 · Sundar 2025 · Richards 2016 |
| 10 | Transport (1): the 600 K pilot did not qualify | P1 (Al₂O₃) vs P2 (Al₂S₃) 확산비 · 40 런 중 자격 0 · MSD 가 2–100 ps 에서 아래로 휘었다 · Li 는 움직였다 (런당 ≈ 4,000 홉) ⇒ 보고량 미정의 → 마감 · **조건 꼬리표**: UMA · 600 K · 200 ps · this cell · this volume | MSD/t 모양 (값 없이) 또는 판정 흐름도 | He 2018 · Phuthi 2026 · Kahle 2020 |
| 11 | Transport (2): the 1000 K round, running | T* = 1000 K (사전 규칙의 탐침이 고름 · '확산 시작 온도' 아님) · 10 parents × P1/P2 × 2 seeds = 40 · **12/40 · 101.1 / 461.4 GPU-h · ≈ 10-21** · 40 런 뒤 **한 번** 판정 (차이 / 등가 δ = ln 1.5 / 미정 / 방법상 무효) · 셀 ≈ 1.6 nm < 2 nm | 진행 막대 + 판정 규칙 상자 | Phuthi 2026 · **Jung 2026 Fig. 5b** · UMA 2026 · Marcolongo 2017 |
| 12 | Direction | §4 로드맵 (세 단계 · 사용자 결정 표시) | 타임라인 | Phuthi 2026 · Muy 2025 · Alghamdi 2026 · Grasselli 2025 |
| 13 | Summary | 세 줄: holds / changed / next | — | — |

**백업 (본문 장수에 안 센다)**: B1 배치 격자 (S11 · 3,615 rows) · B2 BVSE 지형 (S15) · B3 담금질 681/681 (exploratory) · B4 v6 마감 허용 문장 ①–④ 원문 · B5 참고문헌 전체.

## 3. 지금 상황 (08-18 → 10-12)

| 날짜 | 일 | 출처 |
|---|---|---|
| 08-19 | 계면 축 90종 추가 (MP 자료) | `kb/results/interface_axes_90_2026_08_19.md` |
| 08-20~25 | (10-12 추가) As₂S₃ · AlI₃ 재실행 — 원자가 표에 As(+3) 추가 · 60 구성 → **91 전부 완화 · 3,675** · 정본 표 자동 갱신 안 함 | `tools/doping/run_as2s3_recover.sh` · `P/cascade_all_302_2026_08_25.csv` |
| 09-08 | (10-12 추가) D_rel 보고량 카드 비준 | `D-2026-09-08-cascade-d-rel-estimand` |
| 09-12 | (10-12 추가) 재건 개정 넷 비준 — 주목적 D_rel · 설계 목록 237 · S1 생성 계약 · 대표 = ΔE 중앙값 | `P/cascade_primary_objective_amendment_2026_09_12.json` 외 셋 |
| 09-12/13 | 축 감사 · 재앵커 비준 | `P/cascade_axis_global_audit_2026_09_12.json` · `P/cascade_reanchor_comp1k444_2026_09_12.json` |
| 09-19 | v23 탐색 자료로 강등 · v6 카드 · S3 순위 규약 **제안** (δ 빈칸) | `P/cascade_v23_demoted_2026_09_19.json` · `P/cascade_s3_protocol_amendment_2026_09_19.json` |
| 09-22 | ESW 정정 A (356 행 재유도) | `HZ-esw-reduction-limit-label` (CONDITIONAL) |
| 09-23 | 산물 갭 HOLD | `HZ-cascade-product-gaps-nonground-polymorph` |
| 10-01 | v6 마감 (자격 0/40 · 242.10 / 320 GPU-h) · OCV 빈칸 = 안정창 없음 (21종) · v7 카드 초안 | `P/cascade_d_rel_closed_2026_10_01.json` · 결정 셋 active |
| 10-03 | Codex CP: 초안 NO-GO · 방향 조건부 GO → 개정 비준 · 탐침 발사 | `kb/reviews/codex_CP_reply_…` |
| 10-06 | 탐침 끝: **T* = 1000 K** (73.07 / 141 GPU-h) | `P/cascade_v7_probe_runlog_2026_10_03.json` |
| 10-07 | 본 라운드 상한 461.4 GPU-h 비준 · 발사 | `D-2026-10-07-cascade-v7-main-round-cap` |
| 10-08 | Codex CT: 조건부 GO · P0 없음 | open_items |
| 10-12 | kgy 재부팅 → 이어받기 · **12/40 · 101.10 GPU-h · 끝 ≈ 10-21 (단독)** | `P/cascade_v7_main_runlog_2026_10_07.json` |

탄성 (modelc_2x · gabia): 12점 중 9 끝 · 13_m 은 10-11 BFGS 171 에서 세움 (r2 에 GPU 양보) · 60 스텝 게이트를 13_m · 23_p 가 넘었다 ⇒ **사용자 결정 대기**: 측정 불가로 닫기 vs 게이트 개정 (결과 본 뒤임을 기록). 이 캠페인 숫자는 아직 인용 불가 · EOS B₀ 와는 무관.

## 4. 방향 (제안)

**목표: 탐색을 '실험이 시험할 수 있는 결정' 으로 바꾼다.** 09-03 그룹미팅 지침 (`kb/seminars/group_meeting_2026_09_03_nd_professor_directives.md` D-1 *"DFT 자체는 노블티가 아니다"* · D-3 경로 2 *"스크리닝으로 뽑고 실험으로 검증"*) 의 계산판이다. 계산이 **선택을 만들어야** 차별점이 된다.

1. **지금 → ≈ 10-21: 수송 판정 하나.** v7 40 런을 끝내고 판정은 한 번. 중간 집계는 안 낸다.
   ⭐ **판정 전에** 판정 범주마다 다음 일을 적어 둔다 (닫힘 조건 먼저 · 결과 보고 고르지 않는다). 초안:
   - 실제 차이 → 전구체 음이온 (O vs S) 효과가 이 조건에서 분해된다 · 다음 전구체 쌍 하나로 넓힐지 사용자 결정
   - 실제 등가 → 이 조건에서 음이온 효과 없음 (조건 한정) · 수송 축은 선택 규칙에서 빼고 다른 축으로 고른다
   - 미정 → 부모·시드 추가는 **새 상한 결정** 없이는 안 한다
   - 방법상 무효 → 작은 셀 수송 축을 닫고 셀 크기 (≥ 2 nm) 를 바꾸는 카드로만 재개
2. **다음 1–2 달: 축 셋을 인용 가능하게.**
   - (10-12 추가) As₂S₃ 를 안정창 · 계면 · 별도 상 · 깔때기 표에 넣는다 · AlI₃ 순위 2 사용 여부를 정한다.
   - 계면: 산물 갭을 **바닥상태 다형 (E_hull = 0)** 으로 다시 만든다 → HOLD 해제 심사.
   - ESW: 정정 창 그림 + 족별 요약을 **원장 파일로** 만든다 (지금은 정정된 족별 표가 없다 — 그 전엔 족별 숫자를 슬라이드에 안 싣는다).
   - 역학: modelc_2x 탄성 게이트 결정 (닫기 / 개정).
3. **선택 규칙을 사전등록한다** — (10-12 정정) 9월 재건이 이미 뼈대를 박았다: 순위는 **주 보고량 D_rel** 로 매기고, 남은 것은 ① 순위 여유 δ (S3 · 제안 · 빈칸 · 1저자) ② 실행 범위 (#7 · 237 목록 중 무엇을 얼마나 · 예산) ③ 예측 점수 검증 축 (ρ̂ + Fisher CI + 유효 표본수) 이다. 신호가 있는 보조 축 (ΔE · 정정 ESW · HOLD 풀린 계면) 은 조건으로 붙인다. 전부 **결과 전에** 적고 → 짧은 목록 → DFT 확인 → 실험에 넘긴다. "왜 이 도펀트냐" 에 계산이 답하는 길이 이것뿐이다.
4. **그 뒤 방법 개선 (수송)**: ≥ 2 nm 셀 / 0.3 ns (Phuthi 2026 Table S1) · UMA 미세조정 (Alghamdi 2026 · Tompa 2026) · 앙상블 불확도 (Grasselli 2025) · 실제 농도는 전하중성 결함 열역학으로 (Muy 2025).

⚠ **Nd 를 cascade 로 사후 정당화하는 장은 넣지 않는다.** Nd 는 CEI 트랙 (1저자 = 실험 쪽 다른 사람) 이고, 승인 랭킹 0 인 지금 cascade 는 어떤 도펀트도 고르지 않는다. 결과를 보고 경로를 고르는 것은 마감 규율 위반이다 (09-03 지침 문서 D-3 🔗 단락).

**세미나 날짜에 따라**: 10-21 전이면 11장은 "running · no interim values" · 뒤면 판정을 v7 개정 ⑦ 허용 문장으로 싣는다.

## 5. 슬라이드 숫자 — 올려도 되는 것 / 안 되는 것

**올려도 된다 (라벨 그대로)**

| 숫자 | 라벨 | 출처 |
|---|---|---|
| 91 planned = 91 relaxed (37/19/11/10/5/5/4) · 표별 90 / 90 / 89 / 89 (10-12 정정) | curated roster · ledger coverage | CSV p06 · p07 |
| 36 cation elements | — | `P/cascade_v23_ranked_v2.csv` |
| 3,675 generated structures (3,615 + 60 re-run), one dopant level · 693 annealed | "not designs" | 강등 기록 · `P/cascade_all_302_2026_08_25.csv` |
| 237-design roster (composition unit) · approved ranking 0 | "a list, not runs" | `P/cascade_design_roster_amendment_2026_09_12.json` |
| Si only P · 19 of 26 Li · 6 change with loading · nine site pairs used | UMA relative energies | `P/seminar_table_site_preference.csv` · `P/seminar_table_site_grid.csv` |
| within/between: ΔE 0.205 · E 1.104 · BVSE 2.807 | exploratory audit | `P/cascade_label_scatter_audit.json` |
| volume gate 100 → 1,284 when re-anchored to the DFT V₀ | gate sensitivity (해석은 가설) | `P/cascade_reanchor_comp1k444_2026_09_12.json` |
| approved dopant ranking = 0 | — | 강등 기록 §3 |
| B₀ 26.2 / 21.7 GPa · V/f.u. 254.16 / 243.29 Å³ (−4.3 %) | DFT BM3 · per f.u. | `canonical_registry.json` · `HZ-eos-v0-extensive` |
| host window 0.423 V · 21 of 89 no stable window | MP hull · 0 K · oxidation limit − OCV | v3_pinned · `D-2026-10-01-cascade-esw-no-stable-window` |
| v6: 0/40 qualified · MSD bent down 2–100 ps · ≈ 4,000 hops/run | UMA · 600 K · 200 ps · this cell · this volume | `P/cascade_d_rel_closed_2026_10_01.json` 허용 ①–④ |
| v7: T* = 1000 K · 40 runs · 12/40 · 101.1 / 461.4 GPU-h · ≈ 10-21 · cell ≈ 1.6 nm < 2 nm | no values yet | v7 runlog · 결정 10-07 |

**안 된다**
- "47 completed" · "47 (91 planned)" · 47→43→25→11 · 깔때기 통과 수 (funnel_v2 머리말이 금지).
- x 라벨을 농도로 · "3,615 designs" · "30 on average" · "100 removed by the volume gate" (결과로).
- 점수 지도 · block structure · Top-N · "top ten unchanged" · Pareto.
- 옛 창: "five < 0.05 V" · 호스트 0.898 V · 족별 중앙값 0.898…0.310 · `legacy_window_V_2026_09_22` 의 모든 값.
- 산물 갭 통계 ("693 반응 / 69 % 금속 산물" 등) — HOLD.
- v5/v6 의 D · 비 · 기울기 · Ea (v5 값 포함 — 숫자는 마감 기록에만) · "Li 가 확산하지 않는다" · "레시피 효과 없음" · v7 중간값 · "T* = 확산 시작 온도".
- MLIP σ/D 절대값 · modelc_2x 탄성 숫자 · 조성 간 전단/영률 변화 (`HZ-elastic-cross-composition` 확인 전).
- 문헌 숫자를 우리 숫자와 같은 표·그림에 (`litdb/comparison_vs_ours.md` 규칙).

## 6. 참고문헌 (슬라이드 역할별)

digest 기준 서지 (`litdb/papers/<slug>.md`). ⭐ = 본문에 꼭 · 나머지는 그 장에 붙일 수 있는 것.

**도입 · 실패 모드 (3장)**
- ⭐ Kang, Chem. Commun. 62, 10277 (2026) — `kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review`
- Famprikis, Nat. Mater. 18, 1278 (2019) · Bucci, J. Mater. Chem. A 5, 19422 (2017) · Deysher, Mater. Today Phys. 24, 100679 (2022) · Kang, Energy Storage Mater. 63, 103049 (2023) · Jung, J. Mater. Chem. A 7, 22967 (2019)

**선행 스크린 · 위치 (4장)**
- ⭐ Xiao, Joule 3, 1252 (2019) · ⭐ Kahle, Energy Environ. Sci. 13, 928 (2020) · ⭐ Sendek, Energy Environ. Sci. 10, 306 (2017) · Anderson, Adv. Energy Mater. 14, 2304025 (2024) (Miara 2015 은 이것 경유 — digest 없음) · Lee, J. Mater. Chem. A 12, 7272 (2024)
- ⭐ Jung, eTransportation 28, 100570 (2026) — 가장 가까운 도펀트 깔때기 (LGPS · 란탄족 없음) · ⭐ Park, Adv. Sci. 2026, e76305 — ML 계면 안정 스크린 (R² 는 인용 금지) · ⭐ Muy, Chem. Mater. 37, 2395 (2025) — 자리별 · 전하중성 결함 열역학
- Kim, Nano Convergence 13:27 (2026) · Ong, Energy Environ. Sci. 6, 148 (2013) · Jiang, J. Mater. Chem. C 10, 18294 (2022) · 리뷰: Dutra, Nat. Rev. Mater. 10, 566 (2025) · Jain, Mater. Horiz. 13, 15 (2026)

**후보군 · 전구체 공치환 선례 (5장)**
- ⭐ Jang, J. Alloys Compd. 957, 170273 (2023) (ZnO → Zn/O · 우리와 같은 전하 위상) · ⭐ Xu, Nano Energy 157, 112246 (2026) (Nd–O · ⚠ litdb '우선 경쟁' 표시 — 선례로만)
- Taklu, Nano Energy 90, 106542 (2021) · Liu, Angew. Chem. Int. Ed. 62, e202302655 (2023) · Li, Energy Storage Mater. 77, 104221 (2025) · Yang, Electrochim. Acta 535, 146619 (2025) · Wang, Angew. Chem. Int. Ed. 64, e202501411 (2025)
- 호스트: Kraft, J. Am. Chem. Soc. 139, 10909 (2017) · de Klerk, Chem. Mater. 28, 7955 (2016) · Adeli, Angew. Chem. Int. Ed. 58, 8681 (2019)

**방법 (6–7장)**
- ⭐ Wood (UMA), arXiv:2506.23971v2 (2026) — 엔진 · D/σ/장벽 검증이 없다 → 상대량만
- ⭐ Rao, Phys. Status Solidi A 208, 1804 (2011) — argyrodite BVSE
- ⭐ Deng, J. Electrochem. Soc. 163, A67 (2016) · Torii, J. Phys. Chem. C 129, 17882 (2025) — 탄성 앵커 (B_VRH ≠ 우리 BM3 B₀ · 숫자 나란히 금지) · Jung, Adv. Funct. Mater. 2026, e78249 (O 치환 B₀ 상승 경향)
- Pustorino, Chem. Mater. 37, 313 (2025) · Sakuda, Sci. Rep. 3, 2261 (2013)

**스크린 한계 (8장)**
- ⭐ He, npj Comput. Mater. 4, 18 (2018) — 홉 수가 D 오차를 정한다 · ⭐ Ohno, ACS Energy Lett. 5, 910 (2020) — 실험실 간 산포 → 상대 주장만

**안정 축 (9장)**
- ⭐ Zhu, ACS Appl. Mater. Interfaces 7, 23685 (2015) · ⭐ Xiao, Nat. Rev. Mater. 5, 105 (2020) · ⭐ Sundar, Adv. Sci. 12, e13191 (2025) (Fig. 2 를 쓰면 반드시 인용)
- Schwietert, Nat. Mater. 19, 428 (2020) · Schwietert, JACS Au 1, 1488 (2021) · Richards, Chem. Mater. 28, 266 (2016) · Nolan, ACS Energy Lett. 4, 2444 (2019) · Wang, Angew. Chem. Int. Ed. 65, e19663 (2026) (독립 대권위 계산 — 수치는 figure-read)
- ⚠ `HZ-esw-reduction-limit-label` · `HZ-esw-reduction-limit-facet-convention` (CONDITIONAL): 우리 한계와 문헌 한계를 나란히 둘 땐 규약을 적는다 · Zhu 의 LPSC 산화 한계와 우리 값을 같은 표에 두지 않는다

**수송 (10–11장)**
- ⭐ Phuthi, Chem. Mater. 2026 (Perspective) — Table S1 벌크 하한 2 nm / 0.3 ns · 고온 아레니우스 외삽 경고 (⛔ Haven 문장은 부호가 틀렸다 — 인용하지 않는다)
- ⭐ Jung 2026 **Fig. 5b** — 1300 K 에선 Li₉P₃OS₁₁ 의 D 가 넷 중 최하위, 700 K 에선 최상위 (figure-read · 이 문서 작성 때 그림을 직접 봤다) ⇒ 고온 한 점의 순위는 낮은 온도로 옮겨지지 않는다
- Kahle 2020 · He 2018 · Marcolongo, Phys. Rev. Materials 1, 025402 (2017) (Haven < 1) · McCluskey, J. Chem. Theory Comput. 21, 79 (2025) · Wang, npj Comput. Mater. 11, 266 (2025) (범용 MLIP 장벽 과소 경향)

**방향 (12장)**
- Phuthi 2026 · Muy 2025 · Alghamdi, J. Phys. Energy 8, 025013 (2026) · Tompa, arXiv:2606.12704 (2026) · Grasselli, Digital Discovery 4, 2654 (2025) · Lomeli, ACS Appl. Mater. Interfaces 16, 51584 (2024) (부동태 기준) · Hollmann, Nature 637, 319 (2025) (능동학습 대리 모델)

**인용하지 않는다**: banik2022 (미출판) · fan2026 (원고 초안) · cao2026 NEB 값 · kim2026_li_argyrodite_sei (SSRN) · Munsif 2023 E = 67 GPa (우리 E_VRH 옆 금지) · Barai 2021 · Haruyama 2014 · Okuno 2020 을 W_ad 0.8 J/m² 근거로 (`HZ-wad-0p8-misattributed` BLOCKED) · Chaney 2024 · Wang 2022 를 우리 음극 반응 방향 근거로 (`HZ-anode-b2o3-reaction-direction` BLOCKED).

## 7. 사용자가 정할 것

1. 세미나 날짜 — 10-21 전/후에 따라 11장 내용이 갈린다.
2. 9장 새 ESW 그림을 만들지 (권고: 만든다 · 하우스 스타일 + Origin CSV · 정정 창 원장에서만).
3. 탄성 modelc_2x 게이트: 닫기 / 개정 — 12장 '역학' 줄에 들어간다.
4. §4-1 판정 범주별 다음 일 초안 — v7 판정 **전에** 확정 (결정 원장 등록).
5. 덱을 이 구성으로 실제로 만들지 (원본 덱 편집 · 랩 템플릿 유지). → 만들었다 (19장 · 10-12).
6. (10-12 추가) AlI₃ 순위 2 사용 여부 · As₂S₃ 하류 전파 · S3 순위 여유 δ · #7 실행 범위 — 전부 결과 전에.

## 8. 이 문서가 못 하는 것

- **판정이 아니다.** 구성·방향은 제안이고 비준된 결정이 없다.
- 문헌 역할은 **digest 기준**이다. 그림을 직접 본 것은 **Sundar 2025 Fig. 2 · Jung 2026 Fig. 5** 둘뿐이다 — 나머지 그림 속 수치를 슬라이드에 옮기려면 그 그림을 먼저 본다.
- 덱 판정은 원장 대조 (서브에이전트 · 핵심 수치는 원본 파일로 재확인: 강등 기록 · 결정 상태 · B₀ · 호스트 창 · 신호/잡음 비 · 재앵커 · v7 장부) 다. 이야기 문서 줄 번호 인용은 재확인하지 않았다.
  ⚠ 첫 판의 '89/91' 은 낡은 집계표(`cascade_pool_accounting.csv`)만 보고 재실행 원장을 안 봤다 — 10-12 에 `cascade_all_302_2026_08_25.csv` 로 다시 셌다 (91).
- 끝 어림 ≈ 10-21 은 kgy 단독 기준이다 — GPU 공유면 늦어진다.
- 덱 겹침 진단은 좌표 기준이다 — 실제 줄바꿈은 PowerPoint 글꼴에 달렸다.
