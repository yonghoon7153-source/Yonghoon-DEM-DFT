#!/usr/bin/env python3
"""slab_mag_from_scfout.py — 수렴한 슬랩 scf.out → Ni1/Ni2 시드 (mag.json).

슬랩-우선(slab-first) 경로의 **1단계 → 2단계 연결부**다.

⚠⚠ **"밀도 승계"가 아니다.** 슬랩(96원자)과 복합체(130/131원자)는 nat/ntyp 이 달라
  QE 가 charge density 를 이어받지 못한다. 넘어가는 건 오직 **스칼라 시드값**
  (starting_magnetization) 이고, 그게 SCF 초기조건을 결정적으로 좋게 만든다.

⚠ QE 가 찍는 자기모멘트는 두 종류다:
    "Magnetic moment per site" 블록  → 원자별 (원하는 값)
    "total magnetization"           → 셀 전체 (AFM 이면 ~0, 시드로 못 씀)
  원자별 블록의 **마지막 출현**(= 수렴 스텝)만 읽는다. 중간 스텝을 읽으면
  아직 흔들리는 값을 시드로 굳혀 버린다.

⚠ ATOMIC_POSITIONS 의 종 라벨(Ni1/Ni2)은 scf.out 의 site 블록엔 없다 —
  입력의 종 순서로 매핑한다. 그래서 --scf_in 도 함께 받는다.

⚠⚠ **단위가 다르다.** scf.out 의 magn 은 **μB**, 반면 입력의 starting_magnetization 은
  **가전자당 분율 [-1, 1]** 이다. 1.62 를 그대로 넣으면 범위를 벗어나 QE 가 죽는다.
  그래서 frac = μB / ZVAL 로 바꿔 내보내고(클램프 포함), μB 원값도 같이 적어 둔다.
  관례상 AFM+U 는 과분극 출발(±0.3 = 3 μB 상당)이 안전하다고 알려져 있어서,
  승계값이 그보다 작으면 **크기는 관례값을 쓰고 부호만 승계**하는 게 기본이다
  (--use_converged_magnitude 로 끌 수 있다).

  python3 tools/sdcp/slab_mag_from_scfout.py \\
      --scf_out /data/work/runs/.../slab/scf.out \\
      --scf_in  /data/work/runs/.../slab/scf.in \\
      --out     /data/work/runs/.../slab_mag.json
"""
import argparse
import json
import re
from pathlib import Path

# 가전자 수 — pseudo 를 바꾸면 여기도 바꿔야 한다 (ni_pbe_v1.4.uspp.F.UPF = 10)
ZVAL = {"Ni1": 10.0, "Ni2": 10.0}
CONV_MAG = 0.3          # 관례 과분극 출발값 (분율)

SITE_HDR = re.compile(r"Magnetic moment per site")
SITE_ROW = re.compile(r"atom\s+(\d+)\s.*?magn=\s*(-?\d+\.\d+)", re.I)
CONV = re.compile(r"convergence has been achieved")


