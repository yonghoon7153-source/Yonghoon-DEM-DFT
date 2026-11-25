---
title: "EC 회신 (내부 반박 리뷰) — b2o3 개정 4 · 어닐 시간 진단 도구 v2: 조건부 GO (P0 0 · P1 2 · P2 5) — gabia 블록이 결과 공개 전 도구 고정을 기계로 안 지킨다 · 끝 구조만 걸린 100 ps 이완 실패가 성공 집합 규칙을 비켜 간다"
date: 2026-11-10
updated: 2026-11-10
tags: [review, b2o3, doping, uma, anneal, placement, internal, reply, letter]
letter: EC
track: b2o3
channel: internal
kind: reply
status: 수령 2026-11-10 — 원문 그대로 (에이전트 최종 보고 · 저장소 파일 안 고침 · 합성 에너지 · 실제 크기 사슬로 재현)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = b2o3 UMA-MD (1저자 = 사용자). 프롬프트 `internal_EC_prompt_b2o3_amend4_diag_v2_2026_11_10.md` (Codex 토큰이 없어 내부 독립 리뷰 에이전트로 보냈다).
> 아래는 리뷰 에이전트의 최종 보고 **원문 그대로**다. 재현에 쓴 스크래치 파일은 세션 스크래치에만 있다 (저장소 밖).

# EC 회신 (내부 반박 리뷰): b2o3 개정 4 · 어닐 시간 진단 도구 v2

**기준 판:** 브랜치 `claude/friendly-meitner-lldvar`, HEAD c60c20a8. b2o3 쪽 파일(진단 도구 · 판독기 · run_anneal · 실행기 · 카드 · 런로그)은 fd3cdc45 와 바이트까지 같습니다.
- 진단 도구 sha256 2dc493aa…, 판독기 872d91f7… (판 고정과 일치), run_anneal d12e120f…

**재현 조건:** 전부 합성 에너지와 6 원자 시험 구조로 했고, 8 단계 실제 결과는 보지 않았습니다. 사슬은 실제 크기(바탕 18 × 가족 3 = 54, G1 15/18)이고 판 고정 판독기를 그대로 씁니다. UMA · GPU · 원격 기계는 쓰지 않았습니다. 저장소는 고치지 않았습니다 (git status 0 줄).

**selftest 재현:** 진단 도구 49/49, 판독기 69/69, 실행기 `--selftest` queue 6/6 + inputs 3/3. 실행기 `list_inputs` 코드에 진단 manifest 를 그대로 넣으면 입력 53 개와 목적 `b2o3_bo/anneal_diag_t050` 이 제대로 넘어갑니다.

## 1. 판정: 조건부 GO

해제 조건별로 보면 이렇습니다.
- **① 판정 사유 분리:** 채웠습니다.
- **② 성공 집합 불일치 처리:** 규칙 자체는 채웠습니다. 다만 런을 집합에 넣기 전의 부모 상태 분류에 구멍이 하나 있습니다 (P1-2).
- **③ 결과 공개 전 결속 · 정상/음성 경로:** 데이터 사슬 결속은 채웠습니다. 그러나 gabia 블록이 "결과 공개 전 도구 고정"을 기계로 지키지 않습니다 (P1-1). 기록 계산은 맞지만 시험이 그 계산을 지키지 않습니다 (P2-1).

**GO 조건:** P1-1 과 P1-2 를 결과를 열기 전에 고칩니다. 도구 v3 · 카드 · 런로그 블록을 고쳐 커밋하고, 사용자 비준을 받은 뒤 ① 을 엽니다. 결과를 연 뒤에는 규칙을 못 바꾸므로, P2 도 같은 커밋에 넣기를 권합니다.

## 2. P0 / P1 / P2

**P0:** 없습니다.

### P1-1. gabia 블록이 "결과 공개 전 도구 고정"(EA P2-2)을 지키지 않습니다

위치:
- 런로그 `db/properties/b2o3_bo_placement_stage1_runlog_2026_11_09.json:206–213`
- `tools/doping/b2o3_bo_readout.py:1222–1226`
- `tools/doping/b2o3_bo_anneal_diag.py:168–173 · 379–387`

