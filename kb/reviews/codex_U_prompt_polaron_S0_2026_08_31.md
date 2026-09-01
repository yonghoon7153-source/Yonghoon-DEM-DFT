---
title: "리뷰 요청 U — 폴라론 S0 재제출 (회신 T P0 4건 + 해제조건 6 이행)"
date: 2026-08-31
updated: 2026-08-31
tags: [review, codex, sdcp, polaron, orca, pilot, prompt]
status: 발송 대기 (⚠ 라벨 U 가 재사용됨 — 인용 횟수는 codex_U_prompt_neutral_close_plan 과 합산되므로 근거가 아니다)
kind: review-request
system: sdcp
confidence: high
verificationStatus: unverified
explored: false
authoredBy: agent
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 요청 U — 폴라론 S0 (H-제거 n=6 라디칼)

> 이전 회신: `kb/reviews/codex_T_reply_polaron_pilot_2026_08_31.md`
> (NO-GO · P0 4건 · 해제조건 6건 · ε=1 기술적 적합성 pilot **S0** 로 격하)
> **ORCA 는 아직 한 잡도 돌리지 않았습니다.**

## 0. 이번엔 실물을 같이 보냅니다

회신 T 에 "실제 `.inp/.loc/job.json` 을 받지 못했고 문서의 수치·설계만 보고
판정했다" 고 명시해 주셨습니다. 이번에는 **생성된 입력 전부**를 첨부합니다.

```
sdcp_polaron_S0_inputs.zip
sha256  39dcc959a7a30cd87e64b8d84fe37b609f4fca2392123cf07e507eeb29ac0c4d
파일 10 · 26,968 B
```

| | |
|---|---|
| MANIFEST_PILOT.json sha256 | `e264e5578692599df6702d12e14c4aaf77322a234443b66b6fa65f3eb50c7740` |
| builder sha256 | `3faca7ced14043848f47250924ff91b3029ef3090d26d416f8b1da65e89c1b72` |
| builder commit | `9bbf22de4ed1fa978eb5016c6e4003cf1525b727` |
| 부모 구조 | `dp6_gs0_neutral_final.xyz` · `b49076980623185cdde983dba64acc11a73021293b0886e263aee618a8de5085` |

⚠ phase S 입력은 아직 없습니다 — **설계상** phase L2 를 실행해 국재 궤도 인구를 읽은
뒤에만 만들어집니다 (미리 만들면 임의 MO 를 고르는 것이고, 그건 국재화가 아닙니다).
첨부는 phase L(2잡) · L2(2잡) 입력과 manifest 입니다.

## 1. 🔴 먼저 보고드릴 것 — **세 실행 경로가 전부 죽어 있었습니다**

회신 T 의 P0 1~3 을 고치는 과정에서 넣은 회귀입니다. 이행을 확인하려고 실제로
돌려 보고서야 드러났습니다:

| 경로 | 증상 |
|---|---|
| `--polaron_pilot` (생성기) | `_loc_rand` 를 선언 **전에** 참조 → `UnboundLocalError`. 아무것도 만들지 못하고 죽었습니다 |
| `--polaron_seeds` (seed 생성) | `pil_parse_mopop` 의 4-튜플을 3개로 언팩 → `ValueError`. 게다가 성격 판정용 `_sy_j`·`_po_j` 가 아예 정의되지 않았습니다 |
| `--polaron_analyze` (분석기) | `_spin_block` 은 **리스트**를 돌려주는데 Q3 네 성분 코드가 `hir.values()`·`hir.get(i)` 로 dict 처럼 써서 `AttributeError`. 그리고 목표 링 이름을 `"ring" + "B_ring0"[2:]` = `"ringring0"` 으로 조립해 2층 명중이 **영원히 False** 였습니다 |

**그런데 당시 selftest 40건은 전부 통과했습니다** — 순수 헬퍼만 부르고 세 함수를
한 번도 실행하지 않았기 때문입니다. 회신 R2 에서 지적하신 *"23 PASS 는 문자열
selftest 이지 e2e 증명이 아니다"* 가 이 캠페인에서 그대로 재현됐습니다.

이제 합성 다이머(26원자 · 링 2 · SO₃ 2)로 phase L/L2/S/probe 산출물을 만들어
**세 경로를 실제로 돌립니다**. selftest **40 → 152건**.

