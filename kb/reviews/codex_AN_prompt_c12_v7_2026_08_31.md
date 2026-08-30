---
title: "회신 AN — C-12 v7 재심: estimand 를 고정기하 단일점으로 되돌렸다"
date: 2026-08-31
kind: review_request
status: sent
tags: [sdcp, vasp, incar, c12, single-point, estimand, review/codex]
---

# 회신 AN — AM 해제조건을 받아 v7 을 다시 만들었다

**아직 안 보냈다.** 회신 AM(NO-GO, P0 여섯 · 해제조건 아홉)을 받아 고쳤고,
그 과정에서 **AM 이 못 본 것 하나를 우리가 더 찾았다**(§2). 재심 부탁드린다.

| | |
|---|---|
| 번들 | `sdcp_c12_v7.zip` · **12잡 · VASP 실행 14회** · 배포파일 82 |
| ZIP sha256 | `3af4c6beb5ba30295b0a49cd29db0d01e23d387d75ff8cb8a1349971fb830543` (260,246 B) |
| MANIFEST | `d47626dab219a0853a0e2d2fad316c3a58c385c7e0d050512b000d13246e2794` |
| 생성 | 2026-08-30T16:20:05Z · `candidate_set c12 (frozen cc87f6eeae5f9c3a)` |
| 검증 | `verify_zip(expect_jobs=12)` **rc=0** |

---

## 1. ⭐ 가장 큰 변경 — **estimand 를 고정기하 단일점으로 되돌렸다**

AM P0-1 이 *"선언(고정기하 단일점)과 실제(pre→relax→static, NSW=200)가 다르다"* 고 했고,
둘 중 하나를 확정하라고 했다. **우리는 "고정 MLIP 기하 단일점" 으로 확정했다.**