무엇이 틀리나:
- **(가) 순서:** ① 본 판독이 ② worktree 보다 먼저입니다. 그런데 ① 은 결정 줄(`승자 F … ≥ 0.2`)을 화면에 찍습니다 (readout.py:1225). ② 는 `fetch … FETCH_HEAD` 이고, ⛔ 줄이 "v2 가 든 커밋 **이상**"을 허용합니다. 그래서 100 ps 승자를 본 뒤에 고친 도구를 받아도 블록이 막지 않습니다.
- **(나) 지문 없음:** 출력 둘(diag_frames.json · s8b_diag.json)에 진단 도구 자신의 sha 나 커밋이 없고 `readout_tool` 만 있습니다. judge 는 자기가 부른 판독기 sha 를 extract 때 기록과 견주지도 않습니다.
- **(다) 비준 확인 없음:** 결정 D-2026-11-10-b2o3-bo-placement-amend4-ea 는 proposed 인데, ① 앞에 비준을 확인하는 줄이 없습니다 (산문뿐).
- **(라) 낡은 줄:** ⚠ 줄(211)이 아직 개정 3 의 "잠정 규칙"을 가리킵니다.

재현: probes2.py (라). diag_frames.json 최상위 키는 `[card, frames, inputs, kind, n_frames, parent_status, plan_n, purpose, readout_tool, t_a_ps, t_diag_ps]` 이고, judge 출력에도 진단 도구 지문이 없습니다.

최소 고침:
1. ⓪ 원장에서 amend4 가 active 인지 확인하고, 아니면 멈춥니다.
2. ② 를 ① 앞으로 옮깁니다: `git -C /data/work/repo worktree add --detach $R/diag_src <고친 커밋 해시>`.
3. sha256sum 으로 진단 도구 해시와 판독기 872d91f7… 을 확인하고 런로그에 적습니다.
4. 그 다음 ① → ③ → ④ → ⑤ 순서로 갑니다.
5. 도구 쪽: extract 가 `diag_tool {path, sha256}` 을 출처에 쓰고, judge 는 진단 도구와 판독기 sha 가 출처와 같을 때만 진행합니다. 판독 출력에도 둘 다 적습니다.

### P1-2. 끝 구조만 검사에 걸린 100 ps 이완 실패는 50 ps 프레임을 못 받고, 그래서 성공 집합 규칙을 비켜 갑니다

위치:
- `b2o3_bo_anneal_diag.py:118–119` (`if r.get("vo"): return "parent_unverified"`) 와 PARENT_WHY(64–65)
- 카드 `실패_처리_Q6` (`b2o3_bo_placement_estimand_2026_11_09.json:335`)

무엇이 틀리나:
- vo 하나에 post_md · post_relax · md_traj 검사 결과가 같이 들어갑니다.
- 끝 이완이 발산해 post_relax 에 NaN 이 생기면, 궤적이 멀쩡해도 parent_unverified 가 됩니다. 그러면 프레임이 없고, 그 런은 "두 시점 실패"로 세어져 집합이 같아집니다.
- 같은 런이 유한한 미수렴이면 relax100_failed 가 됩니다. 그러면 프레임을 떼고, 50 ps 이완이 성공해 집합이 달라지고 ④ 가 나옵니다.
- 즉 실패 모양에 따라 ① 과 ④ 가 갈립니다. 이 경우 사유 문장 "궤적을 믿지 않는다"도 사실과 다릅니다.
- EA Q6 은 "100 ps 끝 이완 실패"와 "부모 MD 궤적 부재"를 구분하라고 했는데, 카드의 "출력 검증 실패 → 프레임 없음"이 이 축과 어긋납니다.

재현 (scenarios.py · 합성 · 나머지 53 런은 같고 F_B 가 1.0 차 승자):

| 경우 | 부모 상태 | 집합 | 사유 |
|---|---|---|---|
| relax100_unconverged (F_free b5 미수렴 · 유한) | relax100_failed | 다름 | ④ |
| relax100_nan (같은 런 · post_relax NaN · sha 맞춤) | parent_unverified · 프레임 없음 | 같음 | ① "두 시점에서 같은 가족 (F_B) 이 선택됐다" |

