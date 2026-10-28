"""NdO-LPSCl1.6 원고 (CEI 트랙 · 1저자 = 실험 쪽) 의 '4.5. DFT calculations' Word 두 판을 만든다.

쓰기:
  python3 tools/manuscripts/build_ndo_methods_docx.py <template.docx|dir> <out.docx> main|si
  python3 tools/manuscripts/build_ndo_methods_docx.py --md main|si        # kb 문서용 md 문단
  python3 tools/manuscripts/build_ndo_methods_docx.py --verify-md kb/papers/ndo_lpscl16_methods_2026_10_28.md
  python3 tools/manuscripts/build_ndo_methods_docx.py --check | --selftest
템플릿 = 사용자 method 템플릿 패키지. 저장소에는 그 패키지로 만든 B2O3 본문판
(`kb/papers/b2o3_bo_lpsc16_methods_main_2026_10_21.docx`) 이 있어서 그걸 주면 된다 — 본문만 갈아 끼운다.

B2O3 빌더 (2026-10-21 · 스크래치) 와 같은 방식: 템플릿의 styles·theme·settings·쪽 설정은 그대로 두고
본문만 바꾼다 (이탤릭 절 제목 · 2 줄 간격 · 첫 줄 들여쓰기 · 글자 단위 아래/위첨자 · OMML 식 · 참고문헌).
이 원고와 다른 점 (원고 [1] 의 Elsevier 꼴): 인용은 문장부호 앞의 보통 글자 [n] · 참고문헌은 제목·DOI 포함.
`main` = 4.5 절 압축판 (식 없음) · `si` = Supplementary Material 의 Computational details (식 S1–S3).
참고문헌 번호는 SI 가 정한다 (처음 인용 순서 · 14 개 · REFS 순서와 같아야 한다). 본문판은 쓰는 문헌만 남기고
처음 인용 순서로 **다시 매긴다** (`renumber` · 지금은 Marzari–Vanderbilt 가 빠져 13 개). `--check` 가 둘 다 본다.
`--md` 는 같은 문단을 md 로 (유니코드 첨자가 있으면 그것 · 없으면 <sub>/<sup>) — kb 문서 본문을 이 한 원본에서 뽑는다.
`--verify-md` 는 kb 문서 안에 두 판의 md 문단이 **글자 그대로** 다 있는지 본다 (손으로 고친 쪽이 갈라지면 잡는다).

미니 표기: *italic*  _{아래첨자}  ^{위첨자}.
⛔ 이 도구가 못 하는 것: 문법·사실은 안 본다 · SI 문단 순서를 바꿔도 SI 번호는 다시 매기지 않는다 (SI 가 기준 번호라
`--check` 가 순서 어긋남만 알린다) · 원고 자체의 참고문헌 목록에 합치지 않는다 · 식 (S1–S3) 은 md 쪽 LaTeX 와
대조하지 않는다 (OMML 은 이 파일 안의 정의가 정본) · Word 렌더 확인은 하지 않는다 (LibreOffice 로 따로).
"""
import re, sys, shutil, zipfile, os, tempfile
from xml.sax.saxutils import escape

