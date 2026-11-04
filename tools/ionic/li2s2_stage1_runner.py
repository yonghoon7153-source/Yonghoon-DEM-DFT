#!/usr/bin/env python3
"""li2s2_stage1_runner.py — li2s-2 카드 1 단계 (고정 밀도 담금질 10 개 · kgy 한 기계 · 한 번에 하나) 실행기.

카드 : db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json (§1b · §4 S1 · 기계_판독_값)
결정 : D-2026-11-03-li2s2-dense-window — **active 가 아니면 시작하지 않는다**
회신 DF: P1-2 (판정은 --stage1_verdict 의 필드 · 종료코드를 합치지 않는다) · P1-3 (한쪽 계가 닫히면 트랙 전체 멈춤)
         Q-DF-3 (첫 시드의 100 ps 녹음 판정이 그 담금질과 뒤 시드를 **실제로** 멈춘다)
회신 DG (2026-11-03 NO-GO → 고침):
  P0-1 트랙을 닫는 사건은 **재시작에도 남는다** — 세 겹: STOP.json (닫는 사건은 --ack_stop 으로도 못 넘긴다) · 장부의
       closes_system · 판정 파일의 closes_system (묶음 판정이 그 계를 닫는다 — STOP · 장부를 지워도)
  P0-2 어떤 탈출 경로 (예외 · Ctrl-C · SIGTERM · SIGHUP) 에서도 살아 있는 자기 담금질 (자기 프로세스 그룹) 을 멈추고 기다린 뒤
       장부 (경과 비용) · STOP (사유) 을 쓰고 **그 다음에** 잠금을 푼다 · 시작 직후 파일이 없으면 '미완' 으로 기다린다 ·
       담금질을 띄운 **직후** 장부에 적고 poll 마다 heartbeat (러너가 SIGKILL 로 죽어도 시작 사실 · 경과가 남는다)
  P0-3 상한 = 카드 `stage1_cap_gpu_h` (CLI 로 못 바꾼다) · **실행 중에도** (누적 + 이 런 경과) ≥ 상한이면 그 담금질을 멈추고 미완결 ·
       끝난 뒤 넘었으면 통과로 올리지 않는다 · 묶음 판정도 장부로 상한을 다시 잰다 · 관측 최댓값은 착수 판단용 예상치일 뿐
  P1-4 재시작 때 판정 파일을 믿지 않고 **원자료로 다시 판정** (stage1_verdict) · 묶음 판정은 지문 (원자료 · 카드 값 · 도구) 을 다시 잰다
  P1-6 잠금 = flock (한 번의 시스템 호출 · 러너 수명 동안 보유 · 러너가 죽으면 커널이 푼다)
회신 DH (2026-11-03 NO-GO → 고침):
  P0-1 장부 = 실행 목록 — 산출물은 있는데 장부가 없으면 빈 장부를 만들지 않고 거부 · 런 비용 근거 = 측정 (러너가 끝까지 잼) ·
       보수 상한 (고아 런: 그룹이 죽은 것을 본 시각 − 시작 · heartbeat · 파일 시각은 하한으로만 적음) · 묶음 판정이 장부를 판정과
       대조한다 (누락 · 음수 · 근거 없음 = 무효 · 안 끝난 런 = 대기)
  P0-2 실행 식별자 run_id (담금질마다 uuid · --run_id 로 드라이버에 · plan.json · 장부 · 판정) — 폴더 (계, 시드) = plan = 판정 ·
       run_id 중복 = 한 실행을 여러 시드로 세는 것 = 무효 · 판정의 run_id 가 장부에서 다른 시드면 무효
  P0-3 그룹 정리는 대표 (직접 자식) 의 종료와 그룹 잔존을 따로 본다 — 대표가 먼저 끝나도 (TERM 에 죽든 rc 0 이든) 그룹을 TERM →
       KILL → 비었는지 확인 · 못 비우면 런 항목을 닫지 않고 (stop_failed · 비용 미확정) 멈춘다 · 정상 종료 뒤에도 그룹을 정리한다
  P1-4 첫 시드 녹음 invalid · 묶음 invalid = 자료 · 판독 · 기록 오류 → STOP code "invalid" (종료코드 27 · terminal 아님) —
       과학적 종료 (melt · track) 와 다르다. 재개: 원인을 고치고 그 시드 폴더를 같은 계 폴더 안에 보존한 뒤 해당 run_id의 STOP을 --ack_stop (앞 런 비용 유지)
  P1-5 재판정은 덮어쓰기 전에 이전 판정 전체 · 지문 변화 · 사유를 <시드>/stage1_verdict_history.jsonl 에 남긴다 (드라이버)

DI 수정:
  · 보존된 seed 폴더의 plan/실행 전 기록까지 비용 장부와 대조한다. 보존은 같은 root의 A/B 아래에서 한다.
  · 과학적 pass/fail은 재담금질하지 않는다. invalid만 이전 run_id에 연결된 STOP 확인으로 재시도한다.
  · stage1_attempt.json을 실행 전에 작성한다. plan 이전 중단도 실행 신원을 잃지 않는다.
  · /proc 판독 불가는 빈 그룹이 아니다. 종료 확인 불가이면 그룹 정리 실패/재개 거부로 남긴다.
  · 실행·정리 경과는 monotonic, 고아 상한은 동일 호스트/boot의 BOOTTIME이다. 근거 없으면 비용 미확정.
회신 DJ (2026-11-03 NO-GO → 고침 · 카드 §개정_정전_복구_v2_2026_11_03):
  P0-1 재시도 이력은 필드가 아니라 실행 이력으로 — 소비자가 두 번째 실행부터 재시도 필드를 요구하고 직전 실행 · 확인된 STOP · 선언 ·
       stage1_attempt.json 을 서로 대조한다 · 끊긴 런 재시도 수는 앞 실행 종류로 센다 (필드를 지워도 줄지 않는다)
  P0-2 판정 파일 '없음' 과 '있는데 못 읽음' 을 가른다 (못 읽음 = 차단) · 보존 폴더 · 실행 신원 검사를 invalid 런까지 · 장부 → 폴더 방향도
  P0-3 증언은 하한 (heartbeat · 장부 하한) 이 유한 · 일치할 때만 — 미상이면 비용은 미확정 그대로 · 소비자가 증언 때 하한과 대조
  P1-4 증언은 잠금을 먼저 잡고 그 안에서 읽기 · 검사 · 쓰기 · 이미 확정된 것은 거부
  Q1 재시도 사유는 결과와 무관한 사건 (카드 retry_reasons) 을 --ack_stop 때 선언 (사유 · 사건 · 근거 · 선언자) — Ctrl-C 등은 사유가 아니다
  Q2 MD 완료 · FIRE 미완은 재담금질하지 않고 보류 (FIRE 복구는 새 결정) · MD · 최종까지 돈 invalid 런은 다시 판정 못 하는 이유를 선언
  Q3 증언 필드 = 사건 · 시각 기준 · 불확실성 · H 산출 · 확인자 · 확인 시각 (카드 attestation_required_fields)
  Q4 (DK 에서 바뀜) 상한 런은 budget_cap_raised 만 (카드 cap_retry_reasons) · 정전 추가 예산은 v3 에서 없앴다
회신 DK (2026-11-04 NO-GO → 고침 · 카드 §개정_정전_복구_v3_2026_11_04):
  P0-1 · P1-1 MD 완료의 증거 = 드라이버가 MD 루프 직후 (FIRE 전) 쓰는 md_done.json (run_id · 스텝 · traj · thermo 해시) — 프레임을 세지 않는다 ·
       기록 뒤 궤적이 바뀌면 (손상된 완료 궤적) 판독 불가 = 보류 (재담금질하지 않는다) · 기록이 없으면 미완
  P0-2 실행 상태 (과학적 · 판독 불가 · invalid · 끊긴 런) 는 드라이버 run_kind 한 곳 — 재시도 자격 · 확인 때 선언 검사 · 소비자가 같은 답 ·
       정전 추가 예산은 없앴다 (상한 = 카드 값뿐 · 넘으면 기존 상한 규칙)
  P1-2 소비자도 증언 상한은 양수만
정전 복구 개정 (2026-11-03 · 사용자 '2번으로 가자' · 결과 0 건 · 카드 §개정_정전_복구_2026_11_03):
  · 판정 없이 끊긴 런 (장부 · 보존 폴더 둘 다 판정 없음 · 결과 파일 result.json · final.xyz 없음 · 비용 확정) 은 그 run_id 에 묶여 확인된 STOP
    (interrupted · abnormal · resume · cap) 이 있으면 시드마다 카드 stage1_max_interrupt_retries_per_seed 번까지 다시 돌린다 (retry_eligibility)
  · STOP 마다 그 런의 run_id 를 싣는다 (재시도 확인이 어느 런에 묶이는지)
  · 재부팅을 넘긴 고아 런 비용은 자동으로는 미확정 — `--attest_cost RUN_ID` 가 근거를 모아 보여 주고, `--attest_hours H` + 근거 필드
    (회신 DJ 로 바뀜 — 아래 사용 예) 로 사람이 상한을 적는다 (하한 미상 · 하한 미만 거부 · cost_basis attested_upper_bound) ·
    미확정 고아 런이 있으면 러너가 그 run_id 와 이 명령을 알려 주고 멈춘다

하는 일 (순서 A11 → B11 → A12 → B12 → … → B15 · 계를 번갈아):
  ① 시작 전: 결정 active · 드라이버 sha16 = 고정값 · 카드 값 (드라이버 검사 통과) · 순서 = 카드 시드 전부 · 첫 시드 = 카드 first_seed ·
     잠금 · STOP.json (닫는 사건이면 거부 · 아니면 --ack_stop <stop_id> 가 있어야 이어감) · 장부의 도는 중 런 (프로세스 그룹이
     살아 있으면 거부 · 죽었으면 고아 런으로 비용 어림 마감) · 장부의 closes_system · 판정 파일 다시 판정 → 묶음 판정 (멈춤이면 거부)
  ② 시드마다: 판정이 pass · fail 이면 건너뜀 · 판정이 미완 · 무효거나 판정 없이 런 폴더만 있으면 **멈춤** (끊긴 런을 덮어쓰지 않는다)
  ③ 상한: 누적 + 한 시드 최악 (끝난 런 관측 벽시계와 --seed_worst_h 중 큰 값) > 상한이면 새 시드를 안 띄우고 미완결로 멈춤 ·
     실행 중 poll 마다 누적 + 경과 ≥ 상한이면 그 담금질을 멈추고 미완결
  ④ GPU 가 빌 때까지 기다린다 (memory.used ≤ --start_max_mib 두 번 연속 — cascade 가 끝나면 열린다)
  ⑤ 담금질을 띄운다 (카드 기계값에서 만든 명령 · --print_cmd 로 미리 볼 수 있다) — 계의 **첫 시드**면 --poll_s 마다
     melt_window_check: 미충족 · 무효 → 그 담금질을 멈추고 stage1_verdict (그 계를 닫는 사건) · STOP (닫는 사건) · 미완 → 계속 본다
  ⑥ 담금질 rc 0 → stage1_verdict → stage1_summary → 멈춤이면 멈춤 · rc ≠ 0 → 멈춤 (비정상 종료 · 사용자 결정)
  ⑦ 장부 stage1_ledger.json (시드마다 시작 · heartbeat · 끝 · 벽시계 · rc · 판정 · closes_system · STOP 이력) · 로그 stage1.log

종료코드: 0 1 단계 통과 (2 단계 시드는 stage1_summary.json) · 10 거부 (결정 · sha · 잠금 · 카드 · 순서 · 살아 있는 이전 담금질 · ack)
         20 트랙 멈춤 (묶음 판정) · 21 첫 시드 녹음 미충족 (그 계를 닫음 · 자료 무효는 27) · 22 상한 · 미완결 · 23 담금질 비정상 종료 ·
         24 끊긴 런 폴더 · 25 끝났는데 묶음이 대기 · 26 러너 중단 (예외 · Ctrl-C · 신호 — 그룹을 비웠는지는 STOP cleanup)
         27 자료 · 판독 · 기록 오류 (invalid — 과학적 종료 아님 · 고친 뒤 폴더를 옆으로 옮기고 --ack_stop)

⛔ 이 도구가 못 하는 것
  · GPU 를 다른 잡과 나눠 쓰는지 프로세스별로 못 본다 (kgy 는 프로세스 정보가 막혀 있다) — 총 사용량으로만 기다린다
  · 끊긴 시드를 이어 돌리지 않는다 · 2 단계를 띄우지 않는다 (묶음 판정과 2 단계 시드만 적는다)
  · 러너를 다시 띄우면 돌던 담금질을 넘겨받지 않는다 — 러너가 끝날 때 자기 담금질을 멈춘다 (그 시드는 사람이 정한다)
  · 러너가 SIGKILL 로 죽으면 담금질 (자기 세션) 은 산다 — 재시작이 그 프로세스 그룹이 살아 있는 동안 거부하고, 죽은 뒤엔
    동일 호스트·부팅 구간의 BOOTTIME 근거가 있을 때만 종료 확인까지를 **보수 상한**으로 적는다.
    재부팅·옛 기록·시계 근거 부재이면 비용 미확정으로 막는다. UTC 시각 차로 대체하지 않는다
  · 그룹에서 자기 pgid 를 바꾼 (setsid · setpgid) 손자는 이 그룹 밖이라 못 본다 · /proc 이 없는 OS 는 좀비도 '남음' 으로 셀 수 있다
  · 판정 자체는 하지 않는다 — melt_quench_uma.py 의 melt_window_check · stage1_verdict · stage1_summary 를 부른다 (같은 worktree · sha 고정)
  · flock 은 같은 기계의 로컬 파일시스템에서만 믿는다 (NFS 너머 두 기계의 동시 실행은 못 막는다)
  · 사람이 장부 · STOP · 보존 폴더를 손으로 고치는 것은 못 막는다 — 러너 · --attest_cost 는 잠금 안에서만 쓰고, 묶음 판정 (stage1_summary ·
    ledger_check) 이 장부 · 폴더 · 영수증 · 선언을 다시 대조할 뿐이다 (서로 맞게 꾸민 기록은 대조로 못 잡는다)
  · 재시도 선언 (사유 · 사건 · 근거 · 선언자) 이 참인지 — 결과를 보고 멈춘 것이 아닌지 — 는 모른다. 감사할 수 있게 남길 뿐이다

  python3 tools/ionic/li2s2_stage1_runner.py --worktree ~/wt_li2s2 --run_root ~/work/runs/li2s2_dense_1103 \\
          --python /home/kgy/apps/miniforge3/envs/uma/bin/python
  python3 tools/ionic/li2s2_stage1_runner.py --worktree ~/wt_li2s2 --run_root … --print_cmd A:11   # 명령 확인용 (손 실행은 공식 시드로 자동 편입하지 않음)
  python3 tools/ionic/li2s2_stage1_runner.py --worktree ~/wt_li2s2 --run_root … --attest_cost <run_id>          # 근거만 본다
  python3 tools/ionic/li2s2_stage1_runner.py --worktree ~/wt_li2s2 --run_root … --attest_cost <run_id> --attest_hours H \\
          --attest_event '…' --attest_time_reference '…' --attest_uncertainty_h U --attest_derivation '…' --attest_confirmer '…'
  python3 tools/ionic/li2s2_stage1_runner.py --worktree ~/wt_li2s2 --run_root … --ack_stop <stop_id> \\
          --retry_reason power_outage --retry_event '…' --retry_evidence '…' --declared_by '…'      # 끊긴 런 재시도 영수증
  python3 tools/ionic/li2s2_stage1_runner.py --selftest
"""
from __future__ import annotations
import argparse, datetime, hashlib, importlib.util, json, os, pathlib, shlex, shutil, signal, subprocess, sys, tempfile, threading, time, traceback, uuid, socket, math

EXPECTED_DRIVER_SHA16 = "cd45aa850f3f276a"     # tools/ionic/melt_quench_uma.py — 바뀌면 이 줄도 같이 바꾸고 다시 리뷰한다
EXPECTED_VALUES_SHA16 = "086de59c484f9c32"     # 카드 기계_판독_값 (mq.values_sha16) — ⭐ DO 전 리뷰 P2-12: 카드 값 (상한 포함) 을 바꾸면 이 줄도
                                               #   같이 바꾸고 다시 리뷰한다 (카드 파일만 고쳐서는 상한 멈춤을 넘기지 못한다)
STOP_KEYS = ("at", "code", "reason", "terminal", "stop_id", "run_id", "sys", "seed", "cleanup", "rc", "verdict", "melt", "summary",
             "cum_h", "worst_h", "cap_h")   # 확인 때 stop_history 로 옮기는 열쇠 (⭐ DO 전 리뷰 P2-6 — STOP.json 안의 declaration 등은 옮기지 않는다)
DECISION = "D-2026-11-03-li2s2-dense-window"
CARD_REL = "db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json"
DRIVER_REL = "tools/ionic/melt_quench_uma.py"
SYSTEMS = ("A", "B")
DEFAULT_ORDER = "A:11,B:11,A:12,B:12,A:13,B:13,A:14,B:14,A:15,B:15"
RC = {"pass": 0, "refused": 10, "track": 20, "melt": 21, "cap": 22, "abnormal": 23, "resume": 24, "pending": 25, "interrupted": 26,
      "invalid": 27}
TERMINAL_STOPS = ("melt", "track")       # --ack_stop 으로 못 넘긴다 — 그 계 · 트랙이 카드 규칙으로 **과학적으로** 닫혔다 (새 카드 · 새 run_root)
#: ⭐ 회신 DH P1-4 — "invalid" (자료 · 판독 · 기록 오류) 는 과학적 종료가 아니다: 계속 돌리지 않지만 terminal 도 아니다.
#:   고치는 법: 원인을 고치고 (도구 · 카드는 새 결정 · 새 sha) · 그 시드 폴더를 같은 계 폴더 안에 보존 (예 seed11 → seed11.invalid_<날짜>) · 해당 run_id의 STOP을 --ack_stop.
#:   과학적 종료 (melt · track) 의 "재개" 는 새 카드뿐이다 — 둘을 같은 절차로 다루지 않는다.


class _RunnerSignal(BaseException):
    """SIGTERM · SIGHUP 을 예외로 — except Exception 에 안 먹히고 정리 경로 (자식 멈춤 · 장부 · STOP · 잠금) 를 탄다."""


def _now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sha16(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()[:16]


def decision_state(worktree, did=DECISION):
    D = json.loads((pathlib.Path(worktree) / "db/governance/decisions.json").read_text(encoding="utf-8"))
    hit = [d for d in D["decisions"] if d.get("id") == did]
    return hit[0].get("decision_state") if len(hit) == 1 else None


def load_mq(worktree):
    """같은 worktree 의 melt_quench_uma.py 를 모듈로 (sha 를 본 그 파일)."""
    spec = importlib.util.spec_from_file_location("melt_quench_uma_li2s2", str(pathlib.Path(worktree) / DRIVER_REL))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def parse_order(s):
    out = []
    for tok in s.split(","):
        sysn, seed = tok.strip().split(":")
        if sysn not in SYSTEMS:
            raise ValueError(f"순서에 모르는 계 {sysn}")
        out.append((sysn, int(seed)))
    return out


def check_order(order, vals):
    """순서 = 카드 시드 × 두 계 **전부 · 한 번씩** · 계마다 첫 시드 = 카드 first_seed (첫 시드 녹음 판정의 '첫' 을 카드가 정한다)."""
    why = []
    want = {(s, sd) for s in SYSTEMS for sd in vals["seeds"]}
    if len(order) != len(set(order)):
        why.append("순서에 같은 (계, 시드) 가 두 번 있다")
    if set(order) != want:
        why.append(f"순서가 카드 시드 전부가 아니다 (빠짐 {sorted(want - set(order))} · 남음 {sorted(set(order) - want)})")
    for s in SYSTEMS:
        firsts = [sd for (x, sd) in order if x == s][:1]
        if firsts != [vals["first_seed"]]:
            why.append(f"{s} 의 첫 시드 {firsts} ≠ 카드 first_seed {vals['first_seed']}")
    return why


def _num(x):
    """명령줄 숫자 — 반올림 없이 (repr) · 정수값은 정수로. %g 는 여섯 자리에서 잘라 카드 값과 어긋날 수 있다 (회신 DG P2)."""
    x = float(x)
    return str(int(x)) if x.is_integer() and abs(x) < 1e15 else repr(x)


def build_cmd(python, worktree, run_root, sysn, seed, vals, mq, run_id=None):
    """담금질 명령 — **카드 기계값에서만** 만든다 (손 실행도 --print_cmd 로 같은 명령을 쓴다 · 회신 DG P2)."""
    sched, comp = vals["schedule"], vals["composition"][sysn]
    form, _ = mq.SYSTEMS[sysn]
    n_fu = comp.get("P")
    if not n_fu or {e: n * n_fu for e, n in form.items() if n} != comp:
        raise ValueError(f"카드 조성 {comp} 가 드라이버 식단위 {form} × n_fu 와 안 맞는다")
    return [python, str(pathlib.Path(worktree) / DRIVER_REL), "--system", sysn, "--n_fu", str(n_fu), "--seed", str(int(seed)),
            "--T_melt", _num(sched["T_melt_K"]), "--T_final", _num(sched["T_final_K"]), "--melt_ps", _num(sched["melt_ps"]),
            "--quench_rate", _num(sched["quench_rate_K_s"]), "--hold_ps", _num(sched["hold_ps"]), "--dt_fs", _num(sched["dt_fs"]),
            "--save_ps", _num(sched["save_ps"]), "--turbo", "--fix_density", _num(vals["fix_density_g_cm3"][sysn]),
            "--compress_ps", _num(sched["compress_ps"]), "--out_root", str(run_root)] + (["--run_id", run_id] if run_id else [])


class _Proc:
    """subprocess.Popen 감싸개 — 시험에서 같은 모양의 가짜로 바꾼다. 자기 세션 (start_new_session) = 자기 프로세스 그룹."""
    def __init__(self, cmd, log_path):
        self.fh = open(log_path, "a")
        self.p = subprocess.Popen(cmd, stdout=self.fh, stderr=subprocess.STDOUT, start_new_session=True)
    @property
    def pid(self):
        return self.p.pid
    def poll(self):
        rc = self.p.poll()
        if rc is not None and not self.fh.closed:
            self.fh.close()
        return rc
    def stop(self, grace_s=60, kill_wait_s=30):
        """그 담금질의 **프로세스 그룹 전체**를 멈추고 기다린다 — 이름으로 잡지 않는다 (CLAUDE.md pkill 금지).
        ⭐ 회신 DH P0-3: 대표 (직접 자식) 의 종료와 그룹의 잔존을 따로 본다 — 대표가 먼저 끝나도 남은 일꾼이 있으면 TERM → grace →
        KILL → 다시 확인. 반환 {"leader_rc", "group_empty", "signals", "left"} — group_empty 가 거짓이면 '멈췄다' 로 적지 않는다."""
        pg, sent, errors = self.p.pid, [], []
        def members():
            try:
                return _group_members(pg)
            except (OSError, ValueError, _GroupStateUnknown) as e:
                msg = f"{type(e).__name__}: {e}"
                if msg not in errors:
                    errors.append(msg)
                return None
        def send(sig, label):
            try:
                os.killpg(pg, sig); sent.append(label)
            except ProcessLookupError:
                pass
            except OSError as e:
                errors.append(f"{label}: {type(e).__name__}: {e}")
        self.p.poll()
        if self.p.returncode is None or members() != []:
            send(signal.SIGTERM, "TERM")
        t0 = time.monotonic()
        while time.monotonic() - t0 < grace_s:
            self.p.poll()                                   # 대표를 거둔다 (좀비로 그룹을 붙들지 않게)
            if self.p.returncode is not None and members() == []:
                break
            time.sleep(0.2)
        if self.p.returncode is None or members() != []:
            send(signal.SIGKILL, "KILL")
            t1 = time.monotonic()
            while time.monotonic() - t1 < kill_wait_s:
                self.p.poll()
                if self.p.returncode is not None and members() == []:
                    break
                time.sleep(0.2)
        if self.p.returncode is None:
            try:
                self.p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pass
        if not self.fh.closed:
            self.fh.close()
        left = members()
        return {"leader_rc": self.p.returncode, "group_empty": self.p.returncode is not None and left == [],
                "signals": sent, "left": left, "inspection_errors": errors}
    @property
    def returncode(self):
        return self.p.returncode


class _GroupStateUnknown(RuntimeError):
    """프로세스 그룹의 부재를 확인할 수 없다. False/빈 목록으로 바꾸지 않는다."""


def _group_members(pgid):
    """Linux pgrp 생존자를 반환한다. 빈 목록은 부재 확인, 판독 불가는 예외다.
    조회 중 소멸 (ENOENT/ESRCH)만 무시하며 권한·I/O·형식 오류를 빈 그룹으로 읽지 않는다.
    다른 그룹을 읽지 못하는 환경에서는 killpg(0)의 ESRCH로도 자기 그룹의 부재를 확인한다.
    setsid/setpgid로 그룹을 이탈한 자손은 대상 밖이다.
    """
    pgid = int(pgid)
    if pgid <= 0:
        raise _GroupStateUnknown("pgid must be positive")
    proc, out, errors = pathlib.Path("/proc"), [], []
    if proc.is_dir():
        try:
            for d in proc.iterdir():
                if not d.name.isdigit():
                    continue
                try:
                    st = (d / "stat").read_text()
                    close = st.rfind(")")
                    rest = st[close + 2:].split()
                    if close < 0 or len(rest) < 3:
                        raise ValueError("malformed /proc stat")
                    group = int(rest[2])
                except (FileNotFoundError, ProcessLookupError):
                    continue
                except (OSError, ValueError) as e:
                    errors.append(f"{d.name}: {type(e).__name__}"); continue
                if group == pgid and rest[0] != "Z":
                    out.append(int(d.name))
        except OSError as e:
            errors.append(type(e).__name__)
        if out or not errors:
            return out
    # /proc unavailable or incomplete: only ESRCH proves absence; permission failure is unknown.
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return []
    except (OSError, AttributeError) as e:
        raise _GroupStateUnknown(f"group {pgid}: {type(e).__name__} {errors}") from e
    if errors:
        raise _GroupStateUnknown(f"group {pgid}: unreadable process records {errors[:4]}")
    return [pgid]


def _pg_alive(pgid):
    try:
        return bool(_group_members(pgid))
    except Exception:
        return None  # unknown is not dead; restart refuses it


def _recovery_clock():
    """같은 Linux 호스트·부팅 구간의 BOOTTIME. 재부팅·판독 불가이면 상한을 추정하지 않는다."""
    try:
        boot = pathlib.Path("/proc/sys/kernel/random/boot_id").read_text().strip()
        if not boot:
            return None
        return {"host": socket.gethostname(), "boot_id": boot, "kind": "CLOCK_BOOTTIME",
                "seconds": time.clock_gettime(time.CLOCK_BOOTTIME)}
    except (OSError, AttributeError):
        return None


def _is_num(x):
    """수 타입 (int · float) 이고 유한 — bool · 글자 ('100') 는 아니다 (⭐ DO 전 리뷰 P1-3)."""
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _orphan_upper_hours(ent, now):
    start = ent.get("start_recovery_clock")
    if not isinstance(start, dict) or not isinstance(now, dict):
        return None
    keys = ("host", "boot_id", "kind")
    if any(not start.get(k) or start.get(k) != now.get(k) for k in keys):
        return None
    lo_ = ent.get("wall_h_so_far", 0.0)
    if not (_is_num(now.get("seconds")) and _is_num(start.get("seconds")) and _is_num(lo_)):
        return None
    try:
        elapsed = (float(now["seconds"]) - float(start["seconds"])) / 3600.0
        lower = float(lo_)
    except (KeyError, TypeError, ValueError, OverflowError):
        return None
    return elapsed if math.isfinite(elapsed) and math.isfinite(lower) and elapsed >= max(0.0, lower) else None



def _gpu_used_mib():
    out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                         capture_output=True, text=True, check=True, timeout=60).stdout   # ⭐ DO 전 리뷰 P2-18 — 멈춘 GPU 에 매달리지 않는다
    return int(out.split()[0])


