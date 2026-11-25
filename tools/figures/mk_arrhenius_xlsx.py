import numpy as np, json, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

R = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
OUT = R/"docs/figures/seminar_2026_09_07/arrhenius_3sys_2026-09-07.xlsx"
GEN = {g["id"]: g for g in json.loads(
    (R/"db/properties/md_protocol_generations.json").read_text(encoding="utf-8")
)["generations"]}["gen0_pre_gate"]

A="Arial"
HF=PatternFill("solid",fgColor="1F2937"); HFONT=Font(name=A,bold=True,color="FFFFFF",size=10)
IN=Font(name=A,color="0000FF",size=10); FM=Font(name=A,color="000000",size=10)
WARN=Font(name=A,bold=True,color="B91C1C",size=10); BODY=Font(name=A,size=10)
TH=Border(*[Side(style="thin",color="D1D5DB")]*4)

kB=8.617333262e-5; T=[600.,800.,1000.]
SYS=[("LPSCl1.6",[1.037e-05,2.845e-05,4.728e-05],0.197,0.032,2.220e22,"baseline"),
     ("LPSOCl1.6",[6.2705e-06,2.4162e-05,5.7093e-05],0.287,0.024,2.242e22,"baseline"),
     ("B2O3@LPSCl1.6",[1.041e-05,2.163e-05,5.081e-05],0.199,0.034,2.381e22,"RETRACTED 2026-08-25")]

def hdr(ws,row,cols,ws_w):
    for j,(c,w) in enumerate(zip(cols,ws_w),1):
        x=ws.cell(row=row,column=j,value=c); x.fill,x.font,x.border=HF,HFONT,TH
        x.alignment=Alignment(horizontal="center",wrap_text=True)
        ws.column_dimensions[get_column_letter(j)].width=w

wb=Workbook(); wb.remove(wb.active)

# ── Params ───────────────────────────────────────────────────────────────
ws=wb.create_sheet("Params")
ws["A1"]="물리상수 (파란 글씨 = 고정 입력, 검정 = 수식)"; ws["A1"].font=Font(name=A,bold=True,size=11)
for i,(lab,v) in enumerate([("e  [C]",1.602176634e-19),("k_B  [J/K]",1.380649e-23),
                            ("k_B  [eV/K]",8.617333262e-05)],2):
    ws.cell(row=i,column=1,value=lab).font=BODY
    c=ws.cell(row=i,column=2,value=v); c.font=IN; c.number_format="0.000000E+00"
ws.cell(row=5,column=1,value="T_RT [K]").font=BODY
c=ws.cell(row=5,column=2,value=300.0); c.font=IN
hdr(ws,7,["system","Ea_ledger_eV","Ea_err_eV","Ea_fit_eV\n(이 3점 적합)","lnD0","D0_cm2_s",
          "R2","n_Li_cm-3","status"],[22,13,11,14,11,13,9,13,22])
P={}
for r,(name,D,El,err,n,st) in enumerate(SYS,8):
    y=np.log(D); x=[1000/t for t in T]; p=np.polyfit(x,y,1)
    Ea=-p[0]*kB*1000; lnD0=p[1]
    r2=1-((y-np.polyval(p,x))**2).sum()/((y-y.mean())**2).sum()
    P[name]=(r,Ea,lnD0,err,n)
    for j,v in enumerate([name,El,err,round(Ea,6),round(lnD0,6),None,round(r2,5),n,st],1):
        c=ws.cell(row=r,column=j,value=v); c.border=TH
        c.font=IN if j in (2,3,4,5,8) else BODY
    ws.cell(row=r,column=6,value=f"=EXP(E{r})").font=FM
    ws.cell(row=r,column=6).number_format="0.000E+00"
    ws.cell(row=r,column=8).number_format="0.000E+00"
    if st.startswith("RETRACTED"): ws.cell(row=r,column=9).font=WARN
ws["A12"]=("⚠ Ea_ledger 와 Ea_fit 이 최대 2.2 meV 다릅니다. 원장값은 시드별 적합의 평균이고, 여기 적합은 "
           "시드평균 D 3점의 최소제곱선입니다(Jensen). 그림의 선은 Ea_fit 쪽입니다.")
ws["A12"].font=Font(name=A,size=9,italic=True)
ws["A13"]="⚠ Ea_err 는 600 K 멀티시드 산포입니다 — 평균의 신뢰구간이 아니라 run-to-run 변동입니다."
ws["A13"].font=Font(name=A,size=9,italic=True)

# ── Data ─────────────────────────────────────────────────────────────────
ws=wb.create_sheet("Data")
hdr(ws,1,["system","T_K","1000/T [1/K]","D_cm2_s","ln D","n_Li_cm-3","sigma_mS/cm","status"],
    [22,8,14,13,11,13,13,22])
