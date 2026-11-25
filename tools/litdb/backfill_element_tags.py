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
# ⚠⚠ 2026-08-06 실측 버그 — ASCII 가지가 `\s*[+-]` 만 요구해서 **대문자 한 글자 + 부호**면
#   전부 원소로 잡혔다. 실제로 틀린 태그가 커밋됐다:
#     I  ← MPM 변형구배식 (I+Δt∇v_p) 의 **단위행렬**   (stomakhin2013 눈 시뮬 논문에 '요오드')
#     P  ← 접촉력 P+ / P-                              (thorntonning1998)
#     B  ← 절 라벨 (B-1), (B-2)                        (lyu2025 등 4편)
#   --min-hits 3 으로도 못 막는다(전부 3-12회 등장).
#   -> **전하 숫자를 필수**로 만든다. 유니코드 위첨자(In³⁺)는 그대로 두고, ASCII 는 P5+ 처럼
#      숫자가 붙은 것만 인정한다. 맨 기호 + 부호는 근거로 쓰지 않는다(이 파일 머리말의 규율).
ION_RE = re.compile(rf"\b([A-Z][a-z]?)\s*(?:[{SUP}]+|\^?\d[+-])(?![a-zA-Z])")
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


#: ⛔⛔ 부정 표지 — 이 낱말이 낱말 근처에 있으면 그 등장은 **"안 했다"** 는 뜻이다.
#:   실측 사고 (2026-09-09, ren2026 digest): digest 가 *"Bader·COHP 0건"*, *"ESW 0회"*,
#:   *"MLIP 을 하나도 안 한다"* 라고 **없다고 쓴 문장**을 이 스캐너가 키워드로 긁어가
#:   `methods: bader, cohp, elf, esw, bvse, mlip …` 을 달았다. 그 결과 웹앱 Glossary 의
#:   Bader/COHP/ELF 페이지에 **그 기법을 쓴 적 없는 논문이 링크됐다.**
#:   ⚠ **비판적으로 쓴 digest 일수록 더 오염된다** — 없는 것을 꼼꼼히 적을수록 태그가 는다.
_NEG_HINT = re.compile(
    r"(?:0\s*(?:건|회|개|장|편|줄)|없다|없음|없고|없는|안\s*했|안\s*한다|안\s*쓴|"
    r"미시행|미실시|미보고|미수행|하지\s*않|못\s*한다|못\s*했|⛔|"
    r"\bno\b|\bnot\b|\bnone\b|\bzero\b|\babsent\b|\bwithout\b)")
#: 부정을 찾는 범위의 **경계**. 글자수 창이 아니라 **문장**이다.
#:   ⚠ 처음에는 ±N 자 창으로 짰는데 **결과가 창에 3배 민감했다** (실측 2026-09-09,
#:     litdb 246편: 창 20 → 제거 89태그 · 40 → 168 · 60 → 229 · 80 → 270).
#:     그러면 "몇 자로 볼까" 가 답을 정하는 임의 손잡이가 된다. 경계는 문장이어야 한다.
_SENT_SPLIT = re.compile(r"(?:\n|(?<=[.!?。])\s|(?<=다)\s{2,}|(?<=다\.)\s)")
#: 아무리 길어도 이만큼은 안 넘는다 (표·목록에서 한 '문장' 이 통째로 길어지는 것 대비)
_SENT_CAP = 300


def _clauses(low: str):
    """(시작offset, 문장) 목록. 문장이 너무 길면 `_SENT_CAP` 로 잘라 준다."""
    out, pos = [], 0
    for piece in _SENT_SPLIT.split(low):
        if piece is None:
            continue
        i = low.find(piece, pos) if piece else pos
        if i < 0:
            i = pos
        for k in range(0, max(1, len(piece)), _SENT_CAP):
            out.append((i + k, piece[k:k + _SENT_CAP]))
        pos = i + len(piece)
    return out


