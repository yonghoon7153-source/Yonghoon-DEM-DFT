<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 이웃 = hersey1975_ordered_mixing_concept.md · kawaguchi2017_dry_coating_parametric_na2so4_model_se.md (같은 날 같은 묶음).
     원문 = 28 쪽 (본문 27 + 참고문헌) · SI 없음.  쪽 표기 = 인쇄 쪽 "p.N" (PDF n 쪽 = p.(39 + n) · PDF 1 쪽 = p.40).
     ⚠ 텍스트 층의 글꼴 대응이 깨져 있다: µ → "m" (예: 텍스트 "1–200 mm" = 인쇄 "1–200 µm"), ( ) → "Ž ." , / → "r", ° → "8", [ ] → "w x" — 수치 · 단위는 전부 렌더 (170–200 dpi) 로 대조했다 (§원문 대조 기록).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 숫자 / [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv · 정밀도는 그 머리) /
     [우리 산술] = 인쇄값으로 한 계산 · 이 논문 밖 값과 엮은 계산 (가정 명시) / [추정] = 우리 해석 / [미확인] = 원문에 없음. -->

# 건식 입자 코팅 총설 — 큰 호스트 (1–200 µm) 에 서브마이크론 게스트를 **기계력만으로** 붙이는 다섯 장치 (Mechanofusion · Hybridizer · MAIC · Theta Composer · 회전 유동층) · **정렬 혼합 (Hersey) 의 영구판** · 탈응집 → 부착 → 재분배 세 단계 · 피복률은 게스트가 작을수록 · 자석 **자전** 이 셀수록 높다 · DEM 은 호스트–게스트 크기 차 때문에 **게스트 없이** 호스트 · 자석만 — Pfeffer · Dave · Wei · Ramlakhan (Powder Technology 2001)

> slug `pfeffer2001_dry_particle_coating_engineered_particulates` · DOI `[미확인]` (원문에 DOI 인쇄 없음 · 인쇄 PII S0032-5910(01)00314-X) · type `review + exp + DEM (dry particle coating devices — mechanofusion, hybridizer, magnetically assisted impaction coating, theta composer, rotating fluidized bed; ordered mixing; powder flowability by angle of repose; Walton–Braun latching-spring DEM of hosts and magnets only)` · PDF `008731cb-23._Synthesis_of_engineered_particulates_with_tailored_properties_using_dry_particle_coating.pdf` · digested `2026-10-13` · status ✅
>
> **원제**: *Synthesis of engineered particulates with tailored properties using dry particle coating* (p.40)
> **저자**: Robert Pfeffer\* · Rajesh N. Dave · Dongguang Wei · Michelle Ramlakhan — Particle Technology Center, New Jersey Institute of Technology (NJIT), Newark, NJ, USA (p.40)
> *Powder Technology* **117** (2001) 40–67 · 접수 2000-09-06 · 수정 2000-10-13 · 게재확정 2000-12-15 (p.40) · 지원 = New Jersey Commission on Science and Technology · NSF CTS-9985618 (p.65).
> **판독 원자료**: `litdb/figures/pfeffer2001_dry_particle_coating_engineered_particulates/digitized.csv` (그림 15 개 · 80 행) · 크롭 44 장 (그림 42 · 표 2) `figures.json`.
> **이 카드가 서랍에 들어온 이유**: 우리 논지의 "NCM 에 SE 선코팅" 은 **건식 입자 코팅** 공정의 배터리판이다 — 같은 날 정본 카드 [`hersey1975_ordered_mixing_concept`](hersey1975_ordered_mixing_concept.md) (개념 원전) 와 [`kawaguchi2017_dry_coating_parametric_na2so4_model_se`](kawaguchi2017_dry_coating_parametric_na2so4_model_se.md) · [`nakamura2020_dry_coating_ncm_li3ps4_core_shell`](nakamura2020_dry_coating_ncm_li3ps4_core_shell.md) (배터리 적용 — 그 카드의 ref 26 이 이 논문) 사이를 잇는 **장치 · 기전 총설**.  1저자 읽기 목록 `docs/mixer_coating_reading_list_20261013.md` 의 건식 코팅 축.

> ★★ **한 줄로 왜 중요한가**: (i) "정렬 혼합 = 느슨한 피복, 건식 코팅 = 같은 일의 영구판" 이라는 **두 개념의 연결** 과 'interactive mix' 라는 이름의 출처 (Orr) 를 준다.  (ii) 정렬 혼합이 저절로 일어나는 조건을 **두 성분의 크기가 한두 자릿수 다를 때** 로 적는다 — 우리 SE/AM 크기비는 1/4–1/9 라 **그 조건 밖** 이다.  (iii) 코팅에는 **게스트 응집체를 깨는 강한 충돌 · 전단** 이 먼저 필요하고 (탈응집 → 부착 → 재분배), 장치는 수백–수만 rpm 의 고에너지 기계다 — 우리 믹서 드럼 (Fr ≈ 0.08) 은 **코팅 장치가 아니다**.  (iv) 2001 년 DEM 은 호스트–게스트 크기 차 때문에 **게스트를 넣지 못했다**.
> ⚠ 단 이 논문은 **NJIT 그룹 자체 연구 위주의 총설** 이고, 실험 재료는 유기 (옥수수 전분 · 셀룰로스 · PMMA) · 산화물 (실리카 · 알루미나 · SiC) · 금속 (Mg) — **황화물 SE · NCM 값은 하나도 없다**.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 건식 입자 코팅은 큰 호스트 (1–200 µm) 에 서브마이크론 게스트를 용매 · 바인더 없이 기계력으로 붙이는 공정이고 (반데르발스 힘으로 붙어 있음), 정렬 혼합 (Hersey) 과 같은 현상의 더 영구적인 판이며, 게스트 응집체를 깨는 고에너지 충돌 · 전단 (Mechanofusion 200–1600 rpm · Hybridizer 5000–16,000 rpm · MAIC 자석 자전 · Theta Composer · 회전 유동층) 이 핵심이고, 이산 피복만으로도 유동성이 크게 좋아지지만 (안식각 ↓), 장치 선택과 조건은 아직 시행착오이며 모델 (DEM 포함) 은 호스트와 게스트를 함께 다루지 못한다 [인쇄 p.40–65].

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 정렬 혼합 ↔ 코팅의 관계 · 용어 | "ordered mixing (Hersey 가 만든 말 [13])" = 큰 입자 표면을 작은 입자가 **느슨하게** 덮은 것 · 건식 코팅 = 같은 일인데 **더 강한 물리 (또는 화학) 결합** 으로 영구적 · **Orr [20–22] 는 'regimented' 또는 'interactive' mix 라 불렀다** · 'structured mixing' 이라고도 | [인쇄] p.42 |
| ② 정렬 혼합이 저절로 일어나는 조건 | 두 성분 크기가 **한두 자릿수** 다르면 분리 문제가 사라지고 작은 입자가 큰 입자에 붙는다 (작은 입자의 부착력 > 자기 무게) · 큰 쪽 입도 분포가 **너무 넓지 않아야** 균질도가 좋고 · 아주 넓으면 **'ordered unit segregation'** | [인쇄] p.42 |
| ③ 우리 SE/AM 크기비는? | AM_P 9 µm/SE 1 µm = **9** · AM_S 4/1 = **4** — 이 논문 사례 전부 (호스트/게스트 **50–1000**) 보다 한 자릿수 작다 · 배터리 건식 코팅 실례 (같은 날 카드: NCM 4.7/LPS 0.49 ≈ **9.6** · NCM 5.4/Na₂SO₄ 0.95 ≈ **5.7**) 는 **고에너지 장치 (13,000 rpm 급)** 로 코팅했다 | [우리 산술] · 다른 카드 [인쇄] |
| ④ 코팅에 필요한 단계 · 힘 | 세 단계 (Bannister & Harnby [30]): **(1) 미분 응집체 → 1 차 입자로 탈응집 (2) 운반 입자에 결합 (3) 운반 입자 사이 재분배 · 교환 → 무작위 분포** — 탈응집이 필수 ⇒ 높은 법선 · 전단 충돌이 많은 장치 (고강도 혼합기 · 볼 · 매체 밀) · 거친 입자가 함께 있으면 미분 응집체가 더 잘 깨진다 (호스트가 매체 역할 — Alonso [44] 의 통계 모사) | [인쇄] p.42 |
| ⑤ 우리 믹서 드럼이 코팅을 만들 수 있나? | 이 논문의 장치는 전부 고에너지 (§3-2 표) — 보통의 건식 블렌딩은 **정전기로** 정렬 혼합까지 (Honda 등 [51]) · 충격 블렌딩이어야 미분이 단단히 붙는다 | [인쇄] p.43 · 우리 드럼 Fr ≈ 0.08 (`make_mixer_deck.py`) |
| ⑥ 코팅이 응집 (유동성) 을 바꾸나 | **이산 피복만으로 크게** — PMMA 5 µm + TiO₂ 0.015 µm 10 wt% (Mechanofusion) → 안식각 > 30° → **거의 0** · 옥수수 전분 + 실리카 1 % (MAIC) 59 → 47° · Mei 등 [68] (DEM + 확장 JKR): 코팅된 두 입자의 점착력 ∝ **게스트/호스트 크기비** → 급감 · 게스트 수는 "한 개 이상이면" 거의 무관 | [인쇄] p.45 · p.47 · [판독] Fig 11 |
| ⑦ 피복률은 무엇이 정하나 (MAIC 실험) | 게스트가 작을수록 ↑ (0.05 → 1 µm: **69 → 11 %**, 단층 기준 투입량) · 시간 1 → 5 분 ↑ 뒤 평형 (≈ 60–68 %) · 자석 **자전 속도** 에 비례 (80 → 103 rev/s: 51–54 → 71 %) · **병진 속도엔 무관** (36–60 cm/s: ≈ 68 %) | [판독] Fig 20–24 · [인쇄] p.51–53 |
| ⑧ DEM 은? | Walton 형 **부분 걸쇠 스프링** (적재 K₁ · 제하 K₂ · e = √(K₁/K₂)) + Mindlin–Deresiewicz 단순 접선 · **"호스트와 게스트가 함께 있는 계는 모사가 불가능하다"** → 자석 + 호스트만 (MAIC: PMMA 200 µm 1000 개 + 자석 2.36 mm 10–80 개) · 2D Mechanofusion (호스트만) | [인쇄] p.58–63 |

