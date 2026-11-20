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
    pack_fail · pack · finish · pp_ok · ver_of · wav_head · out_num · wsha · elig_A + 성능 파일 · --infra-wall · PACK_ONLY 블록). 끝 줄은 bash -n 이 정한다
    (첫 번째로 문법이 닫히는 줄 — 손으로 괄호를 세지 않는다). 바꾸는 것은 고유 이름 · 판정 입력 (행 머리 관문) · 반송 파일 이름뿐이고, 바꿀 자리가
    정확히 한 번 (또는 정한 횟수) 나오지 않으면 만들지 않는다.
  a5 에서 새로 쓰는 것: 단마다 OSZICAR 행 머리 관문 (A5 · c1 = DAV/RMM · c2 = SDA/CGA · 모르는 머리 = SCF_UNVERIFIED) · 사다리 · ⓪ 확인 ·
  A5 의 재시작 확인 (시작 복사본 sha + 문구만 — A5 는 LWAVE T 라 끝 WAVECAR 가 새로 써진다) · 누적 상한 하나 (180 h) · 보조 기준 숫자 · 반송 사다리 대조.

⛔ 이 도구가 못 하는 것:
   · VASP 를 돌리지 않는다 · 구조를 만들지 않는다 (V5 봉인 묶음의 sha 로 결박만) · SCF 판정은 OSZICAR · OUTCAR 기록만 본다 (해의 유일성 · 같은 바닥상태는 모른다)
   · c2 (ALGO All) 의 OSZICAR 행 머리 (SDA · CGA) 는 5.4.4 실물로 확인하지 않았다 — 첫 반송에서 확인한다. 다른 머리면 SCF_UNVERIFIED 로 멈춘다 (조용히 넘어가지 않는다)
   · 행 머리 관문은 줄 맨 앞 1–4 글자 + ':' 을 '행' 으로 본다 — 그 꼴이 아닌 실물 행은 2차 계약 (행 없음 → SCF_UNVERIFIED) 이 잡는다
   · 보조 기준의 u_E 는 창 두 개 (마지막 50 · 그 앞 50 스텝) 의 E 만 본다 — 창 밖으로 이어지는 느린 드리프트는 과소 평가할 수 있다 (개정 5 '한계')
   · u_W 문턱 (0.002 J/m²) · G4 판정 · 채택 순서는 이 도구가 아니라 V5 수집기가 그 면적으로 한다 (여기서 u_W 를 내지 않는다 — 면적이 두 곳에 있지 않게)
   · ⓪ 원본이 업체 서버에서 안 바뀌었는지는 sha · 크기 · 머리로만 본다 · 업체 작업 트리 전체를 감사하지 않는다 (반송물에 담긴 흔적만)
   · 이력 길이 (Broyden 고유값 개수) · rms(c) 급등은 정보다 — 판정에 쓰지 않는다 (설정 검사는 OUTCAR 의 MAXMIX · IALGO · TIME 해석값으로 따로 한다)
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
MGMT = ("run/env.txt", "run/status.tsv", "run/infra_aborts.tsv", "run/w0_check.json")
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
            "pp_ok", "ver_of", "wav_head", "out_num", "wsha", "elig_A")


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
    # ⓐ 자격: 판정을 A5 행 머리 관문으로 (나머지 — WAVECAR · 머리 · 기록 sha — 는 그대로)
    P["elig_A"] = _patch(_patch(P["elig_A"], "elig_A(){", "elig5(){"), 's=$(stat_of "$d" A)', 's=$(stat5 "$d" A5)')
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
#   필수: VASP_CMD · POTCAR_DIR (PAW_PBE: <POTCAR_DIR>/{Li_sv,P,S,Cl,Ag}/POTCAR) · W0_WAVECAR (보존 ⓐ WAVECAR 경로 — 없으면 W0_WAVECAR=none 을 적는다)
#   선택: PERF_TAGS_FILE (한 줄에 대입 하나 · NCORE/NPAR/KPAR/NSIM 양의 정수 · LPLANE/LSCALU/LSCALAPACK) · PACK_ONLY=1 · WATCH_S (경보 점검 초 · 기본 60)
#   0 스텝 인프라 중단 (전자 반복행 0 · 스케줄러 기록이 있을 때만 · 잡 전체 @INFRA_MAX@ 회):
#     [WALL_S=<초>] bash run_a5.sh --infra-abort <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유…>   → run_aborted/ 로 옮긴다 · 다시 돌리면 같은 단부터
#     bash run_a5.sh --infra-wall <run_aborted 폴더 이름> <초>   (벽시계가 미상일 때만)
#   전자 스텝 뒤 러너째 끊긴 시도 (attempt.json 없음 · 다시 돌리지 않는다 · 그 단 소모): WALL_S=<초> bash run_a5.sh --killed <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유…>
#   ⛔ INCAR·POSCAR·KPOINTS 를 고치지 마세요 · 시도 폴더가 있으면 덮어쓰지 않습니다 (다시 돌리면 기록을 다시 판정해 다음 단을 정합니다)
#   종료: 0 c1 또는 c2 주 기준 수렴 · 1 주 기준 값 없음 (묶음 만듦 — 실패도 기록 · 보조 기준은 반송 뒤 우리가 본다) · 2 패키지·환경·인자 오류
#         4 포장 실패 (PACK_ONLY=1 로 다시) · 5 누적 상한 @CAP_H@ h 또는 벽시계 미상 (다음 단을 띄우지 않음) · 6 공통 환경 고장 (VASP 빌드 · PP — 전체 정지)
#   보내는 것: 종료 0·1·5·6 뒤 `sha256sum -c a5_return.tgz.sha256` 까지 통과한 쌍
#   지원 환경: Linux · bash ≥ 4 · GNU coreutils (find sort grep cmp sha256sum od stat) · GNU tar · awk (mawk/gawk) · sed -E
# =============================================================================
set -u
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
sha256sum -c --quiet MANIFEST.sha256 || { echo "⛔ 패키지 파일이 MANIFEST 와 다르다 — 실행하지 않는다"; exit 2; }
RET_ALLOW='@RET_ALLOW@'
RET_FORBID='@RET_FORBID@'
JOB=@JOB@
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
# ── 중복 실행 막기 — 잠금 폴더 run/.a5.lock (원자적 mkdir) 에 PID · 살아 있는 실행이 있으면 계산 · 기록 · 포장 명령을 다 거부한다 ──
lock_live(){ local op; op=$(cat run/.a5.lock/pid 2>/dev/null); [ -n "$op" ] && kill -0 "$op" 2>/dev/null; }
if lock_live; then
  case "${1:-}" in --infra-abort|--infra-wall|--killed) echo "⛔ run_a5.sh (PID $(cat run/.a5.lock/pid)) 가 돌고 있다 — 기록 명령은 그 실행이 끝난 뒤에"; exit 2;; esac
  [ "${PACK_ONLY:-0}" = 1 ] && { echo "⛔ run_a5.sh (PID $(cat run/.a5.lock/pid)) 가 돌고 있다 — 포장은 그 실행이 끝난 뒤에"; exit 2; }
fi

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
stat5(){ # $1 시도 폴더 · $2 단 · $3 시작 WAVECAR sha (c1 · c2) → 상태 (c1 · c2 는 재시작 확인 먼저 · A5 는 재시작이 자격이 아니다)
  local d=$1 j
  [ -f "$d/attempt.json" ] || { echo INCOMPLETE_ATTEMPT; return; }
  case "$2" in c1|c2)
    { grep -q '"honoured": 1' "$d/WAVECAR.info" 2>/dev/null && [ -n "${3:-}" ] && [ "$(wsha "$d/WAVECAR.info" src_sha256)" = "$3" ] \
      && [ "$(wsha "$d/WAVECAR.info" copied_sha256)" = "$3" ] && [ "$(wsha "$d/WAVECAR.info" end_sha256)" = "$3" ] \
      && grep -aqE -e "$RESTART_RE" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null; } || { echo RESTART_NOT_HONOURED; return; };;
  esac
  j=$(judge5 "$d" "$2"); echo "${j%% *}"
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
'''

RUN_A5_CLI = r'''
# ── 0 스텝 인프라 중단 기록 (외주 2차 --infra-abort 와 같은 확인 · 단 이름만 a5) ──
if [ "${1:-}" = "--infra-abort" ]; then
  [ $# -ge 5 ] || { echo "⛔ 쓰는 법: [WALL_S=<초>] bash run_a5.sh --infra-abort <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유…>"; exit 2; }
  st=$2; sid=$(clean "$3"); when=$(clean "$4"); shift 4; why=$(clean "$*")
  case "$st" in A5|c1|c2) ;; *) echo "⛔ 모르는 단 $st"; exit 2;; esac
  src=run/${JOB}_$st
  [ -d "$src" ] || { echo "⛔ $src 가 없다"; exit 2; }
  if [ -e "$src/OSZICAR" ]; then
    n=$(grep -acE '^[[:space:]]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:' "$src/OSZICAR" 2>/dev/null); g=$?
    [ "$g" -le 1 ] && [ -n "$n" ] || { echo "⛔ $src/OSZICAR 를 읽지 못했다 (grep $g) — 0 행인지 확인할 수 없어 기록하지 않는다 (1저자)"; exit 2; }
    osz=zero_rows
  else
    n=0; osz=missing
  fi
  [ "$n" = 0 ] || { echo "⛔ 전자 반복행 $n 개 — 0 스텝 중단이 아니다 (실행 실패는 사다리가 다룬다)"; exit 2; }
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
  rm -f "$dst/POTCAR" "$dst/WAVECAR" "$dst/CHGCAR" "$dst/CHG" "$dst/vasprun.xml" "$dst/.running"     # WAVECAR 는 복사본이다 (보존 ⓐ 원본은 run/ 밖)
  if [ "$w" = ATTEMPT_JSON ]; then w=$(grep -o '"elapsed_s": [^,}]*[,}]' "$dst/attempt.json" | head -1 | sed 's/^"elapsed_s": //; s/[,}]$//'); secs_ok "$w" || w=UNKNOWN; fi
  printf '{"job": "%s", "rung": "%s", "sched_job_id": "%s", "cancel_utc": "%s", "reason": "%s", "wall_s": "%s", "oszicar": "%s", "recorded_utc": "%s"}\n' \
    "$JOB" "$st" "$sid" "$when" "$why" "$w" "$osz" "$(utc)" > "$dst/infra_abort.json"
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

