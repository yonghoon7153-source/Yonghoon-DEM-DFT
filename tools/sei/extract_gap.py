#!/usr/bin/env python3
"""extract_gap.py — nscf(fixed occupations) 출력에서 **VBM/CBM 고유값**으로 갭을 낸다.

⚠⚠ 이것이 갭의 **정본**이다. DOS 문턱으로 읽으면 Gaussian 퍼짐 때문에 ~0.3 eV
  과소평가된다 (CLAUDE.md 규율). DOS/PDOS 는 그림과 성분 분해 전용이다.

  VBM = max over k of  E(N/2 번째 밴드)
  CBM = min over k of  E(N/2+1 번째 밴드)
  gap = CBM − VBM   (≤ 0 이면 금속/반금속)

  python3 extract_gap.py --nscf 03_nscf_gap.out --tag li2o --json gap.json

--control_gate (2026-10-27 · CEI 생성물 갭 카드 개정 1) — 대조 잡 판정
  다른 기계에서 다시 돈 기준 상의 gap.json 을 카드에 적힌 기준값과 견준다. 카드의
  `6_대조_잡_결과_전_문턱` 에서 기준값 · tol_eV · (있으면) 기준_nk 를 읽는다.
  통과 0 · 실패 3 · 입력 문제 2. 판정은 <work>/control_gate.json 에 남긴다.
  ⛔ 못 하는 것: 왜 어긋났는지는 모른다 (PP · 바이너리 · 생성기 · 이완 경로) — 멈출 뿐이다.
  python3 extract_gap.py --control_gate db/properties/cei_product_gap_card_2026_10_27.json --work <작업폴더>
  python3 extract_gap.py --selftest
"""
import argparse, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import electronic_class as EC          # noqa: E402  (금속/절연체 단일 출처)


def control_gate(card_path, work):
    """카드 §6 의 대조 잡 → (통과 bool, 줄 목록). 갭이 숫자가 아니거나 파일이 없으면 실패."""
    c = json.load(open(card_path, encoding="utf-8"))["6_대조_잡_결과_전_문턱"]
    ref, tol, nk_ref = c["기준값"], float(c["tol_eV"]), c.get("기준_nk") or {}
    rows, ok = [], bool(ref)
    for tag, g0 in ref.items():
        p = os.path.join(work, tag, "gap.json")
        row = {"tag": tag, "ref_eV": g0}
        if not os.path.isfile(p):
            row["verdict"] = "실패 — gap.json 없음"; ok = False; rows.append(row); continue
        g = json.load(open(p))
        gap = g.get("gap")
        if not isinstance(gap, (int, float)) or isinstance(gap, bool):
            row["verdict"] = f"실패 — 갭이 숫자가 아니다 ({g.get('verdict')})"; ok = False
            rows.append(row); continue
        d = gap - g0
        row.update({"gap_eV": round(gap, 4), "delta_eV": round(d, 4), "nk": g.get("nk")})
        bad = []
        if abs(d) > tol:
            bad.append(f"|Δ| {abs(d):.4f} > {tol}")
        if tag in nk_ref and g.get("nk") != nk_ref[tag]:
            bad.append(f"nk {g.get('nk')} ≠ {nk_ref[tag]}")
        row["verdict"] = "통과" if not bad else "실패 — " + " · ".join(bad)
        ok = ok and not bad
        rows.append(row)
    return ok, rows


