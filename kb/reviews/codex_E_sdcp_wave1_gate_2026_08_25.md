---
title: "교차리뷰 E — SDCP wave1 게이트 수정·물리 결론 (판정 수령 + 반영)"
date: 2026-08-25
updated: 2026-08-25
tags: [codex, review, sdcp, vasp, gate, wave15]
status: 리뷰완료-반영중
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-25
verifiedBy: "판정의 코드 지적 4건을 실측 재현 후 수정 (LDAUU 산문형 되울림·AUDIT_KEYS 7키 실측 포함)"
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source
---

# 교차리뷰 E — SDCP wave1 (2026-08-25 판정 수령)

> **판정 요지**: "버그 수정은 정당하지만, 현재 상태로 물리 결론까지 승인하기에는
> 재작업이 필요하다." — E-1/3/5/6 조건부 찬성 · **E-2/E-4 반대** · 구조 내보내기 조건부.

## 우리 실측이 판정을 확인/보강한 것

| 지적 | 실측 결과 |
|---|---|
| `_echo_val` 이 LDAUU 를 한 토큰으로 자름 | **더 나빴다** — LDA+U 되울림은 행 중간 산문형(`for each species LDAUU =`)이라 행두 앵커로 **0건**. 게다가 생성부 `AUDIT_KEYS` 가 7키뿐이라 LDAUU 는 **비교 대상에 든 적이 없었다** (0 UNVERIFIED = 미등록) |
| MAGMOM 감사 없음 | OUTCAR 가 MAGMOM·ADDGRID 를 **아예 되울리지 않는다**(grep 0건) — 원리적 검증 불가 → 명시적 unverified 로 |
| 다중 실행 혼합 | wave1 43개는 전부 단일 실행(배너=timing=1) — 세그먼트 분리는 안전망 |
| E-4 상관 구조 | 재검산 일치 — `ΔE차 = E_ads(Ni)차 − E_ads(Li)차` 항등식, clean net4−pm1 = 128.292 meV |

## 반영 완료 (2026-08-25, 커밋 푸시됨)

- **E-1** 산문형 앵커 + 줄끝 캡처 · Decimal 비교(1e309≠2e309·비유한값 불일치, 문자열
  지름길보다 **먼저**) · AUDIT_KEYS 7→16 · **end-to-end 음성 7건** (실제 파일 →
  read_outcar → phase_gates: LDAUU 실차이·깨진 바이트·잘린 gzip·공존·2실행·MAGMOM·inf)
- **E-2** 게이트 보증 범위를 docstring 명시 + 상마다 `incar_audit`
  (verified_exact / verified_equivalence_class / unverified / mismatch) + `run_segments`
  를 RESULTS.json 에 수록. **LREAL 은 exact 가 아니라 equivalence_class.**
- **E-3** errors="ignore" 제거 — strict 디코드, gzip CRC/절단 → OUTCAR_READ_ERROR
  하드게이트, plain/.gz 공존 차단, 확장자·매직 불일치 기록, NUL(UTF-16) 검출
- **E-4** "50.2±0.2 측정" **철회** → 허용 문구(상관된 contrast 의 49.5–50.5 meV
  branch offset, 진단값)로 kb 판정카드·설명문·artifact 3곳 정정. `flip_indices_poscar`
  를 RESULTS 에 기계기록 (첨부물로 "#82" 재검증 불가 문제 해소)
- **E-5** "2-seed 0.1 meV 일치" → "matched-pose ΔE 의 branch×site 상호작용 0.09 meV"
  + k-미검증 단서 + basin 무관성 증명 아님 단서
- **구조 내보내기** Selective Dynamics 원자별 승계(if_pos·move_mask — 22구조 × 144
  고정), `.qe-structure.inc` 실행불가 확장자, 라디칼 6건 전하/스핀 결정 전 실행금지
  명기, 원본·산출 sha256 + 변환기 git 해시
- **wave1.5 패키지** `--basin_rescue` — clean_slab net4 를 2상(NUPDOWN=+4 pin →
  ICHARG=1 해제)으로 유도. NUPDOWN 은 시드 자화합에서 **계산**(비정수면 거부),
  2상 diff 는 ICHARG 한 줄, POSCAR/KPOINTS 바이트 동일, fail-closed 사슬,
  재반전 시의 해석(realized-basin)까지 README 에 선언. selftest 9/9

## 미반영 (다음 라운드 — 순서대로)

1. **E-6 유효성 분리** — energy_valid / delta_e_valid / e_ads_valid /
   ground_state_valid / realized_basin_id 를 분석기에 구현 + 회귀시험. 규칙 문서화
   전 적용 금지(codex 승인 조건). 첫 구현에서 E_ads 는 계속 막는다.
- 2. **QE assembler** — 조각+정본 템플릿 → 완성 입력 (제약·AFM·U·pseudo·전하·k-mesh
   검사). 수동 splice 를 최종 인터페이스로 두지 않기.
3. **README vs RESULTS 정합** — 사람용 요약이 machine 산출물(정본)과 어긋나지 않게
   wave1.5 부터 README 를 RESULTS 에서 생성.
4. sdcp_doped 라디칼 스핀 규약 (1저자 결정 대기) · noncollinear constrained pair
   (#82 반전 비용 — 프로토콜 변경이라 별도 승인 전 미착수)

## 산출물

`sdcp_wave15_basinA_2026_08_25.zip` — rescue 잡(2상) + 분석기 v2 + README ·
새 추출 검증(analyzer selftest PASS · run_job 문법 OK).
