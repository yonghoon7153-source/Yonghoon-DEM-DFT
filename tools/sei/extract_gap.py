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


def gap_from_text(t, magn_hint=None):
    """QE nscf (fixed occupations) 출력 글자 → VBM/CBM/gap 과 판정. 못 읽으면 ValueError.

    ⛔⛔ 2026-10-29 고침 — 스핀분극에서 채널별 점유 밴드 수를 `total magnetization … Bohr mag/cell`
      줄에서만 읽고, **그 줄이 없으면 조용히 M = 0** 으로 셌다. 그 줄은 **scf 출력에만** 찍히고
      nscf 출력에는 없다. 그래서 스핀분극 nscf 는 늘 두 채널 다 nelec/2 로 읽혀 ↓ 채널의 빈 밴드를
      VBM 으로, ↑ 채널의 찬 밴드를 CBM 으로 잡았다 → 큰 음수 '갭' (NiP2O6 −4.894 eV · 10-29 kgy).
      아래 −0.5 eV 게이트가 숫자를 막았지만 원인을 '점유수가 밀도와 어긋남' 으로 잘못 짚었다.
      ⇒ 순서: ① 머리말의 `number of electrons = N (up: a, down: b)` (tot_magnetization 을 준 계산이
         찍는다) ② 없으면 scf 의 **마지막** `total magnetization` ③ 스핀분극인데 둘 다 없으면 **멈춘다**.
      ⇒ 대조: QE 가 스스로 찍는 `highest occupied, lowest unoccupied level` 과 0.002 eV 안에서 같아야
         한다 (QE 도 같은 채널별 점유수로 센다). 어긋나면 이 도구의 해석이 틀린 것이라 무효로 둔다.
    ⛔⛔ 2026-10-30 덧붙임 (kgy NiP2O6 실측) — nscf 는 점유 설정을 **scf 저장본에서 다시 읽는다**. scf 가 smearing ·
      자유 모멘트였으면 nscf 입력의 tot_magnetization 은 먹지 않고 (머리말에 up/down 이 없다) 두 채널을 nelec/2 씩
      채운다 — QE 가 찍는 HOMO/LUMO 줄도 그 점유로 센 것이라 **대조 기준이 못 된다** (NiP2O6: 8.4891 > 3.5953).
      고유값은 멀쩡하다 (nscf 는 scf 의 스핀 밀도로 만든 퍼텐셜을 그대로 쓴다) — 틀린 것은 '몇 번째 밴드까지 찼나' 뿐이다.
      ⇒ 머리말 up/down 도 total magnetization 도 없으면 magn_hint (02_scf 의 수렴 모멘트 · 03 입력의 tot_magnetization 과
         맞춘 값 · main 의 spin_hint_from_dir) 로 채널별 점유를 정한다. 그 경우 QE HOMO/LUMO 대조는 하지 않는다 (M=0 점유라서).
    ⛔ 못 하는 것: 스핀분극 계에서 '이 M 이 바닥상태인가' 는 모른다 — 주어진 점유수의 갭만 낸다.
    """
    notes = []
    m = re.search(r"number of electrons\s*=\s*([\d.]+)", t)
    if not m:
        raise ValueError("number of electrons 를 못 읽었다")
    nelec = float(m.group(1))
    ms = re.search(r"number of Kohn-Sham states\s*=\s*(\d+)", t)
    nbnd = int(ms.group(1)) if ms else None
    # nspin=2 는 두 스핀 채널이 **각자** 점유 밴드 수를 갖는다 (nocc_up = (nelec+M)/2 · nocc_dn = (nelec−M)/2).
    #   QE 출력은 `------ SPIN UP ------` 뒤에 전 k 점 블록, 그 다음 SPIN DOWN 이 온다.
    #   두 채널을 각자 nocc 로 읽고 VBM = max(양쪽), CBM = min(양쪽) 으로 합친다 (갭은 계 전체의 것).
    spin = "SPIN UP" in t
    ud = re.search(r"number of electrons\s*=\s*[\d.]+\s*\(up:\s*([\d.]+),\s*down:\s*([\d.]+)\)", t)
    mags = re.findall(r"total magnetization\s*=\s*(-?[\d.]+)\s*Bohr mag/cell", t)
    if not spin:
        nocc_up = nocc_dn = int(round(nelec / 2)); magn = 0.0; src = "no spin"
    elif ud:
        nocc_up, nocc_dn = int(round(float(ud.group(1)))), int(round(float(ud.group(2))))
        magn = float(ud.group(1)) - float(ud.group(2)); src = "header up/down"
    elif mags:
        magn = float(mags[-1])
        nocc_up = int(round((nelec + magn) / 2)); nocc_dn = int(round((nelec - magn) / 2))
        src = "last total magnetization"
    elif magn_hint is not None:
        magn = float(magn_hint)
        nocc_up = int(round((nelec + magn) / 2)); nocc_dn = int(round((nelec - magn) / 2))
        src = "02_scf converged moment (nscf kept M=0 filling)"
    else:
        raise ValueError("스핀분극인데 채널별 전자 수를 못 읽었다 (머리말 up/down · total magnetization 둘 다 없음) "
                         "— M = 0 으로 가정하지 않는다")

    # k 점별 밴드 블록 — 줄 단위로 판다 (QE 판 · verbosity 에 따라 빈 줄 · 들여쓰기가 달라진다)
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
                        break
                    i += 1; continue
                try:
                    vals += [float(x) for x in ln.split()]
                except ValueError:
                    break
                i += 1
            if vals:
                blocks.append((chan, vals))
        else:
            i += 1
    if not blocks:
        raise ValueError("밴드 블록을 못 찾았다 — 출력에 'bands (ev)' 가 있는지 확인할 것")
    vbm, cbm, short = -1e9, 1e9, 0
    edge = {0: [-1e9, 1e9], 1: [-1e9, 1e9]}          # 채널별 (VBM, CBM) — 진단용
    for ch, e in blocks:
        no = nocc_dn if ch else nocc_up
        if no < 1 or len(e) < no + 1:
            short += 1
            continue
        vbm = max(vbm, e[no - 1])
        cbm = min(cbm, e[no])
        edge[ch][0] = max(edge[ch][0], e[no - 1]); edge[ch][1] = min(edge[ch][1], e[no])
    if vbm < -1e8 or cbm > 1e8:
        raise ValueError("VBM/CBM 을 못 잡았다 — nbnd 가 점유 밴드보다 크지 않다. nbnd 를 늘릴 것.")
    if short:
        notes.append(f"    ⚠ 밴드가 모자란 k 블록 {short}/{len(blocks)}개를 건너뛰었다 — nbnd 확인")
    gap = cbm - vbm
    verdict = ("금속/반금속 (겹침)" if gap <= 0.02 else
               "좁은 갭" if gap < 1.0 else "절연체")
    # QE 자신의 HOMO/LUMO 줄 (fixed occupations 에서 찍힌다) 과 대조
    qe = re.findall(r"highest occupied, lowest unoccupied level \(ev\):\s*(-?[\d.]+)\s+(-?[\d.]+)", t)
    qe_h = qe_l = None
    qe_check = "QE 줄 없음"
    if qe and src.startswith("02_scf"):
        qe_h, qe_l = float(qe[-1][0]), float(qe[-1][1])
        qe_check = "QE 줄은 M=0 점유라 대조 안 함"
    elif qe:
        qe_h, qe_l = float(qe[-1][0]), float(qe[-1][1])
        if abs(vbm - qe_h) <= 0.002 and abs(cbm - qe_l) <= 0.002:
            qe_check = "일치"
        else:
            qe_check = f"어긋남 (QE {qe_h:.4f}/{qe_l:.4f} · 여기 {vbm:.4f}/{cbm:.4f})"
            verdict = "⛔ 무효 — QE 자체 HOMO/LUMO 와 어긋남 (점유수 해석 오류)"
            notes.append(f"  ⛔ QE 가 찍은 HOMO/LUMO 와 다르다: {qe_check}")
    if spin and gap < -0.5 and not verdict.startswith("⛔"):
        # 점유수를 바로 읽고도 VBM 이 CBM 보다 크게 위면, 주어진 tot_magnetization 이 그 밀도와 안 맞는 것이다
        verdict = "⛔ 무효 — 스핀 점유수 불일치 (겹침 아님)"
        notes.append(f"  ⛔ VBM 이 CBM 보다 {-gap:.3f} eV 위다 (점유수 출처: {src}). 02_scf 의 수렴 모멘트와 "
                     f"03 의 tot_magnetization 이 같은지 본다: python3 tools/sei/sync_magnetization.py <작업폴더>")
    if nbnd and max(nocc_up, nocc_dn) >= nbnd:
        notes.append("    ⚠ nbnd 가 점유 밴드 수와 같거나 작다 — CBM 을 못 봤다. nbnd 를 늘릴 것.")
    return {"vbm": vbm, "cbm": cbm, "gap": gap, "verdict": verdict, "nelec": nelec,
            "nbnd": nbnd, "nk": len(blocks), "spin_polarized": spin,
            "total_magnetization_bohr": magn, "n_occ_up": nocc_up, "n_occ_dn": nocc_dn,
            "occ_source": src, "qe_homo": qe_h, "qe_lumo": qe_l, "qe_check": qe_check,
            "edges_by_spin": ({"up": [round(edge[0][0], 4), round(edge[0][1], 4)],
                               "down": [round(edge[1][0], 4), round(edge[1][1], 4)]} if spin else None),
            "notes": notes}


