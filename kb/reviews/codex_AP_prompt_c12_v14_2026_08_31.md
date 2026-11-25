---
title: "리뷰 요청 AP — C-12 v14 (회신 AO 해제조건 9건 이행)"
date: 2026-08-31
updated: 2026-08-31
tags: [review, codex, sdcp, c12, vasp, bundle, staged, potcar]
status: 발송 대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: max
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 요청 AP — C-12 v14

회신 AO(v13 제출 NO-GO)의 최종 해제조건 9건을 이행했다. AO 는 해시·경로·고정기하는
전부 통과시켰고, 막은 것은 **실행 경로**와 **estimand** 였다. 그 둘만 고쳤다.

- 번들: `sdcp_c12_v14.zip`
- 생성 커밋: `b86a8205` (`claude/friendly-meitner-lldvar`)
- 생성 인자: v13 과 **동일** — `--from_basins db/properties/c12_poses_2026_08_30.json
  --frags sdcp_neutral ptfe_c10 --refs --refs_minimal --both_seeds --single_point
  --allow_no_pin --cell_c 36.6551 --cell_c2 40.6551 --min_vacuum 15.0
  --roles primary sensitivity stress_sensitivity`
- 14잡 · 조각 2 · 자세 동결 동일 (물리·후보집합은 **하나도 안 바꿨다**)

## 1. 조건별 이행

**① stage 별 completeness 분리 (AO P0-1)**
`--gate vacconv` 분기를 **무결성 검사 직후**로 올려, e_ads·전체 completeness 검사가
그것을 앞지르지 못하게 했다. completeness 자체도 단계별로 좁혔다.
단계 분류는 `run_staged.sh` 와 **같은 규칙**(job.json 구조화 필드 `kind`/`role`/`vacconv`/`seed`)
이고 이름 파싱을 하지 않는다.
⚠ 계획 meta 가 없어 단계를 **모르는** 항목은 '2단계' 로 밀지 않고 **양쪽 모두에서 필수**로
센다 (모르는 것을 빼면 거짓 통과다). 그 사실을 미완 메시지에 찍는다.

**② POTCAR 조립을 포함한 단일 staged 실행 경로 (AO P0-2)**
`SEAL_POTCAR_ROOT.sh` 신설. `run_staged.sh` 가 **첫 VASP 실행 전에** 이것을 부른다:
전 잡 `POTCAR_ASSEMBLE.sh` 실행 → variant 별 원본 SHA256 수집 → 잡 사이 불일치가 있으면
중단 → `POTCAR_ROOT_SEAL.json` 봉인. 이미 봉인돼 있으면 **대조만** 하고 바꾸지 않는다.
`run_staged.sh` 는 `PP`·`POTCAR_ALLOWLIST` 를 필수 환경변수로 요구한다.

**③ 해시 결박 stage-1 PASS receipt (AO P0-3)**
1단계 vacconv 통과 시 분석기가 `STAGE1_PASS.json` 을 쓴다 —
`manifest_sha256`(MANIFEST.json 바이트 해시) · `stage1_jobs` · `stage1_energies_eV` ·
verdict · `delta_vac_meV`. `run_staged.sh 2` 는 이 파일이 없거나 **지금 MANIFEST 해시와
다르면** 실행하지 않는다.
그리고 **`run_all.sh` 를 staged 구성에서 아예 내지 않는다** (전체 제출 경로가 있으면
정지 규칙이 무력화된다). README 가 그 부재를 명시한다.

**④ 동일 기하 gas canary (AO P0-4)**
canary 디렉터리에 `PARENT_GEOM`(부모 잡 상대경로)을 넣고, `run_job.sh` 가 static 단계에서
부모의 `relax/CONTCAR`(부모가 static-only 면 부모 루트 POSCAR)를 **런타임에** 복사한다.
부모가 아직 안 돌았으면 중단한다.
분석기는 두 `static/POSCAR` 를 직접 읽어 **Cartesian·셀 최대차 ≤ 1e-6 Å** 를 hard-gate 한다
(`CANARY_GEOM_MISMATCH`). **대조를 못 했으면 그것도 차단**이다(`CANARY_GEOM_UNCHECKED`) —
확인 못 한 것을 통과로 읽지 않는다. `NUPDOWN=-1` + 보상 MAGMOM + fresh `ICHARG=2` 는 유지.
실측: 두 canary 가 각각 `../mol__sdcp_neutral__box24` · `../mol__ptfe_c10__box24` 를 가리킨다.

