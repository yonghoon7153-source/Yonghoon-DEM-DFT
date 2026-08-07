#!/usr/bin/env python3
"""extract_gap.py — nscf(fixed occupations) 출력에서 **VBM/CBM 고유값**으로 갭을 낸다.

⚠⚠ 이것이 갭의 **정본**이다. DOS 문턱으로 읽으면 Gaussian 퍼짐 때문에 ~0.3 eV
  과소평가된다 (CLAUDE.md 규율). DOS/PDOS 는 그림과 성분 분해 전용이다.

  VBM = max over k of  E(N/2 번째 밴드)
  CBM = min over k of  E(N/2+1 번째 밴드)
  gap = CBM − VBM   (≤ 0 이면 금속/반금속)

  python3 extract_gap.py --nscf 03_nscf_gap.out --tag li2o --json gap.json
"""
import argparse, json, re, sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nscf", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--json", required=True)
    a = ap.parse_args()
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