⛔ **한정어 (떼지 말 것)**: ① **총설 + NJIT 자체 결과** — 다른 연구의 수치는 인용 전달 (원 논문 [미확인]) ② 재료 = 유기 · 산화물 · 금속 — **황화물 SE · NCM 없음** ③ "피복률" 은 SEM 에서 게스트를 **세어** 얻은 % (오차 약 5 %) — 기하 피복률과 정의가 다르다 ④ DEM 은 **게스트 없음** · 2D (Mechanofusion) · 자석 수 ≤ 80 ⑤ 정렬 혼합 조건 (한두 자릿수) 은 **정성 서술** — 문턱값 없음.

---

## 1. 한 줄 요약

**건식 입자 코팅 (dry particle coating) 의 역사 · 장치 다섯 가지 · 응용 · NJIT 의 실험 (MAIC 최적화 · Hybridizer Mg 코팅 · 비활성화 소결 · 회전 유동층) · 모델링 (DEM 포함) 을 정리한 28 쪽 총설.**  핵심 주장: 건식 코팅은 습식 코팅의 친환경 대안 (용매 · 건조 불요) 이지만, 장치별 기전이 달라 아직 **시행착오** 로 조건을 잡고 있으며, 예측 모델이 있어야 장치 선택 · 확대 · 최적화가 된다.

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| R. Pfeffer\* · R.N. Dave · D. Wei · M. Ramlakhan (NJIT 입자기술센터) | *Powder Technol.* 117 (2001) 40–67 | [미확인] (PII S0032-5910(01)00314-X 인쇄) | 호스트: PMMA (5 · 200 µm) · 옥수수 전분 (≈15 µm) · 미결정 셀룰로스 (≈180/40 µm) · Mg (75 µm) · 유리구 (300 µm) · 알루미나–실리카 촉매 담체 (50 µm) / 게스트: TiO₂ 0.015 µm · PTFE 0.1 µm · 실리카 (≈0.3 · 0.7 µm) · 알루미나 (0.05–1 µm) · 왁스 16 µm · SiC 0.5 µm | **총설 + 실험 + DEM** |

> ★ **계보**: 정렬 혼합 = Hersey 와 공동연구자 [13–19] (제약 · 직타정) · Orr [20–22] · Staniforth [23–28] → 건식 코팅 장치 = 일본 (Angmill → Mechanofusion (Hosokawa Micron) · Hybridizer (Nara Machinery) · Theta Composer (Tokuju)) → 미국 (MAIC (Aveka) · NJIT 의 회전 유동층 코터 RFBC) · 레이저 절삭 · 스퍼터링 게스트 생성 [63–65] (p.42–44).
> ★ 같은 날 카드의 배터리 계보: Watano (이 논문 감사의 글의 공동연구자 · ref 12 · 59) → Kawaguchi · Nakamura · **Watano** 2017 (Hybridizer · Na₂SO₄ 모델 SE) → Nakamura 2020 (실제 Li₃PS₄) — [우리 연결 · 저자 이름 일치만 확인].

## 3. 핵심 수치 · 식 (★ 전부 쪽 · 표지 병기)

### 3-1. 개념 · 정의 (§1–2 · p.40–45)
| 항목 | 내용 | 표지 |
|---|---|---|
| 건식 코팅 | 서브마이크론 게스트를 마이크론 호스트에 용매 · 바인더 · 물 없이 직접 · 게스트가 아주 작아 **반데르발스 힘만으로 단단히** 붙는다 | [인쇄] p.40–41 |
| 이산 ↔ 연속 | 공정 시간 · 게스트/호스트 무게비 · 입자 성질에 따라 **이산** 또는 **연속** (입자층 = 단층 · 다층 (다공) / 연속 막 (비다공)) — Fig 1 | [인쇄] p.41 |
| 변형 · 박힘 | 게스트가 변형되거나 호스트 표면에 박히면 **접촉 면적 ↑ → 인력 ↑ → 더 강한 코팅** | [인쇄] p.41 |
| 바뀌는 성질 | 유동성 · 분산성 · 용해도 · 젖음성 · 정전기 · 전기 · 자기 · 광학 · 색 · 맛 · 형상 · 소결성 · 고상 반응성 | [인쇄] p.41 |
| 정렬 혼합 | 크기가 한두 자릿수 다르면 분리 문제가 사라지고 작은 입자가 큰 입자에 붙는다 (부착력 > 자기 무게) — "ordered mixing" (Hersey [13]) · "structured mixing" · Orr: "regimented" · "interactive" mix | [인쇄] p.42 |
| 정렬 ↔ 코팅 | 정렬 혼합 = 느슨한 피복 · 건식 코팅 = 같은 일 + 더 강한 결합 (영구) | [인쇄] p.42 |
| 정렬 혼합의 장점 | 큰 쪽 입도 분포가 너무 넓지 않으면 **균질도가 훨씬 좋고** · 이후 분리에 **더 안정** · 아주 넓으면 **'ordered unit segregation'** [16, 37–40] | [인쇄] p.42 |
| 세 단계 (Bannister & Harnby [30]) | (1) 미분 응집체 → 1 차 입자 (2) 운반 입자에 결합 (3) 운반 입자 사이 재분배 · 교환 → **무작위 분포** — 순서는 섞일 수 있지만 **탈응집은 반드시** | [인쇄] p.42 |
| 거친 입자의 매체 효과 | 미분만 있을 때보다 거친 입자와 함께 밀링할 때 응집체가 더 잘 깨진다 ([18] 추측 → Alonso [44] 통계 모사로 보임) · 호스트 = 매체 | [인쇄] p.42 |
| 보통 블렌딩 ↔ 충격 블렌딩 | 보통 건식 블렌딩 = 미분이 **정전기로** 붙은 정렬 혼합 · 충격 블렌딩 (Hybridizer) = 큰 충격력으로 단단히 붙은 코팅 입자 [48–51] | [인쇄] p.43 |
| 기계화학 | 물리 부착 + 계면 화학반응 = mechanochemistry (Senna [53–56]) | [인쇄] p.43 |
| 코팅 분류 | 깊은 박힘 · 캡슐화 · 막 · 이산 (부분) 피복 · 느슨한 표면 코팅 (= 정렬 혼합) | [인쇄] p.44 |
| 현황 | **시행착오** 로 장치 · 조건 결정 · 거시 모델 거의 없음 | [인쇄] p.44 · p.65 |

