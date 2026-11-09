---
title: "DX 회신 — 셀구축 v1.2 · b2o3 B·O 배치 카드 개정 1 v1.2 확인: NO-GO · DW P1-1 · P1-2 · P2 · P1-3 · P3 닫힘 · 새 P1 1 (파일럿 결과를 8 단계 결과로 재사용 — 실행 목적 미구분) · P2 2 (실행기 내용 기준 중복 제거 · EOS 입력 유효성)"
date: 2026-11-09
updated: 2026-11-09
tags: [review, b2o3, cell-construction, uma, readout, pilot, eos, runner, codex, reply, letter]
letter: DX
track: b2o3
channel: codex
kind: reply
status: 회신 원문 (2026-11-09 · 사용자 붙여넣기) — NO-GO · 기준 커밋 93937466 (evac 브랜치) · 생산 계산 안 함 · 재현 수치는 합성 시험 값
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 프롬프트 `codex_DX_prompt_cell_construction_v1_2_release_2026_11_09.md` 에 대한 Codex 회신 **원문 그대로** (사용자가 2026-11-09 대피 세션에 붙여 넣음). 고치지 않는다.
> 링크의 `C:/Users/Administrator/Documents/Codex/...` 경로는 Codex 쪽 작업 사본이다 (이 저장소 경로가 아니다).
> 맨 아래 부록 셋은 회신 끝에 이어 붙어 온 JSON 셋 — `verification.json` · `edge_results.json` · `eos_cli_results.json` (원문 링크 이름) · 값 그대로 · 공백 · 줄바꿈만 접었다 (최상위 키 한 줄씩 · 파싱 확인 12 · 12 · 3 키 · `NaN` 은 원문 그대로).
> ⚠ 두 결정은 proposed 그대로다 — 회신 넷째 확인 목록대로 고친 판의 카드를 사용자가 새로 비준해야 한다 (리뷰 진행 승인 ≠ 카드 비준).

---

NO-GO — 1단계 전체 발사는 아직 보류입니다. DW의 기존 반례는 막혔지만, 새로 선언한 ‘파일럿 재사용 금지’가 판독기에 연결되지 않았습니다.

기준 커밋 93937466을 확인했습니다. 판독기 57/57, run_anneal 자가시험을 재현했고, 생성기 검증을 생략하지 않은 135개 생성 구조 manifest에 합성 결과를 연결해 CLI 전 경로를 실행했습니다. 생산 UMA·DFT·MD는 실행하지 않았으며, 저장소 소스도 수정하지 않았습니다.

새 지적은 P1 한 건, P2 두 건입니다. P0는 확인하지 못했습니다.

P1-1 · 파일럿 결과를 8단계 결과로 재사용해도 통과합니다.
[b2o3_bo_readout.py (line 656)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DX_20261109/source/tools/doping/b2o3_bo_readout.py:656)
- 재현: t_a=100인 정상 합성 사례에서, 8단계의 해당 항목을 기존 파일럿 실행 기록과 산출물로 교체했습니다. 파일 해시와 정체성 검사는 모두 통과하고, anneal은 rc=0으로 승자를 출력했습니다. 합성 사례의 승자–차저 간격도 0.300 → 0.500 eV로 바뀌었습니다.
- 원인: 파일럿과 8단계 모두 stage="anneal_relax"이며, 시작 파일·시간·온도도 같을 수 있습니다. 현재 검사에는 어느 단계의 실행인가를 구별하는 항목이 없습니다.
- 최소 수정: 실행기가 pilot과 stage8의 목적을 실행 정체성에 기록하고, 판독기가 요구하는 목적과 대조해야 합니다. 파일럿 기록을 그대로 넣으면 거부하고, 새 8단계 실행은 같은 입력·100 ps여도 통과하는 시험이 필요합니다. 산출물 해시가 다르다는 조건으로 대체하면 안 됩니다. 정상 재실행도 같은 바이트를 만들 수 있습니다.
재사용 자체를 허용하는 정책으로 바꾸는 선택도 가능하지만, 현재 카드의 금지 문구를 유지한 채 이 경로를 승인할 수는 없습니다.

