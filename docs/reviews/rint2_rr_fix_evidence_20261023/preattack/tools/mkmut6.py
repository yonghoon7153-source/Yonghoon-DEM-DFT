"""M6: RCA2-06 F4 source mutation — upper end removes only the FIRST unsplit component's SDCP cells (labels/census unchanged)."""
import os, shutil
A = os.environ['ATK_ROOT']  # 리뷰어 작업 폴더 (new_src · old_src · mut · logs · tmp · tools) — 리포 사본에서 바꾼 줄
SRC = os.path.join(A, 'new_src')
MUTS = {
    'M6_upper_first_component_only': ('scripts/carbon_junction.py',
        "lins = np.flatnonzero(np.isin(g['labf'], labels)) if labels else np.zeros(0, np.int64)",
        "lins = np.flatnonzero(np.isin(g['labf'], labels[:1])) if labels else np.zeros(0, np.int64)"),
    # M8: R-monotone guard disabled (does the resident test catch a no-op guard?)
    'M8_rmono_guard_noop': ('scripts/rint_r_chain.py',
        "    def _r_monotone(self):\n",
        "    def _r_monotone(self):\n        return\n"),
    # M9: fsum guard removed on final U (RCA2-08) — does the resident test catch it?
}
for nm, (rel, old, new) in MUTS.items():
    dst = os.path.join(A, 'mut', nm)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(SRC, dst, symlinks=True)
    p = os.path.join(dst, rel)
    t = open(p, encoding='utf-8').read()
    assert t.count(old) == 1, (nm, t.count(old))
    open(p, 'w', encoding='utf-8').write(t.replace(old, new))
    print(nm, 'ok')
