# 끝 보고 — kasemchainan2019_critical_stripping_current_dendrite_on_plating (배치 2026-11-24b · #10)

- digest: `litdb/papers/kasemchainan2019_critical_stripping_current_dendrite_on_plating.md` (새 파일 · 503 줄 · 한국어 standalone · §0–§17 + Post-processing 표 · 머리 태그 `elements: Li, P, S, Cl, Na` · `methods: XPS`)
- 그림: `litdb/figures/kasemchainan2019_critical_stripping_current_dendrite_on_plating/` — 크롭 13 장 (본문 6 + SI 7). 도구 그대로 6 장 · 손작업 7 장 (`Fig. 4` 손 크롭 + 다시 자름 6 장 — (f) 표). `figures.json` 에 `recrop` · `manual_crop` 사유 · `auto_bbox` · `viewed` · `viewed_how` 를 달았고, 번호 공백 `f4` 는 `missing_labels` 에 resolved 로 남겼어요. 캡션은 추출에서 빠진 기호 둘만 되살렸어요 (S1 별표 · S7 의 Symbol 글꼴 β — `caption_raw` 보존).
- 판독 · 산수 CSV: `digitized.csv` (49 행 · 그림 판독값 + 우리 산수 · 열 이름 명시).
- 입력 PDF 해시: batch.json 10 번과 둘 다 일치 (본문 `62cc0e91…` · SI `eb2595f7…`).
- 점검 (읽기만):
  · `build_index.py --check` → 이 slug 는 "어느 인덱스에도 없음 [dft]" + "comparison_vs_ours 미편입" 두 줄만 걸려요 ((a) · (b) 를 합치면 풀려요) · 표 칸 수 점검 걸림 없음.
  · `extract_figures.py --inbox --only kasemchainan2019` (매칭표만) → 본문 + SI 자동 매칭 `[제목 100%]` → pdf_map 줄 필요 없음.
  · 웹앱: `/paper/<slug>` 200 · `paper_figures` 13 · `paper_figure_notes` 13/13 (전부 Figure set 표에서) · `_paper_pis` = [] · 원소 페이지 Li · Na · Cl · S · P 에 붙음 ✓ · 기법 페이지는 XPS 가 용어 사전에 항목이 없어 안 붙어요.
  · 시험: `test_v3_literature` + `test_v3_markdown` **43/43 통과** · `test_webapp -k "sakamoto or litdb_figure or recent_digests or digest_date or element_papers or glossary_papers or figure_comment"` **7 통과 · 1 실패** = `test_recent_digests_are_on_every_litdb_surface` (INDEX · comparison 미편입 — 이 배치 다른 편들과 같은 사유 · 합치면 풀려요).
  · 화면: 임시 서버 (포트 5197) 를 띄워 헤드리스 크롬으로 **데스크톱 1440 px · 폰 390 px** 두 장을 찍어 직접 봤어요 — 목차 · 제목 · 저자 · `Fig. N` 자동 링크 · 표가 정상이에요. 못 본 것: 오른쪽 여백 그림 팝업 · 주석 클릭 점프 (상호작용은 안 눌러 봤어요). 서버는 제가 띄운 PID 셋만 골라서 껐어요.
- 공유 파일 · git: 공유 파일은 손 안 댔어요. 단 `litdb/figures/_sources.json` 은 추출 도구가 이 slug 항목을 더해 다시 썼고, 메인 checkpoint 커밋 (`5e5d9165` · `31cae0a5` · `c62c3c65`) 에 이미 들어가 있어요. 제 git 작업은 0 이에요 (status · log 읽기만). 지금 상태: `figures.json` 수정 (viewed · 사유 · 캡션) · digest 미추적.
- 발견 검색: Crossref REST 주제어 검색 4 번 (2025-01-01 이후 · 일반 UA · 개인정보 없음) + DOI 확인 8 번 + 제목 확인 1 번 (Spencer Jolly 2021). 논문 본문 · 출판사 페이지는 안 열었어요.