# ---- content ------------------------------------------------------------------------
P_MAIN = [
"DFT calculations were performed with Quantum ESPRESSO [1–3] using the Perdew–Burke–Ernzerhof (PBE) generalized gradient approximation (GGA) [4], with kinetic energy cutoffs of 60 and 480 Ry for the wavefunctions and charge density, respectively. The Brillouin zone was sampled with Monkhorst–Pack *k*-point grids [5], and further computational details are given in the Supplementary Material.",
"Li migration barriers (Fig. 3f,g) were calculated with the climbing-image nudged elastic band method [6] for a Li vacancy hopping between nearest-neighbor 8*c* sites. Antifluorite Li_{2}S and the Li–Nd alloy, represented by an ordered BiF_{3}-type Li_{3}Nd model, were modeled with 3 × 3 × 3 and 2 × 2 × 2 supercells of their primitive cells containing a negatively charged and a neutral Li vacancy, respectively, starting from the Materials Project structures [7]. Ultrasoft GBRV pseudopotentials were used for Li and S [8], and a projector augmented-wave (PAW) dataset from PSlibrary with the Nd 4*f* electrons frozen in the core was used for Nd [9].",
"The band gaps of Li_{2}S, Li_{3}P, Li_{2}O, Li_{3}PO_{4}, and LiCl (Fig. 3h) were obtained from the Kohn–Sham eigenvalues at the valence band maximum and conduction band minimum of non-self-consistent calculations with fixed occupations, after full relaxation of the Materials Project structures [7]; GBRV ultrasoft pseudopotentials were used for Li, S, and Cl [8], and PSlibrary datasets for P and O [9].",
"Interfacial reaction energies between the SEs and NCM were calculated as a function of voltage (Fig. 5e,f) following the approach of Richards et al. [11], as implemented in pymatgen [12], with the mixed GGA/GGA+*U* energies of the Materials Project database [7,13]. The SEs and NCM were represented by the convex-hull energies at their compositions, and the interface was treated as open to Li at a chemical potential *μ*_{Li}(*φ*) = *μ*_{Li}^{0} − *eφ* [14], where *μ*_{Li}^{0} is the chemical potential of Li metal, *e* is the elementary charge, and *φ* is the applied voltage vs. Li/Li^{+}. At each voltage, the reaction energy was taken as the most negative grand-potential reaction energy over all SE/NCM mixing ratios, and the corresponding reaction products were identified.",
"The band gaps of the Nd-containing CEI components (Fig. SX) were calculated with the same procedure, but with PAW datasets from PSlibrary for all elements, including the Nd dataset with the 4*f* electrons frozen in the core [9].",
]

