---
title: "인수인계 2026-08-29 — Stage A 제출·회수 (보조 세션용)"
date: 2026-08-29
updated: 2026-08-29
tags: [handoff, sdcp, vasp, stage-a, manuscript]
status: 진행
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-29
verifiedBy: 번들 생성 검산 (잡 수·자세당 3잡·라벨·dense 0) + selftest 전건 통과
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 인수인계 — 여기서부터 이어서

> **목표는 하나다: 원고에 들어갈 결합에너지 숫자를 얻는다.** 절차를 더 만들지 않는다.
> 1저자가 여러 번 말했다 — *"길 잃지 마라, binding energy 구하는 게 목적이다."*

## 0. 먼저 읽을 것 (순서대로)

1. `CLAUDE.md` — 프로젝트 규율 전체 (이게 다른 모든 것을 이긴다)
2. 이 파일
3. `db/properties/prereg_sdcp_neutral_contrast_2026_08_29.json` — 사전등록·실측·철회 기록
4. `kb/reviews/codex_X_bundle_reply_2026_08_29.md` — 왜 Stage A 구성이 지금 모양인지

## 1. 지금 상태

**던질 준비가 끝난 번들 둘** (gabia `root@121.78.116.27` · `/data/work/runs/`):

| 번들 | 잡 | 무엇을 답하나 |
|---|---|---|
| `sdcp_stageA_v2` | 40 | 절대 E_ads · 조각 간 대비 · `J_f`(자기 seed 민감도) · D3 분해 |
| `sdcp_motifprobe_v2` | 10 | **술폰산 수소결합 vs 백본접촉** — 기전 주장의 반증 시험 |

- 자세당 3잡: `pm1 D3-on` · `pm1 D3-off` · `net4 D3-on`
- 전 잡 **all-F 고정기하 static** (relax 없음), 분자 기준 free-spin, clean slab dense 없음
- 비용 모형: **256 코어/잡 × 8 동시 → 약 3일** (`tools/sdcp/vasp_cost_estimate.py`, ±2배)
- ⚠ **POTCAR 미포함** — 각 잡 폴더 `POTCAR_SPEC.txt` 의 변형(`Ni_pv` 등)대로 조립

두 번들 다 **생성·검산 완료** (2026-08-29). 총 **50잡**.
`sdcp_motifprobe_v2` 검산 실적: 잡 10 · `probe0` 3 · `probe1` 3 · `candidate_set = motif_probe (frozen motif_probe_decl) ['motif_probe']`.
⚠ `sdcp_motifprobe_v1`(7잡·1자세)은 **폐기본**이다 — 던지지 말 것.

재생성이 필요하면:

```bash
cd /data/work/repo
python3 tools/sdcp/vasp_handoff_bundle.py \
  --runs /data/work/runs/sdcp_v4_sitescreen --freeze 0.85 \
  --from_basins db/properties/motif_probe_2026_08_29.json \
  --frags sdcp_neutral --roles calibration --both_seeds \
  --closure --d3_pairs --d3_seed_main_only \
  --out /data/work/runs/sdcp_motifprobe_v2
```
검산: `candidate_set = motif_probe (…)` · `emitted_basin_roles = ['motif_probe']` ·
`prospective/` 아래 자세 **2개**(probe0 `NiO_bridge__fib04__r180` · probe1 `Ni_top__fib04__r000`).

## 2. 할 일

1. 두 번들 제출 (KISTI 또는 외주). **동시 8잡 이상**이면 가장 긴 잡(19 h @256코어)이 바닥.
2. 회수되면 각 번들에서 분석기 실행 — 번들 안에 들어 있다 (`ANALYZER`). fail-closed 로
   막히면 **막힌 이유를 그대로 보고한다.** 우회하지 않는다.
3. 나온 값을 `db/properties/` 에 등재하고 마감 문서를 쓴다 (닫힘 조건 먼저, 그 다음 값).

## 3. 🔴 하면 안 되는 것

- **Stage B 를 시작하지 않는다.** 창 안 자세 전부(최대 277잡·4개월)는 이번 원고 경로가 아니다.
- **sealed audit 을 풀지 않는다.** `prospective_basins_2026_08_29.json` 의
  `sealed_audit`(sdcp b09·b62 · c10 b76·b21)는 calibration 이 창 W 를 확정한 **뒤에만** 연다.