relax100_nan 런의 vo 는 `['post_relax 좌표에 NaN · inf']` 하나이고, 판 고정 `_verify_md_traj` 만 돌리면 `[]` (궤적 멀쩡) 입니다.

빈도: 드뭅니다 (6 단계 실패 0/135). 그래도 결과를 연 뒤에는 못 고치는 규칙이라 지금 닫아야 합니다.

최소 고침:
- 부모 상태를 궤적 검사로 가릅니다: `RD._RA._verify_md_traj(결과 JSON 의 원 기록, md_traj, base, n_atoms)`.
  - 문제가 있으면 parent_unverified.
  - 없으면 ok100 또는 relax100_failed (끝 구조 · 에너지 문제 포함), 사유는 vo 원문.
- 빠른 대안: vo 항목 중 `"md_traj"` 가 든 것만 parent_unverified 로 봅니다.
- 시험 추가: post_relax NaN · post_md sha 불일치 (궤적 멀쩡) 는 프레임을 떼고, md.traj 변조는 안 떼는지 봅니다.
- 카드도 고칩니다 (4 절 문장 A).

### P2-1. 기록 (EA P2-1 · Q2 · Q4) 계산은 맞지만 selftest 가 지키지 않습니다

- 위치: selftest 의 기록 검사(588–600)는 모든 Δ 가 −0.1 로 같은 자료 하나뿐입니다.
- 재현 (mutate.py · mut2_reorder.sh): 깨기 25 개 중 14 개는 빨강, **11 개가 살아남았습니다.** 살아남은 것:
  - δ 부호를 Δ_G − Δ_F 로
  - 최저 간 차 변화의 부호
  - min ↔ max
  - 내려간 · 올라간 런 수 뒤바꿈
  - IQR 0 고정
  - 최저 기록의 시점 50 ↔ 100
  - 짝 판정의 시점 50 ↔ 100
  - 가족 중앙 E 를 E_100 만으로
  - 끝 꼴 바뀐 수 0 고정
  - ① 문장의 가족 이름 고정
  - ⑤ 를 ④(집합) 뒤로 옮긴 진짜 순서 바꿈
- 카드의 "깨기 22/22"는 하네스가 저장소에 없어서 재현하지 못했습니다.
- 지금 코드 자체는 맞습니다 (Q4 의 손계산 대조).
- 최소 고침: EA 반례 셋 (same_drift · common_per_base_drift · outlier_minimum) 을 실제 사슬에 넣고 손계산 값과 대조합니다. 거기에 "⑤ + 집합 다름 → ⑤" 시험과 끝 꼴 바뀐 런 하나를 더합니다.

### P2-2. md.log 구간 평균이 다시 돈 런에서 두 시도를 섞습니다

- 위치: diag 277–291 · run_anneal.py:134–140
- ASE MDLogger 는 mode "a" 로 덧붙여 쓰고 (3.29 확인), md.traj 는 mode "w" 로 덮어씁니다.
- 재현 (mdlog_two_attempts):
  - 첫 시도 0–60 ps 가 +5 eV 위에 있고, 같은 폴더에서 0–100 ps 를 다시 돌린 경우입니다.
  - [40,50] 구간 줄이 22 개 (한 시도면 11 개) 로 잡힙니다.
  - Epot 변화가 −2.45 로 나옵니다 (참 +0.05). 경고 표지도 없습니다.
- 대안이 있습니다: 판 고정 `anneal_one` 의 md.traj 프레임에는 Epot 과 운동량이 같은 1 ps 간격으로 실립니다 (traj_energy · EMT 6 프레임에서 md.log 와 Epot · T 일치).
- 최소 고침: 구간 평균을 sha 로 묶인 md.traj 에서 냅니다 (`get_potential_energy` · `get_temperature`). md.log 는 대조로만 씁니다.
- gabia 에서 UMA 궤적에도 에너지가 실렸는지 `T[50].get_potential_energy()` 한 줄로 확인합니다 (읽기만).

### P2-3. 진단 이완의 일시 실패 (failed · 예외) 를 50 ps 실패로 세어 ④ 를 냅니다

