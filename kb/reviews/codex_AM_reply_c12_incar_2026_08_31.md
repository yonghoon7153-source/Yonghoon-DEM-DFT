---
title: "회신 AM 접수 — NO-GO. 분석기가 자기 번들을 못 읽는다"
date: 2026-08-31
kind: review_reply
status: 접수
tags: [sdcp, vasp, incar, c12, vacuum-convergence, estimand, review/codex]
---

# 회신 AM 접수 — **NO-GO** (해제조건 9개)

무결성은 정상이었다 (ZIP·MANIFEST 해시 일치, 122파일 전수, 12잡 · pre 10 + relax 12 +
static 12 = 34회, **c1/c2 Cartesian 좌표가 7.1e-15 Å 이내로 동일하고 c 만 정확히 +4 Å**).
문제는 구조 생성이 아니라 **phase graph 와 분석 계약**이다.

---

## 0. 우리가 묻지 않았는데 나온 P0 여섯 — 셋은 repo 에서 즉시 확인했다

### ✅ 확인 P0-2 — 분석기가 c2 잡을 **못 찾는다**
`closure_vacconv()` 가 c1 을 `kind="prospective_pose"`, c2 를 `kind="vacuum_convergence"` 로
고르는데, 실물 `job.json` 은 c2 도 `kind="prospective_pose"` + `vacconv="c2"` 다.
⇒ **c1 후보가 둘(ambiguous), c2 후보가 0.** 결과가 다 있어도 진공 판정이 안 나온다.

### ✅ 확인 P0-4 — 2단계 러너가 작동하지 않는다
`run_staged.sh` 1단계가 **전체 분석기**를 부른다. 전체 분석기는 아직 안 돈 2단계 6잡을
`required_missing` 으로 세어 **무조건 exit 2**. ⇒ 진공 시험을 통과해도 2단계를 못 연다.
`--gate vacconv` 같은 **부분 판정 모드**가 필요하고, 반대로 최종 분석에서는
`closure_vacconv.pass != true` 나 `prereg_closure=NO_VALUE` 를 **비정상 종료코드로** 묶어야 한다.

### ✅ 확인 P0-1 — 선언한 estimand 와 실제 계산이 다르다
주장 문구는 *"고정기하 단일점 규약 아래"* 인데 실물은 `pre→relax→static` 이고
relax 가 `NSW=200, IBRION=2` 다. **DFT 부분이완 에너지**다.
게다가 분석기가 primary 의 pm1·net4 를 함께 모아 조각별 최솟값을 고르므로,
SDCP 와 PTFE 가 **서로 다른 seed 에서 선택될 수 있다** — "pm1 조건부 D" 와도 다르다.

**우리 결정**: **DFT 부분이완 estimand 로 확정**하고 manifest·문구를 고친다.
(static-only 로 되돌리지 않는다 — INCAR 설계가 `pre→relax→static` 을 의도한 것이고
`static 이 판정 에너지의 정본` 이라는 주석도 그 전제다.) 그리고 **D 에 들어가는
정확한 job key 를 사전 고정**한다: 조각별 최솟값이 아니라 **pm1 primary 고정**.

### P0-3 — `--refs_minimal` 과 분석기가 서로 호환되지 않는다
번들엔 box24 만 있는데 분석기가 없는 clean-slab 경로 때문에 `has_refs=True` 가 되고
box20·box24 를 **둘 다** 요구한다 ⇒ `emol=None` · `VACCONV_NO_GAS_REF` 또는 예외.
**더 근본적으로 진공 판정엔 기체가 필요 없다** —
`Δ_vac = [E_C^S(c₂)−E_C^S(c₁)] − [E_C^P(c₂)−E_C^P(c₁)]` 에서 두 기체가 정확히 소거된다.
⇒ C-12 전용 minimal-reference 경로를 따로 구현한다.
⚠ 이건 우리가 짠 1단계 러너 설계도 틀렸다는 뜻이다 —
*"기체 기준이 1단계에 있는 이유: 반올림 비교에 공통 기체 offset 이 필요하다"* 는 근거가
Δ_vac 에는 **성립하지 않는다**.

### P0-5 — 자기상태 계약이 양쪽에서 비어 있다
분석기는 `molecular_spin_controls` 를 **필수**로 요구하는데 번들엔 필드도 잡도 없다.
complex 는 모든 phase 에서 `NUPDOWN` 기대값이 비어 있고, `phase_gates()` 는 실제 OUTCAR 에
값이 있어도 "기대값 미등록" 으로만 남기고 **차단하지 않는다**.
⇒ 모든 complex phase 에 `NUPDOWN=-1` 을 명시하고 **exact echo gate**.
그리고 `_spin_setup_ok()` 가 NUPDOWN 을 안 봐서, 양수 제약에서도 전역 스핀 반전을
동치로 접는다 — `-1/미설정` · `0` · **양수 제약**을 구분해야 한다.

### P0-6 — CHGCAR 승계를 **파일 존재로만** 본다
`read_outcar()` 에 `chgcar_from_file` 판독이 있는데 `phase_gates()` 가 안 쓴다.
`ICHARG=1` 인 모든 static phase 에 **실제 read 증거**를 hard gate 로.

---

## 1. Q1 — 진공 시험: 조건부 찬성, **단 우리 처방이 틀렸다**

우리는 *"c2 의 NSW 만 0 으로"* 라고 했는데 그러면
**c1 static 은 c1 의 DFT 이완 기하를, c2 static 은 배포 당시 원시 기하를** 쓴다. 틀렸다.