r=2
for name,D,El,err,n,st in SYS:
    for t,d in zip(T,D):
        ws.cell(row=r,column=1,value=name).font=BODY
        ws.cell(row=r,column=2,value=t).font=IN
        ws.cell(row=r,column=3,value=f"=1000/B{r}").font=FM
        c=ws.cell(row=r,column=4,value=d); c.font=IN; c.number_format="0.0000E+00"
        ws.cell(row=r,column=5,value=f"=LN(D{r})").font=FM
        ws.cell(row=r,column=5).number_format="0.0000"
        c=ws.cell(row=r,column=6,value=n); c.font=IN; c.number_format="0.000E+00"
        ws.cell(row=r,column=7,value=f"=1000*F{r}*Params!$B$2^2*D{r}/(Params!$B$3*B{r})").font=FM
        ws.cell(row=r,column=7).number_format="0.0"
        ws.cell(row=r,column=8,value=st).font=WARN if st.startswith("RETRACTED") else BODY
        for j in range(1,9): ws.cell(row=r,column=j).border=TH
        r+=1
ws.cell(row=r+1,column=1,value="⚠ sigma 는 Haven ratio H_R=1 을 **가정**한 값입니다 — 상한이 아닙니다. READ_ME 참조.").font=WARN

# ── FitLines ─────────────────────────────────────────────────────────────
ws=wb.create_sheet("FitLines")
hdr(ws,1,["1000/T [1/K]","T_K","lnD_LPSCl1.6","lnD_LPSOCl1.6","lnD_B2O3 (RETRACTED)",
          "구간"],[14,9,15,16,21,26])
xs=np.round(np.arange(0.95,3.3401,0.01),4)
for i,xv in enumerate(xs,2):
    ws.cell(row=i,column=1,value=float(xv)).font=IN
    ws.cell(row=i,column=2,value=f"=1000/A{i}").font=FM
    ws.cell(row=i,column=2).number_format="0.0"
    for j,pr in enumerate((8,9,10),3):
        ws.cell(row=i,column=j,
                value=f"=Params!$E${pr}-(Params!$D${pr}/Params!$B$4)*(A{i}/1000)").font=FM
        ws.cell(row=i,column=j).number_format="0.0000"
    lab="측정 구간 (600-1000 K)" if xv<=1.6667+1e-9 else "⚠ 외삽 (측정 밖)"
    c=ws.cell(row=i,column=6,value=lab); c.font=BODY if xv<=1.6667+1e-9 else WARN
    for j in range(1,7): ws.cell(row=i,column=j).border=TH
ws.cell(row=len(xs)+3,column=1,value=(
  "측정 구간은 1000/T = 1.00~1.67 (600~1000 K) 입니다. 그 밖은 '⚠ 외삽' 으로 표시했습니다 — "
  "그림에서는 실선/점선을 나눠 그려 주세요.")).font=WARN

# ── RT_extrapolation ─────────────────────────────────────────────────────
ws=wb.create_sheet("RT_extrapolation")
ws["A1"]="300 K 외삽 — 우리 적합선을 그대로 연장한 값 (1저자 요청 2026-09-07)"
ws["A1"].font=Font(name=A,bold=True,size=12)
ws["A2"]=("⚠ 이 시트의 값은 **측정 밖**입니다. 적합 구간(1000/T 1.00~1.67)의 끝점에서 2배 지점(3.33)까지 "
          "늘린 것이고, 아래 밴드는 Ea 오차막대(±1σ)만 반영한 것입니다 — 그것만으로도 6~14배 벌어집니다.")
ws["A2"].font=WARN
ws["A3"]="⛔ 논문·발표 인용 불가. 내부 비교·감각용으로만 쓰세요. 사유는 READ_ME 시트."
ws["A3"].font=WARN
hdr(ws,5,["system","Ea_fit_eV","Ea_err_eV","D(300K)_cm2_s","sigma(300K)_mS/cm",
          "sigma −1σ","sigma +1σ","배율폭","status"],[22,11,11,15,17,12,12,9,22])
