---
title: "회신 AR — c12 v15 NO-GO (해제조건 10건)"
date: 2026-08-31
kind: review-reply
system: sdcp
tags: [review, codex, sdcp, c12, vasp, bundle, estimand, no-go]
status: 이행 완료 (해제조건 10건 · v16 재생성 대기)
confidence: high
explored: false
---

> codex 회신 원문. ZIP SHA256 `da6eacb7d7df6a6848a6fc1c40000e2e9ef8a8fd464bccb5cf85e0197fd2b2cd` (v15).

NO-GO
ZIP 자체의 무결성과 16잡 구성은 통과했습니다. 그러나 현재 v15는 exact estimand가 계산 전에 막히는 경로, 반대로 치명적 실패가 지워지거나 stage 2가 열리는 경로가 함께 있습니다. VASP 제출 전 수정해야 합니다.
확인된 정상 항목:

* ZIP SHA256: `da6eacb7d7df6a6848a6fc1c40000e2e9ef8a8fd464bccb5cf85e0197fd2b2cd`
* manifest 등록 파일 114/114 해시 일치
* unsafe·중복 ZIP 경로 없음
* 실물 16잡, stage 1 열 잡·stage 2 여섯 잡
* 새 `δ_gas` 식과 `|δ_gas| ≤ 5 meV` 계산 자체는 맞음
* 최초 box20/box24 POSCAR는 내부좌표가 동일하고 정확한 평행이동 관계

Q1 — pooled diagnostic 전면 강등
조건부 찬성, 현재 구현은 P0.
봉인된 네 exact key로 계산하는 primary D에는 pooled-min heterogeneity가 직접 적용되지 않습니다. 따라서 `scope=pooled_diagnostic`을 primary D의 hard block에서 제외하는 판단은 맞습니다.
다만 analyze_results.py:3880은 강등 시 전체 `out["blocks"]`를 `block_records`에서 다시 만들어, 구조화되지 않은 전역 차단까지 삭제합니다. `MOLECULAR_STATE_UNRESOLVED + BASIN_HETEROGENEOUS`를 넣으면 최종 blocks가 빈 배열이 되는 것을 재현했습니다.
대안:

* canonical block 목록은 절대 수정하지 말 것
* `primary_estimand_blocks`라는 별도 view만 scope로 필터링할 것
* pooled 결과인 `secondary_G`, pooled minimum 및 일반화 주장은 heterogeneity가 있으면 계속 차단할 것
* exact key의 에너지·입력·기하·전자수렴·직접 topology 차단은 별도로 유지할 것

