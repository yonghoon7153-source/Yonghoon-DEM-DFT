---
title: "회신 R4 — 조건부 GO: 중성 Stage A 8개 ORCA Opt만 승인, Stage 0·B·hybrid 전부 NO-GO"
date: 2026-08-29
updated: 2026-08-29
tags: [review, codex, sdcp, reopen, stage0, builder, verdict, orca]
status: 접수 — 조건 6 준수 하에 Stage A 착수 가능, P0-2~5 재수정 필요
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-29
verifiedBy: codex
explored: false
authoredBy: human
effort: max
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 회신 R4 (2026-08-29) — 원문 요지 보존

> 요청: `kb/reviews/codex_R4_prompt_doped_reopen_impl2_2026_08_28.md`
> 검증 고정점: **커밋 `096122b`**. 배포 selftest 40건은 UTF-8 환경에서 통과했으나,
> **별도 공격 재현에서 여러 fail-open 확인.**
>
> **판정: 중성 Stage A 8개 Opt 조건부 GO / Stage 0 NO-GO / Stage B NO-GO / hybrid NO-GO.**

## 새로 확인된 위험 4건

1. **adiabatic hybrid 가 최적화 구조를 안 쓴다.** Opt 승자를 골라도 hybrid 입력은
   **원래 vertical XYZ** 로 SP 를 만든다 ⇒ 현재 hybrid 는 "선택된 adiabatic 상태의
   다른 방법 재계산" 이 아니다.
2. **SP 에서 안정했던 determinant 가 Opt 최종구조에서도 안정하다는 보장이 없다.**
   Opt 입력에 `StabPerform` 없음 + 최종구조 재검사 없음. BS 는 SP 단계에서도 안정성
   검사를 면제한다. ORCA 는 UHF/UKS SP 형 계산에 안정성 분석을 지원하므로 **면제에 별도
   근거가 필요**하다.
3. **제출 예시의 neutral XYZ 경로가 시작구조와 충돌한다.** Stage A 시작 XYZ 를
   `--neutral_xyz` 로 되주면 동일 파일 비교로 거부될 수 있고, 같은 디렉터리에서 ORCA 를
   돌리면 최종 XYZ 가 시작구조 증거를 **덮어쓴다**. `*_start.xyz` 와 최종구조 경로 분리 필요.
4. **"4-leg cycle" 증빙과 실제 manifest 가 다르다.** 실제 cycle 은
   `h1a·h1b·h2_s·h2_t·h2_bs·h0` 의 **6항**이고 `h0` 는 계산 ID 가 아니라 receipt 표기다
   ⇒ 주장한 4-leg 결속으로 간주 불가.

## P0별 판정 (전부 불충분)

| 항목 | 판정 | 근거 |
|---|---|---|
| P0-0 관측량 계약 | 불충분 | 입력의 Hirshfeld·UNO/UCO 는 맞다. 그러나 **Löwdin 블록이 없어도 open-shell 잡이 `OK`**, 출력 원자 index 를 무시해 **행 순서가 바뀌면 오분류**, `REMAP_ERROR` 도 정상 class 처럼 수용. **Hirshfeld share 는 계산조차 안 한다.** |
| P0-1 seed 강제 | 불충분 — **단 제출된 8개 산출물은 통과** | 실물 DP6: 8 torsion·8 XYZ 전부 고유, 최소 dmin 2.04 Å. 그러나 `--allow_underseed` 로 1-seed manifest 를 만들 수 있고 **Stage B 가 그걸 거부하지 않는다.** 문서와 달리 `cands[:1]` 폴백이 **소스에 남아 있다.** |
| P0-2 부모 receipt | 불충분 | `--allow_unverified_parent` 우회 존재. 선택 seed 의 **시작 XYZ 와 receipt 를 결속하지 않는다.** 다른 seed 재라벨링·comment 만 바꾼 미이완 구조·**심지어 UHF·+1·doublet 출력까지 neutral RKS 부모로 통과**. method·charge·multiplicity·입력 SHA 검사 필요. |
| P0-3 dependency | 불충분 | 생성된 `depends_on` tuple 자체는 정확. 그러나 analyzer 가 SP 를 중복출력으로 나중에 `GATED` 해도 **이전의 `OK` 가 dependency map 에 남아** 종속 Opt 를 `OK` 로 승인. **최종 gate 후 dependency map 재구성** 필요. |
| P0-4 analyzer | 불충분 | charge/multiplicity echo 가 **아예 없어도 통과**. 임의의 `stability analysis indicates …` 문자열을 stable 증거로 인정. BS SP 는 안정성 검사 면제. localization 누락 통과. **출력에 주석 한 줄만 추가하면 중복검사 우회.** |
| P0-5 hybrid | 불충분 | 조성별 그룹 분리는 고쳐졌다. 그러나 **adiabatic winner 최종구조를 버리고 vertical XYZ 로 hybrid SP**. 비교기는 **한쪽이 비어도 성공**하고 같은 sector 안에서 localization/state 가 달라져도 "일치". **method 가 selection group key 에 없어** 혼합 가능. |

