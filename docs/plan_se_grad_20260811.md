# 계획서 — `--se-grad`: SE 조성 구배 (Luan 2025 → Phase 5 / A7 확장)

> **상태: 리뷰 대기 (구현 전).**  VGCF/PTFE 계획서(`plan_vgcf_ptfe_coupling_20260811.md`)와
> **같은 리뷰 라운드**에 태운다 (Codex 요청서 §G).
> 근거 논문: Luan 2025 (AFM, GRINM 파일럿 라인, 400 Wh/kg 파우치) — 정본 digest
> `litdb/papers/luan2025_graded_cathode_400whkg_pouch.md` (friendly-meitner).
> 사용자 확인: **"gradient 도 우리 목적 중 하나"** = CLAUDE.md Big goal 의 Phase 5
> ("stack different configs as natural LAYERS inside one composite cathode") 그 자체.

---

> ## ★★ Codex 독립리뷰 판정 (2026-08-11) — 아래 본문은 그 판정으로 갱신됨
> **G4 GO · G1 REDESIGN 후 GO · G2 현재안 HOLD(★ production dead path) · G3 HOLD.**
> 내가 §6-Q2 에서 전제한 "coverage/**CN** 핀 충돌" 은 **전제가 틀렸다** — 2D generator 에
> coordination/CN 계산도 핀도 **없다** (직접 확인: grep 0건).  coverage 만 있다.

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

### **G1. 2D synth `--se-grad`** — (a)형 · **REDESIGN 후 GO** (Codex)
★ 재설계 요건: **band 별 AM/SE 면적과 P:S 를 직접 제어**하고, coverage carving·pore refill 등
**모든 후처리 뒤 K-band profile 을 재측정**해 게이트한다.  우선순위(Codex Q2 답):
 1 hard 전역 AM/SE/void 총량 → 2 hard **realized** φ_SE(z)·φ_AM(z)·구배 부호/단조성 →
 3 hard band 별 AM_P:AM_S 비와 porosity → 4 soft coverage(readout) → 5 readout 연결성/CN
둘을 동시에 못 맞추면 **조용히 구배를 평탄화하지 말고** `infeasible` / `gradient_degraded` 로 기록.
- `synthesize_microstructure` 에 `se_grad ∈ [−1, 1]` 추가: φ_SE(z) 를
  `φ_SE·(1 + g·(z_n − 0.5))` 로 기울이고 **φ_AM(z) 가 역방향으로 보상** (porosity 균일 유지).
  **총 φ_SE·총 φ_AM 각각 고정** (`--poro-grad` 와 같은 게이트 + 마지막 pass UNGATED 폴백).
- 부호 규약 **`--poro-grad` 와 동일**: `>0` = 상단(분리막쪽) SE-rich = **Luan positive**.
  y=0 = 집전체.  meta `graded_z` 에 `se_grad` + K=8 밴드 φ_SE/φ_AM 실측 프로파일 병기.
- selftest: (i) g=0 → 기존 경로 **bitwise 동일** (§F1), (ii) g=±0.5 에서 총량 보존
  (|Δφ_tot| < 0.5 %p), (iii) 밴드 프로파일 단조, (iv) 부호 방향 (g>0 → 상단 φ_SE ↑).

### ~~G2. 킷 scaffold `--se-grad`~~ → ⛔ **HOLD (Codex: production dead path)**
★ **결정적 사실 (내가 직접 확인)**: production `run_mpm.sh` **10개 킷 전부 `--se-dump` 를
넘긴다** → real-SE raster 경로를 탄다.  그런데 내 `prob(z)` 계획은 `--se-dump` **없을 때만**
도는 uniform cell-fill `else` 분기에 들어간다 ⇒ **그대로 구현하면 production 킷에서 죽은 길**이다.
그래도 하려면 **격리 계약**이 선행 (Codex):
```yaml
se_grad_mode: se_vs_porosity_fixed_AM
source_geometry: synthetic_cell_fill      # --se-dump·--load-state 와 상호배타
am_scaffold_frozen: true
exchange_partner: void
anchor_eligible: false                    # 일반 corpus/surrogate 등록 제외
campaign_namespace: experimental_se_grad_b
```
비교 대상도 real-SE baseline 이 아니라 **같은 cell-fill sampler 의 명시적 `g=0`** 이어야 한다.
아래 원안은 역사로만 남긴다.

#### (원안) 킷 scaffold `--se-grad` — (b)형
- 균일 cell-fill 의 `prob` 를 `prob(z) ∝ 1 + g·(z_n − 0.5)` 로 (정규화해 **총 SE 부피 불변**;
  clip ≥0; 한 z-슬라이스의 interstitial 용량 초과분은 이웃으로 재분배 — 재분배량 로그).
- **정직 라벨 (필수)**: AM 동결이라 SE↕porosity 맞교환 = **(b)형**.  payload/mpm_metrics 에
  `se_grad_mode: 'se_vs_porosity_fixed_AM'` 명시 — Luan 순서-앵커와 **직접 대조 금지**,
  Schlautmann [152] 류 "주어진 골격 위 도체 배치" 질문 전용.
