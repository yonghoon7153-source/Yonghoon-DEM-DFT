---
title: "DH 프롬프트 — li2s-2 DG 고침 확인 (7abe7929): 닫는 사건의 재시작 유지 · 모든 탈출 경로의 자식 정리 · 실행 중 상한 · 판정의 원자료 결속 · 선언 시드 전부 판정 · flock · 입력 검사 — 첫 담금질 GO 여부"
date: 2026-11-03
updated: 2026-11-03
tags: [review, li2s, glass, md, uma, density, quench, runner, codex, prompt, letter]
letter: DH
track: li2s
channel: codex
kind: prompt
status: 초안 (2026-11-03) — 사용자 발송 대기 · 기준 커밋 7abe7929
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = li2s-2 (논문 1저자 = 외부 · 위임 10-30). DG (947e83ba0 · NO-GO · P0 3 · P1 5 · P2 3) 다음 편지다 — **고친 곳만** 본다.
> ⛔ li2s 절대 수송값은 싣지 않는다. 기준 커밋 `7abe7929` (브랜치 `claude/friendly-meitner-lldvar`). ⬇ 아래 **보내는 글**만 발송한다.
> 회신이 오면 `codex_DH_reply_li2s2_dg_fixes_2026_11_03.md` 로 원문 보존.

---

**[li2s-2] DG 고침 확인 — 첫 담금질 승인 조건 다섯 (닫는 사건의 재시작 유지 · 예외 시 자식 정리 · 실행 중 상한 · 재시작 원자료 확인 · 미완료 묶음 통과 차단) 이 닫혔나 · 발사 GO 여부**

## 0. 무엇을 묻나

DG 의 P0 셋 · P1 다섯 · P2 셋을 고쳤다 — **지적마다 닫혔는가 (GO / 조건부 / NO-GO) · 고치면서 새로 생긴 구멍은 없는가 · 1 단계를 띄워도 되는가.**
DG 에서 찬성한 것 (window_mto_v1 · 문턱 승계 · invalid > incomplete > fail 우선순위 · 첫 시드가 아닌 시드는 끝난 뒤 판정 · 자기 프로세스 그룹 종료) 은 다시 열지 않아도 된다.
2 단계 전 조건 (MD 압력 도구) 은 이번에도 범위 밖이다.

**가능하면 DG 때의 반례 스크립트 (`dg_probe_gga66ob5` · `dg_lock_race`) 를 이 커밋에 다시 돌려 달라.** 인터페이스가 바뀐 곳 (아래 §2 끝) 은 맞춰서.

## 1. 보는 범위

- `git diff 947e83ba0 7abe7929 -- tools/ionic/melt_quench_uma.py tools/ionic/li2s2_stage1_runner.py db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json`
- 결정 `D-2026-11-03-li2s2-dense-window` (아직 proposed) · 실행 기록 `db/properties/lpscl_glass_dense_window_runlog_2026_11_03.json` 의 `회신_DG_2026_11_03`
- 시험: `python3 tools/ionic/melt_quench_uma.py --selftest` (⭕ 185) · `python3 tools/ionic/li2s2_stage1_runner.py --selftest` (⭕ 36 · Linux flock · 진짜 판독 함수 · 진짜 프로세스 그룹)
- 깨기 (변이) 36/36 빨강 (러너 14 · 드라이버 22 — 목록은 실행 기록 `회신_DG_2026_11_03.반영_시험`) — 고친 곳을 하나씩 되돌리면 해당 시험이 빨개진다 (목록 §2)

## 2. DG 지적별로 한 것 (반례 재현 → 지금 막는 시험 · 깨기)

