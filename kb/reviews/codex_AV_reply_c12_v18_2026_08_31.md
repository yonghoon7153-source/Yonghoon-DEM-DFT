---
title: "회신 AV — C-12 v18 NO-GO (P0 4건 · P1 1건 · 해제조건 8)"
date: 2026-08-31
updated: 2026-08-31
tags: [review, codex, sdcp, c12, vasp, verdict, no-go]
status: 이행 완료 — P0-1 (895af2ed) · P0-2 (1b3fbefc) · P0-3 (d29c322e) · P0-4 (4aed52ff) · P1-5+⑦ (290513d3, ddc6d7ca). 해제조건 ⑧(v19 실물 e2e)만 잔여
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

> 요청: `kb/reviews/codex_AU_prompt_c12_v18_2026_08_31.md`
> **판정: NO-GO — `sdcp_c12_v18` 을 아직 실행하지 말 것.**
> 무결성 정상: ZIP·MANIFEST 해시 일치 · payload 110/110 · 내장 시험 **274/274 PASS** ·
> 16잡의 분자 그래프·기하 감사와 dense 두 잡의 INCAR/KPOINTS 실물 정상.

## 결과 전에 남은 차단점

1. **P0 — root seal 이 실물 스키마에서 영구 실패.** `analyze_results.py:3627–3673` 은
   `MANIFEST.planned[*].meta.species_order` 로 예정 POTCAR variant 를 계산하는데
   실제 MANIFEST 는 **16/16 잡에서 이 필드가 없다**. 완전한 가상 seal 을 넣어도
   `ROOT_SEAL_PLAN_UNREADABLE(계획 잡 16개에 species_order 가 없음)` 이 발생하고
   `root_seal_coverage.ok=false` → 1단계 10잡을 다 계산해도 2단계가 열리지 않는다.
   해결: planned 에 `species_order` 를 넣거나 analyzer 가 계획된 모든 `job.json` 에서
   읽도록 하고 **실제 v18 manifest 형태로 e2e 시험**.
   → ✅ `895af2ed` 에서 **둘 다** 이행 (+ 실물 manifest e2e)
   → P0-2 ✅ `1b3fbefc` · P0-3 ✅ `d29c322e` · P0-4 ✅ `4aed52ff` · P1-5 ✅ `290513d3`(+`ddc6d7ca`) — 2026-08-31 후속 세션
2. **P0 — 봉인된 VASP 실행파일을 여전히 우회 가능.** `run_staged.sh:41–65` 는 PATH 에서
   찾는 실행파일을 잡지 못한다. 통과하는 형태: `mpirun -np 48 other_vasp` ·
   `/tmp/evil/mpirun -np 48` · `env --split-string=/usr/bin/false`.
   또한 각 `run_job.sh` 는 여전히 임의 `VASP_CMD` 와 기본 `vasp_std` 를 직접 실행할 수
   있어 staged lock·봉인·receipt 를 전부 우회한다. `EXECUTABLE_RECEIPT.tsv` 도 생성만
   할 뿐 analyzer 가 **한 번도 읽지 않는다**.
   해결: 자유형 launcher 문자열과 `env` 를 폐지하고 launcher 별 **고정 argv 문법**.
   `run_job.sh` 는 lock-owner token 없이는 거부하고, 각 phase 직전 VASP 해시가 root
   seal 과 같은지 hard gate. receipt 를 필수 반송·분석 대상으로.
3. **P0 — 약속한 C3 산출물이 구조적으로 안 나온다.** `closure_C3()` 가 clean slab 0개
   번들에서 clean slab 을 요구한다. 제거해도 `vacconv` c2 잡을 일반 pose 로 포함해
   조각당 3행을 만들면서 기대값은 2행으로 세어 다시 `unresolved`.
   C3 의 D3 이중차분에서는 slab Edisp 가 소거되므로 clean slab 이나 D3-off 잡을 추가할
   필요가 없다. `vacconv` 를 제외하고
   `(Edisp_C,sdcp − Edisp_G,sdcp) − (Edisp_C,ptfe − Edisp_G,ptfe)` 를 직접 계산.
   `closure_C1()` 도 같은 문제 — 필요 없으면 명시적 `n/a`.
4. **P0 — 반송 계약대로 보내면 재분석이 막힌다.** README·MANIFEST 는 `static/OUTCAR`
   만 요구하지만 실제로 필요한 것: dense 두 상의 `dense/OUTCAR` · 부모·canary 의
   실행된 `static/POSCAR` · 수정 후 잡별 `EXECUTABLE_RECEIPT.tsv`.
   `SUBMIT_CONTRACT.md` 에는 일부가 올바르나 **세 정본이 서로 다르다.** 그대로 반송하면
   `KCONV_NOT_MEASURED` 또는 `CANARY_GEOM_UNCHECKED`.
