---
title: "Codex 회신 X — prospective 번들 NO-GO · P0 6건 · Stage A/B 재설계"
date: 2026-08-29
updated: 2026-08-29
tags: [review, codex, sdcp, vasp, prereg, closure, bundle, reply]
status: 접수
confidence: high
verificationStatus: partial
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 회신 X — **NO-GO**. 지금 40잡은 final bundle 이 아니라 잘못 조립된 calibration tranche 다

> 첨부 사고: zip 과 `INCAR_DIGEST.txt` 가 **실제로 전달되지 않았다.** 리뷰어는 프롬프트
> 안의 수치만으로 판정했고, 그것만으로 P0 넷이 재현됐다.

## P0 (던지기 차단)

| # | 내용 | 우리 상태 |
|---|---|---|
| 1 | **PTFE `b21` 은 sealed audit 이 아니다.** −0.1983−(−0.2660)=+0.0677 < W0=0.15 → 창 **안쪽**. "audit 은 창 밖" 설명과 모순, W 규칙상 candidate 다 | ✅ **우리가 회신 도착 전 독립 발견.** 코드 `rest = pool_out + pool_in` 이 2번째 audit 을 전 pool 에서 뽑는다 (`site_screen.py:1650`) |
| 2 | **4+2 는 최종 `prospective_lowE` 가 아니라 calibration pilot 이다.** W 절차는 calibration DFT → (B)·최종 W 확정 → 창 안 **전부** 선택 → 그 **밖**에서 audit 봉인. 우리는 최종 W 를 모르는 채 audit 과 candidate 를 **동시에** 동결했다 | 인정 |
| 3 | **창 안 후보를 대부분 버렸다.** W0 안에 SDCP 8 · PTFE 75 = **83 pose**. 4+2 만 돌리며 `prospective_lowE` 라 부르는 것은 "k=4 는 batch 이지 hard cap 이 아니다" 는 W 판정과 양립 불가 | 인정 (수치도 정확 — 아래 확인) |
| 4 | **두 seed 가 아니라 두 realized magnetic basin 이 필요하다.** wave1.5 에서 raw `net4` 가 intended topology 가 아니라 Ni 하나 뒤집힌 basin 으로 반복 수렴한 전례. 결과마다 최종 Ni sign-vector · moment collapse · 유기종 상대스핀을 담은 `realized_basin_id` 필요 | 미구현 |
| 5 | **새 clean slab provenance 미해결.** `d5f18feb` 가 틀렸다는 뜻이 아니라, `daf71160` 과 달라진 **원인을 모르는 상태**에서는 reproducible frozen geometry 라 부를 수 없다 | 우리 M1 과 동일 판정, 단 **실행 전 P0** 로 격상 |
| 6 | **실물 감사 자료 없음.** digest 명령이 `head -400` 으로 INCAR 를 자르고 SHA256 을 16자리만 남긴다 → "전 INCAR·전체 해시 감사" 자료가 아니다 | 명령 수정 필요 |

## Q1 — 두 magnetic seed 의 범위 (**우리 self-P0 의 답**)

- **전 complex pose(calibration + audit)에 두 realized basin 이 필요하다.** audit 을 pm1
  하나로만 계산하면 *"창 밖 pose 가 net4 에서만 낮아지는"* 반례를 관측하지 못한다.
- **그러나 64잡은 불필요하다.** 고정기하 D3(zero)는 원자종·기하에 따른 additive
  correction 이므로 **두 번째 자기 seed 에 D3-off 쌍둥이를 다시 만들 필요가 없다.**
- ⇒ pose 당 **3잡**: `pm1 D3-on` · `pm1 D3-off` · `net4 D3-on`

순차 판정:
1. calibration 8 pose 에 먼저 두 seed
2. 최종 topology 가 비교 가능한 basin 쌍인지 확인
3. calibration 의 pose×basin interaction 통과 시 audit 에도 net4
4. raw net4 가 서로 다른 basin 으로 가면 **중단**하고 pin→release 재설계

판정 통계 — 조각별 기준 pose 를 b00 이라 할 때 `E_{p,m} − E_{b00,m}` 을 기록하고
`J_f = max_p(E_{p,n}−E_{p,m}) − min_p(E_{p,n}−E_{p,m})`:

| J_f | 판정 |
|---|---|
| ≤ 10 meV | sampled set 에서 seed-insensitive |
| 10–40 meV | magnetic-sensitive |
| > 40 meV, 또는 seed 에 따라 audit regret > 40 meV | **selector 실패** |

