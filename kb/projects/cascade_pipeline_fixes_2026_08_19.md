---
title: cascade 파이프라인 수정 목록 — codex 교차리뷰용 (2026-08-19 전수 정독 산물)
date: 2026-08-19
updated: 2026-08-19
tags: [cascade, pipeline, doping, uma, bugfix, codex-review, volume-gate]
status: 진행 — 진단 확정, 수정 미착수 (내일 codex 교차리뷰 예정)
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-19
verifiedBy: user
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

# cascade 파이프라인 수정 목록 — codex 교차리뷰용

2026-08-19 `tools/doping/` 31개 파일 전수 정독 + gabia 실측으로 나온 것.
진단은 **끝났고** 수정은 **아직 안 했다.** 이 카드가 그 작업지시서다.

진단 원본: `kb/methodology/cascade_pipeline_anatomy_2026_08_13.md` §전수 정독(A~D).

---

## 0. ⭐⭐ 확정 실측 — 게이트가 거꾸로 작동한다

gabia `00_preflight/preflight_report.json` **273/273** 전부 같은 값:

```
UMA-이완 baseline  V/atom = 27.478 Å³      E/atom = −3.6898 eV
                      입력 CIF 20.705 대비  +32.71 %
                      실험 Li₆PS₅Cl 18.43 대비  +49.1 %
```

⇒ `screen_dV_over_V0` 는 **49 % 부푼 기준에 대한 상대값**이다. 절대 밀도로 환산하면:

| | dV | → V/atom | 실험 대비 |
|---|---|---|---|
| 최대 팽창 | +14.6 % | 31.48 | **+70.8 %** |
| 중앙 (kept 대표) | −13.3 % | 23.81 | **+29.2 %** |
| 게이트 경계 | −25.0 % | 20.61 | +11.8 % |
| **dropped 중앙** | −26.8 % | 20.11 | **+9.1 %** |
| 최대 수축 | −33.1 % | 18.39 | **−0.2 %** ← 실험 밀도 |

**게이트가 떨어뜨린 100개의 범위는 18.39–20.61 Å³/atom** — 실험 밀도에서 +12 % 까지다.
남긴 것들의 중앙은 23.81 (+29 %) 이다.

> 실험 밀도 −10 %~+15 % 구간(16.6–21.2 Å³)에 든 구조 **197개 중 100개(51 %)를
> 현행 게이트가 탈락시켰다.** 게이트는 **물리적 밀도에 도달한 쪽을 골라서 버린다.**

**B₂O₃ plain**: 중앙 dV −29.13 % → **19.47 Å³/atom**. 우리 DFT `b2o3_relaxV0` 는
**19.034**. 차이 **+2.3 %**. ⇒ *"cascade 의 B₂O₃ 는 무너진 게 아니라 밀도를 유일하게
맞춘 것이었고, 그래서 탈락했다."* 1저자 최초 질문("우리 b2o3 DFT 는 어떻게 살아남았나")의
최종 답이다.

