---
title: "DO 회신 — li2s-2 DN 고침 + DO 전 리뷰 고침 확인 (802290db): NO-GO · P0 1 (복구 때 본 녹음 fail 을 장부에 안 적어 뒤 손상으로 재시도 · stage1_pass) · P1 2 (판정 · 이력 · 장부의 같은 열쇠 둘 → 마지막 값 · 러너가 무효 장부를 정상 꼴로 덮어씀) · P2 2 (중첩 타입 오류로 요약이 죽어 이전 통과 파일이 남음 · 자식이 막힌 신호 마스크를 물려받음)"
tags: [review, li2s, glass, md, uma, density, quench, runner, codex, reply, letter]
letter: DO
date: 2026-11-04
track: li2s
channel: codex
kind: reply
status: 수령 2026-11-04 (사용자 붙여넣기 · 원문 보존 · 마크다운 링크와 JSON 의 Codex 로컬 경로 머리만 `<codex>` 로 줄임 · 탭으로 붙은 표는 표 꼴로 · JSON 은 코드 블록 · 붙여넣기 끝의 '오후 7:44' 는 사용자 화면 시각) → 반영 중
confidence: medium
verificationStatus: verified
verifiedAt: 2026-11-04
verifiedBy: self
explored: false
authoredBy: external
claimType: mixed
evidenceScope: multi-source-primary
---

> 프롬프트: `codex_DO_prompt_li2s2_dn_fixes_2026_11_04.md` (기준 커밋 `802290db`) · 트랙 li2s-2 (논문 1저자 = 외부 · 위임 10-30). 아래는 원문이다.
> `<codex>` = `C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DO_20261104` (JSON 안에서는 `C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_DO_20261104`).

---

NO-GO — P0 1건·P1 2건이 남았습니다. DN의 기존 타입 오류는 닫혔지만, 규칙 M과 기록 판독에 다른 우회가 재현됐습니다.

대상은 802290db입니다. Windows에서 드라이버 220/220·러너 97/97 통과를 재현했고, 드라이버·카드 값 지문도 일치했습니다. 추가 검증은 합성 자료와 실제 판독·판정·러너 함수로 수행했습니다. 생산 UMA/DFT 계산과 저장소 수정은 하지 않았습니다. Linux 전용 시험 3건과 변이 222건 전체는 이번에 재실행하지 않았습니다.

1. P0 — 복구 중 확인한 녹음 fail을 저장하지 않아, 이후 손상으로 재시도할 수 있습니다.

위치: [melt_quench_uma.py (line 1754)](<codex>/source/tools/ionic/melt_quench_uma.py:1754), [li2s2_stage1_runner.py (line 496)](<codex>/source/tools/ionic/li2s2_stage1_runner.py:496), [재시도 거부:764 (line 764)](<codex>/source/tools/ionic/li2s2_stage1_runner.py:764).

다음 순서가 첫 시드 A11과 후속 시드 A12 모두에서 재현됐습니다.
1. 녹음 창은 완성됐고 fail이지만, 전체 일정 도중 중단된 폴더를 만듭니다.
2. 실제 러너로 복구하면 fail을 계산하고 재시도를 거부합니다. 그러나 장부에는 melt_check·`verdict`·`closes_system`이 남지 않습니다.
3. 궤적 첫 프레임의 원소 기호 하나를 손상시키면, 같은 실행이 invalid로 바뀝니다.
4. 기존 invalid 원인 수정 선언 절차를 거치면 같은 시드가 재발사되고, 최종 소비자는 **`stage1_pass`**를 냅니다.
기존 장부나 판정 이력을 삭제하지 않았습니다. 프로그램이 이미 확인하고 재시도 거부에 사용한 fail을 보존하지 않는 문제입니다. 관측하기 전에 증거가 사라지는 허용 한계와 다릅니다.

최소 수정: 복구 판정에서 얻은 fail 근거를 반환받아, 러너가 거부하기 전에 잠금 아래 장부에 영구 기록하세요. 첫 시드는 닫힘도 기록해야 합니다. 실시간 감시 경로에 넣은 보존을 복구·재시도 검사 경로에도 연결하면 됩니다.
2. P1 — 완료 기록의 중복 JSON 키가 완료 증거를 지워 재담금질을 허용합니다.

위치: [현재 판정 판독:1466 (line 1466)](<codex>/source/tools/ionic/melt_quench_uma.py:1466), [이력 판독:1480 (line 1480)](<codex>/source/tools/ionic/melt_quench_uma.py:1480), [재판정 시 이전 기록 판독:1094 (line 1094)](<codex>/source/tools/ionic/melt_quench_uma.py:1094).

진짜 판정 함수가 incomplete · n=130 · expected=130을 기록한 뒤, DN과 같은 궤적 꼬리 소실 상태에서 완료 필드를 다음처럼 만들었습니다.
"n": 130, "n": 71
이 경로들은 일반 json.loads로 마지막 값만 취합니다. 결과는 다음과 같습니다.
- 단일 n:130 대조: rc24·발사 0, 완료 증거 때문에 보류.
- 중복 키: md_incomplete → interrupted, B13 재발사 허용, 최종 rc0·`stage1_pass`.
- 보존 이력의 schedule_complete:true,false도 같은 우회가 됩니다.
더구나 재판정을 하면 중복 키가 사라진 정상 모양의 JSON을 이력으로 저장합니다. 이후에는 원래의 모호함도 사라집니다.

최소 수정: 현재 판정·보존 이력·재판정의 이전 기록 판독에 loads_strict를 일관되게 적용하세요. 읽을 수 없는 원문을 마지막 값으로 정규화해서 보존하면 안 됩니다. 원문 보존과 보류가 함께 유지돼야 합니다.
3. P1 — 러너가 무효 비용 장부를 덮어써 정상 장부로 바꿉니다.

위치: [장부 읽기:736 (line 736)](<codex>/source/tools/ionic/li2s2_stage1_runner.py:736), [종료 시 저장:1004 (line 1004)](<codex>/source/tools/ionic/li2s2_stage1_runner.py:1004), [비용 증언 판독:572 (line 572)](<codex>/source/tools/ionic/li2s2_stage1_runner.py:572).