### 3-2. ★ 장치 다섯 (§3 · p.45–47 · Fig 3–8)
| 장치 | 원리 | 수치 | 성격 · 표지 |
|---|---|---|---|
| Mechanofusion (Hosokawa) | 회전 외통 + 고정 inner piece + 고정 scraper · 틈에서 강한 전단 · 압축 · 국부 발열로 표면 **융합** · scraper 가 벽 부착을 깸 · 배치 | 외통 **200–1600 rpm** · 틈 = 코팅 두께 조절 | 강한 힘 · [인쇄] p.46 |
| Hybridizer (Nara) | 6 날 고속 회전자 + 고정자 + 재순환 회로 · 고충격 · 분산 → 응집체 파쇄 · 박힘 · 막 · 배치 | 회전자 **5000–16,000 rpm** · 짧은 공정 시간 · 발열 | 강한 힘 · [인쇄] p.46 |
| MAIC (Aveka) | 진동 자기장이 자석 입자 (바륨 페라이트 + 폴리우레탄 피복) 를 흔들어 충돌 · 게스트를 호스트에 박음 (peening) · 연속 운전 가능 | 200 ml 유리병 (NJIT 벤치) · 거시 온도 상승 무시 가능 | 부드러운 코팅 · 유기물 · 열민감 물질 · [인쇄] p.46 |
| 회전 유동층 코터 RFBC (NJIT) | 원심 유동화 · 다공 원통 분산판을 지나는 반경 방향 기류 · 높은 원심 · 전단 → 게스트 응집체 파쇄 · 기포가 혼합 | "100 g" 에서 u_mf 가 보통 "1 g" 유동층보다 **두 자릿수** 큼 · **Geldart C** 도 회전 속도로 유동화 · 연속 운전 가능 | 부드러운 코팅 · [인쇄] p.46–47 |
| Theta Composer (Tokuju) | 느린 타원 용기 + 빠른 타원 회전자 · 좁은 틈에서 전단 · 압축 → 넓은 틈에서 대량 혼합 | 용기 **≈ 30 rpm** · 회전자 **500–3000 rpm** · 틈 **4 mm** (Fig 8 라벨) | 부드러운 코팅 · [인쇄] p.47 · [판독] Fig 8 |

### 3-3. 응용 예 (§4 · p.47–48 — 인용 전달, 원 논문 [미확인])
| 예 | 수치 | 표지 |
|---|---|---|
| PMMA 5 µm + TiO₂ 0.015 µm **10 wt%** (Mechanofusion) | 자유 흐름 · **안식각 거의 0** ↔ 원래 PMMA · TiO₂ 는 > 30° [4] | [인쇄] p.47 |
| 폴리스티렌 수지 10 µm + 카본블랙 (Mechanofusion) | 둥근 모양 · 잘 흐르는 토너 [4] | [인쇄] p.47 |
| **PTFE** 응집체 10 µm (1 차 0.1 µm) + PMMA 5 µm (Mechanofusion) | 개별 PTFE 입자가 PMMA 표면에 고르게 → 응집체 파쇄 · 분산 · PMMA 의 **음 극성 크게 증가** (원래 전기적 중성) [4] | [인쇄] p.47 |
| isoproterenol HCl 미분 5 wt% + 감자 전분 (≈70 µm) + 카나우바 왁스 5 wt% (Hybridizer) | 서방형 [52, 73, 74] · 무기 미분은 박힘 · 고분자 · 금속 미분은 일부 녹아 연속 막 [67] | [인쇄] p.47 |
| 기타 | 화장품 · 토너 · 금속/세라믹 복합 · 용사 · 세라믹 필터 · 고체 윤활 · 전기 접점 · Y 계 초전도 · TiO₂ · SnO₂ 다공 박막 · Cu–Mo 복합 · Si₃N₄ + 알루미나 전구체 · HAP + 지르코니아 · HPLC · 유리 거품 + 티타니아 (기름 유출) · 질소고정균 + 잔디 씨앗 | [인쇄] p.47–48 |

### 3-4. ★ NJIT 실험 — MAIC (§5.1.1–5.1.2 · p.48–53)
**유동성 · 젖음성 (옥수수 전분 ≈15 µm · 미결정 셀룰로스 ≈180/40 µm + 실리카 1 차 ≈0.3 µm 1 wt% — FDA 기준이라 이산 피복만)**
| 양 | 0 분 | 5 분 | 10 분 | 20 분 | 표지 |
|---|---|---|---|---|---|
| 전분 안식각 (°) | 59.0 | 49.1 | 47.7 | 46.7 | [판독] Fig 11 |
| 셀룰로스 안식각 (°) | 49.6 | 39.6 | **37.5** | 43.8 (섬유 파쇄 → 다시 나빠짐) | [판독] Fig 12 · [인쇄] p.48 |
| 셀룰로스 흡수 (600 s 노출, 질량 %) | 62 | 36.5 | **30** | 48 | [판독] Fig 14 |
- 전분 흡수 (본문 "5 분 노출"): 실리카 110 % · 미처리 전분 60 % · 5 분 처리 28 % · 20 분 처리 18 % [인쇄 p.49] — ⚠ 그림 13 과 어긋남 (§10-2).
- 기전: 실리카의 산성 실라놀 + 전분 · 셀룰로스의 OH → 소수성 –O– + 물 (Fig 15) · MAIC 의 부드러운 충돌이 **기계화학** 을 촉진 · FTIR 3100–3650 cm⁻¹ O–H 흡수 감소 (Fig 16 · 17) [인쇄 p.50].
- Theta Composer (일본 그룹 [59], 셀룰로스 + 실리카 1 %): 안식각 **54.2 → 31.3° (8 분 최소)** → 37.8° (10 분 · 섬유 파쇄) · 비표면적 2.71 → 1.95 (8 분) → 2.15 m² g⁻¹ [판독 Fig 18] · 수분 흡수 10 h 에서 8 분 처리가 가장 낮음 (≈ 24.7 vs 물리 혼합 ≈ 29.8 %) [판독 Fig 19].