def spin_hint_from_dir(d):
    """03 nscf 옆의 02_scf.out (끝난 scf 의 **마지막** total magnetization) 과 03_nscf_gap.in 의 tot_magnetization.

    둘 다 있고 |M_scf − tot_mag| ≤ 0.2 면 tot_mag (정수) 를 준다 · 02 가 안 끝났거나 없으면 None ·
    어긋나면 ValueError (sync_magnetization 이 안 돌았거나 scf 가 다른 모멘트로 갔다 — 갭을 내지 않는다).
    """
    scf, inp = os.path.join(d, "02_scf.out"), os.path.join(d, "03_nscf_gap.in")
    if not (os.path.isfile(scf) and os.path.isfile(inp)):
        return None
    t = open(scf, errors="ignore").read()
    if "JOB DONE" not in t:
        return None
    mv = re.findall(r"total magnetization\s*=\s*(-?[\d.]+)\s*Bohr mag/cell", t)
    tm = re.search(r"tot_magnetization\s*=\s*(-?[\d.]+)", open(inp, errors="ignore").read())
    if not mv or not tm:
        return None
    m_scf, m_in = float(mv[-1]), float(tm.group(1))
    if abs(m_scf - m_in) > 0.2:
        raise ValueError(f"02_scf 수렴 모멘트 {m_scf:.3f} 와 03 입력 tot_magnetization {m_in:g} 가 어긋난다 (> 0.2 μB)")
    return m_in


