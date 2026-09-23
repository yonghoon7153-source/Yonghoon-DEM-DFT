# HIRSCHORN2010 — Determination of effective capacitance and film thickness from constant-phase-element parameters

> **읽은 기록 (불변).** 에이전트가 2026-09-23 에 PDF 를 읽고 쓴 노트다. 기계용 기록은
> `packages/wrdkit/src/wrdkit/eis/knowledge/hirschorn2010.json` 이다. 아래에서 말하는 JSON 이 그것이고,
> 원문 인용은 코드가 인용하는 기록에만 남겼다. "우리 코드" 와의 대조는 그날 02:10–02:30 UTC
> 작업 트리 기준이다. 그 뒤 무엇을 고쳤는지는 `docs/syntheses/eis-paper-knowledge.md` 에 있다.
> PDF 는 저장소에 넣지 않는다 (저작권).

## 서지

- Bryan Hirschorn, Mark E. Orazem, Bernard Tribollet, Vincent Vivier, Isabelle Frateur,
  Marco Musiani, "Determination of effective capacitance and film thickness from
  constant-phase-element parameters", *Electrochimica Acta* **55** (2010) 6218–6227.
- DOI: 10.1016/j.electacta.2009.10.065 (PDF 1쪽에 인쇄되어 있음).
- 쪽 번호: 인쇄 쪽 = PDF 쪽 + 6217. 아래 (p. N) 은 모두 인쇄 쪽이다.
- 구조화 기록: `HIRSCHORN2010.json` (레코드 30개, 우리 코드와의 대조 10건).

## 한 줄 요지

CPE 파라미터에서 유효 커패시턴스를 구하는 식은 Brug 식 (11)·(12) 와 Hsu–Mansfeld 식 (18) 모두
`C_eff = Q^(1/α)·R*^((1−α)/α)` 꼴이다. R* 에 어느 저항을 넣을지는 회로 모양이 아니라 CPE 의
**기원**이 정한다. 표면을 따라 퍼진 분포(surface)면 R_e∥R_t 를 넣고, 블로킹이면 R_e 를 넣는다.
두께 방향 분포(normal)면 R_f 를 넣는다. 잘못 고르면 수십 % 에서 자릿수 단위까지 틀린다.

## 핵심 내용

- CPE 표기는 `Z = R_e + R_t/(1 + (jω)^α Q R_t)` 이다. 우리 `circuit.py` 의 `1/(Q (jω)^n)` 와
  같은 규약이다. α < 1 이면 Q 는 커패시턴스가 아니다 (p. 6218).
- 블로킹 전극은 `Z = R_e + 1/((jω)^α Q)`, 즉 옴 저항과 CPE 의 직렬이다 (p. 6218).
- Hsu–Mansfeld [11] (Corrosion 57 (2001) 747) 은 Q, α, ω_max (−Z'' 가 최대인 주파수) 로 관계를
  제시했다 (p. 6218).
- 시정수 분포는 두 가지다. 하나는 전극 표면을 따라 퍼진 분포(surface), 다른 하나는 표면에
  수직으로 퍼진 분포(normal)다 (p. 6219).
- surface 분포에서는 어드미턴스가 더해진다. 옴 저항이 없으면 `1/R_eff = Σ1/R_i`, `C_eff = ΣC_i`
  인 이상적 RC 하나로 모인다. 그러므로 surface 분포가 CPE 를 만들려면 옴 저항이 필요하다
  (p. 6219).
- normal 분포에서는 임피던스가 더해지고 (Voigt 직렬), 옴 저항 없이도 CPE 가 된다. R_e 는 분산에
  기여하지 않으므로 `Z − R_e` 로 다룬다 (p. 6219).
- 식 (11) 은 Brug 의 surface·패러데이 식이다:
  `C_eff = Q^(1/α)·(R_eR_t/(R_e+R_t))^((1−α)/α)`. τ0 는 어드미턴스 형태에서 정의되며
  (식 (8)·(9)), Nyquist 꼭지에서 정의되지 않는다 (p. 6219).
