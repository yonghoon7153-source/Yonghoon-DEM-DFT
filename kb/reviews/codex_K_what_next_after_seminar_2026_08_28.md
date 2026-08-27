---
title: "교차리뷰 K — 세미나 이후 무엇을 할 것인가 (데이터·모델은 늘었는데 축이 비어 있다)"
date: 2026-08-28
updated: 2026-08-28
tags: [review/codex, cascade, mlip, litdb, ml, surrogate, prioritization]
status: 리뷰대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

> 아래 전문을 그대로 Codex 에 붙인다.
> **묻는 것: 다음 한 달을 어디에 쓸 것인가.** 후보를 다 늘어놓았고 우리 우선순위도 붙였다.
> 리뷰 J(li3nd 선행검사)와 **독립**이다 — 저건 GPU, 이건 방향이다.

---

# 무엇을 할 것인가 — 우리 직관과 숫자가 반대로 간다

## 0. 이 리뷰를 요청하는 이유

1저자의 감각: *"데이터도 많고 모델도 발전했고 ML 등 할 수 있는 게 엄청 많은데."*
**숫자를 재보니 반대였다.** 그 간극을 판정해 달라.

---

## 1. 실측 — cascade 설계행렬은 **거의 비어 있다**

`db/properties/cascade_v23_all.csv` · **3,615행 × 105열** 전수 (2026-08-28):

| 축 | 채워진 행 | 비율 |
|---|---:|---:|
| `screen_de_per_atom` (안정성) | **3615** | 100 % |
| `bvs_li_proxy_score` | 681 | 18.8 % |
| `li_mobility_score` | 681 | 18.8 % |
| `migration_volume_fraction` | 681 | 18.8 % |
| `elastic_E_young_GPa` | 681 | 18.8 % |
| `elastic_pugh_GoverB` | 681 | 18.8 % |
| `eos_B0_GPa` | 622 | 17.2 % |
| `sigma_300K_S_cm_NE` | **0** | 0 % |
| `sigma_md_Ea_eV` | **0** | 0 % |
| `wad_J_m2_mean` | **0** | 0 % |
| `air_hsab` | **열 자체가 없음** | — |
| `concentration` | 3615 | 100 % — **전부 `0.25`** |

⇒ **실제로 3,615행 전부를 채점할 수 있는 축은 안정성 하나**다. 나머지는 18.8 % 아니면 0 %.
`combined_score = 0.4×안정성 + 0.3×탄성 + 0.3×이동도` 인데, 2,934행에서 뒤 두 항이 결측이다.
(결측 정규화가 0.5 상수로 메워지던 버그는 2026-08-25 에 고쳤다 — 그건 별개다.)

**그리고 설계공간의 유일한 연속축이 상수다.** `concentration` 이 3,615행 전부 `0.25`.

## 2. 실측 — 대리모델은 **이미 정직한 CV 에서 졌다**

`db/properties/cascade_audit_ml_validation.csv`:

```
generalization, pair LOOCV weighted R2,      0.0892   (dopant leakage)
generalization, LODO  weighted R2,          -0.1805   (worse than mean)
generalization, L2DO  weighted R2,          -0.2548   (worse than mean)
acquisition,    global discovery enrichment,  1.22    p=0.426  (not significant)
acquisition,    ordering enrichment (top40),  3.35    p=0.0099 (retrospective)
```

**도펀트를 통째로 빼면(LODO) 평균보다 못하다.** 전역 발굴 이득도 유의하지 않다.

우리 해석(2026-08-25 카드): *"−0.18 은 우리 ML 이 나쁘다가 아니라 **우리 CV 가 정직하다**"*.
비교 대상이던 미세구조 ML 세미나의 `R²=0.99` 는 ① 랜덤 폴드(group-CV 아님) ② 노이즈 0 인
결정론적 FEM 라벨에서 나온 값이라 **범주가 다르다.**