러너 selftest 는 이제 **가짜 담금질 + 진짜 판독 함수**다 (DG ④): 가짜 담금질이 진짜 드라이버가 쓰는 파일 (plan.json · thermo.csv · traj.xyz · final.xyz · result.json) 을 poll 마다 조금씩 쓰고 (poll 1 = 폴더만 · 2 = plan + 70 ps · 3 = 100 ps · 끝 = final), 러너는 **진짜** `melt_window_check` · `stage1_verdict` · `stage1_summary` · 카드 검사를 부른다. 바탕 구조는 드라이버의 `build_random_cell` (시드 게이트 통과 확인) · 시험 카드는 진짜 카드에서 일정만 줄인 것 (담금질 9 ps · 유지 20 ps · 밀도 = 그 구조 밀도).

**P0-1 닫는 사건의 재시작 유지** — 세 겹:
① 시드 판정 (`combine_stage1`) 이 계의 첫 시드 (카드 기계값 `first_seed` = 11) 녹음 미충족을 **closes_system** 으로 적는다 (러너가 멈춰 일정이 미완이어도 상태 fail · 다른 invalid 이유가 있으면 닫지 않고 invalid) → 묶음 (`summarize_stage1`) 이 그 계를 `closed` → stop_track (나머지가 4/5 통과여도).
② 러너 STOP.json 에 `terminal` · `stop_id` — 닫는 사건 (melt · track) 은 `--ack_stop` 으로도 못 넘긴다 · 나머지 멈춤은 stop_id 가 맞아야 이어가고 장부 `stop_history` 로 옮긴다.
③ 장부 런 항목의 `closes_system` — STOP 을 지워도 거부.
- 시험: DG 재현 그대로 (A11 미충족 → 21 → 같은 run_root 재시작) + `--ack_stop` · STOP 삭제 · STOP + 장부 삭제 — 넷 다 담금질 0 · 21 / 21 / 21 / 20. 첫 시드가 아닌 A12 미충족은 일반 탈락 (A 4/5 → 2 단계 시드 [11, 13]).
- 깨기: 겹마다 하나씩 (terminal 검사 · 장부 closes · 묶음 closes · 시드 판정 closes).

**P0-2 모든 탈출 경로** — `run()` 전체를 `try / except BaseException / finally`: 예외 · Ctrl-C · SIGTERM · SIGHUP (신호는 BaseException 으로 바꿔 `except Exception` 에 안 먹힌다) → 살아 있는 자기 담금질을 `stop()` (자기 프로세스 그룹 TERM → 60 s → KILL → wait) → 장부 항목 끝 (경과 · `interrupted`) → STOP (`interrupted` · 비종결) → **그 다음** 잠금 해제.
담금질을 띄운 **직후** 장부에 런 항목 (`running` · pgid · 시작 시각) 을 쓰고 poll 마다 heartbeat (`wall_h_so_far`). 재시작 때 끝이 안 적힌 항목은: 프로세스 그룹이 살아 있으면 거부 · 죽었으면 고아 런으로 마감 (비용 어림 = max(마지막 heartbeat, 폴더 파일 마지막 시각 − 시작)).
`melt_window_check` 는 plan.json 없음 · 쓰는 중 (JSON 깨짐) · traj 없음을 **incomplete** 로 (예외 아님) · 러너는 판독 예외가 나도 죽지 않고 장부에 적고 다음 poll 에 다시 본다.
- 시험: B11 담금질 중 Ctrl-C → 그 담금질 멈춤 · 장부 끝 · STOP · 잠금 다시 잡힘 · stop_id 없이 · 틀린 stop_id 로 재시작 → 거부 · 맞는 stop_id → 끊긴 B11 폴더에서 멈춤 (24) / poll 이 예외를 던져도 정리 / 담금질 사이 nvidia-smi 예외 / 판독 예외 한 번 → 계속 / 띄운 직후 (첫 poll 전) 장부에 런 항목이 디스크에 있다 / 고아 런 (살아 있음 → 거부 · 죽음 → 어림 마감) / **진짜 프로세스 그룹** (이 Linux 컨테이너): `_Proc.stop` 이 자식 · 손자 (sleep 프로세스) 를 멈추고 기다린다 · 그룹 밖 프로세스는 산다 (≈ 1 s).