P_SI = [
"DFT calculations were performed with Quantum ESPRESSO [1–3] using the Perdew–Burke–Ernzerhof (PBE) generalized gradient approximation (GGA) [4]. Kinetic energy cutoffs of 60 and 480 Ry were used for the wavefunctions and charge density, respectively, the Brillouin zone was sampled with Γ-centered Monkhorst–Pack *k*-point grids [5], and self-consistent calculations were converged to 10^{−8} Ry.",
"Li migration barriers were calculated with the climbing-image nudged elastic band (CI-NEB) method [6] for a Li vacancy hopping between nearest-neighbor 8*c* sites. Antifluorite Li_{2}S (*Fm*3̅*m*; mp-1153 in the Materials Project database [7]) and an ordered BiF_{3}-type Li_{3}Nd model (*Fm*3̅*m*; mp-976264, a hypothetical phase above the convex hull) were first relaxed with variable cell. Ultrasoft GBRV pseudopotentials were used for Li and S [8], and a projector augmented-wave (PAW) dataset from PSlibrary with the Nd 4*f* electrons frozen in the core was used for Nd [9]. The vacancies were placed in 3 × 3 × 3 (Li_{2}S, 80 atoms) and 2 × 2 × 2 (Li_{3}Nd, 31 atoms) supercells of the primitive cells, sampled with a 3 × 3 × 3 *k*-point grid. The vacancy in the insulating Li_{2}S was modeled in the negatively charged state (V_{Li}^{−}) with a uniform compensating background charge and Gaussian smearing of 0.005 Ry, whereas that in the metallic Li_{3}Nd was modeled as neutral with Marzari–Vanderbilt smearing [10] of 0.02 Ry.",
"The two vacancy endpoints were relaxed at fixed cell until all force components were below 10^{−3} Ry bohr^{−1}, and the minimum-energy path, represented by seven images including the two endpoints, was optimized until the force perpendicular to the path fell below 0.05 eV Å^{−1}. For Li_{3}Nd, both vacancy endpoints reconstructed substantially on relaxation from the ideal lattice, so the barrier refers to this locally reconstructed 2 × 2 × 2 model. A check with a 3 × 3 × 3 supercell was attempted, but its vacancy endpoints also reconstructed substantially and the CI-NEB between them did not converge; the Li_{3}Nd barrier is therefore not converged with respect to cell size.",
"The band gaps of the interphase components in Fig. 3h were calculated for Li_{2}S (mp-1153, *Fm*3̅*m*), Li_{3}P (mp-736, *P*6_{3}/*mmc*), Li_{2}O (mp-1960, *Fm*3̅*m*), β-Li_{3}PO_{4} (mp-13725, *Pmn*2_{1}), and rock-salt LiCl (mp-22905, *Fm*3̅*m*), starting from the Materials Project structures [7]. Ultrasoft GBRV pseudopotentials were used for Li, S, and Cl [8], and PSlibrary datasets for P (ultrasoft) and O (PAW) [9]. The structures were fully relaxed with Marzari–Vanderbilt smearing [10] of 0.01 Ry and a *k*-point spacing of 0.30 Å^{−1}, and the band gap was obtained from the Kohn–Sham eigenvalues at the valence band maximum and conduction band minimum of a non-self-consistent calculation with fixed occupations on a denser *k*-point grid (spacing 0.15 Å^{−1}).",
"Interfacial reaction energies between the solid electrolytes (SEs) and NCM (LiNi_{0.8}Co_{0.1}Mn_{0.1}O_{2}) were calculated following the approach of Richards et al. [11], as implemented in pymatgen [12], using Materials Project energies [7] in the mixed GGA/GGA+*U* scheme [13]. LPSCl_{1.6} (Li_{5.4}PS_{4.4}Cl_{1.6}), NdO-LPSCl_{1.6} (Li_{5.44}Nd_{0.02}P_{0.98}S_{4.37}O_{0.03}Cl_{1.6}), and NCM were represented by the convex-hull energies at their compositions. The interface was treated as open to Li, with the Li chemical potential set by the applied voltage *φ* (vs. Li/Li^{+}) through Eq. (S1) [14], where *μ*_{Li}^{0} is the chemical potential of Li metal and *e* is the elementary charge. With the grand potential of each phase defined by Eq. (S2), where *E* is its energy and *N*_{Li} is its number of Li atoms, the reaction energy was obtained from Eq. (S3), where *x* is the fraction of SE in the SE/NCM mixture, *Φ*_{eq}(*x*) is the grand potential of the equilibrium phases of the mixture, and *Φ*_{SE} and *Φ*_{NCM} are those of the unreacted SE and NCM; all grand potentials were normalized per atom excluding Li. The calculations were performed at six voltages between 2.5 and 4.5 V, and the reaction products were taken from the equilibrium phases at the minimizing *x*.",
"The band gaps of the Nd-containing cathode–electrolyte interphase components, including NdP_{5}O_{14} (mp-560681, *Pmna*), were calculated with the same procedure, but with PAW datasets from PSlibrary for all elements [9]. Because the Nd 4*f* electrons are frozen in the core of the Nd dataset, the calculations were non-spin-polarized and no Hubbard *U* correction was applied.",
]