P2-1 · 서로 다른 계획 항목의 시작 파일이 같으면 러너가 하나를 삭제합니다.
[run_uma_kgy.sh (line 282)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DX_20261109/source/db/inputs/ndo_site_2026_10_14/run_uma_kgy.sh:282)
- 재현: 서로 다른 바탕 번호의 두 성공 항목에 동일한 post_relax.xyz 바이트를 주고, 기록과 해시를 맞췄습니다. 거름 판정과 실행 manifest는 18항목을 만들었지만, 러너의 실제 manifest→입력 목록 변환 블록은 17개만 내보냈습니다. 중복 제거 전에는 항목 이름도 모두 맞았습니다.
- 영향: 이어지는 N_EXPECT=18 검사에서 중단됩니다. 따라서 잘못된 승자를 조용히 내는 문제는 아니지만, 유효한 계획을 실행할 수 없는 경우가 남습니다.
- 최소 수정: b2o3_bo_plan/v1에서는 파일 내용이 같더라도 서로 다른 계획 항목을 보존하세요. 기존 공통 host 중복 제거와 구분하면 됩니다. N_EXPECT를 17로 낮추는 것은 해결이 아닙니다.
P2-2 · EOS 입력이 불완전하거나 비유한 값이어도 ‘생략 가능’이 나옵니다 — DFT 진입 전 조건입니다.
[b2o3_bo_readout.py (line 689)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DX_20261109/source/tools/doping/b2o3_bo_readout.py:689)

실제 eos CLI에서 다음 세 경우 모두 **rc=0, skip_eos=true**를 재현했습니다.
- 세 가족 중 F_B 에너지만 NaN.
- 세 가족의 부피가 모두 음수.
- F_free가 빠져 두 가족만 입력됨.
최소 수정은 가족 집합이 정확히 셋인지, E·P·V가 모두 유한한지, V>0인지를 계산 전에 검사하는 것입니다. 입력 파일 결속과 함께 DFT 진입 전에 닫으면 됩니다.

Q1. DW P1-1·P1-2·P2는 닫혔나?
항목	판정
DW P1-1 기존 단계 결속 반례	닫힘. 남의 시작 파일, identity 부재, 20 ps·1000 K, 합집합 축소, 부분 거름, 결과 누락, 영수증 변경을 차단했습니다. 다만 위의 새 실행 목적 구분은 남았습니다.
DW P1-2 시간축	닫힘. 출처의 해시·프레임·간격 변조뿐 아니라 생산 기록의 간격 500→50도 실제 프레임 수와 불일치하여 거부했습니다.
DW P2 NaN 기하	닫힘. 해시를 맞춘 NaN 좌표는 실패로 기록됐으며 F_free로 분류되지 않았습니다. 합성 사례에서는 G1 규칙에 따라 성공 5/6으로 남았습니다.


정상 경로도 screen → extract → pilot → anneal까지 통과했습니다. 파일럿 에너지 0 / −0.30 / −0.02는 100 ps를 선택했습니다.

Q2. 단계 사슬에 남은 손잡이는?

확인된 것은 위의 실행 목적 구분과 러너의 내용 기준 중복 제거입니다.

_core의 판정 재계산 비교는 합집합과 t_a 변경을 잡았습니다. 전체 자료 트리를 다른 폴더로 옮기고 다른 작업 디렉터리에서 판독해도 정상 결과가 유지됐습니다. 상대경로 검증은 Windows 내 이동까지 확인했으며, 운영체제 사이 이동은 시험하지 않았습니다.

Q3. 결과 전 규칙과 의도적인 생략은 괜찮나?
- k_f 미달 → 보류: 찬성입니다. 부족한 가족만 탐색량을 줄여 비교하는 경로를 막습니다.
- 6단계 실패 항목 → 시작 없음·G1 분모 유지: 찬성입니다. 누락과 구별하고 실패 이유를 보존하는 현재 방식이 맞습니다.
- 8단계 seed 대조 생략: 실제 seed를 기록하고 결과를 보고 seed를 골라 바꾸지 않는 운영 조건에서 수용 가능합니다.
- 저장 간격 500 강제 생략: 찬성입니다. 실제 기록과 궤적이 일치하고 요청 시각을 정확히 선택할 수 있으면 충분합니다.
- 파일럿과 별도 실행: 정책으로 채택할 수 있지만, 현재 구현은 그 정책을 보증하지 못합니다. P1-1을 닫아야 합니다.
- EOS 파일 결속을 DFT 전으로 미룸: 수용 가능합니다. 위 입력 유효성 검사도 함께 닫으세요.
- 판독기 selftest에서 생성기 검증 대체: 단위시험에서는 가능합니다. 이번 독립 검증에서는 실제 생성기 검증을 살린 연결 경로도 통과했습니다. 주장한 변이 13종 전체는 별도로 재실행하지 않았습니다.
Q4. EOS 기준 순서와 관측창 문구는 닫혔나?