음성 경로: 무작위 국재화 표지 · `GuessMode` 누락 · MOPOP 부재 · 면내 σ MO ·
비정상 종료 · 출력 삭제 · `.loc` 삭제 · 프레임 바꿔치기 · 구판 manifest ·
개입 실패 · probe 결측 · 링 미분해 · 불안정 미재판정 · `StabPerform` 미수행 ·
`.gbw` 없는 재계산 요청 · 코어/가상 MO 가 seed 로 뽑히는 것 · 셀/런처를 랭크로 세는 것.

## 2. P0 4건

### P0-1 200원자 집합을 199원자 D 계에 사용

`atom_manifest` 에 **P(200) / D(199) 를 각각 봉인**하고 remap 을 자체 해시로 남깁니다.
seed 생성이 그 프레임에서 **직접** 목표 집합을 꺼내고, 인덱스가 계의 원자수를 넘으면
거부합니다. 그리고 성격 판정용 원소·좌표를 **그 계의 xyz 에서** 읽습니다
(원자수가 어긋나면 거부 — 위 §1 의 두 번째 회귀가 여기였습니다).

⚠ **정정**: 제거 H 는 124 가 아니라 **162**(1-based) / 161(0-based)입니다.
산성 H 후보가 `[119, 134, 148, 162, 176, 190]` 이고 사전 규칙(중간 위치)이 고르는 것이
162 입니다. 따라서 remap 경계도 `i < 161 → i` · `161 → absent` · `i > 161 → i−1` 입니다.

원자 수는 주신 네 줄과 **전건 일치**합니다:

| 분할 | P (중성/P⁺) | D⁻·D• |
|---|---|---|
| extended (ether O 포함) | 44 / 30 / 126 = 200 | 44 / **29** / 126 = 199 |
| ether 제외 | 32 / 30 / 138 = 200 | 32 / **29** / 138 = 199 |

### P0-2 97–99% 국재는 π 의 증거가 아니다

`pil_mo_character()` 를 넣었습니다. AO 라벨별 인구를 읽어

- `p_frac` — 목표 집합 인구 중 p 성분 비율 (s 지배면 σ)
- `pi_share` — 그 p 밀도 중 **고리 법선** 방향 비율. 최소제곱 평면 법선 n̂ 에
  대해 `Σ n̂_k² p_k / Σ p_k` (Löwdin 인구가 |c|² 꼴이라 성분별 대각 근사)
- `O_frac` — sulfonate seed 용

문턱은 **결과 보기 전에** 봉인했습니다: `p_frac ≥ 0.60` · `pi_share ≥ 0.60` ·
`O_frac ≥ 0.70`. 미달이면 seed 를 **만들지 않고** 멈춥니다.

⛔ ORCA 가 p 를 축 없이 찍으면 `axis_resolved=False` 이고 그것은 **통과가 아닙니다**
(`MO_CHARACTER_UNRESOLVED`).

"MO 480 = HOMO" 오표현도 고쳤습니다 — 목표는 **그 계(D•/P⁺)의 베타 첫 빈자리**이고,
부모 닫힌껍질 HOMO 와 우연히 같을 뿐이라 명시 계산합니다 (D• 961전자 doublet →
Nα/Nβ = 481/480 ⇒ 첫 빈자리 480).

### P0-3 결정론 국재화 옵션이 실제로 있다

맞습니다. **`%loc Randomize 0`** 이 primary 가 됐습니다. 무작위 realization 은
`--loc_realization random` 으로 명시했을 때만 R1(민감도)로 허용하고, 출력에서
무작위 표지를 찾으면 선언과 대조해 막습니다.

그리고 `.loc` 를 읽는 입력에 **`GuessMode CMatrix`** 를 넣었습니다.
⛔ 이것이 셋 중 결과를 **조용히** 틀리게 만드는 유일한 항목이라고 봅니다 —
`GuessMode` 기본값은 에너지 정렬을 전제하는데 국재 궤도에는 물리적 에너지 순서가
없고, 우리 seed 는 `.loc` 인구표의 **인덱스**로 목표를 지정하므로 재정렬되면
`Rotate {j, 480}` 이 엉뚱한 궤도를 돕니다. 첨부한 L2 입력에서 확인하실 수 있습니다.

### P0-4 ring5 와 default 는 같은 seed 다

⚠ **실물은 다릅니다.** `moread=(None if sd == "default" else gbw)` 이라 `default` 는
`%moinp` 도 `Guess MORead` 도 없는 **fresh guess** 입니다 — 같은 초기 determinant 가
아닙니다.

