# Bruggeman 식 · Tortuosity 세 가지 · network solver — 지금 리포 기준 정리 (2026-10-02)

> 계기: 사수 질문 — *"Bruggeman 의 τ 를 Dijkstra 말고 모든 경로 (입계 뺀 network solver 버전) 로 구하자"*.
> 옛 설명 (다른 세션) 을 지금 코드 · 원장에 대조해 다시 적는다.  같은 날 라벨 정정 커밋 (§7) 과 한 묶음.

## 1. 식이 무엇인가

```
σ_brug = σ_grain · φ_SE · f_perc / τ²
```

- **복합양극 전체의 유효 이온전도도 어림식** — SE 재료값 σ_grain 을 전극 스케일로 깎는다 (고전 porous-electrode 식 σ₀·ε/τ² + 퍼콜레이션 보정).
- 코드: `scripts/dem_analysis_core.py` `calc_effective_conductivity` (σ_brug / σ_grain = φ_SE × f_perc / τ²).
- 웹앱: 케이스 화면 **'σ_brug / σ_ionic'** 행 = 이 식 ÷ network solver (케이스마다 다르다).

## 2. 각 항 — 지금 코드의 정의

| 항 | 정의 | 근거 |
|---|---|---|
| σ_grain | **3.0 mS/cm = LPSCl 펠릿값** (Cronau 2021 SI 그림 S2c µC 펠릿 평탄 구간 2.88–3.46 의 하단).  펠릿 자체의 입계 (와 잔류 기공) 가 이미 들어 있다 · 온도는 Arrhenius 보정 | `scripts/se_material.py` · 원장 `CL-91` (옛 "단결정 · GB 없음" 라벨 철회 = `SELF-51`) |
| φ_SE | SE 구 부피 합 ÷ (가로 × 세로 × 판 간격) — **겹친 부피를 두 번 세는** 구 부피 합 규약 (union 과 안 닫힌다) | `dem_analysis_core.py` `calc_effective_conductivity` (LHS 인계표는 질량 보존 φ 를 따로 쓴다 · J20-e) |
| f_perc | 바닥 · 가압판 띠에 **모두 닿는** SE cluster 에 속한 SE 수 ÷ 전체 SE 수 (띠 = SE 마다 자기 반지름 2 배 안) | `calc_percolation` (`percolation_pct`) — 개수 비율이지만 우리 침대는 SE 크기가 하나라 부피 비율과 같다 |
| τ | **기하학적 Dijkstra τ** — 바닥 SE → 가압판 SE 최대 200 쌍의 최단 경로 ÷ 높이 차 (흩어짐이 크면 중앙값 = `tortuosity_recommended`) | `calc_tortuosity` |

## 3. Tortuosity 세 가지

| 이름 | 식 | 뜻 | 웹앱 표기 |
|---|---|---|---|
| τ_Dijkstra | 최단 경로 ÷ 높이 차 (쌍마다 길 하나) | 기하학적 우회만 | τ_Dijkstra — geodesic-only |
| **τ_Laplace,bulk** | √(φ_SE · σ_grain / σ_bulk_net) | 접촉 저항을 0 으로 둔 네트워크 (CONTACT_FREE) 로 역산 — **모든 병렬 경로 · 입계 (접촉) 제외** | τ_Laplace,bulk — without constriction |
| τ_Laplace,eff | √(φ_SE · σ_grain / σ_full) | 접촉 (Holm 협착) 까지 넣은 네트워크로 역산 — **COMSOL · EIS 입력** | τ_Laplace,eff ⭐ |

