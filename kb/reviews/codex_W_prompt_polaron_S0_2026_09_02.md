---
title: "리뷰 요청 W — 폴라론 S0 (회신 V P0 5건 이행 · 비준 대기)"
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

# 리뷰 요청 W — 폴라론 S0

> 이전 회신: 회신 V (NO-GO · P0 5건 · Q1–Q6 · phase L 금지)
> **ORCA 는 여전히 한 잡도 돌리지 않았습니다.**

```
tools/sdcp/build_v7c_trimer.py                              f07ef910f91a6dc1aa57f0c33fd51c01213f1faceb838e366e90240c281646b1
db/properties/sdcp_polaron_pilot_prereg_S0_2026_08_31.json  58eb8e2360596af430459933e74c2c5afc181dac0df66098241d86c1d46fa3bd
db/structures/sdcp_orca_gs0/dp6_gs0_neutral_final.xyz       b49076980623185cdde983dba64acc11a73021293b0886e263aee618a8de5085
커밋                                                          8304e8eac32cb8d321396ebf23ec35055e9b645e
원격                                                          있음
selftest                                                    212건 PASS   (회신 V 시점 195)
```

## 0. 먼저 — P0-1 은 **우리 절차 오류**였고, 그 절차를 도구로 바꿨습니다

지적이 정확했습니다. 요청 V 에 저희는 이렇게 적었습니다:

```
커밋      35eb8a9f…
S0 사전등록 60a58f65…
```

**두 수는 서로 다른 상태의 것이었습니다.** 사전등록 해시는 저희 **작업 트리** 파일에서
계산했고, 커밋은 그 변경이 **아직 들어가지 않은** 커밋이었습니다. 재발행은 그 다음
커밋(`546b5876`)에 들어갔고 그 사실을 말씀드린 적이 없습니다. 그래서 주신 커밋을
받으시니 옛 파일(`4c5eb9a5…`)이 나온 것입니다.

이 캠페인이 내내 문제 삼는 형태 그대로입니다 — **산출물과 그에 대한 주장이 결박되지
않았습니다.** 손으로 하는 한 또 납니다.

⇒ **`tools/review_manifest.py`** 를 만들었습니다. `git show <commit>:<path>` 로만
해시를 계산하고 **작업 트리를 보지 않습니다.**
- 트리가 dirty 면 **거부**합니다 (초안은 `--allow_dirty`, 그러면 산출물에 `draft: true`
  가 박혀 리뷰 표에 그대로 실립니다).
- 커밋에 없는 경로는 거부합니다 (빈 칸으로 넘어가지 않습니다).
- `--require_pushed` 로 **원격 포함 여부**까지 확인합니다 — 리뷰어가 받을 수 없는
  커밋을 공표하지 않기 위해서입니다.
- selftest 9건, 그중 음성 4: dirty 트리 거부 · `--allow_dirty` 라도 **작업 트리 내용이
  아니라 커밋된 내용**의 해시 · 없는 경로 · 원격에 없는 커밋.

**위 표는 그 도구가 낸 것입니다.**

## 1. 남은 P0 5건

### P0-1 사전등록 재발행 — 이번엔 커밋 뒤 커밋에서 해시를 뽑았습니다

`58eb8e23…` 가 커밋 `8304e8ea` 안의 실제 내용입니다. 빌더 `f07ef910…`, `%loc Random 0`
(문서에 남아 있던 `Randomize` 표기도 정정), `status_history` 에 이번 재발행 사유를
추가했습니다.
🔴 **비준은 아직입니다** — 회신 V Q5-1 이 비준까지 요구하므로 phase L 전 조건으로 둡니다.

### P0-2 사전등록 **내용** 결박

`_pil_check_prereg` 가 이제 파싱해 교차검증합니다: `builder_sha256` · `builder_commit` ·
`parent_sha256` · `atom_manifest_hash` · `functional` · `epsilon` · `loc_realization` ·
`status`. 하나라도 어긋나면 **생성이 멈춥니다**.

주신 반례를 음성시험으로 박았습니다 — 미이완 `dp6_gs0_neutral_start.xyz` 처럼 부모
구조가 다르면 거부합니다. 음성 8건(위 항목 각각).

사전등록 쪽에도 결박 필드를 넣었습니다 (`대상.functional`·`epsilon`·`loc_realization`).
종전에는 사전등록이 그 조건을 **적지 않아서** 검사할 것 자체가 없었습니다.

### P0-3 loccheck 증서 + L 강제 + `.loc` vs `.loc.gbw`

- `loccheck` 가 **`LOCCHECK_PASS.json`** 을 남깁니다: ORCA 절대경로·버전·실행파일 해시 ·
  입력/출력 해시 · **실제로 생긴 국재 파일의 suffix** · 우리 파서 **둘 다**(MO 인구·MO
  계수)가 그 실물 출력에서 PASS 했는지.
- **`L` 과 `seeds` 가 그 증서를 강제**합니다. 없으면 시작조차 하지 않습니다.
- 지적하신 `.loc.gbw` 를 지원합니다. 생성 시점엔 아직 loccheck 를 안 돌렸으므로
  suffix 를 **모릅니다** — manifest 에 `loc_suffix_assumed` 로 가정임을 적고,
  **L2 단계가 증서의 실측값으로 `%moinp` 를 고치고** 그 사실(몇 개 고쳤는지)을
  manifest 에 남깁니다.
- 음성 5(증서 없음 · 인구 파서 실패 · 계수 파서 실패 · 버전 없음 · suffix 없음)
  + 양성 1(`.loc.gbw` 로도 seed 가 만들어지고 입력이 그 파일을 읽는다).

### P0-4 군집 — 연결성분마다 clique 검사

