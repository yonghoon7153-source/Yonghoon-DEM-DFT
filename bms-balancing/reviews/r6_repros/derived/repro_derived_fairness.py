#!/usr/bin/env python3
"""파생-보고서 + 공정성-의미 렌즈 재현 스크립트 (self-review R6).
`bms-balancing/` 안에서 `python3 <this file>` 로 돌린다. 산출물(out/)·문서·코드 소스만 읽는다 — 아무것도 쓰지 않는다.
각 검사는 PASS(문서와 산출물이 맞음) / FINDING(문서와 산출물이 다름 또는 의미 함정) / INFO 를 찍는다."""
import csv, json, re, sys, pathlib, statistics as st, subprocess
import numpy as np
ROOT = pathlib.Path(".").resolve(); OUT = ROOT / "out"
assert (OUT / "scale_audit_eval_u13.txt").is_file(), "bms-balancing/ 안에서 실행할 것"
status = {"PASS": 0, "FINDING": 0, "INFO": 0}
def say(kind, cid, msg): status[kind] += 1; print(f"[{kind:7}] {cid}: {msg}")
def rows_of(f):
    with open(f, encoding="utf-8") as fh: return list(csv.DictReader(fh))
def width(rs, m): v = [float(r[m]) for r in rs]; return max(v) - min(v)
def doc(name): return (ROOT / name).read_text(encoding="utf-8")

# ── C01 U13 ────────────────────────────────────────────────────────────────
lines = [l for l in (OUT/"scale_audit_eval_u13.txt").read_text().splitlines() if l.startswith("# scale_audit")]
recs = []
for l in lines:
    head, *metrics = l[len("# scale_audit,"):].split("; ")
    rec = {"ident": dict(kv.split("=") for kv in head.split())}
    for m in metrics:
        name, body = m.split(":", 1); rec[name] = dict(kv.split("=") for kv in body.split("/"))
    recs.append(rec)
eps = [float(r[k]["eps_rel"]) for r in recs for k in ("pocv", "dvdq", "dqdv")]
cond = all(r[k]["n"] == r[k]["finite"] == "50" and r[k]["inf"] == r[k]["nan"] == r[k]["exc"] == "0" and r[k]["equiv"] == "1"
           and float(r[k]["eps_rel"]) <= 1e-9 for r in recs for k in ("pocv", "dvdq", "dqdv"))
ok = len(lines) == 18 and cond and abs(min(eps) - 4.74e-16) < 1e-18 and abs(max(eps) - 1.71e-15) < 1e-18
say("PASS" if ok else "FINDING", "C01 U13", f"18 줄={len(lines)==18} 조건 전부={cond} eps_rel {min(eps):.3g}~{max(eps):.3g} (§1-13 '4.7e-16~1.7e-15')")
from collections import Counter
idents = Counter(tuple(sorted(r["ident"].items())) for r in recs); full = Counter(lines)
say("INFO", "C01 U13 식별자", f"식별자 tuple 종류 {len(idents)} (18 줄 중 GITT·Li 4 tuple 이 각 4회) · 숫자까지 완전히 같은 줄 {sum(v-1 for v in full.values() if v>1)} 쌍(pouch pristine = fixedhc pristine, 예상된 동일) · seed 집합 {sorted(set(r['ident']['seed'] for r in recs))}")
need = [("pristine","GITT","Li"),("pristine","GITT","Kunz"),("pristine","step_005C","Li"),("300_0009","GITT","Li")]
have = [c for c in need if any((r["ident"]["state"],r["ident"]["source"],r["ident"]["si"])==c for r in recs)]
say("PASS" if len(have)==4 else "FINDING", "C01 recompare 4 조합", f"{len(have)}/4 이 U13 식별자에 있다 (루트는 보고 순서)")
# ── C02 U12 ────────────────────────────────────────────────────────────────
l12 = [l for l in (OUT/"scale_audit_eval.txt").read_text().splitlines() if l.startswith("# scale_audit")]
say("PASS" if len(l12)==16 and all(l.count("inf=0")==3 and l.count("nan=0")==3 for l in l12) else "FINDING", "C02 U12", f"16 줄={len(l12)==16}, 전부 inf=0·nan=0, 식별자 없음·16 줄 전부 동일 문자열={len(set(l12))==1}")
# ── C03 §1-8 192 값 ─────────────────────────────────────────────────────────
def parse_txt(p):
    anchors={}; rows=[]; hdr=None
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.startswith("=== "): break
        if line.startswith("# dd_eval"): continue
        if line.startswith("# "): k,v=line[2:].split(","); anchors[k]=float(v)
        elif line.startswith("a_PE,"): hdr=line.split(",")
        elif hdr and line.strip(): rows.append([float(x) for x in line.split(",")])
    return anchors,hdr,rows
