---
title: "오늘 원고에 넣을 수 있는 DFT 문장 — 새 계산 없이"
date: 2026-08-29
updated: 2026-08-29
tags: [manuscript, sdcp, dft, closure, citable]
status: 사용 중
confidence: high
verificationStatus: verified
explored: false
authoredBy: agent
effort: medium
claimType: descriptive
evidenceScope: multi-source-primary
---

# 오늘 나가는 원고 — 디스크에 있는 것만으로

> 새 계산 0건. 아래 ✅ 는 `db/properties/sdcp_neutral_closed_2026_08_28.json` 의
> `허용_서술_이대로만_쓴다` 와 철회 항목의 **실측 좌표**에서 그대로 온다.

## ✅ 써도 되는 것

### 1. 접촉 기하 — **이게 오늘 가장 강한 결과다**

에너지 기준 비대칭(δ_m·δ_LREAL)은 **거리에 영향을 주지 않는다.** 좌표는 좌표다.

> In the evaluated geometries (MLIP-relaxed, DFT single-point; not DFT-optimised),
> the acidic sulfonic O–H hydrogen lies 7.08–7.17 Å from the slab and the
> sulfonate oxygens 4.88–5.39 Å from the nearest surface Li. The shortest
> molecule–surface contacts are instead carbon-bound H ··· surface O/Ni at
> 2.44–2.46 Å. Contact in these configurations is therefore made through the
> backbone rather than through the polar sulfonate group.

⚠ 반드시 같이: *MLIP-relaxed geometry, DFT single point, vacuum, 0 K, single molecule.*

### 2. 배향 선호 — 위와 독립적으로 같은 결론

> Across the relaxed MLIP screen, sulfonate-down orientations ranked 88th of 109
> surviving poses (81st percentile), 0.39 eV above the lowest-energy pose; in the
> rigid screen the best sulfonate-down orientation ranked 101st of 322.

⚠ MLIP 절대값·조각 간 비교는 **인용 금지** (부호가 DFT와 반대). **순위만** 쓴다.

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

### 5. 문헌과의 불일치 — 쓸 수 있고, 쓸 값어치가 있다

Han 2025 (Adv. Mater., ICEP)은 NCM811(001) 위에서 ICEP_AMPS 의 결합을
*"술폰산기와 표면 산소 사이의 강한 수소결합"* 으로 귀속한다. 우리는 LiNiO₂(104)
위의 이 조각에서 **그 모티프를 관측하지 못했다** (위 §1).

> ⚠ 서로 다른 표면·조각·코드(CASTEP vs VASP)이므로 **절대값 비교는 하지 않는다.**
> 관측된 접촉 모티프가 다르다는 사실만 적는다.

---

## ⛔ 오늘 쓰면 안 되는 것

| 문장 | 왜 |
|---|---|
| 절대 흡착에너지 (−0.77 eV 등) | 기준 비대칭 δ_m(NUPDOWN 제약 분자) + δ_LREAL(복합체 T vs 분자 F) 미측정 — 회신 P |
| **0.346 eV** · "SDCP 가 PTFE 보다 강하게 붙는다" | 위와 같음. 부등호 방향 서술도 보류 |
| "술포네이트가 표면을 앵커링한다" · "O···Li 2.09 Å" | **철회** — 실측 4.88–5.39 Å (회신 T P0-1) |
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
