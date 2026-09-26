# SI 물성표 리뷰 대응 — 강준희 코멘트 (2026-09-25) · 누적 문서

> 계기: SDCP 원고 SI 물성표 (NCM811 · LPSCl · VGCF) 에 대한 강준희 코멘트 5 건 (09-25 11:40).
> 원칙: **(1) 출처 분류는 사실대로** — 문헌이 그 값을 직접 주지 않으면 `Ref.` 로 바꾸지 않는다 (이 리포는 오귀속으로 세 번 데였다:
> Trevisanello → σ_S/σ_P · [35] → σ_SDCP (`CL-61`) · [36] → 펠릿 보정 (`CL-62`)).  **(2) Assumed 라도 방어는 문헌 밴드 + 우리가 이미 돌린
> 민감도 런으로** 한다.  **(3) 형식은 저널 SI 관행** — 분류 어휘를 표 범례로 정의하고, 한정은 각주로, 문헌은 SI 참고문헌 번호로, 근거 수치는
> Supplementary Figure/Table 로.
> 진행: 항목마다 ① 사실 ② 이미 한 런 ③ 논문 형식 수정안 ④ 답변 초안 ⑤ 남은 일.  상태 = ✅ 정리됨 · ⏳ 진행 · ⬜ 미착수.
> ★ **준희가 본 표 = 사용자 원고 docx 의 Table S2** (09-03/04 검토로 라벨 확정 — `docs/reviews/ms_readthrough_20260903.md`).  리포의
> 생성기 `docs/manuscript_draft/build.js` 는 08-23 판에서 멈춰 있어 라벨이 다르다 (NCM σ_e `Effective value` · VGCF 직경 `Supplier data` ·
> DEM ν 행 없음 · 참고문헌 S6–S8).  ⇒ 이 문서의 "현 표기" 는 **준희가 본 docx 판** 기준이다.

## 0. 공통 — 표 범례 (분류 어휘 정의) · 제안

현 표는 `Experimental value · Measured · Calibrated · Calculated · Assumed · Ref. Sx` 를 쓰는데 **정의가 없다** — 코멘트의 절반이 여기서 나온다.
표 아래 범례로 고정한다 (제안):

> *Measured*: measured in this work (method in Supplementary Note …).  *Calibrated*: adjusted to reproduce an experimental observable
> (Section …).  *Calculated*: derived from other entries of this table.  *Ref.*: value taken directly from the cited work.
> *Assumed*: model input without an independent measurement; the footnote gives the literature range and the sensitivity of the
> conclusions to the value.

- `Experimental value` (NCM 반지름) 와 `Measured` (LPSCl 반지름) 가 **같은 뜻인지** 확인 필요 — 같으면 한 단어로 통일.
- SI 참고문헌은 SI 첫 인용 순서로 번호를 매긴다.  ⚠ `[S6]` · `[S7]` (PTFE 기하) 는 `CL-66/67` 로 표에서 빠져 번호가 재배열될 수 있다 —
  새 문헌은 아래에서 `S(new)` 로 두고 최종 조립 때 번호를 확정한다.

## 1. NCM811 electronic conductivity — 1.0 × 10⁻² S cm⁻¹ · 현 표기 `Assumed` · ✅ 재검토 완료 (09-25 오후) · ✅ Wang 2018 원문 확인 (09-25 밤) — 사용자 결정 1 건 대기

**코멘트**: *"ncm 의 electronic conductivity 는 assumed 여야 하나? reference 가 있지 않나?"*

**결론**: `Assumed` 유지가 맞다.  문헌 측정값은 있지만 NMC 의 σ_e 는 조성·충전상태에 따라 여러 자릿수 움직여 **"NCM811 = 얼마" 로 가져다 쓸 단일
참고값이 없고**, 우리 1.0 × 10⁻² 는 문헌에서 가져온 값도 아니다.  문헌 범위와 이미 돌린 민감도 (CL-70) 를 각주로 붙인다.

> **09-25 재검토에서 고친 것** (앞 판 대비): ① Wang 2018 수치는 여전히 PDF 미확인 — 인용 보류 유지.  ② 앞 판의 *"리포에 격자점별 수치가 없다"* 는
> **틀렸다** — 원장 `CL-70` `measured` 에 9 격자점 표가 있다 (③).  ③ 원고 생성기 메모 D14 의 *"문헌 두 출처가 NMC bulk 를 5 × 10⁻⁵ 로 준다 = 1/200"*
> 은 **모델 입력값을 측정값으로 읽은 것** — 같은 커밋에서 정정 (②).  ④ 표 라벨 이력과 AM 클래스 한정을 ① 에 추가.
>
> **09-25 밤 — Wang 2018 원문 확인** (사용자 제공 PDF 본문 + SI · 정본 카드 `wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni`, canon 커밋
> `35b481d0d` · 핵심 문장은 본문 PDF 텍스트에서 직접 대조): ① **NMC811 σ_e = 4.1 × 10⁻³ S cm⁻¹ (20 °C, DC 분극)** 확정 — 우리 값은 그 2.4 배.
> ② **5 × 10⁻⁵ 는 이 논문에 없다** — Zhang 2023 의 "Wang 2018" 귀속은 원문으로 성립하지 않는다.  ③ 같은 조성 (NMC532, 합성 그대로) 에서
> Wang ↔ Amin & Chiang 이 **~3 자릿수** 어긋난다 = 연구실 간 산포.  ⇒ ② 표 · 정리 · ③ · ④ 각주 (S(new2) 투입) · ⑤ 답변 · ⑥ 갱신.
> 결론 (`Assumed` 유지) 은 그대로다 — 오히려 근거가 하나 늘었다 (③).

### ① 사실 — 이 값은 어디서 왔나 (코드·원장 원문 대조)
- 복셀 솔버 `nmc811` 프리셋 기본값 — `scripts/mpm_webapp_payload.py:1423` `a.sigma_am_s = 0.010`.
- `scripts/step3_sigma.py:20–27` 원문: *"AM_S 0.010 / AM_P 0.005 ⚠ corpus-fit endpoints, NOT a Trevisanello measurement … 10/5 = our σ_e
  scaling-law fit endpoints (live 9.13/4.14) rounded.  ⚠ scale transplant: … using them as a voxel phase σ has an unknown multiplier …
  Treat as an order-of-magnitude hook."*
- 이력:
  1. **출발 (2026-06, Stage 22.5)**: DEM σ_e 스케일링 법칙의 AM 계수를 코퍼스 (DEM 접촉망 솔버 출력) 에 적합 → **σ_S 9.13 · σ_P 4.14 mS cm⁻¹ →
     10 · 5 로 반올림해 LOCKED**.  = 솔버 출력을 가장 잘 재현하는 **유효 AM 계수** (실험 적합이 아니다).
  2. 당시 라벨 "Trevisanello 2021 — 단결정 ≈10 · 다결정 ≈5" 는 **A1 정정 (2026-06-30, `docs/a1_sigma_e_direction_closeout.md`)** 으로 철회 —
     Trevisanello 는 σ_e 가 아니라 Li⁺ 화학확산 · BET · R_ct 를 쟀고, 입경 **방향**만 지지한다.
  3. STEP3 (복셀) 이식: SDCP 원고 NCM811 (r 2.5 µm) 에 AM_S 끝점 **0.010 S cm⁻¹** 을 상 σ 로 부여.
  4. 방어 전환 (2026-09-02): 문헌 앵커가 없으니 **민감도로** — closure 스윕 (③).
  ⇒ **1.0 × 10⁻² 는 물리로 고른 값이 아니라 DEM 스케일링 법칙 적합값을 이어받은 것**이다.  문헌 범위 상단과 맞는 것은 **사후 정합**이지 채택
  근거가 아니다 — 각주에 "문헌에서 골랐다" 로 읽히는 문장을 쓰지 않는다.
- 표 라벨 이력: 08-23 까지 생성기 라벨 `Effective value ᵃ` + 각주 ᵃ *"calibrated against the measured electrode response"* — ⚠ **이 각주는 사실이
  아니었다** (실험이 아니라 DEM 솔버 출력에 적합했다).  08-23 각주 제거 (D14 로 이동) → 09-03 원고 표 검토에서 `Assumed` 로 정정.  준희가 본 판이 그것이다.
- 내부 한정 (원고에는 쓰지 않는다): 침대의 NCM (r 2.5 µm) 은 **크기로** AM_S 끝점 (10 mS cm⁻¹) 을 받았다.  원고는 다결정으로 기술하고, 우리 DEM
  규약의 다결정 끝점은 AM_P 5 mS cm⁻¹ 다 (2 배 차 — D14 가 확인을 요청해 둔 것).  둘 다 ③ 스윕 범위 안이라 순서 결론은 안 바뀐다.
  (09-25 밤 참고: AM_P 5 × 10⁻³ S cm⁻¹ 는 Wang 2018 NMC811 DC 값 (25 °C 환산 ≈ 4.8 × 10⁻³, E_a 0.25 eV) 과 가깝다 — 이것도 **사후 정합**이라
  채택 근거로 쓰지 않는다.)

### ② 문헌 — "reference 가 있지 않나" 에 대한 사실
| 출처 | 무엇을 쟀나 | σ_e (S cm⁻¹) | 지위 |
|---|---|---|---|
| Amin & Chiang, *J. Electrochem. Soc.* **163**, A1512 (2016), DOI 10.1149/2.0131608jes | NMC333 · NMC532 단상 소결 펠릿 (첨가제 없음), 전자/이온 분리 DC, 30 °C | x = 0 (방전): **5.0 × 10⁻⁸** (333) · **1.9 × 10⁻⁶** (532) → x = 0.75: **7.9 × 10⁻³** · **1.4 × 10⁻²** | ✅ 정본 카드 `aminchiang2016_nmc_electronic_ionic_transport_vs_li` (Fig. 2c 디지타이즈 3 중 검증).  ⚠ 811 은 없다 |
| Wang, Yan, Li, Vinado, Yang, *J. Power Sources* **393**, 75–82 (2018), DOI 10.1016/j.jpowsour.2018.05.005 | LiCoO₂ · NMC333/532/622/811 **SPS 펠릿** (800 °C · 40 MPa · 5 min, 상대밀도 > 98 %, 받은 분말 그대로 — 충방전 이력 없음) · 양면 Ag paste 이온차단 2 단자 **DC 분극** + EIS (p.76 §2) | 20 °C: NMC333 2.2 × 10⁻⁶ · NMC532 1.3 × 10⁻³ · **NMC811 4.1 × 10⁻³** (p.78 §3.3 · Fig. 4f).  별도: 4 단자 전기전도도 NMC811 2.1 × 10⁻² · NMC622 5.9 × 10⁻³ (28 °C, p.80 — 저자는 σ_e + σ_i 로 해석) | ✅ **원문 확인 (09-25 밤)** — 본문 PDF 문장 대조 · 정본 카드 `wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni` (canon `35b481d0d`, 그림 20 장).  ⚠ 이 논문의 σ_i 는 카드에서 **인용 금지** (자기 CV D̃ · Nernst–Einstein 역산과 불일치) → σ_i 를 품은 4 단자 값은 각주에 쓰지 않는다.  ⚠ NMC333 상온점은 실제 25 °C (Fig. 4b 범례 — 본문은 20 °C) |
| 모델 논문 입력값: Sangrós 2020 (1 × 10⁻⁵, Amin & Chiang 인용) · Alabdali 2023 (5 × 10⁻⁵, NMC622) · Zhang 2023 (5 × 10⁻⁵, Wang 2018 을 출처로 표기) | 시뮬레이션 **입력** | 10⁻⁵ … 5 × 10⁻⁵ | ⛔ **측정이 아니다** — 방전 상태 · 저 Ni NMC 의 입력값.  811 참고값으로 쓰면 안 된다 (정본 카드 `sangros2020_lib_electrode_dem_mech_elec_ionic` · `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` · `zhang2023_pfib_multiscale_imaging_4d_thick_cathode`).  ⛔ **Zhang 2023 의 "Wang 2018" 귀속은 성립하지 않는다** — Wang 2018 본문 · SI 에 5 × 10⁻⁵ 가 없고 (본문 텍스트 전수 검색으로 재확인), NMC811 은 −20…100 °C 전 구간 7.6 × 10⁻⁴ 이상이다 (카드의 Fig. 4 판독).  근처 값은 NMC333 의 100 °C 값뿐 |
| Lee 2026 (LPSCl 코팅 NCM811) | 본문 서술 | *"in the range of 10⁻⁴"* | ⛔ 인용 없는 서술 (정본 카드 `lee2026_lpscl_coating_thickness_ncm811`) |

