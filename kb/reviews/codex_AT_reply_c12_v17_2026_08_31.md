---
title: "회신 AT — C-12 v17 NO-GO (P0 5건 · 해제조건 9)"
date: 2026-08-31
updated: 2026-08-31
tags: [review, codex, sdcp, c12, vasp, verdict, no-go]
status: 이행 완료 — v18 로 재제출 (AU)
kind: review-reply
system: sdcp
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-31
verifiedBy: codex
explored: false
authoredBy: agent
claimType: prescriptive
evidenceScope: multi-source-primary
---

> 요청: `kb/reviews/codex_AT_prompt_c12_v17_2026_08_31.md`
> **판정: NO-GO — v17 은 VASP 를 한 잡도 돌리기 전에 재생성해야 한다.**
> 무결성은 정상 (ZIP/MANIFEST 해시 일치 · payload 110/110 · selftest 실측 **257/257**,
> 문서의 245 는 낡음).

## P0 — 제출 차단 5건

1. **SDCP 기체 3잡이 계산 전부터 영구 게이트.** `job.json` 의 `mol_graph_canonical`
   이 POSCAR 의 O S C H 종별 재정렬에 맞게 remap 되지 않았다. 리뷰어가 배포본에서
   `geometry_audit()` 를 직접 돌린 결과: box20/box24/box24__nzmag 모두
   **canonical 36 · broken 28 · formed 28** → `SOURCE_TOPOLOGY_CHANGED` hard gate.
   VASP 가 완벽히 끝나도 SDCP 기체 에너지가 사용 불가라 stage 1 과 최종 판정이
   성공할 수 없다.
2. **새 dense 두 상의 INCAR 감사가 fail-open.** `incar_expected.static` 만 있고
   `.dense` 가 없다. dense OUTCAR 가 ENCUT=400 · IVDW=0 · ISPIN=1 · LDAU=F ·
   ICHARG=2 여도 phase INCAR gate 가 비어 있고 그 E0 가 δ_k 에 들어간다.
   `incar_expected.dense` 와 exact k-mesh/shift 감사를 추가해야 한다.
3. **기존 POTCAR/provenance 를 독립 검증 없이 신뢰.** `SEAL_POTCAR_ROOT.sh` 는
   기존 provenance 의 allowlist SHA 만 맞으면 재조립하지 않는다. 가짜 POTCAR 와
   자기일관적인 가짜 provenance 를 미리 두고 PP 원본이 없게 해도 seal 생성이
   성공했다. 매번 PP 원본 SHA·TITEL·allowlist membership·실제 조립 POTCAR SHA 를
   독립 재계산해야 한다.
4. **기존 seal 과 attestation 도 여전히 fail-open.** 위조 schema · 문자열형
   `sealed_before_production` · evidence/time 변조를 놓친다. attestation 필수 필드에
   `schema` 가 없다. root seal 이 없어도 임의 release label 과 비정상 hash 를 넣은
   attestation 이 `usable=true` 와 강한 Methods 후보로 도달했다.
5. **실행 경로와 문서가 서로 모순.** README·SUBMIT 는 `VASP_CMD` 를 쓰는데 runner 는
   즉시 거부한다. 필수인 `EXPECT_ZIP_SHA256` 이 문서에 없다. 또한 임의
   `VASP_LAUNCHER` 가 뒤의 sealed executable 을 무시할 수 있고, TERM trap 이 lock 만
   지우고 runner 는 계속 실행하며, attestation maker 가 bundle-global lock 에
   참여하지 않고, README 의 수동 `run_job.sh` 경로가 binary seal 과 global lock 을
   우회한다.

## Q1–Q6

- **Q1** 셀 한정 문구는 허용, D3-off 추가는 반대. "공통 주기영상 항이 상당 부분
  소거된다" 근거는 **삭제**. 두 primary complex 의 slab 원자가 48/192 로 다르고 최대
  변위 약 0.296 Å. 거리도 구분: primary b00 SDCP **4.894** · PTFE **5.646**;
  4.613 은 SDCP **대안 b12 의 worst case**. IVDW=11 은 pairwise D3 zero-damping 이고
  기존 OUTCAR 의 Edisp 네 항으로 총 D3 기여를 계산할 수 있으므로 신규 D3-off 잡 불필요.
- **Q2** 개별 5 meV 셋만으로는 부족. 세 축은 독립 확률오차가 아니므로 **RSS 금지**,
  모두 같은 방향이면 최대 15 meV. `B_num = |Δ_vac| + |δ_gas| + |δ_k| ≤ 5 meV` 일 때만
  0.01 eV 안정성 주장.
- **Q3** 의존성은 맞으나 병렬 runner 는 조건부 — 코어·메모리가 실제 배정되고 각 step 이
  격리돼야 한다. 아니면 기본 병렬도 1 이 안전. seal·attestation·runner 가 같은 lock
  protocol 에 참여해야 한다.
- **Q4** 서명된 외부 checksum 이 적절 (detached-signed SHA256SUMS · signed tag ·
  minisign/GPG/cosign). runner 는 ZIP 경로를 직접 받아 해시해야 한다.
- **Q5** pooled 완전성 엄격화는 맞으나 불충분. **권장: pooled minimum 과 secondary_G 를
  영구 diagnostic/noncitable 로 유지 — 추가 잡 0.**
- **Q6** 좁은 primary estimand 에는 신규 VASP 잡이 필수가 아니다. 한정 문구:
  *"사전등록한 18.272×11.512 Å² lateral cell, 1 fragment/cell(0.5009 nm⁻²),
  fixed geometry, pm1, PBE+U+D3 protocol 에서의 differential complex–gas reference
  energy 이다. 잔여 lateral-size/coverage dependence 는 추정하지 않았으며, 고립
  흡착·평형 결합·실제 전극 피복률로 일반화하지 않는다."*

## 재제출 해제조건 9

① 기체 3잡 graph remap 후 배포 POSCAR/job.json 에 계산 전 geometry audit 0/0
② `incar_expected.dense` 와 exact mesh/shift gate ③ POTCAR 를 매번 PP 원본에서
독립 재검증·재조립 ④ seal/attestation exact schema·boolean·hash·root 결박
⑤ launcher 까지 봉인하고 실행 직전 executable receipt ⑥ runner·SEAL·MAKE 공통 lock 과
TERM/INT 종료 ⑦ README/SUBMIT 를 실제 runner 계약과 일치·수동 우회 삭제
⑧ 낡은 E_ads/dE_site claim policy 삭제, 세 수치축 합산 예산과 pose 해석 규칙 사전등록
⑨ 위 공격 fixture 를 배포 selftest 에 추가한 새 ZIP 재봉인
