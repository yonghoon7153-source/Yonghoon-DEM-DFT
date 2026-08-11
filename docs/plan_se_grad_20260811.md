# 계획서 — `--se-grad`: SE 조성 구배 (Luan 2025 → Phase 5 / A7 확장)

> **상태: 리뷰 대기 (구현 전).**  VGCF/PTFE 계획서(`plan_vgcf_ptfe_coupling_20260811.md`)와
> **같은 리뷰 라운드**에 태운다 (Codex 요청서 §G).
> 근거 논문: Luan 2025 (AFM, GRINM 파일럿 라인, 400 Wh/kg 파우치) — 정본 digest
> `litdb/papers/luan2025_graded_cathode_400whkg_pouch.md` (friendly-meitner).
> 사용자 확인: **"gradient 도 우리 목적 중 하나"** = CLAUDE.md Big goal 의 Phase 5
> ("stack different configs as natural LAYERS inside one composite cathode") 그 자체.

---

## §0. 결론 요약

**한다.  단 "구배" 는 하나가 아니라 둘이고, 우리 파이프라인마다 만들 수 있는 것이 다르다.**
이 구분을 뭉개면 Luan 앵커를 잘못된 노브에 검증시키게 된다 — 그것이 이미 한 번 일어났다
(A7 의 `--poro-grad` 는 Yoo 2026 흑연/액체계의 **porosity 구배**인데, Luan/ASSB 가 바꾸는
것은 **조성 φ_SE 구배**다.  다른 물리다).

| 번역 | 무엇을 맞교환하나 | Luan 과 같은가 | 어느 파이프라인이 만들 수 있나 |
|---|---|---|---|
| **(a) 조성 구배** | φ_SE(z) ↕ **φ_AM(z)**, porosity 균일 | **= Luan** (CAM 90:9 ↔ 93:6, carbon 고정) | 2D synth ✓ (AM 을 우리가 배치) · **DEM 입력 생성** ✓ (LIGGGHTS 재실행 필요) |
| **(b) 배치 구배** | φ_SE(z) ↕ **porosity(z)**, AM 동결 | ≠ Luan (다른 노브) | **킷 scaffold** ✓ (AM = DEM 골격 동결 — frame[5] AM-freeze 4근거상 움직일 수 없다) |

⇒ **G1(2D synth)·G2(킷)** 는 지금 짤 수 있고, **Luan 순서-앵커의 충실한 검증(G3)은 (a)형
3D 침대가 필요해 DEM 재실행(사용자 머신)이 선행**한다.  G2 는 그 전에 V100 에서 돌릴 수
있는 **다른 질문**("주어진 AM 골격에서 이온 도체를 어디에 둘 것인가")이고, 그렇게 라벨한다.

---

## §1. 앵커 (Luan digest 에서 — 전부 order/trend-only)

- **총량 고정 3-배치**: CAM 91.5/SE 7.5/C 1.0 wt% 고정, 배치만 변경 →
  positive **204.7** / uniform 186.1 (−10 %) / reverse 178.0 (−15 %) mAh/g @ 4 mAh/cm², 0.1 C.
  (우리 `--poro-grad` 총량-고정 게이트와 같은 규율 = 방법론 정합.)
- **rate 스케일링**: 격차 0.1 C +5 % → **1 C +25 %** = 수송 이득 (열역학 아님).
- **두께 스케일링**: 1 mAh/cm² 에선 CAM 95 % 도 무사 → **얇으면 구배 효과 소멸**.
  4 mAh/cm² ≈ 65–70 µm (유도값).  ⚠ **우리 real_14 = 30.3 µm ≈ 1.6–2 mAh/cm² = 효과 미약 영역.**
- **COMSOL Table S1 (stated, 입력값 그대로 쓸 수 있음)**: 2-region φ_SE =
  positive 0.1875/0.3125 · uniform 0.25/0.25 · reverse 0.3125/0.1875 (집전체측/분리막측; 평균 0.25 고정).
- **실험 유도 φ_SE (DERIVED — 내 wt%→vol% 환산, 밀도 가정)**: 0.140/0.201 · 0.171/0.171 · 0.201/0.140.
- **trade-off 자인**: positive 의 SE-lean(93 %) 층이 DRT 10⁰–10¹ s 대역에서 저항 ↑ =
  구배는 공짜가 아니다 → **우리 STEP4 가 재현해야 할 반증 가능 예측**.
- **도전재 구배**: reverse(집전체 rich) 최적, 이득 ≈2 %, **COMSOL 전용**(실험 대조 없음).
- ⚠ 인용 금지 세트: σ_e 절대값(100× 단위 결함) · 404 Wh/kg("stack-level, 파우치필름 제외" 병기
  없이) · Fig 4j–l 농도 컬러바 · CV 기울기비의 D 해석.  (digest §7)

