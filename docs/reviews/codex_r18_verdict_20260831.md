# Codex R18 판정 — **HOLD.  A·B 둘 다 등록 불가** (2026-08-31)

요청: `codex_review_request_r18_20260831.md` · 검토 기준 `manuscript-track @ c79728cb`

| | 처분 |
|---|---|
| **제안 A** (부분부피 가중) | **DROP** — 현 설명은 REFUTED |
| **제안 B** (브릿지 역이용) | **DROP** — REFUTED |
| **A+B 공동 등록** | **DROP** — 분해 불가 |
| **Q6** 보존형 cut-cell face 연산자 | 후속 연구로 이관 |
| **Q7** 아무것도 안 함 | **CONFIRMED — 현재 최선** |
| D13 `UNREACHABLE` | **그대로 유지** |

기존 판정을 뒤집는 P1 은 없다.  제안을 막는 **신규 P1 이 3건**이고, 아래는 전부
**원자료·소스에서 내가 다시 확인한 것**이다 (Codex 의 자기 신고를 그대로 옮기지 않았다).

---

## P1-1 ★ A 는 부분부피가 아니라 **없던 계면층을 새로 얹는 것**이다

내 논거는 *"껍질 계단은 PTFE 가 셀을 부분적으로만 채우는 것을 0/1 로 반올림해서 생긴다"*
였다.  **틀렸다 — PTFE 부피에는 반올림 손실이 없다.**

`pellet_rve_sigma.build_rve` 는 **스탬프된 부피분율 자체를 표적으로** RSA 를 돈다
(`while (sid == bsid).sum() / n_cells < vol_target`, `scripts/pellet_rve_sigma.py:76`).
실측 (`docs/data/pellet_calib_20260825/ptfe_ion_blk0.12.json`):

```
vol_target  = 0.09174311926605504
vol_stamped = 0.091792              →  +0.053 %
```

⇒ PTFE 부피는 **이미 0.05 % 안으로 재현돼 있다.**  복원할 "빠진 부분부피" 가 없다.
계단이 있는 곳은 PTFE 가 아니라 **차단 껍질** 이고, 그 껍질은 물리적 부피가 아니라
우리가 **새로 얹는 확산형 저전도 계면층**이다.

**따르는 제약** (이름과 해석을 바꿔야 한다):
- `partial-volume PTFE` 가 아니라 **`effective interphase attenuation`**
- **`b` 를 피브릴 직경·두께로 해석 금지**
- 계면 폭과 함수형 `w(d)` 를 **결과 전에** 독립적으로 고정
- EDT 가 이미 복셀화된 `sid == 7` 에서 출발하므로(`step3_sigma.py:566`),
  **평활화만으로 격자 무관성이 생긴다는 주장 금지** — 내 R18 §1 의 "부수 이득" 은 성립 안 한다

## P1-2 ★ B 의 **전역 순위 f** 는 PTFE 양·거리에 단조 대응하지 않는다

내가 제안한 규칙은 *"모든 접촉을 최근접 PTFE 거리로 정렬해 가까운 쪽 f 비율을 스킵"* —
**전역 규칙에 고정 개수**다.  그래서 표현하려던 의미론을 **원리적으로 못 담는다**:

- PTFE 가 절반이든 두 배든 **같은 fN 개**를 삭제한다 ⇒ dose 의존이 없다
- 모든 PTFE 가 멀리 있어도 fN 개를 삭제한다 ⇒ no-op 이 안 된다
- PTFE 를 **더하면** 순위가 바뀌어 이전에 삭제됐던 간선이 **복구**될 수 있다 (비단조)
- 이미 face-connected 인 접촉은 repair 를 생략해도 **효과 0**

⇒ `f` 는 *"PTFE 가 막은 접점 비율"* 이 아니라 **수치 repair 생략률**이다.
핵심 의미론(*"PTFE 가 많을수록 접점이 더 끊긴다"*)이 무너진다.

## P1-3 ★ B 는 현재 구조에서 **전자 전용이 아니다**

내 R18 §3 은 *"SE 가 점구름이라 SE–SE 접촉 객체가 없으므로 전자 전용"* 이라고 적었다.
**근거는 맞지만 결론이 틀렸다** — 경로가 다르다.

`rasterize` 는 SE(sid 6)를 **가장 먼저, 가장 낮은 우선순위로** 찍고
(`step3_sigma.py:293`), AM–AM 브릿지는 `_ball` 로 **무조건 덮어쓴다**
(`sub[m] = s`, `step3_sigma.py:303-314` · 호출 `:345`).
(빈 셀에만 쓰는 `_ball_empty` 는 SDCP 브릿지 전용이다, `:507`.)

⇒ 브릿지를 **빼면 그 셀이 SE 로 되돌아간다.**  전자·이온이 **같은 sid 격자**를 공유하므로
(`electronic_sigma_table` / `ionic_sigma_table`), 그 셀은 이온망에 **더해진다**.
B 는 이온축을 같이 움직인다 ⇒ A/B 직교성이 성립하지 않고 공동 등록도 불가.

---

## Q2 — 산술은 맞고, **식별성 주장은 REFUTED**

독립 재계산으로 일치:

```
ln(1.517515 / 0.716959) = 0.749811
secant slope            = 14.996 µm⁻¹
log-선형 보간 b*        = 0.14984 µm
±5 %  →  Δb = 0.00325 µm  =  b* 의 2.2 %
```

그러나 결론은 안 선다:
- 현 이진 껍질에서 **국소 미분은 plateau 에서 0, 전환점에서 불연속**이다.
  위 값은 불연속 하나를 가로지른 **secant** 일 뿐 새 연산자 A 의 국소 기울기가 아니다.
  `w(d)` 의 함수형·전이 폭을 바꾸면 그 기울기도 **임의로 바뀐다**.
