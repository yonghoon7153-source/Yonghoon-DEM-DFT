# Cascade 재감사 정본과 dftweb 수정 계약

**작성일:** 2026-08-14  
**적용 대상:** cascade 계산 캠페인, dftweb `/cascade`, 연구 세미나 PPT·대본, 후속 ML 계획  
**상태:** `9abe5105` 고정 소스에 대한 릴리스 정본. 현재 승인 leaderboard는 0종이며,
회수된 90종은 audit/status와 raw download까지만 공개한다.

> 이 문서를 먼저 읽고 작업한다. 과거 `cascade_screening_funnel.json`, 47종 leaderboard,
> `cascade_pipeline_anatomy_2026_08_13.md`의 해석을 그대로 재사용하지 않는다. 파일이 존재하거나
> `STAGE_*.DONE`가 있다고 해서 그 물성이 계산·수집·검증됐다고 간주하지 않는다.

> **2026-08-14 추가 차단:** `ranked_v2/themes_v2/funnel_v2`는 89종 diagnostic이다.
> AlI3가 전면 결측이고 MgI2는 G4 x005 입력이 없다. `cascade_pool_audit_v2.json`의
> 71/18/1은 B0를 포함하고 Pugh를 누락해 gate completeness가 아니다.

## 1. 지금 확정된 캠페인 계보

| 질문 | 현재 정본 |
|---|---|
| 273은 무엇인가 | 91개 명목 화합물 × `x002/x005/x010` 세 실행 라벨 = 273개 상위 run slot |
| 실제 완주 | 270/273. `As2S3` 세 라벨만 구조 생성 단계에서 종료 |
| 실제 농도 | 1×1×1, 4 f.u. 셀의 정수 치환 때문에 세 라벨 모두 실제 `x=0.25`. 농도 스윕이나 반복실험이 아님 |
| 완주 원자료 | `unified_dataset_273.csv`: 3615행, 90종, 2026-07-11 자동 통합 |
| 왜 정본은 47종이었나 | 풀을 정의한 `cascade_v23_all.csv`가 2026-06-29의 O 37 + F 10 snapshot에서 멈췄고, 7월 11일 완성된 자동 통합본으로 교체되지 않았음 |
| 원인 | 자동 통합은 있었지만 통합본을 정본 풀로 승격하는 writer·handoff·completeness gate가 없었고, 관련 작업도 gabia 미푸시 로컬 브랜치에 갇혔음 |
| 회수 | 90종 270 champion의 grand-potential 배치를 회수. 옛 141건과 겹치는 `ox_V` drift는 0 |
| 회수의 의미 | 새 계산이 아니라 등록 복원. `recovered`이지 곧바로 `approved/canonical`은 아님 |
| 현재 파생표 | 89종 diagnostic. AlI3 전면 결측, MgI2 축별 결측. 승인 leaderboard는 0종 |

`register_cascade_to_db.py`가 존재했다는 사실도 이 경로를 자동화했다는 증거가 아니다. 그 도구는
`doping_cascade.json`을 쓰는 초기 등록기이고, 풀을 정의한 `cascade_v23_all.csv`의 writer는 아니다.
`unified_dataset_273.csv` 자동 집계와 정본 CSV 승격 사이가 수동 handoff로 남아 있었다. 47종은 물리적으로
걸러진 생존자 집합이 아니다. 역사 실행 roster의 첫 47종이 6월 snapshot에
등록된 것이다. 43종은 나쁜 후보도, gate 탈락 후보도 아니다. `As2S3`만 확인된 seed-generation failure다.

gabia의 cascade 관련 체크아웃·run tree·최근 산출물에 대한 **파일 census는 닫혔다**. 현재 남은 위험은
“파일을 더 못 찾았다”가 아니라, 찾은 파일의 producer 코드·단위·phase set·status를 잘못 해석하는 것이다.

## 2. 숫자마다 무엇을 재는지 다시 고정한다

### 2.1 G1: 역사 G1은 vacuous지만, 이유는 풀의 성질이다

- 역사 G1은 host 대비 UMA 상대 에너지라 47/47을 통과했다.
- 별도 `cascade_stability_axes.csv`에는 MP compound-entry 기반 `e_above_hull_meV`가 47종 전부 있다.
- 46종은 0 meV/atom, 최대 `CrO3`도 46.2 meV/atom이라 50 meV 컷에서 탈락 0종이다.
- 결론: `E_above_hull`이 없어서 G1이 비어 있던 게 아니다. 애초 안정한 흔한 이성분 O/F 후보를
  골랐기 때문에 hull 기준을 써도 비어 있다.
