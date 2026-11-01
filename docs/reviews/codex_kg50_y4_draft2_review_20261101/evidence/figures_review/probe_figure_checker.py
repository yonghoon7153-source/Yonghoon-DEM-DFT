from pathlib import Path
import sys,os,copy,json,warnings
BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'figures_review'
os.environ['MPLCONFIGDIR']=str(OUT/'mplconfig')
if os.environ.get('REVIEW_PYDEPS'): sys.path.insert(0,os.environ['REVIEW_PYDEPS'])
SRC=BASE/'source/repo/docs/50kg/report_y4/draft2'
sys.path.insert(0,str(SRC))
import make_draft2_figs as F
orig_rp=F.src.rp
F.src.rp=lambda rel:orig_rp(rel) if orig_rp(rel).is_file() else BASE/'remote'/rel
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    baseline=F.build_all(write=False)
print('BASELINE',baseline)
data,decks=F.load()
F.CHECK['write']=False
F.CHECK['beds_with_data']=tuple(data)
tests={}

# The consumer combines JSON scalars and companion CSVs without a binding.
# Swap one same-schema companion in memory (equivalent to stale/wrong filename on disk).
mut=copy.deepcopy(data)
mut['D1']['per_am']=copy.deepcopy(mut['D2']['per_am'])
F.CHECK['results']={}
F.fig_p3_per_am(mut,{})
tests['D1_per_am_from_D2']={'result':F.CHECK['results'],'D1_p3_contacts_coverage_Hertz':data['D1']['m']['coverage_hertz_pct'],'D1_p3_per_am_mean_after_swap':sum(float(r['coverage_hertz_pct']) for r in mut['D1']['per_am'])/len(mut['D1']['per_am'])}

# One actual D1 relaxation sample becomes NaN: the plotted line loses that vertex,
# while the automatic axis test still reports no problem for this actual figure.
mut=copy.deepcopy(data)
relax_rows=[r for r in mut['D1']['curve'] if r['branch']=='fixed_height_relaxation']
original=copy.deepcopy(relax_rows[20]);relax_rows[20]['plate_pressure_MPa']='nan'
F.CHECK['results']={};F.fig_p2_relax(mut,{})
tests['D1_relax_pressure_nan']={'changed_original_row':original,'result':F.CHECK['results']}

# The declared geometry checker silently drops a non-finite data vertex.
fig=F.plt.figure(figsize=(4.5,2.55));ax=fig.add_axes([.2,.2,.6,.6]);ax.set_xlim(0,2);ax.set_ylim(0,2)
ax.plot([.5,1,1.5],[.5,float('nan'),1.5])
problems,counts=F.check_figure(fig,'synthetic_nonfinite_line');F.plt.close(fig)
tests['nonfinite_line_vertex']={'problems':problems,'counts':counts,'input_points':3}

# A normal finite out-of-range point must still be detected.
fig=F.plt.figure(figsize=(4.5,2.55));ax=fig.add_axes([.2,.2,.6,.6]);ax.set_xlim(0,2);ax.set_ylim(0,2)
ax.plot([.5,1,1.5],[.5,3,1.5])
problems,counts=F.check_figure(fig,'synthetic_outside_line');F.plt.close(fig)
tests['outside_line_vertex']={'problems':problems,'counts':counts,'input_points':3}

# Actual shipped recipe's clipping tag checks existence, not plate geometry identity.
captured=[]
old_save=F.save
def wrong_clip_save(fig,stem,rows,cols,meta):
    if stem=='p1_bed_strip':
        for ax in fig.axes:
            for c in ax.collections:
                if c.get_gid()==F.GID_SECTION_CROP:
                    # Shift the plate clipping boundary upward while retaining a custom clip.
                    x0,x1=ax.get_xlim();y0,y1=ax.get_ylim()
                    c.set_clip_path(F.Rectangle((x0,y0),x1-x0,y1-y0-2.0,transform=ax.transData))
    return old_save(fig,stem,rows,cols,meta)
F.save=wrong_clip_save;F.CHECK['results']={};F.fig_p1(data,decks,{})
tests['section_wrong_clip_top']={'result':F.CHECK['results']}
F.save=old_save

result={'baseline':baseline,'tests':tests,'matplotlib':F.matplotlib.__version__}
(OUT/'figure_checker_probes.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