for k,(name,D,El,err,n,st) in enumerate(SYS):
    pr=P[name][0]; r=6+k
    ws.cell(row=r,column=1,value=name).font=BODY
    ws.cell(row=r,column=2,value=f"=Params!$D${pr}").font=FM
    ws.cell(row=r,column=2).number_format="0.0000"
    ws.cell(row=r,column=3,value=f"=Params!$C${pr}").font=FM
    ws.cell(row=r,column=3).number_format="0.000"
    ws.cell(row=r,column=4,value=f"=Params!$F${pr}*EXP(-B{r}/(Params!$B$4*Params!$B$5))").font=FM
    ws.cell(row=r,column=4).number_format="0.000E+00"
    ws.cell(row=r,column=5,
        value=f"=1000*Params!$H${pr}*Params!$B$2^2*D{r}/(Params!$B$3*Params!$B$5)").font=FM
    # ±1σ : Ea 를 err 만큼 올리면(느려짐) 하한, 내리면 상한
    for col,sgn in ((6,"+"),(7,"-")):
        ws.cell(row=r,column=col,
            value=(f"=1000*Params!$H${pr}*Params!$B$2^2*"
                   f"(Params!$F${pr}*EXP(-(B{r}{sgn}C{r})/(Params!$B$4*Params!$B$5)))"
                   f"/(Params!$B$3*Params!$B$5)")).font=FM
    for col in (5,6,7): ws.cell(row=r,column=col).number_format="0.00"
    ws.cell(row=r,column=8,value=f"=G{r}/F{r}").font=FM
    ws.cell(row=r,column=8).number_format='0.0"배"'
    ws.cell(row=r,column=9,value=st).font=WARN if st.startswith("RETRACTED") else BODY
    for j in range(1,10): ws.cell(row=r,column=j).border=TH
for i,t in enumerate([
  "",
  "■ 이 값을 읽을 때 같이 기억할 것",
  "1) B2O3 는 직선이 아닙니다 — 600→800 구간 Ea 0.151 eV, 800→1000 구간 0.294 eV (145 meV 차).",
  "   굽은 선을 300 K 까지 늘린 값이라 위 밴드보다도 더 불확실합니다. 이 축은 2026-08-25 철회됐습니다.",
  "2) ⚠ sigma 는 Haven ratio H_R = 1 을 가정한 값입니다 — **상한이 아닙니다.** H_R = D*/D_sigma 규약에서",
  "   H_R<1 이면 NE 는 오히려 과소입니다. 저희 궤적에서 직접 재 보니 H_R ~ 0.84 (600-1200 K, 방향 판별용)",
  "   라 보정은 +19 % 뿐이고 아래 밴드(12배) 안에 잠기므로 **이 표에는 적용하지 않았습니다.**",
  "   문헌값(Adeli 2019: 300 K 다결정 펠릿, H_R=0.23)은 조건이 달라 이 MD 값에 곱하면 안 됩니다.",
  "3) MD 는 NVT(부피 고정)라 열팽창이 없습니다. 300 K 의 실제 격자는 이 셀과 다릅니다.",
  "4) 밴드는 Ea 오차만 반영합니다 — D0 불확실도·곡률·프로토콜 편향은 안 들어가 있습니다 (즉 실제는 더 넓습니다).",
 ],start=10):
    c=ws.cell(row=i,column=1,value=t)
    c.font=Font(name=A,bold=True,size=11) if t.startswith("■") else (WARN if t.startswith(("1)","2)","3)","4)","   ")) else BODY)