**P0-3 실행 중 상한** — 상한 = 카드 기계값 `stage1_cap_gpu_h` (230 · 러너 `--cap_h` 없앰). poll 마다 (누적 + 이 런 경과) ≥ 상한이면 그 담금질을 멈추고 미완결 (22) · 끝난 뒤 넘었으면 통과로 안 올림 · 묶음 판정 (`stage1_summary`) 도 장부 합으로 상한을 다시 잰다 (넘음 · 비유한 → `cap_incomplete` 종료 5 · 장부 없음 → 대기). 상한 멈춤은 카드 상한이 올라갔을 때만 `--ack_stop` 으로 넘긴다.
- 시험: DG 재현 그대로 (아홉 런 20 h · 마지막 60 h) → 마지막 런을 50 h 에서 멈춤 · 22 · 묶음 통과 아님 / 다 통과한 폴더에 장부 합 > 상한 → 미완결 · 장부 없음 → 대기 / 상한 멈춤 ack 만으로는 못 넘김.

**P1-4 원자료 결속** — `stage1_verdict` 가 `final_structure_check` (원자 수 · 조성 (카드 · plan) · 종 순서 (traj 마지막 프레임과) · 셀 (traj 마지막 셀과 · 고정 셀) · 밀도 (카드 · 상대 1e-4)) · traj 프레임 수 (계획과 · thermo 가 끝났는데 다르면 무효) · 판정에 지문 (`provenance`: 원자료 다섯 파일 sha256 · 카드 기계값 sha16 · 드라이버 sha16) 을 싣는다.
`stage1_summary` 는 지문을 지금 파일 · 카드 값 · 도구와 **다시 재고** 안 맞으면 그 시드를 invalid ("다시 판정하라"). 러너는 재시작 때 판정 파일을 믿지 않고 **원자료로 다시 판정**한 뒤 묶음을 본다.
- 시험: final.xyz 에 5 원자 PS₄ → 진짜 stage1_verdict 무효 → 트랙 멈춤 / final 셀 · 밀도 0.98 배 → 무효 / 원자료 없이 통과 판정 파일만 있는 열 폴더 → 묶음 무효 (지문 10 개 불일치) · 러너는 다시 판정 (incomplete) 해 안 띄우고 멈춤 / 판정 뒤 final.xyz 한 바이트 → 그 시드 무효.
- ⛔ 못 하는 것 (도구 docstring 에 적음): 같은 원자 수 · 조성 · 셀의 **다른** 구조로 바꿔치면 최종 구조 대조는 못 잡는다 (원시와 변위는 seed_gate 가 기록만) — 일관된 전면 위조는 막지 않는다.

**P1-5 선언 시드 전부** — 계 통과 = missing · incomplete 0 ∧ pass ≥ need. 조기 탈락 (fail > 시드 수 − need) 은 그대로.
- 시험: 두 계 11–14 통과 · 15 미완 (또는 판정 없음) → 대기.

**P1-6 flock** — `_Lock` = `fcntl.flock(LOCK_EX | LOCK_NB)` 한 번 (수명 동안 보유 · 죽으면 커널이 푼다 · 낡은 잠금 파일은 안 막음) · fcntl 없는 OS 는 O_CREAT|O_EXCL.
- 시험: 잡힌 잠금 → 거부 / 둘째 획득 실패 / 낡은 잠금 파일 (flock 없음) → 통과. (in-process 두 fd 의 flock 충돌로 본다 — 실제 두 프로세스 경쟁은 아니다)