⇒ **"데이터가 많으니 ML 을 더" 는 이 숫자 위에서는 성립하지 않아 보인다.** 여기가 첫 질문이다.

## 3. 실측 — **궤적은 진짜로 많다**

`db/properties/md_run_ledger.json` (19 런 · 8 위치):

| 호스트 | 계 | T [K] | 시드 | 궤적 |
|---|---|---|---|---|
| kgy `highT_reseed_traj` | b2o3 | 800/1000/1200 | s2·s3·s4 | ✓ 9/9 |
| kgy `highT_reseed_1200` | b2o3 | 1200 | s2·s3·s4 | ✓ 3/3 (독립 반복) |
| kgy `arrhenius_6pt_traj` | modelc·lpsocl·b2o3 | 700/900 | — | ✓ 진행 |
| kgy `lpsocl_600_long` | modelc | 500/700/900 | — | ✓ 3 |
| gabia `highT_reseed_traj` | modelc | 600/800/1000 | s2·s3·s4 | ✓ 7(+1) |
| gabia `b2o3_600_reseed` | b2o3 | 600 | — | ✓ 3 |
| kgy·gabia (진행) | lpsocl 3셀 | 600 | 1 | **800 ps** 8/29 완주 |

**b2o3 와 modelc 는 600/800/1000 K × 3시드 대조가 이미 있다.** 궤적은 `traj.xyz`, save 100 fs.

## 4. 실측 — litdb 처방이 **코드가 안 됐다**

논문 **195편** + 발표 **8건**. `kb/open_items.md` T-표에 *"기존 궤적 재사용, 새 시뮬레이션 0회"*
계열이 셋 열려 있다:

| | 무엇 | 출처 | 상태 |
|---|---|---|---|
| **T12** | van Hove `G_s(r,t)` — cage 갇힘 vs 자유확산 | Lee 2024 Fig 3e | 🟢 **도구가 이미 있었다** — `tools/ionic/aimd_jump_stats.py` 가 계산한다. **한 번도 안 돌렸을 뿐.** T-표의 "MSD 파이프라인 추가" 는 낡은 기록 |
| **T14** | Li–(S,Cl)₄ CSM(연속대칭척도) 후처리 | Kim 2025 CSP | 미구현 |
| **T16** | 다원자 음이온 회전 자기상관 | Shin 2026 BH₄ | 미구현 (08-26 신설) |
| **T13** | MSD 생산길이 200 ps 타당성 | Lee 2024 (10 ns) | **지금 답해지는 중** — 800 ps 3런 |

T12 는 오늘 selftest 를 붙였다(8/8, 합성 궤적으로 판별력 600배 확인: 홉 봉우리 0.633 vs
흔들림 0.001). **돌리는 것만 남았다.**

## 5. 우리 잠정 우선순위 (반박해 달라)

### 🥇 T12 van Hove — 궤적 25개+ 에 지금 돌린다

**왜 1순위인가**: 우리가 한 달을 쓴 질문이 *"이게 확산 구간이 맞나"* 였고,
β 문턱 → `D_inc` → 창 스캔 → 200 ps 판정불가까지 **전부 MSD 기울기 하나로** 가르려 했다.
`D_inc` 로 옮겼지만 그것도 여전히 MSD 파생이다.
van Hove 는 **창을 안 고르고** 분포 모양으로 답한다 — **독립 관측**이고, 그게 지금 없는 것이다.

비용 0(CPU) · 멀티시드 대조 가능 · 도구·테스트 완비.

### 🥈 T16 회전 자기상관 — **문헌 공백에 우리 계가 정확히 맞는다**

카드가 스스로 한계를 적어뒀다: 우리 host 엔 BH₄ 가 없고, 잴 수 있는 PS₄ 는 그 논문이
*"안 돈다"* 고 판정한 대상이라 **"PS₄ 느리다" 는 재확인이지 신규가 아니다.**
**신규가 되는 길**도 적어뒀다 — *Cl 함량(comp1→modelc) 의존성* 또는 *우리 도펀트(B₂O₃·O 치환)가
PS₄ 회전을 바꾸는지*. **우리는 정확히 그 4조성 궤적을 갖고 있다.**