- 역산은 **φ_SE 만으로** 한다 (f_perc 없음 · `webapp/app.py` τ 비교 블록) → 고립 SE 벌점이 τ 안에 이미 들어 있다.
- 정의상 정확한 관계: **τ_Laplace,eff² = τ_Laplace,bulk² × (σ_bulk_net ÷ σ_full)**.
- **Laplace τ 를 Bruggeman 식에 넣으면 항등식**이다 (네트워크 σ 를 그대로 되돌려 준다).  예측으로서 의미가 있는 것은 기하학적 τ 를 넣었을 때뿐이다.
- 예 (웹앱 화면의 한 케이스): Dijkstra 1.25 · Laplace,bulk 1.13 · Laplace,eff 2.24 → (2.24 ÷ 1.13)² ≈ **3.9** = 이 전극에서 접촉 저항이 이온 전도도를 낮추는 배수.
  bulk 가 Dijkstra 보다 작은 것은 정상 — 전류가 여러 길로 나뉘어 흐르므로 길 하나의 우회보다 덜 깎인다 (Laplace τ 는 길이가 아니라 "전도도가 얼마나 줄었나" 를 τ 꼴로 바꾼 값).
- 웹앱의 'Constriction overhead' 는 τ_eff ÷ τ_Dijkstra (위 예 1.80) 다.  접촉 효과만 보려면 둘 다 Laplace 인 τ_eff ÷ τ_bulk (1.98 · 전도도로 3.9 배) 가 더 깨끗하다 (웹앱 표 추가는 미정).

### 3-1. τ_Laplace,bulk — 정말 모든 경로인가 · 왜 작게 나오나

**모든 경로가 맞다 (나열하지 않고 한 번에).**  `network_conductivity.solve_network` 는 감지된 SE–SE 접촉 **전부**를 간선으로 둔
그래프에 두 전극 띠 사이 전압을 걸고, 모든 입자에서 "들어온 전류 = 나간 전류" 인 Kirchhoff (Laplacian) 연립방정식 L·V = b 를 푼다
(CG → ILU-CG → spsolve).  각 입자의 전류 수지에 그 입자의 모든 접촉이 들어가므로 두 전극을 잇는 **모든 경로가 자기 컨덕턴스만큼 동시에**
전류를 나른다 — 경로를 세거나 표본을 뽑지 않는다 (Dijkstra 는 최대 200 쌍 표본 · 쌍마다 길 하나).  막다른 가지에는 전류가 거의 흐르지 않고,
전극에 닿지 않는 고립 cluster 는 빠진다.  단 "모든 경로" 는 **모델이 감지한 접촉 그래프 안의** 모든 경로다.

**작게 나오는 이유 — 물리 하나 · 모델 하나.**

1. **병렬 경로 (물리)** — 전류는 곧고 넓은 길로 더 많이 흐르고 여러 길로 나뉜다.  그래서 망 전체의 전도도 손실은 "평균적인 한 길의 우회"
   (Dijkstra) 보다 작고, 그것을 τ 꼴로 바꾼 값도 작다.
2. **입자 내부 저항 모델 (모델)** — CONTACT_FREE 모드의 간선 저항은 `R_bulk = (d/2)/(σ·π·r₁²) + (d/2)/(σ·π·r₂²)` 다
   (`network_conductivity.py:401–403`): 입자 중심에서 접촉점까지를 **입자 단면 전체 (π r²) 의 원기둥**으로 둔다.
   - 한 입자의 접촉 (SE 배위수 ≈ 5) **마다** 단면 전체를 따로 주므로, 단면이 접촉끼리 나뉘지 않는다 → 같은 구 부피보다 전도 물질이
     많은 것처럼 계산된다.
   - 한 입자를 지나는 직렬 길 (반원기둥 둘 = 길이 2r · 단면 π r²) 의 저항 2/(σπr) 도 **같은 부피의 원기둥** (단면 ⅔ π r²) 의
     3/(σπr) 보다 작다.
   - ⇒ σ_bulk_net 이 연속체 기준보다 크게 나오고, 그것을 σ_grain · φ_SE 로 나눠 역산한 τ_Laplace,bulk 는 **작게 (1 에 가깝게, 1 보다
     작을 수도)** 나온다.  이 값은 순수한 길이가 아니라 **이 입자 내부 저항 모델 아래의 유효값**이다.
3. (반대 방향 · 작음) φ_SE 는 구 부피 합이라 겹친 부피를 두 번 센다 → φ_SE 가 커져 역산 τ 를 조금 키운다.