**P1-7 입력 검사** — `validate_li2s2_values` (카드 값을 읽을 때 거부: estimator ≠ window_mto_v1 · 비유한 · 조성 합 · software_required · thermo 열 목록 · first_seed = seeds[0] · 상한) · 비교는 `_same` (NaN · None 은 '다르다') · 녹음 상태 허용 목록 밖 → 무효 (시드 · 묶음 둘 다) · 소프트웨어 = 카드 기계값 `software_required` (model · task 같음 · fairchem-core · torch · ase 판이 있음) · gate_check NVT 는 총압 · virial 두 열이 다 있어야 기록 (`thermo_columns_ok`) · thermo 머리줄에 카드 열이 없으면 무효 · `melt_window_check` 는 읽은 모든 프레임의 원자 수 · 종 순서가 같고 plan · 카드 조성과 맞아야 한다 (종은 창 안 프레임에서).
- 시험: DG 표 다섯 줄 그대로 + 0 번 프레임 종 배치만 바꿈 → 무효 · traj 원자 수 ≠ plan → 무효.

**P1-8 카드 본문** — §1b `2_3단계_MD` 와 §4 S2 `측정_가능` 이 이제 `stage1_summary` 의 `stage2.seeds` · `stage2.machines` (그 순서로 kgy · gabia) 를 가리킨다. 3 단계는 1 단계 통과 시드 전부 · 기계는 시드 홀짝 — 같은 시드가 2 · 3 단계에서 다른 기계일 수 있다는 것을 적었다.

**P2** — 옛 비용 현재형 문구 정리 · NVT plan 의 final_relax 설명 = "고정 밀도 셀" (NPT plan 은 옛 설명) · 담금질 명령은 러너 `build_cmd` 가 카드 기계값에서 반올림 없이 (repr) 만든다 · 손 실행은 `--print_cmd A:11` (진짜 카드 → `--fix_density 1.91347`).

**인터페이스가 바뀐 곳** (반례 스크립트를 다시 돌릴 때): 러너 `--cap_h` 없음 (카드 값) · `--ack_stop` 추가 · 순서는 카드 시드 전부 · 첫 시드 = first_seed · 새 종료코드 26 (러너 중단) · `stage1_summary` 종료 5 (상한 미완결) · `combine_stage1(..., checks=None)` · `summarize_stage1(verdicts, values, cost=None)` — cost 가 None 이면 두 계가 통과여도 대기 · 카드 기계값에 composition · software_required · thermo_required_columns · first_seed · stage1_cap_gpu_h 추가.

## 3. 이것을 특히 봐 달라

1. 닫는 사건의 정의 — "첫 시드 녹음 **fail** ∧ 다른 invalid 이유 없음" 만 closes_system · 첫 시드 녹음 **invalid** 는 무효 (트랙은 invalid 로 멈춤) 로 둔 것이 맞는가.
2. 재시작 때 판정을 원자료로 다시 내며 판정 파일을 덮어쓰는 것 — 덮어쓰기가 정보를 잃는 경로가 있는가 (예: 처음 판정과 다시 낸 판정이 다르면 로그에만 남는다).
3. 러너가 끝날 때 돌던 담금질을 **멈추는** 쪽을 골랐다 (넘겨받지 않는다) — 비용 대비 맞는가 · SIGKILL 된 러너 뒤 고아 런 비용 어림이 상한 회계로 충분한가.
4. `stage1_summary` 가 장부 없이는 통과로 올리지 않는 것 — 회수한 결과를 저장소에서 다시 볼 때 장부도 같이 회수해야 한다 (운영 부담) — 이 정도면 되는가.
5. 새로 생긴 조용히 틀린 경로가 있는가 (특히 러너 시험이 여전히 가짜 담금질이라 못 보는 것 — 프로세스 그룹 멈춤은 sleep 프로세스로 봤고 실제 UMA 담금질 · kgy GPU 로는 아직 안 돌렸다).

## 4. 회신 꼴

판정 (GO / 조건부 GO / NO-GO) · 지적 (P0 · P1 · P2 · 각각 무엇 · 왜 · 최소 수정) · DG 지적마다 닫힘 여부 한 줄.