def species_of_atoms(scf_in: str):
    """ATOMIC_POSITIONS 의 종 라벨을 순서대로 — site 번호 ↔ Ni1/Ni2 매핑용."""
    lines = Path(scf_in).read_text(errors="ignore").splitlines()
    try:
        i = next(k for k, l in enumerate(lines) if l.strip().startswith("ATOMIC_POSITIONS"))
    except StopIteration:
        raise SystemExit("scf.in 에 ATOMIC_POSITIONS 가 없다")
    out = []
    for l in lines[i + 1:]:
        t = l.split()
        if len(t) < 4 or not re.match(r"^[A-Za-z][A-Za-z0-9]{0,2}$", t[0]):
            break
        out.append(t[0])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scf_out", required=True)
    ap.add_argument("--scf_in", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--zval", type=float, default=None,
                    help=f"Ni pseudo 의 가전자 수 (기본 {ZVAL['Ni1']:.0f}). "
                         "μB → starting_magnetization 분율 변환에 쓴다.")
    ap.add_argument("--use_converged_magnitude", action="store_true",
                    help="승계값의 크기까지 그대로 쓴다. 기본은 부호만 승계하고 크기는 "
                         f"관례 과분극값 {CONV_MAG} — AFM+U 는 크게 출발해 줄어드는 쪽이 "
                         "잘 붙는다.")
    a = ap.parse_args()
    if a.zval:
        ZVAL["Ni1"] = ZVAL["Ni2"] = a.zval

    txt = Path(a.scf_out).read_text(errors="ignore")
    converged = bool(CONV.search(txt))
    if not converged:
        print("⚠ 'convergence has been achieved' 가 없다 — 미수렴 출력이다.\n"
              "  (report=N 으로 찍힌 마지막 블록을 재시작 시드로 건지는 용도로는 정당 —\n"
              "   json 에 converged:false 로 남기니 받는 쪽이 알고 쓴다)")
    # 원자별 블록의 **마지막** 출현만
    starts = [m.start() for m in SITE_HDR.finditer(txt)]
    if not starts:
        raise SystemExit("'Magnetic moment per site' 블록이 없다 — nspin=2 였는지 확인")
    block = txt[starts[-1]: starts[-1] + 200 * 120]
    mags = {}
    for m in SITE_ROW.finditer(block):
        mags[int(m.group(1))] = float(m.group(2))
    if not mags:
        raise SystemExit("site 블록을 파싱 못 했다 — QE 판본별 서식 확인")

    sp = species_of_atoms(a.scf_in)
    if len(sp) != len(mags):
        print(f"⚠ 원자 수 불일치: scf.in {len(sp)} vs scf.out site {len(mags)} — "
              "앞에서부터 맞춘다")
    per = {}
    for idx, mv in sorted(mags.items()):
        if idx - 1 < len(sp):
            per.setdefault(sp[idx - 1], []).append(mv)

    seed = {}
    print("종별 수렴 모멘트 (μB):")
    for k, v in sorted(per.items()):
        mean = sum(v) / len(v)
        print(f"  {k:4s} n={len(v):3d}  mean {mean:+.3f}  "
              f"[{min(v):+.3f}, {max(v):+.3f}]")
        if k in ("Ni1", "Ni2"):
            frac = mean / ZVAL[k]
            if abs(frac) > 1.0:
                print(f"    ⚠ {k} 분율 {frac:+.3f} 가 [-1,1] 밖 — 클램프. ZVAL 확인.")
                frac = max(-1.0, min(1.0, frac))
            if not a.use_converged_magnitude and abs(frac) < CONV_MAG:
                print(f"    {k}: 분율 {frac:+.3f} → 부호만 승계, 크기는 관례 "
                      f"{CONV_MAG} 사용 (--use_converged_magnitude 로 끌 수 있음)")
                frac = CONV_MAG if frac >= 0 else -CONV_MAG
            seed[k] = round(frac, 3)
            seed[k + "_muB"] = round(mean, 3)

    if "Ni1" in seed and "Ni2" in seed:
        net = seed["Ni1_muB"] + seed["Ni2_muB"]
        print(f"\nAFM 대칭성 Ni1+Ni2 = {net:+.3f} μB "
              + ("✓ (±0.05 이내)" if abs(net) < 0.05 else
                 "⚠ 0.05 초과 — 부격자가 안 맞았다. 시드로 쓰기 전에 슬랩을 다시 본다."))
        # ⚠⚠ 리뷰 §2-3: 옛 판은 여기서 "⛔ 시드 금지" 를 **찍고도 파일을 쓰고 exit 0** —
        #   드라이버의 `|| exit 1` 이 안 걸려 FM 시드가 그대로 하류에 들어갔다. 게다가
        #   '부호만 승계' 정책이 FM 부호(+,+)를 관례 크기(+0.3,+0.3)로 **고정**해 버렸다.
        #   판정 도구는 판정을 남기되, 오염 산출물은 쓰지 않는다: 파일 없이 exit 1.
        if seed["Ni1"] * seed["Ni2"] > 0:
            raise SystemExit(
                "⛔ Ni1·Ni2 부호가 같다 — AFM 이 아니라 FM 으로 떨어진 슬랩이다.\n"
                "   이 값을 시드로 승계하면 FM 을 다음 계산에 **고정**하게 된다.\n"
                "   → json 을 쓰지 않고 종료한다(exit 1). 슬랩 SCF 부터 다시 볼 것\n"
                "     (U-ramp 2단계 + FSM: tools/sdcp/make_slab_relax.py 참조).")
    else:
        raise SystemExit("⛔ Ni1/Ni2 라벨을 못 찾았다 — 이 슬랩이 AFM 분할 입력이 맞는지 확인. "
                         "시드 없이 진행하면 관례값(±0.3)이 조용히 쓰인다 — 그건 받는 쪽에서 "
                         "명시적으로 선택할 일이다.")

    if a.out and seed:
        seed["converged"] = converged
        seed["source"] = str(a.scf_out)
        print(f"\n시드(분율, 입력에 그대로 들어감): "
              + " · ".join(f"{k} {seed[k]:+.3f}" for k in ("Ni1", "Ni2"))
              + ("" if converged else "   ⚠ converged:false — 재시작 시드 전용"))
        Path(a.out).write_text(json.dumps(seed, indent=2) + "\n")
        print(f"\n→ {a.out}   (다음 단계: --mag_json 로 넘긴다)")


if __name__ == "__main__":
    main()
