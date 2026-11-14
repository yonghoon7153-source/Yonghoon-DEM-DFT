#!/usr/bin/env python3
"""li2s-3 2 단계 판독 — v1 런 사후 검증 · 궤적 유효성 · 골격 기록 ⓐ–ⓒ · 측정 가능 온도 창 W
(카드 개정 DZ · 내부 반박 리뷰 EB · EE 의 P0 · P1 · P2 고침 · 결과 전 커밋 · 2026-11-10 ·
 카드 개정 4 — 큐 끝 줄 유실 인정 · 2026-11-14 · 결과 전).

카드 db/properties/lpscl_glass_dense_protocol_ensemble_estimand_2026_11_10.json · 결정 D-2026-11-10-li2s3-dense-protocol-ensemble (+ -amend1)
리뷰 kb/reviews/codex_DZ_reply_li2s3_ensemble_definition_2026_11_10.md · kb/reviews/internal_EB_reply_li2s3_dz_fixes_2026_11_10.md ·
     kb/reviews/internal_EE_reply_li2s3_queue_v2_2026_11_10.md

하위 명령 — 종료 코드: 0 끝 · 2 거부 (문지기) · 3 판정 보류 (검증이 다 안 끝났거나 실패) · control 은 기록과 다르면 1
  verify   런마다 사후 검증 ①–⑦ (수송 · 골격 값은 안 읽는다 — 판독 허가 전에도 돌려도 된다) · --out 에 쓴다 (덮지 않는다)
  readout  결정 둘 active · 판독 허가 (아래) · 도구 작업 트리 깨끗함 · 큐와 계획 런이 모두 끝 · 모두 valid 일 때만
           → W · 갈래 · cond550 자격 · 시드별 기술표 · 세 층 · 기록 ⓐ–ⓒ (D 값 없음). 하나라도 아니면 W · 갈래 · cond550 을
           내지 않고 판정 보류 기록 <BASE>/readout_stage2/hold_*.json 만 남긴다 (종료 3 · 런마다 그때 본 지문을 싣는다 —
           PHASE=rerun 은 지금 지문 = 이 지문일 때만). 큐 잠금이 쥐어져 있으면 보류 기록을 쓰지 않고 거부한다 (상태 보기는 verify).
           판독은 한 번 — <BASE>/readout_stage2/readout_stage2.json (있으면 거부 · 행마다 런 지문 · 기계_판독_값 해시 · 장부 합계)
  pressure readout 과 같은 문지기 · 같은 보류 → 런마다 생산 프레임 k = j·10 − 1 (t = (k+1)·save = 1, 2, …, prod ps) 의
           UMA turbo 단일점 virial + N k_B T_set / V · 계마다 새 turbo 계산기 (조성 고정 모델) · 런마다
           <BASE>/readout_stage2/pressure_runs/ 에 점진 저장 (같은 궤적 · 같은 도구 판 · 같은 카드면 다시 쓴다) ·
           끝 기록 <BASE>/readout_stage2/pressure_stage2.json (있으면 거부) · 판정에 안 씀 (두 계 ⟨P⟩ 차 > 1 GPa 경고)
  control  대조 잡 — 10-14 대조 계 판독 기록의 kgy 시드 (1 · 3) 만 · 루트 run_meta 의 라벨 · 난수가 그 대조 계일 때만 ·
           같은 읽기 경로 (궤적 유효성 → read_run → skeleton_gate) 로 기록 행을 재현하는가 · --out (덮지 않는다)
  endline_facts  읽기만 (파일을 안 쓴다) — 큐 로그에 '■ 큐 끝 · PHASE ladder' 줄이 없을 때 카드 '큐_끝_줄_유실_인정' 에 넣을
           사실 (사다리 블록 마지막 줄 · 블록 sha256 · 장부 sha256) 과 같은 검사의 문제 목록을 찍는다 (문제 0 이면 0 · 아니면 1)

사후 검증 (런마다 — 하나라도 어긋나면 invalid · 끝나지 않았으면 incomplete)
  ① 실행 기록 — 러너 로그 <BASE>/<계>/queue_kgy.log 에서 그 런의 호출 블록 ('▶ v2 큐 시작 · T:S:prod') 이 정확히 하나이고
     그 안에 '드라이버 sha16 <카드> ✅' · '▶ T<T> seed<S> PID … · prod <카드> ps · --seed <offset+S>' ·
     'OK run_meta = 본 런 설정 (… prod <카드> · seed <offset+S>)' · 'dt = 기준과 같다 (<카드 dt> ps/행)' ·
     '✅ T<T> seed<S> 끝 (rc 0)' · '■ 큐 끝 · T:S:prod'. 끝 줄 '✅ …' 이 없으면 incomplete.
     큐 로그 <BASE>/stage2_kgy.log — PHASE ladder 시작 줄이 정확히 하나 (온도 · 시드 · 계 · prod = 카드) ·
     '문지기 ✓ — 카드 <결정> (active) · 러너 sha16 <카드>' · '판 — … · repo … · BASE <원래 BASE> · PHASE ladder' ·
     '■ 큐 끝 · PHASE ladder' — 사다리 블록 (첫 시작 줄 ~ 첫 끝 줄) 안에서만 본다. 큐 줄이 어긋나면 그 큐의 런이 모두 invalid ·
     큐 끝 줄이 없으면 판정 보류 · 블록 밖의 v1 호출 (뒤에 다시 띄움 · PHASE cond550) 은 런을 무효로 만들지 않고 따로 보류 사유.
     카드 개정 4 (2026-11-14 · 결과 전): 끝 줄이 없고 판독 허가에 '큐_끝_줄_유실_인정' {결정 · by · 근거 · 사다리_블록_마지막_줄 ·
     사다리_블록_sha256 · 장부_sha256} 이 있으면 그 줄을 블록 끝으로 받는다 — 그 줄이 시작 뒤에 한 번 · 블록 (시작 줄 ~ 그 줄)
     sha256 · 장부 sha256 = 인정 · 그 줄 = 명단 마지막 런 (돌림 순서 온도 → 시드 → 계) 의 큐 '✅ … 끝 · h · 누적' 줄 · 블록의
     큐 ✅ 줄 = 명단 (순서 그대로 · 하나씩) · 장부 = 머리 + 명단 행 하나씩 · rc 0 · prod = 카드 · 장부 시간 = 큐 ✅ 줄 시간 ·
     큐 잠금 풀림 (+ readout · pressure 문지기에서 그 결정 active). 하나라도 어긋나면 큐 문제 (런 모두 invalid → 판정 보류) ·
     인정이 있는데 끝 줄도 있으면 큐 문제 (인정 뒤에 로그가 바뀌었다).
  ② 설정 — run_meta = 카드 (T · prod · equilib · seed · 원자 수 · supercell · 창 · save_traj · 모델 · 요청 모드 ·
     **실제 모드 turbo** · 라벨 · v0_xyz = <원래 BASE>/<계>/init/seed<S>_final.xyz — 원래 BASE 기준이라 옮긴 사본에서도 읽는다) ·
     ensemble_results.json 끝 요약 (실제 모드 turbo · task omat · 모델 · 온도 · prod · equilib · 원자 수 · 라벨)
  ③ 입력 결속 — init 사본 sha256 = 카드 · 드라이버가 쓴 config.xyz = init (원소 순서 · 셀 · 좌표 1e-6 Å) ·
     생산 첫 프레임 셀 = config.xyz 셀 (1e-6 Å) · 첫 프레임 P · S 최소상 변위 중앙값 < 카드 bind_PS_median_disp_max_A
  ④ 궤적 — aimd_results (T · save · prod · dt · 프레임 수 = round(prod/save)) · traj.xyz (프레임 수 = 계획 · 프레임 k 는
     t = (k+1)·save — 드라이버는 평형 뒤 첫 관측을 한 간격 뒤에 찍는다 · 원자 수 · 원소 순서 · 유한 · PBC · 셀 불변 ·
     프레임 간 최소상 이동 ≤ 원소별 상한 continuity_max_A) · md.log (머리 줄 하나 · 행 수 = (equilib + prod)/dt + 1 ·
     0 에서 dt 간격 단조 · 끝 = equilib + prod · 생산 평균 T 가 설정의 ± mean_T_tol_frac 안)
  ⑤ 산출물 — msd.json (T · 창 · times_ps / msd_Li_A2 길이 = 프레임 수 · 유한 · 0 에서 save 간격 · read_run 이 쓰는
     times_ps_mto / msd_Li_A2_mto 유한 · 단조 · 첫 지연 = save · 끝 지연 = (프레임 수 // 2)·save)
  ⑥ 비용 — 장부 행 하나 (유한 · 비음수) → 없거나 깨졌으면 러너 블록 시각 (시작 → 끝 줄) 으로 재구성 → 그것도 없으면
     '비용 미확정' (0 아님 · 파일 시각은 복사로 바뀌어 근거로 안 쓴다)
  ⑦ 보조 — --worktree (큐가 돈 worktree) 의 드라이버 · 러너 sha16 = 카드 · 큐 파일 sha256 기록

카드 기계 값 (도구가 따로 갖지 않는다 — 없으면 거부 · 종료 2)
  기계_판독_값.stage2.{systems · seeds · temperatures_K · prod_ps · equilib_ps · vseed_offset · n_atoms · save_fs · dt_fs ·
  bind_PS_median_disp_max_A · continuity_max_A {원소: 저장 간격당 Å} · mean_T_tol_frac} ·
  기계_판독_값.{decision · md_driver_sha16 · md_runner_sha16 · inputs_sha256 · inclusion.min_pair_excl_PS_A_gt} · 입력_2026_11_10.시드
판독 허가 (카드 '판독_허가_2단계'): {근거 · by · EB_회신 (kb/reviews/ 아래 파일 · 저장소 기준 경로) · 대조_잡_출력 (경로) ·
  대조_잡_sha256} — 대조 잡 출력이 kind li2s3_stage2_control/v2 · same = True · 깨끗한 작업 트리 · 도구 sha16 이 지금 판과 같아야 한다
  · (있으면) 큐_끝_줄_유실_인정 — 필드 여섯이 다 차 있어야 하고 (빠지면 거부) 그 결정이 원장에서 active 여야 한다 (아니면 거부)

v2 런 (고친 큐 run_stage2_kgy_v2.sh — cond550 · rerun) — 런 폴더에 exec_v2_start.json 이 있으면 그 런은 v2 로 읽는다:
  ①·⑥·⑦ 의 증거가 러너 로그 대신 실행 기록이다 (큐 · 드라이버 sha16 = 카드 · 카드 값 · 입력 sha256 · 명령 인수 = 카드에서 만든
  v2 틀 · 결속 기록 (판독 · 보류) 을 판독 시점에 다시 · 끝 기록 status complete · 종료 코드 0 · 산출물 sha256 = 지금 파일 · gpu_h) ·
  ②–⑤ 는 v1 과 같은 검사 (prod = 그 온도의 카드 값 · 원래 BASE = 실행 기록의 base). 대응표는 VERIFY_MAP (출력에도 싣는다).
  판독 갈래 --phase: ladder (사다리 · 기본 · readout_stage2.json) · cond550 (conditional.T_K + 사다리 · '끝난 뒤 한 번 더' ·
  사다리 판독 고정 기록이 cond550 자격 True 일 때만 · readout_stage2_cond550.json · pressure_stage2_cond550.json · 갈래 확정).
  cond550 판독은 동결된다: 사다리 판독 고정 기록의 행 지문 = 지금 사다리 런 지문 · 판독 도구 sha16 · 카드 기계_판독_값 해시가 같을 때만
  (하나라도 다르면 거부 · 리뷰 EE P1-1) · 550 K 런의 결속은 그 고정 기록 (경로 · sha256 = 지금 고정 기록 · P2-1).
  v2 런이 하나라도 있으면 v1 큐 끝 줄 대신 큐 잠금이 비어 있고 풀리지 않은 v2 멈춤 (by · reason 있는 풂만 셈) 이 없어야 한다 ·
  지금 queue_v2 결정 active. v2 런의 출처 (리뷰 EE P1-2): 시작 기록 test false (시험 런은 판독 selftest 만 받는다 — ALLOW_TEST_RUNS) ·
  card_is_repo_card · decisions_is_repo · repo_clean 참 · 그 커밋 (V2_REPO 에서 git show <repo_head>:<카드 · 원장>) 의 sha256 =
  시작 기록 · 그 커밋 원장에서 카드 결정 · queue_v2 결정 active (커밋을 못 찾으면 invalid).
  카드 기계 값 (v2 런을 읽을 때만): stage2.conditional.{T_K · prod_ps} · stage2.queue_v2.{sha16 · decision} (없으면 v2 런은 invalid).

⛔ 이 도구가 못 하는 것
  · R(T) · ΔEa 를 내지 않는다 (3 단계) · 판정 규칙을 새로 만들지 않는다 (glass_v2_readout · quench_ss_event 그대로).
  · v1 런은 v1 큐 (run_stage2_kgy.sh · PHASE ladder) 의 로그 꼴로만 · v2 런은 v2 실행 기록 꼴로만 읽는다 (그 밖의 큐는 모른다).
  · 러너의 지문 검사와 드라이버 실행 사이 (GPU 대기) 에 파일이 바뀌었다가 되돌아간 경우 · 큐 도중의 러너 교체 · 패키지 판
    변경은 못 본다 (잔여 위험).
  · 골격 판정은 생산 첫 프레임 대비다 — 담금질 결함이 준비 구간 · 생산 구간 전체에서 보존됐다고 말하지 않는다 (ⓐ–ⓒ 는 기록만).
  · 검증 실패 · 미완은 수송 게이트 미통과가 아니다 — W 밖으로 세지 않고 판정 보류만 한다 (처리는 카드 · 사용자 결정).
  · 끝 줄 유실 인정은 끝 줄이 **왜** 없는지 (tee · tmux 창 닫힘 등) 를 증명하지 않는다 — 남은 완료 기록 (블록의 큐 ✅ 줄 = 명단 ·
    장부 rc 0 · 장부 시간 = ✅ 줄 시간 · 잠금 풀림) 이 서로 맞는지와 인정 뒤에 로그 · 장부가 안 바뀌었는지만 본다 (그 판단은 카드 결정이 진다).
  · 비용은 러너 · 큐 벽시계다 (GPU 대기가 섞인다). Li 의 프레임 간 이동은 상한 검사에만 쓰고 기록하지 않는다 (수송 값 아님 원칙).
  · v2 큐 판은 카드 queue_v2.sha16 하나로만 받는다 — 큐를 고쳐 카드가 새 sha16 을 고정하면 옛 판으로 돈 v2 런은 invalid 다 (카드 결정).
  · v2 런의 옮겨 남긴 옛 폴더 (T<T>.superseded_*) 는 읽지 않는다 (기록만) · 멈춤 · 비용 정함 기록은 출력에 싣고 풀리지 않은 멈춤만
    보류 사유로 쓴다 (그 사람 결정이 옳았는지는 보지 않는다).
  · cond550 판독의 동결은 사다리 판독 뒤에 바뀐 것을 거부할 뿐 — 사다리 판독 전에 고른 표본 (결과를 안 본 재실행) 은 못 가린다.
  · v2 런의 커밋 결속은 판독 도구가 도는 저장소 (V2_REPO) 에 그 커밋이 있어야 한다 (없으면 invalid · 같은 저장소의 worktree 에서 읽는다).

--selftest — 양성 픽스처는 실제 생산자에서 만든다: 임시 폴더에서 실제 v1 큐 (run_stage2_kgy.sh) → 실제 v2 러너 → 실제 MD 드라이버를
  돌리고, 그 사본에 실제 v2 큐 (run_stage2_kgy_v2.sh · PHASE=rerun → 섞인 사다리 판독 → PHASE=cond550 → cond550 판독) 를 돌린다
  (fairchem 스텁 · 가짜 nvidia-smi · GPU 안 씀 · 저장소 파일은 안 바꾼다 · 시험 카드라 V2_TEST=1 — 이 동안만 시험 런을 받는다 ·
  생산 경로는 임시 git 저장소의 v2 큐 사본으로 따로 시험). bash · flock · coreutils · git 이 있어야 한다 (≈ 2 분).
  스텁의 Li 는 힘 없는 브라운 입자라 시험 카드의 Li 이동 상한만 6 Å 로 둔다 (실제 카드 값은 카드가 정한다).
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import hashlib
import json
import math
import os
import pathlib
import re
import shutil
import subprocess
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
CARD = REPO / "db" / "properties" / "lpscl_glass_dense_protocol_ensemble_estimand_2026_11_10.json"
DECISIONS = REPO / "db" / "governance" / "decisions.json"
NEED_ACTIVE = ("D-2026-11-10-li2s3-dense-protocol-ensemble", "D-2026-11-10-li2s3-dense-protocol-ensemble-amend1")
READ_PERMIT_KEY = "판독_허가_2단계"
#: 카드 개정 4 (2026-11-14 · 결과 전) — 순수 v1 큐의 '■ 큐 끝 · PHASE ladder' 줄이 파일에 안 남았을 때의 인정 (판독 허가 안 · 결정 하나)
ENDLINE_ACK_KEY = "큐_끝_줄_유실_인정"
ENDLINE_ACK_FIELDS = ("결정", "by", "근거", "사다리_블록_마지막_줄", "사다리_블록_sha256", "장부_sha256")
LADDER_START, LADDER_END = "▶ li2s-3 2 단계 큐 시작 · PHASE ladder · ", "■ 큐 끝 · PHASE ladder"
#: v1 큐 (run_stage2_kgy.sh) 가 런마다 찍는 줄 — say "✅ $x seed$sd T$T 끝 · $h h · 누적 $(cum_h) / $CAP_H h" (h = 장부 hours 와 같은 값)
QUEUE_DONE_RE = re.compile(r"^\[([0-9-]+ [0-9:]+)\] ✅ (\S+) seed(\d+) T(\d+) 끝 · ([0-9.]+) h · 누적 ([0-9.]+) / ([0-9.]+) h$")
LEDGER_HEAD = "system\tT_K\tseed\tprod_ps\tstart\tend\thours\trc"
N_BOOT = 400                      # 10-14 대조 계 판독과 같은 값 (σ 가 n_boot 에 달려 있다)
BIND_TOL_A = 1e-6
STAGE2_KEYS = ("systems", "seeds", "temperatures_K", "prod_ps", "equilib_ps", "vseed_offset", "n_atoms", "save_fs", "dt_fs",
               "bind_PS_median_disp_max_A", "continuity_max_A", "mean_T_tol_frac")
#: 판독 경로의 도구 — 출력의 출처 기록 · 대조 잡과 판독이 같은 판인지 (판독 허가) 를 이것으로 본다
TOOL_FILES = ("tools/ionic/li2s3_stage2_readout.py", "tools/ionic/glass_v2_readout.py", "tools/ionic/quench_ss_event.py",
              "tools/ionic/msd_diffusive_check.py", "tools/ionic/melt_quench_uma.py")
#: ⑦ 보조 — 큐가 돈 worktree 의 파일 (드라이버 · 러너는 카드 sha16 과 대조 · 큐 파일은 기록)
QUEUE_V2_REL = "db/inputs/li2s3_dense_ensemble_2026_11_10/run_stage2_kgy_v2.sh"
WT_FILES = {"md_driver": "tools/modelc_v3/disorder_ensemble_diffusion.py",
            "md_runner": "db/raw/lpscl_glass_md_v2_2026_09_30/glass_kgy_q_v2.sh",
            "queue_v1": "db/inputs/li2s3_dense_ensemble_2026_11_10/run_stage2_kgy.sh",
            "queue_v2": QUEUE_V2_REL}
OUT_DIRNAME, READOUT_NAME, PRESSURE_NAME, PRESSURE_RUNS = "readout_stage2", "readout_stage2.json", "pressure_stage2.json", "pressure_runs"
#: 판독 갈래별 고정 출력 (한 번만) — ladder 는 v1 판 그대로 · cond550 은 '끝난 뒤 한 번 더'
OUT_NAMES = {"ladder": (READOUT_NAME, PRESSURE_NAME), "cond550": ("readout_stage2_cond550.json", "pressure_stage2_cond550.json")}
V2_START, V2_END = "exec_v2_start.json", "exec_v2_end.json"
CARD_REL = "db/properties/lpscl_glass_dense_protocol_ensemble_estimand_2026_11_10.json"
DECISIONS_REL = "db/governance/decisions.json"
#: v2 런의 커밋 결속 (git show <repo_head>:<카드 · 원장>) 을 볼 저장소 — 판독 도구가 도는 저장소 (selftest 만 임시 저장소로 바꾼다)
V2_REPO = REPO
#: 시험 런 (V2_TEST=1 · 시작 기록 test: true) 을 받을까 — 판독 도구 selftest 만 True (명령줄 · 환경변수로는 못 켠다 · 리뷰 EE P1-2)
ALLOW_TEST_RUNS = False
CONTROL_KIND = "li2s3_stage2_control/v2"
#: v1 · v2 런을 한 판독에 넣는 검증 대응표 (카드 개정 EB 문장 6 · 결과 전) — 어느 검사를 어느 증거로 결속하나
VERIFY_MAP = [
    {"검사": "① 끝남 · 종료 코드", "v1": "계 러너 로그의 런 호출 블록 하나 — '✅ T<T> seed<S> 끝 (rc 0)' · '■ 큐 끝 · T:S:prod' (끝 줄 없음 = incomplete)",
     "v2": "런 폴더 exec_v2_start.json · exec_v2_end.json — 같은 run_id · status complete · driver_rc 0 (끝 기록 없음 = incomplete)"},
    {"검사": "① 실행된 코드", "v1": "러너 블록 '드라이버 sha16 <카드> ✅' · 큐 로그 '문지기 ✓ … 러너 sha16 <카드>'",
     "v2": "시작 기록 driver_sha16 = 카드 md_driver_sha16 · queue_v2_sha16 = 카드 stage2.queue_v2.sha16 (러너 없음 — 큐가 드라이버를 직접 부른다)"},
    {"검사": "① 큐 설정 (온도 · 시드 · 계 · prod)", "v1": "큐 로그 시작 줄 = 카드 · 러너 블록 발사 줄 · 'run_meta = 본 런 설정' · 'dt = 기준과 같다'",
     "v2": "시작 기록 card_values (런을 정하는 값) = 지금 카드 · argv[2:] = 카드에서 만든 v2 명령 틀 (온도 · 길이 · 시드 · save · dt · friction · 창 · turbo)"},
    {"검사": "① 원래 BASE (v0_xyz 대조)", "v1": "큐 로그 '판 — … · BASE <경로>' 줄", "v2": "시작 기록 base"},
    {"검사": "① 결속 기록", "v1": "없음 (사다리 16 런)",
     "v2": "cond550 = 사다리 판독 고정 기록 (그 경로만 · sha256 = 지금 고정 기록 · 두 계 600 K 측정 가능) · rerun = 보류 기록 (경로 · sha256 · "
           "그 런이 invalid · incomplete · 런 지문) — 판독 시점에 다시 본다"},
    {"검사": "① 출처 (카드 · 원장 · 저장소)", "v1": "큐 로그 '판 —' 줄의 repo HEAD (기록만)",
     "v2": "시작 기록 test false · card_is_repo_card · decisions_is_repo · repo_clean 참 · 그 커밋 (git show <repo_head>:<카드 · 원장>) 의 sha256 = "
           "시작 기록 · 그 커밋 원장에서 카드 · queue_v2 결정 active (못 찾음 = invalid · 리뷰 EE P1-2)"},
    {"검사": "② 설정 (run_meta · ensemble_results 끝 요약)", "v1": "카드 값 (prod = 사다리)", "v2": "같은 검사 (prod = 그 온도의 카드 값 — 550 K 는 conditional.prod_ps)"},
    {"검사": "③ 입력 결속", "v1": "init sha256 = 카드 · config.xyz = init · 첫 프레임 셀 · P/S 변위 중앙값",
     "v2": "같은 검사 + 시작 기록 input_sha256 (실행 직전 다시 해시한 값) = 카드"},
    {"검사": "④ 궤적 · ⑤ 산출물", "v1": "aimd · traj · md.log · msd.json 검사", "v2": "같은 검사 + 끝 기록 outputs_sha256 = 지금 파일 (기록 뒤 바뀐 산출물은 invalid)"},
    {"검사": "⑥ 비용", "v1": "장부 행 하나 (없으면 러너 블록 시각)", "v2": "끝 기록 gpu_h (장부 행 = 끝 기록 ledger_row 인지 함께 적는다)"},
    {"검사": "⑦ 보조 (판독 시점 worktree)", "v1": "드라이버 · 러너 sha16 = 카드 · 큐 파일 sha256 기록", "v2": "드라이버 sha16 = 카드 · v2 큐 파일 sha16 = 카드 queue_v2.sha16"},
    {"검사": "판정 보류 (한 판독)", "v1": "v1 런만이면 그대로 — v1 큐 로그 valid · 큐 끝 줄 · 계획 런 모두 valid",
     "v2": "v2 런이 하나라도 있으면 — 계획 런 모두 valid (각자 자기 증거로) · v1 런이 있으면 v1 큐 로그에 문제가 없을 것 · 큐 잠금이 비어 있을 것 · "
           "풀리지 않은 v2 멈춤 (queue_v2_stops.jsonl · by · reason 있는 풂만 셈) 이 없을 것 · 지금 카드 queue_v2 결정 active "
           "(v1 큐 끝 줄은 요구하지 않는다 — v1 이 멈춘 뒤 남은 런을 v2 가 돌린 경우)"},
    {"검사": "판정 보류 · 공통 (리뷰 EE)", "v1": "사다리 블록 밖의 v1 호출 → 따로 보류 사유 (런은 그대로) · 잠금이 쥐어져 있으면 보류 기록을 안 쓰고 거부",
     "v2": "같다 · 보류 기록은 런마다 지문 (산출물 7 + 시작 · 끝 기록)"},
    {"검사": "cond550 판독 동결 (리뷰 EE P1-1)", "v1": "사다리 판독 고정 기록의 행 지문 (러너 블록 시작 · 파일 sha256) = 지금",
     "v2": "행 지문 (run_id · 파일 sha256) = 지금 · 판독 도구 sha16 · 카드 기계_판독_값 해시 = 사다리 판독 때 (하나라도 다르면 거부)"},
]
PRESSURE_EVERY_PS = 1.0           # li2s-2 카드 §2 MD_압력 (li2s-3 승계): 1 ps 간격 · t = 1 … prod ps (400 ps 런당 400 프레임)
PRESSURE_WARN_GPA = 1.0           # li2s-2 카드 §1b · §3: 같은 온도 두 계 ⟨P⟩ 차 > 1 GPa 면 경고 하나 더 (보호 기준 아님)
KB_EV = 8.617333262e-5
CONTROL_T = 600
#: 10-14 대조 계 kgy 런의 라벨 · 난수 — 러너 기본값 (glass_kgy_q_v2.sh LABEL_PREFIX lpscl_glass_v2 · run_600k_kgy.sh
#  LABEL_PREFIX lpscl_glass_ctrlB · VSEED_OFFSET 1000 — run_600k_kgy.sh selftest 의 기준 run_meta 와 같다)
CONTROL_LABEL = {"A": "lpscl_glass_v2_s{S}_T600", "B": "lpscl_glass_ctrlB_s{S}_T600"}
CONTROL_VSEED_OFFSET = 1000
EXIT_REFUSED, EXIT_HOLD = 2, 3
TS_RE = r"\[(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)\]"
DEFECT_LABEL_SOURCE = "카드 '입력_2026_11_10.시드' (담금질 final.xyz 기준 · 11-10 kgy 읽기 블록) — 생산 뒤 모습으로 다시 붙이지 않는다"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


class Refused(SystemExit):
    """거부 (종료 2) — 문지기 조건이 안 맞는다. 메시지를 들고 다닌다 (main 이 찍고 selftest 가 읽는다)."""

    def __init__(self, msg):
        super().__init__(EXIT_REFUSED)
        self.msg = msg

    def __str__(self):
        return self.msg


def _sha(p) -> str:
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def _num_eq(a, b, tol=1e-9) -> bool:
    try:
        return a is not None and not isinstance(a, bool) and abs(float(a) - float(b)) <= tol
    except (TypeError, ValueError):
        return False


def _same(g, w) -> bool:
    if isinstance(w, bool):
        return g is w
    if isinstance(w, (int, float)):
        return _num_eq(g, w)
    if isinstance(w, list):
        return isinstance(g, list) and len(g) == len(w) and all(_same(a, b) for a, b in zip(g, w))
    return g == w


def _write_new(path, obj) -> pathlib.Path:
    """새 파일로만 쓴다 (있으면 FileExistsError — 덮지 않는다)."""
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "x", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, ensure_ascii=False, indent=1, default=str) + "\n")
    return path


def _ts(s):
    return _dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def fp_rels(T):
    """런 지문의 파일 — 산출물 7 (v2 큐 outputs_sha) + v2 시작 · 끝 기록. v2 큐 run_fingerprint 와 같은 정의 (보류 기록 · 판독 행)."""
    return ["run_meta.json", "ensemble_results.json", "d0.00_cfg0/config.xyz"] + [
        f"d0.00_cfg0/T{int(T)}/{x}" for x in ("traj.xyz", "msd.json", "aimd_results.json", "md.log")] + [V2_START, V2_END]


def run_fingerprint(rd, T) -> dict:
    """런 폴더 지문 {파일: sha256 · 없으면 None} — 보류 기록 · 사다리 판독 행에 싣는다 (리뷰 EE P1-1)."""
    rd = pathlib.Path(rd)
    return {r: (_sha(rd / r) if (rd / r).is_file() else None) for r in fp_rels(T)}


def rules_sha256(card_obj) -> str:
    """카드 기계_판독_값 해시 (정렬 키 JSON) — 사다리 판독 · cond550 판독이 같은 규칙 값인지 (리뷰 EE P1-1)."""
    return hashlib.sha256(json.dumps(card_obj.get("기계_판독_값"), sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def ledger_total(base):
    """장부 (cost_ledger.tsv) 전체 합 — 옮긴 런 · 정한 비용 포함 (캠페인 비용은 이것으로만 적는다 · 리뷰 EE P2-5). 못 읽으면 None."""
    try:
        lines = (pathlib.Path(base) / "cost_ledger.tsv").read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    tot = 0.0
    for ln in lines[1:]:
        if not ln.strip():
            continue
        try:
            h = float(ln.split("\t")[6])
        except (IndexError, ValueError):
            return None
        if not (math.isfinite(h) and h >= 0):
            return None
        tot += h
    return round(tot, 6)


def card_values(card_path=CARD) -> dict:
    """카드 기계 값 → 판독에 쓰는 값. 도구는 값을 따로 갖지 않는다 — 모자라면 거부 (종료 2)."""
    import quench_ss_event as Q
    p = pathlib.Path(card_path)
    c = json.loads(p.read_text(encoding="utf-8"))
    mv = c.get("기계_판독_값") or {}
    s2 = mv.get("stage2") or {}
    miss = [f"stage2.{k}" for k in STAGE2_KEYS if k not in s2]
    miss += [k for k in ("decision", "md_driver_sha16", "md_runner_sha16", "inputs_sha256") if k not in mv]
    if "min_pair_excl_PS_A_gt" not in (mv.get("inclusion") or {}):
        miss.append("inclusion.min_pair_excl_PS_A_gt")
    inp = (c.get("입력_2026_11_10") or {}).get("시드")
    if not isinstance(inp, dict):
        miss.append("입력_2026_11_10.시드")
    if miss:
        raise Refused(f"⛔ 카드 {p.name} 의 기계 값이 모자란다 {miss} — 도구는 이 값을 따로 갖지 않는다 (카드 개정에서 넣는다 · 결과 전)")
    if not (s2["systems"] and s2["seeds"] and s2["temperatures_K"]):
        raise Refused("⛔ 카드 stage2 의 systems · seeds · temperatures_K 가 비었다")
    defects = {}
    for k, v in inp.items():
        pair, dmin = v.get("그_쌍"), v.get("최단_원자간_P_S_제외_A")
        defects[k] = {"P_S_배위": v.get("P_S_배위"), "다리_S": v.get("다리_S"), "P_P": v.get("P_P"), "li2s2_판정": v.get("li2s2_판정"),
                      "최단_원자간_P_S_제외_A": dmin, "그_쌍": pair,
                      "S_S_lt_cut": bool(pair == "S-S" and dmin is not None and float(dmin) < Q.SS_CUT), "S_S_cut_A": Q.SS_CUT}
    return {"systems": list(s2["systems"]), "seeds": [int(x) for x in s2["seeds"]], "temperatures": [int(x) for x in s2["temperatures_K"]],
            "prod_ps": float(s2["prod_ps"]), "equilib_ps": float(s2["equilib_ps"]), "vseed_offset": int(s2["vseed_offset"]),
            "n_atoms": int(s2["n_atoms"]), "save_fs": float(s2["save_fs"]), "dt_fs": float(s2["dt_fs"]),
            "bind_max_A": float(s2["bind_PS_median_disp_max_A"]),
            "caps": {str(k): float(x) for k, x in dict(s2["continuity_max_A"]).items()}, "T_tol": float(s2["mean_T_tol_frac"]),
            "decision": mv["decision"], "md_driver_sha16": mv["md_driver_sha16"], "md_runner_sha16": mv["md_runner_sha16"],
            "inputs_sha256": dict(mv["inputs_sha256"]), "inclusion_min_pair": float(mv["inclusion"]["min_pair_excl_PS_A_gt"]),
            "defects": defects, "read_permit": c.get(READ_PERMIT_KEY), "card_sha256": _sha(p), "card_path": str(p),
            "rules_sha256": rules_sha256(c),
            # v2 런을 읽을 때만 쓴다 (없으면 None — v1 판독은 이 값을 안 본다)
            "cond": ({"T_K": int(s2["conditional"]["T_K"]), "prod_ps": float(s2["conditional"]["prod_ps"])}
                     if isinstance(s2.get("conditional"), dict) and {"T_K", "prod_ps"} <= set(s2["conditional"]) else None),
            "queue_v2_sha16": (s2.get("queue_v2") or {}).get("sha16") if isinstance(s2.get("queue_v2"), dict) else None,
            "queue_v2_decision": (s2.get("queue_v2") or {}).get("decision") if isinstance(s2.get("queue_v2"), dict) else None}


def decision_states(path=DECISIONS, ids=NEED_ACTIVE) -> dict:
    D = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    L = D["decisions"] if isinstance(D, dict) else D
    return {i: next((e.get("decision_state") for e in L if e.get("id") == i), None) for i in ids}


def _git(repo, *args):
    try:
        r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout if r.returncode == 0 else None


def provenance(repo=REPO) -> dict:
    """출처 기록 — 판독 경로 도구 sha16 · git HEAD · 추적 파일이 깨끗한가 (추적 안 되는 파일은 안 본다) · UTC 시각."""
    repo = pathlib.Path(repo)
    head = _git(repo, "rev-parse", "HEAD")
    st = _git(repo, "status", "--porcelain", "--untracked-files=no")
    dirty = [ln for ln in (st or "").splitlines() if ln.strip()]
    return {"tool_sha16": {rel: (_sha(repo / rel)[:16] if (repo / rel).is_file() else None) for rel in TOOL_FILES},
            "git_head": head.strip() if head else None, "tree_clean": bool(st is not None and not dirty), "dirty_tracked": dirty[:20],
            "utc": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "repo": str(repo)}


def worktree_code(worktree) -> dict:
    wt = pathlib.Path(worktree)
    out = {"worktree": str(wt)}
    for key, rel in WT_FILES.items():
        f = wt / rel
        out[key + "_sha256"] = _sha(f) if f.is_file() else None
    return out


def _mic_disp(a, b, cell):
    d = np.asarray(b, float) - np.asarray(a, float)
    inv = np.linalg.inv(cell)
    f = d @ inv
    f -= np.round(f)
    return np.linalg.norm(f @ cell, axis=1)


# ───────────────────────── ① 실행 기록 (큐 로그 · 러너 로그) ─────────────────────────
def queue_record(base, cv) -> dict:
    """<BASE>/stage2_kgy.log (v1 큐 tee) — 사다리 블록 (첫 PHASE ladder 시작 줄 ~ 첫 '■ 큐 끝 · PHASE ladder') 안에서만 읽는다:
    시작 줄 하나 · 문지기 줄 하나 · 판 줄 하나 · 큐 끝 줄. 블록 밖의 v1 호출 (뒤에 다시 띄움 · PHASE cond550 등) 은 런을 무효로 만들지
    않고 따로 보류 사유로 적는다 (other_invocations · 리뷰 EE P2-6)."""
    p = pathlib.Path(base) / "stage2_kgy.log"
    rec = {"log": str(p), "problems": [], "complete": False, "base_original": None, "other_invocations": [], "end_line": None}
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        rec["problems"].append("큐 로그 stage2_kgy.log 가 없다 — 실행 기록으로 결속할 수 없다")
        rec["status"] = "invalid"
        return rec
    starts = [i for i, ln in enumerate(lines) if LADDER_START in ln]
    if not starts:
        rec["problems"].append("PHASE ladder 큐 시작 줄이 0 개 (하나여야)")
        rec["status"] = "invalid"
        return rec
    s0 = starts[0]
    e0 = next((i for i in range(s0, len(lines)) if LADDER_END in lines[i]), None)
    rec["end_line"] = None if e0 is None else {"kind": "끝 줄", "줄_번호": e0 + 1}
    pmt = cv.get("read_permit") if isinstance(cv.get("read_permit"), dict) else {}
    if ENDLINE_ACK_KEY in pmt:                   # 카드 개정 4 — 끝 줄이 없을 때만 인정을 쓴다
        if e0 is not None:
            rec["problems"].append(f"끝 줄 유실 인정: 카드에 '{ENDLINE_ACK_KEY}' 가 있는데 큐 로그에 '{LADDER_END}' 줄이 있다 "
                                   "(인정 뒤에 큐 로그가 바뀌었다 — 사람이 본다)")
        else:
            e0, rec["end_line"], ack_probs = endline_ack_check(base, cv, lines, s0, pmt[ENDLINE_ACK_KEY])
            rec["problems"].extend(f"끝 줄 유실 인정: {q}" for q in ack_probs)
    stop_at = len(lines) if e0 is None else e0 + 1
    inner = [i for i in starts if i < stop_at]
    if len(inner) != 1:
        rec["problems"].append(f"PHASE ladder 큐 시작 줄이 사다리 블록 안에 {len(inner)} 개 (하나여야 — 끝나기 전에 다시 띄운 것 · v1 운영 규칙 위반)")
        rec["status"] = "invalid"
        return rec
    rec["other_invocations"] = [ln for i, ln in enumerate(lines) if (i < s0 or i >= stop_at) and "▶ li2s-3 2 단계 큐 시작 · PHASE " in ln][:10]
    tail = lines[s0:stop_at]
    m = re.search(r"PHASE ladder · 온도 ([0-9 ]+?) · 시드 ([0-9 ]+?) · 계 ([A-Za-z ]+?) · prod ([0-9.]+) ps", tail[0])
    if not m:
        rec["problems"].append("큐 시작 줄의 꼴을 못 읽었다")
    else:
        st = {"temperatures": [int(x) for x in m.group(1).split()], "seeds": [int(x) for x in m.group(2).split()],
              "systems": m.group(3).split(), "prod_ps": float(m.group(4))}
        rec["start"] = st
        for k, w in (("temperatures", cv["temperatures"]), ("seeds", cv["seeds"]), ("systems", cv["systems"])):
            if st[k] != list(w):
                rec["problems"].append(f"큐 시작 줄의 {k} {st[k]} ≠ 카드 {list(w)}")
        if not _num_eq(st["prod_ps"], cv["prod_ps"]):
            rec["problems"].append(f"큐 시작 줄의 prod {st['prod_ps']:g} ≠ 카드 {cv['prod_ps']:g}")
    gk = [g for g in (re.search(r"문지기 ✓ — 카드 (\S+) \(active\) · 러너 sha16 ([0-9a-f]{16}) ·", ln) for ln in tail) if g]
    if len(gk) != 1:
        rec["problems"].append(f"큐 '문지기 ✓' 줄이 {len(gk)} 개 (하나여야)")
    else:
        rec["gatekeep"] = {"decision": gk[0].group(1), "runner_sha16": gk[0].group(2)}
        if gk[0].group(1) != cv["decision"]:
            rec["problems"].append(f"큐 문지기의 카드 결정 {gk[0].group(1)} ≠ 카드 {cv['decision']}")
        if gk[0].group(2) != cv["md_runner_sha16"]:
            rec["problems"].append(f"큐 문지기의 러너 sha16 {gk[0].group(2)} ≠ 카드 {cv['md_runner_sha16']} (다른 러너로 돌았다)")
    pv = [x for x in (re.search(r"판 — (.*) · repo (\S+) · BASE (.+?) · PHASE (\S+)\s*$", ln) for ln in tail) if x]
    if len(pv) != 1:
        rec["problems"].append(f"큐 '판 —' 줄이 {len(pv)} 개 (하나여야 — 원래 BASE 를 못 읽는다)")
    else:
        rec.update(versions=pv[0].group(1).strip(), repo_head=pv[0].group(2), base_original=pv[0].group(3).strip())
        if pv[0].group(4) != "ladder":
            rec["problems"].append(f"큐 '판 —' 줄의 PHASE {pv[0].group(4)} ≠ ladder")
    rec["complete"] = e0 is not None
    rec["status"] = "invalid" if rec["problems"] else ("valid" if rec["complete"] else "incomplete")
    return rec


def ladder_roster(cv) -> list:
    """v1 큐의 돌림 순서 — run_stage2_kgy.sh 의 `for T in $TEMPS; do for sd in $SEEDS; do for x in $SYSTEMS` (온도 → 시드 → 계)."""
    return [(x, sd, T) for T in cv["temperatures"] for sd in cv["seeds"] for x in cv["systems"]]


def _block_sha(block_lines) -> str:
    """사다리 블록 지문 — 줄 (splitlines) 을 '\\n' 으로 이은 UTF-8 의 sha256 (끝 줄바꿈 · CR 은 줄 나눔이 먹는다)."""
    return hashlib.sha256("\n".join(block_lines).encode("utf-8")).hexdigest()


def endline_ack_check(base, cv, lines, s0, ack):
    """카드 개정 4 — '■ 큐 끝 · PHASE ladder' 줄이 없을 때 판독 허가의 '큐_끝_줄_유실_인정' 과 대조한다.
    받는 것: 인정한 마지막 줄이 사다리 시작 뒤에 정확히 한 번 · 블록 (시작 줄 ~ 그 줄) sha256 = 인정 · 장부 sha256 = 인정 ·
    그 줄 = 명단 마지막 런의 큐 '✅ … 끝 · h · 누적' 줄 · 블록의 큐 ✅ 줄 = 명단 (돌림 순서 그대로 · 하나씩) · 장부 = 머리 +
    명단 행 하나씩 · rc 0 · prod = 카드 · 장부 시간 = 그 런의 큐 ✅ 줄 시간 · 큐 잠금 풀림.
    반환 (블록 끝 줄 번호 (0 부터) 또는 None, 기록, 문제 목록). 결정 active 는 여기서 안 본다 (readout · pressure 문지기 _gate)."""
    info = {"kind": "끝 줄 유실 인정", "결정": ack.get("결정") if isinstance(ack, dict) else None}
    if not isinstance(ack, dict):
        return None, info, [f"'{ENDLINE_ACK_KEY}' 가 dict 가 아니다"]
    miss = [k for k in ENDLINE_ACK_FIELDS if not str(ack.get(k) or "").strip()]
    if miss:
        return None, info, [f"'{ENDLINE_ACK_KEY}' 의 {miss} 가 비었다"]
    last = ack["사다리_블록_마지막_줄"]
    idx = [i for i in range(s0, len(lines)) if lines[i] == last]
    if len(idx) != 1:
        return None, info, [f"인정한 마지막 줄이 사다리 시작 뒤에 {len(idx)} 번 (한 번이어야)"]
    L = idx[0]
    block = lines[s0:L + 1]
    probs = []
    info.update(마지막_줄=last, 마지막_줄_번호=L + 1, 사다리_블록_sha256=_block_sha(block))
    if info["사다리_블록_sha256"] != ack["사다리_블록_sha256"]:
        probs.append("사다리 블록 sha256 ≠ 인정 (인정 뒤에 큐 로그가 바뀌었다)")
    roster = ladder_roster(cv)
    m = QUEUE_DONE_RE.match(last)
    if not m or (m.group(2), int(m.group(3)), int(m.group(4))) != roster[-1]:
        probs.append(f"인정한 마지막 줄이 명단 마지막 런 {roster[-1]} 의 큐 '✅ … 끝' 줄이 아니다")
    done = [(d.group(2), int(d.group(3)), int(d.group(4)), d.group(5)) for d in (QUEUE_DONE_RE.match(ln) for ln in block) if d]
    if [x[:3] for x in done] != roster:
        probs.append(f"사다리 블록의 큐 ✅ 줄 {len(done)} 개가 명단 {len(roster)} 런 (돌림 순서 · 하나씩) 과 다르다")
    lp = pathlib.Path(base) / "cost_ledger.tsv"
    try:
        lb = lp.read_bytes()
    except OSError:
        return None, info, probs + ["장부 cost_ledger.tsv 가 없다"]
    info["장부_sha256"] = hashlib.sha256(lb).hexdigest()
    if info["장부_sha256"] != ack["장부_sha256"]:
        probs.append("장부 sha256 ≠ 인정 (인정 뒤에 장부가 바뀌었다)")
    rows = lb.decode("utf-8", errors="replace").splitlines()
    if not rows or rows[0] != LEDGER_HEAD:
        probs.append("장부 머리 줄이 v1 큐 꼴이 아니다")
    body = [r.split("\t") for r in rows[1:] if r.strip()]
    keyed, bad_shape = {}, 0
    for r in body:
        try:
            k = (r[0], int(r[2]), int(r[1])) if len(r) == 8 else None
        except ValueError:
            k = None
        if k is None or k in keyed:
            bad_shape += 1
            continue
        keyed[k] = r
    if bad_shape or len(body) != len(roster) or sorted(keyed) != sorted(roster):
        probs.append(f"장부 행 {len(body)} 개 (꼴이 틀리거나 겹친 행 {bad_shape}) 가 명단 {len(roster)} 런과 하나씩 맞지 않는다")
    bad_rc = sorted(k for k, r in keyed.items() if r[7].strip() != "0")
    if bad_rc:
        probs.append(f"장부 rc ≠ 0 인 행 {bad_rc[:4]}")
    bad_prod = sorted(k for k, r in keyed.items() if not _num_eq(r[3], cv["prod_ps"]))
    if bad_prod:
        probs.append(f"장부 prod ≠ 카드 {cv['prod_ps']:g} 인 행 {bad_prod[:4]}")
    hrs = {x[:3]: x[3] for x in done}
    bad_h = sorted(k for k in roster if k in hrs and k in keyed and keyed[k][6].strip() != hrs[k])
    if bad_h:
        probs.append(f"장부 시간 ≠ 큐 ✅ 줄 시간 인 행 {bad_h[:4]}")
    if not queue_lock_free(base):
        probs.append("큐 잠금이 쥐어져 있다 — 큐 · 드라이버가 돌고 있다")
    info["검사"] = ("마지막 줄 한 번 · 블록 · 장부 sha256 · 마지막 줄 = 명단 마지막 런 ✅ · 블록 ✅ = 명단 · 장부 = 명단 · rc 0 · prod · "
                  "시간 = ✅ 줄 · 잠금 풀림")
    return (None if probs else L), info, probs


def endline_facts(base, cv) -> dict:
    """읽기만 — 큐 로그에 '■ 큐 끝 · PHASE ladder' 줄이 없을 때 카드 '큐_끝_줄_유실_인정' 에 넣을 사실을 낸다 (파일을 쓰지 않는다).
    마지막 줄 후보 = 사다리 시작 뒤 마지막 비지 않은 줄 · 같은 검사 (endline_ack_check) 를 그 사실로 돌린 문제 목록을 같이 싣는다
    (인정을 쓸지는 사람 · 카드 결정 — 이 도구는 사실만)."""
    base = pathlib.Path(base)
    out = {"kind": "li2s3_stage2_endline_facts/v1", "base": str(base.resolve()), "problems": []}
    try:
        lines = (base / "stage2_kgy.log").read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        out["problems"].append("큐 로그 stage2_kgy.log 가 없다")
        return out
    starts = [i for i, ln in enumerate(lines) if LADDER_START in ln]
    out["사다리_시작_줄"] = len(starts)
    if len(starts) != 1:
        out["problems"].append(f"PHASE ladder 큐 시작 줄이 {len(starts)} 개 (하나여야)")
        return out
    s0 = starts[0]
    if any(LADDER_END in lines[i] for i in range(s0, len(lines))):
        out["problems"].append(f"큐 로그에 '{LADDER_END}' 끝 줄이 있다 — 인정이 필요 없다")
        return out
    cand = next((i for i in range(len(lines) - 1, s0 - 1, -1) if lines[i].strip()), s0)
    led = base / "cost_ledger.tsv"
    probe = {"결정": "(사실 보기)", "by": "(사실 보기)", "근거": "(사실 보기)", "사다리_블록_마지막_줄": lines[cand],
             "사다리_블록_sha256": _block_sha(lines[s0:cand + 1]), "장부_sha256": _sha(led) if led.is_file() else "(장부 없음)"}
    _, info, probs = endline_ack_check(base, cv, lines, s0, probe)
    out.update({k: probe[k] for k in ("사다리_블록_마지막_줄", "사다리_블록_sha256", "장부_sha256")},
               마지막_줄_번호=cand + 1, 명단_런=len(ladder_roster(cv)), problems=probs,
               note="문제 0 이면 위 셋을 카드 판독 허가의 '큐_끝_줄_유실_인정' 에 넣고 결정 · by · 근거를 사람이 채운다 (카드 개정 4)")
    return out


def runner_blocks(log_path):
    """러너 로그 → 호출 블록 목록 ('▶ v2 큐 시작 · T:S:prod' 줄마다 하나). 로그가 없으면 None."""
    try:
        lines = pathlib.Path(log_path).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    blocks, cur = [], None
    for ln in lines:
        m = re.match(TS_RE + r" ▶ v2 큐 시작 · (\S+)\s*$", ln)
        if m:
            cur = {"start_ts": m.group(1), "item": m.group(2), "lines": []}
            blocks.append(cur)
        elif cur is not None:
            cur["lines"].append(ln)
    return blocks


def _block_T_seed(b):
    q = b["item"].split(":")
    try:
        return int(q[0]), int(q[1])
    except (ValueError, IndexError):
        return None


def check_block(b, T, seed, cv) -> dict:
    """그 런의 러너 호출 블록 하나 — 필수 줄 · 값 = 카드. 끝 줄 '✅ … 끝 (rc N)' 이 없으면 incomplete."""
    txt = "\n".join(b["lines"])
    probs = []
    vs = cv["vseed_offset"] + int(seed)
    q = b["item"].split(":")
    if len(q) != 3 or not _num_eq(q[2], cv["prod_ps"]):
        probs.append(f"러너 큐 항목 {b['item']!r} 의 prod ≠ 카드 {cv['prod_ps']:g}")
    end = re.search(TS_RE + rf" ✅ T{T} seed{seed} 끝 \(rc (-?\d+)\)", txt)
    res = {"item": b["item"], "start_ts": b["start_ts"], "end_ts": end.group(1) if end else None,
           "rc": int(end.group(2)) if end else None, "hours_log": None, "stop_lines": [ln for ln in b["lines"] if "⛔" in ln][:5]}
    if not end:
        res.update(problems=probs, incomplete=True)
        return res
    if res["rc"] != 0:
        probs.append(f"드라이버 종료 코드 {res['rc']} ≠ 0 (러너 로그)")
    m = re.search(r"드라이버 sha16 ([0-9a-f]{16}) ✅", txt)
    if not m or m.group(1) != cv["md_driver_sha16"]:
        probs.append(f"러너 블록의 드라이버 sha16 {m.group(1) if m else '없음'} ≠ 카드 {cv['md_driver_sha16']} (다른 드라이버로 돌았다)")
    m = re.search(rf"▶ T{T} seed{seed} PID \d+ · prod (\S+) ps · --seed (\d+) ·", txt)
    if not m or not _num_eq(m.group(1), cv["prod_ps"]) or int(m.group(2)) != vs:
        probs.append(f"러너 블록의 발사 줄이 없거나 prod · --seed ≠ 카드 ({cv['prod_ps']:g} · {vs})")
    m = re.search(r"OK run_meta = 본 런 설정 \(T·seed·v0·prod 만 다름 · prod (\S+) · seed (\d+)\)", txt)
    if not m or not _num_eq(m.group(1), cv["prod_ps"]) or int(m.group(2)) != vs:
        probs.append("러너 블록에 'run_meta = 본 런 설정' 줄이 없거나 prod · seed ≠ 카드")
    m = re.search(r"dt = 기준과 같다 \((\S+) ps/행\)", txt)
    if not m or not _num_eq(m.group(1), cv["dt_fs"] / 1000.0):
        probs.append(f"러너 블록에 'dt = 기준과 같다 ({cv['dt_fs'] / 1000.0:.4f} ps/행)' 줄이 없다")
    if not re.search(rf"■ 큐 끝 · {T}:{seed}:", txt):
        probs.append("러너 끝 줄 뒤 '■ 큐 끝' 줄이 없다 (러너가 끝을 못 찍고 죽었다)")
    try:
        res["hours_log"] = (_ts(end.group(1)) - _ts(b["start_ts"])).total_seconds() / 3600.0
    except ValueError:
        pass
    res.update(problems=probs, incomplete=False)
    return res


def _ledger_hours(ledger, sys_, T, seed):
    try:
        rows = list(csv.DictReader(pathlib.Path(ledger).read_text(encoding="utf-8").splitlines(), delimiter="\t"))
    except OSError:
        return None, "장부 없음"
    hit = [r for r in rows if r.get("system") == sys_ and r.get("T_K") == str(int(T)) and r.get("seed") == str(int(seed))]
    if len(hit) != 1:
        return None, f"장부 행 {len(hit)} 개"
    try:
        h = float(hit[0]["hours"])
    except (TypeError, ValueError, KeyError):
        return None, "장부 시간 못 읽음"
    if not (math.isfinite(h) and h >= 0):
        return None, f"장부 시간 {h}"
    return h, "장부"


# ───────────────────────── ④ 궤적 · ⑤ 산출물 ─────────────────────────
def check_trajectory(tdir, n_atoms, symbols0, prod_ps, T, equilib_ps, save_fs, dt_fs, caps, T_tol,
                     cell_ref=None, pos_ref=None, bind_max_A=None, keep_PS=False):
    """④ — 궤적 · 기록 유효성. → (문제 목록, 미완 여부, 프레임 자료 {P,S 좌표 · 셀} 또는 None, 기록 정보).
    프레임 수 = round(prod/save) — 드라이버는 평형 뒤 첫 관측을 한 간격 뒤에 찍는다 (프레임 k ↔ t = (k+1)·save)."""
    from ase.io import iread
    tdir = pathlib.Path(tdir)
    probs, incomplete, info = [], False, {}
    n_exp = int(round(prod_ps * 1000.0 / save_fs))
    try:
        ar = json.loads((tdir / "aimd_results.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ["aimd_results.json 없음 · 못 읽음"], True, None, info
    for k, want in (("T_K", float(T)), ("save_fs", save_fs), ("prod_ps", float(prod_ps)), ("dt_fs", dt_fs)):
        if not _num_eq(ar.get(k), want):
            probs.append(f"aimd_results {k} {ar.get(k)!r} ≠ {want}")
    if ar.get("n_frames") != n_exp:
        probs.append(f"aimd_results n_frames {ar.get('n_frames')!r} ≠ 계획 {n_exp} (= prod/save)")
    tp = tdir / "traj.xyz"
    if not tp.is_file():
        return probs + ["traj.xyz 없음"], True, None, info
    sym_arr = np.asarray(symbols0)
    els = sorted(set(symbols0))
    miss_cap = [e for e in els if e not in caps]
    if miss_cap:
        return probs + [f"카드 continuity_max_A 에 원소 {miss_cap} 의 상한이 없다"], False, None, info
    masks = {e: sym_arr == e for e in els}
    heavy_max = {e: 0.0 for e in els if e != "Li"}
    n, cell0, prev, P, S, broke = 0, None, None, [], [], False
    try:
        for a in iread(str(tp), index=":", format="extxyz"):
            sym = a.get_chemical_symbols()
            pos, cell = a.get_positions(), np.asarray(a.get_cell())
            if len(a) != n_atoms:
                probs.append(f"프레임 {n}: 원자 {len(a)} ≠ {n_atoms}"); broke = True
                break
            if sym != symbols0:
                probs.append(f"프레임 {n}: 원소 순서가 시작 구조와 다르다"); broke = True
                break
            if not (np.all(np.isfinite(pos)) and np.all(np.isfinite(cell))):
                probs.append(f"프레임 {n}: 좌표 · 셀이 유한하지 않다"); broke = True
                break
            if not all(a.pbc):
                probs.append(f"프레임 {n}: PBC 가 꺼져 있다"); broke = True
                break
            if cell0 is None:
                cell0 = cell
                if cell_ref is not None and float(np.abs(cell - np.asarray(cell_ref)).max()) > BIND_TOL_A:
                    probs.append("첫 프레임 셀 ≠ config.xyz 셀 (1e-6 Å) — 다른 구조의 궤적"); broke = True
                    break
                if pos_ref is not None:
                    mk = masks.get("P", np.zeros(len(sym_arr), bool)) | masks.get("S", np.zeros(len(sym_arr), bool))
                    med = float(np.median(_mic_disp(np.asarray(pos_ref)[mk], pos[mk], cell))) if mk.any() else float("inf")
                    info["bind_PS_median_disp_A"] = round(med, 4)
                    if not med < bind_max_A:
                        probs.append(f"첫 프레임 P · S 최소상 변위 중앙값 {med:.3f} Å ≥ {bind_max_A:g} Å — config.xyz 에서 시작한 궤적이 아니다")
                        broke = True
                        break
            elif float(np.abs(cell - cell0).max()) > 1e-9:
                probs.append(f"프레임 {n}: 셀이 바뀌었다 (NVT 인데)"); broke = True
                break
            if prev is not None:
                d = _mic_disp(prev, pos, cell)
                bad = [(e, float(d[masks[e]].max())) for e in els if float(d[masks[e]].max()) > caps[e]]
                if bad:
                    e, x = bad[0]
                    probs.append(f"프레임 {n - 1}→{n}: {e} 이동 {x:.2f} Å > 상한 {caps[e]:g} Å / {save_fs:g} fs (원자 순서 뒤섞임 · 이어붙인 궤적 의심)")
                    broke = True
                    break
                for e in heavy_max:
                    heavy_max[e] = max(heavy_max[e], float(d[masks[e]].max()))
            prev = pos
            if keep_PS:
                P.append(pos[masks.get("P", np.zeros(len(sym_arr), bool))]); S.append(pos[masks.get("S", np.zeros(len(sym_arr), bool))])
            n += 1
    except Exception as e:                                            # 못 읽은 것은 '변화 없음' 이 아니다
        probs.append(f"traj.xyz 를 못 읽었다 ({type(e).__name__}: {e})"); broke = True
    info["n_frames_read"] = n
    info["heavy_max_step_A"] = {e: round(x, 4) for e, x in heavy_max.items()}
    if not broke and n != n_exp:
        probs.append(f"traj.xyz 프레임 {n} ≠ 계획 {n_exp} (= prod/save)")
        incomplete = n < n_exp
    if not broke and n < 2:
        probs.append(f"traj.xyz 프레임 {n} 개 (2 개 미만)")
        incomplete = True
    try:
        lines = (tdir / "md.log").read_text(encoding="utf-8", errors="replace").splitlines()
        heads = [i for i, ln in enumerate(lines) if ln.strip().startswith("Time[ps]")]
        if heads != [0]:
            probs.append(f"md.log 머리 줄 {len(heads)} 개 (위치 {heads[:3]}) — 하나 · 첫 줄이어야 (이어 쓰기 · 다시 띄움 의심)")
        else:
            hdr = lines[0].split()
            it, iT = hdr.index("Time[ps]"), hdr.index("T[K]")
            rows = [ln.split() for ln in lines[1:] if ln.strip()]
            ts = np.array([float(r[it]) for r in rows])
            TT = np.array([float(r[iT]) for r in rows])
            dt_ps = dt_fs / 1000.0
            n_rows = int(round((equilib_ps + prod_ps) / dt_ps)) + 1
            if len(ts) != n_rows:
                probs.append(f"md.log 행 수 {len(ts)} ≠ 계획 {n_rows} (= (equilib + prod)/dt + 1)")
            if len(ts) < 2 or abs(ts[0]) > 1e-9 or np.any(np.abs(np.diff(ts) - dt_ps) > 1e-6):
                probs.append(f"md.log 시각이 0 에서 dt {dt_ps:g} ps 간격으로 단조 증가하지 않는다")
            if len(ts) and abs(ts[-1] - (equilib_ps + prod_ps)) > 1e-6:
                probs.append(f"md.log 끝 시각 {ts[-1]} ≠ {equilib_ps + prod_ps} ps")
                incomplete = incomplete or ts[-1] < equilib_ps + prod_ps
            prodT = TT[ts > equilib_ps + 1e-9] if len(ts) == len(TT) else np.array([])
            if prodT.size == 0 or not np.all(np.isfinite(prodT)):
                probs.append("md.log 생산 구간 온도를 못 읽었다")
            else:
                mT = float(prodT.mean())
                info["prod_mean_T_K"] = round(mT, 2)
                if abs(mT - float(T)) > T_tol * float(T):
                    probs.append(f"md.log 생산 평균 T {mT:.1f} K — 설정 {T} K 의 ± {100 * T_tol:g} % 밖 (열욕 · 드라이버 의심)")
    except (OSError, IndexError, ValueError) as e:
        probs.append(f"md.log 를 못 읽었다 ({type(e).__name__})")
    data = {"P": P, "S": S, "cell": cell0} if (keep_PS and not probs) else None
    return probs, incomplete, data, info


def check_msd(tdir, T, n_frames, save_fs) -> list:
    """⑤ — msd.json: read_run 이 쓰는 MTO 배열까지 (유한 · 단조 · 지연 범위 · 길이)."""
    try:
        d = json.loads((pathlib.Path(tdir) / "msd.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return [f"msd.json 을 못 읽었다 ({type(e).__name__})"]
    if not isinstance(d, dict):
        return ["msd.json 이 사전이 아니다"]
    probs, dt = [], save_fs / 1000.0
    if not _num_eq(d.get("T_K"), T):
        probs.append(f"msd.json T_K {d.get('T_K')!r} ≠ {T}")
    if not _same(d.get("fit_window_ps"), [2.0, 50.0]):
        probs.append(f"msd.json fit_window_ps {d.get('fit_window_ps')!r} ≠ 정본 창")

    def arr(k):
        v = d.get(k)
        if not isinstance(v, list):
            return None
        try:
            a = np.asarray(v, float)
        except (TypeError, ValueError):
            return None
        return a if a.ndim == 1 else None
    tp, mp, tm, mm = arr("times_ps"), arr("msd_Li_A2"), arr("times_ps_mto"), arr("msd_Li_A2_mto")
    if tp is None or mp is None or len(tp) != n_frames or len(mp) != n_frames:
        probs.append(f"msd.json times_ps · msd_Li_A2 가 없거나 길이 ≠ 프레임 수 {n_frames}")
    elif (not (np.all(np.isfinite(tp)) and np.all(np.isfinite(mp))) or abs(tp[0]) > 1e-9
          or np.any(np.abs(np.diff(tp) - dt) > 1e-6)):
        probs.append("msd.json times_ps · msd_Li_A2 가 유한하지 않거나 0 에서 save 간격이 아니다")
    if tm is None or mm is None or len(tm) != len(mm) or len(tm) < 3:
        probs.append("msd.json MTO 곡선 (times_ps_mto · msd_Li_A2_mto) 이 없거나 길이가 맞지 않다 — read_run 이 쓰는 배열")
    elif (not (np.all(np.isfinite(tm)) and np.all(np.isfinite(mm))) or np.any(np.diff(tm) <= 0)
          or abs(tm[0] - dt) > 1e-6 or abs(tm[-1] - (n_frames // 2) * dt) > 1e-6):
        probs.append(f"msd.json MTO 곡선이 유한 · 단조가 아니거나 지연 범위가 {dt:g} … {(n_frames // 2) * dt:g} ps 가 아니다")
    return probs


# ───────────────────────── 런 하나 · 전체 ─────────────────────────
def verify_run(base, sys_, seed, T, cv, worktree, qrec=None, blocks=None, keep_PS=False) -> dict:
    """런 하나의 사후 검증 ①–⑦ → {status: valid | invalid | incomplete, reasons, cost_h, ...}."""
    from ase.io import read
    base = pathlib.Path(base)
    T, seed = int(T), int(seed)
    if (base / sys_ / f"seed{seed}" / f"T{T}" / V2_START).exists():   # v2 큐 런 — 실행 기록으로 결속 (VERIFY_MAP)
        return verify_run_v2(base, sys_, seed, T, cv, worktree, keep_PS=keep_PS)
    qrec = queue_record(base, cv) if qrec is None else qrec
    blocks = runner_blocks(base / sys_ / "queue_kgy.log") if blocks is None else blocks
    rd = base / sys_ / f"seed{seed}" / f"T{T}"
    tdir = rd / "d0.00_cfg0" / f"T{T}"
    label = f"li2s3_{sys_}_s{seed}_T{T}"
    inc, inv = [], []
    out = {"system": sys_, "seed": seed, "T_K": T, "run_dir": str(rd), "queue_version": "v1", "runner_rc": None}
    started = rd.exists()
    if not started:
        inc.append("런 폴더가 없다 (시작 안 함)")
    # ① 실행 기록
    inv.extend(f"큐: {q}" for q in qrec.get("problems", []))
    bk = None
    if blocks is None:
        (inv if started else inc).append("러너 로그 queue_kgy.log 가 없다")
    else:
        hits = [b for b in blocks if _block_T_seed(b) == (T, seed)]
        if not hits:
            (inv if started else inc).append("러너 로그에 이 런의 호출 블록이 없다")
        elif len(hits) > 1:
            inv.append(f"러너 로그에 이 런의 호출 블록이 {len(hits)} 개 (다시 띄움 — v1 운영 규칙 위반)")
        else:
            bk = check_block(hits[0], T, seed, cv)
            out["runner_rc"] = bk["rc"]
            out["runner"] = {k: bk[k] for k in ("item", "start_ts", "end_ts", "rc", "hours_log", "stop_lines")}
            if bk["incomplete"]:
                inc.append("러너 끝 줄 ('✅ … 끝 (rc N)') 이 없다 — 끝나지 않았다")
            inv.extend(bk["problems"])
    ended = bool(bk and not bk["incomplete"])
    if started and not (tdir / "msd.json").is_file():
        (inv if ended else inc).append("msd.json 없음" + (" — 러너는 끝났다는데" if ended else " (끝나지 않았다)"))
    # ② 설정 — run_meta · ensemble_results 끝 요약
    try:
        m = json.loads((rd / "run_meta.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        m = None
        if started:
            inv.append("run_meta.json 없음 · 못 읽음")
    if m is not None:
        want = {"n_atoms": cv["n_atoms"], "supercell": [1, 1, 1], "temperatures": [float(T)], "prod_ps": cv["prod_ps"],
                "equilib_ps": cv["equilib_ps"], "seed": cv["vseed_offset"] + seed, "fit_window_ps": [2.0, 50.0],
                "save_traj": True, "uma_model": "uma-s-1p1", "uma_inference_mode_requested": "turbo",
                "uma_inference_mode": "turbo", "label": label}
        for k, w in want.items():
            if not _same(m.get(k), w):
                inv.append(f"run_meta {k} {m.get(k)!r} ≠ 카드 {w!r}")
        bo = qrec.get("base_original")
        if not bo:
            inv.append("큐 로그에서 원래 BASE 를 못 읽었다 — run_meta v0_xyz 를 대조할 수 없다")
        elif m.get("v0_xyz") != f"{bo}/{sys_}/init/seed{seed}_final.xyz":
            inv.append(f"run_meta v0_xyz {m.get('v0_xyz')!r} ≠ '{bo}/{sys_}/init/seed{seed}_final.xyz' (원래 BASE 기준)")
    erp = rd / "ensemble_results.json"
    if erp.is_file():
        try:
            er = json.loads(erp.read_text(encoding="utf-8"))
        except ValueError:
            er = None
            inv.append("ensemble_results.json 을 못 읽었다")
        if isinstance(er, dict):
            want_er = {"uma_inference_mode": "turbo", "uma_task": "omat", "uma_model": "uma-s-1p1", "n_atoms": cv["n_atoms"],
                       "temperatures": [float(T)], "prod_ps": cv["prod_ps"], "equilib_ps": cv["equilib_ps"], "label": label}
            for k, w in want_er.items():
                if not _same(er.get(k), w):
                    inv.append(f"ensemble_results {k} {er.get(k)!r} ≠ {w!r}"
                               + (" — 끝 요약이 아니다 (드라이버가 끝까지 안 갔다)" if k not in er else ""))
    elif started:
        (inv if ended else inc).append("ensemble_results.json 없음")
    # ③ 입력 결속
    init = base / sys_ / "init" / f"seed{seed}_final.xyz"
    want_sha = cv["inputs_sha256"].get(f"{sys_}{seed}")
    symbols0 = cell_ref = pos_ref = None
    if not init.is_file() or not want_sha or _sha(init) != want_sha:
        inv.append(f"init 사본 {init.name} 이 없거나 sha256 ≠ 카드 입력 기록")
    elif started:
        try:
            a_in, a_cf = read(str(init)), read(str(rd / "d0.00_cfg0" / "config.xyz"))
            out["_input_atoms"] = a_in
            same_sym = a_in.get_chemical_symbols() == a_cf.get_chemical_symbols()
            dcell = float(np.abs(np.asarray(a_in.get_cell()) - np.asarray(a_cf.get_cell())).max())
            dpos = (float(_mic_disp(a_in.get_positions(), a_cf.get_positions(), np.asarray(a_in.get_cell())).max())
                    if same_sym else float("inf"))
            if not (same_sym and dcell <= BIND_TOL_A and dpos <= BIND_TOL_A):
                inv.append("드라이버가 쓴 시작 구조 (config.xyz) ≠ init 사본 (원소 순서 · 셀 · 좌표)")
            else:
                symbols0, cell_ref, pos_ref = a_cf.get_chemical_symbols(), np.asarray(a_cf.get_cell()), a_cf.get_positions()
        except Exception as e:
            inv.append(f"시작 구조 대조 실패 ({type(e).__name__}: {e})")
    # ④ 궤적 · ⑤ 산출물 (끝난 런만)
    out["trajectory"] = {}
    if not inc and symbols0 is not None:
        tp, _ti, data, tinfo = check_trajectory(tdir, cv["n_atoms"], symbols0, cv["prod_ps"], T, cv["equilib_ps"], cv["save_fs"],
                                                cv["dt_fs"], cv["caps"], cv["T_tol"], cell_ref=cell_ref, pos_ref=pos_ref,
                                                bind_max_A=cv["bind_max_A"], keep_PS=keep_PS)
        inv.extend(tp)                       # 러너가 끝났다는데 궤적이 모자라면 '덜 끝남' 이 아니라 어긋남이다
        out["_frames"], out["trajectory"] = data, tinfo
    if not inc and (tdir / "msd.json").is_file():
        inv.extend(check_msd(tdir, T, int(round(cv["prod_ps"] * 1000.0 / cv["save_fs"])), cv["save_fs"]))
    # ⑥ 비용 — 장부 → 러너 로그 시각 → 미확정
    h, src = _ledger_hours(base / "cost_ledger.tsv", sys_, T, seed)
    hl = (bk or {}).get("hours_log")
    if h is None:
        h, src = (hl, f"러너 로그 시각 (재구성 · {src})") if hl is not None else (None, f"비용 미확정 ({src} · 러너 끝 줄 시각 없음 · 파일 시각은 근거로 안 쓴다)")
    out.update(cost_h=h, cost_source=src, cost_h_from_log=hl)
    # ⑦ 보조 — 큐가 돈 worktree
    wc = worktree_code(worktree)
    for key, ck in (("md_driver", "md_driver_sha16"), ("md_runner", "md_runner_sha16")):
        got = (wc.get(key + "_sha256") or "")[:16] or None
        if got != cv[ck]:
            inv.append(f"{WT_FILES[key]} sha16 {got} ≠ 카드 {cv[ck]} (판독 시점 worktree)")
    out["worktree_code"] = wc
    out["status"] = "incomplete" if inc else ("invalid" if inv else "valid")
    out["reasons"] = inc + inv
    return out


# ───────────────────────── v2 런 (run_stage2_kgy_v2.sh · 실행 기록) ─────────────────────────
def phase_temps(cv, phase):
    """판독 갈래의 계획 온도 — ladder = 카드 사다리 · cond550 = 카드 conditional.T_K + 사다리 ('끝난 뒤 한 번 더')."""
    if phase == "ladder":
        return list(cv["temperatures"])
    if phase == "cond550":
        if not cv.get("cond"):
            raise Refused("⛔ 카드에 stage2.conditional (T_K · prod_ps) 이 없다 — cond550 판독을 할 수 없다")
        return [int(cv["cond"]["T_K"])] + list(cv["temperatures"])
    raise Refused(f"⛔ 모르는 판독 갈래 {phase!r} (ladder · cond550)")


def prod_for(cv, T):
    c = cv.get("cond")
    return float(c["prod_ps"]) if (c and int(T) == int(c["T_K"])) else float(cv["prod_ps"])


def v2_run_values(cv, T):
    """v2 큐 run_values 와 같은 꼴 — 실행 기록의 card_values 와 지금 카드를 맞춘다 (상한 · 한도 · 견적은 안 본다)."""
    c = cv.get("cond")
    return {"T_K": int(T), "block": "cond550" if (c and int(T) == int(c["T_K"])) else "ladder", "prod_ps": prod_for(cv, T),
            "equilib_ps": cv["equilib_ps"], "vseed_offset": cv["vseed_offset"], "save_fs": cv["save_fs"], "dt_fs": cv["dt_fs"],
            "n_atoms": cv["n_atoms"]}


def v2_driver_args(cv, base, s, sd, T):
    """v2 큐의 드라이버 명령 틀 (run_stage2_kgy_v2.sh argv_for 의 argv[2:]) — 값은 카드에서. 파이썬 · 드라이버 경로는 따로 본다."""
    g = lambda x: f"{float(x):g}"
    return ["--v0_xyz", f"{base}/{s}/init/seed{sd}_final.xyz", "--supercell", "1", "1", "1", "--label", f"li2s3_{s}_s{sd}_T{T}",
            "--out_root", f"{base}/{s}/seed{sd}/T{T}", "--disorder_levels", "0", "--n_configs", "1", "--temperatures", str(int(T)),
            "--equilib_ps", g(cv["equilib_ps"]), "--prod_ps", g(prod_for(cv, T)), "--timestep_fs", g(cv["dt_fs"]),
            "--save_fs", g(cv["save_fs"]), "--friction", "0.02", "--fit_window_ps", "2", "50", "--save_traj",
            "--seed", str(cv["vseed_offset"] + int(sd)), "--turbo", "--device", "cuda"]


def _load_json(p):
    try:
        return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _same_base(d, rb) -> bool:
    """결속 기록이 이 런의 BASE (실행 기록 base) 의 것인가 — v2 큐 base_matches 와 같은 뜻 (원래 BASE 문자열 또는 해석한 경로)."""
    if not rb:
        return False
    if d.get("base_original") == rb or d.get("base_now") == rb:
        return True
    try:
        return bool(d.get("base_now")) and pathlib.Path(d["base_now"]).resolve() == pathlib.Path(rb).resolve()
    except OSError:
        return False


def _v2_link_problems(link, want_kind, base, rb, cv, sys_, seed, T):
    """v2 실행 기록의 결속 기록을 판독 시점에 다시 본다 — 파일 · sha256 · 같은 BASE · 내용
    (cond550: 사다리 판독 · 두 계 최저 사다리 온도 측정 가능 · rerun: 보류 기록이 그 런을 invalid · incomplete 로)."""
    if not isinstance(link, dict) or link.get("kind") != want_kind or not link.get("path") or not link.get("sha256"):
        return [f"v2 실행 기록에 {want_kind} 결속 기록이 없다"]
    f = pathlib.Path(link["path"])
    if not f.is_file() and link.get("rel_to_base"):
        f = pathlib.Path(base) / link["rel_to_base"]          # 옮긴 BASE — 실행 때 BASE 아래였으면 지금 BASE 에서 찾는다
    if not f.is_file():
        return [f"결속 기록 {link['path']} 가 없다"]
    if _sha(f) != link["sha256"]:
        return ["결속 기록 sha256 ≠ 실행 기록 (결속 뒤 바뀌었다)"]
    d = _load_json(f)
    if not isinstance(d, dict):
        return ["결속 기록을 못 읽었다"]
    probs = [] if _same_base(d, rb) else ["결속 기록이 이 런의 BASE (실행 기록 base) 의 것이 아니다"]
    if want_kind == "readout":
        lo = min(cv["temperatures"])
        if d.get("kind") != "li2s3_stage2_readout/v2" or d.get("status") != "판독" or d.get("phase", "ladder") != "ladder":
            probs.append("결속 판독 기록이 사다리 판독 (li2s3_stage2_readout/v2 · 판독) 이 아니다")
        if d.get("cond550_eligible") is not True or not all((d.get("measurable") or {}).get(f"{s}_T{lo}") is True for s in cv["systems"]):
            probs.append(f"결속 판독 기록이 두 계 모두 {lo} K 측정 가능을 보이지 않는다")
        fixed = pathlib.Path(base) / OUT_DIRNAME / READOUT_NAME
        if link.get("rel_to_base") != f"{OUT_DIRNAME}/{READOUT_NAME}":
            probs.append(f"결속 판독 기록이 사다리 판독 고정 기록 ({OUT_DIRNAME}/{READOUT_NAME}) 이 아니다 (리뷰 EE P2-1)")
        elif not fixed.is_file() or _sha(fixed) != link["sha256"]:
            probs.append("결속 판독 기록 sha256 ≠ 지금 사다리 판독 고정 기록 (리뷰 EE P2-1)")
        return probs
    st = ((d.get("runs") or {}).get(f"{sys_}{seed}_T{T}") or {}).get("status")
    if d.get("kind") != "li2s3_stage2_readout_hold/v2" or d.get("status") != "판정 보류" or st not in ("invalid", "incomplete"):
        probs.append(f"결속 보류 기록이 이 런을 invalid · incomplete 로 적지 않았다 ({st!r})")
    return probs


def _payload_checks(base, sys_, seed, T, cv, rd, tdir, prod, v0_want, label, inc, inv, out, keep_PS, ended):
    """② 설정 · ③ 입력 결속 · ④ 궤적 · ⑤ 산출물 — v1 경로와 같은 검사 (v2 런용 · prod 와 원래 BASE 를 받는다)."""
    from ase.io import read
    started = rd.exists()
    m = _load_json(rd / "run_meta.json")
    if not isinstance(m, dict):
        m = None
        if started:
            inv.append("run_meta.json 없음 · 못 읽음")
    if m is not None:
        want = {"n_atoms": cv["n_atoms"], "supercell": [1, 1, 1], "temperatures": [float(T)], "prod_ps": prod,
                "equilib_ps": cv["equilib_ps"], "seed": cv["vseed_offset"] + seed, "fit_window_ps": [2.0, 50.0],
                "save_traj": True, "uma_model": "uma-s-1p1", "uma_inference_mode_requested": "turbo",
                "uma_inference_mode": "turbo", "label": label}
        for k, w in want.items():
            if not _same(m.get(k), w):
                inv.append(f"run_meta {k} {m.get(k)!r} ≠ 카드 {w!r}")
        if not v0_want:
            inv.append("원래 BASE 를 모른다 — run_meta v0_xyz 를 대조할 수 없다")
        elif m.get("v0_xyz") != v0_want:
            inv.append(f"run_meta v0_xyz {m.get('v0_xyz')!r} ≠ {v0_want!r} (원래 BASE 기준)")
    erp = rd / "ensemble_results.json"
    if erp.is_file():
        er = _load_json(erp)
        if not isinstance(er, dict):
            inv.append("ensemble_results.json 을 못 읽었다")
        else:
            want_er = {"uma_inference_mode": "turbo", "uma_task": "omat", "uma_model": "uma-s-1p1", "n_atoms": cv["n_atoms"],
                       "temperatures": [float(T)], "prod_ps": prod, "equilib_ps": cv["equilib_ps"], "label": label}
            for k, w in want_er.items():
                if not _same(er.get(k), w):
                    inv.append(f"ensemble_results {k} {er.get(k)!r} ≠ {w!r}" + (" — 끝 요약이 아니다 (드라이버가 끝까지 안 갔다)" if k not in er else ""))
    elif started:
        (inv if ended else inc).append("ensemble_results.json 없음")
    init = base / sys_ / "init" / f"seed{seed}_final.xyz"
    want_sha = cv["inputs_sha256"].get(f"{sys_}{seed}")
    symbols0 = cell_ref = pos_ref = None
    if not init.is_file() or not want_sha or _sha(init) != want_sha:
        inv.append(f"init 사본 {init.name} 이 없거나 sha256 ≠ 카드 입력 기록")
    elif started:
        try:
            a_in, a_cf = read(str(init)), read(str(rd / "d0.00_cfg0" / "config.xyz"))
            out["_input_atoms"] = a_in
            same_sym = a_in.get_chemical_symbols() == a_cf.get_chemical_symbols()
            dcell = float(np.abs(np.asarray(a_in.get_cell()) - np.asarray(a_cf.get_cell())).max())
            dpos = (float(_mic_disp(a_in.get_positions(), a_cf.get_positions(), np.asarray(a_in.get_cell())).max())
                    if same_sym else float("inf"))
            if not (same_sym and dcell <= BIND_TOL_A and dpos <= BIND_TOL_A):
                inv.append("드라이버가 쓴 시작 구조 (config.xyz) ≠ init 사본 (원소 순서 · 셀 · 좌표)")
            else:
                symbols0, cell_ref, pos_ref = a_cf.get_chemical_symbols(), np.asarray(a_cf.get_cell()), a_cf.get_positions()
        except Exception as e:
            inv.append(f"시작 구조 대조 실패 ({type(e).__name__}: {e})")
    out["trajectory"] = {}
    if not inc and symbols0 is not None:
        tp, _ti, data, tinfo = check_trajectory(tdir, cv["n_atoms"], symbols0, prod, T, cv["equilib_ps"], cv["save_fs"], cv["dt_fs"],
                                                cv["caps"], cv["T_tol"], cell_ref=cell_ref, pos_ref=pos_ref, bind_max_A=cv["bind_max_A"],
                                                keep_PS=keep_PS)
        inv.extend(tp)
        out["_frames"], out["trajectory"] = data, tinfo
    if not inc and (tdir / "msd.json").is_file():
        inv.extend(check_msd(tdir, T, int(round(prod * 1000.0 / cv["save_fs"])), cv["save_fs"]))


def _git_blob(repo, rev, rel):
    try:
        r = subprocess.run(["git", "-C", str(repo), "show", f"{rev}:{rel}"], capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout if r.returncode == 0 else None


def _v2_origin_problems(st, cv) -> list:
    """v2 런의 카드 · 원장 출처 (리뷰 EE P1-2) — 시작 기록이 저장소 카드 · 원장 · HEAD 와 같은 판이라고 적었고, 그 커밋 (V2_REPO 에서
    git show <repo_head>:<경로>) 의 카드 · 원장 sha256 = 시작 기록 · 그 커밋 원장에서 카드 결정 · queue_v2 결정 active. 못 찾음 = invalid."""
    probs = [f"v2 시작 기록 {k} 가 참이 아니다 ({what} · 리뷰 EE P1-2)" for k, what in (
        ("card_is_repo_card", "카드가 저장소의 그 파일이 아니었다"), ("decisions_is_repo", "결정 원장이 저장소의 그 파일이 아니었다"),
        ("repo_clean", "카드 · 원장 · 큐 · 드라이버가 HEAD 와 같지 않았다")) if st.get(k) is not True]
    head = str(st.get("repo_head") or "")
    if not re.fullmatch(r"[0-9a-f]{40}([0-9a-f]{24})?", head):
        return probs + ["v2 시작 기록에 repo HEAD (커밋) 가 없다"]
    cb, db_ = _git_blob(V2_REPO, head, CARD_REL), _git_blob(V2_REPO, head, DECISIONS_REL)
    if cb is None or db_ is None:
        return probs + [f"커밋 {head[:12]} 의 카드 · 원장을 저장소 {V2_REPO} 에서 못 찾는다 — '못 찾음' 은 '맞음' 이 아니다"]
    if hashlib.sha256(cb).hexdigest() != st.get("card_sha256"):
        probs.append(f"커밋 {head[:12]} 의 카드 sha256 ≠ 시작 기록 card_sha256 (그 커밋의 카드로 돈 런이 아니다)")
    if hashlib.sha256(db_).hexdigest() != st.get("decisions_sha256"):
        probs.append(f"커밋 {head[:12]} 의 결정 원장 sha256 ≠ 시작 기록 decisions_sha256")
    try:
        D = json.loads(db_.decode("utf-8"))
        L = D["decisions"] if isinstance(D, dict) else D
    except (ValueError, KeyError, UnicodeDecodeError):
        return probs + [f"커밋 {head[:12]} 의 결정 원장을 못 읽었다"]
    for did in (cv["decision"], cv.get("queue_v2_decision")):
        stt = next((e.get("decision_state") for e in L if isinstance(e, dict) and e.get("id") == did), None) if did else None
        if stt != "active":
            probs.append(f"커밋 {head[:12]} 의 원장에서 결정 {did} 가 active 가 아니다 ({stt!r})")
    return probs


def verify_run_v2(base, sys_, seed, T, cv, worktree, keep_PS=False) -> dict:
    """v2 큐 런 하나 — 실행 기록 (exec_v2_start · exec_v2_end) 으로 ① · ⑥ · ⑦ 을 결속하고 ②–⑤ 는 v1 과 같은 검사 (VERIFY_MAP)."""
    base = pathlib.Path(base)
    T, seed = int(T), int(seed)
    rd = base / sys_ / f"seed{seed}" / f"T{T}"
    tdir = rd / "d0.00_cfg0" / f"T{T}"
    label, prod = f"li2s3_{sys_}_s{seed}_T{T}", prod_for(cv, T)
    inc, inv = [], []
    out = {"system": sys_, "seed": seed, "T_K": T, "run_dir": str(rd), "queue_version": "v2", "runner_rc": None}
    st = _load_json(rd / V2_START)
    if not isinstance(st, dict):
        inv.append("v2 시작 기록을 못 읽었다")
        st = {}
    en = None
    if not (rd / V2_END).exists():
        inc.append("v2 끝 기록이 없다 — 끝나지 않았다 (또는 끊겼다)")
    else:
        en = _load_json(rd / V2_END)
        if not isinstance(en, dict):
            inv.append("v2 끝 기록을 못 읽었다")
            en = None
    # ① 실행 기록
    if st.get("kind") != "li2s3_stage2_exec_start/v2" or (st.get("system"), st.get("seed"), st.get("T_K")) != (sys_, seed, T):
        inv.append("v2 시작 기록의 꼴 · 런 (계 · 시드 · 온도) 이 이 폴더와 다르다")
    q16 = cv.get("queue_v2_sha16")
    if not q16:
        inv.append("카드에 stage2.queue_v2.sha16 이 없다 — v2 런을 결속할 수 없다")
    elif st.get("queue_v2_sha16") != q16:
        inv.append(f"v2 큐 sha16 {st.get('queue_v2_sha16')} ≠ 카드 {q16} (다른 큐 판으로 돌았다)")
    if st.get("driver_sha16") != cv["md_driver_sha16"]:
        inv.append(f"v2 실행 기록의 드라이버 sha16 {st.get('driver_sha16')} ≠ 카드 {cv['md_driver_sha16']} (다른 드라이버로 돌았다)")
    dz = st.get("decisions") if isinstance(st.get("decisions"), dict) else {}
    if dz.get(cv["decision"]) != "active" or not cv.get("queue_v2_decision") or dz.get(cv["queue_v2_decision"]) != "active":
        inv.append(f"v2 시작 기록의 결정 상태 {dz} — 카드 결정 · queue_v2 결정이 실행 때 active 가 아니었다")
    if st.get("test") is True:                            # 시험 런 (V2_TEST=1 · 환경변수 카드 · 원장) — 판독에 안 쓴다 (리뷰 EE P1-2)
        if not ALLOW_TEST_RUNS:
            inv.append("시험 런 (V2_TEST=1 · 시작 기록 test: true) — 판독에 안 쓴다 (저장소 카드 · 원장으로 돈 런만)")
    else:
        inv.extend(_v2_origin_problems(st, cv))
    rv = v2_run_values(cv, T)
    got = {k: (st.get("card_values") or {}).get(k) for k in rv}
    if not all(_same(got[k], rv[k]) for k in rv):
        inv.append(f"v2 실행 기록의 카드 값 {got} ≠ 지금 카드 {rv}")
    want_in = cv["inputs_sha256"].get(f"{sys_}{seed}")
    if not want_in or st.get("input_sha256") != want_in:
        inv.append("v2 실행 기록의 입력 sha256 (실행 직전 다시 해시한 값) ≠ 카드")
    rb = st.get("base")
    argv = st.get("argv") if isinstance(st.get("argv"), list) else []
    if not rb or len(argv) < 2 or argv[1] != st.get("driver_path") or argv[2:] != v2_driver_args(cv, rb, sys_, seed, T):
        inv.append("v2 실행 기록의 명령 인수 ≠ 카드에서 만든 v2 명령 틀")
    phase = st.get("phase")
    if phase == "cond550" and rv["block"] == "cond550":
        inv.extend(_v2_link_problems(st.get("link"), "readout", base, rb, cv, sys_, seed, T))
    elif phase == "rerun":
        inv.extend(_v2_link_problems(st.get("link"), "hold", base, rb, cv, sys_, seed, T))
    else:
        inv.append(f"v2 실행 기록 phase {phase!r} 가 이 온도 ({rv['block']}) 에 맞지 않는다")
    if en is not None:
        out["runner_rc"] = en.get("driver_rc")
        if en.get("kind") != "li2s3_stage2_exec_end/v2" or en.get("run_id") != st.get("run_id"):
            inv.append("v2 끝 기록이 이 시작 기록의 것이 아니다 (run_id)")
        if en.get("status") != "complete":
            inv.append(f"v2 끝 기록 상태 {en.get('status')!r} — {'; '.join(en.get('reasons') or [])[:160]}")
        if en.get("driver_rc") != 0:
            inv.append(f"드라이버 종료 코드 {en.get('driver_rc')} ≠ 0 (v2 실행 기록)")
        osha = en.get("outputs_sha256") or {}
        need = ["run_meta.json", "ensemble_results.json", "d0.00_cfg0/config.xyz"] + [
            f"d0.00_cfg0/T{T}/{x}" for x in ("traj.xyz", "msd.json", "aimd_results.json", "md.log")]
        changed = [r for r in need if not osha.get(r) or not (rd / r).is_file() or _sha(rd / r) != osha[r]]
        if changed:
            inv.append(f"v2 끝 기록 뒤 산출물이 바뀌었거나 없다 {changed}")
    ended = en is not None
    if rd.exists() and not (tdir / "msd.json").is_file():
        (inv if ended else inc).append("msd.json 없음" + (" — 끝 기록은 있는데" if ended else " (끝나지 않았다)"))
    # ② · ③ · ④ · ⑤ — v1 과 같은 검사 (원래 BASE = 실행 기록의 base · prod = 그 온도의 카드 값)
    _payload_checks(base, sys_, seed, T, cv, rd, tdir, prod, (f"{rb}/{sys_}/init/seed{seed}_final.xyz" if rb else None), label,
                    inc, inv, out, keep_PS, ended)
    # ⑥ 비용 — 끝 기록의 gpu_h (장부 행과 맞는지 함께 적는다)
    gh = (en or {}).get("gpu_h")
    ok_h = isinstance(gh, (int, float)) and not isinstance(gh, bool) and math.isfinite(float(gh)) and float(gh) >= 0
    try:
        led = (base / "cost_ledger.tsv").read_text(encoding="utf-8").splitlines()[1:]
    except OSError:
        led = []
    out["cost_h"] = float(gh) if ok_h else None
    out["cost_source"] = (("v2 실행 기록 (장부 행 일치)" if (en or {}).get("ledger_row") in led else "v2 실행 기록 (장부 행 없음 · 어긋남)")
                          if ok_h else "비용 미확정 (v2 끝 기록의 gpu_h 없음)")
    out["cost_h_from_log"] = None
    # ⑦ 보조 — 판독 시점 worktree 의 드라이버 · v2 큐 파일
    wc = worktree_code(worktree)
    got_d = (wc.get("md_driver_sha256") or "")[:16] or None
    if got_d != cv["md_driver_sha16"]:
        inv.append(f"{WT_FILES['md_driver']} sha16 {got_d} ≠ 카드 {cv['md_driver_sha16']} (판독 시점 worktree)")
    got_q = (wc.get("queue_v2_sha256") or "")[:16] or None
    if q16 and got_q != q16:
        inv.append(f"{QUEUE_V2_REL} sha16 {got_q} ≠ 카드 queue_v2.sha16 {q16} (판독 시점 worktree)")
    out["worktree_code"] = wc
    out.update(phase_v2=phase, link=st.get("link"), superseded=st.get("superseded"), run_id=st.get("run_id"),
               start_card_sha256=st.get("card_sha256"), start_utc=st.get("start_utc"), end_utc=(en or {}).get("end_utc"),
               test_run=st.get("test"), repo_head=st.get("repo_head"))
    out["status"] = "incomplete" if inc else ("invalid" if inv else "valid")
    out["reasons"] = inc + inv
    return out


def queue_lock_free(base) -> bool:
    """<BASE>/.stage2.lock 을 아무 큐 (v1 · v2) · 드라이버도 쥐고 있지 않은가 — 잠깐 쥐었다가 바로 놓는다."""
    import fcntl
    p = pathlib.Path(base) / ".stage2.lock"
    if not p.exists():
        return True
    fd = os.open(str(p), os.O_RDONLY)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(fd, fcntl.LOCK_UN)
        return True
    except BlockingIOError:
        return False
    finally:
        os.close(fd)


def v2_queue_records(base) -> dict:
    """v2 큐의 멈춤 · 사람 결정 (queue_v2_stops.jsonl) · 비용 정함 (cost_charges_v2.jsonl) — 판독 출력에 싣는다 (감사 · 보류 판단)."""
    out = {"stops": [], "acks": [], "charges": [], "problems": []}
    for name in ("queue_v2_stops.jsonl", "cost_charges_v2.jsonl"):
        p = pathlib.Path(base) / name
        if not p.exists():
            continue
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except OSError as e:
            out["problems"].append(f"{name} 을 못 읽었다 ({type(e).__name__})")
            continue
        for i, ln in enumerate(lines, 1):
            if not ln.strip():
                continue
            try:
                r = json.loads(ln)
            except ValueError:
                out["problems"].append(f"{name} {i} 번째 줄이 깨졌다")
                continue
            if name.startswith("cost"):
                out["charges"].append(r)
            elif isinstance(r, dict) and r.get("type") in ("stop", "ack"):
                out[r["type"] + "s"].append(r)
            else:
                out["problems"].append(f"{name} {i} 번째 줄이 멈춤 · 풂 기록이 아니다")
    real = [a for a in out["acks"] if str(a.get("by") or "").strip() and str(a.get("reason") or "").strip()]
    acked = {a.get("id") for a in real}                 # by · reason 없는 풂 줄은 풂이 아니다 (리뷰 EE P2-2)
    out["acks_without_by_reason"] = [a.get("id") for a in out["acks"] if a not in real]
    out["unacked"] = [s.get("id") for s in out["stops"] if s.get("id") not in acked]
    return out


def ready_state(base, qrec, runs):
    """판정 보류인가 — v1 런만이면 v1 판 그대로 (큐 로그 valid · 큐 끝 줄 · 모두 valid) · v2 런이 있으면 VERIFY_MAP 마지막 줄
    (모두 valid · v1 큐 로그에 문제 없음 · 큐 잠금 비어 있음 · 풀리지 않은 v2 멈춤 없음 — 멈추고 보고한 것을 사람이 풀기 전에는 읽지 않는다).
    둘 다: 사다리 블록 밖의 v1 호출이 있으면 보류 (리뷰 EE P2-6 — 런을 무효로 만들지 않고 따로 적는다)."""
    v2 = [k for k, v in runs.items() if v.get("queue_version") == "v2"]
    bad = [f"{s}{sd}_T{T}" for (s, sd, T), v in runs.items() if v["status"] != "valid"]
    other = qrec.get("other_invocations") or []
    other_why = [f"v1 큐 로그에 사다리 블록 밖의 v1 호출 {len(other)} 개 — 따로 보류 사유 (사람이 본다 · 리뷰 EE P2-6): {other[0][:120]}"] if other else []
    if not v2:
        info = {"mixed": False, "not_valid": bad, "queue_status": qrec["status"]}
        if other_why:
            info["why"] = other_why
        return (qrec["status"] == "valid" and not bad and not other), info
    why = list(other_why)
    if len(v2) < len(runs) and qrec.get("problems"):
        why.append("v1 큐 로그에 문제가 있다")
    if bad:
        why.append(f"valid 아닌 런 {len(bad)} 개")
    lock_free = queue_lock_free(base)
    if not lock_free:
        why.append("큐 잠금이 쥐어져 있다 — 큐 · 드라이버가 돌고 있다")
    qr = v2_queue_records(base)
    if qr["unacked"]:
        why.append(f"풀리지 않은 v2 멈춤 {len(qr['unacked'])} 개 {qr['unacked'][:5]} — 사람 결정 (ACK_STOP · ACK_BY · ACK_REASON) 전에는 판독하지 않는다")
    if qr["problems"]:
        why.append("v2 큐 기록 (멈춤 · 비용) 을 못 읽었다 — " + " · ".join(qr["problems"][:3]))
    return (not why), {"mixed": True, "not_valid": bad, "queue_status": qrec["status"], "lock_free": lock_free, "why": why,
                       "v2_runs": [f"{s}{sd}_T{T}" for (s, sd, T) in v2], "v2_queue_records": qr}


def q2_decision_gate(cv, decisions, runs):
    """v2 런이 하나라도 있으면 카드 queue_v2 결정이 지금도 active 여야 판독한다 (v1 런만이면 보지 않는다 — v1 판 그대로)."""
    if not any(v.get("queue_version") == "v2" for v in runs.values()):
        return None
    did = cv.get("queue_v2_decision")
    stt = decision_states(decisions, ids=(did,)).get(did) if did else None
    if stt != "active":
        raise Refused(f"⛔ v2 런이 있는데 카드 queue_v2 결정 {did!r} 이 active 가 아니다 ({stt!r}) — 판독하지 않는다")
    return {did: stt}


def verify_all(base, cv, worktree, keep_PS=False, phase="ladder"):
    base = pathlib.Path(base)
    qrec = queue_record(base, cv)
    runs = {}
    temps = phase_temps(cv, phase)
    for s in cv["systems"]:
        blocks = runner_blocks(base / s / "queue_kgy.log")
        for sd in cv["seeds"]:
            for T in temps:
                runs[(s, sd, T)] = verify_run(base, s, sd, T, cv, worktree, qrec=qrec, blocks=blocks, keep_PS=keep_PS)
    return qrec, runs


def _public(v) -> dict:
    return {k: x for k, x in v.items() if not k.startswith("_")}


# ───────────────────────── 기록 ⓐ–ⓒ ─────────────────────────
def records_abc(data, a_input, mq, ss_cut=None):
    """기록 ⓐ–ⓒ (판정에 안 씀) — data = {P: [프레임별 P 좌표], S: [...], cell}. P 는 전역 원자 번호로 적는다."""
    import quench_ss_event as Q
    ss_cut = Q.SS_CUT if ss_cut is None else float(ss_cut)
    P, S, cell = data["P"], data["S"], np.asarray(data["cell"])
    rps = mq.R_PS
    sym = np.asarray(a_input.get_chemical_symbols())
    gP = [int(x) for x in np.where(sym == "P")[0]]

    def coord(Pp, Sp):
        return (mq.mic_dists(Pp, Sp, cell) <= rps).sum(axis=1)

    def owners(Pp, Sp):
        D = mq.mic_dists(Pp, Sp, cell)
        return [tuple(np.where(D[:, j] <= rps)[0]) for j in range(D.shape[1])]

    def ss_pairs(Sp):
        D = mq.mic_dists(Sp, Sp, cell)
        iu = np.triu_indices(len(Sp), 1)
        return {(int(i), int(j)) for i, j in zip(*iu) if D[i, j] < ss_cut}

    pairs0 = sorted(ss_pairs(S[0]))
    pa = []
    for i, j in pairs0:
        d = np.array([float(_mic_disp(S[k][i:i + 1], S[k][j:j + 1], cell)[0]) for k in range(len(S))])
        on = d < ss_cut
        pa.append({"S_pair": [i, j], "d0_A": float(d[0]), "d_min_A": float(d.min()), "d_median_A": float(np.median(d)),
                   "d_max_A": float(d.max()), "frac_frames_kept": float(on.mean()), "kept_last": bool(on[-1]),
                   "n_break": int(np.sum(on[:-1] & ~on[1:])), "n_reform": int(np.sum(~on[:-1] & on[1:]))})
    cs = np.array([coord(P[k], S[k]) for k in range(len(P))])
    trans, perP = {}, {}
    for p in range(cs.shape[1]):
        col, tp = cs[:, p], {}
        for a0, a1 in zip(col[:-1], col[1:]):
            if a0 != a1:
                key = f"{int(a0)}→{int(a1)}"
                tp[key] = tp.get(key, 0) + 1
                trans[key] = trans.get(key, 0) + 1
        perP[str(gP[p])] = {"first": int(col[0]), "last": int(col[-1]), "transitions": tp}
    Pin, Sin = a_input.get_positions()[sym == "P"], a_input.get_positions()[sym == "S"]
    hist = lambda c: {int(k): int(v) for k, v in zip(*np.unique(c, return_counts=True))}
    c_in = coord(Pin, Sin)
    o_in, o_f0 = owners(Pin, Sin), owners(P[0], S[0])
    ss_in, ss_f0 = ss_pairs(Sin), set(pairs0)
    return {"ⓐ_first_frame_SS_pairs": pa,
            "ⓑ_P_coordination_transitions": trans,
            "ⓑ_per_P": perP,
            "ⓑ_P_coord_hist_first_last": {"first": hist(cs[0]), "last": hist(cs[-1])},
            "ⓒ_input_vs_first_frame": {"P_coord_hist_input": hist(c_in), "P_coord_hist_first": hist(cs[0]),
                                       "input_not4_P": [gP[p] for p in range(len(c_in)) if c_in[p] != 4],
                                       "P_coord_changed": [{"P": gP[p], "input": int(c_in[p]), "first": int(cs[0][p])}
                                                           for p in range(len(c_in)) if c_in[p] != cs[0][p]],
                                       "n_S_owner_changed": sum(1 for a, b in zip(o_in, o_f0) if set(a) != set(b)),
                                       "SS_pairs_input": len(ss_in), "SS_pairs_first": len(ss_f0),
                                       "SS_kept": len(ss_in & ss_f0), "SS_lost": len(ss_in - ss_f0), "SS_new": len(ss_f0 - ss_in)},
            "⚠": "기록만 — 판정에 안 씀 (카드 개정 DZ ⓐ–ⓒ) · 거리 컷 판독 (결합 차수 안 봄) · P 번호는 전역 원자 번호"}


def _rec_summary(rec):
    if not isinstance(rec, dict) or "ⓐ_first_frame_SS_pairs" not in rec:
        return None
    pa, perP, c = rec["ⓐ_first_frame_SS_pairs"], rec["ⓑ_per_P"], rec["ⓒ_input_vs_first_frame"]
    return {"ⓐ_n_pairs_first": len(pa), "ⓐ_n_kept_last": sum(1 for x in pa if x["kept_last"]),
            "ⓐ_min_frac_kept": min((x["frac_frames_kept"] for x in pa), default=None),
            "ⓑ_n_P_with_transitions": sum(1 for v in perP.values() if v["transitions"]),
            "ⓑ_input_not4_P_transitions": {str(p): (perP.get(str(p)) or {}).get("transitions") for p in c["input_not4_P"]},
            "ⓒ_n_P_coord_changed": len(c["P_coord_changed"]), "ⓒ_SS_lost": c["SS_lost"], "ⓒ_SS_new": c["SS_new"],
            "ⓒ_n_S_owner_changed": c["n_S_owner_changed"]}


def _row(G, rec):
    sk = G.skeleton_gate(rec)
    c2 = rec.get("C2") or {}
    ok = G.run_pass(rec)
    return {"C1_pass": rec.get("C1_pass"), "C1_msd_at_50_mto_A2": rec.get("C1_msd_at_50_mto_A2"), "beta_MTO": rec.get("beta_MTO"),
            "C2_final": c2.get("final_verdict"), "n_sigma_end": c2.get("n_sigma_end_signed"), "n_sigma_prev": c2.get("n_sigma_prev_signed"),
            "b_end": c2.get("b_end"), "b_prev": c2.get("b_prev"), "counts_in_N": ok, "skeleton": sk,
            "in_R_set": bool(ok and sk["pass"]), "error": rec.get("error")}


def _exclusion(row):
    if row["measurable"]:
        return None
    if row.get("error"):
        return "판독 오류"
    if not row["C1_pass"]:
        return "C1 미통과"
    if row["C2_final"] != "통과":
        return f"C2 {row['C2_final']}"
    return "골격 못 잼" if (row.get("skeleton") or {}).get("pass") is None else "골격 이동"


def layers(cv, rows, temps=None) -> dict:
    """세 층 수 — 카드 '입력_2026_11_10.시드' 기록에서 센다 (판정 파일을 다시 읽지 않는다). temps = 판독 갈래의 온도 (기본 사다리)."""
    temps = cv["temperatures"] if temps is None else temps
    gen = sorted(cv["defects"])
    incl, excl = [], {}
    for k in gen:
        d = cv["defects"][k]
        v = d.get("li2s2_판정") or ""
        ok_v = v == "pass" or v.startswith("fail — PS₄ 보존율")
        dm = d.get("최단_원자간_P_S_제외_A")
        ok_d = dm is not None and float(dm) > cv["inclusion_min_pair"]
        if ok_v and ok_d:
            incl.append(k)
        else:
            excl[k] = ("판정이 pass 도 PS₄ 한 줄 fail 도 아니다" if not ok_v else "") + (
                f" 최단 원자간 (P–S 제외) {dm} ≤ {cv['inclusion_min_pair']:g} Å" if not ok_d else "")
    stage2 = [f"{s}{sd}" for s in cv["systems"] for sd in cv["seeds"]]
    per_T = {}
    for s in cv["systems"]:
        for T in temps:
            rr = [r for r in rows if r["system"] == s and r["T_K"] == T]
            ex = {}
            for r in rr:
                if not r["measurable"]:
                    ex[r["exclusion"]] = ex.get(r["exclusion"], 0) + 1
            per_T[f"{s}_T{T}"] = {"n_시드": len(rr), "측정가능": [f"{s}{r['seed']}" for r in rr if r["measurable"]], "제외_사유": ex}
    return {"생성_후보군": {"n": len(gen), "시드": gen},
            "포함_가능군": {"n": len(incl), "시드": incl, "제외": excl,
                        "규칙": f"li2s2 판정 pass 또는 PS₄ 보존율 한 줄 fail · 최단 원자간 (P–S 제외) > {cv['inclusion_min_pair']:g} Å (카드 기록)"},
            "2단계_시드": stage2, "2단계_시드_중_포함_가능군_밖": [x for x in stage2 if x not in incl],
            "최종_측정가능_온도별": per_T}


# ───────────────────────── 판독 허가 · 문지기 ─────────────────────────
def permit_problems(cv, prov, repo=REPO) -> list:
    """판독 허가 키 — 근거 · by · EB 회신 파일 · 대조 잡 출력 (sha256 · same True · 깨끗한 트리 · 같은 도구 sha16)."""
    p = cv.get("read_permit")
    if not isinstance(p, dict):
        return [f"카드에 '{READ_PERMIT_KEY}' 가 없다 — 2 단계 판독 보류 중"]
    repo = pathlib.Path(repo)
    probs = [f"'{k}' 가 비었다" for k in ("근거", "by") if not p.get(k)]
    if ENDLINE_ACK_KEY in p:                      # 카드 개정 4 — 인정은 필드 여섯이 다 차 있어야
        a_ = p.get(ENDLINE_ACK_KEY)
        miss = [k for k in ENDLINE_ACK_FIELDS if not (isinstance(a_, dict) and str(a_.get(k) or "").strip())]
        if miss:
            probs.append(f"'{ENDLINE_ACK_KEY}' 의 {miss} 가 비었다 (카드 개정 4)")
    eb = p.get("EB_회신")
    if not eb or not str(eb).startswith("kb/reviews/") or not (repo / str(eb)).is_file():
        probs.append(f"'EB_회신' {eb!r} 이 kb/reviews/ 아래 있는 파일이 아니다")
    cpath, csha = p.get("대조_잡_출력"), p.get("대조_잡_sha256")
    if not cpath or not csha:
        probs.append("'대조_잡_출력' · '대조_잡_sha256' 이 없다")
        return probs
    f = pathlib.Path(str(cpath)).expanduser()
    f = f if f.is_absolute() else repo / f
    if not f.is_file():
        probs.append(f"대조 잡 출력 {f} 가 없다")
        return probs
    if _sha(f) != csha:
        probs.append("대조 잡 출력 sha256 ≠ 허가 기록")
        return probs
    try:
        cj = json.loads(f.read_text(encoding="utf-8"))
    except ValueError:
        cj = None
    if not isinstance(cj, dict) or cj.get("kind") != CONTROL_KIND:
        probs.append(f"대조 잡 출력의 kind 가 {CONTROL_KIND} 가 아니다")
        return probs
    if cj.get("same") is not True:
        probs.append(f"대조 잡 same = {cj.get('same')!r} (True 여야)")
    cp = cj.get("provenance") or {}
    if cp.get("tree_clean") is not True:
        probs.append("대조 잡을 깨끗한 작업 트리에서 내지 않았다")
    if cp.get("tool_sha16") != prov.get("tool_sha16"):
        probs.append("대조 잡을 낸 도구 판 (sha16) ≠ 지금 판 — 도구를 바꿨으면 대조 잡을 다시")
    return probs


def _gate(base, card, decisions, require_permit, prov, out_name, permit_repo=REPO):
    st = decision_states(decisions)
    if any(v != "active" for v in st.values()):
        raise Refused(f"⛔ 결정이 active 가 아니다 {st} — 판독하지 않는다")
    cv = card_values(card)
    prov = provenance() if prov is None else prov
    if require_permit:
        pp = permit_problems(cv, prov, repo=permit_repo)
        if pp:
            raise Refused(f"⛔ 판독 허가 '{READ_PERMIT_KEY}' 가 조건을 못 채웠다 — " + " · ".join(pp) + " (판독 보류 · 카드 개정 DZ · 리뷰 EB)")
    pmt = cv.get("read_permit") if isinstance(cv.get("read_permit"), dict) else {}
    if ENDLINE_ACK_KEY in pmt:                    # 카드 개정 4 — 인정의 결정이 지금 원장에서 active 여야
        a_ = pmt.get(ENDLINE_ACK_KEY)
        did = a_.get("결정") if isinstance(a_, dict) else None
        ds = decision_states(decisions, ids=(did,)).get(did) if isinstance(did, str) and did.strip() else None
        if ds != "active":
            raise Refused(f"⛔ 판독 허가의 '{ENDLINE_ACK_KEY}' 결정 {did!r} 이 active 가 아니다 ({ds!r}) — 판독하지 않는다 (카드 개정 4)")
        st = dict(st, **{did: ds})
    if not prov.get("tree_clean"):
        raise Refused(f"⛔ 도구 작업 트리가 깨끗하지 않다 {(prov.get('dirty_tracked') or [])[:5]} — 커밋한 판으로만 판독한다")
    od = pathlib.Path(base) / OUT_DIRNAME
    outp = od / out_name
    if outp.exists():
        raise Refused(f"⛔ {outp} 가 이미 있다 — 판독은 한 번 (덮지 않는다)")
    return cv, prov, st, od, outp


def _phase_of(phase):
    if phase not in OUT_NAMES:
        raise Refused(f"⛔ 모르는 판독 갈래 {phase!r} — {sorted(OUT_NAMES)}")
    return phase


def _cond550_gate(od):
    """cond550 판독 · 압력 — 사다리 판독 고정 기록 (<BASE>/readout_stage2/readout_stage2.json) 이 판독 · cond550 자격 True 일 때만
    ('16 런 판독 한 번 → 600 K 두 계 측정 가능이면 cond550 → 끝난 뒤 한 번 더' — 카드 읽는 시점)."""
    p = pathlib.Path(od) / READOUT_NAME
    d = _load_json(p)
    if not isinstance(d, dict) or d.get("kind") != "li2s3_stage2_readout/v2" or d.get("status") != "판독" \
            or d.get("phase", "ladder") != "ladder" or d.get("cond550_eligible") is not True:
        raise Refused(f"⛔ cond550 판독은 사다리 판독 고정 기록 {p} 이 판독 · cond550 자격 True 일 때만 — 없거나 자격이 없다")
    return {"path": str(p), "sha256": _sha(p), "W": d.get("W"), "utc": (d.get("provenance") or {}).get("utc"), "_record": d}


def _cond550_freeze(lad, base, cv, prov):
    """cond550 판독의 동결 (리뷰 EE P1-1) — 사다리 판독 고정 기록과 같은 사다리 런 (런별 지문) · 같은 판독 도구 sha16 · 같은 카드
    기계_판독_값 일 때만. 하나라도 다르면 거부 (새 개정 · 사용자 결정) — 사다리 판독 뒤에 바뀐 런 · 규칙 · 도구는 cond550 갈래에 안 들어간다."""
    probs = []
    if (lad.get("provenance") or {}).get("tool_sha16") != prov.get("tool_sha16"):
        probs.append("판독 도구 sha16 ≠ 사다리 판독 때")
    if lad.get("rules_sha256") != cv["rules_sha256"]:
        probs.append("카드 기계_판독_값 해시 ≠ 사다리 판독 때 (기록에 없으면 고친 도구로 낸 사다리 판독이 아니다)")
    want = {f"{r.get('system')}{r.get('seed')}_T{r.get('T_K')}": ((r.get("fingerprint") or {}).get("files"), r.get("T_K"))
            for r in (lad.get("rows") or [])}
    keys = {f"{s}{sd}_T{T}" for s in cv["systems"] for sd in cv["seeds"] for T in cv["temperatures"]}
    if set(want) != keys:
        probs.append(f"사다리 판독 행의 런 {sorted(want)} ≠ 카드 사다리 런 {sorted(keys)}")
    changed = []
    for k in sorted(keys & set(want)):
        fp, T = want[k]
        m = re.fullmatch(r"([A-Za-z]+)(\d+)_T(\d+)", k)
        if not isinstance(fp, dict) or run_fingerprint(pathlib.Path(base) / m.group(1) / f"seed{m.group(2)}" / f"T{m.group(3)}", T) != fp:
            changed.append(k)
    if changed:
        probs.append(f"사다리 런 지문이 사다리 판독 때와 다르다 {changed[:8]} (다시 굴렸거나 바뀐 런)")
    if probs:
        raise Refused("⛔ cond550 판독을 하지 않는다 — " + " · ".join(probs) + " (카드: cond550 판독은 사다리 판독과 같은 런 · 도구 · 규칙으로만 · "
                      "새 개정 · 사용자 결정)")


def _common(base, cv, prov, st, qrec, worktree, phase="ladder", ready=None):
    return {"card_sha256": cv["card_sha256"], "card": cv["card_path"], "rules_sha256": cv["rules_sha256"], "decisions": st,
            "provenance": prov, "base_now": str(pathlib.Path(base).resolve()), "base_original": qrec.get("base_original"),
            "queue": {k: qrec.get(k) for k in ("status", "complete", "start", "gatekeep", "versions", "repo_head", "problems",
                                               "other_invocations", "end_line")},
            "worktree_code": worktree_code(worktree), "phase": phase, "ready": ready, "verify_map": VERIFY_MAP}


def _hold(kind, od, common, qrec, runs):
    """판정 보류 기록 — 런마다 그때 본 지문 (산출물 7 + v2 시작 · 끝 기록 · 없으면 null) 을 싣는다: PHASE=rerun 은 지금 지문 = 이 지문일 때만
    그 런을 다시 돈다 (리뷰 EE P1-1)."""
    hold = {"kind": kind, "status": "판정 보류", **common, "queue_status": qrec.get("status"), "queue_problems": qrec.get("problems"),
            "hold_reasons": ((common.get("ready") or {}).get("why") or []),
            "runs": {f"{s}{sd}_T{T}": {"status": v["status"], "reasons": v["reasons"], "fingerprint": run_fingerprint(v["run_dir"], T)}
                     for (s, sd, T), v in runs.items()},
            "n_runs_not_valid": sum(1 for v in runs.values() if v["status"] != "valid"),
            "⚠": "W · 갈래 · cond550 · 압력을 내지 않는다 — 검증 실패 · 미완은 수송 게이트 미통과가 아니다 (판정 보류 · 처리는 카드 · 사용자 결정)"}
    stamp = common["provenance"]["utc"].replace(":", "").replace("-", "")
    stem = kind.split("/")[0]
    p, i = od / f"hold_{stem}_{stamp}.json", 1
    while p.exists():
        p, i = od / f"hold_{stem}_{stamp}_{i}.json", i + 1
    _write_new(p, hold)
    hold["hold_path"] = str(p)
    return hold


# ───────────────────────── 판독 ─────────────────────────
def readout(base, worktree, card=CARD, decisions=DECISIONS, n_boot=N_BOOT, read_run=None, require_permit=True, prov=None,
            permit_repo=REPO, phase="ladder"):
    import glass_v2_readout as G
    import quench_ss_event as Q
    base = pathlib.Path(base)
    phase = _phase_of(phase)
    cv, prov, st, od, outp = _gate(base, card, decisions, require_permit, prov, OUT_NAMES[phase][0], permit_repo)
    phase_temps(cv, phase)                                   # cond550 인데 카드에 conditional 이 없으면 먼저 거부
    ladder_ref = _cond550_gate(od) if phase == "cond550" else None
    if ladder_ref:
        _cond550_freeze(ladder_ref.pop("_record"), base, cv, prov)
    qrec, runs = verify_all(base, cv, worktree, keep_PS=True, phase=phase)
    q2st = q2_decision_gate(cv, decisions, runs)
    ok, rinfo = ready_state(base, qrec, runs)
    common = _common(base, cv, prov, st, qrec, worktree, phase=phase, ready=rinfo)
    if ladder_ref:
        common["ladder_readout"] = ladder_ref
    if q2st:
        common["decisions_queue_v2"] = q2st
    if not ok:
        if not queue_lock_free(base):
            raise Refused("⛔ 큐 잠금이 쥐어져 있다 (큐 · 드라이버가 돈다) — 판정 보류 기록을 쓰지 않는다 · 상태 보기는 verify 로만 (리뷰 EE P1-1)")
        return _hold("li2s3_stage2_readout_hold/v2", od, common, qrec, runs)
    rr = read_run or G.read_run
    mq = Q._load_mq(str(HERE))
    rows = []
    for (s, sd, T), v in runs.items():
        msd = pathlib.Path(v["run_dir"]) / "d0.00_cfg0" / f"T{int(T)}" / "msd.json"
        rec = rr(msd, n_boot=n_boot, framework=True, mq=mq)
        rec.pop("_D_slope", None)
        row = {"system": s, "seed": sd, "T_K": T,
               "verify": {k: v.get(k) for k in ("status", "reasons", "runner_rc", "cost_h", "cost_source", "trajectory", "queue_version")},
               "fingerprint": {"queue_version": v.get("queue_version"), "run_id": v.get("run_id"),
                               "runner_start": (v.get("runner") or {}).get("start_ts"), "files": run_fingerprint(v["run_dir"], T)}}
        row.update(_row(G, rec))
        row["measurable"] = bool(row["in_R_set"])
        row["exclusion"] = _exclusion(row)
        row["records"] = records_abc(v["_frames"], v["_input_atoms"], mq) if v.get("_frames") else {"status": "자료 없음"}
        rows.append(row)
    systems, temps = cv["systems"], phase_temps(cv, phase)
    meas = {(s, T): all(r["measurable"] for r in rows if r["system"] == s and r["T_K"] == T) for s in systems for T in temps}
    W = [T for T in temps if all(meas[(s, T)] for s in systems)]
    cond550 = (600 in temps) and all(meas[(s, 600)] for s in systems)
    base_branch = ("3 단계 후보 = W 의 가장 낮은 셋 → 사용자 결정 (상한 포함)" if len(W) >= 3 else
                   "Ea 차 없음 · R 만 그 온도에서 (축소 3 단계 · 사용자 결정)" if W else "닫는다 (S2 허용 문구 + 구조군 문구)")
    provisional = bool(cond550 and phase == "ladder")          # cond550 판독 ('끝난 뒤 한 번 더') 이 갈래를 확정한다
    branch = f"잠정 — cond550 판독 전 · {base_branch}" if provisional else base_branch
    table = []
    for s in systems:
        for sd in cv["seeds"]:
            per_T = {}
            for r in rows:
                if r["system"] == s and r["seed"] == sd:
                    sk = r.get("skeleton") or {}
                    per_T[str(r["T_K"])] = {"C1_pass": r["C1_pass"], "C2_final": r["C2_final"], "skeleton_pass": sk.get("pass"),
                                            "skeleton_criteria": sk.get("criteria"), "skeleton_values": sk.get("values"),
                                            "measurable": r["measurable"], "exclusion": r["exclusion"],
                                            "records_summary": _rec_summary(r.get("records"))}
            table.append({"system": s, "seed": sd, "defect_label": cv["defects"].get(f"{s}{sd}"), "label_source": DEFECT_LABEL_SOURCE,
                          "per_T": per_T})
    cost = [r["verify"]["cost_h"] for r in rows]
    out = {"kind": "li2s3_stage2_readout/v2", "status": "판독", **common, "n_boot": n_boot, "rows": rows,
           "measurable": {f"{s}_T{T}": meas[(s, T)] for (s, T) in meas}, "W": W, "branch": branch, "branch_provisional": provisional,
           "cond550_eligible": cond550, "seed_table": table, "layers": layers(cv, rows, temps),
           "cost_h_total": (sum(cost) if all(c is not None for c in cost) else None),
           "ledger_total_h": ledger_total(base),
           "cost_sources": sorted({r["verify"]["cost_source"] for r in rows}),
           "cost_note": "cost_h_total = 읽은 런만 (None = 비용 미확정 — 0 으로 세지 않는다) · 캠페인 비용은 ledger_total_h (장부 전체 · 옮긴 런 · "
                        "정한 비용 포함) 로만 적는다 (리뷰 EE P2-5)",
           "⚠": "D · σ 값 없음 · 기록 ⓐ–ⓒ 는 판정에 안 씀 · 골격은 생산 첫 프레임 대비 (카드 개정 DZ) · 사다리 판독에서 cond550 자격이면 "
                "갈래는 잠정 (cond550 판독이 확정)"}
    _write_new(outp, out)
    out["out_path"] = str(outp)
    return out


# ───────────────────────── 압력 ─────────────────────────
def run_pressure(tdir, T_set, n_atoms, prod_ps, save_fs, calc, ev_a3_to_gpa, every_ps=PRESSURE_EVERY_PS):
    """생산 프레임 k = j·step − 1 (t = (k+1)·save = j·every ps · j = 1 … prod/every) 의 UMA 단일점 virial 압력 +
    운동 항 N k_B T_set / V (이상기체 · 목표 온도) → 런 기록."""
    import time
    from ase.io import iread
    tdir = pathlib.Path(tdir)
    step = int(round(every_ps * 1000.0 / save_fs))
    n_exp = int(round(prod_ps * 1000.0 / save_fs))
    n_pick = int(round(prod_ps / every_ps))
    want = {j * step - 1 for j in range(1, n_pick + 1)}
    t0, P, n = time.time(), [], 0
    V = None
    for k, a in enumerate(iread(str(tdir / "traj.xyz"), index=":", format="extxyz")):
        n += 1
        if k not in want:
            continue
        a = a.copy()
        a.calc = calc
        sig = np.asarray(a.get_stress(voigt=False), float)
        V = float(a.get_volume())
        pv = float(-np.trace(sig) / 3.0 * ev_a3_to_gpa)
        pk = float(n_atoms * KB_EV * float(T_set) / V * ev_a3_to_gpa)
        P.append({"k": k, "t_ps": round((k + 1) * save_fs / 1000.0, 9), "P_virial_GPa": pv, "P_kin_GPa": pk, "P_GPa": pv + pk})
    if n != n_exp:
        raise Refused(f"⛔ {tdir}: 궤적 프레임 {n} ≠ 계획 {n_exp} — 검증 뒤 파일이 바뀌었다 (압력을 내지 않는다)")
    vals = [x["P_GPa"] for x in P]
    if len(vals) != n_pick or not all(math.isfinite(v) for v in vals):
        return {"status": "압력 못 냄 (프레임 수 · 비유한)", "n": len(vals)}
    bm = [float(np.mean(b)) for b in np.array_split(np.asarray(vals), 10) if len(b)]
    return {"status": "ok", "n": len(vals), "mean_GPa": float(np.mean(vals)),
            "sd_GPa": (float(np.std(vals, ddof=1)) if len(vals) > 1 else None),
            "se_block10_GPa": (float(np.std(bm, ddof=1) / math.sqrt(len(bm))) if len(bm) > 1 else None),
            "V_A3": V, "P_kin_GPa": P[0]["P_kin_GPa"], "every_ps": every_ps,
            "frame_rule": f"k = j·{step} − 1 · t = (k+1)·{save_fs:g} fs (j = 1 … {n_pick})", "wall_s": round(time.time() - t0, 2),
            "frames": P}


def pressure(base, worktree, card=CARD, decisions=DECISIONS, calc_factory=None, device="cuda", require_permit=True, prov=None,
             permit_repo=REPO, phase="ladder"):
    """2 단계 런마다 MD 압력 (스냅숏 재계산 · 판정에 안 씀 · 두 계 ⟨P⟩ 차 > 1 GPa 는 경고 하나 더 — li2s-2 카드 §1b · §3).
    cond550 갈래는 런별 기록을 따로 (pressure_runs_cond550/) 쓴다 — 사다리 기록과 카드 판이 달라도 섞이지 않게."""
    import quench_ss_event as Q
    base = pathlib.Path(base)
    phase = _phase_of(phase)
    cv, prov, st, od, outp = _gate(base, card, decisions, require_permit, prov, OUT_NAMES[phase][1], permit_repo)
    phase_temps(cv, phase)
    ladder_ref = _cond550_gate(od) if phase == "cond550" else None
    if ladder_ref:
        _cond550_freeze(ladder_ref.pop("_record"), base, cv, prov)
    qrec, runs = verify_all(base, cv, worktree, phase=phase)
    q2st = q2_decision_gate(cv, decisions, runs)
    ok, rinfo = ready_state(base, qrec, runs)
    common = _common(base, cv, prov, st, qrec, worktree, phase=phase, ready=rinfo)
    if ladder_ref:
        common["ladder_readout"] = ladder_ref
    if q2st:
        common["decisions_queue_v2"] = q2st
    if not ok:
        if not queue_lock_free(base):
            raise Refused("⛔ 큐 잠금이 쥐어져 있다 (큐 · 드라이버가 돈다) — 판정 보류 기록을 쓰지 않는다 · 상태 보기는 verify 로만 (리뷰 EE P1-1)")
        return _hold("li2s3_stage2_pressure_hold/v2", od, common, qrec, runs)
    mq = Q._load_mq(str(HERE))
    if calc_factory is None:
        def calc_factory(system, _dev=device):
            c = mq.make_calc(_dev, turbo=True)
            if getattr(c, "_mq_mode", "default") != "turbo":
                raise Refused("⛔ turbo 를 못 켰다 — MD 와 같은 추론 모드가 아니다 (압력을 내지 않는다)")
            return c
    rdir = od / (PRESSURE_RUNS if phase == "ladder" else f"{PRESSURE_RUNS}_{phase}")
    temps = phase_temps(cv, phase)
    res = {}
    for s in cv["systems"]:
        calc = None                                      # 계마다 새 계산기 — turbo 는 조성이 고정된 모델이다 (merge_mole)
        for sd in cv["seeds"]:
            for T in temps:
                key = f"{s}{sd}_T{T}"
                tdir = base / s / f"seed{sd}" / f"T{T}" / "d0.00_cfg0" / f"T{T}"
                tsha = _sha(tdir / "traj.xyz")
                f = rdir / f"{key}.json"
                if f.exists():
                    try:
                        old = json.loads(f.read_text(encoding="utf-8"))
                    except ValueError:
                        old = {}
                    if (old.get("status") == "ok" and old.get("traj_sha256") == tsha and old.get("tool_sha16") == prov["tool_sha16"]
                            and old.get("card_sha256") == cv["card_sha256"]):
                        old["reused"] = True
                        res[key] = old
                        continue
                    raise Refused(f"⛔ {f} 가 있는데 같은 궤적 · 같은 도구 판 · 같은 카드의 완료 기록이 아니다 — 확인 뒤 옮기고 다시")
                if calc is None:
                    calc = calc_factory(s)
                r = run_pressure(tdir, T, cv["n_atoms"], prod_for(cv, T), cv["save_fs"], calc, mq.EV_A3_TO_GPA)
                r.update({"system": s, "seed": sd, "T_K": T, "traj_sha256": tsha, "tool_sha16": prov["tool_sha16"],
                          "card_sha256": cv["card_sha256"], "calc_mode": getattr(calc, "_mq_mode", None), "reused": False})
                _write_new(f, r)                         # 런마다 점진 저장 — 중간에 죽어도 끝난 런은 남는다
                res[key] = r
    per = {}
    systems = cv["systems"]
    for T in temps:
        m = {s: [res.get(f"{s}{sd}_T{T}", {}).get("mean_GPa") for sd in cv["seeds"]] for s in systems}
        ok = all(x is not None for v in m.values() for x in v)
        mean = {s: (float(np.mean(v)) if ok else None) for s, v in m.items()}
        d = (mean[systems[0]] - mean[systems[1]]) if (ok and len(systems) == 2) else None
        per[str(T)] = {"mean_by_system_GPa": mean, "A_minus_B_GPa": d,
                       "warn_gt_1GPa": (abs(d) > PRESSURE_WARN_GPA) if d is not None else None}
    out = {"kind": "li2s3_stage2_pressure/v2", "status": "압력", **common,
           "runs": {k: {x: y for x, y in v.items() if x != "frames"} for k, v in res.items()}, "per_T": per,
           "runs_dir": str(rdir),
           "rule": "P = P_virial (UMA turbo 단일점 · −tr σ /3) + N k_B T_set / V · 프레임 k = j·10 − 1 (t = 1 … prod ps) · 계마다 새 계산기 · "
                   "판정에 안 씀 · 두 계 ⟨P⟩ 차 > 1 GPa 면 경고 하나 더 (보호 기준 아님)"}
    _write_new(outp, out)
    out["out_path"] = str(outp)
    return out


# ───────────────────────── 대조 잡 ─────────────────────────
def control(root_a, root_b, seeds=(1, 3), record=None, n_boot=N_BOOT, read_run=None, card=CARD, prov=None):
    """대조 잡 — 10-14 대조 계 판독 기록 행 (kgy 시드) 을 같은 읽기 경로로 재현하는가."""
    import glass_v2_readout as G
    import quench_ss_event as Q
    from ase.io import read
    cv = card_values(card)
    prov = provenance() if prov is None else prov
    rec = G.readout600(record or G.READOUT_600)
    head = {"kind": CONTROL_KIND, "provenance": prov, "card_sha256": cv["card_sha256"], "n_boot": n_boot,
            "roots": {"A": str(root_a), "B": str(root_b)}, "seeds": [int(s) for s in seeds]}
    if rec.get("status"):
        return {**head, "same": None, "status": rec["status"]}
    if rec.get("n_boot") != n_boot:
        return {**head, "same": None, "status": f"n_boot {n_boot} ≠ 기록 {rec.get('n_boot')}"}
    allowed = sorted({x.get("seed") for x in rec["A"] if x.get("machine") == "kgy"}
                     & {x.get("seed") for x in rec["B"] if x.get("machine") == "kgy"})
    sds = [int(s) for s in seeds]
    if not sds or len(set(sds)) != len(sds) or any(s not in allowed for s in sds):
        raise Refused(f"⛔ 대조 잡은 10-14 판독 기록의 kgy 시드 {allowed} 만 받는다 (받은 것 {sds})")
    for sys_, root in (("A", root_a), ("B", root_b)):          # 읽기 전에 — 루트가 그 대조 계인가
        for sd in sds:
            mp = pathlib.Path(root) / f"seed{sd}" / f"T{CONTROL_T}" / "run_meta.json"
            try:
                m = json.loads(mp.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                raise Refused(f"⛔ {mp} 를 못 읽었다 — 10-14 대조 계 루트가 아니다 (읽지 않는다)")
            wl, ws = CONTROL_LABEL[sys_].format(S=sd), CONTROL_VSEED_OFFSET + sd
            if m.get("label") != wl or m.get("seed") != ws:
                raise Refused(f"⛔ {mp}: label {m.get('label')!r} · seed {m.get('seed')!r} ≠ 10-14 대조 계 {wl!r} · {ws}"
                              " — 대조 잡 대상이 아니다 (읽지 않는다)")
    rr = read_run or G.read_run
    mq = Q._load_mq(str(HERE))
    diffs, rows = [], []
    for sys_, root in (("A", root_a), ("B", root_b)):
        old = {x.get("seed"): x for x in rec[sys_]}
        for sd in sds:
            tdir = pathlib.Path(root) / f"seed{sd}" / f"T{CONTROL_T}" / "d0.00_cfg0" / f"T{CONTROL_T}"
            try:
                first = read(str(tdir / "traj.xyz"), index=0)
                ar = json.loads((tdir / "aimd_results.json").read_text(encoding="utf-8"))
                eq = json.loads((tdir.parents[1] / "run_meta.json").read_text(encoding="utf-8")).get("equilib_ps")
                probs, _, _, _ = check_trajectory(tdir, len(first), first.get_chemical_symbols(), float(ar["prod_ps"]), CONTROL_T,
                                                  float(eq), cv["save_fs"], cv["dt_fs"], cv["caps"], cv["T_tol"])
                probs += check_msd(tdir, CONTROL_T, int(round(float(ar["prod_ps"]) * 1000.0 / cv["save_fs"])), cv["save_fs"])
            except Exception as e:
                probs = [f"못 읽었다 ({type(e).__name__}: {e})"]
            if probs:
                diffs.append(f"{sys_} seed{sd}: 궤적 유효성 실패 — {probs[:2]} (옛 런을 이 검사가 거부 = 검사 결함 의심)")
                continue
            x = _row(G, {k: v for k, v in rr(tdir / "msd.json", n_boot=n_boot, framework=True, mq=mq).items() if k != "_D_slope"})
            y = old.get(sd)
            rows.append({"system": sys_, "seed": sd, **{k: x[k] for k in G.ROW_SAME_EXACT + G.ROW_SAME_FLOAT}})
            if y is None:
                diffs.append(f"{sys_} seed{sd}: 기록에 행이 없다")
                continue
            for k in G.ROW_SAME_EXACT:
                if x.get(k) != y.get(k):
                    diffs.append(f"{sys_} seed{sd} {k}: 기록 {y.get(k)} · 지금 {x.get(k)}")
            for k in G.ROW_SAME_FLOAT:
                u, w = x.get(k), y.get(k)
                if u is None or w is None or abs(u - w) > 1e-9:
                    diffs.append(f"{sys_} seed{sd} {k}: 기록 {w} · 지금 {u}")
            if (x.get("skeleton") or {}).get("values") != (y.get("skeleton") or {}).get("values"):
                diffs.append(f"{sys_} seed{sd} 골격 네 값: 기록 {(y.get('skeleton') or {}).get('values')} · 지금 {(x.get('skeleton') or {}).get('values')}")
    return {**head, "same": not diffs, "diffs": diffs, "rows": rows, "record_tool_sha16": rec.get("tool_sha16"),
            "⚠": "대조 잡 — 판정 규칙이 아니다 · 같은 읽기 경로 (궤적 유효성 → read_run → skeleton_gate) 의 무결성 확인 · "
                 "판독 허가는 이 출력 (같은 도구 sha16 · 깨끗한 트리 · same True) 을 요구한다"}


# ───────────────────────── selftest ─────────────────────────
_STUB_PRETRAINED = '''"""selftest 용 fairchem 스텁 (물리 아님) — FAKE_NO_TURBO=1 이면 turbo 요청이 실패한다 (드라이버가 기본 모드로 내려간다)."""
import os


def get_predict_unit(name, device="cuda", inference_settings=None):
    if inference_settings == "turbo" and os.environ.get("FAKE_NO_TURBO"):
        raise RuntimeError("stub: turbo unavailable")
    return {"name": name, "settings": inference_settings, "merged_on": None}
'''
_STUB_CALC = '''"""selftest 용 계산기 스텁 — P · S · Cl 은 처음 본 자리에 조화 구속 (최소상) · Li 는 힘 없음 · 응력 상수.
FAKE_STRICT_TURBO=1 이면 turbo 예측기가 처음 본 조성과 다른 조성을 받을 때 죽는다 (merge_mole 흉내)."""
import os
import numpy as np
from ase.calculators.calculator import Calculator, all_changes


class FAIRChemCalculator(Calculator):
    implemented_properties = ["energy", "forces", "stress"]

    def __init__(self, pu, task_name="omat", k=50.0, p0=0.01):
        super().__init__()
        self.pu, self.task_name, self.k, self.p0, self.ref = pu, task_name, k, p0, None

    def calculate(self, atoms=None, properties=("energy",), system_changes=all_changes):
        super().calculate(atoms, properties, system_changes)
        sym = np.asarray(atoms.get_chemical_symbols())
        comp = tuple(sorted((s, int((sym == s).sum())) for s in set(sym.tolist())))
        if (self.pu or {}).get("settings") == "turbo" and os.environ.get("FAKE_STRICT_TURBO"):
            if self.pu.get("merged_on") is None:
                self.pu["merged_on"] = comp
            elif self.pu["merged_on"] != comp:
                raise AssertionError("stub turbo: merged on a different composition")
        pos, cell = atoms.get_positions(), np.asarray(atoms.get_cell())
        if self.ref is None or len(self.ref) != len(atoms):
            self.ref = pos.copy()
        d = pos - self.ref
        f = d @ np.linalg.inv(cell)
        f -= np.round(f)
        d = f @ cell
        d[sym == "Li"] = 0.0
        self.results["energy"] = float(0.5 * self.k * (d ** 2).sum())
        self.results["forces"] = -self.k * d
        self.results["stress"] = np.array([-self.p0, -self.p0, -self.p0, 0.0, 0.0, 0.0])
'''


def _st_inputs(td, mq):
    """합성 입력 — A (Li48 P12 S48 Cl12) · B (Li45 P15 S60) × 11 · 12 (저장소의 build_random_cell · 실제 담금질과 같은 원소 순서).
    A11 · B12 는 실제 결함 꼴 (P 하나가 S 하나를 잃고 그 S 가 다른 단위의 S 와 2.05 Å — 컷 2.30 에서 넉넉히 떨어뜨린다).
    결함 표지 (카드 '입력_2026_11_10.시드' 꼴) 는 시험용 기록이다 — 최단 원자간 · 그 쌍은 정해 둔 값 (측정이 아니다)."""
    from ase import Atoms
    from ase.io import write
    from ase.geometry import get_distances
    sha, rec, defects = {}, {}, {}
    for s_, nfu in (("A", 12), ("B", 15)):
        for sd in (11, 12):
            sym, pos, cell = mq.build_random_cell(s_, sd, density_g_cm3=1.2, n_fu=nfu)
            sym, pos = np.asarray(sym), np.asarray(pos, float)
            defect = (s_, sd) in (("A", 11), ("B", 12))
            if defect:
                iP, iS = np.where(sym == "P")[0], np.where(sym == "S")[0]
                s0 = iS[np.argsort(mq.mic_dists(pos[[iP[0]]], pos[iS], cell)[0])[0]]
                s1 = iS[np.argsort(mq.mic_dists(pos[[iP[1]]], pos[iS], cell)[0])[0]]
                v = pos[s1] - pos[iP[1]]
                pos[s0] = pos[s1] + 2.05 * v / np.linalg.norm(v)
                if mq.mic_dists(pos[[s0]], pos[iP], cell)[0].min() <= mq.R_PS:
                    raise RuntimeError("selftest 입력: 떼어 낸 S 가 P 에 너무 가깝다")
            a = Atoms(sym.tolist(), positions=pos, cell=cell, pbc=True)
            f = td / "src" / s_ / f"seed{sd}" / "final.xyz"
            f.parent.mkdir(parents=True, exist_ok=True)
            write(str(f), a, format="extxyz")
            _, DD = get_distances(a.positions[sym == "P"], a.positions[sym == "S"], cell=a.cell, pbc=True)
            ps, n4 = float(DD.min()), int(((DD <= 2.6).sum(axis=1) == 4).sum())
            rho = float(a.get_masses().sum() * 1.66053906660 / a.get_volume())
            sha[f"{s_}{sd}"], rec[f"{s_}_{sd}"] = _sha(f), f"{ps:.4f} {n4} {rho:.4f}"
            ind = mq.indicators(sym, pos, cell)
            nP = int((sym == "P").sum())
            defects[f"{s_}{sd}"] = {"P_S_배위": {str(k): v for k, v in ind["P_S_coord_hist"].items()},
                                   "다리_S": ind["bridging_S_P2S7_like"], "P_P": ind["P_P_bonds_P2S6_like"],
                                   "li2s2_판정": "pass" if n4 == nP else f"fail — PS₄ 보존율 {n4}/{nP}",
                                   "최단_원자간_P_S_제외_A": 2.05 if defect else 2.25, "그_쌍": "S-S" if defect else "Li-S"}
    defects["A13"] = {"P_S_배위": {"3": 1, "4": 11}, "다리_S": 0, "P_P": 0, "li2s2_판정": "fail — PS₄ 보존율 11/12",
                      "최단_원자간_P_S_제외_A": 1.95, "그_쌍": "S-S"}             # 포함 가능군 밖 (최단 원자간 ≤ 2.0 Å) — 층 셈 시험
    defects["B13"] = {"P_S_배위": {"4": 15}, "다리_S": 0, "P_P": 0, "li2s2_판정": "pass", "최단_원자간_P_S_제외_A": 2.2, "그_쌍": "Li-S"}
    return sha, rec, defects


def _st_card(path, sha, defects, systems, seeds, temps, prod, permit=None, drop=(), extra=None):
    s2 = {"systems": systems, "seeds": seeds, "temperatures_K": temps, "prod_ps": prod, "equilib_ps": 5.0, "vseed_offset": 3000,
          "n_atoms": 120, "save_fs": 100.0, "dt_fs": 2.0, "bind_PS_median_disp_max_A": 1.0,
          # 스텁의 Li 는 힘 없는 브라운 입자라 실제보다 훨씬 멀리 간다 — 시험 카드의 Li 상한만 6 Å (실제 카드 값은 카드가 정한다)
          "continuity_max_A": {"Li": 6.0, "P": 2.5, "S": 2.5, "Cl": 2.5}, "mean_T_tol_frac": 0.05}
    s2.update(extra or {})                    # v2 큐 기계 값 (conditional · cap · 한도 · 견적 · queue_v2) — v2 시험 카드만
    for k in drop:
        s2.pop(k, None)
    c = {"기계_판독_값": {"decision": NEED_ACTIVE[0], "stage2": s2, "md_driver_sha16": _sha(REPO / WT_FILES["md_driver"])[:16],
                         "md_runner_sha16": _sha(REPO / WT_FILES["md_runner"])[:16], "inputs_sha256": sha,
                         "inclusion": {"min_pair_excl_PS_A_gt": 2.0}},
         "입력_2026_11_10": {"시드": defects}}
    if permit is not None:
        c[READ_PERMIT_KEY] = permit
    pathlib.Path(path).write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
    return pathlib.Path(path)


def _st_launch(td, base, rec, sha, temps, prod, systems, seeds, decisions):
    """실제 v1 큐 (run_stage2_kgy.sh) → 실제 v2 러너 → 실제 MD 드라이버 (fairchem 스텁) — 최소 환경으로 띄운다."""
    env = {"HOME": os.environ.get("HOME", str(td)), "PATH": f"{td / 'bin'}:{os.environ.get('PATH', '/usr/bin:/bin')}",
           "PYTHONPATH": str(td / "stub"), "PYTHONIOENCODING": "utf-8", "LANG": os.environ.get("LANG", "C.UTF-8"),
           "PY": sys.executable, "BASE": str(base), "SRC": str(td / "src"), "REF": str(td / "ref"), "DECISIONS": str(decisions),
           "CARD_DECISION": NEED_ACTIVE[0], "TEMPS": temps, "PROD": prod, "SYSTEMS": systems, "SEEDS": seeds,
           "POLL": "1", "GPU_WAIT": "5", "META_WAIT": "180"}
    for k, v in sha.items():
        env[f"SHA_{k[0]}_{k[1:]}"] = v
    for k, v in rec.items():
        env[f"REC_{k}"] = v
    log = open(td / f"queue_{pathlib.Path(base).name}.log", "w", encoding="utf-8")
    return subprocess.Popen(["bash", str(REPO / WT_FILES["queue_v1"])], env=env, stdout=log, stderr=subprocess.STDOUT), log


def _st_q2(td, base, card, decisions, phase, test=True, script=None, **extra):
    """실제 v2 큐 (run_stage2_kgy_v2.sh) → 실제 MD 드라이버 (fairchem 스텁) — 최소 환경으로 끝까지 돌린다 → (종료 코드, 출력).
    test 면 V2_TEST=1 (시험 카드 · 원장 — 시작 기록 test: true) · 아니면 script (임시 git 저장소의 큐 사본) 의 저장소 카드 · 원장으로."""
    env = {"HOME": os.environ.get("HOME", str(td)), "PATH": f"{td / 'bin'}:{os.environ.get('PATH', '/usr/bin:/bin')}",
           "PYTHONPATH": str(td / "stub"), "PYTHONIOENCODING": "utf-8", "LANG": os.environ.get("LANG", "C.UTF-8"),
           "PY": sys.executable, "BASE": str(base), "SRC": str(td / "src"), "CARD": str(card), "DECISIONS": str(decisions),
           "PHASE": phase, "POLL": "1", "GPU_WAIT": "5", "META_WAIT": "180", **({"V2_TEST": "1"} if test else {}), **extra}
    r = subprocess.run(["bash", str(script or (REPO / QUEUE_V2_REL))], env=env, capture_output=True, text=True, timeout=1800)
    return r.returncode, r.stdout + r.stderr


def _st_git_root(td, files, name="groot"):
    """시험용 git 저장소 — {저장소 경로: 원본 파일 또는 bytes} 를 넣고 커밋 → (루트, git 명령 머리). 저장소 파일은 안 바꾼다."""
    root = pathlib.Path(td) / name
    for rel, src in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_bytes(src if isinstance(src, bytes) else pathlib.Path(src).read_bytes())
    G = ["git", "-C", str(root), "-c", "user.name=selftest", "-c", "user.email=selftest@example.invalid", "-c", "commit.gpgsign=false",
         "-c", "core.hooksPath=/dev/null"]
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True, capture_output=True)
    subprocess.run(G + ["add", "-A"], check=True, capture_output=True)
    subprocess.run(G + ["commit", "-q", "-m", "selftest"], check=True, capture_output=True)
    return root, G


def _selftest():
    """판독 selftest — 시험 런 (V2_TEST=1) 은 이 동안만 받는다 (ALLOW_TEST_RUNS) · 커밋 결속 저장소 (V2_REPO) 도 끝나면 되돌린다."""
    mod = sys.modules[__name__]
    saved = (mod.ALLOW_TEST_RUNS, mod.V2_REPO)
    mod.ALLOW_TEST_RUNS = True
    try:
        return _selftest_body()
    finally:
        mod.ALLOW_TEST_RUNS, mod.V2_REPO = saved


def _selftest_body():
    import tempfile
    import time
    import glass_v2_readout as G
    import quench_ss_event as Q
    from ase import Atoms
    from ase.io import read, write
    n_ok, fails = 0, []
    t0 = time.time()

    def chk(c, msg):
        nonlocal n_ok
        if c:
            n_ok += 1
            print(f"  ✔ {msg}", flush=True)
        else:
            fails.append(msg)
            print(f"  ✘ {msg}", flush=True)

    def refuses(kw, fn, *a, **k):
        try:
            fn(*a, **k)
        except SystemExit as e:
            if kw not in str(e):
                print(f"     (거부 문구: {e})")
            return kw in str(e)
        except Exception as e:
            print(f"     (터짐 {type(e).__name__}: {e})")
            return False
        return False

    mq = Q._load_mq(str(HERE))
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        # ── 준비: 스텁 · 가짜 nvidia-smi · 입력 · 기준 · 결정 ──
        (td / "stub" / "fairchem" / "core" / "calculate").mkdir(parents=True)
        (td / "stub" / "fairchem" / "__init__.py").write_text("")
        (td / "stub" / "fairchem" / "core" / "__init__.py").write_text('__version__ = "stub-0"\n')
        (td / "stub" / "fairchem" / "core" / "calculate" / "__init__.py").write_text("")
        (td / "stub" / "fairchem" / "core" / "pretrained_mlip.py").write_text(_STUB_PRETRAINED)
        (td / "stub" / "fairchem" / "core" / "calculate" / "ase_calculator.py").write_text(_STUB_CALC)
        (td / "bin").mkdir()
        (td / "bin" / "nvidia-smi").write_text("#!/bin/bash\necho 3000\n")
        (td / "bin" / "nvidia-smi").chmod(0o755)
        sha, rec, defects = _st_inputs(td, mq)
        (td / "ref" / "d0.00_cfg0" / "T600").mkdir(parents=True)
        (td / "ref" / "run_meta.json").write_text(json.dumps(
            {"label": "ref", "n_atoms": 120, "supercell": [1, 1, 1], "prod_ps": 400.0, "equilib_ps": 5.0, "fit_window_ps": [2.0, 50.0],
             "save_traj": True, "uma_model": "uma-s-1p1", "uma_inference_mode_requested": "turbo", "temperatures": [600.0],
             "seed": 1, "v0_xyz": "x"}))
        (td / "ref" / "d0.00_cfg0" / "T600" / "md.log").write_text("Time[ps]      Etot[eV]\n0.0000 -1\n0.0020 -1\n")
        dec = td / "dec.json"
        dec.write_text(json.dumps({"decisions": [{"id": i, "decision_state": "active"} for i in NEED_ACTIVE]}))
        # ── 실제 체인: v1 큐 → v2 러너 → 드라이버 (두 큐를 함께 띄운다) ──
        b8, bR = td / "b8", td / "bR"
        p8, l8 = _st_launch(td, b8, rec, sha, "600 650", "3", "A B", "11 12", dec)
        pR, lR = _st_launch(td, bR, rec, {"A12": sha["A12"]}, "600", "100", "A", "12", dec)
        rc8, rcR = p8.wait(timeout=1800), pR.wait(timeout=1800)
        l8.close(), lR.close()
        chk(rc8 == 0 and rcR == 0, f"[준비] 실제 v1 큐 · v2 러너 · 드라이버 (fairchem 스텁) 로 런 9 개 — 3 ps × 8 · 100 ps × 1 "
                                   f"(종료 {rc8} · {rcR} · {time.time() - t0:.0f} s)")
        if rc8 != 0 or rcR != 0:
            for nm in ("b8", "bR"):
                print((td / f"queue_{nm}.log").read_text(encoding="utf-8", errors="replace")[-2500:])
            print(f"selftest FAIL — {n_ok}/{n_ok + len(fails)} (실제 체인을 못 만들었다 — 이어서 시험할 수 없다)")
            return 1
        card8 = _st_card(td / "card8.json", sha, defects, ["A", "B"], [11, 12], [600, 650], 3.0)
        cardR = _st_card(td / "cardR.json", sha, defects, ["A"], [12], [600], 100.0)
        cv8, cvR = card_values(card8), card_values(cardR)
        WT = REPO
        n_clone = [0]

        def clone(src, sys_=None, sd=None, T=None):
            n_clone[0] += 1
            dst = td / f"c{n_clone[0]}"
            if sys_ is None:
                shutil.copytree(src, dst)
                return dst
            for f in ("stage2_kgy.log", "cost_ledger.tsv"):
                if (src / f).exists():
                    dst.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src / f, dst / f)
            (dst / sys_).mkdir(parents=True, exist_ok=True)
            shutil.copy2(src / sys_ / "queue_kgy.log", dst / sys_ / "queue_kgy.log")
            shutil.copytree(src / sys_ / "init", dst / sys_ / "init")
            shutil.copytree(src / sys_ / f"seed{sd}" / f"T{T}", dst / sys_ / f"seed{sd}" / f"T{T}")
            return dst

        def tdir_of(b, s_, sd, T):
            return b / s_ / f"seed{sd}" / f"T{T}" / "d0.00_cfg0" / f"T{T}"

        def edit_text(p, fn):
            p = pathlib.Path(p)
            p.write_text(fn(p.read_text(encoding="utf-8")), encoding="utf-8")

        def edit_json(p, fn):
            p = pathlib.Path(p)
            d = json.loads(p.read_text(encoding="utf-8"))
            fn(d)
            p.write_text(json.dumps(d), encoding="utf-8")

        def rewrite_traj(p, fn):
            fr = read(str(p), index=":")
            fr = fn(fr)
            pathlib.Path(p).unlink()
            for a in fr:
                write(str(p), a, format="extxyz", append=True)

        # ── 양성: 실제 체인 ──
        q8 = queue_record(b8, cv8)
        chk(q8["status"] == "valid" and q8["complete"] and q8["base_original"] == str(b8)
            and q8["gatekeep"]["runner_sha16"] == cv8["md_runner_sha16"],
            "[양성] 큐 로그: PHASE ladder 시작 하나 (온도 · 시드 · 계 · prod = 카드) · 문지기 러너 sha16 · 원래 BASE · 큐 끝")
        _, runs8 = verify_all(b8, cv8, WT, keep_PS=True)
        chk(all(v["status"] == "valid" for v in runs8.values()) and all(v["runner_rc"] == 0 for v in runs8.values())
            and all(v["cost_source"] == "장부" for v in runs8.values()),
            f"[양성] 실제 드라이버 출력 8 런이 사후 검증 ①–⑦ valid (프레임 수 = prod/save = 30 · 러너 블록 · 실제 모드 turbo · "
            f"첫 프레임 결속 · md.log · MTO 배열) — {sorted({v['status'] for v in runs8.values()})}")
        if any(v["status"] != "valid" for v in runs8.values()):
            for k, v in runs8.items():
                if v["status"] != "valid":
                    print(f"     {k}: {v['status']} — {'; '.join(v['reasons'])[:200]}")
            print(f"selftest FAIL — {n_ok}/{n_ok + len(fails)} (실제 드라이버 출력이 검증을 못 통과한다 — 이어서 시험할 수 없다)")
            return 1
        ar = json.loads((tdir_of(b8, "A", 11, 600) / "aimd_results.json").read_text())
        chk(ar["n_frames"] == 30 and len(read(str(tdir_of(b8, "A", 11, 600) / "traj.xyz"), index=":")) == 30,
            "[양성] 실제 드라이버는 3 ps 에 30 프레임을 쓴다 (prod/save · +1 아님 — 리뷰 EB P0-1 의 근거)")
        vA = runs8[("A", 11, 600)]
        rA = records_abc(vA["_frames"], vA["_input_atoms"], mq)
        cA = rA["ⓒ_input_vs_first_frame"]
        chk(cA["P_coord_hist_input"] == {3: 1, 4: 11} and cA["SS_pairs_input"] == 1 and len(cA["input_not4_P"]) == 1
            and str(cA["input_not4_P"][0]) in rA["ⓑ_per_P"] and rA["ⓐ_first_frame_SS_pairs"]
            and all(k in rA["ⓐ_first_frame_SS_pairs"][0] for k in ("d_min_A", "d_median_A", "d_max_A")),
            "[양성] 기록 (실제 체인 A11): 입력 P 배위 {3: 1, 4: 11} · S–S 1 쌍 · 결함 P 전역 번호 · ⓑ P 별 · ⓐ 쌍별 거리 최소 · 중앙 · 최대")

        # ── 음성: 사후 검증 (런 하나 · 실제 체인 사본을 깨서) ──
        def neg(label, mutate, kw, want="invalid", s_="B", sd=11, T=600, cv=None, wt=None, full=False):
            b = clone(b8) if full else clone(b8, s_, sd, T)
            mutate(b)
            v = verify_run(b, s_, sd, T, cv or cv8, wt or WT)
            chk(v["status"] == want and any(kw in q for q in v["reasons"]),
                f"⛔음성: {label} → {want} ({'; '.join(v['reasons'])[:110]})")
            return v

        B11 = lambda b: tdir_of(b, "B", 11, 600)

        def plus1(b):
            p = B11(b) / "traj.xyz"
            write(str(p), read(str(p), index=-1), format="extxyz", append=True)
            edit_json(B11(b) / "aimd_results.json", lambda d: d.__setitem__("n_frames", d["n_frames"] + 1))
        neg("+1 꼴 (프레임 31 · aimd n_frames 31 — 옛 selftest 픽스처 꼴)", plus1, "계획 30")
        neg("aimd_results n_frames 만 31 (궤적은 30)", lambda b: edit_json(B11(b) / "aimd_results.json",
            lambda d: d.__setitem__("n_frames", d["n_frames"] + 1)), "aimd_results n_frames")
        neg("드라이버 종료 코드 7 (msd.json 은 있음)", lambda b: edit_text(b / "B" / "queue_kgy.log",
            lambda t: t.replace("✅ T600 seed11 끝 (rc 0)", "✅ T600 seed11 끝 (rc 7)")), "종료 코드 7")
        neg("러너 끝 줄 없음 (msd.json 은 있음 · 아직 정리 중)", lambda b: edit_text(b / "B" / "queue_kgy.log",
            lambda t: "\n".join(ln for ln in t.splitlines() if "✅ T600 seed11 끝" not in ln and "■ 큐 끝 · 600:11:" not in ln)),
            "끝 줄", want="incomplete")

        def dup_block(b):
            t = (b / "B" / "queue_kgy.log").read_text(encoding="utf-8")
            blk = [ln for ln in t.splitlines()]
            i0 = next(i for i, ln in enumerate(blk) if "▶ v2 큐 시작 · 600:11:" in ln)
            i1 = next(i for i, ln in enumerate(blk) if "■ 큐 끝 · 600:11:" in ln)
            (b / "B" / "queue_kgy.log").write_text(t + "\n".join(blk[i0:i1 + 1]) + "\n", encoding="utf-8")
        neg("같은 런의 호출 블록 둘 (다시 띄움)", dup_block, "블록이 2 개")
        neg("러너 블록의 드라이버 sha16 이 다름 (다른 드라이버)", lambda b: edit_text(b / "B" / "queue_kgy.log",
            lambda t: t.replace(f"드라이버 sha16 {cv8['md_driver_sha16']} ✅", "드라이버 sha16 7cbd8c3701892dc6 ✅", 1)), "드라이버 sha16")
        neg("큐 문지기의 러너 sha16 이 다름 (다른 러너)", lambda b: edit_text(b / "stage2_kgy.log",
            lambda t: t.replace(f"러너 sha16 {cv8['md_runner_sha16']}", "러너 sha16 6be496dc715551d7")), "다른 러너")
        neg("큐 시작 줄의 온도 ≠ 카드 (TEMPS 바꿔 띄움)", lambda b: edit_text(b / "stage2_kgy.log",
            lambda t: t.replace("· 온도 600 650 ·", "· 온도 600 900 ·")), "temperatures")
        def dup_start_inside(t):
            first = next(ln for ln in t.splitlines() if "큐 시작 · PHASE ladder" in ln)
            return t.replace(first, first + "\n" + first, 1)
        neg("사다리 블록 안에 큐 시작 줄이 둘 (끝나기 전에 다시 띄움)", lambda b: edit_text(b / "stage2_kgy.log", dup_start_inside),
            "블록 안에 2 개")
        LATE = "[2026-11-14 01:00:00] ▶ li2s-3 2 단계 큐 시작 · PHASE cond550 · 온도 550 · 시드 11 12 · 계 A B · prod 800 ps\n"
        bLt = clone(b8, "B", 11, 600)
        edit_text(bLt / "stage2_kgy.log", lambda t: t + LATE)
        vLt, qLt = verify_run(bLt, "B", 11, 600, cv8, WT), queue_record(bLt, cv8)
        chk(vLt["status"] == "valid" and qLt["status"] == "valid" and len(qLt["other_invocations"]) == 1,
            "[양성] (리뷰 EE P2-6) 사다리 블록 뒤의 v1 호출 (PHASE cond550) 은 사다리 런을 무효로 만들지 않는다 — 따로 적는다 (other_invocations)")
        LATE_L = "[2026-11-14 02:00:00] ▶ li2s-3 2 단계 큐 시작 · PHASE ladder · 온도 600 650 · 시드 11 12 · 계 A B · prod 3 ps\n"
        bLt2 = clone(b8, "B", 11, 600)
        edit_text(bLt2 / "stage2_kgy.log", lambda t: t + LATE_L)
        vLt2, qLt2 = verify_run(bLt2, "B", 11, 600, cv8, WT), queue_record(bLt2, cv8)
        chk(vLt2["status"] == "valid" and qLt2["status"] == "valid" and len(qLt2["other_invocations"]) == 1,
            "[양성] (리뷰 EE P2-6) 사다리 블록이 끝난 뒤 다시 띄운 사다리 큐도 블록 밖 호출이다 (런 무효 아님 · 따로 보류 사유)")
        neg("run_meta 실제 모드 default (turbo 못 켬)", lambda b: edit_json(b / "B" / "seed11" / "T600" / "run_meta.json",
            lambda d: d.__setitem__("uma_inference_mode", "default")), "uma_inference_mode")
        neg("ensemble_results task oc20", lambda b: edit_json(b / "B" / "seed11" / "T600" / "ensemble_results.json",
            lambda d: d.__setitem__("uma_task", "oc20")), "uma_task")
        neg("ensemble_results 가 중간 저장본 (끝 요약 없음)", lambda b: edit_json(b / "B" / "seed11" / "T600" / "ensemble_results.json",
            lambda d: [d.pop(k, None) for k in ("uma_inference_mode", "uma_task", "uma_model")]), "끝 요약")
        neg("ensemble_results prod ≠ 카드", lambda b: edit_json(b / "B" / "seed11" / "T600" / "ensemble_results.json",
            lambda d: d.__setitem__("prod_ps", 7.0)), "ensemble_results prod_ps")

        def at10(fn):
            return lambda b: rewrite_traj(B11(b) / "traj.xyz", lambda fr: [fn(a) if k >= 10 else a for k, a in enumerate(fr)])

        def nan_f(a):
            p = a.positions.copy(); p[3, 0] = np.nan; a.positions = p
            return a

        def swap_f(a):
            s = a.get_chemical_symbols(); s[1], s[-1] = s[-1], s[1]; a.set_chemical_symbols(s)
            return a

        def cell_f(a):
            a.set_cell(np.asarray(a.get_cell()) * 1.01, scale_atoms=False)
            return a
        neg("궤적 NaN 프레임", at10(nan_f), "유한")
        neg("궤적 원소 바뀜", at10(swap_f), "원소 순서")
        neg("궤적 셀 바뀜 (NVT)", at10(cell_f), "셀이 바뀌었다")
        neg("궤적 프레임 하나 모자람", lambda b: rewrite_traj(B11(b) / "traj.xyz", lambda fr: fr[:-1]), "프레임 29")
        neg("궤적 프레임 1 개", lambda b: rewrite_traj(B11(b) / "traj.xyz", lambda fr: fr[:1]), "2 개 미만")

        def li_perm(b):
            def fn(fr):
                sy = np.asarray(fr[15].get_chemical_symbols())
                li = np.where(sy == "Li")[0]
                D = mq.mic_dists(fr[15].positions[li], fr[15].positions[li], np.asarray(fr[15].get_cell()))
                i, j = np.unravel_index(np.argmax(D), D.shape)
                for a in fr[15:]:
                    p = a.positions.copy(); p[[li[i], li[j]]] = p[[li[j], li[i]]]; a.positions = p
                return fr
            rewrite_traj(B11(b) / "traj.xyz", fn)
        neg("Li 두 개의 번호가 15 번째 프레임부터 뒤바뀜 (같은 원소 순서 · 연속성)", li_perm, "Li 이동")

        def swap_traj(b):
            for f in ("traj.xyz", "msd.json", "aimd_results.json", "md.log"):
                shutil.copy2(tdir_of(b8, "A", 12, 600) / f, tdir_of(b, "A", 11, 600) / f)
        neg("다른 시드 (A12) 의 궤적 · msd · md.log 를 A11 폴더에 (같은 셀 · 같은 원소 순서)", swap_traj, "변위 중앙값",
            s_="A", sd=11)
        neg("모든 프레임의 셀이 config.xyz 와 다름 (1 %)", lambda b: rewrite_traj(B11(b) / "traj.xyz", lambda fr: [cell_f(a) for a in fr]),
            "첫 프레임 셀")

        def cfg_shift(b):
            p = b / "B" / "seed11" / "T600" / "d0.00_cfg0" / "config.xyz"
            a = read(str(p)); q = a.positions.copy(); q[0, 0] += 0.5; a.positions = q; write(str(p), a, format="extxyz")
        neg("드라이버가 쓴 시작 구조 ≠ init (0.5 Å)", cfg_shift, "시작 구조")
        cvX = json.loads(json.dumps({k: v for k, v in cv8.items()}))
        cvX["inputs_sha256"]["B11"] = "0" * 64
        neg("init sha256 ≠ 카드", lambda b: None, "sha256", cv=cvX)
        neg("run_meta seed 9011", lambda b: edit_json(b / "B" / "seed11" / "T600" / "run_meta.json",
            lambda d: d.__setitem__("seed", 9011)), "run_meta seed")
        neg("run_meta prod 7", lambda b: edit_json(b / "B" / "seed11" / "T600" / "run_meta.json",
            lambda d: d.__setitem__("prod_ps", 7.0)), "run_meta prod_ps")
        neg("run_meta v0 가 원래 BASE 밖", lambda b: edit_json(b / "B" / "seed11" / "T600" / "run_meta.json",
            lambda d: d.__setitem__("v0_xyz", "/tmp/other/B/init/seed11_final.xyz")), "v0_xyz")
        neg("md.log 이어 쓰기 (머리 줄 둘)", lambda b: edit_text(B11(b) / "md.log",
            lambda t: t + "Time[ps]      Etot[eV]     Epot[eV]     Ekin[eV]    T[K]\n0.0000 1.0 1.0 1.0 600.0\n"), "머리 줄")
        neg("md.log 가운데 행 하나 빠짐", lambda b: edit_text(B11(b) / "md.log",
            lambda t: "\n".join(ln for i, ln in enumerate(t.splitlines()) if i != 100) + "\n"), "행 수")

        def hot(t):
            L = t.splitlines()
            return "\n".join([L[0]] + [" ".join(ln.split()[:-1] + [f"{1.5 * float(ln.split()[-1]):.1f}"]) for ln in L[1:] if ln.strip()]) + "\n"
        neg("md.log 생산 평균 T 가 설정의 1.5 배 (다른 열욕)", lambda b: edit_text(B11(b) / "md.log", hot), "평균 T")
        neg("깨진 msd.json", lambda b: (B11(b) / "msd.json").write_text("{broken"), "msd.json 을 못 읽었다")
        neg("msd.json MTO 첫 값 NaN (read_run 이 쓰는 배열)", lambda b: edit_json(B11(b) / "msd.json",
            lambda d: d["msd_Li_A2_mto"].__setitem__(0, float("nan"))), "MTO")
        neg("msd.json MTO 를 5 점으로 자름", lambda b: edit_json(B11(b) / "msd.json",
            lambda d: [d.__setitem__(k, d[k][:5]) for k in ("times_ps_mto", "msd_Li_A2_mto")]), "MTO")
        neg("msd.json times_ps 길이 ≠ 프레임 수", lambda b: edit_json(B11(b) / "msd.json",
            lambda d: [d.__setitem__(k, d[k][:-1]) for k in ("times_ps", "msd_Li_A2")]), "times_ps")
        neg("msd.json 없음 (끝나지 않았다 · 러너 끝 줄도 없음)", lambda b: ((B11(b) / "msd.json").unlink(), edit_text(b / "B" / "queue_kgy.log",
            lambda t: "\n".join(ln for ln in t.splitlines() if "✅ T600 seed11 끝" not in ln))), "msd.json 없음", want="incomplete")
        neg("런 폴더 없음 (시작 안 함)", lambda b: shutil.rmtree(b / "B" / "seed11" / "T600"), "런 폴더", want="incomplete")
        bad_wt = td / "wt_bad"
        for key, rel in WT_FILES.items():
            (bad_wt / rel).parent.mkdir(parents=True, exist_ok=True)
            (bad_wt / rel).write_bytes(b"other driver" if key == "md_driver" else (REPO / rel).read_bytes())
        neg("판독 시점 worktree 의 드라이버 sha16 ≠ 카드 (⑦ 보조)", lambda b: None, "판독 시점 worktree", wt=bad_wt)
        bL = clone(b8, "B", 11, 600)
        (bL / "cost_ledger.tsv").unlink()
        vL = verify_run(bL, "B", 11, 600, cv8, WT)
        chk(vL["status"] == "valid" and vL["cost_h"] is not None and vL["cost_h"] >= 0 and "러너 로그 시각" in vL["cost_source"],
            f"⛔음성: 장부 없음 → 비용은 러너 블록 시각으로 재구성 (0 아님 · 판정과 별개) — {vL['cost_source']}")
        chk(card_values(card8)["n_atoms"] == 120 and refuses("기계 값이 모자란다", card_values,
            _st_card(td / "card_drop.json", sha, defects, ["A", "B"], [11, 12], [600, 650], 3.0, drop=("save_fs", "n_atoms"))),
            "⛔음성: 카드 기계 값 (n_atoms · save_fs …) 이 없으면 거부 — 도구는 값을 따로 갖지 않는다")

        # ── 기록 ⓐ · ⓑ 단위 시험 (합성 좌표 · 판정과 무관한 셈) ──
        tet = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) / math.sqrt(3) * 2.05
        P1, P2 = np.array([3.0, 3, 3]), np.array([9.0, 9, 9])
        pos0 = [P1] + list(P1 + tet) + [P2] + list(P2 + tet[:3]) + [np.array([6.0, 2.0, 9.0]), np.array([6.0, 2.0, 11.1]),
                                                                     np.array([2.0, 9.0, 6.0])]
        sy0 = ["P"] + ["S"] * 4 + ["P"] + ["S"] * 3 + ["S", "S", "S"]
        a_in = Atoms(sy0, positions=np.vstack(pos0), cell=np.eye(3) * 12.0, pbc=True)
        sy0a = np.asarray(sy0)
        frames = []
        for k in range(20):
            p = a_in.positions.copy()
            if k >= 10:
                p[10, 2] = p[9, 2] + 4.0                    # 기존 S–S 쌍 (2.1 Å) 을 4.0 Å 로 (리뷰 DZ P2-1 반례)
            if k >= 12:
                p[11] = p[5] + tet[3]                       # P (전역 5) 가 S 를 하나 더 얻는다 (3→4)
            frames.append(p)
        dat = {"P": [f[sy0a == "P"] for f in frames], "S": [f[sy0a == "S"] for f in frames], "cell": np.eye(3) * 12.0}
        ru = records_abc(dat, a_in, mq)
        pa = ru["ⓐ_first_frame_SS_pairs"]
        chk(len(pa) == 1 and not pa[0]["kept_last"] and pa[0]["n_break"] == 1 and abs(pa[0]["frac_frames_kept"] - 0.5) < 1e-9
            and pa[0]["d_max_A"] >= 4.0 - 1e-9 and pa[0]["d_min_A"] < 2.30,
            "[양성] 기록 ⓐ: 기존 S–S 쌍 소멸 (2.1 → 4.0 Å) — 유지 분율 · 마지막 · 끊김 · 쌍별 거리 최소 · 최대 (골격 ①–④ 는 못 잡는 반례)")
        chk(ru["ⓑ_per_P"]["5"]["transitions"] == {"3→4": 1} and ru["ⓑ_per_P"]["5"]["first"] == 3 and ru["ⓑ_per_P"]["5"]["last"] == 4
            and ru["ⓑ_per_P"]["0"]["transitions"] == {} and ru["ⓒ_input_vs_first_frame"]["input_not4_P"] == [5],
            "[양성] 기록 ⓑ: P 별 (전역 번호 5) 배위 전이 3→4 · 다른 P 는 전이 없음 · ⓒ 입력 결함 P 번호")

        # ── 판독 허가 · 대조 잡 준비 ──
        prov_ok = dict(provenance(), tree_clean=True, dirty_tracked=[])
        prepo = td / "prepo"
        (prepo / "kb" / "reviews").mkdir(parents=True)
        (prepo / "kb" / "reviews" / "eb.md").write_text("EB 회신 (시험)\n", encoding="utf-8")
        ctlA, ctlB = td / "ctlA", td / "ctlB"
        for root, s_, lab in ((ctlA, "A", "lpscl_glass_v2_s{S}_T600"), (ctlB, "B", "lpscl_glass_ctrlB_s{S}_T600")):
            for sd_new, sd_src in ((1, 11), (3, 12)):
                dst = root / f"seed{sd_new}" / "T600"
                shutil.copytree(b8 / s_ / f"seed{sd_src}" / "T600", dst)
                edit_json(dst / "run_meta.json", lambda d, sd_new=sd_new, lab=lab: d.update(label=lab.format(S=sd_new), seed=1000 + sd_new))

        def fake_rr_for(outcome):
            def rr_(msd, n_boot=400, framework=True, mq=None):
                p = pathlib.Path(msd)
                T = int(p.parent.name[1:]); sd = int(p.parents[3].name[4:]); s = p.parents[4].name
                o = outcome(s, sd, T) or {}
                fw = {"P": {"frac_frames_any_P_changed_vs_first": 0.0}, "S_moved": o.get("S_moved", 0), "SS_new": 0, "S_transient": 0}
                return {"C1_pass": o.get("C1", True), "C1_msd_at_50_mto_A2": 5.0, "beta_MTO": o.get("beta", 1.0), "_D_slope": 1e-6,
                        "C2": {"final_verdict": o.get("C2", "통과"), "b_end": 64, "b_prev": 48, "n_sigma_end_signed": 0.5,
                               "n_sigma_prev_signed": 0.4},
                        "framework": ({"status": "못 쟀다 (시험)"} if o.get("fw_missing") else fw)}
            return rr_
        ctl_rr = fake_rr_for(lambda s, sd, T: {})
        x0 = _row(G, {k: v for k, v in ctl_rr(ctlA / "seed1" / "T600" / "d0.00_cfg0" / "T600" / "msd.json").items() if k != "_D_slope"})

        def write_record(path, beta_A3=None):
            rows_ = lambda: [dict({k: x0[k] for k in G.ROW_SAME_EXACT + G.ROW_SAME_FLOAT}, seed=sd, machine=mch, skeleton=x0["skeleton"])
                             for sd, mch in ((1, "kgy"), (2, "gabia"), (3, "kgy"))]
            ra, rb = rows_(), rows_()
            if beta_A3 is not None:
                ra[2]["beta_MTO"] = beta_A3
            pathlib.Path(path).write_text(json.dumps({"aggregate": {"systems": {"A": {"rows": ra, "N": 3}, "B": {"rows": rb, "N": 3}}},
                                                      "n_boot": 400, "tool_sha16": {"glass_v2_readout.py": "selftest"}}))
            return pathlib.Path(path)
        recp = write_record(td / "rec1014.json")
        co = control(ctlA, ctlB, seeds=(1, 3), record=recp, read_run=ctl_rr, card=card8, prov=prov_ok)
        chk(co["same"] is True and co["kind"] == CONTROL_KIND and co["provenance"]["tool_sha16"] == prov_ok["tool_sha16"],
            f"[양성] 대조 잡: kgy 시드 1 · 3 · 라벨 · 난수 확인 뒤 같은 읽기 경로로 기록 행 재현 (same True · 출처 기록) — {co.get('diffs')}")
        co2 = control(ctlA, ctlB, seeds=(1, 3), record=write_record(td / "rec1014b.json", beta_A3=1.5), read_run=ctl_rr, card=card8, prov=prov_ok)
        chk(co2["same"] is False and any("beta_MTO" in d for d in co2["diffs"]), "⛔음성: 기록의 β 가 다르면 대조 잡 same False")
        chk(refuses("kgy 시드", control, ctlA, ctlB, seeds=(11, 12), record=recp, read_run=ctl_rr, card=card8, prov=prov_ok),
            "⛔음성: 대조 잡에 10-14 기록 밖 시드 (11 · 12 = 2 단계 런) → 거부 (읽지 않는다)")
        chk(refuses("kgy 시드", control, ctlA, ctlB, seeds=(1, 2), record=recp, read_run=ctl_rr, card=card8, prov=prov_ok),
            "⛔음성: 대조 잡에 gabia 시드 (2) → 거부")
        bad_root = td / "ctlB_bad"
        shutil.copytree(ctlB, bad_root)
        edit_json(bad_root / "seed3" / "T600" / "run_meta.json", lambda d: d.update(label="li2s3_B_s12_T600", seed=3012))
        chk(refuses("대조 잡 대상이 아니다", control, ctlA, bad_root, seeds=(1, 3), record=recp, read_run=ctl_rr, card=card8, prov=prov_ok),
            "⛔음성: 대조 잡 루트의 run_meta 라벨 · 난수가 10-14 대조 계가 아니다 (li2s3 런) → 거부 (읽지 않는다)")
        ctl_out = _write_new(td / "ctl.json", co)
        permit = {"근거": "시험", "by": "selftest", "EB_회신": "kb/reviews/eb.md", "대조_잡_출력": str(ctl_out), "대조_잡_sha256": _sha(ctl_out)}
        card8p = _st_card(td / "card8p.json", sha, defects, ["A", "B"], [11, 12], [600, 650], 3.0, permit=permit)
        cardRp = _st_card(td / "cardRp.json", sha, defects, ["A"], [12], [600], 100.0, permit=permit)
        rd_ok = lambda b, rr, **k: readout(b, WT, card=k.pop("card", card8p), decisions=dec, read_run=rr, prov=k.pop("prov", prov_ok),
                                           permit_repo=prepo, **k)
        allpass = fake_rr_for(lambda s, sd, T: {})

        # ── 판독 문지기 ──
        chk(refuses("판독 허가", readout, clone(b8), WT, card=card8, decisions=dec, read_run=allpass, prov=prov_ok, permit_repo=prepo),
            "⛔음성: 카드에 판독 허가가 없으면 판독하지 않는다")

        def permit_card(name, **over):
            pm = dict(permit, **over)
            return _st_card(td / name, sha, defects, ["A", "B"], [11, 12], [600, 650], 3.0, permit=pm)
        chk(refuses("EB_회신", rd_ok, clone(b8), allpass, card=permit_card("pc1.json", EB_회신="kb/reviews/없음.md")),
            "⛔음성: 판독 허가의 EB 회신 파일이 없으면 거부")
        chk(refuses("sha256", rd_ok, clone(b8), allpass, card=permit_card("pc2.json", 대조_잡_sha256="0" * 64)),
            "⛔음성: 대조 잡 출력 sha256 ≠ 허가 기록 → 거부")
        c_false = _write_new(td / "ctl_false.json", co2)
        chk(refuses("same", rd_ok, clone(b8), allpass, card=permit_card("pc3.json", 대조_잡_출력=str(c_false), 대조_잡_sha256=_sha(c_false))),
            "⛔음성: 대조 잡 same False → 판독 거부")
        c_old = _write_new(td / "ctl_oldtool.json", dict(co, provenance=dict(prov_ok, tool_sha16={**prov_ok["tool_sha16"], TOOL_FILES[0]: "0" * 16})))
        chk(refuses("도구 판", rd_ok, clone(b8), allpass, card=permit_card("pc4.json", 대조_잡_출력=str(c_old), 대조_잡_sha256=_sha(c_old))),
            "⛔음성: 대조 잡을 낸 도구 sha16 ≠ 지금 판 → 판독 거부")
        c_dirty = _write_new(td / "ctl_dirty.json", dict(co, provenance=dict(prov_ok, tree_clean=False)))
        chk(refuses("깨끗한", rd_ok, clone(b8), allpass, card=permit_card("pc5.json", 대조_잡_출력=str(c_dirty), 대조_잡_sha256=_sha(c_dirty))),
            "⛔음성: 대조 잡을 더러운 작업 트리에서 냈으면 판독 거부")
        chk(refuses("깨끗하지 않다", rd_ok, clone(b8), allpass, prov=dict(prov_ok, tree_clean=False, dirty_tracked=[" M x"])),
            "⛔음성: 도구 작업 트리가 깨끗하지 않으면 판독 거부")
        dec2 = td / "dec2.json"
        dec2.write_text(json.dumps({"decisions": [{"id": NEED_ACTIVE[0], "decision_state": "active"},
                                                  {"id": NEED_ACTIVE[1], "decision_state": "proposed"}]}))
        chk(refuses("active", readout, clone(b8), WT, card=card8p, decisions=dec2, read_run=allpass, prov=prov_ok, permit_repo=prepo),
            "⛔음성: 개정 결정이 active 가 아니면 판독하지 않는다")

        # ── 판독 (가짜 read_run — 판정 함수는 glass_v2_readout selftest 몫) ──
        bP = clone(b8)
        o = rd_ok(bP, allpass)
        tA11 = next(t for t in o["seed_table"] if (t["system"], t["seed"]) == ("A", 11))
        chk(o["status"] == "판독" and o["W"] == [600, 650] and o["cond550_eligible"] and o["branch"].startswith("잠정 — cond550 판독 전")
            and "_D_slope" not in json.dumps(o, default=str) and pathlib.Path(o["out_path"]).is_file()
            and all(r["records"].get("ⓐ_first_frame_SS_pairs") is not None for r in o["rows"])
            and tA11["defect_label"]["S_S_lt_cut"] is True and tA11["per_T"]["600"]["records_summary"]["ⓐ_n_pairs_first"] == 1
            and o["provenance"]["tool_sha16"] == prov_ok["tool_sha16"] and o["base_original"] == str(b8),
            "[양성] 판독: 전부 측정 가능 → W [600, 650] · cond550 자격 · 갈래 '잠정 — cond550 판독 전' · D 값 없음 · 기록 ⓐ–ⓒ · "
            "기술표 (S–S 표지 · 요약) · 출처 · 고정 경로")
        L_ = o["layers"]
        chk(L_["생성_후보군"]["n"] == 6 and L_["포함_가능군"]["n"] == 5 and "A13" in L_["포함_가능군"]["제외"]
            and L_["2단계_시드_중_포함_가능군_밖"] == [] and L_["최종_측정가능_온도별"]["B_T650"]["측정가능"] == ["B11", "B12"],
            "[양성] 세 층 수를 카드 기록에서 센다 (생성 6 · 포함 5 — A13 최단 원자간 ≤ 2.0 Å 제외 · 2 단계 시드는 포함 가능군 안)")
        chk(refuses("이미 있다", rd_ok, bP, allpass), "⛔음성: 판독은 한 번 — 고정 출력 경로가 있으면 거부 (덮지 않는다)")
        o2 = rd_ok(clone(b8), fake_rr_for(lambda s, sd, T: {"C2": "경계 · 구분 불가"} if (s, sd, T) == ("B", 12, 650) else {}))
        chk(o2["W"] == [600] and o2["measurable"]["B_T650"] is False and o2["measurable"]["A_T650"],
            "⛔음성: B 시드 하나가 650 K 에서 경계 → 650 K 는 W 에 못 든다 (두 시드 모두 · 두 계 모두)")
        o3 = rd_ok(clone(b8), fake_rr_for(lambda s, sd, T: {"S_moved": 1} if (s, sd, T) == ("B", 12, 650) else {}))
        r3 = next(r for r in o3["rows"] if (r["system"], r["seed"], r["T_K"]) == ("B", 12, 650))
        chk(o3["W"] == [600] and r3["counts_in_N"] and not r3["measurable"] and r3["exclusion"] == "골격 이동",
            "⛔음성: C1 · C2 는 통과했지만 골격 이동 (S 소속 1) → 측정 가능 아님 · 사유 '골격 이동' (변이 in_R_set→counts_in_N 을 잡는다)")
        o4 = rd_ok(clone(b8), fake_rr_for(lambda s, sd, T: {"fw_missing": True} if (s, sd, T) == ("A", 11, 600) else {}))
        r4 = next(r for r in o4["rows"] if (r["system"], r["seed"], r["T_K"]) == ("A", 11, 600))
        chk(o4["W"] == [650] and r4["exclusion"] == "골격 못 잼" and not o4["cond550_eligible"] and not o4["branch"].startswith("잠정"),
            "⛔음성: 골격을 못 쟀으면 '골격 못 잼' (이동과 갈라 적는다) · 측정 가능 아님 · cond550 자격 없음 · 갈래 확정")
        o5 = rd_ok(clone(b8), fake_rr_for(lambda s, sd, T: {"C2": "미통과"} if (s, T) == ("B", 600) else {}))
        chk(o5["W"] == [650] and o5["measurable"]["A_T600"] and not o5["measurable"]["B_T600"] and o5["cond550_eligible"] is False,
            "⛔음성: 600 K 에서 A 만 측정 가능 · B 는 아님 → cond550 자격 없음 (변이 all→any 를 잡는다)")
        o6 = rd_ok(clone(b8), fake_rr_for(lambda s, sd, T: {"C1": False} if T == 600 else {}))
        chk(o6["W"] == [650] and not o6["cond550_eligible"] and o6["branch"] == "Ea 차 없음 · R 만 그 온도에서 (축소 3 단계 · 사용자 결정)",
            "⛔음성: 600 K 가 두 계 모두 측정 불가 → cond550 자격 없음 · 갈래 확정 (잠정 표지 없음)")

        # ── 판정 보류 (검증이 다 안 끝났거나 실패하면 W 를 내지 않는다) ──
        def hold_case(label, mutate):
            b = clone(b8)
            mutate(b)
            oh = rd_ok(b, allpass)
            chk(oh["status"] == "판정 보류" and "W" not in oh and "cond550_eligible" not in oh and "branch" not in oh
                and pathlib.Path(oh["hold_path"]).is_file() and not (b / OUT_DIRNAME / READOUT_NAME).exists(),
                f"⛔음성: {label} → 판정 보류 (W · 갈래 · cond550 없음 · 보류 기록만 · 판독 한 번을 쓰지 않는다)")
        hold_case("B12 650 K 가 아직 정리 중 (msd.json 있음 · 러너 끝 줄 없음)", lambda b: edit_text(b / "B" / "queue_kgy.log",
                  lambda t: "\n".join(ln for ln in t.splitlines() if "✅ T650 seed12 끝" not in ln and "■ 큐 끝 · 650:12:" not in ln)))
        hold_case("A11 600 K 드라이버 rc 7 (검증 실패 — W 밖으로 세지 않는다)", lambda b: edit_text(b / "A" / "queue_kgy.log",
                  lambda t: t.replace("✅ T600 seed11 끝 (rc 0)", "✅ T600 seed11 끝 (rc 7)")))
        hold_case("큐 끝 줄 없음 (큐가 멈췄다 · 다시 띄우지 않는다)", lambda b: edit_text(b / "stage2_kgy.log",
                  lambda t: "\n".join(ln for ln in t.splitlines() if "■ 큐 끝 · PHASE ladder" not in ln)))
        hold_case("B11 650 K msd.json 없음 (끝나지 않은 런)", lambda b: (
            (tdir_of(b, "B", 11, 650) / "msd.json").unlink(),
            edit_text(b / "B" / "queue_kgy.log", lambda t: "\n".join(ln for ln in t.splitlines() if "✅ T650 seed11 끝" not in ln)))[0])
        hold_case("사다리 블록 뒤의 v1 호출 (리뷰 EE P2-6 — 런은 valid · 따로 보류 사유)", lambda b: edit_text(b / "stage2_kgy.log", lambda t: t + LATE))

        # ── 카드 개정 4 (2026-11-14 · 결과 전): 큐 끝 줄 유실 인정 ──
        def lost_end(b=None):
            b = clone(b8) if b is None else b
            edit_text(b / "stage2_kgy.log", lambda t: "".join(ln + "\n" for ln in t.splitlines() if LADDER_END not in ln))
            return b

        def ack_for(b, last=None, did="D-ACK"):
            ls = (b / "stage2_kgy.log").read_text(encoding="utf-8").splitlines()
            s0_ = next(i for i, ln in enumerate(ls) if LADDER_START in ln)
            last = last if last is not None else next(ls[i] for i in range(len(ls) - 1, s0_ - 1, -1) if ls[i].strip())
            L_ = next(i for i in range(s0_, len(ls)) if ls[i] == last)
            return {"결정": did, "by": "selftest", "근거": "시험 — 큐 끝 줄이 파일에 안 남음", "사다리_블록_마지막_줄": last,
                    "사다리_블록_sha256": _block_sha(ls[s0_:L_ + 1]), "장부_sha256": _sha(b / "cost_ledger.tsv")}

        dec_ack = td / "dec_ack.json"
        dec_ack.write_text(json.dumps({"decisions": [{"id": i, "decision_state": "active"} for i in (*NEED_ACTIVE, "D-ACK")]
                                       + [{"id": "D-ACK-P", "decision_state": "proposed"}]}))
        n_ack = [0]

        def rd_ack(b, ack, **k):
            n_ack[0] += 1
            c_ = _st_card(td / f"card_ack{n_ack[0]}.json", sha, defects, ["A", "B"], [11, 12], [600, 650], 3.0,
                          permit=dict(permit, **{ENDLINE_ACK_KEY: ack}))
            return readout(b, WT, card=c_, decisions=k.pop("decisions", dec_ack), read_run=allpass, prov=prov_ok, permit_repo=prepo, **k)

        def hold_ack(label, b, ack):
            o = rd_ack(b, ack)
            chk(o.get("status") == "판정 보류" and "W" not in o and not (b / OUT_DIRNAME / READOUT_NAME).exists()
                and any(str(q).startswith("끝 줄 유실 인정") for q in (o.get("queue_problems") or [])),
                f"⛔음성: (개정 4) {label} → 판정 보류 (큐 문제 '끝 줄 유실 인정: …' · 판독 한 번을 안 쓴다)")

        def edit_ledger(b, fn):
            edit_text(b / "cost_ledger.tsv", lambda t: "".join(r + "\n" for r in fn(t.splitlines())))

        def set_col(rows, i, col, val):
            r = rows[i].split("\t")
            r[col] = val(r[col]) if callable(val) else val
            rows[i] = "\t".join(r)
            return rows

        bA = lost_end()
        ackA = ack_for(bA)
        oA = rd_ack(bA, ackA)
        elA = (oA.get("queue") or {}).get("end_line") or {}
        chk(oA.get("status") == "판독" and "W" in oA and oA["queue"]["status"] == "valid" and elA.get("kind") == "끝 줄 유실 인정"
            and elA.get("결정") == "D-ACK" and elA.get("사다리_블록_sha256") == ackA["사다리_블록_sha256"]
            and (oA.get("decisions") or {}).get("D-ACK") == "active" and (bA / OUT_DIRNAME / READOUT_NAME).is_file(),
            "[양성] (개정 4) 끝 줄 유실 + 인정 (블록 · 장부 sha256 · 명단 · rc 0 · 시간 · 잠금 · 결정 active) → 판독 · 출력에 인정 · 결정 기록")
        fA = endline_facts(lost_end(), cv8)
        chk(fA["problems"] == [] and fA.get("사다리_블록_sha256") == ackA["사다리_블록_sha256"] and fA.get("장부_sha256") == ackA["장부_sha256"]
            and fA.get("사다리_블록_마지막_줄") == ackA["사다리_블록_마지막_줄"],
            "[양성] (개정 4) endline_facts — 인정에 넣을 사실 (마지막 줄 · 블록 · 장부 sha256) = 인정 검사가 받는 값 · 문제 0 (읽기만)")
        chk(any("끝 줄이 있다" in q for q in endline_facts(clone(b8), cv8)["problems"]),
            "⛔음성: (개정 4) endline_facts — 큐 로그에 끝 줄이 있으면 '인정이 필요 없다' 로 찍는다")

        def tail_space(t):
            ls = t.splitlines()
            i = next(i for i, ln in enumerate(ls) if LADDER_START in ln)
            ls[i] += " "
            return "".join(ln + "\n" for ln in ls)
        b = lost_end(); ack = ack_for(b)
        edit_text(b / "stage2_kgy.log", tail_space)
        hold_ack("인정 뒤 큐 로그가 바뀜 (사다리 블록 sha256 ≠ 인정 · 파서는 그대로 읽는다)", b, ack)
        b = lost_end(); ack = ack_for(b)
        edit_ledger(b, lambda rows: set_col(rows, 1, 4, lambda v: v[:-1] + ("1" if v[-1] != "1" else "2")))
        hold_ack("인정 뒤 장부가 바뀜 (장부 sha256 ≠ 인정 · 행 꼴 · rc · 시간은 그대로)", b, ack)
        b = lost_end()
        edit_text(b / "stage2_kgy.log", lambda t: t + "[2026-11-14 00:00:00] (메모 줄)\n")
        hold_ack("인정한 마지막 줄이 명단 마지막 런의 큐 ✅ 줄이 아니다 (뒤에 다른 줄 · 블록 ✅ 는 명단 그대로)", b, ack_for(b))

        def dup_done(t):
            ls = t.splitlines()
            i = [j for j, ln in enumerate(ls) if QUEUE_DONE_RE.match(ln)][2]
            ls.insert(i + 1, ls[i])
            return "".join(ln + "\n" for ln in ls)
        b = lost_end()
        edit_text(b / "stage2_kgy.log", dup_done)
        hold_ack("사다리 블록의 큐 ✅ 줄이 명단과 다르다 (가운데 한 줄 두 번 · 마지막 줄은 그대로)", b, ack_for(b))
        b = lost_end()
        edit_ledger(b, lambda rows: rows[:3] + rows[4:])
        hold_ack("장부 행이 명단보다 하나 적다", b, ack_for(b))
        b = lost_end()
        edit_ledger(b, lambda rows: set_col(rows, 2, 7, "1"))
        hold_ack("장부 한 행의 rc ≠ 0", b, ack_for(b))
        b = lost_end()
        edit_ledger(b, lambda rows: set_col(rows, 2, 3, "4"))
        hold_ack("장부 한 행의 prod ≠ 카드", b, ack_for(b))
        b = lost_end()
        edit_ledger(b, lambda rows: set_col(rows, 2, 6, lambda v: f"{float(v) + 0.0001:.4f}"))
        hold_ack("장부 한 행의 시간 ≠ 그 런의 큐 ✅ 줄 시간", b, ack_for(b))
        b = lost_end(); ack = ack_for(b)
        edit_text(b / "stage2_kgy.log", lambda t: t + ack["사다리_블록_마지막_줄"] + "\n")
        hold_ack("인정한 마지막 줄이 사다리 시작 뒤에 두 번", b, ack)
        hold_ack("인정이 있는데 큐 로그에 끝 줄이 있다 (인정 뒤에 로그가 바뀌었다)", clone(b8), ack_for(lost_end()))
        import fcntl as _fc
        b = lost_end(); ack = ack_for(b)
        (b / ".stage2.lock").touch()
        fdl = os.open(str(b / ".stage2.lock"), os.O_RDONLY)
        _fc.flock(fdl, _fc.LOCK_EX)
        try:
            chk(refuses("큐 잠금", rd_ack, b, ack) and not (b / OUT_DIRNAME / READOUT_NAME).exists(),
                "⛔음성: (개정 4) 큐 잠금이 쥐어져 있으면 인정이 서지 않는다 → 판독 안 함 (보류 기록도 안 쓰고 거부)")
        finally:
            _fc.flock(fdl, _fc.LOCK_UN)
            os.close(fdl)
        b = lost_end()
        chk(refuses("큐_끝_줄_유실_인정", rd_ack, b, dict(ack_for(b), by="")) and not (b / OUT_DIRNAME / READOUT_NAME).exists(),
            "⛔음성: (개정 4) 인정 필드가 비었다 (by) → 판독 허가가 서지 않는다 (거부)")
        chk(refuses("'큐_끝_줄_유실_인정' 결정", rd_ack, b, ack_for(b, did="D-ACK-P")) and not (b / OUT_DIRNAME / READOUT_NAME).exists(),
            "⛔음성: (개정 4) 인정의 결정이 원장에서 proposed → 거부 (판독하지 않는다)")
        chk(refuses("'큐_끝_줄_유실_인정' 결정", rd_ack, b, ack_for(b, did="D-NONE")) and not (b / OUT_DIRNAME / READOUT_NAME).exists(),
            "⛔음성: (개정 4) 인정의 결정이 원장에 없다 → 거부")
        bHf = clone(b8)
        (tdir_of(bHf, "A", 12, 650) / "msd.json").unlink()
        edit_text(bHf / "A" / "queue_kgy.log", lambda t: "\n".join(ln for ln in t.splitlines() if "✅ T650 seed12 끝" not in ln))
        oHf = rd_ok(bHf, allpass)
        hfA = (oHf.get("runs") or {}).get("A12_T650", {})
        chk(oHf["status"] == "판정 보류" and hfA.get("fingerprint") == run_fingerprint(bHf / "A" / "seed12" / "T650", 650)
            and hfA["fingerprint"]["d0.00_cfg0/T650/msd.json"] is None and len(oHf["runs"]) == 8
            and all(set(v["fingerprint"]) == set(fp_rels(int(k.split("_T")[1]))) for k, v in oHf["runs"].items()),
            "[양성] (리뷰 EE P1-1) 보류 기록은 런마다 그때 본 지문 (산출물 7 + v2 시작 · 끝 기록 · 없으면 null) 을 싣는다 — 재실행은 지금 지문 = 이 지문일 때만")
        bHl = clone(bHf)
        import fcntl
        fdh = os.open(str(bHl / ".stage2.lock"), os.O_RDWR | os.O_CREAT, 0o644)
        fcntl.flock(fdh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            n_hold0 = len(list((bHl / OUT_DIRNAME).glob("hold_*.json")))
            refused_lock = refuses("잠금", rd_ok, bHl, allpass)
        finally:
            fcntl.flock(fdh, fcntl.LOCK_UN)
            os.close(fdh)
        chk(refused_lock and len(list((bHl / OUT_DIRNAME).glob("hold_*.json"))) == n_hold0,
            "⛔음성 (리뷰 EE P1-1 · p8): 큐 잠금이 쥐어져 있으면 (v1 이 도는 중) 판독은 보류 기록을 쓰지 않고 거부한다 — 상태 보기는 verify")

        # ── 실제 read_run 한 번 (100 ps 실제 체인 런 · 판정 함수 무변경 경로) ──
        oR = readout(bR, WT, card=cardRp, decisions=dec, prov=prov_ok, permit_repo=prepo, n_boot=40)
        rR = oR["rows"][0] if oR.get("rows") else {}
        chk(oR["status"] == "판독" and not rR.get("error") and rR.get("C2_final") is not None
            and (rR.get("skeleton") or {}).get("pass") is not None and oR["W"] == ([600] if rR["measurable"] else []),
            f"[양성] 실제 read_run (C1 · C2 · 골격) 이 실제 드라이버 100 ps 런을 읽는다 — C2 {rR.get('C2_final')} · 측정 가능 {rR.get('measurable')}")

        # ── 압력 ──
        class StrictCalc:
            """가짜 turbo 계산기 — 처음 본 조성과 다른 조성을 받으면 죽는다 (merge_mole 흉내) · σ = −p₀·I."""
            implemented_properties = ["energy", "forces", "stress"]

            def __init__(self, p0=0.01):
                self.p0, self.comp, self._mq_mode = p0, None, "turbo"

            def _c(self, atoms):
                s = np.asarray(atoms.get_chemical_symbols())
                comp = tuple(sorted((e, int((s == e).sum())) for e in set(s.tolist())))
                if self.comp is None:
                    self.comp = comp
                elif self.comp != comp:
                    raise AssertionError("가짜 turbo: 다른 조성")

            def get_stress(self, atoms=None, voigt=False):
                self._c(atoms)
                return -self.p0 * np.eye(3)

            def get_property(self, name, atoms=None, allow_calculation=True):
                return self.get_stress(atoms)

            def get_potential_energy(self, atoms=None, force_consistent=False):
                return 0.0
        made = []
        fac = lambda s: made.append(s) or StrictCalc()
        bZ = clone(b8)
        chk(refuses("판독 허가", pressure, bZ, WT, card=card8, decisions=dec, calc_factory=fac, prov=prov_ok, permit_repo=prepo),
            "⛔음성: 카드에 판독 허가가 없으면 압력도 내지 않는다")
        chk(refuses("깨끗하지 않다", pressure, bZ, WT, card=card8p, decisions=dec, calc_factory=fac,
                    prov=dict(prov_ok, tree_clean=False), permit_repo=prepo),
            "⛔음성: 도구 작업 트리가 깨끗하지 않으면 압력도 거부")
        try:
            pz = pressure(bZ, WT, card=card8p, decisions=dec, calc_factory=fac, prov=prov_ok, permit_repo=prepo)
            err = None
        except (Exception, SystemExit) as e:
            pz, err = {}, f"{type(e).__name__}: {e}"
        a12 = read(str(tdir_of(b8, "A", 12, 600) / "traj.xyz"), index=0)
        pk = 120 * KB_EV * 600 / a12.get_volume() * mq.EV_A3_TO_GPA
        rA12 = json.loads((bZ / OUT_DIRNAME / PRESSURE_RUNS / "A12_T600.json").read_text()) if not err else {}
        chk(err is None and pz.get("status") == "압력" and made == ["A", "B"] and len(list((bZ / OUT_DIRNAME / PRESSURE_RUNS).glob("*.json"))) == 8
            and [f["t_ps"] for f in rA12.get("frames", [])] == [1.0, 2.0, 3.0] and [f["k"] for f in rA12["frames"]] == [9, 19, 29]
            and abs(rA12["mean_GPa"] - (0.01 * mq.EV_A3_TO_GPA + pk)) < 1e-9 and pz["per_T"]["600"]["A_minus_B_GPa"] is not None,
            f"[양성] 압력: 계마다 새 계산기 (조성 고정 가짜에서 안 죽는다) · 프레임 k = 9 · 19 · 29 (t = 1 · 2 · 3 ps) · "
            f"P = −tr σ/3 + N k_B T/V · 런마다 점진 저장 8 · 두 계 ⟨P⟩ 차 {err or ''}")
        chk(refuses("이미 있다", pressure, bZ, WT, card=card8p, decisions=dec, calc_factory=fac, prov=prov_ok, permit_repo=prepo),
            "⛔음성: 압력 끝 기록이 있으면 거부 (한 번)")
        (bZ / OUT_DIRNAME / PRESSURE_NAME).unlink()
        made.clear()
        pz2 = pressure(bZ, WT, card=card8p, decisions=dec, calc_factory=fac, prov=prov_ok, permit_repo=prepo)
        chk(all(v.get("reused") for v in pz2["runs"].values()) and made == [],
            "[양성] 압력이 중간에 끊겼다 다시 돌면 같은 궤적 · 같은 도구 판의 런별 기록을 다시 쓴다 (계산기를 안 만든다)")
        (bZ / OUT_DIRNAME / PRESSURE_NAME).unlink()
        edit_json(bZ / OUT_DIRNAME / PRESSURE_RUNS / "B11_T650.json", lambda d: d.__setitem__("traj_sha256", "0" * 64))
        chk(refuses("완료 기록이 아니다", pressure, bZ, WT, card=card8p, decisions=dec, calc_factory=fac, prov=prov_ok, permit_repo=prepo),
            "⛔음성: 런별 압력 기록이 다른 궤적의 것이면 거부 (다시 쓰지 않는다)")
        one = StrictCalc()
        try:
            run_pressure(tdir_of(b8, "A", 11, 600), 600, 120, 3.0, 100.0, one, mq.EV_A3_TO_GPA)
            run_pressure(tdir_of(b8, "B", 11, 600), 600, 120, 3.0, 100.0, one, mq.EV_A3_TO_GPA)
            died = False
        except AssertionError:
            died = True
        chk(died, "⛔음성 (시험 장치 확인): 계산기 하나를 A · B 두 조성에 쓰면 조성 고정 가짜가 죽는다 — 압력 도구가 계마다 새로 만드는 이유")
        bH = clone(b8)
        (tdir_of(bH, "A", 12, 650) / "msd.json").unlink()
        edit_text(bH / "A" / "queue_kgy.log", lambda t: "\n".join(ln for ln in t.splitlines() if "✅ T650 seed12 끝" not in ln))
        made.clear()
        ph = pressure(bH, WT, card=card8p, decisions=dec, calc_factory=fac, prov=prov_ok, permit_repo=prepo)
        chk(ph["status"] == "판정 보류" and made == [] and not (bH / OUT_DIRNAME / PRESSURE_RUNS).exists(),
            "⛔음성: 끝나지 않은 런이 하나라도 있으면 압력을 내지 않는다 (판정 보류 · 계산기도 안 만든다)")
        bHp = clone(bH)
        fdp = os.open(str(bHp / ".stage2.lock"), os.O_RDWR | os.O_CREAT, 0o644)
        fcntl.flock(fdp, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            nHp0 = len(list((bHp / OUT_DIRNAME).glob("hold_*.json")))
            refusedP = refuses("잠금", pressure, bHp, WT, card=card8p, decisions=dec, calc_factory=fac, prov=prov_ok, permit_repo=prepo)
        finally:
            fcntl.flock(fdp, fcntl.LOCK_UN)
            os.close(fdp)
        chk(refusedP and len(list((bHp / OUT_DIRNAME).glob("hold_*.json"))) == nHp0 and made == [],
            "⛔음성 (리뷰 EE P1-1): 큐 잠금이 쥐어져 있으면 압력도 보류 기록을 쓰지 않고 거부한다")
        chk(abs(run_pressure(tdir_of(b8, "A", 12, 600), 600, 120, 3.0, 100.0, StrictCalc(p0=float("nan")), mq.EV_A3_TO_GPA)["n"] - 3) == 0
            and run_pressure(tdir_of(b8, "A", 12, 600), 600, 120, 3.0, 100.0, StrictCalc(p0=float("nan")), mq.EV_A3_TO_GPA)["status"].startswith("압력 못 냄"),
            "⛔음성: 비유한 응력 → '압력 못 냄' (0 이 아니다)")
        chk(refuses("궤적 프레임", run_pressure, tdir_of(b8, "A", 12, 600), 600, 120, 4.0, 100.0, StrictCalc(), mq.EV_A3_TO_GPA),
            "⛔음성: 궤적 프레임 수 ≠ 계획 → 압력 안 냄")

        # ── v2 큐 런 — 실제 v2 큐 (run_stage2_kgy_v2.sh) → 실제 드라이버 · 실행 기록으로 결속 (VERIFY_MAP) ──
        #    흐름 = 카드 순서: 사다리 판독 보류 → PHASE=rerun (보류 기록 결속) → 섞인 사다리 판독 → PHASE=cond550 (판독 결속) → cond550 판독
        QD = "D-TEST-queue-v2"
        v2x = {"conditional": {"T_K": 550, "prod_ps": 6.0, "when": "selftest"}, "cap_gpu_h": 160.0, "first_run_max_h": 8.0,
               "gpu_start_max_mib": 6000, "cost_estimate_h_per_ps": 0.0001,
               "queue_v2": {"sha16": _sha(REPO / QUEUE_V2_REL)[:16], "decision": QD}}
        card8v = _st_card(td / "card8v.json", sha, defects, ["A", "B"], [11, 12], [600, 650], 3.0, permit=permit, extra=v2x)
        cv8v = card_values(card8v)
        decv = td / "decv.json"
        decv.write_text(json.dumps({"decisions": [{"id": i, "decision_state": "active"} for i in NEED_ACTIVE + (QD,)]}))
        rd_v = lambda b, rr, **k: readout(b, WT, card=k.pop("card", card8v), decisions=k.pop("decisions", decv), read_run=rr,
                                          prov=k.pop("prov", prov_ok), permit_repo=prepo, **k)
        o1v = readout(clone(b8), WT, card=card8v, decisions=dec, read_run=allpass, prov=prov_ok, permit_repo=prepo)
        chk(o1v["status"] == "판독" and o1v["ready"]["mixed"] is False and "decisions_queue_v2" not in o1v,
            "[양성] v1 런만이면 v2 기계 값 · queue_v2 결정을 안 본다 (v1 판 그대로 · 결정 파일에 queue_v2 결정이 없어도)")
        bW = clone(b8)
        edit_text(bW / "A" / "queue_kgy.log", lambda t: t.replace("✅ T600 seed11 끝 (rc 0)", "✅ T600 seed11 끝 (rc 7)"))
        ohW = rd_v(bW, allpass)
        hp = pathlib.Path(ohW.get("hold_path") or (td / "없음"))
        chk(ohW["status"] == "판정 보류" and ohW["runs"]["A11_T600"]["status"] == "invalid" and ohW["phase"] == "ladder"
            and ohW["ready"]["mixed"] is False and hp.is_file()
            and ohW["runs"]["A11_T600"]["fingerprint"] == run_fingerprint(bW / "A" / "seed11" / "T600", 600),
            "[v2 준비] v1 런 하나 (A11 600 K) 가 rc 7 → 사다리 판독 보류 기록 (v1 판 그대로 · phase ladder · 런 지문)")
        rcq, lgq = _st_q2(td, bW, card8v, decv, "rerun", RERUN="A:11:600", HOLD_RECORD=str(hp),
                          HOLD_SHA256=_sha(hp) if hp.is_file() else "")
        sup = sorted((bW / "A" / "seed11").glob("T600.superseded_*"))
        vW = verify_run(bW, "A", 11, 600, cv8v, WT)
        chk(rcq == 0 and len(sup) == 1 and vW["status"] == "valid" and vW["queue_version"] == "v2" and vW["runner_rc"] == 0
            and vW["phase_v2"] == "rerun" and vW["link"]["kind"] == "hold" and "장부 행 일치" in vW["cost_source"]
            and vW["cost_h"] is not None and vW["superseded"]["rel"] == str(sup[0].relative_to(bW)),
            f"[양성 v2] 실제 v2 큐 PHASE=rerun (보류 기록 결속) → 옛 폴더 옮겨 남김 · 새 런이 실행 기록으로 valid (①–⑦ · 비용 = 끝 기록 "
            f"gpu_h · 장부 행 일치) — 종료 {rcq} · {vW['status']} {'; '.join(vW['reasons'])[:160]}")
        if rcq != 0:
            print(lgq[-2500:])
        mod_ = sys.modules[__name__]
        mod_.ALLOW_TEST_RUNS = False
        vWt = verify_run(bW, "A", 11, 600, cv8v, WT)
        mod_.ALLOW_TEST_RUNS = True
        chk(vWt["status"] == "invalid" and any("시험 런" in q for q in vWt["reasons"]) and vW.get("test_run") is True,
            "⛔음성 (리뷰 EE P1-2): 시험 런 (V2_TEST=1 · 시험 카드 · 원장) 은 판독이 받지 않는다 (판독 selftest 밖에서는 invalid)")
        oW = rd_v(bW, allpass)
        rW = next((r for r in oW.get("rows", []) if (r["system"], r["seed"], r["T_K"]) == ("A", 11, 600)), {})
        led_sum = round(sum(float(ln.split("\t")[6]) for ln in (bW / "cost_ledger.tsv").read_text().splitlines()[1:] if ln.strip()), 6)
        chk(oW["status"] == "판독" and oW["W"] == [600, 650] and oW["cond550_eligible"] and oW["branch_provisional"]
            and oW["ready"]["mixed"] is True and oW["ready"]["lock_free"] is True and oW["ready"]["v2_runs"] == ["A11_T600"]
            and oW["phase"] == "ladder" and oW["verify_map"] == VERIFY_MAP and rW.get("verify", {}).get("queue_version") == "v2"
            and oW["decisions_queue_v2"] == {QD: "active"},
            "[양성 v2] 섞인 사다리 판독 (v1 7 · v2 1) — 대응표 · 잠금 비어 있음 · queue_v2 결정 active · W [600, 650] · cond550 자격 (갈래 잠정)")
        chk(oW.get("rules_sha256") == cv8v["rules_sha256"] and rW.get("fingerprint", {}).get("run_id") == vW.get("run_id")
            and all(r["fingerprint"]["files"] == run_fingerprint(bW / r["system"] / f"seed{r['seed']}" / f"T{r['T_K']}", r["T_K"]) for r in oW["rows"])
            and all(r["fingerprint"]["runner_start"] for r in oW["rows"] if r["fingerprint"]["queue_version"] == "v1")
            and oW.get("ledger_total_h") == led_sum and oW["cost_h_total"] is not None,
            f"[양성] (리뷰 EE P1-1 · P2-5) 사다리 판독 행에 런 지문 (v2 run_id · v1 러너 블록 시작 · 파일 sha256) · 출력에 카드 기계_판독_값 해시 · "
            f"장부 합계 {oW.get('ledger_total_h')} h (= 장부 {led_sum})")
        bWpre = clone(bW)                                   # cond550 전 사본 — 저장소 카드 · 원장으로 도는 생산 경로 시험용
        rcc, lgc = _st_q2(td, bW, card8v, decv, "cond550", READOUT_RECORD=str(oW.get("out_path", "")),
                          READOUT_SHA256=_sha(oW["out_path"]) if oW.get("out_path") else "")
        if rcc != 0:
            print(lgc[-2500:])
        bW0 = clone(bW)                                     # cond550 판독 전 사본 — 음성 · 잠금 · 보류 시험은 여기서 뜬다
        _, runsC = verify_all(bW, cv8v, WT, phase="cond550")
        v550 = [runsC.get((s_, sd, 550), {}) for sd in (11, 12) for s_ in ("A", "B")]
        chk(rcc == 0 and len(runsC) == 12 and all(v["status"] == "valid" for v in runsC.values())
            and all(v.get("queue_version") == "v2" and v.get("phase_v2") == "cond550" and (v.get("link") or {}).get("kind") == "readout"
                    for v in v550) and all(v.get("trajectory", {}).get("n_frames_read") == 60 for v in v550),
            f"[양성 v2] 실제 v2 큐 PHASE=cond550 (사다리 판독 결속) → 550 K · 6 ps (= conditional.prod) 4 런 · 60 프레임 · 12 런 모두 valid "
            f"— 종료 {rcc} · {sorted({v['status'] for v in runsC.values()})}")
        for k_, v_ in runsC.items():
            if v_["status"] != "valid":
                print(f"     {k_}: {v_['status']} — {'; '.join(v_['reasons'])[:240]}")
        oC = rd_v(bW, allpass, phase="cond550")
        chk(oC["status"] == "판독" and oC["phase"] == "cond550" and oC["W"] == [550, 600, 650] and oC["branch_provisional"] is False
            and oC["branch"] == "3 단계 후보 = W 의 가장 낮은 셋 → 사용자 결정 (상한 포함)" and len(oC["rows"]) == 12
            and oC["measurable"]["A_T550"] is True and "A_T550" in oC["layers"]["최종_측정가능_온도별"]
            and oC["ladder_readout"]["sha256"] == _sha(oW["out_path"]) and pathlib.Path(oC["out_path"]).name == OUT_NAMES["cond550"][0]
            and oC["cost_h_total"] is not None and oC["ready"]["mixed"] is True,
            "[양성 v2] cond550 판독 ('끝난 뒤 한 번 더'): 550 + 사다리 → W [550, 600, 650] · 갈래 확정 (잠정 아님) · 사다리 판독 결속 · 고정 경로")
        chk(refuses("이미 있다", rd_v, bW, allpass, phase="cond550"), "⛔음성: cond550 판독도 한 번 (고정 출력 경로가 있으면 거부)")
        oC2 = rd_v(clone(bW0), fake_rr_for(lambda s, sd, T: {"C2": "미통과"} if (s, sd, T) == ("B", 12, 550) else {}), phase="cond550")
        chk(oC2["W"] == [600, 650] and oC2["measurable"]["B_T550"] is False and not oC2["branch_provisional"],
            "⛔음성: cond550 판독에서 B12 550 K 미통과 → 550 K 는 W 밖 · W [600, 650] (갈래 확정)")
        made.clear()
        try:
            pC = pressure(bW, WT, card=card8v, decisions=decv, calc_factory=fac, prov=prov_ok, permit_repo=prepo, phase="cond550")
            rA550 = json.loads((bW / OUT_DIRNAME / f"{PRESSURE_RUNS}_cond550" / "A11_T550.json").read_text())
            errC = None
        except (Exception, SystemExit) as e:
            pC, rA550, errC = {}, {"frames": []}, f"{type(e).__name__}: {e}"
        chk(errC is None and pC.get("status") == "압력" and made == ["A", "B"]
            and len(list((bW / OUT_DIRNAME / f"{PRESSURE_RUNS}_cond550").glob("*.json"))) == 12
            and [f["k"] for f in rA550["frames"]] == [9, 19, 29, 39, 49, 59] and rA550["frames"][-1]["t_ps"] == 6.0
            and set(pC["per_T"]) == {"550", "600", "650"} and pathlib.Path(pC["out_path"]).name == OUT_NAMES["cond550"][1]
            and not (bW / OUT_DIRNAME / PRESSURE_RUNS).exists(),
            f"[양성 v2] cond550 압력: 550 K 런은 conditional.prod (6 ps → k = 9 … 59) · 런별 기록 pressure_runs_cond550/ (사다리와 "
            f"안 섞임) · 고정 경로 {errC or ''}")

        # ── cond550 판독의 동결 (리뷰 EE P1-1 · RM1) — 사다리 판독 고정 기록과 같은 런 지문 · 도구 sha16 · 기계_판독_값 일 때만 ──
        def lad_edit(b, fn):
            p_ = b / OUT_DIRNAME / READOUT_NAME
            d_ = json.loads(p_.read_text(encoding="utf-8"))
            fn(d_)
            p_.write_text(json.dumps(d_, ensure_ascii=False), encoding="utf-8")
        bF1 = clone(bW0)
        aj = tdir_of(bF1, "B", 12, 650) / "aimd_results.json"
        aj.write_text(aj.read_text() + "\n")                          # 값은 같고 바이트만 — 그 런은 여전히 valid · 지문은 바뀐다
        chk(verify_run(bF1, "B", 12, 650, cv8v, WT)["status"] == "valid" and refuses("지문", rd_v, bF1, allpass, phase="cond550"),
            "⛔음성 (리뷰 EE P1-1 · p1): 사다리 판독 뒤 사다리 런이 바뀌면 (그 런은 valid 라도) cond550 판독을 하지 않는다 (런 지문 ≠)")
        bF2 = clone(bW0)
        lad_edit(bF2, lambda d: d["provenance"].__setitem__("tool_sha16", {**d["provenance"]["tool_sha16"], TOOL_FILES[0]: "0" * 16}))
        chk(refuses("판독 도구 sha16", rd_v, bF2, allpass, phase="cond550"),
            "⛔음성 (리뷰 EE P1-1): 사다리 판독을 낸 도구 sha16 ≠ 지금 → cond550 판독을 하지 않는다")
        cardRule = td / "card8v_rule.json"
        cr_ = json.loads(card8v.read_text(encoding="utf-8"))
        cr_["기계_판독_값"]["stage2"]["mean_T_tol_frac"] = 0.06
        cardRule.write_text(json.dumps(cr_, ensure_ascii=False), encoding="utf-8")
        chk(refuses("기계_판독_값", rd_v, clone(bW0), allpass, phase="cond550", card=cardRule),
            "⛔음성 (리뷰 EE P1-1): 사다리 판독 뒤 카드 판독 규칙 값 (기계_판독_값) 이 바뀌면 cond550 판독을 하지 않는다")
        bF4 = clone(bW0)
        lad_edit(bF4, lambda d: d.__setitem__("cond550_eligible", False))
        chk(refuses("자격", rd_v, bF4, allpass, phase="cond550"), "⛔음성 (리뷰 EE RM1): 사다리 판독이 cond550 자격 없음 → cond550 판독 거부")
        bF5 = clone(bW0)
        lad_edit(bF5, lambda d: [r.pop("fingerprint", None) for r in d["rows"]])
        chk(refuses("지문", rd_v, bF5, allpass, phase="cond550"), "⛔음성: 런 지문이 없는 (옛 도구) 사다리 판독 → cond550 판독 거부")
        bF6 = clone(bW0)
        aj6 = tdir_of(bF6, "A", 12, 600) / "aimd_results.json"
        aj6.write_text(aj6.read_text() + "\n")
        made.clear()
        chk(refuses("지문", pressure, bF6, WT, card=card8v, decisions=decv, calc_factory=fac, prov=prov_ok, permit_repo=prepo, phase="cond550")
            and made == [], "⛔음성 (리뷰 EE P1-1): cond550 압력도 사다리 판독에 동결된다 — 사다리 런이 바뀌면 거부 (계산기도 안 만든다)")
        # ── 저장소 카드 · 원장으로 돈 v2 런 (생산 경로 · 리뷰 EE P1-2) — 임시 git 저장소의 v2 큐 사본 · 그 커밋으로 결속 ──
        groot, Gg = _st_git_root(td, {QUEUE_V2_REL: REPO / QUEUE_V2_REL, WT_FILES["md_driver"]: REPO / WT_FILES["md_driver"],
                                      CARD_REL: card8v, DECISIONS_REL: decv})
        bPr = clone(bWpre)
        fixed_pr = bPr / OUT_DIRNAME / READOUT_NAME
        fixed_pr.unlink()                                             # 사본의 사다리 판독은 그 BASE 의 것으로 다시 낸다 (결속 기록은 BASE 마다)
        oLp = rd_v(bPr, allpass)
        rcP, lgP = _st_q2(td, bPr, groot / CARD_REL, groot / DECISIONS_REL, "cond550", test=False, script=groot / QUEUE_V2_REL,
                          READOUT_RECORD=str(fixed_pr), READOUT_SHA256=_sha(fixed_pr) if fixed_pr.is_file() else "")
        if rcP != 0:
            print(lgP[-2500:])
        headG = subprocess.run(["git", "-C", str(groot), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        mod_.V2_REPO = groot
        vP = [verify_run(bPr, s_, sd, 550, cv8v, WT) for sd in (11, 12) for s_ in ("A", "B")]
        chk(oLp["status"] == "판독" and rcP == 0 and all(v["status"] == "valid" and v.get("test_run") is False and v.get("repo_head") == headG
                                                     for v in vP),
            f"[양성] (리뷰 EE P1-2) 저장소 카드 · 원장 (그 커밋) 으로 돈 v2 런 — 시작 기록 test false · repo HEAD · 그 커밋의 카드 · 원장 sha256 · "
            f"결정 active → valid (종료 {rcP} · {[v['status'] for v in vP]} {'; '.join(r for v in vP for r in v['reasons'])[:200]})")
        oPr = rd_v(bPr, allpass, phase="cond550")
        chk(oPr["status"] == "판독" and oPr["W"] == [550, 600, 650], "[양성] 생산 경로 v2 런으로 cond550 판독 (사다리 판독 동결 통과)")

        def negP(label, edit, kw, repo=None):
            b_ = clone(bPr)
            p_ = b_ / "A" / "seed11" / "T550" / V2_START
            d_ = json.loads(p_.read_text(encoding="utf-8"))
            edit(d_)
            p_.write_text(json.dumps(d_, ensure_ascii=False), encoding="utf-8")
            mod_.V2_REPO = repo or groot
            v_ = verify_run(b_, "A", 11, 550, cv8v, WT)
            mod_.V2_REPO = groot
            chk(v_["status"] == "invalid" and any(kw in q for q in v_["reasons"]),
                f"⛔음성 (리뷰 EE P1-2): {label} → invalid ({'; '.join(v_['reasons'])[:120]})")
            shutil.rmtree(b_, ignore_errors=True)
        negP("그 커밋을 판독 저장소에서 못 찾는다", lambda d: None, "못 찾는다", repo=td / "no_such_repo")
        negP("시작 기록 repo HEAD 없음", lambda d: d.__setitem__("repo_head", None), "repo HEAD")
        negP("시작 기록 card_sha256 ≠ 그 커밋의 카드", lambda d: d.__setitem__("card_sha256", "0" * 64), "카드 sha256")
        negP("시작 기록 card_is_repo_card false (환경변수 카드)", lambda d: d.__setitem__("card_is_repo_card", False), "card_is_repo_card")
        negP("시작 기록 repo_clean false (HEAD 와 다른 파일)", lambda d: d.__setitem__("repo_clean", False), "repo_clean")
        dprop = json.loads(decv.read_text())
        dprop["decisions"] = [dict(e, decision_state="proposed") if e["id"] == QD else e for e in dprop["decisions"]]
        (groot / DECISIONS_REL).write_text(json.dumps(dprop))
        subprocess.run(Gg + ["commit", "-q", "-am", "queue_v2 결정 proposed"], check=True, capture_output=True)
        headG2 = subprocess.run(["git", "-C", str(groot), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        negP("그 커밋 원장에서 queue_v2 결정이 proposed", lambda d: d.update(repo_head=headG2, decisions_sha256=_sha(groot / DECISIONS_REL)),
             "active 가 아니다")
        mod_.ALLOW_TEST_RUNS = True
        mod_.V2_REPO = REPO

        def rdir_of(b, s_, sd, T):
            return b / s_ / f"seed{sd}" / f"T{T}"
        S0 = lambda b, s_="A", sd=11, T=550: rdir_of(b, s_, sd, T) / V2_START
        E0 = lambda b, s_="A", sd=11, T=550: rdir_of(b, s_, sd, T) / V2_END

        def neg2(label, mutate, kw, want="invalid", s_="A", sd=11, T=550, cv=None, wt=None):
            b = clone(bW0)
            mutate(b)
            v = verify_run(b, s_, sd, T, cv or cv8v, wt or WT)
            chk(v["status"] == want and v.get("queue_version") == "v2" and any(kw in q for q in v["reasons"]),
                f"⛔음성 (v2): {label} → {want} ({'; '.join(v['reasons'])[:110]})")
            shutil.rmtree(b, ignore_errors=True)            # 사본이 커서 (12 런) 바로 지운다 — 디스크가 좁은 기계에서도 돈다
        neg2("끝 기록 뒤 ensemble_results 에 키 하나 더 (②–⑤ 는 못 보는 변경)", lambda b: edit_json(
            rdir_of(b, "A", 11, 550) / "ensemble_results.json", lambda d: d.__setitem__("note", "x")), "산출물이 바뀌었")
        neg2("끝 기록 없음 (드라이버가 아직 돈다 · 끊겼다)", lambda b: E0(b).unlink(), "끝 기록이 없다", want="incomplete")
        neg2("끝 기록 status failed", lambda b: edit_json(E0(b), lambda d: d.__setitem__("status", "failed")), "끝 기록 상태")
        neg2("끝 기록 driver_rc 1 (status 는 complete)", lambda b: edit_json(E0(b), lambda d: d.__setitem__("driver_rc", 1)), "종료 코드 1")
        neg2("끝 기록 run_id ≠ 시작 기록", lambda b: edit_json(E0(b), lambda d: d.__setitem__("run_id", "0" * 32)), "run_id")
        neg2("시작 기록 큐 sha16 ≠ 카드 (다른 큐 판)", lambda b: edit_json(S0(b), lambda d: d.__setitem__("queue_v2_sha16", "0" * 16)),
             "다른 큐 판")
        neg2("카드 queue_v2.sha16 ≠ 실행 기록", lambda b: None, "다른 큐 판", cv=dict(cv8v, queue_v2_sha16="1" * 16))
        neg2("카드에 queue_v2 가 없다", lambda b: None, "queue_v2.sha16 이 없다", cv=dict(cv8v, queue_v2_sha16=None))
        neg2("시작 기록 드라이버 sha16 ≠ 카드", lambda b: edit_json(S0(b), lambda d: d.__setitem__("driver_sha16", "7cbd8c3701892dc6")),
             "다른 드라이버")
        neg2("시작 기록 queue_v2 결정 proposed (실행 때)", lambda b: edit_json(S0(b), lambda d: d["decisions"].__setitem__(QD, "proposed")),
             "결정 상태")
        neg2("시작 기록 카드 결정 proposed (실행 때)", lambda b: edit_json(S0(b), lambda d: d["decisions"].__setitem__(NEED_ACTIVE[0], "proposed")),
             "결정 상태")
        neg2("시작 기록 카드 값 prod 3 (550 K 를 사다리 길이로)", lambda b: edit_json(S0(b), lambda d: d["card_values"].__setitem__("prod_ps", 3.0)),
             "카드 값")
        neg2("시작 기록 명령 인수 friction 0.05", lambda b: edit_json(S0(b), lambda d: d["argv"].__setitem__(d["argv"].index("--friction") + 1,
                                                                                                   "0.05")), "명령 인수")
        neg2("시작 기록 입력 sha256 ≠ 카드 (실행 직전 해시)", lambda b: edit_json(S0(b), lambda d: d.__setitem__("input_sha256", "0" * 64)),
             "입력 sha256")
        neg2("시작 기록 phase ladder (v2 는 cond550 · rerun 만)", lambda b: edit_json(S0(b), lambda d: d.__setitem__("phase", "ladder")), "phase")
        neg2("시작 기록의 계 ≠ 폴더", lambda b: edit_json(S0(b), lambda d: d.__setitem__("system", "B")), "꼴 · 런")
        neg2("시작 기록 깨짐", lambda b: S0(b).write_text("{broken"), "시작 기록을 못 읽었다")
        neg2("cond550 런의 결속 kind hold", lambda b: edit_json(S0(b), lambda d: d["link"].__setitem__("kind", "hold")),
             "readout 결속 기록이 없다")

        def moved_link(b, tamper=False):
            edit_json(S0(b), lambda d: d["link"].__setitem__("path", "/nonexistent/readout_stage2.json"))
            if tamper:
                edit_text(b / OUT_DIRNAME / READOUT_NAME, lambda t: t + " ")
        bMv = clone(bW0)
        moved_link(bMv)
        vMv = verify_run(bMv, "A", 11, 550, cv8v, WT)
        chk(vMv["status"] == "valid", f"[양성 v2] 옮긴 BASE — 결속 판독 기록을 실행 기록의 rel_to_base 로 지금 BASE 에서 찾는다 "
                                      f"({'; '.join(vMv['reasons'])[:120]})")
        neg2("옮긴 BASE 의 결속 판독 기록이 결속 뒤 바뀜", lambda b: moved_link(b, tamper=True), "결속 기록 sha256")

        def other_base_link(b):
            d = json.loads((b / OUT_DIRNAME / READOUT_NAME).read_text(encoding="utf-8"))
            d.update(base_original="/other/base", base_now="/other/base")
            p = b / "other_readout.json"
            p.write_text(json.dumps(d), encoding="utf-8")
            edit_json(S0(b), lambda x: x.__setitem__("link", dict(x["link"], path=str(p), sha256=_sha(p), rel_to_base=None)))
        neg2("결속 판독 기록이 다른 BASE 의 것", other_base_link, "이 런의 BASE")

        def altered_link(b, **over):
            d = json.loads((b / OUT_DIRNAME / READOUT_NAME).read_text(encoding="utf-8"))
            d.update(over)
            p = b / f"altered_{len(over)}_{sorted(over)[0]}.json"
            p.write_text(json.dumps(d), encoding="utf-8")
            edit_json(S0(b), lambda x: x.__setitem__("link", dict(x["link"], path=str(p), sha256=_sha(p), rel_to_base=None)))
        neg2("결속 판독 기록이 cond550 자격 없음 (sha 는 맞는 다른 기록)", lambda b: altered_link(b, cond550_eligible=False),
             "측정 가능을 보이지 않는다")
        neg2("결속 판독 기록이 cond550 갈래 판독 (사다리 판독이 아니다)", lambda b: altered_link(b, phase="cond550"), "사다리 판독")

        def copy_link(b):
            p_ = b / OUT_DIRNAME / "copy_of_ladder.json"
            p_.write_bytes((b / OUT_DIRNAME / READOUT_NAME).read_bytes())
            edit_json(S0(b), lambda x: x.__setitem__("link", dict(x["link"], path=str(p_), rel_to_base=f"{OUT_DIRNAME}/copy_of_ladder.json")))
        neg2("결속 판독 기록이 같은 내용 · 다른 경로의 사본 (리뷰 EE P2-1)", copy_link, "고정 기록")
        neg2("사본 BASE 의 사다리 판독 고정 기록이 결속 뒤 바뀜 (원래 BASE 의 기록은 그대로 · 리뷰 EE P2-1)",
             lambda b: edit_text(b / OUT_DIRNAME / READOUT_NAME, lambda t: t + " "), "지금 사다리 판독 고정 기록")

        def hold_valid_link(b):
            d = json.loads(hp.read_text(encoding="utf-8"))
            d["runs"]["A11_T600"]["status"] = "valid"
            p = b / "hold_valid.json"
            p.write_text(json.dumps(d), encoding="utf-8")
            edit_json(S0(b, "A", 11, 600), lambda x: x.__setitem__("link", dict(x["link"], path=str(p), sha256=_sha(p), rel_to_base=None)))
        neg2("재실행 런의 결속 보류 기록이 그 런을 valid 로 적음", hold_valid_link, "invalid · incomplete 로 적지 않았다", T=600)
        neg2("재실행 런의 결속 보류 기록 sha256 ≠ 실행 기록", lambda b: edit_json(S0(b, "A", 11, 600),
             lambda x: x["link"].__setitem__("sha256", "0" * 64)), "결속 기록 sha256", T=600)
        neg2("run_meta prod 3 (550 K 는 conditional.prod 6)", lambda b: edit_json(rdir_of(b, "A", 11, 550) / "run_meta.json",
             lambda d: d.__setitem__("prod_ps", 3.0)), "run_meta prod_ps")
        neg2("550 K 궤적 프레임 하나 모자람 (계획 60)", lambda b: rewrite_traj(tdir_of(b, "A", 11, 550) / "traj.xyz", lambda fr: fr[:-1]),
             "계획 60")

        def resealed(b, rel, fn, s_="A", sd=11, T=550):
            """산출물을 바꾸고 끝 기록 outputs_sha256 도 맞춘다 (큐가 잘못 봉인한 경우) — 판독은 큐의 완료 판정을 믿지 않고 ②–⑤ 를 다시 본다."""
            p = rdir_of(b, s_, sd, T) / rel
            fn(p)
            edit_json(E0(b, s_, sd, T), lambda d: d["outputs_sha256"].__setitem__(rel, _sha(p)))

        def shift_cfg(p):
            a = read(str(p)); q = a.positions.copy(); q[0, 0] += 0.5; a.positions = q; write(str(p), a, format="extxyz")
        neg2("ensemble_results task oc20 · 끝 기록 sha 도 맞춤 (큐 판정을 믿지 않는다)", lambda b: resealed(b, "ensemble_results.json",
             lambda p: edit_json(p, lambda d: d.__setitem__("uma_task", "oc20"))), "ensemble_results uma_task")
        neg2("config.xyz ≠ init · 끝 기록 sha 도 맞춤", lambda b: resealed(b, "d0.00_cfg0/config.xyz", shift_cfg), "시작 구조")
        neg2("msd.json MTO NaN · 끝 기록 sha 도 맞춤", lambda b: resealed(b, "d0.00_cfg0/T550/msd.json",
             lambda p: edit_json(p, lambda d: d["msd_Li_A2_mto"].__setitem__(0, float("nan")))), "MTO")
        bad_wt2 = td / "wt_bad_q2"
        for key, rel in WT_FILES.items():
            (bad_wt2 / rel).parent.mkdir(parents=True, exist_ok=True)
            (bad_wt2 / rel).write_bytes(b"other queue" if key == "queue_v2" else (REPO / rel).read_bytes())
        neg2("판독 시점 worktree 의 v2 큐 파일 sha16 ≠ 카드 (⑦)", lambda b: None, "판독 시점 worktree", wt=bad_wt2)
        vv1 = verify_run(clone(b8, "B", 11, 600), "B", 11, 600, cv8, bad_wt2)
        chk(vv1["status"] == "valid", "[양성] v1 런은 worktree 의 v2 큐 파일을 안 본다 (v1 판 그대로)")
        # ── 섞인 판독의 판정 보류 (VERIFY_MAP 마지막 줄) · cond550 문지기 ──
        import fcntl
        bLk = clone(bW0)
        fdl = os.open(str(bLk / ".stage2.lock"), os.O_RDWR | os.O_CREAT, 0o644)
        fcntl.flock(fdl, fcntl.LOCK_EX | fcntl.LOCK_NB)
        nLk0 = len(list((bLk / OUT_DIRNAME).glob("hold_*.json")))
        try:
            refusedLk = refuses("잠금", rd_v, bLk, allpass, phase="cond550")
        finally:
            fcntl.flock(fdl, fcntl.LOCK_UN)
            os.close(fdl)
        chk(refusedLk and len(list((bLk / OUT_DIRNAME).glob("hold_*.json"))) == nLk0 and not (bLk / OUT_DIRNAME / OUT_NAMES["cond550"][0]).exists(),
            "⛔음성 (리뷰 EE P1-1 · p8): 섞인 판독인데 큐 잠금이 쥐어져 있다 (큐 · 드라이버가 돈다) → 거부 · 판정 보류 기록도 안 쓴다")
        bNE = clone(bW0)
        edit_text(bNE / "stage2_kgy.log", lambda t: "\n".join(ln for ln in t.splitlines() if "■ 큐 끝 · PHASE ladder" not in ln))
        oNE = rd_v(bNE, allpass, phase="cond550")
        chk(oNE["status"] == "판독" and oNE["ready"]["queue_status"] == "incomplete" and oNE["W"] == [550, 600, 650],
            "[양성] 섞인 판독은 v1 큐 끝 줄을 요구하지 않는다 (v1 이 멈춘 뒤 v2 가 남은 런을 돈 경우 — 잠금 비어 있음 · 대응표 마지막 줄)")
        bQP = clone(bW0)
        edit_text(bQP / "stage2_kgy.log", dup_start_inside)
        oQP = rd_v(bQP, allpass, phase="cond550")
        chk(oQP["status"] == "판정 보류" and any("v1 큐 로그에 문제" in w for w in oQP["ready"]["why"]),
            "⛔음성: 섞인 판독 · v1 큐 로그에 문제 (사다리 블록 안 시작 줄 둘) → 판정 보류")
        bLI = clone(bW0)
        edit_text(bLI / "stage2_kgy.log", lambda t: t + LATE)
        oLI = rd_v(bLI, allpass, phase="cond550")
        chk(oLI["status"] == "판정 보류" and any("사다리 블록 밖" in w for w in oLI["ready"]["why"])
            and all(v["status"] == "valid" for v in oLI["runs"].values()) and any("사다리 블록 밖" in w for w in oLI["hold_reasons"]),
            "⛔음성 (리뷰 EE P2-6): 섞인 판독 · 사다리 블록 뒤의 v1 호출 → 런은 모두 valid 인 채 따로 보류 사유 (보류 기록 hold_reasons)")
        bSt = clone(bW0)                                    # 멈춤 기록 꼴 = v2 큐가 쓰는 꼴 (큐 selftest 가 실제 멈춤 · 풂을 시험한다)
        stop_ln = json.dumps({"type": "stop", "id": "st0000000001", "code": 21, "phase": "cond550", "run": "B12_T550",
                              "reason": "이 갈래의 첫 런 … > 한도 (시험)"}, ensure_ascii=False)
        (bSt / "queue_v2_stops.jsonl").write_text(stop_ln + "\n", encoding="utf-8")
        oSt = rd_v(bSt, allpass, phase="cond550")
        chk(oSt["status"] == "판정 보류" and any("풀리지 않은 v2 멈춤" in w for w in oSt["ready"]["why"]) and "W" not in oSt,
            "⛔음성: 런은 모두 valid 인데 풀리지 않은 v2 멈춤 (첫 런 한도) → 판정 보류 (멈추고 보고 · 사람이 풀기 전에는 읽지 않는다)")
        (bSt / "queue_v2_stops.jsonl").write_text(stop_ln + "\n" + json.dumps({"type": "ack", "id": "st0000000001"}) + "\n", encoding="utf-8")
        oSh = rd_v(bSt, allpass, phase="cond550")
        chk(oSh["status"] == "판정 보류" and any("풀리지 않은 v2 멈춤" in w for w in oSh["ready"]["why"])
            and oSh["ready"]["v2_queue_records"]["acks_without_by_reason"] == ["st0000000001"],
            "⛔음성 (리뷰 EE P2-2): 손으로 적은 풂 줄 (by · reason 없음) 은 풂이 아니다 → 판정 보류")
        (bSt / "queue_v2_stops.jsonl").write_text(stop_ln + "\n" + json.dumps({"type": "ack", "id": "st0000000001", "by": "selftest",
                                                                                "reason": "시험"}) + "\n", encoding="utf-8")
        oSa = rd_v(bSt, allpass, phase="cond550")
        chk(oSa["status"] == "판독" and oSa["ready"]["v2_queue_records"]["acks"][0]["by"] == "selftest",
            "[양성] 같은 멈춤을 사람이 풀었으면 (ack · by · 사유) 판독 — 멈춤 · 풂 기록을 출력에 싣는다")
        bSb = clone(bW0)
        (bSb / "queue_v2_stops.jsonl").write_text("{broken\n", encoding="utf-8")
        oSb = rd_v(bSb, allpass, phase="cond550")
        chk(oSb["status"] == "판정 보류" and any("못 읽었다" in w for w in oSb["ready"]["why"]),
            "⛔음성: v2 멈춤 기록이 깨졌으면 판정 보류 (멈춤이 없다로 읽지 않는다)")
        bNR = clone(bW0)
        (bNR / OUT_DIRNAME / READOUT_NAME).unlink()
        chk(refuses("사다리 판독 고정 기록", rd_v, bNR, allpass, phase="cond550"), "⛔음성: 사다리 판독 고정 기록이 없으면 cond550 판독 거부")
        bNI = clone(bW0)
        E0(bNI, "B", 12, 550).unlink()
        oNI = rd_v(bNI, allpass, phase="cond550")
        chk(oNI["status"] == "판정 보류" and oNI["runs"]["B12_T550"]["status"] == "incomplete" and oNI["phase"] == "cond550"
            and oNI["kind"] == "li2s3_stage2_readout_hold/v2",
            "⛔음성: cond550 런 하나가 끝 기록 없음 → cond550 판독 보류 (보류 기록 phase cond550 · PHASE=rerun 결속에 쓸 수 있는 꼴)")
        chk(refuses("conditional", rd_v, clone(bW0), allpass, phase="cond550", card=card8p),
            "⛔음성: 카드에 stage2.conditional 이 없으면 cond550 판독 거부")
        decp = td / "decp.json"
        decp.write_text(json.dumps({"decisions": [{"id": i, "decision_state": "active"} for i in NEED_ACTIVE]
                                    + [{"id": QD, "decision_state": "proposed"}]}))
        chk(refuses("queue_v2 결정", rd_v, clone(bW0), allpass, phase="cond550", decisions=decp),
            "⛔음성: v2 런이 있는데 queue_v2 결정이 지금 active 가 아니면 판독 거부")
        chk(refuses("판독 갈래", rd_v, clone(bW0), allpass, phase="ladder2"), "⛔음성: 모르는 판독 갈래 → 거부")

        # ── 명령줄 (종료 코드 · 덮지 않기) — 모듈 전역 CARD · DECISIONS 를 잠깐 시험 카드로 ──
        SELF = sys.modules[__name__]
        saved = (SELF.CARD, SELF.DECISIONS, SELF.readout)
        try:
            SELF.CARD, SELF.DECISIONS = card8, dec
            vout = td / "verify_cli.json"
            rc1 = main(["verify", "--base", str(b8), "--worktree", str(WT), "--out", str(vout)])
            vj = json.loads(vout.read_text(encoding="utf-8"))
            rc2 = main(["verify", "--base", str(b8), "--worktree", str(WT), "--out", str(vout)])
            chk(rc1 == 0 and vj["kind"] == "li2s3_stage2_verify/v2" and vj["판독_가능_상태"] is True and len(vj["runs"]) == 8
                and "provenance" in vj and rc2 == EXIT_REFUSED,
                "[양성] 명령줄 verify: 종료 0 · 출처 기록 · 판독 가능 상태 · 같은 --out 이면 거부 (종료 2)")
            rc3 = main(["readout", "--base", str(clone(b8)), "--worktree", str(WT)])
            SELF.readout = lambda *a, **k: {"status": "판정 보류", "n_runs_not_valid": 1, "queue_status": "valid", "hold_path": "x"}
            rc4 = main(["readout", "--base", str(b8), "--worktree", str(WT)])
            chk(rc3 == EXIT_REFUSED and rc4 == EXIT_HOLD, f"⛔음성: 명령줄 readout — 허가 없음 → 종료 2 · 판정 보류 → 종료 3 ({rc3} · {rc4})")
            SELF.CARD = card8v
            vout2 = td / "verify_cli_cond550.json"
            rc5 = main(["verify", "--base", str(bW0), "--worktree", str(WT), "--out", str(vout2), "--phase", "cond550"])
            vj2 = json.loads(vout2.read_text(encoding="utf-8")) if vout2.is_file() else {}
            chk(rc5 == 0 and vj2.get("phase") == "cond550" and len(vj2.get("runs", [])) == 12 and vj2.get("판독_가능_상태") is True
                and vj2["ready"]["mixed"] is True and vj2["verify_map"] == VERIFY_MAP
                and sum(1 for r in vj2["runs"] if r.get("queue_version") == "v2") == 5,
                "[양성] 명령줄 verify --phase cond550: v1 · v2 런을 함께 (12 런 · v2 5) · 대응표 · 판독 가능 상태")
        finally:
            SELF.CARD, SELF.DECISIONS, SELF.readout = saved
    print(f"selftest {'PASS' if not fails else 'FAIL'} — {n_ok}/{n_ok + len(fails)} ({time.time() - t0:.0f} s)")
    return 0 if not fails else 1


def main(argv=None):
    if argv is None and "--selftest" in sys.argv[1:]:
        return _selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    pv = sub.add_parser("verify")
    pv.add_argument("--base", required=True); pv.add_argument("--worktree", required=True); pv.add_argument("--out", required=True)
    pr = sub.add_parser("readout")
    pr.add_argument("--base", required=True); pr.add_argument("--worktree", required=True)
    pz = sub.add_parser("pressure")
    pz.add_argument("--base", required=True); pz.add_argument("--worktree", required=True); pz.add_argument("--device", default="cuda")
    for p_ in (pv, pr, pz):
        p_.add_argument("--phase", choices=sorted(OUT_NAMES), default="ladder",
                        help="ladder = 사다리 16 런 (기본) · cond550 = 조건부 550 K + 사다리 ('끝난 뒤 한 번 더')")
    pc = sub.add_parser("control")
    pc.add_argument("--root_a", required=True); pc.add_argument("--root_b", required=True)
    pc.add_argument("--seeds", type=int, nargs="+", default=[1, 3]); pc.add_argument("--out", required=True)
    pf = sub.add_parser("endline_facts", help="읽기만 — 큐 끝 줄이 없을 때 카드 인정에 넣을 사실 (카드 개정 4)")
    pf.add_argument("--base", required=True)
    A = ap.parse_args(argv)
    try:
        if A.cmd == "verify":
            if pathlib.Path(A.out).exists():
                raise Refused(f"⛔ {A.out} 가 이미 있다 — 덮지 않는다")
            cv, prov = card_values(CARD), provenance(REPO)
            qrec, runs = verify_all(A.base, cv, A.worktree, phase=A.phase)
            print(f"큐: {qrec['status']}" + (f" — {'; '.join(qrec['problems'])[:200]}" if qrec["problems"] else ""))
            el = qrec.get("end_line") or {}
            if el.get("kind") == "끝 줄 유실 인정":
                did = el.get("결정")
                dst = decision_states(DECISIONS, ids=(did,)).get(did) if isinstance(did, str) else None
                print(f"큐 끝 줄: 유실 인정 · 결정 {did} (원장 {dst!r}) · 블록 끝 {el.get('마지막_줄_번호')} 번째 줄")
            for (s, sd, T), v in runs.items():
                print(f"{s}{sd} T{T} ({v.get('queue_version')}): {v['status']}" + (f" — {'; '.join(v['reasons'])[:160]}" if v["reasons"] else ""))
            ready, rinfo = ready_state(A.base, qrec, runs)
            out = {"kind": "li2s3_stage2_verify/v2", "card_sha256": cv["card_sha256"], "provenance": prov, "phase": A.phase,
                   "queue": {k: qrec.get(k) for k in ("status", "complete", "start", "gatekeep", "versions", "repo_head", "base_original", "problems",
                                                      "other_invocations", "end_line")},
                   "worktree_code": worktree_code(A.worktree), "runs": [_public(v) for v in runs.values()], "판독_가능_상태": ready,
                   "ready": rinfo, "verify_map": VERIFY_MAP,
                   "⚠": "사후 검증만 — 수송 · 골격 값은 안 읽었다 · 판독 가능 상태 = 계획 런이 모두 끝 · 모두 valid · "
                        "v1 런만이면 큐 로그 valid · 큐 끝 줄 · v2 런이 있으면 큐 잠금 비어 있음 (VERIFY_MAP 마지막 줄)"}
            _write_new(A.out, out)
            print(f"판독 가능 상태: {'예' if ready else '아니오 (판정 보류 사유가 남아 있다)'} -> {A.out}")
            return 0
        if A.cmd == "endline_facts":
            o = endline_facts(A.base, card_values(CARD))
            print(json.dumps(o, ensure_ascii=False, indent=1))
            return 0 if o["problems"] == [] else 1
        if A.cmd == "readout":
            o = readout(A.base, A.worktree, card=CARD, decisions=DECISIONS, permit_repo=REPO, phase=A.phase)
            if o["status"] == "판정 보류":
                print(f"판정 보류 — 끝나지 않았거나 검증 실패 런 {o['n_runs_not_valid']} 개 · 큐 {o['queue_status']} -> {o['hold_path']}")
                return EXIT_HOLD
            print(f"[{A.phase}] W = {o['W']} · {o['branch']} · cond550 자격 {o['cond550_eligible']} -> {o['out_path']}")
            return 0
        if A.cmd == "pressure":
            o = pressure(A.base, A.worktree, card=CARD, decisions=DECISIONS, device=A.device, permit_repo=REPO, phase=A.phase)
            if o["status"] == "판정 보류":
                print(f"판정 보류 — 끝나지 않았거나 검증 실패 런 {o['n_runs_not_valid']} 개 · 큐 {o['queue_status']} -> {o['hold_path']}")
                return EXIT_HOLD
            for T, v in o["per_T"].items():
                print(f"T{T}: ⟨P⟩ {v['mean_by_system_GPa']} · A − B {v['A_minus_B_GPa']} · 경고 {v['warn_gt_1GPa']}")
            print(f"-> {o['out_path']}")
            return 0
        if pathlib.Path(A.out).exists():
            raise Refused(f"⛔ {A.out} 가 이미 있다 — 덮지 않는다")
        o = control(A.root_a, A.root_b, tuple(A.seeds), card=CARD)
        _write_new(A.out, o)
        print(f"대조 잡: same = {o.get('same')} · {o.get('status') or ''} · 차이 {len(o.get('diffs') or [])} 건 -> {A.out}")
        for d in (o.get("diffs") or [])[:10]:
            print("  ", d)
        return 0 if o.get("same") is True else 1
    except Refused as e:
        print(str(e), file=sys.stderr)
        return EXIT_REFUSED


if __name__ == "__main__":
    sys.exit(main())