## Q2 — clean slab 변경 (M1)

구조 변경 자체가 prospective **내부 상대순위**를 무효화하지는 않는다 — 같은 fragment
안의 pose 차이·pose×basin interaction 에서 clean slab 과 gas reference 는 소거된다.
전 complex 가 `d5f18feb` 파생이고 같은 `d5f18feb` reference 만 쓰면 조건부 성립.

**금지**: ① `d5f18feb` complex 에 `daf71160` clean energy 사용 ② 두 slab geometry 의
E_ads·branch shift pooling ③ legacy net4 topology 를 새 slab 에 그대로 승계.

**실행 전 기록할 것**: old/new 시작 POSCAR + constraint hash · UMA checkpoint/task/코드
버전/dtype/device · FIRE 설정·fmax·step·최종 force · PBC 정렬 후 old/new RMSD 와
최대변위 · **완전히 같은 입력의 독립 재실행 2회**. 새 clean pm1/net4 는 complex 보다
**먼저** 회수해 realized basin 확인.

## Q3 — basin ≈ pose 인 중복제거

조건부 허용. 단 **"basin" 이라고 부르면 안 된다** → `unique relaxed poses`.
추가로 필요한 확인: slab translation + surface space-group canonicalization ·
PTFE 동등 원자 permutation · 분자 대칭과 뒤집힘 · surface registry/anchor/전체 contact
graph · **정렬된** heavy-atom RMSD.
⇒ PBC minimum-image RMSD 만으로 얻은 최소 3.33 Å 은 symmetry-equivalent pose 가
없다는 충분한 증거가 아니다.
calibration 네 역할은 유지 가능하되 **네 자세가 실제로 서로 다른 contact/site/orientation
stratum** 이어야 한다. b00/b01 또는 경계쌍이 같은 지문이면 farthest-point diversity pose 로 교체.

## Q4 — D3-off reference 범위

ΔE_D3(ads) 는 **complex · clean slab · gas 세 항 전부** 필요하다 (특히 gas 의
intramolecular D3 는 조각 사이에서 소거되지 않는다). 목적별로는:

| 목적 | 필요한 D3-off |
|---|---|
| 같은 fragment 의 pose 순위 | complex 만 (clean·gas 소거) |
| fragment 간 absolute contrast | C · S · M 전부 |
| 같은 POSCAR 의 pm1/net4 | **불필요** (D3 correction 동일) |
| clean slab 두 seed 가 같은 POSCAR | 한 geometry 로 충분 |

더 줄이려면 D3-on OUTCAR 의 `Edisp` 를 파싱하고 대표 complex·slab·gas 한 건씩에서
`D3on − D3off = Edisp` 를 검증한 뒤 나머지 twin 을 생략할 수 있다.

## Q5 — INCAR 와 box20

실물이 없어 판정 불가. digest 수정 요구: **SHA256 64자리 전체** · `head -400` 제거 ·
모든 INCAR 를 path 와 함께 전부 · `MANIFEST.json` 전체(또는 canonical JSON+hash) ·
**ZIP 자체 SHA256**.
확인 못 한 것: 실제 MAGMOM 길이·atom order · complex 의 명시적 `NUPDOWN=-1` ·
`job.json.incar_expected` vs 실제 INCAR · POTCAR spec/조립순서/expected SHA · KPOINTS 와
phase metadata · D3-off job 의 IVDW 가 실제 0/미설정인지 · **audit 역할이 analyzer 에서
primary candidate 와 분리되는지**.
box20 은 승계를 구현하지 않았으면 **유지**가 맞다 (기체라 싸고 all-F·새 molecular-state
protocol 수렴을 직접 확인). box20 의 D3-off twin 은 필수 아님.

## Q6 — 우리가 안 물어본 가장 큰 위험

> **audit 결과를 selector 실패 판정 전에 primary min 에 합치는 것.**

분석 순서는 반드시:
1. calibration 으로 (B)·W 확정 → 2. 창 안 candidate 결과 동결 → 3. **candidate-only
minimum** 기록 → 4. audit unseal → 5. regret 계산 → 6. 실패면 audit 를 candidate 에
편입하되 **selector 는 FAIL 로 기록** → 7. 확장 후 새 audit 재봉인 → 8. 통과한 뒤에만
최종 physical minimum.

