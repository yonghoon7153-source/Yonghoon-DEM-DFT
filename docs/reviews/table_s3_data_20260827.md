# Table S3 — 측정값 원장 (2026-08-27)

> ## ⛔ 정본 상태 = `PROVISIONAL_RAW_W4_PENDING` · **원고 승격 HOLD**
>
> Codex R8 (`codex_r8_verdict_20260827.md`, 스냅샷 `381e8b8c`) 판정을 반영했다.
> **살아남는 것은 하나** — 고정 침대·고정 규약·**8개 사전지정 origin phase** 에서 관측한
> protocol-specific 서술값 **R ≈ 1.30782**.
> **철회됨**: SE · ± · 95 % CI (Q1) · 물리적 bracket 과 "둘 다 하한" (Q2) ·
> 절대값 타당성 주장 (Q3) · "같은 관측량" 전제와 현재 보정 순서 (Q4).
> **해제 조건**: W4 16팔 JSON·receipt 커밋 + 모든 팔의 `input_digest` 를 W2 기대 digest 와
> 대조 (Q6 신규 [P1] — `latest_run` 근접 사고와 결합해, 지금은 **실제로 08-27 침대를
> 읽었는지 독립 대조가 불가능**하다).

핸드오프 §C 의 **D3 채무**("지금 미세구조는 AFM 이전 세대로 압밀한 것이다 … 두께·porosity·
면적용량·σ_e 를 지금 채우지 마라")가 오늘 해소됐다.  W2 로 두 침대를 새 첨가제 탄성계수
세대(`ADD_E_SET_20260818`)로 재압밀했고, W4 로 8팔 origin factorial 을 다시 냈다.

이 문서는 **측정 원장**이다.  원고 표는 여기서 인용한다.

---

## 1. 침대 (W2, 2026-08-27 재압밀)

| | SBE | DBE |
|---|---|---|
| 조성 | VGCF 3.0 + PTFE 1.0 wt% | VGCF 3.0 + PTFE 0.5 + **SDCP 0.5** wt% |
| 첨가제 E | VGCF 10.0 · **PTFE 1.80** GPa | VGCF 10.0 · PTFE 1.80 · **SDCP 9.00** GPa |
| 세대 | `ADD_E_SET_20260818` (옛 세대 = PTFE 0.30 · SDCP 23.6) | 동일 |
| 정지 두께 | **72.53 µm** | **72.53 µm** |
| porosity (MPM union) | 7.86 % | 7.37 % |
| 런 디렉터리 | `kit_SBE/run_VGCF3_PTFE1_20260827_134104_3672586` | `kit_DBE/run_VGCF3_PTFE0.5_SDCP0.5_20260827_150029_3687585` |

★ 재압밀이 **실제로 무엇을 바꿨는지**는 별도 측정으로 확인했다 —
`docs/reviews/w2_bed_regeneration_20260827.md`.  요지: `se_dump.npy` md5 가 다르고,
**E 가 바뀐 PTFE 만** 3배(med)·6배(p95) 더 움직였다(E 가 안 바뀐 VGCF 는 SE 와 구분 불가).
크기는 생산 복셀의 **1.2 %(p95)**.

**porosity·두께 표기 규약** (R8 Q5 — 침묵 삭제가 아니라 **라벨 공개**):

| 값 | 라벨 |
|---|---|
| 7.86 / 7.37 % | **`ε_union` — simulation-geometry diagnostic**.  conventional electrode porosity 가 **아니다**.  SI/방법·한계 절에 공개한다 |
| 원고 D4 의 `ε_sphere` | 새 침대에서 **별도 계산할 때까지 pending** (핸드오프 §C: *"빼서 옮기지 말고 새 침대에서 다시 낼 것"*) |
| 72.53 µm | **terminal wall separation under the kinematic stopping rule** (두 침대 공통) |

⚠ **과압축**: 7.4~7.9 % 는 실험 앵커 ~15.6 % 의 절반 이하다.  플래튼 운동학 정지(트랙 ②):
정착 `wallP` 가 0.006~0.012 GPa = target 0.30 의 **2~4 %** 이고, frame 5 의 2.55 GPa
스파이크는 `V/c_S = 1.94`(플래튼이 전단파보다 빠름)의 관성이다.

★ 두 침대가 **같은 속도로 같은 자리(`wall_z` 1.385)에 정지**했다 = **like-for-like 입력**이
보장된다.
⚠⚠ **그것이 "과압축이 비에서 상쇄된다" 는 뜻은 아니다** (R8 Q5).  R = 1.3078 은 **현
과압축 protocol 안의 contrast** 이지, 과압축이 제거된 실험 ratio 의 추정치가 아니다.
⚠ 또한 두께가 같다는 것은 *"현재 정지 규약에서 **terminal thickness 가 조성 판별량이
아니었다**"* 는 뜻이지, MPM 이 두 침대를 구분하지 못했다는 뜻이 **아니다** — W2 측정은
**상별 변위와 point cloud 가 실제로 달라졌음**을 보여 준다
(`w2_bed_regeneration_20260827.md` §3).
⇒ 이 침대쌍으로 **기계 주장은 하지 않는다** (판별량이 없으므로).

---

## 2. σ_e — PTFE **차단** 규약 (W4, 8팔 origin factorial)

디렉터리 `prereg_v2_vox015_sph_b048_ptscenterline_lean2_rddb33647303c`
규약: vox **0.15 µm** · SDCP **구 스탬프 Ø0.30**(d/vox = 2.00) · AM 브리지 0.48 µm 고정 ·
σ_VGCF 78.5398 S/cm(직경보존) · 섬유 segment · **PTFE centerline 스탬프 = exact-zero DOF** ·
LEAN=2(σ_e 전용) · 비주기

⚠⚠ **표기 규약 (R8 Q1 반영)** — 8팔은 같은 침대의 **완전한 {0,½}³ origin factorial** 이고
독립 복제가 **아니다**.  완전 factorial 은 7개 비상수 대비가 8점을 전부 소모하므로
**복제 기반 오차 자유도가 0** 이다.  ⇒ `sd/√8` 은 표준오차가 아니며, `±` · `95 % CI` 는
**철회**한다.  산포는 **origin-phase SD** 와 **관측 범위**로만 적는다.

| | 값 |
|---|---|
| **σ_e 비 R (정본)** | **1.307820** — 쌍대응 비의 산술평균 (**개정 A1 등록 estimator**) |
| (참고) `mean(DBE)/mean(SBE)` | 1.307824 — **정본 아님**, 혼용 금지 |
| **origin-phase SD** | **0.002977** (8 prescribed origin phases) |
| **관측 범위** | **1.301726 – 1.310448** → 이득 **30.173 – 31.045 %** |
| **이득 G** | **+30.78 %** (범위 30.17 – 31.05) — ⚠ `± 0.105 %p` · `CI` **철회됨** |
| σ_e(DBE) | **70.61** mS/cm · origin-phase SD **0.461** · 범위 70.043 – 71.400 |
| σ_e(SBE) | **53.99** mS/cm · origin-phase SD **0.299** · 범위 53.621 – 54.530 |
| 수렴 | **8/8** (`cg = 0` 전부) |
| 팔-폭 (max−min)/mean | 0.667 % |
| origin 일관성 검사 | 0.3027 % < 문턱 1.17 % — ⚠ **동결된 비추론적 일관성 검사**로 개명.  재현성·격자수렴·통계적 정밀도의 증거로 **쓰지 않는다** |
| dof | DBE 26.76~26.81 M · SBE 26.38~26.42 M |

팔별 원값:

| origin (½셀) | σ_e DBE | σ_e SBE | R |
|---|---|---|---|
| (0,0,0) | 0.0714004 | 0.0545304 | 1.309369 |
| (0,0,½) | 0.0709708 | 0.0542450 | 1.308336 |
| (0,½,0) | 0.0700427 | 0.0536207 | 1.306261 |
| (0,½,½) | 0.0705319 | 0.0538229 | 1.310443 |
| (½,0,0) | 0.0705380 | 0.0538274 | 1.310447 |
| (½,0,½) | 0.0709190 | 0.0541484 | 1.309717 |
| (½,½,0) | 0.0702039 | 0.0539314 | 1.301727 |
| (½,½,½) | 0.0702353 | 0.0537683 | 1.306258 |

⚠⚠ **이것은 가설검정이 아니다.**  사전등록 v2 는 **점 스탬프**에 대해 등록됐고 이 런은
구 스탬프 + PTFE centerline 이다.  판정기가 출력한 `h0`(비 1.3078 ≥ 1.05)는 그 등록된
문턱에 대고 찍은 것이라 **이 런의 검정이 아니다** (prereg §7).
⇒ 원고에는 **"이 규약·8개 사전지정 origin phase 에서 비 = 1.3078 (origin-phase SD 0.0030,
관측 범위 1.3017–1.3104)"** 이라는 **값 서술**로만 쓴다.