# ── 전자 스텝 뒤 끊긴 시도의 벽시계 기록 (외주 2차 --killed 와 같은 확인 · 그 단 소모 · 값 없음) ──
if [ "${1:-}" = "--killed" ]; then
  [ $# -ge 5 ] || { echo "⛔ 쓰는 법: WALL_S=<초> bash run_a5.sh --killed <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유…>"; exit 2; }
  st=$2; sid=$(clean "$3"); when=$(clean "$4"); shift 4; why=$(clean "$*")
  case "$st" in A5|c1|c2) ;; *) echo "⛔ 모르는 단 $st"; exit 2;; esac
  src=run/${JOB}_$st
  [ -f "$src/attempt.start" ] || { echo "⛔ $src 에 시작 표지 (attempt.start) 가 없다 — VASP 가 뜨지 않은 시도다"; exit 2; }
  [ ! -f "$src/attempt.json" ] || { echo "⛔ $src 는 끝난 시도다 (attempt.json 있음) — 기록하지 않는다"; exit 2; }
  [ ! -f "$src/killed.json" ] || { echo "⛔ $src 는 이미 기록했다 — 고치지 않는다"; exit 2; }
  secs_ok "${WALL_S:-}" || { echo "⛔ WALL_S=<초> (스케줄러 장부의 그 시도 벽시계) 가 있어야 한다"; exit 2; }
  n=$(grep -acE '^[[:space:]]*[A-Za-z][A-Za-z ]?[A-Za-z ]?[A-Za-z ]?:' "$src/OSZICAR" 2>/dev/null); oi=$(grep -acE 'Iteration +[0-9]+\(' "$src/OUTCAR" 2>/dev/null)
  [ "${n:-0}" != 0 ] || [ "${oi:-0}" != 0 ] || { echo "⛔ $src 에 전자 반복 흔적이 없다 — 0 스텝 중단이면 --infra-abort 로 기록한다 (같은 단을 다시 돈다)"; exit 2; }
  [ -n "$sid" ] && [ -n "$when" ] && [ -n "$why" ] || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유가 다 있어야 한다"; exit 2; }
  rid=$(grep -o '"run_id": "[^"]*"' "$src/attempt.start" | head -1 | sed 's/.*: "//; s/"$//')
  printf '{"job": "%s", "rung": "%s", "run_id": "%s", "wall_s": "%s", "sched_job_id": "%s", "cancel_utc": "%s", "reason": "%s", "osz_rows": "%s", "recorded_utc": "%s"}\n' \
    "$JOB" "$st" "$rid" "$WALL_S" "$sid" "$when" "$why" "${n:-0}" "$(utc)" > "$src/killed.json.part" && mv -f "$src/killed.json.part" "$src/killed.json" \
    || { echo "⛔ killed.json 쓰기 실패"; exit 2; }
  log "✎ $src 끊긴 시도 벽시계 $WALL_S 초 (스케줄러 $sid · $why) — 그 단 소모 · 값 없음 · 다시 돌리지 않는다"
  echo "✓ $src 벽시계 $WALL_S 초 기록 — 다시 돌리면 다음 단부터 이어 간다"; exit 0
fi

@PACK_ONLY@

if ! mkdir run/.a5.lock 2>/dev/null; then
  if lock_live; then echo "⛔ 다른 run_a5.sh (PID $(cat run/.a5.lock/pid 2>/dev/null)) 가 이 묶음에서 돌고 있다 — 두 번 띄우지 않는다"; exit 2; fi
  echo "⚠ 남은 잠금 (PID $(cat run/.a5.lock/pid 2>/dev/null || echo ?) 가 살아 있지 않다) — 치우고 진행"; rm -rf run/.a5.lock
  mkdir run/.a5.lock 2>/dev/null || { echo "⛔ 잠금 (run/.a5.lock) 을 만들 수 없다 — 다른 실행이 막 시작했을 수 있다"; exit 2; }
fi
echo $$ > run/.a5.lock/pid; trap 'rm -rf run/.a5.lock' EXIT
[[ "$(up)" =~ ^[0-9]+$ ]] || { echo "⛔ /proc/uptime 을 읽을 수 없다 — 벽시계 장부는 단조 시계로 잰다 (Linux)"; exit 2; }
: "${VASP_CMD:?VASP_CMD 를 주세요 (예: mpirun -np 64 vasp_std)}"
: "${POTCAR_DIR:?POTCAR_DIR 를 주세요 (PAW_PBE 폴더)}"
: "${W0_WAVECAR:?W0_WAVECAR 를 주세요 — 보존된 a4 ⓐ WAVECAR 경로 (외주 2차 묶음의 @W0_REL@) · 없으면 W0_WAVECAR=none}"
PERF_LINES=""
@PERF@
{ echo "date_utc $(utc)"; echo "host $(hostname 2>/dev/null)"; echo "VASP_CMD $VASP_CMD"; echo "POTCAR_DIR $POTCAR_DIR"; echo "W0_WAVECAR $W0_WAVECAR"
  echo "PERF_TAGS $(printf '%s' "$PERF_LINES" | tr '\n' ';')"; echo "MANIFEST_sha256 $(h MANIFEST.sha256)"; } >> run/env.txt
[ -f run/status.tsv ] || printf "job\trung\tstage\trc\tstatus\tn_elec\tdE\tdeps\twhy\twall_s\n" > run/status.tsv
'''

RUN_A5_BODY = r'''
# ── 누적 벽시계 (a5 의 모든 시도 · 0 스텝 중단 · 끊긴 시도 · 미상은 0 초가 아니다) ──
wall5(){ local d w tot=0 unk="" dirs=run lst
  [ -d run_aborted ] && dirs="run run_aborted"
  lst=$(find $dirs \( -name attempt.json -o -name attempt.start -o -name infra_abort.json -o -name killed.json \) -type f 2>/dev/null) || { echo "UNKNOWN (반송 폴더 열거 실패)"; return; }
  for d in $(printf '%s\n' "$lst" | sed 's#/[^/]*$##' | LC_ALL=C sort -u); do
    if [ -f "$d/attempt.json" ]; then w=$(grep -o '"elapsed_s": [^,}]*[,}]' "$d/attempt.json" | head -1 | sed 's/^"elapsed_s": //; s/[,}]$//')
    elif [ -f "$d/infra_abort.json" ]; then w=$(grep -o '"wall_s": "[^"]*"' "$d/infra_abort.json" | head -1 | sed 's/.*: "//; s/"$//')
    elif [ -f "$d/killed.json" ]; then w=$(grep -o '"wall_s": "[^"]*"' "$d/killed.json" | head -1 | sed 's/.*: "//; s/"$//')
    else w=""; fi
    if [[ "$w" =~ ^(0|[1-9][0-9]{0,11})$ ]]; then tot=$((tot + w)); else [ -n "$unk" ] || unk=$d; fi
  done
  if [ -n "$unk" ]; then echo "UNKNOWN $unk"; else echo "$tot"; fi
}
cap_ok(){ # → 0 이면 다음 단을 띄워도 된다 (누적 ≤ 상한 · 벽시계 미상이면 안 띄운다)
  local w; w=$(wall5) || w="UNKNOWN (장부 계산 실패)"
  case "$w" in UNKNOWN*) log "⏸ 벽시계 미상 — ${w#UNKNOWN } · 다음 단을 띄우지 않는다. 0 스텝 중단이면 'bash run_a5.sh --infra-wall <폴더> <초>' · 끊긴 시도면 'WALL_S=<초> bash run_a5.sh --killed <단> …' 로 채운 뒤 다시"; return 1;; esac
  [[ "$w" =~ ^[0-9]+$ ]] || { log "⏸ 벽시계 장부가 숫자가 아니다 ('$w') — 다음 단을 띄우지 않는다 (반송하고 연락)"; return 1; }
  awk -v w="$w" -v c="$CAP_H" 'BEGIN { exit !(w <= c * 3600) }' || { log "⏸ a5 누적 $((w / 3600)) h > 상한 $CAP_H h — 다음 단을 띄우지 않는다 (1저자)"; return 1; }
  return 0
}

