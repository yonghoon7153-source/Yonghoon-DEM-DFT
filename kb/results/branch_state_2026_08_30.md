---
title: "브랜치 현황 지도 2026-08-30 — 지금 살아 있는 것과 죽어 있는 것"
date: 2026-08-30
updated: 2026-08-30
tags: [handoff, branch, status, sdcp, li3nd, ionic]
status: superseded — kb/results/branch_state_2026_08_31.md
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-30
verifiedBy: "git log · open_items · db/properties 실물 · gabia 화면·pgrep·nvidia-smi 실측"
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

# 브랜치 지도 (2026-08-30)

> ⛔ **대체됨 → `kb/results/branch_state_2026_08_31.md`** (2026-08-31 전수 조사).
> 이 문서의 §4 는 SDCP 를 "Stage A v9" 로 적는데, 그 뒤 캠페인이 **C-12 로 개명되고
> v18** 까지 갔다. §1·§2 의 gabia 실측(GPU 점유·li3nd 체인 사망)은 그 시점 기록으로 유효하다.

원래 세션이 토큰으로 멈춰 보조 세션이 이어받은 상태. 이 문서는 **SDCP Stage A
하나만 보던 시야를 브랜치 전체로 넓힌 결과**다. 인계 문서
(`handoff_2026_08_29_stage_a.md`)는 Stage A 만 다룬다 — 이 파일이 그 바깥이다.

## 0. 한 줄

**GPU 는 Li₃Nd P0-2 control 이 쓰고 있고, li3nd 선행검사는 이틀 전에 죽었는데
아무도 몰랐다.** SDCP Stage A 는 번들 v9 까지 가서 리뷰 회신 대기다.

## 1. 지금 서버에서 실제로 도는 것 (gabia, 실측)

| | 실측 |
|---|---|
| GPU | pw.x pid 4053765 · **37,736 MiB** (49,140 중) |
| 그 pw.x 가 뭔가 | **Li₃Nd P0-2 control** — `li3nd_mp-976264_p333_r0..r3` rattle 이완. r0 ✓(bfgs=0 · Fmax 1.6e-5), r1 진행(bfgs=13), r2·r3 대기 |
| ORCA | 별도 워처, 이 repo 밖(데스크탑 WSL). Stage A n=6 `gs0` ✓ cyc=65 · RMSgrad 9.85e-6 |

⚠ **화면의 "van Hove 쓸이" 패널과 헷갈리지 말 것.** GPU 를 잡은 건 van Hove 가
아니라 rattle control 이다. van Hove(T12)는 08-28 에 끝났다(§3).

🔴 `li3nd_..._p333_r*` 이 **⏭-4 (Li₃Nd P0-2 control)** 다. open_items 는
2026-08-29 시점에 "한 번도 착수된 적이 없다" 로 적혀 있는데 **그 뒤 착수됐다** —
장부가 아직 그걸 모른다. 회신 I 가 "3주 재개보다 먼저" 라 한 그 한 수다.

## 2. 🔴 죽어 있는데 화면이 감춘 것

**li3nd 선행검사 체인(리뷰 J ②~⑤)이 08-28 02:20 에 죽었다.**
`pgrep -af run_prereq_chain` = 빈 출력. 로그도 그 시각이 마지막.
그런데 화면은 이틀 내내 `🔄 진행 중` 이었다.

원인이 코드에 있었다 — `alive()` 가 문자열 `"-"` 를 냈고 파이썬에서 `"-"` 는 참이라
이 절은 **구조적으로 "안 돌고 있다" 를 낼 수 없었다**. `elif not run` 가지(완주
판정·재기동 안내)는 죽은 코드였다. 2026-08-30 수정(`Alive.__bool__`).

**재기동이 필요하다** — 다만 GPU 여유가 20,000 MiB 이상이어야 시작한다
(리뷰 J5: UMA/GPU 작업과 같이 돌리면 실패 원인이 섞인다). 지금은 rattle control 이
37.7 GB 를 쓰므로 그게 끝난 뒤다:

