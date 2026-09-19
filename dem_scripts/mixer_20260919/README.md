# 믹싱 드럼 파일럿 — 표면에너지 스윕 (2026-09-19)

⚠ **`in.mixer` 를 손으로 고치지 말 것.** 치수가 조성에서 **유도**된다.
```bash
python3 scripts/make_mixer_deck.py --out dem_scripts/mixer_20260919 \
        --n-total 50000 --cgf 200 --rpm 60 --revolutions 5
```

## 규격 (1저자 비준 D8–D12, 2026-09-19)

| | |
|---|---|
| 조성 | `AM:SE:VGCF:PTFE = 80:18:1:1 (wt%)` · `P:S = 7:3` |
| CGF | **200** (실제 AM_P 12 µm → 사물 2.40 mm) — `lischka` 와 같은 값 |
| 입자 | AM_P 2.40 · AM_S 0.80 · SE 0.60 · 섬유구 0.60 mm |
| 섬유 | multisphere 강체 사슬 **3구**, 길이 2.0 mm (`L/D = 3.3`) |
| 개수 | AM_P 742 · AM_S 8,586 · SE 36,635 · VGCF 2,115(705가닥) · PTFE 1,923(641가닥) |
| 드럼 | **Ø76 × 15 mm** (STL scale 0.0757) · 68 mL · 임계 **154 rpm** |
| 운전 | 60 rpm (`Fr 0.152`, cataracting) |
| dt | 4.68e-6 s (Rayleigh 20 %) |
| 비용 | 5바퀴 = 1,067,656 step · **직렬 약 1.5 h** (실측 1.04e7 p·step/s) |

## 실행으로 확인한 것 (추측 아님)

| | |
|---|---|
| 조성 재현 | 실제 침대 `56.00 / 24.00 / 18.00 / 0.999 / 1.002 wt%` — **오차 0.2 % 이내** |
| 섬유 강체 | `mol` 그룹 1,346개 · 전부 3구 |
| 처리율 | **1.04e7 particle-step/s** (직렬, 53k 원자) |

## ⚠ 실행이 가르쳐 준 제약 셋 — 전부 시험에 박았다

1. **`particledistribution/discrete` 의 분율은 `mass%` 다.**
   초판에 개수분율을 넣어 AM_P 가 744 → **6개**로 들어갔다.
   우리 조성이 이미 wt% 라 **그대로 넣으면 된다**.
2. **multisphere 의 `type` 은 원자 타입이 아니라 템플릿 번호**이고 **1부터 연속**이어야 한다.
   (`ERROR: multisphere template types have to be consecutive starting from 1`)
3. **`cohesion` 키워드는 `tangential history` 뒤 · `rolling_friction` 앞.**
   순서를 바꾸면 `ERROR: Unknown argument or wrong keyword order`.

★ 그리고 **섬유 질량에 겹침 보정이 필요하다** — 구 3개 합이 아니라 **0.9627배**다
(등반경 렌즈 해석값). 보정 전에는 섬유가 **+3.8 %** 더 들어갔다.

## ⛔ 생산 압축 덱의 `scale=1000` 규약을 쓰지 않는다

그 규약은 `E_sim = E_real/scale · R_sim = R_real×scale` 이라 **접촉력은 `scale¹`,
중력은 `scale³`** 로 스케일된다 ⇒ 중력/접촉 비가 `scale²` 만큼 틀어진다.
압축 덱은 **플래튼 구동**이라 무해했지만 **드럼은 중력 구동**이다.
⇒ 문헌 방식(CGF + 중력 실제값)으로 간다.

⚠ 영률을 `1e7` 로 낮췄다 — `lischka` 가 *"계산비용 때문이지 물성이 아니다"* 라고 명시한
것과 같은 조작이고 튜토리얼 `Mixer` 도 같은 값이다. **탄성 물성으로 인용 금지.**

## ⬜ 아직 안 한 것

- **팔 스윕** — 지금 덱은 `cohesionEnergyDensity` 가 3.0e5 균일(E1 한 팔)이다.
  E0(0) · E2(AM만 10배) · E3(SE만 10배) · E4(AM 100배) 는 그 블록만 바꿔 만든다.
- **`D11` CED 스케일링** — CG 하면 점착을 어떻게 다시 주나. 두 입경에서
  `H/R` 이 같아지는 `CED` 를 찾아 지수를 **실측**해야 한다.
- 정착 확인 — 회전 시작 전 KE 가 떨어졌는지 (`measure_bed_aspect.py` 의 φ 경고).
