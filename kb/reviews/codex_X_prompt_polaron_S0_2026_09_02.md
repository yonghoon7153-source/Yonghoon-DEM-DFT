---
title: "리뷰 요청 X — 폴라론 S0 (회신 W P0 8건 이행 · 사전등록 비준 완료)"
date: 2026-09-02
updated: 2026-09-02
tags: [review, codex, sdcp, polaron, orca, prompt]
status: 발송 대기
kind: review-request
system: sdcp
confidence: high
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 요청 X — 폴라론 S0

> 이전 회신: 회신 W (NO-GO · P0 8건 · P1 4건 · phase L 금지)
> **ORCA 는 여전히 한 잡도 돌리지 않았습니다.**

```
tools/sdcp/build_v7c_trimer.py                              ded52c96d75ff929029f149f3d8e6768cbd27f53bfcab4a7aa301e85eb6cc90a
db/properties/sdcp_polaron_pilot_prereg_S0_2026_08_31.json  3a562dda4a85e648517256d1169dace33d7d87e1bf805197873e61784026aaa9
db/structures/sdcp_orca_gs0/dp6_gs0_neutral_final.xyz       b49076980623185cdde983dba64acc11a73021293b0886e263aee618a8de5085
커밋                                                          592267297e7075943840d7e1b8daa8f129a01afc
원격                                                          있음
selftest                                                    245건 PASS   (회신 W 시점 225 · V 시점 212)
```

표는 `tools/review_manifest.py --require_pushed` 가 낸 것입니다 (커밋된 트리에서만
계산 · dirty 거부 · 원격 포함 확인).

## 0. 먼저 — 저희가 자체로 찾은 P0 하나를 보고합니다

P0-5 를 하다 처음으로 `bash -n` 을 러너에 걸었습니다.

**배포 중이던 `run_pilot.sh` 는 bash 로 파싱조차 되지 않았습니다.**

원인은 저희가 회신 V P1(“`grep -c … || echo 0` 의 `0\n0` false-green”)을 고치며 남긴
**주석**입니다. 파이썬 문자열 안에 `\n` 을 쓴 것이 실제 줄바꿈이 되어, 주석의 뒷부분이
주석이 아니라 **명령줄**이 됐습니다 — 열린 따옴표와 짝 없는 백틱이 남아 스크립트
전체가 EOF 까지 미완성 토큰 상태였습니다. `loccheck` 를 포함해 **어떤 단계도 실행되지
않는** 상태였습니다.

selftest 225 건은 그때도 전부 PASS 였습니다. **러너를 한 번도 돌리지 않았기 때문입니다.**

이 형태는 회신 AZ 가 C-12 에서 지적한 것과 같습니다(“정상 실행 경로를 selftest 가 한
번도 지나지 않았다”). 같은 결론에 두 번째로 도달했고, 이번엔 시험을 넣었습니다:

- `bash -n` 을 selftest 에 넣었습니다 (양성 1 + **음성 1**: 짝 없는 백틱을 주입하면
  이 시험이 실제로 잡는지 확인).
- 러너 안의 `PYL2` heredoc(파이썬 블록)을 selftest 가 **실제 서브프로세스로 실행**합니다.
  픽스처의 loccheck 증서 suffix 를 `.loc.gbw` 로 두어 **가정과 다른 경로**를 태웁니다.

## 1. P0 이행

### P0-4 — loccheck 증서가 L→L2 사슬을 증명하지 못했다

지적대로였습니다. 종전 `loccheck` 는 L 형만 돌리고, seed 의 원천인 L2 의
`%moinp` readback 은 **한 번도 시험하지 않았습니다.** 그리고 suffix 판정(`.loc` vs
`.loc.gbw`)은 옛 파일이 남아 있으면 그것을 집었습니다.

⇒ 세 가지를 바꿨습니다.

1. **fresh 디렉터리**(`rm -rf "$LC"`)에서 **L → L2 를 둘 다** 돌립니다. L2 는 방금 만든
   국재 파일을 `Guess MORead` / `GuessMode CMatrix` / `%moinp "w<suffix>"` / `NoIter`
   로 읽습니다. 파서 검증(`pil_parse_mopop`·`pil_parse_mos`)도 **L2 출력**으로 합니다.
2. 증서에 `l2_inp_sha256` · `l2_out_sha256` · `l2_moread_suffix` 를 남깁니다.
3. 증서 **판독**이 기록된 ORCA 를 **지금 다시 해시**합니다. 경로가 없으면 거부,
   SHA 가 다르면 거부 — 종전엔 기록을 읽기만 하고 재확인하지 않아 증서를 만든 뒤
   ORCA 를 바꿔도 통과했습니다.

음성 4건: ORCA 경로 소멸 · ORCA SHA 변경 · L2 해시 **키 없음** · L2 해시 **빈 값**
(뒤 둘은 서로 다른 분기라 하나만 시험하면 나머지가 열립니다).

### P0-5 — 계보 해시가 기록만 되고 소비되지 않았다