def parse_csv(p):
    anchors={}; rows=[]; hdr=None; decl=None
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.startswith("# dd_eval"): continue
        if line.startswith("# "):
            k,v=line[2:].split(",",1)
            if k=="printed_format": decl=v; continue
            if k.startswith("impl_"): continue
            anchors[k]=float(v)
        elif line.startswith("a_PE,"): hdr=line.split(",")
        elif hdr and line.strip(): rows.append([float(x) for x in line.split(",")])
    return anchors,hdr,rows,decl
rel=lambda a,b: abs(a-b)/max(abs(a),abs(b)) if (a or b) else 0.0
colmax={}; cfgmax={}; nvals=0; decls={}; anch_ok=True
for cfg in ("300_Li","pristine_Kunz","pristine_Li","pristine_Li_005c"):
    ta,th,tr=parse_txt(OUT/"recompare"/f"dd_eval_{cfg}.txt"); ca,ch,cr,decl=parse_csv(OUT/"recompare"/f"dd_eval_{cfg}_r2.csv")
    decls[cfg]=decl; nvals += len(ta) + len(tr)*4
    amax = max(rel(ta[k],ca[k]) for k in ta if k not in ("dv_PE_0p5","dv_NE_0p5_0p25"))
    per = {c: max(rel(tr[i][j],cr[i][j]) for i in range(8)) for j,c in enumerate(ch[5:],start=5)}
    for c,v in per.items(): colmax[c]=max(colmax.get(c,0),v)
    cfgmax[cfg]=max(per.values())
    anch_ok = anch_ok and amax <= 3.62e-16*1.01 and rel(ta["dv_PE_0p5"],ca["dv_PE_0p5"]) <= 1.36e-13*1.01 and rel(ta["dv_NE_0p5_0p25"],ca["dv_NE_0p5_0p25"]) <= 6.03e-14*1.01
want={"rmse_pocv":4.35e-15,"rmse_dvdq":2.84e-14,"rmse_dqdv":2.90e-12,"rmse_dqdv_w":4.04e-12}
ok = anch_ok and nvals==192 and all(abs(colmax[c]-want[c])/want[c] < 0.01 for c in want) and sorted(round(v,14) for v in cfgmax.values())==sorted(round(v,14) for v in (2.68e-12,4.04e-12,2.54e-12,3.28e-12))
say("PASS" if ok else "FINDING", "C03 §1-8 192 값", f"값 수 {nvals}; 앵커 14 ≤3.62e-16·dv_PE ≤1.36e-13·dv_NE ≤6.03e-14 (1 % 여유)={anch_ok}; 열별 최대 상대차 {{{', '.join(f'{c} {v:.2e}' for c,v in colmax.items())}}}; 조합별 {{{', '.join(f'{c} {v:.2e}' for c,v in cfgmax.items())}}} (§1-8 표·R3 정정 문단과 같음)")
say("INFO", "C03 선언", f"r2 CSV 의 `# printed_format` 선언: {decls} — 넷 다 없음 (§1-8 R3 정정이 이미 말함; §0-1 의 '`%.17g`' 는 TXT 쪽·옵션 기준)")
# ── C04/C05 §3-3·§3-4 ───────────────────────────────────────────────────────
v1=json.load(open(OUT/"degeneracy_300_0009_Li.json")); v2=json.load(open(OUT/"degeneracy_300_0009_Li_v2.json"))
sp={k: v2[k+"_percent"] for k in ("LAM_PE","LAM_NE","LLI")}
ok = (abs(sp["LAM_PE"]["span"]-2.8696)<5e-5 and abs(sp["LAM_NE"]["span"]-3.6027)<5e-5 and abs(sp["LLI"]["span"]-1.0832)<5e-5
      and abs(sp["LAM_NE"]["min"]-5.8948)<5e-5 and abs(v1["LAM_NE_percent"]["min"]-6.0991)<5e-5
      and [round(v1[k+"_percent_observed_cloud"]["span"],4) for k in sp]==[0.3333,1.1959,0.5197])
