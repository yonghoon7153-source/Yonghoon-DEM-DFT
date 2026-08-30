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

> ⚠ **이 문서는 Stage A 만 다룬다.** 브랜치 전체(지금 도는 것·죽은 것·장부)는
> `kb/results/branch_state_2026_08_30.md` 를 볼 것 — 2026-08-30 에 보조 세션이
> 만든 지도다. Stage A 번들도 그 사이 **v2 → v9** 로 갔다 (리뷰 X·Z·AA 3연속 NO-GO).

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
⚠ **폐기본 — 던지지 말 것**
  · `sdcp_motifprobe_v1` (7잡·1자세) — probe 가 하나뿐이라 앵커 원소 대비가 안 된다
  · `sdcp_stageA_v3` (34잡) — c10 을 4→2자세로 줄여 본 판. **쓰지 않는다**:
    아끼는 시간이 2.99→2.37일 = **약 15시간**뿐인데, 그 대가로 c10 의 C1
    (UMA–DFT 오프셋 상수성)이 n=2 로 떨어져 **평가 불가**가 된다. C1 이
    조각당 4자세를 요구하는 조건이라 c10 쪽 선택기 검증이 통째로 빠진다.
    1저자 판단(2026-08-29): 반나절 아끼자고 마감조건 하나를 버리지 않는다.

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

## 1.5 보조 세션 진행 (2026-08-29 저녁, 이 절만 추가)

**경로 확정: 외주** (wave1 과 같은 곳). KISTI 는 배제 — `kb/methodology/kisti_setup.md`
에 VASP 모듈이 없고(QE-GPU/A100), 배치 예시가 `-t 24:00:00` 인데 가장 긴 잡이 19 h,
SUBMIT_CONTRACT 는 120 h 를 권한다.

| 한 것 | 어디 |
|---|---|
| 제출 전 무결성 검사 도구 | `vasp_handoff_bundle.py --verify_bundle <dir> [--expect_jobs N]` |
| 두 번들 검증 **통과** (rc=0) | stageA_v2 40잡 · motifprobe_v2 10잡, 배포파일 245·65 전건 해시 일치 |
| 외주 요청문 | `runs/sdcp_stageA_2026_08_29/REQUEST.md` (봉인 zip 은 안 건드리고 바깥에서 정정) |
| **닫힘 조건 (결과 전 등록)** | `db/properties/sdcp_stageA_closure_conditions_2026_08_29.json` |
| 회신 Q2 발송본 | `kb/reviews/codex_Q2_prompt_claim_and_normalization_2026_08_29.md` |
| P0-5 재현 시험 도구 | `site_screen.py score --clean_probe 2` |

**발송본 = `sdcp_stageA_v5.zip` (40잡) 하나뿐이다.**
zip `8c658763…56ba713c` · MANIFEST `0860ae43…a876670e` ·
clean_slab `d5f18feb…c43676` · 후보 frozen `94675e66e02c855a`.

⚠ **v1~v4 는 전부 폐기본이다** — v2 문서가 이완판(반송계약 오류) · v3 후보집합이
다름(c10 2자세, 그 후보 파일은 repo 에 없다) · v4 MANIFEST 실행횟수 24(문서는 40).
`sdcp_motifprobe_v2` 는 **Stage B 동결 뒤로 미뤘다** (회신 Z P0-5).

### 🔴 이 셋은 이 절을 읽고 알아야 한다

1. **primary X 는 이 캠페인에서 안 나온다.** 두 번들의 `candidate_set` 이
   `calibration_pilot` · `motif_probe` 이고, 분석기 `_closure_estimand()` 가 그 이름에서
   `CALIBRATION_ONLY_TRANCHE` 를 걸어 `NO_VALUE` 를 낸다. **설계된 fail-closed 다.**
   3일 뒤 그게 나오면 정상 — 우회하지 않는다. 대신 닫는 것은 C1~C4(닫힘 조건 파일).
2. **P0-5(clean slab provenance)가 아직 안 닫혔다.** 회신 X 가 "실행 전 P0" 로 격상한
   건인데 해소 기록이 없다. 조각 간 대비는 두 조각이 같은 슬랩이라 성립하지만(회신 X
   Q2 조건부 승인) "재현 가능한 동결 기하" 라 부를 근거는 없다. `--clean_probe 2` 를
   외주와 **병행**해 돌린다 (gabia GPU 는 비어 있다 — VASP 는 외주가 돈다).
3. **`/data/work/runs/` 에 zip 이 9개**고 `sdcp_stageA_v1.zip`(380,307 B)이
   `v2`(380,929 B)와 622 바이트 차이다. 목록에서 골라 보내면 사고다 —
   `/data/work/outbox_2026_08_29/` 에 둘만 격리해 발송한다.

### 부수적으로 고친 것

- `--verify_bundle` 첫 판이 **멀쩡한 번들을 차단**했다 ("n_jobs 40 vs planned 24").
  생성기가 D3-off 쌍둥이를 `plan()` 없이 만들어 `n_jobs` 에만 센다 — 40 = 24 + 16 이
  정상이다. 잡 목록의 정본을 `planned` 에서 **디스크의 run_job.sh 폴더**로 바꿨고,
  그 구조를 selftest 양성 케이스에 심었다.
- 번들 `SUBMIT_CONTRACT.md` 가 "잡 40 / 총 VASP 실행 24" 로 자기모순이다(같은 쌍둥이
  누락). 외주가 24회로 견적을 잡으면 40 % 를 덜 잡는다 — 요청문에서 정정했다.
- `kb` lint **0 errors** (§5 의 doped 카드 6건 해소 — 구조 절만 붙였고 내용 불변).

---

## 2. 할 일

1. 두 번들 제출 (**외주 — 확정**). **동시 8잡 이상**이면 가장 긴 잡(19 h @256코어)이 바닥.
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

- **회신 Q2 — 발송본 완료, 아직 미발송** (2026-08-29 저녁 갱신). Q3(기전 부활 방어) ·
  Q7(b)(Stage A 단독이 정당한 정지점인가) · Q8(b)(동수 N=4 calibration) 를 현재
  사실로 다시 썼다. **붙여넣을 프롬프트 절을 그대로 보내면 된다.**
- ~~`kb/questions/doped_declared_state_feasibility_2026_08_29.md` lint 6건~~ ✅ 해소 (2026-08-29 저녁).
- ~~번들 `README_REQUEST.md` 가 `--from_basins` 구조를 설명 못 한다~~ ✅ 우회 (2026-08-29 저녁) —
  봉인 zip 을 고치면 `files_sha256` 이 전부 깨지므로 **바깥 요청문**으로 정정했다
  (`runs/sdcp_stageA_2026_08_29/REQUEST.md` §0).
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