DW의 해당 지적은 둘 다 닫혔습니다.

EOS는 기존 숫자를 그대로 넣어 확인했습니다. 모든 조합이 기준 승자를 뒤집는 사례와 아래 순위만 바뀌는 사례 모두 skip_eos=false였습니다. 다만 위 P2-2 때문에 EOS 도구 전체의 사용 승인이 끝난 것은 아닙니다.

관측창 재계산값은 다음과 같습니다.
- 기대 사건 1: 0.7744567 eV
- 95% 검출 정확식: 0.6799083 eV
- /3 근사: 0.6797856 eV
- 기대 사건 1 장벽보다 0.10 eV 높을 때 검출 확률: 26.9002%
수정한 문구와 맞습니다.

1단계 시작 전 마지막 확인 목록
1. 파일럿·8단계 실행 목적을 구별하고, 파일럿 복사 거부 / 정상 새 실행 허용을 확인할 것.
2. 동일 시작 바이트를 가진 서로 다른 계획 항목도 계획 수·이름 그대로 러너에 전달되도록 수정할 것.
3. 수정본으로 정상 연결 경로와 위 두 반례를 재확인할 것. 생산 계산을 추가할 필요는 없습니다.
4. 그 버전의 카드에 대해 사용자가 새로 비준할 것. 이번 리뷰 진행 승인은 카드 비준을 대신하지 않습니다.
검증 기록: [검증 요약](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DX_20261109/verification.json) · [경계 사례 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DX_20261109/edge_results.json) · [EOS CLI 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DX_20261109/eos_cli_results.json)

---

## 부록 A — verification.json (사용자 붙여넣기 · 공백만 접음)

```json
{
"target_commit": "939374661dbc5218e03397a7a87e4ba99f37dc7b",
"source_unchanged": true,
"source_files": 10,
"baseline_cli_expected_results": {"positive_screen": true, "positive_extract": true, "positive_pilot": true, "positive_anneal": true, "foreign_input": true, "missing_identity": true, "partial_screen": true, "shortfall": true, "wrong_time": true, "wrong_temperature": true, "missing_anneal": true, "shrunken_union": true, "changed_receipt": true, "bad_traj_hash": true, "bad_frame": true, "bad_interval": true},
"independent_cli_cases": 18,
"synthetic_only": true,
"production_runs": 0,
"old_eos_counterexamples_rejected": {"eos_all_corners_flip_baseline": true, "eos_lower_ranks_change": true},
"observation_window": {"e1_eV": 0.7744567009613421, "e95_eV": 0.6799082941362969, "approx_e95_eV": 0.6797856187879325, "prob_at_e1_plus_0_1": 0.2690020151998205},
"new_findings": {"pilot_reuse_rc": 0, "runner_planned": 18, "runner_actual": 17, "runner_all_role_names_correct_before_dedup": true, "eos_invalid_accepted": ["eos_nan_energy", "eos_negative_volume", "eos_missing_family"]},
"limitations": ["No production UMA, DFT, or MD.", "Did not independently rerun the claimed 13 mutant variants.", "Executed the runner manifest-to-XYZ Python block; its N_EXPECT rejection at exit 7 is determined from the shell source.", "Whole-tree relocation checked on Windows, not cross-platform path serialization."],
"test_generated_source_side_files": ["tools/doping/__pycache__/_provenance.cpython-312.pyc"]
}
```

## 부록 B — edge_results.json (사용자 붙여넣기 · 공백만 접음)

