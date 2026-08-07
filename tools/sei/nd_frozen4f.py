#!/usr/bin/env python3
"""nd_frozen4f.py — Nd 갭을 **우리 손으로** 내기 위한 frozen-4f 경로의 0·1단계 도구.

왜 하나 (2026-08-07)
  Nd 상의 갭을 우리 계산으로 못 냈다. 원인은 확정됐다 — 4f 를 원자가에 둔 PBE(+U) 의
  SCF 해가 **금속**이라 fixed-occ 갭이라는 양 자체가 성립하지 않는다
  (kb/projects/sei_products_2026_08_06.md §진단이 끝났다).

  그래서 "MP frozen-4f 인용" 으로 종결했는데, **그 결론만 남기면 재현 경로가 없다.**
  게다가 이건 숫자 하나짜리 문제가 아니다 — repo 안에서 Nd 갭이 필요한 상이 최소 7종이다:
    NdPO₄ · NdOCl · NdCl₃ · LiNdO₂ · Nd₂O₃ · Nd₂S₃ · NdS  (tools/figures/plot_nd_sei_gaps.py)
  여기에 Nd₂O₃@LPSCl1.6 도핑 라인, cascade Nd 후보, nd_icohp 가 얹힌다.
  → **Nd 축 전체**가 남의 DB 에 의존하고 있다. PP 하나를 확보하면 다 살아난다.

핵심 판별 기준 — **z_valence**
  Nd 는 [Xe]4f⁴6s² 이고 화합물에서는 Nd³⁺(4f³) 이다.
    · 4f 를 원자가에 두면  → z_valence ≈ 14   (지금 우리 것: Nd.paw.z_14.atompaw…)
    · 4f 를 core 에 고정하면 → z_valence ≈ 11   (5s²5p⁶6s²5d⁰. VASP 의 `Nd_3` 가 이것)
  MP 가 쓰는 게 후자다. 그래서 이 도구는 **z_valence 로 PP 를 분류**한다.

  python3 tools/sei/nd_frozen4f.py --inventory        # 0단계: 가진 PP 를 분류한다
  python3 tools/sei/nd_frozen4f.py --check <파일>     # 받아 온 후보 하나를 판별한다
  python3 tools/sei/nd_frozen4f.py --reference        # 검증 표적(MP 갭)을 받아 둔다
  python3 tools/sei/nd_frozen4f.py --plan             # 단계별 계획·비용·중단 기준
"""
import argparse
import glob
import json
import os
import re
import sys

# z_valence 로 판별한다. 경계는 넉넉히 — 다른 관례(반코어 포함 등)를 놓치지 않게.
Z_FROZEN = (10.0, 12.5)      # frozen-4f (Nd³⁺: 5s5p6s5d) 기대 구간
Z_VALENCE_4F = (13.0, 16.0)  # 4f-in-valence 기대 구간
OUT = "db/properties/nd_gap_reference_mp.json"
# repo 안에서 Nd 갭이 필요한 상 (frozen-4f 가 생기면 전부 우리 값으로 바뀔 수 있는 것들)
ND_PHASES = ["Nd2O3", "Nd2S3", "LiNdO2", "NdPO4", "NdOCl", "NdCl3", "NdS"]
# ⚠⚠ **검증 표적은 "MP 에서 제일 안정한 것" 이 아니라 "우리가 계산할 바로 그 구조" 다.**
#   (2026-08-07 실측) 조성만으로 고르면 Nd₂O₃ 가 mp-1045(Ia-3, 40원자)로 잡히는데,
#   우리 db/structures 의 실물은 mp-2763(5원자)이다. 다형체가 다르면 갭도 다르므로
#   그대로 두면 **다른 구조끼리 비교**하게 된다 — 표적이 아니라 오답지가 된다.
#   → db/structures/sei_*.vasp 에 실물이 있는 상은 그 ID 로 **고정**한다.
PINNED = {"Nd2O3": "mp-2763", "Nd2S3": "mp-438", "LiNdO2": "mp-1222355"}
PSEUDO_DIRS = ["/data/work/pseudo",
               "/scratch/x3430a02/kgy/manuscript_support/pseudo",
               os.path.expanduser("~/pseudo")]


def zval(p):
    try:
        t = open(p, errors="ignore").read(400000)
    except OSError:
        return None
    m = re.search(r'z_valence\s*=\s*"?\s*([\d.eE+-]+)', t, re.I) \
        or re.search(r"([\d.eE+-]+)\s+Z valence", t, re.I)
    return float(m.group(1)) if m else None