def scan_methods(text, keep_negated: bool = False):
    """본문에서 **실제로 쓴** 기법만 고른다 → `{gid}`.

    ⚠ 단어경계 필수 — `elf` 를 부분일치로 찾으면 'itself' 가 걸린다(실측).
    ⛔ 그리고 **부정문을 읽는다** — 낱말이 든 **문장 안에** 부정 표지가 있으면 그 등장은
      세지 않는다. 부정 아닌 등장이 **하나라도** 있어야 태그가 붙는다.

    ⛔ 이 함수가 **못 하는 것**
      · 문장 구조를 이해하지 않는다. 한 문장이 섞여 있으면 — *"NEB 로 장벽을 냈고
        COHP 는 미시행"* — **둘 다 끊는다.** 즉 혼합 문장에서는 **과소**로 틀린다.
        과대(안 한 기법을 달기)보다 과소가 낫다고 보고 그쪽으로 틀리게 했다.
      · 표·코드블록·인용문을 구분하지 않는다.
      · **이 판정으로 기존 태그를 자동 삭제하지 않는다** — `--audit_negation` 이
        목록만 낸다. 휴리스틱으로 229개를 조용히 지우는 것은 이 도구가 고치려는
        결함(기계가 임의로 정하고 사람이 안 본다)과 같은 부류다.
    """
    low = text.lower()
    out = set()
    for gid, rx in _MKEY_RE.items():
        hit = False
        for off, sent in _clauses(low):
            if rx.search(sent) and not _NEG_HINT.search(sent):
                hit = True
                break
        if hit:
            out.add(gid)
        elif keep_negated and rx.search(low):
            out.add(gid)                      # 진단용 — 종전(부정 무시) 동작
    return out


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


def _selftest_negation() -> int:
    """부정문 판정 자체시험 — **음성 경로 포함**. 양성만 있는 selftest 는 아무것도 보증 못 한다."""
    cases = [
        ("Bader 전하 분석을 수행했다", {"bader"}, "양성"),
        ("Bader·COHP 0건", set(), "⛔음성: 0건"),
        ("이 논문은 MLIP 을 하나도 안 한다", set(), "⛔음성: 안 한다"),
        ("ESW·gap·탄성 전부 0", set(), "⛔음성: 전부 0"),
        ("COHP 를 계산하지 않았다", set(), "⛔음성: 하지 않"),
        ("no Bader analysis was performed", set(), "⛔음성: no"),
        ("Bader 전하를 냈다.\nCOHP 는 0건이다", {"bader"}, "문장 분리 — 양성만 남는다"),
        ("COHP 는 0건이다.\nBader 전하를 냈다", {"bader"}, "순서를 바꿔도 같다"),
    ]
    ok = True
    for text, want, 이름 in cases:
        got = scan_methods(text)
        good = got == want
        ok &= good
        print("  %s %-26s %-34r → %s" % ("✅" if good else "⛔", 이름, text[:32],
                                         sorted(got) or "없음"))
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def _audit_negation() -> int:
    """⛔ **부정문만으로 붙은** methods 태그를 목록으로 낸다. 파일은 안 고친다.

    자동 삭제하지 않는 이유: 이건 휴리스틱이고, 휴리스틱으로 수백 개를 조용히 지우는 것은
    이 도구가 고치려는 결함(기계가 임의로 정하고 사람이 안 본다)과 **같은 부류**다.
    """
    n_f = n_t = 0
    for p in sorted(PAPERS.glob("*.md")):
        if p.stem.startswith("_") or p.name == "INDEX.md":
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        diff = sorted(scan_methods(t, keep_negated=True) - scan_methods(t))
        if not diff:
            continue
        n_f += 1
        n_t += len(diff)
        print("  %-58s %s" % (p.name[:58], ", ".join(diff)))
    print("\n⛔ digest %d편에 부정문만으로 붙은 태그 %d개 — **사람이 보고 지운다**"
          % (n_f, n_t))
    print("   (웹앱 Glossary 가 그 기법 페이지에 이 논문들을 잘못 링크한다)")
    return 1 if n_t else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="파일에 실제로 기록")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="이미 태그가 있어도 합집합으로 갱신")
    ap.add_argument("--min-hits", type=int, default=3, help="원소 최소 등장 횟수 (기본 3 — 오탐 억제)")
    ap.add_argument("--max-elements", type=int, default=18,
                    help="한 편에 붙일 원소 상한 (넘으면 빈도 상위만) ")
    ap.add_argument("-v", "--verbose", metavar="ID", help="한 편의 근거를 자세히")
    ap.add_argument("--audit_negation", action="store_true",
                    help="⛔ 부정문만으로 붙은 methods 태그 목록 (파일은 안 고친다)")
    ap.add_argument("--selftest", action="store_true",
                    help="부정문 판정 자체시험 (음성 경로 포함)")
    a = ap.parse_args()
    if a.selftest:
        return _selftest_negation()
    if a.audit_negation:
        return _audit_negation()
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