REFS = [
"P. Giannozzi, S. Baroni, N. Bonini, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, G. L. Chiarotti, M. Cococcioni, I. Dabo, A. Dal Corso, S. de Gironcoli, S. Fabris, G. Fratesi, R. Gebauer, U. Gerstmann, C. Gougoussis, A. Kokalj, M. Lazzeri, L. Martin-Samos, N. Marzari, F. Mauri, R. Mazzarello, S. Paolini, A. Pasquarello, L. Paulatto, C. Sbraccia, S. Scandolo, G. Sclauzero, A. P. Seitsonen, A. Smogunov, P. Umari, R. M. Wentzcovitch, QUANTUM ESPRESSO: a modular and open-source software project for quantum simulations of materials, J. Phys.: Condens. Matter 21 (2009) 395502. https://doi.org/10.1088/0953-8984/21/39/395502.",
"P. Giannozzi, O. Andreussi, T. Brumme, O. Bunau, M. Buongiorno Nardelli, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, M. Cococcioni, N. Colonna, I. Carnimeo, A. Dal Corso, S. de Gironcoli, P. Delugas, R. A. DiStasio Jr., A. Ferretti, A. Floris, G. Fratesi, G. Fugallo, R. Gebauer, U. Gerstmann, F. Giustino, T. Gorni, J. Jia, M. Kawamura, H.-Y. Ko, A. Kokalj, E. Küçükbenli, M. Lazzeri, M. Marsili, N. Marzari, F. Mauri, N. L. Nguyen, H.-V. Nguyen, A. Otero-de-la-Roza, L. Paulatto, S. Poncé, D. Rocca, R. Sabatini, B. Santra, M. Schlipf, A. P. Seitsonen, A. Smogunov, I. Timrov, T. Thonhauser, P. Umari, N. Vast, X. Wu, S. Baroni, Advanced capabilities for materials modelling with Quantum ESPRESSO, J. Phys.: Condens. Matter 29 (2017) 465901. https://doi.org/10.1088/1361-648X/aa8f79.",
"P. Giannozzi, O. Baseggio, P. Bonfà, D. Brunato, R. Car, I. Carnimeo, C. Cavazzoni, S. de Gironcoli, P. Delugas, F. Ferrari Ruffino, A. Ferretti, N. Marzari, I. Timrov, A. Urru, S. Baroni, Quantum ESPRESSO toward the exascale, J. Chem. Phys. 152 (2020) 154105. https://doi.org/10.1063/5.0005082.",
"J. P. Perdew, K. Burke, M. Ernzerhof, Generalized gradient approximation made simple, Phys. Rev. Lett. 77 (1996) 3865–3868. https://doi.org/10.1103/PhysRevLett.77.3865.",
"H. J. Monkhorst, J. D. Pack, Special points for Brillouin-zone integrations, Phys. Rev. B 13 (1976) 5188–5192. https://doi.org/10.1103/PhysRevB.13.5188.",
"G. Henkelman, B. P. Uberuaga, H. Jónsson, A climbing image nudged elastic band method for finding saddle points and minimum energy paths, J. Chem. Phys. 113 (2000) 9901–9904. https://doi.org/10.1063/1.1329672.",
"A. Jain, S. P. Ong, G. Hautier, W. Chen, W. D. Richards, S. Dacek, S. Cholia, D. Gunter, D. Skinner, G. Ceder, K. A. Persson, Commentary: The Materials Project: A materials genome approach to accelerating materials innovation, APL Mater. 1 (2013) 011002. https://doi.org/10.1063/1.4812323.",
"K. F. Garrity, J. W. Bennett, K. M. Rabe, D. Vanderbilt, Pseudopotentials for high-throughput DFT calculations, Comput. Mater. Sci. 81 (2014) 446–452. https://doi.org/10.1016/j.commatsci.2013.08.053.",
"A. Dal Corso, Pseudopotentials periodic table: From H to Pu, Comput. Mater. Sci. 95 (2014) 337–350. https://doi.org/10.1016/j.commatsci.2014.07.043.",
"N. Marzari, D. Vanderbilt, A. De Vita, M. C. Payne, Thermal contraction and disordering of the Al(110) surface, Phys. Rev. Lett. 82 (1999) 3296–3299. https://doi.org/10.1103/PhysRevLett.82.3296.",
"W. D. Richards, L. J. Miara, Y. Wang, J. C. Kim, G. Ceder, Interface stability in solid-state batteries, Chem. Mater. 28 (2016) 266–273. https://doi.org/10.1021/acs.chemmater.5b04082.",
"S. P. Ong, W. D. Richards, A. Jain, G. Hautier, M. Kocher, S. Cholia, D. Gunter, V. L. Chevrier, K. A. Persson, G. Ceder, Python Materials Genomics (pymatgen): A robust, open-source python library for materials analysis, Comput. Mater. Sci. 68 (2013) 314–319. https://doi.org/10.1016/j.commatsci.2012.10.028.",
"A. Jain, G. Hautier, S. P. Ong, C. J. Moore, C. C. Fischer, K. A. Persson, G. Ceder, Formation enthalpies by mixing GGA and GGA+U calculations, Phys. Rev. B 84 (2011) 045115. https://doi.org/10.1103/PhysRevB.84.045115.",
"Y. Zhu, X. He, Y. Mo, Origin of outstanding stability in the lithium solid electrolyte materials: Insights from thermodynamic analyses based on first-principles calculations, ACS Appl. Mater. Interfaces 7 (2015) 23685–23693. https://doi.org/10.1021/acsami.5b07517.",
]