- 재현 (probes2.py (가)): failed 기록 하나를 judge 가 그대로 받고, F_free 집합이 달라져 ④ 가 나옵니다.
- run_anneal 은 failed 를 "끝난 것 아님 · 다시 돈다"로 봅니다 (435–437).
- 런로그 블록의 ⑤(210) 앞에는 ④ 큐의 run_rc · check_rc 조건이 없습니다.
- 최소 고침: judge 가 failed 를 누락처럼 거부합니다. 블록 ⑤ 앞에 "run_rc=0 · check_rc=0" 을 넣습니다. 50 ps 실패로 세는 것은 미수렴만입니다.

### P2-4. 출력 문장이 결론의 한계를 덜 싣습니다

- **(가) 부인 문구:** ① 문장(67–69)과 출력 ⚠ (DISCLAIMER 74–75) 에 "전체 가족 순서 · 같은 최저 런 · 같은 구조 골짜기를 뜻하지 않는다"가 없습니다. 카드 ⛔(323)와 docstring 에만 있습니다.
  - same_drift 에서 ① 인데 F_B 최저 런이 b0 → b17 로 바뀝니다.
  - runner_up_changed 에서 ① 인데 차점이 F_P → F_free 로 바뀝니다.
- **(나) ③ 사유:** ③ 사유(195–197)가 50 ps 최저 가족을 적지 않습니다.
  - margin_other_lowest: 50 ps 에서 F_P 가 0.15 차로 최저, 100 ps 는 F_B 0.40 승자.
  - margin_only: 50 ps 에서도 F_B 가 0.10 차로 최저.
  - 두 경우가 같은 문구로 나옵니다.
- **(다) 분포 · 짝:** EA Q2 가 말한 "분포 · 짝을 최저 판정 옆에"가 verdict 객체에 없습니다. outlier_minimum 은 ① 인데 짝 1/18, 중앙 F_B 0.2 > F_P 0 입니다.
- 고침: 부인 한 줄 추가 · ③ 에 50 ps 순서와 최저 가족 · verdict 에 두 시점의 pairs 와 family_median_E (게이트 아님).

### P2-5. 결속의 작은 빈틈 (대부분 손으로 변조해야 열리는 경로)

- **(가) 기하만 대조:** 프레임 → 이완 입력 대조가 기하만 봅니다 (judge 350). probes2 (나) 에서 FixAtoms 를 붙이고 출처 sha 를 맞추면 통과합니다. 고침은 judge 가 프레임을 다시 써서 바이트 sha 를 견주는 것입니다. 같은 환경에서 다시 쓴 sha 는 원 추출과 같고, 변조 파일과는 다릅니다.
- **(나) `--readout` 이 선택:** 빼면 ① 에서 연 본 판독 파일과 묶이지 않습니다 (main 736). 필수로 바꿉니다.
- **(다) OUTNAME 실수:** ④ 의 OUTNAME 을 잘못 s8_anneal 로 주면, run_batch 가 8 단계 결과 파일을 다시 써서 (463–473) 결속이 깨지고 원 바이트로 되돌릴 수 없습니다. ④ 앞에 `[ ! -e $R/s8b_relax ]` 확인을 넣고, 결과 sha 를 런로그에 적어 둡니다.
- **(라) 감시 화면:** 8 단계 감시 스크립트(run_uma_kgy.sh:98)는 이완 중인 런의 relax.log 마지막 줄 (FIRE 에너지) 을 찍습니다. "진행 신호만"이 감시 자체로는 보장되지 않습니다.
- **(마) 저장 간격:** 한 런의 저장 간격이 50 ps 의 약수가 아니면 extract 전체가 멈춥니다 (le3000). 실제 8 단계는 모두 500 걸음이라 해당 없고, 메모만 남깁니다.

## 3. Q1–Q6

**Q1. 사유 다섯 갈래의 순서 · 문장**
- 평가 순서 ⑤ → ④(집합) → ④(보류) → ③ → ② → ① 은 코드(183–202)와 카드(301–323)가 같습니다.
- 실제 크기 사슬에서 나온 사유:

| 경우 | 사유 | 비고 |
|---|---|---|
| margin_only | ③ | "바뀌" 없음 |
| unavailable_50 | ④ | 집합 다름이 먼저 걸림 |
| 집합 같음 + 50 ps 최저 끝 꼴 미분류 | ④ | 50 ps 보류 |
| runner_up_changed | ① | "순서" 없음 |
| 100 ps 못 가름 + 집합 다름 | ⑤ | ⑤ 가 먼저 |

- ① 은 전체 순서를 함의하지 않습니다. 다만 그 부인이 출력에 없고, ③ 의 정보가 모자랍니다 (P2-4). 순서 시험에도 공백이 있습니다 (P2-1).

**Q2. 성공 집합 규칙의 반례**
- EA 의 가짜 일치 (false_same_winner) 와 가짜 역전 (false_time_reversal) 은 둘 다 ④ 로 나옵니다.
- 이름 집합 규칙 자체의 반례는 못 찾았습니다. 구멍은 집합에 넣기 전 분류에 있습니다 (P1-2).
- relax100_failed 런 하나로도 50 ps 이완이 수렴하면 ④ 가 나옵니다. 설계대로의 결과이고, 시간 효과가 아닙니다.
- 시작 없음 · 부모 failed · 궤적 검사 실패는 두 시점 모두 실패로 세어 집합이 같아집니다. 이건 맞습니다.
- 진단 이완의 failed 를 판정으로 세는 것은 틀렸습니다 (P2-3).

**Q3. 결속에 조용히 틀릴 경로가 있는가**
- 확인한 사슬:
  - 계획 ↔ 부모: anneal_readout (계획 밖 · 누락 · 정체성 · 시작 sha · 목적 · 시간 · 설정 · base seed), 이름 유일, judge 에서 (바탕, 가족) 대조.
  - 시간 → 프레임: 기록의 dt × 저장 간격. 프레임 수 검사 때문에 50 ps 를 다른 정수 프레임으로 만드는 저장 간격은 없습니다.
  - 프레임 → 입력: 부모 궤적을 다시 읽어 1e-6 Å 로 대조하고 파일 sha 도 봅니다.
  - 입력 → E_50: 정체성 (단계 · 시작 sha · 설정 · time_ps 0 · 목적), 새 폴더, 유한 E_post_relax.
- 빈틈은 P1-1 (나) 와 P2-5 (가)(나), P2-2 입니다.

**Q4. 기록이 EA 요구를 채우는가**
- 손계산 대조를 통과했습니다:
  - same_drift: Δ F_B 중앙 −0.4 · 최솟값 −3.0 · max|Δ| 3.0 · 최저 런 b0 → b17 (Δ −0.4 / −3.0) · m_F_P − m_F_B 0.30 → 2.05.
  - common_per_base_drift: δ 는 전부 0 인데 m_F_P − m_F_B 가 0.30 → −0.50, 사유 ②.
  - δ 부호: 바탕 17 에서 −2.6 = Δ_FB − Δ_FP.
- 내용은 EA P2-1 · Q2 · Q4 를 채웁니다. 남은 것은 시험 공백 (P2-1), md.log 섞임 (P2-2), "옆에" 표시 (P2-4 다) 입니다.

**Q5. gabia 블록의 판독 순서가 지켜지는가**
- 아닙니다. 이유는 P1-1 그대로입니다: ① 이 먼저 결과를 찍고, 도구 fetch 는 "이상"을 허용하고, 비준 확인과 도구 지문이 없고, ⚠ 줄이 낡았습니다.
- 감시 화면이 이완 에너지를 보일 수 있다는 점도 덧붙입니다 (P2-5 라).

**Q6. 시험이 실제로 깨진 경우를 잡는가**
- EA 가 명시한 음성 시험은 있습니다: 다른 런 프레임 · 49 ps · 저장 간격 · 스냅숏 교체 · 미수렴 · 비유한 E_50 · 한 시점만 실패 · 정상 경로.
- 빠진 시험:
  - 기록 수치 (P2-1)
  - ⑤ 와 ④(집합)의 순서
  - 끝 구조만 걸린 부모 (P1-2)
  - md.log 덧붙임
  - 진단 이완 failed
  - 프레임 파일의 제약 · 배열 변조
  - 출력의 진단 도구 지문

## 4. 카드에 넣을 문장