say("PASS" if ok else "FINDING", "C04 §3-3/§3-4 숫자", f"v2 span PE {sp['LAM_PE']['span']:.4f} NE {sp['LAM_NE']['span']:.4f} LLI {sp['LLI']['span']:.4f}; 도달 격자 {[sp[k]['from_mode_profile']['n_grid_attainable'] for k in sp]}/22 (v1 {[v1[k+'_percent']['from_mode_profile']['n_grid_attainable'] for k in sp]}); 배수 {[round(sp[k]['span']/w,2) for k,w in zip(sp,(1.16,0.87,0.53))]}")
msgs=[]; circular=True
for k in sp:
    ext=sp[k]["from_constrained_extrema"]; prof=sp[k]["from_mode_profile"]; g_lo,g_hi=prof["grid_range_pct"]
    grid=np.linspace(g_lo,g_hi,21); pad=(ext["max"]-ext["min"])/2
    on = abs(grid[5]-ext["min"])<1e-9 and abs(grid[15]-ext["max"])<1e-9 and abs(ext["min"]-pad-g_lo)<1e-9 and abs(ext["max"]+pad-g_hi)<1e-9
    circular &= on
    imin=int(np.argmin(abs(grid-prof["min"]))); imax=int(np.argmin(abs(grid-prof["max"])))
    msgs.append(f"{k}: grid[5]−ext.min={grid[5]-ext['min']:.1e}, grid[15]−ext.max={grid[15]-ext['max']:.1e}; profile.min=grid[{imin}], profile.max=grid[{imax}]; prof.max==ext.max {prof['max']==ext['max']}")
say("FINDING" if circular else "PASS", "C05 §3-4 '독립 수렴'", "힌트 격자(pad=span/2, 21점)는 제약 최적화의 min/max 를 grid[5]·grid[15] 로 **그대로 포함**한다 → LLI 의 '정확히 일치' 는 같은 격자점이다. " + " | ".join(msgs))
# ── C06 §3-3 cross-ref ─────────────────────────────────────────────────────
bm=v2["best_modes_percent"]
r1=[x for x in rows_of(OUT/"matrix_300_0009.csv") if x["half_cell"]=="GITT" and x["si"]=="Li" and float(x["w_dqdv"])==0][0]
r2=[x for x in rows_of(OUT/"matrix_300_0009_v2.csv") if x["half_cell"]=="GITT" and x["si"]=="Li" and float(x["w_dqdv"])==0][0]
d1=max(abs(bm[k]-float(r1[k+"_pct"])) for k in bm); d2=max(abs(bm[k]-float(r2[k+"_pct"])) for k in bm)
say("FINDING" if d2==0 and d1>0 else "PASS", "C06 §3-3 인용 파일", f"best 의 LAM/LLI 는 v2 행과 정확히 같고(Δ {d2:.1e}) 인용된 v1 `matrix_300_0009.csv` 행과는 Δ {d1:.1e} %p — 문장은 v1 을 가리킨다 (사소)")
# ── C07 §4-0 ───────────────────────────────────────────────────────────────
mv1=rows_of(OUT/"matrix_300_0009.csv"); mv2=rows_of(OUT/"matrix_300_0009_v2.csv")
key=lambda r:(r["half_cell"],r["si"],float(r["w_dqdv"])); D1={key(r):r for r in mv1}; D2={key(r):r for r in mv2}
sh={k:{m:float(D2[k][m])-float(D1[k][m]) for m in ("LAM_PE_pct","LAM_NE_pct","LLI_pct")} for k in D2}
mk=max(sh,key=lambda k:max(abs(v) for v in sh[k].values())); big=[k for k in sh if max(abs(v) for v in sh[k].values())>1]
ok = mk==("step_005C","Lu",1.0) and abs(sh[mk]["LAM_PE_pct"]-5.857)<5e-4 and len(big)==8 and sum(k[2]==1.0 for k in big)==5
say("PASS" if ok else "FINDING", "C07 §4-0 이동", f"최대 {mk} ΔPE {sh[mk]['LAM_PE_pct']:+.3f}; >1 %p 조합 {len(big)} (w=1 {sum(k[2]==1.0 for k in big)} · w=0 {sum(k[2]==0.0 for k in big)})")
cnt={}
for tol in (0.0,1e-9):
    w=b=s=0; ww=[]
    for k in D2:
        a=float(D1[k]["obj"]); c=float(D2[k]["obj"]); r=(c-a)/a
        if r>tol: w+=1; ww.append(k[2]==1.0)
        elif r<-tol: b+=1
        else: s+=1
    cnt[tol]=(w,b,s,all(ww))