**⑤ CHGCAR-read gate 연결 (AO P0-5)**
`_icharg1_chgcar_gate()` 를 `phase_gates()` 마지막에 실제로 호출한다.
`True`/`False`/`None` 세 경로를 e2e 로 봉인했다 — 픽스처 OUTCAR 도 실물 마커
(`initial charge density was supplied` / `charge density of overlapping atoms calculated`)를
쓰도록 고쳤다. 이 수정 직후 픽스처 전 잡이 `CHGCAR_NOT_READ` 로 막힌 것이 게이트가
실제로 연결됐다는 증거다.

**⑥ gas-box 근거 (AO P0-6) — 비차단 강등을 택했다**
두 결함을 다 고쳤다. ⑴ `ok = d0 <= BOX_TOL` 이 **부호 있는** 값을 비교해 큰 음수도
통과하던 것 → 절대값. ⑵ 더 근본적으로, prior 는 이번 conformer·이번 Hamiltonian 과의
정합을 확인하지 못했으므로 **게이트로 쓰지 않는다** — `pass: null`,
`source: prior_informational_only`, `verified_in_this_bundle: false`.
대신 침묵하지 않는다: `prereg_closure.caveats` 에 `GAS_BOX_UNVERIFIED` 를 박고
*"최종 D 에는 E_G^SDCP − E_G^control 이 남아 상자 오차가 소거되지 않는다.
'기체 상자 수렴 확인' 을 쓰지 말 것"* 을 같이 싣는다.
⚠ **box20 2잡을 이번 묶음에서 계산하는 쪽은 택하지 않았다.** Q2 에서 묻는다.

**⑦ pm1 exact estimand 와 net4 sensitivity 분리 (AO P0-7)**
집합 검사(2c)가 만든 블록 중 **D 에 들어가는 네 잡을 언급하지 않는 것**
(`BASIN_HETEROGENEOUS`·`BASIN_UNRESOLVED_IN_SET`·`GATED_POSE`)은 차단이 아니라
`nonprimary_notes` 로 내린다. 전역 블록(후보집합·canary·spin control·POTCAR)은 그대로 둔다.
⚠ 이 강등은 `if out["blocks"]: return out` **앞에서** 한다 — 뒤에 두면 이미 return 된 뒤다
(첫 구현이 그 실수를 했고 selftest 가 잡았다).
그 대신 **네 잡 자신**의 realized basin 은 직접 요구한다 (`ESTIMAND_BASIN_UNRESOLVED`).
생성기가 `estimand_job_keys_net4` 를 따로 봉인하고, 분석기가
`D_net4` · `D_net4_minus_D_pm1_eV` 를 **실제로 계산**해 `branch_sensitivity` 에 싣는다.
못 내면 `status: unavailable` 로 적고 **D_pm1 은 영향받지 않는다**.

**⑧ 완전한 원소별 POTCAR fingerprint 및 VASP-version gate (AO P0-8)**
**완주한 모든 잡**(`static` 레코드가 있는 잡)에 대해:
- provenance 존재 — 없으면 `POTCAR_PROVENANCE_MISSING`
- `job.json.species_order` × `manifest.potcar_spec` 로 만든 **기대 variant 전부**의
  원본 SHA256 이 **64자리 hex** — 아니면 `POTCAR_SOURCE_INCOMPLETE`
- VASP 버전 관측 — 없으면 `VASP_VERSION_UNOBSERVED` (0개 관측은 일치가 아니다)
⚠ 아직 안 돈 잡은 세지 않는다 (단계별 실행에서 2단계가 비어 있는 것은 정상).
variant 키(`Ni_pv`)·원소 키(`Ni`) 철자 차이는 pin 대조와 **같은 정규화**로 흡수한다.

**⑨ 문서 동기화 (AO P1)**
- manifest `potcar_pin_note`: "제출본이 아니다" → 새 provenance-root 방식 서술
- `POTCAR_SPEC.txt`: "2026-08-08 납품과 동일 계보" **삭제** (검증하지 않은 주장)
- README: staged 단일 경로만 안내, POTCAR 를 손으로 조립하지 말라고 명시,
  `run_all.sh` 부재를 명시, 단일 잡 실행은 "한 잡 재실행" 용도로만