class _Lock:
    """한 run_root 에 러너 하나 — flock (원자적 · 수명 동안 보유 · 프로세스가 죽으면 커널이 푼다 · 회신 DG P1-6).
    fcntl 이 없는 OS 는 O_CREAT|O_EXCL 로 (그때는 낡은 잠금 파일을 사람이 지운다)."""
    def __init__(self, path):
        self.path, self.fd, self.kind = pathlib.Path(path), None, None
    def acquire(self):
        try:
            import fcntl
        except ImportError:
            try:
                self.fd = os.open(str(self.path) + ".excl", os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            except FileExistsError:
                return False
            os.write(self.fd, f"{os.getpid()}\n".encode()); self.kind = "excl"
            return True
        fd = os.open(str(self.path), os.O_RDWR | os.O_CREAT, 0o644)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            os.close(fd)
            return False
        os.ftruncate(fd, 0); os.write(fd, f"{os.getpid()}\n".encode())
        self.fd, self.kind = fd, "flock"
        return True
    def release(self):
        if self.fd is None:
            return
        if self.kind == "flock":
            import fcntl
            fcntl.flock(self.fd, fcntl.LOCK_UN); os.close(self.fd)
        else:
            os.close(self.fd)
            try:
                os.unlink(str(self.path) + ".excl")
            except FileNotFoundError:
                pass
        self.fd = None


def _folder_run_id(rd):
    for name in ("stage1_attempt.json", "plan.json"):
        try:
            rid = json.loads((pathlib.Path(rd) / name).read_text(encoding="utf-8")).get("run_id")
            if isinstance(rid, str) and rid:
                return rid
        except (OSError, ValueError, AttributeError):
            continue
    return None


def retry_eligibility(attempts, stop_history, inventory, values, mq):
    """⭐ 정전 복구 · 회신 DJ — 같은 계 · 시드의 이전 실행 **전부** (장부 순서 · invalid 런 포함) 를 보고 다시 돌려도 되는지 가른다.
    실행마다:
      · 장부 판정 pass · fail → invalid (과학적 판정 — 다시 담금질하지 않는다)
      · 보존 폴더를 못 찾음 (같은 계 폴더 안 · 실행 전 기록의 run_id) → resume (보존 누락 · 회신 DJ P0-2)
      · 폴더 판정 파일 pass · fail → invalid · **있는데 못 읽음** → invalid ('판정 없음' 으로 읽지 않는다 · 회신 DJ P0-2)
      · 비용 미확정 → resume (고아 런이면 --attest_cost)
      · 완료 단계 (mq.folder_stage_detail) 판독 불가 → resume — 완료 기록 · 임시 기록 · plan 없는 산출물 · FIRE 로그 · 기록 없이 끝 경계
        (완료 여부 불명) 도 여기 (회신 DL P0 · Q2 — 명확한 도중 끊김만 재시도 대상)
      · 종류 = invalid (장부 · 폴더 판정 invalid) 아니면 interrupted — interrupted 인데 최종 산출 → resume (판정하라) ·
        **MD 완료 · FIRE 미완 → resume (보류 — 재담금질하지 않는다 · FIRE 복구는 새 결정 · 회신 DJ Q2)**
    끊긴 런 재시도 수 (앞 실행 종류가 interrupted 인 것 — 필드가 아니라 실행 이력으로 센다) > 카드 한도 → invalid.
    마지막 실행에 묶여 확인된 STOP (종류별 code — mq.RETRY_BIND_CODES) 중 **재시도 선언이 맞는 것** (mq.declaration_problems — 결과와
    무관한 사유 · 사건 · 근거 · 선언자 · MD 까지 돈 invalid 런이면 다시 판정 못 하는 이유 · 상한 런 규칙 · 회신 DJ Q1 · Q4) 이 없으면 그 종류의
    code (invalid · resume) 로 멈춘다 — 그 멈춤을 선언과 함께 --ack_stop 하면 영수증이 된다.
    반환 {"ok", "code", "why", "retry_of", "stop_id", "kind", "stage"}."""
    n_int, kinds, stages = 0, [], []
    for x in attempts:
        rid = x.get("run_id")
        tag = str(rid)[:8]
        v = x.get("verdict")
        if v in ("pass", "fail"):
            return {"ok": False, "code": "invalid", "why": f"이전 실행 {tag} 에 과학적 판정 ({v}) 이 있다 — 다시 담금질하지 않는다 (카드: 미통과 시드는 기록 · 제외)"}
        rec = inventory.get(rid) if isinstance(rid, str) else None
        if rec is None:
            return {"ok": False, "code": "resume", "why": f"이전 실행 {tag} 폴더를 못 찾는다 (invalid 런 포함) — 같은 계 폴더 안에 옆으로 옮겨 보존해야 한다 "
                                                         "(지우거나 run_root 밖으로 옮기지 않는다)"}
        rk = mq.run_kind(x, rec["path"], values)             # ⭐ 회신 DK P0-2 — 소비자 · 확인 검사와 같은 분류 (DO 전 리뷰 — 보존 폴더 녹음까지)
        if rk == "scientific":
            return {"ok": False, "code": "invalid", "why": f"이전 실행 {tag} 에 과학적 판정 (장부 · 폴더) 이 있다 — 다시 담금질하지 않는다"}
        if rk == "unreadable":
            return {"ok": False, "code": "invalid", "why": f"이전 실행 {tag} 의 판정을 못 읽는다 (폴더 판정 파일 · 장부 값) — '판정 없음' 으로 읽지 않는다 "
                                                          "(원자료로 --stage1_verdict 다시 판정한 뒤 다시)"}
        if x.get("end") is None or x.get("cost_basis") not in mq.COST_BASES:
            return {"ok": False, "code": "resume", "why": f"이전 실행 {tag} 비용이 확정 안 됐다 ({x.get('cost_basis')}) — 고아 런이면 --attest_cost {rid}"}
        st, st_why = mq.folder_stage_detail(rec["path"])
        if st == "unreadable":
            return {"ok": False, "code": "resume", "why": f"이전 실행 {tag} 폴더의 완료 단계를 못 읽는다 ({st_why}) — 재담금질하지 않고 보류 · "
                                                         "사람이 본다 (회신 DL: 완료 증거가 남은 폴더는 재시도 대상이 아니다)"}
        kind = rk
        if kind == "interrupted":
            if st == "final":
                return {"ok": False, "code": "resume", "why": f"이전 실행 {tag} 이 끝까지 돌았다 (result.json · final.xyz) — 다시 돌리지 말고 "
                                                             "그 폴더를 --stage1_verdict 로 판정"}
            if st == "md_complete":
                return {"ok": False, "code": "resume", "why": f"이전 실행 {tag} 은 MD 가 끝났고 FIRE 만 못 마쳤다 — 재담금질하지 않고 보류 "
                                                             "(그 마지막 구조에서 정해진 FIRE 만 다시 하는 복구는 새 결정 · 회신 DJ Q2)"}
            n_int += 1
        kinds.append(kind); stages.append(st)
    lim = int(values["stage1_max_interrupt_retries_per_seed"])
    if n_int > lim:
        return {"ok": False, "code": "invalid", "why": f"끊긴 런 재시도가 카드 한도 {lim} 를 넘는다 ({n_int}) — 새 결정 없이는 다시 안 돌린다"}
    prev, kind, st = attempts[-1], kinds[-1], stages[-1]
    codes = mq.RETRY_BIND_CODES[kind]
    rejudge = kind == "invalid" and st in ("final", "md_complete")
    bound = [(h, mq.declaration_problems(h.get("declaration"), kind, values, rejudge_needed=rejudge,
                                         prev_status=prev.get("status_before_orphan") or prev.get("status")))
             for h in stop_history if h.get("acked_at") and h.get("run_id") == prev.get("run_id") and h.get("code") in codes]
    good = [h for h, pr in bound if not pr]
    if not good:
        why = (f"이전 실행 {str(prev.get('run_id'))[:8]} ({kind}) 에 묶여 확인 (--ack_stop) 된 STOP ({' · '.join(codes)}) 중 재시도 선언이 맞는 것이 없다"
               + (" — 선언 문제: " + " / ".join(" · ".join(pr) for _, pr in bound) if bound else "")
               + " · 이 멈춤을 확인할 때 선언을 붙인다: --ack_stop <stop_id> --retry_reason <카드 retry_reasons> --retry_event '…' "
                 "--retry_evidence '…' --declared_by '…'" + (" --rejudge_impossible_reason '…'" if rejudge else ""))
        return {"ok": False, "code": "invalid" if kind == "invalid" else "resume", "why": why}
    return {"ok": True, "code": None, "why": None, "retry_of": prev["run_id"], "stop_id": good[-1]["stop_id"], "kind": kind, "stage": st}


def declaration_from_args(a):
    """--ack_stop 에 붙인 재시도 선언 (없으면 None) — 선언 시각은 자동."""
    f = {"reason": getattr(a, "retry_reason", None), "event": getattr(a, "retry_event", None),
         "evidence": getattr(a, "retry_evidence", None), "declared_by": getattr(a, "declared_by", None),
         "rejudge_impossible_reason": getattr(a, "rejudge_impossible_reason", None)}
    if all(x is None for x in f.values()):
        return None
    d = {k: x for k, x in f.items() if x is not None}
    d["declared_at"] = _now()
    return d


def ack_declaration_problems(decl, sp, led, values, mq, run_root):
    """확인 (--ack_stop) 때 선언을 바로 검사한다 (회신 DJ Q1) — 그 멈춤이 어떤 실행에 묶였나 · 그 code 가 어느 종류의 영수증이 되나 ·
    그 실행의 장부 상태 (상한 규칙) · 폴더 완료 단계 (MD 까지 돈 invalid 런이면 다시 판정 못 하는 이유). 문제 목록."""
    rid, code = sp.get("run_id"), sp.get("code")
    if not rid:
        return ["이 멈춤은 특정 실행 (run_id) 에 묶여 있지 않다 — 재시도 선언을 붙일 곳이 아니다"]
    hit = [r for r in led.get("runs", []) if isinstance(r, dict) and r.get("run_id") == rid]
    if len(hit) != 1:
        return [f"장부에 run_id {str(rid)[:8]} 런이 {len(hit)} 개"]
    inv_, _ = mq.attempt_inventory(run_root)
    rec = inv_.get(rid)
    kind = mq.run_kind(hit[0], rec["path"] if rec else None, values)   # 그 실행의 종류 (code 가 아니라 실행에서 · 회신 DK P0-2 — 한 분류)
    if kind == "scientific":
        return ["이 실행에는 과학적 판정 (pass · fail) 이 있다 — 재시도 대상이 아니다 (선언을 받지 않는다)"]
    if kind == "unreadable":
        return ["이 실행의 판정을 못 읽는다 (폴더 판정 파일 · 장부 값) — 원자료로 --stage1_verdict 다시 판정한 뒤 확인한다 (선언을 받지 않는다)"]
    if code not in mq.RETRY_BIND_CODES[kind]:
        return [f"이 멈춤 ({code}) 은 이 실행 ({kind}) 의 재시도 영수증이 될 수 없다 — 묶는 code {list(mq.RETRY_BIND_CODES[kind])}"]
    st = mq.folder_stage(rec["path"]) if rec else None
    return mq.declaration_problems(decl, kind, values, rejudge_needed=(kind == "invalid" and st in ("final", "md_complete")),
                                   prev_status=hit[0].get("status_before_orphan") or hit[0].get("status"))


def _btime():
    try:
        for ln in pathlib.Path("/proc/stat").read_text().splitlines():
            if ln.startswith("btime "):
                return float(ln.split()[1])
    except OSError:
        pass
    return None


def _attest_evidence(R, e, deps):
    """증언에 쓸 근거를 모은다 (읽기만) — 마지막 heartbeat = 하한 · 시작 시각 · 시작 boot 시계 · 지금 부팅 시각 · 보존 폴더 파일 마지막 시각."""
    rd = R / str(e.get("system")) / f"seed{e.get('seed')}"
    mt = None
    for cand in [rd] + sorted((R / str(e.get("system"))).glob(f"seed{e.get('seed')}*")):
        if cand.is_dir() and (cand / "stage1_attempt.json").is_file():
            try:
                if json.loads((cand / "stage1_attempt.json").read_text(encoding="utf-8")).get("run_id") == e.get("run_id"):
                    mt = max((f.stat().st_mtime for f in cand.iterdir() if f.is_file()), default=None); rd = cand; break
            except (OSError, ValueError):
                pass
    bt = deps.get("btime", _btime)()
    se = e.get("start_epoch")
    se_ok = isinstance(se, (int, float)) and not isinstance(se, bool) and math.isfinite(se)
    return {"start": e.get("start"), "start_epoch": se, "start_recovery_clock": e.get("start_recovery_clock"),
            "wall_h_lower": e.get("wall_h_lower"), "heartbeat_wall_h_so_far": e.get("wall_h_so_far"), "folder": str(rd),
            "folder_last_mtime_minus_start_h": ((mt - float(se)) / 3600.0) if (mt is not None and se_ok) else None,
            "boot_time_now_epoch": bt,
            "suggest_realtime_bound_h": ((bt - float(se)) / 3600.0) if (bt is not None and se_ok and bt > float(se)) else None,
            "⚠": "suggest_realtime_bound_h = 지금 부팅 시각 − 시작 (realtime) — 재부팅 뒤 시계가 맞을 때만 상한이다 (10-16 처럼 2018 로 돌아갔으면 "
                  "쓰지 않는다) · 폴더 마지막 시각은 하한 쪽 근거다 (정전 때 디스크에 안 쓴 꼬리는 사라진다)"}


def _finite_nonneg(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and x >= 0


def attest_cost(run_root, run_id, values, hours=None, fields=None, deps=None):
    """⭐ 정전 복구 · 회신 DJ P0-3 · P1-4 · Q3 — 재부팅을 넘긴 고아 런 (cost_basis unknown) 의 비용 상한을 사람이 근거를 보고 적는다.
    hours 가 없으면 근거만 모아 보여 준다 (읽기만 · 쓰지 않는다).
    hours 가 있으면 **잠금을 먼저 잡고** 장부를 그 안에서 다시 읽어 검사 · 쓰기까지 한다 (잠금 전에 읽은 장부로 덮어쓰지 않는다 · P1-4):
      · 그 런이 orphaned · unknown 이어야 — 이미 증언 · 확정이면 두 번째 쓰기를 거부
      · 하한 (wall_h_lower) 과 heartbeat (wall_h_so_far) 가 유한한 비음수 · 하한 ≥ heartbeat — 아니면 **하한 미상**: 증언을 받지 않고
        비용은 미확정 그대로 (P0-3 · 미상을 비교 생략으로 처리하지 않는다)
      · H 는 유한 · 양수 · 하한 이상
      · 근거 필드 (카드 attestation_required_fields — 사건 · 시각 기준 · 불확실성 h · H 산출 방식 · 확인자 · 확인 시각 (자동)) 가 다 있어야 (Q3)
      → cost_basis attested_upper_bound + attestation {필드 · lower_at_attest · heartbeat_at_attest · evidence · os_user · host}.
    ⛔ 못 하는 것: 상한이 맞는지는 모른다 — 사람이 근거를 보고 정한 값이다 · 확인자가 실제 그 사람인지 못 본다 (OS 사용자 · 호스트를 같이 적는다)."""
    deps = deps or {}
    R = pathlib.Path(run_root)
    led_p = R / "stage1_ledger.json"
    if hours is None:                                        # 근거 보기 — 읽기만
        led = json.loads(led_p.read_text(encoding="utf-8"))
        hit = [e for e in led.get("runs", []) if isinstance(e, dict) and e.get("run_id") == run_id]
        if len(hit) != 1:
            return 10, {"why": f"장부에 run_id {run_id} 가 {len(hit)} 개"}
        return 0, {"evidence": _attest_evidence(R, hit[0], deps), "status": hit[0].get("status"), "cost_basis": hit[0].get("cost_basis"),
                   "required_fields": list(values["attestation_required_fields"])}
    if deps.get("before_lock"):
        deps["before_lock"]()                                # 시험: 잠금 전에 다른 기록자가 끼어드는 순서
    lock = _Lock(R / "stage1.lock")
    if not lock.acquire():
        return 10, {"why": "러너 (또는 다른 증언) 가 잠금을 잡고 있다 — 멈춘 뒤 적는다 (아무것도 안 썼다)"}
    try:
        led = json.loads(led_p.read_text(encoding="utf-8"))  # ⭐ 잠금 안에서 다시 읽는다
        hit = [e for e in led.get("runs", []) if isinstance(e, dict) and e.get("run_id") == run_id]
        if len(hit) != 1:
            return 10, {"why": f"장부에 run_id {run_id} 가 {len(hit)} 개"}
        e = hit[0]
        ev = _attest_evidence(R, e, deps)
        if e.get("cost_basis") == "attested_upper_bound" or e.get("attestation") is not None:
            return 10, {"why": "그 런은 이미 증언으로 확정됐다 — 두 번째 쓰기를 거부 (바꾸려면 결정)", "evidence": ev}
        if not (e.get("status") == "orphaned" and e.get("cost_basis") == "unknown"):
            return 10, {"why": f"그 런은 고아 · 비용 미확정이 아니다 (상태 {e.get('status')} · 근거 {e.get('cost_basis')}) — 증언 상한을 쓰지 않는다",
                        "evidence": ev}
        lo, hb = e.get("wall_h_lower"), e.get("wall_h_so_far")
        if not (_finite_nonneg(lo) and _finite_nonneg(hb) and lo >= hb - 1e-9):
            return 10, {"why": f"하한이 미상 · 잘못이다 (하한 {lo!r} · heartbeat {hb!r}) — 증언을 받지 않는다 · 비용은 미확정 그대로 (새 결정)",
                        "evidence": ev}
        try:
            h = float(hours)
        except (TypeError, ValueError):
            return 10, {"why": f"hours {hours!r} 가 수가 아니다", "evidence": ev}
        if not (math.isfinite(h) and h > 0 and h >= float(lo)):
            return 10, {"why": f"hours {h} 가 유한한 양수가 아니거나 하한 {lo} h 보다 작다", "evidence": ev}
        fields = dict(fields or {})
        rec, miss = {}, []
        for f_ in values["attestation_required_fields"]:
            if f_ == "confirmed_at":
                continue
            x = fields.get(f_)
            if f_ == "uncertainty_h":
                try:
                    x = float(x)
                except (TypeError, ValueError):
                    x = None
                if x is None or not _finite_nonneg(x):
                    miss.append(f_); continue
            elif not (isinstance(x, str) and x.strip()):
                miss.append(f_); continue
            rec[f_] = x.strip() if isinstance(x, str) else x
        if miss:
            return 10, {"why": f"근거 필드가 없다 · 잘못이다: {miss} (카드 attestation_required_fields)", "evidence": ev}
        try:
            import getpass
            os_user = getpass.getuser()
        except Exception:
            os_user = None
        e.update(wall_h=h, cost_basis="attested_upper_bound",
                 attestation={**rec, "confirmed_at": _now(), "lower_at_attest": lo, "heartbeat_at_attest": hb, "evidence": ev,
                              "os_user": os_user, "host": socket.gethostname(), "tool": "li2s2_stage1_runner.py --attest_cost"})
        _write_json_atomic(led_p, led)
    finally:
        lock.release()
    return 0, {"attested_h": h, "evidence": ev}


def _write_json_atomic(path, obj):
    """임시 파일에 쓰고 fsync → 이름 교체 → 디렉터리 fsync (⭐ DO 전 리뷰 P2-14 — 장부 · STOP · 실행 전 기록이 정전 뒤 빈 파일로 돌아오지 않게.
    저장장치 쓰기 캐시까지 보증하지는 않는다)."""
    path = pathlib.Path(path)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, ensure_ascii=False, indent=1, default=str))
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)
    if os.name == "posix":
        fd = os.open(str(path.parent), os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def run(a, deps=None):
    deps = deps or {}
    W, R = pathlib.Path(a.worktree), pathlib.Path(a.run_root)
    R.mkdir(parents=True, exist_ok=True)
    sleep, clock, wall = deps.get("sleep", time.sleep), deps.get("clock", time.monotonic), deps.get("wall", time.time)
    recovery_clock = deps.get("recovery_clock", _recovery_clock)
    gpu_used, launch, pg_alive = deps.get("gpu_used", _gpu_used_mib), deps.get("launch", _Proc), deps.get("pg_alive", _pg_alive)
    logf = open(R / "stage1.log", "a")
    def log(*m):
        line = f"[{_now()}] " + " ".join(str(x) for x in m)
        print(line, flush=True); logf.write(line + "\n"); logf.flush()
    led_p, stop_p = R / "stage1_ledger.json", R / "STOP.json"
    state = {"h": None, "entry": None, "t0": None, "ledger": None, "stopped": False}
    def save_ledger():
        if state["ledger"] is not None:
            _write_json_atomic(led_p, state["ledger"])
    def stop(code, reason, **detail):
        rec = {"at": _now(), "code": code, "reason": reason, "terminal": code in TERMINAL_STOPS, **detail}
        rec["stop_id"] = hashlib.sha256(json.dumps(rec, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()[:16]
        _write_json_atomic(stop_p, rec)
        state["stopped"] = True
        log(f"⛔ 멈춤 ({code}) — {reason} · stop_id {rec['stop_id']}")
        return RC[code]
    def finish(ent, rc, status, wall_h, cleanup=None):
        """런 항목을 닫는다 — **그룹이 비었을 때만** (회신 DH P0-3). 그룹이 남았으면 항목을 열어 둔 채 (end 없음 · 비용 미확정)
        stop_failed 로 적고 False — 재시작이 그 그룹이 살아 있는 동안 거부하고 죽은 뒤 보수 상한으로 마감한다."""
        if cleanup is not None:
            ent["cleanup"] = cleanup
        if cleanup is not None and not cleanup.get("group_empty"):
            ent.update(status="stop_failed", rc=rc, wall_h_so_far=wall_h, last_seen=_now())
            state["entry"] = None
            save_ledger()
            return False
        ent.update(end=_now(), wall_h=wall_h, rc=rc, status=status, cost_basis="measured")
        state["entry"] = None
        save_ledger()
        return True
    def cost_so_far():
        return sum(float(r["wall_h"] if r.get("wall_h") is not None else (r.get("wall_h_so_far") or 0.0))
                   for r in state["ledger"]["runs"])
    def stop_child(why):
        """살아 있는 자기 담금질을 멈추고 기다린다 — 어떤 탈출 경로에서도 (회신 DG P0-2)."""
        h = state["h"]
        if h is None:
            return None
        log(f"  ⚠ {why} — 담금질 프로세스 그룹 {getattr(h, 'pid', '?')} 를 정리한다 (대표가 끝났어도 그룹을 본다)")
        res_ = h.stop()
        state["h"] = None
        if not res_.get("group_empty"):
            log(f"  ⛔ 그룹이 비지 않았다 (남은 pid {res_.get('left')}) — '멈췄다' 로 적지 않는다 · 손으로 본다")
        return res_

    # ① 시작 전 점검 (부작용 없음)
    st = decision_state(W)
    if st != "active":
        log(f"⛔ 결정 {DECISION} 이 active 가 아니다 ({st}) — 시작하지 않는다"); logf.close(); return RC["refused"]
    s16 = sha16(W / DRIVER_REL)
    if s16 != a.expect_sha:
        log(f"⛔ 드라이버 sha16 {s16} ≠ 고정값 {a.expect_sha} — 시작하지 않는다"); logf.close(); return RC["refused"]
    mq = deps.get("mq") or load_mq(W)
    try:
        vals = mq.read_li2s2_values(W / CARD_REL)
        order = parse_order(a.order)
        bad = check_order(order, vals)
        if bad:
            raise ValueError(" · ".join(bad))
        for s in SYSTEMS:
            build_cmd(a.python, W, R, s, vals["first_seed"], vals, mq)
    except Exception as e:
        log(f"⛔ 카드 값 · 순서를 못 받았다 ({type(e).__name__}: {e}) — 시작하지 않는다"); logf.close(); return RC["refused"]
    want_v = getattr(a, "expect_values_sha16", None)
    if want_v is not None and mq.values_sha16(vals) != want_v:   # ⭐ DO 전 리뷰 P2-12 — 카드 값 (상한 포함) 은 러너 고정값과 같아야 한다
        log(f"⛔ 카드 기계_판독_값 지문 {mq.values_sha16(vals)} ≠ 러너 고정값 {want_v} — 카드 값을 바꿨으면 러너 고정값도 같이 바꾸고 다시 리뷰한다 "
            "(시작하지 않는다)"); logf.close(); return RC["refused"]
    if not deps.get("python_ok", lambda x_: shutil.which(x_) is not None)(a.python):   # ⭐ DO 전 리뷰 P2-8 — 발사 실패가 재시도 한도를 먹지 않게
        log(f"⛔ --python {a.python!r} 를 실행할 수 없다 — 시작하지 않는다"); logf.close(); return RC["refused"]
    cap_base = float(vals["stage1_cap_gpu_h"])               # 상한 = 카드 값뿐 (정전 손실로 늘리지 않는다 — 회신 DK · 카드 v3)
    lock = _Lock(R / "stage1.lock")
    if not lock.acquire():
        log("⛔ 같은 run_root 로 러너가 이미 잠금을 잡고 있다 — 시작하지 않는다"); logf.close(); return RC["refused"]
    old = {}
    if threading.current_thread() is threading.main_thread():
        def _raise_sig(signum, frame):
            raise _RunnerSignal(f"신호 {signal.Signals(signum).name}")
        for sg in (signal.SIGTERM, signal.SIGHUP):
            old[sg] = signal.signal(sg, _raise_sig)
    try:
        if not led_p.is_file():
            outs = sorted(str(x.relative_to(R)) for s_ in SYSTEMS for x in (R / s_).glob("seed*") if (R / s_).is_dir())
            if outs:                                         # ⭐ 회신 DH P0-1 — 비용을 모르는 산출물 위에 빈 장부를 만들지 않는다
                log(f"⛔ 산출물 {outs[:4]}{' …' if len(outs) > 4 else ''} 은 있는데 비용 장부 (stage1_ledger.json) 가 없다 — "
                    "빈 장부로 시작하지 않는다 (장부를 회수하거나 새 run_root)")
                return RC["refused"]
        state["ledger"] = (json.loads(led_p.read_text(encoding="utf-8")) if led_p.is_file() else {"runs": []})
        led = state["ledger"]
        led.setdefault("runs", []); led.setdefault("stop_history", [])
        led.update({"decision": DECISION, "driver_sha16": s16, "card": CARD_REL, "cap_h": cap_base,
                    "card_values_sha16": mq.values_sha16(vals)})
        # ①-1 STOP.json — 닫는 사건은 넘기지 않는다 · 나머지는 사람이 stop_id 로 확인해야 이어간다 (회신 DG P0-1)
        if os.path.lexists(stop_p):
            try:                                             # ⭐ DO 전 리뷰 P2-5 · P2-7 — 못 읽는 STOP 은 덮어쓰지 않고 거부 · stop_id 없는 STOP 을 조용히 넘기지 않는다
                sp = mq.loads_strict(stop_p.read_text(encoding="utf-8"))
                if not (isinstance(sp, dict) and isinstance(sp.get("stop_id"), str) and sp["stop_id"].strip()
                        and isinstance(sp.get("code"), str) and sp["code"].strip()):
                    raise ValueError("stop_id · code 가 글자가 아니다")
            except Exception as e:
                log(f"⛔ STOP.json 을 못 읽는다 ({type(e).__name__}: {str(e)[:80]}) — 원본을 덮어쓰지 않고 시작하지 않는다 (사람이 본다)")
                return RC["refused"]
            code = sp.get("code")
            if code in TERMINAL_STOPS:
                log(f"⛔ 이 run_root 는 닫혔다 ({code} · {sp.get('reason')}) — 재시작으로 다시 열지 않는다 (새 카드 · 새 run_root)")
                return RC.get(code, RC["refused"])
            if a.ack_stop != sp.get("stop_id"):
                log(f"⛔ 앞선 멈춤이 남아 있다 ({code} · {sp.get('reason')}) — 확인했으면 --ack_stop {sp.get('stop_id')}")
                return RC.get(code, RC["refused"])
            if code == "cap" and not (_is_num(sp.get("cap_h")) and cap_base > float(sp["cap_h"]) + 1e-9):
                log(f"⛔ 상한 멈춤은 카드 상한이 올라갔을 때만 넘긴다 (멈춤 {sp.get('cap_h')!r} · 지금 {cap_base:g} — 바꾸려면 결정 · 카드 개정 · "
                    "러너 고정값)")
                return RC["cap"]
            decl = declaration_from_args(a)                  # ⭐ 회신 DJ Q1 — 재시도 선언은 확인 때 붙이고 그 자리에서 검사한다
            if decl is not None:
                dprob = ack_declaration_problems(decl, sp, led, vals, mq, R)
                if dprob:
                    log(f"⛔ 재시도 선언을 받지 않는다 — {' · '.join(dprob)} (멈춤은 그대로 · 고쳐서 다시 확인)")
                    return RC["refused"]
            if not any(isinstance(h_, dict) and h_.get("stop_id") == sp["stop_id"] and h_.get("acked_at") for h_ in led["stop_history"]):
                led["stop_history"].append({**{k_: sp[k_] for k_ in STOP_KEYS if k_ in sp}, "acked_at": _now(),
                                            **({"declaration": decl} if decl else {})})
            save_ledger()                                    # ⭐ DO 전 리뷰 P2-15 — 확인 기록을 먼저 남기고 STOP 을 지운다
            stop_p.unlink()
            log(f"  앞선 멈춤 {code} (stop_id {sp.get('stop_id')}) 확인" + (f" · 재시도 선언 {decl['reason']} ({decl['event']})" if decl else "")
                + " — 장부 stop_history 로 옮기고 이어간다")
        elif declaration_from_args(a) is not None:           # 확인할 멈춤이 없는데 선언만 주면 조용히 버리지 않는다
            log("⛔ 재시도 선언은 --ack_stop 으로 확인할 멈춤 (STOP.json) 에 붙인다 — 지금 확인할 멈춤이 없다 (아무것도 안 했다)")
            return RC["refused"]
        # ①-2 장부의 도는 중 런 — 살아 있으면 거부 · 죽었으면 고아 런으로 마감 (비용 어림)
        for ent in led["runs"]:
            if ent.get("end") is None:
                pg = ent.get("pgid")
                rc_now, rc_st = recovery_clock(), ent.get("start_recovery_clock")
                rebooted = bool(isinstance(rc_now, dict) and isinstance(rc_st, dict) and rc_now.get("boot_id") and rc_st.get("boot_id")
                                and rc_now.get("boot_id") != rc_st.get("boot_id"))   # ⭐ DO 전 리뷰 P2-10 — 다른 부팅이면 그 그룹은 죽었다 (pgid 재사용)
                alive = False if rebooted else (pg_alive(pg) if pg is not None else None)
                if alive is not False:
                    log(f"⛔ 장부의 {ent['system']}{ent['seed']} 담금질 (프로세스 그룹 {pg}) 이 살아 있거나 종료 확인 불가다 — 시작하지 않는다")
                    return RC["refused"]
                lo = ent.get("wall_h_so_far")
                ent.setdefault("status_before_orphan", ent.get("status"))   # ⭐ DO 전 리뷰 P0-1 (b) — 고아 마감이 앞 상태 · rc 를 지우지 않는다
                ent.setdefault("rc_before_orphan", ent.get("rc"))
                hi = _orphan_upper_hours(ent, recovery_clock())
                if hi is not None:
                    ent.update(end=_now(), wall_h=hi, wall_h_lower=lo, rc="unknown_runner_died", status="orphaned",
                               cost_basis="upper_bound", wall_h_basis="동일 호스트·boot BOOTTIME 종료 확인 − 시작")
                    log(f"  고아 런 비용 상한 {hi:.2f} h (단조 시계 · 그룹 종료 확인)")
                else:
                    ent.update(end=_now(), wall_h=None, wall_h_lower=lo, rc="unknown_runner_died", status="orphaned", cost_basis="unknown")
                    log("  ⛔ 고아 런의 동일 부팅 시계 근거가 없다 — 비용 미확정 · 통과 불가")
                save_ledger()
        unk = [e for e in led["runs"] if e.get("cost_basis") == "unknown"]
        if unk:                                              # 정전 복구 개정 — 재부팅 고아 런은 사람이 근거를 보고 상한을 적어야 한다
            e0 = unk[0]
            return stop("resume", f"{e0['system']}{e0['seed']} 고아 런 비용이 미확정 (재부팅 · 같은 부팅 시계 근거 없음) — 근거를 보고 "
                                  f"--attest_cost {e0.get('run_id')} (근거 보기) → --attest_hours H --attest_event '…' --attest_time_reference '…' "
                                  "--attest_uncertainty_h U --attest_derivation '…' --attest_confirmer '…' 로 상한을 적은 뒤 다시 (하한 미상이면 증언을 안 받는다)",
                        sys=e0["system"], seed=e0["seed"], run_id=e0.get("run_id"))
        # ①-3 장부에 그 계를 닫은 사건이 있으면 거부 (STOP 을 지워도)
        closed = [f"{r['system']}{r['seed']}" for r in led["runs"] if r.get("closes_system")]
        if closed:
            return stop("melt", f"장부에 계를 닫은 사건이 있다 ({closed} · 첫 시드 녹음 미충족) — 재시작으로 다시 열지 않는다")
        # ①-4 판정 파일을 믿지 않는다 — 원자료로 다시 판정 → 묶음 판정 (회신 DG P1-4)
        for sysn, seed in order:
            rd = R / sysn / f"seed{seed}"
            if (rd / "stage1_verdict.json").is_file():
                now_ = mq.stage1_verdict(rd, values=vals, log=lambda *m: None, reason="러너 재시작 — 판정 파일을 믿지 않고 원자료로 다시 판정")
                hh = now_.get("history") or {}
                ch = hh.get("changed") or {}
                log(f"  {sysn}{seed}: 판정 다시 냄 {hh.get('prev_status')} → {now_.get('status')}"
                    + (f" · ⚠ 지문 바뀜 (파일 {ch.get('files')} · 카드 값 {ch.get('card_values')} · 도구 {ch.get('driver')})"
                       if (ch.get("files") or ch.get("card_values") or ch.get("driver")) else "")
                    + f" — 이전 판정은 {mq.VERDICT_HISTORY}")
        sm = mq.stage1_summary(R, values=vals, log=log)
        if sm["track"] == "stop_track":
            return stop("track", f"시작 전 묶음 판정 stop_track — {sm.get('why')}", summary=sm)
        if sm["track"] == "invalid":
            return stop("invalid", f"시작 전 묶음 판정 invalid (자료 · 기록 오류 — 과학적 종료 아님) — {sm.get('why')}", summary=sm)
        if sm["track"] == "cap_incomplete":
            return stop("cap", f"시작 전 묶음 판정 상한 · 미완결 — {sm.get('why')}", cap_h=cap_base, summary=sm)
        if sm["track"] == "stage1_pass":
            log(f"✅ 이미 1 단계 통과 — 2 단계 시드 {sm['stage2']['seeds']} · 기계 {sm['stage2']['machines']}")
            return RC["pass"]
        log(f"▶ 시작 · sha16 {s16} · 결정 {DECISION} active · 순서 {a.order} · 상한 {cap_base:g} h (카드) · 누적 {cost_so_far():.2f} h")
        for sysn, seed in order:
            rd = R / sysn / f"seed{seed}"
            vf = rd / "stage1_verdict.json"
            if vf.is_file():
                sv = json.loads(vf.read_text(encoding="utf-8")).get("status")
                if sv in ("pass", "fail"):
                    log(f"  {sysn}{seed}: 판정 {sv} — 건너뜀"); continue
                return stop("resume", f"{sysn}{seed} 판정이 {sv} — 끝나지 않은 런 폴더 (덮어쓰지 않는다 · 사람이 정한다)", sys=sysn, seed=seed,
                            run_id=_folder_run_id(rd))
            if rd.exists():
                return stop("resume", f"{sysn}{seed} 런 폴더가 판정 없이 있다 — 끊긴 런을 덮어쓰지 않는다 (사람이 정한다 · 다시 돌리려면 폴더를 같은 계 "
                                      f"폴더 안 옆으로 옮기고 이 STOP 을 확인)", sys=sysn, seed=seed, run_id=_folder_run_id(rd))
            attempts = [x for x in led["runs"] if (x.get("system"), x.get("seed")) == (sysn, seed)]
            retry_of, retry_stop, retry_kind = None, None, None
            if attempts:
                inv_, _ = mq.attempt_inventory(R)
                el_ = retry_eligibility(attempts, led["stop_history"], inv_, vals, mq)
                if not el_["ok"]:
                    return stop(el_["code"], f"{sysn}{seed}: {el_['why']}", sys=sysn, seed=seed, run_id=attempts[-1].get("run_id"))
                retry_of, retry_stop, retry_kind = el_["retry_of"], el_["stop_id"], el_["kind"]
                log(f"  {sysn}{seed}: 다시 돌린다 ({retry_kind} · 앞 런 {retry_of[:8]} · 단계 {el_['stage']} · 확인 STOP {retry_stop})")
            walls = [float(r["wall_h"]) for r in led["runs"] if r.get("wall_h") is not None and r.get("status") == "ended"]
            cum, worst = cost_so_far(), max(walls + [a.seed_worst_h])
            cap = cap_base
            if cum + worst > cap:
                return stop("cap", f"누적 {cum:.1f} h + 한 시드 최악 {worst:.1f} h > 상한 {cap:g} h — 미완결로 멈춤 (끝난 시드만 골라 판정하지 않는다)",
                            cum_h=cum, worst_h=worst, cap_h=cap)
            ok_n, t_wait = 0, clock()
            while ok_n < 2:
                u = gpu_used()
                ok_n = ok_n + 1 if u <= a.start_max_mib else 0
                if ok_n < 2:
                    if u > a.start_max_mib and (clock() - t_wait) % 1800 < a.gpu_poll_s:
                        log(f"  GPU {u} MiB > {a.start_max_mib} — 비기를 기다린다")
                    sleep(a.gpu_poll_s)
            rid = uuid.uuid4().hex                           # ⭐ 회신 DH P0-2 — 실행 식별자 (plan.json · 장부 · 판정을 묶는다)
            cmd = build_cmd(a.python, W, R, sysn, seed, vals, mq, run_id=rid)
            t0 = clock()
            log(f"▶ {sysn}{seed} 담금질 — " + " ".join(cmd[2:]))
            rd.mkdir(parents=True, exist_ok=False)
            _write_json_atomic(rd / mq.ATTEMPT_NAME, {"system": sysn, "seed": seed, "run_id": rid,
                                                     "retry_of": retry_of, "retry_stop_id": retry_stop, "retry_kind": retry_kind})
            ent = {"system": sysn, "seed": seed, "run_id": rid, "start": _now(), "start_epoch": wall(), "pgid": None,
                   "start_recovery_clock": recovery_clock(), "retry_of": retry_of, "retry_stop_id": retry_stop, "retry_kind": retry_kind,
                   "status": "starting", "end": None, "wall_h": None, "wall_h_so_far": 0.0, "cum_before_h": cum}
            led["runs"].append(ent); state["entry"], state["t0"] = ent, t0
            save_ledger()
            hold_sig = hasattr(signal, "pthread_sigmask") and threading.current_thread() is threading.main_thread()
            old_mask = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGTERM, signal.SIGHUP, signal.SIGINT}) if hold_sig else None
            try:                                             # ⭐ DO 전 리뷰 P2-9 — 신호는 손잡이를 적은 뒤에 받는다 (띄운 자식을 놓치지 않게)
                h = launch(cmd, R / f"quench_{sysn}{seed}.log")
                state["h"] = h
                ent.update(pgid=getattr(h, "pid", None), status="running")
                save_ledger()                                # ⭐ 띄운 직후 — 러너가 죽어도 시작 사실이 남는다 (회신 DG P0-2)
            finally:
                if hold_sig:
                    signal.pthread_sigmask(signal.SIG_SETMASK, old_mask)
            need_melt = (seed == vals["first_seed"])
            while h.poll() is None:
                left_s = (cap - cum) * 3600.0 - (clock() - t0)  # ⭐ DO 전 리뷰 P2-11 — 상한 검사를 상한보다 늦게 하지 않는다
                sleep(max(1.0, min(a.poll_s, left_s)))
                el = (clock() - t0) / 3600.0
                ent["wall_h_so_far"], ent["last_seen"] = el, _now()
                save_ledger()
                if cum + el >= cap:                          # ⭐ 실행 중 상한 (회신 DG P0-3)
                    cl = stop_child(f"상한 도달 (누적 {cum:.1f} + 경과 {el:.1f} ≥ {cap:g} h)")
                    if not finish(ent, "killed_cap", "cap", (clock() - t0) / 3600.0, cleanup=cl):
                        return stop("abnormal", f"{sysn}{seed} 상한으로 멈추려 했는데 그룹이 남았다 (pid {cl.get('left')}) — 손으로 정리",
                                    sys=sysn, seed=seed, cleanup=cl, run_id=rid)
                    try:
                        mq.stage1_verdict(rd, values=vals, log=log, reason="상한 멈춤 (기록용 · 미완)")
                    except Exception as e:
                        log(f"  (기록용 판정 실패 {type(e).__name__}: {e})")
                    return stop("cap", f"{sysn}{seed} 실행 중 누적 {cum + el:.1f} h ≥ 상한 {cap:g} h — 그 담금질을 멈추고 미완결",
                                sys=sysn, seed=seed, cum_h=cum + el, cap_h=cap, run_id=rid)
                if need_melt:
                    try:
                        mw = mq.melt_window_check(rd, values=vals, log=lambda *m: None)
                    except Exception as e:                   # 판독 예외로 러너가 죽지 않는다 — 기록하고 다음 poll 에 다시
                        ent.setdefault("melt_check_errors", []).append(f"{_now()} {type(e).__name__}: {e}")
                        save_ledger()
                        log(f"  ⚠ {sysn}{seed}: 녹음 판정 예외 ({type(e).__name__}: {e}) — 다음 poll 에 다시 (끝난 뒤 판정에서도 본다)")
                        continue
                    if mw["verdict"] in ("fail", "invalid"):
                        # ⭐ DO 전 리뷰 P0-1 — 녹음 판정을 담금질을 멈추기 **전에** 장부에 적는다: 정리 실패 · 판정 도중 중단 · 재부팅 ·
                        #   고아 마감에도 남는다 (fail = 그 계를 닫는다 · invalid = 실행 종류 invalid)
                        ent["melt_check"] = {"verdict": mw["verdict"], "message": str(mw.get("message"))[:300], "at": _now()}
                        if mw["verdict"] == "fail":
                            ent["closes_system"] = True
                            ent["closes_basis"] = "first_seed_melt_window_check"
                        save_ledger()
                        cl = stop_child(f"{sysn}{seed} 첫 시드 녹음 판정 {mw['verdict']}")
                        if not finish(ent, "killed_melt", mw["verdict"], (clock() - t0) / 3600.0, cleanup=cl):
                            if mw["verdict"] == "fail":
                                return stop("melt", f"{sysn}{seed} (계의 첫 시드) 녹음 판정 fail — {mw.get('message')} · 그 계가 닫혀 트랙 전체 멈춤 "
                                                    f"(장부에 먼저 적었다) · ⚠ 담금질 그룹이 남았다 (pid {cl.get('left')}) — 손으로 정리",
                                            sys=sysn, seed=seed, cleanup=cl, run_id=rid)
                            return stop("abnormal", f"{sysn}{seed} 를 녹음 판정 invalid 로 멈추려 했는데 그룹이 남았다 (pid {cl.get('left')}) — "
                                                    "손으로 정리 (장부 melt_check = invalid)", sys=sysn, seed=seed, cleanup=cl, run_id=rid)
                        v = mq.stage1_verdict(rd, values=vals, log=log, reason=f"첫 시드 녹음 판정 {mw['verdict']} — 러너가 멈춤")
                        ent["verdict"] = v.get("status")
                        if mw["verdict"] == "fail" and not v.get("closes_system"):
                            ent["verdict_disagrees"] = f"녹음 판정 fail 인데 시드 판정 {v.get('status')} · closes_system {v.get('closes_system')}"
                            log(f"  ⚠ {sysn}{seed}: {ent['verdict_disagrees']} — 장부의 닫힘 (녹음 판정) 을 그대로 둔다 (사람이 본다)")
                        save_ledger()
                        if mw["verdict"] == "fail":                  # 과학적 종료 — 첫 시드 녹음 판정 (카드 S1 ②)
                            return stop("melt", f"{sysn}{seed} (계의 첫 시드) 녹음 판정 fail — {mw.get('message')} · "
                                                "그 계가 닫혀 트랙 전체 멈춤", sys=sysn, seed=seed, verdict=v.get("status"), run_id=rid)
                        return stop("invalid", f"{sysn}{seed} (계의 첫 시드) 녹음 판정 {mw['verdict']} · 시드 판정 {v.get('status')} — "
                                               "자료 · 판독 오류로 멈춘 것이지 그 계가 기준을 못 넘었다는 증거가 아니다 (closes_system 아님)",
                                    sys=sysn, seed=seed, run_id=rid, verdict=v.get("status"), melt=mw.get("message"))
                    if mw["verdict"] == "pass":
                        need_melt = False
                        log(f"  {sysn}{seed}: 녹음 판정 통과 (D_P {mw.get('D_framework_cm2_s')}) — 담금질 계속")
            rc = h.returncode
            cl = stop_child("담금질 대표가 끝났다 — 그룹에 남은 프로세스까지 정리")
            el = (clock() - t0) / 3600.0
            if not finish(ent, rc, "ended", el, cleanup=cl):
                return stop("abnormal", f"{sysn}{seed} 대표는 rc {rc} 로 끝났는데 그룹이 남았다 (pid {cl.get('left')}) — 손으로 정리",
                            sys=sysn, seed=seed, rc=rc, cleanup=cl, run_id=rid)
            if rc != 0:
                return stop("abnormal", f"{sysn}{seed} 담금질 rc {rc} — 비정상 종료 (사용자 결정 · 그 계를 어떻게 할지)", sys=sysn, seed=seed, rc=rc,
                            run_id=rid)
            v = mq.stage1_verdict(rd, values=vals, log=log, reason="담금질 끝")
            ent["verdict"], ent["closes_system"] = v.get("status"), bool(v.get("closes_system"))
            save_ledger()
            if cum + el > cap:                               # 끝난 뒤에도 넘었으면 통과로 올리지 않는다 (회신 DG P0-3)
                return stop("cap", f"{sysn}{seed} 가 끝났을 때 누적 {cum + el:.1f} h > 상한 {cap:g} h — 미완결 (통과로 올리지 않는다)",
                            sys=sysn, seed=seed, cum_h=cum + el, cap_h=cap, run_id=rid)
            sm = mq.stage1_summary(R, values=vals, log=log)
            if sm["track"] == "stop_track":
                return stop("track", f"묶음 판정 stop_track — {sm.get('why')}", summary=sm)
            if sm["track"] == "invalid":
                return stop("invalid", f"묶음 판정 invalid (자료 · 기록 오류 — 과학적 종료 아님) — {sm.get('why')}", summary=sm, run_id=rid, sys=sysn, seed=seed)
            if sm["track"] == "cap_incomplete":
                return stop("cap", f"묶음 판정 상한 · 미완결 — {sm.get('why')}", cap_h=cap_base, summary=sm)
        sm = mq.stage1_summary(R, values=vals, log=log)
        if sm["track"] == "stage1_pass":
            log(f"✅ 1 단계 통과 — 2 단계 시드 {sm['stage2']['seeds']} · 기계 {sm['stage2']['machines']}")
            return RC["pass"]
        if sm["track"] == "stop_track":
            return stop("track", f"묶음 판정 stop_track — {sm.get('why')}", summary=sm)
        if sm["track"] == "invalid":
            return stop("invalid", f"묶음 판정 invalid (자료 · 기록 오류 — 과학적 종료 아님) — {sm.get('why')}", summary=sm)
        if sm["track"] == "cap_incomplete":
            return stop("cap", f"묶음 판정 상한 · 미완결 — {sm.get('why')}", cap_h=cap_base, summary=sm)
        return stop("pending", f"순서를 다 돌았는데 묶음 판정이 {sm['track']} — 판정 파일을 확인한다", summary=sm)
    except BaseException as e:                               # 예외 · Ctrl-C · SIGTERM · SIGHUP (회신 DG P0-2)
        why = f"{type(e).__name__}: {e}"
        cl = {"group_empty": False, "left": "?", "error": "정리 시도 전"}
        try:
            cl = stop_child(f"러너 중단 ({why})") or {"group_empty": True, "left": []}
        except BaseException as e2:
            cl = {"group_empty": False, "left": "?", "error": f"{type(e2).__name__}: {e2}"}
            log(f"  ⛔ 담금질 멈춤도 실패 ({type(e2).__name__}: {e2}) — 프로세스 그룹 {getattr(state['h'], 'pid', '?')} 를 손으로 본다")
        ent = state["entry"]
        ent_rid = ent.get("run_id") if ent is not None else None
        if ent is not None and ent.get("end") is None:
            finish(ent, "killed_runner_exit", "interrupted", (clock() - state["t0"]) / 3600.0, cleanup=cl)
        log("  " + traceback.format_exc().strip().replace("\n", "\n  "))
        if not state["stopped"]:
            stop("interrupted", f"러너 중단 — {why} · " + ("돌던 담금질 그룹을 비웠다" if cl.get("group_empty")
                                                         else f"⛔ 담금질 그룹이 남았을 수 있다 (pid {cl.get('left')}) — 손으로 본다")
                 + " · 그 시드 폴더는 사람이 정한다", cleanup=cl, run_id=ent_rid)
        return RC["interrupted"]
    finally:
        try:
            stop_child("러너가 끝난다")
        finally:
            try:
                save_ledger()
            finally:
                for sg, hd in old.items():
                    signal.signal(sg, hd)
                lock.release()
                logf.close()


# ───────────────────────── selftest ─────────────────────────
def _selftest():
    """가짜 담금질 (진짜 드라이버가 쓰는 파일을 poll 마다 조금씩 쓴다) + **진짜** 판독 함수 (melt_window_check · stage1_verdict ·
    stage1_summary · 카드 검사) — 회신 DG ④: 판독기를 가짜로 바꾸면 판독 예외 · 산출물 검증 누락을 못 본다."""
    import numpy as np
    ok = bad = 0
    failfast = os.environ.get("LI2S2_SELFTEST_FAILFAST") == "1"   # 변이 실행용 — 첫 빨강에서 멈춘다 (빨강 · 초록 판정은 같다 · 시간만 준다)
    def chk(c, m):
        nonlocal ok, bad
        print(("  ⭕ " if c else "  ⛔ ") + m); ok += bool(c); bad += (not c)
        if failfast and not c:                               # SystemExit — finally · atexit (임시 폴더 지우기) 는 그대로 돈다
            print(f"li2s2_stage1_runner selftest: ⭕ {ok} · ⛔ {bad} (첫 빨강에서 멈춤 · LI2S2_SELFTEST_FAILFAST=1)", flush=True)
            raise SystemExit(1)
    repo = pathlib.Path(__file__).resolve().parents[2]
    real = load_mq(repo)
    tmp_root = pathlib.Path(tempfile.mkdtemp(prefix="li2s2_runner_st_"))
    import atexit                                            # 시험이 예외로 죽어도 임시 폴더 (≈ 450 MB) 를 지운다 — 2026-11-04 변이 실행이 105 개를 남겨 디스크를 채웠다
    atexit.register(shutil.rmtree, str(tmp_root), True)
    # 시험 카드 = 진짜 카드에서 일정만 줄이고 (담금질 9 ps · 유지 20 ps) 밀도를 무작위 PS₄ 셀의 밀도로 — 그 외 값은 진짜 그대로
    card0 = json.loads((repo / CARD_REL).read_text(encoding="utf-8"))
    BASE, rho = {}, {}
    for s in SYSTEMS:
        n_fu = card0["기계_판독_값"]["composition"][s]["P"]
        sym, pos, cell = real.build_random_cell(s, seed=3, density_g_cm3=1.2, n_fu=n_fu)
        from ase import Atoms
        at = Atoms(symbols=sym, positions=pos, cell=cell, pbc=True)
        BASE[s] = (list(sym), np.asarray(pos, float), np.asarray(cell, float))
        rho[s] = real.density_g_cm3(at)
        gv = real._gate_view(at)
        chk(gv["PS4_fraction"] == 1.0 and gv["min_pair_excl_PS_A"] > 2.0, f"시험 바탕 구조 {s}: 시드 게이트 통과 ({gv['min_pair_excl_PS_A']:.3f} Å)")
    def mk_card(**over):
        c = json.loads(json.dumps(card0))
        mv = c["기계_판독_값"]
        mv["schedule"].update({"quench_rate_K_s": 1e14, "hold_ps": 20.0})
        mv["fix_density_g_cm3"] = dict(rho)
        for k, x in over.items():
            mv[k] = x
        return c
    SW = {"model": "uma-s-1p1", "task": "omat", "inference": "turbo", "fairchem-core": "2.21.0", "torch": "2.8.0", "ase": "3.26.0"}

    def _xyz(path, sym, frames, cell, mode="a"):
        lat = " ".join(f"{x:.10f}" for x in np.asarray(cell).ravel())
        with open(path, mode) as f:
            for P in frames:
                f.write(f"{len(sym)}\nLattice=\"{lat}\" Properties=species:S:1:pos:R:3 pbc=\"T T T\"\n")
                f.writelines(f"{e} {x:.8f} {y:.8f} {z:.8f}\n" for e, (x, y, z) in zip(sym, P))

    class FakeQuench:
        """진짜 드라이버가 쓰는 파일 (plan.json · thermo.csv · traj.xyz · final.xyz · result.json) 을 poll 마다 조금씩 쓴다.
        poll 1: 폴더만 (plan 없음) · 2: plan + 70 ps · 3: 100 ps (녹음 창 확보) · n_polls: 끝까지 + final · 그 다음 poll 이 rc."""
        def __init__(self, cmd, log_path, scen=None, launched=None):
            g = lambda k: cmd[cmd.index(k) + 1]
            self.cmd, self.sys, self.seed = cmd, g("--system"), int(g("--seed"))
            self.rid = g("--run_id") if "--run_id" in cmd else None
            self.rd = pathlib.Path(g("--out_root")) / self.sys / f"seed{self.seed}"
            self.rd.mkdir(parents=True, exist_ok=True)
            self.f = {k: float(g("--" + k)) for k in ("fix_density", "compress_ps", "melt_ps", "hold_ps", "quench_rate",
                                                       "T_melt", "T_final", "save_ps", "dt_fs")}
            sc = (scen or {}).get((self.sys, self.seed), {})
            self.melt, self.final, self._rc = sc.get("melt", "pass"), sc.get("final", "ok"), sc.get("rc", 0)
            self.n_polls, self.raise_on = max(4, sc.get("polls", 5)), sc.get("raise_on_poll")
            self.group_stuck = sc.get("group_stuck", False)
            self.torn = sc.get("torn_tail", False)            # 죽일 때 traj 마지막 프레임이 반쪽 (쓰기 도중 SIGTERM — DO 전 리뷰 t9)
            self.k, self.stopped, self.killed, self.pid, self.t_written = 0, False, False, 990000 + len(launched or []), -1
            self.sym, self.base, self.cell = BASE[self.sys]
            rng = np.random.default_rng(1000 * self.seed + ord(self.sys))
            step = 0.5 if self.melt == "pass" else 0.0005
            self.walk = np.cumsum(rng.normal(0, step, (51, len(self.sym), 3)), axis=0)
            self.walk -= self.walk[0]
            self.isP = np.array([e == "P" for e in self.sym])
            if launched is not None:
                launched.append(self)
        @property
        def quench_ps(self):
            return (self.f["T_melt"] - self.f["T_final"]) / self.f["quench_rate"] * 1e12
        def _pos(self, t):
            if 50 <= t <= 100:
                P = self.base.copy(); P[self.isP] += self.walk[int(round(t - 50))][self.isP]; return P
            return self.base + (0.002 if t > 100 else 0.0)
        def _write(self, t_end, final=False):
            if self.t_written < 0:
                plan = real.build_plan(self.sys, self.seed, self.sym, 1.0, self.f["T_melt"], self.f["T_final"], self.f["melt_ps"],
                                       self.f["quench_rate"], self.quench_ps, self.f["hold_ps"], self.f["dt_fs"], self.f["save_ps"],
                                       fix_density=self.f["fix_density"], compress_ps=self.f["compress_ps"])
                plan["uma_inference_mode"] = "turbo"; plan["software"] = dict(SW); plan["run_id"] = self.rid
                (self.rd / "plan.json").write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
                (self.rd / "thermo.csv").write_text("t_ps,T_K,T_set_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n", encoding="utf-8")
            ts = [t for t in range(int(self.t_written) + 1, int(round(t_end)) + 1)]
            ts_th = list(ts)                                 # thermo 는 기록마다 한 행 (0 번 포함 — 진짜 드라이버처럼 · 회신 DL 판독이 잡았다)
            if self.melt == "species_swap" and ts and ts[0] == 0:      # 0 번 프레임만 P · S 자리를 바꿈 (회신 DG P1-7 반례)
                sw_ = list(self.sym); iP, iS = sw_.index("P"), sw_.index("S"); sw_[iP], sw_[iS] = "S", "P"
                _xyz(self.rd / "traj.xyz", sw_, [self._pos(0)], self.cell); ts = ts[1:]
            _xyz(self.rd / "traj.xyz", self.sym, [self._pos(t) for t in ts], self.cell)
            M, Q = self.f["melt_ps"], self.quench_ps
            with open(self.rd / "thermo.csv", "a") as fh:
                for t in ts_th:
                    Ts = self.f["T_melt"] if t <= M else (self.f["T_final"] if t >= M + Q else
                                                         self.f["T_melt"] - (self.f["T_melt"] - self.f["T_final"]) * (t - M) / Q)
                    d = self.f["fix_density"] if t >= self.f["compress_ps"] else 1.0 + (self.f["fix_density"] - 1.0) * t / self.f["compress_ps"]
                    fh.write(f"{t:.3f},{Ts + 3:.1f},{Ts:.1f},{d:.4f},{1000.0:.2f},{-500.0:.4f},{3.6:.4f},{3.5:.4f}\n")
            self.t_written = ts_th[-1] if ts_th else self.t_written
            if final:                                        # 진짜 드라이버처럼 MD 완료 기록 (FIRE 전) — 진짜 쓰기 함수로
                n_pl = real.planned_md_steps(json.loads((self.rd / "plan.json").read_text(encoding="utf-8")))
                real.write_md_done(self.rd, run_id=self.rid, n_steps_planned=n_pl, n_steps_done=n_pl)
                fc = self.cell.copy(); fp = self.base.copy(); fs = list(self.sym)
                if self.final == "five":
                    iP = fs.index("P"); D = np.linalg.norm(self.base - self.base[iP], axis=1)
                    idx = [iP] + [i for i in np.argsort(D) if fs[i] == "S"][:4]
                    fp, fs = self.base[idx], [fs[i] for i in idx]
                elif self.final == "dense":
                    fc = self.cell * 0.98; fp = self.base * 0.98
                elif self.final == "ps4_broken":
                    iP = fs.index("P"); D = np.linalg.norm(self.base - self.base[iP], axis=1)
                    iS = [i for i in np.argsort(D) if fs[i] == "S"][0]
                    u = (self.base[iS] - self.base[iP]); fp = self.base.copy(); fp[iS] = self.base[iP] + u / np.linalg.norm(u) * 2.95
                _xyz(self.rd / "final.xyz", fs, [fp], fc, mode="w")
                (self.rd / "result.json").write_text(json.dumps({"files": ["traj.xyz", "thermo.csv", "final.xyz"]}), encoding="utf-8")
        def poll(self):
            if self.stopped:
                return -15
            self.k += 1
            if self.k == 1:                                   # 띄운 직후 — 장부에 시작이 이미 디스크에 있나 (회신 DG P0-2)
                lp = self.rd.parent.parent / "stage1_ledger.json"
                led_ = json.loads(lp.read_text(encoding="utf-8")) if lp.is_file() else {"runs": []}
                self.ledger_at_first_poll = any(r.get("system") == self.sys and r.get("seed") == self.seed and r.get("end") is None
                                                for r in led_.get("runs", []))
            if self.raise_on == self.k:
                raise KeyboardInterrupt("시험: poll 중 Ctrl-C")
            if self.k == 2:
                self._write(70.0)
            elif self.k == 3:
                self._write(100.0)
            elif self.k == self.n_polls:
                self._write(self.f["melt_ps"] + self.quench_ps + self.f["hold_ps"], final=True)
            return None if self.k <= self.n_polls else self._rc
        def stop(self, grace_s=60):
            if self.k <= self.n_polls and not self.stopped:
                self.killed = True                            # 도는 중에 죽임 (끝난 뒤 그룹 정리와 가른다)
                if self.torn and (self.rd / "traj.xyz").is_file():
                    with open(self.rd / "traj.xyz", "a", encoding="utf-8") as fh_:
                        fh_.write(f"{len(self.sym)}\nLattice=\"5 0")
            self.stopped = True
            return {"leader_rc": -15 if self.k <= self.n_polls else self._rc, "group_empty": not self.group_stuck,
                    "signals": ["TERM"], "left": [self.pid + 1] if self.group_stuck else []}
        @property
        def returncode(self):
            return -15 if (self.stopped and self.k <= self.n_polls) else self._rc

    def mk_wt(state="active", card=None, driver_txt="# fake driver\n"):
        td = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
        (td / "db/governance").mkdir(parents=True); (td / "db/properties").mkdir(parents=True); (td / "tools/ionic").mkdir(parents=True)
        (td / "db/governance/decisions.json").write_text(json.dumps({"decisions": [{"id": DECISION, "decision_state": state}]}), encoding="utf-8")
        (td / CARD_REL).write_text(json.dumps(card or mk_card(), ensure_ascii=False), encoding="utf-8")
        (td / DRIVER_REL).write_text(driver_txt, encoding="utf-8")
        return td

    def go(wt, scen=None, poll_s=3600.0, order=DEFAULT_ORDER, expect=None, rr=None, ack=None, mq=None,
           gpu=None, sleep_hook=None, pg_alive=None, seed_worst_h=21.0, cleanup_s=0.0, default_clock=False, boot="fixture", declare=None,
           expect_values=None, python_ok=None, launch_signal=False):
        launched, clock, sig_sent = [], [0.0], [False]
        def launch(cmd, lp):
            h = FakeQuench(cmd, lp, scen=scen, launched=launched)
            if launch_signal and not sig_sent[0]:            # 띄운 직후 · 손잡이를 적기 전에 SIGTERM (DO 전 리뷰 P2-9)
                sig_sent[0] = True
                os.kill(os.getpid(), signal.SIGTERM)
            original_stop = h.stop
            def cleanup(*args, **kwargs):
                clock[0] += cleanup_s
                return original_stop(*args, **kwargs)
            h.stop = cleanup
            return h
        gq = list(gpu or [])
        def gpu_used():
            x = gq.pop(0) if gq else 100
            if isinstance(x, BaseException):
                raise x
            return x
        def sleep(s):
            clock[0] += s
            if sleep_hook:
                sleep_hook(clock[0])
        rr = rr or pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
        a = argparse.Namespace(worktree=str(wt), run_root=str(rr), python="python3", seed_worst_h=seed_worst_h,
                               poll_s=poll_s, gpu_poll_s=60.0, start_max_mib=2000, order=order, ack_stop=ack, expect_values_sha16=expect_values,
                               expect_sha=expect or sha16(pathlib.Path(wt) / DRIVER_REL),
                               **{k: (declare or {}).get(k) for k in ("retry_reason", "retry_event", "retry_evidence", "declared_by",
                                                                      "rejudge_impossible_reason")})
        deps = {"mq": mq or real, "launch": launch, "gpu_used": gpu_used, "sleep": sleep, **({"python_ok": python_ok} if python_ok else {}),
                "pg_alive": pg_alive or (lambda pg: False),
                "recovery_clock": lambda: {"host": "fixture", "boot_id": boot, "kind": "CLOCK_BOOTTIME", "seconds": 7200.0}}
        if not default_clock:
            deps["clock"] = lambda: clock[0]
            rc = run(a, deps)
        else:
            # Production clock default is exercised: wall time is corrected backwards during A11.
            import types
            saved_time = globals()["time"]
            proxy = types.SimpleNamespace(**{k: getattr(saved_time, k) for k in dir(saved_time)})
            proxy.monotonic = lambda: clock[0]
            proxy.time = lambda: clock[0] - (14400.0 if clock[0] >= 14400.0 else 0.0)
            globals()["time"] = proxy
            try:
                rc = run(a, deps)
            finally:
                globals()["time"] = saved_time
        return rc, launched, rr
    J = lambda p: json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    tag = lambda L: [(p.sys, p.seed) for p in L]
    #: 회신 DJ Q1 — 재시도 영수증에 붙이는 선언 (결과와 무관한 사건) · Q3 — 증언 근거 필드
    OUT = {"retry_reason": "power_outage", "retry_event": "kgy 정전 (selftest)", "retry_evidence": "UPS 로그 (selftest)", "declared_by": "selftest"}
    FIX = {"retry_reason": "invalid_cause_fixed", "retry_event": "판독 결함 고침 (selftest)", "retry_evidence": "커밋 (selftest)", "declared_by": "selftest"}
    ATT = {"event": "kgy 정전 (selftest)", "time_reference": "UPS 로그 시각 (selftest)", "uncertainty_h": 0.1,
           "derivation": "정전 시각 − 시작 + 불확실성 (selftest)", "confirmer": "selftest"}
    DECL = lambda d: {"reason": d["retry_reason"], "event": d["retry_event"], "evidence": d["retry_evidence"], "declared_by": d["declared_by"],
                      "declared_at": "2026-11-03 00:00:00", **({"rejudge_impossible_reason": d["rejudge_impossible_reason"]}
                                                             if d.get("rejudge_impossible_reason") else {})}

    FULL_STAGES = ("md_complete", "final", "md_complete_noplan", "md_tmp", "end_no_marker")   # 궤적 · thermo 를 끝까지 남기는 단계
    NOPLAN_STAGES = ("no_plan", "noplan_hist_pass", "noplan_vtmp_pass", "noplan_judged")       # plan 을 안 남기는 단계 (회신 DM P0-2 포함)
    PASSV = {"status": "pass", "reasons": {}, "provenance": {"files_sha256": {"plan.json": "a" * 64, "thermo.csv": "b" * 64,
                                                                              "traj.xyz": "c" * 64, "final.xyz": "d" * 64, "result.json": "e" * 64}}}
    md_judged = []                                           # 진짜 판정 함수가 'MD 완료 · FIRE 미완' 폴더에 낸 판정의 꼴 (fixture 뜻 확인)
    def _note_md_judge(v_, kind="full"):                     # full: thermo 까지 완주 · frames: thermo 없음 (완료 흔적은 프레임뿐 — 회신 DN P1 재현)
        tf_ = (v_.get("checks") or {}).get("traj_frames") or {}
        md_judged.append((kind, v_.get("status"), bool((v_.get("gate_check") or {}).get("schedule_complete")),
                          tf_.get("n") is not None and tf_.get("n") == tf_.get("expected")))
    def _n_to_str(d):                                        # 회신 DN P1 — 판정 기록의 프레임 수 n 만 글자로 (타입 오류 주입)
        vv_ = J(d / "stage1_verdict.json"); tf_ = vv_["checks"]["traj_frames"]; tf_["n"] = str(tf_["n"])
        (d / "stage1_verdict.json").write_text(json.dumps(vv_, ensure_ascii=False), encoding="utf-8")
    def _judge_as_seed(d, reason):                           # 러너는 보존 (이름 바꿈) 전에 seed<번호> 폴더에서 판정한다 — 그 이름 아래에서 진짜 판정
        pl_j = J(d / "plan.json")
        jroot = d.parent.parent / f"_judge_{uuid.uuid4().hex[:8]}"
        jdir = jroot / pl_j["system"] / f"seed{pl_j['seed']}"
        jdir.parent.mkdir(parents=True); d.rename(jdir)
        try:
            return real.stage1_verdict(jdir, values=vals_t, log=lambda *m: None, reason=reason)
        finally:
            jdir.rename(d); shutil.rmtree(jroot)
    def dm_stage(d, st_, th_full=None, src_full=None):
        """회신 DM 반례 · 대조를 폴더 d 에 만든다 — end_row_kept: thermo 에 앞 행 + 끝 시각 행만 · noplan_*: 진짜 판정 함수로 판정 기록 ·
        judged_md_then_cut: MD 완료 · FIRE 미완 폴더를 진짜 판정 (incomplete · 일정 끝 · 프레임 다 참) 한 뒤 완료 기록 · 원자료 꼬리 소실."""
        if st_ in ("judged_md_then_cut", "judged_frames_strn"):   # 같은 갈래 (DN 전) · 회신 DN P1 — 판정 기록의 'MD 가 끝났다' 흔적
            cut_tr, cut_th = (d / "traj.xyz").read_bytes(), (d / "thermo.csv").read_bytes()
            shutil.copy(src_full / "traj.xyz", d / "traj.xyz"); shutil.copy(src_full / "thermo.csv", d / "thermo.csv")
            pl_j = J(d / "plan.json"); n_pl = real.planned_md_steps(pl_j)
            real.write_md_done(d, run_id=pl_j["run_id"], n_steps_planned=n_pl, n_steps_done=n_pl)
            if st_ == "judged_frames_strn":                  # thermo 없음 · 궤적 완주 · FIRE 미완 (Codex DN 재현) — 흔적은 프레임 수뿐
                (d / "thermo.csv").unlink()
            _note_md_judge(_judge_as_seed(d, "selftest — MD 완료 · FIRE 미완 판정"), kind="full" if st_ == "judged_md_then_cut" else "frames")
            (d / real.MD_DONE_NAME).unlink(); (d / "traj.xyz").write_bytes(cut_tr)
            if st_ == "judged_md_then_cut":
                (d / "thermo.csv").write_bytes(cut_th)
            else:
                _n_to_str(d)                                 # 완료 기록 · 궤적 꼬리 소실 뒤 n:"130" (회신 DN P1)
        if st_ == "end_row_kept":                           # P0-1 — 궤적은 앞부분 · thermo 는 앞 행 + 온전한 끝 행
            th_ = (d / "thermo.csv").read_text(encoding="utf-8").splitlines(keepends=True)
            (d / "thermo.csv").write_text("".join(th_) + th_full[-1], encoding="utf-8")
        elif st_ == "noplan_hist_pass":                     # P0-2 반례 1 — pass 판정이 있던 폴더에서 원자료 소실 뒤 진짜 재판정
            (d / "stage1_verdict.json").write_text(json.dumps(PASSV), encoding="utf-8")
            real.stage1_verdict(d, values=vals_t, log=lambda *m: None, reason="selftest — 원자료 소실 뒤 재판정")
        elif st_ == "noplan_vtmp_pass":                     # P0-2 반례 2 — pass 판정이 임시 파일에만
            (d / "stage1_verdict.json.tmp").write_text(json.dumps(PASSV), encoding="utf-8")
        elif st_ == "noplan_judged":                        # 대조 — plan 전 끊긴 런을 두 번 판정 (진짜 · 이력도 plan 전 것)
            for _ in range(2):
                real.stage1_verdict(d, values=vals_t, log=lambda *m: None, reason="selftest — plan 전 끊김 판정")
    def with_history(rr_, sysn, seed, prevs):
        """rr_ 의 (계, 시드) 공식 런 앞에 이전 실행들을 **모든 면에서 맞게** 끼운다 — 보존 폴더 (같은 계 폴더 안) · 실행 전 기록 · 장부 행 ·
        재시도 필드 (retry_of = 바로 앞 · retry_kind = 앞 종류 · retry_stop_id) · 앞 실행에 묶여 확인된 STOP + 선언. 음성 시험은 여기서
        **한 가지만** 깨서 그 한 가지를 잡는지 본다 (양성 대조: 그대로면 통과). prevs (시간 순): {"kind", "stage", "status", "rc",
        "wall_h", "decl" (OUT · FIX · None), "code"}. 반환: 끼운 run_id 목록."""
        led_ = J(rr_ / "stage1_ledger.json")
        canon = rr_ / sysn / f"seed{seed}"
        ic = next(i for i, x in enumerate(led_["runs"]) if (x["system"], x["seed"]) == (sysn, seed))
        lines = (canon / "traj.xyz").read_text(encoding="utf-8").splitlines(keepends=True)
        fr = int(lines[0]) + 2
        n_fr = len(lines) // fr
        chain = []
        for k, pv in enumerate(prevs):
            rid_ = uuid.uuid4().hex
            d = rr_ / sysn / f"seed{seed}.prev{k}"
            d.mkdir()
            st_ = pv.get("stage", "md_incomplete")
            if st_ not in NOPLAN_STAGES:
                shutil.copy(canon / "plan.json", d / "plan.json")
                pl_ = J(d / "plan.json"); pl_["run_id"] = rid_; (d / "plan.json").write_text(json.dumps(pl_, ensure_ascii=False), encoding="utf-8")
                keep = n_fr if st_ in FULL_STAGES else max(1, n_fr // 3)
                (d / "traj.xyz").write_text("".join(lines[:keep * fr]), encoding="utf-8")
                th_ = (canon / "thermo.csv").read_text(encoding="utf-8").splitlines(keepends=True)
                (d / "thermo.csv").write_text("".join(th_[:1 + keep]), encoding="utf-8")   # traj 와 같은 행 수 (회신 DL — 끝 경계 판독)
                if st_ in ("md_complete", "final", "md_complete_noplan", "md_tmp"):   # 진짜 쓰기 함수로 MD 완료 기록 (회신 DK)
                    n_pl = real.planned_md_steps(pl_)
                    real.write_md_done(d, run_id=rid_, n_steps_planned=n_pl, n_steps_done=n_pl)
                if st_ == "md_tmp":                              # 회신 DL P0 반례 2 — os.replace 직전 끊김 (임시 기록만)
                    (d / real.MD_DONE_NAME).rename(d / real.MD_DONE_TMP)
                if st_ == "md_complete_noplan":                  # 회신 DL P0 반례 1 — 완료 폴더에서 plan.json 만 없음
                    (d / "plan.json").unlink()
                if st_ == "final":
                    shutil.copy(canon / "final.xyz", d / "final.xyz"); shutil.copy(canon / "result.json", d / "result.json")
            dm_stage(d, st_, th_full=(canon / "thermo.csv").read_text(encoding="utf-8").splitlines(keepends=True), src_full=canon)
            inv_kind = pv.get("kind") == "invalid"             # invalid 종류는 끝난 런의 판정이다 (DO 전 리뷰 — 끊긴 런의 invalid 판정은 종류를 안 바꾼다)
            row = {"system": sysn, "seed": seed, "run_id": rid_, "start": "t", "end": "t",
                   "status": pv.get("status", "ended" if inv_kind else "interrupted"),
                   "rc": pv.get("rc", 0 if inv_kind else "killed_runner_exit"), "wall_h": pv.get("wall_h", 1.0), "cost_basis": "measured"}
            if pv.get("kind") == "invalid":
                (d / "stage1_verdict.json").write_text(json.dumps({"status": "invalid"}), encoding="utf-8")
                if pv.get("ledger_verdict", True):           # False = 폴더에만 판정 (회신 DK P0-2 대조)
                    row["verdict"] = "invalid"
            chain.append((d, row, pv))
        seq = chain + [(canon, led_["runs"][ic], None)]
        hist_ = list(led_.get("stop_history") or [])
        for k, (d, row, _) in enumerate(seq):
            rf = {"retry_of": None, "retry_stop_id": None, "retry_kind": None}
            if k:
                _, prow, ppv = seq[k - 1]
                kind = ppv.get("kind", "interrupted")
                sid = f"selftest{k}{sysn}{seed}"
                rec = {"at": "t", "code": ppv.get("code", "invalid" if kind == "invalid" else "interrupted"), "reason": "selftest",
                       "terminal": False, "run_id": prow["run_id"], "stop_id": sid, "acked_at": "t"}
                if ppv.get("decl") is not None:
                    rec["declaration"] = DECL(ppv["decl"])
                hist_.append(rec)
                rf = {"retry_of": prow["run_id"], "retry_stop_id": sid, "retry_kind": kind}
            row.update(rf)
            base_att = J(d / "stage1_attempt.json") if (d / "stage1_attempt.json").is_file() else {"system": sysn, "seed": seed, "run_id": row["run_id"]}
            _write_json_atomic(d / "stage1_attempt.json", {**base_att, **rf})
        led_["runs"][ic:ic] = [row for _, row, _ in chain]
        led_["stop_history"] = hist_
        _write_json_atomic(rr_ / "stage1_ledger.json", led_)
        return [row["run_id"] for _, row, _ in chain]

    wt = mk_wt()
    # 1) 모두 통과 — 진짜 판독 함수로
    rc, L, rr = go(wt)
    sm = J(rr / "stage1_summary.json"); led = J(rr / "stage1_ledger.json")
    v11 = J(rr / "A/seed11/stage1_verdict.json")
    chk(rc == 0 and len(L) == 10 and tag(L)[:3] == [("A", 11), ("B", 11), ("A", 12)] and sm["track"] == "stage1_pass"
        and sm["stage2"]["seeds"] == [11, 12] and len(led["runs"]) == 10 and all(r["status"] == "ended" for r in led["runs"])
        and v11["status"] == "pass" and v11["provenance"]["files_sha256"]["traj.xyz"] and not v11["closes_system"]
        and all(getattr(p_, "ledger_at_first_poll", False) for p_ in L),
        f"진짜 판독 함수: 10 담금질 · A/B 번갈아 · 띄운 직후 장부에 시작 (첫 poll 전) · 판정에 원자료 지문 · 1 단계 통과 · 2 단계 시드 {sm['stage2'] and sm['stage2']['seeds']} (rc {rc})")
    c0 = L[0].cmd
    chk(c0[c0.index("--fix_density") + 1] == repr(float(rho["A"])) and c0[c0.index("--compress_ps") + 1] == "20"
        and "--turbo" in c0 and c0[c0.index("--n_fu") + 1] == "12" and L[1].cmd[L[1].cmd.index("--n_fu") + 1] == "15",
        "담금질 명령: 카드 기계값 그대로 (밀도 repr · 압축 20 · turbo · n_fu 12/15 = 카드 조성의 P 수)")
    real_vals = real.read_li2s2_values(repo / CARD_REL)
    cmdA = build_cmd("py", repo, "/r", "A", 11, real_vals, real)
    chk(cmdA[cmdA.index("--fix_density") + 1] == "1.91347" and cmdA[cmdA.index("--quench_rate") + 1] == "1000000000000",
        "DG P2: 진짜 카드의 손 실행 명령은 기계값 1.91347 그대로 (본문 1.9135 반올림 아님) · --print_cmd 와 같은 함수")
    # 2) DG P0-1 — A11 녹음 미충족 → 닫음 → 재시작 · STOP 지움 · 장부 지움 어느 쪽으로도 다시 안 열린다
    wt_m = mk_wt()
    rc, L, rr = go(wt_m, scen={("A", 11): {"melt": "fail", "polls": 8}})
    v = J(rr / "A/seed11/stage1_verdict.json"); sp = J(rr / "STOP.json")
    chk(rc == RC["melt"] and len(L) == 1 and L[0].killed and v["status"] == "fail" and v["closes_system"] and sp["terminal"],
        "⛔음성 DF Q-DF-3 · DG P0-1: A11 녹음 미충족 → 그 담금질을 실제로 멈추고 · 판정 fail + closes_system · STOP (닫는 사건)")
    rc2, L2, _ = go(wt_m, rr=rr)
    rc3, L3, _ = go(wt_m, rr=rr, ack=sp["stop_id"])
    stop_id3, hist3 = J(rr / "STOP.json")["stop_id"], J(rr / "stage1_ledger.json").get("stop_history")   # rc3 직후에 잰다
    (rr / "STOP.json").unlink()
    rc4, L4, _ = go(wt_m, rr=rr)
    (rr / "STOP.json").unlink(); (rr / "stage1_ledger.json").unlink()
    rc5, L5, _ = go(wt_m, rr=rr)
    chk(rc2 == RC["melt"] and rc3 == RC["melt"] and not L2 and not L3 and not hist3 and stop_id3 == sp["stop_id"],
        f"⛔음성 DG P0-1: 같은 run_root 로 재시작해도 · --ack_stop 을 줘도 닫는 사건은 다시 안 열린다 (담금질 0 · rc {rc2} · {rc3} · "
        f"STOP 그대로 · 이력 {len(hist3 or [])})")
    sm5 = real.stage1_summary(rr, values=real.read_li2s2_values(wt_m / CARD_REL), log=lambda *m: None)
    chk(rc4 == RC["melt"] and not L4 and rc5 == RC["refused"] and not L5 and sm5["track"] == "stop_track"
        and not (rr / "stage1_ledger.json").exists(),
        f"⛔음성 DG P0-1: STOP 을 지워도 장부가 막고 · 장부까지 지우면 러너는 빈 장부를 안 만들고 거부 · 판정 파일 (closes_system) 은 "
        f"묶음에서 그 계를 닫는다 (rc {rc4} · {rc5} · 묶음 {sm5['track']})")
    rc, L, rr = go(wt, scen={("B", 11): {"melt": "fail", "polls": 8}})
    chk(rc == RC["melt"] and len(L) == 2 and L[1].killed and not L[0].killed, "⛔음성: B11 녹음 미충족 → B11 을 멈추고 트랙 멈춤 (A11 은 끝까지)")
    rc, L, rr = go(wt, scen={("A", 12): {"melt": "fail"}})
    sm = J(rr / "stage1_summary.json"); v12 = J(rr / "A/seed12/stage1_verdict.json")
    chk(rc == 0 and len(L) == 10 and not any(p.killed for p in L) and v12["status"] == "fail" and not v12["closes_system"]
        and sm["stage2"]["seeds"] == [11, 13],
        f"첫 시드가 아닌 A12 녹음 미충족은 일반 탈락 (담금질 중 안 멈춤 · 계를 안 닫음) → A 4/5 · 2 단계 시드 {sm['stage2'] and sm['stage2']['seeds']}")
    rc, L, rr = go(wt, scen={("A", 12): {"final": "ps4_broken"}, ("A", 13): {"final": "ps4_broken"}})
    chk(rc == RC["track"] and len(L) == 5 and J(rr / "STOP.json")["summary"]["track"] == "stop_track",
        "⛔음성 DF P1-3: A 탈락 (PS₄ 깨짐) 이 둘이 되는 순간 (A13 뒤) 트랙 멈춤 — B 가 통과 중이어도")
    # 3) DG P1-4 — final.xyz 오복사 (5 원자 · 밀도 다름) 는 진짜 stage1_verdict 가 무효로
    rc, L, rr = go(wt, scen={("A", 12): {"final": "five"}})
    v = J(rr / "A/seed12/stage1_verdict.json")
    chk(rc == RC["invalid"] and len(L) == 3 and v["status"] == "invalid" and J(rr / "stage1_summary.json")["track"] == "invalid"
        and not J(rr / "STOP.json")["terminal"],
        "⛔음성 DG P1-4: final.xyz 에 5 원자 PS₄ 를 넣으면 진짜 stage1_verdict 가 무효 → 멈춤 (자료 오류 · 과학적 종료 아님 · 통과 아님)")
    rc, L, rr = go(wt, scen={("B", 11): {"final": "dense"}})
    chk(rc == RC["invalid"] and J(rr / "B/seed11/stage1_verdict.json")["status"] == "invalid",
        "⛔음성 DG P1-4: final.xyz 의 셀 · 밀도가 계획과 다르면 무효")
    rr_full = go(wt)[2]
    rr_v = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
    for s in SYSTEMS:
        for sd in (11, 12, 13, 14, 15):
            (rr_v / s / f"seed{sd}").mkdir(parents=True)
            shutil.copy(rr_full / s / f"seed{sd}" / "stage1_verdict.json", rr_v / s / f"seed{sd}" / "stage1_verdict.json")
    smv = real.stage1_summary(rr_v, values=real.read_li2s2_values(wt / CARD_REL), log=lambda *m: None)
    rc0, L0, _ = go(wt, rr=rr_v)
    chk(rc0 == RC["refused"] and not L0 and not (rr_v / "stage1_ledger.json").exists(),
        "⛔음성 DH P0-1: 산출물은 있는데 장부가 없으면 빈 장부를 만들지 않고 거부 (비용 0 으로 통과하는 길을 막는다)")
    shutil.copy(rr_full / "stage1_ledger.json", rr_v / "stage1_ledger.json")
    rc, L, _ = go(wt, rr=rr_v)
    hist = [json.loads(x) for x in (rr_v / "A/seed11" / real.VERDICT_HISTORY).read_text(encoding="utf-8").splitlines()]
    chk(smv["track"] == "invalid" and len(smv["stale_verdicts"]) == 10 and rc in (RC["resume"], RC["invalid"]) and not L
        and J(rr_v / "stage1_summary.json")["track"] != "stage1_pass"
        and J(rr_v / "A/seed11/stage1_verdict.json")["status"] == "incomplete"
        and hist[-1]["prev_status"] == "pass" and hist[-1]["new_status"] == "incomplete" and hist[-1]["prev"]["status"] == "pass",
        f"⛔음성 DG P1-4: 원자료 없이 통과 판정 파일만 있는 폴더 — 묶음은 지문 불일치로 무효 · 러너는 다시 판정해 안 띄우고 멈춤 (rc {rc})")
    shutil.copy(rr_full / "A/seed11/final.xyz", rr_full / "A/seed11/final.xyz.bak")
    (rr_full / "A/seed11/final.xyz").write_text((rr_full / "A/seed11/final.xyz").read_text().replace("Cl ", "Cl ", 1) + "\n", encoding="utf-8")
    sm_t = real.stage1_summary(rr_full, values=real.read_li2s2_values(wt / CARD_REL), log=lambda *m: None)
    chk(sm_t["track"] == "invalid" and sm_t["stale_verdicts"] == ["A11"],
        "⛔음성 DG P1-4: 판정 뒤 원자료 (final.xyz) 가 한 바이트라도 바뀌면 그 시드 판정은 무효 (다시 판정하라)")
    shutil.move(rr_full / "A/seed11/final.xyz.bak", rr_full / "A/seed11/final.xyz")
    vals_other = json.loads(json.dumps(real.read_li2s2_values(wt / CARD_REL)))
    vals_other["melt_window"]["threshold_source"] = "시험: 카드 값 글자 하나만 다름"
    sm_card = real.stage1_summary(rr_full, values=vals_other, log=lambda *m: None)
    sm_same = real.stage1_summary(rr_full, values=real.read_li2s2_values(wt / CARD_REL), log=lambda *m: None)
    chk(sm_card["track"] == "invalid" and len(sm_card["stale_verdicts"]) == 10 and sm_same["track"] == "stage1_pass",
        "⛔음성 DG P1-4: 다른 카드 값으로 낸 판정은 묶음에서 무효 (카드 값 지문 · 같은 카드면 그대로 통과)")
    # 4) DG P0-2 — Ctrl-C · 예외 · 판독 예외
    hook = {"armed": True}
    def ctrl_c(t):
        if hook["armed"] and t >= 3600.0 * 7 + 1:     # A11 (5 h) 끝난 뒤 B11 의 둘째 poll 전후
            hook["armed"] = False; raise KeyboardInterrupt("시험: 사용자 Ctrl-C")
    wt_i = mk_wt()
    rc, L, rr = go(wt_i, sleep_hook=ctrl_c)
    led = J(rr / "stage1_ledger.json"); sp = J(rr / "STOP.json")
    lk = _Lock(rr / "stage1.lock"); got_lock = lk.acquire(); lk.release()
    chk(rc == RC["interrupted"] and L[-1].killed and led["runs"][-1]["status"] == "interrupted" and led["runs"][-1]["end"]
        and led["runs"][-1]["wall_h"] is not None and sp["code"] == "interrupted" and not sp["terminal"] and got_lock,
        "⛔음성 DG P0-2: 담금질 중 Ctrl-C → 그 담금질을 멈추고 · 장부에 끝 · 경과 · STOP 을 쓴 뒤 잠금을 푼다")
    rc_a, La, _ = go(wt_i, rr=rr)
    rc_b, Lb, _ = go(wt_i, rr=rr, ack="0000000000000000")
    rc_c, Lc, _ = go(wt_i, rr=rr, ack=sp["stop_id"])
    chk(rc_a == RC["interrupted"] and rc_b == RC["interrupted"] and not La and not Lb and rc_c == RC["resume"] and not Lc
        and J(rr / "stage1_ledger.json")["stop_history"][-1]["stop_id"] == sp["stop_id"],
        "⛔음성 DG P0-2: 중단 뒤 재시작은 --ack_stop <stop_id> 가 맞아야 이어가고 · 끊긴 시드 폴더에서 멈춘다 (덮어쓰지 않는다)")
    rc, L, rr = go(wt, scen={("A", 11): {"raise_on_poll": 3, "polls": 6}})
    lk = _Lock(rr / "stage1.lock"); got_lock = lk.acquire(); lk.release()
    chk(rc == RC["interrupted"] and L[0].killed and J(rr / "stage1_ledger.json")["runs"][0]["status"] == "interrupted" and got_lock,
        "⛔음성 DG P0-2: poll 이 예외를 던져도 (자식 상태 확인 실패) 담금질을 멈추고 장부 · 잠금 정리")
    rc, L, rr = go(wt, gpu=[100, 100, 100, 100, RuntimeError("nvidia-smi 실패")])
    sp = J(rr / "STOP.json")
    chk(rc == RC["interrupted"] and len(L) == 2 and not any(p.killed for p in L) and sp["code"] == "interrupted",
        "⛔음성 DG P0-2: 담금질 사이의 예외 (nvidia-smi) → 돌던 담금질 없음 · STOP · 잠금 정리")
    class FlakyMQ:
        def __init__(self):
            self.n = 0
        def __getattr__(self, k):
            return getattr(real, k)
        def melt_window_check(self, rd, values=None, log=None):
            self.n += 1
            if self.n == 2:
                raise RuntimeError("시험: 판독 예외")
            return real.melt_window_check(rd, values=values, log=log)
    rc, L, rr = go(wt, mq=FlakyMQ())
    led = J(rr / "stage1_ledger.json")
    chk(rc == 0 and len(led["runs"][0].get("melt_check_errors", [])) == 1,
        "DG P0-2: 녹음 판정이 한 번 예외를 던져도 러너는 죽지 않고 기록 뒤 다음 poll 에 다시 본다 (진짜 판독기 · plan 없음 → 미완)")
    # 5) DG P0-3 — 실행 중 상한 (아홉 런 20 h · 마지막 60 h · 상한 230)
    scen = {(s, sd): {"polls": 20} for s in SYSTEMS for sd in (11, 12, 13, 14, 15)}
    scen[("B", 15)] = {"polls": 60}
    rc, L, rr = go(wt, scen=scen)
    led = J(rr / "stage1_ledger.json"); sm = real.stage1_summary(rr, values=real.read_li2s2_values(wt / CARD_REL), log=lambda *m: None)
    chk(rc == RC["cap"] and len(L) == 10 and L[-1].killed and abs(led["runs"][-1]["wall_h"] - 50.0) < 1e-9
        and led["runs"][-1]["status"] == "cap" and sm["track"] != "stage1_pass",
        f"⛔음성 DG P0-3: 마지막 런이 60 h 여도 누적 230 h 에서 그 담금질을 멈추고 미완결 (wall {led['runs'][-1]['wall_h']:.1f} h · 묶음 {sm['track']})")
    rc, L, rr = go(mk_wt(card=mk_card(stage1_cap_gpu_h=40.0)), scen={k: {"polls": 10} for k in scen})
    chk(rc == RC["cap"] and len(L) == 2 and J(rr / "STOP.json")["code"] == "cap",
        "⛔음성 DF P1-6: 누적 + 한 시드 최악 > 상한 (카드 40 h) 이면 새 시드를 안 띄우고 미완결")
    sid_cap = J(rr / "STOP.json")["stop_id"]
    rc_c2, Lc2, _ = go(mk_wt(card=mk_card(stage1_cap_gpu_h=40.0)), rr=rr, ack=sid_cap)
    chk(rc_c2 == RC["cap"] and not Lc2 and J(rr / "STOP.json")["stop_id"] == sid_cap and not J(rr / "stage1_ledger.json").get("stop_history"),
        "⛔음성 DG P0-3: 상한 멈춤은 --ack_stop 만으로 안 넘어간다 (STOP 그대로 · 이력에 안 옮김 — 카드 상한이 올라가야)")
    # 소비자 쪽 상한 (회신 DG P0-3) — 다 통과한 폴더라도 장부 합이 상한을 넘거나 장부가 없으면 1 단계 통과가 아니다
    vals_t = real.read_li2s2_values(wt / CARD_REL)
    led_full = J(rr_full / "stage1_ledger.json")
    sm_ok = real.stage1_summary(rr_full, values=vals_t, log=lambda *m: None)
    # 비싼 상한 멈춤 런 (300 h) 뒤의 정당한 재시도 (budget_cap_raised) — 이력 · 선언 규칙은 통과 · 상한만 넘는다 (정전 손실 아님 → 실효 상한 = 230)
    with_history(rr_full, "A", 11, [{"status": "cap", "rc": "killed_cap", "wall_h": 300.0, "code": "cap",
                                     "decl": {**OUT, "retry_reason": "budget_cap_raised", "retry_event": "카드 상한 개정 (selftest)"}}])
    sm_over = real.stage1_summary(rr_full, values=vals_t, log=lambda *m: None)
    (rr_full / "stage1_ledger.json").unlink()
    sm_none = real.stage1_summary(rr_full, values=vals_t, log=lambda *m: None)
    chk(sm_ok["track"] == "stage1_pass" and sm_over["track"] == "cap_incomplete" and sm_over["cost"]["cap_h"] == 230.0 and sm_none["track"] == "pending",
        f"⛔음성 DG P0-3 (소비자): 다 통과해도 장부 합 > 상한이면 미완결 · 장부가 없으면 대기 ({sm_ok['track']} · {sm_over['track']} · {sm_none['track']})")
    # 6) 시작 전 검사 · 끊긴 런 · 잠금 · 고아 런 · 순서
    rc, L, rr = go(mk_wt(state="proposed"))
    chk(rc == RC["refused"] and not L, "⛔음성: 결정이 proposed 면 시작하지 않는다")
    rc, L, rr = go(wt, expect="0000000000000000")
    chk(rc == RC["refused"] and not L, "⛔음성: 드라이버 sha16 이 고정값과 다르면 시작하지 않는다")
    bad_card = mk_card(); bad_card["기계_판독_값"]["melt_window"]["estimator"] = "window_mto_v2"
    rc, L, rr = go(mk_wt(card=bad_card))
    chk(rc == RC["refused"] and not L, "⛔음성 DG P1-7: 카드 estimator 가 구현과 다르면 시작하지 않는다")
    rc, L, rr = go(wt, order="A:11,B:11,A:12,B:12,A:13,B:13,A:14,B:14,A:15")
    rc2, L2, _ = go(wt, order="A:12,B:11,A:11,B:12,A:13,B:13,A:14,B:14,A:15,B:15")
    chk(rc == RC["refused"] and rc2 == RC["refused"] and not L and not L2, "⛔음성: 순서가 카드 시드 전부가 아니거나 첫 시드 ≠ 카드 first_seed 면 거부")
    rr0 = pathlib.Path(tempfile.mkdtemp(dir=tmp_root)); (rr0 / "A/seed11").mkdir(parents=True)
    rc_n, L_n, _ = go(wt, rr=rr0)
    _write_json_atomic(rr0 / "stage1_ledger.json", {"runs": []})
    rc, L, _ = go(wt, rr=rr0)
    chk(rc_n == RC["refused"] and rc == RC["resume"] and not L and not L_n,
        "⛔음성: 판정 없이 런 폴더만 있으면 — 장부도 없으면 거부 · 장부가 있으면 끊긴 런을 덮어쓰지 않고 멈춘다")
    rr1 = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
    held = _Lock(rr1 / "stage1.lock"); assert held.acquire()
    rc, L, _ = go(wt, rr=rr1)
    held.release()
    second = _Lock(rr1 / "stage1.lock"); a1 = second.acquire(); third = _Lock(rr1 / "stage1.lock"); a2 = third.acquire(); second.release()
    chk(rc == RC["refused"] and not L and a1 and not a2,
        "⛔음성 DG P1-6: 잠금을 잡은 러너가 있으면 거부 · 잠금은 한 번의 flock (둘째 획득 실패) · 놓으면 다시 잡힌다")
    (rr1 / "stage1.lock").write_text("999999\n")          # 죽은 러너가 남긴 잠금 파일 — flock 이 아니라 파일만
    rc, L, _ = go(wt, rr=rr1)
    chk(rc == 0 and len(L) == 10, "낡은 잠금 파일 (프로세스 없음) 은 막지 않는다 — flock 은 커널이 풀었다")
    rr2 = pathlib.Path(tempfile.mkdtemp(dir=tmp_root)); (rr2 / "A/seed11").mkdir(parents=True)
    _write_json_atomic(rr2 / "A/seed11/stage1_attempt.json", {"system": "A", "seed": 11, "run_id": "e" * 32, "retry_of": None,
                                                            "retry_stop_id": None, "retry_kind": None})
    (rr2 / "A/seed11/thermo.csv").write_text("x\n")
    t_start = time.time() - 7200
    os.utime(rr2 / "A/seed11/thermo.csv", (t_start + 3600, t_start + 3600))   # 마지막 기록 = 시작 + 1 h → 하한 1.5 h (heartbeat) · 상한 2.0 h 가 갈린다
    _write_json_atomic(rr2 / "stage1_ledger.json", {"runs": [{"system": "A", "seed": 11, "run_id": "e" * 32, "start": "t", "start_epoch": t_start,
                                                               "pgid": 4242, "status": "running", "end": None, "wall_h": None,
                                                               "start_recovery_clock": {"host": "fixture", "boot_id": "fixture", "kind": "CLOCK_BOOTTIME", "seconds": 0.0},
                                                               "wall_h_so_far": 1.5}]})
    rc_al, L_al, _ = go(wt, rr=rr2, pg_alive=lambda pg: pg == 4242)
    rc_or, L_or, _ = go(wt, rr=rr2)
    led = J(rr2 / "stage1_ledger.json")
    chk(rc_al == RC["refused"] and not L_al and rc_or == RC["resume"] and not L_or and led["runs"][0]["status"] == "orphaned"
        and led["runs"][0]["cost_basis"] == "upper_bound" and led["runs"][0]["wall_h"] >= 2.0 - 1e-3
        and abs(led["runs"][0]["wall_h_lower"] - 1.5) < 1e-6 and led["runs"][0]["wall_h"] - led["runs"][0]["wall_h_lower"] > 0.4,
        f"⛔음성 DG P0-2 · DH P0-1: 장부의 도는 중 런 — 그룹이 살아 있으면 거부 · 죽었으면 고아 런 · 비용은 보수 상한 "
        f"({led['runs'][0]['wall_h']:.2f} h ≥ 하한 {led['runs'][0]['wall_h_lower']:.2f}) · 끊긴 폴더에서 멈춤")
    rc, L, rr = go(wt, scen={("B", 12): {"rc": 137}})
    chk(rc == RC["abnormal"] and len(L) == 4, "⛔음성: B12 담금질 rc 137 (비정상) → 멈춤 (뒤 시드 안 띄움)")
    rc, L, rr = go(wt, gpu=[9000, 9000, 1500, 9000, 1500, 1500])
    chk(rc == 0 and len(L) == 10 and "비기를 기다린다" in (rr / "stage1.log").read_text(encoding="utf-8"),
        "GPU 가 찰 때는 두 번 연속 빌 때까지 기다린 뒤 띄운다")
    # 8) 회신 DH — 장부 완전성 · 실행 식별 · 그룹 잔존 · invalid 구분 · 재판정 이력 (진짜 판독 함수)
    vals_t = real.read_li2s2_values(wt / CARD_REL)
    rr_d = go(wt)[2]
    def clone(src):
        dst = pathlib.Path(tempfile.mkdtemp(dir=tmp_root)) / "r"
        shutil.copytree(src, dst)
        (dst / "stage1.lock").unlink(missing_ok=True)
        return dst
    summ = lambda rr_: real.stage1_summary(rr_, values=vals_t, log=lambda *m: None)
    led0 = J(rr_d / "stage1_ledger.json")
    r1 = clone(rr_d); _write_json_atomic(r1 / "stage1_ledger.json", {"runs": []})
    r2 = clone(rr_d); _write_json_atomic(r2 / "stage1_ledger.json", {**led0, "runs": led0["runs"][1:]})
    r3 = clone(rr_d); _write_json_atomic(r3 / "stage1_ledger.json", {**led0, "runs": [dict(x, wall_h=-10.0) for x in led0["runs"]]})
    r4 = clone(rr_d); _write_json_atomic(r4 / "stage1_ledger.json", {**led0, "runs": [dict(x, end=None, status="running") for x in led0["runs"]]})
    r5 = clone(rr_d); _write_json_atomic(r5 / "stage1_ledger.json", {**led0, "runs": [dict(x, cost_basis="lower_bound") for x in led0["runs"]]})
    t1, t2, t3, t4, t5 = (summ(x)["track"] for x in (r1, r2, r3, r4, r5))
    chk(t1 == t2 == t3 == t5 == "invalid" and t4 == "pending" and summ(rr_d)["track"] == "stage1_pass",
        f"⛔음성 DH P0-1: 빈 장부 · 한 행 누락 · 음수 비용 · 하한 근거 → 무효 · 모든 행이 안 끝남 → 대기 ({t1} · {t2} · {t3} · {t5} · {t4})")
    rc_e, L_e, _ = go(wt, rr=r1)
    sid_e = J(r1 / "STOP.json")["stop_id"]
    rc_e2, L_e2, _ = go(wt, rr=r1, ack=sid_e)
    chk(rc_e == RC["invalid"] and rc_e2 == RC["invalid"] and not L_e and not L_e2 and J(r1 / "stage1_summary.json")["track"] == "invalid",
        "⛔음성 DH P0-1: 빈 장부로 러너를 띄워도 · 그 멈춤을 --ack_stop 으로 확인해도 통과 · 발사 없음 (확인이 비용을 복원하지 않는다)")
    c1 = clone(rr_d); shutil.rmtree(c1 / "A/seed12"); shutil.copytree(c1 / "A/seed11", c1 / "A/seed12")
    s_c1 = summ(c1)
    rc_c1, L_c1, _ = go(wt, rr=c1)
    chk(s_c1["track"] == "invalid" and rc_c1 == RC["invalid"] and not L_c1 and J(c1 / "A/seed12/stage1_verdict.json")["status"] == "invalid",
        "⛔음성 DH P0-2: A11 폴더를 A12 에 복사하면 묶음 · 다시 판정 둘 다 무효 (폴더 12 ≠ plan 11) — 발사 없음")
    c2 = clone(rr_d)
    for s_ in SYSTEMS:
        for sd in (12, 13, 14, 15):
            shutil.rmtree(c2 / s_ / f"seed{sd}"); shutil.copytree(c2 / s_ / "seed11", c2 / s_ / f"seed{sd}")
    s_c2 = summ(c2)
    chk(s_c2["track"] == "invalid", f"⛔음성 DH P0-2: 계마다 한 실행을 다섯 자리에 복사해도 다섯 통과로 안 센다 ({s_c2['track']})")
    c3 = clone(rr_d); shutil.rmtree(c3 / "A/seed12"); shutil.copytree(c3 / "A/seed11", c3 / "A/seed12")
    pl = J(c3 / "A/seed12/plan.json"); pl["seed"] = 12; (c3 / "A/seed12/plan.json").write_text(json.dumps(pl), encoding="utf-8")
    real.stage1_verdict(c3 / "A/seed12", values=vals_t, log=lambda *m: None, reason="시험")
    s_c3 = summ(c3)
    chk(s_c3["track"] == "invalid" and J(c3 / "A/seed12/stage1_verdict.json")["status"] != "invalid"
        and any("run_id" in x for x in s_c3["identity_problems"] + list((s_c3.get("cost") or {}).get("invalid") or [])),
        "⛔음성 DH P0-2: plan 시드까지 12 로 고치면 시드 판정은 통과해도 run_id 가 A11 과 같고 장부에선 A11 런이라 묶음 무효")
    r6 = clone(rr_d)
    rows = [dict(x) for x in led0["runs"]]
    ia = [i for i, x in enumerate(rows) if (x["system"], x["seed"]) in (("A", 11), ("A", 12))]
    rows[ia[0]]["seed"], rows[ia[1]]["seed"] = rows[ia[1]]["seed"], rows[ia[0]]["seed"]
    _write_json_atomic(r6 / "stage1_ledger.json", {**led0, "runs": rows})
    s_r6 = summ(r6)
    chk(s_r6["track"] == "invalid" and any("장부에서" in x for x in (s_r6.get("cost") or {}).get("invalid") or []),
        "⛔음성 DH P0-2: 장부 행의 시드 표시가 바뀌면 (A11 ↔ A12) 판정의 run_id 가 장부에서 다른 시드 런이라 무효")
    rc_g, L_g, rr_g = go(wt, scen={("A", 11): {"melt": "fail", "polls": 8, "group_stuck": True}})
    eg, sg = J(rr_g / "stage1_ledger.json")["runs"][0], J(rr_g / "STOP.json")
    rc_g2, L_g2, _ = go(wt, rr=rr_g, ack=sg["stop_id"], pg_alive=lambda pg: True)
    chk(rc_g == RC["melt"] and eg["status"] == "stop_failed" and eg["end"] is None and sg["code"] == "melt" and sg["terminal"] is True
        and eg.get("closes_system") is True and (eg.get("melt_check") or {}).get("verdict") == "fail"
        and rc_g2 == RC["melt"] and not L_g2,
        "⛔음성 DH P0-3 · DO 전 리뷰 P0-1: 첫 시드 녹음 fail 인데 그룹이 남으면 — 비용 확정으로 안 적고 (stop_failed · 끝 없음) · **닫힘은 멈추기 전에 "
        "장부에 적고** (closes_system · melt_check) · 멈춤은 melt (닫힘 · 확인으로 못 넘김) · 재시작 거부")
    rc_g3, L_g3, rr_g3 = go(wt, scen={("B", 11): {"group_stuck": True}})
    e3 = [x for x in J(rr_g3 / "stage1_ledger.json")["runs"] if x["system"] == "B"][0]
    chk(rc_g3 == RC["abnormal"] and e3["status"] == "stop_failed" and e3["end"] is None and len(L_g3) == 2,
        "⛔음성 DH P0-3: 대표가 rc 0 으로 끝나도 그룹에 일꾼이 남으면 정리 실패로 멈춘다 (끝 · 비용 확정 안 함 · 다음 시드 안 띄움)")
    rc_i, L_i, rr_i = go(wt, scen={("A", 11): {"melt": "species_swap", "polls": 8}})
    vi, si = J(rr_i / "A/seed11/stage1_verdict.json"), J(rr_i / "STOP.json")
    chk(rc_i == RC["invalid"] and L_i[0].killed and vi["status"] == "invalid" and not vi["closes_system"]
        and si["code"] == "invalid" and not si["terminal"] and "증거가 아니다" in si["reason"],
        "⛔음성 DH P1-4: 첫 시드 녹음 판정 invalid (0 번 프레임 종 바뀜) → 멈추되 과학적 종료 (melt · terminal) 로 적지 않는다")
    (rr_i / "A/seed11").rename(rr_i / "A/seed11.invalid_selftest")
    rc_i2, L_i2, _ = go(wt, rr=rr_i, ack=si["stop_id"], declare=FIX)
    chk(rc_i2 == 0 and len(L_i2) == 10 and len(J(rr_i / "stage1_ledger.json")["runs"]) == 11
        and J(rr_i / "stage1_summary.json")["track"] == "stage1_pass",
        "DH P1-4 · DJ Q1: 자료 오류는 고친 뒤 (폴더를 옆으로 · --ack_stop + 원인 고침 선언) 다시 돌린다 — 앞 런 비용은 장부에 남는다 (11 런)"
        + ("" if rc_i2 == 0 else f" — rc {rc_i2} · 발사 {len(L_i2)} · STOP {J(rr_i / 'STOP.json').get('reason') if (rr_i / 'STOP.json').is_file() else None} · "
                                 f"단계 {real.folder_stage_detail(rr_i / 'A/seed11.invalid_selftest')}"))
    h1 = clone(rr_d)
    with open(h1 / "A/seed11/final.xyz", "a") as fh:
        fh.write("\n")
    s_h1 = summ(h1)
    rc_h, L_h, _ = go(wt, rr=h1)
    hist = [json.loads(x) for x in (h1 / "A/seed11" / real.VERDICT_HISTORY).read_text(encoding="utf-8").splitlines()]
    last = hist[-1]
    chk(s_h1["track"] == "invalid" and rc_h == 0 and not L_h and last["prev_status"] == "pass" and last["new_status"] == "pass"
        and last["changed"]["files"] == ["final.xyz"] and "재시작" in last["reason"] and last["prev"]["status"] == "pass"
        and last["prev_provenance"]["files_sha256"]["final.xyz"] != last["new_provenance"]["files_sha256"]["final.xyz"],
        "⛔음성 DH P1-5: 판정 뒤 final.xyz 가 바뀌면 묶음 무효 · 재시작 재판정은 통과지만 이전 판정 전체 · 지문 변화 · 사유가 이력에 남는다 (pass → pass)")
    # 9) DI: fail 복구 금지 · 보존 실행 비용 · 그룹 판독 불가 · 정리 시간 · 단조 시계
    rc_f, L_f, rr_f = go(wt, scen={("A", 12): {"final": "ps4_broken"}})
    before_f = J(rr_f / "stage1_summary.json")
    (rr_f / "A/seed12").rename(rr_f / "A/seed12.failed_selftest")
    rc_f2, L_f2, _ = go(wt, rr=rr_f)
    chk(rc_f == 0 and before_f["stage2"]["seeds"] == [11, 13] and rc_f2 == RC["invalid"] and not L_f2,
        "DI 음성: 과학적 fail 폴더를 옮겨도 같은 시드를 재담금질하지 않는다")
    r_hist = clone(rr_i)
    hist_led = J(r_hist / "stage1_ledger.json")
    retired_id = hist_led["runs"][0]["run_id"]
    hist_led["runs"] = hist_led["runs"][1:]
    _write_json_atomic(r_hist / "stage1_ledger.json", hist_led)
    cost_hist = summ(r_hist)
    chk(cost_hist["track"] == "invalid" and any(retired_id in e for e in cost_hist["cost"]["invalid"]),
        "DI 음성: 보존된 invalid 실행의 비용 행만 없어져도 묶음 무효")
    # Missing first-frame plan still has a pre-launch identity record.
    r_planless = clone(rr_d)
    (r_planless / "A/seed11/plan.json").unlink()
    inv, inv_bad = real.attempt_inventory(r_planless)
    chk(not inv_bad and len(inv) == 10 and (r_planless / "A/seed11" / real.ATTEMPT_NAME).is_file(),
        "DI 양성: plan 전 중단에도 실행 전 기록의 run_id 로 장부와 연결한다")
    rc_cc, L_cc, rr_cc = go(mk_wt(card=mk_card(stage1_cap_gpu_h=50.1)), seed_worst_h=5.0, cleanup_s=60.0)
    cc = J(rr_cc / "stage1_ledger.json")
    chk(rc_cc == RC["cap"] and len(L_cc) == 9
        and all(abs(x["wall_h"] - (5.0 + 1.0 / 60.0)) < 1e-9 for x in cc["runs"]),
        "DI 음성: 정상 종료 뒤 그룹 정리 60초도 비용에 포함하여 상한을 넘을 열 번째 실행을 차단한다")
    rc_clk, L_clk, rr_clk = go(mk_wt(card=mk_card(stage1_cap_gpu_h=47.0)), seed_worst_h=5.0, default_clock=True)
    clk = J(rr_clk / "stage1_ledger.json")
    chk(rc_clk == RC["cap"] and clk["runs"][0]["wall_h"] == 5.0,
        "DI 음성: 실제 러너 기본 시계 경로에서 벽시계가 4h 역행해도 실행 비용은 줄지 않는다")
    start_clk = {"host": "fixture", "boot_id": "b1", "kind": "CLOCK_BOOTTIME", "seconds": 100.0}
    eclk = {"start_recovery_clock": start_clk, "wall_h_so_far": 1.5}
    chk(_orphan_upper_hours(eclk, {**start_clk, "seconds": 7300.0}) == 2.0
        and _orphan_upper_hours(eclk, {**start_clk, "boot_id": "b2", "seconds": 7300.0}) is None
        and _orphan_upper_hours(eclk, {**start_clk, "seconds": 0.0}) is None
        and _orphan_upper_hours({}, start_clk) is None,
        "DI 음성/양성: 고아 상한은 같은 부팅의 단조 시계만 · 부팅 변경/역행/근거 없음은 None")
    rc_u, L_u, rr_u = go(wt, scen={("A", 11): {"group_stuck": True}})
    su = J(rr_u / "STOP.json")
    rc_u2, L_u2, _ = go(wt, rr=rr_u, ack=su["stop_id"], pg_alive=lambda pg: None)
    chk(rc_u2 == RC["refused"] and not L_u2 and J(rr_u / "stage1_ledger.json")["runs"][0]["end"] is None,
        "DI 음성: 이전 그룹 조회 불가(None)면 종료 확정 없이 재개 거부")
    # Safe dependency injection: never send signals to a real OS process in this test.
    import types, io
    class DeniedStat:
        def read_text(self):
            raise PermissionError("fixture unreadable stat")
    class ProcChild:
        name = "424243"
        def __truediv__(self, name):
            return DeniedStat()
    class ProcRoot:
        def is_dir(self): return True
        def iterdir(self): return iter([ProcChild()])
    class FinishedLeader:
        pid, returncode = 424242, 0
        def poll(self): return 0
    saved_os, saved_path, saved_sig = globals()["os"], globals()["pathlib"], globals()["signal"]
    os_proxy = types.SimpleNamespace(**{k: getattr(saved_os, k) for k in dir(saved_os)})
    sent = []
    os_proxy.killpg = lambda pg, sig: sent.append(int(sig))
    sig_proxy = types.SimpleNamespace(**{k: getattr(saved_sig, k) for k in dir(saved_sig)})
    sig_proxy.SIGKILL = 9
    globals()["os"], globals()["pathlib"], globals()["signal"] = os_proxy, types.SimpleNamespace(Path=lambda p: ProcRoot()), sig_proxy
    try:
        unknown = _pg_alive(424242)
        proc = _Proc.__new__(_Proc); proc.p = FinishedLeader(); proc.fh = io.StringIO()
        result = proc.stop(grace_s=0, kill_wait_s=0)
        chk(unknown is None and result["group_empty"] is False and result["left"] is None and result["inspection_errors"],
            "DI 음성: /proc 권한 오류는 빈 그룹이 아니며 정리 완료로 기록하지 않는다")
        def gone(pg, sig): raise ProcessLookupError("gone")
        os_proxy.killpg = gone
        chk(_group_members(424242) == [], "DI 양성: /proc 일부 판독 불가라도 자기 그룹 ESRCH 확인이면 부재")
    finally:
        globals()["os"], globals()["pathlib"], globals()["signal"] = saved_os, saved_path, saved_sig
    # 10) 정전 복구 개정 + 회신 DJ — 끊긴 런은 그 run_id 의 STOP 을 **선언과 함께** 확인한 뒤 시드마다 한 번 · 재부팅 고아 런은 증언 상한
    inv_ = lambda s_, w: s_["track"] == "invalid" and any(w in x for x in (s_.get("cost") or {}).get("invalid") or [])
    rc_t1, L_t1, rr_t1 = go(wt, scen={("B", 12): {"raise_on_poll": 3, "polls": 6}})
    s_t1 = J(rr_t1 / "STOP.json")
    e_t1 = [x for x in J(rr_t1 / "stage1_ledger.json")["runs"] if (x["system"], x["seed"]) == ("B", 12)][0]
    ok1 = rc_t1 == RC["interrupted"] and s_t1.get("run_id") == e_t1["run_id"] and e_t1["status"] == "interrupted"
    (rr_t1 / "B/seed12").rename(rr_t1 / "B/seed12.interrupted_selftest")
    rc_n1, L_n1, _ = go(wt, rr=rr_t1, ack=s_t1["stop_id"])                     # 선언 없이 확인 → 확인은 되지만 영수증이 아니다
    s_n1 = J(rr_t1 / "STOP.json")
    rc_n2, L_n2, _ = go(wt, rr=rr_t1, ack=s_n1["stop_id"], declare={**OUT, "retry_reason": "user_ctrl_c"})
    rc_n3, L_n3, _ = go(wt, rr=rr_t1, ack=s_n1["stop_id"], declare={**OUT, "retry_reason": "budget_cap_raised"})
    rc_n4, L_n4, _ = go(wt, rr=rr_t1, ack=s_n1["stop_id"], declare={**OUT, "declared_by": " "})
    still = J(rr_t1 / "STOP.json")["stop_id"] == s_n1["stop_id"]
    chk(ok1 and rc_n1 == RC["resume"] and not L_n1 and "선언" in s_n1["reason"] and s_n1.get("run_id") == e_t1["run_id"]
        and rc_n2 == rc_n3 == rc_n4 == RC["refused"] and not (L_n2 or L_n3 or L_n4) and still,
        "⛔음성 DJ Q1: 선언 없는 확인은 재시도 영수증이 아니다 (그 run_id 에 묶여 멈춤) · 허용 밖 사유 (Ctrl-C) · 상한 아닌 런에 상한 사유 · "
        "선언자 없음 → 확인 자체를 거부 (STOP 그대로 · 발사 0)")
    rc_t2, L_t2, _ = go(wt, rr=rr_t1, ack=s_n1["stop_id"], declare=OUT)
    led_t = J(rr_t1 / "stage1_ledger.json")
    b12 = [x for x in led_t["runs"] if (x["system"], x["seed"]) == ("B", 12)]
    sm_t2 = J(rr_t1 / "stage1_summary.json")
    rcpt_t = [h for h in led_t["stop_history"] if h.get("stop_id") == b12[-1].get("retry_stop_id")]
    chk(rc_t2 == 0 and len(b12) == 2 and b12[1].get("retry_of") == b12[0]["run_id"] and b12[1].get("retry_kind") == "interrupted"
        and len(rcpt_t) == 1 and rcpt_t[0]["declaration"]["reason"] == "power_outage" and rcpt_t[0]["run_id"] == b12[0]["run_id"]
        and J(rr_t1 / "B/seed12" / real.ATTEMPT_NAME).get("retry_stop_id") == b12[1]["retry_stop_id"]
        and sm_t2["track"] == "stage1_pass" and len(led_t["runs"]) == 11 and sm_t2["cost"]["cap_h"] == 230.0,
        "정전 복구 · DJ Q1 · DK: 판정 없이 끊긴 B12 (MD 미완) 는 그 run_id 의 STOP 을 정전 선언과 함께 확인한 뒤 한 번 다시 돈다 · 영수증 · "
        "실행 전 기록 · 장부가 서로 맞고 · 앞 런 비용은 장부에 남고 · 상한은 카드 230 그대로 (11 런 · 통과)")
    rc_dn, L_dn, _ = go(wt, rr=rr_t1, declare=OUT)            # 확인할 멈춤이 없는데 선언만 → 조용히 버리지 않고 거부
    chk(rc_dn == RC["refused"] and not L_dn and not (rr_t1 / "STOP.json").exists(),
        "⛔음성 DJ Q1: 확인할 멈춤이 없는데 재시도 선언만 주면 조용히 버리지 않고 거부 (발사 0)")
    rc_u1, L_u1, rr_u2 = go(wt, scen={("B", 12): {"raise_on_poll": 3, "polls": 6}})
    su1 = J(rr_u2 / "STOP.json"); (rr_u2 / "B/seed12").rename(rr_u2 / "B/seed12.int1")
    rc_u2b, L_u2b, _ = go(wt, rr=rr_u2, ack=su1["stop_id"], declare=OUT, scen={("B", 12): {"raise_on_poll": 3, "polls": 6}})
    su2 = J(rr_u2 / "STOP.json"); (rr_u2 / "B/seed12").rename(rr_u2 / "B/seed12.int2")
    rc_u3, L_u3, _ = go(wt, rr=rr_u2, ack=su2["stop_id"], declare=OUT)
    chk(rc_u2b == RC["interrupted"] and tag(L_u2b) == [("B", 12)] and rc_u3 == RC["invalid"] and not L_u3 and "한도" in J(rr_u2 / "STOP.json")["reason"],
        "⛔음성 정전 복구: 같은 시드가 두 번 끊기면 (카드 한도 1) 선언이 맞아도 세 번째는 안 돌린다 — 새 결정 없이는")
    c_d = clone(rr_d)
    led_cd = J(c_d / "stage1_ledger.json")
    b13 = [x for x in led_cd["runs"] if (x["system"], x["seed"]) == ("B", 13)][0]
    b13.pop("verdict", None)
    (c_d / "B/seed13/stage1_verdict.json").unlink()
    (c_d / "B/seed13").rename(c_d / "B/seed13.unjudged")
    led_cd["stop_history"] = list(led_cd.get("stop_history") or []) + [{"code": "interrupted", "run_id": b13["run_id"], "stop_id": "selftest",
                                                                      "acked_at": "t", "declaration": DECL(OUT)}]
    _write_json_atomic(c_d / "stage1_ledger.json", led_cd)
    rc_cd, L_cd, _ = go(wt, rr=c_d)
    chk(rc_cd == RC["resume"] and not L_cd and "끝까지 돌았다" in J(c_d / "STOP.json")["reason"],
        "⛔음성 정전 복구: 끝까지 돈 런 (결과 파일 있음 · 판정 없음) 은 선언이 맞아도 재시도가 아니라 판정해야 한다")
    c_m = clone(rr_d)
    led_cm = J(c_m / "stage1_ledger.json")
    b13m = [x for x in led_cm["runs"] if (x["system"], x["seed"]) == ("B", 13)][0]
    b13m.pop("verdict", None); b13m.update(status="interrupted", rc="killed_runner_exit")
    for f_ in ("stage1_verdict.json", "final.xyz", "result.json"):
        (c_m / "B/seed13" / f_).unlink()
    (c_m / "B/seed13").rename(c_m / "B/seed13.fire_cut")
    led_cm["stop_history"] = list(led_cm.get("stop_history") or []) + [{"code": "interrupted", "run_id": b13m["run_id"], "stop_id": "selftest_m",
                                                                      "acked_at": "t", "declaration": DECL(OUT)}]
    _write_json_atomic(c_m / "stage1_ledger.json", led_cm)
    rc_cm, L_cm, _ = go(wt, rr=c_m)
    chk(rc_cm == RC["resume"] and not L_cm and "FIRE" in J(c_m / "STOP.json")["reason"] and real.folder_stage(c_m / "B/seed13.fire_cut") == "md_complete",
        "⛔음성 DJ Q2: MD 는 끝났고 FIRE 만 못 마친 런은 선언이 맞아도 재담금질하지 않고 보류 (FIRE 복구는 새 결정)")
    corrupt = {}
    for nm_, how in (("atomcount", lambda t: t.replace(t.split("\n", 1)[0], str(int(t.split("\n", 1)[0]) + 1), 1)),
                     ("first_nul", lambda t: "\x00" + t[1:])):       # 회신 DK P0-1 재현 — 완료 기록 뒤 궤적 첫 줄만 깸
        c_x = clone(c_m); (c_x / "STOP.json").unlink(missing_ok=True)
        trj = c_x / "B/seed13.fire_cut/traj.xyz"; trj.write_text(how(trj.read_text(encoding="utf-8")), encoding="utf-8")
        rc_x, L_x, _ = go(wt, rr=c_x)
        corrupt[nm_] = (rc_x, len(L_x), "완료 단계를 못 읽는다" in J(c_x / "STOP.json")["reason"], real.folder_stage(c_x / "B/seed13.fire_cut"))
    chk(all(v_ == (RC["resume"], 0, True, "unreadable") for v_ in corrupt.values()),
        f"⛔음성 DK P0-1 (Codex 재현): MD 가 끝난 (완료 기록 있는) 궤적의 첫 원자 수만 바꾸거나 첫 줄을 NUL 로 → '미완' 이 아니라 판독 불가 → "
        f"재담금질 · 발사 0 (보류) ({corrupt})")
    # ⭐ 회신 DL P0 (Codex 재현 두 경로) + Q2 (기록 없이 끝 경계) — 완료 증거가 남은 폴더는 선언이 맞아도 재담금질 0 · 보류 · 파일 그대로
    dl_cases = {}
    for nm_, how in (("plan_gone", lambda d: (d / "plan.json").unlink()),
                     ("tmp_only", lambda d: (d / real.MD_DONE_NAME).rename(d / real.MD_DONE_TMP)),
                     ("end_no_marker", lambda d: (d / real.MD_DONE_NAME).unlink())):
        c_x = clone(c_m); (c_x / "STOP.json").unlink(missing_ok=True)
        fc_ = c_x / "B/seed13.fire_cut"; how(fc_)
        snap = lambda: {p_.name: hashlib.sha256(p_.read_bytes()).hexdigest() for p_ in sorted(fc_.iterdir())}
        before = snap()
        rc_x, L_x, _ = go(wt, rr=c_x)
        dl_cases[nm_] = (rc_x, len(L_x), "완료 단계를 못 읽는다" in J(c_x / "STOP.json")["reason"], real.folder_stage(fc_), snap() == before)
    chk(all(v_ == (RC["resume"], 0, True, "unreadable", True) for v_ in dl_cases.values()),
        f"⛔음성 DL P0 (Codex 재현): MD 완료 폴더에서 plan.json 만 지움 · 완료 기록을 임시 이름으로만 (os.replace 직전 끊김) · 기록 없이 "
        f"끝 경계까지 → 선언이 맞아도 재담금질 0 · 보류 · 폴더 파일 그대로 ({dl_cases})")
    # ⭐ 회신 DM P0-1 · P0-2 (Codex 재현) — 러너 발사 0 · 폴더 그대로 / 대조: 진짜 plan 전 판정 · 명확한 도중 끊김은 그대로 재시도
    def _post_md_gone(d):                                    # 끝까지 돈 B13 을 판정할 때 생긴 MD 뒤 산출물 (md_init_raw.xyz) — 도중 끊김 폴더엔 없다
        (d / real.SEED_GATE_RAW).unlink(missing_ok=True)
    def _strip_raw(d):
        for x_ in ("plan.json", "traj.xyz", "thermo.csv", real.MD_DONE_NAME, real.SEED_GATE_RAW):
            (d / x_).unlink(missing_ok=True)
    def _cut_front(d, keep=2):
        _post_md_gone(d)
        (d / real.MD_DONE_NAME).unlink(missing_ok=True)
        tl = (d / "traj.xyz").read_text(encoding="utf-8").splitlines(keepends=True); fr_ = int(tl[0]) + 2
        (d / "traj.xyz").write_text("".join(tl[:keep * fr_]), encoding="utf-8")
        th_ = (d / "thermo.csv").read_text(encoding="utf-8").splitlines(keepends=True)
        (d / "thermo.csv").write_text("".join(th_[:1 + keep]), encoding="utf-8")
        return th_
    def _keep_attempt_only(d):                               # 진짜 plan 전 끊김 — 실행 전 기록만 (pass 였던 폴더의 이력까지 지운다)
        for p_ in list(d.iterdir()):
            if p_.name != real.ATTEMPT_NAME:
                p_.unlink()
    def _end_row(d):
        th_ = _cut_front(d); open(d / "thermo.csv", "a", encoding="utf-8").write(th_[-1])
    def _frames_only(d, as_str):                             # 회신 DN P1 재현 — thermo 없음 · 궤적 완주 · FIRE 미완 폴더를 진짜 판정 → 완료 기록 · 궤적 꼬리 소실
        (d / "thermo.csv").unlink(); _post_md_gone(d)
        _note_md_judge(_judge_as_seed(d, "selftest — thermo 없음 · 궤적 완주 · FIRE 미완 판정"), kind="frames")
        (d / real.MD_DONE_NAME).unlink()
        tl = (d / "traj.xyz").read_text(encoding="utf-8").splitlines(keepends=True); fr_ = int(tl[0]) + 2
        (d / "traj.xyz").write_text("".join(tl[:2 * fr_]), encoding="utf-8")
        if as_str:
            _n_to_str(d)
    dm_cases, dm_ctrl = {}, {}
    for nm_, how, ctrl in (("end_row_kept", _end_row, False),
                           ("noplan_hist_pass", lambda d: (_strip_raw(d), dm_stage(d, "noplan_hist_pass")), False),
                           ("noplan_vtmp_pass", lambda d: (_strip_raw(d), dm_stage(d, "noplan_vtmp_pass")), False),
                           ("judged_md_then_cut", lambda d: (_note_md_judge(_judge_as_seed(d, "selftest — MD 완료 · FIRE 미완 판정")),
                                                             _cut_front(d)), False),
                           ("frames_only_int", lambda d: _frames_only(d, as_str=False), False),   # 회신 DN P1 표 첫 줄 (정상 타입 → 보류)
                           # DO 전 리뷰 (소비자 P1 t7) — 완주한 thermo · traj 에 NUL 꼬리 → 진짜 판정이 일정 끝 · 프레임 다 참을 그대로 적는다 → 꼬리 소실 뒤 보류
                           ("nul_tails_judged", lambda d: (_post_md_gone(d), open(d / "thermo.csv", "ab").write(b"\x00" * 64),
                                                           open(d / "traj.xyz", "ab").write(b"\x00" * 64),
                                                           _note_md_judge(_judge_as_seed(d, "selftest — NUL 꼬리 · MD 완료 · FIRE 미완 판정")),
                                                           _cut_front(d)), False),
                           ("frames_only_strn", lambda d: _frames_only(d, as_str=True), False),   # 회신 DN P1 반례 (n:"130" → 보류)
                           # ⭐ DO 전 리뷰 F1 — 판정 · final · 완료 기록 · 꼬리가 다 사라져도 MD 뒤 산출물 (md_init_raw.xyz · 일정 끝 시각) 이 남으면 보류
                           ("post_md_file_kept", lambda d: (shutil.copy(d / real.SEED_GATE_RAW, d.parent / "_raw_keep"), _cut_front(d),
                                                            shutil.move(str(d.parent / "_raw_keep"), str(d / real.SEED_GATE_RAW))), False),
                           ("ctrl_noplan_judged", lambda d: (_keep_attempt_only(d), dm_stage(d, "noplan_judged")), True),
                           ("ctrl_mid_cut", lambda d: _cut_front(d), True)):
        c_x = clone(c_m); (c_x / "STOP.json").unlink(missing_ok=True)
        fc_ = c_x / "B/seed13.fire_cut"; how(fc_)
        snap = lambda: {p_.name: hashlib.sha256(p_.read_bytes()).hexdigest() for p_ in sorted(fc_.iterdir())}
        before, st0 = snap(), real.folder_stage(fc_)
        rc_x, L_x, _ = go(wt, rr=c_x)
        sp_ = J(c_x / "STOP.json") if (c_x / "STOP.json").is_file() else {}
        held_ = any(w_ in (sp_.get("reason") or "") for w_ in ("완료 단계를 못 읽는다", "과학적 판정", "판정을 못 읽는다"))
        (dm_ctrl if ctrl else dm_cases)[nm_] = (rc_x if not held_ else "held", len(L_x), held_, st0, snap() == before)
    chk(all(v_ == ("held", 0, True, "unreadable", True) for v_ in dm_cases.values())
        and dm_ctrl["ctrl_noplan_judged"][:2] == (0, 1) and dm_ctrl["ctrl_noplan_judged"][3] == "no_plan"
        and dm_ctrl["ctrl_mid_cut"][:2] == (0, 1) and dm_ctrl["ctrl_mid_cut"][3] == "md_incomplete"
        and all(v_[4] for v_ in dm_ctrl.values()),
        f"⛔음성 DM P0-1 · P0-2 (Codex 재현): 궤적 앞부분 + thermo 에 온전한 끝 시각 행 · pass 판정이 있던 폴더를 원자료 소실 뒤 재판정 · "
        f"pass 판정이 임시 파일에만 · (같은 갈래) MD 완료 · FIRE 미완 폴더를 진짜 판정한 뒤 완료 기록 · 꼬리 소실 · (회신 DN P1) thermo 없는 "
        f"폴더의 같은 판정 — 프레임 수 정수 그대로 · n 만 글자로 → 선언이 맞아도 재담금질 0 · "
        f"보류 · 폴더 그대로 / 대조: 진짜 plan 전 판정만 · 명확한 도중 끊김 → 재시도 1 · rc 0 ({dm_cases} · {dm_ctrl})")
    rc_w1, L_w1, rr_w = go(wt, scen={("B", 12): {"raise_on_poll": 3, "polls": 6}})
    sw1 = J(rr_w / "STOP.json")
    (rr_w / "B/seed12").rename(rr_w / "B/seed12.int1")
    led_w = J(rr_w / "stage1_ledger.json")
    led_w.setdefault("stop_history", []).append({**sw1, "run_id": "0" * 32, "acked_at": "t", "declaration": DECL(OUT)})
    _write_json_atomic(rr_w / "stage1_ledger.json", led_w); (rr_w / "STOP.json").unlink()
    rc_w2, L_w2, _ = go(wt, rr=rr_w)
    chk(rc_w2 == RC["resume"] and not L_w2 and "묶여 확인" in J(rr_w / "STOP.json")["reason"],
        "⛔음성 정전 복구: 확인된 STOP (선언 포함) 이 다른 run_id 에 묶여 있으면 다시 안 돌린다")
    # 회신 DJ P0-2 (Codex 재현 두 경로) — 끊긴 보존 폴더의 판정 파일이 잘림 · invalid 폴더를 run_root 밖으로
    rc_v1, L_v1, rr_v1 = go(wt, scen={("B", 12): {"raise_on_poll": 3, "polls": 6}})
    sv1 = J(rr_v1 / "STOP.json"); (rr_v1 / "B/seed12").rename(rr_v1 / "B/seed12.int")
    (rr_v1 / "B/seed12.int/stage1_verdict.json").write_text('{"status": "inc', encoding="utf-8")
    rc_v2, L_v2, _ = go(wt, rr=rr_v1, ack=sv1["stop_id"], declare=OUT)
    rc_x1, L_x1, rr_x1 = go(wt, scen={("A", 11): {"melt": "species_swap", "polls": 8}})
    sx1 = J(rr_x1 / "STOP.json")
    shutil.move(str(rr_x1 / "A/seed11"), str(rr_x1.parent / (rr_x1.name + "_outside_seed11")))
    rc_x2, L_x2, _ = go(wt, rr=rr_x1, ack=sx1["stop_id"], declare=FIX)
    su3 = J(rr_u2 / "STOP.json")                             # 한도 멈춤 (code invalid · 끊긴 런에 묶임) 을 원인 고침 선언으로 확인 → 종류가 안 맞아 거부
    rc_v3, L_v3, _ = go(wt, rr=rr_u2, ack=su3["stop_id"], declare=FIX)
    chk(su3["code"] == "invalid" and rc_v3 == RC["refused"] and not L_v3 and J(rr_u2 / "STOP.json")["stop_id"] == su3["stop_id"],
        "⛔음성 DJ Q1: 확인 때 영수증 종류는 멈춤 code 가 아니라 그 실행에서 정한다 — 끊긴 런에 묶인 invalid 멈춤 (한도) 에 '원인 고침' 선언 → 거부 (STOP 그대로)")
    chk(rc_v2 == RC["refused"] and not L_v2 and J(rr_v1 / "STOP.json")["stop_id"] == sv1["stop_id"]
        and rc_x1 == RC["invalid"] and rc_x2 == RC["invalid"] and not L_x2 and "보존 누락" in J(rr_x1 / "STOP.json")["reason"],
        "⛔음성 DJ P0-2 (Codex 재현): 끊긴 B12 보존 폴더의 판정 파일이 잘리면 '판정 없음' 으로 읽지 않고 확인 단계에서 선언을 거부 (STOP 그대로) · 기술적 invalid A11 폴더를 "
        "run_root 밖으로 옮기면 invalid 런이어도 다시 안 돌린다 (장부 → 폴더 대조 · 발사 0)")
    # 회신 DJ P0-2 끝 — 끝까지 돈 기술적 invalid 런은 다시 판정 못 하는 이유를 선언해야 재담금질
    rc_f5, L_f5, rr_f5 = go(wt, scen={("A", 12): {"final": "five"}})
    sf5 = J(rr_f5 / "STOP.json")
    (rr_f5 / "A/seed12").rename(rr_f5 / "A/seed12.invalid_five")
    rc_f6, L_f6, _ = go(wt, rr=rr_f5, ack=sf5["stop_id"], declare=FIX)
    still_f = J(rr_f5 / "STOP.json")["stop_id"] == sf5["stop_id"]
    rc_f7, L_f7, _ = go(wt, rr=rr_f5, ack=sf5["stop_id"],
                        declare={**FIX, "rejudge_impossible_reason": "final.xyz 원자 5 개 — 원시 traj 마지막 프레임에서 FIRE 를 다시 해야 한다 (selftest)"})
    chk(rc_f5 == RC["invalid"] and sf5.get("run_id") and rc_f6 == RC["refused"] and not L_f6 and still_f and rc_f7 == 0 and len(L_f7) == 8
        and J(rr_f5 / "stage1_summary.json")["track"] == "stage1_pass",
        "⛔음성 DJ P0-2: 끝까지 돈 invalid 런 (final.xyz 5 원자) 은 '다시 판정 못 하는 이유' 없이는 재시도 선언을 안 받고 (STOP 그대로) · 이유를 적으면 "
        "다시 돌아 1 단계를 마친다")
    # 회신 DJ P0-1 (소비자) — 모든 면에서 맞는 이력 (양성 대조) 에서 한 가지씩만 깬다
    def hist_case(prevs, mut=None):
        c = clone(rr_d)
        ids = with_history(c, "B", 13, prevs)
        if mut:
            mut(c, ids)
        return c, summ(c)
    def strip_ledger(c, ids):                                # Codex 재현 1: 장부의 재시도 필드 · STOP 이력을 지운다
        l_ = J(c / "stage1_ledger.json")
        for r in l_["runs"]:
            for f_ in ("retry_of", "retry_kind", "retry_stop_id"):
                r.pop(f_, None)
        l_["stop_history"] = []
        _write_json_atomic(c / "stage1_ledger.json", l_)
    def strip_all(c, ids):                                   # 실행 전 기록까지 같이 지운다 (장부와 맞춰서)
        strip_ledger(c, ids)
        for d in (c / "B").glob("seed13*"):
            a_ = J(d / real.ATTEMPT_NAME)
            a_.update(retry_of=None, retry_kind=None, retry_stop_id=None)
            _write_json_atomic(d / real.ATTEMPT_NAME, a_)
    def strip_kind(c, ids):                                  # Codex 재현 2: 두 번 재시도에서 retry_kind 만 지운다 (장부 · 실행 전 기록 둘 다)
        l_ = J(c / "stage1_ledger.json")
        for r in l_["runs"]:
            r.pop("retry_kind", None)
        _write_json_atomic(c / "stage1_ledger.json", l_)
        for d in (c / "B").glob("seed13*"):
            a_ = J(d / real.ATTEMPT_NAME); a_.pop("retry_kind", None); _write_json_atomic(d / real.ATTEMPT_NAME, a_)
    def att_mismatch(c, ids):
        a_ = J(c / "B/seed13" / real.ATTEMPT_NAME); a_["retry_of"] = None; _write_json_atomic(c / "B/seed13" / real.ATTEMPT_NAME, a_)
    def att_gone(c, ids):
        (c / "B/seed13.prev0" / real.ATTEMPT_NAME).unlink()
    def wrong_kind(c, ids):                                  # retry_kind 만 틀림 (장부 · 실행 전 기록 둘 다 맞춰서) — 그 대조만 잡는다
        l_ = J(c / "stage1_ledger.json")
        for r in l_["runs"]:
            if r.get("retry_of"):
                r["retry_kind"] = "invalid"
        _write_json_atomic(c / "stage1_ledger.json", l_)
        a_ = J(c / "B/seed13" / real.ATTEMPT_NAME); a_["retry_kind"] = "invalid"; _write_json_atomic(c / "B/seed13" / real.ATTEMPT_NAME, a_)
    def rebind(c, ids):
        l_ = J(c / "stage1_ledger.json"); l_["stop_history"][-1]["run_id"] = "0" * 32; _write_json_atomic(c / "stage1_ledger.json", l_)
    def cut_verdict(c, ids):
        (c / "B/seed13.prev0/stage1_verdict.json").write_text('{"status": "pa', encoding="utf-8")
    def move_out(c, ids):
        shutil.move(str(c / "B/seed13.prev0"), str(c.parent / "outside_prev0"))
    s_ok1 = hist_case([{"decl": OUT}])[1]
    c_two, s_two = hist_case([{"decl": OUT}, {"decl": OUT}])
    s_two_k = hist_case([{"decl": OUT}, {"decl": OUT}], strip_kind)[1]
    c_sl, s_sl = hist_case([{"decl": OUT}], strip_ledger)
    s_sa = hist_case([{"decl": OUT}], strip_all)[1]
    s_am = hist_case([{"decl": OUT}], att_mismatch)[1]
    s_ag = hist_case([{"decl": OUT}], att_gone)[1]
    s_nd = hist_case([{"decl": None}])[1]
    s_rb = hist_case([{"decl": OUT}], rebind)[1]
    s_wk = hist_case([{"decl": OUT}], wrong_kind)[1]
    s_cv = hist_case([{"decl": OUT}], cut_verdict)[1]
    s_mo = hist_case([{"decl": OUT}], move_out)[1]
    s_mc = hist_case([{"decl": OUT, "stage": "md_complete"}])[1]
    s_dlnp = hist_case([{"decl": OUT, "stage": "md_complete_noplan"}])[1]     # 회신 DL P0 반례 1 — 소비자도 같은 판독
    s_dltp = hist_case([{"decl": OUT, "stage": "md_tmp"}])[1]                 # 회신 DL P0 반례 2
    s_dlen = hist_case([{"decl": OUT, "stage": "end_no_marker"}])[1]          # 회신 DL Q2 — 기록 없이 끝 경계
    s_dmer = hist_case([{"decl": OUT, "stage": "end_row_kept"}])[1]           # 회신 DM P0-1 — 남은 끝 시각
    s_dmhp = hist_case([{"decl": OUT, "stage": "noplan_hist_pass"}])[1]       # 회신 DM P0-2 반례 1
    s_dmvt = hist_case([{"decl": OUT, "stage": "noplan_vtmp_pass"}])[1]       # 회신 DM P0-2 반례 2
    s_dmjd = hist_case([{"decl": OUT, "stage": "noplan_judged"}])[1]          # 대조 — 진짜 plan 전 판정만
    s_dmjm = hist_case([{"decl": OUT, "stage": "judged_md_then_cut"}])[1]     # 같은 갈래 — 진짜 판정의 MD 완료 흔적 뒤 꼬리 소실
    s_dnfs = hist_case([{"decl": OUT, "stage": "judged_frames_strn"}])[1]     # 회신 DN P1 — 완료 흔적의 n 이 글자
    s_fn = hist_case([{"decl": OUT, "stage": "final"}])[1]
    s_ivn = hist_case([{"kind": "invalid", "stage": "final", "status": "ended", "rc": 0, "decl": FIX}])[1]
    s_ivy = hist_case([{"kind": "invalid", "stage": "final", "status": "ended", "rc": 0,
                        "decl": {**FIX, "rejudge_impossible_reason": "final.xyz 깨짐 (selftest)"}}])[1]
    s_cpo = hist_case([{"status": "cap", "rc": "killed_cap", "code": "cap", "decl": OUT}])[1]
    c_fo, s_fo = hist_case([{"kind": "invalid", "ledger_verdict": False, "decl": FIX}])     # 회신 DK P0-2 — 판정이 폴더에만
    c_lb, s_lb = hist_case([{"kind": "invalid", "decl": FIX}])                             # 같은 판정이 장부에도
    rc_sl, L_sl, _ = go(wt, rr=c_sl)
    got_c = {"ok": s_ok1["track"], "two": inv_(s_two, "한도"), "two_kind": inv_(s_two_k, "한도"), "strip_ledger": inv_(s_sl, "retry_of"),
             "strip_all": inv_(s_sa, "retry_of"), "att_mismatch": inv_(s_am, real.ATTEMPT_NAME), "att_gone": inv_(s_ag, real.ATTEMPT_NAME),
             "no_decl": inv_(s_nd, "재시도 선언"), "rebind": inv_(s_rb, "묶여 확인된"), "wrong_kind": inv_(s_wk, "retry_kind"),
             "cut_verdict": inv_(s_cv, "못 읽는데"),
             "move_out": inv_(s_mo, "보존 누락"), "md_complete": inv_(s_mc, "MD 까지"), "final": inv_(s_fn, "끝까지"),
             "dl_noplan": inv_(s_dlnp, "완료 단계를 못 읽는데"), "dl_tmp": inv_(s_dltp, "완료 단계를 못 읽는데"),
             "dl_end": inv_(s_dlen, "완료 단계를 못 읽는데"),
             "dm_end_row": inv_(s_dmer, "완료 단계를 못 읽는데"), "dm_noplan_hist": inv_(s_dmhp, "과학적 판정"),
             "dm_noplan_vtmp": inv_(s_dmvt, "판정을 못 읽는데"), "dm_noplan_judged": s_dmjd["track"],
             "dm_judged_md": inv_(s_dmjm, "완료 단계를 못 읽는데"), "dn_frames_strn": inv_(s_dnfs, "완료 단계를 못 읽는데"),
             "invalid_final_no_reason": inv_(s_ivn, "다시 판정할 수 없다"), "invalid_final_reason": s_ivy["track"],
             "cap_run_outage_reason": inv_(s_cpo, "상한으로 멈춘 런"), "runner_on_stripped": (rc_sl, len(L_sl)),
             "same_answer_folder_vs_ledger": (s_fo["track"], s_fo["cost"]["cap_h"], s_fo["cost"]["total_h"]) == (s_lb["track"], s_lb["cost"]["cap_h"], s_lb["cost"]["total_h"])
                                            and s_fo["track"] == "stage1_pass"}
    exp_c = {"ok": "stage1_pass", "two": True, "two_kind": True, "strip_ledger": True, "strip_all": True, "att_mismatch": True, "att_gone": True,
             "no_decl": True, "rebind": True, "wrong_kind": True, "cut_verdict": True, "move_out": True, "md_complete": True, "final": True,
             "dl_noplan": True, "dl_tmp": True, "dl_end": True,
             "dm_end_row": True, "dm_noplan_hist": True, "dm_noplan_vtmp": True, "dm_noplan_judged": "stage1_pass", "dm_judged_md": True, "dn_frames_strn": True,
             "invalid_final_no_reason": True, "invalid_final_reason": "stage1_pass", "cap_run_outage_reason": True,
             "runner_on_stripped": (RC["invalid"], 0), "same_answer_folder_vs_ledger": True}
    chk(got_c == exp_c,
        "⛔음성 DJ P0-1 · P0-2 · Q1 · Q2 (소비자 · 맞는 이력에서 한 가지씩): 양성 대조 통과 · 두 번 재시도 → 한도 · retry_kind 를 지워도 한도 (앞 실행 "
        "종류로 셈) · 장부 재시도 필드 + STOP 이력 지움 · 실행 전 기록까지 지움 · 기록 불일치 · 기록 없음 · 선언 없음 · 다른 런에 묶임 · 앞 판정 "
        "잘림 · 보존 폴더 밖 · MD 완료 / 최종 뒤 재담금질 · 끝까지 돈 invalid 에 이유 없음 · 상한 런에 정전 사유 → 무효 (이유가 있으면 통과) · "
        f"지운 자료를 러너에 다시 줘도 통과 아님 · 발사 0 ({ {k: got_c[k] for k in got_c if got_c[k] != exp_c[k]} })")
    # 러너 재시도 자격 단위 (소비자와 따로 깬다)
    ue = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
    src_ = rr_d / "B/seed13"
    def ufold(name, stage="md_incomplete", verdict=None):
        d = ue / name; d.mkdir()
        if stage not in NOPLAN_STAGES:
            shutil.copy(src_ / "plan.json", d / "plan.json")
            lines = (src_ / "traj.xyz").read_text(encoding="utf-8").splitlines(keepends=True)
            fr = int(lines[0]) + 2; n_fr = len(lines) // fr
            keep = n_fr if stage in FULL_STAGES else max(1, n_fr // 3)
            (d / "traj.xyz").write_text("".join(lines[:keep * fr]), encoding="utf-8")
            th_ = (src_ / "thermo.csv").read_text(encoding="utf-8").splitlines(keepends=True)
            (d / "thermo.csv").write_text("".join(th_[:1 + keep]), encoding="utf-8")       # traj 와 같은 행 수 (회신 DL)
            if stage in ("md_complete", "final", "md_complete_noplan", "md_tmp"):
                pl_u = J(d / "plan.json"); n_pl = real.planned_md_steps(pl_u)
                real.write_md_done(d, run_id=pl_u["run_id"], n_steps_planned=n_pl, n_steps_done=n_pl)
            if stage == "md_tmp":
                (d / real.MD_DONE_NAME).rename(d / real.MD_DONE_TMP)
            if stage == "md_complete_noplan":
                (d / "plan.json").unlink()
            if stage == "final":
                shutil.copy(src_ / "final.xyz", d / "final.xyz")
            if stage == "unreadable":
                (d / "plan.json").write_text('{"melt', encoding="utf-8")
        dm_stage(d, stage, th_full=(src_ / "thermo.csv").read_text(encoding="utf-8").splitlines(keepends=True), src_full=src_)
        if verdict is not None:
            (d / "stage1_verdict.json").write_text(verdict, encoding="utf-8")
        return {"path": str(d)}
    R0, R1 = "9" * 32, "7" * 32
    run0 = lambda **k: {"run_id": R0, "end": "t", "cost_basis": "measured",
                        "status": "ended" if k.get("verdict") == "invalid" else "interrupted", **k}
    rcpt = lambda code="interrupted", decl=OUT, rid=R0: [{"stop_id": "u1", "code": code, "run_id": rid, "acked_at": "t",
                                                         **({"declaration": DECL(decl)} if decl else {})}]
    E = lambda atts, hist_, inv: retry_eligibility(atts, hist_, inv, vals_t, real)
    INV = '{"status": "invalid"}'
    cases = {
        "ok": E([run0()], rcpt(), {R0: ufold("ok")}),
        "no_plan_ok": E([run0()], rcpt(), {R0: ufold("np", stage="no_plan")}),
        "ledger_fail": E([run0(verdict="fail")], rcpt(), {R0: ufold("lf")}),
        "ledger_fail_no_folder": E([run0(verdict="fail")], rcpt(), {}),        # 장부의 과학적 판정은 폴더가 없어도 먼저 막는다
        "missing_invalid": E([run0(verdict="invalid")], rcpt("invalid", FIX), {}),
        "folder_pass": E([run0()], rcpt(), {R0: ufold("fp", verdict='{"status": "pass"}')}),
        "folder_cut": E([run0()], rcpt(), {R0: ufold("fc", verdict='{"status": "in')}),
        "cost": E([run0(cost_basis="unknown")], rcpt(), {R0: ufold("co")}),
        "stage_bad": E([run0()], rcpt(), {R0: ufold("sb", stage="unreadable")}),
        "final": E([run0()], rcpt(), {R0: ufold("fi", stage="final")}),
        "fire": E([run0()], rcpt(), {R0: ufold("mc", stage="md_complete")}),
        "no_receipt": E([run0()], [], {R0: ufold("nr")}),
        "no_decl": E([run0()], rcpt(decl=None), {R0: ufold("nd")}),
        "other_run": E([run0()], rcpt(rid="8" * 32), {R0: ufold("or")}),
        "unacked": E([run0()], [{**rcpt()[0], "acked_at": None}], {R0: ufold("ua")}),
        "inv_needs_rejudge": E([run0(verdict="invalid")], rcpt("invalid", FIX), {R0: ufold("ir", stage="md_complete", verdict=INV)}),
        "inv_rejudge_ok": E([run0(verdict="invalid")], rcpt("invalid", {**FIX, "rejudge_impossible_reason": "x"}), {R0: ufold("io", stage="md_complete", verdict=INV)}),
        "inv_wrong_code": E([run0(verdict="invalid")], rcpt("resume", FIX), {R0: ufold("iw", verdict=INV)}),
        "inv_outage_reason": E([run0(verdict="invalid")], rcpt("invalid", OUT), {R0: ufold("iu", verdict=INV)}),
        "cap_outage": E([run0(status="cap")], rcpt("cap", OUT), {R0: ufold("ca")}),
        "cap_raise": E([run0(status="cap")], rcpt("cap", {**OUT, "retry_reason": "budget_cap_raised"}), {R0: ufold("cr")}),
        "two": E([run0(), run0(run_id=R1)], [{**rcpt(rid=R1)[0], "stop_id": "u2"}], {R0: ufold("t0"), R1: ufold("t1")}),
        "inv_then_int": E([run0(verdict="invalid"), run0(run_id=R1)], [{**rcpt(rid=R1)[0], "stop_id": "u3"}],
                          {R0: ufold("v0", verdict=INV), R1: ufold("v1")}),
        # ⭐ 회신 DL P0 · Q2 — 완료 증거가 남은 폴더 (plan 만 없음 · 임시 기록만 · 기록 없이 끝 경계) 는 선언이 맞아도 보류
        "dl_noplan_done": E([run0()], rcpt(), {R0: ufold("dn", stage="md_complete_noplan")}),
        "dl_tmp": E([run0()], rcpt(), {R0: ufold("dt", stage="md_tmp")}),
        "dl_end": E([run0()], rcpt(), {R0: ufold("de", stage="end_no_marker")}),
        "dl_inv_tmp": E([run0(verdict="invalid")], rcpt("invalid", FIX), {R0: ufold("di", stage="md_tmp", verdict=INV)}),
        # ⭐ 회신 DM P0-1 · P0-2 — 남은 끝 시각 · 판정 기록의 완료 흔적은 보류 / 대조: 진짜 plan 전 판정만 있는 폴더는 재시도
        "dm_end_row": E([run0()], rcpt(), {R0: ufold("me", stage="end_row_kept")}),
        "dm_noplan_hist": E([run0()], rcpt(), {R0: ufold("mh", stage="noplan_hist_pass")}),
        "dm_noplan_vtmp": E([run0()], rcpt(), {R0: ufold("mt", stage="noplan_vtmp_pass")}),
        "dm_noplan_judged": E([run0()], rcpt(), {R0: ufold("mj", stage="noplan_judged")}),
        "dm_judged_md": E([run0()], rcpt(), {R0: ufold("mk", stage="judged_md_then_cut")}),   # 같은 갈래 — 판정의 MD 완료 흔적
        "dn_frames_strn": E([run0()], rcpt(), {R0: ufold("mn", stage="judged_frames_strn")}),   # 회신 DN P1 — 흔적의 n 이 글자
    }
    exp_u = {"ok": (True, None), "no_plan_ok": (True, None), "ledger_fail": (False, "invalid"), "ledger_fail_no_folder": (False, "invalid"),
             "missing_invalid": (False, "resume"),
             "folder_pass": (False, "invalid"), "folder_cut": (False, "invalid"), "cost": (False, "resume"), "stage_bad": (False, "resume"),
             "final": (False, "resume"), "fire": (False, "resume"), "no_receipt": (False, "resume"), "no_decl": (False, "resume"),
             "other_run": (False, "resume"), "unacked": (False, "resume"), "inv_needs_rejudge": (False, "invalid"), "inv_rejudge_ok": (True, None),
             "inv_wrong_code": (False, "invalid"), "inv_outage_reason": (False, "invalid"), "cap_outage": (False, "resume"),
             "cap_raise": (True, None), "two": (False, "invalid"), "inv_then_int": (True, None),
             "dl_noplan_done": (False, "resume"), "dl_tmp": (False, "resume"), "dl_end": (False, "resume"), "dl_inv_tmp": (False, "resume"),
             "dm_end_row": (False, "resume"), "dm_noplan_hist": (False, "invalid"), "dm_noplan_vtmp": (False, "invalid"),
             "dm_noplan_judged": (True, None), "dm_judged_md": (False, "resume"), "dn_frames_strn": (False, "resume")}
    got_u = {k: (v["ok"], v["code"]) for k, v in cases.items()}
    chk(got_u == exp_u and "한도" in cases["two"]["why"] and "FIRE" in cases["fire"]["why"] and "못 찾는다" in cases["missing_invalid"]["why"]
        and "못 읽는다" in cases["folder_cut"]["why"] and "선언 문제" in cases["no_decl"]["why"] and cases["ok"]["kind"] == "interrupted"
        and cases["inv_rejudge_ok"]["kind"] == "invalid" and cases["inv_then_int"]["retry_of"] == R1
        and all("완료 단계를 못 읽는다" in cases[k]["why"] for k in ("dl_noplan_done", "dl_tmp", "dl_end", "dl_inv_tmp"))
        and "임시" in cases["dl_tmp"]["why"] and "끝 경계" in cases["dl_end"]["why"] and "plan.json 없이" in cases["dl_noplan_done"]["why"],
        "⛔음성 DJ (러너 재시도 자격 단위): 과학적 판정 · 보존 누락 (invalid 런 포함) · 폴더 판정 pass · 판정 잘림 · 비용 미확정 · 단계 판독 불가 · "
        "최종 (판정하라) · MD 완료 (FIRE 보류) · 영수증 없음 · 선언 없음 · 다른 런 · 확인 안 됨 · 다시 판정 못 하는 이유 없음 · invalid 에 "
        "resume 영수증 · invalid 에 정전 사유 · 상한 런에 정전 사유 · 두 번 끊김 (한도) · **완료 폴더에서 plan 만 없음 · 임시 기록만 · "
        "기록 없이 끝 경계 · invalid 런의 임시 기록 (회신 DL)** → 거부 / 맞으면 통과 (plan 전 끊김 · 상한 사유 · "
        f"invalid 다음 끊김 1 회) ({ {k: got_u[k] for k in got_u if got_u[k] != exp_u[k]} })")
    want_mj = {"full": ("incomplete", True, True), "frames": ("incomplete", False, True)}
    chk(sum(x_[0] == "full" for x_ in md_judged) >= 3 and sum(x_[0] == "frames" for x_ in md_judged) >= 4
        and all(x_[1:] == want_mj[x_[0]] for x_ in md_judged) and "MD 가 끝났던 흔적" in (cases["dm_judged_md"]["why"] or "")
        and "n 타입이 str" in (cases["dn_frames_strn"]["why"] or ""),
        "⛔ fixture 뜻 (같은 갈래 · 회신 DN P1): 진짜 판정 함수가 'MD 완료 · FIRE 미완' 폴더에 낸 판정은 incomplete · 일정 끝 · 프레임 다 참 · "
        "thermo 없는 폴더면 incomplete · 프레임 다 참 (일정 없음) 이다 · n 이 글자면 타입 오류로 보류한다 "
        f"— 그 흔적이 남은 채 완료 기록 · 꼬리가 사라지면 러너 · 재시도 자격 · 소비자가 보류 ({md_judged} · {(cases['dm_judged_md']['why'] or '')[:160]})")
    # 확인 때 선언 검사 단위 (ack_declaration_problems) — 종류는 실행에서 · code 는 그 종류의 묶는 code · 상한 규칙 · 다시 판정 못 하는 이유
    ar = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
    def afold(name, rid_, stage="md_incomplete", verdict=None):
        d = ar / "A" / name
        d.parent.mkdir(parents=True, exist_ok=True)
        info = ufold("ack_" + name, stage=stage, verdict=verdict)
        shutil.copytree(info["path"], d)
        _write_json_atomic(d / real.ATTEMPT_NAME, {"system": "A", "seed": 11, "run_id": rid_, "retry_of": None, "retry_stop_id": None, "retry_kind": None})
    RA, RB, RC_, RD = "1" * 32, "2" * 32, "3" * 32, "4" * 32
    RE_, RF_ = "6" * 32, "8" * 32
    afold("seed11.a", RA); afold("seed11.b", RB, verdict=INV); afold("seed11.c", RC_, stage="final", verdict=INV); afold("seed11.d", RD)
    afold("seed11.e", RE_, verdict='{"status": "pass"}'); afold("seed11.f", RF_, verdict='{"status": "in')
    led_a = {"runs": [{"run_id": RA, "status": "interrupted"}, {"run_id": RB, "status": "invalid", "verdict": "invalid"},
                      {"run_id": RC_, "status": "ended", "verdict": "invalid"}, {"run_id": RD, "status": "cap"},
                      {"run_id": RE_, "status": "interrupted"}, {"run_id": RF_, "status": "interrupted"}]}
    A_ = lambda decl, code, rid_: ack_declaration_problems(DECL(decl), {"run_id": rid_, "code": code}, led_a, vals_t, real, ar)
    ack_cases = {"no_run": bool(ack_declaration_problems(DECL(OUT), {"code": "resume"}, led_a, vals_t, real, ar)),
                 "unknown_run": bool(A_(OUT, "resume", "5" * 32)),
                 "int_run_invalid_code": bool(A_(FIX, "invalid", RA)), "inv_run_resume_code": bool(A_(FIX, "resume", RB)),
                 "inv_run_ok": bool(A_(FIX, "invalid", RB)), "inv_final_no_reason": bool(A_(FIX, "invalid", RC_)),
                 "inv_final_reason": bool(A_({**FIX, "rejudge_impossible_reason": "x"}, "invalid", RC_)),
                 "int_run_ok": bool(A_(OUT, "interrupted", RA)), "cap_run_outage": bool(A_(OUT, "cap", RD)),
                 "cap_run_raise": bool(A_({**OUT, "retry_reason": "budget_cap_raised"}, "cap", RD)),
                 "folder_pass_run": bool(A_(OUT, "interrupted", RE_)), "folder_cut_run": bool(A_(OUT, "interrupted", RF_))}
    exp_a = {"no_run": True, "unknown_run": True, "int_run_invalid_code": True, "inv_run_resume_code": True, "inv_run_ok": False,
             "inv_final_no_reason": True, "inv_final_reason": False, "int_run_ok": False, "cap_run_outage": True, "cap_run_raise": False,
             "folder_pass_run": True, "folder_cut_run": True}
    chk(ack_cases == exp_a,
        "⛔음성 DJ Q1 (확인 때 선언 검사 단위): run_id 없음 · 장부에 없는 런 · 끊긴 런에 invalid code · invalid 런에 resume code · 끝까지 돈 invalid 런에 "
        f"이유 없음 · 상한 런에 정전 사유 → 문제 / 맞는 조합은 통과 ({ {k: ack_cases[k] for k in ack_cases if ack_cases[k] != exp_a[k]} })")
    # 회신 DK (카드 v3) — 정전 손실은 상한을 늘리지 않는다: 러너 사전 검사 · 소비자 모두 카드 상한 그대로
    wt_c = mk_wt(card=mk_card(stage1_cap_gpu_h=50.5))
    rc_q1, L_q1, rr_q = go(wt_c, seed_worst_h=5.0, scen={("B", 12): {"raise_on_poll": 3, "polls": 6}})
    sq = J(rr_q / "STOP.json"); (rr_q / "B/seed12").rename(rr_q / "B/seed12.int")
    rc_q2, L_q2, _ = go(wt_c, rr=rr_q, seed_worst_h=5.0, ack=sq["stop_id"], declare=OUT)
    sq2 = J(rr_q / "STOP.json")
    lc_q = real.ledger_check(rr_q, {}, real.read_li2s2_values(wt_c / CARD_REL))
    chk(rc_q1 == RC["interrupted"] and rc_q2 == RC["cap"] and len(L_q2) == 6 and sq2["code"] == "cap" and sq2["cap_h"] == 50.5
        and lc_q["cap_h"] == 50.5,
        f"⛔음성 DK (카드 v3): 카드 상한 50.5 h 에서 B12 가 정전으로 2 h 를 잃어도 상한은 50.5 그대로 — 러너가 마지막 시드 (B15) 를 안 띄우고 미완결 · "
        f"소비자 상한도 50.5 (발사 {len(L_q2)} · STOP cap_h {sq2.get('cap_h')} · 소비자 {lc_q['cap_h']})")
    # 회신 DJ P0-3 · Q3 · P1-4 — 증언 상한: 하한 검증 · 근거 필드 · 잠금 안에서 읽기 · 검사 · 쓰기
    def orphan_root(lower, hb=5.0):
        rr_ = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
        rid_ = uuid.uuid4().hex
        (rr_ / "A/seed11").mkdir(parents=True)
        _write_json_atomic(rr_ / "A/seed11" / real.ATTEMPT_NAME, {"system": "A", "seed": 11, "run_id": rid_, "retry_of": None,
                                                                "retry_stop_id": None, "retry_kind": None})
        _write_json_atomic(rr_ / "stage1_ledger.json", {"runs": [{"system": "A", "seed": 11, "run_id": rid_, "start": "t",
            "start_epoch": time.time() - 7200, "pgid": 4243, "status": "orphaned", "end": "t", "wall_h": None, "wall_h_so_far": hb,
            "wall_h_lower": lower, "rc": "unknown_runner_died", "cost_basis": "unknown"}], "stop_history": []})
        return rr_, rid_
    res_lb = {}
    for nm_, lo_ in (("null", None), ("nan", float("nan")), ("neg", -1.0), ("below_heartbeat", 4.0)):
        rr_, rid_ = orphan_root(lo_)
        before = (rr_ / "stage1_ledger.json").read_bytes()
        res_lb[nm_] = ([attest_cost(rr_, rid_, vals_t, hours=h_, fields=ATT)[0] for h_ in (0.0, 6.0)],
                       (rr_ / "stage1_ledger.json").read_bytes() == before)
    rr_g0, rid_g0 = orphan_root(0.0, hb=0.0)                # 첫 heartbeat 전에 끊긴 런 — 하한 0 이어도 0 h 는 상한이 아니다
    rc_g00, _ = attest_cost(rr_g0, rid_g0, vals_t, hours=0.0, fields=ATT)
    rc_g05, _ = attest_cost(rr_g0, rid_g0, vals_t, hours=0.5, fields=ATT)
    rr_g5, rid_g5 = orphan_root(5.0)
    rc_z, _ = attest_cost(rr_g5, rid_g5, vals_t, hours=0.0, fields=ATT)
    rc_g, _ = attest_cost(rr_g5, rid_g5, vals_t, hours=6.0, fields=ATT)
    eg5 = J(rr_g5 / "stage1_ledger.json")["runs"][0]
    chk(all(x == ([10, 10], True) for x in res_lb.values()) and rc_z == 10 and rc_g == 0 and eg5["cost_basis"] == "attested_upper_bound"
        and rc_g00 == 10 and rc_g05 == 0
        and eg5["attestation"]["lower_at_attest"] == 5.0 and eg5["attestation"]["heartbeat_at_attest"] == 5.0 and eg5["attestation"]["confirmer"] == "selftest",
        f"⛔음성 DJ P0-3 (Codex 재현): 하한이 null · NaN · −1 · heartbeat 미만이면 0 h · 6 h 어느 증언도 안 받고 장부를 안 건드린다 (비용 미확정 그대로) · "
        f"하한이 맞으면 0 h 는 거부 · 6 h 는 받고 증언 때 하한 · heartbeat 를 같이 적는다 ({res_lb})")
    def attested_bad(lo_, w_=0.0, status="orphaned", hb_at=5.0, hb=5.0):
        c = clone(rr_d)
        l_ = J(c / "stage1_ledger.json")
        l_["runs"][0].update(status=status, cost_basis="attested_upper_bound", wall_h=w_, wall_h_so_far=hb, wall_h_lower=lo_,
                             attestation={**ATT, "confirmed_at": "t", "lower_at_attest": lo_, "heartbeat_at_attest": hb_at})
        _write_json_atomic(c / "stage1_ledger.json", l_)
        return summ(c)
    sb_ = [attested_bad(x) for x in (None, float("nan"), -1.0)]
    s_good0, s_good6, s_ended = attested_bad(5.0), attested_bad(5.0, 6.0), attested_bad(5.0, 6.0, status="ended")
    s_hbat = attested_bad(5.0, 6.0, hb_at=3.0)                # 증언 때 적은 heartbeat 가 장부와 다름 (하한은 맞음)
    s_zero, s_half = attested_bad(0.0, 0.0, hb_at=0.0, hb=0.0), attested_bad(0.0, 0.5, hb_at=0.0, hb=0.0)   # 회신 DK P1-2 — 하한 0 에서 0 h 증언
    chk(all(inv_(x, "하한이 미상") for x in sb_) and inv_(s_good0, "하한") and s_good6["track"] == "stage1_pass" and inv_(s_ended, "고아 런")
        and inv_(s_hbat, "heartbeat") and inv_(s_zero, "양수가 아니다") and s_half["track"] == "stage1_pass",
        "⛔음성 DJ P0-3 (소비자): 증언 상한 0 h 에 하한이 null · NaN · −1 이면 비용 0 으로 통과시키지 않고 무효 · 하한이 맞아도 0 h < 하한이면 무효 · "
        "고아 런이 아닌 행 (정상 끝) 을 증언 상한으로 바꾸면 무효 · 증언 때 적은 heartbeat 가 장부와 다르면 무효 · 하한 0 에서 0 h 증언 무효 (회신 DK P1-2 · "
        "0.5 h 는 통과) (양성 대조: 하한 5 · 상한 6 h 고아 런은 통과)")
    rr_m, rid_m = orphan_root(1.5, hb=1.5)
    rcs_m = [attest_cost(rr_m, rid_m, vals_t, hours=2.0, fields={k: x for k, x in ATT.items() if k != drop})[0]
             for drop in ("event", "time_reference", "uncertainty_h", "derivation", "confirmer")]
    rc_mu, _ = attest_cost(rr_m, rid_m, vals_t, hours=2.0, fields={**ATT, "uncertainty_h": "nan"})
    chk(rcs_m == [10] * 5 and rc_mu == 10 and J(rr_m / "stage1_ledger.json")["runs"][0]["cost_basis"] == "unknown",
        "⛔음성 DJ Q3: 증언 근거 필드 (사건 · 시각 기준 · 불확실성 · H 산출 · 확인자) 가 하나라도 없거나 불확실성이 NaN 이면 거부 (비용 미확정 그대로)")
    rr_l, rid_l = orphan_root(1.5, hb=1.5)
    def other_writer():                                      # Codex 재현: 잠금 전에 다른 기록자가 8 h 증언 + STOP 확인을 저장
        l_ = J(rr_l / "stage1_ledger.json")
        l_["runs"][0].update(wall_h=8.0, cost_basis="attested_upper_bound",
                             attestation={**ATT, "confirmed_at": "t", "lower_at_attest": 1.5, "heartbeat_at_attest": 1.5})
        l_["stop_history"].append({"stop_id": "other", "code": "resume", "run_id": rid_l, "acked_at": "t"})
        _write_json_atomic(rr_l / "stage1_ledger.json", l_)
    rc_l1, _ = attest_cost(rr_l, rid_l, vals_t, hours=2.0, fields=ATT, deps={"before_lock": other_writer})
    el_l = J(rr_l / "stage1_ledger.json")
    rr_l2, rid_l2 = orphan_root(1.5, hb=1.5)
    held2 = _Lock(rr_l2 / "stage1.lock"); assert held2.acquire()
    b2 = (rr_l2 / "stage1_ledger.json").read_bytes()
    rc_l2, _ = attest_cost(rr_l2, rid_l2, vals_t, hours=2.0, fields=ATT)
    held2.release()
    unchanged2 = (rr_l2 / "stage1_ledger.json").read_bytes() == b2
    rc_l3, _ = attest_cost(rr_l2, rid_l2, vals_t, hours=2.0, fields=ATT)
    rc_l4, _ = attest_cost(rr_l2, rid_l2, vals_t, hours=3.0, fields=ATT)
    chk(rc_l1 == 10 and el_l["runs"][0]["wall_h"] == 8.0 and any(h.get("stop_id") == "other" for h in el_l["stop_history"])
        and rc_l2 == 10 and unchanged2 and rc_l3 == 0 and rc_l4 == 10 and J(rr_l2 / "stage1_ledger.json")["runs"][0]["wall_h"] == 2.0,
        "⛔음성 DJ P1-4 (Codex 재현): 잠금 전에 다른 기록자가 8 h 증언 · STOP 확인을 저장하면 우리 증언은 잠금 안에서 다시 읽고 거부 (8 h · 확인 그대로) · "
        "잠금이 잡혀 있으면 아무것도 안 쓴다 · 두 번째 증언은 거부")
    # 재부팅 고아 런 → 증언 → 정전 선언 → 한 번 다시 (끝에서 끝까지)
    rr_o = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
    rid0 = "a" * 32
    (rr_o / "A/seed11").mkdir(parents=True)
    _write_json_atomic(rr_o / "A/seed11/stage1_attempt.json", {"system": "A", "seed": 11, "run_id": rid0, "retry_of": None,
                                                             "retry_stop_id": None, "retry_kind": None})
    t_s = time.time() - 7200
    _write_json_atomic(rr_o / "stage1_ledger.json", {"runs": [{"system": "A", "seed": 11, "run_id": rid0, "start": "t", "start_epoch": t_s, "pgid": 4243,
        "start_recovery_clock": {"host": "fixture", "boot_id": "b-old", "kind": "CLOCK_BOOTTIME", "seconds": 0.0},
        "status": "running", "end": None, "wall_h": None, "wall_h_so_far": 1.5}], "stop_history": []})
    rc_o1, L_o1, _ = go(wt, rr=rr_o, boot="b-new")
    e_o, s_o1 = J(rr_o / "stage1_ledger.json")["runs"][0], J(rr_o / "STOP.json")
    rc_a1, _i1 = attest_cost(rr_o, rid0, vals_t, hours=1.0, fields=ATT)
    rc_a2, _i2 = attest_cost(rr_o, rid0, vals_t, hours=2.5, fields={**ATT, "confirmer": ""})
    rc_a3, info3 = attest_cost(rr_o, rid0, vals_t, hours=2.5, fields=ATT, deps={"btime": lambda: t_s + 3 * 3600})
    e_o2 = J(rr_o / "stage1_ledger.json")["runs"][0]
    chk(rc_o1 == RC["resume"] and not L_o1 and e_o["cost_basis"] == "unknown" and "--attest_cost" in s_o1["reason"] and rc_a1 != 0 and rc_a2 != 0
        and rc_a3 == 0 and e_o2["cost_basis"] == "attested_upper_bound" and e_o2["wall_h"] == 2.5
        and abs(info3["evidence"]["suggest_realtime_bound_h"] - 3.0) < 1e-6,
        "정전 복구: 재부팅을 넘긴 고아 런은 비용 미확정으로 멈추고 --attest_cost 를 알려 준다 · 하한 (1.5 h) 미만 · 확인자 없음 거부 · 근거를 다 적으면 증언 상한")
    rc_o2, L_o2, _ = go(wt, rr=rr_o, boot="b-new", ack=s_o1["stop_id"])
    s_o2 = J(rr_o / "STOP.json")
    (rr_o / "A/seed11").rename(rr_o / "A/seed11.outage")
    rc_o3, L_o3, _ = go(wt, rr=rr_o, boot="b-new", ack=s_o2["stop_id"], declare=OUT)
    smo = J(rr_o / "stage1_summary.json")
    chk(rc_o2 == RC["resume"] and s_o2.get("run_id") == rid0 and rc_o3 == 0 and len(L_o3) == 10 and smo["track"] == "stage1_pass"
        and any("2.5" in x for x in (smo.get("cost") or {}).get("attested") or []) and smo["cost"]["cap_h"] == 230.0,
        "정전 복구: 증언 상한으로 비용을 닫고 · 끊긴 폴더를 옆으로 옮겨 그 run_id 의 STOP 을 정전 선언과 함께 확인하면 A11 을 한 번 다시 돌려 1 단계를 "
        "마친다 (증언 비용은 묶음에 드러나고 상한은 카드 230 그대로)")
    c6 = clone(rr_d); led6 = J(c6 / "stage1_ledger.json")
    a11 = [x for x in led6["runs"] if (x["system"], x["seed"]) == ("A", 11)][0]
    led6["runs"].append({"system": "A", "seed": 11, "run_id": "b" * 32, "end": "t", "status": "ended", "wall_h": 1.0, "cost_basis": "measured",
                         "retry_of": a11["run_id"], "retry_kind": "interrupted"})
    _write_json_atomic(c6 / "stage1_ledger.json", led6)
    c8 = clone(rr_d); led8 = J(c8 / "stage1_ledger.json")
    led8["runs"][0].update(cost_basis="attested_upper_bound")               # 근거 (attestation) 없이 증언 상한이라고만
    _write_json_atomic(c8 / "stage1_ledger.json", led8)
    s6, s8 = summ(c6), summ(c8)
    chk(s6["track"] == "invalid" and any("과학적 판정" in x for x in s6["cost"]["invalid"])
        and s8["track"] == "invalid" and any("근거" in x for x in s8["cost"]["invalid"]),
        "⛔음성 정전 복구 (소비자): 장부에 과학적 판정 뒤 같은 시드 실행 · 근거 없는 증언 상한 → 묶음 무효")
    # ═══ DO 전 리뷰 (독립 리뷰 셋) — 반례를 진짜 판독 · 판정 함수로 ═══
    class _IntJudge:                                         # S1b — 첫 시드 녹음 fail 로 멈춘 뒤 판정 도중 Ctrl-C
        def __init__(self):
            self.armed = True
        def __getattr__(self, k):
            return getattr(real, k)
        def stage1_verdict(self, rd, **kw):
            if self.armed and "첫 시드 녹음 판정" in (kw.get("reason") or ""):
                self.armed = False
                raise KeyboardInterrupt("시험: 판정 도중 Ctrl-C")
            return real.stage1_verdict(rd, **kw)
    rc_b1, L_b1, rr_b = go(wt, scen={("A", 11): {"melt": "fail", "polls": 8}}, mq=_IntJudge())
    eb_, sb1_ = J(rr_b / "stage1_ledger.json")["runs"][0], J(rr_b / "STOP.json")
    rc_b2, L_b2, _ = go(wt, rr=rr_b, ack=sb1_["stop_id"])
    sb2_ = J(rr_b / "STOP.json") if (rr_b / "STOP.json").is_file() else {}
    smb_ = summ(rr_b)
    chk(rc_b1 == RC["interrupted"] and eb_.get("closes_system") is True and (eb_.get("melt_check") or {}).get("verdict") == "fail"
        and rc_b2 == RC["melt"] and not L_b2 and sb2_.get("code") == "melt" and smb_["track"] == "stop_track",
        "⛔음성 DO 전 리뷰 P0-1 (S1b): 첫 시드 녹음 fail 로 멈춘 뒤 판정 도중 러너가 끊겨도 닫힘은 이미 장부에 있다 → 확인해도 재시작이 melt 로 "
        f"멈추고 발사 0 · 소비자 stop_track ({rc_b1} · {rc_b2} · {sb2_.get('code')} · {smb_['track']})")
    rc_a3, L_a3, _ = go(wt, rr=rr_g, ack=sg["stop_id"], boot="b-new")
    sma_ = summ(rr_g)
    chk(rc_a3 == RC["melt"] and not L_a3 and sma_["track"] == "stop_track",
        "⛔음성 DO 전 리뷰 P0-1 (S1a): 첫 시드 녹음 fail · 정리 실패 뒤 재부팅해도 닫힘 (melt · 장부) 은 그대로 · 발사 0 · 소비자 stop_track "
        f"({rc_a3} · {sma_['track']})")
    rc_c1, L_c1, rr_c = go(wt, scen={("A", 11): {"melt": "species_swap", "polls": 8, "group_stuck": True}})
    ec1_, sc1_ = J(rr_c / "stage1_ledger.json")["runs"][0], J(rr_c / "STOP.json")
    go(wt, rr=rr_c, ack=sc1_["stop_id"], boot="b-new")      # 재부팅 → 고아 마감 (앞 상태를 지우지 않는다)
    ec2_ = J(rr_c / "stage1_ledger.json")["runs"][0]
    kc_ = real.run_kind(ec2_, str(rr_c / "A/seed11"), vals_t)
    chk(rc_c1 == RC["abnormal"] and (ec1_.get("melt_check") or {}).get("verdict") == "invalid" and ec1_.get("closes_system") is not True
        and ec2_.get("status") == "orphaned" and ec2_.get("status_before_orphan") == "stop_failed" and kc_ == "invalid",
        "⛔음성 DO 전 리뷰 P1-2 (S1c): 첫 시드 녹음 invalid · 정리 실패 → 장부 melt_check 를 먼저 적고 · 재부팅 고아 마감이 앞 상태를 남긴다 → "
        f"실행 종류 invalid (끊긴 런으로 바뀌지 않는다) ({rc_c1} · {ec2_.get('status')} · {ec2_.get('status_before_orphan')} · {kc_})")
    def _after_window(root_, sd_):                           # S1d · t12 — 녹음 창이 다 찬 직후 (판정 전) 정전
        st_ = {"done": False}
        def hook(_c):
            th_ = root_ / "A" / f"seed{sd_}" / "thermo.csv"
            if not st_["done"] and th_.is_file():
                rows_ = [x_ for x_ in th_.read_text(encoding="utf-8").splitlines()[1:] if x_.strip()]
                if rows_ and float(rows_[-1].split(",")[0]) >= 100.0:
                    st_["done"] = True
                    raise KeyboardInterrupt("시험: 녹음 창이 찬 직후 정전")
        return hook
    res_w = {}
    for nm_, sd_, scen_ in (("S1d_first_seed", 11, {("A", 11): {"melt": "fail", "polls": 8}}),
                            ("t12_second_seed", 12, {("A", 12): {"melt": "fail", "polls": 8}})):
        rw_ = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
        rc1_, L1_, _ = go(wt, rr=rw_, scen=scen_, sleep_hook=_after_window(rw_, sd_))
        sw1_ = J(rw_ / "STOP.json")
        mwv_ = real.melt_window_check(rw_ / "A" / f"seed{sd_}", values=vals_t, log=lambda *m: None)["verdict"]
        rc2_, L2_, _ = go(wt, rr=rw_, ack=sw1_["stop_id"], declare=OUT)       # 정전 선언으로 확인 → 과학적이라 받지 않는다
        led_w_ = J(rw_ / "stage1_ledger.json")
        row_ = [x_ for x_ in led_w_["runs"] if (x_["system"], x_["seed"]) == ("A", sd_)][-1]
        res_w[nm_] = (rc1_ == RC["interrupted"], mwv_, rc2_ == RC["refused"], len(L2_),
                      real.run_kind(row_, str(rw_ / "A" / f"seed{sd_}"), vals_t))
    chk(all(v_ == (True, "fail", True, 0, "scientific") for v_ in res_w.values()),
        "⛔음성 DO 전 리뷰 S1d · t12: 녹음 창이 다 찼고 fail 인 채 (판정 전) 정전으로 끊긴 런은 정전 선언으로 다시 돌리지 않는다 — 첫 시드든 둘째 "
        f"시드든 실행 종류 과학적 (결과가 정해졌다) · 발사 0 ({res_w})")
    rc_p1, L_p1, rr_p = go(wt, scen={("B", 11): {"raise_on_poll": 3, "polls": 8}})
    (rr_p / "B/seed11").rename(rr_p / "B/seed11.cut1")
    vp_ = real.stage1_verdict(rr_p / "B/seed11.cut1", values=vals_t, log=lambda *m: None, reason="selftest — 보존 폴더 제자리 판정")
    rowp_ = [x_ for x_ in J(rr_p / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("B", 11)][-1]
    kp_ = real.run_kind(rowp_, str(rr_p / "B/seed11.cut1"), vals_t)
    chk(vp_["status"] == "incomplete" and (vp_["checks"]["identity"] or {}).get("preserved") is True and kp_ == "interrupted",
        "⛔음성 DO 전 리뷰 (소비자 P0 a · t3): 보존 폴더를 제자리에서 판정해도 이름 때문에 invalid 가 되지 않는다 (incomplete) → 실행 종류는 끊긴 런 · "
        f"한도를 우회하는 invalid 재시도로 바뀌지 않는다 ({vp_['status']} · {kp_})")
    rc_f1, L_f1, rr_f = go(wt, scen={("A", 12): {"final": "ps4_broken", "rc": 1}})
    sf1_ = J(rr_f / "STOP.json")
    (rr_f / "A/seed12").rename(rr_f / "A/seed12.rc1")
    vf_ = real.stage1_verdict(rr_f / "A/seed12.rc1", values=vals_t, log=lambda *m: None, reason="selftest — 러너가 시킨 제자리 판정")
    rc_f2, L_f2, _ = go(wt, rr=rr_f, ack=sf1_["stop_id"], declare={**FIX, "rejudge_impossible_reason": "selftest"})
    chk(rc_f1 == RC["abnormal"] and vf_["status"] == "fail" and rc_f2 == RC["refused"] and not L_f2,
        "⛔음성 DO 전 리뷰 (소비자 P0 b · t8): 끝까지 돌았는데 PS₄ fail 인 런 (드라이버 rc 1) 을 보존해 제자리 판정하면 fail 그대로 → 원인 고침 선언으로도 "
        f"다시 돌리지 않는다 ({rc_f1} · {vf_['status']} · {rc_f2})")
    rc_tt, L_tt, rr_tt = go(wt, scen={("A", 11): {"melt": "fail", "polls": 8, "torn_tail": True}})
    vtt_ = J(rr_tt / "A/seed11/stage1_verdict.json")
    chk(rc_tt == RC["melt"] and vtt_["status"] == "fail" and vtt_.get("closes_system") is True and L_tt[0].killed,
        "⛔음성 DO 전 리뷰 (소비자 P0 c · t9): 첫 시드 녹음 fail 로 죽일 때 traj 마지막 프레임이 반쪽이어도 판정은 fail · closes_system (invalid 로 "
        f"닫힘이 꺼지지 않는다) ({rc_tt} · {vtt_['status']} · {vtt_.get('closes_system')})")
    rc_t1, _, rr_t = go(wt, scen={("A", 11): {"raise_on_poll": 3}})
    good_stop = (rr_t / "STOP.json").read_bytes(); trunc = good_stop[:20]
    (rr_t / "STOP.json").write_bytes(trunc)
    rc_t2, L_t2, _ = go(wt, rr=rr_t)
    keep_ok = (rr_t / "STOP.json").read_bytes() == trunc
    h0_ = J(rr_t / "stage1_ledger.json").get("stop_history")
    (rr_t / "STOP.json").write_text(json.dumps({"code": "interrupted", "reason": "x"}), encoding="utf-8")
    rc_t3, L_t3, _ = go(wt, rr=rr_t)
    h1_ = J(rr_t / "stage1_ledger.json").get("stop_history")
    sp_ok = json.loads(good_stop)
    (rr_t / "STOP.json").write_text(json.dumps({**sp_ok, "declaration": DECL(OUT)}), encoding="utf-8")
    rc_t4, L_t4, _ = go(wt, rr=rr_t, ack=sp_ok["stop_id"])
    h2_ = J(rr_t / "stage1_ledger.json").get("stop_history") or []
    acked_ = [x_ for x_ in h2_ if x_.get("stop_id") == sp_ok["stop_id"]]
    chk(rc_t2 == RC["refused"] and not L_t2 and keep_ok and rc_t3 == RC["refused"] and not L_t3 and h1_ == h0_
        and len(acked_) == 1 and "declaration" not in acked_[0] and not L_t4,
        "⛔음성 DO 전 리뷰 P2-5 · 6 · 7: 잘린 STOP 은 덮어쓰지 않고 거부 (원본 그대로) · stop_id 없는 STOP 을 조용히 확인하지 않는다 · STOP 안에 "
        f"끼운 declaration 은 확인 기록으로 옮기지 않는다 ({rc_t2} · {keep_ok} · {rc_t3} · {acked_[:1]})")
    c_r = clone(rr_g3); sg3_ = J(c_r / "STOP.json")
    go(wt, rr=c_r, ack=sg3_["stop_id"], pg_alive=lambda pg: True, boot="b-new")
    er_ = [x_ for x_ in J(c_r / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("B", 11)][-1]
    chk(er_.get("status") == "orphaned" and er_.get("status_before_orphan") == "stop_failed",
        "⛔음성 DO 전 리뷰 P2-10: 재부팅 뒤 (boot_id 다름) 같은 pgid 가 다른 프로세스에 쓰여도 그 그룹은 죽었다 — 영원히 거부하지 않고 고아로 마감 "
        f"(앞 상태 남김) ({er_.get('status')} · {er_.get('status_before_orphan')})")
    wt_cap = mk_wt(card=mk_card(stage1_cap_gpu_h=7.5))
    rc_k, L_k, rr_k = go(wt_cap, scen={("A", 11): {"polls": 50}}, poll_s=5 * 3600.0, seed_worst_h=1.0)
    ek_ = J(rr_k / "stage1_ledger.json")["runs"][0]
    chk(rc_k == RC["cap"] and ek_.get("wall_h") is not None and ek_["wall_h"] <= 7.5 + 0.01,
        f"⛔음성 DO 전 리뷰 P2-11: 실행 중 상한 검사는 상한보다 늦지 않다 (poll 5 h · 상한 7.5 h → 멈춘 벽시계 {ek_.get('wall_h')} h)")
    rc_v1, L_v1, _ = go(wt, expect_values="0" * 16)
    rc_v2, L_v2, _ = go(wt, python_ok=lambda p_: False)
    rc_v3, L_v3, _ = go(wt, expect_values=real.values_sha16(vals_t))
    chk(rc_v1 == RC["refused"] and not L_v1 and rc_v2 == RC["refused"] and not L_v2 and rc_v3 == RC["pass"] and L_v3,
        "⛔음성 DO 전 리뷰 P2-12 · P2-8: 카드 값 지문이 러너 고정값과 다르면 · --python 을 실행할 수 없으면 시작하지 않는다 (맞으면 돈다)")
    if hasattr(signal, "pthread_sigmask"):                   # POSIX 신호 막기가 있는 OS 만 (Windows 는 os.kill(자기, SIGTERM) 이 프로세스를 바로 끝낸다 · 러너도 막지 않는다)
        rc_sg, L_sg, rr_sg = go(wt, launch_signal=True)
        es_, ss_ = J(rr_sg / "stage1_ledger.json")["runs"][0], J(rr_sg / "STOP.json")
        chk(rc_sg == RC["interrupted"] and L_sg and L_sg[0].stopped and ss_.get("run_id") == es_.get("run_id") and es_.get("end") is not None,
            "⛔음성 DO 전 리뷰 P2-9: 띄운 직후 (손잡이를 적기 전) SIGTERM 이 와도 손잡이를 적은 뒤에 받아 그 담금질을 멈추고 마감한다 (놓친 자식 없음)")
    else:
        print("  · 건너뜀 (POSIX 전용) DO 전 리뷰 P2-9 띄우는 순간 신호 — 이 OS 에는 pthread_sigmask 가 없다")
    fs_calls, _of = [], os.fsync
    os.fsync = lambda fd: (fs_calls.append(fd), _of(fd))[1]
    try:
        _write_json_atomic(pathlib.Path(tempfile.mkdtemp(dir=tmp_root)) / "x.json", {"a": 1})
    finally:
        os.fsync = _of
    chk(len(fs_calls) >= (2 if os.name == "posix" else 1),        # 디렉터리 fsync 는 POSIX 만 (Windows 는 디렉터리를 못 연다)
        f"⛔음성 DO 전 리뷰 P2-14: 장부 · STOP · 실행 전 기록 쓰기는 파일과 디렉터리 (POSIX) 를 fsync 한다 ({len(fs_calls)})")
    def _led_edit(fn=None, raw=None):
        c_ = clone(rr_d)
        if raw is not None:
            (c_ / "stage1_ledger.json").write_text(raw(J(c_ / "stage1_ledger.json")), encoding="utf-8")
        else:
            l_ = J(c_ / "stage1_ledger.json"); fn(l_); _write_json_atomic(c_ / "stage1_ledger.json", l_)
        return summ(c_)
    def _big(l_):
        l_["runs"][0]["wall_h"] = 0
        return json.dumps(l_).replace('"wall_h": 0,', '"wall_h": 1' + "0" * 400 + ",", 1)
    led_t = {"wall_str": (_led_edit(lambda l_: l_["runs"][0].update(wall_h=str(l_["runs"][0]["wall_h"]))), "유한한 비음수"),
             "heartbeat_str": (_led_edit(lambda l_: l_["runs"][0].update(wall_h_so_far="0.5")), "유한한 비음수"),
             "end_false": (_led_edit(lambda l_: l_["runs"][0].update(end=False)), "끝 시각"),
             "seed_float": (_led_edit(lambda l_: l_["runs"][0].update(seed=float(l_["runs"][0]["seed"]))), "계 · 시드 꼴"),
             "closes_str": (_led_edit(lambda l_: l_["runs"][0].update(closes_system="true")), "참거짓"),
             "melt_check_str": (_led_edit(lambda l_: l_["runs"][0].update(melt_check="fail")), "melt_check"),
             "dup_key": (_led_edit(raw=lambda l_: json.dumps(l_).replace('"runs":', '"runs": [], "runs":', 1)), "같은 열쇠"),
             "huge": (_led_edit(raw=_big), "유한한 비음수"),
             "below_heartbeat": (_led_edit(lambda l_: l_["runs"][0].update(wall_h_so_far=float(l_["runs"][0]["wall_h"]) + 5.0)), "자기 하한")}
    s_close = _led_edit(lambda l_: l_["runs"][0].update(closes_system=True, melt_check={"verdict": "fail", "message": "x"}))
    c_tv = clone(rr_d); (c_tv / "A/seed11/stage1_verdict.json").write_text('{"status": "pa', encoding="utf-8")
    s_tv = summ(c_tv)
    got_l = {k: inv_(v_, w_) for k, (v_, w_) in led_t.items()}
    chk(all(got_l.values()) and s_close["track"] == "stop_track" and s_tv["track"] == "invalid" and "A11" in (s_tv.get("stale_verdicts") or []),
        "⛔음성 DO 전 리뷰 (소비자 P2 · P1-3 · P2-17): 장부 값 꼴 — 숫자 글자 · end False · 시드 12.0 · closes 'true' · melt_check 글자 · 같은 열쇠 둘 · "
        "10^400 · heartbeat 보다 작은 측정 비용 → 무효 (죽지 않음) · 장부에만 적힌 첫 시드 닫힘 → stop_track · 잘린 현재 판정 → 무효 (죽지 않음) "
        f"({ {k: x for k, x in got_l.items() if not x} } · {s_close['track']} · {s_tv['track']})")
    clk_ = lambda sec: {"host": "h", "boot_id": "b", "kind": "CLOCK_BOOTTIME", "seconds": sec}
    oh_ = {"ok": _orphan_upper_hours({"start_recovery_clock": clk_(100.0), "wall_h_so_far": 0.5}, clk_(7300.0)),
           "start_str": _orphan_upper_hours({"start_recovery_clock": clk_("100"), "wall_h_so_far": 0.5}, clk_(7300.0)),
           "now_bool": _orphan_upper_hours({"start_recovery_clock": clk_(0.0), "wall_h_so_far": 0.5}, clk_(True)),
           "lower_str": _orphan_upper_hours({"start_recovery_clock": clk_(100.0), "wall_h_so_far": "0.5"}, clk_(7300.0))}
    chk(oh_["ok"] == 2.0 and oh_["start_str"] is None and oh_["now_bool"] is None and oh_["lower_str"] is None,
        f"⛔음성 DO 전 리뷰 P1-3 (러너): 고아 런 상한의 시계 · 하한이 글자 · 참거짓이면 상한을 내지 않는다 (비용 미확정 → 증언) ({oh_})")
    cu_ = {"cap_orphan_outage": E([run0(status="orphaned", status_before_orphan="cap")], rcpt("cap", OUT), {R0: ufold("cpo")}),
           "cap_orphan_raise": E([run0(status="orphaned", status_before_orphan="cap")],
                                 rcpt("cap", {**OUT, "retry_reason": "budget_cap_raised"}), {R0: ufold("cpr")})}
    chk((cu_["cap_orphan_outage"]["ok"], cu_["cap_orphan_raise"]["ok"]) == (False, True),
        "⛔음성 DO 전 리뷰 P2-4: 상한으로 멈춘 런이 고아로 마감돼도 (앞 상태 cap 을 남김) 상한 규칙 그대로 — 정전 사유 거부 · 상한 인상 사유만 "
        f"({cu_['cap_orphan_outage']['ok']} · {cu_['cap_orphan_raise']['ok']})")
    # 7) 진짜 프로세스 그룹 (POSIX) — _Proc.stop 이 자기 그룹 (자식 · 손자) 만 멈추고 기다린다 · 옆 프로세스는 안 건드린다
    #    (회신 DG: '실제 Linux 프로세스 그룹 종료는 하지 않았다' — 가짜 담금질 시험이 못 보는 자리)
    if os.name == "posix":
        def _pid_alive(pid):
            try:
                return pathlib.Path(f"/proc/{pid}/stat").read_text().split()[2] != "Z"     # 거둬지지 않은 좀비는 죽은 것
            except FileNotFoundError:
                return False
            except OSError:
                try:
                    os.kill(pid, 0); return True
                except ProcessLookupError:
                    return False
        tdp = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
        code = ("import subprocess, sys, time; "
                "c = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(600)']); "
                "open(sys.argv[1], 'w').write(str(c.pid)); time.sleep(600)")
        bystander = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(600)"])
        pr = _Proc([sys.executable, "-c", code, str(tdp / "grandchild.pid")], tdp / "p.log")
        for _ in range(200):
            if (tdp / "grandchild.pid").is_file() and (tdp / "grandchild.pid").read_text().strip():
                break
            time.sleep(0.05)
        gpid = int((tdp / "grandchild.pid").read_text())
        before = pr.poll() is None and _pid_alive(gpid) and os.getpgid(gpid) == pr.pid
        t0 = time.time(); r1 = pr.stop(grace_s=5); dt = time.time() - t0
        gone = (pr.poll() is not None) and not _pid_alive(gpid)
        by_ok = bystander.poll() is None
        bystander.kill(); bystander.wait()
        chk(before and gone and by_ok and r1["group_empty"] and r1["signals"] == ["TERM"] and dt < 10,
            f"진짜 프로세스 그룹: TERM 이 그룹 전체 (손자까지) 에 가서 KILL 없이 비고 기다린다 · 옆 프로세스는 산다 (대표 rc {r1['leader_rc']} · {r1['signals']} · {dt:.1f} s)")
        def _wait_pid(path):
            for _ in range(200):
                if path.is_file() and path.read_text().strip():
                    break
                time.sleep(0.05)
            time.sleep(0.5)                                  # 일꾼이 SIGTERM 무시를 걸 시간
            return int(path.read_text())
        IGN = "import signal, time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(600)"
        code2 = ("import subprocess, sys, time; c = subprocess.Popen([sys.executable, '-c', " + repr(IGN) + "]); "
                 "open(sys.argv[1], 'w').write(str(c.pid)); time.sleep(600)")
        pr2 = _Proc([sys.executable, "-c", code2, str(tdp / "w2.pid")], tdp / "p2.log")
        w2 = _wait_pid(tdp / "w2.pid")
        r2 = pr2.stop(grace_s=2)
        ok2 = r2["group_empty"] and "KILL" in r2["signals"] and not _pid_alive(w2) and pr2.poll() is not None
        code3 = ("import subprocess, sys; c = subprocess.Popen([sys.executable, '-c', " + repr(IGN) + "]); "
                 "open(sys.argv[1], 'w').write(str(c.pid))")
        pr3 = _Proc([sys.executable, "-c", code3, str(tdp / "w3.pid")], tdp / "p3.log")
        w3 = _wait_pid(tdp / "w3.pid")
        for _ in range(200):
            if pr3.poll() is not None:
                break
            time.sleep(0.05)
        before3 = pr3.poll() == 0 and _pid_alive(w3) and os.getpgid(w3) == pr3.pid
        r3 = pr3.stop(grace_s=2)
        ok3 = before3 and r3["group_empty"] and "KILL" in r3["signals"] and not _pid_alive(w3)
        for w_ in (w2, w3):                                  # 시험이 실패해도 일꾼을 남기지 않는다
            try:
                os.kill(w_, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass
        chk(ok2 and ok3,
            f"⛔음성 DH P0-3 (진짜 프로세스): 대표가 TERM 에 죽고 일꾼은 TERM 을 무시 → 그룹에 KILL · 비움 ({r2['signals']}) / "
            f"대표가 rc 0 으로 먼저 끝나고 일꾼이 남음 → 그룹을 보고 KILL · 비움 ({r3['signals']})")
    shutil.rmtree(tmp_root, ignore_errors=True)
    print(f"li2s2_stage1_runner selftest: ⭕ {ok} · ⛔ {bad}")
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--worktree", help="이 카드를 담은 커밋의 git worktree (도구 · 카드 · 결정 원장을 여기서 읽는다)")
    ap.add_argument("--run_root", help="담금질 출력 루트 → <run_root>/<A|B>/seed<S>/")
    ap.add_argument("--python", default=sys.executable, help="담금질을 돌릴 python (uma env 절대경로)")
    ap.add_argument("--order", default=DEFAULT_ORDER)
    ap.add_argument("--seed_worst_h", type=float, default=21.0,
                    help="한 시드 최악 예상 (카드 견적 상단) — 끝난 런의 관측 벽시계와 같이 최댓값으로 착수 판단에 쓴다 (관측이 있어도 쓴다)")
    ap.add_argument("--poll_s", type=float, default=300.0, help="첫 시드 녹음 판정 · 상한 · heartbeat 를 볼 간격")
    ap.add_argument("--gpu_poll_s", type=float, default=60.0)
    ap.add_argument("--start_max_mib", type=int, default=2000, help="이 이하가 두 번 연속이면 띄운다")
    ap.add_argument("--ack_stop", default=None, help="STOP.json 의 stop_id — 앞선 (닫는 사건이 아닌) 멈춤을 확인했다는 표시")
    g = ap.add_argument_group("재시도 선언 (--ack_stop 과 함께 · 회신 DJ Q1 — 결과와 무관한 사건만 · 카드 retry_reasons)")
    g.add_argument("--retry_reason", default=None, help="카드 retry_reasons 의 사유 (끊긴 런: power_outage · host_crash_or_reboot · hardware_fault · "
                                                     "budget_cap_raised (상한 런만) · invalid 런: invalid_cause_fixed)")
    g.add_argument("--retry_event", default=None, help="무슨 사건인가 (예: '11-05 03:10 kgy 정전')")
    g.add_argument("--retry_evidence", default=None, help="근거 (로그 · 커밋 · 결정 · 사진 위치 등)")
    g.add_argument("--declared_by", default=None, help="선언하는 사람")
    g.add_argument("--rejudge_impossible_reason", default=None, help="MD 까지 (또는 끝까지) 돈 invalid 런 — 있는 파일을 고쳐 다시 판정할 수 없는 이유")
    g2 = ap.add_argument_group("재부팅 고아 런 비용 증언 (회신 DJ Q3 — 카드 attestation_required_fields)")
    g2.add_argument("--attest_cost", default=None, metavar="RUN_ID", help="그 런의 비용 근거를 본다 (--attest_hours 와 근거 필드를 주면 잠금 안에서 상한을 적는다)")
    g2.add_argument("--attest_hours", type=float, default=None, help="비용 상한 H [GPU-h] — 유한 · 양수 · 하한 (마지막 heartbeat) 이상")
    g2.add_argument("--attest_event", default=None, help="어떤 사건으로 종료 상한을 알았나")
    g2.add_argument("--attest_time_reference", default=None, help="시각의 기준 (어느 시계 · 어느 기록)")
    g2.add_argument("--attest_uncertainty_h", default=None, help="그 시각의 불확실성 [h]")
    g2.add_argument("--attest_derivation", default=None, help="H 를 어떻게 냈나")
    g2.add_argument("--attest_confirmer", default=None, help="확인한 사람")
    ap.add_argument("--print_cmd", default=None, metavar="SYS:SEED", help="그 시드의 담금질 명령을 카드 기계값에서 만들어 찍고 끝난다")
    a = ap.parse_args()
    # ⭐ DO 전 리뷰 P2-13 — 드라이버 · 카드 값 고정값은 명령줄로 바꾸지 않는다 (바꾸려면 이 파일의 고정값을 고치고 다시 리뷰)
    a.expect_sha, a.expect_values_sha16 = EXPECTED_DRIVER_SHA16, EXPECTED_VALUES_SHA16
    if a.selftest:
        return _selftest()
    if not (a.worktree and a.run_root):
        ap.error("--worktree · --run_root 가 필요하다")
    if a.attest_cost:
        W = pathlib.Path(a.worktree); mq = load_mq(W)
        vals = mq.read_li2s2_values(W / CARD_REL)
        rc_, info = attest_cost(a.run_root, a.attest_cost, vals, hours=a.attest_hours,
                                fields={"event": a.attest_event, "time_reference": a.attest_time_reference,
                                        "uncertainty_h": a.attest_uncertainty_h, "derivation": a.attest_derivation,
                                        "confirmer": a.attest_confirmer})
        print(json.dumps(info, ensure_ascii=False, indent=1, default=str))
        return rc_
    if a.print_cmd:
        W = pathlib.Path(a.worktree); mq = load_mq(W)
        vals = mq.read_li2s2_values(W / CARD_REL)
        sysn, seed = parse_order(a.print_cmd)[0]
        print(shlex.join(build_cmd(a.python, W, a.run_root, sysn, seed, vals, mq)))
        return 0
    return run(a)


if __name__ == "__main__":
    sys.exit(main())
