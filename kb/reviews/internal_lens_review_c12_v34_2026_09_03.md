---
title: "내부 6렌즈 리뷰 — C-12 v34 (발송 전 마지막 리뷰) · NO-GO → v35"
date: 2026-09-03
updated: 2026-09-03
tags: [review, sdcp, c12, vasp, handoff, kconv, attestation, prereg, governance]
status: 진행
kind: review
system: sdcp_c12
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-03
verifiedBy: "P0 두 건을 코드·비준 문서 원문에서 재확인 · v35 배치(c7fdc58e · 271a7357) selftest 437/437 · verify 30/30 · e2e 15/15"
explored: true
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
verdict: "NO-GO — v34 발송 불가 · v35 필요 (P0 2건: 선택 attestation 함정 · δ_k 설계 제외의 비준 이탈/재개 조건 충돌)"
---

# 내부 6렌즈 리뷰 — C-12 v34 (2026-09-03)

> 1저자 지시 "마지막으로 리뷰 받아봐봐" 에 따라 v34 번들(`runs/sdcp_c12_2026_08_30/sdcp_c12_v34.zip` ·
> 생성 커밋 2382b6d5)을 서로 모르는 6개 렌즈로 나눠 독립 감사했다. 렌즈 2·4·5 가 완료 보고를 냈고,
> 렌즈 1·3·6 은 API 과부하(529)로 4회 재개에도 최종 보고를 내지 못했다 (§6).
>
> **판정: NO-GO.** 세 렌즈(2·4·5)가 서로 모르고 같은 결론에 닿았다 — δ_k 설계 제외의 근거 인용이 틀렸고
> (사전등록 49행 ≠ 적용 조항 50행) 재개 조건이 비준 프로토콜 §7·§8 과 정반대다. 렌즈4 는 코드에서 실제 결함
> (선택 attestation 이 실물에서 항상 1단계 게이트를 막는다)을 찾았고 내가 코드 세 곳에서 재확인했다.

## 1. 렌즈 구성과 판정

| 렌즈 | 관점 | 판정 | 상태 |
|---|---|---|---|
| 1 | SEAL VASP 프로브 실물 타당성 (빈 INCAR·토큰 규칙·timeout) | — | 미완 (529 ×4) · §6 에 내 자체 점검 |
| 2 | `--no_kconv` 재분석 e2e (합성 16잡 반송 → 분석기) | **NO-GO(거버넌스)** | 완료 |
| 3 | 러너 stub e2e (메일 실행블록 9변수 그대로) | — | 미완 (529 ×4) · §6 |
| 4 | 문서 정합성 (메일·README·SUBMIT·ATTREQ·MANIFEST·비준 문서) | **NO-GO** | 완료 |
| 5 | 감사 사슬 (IDENTITY·MANIFEST·비준 digest·원장) | GO-with-P1 | 완료 (컴팩션 이전 회신) |
| 6 | 아무도 안 본 곳 (fresh) | — | 미완 (529 ×4) |

## 2. P0 — 발송 전에만 깨끗하게 고칠 수 있는 것

### P0-1 (렌즈4 · 코드 재확인) 선택 attestation 이 실물에서 **항상** 1단계 게이트를 막는다
- `MAKE_POTCAR_ATTESTATION.sh` 는 `vasp --version` 의 stdout **전문**(여러 줄)을 번들 루트에서 받아
  `vasp_version_raw` 에 적었다. v34 의 SEAL(회신 BH P0-1 반영)은 `vasp.<버전>` **토큰만** 봉인한다.
  분석기는 `raw not in banner` 로 비교했다 — 긴 문자열이 짧은 토큰의 부분문자열일 수 없으므로
  `ATTESTATION_VASP_VERSION_MISMATCH` → `potcar_identity` 차단 → 2단계가 열리지 않는다. 1단계 ~111 h 를
  태운 뒤에야 드러난다. 픽스처는 방향이 반대(banner 가 더 김)여서 425/425 가 통과했다.
- 덧붙여 MAKE 는 번들 루트에서 VASP 를 기동하므로 OUTCAR 가 남아 SEAL 이 "생산 산출물이 이미 있다" 로
  거부할 수 있었다. 문서 어디에도 "있으면 막힐 수 있다" 는 말이 없었고 ("없어도 러너는 돕니다"),
  post_hoc 정책에서는 러너가 증서를 생산 전에 검사하지도 않았다.
- **v35 조치 (c7fdc58e)**: MAKE 프로브를 SEAL 과 같은 절차(임시 폴더 + 빈 INCAR + 토큰 regex, 토큰 없으면
  증서를 만들지 않음)로 · 분석기는 양쪽 토큰 비교(`ATTESTATION_VASP_VERSION_UNREADABLE` 추가) · post_hoc 이라도
  증서가 있으면 러너가 생산 **전에** `--check_attestation` 으로 검증 · 픽스처를 실물 방향으로 + 회귀 3건 +
  e2e(MAKE → 러너 → --check_attestation).

