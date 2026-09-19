# 점착 대조쌍 — 튜토리얼 `cohesion` 기반 (2026-09-19)

`docs/reviews/mixing_model_design_20260919.md` §6 의 주지표를 검증한 런.

## 출처와 수정

원본 = 1저자가 준 `Tutorials_public/cohesion/in.noCohesion` (LIGGGHTS-PUBLIC 동봉).
**물리 줄은 한 글자도 안 바꿨다.** 바꾼 것은 둘뿐:

1. **덤프 형식** — `dump custom/vtk` → `dump custom` (평문).
   이유: 직렬 빌드(`make serial`)에 VTK 가 없다. 그리고 평문은 우리 `parse_liggghts.py`
   가 그대로 읽는다.
2. **런 길이** — `run 50000 upto` → `run 250000 upto`.
   ⚠ 이유가 중요하다: 50,000 step = **0.5 초**인데 낙하 60 mm · 반발계수 0.9 에서
   정착에 **약 2.1 초**가 걸린다 = **정착의 24 %**. 그 시점에 재면 침대가 아니라
   **튀는 구름**이라 지표가 **부호까지 반대로** 나온다. 250,000 step = 정착 119 %.

`in.cohesion` 은 `in.noCohesion` 에서 **튜토리얼 diff 그대로 두 줄만** 다르다:
```
+ fix  m6 all property/global cohesionEnergyDensity peratomtypepair 1 300000
- pair_style gran model hertz tangential history
+ pair_style gran model hertz tangential history cohesion sjkr
```

## 돌리는 법

```bash
lmp_serial -in in.noCohesion      # 대조
lmp_serial -in in.cohesion        # 점착
python3 scripts/measure_bed_aspect.py     # 두 최종 프레임을 잰다
```
⚠ 최종 프레임은 **숫자순**으로 고른다. `ls | tail` 은 사전순이라
`_9600` 이 `_249600` 뒤에 온다 (측정 스크립트는 숫자로 정렬한다).

## 결과 (1,000 입자 · step 249,600)

| | noCohesion | cohesion | 비 |
|---|---|---|---|
| R(99 %) | 48.50 mm (벽 50 의 0.970) | 43.46 mm | ×0.90 |
| **H** | **2.60 mm** | **13.01 mm** | **×5.01** |
| **H/R** | **0.054** | **0.299** | **×5.59** |
| φ(포락) | 0.737 | 0.183 | ×0.25 |

⇒ 주지표 `H/R` 은 **5.6배** 차이를 낸다. 문턱 조정이 필요 없다.