def _qe_text(spin, header, blocks_up, blocks_dn=None, qe_line=None, mags=()):
    """selftest 용 가짜 QE 출력."""
    L = [header, "     number of Kohn-Sham states=            8"]
    L += [f"     total magnetization       =     {m:.2f} Bohr mag/cell" for m in mags]
    L.append("     End of band structure calculation")
    if spin:
        L.append(" ------ SPIN UP ------------")
    for b in blocks_up:
        L += ["", "          k = 0.0000 0.0000 0.0000 (  100 PWs)   bands (ev):", "",
              "   " + "  ".join(f"{x:8.4f}" for x in b), ""]
    if spin:
        L.append(" ------ SPIN DOWN ----------")
        for b in blocks_dn:
            L += ["", "          k = 0.0000 0.0000 0.0000 (  100 PWs)   bands (ev):", "",
                  "   " + "  ".join(f"{x:8.4f}" for x in b), ""]
    if qe_line:
        L.append(f"     highest occupied, lowest unoccupied level (ev):    {qe_line[0]:.4f}   {qe_line[1]:.4f}")
    return "\n".join(L) + "\n"


def _selftest_bands():
    """띠 읽기 — 스핀분극 nscf (total magnetization 줄 없음) 가 핵심이다 (2026-10-29 NiP2O6)."""
    bad = []
    up = [[-6, -5, -4, -1, 3, 4], [-6, -5, -4, -1.2, 3.5, 4]]
    dn = [[-6, -5, 1, 2, 5, 6], [-6, -5, 1.2, 2, 5, 6]]
    hdr_ud = "     number of electrons       =         6.00 (up:   4.00, down:   2.00)"
    # ① 무스핀 — nelec 4 → 2 개 점유
    r = gap_from_text(_qe_text(False, "     number of electrons       =         4.00",
                               [[-5, -1, 2, 3], [-4.5, -0.5, 2.5, 3.5]], qe_line=(-0.5, 2.0)))
    if abs(r["gap"] - 2.5) > 1e-9 or r["qe_check"] != "일치":
        bad.append(f"무스핀 갭 {r['gap']} · {r['qe_check']}")
    # ② 스핀분극 nscf — 머리말 up/down 만 있고 total magnetization 줄 없음 (실제 nscf 출력 꼴)
    r = gap_from_text(_qe_text(True, hdr_ud, up, dn, qe_line=(-1.0, 1.0)))
    if abs(r["gap"] - 2.0) > 1e-9 or r["occ_source"] != "header up/down" or r["qe_check"] != "일치":
        bad.append(f"[실측회귀] 스핀 nscf 갭 {r['gap']} ({r['occ_source']} · {r['qe_check']}) — 2.0 이어야 한다")
    # ③ [음성] 스핀분극인데 채널별 전자 수 정보가 없다 → 멈춰야 한다 (M = 0 가정 금지)
    try:
        gap_from_text(_qe_text(True, "     number of electrons       =         6.00", up, dn))
        bad.append("[음성] 채널 정보 없이 숫자를 냈다 (M = 0 가정)")
    except ValueError:
        pass
    # ④ [음성] QE 자체 HOMO/LUMO 와 어긋나면 무효
    r = gap_from_text(_qe_text(True, hdr_ud, up, dn, qe_line=(-1.0, 3.0)))
    if not r["verdict"].startswith("⛔"):
        bad.append(f"[음성] QE 줄과 어긋났는데 판정이 {r['verdict']}")
    # ②b [실측회귀 10-30] nscf 가 M=0 으로 채운 꼴 — 머리말 up/down 없음 · QE 줄도 3/3 점유값 (1.2 / −1.2)
    #     02_scf 의 모멘트 2 를 힌트로 주면 4/2 점유로 갭 2.0 이 나와야 하고, QE 줄 때문에 무효로 만들면 안 된다
    r = gap_from_text(_qe_text(True, "     number of electrons       =         6.00", up, dn, qe_line=(1.2, -1.2)),
                      magn_hint=2.0)
    if abs(r["gap"] - 2.0) > 1e-9 or not r["occ_source"].startswith("02_scf") or r["verdict"].startswith("⛔"):
        bad.append(f"[실측회귀] M=0 채움 nscf + 02 힌트: 갭 {r['gap']} · {r['occ_source']} · {r['verdict']}")
    # ②c spin_hint_from_dir — 끝난 02 · 맞는 03 입력 → 정수 · 안 끝난 02 → None · 어긋남 → ValueError
    import tempfile as _tf
    with _tf.TemporaryDirectory() as D:
        def _w(n, s_):
            open(os.path.join(D, n), "w").write(s_)
        _w("02_scf.out", "     total magnetization       =     0.50 Bohr mag/cell\n"
                         "     total magnetization       =     8.00 Bohr mag/cell\n   JOB DONE.\n")
        _w("03_nscf_gap.in", "    tot_magnetization = 8\n")
        if spin_hint_from_dir(D) != 8.0:
            bad.append(f"spin_hint_from_dir 정상 경우 {spin_hint_from_dir(D)}")
        _w("02_scf.out", "     total magnetization       =     8.00 Bohr mag/cell\n")
        if spin_hint_from_dir(D) is not None:
            bad.append("[음성] 안 끝난 02_scf 의 모멘트를 썼다")
        _w("02_scf.out", "     total magnetization       =     7.40 Bohr mag/cell\n   JOB DONE.\n")
        try:
            spin_hint_from_dir(D); bad.append("[음성] 02 (7.40) 와 03 (8) 이 어긋났는데 힌트를 줬다")
        except ValueError:
            pass
    # ⑤ scf 꼴 — 반복마다 찍힌 total magnetization 중 **마지막** 을 쓴다 (첫 줄 0.50 은 미수렴 값)
    r = gap_from_text(_qe_text(True, "     number of electrons       =         6.00", up, dn,
                               mags=(0.50, 1.80, 2.00)))
    if (r["n_occ_up"], r["n_occ_dn"]) != (4, 2):
        bad.append(f"[음성] 첫 total magnetization 을 썼다 (점유 {r['n_occ_up']}/{r['n_occ_dn']})")
    return bad


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
    bad += _selftest_bands()
    print("\n".join("⛔ " + b for b in bad) if bad else "✓ selftest 통과 (대조 잡 6 · 음성 5 · 띠 읽기 8 · 음성 5)")
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
    try:
        hint = spin_hint_from_dir(os.path.dirname(os.path.abspath(a.nscf))) if "SPIN UP" in t else None
        r = gap_from_text(t, magn_hint=hint)
    except ValueError as e:
        sys.exit(f"⛔ {e}")
    for msg in r["notes"]:
        print(msg)
    print(f"  VBM {r['vbm']:.3f} · CBM {r['cbm']:.3f} · **gap {r['gap']:.3f} eV** ({r['verdict']})")
    print(f"    (전자 {r['nelec']:.0f} · 점유 밴드 "
          + (f"↑{r['n_occ_up']}/↓{r['n_occ_dn']} (M={r['total_magnetization_bohr']:.2f} μB · {r['occ_source']})"
             if r["spin_polarized"] else str(r["n_occ_up"]))
          + f" · nbnd {r['nbnd']} · 블록 {r['nk']}"
          + (" · spin-polarized" if r["spin_polarized"] else "") + ")")
    out = {"tag": a.tag}
    out.update({k: v for k, v in r.items() if k != "notes"})
    out.update({"n_occ_bands": r["n_occ_up"],
                "method": "fixed-occupation nscf eigenvalues (NOT DOS threshold)",
                "warning": "PBE gap; systematically 30-50% underestimated for wide-gap insulators"})
    json.dump(out, open(a.json, "w"), ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