say("FINDING", "C07 §4-0 '6 나빠짐·17 좋아짐'", f"부호만 보면 나빠짐 {cnt[0.0][0]}·좋아짐 {cnt[0.0][1]}·같음 {cnt[0.0][2]}(전부 w=1? {cnt[0.0][3]}); 상대 1e-9 허용이면 {cnt[1e-9][0]}·{cnt[1e-9][1]}·{cnt[1e-9][2]}(전부 w=1? {cnt[1e-9][3]}) — 문서 숫자는 **적지 않은 허용오차 1e-9** 에서만 나온다")
# ── C08~C10 §4-1~§4-3 ──────────────────────────────────────────────────────
g=[r for r in mv2 if r["half_cell"]=="GITT" and float(r["w_dqdv"])==0]; s5=[r for r in mv2 if r["half_cell"]=="step_005C" and float(r["w_dqdv"])==0]
free=[r for r in g if r["ref_bounds"]=="-"]
ok=(abs(width(g,"LAM_NE_pct")-10.8774)<5e-5 and abs(width(g,"LAM_PE_pct")-3.6631)<5e-5 and abs(width(g,"LLI_pct")-1.0248)<5e-5 and len(free)==3
    and abs(width(s5,"LAM_NE_pct")-10.4637)<5e-5 and abs(width(s5,"LAM_PE_pct")-2.4250)<5e-5 and abs(width(s5,"LLI_pct")-0.8512)<5e-5 and "(n=8)" in doc("FINDINGS.md"))
say("PASS" if ok else "FINDING", "C08 §4-1", f"GITT·w0 폭 NE {width(g,'LAM_NE_pct'):.4f} PE {width(g,'LAM_PE_pct'):.4f} LLI {width(g,'LLI_pct'):.4f}; 005C NE {width(s5,'LAM_NE_pct'):.4f} PE {width(s5,'LAM_PE_pct'):.4f} LLI {width(s5,'LLI_pct'):.4f}; 제목 (n=8) 표기 True")
fw=width(free,"LAM_NE_pct"); fr={r["si"]: float(r["LAM_NE_pct"]) for r in free}
say("FINDING" if abs(fw-2.11)>=5e-3 else "PASS", "C08 §4-1 '2.11 %p'", f"기준 자유 3 종 LAM_NE {fr} → 폭 {fw:.4f} (%.2f) — 문서 '2.11' 은 반올림한 값끼리의 차(7.90−5.79)이고 원값의 폭은 2.10 (사소)" % fw)
lli=[float(r["LLI_pct"]) for r in mv2]; rf=[r for r in mv2 if r["ref_bounds"]=="-"]; bf=[r for r in rf if r["bounds"]=="-"]; bf0=[r for r in bf if float(r["w_dqdv"])==0]
ok=(abs(max(lli)-min(lli)-22.51)<5e-3 and len(rf)==10 and abs(width(rf,"LLI_pct")-2.71)<5e-3 and len(bf)==10 and len(bf0)==6 and abs(width(bf0,"LLI_pct")-0.5442)<5e-5
    and sum(r["ref_bounds"]!="-" for r in mv2)==22 and sum(r["bounds"]!="-" for r in mv2)==10 and all(r["bounds"]=="-" for r in rf))