def classify(z):
    if z is None:
        return "?", "z_valence 를 못 읽었다"
    if Z_FROZEN[0] <= z <= Z_FROZEN[1]:
        return "frozen-4f", "★ 4f 가 core 에 있다 — 우리가 찾던 것"
    if Z_VALENCE_4F[0] <= z <= Z_VALENCE_4F[1]:
        return "4f-in-valence", "⛔ 지금 쓰는 것과 같은 계열 — 갭이 정의 안 된다"
    return "unknown", f"기대 구간 밖(z={z}) — 직접 확인할 것"


def would_pick(hits):
    """⚠⚠ build_dft_inputs.find_pseudos() 의 선택 규칙을 그대로 재현한 것.

    거기는 `for f in sorted(os.listdir(pdir)): out.setdefault(el, f)` 다 —
    즉 **파일명 알파벳 순 첫 번째가 이긴다.** 조용히.

    이게 왜 함정이냐: 새 frozen-4f 를 같은 디렉터리에 넣기만 하면 끝날 것 같지만,
    지금 있는 `Nd.paw.z_14…` 와 새 `Nd.pbe-…` 가 같이 있으면 "paw" < "pbe" 라
    **옛날 4f-in-valence 가 이긴다.** 그러면 1단계를 통째로 다시 태우고 똑같은
    금속 해를 받는다. 그래서 0단계에서 '실제로 뽑힐 파일' 을 눈에 보이게 찍는다.
    """
    return sorted(hits, key=os.path.basename)[0] if hits else None


def inventory(dirs):
    print("═" * 74)
    print("0단계 — 가진 Nd pseudopotential 분류  (판별 기준: z_valence)")
    print(f"  frozen-4f 기대 {Z_FROZEN[0]}–{Z_FROZEN[1]} · 4f-in-valence 기대 "
          f"{Z_VALENCE_4F[0]}–{Z_VALENCE_4F[1]}")
    print("═" * 74)
    found, any_frozen, ndirs, warn = 0, False, 0, []
    for d in dirs:
        if not os.path.isdir(d):
            print(f"  ⏭ {d} — 이 머신엔 없음")
            continue
        ndirs += 1
        hits = sorted(set(glob.glob(os.path.join(d, "[Nn]d*.[uU][pP][fF]")) +
                          glob.glob(os.path.join(d, "[Nn]d*.upf"))))
        if not hits:
            print(f"  · {d} — Nd PP 없음")
            continue
        print(f"  · {d}")
        pick = would_pick(hits)
        for h in hits:
            z = zval(h)
            kind, why = classify(z)
            any_frozen |= kind == "frozen-4f"
            found += 1
            mark = "◀ 실제로 뽑힘" if h == pick else ""
            print(f"      {os.path.basename(h):52s} z={str(z):>6s}  {kind:14s} "
                  f"{why} {mark}")
        # ★ 여기가 이 도구의 핵심 경고다 — 위 would_pick docstring 참조.
        if len(hits) > 1 and classify(zval(pick))[0] != "frozen-4f":
            warn.append((d, os.path.basename(pick)))
    print()
    for d, p in warn:
        print(f"⛔⛔ {d} 에 Nd UPF 가 여러 개인데 **뽑히는 건 {p}** (frozen-4f 아님).")
        print("    build_dft_inputs 는 알파벳 첫 번째를 조용히 고른다 → 옛 PP 로 그대로 돈다.")
        print("    → 쓰지 않을 UPF 는 디렉터리 밖으로 **옮기고**(지우지 말고) 다시 확인할 것.")
    if warn:
        print()
    if any_frozen and not warn:
        print("✅ frozen-4f 후보가 있다 → **1단계(검증)** 로 간다. 아래 --plan 참조.")
    elif any_frozen:
        print("⚠ frozen-4f 는 있는데 선택 규칙에 걸린다 — 위 경고부터 해소할 것.")
    elif found:
        print("⛔ 전부 4f-in-valence 다 → 확보 경로 A/B/C 중 고른다 (--plan).")
    elif ndirs:
        print("⛔ Nd PP 를 하나도 못 찾았다 — 경로를 먼저 확인할 것.")
    else:
        print("⏭ pseudo 디렉터리가 이 머신에 없다 — **gabia/KISTI 에서 돌려야 한다.**")
        print("   (--pseudo_dirs 로 경로를 직접 줄 수도 있다)")
    return any_frozen and not warn