**MAIC 최적화 (PMMA 200 µm 구형 호스트 + 알루미나 게스트)**
| 변수 | 결과 | 표지 |
|---|---|---|
| 게스트 투입 | **단층 100 % 피복** 을 가정한 양 | [인쇄] p.51 |
| 시간 1 · 3 · 5 · 7 · 10 분 (게스트 0.2 µm) | 35 · 45 · **68.5** · 60 · 63 % — 5 분 뒤 평형 근처에서 출렁 (떨어짐 · 다시 붙음 또는 실험 오차 ≈ 5 %) | [판독] Fig 20 · [인쇄] p.51 |
| 피복률 측정 | SEM 에서 **호스트 표면 게스트를 하나하나 세는** 통계 기법 | [인쇄] p.51 |
| 전류 1–5 A (45 Hz · 5 분) | 최적 **5.0 A** | [인쇄] p.51 |
| 주파수 45–100 Hz | 45 Hz ≈ **66 %** → 70 Hz 까지 감소 → 증가 → **90 Hz 에서 다시 최대** (주기적 요동) | [인쇄] p.51 |
| 자석/분말 질량비 | 비 ↑ → 피복 ↑ · **2 넘으면 거의 그대로 (때로 나빠짐)** [9] | [인쇄] p.52 |
| ★ 게스트 크기 0.05 · 0.2 · 0.4 · 1 µm (투입 0.25 · 1.0 · 2.0 · 5.0 wt%) | 피복 **69 · 51.5 · 27.5 · 11 %** · 0.2 µm 가 0.05 µm 보다 **더 고르게** (0.05 µm 은 응집체가 많이 남음 = MAIC 가 못 깸) | [판독] Fig 21 · [인쇄] p.52 |
| 자석 크기 (≈150 · 800 · 2700 µm) | 42 · 52 · **60 %** — 큰 자석 (관성 · 운동에너지 · 자전 ↑) 이 응집체를 더 잘 깸 | [판독] Fig 22 · [인쇄] p.52 |
| ★ 자석 자전 vs 병진 (고속 카메라) | 자전 79.6–103 rev/s → 피복 51–54 → **71 %** (직선 증가) · 병진 36–60 cm/s → **변화 없음** (≈ 68 %) ⇒ 주 운동 = **자전** (게스트 탈응집 + 호스트 표면에 펴 바름) · 병진은 충격으로 보조 | [판독] Fig 23 · 24 · [인쇄] p.53 |
| 기전 그림 | 자석 들뜸 → 게스트 탈응집 → 호스트 표면 전단 · 펴 바름 → 자석–호스트–호스트 · 자석–호스트–벽 상호작용 → 코팅 입자 (Fig 25) | [인쇄] p.53 |
| 시간 전개 (SEM 연속) | 짧은 시간 = 호스트에 **게스트 덩어리** 가 이산적으로 (게스트가 처음엔 응집 상태) → 긴 시간 = 고른 피복 ⇒ **탈응집 · 재배열 · 코팅이 동시에** | [인쇄] p.59 |

### 3-5. Hybridizer — 마그네슘 (§5.1.3 · p.53–54)
- Mg (75 µm · 조명탄 · 예광탄 · 흡습 → 수소 발생) + 실리카 (0.7 µm) 1–2 % · 왁스 (16 µm) 2–4 % · 배치 20–25 g · **5000–12,000 rpm · 2–4 분** · 22–60 °C (냉각 재킷) [인쇄].
- 점화 성능 = 코팅 전과 같음 · 습도 시험 무게 증가 (96 h): 원 Mg **19.2 %** vs Mg/왁스 (HB) **12.7 %** · 왁스 자체 ≈0.3 % [판독 Fig 28] · 수소압 (반응 시험): 원 Mg ≈300 psi (≈160 h) · 실리카 코팅 ≈190 psi (≈220 h) · 왁스 코팅 ≈105 psi (≈200 h) [판독 Fig 29] · 실리카는 **균열 안까지** 고르게 · BET 감소 (변형된 왁스가 균열 입구를 막음) [인쇄 p.54].

### 3-6. 비활성화 소결 (§5.1.4 · p.54–56 · Table 1–2)
| 시료 (Table 1) | 밀도 (g cm⁻³) | 녹는점 (°C) | 크기 (µm) | 모양 |
|---|---|---|---|---|
| 유리구 | 2.5 | 705 | 300 | 구 · 매끈 · 비다공 |
| 알루미나–실리카 (촉매 담체) | 3.6 | ≈ 2000 | 50 | 불규칙 · 다공 |
| SiC (게스트) | 3.2 | 2700 | 0.5 | 불규칙 |
- 운전 (Table 2): MAIC 유리/SiC 10 분 · 0.8 · 8 wt% · 10 g / 알루미나/SiC 2.5 · 5 · 10 분 · 2 wt% · 10 g · Mechanofusion 유리/SiC 10 분 · 0.8 · 8 wt% · 100 g · Hybridizer 알루미나/SiC 10 분 · 2 wt% · 50 g (유리구는 깨져서 HB 안 씀 · 알루미나는 MF 배치가 커서 안 씀) [인쇄].
- 유리구: 700 °C 에서 미처리는 대부분 융착 · 0.8 · 8 wt% 코팅은 낱개 유지 · 800 °C 에서 0.8 wt% 도 융착 · **8 wt% 만 낱개 (목 성장 약간)** ⇒ 두꺼운 코팅이 소결을 더 늦춘다 [인쇄 p.55].
- 촉매 담체: MAIC 피복 **11 % (2.5 분) · 14 % (5 분) · ≈ 50 % (10 분)** · HB 는 심한 크기 감소 (부피 평균 36.0 → **17.8 µm**, MAIC 10 분 20.2 µm) [인쇄 p.56 · 판독 Fig 32] · 소결 시작 ≈ **1180 → 1320 °C (+140 °C)** (2.5 분 MAIC) [인쇄 p.56 · Fig 33 범례] · 다공 안 소결은 막지 못할 것 [인쇄].

### 3-7. 회전 유동층 코터 (§5.1.5 · p.56–57)
- PMMA 200 µm + 알루미나 0.7 µm [12] · u/u_mf < 2 (기포 적음) = PMMA 날림 거의 없음 · 미분이 큰 입자에 포획 → 정렬 혼합 → 충격 코팅 · u > 2u_mf 면 기포 파열로 게스트가 떨어져 날아감 ⇒ **최적 u = 2u_mf** [인쇄].
- **sticking ratio** = 1 분 초음파 전후 붙어 있는 게스트 질량의 비 · 60 분 뒤 5 · 10 · 15 · 20 · 25 s⁻¹ = **7 · 23 · 38 · 45.5 · 51 %** (회전이 빠를수록 잘 붙음 · 느리면 초음파에 대부분 씻김) [판독 Fig 35 · 인쇄 p.57] · EDX: 20 → 40 → 60 분 피복 증가 · 60 분에 "꽤 고른" 피복 (Fig 36) [인쇄].

### 3-8. ★ 모델링 (§2 · §5.2 · p.45 · p.57–64)
**문헌 모델 (인용 전달)**
- Alonso [41]: 처음엔 미분의 느슨한 응집체가 가까운 호스트에 붙음 (빠름) → 코팅된 호스트와 안 된 호스트의 충돌로 분산 · 재배열 = **2 차 반응 C + N → (k) C + C** [인쇄 p.45].
- Mechanofusion [66]: 입자 = 연속체 · inner piece 작용 영역 · scraper 무시 → 입자에 걸리는 힘 ∝ **각속도²** · 틈이 좁을수록 ↑ (재료 성질 미포함) [인쇄 p.45].
- Hybridizer [51, 67]: 쿨롱 + 런던–반데르발스를 함께 넣은 통계 모사로 단층 형성 부착 에너지 → 입자 크기 · **호스트/게스트 크기비** 효과 (정성) [인쇄 p.45].
- ★ Mei 등 [68]: 움직이는 판–고정 판 사이 분체 흐름 DEM + **코팅 효과를 넣은 확장 JKR** → 미세 코팅이 있는 두 1 차 입자의 점착력은 **코팅 입자/호스트 크기비에 정비례** → 점착력 급감 → 이산 피복만으로 유동성 개선 · 게스트 수는 "한 개 이상" 이면 효과가 작다 [인쇄 p.45].
- Theta Composer DEM [70]: 입자–회전자 상호작용 힘이 중요 · 회전 속도와 **점착 성질** 이 중요 인자 [인쇄 p.45].