HEAD_MAIN, HEAD_SI = "4.5. DFT calculations", "Computational details"
EQ_AFTER_SI = 4          # display equations S1–S3 follow this SI paragraph (the one citing them)


# ---- citation check -----------------------------------------------------------------
def cited(text):
    """[1–3], [10,13] → [1, 2, 3, 10, 13] in order of appearance."""
    out = []
    for grp in re.findall(r"\[(\d+(?:\s*[–,]\s*\d+)*)\]", text):
        for part in grp.split(","):
            if "–" in part:
                a, b = (int(v) for v in part.split("–"))
                out += list(range(a, b + 1))
            else:
                out.append(int(part))
    return out


def check(paras, n_refs, label):
    """SI 용 — 처음 인용 순서가 오름차순이고 1..n_refs 가 빠짐없이 쓰였는가 (SI 가 번호를 정한다)."""
    seq, seen, errs = [], set(), []
    for p in paras:
        for n in cited(p):
            if n not in seen:
                seq.append(n); seen.add(n)
    if seq != sorted(seq):
        errs.append(f"{label}: first-citation order {seq} is not ascending")
    missing = [n for n in range(1, n_refs + 1) if n not in seen]
    extra = [n for n in seen if n > n_refs or n < 1]
    if missing: errs.append(f"{label}: references never cited {missing}")
    if extra: errs.append(f"{label}: citations without a reference {extra}")
    return errs


def renumber(paras, refs=None):
    """본문판 용 — 쓰는 문헌만 처음 인용 순서로 1, 2, … 로 다시 매긴다. (새 문단, 새 문헌 목록) 을 돌려준다.

    [1–3] · [7,13] 꼴을 다시 쓴다 (셋 이상 연속이면 범위, 아니면 쉼표). 목록 밖 번호는 ValueError.
    """
    refs = REFS if refs is None else refs
    order = []
    for p in paras:
        for n in cited(p):
            if n not in order:
                order.append(n)
    bad = [n for n in order if not 1 <= n <= len(refs)]
    if bad:
        raise ValueError(f"citations without a reference: {bad}")
    mp = {g: k + 1 for k, g in enumerate(order)}

    def fmt(nums):
        nums, out, a = sorted(set(nums)), [], 0
        while a < len(nums):
            b = a
            while b + 1 < len(nums) and nums[b + 1] == nums[b] + 1:
                b += 1
            out.append(f"{nums[a]}–{nums[b]}" if b - a >= 2 else ",".join(str(v) for v in nums[a:b + 1]))
            a = b + 1
        return "[" + ",".join(out) + "]"

    new = [re.sub(r"\[\d+(?:\s*[–,]\s*\d+)*\]", lambda m: fmt([mp[n] for n in cited(m.group(0))]), p)
           for p in paras]
    return new, [refs[g - 1] for g in order]


def check_all():
    errs = check(P_SI, len(REFS), "si")
    si, si_refs = renumber(P_SI)
    if si != P_SI or si_refs != REFS:
        errs.append("si: renumbering must be the identity (SI defines the reference numbers)")
    try:
        _, main_refs = renumber(P_MAIN)
        if not main_refs:
            errs.append("main: no citations")
    except ValueError as e:
        errs.append(f"main: {e}")
    return errs