Q2 — box20/box24의 “같은 기하”
개념에는 찬성, 실물 구현은 반대.
같은 절대좌표일 필요는 없습니다. rigid translation을 제거했을 때 내부좌표가 같으면 같은 고정기하입니다. 각 셀 중앙으로 옮기고 `DIPOL`도 COM에 맞춰 갱신하는 편이 적절합니다. VASP도 분자·표면의 dipole correction에서 COM 부근을 권고합니다. [VASP DIPOL 설명](https://vasp.at/wiki/DIPOL)
하지만 실제 번들은 고정기하 static이 아닙니다. box20과 box24의 네 gas parent가 모두 `relax → static`이고, run_job.sh:77이 각 상자에서 독립 이완한 CONTCAR를 static에 넘깁니다. 따라서 현재 `δ_gas`는 셀 효과와 독립 이완 차이를 함께 잽니다.
box24에서 한 번 만든 공통 기하를 box20/box24 중심으로 각각 평행이동해 static 두 개에 사용해야 합니다. 내부좌표·원소순서·전자상태의 cross-job gate도 필요합니다.
또한 옛 조각별 10 meV gate가 analyze_results.py:4644에 남아 있습니다. 예를 들어 SDCP/PTFE 변화가 `+20/+19 meV`면 새 `δ_gas=1 meV`는 통과해야 하지만, 옛 gate가 두 `emol`을 `None`으로 만든 뒤 analyze_results.py:3677에서 `float - None`으로 죽습니다. box20 누락도 `GAS_BOX_NOT_MEASURED`가 아니라 예외로 끝납니다.
Q3 — 전역 스핀 반전 동치
조건부 찬성.
이를 “두 복합체가 같은 전자상태”가 아니라 다음처럼 제한하면 방어 가능합니다.
두 계의 slab-Ni 부호 topology가 전역 시간반전 동치 아래 같은 자기 branch에 속한다.
collinear·무 SOC·무 외부 자기장이고 signed total spin이 구속되지 않았다는 조건이 필요합니다. 이 번들의 `NUPDOWN=-1`은 총 스핀을 고정하지 않는 설정입니다. [VASP NUPDOWN 설명](https://vasp.at/wiki/NUPDOWN)
흡착종에 유의한 spin density가 있으면 Ni 배열만 비교해서는 부족하고, 흡착종–슬랩의 상대 스핀도 비교해야 합니다. 현재 동치는 “슬랩 Ni branch”에만 적용하십시오.
Q4 — stage 1 선결조건
불충분합니다.
현재 네 조건 외에 최소한 다음이 필요합니다.

* `gas_box_delta.pass is true`
* exact pm1 topology가 resolved·usable·same
* 남은 exact-estimand/global closure block이 없음
* 완전한 pre-production root seal이 존재하고 현재 manifest·예정 16잡 전체를 포괄함

현재 analyze_results.py:5327은 `GAS_BOX_DELTA`와 `ESTIMAND_TOPOLOGY_MISMATCH`를 보지 않으므로, 이미 primary estimand가 실패한 뒤에도 `STAGE1_PASS.json`을 쓰고 stage 2를 열 수 있습니다.
미실행 stage-2 provenance를 요구하지 않는 것은 맞습니다. 단, pre-run seal이 미실행 잡의 기대 입력·POTCAR까지 포괄하고 각 후속 실행이 그 seal에 결박돼야 합니다. 현재는 그 결박이 없습니다.
Q5 — 코드가 Methods 문구를 결정하는 것
조건부 찬성.
도구가 검증 상태에 따라 허용 가능한 고정 문장을 고르는 것은 과장 방지에 도움이 됩니다. 다만 필드명과 권한은 `methods_sentence`보다 `methods_candidate` 또는 `allowed_claim`이 맞고, 최종 원고 채택은 사람의 검토를 거쳐야 합니다.
현재 attestation 검증은 fail-open입니다. `FAKE_RELEASE`와 실제 사용 집합에 없는 `UNRELATED` variant 하나만 준 합성 attestation도 `usable:true`가 되고 강한 Methods 문장을 냈습니다. analyze_results.py:2620은 exact variant 집합, ZIP, TITEL·embedded hash, site/time, allowlist·VASP hash의 seal 일치를 요구하지 않습니다.
따라서 현재 생성되는 강한 문구는 사용 금지입니다.
Q6 — 잡 수
잡 수는 일치합니다.

* stage 1: 10잡
* stage 2: 6잡
* 총 16잡

다만 VASP 실행 수는 16회가 아니라 20회입니다. gas parent 네 잡이 각각 relax+static이므로 stage 1은 14회, 전체는 20회입니다.
Q7 — 남은 실행·estimand 차단점

1. P0 — clean-free 설계가 옛 clean-reference gate에 막힙니다.
Manifest에는 clean-slab job이 없지만 analyze_results.py:4448이 모든 magnetic complex에 clean Q reference를 요구합니다. exact pm1/net4 complex가 모두 `MAGNETIC_REFERENCE_INVALID`가 되어 primary D를 낼 수 없습니다. C-12 exact 경로에서는 direct topology 검사가 이 역할을 대신해야 합니다.
2. P0 — pooled 강등이 무관한 차단까지 지웁니다.
Q1의 전체 blocks 재작성 결함입니다. molecular/canary/POTCAR/closure 실패가 사라져 false pass가 가능합니다.
3. P0 — gas 경로가 이중 gate와 독립 이완 때문에 estimand와 다릅니다.
옛 10 meV gate를 제거하고 새 direct `δ_gas`만 hard gate로 삼아야 하며, row 생성은 결측값에도 예외 없이 fail-closed여야 합니다.
4. P0 — stage 1이 실패한 estimand 위에서 stage 2를 엽니다.
`δ_gas`, pm1 topology 및 잔여 exact/global blocks를 선결조건에 추가해야 합니다.
5. P0 — root seal 검증도 fail-open입니다.
analyze_results.py:2583은 `source_sha256`과 `sealed_before_production:true`만 있는 불완전 seal도 받아 `sealed_root_v13`을 발행합니다. schema·manifest·allowlist·assembled hashes·UTC·VASP identity를 모두 필수화하고 실제 실행 바이너리와 결박해야 합니다.
6. P0 — attestation의 exact-set 및 교차 결박이 없습니다.
다음 집합의 완전 일치를 요구해야 합니다.
`attestation variants = root-seal source variants = 실제 16잡 POTCAR_SPEC variants`
각 source SHA, TITEL, embedded hash, manifest·정확한 ZIP SHA, allowlist, VASP path/hash/version, site/UTC도 모두 검증해야 합니다. `made_before_production`은 자기선언이 아니라 산출물 부재 검사로 입증해야 합니다.
7. P0 — runner preflight가 실제 계획 census를 보증하지 않습니다.
run_staged.sh:43은 존재하는 `job.json`만 분류하고 디렉터리 수를 manifest와 비교합니다. job.json 하나를 지워도 `classified=15`, 디렉터리 16로 검사를 통과했습니다. 실행 전에 manifest 파일 해시, exact job set 및 정확한 10/6 분류를 확인해야 합니다.
8. P0 — 실행 lock에 경쟁조건이 있습니다.
한 프로세스가 lock 디렉터리를 만든 뒤 PID를 쓰기 전에 다른 프로세스가 이를 stale로 보고 삭제할 수 있습니다. 다른 HPC 노드의 PID에는 `kill -0`도 유효한 생존검사가 아닙니다. 모르는 lock을 삭제하지 않는 원자적 host/run-id 기반 잠금으로 바꿔야 합니다.
9. P1 — net4 topology 결과가 실제 sensitivity를 막지 않습니다.
analyze_results.py:3847의 `usable_as_sensitivity`는 저장만 하고 읽지 않습니다. topology mismatch여도 `D_net4`가 계산되고 complete로 보고될 수 있습니다. net4 결과와 status를 함께 suppress해야 합니다.
10. P1 — 대안자세는 tier만 있고 estimand가 없습니다.
대안자세 네 잡은 완료 여부만 보고될 뿐 봉인된 exact 식·비교·판정이 없습니다. sensitivity claim에 쓸 것이라면 key·식·gate·status를 정의하고, 아니면 단순 탐색용임을 명시해야 합니다.
11. P1 — 실행·반송 문서가 실물과 충돌합니다.
`MANIFEST.json`은 의존성이 없고 array/run-all을 쓰라고 하면서 다른 문서는 staged 실행을 요구합니다. README는 모든 잡이 static이라고 쓰지만 실제 gas relax가 네 개이고, 존재하지 않는 clean-slab 반송물을 요구합니다. `SUBMIT_CONTRACT.md`는 분석에 필요한 gas `relax/CONTCAR`와 attestation을 누락합니다. 이전 wave 및 `PBE PAW 5.4` 단정도 attestation 정책과 충돌합니다.
12. P1 — “524검사”를 배포본에서 재현할 수 없습니다.
번들 selftest는 UTF-8 환경에서 통과하지만 출력되는 성공 검사는 159건이며, production `_closure_estimand`, staged runner, seal·attestation 스크립트를 실제로 관통하지 않습니다. Windows 기본 인코딩에서는 Unicode fixture 기록 중 실패합니다. 주장한 production-shape e2e를 번들에 포함하고, 개수와 실행 명령을 재현 가능하게 해야 합니다.

제출 해제조건

1. clean-free exact 경로에서 옛 clean-reference gate를 제거하고 direct topology로 대체.
2. master blocks를 보존한 채 primary scope view만 강등하도록 block 구조 수정.
3. box20/24를 공통 내부기하의 static pair로 재생성하고 cross-job geometry/state gate 추가.
4. 옛 조각별 gas gate 제거, 결측·불일치 경로를 예외 없이 구조화된 hard block으로 처리.
5. `δ_gas`, pm1 topology, 잔여 exact/global blocks를 stage-1 prerequisites에 결박.
6. net4 topology 실패 시 `D_net4`와 sensitivity complete를 실제로 차단; 대안자세의 용도·식을 봉인.
7. root seal과 attestation을 exact schema·exact variant set·manifest/ZIP·실행 VASP까지 상호 결박하고 모든 실행에서 필수화.
8. runner가 실행 전에 manifest 해시·exact 16잡·10/6 분류를 검증하도록 하고 lock 경쟁조건 수정.
9. README·SUBMIT·MANIFEST·필수 반송물·실행 횟수·의존성 안내를 실물과 일치시킴.
10. 위 실패 사례를 포함한 production-path e2e를 배포본에서 실행해 fail-closed를 입증.

이 열 조건이 닫히기 전에는 제출하면 안 됩니다. 파일은 수정하지 않았습니다.

