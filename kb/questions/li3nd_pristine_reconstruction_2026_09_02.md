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

## Evidence For — 출발 구조가 최소가 아니었다

**2026-09-02 확인 완료. 답: 그렇다.**

```
control 셀      11.0008710 = 3 × 3.666957     ← 정확히 3×3×3
raw MP 원시셀    3.6669570
vc-relax 최종    3.666957                      ← raw 와 **완전히 동일**
```

- vc-relax 가 셀을 **소수점 7자리까지 하나도 안 움직였다.**
- 이완 좌표가 전부 이상적 고대칭 자리다 (Li at a/2·3a/2 …).
- ⇒ **대칭이 힘을 0으로 만들어 이완기가 즉시 '수렴' 했다.** 힘이 0인 점은 최소일
  수도 안장일 수도 있는데, 우리는 그 둘을 **구분한 적이 없다.**
- 3×3×3 에서 대칭이 깨질 여지가 생기자 0.65 eV 를 굴러떨어지고 있다.
- 원자 이동 Nd 최대 0.707 Å — Li 홉과 **같은 길이 규모**다.

## Evidence Against — 아직 장벽이 틀렸다고 못 하는 이유

- 장벽은 경로 위의 **차이**다. 끝점과 안장이 같은 격자를 공유하면 오차가 부분 상쇄된다.
- `build_neb_inputs.load_relaxed()` 는 raw MP 를 **거부**한다 (li3p Ea=0 사고의 교훈이
  코드에 박혀 있다) — 절차 자체는 지켜졌다. 문제는 그 '이완본' 의 성격이지 절차가 아니다.
- NEB 끝점은 **공공을 넣고 다시 이완**했다. 그 과정에서 재구성을 겪었을 수 있고,
  그랬다면 NEB 은 재구성된 격자 위에서 내부적으로 일관된다.
- 이 대조군 자체가 **아직 진행중**이다 (force 0.043). 최종 구조를 모른다.

## 결정 실험

**NEB 끝점 이완이 같은 미끄러짐을 겪었는가.**

```bash
for R in /data/work/runs/sei_neb_v2 /data/work/runs/sei_neb_v3 /data/work/runs/sei_neb_v2_cc333; do
  for E in $R/li3nd/ep_*; do
    [ -d "$E" ] || continue
    echo "=== $E"
    grep -a "^!    total energy" $E/relax.out 2>/dev/null | sed -n '1p;$p'
    grep -a "Total force"        $E/relax.out 2>/dev/null | sed -n '1p;$p'
  done
done
```

- 끝점 에너지가 **0.6 eV 급으로 하강** → 끝점이 재구성을 겪었다. NEB 은 재구성된
  격자 위에서 일관되고, 장벽은 살아 있을 가능성이 크다. (단 '어느 상태에 대한
  장벽인가' 를 원고에 명시해야 한다.)
- **거의 하강 없음** → 끝점이 미재구성 격자에 머물렀다. 그 위의 장벽은 **불안정한
  기준 상태에 대한 값**이고, Nd 0.7 Å 재구성이 Li 홉과 같은 규모라 무시할 수 없다.

두 번째 확인 (선택): 재구성된 최종 구조로 **끝점을 다시 이완**해 장벽이 바뀌는지 본다.

## ❓ 남은 질문 — 파이프라인 일반의 구멍

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

## Status Log

- **2026-09-02** 개설. control relax 감시 중 발견 (1저자 질문 "2일 9시간이나 도네" 가 출발점).
  같은 날 Evidence For 확정 — vc-relax 가 셀을 전혀 안 움직였고 좌표가 고대칭 자리다.
  결정 실험(끝점 relax 궤적 확인) **미실행**. control relax 진행중.

## 되짚기

- 대조군은 `run_sei_dft.sh` 의 `00_control_relax.in` 경로 (회신 I 실행순서 3)
- 이 발견은 **감시 중 우연히** 나왔다 — "2일 9시간이나 도네" 라는 1저자 질문이 출발점
- ⚠ **파이프라인 일반의 구멍**: 우리는 vc-relax 수렴을 '바닥상태' 로 취급해 왔는데,
  고대칭 구조에서는 힘이 대칭으로 0이 되어 **안장에서도 수렴한다.** 동역학적 안정성
  (포논) 이나 대칭 깨짐 섭동 시험을 한 적이 없다. li3nd 만의 문제가 아닐 수 있다 —
  다른 SEI 상(li2s·li3p·li3po4γ·li2o)도 같은 방식으로 이완됐다.