5. **P1 — `B_num` 처방과 실행 코드가 반대.** 문구는 "5 meV 를 넘어도 raw D 는 보존하고
   0.01 eV 주장만 철회" 인데 코드는 `NUMERIC_BUDGET_EXCEEDED` 를 estimand block 으로
   넣어 D 계산 전에 `NO_VALUE` 로 반환한다. 결과 객체 자체가 없는 축이
   `missing_axes` 에 안 들어가는 경로도 있다.
   분리: 입력·상태·provenance 유효하면 `D_raw` 와 축별 변화 보존 ·
   `B_num > 5 meV` → `citable_at_0.01eV=false` · `[D−B_num, D+B_num]` 이 0 이나 사전
   guard 를 가로지르면 방향 결론 `NO_CLAIM` · 축 결측·상태 전이·기하/계약 실패일 때만
   estimand 를 `NO_VALUE`. **`B_num` 은 "총 오차 상한" 이 아니라 "현재 시험한 세 축의
   보수적 sensitivity envelope"** 라고 불러야 한다.

## Q1–Q6 판정

- **Q1** 있다 — root-seal 스키마 오류가 결과와 무관하게 stage 1 을 영구 차단한다.
  v17 의 기체 그래프와 dense metadata 문제는 닫혔다.
- **Q2** **우리 판단이 맞다.** net4 dense 두 잡을 추가해도 k 검증만 닫히고, 서로 다른
  realized basin 을 가로질러 minimum 을 취하는 문제는 해결되지 않는다. 인용 가능한
  pool 에는 basin 별 pool 분리와 target/min 재정의가 필요하다. 현재처럼 **영구 비인용
  진단값으로 두는 것이 안전**하다.
- **Q3** 5 meV 초과만으로 raw 값을 버리지는 않는다. 다만 소수점을 줄이는 것도 불충분 —
  사전 정의한 더 거친 보고 단위의 **반폭보다 B_num 이 작고**, 불확도 구간이
  sign·guard·해석을 바꾸지 않을 때만 저해상도 보고가 가능하다. 아니면 raw 진단값만
  남기고 원고 결론은 `NO_CLAIM`.
- **Q4** 인증된 이메일로 받은 외부 해시를 실제 ZIP 에 독립 대조하는 위협모델이면
  detached signature 는 선행조건이 아니다. 그러나 현재 runner 는 **실제 ZIP 경로를
  직접 해시하지 않고 환경변수 두 개를 비교하며, 외부 anchor 검사 전에 SEAL 을
  실행한다.** ZIP 밖 절차로 실제 파일을 먼저 대조하는 것이 필수.
- **Q5** launcher 이름 목록이 좁은 것은 괜찮다 (fail-closed 가 맞다). 문제는 이름보다
  **인자 문법이 지나치게 넓은 것**. `env` 는 제거하고, 미지원 launcher 는 현장별 고정
  프로필이나 **해시로 봉인한 wrapper** 로 추가.
- **Q6** 좁은 exact-cell primary estimand 에는 **신규 VASP 잡이 필요 없다.** 현재
  16잡·18회 구성 유지 가능. clean slab·D3-off·lateral 대조·pool 용 net4 dense 도
  추가 불필요. 필요한 것은 **analyzer·runner·반송 계약의 수정과 재생성**이다.
  단, `B_num` 을 "전체 0.01 eV 수렴성" 이라 부르려면 ENCUT 및 교차축 검사가 빠져
  있으므로 우선 **"시험한 세 축의 envelope"** 로 범위를 제한해야 한다.

## 재승인 해제조건 8

① root-seal 계획 variant 를 실제 job 스키마에서 계산 ② launcher 고정 argv +
direct `run_job.sh` 차단 + receipt hard gate ③ production 의 `.SELFTEST_FIXTURE`
우회 제거 ④ C3 에서 clean slab·vacconv 의존 제거 ⑤ `D_raw` 와 0.01 eV 인용 자격 분리
⑥ README·MANIFEST·SUBMIT 의 반송 목록과 용어 통일 ⑦ 철회했다던 "공통 주기영상 항이
상당 부분 소거" 문구 삭제 ⑧ 새 ZIP/MANIFEST 해시로 실물형 e2e 재검증
