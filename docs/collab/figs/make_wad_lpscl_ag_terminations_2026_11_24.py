import sys, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from ase.io import read
from ase.geometry import get_distances
sys.path.insert(0,'tools/figures'); import house_style as H
D='db/raw/wad_se_pairs_uma_2026_10_01/relax'
COL={'Li':H.ELEM.get('Li','#0d9488'),'P':H.ELEM.get('P','#7c3aed'),'S':H.ELEM.get('S','#c05621'),'Cl':H.ELEM.get('Cl','#65a30d'),'Ag':'#9ca3af'}
RAD={'Li':0.5,'P':0.5,'S':0.72,'Cl':0.72,'Ag':0.7}
CUT={'S':2.9,'Li':3.0,'Cl':3.0,'P':3.2}
NOTE={'s_outer':'Ag touches 4 free S (no P bond) + 8 Li','li_outer':'Ag touches 8 S of PS$_4$ tetrahedra + 4 Li'}
fig,axs=plt.subplots(2,1,figsize=(10,8.4))
for ax,(term,title) in zip(axs,(('s_outer','S-outer termination'),('li_outer','Li·PS$_4$-outer termination'))):
    a=read(f'{D}/P1_{term}/A/relaxed.extxyz'); a.wrap()
    sym=np.array(a.get_chemical_symbols()); pos=a.positions
    ag=np.where(sym=='Ag')[0]; se=np.where(sym!='Ag')[0]
    z0=pos[ag,2].min()
    _,dm=get_distances(pos[se],pos[ag],cell=a.cell,pbc=a.pbc); dmin=dm.min(axis=1)
    contact=set(int(se[k]) for k in range(len(se)) if dmin[k]<=CUT.get(sym[se[k]],0))
    show=[i for i in range(len(a)) if (sym[i]!='Ag' and pos[i,2]>=z0-6.3) or (sym[i]=='Ag' and pos[i,2]<=z0+2.8)]
    P=[i for i in show if sym[i]=='P']; S=[i for i in show if sym[i]=='S']
    for p in P:
        for s in S:
            if np.linalg.norm(pos[s]-pos[p])<2.5:
                ax.plot([pos[p,1],pos[s,1]],[pos[p,2]-z0,pos[s,2]-z0],color=H.INK,lw=1.6,zorder=1)
    for i in sorted(show,key=lambda i:-pos[i,0]):
        el=sym[i]; ec,lw=(H.INK,2.4) if i in contact else ('white',0.6)
        ax.add_patch(plt.Circle((pos[i,1],pos[i,2]-z0),RAD[el],facecolor=COL[el],edgecolor=ec,lw=lw,zorder=2))
    ax.axhline(0,color='#2563eb',ls='--',lw=1,zorder=0)
    Ly=float(a.cell.lengths()[1])
    ax.text(Ly,0.95,'first Ag layer',ha='right',va='bottom',fontsize=10,color='#2563eb')
    ax.set_xlim(-0.9,Ly+0.9); ax.set_ylim(-6.8,3.8); ax.set_aspect('equal')
    ax.set_title(f'{title}  —  {NOTE[term]}',fontsize=12.5,color=H.INK,loc='left')
    ax.set_xlabel('y (Å)',color=H.INK); ax.set_ylabel('z − z$_{\\rm Ag}$ (Å)',color=H.INK)
    for sp in ('top','right'): ax.spines[sp].set_visible(False)
hd=[Line2D([0],[0],marker='o',ls='',markerfacecolor=COL[e],markeredgecolor='white',markersize=10,label=e) for e in ('Ag','S','P','Li','Cl')]
hd.append(Line2D([0],[0],marker='o',ls='',markerfacecolor='white',markeredgecolor=H.INK,markeredgewidth=2.4,markersize=10,label='touches Ag'))
hd.append(Line2D([0],[0],color=H.INK,lw=1.6,label='P–S bond (PS$_4$)'))
fig.legend(handles=hd,loc='lower center',ncol=7,frameon=False,fontsize=10)
fig.tight_layout(rect=(0,0.05,1,1))
fig.savefig(sys.argv[1],dpi=200); print('saved')