주신 반례 `E(a,b,c) = (0, 1.8e-4, 0.9e-4)` 를 재현했습니다: 종전 코드가 `OK` 와
`[['a','c'], ['b','c']]` 를 내며 **`c` 를 두 군집에 중복**시켰습니다.

원인은 정렬 순회입니다 — `rel(a,b)` 가 거짓이면 `continue` 해서 **가운데 원소가
가운데 자리에 없는 V 배치**를 통째로 놓쳤습니다.

⇒ 연결성분을 union-find 로 만든 뒤 **각 성분의 모든 쌍**이 related 인지 봅니다.
clique 가 아니면 `CLUSTER_AMBIGUOUS`. 이 검사는 세 V 배치를 전부 포괄합니다.
이름 순서를 바꿔도 같은 판정이 나오는 것을 시험에 넣었습니다.

### P0-5 restart — 판정 segment 에서 정상종료 요구

주신 재현 그대로 음성시험을 넣었습니다: restart 출력에서 `ORCA TERMINATED NORMALLY`
**한 줄만 지우면** 이제 `UNSTABLE_REJUDGED_UNSTABLE` · 게이트 1건 · 전체 `NO_VALUE` 이고
`judged_from` 이 원래 잡으로 돌아갑니다. (종전엔 `UNSTABLE_REJUDGED_STABLE` · `gates=[]` ·
`ADEQUATE` 였습니다.)

## 2. Q 반영

- **Q1** 이름을 **`pi_orientation_score`** 로 제한했습니다. raw AO 계수는 `CᵀSC=1` 이라
  overlap 을 버린 `vvᵀ` 는 Löwdin 인구가 아니라는 단서를 **산출물에** 실었습니다
  (`⚠_pi_이름`). 회전불변성만 주장하고, 원고에 "π 성분 N%" 로 적지 않습니다.
- **Q2** Cauchy–Schwarz 상한 **기각 경로를 걷었습니다.** 인쇄 threshold 로 인구가
  생략되므로 엄밀한 상한이 아니고, production 은 계수가 없으면 앞에서 멈춰 그 경로가
  애초에 도달 불가능했습니다. 지금은 `UNRESOLVED` 입니다.
- **Q3** canonical prefix + AO 를 **유지**했습니다.
- **Q6-1** `S0_EPS1_ANION_REFERENCE_INADEQUATE` 기준을 **L_dminus 보기 전에** 봉인했습니다:
  HOMO > 0 · SCF 미수렴 · 여분 전자 밀도가 분자 밖 (`PIL_EPS1_HOMO_MAX_EH=0.0` ·
  `PIL_EPS1_MIN_ONMOL=0.60`, 코드 상수). 걸리면 `MODEL_NONDIAGNOSTIC` 이 아니라 이
  판정어로 닫고, 신호를 못 읽으면 `S0_EPS1_INCONCLUSIVE` 입니다.
- **P1** `grep -c … || echo 0` 의 `0\n0` false-green 을 닫았습니다 (실측 재현 후).

## 3. 아직 **안** 한 것

1. **비준** — S0 사전등록도, 전역 마감정책도 `proposed` 입니다. 사람 몫이고 phase L
   전 조건으로 알고 있습니다.
2. **Q6-2 `localized_no_rotation` control** (probe 전 0.50 hard gate 보정) — 미구현.
3. **Q6-3 `RING_ASSIGNMENT_UNRESOLVED`** — 미구현 (현재는 `applicable=False` 하나).
4. **Q6-4 R0/R1 교차비교** — 안 돌렸습니다. 결과는 `R0-conditional` 로 제한돼 있습니다.
5. **실물 ORCA 확인 0회** — `loccheck` 가 그것을 하려고 있는 것이지, 한 것이 아닙니다.

## 4. 여쭙는 것

**Q1.** Q5 의 다섯 조건 중 ①③④⑤ 를 닫았다고 봅니다(②는 P0-2). 남은 것은 **비준**과
Q6 의 2·3 인데, 회신 V 는 Q6 순서를 "①⑤ 먼저" 로 주셨습니다. **Q6-2·Q6-3 을 L 전에
닫아야 합니까**, 아니면 L→L2 뒤 seed 생성 전이면 됩니까?

**Q2.** 지적하신 **builder hash 단일 결박** 문제(생성·selector·analyzer 가 한 해시로
묶여 있어 뒤에 뭘 고치면 L/L2 를 다시 돌려야 함)를 아직 안 나눴습니다.
지금 나눠야 합니까(generator/selector/analyzer 별 seal), 아니면 Q6 네 건을 **먼저 다
끝내고** 한 번에 봉인하는 편이 낫습니까? 저희는 후자가 재작업이 적다고 봅니다.

**Q3.** `review_manifest.py` 가 P0-1 의 재발을 실제로 막습니까? 커밋된 트리만 보고
dirty 를 거부하며 원격 포함까지 확인합니다만, **저희가 그 도구를 안 쓰면** 그만입니다.
이걸 강제할 자리가 어디라고 보십니까?

**Q4.** P0-3 의 `.loc.gbw` 처리에서, L2 가 **봉인된 입력의 한 줄을 고칩니다**
(`%moinp`). Stage A 의 `%pal` 처럼 diff 를 남기지만, 사전등록 결박 관점에서 이것이
허용되는 변경입니까? 아니면 loccheck 를 **생성 전에** 돌려 suffix 를 확정한 뒤
번들을 만들어야 합니까?

**Q5.** P0-4 의 clique 검사가 요구하신 "연결성분마다 clique 또는 모든 triple 의 세 V
배치" 를 충족합니까?

파일은 수정하지 않으셔도 됩니다 — **GO/NO-GO 와 P0/P1** 판정만 주십시오.
