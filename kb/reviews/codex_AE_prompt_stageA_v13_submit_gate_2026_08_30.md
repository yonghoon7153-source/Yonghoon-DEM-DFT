---
title: "회신 AE — 제출 게이트: sdcp_stageA_v13 + holdout_v4 (42잡) GO/NO-GO"
date: 2026-08-30
updated: 2026-08-30
tags: [review, codex, sdcp, stage-a, release-gate, vasp, estimand]
status: 발송전
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

# 회신 AE — 이 두 zip 을 던져도 되는가

> **첨부: `sdcp_stageA_v13.zip` · `sdcp_stageA_holdout_v4.zip`.**
> 설명이 아니라 **실물**로 판정해 달라 — 지난 세 라운드에서 문서는 통과하고
> 산출물이 달랐던 것이 반복된 실패 원인이었다.

**묻는 것은 하나다: 아래 두 번들을 외주에 제출해도 되는가 (GO / NO-GO).**

## 0. 번들 정체성 (실측, 2026-08-30 07:19 UTC)

**이 두 파일을 직접 열어서 판정해 달라.** 해시는 gabia 생성기 보고와 제3자 재계산이 일치한다.

| | 잡 | bytes | ZIP sha256 | MANIFEST sha256 |
|---|---:|---:|---|---|
| `sdcp_stageA_v13.zip` | **24** | 357,686 | `3184de59706eddbb9d02a1143dae3df6e0912c81dcce931caf3413637bcc3147` | `c5517f9e00604498ec5cb6586202ef3b9c4abad82b41a8a08c8b9295cd8be4b8` |
| `sdcp_stageA_holdout_v4.zip` | **18** | 311,918 | `892dc8699d9eb82540ace4535f2d61b1d7d3bc8ffc1d7141514aa467a19c5b74` | `3daf5410c05bc5083af10233b9812a9bf52cb504f6e09af4a33c9da4da8f2e0b` |
| | **42** | | | |

두 MANIFEST 가 **자기 `argv` 를 적는다** (AB Q5 재현성 지적):

```
v13        : --runs …/sdcp_v4_sitescreen --freeze 0.85
             --from_basins db/properties/prospective_basins_2026_08_29.json
             --frags sdcp_neutral ptfe_c10 --roles calibration --both_seeds
             --closure --free_spin_refs --refs --cores 256 --concurrency 8
holdout_v4 : (같은 --runs/--freeze) --from_basins db/properties/prospective_holdout_2026_08_30.json
             --frags sdcp_neutral ptfe_c10 --roles holdout --closure --cores 256 --concurrency 8
```

**독립 검증 실적** (두 번들 각각, 제3자 기계에서 zip 을 풀어 실행):

```
v13        : 잡 24 (planned 24 + 쌍둥이 0) · 배포파일 151 · 해시확인 151
             candidate_set = calibration_pilot (frozen 94675e66e02c855a) · emitted_roles ['calibration']
             ✓ 입력 preflight — 결과 없이도 걸리는 게이트 0건 (job.json 24개 검사)
holdout_v4 : 잡 18 (planned 18 + 쌍둥이 0) · 배포파일 113 · 해시확인 113
             candidate_set = holdout_stratified (frozen 3e3ce4820c4df3ec) · emitted_roles ['holdout']
             ✓ 입력 preflight — 결과 없이도 걸리는 게이트 0건 (job.json 18개 검사)
공통       : clean_slab d5f18feb15701f3fc932a1c8f64a09ed48c39ca270d8d8a8f5339658b6c43676
             D3-off 쌍둥이 0 · sealed_audit 미개봉 · 둘 다 "✅ 제출 가능"
```

⚠ **비용 정정 (당신의 14.7일 지적을 실제 결함으로 확인했다).** README·SUBMIT_CONTRACT·Slurm
예시가 `--cores` 를 쓰는데 **시간 추정은 추정기 기준선(48코어) 값 그대로였다** — `--cores 256`
을 줘도 번들이 48코어 시간을 "256코어 기준" 이라고 적었다. 당신이 14.7일로 읽은 이유가
그것이다. `par_speedup` 으로 실제로 나누게 고쳤고, README 의 하드코딩 `longest = 56` 도
제거했다 (그러려면 비용 동결이 README 보다 **먼저** 와야 해서 순서도 바꿨다).

동결된 현재 값 (256 코어/잡 · 속도향상 4.91):

| | 가장 긴 잡 | 동시 8 |
|---|---:|---:|
| v13 | **44.8 h** (`refs/clean_slab__afm2424_pm1`, static→dense 사슬 · 42잡 중 유일한 dense) | 2.37 일 |
| holdout_v4 | 19.2 h | 2.21 일 |

