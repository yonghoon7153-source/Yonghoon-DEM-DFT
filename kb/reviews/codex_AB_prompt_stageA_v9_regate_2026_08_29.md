---
title: "Codex 재검토 요청 AB — 회신 AA 의 P0 5건 + Q2 처리, 그리고 자체검토에서 나온 넷"
date: 2026-08-29
updated: 2026-08-29
tags: [review, codex, sdcp, vasp, bundle, stage-a, regate]
status: 회신 수령 (원문 파일 없음 — 근거: AD (Stage A v10))
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 재검토 요청 AB — AA 의 P0 5건을 닫았다. 그리고 우리가 넷을 더 찾았다

회신 AA 판정: **NO-GO**, P0 5건 + Q2(구조적 시험 결함) P0.
전부 처리했고, 처리 과정과 발송 직전 자체 적대검토에서 **넷을 더 찾았다.**
그중 하나(§F-1)는 AA 의 P0-4 를 우리가 **절반만** 고쳤다는 것이다.

---

## 붙여넣을 프롬프트

```
당신은 계산화학 번들 감사자다. 직전 라운드(회신 AA)에서 당신은 NO-GO 를 냈고 P0 5건
(+ Q2 를 P0 로) 지적했다. 우리는 전부 처리했고, 그 과정에서 넷을 더 찾았다.
이번 심사는 **GO/NO-GO 재판정**이다. P0(발송 차단) / P1(조건부) / P2 로 답해 달라.

━━━ 계와 범위 (변경 없음) ━━━
LiNiO₂(104) 192원자 AFM 슬랩 위 두 조각의 단분자 흡착, 진공·0 K.
sdcp_neutral C₁₁H₁₆O₆S₂ vs 대조군 c10 = CF₃–(CF₂)₈–CF₃.
PBE+U(Ni 6.2) · ENCUT 520 · D3 zero damping(IVDW=11) · MLIP 기하 위 all-F 고정기하 단일점.
이 40잡은 **Stage A calibration tranche** 이고 최종 흡착 결론이 아니다.
사전등록 primary(min−min)는 Stage B 없이 안 나오며 Stage B 는 이번 원고 경로가 아니다.

━━━ 발송본 ━━━
`sdcp_stageA_v9.zip` — 40잡 · 476,238 B
  ZIP SHA256  246da98748e9f2754925504e0cbeb865db91ddd4c68e401b456abfc008dabc3b
  MANIFEST    e232e975e0659f8756c993d1dd1d093c6d701f7f98ce46ff43bf88eee3c053a0
  clean slab  d5f18feb15701f3fc932a1c8f64a09ed48c39ca270d8d8a8f5339658b6c43676
  후보집합    prospective_basins_2026_08_29.json ·
              전체 SHA 20fdde06760b36e15a9bd544925c71e4b1a52f430348ff64a2224f1bf61f6d6e
⚠ **ZIP 실물을 첨부한다.** 증서 `ATTESTATION_v9.json` 도 같이 (ZIP 바이트에서 직접 생성).
그리고 번들 안 `analyze_results.py` 가 **스스로 selftest 를 통과한다** — 우리 repo 없이
`python3 analyze_results.py --selftest` 로 판정 코드를 직접 검증하실 수 있다.
(v8 까지는 그 분석기에 C1·C3 코드가 없었다 — §F-1 때문에 재생성했다.)

━━━ AA P0 5건 처리 ━━━

[P0-1] ZIP 바이트 기반 독립 정체성 증거
  → `--verify_zip` 을 만들었다. **폴더가 아니라 ZIP 이 입력**이다.
    ① ZIP 전체 SHA → ② 엔트리 위험을 **풀기 전에**(중복·`..`·절대경로·대소문자
    충돌·symlink) → ③ 새 임시 디렉터리 → ④ **MANIFEST 를 안 보고 디스크에서
    잡·상·파일을 재열거** → ⑤ 기존 검사 → ⑥ detached attestation.
    증서 필드: ZIP SHA · MANIFEST SHA · **후보집합 전체 SHA**(16자리 접두어 아님) ·
    clean slab SHA · 생성 argv·UTC · 디스크 재계산 census · MANIFEST census ·
    생성기/검증기 파일 SHA · 번들 내 분석기 SHA · git commit·branch·dirty ·
    명령·rc·verdict. 그리고 **이 증서가 보증하지 않는 것 넷**을 같이 적었다
    (verifier 자신의 의미론적 버그 · estimand 타당성 · PP트리/VASP build/스케줄러 ·
    SCF 수렴·OUTCAR 형식) — 당신이 Q6 에서 적은 그대로다.

[P0-2] POTCAR trusted hash allowlist
  → site-local 목록을 **요구**하고 없으면 거부한다(exit 1). 면제는
    `POTCAR_ALLOWLIST_WAIVED=1` 로만 되고 `POTCAR_PROVENANCE.json` 에 기록된다.
    안내문에 "목록을 **한 번만** 만들어 전 잡에 같은 파일을 쓰라" 를 넣었다 —
    잡마다 새로 만들면 아무것도 검증하지 않는다.
    ⚠ 정직하게: 해시를 variant 와 묶어 보게 바꿨지만, **파일이 뒤바뀐 트리는 이미
    TITEL 검사가 잡고 있었다**(TITEL 이 내용을 따라간다). 이건 심층방어지 우리가
    발견한 구멍의 수정이 아니다. → Q4 가 이것을 묻는다.

[P0-3] 경로 문자열 파싱 → 구조화 필드
  → 근본원인이 따로 있었다: **D3-off 쌍둥이의 job.json 이 부모와 완전히 같았다.**
    쌍둥이는 copytree 후 INCAR 의 IVDW 줄만 지우므로 on/off 를 가를 구조화 필드가
    **아예 없었다.** 그래서 이름 접미어에 의존할 수밖에 없었던 것이다.
    이제 `d3` 를 **INCAR 실물에서 유도**해 전 잡에 박고(플래그 기억이 아니라
    배포되는 입력이 근거), `d3` 가 on/off 가 아닌 잡이 하나라도 있으면 **번들을
    만들지 않는다**(hard exit). cohort 조립은 `kind/fragment/seed/basin_id/d3` 로만
    하고, 경로와 어긋나면 `COHORT_INCOHERENT` 로 값을 만들지 않는다.

[P0-4] C1·C3 를 실행 가능한 estimand 로
  → 정의를 고쳤다. C1 은 주장 강도를 **"선택된 네 자세에서의 국소 calibration
    일관성"** 으로 낮췄고(681 후보 selector 검증이 아니다 — 당신 지적 그대로),
    `S_f` 를 **range** 로 명시했으며, 4자세 중 하나라도 빠지면 unresolved 다
    (부분집합은 range 를 작게 만들어 통과 쪽으로 편향된다).
    C2 는 `seed-insensitive` 를 버리고 **"seed×pose 상호작용이 작다"** 로 바꿨다.
    C3 는 δ·D 식, branch(pm1), clean slab, gas box(box24), 집계(4자세 산술평균),
    결측 규칙, 그리고 **부호 먼저** 를 못박았다.
    ⚠ 그런데 이것을 **코드로는 안 냈다.** §F-1 참조 — 그게 이번 자체검토의 핵심이다.

[P0-5] basin 지문 · D3 짝 · stale 산출물
  → 지문 v2: 전역 시간반전을 접기 전에 **collinear·무SOC·무외부장·무제약을 INCAR
    되울림에서 기계로 확인**한다. 붕괴 판정을 **두 문턱**으로 나눠
    (<0.25 붕괴 / 0.25–0.55 **회색 → unresolved** / >0.55 자성) 회색이 하나라도
    있으면 지문을 만들지 않는다. 해시는 정규화 canonical JSON 의 **full SHA256**
    (12자는 표시용). raw 모멘트 벡터와 Ni 인덱스 매핑을 보존한다.
    `basin_distance()` 추가 — 전역부호 정규화 후 ternary Hamming · 붕괴 자리
    대칭차 · 모멘트 RMS/최대차 · flipped index. `same` 은 부호·붕괴가 같고
    **RMS ≤ 0.30 μB** 일 때만 참이다.
    stale: `run_job.sh` 가 시작 전에 OUTCAR/WAVECAR/CHGCAR 등이 있으면 **거부**
    (exit 1). 재개는 `ALLOW_RESUME=1` 로만. 일부만 지우고 재실행해도 막힌다.
    D3 짝: on/off 가 **다른 realized basin** 이면 그 조각의 C3 는 unresolved.

[Q2 = P0] 구조적 시험 결함
  → `--selftest_e2e` 를 만들었고 **표준 `--selftest` 에 물렸다**(따로 두면 아무도
    안 돌린다 — 우리가 맞은 병이 바로 "안 돌린 층" 에서 나왔다).
    이 시험은 **fixture 를 만들지 않는다**: 슬랩·조각·자기원장을 생산 경로 그대로
    부르고(SS.load_slab · SS.load_fragment · afm_ledger + 실제 relax.in),
    `build_bundle()` 이 만든 실물을 검사하고, MANIFEST 를 안 믿고 디스크에서 다시
    세고, 합성 OUTCAR 를 주입해 분석기까지 왕복하고, mutation 4종으로 흔든다.
      A 생산 생성기가 실물로 번들 생성
      B verifier 가 ZIP 바이트에서 통과
      C 디스크 재계산이 **정확히 19·static 19** ("0개가 아님" 이 아니라 정확히 N)
      D 전 잡이 한 구조화 role 로 분류 (미분류 0) · D2 d3 가 정확히 11/8 ·
        D3 d3 가 **INCAR 실물과 전건 일치**
      E 합성 OUTCAR → 분석기 판독 왕복 · E2 cohort 정합성
      F mutation: d3 삭제 · 폴더 개명 · 파일 끼우기 · 잡 삭제 → 전부 깨져야 한다
    12/12. 만들면서 **두 번 막혔는데 그게 증거다** — 장난감 슬랩은 계보 게이트가,
    장난감 분자는 토폴로지 게이트가 거부했다.

━━━ 🔴 우리가 더 찾은 넷 (전부 실측·수정 완료) ━━━

[F-1] ★★ **AA 의 P0-4 를 우리가 절반만 고쳤다.**
  당신은 "C1 과 C3 가 아직 **실행 가능한** estimand 로 고정되지 않았다 … 결과를 본
  뒤 선택할 자유도가 남는다" 고 했다. 우리는 **문서의 정의만** 고쳤고 분석기에는
  J_f(C2) 만 있었다. C1·C3 는 회수 후 손계산이 되는 상태였고 — 그것은 자유도를
  그대로 남기는 것이며 이 계를 여덟 번 물린 경로다.
  → `closure_C1()` · `closure_C3()` 를 분석기에 넣었다. primary 가 막혀도(이 번들은
    calibration tranche 라 CALIBRATION_ONLY_TRANCHE 로 막힌다) 이 둘은 나온다.
  구현하면서 나온 것 둘:
    · 처음에 **기대 자세 수를 회수된 잡에서 셌다.** 그러면 자세가 빠져도 기대가
      같이 줄어 **영영 못 잡는다.** selftest 의 음성이 통과해 버려서 드러났고,
      **동결된 MANIFEST.planned** 를 정본으로 바꿨다.
    · 분석기는 번들 안에 **단독 배포**돼 생성기 상수를 못 본다. C1/C3 가
      `SEED_MAIN` 을 참조해 NameError 로 죽었다 → 분석기 쪽에 정의를 박았다.
      **같은 상수가 두 곳에 있는 구조**가 남는다 → Q5.

[F-2] v7 에서 `d3` 가 **8잡에 비어 있었다.**
  P0-3 을 고친 첫 판은 stamping 을 쌍둥이 생성 루프 안에 뒀는데,
  `--d3_seed_main_only` 라 쌍둥이가 안 생기는 net4 복합체 8잡이 통째로 빠졌다.
  그 8잡은 IVDW=11 이라 실제로는 D3-on 인데 필드만 비었다. 커밋 메시지에
  "필드가 없는 잡이 남으면 분류가 다시 이름으로 샌다" 고 적어 놓고 그 구멍을 남겼다.
  → INCAR 에서 유도 + 생성 시 계약(hard exit) + 정합성 검사의 관용 제거.
  v8 실측: on 24 / off 16 / None **0**, INCAR 실물과 불일치 0.

[F-3] verifier 가 **다른 번들을 검사하고 정상이라 보고**했다.
  재생성을 기존 경로에 던졌더니 생성기는 정상 거부했는데, 이어 돌린 verify 가 그
  자리의 옛 번들(34잡·후보집합이 다름)을 검사했다. `candidate_set` 문자열이 둘 다
  "calibration_pilot" 이라 구별이 안 된다. 잡은 것은 `--expect_jobs` 하나뿐이었다.
  더 나쁜 것: 그 후보 파일은 **repo 에 없었다**(계산 서버에만).
  → verify 가 `from_basins` 를 찍고 그 파일이 repo db/ 에 있는지 본다. 없으면 차단.

[F-4] selftest 가 **전역 상태를 오염**시켰다.
  대형 selftest 가 `SS.load_slab` 를 몽키패치하고 복원하지 않아, E2E 를 이어 돌리면
  장난감 슬랩을 받아 원장과 어긋났다. **단독 실행은 통과** — 시험 순서에 따라
  결과가 달라지는 상태였다. 적재 시점 원본을 붙잡고 selftest 끝에서 복원한다.

━━━ 닫힘 조건 (DFT 0잡 시점 등록, 문턱 숫자 불변) ━━━
C1 S_f = max_p e − min_p e (range), e = E_ads^DFT − E_ads^UMA, pm1·D3-on,
   4자세 전부 필요. ≤50 meV → **이 네 자세 안에서 잔차 범위가 작다**(그 이상 아님)
C2 J_f — 10/40 meV, 문구는 "seed×pose 상호작용", basin 동일성은 별도 게이트
C3 δ_{f,p} = [C_on−C_off]−[S_on−S_off]−[M_on−M_off], D = mean_SDCP − mean_c10,
   **부호가 같을 때만** ≥0.70 채택 / ≤0.30 기각 / 사이 미해결
C4(모티프)는 Stage B 동결 뒤로 (AA P0-5) — 문턱은 보존

━━━ 묻고 싶은 것 ━━━

Q1. **재판정.** `sdcp_stageA_v9` 40잡을 발송해도 되나? 남은 P0 가 있으면 그것만.

Q2. **[F-1] 을 어떻게 봐야 하나.** 우리는 당신의 P0-4 를 받고 **문서만 고쳤다.**
    "실행 가능한 estimand" 를 정의의 명확성으로 읽었고, 코드로 읽지 않았다.
    (a) 이 오독은 개별 실수인가, 아니면 "리뷰 지적을 문서로 닫는" 우리 습관인가?
    (b) 지금 C1·C3 구현이 §닫힘조건의 정의와 실제로 같은가? 특히 —
        · 기대 자세 수를 **MANIFEST.planned** 에서 가져오는 것이 맞나 (회수분에서
          세면 누락을 못 잡는다는 것이 우리 논거다)
        · C1 에서 pose 의 realized basin 이 clean slab 과 다르면 unresolved 로
          두는데, 같은 조각 안의 pose 끼리만 비교하므로 slab 은 소거된다는 반론이
          가능하다. 어느 쪽이 옳나?
        · C3 의 `mean` 이 맞나 — 4자세 중 하나가 극단이면 평균이 끌려간다.
          중앙값이나 자세별 보고가 나은가? (우리는 결과 전이라 못 고른다)

Q3. **[F-2]·[F-4] 는 같은 병인가.** 둘 다 "코드 경로의 분기 하나가 시험에서 안
    돌았다" 이다(쌍둥이 없는 잡 · 시험 순서). E2E 가 이 층을 덮나, 아니면
    **커버리지 계측**(어느 분기가 시험에서 안 돌았는지)이 따로 필요한가?

Q4. **[P0-2] 를 우리가 과대보고했나.** 우리는 variant-해시 결속을 넣었지만, 정작
    파일이 뒤바뀐 트리는 **TITEL 검사가 이미 잡는다**는 것을 시험하면서 확인했다.
    (a) 그러면 allowlist 가 실제로 잡는 것은 무엇인가 — 같은 variant 의 **다른
        release** 뿐인가?
    (b) 그 경우에도 site 가 혼합 트리에서 목록을 만들면 둘 다 통과한다. allowlist
        요구가 실질적 보증을 주나, 아니면 절차만 늘리나?
    (c) 우리가 요구할 수 있는 더 강한 것이 있나 (예: VASP POTCAR 헤더의 자체
        검증 해시를 파싱해 대조)?

Q5. **분석기가 번들 안에 동봉되는 구조.** 분석기는 문자열 템플릿으로 배포되고
    생성기 상수를 못 본다(그래서 `SEED_MAIN` 이 두 곳에 있다). 그리고 분석기를
    고치면 **번들을 다시 만들어야** 한다(v8 → v9 가 그 이유다).
    이 결합이 옳은가, 아니면 분석기를 별도 배포하고 번들엔 버전·해시만 박는 것이
    나은가? 후자면 "회수물과 분석기 버전이 어긋나는" 새 실패 모드가 생긴다.

Q6. **C1 의 주장 강도가 이제 충분히 낮은가.** 당신 지적대로 "국소 calibration
    일관성" 으로 내렸는데, 그러면 이 40잡이 **무엇을 정당화하나**? 우리 이해는
    "prospective 설계를 계속할 근거는 되지만 selector 유효성 주장은 아니다" 이다.
    이 정도로 40잡을 쓰는 것이 합리적인가, 아니면 같은 예산으로 **층화 holdout** 을
    넣어 selector 를 실제로 시험하는 설계가 나은가? (후자면 지금 던지지 말고 다시
    설계해야 한다 — 그렇게 말해 달라.)

Q7. **[반대 방향] 우리가 언제 멈춰야 하나.** 이번 라운드에 자동 검사가 또 늘었다
    (verify 24 · e2e 12 · 분석기 basin 11 · cohort 4 · C1/C3 7). 당신이 AA Q7 에서
    준 stop rule("최종 산출물에서 P0 invariant 가 전부 통과하면 발송, P1/P2 는
    위험등록부") 를 우리가 지키고 있나, 아니면 매 라운드 새 P0 를 스스로 만들어
    내며 발송을 미루고 있나? 후자라면 그렇게 말해 달라.

Q8. 우리가 **안 본 축** 중에 이 40잡을 무의미하게 만들 수 있는 것.

━━━ 답변 형식 ━━━
· Q1 은 **GO / NO-GO** 를 먼저 한 줄로.
· 각 항목 P0/P1/P2 + 근거. 동의는 "동의" 한 줄. **반박에 지면을 써라.**
· 마지막에: 이 40잡을 던지지 말아야 한다면 그렇게 말해 달라.
```

