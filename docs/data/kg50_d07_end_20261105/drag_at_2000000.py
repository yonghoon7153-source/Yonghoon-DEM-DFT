"""D0.7 압축 중 감쇠 저항 몫 — 정지 직전 atom 덤프 하나 (step 2,000,000) · 읽기 전용 (11-05 · 1저자 Q1 예).

감쇠 저항 = −γ Σ v_z (`fix damp all viscous 0.5` · F = −γ v · 질량과 무관) = DEMP-01 방법 · 덤프 읽기 = 기존 도구
docs/data/ps73_damping_branch_20261007/analyze_branch.py 의 read_atoms 그대로 · 절대값 합 γΣ|v_z| (Q5 등록 R5) · 상별 = 같은 덤프 한 번 더.
판 힘 = 로그 같은 step 의 pressMPa × 0.0025 × 1e6 (덱 식 current_press = |f_z| / 0.0025 / 1e6 의 역).
usage: python3 -P drag_at_2000000.py <리포> <atom_2000000.liggghts> <kg50_d07_b50_log_main1103.liggghts>
"""
import sys, re
sys.path.insert(0, sys.argv[1] + '/docs/data/ps73_damping_branch_20261007')
import analyze_branch as AB
dump, log = sys.argv[2], sys.argv[3]
a = AB.read_atoms(dump)                      # 기존 도구 (DEMP-01): Σ v_z
# 절대값 합 · 상별 (같은 덤프 · 따로 한 번 더 읽기)
cols = None; s_abs = {}; s_vz = {}; n = {}
with open(dump) as fh:
    for line in fh:
        if line.startswith('ITEM: ATOMS'):
            cols = line.split()[2:]; it, iv = cols.index('type'), cols.index('vz'); continue
        if cols is None: continue
        w = line.split(); t = w[it]; vz = float(w[iv])
        s_abs[t] = s_abs.get(t, 0.0) + abs(vz); s_vz[t] = s_vz.get(t, 0.0) + vz; n[t] = n.get(t, 0) + 1
p = None
for line in open(log):
    m = re.match(r'^\s*2000000\s+(\d+)\s+\S+\s+\S+\s+(\S+)\s*$', line)
    if m: p = float(m.group(2)); natoms_log = int(m.group(1))
F = p * 0.0025 * 1e6                          # 덱 식 current_press = |f_z| / 0.0025 / 1e6 → 판 힘 (덱 단위 N)
g = 0.5
drag_signed = -g * a['sum_vz']; drag_abs = g * sum(s_abs.values())
print(f"step {a['step']} · 원자 {a['n']} (로그 {natoms_log}) · 판 압력 {p*1000:.3f} MPa · 판 힘 {F:.2f} N (목표 750 N)")
print(f"감쇠 저항 (부호 있는 합 −γΣv_z) = {drag_signed:.2f} N = 판 힘의 {100*drag_signed/F:.1f} % = {drag_signed/2500*1000:.1f} MPa 상당")
print(f"절대값 합 γΣ|v_z| (Q5 R5) = {drag_abs:.2f} N = 판 힘의 {100*drag_abs/F:.1f} %")
print(f"→ 접촉망이 진 몫 (판 힘 − 감쇠, 정적 근사) = {(F-drag_signed)/2500*1000:.1f} MPa 상당")
for t in sorted(n):
    print(f"  type {t}: n {n[t]} · Σv_z {s_vz[t]:.6g} · 저항 {-g*s_vz[t]:.2f} N · 평균 v_z {s_vz[t]/n[t]:.4g}")