say("PASS" if ok else "FINDING", "C09 §4-2", f"32 폭 {max(lli)-min(lli):.4f}; 기준 interior n={len(rf)} 폭 {width(rf,'LLI_pct'):.4f}; 둘 다 n={len(bf)}; w0 n={len(bf0)} 폭 {width(bf0,'LLI_pct'):.4f}; 기준 눌림 {sum(r['ref_bounds']!='-' for r in mv2)}/32 대상 {sum(r['bounds']!='-' for r in mv2)}/32")
pairs=[]
for hc in ("GITT","step_005C"):
    for si in sorted(set(r["si"] for r in mv2)):
        a=D2[(hc,si,0.0)]; b=D2[(hc,si,1.0)]; pairs.append((hc,si,float(b["LLI_pct"])-float(a["LLI_pct"]), all(x["bounds"]=="-" and x["ref_bounds"]=="-" for x in (a,b))))
dl=[p[2] for p in pairs]; fp=[p for p in pairs if p[3]]
ok=len(pairs)==16 and abs(st.median(dl)-1.5237)<5e-5 and sum(x<0 for x in dl)==4 and len(fp)==3 and abs(st.mean(p[2] for p in fp)-1.8385)<5e-5
say("PASS" if ok else "FINDING", "C10 §4-3", f"16 쌍 중앙값 {st.median(dl):.4f} 음수 {sum(x<0 for x in dl)} 범위 {min(dl):.3f}~{max(dl):.3f}; 완전 interior {[(p[0],p[1],round(p[2],4)) for p in fp]} 평균 {st.mean(p[2] for p in fp):.4f}")
# ── C11 §5 ─────────────────────────────────────────────────────────────────
p=rows_of(OUT/"profile_gamma_300_0009_Li.csv"); ths={}
for thr in (8,10,11,12):
    s=[r for r in p if float(r["rmse_pocv"])*1000<=thr]; ne=[float(r["LAM_NE_pct"]) for r in s]
    ths[thr]=(len(s),round(max(ne)-min(ne),3),round(max(float(r["obj_ratio_to_best"]) for r in s),3))
inb=[r for r in p if float(r["obj_ratio_to_best"])<=1.01]
ok=ths=={8:(6,7.249,1.201),10:(10,13.586,1.35),11:(12,15.995,1.35),12:(13,17.375,1.429)} and [r["gamma_Si"] for r in inb]==["0.225","0.25"]
say("PASS" if ok else "FINDING", "C11 §5/§5-1", f"문턱→(n, NE 폭, 최악비) {ths}; 1 % 안 행 {[(r['gamma_Si'],round(float(r['LAM_NE_pct']),4)) for r in inb]} (증인 폭 {max(float(r['LAM_NE_pct']) for r in inb)-min(float(r['LAM_NE_pct']) for r in inb):.4f})")
# ── C12 §1-10 ──────────────────────────────────────────────────────────────
files={"100":"degeneracy_100_Li.json","200":"degeneracy_200_Li.json","300_0009":"degeneracy_300_0009_Li_v2.json","300_0147":"degeneracy_300_0147_Li.json"}
orders=[]; nemin=[]; meta_missing=[]
for s,f in files.items():
    j=json.load(open(OUT/f)); w={k:j[k+"_percent"]["span"] for k in ("LAM_PE","LAM_NE","LLI")}; orders.append(sorted(w,key=w.get,reverse=True)); nemin.append((s,round(j["LAM_NE_percent"]["min"],3)))
    if not (OUT/(f+".meta.json")).is_file(): meta_missing.append(f)
