---
title: "Codex 회신 V 요청 — closure 번들 INCAR 실물 감사 (던지기 전 마지막 관문)"
date: 2026-08-29
updated: 2026-08-29
tags: [review, codex, sdcp, vasp, incar, closure, prereg]
status: 발송 대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 회신 V 요청 — 생성된 INCAR 를 실물로 감사해 달라

> 회신 U P0-5 는 *"생성기가 제안 B 를 실제로 생성하지 않는다"* 였다. 그래서 새 도구를
> 만드는 대신 **기존 생성기에 `--closure` 모드**를 넣고 e2e 시험을 붙였다.
> 이 요청은 그 산출물을 **파일 그대로** 심사받는 것이다. 아직 안 던졌다.

---

## 붙여넣을 프롬프트

````
당신은 계산재료 리뷰어다. 회신 U P0-5 지적("생성기가 계획대로 생성하지 않는다")에 따라
`--closure` 모드를 만들었고, **던지기 전에** 생성물을 실물로 감사받으려 한다.
GO / 조건부 GO / NO-GO 와 P0(던지기 차단) / P1 로 답해 달라.

━━━ 무엇을 고쳤나 ━━━
· 새 병렬 도구를 만들려다 **폐기**했다 — 부격자 원장은 슬랩 기준 인덱스로 부호를 주는데
  복합체 POSCAR 는 원자 순서가 다르고, 정본 생성기는 lineage assert + 순열 재매핑으로
  그걸 처리한다. 그 기계를 복제하는 것은 위험하다 (2026-08-12 에 "파일 순서로 반 갈랐더니
  실제 부격자와 24/48 일치" = 동전 던지기였던 이력).
· 대신 `vasp_handoff_bundle.py --closure`:
  - 전 endpoint `LREAL = .FALSE.` (종전 `--single_point` 는 `Auto` 였다)
  - 고정 기하 `IBRION = -1` · `NSW = 0`
  - **기체 기준의 relax 상 제거** (종전엔 항상 relax→static)
  - 기체 기준마다 **비영 MAGMOM 대조** 추가 (회신 U B3)
· e2e selftest 가 생성된 파일을 읽어 위 성질을 확인하고, **음성 대조**로
  `--single_point` 만으로는 `LREAL = Auto` 가 남는다는 것도 확인한다.

━━━ 생성물: 22 잡 ━━━
refs/  clean_slab × 2 basin (+dense 1) · mol × 2 조각 × box20/box24 · mol__*__box24__nzmag × 2
tier1/ ptfe_c10   fib04vfib04_r090 : Litop · Nitop · global_Ni  × 2 basin (+dense 2)
tier2/ sdcp_neutral fib04vfib04_r180: Litop · Nitop · cross_Li_at_Ni · cross_Ni_at_Li × 2 basin (+dense 2)

━━━ ① 복합체 INCAR 전문 (sdcp_neutral Li-top pm1 static) ━━━
```
SYSTEM = sdcp_neutral__fib04vfib04_r180 Li-top afm2424_pm1 [closure · all-F fixed geometry]
# **UMA 이완 기하 위의 단일점.** 승계할 relax 가 없으므로 원자중첩에서 시작한다.
# ⚠ 기하는 DFT 최소점이 아니다 — E_ads 를 인용할 때 반드시 같이 적을 것.
GGA      = PE          PREC     = Accurate    ENCUT    = 520
ISMEAR   = 0           SIGMA    = 0.05        ALGO     = Normal
NELM     = 200         NELMIN   = 6           ISPIN    = 2
ISYM     = 0           LASPH    = .TRUE.      ADDGRID  = .TRUE.
LORBIT   = 11          AMIN     = 0.01        IVDW     = 11         NCORE = 4
EDIFF    = 1E-6
IBRION   = -1
NSW      = 0
ISIF     = 2
LREAL    = .FALSE.
LDIPOL   = .TRUE.      IDIPOL   = 3           DIPOL = 0.5 0.5 0.5181
LDAU      = .TRUE.     LDAUTYPE  = 2
LDAUL     = -1 2 -1 -1 -1 -1
LDAUU     = 0.0 6.2 0.0 0.0 0.0 0.0
LDAUJ     = 0.0 0.0 0.0 0.0 0.0 0.0
LDAUPRINT = 2          LMAXMIX   = 4
MAGMOM   = [Li 48개 0.000] [Ni 48개 ±1.000 원장 부격자] [O 96개 + 분자 35개 0.000]
ISTART   = 0           ICHARG   = 2
LWAVE    = .FALSE.     LCHARG   = .TRUE.
```
※ 종별 순서는 Li Ni O C H S (6종). wave1 되울림의 `LDAUU = 0.0 6.2 0.0 0.0 0.0 0.0` 과 일치.

━━━ ② 기체 기준 INCAR 전문 (sdcp_neutral box24 static) ━━━
```
SYSTEM = gas sdcp_neutral box+24 [static]
GGA=PE  PREC=Accurate  ENCUT=520  ISMEAR=0  SIGMA=0.05  ALGO=Normal
NELM=200 NELMIN=6 ISPIN=2 ISYM=0 LASPH=.TRUE. ADDGRID=.TRUE. LORBIT=11 AMIN=0.01
IVDW=11  NCORE=4
EDIFF    = 1E-6
IBRION   = -1
NSW      = 0
LREAL    = .FALSE.
LDIPOL   = .TRUE.   IDIPOL = 4   DIPOL = 0.4991 0.4847 0.4912
NUPDOWN  = -1
MAGMOM   = 0.000 × 35
ISTART   = 0        ICHARG = 1
LWAVE    = .FALSE.  LCHARG = .FALSE.
```
`__nzmag` 대조는 이것과 **INCAR 의 MAGMOM 줄만** 다르다 (원자 2개에 +1/−1).
POSCAR 해시가 동일함을 확인했다: box24 `ac9dbcdb…` = box24__nzmag `ac9dbcdb…`
(ptfe_c10 도 `d92cbf1a…` 로 동일).

━━━ ③ 해시 일관성 (회신 U P0-5 "해시로 증명") ━━━
KPOINTS: 슬랩 static 전부 `70989534` · 분자 전부 `a194de81` · dense 전부 `b31fa39c`
POSCAR : basin 쌍(pm1/net4)이 동일 해시 — clean_slab `1e633457`,
         Litop `d34c26f4`, Nitop `d76db61b`, cross_Li `531f1d6a`, cross_Ni `e1a4020a`
         ⇒ **같은 구조, MAGMOM 만 다름**을 해시로 확인.

━━━ 🔴 우리가 스스로 걸리는 것 2 ━━━
S1. **복합체 INCAR 에 `NUPDOWN` 줄이 없다.** VASP 기본이 −1(무제약)이라 거동은 기체 기준
    (`NUPDOWN = -1` 명시)과 같고, wave1 되울림도 복합체가 `NUPDOWN = -1.0` 이었다.
    그래도 **한쪽만 명시적**인 것이 감사상 문제인가? 명시하면 거동이 바뀌나?
S2. **비영 MAGMOM 대조의 시작 위치가 임의다** — POSCAR 순서 앞쪽 원자 2개에 +1/−1 을
    걸었다. 닫힌 껍질 유기분자에서 "다른 자기 basin 을 실제로 탐색했다" 를 보이기에
    이 시작이 충분한가? π 계나 특정 결합 위에 거는 것이 더 나은가?
    (우리는 임의 대칭깨짐도 탐침으로는 유효하다고 봤으나 확신이 없다.)

━━━ 묻고 싶은 것 ━━━
Q1. 위 INCAR 두 개에 **던지기 전에 고쳐야 할 것**이 있나? 특히
    (a) `ISIF = 2` 가 `NSW = 0` 과 함께 있는 것 (무해한가, 혼동을 부르나)
    (b) 복합체 `ICHARG = 2` / 기체 `ICHARG = 1` 의 비대칭
    (c) `LMAXMIX = 4` 가 이 계에 맞나
    (d) `ADDGRID`·`AMIN`·`NCORE` 가 에너지 차에 영향을 주나
Q2. `LDIPOL` 이 복합체는 `IDIPOL=3`(z), 기체는 `IDIPOL=4`(전방향)다. 조각 간 대비에서
    이 비대칭이 소거되나, 아니면 편향을 남기나?
Q3. **box20 과 box24 를 둘 다 생성**했다. 회신 U 는 "최단 경로라면 box20 은 돌리지 않는다"
    고 했다. 상자 수렴은 이미 통과(SDCP 0.322 meV)했는데 그래도 box20 을 빼야 하나,
    아니면 all-F 에서 다시 확인해야 하나?
Q4. `global_Ni` 끝점(전역 shift −51.8 meV 로 추가된 챔피언)이 tier1 에만 있고 tier2 에는
    없다. 이 비대칭이 조각 간 대비를 오염시키나? 빼야 하나?
Q5. 22 잡 중 **던지지 않아도 되는 것**이 있나? 우리는 primary(min−min)에 필요한 최소만
    돌리고 싶다.
Q6. 🔴 **아직 못 채운 P0 가 하나 있다 — 회신 U P0-2(basin 중복제거 저에너지 후보).**
    현재 자세는 전부 `legacy_champion/cross` 계보다. UMA 후보 원장(`atlas_rows.json`,
    조각당 392 행 · ranking 자격 322)에는 **에너지 열이 없고** 기하·접촉 메타만 있다
    (`min_contact_pair` 에 `S···Li` 가 실재한다 — 술포네이트 접촉 자세가 풀에 있다).
    이완 에너지는 별도 산출물에 있을 텐데 아직 못 찾았다.
    **이 상태에서 legacy 자세만으로 던지는 것이 의미가 있나, 아니면 P0-2 를 먼저
    채워야 하나?** 만약 던져도 된다면 그 결과의 허용 서술은 무엇까지인가?

━━━ 답변 형식 ━━━
· GO / 조건부 GO / NO-GO + P0 목록 (던지기를 막는 것만)
· S1·S2 와 Q1~Q6 각각: 답 + 그 답이 틀렸을 때 우리가 관측할 증거 하나
· 마지막에: 이 22 잡 중 **실제로 던질 목록**을 명시해 달라
````

---

## 배경 (프롬프트 밖)

- 사전등록은 이미 박았다: `db/properties/prereg_sdcp_neutral_contrast_2026_08_29.json`
  (primary = `min−min`, secondary = `G`, 국소 Ni topology gate, guard band −0.10 eV,
  0.01 eV 반올림, 무조건 재개 조항).
- **Q6 가 이 요청의 진짜 질문이다.** P0-2 를 못 채운 채로 legacy 자세만 던지면
  회신 U 가 "primary 가 될 수 없다" 고 한 그 집합을 다시 만드는 셈이다.
  다만 기준 교정(all-F·고정기하·NUPDOWN)은 **어느 자세를 쓰든 필요**하므로,
  지금 던지면 최소한 legacy 계보의 교정판은 확보된다는 것이 우리 판단이다.