지적이 정확했습니다. manifest 는 잡마다 `inp_sha256`·`xyz_sha256`·`loc_sha256`/
`gbw_sha256` 를 **기록**했지만 러너가 실행 전에 **한 번도 대조하지 않았습니다.**
게다가 `run()` 은 `.out` 에 `ORCA TERMINATED NORMALLY` 만 있으면 건너뛰었습니다 —
입력을 고쳐도 **옛 결과를 그대로 판정에 썼습니다.**
(저희 `tools/sei/run_sei_dft.sh` 는 2026-08-12 에 정확히 이 사고를 겪고 지문 가드가
있습니다. 규약이 파일마다 갈려 있었습니다.)

⇒ 세 층으로 나눴습니다.

**① 공통 preflight** (`pil_lineage_check(d, stage)`) — 계산 단계(L·L2·probe·S·restart)
가 **돌기 전에** 그 phase 의 잡 전건을 봅니다:
`INP_MISSING` · `INP_CHANGED` · `INP_UNSEALED` · `XYZ_MISSING` · `XYZ_CHANGED` ·
`MOINP_MISSING` · `MOINP_ABSENT` · `ORBITALS_CHANGED` · `STALE_OUTPUT`.
하나라도 걸리면 **그 단계 전체를 돌리지 않습니다** (한 잡만 빼지 않습니다 — 무엇이
어긋났는지 사람이 봐야 하기 때문입니다).

**② 단계별 실행 receipt** (`RUN_RECEIPTS.jsonl`) — 잡마다 stage·job·tag·phase·
시작/종료 시각·rc·입력/xyz/`%moinp`/출력 SHA·정상종료 여부·ORCA 경로+SHA·builder SHA
를 **덧붙입니다**(덮어쓰지 않습니다 — 회신 AZ P1 에서 C-12 가 헤더로 덮어써 완료 상의
행이 사라진 전례가 있습니다).

**③ 분석기가 소비** — `pilot_analyze` 가 S·SR 잡마다
`RUN_RECEIPT_MISSING` / `RUN_RECEIPT_STALE` / `RUN_RECEIPT_NOT_TERMINATED` 를 게이트로
겁니다. 3층 재판정으로 **SR 잡이 basin 대표가 되는 경우**, SR 잡의 receipt 도 따로
봅니다(`SR_` 접두) — S 잡 것만 보면 대표가 무검증으로 들어옵니다.

**부수로 하나 더 나왔습니다.** L2 단계의 suffix 패치는 봉인된 입력의 `%moinp` 한 줄을
고치는데, **manifest 의 `inp_sha256` 은 갱신하지 않았습니다.** 계보 대조를 붙이자
이 단계가 스스로 만든 불일치로 전건이 막혔습니다(실측). 이제 고치면 봉인도 갱신하고,
생성 시점 값을 `inp_sha256_at_generate` 로 남깁니다. **다만 패치 이전에 나온 L2 출력은
`STALE_OUTPUT` 으로 남깁니다** — 봉인만 맞추고 옛 출력을 통과시키면 그게 더 나쁩니다.

음성 6건 + 양성 2건. 신설 시험은 전부 **되돌림 확인**을 거쳤습니다: 검사를 제거하면
해당 음성이 실제로 죽습니다(`rc=1`).

### P0-1 · P0-2 · P0-3 · P0-6 · P0-7 · P0-8

앞선 회신에서 이미 보고드린 대로입니다. 요약만 다시 적습니다.

- **P0-1** 자기 자신을 담는 커밋 SHA 는 파일에 넣을 수 없습니다(순환). 사전등록이
  봉인하는 것은 ⓐ 빌더 blob SHA ⓑ **빌더를 마지막으로 바꾼 커밋**
  (`builder_last_change_commit`) 둘입니다. 전체 커밋 결박은 파일 밖
  `tools/review_manifest.py` 가 집니다.
- **P0-2** 사전등록 필드를 **지우면** 검사가 건너뛰어지던 fail-open 을 닫았습니다
  (`_REQ_EV`·`_REQ_TG` 필수 스키마). 음성 6건.
- **P0-3** 비준·digest 결박을 생성·seeds·restart·analyze **네 진입점 모두**에서
  요구합니다.
- **P0-6** 정상종료 판정을 **판정에 쓰는 segment** 안에서 요구합니다(`_last_segment`).
- **P0-7** 저희 자신의 버그였습니다: `_frac = Σ|s| / t` 에서 `t = Σ|s|` 라 **언제나 1**
  이었습니다. 원자 인구에는 “분자 밖” 바구니가 없어 관측 불가능한 양이었으므로
  기준 자체를 **삭제**했습니다(`PIL_EPS1_MIN_ONMOL` 제거).
- **P0-8** `localized_no_rotation` control 을 넣었습니다. 절대 문턱만으로는
  0.80 → 0.70(**몫이 줄었는데**)도 통과합니다. 이제 무회전 기준 대비 `+0.05` 증가를
  요구합니다(`PIL_PROBE_GAIN_MIN`).

