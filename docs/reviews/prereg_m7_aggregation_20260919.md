# 사전등록 — `m7` 점착 비대칭이 **상별 응집**을 만드는가 (회의 [19a] · [25])

> **상태: 런 전 등록.  2026-09-19.**  이 문서가 커밋된 뒤에만 런이 유효하다.
> 계기 = 2026-09-18 이종기술 회의 (`/hetero/transcript` 발화 **19 · 25 · 35 · 36 · 38**).
> 정정 근거 = 원장 **`SELF-40`** (*"`pair_style` 한 줄로 점착이 없다고 단정했다"*).
> ★ **갱신 2026-09-19 (런 전)**: LIGGGHTS 공식 튜토리얼 대조로 §8 을 채우고 §9 에 팔 **D** 를
> 더했다.  **결과를 본 뒤가 아니라 파라미터의 *뜻*을 새로 안 뒤**의 변경이고, 초판 §8 이
> *"①②가 확인되면 런 전에 고친다"* 고 미리 적어 둔 그 변경이다.  런 뒤에는 고치지 않는다.
> ⚠ **결과를 보고 이 문서를 고치면 사전등록이 아니다.**  판정선·지표·보고창을 런 뒤에
> 옮기지 않는다 (규율: *"결과 보고 창을 옮기면 무효"*).

---

## §1. 회의가 요구한 것 (원문)

```
[19] 참석자 1  "표면 에너지가 당연히 다른 NCM·설파이드·PTFE·VGCF 4종을 섞었을 때
                어디가 응집이 되고 어디가 응집되지 않는다는 걸 보여줄 수 있는
                헤테로지니티가 나오는 결과 하나 그거 하나 필요한 거야.
                지금처럼 잘 랜덤하게 디스트리뷰션 된 게 아니라 어딘가 응집이 되어
                있는 모습이 나오는 그 결과가 하나 필요해."
[25] 참석자 1  "그거를 활물질의 표면 에너지랑 SE 랑 똑같이 만들어서 한 바퀴 돌려."
[35][36]       "전극처럼 십 몇 만 단위로 할 필요가 없고" · "이거 두 개 하면 되는 거잖아."
```

## §2. ⛔ 이 런이 **답하지 않는 것** — 먼저 적는다

1. **믹싱이 아니다.**  우리 덱의 공정은 `insert/pack`(랜덤 배치) → 정착 → 플래튼 압밀이고
   **전단 믹싱 단계가 없다** (실측 확인: `in.ps_7_3_r45.liggghts` 의 run 구조).
   문헌의 믹싱 DEM 은 회전 믹서 기하를 넣는다 (`frankenberg2024_dem_high_intensity_mixer_assb`;
   Otani 2025 *Electrochemistry* 93(6); Eirich 믹서 PEPT 2025).
   ⇒ 이 런이 재는 것은 **"점착이 있는 침전·압밀에서 생기는 상별 분리"** 다.
   ⛔ **결과를 *"믹싱 헤테로지니티"* 라고 부르지 말 것.**  [19] 의 절반이다.
2. **4종이 아니다.**  3종(AM_P·AM_S·SE)뿐이다.  덱 생성기가 4번째 원자타입을 **실제로
   거부**한다 (`make_ps_sweep_decks --selftest` 음성대조, 66 PASS).  VGCF·PTFE 는 DEM
   물체가 아니라 MPM/복셀에서 배치된다.
3. **표면에너지가 아니다.**  우리 노브는 linear hysteretic **`k_c`**(`coefficientAdhesionStiffness`),
   문헌 주류는 **JKR `Γ` (J/m²)** 다.  `m7` 균일화는 [25] 의 **대리**이지 같은 파라미터가
   아니다 (`SELF-40` §한정어).  ⬜ `k_c ↔ Γ` 관계는 미고정.

## §3. 팔 설계 — **비대칭과 크기를 같이 바꾸지 않는다**

⚠ 이 리포는 이 실수로 한 번 졌다: **게이트 ⑤ 2×2 가 대각선 비교였다** (`CL-19` retired —
스탬프와 재료계수를 동시에 바꿨다).  그래서 `m7` 도 **비대칭**과 **전체 크기**를 분리한다.

