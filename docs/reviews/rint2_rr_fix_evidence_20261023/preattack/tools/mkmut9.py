"""M9: RCA2-08 source mutation — _fsum_bound no longer catches OverflowError/ValueError (old behaviour on the final sums)."""
import os, shutil
A = os.environ['ATK_ROOT']  # 리뷰어 작업 폴더 (new_src · old_src · mut · logs · tmp · tools) — 리포 사본에서 바꾼 줄
SRC = os.path.join(A, 'new_src')
nm = 'M9_fsum_no_guard'
rel = 'scripts/step3_conv_cert.py'
old = "    except (OverflowError, ValueError):\n        return math.inf, math.inf\n"
new = "    except ZeroDivisionError:\n        return math.inf, math.inf\n"
dst = os.path.join(A, 'mut', nm)
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(SRC, dst, symlinks=True)
p = os.path.join(dst, rel)
t = open(p, encoding='utf-8').read()
assert t.count(old) == 1, t.count(old)
open(p, 'w', encoding='utf-8').write(t.replace(old, new))
print(nm, 'ok')