**NJIT DEM (p.58–64)**
- 접촉: Walton [105, 106, 116] — **부분 걸쇠 스프링 (partially latching spring)**: 적재 N_l = K₁·α · 제하 N_u = K₂·(α − α₀) · **e = √(K₁/K₂)** (속도 무관 가정) · α₀ = 유한 소성 변형 (식 1–2) · 접선 = Mindlin–Deresiewicz 단순형 K_T = K₀(1 − (T − T\*)/(μN − T\*))^γ (T 증가) · K₀(1 − (T − T\*)/(μN + T\*))^γ (T 감소) · γ ≈ 1/3 · T′ = T + K_T·ΔS (식 3–4 — 인쇄 그대로) [인쇄 p.59].
- 자석: 상수 쌍극자 · 외부장 = 무한 솔레노이드 B = μ₀NI k̂ (I = I₀ sin ωt) · 토크 T = m × B · 쌍극자장 B = μ₀/(4πr⁵)[3(m·r)r − r²m] · 힘 F = (m·∇)B · 회전 J θ̈ = m × B (식 5–10) [인쇄 p.60].
- ★ **"호스트와 게스트가 모두 있는 계는 모사가 불가능하다"** (크기 차 → 입자 수 과다) → 자석만 · 또는 자석 + 제한된 호스트 · 결과는 **통계 모델과 결합** 해야 [인쇄 p.45 · p.60].
- MAIC: 자석 50 개 · 2.5 × 2.5 × 6.0 cm 셀 (중력 퇴적 → 장 인가 0.3 · 0.9 s 에 유동화, Fig 37) · PMMA 200 µm **1000 개** + 자석 2.36 mm **10–80 개**: 호스트–호스트 충돌 (호스트당) 778 → **967 (50 개)** → 668 (80 개) · 벽–호스트 1.36 → 1.41 → 1.17 × 10⁴ · 자석–호스트 50 → 1780 → 2660 (계속 증가) ⇒ 일정 수 넘으면 자석을 더해도 소용없음 · 80 개면 호스트/자석 = **12.5** (실제는 수백만 호스트라 이렇게 낮지 않음) · 확대 = **단위 부피당 자석 수 유지** + 같은 장 세기 [판독 Fig 38 · 인쇄 p.61–63].
- Mechanofusion: **2D** · inner piece = 편심 원통 · scraper = 둥근 입자 여럿 · **호스트만** · scraper 가 있으면 입자를 벽에서 떼어 충돌 수 · 세기 ↑ (없으면 벽에 다져 붙음, Fig 40 · 41) · 법선 힘 inner-piece · scraper 영역 ≈ 1.5–1.6 × 10⁻³ N vs 입력 ≈ 9 × 10⁻⁴ · 자유확산 ≈ 6.5 × 10⁻⁴ N · 접선 ≈ 법선의 1/5 [판독 Fig 42 · 로그 축] · 입자 크기 [미확인 — 원문에 없음].

### 3-9. ★ 우리 산술 — 이 논문 수치로 우리 계를 읽기
| 항목 | 값 | 가정 · 출처 |
|---|---|---|
| MAIC 단층 투입량의 크기 비례 | 0.25/0.05 = 1.0/0.2 = 2.0/0.4 = 5.0/1 = **5.0** → 투입 wt% = **5 × d (µm)** 정확히 비례 | 단층 질량 ∝ d/D (Hersey 식 1) 와 정합 [우리 산술] |
| 그 5 가 함의하는 밀도비 | 식 1 (f = 1) 로 거꾸로: ρ_게스트/ρ_호스트 = 0.05 × 200/4 = **2.5** (식 2 면 2.8) | 원문에 밀도 없음 — 함의값일 뿐 [우리 산술] |
| 이 논문 사례의 호스트/게스트 크기비 | MAIC 200/0.05–1 = **200–4000** · RFBC 200/0.7 ≈ **290** · Mg 75/0.7 ≈ **110** · 유리 300/0.5 = **600** · 촉매 50/0.5 = **100** · 전분 15/0.3 = **50** · PMMA 5/0.015 ≈ **330** · PMMA 5/PTFE 0.1 = **50** | [인쇄] 크기 → [우리 산술] |
| 우리 | AM_P 9/SE 1 = **9** · AM_S 4/1 = **4** (생성기 `D_REAL_UM`) | 이 논문 최소 사례보다 **한 자릿수 이상 작다** |
| 단층에 필요한 SE (식 1 · f = 1) | AM_P 1 g 당 4·ρ_SE·d/(ρ_AM·D) = 4 × 2.0 × 1/(4.8 × 9) = **0.185 g** · AM_S **0.417 g** → 우리 조성 (AM_P 56 · AM_S 24 · SE 18) 에서 필요 20.4 vs 있음 18 = **0.88** | `hersey1975_…` §3-7 과 같은 결론 [우리 산술] |
| 피복률 ÷ 단층 투입 | 같은 "단층 100 %" 투입에서 실제 피복 0.69 · 0.52 · 0.28 · 0.11 → 게스트가 클수록 **투입분 대부분이 단층으로 안 깔린다** (덩어리 · 다층 · 떨어짐) | 피복률 = 단층 대비 면적 분율로 읽을 때 [추정] |

---

## 4. ★ 방법 — 실험 · 모사 · 입자 처리

### 4-1. 실험 측정
- SEM (형상) · EDX (표면 원소 지도) · 안식각 = **고정 바닥 (fixed base)** 법 · 젖음성 = 침투 속도법 [87, 88] · BET · 초음파 견고성 (sticking ratio) · 입도 = API Aerosizer (부피 평균) · FTIR (O–H) · 팽창계 (소결 시작) [인쇄 p.48–56].
- 피복률 = SEM 에서 게스트를 **세는** 통계 기법 (오차 ≈5 %) [인쇄 p.51].

### 4-2. ★ 입자 처리 (DEM)
- **강체 구 + 부분 걸쇠 선형 스프링** (적재 · 제하 강성이 다름 → 반발계수 · 잔류 겹침 α₀ = "유한 소성 변형") — 접촉 소성 (힘 법칙) 이지 입자 **형상** 소성이 아니다.
- 자석 = 상수 쌍극자 · 호스트 = 비자성 구 · **게스트 없음** · Mechanofusion = 2D 원판.
- 점착 · 반데르발스 힘은 **NJIT DEM 에 없다** (본문 식에 없음) — 점착은 Mei 등 [68] · Theta Composer DEM [70] 쪽 (인용).

### 4-3. 기법 미니 용어집
- **호스트 (host · core) / 게스트 (guest · fine)** — 코팅되는 큰 입자 / 붙는 작은 입자.
- **정렬 혼합 (ordered mixing)** — 작은 입자가 큰 입자에 붙어 단위를 이루는 혼합 (Hersey) · **interactive · regimented mix** (Orr) · structured mixing.
- **ordered unit segregation** — 운반 입자 크기 분포가 넓을 때 정렬 단위들끼리 크기로 분리되는 것.
- **Mechanofusion · Hybridizer · MAIC · Theta Composer · RFBC** — §3-2 표.
- **mechanochemistry** — 기계적 응력으로 일어나는 계면 화학반응.
- **비활성화 소결 (deactivated sintering)** — 표면 코팅으로 소결을 늦춰 소결 온도를 올리는 것 (↔ 활성화 소결).
- **sticking ratio** — 초음파 1 분 뒤 남은 게스트 질량 / 그 전.
- **u_mf** — 최소 유동화 속도.
- **부분 걸쇠 스프링** — Walton 형 선형 이력 접촉 (적재 K₁ < 제하 K₂).

---

