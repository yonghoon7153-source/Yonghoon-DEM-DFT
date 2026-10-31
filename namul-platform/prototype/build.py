"""template.html + Pretendard 서브셋(woff2) + Fluent 아이콘(icons.json) → nm_prototype.html (한 파일).

사용: python3 build.py
  - 기본: 같은 폴더의 pretendard-subset.woff2 를 그대로 넣는다 (KS X 1001 한글 2,350자 + 영숫자 + 자주 쓰는 기호).
  - PRETENDARD_TTF=<PretendardVariable.ttf 경로> python3 build.py : 페이지에 쓴 글자까지 포함해 서브셋을 새로 만든다 (fonttools 필요).
글꼴: Pretendard (SIL OFL 1.1, PRETENDARD_LICENSE.txt) · 아이콘: Microsoft Fluent Emoji (MIT, FLUENT_LICENSE.txt)"""
import base64, io, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
icons = json.load(open(os.path.join(HERE, "icons.json"), encoding="utf-8"))
woff_path = os.path.join(HERE, "pretendard-subset.woff2")
ttf = os.environ.get("PRETENDARD_TTF")
if ttf:
    from fontTools import subset
    from fontTools.ttLib import TTFont
    ks = "".join(bytes([hi, lo]).decode("euc-kr") for hi in range(0xB0, 0xC9) for lo in range(0xA1, 0xFF))
    text = set(tpl) | set(ks) | set(chr(c) for c in range(0x20, 0x7F)) | set("·•…→←↑↓×÷±%‘’“”〈〉「」『』①②③④⑤₩~—–★☆✓")
    font = TTFont(ttf)
    opt = subset.Options(); opt.flavor = "woff2"; opt.layout_features = ["*"]; opt.name_IDs = ["*"]; opt.notdef_outline = True
    sub = subset.Subsetter(opt); sub.populate(text="".join(text)); sub.subset(font)
    buf = io.BytesIO(); font.flavor = "woff2"; font.save(buf)
    open(woff_path, "wb").write(buf.getvalue())
missing = sorted({c for c in tpl if ord(c) > 0x3000 and c not in "".join(bytes([hi, lo]).decode("euc-kr", "ignore") for hi in range(0xB0, 0xC9) for lo in range(0xA1, 0xFF))})
if missing and not ttf: print("note: KS X 1001 밖 글자는 대체 글꼴로 보일 수 있음:", "".join(missing[:40]))
woff = open(woff_path, "rb").read()
face = '@font-face{font-family:"Pretendard";src:url(data:font/woff2;base64,' + base64.b64encode(woff).decode() + ') format("woff2");font-weight:45 920;font-style:normal;font-display:swap}'
out = tpl.replace("/*@FONTFACE@*/", face).replace("/*@ICONS@*/{}", json.dumps(icons))
assert "/*@" not in out
open(os.path.join(HERE, "nm_prototype.html"), "w", encoding="utf-8").write(out)
print("font woff2 %.0f KB, page %.0f KB" % (len(woff) / 1024, len(out.encode()) / 1024))
