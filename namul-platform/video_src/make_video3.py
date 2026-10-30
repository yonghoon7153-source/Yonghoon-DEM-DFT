"""슬라이드 이미지 + AI 내레이션(오프라인 한국어 TTS) + 하단 자막 → 1080p MP4."""
import json, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from ko_norm import normalize
from tts_lib import synth, save_wav

S = "/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/a9086aab-2880-555b-a3e5-137ced4672cf/scratchpad"
V = f"{S}/video3"; FR = f"{V}/frames"; os.makedirs(FR, exist_ok=True)
OUT = sys.argv[1]; SPEED = float(sys.argv[2]) if len(sys.argv) > 2 else 0.92
W, H = 1920, 1080; SW, SH = 1664, 936; SX, SY = (W - SW) // 2, 14
BG = (20, 24, 22); FONT = ImageFont.truetype(f"{S}/fonts/NanumGothic-Bold.ttf", 38)
LEAD, CHUNK_GAP, SENT_GAP, TAIL = 0.45, 0.2, 0.42, 0.7
data = json.load(open(f"{os.path.dirname(__file__)}/script.json", encoding="utf-8"))

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
def silence(sec): return np.zeros(int(round(sec * sr)), dtype=np.float32)
for o in data:
    img = Image.open(f"{V}/slides/s-{o['n']:02d}.png").convert("RGB").resize((SW, SH), Image.LANCZOS)
    if not o["sentences"]:
        if sr is None: sr = 22050
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
wav = np.concatenate(audio); save_wav(f"{V}/narration.wav", wav, sr)
total = len(wav) / sr
with open(f"{V}/frames.txt", "w") as f:
    for p, d in segs: f.write(f"file '{p}'\nduration {d:.4f}\n")
    f.write(f"file '{segs[-1][0]}'\n")
print("segments", len(segs), "audio %.1fs (%d:%02d)" % (total, total // 60, total % 60))
json.dump(windows, open(f"{V}/windows.json", "w"))
rect = json.load(open(f"{os.path.dirname(__file__)}/demo_rect.json"))
K = SW / 10.0
ox, oy = round(SX + rect["x"] * K), round(SY + rect["y"] * K)
ow = int(round(rect["w"] * K / 2) * 2); oh = int(round(rect["h"] * K / 2) * 2)
DEMO = f"{S}/proto/rec/demo_phone.mp4"
ddur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", DEMO], capture_output=True, text=True).stdout)
w0, w1 = windows[14]; t0 = w0 + 0.35; span = max(4.0, (w1 - 0.5) - t0); factor = span / ddur
print("demo window %.1f-%.1f, overlay %.1f-%.1f, speed factor %.3f, rect %d,%d %dx%d" % (w0, w1, t0, t0 + span, factor, ox, oy, ow, oh))
fc = (f"[2:v]setpts={factor:.5f}*(PTS-STARTPTS),scale={ow}:{oh}:flags=lanczos,fps=30,setpts=PTS+{t0:.3f}/TB[d];"
      f"[0:v]fps=30,format=yuv420p[b];[b][d]overlay={ox}:{oy}:eof_action=pass:enable='between(t,{t0:.3f},{t0 + span:.3f})',format=yuv420p[v]")
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{V}/frames.txt", "-i", f"{V}/narration.wav", "-i", DEMO,
       "-filter_complex", fc, "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-tune", "film", "-crf", "20",
       "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", OUT]
subprocess.run(cmd, check=True); print("wrote", OUT)
