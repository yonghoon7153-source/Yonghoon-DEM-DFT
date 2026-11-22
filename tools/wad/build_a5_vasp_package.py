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
    pack_fail · pack · finish · pp_ok · ver_of · wav_head · out_num · wsha + 성능 파일 · --infra-wall · PACK_ONLY 블록). 끝 줄은 bash -n 이 정한다
    (첫 번째로 문법이 닫히는 줄 — 손으로 괄호를 세지 않는다). 바꾸는 것은 고유 이름 · 판정 입력 (행 머리 관문) · 반송 파일 이름 · 포장에서 점 폴더 빼기 ·
    끝 안내 8 뿐이고, 바꿀 자리가 정확히 한 번 (또는 정한 횟수) 나오지 않으면 만들지 않는다. A5 자격 (elig5) 은 2차 elig_A 를 쓰지 않고 a5 판으로 쓴다
    ('기록은 유효한데 파일이 사라짐 · 바뀜' 을 ⓪ 으로 넘기지 않고 1저자로).
  a5 에서 새로 쓰는 것: 단마다 OSZICAR 행 머리 관문 (A5 · c1 = DAV/RMM · c2 = SDA/CGA · 모르는 머리 = SCF_UNVERIFIED) · 사다리 · ⓪ 확인 ·
  A5 의 재시작 확인 (시작 복사본 sha + 문구만 — A5 는 LWAVE T 라 끝 WAVECAR 가 새로 써진다) · 누적 상한 하나 (180 h) · 보조 기준 숫자 · 반송 사다리 대조 ·
  설정 에코 관문 (echo5 — a5 가 바꾼 NELM · LDIPOL · IALGO · AMIX · AMIN · MAXMIX · TIME 의 OUTCAR 해석값 · 러너와 검사기가 같은 부분집합).

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


GEN_ROW = re.compile(r"^[ \t]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:")    # 러너 hdr_gate 의 awk 와 같은 꼴 (줄 맨 앞 1–4 글자 + ':')


def row_gate(osz, stage):
    """OSZICAR 원문 → (행 수, 사유 | None) — 행 머리가 그 단의 허용 머리 밖이면 사유 'row_header_<머리>' (러너 hdr_gate 와 같다)."""
    allowed, n, bad = ROW_HDR[stage], 0, None
    for ln in (osz or "").split("\n"):
        if GEN_ROW.match(ln):
            n += 1
            h = ln.lstrip(" \t").split(":", 1)[0].replace(" ", "")
            if bad is None and h not in allowed:
                bad = f"row_header_{h}"
    return n, bad


def judge5(osz, out, incar, rc, stage):
    """a5 판정 = 행 머리 관문 + 외주 2차 judge_text (계약 ①–⑤ · 같은 규칙 · 같은 순서). 관문을 통과한 행 머리는 판정 입력에서 'DAV:' 로 바꿔 넘긴다
    (2차 계약의 행 정규식은 CGA 를 모른다 — 칸 위치는 같다). 러너 judge5() 와 같은 답 (selftest 가 같은 탐침으로 대조)."""
    if osz is None:
        return R2.judge_text(osz, out, incar, rc)
    n, bad = row_gate(osz, stage)
    if bad:
        return "SCF_UNVERIFIED", n, "NA", "NA", bad
    rx = re.compile(r"^([ \t]*)(" + "|".join(ROW_HDR[stage]) + r"):")
    feed = "\n".join(rx.sub(r"\1DAV:", ln) for ln in osz.split("\n"))
    return R2.judge_text(feed, out, incar, rc)


def osz_rows(osz, stage):
    """관문을 통과한 OSZICAR 의 전자 반복행 → [(스텝, E 토큰, dE, d eps, rms(c) (8 째 칸 · 머리 포함) | None)] (행 머리 관문 · 순서 그대로)."""
    rx = re.compile(r"^[ \t]*(" + "|".join(ROW_HDR[stage]) + r"):")
    out = []
    for ln in (osz or "").split("\n"):
        if rx.match(ln):
            t = [x for x in re.split(r"[ \t]+", ln) if x]
            out.append((t[1] if len(t) > 1 else "", t[2] if len(t) > 2 else "", t[3] if len(t) > 3 else "", t[4] if len(t) > 4 else "",
                        t[7] if len(t) > 7 else None))
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
    # 포장: 점으로 시작하는 폴더 (run/.prep_* 준비 폴더 · run/.a5.lock) 는 담지 않는다 (VASP 를 띄운 적 없는 임시 폴더 · 리뷰 P2(c))
    P["pack"] = _patch(P["pack"], 'grep -E "^(run|run_aborted)/[^/]+/(stageA/)?($RET_ALLOW)$"', 'grep -E "^(run|run_aborted)/[^/.][^/]*/(stageA/)?($RET_ALLOW)$"')
    # 끝 안내: 8 (1저자 검토 멈춤 · 개정 5 해석 1) 을 더한다
    P["finish"] = _patch(P["finish"], '    6) echo "⛔ 공통 환경 고장 — 전체 정지. 반송해 주시고 연락 주세요";;\n',
                         '    6) echo "⛔ 공통 환경 고장 — 전체 정지. 반송해 주시고 연락 주세요";;\n'
                         '    8) echo "⏸ 1저자 검토 멈춤 (개정 5 해석 1) — 더 돌리지 않았다. 반송해 주시고 1저자 결정을 기다려 주세요 (다시 돌려도 아무것도 띄우지 않는다)";;\n')
    # A5 자격 (elig5) 은 외주 2차 elig_A 를 쓰지 않고 a5 판으로 새로 쓴다 — '기록은 유효한데 파일이 사라짐 · 바뀜' 을 ⓪ 으로 넘기지 않고 1저자로 (RUN_A5_BODY)
    P["perf"] = r2_block('if [ -n "${PERF_TAGS_FILE:-}" ]; then')
    iw = r2_block('if [ "${1:-}" = "--infra-wall" ]; then')
    P["infra_wall"] = _patch(iw, "bash run_all.sh", "bash run_a5.sh", count=iw.count("bash run_all.sh") or 1)
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
#   기록 명령 (README): --infra-abort · --infra-wall · --killed · --reset-w0 · --unlock
#   종료: 0 c1 또는 c2 주 기준 수렴 (끝) · 1 주 기준 값 없음 — 사다리 끝 (끝 · 실패도 기록) · 2 인자 · 묶음 · 환경 오류 (아무것도 띄우지 않음)
#         3 준비 실패 (그 단은 소모 안 함 — 원인을 고친 뒤 다시) · 4 포장 실패 (PACK_ONLY=1 로 다시)
#         5 누적 상한 @CAP_H@ h (끝) 또는 끊긴 시도 · 벽시계 미상 (--killed · --infra-abort · --infra-wall 로 기록한 뒤 다시)
#         6 공통 환경 고장 (VASP 빌드 · PP — 전체 정지) · 7 전자 반복행 0 (--infra-abort 또는 연락) · 8 1저자 검토 멈춤 (끝)
#   끝 (0 · 1 · 5 상한 · 8 · 돈 뒤의 6 — VASP 빌드 다름) 뒤에 다시 돌리면 run/final.json 을 찍고 같은 코드로 끝낸다 — 아무것도 띄우지 않는다 (포장만: PACK_ONLY=1)
#   보내는 것: 끝 뒤 `sha256sum -c a5_return.tgz.sha256` 까지 통과한 쌍
#   지원 환경: Linux · bash ≥ 4 · GNU coreutils (find sort grep cmp sha256sum od stat mv -T) · GNU tar · awk (mawk/gawk) · sed -E
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

# ── 행 머리 관문 (검사기 row_gate 와 같다): 줄 맨 앞 1–4 글자 + ':' 를 행으로 보고, 그 단의 허용 머리 밖이면 SCF_UNVERIFIED ──
hdr_gate(){ awk -v A="^(${2})\$" '/^[ \t]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:/ { n++; h = $0; sub(/^[ \t]*/, "", h); sub(/:.*/, "", h); gsub(/ /, "", h)
    if (bad == "" && h !~ A) bad = "row_header_" h }
  END { print n + 0, (bad == "" ? "-" : bad) }' "$1/OSZICAR" 2>/dev/null; }
