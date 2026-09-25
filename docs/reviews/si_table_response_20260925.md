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

## 1. NCM811 electronic conductivity — 1.0 × 10⁻² S cm⁻¹ · 현 표기 `Assumed` · ✅ 재검토 완료 (09-25 오후) — 사용자 결정 1 건 대기

**코멘트**: *"ncm 의 electronic conductivity 는 assumed 여야 하나? reference 가 있지 않나?"*

**결론**: `Assumed` 유지가 맞다.  문헌 측정값은 있지만 NMC 의 σ_e 는 조성·충전상태에 따라 여러 자릿수 움직여 **"NCM811 = 얼마" 로 가져다 쓸 단일
참고값이 없고**, 우리 1.0 × 10⁻² 는 문헌에서 가져온 값도 아니다.  문헌 범위와 이미 돌린 민감도 (CL-70) 를 각주로 붙인다.

> **09-25 재검토에서 고친 것** (앞 판 대비): ① Wang 2018 수치는 여전히 PDF 미확인 — 인용 보류 유지.  ② 앞 판의 *"리포에 격자점별 수치가 없다"* 는
> **틀렸다** — 원장 `CL-70` `measured` 에 9 격자점 표가 있다 (③).  ③ 원고 생성기 메모 D14 의 *"문헌 두 출처가 NMC bulk 를 5 × 10⁻⁵ 로 준다 = 1/200"*
> 은 **모델 입력값을 측정값으로 읽은 것** — 같은 커밋에서 정정 (②).  ④ 표 라벨 이력과 AM 클래스 한정을 ① 에 추가.

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

### ② 문헌 — "reference 가 있지 않나" 에 대한 사실
| 출처 | 무엇을 쟀나 | σ_e (S cm⁻¹) | 지위 |
|---|---|---|---|
| Amin & Chiang, *J. Electrochem. Soc.* **163**, A1512 (2016), DOI 10.1149/2.0131608jes | NMC333 · NMC532 단상 소결 펠릿 (첨가제 없음), 전자/이온 분리 DC, 30 °C | x = 0 (방전): **5.0 × 10⁻⁸** (333) · **1.9 × 10⁻⁶** (532) → x = 0.75: **7.9 × 10⁻³** · **1.4 × 10⁻²** | ✅ 정본 카드 `aminchiang2016_nmc_electronic_ionic_transport_vs_li` (Fig. 2c 디지타이즈 3 중 검증).  ⚠ 811 은 없다 |
| Wang, Yan, Li, Vinado, Yang, *J. Power Sources* **393**, 75–82 (2018), DOI 10.1016/j.jpowsour.2018.05.005 | LiCoO₂ · NMC333/532/622/811 펠릿, 전자/이온 분리 | 검색 요약: NMC333 ≈ 2.2 × 10⁻⁶ → **NMC811 ≈ 4.1 × 10⁻³** (20 °C) | ⚠ **PDF 미확인** (출판사 · OSTI · ADS · Semantic Scholar 전부 이 컨테이너에서 차단).  요약본마다 4.1 × 10⁻³ 을 붙이는 조성이 달랐다 — 확인 전 수치 인용 금지 |
| 모델 논문 입력값: Sangrós 2020 (1 × 10⁻⁵, Amin & Chiang 인용) · Alabdali 2023 (5 × 10⁻⁵, NMC622) · Zhang 2023 (5 × 10⁻⁵, Wang 2018 인용) | 시뮬레이션 **입력** | 10⁻⁵ … 5 × 10⁻⁵ | ⛔ **측정이 아니다** — 방전 상태 · 저 Ni NMC 의 입력값.  811 참고값으로 쓰면 안 된다 (정본 카드 `sangros2020_lib_electrode_dem_mech_elec_ionic` · `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` · `zhang2023_pfib_multiscale_imaging_4d_thick_cathode`) |
| Lee 2026 (LPSCl 코팅 NCM811) | 본문 서술 | *"in the range of 10⁻⁴"* | ⛔ 인용 없는 서술 (정본 카드 `lee2026_lpscl_coating_thickness_ncm811`) |

