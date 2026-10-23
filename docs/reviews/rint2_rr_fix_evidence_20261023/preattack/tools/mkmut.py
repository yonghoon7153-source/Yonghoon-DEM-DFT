"""Create mutant trees (copies of new_src) with one textual replacement each in scripts/ca_ext_svcf.py (or another file)."""
import shutil, sys, os, json
A = os.environ['ATK_ROOT']  # 리뷰어 작업 폴더 (new_src · old_src · mut · logs · tmp · tools) — 리포 사본에서 바꾼 줄
SRC = os.path.join(A, 'new_src')
MUTS = {
    'M1_divdir_nearest': ('scripts/ca_ext_svcf.py',
                          '    q = Fraction(a) / Fraction(b)\n',
                          '    return a / b\n    q = Fraction(a) / Fraction(b)\n'),
    'M2_hi_uses_upper_target_hi': ('scripts/ca_ext_svcf.py',
                                   "_div_dir(full[1], hi_end[0], up=True)", "_div_dir(full[1], hi_end[1], up=True)"),
    'M3_lo_uses_lower_target_lo': ('scripts/ca_ext_svcf.py',
                                   "_div_dir(full[0], lo_end[1], up=False)", "_div_dir(full[0], lo_end[0], up=False)"),
    'M4_lo_uses_full_hi': ('scripts/ca_ext_svcf.py',
                           "_div_dir(full[0], lo_end[1], up=False)", "_div_dir(full[1], lo_end[1], up=False)"),
    'M5_hi_uses_full_lo': ('scripts/ca_ext_svcf.py',
                           "_div_dir(full[1], hi_end[0], up=True)", "_div_dir(full[0], hi_end[0], up=True)"),
    'M7_divdir_swapped': ('scripts/ca_ext_svcf.py',
                          "    if up and fq < q:\n        f = math.nextafter(f, math.inf)\n    elif not up and fq > q:\n        f = math.nextafter(f, -math.inf)\n",
                          "    if (not up) and fq < q:\n        f = math.nextafter(f, math.inf)\n    elif up and fq > q:\n        f = math.nextafter(f, -math.inf)\n"),
}
names = sys.argv[1:] or list(MUTS)
for nm in names:
    rel, old, new = MUTS[nm]
    dst = os.path.join(A, 'mut', nm)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(SRC, dst, symlinks=True)
    p = os.path.join(dst, rel)
    t = open(p, encoding='utf-8').read()
    assert t.count(old) == 1, (nm, t.count(old))
    open(p, 'w', encoding='utf-8').write(t.replace(old, new))
    print(nm, 'ok')
