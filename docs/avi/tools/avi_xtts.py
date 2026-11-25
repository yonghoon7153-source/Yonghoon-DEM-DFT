#!/usr/bin/env python3
"""Local TTS with coqui-tts XTTS-v2 (built-in speakers only · no voice cloning · CPML = internal use only).

내부판 전용 (AVI 스킬 S6 · 1저자 11-25) — XTTS-v2 = CPML (비상업) 이라 공개판 음성에 쓰지 않는다 · 내부판 기본 로컬 TTS 는
MeloTTS-Korean (`avi_melo.py`) 이고 이 도구는 예비다 (한국어가 외국인 억양으로 들린다 · 1저자 11-25 내부 1 분판).
모델 파일 · venv 는 리포 밖 (작업 폴더) — 모델 자리 = 환경 변수 AVI_XTTS_MODEL_DIR · 없으면 이 tools/ 폴더 옆의 tts_models/xtts_v2.
torch · TTS 는 함수 안에서만 부른다 (모듈 첫머리 = numpy 만 · 리포 게이트는 torch 없이 돈다).

Run with the TTS venv (NOT system python · the venv lives outside the repo, e.g. the work folder's venv_tts):
  <TTS venv>/bin/python -I avi_xtts.py speakers
  <TTS venv>/bin/python -I avi_xtts.py audition --out DIR --text "…" [--speakers all|A,B] [--seed 7]
  <TTS venv>/bin/python -I avi_xtts.py sample --out FILE.wav --speaker NAME --text "…" --text "…" [--pause 0.45]

Rules (1저자 · 본 세션 11-25): text never leaves this machine (no outside TTS · no outside transcription) · built-in speaker
latents from speakers_xtts.pth only (never a reference recording) · CPU threads <= 2 (a gate runs beside it) · fixed seed per call.
Model files = MODEL_DIR (model.pth · config.json · vocab.json · speakers_xtts.pth · sha256 in DECISIONS).
Metrics per clip (proxies, not a listening test): speech span · syllable rate · long internal gaps · F0 median / IQR (semitones) ·
ending creak proxy (last 0.35 s: F0 < 110 Hz or aperiodic) · ending roughness (last 0.25 s: mean |Δ level| of 10 ms frames) ·
K-weighted gated loudness · peak.
"""
import argparse
import json
import os
import sys
import time

THREADS = 2
os.environ.setdefault("OMP_NUM_THREADS", str(THREADS))
os.environ.setdefault("MKL_NUM_THREADS", str(THREADS))
os.environ.setdefault("OPENBLAS_NUM_THREADS", str(THREADS))
os.environ.setdefault("HF_HUB_OFFLINE", "1")           # never fetch anything at run time
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import audio_measure as M  # noqa: E402
from korean_text import syllables  # noqa: E402

MODEL_DIR = os.environ.get("AVI_XTTS_MODEL_DIR") or os.path.join(os.path.dirname(HERE), "tts_models", "xtts_v2")
SR_OUT = 24000


def load_model():
    import torch
    torch.set_num_threads(THREADS)
    torch.set_num_interop_threads(1)
    from TTS.tts.configs.xtts_config import XttsConfig
    from TTS.tts.models.xtts import Xtts
    cfg = XttsConfig()
    cfg.load_json(os.path.join(MODEL_DIR, "config.json"))
    model = Xtts.init_from_config(cfg)
    model.load_checkpoint(cfg, checkpoint_dir=MODEL_DIR, eval=True, use_deepspeed=False,
                          speaker_file_path=os.path.join(MODEL_DIR, "speakers_xtts.pth"))
    model.eval()
    return model


def speaker_names(model):
    return sorted(model.speaker_manager.speakers.keys())


def synth(model, text, speaker, seed=7, temperature=0.65, speed=1.0):
    import torch
    sp = model.speaker_manager.speakers[speaker]
    torch.manual_seed(seed)
    with torch.inference_mode():
        out = model.inference(text, "ko", sp["gpt_cond_latent"], sp["speaker_embedding"], temperature=temperature,
                              speed=speed, enable_text_splitting=False)
    w = out["wav"]
    w = w.detach().cpu().numpy() if hasattr(w, "detach") else np.asarray(w)
    return np.asarray(w, np.float32).reshape(-1)