---

## 왜 이 프롬프트인가 (프롬프트 밖)

- **Q2 가 본체다.** AA 의 P0-4 를 문서로만 닫은 것은 개별 실수가 아니라 습관일 수
  있다. 이번엔 발송 직전 자체검토가 잡았지만, 그 검토가 매번 있으리라는 보장이 없다.
- **Q6 이 예산 질문이다.** C1 의 강도를 정직하게 내리고 나니 "그럼 이 40잡이 무엇을
  정당화하나" 가 남는다. 층화 holdout 재설계가 답이면 지금 던지면 안 된다.
- **Q7 은 일부러 반대로 물었다.** AA 가 준 stop rule 을 우리가 지키는지 스스로
  판정할 위치에 있지 않다. 매 라운드 새 P0 를 만들어 내는 중일 수 있다.
- Q4 는 우리가 **과대보고했을 가능성**을 먼저 적은 것이다 — 심층방어를 구멍 수정으로
  파는 것은 이 캠페인이 여덟 번 물린 방식과 같다.

## 처리 이력

| AA 지적 | 처리 | 어디 |
|---|---|---|
| P0-1 ZIP attestation | ✅ | `--verify_zip` · `ATTESTATION_v9.json` |
| P0-2 POTCAR allowlist | ✅ (⚠ 심층방어 — Q4) | `_write_potcar_asm` |
| P0-3 구조화 cohort | ✅ (F-2 재수정 포함) | `d3` INCAR 유도 · `COHORT_INCOHERENT` |
| P0-4 C1·C3 estimand | ✅ 문서 + **코드**(F-1) | 닫힘조건 JSON · `closure_C1/C3` |
| P0-5 basin·stale | ✅ | 지문 v2 · `basin_distance` · run_job 가드 |
| Q2 시험 구조 | ✅ | `--selftest_e2e` 12/12, 표준 selftest 에 물림 |