osz_feed(){ sed -E "s/^([[:space:]]*)(${HDR}):/\1DAV:/" "$1/OSZICAR" 2>/dev/null; }
judge5(){ # $1 시도 폴더 · $2 단 → "상태 행수 dE deps 사유" (judge 와 같은 꼴)
  local d=$1 HDR g n why
  HDR=$(stage_hdr "$2"); [ -n "$HDR" ] || { echo "SCF_UNVERIFIED 0 NA NA unknown_stage"; return; }
  [ -f "$d/OSZICAR" ] || { judge_r2 "$d"; return; }
  g=$(hdr_gate "$d" "$HDR"); n=${g%% *}; why=${g#* }
  [ -n "$g" ] || { judge_r2 "$d"; return; }
  if [ "$why" != "-" ]; then echo "SCF_UNVERIFIED ${n:-0} NA NA $why"; return; fi
  judge_r2 "$d"
}
rows_of(){ local n; n=$(grep -acE '^[[:space:]]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:' "$1/OSZICAR" 2>/dev/null); echo "${n:-0}"; }   # 전자 반복행 수 (관문과 같은 꼴 · 없으면 0)
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
  [ ! -f run/final.json ] || { echo "⛔ 이 사다리는 끝났다 (run/final.json: $(tr -d '\n' < run/final.json | cut -c1-200)) — 기록을 더하거나 고치지 않는다 (포장만: PACK_ONLY=1)"; exit 2; };;
esac

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
if [ "${1:-}" = "--infra-abort" ]; then
  [ $# -ge 5 ] || { echo "⛔ 쓰는 법: [WALL_S=<초>] bash run_a5.sh --infra-abort <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유…>"; exit 2; }
  st=$2; sid=$(clean "$3"); when=$(clean "$4"); shift 4; why=$(clean "$*")
  case "$st" in A5|c1|c2) ;; *) echo "⛔ 모르는 단 $st"; exit 2;; esac
  src=run/${JOB}_$st
  [ -d "$src" ] || { echo "⛔ $src 가 없다"; exit 2; }
  lx=$(later5 "$st"); [ -z "$lx" ] || { echo "⛔ 뒤 단 ($lx) 이 이미 있다 — $st 의 0 스텝 중단은 뒤 단을 띄우기 전에만 기록한다 (1저자에게 알린다)"; exit 2; }
  [ -f "$src/attempt.start" ] || { echo "⛔ $src 에 시작 표지 (attempt.start) 가 없다 — 이 러너가 띄운 시도가 아니다 (연락)"; exit 2; }
  if [ -e "$src/OSZICAR" ]; then
    n=$(grep -acE '^[[:space:]]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:' "$src/OSZICAR" 2>/dev/null); g=$?
    [ "$g" -le 1 ] && [ -n "$n" ] || { echo "⛔ $src/OSZICAR 를 읽지 못했다 (grep $g) — 0 행인지 확인할 수 없어 기록하지 않는다 (1저자)"; exit 2; }
    osz=zero_rows
  else
    n=0; osz=missing
  fi
  [ "$n" = 0 ] || { echo "⛔ 전자 반복행 $n 개 — 0 스텝 중단이 아니다 (끊긴 시도면 --killed · 실행 실패는 사다리가 다룬다)"; exit 2; }
  so=$(grep -acE '^[[:space:]]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:[[:space:]]+[0-9]' "$src/stdout.log" 2>/dev/null); so=${so:-0}
  oi=$(grep -acE 'Iteration +[0-9]+\(' "$src/OUTCAR" 2>/dev/null); oi=${oi:-0}
  [ "$so" = 0 ] && [ "$oi" = 0 ] || { echo "⛔ OSZICAR 는 $osz 인데 stdout.log 전자 반복행 $so · OUTCAR Iteration $oi — 출력 유실이지 0 스텝이 아니다 · 기록하지 않는다"; exit 2; }
  [ -n "$sid" ] && [ -n "$when" ] && [ -n "$why" ] || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유가 다 있어야 한다"; exit 2; }
  if [ -n "${WALL_S:-}" ]; then
    secs_ok "$WALL_S" || { echo "⛔ WALL_S '$WALL_S' — 0 이상의 10진 정수 (초 · 선행 0 없이 · 9 자리 이하) 여야 한다"; exit 2; }
    w=$WALL_S
  elif [ -f "$src/attempt.json" ]; then
    w=ATTEMPT_JSON
  else
    w=UNKNOWN
  fi
  k=$(awk -F'\t' -v j="$JOB" '$2 == j' run/infra_aborts.tsv 2>/dev/null | wc -l); k=${k:-0}
  [ "$k" -lt "$INFRA_MAX" ] || { echo "⛔ 0 스텝 중단 기록이 이미 $INFRA_MAX 회 — 상한 (1저자에게 알린다)"; exit 2; }
  mkdir -p run_aborted; dst=run_aborted/${JOB}_${st}_$((k + 1))
  mkdir "$dst" || exit 2
  shopt -s dotglob nullglob
  for f in "$src"/*; do mv "$f" "$dst/" || exit 2; done; rmdir "$src" || exit 2
  shopt -u dotglob nullglob
  rm -f "$dst/POTCAR" "$dst/WAVECAR" "$dst/CHGCAR" "$dst/CHG" "$dst/vasprun.xml" "$dst/.running"     # WAVECAR 는 복사본이다 (보존 ⓐ 원본 · A5 끝 WAVECAR 는 이 폴더 밖)
  if [ "$w" = ATTEMPT_JSON ]; then w=$(grep -o '"elapsed_s": [^,}]*[,}]' "$dst/attempt.json" | head -1 | sed 's/^"elapsed_s": //; s/[,}]$//'); secs_ok "$w" || w=UNKNOWN; fi
  printf '{"job": "%s", "rung": "%s", "sched_job_id": "%s", "cancel_utc": "%s", "reason": "%s", "wall_s": "%s", "oszicar": "%s", "recorded_utc": "%s", "recorded_s": %d}\n' \
    "$JOB" "$st" "$sid" "$when" "$why" "$w" "$osz" "$(utc)" "$(date +%s)" > "$dst/infra_abort.json"
  [ -f run/infra_aborts.tsv ] || printf "recorded_utc\tjob\trung\tsched_job_id\tcancel_utc\twall_s\treason\tdir\n" > run/infra_aborts.tsv
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$(utc)" "$JOB" "$st" "$sid" "$when" "$w" "$why" "$(basename "$dst")" >> run/infra_aborts.tsv
  if [ "$w" = UNKNOWN ]; then
    echo "✓ $src → $dst (0 스텝 인프라 중단 $((k + 1))/$INFRA_MAX) — ⚠ 벽시계 미상: 'bash run_a5.sh --infra-wall $(basename "$dst") <초>' 로 채울 때까지 다음 단이 뜨지 않는다"
  else
    echo "✓ $src → $dst (0 스텝 인프라 중단 $((k + 1))/$INFRA_MAX) — 다시 돌리면 같은 단부터"
  fi
  exit 0
fi

@INFRA_WALL@

# ── 전자 스텝 뒤 끊긴 시도의 벽시계 기록 (그 단 소모 · 값 없음 · 전자 반복행 ≥ 1 이어야 한다 · 뒤 단이 있으면 거부) ──
if [ "${1:-}" = "--killed" ]; then
  [ $# -ge 5 ] || { echo "⛔ 쓰는 법: WALL_S=<초> bash run_a5.sh --killed <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유…>"; exit 2; }
  st=$2; sid=$(clean "$3"); when=$(clean "$4"); shift 4; why=$(clean "$*")
  case "$st" in A5|c1|c2) ;; *) echo "⛔ 모르는 단 $st"; exit 2;; esac
  src=run/${JOB}_$st
  [ -f "$src/attempt.start" ] || { echo "⛔ $src 에 시작 표지 (attempt.start) 가 없다 — VASP 가 뜨지 않은 시도다"; exit 2; }
  [ ! -f "$src/attempt.json" ] || { echo "⛔ $src 는 끝난 시도다 (attempt.json 있음) — 기록하지 않는다"; exit 2; }
  [ ! -f "$src/killed.json" ] || { echo "⛔ $src 는 이미 기록했다 — 고치지 않는다"; exit 2; }
  lx=$(later5 "$st"); [ -z "$lx" ] || { echo "⛔ 뒤 단 ($lx) 이 이미 있다 — $st 의 끊김은 뒤 단을 띄우기 전에만 기록한다 (1저자에게 알린다)"; exit 2; }
  secs_ok "${WALL_S:-}" || { echo "⛔ WALL_S=<초> (스케줄러 장부의 그 시도 벽시계) 가 있어야 한다"; exit 2; }
  n=$(rows_of "$src")
  [ "$n" -ge 1 ] 2>/dev/null || { echo "⛔ $src OSZICAR 전자 반복행 0 — 0 스텝 중단이면 --infra-abort (OUTCAR 에만 반복 흔적이 있으면 출력 유실 — 연락)"; exit 2; }
  [ -n "$sid" ] && [ -n "$when" ] && [ -n "$why" ] || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유가 다 있어야 한다"; exit 2; }
  rid=$(grep -o '"run_id": "[^"]*"' "$src/attempt.start" | head -1 | sed 's/.*: "//; s/"$//')
  printf '{"job": "%s", "rung": "%s", "run_id": "%s", "wall_s": "%s", "sched_job_id": "%s", "cancel_utc": "%s", "reason": "%s", "osz_rows": "%s", "recorded_utc": "%s", "recorded_s": %d}\n' \
    "$JOB" "$st" "$rid" "$WALL_S" "$sid" "$when" "$why" "$n" "$(utc)" "$(date +%s)" > "$src/killed.json.part" && mv -f "$src/killed.json.part" "$src/killed.json" \
    || { echo "⛔ killed.json 쓰기 실패"; exit 2; }
  log "✎ $src 끊긴 시도 벽시계 $WALL_S 초 (스케줄러 $sid · $why · 전자 반복행 $n) — 그 단 소모 · 값 없음 · 다시 돌리지 않는다"
  echo "✓ $src 벽시계 $WALL_S 초 기록 — 다시 돌리면 다음 단부터 이어 간다"; exit 0
fi

@PACK_ONLY@

[ $# -eq 0 ] || { echo "⛔ 모르는 인자 '$1' — 계산은 인자 없이 돌린다 · 기록 명령은 --infra-abort · --infra-wall · --killed · --reset-w0 · --unlock (README)"; exit 2; }

# ── 계산 실행: 잠금을 잡는다 (같은 기계의 죽은 PID 잠금만 치운다 · 다른 기계의 잠금은 --unlock 으로만) ──
if ! mkdir "$LOCK" 2>/dev/null; then
  read -r LK_S LK_H LK_P <<< "$(lock_state)"
  case "$LK_S" in
    live|foreign) lock_say "$LK_S" "$LK_H" "$LK_P" "계산"; exit 2;;
    stale) echo "⚠ 남은 잠금 (기계 $LK_H · PID $LK_P — 이 기계 · 살아 있지 않다) — 치우고 진행"; rm -rf "$LOCK";;
  esac
  mkdir "$LOCK" 2>/dev/null || { echo "⛔ 잠금 (run/.a5.lock) 을 만들 수 없다 — 다른 실행이 막 시작했을 수 있다"; exit 2; }
fi
printf '%s %s\n' "$HOST" "$$" > "$LOCK/owner" || { rm -rf "$LOCK"; echo "⛔ 잠금 주인을 적지 못했다"; exit 2; }
trap 'rm -rf "$LOCK"' EXIT; trap 'exit 143' TERM; trap 'exit 129' HUP; trap 'exit 130' INT
# ── 끝난 사다리면 아무것도 띄우지 않는다 (리뷰 P1-1) ──
if [ -f run/final.json ]; then
  fc=$(grep -o '"code": [0-9]*' run/final.json | head -1 | grep -o '[0-9]*$')
  log "■ 다시 돌림 — 이 사다리는 이미 끝났다: $(tr -d '\n' < run/final.json | cut -c1-240)"
  echo "  아무것도 띄우지 않는다 · 보낼 것은 a5_return.tgz + .sha256 그대로 (포장만 다시: PACK_ONLY=1 bash run_a5.sh)"
  case "$fc" in 0|1|5|6|8) exit "$fc";; *) echo "⛔ run/final.json 의 코드 '$fc' 를 읽을 수 없다 — 연락"; exit 2;; esac
fi
[[ "$(up)" =~ ^[0-9]+$ ]] || { echo "⛔ /proc/uptime 을 읽을 수 없다 — 벽시계 장부는 단조 시계로 잰다 (Linux)"; exit 2; }
[ -n "${VASP_CMD:-}" ] || { echo "⛔ VASP_CMD 를 주세요 (예: mpirun -np 64 vasp_std)"; exit 2; }        # \${VAR:?} 는 1 로 끝난다 — 1 은 '값 없음' 이다 (종료 코드가 겹치지 않게)
[ -n "${POTCAR_DIR:-}" ] && [ -d "$POTCAR_DIR" ] || { echo "⛔ POTCAR_DIR 를 주세요 (PAW_PBE 폴더 · 있어야 한다: '${POTCAR_DIR:-}')"; exit 2; }
[ -n "${W0_WAVECAR:-}" ] || { echo "⛔ W0_WAVECAR 를 주세요 — 보존된 a4 ⓐ WAVECAR 경로 (외주 2차 묶음의 @W0_REL@ · 먼저 ls -l · sha256sum) · 없으면 W0_WAVECAR=none"; exit 2; }
PERF_LINES=""
@PERF@
{ echo "date_utc $(utc)"; echo "host $HOST"; echo "VASP_CMD $VASP_CMD"; echo "POTCAR_DIR $POTCAR_DIR"; echo "W0_WAVECAR $W0_WAVECAR"
  echo "PERF_TAGS $(printf '%s' "$PERF_LINES" | tr '\n' ';')"; echo "MANIFEST_sha256 $(h MANIFEST.sha256)"; } >> run/env.txt
[ -f run/status.tsv ] || printf "job\trung\tstage\trc\tstatus\tn_elec\tdE\tdeps\twhy\twall_s\n" > run/status.tsv
rm -rf "run/.prep_${JOB}_A5" "run/.prep_${JOB}_c1" "run/.prep_${JOB}_c2"     # 앞 실행의 남은 준비 폴더 (VASP 를 띄운 적 없음 · 잠금 아래)
'''

RUN_A5_BODY = r'''
# ── 누적 벽시계 (a5 의 모든 시도 · 0 스텝 중단 · 끊긴 시도 · 미상은 0 초가 아니다) ──
wall5(){ local d w tot=0 unk="" dirs=run lst
  [ -d run_aborted ] && dirs="run run_aborted"
  lst=$(find $dirs -path 'run/.prep_*' -prune -o \( -name attempt.json -o -name attempt.start -o -name infra_abort.json -o -name killed.json \) -type f -print 2>/dev/null) \
    || { echo "UNKNOWN (반송 폴더 열거 실패)"; return; }
  for d in $(printf '%s\n' "$lst" | sed 's#/[^/]*$##' | LC_ALL=C sort -u); do
    if [ -f "$d/attempt.json" ]; then w=$(grep -o '"elapsed_s": [^,}]*[,}]' "$d/attempt.json" | head -1 | sed 's/^"elapsed_s": //; s/[,}]$//')
    elif [ -f "$d/infra_abort.json" ]; then w=$(grep -o '"wall_s": "[^"]*"' "$d/infra_abort.json" | head -1 | sed 's/.*: "//; s/"$//')
    elif [ -f "$d/killed.json" ]; then w=$(grep -o '"wall_s": "[^"]*"' "$d/killed.json" | head -1 | sed 's/.*: "//; s/"$//')
    else w=""; fi
    if [[ "$w" =~ ^(0|[1-9][0-9]{0,11})$ ]]; then tot=$((tot + w)); else [ -n "$unk" ] || unk=$d; fi
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
  log "■ 끝 [$1 $2] $3"
  printf '{"code": %d, "state": "%s", "why": "%s", "written_utc": "%s", "written_s": %d}\n' "$1" "$2" "$(clean "$3")" "$(utc)" "$(date +%s)" > run/final.json.part \
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
        "$(stat -c %s "$d/WAVECAR" 2>/dev/null || echo 0)" "$hd" "$(out_num "$d" NKPTS)" "$(out_num "$d" NBANDS)" "$(out_num "$d" ENCUT)" "$rs" > "$d/WAVECAR.info";;
    c1|c2)
      wend=$(h "$d/WAVECAR")
      hon=0; [ "$istart" = 1 ] && [ "$icharg" = 0 ] && [ "$nr" = 0 ] && [ "$pr" = 1 ] && [ -n "$wsha" ] && [ "$wsha" = "$wcp" ] && [ "$wcp" = "$wend" ] && hon=1
      printf '{"src_sha256": "%s", "copied_sha256": "%s", "end_sha256": "%s", "istart": "%s", "icharg": "%s", "not_read_phrase": %s, "positive_regex_match": "%s", "honoured": %s, "start_head": "%s", "outcar": {"NKPTS": "%s", "NBANDS": "%s", "ENCUT": "%s"}}\n' \
        "$wsha" "$wcp" "$wend" "${istart:-NA}" "${icharg:-NA}" "$nr" "$pr" "$hon" "$SPH" "$(out_num "$d" NKPTS)" "$(out_num "$d" NBANDS)" "$(out_num "$d" ENCUT)" > "$d/WAVECAR.info";;
  esac
  if [ "$st" != c2 ]; then x=$(hist_max "$d"); case "$x" in ''|*[!0-9]*) ;; *) [ "$x" -gt 45 ] && echo "$(utc) $var info history_max $x" >> "$d/warn.log";; esac; fi
  printf '{"job": "%s", "attempt": "%s", "stage": "a5", "run_id": "%s", "rc": %d, "t_start": %d, "t_end": %d, "elapsed_s": %d, "vasp_version": "%s", "kernel_sha256": "", "perf": "%s", "sha256": {"INCAR": "%s", "POSCAR": "%s", "KPOINTS": "%s", "POTCAR": "%s", "OUTCAR": "%s", "OSZICAR": "%s", "WAVECAR.info": "%s", "stdout.log": "%s", "POTCAR.titel": "%s", "POTCAR.species.sha256": "%s", "attempt.start": "%s"}}\n' \
    "$JOB" "$var" "$rid" "$rc" "$t0" "$t1" "$el" "$ver" "$(printf '%s' "$PERF_LINES" | tr '\n' ';')" \
    "$(h "$d/INCAR")" "$(h "$d/POSCAR")" "$(h "$d/KPOINTS")" "$(cat "$d/POTCAR.sha256")" "$(h "$d/OUTCAR")" "$(h "$d/OSZICAR")" "$(h "$d/WAVECAR.info")" \
    "$(h "$d/stdout.log")" "$(h "$d/POTCAR.titel")" "$(h "$d/POTCAR.species.sha256")" "$(h "$d/attempt.start")" > "$d/attempt.json"
  j=$(judge5 "$d" "$st"); set -- $j
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$JOB" "$var" "a5" "$rc" "$1" "$2" "$3" "$4" "$5" "$el" >> run/status.tsv
  rm -f "$d/POTCAR" "$d/CHGCAR" "$d/CHG" "$d/vasprun.xml" "$d/vdw_kernel.bindat" "$d/LOCPOT"
  [ "$st" = A5 ] || rm -f "$d/WAVECAR"          # c1 · c2 의 WAVECAR 는 복사본 (끝 sha 를 잰 뒤 지운다) · A5 WAVECAR 는 사다리가 끝날 때까지 둔다 (반송 안 함)
  return 0
}

# ── 단의 갈래 (개정 5 해석 1 · 사용자 2026-11-20 — 러너와 검사기가 같은 순서로 본다) ──
var_of(){ grep -o '"attempt": "[^"]*"' "$1/attempt.start" 2>/dev/null | head -1 | sed 's/.*: "//; s/"$//'; }
gate5(){ # $1 시도 폴더 · $2 단 → "갈래 상태 행수 사유" (빈칸 없는 낱말 넷)
  #   NEW 띄울 차례 · WAIT5 끊김 (끝 기록 없음) · ZERO 전자 반복행 0 (멈춤 7) · ENV 다른 VASP 빌드 (끝 6) · REVIEW 1저자 (끝 8) · BAD2 이 러너가 띄운 시도가 아님 ·
  #   OK 주 기준 수렴 · NEXT 다음 단 (SCF_NOT_CONVERGED · 행 ≥ 1 실행 실패 · 행 ≥ 1 끊김 기록)
  local d=$1 st=$2 n var ver e s
  [ -e "$d" ] || { echo "NEW - 0 -"; return; }
  { [ -d "$d" ] && [ -f "$d/attempt.start" ]; } || { echo "BAD2 - 0 no_start_marker"; return; }
  var=$(var_of "$d")
  case "$st:$var" in A5:A5c|A5:A5f|c1:c1|c2:c2) ;; *) echo "BAD2 - 0 variant_${var:-none}"; return;; esac
  n=$(rows_of "$d"); ver=$(clean "$(ver_of "$d")")
  if [ -f "$d/attempt.json" ]; then
    if [ -n "$ver" ] && [ "$ver" != "$REL_VER" ]; then echo "ENV VERSION_MISMATCH $n vasp_build"; return; fi
    [ "$n" -ge 1 ] 2>/dev/null || { echo "ZERO SCF_UNVERIFIED 0 no_rows"; return; }
    e=$(echo5 "$d" "$var"); [ "$e" = "-" ] || { echo "REVIEW SETTINGS_ECHO $n $e"; return; }
    s=$(stat5 "$d" "$st" "$SS")
    case "$s" in OK) echo "OK OK $n -";; SCF_NOT_CONVERGED|RUN_FAILED) echo "NEXT $s $n -";; *) echo "REVIEW $s $n -";; esac
    return
  fi
  [ -f "$d/killed.json" ] || { echo "WAIT5 INCOMPLETE_ATTEMPT $n no_end_record"; return; }
  if [ -n "$ver" ] && [ "$ver" != "$REL_VER" ]; then echo "ENV VERSION_MISMATCH $n vasp_build"; return; fi
  [ "$n" -ge 1 ] 2>/dev/null || { echo "REVIEW KILLED_NO_ROWS 0 -"; return; }
  e=$(echo5 "$d" "$var"); [ "$e" = "-" ] || { echo "REVIEW SETTINGS_ECHO $n $e"; return; }
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
    BAD2) log "⛔ $st 폴더 (run/${JOB}_$st) 는 이 러너가 띄운 시도가 아니다 ($why) — 아무것도 띄우지 않는다 · 연락"; exit 2;;
    *) log "⛔ $st 갈래 '$k' 를 모른다 — 연락"; exit 2;;
  esac
}
cap_gate(){ # $1 단 — 띄우기 전 누적 상한 (넘으면 끝 5 · 벽시계 미상이면 멈춤 5)
  cap_ok; case $? in
    0) return 0;;
    1) fin5 5 CAP "누적 상한 $CAP_H h — $1 를 띄우지 않았다 (1저자)";;
    *) stop5 5 "벽시계 미상 · 장부 이상 — '--infra-wall' 또는 '--killed' 로 채운 뒤 다시 ($1 앞)";;
  esac
}
drop5(){ rm -f "run/${JOB}_A5/WAVECAR"; }    # 사다리 끝 (0 · 1) 에서만 — A5 끝 WAVECAR 는 반송하지 않는다 · 멈춤 (3 · 5 · 7 · 8) 에서는 남긴다 (검토 · 이어 돌리기용)
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
sp_field(){ grep -o "\"$1\": \"[^\"]*\"" run/start_point.json 2>/dev/null | head -1 | sed 's/.*: "//; s/"$//'; }
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
  [ ! -f run/start_point.json ] && [ ! -e "$C1" ] && [ ! -e "$C2" ] || fin5 8 REVIEW "A5 가 없는데 뒤 단 기록이 있다 (시작점 · c1 · c2)"
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
  { [ ! -e "$C1" ] && [ ! -e "$C2" ]; } || fin5 8 REVIEW "c 단이 있는데 시작점 기록이 없다"
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
  [ ! -e "$C2" ] || fin5 8 REVIEW "c1 이 없는데 c2 가 있다"
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


def run_a5_text():
    P = r2_parts()
    funcs = "\n".join(P[n] for n in R2_FUNCS)
    head = (RUN_A5_HEAD.replace("@RET_ALLOW@", "|".join(re.escape(x) for x in RETURN_ALLOWED))
            .replace("@RET_FORBID@", "|".join(re.escape(x) for x in RETURN_FORBIDDEN)).replace("@JOB@", JOB)
            .replace("@CAP_H@", f"{CAP_H:g}").replace("@INFRA_MAX@", str(INFRA_MAX)))
    cli = (RUN_A5_CLI.replace("@INFRA_WALL@", P["infra_wall"]).replace("@PACK_ONLY@", P["pack_only"]).replace("@PERF@", P["perf"])
           .replace("@W0_REL@", W0_REL))
    txt = head + "\n# ── 외주 2차 러너 부품 (build_round2_vasp_package.RUN_ALL 에서 이름으로 꺼냄 · 패치 자리는 build_a5 r2_parts) ──\n" + funcs + "\n" + RUN_A5_ENV + cli + RUN_A5_BODY
    for ph in ("@JOB@", "@RET_ALLOW@", "@RET_FORBID@", "@CAP_H@", "@INFRA_MAX@", "@INFRA_WALL@", "@PACK_ONLY@", "@PERF@", "@W0_REL@"):
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
              "6": "공통 환경 고장 (VASP 빌드 · PP — 전체 정지 · 돈 뒤 빌드가 다르면 끝 · 띄우기 전 PP 불일치는 끝 기록 없음)", "7": "전자 반복행 0 (멈춤 · --infra-abort 또는 연락)", "8": "1저자 검토 멈춤 (끝)"}


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
- 다음 단은 지금 단이 **SCF_NOT_CONVERGED** 이거나 **전자 반복행 ≥ 1 인 실행 실패** (끊김을 `--killed` 로 기록한 것 포함) 로 끝났을 때만 띄웁니다.
- **전자 반복행 0** → 멈춤 (종료 7 · 다음 단을 쓰지 않습니다): 스케줄러 기록이 있는 0 스텝 인프라 중단이면 `--infra-abort` 로 기록한 뒤 다시 (같은 단부터) ·
  아니면 (실행 파일 · 모듈 · 입력 문제) 고치기 전에 연락 주세요.
- **재시작 미이행 · SCF 미확인 · 설정 에코 다름** → 멈춤 (종료 8 · 끝 · 1저자 검토).
- A5 가 전자 반복행은 있는데 자격 미달이면 (실행 실패 · WAVECAR 이상) 개정 5 그대로 — 보존 ⓐ 가 확인돼 있으면 c1 · c2 를 그 복사본에서 · 아니면 닫습니다 (종료 1).

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
- 보내는 것: `a5_return.tgz` + `a5_return.tgz.sha256` (`sha256sum -c a5_return.tgz.sha256` 통과 뒤). WAVECAR · CHGCAR · POTCAR 본문은 담지 않습니다.

## 5. 기록 명령 (계산이 돌고 있지 않을 때)
- 0 스텝 인프라 중단: `[WALL_S=<초>] bash run_a5.sh --infra-abort <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유>` — 뒤 단이 이미 있으면 거부 · 잡 전체 {INFRA_MAX} 회
- 벽시계 채우기: `bash run_a5.sh --infra-wall <run_aborted 폴더 이름> <초>`
- 끊긴 시도 (전자 반복행 ≥ 1): `WALL_S=<초> bash run_a5.sh --killed <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유>` — 뒤 단이 이미 있으면 거부
- ⓪ 기록 지우기 (A5 를 띄우기 전에만): `bash run_a5.sh --reset-w0`
- 잠금 지우기: 잠금 주인은 기계 이름 + PID 입니다. 다른 기계의 잠금은 살아 있는지 알 수 없어 러너가 거부합니다 —
  스케줄러로 그 잡이 끝났는지 확인한 뒤, 러너가 찍어 준 그대로 `bash run_a5.sh --unlock <기계> <PID>`.

## 6. 하지 말 것
- INCAR · POSCAR · KPOINTS 를 고치지 마세요 · 시도 폴더 (run/ · run_aborted/) 를 지우거나 옮기지 마세요 (러너가 이 기록으로 다음 단 · 시작점을 정합니다).
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
    a, s = _jread(os.path.join(d, "attempt.json")), _jread(os.path.join(d, "attempt.start"))
    rec = [x.get("recorded_s") for x in (_jread(os.path.join(d, "killed.json")), _jread(os.path.join(d, "infra_abort.json"))) if isint(x.get("recorded_s"))]
    t0 = a.get("t_start") if isint(a.get("t_start")) else (s.get("t_start") if isint(s.get("t_start")) else None)
    return {"start": t0, "end": a.get("t_end") if isint(a.get("t_end")) else None, "recorded": max(rec) if rec else None}


def _head_dims(head):
    """WAVECAR 머리 문자열 (wav_head 꼴 6 칸) → (NKPTS, NBANDS, ENCUT) 문자열 · 못 읽으면 None."""
    hd = str(head or "").split()
    return (hd[3], hd[4], hd[5]) if len(hd) >= 6 else None


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
    r["osz_rows"] = row_gate(osz, stage)[0] if osz else 0
    r["times"] = _times(attdir)
    if not os.path.isfile(os.path.join(attdir, "attempt.json")):
        if r["killed"]:
            r["echo5"] = dict(zip(("missing", "bad"), echo5(R2._read(os.path.join(attdir, "OUTCAR")) or "",
                                                              _jread(os.path.join(attdir, "attempt.start")).get("attempt"))))
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
        try:
            dims_ok = (sd is not None and dims.get("NKPTS") == sd[0] and dims.get("NBANDS") == sd[1]
                       and all(re.fullmatch(r"[0-9]+(\.[0-9]+)?", str(x)) for x in (dims.get("ENCUT"), sd[2])) and abs(float(dims["ENCUT"]) - float(sd[2])) < 0.05)
        except (TypeError, ValueError):
            dims_ok = False
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
    f = _jread(p)
    if not f or f.get("code") not in (0, 1, 5, 6, 8) or isinstance(f.get("code"), bool):
        return None, "final.json 형식 (code 0 · 1 · 5 · 6 · 8)"
    return f, None


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
    if s == "INCOMPLETE_ATTEMPT":
        if x.get("killed"):
            e = x.get("echo5") or {}
            if (x.get("osz_rows") or 0) < 1 or e.get("missing") or e.get("bad"):
                return "REVIEW", None
            return "NEXT", None
        return ("WAIT" if x.get("started") else "PREP_ONLY"), None
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
                    found.append((tag, k, check_attempt5(job, pkgdir, d, m.group(2), registry, src_sha.get(m.group(2)), (src_head or {}).get(m.group(2)))))
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
    for t_, k_, x_ in aborted:
        if (x_.get("osz_rows") or 0) > 0:
            viol.append(f"{t_} 는 전자 반복행 {x_.get('osz_rows')} 개 — 0 스텝 중단으로 옮길 수 없는 시도다")
        if t_.startswith("A5@") and x_.get("variant") and x_["variant"] != want_var:
            viol.append(f"{t_} 변형 {x_['variant']} ≠ ⓪ 판정에 맞는 변형 ({want_var})")
    if len(aborted) > INFRA_MAX:
        viol.append(f"0 스텝 인프라 중단 {len(aborted)} 회 > 잡 전체 {INFRA_MAX} 회")
    if A["status"] != "MISSING" and A.get("variant") and A["variant"] != want_var:
        viol.append(f"A5 변형 {A['variant']} ≠ ⓪ 판정에 맞는 변형 ({want_var})")
    seq = []                                  # 띄운 시도 (attempt.start 있음) 만 순서에 넣는다 — 준비만 있는 폴더는 사다리 대조 (PREP_ONLY) 가 다룬다
    for s_ in STAGES:
        for t_, k_, x_ in sorted((y for y in aborted if y[0].startswith(f"{s_}@")), key=lambda y: y[1]):
            if x_.get("started"):
                seq.append((t_, x_.get("times") or {}))
            elif x_.get("status") != "ATTEMPT_UNREADABLE":
                viol.append(f"{t_} 에 시작 표지 (attempt.start) 가 없다 — 러너는 띄운 시도만 0 스텝 중단으로 옮긴다")
        if att[s_].get("started"):
            seq.append((s_, att[s_].get("times") or {}))
    viol += order_violations(seq)

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
        if fin_rec is not None and fin_rec.get("code") != want_code:
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
beh = plan.get(st, "conv")
nelm = int(iv(inc, "NELM")); lwave = (iv(inc, "LWAVE") or "").upper().strip(".") in ("TRUE", "T")
ldip = (iv(inc, "LDIPOL") or "").upper().strip(".") in ("TRUE", "T")
ist_in = int(iv(inc, "ISTART") or 0); ich_in = int(iv(inc, "ICHARG") or 2)
ist = 1 if (ist_in == 1 and os.path.isfile("WAVECAR") and beh not in ("noread", "istart0")) else 0
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
if beh in ("conv", "sda_rows", "dav_rows", "unknown_hdr", "noread", "istart0", "modwav", "badhead", "badecho", "nowav", "nophrase", "d3off"):
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
osz = open("OSZICAR", "w")
osz.write("       N       E                     dE             d eps       ncg     rms          rms(c)\n")
for i, (k, e, de, dp, rmsc) in enumerate(rr):
    h = h1 if i == 0 else h2
    osz.write(f"{h}: {k:4d}   {e:.12E}   {de: .5E}   {dp: .5E}  8000   0.300E-03    {rmsc:.3E}\n")
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
if ist == 1 and beh != "nophrase":
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
        ck(rechk(exv)["status"] == "LADDER_VIOLATION", "⛔음성 c1 OK 인데 반송에 c2 가 있다 → LADDER_VIOLATION")
        # 시작점 기록 · 끝 기록 · 순서 (반송을 고쳐서)
        exs = unpack(w1, "s1sp"); os.remove(os.path.join(exs, "run", "start_point.json"))
        ck(rechk(exs)["status"] == "START_POINT_MISSING", "⛔음성 c1 이 있는데 시작점 기록이 없다 → START_POINT_MISSING (리뷰 P0-2(b))")
        exs = unpack(w1, "s1sp2"); spj = os.path.join(exs, "run", "start_point.json")
        wrec = json.load(open(os.path.join(exs, "run", "w0_check.json")))
        _write(spj, json.dumps({"from": "W0", "path": w0p, "sha256": w0["sha256"], "head": wrec["head"]}))
        rsp = rechk(exs)
        ck(rsp["status"] == "START_POINT_MISMATCH", f"⛔음성 시작점 기록 W0 인데 A5 가 자격 → START_POINT_MISMATCH (규칙과 대조) — {rsp['status']} {rsp.get('why', '')[:80]}")
        _write(spj, "{not json")
        ck(rechk(exs)["status"] == "START_POINT_MISMATCH", "⛔음성 시작점 기록을 못 읽음 → START_POINT_MISMATCH (형식)")
        exf = unpack(w1, "s1fin"); fj = os.path.join(exf, "run", "final.json"); d_ = json.load(open(fj)); d_["code"] = 1; _write(fj, json.dumps(d_))
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
        ro2 = rechk(exo2)
        ck(ro2["status"] == "LADDER_VIOLATION", f"⛔음성 A5 0 스텝 중단 기록이 c1 뒤 → LADDER_VIOLATION (늦은 중단 · 리뷰 P0-2(a)) — {ro2['status']} {ro2.get('why', '')[:80]}")
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
        def s2_variant(tag, how):
            exx = unpack(w2, f"s2{tag}"); c2d = os.path.join(exx, "run", f"{JOB}_c2")
            if how == "missing":
                shutil.rmtree(c2d)
            elif how == "prep":
                for f_ in os.listdir(c2d):
                    if f_ not in ("INCAR", "POSCAR", "KPOINTS"):
                        os.remove(os.path.join(c2d, f_))
            elif how in ("wait", "killed", "killed0"):
                tend = json.load(open(os.path.join(c2d, "attempt.json")))["t_end"]
                os.remove(os.path.join(c2d, "attempt.json"))
                if how == "killed0":
                    _write(os.path.join(c2d, "OSZICAR"), "       N       E                     dE             d eps       ncg     rms          rms(c)\n")
                if how != "wait":
                    _write(os.path.join(c2d, "killed.json"), json.dumps({"job": JOB, "rung": "c2", "wall_s": "100", "osz_rows": "30", "recorded_s": tend + 1}))
            fj_ = os.path.join(exx, "run", "final.json")
            if how == "killed":
                _write(fj_, json.dumps({"code": 1, "state": "NO_PRIMARY", "why": "c2 끊김 (시험)"}))
            elif os.path.exists(fj_):
                os.remove(fj_)                                      # 끝나지 않은 사다리 (포장만 다시 한 반송)
            return rechk(exx)
        for how_, want_ in (("missing", "LADDER_INCOMPLETE"), ("prep", "LADDER_INCOMPLETE"), ("wait", "LADDER_INCOMPLETE"), ("killed0", "STOPPED_FOR_REVIEW")):
            rv_ = s2_variant(how_, how_)
            a_ = adopt(rv_)
            ck(rv_["status"] == want_ and a_.get("adopted") is None, f"⛔음성 c1 정체 · c2 {how_} → {want_} · c1 보조 자동 채택 없음 (리뷰 P0-1) — {rv_['status']} · {a_.get('adopted')}")
        rv_ = s2_variant("killed", "killed"); a_ = adopt(rv_)
        ck(rv_["status"] == "NO_PRIMARY_VALUE" and a_.get("adopted") == "a5_c1" and a_.get("a5_rule") == "secondary",
           f"c1 정체 · c2 행 ≥ 1 끊김 기록 (확인된 끝) → NO_PRIMARY_VALUE · c1 보조 채택 — {rv_['status']} · {a_.get('adopted')}")
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
        shutil.rmtree(D(w15, "c2")); os.remove(os.path.join(w15, "run", "final.json"))
        aj = os.path.join(D(w15, "c1"), "attempt.json")
        t_ = open(aj).read(); _write(aj, re.sub(r'"elapsed_s": \d+', '"elapsed_s": 700000', t_))
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
        os.makedirs(D(wk, "c2")); pkl = rcmd(wk, "--killed", "c1", "s", "t", "r", env_extra={"WALL_S": "100"}); os.rmdir(D(wk, "c2"))
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
        # S21: 러너 judge5 = 검사기 judge5 (같은 탐침 · 단마다)
        probes = {"conv": dav(30), "sda": dav(30).replace("DAV:", "SDA:"), "cga": sda, "xyz": dav(30).replace("DAV:", "XYZ:"), "cgsp": dav(30) + "CG :  31   1  1  1\n",
                  "nospace": "SDA:1 -0.1E+03 -3E-08 -1E-08\n", "nan": dav(29) + "DAV:   30   -7.3E+02   NaN   NaN  1  1  1\n", "empty": ""}
        harness = os.path.join(T, "harness.sh")
        hb = "\n".join(r2_block(f"{n}(){{") for n in ("incar_val",)) + "\n" + _patch(_patch(r2_block("judge(){"), "judge(){", "judge_r2(){"),
                                                                                         'cat "$d/OSZICAR" 2>/dev/null |', 'osz_feed "$d" |')
        body = RUN_A5_ENV[RUN_A5_ENV.index("stage_hdr(){"):RUN_A5_ENV.index("rows_of(){")]
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
    ("m01 관문 끔 (c1 이 SDA/CGA 도 받음)", "build_a5_vasp_package.py", 'ROW_HDR = {"A5": ("DAV", "RMM"), "c1": ("DAV", "RMM"),', 'ROW_HDR = {"A5": ("DAV", "RMM"), "c1": ("DAV", "RMM", "SDA", "CGA"),', "a5"),
    ("m02 c2 가 DAV 도 받음", "build_a5_vasp_package.py", '"c2": ("SDA", "CGA")}', '"c2": ("SDA", "CGA", "DAV")}', "a5"),
    ("m03 보조 최소 스텝 100 → 10", "build_a5_vasp_package.py", "SEC_W1, SEC_W0, SEC_MIN_STEPS = 50, 50, 100", "SEC_W1, SEC_W0, SEC_MIN_STEPS = 50, 50, 10", "a5"),
    ("m04 u_E 에서 평균 이동 뺌", "build_a5_vasp_package.py", '"u_E_eV": max(rng, shift)', '"u_E_eV": rng', "a5"),
    ("m05 A5 에도 보조 숫자", "build_a5_vasp_package.py", 'if stage not in ("c1", "c2"):\n        return None, f"보조 기준은', 'if stage not in ("c1", "c2", "A5", "a4A", "r1B"):\n        return None, f"보조 기준은', "a5"),
    ("m06 ⓪ 크기 확인 뺌 (러너)", "build_a5_vasp_package.py", 'elif [ "$z" != "$W0_SIZE" ]; then why="크기 다름"', 'elif false; then why="크기 다름"', "a5"),
    ("m07 c1 OK 여도 c2 띄움", "build_a5_vasp_package.py", '  drop5; log "✓ c1 주 기준 수렴 — c2 를 띄우지 않는다"; fin5 0 OK "c1 주 기준 수렴"', "  :", "a5"),
    ("m08 누적 상한 확인 뺌", "build_a5_vasp_package.py", "awk -v w=\"$w\" -v c=\"$CAP_H\" 'BEGIN { exit !(w <= c * 3600) }' ||", "true ||", "a5"),
    ("m09 c1 · c2 끝 sha 를 안 봄 (러너)", "build_a5_vasp_package.py", '[ "$wsha" = "$wcp" ] && [ "$wcp" = "$wend" ] && hon=1', '[ "$wsha" = "$wcp" ] && hon=1', "a5"),
    ("m10 A5 재시작에 끝 sha 를 요구 (러너 A5 를 c 단처럼)", "build_a5_vasp_package.py", 'ok_ = (V.HEX64.match(str(rs.get("src_sha256", ""))) is not None and rs.get("src_sha256") == rs.get("copied_sha256") == src_sha',
     'ok_ = (V.HEX64.match(str(rs.get("src_sha256", ""))) is not None and rs.get("src_sha256") == rs.get("copied_sha256") == src_sha == (w or {}).get("sha256")', "a5"),
    ("m11 MAXMIX 해석값 확인 뺌 (검사기)", "build_a5_vasp_package.py", '"c1": {"IALGO": 38, "AMIX": 0.1, "AMIN": 0.01, "MAXMIX": 200}, "c2"', '"c1": {"IALGO": 38, "AMIX": 0.1, "AMIN": 0.01}, "c2"', "a5"),
    ("m12 사다리 대조 (c1 OK 인데 c2) 뺌", "build_a5_vasp_package.py", '                if present("c2"):\n                    viol.append("c2 가 있는데 c1 이 주 기준 OK',
     '                if False:\n                    viol.append("c2 가 있는데 c1 이 주 기준 OK', "a5"),
    ("m13 수집기 u_W 문턱 0.002 → 0.02", "build_v5_vasp_package.py", "A5_SEC_MAX_UW = 0.002", "A5_SEC_MAX_UW = 0.02", "v5"),
    ("m14 수집기 G4 가 u_W 를 안 더함", "build_v5_vasp_package.py", "if abs(dw) + uW <= G4_DW:", "if abs(dw) <= G4_DW:", "v5"),
    ("m15 수집기 둘 다 보조 불일치 확인 뺌", "build_v5_vasp_package.py", "if abs(e1 - e2) > u1 + u2:", "if False:", "v5"),
    ("m16 수집기 순서: c1 보조가 c2 주보다 먼저", "build_v5_vasp_package.py", "A5_ORDER = (\"c1:primary\", \"c2:primary\", \"c1:secondary\", \"c2:secondary\")",
     "A5_ORDER = (\"c1:primary\", \"c1:secondary\", \"c2:primary\", \"c2:secondary\")", "v5"),
    ("m17 수집기 보조 기준이 A5 를 받음", "build_v5_vasp_package.py", 'A5_SEC_STAGES = ("c1", "c2")', 'A5_SEC_STAGES = ("c1", "c2", "A5")', "v5"),
    ("m18 수집기 보조 최소 스텝 확인 뺌", "build_v5_vasp_package.py", "if not isinstance(n, int) or isinstance(n, bool) or n < A5_SEC_MIN_STEPS:", "if False:", "v5"),
    ("m19 러너 관문: c1 이 SDA/CGA 도 받음 (bash)", "build_a5_vasp_package.py", "stage_hdr(){ case \"$1\" in A5|c1) echo 'DAV|RMM';;", "stage_hdr(){ case \"$1\" in A5|c1) echo 'DAV|RMM|SDA|CGA';;", "a5"),
    ("m20 러너 중복 실행 거부 뺌", "build_a5_vasp_package.py", '    live|foreign) lock_say "$LK_S" "$LK_H" "$LK_P" "계산"; exit 2;;', '    live|foreign) rm -rf "$LOCK";;', "a5"),
    ("m21 러너 ⓪ 머리 확인 뺌", "build_a5_vasp_package.py", "elif ! { [ $# -ge 6 ] && [ \"$4\" = \"$W0_NK\" ] && [ \"$5\" = \"$W0_NB\" ] && enc_eq \"$6\" \"$W0_EN\"; }; then", "elif false; then", "a5"),
    ("m22 검사기 c 단 재시작이 시작 sha 를 안 봄", "build_a5_vasp_package.py", "if not (src_sha and V.HEX64.match(src_sha) and w.get(\"src_sha256\") == src_sha):", "if False:", "a5"),
    # ── 리뷰 수정 (P0-1 · P0-2 · P1 · P2 · P3 · 개정 5 해석 1) 의 새 관문 ──
    ("m23 러너: 행 0 을 다음 단으로 넘김 (해석 1 · ZERO → NEXT)", "build_a5_vasp_package.py", '[ "$n" -ge 1 ] 2>/dev/null || { echo "ZERO SCF_UNVERIFIED 0 no_rows"; return; }',
     '[ "$n" -ge 1 ] 2>/dev/null || { echo "NEXT RUN_FAILED 0 no_rows"; return; }', "a5"),
    ("m24 러너: 재시작 미이행 · SCF 미확인 멈춤 뺌 (REVIEW → NEXT)", "build_a5_vasp_package.py", '*) echo "REVIEW $s $n -";; esac', '*) echo "NEXT $s $n -";; esac', "a5"),
    ("m25 러너: 끝 기록 확인 뺌 (끝난 사다리를 다시 돌림 · P1-1)", "build_a5_vasp_package.py", 'if [ -f run/final.json ]; then\n  fc=$(grep -o', 'if false; then\n  fc=$(grep -o', "a5"),
    ("m26 러너: 시작점을 기록에서 읽지 않고 다시 정함 (P0-2(b))", "build_a5_vasp_package.py", 'if [ -f run/start_point.json ]; then\n  sp_load ||', 'if false; then\n  sp_load ||', "a5"),
    ("m27 러너: --infra-abort 뒤 단 거부 뺌 (P0-2(c))", "build_a5_vasp_package.py", 'lx=$(later5 "$st"); [ -z "$lx" ] || { echo "⛔ 뒤 단 ($lx) 이 이미 있다 — $st 의 0 스텝 중단은',
     'lx=""; [ -z "$lx" ] || { echo "⛔ 뒤 단 ($lx) 이 이미 있다 — $st 의 0 스텝 중단은', "a5"),
    ("m28 러너: --killed 뒤 단 거부 뺌 (P0-2(c))", "build_a5_vasp_package.py", 'lx=$(later5 "$st"); [ -z "$lx" ] || { echo "⛔ 뒤 단 ($lx) 이 이미 있다 — $st 의 끊김은',
     'lx=""; [ -z "$lx" ] || { echo "⛔ 뒤 단 ($lx) 이 이미 있다 — $st 의 끊김은', "a5"),
    ("m29 러너: 없는 W0 경로를 '확인 안 됨' 으로 기록 (옛 동작 · P1-3)", "build_a5_vasp_package.py",
     "  else\n    echo \"⛔ W0_WAVECAR '$p' 가 없거나 읽을 수 없다 — 기록하지 않았다. 'ls -l' · 'sha256sum' 으로 경로를 확인하고, 정말 없으면 W0_WAVECAR=none 으로 다시\"; exit 2\n  fi",
     '  else why="파일이 없거나 읽을 수 없다"; fi', "a5"),
    ("m30 러너: 상대 W0 경로를 부른 곳 기준으로 풀지 않음 (P1-3)", "build_a5_vasp_package.py",
     'if [ -n "${W0_WAVECAR:-}" ] && [ "$W0_WAVECAR" != none ]; then W0_WAVECAR=$(absp "$W0_WAVECAR"); fi', ":", "a5"),
    ("m31 러너: 묶음 폴더 검사 뺌 (P2(g))", "build_a5_vasp_package.py", '[ -z "$FX" ] || { echo "⛔ 이 폴더에 a5 묶음이 아닌 것이 있다:', 'true || { echo "⛔ 이 폴더에 a5 묶음이 아닌 것이 있다:', "a5"),
    ("m32 러너: 다른 기계 잠금을 이 기계 잠금처럼 봄 (P2(d))", "build_a5_vasp_package.py", 'if [ "$hh" != "$HOST" ]; then echo "foreign $hh $pp"', 'if false; then echo "foreign $hh $pp"', "a5"),
    ("m33 러너: 준비 실패 때 임시 폴더를 안 지움 (P2(c))", "build_a5_vasp_package.py",
     'pfail(){ log "⛔ $2 — 준비 실패 · 그 단은 소모되지 않았다 (임시 폴더를 지웠다 · 원인 — 디스크 · 권한 · 경로 — 을 고친 뒤 다시)"; rm -rf "$1"; }',
     'pfail(){ log "⛔ $2 — 준비 실패"; }', "a5"),
    ("m34 러너: 설정 에코 관문 뺌 (해석 1)", "build_a5_vasp_package.py", 'e=$(echo5 "$d" "$var"); [ "$e" = "-" ] || { echo "REVIEW SETTINGS_ECHO $n $e"; return; }\n    s=$(stat5 "$d" "$st" "$SS")',
     'e=-\n    s=$(stat5 "$d" "$st" "$SS")', "a5"),
    ("m35 러너: c 단 재시작에서 시작 WAVECAR 머리 (NBANDS) 를 안 봄 (P3)", "build_a5_vasp_package.py",
     '      && [ "$(out_num "$d" NKPTS)" = "${SP_NK:-x}" ] && [ "$(out_num "$d" NBANDS)" = "${SP_NB:-x}" ] && enc_eq "$(out_num "$d" ENCUT)" "${SP_EN:-x}"; } \\',
     '      ; } \\', "a5"),
    ("m36 러너: --killed 에 행 ≥ 1 요구 뺌 (해석 1)", "build_a5_vasp_package.py", '  [ "$n" -ge 1 ] 2>/dev/null || { echo "⛔ $src OSZICAR 전자 반복행 0',
     '  true || { echo "⛔ $src OSZICAR 전자 반복행 0', "a5"),
    ("m37 러너: 시작점을 기록하지 않고 c1 을 띄움 (P0-2(b))", "build_a5_vasp_package.py", '  if [ ! -f run/start_point.json ]; then\n    sp_write ||', '  if false; then\n    sp_write ||', "a5"),
    ("m38 검사기: 행 0 을 재시작 확인 뒤에 (옛 순서 · P2(f))", "build_a5_vasp_package.py", '    if not n:\n        kw = {"conflicts"', '    if False:\n        kw = {"conflicts"', "a5"),
    ("m39 검사기: c1 정체 뒤 c2 없음 · 끝 기록 없음 · 행 0 을 사다리 미완으로 안 봄 (P0-1)", "build_a5_vasp_package.py",
     '                if k2 in ("MISSING", "PREP_ONLY", "WAIT", "ZERO"):\n                    incomplete.append(', '                if False:\n                    incomplete.append(', "a5"),
    ("m40 검사기: c2 의 주 기준 미정 (REVIEW) 을 1저자 멈춤으로 안 봄 (P0-1)", "build_a5_vasp_package.py",
     '                elif k2 == "REVIEW":\n                    review.append(', '                elif False:\n                    review.append(', "a5"),
    ("m41 검사기: 사다리 순서 대조 뺌 (P0-2(a))", "build_a5_vasp_package.py", "    viol += order_violations(seq)", "    viol += []", "a5"),
    ("m42 검사기: 시작점 기록을 규칙과 대조 안 함 (P2(e))", "build_a5_vasp_package.py", "            if sp is not None and not _same_start(sp, rule):", "            if False:", "a5"),
    ("m43 검사기: c 단이 있는데 시작점 기록 없음을 안 봄 (P0-2(b))", "build_a5_vasp_package.py", '            if (present("c1") or present("c2")) and sp is None:',
     "            if False:", "a5"),
    ("m44 검사기: c 단 OUTCAR NBANDS ≠ 시작 WAVECAR 머리를 안 봄 (P3)", "build_a5_vasp_package.py", "        if not dims_ok:\n", "        if False:\n", "a5"),
    ("m45 검사기: 검사기만 본 실패를 보고하지 않음 (P2(e))", "build_a5_vasp_package.py", '        if cls[s_][1]:\n            review.append(', '        if False:\n            review.append(', "a5"),
    ("m46 검사기: 러너 끝 기록 대조 뺌", "build_a5_vasp_package.py", 'if fin_rec is not None and fin_rec.get("code") != want_code:', "if False:", "a5"),
    ("m47 검사기: 행 0 을 사다리 미완 대신 재시작 단계로 넘김 (a5_class ZERO 뺌)", "build_a5_vasp_package.py", '    if not j.get("n_elec_steps"):\n        return "ZERO", None',
     '    if False:\n        return "ZERO", None', "a5"),
    ("m48 수집기: c1 보조에 'c2 확인된 끝' 조건 뺌 (P0-1)", "build_v5_vasp_package.py",
     '    if "c1:secondary" in cand and "c2:primary" not in cand and not a5_c2_confirmed(atts.get("c2")):', "    if False:", "v5"),
    ("m49 수집기: c 단 재시작 미이행이어도 채택 (P0-2(d))", "build_v5_vasp_package.py", "    if rnh:\n", "    if False:\n", "v5"),
    ("m50 수집기: 총 W 라벨에 개정 5 라벨을 안 실음 (P2(b))", "build_v5_vasp_package.py", "        if dep4 is not None:\n            labels += [", "        if False:\n            labels += [", "v5"),
    ("m51 수집기: 채택 기록에 시작점을 안 실음 (P2(a))", "build_v5_vasp_package.py",
     '"labels": [A5_LABEL] + ([A5_SEC_LABEL] if rule == "secondary" else []), "adoption_history": hist, "a5_start_point": spx}',
     '"labels": [A5_LABEL] + ([A5_SEC_LABEL] if rule == "secondary" else []), "adoption_history": hist}', "v5"),
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
            r = subprocess.run([sys.executable, "-I", tool, "--selftest"], capture_output=True, text=True, timeout=3600)
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