# ── ⓪ 보존된 a4 ⓐ WAVECAR 확인 (한 번 · 원본은 읽기만) ──
w0_check(){
  local p=$W0_WAVECAR s="" z="" hd="" v=0 why=""
  if [ -f run/w0_check.json ]; then
    [ "$(grep -o '"path": "[^"]*"' run/w0_check.json | head -1 | sed 's/.*: "//; s/"$//')" = "$(clean "$p")" ] \
      || { echo "⛔ W0_WAVECAR '$p' 가 첫 기록 (run/w0_check.json) 과 다르다 — 같은 경로로 다시 돌린다"; exit 2; }
    return 0
  fi
  if [ "$p" = none ]; then why="업체가 없다고 적음 (W0_WAVECAR=none)"
  elif [ -f "$p" ] && [ -r "$p" ]; then
    s=$(h "$p"); z=$(stat -c %s "$p" 2>/dev/null); hd=$(wav_head "$p"); set -- $hd
    if [ "$s" != "$W0_SHA" ]; then why="sha256 다름"
    elif [ "$z" != "$W0_SIZE" ]; then why="크기 다름"
    elif ! { [ $# -ge 6 ] && [ "$4" = "$W0_NK" ] && [ "$5" = "$W0_NB" ] && enc_eq "$6" "$W0_EN"; }; then why="머리 (NKPTS·NBANDS·ENCUT) 다름"
    else v=1; why="-"; fi
  else why="파일이 없거나 읽을 수 없다"; fi
  printf '{"path": "%s", "sha256": "%s", "size": "%s", "head": "%s", "expect": {"sha256": "%s", "size": "%s", "NKPTS": "%s", "NBANDS": "%s", "ENCUT": "%s"}, "verified": %d, "why": "%s", "checked_utc": "%s"}\n' \
    "$(clean "$p")" "$s" "$z" "$hd" "$W0_SHA" "$W0_SIZE" "$W0_NK" "$W0_NB" "$W0_EN" "$v" "$why" "$(utc)" > run/w0_check.json.part && mv -f run/w0_check.json.part run/w0_check.json \
    || { echo "⛔ run/w0_check.json 쓰기 실패"; exit 2; }
  log "⓪ 보존 ⓐ WAVECAR $( [ "$v" = 1 ] && echo '확인됨 — A5 는 그 복사본에서 이어서' || echo "확인 안 됨 ($why) — A5 는 새로 시작")"
}

# ── 한 시도 (외주 2차 run_one 과 같은 기록 꼴 · 단 이름 · 시작 WAVECAR 대조만 a5) ──
run_one5(){ # $1 단 (A5|c1|c2) · $2 변형 (A5c|A5f|c1|c2) · $3 시도 폴더 · $4 시작 WAVECAR (A5c · c1 · c2) · $5 그 기대 sha → 0 돌림 · 3 준비 실패 · 6 공통 환경 고장
  local st=$1 var=$2 d=$3 wsrc=${4:-} wexp=${5:-} inc rid t0 t1 u0 u1 el rc j wsha="" wcp="" wend hd istart icharg nr pr hon ver rs x
  inc=$(incar_of "$var")
  pp_ok "$JOB" || return 6
  mkdir "$d" 2>/dev/null || { echo "⛔ $d 가 이미 있거나 만들 수 없다 — 덮어쓰지 않는다"; return 3; }
  { cp "jobs/$JOB/POSCAR" "jobs/$JOB/KPOINTS" "$d/" && cp "jobs/$JOB/$inc" "$d/INCAR"; } || return 3
  [ -n "$PERF_LINES" ] && printf '%s' "$PERF_LINES" >> "$d/INCAR"
  : > "$d/POTCAR"; : > "$d/POTCAR.species.sha256"
  while read -r p; do
    [ -n "$p" ] || continue
    [ -f "$POTCAR_DIR/$p/POTCAR" ] || { echo "⛔ POTCAR $p 없음"; rm -f "$d/POTCAR"; return 3; }
    cat "$POTCAR_DIR/$p/POTCAR" >> "$d/POTCAR"; printf "%s %s\n" "$p" "$(h "$POTCAR_DIR/$p/POTCAR")" >> "$d/POTCAR.species.sha256"
  done < "jobs/$JOB/POTCAR.spec"
  grep -aE "TITEL|ZVAL|VRHFIN|LEXCH" "$d/POTCAR" > "$d/POTCAR.titel"; h "$d/POTCAR" > "$d/POTCAR.sha256"
  if [ -n "$wsrc" ]; then
    wsha=$(h "$wsrc")
    [ -n "$wexp" ] && [ "$wsha" = "$wexp" ] || { log "⛔ $st 시작 WAVECAR sha '$wsha' ≠ 기대 '$wexp' — 띄우지 않는다"; return 3; }
    cp "$wsrc" "$d/WAVECAR" || return 3
    wcp=$(h "$d/WAVECAR")
    [ "$wcp" = "$wexp" ] || { log "⛔ $st 복사한 WAVECAR sha 가 원본과 다르다 — 띄우지 않는다"; rm -f "$d/WAVECAR"; return 3; }
  fi
  rid="$(date -u +%Y%m%dT%H%M%S)-$$-$RANDOM"; t0=$(date +%s); u0=$(up)
  printf '{"job": "%s", "attempt": "%s", "stage": "a5", "run_id": "%s", "t_start": %d, "kernel_sha256": ""}\n' "$JOB" "$var" "$rid" "$t0" > "$d/attempt.start" || return 3
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
      printf '{"src_sha256": "%s", "copied_sha256": "%s", "end_sha256": "%s", "istart": "%s", "icharg": "%s", "not_read_phrase": %s, "positive_regex_match": "%s", "honoured": %s}\n' \
        "$wsha" "$wcp" "$wend" "${istart:-NA}" "${icharg:-NA}" "$nr" "$pr" "$hon" > "$d/WAVECAR.info";;
  esac
  if [ "$st" != c2 ]; then x=$(hist_max "$d"); case "$x" in ''|*[!0-9]*) ;; *) [ "$x" -gt 45 ] && echo "$(utc) $var info history_max $x" >> "$d/warn.log";; esac; fi
  printf '{"job": "%s", "attempt": "%s", "stage": "a5", "run_id": "%s", "rc": %d, "t_start": %d, "t_end": %d, "elapsed_s": %d, "vasp_version": "%s", "kernel_sha256": "", "perf": "%s", "sha256": {"INCAR": "%s", "POSCAR": "%s", "KPOINTS": "%s", "POTCAR": "%s", "OUTCAR": "%s", "OSZICAR": "%s", "WAVECAR.info": "%s", "stdout.log": "%s", "POTCAR.titel": "%s", "POTCAR.species.sha256": "%s", "attempt.start": "%s"}}\n' \
    "$JOB" "$var" "$rid" "$rc" "$t0" "$t1" "$el" "$ver" "$(printf '%s' "$PERF_LINES" | tr '\n' ';')" \
    "$(h "$d/INCAR")" "$(h "$d/POSCAR")" "$(h "$d/KPOINTS")" "$(cat "$d/POTCAR.sha256")" "$(h "$d/OUTCAR")" "$(h "$d/OSZICAR")" "$(h "$d/WAVECAR.info")" \
    "$(h "$d/stdout.log")" "$(h "$d/POTCAR.titel")" "$(h "$d/POTCAR.species.sha256")" "$(h "$d/attempt.start")" > "$d/attempt.json"
  j=$(judge5 "$d" "$st"); set -- $j
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$JOB" "$var" "a5" "$rc" "$1" "$2" "$3" "$4" "$5" "$el" >> run/status.tsv
  rm -f "$d/POTCAR" "$d/CHGCAR" "$d/CHG" "$d/vasprun.xml" "$d/vdw_kernel.bindat" "$d/LOCPOT"
  [ "$st" = A5 ] || rm -f "$d/WAVECAR"          # c1 · c2 의 WAVECAR 는 복사본 (끝 sha 를 잰 뒤 지운다) · A5 WAVECAR 는 잡이 끝날 때까지 둔다 (반송 안 함)
  if [ -n "$ver" ] && [ "$ver" != "$REL_VER" ]; then log "⛔ $var VASP 빌드 '$ver' ≠ 봉인 — 공통 환경 고장 · 전체 정지"; return 6; fi
  return 0
}
done5(){ [ -f "$1/attempt.json" ] || [ -f "$1/killed.json" ]; }      # 끝난 시도 (값이 있든 없든 그 단을 소모했다)
drop5(){ # $1 마지막 상태 — A5 WAVECAR 는 잡이 **끝난** 상태에서만 지운다 (검토·이어 돌리기용 상태면 남긴다 · 반송은 안 한다)
  case "$1" in INCOMPLETE_ATTEMPT|RESTART_NOT_HONOURED|SCF_UNVERIFIED|PREP_FAILED) log "… run/${JOB}_A5/WAVECAR 를 남긴다 ($1 — 검토·이어 돌리기용)";;
    *) rm -f "run/${JOB}_A5/WAVECAR";; esac
}
stage_gate(){ # $1 시도 폴더 · $2 단 → 0 이면 이미 끝난 시도 (다시 안 띄움) · 1 이면 새로 띄울 차례 · 그 밖은 멈춤 (끝 코드 출력)
  local d=$1
  [ -d "$d" ] || return 1
  done5 "$d" && return 0
  if [ -f "$d/attempt.start" ]; then log "⏸ $2 는 시작했는데 끝 기록이 없다 (끊김) — 'WALL_S=<초> bash run_a5.sh --killed $2 <스케줄러 잡 id> <취소 UTC> <사유>' 로 기록한 뒤 다시 (0 스텝이면 --infra-abort)"; finish 5; fi
  log "✗ $2 폴더는 있는데 VASP 를 띄운 흔적이 없다 (준비 실패) — 반송하고 연락"; drop5 PREP_FAILED; finish 1
}

