#!/usr/bin/env python3
"""litdb digest 에 `> elements:` / `> methods:` 태그를 백필한다.

**왜 필요한가** — webapp 의 주기율표는 digest 헤더 60줄 안의 `elements:` 태그로 논문을 건다
(`webapp/data.py` `_paper_index_c`). 태그가 없으면 `ELEMENT_TOKENS` 토큰 스캔으로 폴백하는데
그건 13개 원소만 커버한다. 2026-08-05 감사: 163편 중 **132편에 태그가 없었다.**

**규율 — 조용한 오태깅이 태그 없음보다 나쁘다.**
원소는 **화학식/이온 표기에서만** 뽑는다. 맨 원소기호(`In`, `As`, `I`, `S`)는 영어 단어와 구별이
안 되므로 절대 근거로 쓰지 않는다.

⚠ **1차 시도의 실패를 기록해 둔다** — 약어 블록리스트로 막으려 했더니 `OCV`(→O·C·V) ·
`UPS`(→U·P·S) · `CSV`(→C·S·V) 가 줄줄이 통과했다. 대문자 3글자 약어는 무한정 나온다.
그래서 규칙을 뒤집었다: **화학식은 숫자를 포함해야 한다** (예외는 `NODIGIT_OK` 화이트리스트와
`Li + 할로겐/칼코겐` 2원소뿐). 이 규칙 하나로 위 셋이 전부 죽는다.
방법 키워드도 **단어경계 필수** — `elf` 를 부분일치로 찾으면 `itself` 가 걸렸다.
남는 오탐은 **최소 등장 횟수**(기본 3회) 문턱으로 자른다.

사용:
    python3 tools/litdb/backfill_element_tags.py --dry-run        # 무엇이 붙을지만
    python3 tools/litdb/backfill_element_tags.py --dry-run -v ID  # 한 편 상세
    python3 tools/litdb/backfill_element_tags.py --apply          # 실제 기록
    python3 tools/litdb/backfill_element_tags.py --apply --force  # 기존 태그도 갱신(합집합)
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAPERS = ROOT / "litdb" / "papers"

ELEMENTS = set("""H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn
Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd
Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu""".split())

# ⚠ 2026-08-05 실측 — **약어 블록리스트로는 못 막는다.** OCV·UPS·CSV·SEI·XPS 처럼 원소기호로
#   완전 분해되는 약어가 끝없이 나온다(전부 대문자 3글자). 그래서 규칙을 뒤집었다:
#   **화학식은 숫자를 포함해야 한다.** 예외는 아래 두 가지뿐이며 화이트리스트로만 인정한다.
#   (OCV -> O·C·V, UPS -> U·P·S, CSV -> C·S·V 가 전부 이 규칙 하나로 죽는다.)
LI_BINARY_PARTNERS = {"F", "Cl", "Br", "I", "S", "O", "H", "N", "P", "Se"}   # LiF·LiCl·LiI·LiH…
NODIGIT_OK = {"NaCl", "KCl", "KI", "KBr", "NaBr", "NaI", "HCl", "HF", "HBr",
              "MgO", "CaO", "ZnO", "NiO", "CoO", "MnO", "FeO", "CuO", "BaO", "SrO",
              "PbS", "CdS", "ZnS", "CuS", "FeS", "MnS", "CaS", "BaS", "SrS", "HgS",
              "AgCl", "AgBr", "AgI", "InP", "GaN", "SiC", "BN"}

# 이온 표기: S²⁻ · Cl⁻ · P⁵⁺ · In³⁺ · PS₄³⁻ 등 (유니코드 위첨자 + ASCII 둘 다)
SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻"
ION_RE = re.compile(rf"\b([A-Z][a-z]?)\s*(?:[{SUP}]+|\^?\d?\s*[+-])(?![a-zA-Z])")
# 화학식: 원소기호+선택적 숫자(아스키/아래첨자) 의 연쇄
SUB = "₀₁₂₃₄₅₆₇₈₉"
TOK_RE = re.compile(rf"([A-Z][a-z]?)([0-9{SUB}]*\.?[0-9{SUB}]*)")
FORMULA_RE = re.compile(rf"\b((?:[A-Z][a-z]?[0-9{SUB}]*\.?[0-9{SUB}]*){{2,}})\b")

METHOD_KEYS = {
    "dft": ["dft", "first-principles", "first principles", "density functional", "vasp",
            "quantum espresso", "pw.x"],
    "scf": ["scf convergence", "self-consistent field"],
    "pseudo": ["pseudopotential", "paw ", "uspp", "ultrasoft", "projector augmented"],
    "kpoint": ["k-point", "k-mesh", "monkhorst"],
    "functional": ["pbe", "gga", "hse06", "r2scan", "scan functional", "pbesol"],
    "bandgap": ["band gap", "bandgap", "band-gap"],
    "dos": ["density of states", " dos "],
    "pdos": ["pdos", "projected density"],
    "elf": ["electron localization function", "elf "],
    "bader": ["bader"],
    "cohp": ["cohp", "lobster", "crystal orbital hamilton"],
    "cobi": ["cobi", "crystal orbital bond index"],
    "eos": ["birch-murnaghan", "equation of state", "bm-eos"],
    "elastic": ["elastic constant", "elastic modulus", "young's modulus", "shear modulus",
                "bulk modulus", "cij", "poisson"],
    "bvse": ["bond valence", "bvse", "bvel"],
    "md": ["molecular dynamics", "aimd", "ab initio molecular"],
    "mlip": ["machine learning potential", "mlip", "interatomic potential", "uma", "sevennet",
             "mace", "nequip", "m3gnet", "chgnet", "moment tensor potential", "mtp "],
    "msd": ["mean squared displacement", "msd"],
    "arrhenius": ["arrhenius", "activation energy"],
    "phonon": ["phonon", "vibrational spectrum"],
    "neb": ["nudged elastic band", "ci-neb", "neb "],
    "esw": ["electrochemical stability window", "grand potential", "grand-potential",
            "convex hull", "e_hull", "energy above hull"],
    "adhesion": ["work of adhesion", "adhesion energy", "w_ad"],
}


def parse_formula_elements(tok_str):
    """화학식 문자열 -> 원소 집합. 하나라도 실제 원소가 아니면 None(=화학식 아님)."""
    out, pos = [], 0
    for m in TOK_RE.finditer(tok_str):
        if m.start() != pos:
            return None
        pos = m.end()
        if m.group(1) not in ELEMENTS:
            return None
        out.append(m.group(1))
    if pos != len(tok_str) or not out:
        return None
    return out


def scan(text):
    """본문 -> (원소 Counter, 근거 예시 dict)."""
    cnt, ev = Counter(), {}

    def bump(el, src):
        cnt[el] += 1
        ev.setdefault(el, set())
        if len(ev[el]) < 3:
            ev[el].add(src)

    for m in FORMULA_RE.finditer(text):
        raw = m.group(1)
        if raw in ELEMENTS:
            continue
        els = parse_formula_elements(raw)
        if not els or len(els) < 2:
            continue
        if not any(ch.isdigit() or ch in SUB for ch in raw):
            # 숫자 없는 것은 대문자 약어(OCV·UPS·CSV·SEI…)와 구별이 안 된다 → 화이트리스트만
            ok = raw in NODIGIT_OK or (len(els) == 2 and els[0] == "Li"
                                       and els[1] in LI_BINARY_PARTNERS)
            if not ok:
                continue
        for e in set(els):
            bump(e, raw)

    for m in ION_RE.finditer(text):
        el = m.group(1)
        if el in ELEMENTS:
            bump(el, m.group(0).strip())

    return cnt, ev


_MKEY_RE = {gid: re.compile("|".join(rf"\b{re.escape(k.strip())}\b" for k in keys))
            for gid, keys in METHOD_KEYS.items()}


def scan_methods(text):
    """⚠ 단어경계 필수 — `elf` 를 부분일치로 찾으면 'itself' 가 걸린다(실측)."""
    low = text.lower()
    return {gid for gid, rx in _MKEY_RE.items() if rx.search(low)}


def existing_tags(head_lines):
    el, me = set(), set()
    for line in head_lines:
        m = re.search(r"(?:elements|원소)\s*[:：]\s*(.+)", line, re.I)
        if m:
            el |= {t.strip("`*_ ") for t in re.split(r"[,\s/·]+", m.group(1))} & ELEMENTS
        m2 = re.search(r"(?:methods|기법|기술)\s*[:：]\s*(.+)", line, re.I)
        if m2:
            me |= {t.strip("`*_ ").strip() for t in re.split(r"[,/·]+", m2.group(1).lower())}
    return el, me


def insert_after_title(lines, block):
    """첫 '# ' 제목 바로 다음(그리고 기존 '> ' 인용 블록 뒤)에 태그를 넣는다."""
    i = next((n for n, l in enumerate(lines) if l.startswith("# ")), -1)
    if i < 0:
        return [*block, "", *lines]
    j = i + 1
    while j < len(lines) and (lines[j].strip() == "" or lines[j].startswith(">")):
        j += 1
    out = lines[:j]
    if out and out[-1].strip() != "":
        out.append("")
    out += block + [""]
    return out + lines[j:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="파일에 실제로 기록")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="이미 태그가 있어도 합집합으로 갱신")
    ap.add_argument("--min-hits", type=int, default=3, help="원소 최소 등장 횟수 (기본 3 — 오탐 억제)")
    ap.add_argument("--max-elements", type=int, default=18,
                    help="한 편에 붙일 원소 상한 (넘으면 빈도 상위만) ")
    ap.add_argument("-v", "--verbose", metavar="ID", help="한 편의 근거를 자세히")
    a = ap.parse_args()
    if not a.apply and not a.dry_run and not a.verbose:
        a.dry_run = True

    files = sorted(PAPERS.glob("*.md"))
    n_new = n_skip = n_none = 0
    for p in files:
        if p.stem.startswith("_") or p.name == "INDEX.md":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        had_el, had_me = existing_tags(lines[:60])
        if had_el and had_me and not a.force:
            n_skip += 1
            continue

        cnt, ev = scan(text)
        els = {e for e, c in cnt.items() if c >= a.min_hits}
        if len(els) > a.max_elements:
            els = {e for e, _ in sorted(cnt.items(), key=lambda x: -x[1])[:a.max_elements]}
        mets = scan_methods(text)
        els |= had_el
        mets |= had_me

        if a.verbose and p.stem == a.verbose:
            print(f"\n=== {p.stem} ===")
            for e, c in sorted(cnt.items(), key=lambda x: -x[1]):
                mark = "✓" if e in els else " "
                print(f"  {mark} {e:3s} ×{c:<4d} {sorted(ev.get(e, []))[:3]}")
            print(f"  methods: {sorted(mets)}")
            continue
        if a.verbose:
            continue

        if not els:
            n_none += 1
            print(f"  ⚠ 원소 근거 없음: {p.stem}")
            continue

        block = [f"> elements: {' '.join(sorted(els))}"]
        if mets:
            block.append(f"> methods: {', '.join(sorted(mets))}")
        n_new += 1
        if a.apply:
            # 기존 태그 줄은 지우고 새로 넣는다(중복 방지)
            keep = [l for n, l in enumerate(lines)
                    if not (n < 60 and re.match(r">\s*(elements|methods|원소|기법)\s*[:：]", l, re.I))]
            p.write_text("\n".join(insert_after_title(keep, block)) + "\n", encoding="utf-8")
        else:
            print(f"  + {p.stem}\n      {block[0]}"
                  + (f"\n      {block[1]}" if len(block) > 1 else ""))

    print(f"\n[backfill] 대상 {n_new} · 이미 있음 {n_skip} · 근거없음 {n_none} "
          f"(전체 {len(files)})  {'APPLIED' if a.apply else 'dry-run'}")


if __name__ == "__main__":
    sys.exit(main())
