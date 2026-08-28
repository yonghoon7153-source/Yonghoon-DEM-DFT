---
title: "Codex 회신 R3 요청 프롬프트 — 최소수정 8 구현 재제출 (실물 .inp·manifest·음성 e2e 첨부)"
date: 2026-08-28
updated: 2026-08-28
tags: [review, codex, sdcp, reopen, stage0, prompt]
status: 발송 대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 회신 R3 요청 — R2 최소수정 8 의 구현 증빙 재제출

R2 요구 그대로 **생성된 실제 .inp · manifest · 음성 e2e** 를 첨부한다.
빌더는 stage A/B 아키텍처로 재작성됐다 (tools/sdcp/build_v7c_trimer.py, 발송 시점 HEAD 고정).

---

## 붙여넣을 프롬프트

```
당신은 계산재료 리뷰어다. 회신 R2 에서 v3 카드와 빌더 실물의 불일치(P0 6건)와 재승인
최소수정 8 을 지적했다. 빌더를 2단계(stage A/B) 아키텍처로 재작성해 여덟을 구현했다.
**여전히 계산 0.** 아래 실물 산출로 재심사해 달라 — Stage 0 GO / 조건부 GO / NO-GO 명시.

[최소수정 8 구현]
1. 2단계 빌드: --stage a = 다이머 -> geometry seed 별 중성 조립 + RKS Opt 입력만.
   ORCA Opt 후 --stage b = 최적화 부모(R0)에서 R0-H vertical 기하 · sp_vertical(SP+
   StabPerform) · opt_adiabatic 생성. runner_rule: opt 는 같은 (pattern,sector)의 sp 가
   analyzer 게이트를 통과한 뒤에만. 부모 xyz 에 ORCA 마커 없으면 경고.
2. RKS/UKS · SP/Opt job type 명시 생성 (아래 실물 .inp 4종).
3. REQUIRED_MATRIX 강제: dp6 = singles B,C,D,E + pairs C,D / B,E / A,F / B,C(off-center).
   부분 생성은 SystemExit (--allow_partial 은 '시험 전용, 재심사 제출물 아님' 명시).
   U_PCET 쌍이 요구하는 singles 누락도 SystemExit.
4. fail-closed: 비정본 다이머 조성 -> SystemExit (--allow_noncanonical 은 selftest 전용).
   닫힌꼴 불일치·위상 불일치·parity 불일치 전부 즉시 중단.
5. analyzer (--analyze): abort code 7종 실제 emit (SCF_UNCONVERGED · SECTOR_MISMATCH
   (HFTyp/<S2>) · SPIN_CONTAMINATION_UNREPORTED · NA_STATE_NOT_IDENTIFIED(BS 플립 실패)
   · STABILITY_UNSTABLE 등). 음성 e2e 4종 + 양성 1종이 selftest 에 있다.
6. geometry seed = max-dmin 후보군(DMIN_FLOOR 2.0 A)에서 결정론 LCG 선택 (--step 은
   seed 아님 명시). SCF seed s0/s1(Hueckel) 분리. calculation_id = conditioning 만의
   sha256 16자 (realized 필드 유입 시 발급 거부 — selftest 로 봉인). realized_state_id
   는 analyzer 가 사후 발급.
7. U_eff -> U_PCET(a,b) = E[h2(a,b)]+E[h0]-E[h1(a)]-E[h1(b)] 개명. manifest 에 '순수
   Hubbard U 아님(핵 조성 변화)' + vertical/adiabatic 분리·혼합 금지 명시.
8. hybrid_select(): vertical 승자 ∪ adiabatic 승자 ∪ 0.10 eV 창 ∪ realized localization
   class 별 최저 대표 전부. 입력은 wB97X-D3/def2-TZVP/defGrid3 fresh-start (MORead 금지
   주석). R2 Q2/Q3/Q4 반영: hBC off-center 추가 · A,F 는 섹터 비교 전용(U/추세/일반화
   주장 금지, 승격 규칙 명시) · h1 도 R0-H 공통부모 4-leg · seed floor DP3/4 = 4+2xK2,
   DP6 = 8+4xK2, --step 제외, 변화 시 null counter 리셋.

[실물 증빙 1 — stage A: 실물 다이머, n=6 (시연으로 seed 2개만; 승인 바닥은 8)]
manifest_stage_a.json 발췌:
  schema sdcp_stage0_manifest/v3 · estimand sdcp-doped-gas-stage0/v3
  design_card kb/questions/sdcp_doped_reopen_v3_2026_08_28.md
  closed_form_validated True · dp 6
  geometry_seeds: g0 torsions [130, 80, 30, 150] /
                  g1 torsions [280, 210, 150, 270]   (독립)
gs0/dp6_gs0_neutral.inp 전문:
! RKS r2SCAN-3c Opt TightSCF
%maxcore 6000
* xyzfile 0 1 dp6_gs0_neutral.xyz

[실물 증빙 2 — stage B 산출 .inp 4종 전문 (매트릭스 8패턴 · 잡 56)]
(hCD closed-shell 후보 · SP)
! RKS r2SCAN-3c TightSCF
%maxcore 6000
%scf StabPerform true end
* xyzfile 0 1 dp6_gs0_hCD.xyz
(hCD triplet · SP · SCF seed s1)
! UKS r2SCAN-3c TightSCF
%maxcore 6000
%scf StabPerform true Guess Hueckel end
* xyzfile 0 3 dp6_gs0_hCD.xyz
(hCD BS · SP)
! UKS r2SCAN-3c TightSCF
%maxcore 6000
%scf BrokenSym 1,1 end
* xyzfile 0 3 dp6_gs0_hCD.xyz
(hB doublet · adiabatic Opt)
! UKS r2SCAN-3c Opt TightSCF
%maxcore 6000
* xyzfile 0 2 dp6_gs0_hB.xyz

[실물 증빙 3 — manifest_stage_b 잡 레코드 예 (hCD bs sp s0)]
{
 "tag": "dp6_gs0_hCD_bs_sp_s0",
 "calculation_id": "calc_cc5b8d10b2630436",
 "conditioning": {
  "estimand_id": "sdcp-doped-gas-stage0/v3",
  "dp": 6,
  "species": "DP6_h2_Q0",
  "pattern": "C,D",
  "removed_H_indices": [
   90,
   123
  ],
  "sector": "bs",
  "wavefunction_class": "UKS-BS",
  "orca_mult": 3,
  "n_alpha_minus_beta": 0,
  "net_charge": 0,
  "all_electron_count": 960,
  "job_type": "sp_vertical",
  "geometry_seed": "g0",
  "scf_seed": "s0",
  "parent_neutral_sha256": "bb61c88b3f2d9496957ca152e245defdecb002a1bec3a1b75f0afbb9f8f956ee",
  "method": "r2SCAN-3c/TightSCF"
 },
 "expected": {
  "hf_type": "UHF",
  "s2_target": "report_required"
 },
 "seeded_separation": 1
}

[실물 증빙 4 — 음성 e2e (selftest 실행 출력 발췌 — 총 27건 PASS)]
  ✓ 음성: 비정본 다이머 + 플래그 없음 → stage A 거부 (fail-closed)
  ✓ 음성: --patterns 부분 지정 + allow_partial 없음 → 생성 실패 (fail-open 봉쇄)
  ✓ 음성: conditioning 에 realized 필드가 섞이면 ID 발급 거부
  ✓ analyzer 음성①: 미종료 → SCF_UNCONVERGED emit
  ✓ analyzer 음성②: triplet 기대인데 <S2>=0.76 → SECTOR_MISMATCH
  ✓ analyzer 음성③: bs 인데 <S2> 미보고 → SPIN_CONTAMINATION_UNREPORTED
  ✓ analyzer 음성④: RKS 요청인데 UHF 로 돎 → SECTOR_MISMATCH
  ✓ analyzer 양성: 정상 triplet → OK + realized_state_id 발급 (calc_id 와 분리)
  ✓ analyzer: 불안정 파동함수 → STABILITY_UNSTABLE (opt 차단 마크)
  ✓ 음성: 닫힌꼴 함수가 틀린 조성 거부

[정직 한계 — 남은 미구현 (카드에도 명시)]
- stage B 시연은 미이완 부모로 만든 것이다. 2단계 규약상 실물 stage B 는 ORCA Opt
  후에만 존재 가능하다 (그것이 규약 그 자체다). 실행은 하지 않았다.
- carrier_localization_profile 의 수식·정규화·class 경계·index-remap validator (R2
  조건 4 P1)는 미구현 — analyzer 는 게이트(수렴·섹터·오염·안정성)까지다.
- adaptive stopping 자동화·Yamaguchi AP 산출 미구현. 전부 docstring '못 하는 것' 등재.

심사 요청:
1. 최소수정 8 각각 — 구현 충분/불충분 (불충분이면 무엇이 빠졌나).
2. 조건 4 P1(프로파일 수식·remap validator)을 Stage 0 **실행 전** 요구로 승격하나,
   회수 분석 단계까지 유예 가능한가?
3. 시연 stage B(미이완 부모)로 파이프라인 증빙이 되나, 아니면 GO 를 '조건부 — 실제
   Opt 부모의 stage B manifest 재확인' 으로 걸겠나?
4. 전체 판정: Stage 0 GO / 조건부 GO / NO-GO.

형식: 항목별 P0/P1/P2 + 근거. 동의는 "동의" 한 줄.
```