- 식 (12) 는 Brug 의 surface·블로킹 식이다 (R_t → ∞): `C_eff = Q^(1/α)·R_e^((1−α)/α)` (p. 6219).
- 식 (18) 은 normal 분포 식이다: `C_eff = Q^(1/α)·R_f^((1−α)/α)`, `τ0^α = (R_f C_eff)^α = Q R_f`.
  Hsu–Mansfeld 가 유도 없이 ω_max 로 쓴 식 (3) 과 같다. 세 식은 꼴이 같고 저항만 다르다
  (p. 6220).
- 그래프 방법은 `α = |d log|Z_j|/d log f|`, `Q_eff = sin(απ/2)·(−1/(Z_j ω^α))` 이다. 회귀와 같은
  값을 준다. 특성 주파수보다 한 decade 위 구간을 썼고, α 는 기울기를 잰 주파수에 따라
  달랐다 (p. 6220).
- 원판 전극 시뮬레이션 (Huang et al.) 은 기하 유래 surface 분산을 다룬다. 변수는 `K = ωC0r0/κ`,
  `J = (4/π)R_e/R_t` 이다. 여기서 Q 를 그대로 C 로 쓰면 K = 100 에서 약 500% 오차가 난다
  (p. 6221).
- 같은 시뮬레이션에서 세 식의 오차 (p. 6221):
  - 식 (12): α 를 K < 5 에서 구하면 맞고, K > 5 에서는 틀린다 (그림 4a 로 읽으면 최대 약 1.5배).
  - 식 (11): 오차 20% 미만으로 가장 좋다.
  - 식 (18): −70% ~ +100% 틀려서, surface 분포에는 부적절하다.
- Nb 산화막은 300 Hz 이상에서 기울기가 −0.90 이라 α = 0.90 이다. 기하 유래 surface 분산은
  K = 1 (약 65 kHz) 에서야 보이는데 최고 측정 주파수가 63.1 kHz 였다. 그래서 막 기원 (normal)
  으로 판단했다 (p. 6221).
- 막 두께는 `d_eff = εε0/C_eff` (ε0 = 8.8542×10⁻¹⁴ F/cm) 로 구하며, ε 가 위치에 무관하다고
  가정한다 (p. 6222).
- 표 1 (Nb2O5, ε = 42) 을 식 (18) 로 계산하면 d_eff 는 문헌 두께 (표 2: 11/10/7, 22/19/15,
  33/28/24 nm) 와 잘 맞는다 (p. 6222):

  | E (V vs SCE) | α | Q (Ω⁻¹cm⁻²sᵅ) | R_f (kΩcm²) | C_eff (µF/cm²) | d_eff (nm) |
  |---|---|---|---|---|---|
  | 2 | 0.95 | 5.9e-6 | 1.30 | 4.6 | 8 |
  | 6 | 0.90 | 3.5e-6 | 2.01 | 2.0 | 18 |
  | 10 | 0.88 | 2.5e-6 | 3.65 | 1.3 | 29 |

- 같은 Nb 에 surface 식 (R_f ≫ R_e 라 식 (11) = 식 (12)) 을 쓰면 3.2, 0.9, 0.5 µF/cm² 와
  12, 41, 74 nm 가 나온다. 두께가 너무 크고, 고전위일수록 더 벌어진다. R_e 값은 인쇄되지
  않았다 (p. 6222).
- 표 3 (피부, ε = 49) 은 α 0.824–0.838, Q 5.36–6.13×10⁻⁸, R_f 42–60 kΩcm² 에서 C_eff
  1.66–1.86×10⁻² µF/cm², d_eff 2.3–2.6 µm 를 준다. 알려진 두께 10–40 µm 보다 훨씬 작다
  (p. 6223).
- 피부에서는 식 (12) 가 9.6–14 µm 로 기대값에 더 가까웠다. 하지만 R_e 는 피부의 유전 성질과
  무관하므로 겉보기 일치일 뿐이다 (p. 6223).
- Young 모델은 ε 가 균일하고 저항률이 ρ(x) = ρ0 e^(−x/λ) 로 줄어드는 막이다. 저주파 극한은
  `ρ0λ(1 − e^(−δ/λ))`, 고주파 극한은 `εε0/δ` 다. 분산은 ωεε0ρ0 > 1 인 고주파에서만 나타나므로
  저주파 거동은 설명하지 못한다 (p. 6224).