# ── 사다리 ──
log "════ W_ad a5 · $JOB ════"
w0_check
W0OK=0; grep -q '"verified": 1' run/w0_check.json && W0OK=1
A=run/${JOB}_A5; C1=run/${JOB}_c1; C2=run/${JOB}_c2
if ! stage_gate "$A" A5; then
  cap_ok || finish 5
  if [ "$W0OK" = 1 ]; then var=A5c; ws=$W0_WAVECAR; we=$W0_SHA; else var=A5f; ws=""; we=""; fi
  log "▶ A5 ($var · LDIPOL 끔 · MAXMIX 200)"
  run_one5 A5 "$var" "$A" "$ws" "$we"; r=$?
  [ "$r" = 6 ] && finish 6
  [ "$r" = 0 ] || { log "✗ A5 준비 실패 — 반송하고 연락"; finish 1; }
fi
if why=$(elig5 "$A"); then S=$A/WAVECAR; SS=$(wsha "$A/WAVECAR.info" sha256); START=A5
elif [ "$W0OK" = 1 ]; then S=$W0_WAVECAR; SS=$W0_SHA; START=W0; log "A5 자격 미달 — $why · c1 · c2 시작점 = 보존 ⓐ (복사본)"
else log "✗ A5 자격 미달 — $why · 보존 ⓐ 도 확인 안 됨 → 값 없음 (이 잡은 닫는다)"; drop5 STAGE_A_INELIGIBLE; finish 1; fi
log "시작점 $START (sha $SS)"
if ! stage_gate "$C1" c1; then
  cap_ok || finish 5
  log "▶ c1 (Davidson · MAXMIX 200 · AMIX 0.1 · AMIN 0.01 · NELM 400 · 시작점 $START)"
  run_one5 c1 c1 "$C1" "$S" "$SS"; r=$?
  [ "$r" = 6 ] && finish 6
  [ "$r" = 0 ] || { log "✗ c1 준비 실패 — 반송하고 연락"; drop5 PREP_FAILED; finish 1; }
fi
s1=$(stat5 "$C1" c1 "$SS"); log "c1 → $s1"
if [ "$s1" = OK ]; then drop5 OK; log "✓ c1 주 기준 수렴 — c2 를 띄우지 않는다"; finish 0; fi
if ! stage_gate "$C2" c2; then
  cap_ok || finish 5
  log "▶ c2 (ALGO All · TIME 0.1 · NELM 400 · c1 = $s1 · 시작점 $START 의 새 복사본)"
  run_one5 c2 c2 "$C2" "$S" "$SS"; r=$?
  [ "$r" = 6 ] && finish 6
  [ "$r" = 0 ] || { log "✗ c2 준비 실패 — 반송하고 연락"; drop5 PREP_FAILED; finish 1; }
fi
s2=$(stat5 "$C2" c2 "$SS"); log "c2 → $s2"
drop5 "$s2"
[ "$s2" = OK ] && finish 0
finish 1
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
            "status": "a5 묶음 v1 — 개정 5 v2 비준 뒤 · 발송 전 독립 리뷰 대기",
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


def _readme(meta, msha):
    return f"""# W_ad a5 — 은 쪽 G4 ENCUT 650 분리 끝점 재시도 (개정 5 v2)

- 묶음 MANIFEST sha256: `{msha}` (받은 뒤 `sha256sum MANIFEST.sha256` 로 같은지 확인)
- 잡: `{JOB}` 하나 · 사다리 {meta['ladder']}
- 누적 상한 {CAP_H:g} h (넘으면 다음 단을 띄우지 않고 멈춘다) · 0 스텝 인프라 중단은 잡 전체 {INFRA_MAX} 회

## 돌리는 법
```
W0_WAVECAR=<외주 2차 묶음>/{W0_REL} \\
VASP_CMD="mpirun -np 64 vasp_std" POTCAR_DIR=<PAW_PBE 폴더> [PERF_TAGS_FILE=<성능 태그 파일>] bash run_a5.sh
```
- 보존된 a4 ⓐ WAVECAR 가 없으면 `W0_WAVECAR=none` 을 적는다 (A5 가 새로 시작한다). 원본은 읽기만 한다 (복사본만 쓴다).
- 다 끝나면 `a5_return.tgz` 와 `a5_return.tgz.sha256` 을 보낸다 (`sha256sum -c a5_return.tgz.sha256` 통과 뒤). WAVECAR · CHGCAR · POTCAR 본문은 담지 않는다.
- 종료 0 c1 또는 c2 수렴 · 1 주 기준 값 없음 (그대로 반송 — 실패도 기록) · 2 인자·패키지 오류 · 4 포장 실패 (`PACK_ONLY=1 bash run_a5.sh`) · 5 누적 상한 · 벽시계 미상 · 6 공통 환경 고장
- 0 스텝 인프라 중단: `bash run_a5.sh --infra-abort <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유>` · 끊긴 시도: `WALL_S=<초> bash run_a5.sh --killed <단> <id> <UTC> <사유>`
- INCAR · POSCAR · KPOINTS 를 고치지 마세요. 시도 폴더가 있으면 덮어쓰지 않습니다 (다시 돌리면 기록을 다시 판정해 다음 단을 정합니다).
"""


# ───────────────────────── 반송 검사 (시도 하나) ─────────────────────────
def _wavecar_info(attdir):
    wi = R2._read(os.path.join(attdir, "WAVECAR.info"))
    try:
        w = json.loads(wi) if wi else None
    except ValueError:
        w = None
    return w if isinstance(w, dict) else None