**A. 실패_처리_Q6 를 대체:**
"부모 상태는 궤적으로 가른다 — 시작 없음 (6 단계 실패) · 부모 실패 (상태 failed · 기록에 궤적 결속 없음) · 부모 궤적 무효 (md_traj 없음 · run_anneal 궤적 검사 실패) → 50 ps 프레임 없음 · 두 시점 실패 · 궤적이 검사를 통과하면 100 ps 끝 이완이 미수렴이든 · 끝 구조 파일 (post_md · post_relax) 이 검사에 걸리든 · 에너지가 비유한이든 '100 ps 끝 이완 실패' 로 50 ps 프레임을 떼어 이완한다 (가능한 50 ps 결과를 버리지 않는다 — 회신 EA Q6 · EC P1-2)"

**B. 판독_순서_P2_2 에 덧붙임:**
"기계 순서 (EC P1-1): ⓪ 결정 D-2026-11-10-b2o3-bo-placement-amend4-ea 가 active 인지 원장에서 확인 (아니면 멈춤) → ② 진단 도구 worktree 를 커밋 <해시> 로 고정 · b2o3_bo_anneal_diag.py sha256 과 판독기 sha256 872d91f7… 를 확인해 런로그에 적는다 → ① 본 판독 → ③ → ④ (run_rc 0 · check_rc 0 일 때만 다음) → ⑤ · 진단 도구는 자기 sha256 을 출처와 판독 출력에 적고 judge 는 extract 때와 같은 진단 도구 · 판독기 sha 일 때만 진행한다 · 'v2 이상' (이후 아무 커밋) 은 쓰지 않는다"

**C. 진단 이완 실패:**
"진단 이완의 failed (예외) 는 누락처럼 다룬다 — 같은 출력 폴더 · 같은 설정으로 다시 돌려 check_rc 0 이 된 뒤 판독한다 · 미수렴만 50 ps 실패로 센다 · 100 ps 미수렴 런 하나로도 ④ 가 될 수 있다 (시간 효과가 아니다)"

**D. ① 의 한계 (문장 끝과 판독 출력 ⚠ 에도):**
"① 은 같은 초기 가족의 선택까지다 — 전체 가족 순서 · 같은 최저 런 · 같은 구조 골짜기의 유지를 뜻하지 않는다"

**E. ③ 의 기록:**
"③ 에는 50 ps 의 가족 순서와 최저 가족을 같이 적는다 — 50 ps 최저가 100 ps 승자와 다른 가족이어도 ③ 이다 ('여유 부족' 을 '같은 쪽 · 작은 차' 로 읽지 않는다)"

**F. md.log 진단:**
"구간 평균은 sha 로 묶인 8 단계 md.traj 프레임의 Epot · 운동량 (md.log 와 같은 1 ps 간격) 에서 낸다 — md.log 는 ASE 가 덧붙여 써서 (mode 'a') 다시 돈 런의 두 시도가 섞인다 (EC 재현) · md.log 는 대조로만"

## 5. 재현에 쓴 스크래치 파일

폴더: `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EC/`

- **사슬:** `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EC/chain.py` — 실제 크기 사슬 (생성 manifest → 거름 → 파일럿 → 영수증 → 8 단계 md_traj → extract → 진단 이완 → judge)
- **EA 반례 · 부모 상태 · md.log 시나리오:**
  - `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EC/scenarios.py`
  - `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EC/scenarios.log`
  - `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EC/scenarios_out.json`
- **failed 진단 이완 · FixAtoms 변조 · 도구 지문 탐침:**
  - `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EC/probes2.py`
  - `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EC/probes2_out.json`
- **깨기 시험:**
  - `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EC/mutate.py`
  - `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EC/mutate.log`
  - `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EC/mut2_reorder.sh` (⑤ 를 ④ 뒤로 옮긴 판)
- **selftest 로그:**
  - `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EC/diag_selftest.log`
  - `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EC/readout_selftest.log`
- **실행기 list_inputs 대조:**
  - `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EC/list_inputs_snippet.py`
  - `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EC/runner_probe/`
- **md.traj 의 Epot 과 md.log 대조 (EMT):** `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/ae97ed2c-08ef-5fe9-8fcd-7033671673cd/scratchpad/review_EC/traj_energy/`