## 5. Figure set ★ (크롭 44 장 = `litdb/figures/pfeffer2001_dry_particle_coating_engineered_particulates/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 건식 코팅 모식 — 호스트 + 게스트 → 기계력 → 이산 · 연속 (단층 (다공) · 막 (비다공)) | ★ 코팅 형태 분류 — 우리 LC 팔이 가정하는 "SE 껍질" 은 어느 쪽인가 |
| 2 | 정렬 혼합 모식 — 미분 + 큰 입자 → 미분이 붙은 단위 | ★ Hersey 그림의 운반체판 |
| 3 | Mechanofusion 장치 (회전 용기 · arm head · scraper) | 고에너지 장치 예 |
| 4 | Hybridizer 장치 (회전자 · 날 · 고정자 · 재순환관) | 배터리 건식 코팅 장치 (같은 날 kawaguchi2017 · nakamura2020) |
| 5 | MAIC 장치 (코일 · 자석 · 호스트 · 게스트) | 부드러운 코팅 예 |
| 6 | 회전 유동층 코터 | — |
| 7 | 기포 사진 (최소 유동화 위 운전) | — |
| 8 | Theta Composer — 용기 ≈30 rpm · 회전자 ≈500–3000 rpm · 틈 4 mm · 세 방향 | — |
| 9 | 옥수수 전분 SEM (a) 미처리 (b) 5 분 MAIC (c) Si EDX | 이산 실리카 피복의 모습 |
| 10 | 셀룰로스 SEM (a) 미처리 (b) 5 분 (c) 10 분 | 시간에 따른 피복 증가 |
| 11 | 전분 안식각 vs 처리 시간 | ★ 이산 피복 → 안식각 ↓ (D3 정성 근거) |
| 12 | 셀룰로스 안식각 vs 처리 시간 (20 분 반등) | 과처리 = 호스트 파쇄 → 유동성 다시 나빠짐 |
| 13 | 전분 계 흡수 곡선 (a–d) | ⚠ 본문 수치와 어긋남 (§10 항목 2) |
| 14 | 셀룰로스 계 흡수 곡선 (a–d) | — |
| 15 | 기계화학 모식 (실라놀 + OH → –O– + H₂O) | — |
| 16 | 전분 FTIR O–H | — |
| 17 | 셀룰로스 FTIR O–H | — |
| 18 | Theta Composer 셀룰로스 — 안식각 · 비표면적 vs 시간 (8 분 최소) | 최적 공정 시간이 있다 |
| 19 | Theta Composer 셀룰로스 — 수분 흡수 vs 시간 | — |
| 20 | 피복률 vs 처리 시간 (PMMA/알루미나) | ★ 빠른 상승 → 평형 (≈ 60–68 %) — 혼합 지표의 포화형과 같은 모양 |
| 21 | 피복률 vs 게스트 크기 | ★★ 게스트 1 µm = 11 % — 우리 SE 크기의 경고 (§8 항목 3) |
| 22 | 피복률 vs 자석 크기 | 충돌 에너지 ↑ → 피복 ↑ |
| 23 | 피복률 vs 자석 자전 속도 | ★ 피복 = 전단 · 펴 바름 (자전) 이 지배 |
| 24 | 피복률 vs 자석 병진 속도 (평평) | ★ 병진 충돌은 보조 |
| 25 | MAIC 기전 모식 (a–f) | 탈응집 → 펴 바름 → 3 체 상호작용 |
| 26 | 미처리 Mg 표면 SEM | — |
| 27 | Hybridizer Mg + 왁스 2 % (2 분 · 10,000 rpm) SEM | — |
| 28 | Mg 습도 시험 (무게 증가) | — |
| 29 | Mg 반응 시험 (수소압) | — |
| 30 | 유리구 700 °C 광학 사진 (미처리 · 0.8 · 8 wt% SiC) | — |
| 31 | 유리구 800 °C 광학 사진 | 코팅 두께 ↑ = 소결 지연 ↑ |
| 32 | 촉매 담체 부피 평균 입도 (HB 2 분 = 17.8 µm) | ★ 고에너지 장치 = 호스트 파쇄 위험 (NCM 파쇄의 일반판) |
| 33 | 팽창계 신장 vs 온도 (Ts ≈ 1180 · 1320 °C) | — |
| 34 | 1250 °C SEM (미처리 · 2.5 분 MAIC) | — |
| 35 | sticking ratio vs 운전 시간 (회전 5–25 s⁻¹ · u/u_mf = 2) | 부착 강도 ∝ 충돌 세기 |
| 36 | 알루미나 EDX 지도 (20 · 40 · 60 분) | — |
| 37 | MAIC DEM — 자석 50 개 유동화 (0 · 0.3 · 0.9 s) | — |
| 38 | MAIC DEM — 호스트–호스트 · 벽–호스트 · 자석–호스트 충돌 수 vs 자석 수 | 충돌 통계 = 코팅 예측의 입력 (게스트 없이) |
| 39 | Mechanofusion 2D DEM 기하 (영역 1–4) | — |
| 40 | Mechanofusion DEM 입자 배치 시간 전개 (scraper 있음) | — |
| 41 | 같은 (scraper 없음 — 벽에 다져 붙음) | 벽 부착 깨기의 중요성 |
| 42 | 영역별 평균 법선 · 접선 힘 (로그) | inner-piece · scraper 영역이 최대 |
| Table 1 | 호스트 · 게스트 밀도 · 녹는점 · 크기 · 모양 | — |
| Table 2 | MAIC · Mechanofusion · Hybridizer 운전 조건 | — |

## 6. Post-processing ★
- **원문**: SEM 계수 피복률 · 안식각 · 흡수 곡선 · FTIR · 팽창계 · 입도 · DEM 충돌 수 · 영역 평균 힘 — 통계 처리 기술 없음 (오차막대 = 피복률 ±5 % · 안식각 일부).
- **우리 후처리 (이 카드)**: 그림 15 개 손 판독 (digitized.csv) · 단층 투입량 비례 확인 · 크기비 표 · 우리 조성의 단층 SE 량 (§3-9).

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태)

| 항목 | 이 논문 (Pfeffer 2001) | 우리 | 차이 / 판정 |
|---|---|---|---|
| 코팅을 만드는 장치 | 고에너지 (MF 200–1600 rpm · HB 5000–16,000 rpm · MAIC · RFBC "100 g") | LIGGGHTS 드럼 · Fr ≈ 0.08 (밴드 0.055–0.086) — `make_mixer_deck.py` `FR_ANCHOR` | ★ 우리 드럼은 코팅 장치가 아니다 — LC 팔의 "코팅" 은 **입력으로 준 표면 상태** (논지 §2-6) 이지 믹서가 만든 것이 아니다 |
| 크기비 | 호스트/게스트 50–4000 | AM/SE 4–9 | 정렬 혼합이 "저절로" 서는 영역 (한두 자릿수) 밖 [우리 산술] |
| 혼합 단계 | 탈응집 → 부착 → 재분배 (→ 무작위) | 논지 §2-4 "깨진 조각이 SE 끼리 다시 붙나 · AM 에 붙나" | ★ 같은 그림 — 우리 관측량 (s1 · s2) 이 이 세 단계를 가를 수 있는지 (§8 항목 2) |
| 점착 모델 | Mei: 코팅 입자의 점착 ∝ 게스트/호스트 크기비 (확장 JKR) | SJKR · 매끈한 구 · 상별 CED (LC = AM 쌍을 SE 와 같은 γ 로 JKR 환산) | ⚠ 이산 코팅이면 AM–AM 접촉이 **SE 돌기** 를 거친다 → 매끈한 구 환산은 AM–AM 점착을 과대 [추정] |
| 접촉 힘 법칙 | 부분 걸쇠 선형 스프링 (Walton) | 압축 DEM = hooke/hysteresis · 믹서 = Hertz + SJKR + cdt | 압축 쪽과 같은 "선형 이력" 계열 [추정 — LIGGGHTS 문서 대조 전] |
| 호스트 + 게스트 동시 모사 | **불가** (2001) | 9 : 4 : 1 µm 를 함께 (원자 10 만 · CGF 151.4) | 우리 크기비가 작아서 가능한 것 [추정] — 통계는 얇다 (원자 10 만 → AM_P 176 개 · 생성기 주석) |
| 정전기 | 보통 블렌딩의 정렬 혼합 = 정전기 [51] · 코팅이 극성을 바꿈 [4] | 모델에 없음 (논지 §2-7) | 우리 모델 밖 |

### 7-1. frame[5]
실험 · 장치 총설 — DEM 은 장치 안 호스트 운동 (충돌 통계 · 힘) 만.  우리 파이프라인에서는 **혼합 (믹서 DEM) 과 코팅 (입력 상태) 을 구분** 하는 근거, 그리고 **코팅된 입자의 점착 표현** (Mei) 에 대한 경고.

---

## 8. ★★ 우리 연구에 주는 insight (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