- stage 09e의 `hull_E_at_winner_composition_eV_atom`은 별개다. 후보의 energy-above-hull이 아니라
  해당 조성에서의 MP 평형 에너지와 분해 조합이다. G1 값으로 쓰지 않는다.

### 2.2 G3: 절대 2.14 V가 아니라 phase-set별 host-relative 판정이다

- 기존 G3는 선택한 phase set에서 host onset `2.14 V`를 기준으로 썼다.
- `esw_lis4excluded.json`에서 `LiS4` 등을 제외하면 comp1과 modelc host onset이 `2.256 V`로 이동한다.
- 따라서 `2.14 V`는 물질 고유 상수가 아니다. phase inventory, MP entry set, correction protocol을 포함한
  `method_id`와 함께 써야 한다.
- 기존 2.14-V batch와 LiS4-excluded host 값을 섞어 후보를 재분류하면 안 된다. 같은 phase set으로 host와
  후보를 함께 재계산해야 한다.
- dftweb에는 `host_anchor_V`, `phase_set_id`, `excluded_entries`, `method_id`를 노출한다.

### 2.3 G4: 역사 결과는 Li transport가 아니라 두 프록시를 합친 pool-relative gate다

역사 `bvse_proxy.py`의 규약은 현재 정본 softBV/BVSE 규약과 다르다.

- 역사 BVS 파라미터 예: S `R0=1.94, b=0.40`, Cl `R0=1.91, b=0.37`.
- 현재 프로젝트 정본: S `2.105`, Cl `2.249`, O `1.466`, 모두 `b=0.37`,
  `BVSE=(BVS-1)^2` 및 연결 채널 판정.
- 역사 `bvs_li_proxy_score`는 Li-site BVS 평균과 표준편차의 휴리스틱이다. 경로 연결성, 장벽, 확산계수,
  전도도가 아니다.
- `dopant_blocking_fraction`은 `{Li,P,S,Cl}` 이외 원자에서 4 Å 안에 있는 Li의 비율이다.
  통로·장벽·percolation이 아니라 local foreign-center coverage다.
- 262 champion에서 이 값과 foreign-atom count의 Pearson `r=0.876`, `R²=0.768`이다.

역사 빌더의 식은 다음과 같다.

```text
n = minmax(bvs_li_proxy_score within the current pool)
if blocking < 0.60:
    transport_norm = 0.10 + 0.90*n
else:
    transport_norm = 0.05
G4 pass: transport_norm > 0.30
```

따라서 `transport_norm=0.05`는 낮은 BVS를 독립적으로 관측한 값이 아니라 blocking 실패가 만든 floor다.
47종 G4 단독 탈락 27종 중 24종은 blocking 상수에, 3종만 BVS branch에 걸렸다.

산화 onset을 올린 역사 6종에 대해 blocking을 제거하고 원래 BVS score만 같은 47종 풀에서 재정규화하면:

| 후보 | blocking 없는 transport score | 0.30 통과 여부 |
|---|---:|---|
| Cr2O3 | 0.8086 | 통과 |
| Ga2O3 | 0.3989 | 통과 |
| In2O3 | 0.6652 | 통과 |
| Sc2O3 | 0.4868 | 통과 |
| Y2O3 | 0.8825 | 통과 |
| B2O3 | 0.1000 | 탈락 |

그러므로 “산화가 좋아진 6종이 독립적인 Li-path/BVSE 축에서도 모두 나빴다”는 결론은 성립하지 않는다.
확정할 수 있는 것은 **역사 composite G4에서 6/6이 멈췄다**는 gate-audit 사실뿐이다. 그중 5종은
4 Å loading cutoff가, B2O3는 BVS branch가 결정했다. 이를 물리적 산화–수송 trade-off라고 부르지 않는다.

### 2.4 dual-x: 농도 구조는 맞지만 transport 검증은 아니다

- `dualx_v23`은 co-doping이 아니라 같은 2×2×1 셀에서 `x=0.0625`와 `x=0.25`를 비교한 10종 농도 실험이다.
- 설계상 stage 04 이후 멈췄고 stage 05/06은 불완전한 잔재다.
- 고농도에서 blocking이 커지는 것은 4 Å coverage 정의상 대부분 예상된다. 전도도 회복이나 경로 복원을
  증명하지 않는다.
- `de_post_anneal`은 조성이 다른 구조의 UMA E/atom에서 pristine baseline을 뺀 값이다. 형성에너지나
  도펀트 상호작용 에너지가 아니므로 4배 가산성, sub-linear 안정화, repulsion을 주장하지 않는다.