⇒ τ_Laplace,bulk 를 Dijkstra 와 길이처럼 1:1 비교하지 말 것.  쓸모는 **같은 모델 안의 분해** (τ_eff² = τ_bulk² × 접촉 배수) 에 있다.
절대값으로 쓰려면 입자 내부 저항을 부피에 맞게 보정한 판 (단면을 접촉끼리 나누거나 구 부피와 같은 원기둥) 과 비교해 보는 것이 먼저다 (⬜ 미실행).

## 4. 스케일링 법칙 이력 — Bruggeman 에서 회귀식으로

| 단계 | 형태 | 결과 |
|---|---|---|
| 출발 (`docs/Scaling_Law_Report_Full.md` §2.1) | σ_grain × φ_SE × f_perc / τ² (**τ = 기하학적**) | network solver 대비 **R² ≈ 0.30** — 일정 배수가 아니라 케이스마다 들쭉날쭉 (접촉 저항 없음 · τ² 과벌점) |
| v2.0h | σ_brug × R_comp, R_comp = τ^1.5 / f_perc | 보정 배수가 τ⁻² 를 상쇄 → 실효 τ 지수 −0.5 |
| v2.0i · FORM X | C × σ_grain × (φ_SE − φc)^¾ × CN × √cov / √τ | 맞춘 상수 배수 C + 퍼콜레이션 · 배위수 · 접촉 면적 |
| **최종 T1** | σ_grain · Cronau(r_SE) · √φ_eff · CN² · √cov_Hertz · f_p³ · exp(a + b ln τ + c ln²τ) | 적합 계수 5 · n 88 · **LOOCV 0.975** · τ = 같은 기하학적 τ · 상수 배수가 τ 에 따라 변하는 배수 C(τ) 로 · 접촉 효과는 CN² · √cov 가 맡는다 |

교과서 Bruggeman 은 τ 를 재지 않고 φ 에서 정한다 (σ ∝ φ^1.5 → 길이비 τ = φ^−0.25 · tortuosity factor = φ^−0.5).  우리 "Bruggeman" 은 그 꼴에 **잰 기하학적 τ** 를 넣은 변형이다.

## 5. 사수 제안 — τ 를 "모든 경로 · 입계 제외" 로 = τ_Laplace,bulk

- **이미 계산되고 있다** (§3 둘째 줄).  모든 경로를 하나씩 세지 않는다 — Kirchhoff 연립방정식 한 번이 병렬 경로 전부를 반영한다 (미지수 = 입자 수, 7:3 전극 16 만 개 → 수 초).
- 이것을 Bruggeman 에 넣으면 정의상 σ_bulk_net 이 나온다 → **Bruggeman ÷ network = σ_bulk_net ÷ σ_full = CF/FULL = 접촉 배수만 남는다**.
  기존 열 (`R_brug_over_full`, 이름과 달리 CF/FULL) 로 n = 157 중앙값 4.04 배 (Hertz 면적) · 6.69 배 (소성 면적) · 범위 2.3–13.6 배 — ⚠ **같은 접촉 모델 안의 비**이지 실험 대비 오차가 아니다 · 이 배수는 재계산되지 않았다 · 다른 솔버에 하나의 보정 배수로 옮길 수 없다 (`CLAUDE.md` CL-81 블록 · L2 판정).
- 그러면 회귀는 접촉 배수 하나만 설명하면 된다:
  `σ_full = σ_grain · φ_SE / τ_Laplace,bulk² × g(접촉: coverage · 배위수 · 접촉 면적)` — 경로 (기하) 와 접촉이 깔끔히 나뉜다.
- **한계**: τ_Laplace,bulk 는 solver 를 돌려야 나오는 값이다 → 설계값만으로 σ 를 예측하는 용도에는 Dijkstra τ 보다 쓰기 어렵다 (원인 분해 · 해석 용도에 적합).
- ⬜ 제안 (비준 전): ① 기존 케이스로 τ_Laplace,bulk ↔ τ_Dijkstra 비교 ② 접촉 배수 g 의 회귀.