두 경로를 재현했습니다.
- 정상 장부에 "wall_h":999.0,"wall_h":5.0을 넣으면 소비자는 처음에 invalid입니다. 러너는 rc27·발사 0으로 멈추면서도, 종료 저장에서 5.0만 남깁니다. 직후 소비자는 **`stage1_pass / 50 h`**로 바뀌고, STOP 확인 후 러너도 rc0입니다.
- 고아 런 하한을 "wall_h_lower":99.0,"wall_h_lower":5.0으로 만들면, 6 h 비용 증언이 승인되고 중복 흔적이 사라집니다. 소비자는 stage1_pass / 51 h가 됩니다.
소비자의 엄격한 검사는 작동하지만, 다른 기록자가 그 검사에 걸린 원본을 조용히 바꾸고 있습니다.

최소 수정: 읽기 전용 비용 조회를 포함해 장부 판독을 엄격한 함수로 통일하세요. 판독 실패 시에는 종료 처리에서도 원본 장부를 다시 쓰지 않아야 합니다. 시험은 최초 거부뿐 아니라 원본 바이트 유지·두 번째 실행에서도 거부까지 확인해야 합니다.
추가 P2 두 건입니다.
- 중첩 타입 오류로 요약이 중단되고 이전 통과 파일이 남습니다.
  [melt_quench_uma.py (line 2006)](<codex>/source/tools/ionic/melt_quench_uma.py:2006) 이후에서 현재 판정의 provenance=[1], software=[1], run_id={} 등을 주면 예외로 끝나고 기존 stage1_summary.json의 stage1_pass가 남습니다. 새 러너 승인 우회까지 입증한 것은 아닙니다. 중첩 필드도 검사해 invalid 요약으로 갱신해야 합니다.
- 자식 프로세스가 종료 신호 차단 상태를 물려받습니다 — 코드상 추론, Linux 실측 전입니다.
  [li2s2_stage1_runner.py (line 882)](<codex>/source/tools/ionic/li2s2_stage1_runner.py:882)에서 TERM/HUP/INT를 막은 채 자식을 띄우고, 이후 부모에서만 복원합니다. Linux에서는 신호 마스크가 자식과 exec에 승계되므로, 자식이 별도로 해제하지 않으면 TERM 종료가 60초 대기 후 KILL로 넘어갈 수 있습니다. Popen의 restore_signals는 이 마스크 복원을 뜻하지 않습니다. 자식 시작 경로에서 원래 마스크를 복원하고, 실제 러너 발사 경로를 통한 Linux 시험이 필요합니다. 현재 KILL·비용 기록까지 무력화됐다는 증거는 없어 P0/P1로 올리지 않았습니다. Linux 신호 규칙, Python subprocess 문서.
질문 1–6의 판정은 다음과 같습니다.
1. 실행 종류 규칙: 기본 방향에 찬성합니다. 일반적인 interrupted 폴더의 invalid 재판정으로 재시도 한도를 우회하지 못하는 대조는 통과했습니다. 다만 녹음 재계산의 invalid 경로에는 위 P0가 남습니다.
2. 규칙 M: 정책에 찬성, 구현은 미해제입니다. 복구 때 관측한 fail도 지속적으로 보존해야 합니다.
3. 첫 시드 닫힘 유지: 찬성합니다. 실시간 감시가 저장한 fail은 정리 실패·판정 중 중단·나중 invalid 판정에도 닫힘이 유지됐습니다. 기록 오류를 함께 표시하는 것은 맞습니다.
4. MID_RUN_FILES: 현재 실제 생성 경로와 일치합니다. 보통의 MD 전·중 산출물 누락이나 MD 후 산출물의 잘못된 허용은 찾지 못했습니다.
5. 선언한 운영 한계 셋: 그 자체를 P0/P1로 보지 않습니다. 발사 실패가 재시도 기회를 소모하는 것, STOP 재확인이 필요한 것, GPU 조회 실패로 중단하는 것은 보수적 운영 비용입니다. 다만 이때도 이미 관측한 과학적 결과는 보존돼야 합니다.
6. 새로 확인한 조용한 오류: 위 P0·P1 세 갈래입니다.

| 항목 | 닫힘 판정 |
|---|---|
| DN P1 — 완료 필드 타입 오류 | 닫힘. 단일 n:"130"과 잘못된 컨테이너 타입을 러너·소비자 모두 차단. 중복 키는 별도 미해제 |
| DN P2 — NUL 꼬리 문구 | 닫힘. 복원 불가능한 꼬리의 한계와 구현이 일치 |
| DO 전 — 실시간 첫 시드 fail 보존 | 닫힘. 정리 실패·판정 중단 대조 통과 |
| DO 전 — 규칙 M | 미해제. 복구에서 관측한 fail의 영구 기록 누락 |
| DO 전 — 보존 폴더 식별·중단 분류 | 해당 수정은 닫힘. 판정 기록의 중복 키 처리는 별도 미해제 |
| DO 전 — MD 뒤 산출물 검사 | 닫힘. 현재 생성 경로와 대조 완료 |
| DJ Q2 — 완료 런 구분 | 부분 해제. 정상 완료 증거는 막지만 중복 키 우회가 남음 |
| DJ Q5 — 조용한 오류 | 미해제. 위 P0·P1 세 건 |

재승인 조건은 세 가지입니다: 복구에서 관측한 fail 영구 기록, 판정 기록의 엄격한 판독과 원문 보존, 무효 비용 장부의 덮어쓰기 금지. 각각 이번 재현 순서와 정상 중단 대조를 함께 통과해야 합니다.

[검증 기록](<codex>/VERIFICATION.json) · [규칙 M 재현](<codex>/do_melt_policy/results.json) · [완료 기록 재현](<codex>/do_consumer_records/results.json) · [비용 장부 재현](<codex>/do_runner_recovery/results.json)