1. **'interactive mix' 의 출처는 Orr — 논지 §2-5 · §6 의 용어 둘이 모두 출처를 얻는다 (단 한쪽은 2 차 귀속).**  Pfeffer 는 "ordered mixing (Hersey [13])" 과 "Orr [20–22] 가 'regimented' 또는 'interactive' mix 라 불렀다" 를 같이 적는다 (p.42).  → 'ordered' = Hersey 원문 확인 (`hersey1975_ordered_mixing_concept`) · 'interactive' = **Pfeffer 의 귀속** (Orr 원문 [미확인]) — 인용하려면 이 2 차 표지를 붙인다.
2. **혼합의 세 단계 = 우리 관측량의 설계 틀.**  탈응집 → 운반 입자 부착 → 운반 입자 사이 재분배 (끝 = 무작위 분포) (p.42).  → (가) s1 (SE–SE 군집) 의 시간 변화 = 1 단계 (탈응집) · (나) s2 (AM 에 붙은 SE 분율) = 2 단계 · (다) **AM 하나당 붙은 SE 수의 분포** 를 무작위 (포아송 · 분산/평균 = 1) 와 비교 = 3 단계 (Hersey 의 '같은 단위' 는 분산 0 · Bannister–Harnby 의 끝 = 무작위) [제안 · 새 관측량이면 결과 전 등록].  ⚠ s1 단독은 'AM 표면 SE 껍질' 과 '자유 SE 덩어리' 를 못 가른다 (`hersey1975_…` §8 항목 4).
3. **게스트가 클수록 피복이 안 된다 — 1 µm 게스트는 단층 투입분의 11 %.**  같은 단층 투입에서 0.05 µm 69 % → 1 µm 11 % (MAIC · PMMA 200 µm) [판독 Fig 21].  → 우리 SE (1 µm) 는 이 그림의 **가장 나쁜 쪽** 에 있다 — 실제 NCM 건식 코팅 (같은 날 카드: LPS 0.49 µm · Na₂SO₄ 0.95 µm) 은 고에너지 Hybridizer 로 SE 를 **소성 변형 · 합체** 시켜 막을 만든다.  ⇒ 우리 LC 의 "SE 가 덮은 AM" 은 막 (film) 에 가까운 상태를 가정하는데, 믹서 드럼에서 1 µm SE 구가 그 상태를 **스스로 만들 것이라는 근거는 이 논문에 없다** [추정].  논지가 "선코팅 (공정) → 혼합 (드럼)" 의 두 단계라는 점을 보고에서 분명히.
4. **이산 코팅은 AM–AM 점착을 '게스트 크기' 로 줄인다 — 매끈한 구 JKR 환산은 과대일 수 있다.**  Mei 등: 코팅 입자 쌍의 점착력 ∝ 게스트/호스트 크기비 (p.45).  → LC 의 AM_P–AM_P (Bo_code 0.00109) 는 AM 반경으로 JKR 환산했다 (논지 §2-6) — 이산 SE 돌기를 거치는 접촉이면 R\* 가 SE 크기로 줄어 **약 R_AM/r_SE (≈ 9 배) 더 약할 수 있다** [추정].  LC 에서는 AM–AM 점착이 이미 작아 결론이 바뀌지 않지만, U 팔 (CED 균일 배율) 처럼 AM–AM 점착을 키우는 팔에서는 이 과대가 커진다 → 코팅 표현 = 상별 CED 가 아니라 **돌기 (거칠기) 모델** 이 맞을 수 있다 (논지 §2-7 '거칠기 · 모양' 과 같은 축).
5. **우리 드럼은 코팅 장치가 아니다 — 대조의 질문을 정확히.**  코팅 장치는 수백–수만 rpm (§3-2) · 보통 블렌딩은 정전기 정렬 혼합까지 (p.43).  → 확인 블록 (LC ↔ LH) 이 묻는 것은 "**코팅된 입력** 이 드럼에서 더 잘 분산되는가" 이지 "드럼이 코팅을 만드는가" 가 아니다 — 보고 · 등록 문장에서 둘을 섞지 않는다.
6. **'ordered unit segregation' — 바이모달 AM 은 정렬 단위끼리 분리될 수 있다.**  운반 입자 입도가 아주 넓으면 정렬 단위끼리 분리 (p.42).  → 우리 AM_P 9 + AM_S 4 µm 는 바이모달 운반체 — 코팅 팔에서 AM_P 단위와 AM_S 단위가 드럼에서 **크기 분리** 하면 Lacey M (AM 부피 분율) 이 그것을 '혼합 불량' 으로 잡는다 [추정] → 상별 (AM_P · AM_S) 분해 지표를 같이 본다.
7. **DEM 의 2001 년 벽 — 우리는 크기비가 작아 넘었지만 통계가 얇다.**  "호스트와 게스트가 모두 있는 계는 모사 불가" (p.45 · p.60) · 자석 80 개면 호스트/자석 12.5.  → 우리 원자 10 만에 AM_P 176 개 (생성기 주석) — 혼합 지표의 표본 오차를 시드 반복으로 보고하는 이유와 같다.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
> 아래 영문은 원문 내용을 **우리가 다시 쓴 문장** 이다 (원문 문장 그대로 아님 — 괄호 쪽이 근거).
- "Dry particle coating attaches submicron guest particles onto micron-sized host particles by mechanical forces alone, without solvents or binders; it is closely related to ordered mixing, the coating being more permanent because of stronger bonding (Pfeffer et al., Powder Technol. 2001)." [인쇄 p.40–42 내용]
- "Ordered (also called interactive or regimented) mixing occurs when the two components differ in size by one or two orders of magnitude, so that the fines adhere to the carriers (Pfeffer et al. 2001, attributing 'interactive mix' to Orr)." [인쇄 p.42 내용 · Orr 원문 미확인]
- "Coating requires de-agglomeration of the guest particles, bonding to the hosts and redistribution among hosts (Bannister and Harnby, as reviewed by Pfeffer et al. 2001)." [인쇄 p.42 내용]
- "In MAIC coating of 200 µm PMMA with alumina at monolayer loading, surface coverage fell from about 69 % for 0.05 µm guests to about 11 % for 1 µm guests (read from Fig. 21 of Pfeffer et al. 2001)." [판독 — 추세만]
- ⚠ §3-9 · §8 의 우리 계 산술 (크기비 · 0.88 · ≈9 배) 은 [우리 산술 · 추정] — 원문 값으로 인용하지 말 것.

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **총설 + 자체 결과** — 응용 예 · 모델 서술 대부분이 인용 전달 (원 논문 [미확인]).  NJIT 결과도 대부분 **반복 수 · 통계 미기재**.
2. **본문 ↔ 그림 13 어긋남** — 본문: "5 분 노출" 에 실리카 110 · 미처리 60 · 5 분 처리 28 · 20 분 처리 18 % ↔ 그림 13 판독: 300 s 에서 ≈ 92 · 60 · 13 · 5 %, 곡선 끝 (≈920 s) 에서 ≈ 109 · 65 · 24 · 17 % — 인쇄값은 대체로 곡선 끝에 가깝고 **(c) 28 % 는 그림 어디에도 없다** [판독].
3. **§2 의 그림 번호가 하나씩 밀려 있다** — 본문 p.43–44: Theta Composer "see Fig. 5" · MAIC "Fig. 6" · 원심 유동화 "Fig. 7" ↔ 캡션: Fig 5 = MAIC · Fig 6 = RFBC · Fig 7 = 기포 · Fig 8 = Theta Composer (§3 의 번호는 캡션과 맞음).
4. **"피복률" 정의** — SEM 계수 · 오차 ≈5 % · 응집체로 붙은 게스트 (0.05 µm) 도 높은 피복률로 셈 — 고르기 (uniformity) 와 다른 양.  Fig 20 의 5 분 점 (68.5 %) 은 맞춤 곡선보다 높다.
5. **셀룰로스 종횡비** — "aspect ratio of 4:5, ~180/40 µm" 로 인쇄 (180/40 = 4.5) [인쇄 p.48].
6. **그림 28 범례** — 원 · 삼각 두 계열이 겹치는데 라벨은 "(b) Mg/Wax by HB" 하나 (나머지 계열 [미확인] — 본문은 "MAIC 도 비슷" 이라고만).
7. **참고문헌 [1] 과 [83] 이 같은 서지** (Naito · Kondo · Yokoyama, ISIJ Int. 33 (1993) 915) [인쇄 p.65–66].
8. **DEM 접선 식 (3) 의 감소 가지** — 분자 "T − T\*" 로 인쇄 (원 Walton 형과의 대조 [미확인]) · Mechanofusion DEM 의 입자 크기 · 개수 미기재.
9. **텍스트 층 손상** — µ · 괄호 · 슬래시 · ° 가 깨져 있다 → 기계 추출로 수치를 옮기지 말 것 (이 카드는 렌더 대조).
10. **배터리 전이** — 이 논문의 재료 · 장치 수치를 황화물 SE/NCM 에 직접 옮기지 않는다 (같은 날 kawaguchi2017 · nakamura2020 이 배터리판).

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 13 | J. Hersey, Powder Technol. 11 (1975) 41. | ✅ [`hersey1975_ordered_mixing_concept`](hersey1975_ordered_mixing_concept.md) |
| 16 | J. Hersey, W.J. Thiel, C.C. Yeung, Powder Technol. 24 (1979) 251. | ordered unit segregation — 카드 없음 |
| 20 · 22 | N.A. Orr, E. Shotton, Chem. Eng. (1973) 12, Jan. · H. Egermann, N.A. Orr, Powder Technol. 36 (1983) 117. | 'interactive mix' 원 출처 — 카드 없음 |
| 23–28 | J.N. Staniforth, J.E. Rees, Powder Technol. 30 (1981) 255. · J.N. Staniforth, Powder Technol. 33 (1982) 147. · J.N. Staniforth, J.E. Rees, J. Pharm. Pharmacol. 34 (1982) 69. · J.N. Staniforth, J.E. Rees, J. Pharm. Pharmacol. 34 (1982) 700. · J.N. Staniforth, J.E. Rees, F.K. Lai, J. Hersey, J. Pharm. Pharmacol. 34 (1982) 485. · J.N. Staniforth, Powder Technol. 45 (1985) 73. | 정렬 혼합 (제약) — 카드 없음 |
| 30 | P. Bannister, N. Harnby, Powder Technol. 36 (1983) 275. | ★ 세 단계 원전 — 카드 없음 |
| 41–44 | M. Alonso, M. Satoh, K. Miyanami, Powder Technol. 59 (1989) 45. · M. Alonso, M. Satoh, K. Miyanami, Powder Technol. 59 (1989) 217. · M. Alonso, M. Satoh, K. Miyanami, Powder Technol. 62 (1990) 35. · M. Alonso, A Fundamental Study on the Coating of Powders, Doctoral Thesis, University of Osaka Prefecture, Osaka, Japan, 1991. | 코팅 동역학 (C + N → C + C) · 통계 모사 — 카드 없음 |
| 51 | H. Honda, M. Kimura, T. Matsuno, M. Koishi, Chim. Oggi: Int. J. Chem. Biotechnol. 9 (1991) 21, June. | 보통 블렌딩 = 정전기 정렬 혼합 — 카드 없음 |
| 68 | R. Mei, H. Shang, J.F. Klausner, E. Kallman, Kona 15 (1997) 132–141. | ★ 코팅 입자의 점착 (확장 JKR) — 카드 없음 |
| 105 · 116 | O.R. Walton, R.L. Braun, J. Rheol. 30 (1986) 949–980 · O.R. Walton, Mech. Mater. 16 (1993) 239–247. | 걸쇠 스프링 접촉 — 카드 없음 |
| 110 | K.L. Johnson, K. Kendall, A.D. Roberts, Proc. R. Soc. London, Ser. A 324 (1971) 301. | ✅ [`johnson1971_jkr_surface_energy_contact_elastic_solids`](johnson1971_jkr_surface_energy_contact_elastic_solids.md) |
| 117 | C. Thornton, K.K. Yin, Powder Technol. 65 (1991) 153–166. | 탄소성 접촉 — 카드 없음 |
| 11 | M. Ramlakhan, C.Y. Wu, S. Watano, R.N. Dave, R. Pfeffer, Powder Technol. 112 (1–2) (2000) 137–148. | MAIC 원 논문 — 카드 없음 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 28 쪽 텍스트 층 전수 (pdftotext layout · raw) + 단위가 깨진 곳 렌더 대조 (170–200 dpi): 1–200 µm · 0.015 µm TiO₂ · 10 µm PTFE 응집체 · ≈15 µm 전분 · ≈180/40 µm 셀룰로스 · ≈0.3 µm 실리카 · 200 µm PMMA · 0.05/0.2/0.4/1 µm 알루미나 · 2.7 mm 자석 (그림 22 축 = µm, 2700) · 2.36 mm 자석 · 75 µm Mg · 0.7 µm 실리카 · 16 µm 왁스 · 0.7 µm 알루미나 (RFBC) · 표 1 "Size (µm)".
- 식 (1)–(10) = 렌더로 글자 대조 (식 (3) 의 두 가지 = 인쇄 그대로).
- 그림 · 표 44 장 = 본문 그림 1–42 (전부 임베디드 래스터 · 그림 안 글자 포함 — 래스터 경계 + 2 pt 로 손 크롭 · 200 dpi 원본은 300 dpi · 600 dpi 원본은 600 dpi (긴 변 3000 px 상한)) · 표 1–2 (벡터 글자 300 dpi) — 크롭 전부 열람.
- 판독 15 개 그림 → digitized.csv.  우리 쪽 대조: `scripts/make_mixer_deck.py` (`FR_ANCHOR` · `D_REAL_UM` · `DENS` · `WT` · pair_style) · 논지 `docs/hetero_thesis.md` §2-4 · §2-6 · §2-7 · `scripts/mixer_contact_reader.py` (s1 · s2 정의).
- 정본 litdb 중복 확인: `litdb/papers/` 목록 + 'Pfeffer' · 'engineered particulates' · 'dry particle coating' grep — 이 논문 카드 없음 (nakamura2020 · alizadeh2018 이 참고문헌으로만 언급).