```
nohup bash tools/sei/run_prereq_chain.sh --wait > /data/work/runs/chain3.log 2>&1 &
```

## 3. 끝난 것 (감시 대상 아님)

| | 근거 |
|---|---|
| van Hove T12 | `vanhove_sweep_2026_08_28.json` · `vanhove_dr_sweep_2026_08_28.json` (72 실행/70 유효, 판정·철회까지) |
| LPSOCl ELF | `lpsocl_elf_*.json/csv` (2026-07-29) |
| LPSOCl AE Bader | `lpsocl_bader_ae.json` (2026-07-30, SCF 19회 — 가짜 수렴 아님 기록) |
| ④ 후속 체인 | 08-03 이후 무변화. 설계상 "손으로 착수" |

⇒ watch_all.py 에서 van Hove·④ 패널을 제거했다(2026-08-30). ELF·Bader 는 `done`
파일로 자동 접히므로 남겼다.

## 4. SDCP Stage A (인계받은 본류)

발송본 **`sdcp_stageA_v9.zip`** — repo `runs/sdcp_stageA_2026_08_29/` 에 zip·
`ATTESTATION_v9.json`·`REQUEST.md` 동봉.
리뷰 X → Z → AA 세 라운드 NO-GO 를 거쳐 v2 → v9. 회신 AB 프롬프트 발송 대기
(`kb/reviews/codex_AB_prompt_stageA_v9_regate_2026_08_29.md`).

닫힘 조건은 **DFT 0잡 시점에 등록**됐고 문턱은 그대로다
(`db/properties/sdcp_stageA_closure_conditions_2026_08_29.json`).

⚠ 갈림길: 회신 AB Q6 — C1 의 주장 강도를 "국소 calibration 일관성" 으로 내린 결과
**이 40잡이 무엇을 정당화하나**가 다시 열렸다. 리뷰어가 "층화 holdout 으로 재설계"
라고 하면 v9 는 던지지 않는다.

## 5. 장부(open_items)의 즉시 대기열 — 요약

| | 무엇 | 상태 |
|---|---|---|
| ⏭-0 | SDCP doped 재개 | 회신 R4 **조건부 GO — 데스크탑 ORCA 8잡만**. Stage 0·B·hybrid 전부 NO-GO. 지금 도는 ORCA 가 이것 |
| ⏭-1 | T13 MSD 길이 | ✅ 판정 완료 (200 ps 타당) |
| ⏭-2 | 39설계 D_rel | 설계 확정, **착수 전 준비 2건**(39설계 구조 빌더·캠페인 런처가 없다). "GPU 비면 바로 던진다" 가 안 된다 |
| ⏭-3 | 사전등록 채점 | 기준 동결 — 측정 후 고치지 말 것 |
| ⏭-4 | Li₃Nd P0-2 control | **지금 도는 중** (장부 미갱신) |
| ⏭-5 | 곁가지 | ESW 환원한계 규약 · 웹앱 pull |

## 6. 이 지도를 만들며 고친 것

- `alive()` 진리값 버그 (§2) — 이틀치 사망을 감췄다
- prereq 패널에 로그 나이 + **GPU 대기/정지/못잼 3분기** 진단 추가
- van Hove·④ 패널 제거 (74줄)

## 7. ⚠ 내가 틀렸던 것

첫 판독에서 **"li3nd 체인은 GPU 대기 중이니 죽일 필요 없다"** 고 했다. 틀렸다 —
죽어 있었다. 화면의 `🔄 진행 중` 을 믿고 낸 판단이고, 그 화면이 §2 의 버그로
거짓을 찍고 있었다. `pgrep` 한 줄이 그걸 뒤집었다.

교훈: **워처 출력은 근거가 아니라 주장이다.** 판정에 쓰기 전에 실물(pgrep·mtime·
nvidia-smi)로 받쳐야 한다.
