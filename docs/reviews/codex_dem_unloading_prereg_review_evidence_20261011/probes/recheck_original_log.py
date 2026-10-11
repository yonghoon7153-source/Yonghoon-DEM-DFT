from pathlib import Path
import re,json,statistics
R=Path(__file__).resolve().parents[1]
p=R/'evidence/ps73_logs/home/yonghoon/dem_test/ps45/logs/output_ps_7_3_r45_r8_220537.out'
lines=p.read_text(errors='replace').splitlines();start=next(i for i,l in enumerate(lines) if l=='====== PHASE 4: RELAXATION ======')
rows=[]
for i,l in enumerate(lines[start+1:],start+2):
    a=l.split()
    if len(a)==5 and a[0].isdigit():
        try:rows.append(dict(line=i,step=int(a[0]),atoms=int(a[1]),ke=float(a[2]),cpu=float(a[3]),P_MPa=float(a[4])*1000))
        except ValueError:pass
setup=rows[0];reg=rows[1:];tail=reg[-25:];mean=statistics.mean(x['P_MPa'] for x in tail)
window=[x for x in reg if abs(x['step']-3200000)<=5000]
means=[statistics.mean(x['ke'] for x in tail[i:i+5]) for i in range(0,25,5)]
out=dict(log=str(p.relative_to(R)),phase4_setup=setup,regular_lines=len(reg),S0=next(x for x in reg if x['step']==3200000),last25_mean_MPa=mean,S0_window_count=len(window),max_deviation_MPa=max(abs(x['P_MPa']-mean) for x in window),max_deviation_pct=100*max(abs(x['P_MPa']-mean) for x in window)/mean,KE_fivewindow_means_J=means,KE_baseline_J=statistics.median(means),setup_atom_count=setup['atoms'],final_atom_count=reg[-1]['atoms'],last_line=reg[-1])
(R/'evidence/original_log_recheck.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