### 2.5 stage 10/11: main v23에는 인용 가능한 sigma·W_ad가 없다

- v23 main campaign은 `TOP_K_SIGMA=0`, `TOP_K_NCM=0`으로 실행됐다.
- v22 radius-only pilot에는 stage marker 7/6이 있지만 수집된 sigma/Wad 행은 0이고 raw success·lineage가
  검증되지 않았다.
- producer/collector schema도 stage 11에서 `label` 대 `name`으로 갈린다.
- 웹·발표 문구는 “v23 미실행; v22 pilot marker만 있고 usable label 0”으로 통일한다.

### 2.6 Cl-rich와 회수 화학: 조건부 단서이지 pair proof가 아니다

- plain 대비 seeded `chain_Cl`에서 WO3/MoO3/Al2O3는 약 +0.214~0.216 V, Nd/Sm은 소폭 상승,
  Zn/Mg/Y는 변화 없음, Sc는 -0.017 V다.
- 이는 같은 cascade의 Cl-rich seed 변형이지 명시적 co-doped pair label이 아니다.
- Ga2O3/Ga2S3, Al2O3/Al2S3의 비슷한 onset은 “oxide만의 효과” 해석을 깨지만,
  “양이온 하나가 onset을 결정한다”까지 증명하지 않는다.
- explicit pair label은 여전히 0개다.

### 2.7 계면 반응 축은 없던 게 아니라 core funnel 밖에 따로 있었다

`cascade_stability_axes.csv`/`cascade_stability_axes_verdict.json`은 역사 47종에 대해 양극,
LPSCl SE, Li 금속 계면의 0 K pseudo-binary 반응 구동력을 이미 계산했다.

- 양극 full/half 축은 각각 2/3종만 탈락한다.
- LPSCl SE 축은 29/47종, Li 금속 축은 35/47종을 탈락시킨다.
- 역사 G1–G4 생존 11종 중 SE 또는 Li 축을 추가하면 8종이 더 빠지고 CaF2/LiF/MgO 3종이 남는다.
- 다만 100 meV/atom cutoff 하나에 지배되고, Li 축은 개질제가 실제 Li 금속과 접촉하는 설계에서만 적용된다.
- 결과 요약 JSON은 재현 generator가 없고 사후 추적 confidence가 medium이다.

따라서 “interface reaction 데이터가 없다”는 문장은 틀리다. 정확한 표현은 “역사 47종에 post-hoc
계산됐지만 core funnel에 편입되지 않았고, 90종 확장·cutoff sensitivity·적용 geometry가 미검증”이다.
역사 conditional Pareto 4종도 이 축을 넣으면 그대로 유지되지 않으므로 winner set으로 인용하지 않는다.

### 2.8 회수 17개 중 바로 폐기·재생성해야 하는 파일이 있다

- `sei_product_gaps.json` 생성기는 `energy_above_hull == 0`을 falsy로 취급해 안정상을 뒤로 밀었다.
  13개 중 11개가 양의 `E_above_hull` polymorph이고 LiCl도 안정한 entry가 아니다. 현재 gap 절대값과
  전자절연성 순위는 **invalid**다. `is not None` 조건으로 고친 뒤 다시 조회한다.
- `esw_lpscl_profile.json`은 raw profile은 재파싱할 수 있지만 저장된 summary가 comp1
  `0.87/0.87 V`, width `0`, modelc `None`으로 잘못돼 있다. direct reader에서 막는다.
- `esw_lpscl_hull.json`과 `esw_comp1_mp.json`도 host ESW 정본으로 쓰지 않는다.
- constrained-ESW의 leading/full-relax/hybrid 모드는 `K>0`에서 서로 상충한다. 압력에 따른 product-set
  민감도 진단은 가능하지만 sweet spot이나 정량 window headline은 금지한다.

따라서 “회수됨”은 “표시 가능”이 아니다. 각 artifact에는 최소 `historical`,
`recovered_unvalidated`, `approved`, `superseded`, `invalid` 중 하나의 상태가 있어야 하고,
webapp은 `invalid`와 method-mismatch를 기본 화면에서 fail-closed한다.

## 3. 지금 허용되는 결론과 금지되는 결론

### 허용

