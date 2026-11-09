import math
from scipy.optimize import brentq

def lame(E, nu):
    mu = E/(2*(1+nu)); la = E*nu/((1+nu)*(1-2*nu)); return mu, la

def uniaxial(E, nu, sy, sign, dim=3):
    """Uniaxial stress, lateral stress 0. Fixed-corotated Kirchhoff tau = 2mu(F-R)F^T + la J(J-1) I.
    Yield: ||dev log s|| = sy/(2mu).  sign=-1 compression (s1<1), +1 tension."""
    mu, la = lame(E, nu)
    # dev-norm of (ln s1, ln s2, ln s2) = sqrt(2/3)|ln(s1/s2)| in 3D (2 laterals)
    # in plane-strain 2D (s3=1 out-of-plane, only s1, s2 in-plane): we skip
    r = sy/(2*mu)*math.sqrt(1.5)   # |ln(s1/s2)|
    def lat(s2):
        s1 = s2*math.exp(sign*r)
        J = s1*s2*s2
        return 2*mu*(s2-1)*s2 + la*J*(J-1)
    s2 = brentq(lat, 0.5, 1.5)
    s1 = s2*math.exp(sign*r); J = s1*s2*s2
    tau11 = 2*mu*(s1-1)*s1 + la*J*(J-1)
    return tau11, tau11/J, J, s1, s2

for (E,nu) in [(1.53,0.49),(22.06,0.36),(24.0,0.30),(1.35,0.30),(1.53,0.30)]:
    for sgn,name in [(-1,'comp'),(+1,'tens')]:
        t,c,J,s1,s2 = uniaxial(E,nu,0.30,sgn)
        print(f"E={E:6.2f} nu={nu:.2f} {name}: Kirchhoff {t:+.4f}  Cauchy {c:+.4f}  J={J:.5f} s1={s1:.4f} s2={s2:.4f}")
print("sqrt(3/2)*0.30 =", math.sqrt(1.5)*0.30)
mu,la=lame(1.53,0.49); print("soft mu,la,K",mu,la,la+2*mu/3)
mu,la=lame(22.06,0.36); print("real mu,la,K",mu,la,la+2*mu/3)
print("E/sy real:", 22.06/0.363, 22.06/0.30, "E/sy unaxial comp exact", 22.06/uniaxial(22.06,0.36,0.30,-1)[1])