⇒ 정리:
1. **단일 참고값이 없다** — NMC 측정값이 조성·충전상태에 따라 5 × 10⁻⁸ … 1.4 × 10⁻² S cm⁻¹ 로 움직인다 (Amin & Chiang: 333 은 x = 0 → 0.75
   에서 5 자릿수).  **게다가 같은 조성 · 같은 상태에서도 연구실 간 ~3 자릿수가 어긋난다** — 합성 그대로의 NMC532: Wang 1.3 × 10⁻³ (20 °C) ↔
   Amin & Chiang 1.9 × 10⁻⁶ (30 °C) = 온도 보정 전에도 ~700 배 (30 °C 로 환산하면 ~1000 배 · NMC333 은 30 °C 환산 ~70 배 — 카드 §3-5).  원인은 두 논문으로 가려지지 않는다 (SPS ↔ 소결 등 시료
   준비가 다르다).  ⇒ 어느 한 값을 `Ref.` 로 달면 "한 연구실의 값" 을 고르는 것이 된다.
2. **pristine NCM811 = 4.1 × 10⁻³ S cm⁻¹ (20 °C, DC 분극)** — Wang 2018 원문 확인.  (Amin & Chiang 을 Ni 함량에 로그-선형 외삽한 1.3 × 10⁻³ 은
   이제 필요 없다.)
3. 우리 1.0 × 10⁻² 는 그 **2.4 배** (25 °C 환산 대비 2.1 배) = **같은 자릿수**이고, Amin & Chiang 축 (조성·충전상태) 에서는 범위 상단이다.
   ⚠ "문헌과 맞다" 는 **사후 정합**이지 채택 근거가 아니다 (①) — 각주에는 비교로만 쓴다.
4. 준희가 떠올린 "reference" 가 모델 논문의 5 × 10⁻⁵ 라면, 그것은 입력값이지 NCM811 측정값이 아니고, 그 값이 붙은 출처 (Wang 2018) 에도 그 값이 없다.

### ③ 이미 돌린 런 — σ_NCM · σ_SDCP 공동 closure 스윕 (원장 `CL-70` live · 사전등록 `docs/reviews/sigma_closure_sweep_prereg_20260902.md`, 런 전 커밋 6cd1fb03 · kgy 완주 09-06)
DBE/SBE 비 R̄ (8 origin 쌍대응 평균, vox 0.15 · centerline):

| σ_NCM (S cm⁻¹) \ σ_SDCP (S cm⁻¹) | 2.5 (÷100) | **250 (생산)** | 25 000 (×100) |
|---|---|---|---|
| 3.33 × 10⁻⁴ (÷30) | 1.0578 | 1.3403 | 1.3530 |
| **1.0 × 10⁻² (생산)** | 1.0668 | **1.3078** | 1.3185 |
| 0.30 (×30) | 1.0666 | 1.1979 | 1.2035 |

- 판정 (**런 전 등록 규칙**) = **DIRECTION-ROBUST**: 9 격자점 전부 `R̄ − 3·SD > 1.01` (최소 1.0522) · 미수렴 팔 0/144.
- **σ_NCM 이 클수록 이득이 작다** (생산 σ_SDCP 열 1.3403 → 1.3078 → 1.1979).  ⇒ Wang 2018 의 pristine NCM811 (4.1 × 10⁻³, 우리보다 2.4 배 낮다) 은
  격자점 3.33 × 10⁻⁴ 과 1.0 × 10⁻² **사이**이고, 그 두 격자점의 비가 1.3403 · 1.3078 이라 방향은 **1.31 이상 쪽**이다 — 이득 측면에서 우리 값은
  보수적인 편이다.  (⚠ 격자점 사이 값은 시나리오 보간이지 측정이 아니다 — 그 자리의 비를 숫자로 적지 않는다.)
- 생산점이 원고 헤드라인을 다른 기계에서 재현 — σ_e(SBE) 53.9 (원고 54.0) · σ_e(DBE) 70.6 mS cm⁻¹ · R 1.307824.
- 등록된 한정어 (유지): 격자점 9 (등록 25) · origin SD 는 표준오차가 아니다 (한 침대의 {0,½}³ factorial) · 격자점 사이 폭은 시나리오 범위 ·
  참 σ 값 · 격자 수렴 · 접촉저항 분배는 답하지 않는다.
- ✅ **원자료가 리포에 있다** — 위 표 · `R̄ − 3·SD` · 쌍대응 산포가 원장 `CL-70` `measured` 에 그대로 있어 **SI 그림을 지금 만들 수 있다**.  kgy
  `~/sdcp/verdicts_9pt.log` 는 출처 보강용 (선택).

### ④ 논문 형식 수정안
1. **Table S2 행**: `Electronic conductivity · 1.0 × 10⁻² · S cm⁻¹ · Assumedᵃ`
   > ᵃ Effective model input, not an intrinsic property of NCM811.  Reported electronic conductivities of layered LiNiₓMnᵧCo_zO₂ range from
   > 5 × 10⁻⁸ to 1.4 × 10⁻² S cm⁻¹ with composition and state of charge (Ref. S(new1)) and differ by up to three orders of magnitude between
   > studies of the same composition (Refs. S(new1), S(new2)); for pristine NCM811, DC polarization gives 4.1 × 10⁻³ S cm⁻¹ at 20 °C
   > (Ref. S(new2)), within a factor of 2.5 of the value used.  The DBE > SBE ordering holds for σ_NCM from 3.3 × 10⁻⁴ to 0.30 S cm⁻¹, over
   > which the DBE/SBE ratio decreases from 1.34 to 1.20 at the SDCP conductivity used here (Supplementary Fig. S(new)).
   - S(new2) (Wang 2018) — **09-25 밤 원문 확인 완료 → 투입**.  앞 초안 대비 바뀐 것: ① 범위를 "~10⁻⁸ to ~10⁻²" 에서 실측 끝값
     (5 × 10⁻⁸ · 1.4 × 10⁻², Amin & Chiang) 으로 — 5 × 10⁻⁸ 은 10⁻⁷ 쪽에 더 가깝다  ② "upper end of this range" 대신 **NCM811 실측과의 거리**
     (2.4 배 → "within a factor of 2.5")  ③ 연구실 간 산포 한 구절 — 단일 `Ref.` 가 안 되는 두 번째 이유다.
   - ⛔ 쓰지 않는 것: Wang 의 4 단자 값 2.1 × 10⁻² (σ_i 를 품는데 이 논문의 σ_i 가 인용 금지) · "consistent with / agrees with the literature"
     류 문장 (채택 근거로 읽힌다 — ①).
2. **Supplementary Figure (신설)**: 3 × 3 격자 (σ_NCM × σ_SDCP) 의 R̄, 생산점 표시.  캡션 한정어: *"Nine closure combinations evaluated on one
   SBE/DBE bed pair; bars show the spread over eight grid-origin phases of a single bed, not a standard error; no interpolation between grid
   points."*
   ✅ **09-26 생성** (사용자 비준 — 리포 기본 형식): `docs/figures/sigma_closure_3x3.png` (+ svg · csv · Origin csv), 생성기
   `scripts/plot_sigma_closure_3x3.py` — 원장 CL-70 에서 직접 읽고 9 칸을 검산한다 (selftest 음성 대조 3).  (a) 격자 9 칸의 R̄ · (b) σ_NCM 축의 점 (잇지 않는다).
   ⚠ ±3·SD 막대는 기호보다 작다 · Wang 2018 NCM811 값은 축에 그리지 않았다 (격자점 사이 값을 읽게 만든다 — 보간 금지).  캡션 (제안):
   > *Supplementary Fig. S(new). DBE/SBE electronic-conductivity ratio over nine closure combinations of σ_NCM (3.3 × 10⁻⁴, 1.0 × 10⁻²,
   > 0.30 S cm⁻¹) and σ_SDCP (2.5, 250, 2.5 × 10⁴ S cm⁻¹), evaluated on one SBE/DBE bed pair. (a) Mean ratio at each grid point; the outlined
   > cell is the combination used in this work. (b) The same values against σ_NCM; error bars (±3 SD) show the spread over eight grid-origin
   > phases of a single bed, not a standard error, and are smaller than the symbols. Points are not connected: no interpolation between grid
   > points is implied. All nine points exceed the pre-registered threshold (mean − 3 SD > 1.01, dashed line).*
3. **Methods 한 문장** (Stage 3 문단 뒤): *"The electronic conductivity assigned to NCM811 (1.0 × 10⁻² S cm⁻¹) is an effective input rather
   than a measured property; the DBE/SBE ordering is unchanged when it is varied thirty-fold in either direction (Supplementary Fig. S(new))."*
4. **SI 참고문헌**: S(new1) Amin & Chiang, *J. Electrochem. Soc.* **163**, A1512 (2016) · S(new2) Wang *et al.*, *J. Power Sources* **393**,
   75–82 (2018) — 둘 다 원문 확인.