def audit5(o, job, var):
    """OUTCAR 해석값 (입력 에코 제외) 대조 → (없는 키, 모순 목록, 근거). 외주 2차 audit_r2 와 같은 규칙 (NIONS · NELECT · ENCUT · 점유 · D3 · GGA · DIPOL ·
    EFIELD) + a5 단마다 NELM · IALGO · AMIX · AMIN · MAXMIX (A5 · c1) · TIME (c2). A5 는 퍼텐셜 보정을 끈 단이라 DIPOL 근거가 없어도 된다."""
    s, text = o["settings"], o.get("_body", "")
    st = STAGE_OF_VAR[var]
    exp = {"NIONS": job["nions"], "NELECT": job["nelect_expected"], "ENCUT": job["encut"], "ISMEAR": job["ismear"], "SIGMA": job["sigma"],
           "ISPIN": 1, "LDIPOL": "F" if st == "A5" else "T", "IDIPOL": 3, "IVDW": 12, "VDW_S6": V.D3_PARAMS["s6"], "VDW_S8": V.D3_PARAMS["s8"],
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
    nelm = V._tok_float(V._last(r"^\s*NELM\s*=\s*(\d+)", text))
    if nelm is None:
        missing.append("NELM")
    elif int(nelm) != NELM[var]:
        bad.append(f"NELM {int(nelm)} ≠ {NELM[var]}")
    ex = ECHO_EXPECT[var]
    got = {"IALGO": V._tok_float(V._last(r"^\s*IALGO\s*=\s*(\d+)", text)),
           "AMIX": V._tok_float((V._last(r"^\s*AMIX\s*=\s*([^;\s]+)\s*;\s*BMIX", text) or "").rstrip(";")),
           "AMIN": V._tok_float(V._last(r"^\s*AMIN\s*=\s*(\S+)", text)),
           "MAXMIX": V._tok_float(V._last(r"MAXMIX\s*=\s*(-?\d+)", text)),
           "TIME": V._tok_float(V._last(r"^\s*TIME\s*=\s*(\S+)", text))}
    tol = {"IALGO": 0, "MAXMIX": 0, "AMIX": 1e-3, "AMIN": 1e-4, "TIME": 1e-3}
    for k, e in ex.items():
        v = got[k]
        if v is None:
            missing.append(k)
        elif abs(v - e) > tol[k] + 1e-12:
            bad.append(f"{k} {v:g} ≠ {e:g}")
    dg, dbad = V.dipol_evidence(o, job["dipol_z"])
    bad += dbad
    if not dg and not dbad and st != "A5":
        missing.append("DIPOL")
    if s.get("EFIELD") is not None and abs(s["EFIELD"]) > 1e-12:
        bad.append(f"EFIELD {s['EFIELD']} (외부장 금지)")
    return missing, bad, {"DIPOL": dg, "echo": got}


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


def check_attempt5(job, pkgdir, attdir, stage, registry=None, src_sha=None):
    """a5 시도 하나 → 상태 dict (외주 2차 check_attempt 순서: 실행 기록 결박 → 입력 무결성 → 있는 증거의 모순 → 판정 → 재시작 → 완결성).
    c1 · c2 는 src_sha (그 시도가 읽어야 할 시작 WAVECAR sha — A5 끝 WAVECAR 또는 ⓪) 를 꼭 받는다. A5 의 재시작은 정보 (자격이 아니다)."""
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
    if not os.path.isfile(os.path.join(attdir, "attempt.json")):
        return done("INCOMPLETE_ATTEMPT", "attempt.json 없음 — " + (
            "전자 스텝 뒤 끊긴 시도 (killed.json — 그 단 소모 · 값 없음)" if r["killed"] else
            "VASP 를 띄웠는데 끝 기록이 없다 (attempt.start 만 — 벽시계 미상)" if r["started"] else "VASP 를 띄우기 전에 멈춘 시도 (준비 실패)"))
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
    missing, bad, src = audit5(o, job, var) if o else ([], [], {})
    if bad:
        conflicts.append(("SETTINGS_MISMATCH", "; ".join(bad)))
    ref = fin(job.get("d3_2body_eV_ref"))
    if o and ref is not None and o["Edisp_eV"] is not None and abs(o["Edisp_eV"] - ref) > V.D3_REL_TOL * abs(ref):
        conflicts.append(("D3_MISMATCH", f"Edisp {o['Edisp_eV']:.4f} vs ref {ref:.4f} eV (>1 %)"))
    osz = R2._read_raw(os.path.join(attdir, "OSZICAR"))
    if stage != "c2":
        r["history_max"] = hist_max(out_text)
        r["rmsc_jump_steps"] = rms_jumps(osz, stage)[:20]
    if stage != "A5":
        r["far"] = R2.far_diag(out_text, job["area_A2"])
    if conflicts:
        return done(conflicts[0][0], conflicts[0][1], conflicts=[f"{s_}: {w}" for s_, w in conflicts])
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
    else:
        r["restart"] = {"record": w, "outcar_istart": ev["istart"], "outcar_icharg": ev["icharg"], "not_read_phrase": ev["not_read_phrase"],
                        "expected_src_sha256": src_sha, "positive_regex": rx or None, "positive_regex_match": pos}
        if not (isinstance(w, dict) and w.get("honoured") == 1 and w.get("istart") == "1" and w.get("icharg") == "0" and w.get("not_read_phrase") == 0
                and ev["istart"] == "1" and ev["icharg"] == "0" and not ev["not_read_phrase"]
                and V.HEX64.match(str(w.get("src_sha256", ""))) and w.get("src_sha256") == w.get("copied_sha256") == w.get("end_sha256")):
            return done("RESTART_NOT_HONOURED", f"{stage} 가 시작 WAVECAR 를 읽었다고 확인할 수 없다 (OUTCAR ISTART {ev['istart']} · ICHARG {ev['icharg']} · "
                        f"'WAVECAR not read' {ev['not_read_phrase']} · sha 셋) — 자동 채택 없음 · 1저자 검토")
        if not (src_sha and V.HEX64.match(src_sha) and w.get("src_sha256") == src_sha):
            return done("RESTART_NOT_HONOURED", f"{stage} 원본이 정해진 시작 WAVECAR 가 아니다 (기대 {src_sha or '없음'} · 기록 {w.get('src_sha256')}) — 자동 채택 없음 · 1저자 검토")
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


def a5_aborted(job, pkgdir, ret, registry, src_sha):
    """run_aborted/<잡>_<단>_<k> → [(꼬리표, 검사 기록)] — 환경 감사에만 쓴다 (값에는 안 쓴다 · 외주 2차 aborted_attempts 와 같은 쓰임)."""
    base = ret if os.path.isdir(os.path.join(ret, "run")) else os.path.dirname(os.path.abspath(ret))
    ab, found = os.path.join(base, "run_aborted"), []
    try:
        names = sorted(os.listdir(ab))
    except FileNotFoundError:
        names = []
    except OSError as e:
        return [("run_aborted", R2._unreadable(ab, "-", e))]
    for name in names:
        m, d = AB_RE.match(name), os.path.join(ab, name)
        if m and m.group(1) == job["dir"]:
            try:
                R2._started(d)
                if os.path.isdir(d):
                    found.append((f"{m.group(2)}@aborted{m.group(3)}", check_attempt5(job, pkgdir, d, m.group(2), registry, src_sha.get(m.group(2)))))
            except OSError as e:
                found.append((f"{m.group(2)}@aborted{m.group(3)}", R2._unreadable(d, m.group(2), e)))
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


def check_return(out, ret, manifest_sha256, registry=None):
    """반송 트리 → a5 결과 (시도별 상태 · ⓪ · 시작점 · 사다리 대조 · 환경 감사). 채택은 하지 않는다 (V5 수집기 adopt_a5)."""
    V.verify_manifest(out, manifest_sha256)
    meta = json.load(open(os.path.join(out, "jobs.json"), encoding="utf-8"))
    if meta.get("schema") != SCHEMA_PKG:
        raise PkgError(f"묶음 schema {meta.get('schema')!r}")
    job = meta["jobs"][0]
    run = os.path.join(ret, "run") if os.path.isdir(os.path.join(ret, "run")) else ret
    P = lambda s: os.path.join(run, f"{job['dir']}_{s}")
    w0 = check_w0(run, meta)
    W0S = meta["w0"]["sha256"]
    A = check_attempt5(job, out, P("A5"), "A5", registry, W0S if w0.get("verified") else None)
    if A["status"] in ("MISSING", "INCOMPLETE_ATTEMPT"):
        a_ok, a_why = False, f"A5 {A['status']}"
    else:
        a_ok, a_why = R2.a_eligible(A)
    a_sha = str((A.get("wavecar") or {}).get("sha256") or "")
    start = {"from": "A5", "sha256": a_sha} if a_ok and V.HEX64.match(a_sha) else ({"from": "W0", "sha256": W0S} if w0.get("verified") else None)
    ss = (start or {}).get("sha256")
    C1 = check_attempt5(job, out, P("c1"), "c1", registry, ss)
    C2 = check_attempt5(job, out, P("c2"), "c2", registry, ss)
    att = {"A5": A, "c1": C1, "c2": C2}
    viol = []
    if A["status"] != "MISSING" and A.get("variant") and A["variant"] != ("A5c" if w0.get("verified") else "A5f"):
        viol.append(f"A5 변형 {A['variant']} ≠ ⓪ 판정에 맞는 변형 ({'A5c' if w0.get('verified') else 'A5f'})")
    a_done = A["status"] not in ("MISSING",) and (A["status"] != "INCOMPLETE_ATTEMPT" or A.get("killed"))
    for nm, x in (("c1", C1), ("c2", C2)):
        if x["status"] != "MISSING" and not a_done:
            viol.append(f"{nm} 가 있는데 A5 가 끝나지 않았다")
        if x["status"] != "MISSING" and start is None:
            viol.append(f"{nm} 가 있는데 시작점이 없다 (A5 자격 미달 · ⓪ 미확인)")
    c1_done = C1["status"] != "MISSING" and (C1["status"] != "INCOMPLETE_ATTEMPT" or C1.get("killed"))
    if C2["status"] != "MISSING" and (C1["status"] == "OK" or not c1_done):
        viol.append(f"c2 가 있는데 c1 이 {C1['status']}{'' if c1_done else ' (끝나지 않음)'} — c2 는 c1 이 끝났고 주 기준 OK 가 아닐 때만")
    aborted = a5_aborted(job, out, ret, registry, {"A5": W0S if w0.get("verified") else None, "c1": ss, "c2": ss})
    unreg = a5_unregistered(job, ret)
    env = R2.env_audit([(k, v) for k, v in att.items() if v["status"] != "MISSING"] + aborted, registry)
    res = {"status": None, "w0": w0, "a5_eligible": [a_ok, a_why], "start_point": start, "attempts": att, "ladder_violations": viol,
           "aborted": [[t, x.get("status")] for t, x in aborted], "unregistered": [list(u) for u in unreg], "env_in": [list(e) for e in env]}
    blk = [(k, v["status"]) for k, v in att.items() if v["status"] in BLOCKING]
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
    elif "OK" in (C1["status"], C2["status"]):
        res.update(status="OK", why=f"주 기준 수렴 ({'c1' if C1['status'] == 'OK' else 'c2'})")
    else:
        res.update(status="NO_PRIMARY_VALUE", why=f"c1 {C1['status']} · c2 {C2['status']} — 보조 기준은 V5 수집기가 본다")
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
if beh in ("conv", "sda_rows", "dav_rows", "unknown_hdr", "noread", "istart0", "modwav", "badhead", "badecho", "nowav", "nophrase"):
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
Ed = j["d3_2body_eV_ref"]
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
    ck(_bash_ok(txt) and "judge_r2(){" in txt and 'osz_feed "$d" |' in txt and "a5_return" in txt and "round2_return" not in txt and "run/w0_check.json" in txt,
       "러너 = 2차 부품 (판정 · 포장 · 자격) + a5 · bash -n 통과 · 반송 이름 a5_return · ⓪ 기록 포장")
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

        def run_pkg(name, plan, w0path=None, env_extra=None, args=(), fresh=True, pk=None):
            w = os.path.join(T, "w_" + name)
            if fresh:
                shutil.copytree(pk or pkg, w)
            pf = os.path.join(T, f"plan_{name}.json"); _write(pf, json.dumps(plan))
            env = {**os.environ, "VASP_CMD": f"{py} {fake}", "POTCAR_DIR": potd, "W0_WAVECAR": w0path if w0path is not None else w0p,
                   "FAKE_PLAN": pf, "FAKE_PKG": w, "WATCH_S": "1", **(env_extra or {})}
            p = subprocess.run(["bash", os.path.join(w, "run_a5.sh"), *args], cwd=w, env=env, capture_output=True, text=True, timeout=600)
            return w, p.returncode, p.stdout + p.stderr

        def chk(w, pk=None, ms=None):
            ex = os.path.join(T, "ex_" + os.path.basename(w)); shutil.rmtree(ex, ignore_errors=True); os.makedirs(ex)
            with tarfile.open(os.path.join(w, "a5_return.tgz")) as tf:
                try:
                    tf.extractall(ex, filter="data")
                except TypeError:
                    tf.extractall(ex)
            return check_return(pk or pkg, ex, ms or msha, reg)[1], ex

        def stat_rows(w):
            return [ln.split("\t") for ln in open(os.path.join(w, "run", "status.tsv")).read().splitlines()[1:]]
        # S1: ⓪ 확인 → A5c → c1 수렴 → c2 안 띄움
        w1, rc1, log1 = run_pkg("s1", {"A5": "conv", "c1": "conv"})
        r1, ex1 = chk(w1)
        ck(rc1 == 0 and not os.path.isdir(os.path.join(w1, "run", f"{JOB}_c2")) and r1["status"] == "OK" and r1["attempts"]["c1"]["status"] == "OK"
           and r1["attempts"]["A5"]["variant"] == "A5c" and r1["start_point"]["from"] == "A5", f"S1 ⓪→A5c→c1 수렴 · c2 안 띄움 — rc {rc1} · {r1['status']} {r1.get('why')}")
        ck(r1["attempts"]["A5"]["restart_start"]["honoured"] is True and r1["attempts"]["A5"]["wavecar"]["sha256"] != w0["sha256"],
           "A5 끝 WAVECAR 는 새로 써져 sha 가 달라도 재시작 미이행으로 읽지 않는다 (시작 복사본 sha + 문구만)")
        ck(_sha(w0p) == w0["sha256"] and os.stat(w0p).st_mtime_ns == w0_mtime, "보존 ⓐ 원본은 바뀌지 않았다 (sha · mtime)")
        with tarfile.open(os.path.join(w1, "a5_return.tgz")) as tf:
            mem = tf.getnames()
        ck("run/w0_check.json" in mem and not any(os.path.basename(m) in RETURN_FORBIDDEN for m in mem) and f"run/{JOB}_c1/WAVECAR.info" in mem,
           "반송 묶음: ⓪ 기록 포함 · WAVECAR · CHGCAR · POTCAR 본문 없음")
        ck(r1["attempts"]["c1"]["far"]["p_z_eA"] is not None and "far" not in r1["attempts"]["A5"], "정보: c1 far 진단 (dipolmoment · E-fermi) · A5 (쌍극 보정 끔) 에는 없음")
        # 사다리 대조: c1 OK 인데 c2 가 있으면 LADDER_VIOLATION
        shutil.copytree(os.path.join(ex1, "run", f"{JOB}_c1"), os.path.join(ex1, "run", f"{JOB}_c2"))
        ck(check_return(pkg, ex1, msha, reg)[1]["status"] == "LADDER_VIOLATION", "⛔음성 c1 OK 인데 반송에 c2 가 있다 → LADDER_VIOLATION")
        # S2: c1 정체 (400 스텝) → c2 자동 (SDA/CGA 수렴) · c2 시작 = 같은 A5 WAVECAR
        w2, rc2, log2 = run_pkg("s2", {"A5": "noconv", "c1": "plateau", "c2": "conv"})
        r2, _ = chk(w2)
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
        w4l = [ln for ln in open(os.path.join(w2, "run", f"{JOB}_c1", "warn.log")).read().splitlines()] if os.path.isfile(os.path.join(w2, "run", f"{JOB}_c1", "warn.log")) else []
        ck(any("history_max" in ln for ln in w4l), f"러너 warn.log 에 이력 길이 정보 한 줄 (정보 · 판정 아님) — {w4l[-2:]}")
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
        # S5b · S5c: 기대값만 다른 묶음 — sha 는 같은데 크기만 · 머리만 다르면 그 확인 하나가 잡는다 (sha 가 가리지 않게 따로 본다)
        for nm, w0x, why_ in (("s5b", {**w0, "size": w0["size"] + 1}, "크기 다름"), ("s5c", {**w0, "NBANDS": "871"}, "머리 (NKPTS·NBANDS·ENCUT) 다름")):
            pkx = os.path.join(T, f"pkg_{nm}"); _, msx = build(pkx, registry=(reg, "c" * 64), w0=w0x, check_decision=False)
            wx, rcx, _ = run_pkg(nm, {"A5": "conv", "c1": "conv"}, pk=pkx)
            rx_, _ = chk(wx, pk=pkx, ms=msx)
            ck(rx_["w0"]["verified"] is False and rx_["w0"]["record"]["why"] == why_ and rx_["attempts"]["A5"]["variant"] == "A5f" and rx_["w0"]["status"] == "OK",
               f"⛔음성 ⓪ sha 는 같고 {why_} → 확인 안 됨 (그 확인 하나가 잡는다) — {rx_['w0'].get('record', {}).get('why')}")
        # S6: A5 충돌 + ⓪ 확인 → c1 은 ⓪ 복사본에서
        w6, rc6, _ = run_pkg("s6", {"A5": "crash", "c1": "conv"})
        r6, _ = chk(w6)
        ck(rc6 == 0 and r6["start_point"]["from"] == "W0" and r6["attempts"]["c1"]["restart"]["record"]["src_sha256"] == w0["sha256"] and r6["status"] == "OK",
           f"⛔음성 A5 자격 미달 (충돌) + ⓪ 확인 → c1 · c2 는 ⓪ 복사본에서 — rc {rc6} · {r6['status']} {r6.get('why')}")
        # S7: A5 충돌 + ⓪ 없음 → 값 없음 · c1 안 띄움
        w7, rc7, _ = run_pkg("s7", {"A5": "crash"}, w0path="none")
        r7, _ = chk(w7)
        ck(rc7 == 1 and not os.path.isdir(os.path.join(w7, "run", f"{JOB}_c1")) and r7["start_point"] is None and r7["status"] == "NO_PRIMARY_VALUE",
           f"⛔음성 A5 자격 미달 + ⓪ 없음 → 값 없음 · c1 안 띄움 — rc {rc7} · {r7['status']}")
        # S8 · S9: c1 재시작 미이행 (문구 없음 · 끝 sha 다름) → c2 띄움 · 검사 RESTART_NOT_HONOURED
        for nm, beh_ in (("s8", "noread"), ("s9", "modwav"), ("s9b", "nophrase")):
            wx, rcx, _ = run_pkg(nm, {"A5": "conv", "c1": beh_, "c2": "conv"})
            rx_, _ = chk(wx)
            envx = open(os.path.join(wx, "run", "env.txt")).read()
            ck(rx_["attempts"]["c1"]["status"] == "RESTART_NOT_HONOURED" and "c1 → RESTART_NOT_HONOURED" in envx and os.path.isdir(os.path.join(wx, "run", f"{JOB}_c2"))
               and rx_["status"] == "OK" and json.load(open(os.path.join(wx, "run", f"{JOB}_c1", "WAVECAR.info")))["honoured"] == 0,
               f"⛔음성 c1 재시작 미이행 ({beh_}) → 러너 · 검사기 둘 다 RESTART_NOT_HONOURED · c2 띄움 — {rx_['attempts']['c1'].get('why', '')[:80]}")
        w9c, rc9c, _ = run_pkg("s9c", {"A5": "conv", "c1": "plateau", "c2": "modwav"})
        r9c, _ = chk(w9c)
        ck(rc9c == 1 and r9c["attempts"]["c2"]["status"] == "RESTART_NOT_HONOURED" and "c2 → RESTART_NOT_HONOURED" in open(os.path.join(w9c, "run", "env.txt")).read()
           and r9c["status"] == "NO_PRIMARY_VALUE", f"⛔음성 c2 재시작 미이행 (끝 sha 다름) → 러너 · 검사기 둘 다 RESTART_NOT_HONOURED · 종료 1 — rc {rc9c}")
        # S9d · S9e: 중복 실행 막기 — 살아 있는 잠금이면 아무것도 안 돈다 · 기록 명령도 거부 · 죽은 PID 의 잠금은 치우고 진행
        w9d = os.path.join(T, "w_s9d"); shutil.copytree(pkg, w9d); os.makedirs(os.path.join(w9d, "run", ".a5.lock"))
        _write(os.path.join(w9d, "run", ".a5.lock", "pid"), f"{os.getpid()}\n")
        _, rc9d, log9d = run_pkg("s9d", {"A5": "conv", "c1": "conv"}, fresh=False)
        pab = subprocess.run(["bash", os.path.join(w9d, "run_a5.sh"), "--infra-abort", "A5", "s", "t", "r"], cwd=w9d, capture_output=True, text=True)
        ck(rc9d == 2 and "두 번 띄우지 않는다" in log9d and not os.path.isdir(os.path.join(w9d, "run", f"{JOB}_A5")) and pab.returncode == 2 and "돌고 있다" in pab.stdout,
           f"⛔음성 살아 있는 실행의 잠금 → 계산 · 기록 명령 거부 (종료 2) — rc {rc9d} · {pab.returncode}")
        dead = subprocess.Popen(["true"]); dead.wait()
        w9e = os.path.join(T, "w_s9e"); shutil.copytree(pkg, w9e); os.makedirs(os.path.join(w9e, "run", ".a5.lock"))
        _write(os.path.join(w9e, "run", ".a5.lock", "pid"), f"{dead.pid}\n")
        _, rc9e, log9e = run_pkg("s9e", {"A5": "conv", "c1": "conv"}, fresh=False)
        ck(rc9e == 0 and "남은 잠금" in log9e and not os.path.exists(os.path.join(w9e, "run", ".a5.lock")), f"죽은 PID 의 잠금은 치우고 진행 · 끝나면 잠금을 지운다 — rc {rc9e}")
        # S10: c1 에 SDA 행 → SCF_UNVERIFIED (러너 · 검사기 같은 답) · c2 띄움
        w10, _, _ = run_pkg("s10", {"A5": "conv", "c1": "sda_rows", "c2": "conv"})
        r10, _ = chk(w10)
        st10 = [r_ for r_ in stat_rows(w10) if r_[1] == "c1"][0]
        ck(r10["attempts"]["c1"]["status"] == "SCF_UNVERIFIED" and st10[4] == "SCF_UNVERIFIED" and st10[8] == "row_header_SDA"
           and r10["attempts"]["c1"]["judge"]["why"] == "row_header_SDA" and os.path.isdir(os.path.join(w10, "run", f"{JOB}_c2")),
           f"⛔음성 c1 SDA 행 → 러너 · 검사기 둘 다 SCF_UNVERIFIED (row_header_SDA) — {st10}")
        # S11: c2 에 DAV 행 · 모르는 머리
        for nm, beh_, why_ in (("s11", "dav_rows", "row_header_DAV"), ("s12", "unknown_hdr", "row_header_XYZ")):
            wx, rcx, _ = run_pkg(nm, {"A5": "conv", "c1": "plateau", "c2": beh_})
            rx_, _ = chk(wx)
            stx = [r_ for r_ in stat_rows(wx) if r_[1] == "c2"][0]
            ck(rcx == 1 and rx_["attempts"]["c2"]["status"] == "SCF_UNVERIFIED" and stx[8] == why_ == rx_["attempts"]["c2"]["judge"]["why"],
               f"⛔음성 c2 {beh_} → SCF_UNVERIFIED ({why_}) · 러너 = 검사기 — rc {rcx} {stx}")
        # S13: c1 짧은 미수렴 (60 스텝) → 보조 숫자 거부 · 넓은 정체 · 드리프트
        w13, _, _ = run_pkg("s13", {"A5": "conv", "c1": "short", "c2": "wide"})
        r13, _ = chk(w13)
        ck("스텝 60 < 100" in str(r13["attempts"]["c1"].get("secondary", {}).get("refused", "")).replace("전자 스텝", "스텝"),
           f"⛔음성 c1 60 스텝 미수렴 → 보조 숫자 거부 — {r13['attempts']['c1'].get('secondary')}")
        ck(r13["attempts"]["c2"]["status"] == "SCF_NOT_CONVERGED" and r13["attempts"]["c2"]["secondary"]["u_E_eV"] > 0.1,
           f"넓은 정체 (±0.2 eV) → u_E 가 크다 (수집기가 거부할 값) — {r13['attempts']['c2'].get('secondary')}")
        w14, _, _ = run_pkg("s14", {"A5": "conv", "c1": "drift", "c2": "rmsjump"})
        r14, _ = chk(w14)
        s14 = r14["attempts"]["c1"]["secondary"]
        ck(s14["u_E_eV"] == s14["mean_shift_eV"] and s14["mean_shift_eV"] > s14["W1_range_eV"], f"⛔음성 드리프트 → u_E = 평균 이동 (창 안 폭보다 큼) — {s14}")
        # S15: 누적 상한 — 앞 시도가 180 h 를 넘었으면 다음 단을 안 띄운다 (종료 5)
        w15, rc15, _ = run_pkg("s15", {"A5": "conv", "c1": "plateau", "c2": "conv"}, args=())
        # c2 를 지우고 c1 기록의 경과를 상한 넘게 고친 뒤 (attempt.json sha 결박은 검사기 몫 — 러너 장부만 본다) 다시
        shutil.rmtree(os.path.join(w15, "run", f"{JOB}_c2"))
        aj = os.path.join(w15, "run", f"{JOB}_c1", "attempt.json")
        t_ = open(aj).read(); _write(aj, re.sub(r'"elapsed_s": \d+', '"elapsed_s": 700000', t_))
        _, rc15b, log15 = run_pkg("s15", {"A5": "conv", "c1": "plateau", "c2": "conv"}, fresh=False)
        ck(rc15b == 5 and not os.path.isdir(os.path.join(w15, "run", f"{JOB}_c2")) and "상한" in log15, f"⛔음성 누적 > 180 h → 다음 단 (c2) 안 띄움 · 종료 5 — rc {rc15b}")
        # S16: 0 스텝 인프라 중단 → run_aborted · 같은 단 다시 · 잡 전체 2 회 상한
        w16, rc16, _ = run_pkg("s16", {"A5": "conv", "c1": "zero"})
        env16 = {**os.environ}
        ab = lambda: subprocess.run(["bash", os.path.join(w16, "run_a5.sh"), "--infra-abort", "c1", "sched-1", "2026-11-21T00:00:00Z", "node fault"],
                                    cwd=w16, env=env16, capture_output=True, text=True)
        p1 = ab()
        ck(p1.returncode == 0 and os.path.isdir(os.path.join(w16, "run_aborted", f"{JOB}_c1_1")) and not os.path.isdir(os.path.join(w16, "run", f"{JOB}_c1"))
           and not os.path.isfile(os.path.join(w16, "run_aborted", f"{JOB}_c1_1", "WAVECAR")), f"0 스텝 인프라 중단 → run_aborted (WAVECAR 복사본 지움) — {p1.stdout[-120:]}")
        run_pkg("s16", {"A5": "conv", "c1": "zero"}, fresh=False); p2 = ab()
        run_pkg("s16", {"A5": "conv", "c1": "zero"}, fresh=False); p3 = ab()
        ck(p2.returncode == 0 and p3.returncode == 2 and "상한" in p3.stdout, f"⛔음성 0 스텝 중단 셋째 → 거부 (잡 전체 {INFRA_MAX} 회) — rc {p2.returncode} {p3.returncode}")
        w16b, rc16b, _ = run_pkg("s16b", {"A5": "conv", "c1": "plateau"})
        pz = subprocess.run(["bash", os.path.join(w16b, "run_a5.sh"), "--infra-abort", "c1", "s", "t", "r"], cwd=w16b, capture_output=True, text=True)
        ck(pz.returncode == 2 and "0 스텝 중단이 아니다" in pz.stdout, "⛔음성 전자 반복행이 있는 시도는 0 스텝 중단으로 기록하지 않는다")
        # S17: 인자 — W0_WAVECAR 없으면 시작하지 않는다
        w17 = os.path.join(T, "w_s17"); shutil.copytree(pkg, w17)
        p17 = subprocess.run(["bash", os.path.join(w17, "run_a5.sh")], cwd=w17, env={**os.environ, "VASP_CMD": "true", "POTCAR_DIR": potd},
                             capture_output=True, text=True)
        ck(p17.returncode != 0 and not os.path.isdir(os.path.join(w17, "run", f"{JOB}_A5")), "⛔음성 W0_WAVECAR 를 안 주면 아무것도 안 돈다")
        # S18: 검사기 — A5 이어서인데 ⓪ 기록이 거짓 (verified 1 · sha 다름) → W0_RECORD_MISMATCH
        r1b, ex1b = chk(w1)
        wj = os.path.join(ex1b, "run", "w0_check.json"); d_ = json.load(open(wj)); d_["sha256"] = "0" * 64; _write(wj, json.dumps(d_))
        ck(check_return(pkg, ex1b, msha, reg)[1]["status"] == "W0_RECORD_MISMATCH", "⛔음성 ⓪ 기록의 판정이 기록 값과 다르다 → W0_RECORD_MISMATCH")
        # S19: 검사기 — c1 INCAR 를 고친 반송 → INPUT_MODIFIED (차단)
        r1c, ex1c = chk(w1)
        ip = os.path.join(ex1c, "run", f"{JOB}_c1", "INCAR"); _write(ip, open(ip).read().replace("MAXMIX = 200", "MAXMIX = 120"))
        aj = os.path.join(ex1c, "run", f"{JOB}_c1", "attempt.json"); d_ = json.load(open(aj)); d_["sha256"]["INCAR"] = _sha(ip); _write(aj, json.dumps(d_))
        rr_ = check_return(pkg, ex1c, msha, reg)[1]
        ck(rr_["attempts"]["c1"]["status"] == "INPUT_MODIFIED" and rr_["status"] == "INPUT_MODIFIED", f"⛔음성 c1 INCAR 변경 → INPUT_MODIFIED · 채택 차단 — {rr_['status']}")
        r1d, ex1d = chk(w1)
        wi = os.path.join(ex1d, "run", f"{JOB}_c1", "WAVECAR.info"); d_ = json.load(open(wi))
        for k_ in ("src_sha256", "copied_sha256", "end_sha256"):
            d_[k_] = "d" * 64
        _write(wi, json.dumps(d_))
        aj = os.path.join(ex1d, "run", f"{JOB}_c1", "attempt.json"); d2_ = json.load(open(aj)); d2_["sha256"]["WAVECAR.info"] = _sha(wi); _write(aj, json.dumps(d2_))
        rr2 = check_return(pkg, ex1d, msha, reg)[1]
        ck(rr2["attempts"]["c1"]["status"] == "RESTART_NOT_HONOURED" and "정해진 시작 WAVECAR" in rr2["attempts"]["c1"].get("why", ""),
           f"⛔음성 c1 이 정해진 시작 WAVECAR (A5 끝) 가 아닌 것에서 시작 (기록은 셋 다 같음) → RESTART_NOT_HONOURED — {rr2['attempts']['c1'].get('why', '')[:60]}")
        # S20: 검사기 — OUTCAR MAXMIX 해석값이 기본 (-45) 이면 설정 모순
        w20, _, _ = run_pkg("s20", {"A5": "conv", "c1": "badecho"})
        r20, _ = chk(w20)
        ck(r20["attempts"]["c1"]["status"] == "SETTINGS_MISMATCH" and "MAXMIX" in r20["attempts"]["c1"]["why"], f"⛔음성 OUTCAR MAXMIX -45 → SETTINGS_MISMATCH — {r20['attempts']['c1'].get('why')}")
        # S21: 러너 judge5 = 검사기 judge5 (같은 탐침 · 단마다)
        probes = {"conv": dav(30), "sda": dav(30).replace("DAV:", "SDA:"), "cga": sda, "xyz": dav(30).replace("DAV:", "XYZ:"), "cgsp": dav(30) + "CG :  31   1  1  1\n",
                  "nospace": "SDA:1 -0.1E+03 -3E-08 -1E-08\n", "nan": dav(29) + "DAV:   30   -7.3E+02   NaN   NaN  1  1  1\n", "empty": ""}
        harness = os.path.join(T, "harness.sh")
        hb = "\n".join(r2_block(f"{n}(){{") for n in ("incar_val",)) + "\n" + _patch(_patch(r2_block("judge(){"), "judge(){", "judge_r2(){"),
                                                                                         'cat "$d/OSZICAR" 2>/dev/null |', 'osz_feed "$d" |')
        body = RUN_A5_ENV[RUN_A5_ENV.index("stage_hdr(){"):RUN_A5_ENV.index("stat5(){")]
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
    ("m07 c1 OK 여도 c2 띄움", "build_a5_vasp_package.py", 'if [ "$s1" = OK ]; then drop5 OK; log "✓ c1 주 기준 수렴 — c2 를 띄우지 않는다"; finish 0; fi', ":", "a5"),
    ("m08 누적 상한 확인 뺌", "build_a5_vasp_package.py", "awk -v w=\"$w\" -v c=\"$CAP_H\" 'BEGIN { exit !(w <= c * 3600) }' ||", "true ||", "a5"),
    ("m09 c1 · c2 끝 sha 를 안 봄 (러너)", "build_a5_vasp_package.py", '[ "$wsha" = "$wcp" ] && [ "$wcp" = "$wend" ] && hon=1', '[ "$wsha" = "$wcp" ] && hon=1', "a5"),
    ("m10 A5 재시작에 끝 sha 를 요구 (러너 A5 를 c 단처럼)", "build_a5_vasp_package.py", 'ok_ = (V.HEX64.match(str(rs.get("src_sha256", ""))) is not None and rs.get("src_sha256") == rs.get("copied_sha256") == src_sha',
     'ok_ = (V.HEX64.match(str(rs.get("src_sha256", ""))) is not None and rs.get("src_sha256") == rs.get("copied_sha256") == src_sha == (w or {}).get("sha256")', "a5"),
    ("m11 MAXMIX 해석값 확인 뺌", "build_a5_vasp_package.py", '"c1": {"IALGO": 38, "AMIX": 0.1, "AMIN": 0.01, "MAXMIX": 200}, "c2"', '"c1": {"IALGO": 38, "AMIX": 0.1, "AMIN": 0.01}, "c2"', "a5"),
    ("m12 사다리 대조 (c1 OK 인데 c2) 뺌", "build_a5_vasp_package.py", 'if C2["status"] != "MISSING" and (C1["status"] == "OK" or not c1_done):', "if False:", "a5"),
    ("m13 수집기 u_W 문턱 0.002 → 0.02", "build_v5_vasp_package.py", "A5_SEC_MAX_UW = 0.002", "A5_SEC_MAX_UW = 0.02", "v5"),
    ("m14 수집기 G4 가 u_W 를 안 더함", "build_v5_vasp_package.py", "if abs(dw) + uW <= G4_DW:", "if abs(dw) <= G4_DW:", "v5"),
    ("m15 수집기 둘 다 보조 불일치 확인 뺌", "build_v5_vasp_package.py", "if abs(e1 - e2) > u1 + u2:", "if False:", "v5"),
    ("m16 수집기 순서: c1 보조가 c2 주보다 먼저", "build_v5_vasp_package.py", "A5_ORDER = (\"c1:primary\", \"c2:primary\", \"c1:secondary\", \"c2:secondary\")",
     "A5_ORDER = (\"c1:primary\", \"c1:secondary\", \"c2:primary\", \"c2:secondary\")", "v5"),
    ("m17 수집기 보조 기준이 A5 를 받음", "build_v5_vasp_package.py", 'A5_SEC_STAGES = ("c1", "c2")', 'A5_SEC_STAGES = ("c1", "c2", "A5")', "v5"),
    ("m18 수집기 보조 최소 스텝 확인 뺌", "build_v5_vasp_package.py", "if not isinstance(n, int) or isinstance(n, bool) or n < A5_SEC_MIN_STEPS:", "if False:", "v5"),
    ("m19 러너 관문: c1 이 SDA/CGA 도 받음 (bash)", "build_a5_vasp_package.py", "stage_hdr(){ case \"$1\" in A5|c1) echo 'DAV|RMM';;", "stage_hdr(){ case \"$1\" in A5|c1) echo 'DAV|RMM|SDA|CGA';;", "a5"),
    ("m20 러너 중복 실행 거부 뺌", "build_a5_vasp_package.py", "  if lock_live; then echo \"⛔ 다른 run_a5.sh", "  if false; then echo \"⛔ 다른 run_a5.sh", "a5"),
    ("m21 러너 ⓪ 머리 확인 뺌", "build_a5_vasp_package.py", "elif ! { [ $# -ge 6 ] && [ \"$4\" = \"$W0_NK\" ] && [ \"$5\" = \"$W0_NB\" ] && enc_eq \"$6\" \"$W0_EN\"; }; then", "elif false; then", "a5"),
    ("m22 검사기 c 단 재시작이 시작 sha 를 안 봄", "build_a5_vasp_package.py", "if not (src_sha and V.HEX64.match(src_sha) and w.get(\"src_sha256\") == src_sha):", "if False:", "a5"),
)


