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
import argparse
import copy, datetime, hashlib, importlib.util, json, os, pathlib, re, shlex, shutil, signal, subprocess, sys, tempfile, threading, time, traceback, uuid, socket, math

EXPECTED_DRIVER_SHA16 = "74128f03a7354ee3"     # tools/ionic/melt_quench_uma.py — 바뀌면 이 줄도 같이 바꾸고 다시 리뷰한다
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


_CRIT = [0]                                       # ⭐ DP 전 리뷰 (둘째) F2 · F4 — 쓰기 · 띄우기 구간 깊이: 이 안에서 온 종료 신호는 구간이 끝난 뒤 던진다
_PENDING = []                                     # 미룬 신호 이름 (pthread_sigmask 는 주 스레드만 막는다 — 다른 스레드가 받은 신호도 파이썬 처리기는
                                                  # 주 스레드에서 돈다 · 2026-11-04 selftest 실측: 임시 파일을 만든 직후 처리기가 돌아 임시 파일이 남았다)


class _critical:
    """⭐ 쓰기 (임시 파일 → 이름 교체) · 띄우고 손잡이 적기를 신호로 반쯤 끊기지 않게 — 처리기가 이 안에서 불리면 미뤘다가 나갈 때 던진다
    (예외로 나가는 중이면 그 예외를 그대로 둔다 · 겹쳐 써도 된다)."""
    def __enter__(self):
        _CRIT[0] += 1
        return self
    def __exit__(self, et, ev, tb):
        _CRIT[0] -= 1
        if _CRIT[0] == 0 and _PENDING:
            nm_ = _PENDING[0]
            _PENDING.clear()
            if et is None:
                if nm_ == "SIGINT":
                    raise KeyboardInterrupt(f"신호 {nm_} (쓰기 구간 뒤에 받음)")
                raise _RunnerSignal(f"신호 {nm_} (쓰기 구간 뒤에 받음)")
        return False


class _AfterReplace(OSError):
    """⭐ 회신 DP P0-1 — 파일 교체는 끝났는데 그 뒤 (디렉터리 fsync) 가 실패 — 디스크에는 새 내용이 **보인다**. 부르는 쪽은 메모리를 되돌리지 않는다
    (그래도 멈춘다). ⭐ 회신 DQ Q2 — 뜻은 '교체되어 보이는 상태' 이지 '정전 뒤에도 남는다' 는 보증이 아니다 (파일 fsync 로 디렉터리 항목의
    내구성까지 보장되지 않는다) · 디렉터리 동기화가 계속 실패하는 환경에서는 첫 저장부터 멈춘다 (보수적 제한)."""


class _PersistFailed(Exception):
    """⭐ DP 전 리뷰 F4 — 본 과학적 결과를 장부에 적다가 실패 (보관 목록 · 행 꼴 · 저장 예외). 호출자가 거부 · invalid 로 멈춘다."""


class _RunnerSignal(BaseException):
    """SIGTERM · SIGHUP 을 예외로 — except Exception 에 안 먹히고 정리 경로 (자식 멈춤 · 장부 · STOP · 잠금) 를 탄다."""