### ⑤ 답변 초안 (강준희에게)
> reference 는 있어. Wang 2018 (JPS 393) 이 pristine NCM811 펠릿을 DC 분극으로 재서 4.1e-3 S/cm (20 °C) — 우리 1e-2 는 그 2.4 배라 같은 자릿수야.
> 근데 Ref. 로 달기 어려운 이유가 둘 있어. ① 우리 1e-2 는 거기서 가져온 값이 아니라 DEM 스케일링 법칙 적합값을 이어받은 모델 유효값이라,
> Ref. 로 달면 오귀속이 돼. ② 문헌끼리도 안 맞아 — 같은 NMC532 (합성 그대로) 를 Wang 은 1.3e-3, Amin & Chiang 2016 (JES) 은 1.9e-6 으로 재서
> 연구실 간에 ~3 자릿수가 차이 나고, 조성·충전상태까지 치면 5e-8~1.4e-2 S/cm 로 움직여. 그래서 Assumed 로 두고 각주에 문헌 범위 + Wang 811 값 +
> 민감도를 달게. 모델 논문들이 쓰는 5e-5 는 입력값이고 (Zhang 2023 은 Wang 2018 을 출처로 다는데 원문엔 그 값이 없어).
> 민감도는 이미 돌려 놨어: σ_NCM 을 3.3e-4~0.3 (÷30~×30) 으로 바꿔도 9 조건 전부 DBE > SBE (사전등록 판정 DIRECTION-ROBUST).
> σ_NCM 이 클수록 이득이 작아져서 (비 1.34 → 1.20), Wang 값처럼 더 낮으면 오히려 이득이 커지는 쪽이야 — 우리 값이 보수적인 편.
> 이 격자는 SI 그림으로 붙일게.

### ⑥ 결정할 것 · 남은 일
- [ ] **결정 (사용자)** — A (권장): `Assumed` + 각주 ᵃ (S(new1) + S(new2)) + SI 그림 · 재계산 없음.  B: 문헌값 (Wang 2018 NCM811 DC
  4.1 × 10⁻³ — 이제 원문 확인됨) 으로 바꿔 `Ref.` — 생산 STEP3 팔 전부 재실행 + 헤드라인 (54.0 · 70.6 · 1.308) 이 바뀌고, 충전상태 의존이라
  가정은 남으며, 같은 조성에서 연구실 간 ~3 자릿수 산포라 **한 연구실의 값을 고르는 것**이 된다.  ⇒ Wang 확인 뒤에도 권장은 A.
- [x] Wang 2018 PDF 확인 (사용자 제공 본문 + SI) → 정본 카드 `wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni` (canon `35b481d0d`) →
  각주 S(new2) 초안 투입 (09-25 밤).
- [x] 정본 카드 `zhang2023_pfib_multiscale_imaging_4d_thick_cathode` · `aminchiang2016_nmc_electronic_ionic_transport_vs_li` 의
  "Wang 2018 = 5 × 10⁻⁵" 귀속에 정정 주석 — **사용자 비준 (09-26) → canon d1e64f0a1** (본문 불변, 맨 위 주석만).
- [x] SI 그림 생성 (09-26 — ④-2).
- [x] DEM 접촉망 σ_AM 50 mS/cm (이 표의 1.0 × 10⁻² 와 **다른 솔버의 다른 값**) — 비준 A (09-26): 값 유지 · 라벨 정정 · 원장 CL-92 + 인용 금지 5.
- [ ] 각주 · Methods 문장 · SI 그림을 사용자 docx 에 반영.  리포 `build.js` 는 08-23 판이라 라벨 동기화 필요 여부는 사용자 판단.
- [x] 원고 생성기 메모 D14 정정 (모델 입력값 5 × 10⁻⁵ 를 "문헌 두 출처의 NMC bulk" 로 적은 것) — 이 커밋.

## 2. LPSCl Poisson's ratio (DEM contact) — 0.3 · `Assumed` · ⏳ 판정은 §7 #6

## 3. VGCF fiber diameter — 0.15 µm · `Measured` · ⬜ (이종기술 SEM 원본 대기) · 판정은 §7 #11

## 4. VGCF Young's modulus — 10 GPa · `Assumed` · ✅ 정리됨 (09-25 민감도 판정 h0) — 원고 반영 비준 대기

**코멘트**: *"young's modulus 도 그냥 assumed?"*

**결론**: `Assumed` 가 맞다 — 측정·문헌 앵커가 없는 모델 입력이다.  대신 **이 값이 결과를 안 움직인다는 것을 오늘 런으로 보였다** (사전등록 판정 h0).

### ① 사실
- 원장 `CL-42` (`ADD_E_SET_20260818`): 사용자 지정 · 근거 문헌/측정 미기재.  MPM 압밀에서 섬유 재료점의 Lamé 상수 · CFL dt 가드에만 들어가고
  STEP3 σ 에는 기하를 거쳐서만 들어간다.  생산 침대는 dilation + buckle 모드라 두께는 dilation 이 정한다.
- 문헌 단섬유 탄성계수는 180–245 GPa (Ozkan 2010, Carbon 48, 239 — 웹 검색 기준, PDF 미확인) 로 우리 값의 약 20 배다.

### ② 이미 돌린 런 — VGCF E 민감도 3 팔 (사전등록 `docs/reviews/vgcf_e_sensitivity_prereg_20260925.md` · 원자료 `docs/data/vgcf_e_sensitivity_20260925/`)
| E_VGCF | porosity (%) | 두께 (µm) | σ_e (mS cm⁻¹) |
|---|---|---|---|
| 1 GPa | 14.749 | 121.669 | 59.274 |
| **10 GPa (생산)** | **14.889** | **121.869** | **59.154** |
| 100 GPa | 14.929 | 121.926 | 59.303 |
- 판정선 (런 전 등록): 1 ↔ 100 GPa 에서 |Δε| ≤ 0.3 %p **그리고** |Δσ_e / σ_e(10)| ≤ 2 %.  실측 **0.18 %p · 0.05 %** (팔마다 E=10 대비 ≤ 0.25 %) ⇒ **h0**.
- E=10 재압밀이 생산 침대 (Phase A 09-14 재생성) 와 인쇄 자릿수까지 같다 — 같은 코드 · 같은 입력 재현 확인.
- 한정어: 한 침대 · origin 1 팔 (위상 산포 0.68 % > 팔 간 차이) · 시험 범위 1–100 GPa (문헌 180–245 GPa 는 범위 밖) · E=100 은 CFL 로 dt 가 달랐다.

### ③ 논문 형식 수정안
1. **Table S2 행**: `Young's modulus · 10 · GPa · Assumedᵇ`
   > ᵇ Effective modulus assigned to the sub-grid fibre material points in the MPM compaction.  Varying it from 1 to 100 GPa changed the
   > compacted porosity by 0.18 %p and the electronic conductivity by ≤ 0.25 % (Supplementary Table S(new)).
   - 문헌 단섬유값 (180–245 GPa) 을 각주에 넣으려면 Ozkan 2010 PDF 확인 뒤에 — 넣으면 *"above the tested range"* 를 같이 적는다.
2. **Supplementary Table (신설)**: 위 3 팔 표 (porosity · 두께 · σ_e) + 한정어 캡션.

### ④ 답변 초안 (강준희에게)
> 응 assumed 가 맞아 — 문헌 단섬유값 (~200 GPa) 을 쓴 것도 아니고 잰 것도 아니야. 대신 오늘 민감도를 돌렸어: VGCF E 를 1 / 10 / 100 GPa 로
> 바꿔서 같은 전극을 다시 압밀하고 전자전도도까지 계산했더니 porosity 는 0.18 %p, σ_e 는 0.25 % 이내로만 움직였어 (런 전에 정한 기준
> 0.3 %p · 2 % 안). 그래서 결과가 이 값에 안 걸린다는 걸 각주랑 SI 표로 붙일게.

### ⑤ 남은 일
- [ ] 원고 반영 (Table S2 각주 ᵇ · SI 표) — 사용자 비준 뒤 docx 에.
- [ ] Ozkan 2010 PDF 확인 → 정본 카드 (각주에 문헌값을 넣을 경우).
- [ ] 원장 `SELF-50` (metrics `dt` 가 요청값) — 결과 해석에는 영향 없음, 코드 수정은 비준 뒤.

## 5. VGCF electronic conductivity (compressed powder) — 1.0 × 10² S cm⁻¹ · `Assumed` · ⏳ 판정은 §7 #13

## 6. VGCF electronic conductivity (voxel, diameter-preserving) — 78.5 S cm⁻¹ · `Calculated` · ⏳ 판정은 §7 #14

## 7. 표 전체 재검토 — 사용자 docx 판 14 행 · 참고문헌 무결성 (09-25 밤) · ⏳ 저자 결정 대기

> 계기: 준희 — *"NCM811 Young's modulus 의 source 로 넣은 reference 가 검색해도 안 나온다"* (사용자 전달, docx Table S2 화면).
> 확인 결과 **그 인용은 실재가 확인되지 않는다** — 이 리포의 자동 작성 커밋이 만든 인용이다 (7-1).  그래서 동그라미 6 행만이 아니라
> **표 14 행 전부**를 원문 카드 · 코드와 다시 대조했다.
> 표기: ✅ = 원문 PDF 카드 또는 코드와 대조함 · ⚠ = 대조 못 함 (**미확인 — 인용 전에 확인 필요**).
> 가정: docx 의 `Ref. S4` = 생성기 `[S6]` ("Wang 2020, JPS 470, 228413" — 인용 금지, `CL-90`), `Ref. S5` = 생성기 `[S8]` (Cronau 2021).  번호 체계가 다르므로
> (§0) docx 참고문헌 목록으로 확인할 것.

### 7-1. S4 인용은 어떻게 생겼나 (리포 이력 — 전부 이 리포의 자동 작성 커밋)
1. 04-29 `b1c8262fe` · `0a040f2b0` — 균열 모듈 (`scripts/fracture_model.py`) 과 문헌표 주석에 *"Wang 2020, J. Power Sources 470, 228413 —
   NCM **hardness**"* 가 **출처 확인 없이** 들어갔다 (이 절의 서지는 전부 인용 금지 — `CL-90`).  같은 코드에서 E_AM = 140 GPa 의 출처는 *"Xu 2017 / project-wide convention"* 이었다.
2. 05-04 `bd4d6fe0b` — `docs/Tabor_framework_reference.md` 참고문헌표로 옮기며 역할이 *"NCM E_AM = 140 GPa"* 로 **바뀌었다**.
3. 08-23 `c2670de6e` — 원고 SI 표 초안: `[36] H. Wang, et al., J. Power Sources 2020, 470, 228413` 을 E = 140 의 출처로 (인용 금지).
4. 08-24 `9aa882135` — S6 으로 번호를 바꾸며 제목 *"Elastic properties of layered lithium transition-metal oxides"* 를 **붙였다** — 원문을 본 적이 없다 (지어진 제목 — 인용 금지).
- 검증 (인용 금지 — `CL-90`): 그 제목·저자의 논문은 웹 검색에 나오지 않는다.  DOI `10.1016/j.jpowsour.2020.228413` 은 이 컨테이너에서 해석할 수 없다 (doi.org ·
  Crossref · ScienceDirect 차단) — 그 번호가 어느 논문인지는 **미확인**이지만 어느 쪽이든 교체 대상이다.
