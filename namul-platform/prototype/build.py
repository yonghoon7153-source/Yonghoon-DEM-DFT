"""template.html + Pretendard subset (woff2) + Fluent icons → nm_prototype.html (self-contained)."""
import base64, io, json, re, sys
from fontTools import subset
from fontTools.ttLib import TTFont
S = "/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/a9086aab-2880-555b-a3e5-137ced4672cf/scratchpad"
tpl = open(f"{S}/proto/template.html", encoding="utf-8").read()
icons = json.load(open(f"{S}/proto/build/icons.json"))
# glyph set: every char in the page + KS X 1001 Hangul (2,350 common syllables) + ASCII + common symbols
ks = "".join(bytes([hi, lo]).decode("euc-kr") for hi in range(0xB0, 0xC9) for lo in range(0xA1, 0xFF))
text = set(tpl) | set(ks) | set(chr(c) for c in range(0x20, 0x7F)) | set("·•…→←↑↓×÷±%‘’“”〈〉「」『』①②③④⑤₩~—–★☆✓")
font = TTFont(f"{S}/fonts/pretendard/public/variable/PretendardVariable.ttf")
opt = subset.Options(); opt.flavor = "woff2"; opt.layout_features = ["*"]; opt.name_IDs = ["*"]; opt.notdef_outline = True
sub = subset.Subsetter(opt); sub.populate(text="".join(text)); sub.subset(font)
buf = io.BytesIO(); font.flavor = "woff2"; font.save(buf)
b64 = base64.b64encode(buf.getvalue()).decode()
face = '@font-face{font-family:"Pretendard";src:url(data:font/woff2;base64,' + b64 + ') format("woff2");font-weight:45 920;font-style:normal;font-display:swap}'
out = tpl.replace("/*@FONTFACE@*/", face).replace("/*@ICONS@*/{}", json.dumps(icons))
assert "/*@" not in out
open(f"{S}/proto/nm_prototype.html", "w", encoding="utf-8").write(out)
print("font woff2 %.0f KB, page %.0f KB" % (len(buf.getvalue()) / 1024, len(out.encode()) / 1024))