⇒ 정리:
1. **단일 참고값이 없다** — NMC 측정값이 조성·충전상태에 따라 ~10⁻⁸ … 10⁻² S cm⁻¹ 로 움직인다 (Amin & Chiang: 333 은 x = 0 → 0.75 에서 5 자릿수).
2. **pristine NCM811 은 10⁻³ 급**이다 (Wang 2018 요약값 — 미확인.  Amin & Chiang 을 Ni 함량에 로그-선형으로 외삽하면 1.3 × 10⁻³ — 가정에 기댄 값).
3. 우리 1.0 × 10⁻² 는 이 범위의 **상단 (충전 쪽)** 이고 pristine NCM811 보다 높다.
4. 준희가 떠올린 "reference" 가 모델 논문의 5 × 10⁻⁵ 라면, 그것은 입력값이지 NCM811 측정값이 아니다.

### ③ 이미 돌린 런 — σ_NCM · σ_SDCP 공동 closure 스윕 (원장 `CL-70` live · 사전등록 `docs/reviews/sigma_closure_sweep_prereg_20260902.md`, 런 전 커밋 6cd1fb03 · kgy 완주 09-06)
DBE/SBE 비 R̄ (8 origin 쌍대응 평균, vox 0.15 · centerline):

| σ_NCM (S cm⁻¹) \ σ_SDCP (S cm⁻¹) | 2.5 (÷100) | **250 (생산)** | 25 000 (×100) |
|---|---|---|---|
| 3.33 × 10⁻⁴ (÷30) | 1.0578 | 1.3403 | 1.3530 |
| **1.0 × 10⁻² (생산)** | 1.0668 | **1.3078** | 1.3185 |
| 0.30 (×30) | 1.0666 | 1.1979 | 1.2035 |

- 판정 (**런 전 등록 규칙**) = **DIRECTION-ROBUST**: 9 격자점 전부 `R̄ − 3·SD > 1.01` (최소 1.0522) · 미수렴 팔 0/144.
- **σ_NCM 이 클수록 이득이 작다** (생산 σ_SDCP 열 1.3403 → 1.3078 → 1.1979).  ⇒ 문헌 pristine NCM811 (≈10⁻³, 우리보다 낮다) 쪽이면 비는 1.31 보다
  **커지는 방향**이다 — 이득 측면에서 우리 값은 보수적인 편이다.  (⚠ 격자점 사이 값은 시나리오 보간이지 측정이 아니다.)
- 생산점이 원고 헤드라인을 다른 기계에서 재현 — σ_e(SBE) 53.9 (원고 54.0) · σ_e(DBE) 70.6 mS cm⁻¹ · R 1.307824.
- 등록된 한정어 (유지): 격자점 9 (등록 25) · origin SD 는 표준오차가 아니다 (한 침대의 {0,½}³ factorial) · 격자점 사이 폭은 시나리오 범위 ·
  참 σ 값 · 격자 수렴 · 접촉저항 분배는 답하지 않는다.
- ✅ **원자료가 리포에 있다** — 위 표 · `R̄ − 3·SD` · 쌍대응 산포가 원장 `CL-70` `measured` 에 그대로 있어 **SI 그림을 지금 만들 수 있다**.  kgy
  `~/sdcp/verdicts_9pt.log` 는 출처 보강용 (선택).

### ④ 논문 형식 수정안
1. **Table S2 행**: `Electronic conductivity · 1.0 × 10⁻² · S cm⁻¹ · Assumedᵃ`
   > ᵃ Effective model input, not an intrinsic property of NCM811.  Reported electronic conductivities of layered LiNiₓMnᵧCo_zO₂ range from
   > ~10⁻⁸ to ~10⁻² S cm⁻¹ depending on composition and state of charge (Refs. S(new1), S(new2)); the value used lies at the upper end of this
   > range.  The DBE > SBE ordering holds for σ_NCM from 3.3 × 10⁻⁴ to 0.30 S cm⁻¹, over which the DBE/SBE ratio decreases from 1.34 to 1.20
   > at the SDCP conductivity used here (Supplementary Fig. S(new)).
   - S(new2) (Wang 2018) 은 **PDF 확인 뒤에만** 넣는다 — 그 전이면 S(new1) 하나로 쓴다 (문장은 그대로 성립: Amin & Chiang 이 두 조성 · x 0 → 0.75 를 덮는다).