### P0-2 (렌즈2 · 4 · 5) δ_k 설계 제외의 근거 인용 오류 · 비준 기록 부재 · 재개 조건이 프로토콜과 정반대
- 사전등록(비준 2026-09-02) `3_오차예산`: 49행 "넘으면: 값을 버리지 않는다…" 는 **문턱 초과** 절, 50행
  "축이_하나라도_없으면: NUMERIC_BUDGET_INCOMPLETE" 가 **축 부재** 절이다. v32–v34 의 MANIFEST·분석기·생성기는
  49행을 근거로 δ_k 를 `axes_not_designed` 로 보내 차단하지 않았다 — 적용 조항은 50행이고, 이 예외는
  `decisions.json`·`status_history` 어디에도 없다. 번들 자신의 규칙("비준되지 않은 번들은 해석을 시작하지
  않는다")에 걸린다.
- 재개 조건 "|ΔE_ads| < 50 meV 이면 dense 2잡 추가" 는 비준 프로토콜 §7("최종 대비 |D| < 0.05 eV → 미해결")·
  §8("미해결이면 계산을 확장하지 않고 Figure 2e 패널을 뺀다") 과 **같은 문턱에 반대 행동**이다. 실행 경로도 없다
  (dense 입력 없음 · MANIFEST 변경 = 봉인 불일치 · `--merge` 키 충돌).
- **v35 조치 (271a7357)**: 설계 제외의 근거와 재개 조건을 **비준 사전등록 항**(`3_오차예산.축_설계_제외_*`)에서
  읽는다. 생성기 `--no_kconv` 는 그 항이 없으면 만들지 않고, 있으면 재개 조건을 그대로 MANIFEST 로 복사한다.
  분석기는 번들 사전등록 사본에서 같은 항을 요구한다 (`KCONV_OMISSION_UNRATIFIED` / `_DRIFT` / `_UNDECLARED`
  차단 · δ_k 결측으로 50행 적용). 재개 조건은 기계 평가 구조(판정량 `D_raw_eV` · 문턱 · 비교 · 충족시)로만
  선언되고 결과에 `reopen_eval` 로 남는다. preflight(`--check_governance`)도 같은 정적 조건을 판정한다.
  **⚠ 사전등록 개정 자체는 1저자 결정·비준 사항이다 (§5).**

## 3. P1 (v35 에서 고쳤다)
- 렌즈2 P1-1 `kconv_pair.status=not_applicable` 이 primary 조각 2개여도 조용히 통과 → `KCONV_STATUS_INVALID`.
- 렌즈2 P1-2 재개 조건이 문장뿐, 어느 값(D_raw? rounded?)에 대는지 미특정 → 구조 필드 + `reopen_eval`.
- 렌즈2 P1-3 `KCONV_OMISSION_UNDECLARED` 가 최종 분석에서만 → preflight.
- 렌즈2 P1-4 문서 "0.01 eV 주장 안 함" vs RESULTS `tested_axes_stable=true`·반올림값·"보고 가능" →
  사전등록 축이 빠지면 `overall_citable_at_0.01eV=False`(None 아님) · verdict 꼬리 "사전등록 축 없음(δ_k)".
- 렌즈2 P1-5 · 렌즈5 `numeric_budget.정의` 가 3축 문자열인데 값은 2축 합 → 실제 합산 축으로 렌더 + 원문 정의 별도 키.
- 렌즈4 P1-1 attestation 명령 불완전(RELEASE_LABEL·SITE 없음)·순서 역전(실행 뒤에 안내)·효과 문구 세 갈래 →
  실행 블록 안에 완전한 선택 줄 · README/ATTREQ/MANIFEST 가 같은 말("기록만 남는다 · 인용 자격 불변").
- 렌즈4 P1-2 반송 목록에 `MANIFEST.json`·`job.json`·`RESULTS.json` 없음 · "통째로 압축" 은 메일에만 →
  반송 정본(`_return_contract`)에 넣어 세 문서가 같이 렌더.
- 렌즈4 P1-3 walltime 세 문서 세 말 · README "나눠서 다시 만들어 드립니다"(이행 불가) · 실행 위치 무언급 →
  `_walltime_block` 한 문장(README = SUBMIT = 메일).
- 렌즈4 P1-4 메일 POTCAR 문장(금지문 없음 · "그 해시로만 대조" 의 대상 불명) → 메일 렌더러에서 정정.

## 4. P2 (v35 에서 고쳤다 / 남긴 것)
- 고침: dense 잔존 문구(SUBMIT 상 의존성·임계경로 · README 프로토콜 요약 · MANIFEST phase_dependencies) 조건부 ·
  SUBMIT 종 순서 목록을 planned 실물에서 · CHGCAR "압축에서 빼되 지우지 말 것" · VASP 프로브 기동 안내 ·
  한국어(돕니다→돌아갑니다 · 반말 → 존칭) · README unzip 을 실행 블록 앞으로 · 1단계 게이트 "8축" 명시 ·
  `bundle_label` · 메일 일정 "4.6일" → 동시 8잡 기준(`cost_frozen.makespan_d`).
- 남김: 렌즈2 P2 "1단계 끝에 D 가 이미 보인다"(네 estimand 잡이 전부 1단계 — 재개 판단이 2단계 전에 가능;
  규칙이 결과 전 선언이라는 점만 유효) · 1단계만 반송된 트리에 "계산은 완주했지만" 문구 · IDENTITY 의 v18 참조 ·
  옛 zip 의 `superseded/` 이동 · MANIFEST 의 임시경로 · `STAGE1_PASS.json` 미판독.

## 5. 1저자 결정 요청 — 재개 조건 (사전등록 개정 안)

비준 프로토콜 §7·§8 과 정합하려면 재개 조건은 다음 중 하나여야 한다. 어느 쪽이든 사전등록 `3_오차예산` 에
`축_설계_제외_2026_09_03` 항(축 · 결정 · 50행과의 관계 · 잃는 것 · 재개 조건 구조 · UMA 금지)과
`status_history` 를 추가하고, `decisions.json` 에 등록하고, 1저자가 **비준**해야 v35 를 만들 수 있다
(생성기가 항이 없으면 거부한다 — 확인됨).

- **A (권고)** 재개 없음. |D_raw| < 0.05 eV 는 §7 미해결·§8 확장 금지, |D_raw| ≥ 0.05 eV 면 k 가드밴드(0.01 eV)가
  판정을 못 바꾼다. 경계 0.05 ≤ |D_raw| < 0.06 eV 에서는 분석기가 `KCONV_UNTESTED_AXIS_AT_THRESHOLD` 자문만 내고
  원고에 "미시험 축에 판정이 민감" 을 적는다. 프로토콜 무수정.
- **B** 경계 구간(0.05 ≤ |D_raw| < 0.06 eV)에서만 dense 2잡을 **별도 번들**로 추가 (§8 과 충돌 없음 · 새 봉인·
  merge 절차 문서 필요).
- **C** 현 규칙 유지 → 프로토콜 §7·§8 재비준 (무겁고 "확장 금지" 철학과 충돌).

## 6. 미완 렌즈와 자체 점검

렌즈 1·3·6 은 각각 4회 재개했으나 매번 API 529 로 종료됐다 (모두 확인 도중, 최종 보고 없음). 렌즈 1·3 의
범위는 아래처럼 내가 직접 짚었다 — **독립 리뷰의 대체가 아니다**.
- 렌즈1 범위(SEAL 프로브): 토큰 regex `vasp\.[0-9][A-Za-z0-9._-]*` 는 `vasp.6.4.3 19Mar24 (build …) complex` ·
  `vasp.5.4.4.pl2` · `vasp.6.1.2 22Jul20` 에서 각각 `vasp.6.4.3` · `vasp.5.4.4.pl2` · `vasp.6.1.2` 를 뽑고, 분석기의
  OUTCAR 버전 regex `vasp\.([\w.]+)` 결과(`6.4.3` 등)는 그 토큰에 부분문자열로 들어간다 (ROOT_SEAL_VASP_MISMATCH
  정합). wrapper/srun 이 앞에 줄을 찍어도 `-m1 -oE` 가 첫 토큰을 찾는다. 빈 INCAR 임시폴더 가정은 여전히 ASE 표본
  순서에 근거한 추론이다 — 외주처 첫 기동에서 확정된다 (fail-closed 라 잘못돼도 비용 전에 멈춘다).
- 렌즈3 범위(러너 stub e2e): 생성기 e2e(`_runner_e2e`)가 stub VASP 로 census→SEAL→census→1단계를 실제로 돌리고,
  9변수 각각의 누락·위조 음성시험이 있다 (15/15). 메일 실행블록은 README 에서 글자 그대로 뽑으며 렌더 결과에
  9변수가 있음을 시험이 지킨다. v35 에서 MAKE→러너→`--check_attestation` 관통도 추가했다.
- 렌즈6(fresh)은 대체하지 않았다 — 보고가 오면 이 문서에 덧붙인다.

## 7. 이행 상태
- c7fdc58e — P0-1 · 렌즈2 P1-1/P1-4/P1-5 (selftest 430/430).
- 271a7357 — P0-2 코드측(비준 항 결박 · 재개 조건 기계 평가 · preflight) · 렌즈4 P1/P2 문서 (selftest 437/437 ·
  verify 30/30 · e2e 15/15). `--no_kconv` 가 사전등록 항 부재로 **거부**하는 것을 실물 인자로 확인했다.
- 남은 것: §5 결정 → 사전등록 개정 + decisions 등록 + 비준 → v35 생성(원격 커밋에서만) → 8가지 확인 → 메일.