1. 캠페인 설계와 단계별 계산은 체계적이었지만, 자동 집계 이후 정본 등록이 수동이라 계산과 공개 데이터가 갈라졌다.
2. 47종 funnel은 2026-06의 역사 snapshot 감사 결과이고 90종 현재 endpoint가 아니다.
3. G1의 0-kill은 안정한 O/F 풀을 미리 고른 결과다.
4. 역사 G4는 current BVSE/전도도가 아니라 pool-relative BVS score와 4 Å loading heuristic의 합성 gate다.
5. 회수된 GP 결과와 Cl-rich 변형은 다음 검증 질문을 만든다. 아직 universal winner나 co-doping 성공을 만들지 않는다.
6. 이 캠페인의 가장 중요한 성과는 후보 1등보다 **어떤 계산·등록·metric contract가 다음 결론을 좌우하는지** 드러낸 것이다.

### 금지

- “273개 후보를 물리적으로 47개로 줄였다.”
- “x002/x005/x010은 2/5/10% 농도 의존성 또는 3개 반복이다.”
- “47→43→25→11은 현재 90종 전체 funnel이다.”
- “6/6은 산화 개선과 Li transport의 물리적 trade-off 증거다.”
- “transport_norm=0.05이므로 blocking을 빼도 BVSE에서 떨어진다.”
- “09e는 E_above_hull이다.”
- “2.14 V는 phase set과 무관한 LPSCl 고유 onset이다.”
- “dual-x가 저농도에서 Li transport를 회복했다.”
- “ML이 새 co-dopant pair의 물성을 예측했다.”
- “계면 반응 축은 아직 계산되지 않았다.”

## 4. dftweb `/cascade` P0 수정 계약

### 4.1 기본 화면을 leaderboard에서 audit/status로 바꾼다

현재 `webapp/data.py`와 `webapp/templates/cascade.html`은 옛 47종 파일을 직접 읽어 leaderboard,
score, Pareto, “Li transport”, G1–G4 endpoint를 현재 결과처럼 보여준다. 이 상태는 fail-open이다.

기본 화면의 첫 네 숫자는 다음으로 바꾼다.

```text
planned slots       273
completed slots     270
completed species    90
historical snapshot  47
```

그 아래에 상태를 명시한다.

```text
Historical 47-species snapshot: reproducible, superseded for campaign coverage
Recovered 90-species outputs: recovered, not yet re-ranked/re-gated
Current approved leaderboard: unavailable
Explicit co-doped pair labels: 0
```

### 4.2 versioned artifact manifest를 단일 진입점으로 둔다

새 manifest에는 최소 다음 필드를 둔다.

```json
{
  "artifact_id": "cascade-v23-...",
  "dataset_version": "...",
  "status": "historical|recovered_unvalidated|approved|superseded|invalid",
  "species_count": 47,
  "slot_count": 141,
  "actual_x": 0.25,
  "campaign_labels": ["x002", "x005", "x010"],
  "method_id": "...",
  "phase_set_id": "...",
  "pool_id": "...",
  "source_path": "...",
  "source_commit": "...",
  "sha256": "...",
  "generated_at": "...",
  "limitations": []
}
```

모든 cascade loader와 API는 이 manifest의 `status`를 확인한다. unknown status, method mismatch,
pool mismatch는 표시하지 않고 fail-closed한다. `canonical_registry.json`에 cascade entry가 없다는 사실도
명시한다. “canonical 47”은 registry canonical이 아니라 versioned operational snapshot이었다.

### 4.3 탭과 명칭을 바꾼다

| 현재 | 변경 |
|---|---|
| Leaderboard | Historical 47 snapshot (비기본, superseded 배지) |
| Pareto-optimal | Historical axis-dependent Pareto; winner 아님 |
| Li transport | Legacy BVS + 4 Å foreign-center proxies |
| Oxidation ESW | Grand-potential output + method/phase-set ID |
| Co-doping | Hypothesis queue; explicit pair labels = 0 |
| Funnel | Historical gate audit; 90종 rebuild pending |

`screening hit`, `winner`, `DFT-verified` 같은 배지는 실제 검증 단계를 분리해 쓰고,
UMA convergence audit를 DFT verification으로 표시하지 않는다.

### 4.4 G3/G4를 식과 함께 노출한다

- G3 카드: `host-relative within phase_set_id`; 2.14 V와 LiS4-excluded 2.256 V를 나란히 보여주되
  서로 다른 method로 후보 순위를 섞지 않는다.
- G4 카드: 원래 `bvs_li_proxy_score`, blocking fraction, pool min/max, floor rule, 최종 transport_norm을
  모두 보여준다. `transport_norm=0.05`에는 “forced by blocking gate”를 표시한다.
- Interface 카드: 47종 post-hoc 결과와 100 meV cutoff sensitivity를 함께 보여주고, Li 축은 적용 geometry를
  선택해야만 활성화한다. core funnel 미편입 상태를 `POST_HOC`로 표시한다.