★ **CL-49 재현**: arm 0 한 팔로 잰 1.3092 를 8 origin phase 로 재현했다(1.30782).
⚠ 그때 없던 것은 **표준오차가 아니라 origin-phase 산포**다 (SD 0.0030 · 범위 0.667 %).
"n=1" 이 "8 phases" 가 된 것은 **격자 위상 민감도가 작다는 관측**이지 통계적 정밀도가
생긴 것이 아니다 (R8 Q1).

---

## 3. σ_e — PTFE **미표현** 규약 (W4b, 진행 중 2026-08-27 밤)

같은 침대·같은 격자에서 `PTFE_STAMP` 만 끈 8 origin phase.  목적은 **PTFE 표현 민감도의
두 번째 점**을 같은 침대에서 얻는 것이다 — 옛 세대 침대의 +12.32 %(CL-33/34)를 옆에 놓으면
**침대 세대를 넘나드는 비교**가 된다.
⚠ **브래킷을 만들기 위한 것이 아니다** (R8 Q2 로 브래킷 서술 자체가 철회됐다).

| | |
|---|---|
| 디렉터리 | `prereg_v2_vox015_sph_b048_lean2_*` (PTFE 태그 없음) |
| 상태 | **실행 중** — 완주 후 이 절을 채운다 |

