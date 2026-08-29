---
title: "Codex 재검토 요청 AA — 회신 Z 의 P0 8건 처리 후 Stage A v5 재게이트"
date: 2026-08-29
updated: 2026-08-29
tags: [review, codex, sdcp, vasp, bundle, stage-a, regate]
status: 발송 완료 — 회신 AA 접수, 후속은 codex_AB_prompt_stageA_v9_regate_2026_08_29.md
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 재검토 요청 AA — 회신 Z NO-GO 를 고쳤다. 다시 봐 달라

회신 Z 판정: *"현재 문구대로 50잡 동시 발송은 NO-GO. sdcp_stageA_v2 40잡은
수정 후 calibration tranche 로 조건부 GO, motifprobe 10잡은 HOLD."* P0 8건.

**8건 전부 처리했고, 처리 과정에서 우리가 안 물어본 결함 넷을 더 찾았다.**
그중 하나는 회신 Z 가 지적한 것보다 무겁다 (아래 §추가발견 D).

발송본은 **`sdcp_stageA_v5.zip` 하나**다. v2·v3·v4 는 폐기했다.

---

## 붙여넣을 프롬프트

```
당신은 계산화학 번들 감사자다. 직전 라운드(회신 Z)에서 당신은 NO-GO 를 냈고 P0 8건을
지적했다. 우리는 전부 고쳤고, 고치는 과정에서 당신이 안 물어본 결함 넷을 더 찾았다.
이번 심사는 **GO/NO-GO 재판정**이다. P0(발송 차단) / P1(조건부) / P2 로 답해 달라.

━━━ 계와 목적 (변경 없음) ━━━
LiNiO₂(104) 192원자 AFM 슬랩 위 두 조각의 단분자 흡착, 진공·0 K:
  · sdcp_neutral C₁₁H₁₆O₆S₂ (35원자, 술폰산 보유 바인더 단량체)
  · 대조군 c10 = CF₃–(CF₂)₈–CF₃ perfluorodecane (32원자)
VASP PBE+U(Ni 6.2 Dudarev) · ENCUT 520 · D3 zero damping(IVDW=11) ·
MLIP(UMA-omat) 이완 기하 위 **all-F 고정기하 단일점**.

이 40잡은 최종 흡착 결론이 아니라 **Stage A calibration tranche** 다.
사전등록 primary(min−min)는 Stage B(창 안 전 자세, 최대 277잡) 없이는 안 나오고,
1저자 판단으로 Stage B 는 이번 원고 경로가 아니다.

━━━ 발송본 정체성 ━━━
  파일      sdcp_stageA_v5.zip (약 0.4 MB)
  ZIP SHA   8c6587635e559e81dff68be0b960d318e852ea2b4b608d26f0f11bc656ba713c
  MANIFEST  0860ae4340218b599100052d12fa941aa2a319a74f1b43de8c6ddd36a876670e
  clean slab d5f18feb15701f3fc932a1c8f64a09ed48c39ca270d8d8a8f5339658b6c43676
  후보집합  db/properties/prospective_basins_2026_08_29.json · frozen 94675e66e02c855a
  자세      sdcp_neutral b00 b01 b07 b08 · ptfe_c10 b00 b01 b74 b75
  sealed audit (sdcp b09 b62 · c10 b76 b21) 미개봉 — --roles calibration

✅ **이번엔 ZIP 실물을 첨부한다.** 그리고 우리가 먼저 뜯어서 감사했다 (아래 §E).
  두 라운드 연속 "실물이 없어 검증 못 했다" 였던 것을 이번에 끊는다.

━━━ P0 8건 처리 ━━━

[P0-1] ZIP 내부 README/SUBMIT_CONTRACT 수정 + manifest·SHA 재생성
  → 고쳤다. 그런데 **문구 문제가 아니라 생성기 버그**였다:
    `--closure` 는 상을 ["static"] 하나로 만드는데(_emit_slab_job: single_point
    or closure) README 분기가 `a.single_point` 만 봤다. 그래서 4상짜리 옛
    README(82 systems · 259 phase runs · relax/CONTCAR 반송 · tier/pair 표)가
    그대로 배포됐다. 그 함수 자기 주석이 "옛 판으로 내보내는 것은 문구 문제가
    아니라 반송 계약 위반" 이라고 적어 둔 그 사고다.
    분기를 `single_point or closure` 로 고치고, closure 용 README 를 다시 썼다
    (closure 는 기체 기준계도 static 뿐인데 종전 문구가 refs/mol__* 의
    relax/CONTCAR 를 요구하고 있었다).
  → **이 결함은 해시로 절대 안 잡힌다** (그 문서가 원래 그 내용으로 배포됐다).
    그래서 산출물 검사를 넣었다: relax 상이 0인 번들의 README 가 relax 반송을
    요구하면 차단.

[P0-2] Stage A 역할 명시
  → README 에 "실행 단계와 결과 범위" 절을 넣었다 (당신이 준 문단 기반).
    최종 결론 아님 · audit pose 0 · (B)·W 는 회수 후 · pm1/net4 는 초기 seed
    이름이지 최종 basin 아님 · clean slab 두 seed 선회수 후 complex 사용 ·
    고정기하 단일점 전자에너지이지 relaxed adsorption energy 나 자유에너지 아님.
    같은 내용을 마감조건 문서에도 "닫아도 종결이 아니다" 로 박았다.

[P0-3] 40잡 census
  → 당신 조건("net4/off 가 있으면 48잡") 을 **코드로** 확정했다.
    references  8 endpoint × D3 on/off = 16
    complexes   8 pose × 2 seed = 16, + pm1 쌍둥이 8 = 24 (pose 당 3잡)
    합계 40 · audit 0 · **complex net4/off 없음**
    `--d3_seed_main_only` 가 prospective/ 경로에서만 비주-seed 를 건너뛴다.
    비주-seed complex 쌍둥이가 생기면 **번들 생성을 중단**시킨다(hard exit).
    census 를 MANIFEST·README·SUBMIT_CONTRACT 에 산출물에서 센 값으로 박았다.

[P0-4] realized_basin_id · homologous 뺄셈
  → 구현했다. 지문 = (전역부호 정규화된 Ni 부호벡터, 붕괴한 Ni 자리,
    유기종 상대스핀)의 sha256[:12]. 전역 반전은 시간반전이라 같은 상태이므로
    정규화 뒤에 굽는다. 모멘트 표가 없거나 짧으면 **추측하지 않고 None**.
    강제 3지점: 조각 내 이종 basin(BASIN_HETEROGENEOUS) · basin 미판정
    (BASIN_UNRESOLVED_IN_SET) · clean slab 불일치(BASIN_MISMATCH_SLAB).
    clean slab 선회수는 README 요청으로 넣었다(강제는 아니다 — Q3 참조).

[P0-5] motifprobe HOLD
  → 발송에서 뺐다. 실행 순서를 못박았다: Stage A → (B)·W 확정 →
    Stage B candidate·audit 동결 → 그 뒤에 exact 10잡·matched contrast·seed·
    D3 상태를 별도 manifest 로 재요청. 실행 후에도 primary minimum 에 넣지 않고
    사전 지정 matched contrast 의 descriptive 결과로만 쓴다.
  ⚠ 다만 우리는 **판정 문턱과 해석 비대칭을 지금 이미 박아 두었다**
    (ΔE_motif 판정바닥 0.05 eV; probe 를 고른 omat 에 분산이 없어 눕는 백본
    자세를 불리하게 매기므로 백본이 이기면 강한 결과·수소결합이 이기면 약한
    결과). 나중에 정하면 결과 보고 정하는 것이 되기 때문이다. 이것이 옳은가는
    Q4.

[P0-6] POTCAR 검사
  → 개수만 세고 있었다. 실제 실패 모드는 "$PP/Ni_pv/POTCAR 가 사실은 Ni" ·
    "PBE.52 세트" 이고 **둘 다 개수는 맞는다.** 고쳤다:
    ① 자리별 variant 를 토큰 전체로 비교 (Ni 가 Ni_pv 안에서 오탐되면 안 된다)
    ② functional 이 PAW_PBE 인지
    ③ 원본·조립본 SHA256 을 POTCAR_PROVENANCE.json 에 남겨 **반송**시킨다
    정본 SHA 는 라이선스상 못 싣는다 — 대신 분석기가 잡 사이 일관성을 본다
    (같은 variant 는 전 잡에서 같은 SHA 여야 한다).
    가짜 PP 트리로 검증: 양성 통과, 음성 둘(Ni_pv 자리에 Ni · PAW_LDA) 차단.
    **옛 판은 그 둘을 전부 통과시켰다.**

[P0-7] INCAR allowlist 충돌
  → analyzer 에 NCORE/KPAR/NSIM allowlist 가 **구현돼 있지 않다**(확인함).
    files_sha256 이 INCAR 전체를 덮으므로 한 줄만 바뀌어도 거부된다. 그런데 두
    README 다 "병렬 태그는 예외" 라고 약속하고 있었다. 당신 처방대로 수정 허용을
    없앴다: 그대로 두고 알려 달라 · 재시도는 원본을 덮지 말고 <잡>/_retry_1/ 에.

[P0-8] 두 ZIP 분리
  → README 첫 절에 서로 다른 빈 디렉터리 unzip + 별도 반송 명시.
    (이번엔 묶음이 하나라 실질 위험은 없지만 문구는 남겼다.)

━━━ 🔴 추가발견 — 당신이 안 물어본 것 넷 (전부 우리 실측) ━━━

[A] verify 가 **다른 번들을 검사하고 정상이라고 보고했다.**
  재생성을 기존 경로에 던졌더니 생성기가 정상적으로 거부했는데(경로 비어있지
  않음), 이어 돌린 verify 가 그 자리의 **옛 번들**(34잡, 후보집합이 다름)을
  검사하고 출력만 보면 정상처럼 보였다. `candidate_set` 문자열이 둘 다
  "calibration_pilot" 이라 구별이 안 된다. 잡아낸 것은 --expect_jobs 40 하나였다.
  더 나쁜 것: 그 옛 번들의 후보 파일은 **repo 에 없다**(계산 서버에만 있다).
  → 고침: verify 가 from_basins 경로를 찍고, 그 파일이 repo 에 있는지 본다.
    없으면 차단 — candidate set 을 재현·감사할 수 없는 번들이다.

[B] MANIFEST 와 문서가 **같은 번들 안에서 어긋났다.**
  v4 에서 SUBMIT_CONTRACT 는 "총 VASP 실행 40" 인데 MANIFEST.submission 은 24
  였다. 앞 수정이 문서 쪽 계산만 고치고 MANIFEST 를 만드는 **다른 계산**을 안
  고쳤다. 외주가 둘 중 무엇을 읽을지 우리가 못 정한다.
  → 고침: 실행 횟수를 세는 곳을 **하나로 합쳤다**(중앙에서 한 번 세고 README·
    SUBMIT_CONTRACT·MANIFEST 가 그 값을 쓴다). verify 도 둘 다 본다.
  → v5 실측: MANIFEST 40 = SUBMIT_CONTRACT 40 = 상별 static 40.

[C] 축소판 번들의 유혹을 거절했다.
  c10 을 4→2자세로 줄인 34잡 판이 있었다. 아끼는 시간이 2.99→2.37일 = 약 15시간
  뿐인데, 그 대가로 c10 의 닫힘조건 C1(UMA–DFT 오프셋 조각 내 상수성)이 n=2 로
  떨어져 **평가 불가**가 된다(C1 이 조각당 4자세를 요구한다). 폐기했다.

[D] ★ **조각 매칭이 실물 잡 키에서 하나도 안 걸렸다** (제일 무겁다)
  실제 잡 키에는 그룹 접두어가 붙는다 — `prospective/sdcp_neutral__b00__afm2424_pm1`.
  그런데 estimand 계산기가 `jn.startswith(fragment + "__")` 로 조각을 골랐다.
  **실물에서 한 건도 안 걸린다.** 결과:
    · C2(J_f, 자기 seed × pose 상호작용)가 **조용히 비었다** — 에러가 아니라
      미산출이라, 닫힘조건 하나가 평가 불가가 되는 것을 아무도 못 본다
    · 방금 넣은 realized_basin 강제 3지점이 **전부 죽은 코드**였다
  못 본 이유: selftest fixture 가 `sdcp_neutral__poseA` 처럼 **접두어 없는 키**를
  썼다. 양성·음성 전부 통과하는데 실물에서는 한 건도 안 걸리는 상태였다.
  → 고침: 접두어 내성 매칭 + **fixture 를 실물 키 모양으로 교체**.
    후자가 진짜 수정이다.
  ⚠ v5 번들 자체는 영향 없다(입력이지 분석기가 아니다). 회수 후 분석 단계에서
    드러났을 것이고, 그때는 3일을 이미 쓴 뒤다.

[E] ★★ **ZIP 실물 감사 — 기계 검사는 전부 통과했는데 INCAR 를 열어 보니 결함이 있다**

  먼저 기계 검사(전부 통과): ZIP sha256 일치 · MANIFEST sha256 일치 · 배포파일 245개
  전건 재검증 · census 실물 확인(refs 16 · complex 24 · **complex net4/off 0개** ·
  전 잡 static, relax/pre/dense 폴더 0) · IVDW=11 이 24잡·부재 16잡 ·
  KPOINTS 기체 Γ-only 12 / 슬랩 3 4 1 = 28 · 슬랩 LDIPOL=T·IDIPOL=3, 기체 IDIPOL=4 ·
  MAGMOM 이 pm1 합 0 / net4 합 +4, 양쪽 다 Ni 48개만 비영 · POTCAR ORDER 가 잡마다
  다름(`Li_sv Ni_pv O S C H` / `C F` / `Li_sv Ni_pv O`) · README 에 옛 이완판 문구
  0건. ENCUT 520 · ISMEAR 0/0.05 · LASPH T · LREAL F · NSW 0 · IBRION −1 · ISYM 0 ·
  EDIFF 1E-6 이 40/40 동일.

  🔴 그런데 **자기 제약이 비대칭이다**:
    기체 분자 12잡          NUPDOWN = 0      (제약)
    복합체 24 · slab 4      NUPDOWN 줄 없음  (= 기본 −1, 자유)
    nzmag 대조군            MAGMOM 에 +1 −1 을 심었지만 **NUPDOWN = 0 그대로**

  원인: 생성기가 `nupdown = 1 if open_shell else (-1 if free_spin else 0)` 이고
  `free_spin` 은 `--free_spin_refs` 로만 켜지는데 그 플래그를 안 줬다.
  `nonzero_start` 는 MAGMOM 만 바꾸고 NUPDOWN 을 풀지 않는다.

  이것이 나쁜 이유 둘:
   ① 우리 규율이 이름 붙인 그 패턴이다 — **제약된 기준에서 자유로운 복합체를 뺀다.**
      (당신이 회신 O 에서 "같은 NUPDOWN 값이 아니라 같은 state-selection policy" 라고
       정정해 준 바로 그 건이다.)
   ② **사전등록 게이트 3 이 발동할 수 없다.** 문구는 "더 낮은 다른 상태가 나오면
      MOLECULAR_STATE_UNRESOLVED 로 멈춘다" 인데, 총자화가 0 에 묶여 있으면 다른
      총자화 상태에 도달할 수 없다. 대칭깨짐 singlet 은 여전히 탐지하지만 삼중항 등은
      원리적으로 못 본다. 발동할 수 없는 게이트는 검증이 아니라 거짓 안심이다.

  영향 범위 (우리 판단, 검증해 달라):
    C1 조각 내 오프셋 산포 — 무영향 (E_mol 이 그 조각 전 자세에 같은 상수 → 산포에서 소거)
    C2 J_f                 — 무영향 (복합체끼리만)
    C3 D3 분해             — 무영향 (기체 항이 on/off 양쪽 같은 제약 → 차이에서 소거)
    절대 E_ads · 조각 간 대비 — **영향 있음** (이번 캠페인은 그 값을 안 내지만 원고엔 필요)

  우리 조치안: `--free_spin_refs` 를 켜 재생성(v6). 복합체 24·슬랩 4는 바이트 동일
  (플래그가 기체 잡 생성기에만 들어간다), 기체 12잡만 바뀐다. 재생성 초 단위, 기체 잡
  분 단위. → **Q9 가 이것을 묻는다.**

━━━ 닫힘 조건 (DFT 0잡 시점에 등록, 이후 문턱 불변) ━━━
Stage A 로 닫으려는 것 셋. 각 문턱을 결과 보기 전에 고정했다.
  C1 UMA↔DFT 오프셋의 조각 내 산포 S_f ≤ 50 meV → "조각 내 선택기" 정당화 /
     초과 → 그 판정을 **철회**. (지금 근거는 조각당 2자세뿐. 4자세로 늘린다)
  C2 J_f = max_p d_p − min_p d_p, d_p = E(p,net4) − E(p,pm1).
     ≤10 meV seed-insensitive / 10–40 magnetic-sensitive / >40 SELECTOR_FAIL.
     (당신이 회신 X 에서 준 문턱 그대로 승계 — 새로 정하지 않았다)
  C3 D3 짝계산으로 조각 간 오프셋 차등 0.90 eV 중 분산 기여분 D:
     ≥0.63(70%) → 빠진 분산이 주원인 / ≤0.27(30%) → 기각 / 사이 → **미해결로 닫음**
  C4(모티프 대비)는 P0-5 로 이번 범위에서 제외 — 문턱은 보존.

━━━ 묻고 싶은 것 ━━━

Q1. **재판정.** 위 8건 처리로 sdcp_stageA_v5 40잡을 발송해도 되나?
    남은 P0 가 있으면 그것만.

Q2. **[D] 를 어떻게 봐야 하나.** 우리는 "selftest 가 통과하는데 실물에서
    안 걸리는" 결함을 두 라운드 연속으로 자체 발견했다(직전 라운드에서는
    POTCAR 개수 검사, 이번엔 잡 키 접두어). 둘 다 **입력 모양이 실물과 다른
    fixture** 가 원인이다. 이것은 개별 버그인가, 아니면 우리 시험 방식에
    구조적 결함이 있다는 신호인가? 후자라면 무엇을 바꿔야 하나?
    (우리가 생각한 것: fixture 를 실제 산출물에서 뽑기. 하지만 그러면 산출물이
     없는 단계에서는 못 돌린다.)

Q3. **clean slab 선회수를 강제해야 하나.** 당신은 "clean slab 두 seed 를 먼저
    회수해 통과시킨 뒤 complex 를 여는 편이 안전" 이라고 했다. 우리는 그것을
    README 의 **요청**으로 넣었고 기계적으로 강제하지는 않았다 — 40잡이 서로
    독립이라 순서를 강제하면 외주 쪽 병렬도를 우리가 제약하게 된다.
    분석 시점에 "clean slab 이 게이트를 통과하지 못하면 complex 로 아무 값도
    만들지 않는다" 는 사후 강제로 충분한가, 아니면 실행 순서 자체를 강제해야
    하나? 후자라면 40잡 makespan 이 늘어나는 대가를 감수할 값어치가 있나?

Q4. **P0-5 의 잔여 문제.** motifprobe 를 Stage B 동결 뒤로 미뤘는데, 그
    판정 문턱과 해석 비대칭은 **지금 이미 박아 두었다**(위 P0-5 ⚠).
    이것이 옳은가? 두 가지 우려가 상충한다:
    (a) 나중에 정하면 결과를 보고 문턱을 고르는 것이 된다
    (b) 지금 정하면, Stage A 결과를 본 뒤에 그 문턱이 유리해 보이는지 알게 되고
        그때 "그대로 둔다" 는 선택 자체가 정보를 쓴 것이 된다
    어느 쪽이 덜 나쁜가? 문턱을 **봉인**(우리가 못 보게)하는 절차가 필요한가?

Q5. **realized_basin_id 의 설계.** 지문에 넣은 것은 (Ni 부호벡터, 붕괴 자리,
    유기종 상대스핀) 셋이다. 빠뜨린 축이 있나? 구체적으로:
    (a) 모멘트 **크기**를 안 본다(부호와 붕괴 여부만). 같은 부호벡터인데 크기가
        크게 다른 두 해를 같은 basin 으로 볼 위험은?
    (b) 붕괴 문턱 0.4 μB 는 승계값이다. 이 판정에 그 값이 적절한가?
    (c) 전역 시간반전을 같은 상태로 접는 것은 맞다고 보는데, **부분** 반전이
        많은 경우(예: 48 Ni 중 20개) 지문이 그냥 다른 값이 될 뿐 "얼마나 다른가"
        를 못 말한다. 거리 개념이 필요한가?

Q6. **실물 감사의 한계 — 이번에 실측이 생겼다.** [E] 가 그 답의 일부다:
    우리 기계 검사 전부(해시·census·문서-실물 일치·후보 provenance)를 통과한
    번들에서, **INCAR 를 사람이 열어 보고서야** 자기 제약 비대칭이 나왔다.
    (a) 이 결함을 **자동 검사로 옮길 수 있나?** 우리가 생각한 규칙은
        "한 번들 안에서 기준계와 대상계의 스핀 제약 정책이 다르면 차단" 인데,
        정당한 예외(라디칼은 NUPDOWN=1 이 옳다)를 어떻게 가르나?
    (b) 실물이 있어야만 잡히는 것이 이것 말고 또 무엇인가?

Q7. **[반대 방향] 우리가 과잉인가.** 이번 라운드에 우리가 추가한 자동 검사가
    16건(음성 13)이다. 번들 하나 보내는 데 이 정도 방어가 정당한가, 아니면
    검사 자체가 비용이 되어 실제 물리 진전을 늦추고 있나?
    (배경: 이 계의 흡착에너지는 여덟 번 계산해 여덟 번 반려됐다. 우리는 그
     이후로 계속 방어를 늘리는 쪽으로만 움직였다.)

Q9. **[E] 를 어떻게 처리해야 하나.** 우리 판단은 "C1~C3 은 면역이지만 발동
    불가한 게이트를 안고 나가는 것은 규율 위반이니 v6 으로 고쳐 보낸다" 이다.
    (a) 동의하나? 아니면 C1~C3 에 영향이 없으니 v5 그대로 보내고 free-spin 기체를
        나중에 **보충 잡**으로 붙이는 것이 나은가?
    (b) free-spin 으로 바꾸면 게이트 3 이 이번엔 발동할 수 있게 되는데, 만약 실제로
        더 낮은 비-singlet 이 나오면 우리는 MOLECULAR_STATE_UNRESOLVED 로 멈춘다.
        중성 닫힌껍질 유기분자에서 그럴 확률을 당신은 어떻게 보나? 멈출 각오로
        여는 것이 맞나, 아니면 "중성은 singlet 으로 선언한다" 를 estimand 에
        명시하고 제약을 **유지**하되 복합체에도 같은 제약을 거는 쪽인가?
        (후자면 복합체 24잡을 다시 만들어야 한다 — 비용이 다르다.)

Q8. 우리가 **안 본 축** 중에 이 40잡을 무의미하게 만들 수 있는 것이 있으면
    그것도. (우리가 본 축: 문서-실물 일치 · census · POTCAR 정체성 · INCAR
    무결성 · 자기 basin · 후보집합 provenance · 실행 횟수 · clean slab 동일성)

━━━ 답변 형식 ━━━
· Q1 은 **GO / NO-GO** 를 먼저 한 줄로.
· 각 항목 P0/P1/P2 + 근거. 동의는 "동의" 한 줄. **반박에 지면을 써라.**
· 마지막에: 이 40잡을 던지지 말아야 한다면 그렇게 말해 달라.
```