올바른 fixed-geometry 시험:
1. **c1 최종 기하를 먼저 확정**
2. 그 **Cartesian 좌표를 그대로** 두고 c 만 +4 Å
3. fractional z 와 `DIPOL` 만 새 셀에 맞춰 재계산
4. c2 는 `NSW=0`; **source c1 CONTCAR SHA 와 Cartesian 동일성**을 manifest·분석기가 검증
5. c1/c2 의 **realized magnetic topology 가 같아야** 한다

⇒ 이건 c1 이 끝난 **뒤에** c2 를 만든다는 뜻이다. 지금처럼 한 번에 배포할 수 없다.

**문턱**: `|Δ_vac| ≤ 5 meV` 는 사전 고정 **운영 문턱**으로 유지 (결과 보고 올리지 않는다).
그러나 **"0.01 eV 반올림 일치" 는 hard gate 에서 내린다** — 0.0049 vs 0.0051 eV 는
차이가 0.2 meV 인데 표시는 0.00/0.01 로 갈리고, c 에 무관한 기체 offset 을 더하면
Δ_vac 은 그대로인데 반올림 판정만 바뀐다.
⇒ 물리 gate = `|Δ_vac| ≤ 5 meV` · `same_rounded` 는 **정보용** ·
반올림만 불일치하면 Figure 삭제가 아니라 **불확도 병기 또는 한 자리 추가 보고**.

⚠ c1/c2 두 점은 **"+4 Å 증가에 대한 안정성"** 이지 무한진공 수렴의 증명이 아니다.
판정 범위를 시험한 **b00·pm1 branch** 로 제한한다.

## 2. Q2 — 기체 자기상태: **(c)**

(a) 를 기본 정책으로 채택하되 **조각당 비영 자화 static canary 하나**를 추가한다.

> 허용 문구 — "기체 기준은 중성 closed-shell singlet(`NUPDOWN=0`)로 정의하였다.
> 슬랩 복합체는 `NUPDOWN=-1` 에서 사전 고정된 pm1/net4 초기자화로 시작한
> unconstrained-spin SCF 이며, **자기 바닥상태가 아니라 seed-conditioned realized basin**
> 으로 보고한다."

⛔ (b)(NUPDOWN 만 풀고 `MAGMOM=0` 유지)는 **자유스핀 탐색이 아니다** — VASP 는 최종
자기상태가 초기 `MAGMOM` 에 강하게 의존한다고 명시한다.
⇒ canary 는 `NUPDOWN=-1` + **비영 원자별 MAGMOM** + static-only.
canary 가 사전 문턱보다 낮으면 **자동 채택하지 말고** molecular state 를 `unresolved` 로 재개.

## 3. 부수 4건 판정

| | 판정 | 요지 |
|---|---|---|
| ① `LREAL=Auto` 이완 → `.FALSE.` static | 조건부 | *"Auto-relaxed geometry 에서의 `.FALSE.` energy"* 로 **제한**하거나, 최종 `.FALSE.` 힘 검사로 D 변화가 사전 문턱 안인지 확인 |
| ② `EDIFFG=-0.02` | **부족** | 힘 정지조건일 뿐 D 의 에너지 오차 보증이 아니다. soft mode·자유원자 수 때문에 힘→에너지 환산이 안 된다 |
| ③ 기체 이완 | 찬성 | 통상 0 K 전자 adsorption energy 정의와 맞다. 단 interaction energy·자유에너지·ZPE 가 **아니고**, 기체 conformer 하나만 썼으면 **"지정 conformer 기준"** 으로 제한 |
| ④ `ISTART=0, ICHARG=1` | 조건부 찬성 | spin-polarized CHGCAR 에 자화밀도가 들어 있고 `LMAXMIX=4` 도 맞다. 단 **initializer 일 뿐 basin 제약이 아니므로** 실제 read 증거 + 최종 topology 둘 다 필요 |

**추가**: 최종 D 에서는 SDCP·PTFE 의 **기체 에너지 차가 소거되지 않는다.**
지금 box24 하나뿐이라, 동일 conformer·동일 Hamiltonian 에 대한 **선행 gas-box 수렴 증거를
해시로 연결**하거나 별도 수렴 대조가 필요하다. (Δ_vac 엔 불필요, 최종 0.01 eV D 엔 필요.)

## 4. 제출 승인 해제조건 (9개)

1. 고정 MLIP 기하 vs DFT 부분이완 중 **estimand 하나 확정** + manifest·phase graph·문구 일치
2. D 에 들어가는 **정확한 fragment·pose·seed·cell job key 사전 고정**
3. **c1→c2 기하 계보와 Cartesian 동일성 gate** 구현
4. vacconv metadata 와 `closure_vacconv()` **cohort 선택 정합**
5. clean slab·box20 을 요구하지 않는 **C-12 minimal-reference 분석 경로** + stage-scoped 종료코드
6. **singlet gas + nonzero-spin canary** 정책 · complex `NUPDOWN=-1` exact audit ·
   NUPDOWN-aware topology 판정
7. 모든 `ICHARG=1` phase 에 **실제 CHGCAR-read hard gate**
8. **실제 생성된 번들 자체를 fixture 로** stage 1 PASS/FAIL · refs-minimal · c2 인식 ·
   최종 NO_VALUE 비정상 종료를 e2e 로 봉인
9. 마지막에 **POTCAR pin** 을 넣어 제출본 재생성

`allow_no_pin=true` 와 POTCAR 부재는 dry-run 선언과 일치하므로 새 결함으로 세지 않았다.