```json
{
  "review": "DO",
  "commit": "802290db26aea7cf4ba53786c09880ad6f8ad788",
  "base": "acc648b0a5a91ada8e2c0642a5861f1467b24d7d",
  "verdict": "NO-GO",
  "source_identity": {
    "tools/ionic/melt_quench_uma.py": {
      "expected": "e0ab597b426158d6013c6519f074c1acd7055d0cafab622aab3dc6aa77dabd5b",
      "actual": "e0ab597b426158d6013c6519f074c1acd7055d0cafab622aab3dc6aa77dabd5b",
      "unchanged": true
    },
    "tools/ionic/li2s2_stage1_runner.py": {
      "expected": "ac1c01481f853df62788c37c3945748e411868ee0ec781009c454769b61c561b",
      "actual": "ac1c01481f853df62788c37c3945748e411868ee0ec781009c454769b61c561b",
      "unchanged": true
    },
    "db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json": {
      "expected": "40b3edf87f3cd6f49b9c13d40ca915c6622eddfeaadeef918f0f3ec1409878f4",
      "actual": "40b3edf87f3cd6f49b9c13d40ca915c6622eddfeaadeef918f0f3ec1409878f4",
      "unchanged": true
    }
  },
  "selftests": {
    "platform": "Windows",
    "driver": {
      "pass": 220,
      "fail": 0,
      "rc": 0,
      "log": "driver_selftest.txt"
    },
    "runner": {
      "pass": 97,
      "fail": 0,
      "rc": 0,
      "log": "runner_selftest.txt",
      "native_posix_tests_skipped": 3
    },
    "native_linux_reproduced": false,
    "mutation_suite_222_independently_rerun": false
  },
  "limits": [
    "No production UMA/DFT calculations",
    "Runner process interactions use fake handles; real parsers, runner control flow and summaries",
    "Small driver selftest model calculations are included",
    "Original repository unchanged"
  ],
  "findings": [
    {
      "id": "DO-P0-1",
      "severity": "P0",
      "reproduced": true,
      "locations": [
        "melt_quench_uma.py:1754",
        "li2s2_stage1_runner.py:496",
        "li2s2_stage1_runner.py:764"
      ],
      "problem": "Recovery observes melt fail but does not persist it before refusal; later raw species damage permits invalid retry and stage1_pass for both first and later seed.",
      "evidence": "do_melt_policy/results.json",
      "repro": "do_melt_policy/probe_melt.py"
    },
    {
      "id": "DO-P1-1",
      "severity": "P1",
      "reproduced": true,
      "locations": [
        "melt_quench_uma.py:1094",
        "melt_quench_uma.py:1466",
        "melt_quench_uma.py:1480"
      ],
      "problem": "Permissive verdict/history JSON parsing selects last duplicate completion field; full 130-frame evidence becomes n=71 and permits retry plus stage1_pass. Rejudgment normalizes duplicate history.",
      "evidence": "do_consumer_records/results.json",
      "repro": "do_consumer_records/probe.py"
    },
    {
      "id": "DO-P1-2",
      "severity": "P1",
      "reproduced": true,
      "locations": [
        "li2s2_stage1_runner.py:560",
        "li2s2_stage1_runner.py:572",
        "li2s2_stage1_runner.py:736",
        "li2s2_stage1_runner.py:1004"
      ],
      "problem": "Runner or attestation accepts duplicate cost keys and overwrites invalid ledger with last-value normalized JSON; consumer changes from invalid to stage1_pass.",
      "evidence": "do_runner_recovery/results.json",
      "repro": "do_runner_recovery/probe_runner.py"
    },
    {
      "id": "DO-P2-1",
      "severity": "P2",
      "reproduced": true,
      "locations": [
        "melt_quench_uma.py:2006",
        "melt_quench_uma.py:2017",
        "melt_quench_uma.py:2020"
      ],
      "problem": "Malformed nested verdict containers raise during summary and leave previous stage1_pass file. New runner approval bypass not demonstrated.",
      "evidence": "do_consumer_records/results.json"
    },
    {
      "id": "DO-P2-2",
      "severity": "P2",
      "reproduced": false,
      "basis": "Code plus Linux/Python documented signal behavior; no native Linux execution",
      "locations": [
        "li2s2_stage1_runner.py:197",
        "li2s2_stage1_runner.py:882",
        "li2s2_stage1_runner.py:890"
      ],
      "problem": "Launch-time blocked signal mask is inherited by child; parent-only restore does not unblock child, so TERM may escalate to KILL after grace.",
      "sources": [
        "https://man7.org/linux/man-pages/man7/signal.7.html",
        "https://docs.python.org/3/library/subprocess.html"
      ]
    }
  ],
  "controls": {
    "DN_wrong_type_completion_runner": "blocked rc24 launch0, original folder unchanged",
    "DN_wrong_type_completion_consumer": "single string n and list provenance in retained history both rejected as invalid; no stage2",
    "DN_NUL_wording": "aligned with implemented unrecoverable-tail limitation",
    "preplan_twice_judged": "allowed",
    "clear_interrupted_and_real_verdict": "allowed",
    "live_first_seed_failure_before_cleanup": "persists closure; relaunch denied",
    "preserved_folder_identity": "matching identity accepted; mismatch rejected",
    "partial_frame_tail": "only complete frames count",
    "MID_RUN_FILES": "matches ordinary current driver pre-MD/MD emissions",
    "root_results": "probe_results.json",
    "policy_results": "do_melt_policy/controls.json"
  },
  "closure": {
    "DN_P1_exact_type_bug": "closed; duplicate-key completion ambiguity remains a separate P1",
    "DN_P2": "closed",
    "pre_DO_first_seed_live_fail": "closed",
    "pre_DO_rule_M": "open DO-P0-1",
    "pre_DO_preserved_identity_and_interrupted_classification": "closed; record parsing remains open DO-P1-1",
    "pre_DO_post_MD_artifacts": "closed in tested production emission paths",
    "DJ_Q2": "partial; duplicate completion keys still bypass boundary",
    "DJ_Q5": "open DO-P0-1 / DO-P1-1 / DO-P1-2"
  }
}
```