def check(paths):
    """받아 온 후보 UPF 하나(들)를 설치 전에 판별한다 — 경로 A 의 필수 단계.

    ⚠ **없는 파일과 못 읽은 z_valence 를 구분한다 (2026-08-07 실측).** zval() 은
      OSError 를 삼키고 None 을 주므로, 경로 오타를 'frozen-4f 가 아니다' 로 오인
      보고했다. 없는 건 없다고 말해야 한다 — 측정 실패로 위장시키면 안 된다.
    """
    ok, missing = False, 0
    for p in paths:
        if not os.path.isfile(p):
            missing += 1
            print(f"  {p}")
            print(f"      ⛔ **파일이 없다** — 판정 아님. 경로를 확인할 것"
                  + ("  (‘/경로/후보.UPF’ 는 예시 자리표시자다)" if "경로" in p else ""))
            continue
        z = zval(p)
        kind, why = classify(z)
        ok |= kind == "frozen-4f"
        print(f"  {os.path.basename(p):52s} z={str(z):>6s}  {kind:14s} {why}")
    if missing == len(paths):
        print("\n⛔ 판정할 파일이 하나도 없었다. (frozen-4f 여부를 말한 게 아니다)")
        return False
    if ok:
        print("\n✅ frozen-4f 다. pseudo 디렉터리에 넣은 뒤 **--inventory 로 다시** 확인할 것")
        print("   — 넣는 것만으로는 부족하다(알파벳 선택 규칙).")
    else:
        print("\n⛔ frozen-4f 가 아니다 — 이걸로는 지금과 같은 금속 해가 나온다.")
    return ok


def reference(api_key):
    """검증 표적 — MP 의 Nd 상 밴드갭. **이걸 재현해야 우리 값이 믿을 만하다.**

    ⚠ MP 값은 우리 계산이 아니다. 지금은 이걸 '인용' 하고 있지만, frozen-4f 로 우리가
      계산하면 **같은 방법 계열**(4f in core)이라 재현되어야 정상이다. 재현이 안 되면
      우리 설정에 문제가 있는 것이므로, 이 표가 1단계의 합격/불합격 기준이 된다.
    """
    from mp_api.client import MPRester
    fields = ["material_id", "formula_pretty", "symmetry", "band_gap",
              "energy_above_hull", "theoretical", "nsites"]
    out = {}
    with MPRester(api_key) as m:
        for f in ND_PHASES:
            docs = m.materials.summary.search(formula=f, fields=fields)
            if not docs:
                print(f"  ⏭ {f}: MP 에 없음")
                continue
            docs = sorted(docs, key=lambda d: 9e9 if d.energy_above_hull is None
                          else d.energy_above_hull)
            obs = [d for d in docs if not d.theoretical] or docs
            stable = obs[0]
            # ★ 우리 실물이 있는 상은 그 ID 로 고정한다 (PINNED 주석 참조).
            pin = PINNED.get(f)
            b = next((d for d in docs if d.material_id == pin), None) if pin else None
            if pin and b is None:
                print(f"  ⛔ {f}: 고정 ID {pin} 를 MP 조회 결과에서 못 찾았다 — "
                      f"가장 안정한 것으로 대체하되 **검증 표적으로 쓰지 말 것**")
            b = b or stable
            out[f] = {"material_id": b.material_id, "spacegroup": b.symmetry.symbol,
                      "band_gap_eV": b.band_gap, "nsites": b.nsites,
                      "e_above_hull": b.energy_above_hull,
                      "theoretical": bool(b.theoretical),
                      "pinned_to_our_structure": bool(pin and b.material_id == pin)}
            mark = " ★고정" if out[f]["pinned_to_our_structure"] else ""
            print(f"  {f:9s} {b.material_id:14s} {b.symmetry.symbol:12s} "
                  f"gap {b.band_gap:6.3f} eV  {b.nsites:3d}원자  "
                  + ("⚠ 예측만" if b.theoretical else "✅ 관측") + mark)
            # ⚠ 고정한 것이 MP 최안정과 다르면 **그 사실 자체를 남긴다.** 우리 계는
            #   준안정 다형체일 수 있고, 그러면 "MP 값과 다르다" 가 오류가 아니라 정보다.
            if b.material_id != stable.material_id:
                out[f]["mp_most_stable"] = {
                    "material_id": stable.material_id, "spacegroup": stable.symmetry.symbol,
                    "band_gap_eV": stable.band_gap, "nsites": stable.nsites,
                    "e_above_hull": stable.energy_above_hull}
                print(f"    ↳ ⚠ MP 최안정은 {stable.material_id} ({stable.symmetry.symbol}, "
                      f"{stable.nsites}원자, gap {stable.band_gap:.3f}) — **다형체가 다르다**")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({
        "property": "nd_gap_reference_mp",
        "purpose": ("frozen-4f 재계산의 **검증 표적**. 우리 값이 이 표를 재현해야 설정이 맞다. "
                    "재현되면 우리 계산으로 대체하고, 안 되면 원인을 찾을 때까지 MP 를 인용한다."),
        "warning": ("⚠ MP 는 VASP PAW `Nd_3`(frozen-4f, 11 valence) + PBE(+U) 다. "
                    "우리 QE 계산과 **범함수·PP 계열이 달라 완전 일치는 기대하지 않는다** — "
                    "판정 기준은 '같은 자릿수·같은 순위' 다. "
                    "⛔ 이 값을 우리 db 갭 표에 섞어 넣지 말 것 (문헌·db 분리 규율)."),
        "phases": out,
    }, open(OUT, "w"), ensure_ascii=False, indent=2)
    print(f"\n→ {OUT}")
    return out


