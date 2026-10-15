"""Same immutable OFF probe, changing only old-source and output paths in memory."""
from pathlib import Path
p=Path(__file__).with_name('off_compatibility.py')
src=p.read_text(encoding='utf8')
src=src.replace("R/'source_prior/step3_sigma.py'", "R/'source_prior/step3_sigma_before_fix.py'")
src=src.replace("R/'evidence/off_compatibility.json'", "R/'evidence/off_before_fix.json'")
exec(compile(src,str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