```json
{
  "observed_fail_then_species_damage_11": {
    "root": "<codex>\\do_melt_policy\\li2s2_runner_st_d7gm9y4x\\tmpi03u0yq_",
    "before": {
      "rc": 26,
      "melt": {
        "verdict": "fail",
        "coverage_ok": true,
        "species_ok": true,
        "n_frames_read": 101,
        "read_stop": null
      },
      "kind": "scientific",
      "row": {
        "system": "A",
        "seed": 11,
        "run_id": "09e11778d52e4816a37681185ebc1b87",
        "start": "2026-11-04 19:38:36",
        "start_epoch": 1793788716.8492613,
        "pgid": 990000,
        "start_recovery_clock": {
          "host": "fixture",
          "boot_id": "fixture",
          "kind": "CLOCK_BOOTTIME",
          "seconds": 7200.0
        },
        "retry_of": null,
        "retry_stop_id": null,
        "retry_kind": null,
        "status": "interrupted",
        "end": "2026-11-04 19:38:37",
        "wall_h": 3.0,
        "wall_h_so_far": 2.0,
        "cum_before_h": 0,
        "last_seen": "2026-11-04 19:38:36",
        "cleanup": {
          "leader_rc": -15,
          "group_empty": true,
          "signals": [
            "TERM"
          ],
          "left": []
        },
        "rc": "killed_runner_exit",
        "cost_basis": "measured"
      },
      "files": [
        "plan.json",
        "stage1_attempt.json",
        "thermo.csv",
        "traj.xyz"
      ]
    },
    "after_refusal": {
      "rc": 10,
      "launches": 0,
      "row": {
        "system": "A",
        "seed": 11,
        "run_id": "09e11778d52e4816a37681185ebc1b87",
        "start": "2026-11-04 19:38:36",
        "start_epoch": 1793788716.8492613,
        "pgid": 990000,
        "start_recovery_clock": {
          "host": "fixture",
          "boot_id": "fixture",
          "kind": "CLOCK_BOOTTIME",
          "seconds": 7200.0
        },
        "retry_of": null,
        "retry_stop_id": null,
        "retry_kind": null,
        "status": "interrupted",
        "end": "2026-11-04 19:38:37",
        "wall_h": 3.0,
        "wall_h_so_far": 2.0,
        "cum_before_h": 0,
        "last_seen": "2026-11-04 19:38:36",
        "cleanup": {
          "leader_rc": -15,
          "group_empty": true,
          "signals": [
            "TERM"
          ],
          "left": []
        },
        "rc": "killed_runner_exit",
        "cost_basis": "measured"
      },
      "files": [
        "plan.json",
        "stage1_attempt.json",
        "thermo.csv",
        "traj.xyz"
      ],
      "stop": {
        "at": "2026-11-04 19:38:37",
        "code": "interrupted",
        "reason": "러너 중단 — KeyboardInterrupt: synthetic power cut after complete melt window · 돌던 담금질 그룹을 비웠다 · 그 시드 폴더는 사람이 정한다",
        "terminal": false,
        "cleanup": {
          "leader_rc": -15,
          "group_empty": true,
          "signals": [
            "TERM"
          ],
          "left": []
        },
        "run_id": "09e11778d52e4816a37681185ebc1b87",
        "stop_id": "43f2fe72c747b391"
      }
    },
    "damaged": {
      "melt": {
        "verdict": "invalid",
        "coverage_ok": null,
        "species_ok": false,
        "n_frames_read": 101,
        "read_stop": null
      },
      "kind": "invalid",
      "stage": [
        "md_incomplete",
        "명확한 도중 끊김 (시작된 마지막 기록 스텝 50000 < 끝 경계 64500)"
      ]
    },
    "after_damage_rc": 27,
    "after_damage_launches": 0,
    "new_stop_code": "invalid",
    "retry_rc": 0,
    "retry_launches": 10,
    "track": "stage1_pass",
    "cost_invalid": [],
    "preserved_kind": "invalid"
  },
  "observed_fail_then_species_damage_12": {
    "root": "<codex>\\do_melt_policy\\li2s2_runner_st_d7gm9y4x\\tmpuvgjiqcs",
    "before": {
      "rc": 26,
      "melt": {
        "verdict": "fail",
        "coverage_ok": true,
        "species_ok": true,
        "n_frames_read": 101,
        "read_stop": null
      },
      "kind": "scientific",
      "row": {
        "system": "A",
        "seed": 12,
        "run_id": "f8541ed377d243d3ad89a69c40bed491",
        "start": "2026-11-04 19:38:40",
        "start_epoch": 1793788720.83206,
        "pgid": 990002,
        "start_recovery_clock": {
          "host": "fixture",
          "boot_id": "fixture",
          "kind": "CLOCK_BOOTTIME",
          "seconds": 7200.0
        },
        "retry_of": null,
        "retry_stop_id": null,
        "retry_kind": null,
        "status": "interrupted",
        "end": "2026-11-04 19:38:40",
        "wall_h": 3.0,
        "wall_h_so_far": 2.0,
        "cum_before_h": 10.0,
        "last_seen": "2026-11-04 19:38:40",
        "cleanup": {
          "leader_rc": -15,
          "group_empty": true,
          "signals": [
            "TERM"
          ],
          "left": []
        },
        "rc": "killed_runner_exit",
        "cost_basis": "measured"
      },
      "files": [
        "plan.json",
        "stage1_attempt.json",
        "thermo.csv",
        "traj.xyz"
      ]
    },
    "after_refusal": {
      "rc": 10,
      "launches": 0,
      "row": {
        "system": "A",
        "seed": 12,
        "run_id": "f8541ed377d243d3ad89a69c40bed491",
        "start": "2026-11-04 19:38:40",
        "start_epoch": 1793788720.83206,
        "pgid": 990002,
        "start_recovery_clock": {
          "host": "fixture",
          "boot_id": "fixture",
          "kind": "CLOCK_BOOTTIME",
          "seconds": 7200.0
        },
        "retry_of": null,
        "retry_stop_id": null,
        "retry_kind": null,
        "status": "interrupted",
        "end": "2026-11-04 19:38:40",
        "wall_h": 3.0,
        "wall_h_so_far": 2.0,
        "cum_before_h": 10.0,
        "last_seen": "2026-11-04 19:38:40",
        "cleanup": {
          "leader_rc": -15,
          "group_empty": true,
          "signals": [
            "TERM"
          ],
          "left": []
        },
        "rc": "killed_runner_exit",
        "cost_basis": "measured"
      },
      "files": [
        "plan.json",
        "stage1_attempt.json",
        "thermo.csv",
        "traj.xyz"
      ],
      "stop": {
        "at": "2026-11-04 19:38:40",
        "code": "interrupted",
        "reason": "러너 중단 — KeyboardInterrupt: synthetic power cut after complete melt window · 돌던 담금질 그룹을 비웠다 · 그 시드 폴더는 사람이 정한다",
        "terminal": false,
        "cleanup": {
          "leader_rc": -15,
          "group_empty": true,
          "signals": [
            "TERM"
          ],
          "left": []
        },
        "run_id": "f8541ed377d243d3ad89a69c40bed491",
        "stop_id": "5ede026aed36b522"
      }
    },
    "damaged": {
      "melt": {
        "verdict": "invalid",
        "coverage_ok": null,
        "species_ok": false,
        "n_frames_read": 101,
        "read_stop": null
      },
      "kind": "invalid",
      "stage": [
        "md_incomplete",
        "명확한 도중 끊김 (시작된 마지막 기록 스텝 50000 < 끝 경계 64500)"
      ]
    },
    "after_damage_rc": 27,
    "after_damage_launches": 0,
    "new_stop_code": "invalid",
    "retry_rc": 0,
    "retry_launches": 8,
    "track": "stage1_pass",
    "cost_invalid": [],
    "preserved_kind": "invalid"
  }
}
```