| 팔 | `m7` (AM–AM / AM–SE / SE–SE) | 무엇을 고립시키나 |
|---|---|---|
| **A 현행** | `1.0e5 / 2.0e5 / 1.0e6` | 생산 규약 그대로 (비대칭 O) |
| **B 균일-저** | `1.0e5 / 1.0e5 / 1.0e5` | 비대칭 제거, 크기 = AM–AM 수준 |
| **C 균일-고** | `1.0e6 / 1.0e6 / 1.0e6` | 비대칭 제거, 크기 = SE–SE 수준 |

- **비대칭 효과** = A vs {B, C}   · **크기 효과** = B vs C
- **B 나 C 하나만 돌리면 판정이 불가능하다** — 그 경우 비대칭과 크기가 교락된다.
- ⛔ `m7` **외의 어떤 인자도 팔 사이에서 바꾸지 않는다** (`m1`~`m6`, `m8`, `m9`, 시드 조성,
  삽입 시드, 압력, 플래튼 속도 전부 동일).  런 뒤 덱 diff 로 확인하고 그 diff 를 첨부한다.
- **시드 ≥ 3 / 팔** (팔 내 산포를 재야 판정선이 성립한다, §5).

## §4. 지표 — **런 전에 고정한다**

### 주지표 (primary): 상별 접촉 enrichment
접촉 덤프에서 상쌍별 접촉 수 `n_XY` 를 세고, **무작위 기대**로 나눈다:
```
E_XY = n_XY / n_XY^random ,
n_XY^random = N_contact · (2 - δ_XY) · f_X · f_Y        (f = 입자수 분율)
```
- `E_SE-SE > 1` = SE 가 무작위보다 **자기들끼리** 붙어 있다 = 응집.
- **왜 이것인가**: 입자수 비로 정규화되므로 조성이 달라도 비교 가능하고, **격자·구간
  나누기가 필요 없다**(Lacey 계열의 표본크기 의존을 피한다).  그리고 이 리포는 이미
  같은 형태의 양을 쓴다 (`CL-43` 의 상별 enrichment).
- 보고 대상 = **`E_SE-SE` (주)**, `E_AM-AM` · `E_AM-SE` (부).

### 부지표 (secondary): CN 기반 혼합지수 (CLMI)
입자 `i` 의 이웃 중 **다른 상**의 비율 `x_i` 를 구하고 그 표본분산으로 Lacey:
```
M = (σ₀² − σ²) / (σ₀² − σ_r²)
```
`σ₀²` = 완전분리, `σ_r²` = 완전무작위.  ⚠ **Lacey 는 표본크기에 민감**하므로 부지표로만
쓰고 주판정에 넣지 않는다.  ★ 우리는 이미 배위수를 잰다 (`se_se_cn`·`am_se_cn`) ⇒ 새로
만들 것이 없다.

### 보고창 (fixed)
- **압밀 후 정착 상태의 마지막 프레임**.  ⚠ `CL-04`/플래튼 정본대로 **정지 프레임이
  값을 정한다** — 그래서 팔 사이에 **같은 프레임 규칙**을 쓰고 그 규칙을 여기 적는다:
  `run 100000` (최종 완화) 종료 시점의 atom+contact 덤프 쌍, `ts_a == ts_c`.
- 중간 프레임을 골라 보고하지 않는다.

## §5. 판정선 — **크기를 추측하지 않는다**

이 축의 스케일을 우리는 모른다.  그래서 **절대 문턱을 지어내지 않고** 팔 내 산포로 정의한다:

```
Δ    = E_SE-SE(A) − mean{ E_SE-SE(B), E_SE-SE(C) }
SE_w = 팔 내 시드 표준오차 (시드 ≥ 3 에서 실측)
```
| 판정 | 조건 |
|---|---|
| **h1 — 비대칭이 응집을 만든다** | `Δ > 2 · SE_w` **이고** `Δ > 0` |
| **h0 — 만들지 않는다** | `|Δ| < 1 · SE_w` |
| **미판정** | 그 사이 (= 분해능 부족).  ⛔ 이때 어느 쪽으로도 쓰지 않는다 |

