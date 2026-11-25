#!/bin/bash
# check_inputs_kgy.sh — li2s-3 입력 확인 (읽기만 · GPU 안 씀 · 수 초 · 아무것도 쓰지 않는다)
#   li2s-2 가 만든 여섯 담금질 (A · B × seed11–13) 의 최종 구조 지문 · 판정 파일 · 시드 게이트 값 · MD 러너 기록값 (REC) 과
#   MD 설정 기준 파일이 kgy 에 남아 있는지를 찍는다. 카드 초안 db/properties/lpscl_glass_dense_protocol_ensemble_estimand_2026_11_10.json
# 쓰는 법 (kgy · 한 줄):
#   git -C ~/lldvar fetch origin claude/friendly-meitner-lldvar && git -C ~/lldvar show FETCH_HEAD:db/inputs/li2s3_dense_ensemble_2026_11_10/check_inputs_kgy.sh | bash
# ⛔ 못 하는 것: 판정하지 않는다 · 수송값을 읽지 않는다 (MD 는 아직 없다) · 압력 값 · 녹음 창 D 값은 찍지 않는다.
set -u
PY=${PY:-/home/kgy/apps/miniforge3/envs/uma/bin/python}
R=${R:-$HOME/work/runs/li2s2_dense_1103}
W=${W:-$HOME/wt_li2s2}
echo "== li2s-3 입력 확인 (읽기만) · $(date '+%F %T') · $(hostname) =="
"$PY" - "$R" "$W" <<'PYEOF'
import sys, json, hashlib, pathlib
import numpy as np
from ase.io import read
from ase.geometry import get_distances
R, W = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
sys.path.insert(0, str(W / "tools/ionic"))
try:
    import melt_quench_uma as mq
except Exception as e:                       # 드라이버를 못 불러도 지문 · REC · 판정 파일은 찍는다
    mq = None
    print(f"(드라이버 import 못 함 — {type(e).__name__}: {e})")
KEYS = ("PS4_fraction", "P_S_coord_hist", "bridging_S_P2S7_like", "P_P_bonds_P2S6_like",
        "min_pair_A", "min_pair_kind", "min_pair_excl_PS_A", "min_pair_excl_PS_kind", "density_g_cm3")
for s in ("A", "B"):
    for k in (11, 12, 13):
        d = R / s / f"seed{k}"
        f = d / "final.xyz"
        if not f.is_file():
            print(f"{s}{k}: final.xyz 없음 ({f})")
            continue
        fr = read(str(f), index=":")
        a = fr[-1]
        sym = np.array(a.get_chemical_symbols())
        _, D = get_distances(a.positions[sym == "P"], a.positions[sym == "S"], cell=a.cell, pbc=True)
        ps, n4, nP = float(D.min()), int(((D <= 2.6).sum(axis=1) == 4).sum()), D.shape[0]
        rho = float(a.get_masses().sum() * 1.66053906660 / a.get_volume())
        try:
            v = json.loads((d / "stage1_verdict.json").read_text(encoding="utf-8"))
        except Exception as e:
            v = {"status": f"판정 파일 읽기 실패 ({type(e).__name__})"}
        gv = v.get("seed_gate_view") or {}
        src = "판정 파일"
        if not gv and mq is not None:
            try:
                gv, src = mq._gate_view(a), "드라이버로 다시 냄"
            except Exception as e:
                gv, src = {}, f"못 냄 ({type(e).__name__})"
        print(f"{s}{k}: 프레임 {len(fr)} · 원자 {len(a)} · final.xyz sha256 {hashlib.sha256(f.read_bytes()).hexdigest()}")
        print(f"   REC \"{ps:.4f} {n4} {rho:.4f}\"   (최단 P–S · PS₄ 개수 (2.6 Å) {n4}/{nP} · 밀도)")
        print(f"   판정 {v.get('status')} · closes_system {v.get('closes_system')} · 사유 {json.dumps(v.get('reasons'), ensure_ascii=False)}")
        print(f"   게이트 값 ({src}) {json.dumps({q: gv.get(q) for q in KEYS}, ensure_ascii=False)}")
        print(f"   녹음 판정 {(v.get('melt_window_check') or {}).get('verdict')} · 소프트웨어 {json.dumps(v.get('software'), ensure_ascii=False)}")
PYEOF
echo "== MD 설정 기준 파일 (run_meta · md.log) =="
for d in "$HOME/work/runs/lpscl_glass_md_2026_09_26/pilot600/T600" "$HOME/work/runs/lpscl_glass_md_v2_2026_09_30/seed1/T600" \
         "$HOME/work/runs/lpscl_glass_control_li3ps4_600K_2026_10_13/seed1/T600" "$HOME/work/runs/lpscl_glass_bmeas_650K_2026_10_14/seed1/T650"; do
  m=$d/run_meta.json; l=$(ls "$d"/d0.00_cfg0/T*/md.log 2>/dev/null | head -1)
  [ -s "$m" ] && echo "있음 $m · md.log ${l:-없음}" || echo "없음 $m"
done
echo "== 드라이버 · 러너 지문 (기대 c3e2d358ee53cefa · 3aef029aced0de77) =="
sha256sum "$W/tools/modelc_v3/disorder_ensemble_diffusion.py" "$W/db/raw/lpscl_glass_md_v2_2026_09_30/glass_kgy_q_v2.sh" 2>/dev/null | cut -c1-16,65-
echo "== GPU · 디스크 =="
nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader 2>/dev/null || echo "(nvidia-smi 없음)"
df -h / | tail -1