⚠ **메인에 알릴 것**
1. **이 논문의 CCS 숫자는 두 벌이에요.** 초록 · 서론 (p.1105) 의 *"0.2 and 1.0 mA cm⁻² at 3 and 7 MPa"* 는 100 사이클을 돈 '안전 값' 이고, 본문 2 전극 절 (p.1109) 은 *"the CCS thresholds of 1.0 mA cm⁻² at 3 MPa and 2.0 mA cm⁻² at 7 MPa"* 라고 '처음 실패한 값' 을 같은 이름으로 불러요. 문턱은 그 사이 (3 MPa 0.2–1.0 · 7 MPa 1.0–2.0) 고, CCP 도 2.0–3.0 이에요. litdb 의 2 차 인용 셋 (yang2021_flat · liang2026 · deysher2022) 은 안전 값을 맞게 옮겼어요. 보고서에 넣을 때는 둘을 같이 써 주세요.
2. **'크리프가 확산보다 지배' 는 압력 의존 하나로 내린 판정이에요** — 세 유속 어느 것도 값이 없어요. 논문 숫자로 계산하면 겉보기 압력 지수가 0.8–1.9 (괄호 끝끼리 ≤ 2.7) 로, 벌크 크리프 지수 6.56 이 주는 ×259 와 차수가 달라요. wang2019 (LLZO) 의 겉보기 ≈1 과 '모양' 이 같아요.
3. **`seymour2021_…` digest 가 ref 28 (= 이 논문) 에 단 귀속 두 곳을 원문에서 확인해 주세요** (그 digest 53 · 203 · 293 · 533 행): '~1 mA cm⁻² 에 ~10 MPa 필요' 는 이 논문 값이 아니고 (7 MPa 에서 1.0 이 100 사이클 돌았어요), 'Li/LLZO 에서 큰 압력 없이 공극' 의 근거로도 안 맞아요 (이 논문은 LPSCl · LLZO 실험 0). 남의 digest 라 안 고쳤어요.
4. **'카드 없음' 이라 적힌 자리 셋** — `wang2019_…` digest 38 행 · `comparison_vs_ours_DEM.md` I-15 (5857 행) · `cronau2022_wet_milling_particle_size_ionic_conductivity` digest 76 행. 이제 카드가 있으니 링크로 바꿀지 정해 주세요.
5. **이 논문 서론의 *"LLZO … as low as 0.6 mA cm⁻² (refs 6, 13–15)"*** — ref 14 가 litdb `sharafi2017_…` 인데 거기 CCD 는 0.3 이에요. '0.6' 을 하한으로 인용하지 마세요.
6. **논문 자체 오기** (digest §10-⑪ · ⑫ · ⑮): `Fig. S5` 제목 '4 MPa' (범례 · 본문은 0.5 MPa) · `Fig. S6` 캡션의 'Fig. 7' (본문 `Fig. 6`) · Methods C 기준 '384.8 eV' (✎ 284.8 의 오타로 보임) · 본문 'phosphorus, sulfur and lithium XPS' 대 SI 의 P · S · Cl · Li 항복 0.81 MPa 를 같은 쪽에서 ref 36 · ref 38 로 다르게 인용.
7. **기록 안 된 휴지**: `Fig. S4` 에 반주기 사이 0 mV 구간이 figure-read ≈0.45 h 있어요 (Methods 무언급). shi2026 이 영전류 유지가 CCD 를 올린다고 했으니 CCS 를 비교할 때 걸리는 변수예요.
8. 웹앱 참고: `/paper/<slug>` 맨 위 `<!-- … -->` 주석이 글자로 보여요 — wang2019 · baer2026 도 같아서 이 digest 문제가 아니라 공통 동작이에요.

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🌱 Li 금속 음극 — 공극 · 점착 · 핵생성 · 적층압 · Ag/C 인터레이어 (2026-11-24 · 18 편 한 묶음)` — 행 순서상 **'공극 · 적층압 실험' 묶음의 `wang2019_li_se_interface_dynamics_stack_pressure_current_density` 행 바로 다음** (같은 질문 · 가넷 대 아지로다이트). Jeff Sakamoto 공저가 아니라서 🏷 는 안 달아요. 절 머리의 '18 편' 은 이 배치를 합치면 같이 고쳐야 할 거예요.

| `papers/kasemchainan2019_critical_stripping_current_dendrite_on_plating.md` **(본문 8 pp + SI 8 pp · 크롭 13장 (도구 6 + 손 7 = `Fig. 4` 손 크롭 · 다시 자름 `Fig. 1` · `2` · `5` · `6` · `S1` · `S3`) · 12장 실독 + `Fig. S1` 쪽 렌더 · 판독 · 산수 CSV 49행 · 2026-11-24)** | **[외부·exp·⭐⭐ Li \| Li₆PS₅Cl 박리 임계 전류 (CCS) 의 원전 — 박리 공극 → 다음 도금 덴드라이트 · ⚠ CCS 숫자 두 벌 (안전 0.2 / 1.0 · 실패 1.0 / 2.0 mA cm⁻²) · 조건당 셀 1 · 점착 정량 없음]** ✅ Jitti Kasemchainan · Stefanie Zekoll · Dominic Spencer Jolly · Ziyang Ning · Gareth O. Hartley · James Marrow · **Peter G. Bruce\*** (Oxford · Faraday Institution), "**Critical stripping current leads to dendrite formation on plating in lithium anode solid electrolyte cells**" (***Nat. Mater.* 18, 1105–1111 (2019)**, DOI `10.1038/s41563-019-0438-9`). 3 전극 (WE · CE · 같은 면 옆 RE) Li \| Li₆PS₅Cl \| Li · 스프링 클램프 0.5 / 3 / 7 MPa · 반주기 1 mAh cm⁻² (≈5 µm): **3 MPa 안전 0.2 · 실패 1.0 / 7 MPa 안전 1.0 · 실패 2.0 mA cm⁻²** (초록은 안전 값을, 본문 2 전극 절은 실패 값을 'CCS' 로 부름) · **CCP 2.0–3.0 (두 압력 같음)** · 3 MPa · 1.0 3 전극: 도금 12 mV 평탄 대 박리 끝 19 → 130 mV (7 번째) · 8 번째 단락 · SEM 6 번째 박리 계면 틈 · 7 번째 도금 Li 안 갇힌 공극 (figure-read ≈20–28 × 7 µm) · XCT 계면 흰 화소 증가 · 기전 = 삼중점 옆 Li 막이 공극을 가둠 → 누적 → 국부 전류 ↑ → 도금 덴드라이트 · 0.5 MPa (< 항복 0.81) 셀 형성조차 어려움 · XPS 250 h Li₂S 우세 + Li₃P · 'creep rather than diffusion' 은 압력 의존 하나 — ✎ 겉보기 압력 지수 0.8–1.9 ≪ 벌크 크리프 6.56 · 펠릿 밀도 · 두께 · σ · 운전 온도 · 압력 기준 면적 미기재 · 반주기 사이 0 mV 휴지 ≈0.45 h (`Fig. S4` · Methods 무언급) | 점착 트랙 (인접 · 점착 정량 없음) · W_ad 보고서 8-1 · 8-4 · 연속체 · DEM 대조 표적 (✎ Li 공급 속도 괄호 3 MPa 0.27–1.35 · 7 MPa 1.35–2.69 nm s⁻¹) |

---

## (b) comparison 에 넣을 줄

**A–D 물성 4축: 자리가 없어요** (실험 · 음극 계면 · 계산 0). 방법 원전도 아니라서 §J 블록도 안 만들었어요.

### b-1. `comparison_vs_ours.md` `📑 Reference key` 표에 한 행 (4 칸: 약칭 | 논문 | digest/status | 유형)

| **[Kasem19CSC]** ⭐⭐ **Li\|Li₆PS₅Cl 박리 임계 전류 (CCS) < 도금 임계 전류 (CCP) — 박리 공극이 다음 도금의 덴드라이트를 부른다 · 3 / 7 MPa** · ⚠ **CCS 숫자 두 벌 (안전 값 0.2 / 1.0 · 실패 값 1.0 / 2.0 mA cm⁻²)** · ⛔ **exp — A–D 물성 4축 진입 금지 (§E 행만)** | Jitti Kasemchainan/Stefanie Zekoll/Dominic Spencer Jolly/Ziyang Ning/Gareth O. Hartley/James Marrow/**Peter G. Bruce\*** (Oxford) ***Nat. Mater.* 18, 1105–1111 (2019)** (DOI 10.1038/s41563-019-0438-9) — "Critical stripping current leads to dendrite formation on plating in lithium anode solid electrolyte cells" | ✅ `papers/kasemchainan2019_critical_stripping_current_dendrite_on_plating.md` — 판정은 §E 1 행 + `comparison_vs_ours_DEM.md` §I 블록 | exp (3 전극 전기화학 · SEM · in situ XCT · EIS · XPS) · 계산 0 |

### b-2. `comparison_vs_ours.md` §E 표에 한 행 (4 칸: 주장 | 출처 | 우리 | 일치)

| **🆕 (2026-11-24) Li₆PS₅Cl\|Li 에서는 박리 쪽이 먼저 막힌다 — CCS < CCP · CCS 위에서 벗기면 Li 쪽 공극이 쌓이고 (도금이 삼중점 옆 Li 막으로 공극을 가두며 일부만 메움) 국부 전류가 올라 다음 도금에서 덴드라이트 · 단락 · 3 MPa 안전 0.2 · 실패 1.0 / 7 MPa 안전 1.0 · 실패 2.0 mA cm⁻² · CCP 2.0–3.0 (압력 무관) · XPS 250 h Li₂S 우세 + Li₃P** — ⚠ CCS 숫자 두 벌 (초록 = 안전 값 · 본문 2 전극 절 = 실패 값) · 조건당 셀 1 · 판정 기준 정성 · 'creep 지배' 는 압력 의존 하나 (✎ 겉보기 지수 0.8–1.9 ≪ 6.56) | **[Kasem19CSC]** `Fig. 1b–d` · `Fig. 2` · `Fig. 3` · `Fig. 4` · `Fig. 5` · `Fig. 6` · `Fig. S3` · `Fig. S5` (3 전극 · 스프링 클램프 · 반주기 1 mAh cm⁻² · 운전 온도 미기재) | 우리 §E 는 환원 화학 (산물 · SEI) 축만 — 박리 역학 축 없음 · 0 V 산물 반응식은 **BLOCKED** (`HZ-anode-b2o3-reaction-direction`) · Li 금속 W_ad 는 보고서 7 절 제안 (값은 위치만) | ✅ 산물 방향 (Li₂S + Li₃P) 은 문헌 쪽과 같다 — 우리 반응식 방향 오류 재확인 (새 판정 아님 · XPS 독립 측정 하나 더 · 원장의 '두 방법' 셈은 그대로) · 🔀 [Wang19SP] (LLZO · 같은 질문 · 겉보기 지수 ≈1) 와는 방향 · 모양만 같이 — 숫자 이식 금지 · ⛔ CCS 숫자를 압력 · 정의 없이 인용 금지 |

### b-3. (권장 · 점착 트랙의 실제 집) `comparison_vs_ours_DEM.md` §I 끝에 블록 (번호는 메인이 정해 주세요 — 지금 정본 끝은 I-22 · 이 배치 다른 편도 번호를 제안했을 거예요)

### I-??. `kasemchainan2019_critical_stripping_current_dendrite_on_plating` — ★★ (인접 축 · 점착 정량 없음 · LPSCl) **Li\|Li₆PS₅Cl 박리 임계 전류 (CCS) 의 원전 — 박리 공극 → 다음 도금 덴드라이트 · 압력이 CCS 를 올린다** — ⚠ 접촉 면적 · 공극 분율 · 압력 이력이 숫자로 없어서 DEM 과 같은 눈금에 못 놓는다

> **무엇을 주나.** Li \| Li₆PS₅Cl \| Li 3 전극 (*Nat. Mater.*, 18, 1105 (2019)) · ⌀2 mm × 40 µm Li · ⌀5 mm 소결 펠릿 · 스프링 클램프 0.5 / 3 / 7 MPa · 반주기 1 mAh cm⁻². 3 MPa 안전 0.2 · 실패 1.0 / 7 MPa 안전 1.0 · 실패 2.0 mA cm⁻² · CCP 2.0–3.0 (두 압력 같음) · 0.5 MPa (< 항복 0.81) 는 셀 형성부터 어렵고 빨리 실패. 기전 도식 (`Fig. 4`): 박리 공극 → 삼중점 옆 Li 막이 공극을 가둠 → 다음 박리에서 다시 드러나 커짐 → 국부 전류 ↑ → 도금 덴드라이트.
>
> **★ DEM · 연속체 쪽에 닿는 곳.**
> ① **같은 눈금에 못 놓는 이유 여섯**: 접촉 면적 · 공극 분율 정량 0 (SEM 한 장 · XCT 2D 셋) · 압력은 조립 때 명목값 (운전 중 기록 없음 · 기준 면적 Li ⌀2 mm 대 SE ⌀5 mm 미기재 = 6.25 배) · 공극이 SE 입자 사이가 아니라 Li 금속 안 평면 계면이고 메우는 것이 시간 의존 Li 유동 (DEM 접촉 법칙에 없음) · 벌크 크리프 법칙에 명목 압력을 넣으면 ε̇ 10–10³ s⁻¹ 로 터짐 (유효 응력 ≠ 적층압) · SE 펠릿 밀도 · 거칠기 · 두께 미기재 · 휴지 · 온도 미기재.
> ② **쓸 수 있는 변환 (✎ · 대조 표적)**: CCS 괄호 → Li 공급 속도 괄호 3 MPa 0.27–1.35 · 7 MPa 1.35–2.69 nm s⁻¹ (v = jV_m/F) · 국부 전류 = 전체 전류 / 접촉 분율 (논문 p.1110 · 막힘층 없음 가정) · 겉보기 압력 지수 0.8–1.9 — 모형이 n 6.56 + 명목 압력으로 이 의존을 못 맞춰도 모형 실패로 읽지 않는다 (I-15 wang2019 와 같은 결론).
> ③ **압력 창**: 0.5 MPa 실패 · 3–7 MPa 에서 CCS 상승 · 25 MPa 이상은 Li 가 SE 기공으로 크리프해 단락 (`doux2020_stack_pressure_assb` · 펠릿 87 %) — 상한은 SE 기공률 (DEM 출력) 이 정한다 [우리 해석 · 두 논문 연결].
> ④ **점착**: 이 논문은 재지 않았고 결론에서 '표면 화학 · 미세구조 · 점착 · 기계 물성' 을 CCS 의 다음 변수로만 든다 (p.1110). W 와 잇는 쪽은 CCS (박리) 지 CCP (도금) 가 아니다.
>
> **⛔ 인용 금지 / 한정어**
> · CCS 를 숫자 하나로 인용 금지 — 압력 + '안전 값 / 실패 값' 을 같이.
> · 조건당 셀 1 · 오차 없음 · 판정 기준 정성 · 운전 온도 미기재 · 'creep 지배' 는 저자 해석.
> · LPSCl 값 — LLZO (I-14 · I-15 · I-17 · I-18) · Na (이 논문 `Fig. S7`) 와 섞지 않는다.
> · 우리 W 와 같은 줄 금지 (이 논문에 W 가 없다).
> 상세: digest §3b · §3h · §7c · §7d · §10.

---

## (c) `pdf_map.tsv`

**필요 없어요.** `python3 tools/litdb/extract_figures.py --inbox --only kasemchainan2019` (매칭표만) → `kasemchainan2019_critical_stripping_current_dendrite_on_plating [제목 100%]` · 본문 `kasemchainan2019_critical_stripping_current_main.pdf` + SI `kasemchainan2019_critical_stripping_current_SI.pdf` 둘 다 자동으로 붙어요.

---

## (d) 추가로 먹일 만한 논문 (≤ 8 · 최근 먼저) — Crossref 메타로 서지 확인 · 본문은 안 봤어요

| # | 논문 | 왜 | litdb · 목록 |
|---|---|---|---|
| 1 | Neudecker, Mauersberger & Jossen · *J. Electrochem. Soc.* 173, 220508 (2026) — "Modeling Current Constriction at the Lithium Anode Interface in Solid-State Battery Cells" · DOI 10.1149/1945-7111/aebfc9 | 이 논문이 '없다고 가정한' 전류 수축 — DEM 접촉 분율 → 국부 전류 변환의 모델 쪽 | litdb 없음 · 목록 없음 |
| 2 | Banerjee, Vishnugopi, Lin & Mukherjee · *Adv. Sci.* e78028 (2026 · 온라인 2026-09-30 · 권 미정) — "Mechanistic Insights Into Instability From Single Void Dynamics at the Lithium Metal‐Solid Electrolyte Interface" · DOI 10.1002/advs.78028 | 공극 하나의 성장 · 닫힘 동역학 — 연속체 공극 모델 대조 | 없음 · 없음 |
| 3 | Banerjee, Vishnugopi & Mukherjee · *Adv. Sci.* 13, e15827 (2026 · 온라인 2025-11-23) — "Probing the Impact of Vacancy Diffusion on Void Dynamics at the Lithium Metal–Solid Electrolyte Interface" · DOI 10.1002/advs.202515827 | 이 논문이 정량 안 한 '확산 쪽' — 크리프 대 확산을 숫자로 | 없음 · 없음 |
| 4 | Duan, Feng, Lin, Ye, Li, Wen, Chen & Wei · *Adv. Sci.* 13, e17361 (2026 · 온라인 2025-11-16) — "Thickness‐Dependent Creep in Lithium Layers of All‐Solid‐State Batteries under Stack Pressures" · DOI 10.1002/advs.202517361 | 40 µm 박의 크리프는 벌크와 다르다 — 이 digest §3h 의 '유효 응력 ≠ 적층압' 을 실험으로 | 없음 · 없음 |
| 5 | Kravchyk, Klimpel & Kovalenko · *Matter* 8, 102376 (2025) — "Critical current density measurements of Li/solid-state electrolyte anodes: Time for a rethink" · DOI 10.1016/j.matt.2025.102376 | CCD · CCS 측정 정의 · 프로토콜 — 이 논문의 '두 벌 CCS' · 정성 판정 문제 | 없음 · 없음 |
| 6 | Qu, Huang, Chen, Fu, Chang, Li, Gao & Lin · *ACS Appl. Mater. Interfaces* (2025 · acsami.5c10071 · 권 · 쪽 미확인) — "How Stacking Pressure and Temperature Regulate Lithium Plating and Stripping in Solid-State Lithium Metal Batteries" · DOI 10.1021/acsami.5c10071 | 압력 × 온도 — 크리프 대 확산을 온도로 가르는 쪽 | 없음 · 없음 |
| 7 | Li G., Zhang, Tang, Liu, Xie, Yu, Hui, Deng, Lu, Kim, Huang & Xu Z. · *Adv. Mater.* 37, 2417770 (2025) — "Decoding Chemo‐Mechanical Failure Mechanisms of Solid‐State Lithium Metal Battery Under Low Stack Pressure via Optical Fiber Sensors" · DOI 10.1002/adma.202417770 | 운전 중 압력 · 변형 측정 — 이 논문의 '압력은 조립 때 한 번' 빈칸 | 없음 · 없음 |
| 8 | Spencer Jolly, Ning, Hartley, Liu, Melvin, Adamson, Marrow & Bruce · *ACS Appl. Mater. Interfaces* 13, 22708 (2021) — "Temperature Dependence of Lithium Anode Voiding in Argyrodite Solid-State Batteries" · DOI 10.1021/acsami.1c06706 | **같은 그룹 직계 후속** — 이 논문 결론 (크리프) 을 온도로 시험한 쪽 (2021 이라 2 년 창 밖이지만 결정적 시험이라 넣었어요) | 없음 · 없음 |

**목록에 있음** (`litdb/_curation/batch_2026_11_24/extra_papers_2026_11_24.md` — 다시 안 넣음): Roach 2025 *Eur. J. Mech. A/Solids* 113, 105710 · Li K. 2025 *ACS AMI* 17, 3146 · Haslam 2025 *Adv. Energy Mater.* 15, 2403614 · Ning 2021 *Nat. Mater.* 20, 1121 · Ning 2023 *Nature* 618, 287 · Krauskopf 2019 *ACS AMI* 11, 14463 (이 논문 ref 26) · Spencer Jolly 2020 *ACS AMI* 12, 678 (이 논문이 예고한 Na 후속) · Lewis 2021 *Nat. Mater.* 20, 503.
그 밖 (≤ 2024 · 목록 없음 · 8 편 밖): 이 논문 ref 36 Wang, Wolfenstine & Sakamoto 2019 *Electrochim. Acta* 296, 842 (Li|LLZO flux balance — '공급 = 확산 + 크리프' 틀의 원전 · 🏷 Jeff Sakamoto 공저) · Oh J. 2026 *Batteries & Supercaps* 9, e70514 ("Low Stack Pressure Anode Interfaces in Sulfide‐Based All‐Solid‐State Batteries With Lithium Plating" · DOI 10.1002/batt.70514).

---

## (e) DEM-DFT 보고서 (W_ad 보고서) 에 쓸 거리

보고서 `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` 의 8-1 · 8-4 를 먼저 읽고 맞췄어요. 아래 문장은 보고서 꼴 (짧은 평서문 · 랩 인용 꼴) 이고 내부 사정은 안 넣었어요. '봤나' = 그 근거를 제가 직접 봤는지 (그림 = 크롭을 열어 봄 · 글자 = PDF 본문).

| # | 보고서 자리 | 넣을 문장 후보 | 근거 (쪽 · 그림) | 봤나 |
|---|---|---|---|---|
| 1 | 8-1 끝에 한 문단 | 실제 셀에서 '공극을 막는다' 문턱이 드러나는 쪽은 박리다. Li\|Li₆PS₅Cl\|Li 3 전극 셀에서 박리 쪽 임계 전류가 도금 쪽보다 낮았고, 그 위에서 벗기면 Li 쪽에 공극이 쌓여 다음 도금에서 덴드라이트로 단락됐다 (Nat. Mater., 18, 1105 (2019)). 이 논문은 점착을 재지 않았고, 표면 화학 · 점착 · 기계 물성을 박리 임계 전류의 다음 변수로 들었다. | p.1108 (Two critical currents) · p.1110 (결론) · `Fig. 1b` · `Fig. 4` · `Fig. 5` | 그림 · 글자 다 봄 |
| 2 | 8-4 '필요한 적층압은 전류와 함께 커진다' 문단 뒤 | LPSCl\|Li 셀에서도 같았다. 3 MPa 에서는 0.2 mA/cm² 로 100 사이클을 돌았지만 1.0 mA/cm² 에서 단락됐고, 7 MPa 에서는 1.0 mA/cm² 로 100 사이클을 돌고 2.0 mA/cm² 에서 단락됐다. 도금 쪽 한계 (2.0 mA/cm² 는 버티고 3.0 에서 덴드라이트 신호) 는 두 압력에서 같았다 (Nat. Mater., 18, 1105 (2019)). 조건마다 셀 하나라 대조 표적으로만 쓴다. | p.1105 · p.1108 · p.1109 · `Fig. 5` · `Fig. 6` | 봄 |
| 3 | 8-4 첫 문단 ('Li 금속은 적층압 아래에서 늘 흐른다') 끝 | 항복 응력보다 높은 3 · 7 MPa 에서도 계면에 공극이 생겼고, 항복 아래인 0.5 MPa 에서는 셀을 만들기도 어려웠다 (Nat. Mater., 18, 1105 (2019)). | p.1108 · `Fig. S5` | 봄 |
| 4 | 8-4 '공극을 다시 메우는 것은 속도 문제다' 문단 끝 | 적층압을 3 → 7 MPa (2.3 배) 로 올리자 박리 쪽 한계는 2–5 배 올랐다. 벌크 Li 의 크리프 지수 (6.56) 대로라면 수백 배여야 한다 — 계면으로 Li 를 대는 속도는 명목 적층압과 벌크 크리프 법칙만으로 정해지지 않는다 (두 논문의 숫자로 계산 · Nat. Mater., 18, 1105 (2019) · J. Mater. Sci., 54, 2585 (2019)). | p.1105 · p.1109 · `Fig. 5c,d` · masias2019 n 6.56 | 봄 (계산은 우리 산수 — digest §3h) |
| 5 | 8-4 '연속체 공극 모델이 W 를 받는 자리' 문단 앞 | 공극이 생기는 기준은 전체 전류가 아니라 접촉한 곳의 국부 전류다. 막힘층이 없으면 둘이 같고, 접촉이 줄면 같은 전체 전류에서도 국부 전류가 오른다 (Nat. Mater., 18, 1105 (2019)) — DEM 의 접촉 분율이 들어갈 자리다. | p.1110 (Critical current or potential) | 글자 봄 |
| 6 | 8-6 (가져오지 않는 것) 에 한 줄 | 이 논문의 박리 임계 전류는 두 벌로 쓰였다 (100 사이클을 돈 값 0.2 / 1.0 · 처음 실패한 값 1.0 / 2.0 mA/cm²) — 한 숫자만 떼어 '임계값' 으로 옮기지 않는다. '확산이 아니라 크리프가 Li 를 댄다' 는 압력 의존만으로 내린 해석이라 확정 사실로 옮기지 않는다. | p.1105 · p.1109 | 글자 봄 |
| 7 | 8-7 표에 행 | `Nat. Mater., 18, 1105 (2019)` \| Li \| Li₆PS₅Cl · 3 전극 · 적층압 0.5 / 3 / 7 MPa \| 8-1 박리 쪽 문턱 · 8-4 압력과 임계 전류 · 국부 전류 | — | — |

- 넣지 않는 게 나은 것: 8-4 균열 문단 — 이 논문의 덴드라이트 판정은 SEM 명암뿐이고 균열 개시 · 전파 관찰이 없어요 (`Fig. 2c` 실독). 압력 단계 문단에는 '실험실 셀 3–7 MPa' 사례로만.
- DEM 쪽 답 (질문 3): **이 논문 숫자만으로는 DEM 접촉 모형과 같은 눈금에 못 놓아요** — 이유 여섯과 변환 셋은 digest §7c (위 b-3 ① ② 와 같음). 보고서에 쓴다면 문장 5 (국부 전류) 와 'Li 공급 속도 괄호 0.27–1.35 / 1.35–2.69 nm s⁻¹ (3 / 7 MPa · 논문 숫자로 계산)' 정도가 안전해요.
- 8 절 머리의 '18 편' · 8-7 표 머릿수는 이 배치를 합치면 같이 고쳐야 해요.

**(e) 문장 후보 10 점 기준표** (점수 · 번호로 답해 주시면 고칠게요)

| 항목 | 10 점이면 |
|---|---|
| 정확성 | 숫자 · 쪽 · 그림이 논문과 일치하고 '안전 값 / 실패 값' 을 구분했다 |
| 범위 한정 | 계 (LPSCl) · 조건 (압력 · 셀 하나) · 해석 (크리프) 의 한정어가 붙어 있다 |
| 출처 꼴 | 랩 인용 꼴 (저널 약칭, 권, 첫 쪽 (연도)) · 계산한 문장은 '논문 숫자로 계산' 을 밝힌다 |
| 읽기 쉬움 | 보고서의 짧은 평서문 · 은어 · 내부 사정이 없다 |

---

## (f) 그림 · 동영상 크롭 요약

동영상은 없어요. 그림 13 장 — `tools/litdb/extract_figures.py --slug … --pdf <본문> <SI> --clean` 한 번 + 손작업 (사유는 `figures.json`).

| 파일 | 원본 쪽 | 만든 법 | 봤나 |
|---|---|---|---|
| `fig_1.png` | 본문 p.2 | 다시 자름 — 자동 상단 (y 66.5) 이 판 라벨 a · b · 'Pressure' 화살표 · 140 mV 눈금을 잘라서 y 50 부터 | 크롭 열어 봄 |
| `fig_2.png` | 본문 p.3 | 다시 자름 — 판 라벨 a 잘림 (위 경계만 y 49.5 로) | 봄 (+ 7 번째 도금 칸 2 배 확대로 공극 크기 잼) |
| `fig_3.png` | 본문 p.3 | 도구 그대로 | 봄 |
| `fig_4.png` | 본문 p.4 | **손 크롭** — 도구가 '영역 없음' 으로 건너뜀 (벡터 도식 · 래스터 0) | 봄 |
| `fig_5.png` | 본문 p.5 | 다시 자름 — 판 라벨 a · b · 60 mV 눈금 · 범례 첫 줄 '1.0 mA cm⁻²' 잘림 | 봄 |
| `fig_6.png` | 본문 p.5 | 다시 자름 — 자동 크롭이 c · d 아래 띠 (y 609–668) 만 남김 → a–d 전체 | 봄 |
| `fig_S1.png` | SI p.2 | 다시 자름 — 위에 이메일 줄 · 'Supplementary Information' 제목이 섞임 → 래스터 경계로 | **크롭은 안 열었어요** (첫 훑기 때 SI 쪽 렌더로만 봄 · 래스터가 크롭 안에 다 든 것은 좌표로 확인) |
| `fig_S2.png` | SI p.3 | 도구 그대로 | 봄 |
| `fig_S3.png` | SI p.4 | 다시 자름 — 자동 크롭이 e · f 한 줄만 (쪽 폭 전체) → a–f 전체 | 봄 |
| `fig_S4.png` | SI p.5 | 도구 그대로 | 봄 (반주기 사이 0 mV 휴지 발견) |
| `fig_S5.png` | SI p.6 | 도구 그대로 | 봄 (+ SEM 칸 따로 잘라 틈 두께 잼) |
| `fig_S6.png` | SI p.7 | 도구 그대로 | 봄 |
| `fig_S7.png` | SI p.8 | 도구 그대로 | 봄 |

- 그림과 본문이 어긋난 곳: `Fig. S5` 제목 '4 MPa' 대 범례 · 본문 0.5 MPa · `Fig. S6` 캡션 'Fig. 7' · 본문 '첫 박리 뒤 일부 공극 (`Fig. 2a`)' 은 그림에서 제가 가려내지 못했어요 · 같은 조건 두 셀 (`Fig. 1b` 대 `Fig. S4`) 의 박리 분극이 두 배쯤 달라요 · `Fig. 5c` 의 0.5 곡선은 저자가 '아래' 로 둔 7 MPa 1.0 곡선과 상대 상승이 비슷한데 3 MPa CCS 는 0.2 로 적혔어요 (판독 오차 큼).
- 그림에서만 읽은 값은 digest 에 `figure-read ≈` 로 표시했고 전부 `digitized.csv` 에 있어요.

---

## (g) Jeff Sakamoto 저자 여부

**저자가 아니에요.** 본문 p.1105 저자 줄과 SI 표지 · p.2 저자 블록 모두 일곱 명이에요 — Jitti Kasemchainan · Stefanie Zekoll · Dominic Spencer Jolly · Ziyang Ning · Gareth O. Hartley · James Marrow · Peter G. Bruce (교신 · Oxford · Faraday Institution). 참고문헌에는 공저자로 네 번 나와요 (refs 13 · 14 Sharafi 2017 두 편 · ref 36 Wang, Wolfenstine & Sakamoto 2019 · ref 38 Masias 2019). digest 머리 35 줄 안에는 그 이름이 없고 (Zeier · Ceder 같은 다른 PI 별칭도 0), 웹앱 `_paper_pis` = [] 라서 배지가 안 붙어요. INDEX 행에도 🏷 를 안 달았어요.