- 크기 효과는 따로 적는다: `E_SE-SE(C) − E_SE-SE(B)` 와 그 `SE_w` 대비.
- ⚠ **`E_SE-SE(A) > 1` 자체는 판정이 아니다** — 입자 크기 차이만으로도 접촉 통계가 기운다.
  판정은 **팔 사이 차이**로만 한다.

## §6. 음성 대조

- **C-neg**: 같은 팔을 **다른 삽입 시드**로 돌렸을 때 `E_SE-SE` 가 `SE_w` 안에 드는가.
  안 들면 시드 노이즈가 신호보다 크므로 **판정 불가**를 먼저 선언한다.
- **C-inv**: 덱 diff 가 `m7` 블록 **한 곳만** 다른가 (자동 확인, 결과에 첨부).

## §7. 비용

- 3 팔 × 3 시드 = **9 런**.  [35] 대로 전극 규모 불요 — 기존 생산 덱 크기 그대로면 충분하다
  (응집은 국소 통계라 상자를 키울 이유가 없다).
- ⬜ 조성 = [38] 대로 **기존 DEM 중 porosity 최저 바이모달 조성**.  실제 case 명은 봉인
  코호트에서 고른 뒤 이 문서에 **런 전에** 적는다.

## §8. LIGGGHTS 공식 튜토리얼 대조 — **2026-09-19 답변됨** (런 전 갱신)

사용자가 `Tutorials_public/{cohesion, hysteresis, contactModels, Mixer}` 를 제공했다.
아래는 그 실물에서 읽은 것이고, 이 절 때문에 §3 에 **팔이 하나 늘었다**(§9).

### ① LIGGGHTS 의 점착 경로는 **최소 둘**이고 우리 것은 그 중 하나다
```
# cohesion/in.cohesion  ↔  in.noCohesion  의 diff 전부
+ fix m6 all property/global cohesionEnergyDensity peratomtypepair 1 300000
- pair_style gran model hertz tangential history
+ pair_style gran model hertz tangential history cohesion sjkr
```
```
# hysteresis/in.hysteresis  ↔  in.noHysteresis
+ #ratio: maxK2 or kC to kN (normal stiffness)
+ fix m6 coefficientMaxElasticStiffness peratomtypepair 1 2.
+ fix m7 coefficientAdhesionStiffness   peratomtypepair 1 0.2
+ fix m8 coefficientPlasticityDepth     peratomtypepair 1 0.05
- pair_style gran model hooke tangential history
+ pair_style gran model hooke/hysteresis tangential history
```
| 경로 | 파라미터 | 단위 | 우리가 쓰는가 |
|---|---|---|---|
| `cohesion sjkr` (pair_style 에 추가) | `cohesionEnergyDensity` | **J/m³** | ✗ |
| `hooke/hysteresis` 의 `k_c` | `coefficientAdhesionStiffness` | **k_N 대비 비율**(튜토리얼 주석) | ✅ |
| JKR (믹싱 문헌) | 표면에너지 `Γ` | **J/m²** | ✗ |

⇒ ⛔ **§2-3 의 한정어는 풀린 것이 아니라 더 굳었다** — 서로 다른 파라미터화가 **셋**이고
단위가 전부 다르다.  `m7` 균일화는 여전히 [25] *"표면에너지 동일"* 의 **대리**다.
⇒ **`k_c ↔ Γ` 환산식은 튜토리얼에 없다.**  (추정하지 않는다.)

