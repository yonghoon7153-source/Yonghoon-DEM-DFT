# SI 물성표 리뷰 대응 — 강준희 코멘트 (2026-09-25) · 누적 문서

> 계기: SDCP 원고 SI 물성표 (NCM811 · LPSCl · VGCF) 에 대한 강준희 코멘트 5 건 (09-25 11:40).
> 원칙: **(1) 출처 분류는 사실대로** — 문헌이 그 값을 직접 주지 않으면 `Ref.` 로 바꾸지 않는다 (이 리포는 오귀속으로 세 번 데였다:
> Trevisanello → σ_S/σ_P · [35] → σ_SDCP (`CL-61`) · [36] → 펠릿 보정 (`CL-62`)).  **(2) Assumed 라도 방어는 문헌 밴드 + 우리가 이미 돌린
> 민감도 런으로** 한다.  **(3) 형식은 저널 SI 관행** — 분류 어휘를 표 범례로 정의하고, 한정은 각주로, 문헌은 SI 참고문헌 번호로, 근거 수치는
> Supplementary Figure/Table 로.
> 진행: 항목마다 ① 사실 ② 이미 한 런 ③ 논문 형식 수정안 ④ 답변 초안 ⑤ 남은 일.  상태 = ✅ 정리됨 · ⏳ 진행 · ⬜ 미착수.

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

## 1. NCM811 electronic conductivity — 1.0 × 10⁻² S cm⁻¹ · 현 표기 `Assumed` · ✅ 정리됨 (문헌 1 건 PDF 확인 대기)

**코멘트**: *"ncm 의 electronic conductivity 는 assumed 여야 하나? reference 가 있지 않나?"*

### ① 사실 (이 값이 어디서 왔나)
- 복셀 솔버의 `nmc811` 프리셋 기본값 (`mpm_webapp_payload.py`: `sigma_am_s None → 0.010`).  기원은 DEM σ_e 스케일링 법칙의
  **코퍼스-적합 끝점** σ_S ≈ 9.1 mS cm⁻¹ → 10 반올림 (Stage 22.5 LOCKED).  측정값이 아니다.
- Trevisanello 2021 은 이 크기를 뒷받침하지 않는다 (입경 방향만 — A1 정정, `docs/contradiction_audit_20260720.md`).
  ⇒ **`Ref.` 로 바꾸면 오귀속**이다.  분류는 `Assumed` 가 사실이고, 코멘트의 요지 ("문헌이 있지 않나") 는 **각주의 문헌 밴드**로 받는다.

#### ①-b 왜 1.0 × 10⁻² 를 채택했나 — 이력 (사용자 질문 09-25)
1. **출발 (2026-06, Stage 22.5)**: DEM σ_e 스케일링 법칙 `σ_e = (σ_S·NCM_S)^(1−p)·(σ_P·NCM_P)^p·…` 의 AM 계수를 코퍼스 (DEM 접촉망 솔버 출력) 에
   적합 → **σ_S 9.13 · σ_P 4.14 mS cm⁻¹ → 10 · 5 로 반올림해 LOCKED**.  = 솔버 출력을 가장 잘 재현하는 **유효 AM 계수**.
2. **당시 라벨**: "Trevisanello 2021 — 단결정 ≈10 · 다결정 ≈5 mS cm⁻¹" 인 문헌값으로 믿고 썼다.
3. **A1 정정 (2026-06-30, `docs/a1_sigma_e_direction_closeout.md`)**: Trevisanello 는 σ_e 가 아니라 Li⁺ 화학확산 · BET · R_ct 를 쟀다 →
   입경 **방향**만 지지, 크기는 아님 → 문헌 귀속 **철회**, 라벨을 "corpus-fit endpoint" 로.  값은 **생산 팔 연속성** 때문에 유지.
4. **STEP3 (복셀) 이식**: SDCP 원고 NCM811 (r 2.5 µm) = AM_S 급 → `nmc811` 프리셋 기본값 **0.010 S cm⁻¹** (`scripts/step3_sigma.py` 21–27행).
   ⚠ 거시 유효식의 계수를 복셀 **상(phase) σ** 로 옮긴 것이라 미상 배수가 붙는다 — 코드 자신이 *"order-of-magnitude hook"* 이라 적는다.
5. **방어 전환 (2026-09-02)**: 문헌 앵커가 없으니 **민감도로** — closure 스윕 ÷30~×30 → 방향 강건 (③).
⇒ **1.0 × 10⁻² 는 물리로 고른 값이 아니라 DEM 스케일링 법칙 적합값을 이어받은 것**이다.  문헌 밴드 상단 (탈리튬 NMC) 과 맞는 것은
**사후 정합**이지 채택 근거가 아니다 — 각주에 "문헌에서 골랐다" 로 읽히는 문장을 쓰지 않는다 ("effective value … lies within the range …").

### ② 문헌
| 문헌 | 계 · 조건 | σ_e | 쓰임 |
|---|---|---|---|
| Amin & Chiang, *J. Electrochem. Soc.* **163**, A1512 (2016) | NMC333 · NMC532 소결 펠릿 (첨가제 없음, 상대밀도 96–98 %), 이온차단 DC, 30 °C | x (Li₁₋ₓNMC) 0 → 0.75 에서 **~10⁻⁷ → ~10⁻² S cm⁻¹** (SOC 에 따라 4–5 자릿수) | 밴드 · "단일 스칼라 = 운전점 평균" 의 근거.  정본 카드 `aminchiang2016_nmc_electronic_ionic_transport_vs_li` (확인됨).  ⚠ 811 은 안 쟀다 |
| Wang, Yan, Li, Vinado, Yang, *J. Power Sources* **393**, 75–82 (2018), DOI 10.1016/j.jpowsour.2018.05.005 | LiCoO₂ · NMC333/532/622/811 펠릿, 전자/이온 분리 측정, 20 °C | Ni-rich (532–811) 는 **~10⁻³ S cm⁻¹ 급**, 333 대비 약 3 자릿수 높음 | 811 직접 값.  ⚠ 검색 요약본마다 **4.1 × 10⁻³ 을 532 · 811 에 달리 붙인다** — PDF 로 확인하기 전 값 인용 금지 |

