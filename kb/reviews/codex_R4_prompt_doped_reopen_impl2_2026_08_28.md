---
title: "Codex 회신 R4 요청 프롬프트 — R3 P0 전건 구현 재제출 (receipt·analyzer·계약 증빙)"
date: 2026-08-28
updated: 2026-08-28
tags: [review, codex, sdcp, reopen, stage0, prompt]
status: 회신 수령 — `kb/reviews/codex_R4_doped_reopen_impl2_reply_2026_08_29.md`
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 회신 R4 요청 — R3 의 P0 전건 + GO 요건 9 구현 재제출

---

## 붙여넣을 프롬프트

```
당신은 계산재료 리뷰어다. 회신 R3 에서 실측 fail-open 5건과 관측량 회수 계약 P0,
GO 재심사 요건 9 를 지적했다. 전건 구현했다. **여전히 계산 0.** 재심사해 달라 —
Stage 0 GO / 조건부 GO / NO-GO 명시. 커밋은 발송 시점 HEAD.

[P0 별 구현]
P0-0 관측량 계약: 전 입력에 Hirshfeld, open-shell 에 UNO UCO (RKS 는 Hirshfeld 만).
  localization class 는 **사전 규칙**을 manifest 에 고정: share(g)=Σ_i∈g m_i / Σ_i|m_i|
  (Löwdin), |share|>=0.5 인 집합이 유일하면 그 라벨, 아니면 MIXED_UNRESOLVED,
  Σ|m|<0.3 이면 NO_SPIN. 중성→doped index remap 이 class 산출 경로에 내장되고 원자수
  불일치는 게이트. analyzer 가 실제로 class 를 산출한다 (합성 Löwdin 블록 e2e 2종).
P0-1 seed 강제: 바닥 미만(--seeds 1)·음수·고유성 부족(step 조대)·dmin<2.0 Å 전부
  SystemExit. cands[:1] 폴백 제거. 접합별 dmin 을 manifest 에 기록.
P0-2 부모 receipt: stage B 는 --stage_a_manifest + --neutral_out + --neutral_xyz 3중 결속.
  검증: manifest 의 gseed 존재(재라벨 거부) · strict decode · 마지막 segment 정상종료 ·
  **THE OPTIMIZATION HAS CONVERGED** · .out 마지막 CARTESIAN 블록 == xyz (원소+1e-4 Å) ·
  stage A 조립본과 sha 동일이면 거부. receipt 에 out/xyz sha·마지막 FINAL SP(=h0)·
  Program Version·stage A calculation_id 가 박힌다.
P0-3 dependency: opt 잡에 depends_on = 같은 (parent,pattern,sector,gseed,scf_seed,method)
  sp 의 calculation_id. analyzer 가 선행 sp 가 OK 아니면 DEPENDENCY_NOT_MET emit.
P0-4 analyzer: 마지막 run segment · findall[-1] (에너지·<S2>·HFTyp) · 양성증거 요구
  (에너지 없음→게이트 · HFTyp/charge/mult echo 대조 · sp 는 stability 수행+stable 필수,
  없으면 STABILITY_UNVERIFIED · 대소문자 불문 unstable → STABILITY_UNSTABLE ·
  opt 는 수렴 문구 필수 → OPT_UNCONVERGED) · BS <S2> 창 [0.2,1.5] 밖(미플립 2.0 포함)
  NA_STATE_NOT_IDENTIFIED · 동일 .out 복사 → DUPLICATE_OUTPUT (realized_state_id 는
  calc_id+out_sha 라 재사용 불가) · strict decode → OUTPUT_UNREADABLE ·
  all-PENDING 은 exit 3 (완료 분석 아님).
P0-5 hybrid: hybrid_select 는 (species, job_type) 그룹 **안에서만** 승자/창/class 대표 —
  h1(961e)/h2(960e) 절대에너지 혼합 불가. --hybrid 가 decision set 의 입력을 실제 생성,
  fresh-start 는 **! ... NoAutoStart** 키워드. --compare 가 두 분석의 그룹별 승자를 대조해
  METHOD_DEPENDENT 를 emit (P1 지적의 emit 경로).
P1: stage A 잡에 calculation_id·xyz sha·builder commit / 중첩 realized 도 ID 발급 거부 /
  레거시는 --legacy 명시 필수.

[증빙 1 — 실물 다이머 stage A, n=6, **바닥 8 seed 강제 통과**]
  gs0: torsions [130, 80, 30, 150] · dmin(접합별) [2.509, 2.509, 2.509, 2.509] · calc calc_ff188e5598dc72ef
  gs1: torsions [280, 210, 150, 270] · dmin(접합별) [2.04, 2.488, 2.509, 2.509] · calc calc_d56a5a02e99baa3c
  gs2: torsions [150, 120, 260, 200] · dmin(접합별) [2.337, 2.131, 2.509, 2.421] · calc calc_15d7217f9f1236bc
  … (총 8 seeds — 전부 고유 torsion 벡터, 전 접합 dmin >= 2.04 Å, manifest 에 기록)
  underseed_flag=false · builder_commit 기록 · closed_form_validated=true

[증빙 2 — selftest 40건 중 R3 요건 9 대응 발췌]
  ✓ stage A: 고유 torsion + 전 접합 dmin≥2.0 기록 ([60]/[30] · dmin [2.957])
  ✓ neutral 입력: RKS Opt + Hirshfeld (RKS 라 UNO 없음) — R3 P0-0 회수 계약
  ✓ 음성: 부모 = stage A 조립본과 동일 → 미이완 재사용 거부 (R3 P0-2)
  ✓ 음성: manifest 에 없는 gseed 재라벨링 → 거부
  ✓ 음성: receipt 인자 없이 stage B → 거부 (자유문구는 증거가 아니다)
  ✓ receipt: 수렴·최종에너지(마지막 값)·버전·해시·stage A calc_id 결속
  ✓ sp 입력: UKS SP + StabPerform + Hirshfeld + UNO UCO (R3 P0-0)
  ✓ 음성: 전 잡 PENDING → 완료 아님, 비영 종료 (3)
  ✓ 음성: 동일 .out 복사 → DUPLICATE_OUTPUT (realized ID 재사용 봉쇄)
  ✓ 음성: 대문자 UNSTABLE 도 잡는다 (re.I)
  ✓ 에너지는 **마지막 값** (-2.0, 첫 값 -1.0 아님)
  ✓ 음성: 선행 sp GATED(불안정) → opt DEPENDENCY_NOT_MET (R3 P0-3)
  ✓ localization class: 분산 스핀 → MIXED_UNRESOLVED (사전 규칙)
  ✓ hybrid: 조성(h1/h2)별 그룹 분리 — 서로의 0.10 eV 창에 안 섞인다 (R3 P0-5)
  ✓ hybrid 입력: NoAutoStart 키워드로 fresh-start 강제 (주석 아님)
  ✓ n=3 은 pair 없음 → cycle 0 (정합)
  ✓ U_PCET cycles: CD/BE/BC × vert/ad = 6, 4-leg calc_id 결속 · A,F 제외 (R3 조건 9)
  ✓ h2 RKS 후보: RKS + Hirshfeld (UNO 는 UHF 전용이라 제외)

[증빙 3 — 입력 계약 원문 (합성 부모 시연 stage B)]
sp:  ! UKS r2SCAN-3c TightSCF Hirshfeld UNO UCO   + %scf StabPerform true end
s:   ! RKS r2SCAN-3c TightSCF Hirshfeld           (RKS 라 UNO 없음)
bs:  ! UKS r2SCAN-3c TightSCF Hirshfeld UNO UCO   + %scf BrokenSym 1,1 end (mult 3)
opt: ! UKS r2SCAN-3c Opt TightSCF Hirshfeld UNO UCO
hyb: ! UKS wB97X-D3 def2-TZVP defGrid3 NoAutoStart TightSCF Hirshfeld UNO UCO

[정직 한계]
- 실물 stage B/analyzer 는 여전히 없다 — 정의상 ORCA Opt 부모가 생겨야 존재한다.
  receipt 정상 경로는 좌표 일치까지 재현한 합성 .out 으로 e2e 했다 (증빙 2).
- BLA·participation ratio·UNO 점유수 산출은 미구현 (class 는 Löwdin 국소스핀 경로만) —
  R3 가 후속 유예를 허용한 시각화/정교화 범위로 이해했다. 아니면 지적해 달라.
- adaptive stopping 은 자동화 대신 SEED_FLOOR 규칙 + null-batch 를 불변 로그(manifest)로
  사람이 집행한다 (R3 이 P1 로 허용한 방식).

심사 요청:
1. P0-0~5 각각 충분/불충분.
2. localization class 규칙(0.5/0.3, Löwdin 경로)이 사전 규칙로 충분한가 — Hirshfeld 쪽
   share 도 병기해야 class 로 인정되나?
3. 실물 stage A(증빙 1)로 stage A 실행 승인이 되나 — 즉 **중성 8개 ORCA Opt 시작** 허가?
   (stage B 는 그 부모 receipt 가 생긴 뒤 재확인 제출)
4. 전체 판정: Stage 0 GO / 조건부 GO(stage A 만) / NO-GO.
```