```json
 {
  "commit": "802290db26aea7cf4ba53786c09880ad6f8ad788",
  "fixture_root": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy",
  "tests": {
    "baseline": {
      "root": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmp7lcleo9z",
      "rc": 0,
      "launches": 10,
      "summary": {
        "track": "stage1_pass",
        "cost": {
          "total_h": 50.0,
          "cap_h": 230.0,
          "invalid": [],
          "pending": [],
          "runs": 10,
          "attested": [],
          "closing": [],
          "source": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmp7lcleo9z\\stage1_ledger.json"
        },
        "stage2": {
          "seeds": [
            11,
            12
          ],
          "machines": {
            "11": "kgy",
            "12": "gabia"
          },
          "common_pass_seeds": [
            11,
            12,
            13,
            14,
            15
          ],
          "rule": "두 계 모두 통과한 시드 중 작은 둘 · 기계는 그 순서"
        }
      }
    },
    "history_control": {
      "root": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmppyxr2zay",
      "stage": [
        "md_incomplete",
        "명확한 도중 끊김 (시작된 마지막 기록 스텝 21000 < 끝 경계 64500)"
      ],
      "summary": {
        "track": "stage1_pass",
        "cost": {
          "total_h": 51.0,
          "cap_h": 230.0,
          "invalid": [],
          "pending": [],
          "runs": 11,
          "attested": [],
          "closing": [],
          "source": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmppyxr2zay\\stage1_ledger.json"
        },
        "stage2": {
          "seeds": [
            11,
            12
          ],
          "machines": {
            "11": "kgy",
            "12": "gabia"
          },
          "common_pass_seeds": [
            11,
            12,
            13,
            14,
            15
          ],
          "rule": "두 계 모두 통과한 시드 중 작은 둘 · 기계는 그 순서"
        }
      }
    },
    "duplicate_history_completion": {
      "root": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmppyxr2zay",
      "record_contains_duplicate": 2,
      "stage": [
        "md_incomplete",
        "명확한 도중 끊김 (시작된 마지막 기록 스텝 21000 < 끝 경계 64500)"
      ],
      "kind": "interrupted",
      "summary": {
        "track": "stage1_pass",
        "cost": {
          "total_h": 51.0,
          "cap_h": 230.0,
          "invalid": [],
          "pending": [],
          "runs": 11,
          "attested": [],
          "closing": [],
          "source": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmppyxr2zay\\stage1_ledger.json"
        },
        "stage2": {
          "seeds": [
            11,
            12
          ],
          "machines": {
            "11": "kgy",
            "12": "gabia"
          },
          "common_pass_seeds": [
            11,
            12,
            13,
            14,
            15
          ],
          "rule": "두 계 모두 통과한 시드 중 작은 둘 · 기계는 그 순서"
        }
      }
    },
    "single_history_completion_control": {
      "stage": [
        "unreadable",
        "진행 기록은 도중이지만 판정 이력 1 의 이전 판정 에 일정 끝 (gate_check schedule_complete) 이 적혀 있다 — MD 가 끝났던 흔적 — 보류"
      ],
      "summary": {
        "track": "invalid",
        "cost": {
          "total_h": 51.0,
          "cap_h": 230.0,
          "invalid": [
            "B13: 앞 실행 7ba42d25 폴더의 완료 단계를 못 읽는데 다시 돌렸다 (진행 기록은 도중이지만 판정 이력 1 의 이전 판정 에 일정 끝 (gate_check schedule_complete) 이 적혀 있다 — MD 가 끝났던 흔적 — 보류)"
          ],
          "pending": [],
          "runs": 11,
          "attested": [],
          "closing": [],
          "source": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmppyxr2zay\\stage1_ledger.json"
        },
        "stage2": null
      }
    },
    "nested_type_provenance_list": {
      "root": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmpheaqh34i",
      "result": {
        "raised": "AttributeError",
        "error": "'list' object has no attribute 'get'",
        "persisted_summary_track": "stage1_pass"
      }
    },
    "nested_type_provenance_str": {
      "root": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmpt9wd4hjp",
      "result": {
        "raised": "AttributeError",
        "error": "'str' object has no attribute 'get'",
        "persisted_summary_track": "stage1_pass"
      }
    },
    "nested_type_reasons_list": {
      "root": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmpdmcejvgf",
      "result": {
        "raised": "TypeError",
        "error": "'list' object is not a mapping",
        "persisted_summary_track": "stage1_pass"
      }
    },
    "nested_type_software_list": {
      "root": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmpn_zhtx1w",
      "result": {
        "raised": "AttributeError",
        "error": "'list' object has no attribute 'items'",
        "persisted_summary_track": "stage1_pass"
      }
    },
    "nested_type_run_id_dict": {
      "root": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmpu7rbx7wf",
      "result": {
        "raised": "TypeError",
        "error": "unhashable type: 'dict'",
        "persisted_summary_track": "stage1_pass"
      }
    },
    "duplicate_current_rejudge": {
      "root": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmpj9u8_hxx",
      "before": {
        "stage": [
          "md_incomplete",
          "명확한 도중 끊김 (시작된 마지막 기록 스텝 21000 < 끝 경계 64500)"
        ],
        "kind": "interrupted"
      },
      "new_status": "incomplete",
      "history": {
        "at": "2026-11-04 19:41:08",
        "reason": "수동 (--stage1_verdict)",
        "prev_status": "incomplete",
        "new_status": "incomplete",
        "changed": {
          "status": false,
          "files": [
            "plan.json",
            "thermo.csv",
            "traj.xyz"
          ],
          "card_values": true,
          "driver": true,
          "run_id": true
        },
        "prev_provenance": {},
        "new_provenance": {
          "files_sha256": {
            "plan.json": "fddf38e9564e0594b86c07303348e03cc136cde6de25116b7102ad16c6b4607c",
            "thermo.csv": "6f40223584642ecac780af7b0b6c7440596accb15c28cc17bff590fac4cd54fa",
            "traj.xyz": "2a4e5210f0dcda27dc732c2a106eddf60397fce6cd72f7cb11c0f525de09e8d4",
            "final.xyz": null,
            "result.json": null
          },
          "card_values_sha16": "255adf045a606a46",
          "driver_sha16": "e0ab597b426158d6",
          "⛔": "묶음 판정 (stage1_summary) 이 이 지문을 지금 파일 · 카드 값 · 도구와 다시 잰다 — 안 맞으면 그 시드는 무효 (다시 판정)"
        },
        "prev": {
          "status": "incomplete",
          "provenance": {},
          "gate_check": {
            "schedule_complete": false
          },
          "checks": {
            "traj_frames": {
              "n": 43,
              "expected": 130
            }
          }
        }
      },
      "stage": [
        "md_incomplete",
        "명확한 도중 끊김 (시작된 마지막 기록 스텝 21000 < 끝 경계 64500)"
      ],
      "summary": {
        "track": "stage1_pass",
        "cost": {
          "total_h": 51.0,
          "cap_h": 230.0,
          "invalid": [],
          "pending": [],
          "runs": 11,
          "attested": [],
          "closing": [],
          "source": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmpj9u8_hxx\\stage1_ledger.json"
        },
        "stage2": {
          "seeds": [
            11,
            12
          ],
          "machines": {
            "11": "kgy",
            "12": "gabia"
          },
          "common_pass_seeds": [
            11,
            12,
            13,
            14,
            15
          ],
          "rule": "두 계 모두 통과한 시드 중 작은 둘 · 기계는 그 순서"
        }
      }
    },
    "real_complete_record": {
      "status": "incomplete",
      "traj_frames": {
        "n": 130,
        "expected": 130
      },
      "gate": null
    },
    "real_duplicate_before_retry": {
      "root": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmpi53a4t2i",
      "stage": [
        "md_incomplete",
        "명확한 도중 끊김 (시작된 마지막 기록 스텝 35000 < 끝 경계 64500)"
      ],
      "kind": "interrupted",
      "original_n": 130,
      "duplicate_n": 71
    },
    "real_single_frames_control": {
      "rc": 24,
      "launches": 0,
      "stop": {
        "at": "2026-11-04 19:41:10",
        "code": "resume",
        "reason": "B13: 이전 실행 eb32ebe2 폴더의 완료 단계를 못 읽는다 (진행 기록은 도중이지만 현재 판정 에 궤적 프레임이 다 찼다고 적혀 있다 (130/130) — MD 가 끝났던 흔적 — 보류) — 재담금질하지 않고 보류 · 사람이 본다 (회신 DL: 완료 증거가 남은 폴더는 재시도 대상이 아니다)",
        "terminal": false,
        "sys": "B",
        "seed": 13,
        "run_id": "eb32ebe2008c4763b4d14ec27cb37abe",
        "stop_id": "9e76461c8c1148d3"
      },
      "summary": {
        "track": "pending",
        "cost": {
          "total_h": 27.0,
          "cap_h": 230.0,
          "invalid": [],
          "pending": [],
          "runs": 6,
          "attested": [],
          "closing": [],
          "source": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmpx9imifj8\\stage1_ledger.json"
        },
        "stage2": null
      }
    },
    "real_duplicate_frames_retry": {
      "rc": 0,
      "launches": 5,
      "launched": [
        [
          "B",
          13
        ],
        [
          "A",
          14
        ],
        [
          "B",
          14
        ],
        [
          "A",
          15
        ],
        [
          "B",
          15
        ]
      ],
      "summary": {
        "track": "stage1_pass",
        "cost": {
          "total_h": 52.0,
          "cap_h": 230.0,
          "invalid": [],
          "pending": [],
          "runs": 11,
          "attested": [],
          "closing": [],
          "source": "<codex>\\do_consumer_records\\li2s2_runner_st_cq1qheuy\\tmpi53a4t2i\\stage1_ledger.json"
        },
        "stage2": {
          "seeds": [
            11,
            12
          ],
          "machines": {
            "11": "kgy",
            "12": "gabia"
          },
          "common_pass_seeds": [
            11,
            12,
            13,
            14,
            15
          ],
          "rule": "두 계 모두 통과한 시드 중 작은 둘 · 기계는 그 순서"
        }
      }
    },
    "kind_controls": {
      "interrupted_invalid": "interrupted",
      "ended_invalid": "invalid",
      "orphaned_interrupted_invalid": "interrupted",
      "orphaned_ended_invalid": "invalid",
      "melt_fail_after_invalid": "scientific",
      "melt_invalid": "invalid"
    },
    "ledger_close_preserved_with_invalid": {
      "track": "invalid",
      "A": {
        "status": "invalid",
        "per_seed": {
          "11": "invalid",
          "12": "pass",
          "13": "pass",
          "14": "pass",
          "15": "pass"
        },
        "n_pass": 4,
        "n_fail": 0,
        "n_open": 0,
        "closed_by_first_seed": [
          11
        ]
      },
      "closing": [
        [
          "A",
          11,
          "557fe90f36b548f5bf342e5176809459"
        ]
      ]
    },
    "DN_consumer_string_n": {
      "root": "<codex>\\do_consumer_records\\dn_consumer_string_n_gh0oba8r",
      "folder_stage": [
        "unreadable",
        "진행 기록은 도중이지만 판정 이력 1 의 이전 판정 의 traj_frames 의 n 타입이 str 이다 (기대 int) — 해석할 수 없는 기록 — 보류"
      ],
      "track": "invalid",
      "invalid": [
        "B13: 앞 실행 7ba42d25 폴더의 완료 단계를 못 읽는데 다시 돌렸다 (진행 기록은 도중이지만 판정 이력 1 의 이전 판정 의 traj_frames 의 n 타입이 str 이다 (기대 int) — 해석할 수 없는 기록 — 보류)"
      ],
      "stage2": null
    },
    "DN_consumer_wrong_provenance_type": {
      "root": "<codex>\\do_consumer_records\\dn_consumer_wrong_provenance_type_l755n4o4",
      "folder_stage": [
        "unreadable",
        "진행 기록은 도중이지만 판정 이력 1 의 이전 판정 의 provenance 타입이 list 이다 (기대 dict) — 해석할 수 없는 기록 — 보류"
      ],
      "track": "invalid",
      "invalid": [
        "B13: 앞 실행 7ba42d25 폴더의 완료 단계를 못 읽는데 다시 돌렸다 (진행 기록은 도중이지만 판정 이력 1 의 이전 판정 의 provenance 타입이 list 이다 (기대 dict) — 해석할 수 없는 기록 — 보류)"
      ],
      "stage2": null
    }
  }
}
```