### 🥉 cascade — **막힌 게 아니라 안 한 것** (셋 다 새 계산 0)

- **A3 Pareto 비지배집합** — `analyze_screening.py --objective pareto`. 미착수.
- **결측 구조를 정면으로 보고** — 681/3615 위에서 3,615개를 순위 매기는 것이 정당한가.
- **`air_hsab` 정성 tier → 정량 축** 승급 (open_items #11-3). 열 자체가 없다.

### 비용 > 0

- **`concentration` 축 해동** — 유일한 연속축이 상수다. 새 계산 필요.
- **T2** ICOHP 기반 P–S 약화 기술자.

## 6. 묻는 것

- **K1.** §1·§2 를 놓고 볼 때, **"ML 을 더" 가 지금 틀린 방향인가?**
  우리 읽기는 *"설계행렬이 18.8 % 밖에 안 찼고 LODO 가 음수인데 모델을 더 얹는 것은
  잡음을 학습하는 것"* 이다. 그렇다면 옳은 다음 수는 **모델이 아니라 축을 채우는 것**인가,
  아니면 **채울 축을 ML 로 고르는 것**(active learning)인가?
- **K2.** 681/3615 위에서 3,615개를 순위 매겨 발표·원고에 쓰는 것이 **정당한가.**
  정당하지 않다면, 지금 발표 가능한 단위는 무엇인가 — 681 부분집합인가, 안정성 단일축인가?
- **K3.** T12(van Hove)가 실제로 β/`D_inc` 논쟁에 **독립 증거**가 되나,
  아니면 같은 궤적에서 나온 다른 요약이라 **독립이 아닌가?**
  (우리는 독립이라고 보는데, 같은 데이터라는 점이 걸린다.)
- **K4.** T16 의 "신규가 되는 길"(도펀트가 PS₄ 회전을 바꾸는지)이 **실제로 문헌 공백인가**,
  아니면 우리가 못 찾은 것인가? 그리고 그게 **우리 Li Ea 와 같은 단위로 비교 가능한가?**
- **K5.** `concentration` 이 3,615행 전부 0.25 인 것 — 이걸 **한계로 적고 진행**할 것인가,
  아니면 **해동이 선행조건**인가? (해동은 새 계산이 크다.)
- **K6.** 순서. 우리는 T12 → T16 → cascade(A3·결측 정면화) 로 본다. 다르게 보나?

## 7. 우리가 스스로 의심하는 것

1. **T12 를 1순위로 둔 이유가 "값어치" 가 아니라 "지금 당장 돌릴 수 있어서" 일 수 있다.**
   오늘 하루 도구 버그만 다섯 개 고쳤고(min-image · greedy 대응 · 절대 바닥 · 반전 중심 ·
   수집기 fail-open) 새 계산은 하나도 안 늘었다. **뭐라도 돌리고 싶은 상태**다.
2. **§2 를 "ML 하지 말자" 로 읽는 것이 과잉일 수 있다.** LODO 음수는 *지금 특징·지금 라벨*에서의
   결과지 원리적 한계가 아니다.
3. **cascade 를 "안 한 것" 으로 부르는 것**도 자기변호일 수 있다 — 못 하는 이유가 있었을 수 있다.

## 8. 참고 파일

- `db/properties/cascade_v23_all.csv` · `cascade_audit_ml_validation.csv`
- `db/properties/md_run_ledger.json` — 궤적 전수
- `kb/methodology/microstructure_ml_transfer_to_cascade_2026_08_25.md` — §4 가 CV 논거
- `kb/methodology/cascade_rerank_runbook_2026_08_25.md` — ①~⑤ 재랭킹 결과
- `kb/open_items.md` T-표 — T12·T13·T14·T16
- `tools/ionic/aimd_jump_stats.py` — van Hove (`--selftest` 8/8)