### ② ⛔ 그리고 우리 `m7` 값이 튜토리얼과 **5~6 자릿수** 어긋난다 → 원장 `SELF-41`
```
                     튜토리얼    우리 (AM-AM / AM-SE / SE-SE)
m6                     2.0       1.5 / 3.0 / 5.0        <- 같은 자릿수
m8                     0.05      0.05 / 0.01 / 0.005    <- 같은 자릿수
m7  AdhesionStiffness  0.2       1.0e5 / 2.0e5 / 1.0e6  <- ⛔
```
형제 파라미터 셋이 같은 `#ratio` 주석 아래 나란히 선언되는데 **`m7` 만** 어긋난다.
⚠ **아직 결함이라고 부르지 않는다** — 근거가 튜토리얼 주석 한 줄뿐이고, 우리 침대는
정상으로 압밀되며 porosity 가 실험과 맞는다.  `SELF-41` 의 ①②③ 참조.

### ③ 신/구 모델 규약이 확인됐다 (`contactModels` diff)
구: `pair_style gran/hertz/history 266000.0 NULL 500.0 …` (물성이 **pair_style 줄에**)
신: `pair_style gran model hertz tangential history` + `fix … property/global …`
⇒ **물성이 `pair_style` 줄을 떠났다**는 것이 공식 예제로 확인됐다 = `SELF-40` 의 기전 확정.

### ④ 믹서 공정 단계의 정확한 형태 (`Mixer/input.liggghts`)
```
fix Drum  all mesh/surface file Drum.stl type 2
fix MoveDrum all move/mesh mesh Drum rotate origin 0 0 0 axis 1. 0. 0. period ${drumPeriod}
fix ins all insert/stream … insertion_face ins_mesh extrude_length 0.1
fix m4 coefficientFriction peratomtypepair ${natoms} ${sf11} ${sf12} ${sf21} ${sf22}
```
⇒ **`move/mesh … rotate` 세 줄이면 드럼 회전이 붙는다.**  그리고 **2종 상쌍 행렬**
(`sf11 sf12 sf21 sf22`)을 쓰는 공식 예가 있다.
⛔ **이 사전등록의 런에는 넣지 않는다** — §2-1 대로 이 런은 *"점착 있는 침전·압밀"* 을
재는 것이고, 믹서를 붙이면 **다른 실험**이 된다.  별건으로 등록한다.

## §9. 추가 팔 **D** — `SELF-41` 을 같은 런으로 답한다

`m7` 이 힘에 **실제로 기여하는가**를 1 런으로 가른다.

| 팔 | `m7` | 무엇을 가르나 |
|---|---|---|
| **D 점착 제거** | `0 / 0 / 0` | `m7` 이 접촉력에 기여하는가 |

- **판정**: `D` 의 침대가 `B`(균일-저 1.0e5)와 **입자 좌표까지 동일**하면 `m7` 은 **안 탄다**
  (그 경로가 죽어 있다).  다르면 **탄다** — 그러면 `SELF-41` 의 자릿수 문제가 실물 영향을
  갖는다는 뜻이고, 그때 소스를 읽어 비율/절대값을 확정한다.
- ⚠ **이 팔은 §5 의 판정선을 쓰지 않는다** — 응집 지표가 아니라 **동일성 검사**다.
  비교는 최종 프레임의 좌표 해시로 한다 (같은 시드·같은 인자).
- 비용 = **1 런** (시드 1).  §7 의 9 런에 더해 **총 10 런**.

## §10. 미등록 후속 (여기서 돌리지 않는다)

⬜ **믹서 단계 신설** — `move/mesh … rotate` + `insert/stream`.  별도 사전등록 필요.
⬜ **`cohesion sjkr` 팔** — 우리 `hooke/hysteresis` 를 `hertz + cohesion sjkr` 로 바꾸면
   문헌(`cohesionEnergyDensity`, J/m³)과 **같은 파라미터화**가 된다.  ⚠ 그러나 그것은
   접촉 법칙 자체를 갈아끼우는 것이라 **18× E 연화 보정이 같이 무너진다** — 별건이다.
⬜ **YADE 경로** — 사용자 목표는 *"LIGGGHTS 나 YADE 로 완성"* 이다.  YADE 는 점착·마찰
   접촉(Luding 계열 포함)을 기본 제공하므로 `Γ` 파라미터화에 더 가까울 수 있다.
   ⚠ 확인 안 했다 — 확인 전에는 그렇게 적지 않는다.