---

## 4. ~~브래킷~~ → **PTFE 표현 민감도의 두 점** (R8 Q2 로 철회·재작성)

⛔ **옛 §4 는 삭제됐다.**  적혀 있던 것:
*"PTFE 미표현 < 실험 +23.1 % < PTFE 차단 +30.78 %, 양쪽 다 하한"*.

**철회 이유 둘** (Codex R8 Q2):
1. **W4b 가 미완료인데 부등식을 먼저 선언했다** — 첫 항이 아직 **측정값이 아니다**.
2. **"둘 다 하한" 이 성립하지 않는다.**  `exact-zero` 스탬프는 얇은 실제 코팅보다
   **국소 차단을 과대**할 수도 있고 **공간적 코팅 범위를 과소**할 수도 있어 방향이 미정이다.
   게다가 **각 절대 σ 가 단조로 변해도 비 σ_DBE/σ_SBE 의 방향은 정해지지 않는다.**
   ⇒ "수치적으로 사이에 둔다" 와 "둘 다 하한" 이 형식적으로 동시에 참일 수는 있으나,
   그 경우 두 모델값은 물리값을 **bracket 하지 않는다**.

**대체 보고 형식** — W4b 완료 후에도 **PTFE 표현 민감도의 두 점**으로만 적는다:

| protocol | 이득 |
|---|---|
| `PTFE-off protocol result` (§3) | 측정 예정 |
| `centerline exact-zero protocol result` (§2) | +30.78 % (범위 30.17 – 31.05) |

⚠ 실험값이 두 점 사이에 있어도 그것은 **numerical straddling** 이지 **물리적 상·하한이
아니다.**  "실험을 괄호에 넣는다" 류의 문장을 쓰지 않는다.

## 5. 절대 σ_e 와 문헌 — **거친 자릿수 대조만 유지** (R8 Q3)

문헌 밴드 (litdb 정본 전수조사, 건식 황화물 복합 양극 유효 σ_e):

| 출처 | 조성 | σ_e (mS/cm) |
|---|---|---|
| Kim 2024 | carbon 3 wt%, **AM 80 / 85 / 90** | 38.6 / 54.8 / 65.2 |
| Lee 2025 | VGCF 3 · PTFE 0.5 · **AM 80** | 34 |
| Kim 2024 (건식) | carbon **1** wt% | 5.1 |
| Hong 2026 | 바인더 4종 | 0.85 ~ 1.11 |

