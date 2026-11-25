---
title: "오늘 원고에 넣을 수 있는 DFT 문장 — 새 계산 없이"
date: 2026-08-29
updated: 2026-08-29
tags: [manuscript, sdcp, dft, closure, citable]
status: 사용 중
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-29
verifiedBy: db/properties/sdcp_neutral_closed_2026_08_28.json + 좌표 재측정
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: multi-source-primary
---

# 오늘 나가는 원고 — 디스크에 있는 것만으로

> 새 계산 0건. 아래 ✅ 는 `db/properties/sdcp_neutral_closed_2026_08_28.json` 의
> `허용_서술_이대로만_쓴다` 와 철회 항목의 **실측 좌표**에서 그대로 온다.

## ✅ 써도 되는 것

### 1. 접촉 기하 — ⚠ **2026-08-29 재판정: legacy 자세에 한정된다**

에너지 기준 비대칭(δ_m·δ_LREAL)은 **거리에 영향을 주지 않는다.** 좌표는 좌표다.
다만 **어느 자세의 좌표인가**가 결정적이다 — 두 집합이 서로 다른 말을 한다.

**legacy(wave1) 4자세 — DFT 단일점을 실제로 받은 것들**

> In the four wave-1 configurations, the acidic sulfonic O–H hydrogen lies
> 7.08–7.17 Å from the slab and the sulfonate oxygens 4.88–5.39 Å from the
> nearest surface Li; the closest contacts are carbon-bound H ··· surface O/Ni
> at 2.44–2.46 Å.

**신규(동결) 후보 최저 2자세 — MLIP 기하, DFT 아직 없음**

> b00 `O_top__fib08__r000`   : 산성 O–H 1.020 Å · H ··· 표면 O **1.827 Å**
> b01 `LiO_bridge__fib08__r000`: 산성 O–H 1.018 Å · H ··· 표면 O **1.848 Å**
> (같은 자세의 C-결합 H 는 슬랩에서 3.38–3.95 Å)

⇒ **신규 최저 자세에서는 술폰산이 표면 O 와 수소결합한다.** O–H 가 자유값 ~0.97 Å
에서 1.02 Å 로 늘어난 것도 실제 주개라는 것과 정합적이다.

⛔ **오늘 원고에 이 수소결합을 쓸 수 없다** — MLIP 기하이고 DFT 확인이 없다.
   Stage A 의 b00·b01 이 정확히 그 확인이다.
⛔ 반대로 *"술포네이트가 표면과 상호작용하지 않는다"* 도 **이제 못 쓴다** — legacy
   자세에 한정된 관찰이었다는 것이 드러났다.

### 3. 자리 선호 (조각 내부 — 분자 기준이 소거되므로 살아 있다)

> For the CF₃–(CF₂)₈–CF₃ fragment, the Li-top electronic energy was 49.8 meV
> lower than Ni-top for a matched UMA-selected pose pair (single pm1 magnetic
> label).
>
> For the C₄H₂F₈ fragment, Li-top was 36.1 meV lower; the two labelled jobs
> (pm1 and net4-B/B) reached the same realized basin and their ΔE_site agreed to
> 0.087 meV.
>
> For the neutral SDCP fragment the site contrast (+9.27 meV) is **unresolved**
> at the 30 meV pre-registered decision floor.

⛔ neutral 을 *"no site preference"* 로 쓰면 안 된다 — 판정바닥 아래는 판정이 아니다.
⛔ dimer 를 *"두 자기 시드에서 재현됐다"* 로 쓰면 안 된다 (입력 INCAR 미회수).

### 4. 수렴

> Molecular reference boxes converged between 20 and 24 Å to 0.057–0.322 meV
> against a 10 meV gate.

### 5. 문헌 — ⛔ **"불일치" 라고 쓰면 안 된다 (2026-08-29 정정)**

Han 2025 (Adv. Mater., ICEP)는 NCM811(001) 위 ICEP_AMPS 의 결합을 *"술폰산기와 표면
산소 사이의 강한 수소결합"* 으로 귀속한다. **우리 신규 최저 자세가 바로 그 모티프다**
(위 §1). 초판에서 "우리는 그 모티프를 관측하지 못했다" 고 적었는데 **철회한다** —
그것은 legacy 자세만 본 진술이었다.

지금 상태에서 문헌에 대해 쓸 수 있는 것은 **없다.** DFT 확인 전이다.

---

## ⛔ 오늘 쓰면 안 되는 것

| 문장 | 왜 |
|---|---|
| 절대 흡착에너지 (−0.77 eV 등) | 기준 비대칭 δ_m(NUPDOWN 제약 분자) + δ_LREAL(복합체 T vs 분자 F) 미측정 — 회신 P |
| **0.346 eV** · "SDCP 가 PTFE 보다 강하게 붙는다" | 위와 같음. 부등호 방향 서술도 보류 |
| "O···Li 2.09 Å" (술포네이트 O 가 Li 에 배위) | **철회** — 어느 구조에서도 재현 안 됨 (회신 T P0-1) |
| "술포네이트가 표면과 상호작용하지 않는다" | ⛔ **이것도 못 쓴다** — 신규 최저 자세는 O–H···O 1.83 Å 수소결합 (2026-08-29) |
| 그 수소결합 자체 | 아직 **MLIP 기하**뿐 — Stage A b00·b01 의 DFT 가 나와야 쓴다 |
| "자리 불문" · neutral "무선호" | 30 meV 판정바닥 아래 |
| PTFE **고분자**로 확장 · 접착력/계면저항 | 조각 vs 조각, 진공 0 K 단분자 |
| 타 코드·문헌 절대값과 직접 비교 | VASP PAW 총에너지 |

---

## 🔓 하룻밤이 있으면 — 조각 간 대비를 되살리는 **4잡**

기준 비대칭을 없애려면 복합체와 분자를 **같은 규약(all-F · free-spin)** 으로 맞추면
된다. `/data/work/runs/sdcp_stageA_v1` 에 **이미 그 잡들이 들어 있다.**

```bash
B=/data/work/runs/sdcp_stageA_v1
# 이 넷만 돌린다 (나머지 36잡은 건드리지 않는다)
ls -d $B/prospective/sdcp_neutral__b00__afm2424_pm1 \
      $B/prospective/ptfe_c10__b00__afm2424_pm1 \
      $B/refs/mol__sdcp_neutral__box24 \
      $B/refs/mol__ptfe_c10__box24
```

- 가장 긴 잡 **19 h** (256코어) — 동시 4잡이면 하룻밤
- 나오는 값: `A(SDCP,b00) − A(c10,b00)` — 슬랩이 소거되는 조각 간 대비
- ⚠ 이것은 `min over poses` 가 **아니다.** 쓸 수 있는 문장은
  *"각 조각의 UMA-최저 후보 한 쌍에서, 동일 all-F 고정기하 단일점 규약으로"* 까지다.
  `primary` · `low-energy` · `pose-insensitive` · `전역 최소` 는 **금지** (회신 V).

## 📌 오늘 안 하는 것

- Stage A 전체 40잡 (133k 코어시간) — **원고 숫자를 안 낸다.** 창 W 와 J_f 만 낸다.
- Stage B (최대 277잡) — 리뷰어가 그린 절차지 이번 원고의 경로가 아니다.
