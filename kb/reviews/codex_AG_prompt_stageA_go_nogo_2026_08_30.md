---
title: "회신 AG — Stage A 최종 GO/NO-GO: 회신 AF P0 넷을 닫았다"
date: 2026-08-30
kind: review_request
status: sent
---

# 회신 AG — GO/NO-GO 요청

회신 AF 의 P0 다섯 중 **넷을 코드로 닫았고**, 하나(POTCAR allowlist·provenance)는
열려 있다. 판정을 **GO / NO-GO 로 명시**해 달라. GO 면 그 자리에서 번들을 재생성해
외주에 보낸다.

리포: `claude/friendly-meitner-lldvar` · 도구 `tools/sdcp/vasp_handoff_bundle.py`
(selftest **380**, `convention_check` 0 위반)

---

## 0. AF 지적 대비 처리표

| AF | 지적 | 처리 |
|---|---|---|
| P0-1 | 진공 15 Å 주장이 거짓 (실측 8.63 Å) | **닫음** — §1 |
| P0-2 | "제출 가능" 이 AE 실측과 충돌 | **닫음(문서)** — v10 에서 삭제, 미완 6건을 그대로 등재 |
| P0-3 | 분석기가 번들 하나만 받아 12자세 C5 불가 | **닫음** — §2 |
| P0-4 | H1 이 사전등록을 바꿨다 (미해결 구간 승격) | **닫음** — §3 |
| P0-5 | 자기 분기 서술이 실물과 다름 | **닫음(문서)** — calibration 만 두 시드, NUPDOWN 문구 교체 |
| P1 전부 | Methods/Table 보완 9항 | **닫음(문서)** — §5 |
| AE 잔여 | POTCAR allowlist · provenance 우회 | ⛔ **열려 있다** — §6 |

---

## 1. P0-1 진공 — 재현했고 게이트로 만들었다

**재현**: 24 pm1 자세 중 **9개**가 15 Å 미만. PTFE `b74`/`b75`(calibration) ·
`b71`/`b79`(holdout) 이 8.56–8.79 Å, 최소 **8.63 Å** (F···O, xy 최소영상 포함).
지적한 수치와 자릿수까지 일치한다.

**원인**: 생성기에 진공을 재는 코드가 한 줄도 없었다. 입력 preflight 는
`mol_graph_canonical`·`registry_role` 만 본다.

**레퍼런스 앵커**: `litdb/papers/han2025_icep_binder_ultrahigh_loading_ncm811.md`
Fig. S12 — *"The bottom two layers are constrained. The vacuum spacing is over 15 Å."*
같은 계(바인더/NCM811 표면 DFT)의 관례다.

**교정**:
- `image_separation_A()` — 흡착종↔다음 주기 슬랩(+c) 실제 최단거리
- `poscar_set_c()` — c 만 늘리고 **Cartesian 좌표 보존** (Direct 면 z 분율 되scale).
  c 축이 z 와 안 나란하면 **거부**한다
- `fit_bundle_vacuum()` — 번들 전체를 **한 c** 로 (기준 슬랩 포함, 안 그러면 소거 안 됨).
  ⚠ Δ 를 늘려도 최단거리는 Δ 만큼 안 는다(최단 쌍의 xy 성분) — 한 번만 늘리면
  15.0 목표에 14.978 로 미달한다. **수렴할 때까지 반복**한다
- `--min_vacuum` (기본 15.0) · 확장 뒤에도 미달이면 **번들을 안 내보내고 죽는다**

**실물 적용**: c 30.2609 → **36.6551 Å**, 최소 8.629 → **15.001 Å**, 미달 11자세(net4 포함).

**부수 발견**: 셀 부피 +21.1 % 인데 **비용 모형이 그걸 못 봤다** — `phase_hours` 가
원자수·k 만 봤다. 부피비 인자를 넣었다(1차 선형). ⇒ 외주 견적이 21 % 올라간다.

**묻는 것**: ① 15 Å 이 이 계에 충분한가, 아니면 셀 높이 수렴 시험(같은 자세 두 c)을
번들에 넣어야 하나? ② 넣는다면 몇 잡을 어느 자세로?

---

## 2. P0-3 두 묶음 결합 — 구현했다

**인정**: 지적이 정확했다. 12자세는 calibration 4 + holdout 8 이고 기체 기준계는
calibration 묶음에만 있어 **어느 쪽도 단독으로 대비를 만들 수 없었다.** 문서가
설명하는 양이 코드에 없었다.

- `analyze_results.py <calib> --merge <holdout>` — 잡 수집을 루트별로 돌린다.
  이름 충돌은 조용히 덮지 않고 `MERGE_NAME_COLLISION` 으로 그 잡을 버린다
- `merge_compat()` — 두 MANIFEST 의 **sha256 을 결과에 박고**, `clean_slab` sha ·
  `potcar_spec` · `kmesh_effective` · `gate_version` · `freeze_frac_dft` · `nslab`
  중 하나라도 갈리면 blocking
- C5 가 `merge_info` 를 **요구**한다. 없으면 `NOT_MERGED`, 비호환이면
  `MERGE_INCOMPATIBLE` — 둘 다 값을 만들지 않는다

⛔ 못 하는 것: VASP 바이너리·PAW 배포판 동일성은 MANIFEST 에 없어 여기서 못 본다.
회수된 OUTCAR 되울림으로 따로 봐야 한다. **이걸 결합 게이트에 넣어야 하나?**

---

## 3. P0-4 H1 — 세 갈래 + 정확히 4+8 + 조각 사이 basin

- **삼분법**: `>+30 meV` holds · `±30 meV` **unresolved** · `<−30 meV` fail.
  종전 `> −30 이면 통과` 는 판정 해상도 안의 미해결 구간을 통과로 승격시켰다