⇒ 우리 1.0 × 10⁻² 는 **탈리튬 상태 밴드의 상단**이고, pristine NMC811 (~10⁻³) 보다 높다.

### ③ 이미 돌린 시뮬레이션 (이 표를 위해 한 것)
- **σ_NCM · σ_SDCP 공동 closure 스윕** — 사전등록 `docs/reviews/sigma_closure_sweep_prereg_20260902.md` (런 전 커밋 6cd1fb03), 원장 `CL-70` (live).
  - 설계: σ_AM_S ∈ {3.33 × 10⁻⁴, **1.0 × 10⁻²**, 0.30} S cm⁻¹ (= ÷30 … ×30) × σ_SDCP ∈ {2.5, 250, 25000} · 각 8 origin · vox 0.15 · centerline.
    kgy 완주 2026-09-06.
  - 판정 (**런 전 등록 규칙**) = **DIRECTION-ROBUST**: 9 격자점 전부 `R̄ − 3·SD > 1.01` (최소 1.052) ⇒ *"이 범위 전체에서 DBE 가 SBE 를 넘는다"*.
  - 크기는 σ_NCM 에 의존한다: 생산 σ_SDCP 열에서 R ≈ 1.34 → 1.20 (σ_NCM 낮은 끝 → 높은 끝).  ⇒ **순서는 강건, 이득의 크기는 아니다** — 이것을 그대로 적는다.
  - 중심점이 원고 헤드라인을 다른 기계에서 재현 (SBE 54.0 · DBE 70.6 mS cm⁻¹ · R 1.3078).
  - 한정어 (등록대로 유지): 격자점 9 (등록 25) · origin SD 는 표준오차가 아니다 (한 침대의 {0,½}³ factorial) · 격자점 사이 폭은 시나리오 범위다.
- 문헌 밴드 (10⁻³ … 10⁻²) 는 이 스윕 창 (3.3 × 10⁻⁴ … 0.3) **안에 들어간다**.

### ④ 논문 형식 수정안
1. **SI 표**: `Assumed` → `Assumedᵃ`.
   > ᵃ Effective value at the upper end of the range reported for layered NMC cathodes (≈10⁻⁷–10⁻² S cm⁻¹ depending on the state of
   > charge; Refs. S(new1), S(new2)).  The DBE > SBE ordering holds for σ_NCM between 3.3 × 10⁻⁴ and 0.30 S cm⁻¹ (Supplementary Fig. S(new));
   > the magnitude of the gain decreases as σ_NCM increases.
2. **SI 참고문헌**: Amin & Chiang 2016 · Wang 2018 (PDF 확인 뒤) 추가.
3. **Supplementary Figure (신설)**: closure 스윕 R̄ 격자 (σ_NCM × σ_SDCP 3 × 3), 중심점 표시 · 한정어 캡션.
4. **Methods 한 문장**: *"The electronic conductivity of NCM811 was set to an effective value of 1.0 × 10⁻² S cm⁻¹; the DBE/SBE ordering is
   insensitive to this choice over two orders of magnitude on either side (Supplementary Fig. S(new))."*

### ⑤ 답변 초안 (강준희에게)
> 맞아, 문헌은 있어. 다만 우리 1e-2 는 문헌값을 가져온 게 아니라 운전점 유효값이라 "Ref." 로 쓰면 오귀속이 돼서 Assumed 는 유지하고,
> 각주에 문헌 밴드를 달게 — Amin & Chiang 2016 (NMC, SOC 에 따라 1e-7~1e-2 S/cm) · Wang 2018 (NMC811 펠릿 ~1e-3 급).
> 그리고 이 값은 이미 민감도를 돌려 놨어: σ_NCM 을 ÷30~×30 (3e-4~0.3 S/cm) 로 흔들어도 9 격자점 전부 DBE > SBE 라서
> (사전등록 판정 DIRECTION-ROBUST), 결론이 이 값에 안 걸려. 그 격자를 SI 그림으로 붙일게. 크기(이득 %)는 σ_NCM 에 따라 달라지는 것도 같이 적을게.

### ⑥ 남은 일
- [ ] Wang 2018 PDF 로 NMC811 값 확인 (랩 접근) → 정본 카드.
- [ ] kgy `~/sdcp/verdicts_9pt.log` (9 격자점 R̄ · SD 표) 를 리포 `docs/data/` 로 — **지금 리포에 격자점별 수치가 없다** (CL-70 요약만).  SI 그림의 원자료.
- [ ] SI 그림 · 각주 · Methods 문장 반영 (`scripts/build_methods_docx.py`).

## 2. LPSCl Poisson's ratio (DEM contact) — 0.3 · `Assumed` · ⬜

## 3. VGCF fiber diameter — 0.15 µm · `Measured` · ⬜ (이종기술 SEM 원본 대기)

## 4. VGCF Young's modulus — 10 GPa · `Assumed` · ⏳ (kgy 민감도 3 팔 진행 중 — `docs/reviews/vgcf_e_sensitivity_prereg_20260925.md`)

## 5. VGCF electronic conductivity (compressed powder) — 1.0 × 10² S cm⁻¹ · `Assumed` · ⬜

## 6. VGCF electronic conductivity (voxel, diameter-preserving) — 78.5 S cm⁻¹ · `Calculated` · ⬜