우리 (PTFE 차단 규약, **AM 70.3** wt% · VGCF 3 · PTFE 1): SBE **53.99** · DBE **70.61**.

- 단순 밴드(`~1–65`)로는 SBE 가 **안**, DBE 가 상단을 **8 % 초과**.
- ⚠ **"조성을 맞추면 우리가 높다" 는 결론이 아니라 가설이다** (R8 Q3).  Kim 의 세 점
  (80/85/90)을 **70.3 까지 외삽할 정당성이 없다** — 직선 적합조차 70.3 에서 **≈13.8** 이라
  옛 문서의 "20 급" 도 유일하게 도출되는 값이 아니다.  퍼콜레이션·분산·압밀이 다르면
  명목 carbon 3 wt% 가 같다는 사실만으로 비교 가능성이 확보되지 않는다.
- ★ SBE 53.99 가 Kim 의 AM-85 값 54.8 과 거의 같은 것은 **수준이 우연히 맞은 것**이다.
  "밴드 안" 으로 쓰면 그 사실이 가려진다.

**높게 나올 수 있는 이유 — 방향이 확인된 것만:**

| # | 기전 | 방향 | 근거 |
|---|---|---|---|
| 1 | **복셀 융합이 접촉저항을 삭제** | σ_e ↑ | CL-47.  ⚠ **R8 Q4-a 로 확장됨** — 섬유–섬유뿐 아니라 **AM–AM · AM–탄소 · 집전체 접촉저항도 dedicated term 이 없다**.  σ_VGCF 는 그중 일부만 lumping 한다 |
| 2 | **PTFE 표면 코팅 미표현** | ⚠ **방향 미정** | Lee 의 3,000배 붕괴는 코팅 효과라 복셀이 못 본다.  그러나 `exact-zero` 는 국소 차단을 **과대**할 수도 있다 (R8 Q2) |
| 3 | **침대 과압축** | σ_e ↑ (절대값) | porosity 7.9 % vs 앵커 ~15.6 % (§1) |
| 4 | ~~격자 미수렴~~ | ⚠ **여기서 뺀다** | **내부 모순이었다** (R8 Q3): §6 은 격자 축에서 현재 값을 **하한**이라 적는다.  하한이면 격자는 "높은 값" 을 설명하는 항목이 **아니다**.  ⇒ 격자가 **절대 σ_e** 를 어느 방향으로 움직이는지는 **미측정**이다 (CL-41 이 잰 것은 **이득**의 방향이다) |

### ★ 원고에 쓸 문장 (본문 또는 SI)

**자릿수 대조는 여전히 실을 수 있다** (CL-46 Tier 1) — 다만 **거친 scale comparison**
으로서다.  ⚠ *"절대 크기도 물리적으로 타당한 범위를 낸다"* 는 주장은 **R8 Q3 로 철회**됐다:
솔버 자신의 신뢰 계약이 *"절대값은 contact-area cross-calibration 전에는 신뢰하지 말라"* 다.

⚠⚠ **R8 Q3 로 수정됨.**  옛 판 끝의 *"…indicating that the voxel transport model returns
physically reasonable absolute magnitudes and not merely relative trends"* 는 **삭제**한다 —
솔버 자신의 신뢰 계약이 *"절대값은 contact-area cross-calibration 전에는 신뢰하지 말라"* 다.
유지 가능한 것은 **거친 scale comparison** 뿐이다.

> The computed effective electronic conductivity of the composite cathode
> (54.0 mS cm⁻¹ for the single-binder electrode, 70.6 mS cm⁻¹ with SDCP) is within
> the same order of magnitude (10¹ mS cm⁻¹) as reported dry-processed sulfide
> composite cathodes at nominally comparable carbon loading — 38.6–65.2 mS cm⁻¹ at
> 3 wt% carbon (Kim 2024) and 34 mS cm⁻¹ at VGCF 3 wt% / PTFE 0.5 wt% (Lee 2025).

바로 뒤에 붙이는 한정 문장 (**분리하지 말 것**):

