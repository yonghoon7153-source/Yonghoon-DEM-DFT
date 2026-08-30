---
title: "회신 AM — C-12 INCAR 실물 감사: 진공 시험이 진공만 재지 않는다"
date: 2026-08-31
kind: review_request
status: draft
tags: [sdcp, vasp, incar, c12, vacuum-convergence, estimand, review/codex]
---

# 회신 AM — 12잡 INCAR 을 실물로 뽑아 프로토콜과 대조했다

**아직 안 던졌다.** 번들(12잡)은 만들었고 무결성 검증도 통과했지만, INCAR 을 실제로
꺼내 프로토콜과 줄 단위로 맞춰 보니 **두 곳이 걸린다.** 던지기 전에 묻는다.

리포 `claude/friendly-meitner-lldvar` · 번들 `sdcp_c12_dryrun3`
(zip `fbfa6b3ad9ed…`, MANIFEST `dec14ea178dc…`, 12잡, 프로토콜 §3 과 1:1)

---

## 1. 재려는 것

**`D = [E_C − E_G]^SDCP − [E_C − E_G]^PTFE`** — 두 조각 모델의 **흡착에너지 차** 하나.
clean slab 은 대수적으로 상쇄되므로 계산하지 않고, **개별 절대 E_ads 는 보고하지 않는다.**
보고 단위는 0.01 eV.

잡 12개 = vacconv 4 (primary·pm1·c1/c2 × 2조각) + main net4 4 + main 대안자세 pm1 2
+ 기체 기준 2.

---

## 2. ✅ 프로토콜과 맞는 것 (static = 판정 정본)

`GGA=PE` · `ENCUT 520` · `ISMEAR 0 / SIGMA 0.05` · `IVDW 11`(D3 zero damping) ·
**`LREAL=.FALSE.`** · `NSW 0 / IBRION −1` · `LDIPOL=.TRUE. / IDIPOL=3`(슬랩) ·
`ISYM 0` · `LDAU=.TRUE. / LDAUTYPE 2 / LDAUU(Ni)=6.2 / LMAXMIX 4` · `LORBIT 11` ·
`EDIFF 1E-6` · KPOINTS `3 4 1`(static) / `2 3 1`(pre·relax) ·
`DIPOL` 이 잡마다 COM 을 따라 재스케일됨.

---

## 3. 🔴 걸리는 것 ① — **진공 두께 수렴 시험이 진공만 재지 않는다**

판정식과 문턱:
```
Δ_vac = D(c₂ = 40.6551 Å) − D(c₁ = 36.6551 Å)
통과 = |Δ_vac| ≤ 5 meV  그리고 두 값이 0.01 eV 자리에서 같게 반올림
```

그런데 `vacconv/*/relax/INCAR` 이 **`NSW = 200`, `IBRION = 2`, `EDIFFG = -0.02`** 다 —
**c2 잡이 기하를 처음부터 다시 이완한다.**

⇒ `Δ_vac` 에 (a) 진공 두께 변화 (b) **서로 다른 이완 결과**가 섞인다.
`EDIFFG = −0.02 eV/Å` 로 멈춘 두 최적화가 5 meV 안에서 일치할 근거가 없다.
**5 meV 는 보고 단위(0.01 eV)의 절반으로 정한 값이지 물리 상수가 아니다** — 그래서
이완 잡음이 그 문턱을 넘으면 시험이 진공이 아니라 이완 재현성을 재게 된다.

**우리 판단**: c2 는 **c1 의 최종 기하 그대로 단일점**이어야 한다 (`NSW=0`, 셀 c 만 늘림).
그러면 `Δ_vac` 이 순수하게 주기영상 상호작용만 담는다.

**★ Q1.** 이 진단이 맞는가? 그리고 c2 를 단일점으로 바꾸면
- 늘어난 진공에서 **기하가 실제로 달라지는 효과**를 못 보게 되는데, 그건 이 시험의
  범위 밖이라고 선언해도 되는가?
- 아니면 문턱을 이완 잡음 위로 올려야 하는가? (그럼 5 meV 의 근거가 사라진다)

## 4. 🔴 걸리는 것 ② — **기체 기준에만 제약이 걸려 있다**

| | NUPDOWN | MAGMOM |
|---|---|---|
| 기체 `refs/mol__*` | **`NUPDOWN = 0`** (강제 일중항) | 전부 0.000 |
| 슬랩 복합체 `prospective/*` | **없음** (= 자유, VASP 기본 −1) | AFM 2424 (pm1) 또는 net4 |