def _selftest():
    import tempfile
    bad = []
    with tempfile.TemporaryDirectory() as T:
        card = os.path.join(T, "card.json")
        json.dump({"6_대조_잡_결과_전_문턱": {"기준값": {"a": 5.186, "b": 3.0}, "tol_eV": 0.02,
                                           "기준_nk": {"b": 10}}}, open(card, "w"))

        def put(tag, **g):
            os.makedirs(os.path.join(T, tag), exist_ok=True)
            json.dump(g, open(os.path.join(T, tag, "gap.json"), "w"))
        put("a", gap=5.19, nk=7); put("b", gap=3.01, nk=10)
        ok, rows = control_gate(card, T)
        if not ok:
            bad.append("둘 다 문턱 안인데 실패했다")
        put("a", gap=5.21, nk=7)
        if control_gate(card, T)[0]:
            bad.append("[음성] |Δ| 0.024 > 0.02 를 통과시켰다")
        put("a", gap=5.19, nk=7); put("b", gap=3.0, nk=11)
        if control_gate(card, T)[0]:
            bad.append("[음성] nk 11 ≠ 10 을 통과시켰다")
        put("b", gap=None, verdict="NOT_APPLICABLE(metal)", nk=10)
        if control_gate(card, T)[0]:
            bad.append("[음성] 갭 None 을 통과시켰다")
        os.remove(os.path.join(T, "b", "gap.json"))
        if control_gate(card, T)[0]:
            bad.append("[음성] gap.json 없음을 통과시켰다")
        json.dump({"6_대조_잡_결과_전_문턱": {"기준값": {}, "tol_eV": 0.02}}, open(card, "w"))
        if control_gate(card, T)[0]:
            bad.append("[음성] 기준값이 비었는데 통과시켰다")
    print("\n".join("⛔ " + b for b in bad) if bad else "✓ selftest 통과 (6 · 음성 5)")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nscf")
    ap.add_argument("--tag")
    ap.add_argument("--json")
    ap.add_argument("--control_gate", metavar="CARD")
    ap.add_argument("--work")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.control_gate:
        if not a.work:
            sys.exit("⛔ --control_gate 에는 --work 가 필요하다")
        ok, rows = control_gate(a.control_gate, a.work)
        for r in rows:
            print(f"  {r['tag']:22s} 기준 {r['ref_eV']:.4f} · 지금 {r.get('gap_eV', '—')} · "
                  f"Δ {r.get('delta_eV', '—')} · nk {r.get('nk', '—')} → {r['verdict']}")
        json.dump({"card": a.control_gate, "pass": ok, "rows": rows},
                  open(os.path.join(a.work, "control_gate.json"), "w"), ensure_ascii=False, indent=1)
        print(f"  대조 잡 {'✅ 통과' if ok else '⛔ 실패 — 새 상 값을 읽지 않는다'}")
        return 0 if ok else 3
    if not (a.nscf and a.tag and a.json):
        sys.exit("⛔ --nscf · --tag · --json 셋이 다 필요하다 (또는 --control_gate · --selftest)")
    # ★★ 2026-08-11 — 금속으로 선언된 상은 **갭을 db 에 쓰지 않는다.**
    #   fixed-occ nscf 는 금속에서도 숫자를 내는데, 그건 갭이 아니라
    #   'nelec/2 번째 밴드와 그 다음 밴드의 차' 다. 판정만 남기고 값은 null 로 둔다.
    ecls = EC.get(a.tag)
    if ecls.get("class") == "metal":
        print(f"  ⛔ {a.tag}: electronic_class=metal → 갭을 내지 않는다 (NOT_APPLICABLE). "
              f"금속엔 VBM/CBM 이 없다.")
        print(f"     근거: {ecls.get('evidence')} · {str(ecls.get('basis') or '')[:80]}")
        json.dump({"tag": a.tag, "gap": None, "verdict": "NOT_APPLICABLE(metal)",
                   "electronic_class": "metal",
                   "electronic_class_evidence": ecls.get("evidence"),
                   "reason": "금속에는 VBM/CBM 이 없다. fixed-occ nscf 가 내는 숫자는 "
                             "갭이 아니므로 db 에 등재하지 않는다.",
                   "registry": "db/properties/sei_electronic_class.json",
                   "method": "gap stage skipped by electronic_class registry"},
                  open(a.json, "w"), ensure_ascii=False, indent=2)
        return 0
    t = open(a.nscf, errors="ignore").read()

    m = re.search(r"number of electrons\s*=\s*([\d.]+)", t)
    if not m:
        sys.exit("⛔ number of electrons 를 못 읽었다")
    nelec = float(m.group(1))
    ms = re.search(r"number of Kohn-Sham states\s*=\s*(\d+)", t)
    nbnd = int(ms.group(1)) if ms else None
    # ⚠⚠ 스핀분극 계에서 `nocc = nelec` 은 틀렸다 (2026-08-07 Nd 재계산 준비 중 발견).
    #   nspin=2 는 두 스핀 채널이 **각자** 점유 밴드 수를 갖는다:
    #       nocc_up = (nelec + M)/2 ,  nocc_dn = (nelec − M)/2   (M = tot_magnetization)
    #   QE 출력은 `------ SPIN UP ------` 뒤에 전 k 점 블록, 그 다음 SPIN DOWN 이 온다.
    #   두 채널을 각자 nocc 로 읽고 VBM = max(양쪽), CBM = min(양쪽) 으로 합친다.
    #   (합치는 게 맞는 이유: 갭은 계 전체의 것이지 채널별이 아니다.)
    spin = "SPIN UP" in t
    mm = re.search(r"total magnetization\s*=\s*(-?[\d.]+)\s*Bohr mag/cell", t)
    magn = float(mm.group(1)) if mm else 0.0
    nocc_up = int(round((nelec + magn) / 2)) if spin else int(round(nelec / 2))
    nocc_dn = int(round((nelec - magn) / 2)) if spin else nocc_up
    nocc = nocc_up          # 아래 진단 출력·JSON 용 (스핀 없으면 nelec/2 그대로)

    # k 점별 밴드 블록
    # ⚠ 정규식으로 한 방에 잡으려다 실패했다(2026-08-06). QE 판·verbosity 에 따라
    #   "bands (ev):" 뒤 빈 줄 수와 들여쓰기가 달라진다. 형식에 안 휘둘리게
    #   **줄 단위로** 판다: 표식을 만나면 그 뒤로 '숫자만 있는 줄'을 계속 모은다.
    blocks, lines, i, chan = [], t.splitlines(), 0, 0   # chan: 0=up(또는 무스핀) · 1=down
    while i < len(lines):
        if "SPIN DOWN" in lines[i]:
            chan = 1
        if "bands (ev)" in lines[i]:
            i += 1
            vals = []
            while i < len(lines):
                ln = lines[i].strip()
                if not ln:
                    if vals:
                        break          # 값을 모은 뒤의 빈 줄 = 블록 끝
                    i += 1; continue   # 표식 직후의 빈 줄은 건너뛴다
                try:
                    vals += [float(x) for x in ln.split()]
                except ValueError:
                    break              # 숫자가 아닌 줄 = 블록 끝
                i += 1
            if vals:
                blocks.append((chan, vals))
        else:
            i += 1
    if not blocks:
        sys.exit("⛔ 밴드 블록을 못 찾았다 — scf.out 에 'bands (ev)' 가 있는지 확인할 것")
    vbm, cbm, short = -1e9, 1e9, 0
    for ch, e in blocks:
        no = nocc_dn if ch else nocc_up
        if no < 1 or len(e) < no + 1:
            short += 1
            continue
        vbm = max(vbm, e[no - 1])
        cbm = min(cbm, e[no])
    if vbm < -1e8 or cbm > 1e8:
        sys.exit("⛔ VBM/CBM 을 못 잡았다 — nbnd 가 점유 밴드보다 크지 않다. nbnd 를 늘릴 것.")
    if short:
        print(f"    ⚠ 밴드가 모자란 k 블록 {short}/{len(blocks)}개를 건너뛰었다 — nbnd 확인")
    gap = cbm - vbm
    verdict = ("금속/반금속 (겹침)" if gap <= 0.02 else
               "좁은 갭" if gap < 1.0 else "절연체")
    # ⚠⚠ 스핀분극 fixed-occ 에서 VBM 이 CBM 보다 **크게** 위면 그건 밴드 겹침이 아니라
    #   **점유수가 전하밀도와 어긋난 것**이다 (2026-08-07 nd2o3: −6.460 eV, VBM 16.159 >
    #   CBM 9.700). scf 는 모멘트를 자유롭게 찾는데 nscf 가 다른 tot_magnetization 을
    #   강제하면 정확히 이 꼴이 난다. 숫자를 그대로 내보내면 "반금속" 으로 오독된다.
    if spin and gap < -0.5:
        verdict = "⛔ 무효 — 스핀 점유수 불일치 (겹침 아님)"
        print(f"  ⛔ VBM 이 CBM 보다 {-gap:.3f} eV 위다. 물리적 겹침이 아니라 "
              f"↑/↓ 점유수가 전하밀도와 어긋난 것이다.")
        print(f"     02_scf.out 의 수렴 모멘트를 03 에 옮기고 다시 돌릴 것:")
        print(f"       python3 tools/sei/sync_magnetization.py <작업폴더>")
        print(f"       TAG=<tag> bash tools/sei/redo_stages.sh 03 04 05 06")
    print(f"  VBM {vbm:.3f} · CBM {cbm:.3f} · **gap {gap:.3f} eV** ({verdict})")
    print(f"    (전자 {nelec:.0f} · 점유 밴드 "
          + (f"↑{nocc_up}/↓{nocc_dn} (M={magn:.2f} μB)" if spin else str(nocc))
          + f" · nbnd {nbnd} · 블록 {len(blocks)}"
          + (" · spin-polarized" if spin else "") + ")")
    if nbnd and max(nocc_up, nocc_dn) >= nbnd:
        print("    ⚠ nbnd 가 점유 밴드 수와 같거나 작다 — CBM 을 못 봤다. nbnd 를 늘릴 것.")
    json.dump({"tag": a.tag, "vbm": vbm, "cbm": cbm, "gap": gap, "verdict": verdict,
               "nelec": nelec, "n_occ_bands": nocc, "nbnd": nbnd, "nk": len(blocks),
               "spin_polarized": spin, "total_magnetization_bohr": magn,
               "n_occ_up": nocc_up, "n_occ_dn": nocc_dn,
               "method": "fixed-occupation nscf eigenvalues (NOT DOS threshold)",
               "warning": "PBE gap; systematically 30-50% underestimated for wide-gap insulators"},
              open(a.json, "w"), ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