- 논문은 Young 임피던스를 전해질 저항과 직렬인 R_f–CPE 병렬로 해석하고 식 (18)·(25) 를
  적용했다. 우리 `R0-p(R1,CPE1)` 과 같은 해석이다 (p. 6224).
- 유한한 주파수 구간에서 d_eff 는 λ 와 δ 사이에 놓인다. δ/λ = 400 이면 ωεε0ρ0 = 10⁵ 에서도
  δ 보다 두 자릿수 작다. 저항률이 크게 변하면 가장 저항이 큰 부분만 보인다 (p. 6225).
- Nb (6 V) 에 Young 모델을 회귀하면 ε = 42, ρ0 = 2.66×10⁹ Ωcm, δ = 30 nm, λ = 8 nm 다.
  5 kHz 이상에서 α ≈ 1, d_eff/δ ≈ 1 이다 (p. 6225).
- 피부 (표 4) 는 ρ0 = 4–6×10⁸ Ωcm, ε = 49, λ = 1 µm, δ = 20 또는 40 µm 다. 50 kHz 에서
  α 는 0.839–0.858, d_eff/δ 는 0.074–0.152 다 (p. 6226).
- 결론 (p. 6226):
  - Brug 식은 surface 분포에만, Hsu–Mansfeld 식은 normal 분포에만 맞다.
  - 틀린 유효 저항을 쓰면 거시적인 오차가 난다.
  - 어느 식인지는 국소 임피던스나 분광법 같은 다른 방법으로 얻은 계의 지식에 근거해 골라야
    한다.

참고: 이 논문에는 **power-law 모델과 g(α) 보정 인자가 없다.** power-law 모델은 같은 그룹의
후속 논문 (J. Electrochem. Soc., 2010) 에 있는 것으로 알려져 있으나 여기서 확인하지 않았다.
고체 전해질이나 펠릿도 다루지 않는다. α 의 하한도 제시하지 않는다. 실험 α 는 표 1·3 의
0.824–0.95 뿐이다.

## 우리 코드에 대한 함의

1. **식의 이름에 가정을 적는다.** `capacitance.py` 의 식은 Hirschorn 식 (18) (normal 분포,
   Hsu–Mansfeld ω_max 식과 동치) 이다.
   - 독스트링의 "also the parallel case in Hirschorn" 을
     "Hirschorn et al. Eq. (18), normal distribution" 으로 고친다.
   - ADR 0040 §4 에 "두께 방향(normal) 분포 가정" 을 적는다.
   - 근거: `HIRSCHORN2010.hsu-mansfeld-normal-eq18`, `HIRSCHORN2010.brug-surface-hsu-mansfeld-normal`.
2. **분포 유형을 인자로 받는다.** 예: `effective_capacitance(r, q, n, *, basis="normal")`.
   - `normal`: 아크 자신의 R.
   - `surface_faradaic`: R_e∥R_t.
   - `surface_blocking`: R_e.
   - `ArcCapacitance` 에 `basis` 와 실제로 쓴 R 을 저장한다.
   - 근거: `HIRSCHORN2010.same-form-only-resistance-differs`.
3. **벌크·입계 아크는 지금처럼 식 (18) 을 쓴다.** 논문이 `R_e + (R_f ∥ CPE)` 를 바로 식 (18) 로
   읽는다. 게다가 옴 저항이 없는 표면 (병렬 기둥) 분포는 이상적 RC 로 모인다. 그래서 펠릿의
   두께 방향 아크에서 n < 1 이면 normal 쪽이라는 것이 우리 추론이다.
   근거: `HIRSCHORN2010.young-analysed-as-rf-cpe`, `HIRSCHORN2010.surface-cpe-needs-ohmic-resistance`.
4. **Li|SE|Li 의 계면 (전하전달) 아크는 두 값을 낸다.**
   - 식 (18) 과 식 (11) 을 함께 내고, R_e 는 R0 + 앞선 아크 저항으로 둔다. 다중 아크
     회로에서 R_e 를 이렇게 잡는 것은 우리 추론이다.
   - n < 1 이면 식 (11) 값이 **항상** 우리 값보다 작다. 그래서 "너무 커서 X 일 수 없다" 는
     판정은 surface 해석에서 뒤집힐 수 있고, "너무 작아서 X 일 수 없다" 는 판정은 그대로다.
   - `label_contradicts_capacitance` 는 두 값이 모두 라벨 범위를 벗어날 때만 `문제` 로 낸다.
   - 근거: `HIRSCHORN2010.brug-surface-faradaic-eq11`,
     `HIRSCHORN2010.eq18-on-surface-distribution-wrong`.