## 2. 비준 — 이번엔 했습니다

회신 V Q5-1 과 회신 W 가 요구한 **비용 발생 전 비준**입니다.

- `db/properties/sdcp_polaron_pilot_prereg_S0_2026_08_31.json` → **`ratified`**
  (1저자 · scientific_owner · 2026-09-02).
- `ratification.content_digest` = **`ratification` 을 뺀 문서 내용의 sha256**.
  비준을 받아 놓고 내용을 고치는 경로를 닫습니다 — 실제로 이 세션에서 P0-1/P0-3 을
  이행했을 때 게이트가 “승인 이후에 내용이 바뀌었다”고 잡아 `proposed` 로 되돌렸고,
  P0-4/P0-5 를 끝낸 지금 다시 비준했습니다.
- 실물 게이트(`_pil_check_prereg`)를 태워 통과를 확인했습니다.

`실행_전_봉인` 에 두 조건을 명시했습니다: ① loccheck 증서는 fresh 디렉터리에서
L→L2 를 둘 다 돌린 것이어야 하고 판독 시 ORCA 를 재해시한다 ② 계산 단계는 계보
대조를 통과해야 하고 판정은 receipt 있는 잡만 받는다.

## 3. 아직 **안** 한 것

1. **실물 ORCA 확인 0회.** `loccheck` 는 그것을 하려고 있는 것이지 한 것이 아닙니다.
   지금 상태에서 `bash run_pilot.sh loccheck` 가 저희가 처음 돌리는 ORCA 잡입니다.
2. **builder hash 단일 결박**(요청 W Q2) — 아직 generator/selector/analyzer 로 나누지
   않았습니다. 회신 W 의 답을 기다렸습니다.
3. **Q6-4 R0/R1 교차비교** — 안 돌렸습니다. 결과는 `R0-conditional` 로 제한돼 있습니다.
4. **probe(S0P) 잡에는 receipt 게이트를 걸지 않았습니다** — 계보 preflight 는 걸립니다.
   Q3 에서 여쭙니다.

## 4. 여쭙는 것

**Q1.** P0-5 의 preflight 를 **단계 전체 중단**으로 만들었습니다(한 잡만 빼지 않음).
200원자 잡이 16건일 때 한 건의 `INP_CHANGED` 로 나머지 15건을 막는 것이 옳습니까,
아니면 **문제 잡만 게이트하고 나머지는 진행**한 뒤 분석기가 막는 편이 낫습니까?
저희는 전자가 옳다고 봅니다 — 무엇이 어긋났는지 모르는 채 계속 도는 것이 더 비싸다고
보아서입니다만, 계산 시간 손실 논거는 반대 방향입니다.

**Q2.** receipt 의 위협모델을 산출물에 이렇게 적었습니다: *“위조는 막지 못한다(같은
사용자). 막는 것은 고친 줄 모르고 옛 결과를 판정에 쓰는 것이다.”* 이 서술이 정확합니까,
아니면 receipt 가 **더 약한 것**만 보증한다고 보십니까?

**Q3.** `S0P`(1층 probe) 잡에는 분석기 receipt 게이트를 걸지 않았습니다. probe 는
`NoIter` 라 에너지·class 판정에 쓰이지 않고 “회전이 목표 자리에 스핀을 놓았나”만
보기 때문입니다. 그런데 그 판정이 seed 채택 여부를 가릅니다. **걸어야 합니까?**

**Q4.** 요청 W Q4 에 대한 저희 잠정 답입니다: L2 의 `%moinp` 패치는 **허용하되 봉인을
갱신하고 그 이전 출력을 낡은 것으로 처리**하는 방식을 택했습니다(위 P0-5). 대안은
loccheck 를 **번들 생성 전에** 돌려 suffix 를 확정하는 것입니다. 지금 방식으로
충분합니까, 아니면 생성 전 확정이 맞습니까?

**Q5.** 0절의 `bash -n` 사건이 시사하는 것을 저희는 이렇게 읽습니다 — *“생성기가 만든
산출물을 selftest 가 실행 가능성 수준에서라도 태워 보지 않으면, 통과 개수는 아무것도
보증하지 않는다.”* 같은 형태로 **아직 안 태워 본 산출물**이 이 번들에 또 있다고
보십니까? (저희가 아는 것: `run_pilot.sh` 의 나머지 stage 는 `bash -n` 만 통과했고
`loccheck`/`L`/`S`/`analyze` 경로를 실제로 실행한 적은 없습니다.)

**Q6.** phase L 을 열어도 됩니까? 열 수 있다면 **어디까지**입니까 — `loccheck` 만,
아니면 `loccheck` → `L` → `L2` 까지입니까? 저희는 `loccheck` 단독을 먼저 돌리고
그 증서를 회신에 실어 다시 여쭙는 편이 맞다고 봅니다.

파일은 수정하지 않으셔도 됩니다 — **GO/NO-GO 와 P0/P1** 판정만 주십시오.
