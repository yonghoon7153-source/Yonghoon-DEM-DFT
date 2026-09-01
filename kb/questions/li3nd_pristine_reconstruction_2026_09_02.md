---
title: "Li₃Nd pristine 3×3×3 이 0.65 eV 재구성한다 — NEB 기반 구조도 같은가?"
date: 2026-09-02
updated: 2026-09-02
tags: [li3nd, sei, neb, relaxation, control, open-question]
status: open
kind: question
system: li3nd
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: single-source
---

# Li₃Nd pristine 3×3×3 이 크게 재구성한다

## 무엇을 봤나 (실측 · 진행중)

`sei_control/li3nd_mp-976264_p333_r2` (공공 없는 pristine 대조군, GPU, 2일 9시간째)

| 스텝 | E (Ry) | Total force |
|---|---|---|
| 1 | −14651.90143 | 0.1221 |
| 21 | −14652.03617 | **0.0083** ← 거의 수렴 |
| 31 | −14652.03951 | 0.0167 |
| 36 | −14652.05027 | 0.0452 |
| 42 | −14652.08412 | 0.0428 |

- 21스텝에서 문턱 근처(0.0083)까지 갔다가 **빠져나왔다.**
- 그 뒤 에너지가 **가속하며** 하강 — 42스텝에서 basin 1 대비 **−0.048 Ry = −0.65 eV**,
  아직 스텝당 ~0.006 Ry(0.08 eV) 떨어지는 중이다.
- 원자 이동: **Nd 최대 0.707 Å · 평균 0.415 Å** · Li 최대 0.617 Å (Å, 분율 아님)

## 왜 중요한가

이 대조군의 원래 질문은 *"공공 없는 pristine 셀에서도 같은 Nd 재배열이 나오는가"*
였다. **답은 나왔다 — 난다.** 그런데 크기가 예상 밖이다: 얕은 basin 이 아니라
**0.65 eV 이상 낮은 다른 구조**로 가고 있다.

즉 우리가 출발점으로 쓴 3×3×3 구조는 **국소최소가 아니었다.**

## ❓ 열린 질문 — NEB 기반 구조도 같은 불안정 위에 있나

`build_neb_inputs.load_relaxed()` 는 vc-relax 이완본을 **요구**한다 (raw MP 금지 —
li3p Ea=0 사고의 교훈). 그래서 NEB 끝점은 이완본에서 왔다. 문제는 **어느 이완본**이냐다:

- **원시셀 vc-relax → 3×3×3 복제** 였다면: 원시셀에서 안 보이는 **비-Γ 소프트 모드**가
  초격자에서 풀린 것이다 ⇒ **같은 3×3×3 위에 올린 NEB 도 같은 불안정 구조 위에 있다.**
  그러면 li3nd NEB 장벽의 기준 상태가 흔들린다.
- **raw MP → 3×3×3** 이었다면: control 정의만 문제고 NEB 은 별개다.

확인 방법 (control relax 완료 후):
```
sed -n '/CELL_PARAMETERS/,+3p' $D/00_control_relax.in     # control 출발 셀
sed -n '3,5p' db/structures/sei_li3nd_mp-976264.vasp      # raw MP 원시셀
sed -n '/Begin final coordinates/,/End final/p' <vcrelax.out>
```
control 셀 ÷ 3 이 raw 와 같은가, 이완본과 같은가.

## 아직 말하면 안 되는 것

- ⛔ "li3nd NEB 장벽이 틀렸다" — **확인 안 됨.** 위 질문이 먼저다.
- ⛔ "mp-976264 가 틀렸다" — 우리 설정(PP·U·frozen-4f)에서의 상대적 이야기다.
- ⛔ 미완료 relax 의 에너지·기하를 정량으로 인용 (force 0.043, 진행중)

## 지금 판단

**계속 돌린다.** 0.65 eV 하강 중간에 끊으면 가장 나쁜 지점의 기하가 남는다.
GPU 37.7 GB 를 계속 무는 값어치가 있다 — 우리가 몰랐던 더 낮은 구조다.

## 되짚기

- 대조군은 `run_sei_dft.sh` 의 `00_control_relax.in` 경로 (회신 I 실행순서 3)
- 이 발견은 **감시 중 우연히** 나왔다 — "2일 9시간이나 도네" 라는 1저자 질문이 출발점