- `same_rounded`: v13 에서 이미 정보용으로 강등돼 있었고 문서 문구를 코드에 맞췄다

## 2. AO Q1 — pin 을 어떻게 처리했나

AO 문구를 그대로 채택했다: *"계산 시작 전에 vendor 가 제공한 원소별 source SHA256 을
자동 봉인해 새 v13 root 로 승인하면 된다. 계산 후 각 job 이 신고한 provenance 끼리만
비교하는 현재 방식은 독립적인 사전 승인과 같지 않다."*

`SEAL_POTCAR_ROOT.sh` 가 **첫 VASP 실행 전에** 봉인하고, 봉인이 이미 있으면 대조만 한다.
분석기는 전 잡 provenance 를 그 봉인과 대조한다: `ROOT_SEAL_MISMATCH` ·
`ROOT_SEAL_UNOBSERVED` · `ROOT_SEAL_INCOMPLETE`(봉인에 없는 variant 관측).

라벨이 실측에 따라 **세 갈래**로 갈린다 (v13 의 단일 문구는 사실보다 강했다):
- `sealed_root_v13` — 봉인 일치 **그리고** ⑧ 완전성 통과
- `self_consistent_only` — 완전성은 통과, 봉인 없음
- `unverified` — 원본 fingerprint 또는 VASP 버전 관측이 불완전. **'신원 일치 확인' 이라고
  쓰지 말 것**

⚠ **한계를 그대로 적는다**: 봉인한 트리가 **공식 배포판인지는 확인하지 못한다**(정본 SHA 를
라이선스로 우리가 못 싣는다). 봉인은 "이 계산들이 하나의 트리에서 나왔고 그 트리가
생산 전에 고정됐다" 까지만 보증하고, 그 트리의 신원은 site allowlist 가 진다.
스크립트 docstring 에 그대로 박아 놨다.

## 3. 우리가 하지 않은 것 (숨기지 않는다)

- **box20 을 이번 묶음에서 계산하지 않았다.** prior 를 비차단으로 내리고 D 에 라벨을 달았다.
- **봉인 트리를 공식 release 와 독립 대조하지 않았다.** (위 한계)
- **v14 를 실제 VASP 로 돌려보지 않았다.** 잡 0개다. staged 경로는 selftest e2e 로만 확인했다.
- 물리·후보집합·자세 동결·고정기하는 **하나도 안 바꿨다** (v13 과 동일).

## 4. 증거

`python3 tools/sdcp/vasp_handoff_bundle.py --selftest` — **467 검사 통과** (v13 291).
AO 가 지적한 *"selftest PASS 는 확인했지만 실제 stage 경로와 번들 e2e 를 검증하지 않아
해제 증거로 충분하지 않다"* 를 정면으로 덮었다. 새로 추가한 것 중 핵심:

- **staged(refs_minimal) 번들을 selftest 가 실제로 만든다.** 종전엔 이 구성을 한 번도
  안 만들어서, 문서가 안내한 경로가 fresh ZIP 에서 도는지 아무도 안 봤다.
- **1단계만 완주시킨 뒤** 분석기를 `--gate` 유무로 두 번 실행해 비교한다:
  `--gate` 없으면 2단계 미완 3건이 잡히고, `--gate vacconv` 면 **0건**이다.
  (AO P0-1 이 말한 바로 그 회귀)
- `PARENT_GEOM` 이 부모 잡을 가리키는지 · canary `run_job.sh` 가 `relax/CONTCAR` 를 받는지
- `run_staged.sh` 가 `SEAL_POTCAR_ROOT.sh` 를 부르는지 · `STAGE1_PASS.json` + `manifest_sha256`
  를 요구하는지 · staged 번들에 `run_all.sh` 가 **없는지**
- `POTCAR_SPEC.txt` 에 계보 주장이 없는지 · manifest pin 설명이 새 방식과 일치하는지
- canary 기하 불일치 → 차단 / 대조 결과 부재 → 차단
- net4 가 다른 basin 이어도 D_pm1 이 나오는지 / **네 잡 자신**의 basin 이 없으면 막는지 /
  net4 봉인 시 `D_net4 − D_pm1` 을 실제로 내는지
