#!/usr/bin/env python3
"""check_valence_coverage.py — 로스터의 모든 화합물이 **전하 중성이 가능한지** 미리 본다.

왜 이 도구인가 (2026-08-20)
  As₂S₃ 이 `n_structures = 0` 으로 죽었고, 두 달 동안 "구조 생성 실패" 로만 기록돼 있었다.
  원인은 물리가 아니라 **사전 한 줄 누락**이었다:
    DOPANT_DB['As'] 기본 = +5  →  As₂S₃ net_q = 2(+5) + 3(−2) = +4  (중성 아님)
    ALTERNATIVE_VALENCES 에 'As' 가 없어 +3 재시도를 못 함  →  즉사
  바로 윗줄 'Sb': [+5, +3] 은 **같은 15족·같은 M₂S₃·같은 +5 기본**인데 통과했다.
  ⇒ 한 종만 죽으면 "그 화합물이 이상한가" 로 읽히지만, 옆 종과 나란히 놓으면
    사전 누락인 게 즉시 보인다. 그 대조를 **실행 전에** 자동으로 한다.

무엇을 하나
  master_batch_273.sh 의 로스터(또는 --compounds)를 파싱해, 각 화합물이
  DOPANT_DB 기본 전하 또는 ALTERNATIVE_VALENCES 중 하나로 **net_q = 0** 이 되는지 본다.
  안 되는 화합물은 **실행 전에** 이름과 필요한 원자가를 찍는다.

이 도구가 **못 하는 것**
  · 중성이 된다고 구조가 생긴다는 보증은 아니다. 자리 반지름 필터·시드 실패는 별개다.
    (전하 중성은 **필요조건**이지 충분조건이 아니다.)
  · 어느 원자가가 물리적으로 옳은지 판정하지 않는다. 중성이 되는 값을 찾을 뿐이다.
  · 다원자 음이온(PO₄³⁻ 등)·괄호 표기·수화물을 파싱하지 못한다. 로스터가 단순식이라 충분하다.

  python3 tools/doping/check_valence_coverage.py --selftest
  python3 tools/doping/check_valence_coverage.py                 # 로스터 전수
  python3 tools/doping/check_valence_coverage.py --compounds As2S3 Sb2S3 CrO3
"""
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def _text(name):
    return (HERE / name).read_text(encoding="utf-8")


def dopant_db():
    """site_preference.py 의 DOPANT_DB 에서 원소별 기본 전하를 읽는다."""
    out = {}
    for el, q in re.findall(r"'([A-Z][a-z]?)':\s*\{'charge':\s*([+-]?\d+)", _text("site_preference.py")):
        out.setdefault(el, int(q))
    return out


def alt_valences():
    s = _text("substitute_compound.py")
    blk = re.search(r"ALTERNATIVE_VALENCES\s*=\s*\{(.*?)\n\}", s, re.S)
    if not blk:
        raise RuntimeError("ALTERNATIVE_VALENCES 블록을 못 찾았다")
    out = {}
    for el, vals in re.findall(r"'([A-Z][a-z]?)':\s*\[([^\]]+)\]", blk.group(1)):
        out[el] = [int(v.strip().lstrip("+")) if not v.strip().startswith("-")
                   else int(v.strip()) for v in vals.split(",")]
    return out


def parse_compound(formula):
    """'Nd2O3' → {'Nd': 2, 'O': 3}. substitute_compound.parse_compound 과 같은 규약."""
    parsed = {}
    for el, cnt in re.findall(r"([A-Z][a-z]?)(\d*)", formula):
        if not el:
            continue
        parsed[el] = parsed.get(el, 0) + (int(cnt) if cnt else 1)
    return parsed


def roster():
    """master_batch_273.sh 의 PHASE_1A / PHASE_1B 배열을 읽는다."""
    s = _text("master_batch_273.sh")
    out = []
    for name in ("PHASE_1A", "PHASE_1B"):
        m = re.search(name + r"=\(\s*(.*?)\n\)", s, re.S)
        if not m:
            continue
        for line in m.group(1).splitlines():
            line = line.split("#")[0].strip()
            out += [t for t in line.split() if re.fullmatch(r"[A-Za-z0-9]+", t)]
    return out


