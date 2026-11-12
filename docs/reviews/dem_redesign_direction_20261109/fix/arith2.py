import math
L13=math.log(1.3); L115=math.log(1.15)
f=lambda n:4/n-72/n**2
qinf=0.25; qq=[qinf+f(n) for n in (12,16,24)]
d1=qq[1]-qq[0]; d2=qq[2]-qq[1]; lo=min(qq[2],qq[2]+3*d2)-0.02; hi=max(qq[2],qq[2]+3*d2)+0.02
print('two-term qinf 0.25: q',[round(x,4) for x in qq],'d1',round(d1,4),'d2',round(d2,4),'ratio',round(d2/d1,3),'interval',round(lo,4),round(hi,4),'lo>=ln1.3?',lo>=L13,'truth R',round(math.exp(qinf),4),'limit below lo by',round(lo-qinf,4))
# geometric ladder 16,24,36
p=0.72; print('geom ladder ratio (2/3)^0.72',round((2/3)**0.72,4),'(2/3)^3.08',round((2/3)**3.0816,4))
# D2: LE25 Fig1d -ln eps
y={100:1.24,150:1.41,300:1.90}
D={k:1-math.exp(-v) for k,v in y.items()}
print('LE25 D',{k:round(v,4) for k,v in D.items()})
r150=D[300]/D[150]; r100=D[300]/D[100]
print('h150/h300',round(r150,4),'ln',round(math.log(r150),4),'band ln x[1/1.3,1.3]',round(math.log(r150)/1.3,4),round(math.log(r150)*1.3,4),'-> ratio',round(math.exp(math.log(r150)/1.3),4),round(math.exp(math.log(r150)*1.3),4))
print('h100/h300',round(r100,4))
# 1.64-basis slopes for reading (a): printed is crystal basis 1.860
for TD in (1.860,):
    eps={k:1-D[k]*TD/1.64 for k in D}
    print('(a)->1.64 eps',{k:round(v,4) for k,v in eps.items()},'slope100-300 e-4',round((math.log(eps[100])-math.log(eps[300]))/200*1e4,1),'slope150-300',round((math.log(eps[150])-math.log(eps[300]))/150*1e4,1))
print('(b) slope 100-300 on 1.64 basis',round((1.90-1.24)/200*1e4,1))
# Korjus thickness under load
k={76.2:480.0,127:450.0,255:381.0,382:345.2,510:331.2}
print('Korjus h127/h255',round(k[127]/k[255],4),'ln',round(math.log(k[127]/k[255]),4),'h76/h510',round(k[76.2]/k[510],4))
# DO20J after unload rel dens
print('DO20J D250/D150',round(75.4/70.3,4),'D370/D150',round(77.2/70.3,4))
# porosity conversions
def e(rho,TD): return 100*(1-rho/TD)
print('DO20A 1.522: 1.64',round(e(1.522,1.64),1),'1.860',round(e(1.522,1.860),1))
for rho in (1.47,1.54,1.37,1.46,1.50):
    print('CR21',rho,'1.64',round(e(rho,1.64),1),'1.86',round(e(rho,1.86),1))
print('Ohno 86.7% @1.86 -> rho',round(0.867*1.86,4),'1.64 eps',round(e(0.867*1.86,1.64),1),'range 81-95 ->',round(e(0.81*1.86,1.64),1),round(e(0.95*1.86,1.64),1))
print('Ohno D 1.655 -> 1.64',round(e(1.655,1.64),2))
# color counts final/reduced boxes
lim=43.8
for name,Lx,pts in (('final 50x50x30',400,33.0),('reduced 25x25x30',200,8.25)):
    for h,tag in ((44.0,'DEM pour'),(30*0.88/0.35,'random 0.35')):
        nz=round(h/0.125); nodes=Lx*Lx*nz; base=nodes*24/1e9; col=nodes*36/1e9
        print(name,tag,'h',round(h,1),'nodes M',round(nodes/1e6,1),'base GB',round(base,2),'color GB',round(col,2),'K',int((lim-pts-base)//col))
# 2D dense vs sparse
print('2D dense 0.5M nodes x500 x36B GB',round(0.5e6*500*36/1e9,1))
for dmin in (24,):
    d=dmin/0.8; sup=(d+3)**2; print('2D sparse per-disk support nodes (bbox)',round(sup),'x500x36B MB',round(sup*500*36/1e6,1))
# c_S ratio
mu_r,mu_s=8.110294,0.513423; M_r,M_s=37.08,26.18
cs=math.sqrt(mu_r/mu_s); cl=math.sqrt(M_r/M_s)
print('cS ratio',round(cs,3),'cL ratio',round(cl,3),'real V/cS at soft 0.05',round(0.05/cs,4),'real V/cP',round(0.0070/cl,4))
print('half step ln1.5/2',round(math.log(1.5)/2,4),'factor',round(math.exp(math.log(1.5)/2),4))
print('YL26 92/545',round(92/545,3),'SG25 94/545',round(94/545,3))