# ── READ_ME ──────────────────────────────────────────────────────────────
ws=wb.create_sheet("READ_ME"); ws.column_dimensions["A"].width=120
L=[("Arrhenius — LPSCl1.6 / LPSOCl1.6 / B2O3@LPSCl1.6   (2026-09-07)","t"),("",""),
 ("■ 시트 안내","h"),
 ("Params            : 적합 파라미터. 파란 글씨만 입력이고 나머지는 수식 — Ea 를 바꾸면 다른 시트가 따라 움직입니다.",""),
 ("Data              : 측정점 9개 (3계 × 600/800/1000 K). sigma 는 D 에서 계산된 수식입니다.",""),
 ("FitLines          : 그림의 직선. 1000/T 를 x, lnD_* 를 y 로 그리세요. '구간' 열이 측정/외삽을 갈라 줍니다.",""),
 ("RT_extrapolation  : 300 K 외삽값 + Ea 오차 밴드.",""),("",""),
 ("■ sigma 와 Ea 는 서로 다른 층위입니다","h"),
 ("⚠ 2026-09-07 정정: 저희가 종전에 sigma 를 'NE upper bound' 라고 적었는데 **부호가 틀렸습니다.**","w"),
 ("   H_R = D*/D_sigma 이고 MD 는 D*(tracer) 를 주므로 sigma_NE = H_R x sigma_true 입니다. H_R<1 이면 과소입니다.","w"),
 ("   저희 궤적에서 직접 쟀더니 H_R ~ 0.84 (600-1200 K, 6 계·온도점) — 보정 크기가 +19 % 라 이 파일에는",""),
 ("   적용하지 않았습니다(외삽 밴드 12배 안에 잠깁니다). 문헌값 H_R=0.23 은 300 K 다결정 펠릿 조건이라",""),
 ("   이 MD 값에 곱하면 안 됩니다.",""),
 ("",""),
 ("■ 실험 펠릿값(3.3~10.8 mS/cm)보다 높게 나오는 이유","h"),
 ("1) 저온 외삽. 적합 구간은 1000/T = 1.00~1.67(600~1000 K)이고 300 K 는 3.33 — 측정 끝점의 2배 지점입니다.","w"),
 ("   Ea 오차막대(±1σ)만 넣어도 sigma(300 K) 가 12배 벌어집니다. 대부분의 격차가 이 밴드에 잠깁니다.","w"),
 ("2) D* 자체가 높습니다. 우리 D*(300 K) 외삽 2.31e-7 vs Adeli 7Li PFG 실측 1.01e-7 cm^2/s — 2.3배.",""),
 ("   (단일시드 한 궤적만 쓰면 1.02e-7 로 거의 일치하지만 3시드 평균이 아니라 인용하지 않습니다.)",""),
 ("3) 입계·기공이 없음. MD 는 순수 bulk 단결정, 실험 EIS 는 냉간압축 펠릿(GB + 잔류 기공)입니다.",""),
 ("4) S/Cl disorder 정도. argyrodite 는 여기 극단적으로 민감합니다 — Ou et al., Phys. Rev. Mater. 8,",""),
 ("   115407 (2024): ordered 0.2 vs 50% disordered 29.8 mS/cm, 150배. 셀 배치가 실제 시료와 같은지는 별도 확인.",""),
 ("⇒ Haven 은 이 목록에 없습니다 — 위에서 보듯 +19 % 이고 방향도 반대(격차를 넓힙니다).","w"),
 ("sigma(T) = n · e² · D(T) / (k_B · T)    ← 그 온도의 D 하나만 씁니다. 다른 온도 정보가 안 들어갑니다.",""),
 ("Ea       = ln D vs 1/T 직선의 기울기     ← 세 점 전부를 써서 계마다 하나 나옵니다.",""),
 ("⚠ sigma 를 Arrhenius 로 그릴 때는 sigma 가 아니라 sigma×T 를 세로축에 두세요.","w"),
 ("   1/T 인자 때문에 ln(sigma) 기울기가 ln(D) 기울기보다 0.065 eV 낮게 나옵니다 (우리 데이터 실측).",""),("",""),
 ("■ 300 K 외삽에 대하여","h"),
 ("요청하신 값은 RT_extrapolation 시트에 넣었습니다. 다만 아래를 같이 봐 주세요:",""),
 ("· 외삽 거리 — 적합 구간은 1000/T = 1.00~1.67. 300 K 는 3.33 으로 측정 끝점의 **2배 지점**입니다.","w"),
 ("· Ea 오차막대만 넣어도 sigma(300 K) 가 6~14배 벌어집니다 (그 시트의 밴드).","w"),
 ("· B2O3 는 직선이 아니고(구간 Ea 0.151 vs 0.294 eV) 이 축은 2026-08-25 철회됐습니다.","w"),
 ("⇒ 내부 감각·비교용으로는 쓰실 수 있지만, 논문·발표 수치로는 인용하지 말아 주세요.","w"),("",""),
 ("■ 인용 규칙","h"),
 ("허용 : Ea 값과 오차막대 · 같은 프로토콜 안에서의 계 간 상대 비교 · MSD 곡선 모양",""),
 ("금지 : sigma 절대값 · 300 K 외삽 · B2O3 의 D/Ea/sigma(철회) · 다른 프로토콜 값과 한 표에 놓기","w"),("",""),
 ("■ 프로토콜 세대","h"),(GEN["영문_각주"],""),
 ("(UMA-s-1p1 omat · Langevin NVT dt 2 fs · MSD 창 2-50 ps 자유절편)",""),
 ("⚠ 생산 길이가 온도마다 다릅니다: 600 K = 200 ps, 800/1000 K = 100 ps. 즉 800/1000 K 는 창(2-50 ps)이","w"),
 ("   궤적의 절반입니다. 온도 간 D 를 비교할 때 이 비대칭을 같이 봐 주세요.","w"),
 ("LPSCl1.6 / B2O3 = 3 seeds × 3 T (2026-07-07) · LPSOCl1.6 = 4 seeds × 3 T (2026-07-27)",""),("",""),
 ("원자료 : db/properties/b2o3_vs_lpscl16_conductivity.csv · lpsocl_md_arrhenius.json",""),
 ("설명   : kb/concepts/msd_reading.md",""),]
for i,(t,k) in enumerate(L,1):
    c=ws.cell(row=i,column=1,value=t)
    c.font={"t":Font(name=A,bold=True,size=13),"h":Font(name=A,bold=True,size=11),
            "w":WARN}.get(k,BODY)

wb.calculation.fullCalcOnLoad=True   # ⚠ LibreOffice 재계산 불가 환경 → 열 때 강제 재계산
wb._sheets=[wb["READ_ME"],wb["Data"],wb["FitLines"],wb["RT_extrapolation"],wb["Params"]]
OUT.parent.mkdir(parents=True,exist_ok=True); wb.save(OUT); print("saved:",OUT)