say("PASS" if all(o==["LAM_NE","LAM_PE","LLI"] for o in orders) else "FINDING", "C12 §1-10 순위", f"네 상태 폭 순서 {orders[0]} ×{sum(o==orders[0] for o in orders)}/4 (하한끼리의 순위)")
say("INFO", "C12 §1-10 예산", f"meta.json 없는 degeneracy 산출 {meta_missing} (starts·seed 는 300_0147 만 파일로 확인 가능; §1-12 조건 6 이 인정) · matrix_*.csv 에 scale_seed/n_scale_samples/run_id 열 없음 {all('scale_seed' not in rows_of(OUT/f)[0] for f in ('matrix_100.csv','matrix_200.csv','matrix_300_0009_v2.csv','matrix_300_0147.csv'))}")
say("INFO", "C12 §1-10 '양수 구간'", f"LAM_NE 하한 min {nemin} — '다른 세 상태는 전부 양수 구간' 은 하한 hull 의 성질이지 근최적 집합 전체의 성질이 아니다 (§1-10 본문에 한정어 없음)")
# ── C13 §2 ─────────────────────────────────────────────────────────────────
a97=subprocess.run([sys.executable,"scripts/audit97.py"],capture_output=True,text=True).stdout
ok=all(x in a97 for x in ("32 / 97","16 / 97","2 / 97","18 / 97","34.67 %p","11.16 %p","6.44 %p","8.95e-13","1.177 ~ 1.196")) and "a_NE=lb        19" in a97 and "b_PE=ub        15" in a97
say("PASS" if ok else "FINDING", "C13 §2", f"audit97 출력이 §2 표와 같다={ok}; c_ref/c=74.671/63.72={74.671/63.72:.4f}; Wetjen 100 1−71.631/74.671={100*(1-71.631/74.671):.3f} %")
# ── C14 §1-12 ──────────────────────────────────────────────────────────────
roots={"pouch":OUT,"fixedhc":OUT/"cells_pouch_fixedhc","c168":OUT/"cells_c168","c171":OUT/"cells_c171"}; half={}; rm={}
for name,d in roots.items():
    for s in ("100","200","300_0009"):
        mf=d/("matrix_300_0009_v2.csv" if (name=="pouch" and s=="300_0009") else f"matrix_{s}.csv"); jf=d/("degeneracy_300_0009_Li_v2.json" if (name=="pouch" and s=="300_0009") else f"degeneracy_{s}_Li.json")
        r=[x for x in rows_of(mf) if x["half_cell"]=="GITT" and x["si"]=="Li" and float(x["w_dqdv"])==0][0]; j=json.load(open(jf))
        half[(name,s)]=j["LLI_percent"]["span"]/2; rm[(name,s)]=(float(r["rmse_pocv"])*1000,float(r["ref_rmse_pocv"])*1000)
growth={n: round(rm[(n,"300_0009")][0]/rm[(n,"100")][0],2) for n in roots}
pouch6=[half[("pouch",s)] for s in ("100","200","300_0009")]+[half[("fixedhc",s)] for s in ("100","200","300_0009")]; cyl6=[half[(c,s)] for c in ("c168","c171") for s in ("100","200","300_0009")]
pair=[half[(c,s)]/half[("pouch",s)] for c in ("c168","c171") for s in ("100","200","300_0009")]
say("PASS" if growth=={"pouch":0.77,"fixedhc":0.91,"c168":1.6,"c171":1.52} else "FINDING", "C14 §1-12 잔차", f"300/100 rmse 비 {growth}; ref rmse {[round(rm[(n,'100')][1],2) for n in roots]}")
say("FINDING", "C14 '5~10 배'", f"raw LLI 반폭 배율: max/max {max(cyl6)/max(pouch6):.2f} min/min {min(cyl6)/min(pouch6):.2f} med/med {st.median(cyl6)/st.median(pouch6):.2f} (§1-12 표); 상태별 쌍 비 {min(pair):.1f}~{max(pair):.1f} — §0-1·§7·WORKING_STATE·HANDOFF 의 'raw 로 5~10 배' 는 어느 통계로도 안 나온다 (INTRO §6-2 는 10.5 배)")
# ── C15 테스트 수 ──────────────────────────────────────────────────────────
ntests=len(re.findall(r"^def test_", (ROOT/"tests/test_review_findings.py").read_text(encoding="utf-8"), re.M))
stale=[(f, len(re.findall(r"86 passed", doc(f)))) for f in ("reviews/R6_REQUEST.md","WORKING_STATE.md")]
say("FINDING" if ntests!=86 and any(n for _,n in stale) else "PASS", "C15 테스트 수", f"tests/ 의 test 함수 {ntests} (HEAD 커밋 메시지 '87 passed'); '86 passed' 가 남은 곳 {stale}")
# ── C16 철회 문장 잔존 ──────────────────────────────────────────────────────
strike=re.compile(r"~~.*?~~", re.S)
hits=[]
for f,pats in (("HANDOFF_TO_GATE.md",["대체를 배제했다","정확히 반대다","LAM_NE·LLI 는 겹친다"]),("INTRO.md",["우리 대체 탓이 아니다","순위가 통째로 뒤집힌다","식별 가능성은 두 셀에서 **똑같다**","대조가 배제한 것은"])):
    t=strike.sub("",doc(f))
    for pat in pats:
        for i,l in enumerate(t.splitlines(),1):
            if pat in l: hits.append(f"{f}:{i} '{pat}'")