```json
   {
  "commit": "802290db26aea7cf4ba53786c09880ad6f8ad788",
  "fixture_root": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt",
  "tests": {
    "baseline": {
      "root": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt\\tmph4omf9nq",
      "rc": 0,
      "launches": 10,
      "summary": {
        "track": "stage1_pass",
        "cost": {
          "total_h": 50.0,
          "cap_h": 230.0,
          "invalid": [],
          "pending": [],
          "runs": 10,
          "attested": [],
          "closing": [],
          "source": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt\\tmph4omf9nq\\stage1_ledger.json"
        }
      }
    },
    "duplicate_ledger_laundered": {
      "root": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt\\tmp1e1al87a",
      "before": {
        "track": "invalid",
        "cost": {
          "total_h": NaN,
          "cap_h": 230.0,
          "invalid": [
            "장부를 못 읽었다 (ValueError: 같은 열쇠 'wall_h' 가 둘)"
          ],
          "pending": [],
          "runs": 0,
          "attested": [],
          "closing": [],
          "source": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt\\tmp1e1al87a\\stage1_ledger.json"
        }
      },
      "first_rc": 27,
      "first_launches": 0,
      "first_stop": {
        "at": "2026-11-04 19:41:09",
        "code": "invalid",
        "reason": "시작 전 묶음 판정 invalid (자료 · 기록 오류 — 과학적 종료 아님) — 카드와 다른 실행 · 원자료와 안 맞는 판정 · 실행 식별 불일치 · 모르는 판정 상태 · 장부 불완전 · 또는 통과 시드의 소프트웨어 판이 둘 이상 — 자료 · 기록 오류 (과학적 판정 아님) · 고친 뒤 다시 (장부 [\"장부를 못 읽었다 (ValueError: 같은 열쇠 'wall_h' 가 둘)\"])",
        "terminal": false,
        "summary": {
          "per_system": {
            "A": {
              "status": "pass",
              "per_seed": {
                "11": "pass",
                "12": "pass",
                "13": "pass",
                "14": "pass",
                "15": "pass"
              },
              "n_pass": 5,
              "n_fail": 0,
              "n_open": 0,
              "closed_by_first_seed": []
            },
            "B": {
              "status": "pass",
              "per_seed": {
                "11": "pass",
                "12": "pass",
                "13": "pass",
                "14": "pass",
                "15": "pass"
              },
              "n_pass": 5,
              "n_fail": 0,
              "n_open": 0,
              "closed_by_first_seed": []
            }
          },
          "software_variants": [
            {
              "model": "uma-s-1p1",
              "task": "omat",
              "inference": "turbo",
              "fairchem-core": "2.21.0",
              "torch": "2.8.0",
              "ase": "3.26.0"
            }
          ],
          "stage2": null,
          "unknown_status": [],
          "identity_problems": [],
          "cost": {
            "total_h": NaN,
            "cap_h": 230.0,
            "invalid": [
              "장부를 못 읽었다 (ValueError: 같은 열쇠 'wall_h' 가 둘)"
            ],
            "pending": [],
            "runs": 0,
            "attested": [],
            "closing": [],
            "source": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt\\tmp1e1al87a\\stage1_ledger.json"
          },
          "track": "invalid",
          "why": "카드와 다른 실행 · 원자료와 안 맞는 판정 · 실행 식별 불일치 · 모르는 판정 상태 · 장부 불완전 · 또는 통과 시드의 소프트웨어 판이 둘 이상 — 자료 · 기록 오류 (과학적 판정 아님) · 고친 뒤 다시 (장부 [\"장부를 못 읽었다 (ValueError: 같은 열쇠 'wall_h' 가 둘)\"])",
          "stale_verdicts": []
        },
        "stop_id": "68368953db9e4477"
      },
      "after_first": {
        "track": "stage1_pass",
        "cost": {
          "total_h": 50.0,
          "cap_h": 230.0,
          "invalid": [],
          "pending": [],
          "runs": 10,
          "attested": [],
          "closing": [],
          "source": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt\\tmp1e1al87a\\stage1_ledger.json"
        }
      },
      "ack_rc": 0,
      "ack_launches": 0,
      "after_ack": {
        "track": "stage1_pass",
        "cost": {
          "total_h": 50.0,
          "cap_h": 230.0,
          "invalid": [],
          "pending": [],
          "runs": 10,
          "attested": [],
          "closing": [],
          "source": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt\\tmp1e1al87a\\stage1_ledger.json"
        }
      }
    },
    "first_fail_judgment_cut": {
      "root": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt\\tmpc4hbs42n",
      "rc": 26,
      "entry": {
        "system": "A",
        "seed": 11,
        "run_id": "ae0119e3ace54c2dac98924460365df8",
        "start": "2026-11-04 19:41:10",
        "start_epoch": 1793788870.125498,
        "pgid": 990000,
        "start_recovery_clock": {
          "host": "fixture",
          "boot_id": "fixture",
          "kind": "CLOCK_BOOTTIME",
          "seconds": 7200.0
        },
        "retry_of": null,
        "retry_stop_id": null,
        "retry_kind": null,
        "status": "fail",
        "end": "2026-11-04 19:41:10",
        "wall_h": 3.0,
        "wall_h_so_far": 3.0,
        "cum_before_h": 0,
        "last_seen": "2026-11-04 19:41:10",
        "melt_check": {
          "verdict": "fail",
          "message": "이 밀도 · 온도 · 시간에서 사전 정의한 P 골격 이동 기준을 충족하지 못했다 (D 1.34e-11 ≤ 1e-06 cm²/s) — '액체가 없다' 가 아님",
          "at": "2026-11-04 19:41:10"
        },
        "closes_system": true,
        "closes_basis": "first_seed_melt_window_check",
        "cleanup": {
          "leader_rc": -15,
          "group_empty": true,
          "signals": [
            "TERM"
          ],
          "left": []
        },
        "rc": "killed_melt",
        "cost_basis": "measured"
      },
      "restart_rc": 21,
      "restart_launches": 0,
      "summary": {
        "track": "stop_track",
        "cost": {
          "total_h": 3.0,
          "cap_h": 230.0,
          "invalid": [],
          "pending": [],
          "runs": 1,
          "attested": [],
          "closing": [
            [
              "A",
              11,
              "ae0119e3ace54c2dac98924460365df8"
            ]
          ],
          "source": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt\\tmpc4hbs42n\\stage1_ledger.json"
        }
      }
    },
    "first_fail_cleanup_stuck": {
      "root": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt\\tmp9uupvkxi",
      "rc": 21,
      "entry": {
        "system": "A",
        "seed": 11,
        "run_id": "8ce5a89f60e44dd695c598f36d308f01",
        "start": "2026-11-04 19:41:10",
        "start_epoch": 1793788870.2750049,
        "pgid": 990000,
        "start_recovery_clock": {
          "host": "fixture",
          "boot_id": "fixture",
          "kind": "CLOCK_BOOTTIME",
          "seconds": 7200.0
        },
        "retry_of": null,
        "retry_stop_id": null,
        "retry_kind": null,
        "status": "stop_failed",
        "end": null,
        "wall_h": null,
        "wall_h_so_far": 3.0,
        "cum_before_h": 0,
        "last_seen": "2026-11-04 19:41:10",
        "melt_check": {
          "verdict": "fail",
          "message": "이 밀도 · 온도 · 시간에서 사전 정의한 P 골격 이동 기준을 충족하지 못했다 (D 1.34e-11 ≤ 1e-06 cm²/s) — '액체가 없다' 가 아님",
          "at": "2026-11-04 19:41:10"
        },
        "closes_system": true,
        "closes_basis": "first_seed_melt_window_check",
        "cleanup": {
          "leader_rc": -15,
          "group_empty": false,
          "signals": [
            "TERM"
          ],
          "left": [
            990001
          ]
        },
        "rc": "killed_melt"
      },
      "stop": {
        "at": "2026-11-04 19:41:10",
        "code": "melt",
        "reason": "A11 (계의 첫 시드) 녹음 판정 fail — 이 밀도 · 온도 · 시간에서 사전 정의한 P 골격 이동 기준을 충족하지 못했다 (D 1.34e-11 ≤ 1e-06 cm²/s) — '액체가 없다' 가 아님 · 그 계가 닫혀 트랙 전체 멈춤 (장부에 먼저 적었다) · ⚠ 담금질 그룹이 남았다 (pid [990001]) — 손으로 정리",
        "terminal": true,
        "sys": "A",
        "seed": 11,
        "cleanup": {
          "leader_rc": -15,
          "group_empty": false,
          "signals": [
            "TERM"
          ],
          "left": [
            990001
          ]
        },
        "run_id": "8ce5a89f60e44dd695c598f36d308f01",
        "stop_id": "175a0f72aaa53437"
      },
      "restart_rc": 21,
      "restart_launches": 0,
      "summary": {
        "track": "stop_track",
        "cost": {
          "total_h": 0.0,
          "cap_h": 230.0,
          "invalid": [],
          "pending": [
            "A11 런이 끝나지 않았다 (상태 stop_failed · 비용 미확정 — heartbeat 3.0 h 는 하한)"
          ],
          "runs": 1,
          "attested": [],
          "closing": [
            [
              "A",
              11,
              "8ce5a89f60e44dd695c598f36d308f01"
            ]
          ],
          "source": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt\\tmp9uupvkxi\\stage1_ledger.json"
        }
      }
    },
    "stop_declaration_injection": {
      "root": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt\\tmpsl356__k",
      "rc": 24,
      "launches": 0,
      "history": [
        {
          "at": "2026-11-04 19:41:10",
          "code": "interrupted",
          "reason": "러너 중단 — KeyboardInterrupt: 시험: poll 중 Ctrl-C · 돌던 담금질 그룹을 비웠다 · 그 시드 폴더는 사람이 정한다",
          "terminal": false,
          "stop_id": "0f161eed2f36e9a6",
          "run_id": "ab4f2f827cbc4f9a90cc021383bf3ecb",
          "cleanup": {
            "leader_rc": -15,
            "group_empty": true,
            "signals": [
              "TERM"
            ],
            "left": []
          },
          "acked_at": "2026-11-04 19:41:10"
        }
      ],
      "stop": {
        "at": "2026-11-04 19:41:10",
        "code": "resume",
        "reason": "A11: 이전 실행 ab4f2f82 (interrupted) 에 묶여 확인 (--ack_stop) 된 STOP (interrupted · abnormal · resume · cap) 중 재시도 선언이 맞는 것이 없다 — 선언 문제: 재시도 선언이 없다 (사유 · 사건 · 근거 · 선언자 — 결과와 무관한 설비 · 운영 사건만 · Ctrl-C · abnormal · resume 는 사유가 아니다) · 이 멈춤을 확인할 때 선언을 붙인다: --ack_stop <stop_id> --retry_reason <카드 retry_reasons> --retry_event '…' --retry_evidence '…' --declared_by '…'",
        "terminal": false,
        "sys": "A",
        "seed": 11,
        "run_id": "ab4f2f827cbc4f9a90cc021383bf3ecb",
        "stop_id": "9dda99aadd453298"
      }
    },
    "duplicate_attest_lower_bound": {
      "root": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt\\tmpjxge39z9",
      "before": {
        "track": "invalid",
        "cost": {
          "total_h": NaN,
          "cap_h": 230.0,
          "invalid": [
            "장부를 못 읽었다 (ValueError: 같은 열쇠 'wall_h_lower' 가 둘)"
          ],
          "pending": [],
          "runs": 0,
          "attested": [],
          "closing": [],
          "source": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt\\tmpjxge39z9\\stage1_ledger.json"
        }
      },
      "attest_rc": 0,
      "detail": {
        "attested_h": 6.0,
        "evidence": {
          "start": "2026-11-04 19:41:05",
          "start_epoch": 1793788865.6956744,
          "start_recovery_clock": {
            "host": "fixture",
            "boot_id": "fixture",
            "kind": "CLOCK_BOOTTIME",
            "seconds": 7200.0
          },
          "wall_h_lower": 5.0,
          "heartbeat_wall_h_so_far": 5.0,
          "folder": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt\\tmpjxge39z9\\A\\seed11",
          "folder_last_mtime_minus_start_h": 0.0002820027536816067,
          "boot_time_now_epoch": null,
          "suggest_realtime_bound_h": null,
          "⚠": "suggest_realtime_bound_h = 지금 부팅 시각 − 시작 (realtime) — 재부팅 뒤 시계가 맞을 때만 상한이다 (10-16 처럼 2018 로 돌아갔으면 쓰지 않는다) · 폴더 마지막 시각은 하한 쪽 근거다 (정전 때 디스크에 안 쓴 꼬리는 사라진다)"
        }
      },
      "after": {
        "track": "stage1_pass",
        "cost": {
          "total_h": 51.0,
          "cap_h": 230.0,
          "invalid": [],
          "pending": [],
          "runs": 10,
          "attested": [
            "A11 6 h (kgy 정전 (selftest) · selftest)"
          ],
          "closing": [],
          "source": "<codex>\\do_runner_recovery\\li2s2_runner_st_x4j242bt\\tmpjxge39z9\\stage1_ledger.json"
        }
      }
    },
    "stop_no_id": {
      "rc": 10,
      "launches": 0,
      "unchanged": true
    },
    "stop_truncated": {
      "rc": 10,
      "launches": 0,
      "unchanged": true
    }
  }
}
```
