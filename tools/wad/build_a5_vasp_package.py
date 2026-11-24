#!/usr/bin/env python3
"""build_a5_vasp_package.py — W_ad V5 은 쪽 G4 ENCUT 650 분리 끝점 (V5_s_outer_A_G4_e70_far) 의 결과 뒤 재시도 a5 · 묶음 · 업체 러너 · 반송 검사.

    python3 tools/wad/build_a5_vasp_package.py --selftest
    python3 tools/wad/build_a5_vasp_package.py --mutants
    python3 tools/wad/build_a5_vasp_package.py --build --out db/inputs/wad_a5_vasp_2026_11_20
    python3 tools/wad/build_a5_vasp_package.py --check --out <묶음> --ret <a5_return.tgz 를 푼 곳> --manifest_sha256 <고정값> \
        --registry db/raw/wad_round2_vasp_2026_10_22/pp_registry_round2_2026_10_26.json --registry_sha256 999aa2da… [--a5_result <OUT_JSON>]

근거: 개정 5 v2 db/properties/wad_aprime_pilot_prereg_v5_amendment_5_e70_retry_2026_11_20.json (D-2026-11-20-wad-aprime-v5-e70-a5-retry · 비준 2026-11-20).
사다리 (개정 5 '사다리_a5'): ⓪ 보존된 a4 ⓐ WAVECAR 확인 (sha · 크기 · 머리 — 원본은 읽기만) → A5 (LDIPOL 끔 · ⓪ 이 확인되면 그 복사본에서 이어서 · 아니면 새로)
  → c1 (Davidson · MAXMIX 200 · AMIX 0.1 · AMIN 0.01 · NELM 400 · A5 끝 WAVECAR 복사본에서) → c1 이 주 기준 OK 가 아니면 c2 (ALGO All · TIME 0.1 · NELM 400 ·
  같은 시작 WAVECAR 의 새 복사본에서). A5 자격 미달이면 c1 · c2 는 ⓪ 복사본에서 · ⓪ 도 없으면 값 없음.
채택 (주 기준 → 보조 기준 · 순서 · 둘 다 보조 불일치 · u_W 판정) 은 **V5 수집기** (build_v5_vasp_package.py --a5_result) 에서 한다 —
  이 도구는 묶음을 만들고, 업체 러너를 쓰고, 반송을 검사해 시도별 상태와 보조 기준 숫자 (u_E · 창 두 개) 를 낸다.

왜 새 파일인가 (개정 5 '만들_것' 은 '외주 2차 도구의 러너·검사기에 a5 사다리를 더한다' 고 적었다): 외주 2차 도구는 2차 최종 반송의 재검사·재집계가
  저장본과 바이트 일치로 묶여 있어 고치지 않는다. 대신 그 도구의 공유 부품을 **가져다 쓴다** —
  · 파이썬: judge_text (SCF 판정 계약) · incar_val · semantic_diff · rung_text · restart_evidence · env_evidence · env_audit · outcar_dims · a_eligible ·
    far_diag · restart_regex_problems · _read · _read_raw (+ V5 의 parse_incar_strict · parse_outcar · parse_titel · dipol_evidence · verify_manifest)
  · 러너 bash: 2차 RUN_ALL 의 함수 본문을 이름으로 꺼낸다 (h · utc · up · log · clean · enc_eq · cap_num · secs_ok · incar_val · judge · alarms ·
    pack_fail · pack · finish · pp_ok · ver_of · wav_head · out_num · wsha + 성능 파일 · PACK_ONLY 블록). 끝 줄은 bash -n 이 정한다
    (첫 번째로 문법이 닫히는 줄 — 손으로 괄호를 세지 않는다). 바꾸는 것은 고유 이름 · 판정 입력 (행 머리 관문) · 반송 파일 이름 · 포장에서 점 폴더 빼기 ·
    끝 안내 8 뿐이고, 바꿀 자리가 정확히 한 번 (또는 정한 횟수) 나오지 않으면 만들지 않는다. A5 자격 (elig5) 은 2차 elig_A 를 쓰지 않고 a5 판으로 쓴다
    ('기록은 유효한데 파일이 사라짐 · 바뀜' 을 ⓪ 으로 넘기지 않고 1저자로).
  a5 에서 새로 쓰는 것: 단마다 OSZICAR 행 머리 관문 (A5 · c1 = DAV/RMM · c2 = SDA/CGA · 모르는 머리 = SCF_UNVERIFIED) · 사다리 · ⓪ 확인 ·
  A5 의 재시작 확인 (시작 복사본 sha + 문구만 — A5 는 LWAVE T 라 끝 WAVECAR 가 새로 써진다) · 누적 상한 하나 (180 h) · 보조 기준 숫자 · 반송 사다리 대조 ·
  설정 에코 관문 (echo5 — a5 가 바꾼 NELM · LDIPOL · IALGO · AMIX · AMIN · MAXMIX · TIME 의 OUTCAR 해석값 · 러너와 검사기가 같은 부분집합) ·
  Codex EO (11-23): 완전한 전자 반복행 (row_scan = row_gate) · 한 줄 기록 문법 REC1 (rec5 = rec_parse · 쓸 때 jstr 이스케이프) · attempt.start 폴더 대조 ·
  벽시계 출처 하나 (wall_of — 영수증 먼저) · --infra-wall a5 판 (REC1 로 다시 쓰고 채운 시각) · 중단 장부 ↔ 보존 폴더 (ledger5 = ledger_problems) · 끝 기록 시도 ID (att5 = attempts_of).
  Codex EP (11-23): 완전한 행 = 숫자로 읽히는 행 (칸 6 · 7 · N 양의 정수 · ncg 정수 · 실수 칸) · 콜론 앞에서 잘린 머리 = 손상 · 시간 출처는 보존 폴더의 영수증만 ·
  진행 폴더의 영수증 거부 · 시도 이력 (status.tsv run_id = hist5 = history_problems) · 끝난 시도의 끝 기록 신원 (end_id = end_problem) · 끝 기록 없는 반송 채택 안 함 ·
  다시 포장 · 다시 돌림 전 끝 기록 대조 (fin_ok) · 영수증 필수 칸 비면 거부 · 손으로 넣은 글은 쓸 때 UTF-8 확인 (u8ok) · 장부 줄 순서 = 기록 · 시작 시각 순서.
  Codex EQ (11-23 · 다섯 번째 NO-GO 뒤 구조로): **트리 관문 하나** (러너 tree5 · tree_gate = 검사기 tree_problems · 같은 규칙 · 같은 사유 낱말) 를 러너의 모든 진입점
  (기록 명령 · PACK_ONLY · 다시 돌림 · 단 발사 직전 · 포장 = 기존 반송본을 덮기 전) 에 건다 — 모르는 것 · 못 읽는 것 · 서로 안 맞는 것은 아무것도 쓰지 않고 종료 8:
  이름 (모르는 이름 · 잔여 *.part · 링크 · 하위 폴더) · 시작 기록 · 끝 기록 틀 (attempt.json = printf 그대로 · ATT1_TPL) · 신원 · 봉인 (sha 표 = 지금 파일) ·
  끊김 기록 (끝 기록과 함께 · 보존 폴더 · 문법 · 결속 · 빈칸) · 진행 폴더 영수증 · 장부 (단 순서 A5 ≤ c1 ≤ c2) · 이력 (0 바이트 · 잘린 줄) · 끝 기록 (code/state 조합) ·
  시작점 · ⓪ 기록 (W0_TPL) · 모든 기록 UTF-8 · 기존 반송본 ⊆ 지금 트리 (러너만). 쓰는 쪽: attempt.json · WAVECAR.info 는 임시 파일에 완성한 뒤 mv ·
  필수 칸은 빈칸 문자 (공백 · 탭 · LF · VT · FF · CR — 원문은 그 JSON 이스케이프까지) 만인 글도 거부 (쓸 때 · 읽을 때). 행 판독: 숫자 칸 길이 ≤ 24 (늘 유한) · 앞 빈칸을 걷은 머리 조각도 손상 (열 제목 'N' 만 0 스텝).
  Codex ER (11-23 · 같은 관문 위에): 준비 폴더 (run/.prep_*) 는 러너가 띄우기 전에 쓰는 이름만 (VASP 출력이 있으면 실행 기록 — 지우지 않고 멈춤) ·
  관문을 A5 WAVECAR 지우기 · 끝 기록 쓰기 전 (drop5 · fin5) 에도 · 0 스텝은 OSZICAR 가 빈 줄 · 열 제목 (끝 조각은 그 앞부분) 만일 때 (그 밖 → unexplained_line · 검토) ·
  이력 줄 벽시계 = 그 시도 끝 기록 elapsed_s (합산 전) · 계산 · 기록 명령 · PACK_ONLY 가 같은 배타 잠금 (검사부터 쓰기 끝까지) ·
  기존 반송본 대비 관측 사실 후퇴 거부 (완전한 행이 줄거나 확정된 영수증 벽시계가 바뀜 · UNKNOWN → 확정값만 · 러너) · 끝 기록 잡 · 변형 · stage = 시작 기록 · POTCAR 해시 = POTCAR.sha256.

개정 5 해석 1 (사용자 2026-11-20 · 1저자 · AskUserQuestion '멈추고 1저자에게 (Recommended)') — 러너와 검사기가 같은 갈래로 본다:
  다음 단은 지금 단이 SCF_NOT_CONVERGED 이거나 전자 반복행 ≥ 1 인 실행 실패 (행 ≥ 1 끊김을 --killed 로 기록한 것 포함) 로 끝났을 때만 ·
  전자 반복행 0 → 멈춤 (종료 7 · 다음 단을 쓰지 않는다 · --infra-abort 또는 연락) · RESTART_NOT_HONOURED · SCF_UNVERIFIED · 설정 · 무결성 → 멈춤 (종료 8 · 1저자 —
  개정 5 결과별_처리 '재시작_미이행 … 더 돌리지 않는다' · 개정 4 다음_단_자격) · A5 가 행은 있는데 자격 미달이면 개정 5 그대로 (⓪ 복사본 · 없으면 닫음).
  c1 보조 채택은 c2 가 확인된 끝 (SCF_NOT_CONVERGED · 행 ≥ 1 실행 실패 · 행 ≥ 1 끊김) 일 때만 — 아니면 LADDER_INCOMPLETE / STOPPED_FOR_REVIEW (주 세션 해석 · 보수).
  시작점은 첫 c 단을 띄울 때 run/start_point.json 에 한 번 두고 다시 정하지 않는다 · 끝 (0 · 1 · 5 상한 · 8 · 돈 뒤의 6 — VASP 빌드 다름) 은 run/final.json — 다시 돌려도 아무것도 띄우지 않는다.
  검사기 상태: OK · NO_PRIMARY_VALUE (수집기 채택 대상) · LADDER_INCOMPLETE · STOPPED_FOR_REVIEW · LADDER_VIOLATION · START_POINT_MISSING · START_POINT_MISMATCH ·
  W0_* · 무결성 · 환경 (채택 없음).

⛔ 이 도구가 못 하는 것:
   · VASP 를 돌리지 않는다 · 구조를 만들지 않는다 (V5 봉인 묶음의 sha 로 결박만) · SCF 판정은 OSZICAR · OUTCAR 기록만 본다 (해의 유일성 · 같은 바닥상태는 모른다)
   · c2 (ALGO All) 의 OSZICAR 행 머리 (SDA · CGA) 는 5.4.4 실물로 확인하지 않았다 — 첫 반송에서 확인한다. 다른 머리면 SCF_UNVERIFIED 로 멈춘다 (조용히 넘어가지 않는다)
   · 행 머리 관문은 줄 맨 앞 1–4 글자 + ':' 을 '행' 으로 본다 — 그 꼴이 아닌 실물 행은 2차 계약 (행 없음 → SCF_UNVERIFIED) 이 잡는다
   · 보조 기준의 u_E 는 창 두 개 (마지막 50 · 그 앞 50 스텝) 의 E 만 본다 — 창 밖으로 이어지는 느린 드리프트는 과소 평가할 수 있다 (개정 5 '한계')
   · u_W 문턱 (0.002 J/m²) · G4 판정 · 채택 순서는 이 도구가 아니라 V5 수집기가 그 면적으로 한다 (여기서 u_W 를 내지 않는다 — 면적이 두 곳에 있지 않게)
   · ⓪ 원본이 업체 서버에서 안 바뀌었는지는 sha · 크기 · 머리로만 본다 · 업체 작업 트리 전체를 감사하지 않는다 (반송물에 담긴 흔적만)
   · 이력 길이 (Broyden 고유값 개수) · rms(c) 급등은 정보다 — 판정에 쓰지 않는다 (설정 검사는 OUTCAR 의 MAXMIX · IALGO · TIME 해석값으로 따로 한다)
   · 러너의 설정 관문은 a5 가 바꾼 키 (echo5) 만 본다 — 나머지 설정 · D3 · POTCAR 등록부 · 완결성은 검사기만 본다 (러너는 이어 갔을 수 있다 ·
     검사기는 STOPPED_FOR_REVIEW 로 보고하고 c 단을 재시작 미이행으로 바꾸지 않는다)
   · 사다리 순서는 업체 노드 시계 (date +%s) 로 잰다 — 노드 사이 시계가 어긋나면 거짓 LADDER_VIOLATION 이 날 수 있다 (거짓 통과 쪽은 아니다)
   · 다른 기계의 잠금은 살아 있는지 알 수 없다 — 운영자가 스케줄러로 확인하고 --unlock 으로 지운다 (러너는 지우지 않는다)
   · 묶음 폴더 검사는 이름만 본다 (a5 가 아닌 항목 · 스케줄러 출력 꼴 *.o<번호> · *.e<번호> 는 둔다) — 파일 내용은 MANIFEST · 반송 검사기가 본다
   · 묶음 빌드 · 러너 함수 추출에는 bash 가 필요하다 (bash -n 으로 함수 끝을 정한다)
   · 완전한 전자 반복행 (Codex EO P0 · EP P0) 은 '다 쓰였고 숫자로 읽히는가' 만 본다 — 줄바꿈 · 그 단의 머리 그대로 · ':' 뒤 빈칸 · 칸 6 · 7 · N 양의 정수 ·
     ncg 정수 · 실수 칸 (지수 두 자리까지). 값이 물리적으로 맞는지 (스텝 번호가 이어지는지 · NELM · OUTCAR 대조) 는 판정 계약이 본다 · SDA/CGA 행의 칸 수는
     5.4.4 실물로 확인하지 않았다 (DAV 실물: 6 · 7 칸 — 칸이 다르면 손상 → 멈춤 8 · 채택 쪽으로는 안 틀린다) · 콜론 앞 머리 절단은 앞 빈칸을 걷은 글자 1–4 조각
     (Codex EQ — 앞 빈칸 뒤 'N' 만 열 제목으로 0 스텝 · 줄 맨 앞 'N' 은 손상) · 숫자 칸 길이 ≤ 24 (지수 두 자리와 함께 |x| < 1e119 — 실물 칸 ≤ 16 · 더 긴 칸은 손상)
   · 한 줄 기록 문법 REC1 (Codex EO P1) 의 값 비교는 원문 (이스케이프를 풀지 않은 글) 으로 한다 — 같은 값을 \\u 로 바꿔 쓰면 다른 값으로 본다 (러너 · 검사기 같다) ·
     기록 파일 전체가 UTF-8 이 아니면 트리 관문이 읽을 때 거부한다 (Codex EQ — 저장 뒤 바이트 손상 · 전에는 받았다) ·
     러너는 손으로 넣은 글 (잡 id · 취소 시각 · 사유) 을 쓸 때 UTF-8 이 아니면 거부한다 (u8ok · Codex EP — 전에는 그 바이트를 그대로 썼다) ·
     attempt.json · w0_check.json 은 REC1 이 아니다 (안에 객체) — 트리 관문이 printf 틀 그대로만 받는다 (tpl5 = tpl_parse · Codex EQ — 키 순서 · 빈칸까지 같아야 한다 ·
     러너가 아닌 도구가 같은 내용을 다른 꼴로 쓰면 거부한다) · wall_of 의 elapsed_s 는 여전히 러너 grep · 검사기 json (관문이 틀을 먼저 본다)
   · 트리 관문 (Codex EQ) 의 이름 규칙은 현장 트리 기준이다 — 시도 폴더에 반송 허용 · 금지 이름 · VASP 표준 출력 (VASP_OUT) 밖의 이름이 있으면 멈춘다 (VASP_CMD 가
     시도 폴더에 다른 파일을 쓰는 환경이면 거짓 멈춤 8 · 연락) · 기존 반송본 대조는 러너만 한다 (검사기는 반송본 하나를 받는다) · 업체 시계 · 노드 시계는 믿는다
   · 중단 장부 · 영수증 · 시도 폴더 · 끝 기록을 모두 서로 맞게 함께 바꾼 위조는 못 잡는다 (서로 대조할 뿐 · 업체 서버의 원본을 보지 않는다)
   · 끝 기록의 시도 목록 (Codex EO P2) 은 그 실행의 시도 폴더 · run_id 를 묶는다 — 같은 실행에서 포장을 두 번 해도 같다 (포장 시각은 묶지 않는다)
   · 시도 이력 대조 (Codex EP P1) 는 한 방향이다 — 이력 줄마다 지금 · 보존 폴더의 끝난 시도가 있어야 한다 (끝난 시도에 이력 줄이 없는 것은 러너가 끝 기록과 이력 줄 사이에서
     끊기는 틈 때문에 보지 않는다) · 이력 줄까지 함께 지운 부분 복구는 못 잡는다
   · 장부 줄 순서 (Codex EP P2 · EQ P2) 는 영수증 기록 시각 · 시작 시각이 줄 순서대로 줄지 않는지와 단 순서 (전역 번호순 A5 ≤ c1 ≤ c2) 를 따로 본다 —
     시간 순서는 단 순서를 함의하지 않는다 (같은 초의 맞바꿈은 시간으로는 통과했다 · Codex EQ 정정) · date +%s 를 믿는다
"""
import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_v5_vasp_package as V          # noqa: E402
import build_round2_vasp_package as R2     # noqa: E402

PkgError = V.PkgError
_sha, _sha_text, _write, fin = V._sha, V._sha_text, V._write, V.fin
REPO = R2.REPO

AMEND5 = "db/properties/wad_aprime_pilot_prereg_v5_amendment_5_e70_retry_2026_11_20.json"
DECISION = "D-2026-11-20-wad-aprime-v5-e70-a5-retry"
JOB = "V5_s_outer_A_G4_e70_far_a5"
SRC = R2.A4_SRC                                    # V5_s_outer_A_G4_e70_far — 봉인 V5 잡 (POSCAR · KPOINTS · POTCAR.spec · INCAR)
REG_PATH = "db/raw/wad_round2_vasp_2026_10_22/pp_registry_round2_2026_10_26.json"
REG_SHA256 = "999aa2dae0b137eab7934723d76effecb53bf7d2ddeb8fe687857e467f9ff1b4"   # 외주 2차 봉인 등록부 (같은 업체 · 같은 빌드 · 같은 PP)
A4_RESULT = "db/raw/wad_round2_vasp_2026_10_22/a4_result_round2_2026_10_26.json"
A4_RESULT_SHA256 = "aec74641410695dcdb1a98e738061dfc00b93992a9c4e352b0afaa0cff508d83"
W0_REL = "run/V5_s_outer_A_G4_e70_far_a4_a4/stageA/WAVECAR"                       # 외주 2차 묶음 폴더 기준 (업체 서버)
W0_SHA256 = "8a65bde238eaa088a7d6832cc74523acfd8034e27c1c37f1d62ae0162394e9d9"
W0_SIZE = 6820958848
W0_DIMS = {"NKPTS": "4", "NBANDS": "872", "ENCUT": "650.0"}
STAGES = ("A5", "c1", "c2")
VARIANTS = {"A5": ("A5c", "A5f"), "c1": ("c1",), "c2": ("c2",)}
STAGE_OF_VAR = {v: s for s, vs in VARIANTS.items() for v in vs}
INCAR_OF = {"A5c": "INCAR.a5A5c", "A5f": "INCAR.a5A5f", "c1": "INCAR.a5c1", "c2": "INCAR.a5c2"}
#: 봉인 INCAR 에 대한 **의미상 차이** (개정 5 '사다리_a5' · v2) — 빌드가 만든 뒤 semantic_diff 로 다시 대조한다 (그 밖의 차이 = 빌드 실패)
DELTA = {"A5c": {"LDIPOL": ".FALSE.", "LWAVE": ".TRUE.", "NELM": "300", "MAXMIX": "200", "AMIX": "0.1", "AMIN": "0.01", "ISTART": "1", "ICHARG": "0"},
         "A5f": {"LDIPOL": ".FALSE.", "LWAVE": ".TRUE.", "NELM": "300", "MAXMIX": "200", "AMIX": "0.1", "AMIN": "0.01", "ISTART": "0"},
         "c1": {"ISTART": "1", "ICHARG": "0", "NELM": "400", "MAXMIX": "200", "AMIX": "0.1", "AMIN": "0.01"},
         "c2": {"ALGO": "All", "TIME": "0.1", "ISTART": "1", "ICHARG": "0", "NELM": "400"}}
NELM = {v: int(d["NELM"]) for v, d in DELTA.items()}
#: OUTCAR 해석값 (5.4.4 실물 꼴 — a4 ⓑ OUTCAR: 'IALGO = 38' · 'AMIX = 0.40; BMIX = 1.00' · 'AMIN = 0.01' · '… MIXPRE= 1;  MAXMIX= -45' · 'TIME = 0.40')
ECHO_EXPECT = {"A5c": {"IALGO": 38, "AMIX": 0.1, "AMIN": 0.01, "MAXMIX": 200}, "A5f": {"IALGO": 38, "AMIX": 0.1, "AMIN": 0.01, "MAXMIX": 200},
               "c1": {"IALGO": 38, "AMIX": 0.1, "AMIN": 0.01, "MAXMIX": 200}, "c2": {"IALGO": 58, "TIME": 0.1}}
ROW_HDR = {"A5": ("DAV", "RMM"), "c1": ("DAV", "RMM"), "c2": ("SDA", "CGA")}   # 개정 5 '주_기준' — c2 만 ALGO All 머리 (5.4.4 에서 SDA · CGA 로 예상)
CAP_H = 180.0                       # 개정 5 '누적_상한' (최악 164.6 h × 1.1)
INFRA_MAX = 2                       # 개정 5 '순서': 0 스텝 인프라 중단 '잡마다 2 회 · 개정 4 그대로' (잡이 하나라 전체 2 회)
SEC_W1, SEC_W0, SEC_MIN_STEPS = 50, 50, 100     # 개정 5 '보조_기준' — W1 = 마지막 50 · W0 = 그 앞 50 · 스텝 ≥ 100
HIST_INFO, RMS_JUMP, RMS_WIN = 45, 100.0, 20    # 개정 5 '조기_경보' (정보)
RETURN_ALLOWED = R2.RETURN_ALLOWED
RETURN_FORBIDDEN = R2.RETURN_FORBIDDEN
MGMT = ("run/env.txt", "run/status.tsv", "run/infra_aborts.tsv", "run/w0_check.json", "run/start_point.json", "run/final.json")
SCHEMA_PKG, SCHEMA_RESULT = "wad_a5_vasp_package/v1", "wad_a5_result/v1"
BLOCKING = ("ATTEMPT_MISMATCH", "INPUT_MODIFIED", "POTCAR_UNVERIFIED", "ATTEMPT_UNREADABLE")   # 어느 시도든 이것이면 채택 없음 (무결성)
AB_RE = re.compile(r"^(.+)_(A5|c1|c2)_([0-9]+)$")
# 트리 관문 (Codex EQ — 러너 tree5 = 검사기 tree_problems) 의 한 곳 상수: 러너에는 run_a5_text 가 자리표시 (@ATT_EXTRA@ · @ATT1_T@ · @W0_T@) 로 같은 바이트를 넣는다
VASP_OUT = ("CONTCAR", "DOSCAR", "EIGENVAL", "PCDAT", "XDATCAR", "REPORT", "PROCAR", "PROOUT", "PARCHG", "ELFCAR", "WAVEDER", "AECCAR0", "AECCAR1", "AECCAR2",
            "STOPCAR", "vaspout.h5", ".running")          # 시도 폴더에 둘 수 있는 VASP 표준 출력 · 러너 표지 (반송 허용 · 금지 이름 밖) — 그 밖은 모르는 이름 (멈춤)
SEAL_ORDER = ("INCAR", "POSCAR", "KPOINTS", "POTCAR", "OUTCAR", "OSZICAR", "WAVECAR.info", "stdout.log", "POTCAR.titel", "POTCAR.species.sha256", "attempt.start")
PREP_ALLOW = ("INCAR", "POSCAR", "KPOINTS", "POTCAR", "POTCAR.species.sha256", "POTCAR.titel", "POTCAR.sha256", "WAVECAR", "attempt.start")   # 준비 폴더에 러너가 쓰는 것 (run_one5 · 띄우기 전) — 그 밖 (OSZICAR · OUTCAR …) 은 실행 기록 (Codex ER Q-ER-1①)
OSZ_TITLE = ("N E dE d eps ncg rms", "N E dE d eps ncg rms rms(c)")    # OSZICAR 열 제목 (빈칸 줄여서) — 0 스텝은 빈 줄 · 이 제목 (끝 조각은 그 앞부분) 만 (Codex ER Q-ER-2)
ATT1_TPL = ('{"job": \x01, "attempt": \x01, "stage": \x01, "run_id": \x01, "rc": \x02, "t_start": \x02, "t_end": \x02, "elapsed_s": \x02, "vasp_version": \x01, '
            '"kernel_sha256": \x01, "perf": \x01, "sha256": {' + ", ".join(f'"{f}": \x01' for f in SEAL_ORDER) + "}}")      # run_one5 의 attempt.json printf 그대로
W0_TPL = ('{"path": \x01, "sha256": \x01, "size": \x01, "head": \x01, "expect": {"sha256": \x01, "size": \x01, "NKPTS": \x01, "NBANDS": \x01, "ENCUT": \x01}, '
          '"verified": \x02, "why": \x01, "checked_utc": \x01}')                                                          # w0_check 의 printf 그대로
FINAL_COMBOS = frozenset({(0, "OK"), (1, "NO_PRIMARY"), (1, "CLOSED"), (5, "CAP"), (6, "ENV"), (8, "REVIEW")})         # fin5 가 쓰는 code/state 만


# ───────────────────────── 외주 2차 부품 (파이썬) ─────────────────────────
def variant_text(base, var):
    """봉인 INCAR → a5 변형. 외주 2차 rung_text 를 그대로 쓴다 (있는 줄은 값만 · 없는 태그는 끝에 · 순서 결정적).
    rung_text 는 모듈 표 RUNG_DIFF 에서 차이를 읽는다 — 잠깐 이름 'a5:<변형>' 으로 넣었다가 반드시 뺀다 (selftest 가 새지 않는지 본다)."""
    key = f"a5:{var}"
    if key in R2.RUNG_DIFF:
        raise PkgError(f"외주 2차 RUNG_DIFF 에 {key} 가 이미 있다")
    R2.RUNG_DIFF[key] = DELTA[var]
    try:
        return R2.rung_text(base, key)
    finally:
        del R2.RUNG_DIFF[key]


def verify_variant(base, text, var):
    """VASP 의미상 차이가 등록한 변경 집합과 **정확히** 같은가 (빠진 태그 · 더한 태그 · 다른 값 = PkgError)."""
    got = {k: v[1] for k, v in R2.semantic_diff(base, text).items()}
    if got != DELTA[var]:
        raise PkgError(f"INCAR.{var}: 의미상 차이 {got} ≠ 등록 {DELTA[var]}")


GEN_ROW = re.compile(r"^[ \t]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:")    # 러너 row_scan 의 awk 와 같은 꼴 (줄 맨 앞 1–4 글자 + ':' = '행꼴')
REAL_TOK = re.compile(r"[+-]?(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[Ee][+-]?[0-9][0-9]?)?")   # 행의 실수 칸 (러너 row_scan 의 R 과 같다 · 지수 두 자리 — 유한 · Codex EP P0)
HDR_CUT = re.compile(r"[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?")                    # 콜론 앞에서 잘린 머리 (앞 빈칸 · 탭을 걷은 끝 조각이 글자 1–4 · 앞 빈칸 뒤 'N' 은 열 제목 — Codex EP P0 · EQ P0)
ROW_TOK_MAX = 24    # 완전한 행의 칸 하나 ≤ 24 글자 (Codex EQ P0 — 실물 최장 토큰 19 자: V5 반송 VASP 5.4.4 출력 20 개 · DAV/RMM 2,733 행 · Codex ER 계수)
ROW_MIN_TOK = 6     # 완전한 행 — 머리 ':' 뒤 칸 ≥ 6 (N E dE d eps ncg rms · rms(c) 는 첫 행들 · 수렴 행에 없다 — 외주 2차 반송 실물 OSZICAR 23 개: 6 칸 110 행 · 7 칸 1255 행)


def _complete_row(ln, stage):
    """줄바꿈으로 끝난 행꼴 줄 하나 → 완전한 행이면 칸 목록 (머리 뒤 · N E dE d eps ncg rms [rms(c)] …) · 아니면 None.
    완전한 행 = 머리가 그 단의 허용 머리 그대로 (빈칸 없이) · ':' 뒤 빈칸/탭 ≥ 1 · 칸 6 또는 7 · 숫자로 읽힘 — N 양의 정수 · ncg 정수 · E dE d eps rms [rms(c)] 실수
    (REAL_TOK — 부호 · 소수점 · E 지수 두 자리 · NaN · *** · inf 아님) (러너 row_scan 과 같다 · Codex EO P0 · EP P0)."""
    m = re.fullmatch(r"[ \t]*(?:" + "|".join(ROW_HDR[stage]) + r"):[ \t]+(.*)", ln)
    t = [x for x in re.split(r"[ \t]+", m.group(1)) if x] if m else []
    ok = (len(t) in (ROW_MIN_TOK, ROW_MIN_TOK + 1) and re.fullmatch(r"[1-9][0-9]*", t[0]) is not None and re.fullmatch(r"[0-9]+", t[4]) is not None
          and all(REAL_TOK.fullmatch(t[i]) for i in (1, 2, 3, 5)) and (len(t) == ROW_MIN_TOK or REAL_TOK.fullmatch(t[6]) is not None)
          and all(len(x) <= ROW_TOK_MAX for x in t))                  # 칸 길이 ≤ 24 — 지수 두 자리와 함께 |x| < 1e119 (늘 유한 · 310 자리 → 손상 · Codex EQ P0)
    return t if ok else None


def row_gate(osz, stage):
    """OSZICAR 원문 → (완전한 행 수, 사유 | None) — 러너 row_scan 과 같은 규칙 (selftest 가 같은 탐침으로 대조 · Codex EO P0).
    줄은 '\\n' 으로만 나눈다 · 마지막 '\\n' 뒤 조각 = 끝 조각 (줄바꿈 없음). 행꼴 줄 (GEN_ROW) 마다: 머리가 그 단의 허용 머리 밖이면 사유 row_header_<머리> (첫 것) ·
    줄바꿈으로 끝났고 완전하면 (_complete_row) 센다 · 아니면 손상. 사유 순서: nul_bytes (NUL 이 있으면 — awk 마다 다르게 읽는다) > row_header_<머리> > incomplete_row
    (줄바꿈으로 끝난 완전하지 않은 행꼴 줄이 있거나 · 완전한 행 0 인데 행꼴 끝 조각 또는 콜론 앞에서 잘린 머리 조각 (앞 빈칸 · 탭을 걷고 글자 1–4 · 앞 빈칸 뒤 'N' 만 열 제목) 이 있음). 완전한 행 ≥ 1 뒤의 행꼴 끝 조각은 세지 않고 사유도 아니다 (스케줄러에 끊긴 잘린 꼬리).
    ⚠ 못 하는 것: 줄바꿈까지 쓰인 행의 숫자 값이 맞는지는 판정 계약 (유한수 · 스텝 번호) 이 본다 — 여기서는 '다 쓰였는가' 만 본다."""
    if osz is None:
        return 0, None
    if "\x00" in osz:
        return 0, "nul_bytes"
    allowed, lines = ROW_HDR[stage], osz.split("\n")
    tail = lines.pop()
    n, part, bad, tailrow = 0, 0, None, False
    for ln in lines:
        if not GEN_ROW.match(ln):
            continue
        h = ln.lstrip(" \t").split(":", 1)[0].replace(" ", "")
        if h not in allowed:
            bad = bad or f"row_header_{h}"
        elif _complete_row(ln, stage) is not None:
            n += 1
        else:
            part += 1
    if tail and GEN_ROW.match(tail):
        h = tail.lstrip(" \t").split(":", 1)[0].replace(" ", "")
        if h not in allowed:
            bad = bad or f"row_header_{h}"
        else:
            tailrow = True
    elif tail:                                       # 콜론 앞에서 잘린 머리 ('SDA' · 'D' · 앞 빈칸 '  SDA') — 완전한 행 0 이면 손상 (Codex EP P0 · EQ P0 · 러너 row_scan 과 같다)
        u = tail.lstrip(" \t")
        if HDR_CUT.fullmatch(u) and not (u != tail and re.fullmatch(r"N *", u)):     # 앞 빈칸 뒤 'N' 만 열 제목 (0 스텝)
            tailrow = True
    ux = any(_unexplained(ln, True) for ln in lines if not GEN_ROW.match(ln)) or (bool(tail) and not GEN_ROW.match(tail) and _unexplained(tail, False))
    if bad:
        return n, bad
    if part or (tailrow and n == 0):
        return n, "incomplete_row"
    if ux and n == 0:                                # 0 스텝은 0 행으로 설명되는 내용만 — 빈 줄 · 열 제목 (끝 조각은 그 앞부분) (Codex ER Q-ER-2)
        return 0, "unexplained_line"
    return n, None


def _unexplained(ln, whole):
    """행꼴이 아닌 줄 하나 → 0 스텝으로 설명되지 않는가 (러너 row_scan 의 ux 와 같다): 빈칸 · 탭을 한 칸으로 줄인 글이 비었거나, 앞 빈칸으로 시작하고
    줄바꿈으로 끝난 줄이면 열 제목 (OSZ_TITLE) 그대로 · 끝 조각이면 긴 제목의 앞부분이면 설명된다."""
    v = re.sub(r"[ \t]+", " ", ln).strip(" ")
    if not v:
        return False
    return not (ln[:1] in (" ", "\t") and (v in OSZ_TITLE if whole else OSZ_TITLE[1].startswith(v)))


def feed5(osz, stage):
    """판정 계약 입력 (러너 osz_feed 와 같다) — 줄바꿈으로 끝난 줄만 (끝 조각은 뺀다) · 그 단의 허용 머리 → 'DAV:' (2차 계약의 행 정규식은 CGA 를 모른다 — 칸 위치는 같다).
    row_gate 사유가 없을 때만 쓴다 (그때 행꼴 줄은 다 완전한 행이다)."""
    rx = re.compile(r"^([ \t]*)(" + "|".join(ROW_HDR[stage]) + r"):")
    return "".join(rx.sub(r"\1DAV:", ln) + "\n" for ln in (osz or "").split("\n")[:-1])


def judge5(osz, out, incar, rc, stage):
    """a5 판정 = 완전한 행 판독 (row_gate) + 외주 2차 judge_text (계약 ①–⑤ · 같은 규칙 · 같은 순서) 에 완전한 행만 (feed5).
    러너 judge5() 와 같은 답 (selftest 가 같은 탐침으로 대조)."""
    if osz is None:
        return R2.judge_text(osz, out, incar, rc)
    n, bad = row_gate(osz, stage)
    if bad:
        return "SCF_UNVERIFIED", n, "NA", "NA", bad
    return R2.judge_text(feed5(osz, stage), out, incar, rc)


def osz_rows(osz, stage):
    """OSZICAR 의 완전한 전자 반복행 (row_gate 와 같은 기준) → [(스텝, E 토큰, dE, d eps, rms(c) | None)] (순서 그대로 · 끝 조각 · 손상 행은 없다)."""
    out = []
    for ln in (osz or "").split("\n")[:-1]:
        t = _complete_row(ln, stage) if GEN_ROW.match(ln) else None
        if t is not None:
            out.append((t[0], t[1], t[2], t[3], t[6] if len(t) > 6 else None))
    return out


def secondary_numbers(osz, stage):
    """개정 5 '보조_기준' 숫자 — c1 · c2 의 OSZICAR E (둘째 칸 · 자유에너지 · SCF 단계라 D3 빠짐 — 같은 기하에서 상수) → (숫자 dict, 거부 사유).
    u_E = max( max(W1) − min(W1) , |mean(W1) − mean(W0)| ) · W1 = 마지막 50 · W0 = 그 앞 50 스텝. A5 · 다른 단 · 스텝 < 100 · 비유한 E 는 거부한다.
    ⛔ 상태 (SCF_NOT_CONVERGED) · 완결성 · 재시작 · u_W 문턱은 여기서 정하지 않는다 (check_attempt5 · V5 수집기)."""
    if stage not in ("c1", "c2"):
        return None, f"보조 기준은 a5 의 c1 · c2 에만 (단 {stage!r} — A5 · a4 ⓐ · 옛 시도에는 소급하지 않는다)"
    n, bad = row_gate(osz, stage)
    if bad:
        return None, f"행 머리 관문 {bad}"
    E = [R2._num(r[1]) for r in osz_rows(osz, stage)]
    if len(E) < SEC_MIN_STEPS:
        return None, f"전자 스텝 {len(E)} < {SEC_MIN_STEPS}"
    if any(x is None for x in E[-(SEC_W1 + SEC_W0):]):
        return None, "창 안에 유한하지 않은 E"
    w1, w0 = E[-SEC_W1:], E[-(SEC_W1 + SEC_W0):-SEC_W1]
    rng = max(w1) - min(w1)
    shift = abs(sum(w1) / len(w1) - sum(w0) / len(w0))
    return {"n_steps": len(E), "W1_range_eV": rng, "mean_shift_eV": shift, "u_E_eV": max(rng, shift),
            "window": f"W1 = 마지막 {SEC_W1} · W0 = 그 앞 {SEC_W0} 스텝 (OSZICAR E · D3 빠짐 — 같은 기하에서 상수)"}, None


def hist_max(out_text):
    """OUTCAR 'eigenvalues of (default mixing * dielectric matrix)' 뒤 고유값 개수의 최댓값 = Broyden 이력 길이 (정보 · 러너 hist_max 와 같다)."""
    m, k, state = 0, 0, 0
    for ln in (out_text or "").split("\n"):
        if "eigenvalues of (default mixing * dielectric matrix)" in ln:
            if state == 2:
                m = max(m, k)
            state, k = 1, 0
            continue
        if state == 1:
            state = 2
            continue
        if state == 2:
            if not ln.split():
                m, state = max(m, k), 0
                continue
            k += sum(1 for x in ln.split() if re.fullmatch(r"[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?", x))
    if state == 2:
        m = max(m, k)
    return m


def rms_jumps(osz, stage):
    """OSZICAR rms(c) (8 째 칸 — 머리 DAV: 가 1 째 · 2차 계약의 $4 · $5 와 같은 셈) 가 직전 20 스텝 최솟값의 100 배를 넘은 스텝 목록 (정보 · 러너 rms_jump 와 같은 규칙)."""
    v = [R2._num(r[4]) if r[4] is not None else None for r in osz_rows(osz, stage)]
    out = []
    for k in range(RMS_WIN, len(v)):
        prev = [x for x in v[k - RMS_WIN:k] if x is not None]
        if v[k] is not None and prev and v[k] > RMS_JUMP * min(prev):
            out.append(k + 1)
    return out


# ───────────────────────── 외주 2차 부품 (러너 bash) ─────────────────────────
def _bash_ok(text):
    r = subprocess.run(["bash", "-n"], input=text, text=True, capture_output=True)
    return r.returncode == 0


def r2_block(first_line_prefix):
    """외주 2차 RUN_ALL 에서 첫 줄이 이 접두어로 시작하는 블록 하나 (함수 정의 · if 블록) — 끝은 첫 번째로 bash -n 이 통과하는 줄 (손으로 괄호를 세지 않는다).
    접두어가 정확히 한 줄에 없으면 PkgError."""
    L = R2.RUN_ALL.split("\n")
    st = [i for i, ln in enumerate(L) if ln.startswith(first_line_prefix)]
    if len(st) != 1:
        raise PkgError(f"외주 2차 RUN_ALL 에서 '{first_line_prefix}' 줄이 {len(st)} 개 — 1 개여야 한다")
    s = st[0]
    for e in range(s, len(L)):
        blk = "\n".join(L[s:e + 1])
        if _bash_ok(blk):            # 첫 번째로 문법이 닫히는 줄 = 블록 끝 (줄 끝 주석 · 한 줄 함수도 그대로 · 뒤 줄을 끌어오지 않는다)
            return blk
    raise PkgError(f"외주 2차 RUN_ALL '{first_line_prefix}' 블록의 끝을 못 찾았다")


def _patch(text, old, new, count=1):
    """정확히 count 번 나오는 자리만 바꾼다 (아니면 PkgError — 2차 러너가 바뀌었는데 조용히 다른 것을 만들지 않게)."""
    n = text.count(old)
    if n != count:
        raise PkgError(f"러너 부품 패치 자리 {old[:60]!r} 가 {n} 번 (기대 {count})")
    return text.replace(old, new)


R2_FUNCS = ("h", "utc", "up", "log", "clean", "enc_eq", "cap_num", "secs_ok", "incar_val", "judge", "alarms", "pack_fail", "pack", "finish",
            "pp_ok", "ver_of", "wav_head", "out_num", "wsha")


def r2_parts():
    """a5 러너에 들어가는 외주 2차 부품 (이름 → 텍스트 · 패치 뒤)."""
    P = {n: r2_block(f"{n}(){{") for n in R2_FUNCS}
    # 판정: 이름만 judge_r2 로 · OSZICAR 입력만 행 머리 관문을 통과한 꼴로 (계약 본문은 그대로)
    P["judge"] = _patch(_patch(P["judge"], "judge(){", "judge_r2(){"), 'cat "$d/OSZICAR" 2>/dev/null |', 'osz_feed "$d" |')
    # 조기 경보: c2 의 CGA 행도 센다 (정보 — 판정 아님)
    P["alarms"] = _patch(P["alarms"], "(DAV|RMM|CG|SDA):", "(DAV|RMM|CG|SDA|CGA):")
    # 포장: 반송 이름 a5_return · 관리 파일에 ⓪ 확인 기록
    P["pack"] = _patch(P["pack"], "round2_return", "a5_return", count=P["pack"].count("round2_return") or 1)
    P["pack_fail"] = _patch(P["pack_fail"], "round2_return", "a5_return", count=P["pack_fail"].count("round2_return") or 1)
    P["pack"] = _patch(P["pack"], "for f in run/env.txt run/status.tsv run/infra_aborts.tsv; do",
                       "for f in " + " ".join(MGMT) + "; do")
    P["finish"] = _patch(_patch(P["finish"], "PACK_ONLY=1 bash run_all.sh", "PACK_ONLY=1 bash run_a5.sh"), "round2_return.tgz", "a5_return.tgz")
    P["finish"] = _patch(P["finish"], "⚠ 값 없는 잡이 있다 — 그대로 반송해 주세요 (실패도 기록입니다)",
                         "⚠ 주 기준 값 없음 — 그대로 반송해 주세요 (보조 기준은 반송 뒤 우리가 봅니다 · 실패도 기록입니다)")
    P["finish"] = _patch(P["finish"], "다음 잡을 띄우지 않았다", "다음 단을 띄우지 않았다")
    # 포장 = 덮어쓰기 전에 트리 관문 (끝 포장 · 환경 고장 포장 · PACK_ONLY — 기존 반송본 대조 · 잔여 · 신원 · 끝 기록 · Codex EQ P1)
    P["pack"] = _patch(P["pack"], "pack(){\n", "pack(){\n  tree_gate 포장                       # 덮어쓰기 전에 항상 (Codex EQ — 실패면 종료 8 · 아무것도 안 씀)\n")
    # 포장: 점으로 시작하는 폴더 (run/.prep_* 준비 폴더 · run/.a5.lock) 는 담지 않는다 (VASP 를 띄운 적 없는 임시 폴더 · 리뷰 P2(c))
    P["pack"] = _patch(P["pack"], 'grep -E "^(run|run_aborted)/[^/]+/(stageA/)?($RET_ALLOW)$"', 'grep -E "^(run|run_aborted)/[^/.][^/]*/(stageA/)?($RET_ALLOW)$"')
    # 끝 안내: 8 (1저자 검토 멈춤 · 개정 5 해석 1) 을 더한다
    P["finish"] = _patch(P["finish"], '    6) echo "⛔ 공통 환경 고장 — 전체 정지. 반송해 주시고 연락 주세요";;\n',
                         '    6) echo "⛔ 공통 환경 고장 — 전체 정지. 반송해 주시고 연락 주세요";;\n'
                         '    8) echo "⏸ 1저자 검토 멈춤 (개정 5 해석 1) — 더 돌리지 않았다. 반송해 주시고 1저자 결정을 기다려 주세요 (다시 돌려도 아무것도 띄우지 않는다)";;\n')
    # A5 자격 (elig5) 은 외주 2차 elig_A 를 쓰지 않고 a5 판으로 새로 쓴다 — '기록은 유효한데 파일이 사라짐 · 바뀜' 을 ⓪ 으로 넘기지 않고 1저자로 (RUN_A5_BODY)
    P["perf"] = r2_block('if [ -n "${PERF_TAGS_FILE:-}" ]; then')
    # --infra-wall 은 a5 판으로 새로 쓴다 (RUN_A5_CLI — 영수증을 REC1 로 읽고 다시 쓴다 · 채운 시각 · Codex EO P1) — 외주 2차 블록 (sed · 고정 꼴 grep) 을 쓰지 않는다
    P["pack_only"] = _patch(r2_block('if [ "${PACK_ONLY:-0}" = 1 ]; then'), "PACK_ONLY=1 로 다시", "PACK_ONLY=1 bash run_a5.sh 로 다시")
    return P


RUN_A5_HEAD = r'''#!/usr/bin/env bash
# =============================================================================
# run_a5.sh (W_ad V5 개정 5 · a5) — 은 쪽 G4 ENCUT 650 분리 끝점 한 잡 (@JOB@) 의 결과 뒤 재시도 · 사다리 ⓪ → A5 → c1 → (c2)
#   ⓪ 보존된 a4 ⓐ WAVECAR 확인 (W0_WAVECAR · sha · 크기 · 머리 — 원본은 읽기만 · 복사본만 쓴다)
#   A5 LDIPOL 끔 (⓪ 이 확인되면 그 복사본에서 이어서 · 아니면 새로) → c1 (Davidson · MAXMIX 200) → c1 이 주 기준 수렴이 아니면 c2 (ALGO All · TIME 0.1)
#   SCF 판정 = OSZICAR 마지막 전자 반복행 (검사기와 같은 계약 · 외주 2차 judge() 그대로) + 단마다 행 머리 관문 (A5 · c1 = DAV/RMM · c2 = SDA/CGA)
#   개정 5 해석 1 (사용자 2026-11-20): 다음 단은 지금 단이 SCF_NOT_CONVERGED 이거나, 전자 반복행 ≥ 1 인 실행 실패 (--killed 로 기록한 끊김 포함) 로
#     끝났을 때만 띄운다 · 전자 반복행 0 → 멈춤 (7 · 다음 단을 쓰지 않는다) · 재시작 미이행 · SCF 미확인 · 설정 에코 다름 → 멈춤 (8 · 1저자) ·
#     A5 가 행은 있는데 자격 미달이면 개정 5 그대로 (⓪ 이 확인되면 그 복사본에서 c1 · c2 · 아니면 닫는다)
#   필수: VASP_CMD · POTCAR_DIR (PAW_PBE: <POTCAR_DIR>/{Li_sv,P,S,Cl,Ag}/POTCAR) · W0_WAVECAR (보존 ⓐ WAVECAR 경로 — 없으면 W0_WAVECAR=none)
#   선택: PERF_TAGS_FILE (외주 2차와 같은 NCORE = 4 · KPAR = 2 — 세 단 모두 같은 배치라야 NBANDS 872 가 그대로다) · PACK_ONLY=1 · WATCH_S (기본 60)
#   경로는 절대 경로를 권한다 (상대 경로는 이 스크립트를 부른 폴더 기준으로 푼다)
#   기록 명령 (README): --infra-abort · --infra-wall · --killed · --reset-w0 · --unlock — 영수증 · 끊김 기록은 한 줄 JSON (손으로 넣은 글은 JSON 이스케이프)
#   종료: 0 c1 또는 c2 주 기준 수렴 (끝) · 1 주 기준 값 없음 — 사다리 끝 (끝 · 실패도 기록) · 2 인자 · 묶음 · 환경 오류 (아무것도 띄우지 않음)
#         3 준비 실패 (그 단은 소모 안 함 — 원인을 고친 뒤 다시) · 4 포장 실패 (PACK_ONLY=1 로 다시)
#         5 누적 상한 @CAP_H@ h (끝) 또는 끊긴 시도 · 벽시계 미상 (--killed · --infra-abort · --infra-wall 로 기록한 뒤 다시)
#         6 공통 환경 고장 (VASP 빌드 · PP — 전체 정지) · 7 전자 반복행 0 (--infra-abort 또는 연락) · 8 1저자 검토 멈춤 (끝) 또는 트리 관문 (아무것도 쓰지 않음 · 원본 보존 · 연락)
#   끝 (0 · 1 · 5 상한 · 8 · 돈 뒤의 6 — VASP 빌드 다름) 뒤에 다시 돌리면 run/final.json 을 찍고 같은 코드로 끝낸다 — 아무것도 띄우지 않는다 (포장만: PACK_ONLY=1)
#   보내는 것: 끝 뒤 `sha256sum -c a5_return.tgz.sha256` 까지 통과한 쌍
#   지원 환경: Linux · bash ≥ 4 · GNU coreutils (find sort grep cmp sha256sum od stat mv -T tr tail wc mktemp) · GNU tar · awk (mawk/gawk) · sed -E
# =============================================================================
set -u
ORIG_PWD=$PWD
absp(){ case "$1" in /*) printf '%s' "$1";; *) printf '%s/%s' "${ORIG_PWD%/}" "$1";; esac; }    # 상대 경로 → 부른 곳 기준 절대 경로 (cd 전에 푼다 · 리뷰 P1-3)
if [ -n "${W0_WAVECAR:-}" ] && [ "$W0_WAVECAR" != none ]; then W0_WAVECAR=$(absp "$W0_WAVECAR"); fi
if [ -n "${POTCAR_DIR:-}" ]; then POTCAR_DIR=$(absp "$POTCAR_DIR"); fi
if [ -n "${PERF_TAGS_FILE:-}" ]; then PERF_TAGS_FILE=$(absp "$PERF_TAGS_FILE"); fi
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
sha256sum -c --quiet MANIFEST.sha256 || { echo "⛔ 패키지 파일이 MANIFEST 와 다르다 — 실행하지 않는다"; exit 2; }
RET_ALLOW='@RET_ALLOW@'
RET_FORBID='@RET_FORBID@'
JOB=@JOB@
HOST=$(hostname 2>/dev/null || uname -n 2>/dev/null || echo unknown-host)
# ── 묶음 폴더에 a5 가 아닌 것 (외주 2차 폴더에 풀었을 때 · 다른 잡 흔적) → 거부 (리뷰 P2(g)) · 스케줄러 출력 파일만 둔다 ──
foreign(){
  local f b
  for f in * .[!.]* ..?*; do
    [ -e "$f" ] || [ -L "$f" ] || continue
    case "$f" in
      MANIFEST.sha256|README.md|SEALED_ENV.tsv|run_a5.sh|jobs.json|a5_return.tgz|a5_return.tgz.sha256|a5_return.list|a5_return.tgz.part|a5_return.tgz.sha256.part)
        { [ -f "$f" ] && [ ! -L "$f" ]; } || echo "$f";;
      jobs|run|run_aborted|a5_return.tmp) { [ -d "$f" ] && [ ! -L "$f" ]; } || echo "$f";;
      *.[eo][0-9]*|*.p[eo][0-9]*|slurm-*.out|nohup.out) [ -f "$f" ] || echo "$f";;
      *) echo "$f";;
    esac
  done
  for f in jobs/* jobs/.[!.]* jobs/..?*; do
    [ -e "$f" ] || [ -L "$f" ] || continue
    { [ "$f" = "jobs/$JOB" ] && [ -d "$f" ] && [ ! -L "$f" ]; } || echo "$f"
  done
  for f in run/* run/.[!.]* run/..?*; do
    [ -e "$f" ] || [ -L "$f" ] || continue
    b=${f#run/}
    case "$b" in
      "${JOB}_A5"|"${JOB}_c1"|"${JOB}_c2"|.a5.lock|".prep_${JOB}_A5"|".prep_${JOB}_c1"|".prep_${JOB}_c2") { [ -d "$f" ] && [ ! -L "$f" ]; } || echo "$f";;
      env.txt|status.tsv|infra_aborts.tsv|w0_check.json|start_point.json|final.json|*.part) { [ -f "$f" ] && [ ! -L "$f" ]; } || echo "$f";;
      *) echo "$f";;
    esac
  done
  for f in run_aborted/* run_aborted/.[!.]* run_aborted/..?*; do
    [ -e "$f" ] || [ -L "$f" ] || continue
    b=${f#run_aborted/}
    if [[ "$b" =~ ^${JOB}_(A5|c1|c2)_[1-9][0-9]*$ ]] && [ -d "$f" ] && [ ! -L "$f" ]; then :; else echo "$f"; fi
  done
}
FX=$(foreign | head -6)
[ -z "$FX" ] || { echo "⛔ 이 폴더에 a5 묶음이 아닌 것이 있다: $(printf '%s' "$FX" | tr '\n' ' ')— 새 빈 폴더에 풀어 주세요 (외주 2차 폴더에 풀지 않는다 · 묶음 zip · 제출 스크립트는 폴더 밖에)"; exit 2; }
mkdir -p run
'''

RUN_A5_ENV = r'''
# ── 봉인 환경 (외주 2차 등록부에서 · 빌드가 쓴다) · ⓪ 기대값 · 상한 ──
need_rel=1; REL_VER=""; RESTART_RE=""; W0_SHA=""; W0_SIZE=""; W0_NK=""; W0_NB=""; W0_EN=""; CAP_H=""; INFRA_MAX=""
declare -A REL_SP
while IFS=$'\t' read -r k a b; do
  case "$k" in
    vasp_version) REL_VER=$a;; species_sha256) REL_SP[$a]=$b;; restart_read_regex) RESTART_RE=$a;;
    w0_sha256) W0_SHA=$a;; w0_size) W0_SIZE=$a;; w0_nkpts) W0_NK=$a;; w0_nbands) W0_NB=$a;; w0_encut) W0_EN=$a;;
    cap_h) CAP_H=$a;; infra_max) INFRA_MAX=$a;;
  esac
done < SEALED_ENV.tsv
[ -n "$REL_VER" ] && [ "${#REL_SP[@]}" -ge 5 ] && [ -n "$RESTART_RE" ] && [[ "$W0_SHA" =~ ^[0-9a-f]{64}$ ]] && [[ "$W0_SIZE" =~ ^[0-9]+$ ]] \
  && [ -n "$W0_NK" ] && [ -n "$W0_NB" ] && [ -n "$W0_EN" ] && cap_num "$CAP_H" && [[ "$INFRA_MAX" =~ ^[0-9]+$ ]] \
  || { echo "⛔ SEALED_ENV.tsv 가 불완전하다 — 실행하지 않는다"; exit 2; }
incar_of(){ case "$1" in A5c) echo INCAR.a5A5c;; A5f) echo INCAR.a5A5f;; c1) echo INCAR.a5c1;; c2) echo INCAR.a5c2;; esac; }
stage_hdr(){ case "$1" in A5|c1) echo 'DAV|RMM';; c2) echo 'SDA|CGA';; esac; }
PREP_ALLOW='@PREP_ALLOW@'      # 준비 폴더 (run/.prep_<잡>_<단>) 에 둘 수 있는 이름 — 러너가 띄우기 전에 쓰는 것만 (그 밖은 실행 기록 → 지우지 않고 멈춤 · Codex ER Q-ER-1①)
ATT_EXTRA='@ATT_EXTRA@'      # 시도 폴더에 둘 수 있는 VASP 표준 출력 · 표지 (반송 허용 · 금지 이름 밖) — 그 밖의 이름은 트리 관문이 멈춘다 (Codex EQ P1)
ATT1_T='@ATT1_T@'            # attempt.json 틀 (run_one5 의 printf 그대로 · \001 문자열 · \002 음 아닌 정수) — 검사기 ATT1_TPL 과 같은 바이트
W0_T='@W0_T@'                # w0_check.json 틀 (w0_check 의 printf 그대로) — 검사기 W0_TPL

# ── 한 줄 기록 문법 REC1 (killed.json · infra_abort.json · attempt.start · final.json) — 검사기 rec_parse 와 같은 문법 · 다음 단을 띄우기 전에 전체를 읽는다 (Codex EO P1) ──
#   파일 = 한 줄 (+ 끝 줄바꿈 하나) · NUL 없음 · { "키": 값 (, "키": 값)* } (빈칸 · 탭은 JSON 처럼 토큰 사이 어디든 — "run_id":"x" 도 받는다) · 키 [a-z][a-z0-9_]* ·
#   값 = 문자열 (제어 바이트 0x00–0x1F 날것 금지 · 이스케이프 \" \\ \/ \b \f \n \r \t \uXXXX 만) 또는 음 아닌 정수 (선행 0 없음 · 16 자리 이하) · 같은 키 두 번 금지.
#   값 비교는 원문 (이스케이프를 풀지 않은 것) 으로 한다 — 검사기도 같다. LC_ALL=C (바이트 단위 · mawk · gawk 같은 답)
rec5(){ # $1 파일 → 맞으면 '키<TAB>꼴<TAB>원문' 줄들 (꼴 s 문자열 · i 정수) · 아니면 출력 없이 1
  [ -f "$1" ] || return 1
  tr -d '\000' < "$1" 2>/dev/null | cmp -s - "$1" 2>/dev/null || return 1          # NUL 이 있으면 거부 (awk 마다 NUL 을 다르게 다룬다 · 검사기도 거부)
  LC_ALL=C awk 'BEGIN { for (k = 1; k < 256; k++) ord[sprintf("%c", k)] = k; E1 = "\"\\/bfnrt" }
    function sk() { while (i <= L && (substr(s, i, 1) == " " || substr(s, i, 1) == "\t")) i++ }
    { m++; s = $0 }
    END {
      if (m != 1) exit 1
      L = length(s); i = 1; sk()
      if (substr(s, i, 1) != "{") exit 1
      i++; nk = 0
      while (1) {
        sk(); if (substr(s, i, 1) != "\"") exit 1
        j = i + 1; while (j <= L && substr(s, j, 1) != "\"") j++
        if (j > L) exit 1
        key = substr(s, i + 1, j - i - 1); if (key !~ /^[a-z][a-z0-9_]*$/) exit 1
        i = j + 1; sk(); if (substr(s, i, 1) != ":") exit 1
        i++; sk(); if (i > L) exit 1
        if (substr(s, i, 1) == "\"") {
          j = i + 1
          while (1) {
            if (j > L) exit 1
            c = substr(s, j, 1)
            if (c == "\"") break
            if (!(c in ord) || ord[c] < 32) exit 1
            if (c == "\\") {
              e = substr(s, j + 1, 1)
              if (e != "" && index(E1, e)) { j += 2; continue }
              if (e == "u" && substr(s, j + 2, 4) ~ /^[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F]$/) { j += 6; continue }
              exit 1
            }
            j++
          }
          t = "s"; v = substr(s, i + 1, j - i - 1); i = j + 1
        } else {
          j = i; while (j <= L && substr(s, j, 1) ~ /^[0-9]$/) j++
          v = substr(s, i, j - i)
          if (v !~ /^(0|[1-9][0-9]*)$/ || length(v) > 16) exit 1
          t = "i"; i = j
        }
        if (key in seen) exit 1
        seen[key] = 1; nk++; K[nk] = key; T[nk] = t; W[nk] = v
        sk(); c = substr(s, i, 1)
        if (c == ",") { i++; continue }
        if (c == "}") { i++; break }
        exit 1
      }
      sk(); if (i <= L) exit 1
      for (k = 1; k <= nk; k++) printf "%s\t%s\t%s\n", K[k], T[k], W[k]
    }' "$1"
}
rf(){ printf '%s\n' "$1" | LC_ALL=C awk -F'\t' -v K="$2" -v T="$3" '$1 == K && $2 == T { print substr($0, length(K) + length(T) + 3); f = 1; exit } END { exit !f }'; }   # rec5 출력 · 키 · 꼴 → 원문 (없으면 1)
rhas(){ printf '%s\n' "$1" | LC_ALL=C awk -F'\t' -v K="$2" '$1 == K { f = 1; exit } END { exit !f }'; }                                                              # rec5 출력에 그 키가 (꼴과 관계없이) 있나
rget(){ local r; r=$(rec5 "$1") || return 1; rf "$r" "$2" "$3"; }                                                                                                  # 파일 · 키 · 꼴 → 원문
jstr(){ # JSON 문자열 본문 — 따옴표 · 역슬래시 · 제어 바이트 (0x01–0x1F · 0x7F) 를 이스케이프하고 나머지 바이트는 그대로 (검사기 rec_parse · json 이 받는다 · Codex EO P1)
  printf '%s' "$1" | od -An -v -tx1 | LC_ALL=C awk 'BEGIN { for (k = 1; k < 256; k++) c[sprintf("%02x", k)] = sprintf("%c", k)
      for (k = 1; k < 32; k++) c[sprintf("%02x", k)] = sprintf("\\u%04x", k)
      c["7f"] = "\\u007f"; c["22"] = "\\\""; c["5c"] = "\\\\" }
    { for (i = 1; i <= NF; i++) printf "%s", c[$i] }'
}
start_id(){ # $1 시도 폴더 · $2 단 → '-' 또는 사유 — attempt.start 가 이 폴더의 시도인가 (REC1 · 잡 · stage a5 · 변형 · run_id 꼴 · t_start 정수 · 검사기 start_problem 과 같은 순서 · Codex EO P1 Q-EO-2b)
  local R v
  R=$(rec5 "$1/attempt.start") || { echo start_form; return; }
  [ "$(rf "$R" job s)" = "$JOB" ] || { echo start_job; return; }
  [ "$(rf "$R" stage s)" = a5 ] || { echo start_stage; return; }
  v=$(rf "$R" attempt s)
  case "$2:$v" in A5:A5c|A5:A5f|c1:c1|c2:c2) ;; *) echo "start_variant_${v:-none}"; return;; esac
  [[ "$(rf "$R" run_id s)" =~ ^[[:digit:]]{8}T[[:digit:]]{6}-[[:digit:]]+-[[:digit:]]+$ ]] || { echo start_run_id; return; }
  rf "$R" t_start i > /dev/null || { echo start_t; return; }
  echo -
}
receipt5(){ # $1 run_aborted/<잡>_<단>_<k> → '-' 또는 사유 — 중단 영수증 전체 (검사기 abort_receipt_problem 과 같은 순서 · Codex EN P1 · EO P1)
  local d=$1 b r R k w t0 rs fs
  b=${d##*/}; r=${b#"${JOB}"_}; r=${r%_*}
  [ -e "$d/infra_abort.json" ] || [ -L "$d/infra_abort.json" ] || { echo receipt_missing; return; }
  R=$(rec5 "$d/infra_abort.json") || { echo receipt_form; return; }
  for k in job rung run_id sched_job_id cancel_utc reason wall_s oszicar recorded_utc; do rf "$R" "$k" s > /dev/null || { echo "receipt_field_$k"; return; }; done
  rf "$R" recorded_s i > /dev/null || { echo receipt_field_recorded_s; return; }
  for k in sched_job_id cancel_utc reason; do nbj "$(rf "$R" "$k" s)" || { echo "receipt_blank_$k"; return; }; done     # 빈 값 · 빈칸 문자만 (이스케이프 포함 · 쓸 때도 nbw · Codex EP 조건부 · EQ P1)
  { [ "$(rf "$R" job s)" = "$JOB" ] && [ "$(rf "$R" rung s)" = "$r" ]; } || { echo receipt_job_rung; return; }
  [ "$(rf "$R" run_id s)" = "$(rget "$d/attempt.start" run_id s)" ] || { echo receipt_run_id; return; }
  w=$(rf "$R" wall_s s); { [ "$w" = UNKNOWN ] || secs_ok "$w"; } || { echo receipt_wall_s; return; }
  t0=$(rget "$d/attempt.start" t_start i); rs=$(rf "$R" recorded_s i)
  [ "$rs" -ge "$t0" ] 2>/dev/null || { echo receipt_recorded_s; return; }
  if rhas "$R" wall_s_filled_utc || rhas "$R" wall_s_filled_s; then
    { rf "$R" wall_s_filled_utc s > /dev/null && fs=$(rf "$R" wall_s_filled_s i) && secs_ok "$w" && [ "$fs" -ge "$rs" ]; } 2>/dev/null || { echo receipt_filled; return; }
  fi
  echo -
}
ledger5(){ # 중단 장부 (run/infra_aborts.tsv) ↔ 보존 폴더 (run_aborted/) ↔ 영수증 양방향 대조 → '-' 또는 사유 (검사기 ledger_problems + abort_receipt_problem · Codex EO P1 Q-EO-3)
  local L=run/infra_aborts.tsv d b lst rows x n w s prs=0 pt0=0
  lst=$(for d in run_aborted/*; do b=${d#run_aborted/}; [[ "$b" =~ ^${JOB}_(A5|c1|c2)_[[:digit:]]+$ ]] && [ -d "$d" ] && printf '%s\n' "$b"; done | LC_ALL=C sort)
  if [ ! -e "$L" ] && [ ! -L "$L" ]; then
    [ -z "$lst" ] && { hist5; return; }
    echo "ledger_missing_but_folder_$(printf '%s\n' "$lst" | head -1)"; return
  fi
  [ -f "$L" ] || { echo ledger_not_file; return; }
  tr -d '\000' < "$L" 2>/dev/null | cmp -s - "$L" 2>/dev/null || { echo ledger_nul; return; }
  [ "$(tail -c 1 "$L" | od -An -tx1 | tr -d ' \n')" = 0a ] || { echo ledger_no_final_newline; return; }
  u8f "$L" || { echo utf8_infra_aborts.tsv; return; }
  rows=$(LC_ALL=C awk -F'\t' -v J="$JOB" -v M="$INFRA_MAX" 'BEGIN { H = "recorded_utc\tjob\trung\tsched_job_id\tcancel_utc\twall_s\treason\tdir" }
    NR == 1 { if ($0 != H) { print "BAD ledger_header"; exit } next }
    { i++
      if (NF != 8) { print "BAD ledger_row_" i "_fields"; exit }
      if ($2 != J || ($3 != "A5" && $3 != "c1" && $3 != "c2")) { print "BAD ledger_row_" i "_job_rung"; exit }
      r = ($3 == "A5") ? 1 : (($3 == "c1") ? 2 : 3); if (r < pr) { print "BAD ledger_row_" i "_rung_order"; exit }; pr = r     # 단 순서 (전역 번호순 A5 ≤ c1 ≤ c2 · 같은 초 · Codex EQ P2)
      if ($8 != J "_" $3 "_" i) { print "BAD ledger_row_" i "_dir"; exit }
      if (!($6 == "UNKNOWN" || ($6 ~ /^(0|[1-9][0-9]*)$/ && length($6) <= 9))) { print "BAD ledger_row_" i "_wall_s"; exit }
      if (i > M) { print "BAD ledger_over_max"; exit }
      print $8 "\t" $6 }' "$L")
  x=$(printf '%s\n' "$rows" | grep -m1 '^BAD ' | cut -c5-); [ -z "$x" ] || { echo "$x"; return; }
  x=$(printf '%s\n' "$rows" | cut -f1 | LC_ALL=C sort)
  [ "$x" = "$lst" ] || { echo ledger_folders_differ; return; }
  while IFS=$'\t' read -r b n; do
    [ -n "$b" ] || continue
    x=$(receipt5 "run_aborted/$b"); [ "$x" = - ] || { echo "${b}_$x"; return; }
    w=$(rget "run_aborted/$b/infra_abort.json" wall_s s); [ "$w" = "$n" ] || { echo "${b}_ledger_wall_s_differs"; return; }
    w=$(rget "run_aborted/$b/infra_abort.json" recorded_s i); x=$(rget "run_aborted/$b/attempt.start" t_start i)       # 장부 줄 순서 = 일어난 순서 (Codex EP P2)
    { [ "$w" -ge "$prs" ] && [ "$x" -ge "$pt0" ]; } 2>/dev/null || { echo "${b}_ledger_time_order"; return; }
    prs=$w; pt0=$x
  done <<< "$rows"
  hist5
}
wall_of(){ # $1 시도 폴더 → 초 · UNKNOWN · BAD — 검사기 wall_of 와 같은 출처 순서 (Codex EO P1 Q-EO-2c · EP P1): 보존 폴더 (run_aborted/) 는 그 중단 영수증만
  #         (장부 · 폴더 · run_id 대조는 ledger5) · 진행 폴더 (run/<잡>_<단>) 는 영수증을 보지 않는다 (섞인 영수증은 ledger5 가 막는다) → 끊김 기록 → attempt.json elapsed_s → 미상
  local d=$1 w
  case "$d" in run_aborted/*)
    w=$(rget "$d/infra_abort.json" wall_s s) || { echo BAD; return; }
    if [ "$w" = UNKNOWN ] || secs_ok "$w"; then echo "$w"; else echo BAD; fi; return;;
  esac
  if [ -e "$d/killed.json" ] || [ -L "$d/killed.json" ]; then
    w=$(rget "$d/killed.json" wall_s s) || { echo BAD; return; }
    if secs_ok "$w"; then echo "$w"; else echo BAD; fi; return
  fi
  if [ -f "$d/attempt.json" ]; then
    w=$(grep -o '"elapsed_s": [^,}]*[,}]' "$d/attempt.json" | head -1 | sed 's/^"elapsed_s": //; s/[,}]$//')
    if [[ "$w" =~ ^(0|[1-9][0-9]{0,11})$ ]]; then echo "$w"; else echo BAD; fi; return
  fi
  echo UNKNOWN
}
att5(){ # 이 사다리의 시도 목록 '경로=run_id' (경로 바이트 순 · 빈칸으로 · run_id 를 못 읽으면 -) — 끝 기록 final.json 에 묶는다 (검사기 attempts_of 와 같다 · Codex EO P2)
  local d out="" rid lst
  lst=$(for d in "run/${JOB}_A5" "run/${JOB}_c1" "run/${JOB}_c2" run_aborted/*; do
          case "$d" in run_aborted/*) [[ "${d#run_aborted/}" =~ ^${JOB}_(A5|c1|c2)_[[:digit:]]+$ ]] || continue;; esac
          [ -d "$d" ] && printf '%s\n' "$d"; done | LC_ALL=C sort)
  for d in $lst; do
    rid=$(rget "$d/attempt.start" run_id s) || rid=-
    [ -n "$rid" ] || rid=-
    out="$out${out:+ }$d=$rid"
  done
  printf '%s' "$out"
}

hist5(){ # run/status.tsv 의 시도 줄 (run_id · 변형) 이 지금 · 보존 폴더의 끝난 시도 (attempt.json 있음) 로 설명되는가 → '-' 또는 사유 (검사기 history_problems 와 같다 · Codex EP P1 Q-EP-4a)
  local S=run/status.tsv d have
  { [ -e "$S" ] || [ -L "$S" ]; } || { echo -; return; }
  [ -f "$S" ] || { echo status_not_file; return; }
  [ -s "$S" ] || { echo status_empty; return; }                                                       # 0 바이트 — 머리 줄도 없다 (머리만 있는 파일은 받는다 · Codex EQ P1)
  tr -d '\000' < "$S" 2>/dev/null | cmp -s - "$S" 2>/dev/null || { echo status_nul; return; }
  [ "$(tail -c 1 "$S" | od -An -tx1 | tr -d ' \n')" = 0a ] || { echo status_no_final_newline; return; }  # 잘린 줄 (쓰다 끊김)
  u8f "$S" || { echo utf8_status.tsv; return; }
  have=$(for d in "run/${JOB}_A5" "run/${JOB}_c1" "run/${JOB}_c2" run_aborted/*; do
           case "$d" in run_aborted/*) [[ "${d#run_aborted/}" =~ ^${JOB}_(A5|c1|c2)_[[:digit:]]+$ ]] || continue;; esac
           { [ -d "$d" ] && [ -f "$d/attempt.json" ]; } || continue
           printf '%s\t%s\t%s\n' "$(rget "$d/attempt.start" run_id s)" "$(rget "$d/attempt.start" attempt s)" "$(tpl5 "$d/attempt.json" "$ATT1_T" | sed -n '8s/^=//p')"; done)
  printf '%s\n' "$have" | LC_ALL=C awk -F'\t' -v J="$JOB" -v H='job\trung\tstage\trc\tstatus\tn_elec\tdE\tdeps\twhy\twall_s\trun_id' '
    NR == FNR { if ($0 != "") have[$1 "\t" $2] = $3; next }
    FNR == 1 { if ($0 != H) { print "status_header"; x = 1; exit } next }
    { i++
      if (NF != 11 || $1 != J) { print "status_row_" i "_form"; x = 1; exit }
      k = $11 "\t" $2
      if (!(k in have)) { print "status_row_" i "_no_attempt"; x = 1; exit }
      if ($10 != have[k]) { print "status_row_" i "_elapsed"; x = 1; exit }                 # 이력 줄 벽시계 = 그 시도 끝 기록 elapsed_s — 합산 전에 (Codex ER Q-ER-3①)
      if (k in seen) { print "status_row_" i "_twice"; x = 1; exit }
      seen[k] = 1 }
    END { if (!x) print "-" }' - "$S"
}
u8ok(){ printf '%s' "$1" | u8in; }    # $1 글 → 0 · 1 — 손으로 넣은 글을 기록에 쓰기 전에 (Codex EP 조건부 Q-EP-2)
u8f(){ u8in < "$1"; }                # $1 파일 → 0 · 1 — 기록을 읽어 쓰기 전에 (영수증 · 끊김 · 시작 · 끝 기록 · 장부 · 이력 — 저장 뒤 바이트 손상 · Codex EQ P1)
nbw(){ [ -n "$(printf '%s' "$1" | tr -d ' \t\n\v\f\r')" ]; }       # 쓸 때 필수 칸 — 빈칸 문자 여섯 (공백 · 탭 · LF · VT · FF · CR) 밖 글자 하나 (검사기 _blank 와 같은 집합 · Codex EQ P1)
nbj(){ printf '%s\n' "$1" | LC_ALL=C awk '{ gsub(/\\[tnrf]|\\u00(0[9a-dA-D]|20)| /, ""); exit ($0 == "") }'; }   # 읽을 때 (JSON 원문) — 공백 · 빈칸 이스케이프 (\t \n \r \f · \u0009–\u000d ·  ) 를 걷고 남는 글자 하나 (검사기 _blank)
u8in(){ # 표준 입력 바이트 → 0 (UTF-8 로 온전함 · RFC 3629 — 검사기 쪽 기준은 Python bytes.decode('utf-8')) · 1 (아님)
  od -An -v -tx1 | LC_ALL=C awk 'BEGIN { for (k = 0; k < 256; k++) v[sprintf("%02x", k)] = k }
    { for (i = 1; i <= NF; i++) b[++n] = v[$i] }
    END { i = 1
      while (i <= n) {
        c = b[i]
        if (c < 128) { i++; continue }
        if (c >= 194 && c <= 223) { L = 1; lo = 128; hi = 191 }
        else if (c == 224) { L = 2; lo = 160; hi = 191 }
        else if (c == 237) { L = 2; lo = 128; hi = 159 }
        else if (c >= 225 && c <= 239) { L = 2; lo = 128; hi = 191 }
        else if (c == 240) { L = 3; lo = 144; hi = 191 }
        else if (c >= 241 && c <= 243) { L = 3; lo = 128; hi = 191 }
        else if (c == 244) { L = 3; lo = 128; hi = 143 }
        else exit 1
        if (i + L > n || b[i + 1] < lo || b[i + 1] > hi) exit 1
        for (q = 2; q <= L; q++) if (b[i + q] < 128 || b[i + q] > 191) exit 1
        i += L + 1
      }
      exit 0 }'
}
fin_ok(){ # run/final.json → '-' 또는 사유 — 끝 기록 전체 (UTF-8 · REC1 · 칸 · fin5 가 쓰는 code/state 조합만 · attempts = 지금 시도 목록 att5) — 검사기 final_problem 과 같다 (Codex EP 조건부 · EQ P1)
  local R a c s
  u8f run/final.json || { echo utf8_final.json; return; }
  R=$(rec5 run/final.json) || { echo final_form; return; }
  c=$(rf "$R" code i) || { echo final_form; return; }
  { s=$(rf "$R" state s) && rf "$R" why s > /dev/null && rf "$R" written_utc s > /dev/null && rf "$R" written_s i > /dev/null; } || { echo final_fields; return; }
  case "$c:$s" in 0:OK|1:NO_PRIMARY|1:CLOSED|5:CAP|6:ENV|8:REVIEW) ;; *) echo final_code_state; return;; esac
  a=$(rf "$R" attempts s) || { echo final_no_attempts; return; }
  [ "$a" = "$(att5)" ] || { echo final_attempts_differ; return; }
  echo -
}

# ── 트리 관문 (Codex EQ · 다섯 번째 NO-GO 뒤 구조로 · 러너 = 검사기 tree_problems · 같은 규칙 · 같은 사유 낱말) ──
#   어디서: 기록 명령 (--infra-abort · --infra-wall · --killed · --reset-w0) · PACK_ONLY · 다시 돌림 (잠금 다음 · 무엇을 쓰기 전 · 끝난 사다리 재사용 포함) ·
#   단 발사 직전 (cap_gate) · A5 WAVECAR 지우기 · 끝 기록 쓰기 전 (drop5 · fin5 · Codex ER) · 포장 (pack — 기존 반송본을 덮어쓰기 전). 첫 사유에서 종료 8 · 아무것도 쓰지 않는다 (원본 보존).
#   차례: 이름 (files5 — 준비 폴더는 띄우기 전 이름만 · Codex ER) → 시도 폴더마다 시작 · 끝 · 끊김 기록 (rec_dir5) → 중단 장부 · 영수증 · 시도 이력 (ledger5 → hist5) → 끝 기록 (fin_ok) →
#         시작점 (sp_rec5) → ⓪ 기록 (w0_rec5) → 기존 반송본 (tgz5 — 러너 쪽만: 검사기는 반송본 하나만 받는다 · 완전한 행 · 영수증 벽시계도 후퇴 없음 · Codex ER).
#   ⚠ 못 하는 것: 모든 기록을 서로 맞게 함께 고친 트리 (선언한 위협 범위 밖 · §1b) · 업체 시계 · 노드 시계 · VASP_CMD 가 시도 폴더에 표준 밖 이름을 쓰면 거짓 멈춤 (8 · 연락).
tpl5(){ # $1 파일 · $2 틀 (\001 = 문자열 — 따옴표 · 역슬래시 · 제어 바이트 없음 · \002 = 음 아닌 정수 — 선행 0 없음 · 16 자리 이하 · 나머지 글자 그대로) →
  #       맞으면 '=값' 줄들 (틀 차례) · 아니면 출력 없이 1 — 한 줄 (+ 끝 줄바꿈 하나) · NUL 없음 · 검사기 tpl_parse 와 같은 규칙 (잘린 JSON · 정수 칸의 소수 → 거부)
  [ -f "$1" ] || return 1
  tr -d '\000' < "$1" 2>/dev/null | cmp -s - "$1" 2>/dev/null || return 1
  LC_ALL=C awk -v T="$2" 'BEGIN { for (k = 1; k < 256; k++) ord[sprintf("%c", k)] = k }
    { m++; s = $0 }
    END {
      if (m != 1) exit 1
      L = length(s); n = length(T); i = 1; out = ""
      for (p = 1; p <= n; p++) {
        c = substr(T, p, 1)
        if (c == "\001") {
          if (substr(s, i, 1) != "\"") exit 1
          j = i + 1
          while (j <= L) { d = substr(s, j, 1); if (d == "\"") break; if (d == "\\" || ord[d] < 32) exit 1; j++ }
          if (j > L) exit 1
          out = out "=" substr(s, i + 1, j - i - 1) "\n"; i = j + 1
        } else if (c == "\002") {
          j = i; while (j <= L && substr(s, j, 1) ~ /^[0-9]$/) j++
          v = substr(s, i, j - i)
          if (v !~ /^(0|[1-9][0-9]*)$/ || length(v) > 16) exit 1
          out = out "=" v "\n"; i = j
        } else {
          if (substr(s, i, 1) != c) exit 1
          i++
        }
      }
      if (i <= L) exit 1
      printf "%s", out
    }' "$1"
}
att_ok5(){ # $1 끝난 시도 폴더 · $2 attempt.start (rec5) · $3 attempt.json 값 (tpl5) → '-' 또는 사유 — 신원 (run_id · t_start = 시작 기록) · 봉인 (sha 표 = 지금 파일 · POTCAR 본문 빼고 열 개)
  local d=$1 i=11 f k V
  mapfile -t V <<< "$3"
  [ "${#V[@]}" = 22 ] || { echo att_form; return; }
  V=("${V[@]#=}")
  [ "${V[3]}" = "$(rf "$2" run_id s)" ] || { echo end_run_id; return; }
  [ "${V[5]}" = "$(rf "$2" t_start i)" ] || { echo end_t_start; return; }
  [ "${V[0]}" = "$(rf "$2" job s)" ] || { echo end_job; return; }                       # 끝 기록 신원 = 시작 기록 (잡 · 변형 · stage — 시작 기록은 폴더와 맞는다 · Codex ER Q-ER-5)
  [ "${V[1]}" = "$(rf "$2" attempt s)" ] || { echo end_attempt; return; }
  [ "${V[2]}" = "$(rf "$2" stage s)" ] || { echo end_stage; return; }
  for f in INCAR POSCAR KPOINTS POTCAR OUTCAR OSZICAR WAVECAR.info stdout.log POTCAR.titel POTCAR.species.sha256 attempt.start; do
    k=${V[$i]}; i=$((i + 1))
    [ "$f" != POTCAR ] || continue
    if [ -f "$d/$f" ]; then [ "$k" = "$(h "$d/$f")" ] || { echo "seal_$f"; return; }
    else [ -z "$k" ] || { echo "seal_$f"; return; }; fi
  done
  printf '%s\n' "${V[14]}" | cmp -s - "$d/POTCAR.sha256" || { echo end_potcar_sha; return; }      # 끝 기록의 POTCAR 해시 = 현장 POTCAR.sha256 (POTCAR 본문은 지운다 · Codex ER Q-ER-5)
  echo -
}
killed_rec5(){ # $1 진행 폴더 · $2 단 · $3 attempt.start (rec5) → '-' 또는 사유 — 끊김 기록 문법 · 칸 · 빈칸 · 결속 (잡 · 단 · run_id · 초 · 기록 시각 ≥ 시작) — 그 시간을 쓰기 전에 (Codex EQ P0)
  local K k t0 rs
  K=$(rec5 "$1/killed.json") || { echo killed_json_form; return; }
  for k in job rung run_id wall_s sched_job_id cancel_utc reason osz_rows recorded_utc; do rf "$K" "$k" s > /dev/null || { echo "killed_json_field_$k"; return; }; done
  rf "$K" recorded_s i > /dev/null || { echo killed_json_field_recorded_s; return; }
  for k in sched_job_id cancel_utc reason; do nbj "$(rf "$K" "$k" s)" || { echo "killed_json_blank_$k"; return; }; done
  { [ "$(rf "$K" job s)" = "$JOB" ] && [ "$(rf "$K" rung s)" = "$2" ]; } || { echo killed_job_or_rung; return; }
  [ "$(rf "$K" run_id s)" = "$(rf "$3" run_id s)" ] || { echo killed_run_id; return; }
  secs_ok "$(rf "$K" wall_s s)" || { echo killed_wall_s; return; }
  t0=$(rf "$3" t_start i); rs=$(rf "$K" recorded_s i)
  { [ -n "$t0" ] && [ -n "$rs" ] && [ "$rs" -ge "$t0" ]; } 2>/dev/null || { echo killed_recorded_s; return; }
  echo -
}
rec_dir5(){ # $1 시도 폴더 (run/<잡>_<단> · run_aborted/<잡>_<단>_<k>) · $2 단 → '-' 또는 사유 — 시작 기록 → UTF-8 → 끝 기록 (틀 · 신원 · 봉인) → 끊김 기록 (자리 · 문법 · 결속) → 진행 폴더의 영수증
  local d=$1 S A x f
  [ -f "$d/attempt.start" ] || { echo no_start; return; }
  x=$(start_id "$d" "$2"); [ "$x" = - ] || { echo "$x"; return; }
  for f in attempt.start attempt.json killed.json infra_abort.json; do
    if [ -f "$d/$f" ] && ! u8f "$d/$f"; then echo "utf8_$f"; return; fi
  done
  S=$(rec5 "$d/attempt.start")
  if [ -f "$d/attempt.json" ]; then
    A=$(tpl5 "$d/attempt.json" "$ATT1_T") || { echo att_form; return; }
    x=$(att_ok5 "$d" "$S" "$A"); [ "$x" = - ] || { echo "$x"; return; }
  fi
  if [ -f "$d/killed.json" ]; then
    case "$d" in run_aborted/*) echo killed_in_aborted; return;; esac                  # 0 스텝 중단 폴더에 끊김 (행 ≥ 1) 기록 — 서로 안 맞는다
    [ ! -f "$d/attempt.json" ] || { echo end_and_killed; return; }                      # 끝난 시도에 끊김 기록 — 남의 killed.json 으로 시간을 바꾸지 못하게 (Codex EQ P0)
    x=$(killed_rec5 "$d" "$2" "$S"); [ "$x" = - ] || { echo "$x"; return; }
  fi
  case "$d" in run/*) [ ! -f "$d/infra_abort.json" ] || { echo stray_receipt; return; };; esac     # 영수증은 run_aborted/ 에만 (Codex EP P1)
  echo -
}
files5(){ # → '-' 또는 사유 — run/ · run_aborted/ · 시도 폴더의 이름 (모르는 이름 · 잔여 *.part · 링크 · 하위 폴더 → 멈춤 · 재포장이 현장 오류를 지우지 못하게 · Codex EQ P1)
  local f b d e
  for f in run/* run/.[!.]* run/..?*; do
    { [ -e "$f" ] || [ -L "$f" ]; } || continue
    b=${f#run/}
    case "$b" in
      "${JOB}_A5"|"${JOB}_c1"|"${JOB}_c2"|.a5.lock|".prep_${JOB}_A5"|".prep_${JOB}_c1"|".prep_${JOB}_c2") { [ -d "$f" ] && [ ! -L "$f" ]; } || { echo "run_entry_$b"; return; };;
      env.txt|status.tsv|infra_aborts.tsv|w0_check.json|start_point.json|final.json) { [ -f "$f" ] && [ ! -L "$f" ]; } || { echo "run_entry_$b"; return; };;
      *) echo "run_entry_$b"; return;;
    esac
  done
  for f in run_aborted/* run_aborted/.[!.]* run_aborted/..?*; do
    { [ -e "$f" ] || [ -L "$f" ]; } || continue
    b=${f#run_aborted/}
    { [[ "$b" =~ ^${JOB}_(A5|c1|c2)_[1-9][0-9]*$ ]] && [ -d "$f" ] && [ ! -L "$f" ]; } || { echo "aborted_entry_$b"; return; }
  done
  for d in "run/${JOB}_A5" "run/${JOB}_c1" "run/${JOB}_c2" run_aborted/*; do
    [ -d "$d" ] || continue
    for f in "$d"/* "$d"/.[!.]* "$d"/..?*; do
      { [ -e "$f" ] || [ -L "$f" ]; } || continue
      e=${f##*/}
      { [ -f "$f" ] && [ ! -L "$f" ] && [[ "$e" =~ ^($RET_ALLOW|$RET_FORBID|$ATT_EXTRA)$ ]]; } || { echo "file_$f"; return; }
    done
  done
  for d in "run/.prep_${JOB}_A5" "run/.prep_${JOB}_c1" "run/.prep_${JOB}_c2"; do     # 준비 폴더 — 러너가 띄우기 전에 쓰는 이름만 (VASP 출력이 있으면 실행 기록 · 지우지 않고 멈춤 · Codex ER Q-ER-1①)
    [ -d "$d" ] || continue
    for f in "$d"/* "$d"/.[!.]* "$d"/..?*; do
      { [ -e "$f" ] || [ -L "$f" ]; } || continue
      e=${f##*/}
      { [ -f "$f" ] && [ ! -L "$f" ] && [[ "$e" =~ ^($PREP_ALLOW)$ ]]; } || { echo "prep_$f"; return; }
    done
  done
  echo -
}
sp_rec5(){ # run/start_point.json → '-' 또는 사유 — UTF-8 · REC1 · 칸 (from · path · sha256 · head 문자열 · written_s 정수) — sp_load 가 읽기 전에 (검사기 sp_problem)
  local R k
  u8f run/start_point.json || { echo utf8_start_point.json; return; }
  R=$(rec5 run/start_point.json) || { echo start_point_form; return; }
  for k in from path sha256 head; do rf "$R" "$k" s > /dev/null || { echo start_point_form; return; }; done
  rf "$R" written_s i > /dev/null || { echo start_point_form; return; }
  echo -
}
w0_rec5(){ # run/w0_check.json → '-' 또는 사유 — UTF-8 · 틀 (w0_check 의 printf 그대로 · 잘림 → 거부) (검사기 w0_problem)
  u8f run/w0_check.json || { echo utf8_w0_check.json; return; }
  tpl5 run/w0_check.json "$W0_T" > /dev/null || { echo w0_form; return; }
  echo -
}
tgz5(){ # 기존 반송본 (a5_return.tgz + .sha256) ↔ 지금 트리 → '-' 또는 사유 — 덮어쓰기 · 이어 돌리기 전에 (Codex EQ P1 Q-EQ-3 · 러너 쪽만):
  #   둘 다 없으면 볼 것 없음 · 하나만 있음 · sha 꼴 · sha 다름 · 못 읽음 → 멈춤 · 반송본의 끝 기록 (run/final.json) = 지금 끝 기록 (바이트) ·
  #   반송본의 시도마다 (attempt.start run_id) 지금 트리에 그 시도가 있고 (진행 폴더 → 그 자리 또는 같은 단의 보존 폴더) · 반송본에 있던 attempt.json · killed.json 은 바이트로 같고 ·
  #   보존 폴더의 시도는 같은 자리 (영수증은 장부 규칙 · --infra-wall 이 벽시계를 채우므로 바이트는 안 본다) — 지금 트리 ⊇ 반송본 (완료 기록 없는 중간 포장 허용)
  local T x
  { [ -e a5_return.tgz ] || [ -L a5_return.tgz ] || [ -e a5_return.tgz.sha256 ] || [ -L a5_return.tgz.sha256 ]; } || { echo -; return; }
  { [ -f a5_return.tgz ] && [ ! -L a5_return.tgz ] && [ -f a5_return.tgz.sha256 ] && [ ! -L a5_return.tgz.sha256 ]; } || { echo tgz_pair; return; }
  { [ "$(awk 'END { print NR }' a5_return.tgz.sha256 2>/dev/null)" = 1 ] && grep -qxE '[0-9a-f]{64}  a5_return\.tgz' a5_return.tgz.sha256; } || { echo tgz_sha_form; return; }
  sha256sum -c --status a5_return.tgz.sha256 2>/dev/null || { echo tgz_sha; return; }
  T=$(mktemp -d 2>/dev/null) && [ -d "$T" ] || { echo tgz_tmp; return; }
  x=$(tgz5_in "$T"); rm -rf "$T"; echo "${x:-tgz_fail}"
}
tgz5_in(){ # $1 임시 폴더 — tgz5 의 대조 (반송본의 기록 파일만 꺼낸다)
  local T=$1 f d b st rid c x e
  tar tzf a5_return.tgz > "$T/m" 2>/dev/null || { echo tgz_list; return; }
  grep -E "^(run/final\.json|run/${JOB}_(A5|c1|c2)/(attempt\.start|attempt\.json|killed\.json|infra_abort\.json|OSZICAR)|run_aborted/${JOB}_(A5|c1|c2)_[1-9][0-9]*/(attempt\.start|attempt\.json|killed\.json|infra_abort\.json|OSZICAR))$" "$T/m" > "$T/w"
  mkdir "$T/x" || { echo tgz_tmp; return; }
  if [ -s "$T/w" ]; then tar xzf a5_return.tgz -C "$T/x" -T "$T/w" 2>/dev/null || { echo tgz_extract; return; }; fi
  if [ -f "$T/x/run/final.json" ]; then cmp -s "$T/x/run/final.json" run/final.json || { echo tgz_final_differs; return; }; fi
  for f in "$T"/x/run/*/attempt.start "$T"/x/run_aborted/*/attempt.start; do
    [ -f "$f" ] || continue
    d=${f%/attempt.start}; b=${d#"$T"/x/}; st=${b#*/"${JOB}"_}; st=${st%%_*}
    rid=$(rget "$f" run_id s) || { echo "tgz_start_form_$b"; return; }
    c=""
    case "$b" in
      run_aborted/*) [ "$(rget "$b/attempt.start" run_id s 2>/dev/null)" = "$rid" ] && c=$b;;          # 보존 폴더는 옮기지 않는다 — 같은 자리 · 같은 run_id (영수증은 장부 규칙)
      *) for x in "$b" run_aborted/"${JOB}_${st}"_*; do                                                    # 진행 폴더는 그 자리 또는 --infra-abort 로 옮긴 같은 단의 보존 폴더
           [ -f "$x/attempt.start" ] && [ "$(rget "$x/attempt.start" run_id s)" = "$rid" ] && { c=$x; break; }
         done;;
    esac
    [ -n "$c" ] || { echo "tgz_attempt_missing_$b"; return; }
    for e in attempt.json killed.json; do
      [ ! -f "$d/$e" ] || cmp -s "$d/$e" "$c/$e" || { echo "tgz_end_differs_$b/$e"; return; }
    done
    if [ -f "$d/OSZICAR" ]; then                                                                      # 반송본이 본 완전한 행은 줄지 않는다 (출력 전 체크포인트로 되돌린 시도 · Codex ER Q-ER-4)
      x=$(row_scan "$d" "$st"); e=$(row_scan "$c" "$st")
      [ "${e%% *}" -ge "${x%% *}" ] 2>/dev/null || { echo "tgz_rows_lost_$b"; return; }
    fi
    if [ -f "$d/infra_abort.json" ]; then                                                             # 영수증 벽시계는 UNKNOWN → 확정값으로만 (확정값이 바뀌거나 UNKNOWN 으로 되돌면 멈춤 · Codex ER Q-ER-4)
      x=$(rget "$d/infra_abort.json" wall_s s); e=$(rget "$c/infra_abort.json" wall_s s)
      [ "$x" = UNKNOWN ] || [ "$e" = "$x" ] || { echo "tgz_receipt_wall_$b"; return; }
    fi
  done
  echo -
}
tree5(){ # 트리 관문 — '-' 또는 첫 사유 (검사기 tree_problems + ledger_problems 와 같은 규칙 · 같은 낱말)
  local x d st
  x=$(files5); [ "$x" = - ] || { echo "$x"; return; }
  for d in "run/${JOB}_A5" "run/${JOB}_c1" "run/${JOB}_c2" run_aborted/*; do
    [ -d "$d" ] || continue
    st=${d#*/"${JOB}"_}; st=${st%%_*}
    x=$(rec_dir5 "$d" "$st"); [ "$x" = - ] || { echo "$d:$x"; return; }
  done
  x=$(ledger5); [ "$x" = - ] || { echo "$x"; return; }
  if [ -e run/final.json ]; then x=$(fin_ok); [ "$x" = - ] || { echo "$x"; return; }; fi
  if [ -e run/start_point.json ]; then x=$(sp_rec5); [ "$x" = - ] || { echo "$x"; return; }; fi
  if [ -e run/w0_check.json ]; then x=$(w0_rec5); [ "$x" = - ] || { echo "$x"; return; }; fi
  x=$(tgz5); [ "$x" = - ] || { echo "$x"; return; }
  echo -
}
tree_gate(){ # $1 어디서 — 트리 관문이 '-' 가 아니면 아무것도 쓰지 않고 종료 8 (원본 보존 · 잠금은 EXIT trap 이 지운다)
  local x; x=$(tree5)
  [ "$x" = - ] && return 0
  echo "⛔ 트리 관문 ($1) — ${x:-판독 실패} — 아무것도 쓰거나 띄우거나 포장하지 않고 멈춘다 (종료 8 · run/ · run_aborted/ · a5_return.tgz 그대로). 이 줄을 그대로 보내 주세요 (1저자)"
  exit 8
}

# ── 완전한 전자 반복행 (검사기 row_gate 와 같은 규칙 · selftest 가 같은 탐침으로 대조 · Codex EO P0 · EP P0) ──
#   행꼴 = 줄 맨 앞 1–4 글자 + ':' · 완전한 행 = 줄바꿈으로 끝난 행꼴 줄 · 머리가 그 단의 허용 머리 그대로 · ':' 뒤 빈칸 · 칸 6 또는 7 (N E dE d eps ncg rms [rms(c)]) ·
#   숫자로 읽힘 — N 양의 정수 · ncg 정수 · 나머지 실수 (부호 · 소수점 · E 지수 두 자리까지 — NaN · *** · inf · 글자는 아니다) · 칸마다 24 글자 이하 (늘 유한 · Codex EQ P0).
#   사유: '-' · row_header_<머리> (허용 밖 머리) · incomplete_row (줄바꿈 있는 덜 쓴 행꼴 줄 · 완전한 행 0 인데 행꼴 끝 조각 또는 콜론 앞에서 잘린 머리 — 앞 빈칸 · 탭을 걷고 글자 1–4 · 앞 빈칸 뒤 'N' 만 열 제목) · nul_bytes.
#   완전한 행 ≥ 1 뒤 줄바꿈 없는 끝 조각 (행꼴 · 머리 조각) 은 세지 않고 넘어간다 (스케줄러 끊김의 잘린 꼬리).
row_scan(){ # $1 시도 폴더 · $2 단 → "완전한행수 사유"
  local f=$1/OSZICAR H nl
  H=$(stage_hdr "$2"); [ -n "$H" ] || { echo "0 unknown_stage"; return; }
  { [ -f "$f" ] && [ -r "$f" ]; } || { echo "0 -"; return; }
  tr -d '\000' < "$f" 2>/dev/null | cmp -s - "$f" 2>/dev/null || { echo "0 nul_bytes"; return; }
  nl=$(tr -dc '\n' < "$f" | wc -c | tr -d ' ')
  LC_ALL=C awk -v A="^(${H})\$" -v F="^[ \t]*(${H}):[ \t]+" -v NL="${nl:-0}" -v T6='N E dE d eps ncg rms' -v T7='N E dE d eps ncg rms rms(c)' -v R='^[+-]?([0-9]+[.]?[0-9]*|[.][0-9]+)([Ee][+-]?[0-9][0-9]?)?$' '
    /^[ \t]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:/ {
      h = $0; sub(/^[ \t]*/, "", h); sub(/:.*/, "", h); gsub(/ /, "", h)
      if (h !~ A) { if (bad == "") bad = "row_header_" h; next }
      if (NR > NL) { tp = 1; next }
      r = $0
      if (r !~ F) { p++; next }
      sub(F, "", r); sub(/[ \t]+$/, "", r)
      k = (r == "") ? 0 : split(r, t, /[ \t]+/)
      lg = 1; for (q = 1; q <= k; q++) if (length(t[q]) > 24) lg = 0                                  # 칸 길이 ≤ 24 — 늘 유한 (Codex EQ P0 · 310 자리)
      if (lg && (k == 6 || k == 7) && t[1] ~ /^[1-9][0-9]*$/ && t[5] ~ /^[0-9]+$/ && t[2] ~ R && t[3] ~ R && t[4] ~ R && t[6] ~ R && (k == 6 || t[7] ~ R)) n++; else p++
    }
    !/^[ \t]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:/ {                                                # 행꼴이 아닌 줄 — 0 스텝이면 빈 줄 · 열 제목 (끝 조각은 그 앞부분) 만 (Codex ER Q-ER-2)
      v = $0; gsub(/[ \t]+/, " ", v); sub(/^ /, "", v); sub(/ $/, "", v)
      if (v != "" && !($0 ~ /^[ \t]/ && (NR <= NL ? (v == T6 || v == T7) : index(T7, v) == 1))) ux = 1 }
    NR > NL { u = $0; sub(/^[ \t]+/, "", u); if (u ~ /^[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?$/ && !(u != $0 && u ~ /^N *$/)) tp = 1 }     # 머리 조각 (앞 빈칸 걷고 · 열 제목 'N' 만 0 스텝 · Codex EQ P0)
    END { if (bad != "") print n + 0, bad; else if (p > 0 || (tp && n == 0)) print n + 0, "incomplete_row"; else if (ux && n == 0) print 0, "unexplained_line"; else print n + 0, "-" }' "$f"
}
osz_feed(){ # 판정 계약 입력 — 줄바꿈으로 끝난 줄만 (끝 조각은 뺀다) · 그 단의 허용 머리 → DAV: (검사기 feed5 와 같다 · row_scan 사유가 없을 때만 쓴다)
  local nl; nl=$(tr -dc '\n' < "$1/OSZICAR" 2>/dev/null | wc -c | tr -d ' ')
  LC_ALL=C awk -v H="^[ \t]*(${HDR}):" -v NL="${nl:-0}" 'NR > NL { exit }
    { if (match($0, H)) { l = $0; sub(/[^ \t].*$/, "", l); print l "DAV:" substr($0, RLENGTH + 1) } else print }' "$1/OSZICAR" 2>/dev/null
}
judge5(){ # $1 시도 폴더 · $2 단 → "상태 행수 dE deps 사유" (judge 와 같은 꼴) — 완전한 행 판독 (row_scan) 뒤 외주 2차 판정 계약에 완전한 행만
  local d=$1 HDR g n why
  HDR=$(stage_hdr "$2"); [ -n "$HDR" ] || { echo "SCF_UNVERIFIED 0 NA NA unknown_stage"; return; }
  [ -f "$d/OSZICAR" ] || { judge_r2 "$d"; return; }
  g=$(row_scan "$d" "$2"); n=${g%% *}; why=${g#* }
  [ -n "$g" ] || { judge_r2 "$d"; return; }
  if [ "$why" != "-" ]; then echo "SCF_UNVERIFIED ${n:-0} NA NA $why"; return; fi
  judge_r2 "$d"
}
stat5(){ # $1 시도 폴더 · $2 단 · $3 시작 WAVECAR sha (c1 · c2) → 상태. 순서 (검사기와 같다): 행 0 → SCF_UNVERIFIED (재시작 확인 전 · 리뷰 P2(f)) →
  #        c1 · c2 재시작 (sha 셋 · 문구 · c 단 OUTCAR NKPTS·NBANDS·ENCUT = 시작 WAVECAR 머리 — 리뷰 P3) → 판정. A5 는 재시작이 자격이 아니다
  local d=$1 st=$2 ss=${3:-} j n
  [ -f "$d/attempt.json" ] || { echo INCOMPLETE_ATTEMPT; return; }
  j=$(judge5 "$d" "$st"); n=$(printf '%s\n' "$j" | awk '{ print $2; exit }')
  [ "$n" = 0 ] && { echo SCF_UNVERIFIED; return; }
  case "$st" in c1|c2)
    { grep -q '"honoured": 1' "$d/WAVECAR.info" 2>/dev/null && [ -n "$ss" ] && [ "$(wsha "$d/WAVECAR.info" src_sha256)" = "$ss" ] \
      && [ "$(wsha "$d/WAVECAR.info" copied_sha256)" = "$ss" ] && [ "$(wsha "$d/WAVECAR.info" end_sha256)" = "$ss" ] \
      && grep -aqE -e "$RESTART_RE" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null \
      && [ "$(out_num "$d" NKPTS)" = "${SP_NK:-x}" ] && [ "$(out_num "$d" NBANDS)" = "${SP_NB:-x}" ] && enc_eq "$(out_num "$d" ENCUT)" "${SP_EN:-x}"; } \
      || { echo RESTART_NOT_HONOURED; return; };;
  esac
  echo "${j%% *}"
}
echo5(){ # $1 시도 폴더 · $2 변형 → "-" (맞음) 또는 "키:값!=기대,…" — a5 가 바꾼 설정의 OUTCAR 해석값 (입력 에코 구획 INCAR: … POTCAR: 은 뺀다) ·
  #        검사기 echo5 와 같은 키 · 같은 정규식 꼴 · 같은 허용치 (러너가 1저자 멈춤을 거는 부분집합 · 나머지 설정은 검사기 audit5)
  local ne ld ia am an mx tm
  case "$2" in
    A5c|A5f) ne=300; ld=F; ia=38; am=0.1; an=0.01; mx=200; tm="";;
    c1) ne=400; ld=T; ia=38; am=0.1; an=0.01; mx=200; tm="";;
    c2) ne=400; ld=T; ia=58; am=""; an=""; mx=""; tm=0.1;;
    *) echo "variant:$2"; return;;
  esac
  [ -f "$1/OUTCAR" ] || { echo "OUTCAR:missing"; return; }
  awk -v NE="$ne" -v LD="$ld" -v IA="$ia" -v AM="$am" -v AN="$an" -v MX="$mx" -v TM="$tm" '
    function isnum(s) { return s ~ /^[-+]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][-+]?[0-9]+)?$/ }
    function ab(x) { return x < 0 ? -x : x }
    function val(s, re,   t) { t = s; sub(re, "", t); if (match(t, /^[^; \t]+/)) return substr(t, 1, RLENGTH); return "" }
    function chk(k, g, w, tol) { if (w == "") return; if (g == "") { out = out k ":missing,"; return }
      if (!isnum(g) || ab(g - w) > tol + 1e-12) out = out k ":" g "!=" w "," }
    /^[ \t]*INCAR:[ \t]*$/ { skip = 1; next }
    skip { if ($0 ~ /^[ \t]*POTCAR:/) skip = 0; else next }
    /^[ \t]*NELM[ \t]*=[ \t]*[0-9]/ { x = val($0, "^[ \t]*NELM[ \t]*=[ \t]*"); if (match(x, /^[0-9]+/)) gne = substr(x, 1, RLENGTH) }
    /^[ \t]*IALGO[ \t]*=[ \t]*[0-9]/ { x = val($0, "^[ \t]*IALGO[ \t]*=[ \t]*"); if (match(x, /^[0-9]+/)) gia = substr(x, 1, RLENGTH) }
    /^[ \t]*AMIX[ \t]*=[ \t]*[^; \t]+[ \t]*;[ \t]*BMIX/ { gam = val($0, "^[ \t]*AMIX[ \t]*=[ \t]*") }
    /^[ \t]*AMIN[ \t]*=[ \t]*[^ \t]/ { t = $0; sub(/^[ \t]*AMIN[ \t]*=[ \t]*/, "", t); if (match(t, /^[^ \t]+/)) gan = substr(t, 1, RLENGTH) }
    /MAXMIX[ \t]*=[ \t]*-?[0-9]/ { t = $0; sub(/.*MAXMIX[ \t]*=[ \t]*/, "", t); if (match(t, /^-?[0-9]+/)) gmx = substr(t, 1, RLENGTH) }
    /^[ \t]*TIME[ \t]*=[ \t]*[^ \t]/ { t = $0; sub(/^[ \t]*TIME[ \t]*=[ \t]*/, "", t); if (match(t, /^[^ \t]+/)) gtm = substr(t, 1, RLENGTH) }
    /^[ \t]*LDIPOL[ \t]*=[ \t]*[^ \t]/ { t = $0; sub(/^[ \t]*LDIPOL[ \t]*=[ \t]*/, "", t); if (match(t, /^[^ \t]+/)) gld = substr(t, 1, RLENGTH) }
    END { out = ""
      chk("NELM", gne, NE, 0); chk("IALGO", gia, IA, 0); chk("AMIX", gam, AM, 1e-3); chk("AMIN", gan, AN, 1e-4); chk("MAXMIX", gmx, MX, 0); chk("TIME", gtm, TM, 1e-3)
      l = gld; gsub(/^\.+|\.+$/, "", l); l = toupper(substr(l, 1, 1))
      if (gld == "") out = out "LDIPOL:missing,"; else if (l != LD) out = out "LDIPOL:" gld "!=" LD ","
      print (out == "" ? "-" : out) }' "$1/OUTCAR" 2>/dev/null || echo "OUTCAR:unreadable"
}
hist_max(){ awk '/eigenvalues of \(default mixing \* dielectric matrix\)/ { if (c == 2 && k > m) m = k; c = 1; k = 0; next }
  c == 1 { c = 2; next }
  c == 2 { if (NF == 0) { if (k > m) m = k; c = 0; next } for (i = 1; i <= NF; i++) if ($i ~ /^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$/) k++ }
  END { if (c == 2 && k > m) m = k; print m + 0 }' "$1/OUTCAR" 2>/dev/null; }
rms_jump(){ # $1 시도 폴더 · $2 단 → rms(c) 가 직전 20 스텝 최솟값의 100 배를 넘은 마지막 스텝 (없으면 0) · 정보
  awk -v H="^[ \t]*($(stage_hdr "$2")):" 'function isnum(s) { return s ~ /^[-+]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][-+]?[0-9]+)?$/ }
    $0 ~ H { n++; v[n] = (NF >= 8 && isnum($8)) ? $8 + 0 : -1 }
    END { last = 0; for (k = 21; k <= n; k++) { if (v[k] < 0) continue; m = -1
            for (i = k - 20; i < k; i++) if (v[i] >= 0 && (m < 0 || v[i] < m)) m = v[i]
            if (m >= 0 && v[k] > 100 * m) last = k }
          print last }' "$1/OSZICAR" 2>/dev/null; }
watch5(){ # $1 시도 폴더 · $2 꼬리표 · $3 단 — 외주 2차 alarms (120 스텝 뒤 20 스텝마다) + a5 정보 (이력 길이 > 45 · rms(c) 급등) · 경보 ≠ 중단
  local d=$1 tag=$2 st=$3 last=100 o n a hm=0 rj=0 x
  while [ -f "$d/.running" ]; do
    sleep "${WATCH_S:-60}"
    [ -f "$d/OSZICAR" ] || continue
    o=$(alarms "$d"); n=${o%% *}; a=${o#* }
    case "$n" in ''|*[!0-9]*) continue;; esac
    if [ "$n" -ge 120 ] && [ "$n" -ge $((last + 20)) ]; then
      last=$((n - n % 20))
      if [ "$a" != "-" ]; then echo "$(utc) $tag step $n $a" >> "$d/warn.log"; log "⚠ 경보 $tag 스텝 $n: $a (중단 아님 · NELM 까지 돈다)"; fi
    fi
    [ "$st" = c2 ] && continue
    if [ "$hm" = 0 ]; then x=$(hist_max "$d"); case "$x" in ''|*[!0-9]*) ;; *) if [ "$x" -gt 45 ]; then hm=1; echo "$(utc) $tag info history_gt45 $x" >> "$d/warn.log"; fi;; esac; fi
    x=$(rms_jump "$d" "$st")
    case "$x" in ''|*[!0-9]*) ;; *) if [ "$x" -gt "$rj" ]; then rj=$x; echo "$(utc) $tag info rmsc_jump_step $x" >> "$d/warn.log"
      log "⚠ 정보 $tag rms(c) 급등 스텝 $x (직전 20 스텝 최솟값의 100 배 초과 · 중단 아님 — c1 이 실패하면 c2 는 혼합기를 안 쓴다)"; fi;; esac
  done
}

# ── 잠금 run/.a5.lock (원자적 mkdir) · 주인 = 기계 이름 + PID. 다른 기계의 잠금은 살아 있는지 알 수 없어 '살아 있음' 으로 본다 (리뷰 P2(d)) ──
LOCK=run/.a5.lock
lock_state(){ # → "상태 기계 PID" — none · live (이 기계 · 살아 있음) · stale (이 기계 · 죽음) · foreign (다른 기계 · 주인 기록 없음 포함)
  local o hh pp
  [ -d "$LOCK" ] || { echo "none - -"; return; }
  o=$(cat "$LOCK/owner" 2>/dev/null); hh=$(printf '%s\n' "$o" | awk '{ print $1; exit }'); pp=$(printf '%s\n' "$o" | awk '{ print $2; exit }')
  [ -n "$hh" ] || hh=-; [ -n "$pp" ] || pp=-
  if [ "$hh" != "$HOST" ]; then echo "foreign $hh $pp"
  elif [[ "$pp" =~ ^[0-9]+$ ]] && kill -0 "$pp" 2>/dev/null; then echo "live $hh $pp"
  else echo "stale $hh $pp"; fi
}
lock_say(){ # $1 상태 · $2 기계 · $3 PID · $4 거부한 것
  case "$1" in
    live) echo "⛔ run_a5.sh (기계 $2 · PID $3) 가 이 묶음에서 돌고 있다 — $4 는 그 실행이 끝난 뒤에";;
    *) echo "⛔ 다른 기계의 잠금 (기계 $2 · PID $3) — 여기서는 살아 있는지 알 수 없어 돌고 있는 것으로 본다 ($4 거부). 스케줄러로 그 잡이 끝났는지 확인한 뒤 'bash run_a5.sh --unlock $2 $3' 로 지우고 다시";;
  esac
}
read -r LK_S LK_H LK_P <<< "$(lock_state)"
lock_take(){ # $1 거부한 것 — 배타 잠금 (run/.a5.lock): 계산 · 기록 명령 · 포장이 같은 잠금을 검사부터 쓰기 끝까지 쥔다 (겹친 두 번째는 거부 · 첫 기록 보존 · Codex ER Q-ER-3②)
  if ! mkdir "$LOCK" 2>/dev/null; then
    read -r LK_S LK_H LK_P <<< "$(lock_state)"
    case "$LK_S" in
      live|foreign) lock_say "$LK_S" "$LK_H" "$LK_P" "$1"; exit 2;;
      stale) echo "⚠ 남은 잠금 (기계 $LK_H · PID $LK_P — 이 기계 · 살아 있지 않다) — 치우고 진행"; rm -rf "$LOCK";;
    esac
    mkdir "$LOCK" 2>/dev/null || { echo "⛔ 잠금 (run/.a5.lock) 을 만들 수 없다 — 다른 실행이 막 시작했을 수 있다"; exit 2; }
  fi
  printf '%s %s\n' "$HOST" "$$" > "$LOCK/owner" || { rm -rf "$LOCK"; echo "⛔ 잠금 주인을 적지 못했다"; exit 2; }
  trap 'rm -rf "$LOCK"' EXIT; trap 'exit 143' TERM; trap 'exit 129' HUP; trap 'exit 130' INT
}
if [ "${1:-}" != --unlock ] && { [ $# -gt 0 ] || [ "${PACK_ONLY:-0}" = 1 ]; }; then
  case "$LK_S" in live|foreign) lock_say "$LK_S" "$LK_H" "$LK_P" "기록 · 포장 명령"; exit 2;; esac
fi
'''

RUN_A5_CLI = r'''
# ── 끝난 사다리 (run/final.json) 에는 기록을 더하지 않는다 · 뒤 단이 있으면 앞 단 기록을 고치지 않는다 (리뷰 P1-1 · P0-2(c)) ──
later5(){ # $1 단 → 그 뒤 단의 폴더 · 기록 이름 (없으면 빈 출력)
  local x
  case "$1" in
    A5) for x in "run/${JOB}_c1" "run/${JOB}_c2" run/start_point.json; do [ -e "$x" ] && { echo "$x"; return; }; done
        compgen -G "run_aborted/${JOB}_c[12]_*" | head -1;;
    c1) [ -e "run/${JOB}_c2" ] && { echo "run/${JOB}_c2"; return; }
        compgen -G "run_aborted/${JOB}_c2_*" | head -1;;
  esac
}
case "${1:-}" in --infra-abort|--infra-wall|--killed|--reset-w0)
  [ ! -f run/final.json ] || { echo "⛔ 이 사다리는 끝났다 (run/final.json: 코드 $(rget run/final.json code i) · $(rget run/final.json state s)) — 기록을 더하거나 고치지 않는다 (포장만: PACK_ONLY=1)"; exit 2; };;
esac
case "${1:-}" in --infra-abort|--infra-wall|--killed|--reset-w0) lock_take "기록 명령 $1"; tree_gate "기록 명령 $1";; esac      # 기록을 더하기 전 트리 관문 (모르는 것 · 못 읽는 것 · 서로 안 맞는 것 → 종료 8 · Codex EQ)

# ── 잠금 지우기 — 운영자가 스케줄러로 그 잡이 끝났음을 확인한 뒤 (주인을 그대로 적어야 지운다) ──
if [ "${1:-}" = "--unlock" ]; then
  [ $# -eq 3 ] || { echo "⛔ 쓰는 법: bash run_a5.sh --unlock <기계> <PID> (잠금 주인을 그대로)"; exit 2; }
  [ "$LK_S" != none ] || { echo "⛔ 잠금이 없다"; exit 2; }
  { [ "$2" = "$LK_H" ] && [ "$3" = "$LK_P" ]; } || { echo "⛔ 잠금 주인은 기계 $LK_H · PID $LK_P 다 — 그대로 적어야 지운다"; exit 2; }
  [ "$LK_S" != live ] || { echo "⛔ 이 기계에서 PID $LK_P 가 살아 있다 — 지우지 않는다"; exit 2; }
  rm -rf "$LOCK" || { echo "⛔ 잠금을 지우지 못했다"; exit 2; }
  log "✎ 잠금을 지웠다 (기계 $LK_H · PID $LK_P · $LK_S — 운영자 확인)"; echo "✓ 잠금을 지웠다 — 다시 돌리면 기록에서 이어 간다"; exit 0
fi

# ── ⓪ 기록 지우기 — A5 를 띄우기 전에만 (경로를 잘못 적어 'sha 다름' 이 기록된 경우 · 리뷰 P1-3) ──
if [ "${1:-}" = "--reset-w0" ]; then
  [ $# -eq 1 ] || { echo "⛔ 쓰는 법: bash run_a5.sh --reset-w0"; exit 2; }
  [ -f run/w0_check.json ] || { echo "⛔ 지울 ⓪ 기록 (run/w0_check.json) 이 없다"; exit 2; }
  if [ -e "run/${JOB}_A5" ] || [ -f run/start_point.json ] || compgen -G "run_aborted/${JOB}_*" > /dev/null; then
    echo "⛔ A5 가 이미 시작했다 — ⓪ 기록은 A5 를 띄우기 전에만 지운다"; exit 2
  fi
  log "✎ ⓪ 기록을 지운다 (A5 시작 전 · 운영자) — 이전 기록 $(tr -d '\n' < run/w0_check.json | cut -c1-400)"
  rm -f run/w0_check.json || { echo "⛔ 지우지 못했다"; exit 2; }
  echo "✓ ⓪ 기록을 지웠다 — 맞는 W0_WAVECAR (또는 none) 로 다시 돌리면 ⓪ 을 다시 확인한다"; exit 0
fi

# ── 0 스텝 인프라 중단 기록 (외주 2차 --infra-abort 와 같은 확인 · 단 이름만 a5 · 뒤 단이 있으면 거부) ──
#    영수증은 REC1 한 줄 · 손으로 넣은 글 (잡 id · 취소 시각 · 사유) 은 JSON 이스케이프 (jstr) · run_id = 그 시도의 attempt.start (Codex EO P1) · 장부는 탭 · 줄바꿈 없앤 글
if [ "${1:-}" = "--infra-abort" ]; then
  [ $# -ge 5 ] || { echo "⛔ 쓰는 법: [WALL_S=<초>] bash run_a5.sh --infra-abort <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유…>"; exit 2; }
  st=$2; sid_r=$3; when_r=$4; shift 4; why_r="$*"; sid=$(clean "$sid_r"); when=$(clean "$when_r"); why=$(clean "$why_r")
  case "$st" in A5|c1|c2) ;; *) echo "⛔ 모르는 단 $st"; exit 2;; esac
  src=run/${JOB}_$st
  [ -d "$src" ] || { echo "⛔ $src 가 없다"; exit 2; }
  lx=$(later5 "$st"); [ -z "$lx" ] || { echo "⛔ 뒤 단 ($lx) 이 이미 있다 — $st 의 0 스텝 중단은 뒤 단을 띄우기 전에만 기록한다 (1저자에게 알린다)"; exit 2; }
  if [ -e "$src/OSZICAR" ]; then
    { [ -f "$src/OSZICAR" ] && [ -r "$src/OSZICAR" ]; } || { echo "⛔ $src/OSZICAR 를 읽지 못했다 — 0 행인지 확인할 수 없어 기록하지 않는다 (1저자)"; exit 2; }
    g=$(row_scan "$src" "$st"); osz=zero_rows
  else
    g="0 -"; osz=missing
  fi
  [ "$g" = "0 -" ] || { echo "⛔ OSZICAR 완전한 전자 반복행 ${g%% *} · 판독 ${g#* } — 0 스텝 중단이 아니다 (행꼴 조각 · 남의 머리도 0 스텝이 아니다 · 끊긴 시도면 --killed · 실행 실패는 사다리가 다룬다)"; exit 2; }
  so=$(grep -acE '^[[:space:]]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:[[:space:]]+[0-9]' "$src/stdout.log" 2>/dev/null); so=${so:-0}
  oi=$(grep -acE 'Iteration +[0-9]+\(' "$src/OUTCAR" 2>/dev/null); oi=${oi:-0}
  [ "$so" = 0 ] && [ "$oi" = 0 ] || { echo "⛔ OSZICAR 는 $osz 인데 stdout.log 전자 반복행 $so · OUTCAR Iteration $oi — 출력 유실이지 0 스텝이 아니다 · 기록하지 않는다"; exit 2; }
  { nbw "$sid" && nbw "$when" && nbw "$why"; } || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유가 다 있어야 한다 (빈칸 문자 — 공백 · 탭 · 줄바꿈 · VT · FF · CR — 만인 글도 안 된다 · Codex EQ)"; exit 2; }
  { u8ok "$sid_r" && u8ok "$when_r" && u8ok "$why_r"; } || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유에 UTF-8 이 아닌 바이트가 있다 — 기록하지 않는다 (UTF-8 글로 다시 · Codex EP)"; exit 2; }
  if [ -n "${WALL_S:-}" ]; then
    secs_ok "$WALL_S" || { echo "⛔ WALL_S '$WALL_S' — 0 이상의 10진 정수 (초 · 선행 0 없이 · 9 자리 이하) 여야 한다"; exit 2; }
    w=$WALL_S
  elif [ -f "$src/attempt.json" ]; then
    w=ATTEMPT_JSON
  else
    w=UNKNOWN
  fi
  k=$(awk -F'\t' -v j="$JOB" 'NR > 1 && $2 == j' run/infra_aborts.tsv 2>/dev/null | wc -l); k=${k:-0}
  [ "$k" -lt "$INFRA_MAX" ] || { echo "⛔ 0 스텝 중단 기록이 이미 $INFRA_MAX 회 — 상한 (1저자에게 알린다)"; exit 2; }
  rid=$(rget "$src/attempt.start" run_id s)
  mkdir -p run_aborted; dst=run_aborted/${JOB}_${st}_$((k + 1))
  mkdir "$dst" || exit 2
  shopt -s dotglob nullglob
  for f in "$src"/*; do mv "$f" "$dst/" || exit 2; done; rmdir "$src" || exit 2
  shopt -u dotglob nullglob
  rm -f "$dst/POTCAR" "$dst/WAVECAR" "$dst/CHGCAR" "$dst/CHG" "$dst/vasprun.xml" "$dst/.running"     # WAVECAR 는 복사본이다 (보존 ⓐ 원본 · A5 끝 WAVECAR 는 이 폴더 밖)
  if [ "$w" = ATTEMPT_JSON ]; then w=$(grep -o '"elapsed_s": [^,}]*[,}]' "$dst/attempt.json" | head -1 | sed 's/^"elapsed_s": //; s/[,}]$//'); secs_ok "$w" || w=UNKNOWN; fi
  printf '{"job": "%s", "rung": "%s", "run_id": "%s", "sched_job_id": "%s", "cancel_utc": "%s", "reason": "%s", "wall_s": "%s", "oszicar": "%s", "recorded_utc": "%s", "recorded_s": %d}\n' \
    "$JOB" "$st" "$rid" "$(jstr "$sid_r")" "$(jstr "$when_r")" "$(jstr "$why_r")" "$w" "$osz" "$(utc)" "$(date +%s)" > "$dst/infra_abort.json.part" \
    && mv -f "$dst/infra_abort.json.part" "$dst/infra_abort.json" || { echo "⛔ 영수증 (infra_abort.json) 쓰기 실패 — 연락 (다시 돌리면 장부 대조가 멈춘다)"; exit 2; }
  [ -f run/infra_aborts.tsv ] || printf "recorded_utc\tjob\trung\tsched_job_id\tcancel_utc\twall_s\treason\tdir\n" > run/infra_aborts.tsv
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$(utc)" "$JOB" "$st" "$sid" "$when" "$w" "$why" "$(basename "$dst")" >> run/infra_aborts.tsv
  if [ "$w" = UNKNOWN ]; then
    echo "✓ $src → $dst (0 스텝 인프라 중단 $((k + 1))/$INFRA_MAX) — ⚠ 벽시계 미상: 'bash run_a5.sh --infra-wall $(basename "$dst") <초>' 로 채울 때까지 다음 단이 뜨지 않는다"
  else
    echo "✓ $src → $dst (0 스텝 인프라 중단 $((k + 1))/$INFRA_MAX) — 다시 돌리면 같은 단부터"
  fi
  exit 0
fi

# ── 0 스텝 중단의 벽시계 채우기 (미상일 때만 · 스케줄러 장부 값) — 영수증을 REC1 로 읽고 같은 칸 순서로 다시 쓴다 + 채운 시각 (wall_s_filled_utc · wall_s_filled_s) ──
#    검사기는 채운 시각 ≤ 다음 시도 시작 · 미상 영수증 뒤에 시도가 없음을 본다 (Codex EO P1 Q-EO-2c)
if [ "${1:-}" = "--infra-wall" ]; then
  [ $# -eq 3 ] || { echo "⛔ 쓰는 법: bash run_a5.sh --infra-wall <run_aborted 폴더 이름> <초>"; exit 2; }
  b=$(basename "$2"); dd=run_aborted/$b; sec=$3
  [ -f "$dd/infra_abort.json" ] || { echo "⛔ $dd/infra_abort.json 이 없다"; exit 2; }
  secs_ok "$sec" || { echo "⛔ 초 '$sec' — 0 이상의 10진 정수 (선행 0 없이 · 9 자리 이하) 여야 한다"; exit 2; }
  R=$(rec5 "$dd/infra_abort.json") || { echo "⛔ $dd/infra_abort.json 을 읽지 못했다 — 고치지 않는다"; exit 2; }
  [ "$(rf "$R" wall_s s)" = UNKNOWN ] || { echo "⛔ $dd 의 벽시계는 미상이 아니다 — 고치지 않는다"; exit 2; }
  { printf '%s\n' "$R" | LC_ALL=C awk -F'\t' -v W="$sec" -v U="$(utc)" -v S="$(date +%s)" 'BEGIN { printf "{" }
      { v = substr($0, length($1) + length($2) + 3); if ($1 == "wall_s") v = W
        printf "%s\"%s\": %s", (NR > 1 ? ", " : ""), $1, ($2 == "i" ? v : "\"" v "\"") }
      END { printf ", \"wall_s_filled_utc\": \"%s\", \"wall_s_filled_s\": %s}\n", U, S }'; } > "$dd/infra_abort.json.part" \
    && rec5 "$dd/infra_abort.json.part" > /dev/null && mv -f "$dd/infra_abort.json.part" "$dd/infra_abort.json" || { rm -f "$dd/infra_abort.json.part"; echo "⛔ infra_abort.json 고치기 실패"; exit 2; }
  LC_ALL=C awk -F'\t' -v OFS='\t' -v d="$b" -v w="$sec" 'NR > 1 && $8 == d && $6 == "UNKNOWN" { $6 = w } { print }' run/infra_aborts.tsv > run/infra_aborts.tsv.part \
    && mv -f run/infra_aborts.tsv.part run/infra_aborts.tsv || { echo "⛔ infra_aborts.tsv 고치기 실패"; exit 2; }
  x=$(ledger5); [ "$x" = - ] || { echo "⛔ 고친 뒤 장부 대조가 어긋난다 ($x) — 연락"; exit 2; }
  echo "✓ $dd 벽시계 $sec 초 (스케줄러 장부) — 다시 돌리면 누적 상한 장부에 들어간다"; exit 0
fi

# ── 전자 스텝 뒤 끊긴 시도의 벽시계 기록 (그 단 소모 · 값 없음 · 완전한 전자 반복행 ≥ 1 · 행 손상 없음 · 뒤 단이 있으면 거부) ──
if [ "${1:-}" = "--killed" ]; then
  [ $# -ge 5 ] || { echo "⛔ 쓰는 법: WALL_S=<초> bash run_a5.sh --killed <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유…>"; exit 2; }
  st=$2; sid_r=$3; when_r=$4; shift 4; why_r="$*"; sid=$(clean "$sid_r"); when=$(clean "$when_r"); why=$(clean "$why_r")
  case "$st" in A5|c1|c2) ;; *) echo "⛔ 모르는 단 $st"; exit 2;; esac
  src=run/${JOB}_$st
  [ -f "$src/attempt.start" ] || { echo "⛔ $src 에 시작 표지 (attempt.start) 가 없다 — VASP 가 뜨지 않은 시도다"; exit 2; }
  [ ! -f "$src/attempt.json" ] || { echo "⛔ $src 는 끝난 시도다 (attempt.json 있음) — 기록하지 않는다"; exit 2; }
  [ ! -f "$src/killed.json" ] || { echo "⛔ $src 는 이미 기록했다 — 고치지 않는다"; exit 2; }
  lx=$(later5 "$st"); [ -z "$lx" ] || { echo "⛔ 뒤 단 ($lx) 이 이미 있다 — $st 의 끊김은 뒤 단을 띄우기 전에만 기록한다 (1저자에게 알린다)"; exit 2; }
  secs_ok "${WALL_S:-}" || { echo "⛔ WALL_S=<초> (스케줄러 장부의 그 시도 벽시계) 가 있어야 한다"; exit 2; }
  g=$(row_scan "$src" "$st"); n=${g%% *}; rw=${g#* }
  [ "$rw" = - ] || { echo "⛔ $src OSZICAR 행 판독 $rw (완전한 행 $n) — 잘린 첫 행 · 손상 · 남의 머리는 기록하지 않는다 (다시 돌리면 1저자 검토 멈춤 8)"; exit 2; }
  [ "$n" -ge 1 ] 2>/dev/null || { echo "⛔ $src OSZICAR 전자 반복행 0 — 0 스텝 중단이면 --infra-abort (OUTCAR 에만 반복 흔적이 있으면 출력 유실 — 연락)"; exit 2; }
  { nbw "$sid" && nbw "$when" && nbw "$why"; } || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유가 다 있어야 한다 (빈칸 문자 — 공백 · 탭 · 줄바꿈 · VT · FF · CR — 만인 글도 안 된다 · Codex EQ)"; exit 2; }
  { u8ok "$sid_r" && u8ok "$when_r" && u8ok "$why_r"; } || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유에 UTF-8 이 아닌 바이트가 있다 — 기록하지 않는다 (UTF-8 글로 다시 · Codex EP)"; exit 2; }
  rid=$(rget "$src/attempt.start" run_id s)
  printf '{"job": "%s", "rung": "%s", "run_id": "%s", "wall_s": "%s", "sched_job_id": "%s", "cancel_utc": "%s", "reason": "%s", "osz_rows": "%s", "recorded_utc": "%s", "recorded_s": %d}\n' \
    "$JOB" "$st" "$rid" "$WALL_S" "$(jstr "$sid_r")" "$(jstr "$when_r")" "$(jstr "$why_r")" "$n" "$(utc)" "$(date +%s)" > "$src/killed.json.part" && mv -f "$src/killed.json.part" "$src/killed.json" \
    || { echo "⛔ killed.json 쓰기 실패"; exit 2; }
  log "✎ $src 끊긴 시도 벽시계 $WALL_S 초 (스케줄러 $sid · $why · 전자 반복행 $n) — 그 단 소모 · 값 없음 · 다시 돌리지 않는다"
  echo "✓ $src 벽시계 $WALL_S 초 기록 — 다시 돌리면 다음 단부터 이어 간다"; exit 0
fi

[ "${PACK_ONLY:-0}" != 1 ] || { lock_take "PACK_ONLY 포장"; tree_gate "PACK_ONLY 포장"; }      # 다시 포장 전 트리 관문 — env.txt 에 쓰기 전 (끝 기록 조합 · 잔여 파일 · 끝 기록 신원 · 기존 반송본 · Codex EQ P1 Q-EQ-4)
@PACK_ONLY@

[ $# -eq 0 ] || { echo "⛔ 모르는 인자 '$1' — 계산은 인자 없이 돌린다 · 기록 명령은 --infra-abort · --infra-wall · --killed · --reset-w0 · --unlock (README)"; exit 2; }

# ── 계산 실행: 잠금을 잡는다 (같은 기계의 죽은 PID 잠금만 치운다 · 다른 기계의 잠금은 --unlock 으로만) ──
lock_take "계산"
tree_gate "다시 돌림"      # 잠금 다음 · 무엇을 쓰기 전 (env.txt · status.tsv · 준비 폴더 정리 · ⓪ · 끝난 사다리 재사용) — Codex EQ
# ── 끝난 사다리면 아무것도 띄우지 않는다 (리뷰 P1-1) · 보낼 묶음이 그 끝 기록을 담았는지 본다 (Codex EN P1 — 중간 PACK_ONLY 묶음 · 끝 포장 실패 뒤) ──
ret_has_final(){ # a5_return.tgz 가 .sha256 (한 줄 · 그 이름) 과 맞고, 그 안의 run/final.json 이 지금 run/final.json 과 바이트로 같으면 0
  [ -f a5_return.tgz ] && [ -f a5_return.tgz.sha256 ] || return 1
  [ "$(awk 'END { print NR }' a5_return.tgz.sha256 2>/dev/null)" = 1 ] && grep -qxE '[0-9a-f]{64}  a5_return\.tgz' a5_return.tgz.sha256 || return 1
  sha256sum -c --status a5_return.tgz.sha256 2>/dev/null || return 1
  tar xzf a5_return.tgz -O run/final.json 2>/dev/null | cmp -s - run/final.json
}
if [ -f run/final.json ]; then
  log "■ 다시 돌림 — 이 사다리는 이미 끝났다: 코드 $(rget run/final.json code i) · $(rget run/final.json state s)"
  fc=$(rget run/final.json code i)
  if ! ret_has_final; then
    log "⛔ a5_return.tgz 가 없거나 · sha256 이 맞지 않거나 · 이 끝 기록 (run/final.json) 을 담지 않았다 — 옛 묶음을 보내지 않는다"
    echo "⛔ 반송 묶음이 끝 기록과 맞지 않는다 (종료 4) — 계산은 다시 돌리지 말고 PACK_ONLY=1 bash run_a5.sh 로 포장만 다시"; exit 4
  fi
  echo "  아무것도 띄우지 않는다 · 보낼 것은 a5_return.tgz + .sha256 그대로 (sha256 · 끝 기록 포함 확인 · 포장만 다시: PACK_ONLY=1 bash run_a5.sh)"
  exit "$fc"
fi
[[ "$(up)" =~ ^[0-9]+$ ]] || { echo "⛔ /proc/uptime 을 읽을 수 없다 — 벽시계 장부는 단조 시계로 잰다 (Linux)"; exit 2; }
[ -n "${VASP_CMD:-}" ] || { echo "⛔ VASP_CMD 를 주세요 (예: mpirun -np 64 vasp_std)"; exit 2; }        # \${VAR:?} 는 1 로 끝난다 — 1 은 '값 없음' 이다 (종료 코드가 겹치지 않게)
[ -n "${POTCAR_DIR:-}" ] && [ -d "$POTCAR_DIR" ] || { echo "⛔ POTCAR_DIR 를 주세요 (PAW_PBE 폴더 · 있어야 한다: '${POTCAR_DIR:-}')"; exit 2; }
[ -n "${W0_WAVECAR:-}" ] || { echo "⛔ W0_WAVECAR 를 주세요 — 보존된 a4 ⓐ WAVECAR 경로 (외주 2차 묶음의 @W0_REL@ · 먼저 ls -l · sha256sum) · 없으면 W0_WAVECAR=none"; exit 2; }
PERF_LINES=""
@PERF@
{ echo "date_utc $(utc)"; echo "host $HOST"; echo "VASP_CMD $VASP_CMD"; echo "POTCAR_DIR $POTCAR_DIR"; echo "W0_WAVECAR $W0_WAVECAR"
  echo "PERF_TAGS $(printf '%s' "$PERF_LINES" | tr '\n' ';')"; echo "MANIFEST_sha256 $(h MANIFEST.sha256)"; } >> run/env.txt
[ -f run/status.tsv ] || printf "job\trung\tstage\trc\tstatus\tn_elec\tdE\tdeps\twhy\twall_s\trun_id\n" > run/status.tsv     # run_id — 이력 대조 (hist5 · Codex EP P1)
rm -rf "run/.prep_${JOB}_A5" "run/.prep_${JOB}_c1" "run/.prep_${JOB}_c2"     # 앞 실행의 남은 준비 폴더 (VASP 를 띄운 적 없음 · 잠금 아래)
'''

RUN_A5_BODY = r'''
# ── 누적 벽시계 (a5 의 모든 시도 · 0 스텝 중단 · 끊긴 시도 · 미상은 0 초가 아니다) ──
wall5(){ # 시도 폴더 (run/<잡>_<단> · run_aborted/<잡>_<단>_<k>) 마다 wall_of (영수증 → 끊김 기록 → attempt.json → 미상 · 검사기 wall_of 와 같은 출처 순서 · Codex EO P1 Q-EO-2c)
  local d w tot=0 unk=""
  for d in "run/${JOB}_A5" "run/${JOB}_c1" "run/${JOB}_c2" run_aborted/*; do
    [ -d "$d" ] || continue
    w=$(wall_of "$d")
    case "$w" in UNKNOWN|BAD) [ -n "$unk" ] || unk="$d ($w)";; *) tot=$((tot + w));; esac
  done
  if [ -n "$unk" ]; then echo "UNKNOWN $unk"; else echo "$tot"; fi
}
cap_ok(){ # → 0 띄워도 된다 · 1 누적 > 상한 · 2 벽시계 미상 · 장부 이상
  local w; w=$(wall5) || w="UNKNOWN (장부 계산 실패)"
  case "$w" in UNKNOWN*) log "⏸ 벽시계 미상 — ${w#UNKNOWN } · 다음 단을 띄우지 않는다. 0 스텝 중단이면 'bash run_a5.sh --infra-wall <폴더> <초>' · 끊긴 시도면 'WALL_S=<초> bash run_a5.sh --killed <단> …' 로 채운 뒤 다시"; return 2;; esac
  [[ "$w" =~ ^[0-9]+$ ]] || { log "⏸ 벽시계 장부가 숫자가 아니다 ('$w') — 다음 단을 띄우지 않는다 (반송하고 연락)"; return 2; }
  awk -v w="$w" -v c="$CAP_H" 'BEGIN { exit !(w <= c * 3600) }' || { log "⏸ a5 누적 $((w / 3600)) h > 상한 $CAP_H h — 다음 단을 띄우지 않는다 (1저자)"; return 1; }
  return 0
}

# ── 끝 · 멈춤 ──
fin5(){ # $1 코드 (0 · 1 · 5 상한 · 6 · 8) · $2 상태 · $3 사유 — 끝: run/final.json 을 쓰고 포장한다 (다시 돌려도 아무것도 띄우지 않는다)
  tree_gate "끝 기록 쓰기 전 ($1 $2)"          # 되돌릴 수 없는 일 (끝 기록 · 포장) 전에 같은 관문 (Codex ER Q-ER-1②)
  log "■ 끝 [$1 $2] $3"
  #  attempts = 이 사다리의 시도 폴더 · run_id 목록 (att5) — 같은 시각의 다른 실행 묶음과 끝 기록이 같아지지 않게 (ret_has_final 이 바이트로 대조 · Codex EO P2)
  printf '{"code": %d, "state": "%s", "why": "%s", "attempts": "%s", "written_utc": "%s", "written_s": %d}\n' "$1" "$2" "$(jstr "$3")" "$(att5)" "$(utc)" "$(date +%s)" > run/final.json.part \
    && mv -f run/final.json.part run/final.json || { echo "⛔ run/final.json 쓰기 실패 — 디스크를 확인한 뒤 다시 돌려 주세요 (기록에서 같은 판정을 다시 낸다)"; exit 4; }
  finish "$1"
}
stop5(){ # $1 코드 (3 · 5 · 7) · $2 사유 — 멈춤 (끝이 아니다: 기록하거나 고친 뒤 다시 돌린다 · 포장하지 않는다 · run/final.json 없음)
  log "⏸ [$1] $2"
  case "$1" in
    3) echo "⛔ 준비 실패 (종료 3) — 그 단은 소모되지 않았다. 원인을 고친 뒤 다시 돌려 주세요 (막히면 PACK_ONLY=1 로 포장해 연락)";;
    5) echo "⏸ 멈춤 (종료 5) — 위 줄의 기록 명령을 쓴 뒤 다시 돌려 주세요";;
    7) echo "⏸ 멈춤 (종료 7) — 전자 반복행 0 · 다음 단을 띄우지 않았다 (위 줄 · 막히면 PACK_ONLY=1 로 포장해 연락)";;
  esac
  exit "$1"
}
env6_pre(){ # 띄우기 전 PP sha ≠ 봉인 — 이번 실행은 아무것도 띄우지 않았다 (끝 기록 없음 · POTCAR_DIR 를 고친 경우에만 다시)
  log "⛔ 공통 환경 고장 (PP sha ≠ 봉인) — 이번 실행은 아무것도 띄우지 않았다 · 반송하고 연락 (POTCAR_DIR 를 잘못 준 경우에만 고쳐서 다시)"
  if ! pack; then echo "⛔ 반송 포장 실패 — PACK_ONLY=1 bash run_a5.sh"; exit 4; fi
  echo "⛔ 공통 환경 고장 (PP) — 반송해 주시고 연락 주세요"; exit 6
}

# ── ⓪ 보존된 a4 ⓐ WAVECAR 확인 (한 번 · 원본은 읽기만 · 경로가 없거나 못 읽으면 기록하지 않고 멈춘다 — 리뷰 P1-3) ──
w0_check(){
  local p=$W0_WAVECAR s="" z="" hd="" v=0 why=""
  if [ -f run/w0_check.json ]; then
    [ "$(grep -o '"path": "[^"]*"' run/w0_check.json | head -1 | sed 's/.*: "//; s/"$//')" = "$(clean "$p")" ] \
      || { echo "⛔ W0_WAVECAR '$p' 가 첫 기록 (run/w0_check.json) 과 다르다 — 같은 경로로 다시 돌린다 (A5 를 띄우기 전이면 'bash run_a5.sh --reset-w0' 로 기록을 지울 수 있다)"; exit 2; }
    return 0
  fi
  if [ "$p" = none ]; then why="업체가 없다고 적음 (W0_WAVECAR=none)"
  elif [ -f "$p" ] && [ -r "$p" ]; then
    s=$(h "$p"); z=$(stat -c %s "$p" 2>/dev/null); hd=$(wav_head "$p"); set -- $hd
    if [ "$s" != "$W0_SHA" ]; then why="sha256 다름"
    elif [ "$z" != "$W0_SIZE" ]; then why="크기 다름"
    elif ! { [ $# -ge 6 ] && [ "$4" = "$W0_NK" ] && [ "$5" = "$W0_NB" ] && enc_eq "$6" "$W0_EN"; }; then why="머리 (NKPTS·NBANDS·ENCUT) 다름"
    else v=1; why="-"; fi
  else
    echo "⛔ W0_WAVECAR '$p' 가 없거나 읽을 수 없다 — 기록하지 않았다. 'ls -l' · 'sha256sum' 으로 경로를 확인하고, 정말 없으면 W0_WAVECAR=none 으로 다시"; exit 2
  fi
  printf '{"path": "%s", "sha256": "%s", "size": "%s", "head": "%s", "expect": {"sha256": "%s", "size": "%s", "NKPTS": "%s", "NBANDS": "%s", "ENCUT": "%s"}, "verified": %d, "why": "%s", "checked_utc": "%s"}\n' \
    "$(clean "$p")" "$s" "$z" "$hd" "$W0_SHA" "$W0_SIZE" "$W0_NK" "$W0_NB" "$W0_EN" "$v" "$why" "$(utc)" > run/w0_check.json.part && mv -f run/w0_check.json.part run/w0_check.json \
    || { echo "⛔ run/w0_check.json 쓰기 실패"; exit 2; }
  log "⓪ 보존 ⓐ WAVECAR $( [ "$v" = 1 ] && echo '확인됨 — A5 는 그 복사본에서 이어서' || echo "확인 안 됨 ($why) — A5 는 새로 시작")"
}

# ── 한 시도 — 준비는 임시 폴더 run/.prep_<잡>_<단> 에서 하고, 다 되면 시도 폴더로 이름을 바꾼 뒤 띄운다 (준비 실패는 그 단을 소모하지 않는다 — 리뷰 P2(c)) ──
pfail(){ log "⛔ $2 — 준비 실패 · 그 단은 소모되지 않았다 (임시 폴더를 지웠다 · 원인 — 디스크 · 권한 · 경로 — 을 고친 뒤 다시)"; rm -rf "$1"; }
run_one5(){ # $1 단 (A5|c1|c2) · $2 변형 (A5c|A5f|c1|c2) · $3 시도 폴더 · $4 시작 WAVECAR (A5c · c1 · c2) · $5 그 기대 sha → 0 돌림 · 3 준비 실패 · 6 띄우기 전 PP 불일치
  local st=$1 var=$2 d=$3 wsrc=${4:-} wexp=${5:-} inc tp rid t0 t1 u0 u1 el rc j wsha="" wcp="" wend hd istart icharg nr pr hon ver rs x p
  inc=$(incar_of "$var"); tp="run/.prep_${JOB}_$st"
  pp_ok "$JOB" || return 6
  [ ! -e "$d" ] || { log "⛔ $d 가 이미 있다 — 덮어쓰지 않는다"; return 3; }
  rm -rf "$tp"; mkdir "$tp" || { log "⛔ $st 준비 폴더 ($tp) 를 만들 수 없다"; return 3; }
  { cp "jobs/$JOB/POSCAR" "jobs/$JOB/KPOINTS" "$tp/" && cp "jobs/$JOB/$inc" "$tp/INCAR"; } || { pfail "$tp" "$st 입력 복사"; return 3; }
  if [ -n "$PERF_LINES" ]; then printf '%s' "$PERF_LINES" >> "$tp/INCAR" || { pfail "$tp" "$st 성능 태그"; return 3; }; fi
  { : > "$tp/POTCAR" && : > "$tp/POTCAR.species.sha256"; } || { pfail "$tp" "$st POTCAR 시작"; return 3; }
  while read -r p; do
    [ -n "$p" ] || continue
    [ -f "$POTCAR_DIR/$p/POTCAR" ] || { pfail "$tp" "POTCAR $p 없음"; return 3; }
    { cat "$POTCAR_DIR/$p/POTCAR" >> "$tp/POTCAR" && printf "%s %s\n" "$p" "$(h "$POTCAR_DIR/$p/POTCAR")" >> "$tp/POTCAR.species.sha256"; } || { pfail "$tp" "POTCAR $p 잇기"; return 3; }
  done < "jobs/$JOB/POTCAR.spec"
  { grep -aE "TITEL|ZVAL|VRHFIN|LEXCH" "$tp/POTCAR" > "$tp/POTCAR.titel" && h "$tp/POTCAR" > "$tp/POTCAR.sha256"; } || { pfail "$tp" "$st POTCAR 기록"; return 3; }
  if [ -n "$wsrc" ]; then
    wsha=$(h "$wsrc")
    { [ -n "$wexp" ] && [ "$wsha" = "$wexp" ]; } || { pfail "$tp" "$st 시작 WAVECAR ($wsrc) sha '$wsha' ≠ 기대 '$wexp'"; return 3; }
    cp "$wsrc" "$tp/WAVECAR" || { pfail "$tp" "$st 시작 WAVECAR 복사 (디스크?)"; return 3; }
    wcp=$(h "$tp/WAVECAR")
    [ "$wcp" = "$wexp" ] || { pfail "$tp" "$st 복사한 WAVECAR sha 가 원본과 다르다"; return 3; }
  fi
  rid="$(date -u +%Y%m%dT%H%M%S)-$$-$RANDOM"; t0=$(date +%s); u0=$(up)
  printf '{"job": "%s", "attempt": "%s", "stage": "a5", "run_id": "%s", "t_start": %d, "kernel_sha256": ""}\n' "$JOB" "$var" "$rid" "$t0" > "$tp/attempt.start" \
    || { pfail "$tp" "$st 시작 표지"; return 3; }
  mv -T "$tp" "$d" || { pfail "$tp" "$st 준비 폴더를 $d 로 옮기지 못했다"; return 3; }
  touch "$d/.running"; watch5 "$d" "$JOB/$var" "$st" & local wpid=$!
  (cd "$d" && $VASP_CMD > stdout.log 2>&1); rc=$?; t1=$(date +%s); u1=$(up)
  el=$((u1 - u0)); [ "$el" -ge 0 ] 2>/dev/null || el=$(( t1 > t0 ? t1 - t0 : 0 ))
  rm -f "$d/.running"; kill "$wpid" 2>/dev/null; wait "$wpid" 2>/dev/null
  ver=$(clean "$(ver_of "$d")")
  istart=$(grep -aE '^[[:space:]]*ISTART *= *[0-9]+[[:space:]]+job' "$d/OUTCAR" 2>/dev/null | tail -1 | grep -oE 'ISTART *= *[0-9]+' | grep -oE '[0-9]+$')
  icharg=$(grep -aE '^[[:space:]]*ICHARG *= *[0-9]+[[:space:]]+charge' "$d/OUTCAR" 2>/dev/null | tail -1 | grep -oE 'ICHARG *= *[0-9]+' | grep -oE '[0-9]+$')
  nr=0; grep -aq "WAVECAR not read" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null && nr=1
  pr=0; grep -aqE -e "$RESTART_RE" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null && pr=1
  case "$st" in
    A5)
      hd=$(wav_head "$d/WAVECAR")
      if [ "$var" = A5c ]; then
        # A5 의 재시작 확인 = 시작 복사본 sha + 문구 (끝 sha 는 안 본다 — LWAVE T 라 새로 써진다 · 정보 · 자격 아님)
        hon=0; [ "$istart" = 1 ] && [ "$icharg" = 0 ] && [ "$nr" = 0 ] && [ "$pr" = 1 ] && [ -n "$wsha" ] && [ "$wsha" = "$wcp" ] && [ "$wcp" = "$wexp" ] && hon=1
        rs=$(printf '{"src_sha256": "%s", "copied_sha256": "%s", "istart": "%s", "icharg": "%s", "not_read_phrase": %s, "positive_regex_match": "%s", "honoured_start": %s}' \
          "$wsha" "$wcp" "${istart:-NA}" "${icharg:-NA}" "$nr" "$pr" "$hon")
      else rs=null; fi
      printf '{"sha256": "%s", "size": %s, "head": "%s", "outcar": {"NKPTS": "%s", "NBANDS": "%s", "ENCUT": "%s"}, "restart": %s}\n' "$(h "$d/WAVECAR")" \
        "$(stat -c %s "$d/WAVECAR" 2>/dev/null || echo 0)" "$hd" "$(out_num "$d" NKPTS)" "$(out_num "$d" NBANDS)" "$(out_num "$d" ENCUT)" "$rs" > "$d/WAVECAR.info.part" && mv -f "$d/WAVECAR.info.part" "$d/WAVECAR.info" || { log "⛔ $d WAVECAR 기록 쓰기 실패 — 더 하지 않는다 (종료 8 · 연락)"; exit 8; };;
    c1|c2)
      wend=$(h "$d/WAVECAR")
      hon=0; [ "$istart" = 1 ] && [ "$icharg" = 0 ] && [ "$nr" = 0 ] && [ "$pr" = 1 ] && [ -n "$wsha" ] && [ "$wsha" = "$wcp" ] && [ "$wcp" = "$wend" ] && hon=1
      printf '{"src_sha256": "%s", "copied_sha256": "%s", "end_sha256": "%s", "istart": "%s", "icharg": "%s", "not_read_phrase": %s, "positive_regex_match": "%s", "honoured": %s, "start_head": "%s", "outcar": {"NKPTS": "%s", "NBANDS": "%s", "ENCUT": "%s"}}\n' \
        "$wsha" "$wcp" "$wend" "${istart:-NA}" "${icharg:-NA}" "$nr" "$pr" "$hon" "$SPH" "$(out_num "$d" NKPTS)" "$(out_num "$d" NBANDS)" "$(out_num "$d" ENCUT)" > "$d/WAVECAR.info.part" && mv -f "$d/WAVECAR.info.part" "$d/WAVECAR.info" || { log "⛔ $d WAVECAR 기록 쓰기 실패 — 더 하지 않는다 (종료 8 · 연락)"; exit 8; };;
  esac
  if [ "$st" != c2 ]; then x=$(hist_max "$d"); case "$x" in ''|*[!0-9]*) ;; *) [ "$x" -gt 45 ] && echo "$(utc) $var info history_max $x" >> "$d/warn.log";; esac; fi
  printf '{"job": "%s", "attempt": "%s", "stage": "a5", "run_id": "%s", "rc": %d, "t_start": %d, "t_end": %d, "elapsed_s": %d, "vasp_version": "%s", "kernel_sha256": "", "perf": "%s", "sha256": {"INCAR": "%s", "POSCAR": "%s", "KPOINTS": "%s", "POTCAR": "%s", "OUTCAR": "%s", "OSZICAR": "%s", "WAVECAR.info": "%s", "stdout.log": "%s", "POTCAR.titel": "%s", "POTCAR.species.sha256": "%s", "attempt.start": "%s"}}\n' \
    "$JOB" "$var" "$rid" "$rc" "$t0" "$t1" "$el" "$ver" "$(printf '%s' "$PERF_LINES" | tr '\n' ';')" \
    "$(h "$d/INCAR")" "$(h "$d/POSCAR")" "$(h "$d/KPOINTS")" "$(cat "$d/POTCAR.sha256")" "$(h "$d/OUTCAR")" "$(h "$d/OSZICAR")" "$(h "$d/WAVECAR.info")" \
    "$(h "$d/stdout.log")" "$(h "$d/POTCAR.titel")" "$(h "$d/POTCAR.species.sha256")" "$(h "$d/attempt.start")" > "$d/attempt.json.part" && mv -f "$d/attempt.json.part" "$d/attempt.json" \
    || { log "⛔ $d 끝 기록 (attempt.json) 쓰기 실패 — 더 하지 않는다 (종료 8 · 남은 .part 는 트리 관문이 멈춘다 · 연락)"; exit 8; }
  j=$(judge5 "$d" "$st"); set -- $j
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$JOB" "$var" "a5" "$rc" "$1" "$2" "$3" "$4" "$5" "$el" "$rid" >> run/status.tsv
  rm -f "$d/POTCAR" "$d/CHGCAR" "$d/CHG" "$d/vasprun.xml" "$d/vdw_kernel.bindat" "$d/LOCPOT"
  [ "$st" = A5 ] || rm -f "$d/WAVECAR"          # c1 · c2 의 WAVECAR 는 복사본 (끝 sha 를 잰 뒤 지운다) · A5 WAVECAR 는 사다리가 끝날 때까지 둔다 (반송 안 함)
  return 0
}

# ── 단의 갈래 (개정 5 해석 1 · 사용자 2026-11-20 — 러너와 검사기가 같은 순서로 본다) ──
killed5(){ # $1 시도 폴더 · $2 단 · $3 완전한 행 수 → "-" (맞음) 또는 "상태 행수 사유" — 끊긴 시도도 원문에 남은 증거를 본다 (Codex EN P0 · P1 · EO P1 — 검사기 killed_problems 와 같은 순서):
  #   ① c1 · c2 재시작 원문 — OUTCAR ISTART 1 job · ICHARG 0 charge · 'WAVECAR not read' 없음 · 등록부 문구 · NKPTS·NBANDS·ENCUT = 시작점 머리
  #      (끝 기록이 없어 sha 셋은 못 본다 · 시작 복사본 sha 는 띄우기 전에 확인했다) — 아니면 RESTART_NOT_HONOURED
  #   ② killed.json osz_rows = 지금 완전한 행 수 — 아니면 KILLED_RECORD_MISMATCH (문법 · 칸 · 빈칸 · 잡 · 단 · run_id · 초 · 기록 시각은 트리 관문 killed_rec5 · Codex EQ)
  #   행 머리 · 행 손상 · attempt.start 의 잡 · 단 · 변형은 그 앞 (gate5) 에서 본다
  local d=$1 st=$2 n=$3 is ic
  case "$st" in c1|c2)
    is=$(grep -aE '^[[:space:]]*ISTART *= *[0-9]+[[:space:]]+job' "$d/OUTCAR" 2>/dev/null | tail -1 | grep -oE 'ISTART *= *[0-9]+' | grep -oE '[0-9]+$')
    ic=$(grep -aE '^[[:space:]]*ICHARG *= *[0-9]+[[:space:]]+charge' "$d/OUTCAR" 2>/dev/null | tail -1 | grep -oE 'ICHARG *= *[0-9]+' | grep -oE '[0-9]+$')
    { [ "$is" = 1 ] && [ "$ic" = 0 ]; } || { echo "RESTART_NOT_HONOURED $n istart_${is:-NA}_icharg_${ic:-NA}"; return; }
    ! grep -aq "WAVECAR not read" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null || { echo "RESTART_NOT_HONOURED $n wavecar_not_read"; return; }
    grep -aqE -e "$RESTART_RE" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null || { echo "RESTART_NOT_HONOURED $n no_restart_phrase"; return; }
    { [ "$(out_num "$d" NKPTS)" = "${SP_NK:-x}" ] && [ "$(out_num "$d" NBANDS)" = "${SP_NB:-x}" ] && enc_eq "$(out_num "$d" ENCUT)" "${SP_EN:-x}"; } \
      || { echo "RESTART_NOT_HONOURED $n dims_ne_start_head"; return; };;
  esac
  [ "$(rget "$d/killed.json" osz_rows s)" = "$n" ] || { echo "KILLED_RECORD_MISMATCH $n osz_rows"; return; }
  echo -
}
gate5(){ # $1 시도 폴더 · $2 단 → "갈래 상태 행수 사유" (빈칸 없는 낱말 넷)
  #   NEW 띄울 차례 · WAIT5 끊김 (끝 기록 없음) · ZERO 전자 반복행 0 (멈춤 7) · ENV 다른 VASP 빌드 (끝 6) · REVIEW 1저자 (끝 8) ·
  #   OK 주 기준 수렴 · NEXT 다음 단 (SCF_NOT_CONVERGED · 행 ≥ 1 실행 실패 · 행 ≥ 1 끊김 기록)
  #   순서 (검사기 check_attempt5 · a5_class 와 같다): [시작 · 끝 기록 신원 · 봉인 · 끊김 기록 결속은 트리 관문 — Codex EQ] → 완전한 행 판독 (row_scan) →
  #   끝난 시도: 빌드 → 행 손상 · 남의 머리 (REVIEW · Codex EO P0) → 행 0 (ZERO) → 설정 에코 → 판정 · 끝 기록 없는 시도: 행 손상 · 남의 머리 (REVIEW — 기록 전이라도) → 끊김 기록
  local d=$1 st=$2 n why g var ver e s
  [ -e "$d" ] || { echo "NEW - 0 -"; return; }
  #   폴더 이름 · 시작 기록 (잡 · 단 · 변형) · 끝 기록 틀 · 신원 · 봉인 · 끊김 기록은 트리 관문 (tree5) 이 다시 돌릴 때 · 띄우기 전에 본다 (Codex EQ — 한 곳)
  var=$(rget "$d/attempt.start" attempt s)
  g=$(row_scan "$d" "$st"); [ -n "$g" ] || g="0 -"
  n=${g%% *}; why=${g#* }; ver=$(clean "$(ver_of "$d")")
  if [ -f "$d/attempt.json" ]; then
    if [ -n "$ver" ] && [ "$ver" != "$REL_VER" ]; then echo "ENV VERSION_MISMATCH $n vasp_build"; return; fi
    [ "$why" = - ] || { echo "REVIEW SCF_UNVERIFIED $n $why"; return; }
    [ "$n" -ge 1 ] 2>/dev/null || { echo "ZERO SCF_UNVERIFIED 0 no_rows"; return; }
    e=$(echo5 "$d" "$var"); [ "$e" = "-" ] || { echo "REVIEW SETTINGS_ECHO $n $e"; return; }
    s=$(stat5 "$d" "$st" "$SS")
    case "$s" in OK) echo "OK OK $n -";; SCF_NOT_CONVERGED|RUN_FAILED) echo "NEXT $s $n -";; *) echo "REVIEW $s $n -";; esac
    return
  fi
  [ "$why" = - ] || { echo "REVIEW SCF_UNVERIFIED $n $why"; return; }       # 끝 기록이 없어도 — 잘린 첫 행 (완전한 행 0 + 행꼴 조각) 은 기록할 수 없고 다음 단으로 넘기지 않는다 (Codex EO P0)
  [ -f "$d/killed.json" ] || { echo "WAIT5 INCOMPLETE_ATTEMPT $n no_end_record"; return; }
  if [ -n "$ver" ] && [ "$ver" != "$REL_VER" ]; then echo "ENV VERSION_MISMATCH $n vasp_build"; return; fi
  [ "$n" -ge 1 ] 2>/dev/null || { echo "REVIEW KILLED_NO_ROWS 0 -"; return; }
  e=$(echo5 "$d" "$var"); [ "$e" = "-" ] || { echo "REVIEW SETTINGS_ECHO $n $e"; return; }
  e=$(killed5 "$d" "$st" "$n"); [ "$e" = "-" ] || { echo "REVIEW $e"; return; }
  echo "NEXT KILLED $n -"
}
rc_of(){ grep -o '"rc": -\{0,1\}[0-9]*' "$1/attempt.json" 2>/dev/null | head -1 | grep -o -- '-\{0,1\}[0-9]*$'; }
on_stop(){ # gate5 낱말 넷 + 단 → 멈출 갈래면 끝낸다 (돌아오면 OK · NEXT)
  local k=$1 s=$2 n=$3 why=$4 st=$5
  case "$k" in
    OK|NEXT) return 0;;
    WAIT5) stop5 5 "$st 는 시작했는데 끝 기록이 없다 (끊김 · 전자 반복행 $n) — 행 ≥ 1 이면 'WALL_S=<초> bash run_a5.sh --killed $st <스케줄러 잡 id> <취소 UTC> <사유>' · 행 0 이면 'bash run_a5.sh --infra-abort $st <잡 id> <취소 UTC> <사유>' 로 기록한 뒤 다시";;
    ZERO) stop5 7 "$st 전자 반복행 0 (rc $(rc_of "run/${JOB}_$st") · stdout.log 첫 줄: $(head -c 160 "run/${JOB}_$st/stdout.log" 2>/dev/null | head -1)) — 다음 단을 띄우지 않는다. 스케줄러 기록이 있는 0 스텝 인프라 중단이면 'bash run_a5.sh --infra-abort $st <잡 id> <취소 UTC> <사유>' 뒤 다시 (같은 단부터 · 잡 전체 $INFRA_MAX 회) · 아니면 (실행 파일 · 모듈 · 입력) 고치기 전에 연락";;
    ENV) fin5 6 ENV "$st VASP 빌드가 봉인과 다르다 — 공통 환경 고장 · 전체 정지";;
    REVIEW) fin5 8 REVIEW "$st $s ($why · 전자 반복행 $n) — 개정 5 해석 1 (사용자 2026-11-20): 재시작 미이행 · SCF 미확인 · 설정 에코 다름은 더 돌리지 않는다 → 1저자";;
    *) log "⛔ $st 갈래 '$k' 를 모른다 — 연락"; exit 2;;
  esac
}
cap_gate(){ # $1 단 — 띄우기 전: 트리 관문 (모르는 것 · 못 읽는 것 · 서로 안 맞는 것 → 종료 8 · Codex EQ) → 누적 상한 (넘으면 끝 5 · 벽시계 미상이면 멈춤 5)
  tree_gate "$1 발사 직전"
  cap_ok; case $? in
    0) return 0;;
    1) fin5 5 CAP "누적 상한 $CAP_H h — $1 를 띄우지 않았다 (1저자)";;
    *) stop5 5 "벽시계 미상 · 장부 이상 — '--infra-wall' 또는 '--killed' 로 채운 뒤 다시 ($1 앞)";;
  esac
}
drop5(){ tree_gate "A5 WAVECAR 지우기 전"; rm -f "run/${JOB}_A5/WAVECAR"; }    # 사다리 끝 (0 · 1) 에서만 — A5 끝 WAVECAR 는 반송하지 않는다 · 멈춤 (3 · 5 · 7 · 8) 에서는 남긴다 (검토 · 이어 돌리기용)
info_head(){ awk '{ if (match($0, /"head": "[^"]*"/)) { print substr($0, RSTART + 9, RLENGTH - 10); exit } }' "$1" 2>/dev/null; }
info_num(){ grep -o "\"$2\": [0-9]*" "$1" 2>/dev/null | head -1 | grep -o '[0-9]*$'; }
elig5(){ # A5 자격 (개정 5 '자격 = 개정 4 ⓐ 자격의 앞 셋' — 검사기 a_eligible 과 같은 기록 대조) → 0 자격 · 1 미달 (⓪ 복사본 또는 닫음) ·
  #        2 이상 (기록은 유효한 WAVECAR 인데 파일이 사라졌거나 바뀜 → 1저자 · ⓪ 으로 넘어가지 않는다)
  local d=$1 s r c k z
  s=$(stat5 "$d" A5)
  case "$s" in OK|SCF_NOT_CONVERGED) ;; *) echo "ⓐ 상태 $s (정상 종료·유한 상태 아님)"; return 1;; esac
  for k in NKPTS NBANDS ENCUT; do
    c=$(grep -o "\"$k\": \"[^\"]*\"" "$d/WAVECAR.info" 2>/dev/null | head -1 | sed 's/.*: "//; s/"$//')
    { [ -n "$c" ] && [ "$c" = "$(out_num "$d" "$k")" ]; } || { echo "ⓐ WAVECAR.info 의 OUTCAR 사본 $k '$c' ≠ ⓐ OUTCAR 원문 '$(out_num "$d" "$k")'"; return 1; }
  done
  r=$(info_head "$d/WAVECAR.info"); set -- $r
  { [ $# -ge 6 ] && [ "$4" = "$(out_num "$d" NKPTS)" ] && [ "$5" = "$(out_num "$d" NBANDS)" ] && enc_eq "$6" "$(out_num "$d" ENCUT)"; } \
    || { echo "ⓐ WAVECAR 머리 ($r) ≠ OUTCAR NKPTS/NBANDS/ENCUT"; return 1; }
  z=$(info_num "$d/WAVECAR.info" size)
  [ "${z:-0}" -gt 0 ] 2>/dev/null || { echo "ⓐ WAVECAR 기록 크기 0"; return 1; }
  [ -s "$d/WAVECAR" ] || { echo "ⓐ 끝 WAVECAR 가 기록 (크기 $z) 뒤 없어졌다"; return 2; }
  [ "$(h "$d/WAVECAR")" = "$(wsha "$d/WAVECAR.info" sha256)" ] || { echo "ⓐ 끝 WAVECAR 가 기록 뒤 바뀌었다"; return 2; }
  return 0
}
# ── 시작점 — 첫 c 단을 띄울 때 한 번 정해 run/start_point.json 에 두고, 그 뒤로는 다시 정하지 않는다 (리뷰 P0-2(b)) ──
sp_field(){ rget run/start_point.json "$1" s; }     # REC1 (검사기 json 과 같은 값 · 트리 관문 sp_rec5 가 먼저 · Codex EQ)
sp_load(){
  SPF=$(sp_field from); S=$(sp_field path); SS=$(sp_field sha256); SPH=$(sp_field head)
  case "$SPF" in A5) [ "$S" = "run/${JOB}_A5/WAVECAR" ] || return 1;; W0) [ "$S" = "$W0_WAVECAR" ] || return 1;; *) return 1;; esac
  [[ "$SS" =~ ^[0-9a-f]{64}$ ]] || return 1
  set -- $SPH; [ $# -ge 6 ] || return 1
  SP_NK=$4; SP_NB=$5; SP_EN=$6
}
sp_write(){
  printf '{"from": "%s", "path": "%s", "sha256": "%s", "head": "%s", "a5_why": "%s", "written_utc": "%s", "written_s": %d}\n' \
    "$SPF" "$(clean "$S")" "$SS" "$SPH" "$(clean "$SPWHY")" "$(utc)" "$(date +%s)" > run/start_point.json.part && mv -f run/start_point.json.part run/start_point.json
}

# ── 사다리 ──
log "════ W_ad a5 · $JOB ════"
pp_ok "$JOB" || env6_pre
w0_check
W0OK=0; grep -q '"verified": 1' run/w0_check.json && W0OK=1
A=run/${JOB}_A5; C1=run/${JOB}_c1; C2=run/${JOB}_c2
SS=""; SPF=""; S=""; SPH=""; SP_NK=""; SP_NB=""; SP_EN=""; SPWHY="-"
# A5
read -r gk gs gn gw <<< "$(gate5 "$A" A5)"
if [ "$gk" = NEW ]; then
  [ ! -f run/start_point.json ] && [ ! -e "$C1" ] && [ ! -e "$C2" ] && ! compgen -G "run_aborted/${JOB}_c[12]_*" > /dev/null \
    || fin5 8 REVIEW "A5 가 없는데 뒤 단 기록이 있다 (시작점 · c1 · c2 · run_aborted 의 c 단)"
  cap_gate A5
  if [ "$W0OK" = 1 ]; then var=A5c; ws=$W0_WAVECAR; we=$W0_SHA; else var=A5f; ws=""; we=""; fi
  log "▶ A5 ($var · LDIPOL 끔 · MAXMIX 200 · AMIX 0.1 · AMIN 0.01 · NELM 300)"
  run_one5 A5 "$var" "$A" "$ws" "$we"; r=$?
  [ "$r" = 6 ] && env6_pre
  [ "$r" = 0 ] || stop5 3 "A5 준비 실패"
  read -r gk gs gn gw <<< "$(gate5 "$A" A5)"
fi
log "A5 → $gs (전자 반복행 $gn)"
on_stop "$gk" "$gs" "$gn" "$gw" A5
# 시작점
if [ -f run/start_point.json ]; then
  sp_load || fin5 8 REVIEW "시작점 기록 (run/start_point.json) 의 형식 · 경로가 맞지 않는다"
  log "시작점 $SPF (기록 · sha $SS · 다시 정하지 않는다)"
else
  { [ ! -e "$C1" ] && [ ! -e "$C2" ] && ! compgen -G "run_aborted/${JOB}_c[12]_*" > /dev/null; } \
    || fin5 8 REVIEW "c 단 (run/ 또는 run_aborted/) 이 있는데 시작점 기록이 없다 — 시작점은 첫 c 단 전에 한 번만 쓴다 (유실 뒤 다시 정하지 않는다 · Codex EN P1)"
  why=$(elig5 "$A"); e=$?
  case "$e" in
    0) SPF=A5; S=$A/WAVECAR; SS=$(wsha "$A/WAVECAR.info" sha256); SPH=$(info_head "$A/WAVECAR.info");;
    2) fin5 8 REVIEW "A5 끝 WAVECAR 이상 — $why";;
    *) if [ "$W0OK" = 1 ]; then
         SPF=W0; S=$W0_WAVECAR; SS=$W0_SHA; SPH=$(info_head run/w0_check.json); SPWHY=$why
         log "A5 자격 미달 — $why · c1 · c2 시작점 = 보존 ⓐ (복사본 · 개정 5 A5_자격_미달)"
       else
         log "✗ A5 자격 미달 — $why · 보존 ⓐ 도 확인 안 됨 → 값 없음 (이 잡은 닫는다)"; drop5
         fin5 1 CLOSED "A5 자격 미달 ($why) · 보존 ⓐ 확인 안 됨 — 값 없음 (개정 5 A5_자격_미달)"
       fi;;
  esac
  set -- $SPH; SP_NK=${4:-}; SP_NB=${5:-}; SP_EN=${6:-}
fi
# c1
read -r gk gs gn gw <<< "$(gate5 "$C1" c1)"
if [ "$gk" = NEW ]; then
  [ ! -e "$C2" ] && ! compgen -G "run_aborted/${JOB}_c2_*" > /dev/null || fin5 8 REVIEW "c1 이 없는데 c2 (run/ 또는 run_aborted/) 가 있다"
  cap_gate c1
  if [ ! -f run/start_point.json ]; then
    sp_write || stop5 3 "시작점 기록 (run/start_point.json) 쓰기 실패"
    log "시작점 $SPF 를 기록했다 (sha $SS — 이 뒤로 다시 정하지 않는다)"
  fi
  log "▶ c1 (Davidson · MAXMIX 200 · AMIX 0.1 · AMIN 0.01 · NELM 400 · 시작점 $SPF)"
  run_one5 c1 c1 "$C1" "$S" "$SS"; r=$?
  [ "$r" = 6 ] && env6_pre
  [ "$r" = 0 ] || stop5 3 "c1 준비 실패"
  read -r gk gs gn gw <<< "$(gate5 "$C1" c1)"
fi
log "c1 → $gs (전자 반복행 $gn)"
on_stop "$gk" "$gs" "$gn" "$gw" c1
s1=$gs
if [ "$gk" = OK ]; then
  [ ! -e "$C2" ] || fin5 8 REVIEW "c1 이 주 기준 수렴인데 c2 가 있다"
  drop5; log "✓ c1 주 기준 수렴 — c2 를 띄우지 않는다"; fin5 0 OK "c1 주 기준 수렴"
fi
# c2
read -r gk gs gn gw <<< "$(gate5 "$C2" c2)"
if [ "$gk" = NEW ]; then
  cap_gate c2
  log "▶ c2 (ALGO All · TIME 0.1 · NELM 400 · c1 = $s1 · 시작점 $SPF 의 새 복사본)"
  run_one5 c2 c2 "$C2" "$S" "$SS"; r=$?
  [ "$r" = 6 ] && env6_pre
  [ "$r" = 0 ] || stop5 3 "c2 준비 실패"
  read -r gk gs gn gw <<< "$(gate5 "$C2" c2)"
fi
log "c2 → $gs (전자 반복행 $gn)"
on_stop "$gk" "$gs" "$gn" "$gw" c2
drop5
[ "$gk" = OK ] && fin5 0 OK "c2 주 기준 수렴"
fin5 1 NO_PRIMARY "c1 $s1 · c2 $gs — 주 기준 값 없음 (보조 기준은 반송 뒤 V5 수집기)"
'''


def _env_text():
    """RUN_A5_ENV + 트리 관문 상수 (VASP_OUT · ATT1_TPL · W0_TPL — 검사기와 같은 바이트 · 러너 awk 는 \\001 · \\002 를 바이트로 푼다)."""
    tb = lambda s_: s_.replace("\x01", "\\001").replace("\x02", "\\002")
    return (RUN_A5_ENV.replace("@ATT_EXTRA@", "|".join(re.escape(x) for x in VASP_OUT)).replace("@PREP_ALLOW@", "|".join(re.escape(x) for x in PREP_ALLOW)).replace("@ATT1_T@", tb(ATT1_TPL))
            .replace("@W0_T@", tb(W0_TPL)))


def run_a5_text():
    P = r2_parts()
    funcs = "\n".join(P[n] for n in R2_FUNCS)
    head = (RUN_A5_HEAD.replace("@RET_ALLOW@", "|".join(re.escape(x) for x in RETURN_ALLOWED))
            .replace("@RET_FORBID@", "|".join(re.escape(x) for x in RETURN_FORBIDDEN)).replace("@JOB@", JOB)
            .replace("@CAP_H@", f"{CAP_H:g}").replace("@INFRA_MAX@", str(INFRA_MAX)))
    cli = (RUN_A5_CLI.replace("@PACK_ONLY@", P["pack_only"]).replace("@PERF@", P["perf"])
           .replace("@W0_REL@", W0_REL))
    txt = head + "\n# ── 외주 2차 러너 부품 (build_round2_vasp_package.RUN_ALL 에서 이름으로 꺼냄 · 패치 자리는 build_a5 r2_parts) ──\n" + funcs + "\n" + _env_text() + cli + RUN_A5_BODY
    for ph in ("@JOB@", "@RET_ALLOW@", "@RET_FORBID@", "@CAP_H@", "@INFRA_MAX@", "@PACK_ONLY@", "@PERF@", "@W0_REL@", "@ATT_EXTRA@", "@PREP_ALLOW@", "@ATT1_T@", "@W0_T@"):
        if ph in txt:
            raise PkgError(f"러너에 채우지 않은 자리 {ph}")
    if not _bash_ok(txt):
        raise PkgError("run_a5.sh 가 bash -n 을 통과하지 못한다")
    return txt


# ───────────────────────── 묶음 만들기 ─────────────────────────
def _decision_state(did, ledger=None):
    return R2._decision_state(did, ledger)


def load_registry(path=None, sha=None):
    """외주 2차 봉인 등록부 (같은 업체 · 같은 빌드 · 같은 PP · 재시작 문구) — sha 고정 · schema · 문구 regex 형식."""
    path = path or os.path.join(REPO, REG_PATH)
    sha = (sha or REG_SHA256).lower()
    if _sha(path) != sha:
        raise PkgError("외주 2차 등록부 sha 가 고정값과 다르다")
    reg = json.load(open(path, encoding="utf-8"))
    if reg.get("schema") != R2.REG_SCHEMA:
        raise PkgError(f"등록부 schema {reg.get('schema')!r}")
    rx = reg.get("restart_read_regex") or ""
    if not rx or R2.restart_regex_problems(rx):
        raise PkgError(f"등록부 재시작 문구 regex 형식 {R2.restart_regex_problems(rx) if rx else '없음'}")
    for sp in ("Li_sv", "P", "S", "Cl", "Ag"):
        if not V.HEX64.match(str((reg.get("species_sha256") or {}).get(sp, ""))) or not (reg.get("titel") or {}).get(sp):
            raise PkgError(f"등록부에 {sp} sha · TITEL 이 없다")
    return reg, sha


def w0_expect_from_a4(path=None, sha=None):
    """⓪ 기대값 — 외주 2차 a4 결과 (sha 고정) 의 a4A WAVECAR 기록에서 읽고, 모듈 상수 (개정 5 원문 값) 와 같은지 대조한다."""
    path = path or os.path.join(REPO, A4_RESULT)
    if _sha(path) != (sha or A4_RESULT_SHA256):
        raise PkgError("a4 결과 JSON sha 가 고정값과 다르다")
    w = json.load(open(path, encoding="utf-8"))["result"]["attempts"]["a4A"]["wavecar"]
    got = {"sha256": w["sha256"], "size": int(w["size"]), "NKPTS": w["outcar"]["NKPTS"], "NBANDS": w["outcar"]["NBANDS"], "ENCUT": w["outcar"]["ENCUT"]}
    want = {"sha256": W0_SHA256, "size": W0_SIZE, **W0_DIMS}
    if got != want:
        raise PkgError(f"a4 결과의 ⓐ WAVECAR 기록 {got} ≠ 개정 5 값 {want}")
    hd = str(w.get("head", "")).split()
    if len(hd) < 6 or hd[3] != W0_DIMS["NKPTS"] or hd[4] != W0_DIMS["NBANDS"] or abs(float(hd[5]) - float(W0_DIMS["ENCUT"])) >= 0.05:
        raise PkgError(f"a4 결과의 ⓐ WAVECAR 머리 {hd} 가 기대 크기와 다르다")
    return want


def build(out, v5_pkg=None, ledger=None, registry=None, w0=None, check_decision=True):
    """V5 봉인 잡 (sha 대조) → a5 묶음 폴더 (INCAR 변형 넷 · 봉인 환경 · 러너 · jobs.json · MANIFEST). 구조를 새로 만들지 않는다.
    registry · w0 는 시험용 주입 (없으면 외주 2차 봉인 등록부 · a4 결과의 ⓐ WAVECAR 기록)."""
    if check_decision:
        st = _decision_state(DECISION, ledger)
        if st != "active":
            raise PkgError(f"{DECISION} 가 원장에서 active 가 아니다 ({st}) — 묶음을 만들지 않는다")
    amend = open(os.path.join(REPO, AMEND5), encoding="utf-8").read()
    for s_ in (W0_SHA256, "6,820,958,848", "MAXMIX 200", "TIME 0.1", "NELM 400", "180 h"):
        if s_ not in amend:
            raise PkgError(f"개정 5 원문에 '{s_}' 가 없다 — 도구 상수와 개정이 어긋났을 수 있다")
    reg, reg_sha = (registry if registry is not None else load_registry())
    w0 = w0 or w0_expect_from_a4()
    v5_pkg = v5_pkg or os.path.join(REPO, R2.V5_PKG)
    if _sha(os.path.join(v5_pkg, "MANIFEST.sha256")) != R2.V5_MANIFEST_SHA256:
        raise PkgError("V5 묶음 MANIFEST sha 가 고정값과 다르다 — a5 입력을 만들지 않는다")
    v5man = R2._manifest_lines(os.path.join(v5_pkg, "MANIFEST.sha256"))
    vj = {j["dir"]: j for j in json.load(open(os.path.join(v5_pkg, "jobs.json"), encoding="utf-8"))["jobs"]}[SRC]
    src = os.path.join(v5_pkg, "jobs", SRC)
    files = {}
    for f in ("POSCAR", "KPOINTS", "POTCAR.spec"):
        t = open(os.path.join(src, f), encoding="utf-8").read()
        if _sha_text(t) != v5man.get(f"jobs/{SRC}/{f}"):
            raise PkgError(f"V5 {SRC}/{f} sha 가 V5 MANIFEST 와 다르다")
        files[f] = t
    base = open(os.path.join(src, "INCAR"), encoding="utf-8").read()
    if _sha_text(base) != v5man.get(f"jobs/{SRC}/INCAR"):
        raise PkgError(f"V5 {SRC}/INCAR sha 가 V5 MANIFEST 와 다르다")
    for var in DELTA:
        t = variant_text(base, var)
        verify_variant(base, t, var)
        files[INCAR_OF[var]] = t
    if os.path.exists(out) and os.listdir(out):
        raise PkgError(f"{out} 가 비어 있지 않다 — 덮어쓰지 않는다")
    d = os.path.join(out, "jobs", JOB)
    os.makedirs(d, exist_ok=True)
    for n, t in files.items():
        _write(os.path.join(d, n), t)
    env = [("vasp_version", reg["vasp_version"])] + [("species_sha256", sp, reg["species_sha256"][sp]) for sp in vj["potcar_spec"]] \
        + [("restart_read_regex", reg["restart_read_regex"]), ("registry_sha256", reg_sha), ("w0_sha256", w0["sha256"]), ("w0_size", str(w0["size"])),
           ("w0_nkpts", w0["NKPTS"]), ("w0_nbands", w0["NBANDS"]), ("w0_encut", w0["ENCUT"]), ("cap_h", f"{CAP_H:g}"), ("infra_max", str(INFRA_MAX))]
    _write(os.path.join(out, "SEALED_ENV.tsv"), "".join("\t".join(x) + "\n" for x in env))
    _write(os.path.join(out, "run_a5.sh"), run_a5_text()); os.chmod(os.path.join(out, "run_a5.sh"), 0o755)
    job = {k: vj[k] for k in ("nions", "composition", "nelect_expected", "potcar_spec", "pp_expected_titel", "zval_expected", "encut", "sigma",
                              "kpts", "cell_A", "dipol_z", "area_A2", "structure_sha256", "d3_2body_eV_ref")}
    job.update({"dir": JOB, "method": "v5", "ismear": 1, "stage": "a5",
                "stages": {v: {"incar": INCAR_OF[v], "nelm": NELM[v], "delta": DELTA[v], "echo_expect": ECHO_EXPECT[v], "row_headers": list(ROW_HDR[STAGE_OF_VAR[v]])}
                           for v in DELTA},
                "v5_source": {"pkg": R2.V5_PKG, "job": SRC, "manifest_sha256": R2.V5_MANIFEST_SHA256,
                              "files_sha256": {f: v5man[f"jobs/{SRC}/{f}"] for f in ("POSCAR", "KPOINTS", "POTCAR.spec", "INCAR")}},
                "files_sha256": {n: _sha_text(t) for n, t in files.items()}})
    meta = {"schema": SCHEMA_PKG, "amendment_5": AMEND5, "decision": DECISION,
            "status": "a5 묶음 v2 — 발송 전 독립 리뷰 (P0 2 · P1 4) 반영 · 개정 5 해석 1 (사용자 2026-11-20) · 발송 전 재검토 대기",
            "interpretation_1": INTERP1, "c1_secondary_order_rule": C1_SEC_ORDER, "exit_codes": EXIT_CODES,
            "start_point_rule": "첫 c 단을 띄울 때 한 번 run/start_point.json (from A5|W0 · path · sha256 · head) 에 두고 다시 정하지 않는다 · 검사기는 c 단을 그 기록에 대조하고, 그 기록이 규칙 (A5 자격 → A5 · 아니면 ⓪ · 둘 다 아니면 닫음) 과 같은지 따로 본다",
            "final_record": "끝 (0 · 1 · 5 상한 · 8 · 돈 뒤의 6 — VASP 빌드 다름) 에 run/final.json — 다시 돌려도 아무것도 띄우지 않는다 · 검사기는 끝 기록이 기록으로 낸 사다리 판정과 같은지 본다 (보수 쪽으로만)",
            "complete_row_rule": ("완전한 전자 반복행만 센다 (러너 row_scan = 검사기 row_gate · Codex EO P0 · EP P0): 줄바꿈까지 쓰임 · 그 단의 머리 그대로 · ':' 뒤 빈칸 · "
                                  "칸 6 또는 7 (N E dE d eps ncg rms [rms(c)]) · 숫자로 읽힘 (N 양의 정수 · ncg 정수 · 실수 칸 — 지수 두 자리) · 완전한 행 ≥ 1 뒤 줄바꿈 없는 끝 조각은 세지 않음 · "
                                  "완전한 행 0 + 행꼴 조각 또는 콜론 앞 머리 조각 (앞 빈칸을 걷은 글자 1–4 · 앞 빈칸 뒤 'N' 만 열 제목 0 스텝) · 줄바꿈 있는 덜 쓴 행 · 숫자로 안 읽히는 행 · "
                                  "칸 길이 > 24 (늘 유한 · Codex EQ) · 남의 머리 · NUL = 손상 → 끝 기록과 관계없이 멈춤 8"),
            "record_grammar": ("한 줄 기록 REC1 (killed.json · infra_abort.json · attempt.start · final.json — 러너 rec5 = 검사기 rec_parse · Codex EO P1): 한 줄 · NUL 없음 · "
                               "{\"키\": 값, …} · 토큰 사이 빈칸/탭 · 키 [a-z][a-z0-9_]* · 값 = JSON 문자열 (제어 바이트 날것 금지) 또는 음 아닌 정수 (16 자리 이하) · 같은 키 금지 · "
                               "값 비교는 원문 · 러너는 손으로 넣은 글을 JSON 이스케이프 (jstr) 해서 쓰고 UTF-8 이 아니면 쓰지 않는다 (u8ok) · 잡 id · 취소 시각 · 사유는 쓸 때 · 읽을 때 "
                               "비거나 빈칸 문자 (공백 · 탭 · LF · VT · FF · CR · 원문은 그 이스케이프까지) 뿐이면 거부 (Codex EP · EQ) · 기록 파일은 읽을 때 UTF-8 이어야 한다 (트리 관문) · attempt.json · w0_check.json 은 printf 틀 그대로 (tpl5 = tpl_parse)"),
            "time_source_rule": ("벽시계 출처 (러너 wall_of = 검사기 wall_of · Codex EO P1 · EP P1): 보존 폴더 (run_aborted/) 는 그 중단 영수증 wall_s 만 · 진행 폴더는 영수증을 보지 않고 "
                                 "끊김 기록 wall_s (그 시작 기록과 결속된 것만 · 끝 기록과 함께 있으면 트리 관문이 멈춤 · Codex EQ) → attempt.json elapsed_s → 미상 · "
                                 "검사기는 띄운 시도마다 앞 시도들의 합이 알려졌고 ≤ 상한인지 · 미상 영수증 뒤 시도 없음 · 채운 시각 ≤ 다음 시작을 본다"),
            "ledger_rule": ("중단 장부 (run/infra_aborts.tsv) ↔ 보존 폴더 (run_aborted/) ↔ 영수증 양방향 · 장부 줄 순서 = 기록 시각 · 시작 시각 순 + 단 순서 A5 ≤ c1 ≤ c2 (Codex EQ P2) · "
                            "진행 폴더에 영수증 없음 (트리 관문) "
                            "(러너 ledger5 = 검사기 ledger_problems + abort_receipt_problem · Codex EO P1 · EP P1 · P2) — 어긋나면 러너 멈춤 8 · 검사기 LADDER_VIOLATION"),
            "history_rule": ("시도 이력 run/status.tsv (끝난 시도마다 한 줄 · 마지막 칸 run_id) 의 줄마다 지금 · 보존 폴더의 끝난 시도 (run_id · 변형) 가 있어야 한다 "
                             "(러너 hist5 = 검사기 history_problems · Codex EP P1) · 0 바이트 · 줄바꿈 없는 끝 · 비 UTF-8 은 거부 · 머리만 있는 파일은 받는다 (Codex EQ) — 트리 관문 · 어긋나면 멈춤 8 · LADDER_VIOLATION"),
            "final_attempts_rule": ("run/final.json attempts = 시도 폴더=run_id 목록 (경로 바이트 순 · 러너 att5 = 검사기 attempts_of · Codex EO P2) · code/state 는 fin5 가 쓰는 조합만 "
                                    "(0 OK · 1 NO_PRIMARY|CLOSED · 5 CAP · 6 ENV · 8 REVIEW · Codex EQ) — 어긋나면 트리 관문 (러너 8 · 검사기 LADDER_VIOLATION) · 끝 기록 없는 반송은 "
                                    "STOPPED_FOR_REVIEW · 끝난 시도의 attempt.json run_id · t_start = attempt.start (att_ok5 = att_problem)"),
            "tree_gate_rule": ("트리 관문 하나 (러너 tree5 = 검사기 tree_problems · 같은 규칙 · 같은 사유 낱말 · Codex EQ): 기록 명령 · PACK_ONLY · 다시 돌림 · 단 발사 직전 · 포장 "
                               "(기존 반송본을 덮기 전) 마다 — 이름 (run/ · run_aborted/ · 시도 폴더 = 반송 허용 · 금지 · VASP 표준 출력만 · 잔여 *.part · 링크 · 하위 폴더 거부) → "
                               "시도 폴더마다 시작 기록 · UTF-8 · 끝 기록 틀 · 신원 · 봉인 (sha 표 = 지금 파일) · 끊김 기록 자리 · 문법 · 결속 · 진행 폴더 영수증 → 장부 · 영수증 · 이력 → "
                               "끝 기록 → 시작점 → ⓪ 기록 → 기존 반송본 ⊆ 지금 트리 (러너만) — 첫 사유에서 종료 8 · 아무것도 쓰지 않는다 (원본 보존) · "
                               "Codex ER: A5 WAVECAR 지우기 · 끝 기록 쓰기 전에도 · 준비 폴더는 띄우기 전 이름만 (실행 기록은 지우지 않고 멈춤) · 끝 기록 잡 · 변형 · stage = 시작 기록 · "
                               "POTCAR 해시 = POTCAR.sha256 · 이력 줄 벽시계 = 끝 기록 elapsed_s · 기존 반송본 대비 완전한 행 · 영수증 벽시계 후퇴 없음 (UNKNOWN → 확정값만)"),
            "zero_step_rule": ("0 스텝 (--infra-abort · 0 행 다시 돌림) 은 OSZICAR 가 빈 줄 · 열 제목 (N E dE d eps ncg rms [rms(c)] · 잘린 끝은 그 앞부분 · 앞 빈칸) 뿐일 때만 — "
                               "그 밖의 줄은 unexplained_line → 검토 종료 8 (러너 row_scan = 검사기 row_gate · Codex ER Q-ER-2)"),
            "lock_rule": ("계산 · 기록 명령 (--infra-abort · --infra-wall · --killed · --reset-w0) · PACK_ONLY 는 같은 배타 잠금 (run/.a5.lock · lock_take) 을 검사부터 쓰기 끝까지 쥔다 — "
                          "겹친 두 번째는 종료 2 · 먼저 쓴 기록 보존 (Codex ER Q-ER-3②)"),
            "tool_sha256": _sha(os.path.abspath(__file__)), "round2_tool_sha256": _sha(os.path.abspath(R2.__file__)), "v5_tool_sha256": _sha(os.path.abspath(V.__file__)),
            "sources": {"v5_manifest_sha256": R2.V5_MANIFEST_SHA256, "registry_path": REG_PATH, "registry_sha256": reg_sha,
                        "a4_result": A4_RESULT, "a4_result_sha256": A4_RESULT_SHA256},
            "w0": {"rel_path_in_round2_pkg": W0_REL, **{k: w0[k] for k in ("sha256", "size", "NKPTS", "NBANDS", "ENCUT")},
                   "⛔": "원본은 읽기만 — 러너는 복사본만 쓴다 · 업체가 지웠으면 W0_WAVECAR=none (A5 새로 시작)"},
            "ladder": "⓪ 확인 → A5 (A5c 이어서 · A5f 새로) → c1 → c1 이 주 기준 OK 가 아니면 c2 · A5 자격 미달이면 c1 · c2 는 ⓪ 복사본에서 · ⓪ 도 없으면 값 없음",
            "cap_h": CAP_H, "infra_max_per_job": INFRA_MAX,
            "secondary": {"stages": ["c1", "c2"], "window_last": SEC_W1, "window_prev": SEC_W0, "min_steps": SEC_MIN_STEPS,
                          "u_E": "max(range(W1), |mean(W1) − mean(W0)|)", "⛔": "u_W 문턱 · G4 판정 · 채택은 V5 수집기 (--a5_result)"},
            "return_allowed": RETURN_ALLOWED, "return_forbidden": RETURN_FORBIDDEN, "jobs": [job]}
    _write(os.path.join(out, "jobs.json"), json.dumps(meta, ensure_ascii=False, indent=1, allow_nan=False))
    lines = []
    for root, _, fs in os.walk(out):
        for f in sorted(fs):
            p = os.path.join(root, f); r = os.path.relpath(p, out).replace(os.sep, "/")
            if r in ("MANIFEST.sha256", "README.md") or r.startswith(("run/", "run_aborted/")):
                continue
            lines.append(f"{_sha(p)}  {r}")
    _write(os.path.join(out, "MANIFEST.sha256"), "\n".join(sorted(lines, key=lambda s: s.split("  ", 1)[1])) + "\n")
    msha = _sha(os.path.join(out, "MANIFEST.sha256"))
    _write(os.path.join(out, "README.md"), _readme(meta, msha))
    return meta, msha


INTERP1 = ("개정 5 해석 1 (사용자 2026-11-20 · 1저자 · AskUserQuestion '멈추고 1저자에게 (Recommended)') — 러너는 지금 단이 SCF_NOT_CONVERGED 이거나 "
           "전자 반복행 ≥ 1 인 실행 실패 (행 ≥ 1 끊김을 --killed 로 기록한 것 포함) 로 끝났을 때만 다음 단을 띄운다 · 전자 반복행 0 → 멈춤 (종료 7 · "
           "--infra-abort (스케줄러 기록) 또는 연락 · 다음 단을 쓰지 않는다) · RESTART_NOT_HONOURED · SCF_UNVERIFIED · 설정 · 무결성 실패 → 멈춤 (종료 8 · 1저자 — "
           "개정 5 결과별_처리 '재시작_미이행 … 더 돌리지 않는다' · 개정 4 다음_단_자격) · A5 가 행은 있는데 자격 미달이면 개정 5 그대로 (⓪ 이 확인되면 그 복사본에서 c1 · c2 · 아니면 닫음)")
C1_SEC_ORDER = ("c1 보조 채택은 c2 가 확인된 끝 (SCF_NOT_CONVERGED · 행 ≥ 1 실행 실패 · 행 ≥ 1 끊김 기록) 일 때만 — c2 가 없음 · 준비만 · 끝 기록 없음 · 0 스텝 중단 "
                "(run_aborted 에만) 이면 LADDER_INCOMPLETE · c2 가 SCF_UNVERIFIED · RESTART_NOT_HONOURED · 설정 · 무결성 실패면 c2 의 주 기준이 미정이라 STOPPED_FOR_REVIEW "
                "(자동 채택 없음 → 1저자 · 주 세션 해석 2026-11-20 · 보수)")
EXIT_CODES = {"0": "c1 또는 c2 주 기준 수렴 (끝)", "1": "주 기준 값 없음 — 사다리 끝 (끝 · 실패도 기록)", "2": "인자 · 묶음 · 환경 · 잠금 오류 (아무것도 띄우지 않음)",
              "3": "준비 실패 (그 단 소모 안 함 — 원인을 고친 뒤 다시)", "4": "포장 실패 (PACK_ONLY=1)",
              "5": "누적 상한 (끝) 또는 끊긴 시도 · 벽시계 미상 (--killed · --infra-abort · --infra-wall 로 기록한 뒤 다시)",
              "6": "공통 환경 고장 (VASP 빌드 · PP — 전체 정지 · 돈 뒤 빌드가 다르면 끝 · 띄우기 전 PP 불일치는 끝 기록 없음)", "7": "전자 반복행 0 (멈춤 · --infra-abort 또는 연락)", "8": "1저자 검토 멈춤 (끝) · 또는 트리 관문 — 모르는 · 못 읽는 · 서로 안 맞는 기록 (아무것도 쓰지 않음 · 원본 보존 · 연락)"}


def _readme(meta, msha):
    return f"""# W_ad a5 — 은 쪽 G4 ENCUT 650 분리 끝점 재시도 (개정 5 v2)

- 묶음 MANIFEST sha256: `{msha}` (받은 뒤 `sha256sum MANIFEST.sha256` 로 같은지 확인)
- 잡: `{JOB}` 하나 · 사다리 {meta['ladder']}
- 누적 상한 {CAP_H:g} h (넘으면 다음 단을 띄우지 않고 끝낸다) · 0 스텝 인프라 중단은 잡 전체 {INFRA_MAX} 회

## 0. 돌리기 전에
1. **새 빈 폴더**에 풀어 주세요 — 외주 2차 폴더에 풀지 마세요. 폴더에 a5 가 아닌 것 (다른 잡 폴더 · `run_all.sh` · 다른 반송 묶음 …) 이 있으면
   러너는 아무것도 띄우지 않고 종료 2 로 멈춥니다. 묶음 zip · 제출 스크립트는 폴더 밖에 두세요 (스케줄러 출력 `*.o<잡 번호>` · `*.e<잡 번호>` 는 괜찮습니다).
2. **보존 ⓐ WAVECAR 를 먼저 확인** — 외주 2차 러너는 a4 잡이 SCF_NOT_CONVERGED 로 끝날 때 `stageA/WAVECAR` 를 지우게 돼 있었고,
   반송된 env.txt 에 '남긴다' 줄이 없습니다 → **없을 가능성이 높습니다**.
   ```
   ls -l <외주 2차 묶음>/{W0_REL}
   sha256sum <외주 2차 묶음>/{W0_REL}
   ```
   크기 {W0_SIZE:,} B · sha256 `{W0_SHA256}` 이면 그 **절대 경로**를 `W0_WAVECAR` 에 · **없으면 `W0_WAVECAR=none`** (A5 가 새로 시작합니다 — 개정 5 가 정한 길).
   ⛔ 외주 2차 러너 (`run_all.sh`) 를 다시 돌리지 마세요 — 그 파일이 남아 있으면 지울 수 있습니다.
   경로를 잘못 주면 (없는 파일) 러너가 기록하지 않고 종료 2 로 멈춥니다. 있는 파일인데 sha · 크기 · 머리가 다르면 '확인 안 됨' 으로 기록하고 A5 를 새로 시작합니다
   (A5 를 띄우기 전에만 `bash run_a5.sh --reset-w0` 로 그 기록을 지울 수 있습니다).
3. 확인된 보존 ⓐ 는 **a5 가 끝날 때까지 지우거나 옮기지 마세요** (A5 가 자격 미달이면 c1 · c2 가 그 복사본에서 시작합니다).
4. **병렬 배치는 외주 2차와 같게 — 세 단 모두** `mpirun -np 64` · `PERF_TAGS_FILE` 에 `NCORE = 4` · `KPAR = 2` (한 줄에 하나). 그래야 NBANDS 가 872 그대로이고
   c1 · c2 가 시작 WAVECAR 를 온전히 읽습니다 — 띠 수가 다르면 재시작이 온전하지 않아 러너가 멈추고 (종료 8) 자동 채택이 없습니다.
5. 경로 (`W0_WAVECAR` · `POTCAR_DIR` · `PERF_TAGS_FILE`) 는 **절대 경로**로 (상대 경로는 러너를 부른 폴더 기준으로 풉니다).
6. **디스크 여유 약 14–21 GB** — A5 끝 WAVECAR 6.8 GB + c 단 시작 복사본 6.8 GB (단이 끝나면 지움 · 보존 ⓐ 가 같은 디스크면 21 GB 쪽).
   복사 중 디스크가 차면 그 단은 소모되지 않습니다 (종료 3 · 비운 뒤 다시).

## 1. 돌리는 법
```
W0_WAVECAR=<보존 ⓐ 절대 경로 또는 none> VASP_CMD="mpirun -np 64 vasp_std" POTCAR_DIR=<PAW_PBE 절대 경로> PERF_TAGS_FILE=<절대 경로> bash run_a5.sh
```

## 2. 단과 최악 벽시계 (스텝당 약 395 s · c2 는 2 배 가정)
| 단 | 설정 | 최악 벽시계 |
|---|---|---|
| A5 | LDIPOL 끔 · MAXMIX 200 · AMIX 0.1 · AMIN 0.01 · NELM 300 | ≈ 33 h |
| c1 | Davidson · MAXMIX 200 · AMIX 0.1 · AMIN 0.01 · NELM 400 | ≈ 44 h |
| c2 | ALGO All · TIME 0.1 · NELM 400 (c1 이 주 기준 수렴이 아닐 때만) | ≤ ≈ 88 h |

- 스케줄러 시간 제한은 그 배치가 띄울 단들의 최악 합보다 길게 (한 배치에 다 돌리면 ≥ 170 h).
  **전자 반복행이 하나라도 나온 뒤 스케줄러가 끊은 단은 소모됩니다** (값 없음 · `--killed` 로 기록 · 다시 돌리면 다음 단부터).
- 누적 상한 {CAP_H:g} h 를 넘으면 다음 단을 띄우지 않고 끝냅니다 (종료 5 · 1저자).

## 3. 다음 단으로 가는 조건 — 개정 5 해석 1 (사용자 2026-11-20)
- **A5 → c1 (시작점 고르기)**: A5 가 수렴 · 미수렴 · 전자 반복행 ≥ 1 인 실행 실패 (끊김을 `--killed` 로 기록한 것 포함) 로 끝나면 c1 을 띄웁니다.
  A5 의 결과는 c1 · c2 의 **시작점**만 정합니다 — A5 가 자격이 있으면 (정상 종료 · 수렴 또는 미수렴 · WAVECAR 온전) A5 끝 WAVECAR, 아니면 확인된 보존 ⓐ 의 복사본 ·
  둘 다 아니면 닫습니다 (종료 1 · 값 없음). 시작점은 c1 을 처음 띄우기 전에 `run/start_point.json` 에 한 번 쓰고 다시 정하지 않습니다 (이 파일을 지우거나 옮기지 마세요).
- **c1 → c2 (다음 단 조건)**: c1 이 주 기준 수렴이면 끝입니다 (종료 0 · c2 를 띄우지 않습니다). c2 는 c1 이 **SCF_NOT_CONVERGED** 이거나
  **전자 반복행 ≥ 1 인 실행 실패** (끊김을 `--killed` 로 기록한 것 포함) 로 끝났을 때만 띄웁니다.
- 어느 단이든 **전자 반복행 0** → 멈춤 (종료 7 · 다음 단을 쓰지 않습니다): 스케줄러 기록이 있는 0 스텝 인프라 중단이면 `--infra-abort` 로 기록한 뒤 다시 (같은 단부터) ·
  아니면 (실행 파일 · 모듈 · 입력 문제) 고치기 전에 연락 주세요.
- **재시작 미이행 · SCF 미확인 (그 단의 것이 아닌 행 머리 포함) · 설정 에코 다름 · 끊김 기록 (killed.json) 이 그 시도와 다름** → 멈춤 (종료 8 · 끝 · 1저자 검토).
  `--killed` 로 기록한 끊긴 시도에도 같은 원문 검사를 합니다 (끊겼다고 검사를 건너뛰지 않습니다).
- **전자 반복행은 '완전한 행' 만 셉니다** (러너 · 반송 검사 같은 기준): 줄바꿈까지 쓰였고 · 그 단의 머리 (A5 · c1 `DAV:` `RMM:` · c2 `SDA:` `CGA:`) 그대로 ·
  `:` 뒤 빈칸 · 칸 6 또는 7 개 (N E dE d eps ncg rms [rms(c)]) · **숫자로 읽히는** 줄 (N 양의 정수 · ncg 정수 · 나머지 실수). 스케줄러가 끊어 마지막 줄이
  줄바꿈 없이 잘렸으면 그 조각은 세지 않습니다 (앞에 완전한 행이 있으면 보통의 끊김입니다). **완전한 행이 0 인데 행 조각만 있거나 (예: 첫 줄이 `SDA:` 또는
  콜론 앞 `SDA` 에서 잘림) · 줄바꿈까지 쓰인 덜 쓴 행 · 숫자로 읽히지 않는 행이 있으면 '행 손상'** → 끝 기록이 있든 없든 멈춤 (종료 8) · `--killed` · `--infra-abort` 로
  기록하지 않습니다 (둘 다 거부).
- **중단 장부 (`run/infra_aborts.tsv`) 와 보존 폴더 (`run_aborted/`) · 영수증이 서로 맞지 않으면** (한쪽에만 있는 중단 · 다른 벽시계 · 다른 run_id) → 멈춤 (종료 8) —
  시작점을 다시 쓰거나 어느 단도 다시 띄우지 않습니다. 장부 줄은 일어난 순서 (기록 시각 · 시작 시각 순) 여야 합니다. **진행 폴더 (`run/<잡>_<단>/`) 에
  중단 영수증 (`infra_abort.json`) 이 있거나 · 시도 이력 (`run/status.tsv`) 의 줄에 해당하는 끝난 시도 폴더가 없어도** 같은 멈춤 (종료 8) 입니다.
- **트리 관문 (같은 검사 하나 — 기록 명령 · `PACK_ONLY=1` · 다시 돌림 · 단을 띄우기 직전 · A5 `WAVECAR` 를 지우기 · 끝 기록을 쓰기 전 · 포장 = 기존 `a5_return.tgz` 를 덮기 전)**: 아래 중 하나라도 걸리면
  **아무것도 쓰거나 띄우거나 포장하지 않고 종료 8** 입니다 (`run/` · `run_aborted/` · `a5_return.tgz` 그대로 — 화면의 `⛔ 트리 관문 …` 줄을 그대로 보내 주세요).
  모르는 이름 · 남은 `*.part` · 링크 · 하위 폴더 (시도 폴더에는 반송 이름 · VASP 표준 출력만) · 시작 기록 (`attempt.start`) 이 그 폴더의 시도가 아님 ·
  끝 기록 (`attempt.json`) 이 잘렸거나 그 시작 기록과 다름 · 끝 기록 뒤에 바뀐 파일 (OUTCAR · OSZICAR · INCAR … sha 표) · 끝난 시도에 끊김 기록 (`killed.json`) ·
  끊김 기록이 그 시도와 다름 · 진행 폴더의 중단 영수증 · 중단 장부 · 영수증 · 시도 이력 (`run/status.tsv` — 0 바이트 · 잘린 줄 · 끝난 시도 없는 줄) ·
  끝 기록 (`run/final.json`) 의 코드 · 상태 조합 · 시도 목록 · 시작점 · ⓪ 기록 · UTF-8 아닌 기록 · 옆의 `a5_return.tgz` 보다 트리가 과거 (그 안의 끝 기록 · 끝난 시도가 지금 없음 ·
  그 안의 완전한 전자행이 줄었음 · 확정된 영수증 벽시계가 바뀌거나 UNKNOWN 으로 되돌아감) · 준비 폴더 (`run/.prep_…`) 에 VASP 출력 (`OSZICAR` · `OUTCAR` …) — 실행 기록이라 지우지 않습니다 ·
  끝 기록의 잡 · 변형 · stage 가 시작 기록과 다름 · 끝 기록의 POTCAR 해시가 `POTCAR.sha256` 과 다름 · 시도 이력 줄의 벽시계가 그 끝 기록의 `elapsed_s` 와 다름.
- **0 스텝은 0 행으로 설명될 때만**: `--infra-abort` 와 0 행 다시 돌림은 `OSZICAR` 가 빈 줄 · 열 제목 (`N E dE d eps ncg rms …` — 잘린 끝은 그 앞부분) 뿐일 때만 받습니다.
  그 밖의 줄 (예: 콜론이 깨진 `SDA; …` · `SDA` 한 줄) 은 1저자 검토 (종료 8) 입니다.
- **잠금 하나**: 계산 · 기록 명령 (`--infra-abort` · `--infra-wall` · `--killed` · `--reset-w0`) · `PACK_ONLY=1` 은 같은 잠금 (`run/.a5.lock`) 을 검사부터 쓰기 끝까지 쥡니다 —
  겹친 두 번째 명령은 종료 2 (먼저 쓴 기록은 그대로) 입니다. 메시지대로 앞 명령이 끝난 뒤 다시 하세요.

## 4. 종료 코드
| 코드 | 뜻 | 할 일 |
|---|---|---|
| 0 | {EXIT_CODES['0']} | 반송 |
| 1 | {EXIT_CODES['1']} | 반송 |
| 2 | {EXIT_CODES['2']} | 메시지대로 고친 뒤 다시 |
| 3 | {EXIT_CODES['3']} | 디스크 · 권한 · 경로를 고친 뒤 다시 |
| 4 | {EXIT_CODES['4']} | `PACK_ONLY=1 bash run_a5.sh` |
| 5 | {EXIT_CODES['5']} | 상한이면 반송 · 끊김이면 `--killed` (행 ≥ 1) / `--infra-abort` (행 0) · 미상이면 `--infra-wall` |
| 6 | {EXIT_CODES['6']} | 반송하고 연락 (띄우기 전 PP 불일치는 POTCAR_DIR 를 잘못 준 경우에만 고쳐서 다시) |
| 7 | {EXIT_CODES['7']} | `--infra-abort` 뒤 다시 · 아니면 연락 |
| 8 | {EXIT_CODES['8']} | 반송하고 1저자 결정을 기다림 |

- **끝 (0 · 1 · 5 상한 · 8 · 돈 뒤의 6 — VASP 빌드 다름) 뒤에는 다시 돌려도 아무것도 띄우지 않습니다** (run/final.json 을 찍고 같은 코드로 끝) — 포장만 다시 하려면 `PACK_ONLY=1 bash run_a5.sh`.
  다시 돌렸을 때 `a5_return.tgz` 가 없거나 · sha256 이 안 맞거나 · 그 끝 기록 (run/final.json) 을 담지 않았으면 (중간에 만든 옛 묶음) 종료 4 입니다 — `PACK_ONLY=1 bash run_a5.sh` 로 포장만 다시 하고 그 묶음을 보내 주세요.
- 끝 기록 (`run/final.json`) 에는 이 사다리의 시도 폴더와 run_id 가 묶여 있습니다 — 다른 폴더 (다른 실행) 의 끝난 `a5_return.tgz` · `.sha256` 을 옮겨 오면
  다시 돌림 · 포장만 (`PACK_ONLY=1`) 모두 종료 8 (트리 관문 · 반송본을 덮지 않음 · 연락) 입니다. 끝 기록이 이 사다리의 것이 아니어도 (시도 목록 · 코드 · 상태) 종료 8 입니다.
- 보내는 것: `a5_return.tgz` + `a5_return.tgz.sha256` (`sha256sum -c a5_return.tgz.sha256` 통과 뒤). WAVECAR · CHGCAR · POTCAR 본문은 담지 않습니다.

## 5. 기록 명령 (계산이 돌고 있지 않을 때)
- 0 스텝 인프라 중단: `[WALL_S=<초>] bash run_a5.sh --infra-abort <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유>` — 뒤 단이 이미 있으면 거부 · 잡 전체 {INFRA_MAX} 회
- 벽시계 채우기 (영수증 벽시계가 UNKNOWN 일 때만 · 채운 시각도 적힙니다): `bash run_a5.sh --infra-wall <run_aborted 폴더 이름> <초>`
- 끊긴 시도 (완전한 전자 반복행 ≥ 1 · 행 손상 없음): `WALL_S=<초> bash run_a5.sh --killed <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유>` — 뒤 단이 이미 있으면 거부
- 영수증 (`infra_abort.json`) · 끊김 기록 (`killed.json`) 은 한 줄 JSON 입니다 — 사유에 따옴표 · 역슬래시 · 제어문자가 있어도 JSON 으로 이스케이프해서 적습니다.
  잡 id · 취소 시각 · 사유는 비울 수 없고 UTF-8 글이어야 합니다 (아니면 기록하지 않고 종료 2 — UTF-8 로 다시 적어 주세요).
  누적 상한은 0 스텝 중단의 **영수증 벽시계 (WALL_S · 스케줄러 장부 값)** 로 셉니다 (같은 폴더의 attempt.json 경과보다 먼저).
- ⓪ 기록 지우기 (A5 를 띄우기 전에만): `bash run_a5.sh --reset-w0`
- 잠금 지우기: 잠금 주인은 기계 이름 + PID 입니다. 다른 기계의 잠금은 살아 있는지 알 수 없어 러너가 거부합니다 —
  스케줄러로 그 잡이 끝났는지 확인한 뒤, 러너가 찍어 준 그대로 `bash run_a5.sh --unlock <기계> <PID>`.

## 6. 하지 말 것
- INCAR · POSCAR · KPOINTS 를 고치지 마세요 · 시도 폴더 (run/ · run_aborted/) 를 지우거나 옮기지 마세요 (러너가 이 기록으로 다음 단 · 시작점을 정합니다).
  복구할 때는 `run/` · `run_aborted/` · `run/infra_aborts.tsv` 를 **함께** 되살리세요 — 일부만 되살리면 장부 대조가 어긋나 종료 8 입니다.
  `run/` 를 옛 체크포인트로 되살렸는데 옆의 `a5_return.tgz` 가 더 뒤 (끝난 단 · 끝 기록이 있음) 이면 종료 8 — 반송본을 덮지 않습니다 (연락).
  끝 (종료 0 · 1 · 5 상한 · 8) 뒤에는 다시 돌려도 아무것도 띄우지 않습니다 — 포장만 다시 하려면 `PACK_ONLY=1 bash run_a5.sh`.
- 외주 2차 러너를 다시 돌리지 마세요.
"""


# ───────────────────────── 반송 검사 (시도 하나) ─────────────────────────
def _wavecar_info(attdir):
    wi = R2._read(os.path.join(attdir, "WAVECAR.info"))
    try:
        w = json.loads(wi) if wi else None
    except ValueError:
        w = None
    return w if isinstance(w, dict) else None


def _echo_body(body, var):
    """a5 가 바꾼 설정의 OUTCAR 해석값 (입력 에코 구획을 뺀 본문) → (없는 키, 모순, 읽은 값) — **러너 echo5 와 같은 키 · 같은 정규식 꼴 · 같은 허용치**
    (러너가 1저자 멈춤을 거는 부분집합 · selftest 가 같은 탐침으로 대조). NELM · LDIPOL (A5 = F · c 단 = T) · ECHO_EXPECT[변형]
    (A5 · c1: IALGO 38 · AMIX 0.1 · AMIN 0.01 · MAXMIX 200 · c2: IALGO 58 · TIME 0.1). 토큰이 있는데 유한수가 아니면 모순 (없음과 다르다)."""
    st = STAGE_OF_VAR[var]
    missing, bad = [], []
    tol = {"NELM": 0, "IALGO": 0, "MAXMIX": 0, "AMIX": 1e-3, "AMIN": 1e-4, "TIME": 1e-3}
    raw = {"NELM": V._last(r"^\s*NELM\s*=\s*(\d+)", body),
           "IALGO": V._last(r"^\s*IALGO\s*=\s*(\d+)", body),
           "AMIX": V._last(r"^\s*AMIX\s*=\s*([^;\s]+)\s*;\s*BMIX", body),
           "AMIN": V._last(r"^\s*AMIN\s*=\s*(\S+)", body),
           "MAXMIX": V._last(r"MAXMIX\s*=\s*(-?\d+)", body),
           "TIME": V._last(r"^\s*TIME\s*=\s*(\S+)", body)}
    got = {k: V._tok_float(v) for k, v in raw.items()}
    for k, e in [("NELM", NELM[var])] + list(ECHO_EXPECT[var].items()):
        if raw[k] is None:
            missing.append(k)
        elif got[k] is None or abs(got[k] - e) > tol[k] + 1e-12:
            bad.append(f"{k} {raw[k]} ≠ {e:g}" if got[k] is None else (f"NELM {int(got[k])} ≠ {e}" if k == "NELM" else f"{k} {got[k]:g} ≠ {e:g}"))
    ld = V._last(r"^\s*LDIPOL\s*=\s*(\S+)", body)
    want = "F" if st == "A5" else "T"
    if ld is None:
        missing.append("LDIPOL")
    elif ld.strip(".").upper()[:1] != want:
        bad.append(f"LDIPOL {ld.strip('.').upper()[:1]} ≠ {want}")
    return missing, bad, got


def echo5(out_text, var):
    """OUTCAR 원문 → 러너 echo5 와 같은 a5 설정 에코 관문 (없는 키, 모순). 입력 에코 구획 (INCAR: … POTCAR:) 은 뺀다."""
    if var not in STAGE_OF_VAR:
        return ["variant"], []
    m, b, _ = _echo_body(V._strip_incar_echo(out_text or "")[0], var)
    return m, b


def audit5(o, job, var):
    """OUTCAR 해석값 (입력 에코 제외) 대조 → (없는 키, 모순 목록, 근거). 외주 2차 audit_r2 와 같은 규칙 (NIONS · NELECT · ENCUT · 점유 · D3 · GGA · DIPOL ·
    EFIELD) + a5 설정 에코 (_echo_body — 러너 echo5 와 같은 부분집합: NELM · LDIPOL · IALGO · AMIX · AMIN · MAXMIX (A5 · c1) · TIME (c2)).
    A5 는 퍼텐셜 보정을 끈 단이라 DIPOL 근거가 없어도 된다."""
    s, text = o["settings"], o.get("_body", "")
    st = STAGE_OF_VAR[var]
    exp = {"NIONS": job["nions"], "NELECT": job["nelect_expected"], "ENCUT": job["encut"], "ISMEAR": job["ismear"], "SIGMA": job["sigma"],
           "ISPIN": 1, "IDIPOL": 3, "IVDW": 12, "VDW_S6": V.D3_PARAMS["s6"], "VDW_S8": V.D3_PARAMS["s8"],
           "VDW_A1": V.D3_PARAMS["a1"], "VDW_A2": V.D3_PARAMS["a2"], "VDW_RADIUS": V.VDW_RADIUS_A, "VDW_CNRADIUS": V.VDW_CNRADIUS_A}
    missing, bad = [], []
    for k, e in exp.items():
        v = s.get(k)
        if v is None:
            missing.append(k); continue
        if k == "SIGMA":
            ok = abs(v - e) <= V.SIGMA_ECHO_TOL + 1e-9
        elif k in ("ENCUT", "NELECT"):
            ok = abs(v - e) <= 0.05
        elif k in ("VDW_S6", "VDW_S8", "VDW_A1", "VDW_A2"):
            ok = abs(v - e) <= V.D3_PARAM_TOL + 1e-12
        elif k in ("VDW_RADIUS", "VDW_CNRADIUS"):
            ok = abs(v - e) <= V.D3_RADIUS_TOL + 1e-12
        else:
            ok = v == e
        if not ok:
            bad.append(f"{k} {v} ≠ {e}")
    gga = V._last(r"^\s*GGA\s*=\s*(\S+)\s+GGA type", text)
    if gga is None:
        missing.append("GGA")
    elif gga.upper() != "PE":
        bad.append(f"GGA {gga} ≠ PE (실제 교환함수)")
    em, eb, got = _echo_body(text, var)
    missing += em
    bad += eb
    dg, dbad = V.dipol_evidence(o, job["dipol_z"])
    bad += dbad
    if not dg and not dbad and st != "A5":
        missing.append("DIPOL")
    if s.get("EFIELD") is not None and abs(s["EFIELD"]) > 1e-12:
        bad.append(f"EFIELD {s['EFIELD']} (외부장 금지)")
    return missing, bad, {"DIPOL": dg, "echo": got, "echo5": {"missing": em, "bad": eb}}


def completeness5(o, missing, titel, job):
    """외주 2차 check_attempt ③ 과 같은 완결성 (방법 v5) → "OK" 또는 (상태, 사유). OK 시도와 보조 후보 (SCF_NOT_CONVERGED) 에 같이 쓴다."""
    if not o or not o["outcar_titel"] or len(o["outcar_titel"]) < len(titel):
        return "POTCAR_UNVERIFIED", "OUTCAR TITEL 이 없거나 앞부분만 있다"
    if any(k in missing for k in ("NIONS", "NELECT")):
        return "SYSTEM_UNVERIFIED", f"OUTCAR 에 {missing} 없음"
    if missing:
        return "SETTINGS_UNVERIFIED", f"해석값을 못 읽음: {missing}"
    if o["TOTEN_eV"] is None or o["E_sigma0_eV"] is None:
        return "ENERGY_UNPARSEABLE", "마지막 FREE ENERGIE 구획의 TOTEN·E(σ→0) 가 없다"
    if fin(job.get("d3_2body_eV_ref")) is None or o["Edisp_eV"] is None:
        return "D3_UNVERIFIED", "D3 기대값 또는 Edisp 없음"
    return "OK", None


def _jread(p):
    try:
        x = json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return x if isinstance(x, dict) else {}


def _times(d):
    """시도 폴더 → {start: t_start (attempt.json · 없으면 attempt.start) · end: attempt.json t_end · recorded: killed.json · infra_abort.json 의 recorded_s 중 늦은 것}
    (epoch 초 · 정수만 · 없으면 None) — 사다리 순서 대조 (리뷰 P0-2(a))."""
    isint = lambda x: isinstance(x, int) and not isinstance(x, bool)
    a = _jread(os.path.join(d, "attempt.json"))
    rec = [rec_i(rec_read(os.path.join(d, f)), "recorded_s") for f in ("killed.json", "infra_abort.json")]      # 한 줄 기록은 REC1 로만 읽는다 (러너와 같다)
    rec = [x for x in rec if x is not None]
    ts = rec_i(rec_read(os.path.join(d, "attempt.start")), "t_start")
    t0 = a.get("t_start") if isint(a.get("t_start")) else ts
    return {"start": t0, "end": a.get("t_end") if isint(a.get("t_end")) else None, "recorded": max(rec) if rec else None}


def _head_dims(head):
    """WAVECAR 머리 문자열 (wav_head 꼴 6 칸) → (NKPTS, NBANDS, ENCUT) 문자열 · 못 읽으면 None."""
    hd = str(head or "").split()
    return (hd[3], hd[4], hd[5]) if len(hd) >= 6 else None


KILLED_PROBLEMS = ("SCF_UNVERIFIED", "RESTART_NOT_HONOURED", "KILLED_RECORD_MISMATCH")    # 끊긴 시도에서 원문 · 기록이 모순일 때 (러너 killed5 · Codex EN P0 · P1)
SECS_RE = re.compile(r"(0|[1-9][0-9]{0,8})")                                                  # 러너 secs_ok 와 같은 꼴 (손으로 넣는 초)
RUN_ID_ASCII = re.compile(r"[0-9]{8}T[0-9]{6}-[0-9]+-[0-9]+")                                 # 러너 start_id 와 같은 꼴 (ASCII 숫자만 — V.RUN_ID_RE 의 \d 는 유니코드 숫자도 받는다)

# ───────────────────────── 한 줄 기록 문법 REC1 (러너 rec5 와 같은 문법 · Codex EO P1 Q-EO-2a) ─────────────────────────
#   killed.json · infra_abort.json · attempt.start · final.json — 러너가 printf 로 한 줄에 쓰고, 다음 단을 띄우기 전에 러너도 검사기도 이 문법으로 **전체를** 읽는다.
#   파일 = 한 줄 (+ 끝 줄바꿈 하나 있어도 없어도) · NUL 없음 · '{' 멤버 (',' 멤버)* '}' · 앞뒤와 토큰 사이 빈칸/탭 허용 (JSON 과 같다 — "run_id":"x" 도 받는다) ·
#   키 = "[a-z][a-z0-9_]*" · 값 = 문자열 (제어 바이트 0x00–0x1F 날것 금지 · 이스케이프 \" \\ \/ \b \f \n \r \t \uXXXX 만) 또는 음 아닌 정수 (선행 0 없음 · 16 자리 이하) ·
#   같은 키 두 번 금지 · 그 밖 (배열 · 객체 · 실수 · true/false/null · 음수) 은 거부. 문자열 값은 **원문** (이스케이프를 풀지 않은 바이트 — latin-1 로 1:1) —
#   값 비교는 양쪽 다 원문으로 한다 (_ 같은 다른 표기는 다른 값으로 본다 · 러너가 쓴 값은 이스케이프가 필요 없는 ASCII 다).
REC_KEY = re.compile(rb"[a-z][a-z0-9_]*")
REC_UINT = re.compile(rb"0|[1-9][0-9]{0,15}")
_REC_HEX = frozenset(b"0123456789abcdefABCDEF")
_REC_ESC = frozenset(b'"\\/bfnrt')


def rec_parse(raw):
    """한 줄 기록 바이트 → {키: ('s', 원문 str) | ('i', int)} · 문법 (REC1) 밖이면 None. 러너 rec5 (awk) 와 한 글자씩 같은 순서로 읽는다."""
    if not isinstance(raw, (bytes, bytearray)):
        return None
    s = bytes(raw)
    if s.endswith(b"\n"):
        s = s[:-1]
    if b"\n" in s or b"\x00" in s:
        return None
    n_, out = len(s), {}

    def ws(k):
        while k < n_ and s[k] in (0x20, 0x09):
            k += 1
        return k
    i = ws(0)
    if i >= n_ or s[i] != 0x7B:
        return None
    i += 1
    while True:
        i = ws(i)
        if i >= n_ or s[i] != 0x22:
            return None
        j = s.find(b'"', i + 1)
        if j < 0 or not REC_KEY.fullmatch(s[i + 1:j]):
            return None
        key = s[i + 1:j].decode("ascii")
        i = ws(j + 1)
        if i >= n_ or s[i] != 0x3A:
            return None
        i = ws(i + 1)
        if i >= n_:
            return None
        if s[i] == 0x22:
            j = i + 1
            while True:
                if j >= n_:
                    return None
                c = s[j]
                if c == 0x22:
                    break
                if c < 0x20:
                    return None
                if c == 0x5C:
                    e = s[j + 1] if j + 1 < n_ else None
                    if e is not None and e in _REC_ESC:
                        j += 2
                        continue
                    if e == 0x75 and len(s[j + 2:j + 6]) == 4 and all(x in _REC_HEX for x in s[j + 2:j + 6]):
                        j += 6
                        continue
                    return None
                j += 1
            val, i = ("s", s[i + 1:j].decode("latin-1")), j + 1
        else:
            j = i
            while j < n_ and 0x30 <= s[j] <= 0x39:
                j += 1
            if not REC_UINT.fullmatch(s[i:j]):
                return None
            val, i = ("i", int(s[i:j])), j
        if key in out:                                   # 같은 키 두 번 (러너 rec5 도 거부)
            return None
        out[key] = val
        i = ws(i)
        if i < n_ and s[i] == 0x2C:
            i += 1
            continue
        if i < n_ and s[i] == 0x7D:
            i += 1
            break
        return None                                      # 멤버 뒤에 ',' 도 '}' 도 없다 (쉼표 유실 · 쓰레기)
    return out if ws(i) == n_ else None


def rec_read(p):
    """한 줄 기록 파일 → rec_parse 결과 (일반 파일이 아니거나 못 읽으면 None — 러너 rec5 의 [ -f ] 와 같다)."""
    try:
        return rec_parse(open(p, "rb").read()) if os.path.isfile(p) else None
    except OSError:
        return None


def rec_s(x, k):
    """한 줄 기록의 문자열 값 (원문) · 없거나 꼴이 다르면 None (러너 rf … s)."""
    v = (x or {}).get(k)
    return v[1] if v and v[0] == "s" else None


def rec_i(x, k):
    """한 줄 기록의 정수 값 · 없거나 꼴이 다르면 None (러너 rf … i)."""
    v = (x or {}).get(k)
    return v[1] if v and v[0] == "i" else None


def rec_text(v):
    """원문 (latin-1 1:1) → 사람이 읽을 글 (UTF-8 로 풀고 JSON 이스케이프를 푼다 · 못 풀면 원문) — 보고용이다 (판정 · 비교에는 원문을 쓴다)."""
    if v is None:
        return None
    try:
        return json.loads('"' + v.encode("latin-1").decode("utf-8", "replace") + '"')
    except ValueError:
        return v


def start_problem(job_dir, d, stage):
    """시도 폴더의 attempt.start 가 이 폴더의 것인가 → 사유 | None (러너 start_id 와 같은 순서 · Codex EO P1 Q-EO-2b):
    REC1 · 잡 = 이 묶음 · stage 'a5' · 변형 = 이 단의 것 · run_id 꼴 · t_start 정수. run_id 를 이어 대조하기 전에 본다."""
    x = rec_read(os.path.join(d, "attempt.start"))
    if x is None:
        return "start_form"
    if rec_s(x, "job") != job_dir:
        return "start_job"
    if rec_s(x, "stage") != "a5":
        return "start_stage"
    v = rec_s(x, "attempt")
    if v not in VARIANTS.get(stage, ()):
        return f"start_variant_{v or 'none'}"
    if not (rec_s(x, "run_id") and RUN_ID_ASCII.fullmatch(rec_s(x, "run_id"))):
        return "start_run_id"
    if rec_i(x, "t_start") is None:
        return "start_t"
    return None


def end_problem(d):
    """끝난 시도 폴더 → None 또는 사유 — 끝 기록 (attempt.json) 의 run_id · t_start = 시작 기록 (attempt.start) (러너 end_id 와 같다 · Codex EP 조건부 Q-EP-4c).
    ⚠ 못 하는 것: attempt.json 은 REC1 이 아니다 — 러너는 첫 'run_id' · 't_start' 를 grep 으로, 여기는 json 으로 읽는다 (러너가 쓴 꼴에서만 같다 · 같은 키 두 번이면 여기가 더 엄하다)."""
    s0 = rec_read(os.path.join(d, "attempt.start"))
    if s0 is None:
        return "end_start_form"
    a = _jread(os.path.join(d, "attempt.json"))
    rid, t0 = a.get("run_id"), a.get("t_start")
    if not (isinstance(rid, str) and rid and rid == rec_s(s0, "run_id")):
        return "end_run_id"
    if not (isinstance(t0, int) and not isinstance(t0, bool) and t0 == rec_i(s0, "t_start")):
        return "end_t_start"
    return None


KILLED_STR = ("job", "rung", "run_id", "wall_s", "sched_job_id", "cancel_utc", "reason", "osz_rows", "recorded_utc")              # killed.json 문자열 칸 (러너가 쓰는 것)
RECEIPT_STR = ("job", "rung", "run_id", "sched_job_id", "cancel_utc", "reason", "wall_s", "oszicar", "recorded_utc")            # infra_abort.json 문자열 칸


def dims_match(dims, sd):
    """c 단 OUTCAR NKPTS · NBANDS · ENCUT (outcar_dims) 가 시작 WAVECAR 머리 (_head_dims) 와 같은가 — 러너 stat5 · killed5 의 out_num · enc_eq 와 같은 기준 (ENCUT ±0.05 · 숫자 꼴만)."""
    try:
        return (sd is not None and dims.get("NKPTS") == sd[0] and dims.get("NBANDS") == sd[1]
                and all(re.fullmatch(r"[0-9]+(\.[0-9]+)?", str(x)) for x in (dims.get("ENCUT"), sd[2])) and abs(float(dims["ENCUT"]) - float(sd[2])) < 0.05)
    except (TypeError, ValueError):
        return False


def killed_problems(job, attdir, stage, osz, n, registry=None, src_head=None):
    """끊긴 시도 (killed.json · attempt.json 없음 · 행 판독 사유 없음 · 완전한 행 ≥ 1 · 설정 에코 맞음 · attempt.start 가 이 폴더의 것) → (상태, 사유) | None —
    러너 killed5 와 같은 순서 (Codex EN P0 · P1 · EO P1): ① c1 · c2 재시작 원문 — OUTCAR ISTART 1 job · ICHARG 0 charge · 'WAVECAR not read' 없음 ·
    등록부 문구 · NKPTS·NBANDS·ENCUT = 시작점 머리 — 아니면 RESTART_NOT_HONOURED ② killed.json — 한 줄 기록 문법 (REC1) 전체 · 칸 · 잡 · 단 ·
    run_id = attempt.start · osz_rows = 지금 완전한 행 수 · wall_s 초 · recorded_s ≥ 시작 시각 — 아니면 KILLED_RECORD_MISMATCH.
    행 머리 · 행 손상은 그 앞 (check_attempt5 · 러너 gate5) 에서 끝 기록과 관계없이 본다 (Codex EO P0).
    ⚠ 못 하는 것: 끝 기록이 없어 c 단의 시작 · 끝 WAVECAR sha 셋 (WAVECAR.info) 은 못 본다 — 시작 복사본 sha 는 러너가 띄우기 전에 확인했지만 그 확인의 기록은 없다."""
    if stage in ("c1", "c2"):
        out_text = R2._read(os.path.join(attdir, "OUTCAR")) or ""
        ev = R2.restart_evidence(attdir, out_text)
        if not (ev["istart"] == "1" and ev["icharg"] == "0"):
            return "RESTART_NOT_HONOURED", f"끊긴 {stage} OUTCAR ISTART {ev['istart']} · ICHARG {ev['icharg']} — 시작 WAVECAR 를 읽지 않았다 → 1저자 (자동 채택 없음)"
        if ev["not_read_phrase"]:
            return "RESTART_NOT_HONOURED", f"끊긴 {stage} 원문에 'WAVECAR not read' → 1저자 (자동 채택 없음)"
        rx = (registry or {}).get("restart_read_regex") or ""
        rxbad = R2.restart_regex_problems(rx) if rx else ["등록부 재시작 문구 없음"]
        if rxbad or re.search(rx, ev["text"], re.M) is None:
            return "RESTART_NOT_HONOURED", (f"등록부 재시작 regex 형식 {rxbad}" if rxbad else f"등록부 재시작 문구 /{rx}/ 가 끊긴 {stage} OUTCAR·stdout.log 원문에 없다") \
                + " → 1저자 (자동 채택 없음)"
        dims, sd = R2.outcar_dims(out_text), _head_dims(src_head)
        if not dims_match(dims, sd):
            return "RESTART_NOT_HONOURED", f"끊긴 {stage} OUTCAR NKPTS·NBANDS·ENCUT {dims} ≠ 시작점 머리 {sd} → 1저자 (자동 채택 없음)"
    k = rec_read(os.path.join(attdir, "killed.json"))
    if k is None:
        return "KILLED_RECORD_MISMATCH", "killed.json 이 한 줄 기록 문법 (REC1) 밖이다 — 잘렸거나 손댄 기록 (쉼표 유실 · 날것 제어문자 · 같은 키 두 번 …) → 1저자"
    for f_ in KILLED_STR:
        if rec_s(k, f_) is None:
            return "KILLED_RECORD_MISMATCH", f"killed.json 칸 {f_} 가 없거나 문자열이 아니다"
    if rec_i(k, "recorded_s") is None:
        return "KILLED_RECORD_MISMATCH", "killed.json 칸 recorded_s 가 없거나 정수가 아니다"
    for f_ in ("sched_job_id", "cancel_utc", "reason"):
        if _blank(rec_s(k, f_)):
            return "KILLED_RECORD_MISMATCH", f"killed.json 칸 {f_} 가 비었다 · 빈칸뿐이다 — 기록 명령이 요구한 칸 (Codex EP 조건부 · EQ P1)"
    s0 = rec_read(os.path.join(attdir, "attempt.start"))
    if rec_s(k, "job") != job["dir"] or rec_s(k, "rung") != stage:
        return "KILLED_RECORD_MISMATCH", f"killed.json 잡 {rec_s(k, 'job')!r} · 단 {rec_s(k, 'rung')!r} ≠ 이 시도 ({job['dir']} · {stage})"
    if rec_s(k, "run_id") != rec_s(s0, "run_id"):
        return "KILLED_RECORD_MISMATCH", f"killed.json run_id {rec_s(k, 'run_id')!r} ≠ attempt.start {rec_s(s0, 'run_id')!r}"
    if rec_s(k, "osz_rows") != str(n):
        return "KILLED_RECORD_MISMATCH", f"killed.json osz_rows {rec_s(k, 'osz_rows')!r} ≠ OSZICAR 완전한 전자 반복행 {n}"
    if not SECS_RE.fullmatch(rec_s(k, "wall_s")):
        return "KILLED_RECORD_MISMATCH", f"killed.json wall_s {rec_s(k, 'wall_s')!r} (10진 정수 초 · 선행 0 없음 · 9 자리 이하)"
    if not (rec_i(s0, "t_start") is not None and rec_i(k, "recorded_s") >= rec_i(s0, "t_start")):
        return "KILLED_RECORD_MISMATCH", f"killed.json recorded_s {rec_i(k, 'recorded_s')!r} < attempt.start t_start {rec_i(s0, 't_start')!r}"
    return None


def check_attempt5(job, pkgdir, attdir, stage, registry=None, src_sha=None, src_head=None):
    """a5 시도 하나 → 상태 dict. 순서 (러너 gate5 · stat5 와 같다): 실행 기록 결박 → 입력 무결성 → POTCAR 기록 → 판정 (행 수) →
    **행 0 이면 SCF_UNVERIFIED** (모순 · 재시작 확인보다 먼저 — 리뷰 P2(f) · 환경 등급 모순은 conflicts 로 남긴다) → 있는 증거의 모순 (설정 · D3 · POTCAR · 버전) →
    c 단 재시작 (sha 셋 · 문구 · 시작 WAVECAR 머리 = c 단 OUTCAR NKPTS·NBANDS·ENCUT — 리뷰 P3) → 판정 상태 → 완결성.
    판정 · A5 의 WAVECAR 기록 · echo5 (러너 설정 관문) 는 모순이 있어도 적어 둔다 — 러너가 본 것을 기록으로 다시 내기 위해 (리뷰 P2(e)).
    c1 · c2 는 src_sha · src_head (러너가 기록한 시작점 run/start_point.json — 없으면 규칙으로 낸 시작점) 를 받는다. A5 의 재시작은 정보 (자격이 아니다)."""
    r = {"dir": os.path.relpath(attdir, os.path.dirname(os.path.dirname(attdir))), "a5_stage": stage}

    def done(status, why=None, **kw):
        r["status"] = status
        if why:
            r["why"] = why
        r.update(kw)
        return r
    if not os.path.isdir(attdir):
        return done("MISSING")
    r["env"] = R2.env_evidence(attdir, False)
    r["killed"] = os.path.isfile(os.path.join(attdir, "killed.json")); r["started"] = os.path.isfile(os.path.join(attdir, "attempt.start"))
    osz = R2._read_raw(os.path.join(attdir, "OSZICAR"))
    n_rows, why_rows = row_gate(osz, stage)
    r["osz_rows"] = n_rows                                                   # 완전한 전자 반복행 수 (러너 row_scan 과 같은 기준 · Codex EO P0)
    r["row_scan"] = {"complete_rows": n_rows, "why": why_rows or "-"}
    r["times"] = _times(attdir)
    if r["started"]:
        sp_ = start_problem(job["dir"], attdir, stage)
        if sp_:
            return done("ATTEMPT_MISMATCH", f"attempt.start 가 이 폴더 ({job['dir']} · {stage}) 의 시도가 아니다 ({sp_}) — 러너도 아무것도 띄우지 않고 멈춘다 "
                                            "(종료 2 · Codex EO P1 Q-EO-2b)")
    if not os.path.isfile(os.path.join(attdir, "attempt.json")):
        if why_rows:                                                         # 끝 기록이 없어도 행 손상 · 남의 머리는 먼저 본다 (러너 gate5 · 종료 8 · Codex EO P0)
            return done("SCF_UNVERIFIED", f"끝 기록 없는 {stage} 의 OSZICAR 행 판독 {why_rows} (완전한 행 {n_rows}) — 잘린 첫 행 · 손상 · 남의 머리 → 1저자 "
                                          "(자동 채택 없음 · Codex EO P0)")
        if r["killed"]:
            r["echo5"] = dict(zip(("missing", "bad"), echo5(R2._read(os.path.join(attdir, "OUTCAR")) or "",
                                                              rec_s(rec_read(os.path.join(attdir, "attempt.start")), "attempt"))))
            if r["osz_rows"] >= 1 and not (r["echo5"].get("missing") or r["echo5"].get("bad")):
                kp = killed_problems(job, attdir, stage, osz, r["osz_rows"], registry, src_head)
                if kp:
                    return done(kp[0], kp[1])
        return done("INCOMPLETE_ATTEMPT", "attempt.json 없음 — " + (
            "전자 스텝 뒤 끊긴 시도 (killed.json — 그 단 소모 · 값 없음)" if r["killed"] else
            "VASP 를 띄웠는데 끝 기록이 없다 (attempt.start 만 — 벽시계 미상)" if r["started"] else "VASP 를 띄우기 전에 멈춘 시도 (준비만)"))
    try:
        a = json.load(open(os.path.join(attdir, "attempt.json"), encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return done("ATTEMPT_MISMATCH", f"attempt.json 읽기 실패 {e}")
    var = a.get("attempt") if isinstance(a, dict) else None
    if not isinstance(a, dict) or a.get("job") != job["dir"] or var not in VARIANTS[stage] or a.get("stage") != "a5" or not isinstance(a.get("sha256"), dict):
        return done("ATTEMPT_MISMATCH", "attempt.json 의 잡·단·변형·sha 형식")
    r["variant"] = var
    rid, t0, t1, el, rc = a.get("run_id"), a.get("t_start"), a.get("t_end"), a.get("elapsed_s"), a.get("rc")
    isint = lambda x: isinstance(x, int) and not isinstance(x, bool)
    if not (isinstance(rid, str) and V.RUN_ID_RE.match(rid)) or not (isint(t0) and isint(t1) and isint(el) and el >= 0) or not isint(rc):
        return done("ATTEMPT_MISMATCH", f"실행 기록 형식 (run_id {rid!r} · 경과 {el!r} · rc {rc!r})")
    ep_ = end_problem(attdir)
    if ep_:
        return done("ATTEMPT_MISMATCH", f"끝 기록 (attempt.json) 이 이 시작 기록의 것이 아니다 ({ep_} · run_id · t_start) — 러너 종료 2 (Codex EP 조건부)")
    for f in ("INCAR", "POSCAR", "KPOINTS", "OUTCAR", "OSZICAR", "WAVECAR.info", "stdout.log", "POTCAR.titel", "POTCAR.species.sha256", "attempt.start"):
        p = os.path.join(attdir, f)
        if (a["sha256"].get(f) or "") != (_sha(p) if os.path.isfile(p) else ""):
            return done("ATTEMPT_MISMATCH", f"{f} 가 실행 기록(attempt.json)과 다르다")
    r.update({"run_id": rid, "rc": rc, "wall_s": el, "attempt_json_sha256": _sha(os.path.join(attdir, "attempt.json")),
              "outcar_sha256": str(a["sha256"].get("OUTCAR") or "")})
    for f in ("POSCAR", "KPOINTS"):
        if _sha(os.path.join(attdir, f)) != job["files_sha256"][f]:
            return done("INPUT_MODIFIED", f)
    ours, e0 = V.parse_incar_strict(open(os.path.join(pkgdir, "jobs", job["dir"], INCAR_OF[var]), encoding="utf-8").read())
    incar_text = open(os.path.join(attdir, "INCAR"), encoding="utf-8", errors="replace").read()
    ran, e1 = V.parse_incar_strict(incar_text)
    extra = {k: v for k, v in ran.items() if k not in ours}
    badperf = [k for k, v in extra.items() if k not in V.PERF_TAGS or not V.perf_value_ok(k, v)]
    diff = [k for k in ours if ran.get(k) != ours[k]]
    if e0 or e1 or badperf or diff:
        return done("INPUT_MODIFIED", f"INCAR 문법 {e1[:3]} · 다른 태그 {diff} · 허용 밖 추가 {badperf}")
    out_text = R2._read(os.path.join(attdir, "OUTCAR")) or ""
    o = V.parse_outcar(out_text) if out_text else None
    if o:
        o["_body"] = V._strip_incar_echo(out_text)[0]
        r.update({k: v for k, v in o.items() if k not in ("settings", "_body")}); r["settings"] = o["settings"]
    tp, sp_, spp = (os.path.join(attdir, f) for f in ("POTCAR.titel", "POTCAR.sha256", "POTCAR.species.sha256"))
    if not all(os.path.isfile(x) for x in (tp, sp_, spp)):
        return done("POTCAR_UNVERIFIED", "POTCAR 기록 (titel · sha256 · species.sha256) 결측")
    psha = open(sp_, encoding="utf-8").read().strip().lower()
    sps = [ln.split() for ln in open(spp, encoding="utf-8").read().splitlines() if ln.strip()]
    if not V.HEX64.match(psha) or psha != str(a["sha256"].get("POTCAR", "")).lower() \
            or [x[0] for x in sps] != job["potcar_spec"] or any(len(x) != 2 or not V.HEX64.match(x[1].lower()) for x in sps):
        return done("POTCAR_UNVERIFIED", "POTCAR sha 형식·순서·실행 기록 불일치")
    r["potcar_species_sha256"] = {x[0]: x[1].lower() for x in sps}; r["potcar_sha256"] = psha
    conflicts = []
    titel, zv = V.parse_titel(open(tp, encoding="utf-8", errors="replace").read())
    exp_t = [registry["titel"][p] for p in job["potcar_spec"]] if registry else job["pp_expected_titel"]
    if titel != exp_t or [round(x, 3) for x in zv] != [round(x, 3) for x in job["zval_expected"]]:
        conflicts.append(("POTCAR_MISMATCH", f"POTCAR.titel {titel} · ZVAL {zv} (기대 {exp_t})"))
    ot = o["outcar_titel"] if o else []
    if ot and ot != titel and not (len(ot) < len(titel) and titel[:len(ot)] == ot):
        conflicts.append(("POTCAR_MISMATCH", f"OUTCAR TITEL {ot} ≠ POTCAR.titel {titel}"))
    if registry:
        if any(registry["species_sha256"].get(k) != v for k, v in r["potcar_species_sha256"].items()):
            conflicts.append(("POTCAR_MISMATCH", "봉인 등록부의 종별 sha 와 다르다"))
        if o and o["version"] and o["version"] != registry["vasp_version"]:
            conflicts.append(("VERSION_MISMATCH", f"VASP {o['version']!r} ≠ 등록부"))
    missing, bad, src = audit5(o, job, var) if o else ([], [], {"echo5": dict(zip(("missing", "bad"), echo5("", var)))})
    r["echo5"] = src.get("echo5")
    if bad:
        conflicts.append(("SETTINGS_MISMATCH", "; ".join(bad)))
    ref = fin(job.get("d3_2body_eV_ref"))
    if o and ref is not None and o["Edisp_eV"] is not None and abs(o["Edisp_eV"] - ref) > V.D3_REL_TOL * abs(ref):
        conflicts.append(("D3_MISMATCH", f"Edisp {o['Edisp_eV']:.4f} vs ref {ref:.4f} eV (>1 %)"))
    if stage != "c2":
        r["history_max"] = hist_max(out_text)
        r["rmsc_jump_steps"] = rms_jumps(osz, stage)[:20]
    if stage != "A5":
        r["far"] = R2.far_diag(out_text, job["area_A2"])
    st, n, de, dp, why = judge5(osz, *(R2._read_raw(os.path.join(attdir, f)) for f in ("OUTCAR", "INCAR")), rc, stage)
    r["judge"] = {"status": st, "n_elec_steps": n, "dE": de, "d_eps": dp, "why": why}
    w = _wavecar_info(attdir)
    ev = R2.restart_evidence(attdir, out_text)
    rx = (registry or {}).get("restart_read_regex") or ""
    rxbad = R2.restart_regex_problems(rx) if rx else ["등록부 재시작 문구 없음"]
    pos = (not rxbad and re.search(rx, ev["text"], re.M) is not None)
    if stage == "A5":
        r["wavecar"] = {k: w.get(k) for k in ("sha256", "size", "head", "outcar")} if w else None
        r["outcar_dims"] = R2.outcar_dims(out_text)
        if var == "A5c":
            rs = (w or {}).get("restart") if isinstance((w or {}).get("restart"), dict) else {}
            ok_ = (V.HEX64.match(str(rs.get("src_sha256", ""))) is not None and rs.get("src_sha256") == rs.get("copied_sha256") == src_sha
                   and ev["istart"] == "1" and ev["icharg"] == "0" and not ev["not_read_phrase"] and pos)
            r["restart_start"] = {"record": rs or None, "w0_sha256": src_sha, "outcar_istart": ev["istart"], "outcar_icharg": ev["icharg"],
                                  "not_read_phrase": ev["not_read_phrase"], "positive_regex_match": pos, "honoured": bool(ok_),
                                  "⛔": "정보 — A5 자격이 아니다 (끝 WAVECAR 는 LWAVE T 로 새로 써진다 · 끝 sha 를 보지 않는다)"}
    if why_rows:                                                             # 행 손상 · 남의 머리 — 행 0 판정보다 먼저 (러너 gate5 와 같은 순서 · 종료 8 · Codex EO P0)
        kw = {"conflicts": [f"{s_}: {w_}" for s_, w_ in conflicts]} if conflicts else {}
        return done("SCF_UNVERIFIED", f"OSZICAR 행 판독 {why_rows} (완전한 행 {n}) — 손상 · 남의 머리 → 1저자 (자동 채택 없음 · Codex EO P0)", **kw)
    if not n:
        kw = {"conflicts": [f"{s_}: {w_}" for s_, w_ in conflicts]} if conflicts else {}
        return done("SCF_UNVERIFIED", f"판정 계약 {why} (전자 반복행 0) — 0 스텝 · 재시작 · 설정 확인 전 (리뷰 P2(f) · 인프라 중단 경로)", **kw)
    if conflicts:
        return done(conflicts[0][0], conflicts[0][1], conflicts=[f"{s_}: {w_}" for s_, w_ in conflicts])
    if stage != "A5":
        dims, sd = R2.outcar_dims(out_text), _head_dims(src_head)
        r["restart"] = {"record": w, "outcar_istart": ev["istart"], "outcar_icharg": ev["icharg"], "not_read_phrase": ev["not_read_phrase"],
                        "expected_src_sha256": src_sha, "expected_src_head": src_head, "outcar_dims": dims, "positive_regex": rx or None, "positive_regex_match": pos}
        if not (isinstance(w, dict) and w.get("honoured") == 1 and w.get("istart") == "1" and w.get("icharg") == "0" and w.get("not_read_phrase") == 0
                and ev["istart"] == "1" and ev["icharg"] == "0" and not ev["not_read_phrase"]
                and V.HEX64.match(str(w.get("src_sha256", ""))) and w.get("src_sha256") == w.get("copied_sha256") == w.get("end_sha256")):
            return done("RESTART_NOT_HONOURED", f"{stage} 가 시작 WAVECAR 를 읽었다고 확인할 수 없다 (OUTCAR ISTART {ev['istart']} · ICHARG {ev['icharg']} · "
                        f"'WAVECAR not read' {ev['not_read_phrase']} · sha 셋) — 자동 채택 없음 · 1저자 검토")
        if not (src_sha and V.HEX64.match(src_sha) and w.get("src_sha256") == src_sha):
            return done("RESTART_NOT_HONOURED", f"{stage} 원본이 정해진 시작 WAVECAR 가 아니다 (기대 {src_sha or '없음'} · 기록 {w.get('src_sha256')}) — 자동 채택 없음 · 1저자 검토")
        dims_ok = dims_match(dims, sd)
        if not dims_ok:
            return done("RESTART_NOT_HONOURED", f"{stage} OUTCAR NKPTS·NBANDS·ENCUT {dims} ≠ 시작 WAVECAR 머리 {sd} — 재시작이 온전하지 않다 (병렬 배치가 달라 띠 수가 바뀌었나 ·"
                        " 외주 2차와 같은 64 랭크 · KPAR 2 · NCORE 4) — 자동 채택 없음 · 1저자 검토")
        if not pos:
            return done("RESTART_NOT_HONOURED", (f"등록부 재시작 regex 형식 {rxbad}" if rxbad else f"등록부 재시작 문구 /{rx}/ 가 {stage} OUTCAR·stdout.log 원문에 없다")
                        + " — 자동 채택 없음 · 1저자 검토")
    r["settings_sources"] = src
    if st != "OK":
        if stage in ("c1", "c2") and st == "SCF_NOT_CONVERGED":
            sec, why_s = secondary_numbers(osz, stage)
            r["secondary"] = sec if sec else {"refused": why_s}
            c = completeness5(o, missing, titel, job)
            r["completeness"] = "OK" if c[0] == "OK" else f"{c[0]}: {c[1]}"
        return done(st, f"판정 계약 {why} (행 {n} · dE {de} · d eps {dp})")
    c = completeness5(o, missing, titel, job)
    if c[0] != "OK":
        return done(c[0], c[1])
    r["completeness"] = "OK"
    return done("OK")


# ───────────────────────── 반송 검사 (사다리 전체) ─────────────────────────
def check_w0(run, meta):
    """run/w0_check.json → ⓪ 기록 검사. 러너가 적은 'verified' 와 기록 값 (sha · 크기 · 머리) 로 다시 낸 판정이 같아야 한다."""
    w0 = meta["w0"]
    p = os.path.join(run, "w0_check.json")
    if not os.path.isfile(p):
        return {"status": "W0_RECORD_MISSING", "verified": False}
    try:
        rec = json.load(open(p, encoding="utf-8"))
    except ValueError as e:
        return {"status": "W0_RECORD_MISMATCH", "why": f"w0_check.json 읽기 실패 {e}", "verified": False}
    if not isinstance(rec, dict):
        return {"status": "W0_RECORD_MISMATCH", "why": "w0_check.json 형식", "verified": False}
    hd = str(rec.get("head", "")).split()
    try:
        head_ok = len(hd) >= 6 and hd[3] == w0["NKPTS"] and hd[4] == w0["NBANDS"] and abs(float(hd[5]) - float(w0["ENCUT"])) < 0.05
    except ValueError:
        head_ok = False
    re_v = rec.get("path") != "none" and rec.get("sha256") == w0["sha256"] and str(rec.get("size")) == str(w0["size"]) and head_ok
    exp_ok = rec.get("expect") == {"sha256": w0["sha256"], "size": str(w0["size"]), "NKPTS": w0["NKPTS"], "NBANDS": w0["NBANDS"], "ENCUT": w0["ENCUT"]}
    claimed = rec.get("verified") == 1
    out = {"record": rec, "verified": bool(re_v and claimed and exp_ok), "verified_recomputed": bool(re_v), "verified_claimed": claimed}
    if not exp_ok:
        return {**out, "status": "W0_RECORD_MISMATCH", "why": "기록의 기대값이 묶음과 다르다", "verified": False}
    if claimed != re_v:
        return {**out, "status": "W0_RECORD_MISMATCH", "why": f"러너 판정 {claimed} ≠ 기록 값으로 다시 낸 판정 {re_v}", "verified": False}
    return {**out, "status": "OK"}


def load_start_point(run, job):
    """run/start_point.json (러너가 첫 c 단을 띄울 때 한 번 쓴 시작점 — 리뷰 P0-2(b)) → (기록, 형식 오류). 없으면 (None, None)."""
    p = os.path.join(run, "start_point.json")
    if not os.path.lexists(p):
        return None, None
    sp = _jread(p)
    if not sp:
        return None, "start_point.json 을 읽지 못했다 (형식)"
    if sp.get("from") not in ("A5", "W0") or not V.HEX64.match(str(sp.get("sha256", ""))) or _head_dims(sp.get("head")) is None:
        return None, f"start_point.json 형식 (from {sp.get('from')!r} · sha256 · head)"
    if sp["from"] == "A5" and sp.get("path") != f"run/{job['dir']}_A5/WAVECAR":
        return None, f"A5 시작점 경로 {sp.get('path')!r}"
    return sp, None


def load_final(run):
    """run/final.json (러너의 끝 기록) → (기록, 형식 오류). 없으면 (None, None). 끝 기록은 판정을 **더 보수 쪽으로만** 바꾼다 (OK 를 만들지 않는다)."""
    p = os.path.join(run, "final.json")
    if not os.path.lexists(p):
        return None, None
    x = rec_read(p)                                       # 러너도 REC1 로 읽는다 (다시 돌릴 때 code · Codex EO P1)
    if x is None or rec_i(x, "code") not in (0, 1, 5, 6, 8) or any(rec_s(x, k) is None for k in ("state", "why", "attempts")):
        return None, "final.json 형식 (한 줄 기록 · code 0 · 1 · 5 · 6 · 8 · state · why · attempts)"
    return {"code": rec_i(x, "code"), "state": rec_text(rec_s(x, "state")), "why": rec_text(rec_s(x, "why")), "attempts": rec_s(x, "attempts"),
            "written_s": rec_i(x, "written_s")}, None


def order_violations(seq):
    """[(꼬리표, times)] — 사다리 순서 (A5 중단 기록 k 순 → run/ A5 → c1 중단 → c1 → c2 중단 → c2) → 위반 목록 (리뷰 P0-2(a)).
    시도마다 시작 ≥ 앞 시도의 끝 (attempt.json t_end · 끊김 · 중단 기록 시각 중 늦은 것) · 끝 ≥ 시작 · 끝을 모르는 시도 뒤에 시도가 있으면 위반.
    ⚠ 못 하는 것: 시계는 업체 노드의 date +%s 다 — 노드 사이 시계가 어긋나면 거짓 위반이 날 수 있다 (거짓 통과 쪽은 아니다 · 1저자 검토로 간다)."""
    viol, prev_end, prev_tag = [], None, None
    for tag, tm in seq:
        t0 = tm.get("start")
        if t0 is None:
            viol.append(f"{tag} 시작 시각이 없다 — 순서를 확인할 수 없다")
            prev_end, prev_tag = None, tag
            continue
        if prev_tag is not None:
            if prev_end is None:
                viol.append(f"{prev_tag} 의 끝을 모르는데 뒤에 {tag} 가 있다")
            elif t0 < prev_end:
                viol.append(f"{tag} 시작 {t0} < 앞 시도 {prev_tag} 끝 {prev_end} — 단 순서가 어긋났다")
        ends = [x for x in (tm.get("end"), tm.get("recorded")) if x is not None]
        end = max(ends) if ends else None
        if end is not None and end < t0:
            viol.append(f"{tag} 끝 {end} < 시작 {t0}")
        prev_end, prev_tag = end, tag
    return viol


def a5_class(x):
    """검사 기록 → (러너 갈래, 검사기만 본 실패 | None) — 러너 gate5 가 기록으로 냈을 갈래를 다시 낸다 (개정 5 해석 1 · 사용자 2026-11-20).
    러너 갈래: MISSING · PREP_ONLY · WAIT (끝 기록 없음) · ZERO (행 0) · REVIEW (러너가 멈췄어야 할 것 — SCF 미확인 · 재시작 미이행 · 설정 에코) ·
    BLOCKED (결박 · 무결성) · OK · NEXT (SCF_NOT_CONVERGED · 행 ≥ 1 실행 실패 · 행 ≥ 1 끊김 기록).
    검사기만 본 실패 = 러너가 못 보는 것 (설정 · D3 · POTCAR 등록부 · 완결성 …) — 러너는 갈래대로 이어 갔을 수 있다 (그래도 자동 채택은 없다)."""
    s = x.get("status")
    if s == "MISSING":
        return "MISSING", None
    if s in BLOCKING:
        return "BLOCKED", None
    if (x.get("row_scan") or {}).get("why", "-") != "-":
        return "REVIEW", None                  # 행 손상 (완전한 행 0 + 행꼴 조각 · 줄바꿈 있는 덜 쓴 행) · 남의 머리 — 러너 gate5 도 끝 기록과 관계없이 멈춤 8 (Codex EO P0)
    if s == "INCOMPLETE_ATTEMPT":
        if x.get("killed"):
            e = x.get("echo5") or {}
            if (x.get("osz_rows") or 0) < 1 or e.get("missing") or e.get("bad"):
                return "REVIEW", None
            return "NEXT", None
        return ("WAIT" if x.get("started") else "PREP_ONLY"), None
    if x.get("killed") and s in KILLED_PROBLEMS:
        return "REVIEW", None                  # 끊긴 시도의 원문 · 기록 모순 — 러너 gate5 도 멈춤 8 (Codex EN P0 · P1)
    j = x.get("judge") or {}
    if not j:
        return "BLOCKED", None
    if not j.get("n_elec_steps"):
        return "ZERO", None
    e = x.get("echo5") or {}
    if e.get("missing") or e.get("bad") or s == "RESTART_NOT_HONOURED" or j.get("status") == "SCF_UNVERIFIED":
        return "REVIEW", None
    rv = "OK" if j.get("status") == "OK" else ("NEXT" if j.get("status") in ("SCF_NOT_CONVERGED", "RUN_FAILED") else "REVIEW")
    if s in ("OK", "SCF_NOT_CONVERGED", "RUN_FAILED"):
        return rv, None
    return rv, f"{s}: {x.get('why', '')}"[:240]


def abort_receipt_problem(job, d, stage):
    """run_aborted/<잡>_<단>_<k> 의 중단 영수증 (infra_abort.json — 러너 --infra-abort 가 한 줄로 쓰고 · --infra-wall 이 다시 쓴다) → 문제 | None —
    러너 receipt5 와 같은 순서 (Codex EN P1 · EO P1): 있어야 하고 · 한 줄 기록 문법 (REC1) 전체 · 칸 · 잡 · 단 = 폴더 · attempt.start 가 그 폴더의 시도 (start_problem) ·
    run_id = attempt.start · wall_s 는 초 또는 UNKNOWN · recorded_s ≥ 그 시도 시작 · 채운 기록 (wall_s_filled_utc · wall_s_filled_s) 은 둘 다 있거나 둘 다 없고,
    있으면 wall_s 가 초 · 채운 시각 ≥ recorded_s. 영수증이 빠지면 순서 · 상한 대조가 attempt.json 으로만 돌아 늦게 쓴 기록 · 영수증 시간을 못 잡는다 — 그래서 필수다."""
    p = os.path.join(d, "infra_abort.json")
    if not os.path.lexists(p):
        return "중단 영수증 (infra_abort.json) 이 없다 — run_aborted 의 시도는 러너 --infra-abort 영수증이 있어야 한다 (그 기록 시각 · 벽시계로 순서 · 상한을 본다)"
    x = rec_read(p)
    if x is None:
        return "중단 영수증 (infra_abort.json) 이 한 줄 기록 문법 (REC1) 밖이다 (쉼표 유실 · 날것 제어문자 · 같은 키 두 번 …)"
    for f_ in RECEIPT_STR:
        if rec_s(x, f_) is None:
            return f"중단 영수증 칸 {f_} 가 없거나 문자열이 아니다"
    if rec_i(x, "recorded_s") is None:
        return "중단 영수증 칸 recorded_s 가 없거나 정수가 아니다"
    for f_ in ("sched_job_id", "cancel_utc", "reason"):
        if _blank(rec_s(x, f_)):
            return f"중단 영수증 칸 {f_} 가 비었다 · 빈칸뿐이다 (receipt_blank_{f_}) — 기록 명령이 요구한 칸 (Codex EP 조건부 · EQ P1)"
    if rec_s(x, "job") != job["dir"] or rec_s(x, "rung") != stage:
        return f"중단 영수증 잡 {rec_s(x, 'job')!r} · 단 {rec_s(x, 'rung')!r} ≠ 폴더 ({job['dir']} · {stage})"
    # 그 폴더의 시작 기록 · 끝 기록 신원 · 봉인은 트리 관문 (rec_dir_problem — 모든 시도 폴더 · 러너 rec_dir5) 이 본다 (Codex EQ — 한 곳)
    s0 = rec_read(os.path.join(d, "attempt.start"))
    if rec_s(x, "run_id") != rec_s(s0, "run_id"):
        return f"중단 영수증 run_id {rec_s(x, 'run_id')!r} ≠ attempt.start {rec_s(s0, 'run_id')!r} (Codex EO P1)"
    w = rec_s(x, "wall_s")
    if not (w == "UNKNOWN" or SECS_RE.fullmatch(w)):
        return f"중단 영수증 wall_s {w!r} (10진 정수 초 또는 UNKNOWN)"
    if rec_i(x, "recorded_s") < rec_i(s0, "t_start"):
        return f"중단 영수증 기록 시각 {rec_i(x, 'recorded_s')} < 그 시도 시작 {rec_i(s0, 't_start')}"
    if "wall_s_filled_utc" in x or "wall_s_filled_s" in x:
        fs = rec_i(x, "wall_s_filled_s")
        if rec_s(x, "wall_s_filled_utc") is None or fs is None or not SECS_RE.fullmatch(w) or fs < rec_i(x, "recorded_s"):
            return "중단 영수증 채운 기록 (wall_s_filled_utc · wall_s_filled_s · 초 · 채운 시각 ≥ 기록 시각) 이 맞지 않는다"
    return None


def wall_of(d):
    """시도 폴더 → 벽시계 초 (int) · 'UNKNOWN' · None (기록을 읽을 수 없음) — 러너 wall_of 와 같은 출처 순서 (Codex EO P1 Q-EO-2c):
    보존 폴더 (run_aborted/) 는 그 중단 영수증만 (스케줄러 장부 값 · 장부 · 폴더 · run_id 대조는 ledger_problems) · 진행 폴더는 영수증을 보지 않고
    끊김 기록 (killed.json) → attempt.json elapsed_s → 미상 (Codex EP P1 — 진행 폴더에 섞인 남의 영수증으로 상한을 비켜 가지 못하게).
    ⚠ 못 하는 것: attempt.json 은 REC1 이 아니다 (sha 표가 든 객체) — elapsed_s 는 json 으로 읽고 러너는 grep 으로 읽는다 (러너가 %d 로 쓴 값에서만 같다)."""
    if os.path.basename(os.path.dirname(os.path.abspath(d))) == "run_aborted":       # 보존 폴더는 그 중단 영수증만 · 진행 폴더의 영수증은 시간 출처가 아니다 (Codex EP P1)
        w = rec_s(rec_read(os.path.join(d, "infra_abort.json")), "wall_s")
        return "UNKNOWN" if w == "UNKNOWN" else (int(w) if w is not None and SECS_RE.fullmatch(w) else None)
    p = os.path.join(d, "killed.json")
    if os.path.lexists(p):
        w = rec_s(rec_read(p), "wall_s")
        return int(w) if w is not None and SECS_RE.fullmatch(w) else None
    p = os.path.join(d, "attempt.json")
    if os.path.isfile(p):
        el = _jread(p).get("elapsed_s")
        return el if isinstance(el, int) and not isinstance(el, bool) and 0 <= el < 10 ** 12 else None
    return "UNKNOWN"


LEDGER_HEAD = "recorded_utc\tjob\trung\tsched_job_id\tcancel_utc\twall_s\treason\tdir"


STATUS_HEAD = "job\trung\tstage\trc\tstatus\tn_elec\tdE\tdeps\twhy\twall_s\trun_id"


def history_problems(job, base):
    """run/status.tsv (러너가 끝난 시도마다 한 줄 · 마지막 칸 run_id) 의 줄이 지금 · 보존 폴더의 끝난 시도 (attempt.json 있음 · attempt.start 의 run_id · 변형) 로
    설명되는가 → 문제 목록 (러너 hist5 와 같은 규칙 · Codex EP P1 Q-EP-4a — 부분 복구로 폴더 · 장부 · 시작점이 함께 빠져도 이력 줄이 남으면 잡는다).
    ⚠ 못 하는 것: status.tsv 까지 함께 지우거나 맞게 고친 부분 복구는 못 잡는다 (반송 안의 것끼리만 대조) · 끝난 시도에 이력 줄이 없는 것은 보지 않는다
    (러너가 끝 기록과 이력 줄 사이에 끊기는 틈 · 거짓 멈춤을 피하려고)."""
    J = job["dir"]
    p = os.path.join(base, "run", "status.tsv")
    if not os.path.lexists(p):
        return []
    if not os.path.isfile(p):
        return ["시도 이력 (run/status.tsv) 이 파일이 아니다"]
    raw = open(p, "rb").read()
    if not raw:
        return ["시도 이력 (run/status.tsv) 이 0 바이트다 (status_empty) — 머리 줄도 없다 · 머리만 있는 파일은 받는다 (Codex EQ P1)"]
    if b"\x00" in raw:
        return ["시도 이력 (run/status.tsv) 에 NUL 이 있다"]
    if not raw.endswith(b"\n"):
        return ["시도 이력 (run/status.tsv) 이 줄바꿈으로 끝나지 않는다 (status_no_final_newline) — 쓰다 끊긴 줄"]
    if not _u8(raw):
        return ["시도 이력 (run/status.tsv) 이 UTF-8 이 아니다 (utf8_status.tsv)"]
    cand = [f"run/{J}_{s}" for s in STAGES]
    try:
        cand += [f"run_aborted/{n}" for n in os.listdir(os.path.join(base, "run_aborted")) if re.fullmatch(re.escape(J) + r"_(A5|c1|c2)_[0-9]+", n)]
    except OSError:
        pass
    have = {}
    for c in cand:
        d = os.path.join(base, c)
        if os.path.isdir(d) and os.path.isfile(os.path.join(d, "attempt.json")):
            s0 = rec_read(os.path.join(d, "attempt.start"))
            av_ = tpl_parse(_readb(os.path.join(d, "attempt.json")), ATT1_TPL)
            have[(rec_s(s0, "run_id") or "") + "\t" + (rec_s(s0, "attempt") or "")] = str(av_[7]) if av_ else ""
    lines = raw.decode("latin-1").split("\n")
    if raw.endswith(b"\n"):
        lines.pop()
    seen = set()
    for i, ln in enumerate(lines):
        if i == 0:
            if ln != STATUS_HEAD:
                return ["시도 이력 (run/status.tsv) 머리 줄이 다르다 (run_id 칸 · Codex EP P1)"]
            continue
        f = ln.split("\t")
        if len(f) != 11 or f[0] != J:
            return [f"시도 이력 (run/status.tsv) {i} 째 줄 꼴 (칸 {len(f)} · 잡)"]
        k = f[10] + "\t" + f[1]
        if k not in have:
            return [f"시도 이력 (run/status.tsv) {i} 째 줄 ({f[1]} · run_id {f[10]!r} · {f[4]}) 의 시도가 지금 · 보존 폴더에 없다 — 부분 복구 · 손댄 기록 (Codex EP P1)"]
        if f[9] != have[k]:
            return [f"시도 이력 (run/status.tsv) {i} 째 줄 벽시계 {f[9]!r} ≠ 그 시도 끝 기록 elapsed_s {have[k]!r} (status_row_{i}_elapsed) — 합산 전에 (Codex ER Q-ER-3①)"]
        if k in seen:
            return [f"시도 이력 (run/status.tsv) {i} 째 줄 — 같은 시도가 두 번"]
        seen.add(k)
    return []


def ledger_problems(job, base):
    """장부 핵심 (_ledger_core) + 시도 이력 (history_problems) → 문제 목록 (러너 ledger5 = 이 둘 + abort_receipt_problem · 진행 폴더의 영수증은 트리 관문 rec_dir_problem)."""
    return _ledger_core(job, base) + history_problems(job, base)        # 진행 폴더의 영수증 (자리) · *.part (잔여) 는 트리 관문 (tree_problems · Codex EQ)


def _ledger_core(job, base):
    """중단 장부 (run/infra_aborts.tsv) ↔ 보존 폴더 (run_aborted/<잡>_<단>_<k>) 양방향 대조 → 문제 목록 (러너 ledger5 와 같은 규칙 · Codex EO P1 Q-EO-3):
    장부가 없으면 보존 폴더도 없어야 · 있으면 NUL 없음 · 줄바꿈으로 끝남 · 첫 줄 = 머리 · 줄마다 탭 8 칸 · 잡 · 단 · 폴더 = <잡>_<단>_<줄 번호> · wall_s 초 또는 UNKNOWN ·
    줄 수 ≤ 잡 전체 상한 · 장부 폴더 집합 = 보존 폴더 집합 · 영수증 wall_s = 장부 wall_s. (영수증 자체의 문제는 abort_receipt_problem 이 따로 낸다 — 러너 ledger5 는 둘을 한 번에 본다.)"""
    J = job["dir"]
    ab = os.path.join(base, "run_aborted")
    try:
        names = os.listdir(ab)
    except FileNotFoundError:
        names = []
    except OSError as e:
        return [f"보존 폴더 (run_aborted) 를 읽지 못했다 ({type(e).__name__})"]
    pat = re.compile(re.escape(J) + r"_(A5|c1|c2)_[0-9]+")
    folders = sorted(n for n in names if pat.fullmatch(n) and os.path.isdir(os.path.join(ab, n)))
    p = os.path.join(base, "run", "infra_aborts.tsv")
    if not os.path.lexists(p):
        return [f"중단 장부 (run/infra_aborts.tsv) 가 없는데 보존 폴더 {folders[0]} 가 있다 (Codex EO P1)"] if folders else []
    try:
        raw = open(p, "rb").read() if os.path.isfile(p) else None
    except OSError:
        raw = None
    if raw is None:
        return ["중단 장부 (run/infra_aborts.tsv) 가 파일이 아니거나 읽을 수 없다"]
    if b"\x00" in raw:
        return ["중단 장부에 NUL 이 있다"]
    if not raw.endswith(b"\n"):
        return ["중단 장부가 줄바꿈으로 끝나지 않는다 (잘린 장부)"]
    if not _u8(raw):
        return ["중단 장부가 UTF-8 이 아니다 (utf8_infra_aborts.tsv)"]
    lines = raw[:-1].decode("latin-1").split("\n")
    if lines[0] != LEDGER_HEAD:
        return ["중단 장부 머리 줄이 다르다"]
    rows, pr = {}, 0
    for i, ln in enumerate(lines[1:], 1):
        f = ln.split("\t")
        if len(f) != 8:
            return [f"중단 장부 {i} 째 줄 칸 수 {len(f)} ≠ 8"]
        if f[1] != J or f[2] not in STAGES:
            return [f"중단 장부 {i} 째 줄 잡 · 단 ({f[1]!r} · {f[2]!r})"]
        if STAGES.index(f[2]) + 1 < pr:
            return [f"중단 장부 {i} 째 줄 단 {f[2]} 이 앞 줄 단보다 앞이다 (ledger_row_{i}_rung_order) — 전역 번호순 A5 ≤ c1 ≤ c2 (같은 초의 맞바꿈 · Codex EQ P2)"]
        pr = STAGES.index(f[2]) + 1
        if f[7] != f"{J}_{f[2]}_{i}":
            return [f"중단 장부 {i} 째 줄 폴더 {f[7]!r} ≠ {J}_{f[2]}_{i} (줄 번호 = 폴더 번호)"]
        if not (f[5] == "UNKNOWN" or SECS_RE.fullmatch(f[5])):
            return [f"중단 장부 {i} 째 줄 wall_s {f[5]!r}"]
        if i > INFRA_MAX:
            return [f"중단 장부 줄 수 > 잡 전체 {INFRA_MAX} 회"]
        rows[f[7]] = f[5]
    if sorted(rows) != folders:
        only_l, only_f = sorted(set(rows) - set(folders)), sorted(set(folders) - set(rows))
        return [f"중단 장부 ↔ 보존 폴더가 다르다 — 장부에만 {only_l} · 폴더에만 {only_f} (부분 복구 · 손댄 기록 · Codex EO P1 Q-EO-3)"]
    out, prs, pt0 = [], 0, 0
    for n_, w in rows.items():
        ww = rec_s(rec_read(os.path.join(ab, n_, "infra_abort.json")), "wall_s")
        if ww is not None and ww != w:
            out.append(f"중단 장부 {n_} wall_s {w!r} ≠ 영수증 {ww!r} (Codex EO P1)")
        rs_, t0_ = rec_i(rec_read(os.path.join(ab, n_, "infra_abort.json")), "recorded_s"), rec_i(rec_read(os.path.join(ab, n_, "attempt.start")), "t_start")
        if rs_ is not None and t0_ is not None:
            if rs_ < prs or t0_ < pt0:
                out.append(f"중단 장부 {n_} 의 기록 시각 {rs_} · 시작 {t0_} 이 앞 줄 ({prs} · {pt0}) 보다 이르다 (ledger_time_order) — 장부 줄 순서 = 일어난 순서 (Codex EP P2)")
            prs, pt0 = rs_, t0_
    return out


def attempts_of(base, job):
    """반송 트리 → '경로=run_id …' (경로 바이트 순 · 빈칸으로 잇는다 · run_id 를 못 읽으면 '-') — 러너 att5 가 끝 기록 (final.json attempts) 에 묶는 것과 같다 (Codex EO P2)."""
    J = job["dir"]
    cand = [f"run/{J}_{s}" for s in STAGES]
    try:
        cand += [f"run_aborted/{n}" for n in os.listdir(os.path.join(base, "run_aborted")) if re.fullmatch(re.escape(J) + r"_(A5|c1|c2)_[0-9]+", n)]
    except OSError:
        pass
    out = []
    for p in sorted(c for c in cand if os.path.isdir(os.path.join(base, c))):
        out.append(f"{p}={rec_s(rec_read(os.path.join(base, p, 'attempt.start')), 'run_id') or '-'}")
    return " ".join(out)


def tpl_parse(raw, tpl):
    """한 줄 틀 기록 (attempt.json · w0_check.json — 러너 printf 그대로의 꼴) → 값 목록 (틀의 바이트 1 = 문자열 원문 · 바이트 2 = 정수) | None — 러너 tpl5 와 같은 규칙:
    한 줄 (+ 끝 줄바꿈 하나) · NUL 없음 · 틀 글자 그대로 · 문자열 = 따옴표 · 역슬래시 · 제어 바이트 (0x00–0x1F) 없음 · 정수 = 선행 0 없음 · 16 자리 이하 (잘린 JSON · 정수 칸의 소수 → None)."""
    if not isinstance(raw, (bytes, bytearray)) or b"\x00" in raw:
        return None
    lines = bytes(raw).split(b"\n")
    if raw.endswith(b"\n"):
        lines.pop()
    if len(lines) != 1:
        return None
    s, out, i = lines[0], [], 0
    L = len(s)
    for c in tpl.encode("latin-1"):
        if c == 1:
            if i >= L or s[i] != 0x22:
                return None
            j = i + 1
            while j < L and s[j] != 0x22:
                if s[j] == 0x5C or s[j] < 0x20:
                    return None
                j += 1
            if j >= L:
                return None
            out.append(s[i + 1:j].decode("latin-1")); i = j + 1
        elif c == 2:
            j = i
            while j < L and 0x30 <= s[j] <= 0x39:
                j += 1
            v = s[i:j]
            if not re.fullmatch(rb"0|[1-9][0-9]*", v) or len(v) > 16:
                return None
            out.append(int(v)); i = j
        else:
            if i >= L or s[i] != c:
                return None
            i += 1
    return out if i == L else None


def _u8(raw):
    """바이트 → UTF-8 로 온전한가 (러너 u8in · u8f 와 같은 판정 — selftest 탐침 대조)."""
    try:
        bytes(raw).decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


BLANK_ESC = re.compile(r"\\(?:[tnrf]|u00(?:0[9a-dA-D]|20))| ")     # 필수 칸 빈칸 판정에서 걷는 것 (러너 nbj 의 awk 정규식과 같다)


def _blank(v):
    """필수 칸 원문 (JSON 이스케이프 그대로) → 비었거나 빈칸 문자뿐인가 — 공백 · 빈칸 이스케이프 (\\t \\n \\r \\f · \\u0009–\\u000d · \\u0020) 를 걷고
    남는 글자가 없다 (러너 nbj 와 같은 규칙 · 쓸 때 러너 nbw 는 같은 여섯 문자 — 공백 · 탭 · LF · VT · FF · CR · Codex EQ P1). 원문의 날것 탭 · 줄바꿈은 REC1 이 이미 거부한다."""
    return v is None or BLANK_ESC.sub("", v) == ""


def _readb(p):
    try:
        return open(p, "rb").read()
    except OSError:
        return None


def att_problem(d, s0, vals):
    """끝난 시도의 attempt.json 값 (tpl_parse · ATT1_TPL) → 사유 | None — 신원 (run_id · t_start = attempt.start) · 봉인 (sha 표 = 지금 파일 · POTCAR 본문 빼고 열 개 · 러너 att_ok5)."""
    if vals[3] != rec_s(s0, "run_id"):
        return "end_run_id"
    if vals[5] != rec_i(s0, "t_start"):
        return "end_t_start"
    if vals[0] != rec_s(s0, "job"):                 # 끝 기록 신원 = 시작 기록 (잡 · 변형 · stage · Codex ER Q-ER-5)
        return "end_job"
    if vals[1] != rec_s(s0, "attempt"):
        return "end_attempt"
    if vals[2] != rec_s(s0, "stage"):
        return "end_stage"
    for f, k in zip(SEAL_ORDER, vals[11:]):
        if f == "POTCAR":
            continue
        p = os.path.join(d, f)
        if k != (_sha(p) if os.path.isfile(p) else ""):
            return f"seal_{f}"
    if _readb(os.path.join(d, "POTCAR.sha256")) != (vals[14] + "\n").encode("latin-1"):     # 끝 기록의 POTCAR 해시 = 반송된 POTCAR.sha256 (러너 att_ok5 와 같다 · Codex ER Q-ER-5)
        return "end_potcar_sha"
    return None


def killed_rec_problem(job_dir, d, stage, s0):
    """진행 폴더의 killed.json → 사유 | None — 문법 · 칸 · 빈칸 · 결속 (잡 · 단 · run_id · 초 · 기록 시각 ≥ 시작 · 러너 killed_rec5 · 그 시간을 쓰기 전에 · Codex EQ P0)."""
    k = rec_read(os.path.join(d, "killed.json"))
    if k is None:
        return "killed_json_form"
    for f_ in KILLED_STR:
        if rec_s(k, f_) is None:
            return f"killed_json_field_{f_}"
    if rec_i(k, "recorded_s") is None:
        return "killed_json_field_recorded_s"
    for f_ in ("sched_job_id", "cancel_utc", "reason"):
        if _blank(rec_s(k, f_)):
            return f"killed_json_blank_{f_}"
    if rec_s(k, "job") != job_dir or rec_s(k, "rung") != stage:
        return "killed_job_or_rung"
    if rec_s(k, "run_id") != rec_s(s0, "run_id"):
        return "killed_run_id"
    if not SECS_RE.fullmatch(rec_s(k, "wall_s")):
        return "killed_wall_s"
    t0 = rec_i(s0, "t_start")
    if t0 is None or rec_i(k, "recorded_s") < t0:
        return "killed_recorded_s"
    return None


def rec_dir_problem(job_dir, d, rel, stage):
    """시도 폴더 하나 → 사유 | None (러너 rec_dir5 와 같은 차례): 시작 기록 → UTF-8 (시작 · 끝 · 끊김 · 영수증) → 끝 기록 (틀 · 신원 · 봉인) →
    끊김 기록 (보존 폴더면 killed_in_aborted · 끝 기록과 함께면 end_and_killed · 문법 · 결속) → 진행 폴더의 영수증 (stray_receipt)."""
    if not os.path.isfile(os.path.join(d, "attempt.start")):
        return "no_start"
    sp_ = start_problem(job_dir, d, stage)
    if sp_:
        return sp_
    for f in ("attempt.start", "attempt.json", "killed.json", "infra_abort.json"):
        p = os.path.join(d, f)
        if os.path.isfile(p):
            raw_ = _readb(p)
            if raw_ is None or not _u8(raw_):
                return f"utf8_{f}"
    s0 = rec_read(os.path.join(d, "attempt.start"))
    if os.path.isfile(os.path.join(d, "attempt.json")):
        vals = tpl_parse(_readb(os.path.join(d, "attempt.json")), ATT1_TPL)
        if vals is None:
            return "att_form"
        ap_ = att_problem(d, s0, vals)
        if ap_:
            return ap_
    if os.path.isfile(os.path.join(d, "killed.json")):
        if rel.startswith("run_aborted/"):
            return "killed_in_aborted"
        if os.path.isfile(os.path.join(d, "attempt.json")):
            return "end_and_killed"
        kp_ = killed_rec_problem(job_dir, d, stage, s0)
        if kp_:
            return kp_
    if rel.startswith("run/") and os.path.isfile(os.path.join(d, "infra_abort.json")):
        return "stray_receipt"
    return None


def files_problem(job_dir, base):
    """run/ · run_aborted/ · 시도 폴더의 이름 → 사유 | None (러너 files5 와 같은 규칙): run/ = 시도 폴더 · 잠금 · 준비 폴더 (폴더 · 링크 아님) · 관리 기록 (파일 · 링크 아님) 만 ·
    run_aborted/ = <잡>_<단>_<k> 폴더만 · 시도 폴더 = 반송 허용 · 금지 이름 · VASP 표준 출력 (VASP_OUT) 의 파일만 — 잔여 *.part · 모르는 이름 · 링크 · 하위 폴더 → 멈춤."""
    isdir_ = lambda p: os.path.isdir(p) and not os.path.islink(p)
    isfile_ = lambda p: os.path.isfile(p) and not os.path.islink(p)
    run, ab = os.path.join(base, "run"), os.path.join(base, "run_aborted")
    dirs_ok = {f"{job_dir}_{s}" for s in STAGES} | {".a5.lock"} | {f".prep_{job_dir}_{s}" for s in STAGES}
    files_ok = {os.path.basename(m) for m in MGMT}
    for n in sorted(os.listdir(run)) if os.path.isdir(run) else []:
        p = os.path.join(run, n)
        if not ((n in dirs_ok and isdir_(p)) or (n in files_ok and isfile_(p))):
            return f"run_entry_{n}"
    abn = sorted(os.listdir(ab)) if os.path.isdir(ab) else []
    for n in abn:
        if not (re.fullmatch(re.escape(job_dir) + r"_(A5|c1|c2)_[1-9][0-9]*", n) and isdir_(os.path.join(ab, n))):
            return f"aborted_entry_{n}"
    names = set(RETURN_ALLOWED) | set(RETURN_FORBIDDEN) | set(VASP_OUT)
    for rel in [f"run/{job_dir}_{s}" for s in STAGES] + [f"run_aborted/{n}" for n in abn]:
        d = os.path.join(base, rel)
        if not os.path.isdir(d):
            continue
        for n in sorted(os.listdir(d)):
            if not (n in names and isfile_(os.path.join(d, n))):
                return f"file_{rel}/{n}"
    for s in STAGES:                                 # 준비 폴더 — 러너가 띄우기 전에 쓰는 이름만 (그 밖은 실행 기록 · 러너는 지우지 않고 멈춤 · Codex ER Q-ER-1①)
        rel = f"run/.prep_{job_dir}_{s}"
        d = os.path.join(base, rel)
        if not isdir_(d):
            continue
        for n in sorted(os.listdir(d)):
            if not (n in PREP_ALLOW and isfile_(os.path.join(d, n))):
                return f"prep_{rel}/{n}"
    return None


def final_problem(job, base):
    """run/final.json → 사유 | None (러너 fin_ok 와 같은 차례): UTF-8 · REC1 · code 정수 · 칸 (state · why · written_utc · written_s) · fin5 가 쓰는 code/state 조합 · attempts = 지금 시도 목록."""
    raw = _readb(os.path.join(base, "run", "final.json")) or b""
    if not _u8(raw):
        return "utf8_final.json"
    x = rec_parse(raw)
    if x is None or rec_i(x, "code") is None:
        return "final_form"
    if any(rec_s(x, k) is None for k in ("state", "why", "written_utc")) or rec_i(x, "written_s") is None:
        return "final_fields"
    if (rec_i(x, "code"), rec_s(x, "state")) not in FINAL_COMBOS:
        return "final_code_state"
    if rec_s(x, "attempts") is None:
        return "final_no_attempts"
    if rec_s(x, "attempts") != attempts_of(base, job):
        return "final_attempts_differ"
    return None


def sp_problem(base):
    """run/start_point.json → 사유 | None (러너 sp_rec5): UTF-8 · REC1 · from · path · sha256 · head 문자열 · written_s 정수."""
    raw = _readb(os.path.join(base, "run", "start_point.json")) or b""
    if not _u8(raw):
        return "utf8_start_point.json"
    x = rec_parse(raw)
    if x is None or any(rec_s(x, k) is None for k in ("from", "path", "sha256", "head")) or rec_i(x, "written_s") is None:
        return "start_point_form"
    return None


def w0_problem(base):
    """run/w0_check.json → 사유 | None (러너 w0_rec5): UTF-8 · 틀 (W0_TPL — w0_check 의 printf 그대로 · 잘림 → 거부)."""
    raw = _readb(os.path.join(base, "run", "w0_check.json")) or b""
    if not _u8(raw):
        return "utf8_w0_check.json"
    if tpl_parse(raw, W0_TPL) is None:
        return "w0_form"
    return None


def tree_problems(job, base):
    """트리 관문 (Codex EQ — 러너 tree5 와 같은 규칙 · 같은 차례 · 같은 사유 낱말) → 사유 목록. 러너는 첫 사유에서 종료 8 (아무것도 쓰지 않는다).
    차례: 이름 (files_problem) → 시도 폴더마다 (rec_dir_problem · 폴더:사유) → [중단 장부 · 영수증 · 시도 이력은 ledger_problems · abort_receipt_problem 이 따로 — 러너 ledger5] →
    끝 기록 (final_problem) → 시작점 (sp_problem) → ⓪ 기록 (w0_problem). 기존 반송본 대조 (러너 tgz5) 는 러너 쪽만 — 검사기는 반송본 하나를 받는다.
    ⚠ 못 하는 것: 모든 기록을 서로 맞게 함께 고친 트리 (위협 범위 밖 · §1b) · 반송에 담기지 않는 이름 (러너가 현장에서 막는다)."""
    J, out = job["dir"], []
    fp_ = files_problem(J, base)
    if fp_:
        out.append(fp_)
    abd_ = os.path.join(base, "run_aborted")
    abn = sorted(n for n in os.listdir(abd_) if re.fullmatch(re.escape(J) + r"_(A5|c1|c2)_[1-9][0-9]*", n)) if os.path.isdir(abd_) else []
    for rel in [f"run/{J}_{s}" for s in STAGES] + [f"run_aborted/{n}" for n in abn]:
        d = os.path.join(base, rel)
        if not os.path.isdir(d):
            continue
        st_ = rel.split("/", 1)[1][len(J) + 1:].split("_")[0]
        rp_ = rec_dir_problem(J, d, rel, st_)
        if rp_:
            out.append(f"{rel}:{rp_}")
    for f_, fn_ in (("final.json", lambda: final_problem(job, base)), ("start_point.json", lambda: sp_problem(base)), ("w0_check.json", lambda: w0_problem(base))):
        if os.path.lexists(os.path.join(base, "run", f_)):
            p_ = fn_()
            if p_:
                out.append(p_)
    return out


def a5_aborted(job, pkgdir, ret, registry, src_sha, src_head=None):
    """run_aborted/<잡>_<단>_<k> → [(꼬리표, k, 검사 기록)] — 환경 감사 · 사다리 순서에만 쓴다 (값에는 안 쓴다 · 외주 2차 aborted_attempts 와 같은 쓰임)."""
    base = ret if os.path.isdir(os.path.join(ret, "run")) else os.path.dirname(os.path.abspath(ret))
    ab, found = os.path.join(base, "run_aborted"), []
    try:
        names = sorted(os.listdir(ab))
    except FileNotFoundError:
        names = []
    except OSError as e:
        return [("run_aborted", 0, R2._unreadable(ab, "-", e))]
    for name in names:
        m, d = AB_RE.match(name), os.path.join(ab, name)
        if m and m.group(1) == job["dir"]:
            tag, k = f"{m.group(2)}@aborted{m.group(3)}", int(m.group(3))
            try:
                R2._started(d)
                if os.path.isdir(d):
                    x = check_attempt5(job, pkgdir, d, m.group(2), registry, src_sha.get(m.group(2)), (src_head or {}).get(m.group(2)))
                    rp = abort_receipt_problem(job, d, m.group(2))
                    if rp:
                        x["receipt_problem"] = rp
                    found.append((tag, k, x))
            except OSError as e:
                found.append((tag, k, R2._unreadable(d, m.group(2), e)))
    return found


def a5_unregistered(job, ret):
    """반송 트리에서 등록된 a5 시도 폴더 밖의 실행 흔적 → [(꼬리표, 등급, 사유)] (외주 2차 unregistered_traces 와 같은 규칙 · 등록 = run/<잡>_{A5,c1,c2} ·
    run_aborted/<잡>_<단>_<k>)."""
    run = os.path.join(ret, "run") if os.path.isdir(os.path.join(ret, "run")) else ret
    base = ret if run != ret else os.path.dirname(os.path.abspath(ret))
    abd = os.path.normpath(os.path.join(base, "run_aborted"))
    reg = {os.path.normpath(os.path.join(run, f"{job['dir']}_{s}")) for s in STAGES}
    out = []
    for root in (run, abd):
        errs = []
        for dp, _, fns in os.walk(root, onerror=errs.append):
            tr, dn = sorted(f for f in fns if f in R2.TRACE_NAMES), os.path.normpath(dp)
            if not tr or dn in reg:
                continue
            if os.path.dirname(dn) == abd:
                m = AB_RE.match(os.path.basename(dn))
                if m and m.group(1) == job["dir"]:
                    continue
            out.append((os.path.relpath(dn, base), "UNREGISTERED_ATTEMPT", f"등록되지 않은 폴더의 실행 흔적 {tr[:4]} — 감사되지 않음 · 채택 보류"))
        for e in errs:
            if not isinstance(e, FileNotFoundError):
                out.append((os.path.relpath(e.filename or root, base), "AUDIT_UNREADABLE", f"반송 폴더를 읽지 못했다 ({type(e).__name__})"))
    return out


def _same_start(sp, rule):
    return (sp.get("from") == rule.get("from") and sp.get("sha256") == rule.get("sha256")
            and " ".join(str(sp.get("head", "")).split()) == " ".join(str(rule.get("head", "")).split()))


def check_return(out, ret, manifest_sha256, registry=None):
    """반송 트리 → a5 결과 (시도별 상태 · ⓪ · 시작점 · 사다리 대조 · 순서 · 환경 감사). 채택은 하지 않는다 (V5 수집기 adopt_a5).
    사다리 대조 = 개정 5 해석 1 (사용자 2026-11-20 — 러너와 같은 갈래):
      · 다음 단은 앞 단이 NEXT (SCF_NOT_CONVERGED · 행 ≥ 1 실행 실패 · 행 ≥ 1 끊김 기록) 로 끝났을 때만 · 그 밖에 뒤 단이 있으면 LADDER_VIOLATION
      · 앞 단이 없음 · 준비만 · 끝 기록 없음 · 행 0 이면 LADDER_INCOMPLETE · 러너가 멈췄어야 할 것 (SCF 미확인 · 재시작 미이행 · 설정 에코) 은 STOPPED_FOR_REVIEW
      · c1 이 주 기준 OK 가 아니면 c2 가 확인된 끝 (OK · NEXT) 이어야 사다리가 끝난다 — c2 가 없거나 (run_aborted 에만 있어도) 준비만 · 끝 기록 없음 · 행 0 이면
        LADDER_INCOMPLETE · c2 가 SCF 미확인 · 재시작 미이행 · 설정 · 무결성 실패면 STOPPED_FOR_REVIEW (c2 의 주 기준이 미정 — c1 보조도 자동 채택 없음 · 리뷰 P0-1)
      · 검사기만 본 실패 (러너가 못 보는 설정 · D3 · POTCAR · 완결성) 는 어느 단이든 STOPPED_FOR_REVIEW (재시작 미이행으로 바꾸지 않는다 — 리뷰 P2(e))
      · 시작점: c 단이 있으면 run/start_point.json 이 있어야 하고 (START_POINT_MISSING), 그 기록이 규칙 (A5 자격 → A5 · 아니면 ⓪ · 둘 다 아니면 닫음)
        으로 다시 낸 시작점과 같아야 한다 (START_POINT_MISMATCH). c 단의 재시작은 그 기록에 대조한다 (리뷰 P0-2(b) · P2(e))
      · 순서: A5 끝 ≤ c1 시작 ≤ c1 끝 ≤ c2 시작 · 중단 기록은 다음 시도 시작보다 앞 (리뷰 P0-2(a))
    OK · NO_PRIMARY_VALUE 만 V5 수집기 채택 대상이다 (A5_OK_STATES)."""
    V.verify_manifest(out, manifest_sha256)
    meta = json.load(open(os.path.join(out, "jobs.json"), encoding="utf-8"))
    if meta.get("schema") != SCHEMA_PKG:
        raise PkgError(f"묶음 schema {meta.get('schema')!r}")
    job = meta["jobs"][0]
    run = os.path.join(ret, "run") if os.path.isdir(os.path.join(ret, "run")) else ret
    P = lambda s: os.path.join(run, f"{job['dir']}_{s}")
    w0 = check_w0(run, meta)
    W0S = meta["w0"]["sha256"]
    sp, sp_err = load_start_point(run, job)
    fin_rec, fin_err = load_final(run)
    A = check_attempt5(job, out, P("A5"), "A5", registry, W0S if w0.get("verified") else None)
    cA, _ = a5_class(A)
    if A["status"] == "INCOMPLETE_ATTEMPT":
        a_ok, a_why = False, "A5 끝 기록 없음 (attempt.json — 끊김이면 정상 종료가 아니다)"
    elif not A.get("judge"):
        a_ok, a_why = False, f"A5 {A['status']}"
    else:
        a_ok, a_why = R2.a_eligible({**A, "status": A["judge"]["status"]})        # 러너가 본 갈래 (판정 + WAVECAR 기록) — 검사기만 본 실패는 따로 (리뷰 P2(e))
    a_sha = str((A.get("wavecar") or {}).get("sha256") or "")
    rule = None
    if cA in ("OK", "NEXT"):
        if a_ok and V.HEX64.match(a_sha):
            rule = {"from": "A5", "sha256": a_sha, "head": (A.get("wavecar") or {}).get("head")}
        elif w0.get("verified"):
            rule = {"from": "W0", "sha256": W0S, "head": (w0.get("record") or {}).get("head"), "why": a_why}
    eff = sp if sp is not None else rule
    ss, sh = (eff or {}).get("sha256"), (eff or {}).get("head")
    C1 = check_attempt5(job, out, P("c1"), "c1", registry, ss, sh)
    C2 = check_attempt5(job, out, P("c2"), "c2", registry, ss, sh)
    att = {"A5": A, "c1": C1, "c2": C2}
    aborted = a5_aborted(job, out, ret, registry, {"A5": W0S if w0.get("verified") else None, "c1": ss, "c2": ss}, {"c1": sh, "c2": sh})
    unreg = a5_unregistered(job, ret)
    env = R2.env_audit([(k, v) for k, v in att.items() if v["status"] != "MISSING"] + [(t, x) for t, _, x in aborted], registry)
    cls = {s_: a5_class(att[s_]) for s_ in STAGES}
    present = lambda s_: att[s_]["status"] != "MISSING" or any(t.startswith(f"{s_}@") for t, _, _ in aborted)
    viol, incomplete, review, sp_prob = [], [], [], []
    for s_ in STAGES:
        if cls[s_][1]:
            review.append(f"{s_} 검사기만 본 실패 — {cls[s_][1]}")
    want_var = "A5c" if w0.get("verified") else "A5f"
    base = ret if os.path.isdir(os.path.join(ret, "run")) else os.path.dirname(os.path.abspath(ret))
    for t_, k_, x_ in aborted:
        if (x_.get("osz_rows") or 0) > 0:
            viol.append(f"{t_} 는 전자 반복행 {x_.get('osz_rows')} 개 — 0 스텝 중단으로 옮길 수 없는 시도다")
        if (x_.get("row_scan") or {}).get("why", "-") != "-":
            viol.append(f"{t_} 는 OSZICAR 행 판독 {x_['row_scan']['why']} — 행꼴 조각 · 남의 머리가 있어 0 스텝 중단으로 옮길 수 없는 시도다 (러너 --infra-abort 도 거부 · Codex EO P0)")
        if x_.get("receipt_problem"):
            viol.append(f"{t_} {x_['receipt_problem']}")
        if t_.startswith("A5@") and x_.get("variant") and x_["variant"] != want_var:
            viol.append(f"{t_} 변형 {x_['variant']} ≠ ⓪ 판정에 맞는 변형 ({want_var})")
    if len(aborted) > INFRA_MAX:
        viol.append(f"0 스텝 인프라 중단 {len(aborted)} 회 > 잡 전체 {INFRA_MAX} 회")
    if A["status"] != "MISSING" and A.get("variant") and A["variant"] != want_var:
        viol.append(f"A5 변형 {A['variant']} ≠ ⓪ 판정에 맞는 변형 ({want_var})")
    viol += ledger_problems(job, base)        # 중단 장부 ↔ 보존 폴더 양방향 (러너 ledger5 · Codex EO P1 Q-EO-3)
    seq = []                                  # 띄운 시도 (attempt.start 있음) 만 순서에 넣는다 — 준비만 있는 폴더는 사다리 대조 (PREP_ONLY) 가 다룬다
    for s_ in STAGES:
        for t_, k_, x_ in sorted((y for y in aborted if y[0].startswith(f"{s_}@")), key=lambda y: y[1]):
            if x_.get("started"):
                seq.append((t_, x_.get("times") or {}, os.path.join(base, x_.get("dir", ""))))
            elif x_.get("status") != "ATTEMPT_UNREADABLE":
                viol.append(f"{t_} 에 시작 표지 (attempt.start) 가 없다 — 러너는 띄운 시도만 0 스텝 중단으로 옮긴다")
        if att[s_].get("started"):
            seq.append((s_, att[s_].get("times") or {}, P(s_)))
    viol += order_violations([(t_, tm_) for t_, tm_, _ in seq])
    # 누적 벽시계 · 상한 — 러너 cap_gate 가 띄울 때마다 본 것을 기록으로 다시 낸다 (Codex EO P1 Q-EO-2c): 앞 시도들의 벽시계 (wall_of — 영수증이 먼저) 가 다 알려졌고
    # 합 ≤ 상한이어야 그 시도를 띄울 수 있었다 · 미상 (UNKNOWN) 영수증은 그 자체로는 적법하지만 그 뒤에 시도가 있으면 안 된다 · --infra-wall 로 채운 시각 ≤ 다음 시도 시작
    cap_s, tot, unk, fill = float(meta.get("cap_h", CAP_H)) * 3600.0, 0, None, None
    for t_, tm_, d_ in seq:
        if unk is not None:
            viol.append(f"{t_} 앞 시도 {unk} 의 벽시계가 미상 · 판독 불가인데 {t_} 를 띄웠다 — 러너는 미상이면 띄우지 않는다 (Codex EO P1 Q-EO-2c)")
        elif tot > cap_s:
            viol.append(f"{t_} 앞 누적 벽시계 {tot} s > 상한 {cap_s:g} s 인데 {t_} 를 띄웠다 (영수증 시간이 먼저 · Codex EO P1 Q-EO-2c)")
        if fill is not None and tm_.get("start") is not None and tm_["start"] < fill[1]:
            viol.append(f"{t_} 시작 {tm_['start']} < 앞 시도 {fill[0]} 의 벽시계를 채운 시각 {fill[1]} — 미상인 채로 띄웠다 (Codex EO P1 Q-EO-2c)")
        w_ = wall_of(d_)
        if w_ is None or w_ == "UNKNOWN":
            unk = unk or f"{t_} ({'판독 불가' if w_ is None else 'UNKNOWN'})"
        else:
            tot += w_
        fs_ = rec_i(rec_read(os.path.join(d_, "infra_abort.json")), "wall_s_filled_s") if os.path.basename(os.path.dirname(os.path.abspath(d_))) == "run_aborted" else None
        fill = (t_, fs_) if fs_ is not None else None
    c_t0 = [tm.get("start") for t_, tm, _ in seq if t_.split("@")[0] in ("c1", "c2") and tm.get("start") is not None]
    if sp is not None and c_t0:                # 시작점은 첫 c 단 전에 한 번 쓴다 — 유실 뒤 다시 쓴 기록은 첫 c 단보다 늦다 (Codex EN P1)
        ws_ = sp.get("written_s")
        if not (isinstance(ws_, int) and not isinstance(ws_, bool)):
            viol.append(f"시작점 기록 시각 (written_s {ws_!r}) 이 정수가 아니다 — 첫 c 단 전에 썼는지 확인할 수 없다")
        elif ws_ > min(c_t0):
            viol.append(f"시작점 기록 written_s {ws_} > 첫 c 단 시작 {min(c_t0)} — 시작점은 첫 c 단 전에 한 번만 쓴다 (유실 뒤 다시 쓴 기록 · Codex EN P1)")

    viol += [f"트리 관문 ({t_}) — 러너는 이 트리에서 아무것도 쓰거나 띄우거나 포장하지 않고 멈춘다 (종료 8 · Codex EQ)" for t_ in tree_problems(job, base)]

    def stop_at(s_, kind, later):
        lat = [x for x in later if present(x)] + (["시작점 기록"] if (s_ == "A5" and sp is not None) else [])
        msg = {"MISSING": "없다", "PREP_ONLY": "준비만 있다 (VASP 를 띄운 흔적 없음)", "WAIT": "끝 기록이 없다 (끊김 — --killed · --infra-abort 기록 대기)",
               "ZERO": "전자 반복행 0 (0 스텝 — --infra-abort 기록 대기 또는 연락)", "REVIEW": f"{att[s_]['status']} — 러너가 멈춰야 하는 결과 (개정 5 해석 1 · 1저자)"}[kind]
        if lat:
            viol.append(f"{s_} 가 {msg} 인데 뒤 단 {lat} 이 있다")
        elif kind == "REVIEW":
            review.append(f"{s_} {msg}")
        else:
            incomplete.append(f"{s_} {msg}")
    closed, done_ok = False, None
    if cA in ("MISSING", "PREP_ONLY", "WAIT", "ZERO", "REVIEW"):
        stop_at("A5", cA, ("c1", "c2"))
    elif cA in ("OK", "NEXT"):
        if rule is None:
            if present("c1") or present("c2") or sp is not None:
                viol.append(f"A5 자격 미달 ({a_why}) · ⓪ 확인 안 됨 — 닫힌 사다리인데 c 단 · 시작점 기록이 있다")
            else:
                closed = True
        else:
            if (present("c1") or present("c2")) and sp is None:
                sp_prob.append(("START_POINT_MISMATCH", f"c 단이 있는데 시작점 기록을 읽을 수 없다 — {sp_err}") if sp_err else
                               ("START_POINT_MISSING", "c 단이 있는데 시작점 기록 (run/start_point.json) 이 없다"))
            if sp is not None and not _same_start(sp, rule):
                sp_prob.append(("START_POINT_MISMATCH", f"시작점 기록 {sp.get('from')} {str(sp.get('sha256'))[:12]} ≠ 규칙 (A5 자격 → A5 · 아니면 ⓪) 으로 낸 "
                                f"{rule['from']} {str(rule['sha256'])[:12]} (머리 {sp.get('head')} · {rule.get('head')})"))
            k1 = cls["c1"][0]
            if k1 in ("MISSING", "PREP_ONLY", "WAIT", "ZERO", "REVIEW"):
                stop_at("c1", k1, ("c2",))
            elif k1 == "OK":
                if present("c2"):
                    viol.append("c2 가 있는데 c1 이 주 기준 OK — c2 는 c1 이 주 기준 OK 가 아닐 때만")
                done_ok = "c1"
            elif k1 == "NEXT":
                k2 = cls["c2"][0]
                if k2 in ("MISSING", "PREP_ONLY", "WAIT", "ZERO"):
                    incomplete.append(f"c1 이 {C1['status']} 로 끝났는데 c2 가 " + {"MISSING": "없다 (run_aborted 에만 있어도 같다)", "PREP_ONLY": "준비만 있다",
                                                                               "WAIT": "끝 기록이 없다", "ZERO": "전자 반복행 0 이다"}[k2]
                                      + " — 사다리가 끝나지 않았다 (c1 보조 자동 채택 없음 · 리뷰 P0-1)")
                elif k2 == "REVIEW":
                    review.append(f"c2 {C2['status']} — c2 주 기준 미정 (재시작 미이행 · SCF 미확인 · 설정 에코) → c1 보조도 자동 채택 없음 · 1저자 (리뷰 P0-1)")
                elif k2 == "OK":
                    done_ok = "c2"
    if fin_rec is not None and fin_rec.get("attempts") != attempts_of(base, job):
        review.append("러너 끝 기록 (final.json attempts) 의 시도 목록이 이 반송의 시도 폴더 · run_id 와 다르다 — 다른 실행의 묶음 · 끝난 뒤 바뀐 폴더 (Codex EO P2)")
    if sp_err and not sp_prob:
        sp_prob.append(("START_POINT_MISMATCH", sp_err))
    blk = [(k, v["status"]) for k, v in att.items() if v["status"] in BLOCKING]
    res = {"status": None, "w0": w0, "a5_eligible": [a_ok, a_why], "start_point": ({"from": eff["from"], "sha256": eff["sha256"]} if eff else None),
           "start_point_record": sp, "start_point_rule": rule, "final_record": fin_rec, "classes": {k: list(v) for k, v in cls.items()},
           "attempts": att, "ladder_violations": viol, "ladder_incomplete": incomplete, "review": review,
           "aborted": [[t, x.get("status")] for t, _, x in aborted], "unregistered": [list(u) for u in unreg], "env_in": [list(e) for e in env]}
    if env:
        res.update(status=env[0][1], why=f"환경 감사 — {env[0][0]}: {env[0][2]}")
    elif unreg:
        res.update(status="UNREGISTERED_ATTEMPT", why=unreg[0][2])
    elif w0["status"] not in ("OK",) and not (w0["status"] == "W0_RECORD_MISSING" and A["status"] == "MISSING"):
        res.update(status=w0["status"], why=w0.get("why", "⓪ 기록"))
    elif viol:
        res.update(status="LADDER_VIOLATION", why=viol[0])
    elif blk:
        res.update(status=blk[0][1], why=f"시도 {blk[0][0]} 무결성 실패 — {att[blk[0][0]].get('why', '')}"[:300])
    elif sp_prob:
        res.update(status=sp_prob[0][0], why=sp_prob[0][1])
    elif review:
        res.update(status="STOPPED_FOR_REVIEW", why=review[0])
    elif incomplete:
        res.update(status="LADDER_INCOMPLETE", why=incomplete[0])
    elif fin_err:
        res.update(status="STOPPED_FOR_REVIEW", why=f"러너 끝 기록 {fin_err}")
    else:
        st_, why_ = (("OK", f"주 기준 수렴 ({done_ok})") if done_ok else
                     ("NO_PRIMARY_VALUE", "A5 자격 미달 · ⓪ 확인 안 됨 — 닫음 (값 없음)" if closed else f"c1 {C1['status']} · c2 {C2['status']} — 보조 기준은 V5 수집기가 본다"))
        want_code = 0 if st_ == "OK" else 1
        if fin_rec is None:
            res.update(status="STOPPED_FOR_REVIEW", why="러너 끝 기록 (run/final.json) 이 없다 — 러너는 사다리 끝 (0 · 1) 마다 쓰고 묶는다 · 끝 기록 없는 반송은 채택하지 않는다 (Codex EP 조건부)")
        elif fin_rec.get("code") != want_code:
            res.update(status="STOPPED_FOR_REVIEW", why=f"러너 끝 기록 (final.json 코드 {fin_rec.get('code')} · {fin_rec.get('state')}) ≠ 기록으로 낸 사다리 판정 {st_} (코드 {want_code})")
        else:
            res.update(status=st_, why=why_)
    return meta, res


# ───────────────────────── 시험용 가짜 VASP ─────────────────────────
FAKE_VASP5 = r"""
import os, sys, json, re, struct, math
plan = json.load(open(os.environ["FAKE_PLAN"])) if os.environ.get("FAKE_PLAN") else {}
pkg = json.load(open(os.path.join(os.environ["FAKE_PKG"], "jobs.json")))
j = pkg["jobs"][0]
def iv(t, k):
    v = None
    for ln in t.splitlines():
        ln = re.split(r"[#!]", ln, maxsplit=1)[0]
        for st in ln.split(";"):
            if "=" in st and st.split("=", 1)[0].strip().upper() == k:
                v = st.split("=", 1)[1].strip()
    return v
inc = open("INCAR").read()
st = os.path.basename(os.getcwd()).rsplit("_", 1)[1]
beh, _, cut = plan.get(st, "conv").partition("@")      # 'beh@N' — 전자 반복행 N 개만 쓰고 끝 기록 없이 (스케줄러에 끊긴 VASP 흉내 · Codex EN 의 7 행 중단)
cut, _, frag = cut.partition("|")                        # 'beh@N|조각' — 그 뒤에 조각을 줄바꿈 없이 (잘린 행 흉내 · '\\n' 은 줄바꿈 · Codex EO P0 의 'SDA:' 절단)
nelm = int(iv(inc, "NELM")); lwave = (iv(inc, "LWAVE") or "").upper().strip(".") in ("TRUE", "T")
ldip = (iv(inc, "LDIPOL") or "").upper().strip(".") in ("TRUE", "T")
ist_in = int(iv(inc, "ISTART") or 0); ich_in = int(iv(inc, "ICHARG") or 2)
ist = 1 if (ist_in == 1 and os.path.isfile("WAVECAR") and beh not in ("noread", "istart0", "istart0p")) else 0
ich = ich_in if ist == 1 else 2
algo = (iv(inc, "ALGO") or "Normal").lower(); ialgo = 58 if algo == "all" else 38
maxmix = int(iv(inc, "MAXMIX") or -45); amix = float(iv(inc, "AMIX") or 0.4); amin = float(iv(inc, "AMIN") or min(0.1, amix)); tim = float(iv(inc, "TIME") or 0.4)
if beh == "badecho":
    maxmix = -45
h1, h2 = ("SDA", "CGA") if ialgo == 58 else ("DAV", "DAV")
if beh == "sda_rows":
    h1, h2 = "SDA", "CGA"
if beh == "dav_rows":
    h1, h2 = "DAV", "DAV"
if beh == "unknown_hdr":
    h1, h2 = "XYZ", "XYZ"
E0 = -731.2 if ldip else -731.0
rows, rc, term = [], 0, True
def conv_rows(n=30):
    out = [(k, E0 + 0.5 / k ** 2, 1e-3 / k, 1e-4 / k) for k in range(1, n)]
    return out + [(n, E0, -3.1e-8, -1.2e-8)]
if beh in ("conv", "sda_rows", "dav_rows", "unknown_hdr", "noread", "istart0", "istart0p", "modwav", "badhead", "badecho", "nowav", "nophrase", "d3off"):
    rows = conv_rows()
elif beh == "noconv":
    rows = [(k, E0 + 0.0003 * (-1) ** k, 2.2e-4 * (-1) ** k, 1e-5) for k in range(1, nelm + 1)]
elif beh in ("plateau", "rmsjump"):
    rows = [(k, E0 + 0.002 * math.sin(k), 0.0, 1e-5) for k in range(1, nelm + 1)]
elif beh == "wide":
    rows = [(k, E0 + 0.2 * math.sin(k), 0.0, 1e-5) for k in range(1, nelm + 1)]
elif beh == "drift":
    rows = [(k, E0 - 0.0005 * k, -5e-4, 1e-5) for k in range(1, nelm + 1)]
elif beh == "short":
    rows = [(k, E0 + 0.002 * math.sin(k), 0.0, 1e-5) for k in range(1, 61)]
elif beh == "crash":
    rows, rc, term = [(k, E0, 1e-2, 1e-3) for k in range(1, 8)], 1, False
elif beh == "zero":
    rows, rc, term = [], 1, False
rr = []
for idx, (k, e, de, dp) in enumerate(rows):
    if beh in ("plateau", "rmsjump", "wide", "short") and idx > 0:
        de = e - rows[idx - 1][1]
    rmsc = 0.03 if not (beh == "rmsjump" and k == 150) else 30.0
    rr.append((k, e, de, dp, rmsc))
if cut:
    rr, term = rr[:int(cut)], False
osz = open("OSZICAR", "w")
osz.write("       N       E                     dE             d eps       ncg     rms          rms(c)\n")
for i, (k, e, de, dp, rmsc) in enumerate(rr):
    h = h1 if i == 0 else h2
    osz.write(f"{h}: {k:4d}   {e:.12E}   {de: .5E}   {dp: .5E}  8000   0.300E-03    {rmsc:.3E}\n")
if frag:
    osz.write(frag.replace("\\n", "\n"))
if term and rr:
    osz.write(f"   1 F= {rr[-1][1]:.8E} E0= {rr[-1][1]:.8E}  d E ={rr[-1][1]:.6E}\n")
osz.close()
version = os.environ.get("FAKE_VERSION", "vasp.5.4.4.18Apr17-6-g9f103f2a35 (build Aug 19 2022 11:57:46) complex")
pot = open("POTCAR").read()
titel = re.findall(r"TITEL\s*=\s*(.+)", pot); zv = [float(x) for x in re.findall(r"ZVAL\s*=\s*(-?\d+\.?\d*)", pot)]
pl = open("POSCAR").read().splitlines(); nn = [int(x) for x in pl[6].split()]
nel = sum(z * n for z, n in zip(zv, nn)); nions = sum(nn)
dz = float(iv(inc, "DIPOL").split()[2])
o = [f" {version}", " executed on             LinuxIFC date 2026.11.21  00:00:00", "", " INCAR:"] + [f"   {x}" for x in inc.splitlines()]
o += [f" POTCAR:    {t}" for t in titel] + [f"   TITEL  = {t}" for t in titel]
nb = 873 if beh == "badhead" else 872
o += [" Dimension of arrays:", f"   k-points           NKPTS =      4   k-points in BZ     NKDIM =      4   number of bands    NBANDS=    {nb}",
      f"   number of dos      NEDOS =    301   number of ions     NIONS = {nions:6d}", "   dimension x,y,z NGXF=   168 NGYF=   336 NGZF=   400", "",
      " Startparameter for this run:", "   NWRITE =      2    write-flag & timer", f"   ISTART =      {ist}    job   : 0-new  1-cont  2-samecut",
      f"   ICHARG =      {ich}    charge: 1-file 2-atom 10-const", "   ISPIN  =      1    spin polarized calculation?",
      f"   ENCUT  =  {float(iv(inc, 'ENCUT')):5.1f} eV  47.77 Ry    6.91 a.u.", f"   NELM   =    {nelm};   NELMIN=  6; NELMDL=  0     # of ELM steps",
      f"   NELECT = {nel:12.4f}    total number of electrons", f"   ISMEAR =     {int(iv(inc, 'ISMEAR'))};   SIGMA  = {float(iv(inc, 'SIGMA')):7.2f}  broadening in eV -4-tet -1-fermi 0-gaus",
      f"   IALGO  =     {ialgo}    algorithm", "   IMIX   =      4    mixing-type and parameters", f"     AMIX     = {amix:6.2f};   BMIX     =  1.00",
      f"     AMIN     = {amin:6.2f}", f"     WC   =   100.;   INIMIX=   1;  MIXPRE=   1;  MAXMIX= {maxmix}", f"   TIME   = {tim:6.2f}     timestep for ELM",
      f"   LDIPOL =      {'T' if ldip else 'F'}    correct potential (dipole corrections)", "   IDIPOL =      3    1-x, 2-y, 3-z, 4-all directions",
      "   GGA     =    PE    GGA type"]
cap = (abs(maxmix) - 1) if maxmix < 0 else maxmix
for i, (k, e, de, dp, rmsc) in enumerate(rr):
    o.append(f"--------------------------------------- Iteration      1( {k:3d})  ---------------------------------------")
    if ldip:
        o += [" DIPCOR: dipole corrections for dipol", f" direction  3 min pos {round(((dz + 0.5) % 1.0) * 400) % 400:5d},"]
    o += [" dipolmoment           0.000000      0.000000      0.100000 electrons x Angstroem", " dipol+quadrupol energy correction           -0.000107 eV"]
    if ialgo == 38 and k >= 2:
        hl = min(k - 1, cap)
        o += ["", " eigenvalues of (default mixing * dielectric matrix)", "  average eigenvalue GAMMA=   0.6000", "  " + " ".join("0.6000" for _ in range(hl)), ""]
Ed = j["d3_2body_eV_ref"] * (1.05 if beh == "d3off" else 1.0)
if term and rr:
    Et = rr[-1][1] + Ed
    o += [" E-fermi :   0.9032     XC(G=0):  -6.3203     alpha+bet : -6.2429", "         DFTD3 V3.0 Rev 1        ", " IVDW         = 12", " VDW_S6       = 1.0000",
          " VDW_S8       = 0.7875", " VDW_A1       = 0.4289", " VDW_A2       = 4.4407", " VDW_RADIUS   = 50.2000 A", " VDW_CNRADIUS = 21.1700 A", f" Edisp (eV)  {Ed:.5f}",
          "  FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)", "  ---------------------------------------------------", f"  free  energy   TOTEN  =  {Et:18.8f} eV", "",
          f"  energy  without entropy=  {Et + 0.01:18.8f}  energy(sigma->0) =  {Et + 0.005:18.8f}", " General timing and accounting informations for this job:"]
open("OUTCAR", "w").write("\n".join(o) + "\n")
so = [" running on   64 total cores", f" {version}"]
if (ist == 1 or beh == "istart0p") and beh != "nophrase":         # istart0p: 문구는 있는데 OUTCAR ISTART 0 (원문끼리 모순 — ISTART 확인만 잡는다)
    so.append(" the WAVECAR file was read successfully")
open("stdout.log", "w").write("\n".join(so) + "\n")
if lwave and beh != "nowav" and rr and term:
    recl = 64
    rec1 = struct.pack("3d", recl, 1, 45200).ljust(recl, b"\0")
    rec2 = struct.pack("3d", 4, nb, float(iv(inc, "ENCUT"))).ljust(recl, b"\0")
    open("WAVECAR", "wb").write(rec1 + rec2 + os.urandom(512))
if beh == "modwav" and os.path.isfile("WAVECAR"):
    open("WAVECAR", "ab").write(b"x")
for f in ("CHGCAR", "CHG", "vasprun.xml"):
    open(f, "w").write("FAKE DO_NOT_SHIP\n")
sys.exit(rc)
"""


# ───────────────────────── selftest ─────────────────────────
def _fake_wavecar(path, nb=872, encut=650.0, extra=512):
    import struct
    recl = 64
    open(path, "wb").write(struct.pack("3d", recl, 1, 45200).ljust(recl, b"\0") + struct.pack("3d", 4, nb, encut).ljust(recl, b"\0") + b"\x01" * extra)


def _selftest():
    import tempfile
    import tarfile
    ok = bad = 0

    def ck(c, m):
        nonlocal ok, bad
        if c:
            ok += 1
        else:
            bad += 1; print("  ✗", m)
            if os.environ.get("A5_SELFTEST_FAILFAST"):                 # 돌연변이 시험: 첫 빨강에서 멈춘다 (판정은 같다 — 0 아닌 종료)
                print(f"⛔ 빠른 멈춤 — {ok}/{ok + bad}"); sys.exit(1)

    def raises(fn):
        try:
            fn()
        except PkgError:
            return True
        return False
    py = sys.executable
    # ① 순수 함수 — 행 머리 관문 · 판정 · 보조 숫자
    dav = lambda n, conv=True: "".join(f"DAV: {k:4d}   {-731 + 0.001 * k:.12E}   {(-3e-8 if (conv and k == n) else 2e-4): .5E}   {(-1e-8 if (conv and k == n) else 1e-5): .5E}  8000   0.3E-03  0.3E-01\n"
                                       for k in range(1, n + 1))
    out_ok = " vasp.5.4.4\n Iteration      1(  30)\n General timing and accounting informations for this job:\n"
    inc = "NELM = 400\nEDIFF = 1E-6\n"
    ck(judge5(dav(30), out_ok, inc, 0, "c1")[0] == "OK", "c1 DAV 행 수렴 → OK")
    ck(judge5(dav(30).replace("DAV:", "SDA:"), out_ok, inc, 0, "c1")[:1] == ("SCF_UNVERIFIED",) and
       judge5(dav(30).replace("DAV:", "SDA:"), out_ok, inc, 0, "c1")[4] == "row_header_SDA", "⛔음성 c1 에 SDA/CGA 행 → SCF_UNVERIFIED (row_header_SDA)")
    sda = dav(30).replace("DAV:", "CGA:").replace("CGA:    1", "SDA:    1", 1)
    ck(judge5(sda, out_ok, inc, 0, "c2")[0] == "OK", "c2 SDA · CGA 행 수렴 → OK (2차 계약 입력은 DAV 로 바꿔 넘김)")
    ck(judge5(dav(30), out_ok, inc, 0, "c2")[4] == "row_header_DAV", "⛔음성 c2 에 DAV 행 → SCF_UNVERIFIED")
    ck(judge5(dav(30).replace("DAV:", "XYZ:"), out_ok, inc, 0, "A5")[4] == "row_header_XYZ", "⛔음성 모르는 행 머리 → SCF_UNVERIFIED")
    ck(judge5(dav(30) + "CG :  31   1  1  1\n", out_ok, inc, 0, "c1")[4] == "row_header_CG", "⛔음성 'CG :' (공백 머리) → SCF_UNVERIFIED")
    ck(judge5("SDA:1 -0.1E+03 -3E-08 -1E-08\n", out_ok, inc, 0, "c1")[4] == "row_header_SDA", "⛔음성 콜론 뒤 공백 없는 SDA 행도 관문에 걸린다 (2차 행 정규식 우회 막음)")
    ck(judge5(None, out_ok, inc, 0, "c1")[4] == "no_rows", "OSZICAR 없음 → 2차 계약 그대로 (no_rows)")
    # ①a 완전한 전자 반복행 (Codex EO P0) — 줄바꿈으로 끝남 · 그 단의 머리 그대로 · ':' 뒤 빈칸 · 칸 ≥ 6 · N 정수 / 잘린 꼬리는 세지 않음 / 완전한 행 0 + 조각 = 손상
    hd_ = "       N       E                     dE             d eps       ncg     rms          rms(c)\n"
    sda1 = "SDA:   1    -0.731000000000E+03   -0.73100E+03   -0.12000E+02  8000   0.300E-03\n"
    cga2 = "CGA:   2    -0.731100000000E+03   -0.10000E+00   -0.30000E-01  8000   0.200E-03    0.100E-01\n"
    rg = lambda t, st="c2": row_gate(t, st)
    ck(rg(hd_ + "SDA:") == (0, "incomplete_row"), f"⛔음성 Codex EO P0: c2 첫 행이 'SDA:' 에서 잘림 → 완전한 행 0 · 손상 (1 행으로 세지 않는다) — {rg(hd_ + 'SDA:')}")
    ck(rg(hd_ + sda1 + "SDA:") == (1, None), f"Codex EO P0: 완전한 1 행 뒤 'SDA:' 잘린 꼬리 → 1 행 (꼬리는 세지 않고 손상도 아니다) — {rg(hd_ + sda1 + 'SDA:')}")
    ck(rg(hd_ + sda1 + cga2[:-1]) == (1, None), "완전해 보이는 끝 조각도 줄바꿈이 없으면 세지 않는다 (마지막 칸이 잘렸는지 알 수 없다)")
    ck(rg(hd_ + sda1 + "SDA:\n") == (1, "incomplete_row") and rg(hd_ + sda1 + "CGA:   2   -0.73E+03\n") == (1, "incomplete_row"),
       "⛔음성 줄바꿈까지 쓰인 덜 쓴 행 ('SDA:\\n' · 칸 2 개) → 손상 (잘림이 아니다)")
    ck(rg(hd_ + sda1 + "CGA:   2   -0.73E+03\n" + cga2.replace("   2 ", "   3 ")) == (2, "incomplete_row"), "⛔음성 중간의 덜 쓴 행 → 손상 (뒤 행이 있어도)")
    ck(rg(hd_ + "SDA:1 -0.1E+03 -3E-08 -1E-08 8000 0.3E-03\n") == (0, "incomplete_row") and rg(hd_ + "DA V:   1  -7.3E+02 1 1 8000 1\n", "c1") == (0, "incomplete_row"),
       "⛔음성 ':' 뒤 빈칸 없음 · 머리 사이 빈칸 ('DA V:') → 완전한 행이 아니다 (판정 계약의 칸 위치와 어긋남)")
    ck(rg(hd_ + "XYZ:   1  -7.3E+02  1  1  8000  1\n" + "SDA:") == (0, "row_header_XYZ") and rg(hd_ + sda1 + "\x00\n") == (0, "nul_bytes"),
       "⛔음성 남의 머리가 손상보다 먼저 · NUL → nul_bytes")
    ck(rg(dav(30), "c1") == (30, None) and rg(dav(30)[:-1], "c1") == (29, None), "DAV 30 행 → 30 · 마지막 줄바꿈이 없으면 29 (끝 조각)")
    ck(row_gate("DAV:   1     0.137702065626E+05    0.13770E+05   -0.61641E+05  7848   0.137E+03\n"
                "DAV:   2    -0.412587307621E+03   -0.14183E+05   -0.13562E+05 10088   0.328E+02    0.201E+01\n", "A5") == (2, None),
       "5.4.4 실물 꼴: 칸 6 (rms(c) 없는 첫 행) · 칸 7 둘 다 완전한 행")
    jt_ = judge5(dav(7, conv=False) + "DAV:   8   -0.7310", " vasp.5.4.4\n Iteration      1(   8)\n", inc, 1, "c1")
    ck(jt_[:2] == ("RUN_FAILED", 7), f"충돌 (rc 1) · 완전한 7 행 + 잘린 꼬리 → RUN_FAILED 7 행 (꼬리는 판정 입력에서 뺀다) — {jt_}")
    ck(osz_rows(dav(3) + "DAV:   4   -7.3E+02", "c1") == osz_rows(dav(3), "c1") and len(osz_rows(dav(3), "c1")) == 3, "보조 숫자의 행 목록도 완전한 행만")
    # ①a′ 숫자로 읽히는 행 (Codex EP P0) — 칸 6 또는 7 · N 양의 정수 · ncg 정수 · 나머지 실수 (부호 · 소수점 · E 지수 두 자리) / 콜론 앞에서 잘린 머리
    gb_ = "SDA: 1 none missing missing abc bad\n"
    ck(rg(hd_ + gb_) == (0, "incomplete_row") and rg(hd_ + sda1 + gb_) == (1, "incomplete_row"),
       f"⛔음성 Codex EP P0: 유일 행 'SDA: 1 none missing missing abc bad' (칸 수만 맞음) → 완전한 행 0 · 손상 — {rg(hd_ + gb_)}")
    ck(all(rg(x_, "c1") == (0, "incomplete_row") for x_ in ("DAV:   1   NaN   NaN   NaN  8000   0.3E-03\n", "DAV:   1   -0.73E+03   1E-3   1E-4   80.5   0.3E-03\n",
                                                           "DAV:   0   -0.73E+03   1E-3   1E-4   80   0.3E-03\n", "DAV:   1   -0.73E+03   1E-3   1E-4   80   0.3E-03   0.1   9\n",
                                                           "DAV:   1   -0.73E+100   1E-3   1E-4   80   0.3E-03\n", "DAV:   1   -0.73E+03   1E-3   1E-4   ******   0.3E-03\n",
                                                           "DAV:   -1   -0.73E+03   1E-3   1E-4   80   0.3E-03\n", "DAV:   1   -0.73E+03   1E-3   1E-4   80   inf\n")),
       "⛔음성 NaN · 정수 아닌 ncg · N 0 · N 음수 · 칸 8 · 지수 세 자리 · *** · inf → 완전한 행이 아니다 (손상)")
    ck(rg("DAV:   1   -0.73E+03   +1.E-3   .1E-4   80   0.3E-03\n", "c1") == (1, None) and rg("DAV:   1   -731   0   0   80   3\n", "c1") == (1, None),
       "숫자 꼴: 부호 · 끝 소수점 · 앞 소수점 · 정수 실수 → 완전한 행")
    ck(rg(hd_ + "SDA") == (0, "incomplete_row") and rg(hd_ + "D", "c1") == (0, "incomplete_row") and rg(hd_ + "SD A") == (0, "incomplete_row")
       and rg(hd_ + sda1 + "SDA") == (1, None) and rg("       N       E   ") == (0, None),
       "⛔음성 Codex EP P0: 콜론 앞 머리 절단 ('SDA' · 'D') + 완전한 행 0 → 손상 · 완전한 1 행 뒤면 세지 않는 꼬리 · 열 머리 줄의 절단 · 앞 빈칸 조각은 0 스텝")
    ck(rg(hd_ + "  SDA") == (0, "incomplete_row") and rg(hd_ + "\tDA", "c1") == (0, "incomplete_row") and rg(hd_ + "  DAV") == (0, "incomplete_row")
       and rg("       N") == (0, None) and rg("       N   ") == (0, None) and rg(hd_ + "  ") == (0, None) and rg("N") == (0, "incomplete_row")
       and rg(hd_ + sda1 + "  SDA") == (1, None),
       f"⛔음성 Codex EQ P0: 앞 빈칸 뒤 머리 조각 ('  SDA' · 탭 'DA' · 남의 머리 '  DAV') + 완전한 행 0 → 손상 · 앞 빈칸 'N' (열 제목) 만 0 스텝 · 줄 맨 앞 'N' 은 손상 · 완전한 1 행 뒤면 꼬리 — {rg(hd_ + '  SDA')}")
    r24 = "SDA:   1   " + "1" * 24 + "   -0.10000E+00   -0.10000E+00  8000   0.300E-03\n"
    ck(rg(hd_ + r24) == (1, None) and rg(hd_ + r24.replace("1" * 24, "1" * 25)) == (0, "incomplete_row") and rg(hd_ + r24.replace("1" * 24, "1" * 310)) == (0, "incomplete_row")
       and rg(hd_ + r24.replace("8000", "8" * 25)) == (0, "incomplete_row"),
       "⛔음성 Codex EQ P0: 숫자 칸 길이 ≤ 24 (지수 두 자리와 함께 |x| < 1e119 — 늘 유한) · 25 자리 · 310 자리 에너지 · 25 자리 ncg → 손상")
    # ①b′ 한 줄 기록 문법 REC1 (Codex EO P1 Q-EO-2a) — 쉼표 유실 · 날것 제어문자 · 같은 키 거부 · 콜론 뒤 공백 없음 · 이스케이프는 받음
    kj = {"job": JOB, "rung": "c2", "run_id": "20261122T000000-1-1", "osz_rows": "7", "recorded_s": 5}
    canon = (json.dumps(kj) + "\n").encode()
    ck(rec_parse(canon) == {"job": ("s", JOB), "rung": ("s", "c2"), "run_id": ("s", "20261122T000000-1-1"), "osz_rows": ("s", "7"), "recorded_s": ("i", 5)},
       "REC1: 러너 꼴 한 줄 기록 → 칸 · 꼴 그대로")
    ck(rec_parse(json.dumps(kj, separators=(",", ":")).encode()) == rec_parse(canon), "Codex EO P1: 콜론 뒤 공백 없는 유효 JSON → 같게 읽는다 (러너도)")
    ck(rec_parse(canon.replace(b', "rung"', b' "rung"', 1)) is None, "⛔음성 Codex EO P1: 쉼표 하나 유실 → 거부 (러너도)")
    ck(rec_parse(canon.replace(b'"c2"', b'"c2\x1b[0m"', 1)) is None and rec_parse(canon.replace(b'"c2"', b'"c2\\u001b[0m"', 1)) is not None,
       "⛔음성 날것 ESC → 거부 · 이스케이프한 ESC (\\u001b) → 받음")
    ck(rec_parse(canon.replace(b', "rung"', b', "osz_rows": "1", "rung"', 1)) is None and rec_parse(canon.replace(b"\n", b"\n\n")) is None
       and rec_parse(canon.replace(b"5}", b"5.0}")) is None and rec_parse(canon.replace(b"5}", b"05}")) is None and rec_parse(b"{}") is None,
       "⛔음성 같은 키 두 번 · 두 줄 · 실수 · 선행 0 · 빈 객체 → 거부")
    p40 = "".join(f"DAV: {k:4d}   {-731 + 0.002 * math.sin(k):.12E}   2.0E-04   1.0E-05  8000   0.3E-03  0.3E-01\n" for k in range(1, 121))
    s_, w_ = secondary_numbers(p40, "c1")
    E_ = [-731 + 0.002 * math.sin(k) for k in range(1, 121)]
    r_ = max(E_[-50:]) - min(E_[-50:]); sh_ = abs(sum(E_[-50:]) / 50 - sum(E_[-100:-50]) / 50)
    ck(s_ and abs(s_["u_E_eV"] - max(r_, sh_)) < 1e-9 and s_["n_steps"] == 120, f"보조 숫자 u_E = max(폭 · 평균 이동) — {s_}")
    dr = "".join(f"DAV: {k:4d}   {-731 - 0.0005 * k:.12E}   -5.0E-04   1.0E-05  8000   0.3E-03  0.3E-01\n" for k in range(1, 121))
    s2_, _ = secondary_numbers(dr, "c1")
    ck(s2_ and abs(s2_["mean_shift_eV"] - 0.025) < 1e-6 and s2_["u_E_eV"] == s2_["mean_shift_eV"] and s2_["W1_range_eV"] < s2_["mean_shift_eV"],
       "⛔음성 드리프트: 창 안 폭보다 평균 이동이 커서 u_E 가 이동을 잡는다")
    ck(secondary_numbers(p40[: p40.index("DAV:   99")], "c1")[0] is None, "⛔음성 스텝 < 100 → 보조 숫자 거부")
    for st_ in ("A5", "a4A", "r1B"):
        ck(secondary_numbers(p40, st_)[0] is None and "c1 · c2 에만" in secondary_numbers(p40, st_)[1], f"⛔음성 보조 기준을 {st_} 에 적용 → 거부")
    ck(secondary_numbers(p40.replace("DAV:", "SDA:"), "c1")[0] is None, "⛔음성 c1 에 SDA 행이면 보조 숫자도 거부 (관문)")
    hx = "\n".join([" eigenvalues of (default mixing * dielectric matrix)", "  average eigenvalue GAMMA=   0.6", "  " + " ".join(["0.6"] * 44), "",
                    " eigenvalues of (default mixing * dielectric matrix)", "  average eigenvalue GAMMA=   0.6", "  " + " ".join(["0.6"] * 40), ""])
    ck(hist_max(hx) == 44, f"이력 길이 = 고유값 개수 최댓값 (44 → 40 → 44) — {hist_max(hx)}")
    rj = "".join(f"DAV: {k:4d}   -7.31E+02   1E-04   1E-05  8000   0.3E-03  {(30.0 if k == 50 else 0.03):.3E}\n" for k in range(1, 61))
    ck(rms_jumps(rj, "c1") == [50], f"rms(c) 급등 스텝 = 50 — {rms_jumps(rj, 'c1')}")
    before = dict(R2.RUNG_DIFF)
    vt = variant_text("NELM = 200\nLDIPOL = .TRUE.\n", "A5c")
    ck(R2.RUNG_DIFF == before and "LDIPOL = .FALSE." in vt and "MAXMIX = 200" in vt, "variant_text: 2차 rung_text 를 쓰고 RUNG_DIFF 를 되돌린다 (새지 않음)")
    ck(raises(lambda: verify_variant("NELM = 200\n", variant_text("NELM = 200\n", "c1") + "BMIX = 0.01\n", "c1")),
       "⛔음성 변형에 등록 밖 태그 (BMIX) 가 더해지면 빌드 거부")
    ck(raises(lambda: verify_variant("NELM = 200\n", variant_text("NELM = 200\n", "c1").replace("MAXMIX = 200", "MAXMIX = 120"), "c1")),
       "⛔음성 변형 값이 등록과 다르면 (MAXMIX 120) 빌드 거부")
    ck(raises(lambda: _patch("abc", "x", "y")), "⛔음성 러너 부품 패치 자리가 없으면 PkgError")
    txt = run_a5_text()
    ck(_bash_ok(txt) and "judge_r2(){" in txt and 'osz_feed "$d" |' in txt and "a5_return" in txt and "round2_return" not in txt and "run/w0_check.json" in txt
       and "run/start_point.json" in txt and "run/final.json" in txt and "elig_A" not in txt,
       "러너 = 2차 부품 (판정 · 포장) + a5 · bash -n 통과 · 반송 이름 a5_return · ⓪ · 시작점 · 끝 기록 포장 · 2차 elig_A 대신 a5 elig5")
    # ①b 설정 에코 관문 (러너 echo5 와 같은 부분집합)
    def oc(nelm=400, ialgo=38, amix="0.10", amin="0.01", maxmix="200", time_="0.40", ldip="T", echo="", drop=()):
        L = [f"   NELM   =    {nelm};   NELMIN=  6; NELMDL=  0     # of ELM steps", f"   IALGO  =     {ialgo}    algorithm",
             f"     AMIX     = {amix};   BMIX     =  1.00", "     AMIX_MAG =   1.60;   BMIX_MAG =  1.00", f"     AMIN     = {amin}",
             f"     WC   =   100.;   INIMIX=   1;  MIXPRE=   1;  MAXMIX= {maxmix}", f"   TIME   = {time_}     timestep for ELM",
             "   RTIME   =   -0.100 relaxation time in fs", f"   LDIPOL =      {ldip}    correct potential (dipole corrections)",
             " initial mixing is a Kerker type mixing with AMIX =  0.4000 and BMIX =      1.0000"]
        L = [x for x in L if not any(x.lstrip().startswith(d_) for d_ in drop)]
        return " vasp.5.4.4\n INCAR:\n" + echo + " POTCAR:    PAW_PBE Li_sv 10Sep2004\n" + "\n".join(L) + "\n"
    eprobes = {"c1_ok": (oc(), "c1"), "c1_mx45": (oc(maxmix="-45"), "c1"), "c1_amix": (oc(amix="0.40"), "c1"), "c1_nelm": (oc(nelm=300), "c1"),
               "c1_echo_only": (oc(echo="   MAXMIX = -45\n   NELM = 1\n   LDIPOL = .FALSE.\n"), "c1"), "c1_nomx": (oc(drop=("WC",), echo="   MAXMIX = 200\n"), "c1"),
               "c2_ok": (oc(ialgo=58, amix="0.40", amin="0.10", maxmix="-45", time_="0.10"), "c2"), "c2_time": (oc(ialgo=58, time_="0.40"), "c2"),
               "c2_ialgo": (oc(ialgo=38, time_="0.10"), "c2"), "A5c_ok": (oc(nelm=300, ldip="F"), "A5c"), "A5f_dots": (oc(nelm=300, ldip=".FALSE."), "A5f"),
               "A5c_ldip": (oc(nelm=300, ldip="T"), "A5c"), "c1_nan": (oc(amin="NaN"), "c1"), "c1_empty": ("", "c1")}
    keys = lambda m, b: sorted(set(m) | {x.split(" ")[0] for x in b})
    ck(echo5(*eprobes["c1_ok"]) == ([], []) and echo5(*eprobes["c2_ok"]) == ([], []) and echo5(*eprobes["A5c_ok"]) == ([], [])
       and echo5(*eprobes["A5f_dots"]) == ([], []) and echo5(*eprobes["c1_echo_only"]) == ([], []), "설정 에코: 맞는 OUTCAR 해석값 → 통과 (입력 에코 구획의 틀린 값은 안 본다)")
    for k_, want_ in (("c1_mx45", ["MAXMIX"]), ("c1_amix", ["AMIX"]), ("c1_nelm", ["NELM"]), ("c1_nomx", ["MAXMIX"]), ("c2_time", ["TIME"]), ("c2_ialgo", ["IALGO"]),
                      ("A5c_ldip", ["LDIPOL"]), ("c1_nan", ["AMIN"])):
        ck(keys(*echo5(*eprobes[k_])) == want_, f"⛔음성 설정 에코 {k_} → {want_} 에 걸린다 (받음 {echo5(*eprobes[k_])})")
    # ② 묶음 + 러너 끝까지 (가짜 VASP)
    with tempfile.TemporaryDirectory() as T:
        potd = os.path.join(T, "pot")
        titels = {"Li_sv": "PAW_PBE Li_sv 10Sep2004", "P": "PAW_PBE P 06Sep2000", "S": "PAW_PBE S 06Sep2000", "Cl": "PAW_PBE Cl 06Sep2000", "Ag": "PAW_PBE Ag 02Apr2005"}
        zval = {"Li_sv": 3.0, "P": 5.0, "S": 6.0, "Cl": 7.0, "Ag": 11.0}
        sp_sha = {}
        for sp, t in titels.items():
            os.makedirs(os.path.join(potd, sp))
            pp = os.path.join(potd, sp, "POTCAR")
            _write(pp, f"  PAW_PBE {sp}\n   VRHFIN =x\n   LEXCH  = PE\n   TITEL  = {t}\n   POMASS =    1.0; ZVAL   =   {zval[sp]:.1f}    mass and valenz\n")
            sp_sha[sp] = _sha(pp)
        reg = {"schema": R2.REG_SCHEMA, "titel": titels, "species_sha256": sp_sha,
               "vasp_version": "vasp.5.4.4.18Apr17-6-g9f103f2a35 (build Aug 19 2022 11:57:46) complex", "restart_read_regex": "the WAVECAR file was read successfully"}
        w0p = os.path.join(T, "w0", "WAVECAR"); os.makedirs(os.path.dirname(w0p)); _fake_wavecar(w0p)
        w0 = {"sha256": _sha(w0p), "size": os.path.getsize(w0p), "NKPTS": "4", "NBANDS": "872", "ENCUT": "650.0"}
        w0_mtime = os.stat(w0p).st_mtime_ns
        pkg = os.path.join(T, "pkg")
        meta, msha = build(pkg, registry=(reg, "c" * 64), w0=w0, check_decision=False)
        ck(raises(lambda: build(pkg, registry=(reg, "c" * 64), w0=w0, check_decision=False)), "⛔음성 비어 있지 않은 폴더에 다시 빌드 → 거부 (덮어쓰지 않음)")
        base = open(os.path.join(REPO, R2.V5_PKG, "jobs", SRC, "INCAR"), encoding="utf-8").read()
        for var in DELTA:
            t = open(os.path.join(pkg, "jobs", JOB, INCAR_OF[var]), encoding="utf-8").read()
            ck({k: v[1] for k, v in R2.semantic_diff(base, t).items()} == DELTA[var], f"묶음 INCAR.{var} 의 의미상 차이 = 등록 집합 정확히")
        fake = os.path.join(T, "fake_vasp.py"); _write(fake, FAKE_VASP5)
        HN = subprocess.run(["bash", "-c", "hostname 2>/dev/null || uname -n"], capture_output=True, text=True).stdout.strip()
        bind = os.path.join(T, "bin"); os.makedirs(bind)
        _write(os.path.join(bind, "cp"), "#!/bin/bash\nlast=\"\"; for a in \"$@\"; do last=$a; done\n"
               "if [ -n \"${FAKE_CP_FAIL:-}\" ]; then case \"$last\" in *_\"$FAKE_CP_FAIL\"/WAVECAR) echo 'cp: No space left on device' >&2; exit 1;; esac; fi\n"
               f"exec {shutil.which('cp')} \"$@\"\n")
        os.chmod(os.path.join(bind, "cp"), 0o755)
        _write(os.path.join(bind, "tar"), "#!/bin/bash\n"           # 끝 포장 실패 흉내 (FAKE_TAR_FAIL=1 이면 묶음 만들기 czf 만 실패 · 읽기 xzf · tzf 는 그대로)
               "if [ -n \"${FAKE_TAR_FAIL:-}\" ] && [ \"${1:-}\" = czf ]; then echo 'tar: write error' >&2; exit 2; fi\n"
               f"exec {shutil.which('tar')} \"$@\"\n")
        os.chmod(os.path.join(bind, "tar"), 0o755)
        _write(os.path.join(bind, "date"), "#!/bin/bash\n"          # 모의 시계 (FAKE_NOW 초 — 같은 초의 별개 실행 둘 · Codex EO P2 재현) · 없으면 그대로
               f"if [ -n \"${{FAKE_NOW:-}}\" ]; then exec {shutil.which('date')} -d \"@$FAKE_NOW\" \"$@\"; fi\nexec {shutil.which('date')} \"$@\"\n")
        os.chmod(os.path.join(bind, "date"), 0o755)
        killer = os.path.join(T, "killer.sh")          # 스케줄러 kill 흉내: 그 단의 VASP 흉내를 끝까지 쓴 뒤 러너 프로세스 묶음 전체를 SIGKILL (attempt.json 없음)
        _write(killer, f"#!/bin/bash\n{py} {fake}; r=$?\ncase \"$(basename \"$PWD\")\" in *_\"${{FAKE_KILL_STAGE:-none}}\") kill -9 -- -$(ps -o pgid= -p $$ | tr -d ' ');; esac\nexit $r\n")
        os.chmod(killer, 0o755)
        failer = os.path.join(T, "failer.sh")          # 그 단에서만 VASP 가 뜨지 않음 (실행 파일 없음 흉내 · rc 127 · 아무것도 안 씀)
        _write(failer, f"#!/bin/bash\ncase \"$(basename \"$PWD\")\" in *_\"${{FAKE_FAIL_STAGE:-none}}\") echo 'vasp_std: command not found'; exit 127;; esac\nexec {py} {fake}\n")
        os.chmod(failer, 0o755)

        def run_pkg(name, plan, w0path=None, env_extra=None, args=(), fresh=True, pk=None, cwd=None, vasp=None, session=False):
            w = os.path.join(T, "w_" + name)
            if fresh:
                shutil.copytree(pk or pkg, w)
            pf = os.path.join(T, f"plan_{name}.json"); _write(pf, json.dumps(plan))
            env = {**os.environ, "PATH": bind + os.pathsep + os.environ.get("PATH", ""), "VASP_CMD": vasp or f"{py} {fake}", "POTCAR_DIR": potd,
                   "W0_WAVECAR": w0path if w0path is not None else w0p, "FAKE_PLAN": pf, "FAKE_PKG": w, "WATCH_S": "1", **(env_extra or {})}
            p = subprocess.run(["bash", os.path.join(w, "run_a5.sh"), *args], cwd=cwd or w, env=env, capture_output=True, text=True, timeout=600,
                               start_new_session=session)
            return w, p.returncode, p.stdout + p.stderr

        def rcmd(w, *args, env_extra=None):
            p = subprocess.run(["bash", os.path.join(w, "run_a5.sh"), *args], cwd=w, env={**os.environ, **(env_extra or {})}, capture_output=True, text=True, timeout=120)
            return p.returncode, p.stdout + p.stderr

        def unpack(w, tag=None):
            ex = os.path.join(T, "ex_" + (tag or os.path.basename(w))); shutil.rmtree(ex, ignore_errors=True); os.makedirs(ex)
            with tarfile.open(os.path.join(w, "a5_return.tgz")) as tf:
                try:
                    tf.extractall(ex, filter="data")
                except TypeError:
                    tf.extractall(ex)
            return ex

        def chk(w, pk=None, ms=None):
            ex = unpack(w)
            return check_return(pk or pkg, ex, ms or msha, reg)[1], ex

        def rechk(ex):
            return check_return(pkg, ex, msha, reg)[1]

        def fcode(w):
            p_ = os.path.join(w, "run", "final.json")
            return json.load(open(p_)).get("code") if os.path.isfile(p_) else None

        def stat_rows(w):
            return [ln.split("\t") for ln in open(os.path.join(w, "run", "status.tsv")).read().splitlines()[1:]]
        D = lambda w, s_: os.path.join(w, "run", f"{JOB}_{s_}")
        prevA = {"status": "SCF_NOT_CONVERGED", "a4_history": {"first_attempt": "SCF_NOT_CONVERGED", "r1": "SCF_NOT_CONVERGED", "a4": "SCF_NOT_CONVERGED"}}
        adopt = lambda r_: V.adopt_a5(prevA, r_, 202.209896)
        # S1: ⓪ 확인 → A5c → c1 수렴 → c2 안 띄움 · 끝 기록 0 · 시작점 A5
        w1, rc1, log1 = run_pkg("s1", {"A5": "conv", "c1": "conv"})
        r1, ex1 = chk(w1)
        ck(rc1 == 0 and not os.path.isdir(D(w1, "c2")) and r1["status"] == "OK" and r1["attempts"]["c1"]["status"] == "OK" and fcode(w1) == 0
           and r1["attempts"]["A5"]["variant"] == "A5c" and r1["start_point"]["from"] == "A5" and r1["start_point_record"]["from"] == "A5",
           f"S1 ⓪→A5c→c1 수렴 · c2 안 띄움 · 끝 기록 0 · 시작점 기록 A5 — rc {rc1} · {r1['status']} {r1.get('why')}")
        ck(r1["attempts"]["A5"]["restart_start"]["honoured"] is True and r1["attempts"]["A5"]["wavecar"]["sha256"] != w0["sha256"],
           "A5 끝 WAVECAR 는 새로 써져 sha 가 달라도 재시작 미이행으로 읽지 않는다 (시작 복사본 sha + 문구만)")
        ck(_sha(w0p) == w0["sha256"] and os.stat(w0p).st_mtime_ns == w0_mtime, "보존 ⓐ 원본은 바뀌지 않았다 (sha · mtime)")
        with tarfile.open(os.path.join(w1, "a5_return.tgz")) as tf:
            mem = tf.getnames()
        ck("run/w0_check.json" in mem and "run/start_point.json" in mem and "run/final.json" in mem and not any(os.path.basename(m) in RETURN_FORBIDDEN for m in mem)
           and f"run/{JOB}_c1/WAVECAR.info" in mem and not any("/.prep_" in m or "/.a5.lock" in m for m in mem),
           "반송 묶음: ⓪ · 시작점 · 끝 기록 포함 · WAVECAR · CHGCAR · POTCAR 본문 · 준비 폴더 · 잠금 없음")
        ck(r1["attempts"]["c1"]["far"]["p_z_eA"] is not None and "far" not in r1["attempts"]["A5"], "정보: c1 far 진단 (dipolmoment · E-fermi) · A5 (쌍극 보정 끔) 에는 없음")
        ck(adopt(r1).get("adopted") == "a5_c1" and adopt(r1)["a5_start_point"]["label"] == "시작점 = A5 끝 WAVECAR",
           "S1 수집기: c1 주 채택 · 채택 기록에 시작점 (A5 끝 WAVECAR · 리뷰 P2(a))")
        # P1-1: 끝난 사다리를 다시 돌리면 아무것도 띄우지 않는다 · 같은 코드 · 포장도 안 다시 한다 · 기록 명령 거부
        tg1 = _sha(os.path.join(w1, "a5_return.tgz"))
        _, rc1b, log1b = run_pkg("s1", {"A5": "conv", "c1": "conv", "c2": "conv"}, fresh=False)
        ck(rc1b == 0 and "이미 끝났다" in open(os.path.join(w1, "run", "env.txt")).read() and not os.path.isdir(D(w1, "c2")) and _sha(os.path.join(w1, "a5_return.tgz")) == tg1
           and len(stat_rows(w1)) == 2, f"⛔음성 끝난 사다리 (c1 OK) 다시 돌림 → 아무것도 안 띄움 · 종료 0 · 반송 묶음 그대로 (리뷰 P1-1) — rc {rc1b}")
        for args_ in (("--infra-abort", "A5", "s", "t", "r"), ("--killed", "c1", "s", "t", "r"), ("--infra-wall", "x", "1"), ("--reset-w0",)):
            rcx, outx = rcmd(w1, *args_, env_extra={"WALL_S": "5"})
            ck(rcx == 2 and "끝났다" in outx, f"⛔음성 끝난 사다리에 기록 명령 {args_[0]} → 거부 (종료 2) — {outx.strip()[-80:]}")
        # 사다리 대조: c1 OK 인데 c2 가 있으면 LADDER_VIOLATION
        exv = unpack(w1, "s1v"); shutil.copytree(os.path.join(exv, "run", f"{JOB}_c1"), os.path.join(exv, "run", f"{JOB}_c2"))
        rv_ = rechk(exv)                                  # 사유 목록 전체에서 그 대조를 찾는다 — c1 이 1 초 넘게 걸리면 시간 순서 위반이 먼저 잡아서
        ck(rv_["status"] == "LADDER_VIOLATION"           # 상태만 보면 돌연변이 m12 (이 대조를 뺌) 가 시각에 따라 살아남는다 (11-22 병렬 돌연변이 실측)
           and any("c2 가 있는데 c1 이 주 기준 OK" in v for v in rv_.get("ladder_violations", [])),
           f"⛔음성 c1 OK 인데 반송에 c2 가 있다 → LADDER_VIOLATION · 사유 목록에 'c1 OK 인데 c2' 대조 — {rv_.get('ladder_violations', [])[:2]}")
        # 시작점 기록 · 끝 기록 · 순서 (반송을 고쳐서)
        exs = unpack(w1, "s1sp"); os.remove(os.path.join(exs, "run", "start_point.json"))
        ck(rechk(exs)["status"] == "START_POINT_MISSING", "⛔음성 c1 이 있는데 시작점 기록이 없다 → START_POINT_MISSING (리뷰 P0-2(b))")
        exs = unpack(w1, "s1sp2"); spj = os.path.join(exs, "run", "start_point.json")
        wrec = json.load(open(os.path.join(exs, "run", "w0_check.json")))
        _write(spj, json.dumps({"from": "W0", "path": w0p, "sha256": w0["sha256"], "head": wrec["head"], "written_s": json.load(open(spj))["written_s"]}))
        rsp = rechk(exs)
        ck(rsp["status"] == "START_POINT_MISMATCH", f"⛔음성 시작점 기록 W0 인데 A5 가 자격 → START_POINT_MISMATCH (규칙과 대조) — {rsp['status']} {rsp.get('why', '')[:80]}")
        _write(spj, "{not json")
        rsf_ = rechk(exs)
        ck(rsf_["status"] == "LADDER_VIOLATION" and any("start_point_form" in v for v in rsf_["ladder_violations"]),
           f"⛔음성 시작점 기록을 못 읽음 → 트리 관문 start_point_form · LADDER_VIOLATION (러너도 종료 8 · Codex EQ — 전에는 START_POINT_MISMATCH) — {rsf_['status']}")
        exf = unpack(w1, "s1fin"); fj = os.path.join(exf, "run", "final.json"); d_ = json.load(open(fj)); d_["code"] = 1; d_["state"] = "NO_PRIMARY"; _write(fj, json.dumps(d_))
        ck(rechk(exf)["status"] == "STOPPED_FOR_REVIEW", "⛔음성 러너 끝 기록 (코드 1) ≠ 기록으로 낸 사다리 판정 (OK) → STOPPED_FOR_REVIEW")
        exo = unpack(w1, "s1ord"); aj_ = os.path.join(exo, "run", f"{JOB}_c1", "attempt.json"); d_ = json.load(open(aj_))
        tA = json.load(open(os.path.join(exo, "run", f"{JOB}_A5", "attempt.json")))["t_end"]
        d_["t_start"] = tA - 50; _write(aj_, json.dumps(d_))
        ro = rechk(exo)
        ck(ro["status"] == "LADDER_VIOLATION" and "순서" in ro["why"], f"⛔음성 c1 시작 < A5 끝 → LADDER_VIOLATION (리뷰 P0-2(a)) — {ro.get('why', '')[:80]}")
        exo2 = unpack(w1, "s1ord2"); ab_ = os.path.join(exo2, "run_aborted", f"{JOB}_A5_1"); os.makedirs(ab_)
        tc1 = json.load(open(os.path.join(exo2, "run", f"{JOB}_c1", "attempt.json")))
        _write(os.path.join(ab_, "attempt.start"), json.dumps({"job": JOB, "attempt": "A5c", "stage": "a5", "run_id": "20261121T000000-1-1", "t_start": tc1["t_start"] + 5}))
        _write(os.path.join(ab_, "OSZICAR"), "       N       E                     dE             d eps       ncg     rms          rms(c)\n")
        _write(os.path.join(ab_, "infra_abort.json"), json.dumps({"job": JOB, "rung": "A5", "wall_s": "5", "recorded_s": tc1["t_end"] + 5}))
        ro2 = rechk(exo2)                                         # 이 반송은 영수증 · 장부도 어긋난다 — 순서 위반 문구가 목록에 있는지까지 본다 (다른 위반에 가려지지 않게)
        ck(ro2["status"] == "LADDER_VIOLATION" and any("순서" in v for v in ro2.get("ladder_violations", [])),
           f"⛔음성 A5 0 스텝 중단 기록이 c1 뒤 → LADDER_VIOLATION (늦은 중단 · 리뷰 P0-2(a)) · 사유 목록에 순서 위반 — {ro2['status']} {ro2.get('ladder_violations', [])[:3]}")
        # S2: c1 정체 (400 스텝) → c2 자동 (SDA/CGA 수렴) · c2 시작 = 같은 A5 WAVECAR
        w2, rc2, log2 = run_pkg("s2", {"A5": "noconv", "c1": "plateau", "c2": "conv"})
        r2, ex2 = chk(w2)
        a5sha = r2["attempts"]["A5"]["wavecar"]["sha256"]
        ck(rc2 == 0 and r2["attempts"]["c1"]["status"] == "SCF_NOT_CONVERGED" and r2["attempts"]["c2"]["status"] == "OK" and r2["status"] == "OK"
           and r2["attempts"]["c2"]["restart"]["record"]["src_sha256"] == a5sha == r2["start_point"]["sha256"],
           f"S2 A5 미수렴이어도 자격 · c1 정체 → c2 (ALGO All · SDA/CGA) 수렴 · c2 시작 = A5 WAVECAR — rc {rc2} · {r2['status']}")
        s2c = r2["attempts"]["c1"]
        ck(s2c.get("secondary", {}).get("n_steps") == 400 and s2c["secondary"]["u_E_eV"] < 0.005 and s2c.get("completeness") == "OK",
           f"S2 c1 보조 숫자 (스텝 400 · u_E 작음 · 완결성 OK) — {s2c.get('secondary')} {s2c.get('completeness')}")
        ck("secondary" not in r2["attempts"]["A5"], "⛔음성 A5 (미수렴) 에는 보조 숫자를 내지 않는다")
        ck(r2["attempts"]["A5"]["history_max"] > 45 and r2["attempts"]["c1"]["history_max"] > 45 and "history_max" not in r2["attempts"]["c2"],
           f"정보: A5 · c1 이력 길이 > 45 (MAXMIX 200 이 먹었다) · c2 (혼합기 없음) 에는 없음 — {r2['attempts']['A5']['history_max']}")
        w4l = [ln for ln in open(os.path.join(D(w2, "c1"), "warn.log")).read().splitlines()] if os.path.isfile(os.path.join(D(w2, "c1"), "warn.log")) else []
        ck(any("history_max" in ln for ln in w4l), f"러너 warn.log 에 이력 길이 정보 한 줄 (정보 · 판정 아님) — {w4l[-2:]}")
        # P0-1: c1 이 주 기준 OK 가 아닌데 c2 가 확인된 끝이 아니면 사다리가 안 끝났다 (반송을 고쳐서 — c2 없음 · 준비만 · 끝 기록 없음 · 끊김 행 0 · 끊김 행 ≥ 1)
        def drop_rows(base_, rung_):                       # 시험 꾸밈: 끝나지 않은 단으로 바꾼 시도의 이력 줄 (status.tsv) 도 지운다 — 실제 그런 반송과 같게 (Codex EP P1 이력 대조)
            sp_ = os.path.join(base_, "run", "status.tsv"); L_ = open(sp_).read().split("\n")
            _write(sp_, "\n".join([L_[0]] + [l_ for l_ in L_[1:] if l_.split("\t")[1:2] != [rung_]]))

        def s2_variant(tag, how):
            exx = unpack(w2, f"s2{tag}"); c2d = os.path.join(exx, "run", f"{JOB}_c2"); drop_rows(exx, "c2")
            if how == "missing":
                shutil.rmtree(c2d)
            elif how == "prep":
                for f_ in os.listdir(c2d):
                    if f_ not in ("INCAR", "POSCAR", "KPOINTS"):
                        os.remove(os.path.join(c2d, f_))
            elif how in ("wait", "killed", "killed0") or how.startswith("killed_"):
                tend = json.load(open(os.path.join(c2d, "attempt.json")))["t_end"]
                os.remove(os.path.join(c2d, "attempt.json"))
                if how == "killed0":
                    _write(os.path.join(c2d, "OSZICAR"), "       N       E                     dE             d eps       ncg     rms          rms(c)\n")
                if how == "killed_hdr":                            # 끊긴 c2 의 행 머리가 그 단의 것이 아님 (Codex EN P0 둘째 줄)
                    oz_ = os.path.join(c2d, "OSZICAR"); _write(oz_, re.sub(r"(?m)^(SDA|CGA):", "XYZ:", open(oz_).read()))
                if how == "killed_ist0":                           # 끊긴 c2 가 시작 WAVECAR 를 안 읽음 (Codex EN P0 첫 줄)
                    oc_ = os.path.join(c2d, "OUTCAR"); t_ = open(oc_).read()
                    t_ = re.sub(r"(?m)^(\s*ISTART =\s*)1(\s+job)", r"\g<1>0\2", t_); _write(oc_, re.sub(r"(?m)^(\s*ICHARG =\s*)0(\s+charge)", r"\g<1>2\2", t_))
                if how != "wait":
                    s0_ = json.load(open(os.path.join(c2d, "attempt.start")))
                    rows_ = row_gate(open(os.path.join(c2d, "OSZICAR")).read(), "c2")[0]
                    kj_ = {"job": JOB, "rung": "c2", "run_id": s0_["run_id"], "wall_s": "100", "sched_job_id": "s", "cancel_utc": "t", "reason": "r",
                           "osz_rows": str(rows_), "recorded_utc": "2026-11-22T00:00:00Z", "recorded_s": tend + 1}
                    kj_.update({"killed_rows": {"osz_rows": str(rows_ - 1)}, "killed_rid": {"run_id": "20261122T000000-1-1"}, "killed_wall": {"wall_s": "0100"},
                                "killed_early": {"recorded_s": s0_["t_start"] - 1}, "killed_rung": {"rung": "c1"}}.get(how, {}))
                    txt_ = json.dumps(kj_) + "\n"
                    if how == "killed_trunc":
                        txt_ = "{"                                 # 반송본의 killed.json 이 한 글자로 잘림 (Codex EN P1 첫 줄)
                    elif how == "killed_dup":                          # 틀린 값이 먼저 · 맞는 값이 뒤 — json.loads 는 뒤 값을 받으니 같은 키 거부가 없으면 통과한다 (러너 kf5 는 빈칸)
                        txt_ = txt_.replace(', "rung"', ', "osz_rows": "1", "rung"')
                    elif how == "killed_multi":                        # 두 줄 (필드는 다 있고 JSON 으로는 읽힌다 — 한 줄 꼴 확인만 잡는다)
                        txt_ = txt_.replace(', "reason"', ',\n "reason"')
                    _write(os.path.join(c2d, "killed.json"), txt_)
            fj_ = os.path.join(exx, "run", "final.json")
            if how == "killed" or how.startswith("killed_"):           # 끝 기록은 그 반송의 시도 목록과 같게 (Codex EO P2 — 검사기가 대조한다)
                _write(fj_, json.dumps({"code": 1, "state": "NO_PRIMARY", "why": "c2 끊김 (시험)", "attempts": attempts_of(exx, meta["jobs"][0]),
                                       "written_utc": "2026-11-22T00:00:00Z", "written_s": 1}))
            elif os.path.exists(fj_):
                os.remove(fj_)                                      # 끝나지 않은 사다리 (포장만 다시 한 반송)
            return rechk(exx)
        for how_, want_ in (("missing", "LADDER_INCOMPLETE"), ("prep", "LADDER_VIOLATION"), ("wait", "LADDER_INCOMPLETE"), ("killed0", "STOPPED_FOR_REVIEW")):   # prep = 시작 기록 없는 c2 폴더 → 트리 관문 no_start (Codex EQ)
            rv_ = s2_variant(how_, how_)
            a_ = adopt(rv_)
            ck(rv_["status"] == want_ and a_.get("adopted") is None, f"⛔음성 c1 정체 · c2 {how_} → {want_} · c1 보조 자동 채택 없음 (리뷰 P0-1) — {rv_['status']} · {a_.get('adopted')}")
        rv_ = s2_variant("killed", "killed"); a_ = adopt(rv_)
        ck(rv_["status"] == "NO_PRIMARY_VALUE" and a_.get("adopted") == "a5_c1" and a_.get("a5_rule") == "secondary",
           f"c1 정체 · c2 행 ≥ 1 끊김 기록 (확인된 끝) → NO_PRIMARY_VALUE · c1 보조 채택 — {rv_['status']} · {a_.get('adopted')}")
        # Codex EN P0 · P1: 끊긴 c2 의 원문 · 기록 모순은 끊김이라도 버리지 않는다 → 1저자 · c1 보조 자동 채택 없음
        for how_, want_st in (("killed_hdr", "SCF_UNVERIFIED"), ("killed_ist0", "RESTART_NOT_HONOURED"), ("killed_trunc", "KILLED_RECORD_MISMATCH"),
                              ("killed_rows", "KILLED_RECORD_MISMATCH"), ("killed_rid", "KILLED_RECORD_MISMATCH"), ("killed_wall", "KILLED_RECORD_MISMATCH"),
                              ("killed_rung", "KILLED_RECORD_MISMATCH"), ("killed_dup", "KILLED_RECORD_MISMATCH"), ("killed_multi", "KILLED_RECORD_MISMATCH"),
                              ("killed_early", "KILLED_RECORD_MISMATCH")):
            rv_ = s2_variant(how_, how_); a_ = adopt(rv_); c2_ = rv_["attempts"]["c2"]
            ok_st = ("STOPPED_FOR_REVIEW",) if how_ in ("killed_hdr", "killed_ist0", "killed_rows") else ("LADDER_VIOLATION",)       # 기록 문법 · 결속 = 트리 관문 (Codex EQ)
            ck(rv_["status"] in ok_st and c2_["status"] == want_st and c2_.get("killed") is True and rv_["classes"]["c2"][0] == "REVIEW" and a_.get("adopted") is None,
               f"⛔음성 Codex EN: c1 정체 · 끊긴 c2 {how_} → c2 {want_st} · {ok_st[0]} · c1 보조 자동 채택 없음 — {rv_['status']} · {c2_['status']} · {a_.get('adopted')}")
        # S3–S5: ⓪ sha · 크기 · 머리 불일치 → A5 새로 (A5f) · 원본 그대로
        for nm, mk in (("s3", "sha"), ("s4", "size"), ("s5", "head")):
            alt = os.path.join(T, f"w0_{nm}", "WAVECAR"); os.makedirs(os.path.dirname(alt))
            if mk == "sha":
                _fake_wavecar(alt, extra=512)
                with open(alt, "r+b") as fh_:                                           # 같은 크기 · 같은 머리 · 다른 sha (본문 한 바이트)
                    fh_.seek(200); fh_.write(b"\x02")
            elif mk == "size":
                _fake_wavecar(alt, extra=513)
            else:
                _fake_wavecar(alt, nb=873)
            m0 = os.stat(alt).st_mtime_ns; h0 = _sha(alt)
            wx, rcx, _ = run_pkg(nm, {"A5": "conv", "c1": "conv"}, w0path=alt)
            rx_, _ = chk(wx)
            ck(rx_["w0"]["verified"] is False and rx_["w0"]["status"] == "OK" and rx_["attempts"]["A5"]["variant"] == "A5f" and rx_["status"] == "OK"
               and _sha(alt) == h0 and os.stat(alt).st_mtime_ns == m0, f"⛔음성 ⓪ {mk} 불일치 → 확인 안 됨 · A5 새로 (A5f) · 원본 그대로 — {rx_['w0'].get('record', {}).get('why')}")
        # S5b · S5c: 기대값만 다른 묶음 — sha 는 같은데 크기만 · 머리만 다르면 그 확인 하나가 잡는다
        for nm, w0x, why_ in (("s5b", {**w0, "size": w0["size"] + 1}, "크기 다름"), ("s5c", {**w0, "NBANDS": "871"}, "머리 (NKPTS·NBANDS·ENCUT) 다름")):
            pkx = os.path.join(T, f"pkg_{nm}"); _, msx = build(pkx, registry=(reg, "c" * 64), w0=w0x, check_decision=False)
            wx, rcx, _ = run_pkg(nm, {"A5": "conv", "c1": "conv"}, pk=pkx)
            rx_, _ = chk(wx, pk=pkx, ms=msx)
            ck(rx_["w0"]["verified"] is False and rx_["w0"]["record"]["why"] == why_ and rx_["attempts"]["A5"]["variant"] == "A5f" and rx_["w0"]["status"] == "OK",
               f"⛔음성 ⓪ sha 는 같고 {why_} → 확인 안 됨 (그 확인 하나가 잡는다) — {rx_['w0'].get('record', {}).get('why')}")
        # P1-3: 경로 — 상대 경로는 부른 곳 기준 · 없는 경로는 기록 없이 종료 2 · 고친 경로로 다시
        wr, rcr, _ = run_pkg("p13a", {"A5": "conv", "c1": "conv"}, w0path=os.path.relpath(w0p, T), cwd=T)
        rr_, _ = chk(wr)
        ck(rcr == 0 and rr_["w0"]["verified"] is True and rr_["attempts"]["A5"]["variant"] == "A5c",
           f"⛔음성 W0 상대 경로 (다른 폴더에서 부름) → 부른 곳 기준으로 풀어 확인됨 · A5c (리뷰 P1-3) — rc {rcr} · {rr_['w0'].get('record', {}).get('why')}")
        wt, rct, logt = run_pkg("p13b", {"A5": "conv", "c1": "conv"}, w0path=w0p + "_typo")
        ck(rct == 2 and not os.path.exists(os.path.join(wt, "run", "w0_check.json")) and not os.path.isdir(D(wt, "A5")) and "없거나 읽을 수 없다" in logt,
           f"⛔음성 W0 경로 오타 (없는 파일) → 기록 없이 종료 2 · A5 안 띄움 (리뷰 P1-3) — rc {rct}")
        _, rct2, _ = run_pkg("p13b", {"A5": "conv", "c1": "conv"}, fresh=False)
        ck(rct2 == 0 and json.load(open(os.path.join(wt, "run", "w0_check.json")))["verified"] == 1, f"고친 경로로 다시 → ⓪ 확인 · 진행 — rc {rct2}")
        # P2(c): 준비 실패 (시작 WAVECAR 복사 중 디스크 참) → 그 단 소모 안 함 · 임시 폴더 지움 · 종료 3 · 고친 뒤 다시
        wc, rcc, logc = run_pkg("p2c", {"A5": "conv", "c1": "conv"}, env_extra={"FAKE_CP_FAIL": "A5"})
        ck(rcc == 3 and not os.path.isdir(D(wc, "A5")) and not any(x.startswith(".prep_") for x in os.listdir(os.path.join(wc, "run")))
           and len(stat_rows(wc)) == 0 and os.path.isfile(os.path.join(wc, "run", "w0_check.json")) and fcode(wc) is None,
           f"⛔음성 A5 준비 실패 (WAVECAR 복사 실패) → 종료 3 · A5 폴더 없음 · 임시 폴더 없음 · 끝 기록 없음 (리뷰 P2(c)) — rc {rcc}")
        rcz, outz = rcmd(wc, "--reset-w0")
        ck(rcz == 0 and not os.path.exists(os.path.join(wc, "run", "w0_check.json")), f"A5 를 띄우기 전이면 --reset-w0 로 ⓪ 기록을 지운다 — {outz.strip()[-60:]}")
        _, rcc2, _ = run_pkg("p2c", {"A5": "conv", "c1": "conv"}, fresh=False, env_extra={"FAKE_CP_FAIL": "c1"})
        spc = json.load(open(os.path.join(wc, "run", "start_point.json")))
        ck(rcc2 == 3 and os.path.isdir(D(wc, "A5")) and not os.path.isdir(D(wc, "c1")) and spc["from"] == "A5",
           f"⛔음성 c1 준비 실패 → 종료 3 · c1 폴더 없음 · 시작점은 이미 기록 (첫 c 단 띄울 때 한 번) — rc {rcc2}")
        rca, outa = rcmd(wc, "--infra-abort", "A5", "s", "t", "r")
        ck(rca == 2 and "뒤 단" in outa, f"⛔음성 시작점 기록이 있으면 A5 0 스텝 중단 기록 거부 (리뷰 P0-2(c)) — {outa.strip()[-70:]}")
        rcz2, outz2 = rcmd(wc, "--reset-w0")
        ck(rcz2 == 2 and "이미 시작" in outz2, "⛔음성 A5 가 시작한 뒤에는 --reset-w0 거부")
        _, rcc3, _ = run_pkg("p2c", {"A5": "conv", "c1": "conv"}, fresh=False)
        rc_, _ = chk(wc)
        ck(rcc3 == 0 and rc_["status"] == "OK" and rc_["start_point"]["from"] == "A5" and json.load(open(os.path.join(wc, "run", "start_point.json"))) == spc,
           f"고친 뒤 다시 → c1 이 기록된 시작점에서 · OK — rc {rcc3} · {rc_['status']}")
        # S6: A5 충돌 (행 ≥ 1) + ⓪ 확인 → c1 은 ⓪ 복사본에서 · 시작점 = 보존 ⓐ
        w6, rc6, _ = run_pkg("s6", {"A5": "crash", "c1": "conv"})
        r6, _ = chk(w6)
        ck(rc6 == 0 and r6["start_point"]["from"] == "W0" and r6["attempts"]["c1"]["restart"]["record"]["src_sha256"] == w0["sha256"] and r6["status"] == "OK"
           and adopt(r6)["a5_start_point"]["label"] == "시작점 = 보존 ⓐ",
           f"⛔음성 A5 자격 미달 (충돌 · 행 7) + ⓪ 확인 → c1 은 ⓪ 복사본에서 · 채택 기록 '시작점 = 보존 ⓐ' — rc {rc6} · {r6['status']} {r6.get('why')}")
        # S7: A5 충돌 + ⓪ 없음 → 값 없음 · c1 안 띄움 · 끝 기록 1 · 다시 돌려도 1
        w7, rc7, _ = run_pkg("s7", {"A5": "crash"}, w0path="none")
        r7, _ = chk(w7)
        _, rc7b, _ = run_pkg("s7", {"A5": "crash"}, w0path="none", fresh=False)
        ck(rc7 == 1 and rc7b == 1 and fcode(w7) == 1 and not os.path.isdir(D(w7, "c1")) and r7["start_point"] is None and r7["status"] == "NO_PRIMARY_VALUE",
           f"⛔음성 A5 자격 미달 + ⓪ 없음 → 값 없음 · c1 안 띄움 · 끝 기록 1 · 다시 돌려도 1 — rc {rc7} {rc7b} · {r7['status']}")
        # S8 · S9 · S9b: c1 재시작 미이행 → 멈춤 8 (c2 안 띄움 · 개정 5 해석 1) · 검사기 STOPPED_FOR_REVIEW · 수집기 채택 없음
        for nm, beh_ in (("s8", "noread"), ("s9", "modwav"), ("s9b", "nophrase")):
            wx, rcx, _ = run_pkg(nm, {"A5": "conv", "c1": beh_, "c2": "conv"})
            rx_, _ = chk(wx)
            hon_ = json.load(open(os.path.join(D(wx, "c1"), "WAVECAR.info"))).get("honoured")
            ck(rcx == 8 and fcode(wx) == 8 and not os.path.isdir(D(wx, "c2")) and rx_["attempts"]["c1"]["status"] == "RESTART_NOT_HONOURED"
               and rx_["status"] == "STOPPED_FOR_REVIEW" and adopt(rx_).get("adopted") is None and hon_ == 0,
               f"⛔음성 c1 재시작 미이행 ({beh_}) → 멈춤 8 · c2 안 띄움 · STOPPED_FOR_REVIEW · 채택 없음 · 반송 기록 WAVECAR.info honoured 0 — rc {rcx} · {rx_['status']} · honoured {hon_}")
        _, rc8b, _ = run_pkg("s8", {"A5": "conv", "c1": "conv", "c2": "conv"}, fresh=False)
        ck(rc8b == 8 and not os.path.isdir(D(os.path.join(T, "w_s8"), "c2")), "⛔음성 멈춤 8 뒤 다시 돌려도 아무것도 안 띄움 · 종료 8")
        w9c, rc9c, _ = run_pkg("s9c", {"A5": "conv", "c1": "plateau", "c2": "modwav"})
        r9c, _ = chk(w9c)
        hon9c = json.load(open(os.path.join(D(w9c, "c2"), "WAVECAR.info"))).get("honoured")
        ck(rc9c == 8 and r9c["attempts"]["c2"]["status"] == "RESTART_NOT_HONOURED" and r9c["status"] == "STOPPED_FOR_REVIEW" and adopt(r9c).get("adopted") is None
           and hon9c == 0,
           f"⛔음성 c2 재시작 미이행 (끝 sha 다름) → 멈춤 8 · STOPPED_FOR_REVIEW (c2 주 기준 미정 → c1 보조 채택 없음) · 반송 기록 honoured 0 (돌연변이 m09) — rc {rc9c} · {r9c['status']} · honoured {hon9c}")
        # P3: c1 OUTCAR NBANDS ≠ 시작 WAVECAR 머리 → 재시작 불완전 · 멈춤 8
        wb, rcb, _ = run_pkg("p3", {"A5": "conv", "c1": "badhead", "c2": "conv"})
        rb_, _ = chk(wb)
        ck(rcb == 8 and not os.path.isdir(D(wb, "c2")) and rb_["attempts"]["c1"]["status"] == "RESTART_NOT_HONOURED" and "온전하지 않다" in rb_["attempts"]["c1"].get("why", ""),
           f"⛔음성 c1 NBANDS 873 ≠ 시작 WAVECAR 872 → 러너 멈춤 8 · 검사기 RESTART_NOT_HONOURED (리뷰 P3) — rc {rcb} · {rb_['attempts']['c1'].get('why', '')[:60]}")
        # P2(d): 잠금 — 이 기계 · 살아 있음 / 이 기계 · 죽음 / 다른 기계
        w9d = os.path.join(T, "w_s9d"); shutil.copytree(pkg, w9d); os.makedirs(os.path.join(w9d, "run", ".a5.lock"))
        _write(os.path.join(w9d, "run", ".a5.lock", "owner"), f"{HN} {os.getpid()}\n")
        _, rc9d, log9d = run_pkg("s9d", {"A5": "conv", "c1": "conv"}, fresh=False)
        pab, oab = rcmd(w9d, "--infra-abort", "A5", "s", "t", "r")
        ck(rc9d == 2 and "돌고 있다" in log9d and not os.path.isdir(D(w9d, "A5")) and pab == 2 and "돌고 있다" in oab,
           f"⛔음성 이 기계의 살아 있는 잠금 → 계산 · 기록 명령 거부 (종료 2) — rc {rc9d} · {pab}")
        dead = subprocess.Popen(["true"]); dead.wait()
        w9e = os.path.join(T, "w_s9e"); shutil.copytree(pkg, w9e); os.makedirs(os.path.join(w9e, "run", ".a5.lock"))
        _write(os.path.join(w9e, "run", ".a5.lock", "owner"), f"{HN} {dead.pid}\n")
        _, rc9e, log9e = run_pkg("s9e", {"A5": "conv", "c1": "conv"}, fresh=False)
        ck(rc9e == 0 and "남은 잠금" in log9e and not os.path.exists(os.path.join(w9e, "run", ".a5.lock")), f"이 기계의 죽은 PID 잠금은 치우고 진행 · 끝나면 잠금을 지운다 — rc {rc9e}")
        w9f = os.path.join(T, "w_s9f"); shutil.copytree(pkg, w9f); os.makedirs(os.path.join(w9f, "run", ".a5.lock"))
        _write(os.path.join(w9f, "run", ".a5.lock", "owner"), "otherhost-n38 4242\n")
        _, rc9f, log9f = run_pkg("s9f", {"A5": "conv", "c1": "conv"}, fresh=False)
        a5_9f = os.path.isdir(D(w9f, "A5"))
        pfa_, ofa_ = rcmd(w9f, "--infra-abort", "A5", "s", "t", "r")
        pw_, ow_ = rcmd(w9f, "--unlock", "otherhost-n38", "999")
        pu_, ou_ = rcmd(w9f, "--unlock", "otherhost-n38", "4242")
        _, rc9f2, _ = run_pkg("s9f", {"A5": "conv", "c1": "conv"}, fresh=False)
        ck(rc9f == 2 and "--unlock otherhost-n38 4242" in log9f and not a5_9f and pfa_ == 2 and pw_ == 2 and pu_ == 0 and rc9f2 == 0,
           f"⛔음성 다른 기계의 잠금 → 살아 있는 것으로 보고 거부 · --unlock 은 주인을 그대로 적어야 · 지운 뒤 진행 (리뷰 P2(d)) — rc {rc9f} · {pw_} · {pu_} · {rc9f2}")
        # P2(g): 다른 묶음 흔적이 있는 폴더 → 종료 2 · 아무것도 안 띄움 · 스케줄러 출력 파일은 둔다
        for nm, mk in (("fx1", "run"), ("fx2", "jobs"), ("fx3", "top"), ("fx4", "aborted")):
            wf = os.path.join(T, f"w_{nm}"); shutil.copytree(pkg, wf)
            if mk == "run":
                os.makedirs(os.path.join(wf, "run", "P2S_S_A_bound")); _write(os.path.join(wf, "run", "P2S_S_A_bound", "attempt.json"), "{}")
            elif mk == "jobs":
                os.makedirs(os.path.join(wf, "jobs", "P2S_S_A_bound"))
            elif mk == "top":
                _write(os.path.join(wf, "run_all.sh"), "#!/bin/bash\n")
            else:
                os.makedirs(os.path.join(wf, "run_aborted", "P2S_S_A_far_A_1"))
            _, rcf, logf = run_pkg(nm, {"A5": "conv", "c1": "conv"}, fresh=False)
            pof = subprocess.run(["bash", os.path.join(wf, "run_a5.sh")], cwd=wf, env={**os.environ, "PACK_ONLY": "1"}, capture_output=True, text=True).returncode
            ck(rcf == 2 and pof == 2 and "새 빈 폴더" in logf and not os.path.isdir(D(wf, "A5")),
               f"⛔음성 묶음 폴더에 a5 가 아닌 것 ({mk}) → 계산 · 포장 거부 (종료 2 · 리뷰 P2(g)) — rc {rcf} · {pof}")
        wf = os.path.join(T, "w_fx5"); shutil.copytree(pkg, wf); _write(os.path.join(wf, "run_a5.sh.o128669"), "sge log\n")
        _, rcf5, _ = run_pkg("fx5", {"A5": "conv", "c1": "conv"}, fresh=False)
        ck(rcf5 == 0, f"스케줄러 출력 파일 (run_a5.sh.o<잡>) 은 두고 진행 — rc {rcf5}")
        # S10: c1 에 SDA 행 → SCF_UNVERIFIED → 멈춤 8 (c2 안 띄움)
        w10, rc10, _ = run_pkg("s10", {"A5": "conv", "c1": "sda_rows", "c2": "conv"})
        r10, _ = chk(w10)
        st10 = [r_ for r_ in stat_rows(w10) if r_[1] == "c1"][0]
        ck(rc10 == 8 and r10["attempts"]["c1"]["status"] == "SCF_UNVERIFIED" and st10[4] == "SCF_UNVERIFIED" and st10[8] == "row_header_SDA"
           and r10["attempts"]["c1"]["judge"]["why"] == "row_header_SDA" and not os.path.isdir(D(w10, "c2")) and r10["status"] == "STOPPED_FOR_REVIEW",
           f"⛔음성 c1 SDA 행 → 러너 · 검사기 둘 다 SCF_UNVERIFIED (row_header_SDA) · 멈춤 8 · c2 안 띄움 — rc {rc10} {st10}")
        # S11 · S12: c2 에 DAV 행 · 모르는 머리 → 멈춤 8
        for nm, beh_, why_ in (("s11", "dav_rows", "row_header_DAV"), ("s12", "unknown_hdr", "row_header_XYZ")):
            wx, rcx, _ = run_pkg(nm, {"A5": "conv", "c1": "plateau", "c2": beh_})
            rx_, _ = chk(wx)
            stx = [r_ for r_ in stat_rows(wx) if r_[1] == "c2"][0]
            ck(rcx == 8 and rx_["attempts"]["c2"]["status"] == "SCF_UNVERIFIED" and stx[8] == why_ == rx_["attempts"]["c2"]["judge"]["why"]
               and rx_["status"] == "STOPPED_FOR_REVIEW" and adopt(rx_).get("adopted") is None,
               f"⛔음성 c2 {beh_} → SCF_UNVERIFIED ({why_}) · 멈춤 8 · c1 보조 채택 없음 — rc {rcx} {stx}")
        # S13: c1 짧은 미수렴 (60 스텝) → 보조 숫자 거부 · 넓은 정체 · 드리프트
        w13, rc13, _ = run_pkg("s13", {"A5": "conv", "c1": "short", "c2": "wide"})
        r13, _ = chk(w13)
        ck(rc13 == 1 and fcode(w13) == 1 and "스텝 60 < 100" in str(r13["attempts"]["c1"].get("secondary", {}).get("refused", "")).replace("전자 스텝", "스텝"),
           f"⛔음성 c1 60 스텝 미수렴 → 보조 숫자 거부 · c2 미수렴 → 종료 1 — {r13['attempts']['c1'].get('secondary')}")
        ck(r13["attempts"]["c2"]["status"] == "SCF_NOT_CONVERGED" and r13["attempts"]["c2"]["secondary"]["u_E_eV"] > 0.1 and r13["status"] == "NO_PRIMARY_VALUE",
           f"넓은 정체 (±0.2 eV) → u_E 가 크다 (수집기가 거부할 값) — {r13['attempts']['c2'].get('secondary')}")
        w14, _, _ = run_pkg("s14", {"A5": "conv", "c1": "drift", "c2": "rmsjump"})
        r14, _ = chk(w14)
        s14 = r14["attempts"]["c1"]["secondary"]
        ck(s14["u_E_eV"] == s14["mean_shift_eV"] and s14["mean_shift_eV"] > s14["W1_range_eV"], f"⛔음성 드리프트 → u_E = 평균 이동 (창 안 폭보다 큼) — {s14}")
        # S15: 누적 상한 — c2 앞에서 넘으면 끝 5 (상한) · 검사기 LADDER_INCOMPLETE · 채택 없음 (리뷰 P0-1)
        w15, rc15, _ = run_pkg("s15", {"A5": "conv", "c1": "plateau", "c2": "conv"})
        shutil.rmtree(D(w15, "c2")); os.remove(os.path.join(w15, "run", "final.json")); drop_rows(w15, "c2")
        os.remove(os.path.join(w15, "a5_return.tgz")); os.remove(os.path.join(w15, "a5_return.tgz.sha256"))        # 완료 반송본이 남으면 트리 관문이 '복구' 로 멈춘다 (Codex EQ)
        aj = os.path.join(D(w15, "c1"), "attempt.json")
        t_ = open(aj).read(); _write(aj, re.sub(r'"elapsed_s": \d+', '"elapsed_s": 700000', t_))
        rid15 = json.loads(t_)["run_id"]; sp15 = os.path.join(w15, "run", "status.tsv")      # 이력 줄도 같은 벽시계 (Codex ER Q-ER-3① — 끝 기록과 이력 줄을 함께 쓴 꼴)
        _write(sp15, "\n".join(("\t".join(l_.split("\t")[:9] + ["700000"] + l_.split("\t")[10:]) if l_.endswith("\t" + rid15) else l_) for l_ in open(sp15).read().split("\n")))
        _, rc15b, log15 = run_pkg("s15", {"A5": "conv", "c1": "plateau", "c2": "conv"}, fresh=False)
        r15, _ = chk(w15)
        _, rc15c, _ = run_pkg("s15", {"A5": "conv", "c1": "plateau", "c2": "conv"}, fresh=False)
        ck(rc15b == 5 and rc15c == 5 and fcode(w15) == 5 and not os.path.isdir(D(w15, "c2")) and "상한" in log15 and r15["status"] == "LADDER_INCOMPLETE"
           and adopt(r15).get("adopted") is None,
           f"⛔음성 누적 > 180 h → c2 안 띄움 · 끝 5 (다시 돌려도 5) · 검사기 LADDER_INCOMPLETE · c1 보조 채택 없음 — rc {rc15b} {rc15c} · {r15['status']}")
        # S16: c1 행 0 → 멈춤 7 (c2 를 쓰지 않는다 · 개정 5 해석 1) · 0 스텝 중단 기록 → 같은 단 다시 · 잡 전체 2 회 상한
        w16, rc16, _ = run_pkg("s16", {"A5": "conv", "c1": "zero"})
        packed16 = os.path.isfile(os.path.join(w16, "a5_return.tgz"))
        subprocess.run(["bash", os.path.join(w16, "run_a5.sh")], cwd=w16, env={**os.environ, "PACK_ONLY": "1"}, capture_output=True, text=True)
        r16, _ = chk(w16)
        ck(rc16 == 7 and fcode(w16) is None and not packed16 and not os.path.isdir(D(w16, "c2")) and r16["status"] == "LADDER_INCOMPLETE"
           and r16["attempts"]["c1"]["status"] == "SCF_UNVERIFIED" and "전자 반복행 0" in r16["attempts"]["c1"]["why"],
           f"⛔음성 c1 행 0 → 멈춤 7 · c2 안 띄움 · 끝 기록 없음 · LADDER_INCOMPLETE — rc {rc16} · {r16['status']}")
        rcw, outw = rcmd(w16, "--reset-w0")
        ck(rcw == 2 and "이미 시작" in outw, "⛔음성 A5 가 있으면 --reset-w0 거부")
        ab = lambda: rcmd(w16, "--infra-abort", "c1", "sched-1", "2026-11-21T00:00:00Z", "node fault")
        p1 = ab()
        ck(p1[0] == 0 and os.path.isdir(os.path.join(w16, "run_aborted", f"{JOB}_c1_1")) and not os.path.isdir(D(w16, "c1"))
           and not os.path.isfile(os.path.join(w16, "run_aborted", f"{JOB}_c1_1", "WAVECAR")), f"0 스텝 인프라 중단 → run_aborted (WAVECAR 복사본 지움) — {p1[1][-120:]}")
        _, rc16b, _ = run_pkg("s16", {"A5": "conv", "c1": "zero"}, fresh=False); p2 = ab()
        _, rc16c, _ = run_pkg("s16", {"A5": "conv", "c1": "zero"}, fresh=False); p3 = ab()
        ck(rc16b == 7 and rc16c == 7 and p2[0] == 0 and p3[0] == 2 and "상한" in p3[1], f"⛔음성 0 스텝 중단 셋째 → 거부 (잡 전체 {INFRA_MAX} 회) — rc {p2[0]} {p3[0]}")
        # P0-2(b): 시작점은 기록에서만 — A5 끝 WAVECAR 가 없어져도 ⓪ 으로 다시 정하지 않는다 (준비 실패 3)
        w16d, _, _ = run_pkg("s16d", {"A5": "conv", "c1": "zero"})
        rcmd(w16d, "--infra-abort", "c1", "s", "2026-11-21T00:00:00Z", "node fault")
        sp16 = json.load(open(os.path.join(w16d, "run", "start_point.json")))
        os.remove(os.path.join(D(w16d, "A5"), "WAVECAR"))
        _, rc16d, _ = run_pkg("s16d", {"A5": "conv", "c1": "conv"}, fresh=False)
        ck(rc16d == 3 and not os.path.isdir(D(w16d, "c1")) and json.load(open(os.path.join(w16d, "run", "start_point.json"))) == sp16 and sp16["from"] == "A5",
           f"⛔음성 c1 다시 돌리기 전에 A5 끝 WAVECAR 가 없어짐 → 시작점 그대로 (A5) · ⓪ 으로 바꾸지 않음 · 준비 실패 3 (리뷰 P0-2(b)) — rc {rc16d}")
        w16e, _, _ = run_pkg("s16e", {"A5": "conv", "c1": "zero"})
        rcmd(w16e, "--infra-abort", "c1", "s", "2026-11-21T00:00:00Z", "node fault")
        _, rc16e, _ = run_pkg("s16e", {"A5": "conv", "c1": "conv"}, fresh=False)
        r16e, _ = chk(w16e)
        ck(rc16e == 0 and r16e["status"] == "OK" and r16e["start_point"]["from"] == "A5" and r16e["attempts"]["c1"]["restart"]["record"]["src_sha256"] == r16e["attempts"]["A5"]["wavecar"]["sha256"],
           f"c1 0 스텝 중단 뒤 다시 → 기록된 시작점 (A5) 에서 · OK — rc {rc16e} · {r16e['status']}")
        # P2(f): c1 VASP 가 아예 안 뜸 (rc 127 · 출력 없음) → 행 0 이 재시작 확인보다 먼저 → 멈춤 7 (8 아님) · 검사기 SCF_UNVERIFIED (재시작 미이행 아님)
        wn, rcn, logn = run_pkg("p2f", {"A5": "conv", "c1": "conv"}, vasp=failer, env_extra={"FAKE_FAIL_STAGE": "c1"})
        _, rcn2, _ = run_pkg("p2f", {}, fresh=False, vasp=failer, env_extra={"FAKE_FAIL_STAGE": "c1"})
        rcp = subprocess.run(["bash", os.path.join(wn, "run_a5.sh")], cwd=wn, env={**os.environ, "PACK_ONLY": "1"}, capture_output=True, text=True).returncode
        rn_, _ = chk(wn)
        ck(rcn == 7 and rcn2 == 7 and rcp == 0 and rn_["attempts"]["c1"]["status"] == "SCF_UNVERIFIED" and rn_["status"] == "LADDER_INCOMPLETE" and "rc 127" in open(os.path.join(wn, "run", "env.txt")).read(),
           f"⛔음성 c1 VASP 안 뜸 (rc 127) → 멈춤 7 (재시작 미이행 8 이 아니다) · 검사기 SCF_UNVERIFIED · LADDER_INCOMPLETE (리뷰 P2(f)) — rc {rcn} · {rn_['attempts']['c1']['status']}")
        wa, rca5, _ = run_pkg("p2fa", {"A5": "conv"}, vasp=failer, env_extra={"FAKE_FAIL_STAGE": "A5"})
        ck(rca5 == 7 and not os.path.isdir(D(wa, "c1")) and not os.path.isdir(D(wa, "c2")), f"⛔음성 A5 VASP 안 뜸 → 멈춤 7 · c1 · c2 를 쓰지 않는다 (개정 5 해석 1) — rc {rca5}")
        # 끊긴 시도 (스케줄러가 러너째 죽임): 행 ≥ 1 이면 --killed 뒤 다음 단 · 0 스텝 중단으로는 거부 · 뒤 단이 있으면 거부
        wk, rck, _ = run_pkg("kill1", {"A5": "conv", "c1": "plateau", "c2": "conv"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c1"}, session=True)
        ck(not os.path.isfile(os.path.join(D(wk, "c1"), "attempt.json")) and os.path.isfile(os.path.join(D(wk, "c1"), "OSZICAR")) and os.path.isfile(os.path.join(D(wk, "A5"), "WAVECAR")),
           f"시험 준비: c1 이 러너째 끊김 (attempt.json 없음 · A5 끝 WAVECAR 남음) — rc {rck}")
        pz = rcmd(wk, "--infra-abort", "c1", "s", "t", "r")
        _, rck2, logk2 = run_pkg("kill1", {"A5": "conv", "c1": "plateau", "c2": "conv"}, fresh=False)
        os.makedirs(D(wk, "c2")); _write(os.path.join(D(wk, "c2"), "attempt.start"), json.dumps({"job": JOB, "attempt": "c2", "stage": "a5", "run_id": "20261121T000000-1-1", "t_start": 5, "kernel_sha256": ""}) + "\n")
        pkl = rcmd(wk, "--killed", "c1", "s", "t", "r", env_extra={"WALL_S": "100"}); shutil.rmtree(D(wk, "c2"))
        pk0 = rcmd(wk, "--killed", "c1", "s", "t", "r")
        pk1 = rcmd(wk, "--killed", "c1", "sched-9", "2026-11-21T00:00:00Z", "walltime", env_extra={"WALL_S": "100"})
        pk2 = rcmd(wk, "--killed", "c1", "sched-9", "2026-11-21T00:00:00Z", "walltime", env_extra={"WALL_S": "100"})
        _, rck3, _ = run_pkg("kill1", {"A5": "conv", "c1": "plateau", "c2": "conv"}, fresh=False)
        rk_, _ = chk(wk)
        ck(pz[0] == 2 and "0 스텝 중단이 아니다" in pz[1] and rck2 == 5 and "--killed c1" in logk2 and fcode(wk) == 0 and pkl[0] == 2 and "뒤 단" in pkl[1]
           and pk0[0] == 2 and pk1[0] == 0 and pk2[0] == 2 and rck3 == 0 and rk_["status"] == "OK" and rk_["attempts"]["c1"]["status"] == "INCOMPLETE_ATTEMPT" and rk_["attempts"]["c1"]["killed"],
           f"⛔음성 c1 끊김 (행 400): 0 스텝 중단 거부 · 다시 돌리면 멈춤 5 · 뒤 단이 있으면 --killed 거부 · WALL_S 없으면 거부 · 기록 뒤 c2 · 두 번 기록 거부 — "
           f"{pz[0]} {rck2} {pkl[0]} {pk0[0]} {pk1[0]} {pk2[0]} {rck3} · {rk_['status']}")
        wk2, _, _ = run_pkg("kill2", {"A5": "conv", "c1": "plateau", "c2": "plateau"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c2"}, session=True)
        rcmd(wk2, "--killed", "c2", "sched-9", "2026-11-21T00:00:00Z", "walltime", env_extra={"WALL_S": "100"})
        _, rck4, _ = run_pkg("kill2", {"A5": "conv", "c1": "plateau", "c2": "plateau"}, fresh=False)
        rk2, _ = chk(wk2)
        ak2 = adopt(rk2)
        ck(rck4 == 1 and rk2["status"] == "NO_PRIMARY_VALUE" and ak2.get("adopted") == "a5_c1" and ak2.get("a5_rule") == "secondary",
           f"c2 끊김 (행 ≥ 1 · --killed) = 확인된 끝 → 종료 1 · NO_PRIMARY_VALUE · c1 보조 채택 가능 — rc {rck4} · {rk2['status']} · {ak2.get('adopted')}")
        wk3, _, _ = run_pkg("kill3", {"A5": "conv", "c1": "zero"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c1"}, session=True)
        pk3 = rcmd(wk3, "--killed", "c1", "s", "t", "r", env_extra={"WALL_S": "100"})
        pk4 = rcmd(wk3, "--infra-abort", "c1", "s", "2026-11-21T00:00:00Z", "node fault")
        ck(pk3[0] == 2 and "전자 반복행 0" in pk3[1] and pk4[0] == 0, f"⛔음성 행 0 끊김 → --killed 거부 · --infra-abort 로만 — {pk3[0]} {pk4[0]}")
        # ── Codex EN P0: c2 가 재시작에 실패하거나 c2 의 것이 아닌 행을 남긴 뒤 스케줄러에 끊김 (7 행) → --killed → 다시 돌림 = 끝까지 판정했을 때와 같은 멈춤 8 ──
        for tag_, beh_, want_ in (("ken1", "istart0@7", "RESTART_NOT_HONOURED"), ("ken2", "unknown_hdr@7", "SCF_UNVERIFIED"),
                                  ("ken3", "nophrase@7", "RESTART_NOT_HONOURED"), ("ken4", "badhead@7", "RESTART_NOT_HONOURED"),
                                  ("ken5", "istart0p@7", "RESTART_NOT_HONOURED")):
            wq, _, _ = run_pkg(tag_, {"A5": "conv", "c1": "plateau", "c2": beh_}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c2"}, session=True)
            pq = rcmd(wq, "--killed", "c2", "sched-9", "2026-11-22T00:00:00Z", "walltime", env_extra={"WALL_S": "100"})
            _, rcq, logq = run_pkg(tag_, {"A5": "conv", "c1": "plateau", "c2": beh_}, fresh=False)
            rq, _ = chk(wq); aq = adopt(rq)
            hdr_ = tag_ == "ken2"                                  # 남의 머리 (XYZ) 7 행 = 완전한 행 0 · 행 판독 row_header_XYZ → --killed 는 기록하지 않고 (종료 2) 다시 돌리면 끝 기록 없이도 8 (Codex EO P0)
            ck((pq[0] == 2 and "row_header_XYZ" in pq[1] if hdr_ else pq[0] == 0) and rcq == 8 and fcode(wq) == 8 and f"c2 {want_}" in logq
               and rq["status"] == "STOPPED_FOR_REVIEW" and rq["attempts"]["c2"]["status"] == want_ and rq["classes"]["c2"][0] == "REVIEW"
               and rq["attempts"]["c2"].get("killed") is (not hdr_) and aq.get("adopted") is None,
               f"⛔음성 Codex EN P0: c2 {beh_} 끊김 (7 행) → --killed → 다시 돌림 종료 8 ({want_}) · 검사기 STOPPED_FOR_REVIEW · 채택 없음 — "
               f"--killed {pq[0]} · rc {rcq} · {rq['status']} · {rq['attempts']['c2']['status']} · {aq.get('adopted')}")
        # 양성 대조: c2 가 c2 행 머리 · 재시작 증거를 다 남긴 채 7 행에서 끊김 → --killed → 확인된 끝 → 종료 1 · c1 보조 채택 (끊김 경로를 막지 않는다)
        wkb, _, _ = run_pkg("kill2b", {"A5": "conv", "c1": "plateau", "c2": "plateau@7"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c2"}, session=True)
        pkb = rcmd(wkb, "--killed", "c2", "sched-9", "2026-11-22T00:00:00Z", "walltime", env_extra={"WALL_S": "100"})
        kb_base = os.path.join(T, "kill2b_base"); shutil.copytree(wkb, kb_base, symlinks=True)        # 다시 돌리기 전 상태 (아래 killed.json 손상 시험의 원본)
        _, rckb, _ = run_pkg("kill2b", {"A5": "conv", "c1": "plateau", "c2": "plateau@7"}, fresh=False)
        rkb, _ = chk(wkb); akb = adopt(rkb)
        ck(pkb[0] == 0 and rckb == 1 and rkb["status"] == "NO_PRIMARY_VALUE" and rkb["attempts"]["c2"]["status"] == "INCOMPLETE_ATTEMPT" and rkb["attempts"]["c2"]["osz_rows"] == 7
           and akb.get("adopted") == "a5_c1" and akb.get("a5_rule") == "secondary",
           f"Codex EN 양성 대조: c2 7 행 끊김 (행 머리 · 재시작 증거 온전) → --killed → 종료 1 · NO_PRIMARY_VALUE · c1 보조 채택 — rc {rckb} · {rkb['status']} · {akb.get('adopted')}")
        # Codex EN P1: 러너도 killed.json 을 그 시도와 대조한다 (잘림 · 행 수 · run_id · 단 · 초 꼴 · 기록 시각 · 같은 키 두 번 · 여러 줄) → 멈춤 8
        kbk = os.path.join(kb_base, "run", f"{JOB}_c2", "killed.json"); kb0 = json.loads(open(kbk).read())
        for i_, (lab_, txt_) in enumerate((("한 글자", "{"), ("행 수 6", json.dumps({**kb0, "osz_rows": "6"})), ("run_id 다름", json.dumps({**kb0, "run_id": "20261122T000000-1-1"})),
                                         ("단 c1", json.dumps({**kb0, "rung": "c1"})), ("초 0100", json.dumps({**kb0, "wall_s": "0100"})),
                                         ("기록 시각 < 시작", json.dumps({**kb0, "recorded_s": 1000})),
                                         ("같은 키 두 번", json.dumps(kb0).replace(', "recorded_utc"', ', "osz_rows": "7", "recorded_utc"')),
                                         ("두 줄", json.dumps(kb0).replace(', "reason"', ',\n "reason"')))):
            wv = os.path.join(T, f"w_kv{i_}"); shutil.copytree(kb_base, wv, symlinks=True); _write(os.path.join(wv, "run", f"{JOB}_c2", "killed.json"), txt_ + "\n")
            _, rcv, logv = run_pkg(f"kv{i_}", {"A5": "conv", "c1": "plateau", "c2": "plateau@7"}, fresh=False)
            ok_ = (fcode(wv) == 8 and "KILLED_RECORD_MISMATCH" in logv) if lab_ == "행 수 6" else (fcode(wv) is None and "트리 관문" in logv and "killed" in logv)
            ck(rcv == 8 and ok_, f"⛔음성 Codex EN P1 러너: killed.json {lab_} → 멈춤 8 ({'KILLED_RECORD_MISMATCH · 끝 기록 8' if lab_ == '행 수 6' else '트리 관문 · 아무것도 안 씀'}) — rc {rcv} · 끝 기록 {fcode(wv)}")
        # Codex EN P1: run_aborted 의 시도에는 읽을 수 있는 중단 영수증 (기록 시각) 이 있어야 한다 — 빠지면 순서 대조가 attempt.json 끝 시각으로만 돈다
        wr, rcr1, _ = run_pkg("rcpt", {"A5": "zero"})
        prc = rcmd(wr, "--infra-abort", "A5", "sched-3", "2026-11-22T00:00:00Z", "node fault")
        _, rcr2, _ = run_pkg("rcpt", {"A5": "conv", "c1": "conv"}, fresh=False)
        rr0, exr = chk(wr)
        ck(rcr1 == 7 and prc[0] == 0 and rcr2 == 0 and rr0["status"] == "OK" and rr0["aborted"] == [["A5@aborted1", "SCF_UNVERIFIED"]],
           f"영수증 양성 대조: A5 행 0 → --infra-abort → 다시 → OK (중단 영수증 온전) — {rcr1} {prc[0]} {rcr2} · {rr0['status']} {rr0.get('why')}")
        rp_ = os.path.join("run_aborted", f"{JOB}_A5_1", "infra_abort.json")
        r0_ = json.loads(open(os.path.join(exr, rp_)).read())
        for lab_, txt_ in (("없음", None), ("한 글자", "{"), ("단 다름", json.dumps({**r0_, "rung": "c1"})), ("기록 시각 글자", json.dumps({**r0_, "recorded_s": str(r0_["recorded_s"])})),
                           ("기록 시각 없음", json.dumps({k: v for k, v in r0_.items() if k != "recorded_s"})), ("초 꼴", json.dumps({**r0_, "wall_s": "5s"}))):
            exv = os.path.join(T, f"ex_rcpt_{abs(hash(lab_))}"); shutil.rmtree(exv, ignore_errors=True); shutil.copytree(exr, exv)
            if txt_ is None:
                os.remove(os.path.join(exv, rp_))
            else:
                _write(os.path.join(exv, rp_), txt_ + "\n")
            rv_ = rechk(exv)
            ck(rv_["status"] == "LADDER_VIOLATION" and "중단 영수증" in rv_["why"] and adopt(rv_).get("adopted") is None,
               f"⛔음성 Codex EN P1: run_aborted A5 중단 영수증 {lab_} → LADDER_VIOLATION · 채택 없음 — {rv_['status']} {rv_.get('why', '')[:80]}")
        # Codex EN P1: c1 행 0 → --infra-abort 로 보존 → start_point.json 만 유실 → 다시 돌려도 시작점을 다시 쓰지 않는다 (멈춤 8 · 검사기 START_POINT_MISSING)
        wsp, rcs1, _ = run_pkg("splost", {"A5": "conv", "c1": "zero"})
        psp = rcmd(wsp, "--infra-abort", "c1", "sched-4", "2026-11-22T00:00:00Z", "node fault")
        sp_base = os.path.join(T, "splost_base"); shutil.copytree(wsp, sp_base, symlinks=True)
        os.remove(os.path.join(wsp, "run", "start_point.json"))
        _, rcs2, logs2 = run_pkg("splost", {"A5": "conv", "c1": "conv"}, fresh=False)
        rsp, _ = chk(wsp)
        ck(rcs1 == 7 and psp[0] == 0 and rcs2 == 8 and fcode(wsp) == 8 and "시작점 기록이 없다" in logs2 and not os.path.isfile(os.path.join(wsp, "run", "start_point.json"))
           and not os.path.isdir(D(wsp, "c1")) and rsp["status"] == "START_POINT_MISSING" and adopt(rsp).get("adopted") is None,
           f"⛔음성 Codex EN P1: c1 0 스텝 중단 뒤 start_point.json 유실 → 다시 쓰지 않고 멈춤 8 · c1 안 띄움 · START_POINT_MISSING — rc {rcs2} · {rsp['status']}")
        # 양성 대조: 유실 없이 다시 → c1 수렴 → OK (시작점 기록 시각 ≤ 첫 c 단 시작)
        wso = os.path.join(T, "w_spok"); shutil.copytree(sp_base, wso, symlinks=True)
        _, rco, _ = run_pkg("spok", {"A5": "conv", "c1": "conv"}, fresh=False)
        rso, exso = chk(wso)
        ck(rco == 0 and rso["status"] == "OK" and rso["aborted"] == [["c1@aborted1", "SCF_UNVERIFIED"]],
           f"시작점 양성 대조: c1 0 스텝 중단 → --infra-abort → 다시 → OK (시작점 기록 그대로) — rc {rco} · {rso['status']} {rso.get('why')}")
        # 검사기: 시작점 기록 시각이 첫 c 단 (run_aborted 포함) 시작보다 늦으면 보류 — 옛 러너가 유실 뒤 다시 쓴 기록 (Codex EN P1 재현의 '2 초 늦음')
        spj = os.path.join(exso, "run", "start_point.json"); sp0 = json.loads(open(spj).read())
        c1a0 = json.loads(open(os.path.join(exso, "run_aborted", f"{JOB}_c1_1", "attempt.start")).read())["t_start"]
        for lab_, rec_ in (("첫 c1 보다 2 초 늦음", {**sp0, "written_s": c1a0 + 2}), ("기록 시각 글자", {**sp0, "written_s": str(sp0["written_s"])}),
                           ("기록 시각 없음", {k: v for k, v in sp0.items() if k != "written_s"})):
            exv = os.path.join(T, f"ex_spw_{abs(hash(lab_))}"); shutil.rmtree(exv, ignore_errors=True); shutil.copytree(exso, exv)
            _write(os.path.join(exv, "run", "start_point.json"), json.dumps(rec_) + "\n")
            rv_ = rechk(exv)
            ck(rv_["status"] == "LADDER_VIOLATION" and "시작점 기록" in rv_["why"] and adopt(rv_).get("adopted") is None,
               f"⛔음성 Codex EN P1 검사기: 시작점 {lab_} → LADDER_VIOLATION · 채택 없음 — {rv_['status']} {rv_.get('why', '')[:80]}")
        # 러너 가드: A5 · c1 이 없는데 run_aborted 에 뒤 단이 있으면 (시작점 · run/ 의 뒤 단이 없어도) 띄우지 않고 멈춤 8
        wg1 = os.path.join(T, "w_ga5"); shutil.copytree(sp_base, wg1, symlinks=True)
        shutil.rmtree(D(wg1, "A5")); os.remove(os.path.join(wg1, "run", "start_point.json")); drop_rows(wg1, "A5c"); drop_rows(wg1, "A5f")
        _, rcg1, _ = run_pkg("ga5", {"A5": "conv", "c1": "conv"}, fresh=False)
        ck(rcg1 == 8 and fcode(wg1) == 8 and not os.path.isdir(D(wg1, "A5")) and not os.path.isdir(D(wg1, "c1")),
           f"⛔음성 Codex EN P1 러너: A5 없음 · run_aborted 에 c1 → A5 를 다시 띄우지 않고 멈춤 8 — rc {rcg1}")
        wg2, rcg2a, _ = run_pkg("gc1", {"A5": "conv", "c1": "plateau", "c2": "zero"})
        pg2 = rcmd(wg2, "--infra-abort", "c2", "sched-5", "2026-11-22T00:00:00Z", "node fault")
        shutil.rmtree(D(wg2, "c1")); drop_rows(wg2, "c1")
        _, rcg2, _ = run_pkg("gc1", {"A5": "conv", "c1": "plateau", "c2": "zero"}, fresh=False)
        ck(rcg2a == 7 and pg2[0] == 0 and rcg2 == 8 and fcode(wg2) == 8 and not os.path.isdir(D(wg2, "c1")),
           f"⛔음성 Codex EN P1 러너: c1 없음 · run_aborted 에 c2 → c1 을 띄우지 않고 멈춤 8 — {rcg2a} {pg2[0]} rc {rcg2}")
        # Codex EN P1: 중간 PACK_ONLY 묶음이 남은 채 끝 포장이 실패 (종료 4) → 다시 돌리면 옛 묶음을 보내라고 하지 않고 종료 4 · PACK_ONLY 뒤에야 0
        wpo, rcp1, _ = run_pkg("stale", {"A5": "conv", "c1": "zero"})
        rcp2 = subprocess.run(["bash", os.path.join(wpo, "run_a5.sh")], cwd=wpo, env={**os.environ, "PACK_ONLY": "1"}, capture_output=True, text=True).returncode
        old_tgz = _sha(os.path.join(wpo, "a5_return.tgz"))
        prc2 = rcmd(wpo, "--infra-abort", "c1", "sched-6", "2026-11-22T00:00:00Z", "node fault")
        _, rcp3, _ = run_pkg("stale", {"A5": "conv", "c1": "conv"}, fresh=False, env_extra={"FAKE_TAR_FAIL": "1"})
        tgz3, fc3 = _sha(os.path.join(wpo, "a5_return.tgz")), fcode(wpo)            # 끝 포장 실패 직후: 옛 묶음 그대로 · 끝 기록 0
        _, rcp4, logp4 = run_pkg("stale", {"A5": "conv", "c1": "conv"}, fresh=False)
        rs4, _ = chk(wpo)
        rcp5 = subprocess.run(["bash", os.path.join(wpo, "run_a5.sh")], cwd=wpo, env={**os.environ, "PACK_ONLY": "1"}, capture_output=True, text=True).returncode
        _, rcp6, logp6 = run_pkg("stale", {"A5": "conv", "c1": "conv"}, fresh=False)
        rs6, _ = chk(wpo)
        ck(rcp1 == 7 and rcp2 == 0 and prc2[0] == 0 and rcp3 == 4 and fc3 == 0 and tgz3 == old_tgz
           and rcp4 == 4 and "PACK_ONLY=1 bash run_a5.sh" in logp4 and rs4["status"] == "LADDER_INCOMPLETE" and rcp5 == 0 and rcp6 == 0 and rs6["status"] == "OK",
           f"⛔음성 Codex EN P1: 옛 묶음 (끝 기록 없음 · {rs4['status']}) → 다시 돌림 종료 4 (0 이 아니다) · PACK_ONLY 뒤 다시 0 · OK — "
           f"{rcp1} {rcp2} {prc2[0]} {rcp3} {rcp4} {rcp5} {rcp6} · {rs6['status']}")
        # S16e′: c2 행 0 → 멈춤 7 → 0 스텝 중단 기록 → 포장만 → 검사기 LADDER_INCOMPLETE (run_aborted 에만 있다) · 채택 없음 (리뷰 P0-1)
        w3b, rc3b, _ = run_pkg("p3b", {"A5": "conv", "c1": "plateau", "c2": "zero"})
        rcmd(w3b, "--infra-abort", "c2", "sched-7", "2026-11-22T00:00:00Z", "node fault")
        subprocess.run(["bash", os.path.join(w3b, "run_a5.sh")], cwd=w3b, env={**os.environ, "PACK_ONLY": "1"}, capture_output=True, text=True)
        r3b, _ = chk(w3b)
        ck(rc3b == 7 and r3b["status"] == "LADDER_INCOMPLETE" and adopt(r3b).get("adopted") is None and r3b["aborted"] == [["c2@aborted1", "SCF_UNVERIFIED"]],
           f"⛔음성 c2 0 스텝 → 중단 기록 → 포장만 → LADDER_INCOMPLETE · c1 보조 채택 없음 (리뷰 P0-1) — rc {rc3b} · {r3b['status']}")
        # P0-2(c): 뒤 단이 있으면 앞 단 기록 거부 (늦은 0 스텝 중단)
        w8, _, _ = run_pkg("p8", {"A5": "zero"})
        ck(not os.path.isdir(D(w8, "c1")), "A5 행 0 → c1 안 띄움 (개정 5 해석 1)")
        packed7 = os.path.isfile(os.path.join(w8, "a5_return.tgz"))          # 멈춤 7 은 포장하지 않는다 (보낼 것이 아니다)
        rcmd(w8, "--infra-abort", "A5", "s", "2026-11-21T00:00:00Z", "node fault")
        _, rc8a, _ = run_pkg("p8", {"A5": "conv", "c1": "zero"}, fresh=False)
        p8x = rcmd(w8, "--infra-abort", "A5", "s", "2026-11-21T00:00:00Z", "late")
        ck(rc8a == 7 and p8x[0] == 2 and "뒤 단" in p8x[1] and not packed7, f"⛔음성 c1 이 있으면 A5 0 스텝 중단 기록 거부 (리뷰 P0-2(c)) — {p8x[0]} {p8x[1].strip()[-60:]}")
        # P2(e): A5 에 검사기만 보는 실패 (D3) — 러너는 이어 간다 · 검사기는 STOPPED_FOR_REVIEW 로 보고 (c 단을 재시작 미이행으로 바꾸지 않는다)
        we, rce, _ = run_pkg("p2e", {"A5": "d3off", "c1": "conv"})
        re_, _ = chk(we)
        ck(rce == 0 and re_["attempts"]["A5"]["status"] == "D3_MISMATCH" and re_["attempts"]["c1"]["status"] == "OK" and re_["status"] == "STOPPED_FOR_REVIEW"
           and "A5 검사기만" in re_["why"] and re_["start_point"]["from"] == "A5" and adopt(re_).get("adopted") is None,
           f"⛔음성 A5 D3 불일치 (검사기만) → c1 은 기록된 시작점 (A5) 에 대조돼 OK · 전체 STOPPED_FOR_REVIEW · 채택 없음 (리뷰 P2(e)) — {re_['status']} · c1 {re_['attempts']['c1']['status']}")
        # S17: 인자 — VASP_CMD 없음 · W0_WAVECAR 없음 · 모르는 인자 → 종료 2 (1 이 아니다) · 아무것도 안 돈다
        w17 = os.path.join(T, "w_s17"); shutil.copytree(pkg, w17)
        p17 = subprocess.run(["bash", os.path.join(w17, "run_a5.sh")], cwd=w17, env={**os.environ, "VASP_CMD": "true", "POTCAR_DIR": potd}, capture_output=True, text=True)
        p17b = subprocess.run(["bash", os.path.join(w17, "run_a5.sh")], cwd=w17, env={**os.environ, "POTCAR_DIR": potd, "W0_WAVECAR": "none"}, capture_output=True, text=True)
        p17c = subprocess.run(["bash", os.path.join(w17, "run_a5.sh"), "--infra_abort", "A5"], cwd=w17, env={**os.environ, "VASP_CMD": "true", "POTCAR_DIR": potd, "W0_WAVECAR": "none"},
                              capture_output=True, text=True)
        ck(p17.returncode == 2 and p17b.returncode == 2 and p17c.returncode == 2 and "모르는 인자" in p17c.stdout and not os.path.isdir(D(w17, "A5")),
           f"⛔음성 W0_WAVECAR · VASP_CMD 없음 · 모르는 인자 → 종료 2 (값 없음 1 과 겹치지 않음) · 아무것도 안 돈다 — {p17.returncode} {p17b.returncode} {p17c.returncode}")
        # S18: 검사기 — ⓪ 기록이 거짓 (verified 1 · sha 다름) → W0_RECORD_MISMATCH
        ex1b = unpack(w1, "s18")
        wj = os.path.join(ex1b, "run", "w0_check.json"); d_ = json.load(open(wj)); d_["sha256"] = "0" * 64; _write(wj, json.dumps(d_))
        ck(rechk(ex1b)["status"] == "W0_RECORD_MISMATCH", "⛔음성 ⓪ 기록의 판정이 기록 값과 다르다 → W0_RECORD_MISMATCH")
        # S19: 검사기 — c1 INCAR 를 고친 반송 → INPUT_MODIFIED (차단)
        ex1c = unpack(w1, "s19")
        ip = os.path.join(ex1c, "run", f"{JOB}_c1", "INCAR"); _write(ip, open(ip).read().replace("MAXMIX = 200", "MAXMIX = 120"))
        aj = os.path.join(ex1c, "run", f"{JOB}_c1", "attempt.json"); d_ = json.load(open(aj)); d_["sha256"]["INCAR"] = _sha(ip); _write(aj, json.dumps(d_))
        rr_ = rechk(ex1c)
        ck(rr_["attempts"]["c1"]["status"] == "INPUT_MODIFIED" and rr_["status"] == "INPUT_MODIFIED", f"⛔음성 c1 INCAR 변경 → INPUT_MODIFIED · 채택 차단 — {rr_['status']}")
        ex1d = unpack(w1, "s19b")
        wi = os.path.join(ex1d, "run", f"{JOB}_c1", "WAVECAR.info"); d_ = json.load(open(wi))
        for k_ in ("src_sha256", "copied_sha256", "end_sha256"):
            d_[k_] = "d" * 64
        _write(wi, json.dumps(d_))
        aj = os.path.join(ex1d, "run", f"{JOB}_c1", "attempt.json"); d2_ = json.load(open(aj)); d2_["sha256"]["WAVECAR.info"] = _sha(wi); _write(aj, json.dumps(d2_))
        rr2 = rechk(ex1d)
        ck(rr2["attempts"]["c1"]["status"] == "RESTART_NOT_HONOURED" and "정해진 시작 WAVECAR" in rr2["attempts"]["c1"].get("why", "") and rr2["status"] == "STOPPED_FOR_REVIEW",
           f"⛔음성 c1 이 기록된 시작점이 아닌 것에서 시작 (기록은 셋 다 같음) → RESTART_NOT_HONOURED · STOPPED_FOR_REVIEW — {rr2['attempts']['c1'].get('why', '')[:60]}")
        # S20: c1 OUTCAR MAXMIX 해석값이 기본 (-45) → 러너 설정 에코 멈춤 8 · 검사기 SETTINGS_MISMATCH
        w20, rc20, _ = run_pkg("s20", {"A5": "conv", "c1": "badecho", "c2": "conv"})
        r20, _ = chk(w20)
        ck(rc20 == 8 and not os.path.isdir(D(w20, "c2")) and r20["attempts"]["c1"]["status"] == "SETTINGS_MISMATCH" and "MAXMIX" in r20["attempts"]["c1"]["why"]
           and r20["status"] == "STOPPED_FOR_REVIEW", f"⛔음성 OUTCAR MAXMIX -45 → 러너 멈춤 8 (c2 안 띄움) · 검사기 SETTINGS_MISMATCH — rc {rc20} · {r20['attempts']['c1'].get('why')}")
        # ═══ Codex EO (11-23) — 완전한 행 · 한 줄 기록 · 시작 기록 · 중단 시간 · 장부 ↔ 보존 폴더 · 끝 기록 시도 ID ═══
        import time as _time
        J_ = meta["jobs"][0]
        cp_ = lambda src_, nm_: (shutil.rmtree(os.path.join(T, nm_), ignore_errors=True), shutil.copytree(src_, os.path.join(T, nm_), symlinks=True))[1]
        pack_only = lambda w_: subprocess.run(["bash", os.path.join(w_, "run_a5.sh")], cwd=w_, env={**os.environ, "PACK_ONLY": "1"}, capture_output=True, text=True).returncode
        # EO P0 ①: c2 첫 행이 'SDA:' 에서 잘린 채 끊김 → --killed · --infra-abort 둘 다 거부 · 다시 돌리면 끝 기록 없이도 종료 8 · STOPPED_FOR_REVIEW · 채택 없음
        we1, _, _ = run_pkg("eo_sda", {"A5": "conv", "c1": "plateau", "c2": "plateau@0|SDA:"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c2"}, session=True)
        pk1_ = rcmd(we1, "--killed", "c2", "sched-9", "2026-11-23T00:00:00Z", "walltime", env_extra={"WALL_S": "100"})
        pa1_ = rcmd(we1, "--infra-abort", "c2", "sched-9", "2026-11-23T00:00:00Z", "node")
        eo1_base = cp_(we1, "eo_sda_base")
        _, rce1, _ = run_pkg("eo_sda", {}, fresh=False)
        re1, _ = chk(we1); c2e = re1["attempts"]["c2"]
        ck(pk1_[0] == 2 and "incomplete_row" in pk1_[1] and pa1_[0] == 2 and rce1 == 8 and fcode(we1) == 8 and re1["status"] == "STOPPED_FOR_REVIEW"
           and c2e["osz_rows"] == 0 and c2e["row_scan"]["why"] == "incomplete_row" and re1["classes"]["c2"][0] == "REVIEW" and adopt(re1).get("adopted") is None,
           f"⛔음성 Codex EO P0: c2 첫 행 'SDA:' 절단 (완전한 행 0) → --killed {pk1_[0]} · --infra-abort {pa1_[0]} 거부 · 다시 돌림 종료 {rce1} · {re1['status']} · "
           f"행 {c2e.get('osz_rows')} {c2e.get('row_scan')} · 채택 {adopt(re1).get('adopted')}")
        wo1 = cp_(eo1_base, "w_eo_sda_old"); s0e = rec_read(os.path.join(D(wo1, "c2"), "attempt.start"))       # 옛 러너가 받아 준 끊김 기록 (osz_rows '1') 이 있어도
        _write(os.path.join(D(wo1, "c2"), "killed.json"), json.dumps({"job": JOB, "rung": "c2", "run_id": rec_s(s0e, "run_id"), "wall_s": "100", "sched_job_id": "s",
               "cancel_utc": "t", "reason": "r", "osz_rows": "1", "recorded_utc": "u", "recorded_s": rec_i(s0e, "t_start") + 1}) + "\n")
        _, rco1, _ = run_pkg("eo_sda_old", {}, fresh=False)
        ro1, _ = chk(wo1)
        ck(rco1 == 8 and ro1["status"] == "STOPPED_FOR_REVIEW" and ro1["attempts"]["c2"]["status"] == "SCF_UNVERIFIED" and ro1["attempts"]["c2"]["osz_rows"] == 0
           and adopt(ro1).get("adopted") is None,
           f"⛔음성 Codex EO P0 재현: 'SDA:' 절단에 옛 러너가 쓴 끊김 기록 (행 1) → 종료 8 · 검사기 SCF_UNVERIFIED (행 0) · 채택 없음 — rc {rco1} · {ro1['status']}")
        # EO P0 ②: 완전한 1 행 뒤 'SDA:' 잘린 꼬리 → 1 행 (2 가 아니다) · --killed osz_rows '1' · 다시 → 종료 1 · NO_PRIMARY_VALUE · c1 보조 채택 (확인된 끝 · 양성)
        we2, _, _ = run_pkg("eo_tail", {"A5": "conv", "c1": "plateau", "c2": "plateau@1|SDA:"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c2"}, session=True)
        pk2_ = rcmd(we2, "--killed", "c2", "sched-9", "2026-11-23T00:00:00Z", "walltime", env_extra={"WALL_S": "100"})
        kj2 = rec_read(os.path.join(D(we2, "c2"), "killed.json"))
        _, rce2, _ = run_pkg("eo_tail", {}, fresh=False)
        re2, _ = chk(we2); ae2 = adopt(re2)
        ck(pk2_[0] == 0 and rec_s(kj2, "osz_rows") == "1" and rce2 == 1 and re2["status"] == "NO_PRIMARY_VALUE" and re2["attempts"]["c2"]["osz_rows"] == 1
           and ae2.get("adopted") == "a5_c1" and ae2.get("a5_rule") == "secondary",
           f"Codex EO P0: 완전한 1 행 + 'SDA:' 꼬리 → 1 행 · 끊김 기록 · 종료 1 · NO_PRIMARY_VALUE · c1 보조 — --killed {pk2_[0]} · 행 {rec_s(kj2, 'osz_rows')} · rc {rce2} · "
           f"{re2['status']} · {ae2.get('adopted')}")
        # EO P0 ③: 완전한 1 행 뒤 줄바꿈까지 쓰인 'SDA:' → 잘림이 아니라 손상 → --killed 거부 · 다시 → 8 · 채택 없음
        we3, _, _ = run_pkg("eo_tailnl", {"A5": "conv", "c1": "plateau", "c2": "plateau@1|SDA:\\n"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c2"}, session=True)
        pk3_ = rcmd(we3, "--killed", "c2", "sched-9", "2026-11-23T00:00:00Z", "walltime", env_extra={"WALL_S": "100"})
        _, rce3, _ = run_pkg("eo_tailnl", {}, fresh=False)
        re3, _ = chk(we3)
        ck(pk3_[0] == 2 and rce3 == 8 and re3["status"] == "STOPPED_FOR_REVIEW" and re3["attempts"]["c2"]["row_scan"]["why"] == "incomplete_row" and adopt(re3).get("adopted") is None,
           f"⛔음성 완전한 1 행 + 줄바꿈 있는 'SDA:' → 손상 · --killed {pk3_[0]} · 종료 {rce3} · {re3['status']} · 채택 없음")
        # EO P0 ④: 끝난 c2 (끝 기록 있음) — 완전한 행 5 + 줄바꿈까지 쓰인 덜 쓴 행 (손상) + 재시작 안 됨 (OUTCAR ISTART 0) → 손상이 재시작 · 설정 확인보다 먼저:
        #   러너 status.tsv · 검사기 시도 상태 둘 다 SCF_UNVERIFIED (incomplete_row) — 같은 순서 (돌연변이 m101 이 이 대조를 깬다)
        wfd, rcfd, _ = run_pkg("eo_findmg", {"A5": "conv", "c1": "plateau", "c2": "istart0@5|SDA:   6   -0.7E+03\\n"})
        rfd, _ = chk(wfd); sfd = [r_ for r_ in stat_rows(wfd) if r_[1] == "c2"][0]
        ck(rcfd == 8 and sfd[4] == "SCF_UNVERIFIED" and sfd[8] == "incomplete_row" and rfd["attempts"]["c2"]["status"] == "SCF_UNVERIFIED"
           and rfd["attempts"]["c2"]["osz_rows"] == 5 and rfd["status"] == "STOPPED_FOR_REVIEW" and adopt(rfd).get("adopted") is None,
           f"⛔음성 Codex EO P0: 끝난 c2 의 행 손상 (완전한 행 5 + 덜 쓴 행 · ISTART 0) → 손상이 먼저 — 러너 {sfd[4]} ({sfd[8]}) · 검사기 "
           f"{rfd['attempts']['c2']['status']} · 종료 {rcfd} · {rfd['status']}")
        # EO P1 Q-EO-2a ①: --killed 사유에 ESC (터미널 색) · 따옴표 · 역슬래시 · 한글 → 영수증은 JSON 이스케이프 · 양쪽이 받는다 · c2 가 돌고 OK (전에는 러너 통과 · 검사기 거부)
        esc_reason = "walltime \x1b[31mred\x1b[0m \"q\" back\\slash 노드"
        we4, _, _ = run_pkg("eo_esc", {"A5": "conv", "c1": "plateau@7", "c2": "conv"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c1"}, session=True)
        pk4_ = rcmd(we4, "--killed", "c1", "sched-\x1b7", "2026-11-23T00:00:00Z", esc_reason, env_extra={"WALL_S": "100"})
        kp4 = os.path.join(D(we4, "c1"), "killed.json")
        kj4, kd4 = rec_read(kp4), json.loads(open(kp4, encoding="utf-8").read())
        _, rce4, _ = run_pkg("eo_esc", {"A5": "conv", "c1": "plateau@7", "c2": "conv"}, fresh=False)
        re4, _ = chk(we4)
        ck(pk4_[0] == 0 and kj4 is not None and kd4["reason"] == esc_reason and kd4["sched_job_id"] == "sched-\x1b7" and b"\x1b" not in open(kp4, "rb").read()
           and rce4 == 0 and re4["status"] == "OK" and re4["attempts"]["c1"]["status"] == "INCOMPLETE_ATTEMPT" and adopt(re4).get("adopted") == "a5_c2",
           f"Codex EO P1: --killed 사유 ESC · 따옴표 · 역슬래시 → 이스케이프한 한 줄 기록 · 원래 글로 풀림 · 종료 {rce4} · {re4['status']} · c2 채택 — {pk4_[1].strip()[-80:]}")
        # EO P1 Q-EO-2a ②: 반송의 killed.json — 쉼표 하나 유실 → 양쪽 거부 (8 · STOPPED_FOR_REVIEW) / 콜론 뒤 공백 없는 유효 JSON → 양쪽 받음 (1 · NO_PRIMARY_VALUE · c1 보조)
        for i_, (lab_, txt_, wrc_, wst_) in enumerate((("쉼표 유실", json.dumps(kb0).replace(', "rung"', ' "rung"', 1), 8, "LADDER_VIOLATION"),
                                                     ("콜론 뒤 공백 없음 (유효 JSON)", json.dumps(kb0, separators=(",", ":")), 1, "NO_PRIMARY_VALUE"),
                                                     ("탭 · 앞뒤 빈칸 (유효 JSON)", " " + json.dumps(kb0, separators=(" ,\t", " :\t")) + "\t", 1, "NO_PRIMARY_VALUE"))):
            wv = cp_(kb_base, f"w_eo_kj{i_}"); _write(os.path.join(wv, "run", f"{JOB}_c2", "killed.json"), txt_ + "\n")
            _, rcv, logv = run_pkg(f"eo_kj{i_}", {}, fresh=False)
            rv = chk(wv)[0] if wrc_ == 1 else rechk(cp_(wv, f"ex_eo_kj{i_}")); av = adopt(rv)
            ck(rcv == wrc_ and rv["status"] == wst_ and (av.get("adopted") == "a5_c1" if wrc_ == 1 else (av.get("adopted") is None and "killed_json_form" in logv)),
               f"{'⛔음성 ' if wrc_ == 8 else ''}Codex EO P1: 반송 killed.json {lab_} → 러너 종료 {rcv} (기대 {wrc_}) · 검사기 {rv['status']} (기대 {wst_}) · 채택 {av.get('adopted')}")
        # EO P1 Q-EO-2b: c2 attempt.start 의 잡 · 변형 · stage 만 바꾸고 run_id 유지 → 러너 BAD2 (종료 2 · 끝 기록 없음) · 검사기 ATTEMPT_MISMATCH · 채택 없음
        for i_, (lab_, fld_, val_) in enumerate((("잡 이름", "job", "V5_s_outer_A_G4_e70_far_a4"), ("변형", "attempt", "c1"), ("stage", "stage", "a4"))):
            wv = cp_(kb_base, f"w_eo_st{i_}"); spp_ = os.path.join(wv, "run", f"{JOB}_c2", "attempt.start")
            s0d = json.loads(open(spp_).read()); s0d[fld_] = val_; _write(spp_, json.dumps(s0d) + "\n")
            _, rcv, logv = run_pkg(f"eo_st{i_}", {}, fresh=False)
            pov = pack_only(wv)
            rv = rechk(cp_(wv, f"ex_eo_st{i_}"))
            ck(rcv == 8 and fcode(wv) is None and pov == 8 and rv["attempts"]["c2"]["status"] == "ATTEMPT_MISMATCH" and rv["status"] == "LADDER_VIOLATION" and "start_" in logv
               and adopt(rv).get("adopted") is None,
               f"⛔음성 Codex EO P1: c2 attempt.start {lab_} 바꿈 (run_id 유지) → 러너 종료 {rcv} · 검사기 {rv['attempts']['c2']['status']} · {rv['status']} · 채택 {adopt(rv).get('adopted')}")
        # EO P1 Q-EO-2b ②: --infra-abort 도 attempt.start 를 그 폴더와 대조 (A5 0 스텝 · 잡 이름만 바꿈 · run_id 유지) → 종료 2 · 폴더 그대로 · 영수증 · 장부 없음 (m113)
        wia, rcia, _ = run_pkg("eo_st_iab", {"A5": "zero"})
        spi_ = os.path.join(D(wia, "A5"), "attempt.start"); sdi_ = json.loads(open(spi_).read()); sdi_["job"] = "V5_s_outer_A_G4_e70_far_a4"
        _write(spi_, json.dumps(sdi_) + "\n")
        pia = rcmd(wia, "--infra-abort", "A5", "sched-1", "2026-11-23T00:00:00Z", "node", env_extra={"WALL_S": "100"})
        ck(rcia == 7 and pia[0] == 8 and "start_job" in pia[1] and os.path.isdir(D(wia, "A5"))
           and not os.path.exists(os.path.join(wia, "run_aborted")) and not os.path.exists(os.path.join(wia, "run", "infra_aborts.tsv")),
           f"⛔음성 Codex EO P1: --infra-abort 도 attempt.start 를 그 폴더와 대조 (잡만 바꿈) → 종료 {pia[0]} · 폴더 그대로 · 영수증 · 장부 없음 — {pia[1].strip()[-90:]}")
        # EO P1 Q-EO-2c ①: A5 0 스텝 (attempt.json elapsed ≈ 0) 뒤 WALL_S=648001 로 중단 기록 → 영수증 시간이 먼저 → 다시 돌리면 상한 (끝 5) · A5 안 띄움
        wc5, rcc1, _ = run_pkg("eo_cap", {"A5": "zero"})
        pc5 = rcmd(wc5, "--infra-abort", "A5", "sched-1", "2026-11-23T00:00:00Z", "node", env_extra={"WALL_S": "648001"})
        el0 = json.load(open(os.path.join(wc5, "run_aborted", f"{JOB}_A5_1", "attempt.json")))["elapsed_s"]
        _, rcc2, logc2 = run_pkg("eo_cap", {"A5": "conv", "c1": "conv"}, fresh=False)
        rc5_, _ = chk(wc5)
        ck(rcc1 == 7 and pc5[0] == 0 and el0 < 600 and rcc2 == 5 and fcode(wc5) == 5 and not os.path.isdir(D(wc5, "A5")) and "상한" in logc2
           and rc5_["status"] == "LADDER_INCOMPLETE" and adopt(rc5_).get("adopted") is None,
           f"⛔음성 Codex EO P1: WALL_S 648001 + attempt.json elapsed {el0} → 영수증 시간으로 상한 넘음 · A5 안 띄움 · 끝 5 · {rc5_['status']} — rc {rcc2}")
        exc_ = cp_(exr, "ex_eo_cap"); rpc_ = os.path.join(exc_, rp_); dpc_ = json.loads(open(rpc_).read()); dpc_["wall_s"] = "648001"; _write(rpc_, json.dumps(dpc_) + "\n")
        lpc_ = os.path.join(exc_, "run", "infra_aborts.tsv"); lt_ = open(lpc_).read().split("\n"); f_ = lt_[1].split("\t"); f_[5] = "648001"; lt_[1] = "\t".join(f_)
        _write(lpc_, "\n".join(lt_)); rvc = rechk(exc_)
        ck(rvc["status"] == "LADDER_VIOLATION" and any("상한" in v for v in rvc["ladder_violations"]) and adopt(rvc).get("adopted") is None,
           f"⛔음성 Codex EO P1: 옛 러너가 영수증 648001 s 뒤에 A5 를 다시 띄운 반송 → 누적 상한 위반 (LADDER_VIOLATION) — {rvc['ladder_violations'][:2]}")
        # EO P1 Q-EO-2c ②: 벽시계 미상 (UNKNOWN) 영수증 — 그 자체로는 적법 · 다시 돌리면 멈춤 5 · --infra-wall 로 채운 뒤 진행 · 완료 반송을 UNKNOWN 으로 되돌리면 거부
        wu_, _, _ = run_pkg("eo_unk", {"A5": "zero"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "A5"}, session=True)
        pu1 = rcmd(wu_, "--infra-abort", "A5", "sched-2", "2026-11-23T00:00:00Z", esc_reason)
        rpu = os.path.join(wu_, "run_aborted", f"{JOB}_A5_1", "infra_abort.json"); ru0 = rec_read(rpu)
        _, rcu2, logu2 = run_pkg("eo_unk", {"A5": "conv", "c1": "conv"}, fresh=False)
        pu3 = rcmd(wu_, "--infra-wall", f"{JOB}_A5_1", "300"); pu3b = rcmd(wu_, "--infra-wall", f"{JOB}_A5_1", "400")
        ru1 = rec_read(rpu)
        _, rcu4, _ = run_pkg("eo_unk", {"A5": "conv", "c1": "conv"}, fresh=False)
        ruu, exu = chk(wu_)
        ck(pu1[0] == 0 and rec_s(ru0, "wall_s") == "UNKNOWN" and json.loads(open(rpu, encoding="utf-8").read())["reason"] == esc_reason and rcu2 == 5 and "미상" in logu2
           and pu3[0] == 0 and pu3b[0] == 2 and rec_s(ru1, "wall_s") == "300" and rec_i(ru1, "wall_s_filled_s") is not None and rcu4 == 0 and ruu["status"] == "OK",
           f"Codex EO P1: 끊긴 A5 (행 0 · attempt.json 없음) → 영수증 UNKNOWN (ESC 사유 이스케이프) → 멈춤 5 → --infra-wall 300 (채운 시각) → OK — "
           f"{pu1[0]} {rcu2} {pu3[0]} {pu3b[0]} {rcu4} · {ruu['status']}")
        exv = cp_(exu, "ex_eo_unk_rev"); rpv = os.path.join(exv, "run_aborted", f"{JOB}_A5_1", "infra_abort.json"); dv_ = json.loads(open(rpv, encoding="utf-8").read())
        dv_["wall_s"] = "UNKNOWN"; dv_.pop("wall_s_filled_utc"); dv_.pop("wall_s_filled_s"); _write(rpv, json.dumps(dv_) + "\n")
        lpv = os.path.join(exv, "run", "infra_aborts.tsv"); _write(lpv, open(lpv).read().replace("\t300\t", "\tUNKNOWN\t"))
        rvu = rechk(exv)
        ck(rvu["status"] == "LADDER_VIOLATION" and any("미상" in v for v in rvu["ladder_violations"]) and adopt(rvu).get("adopted") is None,
           f"⛔음성 Codex EO P1: 완료 반송에서 영수증 · 장부를 UNKNOWN 으로 되돌림 → 미상인데 A5 를 띄웠다 (LADDER_VIOLATION) — {rvu['ladder_violations'][:2]}")
        exv = cp_(exu, "ex_eo_unk_late"); rpv = os.path.join(exv, "run_aborted", f"{JOB}_A5_1", "infra_abort.json"); dv_ = json.loads(open(rpv, encoding="utf-8").read())
        dv_["wall_s_filled_s"] = json.loads(open(os.path.join(exv, "run", f"{JOB}_A5", "attempt.start")).read())["t_start"] + 100; _write(rpv, json.dumps(dv_) + "\n")
        rvl = rechk(exv)
        ck(rvl["status"] == "LADDER_VIOLATION" and any("채운 시각" in v for v in rvl["ladder_violations"]),
           f"⛔음성 Codex EO P1: 벽시계를 채운 시각 > 다음 A5 시작 → 미상인 채로 띄웠다 (LADDER_VIOLATION) — {rvl['ladder_violations'][:2]}")
        # EO P0 ⑤ 검사기: 보존된 0 스텝 중단 폴더 (끊긴 A5 · 끝 기록 없음 · 영수증 그대로) 의 OSZICAR 에 덜 쓴 행 → LADDER_VIOLATION (러너 --infra-abort 도 거부하는 손상 · m112)
        exv = cp_(exu, "ex_eo_ab_dmg"); _write(os.path.join(exv, "run_aborted", f"{JOB}_A5_1", "OSZICAR"), hd_ + "DAV:   1   -0.73E+03\n")
        rvd = rechk(exv)
        ck(rvd["status"] == "LADDER_VIOLATION" and any("행 판독 incomplete_row" in v for v in rvd["ladder_violations"]) and adopt(rvd).get("adopted") is None,
           f"⛔음성 Codex EO P0 검사기: 0 스텝 중단 폴더의 행 손상 (덜 쓴 행) → LADDER_VIOLATION — {rvd['ladder_violations'][:2]}")
        # EO P1 Q-EO-3: 부분 복구 — 장부에 c1 중단이 있는데 보존 폴더 · 시작점만 빠짐 → 러너는 시작점을 쓰지 않고 c1 을 띄우지 않고 8 · 검사기 LADDER_VIOLATION
        for i_, how_ in enumerate(("폴더 · 시작점 빠짐", "장부 줄 빠짐", "영수증 run_id 다름")):
            wv = cp_(sp_base, f"w_eo_led{i_}"); abd_ = os.path.join(wv, "run_aborted", f"{JOB}_c1_1")
            if i_ == 0:
                shutil.rmtree(abd_); os.remove(os.path.join(wv, "run", "start_point.json"))
            elif i_ == 1:
                lp_ = os.path.join(wv, "run", "infra_aborts.tsv"); _write(lp_, open(lp_).read().split("\n")[0] + "\n")
            else:
                rp2 = os.path.join(abd_, "infra_abort.json"); d2 = json.loads(open(rp2, encoding="utf-8").read()); d2["run_id"] = "20261123T000000-1-1"; _write(rp2, json.dumps(d2) + "\n")
            sp_had = os.path.isfile(os.path.join(wv, "run", "start_point.json")); sp_sha = _sha(os.path.join(wv, "run", "start_point.json")) if sp_had else None
            _, rcv, logv = run_pkg(f"eo_led{i_}", {"A5": "conv", "c1": "conv"}, fresh=False)
            rv = rechk(cp_(wv, f"ex_eo_led{i_}"))
            sp_now = _sha(os.path.join(wv, "run", "start_point.json")) if os.path.isfile(os.path.join(wv, "run", "start_point.json")) else None
            ck(rcv == 8 and fcode(wv) is None and "트리 관문" in logv and ("ledger" in logv or "receipt" in logv) and sp_now == sp_sha and not os.path.isdir(D(wv, "c1"))
               and rv["status"] == "LADDER_VIOLATION"
               and any(("장부" in v or "영수증" in v) for v in rv["ladder_violations"]) and adopt(rv).get("adopted") is None,
               f"⛔음성 Codex EO P1: 부분 복구 ({how_}) → 러너 종료 {rcv} · 시작점 {'그대로' if sp_now == sp_sha else '바뀜'} · c1 안 띄움 · 검사기 {rv['status']}")
        for lab_, fn_ in (("장부 줄 빠짐", lambda e_: _write(os.path.join(e_, "run", "infra_aborts.tsv"), LEDGER_HEAD + "\n")),
                          ("보존 폴더 빠짐", lambda e_: shutil.rmtree(os.path.join(e_, "run_aborted", f"{JOB}_c1_1"))),
                          ("장부 wall_s ≠ 영수증", lambda e_: _write(os.path.join(e_, "run", "infra_aborts.tsv"), "\n".join(
                              (lambda L_: [L_[0], "\t".join(f_ if j_ != 5 else str(int(f_) + 7) for j_, f_ in enumerate(L_[1].split("\t")))] + L_[2:])(
                                  open(os.path.join(e_, "run", "infra_aborts.tsv")).read().split("\n")))))):
            exv = cp_(exso, f"ex_eo_l_{abs(hash(lab_))}"); fn_(exv); rv = rechk(exv)
            ck(rv["status"] == "LADDER_VIOLATION" and any("장부" in v for v in rv["ladder_violations"]) and adopt(rv).get("adopted") is None,
               f"⛔음성 Codex EO P1 검사기: OK 반송에서 {lab_} → 장부 ↔ 보존 폴더 대조 LADDER_VIOLATION — {rv['ladder_violations'][:2]}")
        # EO P2 Q-EO-4: 같은 초 (모의 시계) 의 별개 실행 둘 — 끝 기록은 시도 ID 만 다르다 → 다른 실행의 tgz + sha 쌍을 옮기면 다시 돌림 종료 4 · 포장만 다시 → 0
        now_ = str(int(_time.time()))
        wx1, rx1, _ = run_pkg("eo_sw1", {"A5": "conv", "c1": "conv"}, env_extra={"FAKE_NOW": now_})
        wx2, rx2, _ = run_pkg("eo_sw2", {"A5": "conv", "c1": "conv"}, env_extra={"FAKE_NOW": now_})
        f1_, f2_ = (rec_read(os.path.join(w_, "run", "final.json")) for w_ in (wx1, wx2))
        same_ = {k: v for k, v in f1_.items() if k != "attempts"} == {k: v for k, v in f2_.items() if k != "attempts"} and f1_["attempts"] != f2_["attempts"]
        for f_ in ("a5_return.tgz", "a5_return.tgz.sha256"):
            shutil.copy2(os.path.join(wx2, f_), os.path.join(wx1, f_))
        tgsw = _sha(os.path.join(wx1, "a5_return.tgz"))
        _, rsw1, logsw = run_pkg("eo_sw1", {}, fresh=False, env_extra={"FAKE_NOW": now_})
        psw = pack_only(wx1)
        _, rsw2, _ = run_pkg("eo_sw1", {}, fresh=False, env_extra={"FAKE_NOW": now_})
        rsw, exsw = chk(wx1)
        ck(rx1 == 0 and rx2 == 0 and same_ and rsw1 == 8 and "tgz_final_differs" in logsw and psw == 8 and rsw2 == 8 and _sha(os.path.join(wx1, "a5_return.tgz")) == tgsw
           and rsw["status"] == "OK"
           and rsw["final_record"]["attempts"] == attempts_of(exsw, J_),
           f"⛔음성 Codex EO P2 · EQ: 같은 초 별개 실행의 tgz + sha 쌍 (끝 기록 다름) → 다시 돌림 {rsw1} · 포장만 {psw} · 다시 {rsw2} (모두 8 · 트리 관문 tgz_final_differs · 반송본 그대로) · 그 반송본 자체는 {rsw['status']} · 끝 기록 시도 ID 만 다름 {same_}")
        exv = cp_(exsw, "ex_eo_fin"); fjp = os.path.join(exv, "run", "final.json"); dfj = json.loads(open(fjp).read())
        dfj["attempts"] = dfj["attempts"].replace("=", "=9", 1); _write(fjp, json.dumps(dfj) + "\n"); rvf = rechk(exv)
        ck(rvf["status"] == "LADDER_VIOLATION" and any("final_attempts_differ" in v for v in rvf["ladder_violations"]),
           f"⛔음성 Codex EO P2: 끝 기록의 시도 목록 ≠ 반송 시도 → 트리 관문 final_attempts_differ · LADDER_VIOLATION (러너도 8) — {rvf['status']} {rvf.get('why', '')[:70]}")
        # ═══ Codex EP (11-23) — 숫자를 못 읽는 행 · 콜론 앞 머리 절단 · 진행 폴더의 남의 영수증 · status.tsv 이력 · 끝난 시도 신원 · 끝 기록 · 빈 영수증 칸 · 비 UTF-8 · 장부 순서 ═══
        garb = "SDA: 1 none missing missing abc bad\\n"
        # EP P0 ①: c2 유일 행이 숫자를 못 읽는 행 (칸 수만 맞음) 에서 끊김 → --killed 거부 · 다시 돌림 8 · STOPPED_FOR_REVIEW · 채택 없음 (전에는 --killed 0 · 1 · c1 보조)
        wg1, _, _ = run_pkg("ep_garb", {"A5": "conv", "c1": "plateau", "c2": "plateau@0|" + garb}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c2"}, session=True)
        pg1 = rcmd(wg1, "--killed", "c2", "sched-9", "2026-11-23T00:00:00Z", "walltime", env_extra={"WALL_S": "100"})
        _, rcg1, _ = run_pkg("ep_garb", {}, fresh=False)
        rg1, _ = chk(wg1)
        ck(pg1[0] == 2 and rcg1 == 8 and rg1["status"] == "STOPPED_FOR_REVIEW" and rg1["attempts"]["c2"].get("osz_rows") == 0
           and (rg1["attempts"]["c2"].get("row_scan") or {}).get("why") == "incomplete_row" and adopt(rg1).get("adopted") is None,
           f"⛔음성 Codex EP P0: c2 유일 행 'SDA: 1 none missing missing abc bad' 끊김 → --killed {pg1[0]} · 다시 돌림 {rcg1} · {rg1['status']} · 채택 {adopt(rg1).get('adopted')}")
        # EP P0 ②: 끝 기록이 있는 실행 실패 (rc 1) 의 유일 행이 같은 행 → 손상 → 종료 8 (전에는 RUN_FAILED · 1 행 · c1 보조)
        wg2, rcg2, _ = run_pkg("ep_garb_rf", {"A5": "conv", "c1": "plateau", "c2": "crash@0|" + garb})
        rg2, _ = chk(wg2); sg2 = [r_ for r_ in stat_rows(wg2) if r_[1] == "c2"]
        ck(rcg2 == 8 and len(sg2) == 1 and sg2[0][4] == "SCF_UNVERIFIED" and sg2[0][8] == "incomplete_row" and rg2["status"] == "STOPPED_FOR_REVIEW"
           and rg2["attempts"]["c2"]["status"] == "SCF_UNVERIFIED" and adopt(rg2).get("adopted") is None,
           f"⛔음성 Codex EP P0: 끝난 c2 실행 실패의 유일 행이 숫자를 못 읽는 행 → 종료 {rcg2} · {sg2[:1]} · {rg2['status']} · 채택 {adopt(rg2).get('adopted')}")
        # EP P0 ③: 첫 행이 콜론 앞 'SDA' 에서 끊김 → --infra-abort 거부 · 다시 돌림 8 (전에는 0 스텝으로 받고 c2 다시 · OK · c2 채택)
        wg3, _, _ = run_pkg("ep_hcut", {"A5": "conv", "c1": "plateau", "c2": "plateau@0|SDA"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c2"}, session=True)
        pg3 = rcmd(wg3, "--infra-abort", "c2", "sched-9", "2026-11-23T00:00:00Z", "node", env_extra={"WALL_S": "100"})
        _, rcg3, _ = run_pkg("ep_hcut", {"A5": "conv", "c1": "plateau", "c2": "conv"}, fresh=False)
        rg3, _ = chk(wg3)
        ck(pg3[0] == 2 and rcg3 == 8 and rg3["status"] == "STOPPED_FOR_REVIEW" and not os.path.isdir(os.path.join(wg3, "run_aborted")) and adopt(rg3).get("adopted") is None,
           f"⛔음성 Codex EP P0: 'SDA' (콜론 앞) 절단 → --infra-abort {pg3[0]} · 다시 돌림 {rcg3} · {rg3['status']}")
        # EP P1 ②: 시간 출처 — c1 이 648001 s 로 끊겨 상한을 넘었는데 남의 0 스텝 영수증을 run/<잡>_c1/ 에 넣음 → 러너 8 (c2 안 띄움) · 검사기 LADDER_VIOLATION
        wst_, _, _ = run_pkg("ep_stray", {"A5": "conv", "c1": "plateau@7", "c2": "conv"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c1"}, session=True)
        pst = rcmd(wst_, "--killed", "c1", "sched-5", "2026-11-23T00:00:00Z", "walltime", env_extra={"WALL_S": "648001"})
        shutil.copy(os.path.join(exu, "run_aborted", f"{JOB}_A5_1", "infra_abort.json"), os.path.join(D(wst_, "c1"), "infra_abort.json"))
        _, rcst, logst = run_pkg("ep_stray", {"A5": "conv", "c1": "plateau@7", "c2": "conv"}, fresh=False)
        ck(pst[0] == 0 and rcst == 8 and fcode(wst_) is None and not os.path.isdir(D(wst_, "c2")) and "stray_receipt" in logst,
           f"⛔음성 Codex EP P1: 상한 넘은 c1 + 진행 폴더의 남의 영수증 → 러너 종료 {rcst} · c2 {'뜸' if os.path.isdir(D(wst_, 'c2')) else '안 뜸'}")
        exv = cp_(exso, "ex_ep_stray"); shutil.copy(os.path.join(exso, "run_aborted", f"{JOB}_c1_1", "infra_abort.json"), os.path.join(exv, "run", f"{JOB}_c1", "infra_abort.json"))
        rvs = rechk(exv)
        ck(rvs["status"] == "LADDER_VIOLATION" and any("stray_receipt" in v for v in rvs["ladder_violations"]) and adopt(rvs).get("adopted") is None,
           f"⛔음성 Codex EP P1 검사기: 진행 폴더 (run/<잡>_c1) 의 중단 영수증 → LADDER_VIOLATION — {rvs['ladder_violations'][:2]}")
        # EP P1 ③: 부분 복구 — c1 0 스텝 중단의 장부 · 보존 폴더 · 시작점을 함께 지우고 status.tsv 의 첫 c1 줄만 남음 → 러너 8 (시작점 안 씀 · c1 안 띄움) · 검사기 LADDER_VIOLATION
        wh_ = cp_(sp_base, "w_ep_hist")
        os.remove(os.path.join(wh_, "run", "infra_aborts.tsv")); shutil.rmtree(os.path.join(wh_, "run_aborted")); os.remove(os.path.join(wh_, "run", "start_point.json"))
        _, rch, logh = run_pkg("ep_hist", {"A5": "conv", "c1": "conv"}, fresh=False)
        ck(rch == 8 and fcode(wh_) is None and not os.path.isfile(os.path.join(wh_, "run", "start_point.json")) and not os.path.isdir(D(wh_, "c1")) and "status_row" in logh,
           f"⛔음성 Codex EP P1: 부분 복구 (장부 · 보존 폴더 · 시작점 함께 빠짐 · status.tsv 의 첫 c1 남음) → 러너 종료 {rch} · 시작점 "
           f"{'다시 씀' if os.path.isfile(os.path.join(wh_, 'run', 'start_point.json')) else '안 씀'}")
        exh = cp_(exso, "ex_ep_hist")
        os.remove(os.path.join(exh, "run", "infra_aborts.tsv")); shutil.rmtree(os.path.join(exh, "run_aborted"))
        fjh = os.path.join(exh, "run", "final.json"); dfh = json.loads(open(fjh).read()); dfh["attempts"] = attempts_of(exh, J_); _write(fjh, json.dumps(dfh) + "\n")
        rvh = rechk(exh)
        ck(rvh["status"] == "LADDER_VIOLATION" and any("status.tsv" in v for v in rvh["ladder_violations"]) and adopt(rvh).get("adopted") is None,
           f"⛔음성 Codex EP P1 검사기: 부분 복구 (장부 · 보존 폴더 빠짐 · 끝 기록 맞춤) 에 status.tsv 의 첫 c1 줄이 남음 → {rvh['status']} — {rvh['ladder_violations'][:2]}")
        # EP 조건부 ④: 끝난 시도의 신원 — 정상 c1 의 attempt.json run_id (다른 유효 ID) · t_start 만 바꿈 → 검사기 ATTEMPT_MISMATCH · 러너 (끝 전) BAD2 종료 2
        for i_, (fld_, val_) in enumerate((("run_id", "20261123T000000-9-9"), ("t_start", 5))):
            exv = cp_(exso, f"ex_ep_eid{i_}"); ajp = os.path.join(exv, "run", f"{JOB}_c1", "attempt.json"); daj = json.loads(open(ajp).read()); daj[fld_] = val_
            _write(ajp, json.dumps(daj) + "\n"); rve = rechk(exv)
            ck(rve["attempts"]["c1"]["status"] == "ATTEMPT_MISMATCH" and rve["status"] in ("ATTEMPT_MISMATCH", "LADDER_VIOLATION") and adopt(rve).get("adopted") is None,
               f"⛔음성 Codex EP 조건부: 끝난 c1 attempt.json {fld_} 만 바꿈 → 검사기 {rve['attempts']['c1']['status']} · {rve['status']} · 채택 {adopt(rve).get('adopted')}")
        wei, rcei1, _ = run_pkg("ep_eid", {"A5": "zero"})
        ajp = os.path.join(D(wei, "A5"), "attempt.json"); _write(ajp, open(ajp).read().replace('"run_id": "', '"run_id": "9', 1))
        _, rcei2, logei = run_pkg("ep_eid", {"A5": "zero"}, fresh=False)
        ck(rcei1 == 7 and rcei2 == 8 and "end_run_id" in logei, f"⛔음성 Codex EP 조건부: 러너 — 끝난 A5 의 attempt.json run_id ≠ attempt.start → 종료 {rcei2} (BAD2 · 전에는 7)")
        # EP 조건부 ④: 끝 기록 — 검사기는 끝 기록 없는 반송을 채택하지 않는다 · 러너는 attempts 가 없거나 다른 끝 기록이면 포장 · 다시 돌림 전에 종료 2
        exv = cp_(exso, "ex_ep_nofin"); os.remove(os.path.join(exv, "run", "final.json")); rvn = rechk(exv)
        ck(rvn["status"] == "STOPPED_FOR_REVIEW" and "끝 기록" in rvn.get("why", "") and adopt(rvn).get("adopted") is None,
           f"⛔음성 Codex EP 조건부: 끝 기록 (run/final.json) 없는 OK 반송 → {rvn['status']} {rvn.get('why', '')[:60]}")
        for i_, how_ in enumerate(("drop", "edit")):
            wf_ = cp_(wso, f"w_ep_fin{i_}"); fjp_ = os.path.join(wf_, "run", "final.json"); dff = json.loads(open(fjp_).read())
            if how_ == "drop":
                dff.pop("attempts")
            else:
                dff["attempts"] = dff["attempts"] + " run/x=1"
            _write(fjp_, json.dumps(dff) + "\n"); tg0 = _sha(os.path.join(wf_, "a5_return.tgz"))
            pf_ = pack_only(wf_); _, rcf_, _ = run_pkg(f"ep_fin{i_}", {}, fresh=False)
            ck(pf_ == 8 and rcf_ == 8 and _sha(os.path.join(wf_, "a5_return.tgz")) == tg0,
               f"⛔음성 Codex EP 조건부: 러너 끝 기록 attempts {how_} → 포장만 {pf_} · 다시 돌림 {rcf_} (둘 다 2 · 묶음 그대로)")
        wf3 = cp_(wso, "w_ep_fin_notgz"); fjp3 = os.path.join(wf3, "run", "final.json"); dff3 = json.loads(open(fjp3).read())
        dff3["attempts"] = dff3["attempts"] + " run/x=1"; _write(fjp3, json.dumps(dff3) + "\n"); fb3 = open(fjp3, "rb").read()
        for f_ in ("a5_return.tgz", "a5_return.tgz.sha256"):
            os.remove(os.path.join(wf3, f_))
        pf3 = pack_only(wf3); _, rcf3, logf3 = run_pkg("ep_fin_notgz", {}, fresh=False)
        ck(pf3 == 8 and rcf3 == 8 and "final_attempts_differ" in logf3 and not os.path.exists(os.path.join(wf3, "a5_return.tgz")) and open(fjp3, "rb").read() == fb3,
           f"⛔음성 Codex EQ: 끝 기록 attempts 다름 · 기존 반송본 없음 (반송본 대조가 가리지 않게 — 러너 fin_ok 만) → 포장만 {pf3} · 다시 돌림 {rcf3}")
        # EP 조건부 ⑤: 영수증 · 끊김 기록의 필수 칸 (잡 ID · 취소 시각 · 사유) 이 비면 거부 (러너 · 검사기)
        wv = cp_(kb_base, "w_ep_kjempty"); _write(os.path.join(wv, "run", f"{JOB}_c2", "killed.json"), json.dumps({**kb0, "sched_job_id": ""}) + "\n")
        _, rcv, logv = run_pkg("ep_kjempty", {}, fresh=False); rv = rechk(cp_(wv, "ex_ep_kjempty"))
        ck(rcv == 8 and "killed_json_blank_sched_job_id" in logv and rv["status"] == "LADDER_VIOLATION" and adopt(rv).get("adopted") is None,
           f"⛔음성 Codex EP 조건부: killed.json sched_job_id 빈 문자열 → 러너 {rcv} · 검사기 {rv['status']} · 채택 {adopt(rv).get('adopted')}")
        exk = unpack(wkb, "ep_kjempty_ex"); kpk = os.path.join(exk, "run", f"{JOB}_c2", "killed.json")
        _write(kpk, json.dumps({**json.loads(open(kpk).read()), "sched_job_id": ""}) + "\n"); rvk = rechk(exk)
        ck(rvk["attempts"]["c2"]["status"] == "KILLED_RECORD_MISMATCH" and rvk["status"] == "LADDER_VIOLATION" and adopt(rvk).get("adopted") is None,
           f"⛔음성 Codex EP 조건부 검사기: 옛 러너 반송 (끝 기록 code 1) 의 killed.json sched_job_id 빈 문자열 → {rvk['attempts']['c2']['status']} · {rvk['status']}")
        exv = cp_(exso, "ex_ep_rempty"); rpe = os.path.join(exv, "run_aborted", f"{JOB}_c1_1", "infra_abort.json"); dre = json.loads(open(rpe, encoding="utf-8").read())
        dre["reason"] = ""; _write(rpe, json.dumps(dre, ensure_ascii=False) + "\n"); rve = rechk(exv)
        ck(rve["status"] == "LADDER_VIOLATION" and any("비었다" in v for v in rve["ladder_violations"]), f"⛔음성 Codex EP 조건부 검사기: 중단 영수증 reason 빈 문자열 → {rve['status']}")
        # EP 조건부 ⑤: 비 UTF-8 사유 — 쓸 때 거부 (기록하지 않는다)
        wu8, _, _ = run_pkg("ep_u8", {"A5": "conv", "c1": "plateau", "c2": "plateau@3"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c2"}, session=True)
        pu8 = subprocess.run(["bash", os.path.join(wu8, "run_a5.sh"), "--killed", "c2", "sched-9", "2026-11-23T00:00:00Z", b"walltime \xe9t\xe9"], cwd=wu8,
                             env={**os.environ, "WALL_S": "100"}, capture_output=True, timeout=120)
        o8 = (pu8.stdout + pu8.stderr).decode("utf-8", "replace")
        ck(pu8.returncode == 2 and not os.path.exists(os.path.join(D(wu8, "c2"), "killed.json")) and "UTF-8" in o8,
           f"⛔음성 Codex EP 조건부: --killed 사유에 비 UTF-8 바이트 (0xE9) → 종료 {pu8.returncode} · 기록 {'함' if os.path.exists(os.path.join(D(wu8, 'c2'), 'killed.json')) else '안 함'}")
        wu8b, rcu8b, _ = run_pkg("ep_u8b", {"A5": "zero"})
        pu8b = subprocess.run(["bash", os.path.join(wu8b, "run_a5.sh"), "--infra-abort", "A5", "sched-1", "2026-11-23T00:00:00Z", b"node \xe9"], cwd=wu8b,
                              env={**os.environ, "WALL_S": "10"}, capture_output=True, timeout=120)
        ck(rcu8b == 7 and pu8b.returncode == 2 and os.path.isdir(D(wu8b, "A5")) and not os.path.isdir(os.path.join(wu8b, "run_aborted")),
           f"⛔음성 Codex EP 조건부: --infra-abort 사유에 비 UTF-8 바이트 → 종료 {pu8b.returncode} · 폴더 그대로 · 영수증 없음")
        # EP P2 ⑥: 장부 순서 — 실제 A5 → c1 중단인데 장부 줄 · 폴더 번호를 c1#1 → A5#2 로 맞바꿈 → 러너 8 (c1 안 띄움) · 검사기 LADDER_VIOLATION
        wr_, rcr1, _ = run_pkg("ep_rev", {"A5": "zero"})
        prA = rcmd(wr_, "--infra-abort", "A5", "sched-1", "2026-11-23T00:00:00Z", "node", env_extra={"WALL_S": "10"})
        _, rcr2, _ = run_pkg("ep_rev", {"A5": "conv", "c1": "zero"}, fresh=False)
        prC = rcmd(wr_, "--infra-abort", "c1", "sched-2", "2026-11-23T00:00:01Z", "node", env_extra={"WALL_S": "10"})
        wr2 = cp_(wr_, "w_ep_rev_ok")                     # 맞바꾸지 않은 쪽 (양성 대조 · 검사기 시험의 원본)

        def swap_(b_):
            ra_ = os.path.join(b_, "run_aborted")
            os.rename(os.path.join(ra_, f"{JOB}_A5_1"), os.path.join(ra_, f"{JOB}_A5_2")); os.rename(os.path.join(ra_, f"{JOB}_c1_2"), os.path.join(ra_, f"{JOB}_c1_1"))
            lp_ = os.path.join(b_, "run", "infra_aborts.tsv"); L_ = open(lp_).read().split("\n")
            _write(lp_, "\n".join([L_[0], L_[2].replace(f"{JOB}_c1_2", f"{JOB}_c1_1"), L_[1].replace(f"{JOB}_A5_1", f"{JOB}_A5_2")] + L_[3:]))
        swap_(wr_)
        _, rcr3, _ = run_pkg("ep_rev", {"A5": "conv", "c1": "conv"}, fresh=False)
        _, rcr4, _ = run_pkg("ep_rev_ok", {"A5": "conv", "c1": "conv"}, fresh=False)
        rro, exro = chk(wr2)
        swap_(exro)
        fjr = os.path.join(exro, "run", "final.json"); dfr = json.loads(open(fjr).read()); dfr["attempts"] = attempts_of(exro, J_); _write(fjr, json.dumps(dfr) + "\n")
        rvr = rechk(exro)
        ck(rcr1 == 7 and prA[0] == 0 and rcr2 == 7 and prC[0] == 0 and rcr3 == 8 and not os.path.isdir(D(wr_, "c1")) and rcr4 == 0 and rro["status"] == "OK"
           and rvr["status"] == "LADDER_VIOLATION" and any(("순서" in v or "rung_order" in v) for v in rvr["ladder_violations"]),
           f"⛔음성 Codex EP P2: 장부 줄 · 폴더 번호를 c1#1 → A5#2 로 맞바꿈 → 러너 {rcr3} (c1 {'뜸' if os.path.isdir(D(wr_, 'c1')) else '안 뜸'}) · 검사기 {rvr['status']} · "
           f"양성 {rcr4} {rro['status']} — {rvr['ladder_violations'][:2]}")
        # ═══ Codex EQ (11-23) — 트리 관문 하나: 모르는 것 · 못 읽는 것 · 서로 안 맞는 것은 아무것도 쓰지 않고 멈춤 8 (러너 tree5 = 검사기 tree_problems) ═══
        import hashlib as _hl

        def snap(w_):                                      # 트리 바이트 지문 (run · run_aborted · 반송본 — 잠금 폴더 빼고) — '아무것도 쓰지 않았다' 를 바이트로 본다
            h_ = _hl.sha256()
            for root_ in ("run", "run_aborted"):
                for dp_, dns_, fns_ in os.walk(os.path.join(w_, root_)):
                    dns_[:] = sorted(x_ for x_ in dns_ if x_ != ".a5.lock")
                    for fn_ in sorted(fns_):
                        p_ = os.path.join(dp_, fn_); h_.update(os.path.relpath(p_, w_).encode() + b"\0" + open(p_, "rb").read() + b"\0")
            for f_ in ("a5_return.tgz", "a5_return.tgz.sha256"):
                if os.path.isfile(os.path.join(w_, f_)):
                    h_.update(f_.encode() + open(os.path.join(w_, f_), "rb").read())
            return h_.hexdigest()
        junker = os.path.join(T, "junker.sh")          # 그 단의 VASP 가 시도 폴더에 표준 밖 이름 (core.1) 을 남김
        _write(junker, f"#!/bin/bash\n{py} {fake}; r=$?\ncase \"$(basename \"$PWD\")\" in *_\"${{FAKE_JUNK_STAGE:-none}}\") echo core > core.1;; esac\nexit $r\n")
        os.chmod(junker, 0o755)
        PB = {"PATH": bind + os.pathsep + os.environ.get("PATH", "")}
        # EQ P0 ① (Q-EQ-1): c2 첫 행 앞 빈칸 두 칸 + 'SDA' 절단 → --infra-abort 거부 · 다시 돌림 8 (전에는 0 스텝으로 받고 c2 다시 · OK · c2 채택)
        wq1, _, _ = run_pkg("eq_sda2", {"A5": "conv", "c1": "plateau", "c2": "plateau@0|  SDA"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c2"}, session=True)
        pq1 = rcmd(wq1, "--infra-abort", "c2", "sched-9", "2026-11-23T00:00:00Z", "node", env_extra={"WALL_S": "100"})
        _, rcq1, _ = run_pkg("eq_sda2", {"A5": "conv", "c1": "plateau", "c2": "conv"}, fresh=False)
        rq1, _ = chk(wq1)
        ck(pq1[0] == 2 and rcq1 == 8 and fcode(wq1) == 8 and rq1["status"] == "STOPPED_FOR_REVIEW" and not os.path.isdir(os.path.join(wq1, "run_aborted"))
           and adopt(rq1).get("adopted") is None,
           f"⛔음성 Codex EQ P0: 앞 빈칸 + 'SDA' 절단 → --infra-abort {pq1[0]} · 다시 돌림 {rcq1} · {rq1['status']} · 채택 {adopt(rq1).get('adopted')}")
        # EQ P0 ② (Q-EQ-1): c2 유일 행 에너지 칸 310 자리 (실행 실패) → 손상 → 종료 8 · 채택 없음 (전에는 RUN_FAILED 근거 → c1 보조)
        r310 = "SDA:   1   " + "1" * 310 + "   -0.10000E+00   -0.10000E+00  8000   0.300E-03\\n"
        wq2, rcq2, _ = run_pkg("eq_310", {"A5": "conv", "c1": "plateau", "c2": "crash@0|" + r310})
        rq2, _ = chk(wq2); sq2 = [r_ for r_ in stat_rows(wq2) if r_[1] == "c2"]
        ck(rcq2 == 8 and len(sq2) == 1 and sq2[0][4] == "SCF_UNVERIFIED" and sq2[0][8] == "incomplete_row" and rq2["status"] == "STOPPED_FOR_REVIEW"
           and adopt(rq2).get("adopted") is None,
           f"⛔음성 Codex EQ P0: c2 유일 행 에너지 310 자리 → 종료 {rcq2} · {sq2[:1]} · {rq2['status']} · 채택 {adopt(rq2).get('adopted')}")
        # EQ P0 ③ (Q-EQ-2): 648001 s 로 끝난 c1 (상한 넘음 · 대조군 끝 5) 에 남의 0 초 killed.json 복사 → 러너 8 (c2 안 띄움 · 아무것도 안 씀) · 검사기 LADDER_VIOLATION
        wqk, _, _ = run_pkg("eq_kc", {"A5": "conv", "c1": "plateau", "c2": "conv"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c2"}, session=True)
        shutil.rmtree(D(wqk, "c2"))
        ajq = os.path.join(D(wqk, "c1"), "attempt.json"); _write(ajq, re.sub(r'"elapsed_s": [0-9]+', '"elapsed_s": 648001', open(ajq).read(), count=1))
        ridq = json.loads(open(ajq).read())["run_id"]; spq = os.path.join(wqk, "run", "status.tsv")      # 이력 줄도 같은 벽시계 (끝 기록과 이력 줄을 함께 쓴 뒤 끊긴 꼴 · Codex ER Q-ER-3①)
        _write(spq, "\n".join(("\t".join(l_.split("\t")[:9] + ["648001"] + l_.split("\t")[10:]) if l_.endswith("\t" + ridq) else l_) for l_ in open(spq).read().split("\n")))
        wqk0 = cp_(wqk, "w_eq_kc0"); _, rcqk0, _ = run_pkg("eq_kc0", {"A5": "conv", "c1": "plateau", "c2": "conv"}, fresh=False)
        wqk1 = cp_(wqk, "w_eq_kc1"); _write(os.path.join(D(wqk1, "c1"), "killed.json"), json.dumps({**kb0, "wall_s": "0"}) + "\n"); s0q = snap(wqk1)
        _, rcqk1, logqk1 = run_pkg("eq_kc1", {"A5": "conv", "c1": "plateau", "c2": "conv"}, fresh=False)
        rqk1 = rechk(cp_(wqk1, "ex_eq_kc1"))
        ck(rcqk0 == 5 and fcode(wqk0) == 5 and rcqk1 == 8 and fcode(wqk1) is None and not os.path.isdir(D(wqk1, "c2")) and snap(wqk1) == s0q and "end_and_killed" in logqk1
           and rqk1["status"] == "LADDER_VIOLATION" and any("end_and_killed" in v for v in rqk1["ladder_violations"]),
           f"⛔음성 Codex EQ P0: 648001 s c1 대조군 {rcqk0} · 남의 killed.json 복사 → 러너 {rcqk1} (c2 {'뜸' if os.path.isdir(D(wqk1, 'c2')) else '안 뜸'}) · 검사기 {rqk1['status']}")
        # EQ P1 ① (Q-EQ-3): 정상 완료 뒤 run/ 만 A5 직후로 복구 (완료 반송본 · sha 그대로) → 러너 8 · 반송본 그대로 · c1 다시 안 띄움 (전에는 두 단을 새 ID 로 다시 돌리고 반송본을 덮음)
        wqr = cp_(w2, "w_eq_restore")
        for s_ in ("c1", "c2"):
            shutil.rmtree(D(wqr, s_)); drop_rows(wqr, s_)
        for f_ in ("final.json", "start_point.json"):
            os.remove(os.path.join(wqr, "run", f_))
        s0r = snap(wqr); _, rcqr, logqr = run_pkg("eq_restore", {"A5": "noconv", "c1": "plateau", "c2": "conv"}, fresh=False)
        ck(rcqr == 8 and snap(wqr) == s0r and not os.path.isdir(D(wqr, "c1")) and "tgz_" in logqr,
           f"⛔음성 Codex EQ P1: run/ 를 A5 직후로 복구 + 완료 반송본 → 러너 {rcqr} · 트리 · 반송본 {'그대로' if snap(wqr) == s0r else '바뀜'} — {logqr.strip()[-100:]}")
        wqi, _, _ = run_pkg("eq_mid", {"A5": "conv", "c1": "plateau@7", "c2": "conv"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c1"}, session=True)
        pqi = pack_only(wqi)
        pqik = rcmd(wqi, "--killed", "c1", "sched-3", "2026-11-23T00:00:00Z", "walltime", env_extra={"WALL_S": "100"})
        _, rcqi, _ = run_pkg("eq_mid", {"A5": "conv", "c1": "plateau@7", "c2": "conv"}, fresh=False)
        rqi, _ = chk(wqi)
        ck(pqi == 0 and pqik[0] == 0 and rcqi == 0 and rqi["status"] == "OK",
           f"Codex EQ P1 양성: 끝 기록 없는 중간 포장 (PACK_ONLY) 뒤 --killed · 이어 돌림 → 트리 ⊇ 반송본 → {pqi} · {pqik[0]} · {rcqi} · {rqi['status']}")
        # EQ P1 ② (Q-EQ-3): status.tsv 0 바이트 → 러너 8 (c1 안 띄움 · 전에는 머리 검사를 건너뛰고 c1 · c2) — 머리만 있는 파일은 모든 새 실행이 받는다
        wqa, _, _ = run_pkg("eq_abase", {"A5": "conv", "c1": "plateau@7", "c2": "conv"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c1"}, session=True)
        qa_base = cp_(wqa, "eq_abase_clean"); shutil.rmtree(D(qa_base, "c1"))          # A5 끝 · 시작점 기록 뒤 c1 준비 실패와 같은 트리 (c1 안 띄움)
        wq5 = cp_(qa_base, "w_eq_st0"); _write(os.path.join(wq5, "run", "status.tsv"), ""); s05 = snap(wq5)
        _, rcq5, logq5 = run_pkg("eq_st0", {"A5": "conv", "c1": "conv"}, fresh=False)
        hq5 = history_problems(J_, wq5)
        ck(rcq5 == 8 and snap(wq5) == s05 and not os.path.isdir(D(wq5, "c1")) and "status_empty" in logq5 and any("status_empty" in p_ for p_ in hq5),
           f"⛔음성 Codex EQ P1: status.tsv 0 바이트 → 러너 {rcq5} · 검사기 {hq5[:1]} (같은 낱말 status_empty)")
        # EQ P1 ③ (Q-EQ-4): 잘린 끝 기록 — A5 attempt.json 끝 중괄호 유실 · t_start 뒤 '.5' → 러너 8 (c1 안 띄움 · 전에는 c1 · c2 를 돌리고 0)
        for i_, how_ in enumerate(("brace", "dot5")):
            wqt = cp_(qa_base, f"w_eq_trunc{i_}"); ajt = os.path.join(D(wqt, "A5"), "attempt.json"); tx_ = open(ajt).read()
            _write(ajt, (tx_.rstrip("\n")[:-1] + "\n") if how_ == "brace" else re.sub(r'("t_start": [0-9]+)', r'\1.5', tx_, count=1))
            s0t = snap(wqt); _, rcqt, logqt = run_pkg(f"eq_trunc{i_}", {"A5": "conv", "c1": "conv"}, fresh=False)
            ck(rcqt == 8 and snap(wqt) == s0t and not os.path.isdir(D(wqt, "c1")) and "att_form" in logqt, f"⛔음성 Codex EQ P1: A5 attempt.json {how_} → 러너 {rcqt}")
        # EQ P1 ④: 봉인 — 끝난 A5 의 OUTCAR 가 끝 기록 (sha 표) 뒤에 바뀜 → 러너 8 (전에는 이어 돌림 · 검사기만 ATTEMPT_MISMATCH)
        wqs = cp_(qa_base, "w_eq_seal"); open(os.path.join(D(wqs, "A5"), "OUTCAR"), "a").write(" \n"); s0s = snap(wqs)
        _, rcqs, logqs = run_pkg("eq_seal", {"A5": "conv", "c1": "conv"}, fresh=False)
        ck(rcqs == 8 and snap(wqs) == s0s and not os.path.isdir(D(wqs, "c1")) and "seal_OUTCAR" in logqs, f"⛔음성 Codex EQ: 끝난 A5 OUTCAR 가 봉인과 다름 → 러너 {rcqs}")
        # EQ P1 ⑤ (Q-EQ-4): 재포장이 현장 오류를 지움 — 끝난 사다리의 c1 폴더에 infra_abort.json.part · c1 끝 기록 신원 다름 · final.json code 0 + REVIEW
        #   → PACK_ONLY 8 · 다시 돌림 (재사용) 8 · 트리 · 반송본 · env.txt 바이트 그대로 / 검사기 (현장 트리 그대로) LADDER_VIOLATION
        for i_, how_ in enumerate(("part", "eid", "code0rev")):
            wqp = cp_(w1, f"w_eq_pack{i_}")
            if how_ == "part":
                _write(os.path.join(D(wqp, "c1"), "infra_abort.json.part"), "{")
            elif how_ == "eid":
                ajp_ = os.path.join(D(wqp, "c1"), "attempt.json"); _write(ajp_, open(ajp_).read().replace('"run_id": "', '"run_id": "9', 1))
            else:
                fjp_ = os.path.join(wqp, "run", "final.json"); _write(fjp_, open(fjp_).read().replace('"state": "OK"', '"state": "REVIEW"', 1))
            s0p = snap(wqp); pqp = pack_only(wqp); _, rcqp, _ = run_pkg(f"eq_pack{i_}", {}, fresh=False)
            rqp = rechk(cp_(wqp, f"ex_eq_pack{i_}"))
            ck(pqp == 8 and rcqp == 8 and snap(wqp) == s0p and rqp["status"] == "LADDER_VIOLATION" and adopt(rqp).get("adopted") is None,
               f"⛔음성 Codex EQ P1: 끝난 사다리 {how_} → PACK_ONLY {pqp} · 다시 돌림 {rcqp} · 트리 {'그대로' if snap(wqp) == s0p else '바뀜'} · 검사기 {rqp['status']}")
        # EQ P1 ⑥ (Q-EQ-5): 필수 칸 빈칸만 (잡 ID '   ') → --killed · --infra-abort 거부 (쓰지 않는다)
        wqb = cp_(wqa, "w_eq_blank"); pqb1 = rcmd(wqb, "--killed", "c1", "   ", "2026-11-23T00:00:00Z", "walltime", env_extra={"WALL_S": "100"})
        wqb0, rcqb0, _ = run_pkg("eq_blank0", {"A5": "zero"})
        pqb2 = rcmd(wqb0, "--infra-abort", "A5", "   ", "2026-11-23T00:00:00Z", "node", env_extra={"WALL_S": "10"})
        ck(pqb1[0] == 2 and not os.path.exists(os.path.join(D(wqb, "c1"), "killed.json")) and rcqb0 == 7 and pqb2[0] == 2 and not os.path.isdir(os.path.join(wqb0, "run_aborted")),
           f"⛔음성 Codex EQ P1: 잡 ID 빈칸 세 칸 → --killed {pqb1[0]} · --infra-abort {pqb2[0]} (둘 다 2 · 기록 없음)")
        pqb3 = rcmd(wqb, "--killed", "c1", "sched-3", "\x0b\x0c", "walltime", env_extra={"WALL_S": "100"})
        pqb4 = rcmd(wqb0, "--infra-abort", "A5", "sched-4", "2026-11-23T00:00:00Z", " \x0c\x0b ", env_extra={"WALL_S": "10"})
        ck(pqb3[0] == 2 and not os.path.exists(os.path.join(D(wqb, "c1"), "killed.json")) and pqb4[0] == 2 and not os.path.isdir(os.path.join(wqb0, "run_aborted")),
           f"⛔음성 Codex EQ P1: 취소 시각 VT · FF 만 → --killed {pqb3[0]} · 사유 공백 · FF · VT 만 → --infra-abort {pqb4[0]} (둘 다 2 · 기록 없음 — 읽을 때 규칙과 같은 집합)")
        # EQ P1 ⑦ (Q-EQ-5): 저장 뒤 영수증 사유 한 바이트 손상 (0xE9 — 비 UTF-8) → 러너 8 (c1 안 띄움) · 검사기 LADDER_VIOLATION
        wqd = cp_(sp_base, "w_eq_byte"); exd = cp_(exso, "ex_eq_byte")
        for b_ in (wqd, exd):
            rpd = os.path.join(b_, "run_aborted", f"{JOB}_c1_1", "infra_abort.json"); bd_ = open(rpd, "rb").read(); ir_ = bd_.index(b'"reason": "') + len(b'"reason": "')
            open(rpd, "wb").write(bd_[:ir_] + b"\xe9" + bd_[ir_ + 1:])
        s0d = snap(wqd); _, rcqd, logqd = run_pkg("eq_byte", {"A5": "conv", "c1": "conv"}, fresh=False); rvd = rechk(exd)
        ck(rcqd == 8 and snap(wqd) == s0d and not os.path.isdir(D(wqd, "c1")) and "utf8_infra_abort.json" in logqd and rvd["status"] == "LADDER_VIOLATION"
           and any("utf8_infra_abort.json" in v for v in rvd["ladder_violations"]),
           f"⛔음성 Codex EQ P1: 저장 뒤 영수증 사유 바이트 손상 → 러너 {rcqd} · 검사기 {rvd['status']}")
        # EQ P2 (Q-EQ-5): 같은 초 (모의 시계 고정) 의 장부 맞바꿈 c1#1 → A5#2 → 러너 8 (c1 안 띄움) · 검사기 LADDER_VIOLATION — 시간 순서만으로는 통과했다 (단 순서 대조)
        FN = {"FAKE_NOW": "1795400000"}
        wqn, _, _ = run_pkg("eq_ss", {"A5": "zero"}, env_extra=FN)
        rcmd(wqn, "--infra-abort", "A5", "sched-1", "2026-11-23T00:00:00Z", "node", env_extra={"WALL_S": "10", **FN, **PB})
        run_pkg("eq_ss", {"A5": "conv", "c1": "zero"}, fresh=False, env_extra=FN)
        rcmd(wqn, "--infra-abort", "c1", "sched-2", "2026-11-23T00:00:00Z", "node", env_extra={"WALL_S": "10", **FN, **PB})
        wqn2 = cp_(wqn, "w_eq_ss_ok"); swap_(wqn); s0n = snap(wqn)
        _, rcqn, logqn = run_pkg("eq_ss", {"A5": "conv", "c1": "conv"}, fresh=False, env_extra=FN)
        _, rcqn2, _ = run_pkg("eq_ss_ok", {"A5": "conv", "c1": "conv"}, fresh=False, env_extra=FN)
        rqn2, exqn = chk(wqn2); swap_(exqn)
        fjn = os.path.join(exqn, "run", "final.json"); dfn = json.loads(open(fjn).read()); dfn["attempts"] = attempts_of(exqn, J_); _write(fjn, json.dumps(dfn) + "\n")
        rvn_ = rechk(exqn)
        ck(rcqn == 8 and snap(wqn) == s0n and not os.path.isdir(D(wqn, "c1")) and "rung_order" in logqn and rcqn2 == 0 and rqn2["status"] == "OK"
           and rvn_["status"] == "LADDER_VIOLATION" and any("rung_order" in v for v in rvn_["ladder_violations"]),
           f"⛔음성 Codex EQ P2: 같은 초 장부 맞바꿈 → 러너 {rcqn} · 양성 {rcqn2} {rqn2['status']} · 검사기 {rvn_['status']}")
        FT1, FT2 = {"FAKE_NOW": "1795400000"}, {"FAKE_NOW": "1795400100"}
        wto, _, _ = run_pkg("eq_to", {"A5": "zero"}, env_extra=FT1)
        pto1 = rcmd(wto, "--infra-abort", "A5", "sched-1", "2026-11-23T00:00:00Z", "node", env_extra={"WALL_S": "10", **FT1, **PB})
        run_pkg("eq_to", {"A5": "zero"}, fresh=False, env_extra=FT2)
        pto2 = rcmd(wto, "--infra-abort", "A5", "sched-2", "2026-11-23T00:01:40Z", "node", env_extra={"WALL_S": "10", **FT2, **PB})
        wto2 = cp_(wto, "w_eq_to_ok")

        def lswap_(b_):                                # 장부 줄 · 폴더 번호를 함께 맞바꿈 (줄 i ↔ <잡>_A5_i 는 그대로 맞게 — 시각만 거꾸로)
            ra_ = os.path.join(b_, "run_aborted"); a1_, a2_ = os.path.join(ra_, f"{JOB}_A5_1"), os.path.join(ra_, f"{JOB}_A5_2")
            os.rename(a1_, a1_ + ".t"); os.rename(a2_, a1_); os.rename(a1_ + ".t", a2_)
            lp_ = os.path.join(b_, "run", "infra_aborts.tsv"); L_ = open(lp_).read().split("\n")
            _write(lp_, "\n".join([L_[0], L_[2].replace(f"{JOB}_A5_2", f"{JOB}_A5_1"), L_[1].replace(f"{JOB}_A5_1", f"{JOB}_A5_2")] + L_[3:]))
        lswap_(wto); s0to = snap(wto)
        _, rcto, logto = run_pkg("eq_to", {"A5": "conv", "c1": "conv"}, fresh=False, env_extra=FT2)
        _, rcto2, _ = run_pkg("eq_to_ok", {"A5": "conv", "c1": "conv"}, fresh=False, env_extra=FT2)
        rto2, exto = chk(wto2); lswap_(exto)
        fjt = os.path.join(exto, "run", "final.json"); dft = json.loads(open(fjt).read()); dft["attempts"] = attempts_of(exto, J_); _write(fjt, json.dumps(dft) + "\n")
        rvto = rechk(exto)
        ck(pto1[0] == 0 and pto2[0] == 0 and rcto == 8 and snap(wto) == s0to and "ledger_time_order" in logto and "rung_order" not in logto
           and rcto2 == 0 and rto2["status"] == "OK" and rvto["status"] == "LADDER_VIOLATION" and any("ledger_time_order" in v for v in rvto["ladder_violations"])
           and not any("rung_order" in v for v in rvto["ladder_violations"]),
           f"⛔음성 Codex EP P2 (EQ 뒤 떼어 냄): 같은 단 A5#1 · A5#2 (다른 시각) 장부 줄만 맞바꿈 → 러너 {rcto} · 양성 {rcto2} {rto2['status']} · 검사기 {rvto['status']} — 단 순서는 그대로 · 시각 순서만")
        # 관문 자리 (진입점마다 같은 tree5): 발사 직전 · 끝 포장 · 다시 돌림 (잠금 다음 · env.txt 전) · 기록 명령
        wqj1, rcqj1, logqj1 = run_pkg("eq_junkA5", {"A5": "conv", "c1": "conv"}, vasp=junker, env_extra={"FAKE_JUNK_STAGE": "A5"})
        ck(rcqj1 == 8 and not os.path.isdir(D(wqj1, "c1")) and fcode(wqj1) is None and "core.1" in logqj1 and "발사 직전" in logqj1,
           f"⛔음성 Codex EQ 관문 (c1 발사 직전): A5 폴더에 표준 밖 이름 (core.1) → 러너 {rcqj1} · c1 {'뜸' if os.path.isdir(D(wqj1, 'c1')) else '안 뜸'}")
        wqj2, rcqj2, logqj2 = run_pkg("eq_junkc1", {"A5": "conv", "c1": "conv"}, vasp=junker, env_extra={"FAKE_JUNK_STAGE": "c1"})
        ck(rcqj2 == 8 and fcode(wqj2) is None and os.path.isfile(os.path.join(D(wqj2, "A5"), "WAVECAR")) and not os.path.exists(os.path.join(wqj2, "a5_return.tgz")) and "WAVECAR 지우기 전" in logqj2,
           f"⛔음성 Codex EQ · ER 관문 (마지막 단 뒤 · WAVECAR 지우기 · 끝 기록 전): c1 폴더에 core.1 → 러너 {rcqj2} · 끝 기록 {fcode(wqj2)} · 반송본 {'없음' if not os.path.exists(os.path.join(wqj2, 'a5_return.tgz')) else '씀'}")
        wqe = cp_(qa_base, "w_eq_entry"); _write(os.path.join(wqe, "run", "final.json.part"), "{"); s0e = snap(wqe)
        _, rcqe, logqe = run_pkg("eq_entry", {"A5": "conv", "c1": "conv"}, fresh=False)
        ck(rcqe == 8 and snap(wqe) == s0e and "run_entry_final.json.part" in logqe and "다시 돌림" in logqe,
           f"⛔음성 Codex EQ 관문 (다시 돌림 · 무엇을 쓰기 전): run/final.json.part 잔여 → 러너 {rcqe} · 트리 {'그대로' if snap(wqe) == s0e else '바뀜 (env.txt?)'}")
        wqg = cp_(wqa, "w_eq_recgate"); _write(os.path.join(wqg, "run", "start_point.json.part"), "{"); s0g = snap(wqg)
        pqg = rcmd(wqg, "--killed", "c1", "sched-3", "2026-11-23T00:00:00Z", "walltime", env_extra={"WALL_S": "100"})
        ck(pqg[0] == 8 and snap(wqg) == s0g and not os.path.exists(os.path.join(D(wqg, "c1"), "killed.json")),
           f"⛔음성 Codex EQ 관문 (기록 명령): run/start_point.json.part 잔여 → --killed {pqg[0]} · 기록 {'함' if os.path.exists(os.path.join(D(wqg, 'c1'), 'killed.json')) else '안 함'}")
        # 기존 반송본 대조 (러너만 · 규칙마다): 끝 기록만 지움 → tgz_final_differs · 중간 포장 뒤 그 시도 폴더를 지움 → tgz_attempt_missing ·
        #   중간 포장 뒤 끝난 시도의 끝 기록을 지움 → tgz_end_differs — 모두 종료 8 · 트리 · 반송본 바이트 그대로
        wqf = cp_(w1, "w_eq_finlost"); os.remove(os.path.join(wqf, "run", "final.json")); s0f = snap(wqf)
        _, rcqf, logqf = run_pkg("eq_finlost", {"A5": "conv", "c1": "conv"}, fresh=False)
        ck(rcqf == 8 and snap(wqf) == s0f and "tgz_final_differs" in logqf, f"⛔음성 Codex EQ P1: 끝 기록만 지운 트리 + 완료 반송본 → 러너 {rcqf} (반송본을 다시 쓰지 않음)")
        wqm2, _, _ = run_pkg("eq_mr", {"A5": "conv", "c1": "plateau@7", "c2": "conv"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c1"}, session=True)
        pqm = rcmd(wqm2, "--killed", "c1", "sched-3", "2026-11-23T00:00:00Z", "walltime", env_extra={"WALL_S": "100"})
        pqm2 = pack_only(wqm2); shutil.rmtree(D(wqm2, "c1")); s0m = snap(wqm2)
        _, rcqm3, logqm3 = run_pkg("eq_mr", {"A5": "conv", "c1": "plateau@7", "c2": "conv"}, fresh=False)
        ck(pqm[0] == 0 and pqm2 == 0 and rcqm3 == 8 and snap(wqm2) == s0m and "tgz_attempt_missing" in logqm3,
           f"⛔음성 Codex EQ P1: 중간 포장 (끊긴 c1 기록 포함) 뒤 c1 폴더를 지움 → 러너 {rcqm3} (c1 다시 안 띄움)")
        wqd2, _, _ = run_pkg("eq_ed", {"A5": "conv", "c1": "plateau", "c2": "conv"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c2"}, session=True)
        pqd = pack_only(wqd2); os.remove(os.path.join(D(wqd2, "c1"), "attempt.json")); drop_rows(wqd2, "c1"); s0d2 = snap(wqd2)
        _, rcqd2, logqd2 = run_pkg("eq_ed", {"A5": "conv", "c1": "plateau", "c2": "conv"}, fresh=False)
        ck(pqd == 0 and rcqd2 == 8 and snap(wqd2) == s0d2 and "tgz_end_differs" in logqd2,
           f"⛔음성 Codex EQ P1: 중간 포장 (끝난 c1) 뒤 c1 끝 기록 · 이력 줄을 지움 (끝나기 전 체크포인트) → 러너 {rcqd2}")
        # 쓰는 쪽: 끝 기록은 임시 파일에 완성한 뒤 mv — mv 실패 (디스크) 흉내 → 그 자리에서 종료 8 · 끝 기록 없음 · 다음 실행은 남은 .part 로 트리 관문 8
        _write(os.path.join(bind, "mv"), "#!/bin/bash\nlast=\"\"; for a in \"$@\"; do last=$a; done\n"
               "if [ -n \"${FAKE_MV_FAIL:-}\" ]; then case \"$last\" in *\"$FAKE_MV_FAIL\") echo 'mv: No space left on device' >&2; exit 1;; esac; fi\n"
               f"exec {shutil.which('mv')} \"$@\"\n")
        os.chmod(os.path.join(bind, "mv"), 0o755)
        wqv, rcqv1, _ = run_pkg("eq_mvfail", {"A5": "conv", "c1": "conv"}, env_extra={"FAKE_MV_FAIL": "_A5/attempt.json"})
        _, rcqv2, logqv2 = run_pkg("eq_mvfail", {"A5": "conv", "c1": "conv"}, fresh=False)
        ck(rcqv1 == 8 and not os.path.isfile(os.path.join(D(wqv, "A5"), "attempt.json")) and os.path.isfile(os.path.join(D(wqv, "A5"), "attempt.json.part"))
           and not os.path.isdir(D(wqv, "c1")) and rcqv2 == 8 and "attempt.json.part" in logqv2,
           f"⛔음성 Codex EQ P1: 끝 기록 mv 실패 → 러너 {rcqv1} (끝 기록 없음 · c1 안 띄움) · 다시 {rcqv2} (남은 .part → 트리 관문)")
        # ── Codex ER 반례 (회신 글의 재현 설명대로 · 먼저 빨강 재현 → 고침) ──
        import time as time_
        # ER Q-ER-1①: 전자행 7 개 남은 끊긴 c1 을 같은 단 준비 폴더 이름 (.prep_<잡>_c1) 으로 옮김 → 지우지 않고 멈춤 (종료 8 · 보존 · 새 c1 없음)
        wr1, _, _ = run_pkg("er_prep", {"A5": "conv", "c1": "plateau@7", "c2": "conv"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c1"}, session=True)
        os.rename(D(wr1, "c1"), os.path.join(wr1, "run", f".prep_{JOB}_c1")); s0r1 = snap(wr1)
        _, rcr1, logr1 = run_pkg("er_prep", {"A5": "conv", "c1": "conv", "c2": "conv"}, fresh=False)
        ck(rcr1 == 8 and snap(wr1) == s0r1 and "prep_" in logr1 and not os.path.isdir(D(wr1, "c1")) and os.path.isfile(os.path.join(wr1, "run", f".prep_{JOB}_c1", "OSZICAR")),
           f"⛔음성 Codex ER Q-ER-1①: 전자행 7 개 끊긴 c1 을 .prep_…_c1 로 옮김 → 러너 {rcr1} (지우지 않음 · 새 c1 안 띄움)")
        # ER Q-ER-1②: 마지막 단 c1 이 core.1 을 남김 → 끝 기록 · WAVECAR 지우기 전에 관문 (끝 기록 없음 · A5 WAVECAR 그대로 · 반송본 없음)
        wr2, rcr2, logr2 = run_pkg("er_end", {"A5": "conv", "c1": "conv"}, vasp=junker, env_extra={"FAKE_JUNK_STAGE": "c1"})
        ck(rcr2 == 8 and fcode(wr2) is None and os.path.isfile(os.path.join(D(wr2, "A5"), "WAVECAR")) and not os.path.exists(os.path.join(wr2, "a5_return.tgz")) and "core.1" in logr2,
           f"⛔음성 Codex ER Q-ER-1②: 마지막 단 c1 이 core.1 을 남김 → 러너 {rcr2} · 끝 기록 {fcode(wr2)} · A5 WAVECAR {'그대로' if os.path.isfile(os.path.join(D(wr2, 'A5'), 'WAVECAR')) else '지워짐'}")
        wr2b, rcr2b, logr2b = run_pkg("er_end_rev", {"A5": "conv", "c1": "crash@0|SDA: 1 none missing missing abc bad\n"}, vasp=junker, env_extra={"FAKE_JUNK_STAGE": "c1"})
        ck(rcr2b == 8 and fcode(wr2b) is None and "core.1" in logr2b and not os.path.exists(os.path.join(wr2b, "a5_return.tgz")),
           f"⛔음성 Codex ER Q-ER-1②: c1 이 검토로 끝남 (WAVECAR 지우기 없이 끝 기록) + core.1 → 러너 {rcr2b} · 끝 기록 {fcode(wr2b)} (관문이 끝 기록 전에)")
        zq = {"SDA; 1 0 0 0 12 0\n": (0, "unexplained_line"), "SDA\n": (0, "unexplained_line"), hd_: (0, None), hd_ + "\n  \t\n": (0, None), hd_[:-1][:30]: (0, None),
              "  N": (0, None), "": (0, None), "   \n": (0, None), hd_.lstrip(" "): (0, "unexplained_line"),
              hd_ + "   1 F= -.73E+03 E0= -.73E+03  d E =-.73E+03\n": (0, "unexplained_line"), hd_ + sda1 + "   1 F= -.73E+03 E0= -.73E+03  d E =-.73E+03\n": (1, None),
              hd_ + "SDA x\n": (0, "unexplained_line")}
        zgot = {k_: row_gate(k_, "c2") for k_ in zq}
        ck(zgot == zq, f"Codex ER Q-ER-2: 0 스텝은 빈 줄 · 열 제목 (끝 조각은 그 앞부분) 만 — 다름 {[(k_[:30], zgot[k_], v_) for k_, v_ in zq.items() if zgot[k_] != v_]}")
        # ER Q-ER-2: 0 스텝은 0 행으로 설명되는 내용만 — 'SDA; 1 0 0 0 12 0' (콜론 → 세미콜론) · 'SDA' 한 줄 → --infra-abort 거부 (2) · 다시 돌림 검토 (8)
        for i_, osz_ in enumerate(("SDA; 1 0 0 0 12 0\n", "SDA\n")):
            wr3, _, _ = run_pkg(f"er_zero{i_}", {"A5": "conv", "c1": "plateau", "c2": "plateau@0|" + osz_}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c2"}, session=True)
            pr3 = rcmd(wr3, "--infra-abort", "c2", "sched-1", "2026-11-23T00:00:00Z", "node", env_extra={"WALL_S": "10"})
            _, rcr3, _ = run_pkg(f"er_zero{i_}", {"A5": "conv", "c1": "plateau", "c2": "conv"}, fresh=False)
            ck(pr3[0] == 2 and rcr3 == 8 and not os.path.isdir(os.path.join(wr3, "run_aborted")) and fcode(wr3) == 8,
               f"⛔음성 Codex ER Q-ER-2: c2 OSZICAR {osz_!r} → --infra-abort {pr3[0]} · 다시 돌림 {rcr3} (0 스텝 아님 · 검토)")

        # ER Q-ER-3①: c1 끝 기록 · 이력 줄 둘 다 648001 s (대조군 끝 5) → attempt.json 만 첫 숫자 유실 (48001) → 러너 8 (c2 안 띄움) · 검사기 LADDER_VIOLATION
        def set_el(w_, st_, secs_):
            aj_ = os.path.join(D(w_, st_), "attempt.json"); txt_ = open(aj_).read(); rid_ = json.loads(txt_)["run_id"]
            _write(aj_, re.sub(r'"elapsed_s": [0-9]+', f'"elapsed_s": {secs_}', txt_, count=1))
            sp_ = os.path.join(w_, "run", "status.tsv")
            _write(sp_, "\n".join(("\t".join(l_.split("\t")[:9] + [str(secs_)] + l_.split("\t")[10:]) if l_.endswith("\t" + rid_) else l_) for l_ in open(sp_).read().split("\n")))
        wr4, _, _ = run_pkg("er_el", {"A5": "conv", "c1": "plateau", "c2": "conv"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c2"}, session=True)
        shutil.rmtree(D(wr4, "c2")); set_el(wr4, "c1", 648001)
        cp_(wr4, "w_er_el_ok"); _, rcr4a, _ = run_pkg("er_el_ok", {"A5": "conv", "c1": "plateau", "c2": "conv"}, fresh=False)
        aj4 = os.path.join(D(wr4, "c1"), "attempt.json"); _write(aj4, open(aj4).read().replace('"elapsed_s": 648001', '"elapsed_s": 48001', 1)); s0r4 = snap(wr4)
        rvr4 = rechk(cp_(wr4, "ex_er_el"))
        _, rcr4, logr4 = run_pkg("er_el", {"A5": "conv", "c1": "plateau", "c2": "conv"}, fresh=False)
        ck(rcr4a == 5 and rcr4 == 8 and snap(wr4) == s0r4 and not os.path.isdir(D(wr4, "c2")) and rvr4["status"] == "LADDER_VIOLATION" and adopt(rvr4).get("adopted") is None,
           f"⛔음성 Codex ER Q-ER-3①: c1 끝 기록 48001 · 이력 줄 648001 → 러너 {rcr4} (대조군 {rcr4a}) · 검사기 {rvr4['status']}")
        # ER Q-ER-3②: 기록 명령 둘이 겹침 — 첫 --killed 가 검사를 마치고 쓰기 전에 멈춘 동안 둘째 --killed 는 거부 (2 · 잠금) · 첫 기록이 남는다
        _write(os.path.join(bind, "date"), "#!/bin/bash\n"           # 모의 시계 + 멈춤 (FAKE_DATE_PAUSE = 이 파일이 생길 때까지 · 기다리기 시작하면 .wait 표지) — 검사 뒤 · 쓰기 전 자리 ($(date)) 에서 세운다
               "if [ -n \"${FAKE_DATE_PAUSE:-}\" ]; then touch \"$FAKE_DATE_PAUSE.wait\"; i=0; while [ ! -e \"$FAKE_DATE_PAUSE\" ] && [ $i -lt 600 ]; do sleep 0.1; i=$((i+1)); done; fi\n"
               f"if [ -n \"${{FAKE_NOW:-}}\" ]; then exec {shutil.which('date')} -d \"@$FAKE_NOW\" \"$@\"; fi\nexec {shutil.which('date')} \"$@\"\n")
        os.chmod(os.path.join(bind, "date"), 0o755)
        wr5, _, _ = run_pkg("er_lock", {"A5": "conv", "c1": "plateau@7", "c2": "conv"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c1"}, session=True)
        go5 = os.path.join(T, "er_lock_go")
        p5 = subprocess.Popen(["bash", os.path.join(wr5, "run_a5.sh"), "--killed", "c1", "sched-1", "2026-11-23T00:00:00Z", "walltime"], cwd=wr5,
                              env={**os.environ, **PB, "WALL_S": "648001", "FAKE_DATE_PAUSE": go5}, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        t5 = time_.time()
        while not os.path.exists(go5 + ".wait") and p5.poll() is None and time_.time() - t5 < 60:
            time_.sleep(0.1)
        pr5 = rcmd(wr5, "--killed", "c1", "sched-2", "2026-11-23T00:00:00Z", "walltime", env_extra={"WALL_S": "0", **PB})
        open(go5, "w").close(); p5.communicate(timeout=120)
        kj5 = os.path.join(D(wr5, "c1"), "killed.json"); k5 = json.loads(open(kj5).read()) if os.path.isfile(kj5) else {}
        ck(pr5[0] == 2 and p5.returncode == 0 and k5.get("wall_s") == "648001" and k5.get("sched_job_id") == "sched-1",
           f"⛔음성 Codex ER Q-ER-3②: 겹친 --killed → 둘째 {pr5[0]} · 첫째 {p5.returncode} · 남은 기록 {k5.get('wall_s')} 초 ({k5.get('sched_job_id')})")
        # pack() 자체 관문 (m158): 앞 관문 (fin5 · drop5 · PACK_ONLY) 이 가리므로 따로 — PACK_ONLY 관문 뒤 · pack() 전 ($(utc) 자리) 에서 세우고 시도 폴더에 모르는 파일 → 포장 관문 8 (반송본 · 임시 파일 안 만듦)
        wpg = cp_(qa_base, "w_er_packgate"); gopg = os.path.join(T, "er_packgate_go"); tgzpg = os.path.join(wpg, "a5_return.tgz")
        tgpg0 = _sha(tgzpg) if os.path.isfile(tgzpg) else None
        ppg = subprocess.Popen(["bash", os.path.join(wpg, "run_a5.sh")], cwd=wpg, env={**os.environ, **PB, "PACK_ONLY": "1", "FAKE_DATE_PAUSE": gopg},
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        tpg = time_.time()
        while not os.path.exists(gopg + ".wait") and ppg.poll() is None and time_.time() - tpg < 60:
            time_.sleep(0.1)
        wtpg = os.path.exists(gopg + ".wait"); _write(os.path.join(D(wpg, "A5"), "junk.txt"), "x\n")
        open(gopg, "w").close(); outpg = ppg.communicate(timeout=120)[0]
        tgpg = _sha(tgzpg) if os.path.isfile(tgzpg) else None
        lfpg = [f_ for f_ in ("a5_return.tgz.part", "a5_return.tgz.sha256.part", "a5_return.tmp", "a5_return.list") if os.path.exists(os.path.join(wpg, f_))]
        ck(wtpg and ppg.returncode == 8 and "트리 관문 (포장)" in outpg and tgpg == tgpg0 and not lfpg,
           f"⛔음성 pack() 자체 관문 (m158): PACK_ONLY 관문 뒤 · 포장 전에 생긴 모르는 파일 → {ppg.returncode} (멈춤 {wtpg} · 포장 관문 {'트리 관문 (포장)' in outpg}) · 반송본 {'그대로' if tgpg == tgpg0 else '바뀜'} · 남은 임시 {lfpg}")
        # ER Q-ER-4: 중간 반송본 (c1 전자행 7) 뒤 같은 c1 폴더를 출력 전 체크포인트로 복구 → --infra-abort · 다시 돌림 모두 8 (트리 · 반송본 그대로)
        wr6, _, _ = run_pkg("er_rows", {"A5": "conv", "c1": "plateau@7", "c2": "conv"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c1"}, session=True)
        pk6 = pack_only(wr6)
        for f_ in os.listdir(D(wr6, "c1")):
            if f_ not in ("INCAR", "POSCAR", "KPOINTS", "POTCAR", "POTCAR.titel", "POTCAR.sha256", "POTCAR.species.sha256", "attempt.start", "WAVECAR"):
                os.remove(os.path.join(D(wr6, "c1"), f_))
        tg6 = _sha(os.path.join(wr6, "a5_return.tgz")); s0r6 = snap(wr6)
        pr6 = rcmd(wr6, "--infra-abort", "c1", "sched-1", "2026-11-23T00:00:00Z", "node", env_extra={"WALL_S": "10"})
        _, rcr6, logr6 = run_pkg("er_rows", {"A5": "conv", "c1": "conv", "c2": "conv"}, fresh=False)
        ck(pk6 == 0 and pr6[0] == 8 and rcr6 == 8 and snap(wr6) == s0r6 and _sha(os.path.join(wr6, "a5_return.tgz")) == tg6,
           f"⛔음성 Codex ER Q-ER-4: 중간 반송본 (c1 7 행) 뒤 c1 을 출력 전으로 복구 → --infra-abort {pr6[0]} · 다시 돌림 {rcr6} · 반송본 {'그대로' if _sha(os.path.join(wr6, 'a5_return.tgz')) == tg6 else '바뀜'}")
        # ER Q-ER-4: 중간 반송본에 648001 s 로 채운 영수증 → 영수증 · 장부를 채우기 전 (UNKNOWN) 으로 복구 → PACK_ONLY 8 (반송본 그대로)
        wr7, _, _ = run_pkg("er_rcpt", {"A5": "conv", "c1": "plateau@0", "c2": "conv"}, vasp=killer, env_extra={"FAKE_KILL_STAGE": "c1"}, session=True)   # 끊긴 0 스텝 (끝 기록 없음 → 영수증 벽시계 UNKNOWN)
        pr7 = rcmd(wr7, "--infra-abort", "c1", "sched-1", "2026-11-23T00:00:00Z", "node")
        ab7 = os.path.join(wr7, "run_aborted", f"{JOB}_c1_1")
        old7 = {p_: open(p_, "rb").read() for p_ in (os.path.join(ab7, "infra_abort.json"), os.path.join(wr7, "run", "infra_aborts.tsv"))}
        pw7 = rcmd(wr7, "--infra-wall", f"{JOB}_c1_1", "648001"); pk7 = pack_only(wr7); tg7 = _sha(os.path.join(wr7, "a5_return.tgz"))
        for p_, b_ in old7.items():
            open(p_, "wb").write(b_)
        s0r7 = snap(wr7); pk7b = pack_only(wr7)
        ck(pr7[0] == 0 and pw7[0] == 0 and pk7 == 0 and pk7b == 8 and _sha(os.path.join(wr7, "a5_return.tgz")) == tg7 and snap(wr7) == s0r7,
           f"⛔음성 Codex ER Q-ER-4: 채운 영수증 (648001) 을 UNKNOWN 으로 되돌림 → PACK_ONLY {pk7b} · 반송본 {'그대로' if _sha(os.path.join(wr7, 'a5_return.tgz')) == tg7 else '바뀜'}")
        # ER Q-ER-5: 끝난 A5 의 attempt.json job 한 글자 · POTCAR.sha256 한 자리 → 러너 8 (c1 안 띄움 · 트리 그대로) · 검사기 채택 없음
        for i_, how_ in enumerate(("job", "potcar")):
            wr8 = cp_(qa_base, f"w_er_endrec{i_}")
            if how_ == "job":
                aj8 = os.path.join(D(wr8, "A5"), "attempt.json"); _write(aj8, open(aj8).read().replace(f'"job": "{JOB}"', f'"job": "{JOB[:-1]}x"', 1))
            else:
                ps8 = os.path.join(D(wr8, "A5"), "POTCAR.sha256"); b8 = open(ps8).read(); _write(ps8, ("0" if b8[0] != "0" else "1") + b8[1:])
            s0r8 = snap(wr8); rvr8 = rechk(cp_(wr8, f"ex_er_endrec{i_}"))
            _, rcr8, logr8 = run_pkg(f"er_endrec{i_}", {"A5": "conv", "c1": "conv"}, fresh=False)
            ck(rcr8 == 8 and snap(wr8) == s0r8 and not os.path.isdir(D(wr8, "c1")) and rvr8["status"] != "OK" and adopt(rvr8).get("adopted") is None,
               f"⛔음성 Codex ER Q-ER-5: 끝난 A5 {how_} 손상 → 러너 {rcr8} (c1 {'뜸' if os.path.isdir(D(wr8, 'c1')) else '안 뜸'}) · 검사기 {rvr8['status']}")
        # 러너 ↔ 검사기 같은 문법 · 같은 규칙 (같은 탐침 · 러너 함수는 RUN_A5_ENV 에서 그대로 꺼낸다 — 손으로 옮기지 않는다)
        _ee = _env_text(); envf = _ee[_ee.index("stage_hdr(){"):_ee.index("stat5(){")]
        _retl = "\n".join(l_ for l_ in run_a5_text().splitlines() if l_.startswith(("RET_ALLOW=", "RET_FORBID=")))
        hsh = os.path.join(T, "eo_harness.sh")
        _write(hsh, f"set -u\nJOB={JOB}\nINFRA_MAX={INFRA_MAX}\n" + _retl + "\n" + r2_block("h(){") + "\n" + r2_block("secs_ok(){") + "\n" + envf + "\n" + r"""
case "$1" in
  rec) shift; for f in "$@"; do if r=$(rec5 "$f"); then printf '%s|OK\n%s\n' "$(basename "$f")" "$r"; else echo "$(basename "$f")|BAD"; fi; done;;
  jstr) shift; for a in "$@"; do printf '%s\n' "$(jstr "$a")"; done;;
  rows) shift; for d in "$@"; do echo "$(basename "$d")|$(row_scan "$d" "$(cat "$d/STAGE")")"; done;;
  start) shift; for d in "$@"; do echo "$(basename "$d")|$(start_id "$d" "$(cat "$d/STAGE")")"; done;;
  ledger) shift; for d in "$@"; do echo "$(basename "$d")|$(cd "$d" && ledger5)"; done;;
  tree) shift; for d in "$@"; do echo "$(basename "$d")|$(cd "$d" && tree5)"; done;;
  u8) shift; for a in "$@"; do if u8ok "$a"; then echo OK; else echo BAD; fi; done;;
  blank) shift; for a in "$@"; do if nbj "$a"; then echo OK; else echo BLANK; fi; done;;
  wblank) shift; for a in "$@"; do if nbw "$a"; then echo OK; else echo BLANK; fi; done;;
  wall) shift; B=$1; shift; for r in "$@"; do echo "$r|$(cd "$B" && wall_of "$r")"; done;;
esac
""")
        rprobes = {"canon": b'{"job": "X", "n": 5}\n', "nospace": b'{"job":"X","n":5}', "tabs": b'\t{ "job" :\t"X" , "n":5 }  \n', "comma": b'{"job": "X" "n": 5}\n',
                   "dup": b'{"a": "1", "a": "2"}\n', "twolines": b'{"a": "1",\n "b": 2}\n', "trail": b'{"a": "1"}x\n', "ctrl": b'{"a": "\x1b[31m"}\n',
                   "esc": b'{"a": "\\u001b[31m \\" \\\\ \\/"}\n', "badesc": b'{"a": "\\x"}\n', "lead0": b'{"a": 01}\n', "neg": b'{"a": -1}\n', "float": b'{"a": 1.5}\n',
                   "d17": b'{"a": 12345678901234567}\n', "d16": b'{"a": 1234567890123456}\n', "empty": b"", "brace": b"{}\n", "utf8": '{"a": "노드 고장"}\n'.encode(),
                   "badutf8": b'{"a": "\xff\xfe"}\n', "del": b'{"a": "\x7f"}\n', "unterm": b'{"a": "x}\n', "crlf": b'{"a": "x"}\r\n', "nul": b'{"a": "x\x00"}\n',
                   "upper": b'{"A": "x"}\n', "nested": b'{"a": {"b": 1}}\n', "twoLF": b'{"a": "x"}\n\n', "lf_only": b"\n", "u_short": b'{"a": "\\u12"}\n',
                   "bs_end": b'{"a": "x\\', "true": b'{"a": true}\n', "sp_key": b'{"a b": "x"}\n', "bom": b'\xef\xbb\xbf{"a": "x"}\n'}
        rdir = os.path.join(T, "eo_rec"); os.makedirs(rdir)
        for k_, v_ in rprobes.items():
            open(os.path.join(rdir, k_), "wb").write(v_)
        ho = subprocess.run(["bash", hsh, "rec", *[os.path.join(rdir, k_) for k_ in rprobes]], capture_output=True).stdout.decode("latin-1")
        rgot, cur_ = {}, None
        for ln in ho.split("\n"):
            if "|" in ln and ln.split("|")[0] in rprobes:
                cur_ = ln.split("|")[0]; rgot[cur_] = None if ln.endswith("|BAD") else {}
            elif ln and cur_ and rgot.get(cur_) is not None:
                k_, t_, v_ = ln.split("\t", 2); rgot[cur_][k_] = (t_, int(v_) if t_ == "i" else v_)
        rdiff = {k_: (rec_parse(v_), rgot.get(k_)) for k_, v_ in rprobes.items() if rec_parse(v_) != rgot.get(k_)}
        nacc = sum(1 for v_ in rgot.values() if v_ is not None)
        ck(not rdiff and len(rgot) == len(rprobes) and 6 <= nacc <= 10, f"러너 rec5 = 검사기 rec_parse ({len(rprobes)} 탐침 · 받음 {nacc} · 칸 원문까지) — 다름 {rdiff}")
        bprobes = ["", "   ", "\\t", "\\n \\r\\f", "\\u0009\\u000A\\u000b\\u000C\\u000d\\u0020", "\\u00a0", "\\u001c", "\\b", "\\\\t", "\\/", "a", " 0 ",
                   "노드", "\\u0009x", "\\\\u0009", "\\u00200", "\\U0009", "\\u0008"]
        bo = subprocess.run(["bash", hsh, "blank", *bprobes], capture_output=True).stdout.decode("utf-8").split("\n")[:len(bprobes)]
        wprobes = ["", " ", "\t", "\r\n", "\x0b\x0c", " \x0b ", "a", " a ", "\x1c", "\xa0", "노드", "\x0c-"]
        wo = subprocess.run(["bash", hsh, "wblank", *wprobes], capture_output=True).stdout.decode("utf-8").split("\n")[:len(wprobes)]
        bdiff = [(p_, o_) for p_, o_ in zip(bprobes, bo) if (o_ == "BLANK") != _blank(p_)]
        wdiff = [(p_, o_) for p_, o_ in zip(wprobes, wo) if (o_ == "BLANK") != (p_.strip(" \t\n\x0b\x0c\r") == "")]
        ck(not bdiff and not wdiff and len(bo) == len(bprobes) and len(wo) == len(wprobes) and bo.count("BLANK") == 5 and wo.count("BLANK") == 6,
           f"러너 nbj = 검사기 _blank ({len(bprobes)} 원문 탐침 · 빈칸 {bo.count('BLANK')}) · 러너 nbw = 빈칸 문자 여섯 ({len(wprobes)} 탐침 · 빈칸 {wo.count('BLANK')}) — 다름 {bdiff} {wdiff}")
        jprobes = ["walltime \x1b[31mred\x1b[0m", 'q"uote', "back\\slash", "tab\there", "nl\nhere", "del\x7f", "한글 노드", "", "plain"]
        jo = subprocess.run(["bash", hsh, "jstr", *jprobes], capture_output=True).stdout.decode("utf-8").split("\n")[:len(jprobes)]
        jok = [json.loads('"' + o_ + '"') == p_ and rec_parse(('{"a": "' + o_ + '"}').encode()) is not None for o_, p_ in zip(jo, jprobes)]
        ck(all(jok) and len(jo) == len(jprobes), f"러너 jstr → JSON 이 원래 글로 풀고 REC1 도 받는다 ({len(jprobes)} 탐침) — {list(zip(jprobes, jok))}")
        oprobes = {"er_semi": "SDA; 1 0 0 0 12 0\n", "er_word": "SDA\n", "er_title": hd_, "er_titlecut": hd_[:-1][:30], "er_blank": "   \n\n", "er_col1": hd_.lstrip(" "),
                   "er_fline": hd_ + "   1 F= -.73E+03 E0= -.73E+03  d E =-.73E+03\n", "sdacut": hd_ + "SDA:", "one_tail": hd_ + sda1 + "SDA:", "one_tailnl": hd_ + sda1 + "SDA:\n", "one_fulltail": hd_ + sda1 + cga2[:-1],
                   "mid": hd_ + sda1 + "CGA:   2   -0.73E+03\n" + cga2.replace("   2 ", "   3 "), "nospace": hd_ + "SDA:1 -0.1E+03 -3E-08 -1E-08 8000 0.3E-03\n",
                   "spaced": hd_ + "DA V:   1  -7.3E+02 1 1 8000 1\n", "xyz_tail": hd_ + "XYZ:   1  -7.3E+02  1  1  8000  1\nSDA:", "nul": hd_ + sda1 + "\x00\n",
                   "dav30": dav(30), "dav30_cut": dav(30)[:-1], "real67": "DAV:   1     0.13E+05    0.13E+05   -0.61E+05  7848   0.137E+03\nDAV:   2    -0.41E+03   -0.14E+05   -0.13E+05 10088   0.328E+02    0.201E+01\n",
                   "crlf": dav(3).replace("\n", "\r\n"), "lead_ws": "  \t" + sda1 + " DAV:   2   1 1 1 1 1\n", "empty": "", "hdr_only": hd_, "cr_tail": dav(2) + "DAV:   3\r",
                   "step_x": hd_ + "SDA:   x   -0.7E+03 1 1 8000 1\n", "six_dav": "DAV:   1 1 1 1 1 1\n", "five": "DAV:   1 1 1 1 1\n", "ion": dav(2) + "   1 F= -.7E+03 E0= -.7E+03  d E =0.1E-01\n",
                   "garb": hd_ + "SDA: 1 none missing missing abc bad\n", "nan_row": dav(2) + "DAV:   3   NaN   NaN   NaN  8000   0.3E-03\n",
                   "ncg_frac": "DAV:   1   -0.73E+03   1E-3   1E-4   80.5   0.3E-03\n", "n_zero": "DAV:   0   -0.73E+03   1E-3   1E-4   80   0.3E-03\n",
                   "eight": "DAV:   1   -0.73E+03   1E-3   1E-4   80   0.3E-03   0.1   9\n", "exp3": "DAV:   1   -0.73E+100   1E-3   1E-4   80   0.3E-03\n",
                   "stars": "DAV:   1   -0.73E+03   1E-3   1E-4   ******   0.3E-03\n", "signs": "DAV:   1   -0.73E+03   +1.E-3   .1E-4   80   0.3E-03\n",
                   "hcut": hd_ + "SDA", "hcut1": hd_ + sda1 + "SDA", "colcut": "       N       E   ", "dcut": "D", "hcut_ws": hd_ + "  SDA", "hcut_sp": hd_ + "SD A",
                   "hcut_tab": hd_ + "\tDA", "hcut_dav": hd_ + "  DAV", "col_n": "       N", "col_n_sp": "       N   ", "n_col1": "N", "ws_only": hd_ + "   ",
                   "r310": hd_ + "SDA:   1   " + "1" * 310 + "   -0.1E+00   -0.1E+00  8000   0.3E-03\n", "r24": hd_ + "SDA:   1   " + "1" * 24 + "   -0.1E+00   -0.1E+00  8000   0.3E-03\n",
                   "r25": hd_ + "SDA:   1   " + "1" * 25 + "   -0.1E+00   -0.1E+00  8000   0.3E-03\n"}
        odirs, owant = [], {}
        for k_, t_ in oprobes.items():
            for st_ in STAGES:
                pd = os.path.join(T, "eo_osz", f"{k_}_{st_}"); os.makedirs(pd); open(os.path.join(pd, "OSZICAR"), "wb").write(t_.encode("latin-1"))
                _write(os.path.join(pd, "STAGE"), st_); odirs.append(pd)
                n_, w_ = row_gate(R2._read_raw(os.path.join(pd, "OSZICAR")), st_); owant[os.path.basename(pd)] = f"{n_} {w_ or '-'}"
        oo = subprocess.run(["bash", hsh, "rows", *odirs], capture_output=True, text=True).stdout
        ogot = dict(ln.split("|", 1) for ln in oo.splitlines() if "|" in ln)
        odiff = {k_: (owant[k_], ogot.get(k_)) for k_ in owant if owant[k_] != ogot.get(k_)}
        ck(not odiff and len(ogot) == len(owant), f"러너 row_scan = 검사기 row_gate ({len(oprobes)} 탐침 × 단 셋 · 완전한 행 수 · 사유) — 다름 {odiff}")
        u8p = [b"plain", "노드 고장".encode(), b"\x1b[31m", b"\xe9", b"\xff\xfe", b"\xc0\x80", b"\xc2\x80", b"\xed\xa0\x80", b"\xed\x9f\xbf", b"\xf4\x8f\xbf\xbf",
               b"\xf4\x90\x80\x80", b"\xe2\x82", b"\xf0\x9f\x98\x80", b"\xe0\x9f\x80", b"\xe0\xa0\x80", b"a\xf5b", b"\xc2", b""]
        uo_ = subprocess.run(["bash", hsh, "u8", *u8p], capture_output=True).stdout.decode("latin-1").split("\n")[:len(u8p)]

        def dec_ok(b_):
            try:
                b_.decode("utf-8")
                return "OK"
            except UnicodeDecodeError:
                return "BAD"
        uw_ = [dec_ok(b_) for b_ in u8p]
        ck(uo_ == uw_ and uw_.count("BAD") == 9, f"러너 u8ok = 검사기 쪽 UTF-8 (Python decode) — {len(u8p)} 탐침 · 거부 {uw_.count('BAD')} — 러너 {uo_} · 기대 {uw_}")
        wb_ = os.path.join(T, "ep_wall"); os.makedirs(os.path.join(wb_, "run")); os.makedirs(os.path.join(wb_, "run_aborted"))
        rcw_ = {"job": JOB, "rung": "A5", "wall_s": "300"}
        for rel_, files_ in ((f"run/{JOB}_c1", {"infra_abort.json": rcw_, "killed.json": {"wall_s": "648001"}}), (f"run/{JOB}_c2", {"infra_abort.json": rcw_, "attempt.json": {"elapsed_s": 50}}),
                             (f"run/{JOB}_A5", {}), (f"run_aborted/{JOB}_A5_1", {"infra_abort.json": rcw_, "attempt.json": {"elapsed_s": 7}}),
                             (f"run_aborted/{JOB}_c1_2", {"attempt.json": {"elapsed_s": 9}})):
            os.makedirs(os.path.join(wb_, rel_))
            for f_, x_ in files_.items():
                _write(os.path.join(wb_, rel_, f_), json.dumps(x_) + "\n")
        wrel_ = [f"run/{JOB}_c1", f"run/{JOB}_c2", f"run/{JOB}_A5", f"run_aborted/{JOB}_A5_1", f"run_aborted/{JOB}_c1_2"]
        wo_ = subprocess.run(["bash", hsh, "wall", wb_, *wrel_], capture_output=True, text=True).stdout
        wgot = dict(ln.split("|", 1) for ln in wo_.splitlines() if "|" in ln)
        wwant = {r_: ("BAD" if w_ is None else str(w_)) for r_ in wrel_ for w_ in [wall_of(os.path.join(wb_, r_))]}
        ck(wgot == wwant and [wwant[r_] for r_ in wrel_] == ["648001", "50", "UNKNOWN", "300", "BAD"],
           f"러너 wall_of = 검사기 wall_of — 진행 폴더의 영수증은 시간 출처가 아니다 · 보존 폴더는 그 영수증만 (Codex EP P1) — 러너 {wgot} · 검사기 {wwant}")
        sprobes = {"ok": ({}, "c2"), "job": ({"job": "V5_x"}, "c2"), "stage": ({"stage": "a4"}, "c2"), "var": ({"attempt": "c1"}, "c2"), "a5c": ({"attempt": "A5c"}, "A5"),
                   "rid": ({"run_id": "2026-1-1"}, "c2"), "rid_uni": ({"run_id": "２０261122T000000-1-1"}, "c2"), "tstr": ({"t_start": "5"}, "c2"), "form": (None, "c2"), "miss": ("miss", "c2")}
        sdirs, swant = [], {}
        for k_, (mod_, st_) in sprobes.items():
            pd = os.path.join(T, "eo_start", k_); os.makedirs(pd); _write(os.path.join(pd, "STAGE"), st_)
            base_ = {"job": JOB, "attempt": "c2", "stage": "a5", "run_id": "20261122T000000-1-1", "t_start": 5, "kernel_sha256": ""}
            if mod_ is None:
                _write(os.path.join(pd, "attempt.start"), json.dumps(base_).replace(", ", " ", 1) + "\n")
            elif mod_ != "miss":
                _write(os.path.join(pd, "attempt.start"), json.dumps({**base_, **mod_}, ensure_ascii=False) + "\n")
            sdirs.append(pd); swant[k_] = start_problem(JOB, pd, st_) or "-"
        so_ = subprocess.run(["bash", hsh, "start", *sdirs], capture_output=True, text=True).stdout
        sgot = dict(ln.split("|", 1) for ln in so_.splitlines() if "|" in ln)
        sdiff = {k_: (swant[k_], sgot.get(k_)) for k_ in swant if swant[k_] != sgot.get(k_)}
        ck(not sdiff and swant["ok"] == "-" and swant["a5c"] == "-" and sum(1 for v_ in swant.values() if v_ != "-") == 8,
           f"러너 start_id = 검사기 start_problem ({len(sprobes)} 탐침 · 잡 · stage · 변형 · run_id · t_start · 꼴) — 다름 {sdiff}")
        lv_ = {"ok": None, "row_gone": "row", "folder_gone": "folder", "extra_folder": "extra", "head": "head", "dir": "dir", "wall": "wall", "nonl": "nonl",
               "nine": "nine", "rcpt_rid": "rid", "rcpt_filled": "filled", "rcpt_wall0": "wall0", "rcpt_noreason": "noreason", "rcpt_rung": "rung",
               "rcpt_early": "early", "rcpt_rawesc": "rawesc", "start_job": "sjob", "no_ledger_no_folder": "none", "no_ledger_folder": "nol",
               "stray": "stray", "hist_extra": "hist", "rcpt_empty": "rempty", "end_rid": "endrid",
               "st_empty": "stempty", "rcpt_blank": "rblank", "rcpt_u8": "ru8", "rcpt_ws": "rws", "rcpt_wsu": "rwsu", "hist_el": "histel"}
        ldirs, lwant = [], {}
        for k_, how_ in lv_.items():
            e_ = cp_(exso, f"eo_ledger_{k_}"); ab_ = os.path.join(e_, "run_aborted", f"{JOB}_c1_1"); lp_ = os.path.join(e_, "run", "infra_aborts.tsv")
            rc_p = os.path.join(ab_, "infra_abort.json"); rcd = json.loads(open(rc_p, encoding="utf-8").read()); lt_ = open(lp_).read()
            if how_ == "row":
                _write(lp_, LEDGER_HEAD + "\n")
            elif how_ == "folder":
                shutil.rmtree(ab_)
            elif how_ == "extra":
                shutil.copytree(ab_, os.path.join(e_, "run_aborted", f"{JOB}_c1_2"))
            elif how_ == "head":
                _write(lp_, lt_.replace("recorded_utc", "recorded_UTC", 1))
            elif how_ == "dir":
                _write(lp_, lt_.replace(f"{JOB}_c1_1", f"{JOB}_c1_2"))
            elif how_ == "wall":
                f_ = lt_.split("\n"); g_ = f_[1].split("\t"); g_[5] = "1" if g_[5] != "1" else "2"; f_[1] = "\t".join(g_); _write(lp_, "\n".join(f_))
            elif how_ == "nonl":
                _write(lp_, lt_.rstrip("\n"))
            elif how_ == "nine":
                _write(lp_, lt_.replace(f"\t{JOB}_c1_1", f"\tx\t{JOB}_c1_1"))
            elif how_ == "stray":
                shutil.copy(rc_p, os.path.join(e_, "run", f"{JOB}_c1", "infra_abort.json"))
            elif how_ == "hist":
                with open(os.path.join(e_, "run", "status.tsv"), "a") as fh_:
                    fh_.write(f"{JOB}\tc1\ta5\t0\tOK\t1\t0\t0\t-\t1\t20261123T000000-7-7\n")
            elif how_ == "endrid":
                ajp_ = os.path.join(ab_, "attempt.json"); _write(ajp_, open(ajp_).read().replace('"run_id": "', '"run_id": "9', 1))
            elif how_ in ("rid", "filled", "wall0", "noreason", "rung", "early", "rawesc", "rempty", "rblank", "rws", "rwsu"):
                rcd2 = dict(rcd)
                if how_ == "rid":
                    rcd2["run_id"] = "20261123T000000-1-1"
                elif how_ == "filled":
                    rcd2["wall_s_filled_utc"] = "2026-11-23T00:00:00Z"
                elif how_ == "wall0":
                    rcd2["wall_s"] = "0" + rcd["wall_s"]
                elif how_ == "noreason":
                    rcd2.pop("reason")
                elif how_ == "rung":
                    rcd2["rung"] = "A5"
                elif how_ == "early":
                    rcd2["recorded_s"] = 1000
                elif how_ == "rempty":
                    rcd2["sched_job_id"] = ""
                elif how_ == "rblank":
                    rcd2["sched_job_id"] = "   "
                elif how_ == "rws":
                    rcd2["sched_job_id"] = "\t\r\n\x0b\x0c "             # json.dumps → \t \r \n \u000b \f (Codex EQ P1 보강)
                txt_ = json.dumps(rcd2, ensure_ascii=False)
                if how_ == "rwsu":
                    txt_ = re.sub(r'"cancel_utc": "[^"]*"', lambda m_: '"cancel_utc": "\\u000D\\u0020\\u0009"', txt_, count=1)
                if how_ == "rawesc":
                    txt_ = txt_.replace('"reason": "', '"reason": "\x1b', 1)
                _write(rc_p, txt_ + "\n")
            elif how_ == "sjob":
                sp2 = os.path.join(ab_, "attempt.start"); s2 = json.loads(open(sp2).read()); s2["job"] = "V5_x"; _write(sp2, json.dumps(s2) + "\n")
            elif how_ == "none":                           # 장부 · 보존 폴더 · 그 시도의 이력 줄까지 맞게 지운 반송 (서로 맞는 부분 복구 — 문제 없음 · 못 잡는 한계)
                rid_ab = json.loads(open(os.path.join(ab_, "attempt.start")).read())["run_id"]
                shutil.rmtree(os.path.join(e_, "run_aborted")); os.remove(lp_)
                stp_ = os.path.join(e_, "run", "status.tsv")
                _write(stp_, "".join(l_ for l_ in open(stp_).readlines() if not l_.rstrip("\n").endswith("\t" + rid_ab)))
                fjn_ = os.path.join(e_, "run", "final.json"); dfn_ = json.loads(open(fjn_).read()); dfn_["attempts"] = attempts_of(e_, J_)
                _write(fjn_, json.dumps(dfn_) + "\n")                # 끝 기록의 시도 목록까지 맞게 (서로 맞는 복구 — 트리 관문도 못 잡는 한계 · 위협 범위 밖)
            elif how_ == "nol":
                os.remove(lp_)
            elif how_ == "histel":                          # 이력 줄 벽시계 ≠ 그 시도 끝 기록 elapsed_s (Codex ER Q-ER-3①)
                sp_ = os.path.join(e_, "run", "status.tsv"); L_ = open(sp_).read().split("\n"); g_ = L_[1].split("\t"); g_[9] = str(int(g_[9]) + 1)
                L_[1] = "\t".join(g_); _write(sp_, "\n".join(L_))
            elif how_ == "stempty":
                _write(os.path.join(e_, "run", "status.tsv"), "")
            elif how_ == "ru8":
                bb_ = open(rc_p, "rb").read(); ib_ = bb_.index(b'"reason": "') + len(b'"reason": "'); open(rc_p, "wb").write(bb_[:ib_] + b"\xe9" + bb_[ib_ + 1:])
            prob_ = tree_problems(J_, e_) + ledger_problems(J_, e_) + [p_ for n_ in sorted(os.listdir(os.path.join(e_, "run_aborted"))) if os.path.isdir(os.path.join(e_, "run_aborted"))
                                               for p_ in [abort_receipt_problem(J_, os.path.join(e_, "run_aborted", n_), AB_RE.match(n_).group(2))] if p_] \
                if os.path.isdir(os.path.join(e_, "run_aborted")) else tree_problems(J_, e_) + ledger_problems(J_, e_)
            ldirs.append(e_); lwant[os.path.basename(e_)] = bool(prob_)
        lo_ = subprocess.run(["bash", hsh, "tree", *ldirs], capture_output=True, text=True).stdout
        lgot = {k_: (v_ != "-") for k_, v_ in (ln.split("|", 1) for ln in lo_.splitlines() if "|" in ln)}
        ldiff = {k_: (lwant[k_], lgot.get(k_)) for k_ in lwant if lwant[k_] != lgot.get(k_)}
        ck(not ldiff and lwant["eo_ledger_ok"] is False and lwant["eo_ledger_no_ledger_no_folder"] is False and sum(lwant.values()) == len(lwant) - 2,
           f"러너 tree5 = 검사기 tree_problems + ledger_problems + abort_receipt_problem ({len(lv_)} 반송 변형 · 문제 있음/없음) — 다름 {ldiff} · 문제 없음 {[k_ for k_, v_ in lwant.items() if not v_]}")
        # 트리 관문 같은 낱말 (러너 tree5 첫 사유 = 검사기 tree_problems 첫 사유 = 기대 — 탐침마다 문제 하나 · Codex EQ)
        jn_ = os.path.join

        def _trim(p_):
            _write(p_, open(p_).read().rstrip("\n")[:-1] + "\n")

        def _jset(p_, **kw_):
            d_ = json.loads(open(p_, encoding="utf-8").read()); d_.update(kw_); _write(p_, json.dumps(d_, ensure_ascii=False) + "\n")

        def _jdrop(p_, k_):
            d_ = json.loads(open(p_, encoding="utf-8").read()); d_.pop(k_); _write(p_, json.dumps(d_, ensure_ascii=False) + "\n")

        def _bad8(p_, key_):
            bb_ = open(p_, "rb").read(); ib_ = bb_.index(key_) + len(key_); open(p_, "wb").write(bb_[:ib_] + b"\xe9" + bb_[ib_ + 1:])
        Jq_ = JOB; A_ = f"run/{Jq_}_A5"; C1_ = f"run/{Jq_}_c1"; C2_ = f"run/{Jq_}_c2"; AB_ = f"run_aborted/{Jq_}_c1_1"
        tprobes = [
            ("ok", exso, lambda e: None, "-"),
            ("runpart", exso, lambda e: _write(jn_(e, "run", "final.json.part"), "{"), "run_entry_final.json.part"),
            ("c1part", exso, lambda e: _write(jn_(e, C1_, "infra_abort.json.part"), "{"), f"file_{C1_}/infra_abort.json.part"),
            ("c1junk", exso, lambda e: _write(jn_(e, C1_, "notes.txt"), "x"), f"file_{C1_}/notes.txt"),
            ("c1sub", exso, lambda e: os.makedirs(jn_(e, C1_, "sub")), f"file_{C1_}/sub"),
            ("abjunk", exso, lambda e: os.makedirs(jn_(e, "run_aborted", "junk")), "aborted_entry_junk"),
            ("att_brace", exso, lambda e: _trim(jn_(e, C1_, "attempt.json")), f"{C1_}:att_form"),
            ("att_dot5", exso, lambda e: _write(jn_(e, C1_, "attempt.json"), re.sub(r'("t_start": [0-9]+)', r'\1.5', open(jn_(e, C1_, "attempt.json")).read(), count=1)), f"{C1_}:att_form"),
            ("att_rid", exso, lambda e: _write(jn_(e, C1_, "attempt.json"), open(jn_(e, C1_, "attempt.json")).read().replace('"run_id": "', '"run_id": "9', 1)), f"{C1_}:end_run_id"),
            ("att_t0", exso, lambda e: _write(jn_(e, C1_, "attempt.json"), re.sub(r'"t_start": ([0-9]+)', lambda m_: f'"t_start": {int(m_.group(1)) + 1}', open(jn_(e, C1_, "attempt.json")).read(), count=1)), f"{C1_}:end_t_start"),
            ("seal", exso, lambda e: open(jn_(e, C1_, "OUTCAR"), "a").write(" \n"), f"{C1_}:seal_OUTCAR"),
            ("att_job", exso, lambda e: _write(jn_(e, C1_, "attempt.json"), open(jn_(e, C1_, "attempt.json")).read().replace(f'"job": "{Jq_}"', f'"job": "{Jq_}x"', 1)), f"{C1_}:end_job"),
            ("att_attempt", exso, lambda e: _write(jn_(e, C1_, "attempt.json"), open(jn_(e, C1_, "attempt.json")).read().replace('"attempt": "c1"', '"attempt": "c2"', 1)), f"{C1_}:end_attempt"),
            ("att_stage", exso, lambda e: _write(jn_(e, C1_, "attempt.json"), open(jn_(e, C1_, "attempt.json")).read().replace('"stage": "a5"', '"stage": "a6"', 1)), f"{C1_}:end_stage"),
            ("potsha", exso, lambda e: _write(jn_(e, C1_, "POTCAR.sha256"), "0" * 64 + "\n"), f"{C1_}:end_potcar_sha"),
            ("prep_osz", exso, lambda e: (os.makedirs(jn_(e, "run", f".prep_{Jq_}_c1")), _write(jn_(e, "run", f".prep_{Jq_}_c1", "OSZICAR"), "x")), f"prep_run/.prep_{Jq_}_c1/OSZICAR"),
            ("endkill", exso, lambda e: _write(jn_(e, C1_, "killed.json"), json.dumps(kb0) + "\n"), f"{C1_}:end_and_killed"),
            ("abkill", exso, lambda e: _write(jn_(e, AB_, "killed.json"), json.dumps(kb0) + "\n"), f"{AB_}:killed_in_aborted"),
            ("stray", exso, lambda e: shutil.copy(jn_(e, AB_, "infra_abort.json"), jn_(e, C1_, "infra_abort.json")), f"{C1_}:stray_receipt"),
            ("rcpt_u8", exso, lambda e: _bad8(jn_(e, AB_, "infra_abort.json"), b'"reason": "'), f"{AB_}:utf8_infra_abort.json"),
            ("start_job", exso, lambda e: _jset(jn_(e, A_, "attempt.start"), job="V5_x"), f"{A_}:start_job"),
            ("nostart", exso, lambda e: os.remove(jn_(e, C1_, "attempt.start")), f"{C1_}:no_start"),
            ("fin_state", exso, lambda e: _write(jn_(e, "run", "final.json"), open(jn_(e, "run", "final.json")).read().replace('"state": "OK"', '"state": "REVIEW"', 1)), "final_code_state"),
            ("fin_fields", exso, lambda e: _jdrop(jn_(e, "run", "final.json"), "written_s"), "final_fields"),
            ("fin_u8", exso, lambda e: _bad8(jn_(e, "run", "final.json"), b'"why": "'), "utf8_final.json"),
            ("sp_form", exso, lambda e: _trim(jn_(e, "run", "start_point.json")), "start_point_form"),
            ("w0_form", exso, lambda e: _trim(jn_(e, "run", "w0_check.json")), "w0_form"),
            ("k_ok", kb_base, lambda e: None, "-"),
            ("k_rid", kb_base, lambda e: _jset(jn_(e, C2_, "killed.json"), run_id="20261123T000000-9-9"), f"{C2_}:killed_run_id"),
            ("k_blank", kb_base, lambda e: _jset(jn_(e, C2_, "killed.json"), reason="   "), f"{C2_}:killed_json_blank_reason"),
            ("k_blank_ws", kb_base, lambda e: _jset(jn_(e, C2_, "killed.json"), reason="\t\r\n\x0b\x0c "), f"{C2_}:killed_json_blank_reason"),
            ("k_blank_u", kb_base, lambda e: _write(jn_(e, C2_, "killed.json"), re.sub(r'"reason": "[^"]*"', lambda m_: '"reason": "\\u0009\\u000A\\u0020"',
                                                                                         open(jn_(e, C2_, "killed.json")).read(), count=1)), f"{C2_}:killed_json_blank_reason"),
            ("k_nb_fs", kb_base, lambda e: _jset(jn_(e, C2_, "killed.json"), reason="\x1c"), "-"),
            ("k_nb_bst", kb_base, lambda e: _write(jn_(e, C2_, "killed.json"), re.sub(r'"reason": "[^"]*"', lambda m_: '"reason": "\\\\t"',
                                                                                         open(jn_(e, C2_, "killed.json")).read(), count=1)), "-"),
            ("k_form", kb_base, lambda e: _trim(jn_(e, C2_, "killed.json")), f"{C2_}:killed_json_form"),
            ("k_rung", kb_base, lambda e: _jset(jn_(e, C2_, "killed.json"), rung="A5"), f"{C2_}:killed_job_or_rung"),
            ("k_early", kb_base, lambda e: _jset(jn_(e, C2_, "killed.json"), recorded_s=1), f"{C2_}:killed_recorded_s"),
            ("k_wall", kb_base, lambda e: _jset(jn_(e, C2_, "killed.json"), wall_s="01"), f"{C2_}:killed_wall_s"),
            ("k_field", kb_base, lambda e: _jdrop(jn_(e, C2_, "killed.json"), "osz_rows"), f"{C2_}:killed_json_field_osz_rows")]
        tdirs, twant, tchk = [], {}, {}
        for nm_, src_, fn_, want_ in tprobes:
            e_ = cp_(src_, f"eq_tree_{nm_}"); fn_(e_); tdirs.append(e_); twant[os.path.basename(e_)] = want_
            tp_ = tree_problems(J_, e_); tchk[os.path.basename(e_)] = tp_[0] if tp_ else "-"
        to_ = subprocess.run(["bash", hsh, "tree", *tdirs], capture_output=True, text=True).stdout
        tgot = dict(ln.split("|", 1) for ln in to_.splitlines() if "|" in ln)
        tdiff = {k_: (twant[k_], tgot.get(k_), tchk[k_]) for k_ in twant if not (twant[k_] == tgot.get(k_) == tchk[k_])}
        ck(not tdiff and len(tgot) == len(twant),
           f"러너 tree5 = 검사기 tree_problems = 기대 낱말 ({len(tprobes)} 탐침 · 이름 · 시작 · 끝 기록 틀 · 신원 · 봉인 · 끊김 기록 자리 · 결속 · 빈칸 · UTF-8 · 끝 기록 조합 · 시작점 · ⓪) — 다름 {tdiff}")
        # S21: 러너 judge5 = 검사기 judge5 (같은 탐침 · 단마다)
        probes = {"conv": dav(30), "sda": dav(30).replace("DAV:", "SDA:"), "cga": sda, "xyz": dav(30).replace("DAV:", "XYZ:"), "cgsp": dav(30) + "CG :  31   1  1  1\n",
                  "nospace": "SDA:1 -0.1E+03 -3E-08 -1E-08\n", "nan": dav(29) + "DAV:   30   -7.3E+02   NaN   NaN  1  1  1\n", "empty": "",
                  "sdacut": hd_ + "SDA:", "one_tail": hd_ + sda1 + "SDA:", "dav_tail": dav(30) + "DAV:   31   -7.3", "cga_tail": sda + "CGA:   31   -7.3E+02",
                  "mid_part": dav(3) + "DAV:   4   -7.3E+02\n" + dav(30).split("\n", 4)[4], "fulltail": dav(29) + dav(30).split("\n")[29]}      # 완전한 행 · 잘린 꼬리 (Codex EO P0)
        harness = os.path.join(T, "harness.sh")
        hb = "\n".join(r2_block(f"{n}(){{") for n in ("incar_val",)) + "\n" + _patch(_patch(r2_block("judge(){"), "judge(){", "judge_r2(){"),
                                                                                         'cat "$d/OSZICAR" 2>/dev/null |', 'osz_feed "$d" |')
        body = _ee[_ee.index("stage_hdr(){"):_ee.index("stat5(){")]
        _write(harness, "set -u\n" + hb + "\n" + body + '\nfor d in "$@"; do echo "$(basename "$d")|$(judge5 "$d" "$(cat "$d/STAGE")")"; done\n')
        dirs, want = [], {}
        for k_, osz_ in probes.items():
            for st_ in STAGES:
                pd = os.path.join(T, "probe", f"{k_}_{st_}"); os.makedirs(pd)
                _write(os.path.join(pd, "OSZICAR"), osz_); _write(os.path.join(pd, "OUTCAR"), out_ok); _write(os.path.join(pd, "INCAR"), inc)
                _write(os.path.join(pd, "attempt.json"), '{"rc": 0}'); _write(os.path.join(pd, "STAGE"), st_)
                dirs.append(pd); want[os.path.basename(pd)] = " ".join(str(x) for x in judge5(osz_, out_ok, inc, 0, st_))
        hp = subprocess.run(["bash", harness, *dirs], capture_output=True, text=True)
        got = dict(ln.split("|", 1) for ln in hp.stdout.splitlines() if "|" in ln)
        diff_ = {k: (want[k], got.get(k)) for k in want if want[k] != got.get(k)}
        ck(not diff_ and len(got) == len(want), f"러너 judge5 = 검사기 judge5 ({len(want)} 탐침 · 단 셋) — 다름 {diff_}")
        # S22: 러너 echo5 = 검사기 echo5 (같은 OUTCAR 탐침 · 걸린 키 집합)
        eh = os.path.join(T, "eharness.sh")
        _write(eh, "set -u\n" + RUN_A5_ENV[RUN_A5_ENV.index("echo5(){"):RUN_A5_ENV.index("hist_max(){")]
               + '\nfor d in "$@"; do echo "$(basename "$d")|$(echo5 "$d" "$(cat "$d/VAR")")"; done\n')
        edirs, ewant = [], {}
        for k_, (txt_, var_) in eprobes.items():
            pd = os.path.join(T, "eprobe", k_); os.makedirs(pd)
            _write(os.path.join(pd, "OUTCAR"), txt_); _write(os.path.join(pd, "VAR"), var_)
            edirs.append(pd); ewant[k_] = keys(*echo5(txt_, var_))
        eo = subprocess.run(["bash", eh, *edirs], capture_output=True, text=True)
        egot = {}
        for ln in eo.stdout.splitlines():
            if "|" in ln:
                k_, v_ = ln.split("|", 1)
                egot[k_] = [] if v_.strip() == "-" else sorted({x.split(":")[0] for x in v_.strip().strip(",").split(",") if x})
        ediff = {k: (ewant[k], egot.get(k)) for k in ewant if ewant[k] != egot.get(k)}
        ck(not ediff and len(egot) == len(ewant), f"러너 echo5 = 검사기 echo5 ({len(ewant)} 탐침) — 다름 {ediff}")
    print(f"{'✅' if not bad else '⛔'} build_a5_vasp_package selftest {ok}/{ok + bad}")
    return 0 if not bad else 1


# ───────────────────────── 돌연변이 (시험이 빨간불을 내는지) ─────────────────────────
MUTANTS = (
    ('m01 관문 끔 (c1 이 SDA/CGA 도 받음)', 'build_a5_vasp_package.py', 'ROW_HDR = {"A5": ("DAV", "RMM"), "c1": ("DAV", "RMM"),', 'ROW_HDR = {"A5": ("DAV", "RMM"), "c1": ("DAV", "RMM", "SDA", "CGA"),', 'a5'),
    ('m02 c2 가 DAV 도 받음', 'build_a5_vasp_package.py', '"c2": ("SDA", "CGA")}', '"c2": ("SDA", "CGA", "DAV")}', 'a5'),
    ('m03 보조 최소 스텝 100 → 10', 'build_a5_vasp_package.py', 'SEC_W1, SEC_W0, SEC_MIN_STEPS = 50, 50, 100', 'SEC_W1, SEC_W0, SEC_MIN_STEPS = 50, 50, 10', 'a5'),
    ('m04 u_E 에서 평균 이동 뺌', 'build_a5_vasp_package.py', '"u_E_eV": max(rng, shift)', '"u_E_eV": rng', 'a5'),
    ('m05 A5 에도 보조 숫자', 'build_a5_vasp_package.py', 'if stage not in ("c1", "c2"):\n        return None, f"보조 기준은', 'if stage not in ("c1", "c2", "A5", "a4A", "r1B"):\n        return None, f"보조 기준은', 'a5'),
    ('m06 ⓪ 크기 확인 뺌 (러너)', 'build_a5_vasp_package.py', 'elif [ "$z" != "$W0_SIZE" ]; then why="크기 다름"', 'elif false; then why="크기 다름"', 'a5'),
    ('m07 c1 OK 여도 c2 띄움', 'build_a5_vasp_package.py', '  drop5; log "✓ c1 주 기준 수렴 — c2 를 띄우지 않는다"; fin5 0 OK "c1 주 기준 수렴"', '  :', 'a5'),
    ('m08 누적 상한 확인 뺌', 'build_a5_vasp_package.py', 'awk -v w="$w" -v c="$CAP_H" \'BEGIN { exit !(w <= c * 3600) }\' ||', 'true ||', 'a5'),
    ('m09 c1 · c2 끝 sha 를 안 봄 (러너)', 'build_a5_vasp_package.py', '[ "$wsha" = "$wcp" ] && [ "$wcp" = "$wend" ] && hon=1', '[ "$wsha" = "$wcp" ] && hon=1', 'a5'),
    ('m10 A5 재시작에 끝 sha 를 요구 (러너 A5 를 c 단처럼)', 'build_a5_vasp_package.py', 'ok_ = (V.HEX64.match(str(rs.get("src_sha256", ""))) is not None and rs.get("src_sha256") == rs.get("copied_sha256") == src_sha', 'ok_ = (V.HEX64.match(str(rs.get("src_sha256", ""))) is not None and rs.get("src_sha256") == rs.get("copied_sha256") == src_sha == (w or {}).get("sha256")', 'a5'),
    ('m11 MAXMIX 해석값 확인 뺌 (검사기)', 'build_a5_vasp_package.py', '"c1": {"IALGO": 38, "AMIX": 0.1, "AMIN": 0.01, "MAXMIX": 200}, "c2"', '"c1": {"IALGO": 38, "AMIX": 0.1, "AMIN": 0.01}, "c2"', 'a5'),
    ('m12 사다리 대조 (c1 OK 인데 c2) 뺌', 'build_a5_vasp_package.py', '                if present("c2"):\n                    viol.append("c2 가 있는데 c1 이 주 기준 OK', '                if False:\n                    viol.append("c2 가 있는데 c1 이 주 기준 OK', 'a5'),
    ('m13 수집기 u_W 문턱 0.002 → 0.02', 'build_v5_vasp_package.py', 'A5_SEC_MAX_UW = 0.002', 'A5_SEC_MAX_UW = 0.02', 'v5'),
    ('m14 수집기 G4 가 u_W 를 안 더함', 'build_v5_vasp_package.py', 'if abs(dw) + uW <= G4_DW:', 'if abs(dw) <= G4_DW:', 'v5'),
    ('m15 수집기 둘 다 보조 불일치 확인 뺌', 'build_v5_vasp_package.py', 'if abs(e1 - e2) > u1 + u2:', 'if False:', 'v5'),
    ('m16 수집기 순서: c1 보조가 c2 주보다 먼저', 'build_v5_vasp_package.py', 'A5_ORDER = ("c1:primary", "c2:primary", "c1:secondary", "c2:secondary")', 'A5_ORDER = ("c1:primary", "c1:secondary", "c2:primary", "c2:secondary")', 'v5'),
    ('m17 수집기 보조 기준이 A5 를 받음', 'build_v5_vasp_package.py', 'A5_SEC_STAGES = ("c1", "c2")', 'A5_SEC_STAGES = ("c1", "c2", "A5")', 'v5'),
    ('m18 수집기 보조 최소 스텝 확인 뺌', 'build_v5_vasp_package.py', 'if not isinstance(n, int) or isinstance(n, bool) or n < A5_SEC_MIN_STEPS:', 'if False:', 'v5'),
    ('m19 러너 관문: c1 이 SDA/CGA 도 받음 (bash)', 'build_a5_vasp_package.py', 'stage_hdr(){ case "$1" in A5|c1) echo \'DAV|RMM\';;', 'stage_hdr(){ case "$1" in A5|c1) echo \'DAV|RMM|SDA|CGA\';;', 'a5'),
    ('m20 러너 중복 실행 거부 뺌 (lock_take — 계산 · 기록 명령 · 포장이 같은 잠금 · Codex ER)', 'build_a5_vasp_package.py', '      live|foreign) lock_say "$LK_S" "$LK_H" "$LK_P" "$1"; exit 2;;', '      live|foreign) rm -rf "$LOCK";;', 'a5'),
    ('m21 러너 ⓪ 머리 확인 뺌', 'build_a5_vasp_package.py', 'elif ! { [ $# -ge 6 ] && [ "$4" = "$W0_NK" ] && [ "$5" = "$W0_NB" ] && enc_eq "$6" "$W0_EN"; }; then', 'elif false; then', 'a5'),
    ('m22 검사기 c 단 재시작이 시작 sha 를 안 봄', 'build_a5_vasp_package.py', 'if not (src_sha and V.HEX64.match(src_sha) and w.get("src_sha256") == src_sha):', 'if False:', 'a5'),
    ('m23 러너: 행 0 을 다음 단으로 넘김 (해석 1 · ZERO → NEXT)', 'build_a5_vasp_package.py', '[ "$n" -ge 1 ] 2>/dev/null || { echo "ZERO SCF_UNVERIFIED 0 no_rows"; return; }', '[ "$n" -ge 1 ] 2>/dev/null || { echo "NEXT RUN_FAILED 0 no_rows"; return; }', 'a5'),
    ('m24 러너: 재시작 미이행 · SCF 미확인 멈춤 뺌 (REVIEW → NEXT)', 'build_a5_vasp_package.py', '*) echo "REVIEW $s $n -";; esac', '*) echo "NEXT $s $n -";; esac', 'a5'),
    ('m25 러너: 끝 기록 확인 뺌 (끝난 사다리를 다시 돌림 · P1-1)', 'build_a5_vasp_package.py', 'if [ -f run/final.json ]; then\n  log "■ 다시 돌림', 'if false; then\n  log "■ 다시 돌림', 'a5'),
    ('m26 러너: 시작점을 기록에서 읽지 않고 다시 정함 (P0-2(b))', 'build_a5_vasp_package.py', 'if [ -f run/start_point.json ]; then\n  sp_load ||', 'if false; then\n  sp_load ||', 'a5'),
    ('m27 러너: --infra-abort 뒤 단 거부 뺌 (P0-2(c))', 'build_a5_vasp_package.py', 'lx=$(later5 "$st"); [ -z "$lx" ] || { echo "⛔ 뒤 단 ($lx) 이 이미 있다 — $st 의 0 스텝 중단은', 'lx=""; [ -z "$lx" ] || { echo "⛔ 뒤 단 ($lx) 이 이미 있다 — $st 의 0 스텝 중단은', 'a5'),
    ('m28 러너: --killed 뒤 단 거부 뺌 (P0-2(c))', 'build_a5_vasp_package.py', 'lx=$(later5 "$st"); [ -z "$lx" ] || { echo "⛔ 뒤 단 ($lx) 이 이미 있다 — $st 의 끊김은', 'lx=""; [ -z "$lx" ] || { echo "⛔ 뒤 단 ($lx) 이 이미 있다 — $st 의 끊김은', 'a5'),
    ("m29 러너: 없는 W0 경로를 '확인 안 됨' 으로 기록 (옛 동작 · P1-3)", 'build_a5_vasp_package.py', '  else\n    echo "⛔ W0_WAVECAR \'$p\' 가 없거나 읽을 수 없다 — 기록하지 않았다. \'ls -l\' · \'sha256sum\' 으로 경로를 확인하고, 정말 없으면 W0_WAVECAR=none 으로 다시"; exit 2\n  fi', '  else why="파일이 없거나 읽을 수 없다"; fi', 'a5'),
    ('m30 러너: 상대 W0 경로를 부른 곳 기준으로 풀지 않음 (P1-3)', 'build_a5_vasp_package.py', 'if [ -n "${W0_WAVECAR:-}" ] && [ "$W0_WAVECAR" != none ]; then W0_WAVECAR=$(absp "$W0_WAVECAR"); fi', ':', 'a5'),
    ('m31 러너: 묶음 폴더 검사 뺌 (P2(g))', 'build_a5_vasp_package.py', '[ -z "$FX" ] || { echo "⛔ 이 폴더에 a5 묶음이 아닌 것이 있다:', 'true || { echo "⛔ 이 폴더에 a5 묶음이 아닌 것이 있다:', 'a5'),
    ('m32 러너: 다른 기계 잠금을 이 기계 잠금처럼 봄 (P2(d))', 'build_a5_vasp_package.py', 'if [ "$hh" != "$HOST" ]; then echo "foreign $hh $pp"', 'if false; then echo "foreign $hh $pp"', 'a5'),
    ('m33 러너: 준비 실패 때 임시 폴더를 안 지움 (P2(c))', 'build_a5_vasp_package.py', 'pfail(){ log "⛔ $2 — 준비 실패 · 그 단은 소모되지 않았다 (임시 폴더를 지웠다 · 원인 — 디스크 · 권한 · 경로 — 을 고친 뒤 다시)"; rm -rf "$1"; }', 'pfail(){ log "⛔ $2 — 준비 실패"; }', 'a5'),
    ('m34 러너: 설정 에코 관문 뺌 (해석 1)', 'build_a5_vasp_package.py', 'e=$(echo5 "$d" "$var"); [ "$e" = "-" ] || { echo "REVIEW SETTINGS_ECHO $n $e"; return; }\n    s=$(stat5 "$d" "$st" "$SS")', 'e=-\n    s=$(stat5 "$d" "$st" "$SS")', 'a5'),
    ('m35 러너: c 단 재시작에서 시작 WAVECAR 머리 (NBANDS) 를 안 봄 (P3)', 'build_a5_vasp_package.py', '      && [ "$(out_num "$d" NKPTS)" = "${SP_NK:-x}" ] && [ "$(out_num "$d" NBANDS)" = "${SP_NB:-x}" ] && enc_eq "$(out_num "$d" ENCUT)" "${SP_EN:-x}"; } \\', '      ; } \\', 'a5'),
    ('m36 러너: --killed 에 행 ≥ 1 요구 뺌 (해석 1)', 'build_a5_vasp_package.py', '  [ "$n" -ge 1 ] 2>/dev/null || { echo "⛔ $src OSZICAR 전자 반복행 0', '  true || { echo "⛔ $src OSZICAR 전자 반복행 0', 'a5'),
    ('m37 러너: 시작점을 기록하지 않고 c1 을 띄움 (P0-2(b))', 'build_a5_vasp_package.py', '  if [ ! -f run/start_point.json ]; then\n    sp_write ||', '  if false; then\n    sp_write ||', 'a5'),
    ('m38 검사기: 행 0 을 재시작 확인 뒤에 (옛 순서 · P2(f))', 'build_a5_vasp_package.py', '    if not n:\n        kw = {"conflicts"', '    if False:\n        kw = {"conflicts"', 'a5'),
    ('m39 검사기: c1 정체 뒤 c2 없음 · 끝 기록 없음 · 행 0 을 사다리 미완으로 안 봄 (P0-1)', 'build_a5_vasp_package.py', '                if k2 in ("MISSING", "PREP_ONLY", "WAIT", "ZERO"):\n                    incomplete.append(', '                if False:\n                    incomplete.append(', 'a5'),
    ('m40 검사기: c2 의 주 기준 미정 (REVIEW) 을 1저자 멈춤으로 안 봄 (P0-1)', 'build_a5_vasp_package.py', '                elif k2 == "REVIEW":\n                    review.append(', '                elif False:\n                    review.append(', 'a5'),
    ('m41 검사기: 사다리 순서 대조 뺌 (P0-2(a))', 'build_a5_vasp_package.py', '    viol += order_violations([(t_, tm_) for t_, tm_, _ in seq])', '    viol += []', 'a5'),
    ('m42 검사기: 시작점 기록을 규칙과 대조 안 함 (P2(e))', 'build_a5_vasp_package.py', '            if sp is not None and not _same_start(sp, rule):', '            if False:', 'a5'),
    ('m43 검사기: c 단이 있는데 시작점 기록 없음을 안 봄 (P0-2(b))', 'build_a5_vasp_package.py', '            if (present("c1") or present("c2")) and sp is None:', '            if False:', 'a5'),
    ('m44 검사기: c 단 OUTCAR NBANDS ≠ 시작 WAVECAR 머리를 안 봄 (P3)', 'build_a5_vasp_package.py', '        if not dims_ok:\n', '        if False:\n', 'a5'),
    ('m45 검사기: 검사기만 본 실패를 보고하지 않음 (P2(e))', 'build_a5_vasp_package.py', '        if cls[s_][1]:\n            review.append(', '        if False:\n            review.append(', 'a5'),
    ('m46 검사기: 러너 끝 기록 대조 뺌', 'build_a5_vasp_package.py', '        elif fin_rec.get("code") != want_code:', '        elif False:', 'a5'),
    ('m47 검사기: 행 0 을 사다리 미완 대신 재시작 단계로 넘김 (a5_class ZERO 뺌)', 'build_a5_vasp_package.py', '    if not j.get("n_elec_steps"):\n        return "ZERO", None', '    if False:\n        return "ZERO", None', 'a5'),
    ("m48 수집기: c1 보조에 'c2 확인된 끝' 조건 뺌 (P0-1)", 'build_v5_vasp_package.py', '    if "c1:secondary" in cand and "c2:primary" not in cand and not a5_c2_confirmed(atts.get("c2")):', '    if False:', 'v5'),
    ('m49 수집기: c 단 재시작 미이행이어도 채택 (P0-2(d))', 'build_v5_vasp_package.py', '    if rnh:\n', '    if False:\n', 'v5'),
    ('m50 수집기: 총 W 라벨에 개정 5 라벨을 안 실음 (P2(b))', 'build_v5_vasp_package.py', '        if dep4 is not None:\n            labels += [', '        if False:\n            labels += [', 'v5'),
    ('m51 수집기: 채택 기록에 시작점을 안 실음 (P2(a))', 'build_v5_vasp_package.py', '"labels": [A5_LABEL] + ([A5_SEC_LABEL] if rule == "secondary" else []), "adoption_history": hist, "a5_start_point": spx}', '"labels": [A5_LABEL] + ([A5_SEC_LABEL] if rule == "secondary" else []), "adoption_history": hist}', 'v5'),
    ('m52 러너: 끝 기록 없는 시도의 행 손상 · 남의 머리 멈춤 뺌 (EN P0 · EO P0 — gate5 로 옮김)', 'build_a5_vasp_package.py', '  [ "$why" = - ] || { echo "REVIEW SCF_UNVERIFIED $n $why"; return; }       # 끝 기록이 없어도', '  :       # 끝 기록이 없어도', 'a5'),
    ('m53 러너: 끊긴 c 단의 ISTART · ICHARG 확인 뺌 (EN P0)', 'build_a5_vasp_package.py', '    { [ "$is" = 1 ] && [ "$ic" = 0 ]; } || { echo "RESTART_NOT_HONOURED $n istart_', '    true || { echo "RESTART_NOT_HONOURED $n istart_', 'a5'),
    ('m54 러너: 끊긴 c 단의 등록부 재시작 문구 확인 뺌 (EN P0)', 'build_a5_vasp_package.py', '    grep -aqE -e "$RESTART_RE" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null || { echo "RESTART_NOT_HONOURED $n no_restart_phrase"; return; }', '    true || { echo "RESTART_NOT_HONOURED $n no_restart_phrase"; return; }', 'a5'),
    ('m55 러너: 끊긴 c 단의 NBANDS · 시작점 머리 대조 뺌 (EN P0)', 'build_a5_vasp_package.py', '      || { echo "RESTART_NOT_HONOURED $n dims_ne_start_head"; return; };;', '      || true;;', 'a5'),
    ('m56 러너: gate5 가 끊긴 시도를 killed5 로 안 봄 (EN P0)', 'build_a5_vasp_package.py', '  e=$(killed5 "$d" "$st" "$n"); [ "$e" = "-" ] || { echo "REVIEW $e"; return; }', '  :', 'a5'),
    ('m57 러너: 한 줄 기록의 쉼표 없음을 받음 (rec5 · EN P1 · EO P1)', 'build_a5_vasp_package.py', '        if (c == "}") { i++; break }\n        exit 1\n      }', '        if (c == "}") { i++; break }\n        continue\n      }', 'a5'),
    ('m58 러너: killed.json run_id 대조 뺌 (EN P1)', 'build_a5_vasp_package.py', '  [ "$(rf "$K" run_id s)" = "$(rf "$3" run_id s)" ] || { echo killed_run_id; return; }', '  :', 'a5'),
    ('m59 러너: killed.json 행 수 대조 뺌 (EN P1)', 'build_a5_vasp_package.py', '  [ "$(rget "$d/killed.json" osz_rows s)" = "$n" ] || { echo "KILLED_RECORD_MISMATCH $n osz_rows"; return; }', '  :', 'a5'),
    ('m60 러너: killed.json 기록 시각 대조 뺌 (EN P1)', 'build_a5_vasp_package.py', '  { [ -n "$t0" ] && [ -n "$rs" ] && [ "$rs" -ge "$t0" ]; } 2>/dev/null || { echo killed_recorded_s; return; }', '  :', 'a5'),
    ('m61 러너: killed.json 초 꼴 대조 뺌 (EN P1)', 'build_a5_vasp_package.py', '  secs_ok "$(rf "$K" wall_s s)" || { echo killed_wall_s; return; }', '  :', 'a5'),
    ('m62 러너: killed.json 잡 · 단 대조 뺌 (EN P1)', 'build_a5_vasp_package.py', '  { [ "$(rf "$K" job s)" = "$JOB" ] && [ "$(rf "$K" rung s)" = "$2" ]; } || { echo killed_job_or_rung; return; }', '  :', 'a5'),
    ('m63 러너: 한 줄 기록의 같은 키 두 번을 받음 (rec5 · EN P1)', 'build_a5_vasp_package.py', '        if (key in seen) exit 1', '        if (0) exit 1', 'a5'),
    ('m64 러너: 시작점 최초 생성 전 run_aborted 의 c 단을 안 봄 (EN P1)', 'build_a5_vasp_package.py', '  { [ ! -e "$C1" ] && [ ! -e "$C2" ] && ! compgen -G "run_aborted/${JOB}_c[12]_*" > /dev/null; } \\', '  { [ ! -e "$C1" ] && [ ! -e "$C2" ]; } \\', 'a5'),
    ('m65 러너: A5 를 다시 띄우기 전 run_aborted 의 c 단을 안 봄 (EN P1)', 'build_a5_vasp_package.py', '  [ ! -f run/start_point.json ] && [ ! -e "$C1" ] && [ ! -e "$C2" ] && ! compgen -G "run_aborted/${JOB}_c[12]_*" > /dev/null \\', '  [ ! -f run/start_point.json ] && [ ! -e "$C1" ] && [ ! -e "$C2" ] \\', 'a5'),
    ('m66 러너: c1 을 다시 띄우기 전 run_aborted 의 c2 를 안 봄 (EN P1)', 'build_a5_vasp_package.py', '  [ ! -e "$C2" ] && ! compgen -G "run_aborted/${JOB}_c2_*" > /dev/null || fin5 8 REVIEW', '  [ ! -e "$C2" ] || fin5 8 REVIEW', 'a5'),
    ('m67 러너: 끝난 사다리 재실행이 반송 묶음의 끝 기록을 안 봄 (EN P1)', 'build_a5_vasp_package.py', '  if ! ret_has_final; then', '  if false; then', 'a5'),
    ('m68 검사기: 끊긴 시도를 killed_problems 로 안 봄 (EN P0)', 'build_a5_vasp_package.py', '                if kp:\n                    return done(kp[0], kp[1])', '                if False:\n                    return done(kp[0], kp[1])', 'a5'),
    ('m69 검사기: 끝 기록 없는 시도의 행 손상 · 남의 머리 먼저 보기 뺌 (EN P0 · EO P0)', 'build_a5_vasp_package.py', '        if why_rows:                                                         # 끝 기록이 없어도', '        if False:                                                         # 끝 기록이 없어도', 'a5'),
    ('m70 검사기: 끊긴 c 단의 ISTART · ICHARG 확인 뺌 (EN P0)', 'build_a5_vasp_package.py', '        if not (ev["istart"] == "1" and ev["icharg"] == "0"):\n            return "RESTART_NOT_HONOURED", f"끊긴', '        if False:\n            return "RESTART_NOT_HONOURED", f"끊긴', 'a5'),
    ('m71 검사기: 끊긴 c 단의 등록부 재시작 문구 확인 뺌 (EN P0)', 'build_a5_vasp_package.py', '        if rxbad or re.search(rx, ev["text"], re.M) is None:', '        if False:', 'a5'),
    ('m72 검사기: 끊긴 c 단의 시작점 머리 대조 뺌 (EN P0)', 'build_a5_vasp_package.py', '        if not dims_match(dims, sd):\n            return "RESTART_NOT_HONOURED", f"끊긴', '        if False:\n            return "RESTART_NOT_HONOURED", f"끊긴', 'a5'),
    ('m73 검사기: 한 줄 기록의 같은 키 거부 뺌 (rec_parse · EN P1)', 'build_a5_vasp_package.py', '        if key in out:                                   # 같은 키 두 번', '        if False:                                   # 같은 키 두 번', 'a5'),
    ('m74 검사기: 한 줄 기록의 쉼표 없음을 받음 (rec_parse · EN P1 · EO P1)', 'build_a5_vasp_package.py', '        return None                                      # 멤버 뒤에', '        continue                                      # 멤버 뒤에', 'a5'),
    ('m75 검사기: killed.json run_id 대조 뺌 (EN P1)', 'build_a5_vasp_package.py', '    if rec_s(k, "run_id") != rec_s(s0, "run_id"):\n        return "KILLED_RECORD_MISMATCH"', '    if False:\n        return "KILLED_RECORD_MISMATCH"', 'a5'),
    ('m76 검사기: killed.json 행 수 대조 뺌 (EN P1)', 'build_a5_vasp_package.py', '    if rec_s(k, "osz_rows") != str(n):', '    if False:', 'a5'),
    ('m77 검사기: killed.json 기록 시각 대조 뺌 (EN P1)', 'build_a5_vasp_package.py', '    if not (rec_i(s0, "t_start") is not None and rec_i(k, "recorded_s") >= rec_i(s0, "t_start")):', '    if False:', 'a5'),
    ('m78 검사기: killed.json 초 꼴 대조 뺌 (EN P1)', 'build_a5_vasp_package.py', '    if not SECS_RE.fullmatch(rec_s(k, "wall_s")):\n        return "KILLED_RECORD_MISMATCH"', '    if False:\n        return "KILLED_RECORD_MISMATCH"', 'a5'),
    ('m79 검사기: killed.json 잡 · 단 대조 뺌 (EN P1)', 'build_a5_vasp_package.py', '    if rec_s(k, "job") != job["dir"] or rec_s(k, "rung") != stage:\n        return "KILLED_RECORD_MISMATCH"', '    if False:\n        return "KILLED_RECORD_MISMATCH"', 'a5'),
    ('m80 검사기: 끊긴 시도의 모순을 1저자 멈춤으로 안 봄 (a5_class · EN P0)', 'build_a5_vasp_package.py', '    if x.get("killed") and s in KILLED_PROBLEMS:\n        return "REVIEW", None', '    if False:\n        return "REVIEW", None', 'a5'),
    ('m81 검사기: run_aborted 중단 영수증 필수 뺌 (EN P1)', 'build_a5_vasp_package.py', '        if x_.get("receipt_problem"):', '        if False:', 'a5'),
    ('m82 검사기: 시작점 기록 시각 ≤ 첫 c 단 시작 대조 뺌 (EN P1)', 'build_a5_vasp_package.py', '        elif ws_ > min(c_t0):', '        elif False:', 'a5'),
    ('m83 검사기: 시작점 기록 시각이 정수가 아니어도 넘김 (EN P1)', 'build_a5_vasp_package.py', '        if not (isinstance(ws_, int) and not isinstance(ws_, bool)):\n            viol.append(f"시작점 기록 시각', '        if False:\n            viol.append(f"시작점 기록 시각', 'a5'),
    ('m84 수집기: RUN_FAILED · 미수렴에 행 수 ≥ 1 요구 뺌 (EN P2)', 'build_v5_vasp_package.py', '    if not (isinstance(n, int) and not isinstance(n, bool) and n >= 1):\n        return False                               # 행 수가', '    if False:\n        return False                               # 행 수가', 'v5'),
    ('m85 러너: 완전한 행 칸 규칙 뺌 (칸 < 6 · N 정수 아님도 셈 · EO P0)', 'build_a5_vasp_package.py', '      if (lg && (k == 6 || k == 7) && t[1] ~ /^[1-9][0-9]*$/ && t[5] ~ /^[0-9]+$/ && t[2] ~ R && t[3] ~ R && t[4] ~ R && t[6] ~ R && (k == 6 || t[7] ~ R)) n++; else p++', '      n++', 'a5'),
    ('m86 러너: 줄바꿈 없는 끝 조각을 줄로 봄 (잘린 꼬리를 손상으로 · EO P0)', 'build_a5_vasp_package.py', '      if (NR > NL) { tp = 1; next }', '      if (0) { tp = 1; next }', 'a5'),
    ("m87 러너: 완전한 행 0 + 행꼴 끝 조각을 손상으로 안 봄 (EO P0 — 'SDA:' 절단)", 'build_a5_vasp_package.py', 'else if (p > 0 || (tp && n == 0)) print n + 0, "incomplete_row"', 'else if (p > 0) print n + 0, "incomplete_row"', 'a5'),
    ('m88 러너: 끝난 시도의 행 손상 · 남의 머리 멈춤 뺌 (EO P0 — 행 0 판정 앞)', 'build_a5_vasp_package.py', '    [ "$why" = - ] || { echo "REVIEW SCF_UNVERIFIED $n $why"; return; }\n    [ "$n" -ge 1 ] 2>/dev/null || { echo "ZERO', '    :\n    [ "$n" -ge 1 ] 2>/dev/null || { echo "ZERO', 'a5'),
    ('m89 러너: 기록 글의 제어 바이트를 이스케이프하지 않음 (jstr · EO P1)', 'build_a5_vasp_package.py', '      for (k = 1; k < 32; k++) c[sprintf("%02x", k)] = sprintf("\\\\u%04x", k)', '      for (k = 1; k < 1; k++) c[sprintf("%02x", k)] = sprintf("\\\\u%04x", k)', 'a5'),
    ('m90 러너: attempt.start 잡 대조 뺌 (start_id · EO P1 Q-EO-2b)', 'build_a5_vasp_package.py', '  [ "$(rf "$R" job s)" = "$JOB" ] || { echo start_job; return; }', '  :', 'a5'),
    ('m91 러너: 중단 영수증 시간을 attempt.json 뒤로 (wall_of 옛 순서 · EO P1 Q-EO-2c)', 'build_a5_vasp_package.py', '  case "$d" in run_aborted/*)\n    w=$(rget "$d/infra_abort.json" wall_s s) || { echo BAD; return; }\n    if [ "$w" = UNKNOWN ] || secs_ok "$w"; then echo "$w"; else echo BAD; fi; return;;', '  case "$d" in run_aborted/*)\n    w=$(rget "$d/infra_abort.json" wall_s s) || { echo BAD; return; }\n    if [ "$w" = UNKNOWN ] || secs_ok "$w"; then echo "$w"; else echo BAD; fi;;', 'a5'),
    ('m92 러너: 사다리 시작의 장부 ↔ 보존 폴더 대조 뺌 (EO P1 Q-EO-3)', 'build_a5_vasp_package.py', 'tree_gate "다시 돌림"      # 잠금 다음', ':      # 잠금 다음', 'a5'),
    ('m93 러너: 장부 폴더 집합 = 보존 폴더 집합 대조 뺌 (ledger5 · EO P1 Q-EO-3)', 'build_a5_vasp_package.py', '  [ "$x" = "$lst" ] || { echo ledger_folders_differ; return; }', '  :', 'a5'),
    ('m94 러너: 중단 영수증 run_id = attempt.start 대조 뺌 (receipt5 · EO P1)', 'build_a5_vasp_package.py', '  [ "$(rf "$R" run_id s)" = "$(rget "$d/attempt.start" run_id s)" ] || { echo receipt_run_id; return; }', '  :', 'a5'),
    ('m95 러너: 끝 기록에 시도 목록을 안 묶음 (att5 · EO P2 Q-EO-4)', 'build_a5_vasp_package.py', '"$1" "$2" "$(jstr "$3")" "$(att5)" "$(utc)"', '"$1" "$2" "$(jstr "$3")" "" "$(utc)"', 'a5'),
    ('m96 러너: --infra-abort 가 행 손상 (행꼴 조각) 을 0 스텝으로 받음 (EO P0)', 'build_a5_vasp_package.py', '  [ "$g" = "0 -" ] || { echo "⛔ OSZICAR 완전한 전자 반복행', '  [ "${g%% *}" = 0 ] || { echo "⛔ OSZICAR 완전한 전자 반복행', 'a5'),
    ('m97 러너: --killed 가 행 손상을 기록함 (EO P0)', 'build_a5_vasp_package.py', '  [ "$rw" = - ] || { echo "⛔ $src OSZICAR 행 판독 $rw', '  true || { echo "⛔ $src OSZICAR 행 판독 $rw', 'a5'),
    ('m98 러너: --infra-wall 이 채운 시각을 안 남김 (EO P1 Q-EO-2c)', 'build_a5_vasp_package.py', '      END { printf ", \\"wall_s_filled_utc\\": \\"%s\\", \\"wall_s_filled_s\\": %s}\\n", U, S }', '      END { printf "}\\n" }', 'a5'),
    ('m99 검사기: 완전한 행 칸 규칙 뺌 (_complete_row · EO P0)', 'build_a5_vasp_package.py', '    return t if ok else None', '    return t if m else None', 'a5'),
    ('m100 검사기: 행 손상 · 남의 머리를 1저자 멈춤으로 안 봄 (a5_class · EO P0)', 'build_a5_vasp_package.py', '    if (x.get("row_scan") or {}).get("why", "-") != "-":\n        return "REVIEW", None', '    if False:\n        return "REVIEW", None', 'a5'),
    ('m101 검사기: 끝난 시도의 행 손상 · 남의 머리를 행 0 앞에서 안 봄 (EO P0)', 'build_a5_vasp_package.py', '    if why_rows:                                                             # 행 손상', '    if False:                                                             # 행 손상', 'a5'),
    ('m102 검사기: attempt.start 잡 대조 뺌 (start_problem · EO P1 Q-EO-2b)', 'build_a5_vasp_package.py', '    if rec_s(x, "job") != job_dir:\n        return "start_job"', '    if False:\n        return "start_job"', 'a5'),
    ('m103 검사기: attempt.start 가 그 폴더의 것인지 안 봄 (check_attempt5 · EO P1 Q-EO-2b)', 'build_a5_vasp_package.py', '        if sp_:\n            return done("ATTEMPT_MISMATCH"', '        if False:\n            return done("ATTEMPT_MISMATCH"', 'a5'),
    ('m104 러너: gate5 가 attempt.start 를 그 폴더와 대조 안 함 (BAD2 · EO P1 Q-EO-2b)', 'build_a5_vasp_package.py', '  x=$(start_id "$d" "$2"); [ "$x" = - ] || { echo "$x"; return; }', '  :', 'a5'),
    ('m105 검사기: 중단 영수증 시간을 attempt.json 뒤로 (wall_of 옛 순서 · EO P1 Q-EO-2c)', 'build_a5_vasp_package.py', '        w = rec_s(rec_read(os.path.join(d, "infra_abort.json")), "wall_s")\n        return "UNKNOWN" if w == "UNKNOWN" else (int(w) if w is not None and SECS_RE.fullmatch(w) else None)\n    p = os.path.join(d, "killed.json")', '        w = rec_s(rec_read(os.path.join(d, "infra_abort.json")), "wall_s")\n        pass\n    p = os.path.join(d, "killed.json")', 'a5'),
    ('m106 검사기: 띄울 때의 누적 상한 대조 뺌 (EO P1 Q-EO-2c)', 'build_a5_vasp_package.py', '        elif tot > cap_s:', '        elif False:', 'a5'),
    ('m107 검사기: 미상 영수증 뒤의 시도를 안 봄 (EO P1 Q-EO-2c — UNKNOWN 되돌림)', 'build_a5_vasp_package.py', '        if unk is not None:\n            viol.append(f"{t_} 앞 시도 {unk}', '        if False:\n            viol.append(f"{t_} 앞 시도 {unk}', 'a5'),
    ('m108 검사기: 벽시계를 채운 시각 ≤ 다음 시도 시작 대조 뺌 (EO P1 Q-EO-2c)', 'build_a5_vasp_package.py', '        if fill is not None and tm_.get("start") is not None and tm_["start"] < fill[1]:', '        if False:', 'a5'),
    ('m109 검사기: 장부 ↔ 보존 폴더 대조 뺌 (ledger_problems · EO P1 Q-EO-3)', 'build_a5_vasp_package.py', '    viol += ledger_problems(job, base)', '    viol += []', 'a5'),
    ('m110 검사기: 끝 기록의 시도 목록 대조 뺌 (final_problem — 트리 관문 · EO P2 Q-EO-4 · check_return 의 옛 대조는 관문 뒤 둘째 줄)', 'build_a5_vasp_package.py', '    if rec_s(x, "attempts") != attempts_of(base, job):\n        return "final_attempts_differ"', '    if False:\n        return "final_attempts_differ"', 'a5'),
    ('m111 검사기: 중단 영수증 run_id = attempt.start 대조 뺌 (abort_receipt_problem · EO P1)', 'build_a5_vasp_package.py', '    if rec_s(x, "run_id") != rec_s(s0, "run_id"):\n        return f"중단 영수증 run_id', '    if False:\n        return f"중단 영수증 run_id', 'a5'),
    ('m112 검사기: 0 스텝 중단 폴더의 행 손상을 안 봄 (EO P0)', 'build_a5_vasp_package.py', '        if (x_.get("row_scan") or {}).get("why", "-") != "-":\n            viol.append(f"{t_} 는 OSZICAR 행 판독', '        if False:\n            viol.append(f"{t_} 는 OSZICAR 행 판독', 'a5'),
    ('m113 러너: --infra-abort 가 attempt.start 를 그 폴더와 대조 안 함 (EO P1 Q-EO-2b)', 'build_a5_vasp_package.py', 'lock_take "기록 명령 $1"; tree_gate "기록 명령 $1";; esac', 'lock_take "기록 명령 $1";; esac', 'a5'),
    ('m114 러너: 행의 숫자 판독 뺌 (칸 ≥ 6 · N 정수만 — EP P0)', 'build_a5_vasp_package.py', '      if (lg && (k == 6 || k == 7) && t[1] ~ /^[1-9][0-9]*$/ && t[5] ~ /^[0-9]+$/ && t[2] ~ R && t[3] ~ R && t[4] ~ R && t[6] ~ R && (k == 6 || t[7] ~ R)) n++; else p++', '      if (lg && (k == 6 || k == 7) && t[1] ~ /^[1-9][0-9]*$/) n++; else p++', 'a5'),
    ('m115 러너: 콜론 앞 머리 조각을 끝 조각으로 안 봄 (EP P0)', 'build_a5_vasp_package.py', '    NR > NL { u = $0; sub(/^[ \\t]+/, "", u); if (u ~ /^[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?$/ && !(u != $0 && u ~ /^N *$/)) tp = 1 }', '    NR > NL { u = $0 }', 'a5'),
    ('m116 러너: 진행 폴더의 영수증을 시간 출처로 (wall_of 옛 · EP P1)', 'build_a5_vasp_package.py', '  case "$d" in run_aborted/*)\n    w=$(rget "$d/infra_abort.json" wall_s s) || { echo BAD; return; }', '  [ -e "$d/infra_abort.json" ] && case x in x)\n    w=$(rget "$d/infra_abort.json" wall_s s) || { echo BAD; return; }', 'a5'),
    ('m117 러너: 진행 폴더의 영수증 거부 뺌 (ledger5 · EP P1)', 'build_a5_vasp_package.py', '  case "$d" in run/*) [ ! -f "$d/infra_abort.json" ] || { echo stray_receipt; return; };; esac', '  :', 'a5'),
    ('m118 러너: 장부 줄 시각 순서 뺌 (ledger5 · EP P2)', 'build_a5_vasp_package.py', '    { [ "$w" -ge "$prs" ] && [ "$x" -ge "$pt0" ]; } 2>/dev/null || { echo "${b}_ledger_time_order"; return; }', '    :', 'a5'),
    ('m119 러너: 시도 이력 대조 뺌 (hist5 · EP P1)', 'build_a5_vasp_package.py', '  local S=run/status.tsv d have\n  { [ -e "$S" ] || [ -L "$S" ]; } || { echo -; return; }', '  local S=run/status.tsv d have\n  echo -; return', 'a5'),
    ('m120 러너: 장부 없을 때 시도 이력을 안 봄 (부분 복구 · EP P1)', 'build_a5_vasp_package.py', '    [ -z "$lst" ] && { hist5; return; }', '    [ -z "$lst" ] && { echo -; return; }', 'a5'),
    ('m121 러너: 끝난 시도의 끝 기록 신원 뺌 (gate5 end_id · EP 조건부)', 'build_a5_vasp_package.py', '  [ "${V[3]}" = "$(rf "$2" run_id s)" ] || { echo end_run_id; return; }', '  :', 'a5'),
    ('m122 러너: 보존 폴더의 끝 기록 신원 뺌 (receipt5 end_id · EP 조건부)', 'build_a5_vasp_package.py', '  [ "${V[5]}" = "$(rf "$2" t_start i)" ] || { echo end_t_start; return; }', '  :', 'a5'),
    ('m123 러너: 영수증 필수 칸 빈 값을 받음 (receipt5 · EP 조건부)', 'build_a5_vasp_package.py', '  for k in sched_job_id cancel_utc reason; do nbj "$(rf "$R" "$k" s)" || { echo "receipt_blank_$k"; return; }; done', '  :', 'a5'),
    ('m124 러너: 끊김 기록 필수 칸 빈 값을 받음 (killed5 · EP 조건부)', 'build_a5_vasp_package.py', '  for k in sched_job_id cancel_utc reason; do nbj "$(rf "$K" "$k" s)" || { echo "killed_json_blank_$k"; return; }; done', '  :', 'a5'),
    ('m125 러너: --killed 가 비 UTF-8 글을 씀 (u8ok · EP 조건부)', 'build_a5_vasp_package.py', '  { u8ok "$sid_r" && u8ok "$when_r" && u8ok "$why_r"; } || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유에 UTF-8 이 아닌 바이트가 있다 — 기록하지 않는다 (UTF-8 글로 다시 · Codex EP)"; exit 2; }\n  rid=$(rget "$src/attempt.start" run_id s)\n', '  :\n  rid=$(rget "$src/attempt.start" run_id s)\n', 'a5'),
    ('m126 러너: --infra-abort 가 비 UTF-8 글을 씀 (u8ok · EP 조건부)', 'build_a5_vasp_package.py', '  { u8ok "$sid_r" && u8ok "$when_r" && u8ok "$why_r"; } || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유에 UTF-8 이 아닌 바이트가 있다 — 기록하지 않는다 (UTF-8 글로 다시 · Codex EP)"; exit 2; }\n  if [ -n "${WALL_S:-}" ]; then', '  :\n  if [ -n "${WALL_S:-}" ]; then', 'a5'),
    ('m127 러너: 다시 돌림 전 끝 기록 대조 뺌 (fin_ok · EP 조건부)', 'build_a5_vasp_package.py', '  if [ -e run/final.json ]; then x=$(fin_ok); [ "$x" = - ] || { echo "$x"; return; }; fi', '  :', 'a5'),
    ('m128 러너: 포장만 전 끝 기록 대조 뺌 (fin_ok · EP 조건부)', 'build_a5_vasp_package.py', '[ "${PACK_ONLY:-0}" != 1 ] || { lock_take "PACK_ONLY 포장"; tree_gate "PACK_ONLY 포장"; }', '[ "${PACK_ONLY:-0}" != 1 ] || { lock_take "PACK_ONLY 포장"; }', 'a5'),
    ('m129 러너: 끝 기록의 시도 목록을 지금 목록과 대조 안 함 (fin_ok · EP 조건부)', 'build_a5_vasp_package.py', '  [ "$a" = "$(att5)" ] || { echo final_attempts_differ; return; }', '  :', 'a5'),
    ('m130 검사기: 행의 숫자 판독 뺌 (_complete_row · EP P0)', 'build_a5_vasp_package.py', '          and all(REAL_TOK.fullmatch(t[i]) for i in (1, 2, 3, 5)) and (len(t) == ROW_MIN_TOK or REAL_TOK.fullmatch(t[6]) is not None)', '          and True', 'a5'),
    ('m131 검사기: 콜론 앞 머리 조각을 끝 조각으로 안 봄 (row_gate · EP P0)', 'build_a5_vasp_package.py', '        if HDR_CUT.fullmatch(u) and not (u != tail and re.fullmatch(r"N *", u)):', '        if False:', 'a5'),
    ('m132 검사기: 진행 폴더의 영수증을 시간 출처로 (wall_of 옛 · EP P1)', 'build_a5_vasp_package.py', '    if os.path.basename(os.path.dirname(os.path.abspath(d))) == "run_aborted":       # 보존 폴더는', '    if os.path.lexists(os.path.join(d, "infra_abort.json")):       # 보존 폴더는', 'a5'),
    ('m133 검사기: 진행 폴더의 영수증 거부 뺌 (ledger_problems · EP P1)', 'build_a5_vasp_package.py', '    if rel.startswith("run/") and os.path.isfile(os.path.join(d, "infra_abort.json")):\n        return "stray_receipt"', '    if False:\n        return "stray_receipt"', 'a5'),
    ('m134 검사기: 장부 줄 시각 순서 뺌 (EP P2)', 'build_a5_vasp_package.py', '            if rs_ < prs or t0_ < pt0:', '            if False:', 'a5'),
    ('m135 검사기: 시도 이력 대조 뺌 (history_problems · EP P1)', 'build_a5_vasp_package.py', '    return _ledger_core(job, base) + history_problems(job, base)', '    return _ledger_core(job, base)', 'a5'),
    ('m136 검사기: 끝난 시도의 끝 기록 신원 뺌 (check_attempt5 end_problem · EP 조건부)', 'build_a5_vasp_package.py', '    ep_ = end_problem(attdir)', '    ep_ = None', 'a5'),
    ('m137 검사기: 보존 폴더의 끝 기록 신원 뺌 (abort_receipt_problem · EP 조건부)', 'build_a5_vasp_package.py', '    if vals[3] != rec_s(s0, "run_id"):\n        return "end_run_id"', '    if False:\n        return "end_run_id"', 'a5'),
    ('m138 검사기: 영수증 필수 칸 빈 값을 받음 (abort_receipt_problem · EP 조건부)', 'build_a5_vasp_package.py', '        if _blank(rec_s(x, f_)):\n            return f"중단 영수증 칸', '        if False:\n            return f"중단 영수증 칸', 'a5'),
    ('m139 검사기: 끊김 기록 필수 칸 빈 값을 받음 (killed_problems · EP 조건부)', 'build_a5_vasp_package.py', '        if _blank(rec_s(k, f_)):\n            return "KILLED_RECORD_MISMATCH"', '        if False:\n            return "KILLED_RECORD_MISMATCH"', 'a5'),
    ('m140 검사기: 끝 기록 없는 반송을 채택 (EP 조건부)', 'build_a5_vasp_package.py', '        if fin_rec is None:\n            res.update(status="STOPPED_FOR_REVIEW"', '        if False:\n            res.update(status="STOPPED_FOR_REVIEW"', 'a5'),
    ('m141 러너: 트리 관문 통째로 끔 (tree_gate → 늘 통과 · Codex EQ — 관문 하나를 빼면 반례 묶음이 한꺼번에 빨강인가)', 'build_a5_vasp_package.py', '  local x; x=$(tree5)\n  [ "$x" = - ] && return 0', '  return 0', 'a5'),
    ('m142 러너: 이름 검사 뺌 (tree5 → files5 · Codex EQ P1)', 'build_a5_vasp_package.py', '  x=$(files5); [ "$x" = - ] || { echo "$x"; return; }', '  :', 'a5'),
    ('m143 러너: 시도 폴더의 모르는 이름 · 잔여 *.part 거부 뺌 (files5 · Codex EQ P1)', 'build_a5_vasp_package.py', '      { [ -f "$f" ] && [ ! -L "$f" ] && [[ "$e" =~ ^($RET_ALLOW|$RET_FORBID|$ATT_EXTRA)$ ]]; } || { echo "file_$f"; return; }', '      :', 'a5'),
    ('m144 러너: run/ 의 모르는 이름 · 잔여 *.part 거부 뺌 (files5 · Codex EQ P1)', 'build_a5_vasp_package.py', '      *) echo "run_entry_$b"; return;;', '      *) ;;', 'a5'),
    ('m145 러너: 끝 기록 틀 (attempt.json) 거부 뺌 (tpl5 · Codex EQ P1)', 'build_a5_vasp_package.py', '    A=$(tpl5 "$d/attempt.json" "$ATT1_T") || { echo att_form; return; }', '    A=$(tpl5 "$d/attempt.json" "$ATT1_T") || { echo -; return; }', 'a5'),
    ('m146 러너: 봉인 (sha 표 = 지금 파일) 뺌 (att_ok5 · Codex EQ)', 'build_a5_vasp_package.py', '    if [ -f "$d/$f" ]; then [ "$k" = "$(h "$d/$f")" ] || { echo "seal_$f"; return; }', '    if true; then :', 'a5'),
    ('m147 러너: 끝 기록 · 끊김 기록 공존 거부 뺌 (rec_dir5 · Codex EQ P0)', 'build_a5_vasp_package.py', '    [ ! -f "$d/attempt.json" ] || { echo end_and_killed; return; }', '    [ ! -f "$d/attempt.json" ] || { echo -; return; }', 'a5'),
    ('m148 러너: 보존 폴더의 끊김 기록 거부 뺌 (rec_dir5 · Codex EQ)', 'build_a5_vasp_package.py', '    case "$d" in run_aborted/*) echo killed_in_aborted; return;; esac', '    :', 'a5'),
    ('m149 러너: 기록 UTF-8 읽기 검사 뺌 (rec_dir5 · Codex EQ P1)', 'build_a5_vasp_package.py', '    if [ -f "$d/$f" ] && ! u8f "$d/$f"; then echo "utf8_$f"; return; fi', '    :', 'a5'),
    ('m150 러너: 0 바이트 status.tsv 거부 뺌 (hist5 · Codex EQ P1)', 'build_a5_vasp_package.py', '  [ -s "$S" ] || { echo status_empty; return; }', '  :', 'a5'),
    ('m151 러너: 끝 기록 code/state 조합 뺌 (fin_ok · Codex EQ P1)', 'build_a5_vasp_package.py', '  case "$c:$s" in 0:OK|1:NO_PRIMARY|1:CLOSED|5:CAP|6:ENV|8:REVIEW) ;; *) echo final_code_state; return;; esac', '  :', 'a5'),
    ('m152 러너: 장부 단 순서 뺌 (ledger5 · Codex EQ P2)', 'build_a5_vasp_package.py', 'r = ($3 == "A5") ? 1 : (($3 == "c1") ? 2 : 3); if (r < pr) { print "BAD ledger_row_" i "_rung_order"; exit }; pr = r', 'r = 0', 'a5'),
    ('m153 러너: 기존 반송본 대조 뺌 (tree5 → tgz5 · Codex EQ P1)', 'build_a5_vasp_package.py', '  x=$(tgz5); [ "$x" = - ] || { echo "$x"; return; }', '  :', 'a5'),
    ('m154 러너: 반송본 끝 기록 대조 뺌 (tgz5 · Codex EQ P1)', 'build_a5_vasp_package.py', '  if [ -f "$T/x/run/final.json" ]; then cmp -s "$T/x/run/final.json" run/final.json || { echo tgz_final_differs; return; }; fi', '  :', 'a5'),
    ('m155 러너: 반송본 시도 대조 뺌 (tgz5 · Codex EQ P1)', 'build_a5_vasp_package.py', '    [ -n "$c" ] || { echo "tgz_attempt_missing_$b"; return; }', '    [ -n "$c" ] || continue', 'a5'),
    ('m156 러너: 반송본 끝 기록 바이트 대조 뺌 (tgz5 · Codex EQ P1)', 'build_a5_vasp_package.py', '      [ ! -f "$d/$e" ] || cmp -s "$d/$e" "$c/$e" || { echo "tgz_end_differs_$b/$e"; return; }', '      :', 'a5'),
    ('m157 러너: 단 발사 직전 관문 뺌 (cap_gate · Codex EQ)', 'build_a5_vasp_package.py', '  tree_gate "$1 발사 직전"', '  :', 'a5'),
    ('m158 러너: 포장 관문 뺌 (pack — 덮어쓰기 전 · Codex EQ)', 'build_a5_vasp_package.py', '  tree_gate 포장 ', '  : ', 'a5'),
    ('m159 러너: --killed 필수 칸 빈칸만 받음 (Codex EQ P1)', 'build_a5_vasp_package.py', '  { nbw "$sid" && nbw "$when" && nbw "$why"; } || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유가 다 있어야 한다 (빈칸 문자 — 공백 · 탭 · 줄바꿈 · VT · FF · CR — 만인 글도 안 된다 · Codex EQ)"; exit 2; }\n  { u8ok "$sid_r" && u8ok "$when_r" && u8ok "$why_r"; } || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유에 UTF-8 이 아닌 바이트가 있다 — 기록하지 않는다 (UTF-8 글로 다시 · Codex EP)"; exit 2; }\n  rid=$(rget', '  [ -n "$sid" ] && [ -n "$when" ] && [ -n "$why" ] || { echo "⛔"; exit 2; }\n  { u8ok "$sid_r" && u8ok "$when_r" && u8ok "$why_r"; } || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유에 UTF-8 이 아닌 바이트가 있다 — 기록하지 않는다 (UTF-8 글로 다시 · Codex EP)"; exit 2; }\n  rid=$(rget', 'a5'),
    ('m160 러너: --infra-abort 필수 칸 빈칸만 받음 (Codex EQ P1)', 'build_a5_vasp_package.py', '  { nbw "$sid" && nbw "$when" && nbw "$why"; } || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유가 다 있어야 한다 (빈칸 문자 — 공백 · 탭 · 줄바꿈 · VT · FF · CR — 만인 글도 안 된다 · Codex EQ)"; exit 2; }\n  { u8ok "$sid_r" && u8ok "$when_r" && u8ok "$why_r"; } || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유에 UTF-8 이 아닌 바이트가 있다 — 기록하지 않는다 (UTF-8 글로 다시 · Codex EP)"; exit 2; }\n  if [ -n "${WALL_S:-}" ]; then', '  [ -n "$sid" ] && [ -n "$when" ] && [ -n "$why" ] || { echo "⛔"; exit 2; }\n  { u8ok "$sid_r" && u8ok "$when_r" && u8ok "$why_r"; } || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유에 UTF-8 이 아닌 바이트가 있다 — 기록하지 않는다 (UTF-8 글로 다시 · Codex EP)"; exit 2; }\n  if [ -n "${WALL_S:-}" ]; then', 'a5'),
    ('m161 러너: 끝 기록을 임시 파일 · mv 없이 바로 씀 (run_one5 · Codex EQ P1)', 'build_a5_vasp_package.py', '> "$d/attempt.json.part" && mv -f "$d/attempt.json.part" "$d/attempt.json"', '> "$d/attempt.json"', 'a5'),
    ('m162 러너: 시작점 기록 문법 뺌 (tree5 → sp_rec5 · Codex EQ)', 'build_a5_vasp_package.py', '  if [ -e run/start_point.json ]; then x=$(sp_rec5); [ "$x" = - ] || { echo "$x"; return; }; fi', '  :', 'a5'),
    ('m163 러너: ⓪ 기록 틀 뺌 (tree5 → w0_rec5 · Codex EQ)', 'build_a5_vasp_package.py', '  if [ -e run/w0_check.json ]; then x=$(w0_rec5); [ "$x" = - ] || { echo "$x"; return; }; fi', '  :', 'a5'),
    ('m164 러너: 숫자 칸 길이 ≤ 24 뺌 (row_scan · Codex EQ P0)', 'build_a5_vasp_package.py', '      if (lg && (k == 6 || k == 7)', '      if ((k == 6 || k == 7)', 'a5'),
    ('m165 러너: 머리 조각의 앞 빈칸을 안 걷음 (row_scan · Codex EQ P0)', 'build_a5_vasp_package.py', 'NR > NL { u = $0; sub(/^[ \\t]+/, "", u); ', 'NR > NL { u = $0; ', 'a5'),
    ("m166 러너: 열 제목 'N' 예외 뺌 (row_scan · Codex EQ P0)", 'build_a5_vasp_package.py', ' && !(u != $0 && u ~ /^N *$/)) tp = 1 }', ') tp = 1 }', 'a5'),
    ('m167 러너: 시작 기록 없음을 문법 오류로 (no_start 뺌 · rec_dir5)', 'build_a5_vasp_package.py', '  [ -f "$d/attempt.start" ] || { echo no_start; return; }', '  :', 'a5'),
    ('m168 러너: 끊김 기록 문법 오류를 받음 (killed_rec5 · Codex EQ)', 'build_a5_vasp_package.py', '  K=$(rec5 "$1/killed.json") || { echo killed_json_form; return; }', '  K=$(rec5 "$1/killed.json") || { echo -; return; }', 'a5'),
    ('m169 검사기: 트리 관문 통째로 끔 (check_return → tree_problems · Codex EQ)', 'build_a5_vasp_package.py', '    viol += [f"트리 관문 ({t_}) — 러너는 이 트리에서 아무것도 쓰거나 띄우거나 포장하지 않고 멈춘다 (종료 8 · Codex EQ)" for t_ in tree_problems(job, base)]', '    viol += []', 'a5'),
    ('m170 검사기: 이름 검사 뺌 (tree_problems → files_problem · Codex EQ P1)', 'build_a5_vasp_package.py', '    fp_ = files_problem(J, base)\n    if fp_:', '    fp_ = None\n    if fp_:', 'a5'),
    ('m171 검사기: 끝 기록 틀 거부 뺌 (rec_dir_problem · Codex EQ P1)', 'build_a5_vasp_package.py', '        if vals is None:\n            return "att_form"', '        if vals is None:\n            return None', 'a5'),
    ('m172 검사기: 봉인 뺌 (att_problem · Codex EQ)', 'build_a5_vasp_package.py', '        if k != (_sha(p) if os.path.isfile(p) else ""):\n            return f"seal_{f}"', '        if False:\n            return f"seal_{f}"', 'a5'),
    ('m173 검사기: 끝 기록 · 끊김 기록 공존 거부 뺌 (rec_dir_problem · Codex EQ P0)', 'build_a5_vasp_package.py', '        if os.path.isfile(os.path.join(d, "attempt.json")):\n            return "end_and_killed"', '        if False:\n            return "end_and_killed"', 'a5'),
    ('m174 검사기: 보존 폴더의 끊김 기록 거부 뺌 (rec_dir_problem · Codex EQ)', 'build_a5_vasp_package.py', '        if rel.startswith("run_aborted/"):\n            return "killed_in_aborted"', '        if False:\n            return "killed_in_aborted"', 'a5'),
    ('m175 검사기: 기록 UTF-8 읽기 검사 뺌 (rec_dir_problem · Codex EQ P1)', 'build_a5_vasp_package.py', '            if raw_ is None or not _u8(raw_):\n                return f"utf8_{f}"', '            if False:\n                return f"utf8_{f}"', 'a5'),
    ('m176 검사기: 0 바이트 status.tsv 거부 뺌 (history_problems · Codex EQ P1)', 'build_a5_vasp_package.py', '    if not raw:\n        return ["시도 이력 (run/status.tsv) 이 0 바이트다', '    if False:\n        return ["시도 이력 (run/status.tsv) 이 0 바이트다', 'a5'),
    ('m177 검사기: 끝 기록 code/state 조합 뺌 (final_problem · Codex EQ P1)', 'build_a5_vasp_package.py', '    if (rec_i(x, "code"), rec_s(x, "state")) not in FINAL_COMBOS:', '    if False:', 'a5'),
    ('m178 검사기: 장부 단 순서 뺌 (_ledger_core · Codex EQ P2)', 'build_a5_vasp_package.py', '        if STAGES.index(f[2]) + 1 < pr:', '        if False:', 'a5'),
    ('m179 검사기: 트리 관문의 끊김 기록 run_id 결속 뺌 (killed_rec_problem · Codex EQ P0)', 'build_a5_vasp_package.py', '    if rec_s(k, "run_id") != rec_s(s0, "run_id"):\n        return "killed_run_id"', '    if False:\n        return "killed_run_id"', 'a5'),
    ('m180 검사기: 트리 관문의 끊김 기록 빈칸 뺌 (killed_rec_problem · Codex EQ P1)', 'build_a5_vasp_package.py', '        if _blank(rec_s(k, f_)):\n            return f"killed_json_blank_{f_}"', '        if False:\n            return f"killed_json_blank_{f_}"', 'a5'),
    ('m181 검사기: 시작점 기록 문법 뺌 (sp_problem · Codex EQ)', 'build_a5_vasp_package.py', '    if x is None or any(rec_s(x, k) is None for k in ("from", "path", "sha256", "head")) or rec_i(x, "written_s") is None:\n        return "start_point_form"', '    if False:\n        return "start_point_form"', 'a5'),
    ('m182 검사기: ⓪ 기록 틀 뺌 (w0_problem · Codex EQ)', 'build_a5_vasp_package.py', '    if tpl_parse(raw, W0_TPL) is None:\n        return "w0_form"', '    if False:\n        return "w0_form"', 'a5'),
    ('m183 검사기: 숫자 칸 길이 ≤ 24 뺌 (_complete_row · Codex EQ P0)', 'build_a5_vasp_package.py', '          and all(len(x) <= ROW_TOK_MAX for x in t))', '          and True)', 'a5'),
    ('m184 검사기: 머리 조각의 앞 빈칸을 안 걷음 (row_gate · Codex EQ P0)', 'build_a5_vasp_package.py', '        u = tail.lstrip(" \\t")', '        u = tail', 'a5'),
    ("m185 검사기: 열 제목 'N' 예외 뺌 (row_gate · Codex EQ P0)", 'build_a5_vasp_package.py', ' and not (u != tail and re.fullmatch(r"N *", u)):', ':', 'a5'),
    ('m186 검사기: 트리 관문의 시작 기록 신원 뺌 (rec_dir_problem · Codex EQ)', 'build_a5_vasp_package.py', '    sp_ = start_problem(job_dir, d, stage)\n    if sp_:\n        return sp_', '    sp_ = None\n    if sp_:\n        return sp_', 'a5'),
    ('m187 검사기: 시작 기록 없음을 문법 오류로 (no_start 뺌 · rec_dir_problem)', 'build_a5_vasp_package.py', '    if not os.path.isfile(os.path.join(d, "attempt.start")):\n        return "no_start"', '    if False:\n        return "no_start"', 'a5'),
    ('m188 검사기: 트리 관문의 끝 기록 t_start 신원 뺌 (att_problem · Codex EQ)', 'build_a5_vasp_package.py', '    if vals[5] != rec_i(s0, "t_start"):\n        return "end_t_start"', '    if False:\n        return "end_t_start"', 'a5'),
    ('m189 러너: 읽을 때 빈칸 판정이 공백만 걷음 (nbj — 빈칸 이스케이프를 글자로 셈 · Codex EQ P1 보강)', 'build_a5_vasp_package.py', "gsub(/\\\\[tnrf]|\\\\u00(0[9a-dA-D]|20)| /, \"\")", "gsub(/ /, \"\")", 'a5'),
    ('m190 검사기: 빈칸 판정이 공백만 걷음 (_blank — BLANK_ESC · Codex EQ P1 보강)', 'build_a5_vasp_package.py', '    return v is None or BLANK_ESC.sub("", v) == ""', '    return v is None or v.replace(" ", "") == ""', 'a5'),
    ('m191 러너: 쓸 때 빈칸 판정이 공백만 지움 (nbw — VT · FF 만인 글을 받음 · Codex EQ P1 보강)', 'build_a5_vasp_package.py', "tr -d ' \\t\\n\\v\\f\\r'", "tr -d ' '", 'a5'),
    ('m192 러너: 준비 폴더 내용 검사 뺌 (files5 — 실행 기록을 지움 · Codex ER Q-ER-1①)', 'build_a5_vasp_package.py', '      { [ -f "$f" ] && [ ! -L "$f" ] && [[ "$e" =~ ^($PREP_ALLOW)$ ]]; } || { echo "prep_$f"; return; }', '      :', 'a5'),
    ('m193 검사기: 준비 폴더 내용 검사 뺌 (files_problem · Codex ER Q-ER-1①)', 'build_a5_vasp_package.py', '            if not (n in PREP_ALLOW and isfile_(os.path.join(d, n))):\n                return f"prep_{rel}/{n}"', '            if False:\n                return f"prep_{rel}/{n}"', 'a5'),
    ('m194 러너: 끝 기록 쓰기 전 관문 뺌 (fin5 · Codex ER Q-ER-1②)', 'build_a5_vasp_package.py', '  tree_gate "끝 기록 쓰기 전 ($1 $2)"', '  :', 'a5'),
    ('m195 러너: A5 WAVECAR 지우기 전 관문 뺌 (drop5 · Codex ER Q-ER-1②)', 'build_a5_vasp_package.py', 'drop5(){ tree_gate "A5 WAVECAR 지우기 전"; rm -f', 'drop5(){ rm -f', 'a5'),
    ('m196 러너: 0 스텝의 설명 안 되는 줄을 받음 (row_scan · Codex ER Q-ER-2)', 'build_a5_vasp_package.py', 'else if (ux && n == 0) print 0, "unexplained_line"; ', '', 'a5'),
    ('m197 검사기: 0 스텝의 설명 안 되는 줄을 받음 (row_gate · Codex ER Q-ER-2)', 'build_a5_vasp_package.py', '    if ux and n == 0:', '    if False:', 'a5'),
    ('m198 러너: 이력 줄 벽시계 = 끝 기록 elapsed_s 대조 뺌 (hist5 · Codex ER Q-ER-3①)', 'build_a5_vasp_package.py', '      if ($10 != have[k]) { print "status_row_" i "_elapsed"; x = 1; exit }', '      if (0) { print "status_row_" i "_elapsed"; x = 1; exit }', 'a5'),
    ('m199 검사기: 이력 줄 벽시계 대조 뺌 (history_problems · Codex ER Q-ER-3①)', 'build_a5_vasp_package.py', '        if f[9] != have[k]:', '        if False:', 'a5'),
    ('m200 러너: 기록 명령의 배타 잠금 뺌 (Codex ER Q-ER-3②)', 'build_a5_vasp_package.py', 'lock_take "기록 명령 $1"; tree_gate "기록 명령 $1"', 'tree_gate "기록 명령 $1"', 'a5'),
    ('m201 러너: 반송본이 본 완전한 행의 후퇴 대조 뺌 (tgz5_in · Codex ER Q-ER-4)', 'build_a5_vasp_package.py', '      [ "${e%% *}" -ge "${x%% *}" ] 2>/dev/null || { echo "tgz_rows_lost_$b"; return; }', '      :', 'a5'),
    ('m202 러너: 반송본 영수증 벽시계 후퇴 대조 뺌 (tgz5_in · Codex ER Q-ER-4)', 'build_a5_vasp_package.py', '      [ "$x" = UNKNOWN ] || [ "$e" = "$x" ] || { echo "tgz_receipt_wall_$b"; return; }', '      :', 'a5'),
    ('m203 러너: 끝 기록 job 대조 뺌 (att_ok5 · Codex ER Q-ER-5)', 'build_a5_vasp_package.py', '  [ "${V[0]}" = "$(rf "$2" job s)" ] || { echo end_job; return; }', '  :', 'a5'),
    ('m204 러너: 끝 기록 attempt 대조 뺌 (att_ok5 · Codex ER Q-ER-5)', 'build_a5_vasp_package.py', '  [ "${V[1]}" = "$(rf "$2" attempt s)" ] || { echo end_attempt; return; }', '  :', 'a5'),
    ('m205 러너: 끝 기록 stage 대조 뺌 (att_ok5 · Codex ER Q-ER-5)', 'build_a5_vasp_package.py', '  [ "${V[2]}" = "$(rf "$2" stage s)" ] || { echo end_stage; return; }', '  :', 'a5'),
    ('m206 러너: 끝 기록 POTCAR 해시 = POTCAR.sha256 대조 뺌 (att_ok5 · Codex ER Q-ER-5)', 'build_a5_vasp_package.py', '  printf \'%s\\n\' "${V[14]}" | cmp -s - "$d/POTCAR.sha256" || { echo end_potcar_sha; return; }', '  :', 'a5'),
    ('m207 검사기: 끝 기록 job 대조 뺌 (att_problem · Codex ER Q-ER-5)', 'build_a5_vasp_package.py', '    if vals[0] != rec_s(s0, "job"):', '    if False:', 'a5'),
    ('m208 검사기: 끝 기록 attempt 대조 뺌 (att_problem · Codex ER Q-ER-5)', 'build_a5_vasp_package.py', '    if vals[1] != rec_s(s0, "attempt"):', '    if False:', 'a5'),
    ('m209 검사기: 끝 기록 stage 대조 뺌 (att_problem · Codex ER Q-ER-5)', 'build_a5_vasp_package.py', '    if vals[2] != rec_s(s0, "stage"):', '    if False:', 'a5'),
    ('m210 검사기: 끝 기록 POTCAR 해시 대조 뺌 (att_problem · Codex ER Q-ER-5)', 'build_a5_vasp_package.py', '    if _readb(os.path.join(d, "POTCAR.sha256")) != (vals[14] + "\\n").encode("latin-1"):', '    if False:', 'a5'),
)


def _mutants(names=None, jobs=1):
    """돌연변이마다 tools/wad 를 임시 폴더에 복사해 한 자리를 바꾸고 그 도구의 selftest 가 빨간불 (0 아닌 종료) 을 내는지 본다 (jobs 개씩 나란히).
    임시 폴더의 db/ 는 레포 db/ 로 잇는다 (REPO = 임시 폴더). 바꿀 자리가 정확히 한 번이 아니면 그 돌연변이는 '무효' 로 센다 (조용히 넘기지 않는다)."""
    import tempfile
    from concurrent.futures import ThreadPoolExecutor
    todo = [m for m in MUTANTS if not names or any(m[0].startswith(x) for x in names)]

    def one(m):
        name, fn, old, new, which = m
        with tempfile.TemporaryDirectory() as T:
            os.makedirs(os.path.join(T, "tools"))
            shutil.copytree(HERE, os.path.join(T, "tools", "wad"), ignore=shutil.ignore_patterns("__pycache__"))
            os.symlink(os.path.join(REPO, "db"), os.path.join(T, "db"))
            p = os.path.join(T, "tools", "wad", fn)
            src = open(p, encoding="utf-8").read()
            code, sep, table = src.partition("\nMUTANTS = (")          # 돌연변이 표 자체에 바꿀 글이 들어 있다 — 코드 부분에서만 센다 · 바꾼다
            if code.count(old) != 1:
                return name, f"무효 (코드에 자리 {code.count(old)} 번)", False
            _write(p, code.replace(old, new) + sep + table)
            tool = os.path.join(T, "tools", "wad", "build_a5_vasp_package.py" if which == "a5" else "build_v5_vasp_package.py")
            r = subprocess.run([sys.executable, "-I", tool, "--selftest"], capture_output=True, text=True, timeout=3600,
                               env={**os.environ, "A5_SELFTEST_FAILFAST": "1"})      # 첫 빨강에서 멈춤 (V5 selftest 는 이 변수를 보지 않는다)
            red = r.returncode != 0
            return name, ("빨강 ✓" if red else "초록 ✗ (시험이 못 잡음)"), red
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as ex:
        rows = list(ex.map(one, todo))
    caught = sum(1 for _, _, red in rows if red)
    for n, s, _ in rows:
        print(f"  {s:<22s} {n}")
    tot = len(rows)
    print(f"{'✅' if caught == tot else '⛔'} 돌연변이 {caught}/{tot} 잡음")
    return 0 if caught == tot else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--mutants", nargs="*", metavar="접두어", help="돌연변이 시험 (이름 접두어로 고를 수 있다)")
    ap.add_argument("--jobs", type=int, default=1, help="돌연변이를 나란히 돌릴 개수 (기본 1)")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--out", help="a5 묶음 폴더")
    ap.add_argument("--ret", help="반송 (a5_return.tgz 를 푼 곳)")
    ap.add_argument("--manifest_sha256", help="보낸 a5 묶음의 MANIFEST.sha256 sha256 (고정값)")
    ap.add_argument("--registry", help=f"외주 2차 봉인 등록부 JSON (기본 {REG_PATH})")
    ap.add_argument("--registry_sha256", help=f"등록부 sha256 (기본 {REG_SHA256[:12]}…)")
    ap.add_argument("--a5_result", metavar="OUT_JSON", help="V5 수집기 --a5_result 입력")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.mutants is not None:
        return _mutants(a.mutants, a.jobs)
    try:
        if a.build:
            if not a.out:
                ap.error("--build 에는 --out")
            meta, msha = build(a.out)
            print(f"✓ a5 묶음 {a.out} · MANIFEST sha256 {msha}")
            return 0
        if a.check:
            if not (a.out and a.ret and a.manifest_sha256):
                ap.error("--check 에는 --out · --ret · --manifest_sha256")
            reg, reg_sha = load_registry(a.registry, a.registry_sha256)      # 없으면 외주 2차 봉인 등록부 (고정 경로 · 고정 sha) — 재시작 문구 · 환경 대조에 필수
            meta, res = check_return(a.out, a.ret, a.manifest_sha256, reg)
            for k, v in res["attempts"].items():
                print(f"  {k:3s} {v['status']:<24s} {v.get('variant') or ''} {('· ' + str(v.get('why'))[:100]) if v.get('why') else ''}")
            print(f"  ⓪ {res['w0']['status']} (확인 {res['w0'].get('verified')}) · 시작점 {res['start_point']} · 사다리 위반 {res['ladder_violations'] or '없음'} → {res['status']}")
            if a.a5_result:
                _write(a.a5_result, json.dumps({"schema": SCHEMA_RESULT, "job": JOB, "package_manifest_sha256": a.manifest_sha256.lower(),
                                                "registry_sha256": reg_sha, "common_environment_failure": res["env_in"] or None,
                                                "result": res}, ensure_ascii=False, indent=1, default=float) + "\n")
                print(f"  → {a.a5_result} (sha256 {_sha(a.a5_result)})")
            return 0 if res["status"] in ("OK", "NO_PRIMARY_VALUE") else 3
    except PkgError as e:
        print(f"⛔ {e}")
        return 2
    ap.error("--selftest · --mutants · --build · --check 중 하나")


if __name__ == "__main__":
    sys.exit(main())