say("FINDING" if hits else "PASS", "C16 철회 문장 잔존", "취소선 없이 남은 §0-2 철회 문장: " + "; ".join(hits))
# ── C17 README ↔ 코드 ──────────────────────────────────────────────────────
sys.path.insert(0,str(ROOT)); from bms_balancing import verify as V
ok = V.EXIT_BY_STATUS=={"complete":0,"anchor_mismatch":1,"model_mismatch":1,"incomplete":2,"empty":2,"invalid":2,"partial":3} and "명시 옵션 → 파일 선언 → 추정" in V.resolve_precision.__doc__
rs=(ROOT/"scripts/run_states.sh").read_text(); ok2=all(x in rs for x in ('STATES="${STATES:-100 200 300_0147}"','STARTS="${STARTS:-24}"','SI="${SI:-Li}"','FORCE_SRC="${SRC:-}"','OUT="${OUT:-out}"'))
hp=subprocess.run([sys.executable,"-m","bms_balancing.verify","eval","--help"],capture_output=True,text=True).stdout
readme_flags=set(re.findall(r"--[a-z][a-z-]+",doc("README.md"))); missing=[f for f in readme_flags if f not in hp]
say("PASS" if ok and ok2 and not missing else "FINDING", "C17 README↔코드", f"종료 코드 표={ok} · run_states 기본값(100 200 300_0147 / 24 / Li / SRC / OUT)={ok2} · README 플래그 중 argparse 에 없는 것 {missing}")
# ── C18 192 값은 scale 을 안 탄다 ───────────────────────────────────────────
src=(ROOT/"bms_balancing/verify.py").read_text(encoding="utf-8"); msrc=(ROOT/"bms_balancing/model.py").read_text(encoding="utf-8")
ev=src[src.index("def cmd_eval"):src.index("def cmd_eval")+4000]
raw_used = 'obj.rmse_pocv(q) for q in P' in ev and "scales" not in ev.split("cols = [")[1].split("print(lines[0])")[0]
rp=msrc[msrc.index("def rmse_pocv"):msrc.index("def rmse_dvdq")]; raw_def = "scales" not in rp
er=float(re.search(r"state=300_0009 source=GITT si=Li.*?pocv:.*?eps_rel=([0-9.e+-]+)", "\n".join(lines)).group(1)); rawmean=2.220446049250313e-16/er
r3=[float(x) for x in [l for l in (OUT/"recompare/dd_eval_300_Li_r2.csv").read_text().splitlines() if l and not l.startswith(("#","a_PE"))][2].split(",")]
say("FINDING" if raw_used and raw_def else "PASS", "C18 192 값 ↔ scale", f"cmd_eval 은 obj.rmse_* (raw) 를 찍고 rmse_pocv 정의에 scales 없음={raw_used and raw_def}; 300 build 의 pocv scale ≈ eps/eps_rel = {rawmean:.4f} V 인데 recompare 행 3 rmse_pocv = {r3[5]:.6f} V (raw; scale 로 나눴다면 {r3[5]/rawmean:.4f}) → §0-1·§1-13 이 U13 을 '192 값의 조건' 으로 묶은 것은 대상이 틀렸다")
# ── C20 seed/문턱 여유 ─────────────────────────────────────────────────────
say("INFO", "C20 seed·1e-9 여유", f"eps_rel 최대 {max(eps):.2e} vs SCALE_EQUIV_REL 1e-9 → 여유 {1e-9/max(eps):.1e} 배; flag 가 뒤집히려면 하위절반평균이 {2.220446049250313e-16/1e-9:.1e} V 아래여야 한다 (실측 ≈ {rawmean:.3f} V) — seed 는 verdict 에 무관, 단 1e-9 의 근거는 model.py 주석 '비교기 MODEL_REL 과 같은 크기' 뿐")
print("\n요약:", status)