def selftest():
    ok = True
    def t(c, m):
        nonlocal ok
        print(("  ok  " if c else "  FAIL ") + m); ok &= bool(c)
    t(cited("a [1–3] b [10,13] c [4].") == [1, 2, 3, 10, 13, 4], "cited() expands ranges and lists")
    t(not check_all(), "si: ascending and complete (14) · main: renumbers cleanly")
    nm, nr = renumber(P_MAIN)
    t(len(nr) == 13 and REFS[9] not in nr and "[7,12]" in nm[3] and "[13]" in nm[3],
      "main: Marzari–Vanderbilt dropped → 13 refs, [7,13]→[7,12] and [14]→[13]")
    t(renumber(["a [2] b [5,7] c [1–3]."])[0] == ["a [1] b [2,3] c [1,4,5]."], "renumber(): first-appearance order, ranges and lists")
    try:
        renumber(["x [15]."]); t(False, "[negative] renumber() rejects a citation beyond the list")
    except ValueError:
        t(True, "[negative] renumber() rejects a citation beyond the list")
    # negative paths: the check must catch a swapped order and an uncited reference
    t(bool(check(["x [2] y [1]."], 2, "neg")), "[negative] out-of-order first citation is caught")
    t(bool(check(["x [1]."], 2, "neg")), "[negative] an uncited reference is caught")
    t(bool(check(["x [1] [3]."], 2, "neg")), "[negative] a citation beyond the list is caught")
    t(md("Li_{2}S ^{−1} *μ*_{Li}^{0}") == "Li₂S ⁻¹ *μ*<sub>Li</sub>⁰", "md(): Unicode where it exists, <sub> otherwise")
    # Word runs must keep every visible character: compare the run text with the md text
    def run_text(markup):
        return "".join(re.findall(r'<w:t xml:space="preserve">([^<]*)</w:t>', runs(markup)))
    t(run_text("Li.pbe-sl-kjpaw_psl.1.0.0 · mp_api") == "Li.pbe-sl-kjpaw_psl.1.0.0 · mp_api",
      "[negative] a lone '_' survives into the Word runs (kjpaw_psl · mp_api)")
    flat = lambda p: re.sub(r"[*{}]|_(?=\{)|\^(?=\{)", "", p)
    lost = [p[:40] for p in P_MAIN + P_SI + REFS if run_text(p) != escape(flat(p))]
    t(not lost, f"every main/si/reference paragraph keeps all its characters in Word ({len(lost)} lost)")
    # verify_md: a complete document passes, a document with one word changed is caught
    d = tempfile.mkdtemp(prefix="ndo_md_")
    full = os.path.join(d, "full.md"); bad = os.path.join(d, "bad.md")
    body = "\n\n".join(md(p) for p in renumber(P_MAIN)[0] + P_SI)
    open(full, "w", encoding="utf8").write(body)
    open(bad, "w", encoding="utf8").write(body.replace("seven images", "eight images", 1))
    t(verify_md(full) == [], "verify_md: every main/si paragraph found verbatim")
    t(len(verify_md(bad)) == 1, "[negative] verify_md catches a one-word edit in the kb text")
    shutil.rmtree(d)
    return ok