- ★★ **`±5 %` 는 측정오차나 likelihood 가 아니라 허용창이다.**  그것을 `b` 의 불확실성으로
  환산할 수 없다.  내가 **허용창을 신뢰구간처럼 다뤘다** — 범주 오류다.
- 식별성을 주장하려면: 함수형 봉인 → 독립 오차모형 → nuisance profile →
  synthetic recovery → **미사용 조건 holdout**.

## Q3 — 문헌 밴드로는 반증이 안 된다

`b` 는 **이미 스탬프된 PTFE 바깥의 유효 계면 거리**이지 피브릴 직경이 아니고,
`f` 는 **AM–AM repair 생략률**이지 표면 피복률이 아니다 ⇒ 대응 자체가 성립 안 한다.

문헌 값이 없는 것은 아니나(다른 공정에서 개별 섬유 ~48 nm · rope ~248 nm 등, 계열마다
수십 nm ~ µm) **밴드가 너무 넓어 거의 무엇이든 통과시킨다** = 반증력 0.
유효한 독립 측정은 **같은 조성·혼련·가공**에서 다음을 직접 재는 것뿐이다:
FV face 의 PTFE 차단 **면적분율**(→ A) · AM–AM contact patch 와 PTFE 의 **교차 비율**(→ B),
fibre/rope 구분 · z 층 · 이미지 선택 · segmentation 을 **사전등록**.

## Q4 — 위치 scramble 은 단독 대조로 부족

점 단위 scramble 은 피브릴 길이·연결성·z 분포·경계·AM 주변 배치를 **동시에** 바꾼다 ⇒
"PTFE 근접성" 만 시험하지 않는다.  B 를 **국소 연산자로 재정의한 뒤** 다섯을 함께:
① AM pair·gap·z·contact radius·격자 origin 별 층 **안에서 distance label 만 permutation**
② 같은 삭제 수의 **무작위 간선 제거**와 비교
③ 점이 아니라 **피브릴 전체의 rigid translation/rotation**
④ no-PTFE · 전부 원거리에서 **정확한 no-op**
⑤ 같은 AM graph 에 **PTFE dose 를 중첩 추가**하며 차단 집합·저항의 **단조성** 검사

## Q5 — 공동 등록 불가

D13 펠릿에는 **AM 이 없어 B 를 식별하지 못하고**, 전극에서는 P1-3 때문에 B 가 이온축도 바꾼다.
같은 결과에 A·B 를 함께 맞추면 **분해 불가능**하다.
가능한 형태는 **파라미터를 각각 독립으로 먼저 고정**한 뒤 경쟁 모델로 등록하는 것뿐:
`M0`(현 기준) · `MA` · `MB`(재설계판) · `MAB`(재적합 없음) → **미사용 holdout 에서 비교**.
A 를 이온 전용으로 구현하려면 shared sid 를 건드리지 말고 **별도 voxel/face conductivity
field** 를 쓸 것 — 솔버에 `sigma_field` 경로가 이미 있다 (`step3_sigma.py:1119`).

## Q6 — 권고: **보존형 cut-cell / capsule face 연산자**

원본 피브릴 **중심선 + 직경**에서 각 FV face 의 **열린 면적분율 α** 를 계산해
`G_face = α · G0` 로 둔다 (불투과 PTFE 가정).  독립 측정된 계면저항이 있을 때만
`R_int` 를 직렬/Robin 항으로 더한다.

국소적이고 · 방향성을 보존하고 · KCL 에 맞고 · **복셀 원점을 바꿔 수렴성을 직접 시험**할 수 있다.
코드에 `capsule` 예약 경로가 이미 있다 (`mpm_webapp_payload.py:596`).
최소 종료조건: α=1/0 극한 · reciprocal flux · KCL · 회전/반사 · periodic seam ·
**고정 물리기하에서의 voxel refinement** · origin invariance · dose monotonicity.
⚠ 직경이나 `R_int` 를 다시 0.97 에 맞추면 그것도 **calibration 이지 validation 이 아니다.**

⚠ 내가 R18 §1 에서 *"capsule 은 답이 아니다 — 참 직경으로 찍는 것도 부피 표현"* 이라 적은 것은
**셀 스탬프** 얘기였다.  Q6 은 셀을 찍는 것이 아니라 **face 개구율**을 계산하는 것이라
피브릴이 복셀보다 얇아도 성립한다 — 다른 물건이다.

## Q7 — **CONFIRMED.  지금은 아무것도 더하지 않는 것이 최선**

`0.716959 – 1.517515` 는 **물리적 신뢰구간도, 참값의 상·하한도 아니다.**
현 이진 연산자의 **인접한 두 표현 상태**가 만든 **결정론적 해상도/모델형식 브래킷**이다.

원고에 쓸 수 있는 최대 문장 (이 이상 주장하지 않는다):

> Within the preregistered 0.12-µm voxel binary EDT-shell representation, the PTFE-pellet
> target (0.97 mS cm⁻¹) fell between the two adjacent representable shell states
> (1.518 and 0.717 mS cm⁻¹, normalized to σ_SE = 3.57 mS cm⁻¹).  We therefore selected no
> blocking thickness and did not treat the PTFE correction as calibrated.  This deterministic
> bracket reflects operator resolution and model form; it is neither a confidence interval nor
> a bound on physical fibril size or conductivity.

---

## 처분

**A DROP · B DROP · A+B DROP · Q6 후속 · Q7 유지.**
A/B 를 적용한 8팔 생산 런은 **시작하지 않는다**.  진행 중인 이온 8팔(4시나리오 × 8 origin)은
이 판정과 무관한 별개 사전등록이므로 그대로 완주한다.