- 47→90 pool이 바뀌면 min-max 값도 바뀌므로 옛 norm은 자동 invalid/superseded 처리한다.
- legacy BVS와 current canonical BVSE를 같은 열·같은 색 범례로 표시하지 않는다.

### 4.5 자동 검증 테스트

1. 273/270/90/47 숫자가 manifest와 원자료에서 일치하는지.
2. `x002/x005/x010`을 농도값으로 렌더링하지 않는지.
3. `transport_norm=0.05` 행이 raw BVS failure로 설명되지 않는지.
4. pool ID가 바뀌면 normalized score, Pareto, rank, funnel을 stale로 막는지.
5. phase-set ID가 다른 onset을 한 leaderboard에서 비교하지 않는지.
6. recovered artifact가 approved/canonical 배지를 받지 않는지.
7. explicit pair label count가 0인데 co-doping “prediction”을 결과로 노출하지 않는지.
8. post-hoc interface axis를 “missing”이나 “approved core gate” 어느 쪽으로도 잘못 표시하지 않는지.

## 5. ML은 predictor가 아니라 검증 순서 관리자다

현재 ML은 새 화학의 물성 예측기로 쓸 수 없다.

- Stage-1 LOOCV `R²=0.9998`: score 공식을 복원한 결과.
- pair LOOCV 약 `0.089`, LODO 약 `-0.18`, L2DO 약 `-0.25`.
- 1081쌍 전역 발굴은 1.22×, `p=0.43`: 무작위와 구별되지 않는다.
- 이미 heuristic으로 고른 40쌍 안의 정렬은 더 낫지만, 이것도 실제 pair 물성 검증이 아니라 v1 queue 재현이다.

따라서 acquisition 순서는 다음처럼 둔다.

1. **VALIDATE:** G3 phase-set sensitivity, G4 metric semantics, realistic-x current BVSE를 먼저 닫는다.
2. **RECOVER:** 90종 동일 method/pool로 rank·gate를 재생성한다.
3. **EXPLORE:** 불확실하고 서로 다른 화학 계열의 소수점을 고른다.
4. **EXPLOIT:** 검증된 label이 생긴 뒤에만 모델 score를 순서 보조로 쓴다.
5. 각 DFT/MD 결과를 새 label로 되먹여 다음 acquisition을 갱신한다.

첫 pair를 곧바로 “산화 후보 ⊕ transport 후보”로 고르는 것도 아직 이르다. 역사 6/6의 transport 해석이
무너졌으므로, 먼저 single-modification의 실제 농도와 current BVSE/MD 축을 확인한다.

## 6. 세미나의 새 중심 결론

> 이 연구가 확정한 것은 단일 첨가제의 보편적 1등이나 산화–수송 trade-off가 아니다.
> 체계적인 계산도 provenance handoff와 metric semantics가 닫히지 않으면 다른 결론을 만든다는 점,
> 그리고 다음 비싼 계산은 그 두 경계를 먼저 검증해야 한다는 점이다.

서사는 다음 순서로 간다.

1. 91×3의 체계적 캠페인을 설계했다.
2. 계산은 90종까지 끝났지만 정본은 47종에서 멈췄다.
3. 옛 47종 gate를 다시 보니 G1은 풀 때문에 비었고, G4는 transport보다 loading 상수에 지배됐다.
4. GP onset은 phase inventory에 따라 이동하고, 별도 계면 축을 넣으면 역사 shortlist도 다시 바뀐다.
5. 따라서 현재 결과는 winner 선정표가 아니라 검증 contract와 회수 우선순위다.
6. ML은 결론을 내리지 않고 그 검증 순서만 고른다.

## 7. 아직 닫히지 않은 것

- 90종 `champions → ranked → funnel/Pareto` 동일 세대 재생성. 현재 89종 diagnostic은 승인본이 아니다.
- 축별 결측을 `missing != fail`로 처리하는 evaluator와 exact gate-completeness audit.
- `substitute_compound.py`, `select_winners.py`, `combine_rankings.py` 전체와 producer/collector schema 감사.
- 회수된 17개 JSON/CSV의 record-level status·method·source 검증.
- current canonical BVSE로 realistic-x 농도 비교.
- G3 후보 전수의 동일 phase-set 재계산.
- v22 sigma/Wad pilot raw success 여부. 본문 인용 우선순위는 낮다.
- explicit pair 계산과 실제 pair label.

이 항목이 닫히기 전에는 새 leaderboard, universal Pareto, “최종 11종”, co-doping 추천을 배포하지 않는다.