def kweight(sig, sr):
    from scipy.signal import lfilter
    # BS.1770 pre-filter + RLB, designed for the given sample rate (analog prototypes via bilinear transform)
    f0, G, Q = 1681.974450955533, 3.999843853973347, 0.7071752369554196
    K = np.tan(np.pi * f0 / sr)
    Vh = 10 ** (G / 20)
    Vb = Vh ** 0.4996667741545416
    a0 = 1 + K / Q + K * K
    b = [(Vh + Vb * K / Q + K * K) / a0, 2 * (K * K - Vh) / a0, (Vh - Vb * K / Q + K * K) / a0]
    a = [1, 2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0]
    y = lfilter(b, a, sig)
    f1, Q1 = 38.13547087602444, 0.5003270373238773
    K = np.tan(np.pi * f1 / sr)
    a0 = 1 + K / Q1 + K * K
    b2 = [1, -2, 1]
    a2 = [1, 2 * (K * K - 1) / a0, (1 - K / Q1 + K * K) / a0]
    return lfilter(b2, a2, y)


def lufs(x, sr):
    y = kweight(x, sr)
    blk, hop = int(0.4 * sr), int(0.1 * sr)
    if len(y) < blk:
        return None
    ms = np.array([np.mean(y[i:i + blk] ** 2) for i in range(0, len(y) - blk + 1, hop)])
    lv = -0.691 + 10 * np.log10(ms + 1e-20)
    g = ms[lv > -70]
    if not len(g):
        return None
    rel = -0.691 + 10 * np.log10(np.mean(g)) - 10
    g2 = ms[(lv > -70) & (lv > rel)]
    return round(float(-0.691 + 10 * np.log10(np.mean(g2))), 2)


def metrics(x, sr, text):
    hop = int(0.01 * sr)
    fr = np.array([np.sqrt(np.mean(x[i:i + hop] ** 2) + 1e-14) for i in range(0, max(1, len(x) - hop), hop)])
    db = 20 * np.log10(fr + 1e-12)
    loud = db[db > -60]
    med = float(np.median(loud)) if len(loud) else -60.0
    sp = np.where(db > med - 25)[0]
    if not len(sp):
        return dict(ok=False, why="no speech")
    # isolated blips (11-25 · seen at the end of two sweep clips: ~0.5 s of near-silence, then a 20–40 ms burst = an XTTS
    # end artifact): a run of speech frames ≤ 0.15 s separated from the rest by a gap ≥ 0.25 s, at either end of the clip.
    # It is reported (end_blip_s / start_blip_s) and the speech span is measured without it.
    runs, st = [], sp[0]
    for a_, b_ in zip(sp[:-1], sp[1:]):
        if b_ - a_ > 1:
            runs.append((st, a_))
            st = b_
    runs.append((st, sp[-1]))
    end_blip = start_blip = 0.0
    while len(runs) > 1 and (runs[-1][1] - runs[-1][0] + 1) <= 15 and (runs[-1][0] - runs[-2][1]) >= 25:
        end_blip += (runs[-1][1] - runs[-1][0] + 1) * 0.01
        runs.pop()
    while len(runs) > 1 and (runs[0][1] - runs[0][0] + 1) <= 15 and (runs[1][0] - runs[0][1]) >= 25:
        start_blip += (runs[0][1] - runs[0][0] + 1) * 0.01
        runs.pop(0)
    sp = sp[(sp >= runs[0][0]) & (sp <= runs[-1][1])]
    t0, t1 = sp[0] * 0.01, (sp[-1] + 1) * 0.01
    seg = db[sp[0]:sp[-1] + 1]
    low = seg < med - 30
    gaps, k = [], 0
    while k < len(low):
        if low[k]:
            j = k
            while j < len(low) and low[j]:
                j += 1
            gaps.append((j - k) * 0.01)
            k = j
        else:
            k += 1
    syl = syllables(text)
    speech_s = t1 - t0
    tt, f0, ap = M.yin_f0(x[int(t0 * sr):int(t1 * sr)], sr, fmin=60, fmax=500)
    v = f0[np.isfinite(f0) & (ap < 0.35)]
    f0_med = float(np.median(v)) if len(v) else None
    iqr_st = float(12 * np.log2(np.percentile(v, 75) / np.percentile(v, 25))) if len(v) > 10 else None
    tail = x[int(max(0, t1 - 0.35) * sr):int(t1 * sr)]
    ttt, tf0, tap = M.yin_f0(tail, sr, fmin=60, fmax=500)
    lv = np.array([20 * np.log10(np.sqrt(np.mean(tail[max(0, int((t - 0.01) * sr)):int((t + 0.01) * sr)] ** 2)) + 1e-12)
                   for t in ttt])
    lmask = lv > med - 30
    # creak floor: 110 Hz was set for a high voice (Typecast 문정 · F0 ≈ 225 Hz); a low voice sits near 110 Hz by nature,
    # so the floor is min(110, 0.6 × this clip's median F0) (11-25 · fixed after the first sweep row, before ranking)
    floor = min(110.0, 0.6 * f0_med) if f0_med else 110.0
    creak = int(np.sum(lmask & (~np.isfinite(tf0) | (tf0 < floor) | (tap > 0.35))))
    w = db[max(0, sp[-1] - 25):sp[-1] + 1]
    w = w[w > med - 25]
    rough = float(np.mean(np.abs(np.diff(w)))) if len(w) > 3 else None
    return dict(ok=True, dur_s=round(len(x) / sr, 2), speech_t0=round(t0, 2), speech_t1=round(t1, 2),
                end_blip_s=round(end_blip, 2), start_blip_s=round(start_blip, 2),
                trail_s=round(len(x) / sr - t1, 2), speech_s=round(speech_s, 2), syllables=syl,
                syl_rate=round(syl / speech_s, 2) if speech_s > 0 else None, gaps_over_0p6=sum(g > 0.6 for g in gaps),
                gap_max=round(max(gaps), 2) if gaps else 0.0, f0_med=round(f0_med, 1) if f0_med else None,
                f0_iqr_st=round(iqr_st, 2) if iqr_st is not None else None, creak=f"{creak}/{int(np.sum(lmask))}",
                creak_n=creak, creak_floor_hz=round(floor, 1), rough_db=round(rough, 2) if rough is not None else None, lufs=lufs(x, sr),
                peak_db=round(float(20 * np.log10(np.max(np.abs(x)) + 1e-12)), 2))


