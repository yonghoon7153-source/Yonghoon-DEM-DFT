---
title: "cascade 3,615행은 237설계였다 — 표본 계약을 다시 쓴다"
date: 2026-08-28
updated: 2026-08-28
tags: [cascade, doping, pareto, sampling, pseudo-replication, review/codex]
status: 채택
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-28
verifiedBy: "정본 CSV 실측 — concentration 열이 3,615행 전부 0.25. 도구 selftest 30건(음성 8건) 통과. 재현: python3 tools/doping/axis_corr_csv.py --pareto"
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

# cascade 3,615행은 237설계였다

> 리뷰 K ② 의 지시("그룹 키로 묶고, 무효 축은 도구가 거부하게")를 실행한 결과.
> **새 계산 0.** 있던 CSV 를 바르게 세기만 했는데 세 가지가 달라졌다.

## 0. 한 줄

행을 설계로 착각했고, 9일 전 무효 판정한 축을 다시 썼고, **핵심 축 두 개에는 데이터가 아예 없었다.**

## 1. 3,615 → 237

`n_units = max(1, round(n_fu_actual × x))` 인데 `n_fu_actual = 4` 다.
`round(4×0.02) = round(4×0.05) = round(4×0.10) = 0` → `max(1,0) = 1`.

⇒ **`concentration` 열이 3,615행 전부 `0.25`.** x020·x050·x100 은 같은 조성의 다른 이름이다.

| 세는 방법 | 개수 |
|---|---:|
| 행 (`name`) | 3,615 |
| 시드 접미사 `_sNN` 제거 | 723 |
| 가짜 x 라벨까지 제거 | 229 |
| **조성 + 자리 + 전하보상 (채택)** | **237** |

설계당 복제본 15개(가짜 x 3 × 시드 5), 공도핑 4건만 30개.

⚠ 이름 기반(229)과 조성 기반(237)이 **8개 다르다.** 어느 쪽도 아직 검증 안 했다 —
조성 기반을 쓰는 이유는 이름을 안 믿기 때문이지 더 정확하다고 확인해서가 아니다.

## 2. 무효 축을 다시 쓰고 있었다

2026-08-19 에 우리가 직접 내린 판정:

| 축 | 판정 |
|---|---|
| `screen_dV_over_V0` | ⛔ 무의미 — 미수렴 기준 대비 미수렴 값 |
| `screen_de_per_atom` 절대값 | ⛔ 인용 금지 — 기준이 미수렴 |

그런데 **2026-08-28 A3 Pareto 를 이 둘을 넣은 채로 돌렸다.** 9일 전 카드가 repo 안에 있었다.

⇒ 도구가 거부하게 했다. `INVALID_AXES` 에 사유와 날짜를 달고, 뚫으려면
`--allow_invalid_axes` 를 명시해야 하며 그 경우 출력에 인용금지가 찍힌다.

## 3. 🔑 핵심 축 두 개가 **비어 있다**

바른 축 집합으로 돌리니 채점 가능 행이 **0개**로 나왔다. 원인:

| 축 | 채움 |
|---|---:|
| `sigma_300K_S_cm_NE` (σ 300 K) | **0 / 3,615** |
| `wad_J_m2_mean` (계면 부착일) | **0 / 3,615** |
| `bvs_li_proxy_score` | 227 / 237 설계 |
| `elastic_G_hill_GPa` | 227 / 237 |
| `elastic_pugh_GoverB` | 227 / 237 |
| `migration_volume_fraction` | 227 / 237 |

**전도도와 계면 부착일 — 우리 문제의 목적 그 자체인 두 축에 값이 한 줄도 없다.**
남은 4축은 이동도 재료 2개 + 탄성 2개다. 즉 지금 cascade 의 "다목적" 은
*전도도를 뺀* 다목적이다.

한 축이라도 완전히 비면 교집합이 0 이 되어 front 가 통째로 사라지는데,
예전 출력은 *"채점 가능 0개"* 한 줄뿐이라 **어느 축 때문인지 안 보였다.**
이제 축별 채움을 찍고, 빈 축은 이유를 말하며 뺀다.

## 4. 바른 수치 (옛 수치 철회)

| | 옛 (2026-08-28 오전) | 새 |
|---|---|---|
| 표본 | 3,615행 중 681 (18.8 %) | **237설계 중 227 (95.8 %)** |
| front | 160 / 681 (23.5 %) | **39 / 227 (17.2 %)** |
| 축 | 6–8개 (무효 2개 포함) | **4개 (전부 유효)** |

⇒ **`front 160/681` 은 철회.** 채움률 18.8 % 도 철회 — 복제본이 분모를 부풀린 것이지
데이터가 그만큼 비었던 게 아니다. 설계 단위로는 **95.8 % 가 채워져 있다.**

축 독립성: 유효 4축은 설계 단위(n=227)에서 **|ρ| ≤ 0.32**, 공선성(|ρ|>0.85) 없음.
⇒ 뭉개진 축이 아니라 **진짜 4축 문제**다. front 39개는 그 위에서 뜻이 있다.

front 상위(알파벳순): CaCl₂ · CaO · CaS · Cu₂O · Ga₂O₃ · Gd₂O₃ · GeS₂ · HfCl₄ · HfO₂ ·
LaCl₃ · LaF₃ · Li₂O · LiBr · Mg₃N₂ · MgS · Na₂S · Sb₂O₅ · Sb₂S₃ · SiO₂ …

## 5. ⛔ 이 카드가 말하지 않는 것

- **front 39개는 순위가 아니다.** 집합이고, 그 안의 선택은 사람이 한다.
- **σ 가 비어 있다는 건 "σ 가 나쁘다" 가 아니다.** 안 쟀다는 뜻이다. 채우면 front 가
  통째로 바뀔 수 있다 — 지금 39개는 *전도도를 안 본* front 다.
- 조성 기반 그룹 키는 **원자 매핑 해시가 아니다.** 같은 조성·다른 배치는 여기서
  한 설계로 묶인다 (그건 사실상 시드라 묶는 게 맞지만, 구조가 진짜 다르면 놓친다).
- 복제본 산포를 **오차막대로 쓰면 안 된다.** 같은 파이프라인·같은 설정이라 계통오차가 공통이다.
- 4축 중 BVS 프록시와 이동부피비는 `li_mobility_score` 의 **재료**다. 서로는 독립
  측정이지만(ρ −0.19), 둘 다 넣으면 이동도 방향에 가중치가 두 번 간다는 지적은 여전히 유효하다.

## 6. 연결

- `db/properties/cascade_design_contract_2026_08_28.json` — 실측 기록 + CSV SHA256
- `kb/reviews/codex_K_what_next_after_seminar_2026_08_28.md` — ② 를 지시한 리뷰
- `kb/projects/cascade_pipeline_fixes_2026_08_19.md` — 무효 축 원 판정
- `kb/methodology/selftest_blind_spots_2026_08_28.md` — **사각 D**(우리 판정을 안 읽는다)의 사례
- `tools/doping/axis_corr_csv.py` — `INVALID_AXES` · `design_key` · `axis_fill`