- POTCAR: sha 가 64자리 아님 / variant 누락 / 버전 0개 관측 / provenance 부재 →
  각각 차단. **아직 안 돈 잡은 대상 아님**(양성). root seal 불일치·미봉인 variant → 차단.
  라벨 세 갈래가 실제로 갈리는지.

실물 v14 확인 (gabia, 생성 직후):
```
잡 수: 14 · pm1 직접식 True · net4 직접식 True
run_staged.sh ✔ · SEAL_POTCAR_ROOT.sh ✔ · run_all.sh 없음 ✔
canary mol__sdcp_neutral__box24__nzmag → ../mol__sdcp_neutral__box24
canary mol__ptfe_c10__box24__nzmag     → ../mol__ptfe_c10__box24
```

## 5. 묻는 것

**Q1.** ⑥ 의 선택 — prior 를 **비차단 강등 + D 에 라벨** 로 둔 것이 AO 의 두 갈래 중
받아들일 수 있는 쪽인가? 아니면 원고에 쓰려면 결국 **box20 2잡을 이 묶음에서 계산**해야
하나? (기체 static 2잡이라 비용은 작다. 넣으면 14 → 16잡, 1단계 8 → 10.)
넣는 쪽이 맞다면 **지금 넣고 다시 심사**받는 게 나은지, v14 로 돌린 뒤 별도로 붙이는 게
나은지도 판단해 달라.

**Q2.** AO Q1 의 "사전 승인" 을 **러너가 원격에서 생성 전에 봉인**하는 방식으로 만족시켰다고
볼 수 있나? 우리가 승인한 트리와 대조한 것이 아니라, **외주처의 트리를 첫 실행 전에
동결**한 것이다. 이것이 "결과를 본 뒤 Hamiltonian 을 고르는 자유를 없앤다" 는 목적을
달성하는가, 아니면 여전히 우리 쪽 사전 승인이 필요한가?

**Q3.** ⑨ 의 Methods 문구. AO 가 준 권장 문구를 쓰되, 우리는 release 와 독립 대조를 하지
않으므로 AO 가 말한 두 번째 단서가 필요하다. 그런데 AO 스스로 *"두 번째 문구는 내부
기록에는 가능해도 원고 Methods 로는 약하다"* 고 했다.
⇒ **원고에 넣으려면 release·variant 를 실제로 확인해야 하나?** 확인한다면 우리가 무엇을
어떻게 받아야 하나 (외주처에서 받을 구체적 산출물)?

**Q4.** ① 의 "meta 가 없어 단계를 모르는 항목은 양쪽 다 필수" 규칙이 옳은가?
반대 방향(1단계에서 제외)이 거짓 통과를 만든다는 판단인데, 실제 v14 는 전 항목에 meta 가
있어 이 경로가 안 돈다. 죽은 안전장치인가, 남길 값이 있나?

**Q5.** ⑦ 의 강등 목록(`BASIN_HETEROGENEOUS`·`BASIN_UNRESOLVED_IN_SET`·`GATED_POSE`)이
과한가 부족한가? 강등 판정은 "블록 문자열이 네 잡 경로를 **언급하지 않으면**" 이다 —
문자열 매칭이라 취약해 보인다. 구조화된 방식이 필요한가?

**Q6.** ④ 의 `PARENT_GEOM` 이 **런타임 파일 복사**라, 부모가 실패했는데 이어 돌리면
어떻게 되는지. 지금은 `relax/CONTCAR` 가 없으면 중단한다. 부모가 **잘못된 값으로 완주**한
경우(예: 미수렴)는 분석기가 잡지만, canary 는 그 기하를 이미 썼다. 이 순서가 문제인가?

**Q7.** ⑧ 이 "완주한 잡" 을 `static` 레코드 존재로 판정한다. 단계별 실행에서 2단계가
비어 있는 것을 정상으로 보기 위한 것인데, 이 판정이 우회 가능한가?

**Q8.** 그 외 v14 에서 실행·estimand 를 막는 것이 남았는가. **제출 GO/NO-GO.**