> This is a coarse scale comparison, not an absolute validation.  The composition
> is not matched — our active-material loading is 70.3 wt% against 80–90 wt% in the
> cited work — and the comparison additionally differs in compaction pressure,
> porosity, thickness and carbon morphology.  The model further contains no
> interfacial contact resistance of any kind, so its absolute conductivity is that
> of an idealized bulk-model counterpart of the measured transport mode rather than
> of the measurement itself.

⇒ **국문 요약**: *"모델의 유효 전자전도도는 문헌 건식 황화물 양극과 **같은 자릿수**
(10¹ mS cm⁻¹)다 — 절대 크기가 물리적으로 타당한 범위에 있다.  ⚠ 다만 조성이 안 맞아
(우리 AM 70.3 vs 문헌 80~90) **정량 검증이 아니라 자릿수 정합**이고, 조성을 맞추면
우리가 높은 쪽이다.  방향은 설명된다 — 복셀 융합의 접촉저항 삭제 · PTFE 코팅 미표현 ·
과압축 침대가 모두 σ_e 를 올리는 쪽이다."*

⚠ **"밴드 안" 이라고 쓰지 말 것.**  조성을 안 맞춘 밴드 대조는 우연한 일치를 검증으로
읽게 만든다.  ⇒ 지름길은 **Lee 2025 조성(80:17:3:0.5)으로 침대 1건**을 만들어
같은-조성 대 같은-조성으로 재는 것이다 (CL-46 이 이미 지목, **미실행**).

★ 이 절은 `week_plan_manuscript_20260825.md` §4 의 보류 블록(p1 세대, 인용 금지)을
**대체한다** — 거기 적힌 "W4 (p2 재측정) 뒤에 이 절을 다시 쓴다" 가 이것이다.

---

## 6. 아직 못 쓰는 것 (열린 채무)

| 항목 | 왜 |
|---|---|
| porosity · 면적용량 | §1 의 두 이유 (관례 + 과압축).  `ε_sphere` 재계산 + 라벨 필요 |
| **격자 수렴** | **미확인** (CL-41: 증분비가 어떤 멱법칙과도 안 맞아 Richardson 외삽 무의미) ⇒ 보고값은 이 축에서 **하한** |
| 이온 축 | LEAN=2 가 이온을 안 푼다 (`--no-ion`).  B 트랙 펠릿 보정 후 별도 런 |
| σ_SDCP 250 출처 | 캐스트 필름 vs 압착 펠릿 미상 → 이중계상 위험 (핸드오프 §C, 사용자 회신 대기) |
| ρ_SDCP 1.30 | 코드에 `PROXY, REPLACE with the user's manuscript value` |

---

## 7. 재현 (봉인)

```
코드   ~/dem-mt @ c2f5b047 (manuscript-track, dirty 0)  ⚠ 브랜치 이름이 아니라 SHA 로 인용할 것
러너   ARMS=8 LEAN=2 VOX=0.15 SDCP_SPHERE_D=0.30 PTFE_STAMP=centerline \
       bash ~/dem-mt/scripts/sdcp_gain_vox015_8arm.sh
계약   [p2] ✓ 계약 봉인 통과 (8 팔)
판정   python3 ~/dem-mt/scripts/sdcp_gain_verdict.py --dir "$O"
```

⚠ **`claude/stoic-knuth-NObVQ` @ `ce2f318f` 의 sealed runner–payload–verdict 경로로는 이 런을 그대로 replay 할 수 없다** (backport 필요) — 거기엔 `PTFE_STAMP` 노브도
`ptfe_block_um` 필드도 없어서 러너가 규약을 못 켜고 판정기가 매니페스트를 거부한다.
그래서 kgy 를 manuscript-track worktree 로 옮긴 뒤 돌렸다.

---

## 8. σ_e 절대값을 실험에 맞출 것인가 (사용자 질문, 2026-08-27)

**질문**: 조금 안 맞으면 σ_e 입력값(σ_VGCF)만 조절하면 되나 · 그게 가능한 이유가
DC 분극이라서 맞나.

⚠⚠ **첫 답은 과했다 — R8 Q4-a 로 수정한다.**