⛔ 다만 **job 레코드가 default 에도 `orbitals_from`·`loc_sha256` 를 찍고 있었습니다.**
읽지도 않는 파일을 출처로 기록한 것이고, 그렇게 읽히신 것이 무리가 아닙니다.
레코드를 고치고 `seed_equivalence_class` (`fresh_guess` / `localized_no_rotation` /
`localized_rotated`)를 명시했습니다.

또한 고른 MO 가 **베타 첫 빈자리 자신**이면 `Rotate {480,480}` 이 되어 무의미하므로
회전을 생략하고 `rotate_skipped_why` 를 남깁니다.

## 3. 해제조건 Q1~Q4

**Q1 S0 격하 — 채택.** `db/properties/sdcp_polaron_pilot_prereg_S0_2026_08_31.json`
(원본 사전등록은 **보존**합니다 — 무엇을 하려 했는지가 격하의 근거이므로).
환경 3 → ε=1 하나 · 범함수 2 → r2SCAN-3c 하나 · Opt·branch following·λ_in·BLA 전부
범위 밖 · 산출물을 "상태지도" 에서 **"이 방법이 상태를 구분해 낼 수 있는가"** 하나로.
새 해시·새 시각으로 다시 봉인했습니다 (빌더가 바뀌어 원본 해시로 이 실행을 설명할 수
없으므로).

**Q2 `LOCALIZATION_DEPENDENT` — 추가.** R0(결정론)과 R1(무작위)이 다른 최종 basin
집합을 주면 이 판정어로 닫습니다. `.loc` 해시 결박은 정확한 재실행에 필요하지만
robustness 를 대체하지 않는다고 사전등록에 적었습니다.

**Q3 네 성분 분리 — 채택.** `bb_core` / `ether_O` / `sulfonate` / `other` 로 나누고
strict(bb_core) 와 extended(bb_core+ether_O) 를 **둘 다** 냅니다. class 가 갈리면
`BACKBONE_DEFINITION_DEPENDENT` 이고 억지로 하나를 고르지 않습니다. ether O 몫이
가장 크면 `ETHER_O_CENTERED` 라고 부르지 "backbone 폴라론" 이라고 하지 않습니다.

**Q4 4층 판정 — 구현.**

| 층 | 무엇 | 문턱 | 미달 |
|---|---|---|---|
| 1 초기 개입 | 회전 직후 **SCF 전** 밀도의 목표집합 \|스핀\| 몫. 계의 **실제** charge/mult 로 `NoIter` probe 를 따로 돕니다 | ≥ 0.50 | `SEED_INTERVENTION_FAILED` / probe 없으면 `..._UNVERIFIED` |
| 2 최종 분해 | 링 몫의 최대−차순위 | ≥ 0.10 | `TARGET_UNRESOLVED` |
| 3 최종 안정성 | 불안정하면 따라 내려간 `.gbw` 로 재계산하고 **다시** 판정 | — | `UNSTABLE_NOT_REJUDGED` |
| 4 basin 군집 | 전자수·에너지·⟨S²⟩·원자별 **부호 있는** 스핀 벡터·링 몫 벡터 | dE 1e-4 Eh · spin L1 0.30 · ring L1 0.10 · dS² 0.02 | 임계 근처는 `borderline` |

설계 판단 셋을 밝혀 둡니다:

- **2층에서 명중(hit)을 요구하지 않습니다.** 요구하면 "심은 데로 갔다" 만 남기는
  순환논증이 됩니다. 요구하는 것은 **분해 가능**이고, 옮겨간 것은 `MOVED_FROM_SEED`
  로 기록합니다.
- **backbone 몫이 0.50 미만이면 2층을 면제합니다.** SO₃ 중심 해에 링 분해를
  요구하면 정상 결과를 오답 처리합니다.
- **4층은 전역 스핀 뒤집힘을 같은 상태로 자동 흡수하지 않습니다.** 분자 doublet 이라
  슬랩 AFM 처럼 자명하지 않습니다 — 필요하면 선언해서 따로 처리할 일이라고 봤습니다.

그리고 **`n_states` 를 잡 개수가 아니라 구분되는 basin 수**로 바꿨습니다.
⛔ seed 개수는 반복수가 아닙니다.

3층 게이트가 막다른 길이 되지 않도록 `--polaron_restart` 를 만들었습니다 —
불안정 잡의 `.gbw` 로 재판정 입력을 생성하고 `restart_of` 로 연결합니다.
`.gbw` 가 없으면 만들지 않습니다 (그냥 다시 돌리면 같은 해로 갑니다).