def _now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sha16(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()[:16]


def _no_dup_pairs(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError(f"같은 열쇠 {k!r} 가 둘")
        d[k] = v
    return d


def _loads_strict(text):
    """⭐ 회신 DO P1 — 러너의 기록 읽기 (장부 · 결정 원장 · 실행 전 기록 · 판정) 는 같은 열쇠 둘을 받지 않는다 (드라이버 loads_strict 와 같은 뜻 ·
    드라이버를 싣기 전에도 쓴다). 마지막 값으로 읽으면 소비자가 무효로 본 기록을 다른 기록자 (러너 · 증언) 가 정상 꼴로 다시 쓴다."""
    return json.loads(text, object_pairs_hook=_no_dup_pairs)


def decision_state(worktree, did=DECISION):
    try:                                                     # ⭐ 회신 DO P1 — 결정 원장도 엄격히 (못 읽으면 '모름' → 시작하지 않는다)
        D = _loads_strict((pathlib.Path(worktree) / "db/governance/decisions.json").read_text(encoding="utf-8"))
        hit = [d for d in D["decisions"] if isinstance(d, dict) and d.get("id") == did]
    except (OSError, ValueError, KeyError, TypeError, RecursionError):
        return None
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


HELD_SIGNALS = ("SIGTERM", "SIGHUP", "SIGINT")   # 띄우는 동안 부모가 막는 종료 신호 (DO 전 리뷰 P2-9)
_PRE_HOLD_MASK = None                            # _held 가 막기 전 마스크 — 그 사이 띄운 자식이 exec 전에 이 마스크로 돌아간다


def _held_signal_set():
    return {getattr(signal, n) for n in HELD_SIGNALS if hasattr(signal, n)}


def _held(fn):
    """⭐ DO 전 리뷰 P2-9 · 회신 DO P2 — fn() 을 종료 신호를 막은 채 부른다 (손잡이를 적기 전 신호로 자식을 놓치지 않게 · 부모만 ·
    주 스레드 · pthread_sigmask 가 있는 OS 만). 그 사이 _Proc 로 띄운 자식은 막기 전 마스크로 돌아간 뒤 exec 한다 (_child_restore_mask)."""
    global _PRE_HOLD_MASK
    hold = hasattr(signal, "pthread_sigmask") and threading.current_thread() is threading.main_thread()
    old = signal.pthread_sigmask(signal.SIG_BLOCK, _held_signal_set()) if hold else None
    outer = _PRE_HOLD_MASK                                   # ⭐ DP 전 리뷰 (둘째) F4 — 안에서 다시 불러도 바깥 값을 지우지 않는다
    _PRE_HOLD_MASK = old if outer is None else outer
    try:
        return fn()
    finally:
        _PRE_HOLD_MASK = outer
        if hold:
            signal.pthread_sigmask(signal.SIG_SETMASK, old)


def _child_restore_mask():
    """Popen preexec (자식 · exec 전) — ⭐ 회신 DO P2: 신호 마스크는 fork · exec 로 물려받고 restore_signals 는 마스크를 풀지 않는다 →
    러너가 띄우는 동안 막은 TERM · HUP · INT 가 자식 (담금질 · 손자) 에서 막힌 채로 남아 TERM 이 안 먹고 KILL 로 넘어간다.
    막기 전 마스크로 돌린다 (_held 밖에서 띄웠으면 그 신호들만 푼다)."""
    m = _PRE_HOLD_MASK
    if m is not None:
        signal.pthread_sigmask(signal.SIG_SETMASK, m)
    signal.pthread_sigmask(signal.SIG_UNBLOCK, _held_signal_set())   # ⭐ DP 전 리뷰 (둘째) F4 — 러너가 TERM 막힌 채 시작됐어도 (물려받은 마스크) 자식은 푼다


class _Proc:
    """subprocess.Popen 감싸개 — 시험에서 같은 모양의 가짜로 바꾼다. 자기 세션 (start_new_session) = 자기 프로세스 그룹."""
    def __init__(self, cmd, log_path):
        self.fh = open(log_path, "a")
        kw = {"preexec_fn": _child_restore_mask} if (os.name == "posix" and hasattr(signal, "pthread_sigmask")) else {}
        self.p = subprocess.Popen(cmd, stdout=self.fh, stderr=subprocess.STDOUT, start_new_session=True, **kw)
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
            rid = _loads_strict((pathlib.Path(rd) / name).read_text(encoding="utf-8")).get("run_id")
            if isinstance(rid, str) and rid:
                return rid
        except (OSError, ValueError, AttributeError, RecursionError):
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
        rk, rk_d = mq.run_kind_detail(x, rec["path"], values)   # ⭐ 회신 DK P0-2 — 소비자 · 확인 검사와 같은 분류 (DO 전 리뷰 — 보존 폴더 녹음까지)
        if rk == "scientific":
            if rk_d.get("source") == "folder_verdict":         # ⭐ DP 전 리뷰 F1 · F2 — 폴더 판정 기록으로 본 과학적 결과도 거부 전에 장부에
                return {"ok": False, "code": "invalid",
                        "observed": {"kind": "verdict", "run_id": rid, "status": rk_d.get("status"), "closes_system": rk_d.get("closes_system") is True,
                                     "provenance": rk_d.get("provenance"), "prior": rk_d.get("prior")},
                        "why": f"이전 실행 {tag} 폴더의 판정 기록에 과학적 판정 ({rk_d.get('status')}) 이 있다 — 장부에 남긴다 (장부 판정과 다르면 덮지 않고 충돌 관측으로) · 다시 담금질하지 않는다"}
            if rk_d.get("source") == "folder_melt_window":     # ⭐ 회신 DO P0 — 지금 계산한 녹음 fail 을 러너가 거부 전에 장부에 적는다
                return {"ok": False, "code": "invalid", "observed": {"kind": "melt", "run_id": rid, **(rk_d.get("melt") or {})},
                        "why": f"이전 실행 {tag} 의 녹음 창이 다 찼고 fail (보존 폴더에서 지금 계산 · 규칙 M) — 그 시드는 fail · 장부에 남긴다 · "
                               "다시 담금질하지 않는다 (묶음에 넣으려면 그 폴더를 seed 자리로 되돌려 --stage1_verdict)"}
            return {"ok": False, "code": "invalid", "why": f"이전 실행 {tag} 에 과학적 판정 (장부 · 폴더) 이 있다 — 다시 담금질하지 않는다"}
        if rk == "unreadable":
            return {"ok": False, "code": "invalid", "why": f"이전 실행 {tag} 의 판정을 못 읽는다 (폴더 판정 파일 · 장부 값) — '판정 없음' 으로 읽지 않는다 "
                                                          "(원자료로 --stage1_verdict 다시 판정한 뒤 다시)"
                                                          + (f" · {rk_d.get('why')}" if rk_d.get("why") else "")}   # ⭐ DR 전 5차 — 판독 불가 까닭 · 출구
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


def ack_declaration_problems(decl, sp, led, values, mq, run_root, observed=None):
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
    kind, kd = mq.run_kind_detail(hit[0], rec["path"] if rec else None, values)   # 그 실행의 종류 (code 가 아니라 실행에서 · 회신 DK P0-2 — 한 분류)
    if kind == "scientific":
        if kd.get("source") == "folder_melt_window" and observed is not None:   # ⭐ 회신 DO P0 — 본 녹음 fail 을 호출자가 장부에 적는다
            observed.append({"kind": "melt", "run_id": rid, **(kd.get("melt") or {})})
        elif kd.get("source") == "folder_verdict" and observed is not None:     # ⭐ DP 전 리뷰 F1 — 폴더 판정 기록의 과학적 판정도
            observed.append({"kind": "verdict", "run_id": rid, "status": kd.get("status"), "closes_system": kd.get("closes_system") is True,
                             "provenance": kd.get("provenance"), "prior": kd.get("prior")})
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
                if _loads_strict((cand / "stage1_attempt.json").read_text(encoding="utf-8")).get("run_id") == e.get("run_id"):
                    mt = max((f.stat().st_mtime for f in cand.iterdir() if f.is_file()), default=None); rd = cand; break
            except (OSError, ValueError, AttributeError, RecursionError):
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
        try:                                                 # ⭐ 회신 DO P1 — 읽기만 하는 조회도 엄격히 (같은 열쇠 둘 = 못 읽음)
            led = _loads_strict(led_p.read_text(encoding="utf-8"))
            if not isinstance(led, dict):
                raise ValueError("장부가 객체가 아니다")
        except (OSError, ValueError, RecursionError) as e_:
            return 10, {"why": f"장부를 엄격히 못 읽는다 ({type(e_).__name__}: {str(e_)[:80]}) — 사람이 본다 (아무것도 안 썼다)"}
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
        left_ = _leftover_tmps(led_p, R / "STOP.json")
        if left_:                                            # ⭐ DP 전 리뷰 (둘째) F2
            return 10, {"why": f"앞 쓰기가 끊겨 남은 임시 파일이 있다 ({left_}) — 그 안이 더 새 기록일 수 있어 증언을 받지 않는다 (아무것도 안 썼다 · 사람이 본다)"}
        try:                                                 # ⭐ 잠금 안에서 다시 읽는다 · 회신 DO P1 — 엄격히 (못 읽으면 증언을 받지 않고 원본 그대로)
            led = _loads_strict(led_p.read_text(encoding="utf-8"))
            if not isinstance(led, dict):
                raise ValueError("장부가 객체가 아니다")
        except (OSError, ValueError, RecursionError) as e_:
            return 10, {"why": f"장부를 엄격히 못 읽는다 ({type(e_).__name__}: {str(e_)[:80]}) — 증언을 받지 않는다 (아무것도 안 썼다)"}
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


TMP_SUFFIX = ".tmp"


def _leftover_tmps(*paths):
    """⭐ DP 전 리뷰 (둘째) F2 — 앞 쓰기가 끊겨 남은 임시 파일 (그 안이 더 새 기록일 수 있다)."""
    return [str(pathlib.Path(x).with_name(pathlib.Path(x).name + TMP_SUFFIX)) for x in paths
            if os.path.lexists(pathlib.Path(x).with_name(pathlib.Path(x).name + TMP_SUFFIX))]


def _write_json_atomic(path, obj):
    """임시 파일에 쓰고 fsync → 이름 교체 → 디렉터리 fsync (⭐ DO 전 리뷰 P2-14 — 장부 · STOP · 실행 전 기록이 정전 뒤 빈 파일로 돌아오지 않게.
    저장장치 쓰기 캐시까지 보증하지는 않는다)."""
    path = pathlib.Path(path)
    tmp = path.with_name(path.name + ".tmp")
    with _critical():                                        # ⭐ 신호가 임시 파일을 만든 직후에 끼어들지 않게 (끝나고 받는다)
        fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)   # ⭐ DP 전 리뷰 (둘째) F2 — 남은 임시 파일 (앞 쓰기의 흔적) 을 덮지 않는다
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(json.dumps(obj, ensure_ascii=False, indent=1, default=str))
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp, path)
        except BaseException:
            try:
                os.unlink(tmp)                               # O_EXCL 로 우리가 만든 것만 — 교체 뒤면 이미 없다
            except OSError:
                pass
            raise
        if os.name == "posix":
            try:
                fd = os.open(str(path.parent), os.O_RDONLY)
                try:
                    os.fsync(fd)
                finally:
                    os.close(fd)
            except OSError as e_:                            # ⭐ 회신 DP P0-1 — 교체 뒤 실패는 '저장 실패' 가 아니다 (부르는 쪽이 되돌리지 않게 따로 알린다)
                raise _AfterReplace(f"교체 뒤 디렉터리 fsync 실패 ({type(e_).__name__}: {e_})") from e_


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
    state = {"h": None, "entry": None, "t0": None, "ledger": None, "stopped": False, "stop_pending": False, "stop_code": None}
    _CRIT[0] = 0; _PENDING.clear()                           # 앞 실행 (같은 프로세스의 시험) 이 남긴 구간 깊이 · 미룬 신호를 잇지 않는다
    def save_ledger():
        if state["ledger"] is not None:
            _write_json_atomic(led_p, state["ledger"])
    def stop(code, reason, **detail):
        rec = {"at": _now(), "code": code, "reason": reason, "terminal": code in TERMINAL_STOPS, **detail}
        rec["stop_id"] = hashlib.sha256(json.dumps(rec, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()[:16]
        with _critical():                                    # ⭐ 회신 DP P2-1 — STOP 저장과 종료 확정을 한 구간으로 (미룬 신호는 확정 뒤에 받는다)
            try:
                _write_json_atomic(stop_p, rec)
            except _AfterReplace:
                state["stopped"], state["stop_code"] = True, code   # 디스크에 이 STOP 이 있다 — 끝 처리가 덮지 않게 · 그 코드로 끝낸다
                raise
            state["stopped"], state["stop_code"] = True, code
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
    def persist_observed(obs, where):
        """⭐ 회신 DO P0 · DP 전 리뷰 F1 · F2 · F4 — 복구 · 확인 · 재판정 경로가 본 과학적 결과를 거부 **전에** 장부에 남긴다 (잠금 안 · 저장 ·
        실시간 감시 경로와 같은 보존). obs["kind"]:
          · melt — 그 행의 melt_check 를 fail 로 (앞 값은 melt_check_history 로 옮긴다 — 지우지 않는다) · 첫 시드면 closes_system.
          · verdict — 그 행의 verdict 가 비었으면 본 상태 (pass · fail) 를 적는다 (이미 있으면 덮지 않는다 — 다르면 호출자가 본다) ·
            판정의 closes_system 이고 첫 시드면 closes_system.
        행이 정확히 하나가 아니면 적지 않고 None (거부는 그대로). 행 꼴이 틀렸거나 (보관 목록이 목록이 아님 · closes_system 이 참거짓이
        아님 …) 저장이 실패하면 _PersistFailed — 메모리의 장부는 그대로 (복사본에 적고 다 되면 바꾼다) · 호출자가 거부 · invalid 로 멈춘다."""
        led_ = state["ledger"]
        hit_ = [r for r in led_.get("runs", []) if isinstance(r, dict) and r.get("run_id") == obs.get("run_id")]
        if len(hit_) != 1:
            log(f"  ⛔ 본 과학적 결과를 붙일 장부 행이 {len(hit_)} 개 (run_id {str(obs.get('run_id'))[:8]}) — 적지 못했다 (거부는 그대로)")
            return None
        r_ = hit_[0]
        first_ = r_.get("seed") == vals["first_seed"]
        try:
            new_ = copy.deepcopy(r_)
            cs0, mc0, mh0, v0 = new_.get("closes_system"), new_.get("melt_check"), new_.get("melt_check_history"), new_.get("verdict")
            if cs0 is not None and not isinstance(cs0, bool):
                raise ValueError(f"closes_system {cs0!r} 가 참거짓이 아니다")
            if mh0 is not None and not isinstance(mh0, list):
                raise ValueError(f"melt_check_history 가 목록이 아니다 ({type(mh0).__name__})")
            if mc0 is not None and not (isinstance(mc0, dict) and mc0.get("verdict") in ("fail", "invalid")):
                raise ValueError(f"melt_check {str(mc0)[:40]!r} 꼴이 아니다")
            if v0 not in mq.LEDGER_VERDICTS:                 # ⭐ DQ 전 리뷰 P1-A — 소비자와 같은 허용 값
                raise ValueError(f"verdict {v0!r} 를 모른다")
            vc0, vs0 = new_.get("verdict_observed_conflict"), new_.get("verdict_superseded")
            if vc0 is not None and not (isinstance(vc0, list) and all(isinstance(x_, dict) for x_ in vc0)):
                raise ValueError(f"verdict_observed_conflict 가 목록이 아니다 ({type(vc0).__name__})")
            if vs0 is not None and not (isinstance(vs0, list) and all(isinstance(x_, dict) for x_ in vs0)):
                raise ValueError(f"verdict_superseded 가 목록이 아니다 ({type(vs0).__name__})")
            if obs.get("kind") == "melt":
                if not (isinstance(mc0, dict) and mc0.get("verdict") == "fail"):
                    if mc0 is not None:
                        new_["melt_check_history"] = list(mh0 or []) + [mc0]
                    new_["melt_check"] = {"verdict": "fail", "message": obs.get("message"), "at": _now(), "observed_in": where,
                                          **{k: obs.get(k) for k in ("D_framework_cm2_s", "window_used_ps", "n_frames_read", "estimator")}}
                closes_, basis_ = first_, "first_seed_melt_window_check (복구 때 관측)"
            elif obs.get("kind") == "verdict" and obs.get("status") in ("pass", "fail"):
                cf_ = mq.ledger_verdict_conflict(r_, obs["status"], recorded=False,   # ⭐ DQ 전 리뷰 P1-A · P2-B — 소비자와 같은 함수
                                                 folder_provenance=obs.get("provenance"), folder_prior=obs.get("prior"))
                if cf_ is not None:                          # 장부를 덮지 않고 충돌 관측으로 남긴다 (호출자가 멈춘다)
                    ent_ = {"status": obs["status"], "closes_system": obs.get("closes_system") is True, "why": cf_}
                    if not any({k_: x_.get(k_) for k_ in ent_} == ent_ for x_ in (vc0 or [])):   # ⭐ 2차 N2 — 같은 관측은 한 번만 (재시작마다 늘지 않게)
                        new_["verdict_observed_conflict"] = list(vc0 or []) + [{**ent_, "in": where, "at": _now()}]
                    closes_, basis_ = False, None            # ⭐ 2차 N1 — 사람이 볼 충돌 관측으로는 계를 닫지 않는다 (그 관측의 closes 는 기록에만)
                else:
                    if v0 is None or v0 in ("invalid", "incomplete"):   # ⭐ 2차 N3 — 같은 원자료 · 카드 · 도구의 과학적 판정이 앞의 비과학적 판정을 대체
                        if v0 is not None:
                            new_["verdict_superseded"] = list(vs0 or []) + [{"from": v0, "to": obs["status"], "in": where, "at": _now(),
                                                                             "basis": "같은 원자료 · 카드 · 도구 (앞 판정은 판정 도중 오류로 못 끝남)"}]
                        new_["verdict"], new_["verdict_provenance"] = obs["status"], obs.get("provenance")
                        new_["verdict_observed"] = {"in": where, "at": _now()}
                    closes_, basis_ = first_ and obs.get("closes_system") is True, f"first_seed 판정 closes_system ({where} 에서 관측)"
            else:
                raise ValueError(f"모르는 관측 ({obs.get('kind')!r} · {obs.get('status')!r})")
            if closes_ and cs0 is not True:
                new_["closes_system"], new_["closes_basis"] = True, basis_
            changed_ = new_ != r_
            conflict_ = new_.get("verdict_observed_conflict") != r_.get("verdict_observed_conflict")
            if changed_:
                old_ = copy.deepcopy(r_)
                with _critical():                            # ⭐ 회신 DP P0-1 — 메모리 변경 → 저장 → 성공 확정을 한 구간으로 (저장 뒤 미룬 신호가 되돌림으로 안 간다)
                    r_.clear(); r_.update(new_)
                    try:
                        save_ledger()
                    except _AfterReplace:
                        raise                                # 디스크에 새 행이 있다 — 메모리를 되돌리지 않는다 (호출자는 그래도 멈춘다)
                    except BaseException:
                        r_.clear(); r_.update(old_)          # 교체 전 실패 — 메모리도 되돌린다 (끝 처리가 반쯤 적은 것을 저장하지 않게)
                        raise
        except Exception as e_:
            raise _PersistFailed(f"{type(e_).__name__}: {str(e_)[:120]}") from e_
        what_ = "녹음 fail (보존 폴더에서 계산)" if obs.get("kind") == "melt" else f"폴더 판정 {obs.get('status')}"
        tag_ = f"  ⭐ {r_.get('system')}{r_.get('seed')} 실행 {str(obs.get('run_id'))[:8]} 의 {what_} ({where})"
        if conflict_:                                        # ⭐ DQ 전 리뷰 P2-B — 한 일을 그대로 말한다
            log(f"{tag_} — 장부 판정 {r_.get('verdict')!r} 와 달라 덮지 않고 충돌 관측 (verdict_observed_conflict) 으로 적었다")
        elif changed_:
            log(f"{tag_} 을 장부에 적었다" + (" · 계의 첫 시드 — 그 계를 닫는다" if r_.get("closes_system") is True else ""))
        else:
            log(f"{tag_} — 장부에 이미 같은 기록이 있다 (그대로)")
        return r_
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
    state["stop_pending"] = os.path.lexists(stop_p)          # ⭐ DQ 전 리뷰 P2-A · DP 전 리뷰 F4 — 신호 처리기를 걸기 **전에**: 시작 점검 도중 신호가 와도
    #                                                          끝 처리가 확인 안 된 앞 STOP (닫는 STOP 포함) 을 덮지 않는다 (잠금 뒤라 다른 러너가 새로 못 쓴다)
    old = {}
    if threading.current_thread() is threading.main_thread():
        def _raise_sig(signum, frame):
            nm_ = signal.Signals(signum).name
            if _CRIT[0] > 0:                                 # ⭐ 쓰기 · 띄우기 구간 안 — 미뤘다가 구간 끝에서 던진다 (임시 파일 · 손잡이를 반쯤 남기지 않게)
                _PENDING.append(nm_)
                return
            if signum == signal.SIGINT:
                raise KeyboardInterrupt(f"신호 {nm_}")
            raise _RunnerSignal(f"신호 {nm_}")
        for sg in [getattr(signal, n_) for n_ in HELD_SIGNALS if hasattr(signal, n_)]:   # Windows 에는 SIGHUP 이 없다
            old[sg] = signal.signal(sg, _raise_sig)
    try:
        mq.mark_summary_not_current(R, "러너가 이 run_root 로 시작했다 (시작 점검 · 재판정 뒤에 새로 낸다)")   # ⭐ DQ 전 리뷰 P2-F — 거부해도 낡은 통과 요약이 안 남게
        left_ = _leftover_tmps(led_p, stop_p)
        if left_:                                            # ⭐ DP 전 리뷰 (둘째) F2 — 남은 임시 파일을 무시 · 덮지 않는다
            log(f"⛔ 앞 쓰기가 끊겨 남은 임시 파일이 있다 ({left_}) — 그 안이 더 새 장부 · 멈춤일 수 있다 · 시작하지 않는다 (사람이 보고 정리)")
            return RC["refused"]
        if not led_p.is_file():
            outs = sorted(str(x.relative_to(R)) for s_ in SYSTEMS for x in (R / s_).glob("seed*") if (R / s_).is_dir())
            if outs:                                         # ⭐ 회신 DH P0-1 — 비용을 모르는 산출물 위에 빈 장부를 만들지 않는다
                log(f"⛔ 산출물 {outs[:4]}{' …' if len(outs) > 4 else ''} 은 있는데 비용 장부 (stage1_ledger.json) 가 없다 — "
                    "빈 장부로 시작하지 않는다 (장부를 회수하거나 새 run_root)")
                return RC["refused"]
        if led_p.is_file():                                  # ⭐ 회신 DO P1 — 엄격히 읽는다 · 못 읽으면 state 에 안 넣고 거부 (끝 처리가 원본을 다시 쓰지 않게)
            try:
                led0_ = _loads_strict(led_p.read_text(encoding="utf-8"))
                shp_ = mq.ledger_shape_problems(led0_)       # ⭐ DP 전 리뷰 (둘째) F1 · 회신 DP P1-2 — 소비자와 같은 꼴 검사 (열쇠가 없어도 채워 넣지 않는다)
                if shp_:
                    raise ValueError("장부 꼴이 아니다 — " + " · ".join(shp_))
            except (OSError, ValueError, RecursionError) as e_:
                log(f"⛔ 비용 장부를 엄격히 못 읽는다 ({type(e_).__name__}: {str(e_)[:80]}) — 원본을 덮어쓰지 않고 시작하지 않는다 (사람이 본다)")
                return RC["refused"]
            state["ledger"] = led0_
        else:
            state["ledger"] = {"runs": [], "stop_history": []}
        led = state["ledger"]
        led.update({"decision": DECISION, "driver_sha16": mq.driver_sha16(), "card": CARD_REL, "cap_h": cap_base,   # ⭐ DQ 전 리뷰 P2-G — 판정을 낸
                    "card_values_sha16": mq.values_sha16(vals)})   # 도구 (불러온 모듈) 의 지문 · 소비자 _ledger_check 가 지금 도구 · 카드 값과 대조 (운영에선 = 고정값 s16)
        save_ledger()                                        # ⭐ DQ 전 리뷰 P2-G — 지문을 바로 디스크에 (①-4 묶음 판정이 디스크 장부를 읽는다 · 고정된 새 도구로 이어 갈 때도 맞게)
        # ①-1 STOP.json — 닫는 사건은 넘기지 않는다 · 나머지는 사람이 stop_id 로 확인해야 이어간다 (회신 DG P0-1)
        if os.path.lexists(stop_p):                          # (stop_pending 은 잠금 직후에 이미 켰다 — 지우기 전까지 끝 처리가 이 STOP 을 덮지 않는다)
            try:                                             # ⭐ DO 전 리뷰 P2-5 · P2-7 — 못 읽는 STOP 은 덮어쓰지 않고 거부 · stop_id 없는 STOP 을 조용히 넘기지 않는다
                st_sp, sp = mq.stop_record(R)                # ⭐ 회신 DQ P2-1 — 소비자와 같은 함수 (모르는 코드 · terminal 모순 = 판독 불가)
            except Exception as e:
                st_sp, sp = "unreadable", f"{type(e).__name__}: {str(e)[:80]}"
            if st_sp != "terminal" and st_sp != "open":
                log(f"⛔ STOP.json 을 받을 수 없다 ({str(sp)[:160]}) — 원본을 덮어쓰거나 확인으로 지우지 않고 시작하지 않는다 (사람이 본다)")
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
                obs_ = []
                dprob = ack_declaration_problems(decl, sp, led, vals, mq, R, observed=obs_)
                for o_ in obs_:                              # ⭐ 회신 DO P0 · DP 전 리뷰 F1 — 거부하기 전에 본 과학적 결과를 장부에
                    try:
                        persist_observed(o_, "확인 (--ack_stop) 의 선언 검사")
                    except _PersistFailed as e_:             # ⭐ DP 전 리뷰 F4 — STOP 은 그대로 · 장부도 그대로 · 거부
                        log(f"⛔ 확인 중 본 과학적 결과를 장부에 못 적었다 ({e_}) — 멈춤 · 장부를 그대로 두고 거부 (사람이 본다)")
                        return RC["refused"]
                if dprob:
                    log(f"⛔ 재시도 선언을 받지 않는다 — {' · '.join(dprob)} (멈춤은 그대로 · 고쳐서 다시 확인)")
                    return RC["refused"]
            if not any(isinstance(h_, dict) and h_.get("stop_id") == sp["stop_id"] and h_.get("acked_at") for h_ in led["stop_history"]):
                led["stop_history"].append({**{k_: sp[k_] for k_ in STOP_KEYS if k_ in sp}, "acked_at": _now(),
                                            **({"declaration": decl} if decl else {})})
            with _critical():                                # ⭐ 회신 DP — 확인 기록 저장 · STOP 지우기 · 확인 끝 표시를 한 구간으로
                save_ledger()                                # ⭐ DO 전 리뷰 P2-15 — 확인 기록을 먼저 남기고 STOP 을 지운다
                stop_p.unlink()
                state["stop_pending"] = False
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
        cl_bad = [f"{r.get('system')}{r.get('seed')}" for r in led["runs"]
                  if not (r.get("closes_system") is None or type(r.get("closes_system")) is bool)
                  or (r.get("closes_system") is True and r.get("seed") != vals["first_seed"])]
        if cl_bad:                                           # ⭐ DQ 전 리뷰 P2-D — 카드: 첫 시드 녹음만 계를 닫는다 (소비자 _ledger_check 와 같은 규칙)
            return stop("invalid", f"장부 closes_system 이 기록 규칙과 안 맞는다 ({cl_bad} — 첫 시드 ({vals['first_seed']}) 아님 · 참거짓 아님) — "
                                   "기록 오류 (사람이 본다 · 과학적 닫힘으로 읽지 않는다)")
        closed = [f"{r['system']}{r['seed']}" for r in led["runs"] if r.get("closes_system") is True]
        if closed:
            return stop("melt", f"장부에 계를 닫은 사건이 있다 ({closed} · 첫 시드 녹음 미충족) — 재시작으로 다시 열지 않는다")
        # ①-3b ⭐ 회신 DQ P1-2 — 정본 판정 없이 판정 기록 (이력 · 임시 파일) 만 남은 현재 시드 폴더가 하나라도 있으면 아무것도 띄우지 않는다
        #       (실행 순서와 무관하게 전부 먼저 본다 · 판정을 시도하지 않은 정상 미완료 폴더는 아니다 · 자동 승격 · 다시 판정하지 않는다)
        ur_all = [(s_, d_, f"{s_}{d_}", R / s_ / f"seed{d_}") for s_ in ("A", "B") for d_ in vals["seeds"]]
        ur_all = [(s_, d_, lab_, rd_, mq.unresolved_first_write(rd_)) for s_, d_, lab_, rd_ in ur_all]
        ur_all = [x_ for x_ in ur_all if x_[4]] + [(s_, d_, f"{s_}/{nm_}", R / s_ / nm_, why_)    # ⭐ DR 전 리뷰 P2-B · 2차 — 옆으로 옮긴 폴더도 (이름 꼴과
                                                   for s_, d_, nm_, why_ in mq.preserved_unresolved(R, vals["seeds"])]   # 무관 · 판독 불가 기준)
        if ur_all:
            for s_, d_, lab_, rd_, why_ in ur_all:           # ⭐ DR 전 2차 리뷰 P3 — 그 폴더에서 읽을 수 있는 과학적 결과는 멈추기 **전에** 장부에 (복구 · 확인 ·
                rid_ = _folder_run_id(rd_)                   # 재판정 경로와 같은 보존 — 폴더를 나중에 지우거나 옮겨도 장부에 남는다)
                rows_ = [r_ for r_ in led["runs"] if isinstance(r_, dict) and r_.get("run_id") == rid_] if rid_ else []
                if len(rows_) != 1:
                    continue
                rk_, rkd_ = mq.run_kind_detail(rows_[0], str(rd_), vals)
                if rk_ != "scientific" or rkd_.get("source") not in ("folder_verdict", "folder_melt_window"):
                    continue
                obs_ = ({"kind": "verdict", "run_id": rid_, "status": rkd_.get("status"), "closes_system": rkd_.get("closes_system") is True,
                         "provenance": rkd_.get("provenance"), "prior": rkd_.get("prior")} if rkd_.get("source") == "folder_verdict"
                        else {"kind": "melt", "run_id": rid_, **(rkd_.get("melt") or {})})
                try:
                    persist_observed(obs_, f"시작 점검 (①-3b) — 미해결 기록 폴더 {lab_}")
                except _PersistFailed as e_:
                    return stop("invalid", f"{lab_} 미해결 판정 기록 폴더의 과학적 결과를 장부에 못 적었다 ({e_}) — 사람이 본다", sys=s_, seed=d_, run_id=rid_)
            closed_ = [f"{r_['system']}{r_['seed']}" for r_ in led["runs"] if isinstance(r_, dict) and r_.get("closes_system") is True]
            if closed_:                                      # ⭐ DR 전 4차 리뷰 P3 — 방금 장부에 적은 관측이 계를 닫았으면 그 자리에서 닫는 STOP (다음 시작을 기다리지 않는다)
                return stop("melt", f"장부에 계를 닫은 사건이 있다 ({closed_} · 미해결 판정 기록 폴더에서 읽은 첫 시드 녹음 미충족) — 재시작으로 다시 열지 않는다")
            s_, d_, lab_, rd_, why_ = ur_all[0]
            rid0_ = _folder_run_id(rd_)
            row0_ = [r_ for r_ in led["runs"] if isinstance(r_, dict) and r_.get("run_id") == rid0_] if rid0_ else []
            if len(row0_) == 1:                              # ⭐ DR 전 3차 리뷰 P3 — 계 · 시드는 그 실행의 장부 행에서 (폴더 이름에서 읽지 않는다)
                s_, d_ = row0_[0].get("system"), row0_[0].get("seed")
            return stop("invalid", f"{lab_} 미해결 판정 기록 — {why_} · 같은 상태 {[x_[2] for x_ in ur_all]} — 새 실행 0 (순서를 바꿔도 · 폴더를 옆으로 "
                                   "옮겨도 같다 · 사람이 본다)",
                        sys=s_, seed=d_, run_id=rid0_)
        # ①-4 판정 파일을 믿지 않는다 — 원자료로 다시 판정 → 묶음 판정 (회신 DG P1-4)
        rejudged = []
        for sysn, seed in order:
            rd = R / sysn / f"seed{seed}"
            if (rd / "stage1_verdict.json").is_file():
                with _critical():                            # ⭐ DQ 전 리뷰 P2-E — 판정 파일 쓰기 (임시 → 교체) 가 신호로 반쯤 끊기지 않게
                    now_ = mq.stage1_verdict(rd, values=vals, log=lambda *m: None, reason="러너 재시작 — 판정 파일을 믿지 않고 원자료로 다시 판정")
                if now_.get("written") is False:             # ⭐ 회신 DP P1-1 — 다시 판정하지 못했다 (판정 임시 파일) = 보류 · 디스크의 옛 판정으로 가지 않는다
                    return stop("invalid", f"{sysn}{seed} 판정을 다시 쓰지 못했다 — {' · '.join((now_.get('reasons') or {}).get('invalid', []))[:200]}",
                                sys=sysn, seed=seed, run_id=_folder_run_id(rd))
                if now_.get("status") in ("pass", "fail") and isinstance(now_.get("run_id"), str):
                    rejudged.append((sysn, seed, now_))
                hh = now_.get("history") or {}
                ch = hh.get("changed") or {}
                log(f"  {sysn}{seed}: 판정 다시 냄 {hh.get('prev_status')} → {now_.get('status')}"
                    + (f" · ⚠ 지문 바뀜 (파일 {ch.get('files')} · 카드 값 {ch.get('card_values')} · 도구 {ch.get('driver')})"
                       if (ch.get("files") or ch.get("card_values") or ch.get("driver")) else "")
                    + f" — 이전 판정은 {mq.VERDICT_HISTORY}")
        for sysn, seed, now_ in rejudged:                    # ⭐ DP 전 리뷰 F2 — 재판정의 과학적 결과도 장부에 (첫 시드 닫힘 포함) · 장부 판정과 다르면 멈춤
            try:
                r_ = persist_observed({"kind": "verdict", "run_id": now_["run_id"], "status": now_["status"], "provenance": now_.get("provenance"),
                                       "prior": mq.folder_verdict_chain(R / sysn / f"seed{seed}"),   # ⭐ 4차 P1 — 폴더 판정 기록 전체
                                       "closes_system": now_.get("closes_system") is True}, "시작 전 재판정 (①-4)")
            except _PersistFailed as e_:
                return stop("invalid", f"{sysn}{seed} 재판정 결과를 장부에 못 적었다 ({e_}) — 사람이 본다", sys=sysn, seed=seed, run_id=now_["run_id"])
            cf_ = (mq.ledger_verdict_conflict(r_, now_["status"], recorded=False, folder_provenance=now_.get("provenance"),   # ⭐ DQ 전 리뷰 P1-A — 소비자와 같은 함수
                                              folder_prior=mq.folder_verdict_chain(R / sysn / f"seed{seed}"))
                   if r_ is not None else None)
            if cf_ is not None:
                return stop("invalid", f"{sysn}{seed} 재판정 {now_['status']} — {cf_} · 원자료 · 도구가 바뀌었을 수 있다 · "
                                       "장부를 덮지 않는다 (충돌 관측으로 남김 · 사람이 본다)", sys=sysn, seed=seed, run_id=now_["run_id"])
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
                try:                                         # ⭐ 회신 DO P1
                    sv = _loads_strict(vf.read_text(encoding="utf-8")).get("status")
                except (OSError, ValueError, AttributeError, RecursionError) as e_:
                    return stop("invalid", f"{sysn}{seed} 판정 파일을 엄격히 못 읽는다 ({type(e_).__name__}) — 덮어쓰지 않는다 · 사람이 본다",
                                sys=sysn, seed=seed, run_id=_folder_run_id(rd))
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
                    if el_.get("observed"):                      # ⭐ 회신 DO P0 · DP 전 리뷰 F1 · F2 — 거부하기 전에 장부에 · 첫 시드면 그 계를 닫는다
                        try:
                            r_ = persist_observed(el_["observed"], "재시도 자격 검사")
                        except _PersistFailed as e_:
                            return stop("invalid", f"{sysn}{seed}: 앞 실행에서 본 과학적 결과를 장부에 못 적었다 ({e_}) — 다시 담금질하지 않는다 · "
                                                   "사람이 본다", sys=sysn, seed=seed, run_id=attempts[-1].get("run_id"))
                        if r_ is not None and r_.get("closes_system") is True:
                            src_ = ("녹음 창이 다 찼고 fail — 복구 때 보존 폴더에서 계산" if el_["observed"].get("kind") == "melt"
                                    else "폴더 판정 기록이 그 계를 닫는다 (closes_system)")
                            return stop("melt", f"{sysn}{seed} (계의 첫 시드) 앞 실행의 {src_} · 장부에 먼저 적었다 · 그 계가 닫혀 트랙 전체 멈춤",
                                        sys=sysn, seed=seed, run_id=r_.get("run_id"))
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
            with _critical():                                # ⭐ 회신 DP — 폴더 · 실행 전 기록 · 장부 행을 한 구간으로 (그 사이 신호로 장부에 없는 폴더를 안 남긴다)
                rd.mkdir(parents=True, exist_ok=False)
                _write_json_atomic(rd / mq.ATTEMPT_NAME, {"system": sysn, "seed": seed, "run_id": rid,
                                                         "retry_of": retry_of, "retry_stop_id": retry_stop, "retry_kind": retry_kind})
                ent = {"system": sysn, "seed": seed, "run_id": rid, "start": _now(), "start_epoch": wall(), "pgid": None,
                       "start_recovery_clock": recovery_clock(), "retry_of": retry_of, "retry_stop_id": retry_stop, "retry_kind": retry_kind,
                       "status": "starting", "end": None, "wall_h": None, "wall_h_so_far": 0.0, "cum_before_h": cum}
                led["runs"].append(ent); state["entry"], state["t0"] = ent, t0
                save_ledger()
            def _launch_and_record():                        # ⭐ DO 전 리뷰 P2-9 — 신호는 손잡이를 적은 뒤에 받는다 (띄운 자식을 놓치지 않게)
                with _critical():                            # ⭐ DP 전 리뷰 (둘째) F4 — 다른 스레드가 받은 신호도 (처리기는 주 스레드) 구간 끝에서
                    h_ = launch(cmd, R / f"quench_{sysn}{seed}.log")
                    state["h"] = h_
                    ent.update(pgid=getattr(h_, "pid", None), status="running")
                    save_ledger()                            # ⭐ 띄운 직후 — 러너가 죽어도 시작 사실이 남는다 (회신 DG P0-2)
                return h_
            h = _held(_launch_and_record)                    # ⭐ 회신 DO P2 — 자식은 막기 전 마스크로 (_Proc preexec)
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
                        with _critical():                    # ⭐ DQ 전 리뷰 P2-E — 판정 파일 쓰기를 신호로 반쯤 끊지 않게
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
                        with _critical():                    # ⭐ DQ 전 리뷰 P2-E · 3차 P1 — 판정 쓰기 · 장부 적기 · 저장을 한 구간으로 (그 사이 신호로 장부가 비지 않게)
                            v = mq.stage1_verdict(rd, values=vals, log=log, reason=f"첫 시드 녹음 판정 {mw['verdict']} — 러너가 멈춤")
                            ent["verdict"], ent["verdict_provenance"] = v.get("status"), v.get("provenance")   # ⭐ DQ 전 2차 리뷰 N3 — 장부 판정의 지문
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
            with _critical():                                # ⭐ DQ 전 리뷰 P2-E · 3차 P1 — 끝 판정 쓰기 · 장부 적기 · 저장을 한 구간으로 (판정을 쓴 뒤 신호로
                v = mq.stage1_verdict(rd, values=vals, log=log, reason="담금질 끝")   # 장부 판정이 비면 보류 규칙이 비교할 것이 없어진다)
                if v.get("written") is not False:
                    ent["verdict"], ent["closes_system"] = v.get("status"), bool(v.get("closes_system"))
                    ent["verdict_provenance"] = v.get("provenance")  # ⭐ DQ 전 2차 리뷰 N3 — 그 판정이 기댄 원자료 · 카드 · 도구 (뒤 재판정이 대체할 수 있는지 가른다)
                    save_ledger()
            if v.get("written") is False:                    # ⭐ 회신 DP P1-1 — 판정을 쓰지 못했다 (판정 임시 파일) = 보류
                return stop("invalid", f"{sysn}{seed} 판정을 쓰지 못했다 — {' · '.join((v.get('reasons') or {}).get('invalid', []))[:200]}",
                            sys=sysn, seed=seed, run_id=rid)
            if cum + el > cap:                               # 끝난 뒤에도 넘었으면 통과로 올리지 않는다 (회신 DG P0-3)
                return stop("cap", f"{sysn}{seed} 가 끝났을 때 누적 {cum + el:.1f} h > 상한 {cap:g} h — 미완결 (통과로 올리지 않는다)",
                            sys=sysn, seed=seed, cum_h=cum + el, cap_h=cap, run_id=rid)
            mw_end = (v.get("melt_window_check") or {}).get("verdict") if isinstance(v.get("melt_window_check"), dict) else None
            if need_melt and v.get("closes_system") is not True and mw_end != "pass":   # ⭐ DP 전 리뷰 (둘째) F5 — 첫 시드가 판정 없이 끝남
                return stop("invalid", f"{sysn}{seed} (계의 첫 시드) 가 끝났는데 녹음 판정이 정해지지 않았다 (끝 판정의 녹음 {mw_end!r}) — "
                                       "자료 · 판독 문제 (과학적 종료 아님 · 사람이 본다)", sys=sysn, seed=seed, run_id=rid, verdict=v.get("status"))
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
        if state.get("stop_pending"):                        # ⭐ DP 전 리뷰 F4 · (둘째) F6 — 확인 안 된 앞 STOP 을 덮지 않는다
            log(f"  ⛔ 확인 안 된 앞 STOP.json 이 있는 채로 끊겼다 ({why}) — 그 STOP 을 그대로 둔다 (덮지 않는다 · 다시 확인)")
        elif not state["stopped"]:
            stop("interrupted", f"러너 중단 — {why} · " + ("돌던 담금질 그룹을 비웠다" if cl.get("group_empty")
                                                         else f"⛔ 담금질 그룹이 남았을 수 있다 (pid {cl.get('left')}) — 손으로 본다")
                 + " · 그 시드 폴더는 사람이 정한다", cleanup=cl, run_id=ent_rid)
        elif state.get("stop_code") in RC:                   # ⭐ DQ 전 리뷰 P3 — 이 실행이 STOP 을 쓴 뒤 끊겼으면 (교체 뒤 실패 · 미룬 신호) 그 STOP 의 코드로
            return RC[state["stop_code"]]
        return RC["interrupted"]
    finally:
        try:
            stop_child("러너가 끝난다")
        finally:
            try:
                save_ledger()
            except Exception as e_:                          # ⭐ DP 전 리뷰 F4 — 끝 저장 실패로 멈춤 코드 · 잠금 정리를 잃지 않는다 (디스크 장부는 앞 저장 그대로)
                log(f"  ⛔ 끝 처리에서 장부를 못 저장했다 ({type(e_).__name__}: {str(e_)[:100]}) — 디스크의 장부는 앞 저장 그대로 · 사람이 본다")
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
                if launch_signal == "direct":                # 다른 스레드가 받은 신호 — 파이썬 처리기가 주 스레드에서 바로 돈다 (부모 마스크와 무관 · 깨기 DP68)
                    signal.getsignal(signal.SIGTERM)(signal.SIGTERM, None)
                else:
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
            pv_np = {**PASSV["provenance"], "card_values_sha16": real.values_sha16(vals_t), "driver_sha16": real.driver_sha16()}   # DR 전 4차 P2 — 지금
            (d / "stage1_verdict.json").write_text(json.dumps({**PASSV, "provenance": pv_np}), encoding="utf-8")   # 카드 · 도구로 낸 pass (과학적 기록)
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
    _write_json_atomic(rr0 / "stage1_ledger.json", {"runs": [], "stop_history": []})
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
                                                               "wall_h_so_far": 1.5}], "stop_history": []})
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
    r1 = clone(rr_d); _write_json_atomic(r1 / "stage1_ledger.json", {"runs": [], "stop_history": []})
    r2 = clone(rr_d); _write_json_atomic(r2 / "stage1_ledger.json", {**led0, "runs": led0["runs"][1:]})
    r3 = clone(rr_d); _write_json_atomic(r3 / "stage1_ledger.json", {**led0, "runs": [dict(x, wall_h=-10.0) for x in led0["runs"]]})
    r4 = clone(rr_d); _write_json_atomic(r4 / "stage1_ledger.json", {**led0, "runs": [dict(x, end=None, status="running") for x in led0["runs"]]})
    r5 = clone(rr_d); _write_json_atomic(r5 / "stage1_ledger.json", {**led0, "runs": [dict(x, cost_basis="lower_bound") for x in led0["runs"]]})
    t1, t2, t3, t4, t5 = (summ(x)["track"] for x in (r1, r2, r3, r4, r5))
    chk(t1 == t2 == t3 == t5 == "invalid" and t4 == "pending" and summ(rr_d)["track"] == "stage1_pass",
        f"⛔음성 DH P0-1: 빈 장부 · 한 행 누락 · 음수 비용 · 하한 근거 → 무효 · 모든 행이 안 끝남 → 대기 ({t1} · {t2} · {t3} · {t5} · {t4})")
    # 같은 반례가 각자의 검사로 무효인지 (다른 검사가 먼저 잡아 가리지 않게 — 깨기 D22 · D23 이 드러낸 시험 구멍)
    s2_, s3_ = summ(r2), summ(r3)
    has_ = lambda s_, w: s_["track"] == "invalid" and any(w in x for x in (s_.get("cost") or {}).get("invalid") or [])
    chk(has_(s2_, "비용이 안 잡힌 실행") and has_(s3_, "유한한 비음수"),
        "⛔음성 DH P0-1 (이유): 장부에서 빠진 행의 판정 → '판정의 run_id 가 장부에 없다' · 음수 비용 → '유한한 비음수가 아니다' "
        f"({[x for x in (s2_.get('cost') or {}).get('invalid') or []][:3]} · {[x for x in (s3_.get('cost') or {}).get('invalid') or []][:3]})")
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
    (c_d / "B/seed13" / real.VERDICT_HISTORY).unlink()       # ⭐ 5차 P2 뒤 — 첫 판정도 이력에 남으니 '판정한 적 없음' 은 이력까지 없는 상태다
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
    for f_ in ("stage1_verdict.json", "final.xyz", "result.json", real.VERDICT_HISTORY):   # ⭐ 5차 P2 뒤 — 판정한 적 없는 상태 = 이력도 없음
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
    def _dup_n(d):                                           # ⭐ 회신 DO P1-1 — 판정 기록의 프레임 수에 같은 열쇠 둘 ("n": 130, "n": 71)
        vf_ = d / "stage1_verdict.json"; vv_ = J(vf_); n_ = vv_["checks"]["traj_frames"]["n"]
        t_ = json.dumps(vv_, ensure_ascii=False); a_ = f'"traj_frames": {{"n": {n_},'
        assert a_ in t_, "fixture: traj_frames 꼴"
        vf_.write_text(t_.replace(a_, f'"traj_frames": {{"n": {n_}, "n": 71,', 1), encoding="utf-8")
    def _hist_sched_dup(d):                                  # ⭐ 회신 DO P1-1 — 보존 이력의 이전 판정에 schedule_complete: true, false
        _post_md_gone(d)
        _note_md_judge(_judge_as_seed(d, "selftest — MD 완료 · FIRE 미완 판정"))
        _cut_front(d)
        _judge_as_seed(d, "selftest — 꼬리 소실 뒤 재판정")
        hp_ = d / real.VERDICT_HISTORY; t_ = hp_.read_text(encoding="utf-8")
        assert '"schedule_complete": true' in t_, "fixture: 이력의 일정 끝 흔적"
        t_ = t_.replace('"schedule_complete": true', '"schedule_complete": true, "schedule_complete": false', 1)
        m_ = re.search(r'"traj_frames": \{"n": (\d+), "expected": (\d+)\}', t_)   # 마지막 값만 보면 완료 흔적이 다 사라지게 (프레임 수도 둘)
        assert m_ and m_.group(1) == m_.group(2), "fixture: 이력의 프레임 다 참 흔적"
        t_ = t_.replace(m_.group(0), f'"traj_frames": {{"n": {m_.group(1)}, "n": 2, "expected": {m_.group(2)}}}', 1)
        hp_.write_text(t_, encoding="utf-8")
    def _rejudge_over_dup(d):                                # ⭐ 회신 DO P1-1 — 같은 열쇠 둘인 현재 판정 위에 재판정 → 이력에 원문 (정규화 안 함)
        _frames_only(d, as_str=False); _dup_n(d)
        _judge_as_seed(d, "selftest — 같은 열쇠 둘 판정 위에 재판정")
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
                           ("frames_only_dup", lambda d: (_frames_only(d, as_str=False), _dup_n(d)), False),   # ⭐ 회신 DO P1-1 ("n": 130, "n": 71)
                           ("hist_sched_dup", _hist_sched_dup, False),                                        # ⭐ 회신 DO P1-1 (이력 true, false)
                           ("rejudge_over_dup", _rejudge_over_dup, False),                                    # ⭐ 회신 DO P1-1 (재판정이 원문 보존)
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
        held_ = any(w_ in (sp_.get("reason") or "") for w_ in ("완료 단계를 못 읽는다", "과학적 판정", "판정을 못 읽는다",
                                                                "미해결 판정 기록"))   # ⭐ DR 전 리뷰 P2-B — 보존 폴더의 못 읽는 기록은 시작 점검이 먼저 막는다
        (dm_ctrl if ctrl else dm_cases)[nm_] = (rc_x if not held_ else "held", len(L_x), held_, st0, snap() == before)
    chk(all(v_ == ("held", 0, True, "unreadable", True) for v_ in dm_cases.values())
        and dm_ctrl["ctrl_noplan_judged"][:2] == (0, 1) and dm_ctrl["ctrl_noplan_judged"][3] == "no_plan"
        and dm_ctrl["ctrl_mid_cut"][:2] == (0, 1) and dm_ctrl["ctrl_mid_cut"][3] == "md_incomplete"
        and all(v_[4] for v_ in dm_ctrl.values()),
        f"⛔음성 DM P0-1 · P0-2 (Codex 재현): 궤적 앞부분 + thermo 에 온전한 끝 시각 행 · pass 판정이 있던 폴더를 원자료 소실 뒤 재판정 · "
        f"pass 판정이 임시 파일에만 · (같은 갈래) MD 완료 · FIRE 미완 폴더를 진짜 판정한 뒤 완료 기록 · 꼬리 소실 · (회신 DN P1) thermo 없는 "
        f"폴더의 같은 판정 — 프레임 수 정수 그대로 · n 만 글자로 → 선언이 맞아도 재담금질 0 · "
        f"보류 · 폴더 그대로 / 대조: 진짜 plan 전 판정만 · 명확한 도중 끊김 → 재시도 1 · rc 0 ({dm_cases} · {dm_ctrl})")
    c_rj = clone(c_m); fr_rj = c_rj / "B/seed13.fire_cut"; _rejudge_over_dup(fr_rj)
    hl_rj = [json.loads(x_) for x_ in (fr_rj / real.VERDICT_HISTORY).read_text(encoding="utf-8").splitlines() if x_.strip()][-1]
    import base64 as _b64
    chk(hl_rj.get("prev_status") is None and b'"n": 71' in _b64.b64decode((hl_rj.get("prev") or {}).get("raw_b64") or "")
        and real.folder_stage(fr_rj) == "unreadable",
        "⛔음성 회신 DO P1-1: 같은 열쇠 둘인 판정 위에 다시 판정하면 이전 판정을 마지막 값으로 정규화하지 않고 원문 (raw_b64 · 바이트 그대로) 으로 이력에 남긴다 → "
        f"그 폴더는 보류 ({hl_rj.get('prev_status')} · {real.folder_stage(fr_rj)})")
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
    wt_dd = pathlib.Path(tempfile.mkdtemp(dir=tmp_root)); (wt_dd / "db/governance").mkdir(parents=True)   # ⭐ 회신 DO P1 — 결정 원장도 엄격히
    (wt_dd / "db/governance/decisions.json").write_text('{"decisions": [{"id": "' + DECISION + '", "decision_state": "proposed", '
                                                        '"decision_state": "active"}]}', encoding="utf-8")
    st_dup = decision_state(wt_dd)
    (wt_dd / "db/governance/decisions.json").write_text(json.dumps({"decisions": [{"id": DECISION, "decision_state": "active"}]}), encoding="utf-8")
    st_ok = decision_state(wt_dd)
    chk(st_dup is None and st_ok == "active",
        f"⛔음성 회신 DO P1: 결정 원장에 같은 열쇠 둘 (decision_state proposed · active) 이면 '모름' (시작하지 않는다) · 대조는 active ({st_dup} · {st_ok})")
    # ⭐ 회신 DO P1-2 (Codex 재현) — 같은 열쇠 둘인 장부를 러너 · 증언이 정상 꼴로 다시 쓰지 않는다 (원본 바이트 그대로 · 두 번째 실행도 거부)
    c_dw = clone(rr_d); lp_dw = c_dw / "stage1_ledger.json"
    t_dw = lp_dw.read_text(encoding="utf-8"); assert '"wall_h": ' in t_dw, "fixture: wall_h"
    lp_dw.write_text(t_dw.replace('"wall_h": ', '"wall_h": 999.0, "wall_h": ', 1), encoding="utf-8"); b_dw = lp_dw.read_bytes()
    s_dw0 = summ(c_dw)["track"]
    rc_dw1, L_dw1, _ = go(wt, rr=c_dw); same1 = lp_dw.read_bytes() == b_dw
    rc_dw2, L_dw2, _ = go(wt, rr=c_dw); same2 = lp_dw.read_bytes() == b_dw
    s_dw1 = summ(c_dw)["track"]
    rr_dl, rid_dl = orphan_root(5.0); lp_dl = rr_dl / "stage1_ledger.json"
    t_dl = lp_dl.read_text(encoding="utf-8"); assert '"wall_h_lower": 5.0' in t_dl, "fixture: wall_h_lower"
    lp_dl.write_text(t_dl.replace('"wall_h_lower": 5.0', '"wall_h_lower": 99.0, "wall_h_lower": 5.0', 1), encoding="utf-8"); b_dl = lp_dl.read_bytes()
    rc_dl_view, _ = attest_cost(rr_dl, rid_dl, vals_t)
    rc_dl1, _ = attest_cost(rr_dl, rid_dl, vals_t, hours=6.0, fields=ATT)
    rc_dl2, _ = attest_cost(rr_dl, rid_dl, vals_t, hours=6.0, fields=ATT)
    same_dl = lp_dl.read_bytes() == b_dl
    chk(s_dw0 == "invalid" and rc_dw1 == RC["refused"] and rc_dw2 == RC["refused"] and not L_dw1 and not L_dw2 and same1 and same2
        and s_dw1 == "invalid" and rc_dl_view == 10 and rc_dl1 == 10 and rc_dl2 == 10 and same_dl and summ(rr_dl)["track"] == "invalid",
        "⛔음성 회신 DO P1-2 (Codex 재현): 장부에 wall_h 가 둘 → 러너가 거부하고 원본 바이트를 그대로 둔다 (두 번째 실행도 거부 · 소비자 무효 그대로) · "
        "고아 런 하한 wall_h_lower 가 둘 → 근거 보기 · 증언 모두 거부 · 원본 그대로 "
        f"({s_dw0} · {rc_dw1} · {rc_dw2} · {same1} · {same2} · {s_dw1} · {rc_dl_view} · {rc_dl1} · {rc_dl2} · {same_dl})")
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
    # ⭐ 회신 DO P0 (Codex 재현 그대로) — 복구 · 확인 경로가 계산한 녹음 fail 을 거부 전에 장부에 적는다 → 뒤에 궤적 원소를 손상해도
    #   원인 고침 선언 · 재담금질 · 1 단계 통과로 새지 않는다. 확인 경로 (폴더 제자리) · 재시도 자격 경로 (보존 폴더) 둘 다 · 첫 시드 · 둘째 시드
    def _damage_species(folder_):                            # 궤적 첫 프레임의 첫 원자 원소 기호를 바꾼다 (녹음 판정 invalid)
        tp_ = pathlib.Path(folder_) / "traj.xyz"
        ln_ = tp_.read_text(encoding="utf-8").splitlines(keepends=True)
        tok_ = ln_[2].split(None, 1)
        ln_[2] = ("Na " if tok_[0] != "Na" else "K ") + tok_[1]
        tp_.write_text("".join(ln_), encoding="utf-8")
    res_p = {}
    for nm_, sd_, scen_ in (("ack_first", 11, {("A", 11): {"melt": "fail", "polls": 8}}),
                            ("ack_second", 12, {("A", 12): {"melt": "fail", "polls": 8}}),
                            ("loop_first", 11, {("A", 11): {"melt": "fail", "polls": 8}}),
                            ("loop_second", 12, {("A", 12): {"melt": "fail", "polls": 8}})):
        rw_ = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
        go(wt, rr=rw_, scen=scen_, sleep_hook=_after_window(rw_, sd_))
        sw1_ = J(rw_ / "STOP.json")
        fd_ = rw_ / "A" / f"seed{sd_}"
        if nm_.startswith("ack"):                            # 확인 경로 — 폴더 제자리 · 정전 선언으로 확인 → 거부 (장부에 적힌다)
            rc2_, L2_, _ = go(wt, rr=rw_, ack=sw1_["stop_id"], declare=OUT)
            stop_after_ = sw1_
        else:                                                # 재시도 자격 경로 — 보존 폴더로 옮기고 선언 없이 확인 → 시드 루프에서 거부
            fd_.rename(fd_.with_name(f"seed{sd_}.cut1")); fd_ = fd_.with_name(f"seed{sd_}.cut1")
            rc2_, L2_, _ = go(wt, rr=rw_, ack=sw1_["stop_id"])
            stop_after_ = J(rw_ / "STOP.json")
        row_ = [x_ for x_ in J(rw_ / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", sd_)][-1]
        kept_ = ((row_.get("melt_check") or {}).get("verdict"), row_.get("closes_system") is True)
        _damage_species(fd_)
        mw_dmg_ = real.melt_window_check(fd_, values=vals_t, log=lambda *m: None)["verdict"]
        k_dmg_ = real.run_kind(row_, str(fd_), vals_t)
        rc3_, L3_, _ = go(wt, rr=rw_, ack=stop_after_["stop_id"], declare={**FIX, "rejudge_impossible_reason": "selftest"})
        sm_ = summ(rw_)
        res_p[nm_] = (rc2_, len(L2_), kept_, mw_dmg_, k_dmg_, rc3_, len(L3_), sm_["track"])
    exp_p = {"ack_first": (RC["refused"], 0, ("fail", True), "invalid", "scientific", RC["refused"], 0, "stop_track"),
             "ack_second": (RC["refused"], 0, ("fail", False), "invalid", "scientific", RC["refused"], 0, "pending"),
             "loop_first": (RC["melt"], 0, ("fail", True), "invalid", "scientific", RC["melt"], 0, "stop_track"),
             "loop_second": (RC["invalid"], 0, ("fail", False), "invalid", "scientific", RC["refused"], 0, "pending")}
    chk(res_p == exp_p,
        "⛔음성 회신 DO P0 (Codex 재현): 녹음 창이 다 찼고 fail 인 끊긴 런을 확인 · 재시도 검사가 계산하면 거부 전에 장부에 melt_check fail "
        "(첫 시드는 closes_system) 을 적는다 → 궤적 원소를 손상해 녹음 판정이 invalid 가 돼도 실행 종류는 과학적 · 원인 고침 선언으로 "
        f"재발사 0 · 1 단계 통과 아님 (첫 시드는 그 계가 닫힘) ({ {k: v for k, v in res_p.items() if v != exp_p[k]} })")
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
    # ⭐ 깨기 DP67 · DP68 이 드러낸 시험 구멍 — 두 미룸 구간 (쓰기 · 띄우고 손잡이 적기) 이 서로를 덮어 하나씩 끄면 안 잡혔다 → 따로 본다
    rc_sd, L_sd, rr_sd = go(wt, launch_signal="direct")
    es_d = J(rr_sd / "stage1_ledger.json")["runs"][0]
    chk(rc_sd == RC["interrupted"] and L_sd and L_sd[0].stopped and es_d.get("pgid") is not None and es_d.get("end") is not None,
        "⛔음성 DP 전 리뷰 (둘째) F4 · 깨기 DP68: 띄우는 구간 안에서 처리기가 바로 돌아도 (다른 스레드가 받은 신호 — 부모 마스크와 무관) 손잡이를 적은 "
        f"뒤에 받아 그 담금질을 멈추고 마감한다 ({rc_sd} · 멈춤 {bool(L_sd and L_sd[0].stopped)} · pgid {es_d.get('pgid')})")
    import types as _ty3
    _os0 = globals()["os"]
    st67 = {"armed": False, "fired": False}
    def _open_sig(path_, flags, *a_, **k_):
        fd_ = _os0.open(path_, flags, *a_, **k_)
        if st67["armed"] and not st67["fired"] and str(path_).endswith("stage1_ledger.json.tmp"):
            st67["fired"] = True                             # 임시 파일을 만든 직후 처리기가 돈다 (2026-11-04 실측 자리 · 다른 스레드가 받은 신호)
            signal.getsignal(signal.SIGTERM)(signal.SIGTERM, None)
        return fd_
    osp_ = _ty3.SimpleNamespace(**{k_: getattr(_os0, k_) for k_ in dir(_os0) if not k_.startswith("__")})
    osp_.open = _open_sig
    def _arm67(t_):
        if t_ >= 3600.0:                                     # 첫 poll 뒤 — 띄우기 구간 밖 (실행 중 장부 저장)
            st67["armed"] = True
    globals()["os"] = osp_
    try:
        rc67, L67, rr67 = go(wt, sleep_hook=_arm67)
    finally:
        globals()["os"] = _os0
    e67 = J(rr67 / "stage1_ledger.json")["runs"][0]
    chk(st67["fired"] and rc67 == RC["interrupted"] and not (rr67 / "stage1_ledger.json.tmp").exists() and L67 and L67[0].stopped
        and e67.get("status") == "interrupted",
        "⛔음성 DP 전 리뷰 (둘째) F2 · F4 · 깨기 DP67: 실행 중 장부 임시 파일을 만든 직후 처리기가 돌아도 쓰기를 마친 뒤 받는다 — 임시 파일이 안 남고 "
        f"그 담금질을 멈추고 마감 · 중단 STOP 까지 간다 ({st67['fired']} · {rc67} · {e67.get('status')})")
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
    c_cl = clone(rr_d)                                       # 장부에만 적힌 첫 시드 닫힘 — 폴더 판정은 닫힘을 모른다 (끊긴 런 · incomplete) · ⭐ 회신 DP: pass 면 같은 실행 충돌 (invalid · 아래)
    l_cl = J(c_cl / "stage1_ledger.json"); l_cl["runs"][0].update(closes_system=True, melt_check={"verdict": "fail", "message": "x"})
    _write_json_atomic(c_cl / "stage1_ledger.json", l_cl)
    v_cl = J(c_cl / "A/seed11/stage1_verdict.json"); v_cl["status"] = "incomplete"
    (c_cl / "A/seed11/stage1_verdict.json").write_text(json.dumps(v_cl, ensure_ascii=False), encoding="utf-8")
    s_close = summ(c_cl)
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
        if hasattr(signal, "pthread_sigmask"):               # ⭐ 회신 DO P2 — 러너와 같은 경로 (_held + _Proc) 로 띄운 자식은 종료 신호가 막히지 않는다
            code_m = ("import sys, time; open(sys.argv[1], 'w').write([l for l in open('/proc/self/status') if l.startswith('SigBlk')][0]); "
                      "time.sleep(600)")
            seen_ = {}
            def _mk_masked():
                seen_["parent_blocked"] = signal.SIGTERM in signal.pthread_sigmask(signal.SIG_BLOCK, [])
                return _Proc([sys.executable, "-c", code_m, str(tdp / "mask.txt")], tdp / "pm.log")
            prm = _held(_mk_masked)
            for _ in range(200):
                if (tdp / "mask.txt").is_file() and (tdp / "mask.txt").read_text().strip():
                    break
                time.sleep(0.05)
            blk_ = int((tdp / "mask.txt").read_text().split()[1], 16)
            child_term_blocked = bool(blk_ & (1 << (int(signal.SIGTERM) - 1)))
            parent_after = signal.SIGTERM in signal.pthread_sigmask(signal.SIG_BLOCK, [])
            t0_m = time.time(); r_m = prm.stop(grace_s=5); dt_m = time.time() - t0_m
            chk(seen_.get("parent_blocked") is True and not parent_after and not child_term_blocked and r_m["group_empty"]
                and r_m["signals"] == ["TERM"] and dt_m < 10,
                "⛔음성 회신 DO P2 (진짜 프로세스): 띄우는 동안 부모는 TERM 을 막지만 (_held) 자식은 막기 전 마스크로 시작한다 → TERM 만으로 "
                f"그룹이 빈다 (KILL 없음) · 부모 마스크도 돌아온다 (부모 막힘 {seen_.get('parent_blocked')} · 자식 SigBlk {blk_:#x} · "
                f"{r_m['signals']} · {dt_m:.1f} s)")
            # ⭐ DP 전 리뷰 (둘째) F4 — 러너가 TERM 막힌 채 시작됐어도 (물려받은 마스크) · _held 를 겹쳐 불러도 자식은 TERM 이 풀린 채 시작한다
            res_inh = {}
            for nm_, fn_ in (("inherited", lambda: _held(lambda: _Proc([sys.executable, "-c", code_m, str(tdp / "m_inh.txt")], tdp / "pi.log"))),
                             ("nested", lambda: _held(lambda: _held(lambda: _Proc([sys.executable, "-c", code_m, str(tdp / "m_nest.txt")],
                                                                                   tdp / "pn.log"))))):
                m0_ = signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGTERM] if nm_ == "inherited" else [])
                try:
                    pr_ = fn_()
                    pre_ok_ = _PRE_HOLD_MASK is None
                finally:
                    signal.pthread_sigmask(signal.SIG_SETMASK, m0_)
                mf_ = tdp / ("m_inh.txt" if nm_ == "inherited" else "m_nest.txt")
                for _ in range(200):
                    if mf_.is_file() and mf_.read_text().strip():
                        break
                    time.sleep(0.05)
                b_ = int(mf_.read_text().split()[1], 16)
                rr_s = pr_.stop(grace_s=5)
                res_inh[nm_] = (bool(b_ & (1 << (int(signal.SIGTERM) - 1))), rr_s["signals"], rr_s["group_empty"], pre_ok_)
            m_pre_ = signal.pthread_sigmask(signal.SIG_BLOCK, [])
            seen_in_ = _held(lambda: _held(lambda: _PRE_HOLD_MASK))
            seen_out_ = _held(lambda: (_held(lambda: None), _PRE_HOLD_MASK)[1])
            res_inh["nested_value"] = (seen_in_ == m_pre_, seen_out_ == m_pre_, _PRE_HOLD_MASK is None, True)
            chk(all(v_ == (False, ["TERM"], True, True) for v_ in res_inh.values() if len(v_) == 4 and v_ != (True, True, True, True))
                and res_inh["nested_value"] == (True, True, True, True),
                "⛔음성 DP 전 리뷰 (둘째) F4 (진짜 프로세스): 러너가 TERM 을 막은 채 시작해도 · _held 를 겹쳐 불러도 자식은 TERM 이 풀려 있다 → TERM 만으로 "
                f"그룹이 빈다 · 겹친 _held 뒤 막기 전 마스크 자리가 비워진다 ({res_inh})")
    # ⭐ DP 전 리뷰 F1 · F2 · F4 (첫째) — 폴더 판정 기록으로 본 과학적 결과 (사람이 보존 폴더 · 제자리에서 판정) 를 거부 전에 장부에 ·
    #   시작 전 재판정 (①-4) 결과도 장부에 · 장부와 다르면 멈춤 · 적다가 실패하면 STOP · 장부를 그대로 두고 거부 · invalid
    import types as _ty
    def mq_with(**over):
        ns_ = _ty.SimpleNamespace(**{k: getattr(real, k) for k in dir(real) if not k.startswith("__")})
        for k_, v_ in over.items():
            setattr(ns_, k_, v_)
        return ns_
    res_fv = {}
    for nm_, sd_, path_ in (("ack_first", 11, "ack"), ("ack_second", 12, "ack"), ("loop_first", 11, "loop"), ("loop_second", 12, "loop")):
        rw_ = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
        go(wt, rr=rw_, scen={("A", sd_): {"melt": "fail", "polls": 8}}, sleep_hook=_after_window(rw_, sd_))
        sw1_ = J(rw_ / "STOP.json")
        fd_ = rw_ / "A" / f"seed{sd_}"
        if path_ == "loop":
            fd_.rename(fd_.with_name(f"seed{sd_}.cut1")); fd_ = fd_.with_name(f"seed{sd_}.cut1")
        vj_ = real.stage1_verdict(fd_, values=vals_t, log=lambda *m: None, reason="selftest — 사람이 폴더를 판정")
        rkd_ = real.run_kind_detail([x_ for x_ in J(rw_ / "stage1_ledger.json")["runs"] if x_["seed"] == sd_ and x_["system"] == "A"][-1],
                                    str(fd_), None)
        stop_b = (rw_ / "STOP.json").read_bytes()
        if path_ == "ack":
            rc2_, L2_, _ = go(wt, rr=rw_, ack=sw1_["stop_id"], declare=OUT)
            stop_kept = (rw_ / "STOP.json").read_bytes() == stop_b
        else:
            rc2_, L2_, _ = go(wt, rr=rw_, ack=sw1_["stop_id"])
            stop_kept = J(rw_ / "STOP.json").get("code")
        row_ = [x_ for x_ in J(rw_ / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", sd_)][-1]
        res_fv[nm_] = (vj_["status"], rkd_[1].get("source"), rc2_, len(L2_), row_.get("verdict"), row_.get("closes_system") is True,
                       "verdict_observed" in row_, stop_kept)
    exp_fv = {"ack_first": ("fail", "folder_verdict", RC["refused"], 0, "fail", True, True, True),
              "ack_second": ("fail", "folder_verdict", RC["refused"], 0, "fail", False, True, True),
              "loop_first": ("fail", "folder_verdict", RC["melt"], 0, "fail", True, True, "melt"),
              "loop_second": ("fail", "folder_verdict", RC["invalid"], 0, "fail", False, True, "invalid")}
    chk(res_fv == exp_fv,
        "⛔음성 DP 전 리뷰 F1 · F2: 끊긴 런 폴더를 사람이 판정해 fail 이 나오면 (폴더 판정 기록) 확인 · 재시도 검사가 거부 전에 장부 verdict 에 적는다 · "
        "첫 시드면 closes_system → 재시도 경로는 STOP melt · 확인 경로는 거부 (STOP 그대로) · 발사 0 "
        f"({ {k: v for k, v in res_fv.items() if v != exp_fv[k]} })")
    rw_ = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))           # ①-4 — 제자리 판정 fail 을 재시작의 재판정이 장부에
    go(wt, rr=rw_, scen={("A", 12): {"melt": "fail", "polls": 8}}, sleep_hook=_after_window(rw_, 12))
    sw1_ = J(rw_ / "STOP.json")
    real.stage1_verdict(rw_ / "A/seed12", values=vals_t, log=lambda *m: None, reason="selftest — 제자리 판정")
    rc_rj, L_rj, _ = go(wt, rr=rw_, ack=sw1_["stop_id"])
    row_rj = [x_ for x_ in J(rw_ / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", 12)][-1]
    rc_d0, L_d0, rr_d0 = go(wt)                                  # 다 통과한 run_root — 장부 A13 판정을 fail 로 바꾸고 재시작
    led_d = J(rr_d0 / "stage1_ledger.json")
    for x_ in led_d["runs"]:
        if (x_["system"], x_["seed"]) == ("A", 13):
            x_["verdict"] = "fail"
    (rr_d0 / "stage1_ledger.json").write_text(json.dumps(led_d), encoding="utf-8")
    rc_d1, L_d1, _ = go(wt, rr=rr_d0)
    sd1_ = J(rr_d0 / "STOP.json")
    for x_ in led_d["runs"]:                                     # 같은 run_root — A13 행의 보관 목록을 망가뜨리면 재판정 결과를 못 적는다
        if (x_["system"], x_["seed"]) == ("A", 13):
            x_["verdict"] = "pass"; x_["melt_check_history"] = "x"
    (rr_d0 / "stage1_ledger.json").write_text(json.dumps(led_d), encoding="utf-8")
    rc_d2, L_d2, _ = go(wt, rr=rr_d0, ack=sd1_["stop_id"])
    sd2_ = J(rr_d0 / "STOP.json")
    chk(rc_rj == RC["pass"] and row_rj.get("verdict") == "fail" and "①-4" in str((row_rj.get("verdict_observed") or {}).get("in"))
        and rc_d0 == RC["pass"] and rc_d1 == RC["invalid"] and not L_d1 and "장부 판정 fail ≠ 폴더 판정 pass" in sd1_.get("reason", "")
        and rc_d2 == RC["invalid"] and not L_d2 and "못 적었다" in sd2_.get("reason", ""),
        "⛔음성 DP 전 리뷰 F2 · F4: 시작 전 재판정 (①-4) 의 fail 도 장부 verdict 에 적는다 · 재판정이 장부 판정과 다르면 덮지 않고 invalid 로 멈춘다 · "
        f"장부 행 꼴이 틀려 못 적으면 invalid ({rc_rj} · {row_rj.get('verdict')} · {rc_d1} · {sd1_.get('reason', '')[:60]} · {rc_d2})")
    res_pf = {}                                                  # 적다가 실패 — 일시 실패 (한 번만 · 되돌림) · 남은 임시 파일 (끝 저장도 실패) × 확인 경로 · 재시도 경로
    for nm_ in ("ack", "loop", "ack_left", "loop_left"):
        rw_ = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
        go(wt, rr=rw_, scen={("A", 12): {"melt": "fail", "polls": 8}}, sleep_hook=_after_window(rw_, 12))
        sw1_ = J(rw_ / "STOP.json")
        fd_ = rw_ / "A/seed12"
        if nm_.startswith("loop"):
            fd_.rename(fd_.with_name("seed12.cut1")); fd_ = fd_.with_name("seed12.cut1")
        real.stage1_verdict(fd_, values=vals_t, log=lambda *m: None, reason="selftest — 사람이 폴더를 판정")
        arm_ = {"on": False, "left": nm_.endswith("_left")}
        def _rkd_tmp(*a_, _rw=rw_, _arm=arm_, **k_):
            r_ = real.run_kind_detail(*a_, **k_)
            if r_[0] == "scientific":
                _arm["on"] = True
                if _arm["left"]:
                    (_rw / "stage1_ledger.json.tmp").write_text("{}", encoding="utf-8")   # 다른 기록자의 임시 파일 (끝 저장까지 실패)
            return r_
        _wja0 = globals()["_write_json_atomic"]
        def _wja_once(path_, obj_, _arm=arm_):               # 일시 실패 — 본 결과를 적는 첫 장부 저장만 (끝 저장은 성공)
            if _arm["on"] and not _arm["left"] and pathlib.Path(path_).name == "stage1_ledger.json":
                _arm["on"] = False
                raise OSError(28, "selftest — 공간 없음 (한 번)")
            return _wja0(path_, obj_)
        stop_b, led_b = (rw_ / "STOP.json").read_bytes(), (rw_ / "stage1_ledger.json").read_bytes()
        globals()["_write_json_atomic"] = _wja_once
        try:
            rc_pf, L_pf, _ = go(wt, rr=rw_, ack=sw1_["stop_id"], declare=OUT if nm_.startswith("ack") else None, mq=mq_with(run_kind_detail=_rkd_tmp))
        finally:
            globals()["_write_json_atomic"] = _wja0
        row_pf = [x_ for x_ in J(rw_ / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", 12)][-1]
        if nm_.startswith("ack"):
            res_pf[nm_] = (rc_pf, len(L_pf), (rw_ / "STOP.json").read_bytes() == stop_b, (rw_ / "stage1_ledger.json").read_bytes() == led_b,
                           row_pf.get("verdict"))
        else:
            res_pf[nm_] = (rc_pf, len(L_pf), J(rw_ / "STOP.json").get("code"), "못 적었다" in J(rw_ / "STOP.json").get("reason", ""),
                           row_pf.get("verdict"))
    exp_pf = {"ack": (RC["refused"], 0, True, True, None), "loop": (RC["invalid"], 0, "invalid", True, None),
              "ack_left": (RC["refused"], 0, True, True, None), "loop_left": (RC["invalid"], 0, "invalid", True, None)}
    chk(res_pf == exp_pf,
        "⛔음성 DP 전 리뷰 F4 · (둘째) F2 · F6: 본 결과를 장부에 적다가 저장이 실패하면 — 메모리도 되돌린다 (끝 저장이 반쯤 적은 것을 쓰지 않는다) · "
        "확인 경로는 거부 (앞 STOP · 장부 바이트 그대로) · 재시도 경로는 invalid 멈춤 (장부 판정 안 바뀜) · 남의 임시 파일로 끝 저장까지 실패해도 "
        f"러너가 죽지 않고 멈춤 코드를 낸다 ({ {k: v for k, v in res_pf.items() if v != exp_pf[k]} })")
    # ⭐ DP 전 리뷰 (둘째) F5 — 첫 시드가 녹음 판정 없이 끝나면 invalid (실시간 판정이 끝까지 미정 · 끝 판정의 녹음도 미정)
    _sv0 = real.stage1_verdict
    def _sv_undecided(rd_, **k_):
        v_ = _sv0(rd_, **k_)
        return {**v_, "melt_window_check": {"verdict": "incomplete", "message": "selftest — 미정"}}
    mq_u = mq_with(melt_window_check=lambda *a_, **k_: {"verdict": "incomplete", "message": "selftest — 미정"}, stage1_verdict=_sv_undecided)
    rc_u, L_u, rr_u = go(wt, mq=mq_u)
    su_ = J(rr_u / "STOP.json")
    chk(rc_u == RC["invalid"] and len(L_u) == 1 and su_.get("seed") == 11 and "정해지지 않았다" in su_.get("reason", ""),
        f"⛔음성 DP 전 리뷰 (둘째) F5: 계의 첫 시드가 녹음 판정 없이 끝나면 (실시간 · 끝 판정 둘 다 미정) 다음 시드로 넘어가지 않고 invalid ({rc_u} · {len(L_u)} · "
        f"{su_.get('reason', '')[:60]})")
    # ⭐ DP 전 리뷰 (둘째) F1 · F2 · F6 — 장부 꼴 · 남은 임시 파일 · 확인 중 예외
    res_sh = {}
    for nm_, led_txt in (("no_runs", '{"stop_history": []}'), ("no_hist", '{"runs": []}'), ("runs_elem", '{"runs": [1], "stop_history": []}'),
                         ("hist_elem", '{"runs": [], "stop_history": ["x"]}')):
        rw_ = pathlib.Path(tempfile.mkdtemp(dir=tmp_root)); (rw_ / "stage1_ledger.json").write_text(led_txt, encoding="utf-8")
        rc_s, L_s, _ = go(wt, rr=rw_)
        res_sh[nm_] = (rc_s, len(L_s), (rw_ / "stage1_ledger.json").read_text(encoding="utf-8") == led_txt)
    for nm_ in ("stage1_ledger.json.tmp", "STOP.json.tmp"):
        rw_ = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
        go(wt, rr=rw_, scen={("A", 11): {"raise_on_poll": 3}})
        (rw_ / nm_).write_text('{"newer": true}', encoding="utf-8")
        led_b = (rw_ / "stage1_ledger.json").read_bytes()
        rc_s, L_s, _ = go(wt, rr=rw_, ack=J(rw_ / "STOP.json")["stop_id"], declare=OUT)
        res_sh[nm_] = (rc_s, len(L_s), (rw_ / nm_).read_text(encoding="utf-8") == '{"newer": true}', (rw_ / "stage1_ledger.json").read_bytes() == led_b)
    rw_ = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
    (rw_ / "x.json.tmp").write_text("남의 것", encoding="utf-8"); (rw_ / "x.json").write_text("{}", encoding="utf-8")
    try:
        _write_json_atomic(rw_ / "x.json", {"a": 1}); w_ex = None
    except FileExistsError:
        w_ex = "FileExistsError"
    res_sh["write_excl"] = (w_ex, (rw_ / "x.json.tmp").read_text(encoding="utf-8"), (rw_ / "x.json").read_text(encoding="utf-8"))
    rc_at, L_at, rr_at = go(wt, scen={("A", 11): {"raise_on_poll": 3}})
    (rr_at / "stage1_ledger.json.tmp").write_text("{}", encoding="utf-8")
    rid_at = J(rr_at / "stage1_ledger.json")["runs"][0]["run_id"]
    led_b = (rr_at / "stage1_ledger.json").read_bytes()
    rc_a, info_a = attest_cost(rr_at, rid_at, vals_t, hours=1.0, fields=ATT)
    res_sh["attest_tmp"] = (rc_a, "임시 파일" in str(info_a.get("why")), (rr_at / "stage1_ledger.json").read_bytes() == led_b)
    rw_ = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))           # 확인 중 예외 — 앞 STOP 을 '중단' STOP 으로 덮지 않는다
    go(wt, rr=rw_, scen={("A", 11): {"raise_on_poll": 3}})
    stop_b = (rw_ / "STOP.json").read_bytes()
    def _inv_boom(*a_, **k_):
        raise RuntimeError("selftest — 확인 중 판독 예외")
    rc_x, L_x, _ = go(wt, rr=rw_, ack=json.loads(stop_b)["stop_id"], declare=OUT, mq=mq_with(attempt_inventory=_inv_boom))
    res_sh["ack_exception"] = (rc_x, len(L_x), (rw_ / "STOP.json").read_bytes() == stop_b)
    exp_sh = {"no_runs": (RC["refused"], 0, True), "no_hist": (RC["refused"], 0, True), "runs_elem": (RC["refused"], 0, True),
              "hist_elem": (RC["refused"], 0, True), "stage1_ledger.json.tmp": (RC["refused"], 0, True, True),
              "STOP.json.tmp": (RC["refused"], 0, True, True), "write_excl": ("FileExistsError", "남의 것", "{}"),
              "attest_tmp": (10, True, True), "ack_exception": (RC["interrupted"], 0, True)}
    chk(res_sh == exp_sh,
        "⛔음성 DP 전 리뷰 (둘째) F1 · F2 · F6: runs · stop_history 가 없거나 원소가 객체가 아닌 장부는 채워 넣지 않고 거부 (원본 그대로) · 앞 쓰기가 남긴 "
        "장부 · STOP 임시 파일이 있으면 거부 (임시 · 장부 그대로) · 원자 쓰기는 남은 임시 파일을 덮지 않는다 · 증언도 거부 · 확인 중 예외는 앞 STOP 을 "
        f"덮지 않는다 ({ {k: v for k, v in res_sh.items() if v != exp_sh[k]} })")
    # ⭐ 회신 DP P0-1 (Codex 재현) — 본 결과를 장부에 적은 **교체가 끝나는 순간** 미룬 신호 → 끝 처리가 옛 행을 다시 쓰지 않는다 ·
    #   그 뒤 궤적 손상 + 원인 고침 선언으로도 재담금질하지 않는다 (확인 · 재시도 × 첫 · 둘째 시드)
    import types as _ty4
    _os4 = globals()["os"]
    res_b = {}
    for nm_, sd_, path_ in (("ack_first", 11, "ack"), ("ack_second", 12, "ack"), ("loop_first", 11, "loop"), ("loop_second", 12, "loop")):
        rw_ = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
        go(wt, rr=rw_, scen={("A", sd_): {"melt": "fail", "polls": 8}}, sleep_hook=_after_window(rw_, sd_))
        sw1_ = J(rw_ / "STOP.json")
        fd_ = rw_ / "A" / f"seed{sd_}"
        if path_ == "loop":
            fd_.rename(fd_.with_name(f"seed{sd_}.cut1")); fd_ = fd_.with_name(f"seed{sd_}.cut1")
        arm_b = {"on": False, "fired": False}
        def _rkd_arm(*a_, _arm=arm_b, **k_):
            r_ = real.run_kind_detail(*a_, **k_)
            if r_[0] == "scientific" and not _arm["fired"]:
                _arm["on"] = True
            return r_
        def _replace_pend(src_, dst_, _arm=arm_b):
            _os4.replace(src_, dst_)
            if _arm["on"] and str(dst_).endswith("stage1_ledger.json"):
                _arm["on"], _arm["fired"] = False, True
                _PENDING.append("SIGTERM")                   # 처리기가 쓰기 구간 안에서 불려 미뤄 둔 상태 — 교체가 끝나는 순간 (Codex 주입 자리)
        osb_ = _ty4.SimpleNamespace(**{k_: getattr(_os4, k_) for k_ in dir(_os4) if not k_.startswith("__")}); osb_.replace = _replace_pend
        globals()["os"] = osb_
        try:
            rc2_, L2_, _ = go(wt, rr=rw_, ack=sw1_["stop_id"], declare=OUT if path_ == "ack" else None, mq=mq_with(run_kind_detail=_rkd_arm))
        finally:
            globals()["os"] = _os4
        row_ = [x_ for x_ in J(rw_ / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", sd_)][-1]
        kept_ = ((row_.get("melt_check") or {}).get("verdict"), row_.get("closes_system") is True)
        _damage_species(fd_)
        st_now = J(rw_ / "STOP.json")
        if path_ == "ack":
            rc3_, L3_, _ = go(wt, rr=rw_, ack=st_now["stop_id"], declare={**FIX, "rejudge_impossible_reason": "selftest"})
        else:
            rc3_, L3_, _ = go(wt, rr=rw_, ack=st_now["stop_id"])
        res_b[nm_] = (arm_b["fired"], rc2_, len(L2_), kept_, len(L3_), summ(rw_)["track"] != "stage1_pass")
    exp_b = {"ack_first": (True, RC["interrupted"], 0, ("fail", True), 0, True), "ack_second": (True, RC["interrupted"], 0, ("fail", False), 0, True),
             "loop_first": (True, RC["interrupted"], 0, ("fail", True), 0, True), "loop_second": (True, RC["interrupted"], 0, ("fail", False), 0, True)}
    chk(res_b == exp_b,
        "⛔음성 회신 DP P0-1 (Codex 재현): 본 녹음 fail 을 적은 장부 교체가 끝나는 순간 미룬 신호가 와도 — 메모리를 되돌리지 않고 (적기 · 확정을 한 구간) 끝 저장이 "
        "그 행을 지키고 (첫 시드는 closes_system) · 뒤 궤적 손상 + 원인 고침 선언으로도 재발사 0 · stage1_pass 아님 "
        f"({ {k: v for k, v in res_b.items() if v != exp_b[k]} })")
    # ⭐ 회신 DP P2-1 — terminal STOP (melt) 교체가 끝나는 순간 미룬 신호 → 끝 처리가 interrupted 로 덮지 않는다
    arm_s = {"fired": False}
    def _replace_stop(src_, dst_, _arm=arm_s):
        _os4.replace(src_, dst_)
        if not _arm["fired"] and str(dst_).endswith("STOP.json"):
            _arm["fired"] = True
            _PENDING.append("SIGTERM")
    oss_ = _ty4.SimpleNamespace(**{k_: getattr(_os4, k_) for k_ in dir(_os4) if not k_.startswith("__")}); oss_.replace = _replace_stop
    globals()["os"] = oss_
    try:
        rc_ps, L_ps, rr_ps = go(wt, scen={("A", 11): {"melt": "fail", "polls": 8}})
    finally:
        globals()["os"] = _os4
    sps_ = J(rr_ps / "STOP.json")
    chk(arm_s["fired"] and rc_ps == RC["melt"] and sps_.get("code") == "melt" and sps_.get("terminal") is True,
        f"⛔음성 회신 DP P2-1 · DQ 전 리뷰 P3: terminal STOP (melt) 교체가 끝나는 순간 미룬 신호가 와도 끝 처리가 interrupted 로 덮지 않고 · 그 STOP 의 코드로 끝난다 "
        f"({rc_ps} · {sps_.get('code')} · {sps_.get('terminal')})")
    # ⭐ 회신 DP P1-1 (Codex 재현) — 8 실행까지만 끝난 묶음 (상한 멈춤) 에서 A11 에 판정 임시 파일 · 깨진 이력 · 같은 열쇠 판정 → 추가 실행 0
    rc_8a, L_8a, rr_8a = go(wt)
    wl_ = [float(x_["wall_h"]) for x_ in J(rr_8a / "stage1_ledger.json")["runs"]]
    cap8 = sum(wl_[:8]) + max(wl_[:8] + [21.0]) - 0.5          # 8 번째 뒤 '누적 + 최악 > 상한' (7 번째 뒤는 아님)
    wt_8 = mk_wt(card=mk_card(stage1_cap_gpu_h=cap8))
    rc_8, L_8, rr_8 = go(wt_8)
    n8_ = len(J(rr_8 / "stage1_ledger.json")["runs"])
    def _vtmp(d_):
        (d_ / "stage1_verdict.json.tmp").write_text('{"status": "pass"}', encoding="utf-8")
    def _hist_broken(d_):
        with open(d_ / real.VERDICT_HISTORY, "a", encoding="utf-8") as fh_:
            fh_.write('{"prev": {"status": "fa\n')
    def _dup_verdict(d_):
        vf_ = d_ / "stage1_verdict.json"; t_ = vf_.read_text(encoding="utf-8")
        vf_.write_text(t_.replace('"status": "pass"', '"status": "fail", "status": "pass"', 1), encoding="utf-8")
    res_8 = {}
    for nm_, fn_ in (("verdict_tmp", _vtmp), ("history_broken", _hist_broken), ("dup_key_verdict", _dup_verdict)):
        c8_ = clone(rr_8)
        fn_(c8_ / "A/seed11")
        s8_ = J(c8_ / "STOP.json")
        rc_x8, L_x8, _ = go(wt, rr=c8_, ack=s8_["stop_id"])          # 상한을 올린 카드 (230 h) 로 상한 멈춤을 확인하고 이어가려 한다
        res_8[nm_] = (len(L_x8), rc_x8, summ(c8_)["track"])
        if nm_ == "verdict_tmp":
            res_8["verdict_tmp_reason"] = "다시 쓰지 못했다" in J(c8_ / "STOP.json").get("reason", "")
    chk(rc_8 == RC["cap"] and n8_ == 8 and res_8.pop("verdict_tmp_reason", False) is True
        and all(v_ == (0, RC["invalid"], "invalid") for v_ in res_8.values()),
        "⛔음성 회신 DP P1-1 (Codex 재현): 8 실행까지만 끝난 묶음에서 A11 에 판정 임시 파일 (다시 판정 못 함 · written False) · 깨진 이력 줄 · 같은 열쇠 판정 "
        f"(재판정 뒤 원문만 남은 이전 판정) → 새 실행 0 · invalid 멈춤 · 요약 invalid ({rc_8} · {n8_} 실행 · {res_8})")
    # ⭐ 회신 DP P1-2 (Codex 재현) — 러너가 거부하는 장부 상태를 독립 요약도 통과시키지 않는다 (invalid · 2 단계 없음)
    def _sum_case(fn_):
        c_ = clone(rr_d); fn_(c_); r_ = summ(c_)
        return (r_["track"], r_.get("stage2"))
    def _led_tmp(c_):
        l_ = J(c_ / "stage1_ledger.json"); l_["runs"][0].update(melt_check={"verdict": "fail"}, closes_system=True)
        (c_ / "stage1_ledger.json.tmp").write_text(json.dumps(l_), encoding="utf-8")
    def _stop_tmp(c_):
        (c_ / "STOP.json.tmp").write_text(json.dumps({"code": "melt", "terminal": True, "stop_id": "x" * 16}), encoding="utf-8")
    def _same_run_fail(c_):
        l_ = J(c_ / "stage1_ledger.json"); l_["runs"][2]["verdict"] = "fail"; _write_json_atomic(c_ / "stage1_ledger.json", l_)
    def _same_run_melt(c_):
        l_ = J(c_ / "stage1_ledger.json"); l_["runs"][2]["melt_check"] = {"verdict": "fail"}; _write_json_atomic(c_ / "stage1_ledger.json", l_)
    def _no_hist(c_):
        l_ = J(c_ / "stage1_ledger.json"); l_.pop("stop_history", None)
        (c_ / "stage1_ledger.json").write_text(json.dumps(l_), encoding="utf-8")
    def _hist_dict(c_):                                      # ⭐ DQ 깨기 설계 — 빈 객체 stop_history 는 뒤 원소 검사가 못 본다 (꼴 검사만 잡는다)
        l_ = J(c_ / "stage1_ledger.json"); l_["stop_history"] = {}
        (c_ / "stage1_ledger.json").write_text(json.dumps(l_), encoding="utf-8")
    res_s = {k_: _sum_case(f_) for k_, f_ in (("ledger_tmp", _led_tmp), ("stop_tmp", _stop_tmp), ("same_run_fail", _same_run_fail),
                                               ("same_run_melt_fail", _same_run_melt), ("no_stop_history", _no_hist),
                                               ("stop_history_empty_obj", _hist_dict))}
    s_ok_ = summ(clone(rr_d))
    chk(s_ok_["track"] == "stage1_pass" and all(v_ == ("invalid", None) for v_ in res_s.values()),
        "⛔음성 회신 DP P1-2 (Codex 재현): 다 통과한 묶음에 장부 임시 파일 (A11 녹음 fail · 닫힘) · STOP 임시 파일 · 같은 실행의 장부 fail ↔ 폴더 pass · "
        f"장부 녹음 fail ↔ 폴더 pass · stop_history 누락 · 빈 객체 → 독립 요약도 invalid · 2 단계 없음 (손 안 댄 묶음은 통과) ({s_ok_['track']} · {res_s})")
    # ⭐ 회신 DP P0-1 · P2-1 (교체 뒤 실패) — 파일 교체는 끝났는데 디렉터리 fsync 가 실패하면 (_AfterReplace) 메모리를 되돌리지 않고 · STOP 은 확정으로 둔다
    if os.name == "posix":
        import stat as _st5
        _os5 = globals()["os"]
        def _os_with_dirfail(arm_):
            def _fsync_fail(fd_, _arm=arm_):
                if _arm["on"] and _st5.S_ISDIR(_os5.fstat(fd_).st_mode):
                    _arm["on"], _arm["fired"] = False, True
                    raise OSError(5, "selftest — 디렉터리 fsync 실패 (교체 뒤)")
                return _os5.fsync(fd_)
            ns_ = _ty4.SimpleNamespace(**{k_: getattr(_os5, k_) for k_ in dir(_os5) if not k_.startswith("__")}); ns_.fsync = _fsync_fail
            return ns_
        res_ar = {}
        for nm_ in ("ack", "loop"):
            rw_ = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
            go(wt, rr=rw_, scen={("A", 12): {"melt": "fail", "polls": 8}}, sleep_hook=_after_window(rw_, 12))
            sw1_ = J(rw_ / "STOP.json")
            fd_ = rw_ / "A/seed12"
            if nm_ == "loop":
                fd_.rename(fd_.with_name("seed12.cut1"))
            arm_ar = {"on": False, "fired": False}
            def _rkd_ar(*a_, _arm=arm_ar, **k_):
                r_ = real.run_kind_detail(*a_, **k_)
                if r_[0] == "scientific" and not _arm["fired"]:
                    _arm["on"] = True
                return r_
            globals()["os"] = _os_with_dirfail(arm_ar)
            try:
                rc_ar, L_ar, _ = go(wt, rr=rw_, ack=sw1_["stop_id"], declare=OUT if nm_ == "ack" else None, mq=mq_with(run_kind_detail=_rkd_ar))
            finally:
                globals()["os"] = _os5
            row_ = [x_ for x_ in J(rw_ / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", 12)][-1]
            res_ar[nm_] = (arm_ar["fired"], rc_ar, len(L_ar), (row_.get("melt_check") or {}).get("verdict"))
        arm_st = {"on": False, "fired": False}
        def _rkd_none(*a_, **k_):
            return real.run_kind_detail(*a_, **k_)
        osx_ = _os_with_dirfail(arm_st)
        _wja5 = globals()["_write_json_atomic"]
        def _wja_stop(path_, obj_, _arm=arm_st):            # 녹음 fail 로 쓰는 terminal STOP 의 디렉터리 fsync 만 실패
            if pathlib.Path(path_).name == "STOP.json" and isinstance(obj_, dict) and obj_.get("code") == "melt" and not _arm["fired"]:
                _arm["on"] = True
            return _wja5(path_, obj_)
        globals()["os"], globals()["_write_json_atomic"] = osx_, _wja_stop
        try:
            rc_sa, L_sa, rr_sa = go(wt, scen={("A", 11): {"melt": "fail", "polls": 8}})
        finally:
            globals()["os"], globals()["_write_json_atomic"] = _os5, _wja5
        res_ar["stop_terminal"] = (arm_st["fired"], J(rr_sa / "STOP.json").get("code"), rc_sa)
        exp_ar = {"ack": (True, RC["refused"], 0, "fail"), "loop": (True, RC["invalid"], 0, "fail"), "stop_terminal": (True, "melt", RC["melt"])}
        chk(res_ar == exp_ar,
            "⛔음성 회신 DP P0-1 · P2-1 (교체 뒤 실패): 본 녹음 fail 을 적은 장부 교체 뒤 디렉터리 fsync 가 실패해도 메모리를 되돌리지 않는다 — 확인은 거부 · "
            f"재시도는 invalid · 장부에 fail 이 남는다 · terminal STOP 교체 뒤 실패도 끝 처리가 덮지 않는다 ({ {k: v for k, v in res_ar.items() if v != exp_ar.get(k)} })")
    else:
        print("  · 건너뜀 (POSIX 전용) 회신 DP 교체 뒤 디렉터리 fsync 실패 — 이 OS 는 디렉터리 fsync 를 하지 않는다")
    # ⭐ 회신 DP (같은 꼴) — 실행 전 기록 · 장부 행을 한 구간으로: 실행 전 기록 교체가 끝나는 순간 미룬 신호가 와도 장부에 그 실행 행이 있다
    arm_at = {"fired": False}
    def _replace_att(src_, dst_, _arm=arm_at):
        _os4.replace(src_, dst_)
        if not _arm["fired"] and str(dst_).endswith(real.ATTEMPT_NAME):
            _arm["fired"] = True
            _PENDING.append("SIGTERM")
    osa_ = _ty4.SimpleNamespace(**{k_: getattr(_os4, k_) for k_ in dir(_os4) if not k_.startswith("__")}); osa_.replace = _replace_att
    globals()["os"] = osa_
    try:
        rc_at2, L_at2, rr_at2 = go(wt)
    finally:
        globals()["os"] = _os4
    att_rid = J(rr_at2 / "A/seed11" / real.ATTEMPT_NAME)["run_id"]
    rows_at = [x_ for x_ in J(rr_at2 / "stage1_ledger.json")["runs"] if x_.get("run_id") == att_rid]
    chk(arm_at["fired"] and rc_at2 == RC["interrupted"] and not L_at2 and len(rows_at) == 1 and rows_at[0].get("end") is not None,
        "⛔음성 회신 DP (같은 꼴): 실행 전 기록 교체가 끝나는 순간 미룬 신호가 와도 장부에 그 실행 행이 생기고 (발사 전) 마감된다 — 장부에 없는 폴더를 안 남긴다 "
        f"({arm_at['fired']} · {rc_at2} · 발사 {len(L_at2)} · 행 {len(rows_at)})")
    # ⭐ 회신 DP P1-1 — 담금질 끝 판정을 쓰지 못하면 (written False) 다음 시드로 가지 않고 invalid
    def _sv_end(rd_, **k_):
        if k_.get("reason") == "담금질 끝":
            return {"status": "invalid", "written": False, "closes_system": False, "reasons": {"invalid": ["selftest — 판정 임시 파일이 남았다"]}}
        return real.stage1_verdict(rd_, **k_)
    rc_we, L_we, rr_we = go(wt, mq=mq_with(stage1_verdict=_sv_end))
    chk(rc_we == RC["invalid"] and len(L_we) == 1 and "쓰지 못했다" in J(rr_we / "STOP.json").get("reason", ""),
        f"⛔음성 회신 DP P1-1: 담금질 끝 판정을 쓰지 못하면 (written False) 다음 시드로 가지 않고 invalid ({rc_we} · 발사 {len(L_we)})")
    # ⭐ DQ 편지 §3-3 확인 — 끝 처리의 쓰기 구간 안에 두 번째 신호 (Ctrl-C 두 번): 끝 처리가 STOP interrupted 를 못 쓰고 나가도
    #   조용히 이어가지 않고 (예외가 밖으로) · 장부 행은 끝남 (interrupted) · 다음 시작은 판정 없는 폴더를 보고 resume 으로 멈춘다 (발사 0 · 덮지 않음)
    hk2 = {"armed": True}
    def _ctrl_c_first(t):
        if hk2["armed"] and t >= 3600.0 * 7 + 1:             # A11 (5 h) 끝난 뒤 B11 도중 — 첫째 Ctrl-C
            hk2["armed"] = False; raise KeyboardInterrupt("시험: 첫째 Ctrl-C")
    arm_2 = {"on": True, "fired": False}
    def _replace_2nd(src_, dst_, _arm=arm_2):
        _os4.replace(src_, dst_)
        if _arm["on"] and not hk2["armed"] and str(dst_).endswith("stage1_ledger.json"):
            runs_ = json.loads(pathlib.Path(dst_).read_text(encoding="utf-8")).get("runs") or [{}]
            if runs_[-1].get("status") == "interrupted":     # 끝 처리 (finish) 가 그 행을 끝낸 장부 교체 — 그 순간 둘째 신호가 미뤄져 있다
                _arm["on"], _arm["fired"] = False, True
                _PENDING.append("SIGINT")
    os2_ = _ty4.SimpleNamespace(**{k_: getattr(_os4, k_) for k_ in dir(_os4) if not k_.startswith("__")}); os2_.replace = _replace_2nd
    rr_2s = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
    exc_2s = None
    globals()["os"] = os2_
    try:
        try:
            go(wt, rr=rr_2s, sleep_hook=_ctrl_c_first)
        except KeyboardInterrupt as e_:
            exc_2s = e_
    finally:
        globals()["os"] = _os4
    led_2s = J(rr_2s / "stage1_ledger.json")
    lk2 = _Lock(rr_2s / "stage1.lock"); got_lk2 = lk2.acquire(); lk2.release()
    rc_2r, L_2r, _ = go(wt, rr=rr_2s)
    sp_2r = J(rr_2s / "STOP.json")
    chk(arm_2["fired"] and exc_2s is not None and led_2s["runs"][-1]["status"] == "interrupted" and led_2s["runs"][-1].get("end")
        and got_lk2 and rc_2r == RC["resume"] and not L_2r and sp_2r.get("code") == "resume"
        and sp_2r.get("run_id") == led_2s["runs"][-1]["run_id"],
        "⛔음성 DQ 편지 §3-3: 끝 처리의 장부 교체 직후 둘째 신호 → 조용히 이어가지 않고 (예외) · 장부 행은 끝남 · 잠금 풀림 · "
        f"다음 시작은 판정 없는 폴더에서 resume STOP (그 실행에 묶임 · 발사 0) ({arm_2['fired']} · {type(exc_2s).__name__} · {rc_2r} · {len(L_2r)})")
    # ⭐ DQ 전 리뷰 (독립 · 2026-11-05) 재현 — 러너가 거부하는 기록을 요약도 거부 · 확인 안 된 STOP 을 덮지 않음 · 판정 쓰기 구간 · 낡은 요약
    chk(tuple(TERMINAL_STOPS) == tuple(real.STOP_TERMINAL_CODES), f"러너 닫는 STOP 코드 {TERMINAL_STOPS} = 소비자 {real.STOP_TERMINAL_CODES} (DQ 전 리뷰 P2-D)")
    chk(sorted(k_ for k_ in RC if k_ not in ("pass", "refused")) == sorted(real.STOP_CODES),
        f"러너 STOP 코드 {sorted(k_ for k_ in RC if k_ not in ('pass', 'refused'))} = 소비자 STOP_CODES {sorted(real.STOP_CODES)} (회신 DQ P2-1)")
    def _led_row(c_, sys_, sd_, **kv):
        l_ = J(c_ / "stage1_ledger.json")
        [x_ for x_ in l_["runs"] if (x_["system"], x_["seed"]) == (sys_, sd_)][-1].update(kv)
        _write_json_atomic(c_ / "stage1_ledger.json", l_)
    def _led_top(c_, **kv):
        l_ = J(c_ / "stage1_ledger.json"); l_.update(kv); _write_json_atomic(c_ / "stage1_ledger.json", l_)
    def _vf_edit(c_, sys_, sd_, **kv):
        vf_ = c_ / sys_ / f"seed{sd_}" / "stage1_verdict.json"; v_ = J(vf_); v_.update(kv)
        vf_.write_text(json.dumps(v_, ensure_ascii=False), encoding="utf-8")
    def _hist_add(c_, line_):
        with open(c_ / "A/seed11" / real.VERDICT_HISTORY, "a", encoding="utf-8") as fh_:
            fh_.write(line_ + "\n")
    def _prov_changed(c_, sys_, sd_):
        pv_ = dict(J(c_ / sys_ / f"seed{sd_}" / "stage1_verdict.json")["provenance"])
        pv_["files_sha256"] = {**pv_["files_sha256"], "traj.xyz": "0" * 64}
        return pv_
    def _prov_judge_err(c_, sys_, sd_, mismatch=False):     # ⭐ 회신 DQ P1-1 — 지금 판정의 지문 + 판정 성격 (판정 도중 예외 · 또는 입력 불일치)
        pv_ = dict(J(c_ / sys_ / f"seed{sd_}" / "stage1_verdict.json")["provenance"])
        pv_["judge_nature"] = ({"errors": [], "input_mismatch": ["md_init_raw.xyz 불일치 (selftest)"]} if mismatch
                               else {"errors": ["seed_gate OSError: selftest"], "input_mismatch": []})
        return pv_
    def _stop_put(c_, txt_):
        (c_ / "STOP.json").write_text(txt_, encoding="utf-8")
    STOPJ = lambda code_, term_=False: json.dumps({"at": "x", "code": code_, "reason": "selftest", "terminal": term_, "stop_id": "ab" * 8})
    cases_q = {
        # P1-A — 같은 실행의 장부 판정 ↔ 폴더 판정 (러너 ①-4 와 같은 함수)
        "led_invalid_noprov": lambda c_: _led_row(c_, "A", 12, verdict="invalid", verdict_provenance=None),
        "led_incomplete_noprov": lambda c_: _led_row(c_, "A", 12, verdict="incomplete", verdict_provenance=None),
        "led_invalid_prov_changed": lambda c_: _led_row(c_, "A", 12, verdict="invalid", verdict_provenance=_prov_changed(c_, "A", 12)),
        "led_PASS": lambda c_: _led_row(c_, "A", 12, verdict="PASS"),
        "led_fail_folder_pass": lambda c_: _led_row(c_, "A", 12, verdict="fail"),
        "led_inv_folder_fail": lambda c_: (_led_row(c_, "A", 13, verdict="invalid", verdict_provenance=None), _vf_edit(c_, "A", 13, status="fail")),
        "led_prov_badshape": lambda c_: _led_row(c_, "A", 12, verdict_provenance="x"),
        "led_superseded_badshape": lambda c_: _led_row(c_, "A", 12, verdict_superseded=[{"from": "pass", "to": "fail"}]),
        "led_conflict_rec": lambda c_: _led_row(c_, "A", 12, verdict_observed_conflict=[{"status": "fail", "in": "selftest"}]),
        # P2-C — 이력 줄의 prev · 상태 꼴
        "hist_prev_null": lambda c_: _hist_add(c_, '{"prev": null, "new_status": "pass"}'),
        "hist_no_prev": lambda c_: _hist_add(c_, '{"new_status": "pass"}'),
        "hist_prev_garbage": lambda c_: _hist_add(c_, '{"prev": {"status": "garbage"}, "new_status": "pass"}'),
        "hist_new_garbage": lambda c_: _hist_add(c_, '{"prev": {"status": "pass"}, "new_status": "garbage"}'),
        # P2-D — STOP.json · 첫 시드 아닌 닫힘
        "stop_trunc": lambda c_: _stop_put(c_, '{"code": "melt", "stop_id": "a'),
        "stop_terminal": lambda c_: _stop_put(c_, STOPJ("melt", True)),
        "closes_nonfirst_ledger": lambda c_: _led_row(c_, "A", 12, closes_system=True),
        "led_PASS_noverdict": lambda c_: (_led_row(c_, "A", 12, verdict="PASS"), (c_ / "A/seed12/stage1_verdict.json").unlink()),
        "led_conflict_badshape": lambda c_: _led_row(c_, "A", 12, verdict_observed_conflict={}),
        "closes_nonfirst_verdict": lambda c_: _vf_edit(c_, "A", 12, closes_system=True),
        # P2-G — 장부를 쓴 러너의 카드 값 · 도구 지문
        "led_card_fp": lambda c_: _led_top(c_, card_values_sha16="0" * 16),
        "led_driver_fp": lambda c_: _led_top(c_, driver_sha16="0" * 16),
        # ⭐ 회신 DQ P1-1 — 같은 지문이어도 앞 판정이 판정 도중 예외가 아니면 (예외 없이 끝남 · 입력 불일치) 대체하지 않는다
        "led_invalid_same_noerr": lambda c_: _led_row(c_, "A", 12, verdict="invalid"),
        "led_invalid_same_mismatch": lambda c_: _led_row(c_, "A", 12, verdict="invalid", verdict_provenance=_prov_judge_err(c_, "A", 12, mismatch=True)),
        # ⭐ 회신 DQ P2-1 — 모순된 STOP (interrupted + true · melt + false) · 모르는 코드 · terminal 없음 = 판독 불가
        "stop_contra": lambda c_: _stop_put(c_, STOPJ("interrupted", True)),
        "stop_melt_false": lambda c_: _stop_put(c_, STOPJ("melt", False)),
        "stop_bogus": lambda c_: _stop_put(c_, STOPJ("bogus")),
        "stop_noterm": lambda c_: _stop_put(c_, json.dumps({"at": "x", "code": "invalid", "reason": "selftest", "stop_id": "ab" * 8})),
    }
    res_q = {k_: _sum_case(f_) for k_, f_ in cases_q.items()}
    same_q = _sum_case(lambda c_: _led_row(c_, "A", 12, verdict="invalid", verdict_provenance=_prov_judge_err(c_, "A", 12)))   # 지문 그대로 · 판정 도중 예외 → 대체 (통과)
    def _hist_mm(c_):                                         # ⭐ DR 전 2차 리뷰 P1 (요약) — 장부 invalid (판정 도중 예외 · 같은 입력) 인데 폴더 이력에 입력 불일치 판정이
        _led_row(c_, "A", 12, verdict="invalid", verdict_provenance=_prov_judge_err(c_, "A", 12))   # 있다 (러너가 충돌 관측을 적기 전 — 요약만으로 가른다)
        cur_ = J(c_ / "A/seed12" / "stage1_verdict.json")
        with open(c_ / "A/seed12" / real.VERDICT_HISTORY, "a", encoding="utf-8") as fh_:
            fh_.write(json.dumps({"prev": {"status": "invalid", "provenance": _prov_judge_err(c_, "A", 12, mismatch=True)},
                                  "new_status": cur_["status"], "new_provenance": cur_["provenance"]}, ensure_ascii=False) + "\n")
    mm_q = _sum_case(_hist_mm)
    open_q = (_sum_case(lambda c_: _stop_put(c_, STOPJ("interrupted"))), _sum_case(lambda c_: _stop_put(c_, STOPJ("invalid"))))
    chk(all(v_ == ("invalid", None) for v_ in res_q.values()) and open_q == (("pending", None), ("pending", None)) and s_ok_["track"] == "stage1_pass"
        and same_q[0] == "stage1_pass" and mm_q[0] == "invalid",
        "⛔음성 DQ 전 리뷰 P1-A · 2차 N3 · P2-C · P2-D · P2-G: 장부 판정 invalid · incomplete (지문 없음 · 원자료 지문 다름) · 'PASS' · fail ↔ 폴더 pass · "
        "장부 invalid ↔ 폴더 fail · 장부 지문 · 대체 기록 꼴 · 적힌 충돌 관측 · "
        "이력 prev 없음 · null · 모르는 상태 · 잘린 STOP · 닫는 STOP (기록은 통과) · 첫 시드 아닌 닫힘 (장부 · 판정) · 장부의 모르는 판정 (판정 파일 없이) · "
        "충돌 관측 꼴 · 장부 카드 · 도구 지문 → 요약 invalid · 2 단계 없음 · 확인 안 된 다른 STOP (interrupted · invalid) → pending "
        f"· 장부 invalid 인데 그때 지문 = 지금 (판정 도중 예외) → 통과 · (회신 DQ) 같은 지문이어도 예외 없이 끝난 · 입력 불일치 판정 → invalid · 모순된 · "
        f"모르는 · terminal 없는 STOP → invalid · (DR 전 2차) 장부 invalid 여도 폴더 이력의 입력 불일치 판정 → invalid "
        f"({ {k: v for k, v in res_q.items() if v != ('invalid', None)} } · {open_q} · {same_q} · {mm_q})")
    # ⭐ 회신 DQ P2-1 (러너) — 모순된 STOP · 모르는 코드 · terminal 없음은 확인으로 지우지 않는다 (거부 · STOP 바이트 그대로 · 발사 0 · 요약 invalid)
    res_p21 = {}
    for nm_, txt_ in (("contra", STOPJ("interrupted", True)), ("melt_false", STOPJ("melt", False)), ("bogus", STOPJ("bogus")),
                      ("noterm", json.dumps({"at": "x", "code": "invalid", "reason": "selftest", "stop_id": "ab" * 8}))):
        c_ = clone(rr_d)
        _stop_put(c_, txt_)
        b0_ = (c_ / "STOP.json").read_bytes()
        rc_x, L_x, _ = go(wt, rr=c_, ack="ab" * 8)
        res_p21[nm_] = (rc_x, len(L_x), (c_ / "STOP.json").read_bytes() == b0_, real.stage1_summary(c_, values=vals_t, log=lambda *m: None)["track"])
    chk(all(v_ == (RC["refused"], 0, True, "invalid") for v_ in res_p21.values()),
        f"⛔음성 회신 DQ P2-1 (Codex 재현): interrupted + terminal true · melt + false · 모르는 코드 · terminal 없는 STOP 은 --ack_stop 으로 지우지 않는다 "
        f"(러너 거부 · STOP 그대로 · 발사 0) · 독립 요약도 invalid — 같은 함수 ({res_p21})")
    # 닫는 STOP 이 기록과 맞으면 (첫 시드 녹음 fail · 장부 closes_system) 요약은 stop_track 그대로
    rc_cq, L_cq, rr_cq = go(wt, scen={("A", 11): {"melt": "fail", "polls": 8}})
    sm_cq = summ(rr_cq)
    chk(rc_cq == RC["melt"] and J(rr_cq / "STOP.json").get("code") == "melt" and sm_cq["track"] == "stop_track",
        f"DQ 전 리뷰 P2-D 양성: 닫는 STOP 이 기록 (첫 시드 녹음 fail) 과 맞으면 요약은 stop_track ({rc_cq} · {sm_cq['track']})")
    # P1-A · P2-B — 러너 ①-4: 장부 판정 invalid ↔ 재판정 pass → 덮지 않고 충돌 관측으로 남기고 invalid (발사 0) · 로그는 한 일을 그대로
    rr_q1 = clone(rr_d); _led_row(rr_q1, "A", 12, verdict="invalid", verdict_provenance=None)
    rc_q1, L_q1, _ = go(wt, rr=rr_q1)
    row_q1 = [x_ for x_ in J(rr_q1 / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", 12)][-1]
    log_q1 = (rr_q1 / "stage1.log").read_text(encoding="utf-8")
    chk(rc_q1 == RC["invalid"] and not L_q1 and row_q1.get("verdict") == "invalid"
        and [x_.get("status") for x_ in row_q1.get("verdict_observed_conflict") or []] == ["pass"]
        and "덮지 않고 충돌 관측 (verdict_observed_conflict) 으로 적었다" in log_q1 and "A12 재판정" in J(rr_q1 / "STOP.json").get("reason", "")[:12],
        f"⛔음성 DQ 전 리뷰 P1-A · P2-B: 장부 판정 invalid 인 실행을 재판정이 pass 로 내면 러너는 덮지 않고 충돌 관측으로 남기고 invalid (발사 0) · "
        f"로그에 '충돌 관측' ({rc_q1} · 발사 {len(L_q1)} · {row_q1.get('verdict')} · {row_q1.get('verdict_observed_conflict')})")
    # ⭐ DQ 전 2차 리뷰 N3 — 끝 판정 도중 일시 오류 (시드 게이트 OSError) → 장부 invalid → 확인 뒤 같은 원자료 · 카드 · 도구로 다시 낸 pass 가 대체 · 남은 시드를 이어 돌린다
    _sg0 = real.seed_gate
    n_sg = {"left": 1}
    def _sg_flaky(run_, *a_, **k_):
        if n_sg["left"] and pathlib.Path(run_).name == "seed12" and pathlib.Path(run_).parent.name == "A":
            n_sg["left"] -= 1
            raise OSError("selftest — 판정 도중 일시 오류")
        return _sg0(run_, *a_, **k_)
    real.seed_gate = _sg_flaky
    try:
        rc_n3, L_n3, rr_n3 = go(wt)
    finally:
        real.seed_gate = _sg0
    row_n3a = [x_ for x_ in J(rr_n3 / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", 12)][-1]
    sp_n3 = J(rr_n3 / "STOP.json")
    rr_n3f, rr_n3m, rr_n3m0 = clone(rr_n3), clone(rr_n3), clone(rr_n3)   # ⭐ DR 전 리뷰 P2-A — 확인 전에 사람이 --seed_gate · --stage1_verdict 로 들여다본 경우 ·
                                                                          # (2차 P1) 확인 전에 다른 md_init_raw.xyz 가 놓인 경우
    rc_n3b, L_n3b, _ = go(wt, rr=rr_n3, ack=sp_n3["stop_id"])
    row_n3b = [x_ for x_ in J(rr_n3 / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", 12)][-1]
    chk(rc_n3 == RC["invalid"] and len(L_n3) == 3 and row_n3a.get("verdict") == "invalid" and isinstance(row_n3a.get("verdict_provenance"), dict)
        and rc_n3b == RC["pass"] and len(L_n3b) == 7 and row_n3b.get("verdict") == "pass"
        and [(x_.get("from"), x_.get("to")) for x_ in row_n3b.get("verdict_superseded") or []] == [("invalid", "pass")]
        and not row_n3b.get("verdict_observed_conflict") and J(rr_n3 / "stage1_summary.json")["track"] == "stage1_pass",
        f"⛔음성 DQ 전 2차 리뷰 N3: 끝 판정 도중 일시 오류로 장부 invalid → 확인 뒤 같은 원자료 · 카드 · 도구의 재판정 pass 가 대체하고 (기록) 이어 돌린다 · "
        f"통과 ({rc_n3} · 발사 {len(L_n3)} · {rc_n3b} · 발사 {len(L_n3b)} · {row_n3b.get('verdict_superseded')})")
    real.seed_gate(rr_n3f / "A/seed12", write_raw=True, log=lambda *m: None)            # 문서대로 --seed_gate (파생 파일을 쓴다) 로 들여다봄
    rc_n3f, L_n3f, _ = go(wt, rr=rr_n3f, ack=sp_n3["stop_id"])
    real.stage1_verdict(rr_n3m / "A/seed12", values=vals_t, log=lambda *m: None, reason="selftest — 확인 전 손 판정")
    rc_n3m, L_n3m, _ = go(wt, rr=rr_n3m, ack=sp_n3["stop_id"])
    sup_ = lambda c_: [(x_.get("from"), x_.get("to")) for x_ in [r_ for r_ in J(c_ / "stage1_ledger.json")["runs"]
                                                                  if (r_["system"], r_["seed"]) == ("A", 12)][-1].get("verdict_superseded") or []]
    chk(rc_n3f == RC["pass"] and len(L_n3f) == 7 and sup_(rr_n3f) == [("invalid", "pass")]
        and rc_n3m == RC["pass"] and len(L_n3m) == 7 and sup_(rr_n3m) == [("invalid", "pass")],
        "⛔음성 DR 전 리뷰 P2-A: 판정 도중 일시 오류 뒤 사람이 --seed_gate (파생 파일을 씀) · --stage1_verdict 로 한 번 들여다보고 확인해도 같은 입력의 재판정이 "
        f"대체하고 이어 간다 (중간 판정이 파생 파일을 만들었어도 영구 보류로 굳지 않는다) ({rc_n3f} · 발사 {len(L_n3f)} · {rc_n3m} · 발사 {len(L_n3m)})")
    # ⭐ DR 전 2차 리뷰 P1 — 일시 오류로 장부 invalid (파생 파일 없음) → 다른 md_init_raw.xyz 가 놓임 → 러너의 재판정이 입력 불일치를 봄 (장부엔 안 적힘 · rc 27)
    #    → 사람이 맞는 파일로 바꾸거나 (R1b) 지우고 (R1c) 확인 → 폴더 판정 기록의 입력 불일치 때문에 자동 대체하지 않는다 (발사 0 · 충돌 관측)
    from ase.io import read as _rd_t, write as _wr_t
    def _wrong_raw(d_):
        at_ = _rd_t(str(d_ / "traj.xyz"), index=-1); at_.wrap(); at_.positions[0] += 0.5
        _wr_t(str(d_ / real.SEED_GATE_RAW), at_, format="extxyz")
    r1_ = {}
    for nm_ in ("R1b_replace", "R1c_delete"):
        c_ = clone(rr_n3m0)
        _wrong_raw(c_ / "A/seed12")
        rc_a, L_a, _ = go(wt, rr=c_, ack=sp_n3["stop_id"])                 # 재판정이 불일치를 본다 (장부 그대로)
        (c_ / "A/seed12" / real.SEED_GATE_RAW).unlink()
        if nm_ == "R1b_replace":
            real.seed_gate(c_ / "A/seed12", write_raw=True, log=lambda *m: None)   # 맞는 파일로 바꿔 놓음
        rc_b, L_b, _ = go(wt, rr=c_, ack=J(c_ / "STOP.json")["stop_id"])
        row_ = [x_ for x_ in J(c_ / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", 12)][-1]
        r1_[nm_] = (rc_a, len(L_a), rc_b, len(L_b), row_.get("verdict"), len(row_.get("verdict_observed_conflict") or []), bool(row_.get("verdict_superseded")),
                    real.stage1_summary(c_, values=vals_t, log=lambda *m: None)["track"])
    chk(all(v_ == (RC["invalid"], 0, RC["invalid"], 0, "invalid", 1, False, "invalid") for v_ in r1_.values()),
        "⛔음성 DR 전 2차 리뷰 P1: 일시 오류 장부 invalid 뒤 러너의 재판정이 md_init_raw.xyz 불일치를 본 다음 사람이 맞는 파일로 바꾸거나 지우고 확인해도 — "
        f"폴더 판정 기록의 입력 불일치 때문에 자동 대체하지 않는다 (발사 0 · 충돌 관측 하나 · 요약 invalid) ({r1_})")
    # ⭐ DR 전 5차 리뷰 P2 — 첫 시드 (A11) 가 녹음 창이 찬 채 실행 중 상한으로 멈춤 → 상한 판정 fail + 계 닫힘 → (문서대로) 상한을 올린 카드로 · 폴더를 옆으로
    #    옮기고 확인 → 상한 칸은 판정 규칙이 아니라서 그 판정 기록은 지금 규칙의 것 → 장부에 닫힘 · 닫는 STOP melt (상한을 올린 것이 진짜 닫힘을 지우지 않는다)
    rc_cp, L_cp, rr_cp = go(mk_wt(card=mk_card(stage1_cap_gpu_h=3.0)), seed_worst_h=1.0, scen={("A", 11): {"melt": "fail"}})
    v_cp = J(rr_cp / "A/seed11/stage1_verdict.json")
    (rr_cp / "A/seed11").rename(rr_cp / "A/seed11.cap")
    rc_cp2, L_cp2, _ = go(wt, rr=rr_cp, ack=J(rr_cp / "STOP.json")["stop_id"])
    row_cp = [x_ for x_ in J(rr_cp / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", 11)][-1]
    chk(v_cp.get("status") == "fail" and v_cp.get("closes_system") is True
        and v_cp["provenance"]["card_values_sha16"] != real.values_sha16(vals_t) and v_cp["provenance"]["judge_values_sha16"] == real.judge_values_sha16(vals_t)
        and rc_cp2 == RC["melt"] and not L_cp2 and row_cp.get("closes_system") is True and J(rr_cp / "STOP.json").get("code") == "melt",
        "⛔음성 DR 전 5차 리뷰 P2: 첫 시드가 실행 중 상한으로 멈춘 판정 fail · 계 닫힘 — 문서대로 상한을 올린 카드 (카드 값 지문은 다르고 판정 규칙 지문은 같다) 로 "
        f"폴더를 옆으로 옮기고 확인해도 장부에 닫힘 · 닫는 STOP melt (발사 0) ({v_cp.get('status')} · {v_cp.get('closes_system')} · {rc_cp2} · {row_cp.get('closes_system')})")
    # ⭐ DR 전 4차 리뷰 P1 — 일시 오류로 장부 invalid → 원자료 (final.xyz) 가 바뀜 → 러너의 재판정이 결정적 invalid (예외 없음 · 불일치 기록 없음) → 원래
    #    바이트로 되돌리고 확인 → 장부 판정 뒤의 그 기록 때문에 자동 대체하지 않는다 (회신 DP Q2 '원자료 복구 → 보류' · 발사 0)
    c_rs = clone(rr_n3m0)
    fx_ = c_rs / "A/seed12/final.xyz"; b0_fx = fx_.read_bytes()
    at_fx = _rd_t(str(fx_)); at_fx.set_cell(at_fx.get_cell() * 1.01, scale_atoms=True); _wr_t(str(fx_), at_fx, format="extxyz")
    rc_ra, L_ra, _ = go(wt, rr=c_rs, ack=sp_n3["stop_id"])
    fx_.write_bytes(b0_fx)
    rc_rb, L_rb, _ = go(wt, rr=c_rs, ack=J(c_rs / "STOP.json")["stop_id"])
    row_rs = [x_ for x_ in J(c_rs / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", 12)][-1]
    chk(rc_ra == RC["invalid"] and not L_ra and rc_rb == RC["invalid"] and not L_rb and row_rs.get("verdict") == "invalid"
        and len(row_rs.get("verdict_observed_conflict") or []) == 1 and not row_rs.get("verdict_superseded")
        and real.stage1_summary(c_rs, values=vals_t, log=lambda *m: None)["track"] == "invalid",
        "⛔음성 DR 전 4차 리뷰 P1: 일시 오류 장부 invalid 뒤 final.xyz 가 바뀌어 러너 재판정이 결정적 invalid 를 낸 다음 원래 바이트로 되돌리고 확인해도 — "
        f"장부 판정 뒤의 그 기록 때문에 자동 대체하지 않는다 (발사 0 · 충돌 관측 · 요약 invalid) ({rc_ra} · {rc_rb} · {row_rs.get('verdict_superseded')})")
    # ⭐ DR 전 3차 리뷰 P3 — 실행 중에 사람이 --stage1_verdict 로 한 번 들여다본 (incomplete · 예외 없음) 기록이 있어도 끝 판정의 일시 오류는 회복된다
    rr_pk = pathlib.Path(tempfile.mkdtemp(dir=tmp_root))
    pk_ = {"done": False}
    def _peek(_c):
        d_ = rr_pk / "A/seed12"
        if not pk_["done"] and (d_ / "plan.json").is_file() and (d_ / "traj.xyz").is_file() and not (d_ / "final.xyz").exists():
            pk_["done"] = True
            pk_["st"] = real.stage1_verdict(d_, values=vals_t, log=lambda *m: None, reason="selftest — 실행 중 들여다봄")["status"]
    n_sg["left"] = 1
    real.seed_gate = _sg_flaky
    try:
        rc_pk, L_pk, _ = go(wt, rr=rr_pk, sleep_hook=_peek)
    finally:
        real.seed_gate = _sg0
    rc_pk2, L_pk2, _ = go(wt, rr=rr_pk, ack=J(rr_pk / "STOP.json")["stop_id"])
    chk(pk_.get("st") == "incomplete" and rc_pk == RC["invalid"] and len(L_pk) == 3 and rc_pk2 == RC["pass"] and len(L_pk2) == 7
        and sup_(rr_pk) == [("invalid", "pass")],
        "⛔음성 DR 전 3차 리뷰 P3: 실행 중 들여다본 incomplete 기록 (예외 없음 · 그때의 짧은 원자료) 이 폴더 이력에 있어도 — 장부 판정 (끝 판정의 일시 오류) 과 같은 "
        f"입력의 재판정이 대체하고 이어 간다 ({pk_.get('st')} · {rc_pk} · 발사 {len(L_pk)} · {rc_pk2} · 발사 {len(L_pk2)})")
    # ⭐ DR 전 3차 리뷰 P2 — 첫 시드 (A11) 의 닫힘이 이력 줄에만 있어도 (정본 없음) 시작 점검이 장부에 fail · closes_system 을 적고 다음 시작은 닫는 STOP (melt)
    rr_cl = clone(rr_d)
    d11_ = rr_cl / "A/seed11"
    pv11_ = J(d11_ / "stage1_verdict.json")["provenance"]
    for f_ in ("stage1_verdict.json", real.VERDICT_HISTORY):
        (d11_ / f_).unlink(missing_ok=True)
    _led_row(rr_cl, "A", 11, verdict=None, verdict_provenance=None)
    real._append_history_first(d11_, {"status": "fail", "closes_system": True, "provenance": pv11_}, "selftest — 첫 시드 녹음 fail (정본 쓰기 끊김)")
    (rr_cl / "STOP.json").unlink(missing_ok=True)
    rc_cl1, L_cl1, _ = go(wt, rr=rr_cl)
    row_cl = [x_ for x_ in J(rr_cl / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", 11)][-1]
    sp_cl1 = J(rr_cl / "STOP.json")
    rc_cl2, L_cl2, _ = go(wt, rr=rr_cl, ack=sp_cl1["stop_id"])
    chk(rc_cl1 == RC["melt"] and not L_cl1 and sp_cl1.get("code") == "melt" and sp_cl1.get("terminal") is True
        and row_cl.get("verdict") == "fail" and row_cl.get("closes_system") is True
        and rc_cl2 == RC["melt"] and not L_cl2 and J(rr_cl / "STOP.json").get("stop_id") == sp_cl1["stop_id"],
        "⛔음성 DR 전 3차 리뷰 P2 · 4차 P3: 첫 시드의 녹음 fail · 계 닫힘이 이력 줄에만 남은 폴더 (정본 없음) — 시작 점검이 장부에 fail 과 closes_system 을 "
        f"적고 그 자리에서 닫는 STOP melt (발사 0 · 확인으로 못 넘김) ({rc_cl1} · {row_cl.get('verdict')} · {row_cl.get('closes_system')} · {rc_cl2})")
    # ⭐ 회신 DQ P1-1 (Codex 재현) — A12 의 md_init_raw.xyz 가 traj 원시와 다르면 판정은 입력 불일치 (invalid · rc 27) · 그 파일을 다른 이름으로 보존하고
    #    일반 확인 → 다시 만든 판정 pass 를 '판정 도중 오류' 로 자동 대체하지 않는다 (발사 0 · 충돌 관측 · 독립 요약 invalid)
    from ase.io import read as _rd_t, write as _wr_t
    n_mm = {"left": 1}
    def _sg_mm(run_, *a_, **k_):
        rp_ = pathlib.Path(run_)
        if n_mm["left"] and rp_.name == "seed12" and rp_.parent.name == "A":
            n_mm["left"] -= 1
            at_ = _rd_t(str(rp_ / "traj.xyz"), index=-1); at_.wrap(); at_.positions[0] += 0.5
            _wr_t(str(rp_ / real.SEED_GATE_RAW), at_, format="extxyz")
        return _sg0(run_, *a_, **k_)
    real.seed_gate = _sg_mm
    try:
        rc_mm, L_mm, rr_mm = go(wt)
    finally:
        real.seed_gate = _sg0
    row_mm = [x_ for x_ in J(rr_mm / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", 12)][-1]
    nat_mm = (row_mm.get("verdict_provenance") or {}).get("judge_nature") or {}
    (rr_mm / "A/seed12" / real.SEED_GATE_RAW).rename(rr_mm / "A/seed12" / (real.SEED_GATE_RAW + ".kept"))
    rc_mm2, L_mm2, _ = go(wt, rr=rr_mm, ack=J(rr_mm / "STOP.json")["stop_id"])
    row_mm2 = [x_ for x_ in J(rr_mm / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", 12)][-1]
    sm_mm2 = real.stage1_summary(rr_mm, values=vals_t, log=lambda *m: None)
    chk(rc_mm == RC["invalid"] and len(L_mm) == 3 and row_mm.get("verdict") == "invalid" and nat_mm.get("input_mismatch") and not nat_mm.get("errors")
        and rc_mm2 == RC["invalid"] and not L_mm2 and row_mm2.get("verdict") == "invalid" and len(row_mm2.get("verdict_observed_conflict") or []) == 1
        and not row_mm2.get("verdict_superseded") and "자동 대체 조건이 아니다" in J(rr_mm / "STOP.json").get("reason", "")
        and (rr_mm / "A/seed12" / real.SEED_GATE_RAW).is_file() and sm_mm2["track"] == "invalid" and not sm_mm2.get("stage2"),
        "⛔음성 회신 DQ P1-1 (Codex 재현): md_init_raw.xyz 불일치 = 입력 불일치 판정 (invalid · rc 27 · 판정 도중 예외 아님) → 그 파일을 보존하고 확인해도 "
        "다시 만든 판정 pass 로 자동 대체하지 않는다 (발사 0 · 충돌 관측 하나 · 요약 invalid · 2 단계 없음) "
        f"({rc_mm} · 발사 {len(L_mm)} · {nat_mm} · {rc_mm2} · 발사 {len(L_mm2)} · {row_mm2.get('verdict_superseded')} · {sm_mm2['track']})")
    # ⭐ 회신 DQ P1-2 (Codex 재현) — 허용된 순서로 B14 를 A14 보다 먼저 · B14 첫 판정의 정본 교체가 한 번 실패 (이력 · 임시 판정만 남는다) →
    #    독립 요약 invalid · STOP 을 확인하고 기본 순서로 다시 시작해도 · 그 순서로 다시 시작해도 발사 0
    import types as _ty_u
    ORD_B14 = "A:11,B:11,A:12,B:12,A:13,B:13,B:14,A:14,A:15,B:15"
    _os_r = real.os
    arm_v = {"fired": False}
    def _rep_v(src_, dst_):
        if not arm_v["fired"] and str(dst_).replace("\\", "/").endswith("B/seed14/stage1_verdict.json"):
            arm_v["fired"] = True
            raise OSError("selftest — 첫 정본 판정 교체 실패")
        return _os_r.replace(src_, dst_)
    osv_ = _ty_u.SimpleNamespace(**{k_: getattr(_os_r, k_) for k_ in dir(_os_r) if not k_.startswith("__")}); osv_.replace = _rep_v
    real.os = osv_
    try:
        rc_u1, L_u1, rr_u1 = go(wt, order=ORD_B14, scen={("B", 14): {"melt": "fail"}})
    finally:
        real.os = _os_r
    b14_ = rr_u1 / "B/seed14"
    left_u = (os.path.lexists(b14_ / real.VERDICT_HISTORY), os.path.lexists(b14_ / "stage1_verdict.json.tmp"), os.path.lexists(b14_ / "stage1_verdict.json"))
    sm_u1 = real.stage1_summary(rr_u1, values=vals_t, log=lambda *m: None)
    rc_u2, L_u2, _ = go(wt, rr=rr_u1, ack=J(rr_u1 / "STOP.json")["stop_id"])               # 기본 순서 (A14 가 B14 앞)
    sp_u2 = J(rr_u1 / "STOP.json")
    rr_u4 = clone(rr_u1)                                      # ⭐ DR 전 리뷰 P2-B — 그 폴더를 옆으로 옮기고 (보존 폴더) 확인해도
    (rr_u4 / "B/seed14").rename(rr_u4 / "B/seed14.moved")
    hl_ = lambda c_: (c_ / "A/seed11" / real.VERDICT_HISTORY).read_bytes()          # 다른 폴더의 판정 기록은 건드리지 않고 먼저 멈춘다 (①-4 재판정 전)
    h0_u4 = hl_(rr_u4)
    rc_u4, L_u4, _ = go(wt, rr=rr_u4, ack=sp_u2["stop_id"])
    sp_u4 = J(rr_u4 / "STOP.json")
    sm_u4 = real.stage1_summary(rr_u4, values=vals_t, log=lambda *m: None)
    rr_u5 = clone(rr_u1); (rr_u5 / "B/seed14").rename(rr_u5 / "B/old14")      # ⭐ DR 전 2차 리뷰 P2-B — 이름 꼴과 무관
    rc_u5, L_u5, _ = go(wt, rr=rr_u5, ack=sp_u2["stop_id"])
    rr_u6 = clone(rr_u1); (rr_u6 / "B/seed14" / "stage1_verdict.json.tmp").unlink()   # ⭐ DR 전 2차 리뷰 P3 — 이력 줄만 남은 (fail) 폴더
    rc_u6, L_u6, _ = go(wt, rr=rr_u6, ack=sp_u2["stop_id"])
    row_u6 = [x_ for x_ in J(rr_u6 / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("B", 14)][-1]
    rc_u3, L_u3, _ = go(wt, rr=rr_u1, ack=sp_u2["stop_id"], order=ORD_B14)                # 그 순서로 한 번 더
    chk(arm_v["fired"] and rc_u1 == RC["interrupted"] and tag(L_u1)[-1] == ("B", 14) and left_u == (True, True, False)
        and sm_u1["track"] == "invalid" and "B14" in (sm_u1.get("stale_verdicts") or [])
        and rc_u2 == RC["invalid"] and not L_u2 and "B14" in sp_u2.get("reason", "") and "정본 판정" in sp_u2.get("reason", "")
        and rc_u3 == RC["invalid"] and not L_u3
        and rc_u4 == RC["invalid"] and not L_u4 and "B/seed14.moved" in sp_u4.get("reason", "") and sm_u4["track"] == "invalid"
        and hl_(rr_u4) == h0_u4 and sp_u4.get("reason", "").startswith("B/seed14.moved 미해결 판정 기록")
        and rc_u5 == RC["invalid"] and not L_u5 and "B/old14" in J(rr_u5 / "STOP.json").get("reason", "")
        and (J(rr_u5 / "STOP.json").get("sys"), J(rr_u5 / "STOP.json").get("seed")) == ("B", 14)   # ⭐ DR 전 3차 P3 — 계 · 시드는 장부 행에서
        and rc_u6 == RC["invalid"] and not L_u6 and row_u6.get("verdict") == "fail" and row_u6.get("verdict_observed") is not None,
        "⛔음성 회신 DQ P1-2 (Codex 재현): B14 를 A14 보다 먼저 돌려 B14 첫 정본 판정 교체가 실패 (이력 · 임시 판정만 · 정본 없음) → 독립 요약 invalid · "
        "STOP 을 확인하고 기본 순서로 다시 시작해도 (A14 를 띄우지 않는다) · 그 순서로 한 번 더 해도 발사 0 "
        f"({arm_v['fired']} · {rc_u1} · {tag(L_u1)[-2:]} · {left_u} · {sm_u1['track']} · {sm_u1.get('stale_verdicts')} · {rc_u2} · 발사 {len(L_u2)} · "
        f"{sp_u2.get('reason', '')[:80]} · {rc_u3} · 발사 {len(L_u3)} · (DR 전 리뷰 P2-B) 옆으로 옮김 {rc_u4} · 발사 {len(L_u4)} · {sm_u4['track']} · "
        f"다른 폴더 이력 그대로 {hl_(rr_u4) == h0_u4} · (2차) old14 {rc_u5} · 발사 {len(L_u5)} · 이력만 남은 fail → 장부 {row_u6.get('verdict')} · {rc_u6})")
    # ⭐ DQ 전 2차 리뷰 N1 · N2 — 재판정이 장부 판정 (pass) 과 다른 fail + closes 를 내면 충돌 관측으로만 (계를 닫지 않음) · 재시작해도 같은 관측은 한 번만
    def _sv_flip(rd_, **k_):
        r_ = real.stage1_verdict(rd_, **k_)
        if rd_.name == "seed11" and rd_.parent.name == "A" and r_.get("status") == "pass":
            return {**r_, "status": "fail", "closes_system": True}
        return r_
    rr_n1 = clone(rr_d)
    rc_n1, L_n1, _ = go(wt, rr=rr_n1, mq=mq_with(stage1_verdict=_sv_flip))
    sp_n1 = J(rr_n1 / "STOP.json")
    rc_n1b, L_n1b, _ = go(wt, rr=rr_n1, ack=sp_n1["stop_id"], mq=mq_with(stage1_verdict=_sv_flip))
    row_n1 = [x_ for x_ in J(rr_n1 / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", 11)][-1]
    vc_n1 = row_n1.get("verdict_observed_conflict") or []
    chk(rc_n1 == RC["invalid"] and rc_n1b == RC["invalid"] and not L_n1 and not L_n1b and row_n1.get("verdict") == "pass"
        and row_n1.get("closes_system") is not True and len(vc_n1) == 1 and vc_n1[0].get("closes_system") is True
        and J(rr_n1 / "STOP.json").get("code") == "invalid",
        f"⛔음성 DQ 전 2차 리뷰 N1 · N2: 재판정이 장부 pass 와 다른 fail + closes 면 충돌 관측으로만 남기고 계를 닫지 않는다 (닫는 STOP 아님) · 재시작해도 "
        f"같은 관측은 한 번만 ({rc_n1} · {rc_n1b} · closes {row_n1.get('closes_system')} · 관측 {len(vc_n1)})")
    # ⭐ DQ 전 2차 리뷰 N3 — 재시도 · 확인 경로의 폴더 판정 관측에도 지금 판정의 지문이 실린다 (①-4 와 같은 대체 규칙을 쓰게)
    rr_x = clone(rr_d)
    real.stage1_verdict(rr_x / "A/seed12", values=vals_t, log=lambda *m: None, reason="selftest — 이력 한 줄")   # 지금 판정에 history 를 만든다
    fdp_ = rr_x / "A" / "seed12.cut1"; (rr_x / "A/seed12").rename(fdp_)
    vx0_ = J(fdp_ / "stage1_verdict.json"); ridx = vx0_["run_id"]
    rowx = {"system": "A", "seed": 12, "run_id": ridx, "status": "ended", "end": "x", "verdict": "invalid"}
    def _obs_pair():
        el_ = retry_eligibility([rowx], [], {ridx: {"path": str(fdp_)}}, vals_t, real)
        ob_ = []
        ack_declaration_problems({}, {"run_id": ridx, "code": "invalid"}, {"runs": [rowx]}, vals_t,
                                 mq_with(attempt_inventory=lambda r_: ({ridx: {"path": str(fdp_)}}, [])), rr_x, observed=ob_)
        return el_.get("observed") or {}, (ob_ or [{}])[0]
    o0a_, o0b_ = _obs_pair()                                 # ⭐ 회신 DQ P1-1 — 이름을 바꾸기 전 판정: 보존 폴더에서는 폴더 이름 · 실행 전 기록도 판정 입력 → 지금이 아니다
    real.stage1_verdict(fdp_, values=vals_t, log=lambda *m: None, reason="selftest — 보존 폴더에서 다시 판정")
    vx_ = J(fdp_ / "stage1_verdict.json")
    o1_, o2_ = _obs_pair()
    with open(fdp_ / "result.json", "a", encoding="utf-8") as fh_:      # 보존 폴더의 원자료를 판정 뒤에 바꾼다 — 기록된 지문은 이제 낡았다
        fh_.write("\n")
    o3_, o4_ = _obs_pair()
    ch_x = real.folder_verdict_chain(fdp_)
    chk(o1_.get("provenance") == vx_["provenance"] and o2_.get("provenance") == vx_["provenance"] and o1_.get("prior") == ch_x
        and o2_.get("prior") == ch_x and len(ch_x) >= 3 and o3_.get("provenance") is None and o4_.get("provenance") is None
        and o0a_.get("provenance") is None and o0b_.get("provenance") is None and real.ATTEMPT_NAME in vx_["provenance"]["files_sha256"]
        and real.ATTEMPT_NAME not in vx0_["provenance"]["files_sha256"],
        "⛔음성 DQ 전 2차 · 3차 · 4차 리뷰 · 회신 DQ P1-1: 재시도 자격 · 확인 경로의 폴더 판정 관측에 지금 판정의 지문 · 폴더 판정 기록 전체가 실린다 · 판정 뒤 원자료가 "
        "바뀐 보존 폴더의 낡은 지문 · 보존 폴더로 이름을 바꾸기 전 판정의 지문 (그 자리에선 실행 전 기록까지 판정 입력) 은 싣지 않는다 (대체 못 함) "
        f"({o1_.get('provenance') == vx_['provenance']} · {o3_.get('provenance')} · {o4_.get('provenance')} · {o0a_.get('provenance')})")
    # ⭐ DQ 전 3차 리뷰 P1 — 장부 판정이 빈 채 (판정을 쓴 뒤 장부에 적기 전에 SIGKILL · 정전) 폴더의 앞 판정과 다른 결과가 나오면 보류 (러너 · 요약 같은 규칙)
    def _crash_state(c_, sd_, **vf_kv):
        _vf_edit(c_, "A", sd_, **vf_kv); _led_row(c_, "A", sd_, verdict=None, verdict_provenance=None)
    rr_k1 = clone(rr_d); _crash_state(rr_k1, 12, status="fail")                                    # 앞 판정 fail → 지금 원자료로 pass
    rc_k1, L_k1, _ = go(wt, rr=rr_k1)
    rr_k2 = clone(rr_d); _crash_state(rr_k2, 12, status="invalid", provenance=_prov_changed(rr_k2, "A", 12))   # 앞 invalid · 그 뒤 원자료가 바뀜
    rc_k2, L_k2, _ = go(wt, rr=rr_k2)
    rr_k3 = clone(rr_d); _crash_state(rr_k3, 12, status="invalid", provenance=_prov_judge_err(rr_k3, "A", 12))   # 앞 invalid · 같은 입력 · 판정 도중 예외 → 대체 (이어 감)
    rc_k3, L_k3, _ = go(wt, rr=rr_k3)
    rr_k3b = clone(rr_d); _crash_state(rr_k3b, 12, status="invalid")                              # ⭐ 회신 DQ P1-1 — 같은 입력이어도 예외 없이 끝난 invalid → 보류
    rc_k3b, L_k3b, _ = go(wt, rr=rr_k3b)
    rr_k4 = clone(rr_d); _crash_state(rr_k4, 12, status="fail")                                    # 4차 — 끊긴 뒤 사람이 한 번 더 다시 판정
    real.stage1_verdict(rr_k4 / "A/seed12", values=vals_t, log=lambda *m: None, reason="selftest — 사람의 다시 판정")
    rc_k4, L_k4, _ = go(wt, rr=rr_k4)
    rr_k5 = clone(rr_d); _crash_state(rr_k5, 12, status="invalid", provenance=_prov_changed(rr_k5, "A", 12))
    real.stage1_verdict(rr_k5 / "A/seed12", values=vals_t, log=lambda *m: None, reason="selftest — 사람의 다시 판정")
    rc_k5, L_k5, _ = go(wt, rr=rr_k5)
    rr_k6 = clone(rr_d)                                                    # 5차 P2 — 판정 파일을 지우고 다시 판정해도 이력의 첫 판정 (fail) 이 남는다
    _led_row(rr_k6, "A", 12, verdict=None, verdict_provenance=None)
    rd_k6 = rr_k6 / "A/seed12"
    real._append_history_first(rd_k6, {"status": "fail", "provenance": J(rd_k6 / "stage1_verdict.json")["provenance"]}, "selftest — 첫 판정 fail")
    (rd_k6 / "stage1_verdict.json").unlink()
    real.stage1_verdict(rd_k6, values=vals_t, log=lambda *m: None, reason="selftest — 판정 파일을 지운 뒤 다시 판정")
    s_k6 = summ(clone(rr_k6))["track"]
    rc_k6, L_k6, _ = go(wt, rr=rr_k6)
    row_k1 = [x_ for x_ in J(rr_k1 / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", 12)][-1]
    row_k3 = [x_ for x_ in J(rr_k3 / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", 12)][-1]
    chk(rc_k1 == RC["invalid"] and not L_k1 and "A12 재판정" in J(rr_k1 / "STOP.json").get("reason", "")[:12] and row_k1.get("verdict") is None
        and len(row_k1.get("verdict_observed_conflict") or []) == 1 and rc_k2 == RC["invalid"] and not L_k2
        and rc_k3 == RC["pass"] and not L_k3 and row_k3.get("verdict") == "pass" and rc_k3b == RC["invalid"] and not L_k3b
        and rc_k4 == RC["invalid"] and not L_k4 and rc_k5 == RC["invalid"] and not L_k5
        and s_k6 == "invalid" and rc_k6 == RC["invalid"] and not L_k6,
        f"⛔음성 DQ 전 3차 리뷰 P1: 장부 판정이 빈 끊긴 상태에서 폴더의 앞 판정 fail → 지금 pass · 앞 invalid → 원자료가 바뀐 뒤 pass 면 러너가 보류 (발사 0) · "
        f"같은 원자료면 적고 이어 간다 · (4차) 끊긴 뒤 사람이 한 번 더 다시 판정해도 · (5차) 판정 파일을 지우고 다시 판정해도 앞 판정이 증거로 남는다 "
        f"(요약 · 러너) ({rc_k1} · {rc_k2} · {rc_k3} · {rc_k4} · {rc_k5} · {s_k6} · {rc_k6} · "
        f"{row_k1.get('verdict_observed_conflict')})")
    def _crash_rejudged(c_, sd_, **vf_kv):                   # 같은 상태를 러너 없이 — 사람이 --stage1_verdict 로 다시 판정한 뒤 요약
        _crash_state(c_, sd_, **vf_kv)
        real.stage1_verdict(c_ / "A" / f"seed{sd_}", values=vals_t, log=lambda *m: None, reason="selftest — 끊긴 뒤 다시 판정")
    sum_k = {"flip": _sum_case(lambda c_: _crash_rejudged(c_, 12, status="fail")),
             "nonsci_changed": _sum_case(lambda c_: _crash_rejudged(c_, 12, status="invalid", provenance=_prov_changed(c_, "A", 12))),
             "nonsci_same": _sum_case(lambda c_: _crash_rejudged(c_, 12, status="invalid", provenance=_prov_judge_err(c_, "A", 12))),
             "nonsci_same_noerr": _sum_case(lambda c_: _crash_rejudged(c_, 12, status="invalid")),      # ⭐ 회신 DQ P1-1 — 예외 없이 끝난 invalid
             "nonsci_same_mismatch": _sum_case(lambda c_: _crash_rejudged(c_, 12, status="invalid", provenance=_prov_judge_err(c_, "A", 12, mismatch=True))),
             "flip_twice": _sum_case(lambda c_: (_crash_rejudged(c_, 12, status="fail"),
                                                 real.stage1_verdict(c_ / "A/seed12", values=vals_t, log=lambda *m: None, reason="selftest — 한 번 더")))}
    chk(sum_k == {"flip": ("invalid", None), "nonsci_changed": ("invalid", None), "nonsci_same": ("stage1_pass", sum_k["nonsci_same"][1]),
                  "nonsci_same_noerr": ("invalid", None), "nonsci_same_mismatch": ("invalid", None), "flip_twice": ("invalid", None)}
        and sum_k["nonsci_same"][1] is not None,
        f"⛔음성 DQ 전 3차 리뷰 P1 (요약): 장부 판정이 빈 끊긴 상태의 다시 낸 판정 — 앞 fail → pass · 앞 invalid → 원자료가 바뀐 뒤 pass 면 요약 invalid · "
        f"같은 원자료면 통과 ({sum_k})")
    # P2-D — 러너 ①-3: 첫 시드 아닌 장부 닫힘 = 기록 오류 (invalid · 닫는 STOP 아님) · P2-C 러너도 이력 꼴 오류에서 발사 0
    rr_q2 = clone(rr_d); _led_row(rr_q2, "A", 12, closes_system=True)
    rc_q2, L_q2, _ = go(wt, rr=rr_q2)
    rr_q3 = clone(rr_d); _hist_add(rr_q3, '{"prev": null, "new_status": "pass"}')
    rc_q3, L_q3, _ = go(wt, rr=rr_q3)
    chk(rc_q2 == RC["invalid"] and not L_q2 and J(rr_q2 / "STOP.json").get("code") == "invalid" and rc_q3 == RC["invalid"] and not L_q3,
        f"⛔음성 DQ 전 리뷰 P2-D · P2-C: 첫 시드 아닌 장부 닫힘 → 러너 invalid (닫는 STOP 아님 · 발사 0) · 이력 prev null → 러너 invalid (발사 0) ({rc_q2} · {rc_q3})")
    # P2-A — 시작 점검 도중 신호가 와도 확인 안 된 닫는 STOP 을 덮지 않는다
    rr_q4 = clone(rr_d); _stop_put(rr_q4, STOPJ("melt", True)); sp_q4 = (rr_q4 / "STOP.json").read_bytes()
    _lt0 = globals()["_leftover_tmps"]
    def _lt_sig(*a_):
        signal.getsignal(signal.SIGTERM)(signal.SIGTERM, None)     # 처리기를 직접 부른다 (이식 가능 · 구간 밖이라 바로 던진다)
        return _lt0(*a_)
    globals()["_leftover_tmps"] = _lt_sig
    try:
        rc_q4, L_q4, _ = go(wt, rr=rr_q4)
    finally:
        globals()["_leftover_tmps"] = _lt0
    chk(rc_q4 == RC["interrupted"] and not L_q4 and (rr_q4 / "STOP.json").read_bytes() == sp_q4,
        f"⛔음성 DQ 전 리뷰 P2-A: 시작 점검 도중 (STOP 을 읽기 전) 신호가 와도 확인 안 된 닫는 STOP 을 덮지 않는다 ({rc_q4} · STOP 그대로)")
    # P2-E — 판정 파일 쓰기 (임시 → 교체) 사이에 온 신호는 구간 끝에서 받는다 (판정 임시 파일이 안 남는다) — 러너가 판정을 쓰는 네 자리 모두
    _ros = real.os
    def _verdict_signal_run(call_, seed_dir="seed11"):
        arm_vw = {"on": True, "fired": False}
        def _drv_replace(src_, dst_, _arm=arm_vw):
            if _arm["on"] and pathlib.Path(dst_).name == "stage1_verdict.json" and pathlib.Path(dst_).parent.name == seed_dir:
                _arm["on"], _arm["fired"] = False, True
                signal.getsignal(signal.SIGTERM)(signal.SIGTERM, None)   # 처리기를 직접 — 구간 안이면 미뤄지고 · 밖이면 교체 전에 던진다
            return _ros.replace(src_, dst_)
        osd_ = _ty4.SimpleNamespace(**{k_: getattr(_ros, k_) for k_ in dir(_ros) if not k_.startswith("__")}); osd_.replace = _drv_replace
        real.os = osd_
        try:
            rc_, L_, rr_ = call_()
        finally:
            real.os = _ros
        vd_ = rr_ / "A" / seed_dir
        rows_ = [x_ for x_ in J(rr_ / "stage1_ledger.json")["runs"] if (x_["system"], x_["seed"]) == ("A", int(seed_dir[4:]))]
        return (arm_vw["fired"], rc_, not (vd_ / "stage1_verdict.json.tmp").exists(), (vd_ / "stage1_verdict.json").is_file(),
                rows_[-1].get("verdict") if rows_ else "?"), len(L_)
    rr_vr = clone(rr_d)
    res_vw = {"end": _verdict_signal_run(lambda: go(wt)),
              "rejudge": _verdict_signal_run(lambda: go(wt, rr=rr_vr)),
              "melt": _verdict_signal_run(lambda: go(wt, scen={("A", 11): {"melt": "fail", "polls": 8}})),
              "cap": _verdict_signal_run(lambda: go(mk_wt(card=mk_card(stage1_cap_gpu_h=3.0)), seed_worst_h=1.0))}
    exp_vw = {"end": ((True, RC["interrupted"], True, True, "pass"), 1), "rejudge": ((True, RC["interrupted"], True, True, "pass"), 0),
              "melt": ((True, RC["interrupted"], True, True, "fail"), 1), "cap": ((True, RC["interrupted"], True, True, None), 1)}
    chk(res_vw == exp_vw,
        "⛔음성 DQ 전 리뷰 P2-E: 러너가 판정을 쓰는 네 자리 (담금질 끝 · 시작 전 재판정 · 첫 시드 녹음 멈춤 · 실행 중 상한) 모두 — 판정 파일의 임시 → 교체 사이에 "
        f"신호가 와도 교체를 끝낸 뒤 받는다 · 판정 임시 파일이 안 남는다 · (3차 P1) 끝 · 녹음 멈춤 판정은 장부에도 남는다 (판정 쓰기 · 장부 적기 · 저장이 한 구간) "
        f"({ {k: v for k, v in res_vw.items() if v != exp_vw[k]} })")
    # P2-F — 러너가 시작 점검 · 재판정에서 거부해도 낡은 통과 요약이 남지 않는다
    rr_q5 = clone(rr_d); (rr_q5 / "A/seed11/stage1_verdict.json.tmp").write_text('{"status": "pass"}', encoding="utf-8")
    rc_q5, L_q5, _ = go(wt, rr=rr_q5)
    rr_q6 = clone(rr_d); (rr_q6 / "stage1_ledger.json.tmp").write_text("{}", encoding="utf-8")
    rc_q6, L_q6, _ = go(wt, rr=rr_q6)
    sq5, sq6 = J(rr_q5 / "stage1_summary.json"), J(rr_q6 / "stage1_summary.json")
    chk(J(rr_d / "stage1_summary.json")["track"] == "stage1_pass" and rc_q5 == RC["invalid"] and rc_q6 == RC["refused"] and not L_q5 and not L_q6
        and sq5["track"] != "stage1_pass" and sq5.get("stage2") is None and sq6.get("not_current") is True and sq6["track"] == "pending",
        f"⛔음성 DQ 전 리뷰 P2-F: 통과 요약이 있던 묶음에서 러너가 거부해도 (판정 임시 파일 → invalid · 장부 임시 파일 → 거부) 그 요약이 stage1_pass 로 안 남는다 "
        f"({rc_q5} · {sq5['track']} · {rc_q6} · {sq6['track']})")
    # P2-G — 카드 값만 바꿔 모든 시드를 다시 판정해도 장부의 카드 값 지문이 막는다
    rr_q7 = clone(rr_d)
    vals_e = dict(vals_t, stage1_cap_gpu_h=float(vals_t["stage1_cap_gpu_h"]) + 1.0)
    for s_ in SYSTEMS:
        for sd_ in vals_t["seeds"]:
            real.stage1_verdict(rr_q7 / s_ / f"seed{sd_}", values=vals_e, log=lambda *m: None, reason="selftest — 카드 값만 바꿔 다시 판정")
    sm_q7 = real.stage1_summary(rr_q7, values=vals_e, log=lambda *m: None)
    chk(sm_q7["track"] == "invalid" and any("카드 값 지문" in x_ for x_ in (sm_q7.get("cost") or {}).get("invalid", [])),
        f"⛔음성 DQ 전 리뷰 P2-G: 카드 값만 바꿔 (상한) 모든 시드를 다시 판정해도 장부의 카드 값 지문이 달라 요약 invalid ({sm_q7['track']})")
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
