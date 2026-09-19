# `hooke/hysteresis` + `cohesion sjkr` 결합 탐침 (2026-09-19)

**질문**: 생산 압축 덱의 접촉모델(`hooke/hysteresis` + m6/m7/m8)에 튜토리얼의
SJKR 점착을 **얹을 수 있는가?** 추측하지 않고 돌려서 확인했다.

**답: 된다.** 400 입자 · 3종 · 생산 물성 그대로 10,000 step 완주 (`rc=0`).

```
pair_style gran model hooke/hysteresis tangential history cohesion sjkr rolling_friction cdt
soft_particles yes
fix mC all property/global cohesionEnergyDensity peratomtypepair 3 …3×3…
```

## 두 가지 제약을 실측으로 확인했다

1. **키워드 순서** — `cohesion` 은 `tangential history` **뒤**, `rolling_friction` **앞**.
   - `… rolling_friction cdt cohesion sjkr` → `ERROR: Unknown argument or wrong keyword order: 'cohesion'`
   - `model … cohesion sjkr tangential …` → `ERROR: … 'tangential'`
2. **`soft_particles yes` 필수** — SE 의 `youngsModulus = 0.135e7 = 1.35e6` 이
   `ERROR: youngsModulus >= 5e6 required for SI units` 문턱 아래다.
   생산 덱도 33행에서 이미 `soft_particles yes` 를 쓴다.

## 왜 중요한가

`m7`(강성비)을 **생산값 그대로 고정**하고 `cohesionEnergyDensity`(J/m³)만 스윕할 수 있다.
⇒ `k_c ↔ γ` **환산이 필요 없어진다**. 그리고 압축 작업과 접촉역학이 같아 연속성이 선다.