## 6. 옛 설명 대조

| 옛 설명 | 판정 | 지금 리포 기준 |
|---|---|---|
| σ_grain = GB 없는 재료값 | ✘ | 펠릿값 — 펠릿 입계 포함 (`SELF-51` · `CL-91`) |
| φ_SE = 전극 부피 중 SE 비율 | ✔ (보충) | 구 부피 합 → 겹친 부피를 두 번 센다 |
| f_perc = 양 끝을 잇는 비율 | ✔ | 개수 비율 (단일 SE 크기라 부피 비율과 같다) |
| 1/τ² = 길이 · 단면 두 번 벌점 | ✔ | — |
| 기하 τ 면 GB · 협착이 통째로 빠진 상한 | △ | 빠지는 것은 **입자 사이 접촉 (협착) 저항** (네트워크 저항의 70–80 %).  펠릿 입계는 σ_grain 에 이미 있으므로 "엄밀한 상한" 은 아니다 |
| 펠릿 σ + τ_eff → GB 두 번 | ✔ (지금 해당) | 네트워크 (FULL) 는 펠릿 σ_grain 위에 Holm 접촉 저항을 더한다 → 입자 경계 효과가 **일부 두 번** 들어갈 수 있다 (크기 미상 · 재해석 = 저자 결정 대기 · `CLAUDE.md` CL-81 블록) |
| τ²_eff = τ²_geom (1 + R_GB/R_bulk) | △ | 리포 관계는 τ_Lap,eff² = τ_Lap,bulk² × (σ_bulk_net ÷ σ_full) (정의상 정확) · (1 + R/R) 꼴은 접촉이 고르게 직렬일 때만 |
| Laplace τ + f_perc = 이중 벌점 · Laplace τ 면 항등식 | ✔ | τ_Laplace 는 φ_SE 만으로 역산 |
| τ 와 τ² 표기 | ✔ | 리포 = 길이비 τ · /τ² |
| 스크립트마다 percolation 정의가 다르다 | 해당 없음 | 그 변수들 (`SE_percolated_fraction` 등) 은 지금 리포에 없다 (외부 스킬 스크립트) · 지금 f_perc 정의는 하나 |

## 7. 정정 (2026-10-02 · 1저자 비준 · J20-l 코드 → 웹앱 같은 묶음)

- `dem_analysis_core.calc_effective_conductivity` docstring: "network solver 대비 3–10 배 과대" 철회 → 비는 케이스마다 ('σ_brug / σ_ionic') · 3–10 배는 CF/FULL (L2-07) 에서 온 숫자.
- 그룹 비교 그림 `r_brug_comparison` (키 · 파일명 · CSV 머리는 그대로): 범례 'R_brug' → 'CF/FULL' · y = 1 문구 'Bruggeman = exact' → '1 = no contact resistance' · 제목 'Bruggeman Overestimation' → 'Contact-resistance factor … (not Bruggeman · L2-07)' · 그림 목록 제목 · 설명 · `group.html` 체크박스 이름 '접촉 배수 (CF/FULL)'.
- 회귀 시험 `webapp/test_cf_full_labels.py` (옛 코드 1 PASS · 10 FAIL → 11/11) · `scripts/check_all.sh` 등록.

## 8. 한정어 (인용할 때 붙일 것)

- σ_grain 은 펠릿값 — 네트워크 σ (FULL) 는 그 위에 Holm 접촉 저항을 더하므로 부분 이중계상 가능 (크기 미상).
- 웹앱 τ (띠 = SE 자기 반지름 2 배) 와 슬라이드 · 인계표 τ (수확기 벽 띠 = 가장 큰 SE 반지름) 는 띠 정의가 달라 숫자가 조금 다를 수 있다.
- CF/FULL · Bruggeman ÷ network 은 모두 **같은 모델 안의 비**다 — 실험 대비 오차로 읽지 않는다.