- 같은 04-29 목록의 다른 서지도 미확인이다 (예: *"Xu 2017 PRX 7, 041038"* — 실제 Xu 2017 은 *J. Electrochem. Soc.* **164**, A3333).
- ⚠⚠ **"Wang 2020" 은 이미 세 가지 다른 값의 출처로 퍼져 있다** (09-25 밤 전수 grep — litdb 제외) — 한 논문이 NCM 경도 · NCM 영률 ·
  LPSCl 영률을 모두 줄 리 없으므로 **지어진 인용이라는 강한 신호**다:
  - NCM 경도 6.0 GPa — `scripts/fracture_model.py` · `scripts/build_literature_reference.py` (웹앱 문헌 CSV 의 `source` 열)
  - NCM 영률 140 GPa — `docs/Tabor_framework_reference.md` 참고문헌표 · 원고 생성기 `docs/manuscript_draft/build.js` S6
  - **LPSCl 영률 24 GPa** — `scripts/analyze_tabor_regime.py` 주석 · `docs/Tabor_framework_reference.md` · `docs/Reviewer_Defence_Notes.md`
    (*"LPSCl 의 진짜 lab 값 (Wang 2020 nanoindentation)"*) · `docs/paper_brittle_caveat.md` · 웹앱 `webapp/templates/single.html` 배지 툴팁
    (사용자에게 보이는 자리)
  ⇒ 원고 밖에도 **반박 대응 노트 · 논문 초고 · 웹앱 UI** 에 남아 있다.  고치는 것은 7-4 의 내부 서지 점검 (비준 뒤) 에서 한 번에.
- 원장 `SELF-51`.

### 7-2. 행별 판정

| # | 행 | 값 | docx 라벨 | 판정 | 조치 |
|---|---|---|---|---|---|
| 1 | NCM811 입자 반지름 | 2.5 µm | Experimental value | ⚠ 출처 기록이 리포에 없다 (본문: *"sized after the experimental powders"*) | 측정 방법 · D50 확인 → 측정이면 `Measured` 로 #4 와 통일, 공급사 값이면 `Supplier data`.  D14 (원고의 다결정 기술 ↔ 침대의 AM_S 클래스) 와 함께 |
| 2 | NCM811 영률 | 140 GPa | Ref. S4 | ⛔ **인용 불성립** (7-1).  값 140 은 측정 범위 안 | **교체 문헌 (사용자 제공 서지, 09-25)**: T. Sedlatschek *et al.*, *Characterization of the grain boundary strength of polycrystalline NMC811 using in situ micro tensile tests*, *J. Power Sources* **681** (2026) 240276 — 다결정 NMC811 나노압입 E = 138 ± 24 GPa (압입 29 회).  ✅ **PDF 확인 (09-25 밤 — 정본 카드 `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile`, canon `7d23f44d9`)**: 138 ± 24 GPa · ν 0.32 **가정** · 인장 165 ± 7 GPa (n = 3).  ✅ **표는 *140 GPa · Ref. S4* 로 충분하다** (사용자 결정 09-25 밤 — *"모델로 140 을 채택했으면 140 이라 적고 그 reference 를 넣으면 된다"*): 140 은 측정값 138 ± 24 (평균의 95 % 구간 129–147) 안이고 접촉 강성 E/(1−ν²) 차도 3 % 안이다.  ~~표에 "140 GPa (Ref. S4)" 처럼 쓰지 않는다~~ (내 과한 제한 — 철회).  측정값 병기 (§8-2 ᶠ) 는 선택.  같은 부류: NMC532 2차입자 142.5 ± 11.3 GPa (Xu 2017, JES 164, A3333 — canon `eef51c83b`) |
| 3 | NCM811 σ_e | 1.0 × 10⁻² S cm⁻¹ | Assumed | ✅ §1 (Wang 2018 원문 · Amin & Chiang 정본 카드) | `Assumed` 유지 + 각주 ᵃ — 결정 A/B 대기 |
| 4 | LPSCl 입자 반지름 | 0.5 µm | Measured | ⚠ 출처 기록이 리포에 없다 | #1 과 같다 |
| 5 | LPSCl 영률 (DEM 접촉) | 1.35 GPa | Calibrated | ✅ 보정값 (`docs/esse_calibration_2mAh_real_9.md`) | 각주에 보정 표적.  ⚠ docx 에서 `E (dense) 24 GPa` 행이 빠졌다 — 09-01 시트 §3-1 은 *"둘 다 남긴다 (지우면 연화 배수를 감춘다)"* 였다.  되살린다면 출처를 LPSCl 값으로 (Sakuda 2013 의 24 GPa 는 **75Li₂S·25P₂S₅ 유리**).  본문 *"(24 GPa)[34] is listed beside it in Table S2"* 도 표와 맞출 것 |
| 6 | LPSCl ν (DEM 접촉) | 0.3 | Assumed | ✅ `Assumed` 가 맞다 — DEM 관례 입력 (LIGGGHTS `poissonsRatio` SE 0.30) | 각주: LPSCl 참고값 ≈ 0.33–0.37 (우리 DFT E_VRH·B₀ 쌍 → 0.360 · 문헌 DEM **입력** 0.33 / 0.37 — 측정 아님).  ν 는 Hertz 강성 E* = E/(1−ν²) 로 2 차로만 들어가고 (0.30 → 0.36: +4 %) E 1.35 가 이 ν 로 보정됐다.  ⚠ 진행 파일의 *"= Ref. (…)"* 메모는 모델 입력값을 측정처럼 묶은 것 — 쓰지 않는다.  ⊕ **NCM811 ν = 0.25** (DEM 입력) 행이 표에 없다 → 추가 (`Assumed`) |
| 7 | LPSCl 영률 (MPM) | 1.53 GPa | Calibrated | ✅ 2D 보정값 (SEM 형태 + 순수 SE 다공도 — `docs/mpm3d_calibration.md`) | 각주에 보정 표적 |
| 8 | LPSCl ν (MPM) | 0.49 | Calibrated | △ **무엇에** 맞췄는지가 빠졌다 — 체적탄성률 K = E/[3(1−2ν)] = 25.5 GPa 를 DFT B₀ 26.2 GPa 에 맞춘 선택 (+ ν 스윕: 0.45 → 0 % 과압축 · 0.49 → 6.3 %) | 각주: *"chosen so that the bulk modulus (25.5 GPa) matches the DFT value (26.2 GPa) while the shear modulus stays soft"* |
| 9 | 항복강도 | 0.30 GPa | Calibrated | ✅ 순수 SE σ_y 스윕 (0.15 → 5.6 · 0.20 → 6.7 · 0.25 → 9.0 · **0.30 → 10.0 %**) — 표적 ~10 % @ 300 MPa | 각주: 표적은 LPSCl 직접 측정이 아니라 문헌 유도값 (본문과 같은 한정어) · 문헌 범위 0.05–0.30 GPa 의 상단.  ⚠ 이 보정 (06-16, servo · settled) 에 이후 플래튼 정지 논의 (`fam_platen_prereg_20260812`) 가 미치는 영향은 이 검토에서 보지 않았다 |
| 10 | LPSCl σ_ion | 3.0 × 10⁻³ S cm⁻¹ | Ref. S5 | ~~⛔ 오귀속 — 3.0 이라는 숫자가 없다 · 측정한 argyrodite 는 Li₆PS₅Br~~ (09-25 밤 **철회** — 정본 카드가 본문만 읽은 거짓 음성이었다, `CL-91`).  ✅ **값은 지지된다 — 다른 양**: Ref. S5 의 **SI 그림 S2c** = µC-Li₆PS₅Cl 펠릿, 적층압 ≥146 MPa 평탄 2.88–3.46 mS cm⁻¹ (그림 판독 · 저자 신뢰조건 곡선 3.06–3.23) → 3.0 은 그 하단.  틀린 것은 *단결정* 라벨뿐 (정본 카드 SI 보강 canon `729818f95`) | `Ref. S5` **유지** + 각주 (§8-2 문안): 펠릿 · 적층압 조건 · 연구실 간 산포 (한 배치 8 개 연구실 0.44–2.98 mS cm⁻¹ — Ohno 2020 SI Table S11, canon `ae22bf37b`).  행 이름에 *(grain interior)* 를 쓰지 않는다.  복셀 솔버 한정어 (`CL-81`) 는 *입력이 이미 펠릿값* 이라는 점과 함께 (CLAUDE.md §CL-81 정정) |
| 11 | VGCF 직경 | 0.15 µm | Measured | ⚠ 측정 원자료가 리포에 없다 (§3 — 이종기술 SEM 원본 대기).  생성기 판 라벨은 `Supplier data` | SEM 원자료 (n · 평균 ± SD) 가 오면 `Measured (SEM)`, 아니면 `Supplier data (VGCF-H, 150 nm)` — 증빙과 같이 |
| 12 | VGCF 영률 | 10 GPa | Assumed | ✅ §4 (민감도 h0, 1–100 GPa) | `Assumed` + 각주 ᵇ |
| 13 | VGCF σ_e (압착 분말) | 1.0 × 10² S cm⁻¹ | Assumed | ✅ `Assumed` 가 맞다 — 09-01 시트 §3-1 R20 처분과 같다: 100 은 공급사 분말값 83 에서 **유도되지 않았다** (도입 커밋 `087d1a07` 의 order-of-magnitude hook — 83 감사보다 먼저) | ⛔ 각주에 *"83 을 반올림"* 이라 쓰지 말 것 (없던 근거를 만드는 것).  각주: 공급사 단섬유 10⁴ · 압착 분말 83 S cm⁻¹ (⚠ 카탈로그 원본이 리포에 없다) · 유효 망 계수 · 미보정.  행 이름 *"(compressed powder)"* 는 값이 분말 측정인 것처럼 읽힌다 → *"(effective network coefficient)"* |
| 14 | VGCF σ_e (복셀) | 78.5 S cm⁻¹ | Calculated | ✅ 계산 맞음: σ·πd²/(4h²), d = h = 0.15 µm → 100·π/4 = 78.54 (`scripts/step3_sigma.py` 1153 행 `diameter_preserving_sigma`) | 재료 파라미터가 아니라 **격자 환산값** (h = 0.125 이면 113.1) → 09-01 권고대로 표에서 빼고 Methods 식으로.  남긴다면 `Calculated (Eq. Sx, h = 0.15 µm)` |

### 7-3. 요약
- ⛔ 고칠 것 1 — #2 (S4 인용 불성립 → Sedlatschek 2026 교체, 값은 측정값 병기).  △ #10 (S5) 은 **값이 SI 그림 S2c 로 지지되고 각주만** 단다.
  ~~표에 남은 `Ref.` 두 개가 둘 다 틀렸다~~ (09-25 밤 철회 — S5 판정은 SI 를 안 본 거짓 음성이었다, `CL-91`).