## 🔗 관련 카드
- 같은 날 · 개념 원전: [`hersey1975_ordered_mixing_concept`](hersey1975_ordered_mixing_concept.md) — 정렬 혼합 · 단층 수용량.
- 배터리 건식 코팅 — 같은 날: [`kawaguchi2017_dry_coating_parametric_na2so4_model_se`](kawaguchi2017_dry_coating_parametric_na2so4_model_se.md) (Hybridizer 공정 창 · 모델 SE) · [`nakamura2020_dry_coating_ncm_li3ps4_core_shell`](nakamura2020_dry_coating_ncm_li3ps4_core_shell.md) (실제 Li₃PS₄ 껍질 · 이 논문 = 그 카드의 ref 26) / 이전: [`lee2026_mechanical_halogen_argyrodite_drycoating`](lee2026_mechanical_halogen_argyrodite_drycoating.md) · [`choi2026_bzox_dry_zro2x_nmc_shell_coating`](choi2026_bzox_dry_zro2x_nmc_shell_coating.md).
- 같은 날 · 점착 · 유동성: [`johnson1971_jkr_surface_energy_contact_elastic_solids`](johnson1971_jkr_surface_energy_contact_elastic_solids.md) · [`begat2004_cohesive_adhesive_balance_afm_colloid_probe`](begat2004_cohesive_adhesive_balance_afm_colloid_probe.md) · [`geldart2006_powder_flowability_angle_of_repose_tester`](geldart2006_powder_flowability_angle_of_repose_tester.md) (안식각 · Geldart 분류) · [`alizadeh2018_dem_adhesion_calibration_segregation_heap`](alizadeh2018_dem_adhesion_calibration_segregation_heap.md) (그 카드의 ref 9 = 같은 NJIT 그룹의 건식 코팅 유동성 논문).
- 혼합 지표: [`chandratilleke2012_particle_scale_mixing_index`](chandratilleke2012_particle_scale_mixing_index.md) · [`jarray2019_cohesion_driven_mixing_segregation_drum`](jarray2019_cohesion_driven_mixing_segregation_drum.md).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