def write_wav(path, x, sr=SR_OUT):
    import soundfile as sf
    sf.write(path, np.clip(x, -1, 1), sr, subtype="PCM_16")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("speakers")
    a1 = sub.add_parser("audition")
    a1.add_argument("--out", required=True)
    a1.add_argument("--text", action="append", required=True)
    a1.add_argument("--speakers", default="all")
    a1.add_argument("--seed", type=int, default=7)
    a1.add_argument("--temperature", type=float, default=0.65)
    a1.add_argument("--speed", type=float, default=1.0)
    a1.add_argument("--speed-map", default="", help="speaker=speed,… (overrides --speed for those speakers)")
    a2 = sub.add_parser("sample")
    a2.add_argument("--out", required=True)
    a2.add_argument("--speaker", required=True)
    a2.add_argument("--text", action="append", required=True)
    a2.add_argument("--pause", type=float, default=0.45)
    a2.add_argument("--seed", type=int, default=7)
    a2.add_argument("--temperature", type=float, default=0.65)
    a2.add_argument("--speed", type=float, default=1.0)
    a4 = sub.add_parser("lines", help="synthesize every line of an episode (scenes.json 'say') -> OUT/<episode>_<line>.wav + lines.json")
    a4.add_argument("ep_dir")
    a4.add_argument("--out", required=True)
    a4.add_argument("--speaker", required=True)
    a4.add_argument("--speed", type=float, default=1.3, help="base speed (× each line's own speed)")
    a4.add_argument("--seed", type=int, default=7, help="line k uses seed + k")
    a4.add_argument("--temperature", type=float, default=0.65)
    a4.add_argument("--only", default="", help="comma list of line ids (default: all)")
    a3 = sub.add_parser("measure")
    a3.add_argument("audition_json")
    a = ap.parse_args(argv)
    if a.cmd == "measure":
        import soundfile as sf
        res = json.load(open(a.audition_json, encoding="utf-8"))
        base = os.path.dirname(os.path.abspath(a.audition_json))
        rows = []
        for r in res["rows"]:
            x, sr = sf.read(os.path.join(base, r["file"]), dtype="float32")
            m = metrics(np.asarray(x, np.float32).reshape(-1), sr, res["texts"][r["text_no"] - 1])
            m.update({k: r[k] for k in ("speaker", "text_no", "file", "synth_s", "rtf", "speed") if k in r})
            rows.append(m)
        res["rows"] = rows
        res["remeasured"] = "metrics recomputed from the saved wavs (creak floor = min(110, 0.6 × F0 median))"
        out = os.path.splitext(a.audition_json)[0] + "_m.json"
        json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(out, len(rows))
        return 0
    t_load = time.time()
    model = load_model()
    t_load = time.time() - t_load
    names = speaker_names(model)
    if a.cmd == "speakers":
        print(json.dumps(dict(n=len(names), speakers=names, load_s=round(t_load, 1)), ensure_ascii=False))
        return 0
    if a.cmd == "audition":
        os.makedirs(a.out, exist_ok=True)
        pick = names if a.speakers == "all" else [s.strip() for s in a.speakers.split(",") if s.strip()]
        bad = [s for s in pick if s not in names]
        if bad:
            print("unknown speakers:", bad, file=sys.stderr)
            return 2
        smap = {}
        for kv in [x for x in a.speed_map.split(",") if x.strip()]:
            k_, v_ = kv.rsplit("=", 1)
            smap[k_.strip()] = float(v_)
        if not all(0.5 <= v <= 2.0 for v in list(smap.values()) + [a.speed]):
            print("speed out of 0.5–2.0", file=sys.stderr)
            return 2
        res = dict(model_dir=MODEL_DIR, threads=THREADS, seed=a.seed, temperature=a.temperature, texts=a.text,
                   speed=a.speed, speed_map=smap, load_s=round(t_load, 1), rows=[])
        for spk in pick:
            for k, txt in enumerate(a.text):
                t = time.time()
                x = synth(model, txt, spk, seed=a.seed, temperature=a.temperature, speed=smap.get(spk, a.speed))
                el = time.time() - t
                fn = f"{spk.replace(' ', '_')}_t{k + 1}.wav"
                write_wav(os.path.join(a.out, fn), x)
                m = metrics(x, SR_OUT, txt)
                m.update(speaker=spk, text_no=k + 1, file=fn, synth_s=round(el, 1), speed=smap.get(spk, a.speed),
                         rtf=round(el / max(0.01, len(x) / SR_OUT), 2))
                res["rows"].append(m)
                print(json.dumps(m, ensure_ascii=False), flush=True)
                json.dump(res, open(os.path.join(a.out, "audition.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return 0
    if a.cmd == "lines":
        import hashlib
        ep = json.load(open(os.path.join(a.ep_dir, "scenes.json"), encoding="utf-8"))
        if a.speaker not in names:
            print("unknown speaker", file=sys.stderr)
            return 2
        os.makedirs(a.out, exist_ok=True)
        only = {x.strip() for x in a.only.split(",") if x.strip()}
        ledger_p = os.path.join(a.out, "lines.json")
        led = json.load(open(ledger_p, encoding="utf-8")) if os.path.exists(ledger_p) else dict(lines={})
        led.update(speaker=a.speaker, base_speed=a.speed, temperature=a.temperature, model_dir=MODEL_DIR, threads=THREADS,
                   episode=ep.get("episode"))
        k = 0
        for sc in ep["scenes"]:
            for ln in sc["lines"]:
                k += 1
                if only and ln["id"] not in only:
                    continue
                sp = round(a.speed * float(ln.get("speed", 1.0) or 1.0), 4)
                # seed from the sentence text (11-25 v1): a take does not change when other sentences are added or cut
                seed = a.seed + int(hashlib.sha256(ln["say"].encode("utf-8")).hexdigest()[:6], 16) % 1000
                t = time.time()
                x = synth(model, ln["say"], a.speaker, seed=seed, temperature=a.temperature, speed=sp)
                fn = f"{ep.get('episode', 'ep').split('_')[0]}_{ln['id']}.wav"      # same name rule as avi_audio._find_line_inputs
                write_wav(os.path.join(a.out, fn), x)
                m = metrics(x, SR_OUT, ln["say"])
                led["lines"][ln["id"]] = dict(file=fn, say=ln["say"], say_sha256=hashlib.sha256(ln["say"].encode("utf-8")).hexdigest(),
                                              seed=seed, speed=sp, synth_s=round(time.time() - t, 1),
                                              wav_sha256=hashlib.sha256(open(os.path.join(a.out, fn), "rb").read()).hexdigest(), **m)
                json.dump(led, open(ledger_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                print(json.dumps(dict(id=ln["id"], speed=sp, speech_s=m.get("speech_s"), rate=m.get("syl_rate"),
                                      blip=(m.get("end_blip_s"), m.get("start_blip_s")), gap=m.get("gap_max")), ensure_ascii=False), flush=True)
        return 0
    if a.cmd == "sample":
        if a.speaker not in names:
            print("unknown speaker", file=sys.stderr)
            return 2
        parts, rows, pos = [], [], 0
        for k, txt in enumerate(a.text):
            x = synth(model, txt, a.speaker, seed=a.seed + k, temperature=a.temperature, speed=a.speed)
            rows.append(dict(text_no=k + 1, start_s=round(pos / SR_OUT, 3), end_s=round((pos + len(x)) / SR_OUT, 3),
                             **metrics(x, SR_OUT, txt)))
            parts.append(x)
            pos += len(x)
            if k < len(a.text) - 1:
                parts.append(np.zeros(int(a.pause * SR_OUT), np.float32))
                pos += int(a.pause * SR_OUT)
        y = np.concatenate(parts)
        write_wav(a.out, y)
        meta = dict(speaker=a.speaker, seed=a.seed, temperature=a.temperature, speed=a.speed, pause=a.pause, texts=a.text,
                    dur_s=round(len(y) / SR_OUT, 2), rows=rows, model_dir=MODEL_DIR, threads=THREADS)
        json.dump(meta, open(os.path.splitext(a.out)[0] + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(json.dumps(meta, ensure_ascii=False))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