- 산출: STEP3 밴드별 σ_ion/σ_e/τ (기존 솔버가 자동으로 봄) → **σ_ion(z) 프로파일**.
- selftest: g=0 bitwise 동일 · 총 SE 셀 수 보존 · z-프로파일 부호.

### **G3. Luan 순서-앵커 검증 캠페인** — ⛔ **HOLD (Codex)**.  선행 3건:
 ① **wt%→vol% 변환 규약** — 현행 deck weight 는 **질량 레시피** 의미인데 Luan Table S1 의
   φ_SE 는 **부피분율**이다.  밀도·porosity·carbon 포함여부를 명시해 wt%→vol%→template
   count/weight 로 변환해야 한다.  **COMSOL 이상화 profile 을 그대로 넣으면 안 된다.**
 ② **finite interface** — sharp step 은 limiting control 로만.  profile family =
   `uniform` · `two_layer_sharp` · **`two_layer_mixed(width_um)`(primary)** · 같은 width 의
   positive/reverse.  생성 직후·압밀 후 realized band profile 을 둘 다 기록.
 ③ **실험 wt% 기반 profile 을 external-anchor primary** 로, COMSOL 0.1875/0.3125 는
   **sensitivity arm** 으로 분리 — 이상화 profile 로 같은 논문의 순서를 맞추면 진폭까지
   내부 모델에 맞춘 **약한 순환검증**이 된다.
(원안)
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
| V3 | ~~30 µm 에선 격차 ≈ 0~~ → **재설계 (Codex)**: 30 µm ≠ 1 mAh/cm² 다.  `ΔQ(30µm) < ΔQ(65µm)` + **독립 노이즈/등가 밴드**로.  같은 (a)형 조성·profile·scaffold family 에서 30/65/(105) µm × uniform/positive/reverse × paired seeds 필요 | |
| V4 | ~~SE-lean 층 국소 과전압~~ → ⛔ **readout 전 HOLD (Codex SG-01)**: STEP3 는 **전역** σ_e/σ_ion/τ 만 낸다.  `phi_profile` 은 unit-ΔV layer potential 이지 국소 전도도가 아니고, STEP4 φ(z) 는 분포반응이 섞인 운전 전위라 σ(z) 로 환산 불가.  DRT 저항과 국소 η 를 같은 observable 로 보지 말 것 | |

- **V1–V4 는 전부 순서/방향만 요구** — 절대값 요구 없음 (§F1).
- V1 은 **same total AM/SE · 같은 cutoff·grid · paired multi-seed** 조건에서만, **순서 확률과
  CI** 로 보고 (Codex).  V2 는 **문헌이 준 0.1↔1 C 를 primary**, 0.5↔2 C 는 외삽 secondary.
- G2(b형) 런에는 V1 을 **적용하지 않는다** (다른 노브).  ⚠ 그리고 "σ_ion(z) 가 φ_SE(z) 를
  **단조 추종**" 을 code selftest 로 쓰면 안 된다 (Codex SG-04) — 실제 침대에서는
  topology/percolation 때문에 **비단조가 물리적으로 가능**하다.  합성 slab 해석해 테스트와
  실제 morphology 결과를 분리한다.

### ★ 신규 구현 계약 (Codex SG-01~04) — G1/G2 착수 전 필수
- **SG-01 band readout 부재**: 위 V4 참조.  face flux·Joule 기반 **band 저항 몫**,
  band 반응 몫/활용률, 미퍼콜 band 는 `null + reason`, STEP4 band 전류가중 과전압 export.
- **SG-02 `g=0 bitwise` 와 총량 보존이 섞였다**: 단순 `prob·w(z)` + clip 은 z 별 free
  capacity·포화 때문에 **총 셀 수를 보존하지 않는다**.  → 옵션 미지정 `None` = 완전 legacy
  (RNG 소비 포함) · 명시적 `g=0` = 새 campaign 의 uniform control · `g≠0` = 같은 uniform draw
  의 target `N0` 를 **capacity-aware 무복원 가중표집**으로 재배치 (`ΣN_k=N0`, `N_k≤cap_k`,
  포화/재분배 원장).  "geometry bitwise" 와 "provenance JSON bytewise" 를 구분해 약속.
- **SG-03 provenance 가 STEP4 까지 자동 전달 안 됨**: CLI → MPM metrics/restart → payload
  whitelist + STEP3 manifest → step4_grid → STEP4 params/result → webapp 등록/campaign 필터
  전 경로에 mode·profile family·exchange partner·requested/realized profile·interface width·
  seed·grid·scaffold digest·`anchor_eligible` 를 실어야 한다.

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

## §7. 순서 (Codex 반영 최종)

1. **G4** 문서 가드 (무해, 즉시) — **GO**
2. **G1 재설계** — band-면적 제약 generator + 최종 profile 게이트 → 커밋
3. **band transport/reaction readout + provenance end-to-end 배선** (SG-01·SG-03)
4. **G2 는 격리 experimental mode 로만** — 보존/배선 스모크까지 (production 대조 금지)
5. **G3 은 wt%→vol% 변환·finite interface·matched thickness 행렬이 준비된 뒤** 승인
5. VGCF/PTFE 계획서의 3각 적대리뷰 결과가 나오면 **같은 종합 문서**에서 두 계획을 함께 판정