**⚠ 위험도**: preflight 의 통과 문턱이 35 % 인데 실측이 **32.71 %** 다. 2.3 %p 차로 통과했고,
그 문턱은 v4.5.5 에서 **5 % → 35 % 로 넓힌 것**이다(사유 주석: "false-failed on every UMA
cascade"). 즉 검사가 신호를 잡았는데 문턱을 옮겨 통과시켰다.

---

## 1. 수정 항목 (우선순위 순)

### P0-A. 기준 셀 — 왜 27.478 인가부터 가른다 (수정 전 진단)

UMA 는 **DFT 이완된** `modelC`(19.42) 를 +0.92 %, `b2o3_relaxV0` 를 −0.00 % 로 놔둔다.
같은 계열인데 canonical Li₆PS₅Cl 만 +32.7 % 부푼다. 후보:

1. **Li 배열** — `lpscl_F43m_24G_canonical.cif` 는 Li 를 **24g 에 완전 정렬**시킨 셀이다.
   실제 argyrodite 는 48h/24g 부분점유 무질서다. 정렬된 Li 는 Li–Li 반발이 커서 UMA 가
   벌릴 수 있다. **기준만 anneal 을 안 받는다**(Stage 04 는 winner 만 anneal).
2. **입력 셀** — 입력 CIF 자체가 a=10.2493 로 실험(9.859)보다 이미 **+12.4 %** 다.
   출처 미확인 (`fetch_mp_structure.py` 는 mp-985592 를 **준안정 다형**이라 스스로 적어 놨다).
3. **UMA task** — `omat` 로 돌린다. `omc`/`oc20` 등 다른 task 나 다른 체크포인트에서
   같은 셀이 어떻게 되는지 안 봤다.

**가르는 판 (싸다)**:
```
(a) canonical CIF 를 500 K/50 ps anneal → 재이완 → V/atom
(b) Li 무질서 셀(48h 부분점유 realization) 3개를 UMA 이완 → V/atom
(c) 실험 격자(a=9.859)로 스케일한 셀을 고정셀 이완 → 에너지 비교
(d) modelC(19.42) vs canonical(27.48) 을 같은 조건에서 나란히
```
⇒ (a)/(b) 가 19 근처면 **정렬-Li 인공물**, 그대로 27 이면 **UMA 편향**.

### P0-B. 게이트를 절대 밀도로 바꾼다

현행 `|dV| ≤ 0.25` 는 (i) 기준이 틀렸고 (ii) 이름과 하는 일이 다르다
(깨진 구조를 안 잡는다 — 대안 A/B 와 교집합 **0행**, `cascade_volume_gate_review.json`).

제안 — 셋을 **따로** 쓴다. 하나로 뭉치지 않는다.
```
G_shape   : 각도 편차 > 5° 또는 축비 > 1.25        → 이완 실패 (78행)
G_resid   : 종내 |dV − median| > 6·MAD             → 씨드 이상치 (111행)
G_density : |V/atom − V_ref(조성)| 가 과도          → 물리 밀도 이탈
            V_ref 는 **UMA 기준이 아니라** 조성별 참조(우리 DFT EOS V0 / MP hull 상)
```
`--max_dv` 를 없애지는 말고 **기본값을 끄고**(`--max_dv none`) 위 셋을 켠다.

### P1-A. `Li_24g` / `Li_48h` 중복 제거

`substitute_struct.find_host_indices_for_site()` 가 두 라벨에 **같은 Li 전체**를 돌려준다
(자기 docstring이 인정). 330쌍이 좌표까지 동일, |Δde| 중앙 1.5e-06 eV/atom.
winner 681 중 **66 슬롯이 둘 다 뽑혀 132행**이 중복 계산됐다.

수정 후보:
- (권장) `HOST_SITES` 에서 `Li_48h` 를 **빼고** `Li` 하나로 통일 + 마이그레이션 노트.
- 또는 입력 CIF 에 Wyckoff 메타데이터를 실어 진짜로 가른다 (pymatgen `SpacegroupAnalyzer`
  로 24g/48h 를 판정 — 정렬 셀에서는 48h 가 비어 있을 수 있음).
- 어느 쪽이든 **`LITERATURE_SITES` 의 `['Li_24g','Li_48h']` 표기도 같이 정리**.

### P1-B. `li_mobility_score` 가 파일에 안 들어간다 → 랭킹 30 % 사망

`bvse_proxy.py` 가 JSON 을 **먼저 쓰고**(267–273) 점수를 **나중에** 계산한다(278–282).
CSV 에서 **0/3,615**. `combine_rankings.py` 는 전부 None 인 열을 상수 0.5 로 정규화한다.
지문: `combined_score` 3,615행 **전부** `[0.1500, 0.8500]` (= 0.4·0+0.3·0+0.15 … 0.4+0.3+0.15).

⇒ **모든 챔피언(`rank_combined==1`)이 안정성+영률 둘로만 뽑혔다.**

수정: (1) 점수 계산을 write 앞으로 옮긴다. (2) `normalize()` 가 전열 결측이면
**0.5 를 조용히 돌려주지 말고 실패**하게 한다(또는 가중치를 재정규화). (3) 회귀 시험 추가.
⚠ 고치면 **챔피언이 바뀐다** — 47/90종 리더보드·계면·ESW 를 다시 돌려야 한다.

### P1-C. Type C 스윕이 조용히 3/4 소실

`halide_rich_swap()` 의 ValueError 가 try 밖 + `compound_summary.json` 을 루프 **끝에** 쓴다
⇒ 뒤쪽 조합 하나가 죽으면 **앞에서 만든 구조까지 버려진다**. `|| true` 가 에러를 삼킨다.
결과: Cl 과잉 0.4/0.6/0.8 이 **MgO·ZnO 에만** 있다(O 1개라 S_4a 가 3개 남음).
M₂O₃ 9종은 0.2 만. 44 조합 중 **17개만** 존재.

수정: (1) 각 (site, seed) 를 개별 try 로 감싼다. (2) summary 를 **증분 저장**한다.
(3) `|| true` 대신 실패를 로그에 남기고 카운트한다. (4) S_4a 잔여 자리를 **미리 검사**해
불가능한 조합은 사유와 함께 skip 한다.

### P1-D. `--method cluster` 는 실행된 적이 없다

`run_compound_batch.sh:174` 가 `--method cluster` 를 넘기는데
`substitute_compound.py:578` argparse `choices=['spread','random','first']` 가 막는다
(`select_substitution_sites` 자체는 cluster 지원). CSV 중복 name **0건**이 증거.
⇒ "Type A cluster (전구체 국소배위)" 10종 × 3농도 전멸.
수정: choices 에 `cluster`, `near_cation` 추가 + 스모크 테스트.

### P2. 낡은 주석 정리 (읽는 사람을 속인다)

| 파일 | 고칠 것 |
|---|---|
| `tier_cascade.sh` 머리 Stage map | 04/05 순서와 anneal 조건(500 K/50 ps) |
| `tier_cascade.sh` Stage 08 | "clamped-ion" → **relaxed-ion** |
| `run_compound_batch.sh` 머리 | interstitial "미구현" → 구현됨 |
| `bvse_proxy.py` docstring | proxy 식 **부호가 코드와 반대** |
| `substitute_compound.li_vacancies_needed()` | 죽은 함수 — 지우거나 실제로 쓴다 |

### P3. 우리 쪽에서 같이 볼 것

- **cascade BVSE ≠ 우리 BVSE**: `bvse_proxy.py` 는 Li–S R0 **1.94**(b **0.40**) ·
  Li–Cl **1.91**. 우리 정본은 S **2.105** · Cl **2.249**, b 0.37 (CLAUDE.md).
  `migration_volume_fraction` 도 "BVS∈[0.8,1.2] 격자점 비율"이지 채널 % 도 퍼콜레이션도 아니다.
  → `convention_check.py` 에 **교차인용 금지** 규칙을 넣을 후보.
- `select_winners.py` 가 `group_metric_spread` 를 **이미 기록한다** — best-of-N 편향 계기가
  산출물에 있는데 안 썼다. 회수해서 `champion_pool_size_bias` 카드에 붙일 것.
- `eos_ensemble` 은 rattle 5개 중 r² 최대를 고른다(또 다른 best-of-N). 시드별 B0 산포는
  `ensemble` 에 있는데 우리 CSV 는 선택값만 들고 있다 → 열 추가 후보.
- `run_md_sigma.py`(미실행)는 창이 `fit_start:끝`(50 ps)·prod 50 ps 로 우리 규약
  (2–50 ps, prod 200 ps)과 다르다. 켜기 전에 맞출 것.
- preflight 이 스스로 적기를, UMA 가 Nd₂O₃/Al₂O₃/MgO 에 ΔE/atom **−0.5~−0.9 eV** 를 주는데
  문헌은 ±0.03 eV — **20~30배**. 허용범위를 넓혀 통과시켰다. ΔE 축의 절대값 인용 금지.

---

## 2. 발표(세미나)에 즉시 반영해야 하는 것

11장 대본을 오늘 아침 한 번 고쳤는데, 이 실측으로 **또 바뀐다**:

- ⛔ "25 % 넘어간 것은 구조가 무너진 것" → **틀렸다.** 탈락 100개는 18.4–20.6 Å³/atom,
  즉 **실험 밀도에 가장 가까운 것들**이다.
- ⛔ "게이트가 독립적으로 일한다" 는 **에너지 축과 직교한다**는 뜻으로만 유효하다.
  "무너진 구조를 잡는다" 는 주장은 못 쓴다.
- ✅ 쓸 수 있는 정직한 문장: *"이 스크린의 부피 축은 MLIP 이완이 도달한 셀을
  **MLIP 자신의 host 셀**에 대해 잰 것이고, 그 host 는 실험 격자보다 크다.
  그래서 이 축은 절대 밀도 판정이 아니라 상대 지표로만 쓴다."*
- 10장 `step2_site_grid` 의 *"9칸이 전부 채워져 있다"* → **6칸 진짜 + 3칸(Li 48h) 복사본.**

## 이 카드가 말하지 않는 것

- **왜** UMA 가 canonical 셀만 32.7 % 부풀리는지 — P0-A 미실행.
- 게이트를 바꿨을 때 챔피언이 어떻게 바뀌는지 — 하위 축 재계산이 필요하다(계산 붙음).
- 다른 MLIP(MACE·SevenNet 등)에서 같은 셀이 어떻게 되는지 — 안 봤다.
- 이 문제가 `dualx_v23` 등 **다른 캠페인**에도 있는지 — 확인 안 했다.