def _mutants(names=None):
    """돌연변이마다 tools/wad 를 임시 폴더에 복사해 한 줄을 바꾸고 그 도구의 selftest 가 빨간불 (0 아닌 종료) 을 내는지 본다.
    임시 폴더의 db/ 는 레포 db/ 로 잇는다 (REPO = 임시 폴더). 바꿀 자리가 정확히 한 번이 아니면 그 돌연변이는 '무효' 로 센다 (조용히 넘기지 않는다)."""
    import tempfile
    rows, caught = [], 0
    for name, fn, old, new, which in MUTANTS:
        if names and not any(name.startswith(x) for x in names):
            continue
        with tempfile.TemporaryDirectory() as T:
            os.makedirs(os.path.join(T, "tools"))
            shutil.copytree(HERE, os.path.join(T, "tools", "wad"), ignore=shutil.ignore_patterns("__pycache__"))
            os.symlink(os.path.join(REPO, "db"), os.path.join(T, "db"))
            p = os.path.join(T, "tools", "wad", fn)
            src = open(p, encoding="utf-8").read()
            code, sep, table = src.partition("\nMUTANTS = (")          # 돌연변이 표 자체에 바꿀 글이 들어 있다 — 코드 부분에서만 센다 · 바꾼다
            if code.count(old) != 1:
                rows.append((name, f"무효 (코드에 자리 {code.count(old)} 번)")); continue
            _write(p, code.replace(old, new) + sep + table)
            tool = os.path.join(T, "tools", "wad", "build_a5_vasp_package.py" if which == "a5" else "build_v5_vasp_package.py")
            r = subprocess.run([sys.executable, "-I", tool, "--selftest"], capture_output=True, text=True, timeout=1800)
            red = r.returncode != 0
            caught += red
            rows.append((name, "빨강 ✓" if red else "초록 ✗ (시험이 못 잡음)"))
    for n, s in rows:
        print(f"  {s:<22s} {n}")
    tot = len(rows)
    print(f"{'✅' if caught == tot else '⛔'} 돌연변이 {caught}/{tot} 잡음")
    return 0 if caught == tot else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--mutants", nargs="*", metavar="접두어", help="돌연변이 시험 (이름 접두어로 고를 수 있다)")
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
        return _mutants(a.mutants)
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