---

## 왜 이 프롬프트인가 (프롬프트 밖)

- **Q2 가 본체다.** 두 라운드 연속으로 "selftest 는 통과하는데 실물에서 안
  걸리는" 결함이 나왔고 원인이 같다 — fixture 의 입력 모양이 실물과 다르다.
  개별 버그로 처리하면 세 번째가 온다.
- **Q4 는 우리가 답을 모른다.** 문턱을 미리 박는 것과 나중에 박는 것 둘 다
  정보를 쓰는 경로가 있다. 봉인 절차가 답일 수 있는데 우리 이력에 없다.
- **Q7 은 일부러 반대로 물었다.** 여덟 번 반려 이후 우리는 방어만 늘려 왔고,
  그것이 지금 정당한지 스스로 판정할 위치에 있지 않다.
- Q6 은 회신 Z 가 스스로 적은 한계("ZIP 이 첨부되지 않아 검증하지 못했다")를
  되돌려 묻는 것이다 — 우리가 그 간극을 자동 검사로 얼마나 메울 수 있나.

## 처리 이력

| 회신 Z P0 | 처리 | 어디 |
|---|---|---|
| 1 문서/manifest 재생성 | ✅ 생성기 버그 수정 후 v5 재생성 | `vasp_handoff_bundle.py` README 분기·`_readme_sp` |
| 2 Stage A 역할 | ✅ README "실행 단계와 결과 범위" | 같은 파일 · 마감조건 문서 |
| 3 census | ✅ 코드로 세고 위반 시 생성 중단 | `man["job_census"]` |
| 4 realized_basin_id | ✅ 지문 + 강제 3지점 | ANALYZER `realized_basin_id` · `_closure_estimand` |
| 5 motifprobe HOLD | ✅ 발송 제외 + 순서 명시 | `REQUEST.md` §8 · 마감조건 C4 |
| 6 POTCAR | ✅ 순서·variant·PAW_PBE·SHA 반송 | `_write_potcar_asm` |
| 7 INCAR allowlist | ✅ 예외 삭제 · 실패 반송 | 두 README |
| 8 ZIP 분리 | ✅ README 첫 절 | `_readme_sp` |

추가발견 A~D 는 전부 이번 라운드에 자체 발견·수정했다.