이유는 AM 이 몰랐던 사실이다 — **2026-08-29 stageA wave 가 이미 그 규약이었다**
(`runs/sdcp_stageA_2026_08_29/REQUEST.md` §0: *"이 묶음은 단일점만 돕니다 · 상 static
하나뿐 · 기하 고정"*). C-12 가 `pre→relax→static` 으로 **드리프트한 것**이었고,
그대로 두면 원고 안에서 이전 wave 값과 규약이 갈린다.

**부수효과 — AM Q1 이 자동으로 해소된다.** 이완이 없으므로 c1·c2 는 **같은 Cartesian
좌표에 c 만 +4 Å** 다 (AM 이 실측한 7.1e-15 Å 그대로). AM 이 처방한 5단계
(c1 확정 → 좌표 유지 → DIPOL 재계산 → NSW=0 → 계보 검증) 중 1–4 가 구조적으로 만족된다.

⇒ 실행 14회 (34회 → 14회). 상 분포 `pre 0 · relax 2 · static 12`.
relax 2 는 **기체 기준뿐**이다 (분자는 상자 안에서 이완해야 한다).

## 2. 🔴 우리가 더 찾은 것 — `LREAL` 이 한 양 안에서 갈려 있었다

v5(단일점 첫 판)를 실물 대조하다 찾았다:

| | LREAL |
|---|---|
| 슬랩 static | **`Auto`** |
| 기체 기준 static | **`.FALSE.`** |

⇒ `E_ads = E_복합체(Auto) − E_기체(.FALSE.)` — **한 양 안에서 두 해밀토니안이 섞였다.**

회신 U P0-5 가 **이미 이 결함을 판정했었다**: *"종전 `--single_point` 는 고정기하이면서도
`LREAL = Auto` 였다. 조각 간 대비에서 LREAL 오차는 서로 다른 흡착종이라 소거되지 않는다."*
그런데 그때 고친 것은 `--closure` 가지뿐이었고 `--single_point` 는 그대로였다.
C-12 가 쓰는 것이 후자다.

**더 나쁜 것**: 그 사실을 selftest 가 **양성으로 못박고** 있었다 —
*"(음성 대조) --single_point 만으로는 LREAL=Auto 가 남는다 — closure 가 그것을 고친다"*.
판정의 적용 범위를 좁게 읽어 시험에 새겨 넣은 것이다.

v7 실측: `LREAL = .FALSE.` **12개(static 전부)** · `Auto` 2개(**기체 relax 뿐**).

**★ Q1.** 기체 relax 만 `Auto` 인 것은 AM ①(*"Auto-relaxed geometry 에서의 `.FALSE.` energy"*
로 제한)의 범위로 보면 되는가? 슬랩은 애초에 이완이 없으므로 그 문제가 없고, 기체만
"Auto 로 이완한 기하에서 `.FALSE.` 로 평가" 가 된다.

## 3. AM 해제조건 이행표

| | 조건 | 상태 |
|---|---|---|
| 1 | estimand 확정 + manifest·phase graph·문구 일치 | ✅ 고정 MLIP 기하 단일점 (`db/properties/sdcp_c12_protocol_2026_08_30.json`) |
| 2 | D 의 정확한 job key 사전 고정 | ✅ **pm1 primary 네 개로 못박음** (§4) |
| 3 | c1→c2 기하 계보 · Cartesian 동일성 | ✅ 이완 제거로 **구조적으로** 만족 · ⚠ 명시적 gate 는 미구현 |
| 4 | vacconv metadata ↔ cohort 정합 | ✅ `job.json` 의 `vacconv` 필드로 고른다 (종전엔 `kind` 로 골라 c1 ambiguous·c2 0개였다) |
| 5 | minimal-reference 분석 경로 · stage 종료코드 | 🔄 **절반** — Δ_vac 의 기체 소거는 구현 · stage-scoped exit 미구현 |
| 6 | singlet gas + canary · complex `NUPDOWN=-1` exact audit | 🔄 **절반** — 슬랩 10잡에 `NUPDOWN=-1` **명시** · canary 와 exact echo gate 미구현 |
| 7 | `ICHARG=1` phase 에 CHGCAR-read hard gate | 🔄 미구현 (슬랩은 `ICHARG=2` 라 해당 없음 · **기체 static 만** `ICHARG=1`) |
| 8 | 실제 번들을 e2e fixture 로 | 🔄 **절반** — 픽스처를 실물 규약(`vacconv` 필드)에 맞췄다 (그전엔 옛 규약이라 c2 미인식을 못 잡았다) |
| 9 | POTCAR pin | ⚠ **경고로 강등** — 사유는 §5 |

**5·7·8 은 분석기 쪽이라 발송을 막지 않는다** (결과 회수 시점에 필요). 회수 전까지 닫는다.
**⇒ 발송을 막는 것이 남아 있는지가 이번 질문이다.**

## 4. D 의 job key (사전 고정)

```
D = [E_C − E_G]^SDCP − [E_C − E_G]^PTFE

E_C^SDCP  prospective/sdcp_neutral__b00__afm2424_pm1
E_C^PTFE  prospective/ptfe_c10__b00__afm2424_pm1
E_G^SDCP  refs/mol__sdcp_neutral__box24
E_G^PTFE  refs/mol__ptfe_c10__box24
```

AM 지적대로 **"조각별 최솟값" 을 폐기했다** — 그러면 SDCP 와 PTFE 가 서로 다른 seed 에서
뽑힐 수 있어 "pm1 조건부 D" 와도 다른 양이 된다.
`net4` 4잡과 대안 자세(ptfe b52 `sensitivity` · sdcp b12 `stress_sensitivity`) 4잡은
**D 에 안 들어간다** — 자기 분기·자세 민감도 병기용이다.

**★ Q2.** `|D(pm1) − D(net4)|` 를 민감도로 병기하는 것이 맞는가, 아니면 그 차가 문턱을
넘으면 D 자체를 `unresolved` 로 두어야 하는가? 넘는다면 문턱은 무엇으로 정하는가?

## 5. 자기상태 정책 (AM Q2 = (c) 를 절반만 이행)

채택한 문구:
> 기체 기준은 중성 closed-shell singlet(`NUPDOWN=0`)로 정의하였다. 슬랩 복합체는
> `NUPDOWN=-1` 에서 사전 고정된 pm1/net4 초기자화로 시작한 unconstrained-spin SCF 이며,
> **자기 바닥상태가 아니라 seed-conditioned realized basin** 으로 보고한다.

v7 실측: 슬랩 10잡 `NUPDOWN = -1` **명시** (종전엔 줄이 아예 없어 VASP 기본값에 기댔고,
분석기는 "기대값 미등록" 으로만 남기고 차단하지 않았다) · 기체 4개 `NUPDOWN = 0`.

**미이행**: 비영 자화 static **canary**(조각당 1잡). 넣으면 14잡이 된다.

**★ Q3.** canary 를 이번 발송에 넣어야 하는가, 아니면 D 가 나온 뒤 필요할 때
따로 보내도 되는가? (두 조각 다 짝수전자 포화 중성계이고 `job.json` 도 `open_shell:false` 다.)

## 6. POTCAR pin — 차단에서 경고로 내렸다

`run_job.sh` 는 `POTCAR_PROVENANCE.json` 없이 **실행을 거부한다**(회신 AB P0-8).
조립기가 그 파일에 변형별 원본 SHA256·TITEL·조립본 SHA 를 적으므로, **계산을 돌리면
provenance 가 반송물에 자동 포함된다.**

⇒ pin 을 미리 받아 얻는 것은 *"우리가 먼저 선언한 기준과의 대조"* 이고, 없으면
*"실제로 쓴 것의 사후 기록"* 이다. 후자도 검증이며 **못 잡는 것은 '우리가 의도한 트리와
다른 트리를 썼다' 하나뿐**이다. 그 하나 때문에 발송을 막고 왕복을 요구하는 것은
비용이 안 맞는다고 판단해 **경고로 내렸다.** README 에도 *"따로 보내실 것 없음 · 트리를
바꾸실 때만 알려달라"* 로 적었다.

**★ Q4.** 이 판단이 맞는가? (같은 외주처가 2026-08-12 wave 를 돌렸고, 그 wave 의
provenance 는 우리 쪽에 **없다** — repo·gabia 어디에도.)

## 7. 우리가 답 없이는 안 하는 것

- 5·7·8 을 닫지 않은 채 **결과를 판정**하는 것 (발송은 별개)
- `net4` 나 대안 자세를 D 에 넣는 것
- 기하가 DFT 최소점이라고 적는 것 (**UMA 이완 기하**임을 반드시 병기)
- `Δ_vac` 문턱(5 meV)을 결과를 본 뒤 바꾸는 것

## 8. 첨부

`sdcp_c12_v7.zip` (위 해시). `unzip` 후 `*/static/INCAR` 로 직접 보실 수 있고,
`MANIFEST.json` 에 잡 목록·해시·생성 argv 가 있습니다. POTCAR 는 미포함(라이선스).