- **~~"같은 양을 잰다"~~ → "같은 수송 모드의 idealized bulk-model counterpart".**
  STEP3 가 정상상태 전자 through-plane conduction 을 푸는 것은 맞다.  그러나 **수치적
  observable 이 다르다**: 코드는 인접 셀 사이에 bulk σ 의 harmonic-mean 저항만 두고
  **AM–AM · AM–탄소 · 탄소–탄소 excess contact resistance 도, 집전체 접촉저항도 두지
  않는다**(닿으면 한 셀로 융합된다).  Lee 의 two-terminal DCP 는 `R = V/I`,
  `σ = L/(RA)` 로 환산하며 **계면 de-embedding 이 기술돼 있지 않다** = 모든 계면저항을
  포함한 값이다.
  ★ **따라서 CL-47 의 lumping 서술도 불완전하다** — 그것은 **섬유–섬유**만 가리킨다.
  **AM–AM · AM–탄소 접촉저항은 dedicated term 이 없다.**
- **σ_VGCF 조절 자체는 여전히 가능하다** (CL-47: 재료상수가 아니라 유효 망 상수, DEM 의
  18배 E 연화와 같은 인식론 frame[2]).  ⚠ 다만 그것으로 **위 결손 일부를 수치적으로
  흡수**할 수는 있어도 **섬유–섬유 접촉만의 물리 파라미터로 식별할 수는 없다.**

**조건 셋:**

| | |
|---|---|
| ⓐ **앵커가 같은 조성이어야** | 우리 AM 70.3 wt% vs 문헌 80~90.  조성이 다른 값에 맞추면 **조성 불일치를 재료 파라미터에 밀어 넣는다**.  ⇒ CL-46 의 "Lee 조성 침대 1건" 이 선행 조건 (**미실행**) |
| ⓑ **맞춘 뒤 그 일치를 검증으로 못 쓴다** | frame[4] — 실험에 맞춘 것이 실험과 맞는다고 쓰면 순환.  "보정했다" 로만 |
| ⓒ **σ_VGCF 는 편향 넷 중 하나만 먹는다** | 접촉저항 삭제(#1)만 σ 로 흡수된다.  PTFE 코팅 미표현(#2)·과압축(#3)·격자(#4)는 **기하** 문제라 σ 로 맞추면 **숨는다** |

⚠ **#2 에 대한 옛 문장은 과했다** (R8 Q4-b).  *"비대칭이라 σ 로 **원리적으로** 못 고친다"*
는 틀렸다 — 같은 scalar 라도 **두 topology 의 민감도가 달라 비는 움직인다.**
정확한 서술: **PTFE-specific bias 를 인과적으로 교정하거나 식별할 수 없다.**

⚠ **ⓐ 는 필요조건일 뿐 충분조건이 아니다** (R8 Q4-b).  같은 조성 외에 **압밀압 ·
밀도/공극률 · 두께 · 온도 · 탄소 형상과 분산 · 집전체 경계/접촉 처리**를 맞춰야 한다.
그리고 **한 scalar 로 두 전극의 두 절대 target 을 동시에 맞출 수 있다는 보장이 없다.**

⚠⚠ **"헤드라인 불변" 을 보정의 근거로 쓰는 논법은 순서가 틀렸다** (R8 Q4-c).
CL-39 의 `dR/dlnσ_VGCF = −0.0099` 는 **옛 geometry 의 좁은 ×1.44 국소 결과**라 W4 나 더 큰
보정 범위의 불변성을 **보증하지 않는다**.  그리고 "보정한 뒤에 불변을 확인" 하면 그때는
**이미 보정을 한 뒤**다.

**⇒ 바로잡은 순서** (측정 먼저, 보정 나중, 그 다음 holdout):

1. 같은 조건의 **anchor 와 calibration observable · σ 범위를 사전 고정**
2. 그 **전체 후보 범위**에서 절대 σ 와 ratio 민감도를 **보정 전에 측정**
3. 한 조건으로 **calibration**
4. **사용하지 않은 구조·조건**으로 **holdout validation**

⚠ **holdout 이 없으면 최종 표기는 `calibrated` 이지 `validated` 가 아니다.**

선행 조건은 여전히 **Lee 조성 침대 1건**(같은-조성 앵커, CL-46 지목, 미실행)이다 —
그것이 없으면 1단계의 anchor 자체가 없다.  **지금은 σ 를 건드리지 않는다.**