**probe 의 관측량 면제**: `NoIter` probe 에는 UNO/UCO 를 넣지 않았습니다. 수렴하지
않은 밀도에는 정의되지 않기 때문입니다. 그 대신 probe 결과는 **에너지·class 판정에
쓰지 않고** 개입 확인에만 씁니다 — job 레코드에 면제 사유를 적었습니다.

## 4. 규모

| | |
|---|---|
| 환경 | ε=1 하나 |
| phase L / L2 | 2 / 2 |
| 측정 SP | 16 (D• 8 + P⁺ 7 + D⁻ 기준 1) |
| 1층 probe | 13 (`NoIter` — `default` 는 개입이 없어 없습니다) |
| **총 ORCA 실행** | **32** |
| Opt | **없음** (S0 은 고정기하 SP 만) |

실행 순서: `L → L2 → seeds → probe → S → analyze → (restart)`.
probe 를 phase S **앞**에 둡니다 — 개입이 실패한 seed 로 200원자 r2SCAN-3c 를
돌리지 않기 위해서입니다.

## 5. ⚠ 아직 못 한 것 — 숨기지 않겠습니다

- **실물 ORCA 검증이 없습니다.** `%loc` 출력 형식, `Rotate {j,nbeta,90,1,1}` 의 실제
  동작, `NoIter` probe 가 스핀 인구를 찍는지 — 전부 미검증입니다. selftest 픽스처는
  *우리 판독기가 받는 형식*의 재현이지 ORCA 출력이 아닙니다. **phase L 첫 실행이
  곧 smoke test** 입니다.
- ε_dry_polymer 값 미정 (litdb 근거 필요) · torsion-diverse 거리 척도 미정.
- 중성 conformer 8개 중 gs0/gs1 만 완주했습니다. **gs2 가 진행 중인데 gs0 보다
  137 meV 낮습니다**(미수렴). S0 은 방법 시험이라 conformer 하나로 성립한다고 보고
  gs0 을 그대로 씁니다 — 지금 gs2 로 갈아타면 사후선택입니다. 8개 완주 뒤
  확장 규칙(저에너지 + torsion-diverse 2개)이 이것을 흡수합니다.

## 6. 여쭙는 것

**Q1.** §1 의 세 회귀 같은 것 — **실행하지 않으면 드러나지 않는** 결함이 첨부한
입력·manifest 에 또 있습니까? 커밋을 checkout 해서 직접 돌려 보셔도 됩니다
(회신 R2 에서 하신 그 방식이 이번에도 유효합니다).

**Q2.** 4층의 **설계 판단 셋**(명중 미요구 · backbone < 0.50 면 2층 면제 ·
전역 스핀 뒤집힘 미흡수)이 맞습니까?

**Q3.** 1층 문턱 0.50 이 적절합니까? `NoIter` 초기 밀도의 목표집합 몫이 실제 ORCA
에서 어느 정도 나올지 우리는 모릅니다 — 너무 높으면 정상 seed 를 막고, 너무 낮으면
아무것도 안 거릅니다.

**Q4.** 4층 군집 문턱(dE 1e-4 Eh ≈ 2.7 meV · spin L1 0.30 · ring L1 0.10 ·
dS² 0.02)이 이 계에서 적절합니까? 특히 **spin L1 0.30** 은 199원자 벡터에 대한
값이라 감이 없습니다.

**Q5.** probe 에서 UNO/UCO 를 면제한 것이 맞습니까? 아니면 `NoIter` 에서도
의미 있는 값이 나옵니까?

**Q6.** ε=1 하나로 시작해도 됩니까 — 아니면 dry-polymer ε 을 확정하는 것이
S0 의 선행조건입니까?

**Q7.** 이 상태로 phase L 을 **돌려도 됩니까**? 돌리면 그것이 곧 `%loc` 형식·
`Rotate` 동작의 첫 실물 검증이 됩니다.

## 7. 확인 방법

```bash
python3 tools/sdcp/build_v7c_trimer.py --selftest        # 152건 (음성 포함)
python3 tools/sdcp/build_v7c_trimer.py --polaron_pilot \
  --neutral_xyz db/structures/sdcp_orca_gs0/dp6_gs0_neutral_final.xyz \
  --out <빈 디렉터리> --eps 1.0 --nprocs 4 --maxcore 3000 --eps_why "..."
```

파일은 수정하지 않으셔도 됩니다 — 판정만 주십시오.
