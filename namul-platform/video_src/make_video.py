"""슬라이드 이미지 + AI 내레이션(오프라인 한국어 TTS) + 하단 자막 → 1080p MP4 (리허설용 초안).

사용: python3 make_video.py <슬라이드 PNG 폴더> <출력.mp4> [말하기 속도, 기본 0.92]
  슬라이드 PNG 폴더: 발표자료를 PDF로 내보낸 뒤 `pdftoppm -r 192 -png deck.pdf <폴더>/s` 로 만든 s-01.png, s-02.png ...
환경 변수
  NAMUL_TTS_MODELS  sherpa-onnx 모델 폴더 (vits-mimic3-ko_KO-kss_low 가 들어 있는 곳, 기본 namul-platform/.cache/tts)
  NAMUL_SUB_FONT    자막 글꼴 TTF (기본 NanumGothic-Bold, 시스템 경로에서 찾음)
대본은 deck_src/script.json, 시연 영상 위치는 deck_src/demo_rect.json 에서 읽는다 (build_deck.js 가 만든다)."""
import glob, json, os, re, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); DECK = os.path.join(ROOT, "deck_src")
sys.path.insert(0, HERE); sys.path.insert(0, DECK)
from ko_norm import normalize
from tts_lib import synth, save_wav

SLIDES, OUT = sys.argv[1], sys.argv[2]; SPEED = float(sys.argv[3]) if len(sys.argv) > 3 else 0.92
def find_font():
    if os.environ.get("NAMUL_SUB_FONT"): return os.environ["NAMUL_SUB_FONT"]
    hits = glob.glob("/usr/share/fonts/**/NanumGothic*Bold*.ttf", recursive=True) + glob.glob(os.path.expanduser("~/.fonts/**/NanumGothic*Bold*.ttf"), recursive=True)
    if not hits: sys.exit("자막 글꼴을 찾지 못했다. NAMUL_SUB_FONT 에 한글 TTF 경로를 지정하세요.")
    return hits[0]
W, H = 1920, 1080; SW, SH = 1664, 936; SX, SY = (W - SW) // 2, 14
BG = (20, 24, 22); FONT = ImageFont.truetype(find_font(), 38)
LEAD, CHUNK_GAP, SENT_GAP, TAIL = 0.45, 0.2, 0.42, 0.7
data = json.load(open(os.path.join(DECK, "script.json"), encoding="utf-8"))
rect = json.load(open(os.path.join(DECK, "demo_rect.json"), encoding="utf-8"))
DEMO = os.path.join(ROOT, "assets/demo/demo_phone.mp4")
WORK = tempfile.mkdtemp(prefix="namul_video_"); FR = os.path.join(WORK, "frames"); os.makedirs(FR)

def chunks(sent, maxc=58):
    if len(sent) <= maxc: return [sent]
    cuts = [m.end() for m in re.finditer(r"[,.] ", sent)]
    if not cuts: return [sent]
    mid = len(sent) / 2; c = min(cuts, key=lambda k: abs(k - mid))
    return chunks(sent[:c].strip(), maxc) + chunks(sent[c:].strip(), maxc)

def wrap(text, width):
    lines, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if FONT.getlength(t) <= width: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def frame(slide_img, sub, path):
    im = Image.new("RGB", (W, H), BG); im.paste(slide_img, (SX, SY))
    if sub:
        d = ImageDraw.Draw(im); lines = wrap(sub, SW - 40)
        lh = 50; y0 = SY + SH + (H - SY - SH - lh * len(lines)) // 2 + 2
        for i, ln in enumerate(lines):
            d.text((W // 2, y0 + i * lh), ln, font=FONT, fill=(255, 255, 255), anchor="mt")
    im.save(path)

audio, segs, sr, k = [], [], None, 0
windows = {}; tcur = 0.0
def silence(sec): return np.zeros(int(round(sec * (sr or 22050))), dtype=np.float32)
for o in data:
    img = Image.open(os.path.join(SLIDES, f"s-{o['n']:02d}.png")).convert("RGB").resize((SW, SH), Image.LANCZOS)
    if not o["sentences"]:  # 부록: 4초만 보여 준다
        p = f"{FR}/f{k:04d}.png"; frame(img, None, p); k += 1
        audio.append(silence(4.0)); segs.append((p, 4.0)); tcur += 4.0; continue
    first = True; wstart = tcur
    for si, sent in enumerate(o["sentences"]):
        cs = chunks(sent)
        for ci, c in enumerate(cs):
            x, r = synth(normalize(c), SPEED); sr = sr or r
            if first:
                p = f"{FR}/f{k:04d}.png"; frame(img, None, p); k += 1
                audio.append(silence(LEAD)); segs.append((p, LEAD)); first = False; tcur += LEAD
            last_chunk = ci == len(cs) - 1; last_sent = si == len(o["sentences"]) - 1
            gap = (TAIL if last_sent else SENT_GAP) if last_chunk else CHUNK_GAP
            p = f"{FR}/f{k:04d}.png"; frame(img, c, p); k += 1
            audio.append(x); audio.append(silence(gap)); segs.append((p, len(x) / sr + gap)); tcur += len(x) / sr + gap
    windows[o["n"]] = (wstart, tcur)
wav = np.concatenate(audio); save_wav(f"{WORK}/narration.wav", wav, sr)
total = len(wav) / sr
with open(f"{WORK}/frames.txt", "w") as f:
    for p, d in segs: f.write(f"file '{p}'\nduration {d:.4f}\n")
    f.write(f"file '{segs[-1][0]}'\n")
print("segments", len(segs), "audio %.1fs (%d:%02d)" % (total, total // 60, total % 60))
json.dump(windows, open(os.path.join(HERE, "windows.json"), "w"))
# 시연 장표에서 슬라이드 속 휴대폰 틀 위치에 실제 앱 녹화를 겹친다
K = SW / 10.0
ox, oy = round(SX + rect["x"] * K), round(SY + rect["y"] * K)
ow = int(round(rect["w"] * K / 2) * 2); oh = int(round(rect["h"] * K / 2) * 2)
ddur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", DEMO], capture_output=True, text=True).stdout)
w0, w1 = windows[rect["slide"]]; t0 = w0 + 0.35; span = max(4.0, (w1 - 0.5) - t0)
factor = min(1.0, span / ddur)  # 시연 녹화는 실제 속도보다 느리게 하지 않는다. 남는 시간은 마지막 화면을 유지
print("demo slide %d window %.1f-%.1f, overlay %.1f-%.1f, speed factor %.3f, rect %d,%d %dx%d" % (rect["slide"], w0, w1, t0, t0 + span, factor, ox, oy, ow, oh))
fc = (f"[2:v]setpts={factor:.5f}*(PTS-STARTPTS),scale={ow}:{oh}:flags=lanczos,fps=30,setpts=PTS+{t0:.3f}/TB[d];"
      f"[0:v]fps=30,format=yuv420p[b];[b][d]overlay={ox}:{oy}:eof_action=repeat:enable='between(t,{t0:.3f},{t0 + span:.3f})',format=yuv420p[v]")
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{WORK}/frames.txt", "-i", f"{WORK}/narration.wav", "-i", DEMO,
       "-filter_complex", fc, "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-tune", "film", "-crf", "20",
       "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", OUT]
subprocess.run(cmd, check=True); print("wrote", OUT, "(work dir", WORK + ")")