- ⚠ 저자 측 자료 확인 3 — #1 · #4 (입자 반지름) · #11 (VGCF 직경).
- △ 각주 보강 5 — #5 · #7 · #8 · #9 (보정 표적) · #6 (ν 참고범위 + NCM811 ν 행 추가).
- ✅ 라벨 유지 4 — #3 · #12 · #13 · #14 (각주 · 위치만).
- 본문 확인 1 — *"(24 GPa)[34] is listed beside it in Table S2"* 가 표와 맞는지.
- 동그라미 6 행 (#3 · #6 · #11 · #12 · #13 · #14) 중 라벨이 **틀린** 것은 없다 — #11 만 증빙이 없다.  **틀린 것은 동그라미 밖의 S4 한 행이다**
  (S5 는 각주 보강 — 위 철회 참조).

### 7-4. 재발 방지 — 비준 (09-25 밤 *"ㅇㅇ 고치고"*) · 진행 상태
1. **원고 참고문헌 게이트** — 원고 (생성기 · docx 에서 뽑은 목록) 의 인용마다 원문을 확인한 litdb 정본 카드 (DOI) 에 연결하고, 연결 안 된
   인용이 있으면 `check_all.sh` 가 실패한다.
2. **내부 서지 점검** — 코드 주석 · docs 의 서지 (특히 04-29 균열 모듈 목록) 를 훑어 카드 없는 것에 `미확인` 표시.
3. **작성 규율** — 원문을 보지 않은 서지는 제목 · 권호를 채우지 않고 `[미확인]` 으로 둔다.  CLAUDE.md 에 한 줄로 상주시킨다
   (세션이 바뀌어도 남도록).
- 진행 (09-25 밤):
  - ✅ **등록부** — `claims.json` `CL-90` + `quotation_ban` 두 패턴 (그 인용의 논문 번호 · 지어진 제목).  스윕이 기록 문서 속 언급까지
    잡는 것을 확인했고, 기록 줄에는 *인용 금지* 표지를 달았다.
  - ✅ **"Wang 2020" 9 곳 정정** — 코드 주석 3 (`scripts/fracture_model.py` · `scripts/build_literature_reference.py` ·
    `scripts/analyze_tabor_regime.py`) · docs 3 (`docs/Tabor_framework_reference.md` · `docs/Reviewer_Defence_Notes.md` ·
    `docs/paper_brittle_caveat.md`) · 웹앱 툴팁 (`webapp/templates/single.html`) · 원고 생성기 S6 → Sedlatschek 2026 · S8 행 `Assumed`.
    **값은 하나도 바꾸지 않았다** — 출처 표기만.  24 GPa 는 LPSCl 측정이 아니라 Li₂S–P₂S₅ 유리 값으로 적었다.
  - ✅ **CLAUDE.md 작업 규율 ⑥** 상주.
  - ⬜ **원고 참고문헌 ↔ 정본 카드 게이트** — 설계 필요 (생성기만 보면 docx 를 못 본다 = 규율 ⑤ 의 부분집합 초록 위험).
  - ⬜ **다른 미확인 서지** — 같은 04-29 목록의 *"Xu 2017"* 범위값 · *"Cheng 2017"* · LPSCl 경도 0.85 GPa 의 *"Sakuda 2013"* 귀속 (그 논문은
    Li₂S–P₂S₅ 유리) — 전수 점검은 게이트와 함께.
  - ⬜ **사용자 docx** — S4 교체 · S5 각주는 사용자 원고에서 (생성기는 08-23 판) — 붙여 넣을 문안 = §8-2.
  - ✅ **09-25 밤 재정정 (SELF-51 3단계 · `CL-91`)** — 논문 에이전트 7 편 원문 대조 (Cronau 2021 SI · Cronau 2022 · Sedlatschek 2026 ·
    Xu 2017 · Ketter 2025 · Endo 2001 · Ohno 2020 SI).  S5 *"3.0 없음"* 판정 철회 · σ_grain 라벨을 *"SI 그림 S2c µC 펠릿 평탄 하단"* 으로
    코드 · 웹앱 · 문서 전역 정정 (값 불변) · *단결정* 라벨을 인용 금지 등록부에 올림 · Cronau(r_SE) = 출처 없는 모델 가정 (구간값이
    Cronau 2022 원문에 없다).

## 8. 준희 1차 요청 4 건 — 최종안 (09-25 밤, *"얘네만 해결해줘 일단"*) · ⏳ 사용자 확인 뒤 docx 반영

> 범위: NCM σ_e · LPSCl ν · VGCF E · VGCF σ_e.  근거는 §1 · §4 · §7 에 있고 여기는 **붙여 넣을 문안**만 둔다.  수치 인용은 원문 확인분만
> (규율 ⑥).  ✅ 09-25 밤 논문 에이전트 원문 대조로 ᵃ · ᶜ · ᵈ 의 문헌값이 확인됐다 (Ketter 2025 · Deng 2016 · Endo 2001 — 정본 카드).
> VGCF-H 공급사 데이터시트는 **없어도 된다** (Endo 2001 로 대체 — 단 그 논문에 *VGCF-H* 라는 이름은 없다).  첫 질문 (S4) 과 S5 문안 = §8-2.

| 행 | 값 | 라벨 (최종) | 각주 |
|---|---|---|---|
| NCM811 electronic conductivity | 1.0 × 10⁻² S cm⁻¹ | `Assumed`ᵃ | ᵃ (§1 ④ 판 — Amin & Chiang 2016 · Wang 2018 · CL-70 민감도) + ᵃ⁺ 두 문장 (아래) |
| LPSCl Poisson's ratio (DEM contact) | 0.3 | `Assumed`ᶜ | ᶜ 아래 |
| VGCF Young's modulus | 10 GPa | `Assumed`ᵇ | ᵇ (§4 ③ 판 그대로 — 1 / 10 / 100 GPa 민감도) |
| VGCF electronic conductivity — 행 이름 *(compressed powder)* → ***(effective, fibre network)*** | 1.0 × 10² S cm⁻¹ | `Assumed`ᵈ | ᵈ 아래 |
| VGCF electronic conductivity (voxel, diameter-preserving) | 78.5 S cm⁻¹ | `Calculated`ᵉ | ᵉ 아래 (또는 행을 빼고 Methods 식으로 — 09-01 시트 §3-1 권고) |

> ᵃ⁺ (§1 ④ 판 뒤에 붙이는 두 문장) A second measured value, 5.22 mS cm⁻¹ for NCM83 by DC polarization (Ketter et al., Nat. Commun.
> 2025, SI), is of the same order.  Because the electron network in these electrodes is carried by the carbon additives, lowering
> σ_NCM thirty-fold changes the DBE/SBE electronic-conductivity ratio only from 1.31 to 1.34.
>
> ᶜ Conventional value for the DEM contact model.  The Poisson's ratio enters the Hertzian contact stiffness only through
> E* = E/(1 − ν²) (a 5 % change between 0.30 and the first-principles value 0.37 for Li₆PS₅Cl; Z. Deng et al., J. Electrochem. Soc.
> 163 (2016) A67), and the DEM contact modulus (1.35 GPa) was calibrated with ν = 0.3, so a different choice is absorbed by the
> calibrated modulus.
>
> ᵈ Effective conductivity assigned to the VGCF phase in the voxel model; not calibrated.  Because the voxel model merges touching
> fibres, this value represents the fibre network including fibre–fibre contact losses rather than a single fibre; for reference,
> a single graphitized (2800 °C) submicron vapour-grown carbon fibre has a longitudinal resistivity of 1 × 10⁻⁴ Ω cm (≈10⁴ S cm⁻¹),
> and the same fibres compressed to 0.8 g cm⁻³ about 0.012 Ω cm (≈80 S cm⁻¹) (M. Endo et al., Carbon 39 (2001) 1287; the powder
> value is read from its Fig. 7).
>
> ᵉ σ_voxel = σ·πd²/(4h²) with the fibre diameter d = 0.15 µm and the voxel edge h = 0.15 µm, so that a fibre rendered one voxel wide
> carries the axial conductance of a 0.15 µm fibre.

- ⛔ ᵈ 에 *"83 을 반올림했다 / 압착 분말값을 썼다"* 라고 쓰지 않는다 — 100 은 83 감사보다 먼저 들어온 값이다 (09-01 시트 R20).
- ⚠ VGCF σ 의 민감도는 **현행 규약으로 잰 것이 없다** — 옛 침대 (08-12, CL-39) 에서 ×1.44 에 DBE/SBE 비가 −0.3 % 움직인 것뿐이고,
  공급사 밴드 [83, 10⁴] 전체를 보는 프로브 `CL-48` 은 **등록만 되고 미실행**이다.  준희가 방어를 더 원하면 CL-48 을 돌린다 (GPU, 짧다).
- ν 행: 원고의 DFT 절은 흡착에너지만 다뤄 LPSCl 탄성상수가 없다.  문헌 DFT (Deng et al., JES 2016) 는 **원문 확인 완료** (Table III:
  E 22.1 · G 8.1 · B 28.7 GPa · **ν 0.37**, PBEsol — 정본 카드 `deng2016_elastic_superionic_electrolytes_dft`) → ᶜ 에 넣었다.
  ⊕ DEM 입력 NCM811 ν = 0.25 행도 표에 넣는 것을 권한다 (`Assumed`) — ⛔ 출처를 *Xu 2017* 로 달지 말 것 (그 논문은 ν 를 재지 않고 0.3 으로
  **가정**했다).
- ᵈ: ⛔ *VGCF-H* 이름으로 Endo 2001 을 인용하지 않는다 (그 논문에 그 이름이 없고 섬유 지름도 0.2 µm) · *≈80* 을 쓰고 *83* 은 쓰지 않는다
  (그림 판독값보다 자릿수가 많다) · 100 은 이 값들에서 **유도되지 않았다** (*coincides with* 까지만).
- ᵇ (선택): *"Reported tensile moduli of vapour-grown carbon fibres are of order 10² GPa (≈110–310 GPa; Endo et al. 2001, Fig. 6),
  above the tested range."* — 넣으면 민감도 범위 (1–100 GPa) 밖이라는 점까지 같이 적힌다.

**준희에게 보낼 답 (초안)**
> 1) NCM σ_e 1e-2: Assumed 유지. 문헌값을 가져온 게 아니라 모델 유효값이야. NCM811 pristine 실측은 4.1e-3 (Wang 2018, DC 분극),
>    NCM83 은 5.22e-3 (Ketter 2025, DC) 이고,
>    NMC 전자전도도는 조성·충전상태·연구실에 따라 5e-8~1.4e-2 로 흔들려서 단일 Ref 로 달 값이 없어. 각주에 문헌 범위 + Wang 값 +
>    민감도 (σ_NCM 을 ÷30~×30 해도 DBE > SBE · ÷30 이면 비가 1.31 → 1.34 로 거의 그대로) 를 달게.
> 2) LPSCl ν 0.3: Assumed 가 맞아. DEM 접촉모델 관례값이고 E* = E/(1−ν²) 로만 들어가서 LPSCl DFT 값 0.37 (Deng 2016) 과도 5 % 차이인데, DEM 탄성률
>    (1.35 GPa) 을 이 ν 로 보정했기 때문에 그 차이는 보정값에 흡수돼. 각주로 달게.
> 3) VGCF E 10 GPa: Assumed 유지. 1 / 10 / 100 GPa 로 바꿔 전극을 다시 압밀하고 전자전도도까지 계산했더니 porosity 0.18 %p,
>    σ_e 0.25 % 안에서만 움직였어 (런 전에 정한 기준 안). 각주 + SI 표로 붙일게.
> 4) VGCF σ_e: 100 S/cm 은 Assumed — 섬유 하나의 값이 아니라 접촉 손실을 포함한 섬유망 유효값이야 (문헌: 흑연화 단섬유 ~1e4,
>    0.8 g/cm³ 로 누른 분말 ~80 S/cm — Endo 2001). 행 이름 "compressed powder" 는 오해 소지가 있어서 "effective, fibre network" 로 바꿀게.
>    78.5 는 그 100 을 복셀 한 칸 굵기로 그린 섬유에 맞게 환산한 계산값 (σ·πd²/4h²) 이라 Calculated 가 맞고, 식은 Methods 에 적을게.