```json
{
"relocated_chain": {"rc": 0, "output": "-> C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\relocated_chain\\answer_checked.json\n승자 F_B (차저 F_free 와 0.300 ≥ 0.2) \n"},
"duplicate_role_screen": {"rc": 0, "output": "-> C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\duplicate_verdict.json\n거름 완결 — 합집합 M = 6 · 8 단계 계획 18 (시작 없음 0) · 파일럿 cfg0000_E-2256.634_O-bo4\n   시작 파일 manifest {'pilot': 1, 'anneal': 18} -> C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\duplicate_plan\n"},
"duplicate_runner": {"rc": 0, "declared": 18, "actual": 17, "missing_names": ["cfg0001_E-2255.860_O-bo4"], "stdout": "C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0000_E-2256.634_O-bo4\\post_relax.xyz\nC:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0000_E-2256.634_O-distributed\\post_relax.xyz\nC:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0000_E-2256.634_O-free_s\\post_relax.xyz\nC:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0001_E-2255.860_O-distributed\\post_relax.xyz\nC:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0001_E-2255.860_O-free_s\\post_relax.xyz\nC:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0002_E-2255.792_O-bo4\\post_relax.xyz\nC:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0002_E-2255.792_O-distributed\\post_relax.xyz\nC:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0002_E-2255.792_O-free_s\\post_relax.xyz\nC:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0003_E-2255.483_O-bo4\\post_relax.xyz\nC:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0003_E-2255.483_O-distributed\\post_relax.xyz\nC:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0003_E-2255.483_O-free_s\\post_relax.xyz\nC:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0004_E-2255.404_O-bo4\\post_relax.xyz\nC:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0004_E-2255.404_O-distributed\\post_relax.xyz\nC:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0004_E-2255.404_O-free_s\\post_relax.xyz\nC:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0005_E-2255.140_O-bo4\\post_relax.xyz\nC:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0005_E-2255.140_O-distributed\\post_relax.xyz\nC:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\screen_results\\cfg0005_E-2255.140_O-free_s\\post_relax.xyz\n", "stderr": "   anneal: 해시 18 개 확인\n", "full_runner_exit_with_declared_N_EXPECT": 7},
"reused_pilot": {"rc": 0, "output": "-> C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\reused_answer.json\n승자 F_B (차저 F_free 와 0.500 ≥ 0.2) \n"},
"reuse_answer": {"decision": "승자 F_B (차저 F_free 와 0.500 ≥ 0.2)", "winner": "F_B", "families": {"F_B": {"M": 6, "n_success": 6, "need_G1": 5, "G1": true, "failed": [], "n_end_changed": 0, "G3_mixed": false, "G3": "0/6", "min": {"rank": 0, "name": "cfg0000_E-2256.634_O-bo4", "E": -0.7, "end_motif": "F_B"}}, "F_P": {"M": 6, "n_success": 6, "need_G1": 5, "G1": true, "failed": [], "n_end_changed": 0, "G3_mixed": false, "G3": "0/6", "min": {"rank": 0, "name": "cfg0000_E-2256.634_O-distributed", "E": 0.0, "end_motif": "F_P"}}, "F_free": {"M": 6, "n_success": 6, "need_G1": 5, "G1": true, "failed": [], "n_end_changed": 0, "G3_mixed": false, "G3": "0/6", "min": {"rank": 0, "name": "cfg0000_E-2256.634_O-free_s", "E": -0.2, "end_motif": "F_free"}}}},
"bad_producer_cadence": {"rc": 1, "output": "⛔ 파일럿 런 결속 실패 (cfg0000_E-2256.634_O-bo4: md_traj 프레임 수 101 ≠ 걸음 50000 // 간격 50 + 1) — 스냅숏을 믿지 않는다\n"},
"nan_coordinates": {"rc": 0, "output": "-> C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\chain\\nan_answer.json\n승자 F_B (차저 F_free 와 0.290 ≥ 0.2) \n"},
"nan_answer": {"kind": "b2o3_bo_anneal_readout/v1", "inputs": {"screen_verdict": {"path": "verdict.json", "sha256": "14b8e2101d8e91a08e333d31ee5655800af12aeb3727a6cfc8ca8bf48d521b66"}, "pilot_receipt": {"path": "receipt.json", "sha256": "426d858e1a1379c8c2646b9e0943b164893fa4c76412b18d1acb288afcf53a92"}, "anneal_results": {"path": "anneal\\nan_geometry.json", "sha256": "c49aa36f7dc79feab5fc1e4a9022a7722f01c47d4fb62e60da0c376962a18283"}}, "t_a_ps": 100, "M": 6, "plan_n": 18, "plan_no_start": [], "contract": {"families": {"bo4": "F_B", "distributed": "F_P", "free_s": "F_free"}, "unit_B2O3": 1, "k_f": 6, "k_f_shortfall": "hold", "r_bond_A": 1.8, "r_grey_A": 2.3, "g1_frac": "ceil(5M/6)", "g3_rule": "changed / n_success > 1/3", "margin_uma_eV": 0.2, "pair_min": 3, "pair_frac": 0.8333333333333334, "pilot_times_ps": [20, 50, 100], "pilot_spread_eV": 0.05, "margin_dft_eV": 0.1, "B_range_GPa": [21.7, 32.5], "eos_P_max_GPa": 2.0, "model": "uma-s-1p1/omat", "relax_fmax": 0.05, "cell_relax": true, "relax_steps": 1500, "dt_fs": 2.0, "friction": 0.01, "anneal_T_K": 500.0}, "families": {"F_B": {"M": 6, "n_success": 5, "need_G1": 5, "G1": true, "failed": [{"name": "cfg0000_E-2256.634_O-bo4", "why": ["cfg0000_E-2256.634_O-bo4: post_relax 좌표에 NaN · inf"]}], "n_end_changed": 0, "G3_mixed": false, "G3": "0/5", "min": {"rank": 1, "name": "cfg0001_E-2255.860_O-bo4", "E": -0.49, "end_motif": "F_B"}}, "F_P": {"M": 6, "n_success": 6, "need_G1": 5, "G1": true, "failed": [], "n_end_changed": 0, "G3_mixed": false, "G3": "0/6", "min": {"rank": 0, "name": "cfg0000_E-2256.634_O-distributed", "E": 0.0, "end_motif": "F_P"}}, "F_free": {"M": 6, "n_success": 6, "need_G1": 5, "G1": true, "failed": [], "n_end_changed": 0, "G3_mixed": false, "G3": "0/6", "min": {"rank": 0, "name": "cfg0000_E-2256.634_O-free_s", "E": -0.2, "end_motif": "F_free"}}}, "G2_same_composition": true, "common_success_pairs": [1, 2, 3, 4, 5], "n_pairs": 5, "order": ["F_B", "F_free", "F_P"], "winner_runner_up_gap_eV": 0.29, "winner": "F_B", "decision": "승자 F_B (차저 F_free 와 0.290 ≥ 0.2)", "pairs": {"n": 5, "same_sign_as_order": 5, "같은_방향": true}, "G3_mixed_families": []},
"eos_valid": {"baseline_order": ["F_B", "F_P", "F_free"], "baseline_gap": 1.0, "baseline_decision": {"lowest": "F_B", "gap_ge_margin": true, "margin": 0.1}, "robust_independent_B": true, "robust_common_B": true, "pressure_ok": true, "skip_eos": true, "corners": [{"B": {"F_B": 21.7, "F_P": 21.7, "F_free": 21.7}, "order": ["F_B", "F_P", "F_free"], "gap": 1.0, "same_as_baseline": true}, {"B": {"F_B": 21.7, "F_P": 21.7, "F_free": 32.5}, "order": ["F_B", "F_P", "F_free"], "gap": 1.0, "same_as_baseline": true}, {"B": {"F_B": 21.7, "F_P": 32.5, "F_free": 21.7}, "order": ["F_B", "F_P", "F_free"], "gap": 1.0004779035661409, "same_as_baseline": true}, {"B": {"F_B": 21.7, "F_P": 32.5, "F_free": 32.5}, "order": ["F_B", "F_P", "F_free"], "gap": 1.0004779035661409, "same_as_baseline": true}, {"B": {"F_B": 32.5, "F_P": 21.7, "F_free": 21.7}, "order": ["F_B", "F_P", "F_free"], "gap": 0.999522096433859, "same_as_baseline": true}, {"B": {"F_B": 32.5, "F_P": 21.7, "F_free": 32.5}, "order": ["F_B", "F_P", "F_free"], "gap": 0.999522096433859, "same_as_baseline": true}, {"B": {"F_B": 32.5, "F_P": 32.5, "F_free": 21.7}, "order": ["F_B", "F_P", "F_free"], "gap": 1.0, "same_as_baseline": true}, {"B": {"F_B": 32.5, "F_P": 32.5, "F_free": 32.5}, "order": ["F_B", "F_P", "F_free"], "gap": 1.0, "same_as_baseline": true}]},
"eos_nan_energy": {"baseline_order": ["F_B", "F_P", "F_free"], "baseline_gap": NaN, "baseline_decision": {"lowest": "F_B", "gap_ge_margin": false, "margin": 0.1}, "robust_independent_B": true, "robust_common_B": true, "pressure_ok": true, "skip_eos": true, "corners": [{"B": {"F_B": 21.7, "F_P": 21.7, "F_free": 21.7}, "order": ["F_B", "F_P", "F_free"], "gap": NaN, "same_as_baseline": true}, {"B": {"F_B": 21.7, "F_P": 21.7, "F_free": 32.5}, "order": ["F_B", "F_P", "F_free"], "gap": NaN, "same_as_baseline": true}, {"B": {"F_B": 21.7, "F_P": 32.5, "F_free": 21.7}, "order": ["F_B", "F_P", "F_free"], "gap": NaN, "same_as_baseline": true}, {"B": {"F_B": 21.7, "F_P": 32.5, "F_free": 32.5}, "order": ["F_B", "F_P", "F_free"], "gap": NaN, "same_as_baseline": true}, {"B": {"F_B": 32.5, "F_P": 21.7, "F_free": 21.7}, "order": ["F_B", "F_P", "F_free"], "gap": NaN, "same_as_baseline": true}, {"B": {"F_B": 32.5, "F_P": 21.7, "F_free": 32.5}, "order": ["F_B", "F_P", "F_free"], "gap": NaN, "same_as_baseline": true}, {"B": {"F_B": 32.5, "F_P": 32.5, "F_free": 21.7}, "order": ["F_B", "F_P", "F_free"], "gap": NaN, "same_as_baseline": true}, {"B": {"F_B": 32.5, "F_P": 32.5, "F_free": 32.5}, "order": ["F_B", "F_P", "F_free"], "gap": NaN, "same_as_baseline": true}]},
"eos_negative_volume": {"baseline_order": ["F_B", "F_P", "F_free"], "baseline_gap": 1.0, "baseline_decision": {"lowest": "F_B", "gap_ge_margin": true, "margin": 0.1}, "robust_independent_B": true, "robust_common_B": true, "pressure_ok": true, "skip_eos": true, "corners": [{"B": {"F_B": 21.7, "F_P": 21.7, "F_free": 21.7}, "order": ["F_B", "F_P", "F_free"], "gap": 1.0, "same_as_baseline": true}, {"B": {"F_B": 21.7, "F_P": 21.7, "F_free": 32.5}, "order": ["F_B", "F_P", "F_free"], "gap": 1.0, "same_as_baseline": true}, {"B": {"F_B": 21.7, "F_P": 32.5, "F_free": 21.7}, "order": ["F_B", "F_P", "F_free"], "gap": 0.9995220964338591, "same_as_baseline": true}, {"B": {"F_B": 21.7, "F_P": 32.5, "F_free": 32.5}, "order": ["F_B", "F_P", "F_free"], "gap": 0.9995220964338591, "same_as_baseline": true}, {"B": {"F_B": 32.5, "F_P": 21.7, "F_free": 21.7}, "order": ["F_B", "F_P", "F_free"], "gap": 1.0004779035661409, "same_as_baseline": true}, {"B": {"F_B": 32.5, "F_P": 21.7, "F_free": 32.5}, "order": ["F_B", "F_P", "F_free"], "gap": 1.0004779035661409, "same_as_baseline": true}, {"B": {"F_B": 32.5, "F_P": 32.5, "F_free": 21.7}, "order": ["F_B", "F_P", "F_free"], "gap": 1.0, "same_as_baseline": true}, {"B": {"F_B": 32.5, "F_P": 32.5, "F_free": 32.5}, "order": ["F_B", "F_P", "F_free"], "gap": 1.0, "same_as_baseline": true}]},
"eos_missing_family": {"baseline_order": ["F_B", "F_P"], "baseline_gap": 1.0, "baseline_decision": {"lowest": "F_B", "gap_ge_margin": true, "margin": 0.1}, "robust_independent_B": true, "robust_common_B": true, "pressure_ok": true, "skip_eos": true, "corners": [{"B": {"F_B": 21.7, "F_P": 21.7}, "order": ["F_B", "F_P"], "gap": 1.0, "same_as_baseline": true}, {"B": {"F_B": 21.7, "F_P": 32.5}, "order": ["F_B", "F_P"], "gap": 1.0004779035661409, "same_as_baseline": true}, {"B": {"F_B": 32.5, "F_P": 21.7}, "order": ["F_B", "F_P"], "gap": 0.999522096433859, "same_as_baseline": true}, {"B": {"F_B": 32.5, "F_P": 32.5}, "order": ["F_B", "F_P"], "gap": 1.0, "same_as_baseline": true}]}
}
```

## 부록 C — eos_cli_results.json (사용자 붙여넣기 · 공백만 접음)

```json
{
"nan_energy": {"rc": 0, "output": "-> C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\scratch\\eos_nan_energy_out.json\nEOS 생략 가능\n", "skip_eos": true},
"negative_volume": {"rc": 0, "output": "-> C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\scratch\\eos_negative_volume_out.json\nEOS 생략 가능\n", "skip_eos": true},
"missing_family": {"rc": 0, "output": "-> C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DX_20261109\\scratch\\eos_missing_family_out.json\nEOS 생략 가능\n", "skip_eos": true}
}
```