2. **Supplementary Figure (신설)**: 3 × 3 격자 (σ_NCM × σ_SDCP) 의 R̄, 생산점 표시.  캡션 한정어: *"Nine closure combinations evaluated on one
   SBE/DBE bed pair; bars show the spread over eight grid-origin phases of a single bed, not a standard error; no interpolation between grid
   points."*
3. **Methods 한 문장** (Stage 3 문단 뒤): *"The electronic conductivity assigned to NCM811 (1.0 × 10⁻² S cm⁻¹) is an effective input rather
   than a measured property; the DBE/SBE ordering is unchanged when it is varied thirty-fold in either direction (Supplementary Fig. S(new))."*
4. **SI 참고문헌**: Amin & Chiang 2016 (+ Wang 2018 — 확인 뒤).

### ⑤ 답변 초안 (강준희에게)
> reference 는 있긴 한데 "NCM811 σ_e = 얼마" 로 가져다 쓸 단일 값이 없어. NMC 전자전도도는 조성이랑 충전상태에 따라 10⁻⁸~10⁻² S/cm 까지 움직여
> (Amin & Chiang 2016 JES — 333/532 펠릿, 30 °C). 모델 논문들이 쓰는 1e-5~5e-5 는 방전 상태·저 Ni 입력값이라 811 측정값도 아니고.
> 우리 1e-2 는 그중 하나를 가져온 게 아니라 모델 유효값이라 Ref. 로 달면 오귀속이 돼서, Assumed 로 두고 각주에 문헌 범위랑 민감도를 달게.
> 민감도는 이미 돌려 놨어: σ_NCM 을 3.3e-4~0.3 (÷30~×30) 으로 바꿔도 9 조건 전부 DBE > SBE (사전등록 판정 DIRECTION-ROBUST).
> σ_NCM 이 클수록 이득이 작아져서 (비 1.34 → 1.20), pristine 811 처럼 더 낮은 값이면 오히려 이득이 커지는 쪽이야 — 우리 값이 보수적인 편.
> 이 격자는 SI 그림으로 붙일게.

### ⑥ 결정할 것 · 남은 일
- [ ] **결정 (사용자)** — A (권장): `Assumed` + 각주 ᵃ + SI 그림 · 재계산 없음.  B: 문헌값 (예: NCM811 pristine ≈ 4 × 10⁻³) 으로 바꿔 `Ref.` —
  생산 STEP3 팔 전부 재실행 + 헤드라인 (54.0 · 70.6 · 1.308) 이 바뀌고, 그래도 충전상태 의존이라 가정은 남는다.
- [ ] Wang 2018 PDF 확인 (랩 접근) → 정본 카드 → 각주 S(new2).
- [ ] SI 그림 (CL-70 표로 지금 가능) · 각주 · Methods 문장을 사용자 docx 에 반영.  리포 `build.js` 는 08-23 판이라 라벨 동기화 필요 여부는 사용자 판단.
- [x] 원고 생성기 메모 D14 정정 (모델 입력값 5 × 10⁻⁵ 를 "문헌 두 출처의 NMC bulk" 로 적은 것) — 이 커밋.

## 2. LPSCl Poisson's ratio (DEM contact) — 0.3 · `Assumed` · ⬜

## 3. VGCF fiber diameter — 0.15 µm · `Measured` · ⬜ (이종기술 SEM 원본 대기)

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

## 5. VGCF electronic conductivity (compressed powder) — 1.0 × 10² S cm⁻¹ · `Assumed` · ⬜

## 6. VGCF electronic conductivity (voxel, diameter-preserving) — 78.5 S cm⁻¹ · `Calculated` · ⬜