### 8-2. 첫 질문 (S4 — NCM811 E) · S5 (LPSCl σ_ion) — 최종 문안 (09-25 밤, 원문 확인 뒤)

| 행 | 값 | Source (최종) | 각주 |
|---|---|---|---|
| NCM811 Young's modulus | 140 GPa | `Ref. S4` (S4 = Sedlatschek 2026 으로 교체) | 없어도 된다 — ᶠ 는 측정값을 보여 주고 싶을 때만 (선택) |
| LPSCl ionic conductivity | 3.0 × 10⁻³ S cm⁻¹ | `Ref. S5`ᵍ (유지) | ᵍ 아래 — 행 이름에 *(grain interior)* 를 쓰지 않는다 |

> ᶠ (선택) DEM input.  Nanoindentation of polycrystalline NCM811 gave 138 ± 24 GPa (n = 29; ν = 0.32 assumed) [S4: T. Sedlatschek et al.,
> J. Power Sources 681 (2026) 240276]; pristine NMC532 secondary particles gave 142.5 ± 11.3 GPa [R. Xu et al., J. Electrochem. Soc.
> 164 (2017) A3333].
>
> ᵍ Lower end of the plateau measured for microcrystalline Li₆PS₅Cl pellets under ≥146 MPa stack pressure (2.9–3.5 mS cm⁻¹, read from
> SI Fig. S2c of Ref. S5) — a grain-boundary-inclusive pellet value, not a single-crystal value.  An inter-laboratory study of one
> Li₆PS₅Cl batch reported 0.44–2.98 mS cm⁻¹ at room temperature (Ohno et al., ACS Energy Lett. 2020).

- ✅ 표는 *140 GPa · Ref. S4* 로 충분하다 (사용자 결정 09-25 밤) — 140 은 측정값 138 ± 24 (평균의 95 % 구간 129–147) 안이다.
  ~~ᶠ 에 "140 GPa (Sedlatschek 2026)" 처럼 쓰지 않는다~~ (과한 제한이라 철회 — S5 사고는 *없는 인용* · *다른 양 (단결정)* 이었고, 이번은
  실재하는 논문이 같은 양을 재서 그 범위 안에 있는 경우다).
- ᵍ 의 Ohno 2020 은 **SI 만** 확인했다 — 권·쪽은 원문 미확인 (DOI 접미 `9b02764` 는 SI 파일명과 일치).  빼도 ᵍ 는 선다.
- 준희에게 (초안): *"S4 는 우리 쪽 코드 주석에서 원문 확인 없이 생긴 인용이 표까지 퍼진 거였어 — 미안. Sedlatschek 2026 (다결정 NCM811
  나노압입 138 ± 24 GPa) 으로 바꿀게 — 140 은 그 측정 범위 안이라 값은 그대로 둬. S5 (Cronau 2021) 는 3.0 이 본문이 아니라 SI 그림 S2c 에 있어서 검색에 안 걸린
  거였고, 단결정이 아니라 고압 펠릿값이라 조건을 각주로 달게."*

## 9. 종합 회신 (09-26, *"준희 얘기 대응하자 다 종합해서"*) — 표 S2 전 행 · Methods 두 문장 · 참고문헌 · 뿌리 감사 중 원고에 걸린 것

