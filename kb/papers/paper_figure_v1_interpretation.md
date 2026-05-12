# 왜 어떤 SE 는 NCM 에 잘 붙고, 어떤 건 잘 안 붙는가
## — Halogen-치환 Argyrodite 의 계면 메커니즘

> 이 문서는 paper #1 의 두 핵심 figure (binding curves + bond densities) 가 **왜 그런 모양으로 나오는지** 그 메커니즘만 풀어 쓴 글입니다. 측정 방법, code, 숫자 처리는 다루지 않습니다.

---

## 한 줄 요약

**Li 자리가 비어 있을수록 (Li5.4 > Li6), 그리고 작은 음이온 (Cl⁻) 이 표면에 덜 노출될수록, SE 와 NCM 이 잘 붙는다.**

실험 접착력 순위:
```
comp3 (316) > comp4 (298) > comp5 (249)  >  comp1 (194) > comp2 (180)   [단위 mJ/m²]
└────────── Li5.4 family ──────────┘    └── Li6 family ──┘
```

같은 family 안에서는 Br 함량 차이로 추가 미세 trend 가 생긴다.

---

## 1. 왜 두 family 사이에 차이가 큰가 — "빈 자리 효과"

Argyrodite Li-아지로다이트 의 화학식은 ==Li₅₊ₓPS₅₋ₓX₁₊ₓ== 형태 (X = Cl/Br). 우리는 두 family 를 비교한다:

| Family  | f.u. 당 Li 개수 | 의미 |
|---------|----------------|------|
| **Li6** (comp1, comp2)        | 6   | Li 자리가 **꽉 차 있음** |
| **Li5.4** (comp3, comp4, comp5, modelC) | 5.4 | 6 개 자리 중 ==**0.6 개가 비어 있음**== (vacancy) |

### 비유

NCM 표면을 손님 (=O 이온) 이 와서 손 잡으려는 가게라고 생각해보면:

- **Li6 (가게가 만석)**:
  - 모든 자리에 Li 가 앉아있다. 각 Li 는 이미 옆의 S²⁻ 와 손을 잡고 있어 안정 (=**fully coordinated**).
  - 새로 온 NCM O 와 손 잡을 여유가 **없다** → 약하게만 결합.

- **Li5.4 (가게에 빈 자리)**:
  - 어떤 Li 들은 옆자리가 비어 있어서 손을 ==하나 덜 잡고 있다== (=**under-coordinated**).
  - "한 손 비어 있는" 상태이므로 NCM O 와 적극적으로 결합 → **강한 Li-O 결합** 형성.

### 결과
- Figure 2 의 ==**Li-O bond density**== 가 Li5.4 family 에서 훨씬 높음 (0.12-0.14 vs 0.08-0.11 Å⁻²).
- Li-O 결합이 SE 와 NCM 을 잡아당기는 **주된 attractive force** 이므로 → Li5.4 가 잘 붙음.
- Figure 1 의 binding curve 에서 Li5.4 곡선들 (red/purple/green) 이 Li6 곡선들 (blue/cyan) 보다 **더 깊은 well** 을 가짐.

---

## 2. Cl 과 Br 의 차이 — "작은 놈이 더 시끄럽다"

표면에 노출된 halogen 음이온은 NCM 의 O²⁻ 와 ==**음이온–음이온 repulsion**== 을 일으킨다 (둘 다 음전하). 그런데 Cl 과 Br 의 거동이 다르다:

| Halogen | 이온 반지름 | 표면 노출 시 영향 |
|---------|------------|-------------------|
| **Cl⁻** | 작음 (1.81 Å)  | NCM O 와 가까이 다가가서 **강한 repulsion** → adhesion 죽임 |
| **Br⁻** | 큼 (1.96 Å)    | 크기 때문에 가까이 못 가서 **약한 repulsion** → 영향 작음 |

### 직관적으로
- Cl 은 작아서 NCM O 와 어깨를 부딪힐 거리까지 다가갈 수 있다 → 강한 밀어내기.
- Br 은 부피 크니까 멀리 떨어진 위치에서 잠시 마주칠 뿐 → 밀어내기 약함.

### 결과
- Figure 2 에서 **Cl-O density** 가 paper Wad 와 **강한 음의 상관** (작아질수록 Wad 올라감).
- Br-O density 는 영향이 약함 (커도 Wad 별로 안 떨어짐).

==**핵심**: Cl 이 표면에 노출되는 것이 adhesion 의 최대 적이다.==

---

## 3. comp 별로 왜 그렇게 나오는가

### comp3 — LPSC₁.₀Br₀.₆ — 🏆 가장 강한 접착 (316 mJ/m²)
- Li5.4 family: vacancy 가 있어서 Li 가 NCM O 와 결합할 여유.
- Cl 이 많지만 (1.0) ==bulk 안쪽에 안전하게 자리잡음== → 표면 Cl-O 거의 없음.
- Br 이 적음 (0.6) → 표면 Br-O 도 낮음.
- 결과: ==Li-O 만 풍부, repulsion 거의 없음== → sweet spot.