def polymorphs(api_key, phases=None):
    """조성별로 **모든** MP 항목을 찍는다 — 하드코딩 값이 어느 다형체에서 왔는지 가린다.

    왜 (2026-08-07): `plot_nd_sei_gaps.py` 의 하드코딩 7종 중 2종이 고정 ID 조회와
    안 맞았다(Nd₂S₃ 1.79 vs mp-438 0.760, NdPO₄ 5.55 vs mp-3584 5.679). 그 파일은
    material_id 를 안 남겼으므로, **형제 다형체 중에 그 값이 있는지**가 유일한 단서다.
      · 있으면 → 다형체 선택이 달랐던 것. ID 를 박고 어느 쪽을 쓸지 정하면 끝난다.
      · 없으면 → 그 숫자의 출처가 MP 가 아니다. 그건 더 큰 문제고 따로 추적해야 한다.
    """
    from mp_api.client import MPRester
    fields = ["material_id", "formula_pretty", "symmetry", "band_gap",
              "energy_above_hull", "theoretical", "nsites"]
    # 하드코딩 값(그림) — 일치하는 다형체가 있으면 표시한다
    HARD = {"Nd2O3": 3.81, "Nd2S3": 1.79, "LiNdO2": 4.21, "NdPO4": 5.55,
            "NdOCl": 4.77, "NdCl3": 4.30, "NdS": 0.00}
    out = {}
    with MPRester(api_key) as m:
        for f in (phases or ND_PHASES):
            docs = m.materials.summary.search(formula=f, fields=fields)
            if not docs:
                print(f"  ⏭ {f}: MP 에 없음")
                continue
            docs = sorted(docs, key=lambda d: 9e9 if d.energy_above_hull is None
                          else d.energy_above_hull)
            tgt = HARD.get(f)
            print(f"\n  ══ {f}  (다형체 {len(docs)}개, e_above_hull 오름차순) "
                  f"— 그림 하드코딩 {tgt}")
            rows, hit = [], False
            for d in docs:
                # 그림 값은 소수 둘째 자리까지라 그 자리에서 맞춘다
                same = tgt is not None and abs(round(d.band_gap, 2) - tgt) < 0.005
                hit |= same
                rows.append({"material_id": d.material_id,
                             "spacegroup": d.symmetry.symbol, "band_gap_eV": d.band_gap,
                             "nsites": d.nsites, "e_above_hull": d.energy_above_hull,
                             "theoretical": bool(d.theoretical),
                             "matches_hardcoded": bool(same)})
                print(f"     {d.material_id:14s} {d.symmetry.symbol:12s} "
                      f"gap {d.band_gap:6.3f}  {d.nsites:3d}원자  "
                      f"hull {0.0 if d.energy_above_hull is None else d.energy_above_hull:6.3f}  "
                      + ("⚠예측" if d.theoretical else "✅관측")
                      + ("   ★ 그림 값과 일치" if same else ""))
            if tgt is not None and not hit:
                print(f"     ⛔ **{tgt} 와 맞는 다형체가 없다** — 이 숫자의 출처는 MP 가 "
                      f"아니거나 값이 갱신됐다. 그림에서 그대로 쓰면 안 된다.")
            out[f] = rows
    print("\n판정 요령: ★ 가 붙으면 다형체 선택 문제 — ID 를 박고 어느 쪽을 쓸지 정하면 닫힌다.")
    print("           ⛔ 가 붙으면 출처 문제 — 그 값을 그림에서 내리거나 출처를 찾아야 한다.")
    return out