- **정확히 4 + 8**: 종전엔 합이 12 면 통과라 11+1 도 지나갔고 그러면 홀드아웃
  시험 자체가 사라진다
- **조각 사이 basin**: 종전엔 조각 안에서만 맞춰서 SDCP 최저와 PTFE 최저가 서로
  다른 자기 배열이어도 뺄셈이 나갔다

⚠ **양성 픽스처가 옛 규약을 encode 하고 있었다** — PTFE 여유 20 meV 가 새 삼분법에서
미해결이다. 픽스처를 고치고 그 20 meV 케이스를 **음성 시험으로 남겼다.**

---

## 4. ★ 새로 여는 것 — 판정바닥 δ 가 MLIP 유래였다

이건 AF 가 지적하지 않았는데 사용자가 물어서 확인한 것이다.

**사실**: 30 meV 는 `site_screen.py` `GATE["decision_floor_eV"]` 로 2026-08-11 에
정한 **UMA(MLIP) 실무 해상도**다. wave1 부터 **DFT 값**에 그대로 써 왔고,
`kb/questions/sdcp_site_preference.md` 가 2026-08-28 에 *"옮겨 쓸 근거가 문서에
없다"* 로 미해결 등재했으나 닫히지 않았다.

같은 카드의 실측: 자기 basin gap **49.718 meV** · 자세 폭 **14.6 meV** ·
시드 재현 0.087 meV · dense-k 0.003 meV. ⇒ 카드의 결론은
*"DFT 바닥이 30 meV 보다 **커질** 가능성이 있다 (= 지금 판정이 지나치게 관대할 수 있다)"*.

**⚠ 우리가 먼저 낸 제안은 철회했다**: `δ = max(시드 산포, k 오차, 10 meV)` 는
실측이 0.1 meV 급이라 바닥이 10 meV 로 **내려간다** — 카드 경고와 정반대 방향이다.

**등록한 교정** (`db/properties/…closure_conditions….json` §14, proposed):

> **δ_f = max(30 meV, S_f)** — 조각별. `S_f` = C1 이 재는 **(UMA − DFT) 오프셋의
> 조각내 폭**. 이 42잡이 직접 낸다.

**근거**: `S_f` 는 *"UMA 순위를 믿었을 때 DFT 순서가 얼마나 흔들리는가"* 를 **DFT 단위**로
잰 값이라, 홀드아웃 시험이 실제로 요구하는 해상도다. `max` 라서 **엄격해질 수만 있다.**
30 meV 는 철회하지 않고 하한으로 남기되 **MLIP 유래임을 병기**한다.

⛔ 못 하는 것: UMA **기하** 오차가 DFT 에너지차에 싣는 몫을 직접 재지 못한다 —
자세를 DFT 로 다시 이완해야 나오고 그건 Stage B 다. `S_f` 는 그 몫의 **대리값**이다.

**묻는 것**: ① `S_f` 가 그 대리값으로 타당한가? ② 아니라면 42잡이 낼 수 있는 것 중
무엇이 맞나? ③ 결과 전에 바꾸는 것이므로 사전등록상 문제없다고 보는가?

---

## 5. 문서 (P0-2 · P0-5 · P1)

`docs/manuscripts/figure2e_explained_v10.md` (+ docx). v9 가 내부 약어를 설명 없이
깔아 공저자가 못 읽는다는 지적을 받아 **1부(배경, 처음 보는 사람 기준) / 2부(원고 문장) /
3부(게이트·용어)** 로 갈랐다. `ΔΔE_obs` 등 자체 기호는 **원고 어휘에서 제거**했다 —
논문은 값 둘과 그 차이를 문장으로 적는다.

반영: energy(sigma→0) · 기체 conformer 출처 · box20/24 조각별 두 칸 ·
PREC/ADDGRID/ISYM/ALGO/ISTART/ICHARG/IDIPOL=4 · coverage 문구 · 변형 포함 ·
stoichiometric LNO proxy · 42잡/43실행 · 숫자 문장은 **절댓값 + 부호로 정한 이름**.
"제출 가능" 삭제, 미완 6건 등재.

---

## 6. ⛔ 아직 열린 것

| # | 무엇 | 상태 |
|---|---|---|
| 1 | POTCAR allowlist 누락 · provenance 우회 (AE) | 미해결 |
| 2 | 판정 규약 사람 승인 | `proposed` |
| 3 | 셀 높이 수렴 시험 넣을지 | **이 리뷰의 질문** |
| 4 | 외주 큐 walltime 상한 vs 최장 잡 | 확인 필요 — §7 |

---

## 7. 외주 규모 (재생성 전 추정)

| | 종전 | 부피 +21 % 반영 |
|---|---:|---:|
| 잡 수 | 42 (VASP 실행 43) | 동일 |
| 코어/잡 | 256 | 256 |
| 최장 단일 잡 | 44.8 h | **≈ 54 h** |
| makespan @ 동시 8 | 4.6 d | **≈ 5.6 d** |

⚠ 최장 잡이 **48 h 큐 상한을 넘을 수 있다.** 그 잡은 `refs/clean_slab__afm2424_pm1`
(static → dense 직렬)이다.

**묻는 것**: dense 를 별도 잡으로 분리해 각각 48 h 아래로 넣는 것이 맞나, 아니면
CHGCAR 승계를 유지해야 하나? 분리하면 승계 증거가 약해진다.

---

## 8. 판정 형식

**GO** — 재생성해 외주 발송해도 된다 (조건이 있으면 명시)
**NO-GO** — 남은 P0 를 번호로. 각각 *"무엇을 고치면 닫히나"* 를 한 줄로.

첨부가 필요하면 말해 달라 — 재생성한 zip 둘과 `MANIFEST.json` 을 보낸다.