지금처럼 audit 포함 12 pose 를 처음부터 `prospective_lowE` 라 부르면, audit 이 새 최저가
되어도 *"우리가 더 낮은 자세를 찾았다"* 로 흡수돼 **selector 실패가 사라진다.**
추가: SDCP gate 3건의 ID·이유·원자료를 manifest 에 남길 것.

## 실제로 던질 목록

### Stage A — calibration **40잡** (현재 예산 그대로, 구성만 교체)

**References 16**
- clean slab `pm1`/`net4` × D3 on/off (4)
- PTFE molecule `box20`/`box24`/`box24-nzmag` × D3 on/off (6)
- SDCP molecule 동일 (6)

**Calibration complexes 24** — SDCP `b00 b01 b07 b08` · PTFE `b00 b01 b74 b75`,
각 pose 에 `pm1 D3-on` · `pm1 D3-off` · `net4 D3-on`

⇒ 현재 번들의 **audit complex 8잡은 던지지 않는다.** 그 자리를 **calibration net4 8잡**
으로 교체하면 총량은 40 그대로.

### Stage B — calibration 회수 후

(B)·최종 W 계산·커밋 → 창 안 전 pose 를 `S_W` 로 동결 → 최종 W 밖에서 조각당
nearest-outside 1 + 층화난수 1 을 **새 audit** 로 동결 → 미계산 candidate·audit 마다 3잡 →
realized basin 과 audit regret 확인.

```
총잡수 = 40 + 3·( |S_W \ C_cal| + 4 )
```

W ≥ 0.15 이고 현재 경계 번호가 에너지순이면 S_W ≈ 83 → **총 283잡 수준까지 열린다.**
예산상 불가능하면 **네 개로 자를 것이 아니라**, DFT 를 보기 전에 window floor 를 수정해
재등록하거나, UMA 를 순위 선택기에서 강등하고 **diversity-stratified DFT 설계**로 바꾼다.

---

## 우리 쪽 실측 — 창 폭 대 후보수 (동결 manifest 에서 직접)

`basin_id` 는 에너지 오름차순임을 확인했다 (두 조각 다 정렬 OK). 리뷰어의 83 은 정확하다.

| W (eV) | SDCP 창 안 | c10 창 안 | S_W | 총잡수 | 동시 8잡 |
|---|---|---|---|---|---|
| 0.03 | 2 | 5 | 7 | 52 | 25.5 일 |
| 0.05 | 2 | 13 | 15 | 73 | 35.7 일 |
| 0.08 | 4 | 32 | 36 | 136 | 66.6 일 |
| 0.10 | 6 | 51 | 57 | 199 | 97.4 일 |
| **0.15** | **8** | **75** | **83** | **277** | **135.6 일** |

## 🔴 이 표에서 나온, 아무도 안 물어본 것 — **두 팔의 표본밀도가 다르다**

- c10 은 96 basin 이 **0.19 eV 안에** 뭉쳐 있다 (W=0.15 안에 75개).
- SDCP 는 101 basin 이 넓게 퍼져 있다 (W=0.15 안에 **8개**).

primary estimand 는 `min_p A(SDCP,p) − min_q A(c10,q)` 다. **min 은 표본이 많을수록
내려가는 편향 통계다.** 같은 창 규칙을 적용하면 c10 은 75개에서, SDCP 는 8개에서 min 을
뽑는다 — **대조군만 조직적으로 유리해진다.**

실측 크기 (UMA):
- c10 min: 상위 8개만 보면 −0.2269, 75개 전부 보면 **−0.2660** → **39 meV 하락**
- SDCP min: 8개든 2개든 **+0.0200** → **0 하락**

UMA 는 자세 간 차이를 **2.9–3.9배 압축**한다 (`prereg …_2026_08_29.json`
`Δ_압축`). 압축을 되돌리면 DFT 에서 **~110–150 meV** 규모다. 주장하려는 격차가
0.346 eV 인데 그 **3분의 1** 이 표본밀도 차이에서만 나올 수 있다.

⇒ 회신 X 의 Q6("audit 흡수")과 **다른** 병이다. 그쪽은 audit 회계 문제고, 이쪽은
**primary estimand 자체가 두 팔의 표본수에 의존**한다는 것이다. 사전등록이 G 를
primary 에서 뺀 이유(*"자세를 더 볼수록 나빠진다"*)가 min−min 에도 **약한 형태로
그대로 있다.**

이것이 회신 Y 의 첫 질문이 된다.