### comp4 — LPSC₀.₈Br₀.₈ — 두번째 (298)
- Li5.4 vacancy 있음 → Li-O 충분.
- Cl 과 Br 이 비슷한 비율로 섞임. Cl 은 다행히 bulk 에 머무름.
- Br 일부 표면 노출 → 약간의 repulsion. 하지만 Br 크기 덕분에 큰 손해 없음.

### comp5 — LPSC₀.₆Br₁.₀ — 세번째 (249)
- Li5.4 vacancy 있음 → Li-O 좋음.
- Br 가 많음 → 표면에 Br 가 더 많이 노출됨 → comp4 보다 ==Br-O repulsion 좀 더 큼==.
- comp3, comp4 보다 약함.

### comp1 — Li₆PS₅Cl — Li6 의 베이스라인 (194)
- Li6 family: ==Li 자리 다 채워짐 → Li-O 결합 약함==.
- Cl 일부 표면 노출 → 약한 Cl-O repulsion.
- Li5.4 family 의 절반 수준.

### comp2 — Li₆PS₅Cl₀.₅Br₀.₅ — 가장 약함 (180)
- Li6 family: Li-O 결합 weak.
- Cl 절반이 Br 로 치환되면서 ==Li-O density 가 오히려 더 낮아짐== (0.076 vs comp1 의 0.115).
  - 이유: Br 이 들어오면서 표면 재구조가 일어나 Li-O 결합 약간 깨짐.
- Cl 일부도 여전히 표면에 → 약한 repulsion 도 있음.
- 모든 면에서 불리.

### modelC — LPSC₁.₆ (Br 없음, 참고용)
- Li5.4 family 인데도 ==Cl 이 많아서 표면에 노출== → Cl-O density 가 0.088 로 가장 높음.
- Vacancy 효과 (Li-O 강화) 가 Cl-O repulsion 으로 ==상쇄됨==.
- 실험값은 알려지지 않았지만 이론상 낮을 것.

---

## 4. 전체 그림 — 두 축의 경쟁

```
     강한 Li-O bonding (좋음)        강한 Cl-O repulsion (나쁨)
       ↑                                       ↑
       │                                       │
       │  ← Li5.4 vacancy 가 강화              │  ← Cl 작아서 강함
       │                                       │  ← Br 크기 때문에 약함
       │                                       │
                                               │
        Adhesion (Wad)  =  Li-O attractive  −  Cl-O repulsive  +  (작은 Br-O)
```

==**Wad 의 최종 값은 이 두 힘의 줄다리기로 결정된다.**==

- **comp3 (316)**: Li-O 최고 + Cl-O 0 + Br-O 작음 → 최강.
- **comp1 (194)**: Li-O 보통 + Cl-O 작음 + Br-O 0 → 보통.
- **comp2 (180)**: Li-O 가장 낮음 + Cl-O 약간 → 최약.

---

## 5. Binding curve 의 모양 (Figure 1) 도 같은 메커니즘으로 설명됨

- d = 1.2 ~ 1.6 Å 부근에서 well 이 가장 깊음 → 이 거리에서 ==Li-O 결합과 Cl/Br-O repulsion 의 균형이 잡힘==.
- 더 가깝게 (d < 1) 가면 모든 결합이 short-range repulsion (Pauli) 으로 튀어오름 → 위로 솟음.
- 멀어지면 (d > 3) 결합 깨지고 거의 0 으로 수렴 → 각 comp 의 baseline.
- Li5.4 곡선 들의 minimum 이 d ≈ 1.6 Å, Li6 들은 d ≈ 1.2 Å.
  - 이유: Li5.4 의 표면 Li 는 vacancy 때문에 살짝 들어가 있어 NCM 과의 최적 거리가 조금 멀음.

---

## 6. 그래서 paper 의 main message 가 뭔가

==**Halogen substitution 으로 mechanical 물성을 의도적으로 tuning 할 수 있다.**==

1. **Vacancy 가 핵심**: Li₅.₄ 처럼 Li 자리를 일부 비워두면 표면에서 NCM 과의 chemical bonding 이 강해진다.
2. **Cl 은 위험, Br 은 안전**: Cl-O 같이 작은 음이온끼리의 마찰이 adhesion 을 깎는다. Br 은 비슷한 역할이지만 크기 덕에 덜 깎는다.
3. **Cl-rich / Br-light 가 최적**: comp3 (Cl 1.0 / Br 0.6) 처럼 Cl 이 많지만 표면에 안 나오고 Br 이 적은 조성이 sweet spot.

이 미시적 (Li-O / Cl-O / Br-O 결합 개수) 그림이 거시적 ==**peel test 실험 결과를 그대로 재현**== 한다는 것이 paper #2 의 핵심 발견이다.

---

## 데이터 파일 (참고용)

- `output/paper_figures_v1/binding_curves_v1_paper_figure.csv` — Figure 1 raw 값
- `output/paper_figures_v1/bond_density_v1_paper_figure.csv` — Figure 2 raw 값

#paper #adhesion #vacancy #halogen #micro-to-macro #mechanism