---

## §2. 우리 현황

- `extract_2d_microstructure.py`: `--poro-grad` (부호: >0 = 상단/분리막쪽 다공, y=0 = 집전체;
  총 porosity 고정 게이트, pass 1–3 gated + pass 4 UNGATED 폴백; K=8 밴드 실측 프로파일 meta) +
  `--cb-ratio/--cb-grad` (설계-프로파일, meta 전용).  **φ_SE 구배 노브는 없다.**
- `mpm3d_compaction.py` scaffold: `--se-frac` 균일 cell-fill (`prob = se_target/Σinter`,
  z-무관 스칼라).  `--se-dump` 는 실측 위치라 구배 대상 아님.
- STEP3/STEP4: 침대에 구배가 있으면 **자동으로 본다** (복셀/격자 기반) — 새 코드 불요.
  STEP4 는 이미 운전-φ(z) export 가 있다 (φ_e µV-평평 vs φ_i 수십 mV — 우리가 Luan 의
  개념 서사를 정량하는 자리).

---

## §3. 제안

### **G1. 2D synth `--se-grad`** — (a)형, Phase 4/5 배선 (비용 낮음)
- `synthesize_microstructure` 에 `se_grad ∈ [−1, 1]` 추가: φ_SE(z) 를
  `φ_SE·(1 + g·(z_n − 0.5))` 로 기울이고 **φ_AM(z) 가 역방향으로 보상** (porosity 균일 유지).
  **총 φ_SE·총 φ_AM 각각 고정** (`--poro-grad` 와 같은 게이트 + 마지막 pass UNGATED 폴백).
- 부호 규약 **`--poro-grad` 와 동일**: `>0` = 상단(분리막쪽) SE-rich = **Luan positive**.
  y=0 = 집전체.  meta `graded_z` 에 `se_grad` + K=8 밴드 φ_SE/φ_AM 실측 프로파일 병기.
- selftest: (i) g=0 → 기존 경로 **bitwise 동일** (§F1), (ii) g=±0.5 에서 총량 보존
  (|Δφ_tot| < 0.5 %p), (iii) 밴드 프로파일 단조, (iv) 부호 방향 (g>0 → 상단 φ_SE ↑).

### **G2. 킷 scaffold `--se-grad`** — (b)형, **Luan 과 다른 노브임을 라벨에 박제** (비용 낮음)
- 균일 cell-fill 의 `prob` 를 `prob(z) ∝ 1 + g·(z_n − 0.5)` 로 (정규화해 **총 SE 부피 불변**;
  clip ≥0; 한 z-슬라이스의 interstitial 용량 초과분은 이웃으로 재분배 — 재분배량 로그).
- **정직 라벨 (필수)**: AM 동결이라 SE↕porosity 맞교환 = **(b)형**.  payload/mpm_metrics 에
  `se_grad_mode: 'se_vs_porosity_fixed_AM'` 명시 — Luan 순서-앵커와 **직접 대조 금지**,
  Schlautmann [152] 류 "주어진 골격 위 도체 배치" 질문 전용.
- 산출: STEP3 밴드별 σ_ion/σ_e/τ (기존 솔버가 자동으로 봄) → **σ_ion(z) 프로파일**.
- selftest: g=0 bitwise 동일 · 총 SE 셀 수 보존 · z-프로파일 부호.

### **G3. Luan 순서-앵커 검증 캠페인** — (a)형 3D, **DEM 선행 필요** (비용 높음 · 별도 승인)
- 침대: **DEM 입력 생성기에 층상 조성** (2-층, Table S1 φ_SE 그대로) → 사용자 LIGGGHTS 실행
  → STEP1–4.  두께는 **≥ 65 µm** (효과가 나타나는 영역; §1).  ⚠ 100 µm 급 = n_grid 384 불가
  (V100 32 GB), 192 로 계획 + `d_h/dx ≳ 3.5` 사전 점검(스캐폴드 CSV 만으로 GPU-불요 계산).
- **사전등록 예측 4건** (§4).  이것이 통과하면 Luan 이 우리 STEP4 의 **첫 구배-방향 외부
  실험 앵커**가 된다 (절대값 아님, 순서만).

### **G4. 문서 가드 2건** (코드 변경 없음, 비용 최소)
- σ_e Stage 22.5 문서에 **"φ_AM < 0.3 외삽 금지"** 명문화 (Luan Fig 7 붕괴 φ_AM ≈ 0.2–0.28,
  우리 corpus 0.37–0.88 = 문턱항 없이 fit 된 폼).  **폼 변경 아님** (동결 유지).