- **사전등록 estimand 를 바꾸지 않는다.** `min−min` 에 표본밀도 편향이 있다는 것은
  이미 기록돼 있고(회신 Q2 Q8), 우리 손으로 통계를 고치면 결과 보고 고른 게 된다.
- **`motif_probe` 를 primary/calibration 에 합치지 않는다.** 별도 문장 하나에만 쓴다.
- **UMA 절대값·조각 간 비교 인용 금지.** 순위만 쓴다 (DFT 와 부호가 반대다).
- **legacy(wave1) 값과 신규 값을 섞지 않는다** — clean slab 이 다르다
  (`daf71160` vs `d5f18feb`).
- 커밋·푸시는 **`claude/friendly-meitner-lldvar` 에만.** PR 만들지 않는다.

## 4. 결과 셋 — 미리 적어둔 것 (서사를 고르지 않기 위해)

| DFT 결과 | 쓸 수 있는 문장 |
|---|---|
| 수소결합 자세가 백본 probe 보다 **낮다** | 술폰산 O–H 가 표면 산소와 수소결합해 결합을 지배한다 — Han 2025 과 **일치** |
| 차이가 **판정바닥 아래** | 두 접촉 모티프가 구별되지 않는다 — 기전 주장 없이 에너지만 |
| 백본 probe 가 **낮다** | 회신 T 의 기전 철회가 신규 자세에서도 유지 — 기전 주장 없음 |

조각 간 대비 문장은 회신 V 가 이미 승인한 틀을 쓴다:
> *"사전 명명한 endpoint 집합에서, all-F 고정기하 단일점과 명시된 분자·국소 자기상태
> gate 아래 관측한 조각 대비"*
> ⛔ 금지: `primary` · `low-energy` · `pose-insensitive` · `전역 최소` · `결합 선호를 종결했다`

## 5. 아직 안 한 것

- **회신 Q2 미발송** — `kb/reviews/codex_Q2_prompt_claim_and_normalization_2026_08_29.md`.
  정규화(분자당 vs 원자당 순위 역전)·표본밀도 비대칭·과잉방어를 묻는다. 보내면 좋다.
- `kb/questions/doped_declared_state_feasibility_2026_08_29.md` lint 6건 (구조 절 없음).
- 번들 `README_REQUEST.md` 가 `--from_basins` 구조를 설명 못 한다 (tier/pair 판 문구 그대로).
- wave1 정본값의 **k 메시 provenance 불명** — 납품 OUTCAR 가 repo·gabia 어디에도 없다.
  세 기록이 어긋난다(요청문 2×2×1 · 생성기 3×4×1 · 비용도구 시나리오 2×3×1).

## 6. 오늘 확정된 것 (되풀이 논증 금지)

- 동결 calibration 4자세 **전부** 산성 H 앵커. `H···O` 1.827/1.848/1.871/2.294 Å,
  분자내 `O–H` 1.020/1.018/1.015/0.993 Å, UMA E +0.0200/+0.0425/+0.1661/+0.1982 eV —
  **세 양이 같은 순서로 움직인다 (4/4).**
- 백본접촉 자세 88개, 최저 +0.2853 eV → **UMA 격차 0.265 eV** (수소결합 쪽이 낮다).
  ⚠ `omat` 에 분산이 없어 백본을 과소평가하므로 이 격차는 **상한**이다.
- 백본 5위 +0.3053 = wave1 champion 의 UMA 값. legacy 자세가 백본이었던 이유는
  rigid 스크린이 gap 2.4 Å 고정이라 1.83 Å 수소결합을 **만들 수 없었기** 때문이다.
- ⛔ 철회됨: *"rigid 101/322 · relax 88/109 이므로 기전이 죽었다"* — 그 순위는
  `sulfonate_down` **태그** 자세의 것이고, 실제 최저 자세는 `O_top` 태그를 달고
  술포네이트가 닿아 있다. 태그가 나쁜 대리변수였다.
- legacy 4자세에 대한 철회는 **유효**하다 (산성 H 7.08–7.17 Å 재측정 확인).