# ---- Markdown rendering (kb document is generated from the same source) ---------------
SUBS = dict(zip("0123456789+−=()aehijklmnoprstuvx", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ"))
SUPS = dict(zip("0123456789+−=()in", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁱⁿ"))


def md(markup):
    def sub(m):
        s = m.group(1)
        if all(c in SUBS or c == "." for c in s):          # '.' stays on the line (₁.₆ — as the B2O3 md)
            return "".join(SUBS.get(c, c) for c in s)
        return f"<sub>{s}</sub>"
    def sup(m):
        s = m.group(1)
        return "".join(SUPS[c] for c in s) if all(c in SUPS for c in s) else f"<sup>{s}</sup>"
    return re.sub(r"\^\{([^}]*)\}", sup, re.sub(r"_\{([^}]*)\}", sub, markup))


# ---- WordprocessingML ---------------------------------------------------------------
def runs(markup):
    out = []
    # ⛔ 마지막 갈래 `([*_^])` 가 없으면 짝 없는 '_' 가 어느 갈래에도 안 걸려 **조용히 사라진다**
    #   (2026-10-28 렌더에서 잡음: 'kjpaw_psl' → 'kjpawpsl' · 'mp_api' → 'mpapi' · md 쪽은 멀쩡해서 안 보였다).
    for m in re.finditer(r"\*([^*]+)\*|_\{([^}]*)\}|\^\{([^}]*)\}|([^*_^]+)|([*_^])", markup):
        it, sb, sp, plain, lone = m.groups()
        if lone is not None:
            plain = lone
        if it is not None:
            rpr, t = "<w:i/><w:iCs/>", it
        elif sb is not None:
            rpr, t = '<w:vertAlign w:val="subscript"/>', sb
        elif sp is not None:
            rpr, t = '<w:vertAlign w:val="superscript"/>', sp
        else:
            rpr, t = "", plain
        rp = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
        for k, piece in enumerate(t.split("\t")):
            if k: out.append(f"<w:r>{rp}<w:tab/></w:r>")
            if piece: out.append(f'<w:r>{rp}<w:t xml:space="preserve">{escape(piece)}</w:t></w:r>')
    return "".join(out)


HEAD_PPR = '<w:pPr><w:spacing w:before="240" w:after="240" w:line="480" w:lineRule="auto"/></w:pPr>'
BODY_PPR = '<w:pPr><w:spacing w:after="0" w:line="480" w:lineRule="auto"/><w:ind w:firstLineChars="150" w:firstLine="360"/><w:jc w:val="both"/></w:pPr>'
REF_PPR = ('<w:pPr><w:tabs><w:tab w:val="left" w:pos="560"/></w:tabs>'
           '<w:spacing w:after="0" w:line="480" w:lineRule="auto"/><w:ind w:left="560" w:hanging="560"/></w:pPr>')
EQ_PPR = ('<w:pPr><w:tabs><w:tab w:val="center" w:pos="4513"/><w:tab w:val="right" w:pos="9026"/></w:tabs>'
          '<w:spacing w:after="0" w:line="480" w:lineRule="auto"/></w:pPr>')


def heading(text):
    return f"<w:p>{HEAD_PPR}{runs('*' + text + '*')}</w:p>"


def para(markup, ppr=BODY_PPR):
    return f"<w:p>{ppr}{runs(markup)}</w:p>"


# OMML helpers (same conventions as the B2O3 builder: variables italic, labels upright)
MF = '<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/></w:rPr>'
def mr(t, upright=False):
    sty = '<m:rPr><m:sty m:val="p"/></m:rPr>' if upright else ""
    return f'<m:r>{sty}{MF}<m:t xml:space="preserve">{escape(t)}</m:t></m:r>'
def sub(base, s):
    return f"<m:sSub><m:e>{mr(base)}</m:e><m:sub>{mr(s, True)}</m:sub></m:sSub>"
def subsup(base, s, p):
    return f"<m:sSubSup><m:e>{mr(base)}</m:e><m:sub>{mr(s, True)}</m:sub><m:sup>{mr(p, True)}</m:sup></m:sSubSup>"
def paren(inner, beg="(", end=")"):
    dpr = "" if (beg, end) == ("(", ")") else f'<m:dPr><m:begChr m:val="{beg}"/><m:endChr m:val="{end}"/></m:dPr>'
    return f"<m:d>{dpr}<m:e>{inner}</m:e></m:d>"
def minx(arg):
    return (f"<m:func><m:fName><m:limLow><m:e>{mr('min', True)}</m:e><m:lim>{mr('x')}</m:lim></m:limLow></m:fName>"
            f"<m:e>{arg}</m:e></m:func>")
def eq_para(omml, number):
    return (f"<w:p>{EQ_PPR}<w:r><w:tab/></w:r><m:oMath>{omml}</m:oMath>"
            f'<w:r><w:tab/><w:t xml:space="preserve">({number})</w:t></w:r></w:p>')

EQ_S1 = sub("μ", "Li") + paren(mr("φ")) + mr("=", True) + subsup("μ", "Li", "0") + mr("−", True) + mr("e") + mr("φ")
EQ_S2 = mr("Φ") + mr("=", True) + mr("E") + mr("−", True) + sub("μ", "Li") + sub("N", "Li")
EQ_S3 = (mr("Δ", True) + sub("E", "rxn") + paren(mr("φ")) + mr("=", True)
         + minx(paren(sub("Φ", "eq") + paren(mr("x")) + mr("−", True) + mr("x") + sub("Φ", "SE")
                      + mr("−", True) + paren(mr("1", True) + mr("−", True) + mr("x")) + sub("Φ", "NCM"), "[", "]")))


def verify_md(path):
    """kb 문서에 두 판의 md 문단이 글자 그대로 있는가. 없는 문단의 앞머리를 돌려준다."""
    text = open(path, encoding="utf8").read()
    miss = []
    for label, paras in (("main", renumber(P_MAIN)[0]), ("si", P_SI)):
        for k, p in enumerate(paras, 1):
            if md(p) not in text:
                miss.append(f"{label} 문단 {k}: {md(p)[:70]}…")
    return miss


def build(tpl, out, variant):
    tmp = None
    if os.path.isfile(tpl):                       # .docx 를 주면 풀어서 쓴다
        tmp = tempfile.mkdtemp(prefix="ndo_tpl_")
        with zipfile.ZipFile(tpl) as z:
            z.extractall(tmp)
        tpl_dir = tmp
    else:
        tpl_dir = tpl
    paras, refs = renumber(P_MAIN if variant == "main" else P_SI)   # 본문판은 쓰는 문헌만 · 번호 다시
    if variant == "main":
        body = [heading(HEAD_MAIN)] + [para(p) for p in paras]
        neq = 0
    else:
        body = [heading(HEAD_SI)]
        for i, p in enumerate(paras):
            body.append(para(p))
            if i == EQ_AFTER_SI:
                body += [eq_para(EQ_S1, "S1"), eq_para(EQ_S2, "S2"), eq_para(EQ_S3, "S3")]
        neq = 3
    body.append(heading("References"))
    body += [para(f"[{i}]\t" + r, REF_PPR) for i, r in enumerate(refs, 1)]

    x = open(os.path.join(tpl_dir, "word", "document.xml"), encoding="utf8").read()
    head = x[: x.find("<w:body>") + len("<w:body>")]
    sect = x[x.find("<w:sectPr"):]
    work = out + ".d"
    shutil.rmtree(work, ignore_errors=True)
    shutil.copytree(tpl_dir, work)
    open(os.path.join(work, "word", "document.xml"), "w", encoding="utf8").write(head + "".join(body) + sect)
    if os.path.exists(out): os.remove(out)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        names = []
        for root, _, files in os.walk(work):
            for f in files:
                names.append(os.path.relpath(os.path.join(root, f), work))
        names.sort(key=lambda n: (n != "[Content_Types].xml", n))
        for n in names: z.write(os.path.join(work, n), n)
    shutil.rmtree(work)
    if tmp:
        shutil.rmtree(tmp)
    words = sum(len(re.sub(r"[*_^{}]", "", p).split()) for p in paras)
    print("wrote", out, os.path.getsize(out), "bytes;", variant, len(paras), "paragraphs,",
          words, "words,", neq, "equations,", len(refs), "references")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--selftest"]:
        sys.exit(0 if selftest() else 1)
    if a[:1] == ["--check"]:
        errs = check_all()
        n_main = len(renumber(P_MAIN)[1]) if not errs else "?"
        print("\n".join(errs) or f"citations ok (si: ascending, all {len(REFS)} cited · main: renumbered, {n_main} refs)")
        sys.exit(1 if errs else 0)
    if a[:1] == ["--md"]:
        for p in renumber(P_MAIN if a[1] == "main" else P_SI)[0]:
            print(md(p) + "\n")
        sys.exit(0)
    if a[:1] == ["--verify-md"]:
        miss = verify_md(a[1])
        print("\n".join(miss) or f"md ok — {len(P_MAIN)} + {len(P_SI)} 문단이 {a[1]} 에 글자 그대로 있다")
        sys.exit(1 if miss else 0)
    tpl, out = a[0], a[1]
    variant = a[2] if len(a) > 2 else "si"
    assert variant in ("main", "si"), variant
    build(tpl, out, variant)