5. **블로킹 꼬리 (SS|SE|SS 의 직렬 CPE3) 에도 커패시턴스를 붙인다.**
   - 식 (12): `C = Q3^(1/n3)·R_e^((1−n3)/n3)`. R_e 는 꼬리 앞 직렬 저항의 합 R0+R1+R2 로 둔다
     (우리 추론).
   - 병렬 식은 쓸 수 없다. 넣을 R_f 가 없다.
   - 대칭셀은 같은 계면 둘이 직렬이므로 계면 하나의 값은 2·C/A 다. 이것은 회로 산수이고
     논문 밖의 내용이다.
   - n3 ≈ 0.9 면 R_e 가 10배 틀려도 C 는 1.29배만 변한다.
   - 검수의 `tail_mimicked_by_arc` 도 같다. 꼬리를 흉내 낸 p(R,CPE) 아크의 커패시턴스는 그 아크의
     R (경계 1e9 Ω 이거나 외삽값) 로 낸 식 (18) 값이 아니라, `Q^(1/n)·R_e^((1−n)/n)`
     (R_e = r0 + 꼬리 앞 구간 안 아크 저항) 로 내야 한다. n = 0.85 에서 경계 R = 1e9 Ω,
     R_e = 100 Ω 이면 지금 값이 17배 크다 (우리 계산).
   - 근거: `HIRSCHORN2010.brug-surface-blocking-eq12`,
     `HIRSCHORN2010.blocking-electrode-re-plus-cpe`.
6. **테스트 앵커.** 면적 규격화 입력이고 결과는 F/cm² 이다.
   - `effective_capacitance(1300, 5.9e-6, 0.95) ≈ 4.566e-6`
   - `(2010, 3.5e-6, 0.90) ≈ 2.018e-6`
   - `(3650, 2.5e-6, 0.88) ≈ 1.318e-6`
   - `(60000, 6.13e-8, 0.824) ≈ 1.851e-8`
   - `(51000, 5.36e-8, 0.834) ≈ 1.656e-8`
   - `(42000, 5.40e-8, 0.838) ≈ 1.664e-8`

   인쇄값과 유효숫자 2자리로 맞는다. d_eff 는 5% 정도 허용한다 (10 V 행은 28.2 nm 대 29 nm).
   식 (12) 앵커는 R_e 가 인쇄되지 않아 만들 수 없다. 전체 셀 값으로 계산해 A 로 나눠도 면적
   규격화 입력과 정확히 같다 (식이 동차다). 근거: `HIRSCHORN2010.nb-oxide-table1-anchor`,
   `HIRSCHORN2010.skin-table3-anchor`.
7. **맞춤 없이 n 을 교차검증한다.**
   - 각 아크의 고주파 쪽과 저주파 꼬리에서 `|d log|Z''|/d log f|` 를 재어 맞춘 n 과 비교한다.
   - 직렬 꼬리에서는 식 (20) 이 Q 까지 정확히 준다.
   - 기울기가 구간에 따라 변하면 pseudo-CPE 다. 이때 맞춘 n 하나는 평균값일 뿐이다.
   - 근거: `HIRSCHORN2010.graphical-alpha-and-q`.
8. **겉보기 εr 을 보고한다.** `εr = C·l/(ε0·A) = per_length / 8.8542e-14` 다. 재료 값보다 훨씬
   크면 그 아크는 펠릿 전체가 아니라 더 얇은 저항층 (계면층, 입계) 의 것일 수 있다. 논문은
   황화물의 εr 을 주지 않으므로 임계값은 따로 정해야 한다. 근거:
   `HIRSCHORN2010.film-thickness-eq25`, `HIRSCHORN2010.only-most-resistive-part-probed`,
   `HIRSCHORN2010.deff-between-lambda-and-delta`.