## Localization 규칙 판정 — 0.5/0.3 은 라우팅 기준으로만 조건부 수용

확정 기준으로는 부족. 보완 6:
- **연속 share 원값 보존**, threshold 적용 전 반올림 금지.
- 0.4/0.5/0.6 **경계 민감도 기록** — 바뀌면 `THRESHOLD_DEPENDENT`.
- 현재 `backbone` 은 여러 ring 을 한 집합으로 합쳐 **어느 ring 의 polaron 인지 구별 못 한다** ⇒ ring 별 집합 필요.
- **BS 는 양·음 lobe 가 signed sum 에서 상쇄**된다 ⇒ 양·음 위치를 별도 분류.
- **Löwdin·Hirshfeld 둘 다 계산.** 두 partition 이 다르면 억지 선택 금지 —
  `PARTITION_DEPENDENT` 또는 `MIXED_UNRESOLVED`.
- 예상 open-shell 의 `NO_SPIN`·누락 블록·remap 오류는 class 가 아니라 **hard gate**.

⇒ **Löwdin 을 primary label 로 쓰는 것은 가능. 단 Hirshfeld 병기와 partition 일치 확인
없이 "localization class 가 검증됐다" 고 말하면 안 된다.**

## Stage A 실행 판정 — 실물 DP6 재생성으로 확인

- 8 seed · torsion vector 8개 · XYZ hash 8개 **전부 고유**
- 각 구조 `C66H86O36S12`, **200 atoms, 962 electrons**
- 전 접합 **dmin ≥ 2.04 Å**
- 입력 전부 `RKS r2SCAN-3c Opt TightSCF Hirshfeld`

**정확히 이 8개 중성 Opt 만** 아래 조건으로 착수 가능:

1. 현재 8개의 **manifest·INP·XYZ SHA256 을 동결**하고 재생성하지 않는다.
2. **모든 `--allow_*` 우회 옵션 사용 금지.**
3. 정본 입력은 **읽기 전용 보존**, 계산은 **seed 별 별도 scratch 복사본**에서.
4. **시작 XYZ·INP·OUT·최종 XYZ 를 서로 다른 파일로 보존** + SHA256·ORCA 버전·실행 명령 기록.
5. `builder_commit` 만 믿지 말고 **builder 파일 자체의 SHA256** 도 기록.
6. **이 결과로 현재 receipt 를 통과시켜 Stage B 를 열지 않는다.**
   P0-2~5 수정 후 **실제 Stage A 산출물로 다시 심사.**

> ⚠ 이 8개는 서로 다른 시작 conformer 이지 **통계적으로 독립인 8개 반복측정이 아니다.**

## 최종 판정

- 중성 Stage A 8개 Opt: **조건부 GO**
- 전체 Stage 0: **NO-GO**
- Stage B 생성·실행: **NO-GO**
- hybrid 생성·비교: **NO-GO**

## 다음 제출에 반드시 넣을 회귀시험 6

교차-seed/wrong-state receipt · localization 누락·행 재배열 · duplicate→dependency ·
BS 안정성 · adiabatic 최종구조 hybrid · 빈 method 비교.

---

## 우리 쪽 처리 (2026-08-29)

- selftest 40건의 성격이 R2→R3 와 **같은 방식으로** 한 번 더 부족했다: 정상 경로는
  증명하지만 **공격 경로를 안 만든다.** R3 가 "실행해 봤다" 로 잡았고 R4 는 "공격을
  재현했다" 로 잡았다 — 다음 selftest 는 **공격 사례를 fixture 로 갖고 있어야** 한다.
- 착수 가능한 것은 **데스크탑 ORCA 8잡**뿐이다. GPU 자원(kgy·gabia)과 경합하지 않는다.
- Stage B 를 여는 열쇠는 계산이 아니라 **P0-2~5 재수정 + 회귀시험 6**이다.