두 번들을 한 큐(동시 8)에 넣으면 **약 4.6일**로 본다 (작업량 합 ÷ 8, 하한 44.8 h).
⚠ 44.8 h 잡이 있으므로 **큐 벽시간 제한이 48 h 미만이면 그 잡이 죽는다.**

## 1. ★ 이번 판의 핵심 변경 — C5 `ΔΔE_obs` (여기를 제일 세게 봐 달라)

당신은 회신 AB 에서 *"Stage A 는 calibration tranche 이고 Figure 2e 는 Stage B 뒤에야 가능하다"*
고 했고, 우리 마감조건도 같은 것을 등록해 두었다. 그 금지의 **근거**는 §9 가 직접 적는다:

> "이 tranche 는 (B)·W 를 정하려고 돈 것이고 **audit pose 가 없다**"

즉 반대 이유는 **"min 이 UMA 선택기의 산물일 수 있다"** 이다. 그 금지는 08-29 에 쓰였고,
**08-30 에 층화 홀드아웃 16잡이 추가됐다** (당신의 AB Q6 권고). 홀드아웃은 UMA 점수
**사분위 전 구간**에 걸쳐 조각당 8자세를 더 재므로 **정확히 그 반대 이유를 시험한다**.

그래서 옛 금지를 푸는 대신 **더 약한 양을 따로 정의**했다:

```
ΔΔE_obs = min_{p∈S} A(SDCP,p) − min_{q∈S} A(c10,q)      [pm1 · D3-on]
A(f,p)  = E_complex(f,p) − E_mol(f, box24)
S       = 조각당 **선언된 12자세** = calibration 4 (frozen 20fdde06…) + holdout 8 (frozen 3e3ce482…)
```

**게이트 (결과 보기 전 고정, 하나라도 새면 값 없음)**
① 조각당 12자세 완비 ② 12자세 상호 `same_basin`(크기 포함) ③ **H1** — 홀드아웃 최저가
calibration 최저를 **30 meV 이상 밑돌지 않는다** ④ 두 조각 기체 기준 존재

**H1 실패는 "더 낮은 자세를 찾았다" 로 흡수하지 않는다 — 재개 사유다.**

**유지되는 것**: primary `ΔΔE_lowE` 의 Stage B 의존성 · "어느 조각이 더 강하게 붙는다" 의
**종결형** 금지 · `sealed_audit` 봉인. C5 는 셋 중 어느 것도 건드리지 않는다.
거버넌스: `D-2026-08-30-sdcp-neutral-ptfe-ddE-obs` (**proposed** — 사람이 ratify 해야 active).

### Q1 [최우선] — C5 가 정당한가, 아니면 금지를 우회하는 이름 바꾸기인가

우리 주장: 반대의 **근거**(선택기 산물 가능성)를 실측으로 시험하게 됐으므로 그 시험을
통과할 때에 한해 **표본 조건부** 양을 인용할 수 있다. 이름·서술·게이트를 모두 갈라 두었다.

**반대로 볼 여지도 있다** — 홀드아웃 8자세는 여전히 **UMA 가 만든 후보풀 안**이다.
UMA 가 계통적으로 틀렸다면(후보풀 자체에 진짜 최저가 없다면) 홀드아웃도 그것을 못 잡는다.
그러면 C5 는 "선택기가 자기 자신을 검증한다" 가 된다.

