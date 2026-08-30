---
title: "리뷰 요청 AQ — C-12 v15 (회신 AP 해제조건 12건 이행)"
date: 2026-08-31
updated: 2026-08-31
tags: [review, codex, sdcp, c12, vasp, bundle, staged, potcar, attestation]
status: 발송 대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: max
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 요청 AQ — C-12 v15

회신 AP(v14 제출 NO-GO)의 해제조건 **12건 전부**와 Q1·Q3·Q4·Q5·Q7 을 이행했다.
AP 는 ZIP 무결성·해시·잡수를 통과시켰고, 막은 것은 **실행 경로와 exact estimand** 였다.

- 번들: `sdcp_c12_v15.zip`
- 생성 커밋: `claude/friendly-meitner-lldvar`
- **잡 수가 14 → 16 으로 늘었다** (box20 두 잡 · AP #11). 1단계 8 → **10**.
- 물리·후보집합·자세 동결은 **하나도 안 바꿨다**. v14 와 같은 인자 + box20.
- ⚠ **VASP 를 한 잡도 돌리지 않았다.** 따라서 AP Q1 이 말한
  *"결과를 보기 전"* 창이 아직 열려 있고, box20 을 지금 넣었다.

## 1. 조건별 이행

**① canary 기하 기대값 (AP #1)**
`PARENT_GEOM` 이 있는 잡은 **선언된 부모의 최종 기하**를 기대값으로 삼는다
(`_expected_geom_src`). 비교는 바이트 해시가 아니라 `_geom_equal` —
원소·순서·개수·셀·Cartesian(1e-4 Å)·고정플래그. OUTCAR 좌표 대조 경로도 같은
기대값을 쓴다. 부모 기하를 못 찾으면 그 사유가 찍힌다.
⇒ 종전엔 **정상 canary 가 반드시 막혔다** (CONTCAR 서식만 달라도 불일치).

**② exact complex 쌍의 Ni topology 직접 비교 (AP #2)**
`_estimand_topology_check(keys, jobs, label)` 신설. 두 complex 의 Ni 부호
topology 를 **전역 스핀 반전 동치 아래** 직접 비교한다(`same_topology_direct`).
모멘트 표를 못 읽으면 `ESTIMAND_TOPOLOGY_UNRESOLVED`, 갈리면 `_MISMATCH`.
net4 도 같은 검사를 하되 **차단하지 않고** `usable_as_sensitivity` 를 내린다.
⚠ 처음 붙일 때 이 검사를 강등 블록 **안에** 넣어서 `blocks` 가 비면 실행되지
않았다 — 밖으로 뺐다. (원래의 basin 존재 요구도 같은 자리였으니 같은 결함이었다.)

**③ pooled block 구조화 + 문자열 판정 제거 (AP #3)**
`block_records` = `{code, msg, job_keys, scope, affects_estimand}`.
⇒ 그런데 job_keys 교집합으로 걸러 보니 **반대 문제**가 나왔다: pooled 집합에는
exact key 가 거의 항상 섞여 있어(`BASIN_HETEROGENEOUS` 의 job_keys 가 그 조각의
전 잡) 결국 D 가 죽는다.
⇒ AP 권고대로 **필터링을 버렸다.** exact-key 경로에서는 `scope=pooled_diagnostic`
을 **전부** 강등한다. 그 진단의 목적("pooled 집합에서 min 을 뽑지 마라")이 이
경로에 적용되지 않기 때문이다. 네 잡의 안전은 따로 보장한다:
게이트 → `ESTIMAND_KEY_UNUSABLE` · 에너지 없음 → 같음 · 자기 상태 → ②.
그 근거를 `pooled_demote_policy` 로 결과에 명시한다. **Q1 에서 묻는다.**

**④ primary/net4/대안자세 분리 (AP #4)**
tier: `estimand` = 봉인된 네 잡 + 기체 기준 + 진공쌍 / `sensitivity` = net4·대안자세.
종료코드는 estimand tier 만 본다. sensitivity 결측은
`required_missing_sensitivity` · `sensitivity_status` · 경고로 **보고**한다.
⚠ 처음엔 무조건 나눴더니 레거시 Li/Ni 경로 잡이 sensitivity 로 강등돼 **누락이
종료코드에서 사라졌다.** 봉인된 식이 없으면 전부 estimand 로 둔다.

**⑤ stage-1 선결조건 (AP #5)**
`stage1_prerequisites` = `vacuum` · `molecular_state` · `canary_geometry` ·
`potcar_identity`. **전부** 통과해야 열리고, **vacuum 판정보다 먼저** 본다.
각 항목의 pass/why 를 찍고 `STAGE1_PASS.json` 에도 싣는다.

**⑥ receipt 결박 (AP #6)**
AP 가 권한 단순한 쪽을 택했다 — **2단계 시작 직전에 `--gate vacconv` 를 다시
실행**한다. 위조 receipt(`verdict:"FAIL"`)로 우회할 경로 자체가 없어진다.
receipt 에도 "이 파일이 있다는 것만으로 열지 않는다" 를 적었다.

**⑦ 진짜 pre-production root seal (AP #7)**
`SEAL_POTCAR_ROOT.sh` v2:
- 최초 봉인 전 `OUTCAR/vasprun/OSZICAR/CONTCAR/WAVECAR/CHGCAR` 가 하나라도 있으면 **거부**
- 기존 provenance 의 `allowlist_sha256` 이 현재와 다르면 **재조립** (종전엔 건너뜀)
- 봉인 내용: variant source sha · 잡별 assembled sha · allowlist sha ·
  MANIFEST sha · VASP 실행파일 경로/sha/버전 배너 · 봉인 UTC
- 재봉인 시 allowlist 가 바뀌었으면 중단
분석기: 봉인의 `manifest_sha256` 이 이 묶음과 다르면 `ROOT_SEAL_WRONG_BUNDLE`,
`sealed_before_production` 근거 없으면 `_NOT_PREPRODUCTION`, 그리고
**identity blocking 이 하나라도 있으면 sealed 라벨을 발행하지 않는다**
(종전엔 `ROOT_SEAL_MISMATCH` 와 `sealed_root_v13` 이 동시에 나올 수 있었다).

**⑧ completed 판정 + production-shape selftest (AP #8)**
생성부가 미실행 잡에도 `static: None` 키를 넣는다는 것을 코드에서 확인했다
(`rec = {..., "static": ocs.get("static"), ...}`). 판정을 세 단계로:
`not_attempted`(static 이 dict 아님) / `attempted`(OUTCAR 있으나 정상종료·에너지
없음) / `completed`. 완전성은 **completed 에만** 건다.
**픽스처를 실물 모양으로 바꿨다** — `ran=False` 가 이제 `static: None` 이다.
종전 픽스처는 키를 아예 빼서 `"static" in jr` 이 항상 참인 것을 재현하지 못했다.

**⑨ 러너 fail-hard (AP #9)**
stage 값 검증(1|2) · 잡 분류 실패 시 중단 · `job.json` 에 `kind` 없으면 중단 ·
**잡 수 census 검증**(이 단계 0개면 중단, 잡 폴더 수 ≠ 계획 수면 중단) ·
중복 실행 가드(mkdir 원자성) · **2단계 뒤 최종 분석기까지** 러너가 돌린다.

**⑩ 문서 동기화 (AP #10)**
staged 구성에서:
- SUBMIT 이 **의존성 두 가지**를 명시(canary→부모, 2단계→1단계 게이트)
- **전체 array 제출 예시를 넣지 않는다**
- README 가 "서로 독립이 아닙니다" 로 시작
- **필수 반송물** 명시: `POTCAR_ROOT_SEAL.json` · `STAGE1_PASS.json` ·
  잡별 `POTCAR_PROVENANCE.json` · **부모·canary 의 `static/POSCAR`** · OUTCAR/OSZICAR
비-staged 번들은 종전 안내를 유지한다(회귀 방지 시험 포함).

**⑪ box20 + δ_gas (AP #11)**
`refs_minimal` 에서도 box20 을 낸다 (**16잡 · 1단계 10**). 두 잡 다
`--single_point` 라 **독립 재이완이 없다** — 같은 원본 분자에서 셀만 바꾼
고정기하 static 이고 state-selection policy 도 같다.
`gas_box_prior`(선행 대조)를 **싣지 않는다**.
게이트를 조각별 10 meV 가 아니라 **최종 estimand 에 직접**:
```
δ_gas = [E_G^sdcp(24) − E_G^sdcp(20)] − [E_G^ctl(24) − E_G^ctl(20)]
|δ_gas| ≤ 5 meV
```
selftest 가 정확히 "조각별 4 meV 씩인데 부호가 반대라 차에서 8 meV" 를 만든다.
box20 이 없으면 `GAS_BOX_NOT_MEASURED` 로 막는다. **Q2 에서 묻는다.**

**⑫ release attestation (AP #12·Q3)**
번들에 `POTCAR_ATTESTATION_REQUEST.md` + `MAKE_POTCAR_ATTESTATION.sh`.
AP 가 준 목록 그대로 담는다(ZIP·MANIFEST sha · release label · variant 목록 ·
variant 별 원본 전체 sha · TITEL 과 embedded hash · allowlist sha · 생성 UTC·
사이트 · `vasp_std --version` 원문 · VASP 실행파일 sha·경로).
분석기가 검증한다: 필드 누락 · 다른 묶음 · variant sha 형식 · 생산 전 근거 ·
**root seal 과 원본 sha 일치**. 하나라도 걸리면 blocking.
그리고 **Methods 문구를 코드가 하나로 만든다**(`methods_sentence`) — 사람이
고르게 두면 강한 쪽을 고르기 때문이다. attestation 통과 시 AP 가 준 release
명시 문구, 아니면 조건부 문구 + "원고 Methods 로는 약하다".
`POTCAR_SPEC.txt` 의 `PBE PAW 5.4` 단정도 제거했다 (AP Q3).

**Q4 (meta 결측)** — "양쪽 stage 필수" 는 안전장치가 아니라 **영구 deadlock**
이었다. **첫 VASP 전에 생성기에서 schema error 로 중단**한다.
⚠ deadlock 은 단계를 meta 로 나누는 **staged 구성에서만** 생기므로 거기에만 건다.

## 2. 작업 중 우리 selftest 가 잡은 우리 실수 (숨기지 않는다)

1. δ_gas 블록을 `if _ejk0:` 안쪽 들여쓰기로 넣어 **배포 분석기가
   IndentationError 로 죽었다.** 그래서 "분석기가 예외로 죽지 않는다" 를
   다른 검사보다 **먼저** 보는 시험을 추가했다.
2. topology 검사를 강등 블록 안에 넣어 `blocks` 가 비면 안 돌았다.
3. tier 를 무조건 나눴더니 레거시 경로에서 누락이 종료코드에서 사라졌다.
4. Q4 schema error 를 너무 넓게 걸어 레거시 tier1 경로를 막았다.

## 3. 우리가 하지 않은 것

- **attestation 을 아직 받지 않았다.** 따라서 지금 `methods_sentence` 는 약한 쪽이다.
- **VASP 를 한 잡도 돌리지 않았다.** staged 경로는 selftest e2e 로만 확인했다.
- 봉인 트리를 공식 release 와 독립 대조하지 않았다(⑫가 그 통로다).
- 물리·후보집합·자세 동결·고정기하는 **하나도 안 바꿨다**.

## 4. 증거

`--selftest` **524 검사 통과** (AP 심사 시점 469). AP #1~#12 각각에 음성 시험을 붙였다.
staged 번들 e2e 에서 **1단계만 완주시킨 뒤** 분석기를 `--gate` 유무로 두 번 돌려
completeness 범위가 실제로 갈리는지 실행해서 확인한다.

## 5. 묻는 것

**Q1.** ③ 의 최종 선택 — exact-key 경로에서 `pooled_diagnostic` 을 **전부** 강등하는 것이
맞나? AP 는 "필터링보다 직접 비교가 안전" 이라 했고 우리는 **둘 다** 했다(직접 비교 +
전면 강등). 전면 강등이 과한가? pooled 진단 중 estimand 에 **실제로** 적용돼야 하는
것이 남아 있나?

**Q2.** ⑪ 의 "같은 기하" 주장. box20/box24 는 같은 원본 분자를 각각
`p - p.min()` 뒤 `+margin/2` 로 놓아 **내부 좌표는 동일하지만 상자 안 위치가 다르다**
(따라서 `DIPOL`(COM)도 다르다). 이것을 "셀만 바꾼 고정기하" 라고 불러도 되나,
아니면 두 상자에서 **같은 절대 좌표**를 써야 하나? 후자라면 큰 상자 기준으로
작은 상자를 잘라야 하는데 그러면 분자가 경계에 붙을 수 있다.

**Q3.** ② 의 동치 관계 — `same_topology_direct` 는 **전역 스핀 반전**을 같은 상태로 본다.
SDCP 와 PTFE 복합체 사이에 이 동치를 적용하는 것이 맞나? 두 계는 흡착종이 다르므로
슬랩 Ni 배열의 전역 부호가 뒤집힌 것이 물리적으로 같은 상태라고 볼 수 있는지.

**Q4.** ⑤ 의 네 선결조건이 충분한가 과한가. 특히 `potcar_identity` 를 1단계 게이트에
넣으면 **2단계 잡이 아직 안 돌아 provenance 가 없는 상태**가 정상인데, 우리는
completed 잡에만 완전성을 걸어 이를 통과시킨다(⑧). 이 조합에 구멍이 있나?

**Q5.** ⑫ 의 `methods_sentence` 를 **코드가 결정**하게 한 것 — 과한가?
원고 문구를 도구가 내는 것이 적절한 경계인지.

**Q6.** ⑪ 로 잡이 16개가 됐다. AP 가 말한 "16잡·stage 1 열 잡" 과 일치하는지 확인해 달라.

**Q7.** 그 외 v15 에서 실행·estimand 를 막는 것이 남았는가. **제출 GO/NO-GO.**
