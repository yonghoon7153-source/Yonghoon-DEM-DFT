# ── 정적대조 (b) 기하 생성 + UMA 단일점 (a)(b) — gabia · tmux ──
# 카드 v3 §5. (b) = canonical 을 UMA 로 완화한 종점(FrechetCellFilter, fmax 0.05, ≤1500 스텝 —
# uma_relax_check_hosts.json 과 같은 설정). 구조를 **저장**하고 sha256 을 박는다.
# (a) = comp1_V0_k444.cif 그대로. 둘 다 UMA 단일점 E·F·전체응력을 JSON 으로.
U=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
echo "GPU 사용 중: ${U} MiB"; [ "$U" -gt 44000 ] && { echo "⛔ QE 가 물고 있음 — 대기"; exit 1; }
R=/root/Yonghoon-DEM-DFT; OUT=/root/static_ab; mkdir -p $OUT
cat > $OUT/make_b_and_sp.py <<'PYEOF'
import json, hashlib, numpy as np
from ase.io import read, write
from ase.optimize import FIRE
try:    from ase.filters import FrechetCellFilter as CF
except: from ase.constraints import ExpCellFilter as CF
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
R="/root/Yonghoon-DEM-DFT"; OUT="/root/static_ab"
EV=160.21766208
calc=FAIRChemCalculator(pretrained_mlip.get_predict_unit("uma-s-1p1",device="cuda"),task_name="omat")
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def sp(a,tag):
    a=a.copy(); a.calc=calc
    E=float(a.get_potential_energy()); F=np.asarray(a.get_forces()); s=np.asarray(a.get_stress(voigt=True),float)
    return {"tag":tag,"n":len(a),"E_eV":E,"E_per_atom_eV":E/len(a),
            "F_eV_A":F.tolist(),"stress_voigt_GPa":(-s*EV).tolist(),   # QE 부호 관례(압력 +)로 맞춤
            "V_per_atom":a.get_volume()/len(a),"cell":a.cell.array.tolist()}
# (a)
a=read(f"{R}/db/structures/comp1_V0_k444.cif")
write(f"{OUT}/a_comp1_k444.xyz",a); write(f"{OUT}/a_comp1_k444.vasp",a,format="vasp")
# (b): canonical → UMA 완화 (uma_relax_check_hosts 설정)
b=read(f"{R}/db/structures/lpscl_F43m_24G_canonical.cif"); b.calc=calc
v0=b.get_volume()/len(b)
opt=FIRE(CF(b),logfile=None); opt.run(fmax=0.05,steps=1500)
nb=opt.get_number_of_steps(); conv=nb<1500
write(f"{OUT}/b_canonical_uma.xyz",b); write(f"{OUT}/b_canonical_uma.vasp",b,format="vasp")
res={"settings":{"model":"uma-s-1p1/omat","filter":"FrechetCellFilter","fmax":0.05,"max_steps":1500},
     "b_relax":{"V_per_atom_before":v0,"V_per_atom_after":b.get_volume()/len(b),"steps":nb,"converged":conv},
     "sha256":{k:sha(f"{OUT}/{k}") for k in ("a_comp1_k444.xyz","a_comp1_k444.vasp","b_canonical_uma.xyz","b_canonical_uma.vasp")},
     "uma_singlepoint":{"a":sp(a,"a"),"b":sp(b,"b")}}
json.dump(res,open(f"{OUT}/uma_ab.json","w"),indent=1)
print(f"(b) V/atom {v0:.3f} → {b.get_volume()/len(b):.3f}  steps {nb}  conv {conv}")
for k in ("a","b"):
    r=res["uma_singlepoint"][k]; s=r["stress_voigt_GPa"]
    # ⚠ |F|max 는 **벡터 노름** 최대다. np.abs(F).max() 는 성분 최대라 작게 나온다 (2026-09-12 정정).
    _pa=np.linalg.norm(np.asarray(r["F_eV_A"]), axis=1); _dev=np.asarray(s[:3])-np.mean(s[:3])
    print(f"UMA {k}: E/atom {r['E_per_atom_eV']:.5f}  P {sum(s[:3])/3:+.3f} GPa  "
          f"|F|max(벡터) {_pa.max():.4f}  RMSE {np.sqrt((_pa**2).mean()):.4f}  "
          f"편차대각 {_dev.round(3).tolist()}  전단 {np.asarray(s[3:]).round(3).tolist()}")
PYEOF
tmux new -d -s sab "/data/apps/miniforge3/envs/uma/bin/python $OUT/make_b_and_sp.py > $OUT/run.log 2>&1"
sleep 120; grep -av "Warning\|return f" $OUT/run.log; ls -la $OUT/
echo "── 이 넷을 회수 (scp) ──"; echo "  $OUT/{a_comp1_k444.vasp,b_canonical_uma.vasp,uma_ab.json}"