`D` 는 자유롭게 푼 복합체에서 **제약된** 기체를 뺀다.

이건 우리가 2026-08-28 에 직접 데인 실수의 모양이다
(`kb/methodology/estimand_before_running_2026_08_28.md` §2.1 —
*"제약된 기준에서 자유로운 복합체를 뺐다"*). 그때 회신 O 의 처방은
*"전 계에 같은 NUPDOWN 값이 아니라 같은 **state-selection policy**"* 였다.

두 조각(SDCP repeat unit · perfluorodecane)은 닫힌 껍질이라 자유로 풀어도 일중항일
개연성이 높다 — **그러나 그 정책이 어디에도 선언돼 있지 않다.**

**★ Q2.** 다음 중 무엇이 맞는가?
- (a) 정책을 선언하고 지금 설정을 유지 — *"기체 기준은 닫힌 껍질 일중항으로 선언;
  슬랩+흡착질은 자유 바닥상태"*. `D` 는 두 조각에서 같은 정책을 쓰므로 차에서 정합.
- (b) 기체도 `NUPDOWN = −1` 로 풀고, 결과 자화가 0 인지 **확인**해서 정책을 실측으로 세운다
  (추가 비용 2잡 × 2상).
- (c) 다른 처방.

## 5. ⚠ 같이 봐 주었으면 하는 것

**⓵ 기하는 `LREAL = Auto`, 에너지는 `.FALSE.`**
`relax` 는 `LREAL = Auto`, `static` 은 `.FALSE.` 다. 판정 에너지는 `.FALSE.` 로 맞지만,
**그 에너지를 평가하는 기하는 `Auto` 힘으로 최적화된 것**이다. 0.01 eV 단위 보고에서
이 분리가 문제가 되는가?

**⓶ `EDIFFG = -0.02 eV/Å`**
0.01 eV 자리를 보고하는데 이 힘 문턱이 충분한가? (①의 5 meV 문턱과 직접 얽힌다)

**⓷ 기체 기준이 이완된다 (`NSW = 300`)**
각 조각의 기체 기준은 자기 자신의 이완 구조다. 우리는 이 값을 **adsorption energy**
(변형 포함)라 부르고 있는데, 그 명명과 정합하는가?

**⓸ `ISTART = 0` + `ICHARG = 1` (static)**
relax 의 CHGCAR 를 읽고 WAVECAR 는 안 읽는다. 의도한 것이지만 자성 계에서
**시작 자기상태가 CHGCAR 로만 전달**되는 것이 충분한가?

**⓹ `LDAUL` 자리**
ptfe `-1 2 -1 -1 -1` (5종) · sdcp `-1 2 -1 -1 -1 -1` (6종). `2` 가 Ni 자리라는 전제인데,
POSCAR 종 순서가 `Li Ni O …` 일 때만 맞다. (별도로 실측 확인 중)

**⓺ 기체 상자의 KPOINTS**
Γ 하나여야 한다. (별도로 실측 확인 중)

## 6. 우리가 답 없이는 안 하는 것

- `Δ_vac` 문턱(5 meV)을 결과를 본 뒤에 바꾸는 것
- state-selection policy 를 선언하지 않은 채 `D` 를 인용하는 것
- 12잡을 그대로 던지는 것 (①이 맞으면 vacconv 2잡의 INCAR 이 바뀐다)

## 7. 첨부

전체 INCAR 덤프(34종, 단계별 전문) · KPOINTS · POTCAR_SPEC · 잡 12개 역할표는
이 요청과 함께 보낸다. 재현:
```
python3 tools/sdcp/vasp_handoff_bundle.py --from_basins db/properties/c12_poses_2026_08_30.json \
  --frags sdcp_neutral ptfe_c10 --refs --refs_minimal --both_seeds --allow_no_pin \
  --cell_c 36.6551 --cell_c2 40.6551 --min_vacuum 15.0 \
  --roles primary sensitivity stress_sensitivity --out <새 경로>
```

⛔ 이 번들은 **제출본이 아니다** — `--allow_no_pin` 으로 만들었다 (POTCAR 원본 SHA 미확보).
POTCAR 는 포함하지 않는다(라이선스). `POTCAR_SPEC.txt` 의 변형명과 조립 스크립트만 들어 있다.