def neutralisable(formula, db, alt):
    """(가능?, 사유) — 기본 전하 또는 대안 원자가로 net_q = 0 이 되는가."""
    comp = parse_compound(formula)
    missing = [e for e in comp if e not in db]
    if missing:
        return False, f"DOPANT_DB 에 없는 원소: {', '.join(missing)}"
    net = sum(db[e] * n for e, n in comp.items())
    if net == 0:
        return True, "기본 전하로 중성"
    # 양이온 하나씩 대안 원자가를 시도 (substitute_compound 의 동작과 같다)
    cats = [e for e in comp if db[e] > 0]
    for c in cats:
        if c not in alt:
            continue
        rest = sum(db[e] * n for e, n in comp.items() if e != c)
        for v in alt[c]:
            if rest + v * comp[c] == 0:
                return True, f"{c} 를 {v:+d} 로 재시도하면 중성"
    # 왜 안 되는지 — 어떤 값이면 됐을지 알려준다
    hints = []
    for c in cats:
        rest = sum(db[e] * n for e, n in comp.items() if e != c)
        if rest % comp[c] == 0:
            need = -rest // comp[c]
            have = alt.get(c)
            hints.append(f"{c} = {need:+d} 이면 중성인데 "
                         + (f"ALTERNATIVE_VALENCES[{c}] = {have} 에 없다" if have
                            else f"ALTERNATIVE_VALENCES 에 '{c}' 항목이 아예 없다"))
    return False, f"기본 net_q = {net:+d}; " + ("; ".join(hints) if hints else "정수 원자가로 중성 불가")


def selftest():
    ok = True

    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        if not c:
            ok = False

    db, alt = dopant_db(), alt_valences()
    chk(db.get("As") == 5, f"DOPANT_DB['As'] = {db.get('As')} (기본 +5)")
    chk(db.get("S") == -2, f"DOPANT_DB['S'] = {db.get('S')}")

    # ★ 이 도구가 존재하는 이유 — 고친 뒤에는 통과해야 한다
    good, why = neutralisable("As2S3", db, alt)
    chk(good, f"[양성] As2S3 중성 가능 — {why}")
    good, why = neutralisable("Sb2S3", db, alt)
    chk(good, f"[양성] Sb2S3 중성 가능 — {why}")

    # [음성] 대안이 없으면 잡아내야 한다 (사고 당시 상태를 재현)
    alt_broken = {k: v for k, v in alt.items() if k != "As"}
    good, why = neutralisable("As2S3", db, alt_broken)
    chk(not good, "[음성] 'As' 항목을 빼면 As2S3 를 불가로 잡는다")
    chk("아예 없다" in why, f"[음성] 사유가 '항목이 없다' 로 나온다 — {why[:70]}")

    # [음성] 기본으로 이미 중성인 것을 '대안 필요' 로 오판하지 않는다
    good, why = neutralisable("Al2O3", db, alt)
    chk(good and "기본" in why, f"[음성] Al2O3 는 기본 전하로 중성 — {why}")

    # [음성] DB 에 없는 원소는 그렇게 말한다 (중성 계산을 지어내지 않는다)
    good, why = neutralisable("XyO2", db, alt)
    chk(not good and "DOPANT_DB 에 없는" in why, f"[음성] 미등록 원소 검출 — {why}")

    # [음성] 정수 원자가로 절대 안 되는 조합
    good, _ = neutralisable("LiO", db, alt)
    chk(not good, "[음성] LiO(Li+1, O−2) 는 중성 불가로 잡는다")

    r = roster()
    chk(len(r) == 91, f"로스터 {len(r)}종 (master_batch_273.sh 의 91)")
    chk("As2S3" in r and "Sb2S3" in r, "로스터에 As2S3·Sb2S3 둘 다 있다")

    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--compounds", nargs="*")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--verbose", action="store_true", help="통과한 것도 전부 찍는다")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    db, alt = dopant_db(), alt_valences()
    items = a.compounds or roster()
    bad = []
    for f in items:
        good, why = neutralisable(f, db, alt)
        if good:
            if a.verbose:
                print(f"  ✅ {f:10s} {why}")
        else:
            bad.append((f, why))
    print(f"로스터 {len(items)}종 검사 — 통과 {len(items) - len(bad)} · ⛔ {len(bad)}")
    for f, why in bad:
        print(f"  ⛔ {f}: {why}")
    if bad:
        print("\n⚠ 위 화합물은 stage-01 에서 n_structures = 0 으로 죽는다. "
              "**실행 전에** ALTERNATIVE_VALENCES 를 고칠 것.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