PLAN = """
═══ Nd frozen-4f 경로 — 단계별 계획 ═══════════════════════════════════════

⚠ 시작 전에: 이건 "숫자 하나" 가 아니다. repo 안에서 Nd 갭이 필요한 상이 7종이고
  (NdPO₄·NdOCl·NdCl₃·LiNdO₂·Nd₂O₃·Nd₂S₃·NdS) 전부 지금 MP 소환값이다.
  PP 하나를 확보하면 **Nd 축 전체**가 우리 값으로 바뀐다.

【0단계】 가진 것 확인                                            비용: 5분
  python3 tools/sei/nd_frozen4f.py --inventory
  → z_valence ≈ 11 인 Nd PP 가 있으면 곧장 1단계.
     전부 z ≈ 14 면 아래 확보 경로 A/B/C.

【확보 경로 — 0단계가 빈손일 때】
  A. **기성품을 찾는다**                                          비용: 반나절
     · pslibrary / SSSP / PseudoDojo 의 Nd 항목을 z_valence 로 훑는다
     · 란타나이드는 "RE-in-core" 로 불리는 세트가 따로 있는 경우가 많다
     · ⚠ 출처와 생성 조건(범함수·상대론)을 반드시 기록한다 — 기억으로 채우지 않는다
  B. **ld1.x 로 만든다**                                          비용: 1–2일 + 검증
     · QE 가 ld1.x 를 같이 빌드한다. pslibrary 에 란타나이드 입력 템플릿이 있다
     · 4f 를 core configuration 에 넣고 5s5p6s5d 를 원자가로 잡는다
     · ⚠ 직접 만든 PP 는 **반드시 검증**해야 한다 — 격자상수·체적탄성률을 알려진
       값과 대조하기 전에는 갭에 쓰지 않는다
  C. **그 계산만 VASP 로**                                        비용: 외주 조율
     · MP 가 쓰는 `Nd_3` 를 그대로 쓰면 **MP 와 같은 방법 계열**이 된다
     · tools/sdcp/qe_to_vasp.py 가 이미 있다 (SDCP 외주에 쓴 것)
     · ⚠ 그러면 우리 Li 계 6종(QE)과 **다른 코드**라 한 표에 못 섞는다 —
       "Nd 상은 VASP" 라는 단서가 영구적으로 붙는다. A/B 가 되면 그쪽이 낫다.

【1단계】 Nd₂O₃ 로 검증                                          비용: 30분 (5원자!)
  ★ 제일 싼 계로 먼저 재현되는지 본다. 여기서 갈린다.
  python3 tools/sei/nd_frozen4f.py --check /경로/새PP.UPF   # 설치 전 판별
  # ⚠⚠ 설치 후 반드시 --inventory 를 **다시** 돌린다. build_dft_inputs 는 pseudo
  #    디렉터리에서 **파일명 알파벳 첫 번째**를 조용히 고른다(setdefault). 새 PP 를
  #    넣기만 하면 옛 `Nd.paw.z_14…` 가 그대로 이겨서 똑같은 금속 해가 나온다.
  python3 tools/sei/nd_frozen4f.py --inventory              # '◀ 실제로 뽑힘' 확인
  python3 tools/sei/nd_frozen4f.py --reference     # 표적값 받아 두기
  python3 tools/sei/build_dft_inputs.py --pattern "db/structures/sei_nd2o3*.vasp" \\
      --no_nd_spin --nd_u 0          # frozen-4f 면 스핀·U 가 필요 없다(4f 가 core 라서)
  # 생성된 입력의 UPF 이름을 눈으로 한 번 더 본다 — 여기서 틀리면 30분이 아니라 하루다
  grep -a UPF /data/work/runs/sei_dft/nd2o3_mp-2763/*.in | sort -u
  bash tools/sei/run_sei_dft.sh nd2o3_mp-2763

  합격 기준 — 셋 다 맞아야 한다:
    ① 02_scf.out 이 `highest occupied, lowest unoccupied` 를 찍는다
       (= 절연체. `the Fermi energy is` 가 찍히면 여전히 금속이다 → 불합격)
    ② 갭이 **양수**이고 VBM < CBM
    ③ MP 값과 **같은 자릿수** (완전 일치는 기대 안 한다 — 코드·PP 계열이 다르다)

  ⛔ 불합격이면 **거기서 멈춘다.** PP 문제인지 설정 문제인지 가리기 전에 다른 계로
     넘어가면 실패를 3배로 늘릴 뿐이다. (이번에 그렇게 했다가 3종을 다 태웠다.)

【2단계】 나머지 Nd 상                                            비용: 1–2시간
  LiNdO₂(16) · Nd₂S₃(20) → 통과하면 NdPO₄ · NdOCl · NdCl₃ · NdS 까지
  ⚠ 4f 가 core 면 스핀분극도 U 도 필요 없어져서 **비용이 확 준다** — 그게 이 경로의
    실질적 이점이다(이번에 실패한 계산들이 비쌌던 이유가 그것이었다).

【3단계】 등재·갱신                                               비용: 30분
  · db/properties/electronic.json 에 Nd 갭 등재 (method_id 에 frozen-4f 명시)
  · canonical_registry.json 에 항목 추가 — **새 comparison_group**
    (`gap-fixedocc-frozen4f-v1`) 로 둔다. Li 계 6종과 PP 계열이 다르므로 같은 묶음이
    아니다. 이번 리뷰에서 배운 규칙 그대로다.
  · tools/figures/plot_nd_sei_gaps.py 의 하드코딩 MP 값을 우리 값으로 교체
  · 협업자 회신 문안(docs/collab/sei_reply_2026_08_07.md) 갱신

【중단 기준】 — 미리 정해 둔다
  · 1단계 불합격 + 원인이 30분 안에 안 잡히면 → MP 인용 유지, 이 계획을 보류로 기록
  · 경로 B(ld1.x)에서 검증(격자·탄성)이 안 맞으면 → 그 PP 폐기. 미검증 PP 로 낸 갭은
    4f-in-valence 로 낸 값보다 나을 게 없다
  · ⚠ **U 를 돌려가며 갭이 열릴 때까지 맞추지 않는다** — 그건 답을 정해 놓고 파라미터를
    고르는 것이다. frozen-4f 는 애초에 U 가 필요 없는 게 요점이다

【이 계획의 값】
  성공하면: Nd 축 7종이 우리 계산이 되고, 협업자에게 "MP 를 쓰세요" 대신 우리 표를 준다.
  실패해도: **왜 안 되는지를 두 층(4f-in-valence · frozen-4f)에서 확인**한 셈이라,
  "우리가 해 봤고 이러이러해서 MP 를 인용한다" 가 근거 있는 문장이 된다.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", action="store_true", help="0단계: Nd PP 를 z_valence 로 분류")
    ap.add_argument("--check", nargs="+", metavar="UPF",
                    help="받아 온 후보 UPF 를 설치 전에 판별")
    ap.add_argument("--reference", action="store_true", help="검증 표적(MP 갭)을 받아 저장")
    ap.add_argument("--polymorphs", nargs="*", metavar="상", default=None,
                    help="조성별 전 다형체를 찍어 그림 하드코딩 값의 출처를 가린다 "
                         "(인자 없으면 7종 전부)")
    ap.add_argument("--plan", action="store_true", help="단계별 계획·비용·중단 기준")
    ap.add_argument("--pseudo_dirs", nargs="*", default=PSEUDO_DIRS)
    a = ap.parse_args()
    if not (a.inventory or a.check or a.reference or a.plan or a.polymorphs is not None):
        a.plan = True
    if a.inventory:
        inventory(a.pseudo_dirs)
    if a.check:
        print("후보 UPF 판별  (판별 기준: z_valence)")
        check(a.check)
    if a.reference:
        key = os.environ.get("MP_API_KEY")
        if not key:
            sys.exit("⛔ MP_API_KEY 가 없다.  export MP_API_KEY=...  (⚠ 파일에 넣지 말 것)")
        print("검증 표적 — MP 의 Nd 상 밴드갭")
        reference(key)
    if a.polymorphs is not None:
        key = os.environ.get("MP_API_KEY")
        if not key:
            sys.exit("⛔ MP_API_KEY 가 없다.  export MP_API_KEY=...  (⚠ 파일에 넣지 말 것)")
        print("조성별 전 다형체 — 그림 하드코딩 값의 출처 규명")
        polymorphs(key, a.polymorphs or None)
    if a.plan:
        print(PLAN)
    return 0


if __name__ == "__main__":
    sys.exit(main())