- `--cb-grad` help 에 Luan 답 기록: "황화물-ASSB COMSOL 은 집전체-rich 최적, 이득 ≈2 %,
  실험 대조 없음 — 기본값 불변".  Phase-5 z-stacking 규약에 **"날카로운 조성 계단은
  비물리(Fig 6d: 롤프레스 후 계면 없음, PTFE fibril 이 층을 가로지름) → 계면 폭(수 µm
  혼합대) 규약 필요"** 추가.

---

## §4. 사전등록 검증 (G3 캠페인 — 구현 전에 박제)

| # | 예측 | 통과 기준 | 실패 시 해석 |
|---|---|---|---|
| V1 | **순서**: positive > uniform > reverse | STEP4 delivered capacity (같은 컷오프) 순서 재현 | 실패 = 우리 이온-수송 표현의 구배 감도 결손 (frame[4] 정량 한계로 보고) |
| V2 | **rate 스케일링**: 격차가 C-rate 와 함께 커짐 | 0.5 C vs 2 C 에서 V1 격차 단조 증가 (정성) | 실패 = 이득이 수송 기원이 아니라는 뜻 → V1 재해석 |
| V3 | **두께 스케일링**: 30 µm 침대에선 격차 ≈ 0 | real_14 급 두께에서 V1 격차 < 노이즈 | 실패(얇은데 격차 큼) = 우리 모델이 구배를 과대반응 |
| V4 | **trade-off**: positive 의 SE-lean 층 국소 과전압 ↑ | STEP4 층별 반응분포에서 SE-lean 밴드 η 상승 | 실패 = 층내 국소 이온부족 미표현 (frame[4]) |

- **V1–V4 는 전부 순서/방향만 요구** — 절대값 요구 없음 (§F1).
- G2(b형) 런에는 V1 을 **적용하지 않는다** (다른 노브).  G2 의 자체 검증 = 총량 보존 +
  σ_ion(z) 가 φ_SE(z) 를 단조 추종하는지 (우리 스케일링 법칙의 국소 버전).

## §5. 하지 않는 것

- **COMSOL 패리티**: 그들 모델은 미공개 퍼콜 상관식 + 재현 불가 — 패리티 대상은 PyBaMM(#5)이지
  이 논문이 아니다.
- **σ_e 절대값 사용**: 100× 단위 결함 (digest §7).
- **--poro-grad 의 대체/제거**: Yoo 앵커(porosity 구배)는 액체계 질문으로 **유효** — 노브 병존,
  help 텍스트에 "액체계=Yoo / ASSB 조성구배=--se-grad" 구분만 명시.
- **5 Ah 파우치 조성(85/88 % 이층) 재현**: 구배 실험과 다른 조성 + 적층 정보 미기재.

## §6. 리뷰 질문

- **Q1**: G2(b형)를 지금 하는 것이 옳은가, 아니면 (a)형이 가능해질 때까지 미뤄 **앵커 혼동
  리스크**(라벨을 박아도 결과 표에서 섞일 수 있다)를 없애는 게 나은가?
- **Q2**: G1 의 "φ_AM 보상" 방식 — AM 입자 배치를 z-가중으로 바꾸는 것이라 2D synth 의
  coverage·CN 핀과 상호작용할 수 있다.  핀 우선순위(coverage 를 지키고 구배를 양보 vs 반대)를
  어느 쪽으로?
- **Q3**: G3 의 DEM 층상 침대 — 입력 생성기에서 2-층 삽입(ز-영역별 조성)으로 충분한가,
  아니면 층 경계 혼합대(§3-G4 계면 폭)까지 생성 단계에서 넣어야 하나?
- **Q4**: V3(두께 스케일링)를 위해 65 µm 급 침대를 새로 만드는 대신, 기존 kit_ps(105–114 µm)
  침대에 (b)형 구배를 걸어 **두께 축만 먼저** 보는 절충이 의미 있나? (노브가 달라 V1 과
  분리 보고해야 함.)

## §7. 순서 (승인 시)

1. **G4** (문서 가드 — 무해, 즉시)
2. **G1** (2D synth, selftest 포함) → 커밋
3. **G2** (킷, 라벨 박제 + selftest) → 커밋 → V100 에서 (b)형 스모크 1건
4. **G3** 은 Codex/사용자 리뷰 통과 + DEM 실행 일정 확정 후 별도 착수
5. VGCF/PTFE 계획서의 3각 적대리뷰 결과가 나오면 **같은 종합 문서**에서 두 계획을 함께 판정