9. **n 이 낮으면 판정을 넓히거나 보류한다.** 두 저항 선택의 비는 `(R_a/R_b)^((1−n)/n)` 이다
   (우리 대수).

   | n | 저항 비 | C 비 |
   |---|---|---|
   | 0.9 | 1000 | ×2.15 |
   | 0.7 | 100 | ×7.2 |
   | 0.6 | 1000 | ×100 (Irvine 표 두 줄) |

   근거: `HIRSCHORN2010.misuse-gives-macroscopic-errors`.
10. **경계 근처 값은 모호로 둔다.** 올바른 식도 20% 가까이 틀리고, 분포 가정이 틀리면
    0.3–2배 틀린다. 그러니 범위 경계에서 ×3 안쪽의 값은 모순이 아니라 후보 둘로 처리한다.
    ×3 은 우리가 고른 임계값이다. 근거: `HIRSCHORN2010.eq11-best-within-20pct`,
    `HIRSCHORN2010.eq18-on-surface-distribution-wrong`.
11. **기대에 맞는 식을 고르지 않는다.** 분포 가정은 숫자를 보기 전에 아크 종류별로 정해 둔다.
    피부 예가 주는 교훈이다. 근거: `HIRSCHORN2010.skin-eq12-closer-for-wrong-reason`,
    `HIRSCHORN2010.choose-formula-from-system-knowledge`.
12. **원판 전극의 K 를 펠릿에 옮기지 않는다.** 양면을 전극이 덮은 펠릿은 절연면에 박힌 원판이
    아니다 (우리 추론). 근거: `HIRSCHORN2010.disk-dimensionless-frequency-k`.

## 우리 코드와 어긋나는 것

식과 수치 구현은 표 1·3 을 그대로 재현한다. 어긋나는 것은 대부분 적용 범위와 이름이다.
틀린 값 (`wrong`) 은 하나로, 읽을 때 아직 커밋되지 않은 작업 트리 코드에 있다.

- **`audit.py` 의 `tail_mimicked_by_arc` (wrong, 작업 트리):** 블로킹 꼬리를 흉내 낸 아크의
  커패시턴스를 그 아크 자신의 R 로 낸다. 그 R 은 맞춤 경계 1e9 Ω 이거나 외삽값이라, n < 1 이면
  숫자가 경계값에 따라 달라진다. 논문은 블로킹 계면 (R_e 와 CPE 의 직렬) 에 식 (12) 를 쓰고
  옴 저항 R_e 를 넣는다 (p. 6218, p. 6219). 저항을 잘못 쓰면 거시적 오차가 난다 (p. 6226).

- **`capacitance.py` (imprecise):** 모든 p(R,CPE) 아크에 식 (18) 을 조건 없이 쓴다. 논문은 이 식을
  normal 분포에만 준다 (p. 6220, p. 6226). surface 분포라면 식 (11) 이 맞다 (p. 6219). surface
  분포에 식 (18) 을 쓰면 −70% ~ +100% 틀린다 (p. 6221). 계면 아크는 surface 분포일 수 있다.
- **`capacitance.py` 독스트링 (imprecise / fine):** "also the parallel case in Hirschorn" 은
  부정확하다. Hirschorn 의 "parallel combination" 은 식 (11) 의 R_e∥R_t 다 (p. 6220). Hsu &
  Mansfeld, Corrosion 57, 747 (2001) 인용 자체는 논문의 참고문헌 [11] 과 같다 (p. 6226).
- **ADR 0040 §4 (imprecise):** 꼭지 기준 (τ = RC) 정의가 normal 분포의 정의라는 가정이 빠졌다
  (p. 6220).
- **`audit.py` 의 `label_contradicts_capacitance` (imprecise):** 한 가지 식의 값만으로 `문제` 를
  낸다. surface 해석이면 값이 작아지므로 "너무 크다" 쪽 판정은 뒤집힐 수 있다 (p. 6219,
  p. 6221). 작업 트리의 `arcs_are_electrode` 도 같은 값에 기댄다. 다만 벌크와 전극 사이는
  여러 자릿수라, n 이 낮고 R0 ≪ R_arc 일 때만 위험하다.
- **직렬 CPE, 블로킹 꼬리 (fine, 공백):** 지금은 값을 내지 않으므로 틀린 값도 없다. 붙일 때는
  식 (12) 에 R_e 를 쓴다 (p. 6219).
