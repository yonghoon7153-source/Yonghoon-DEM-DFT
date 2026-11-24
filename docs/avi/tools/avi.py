#!/usr/bin/env python3
"""AVI pipeline CLI.

  python3 -I avi.py plan    EP_DIR [--timing EP_DIR/audio/timing.json]
  python3 -I avi.py stills  EP_DIR [--every 3 | --times 1,2.5] [--width 960]
  python3 -I avi.py render  EP_DIR [--out preview_silent.mp4] [--audio mix.wav --timing timing.json]
  python3 -I avi.py tts     EP_DIR        (Typecast TSV, ElevenLabs text, plain text, SSML)
  python3 -I avi.py audio-prep EP_DIR [--in EP_DIR/audio_in] [--bgm music.wav]
  python3 -I avi.py audio-qc   EP_DIR
  python3 -I avi.py thumb   EP_DIR
  python3 -I avi.py typecast EP_DIR [--run --lines s01_l01,… | --run --all] [--tempo 1.0] [--mode smart|preset] [--force]
                              (Typecast 문정 · one wav per sentence into EP_DIR/audio_in · default = dry run)
  python3 -I avi.py voice-auto EP_DIR [--run] [--rounds 2 --takes 2 --budget-x 3] [--bgm music.wav]
                              (voice stage on its own: typecast smart 1.0 for out-of-date lines -> audio-prep -> audio-qc ->
                               retake jumps up to --rounds -> EP_DIR/audio/voice_auto_report.md · default = preview, 0 calls)
  python3 -I avi.py selftest
EP_DIR must contain scenes.json.  Run with `python3 -I` from anywhere.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")      # keep numpy single-threaded (shared machine)

import argparse  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import avi_style as S  # noqa: E402
import avi_timeline as T  # noqa: E402


def _ep(ep_dir):
    path = os.path.join(ep_dir, "scenes.json")
    return T.load(path), path


def _timing(ep_dir, arg):
    if arg:
        return arg
    p = os.path.join(ep_dir, "audio", "timing.json")
    return None if not os.path.exists(p) else None  # explicit only


def cmd_plan(a):
    ep, _ = _ep(a.ep)
    tl = T.build(ep, a.timing)
    s = T.summary(tl)
    print(json.dumps(s, ensure_ascii=False, indent=1))
    name = ep["episode"].split("_")[0]
    srt = os.path.join(a.ep, f"{name}.srt")
    T.write_srt(tl, srt)
    out = dict(summary=s, lines=[{k: v for k, v in ln.items() if k in ("id", "scene", "text", "say", "t0", "t1", "pause")}
                                 for ln in tl["lines"]],
               captions=[{k: round(v, 3) if isinstance(v, float) else v for k, v in c.items()
                          if k in ("line", "k", "text", "on", "off")} for c in tl["captions"]],
               shots=[dict(id=sh["id"], scene=sh["scene"], t_start=round(sh["t_start"], 3), t_end=round(sh["t_end"], 3))
                      for sh in tl["shots"]])
    with open(os.path.join(a.ep, "timeline.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("wrote", srt, "and timeline.json")


def cmd_stills(a):
    import avi_render as R
    ep, _ = _ep(a.ep)
    tl = T.build(ep, a.timing)
    rend = R.Renderer(ep, tl)
    if a.times:
        times = [float(x) for x in a.times.split(",")]
    elif a.shots:
        times = []
        for sh in tl["shots"]:
            times.append(min(sh["t_end"] - 0.1, sh["t_start"] + 0.82 * (sh["t_end"] - sh["t_start"])))
    else:
        times = [i * a.every for i in range(int(tl["duration"] / a.every) + 1)]
    out_dir = os.path.join(a.ep, "qa", a.tag)
    paths = R.stills(rend, times, out_dir, width=a.width)
    sheets = []
    per = 12
    for k in range(0, len(paths), per):
        sp = os.path.join(out_dir, f"sheet_{k // per + 1:02d}.jpg")
        R.contact_sheet(paths[k:k + per], sp, cols=3)
        sheets.append(sp)
    print("\n".join(sheets))


def cmd_render(a):
    import avi_render as R
    ep, _ = _ep(a.ep)
    tl = T.build(ep, a.timing)
    rend = R.Renderer(ep, tl)
    out = a.out if os.path.isabs(a.out) else os.path.join(a.ep, a.out)
    info = rend.render(out, audio=a.audio, threads=a.threads, t0=a.t0, t1=a.t1)
    name = ep["episode"].split("_")[0]
    T.write_srt(tl, os.path.join(a.ep, f"{name}.srt"))
    print(json.dumps(dict(out=out, duration=round(tl["duration"], 2), **info)))


def cmd_tts(a):
    import avi_tts
    ep, _ = _ep(a.ep)
    tl = T.build(ep)
    for p in avi_tts.export_all(ep, tl, a.ep):
        print("wrote", p)


def cmd_audio_prep(a):
    import avi_audio
    ep, _ = _ep(a.ep)
    res = avi_audio.prep(ep, a.ep, in_dir=a.inp, bgm=a.bgm, bgm_lufs=a.bgm_lufs, keep_pauses=a.keep_pauses,
                         target_lufs=a.lufs, threads=a.threads)
    print(json.dumps(res, ensure_ascii=False, indent=1))


def cmd_audio_qc(a):
    import avi_audio
    ep, _ = _ep(a.ep)
    lines = None
    if a.text:
        lines = [l.strip() for l in open(a.text, encoding="utf-8") if l.strip() and not l.startswith("#")]
    print(avi_audio.qc(ep, a.ep, wav=a.wav, text_lines=lines))


def cmd_thumb(a):
    import avi_thumb
    ep, _ = _ep(a.ep)
    print(avi_thumb.make(ep, a.ep, a.out))
    # end-card object (transparent PNG) — any image element whose file lives in <ep>/assets/powder_obj.png
    obj = os.path.join(a.ep, "assets", "powder_obj.png")
    if a.obj or not os.path.exists(obj):
        os.makedirs(os.path.dirname(obj), exist_ok=True)
        print(avi_thumb.object_png(obj))


def cmd_typecast(a):
    import avi_typecast
    argv = [a.ep] + (["--run"] if a.run else []) + (["--lines", a.lines] if a.lines else []) + \
        (["--all"] if a.all else []) + (["--force"] if a.force else []) + ["--tempo", str(a.tempo), "--mode", a.mode] + \
        (["--retake", a.retake] if a.retake else []) + (["--retake-jumps"] if a.retake_jumps else []) + ["--takes", str(a.takes)]
    avi_typecast.main(argv)


def cmd_voice_auto(a):
    import avi_voice_auto
    argv = [a.ep] + (["--run"] if a.run else []) + ["--rounds", str(a.rounds), "--takes", str(a.takes),
                                                     "--budget-x", str(a.budget_x)] + \
        (["--bgm", a.bgm, "--bgm-lufs", str(a.bgm_lufs)] if a.bgm else [])
    sys.exit(avi_voice_auto.main(argv))


def cmd_selftest(a):
    import avi_audio
    import avi_typecast
    import avi_voice_auto
    ok1 = avi_audio.selftest(os.path.join(os.path.dirname(HERE), "selftest"))
    ok2 = avi_typecast.selftest()
    ok3 = avi_voice_auto.selftest()
    sys.exit(0 if (ok1 and ok2 and ok3) else 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan"); p.add_argument("ep"); p.add_argument("--timing"); p.set_defaults(f=cmd_plan)
    p = sub.add_parser("stills"); p.add_argument("ep"); p.add_argument("--timing"); p.add_argument("--every", type=float, default=3.0)
    p.add_argument("--times"); p.add_argument("--shots", action="store_true"); p.add_argument("--width", type=int, default=960)
    p.add_argument("--tag", default="stills"); p.set_defaults(f=cmd_stills)
    p = sub.add_parser("render"); p.add_argument("ep"); p.add_argument("--out", default="preview_silent.mp4")
    p.add_argument("--audio"); p.add_argument("--timing"); p.add_argument("--threads", type=int, default=1)
    p.add_argument("--t0", type=float, default=0.0); p.add_argument("--t1", type=float, default=None); p.set_defaults(f=cmd_render)
    p = sub.add_parser("tts"); p.add_argument("ep"); p.set_defaults(f=cmd_tts)
    p = sub.add_parser("audio-prep"); p.add_argument("ep"); p.add_argument("--in", dest="inp")
    p.add_argument("--bgm"); p.add_argument("--bgm-lufs", type=float, default=-28.0); p.add_argument("--lufs", type=float, default=-14.0)
    p.add_argument("--keep-pauses", action="store_true"); p.add_argument("--threads", type=int, default=1); p.set_defaults(f=cmd_audio_prep)
    p = sub.add_parser("audio-qc"); p.add_argument("ep"); p.add_argument("--wav")
    p.add_argument("--text", help="one sentence per line (default for audition_*.wav: voice_audition.txt)")
    p.set_defaults(f=cmd_audio_qc)
    p = sub.add_parser("thumb"); p.add_argument("ep"); p.add_argument("--out", default="thumbnail.png"); p.add_argument("--obj", action="store_true", help="also re-render assets/powder_obj.png (end card)"); p.set_defaults(f=cmd_thumb)
    p = sub.add_parser("typecast"); p.add_argument("ep"); p.add_argument("--run", action="store_true")
    p.add_argument("--lines"); p.add_argument("--all", action="store_true"); p.add_argument("--force", action="store_true")
    p.add_argument("--tempo", type=float, default=1.0); p.add_argument("--mode", choices=("smart", "preset"), default="smart")
    p.add_argument("--retake"); p.add_argument("--retake-jumps", action="store_true"); p.add_argument("--takes", type=int, default=2)
    p.set_defaults(f=cmd_typecast)
    p = sub.add_parser("voice-auto", help="voice stage on its own (default = preview · 0 calls)"); p.add_argument("ep")
    p.add_argument("--run", action="store_true"); p.add_argument("--rounds", type=int, default=2)
    p.add_argument("--takes", type=int, default=2); p.add_argument("--budget-x", type=float, default=3.0)
    p.add_argument("--bgm"); p.add_argument("--bgm-lufs", type=float, default=-28.0); p.set_defaults(f=cmd_voice_auto)
    p = sub.add_parser("selftest"); p.set_defaults(f=cmd_selftest)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