**이 반론이 치명적인가?** 치명적이면 NO-GO 로 판정하고, 아니라면 허용 서술을 어디까지로
좁혀야 하는지 문구로 달라. (우리 현재 문구: *"조사한 12자세에서 … 낮았다. 층화 홀드아웃
8자세 중 어느 것도 사전등록 4자세의 최저를 30 meV 이상 밑돌지 않았다."*)

### Q2 — C5 게이트가 충분한가
특히 (a) **H1 문턱 30 meV** — 사전등록 자리선호 판정바닥을 승계한 값이다. 맞나?
(b) 12자세 완비 요구가 옳나, 아니면 결측 시 축소 표본으로라도 내야 하나?
(c) `same_basin` 을 12자세 **상호**로 요구하고 clean slab 일치는 안 거는 것 — 당신의 AB
P0-4 후단(“S_f 에서 슬랩·분자가 소거된다”)을 A(f,p) 에도 그대로 적용했다. 맞나?

## 2. AB 의 P0 8건 — 처리 요약

| P0 | 처리 |
|---|---|
| **1** | `role` 이 분석역할(calibration)/등록역할(Li·Ni) 두 뜻이었다 → `registry_role` 분리, basin 자세는 `None` **선언**. 기체에 `mol_graph_canonical` 기록. ★ **배포 전 입력 preflight** 를 `verify_bundle` 에 추가 — 실물 v9 에 걸어 **36건 재현**(당신이 센 수와 일치), v13/holdout_v4 에서 **0건** |
| **2** | 소멸 — D3-off 제거 (Q6 권고 채택) |
| **3** | **당신이 옳았다.** 봉인값 0.90 eV 의 정본 필드명이 `오프셋_UMA_빼기_DFT_eV` (SDCP 1.0728/1.0667 · c10 0.1855/0.1484 ⇒ +0.9028). D3 는 additive 라 `offset ≈ −δ` ⇒ 비교량을 `predicted_offset_gap = −D` 로 이름부터 고쳤다. ⚠ selftest 두 건이 **같은 틀린 규약을 인코딩**해 코드와 시험이 서로 동의하며 둘 다 틀렸다. 추가로 **조각내 일관성**을 필수화 (δ range ≤ 관측 오프셋 상수성 × 5) |
| **4** | `basin_distance()` 가 selftest 밖에서 **한 번도 호출되지 않았다** → `same_basin()` 신설, 해시가 같아도 상세 지문으로 재확인, **상세 없으면 통과 아님**. C1 은 네 자세 **상호** 동질성으로 (슬랩 일치는 절대 E_ads 쪽) |
| **5** | 키 넷이 `AUDIT_KEYS_RUNTIME` 에 없어 실제로 안 읽혔다 → 추가. **그러자 잠복 버그가 드러났다** — `str(None)=="NONE"` 이라 미출력이 곧 "스핀 제약 있음" 이 되어 전 잡 `BASIN_UNRESOLVED`. VASP 는 기본값이면 안 찍으므로 None=기본값(꺼짐). 시험도 production 과 **같은 식**으로 |
| **6** | 실측 일치 (24=24, 18=18) |
| **7** | C2 완비성 강제 (동결 manifest 기대수 × 두 seed 모두). "seed-insensitive" → *"시험한 N자세 안에서 seed×pose interaction range 가 작았다"* |
| **8** | 조립기: `POTCAR.tmp` → 검증 → 통과 시에만 원자적 `mv`, 실패 시 trap 이 전부 삭제, `set -euo pipefail`, **면제 폐지**. 러너: provenance 존재·비면제·**현재 POTCAR sha 일치** 요구 |

selftest **355건** · convention_check 0 위반 · e2e 12/12.

### Q3 — 이 여덟이 실제로 닫혔나
문서가 아니라 **코드와 산출물**로. 특히 P0-1: preflight 가 v9 에서 36건·신규에서 0건인 것이
*"OUTCAR 가 와도 안 막힌다"* 를 보증하나?

## 3. 나머지 질문

### Q4 — 두 번들로 나눈 것
홀드아웃에는 **기체 기준이 없다** (`--refs` 미지정). A(f,p) 계산에 v11 의 `E_mol` 을 쓴다 —
같은 기준을 두 번 돌리지 않게 하려는 의도다. 대신 `controls/clean_slab` 2잡이 홀드아웃에
딸려 온다(자기 대조군 — 빼면 basin 판정이 전 잡에서 '보류' 로 조용히 통과한다).
**이 분리가 건전한가, 아니면 provenance 위험인가?** 합쳐야 한다면 그 근거를 달라.

### Q5 — 당신의 release gate 6조건
① ZIP·MANIFEST hash — §0 확정 ② production `main()` 합성 완주 — e2e 12/12
③ required = 디스크 = census — 실측 일치 ④ C1/C2/C3/C5 cohort 수 — 전부 manifest 기대수 강제
⑤ **승인 PP 로 site dry-run — 우리가 못 한다** (PP 를 못 가진다) ⑥ MANIFEST 가 argv 기록
**⑤가 GO 를 막나? 대체 조건이 있나?**

### Q6 — 여전히 못 본 것
AB 는 세 개를 새로 잡았다. 특히 P0-5 처럼 **"검사가 있는데 실제로는 안 도는"** 부류를
찾아 달라 — 이 캠페인이 반복해 밟는 자리다.

## 4. 형식

Q1–Q6 각각 **P0/P1/P2 + 한 줄 판정 + 근거**. 마지막에 **GO / NO-GO**.
GO 면 이 두 zip 을 그대로 제출한다 (256 코어/잡 · 동시 8 → 3.8일).
NO-GO 면 해제조건을 번호로.