> **이 절이 붙여 넣을 최종판이다.**  근거는 §1–§8-2 (행별) 와 원장 `SELF-51` (뿌리 감사).  §8 · §8-2 의 각주 글자 (ᵃ–ᵍ) 는 작업용이었고, 9-1 은
> **표 행 순서로 다시 붙인** 최종 글자다 (대응: §8-2 ᶠ → ᵃ · §8 ᵃ(+ᵃ⁺) → ᵇ · §8 ᶜ → ᵈ · §8-2 ᵍ → ᶠ · §4 ③ ᵇ → ᵍ · §8 ᵈ → ʰ · §8 ᵉ → ⁱ · 새것 ᶜ · ᵉ).
> 09-26 에 더한 것: ① 보정 행 (#5 · #7 · #9) 각주 — 보정 표적 *"순수 LPSCl ≈10 % @300 MPa"* 는 **어느 문헌의 값도 아니다** (감사 A ④ · C ①) →
> 모델 표적이라고 적고 문헌 실측 폭을 붙인다.  ② Methods 두 문장 — `[9]` 는 그 수치를 담지 않고, `(24 GPa)[34]` 는 Li₂S–P₂S₅ **유리** 값인데 docx
> 표에는 그 행이 없다.  ③ 새 SI 참고문헌 서지는 전부 정본 카드 (원문 PDF) 에서 가져왔다 — 기억 · 검색 요약으로 채운 칸 없음 (규율 ⑥).
> 09-26 원문 재확인 (직접, pymupdf): Ohno 2020 SI Table S2 성형압 (A 380 · B 375 · C 370 · D 720 · E 325 등방 · F 275 · G 441 MPa) · Tables S3–S9
> 시료 (2) 상대밀도 (81 · 86 · 95 · 88/89 · 83 · 84 · 91 %) · Song 2025 본문 (*"the porosity was estimated to be 13% ± 2%"* · 360 MPa 단축 압착 뒤 60 °C
> 2 h · *"4.7 ± 1.1 GPa"* · 서지 쪽) · Böger 2023 SI 그림 S10 · S11 (κ — 표에는 안 들어감).  권호는 정본 카드 (Sedlatschek · Xu · Deng · Endo · Wang ·
> Amin & Chiang · Ketter · Cronau 2021).
> ✅ 원고 참고문헌 **전수** 대조 (감사 G — build.js 7/7 · 코저자 docx · 세미나 덱 · main.tex 50/50) 끝 → 9-4.  사용자 docx 원본은 리포에 없어
> 09-03 통독 기록으로 보이는 부분만 판정했다 (9-2 (4) 의 각주 ※ 가 그렇게 잡혔다).

### 9-1. 표 S2 — 최종 (docx 14 행 + 권고 1 행)

| # | Parameter | Value | Source | 상태 |
|---|---|---|---|---|
| 1 | NCM811 particle radius | 2.5 µm | Experimental value | ⬜ 저자 — 측정이면 `Measured` (#4 와 통일), 공급사 D50 이면 `Supplier data` |
| 2 | NCM811 Young's modulus | 140 GPa | Ref. S4ᵃ (S4 = Sedlatschek 2026 으로 교체) | ✅ (ᵃ 는 선택) |
| ⊕ | NCM811 Poisson's ratio (DEM contact) | 0.25 | Assumed | 권고 — DEM 입력 (`dem_scripts/case09_*.liggghts`).  출처를 Xu 2017 로 달지 말 것 (그 논문은 0.3 **가정**).  원출처 1순위 후보 = Sharma 2023 **NMC622** 단결정 C_ij 의 VRH ν 0.253 (09-26 원문 확인 — 조성이 달라 `Ref.` 가 아니라 `Assumed` + ᵃ 의 선택 문장) |
| 3 | NCM811 electronic conductivity | 1.0 × 10⁻² S cm⁻¹ | Assumedᵇ | ✅ |
| 4 | LPSCl particle radius | 0.5 µm | Measured | ⬜ 저자 (#1 과 같이) |
| 5 | LPSCl Young's modulus (DEM contact) | 1.35 GPa | Calibratedᶜ | ⏳ 보정 표적 문구 저자 확인 (9-5 ③) |
| 6 | LPSCl Poisson's ratio (DEM contact) | 0.3 | Assumedᵈ | ✅ |
| 7 | LPSCl Young's modulus (MPM continuum) | 1.53 GPa | Calibratedᶜ | ✅ |
| 8 | LPSCl Poisson's ratio (MPM continuum) | 0.49 | Calibratedᵉ | ✅ (근거값 선택 — 9-5 ②) |
| 9 | Yield strength | 0.30 GPa | Calibratedᶜ | ✅ |
| 10 | LPSCl ionic conductivity | 3.0 × 10⁻³ S cm⁻¹ | Ref. S5ᶠ | ✅ 행 이름에 *(grain interior)* 쓰지 않는다 |
| 11 | VGCF fiber diameter | 0.15 µm | Measured | ⬜ SEM 원자료 (n · 평균 ± SD) 가 있으면 `Measured (SEM)`, 없으면 `Supplier data` |
| 12 | VGCF Young's modulus | 10 GPa | Assumedᵍ | ✅ |
| 13 | VGCF electronic conductivity (effective, fibre network) | 1.0 × 10² S cm⁻¹ | Assumedʰ | ✅ 행 이름 변경 (*compressed powder* → *effective, fibre network*) |
| 14 | VGCF electronic conductivity (voxel, diameter-preserving) | 78.5 S cm⁻¹ | Calculatedⁱ | ✅ (또는 행을 빼고 Methods 식으로 — 09-01 권고) |

**각주 (붙여 넣을 문안)** — `S(…)` 는 SI 참고문헌 번호 자리 (9-3):

> ᵃ (optional) DEM input; nanoindentation of polycrystalline NCM811 gave 138 ± 24 GPa (n = 29; ν = 0.32 assumed) [S4].
> (optional addition) The Voigt–Reuss–Hill average of elastic constants measured on single-crystal NMC622 grains is 140.16 GPa with
> ν = 0.253 [S(Sharma)], the pair used for both NMC classes in the DEM.
>
> ᵇ Effective model input, not an intrinsic property of NCM811. Reported electronic conductivities of layered LiNiₓMnᵧCo_zO₂ range from
> 5 × 10⁻⁸ to 1.4 × 10⁻² S cm⁻¹ with composition and state of charge [S(Amin)] and differ by up to three orders of magnitude between studies of the
> same composition [S(Amin), S(Wang)]; for pristine NCM811, DC polarization gives 4.1 × 10⁻³ S cm⁻¹ at 20 °C [S(Wang)], and 5.22 × 10⁻³ S cm⁻¹ was
> reported for NCM83 [S(Ketter)]. The DBE > SBE ordering holds for σ_NCM from 3.3 × 10⁻⁴ to 0.30 S cm⁻¹ (thirty-fold either way); across this range
> the DBE/SBE ratio moves from 1.34 to 1.20 (1.31 at the value used), consistent with the electron network being carried mainly by the carbon
> additives (Supplementary Fig. S(new)).
>
> ᶜ Effective parameters of the particle models rather than intrinsic properties of LPSCl, chosen so that the compacted beds densify like
> cold-pressed sulfide powder at 300 MPa (model target ≈10 % porosity for pure LPSCl; see Methods). Reported porosities of cold-pressed Li₆PS₅Cl
> pellets are 5–19 % after pressing at 275–441 MPa across laboratories [S(Ohno)] and 13 ± 2 % after 360 MPa [S(Song)]. For comparison, the
> first-principles Young's modulus of Li₆PS₅Cl is 22.1 GPa [S(Deng)], and a cold-pressed pellet with 13 % porosity gives 4.7 ± 1.1 GPa in
> bending [S(Song)].
>
> ᵈ Conventional value for the DEM contact model. The Poisson's ratio enters the Hertzian contact stiffness only through E* = E/(1 − ν²)
> (a 5 % change between 0.30 and the first-principles value 0.37 for Li₆PS₅Cl [S(Deng)]), and the DEM contact modulus was calibrated with ν = 0.3,
> so a different choice is absorbed by the calibrated modulus.
>
> ᵉ Chosen together with the modulus so that the bulk modulus K = E/[3(1 − 2ν)] = 25.5 GPa stays close to the first-principles bulk modulus of
> Li₆PS₅Cl (28.7 GPa [S(Deng)]) while the shear modulus remains soft (0.51 GPa), confining the softening to shear.
>
> ᶠ Lower end of the plateau measured for microcrystalline Li₆PS₅Cl pellets under ≥146 MPa stack pressure (2.9–3.5 mS cm⁻¹, read from SI
> Fig. S2c of Ref. S5) — a grain-boundary-inclusive pellet value, not a single-crystal value. An inter-laboratory study of one Li₆PS₅Cl batch
> reported 0.44–2.98 mS cm⁻¹ at room temperature [S(Ohno)].
>
> ᵍ Effective modulus assigned to the sub-grid fibre material points in the MPM compaction. Varying it from 1 to 100 GPa changed the compacted
> porosity by 0.18 percentage points and the electronic conductivity by ≤ 0.25 % (Supplementary Table S(new)); reported tensile moduli of
> vapour-grown carbon fibres are of order 10² GPa [S(Endo)], above the tested range.
>
> ʰ Effective conductivity assigned to the VGCF phase in the voxel model; not calibrated. Because the voxel model merges touching fibres, this
> value represents the fibre network including fibre–fibre contact losses rather than a single fibre; for reference, a single graphitized
> (2800 °C) submicron vapour-grown carbon fibre has a longitudinal resistivity of 1 × 10⁻⁴ Ω cm (≈10⁴ S cm⁻¹), and the same fibres compressed
> to 0.8 g cm⁻³ about 0.012 Ω cm (≈80 S cm⁻¹) [S(Endo); the powder value is read from its Fig. 7].
>
> ⁱ σ_voxel = σ·πd²/(4h²) with the fibre diameter d = 0.15 µm and the voxel edge h = 0.15 µm, so that a fibre rendered one voxel wide carries
> the axial conductance of a 0.15 µm fibre.

- ᵉ 선택지: *"…close to first-principles values for Li₆PS₅Cl (26.2 GPa, this work; 28.7 GPa [S(Deng)])"* — 실제 보정 표적은 **우리 DFT B₀ 26.2**
  였다 (CLAUDE.md §3D MPM (2)).  *this work* 로 쓰려면 SI DFT 절에 B₀ 를 실어야 한다 (지금 DFT 절은 흡착에너지뿐).
- ᶜ 의 *"≈10 % … model target"* 은 MPM (σ_y 스윕) 에 대해서는 기록 그대로다.  DEM 1.35 의 실제 보정 표적은 9-5 ③ 에서 저자 확인.
- ⛔ 쓰지 않는 것: ᶜ 에 *"derived from (literature)"* · ᶠ 에 *single-crystal* 라벨 · ʰ 에 *"83"* · *VGCF-H* 이름으로 Endo 인용 (그 논문에 그
  이름이 없다) · ⊕ 행에 Xu 2017 의 ν.

### 9-2. Methods — 고칠 두 문장 (생성기 `build.js:141–148` 기준 — docx 에서 같은 문장을 찾아 바꿀 것)

**(1) 현재** — *"The 1.35 GPa value is an empirical contact-law input, not an intrinsic LPSCl modulus and not an independent validation of the
present beds; the dense-material value (24 GPa)^[34]^ is listed beside it in Table S2."*
- 문제: ① [34] (Sakuda 2013) 의 24 GPa 는 **75Li₂S·25P₂S₅ 유리**의 값이다 — LPSCl 이 아니다 (정본 카드 `sakuda2013_sulfide_mechanical_property`).
  ② docx 표 S2 에는 그 행이 **없다** (§7-2 #5) → 문장이 없는 행을 가리킨다.
- **권고 (A)**: *"The 1.35 GPa value is an empirical contact-law input, not an intrinsic LPSCl modulus (the first-principles value is
  22.1 GPa^[new: Deng]^) and not an independent validation of the present beds."* — [34] 는 다른 자리에 인용이 없으면 목록에서 뺀다 (9-4).
- (B) 24 GPa 를 남기면: *"… (24 GPa for a Li₂S–P₂S₅ glass^[34]^) …"* 로 소재를 밝히고 *"is listed beside it in Table S2"* 는 지운다.

**(2) 현재** — *"The ~10 % target is derived from composite and glass literature rather than measured directly on pure LPSCl, and the 11–12 %
contact overlap is a pure-SE simulation consistency result rather than a measured target.^[9]^"*
- 문제: ① [9] Minnmann 2022 (*Adv. Energy Mater.* Perspective) 에는 공극 수치가 **하나도 없다** (정본 카드 · 감사 C A2 — 저자 이니셜도 T. 가
  아니라 **P.** Minnmann).  ② *"pure LPSCl 에서 직접 잰 값이 없다"* 도 이제 사실이 아니다 — 순수 Li₆PS₅Cl 펠릿 공극 실측이 있다.
- **권고**: *"The ~10 % target is a model target within the range reported for cold-pressed Li₆PS₅Cl pellets (5–19 % after pressing at
  275–441 MPa across laboratories^[new: Ohno]^; 13 ± 2 % at 360 MPa^[new: Song]^), and the 11–12 % contact overlap is a pure-SE simulation
  consistency result rather than a measured target."* — [9] 는 **이 문장에서** 뺀다 (다른 자리의 [9] 는 9-4).
- ⚠ 정직 한정: 10 % 는 그 범위 **안**이지만 단일 연구값 13 ± 2 % (Song) · ≈18 % @370 MPa (Doux 2020 — 정본 카드 기준, 원문 PDF 는 이 세션에
  없음) 보다 **치밀한 쪽**이다.  바로 다음 문장 *"The resulting beds are more compacted than the experimental porosity anchor"* 와 같은 방향이므로
  숨기지 않는다.

- ⚠ **docx 에는 더 강한 옛 문장이 있을 수 있다** — 리포의 08-25 생성본 (`docs/manuscript_draft/DEM_methodology_and_tables_v1.docx`) 은
  *"… reduced from the dense-material value of 24 GPa [34] to 1.35 GPa, which reproduces the ~10 % porosity and 11–12 % contact overlap reported
  for cold-pressed LPSCl at 300 MPa. [9]"* 이다 (감사 G, 09-26 원문 확인).  *"reported for cold-pressed LPSCl"* 은 두 값 모두 문헌에 없으므로
  (10 % 는 모델 표적, 11–12 % 는 우리 시뮬 결과) 사용자 docx 에 이 판이 남아 있으면 위 권고 문장으로 **통째로** 바꾼다.

**(3) 저자 확인** — 같은 문단 *"more compacted than the experimental porosity anchor"* 의 *experimental porosity anchor* 가 무엇인가.  ⚠ 리포에서
이 앵커로 쓰인 **15.6 %** 는 플래튼 사전등록 표 (`docs/reviews/fam_platen_prereg_20260812.md:30`) 가 행 이름은 *"실험"* 인데 출처 칸을
**"DEM 정본"** 으로 적는다 (감사 G, 09-26 원문 확인) — 실험값이 아니라 DEM 침대의 ε_sphere 일 수 있다.  실측 SBE/DBE 전극 공극이면 값과
측정법을 Table S3 에 적고, DEM 값이면 *experimental* 을 빼고 *"the DEM packing porosity (15.6 %)"* 로 적는다.

**(4) 표 S2 각주 ※ (사용자 docx — 09-03 통독 기록 `docs/reviews/ms_readthrough_20260903.md:656–657`)** — *"Parameters marked 'Calibrated'
were adjusted so that the compacted packing reproduces the porosity and contact overlap measured for cold-pressed LPSCl.[S5]"*
- 문제: [S5] Cronau 2021 은 공극도 접촉 겹침도 재지 않았다 (적층압–σ_ion 논문) — **M**.  겹침 11–12 % 는 우리 시뮬 결과이고, 10 % 는 모델 표적이다.
- 조치: 이 각주를 9-1 의 **ᶜ** 로 바꾼다.  (Calibrated 세 행 #5 · #7 · #9 에 ᶜ 를 단다.)

### 9-3. SI 참고문헌 — 바뀌는 것 (서지는 전부 정본 카드 · 원문 PDF)

| 쓰임 | 서지 (ACS 형, 제목 생략 — 넣을 때는 PDF 첫 쪽에서) | 근거 |
|---|---|---|
| S4 **교체** (#2 · ᵃ) | T. Sedlatschek et al., *J. Power Sources* **681** (2026) 240276 | 카드 `sedlatschek2026_…` (생성기 S6 와 같음) |
| S5 유지 (#10 · ᶠ) | M. Cronau, M. Szabo, C. König, T. B. Wassermann, B. Roling, *ACS Energy Lett.* **6** (2021) 3072 | 카드 `cronau2021_…` (SI 보강) |
| 새 (ᵇ) | S. Wang, M. Yan, Y. Li, C. Vinado, J. Yang, *J. Power Sources* **393** (2018) 75 | 카드 `wang2018_…` |
| 새 (ᵇ) | R. Amin, Y.-M. Chiang, *J. Electrochem. Soc.* **163** (2016) A1512; erratum **163** (2016) X7 | 카드 `aminchiang2016_…` — NMC532 표기는 정오표에서 |
| 새 (ᵇ) | L. Ketter, N. Greb, T. Bernges, W. G. Zeier, *Nat. Commun.* **16** (2025) 1411 | 카드 `ketter2025_…` |
| 새 (ᶜ ᵈ ᵉ · Methods) | Z. Deng, Z. Wang, I.-H. Chu, J. Luo, S. P. Ong, *J. Electrochem. Soc.* **163** (2016) A67 | 카드 `deng2016_…` (Table III) |
| 새 (ᶜ ᶠ · Methods) | S. Ohno et al., *ACS Energy Lett.* **5** (2020) 910 | 카드 `ohno2020_…` — **SI 만** 확인, 권·쪽은 사용자 제공 서지 |
| 새 (ᶜ · Methods) | S. Song, C. Shi, A. Pakhare, B. W. Sheldon, P. R. Guduru, *ACS Appl. Energy Mater.* **8** (2025) 5636 | 카드 `song2025_…` + PDF 첫 쪽 (09-26) |
| 새 (ᵍ ʰ) | M. Endo, Y. A. Kim, T. Hayashi, K. Nishimura, T. Matusita, K. Miyashita, M. S. Dresselhaus, *Carbon* **39** (2001) 1287 | 카드 `endo2001_…` |
| 새 (ᵃ 선택 문장) | N. Sharma, D. Meng, X. Wu, L. S. de Vasconcelos, L. Li, K. Zhao, *Extreme Mech. Lett.* **58** (2023) 101920 | 카드 `sharma2023_…` + PDF p. 5 (09-26) — ⛔ *"230 GPa single-crystal NCM811"* 로 인용하지 말 것 (그 값은 NMC811 소결 펠릿의 **압입탄성률**) |
| Methods [9] | 10 % 문장에서 제거 | 다른 인용 자리 = 9-4 |
| Methods [34] | A 안이면 제거 | 다른 인용 자리 = 9-4 |

### 9-4. 원고 참고문헌 전수 대조 — ✅ 감사 G (09-26) · 원문 `docs/reviews/citation_root_audit_20260925/audit_G_blindspots.md`
- **SDCP 원고 생성기 `build.js` 참고문헌 7/7 판정**:
  - `[9]` Minnmann 2022 — **M** (공극 수치 없음 · 1저자 이니셜 **P.** — 9-2 (2)).
  - `[34]` · `[S7]` Sakuda 2013 — **M** (24 GPa 는 Li₂S–P₂S₅ 유리 — 9-2 (1)).  docx 는 이미 그 표 행을 뺐고 생성기에는 남아 있다.
  - `[S8]` Cronau 2021 — **P** (3.0 = SI 그림 S2c 평탄의 하단 판독 — `CL-91`, 각주 ᶠ).
  - `[33]` Kloss (LIGGGHTS) · `[35]` Hu (MLS-MPM) — **C** (방법 인용, 서지 확인).
  - `[S6]` Sedlatschek 2026 — V (카드 · PDF).
- **표 S2 각주 ※** (docx) — **M** → 9-2 (4).
- **"experimental porosity anchor"** — **U⚠** → 9-2 (3).
- **리포의 08-25 생성 docx** (`DEM_methodology_and_tables_v1.docx`) 는 **낡았다** — 지어진 S6 (`CL-90`) · *(grain interior)* 라벨 · 9-2 (2) 의 옛
  문장 · *"Wang 2018 = 5 × 10⁻⁵"* 오귀속이 그대로다 (머리 배너가 파일 전체를 스윕에서 면제하고 있어 스윕에 안 잡힌다).  ⚠ **이 파일을
  공저자에게 보내지 말 것** — 생성기로 다시 만들거나 (9-5 ⑦) 사용자 docx 만 쓴다.
- **코저자 Methods v7 docx** (`docs/manuscript/Methods_simulation_v7_for_coauthors.docx`, 08-30): *"~10 % target derived from composite and glass
  literature"* — **M** (9-2 (2) 와 같이 고침) · Endo 값에 붙은 *VGCF-H* 이름 — **P** (그 논문에 그 이름이 없다) · Hong 2026 PTFE 1 wt% 가 SBE/DBE 와
  *"exactly"* 같다 — **P** (Hong 은 0 · 1 wt% 비교, DBE 는 0.5 wt%) · `E(dense) = 24 GPa` (유리 값).
- **세미나 덱** (`docs/seminar/*.pptx`): 5 번 장 *"measured"* 순수 SE 10 % + Minnmann 꼬리말 — **M** · 부록 A 의 11–12 % 겹침 *"(Cronau)"* ·
  LPSCl 24 GPa — **M** · 9 번 장 Bazzoun *"same resistor-network method"* · *"≈ experiment"* — **P** (그쪽은 접촉망, 우리는 복셀 — `CL-81`).
  발표에 다시 쓸 때만 고친다.
- **다른 원고 `docs/paper/main.tex` (Stage E 파괴 인지 솔버)** — 인용 키 50/50 판정: F (`Wang2022` · `Minnmann2021` 040502) · 서지 오류 새로 2
  (`Lewis2022` · `Tippens2019` — DOI · 권 · 쪽이 다른 논문) · 기존 서지 오류 9 · 주장 M 다수 (`LiuYin2025` 포함).  σ_grain 잔재 한 문장
  (803–806 행, *"single-crystal … \citep{Sakuda2013}"*) 은 **이 커밋에서 고쳤다**.  나머지는 준희 회신과 무관 — 정정 묶음 (원고 참고문헌) 으로.

### 9-5. 결정할 것 (사용자)
1. **Methods (24 GPa)[34]** — A (Deng 22.1, 표 언급 삭제 · 권고) / B (24 GPa 에 유리 명시).
2. **ᵉ (ν 0.49) 근거** — Deng 28.7 만 / 우리 DFT B₀ 26.2 도 SI 에 싣기 (실제 보정 표적).
3. **DEM 1.35 의 보정 표적** — 보정 기록 (`docs/esse_calibration_2mAh_real_9.md:53–58`) 은 *복합 전극 "실험/생산 공극 ~13.5 %"* 에 맞췄다고 적는데
   그 실험의 출처가 리포에 없고, 같은 자리의 *"냉간압착 LPSCl 유효 탄성률 문헌 범위 ~1–2 GPa"* 는 정본 카드 근거가 없다 (Song 2025 실측 4.7 ±
   1.1 GPa).  Methods 는 ~10 % 표적으로 읽힌다 → 어느 쪽이 맞는지 + 9-2 (3) *experimental porosity anchor*.
4. **#1 · #4 · #11 증빙** (D50 · SEM).
5. **선택**: ᵃ (S4 측정값 병기) · NCM811 ν 0.25 행 추가.
6. NCM σ_e (§1 ⑥) — **A 로 진행 중** (§8 최종안).  B 를 원하면 말씀.
7. **리포의 08-25 생성 docx** — 생성기 (`build.js`, 08-29 이후 정정분 반영) 로 다시 만들지 / 지울지 / 그대로 두고 *"보내지 말 것"* 배너만 둘지.
8. **SDCP σ_e 250 S cm⁻¹ 라벨** — 09-03 통독 기록은 `Measured` (*저자 4-probe*), 생성기 · 코저자 v7 docx · 원장 `CL-61` 은 `Assumed` 다.  저자가
   직접 4-probe 로 쟀으면 `Measured (4-probe, this work)` + 측정 조건을 SI 에, 아니면 `Assumed` — 한쪽으로 통일 (원장 `CL-61` 서술도 함께).

### 9-6. 준희에게 보낼 답 (최종 — §8 · §8-2 초안을 합침)

> 준희야, 표 S2 를 행마다 원문 PDF 로 다시 대조했어. 정리하면:
> 0) **S4 (NCM811 E 140 GPa)** — 우리 쪽 코드 주석에서 원문 확인 없이 생긴 인용이 표까지 퍼진 거였어, 미안. Sedlatschek 2026 (JPS 681,
>    240276 — 다결정 NCM811 나노압입 138 ± 24 GPa) 로 바꿀게. 140 은 그 측정 범위 안이라 값은 그대로 둬.
> 1) **NCM σ_e 1e-2** — Assumed 유지. 문헌값을 가져온 게 아니라 모델 유효값이야. NCM811 pristine 실측은 4.1e-3 (Wang 2018, DC 분극), NCM83 은
>    5.22e-3 (Ketter 2025) 이고, NMC 전자전도도는 조성·충전상태·연구실에 따라 5e-8~1.4e-2 로 흔들려서 단일 Ref 로 달 값이 없어. 각주에 문헌
>    범위 + Wang 값 + 민감도 (σ_NCM 을 ÷30~×30 해도 DBE > SBE, 비 1.34~1.20) 를 달게.
> 2) **LPSCl ν 0.3** — Assumed 가 맞아. DEM 접촉모델 관례값이고 E* = E/(1−ν²) 로만 들어가서 LPSCl 제일원리 값 0.37 (Deng 2016) 과 5 %
>    차이인데, DEM 탄성률 (1.35 GPa) 을 이 ν 로 보정했기 때문에 그 차이는 보정값에 흡수돼.
> 3) **VGCF E 10 GPa** — Assumed 유지. 1 / 10 / 100 GPa 로 바꿔 전극을 다시 압밀하고 전자전도도까지 계산했더니 porosity 0.18 %p, σ_e 0.25 %
>    안에서만 움직였어 (런 전에 정한 기준 안). 각주 + SI 표로 붙일게.
> 4) **VGCF σ_e 100 S/cm** — Assumed. 섬유 하나의 값이 아니라 접촉 손실을 포함한 섬유망 유효값이야 (문헌: 흑연화 단섬유 ~1e4, 0.8 g/cm³ 로 누른
>    분말 ~80 S/cm — Endo 2001). 행 이름 "compressed powder" 는 "effective, fibre network" 로 바꾸고, 78.5 는 그 100 을 복셀 한 칸 굵기로 그린 섬유에
>    맞게 환산한 계산값이라 Calculated + Methods 식으로.
> 5) **S5 (LPSCl σ_ion 3.0e-3, Cronau 2021)** — 3.0 은 본문이 아니라 SI 그림 S2c 에 있어서 검색에 안 걸렸던 거야 (미세결정 Li6PS5Cl 펠릿, 적층압
>    ≥146 MPa 평탄 2.9~3.5 mS/cm 의 하단). 단결정 값이 아니라 고압 펠릿값이라 조건을 각주로 달게.
> 6) 그 김에 표 전체랑 Methods 를 원문으로 다시 봤더니 **추가로 고칠 게 셋** 있어:
>    - 보정 행 (DEM 1.35 · MPM 1.53 · σ_y 0.30) 의 표적 "순수 LPSCl 300 MPa 에서 공극 ~10 %" 는 어느 논문의 값이 아니라 우리 모델 표적이야.
>      순수 Li6PS5Cl 펠릿 실측은 여러 연구실 5~19 % (275~441 MPa, Ohno 2020) · 13 ± 2 % (360 MPa, Song 2025) 라서, 각주에 "모델 표적 + 이 범위" 로
>      적을게. 지금 표 S2 각주 ※ 가 "냉간압착 LPSCl 에서 측정된 공극·접촉 겹침을 재현" 이라며 [S5] 를 다는데, Cronau 2021 은 공극도 겹침도 안
>      잰 논문이라 이 각주를 통째로 바꿀게 (겹침 11~12 % 는 우리 시뮬 결과야).
>    - 그래서 Methods 그 문장 끝의 [9] (Minnmann 2022 Perspective) 는 그 수치가 없어서 빼고 위 두 문헌으로 바꿀게.
>    - Methods 의 "(24 GPa)[34] is listed beside it in Table S2" — 24 GPa 는 Sakuda 2013 의 Li2S–P2S5 유리 값이라 LPSCl 이 아니고, 지금 표엔 그
>      행도 없어. LPSCl 제일원리 값 22.1 GPa (Deng 2016) 로 바꾸고 표 언급은 뺄게.
> 7) 입자 반지름 (NCM 2.5 · LPSCl 0.5 µm) 과 VGCF 직경 0.15 µm 는 측정 근거 (D50 / SEM) 를 우리 쪽에서 확인해서 라벨을 맞출게.
> 8) Methods 참고문헌도 전부 원문과 대조했는데, 표 S2 · Methods 에 걸리는 건 위가 전부야 ([33] LIGGGHTS · [35] MPM 은 방법 인용이라 문제없음).
>    Methods 의 "more compacted than the experimental porosity anchor" 는 그 앵커 (15.6 %) 가 실험값인지 DEM 값인지 우리 쪽에서 확인해서 표현 맞출게.
