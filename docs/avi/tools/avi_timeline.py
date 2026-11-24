#!/usr/bin/env python3
"""Timeline: lines -> speech spans -> caption spans -> shot spans -> anchors.

Two timing sources:
  * text model  : speech = syllables / (base_rate * speed) + comma pauses
                  (base rate fitted to the reference: articulation 8.37 syl/s;
                   our default 7.2 syl/s = ~14 % slower, see reference_analysis.md)
  * audio model : line spans measured from the processed narration
                  (avi_audio.py prep writes <episode>/audio/timing.json)
"""
import json
import os
import re

from korean_text import syllables, spoken

DEFAULTS = dict(base_rate=7.2, comma_pause=0.16, lead_in=0.6, caption_lead=0.2,
                caption_min=0.45, hide_gap=1.0, hide_after=0.35, tail=0.0)


def load(path):
    with open(path, encoding="utf-8") as f:
        ep = json.load(f)
    # 그림 개체의 상대 경로 (예 "assets/powder_obj.png") = scenes.json 이 있는 편 폴더 기준 — 메모리에서만 푼다 (파일은 상대 경로 그대로)
    base = os.path.dirname(os.path.abspath(path))
    for sc in ep.get("scenes", []):
        for sh in sc.get("shots", []):
            for e in sh.get("elements", []):
                if e.get("type") == "image" and isinstance(e.get("path"), str) and not os.path.isabs(e["path"]):
                    e["path"] = os.path.join(base, e["path"])
    return ep


def all_lines(ep):
    out = []
    for sc in ep["scenes"]:
        for i, ln in enumerate(sc["lines"]):
            d = dict(ln)
            d["scene"] = sc["id"]
            d["scene_index"] = i
            d["say"] = ln.get("say") or spoken(ln["text"])
            d["is_last_in_scene"] = (i == len(sc["lines"]) - 1)
            out.append(d)
    return out


def split_captions(text, max_chars=22):
    """Fallback splitter: break at commas / spaces near the middle."""
    t = text.strip()
    if len(t) <= max_chars:
        return [t]
    parts = [p.strip() for p in re.split(r"(?<=,)\s+", t) if p.strip()]
    out = []
    for p in parts:
        while len(p) > max_chars:
            cut = p.rfind(" ", 0, max_chars)
            if cut <= 0:
                cut = max_chars
            out.append(p[:cut].strip())
            p = p[cut:].strip()
        if p:
            out.append(p)
    return out


def _chunk_weights(chunks):
    return [max(1, syllables(c)) for c in chunks]


def speech_duration(line, cfg):
    syl = syllables(line["say"])
    commas = line["say"].count(",")
    return syl / (cfg["base_rate"] * float(line.get("speed", 1.0))) + commas * cfg["comma_pause"]


def build(ep, audio_timing=None, cfg_over=None):
    """Return a timeline dict (lines, captions, shots, duration)."""
    cfg = dict(DEFAULTS)
    cfg.update(ep.get("voice_model", {}))
    if cfg_over:
        cfg.update(cfg_over)
    lines = all_lines(ep)
    t = cfg["lead_in"]
    timing = None
    if audio_timing:
        with open(audio_timing, encoding="utf-8") as f:
            timing = json.load(f)
        tmap = {d["id"]: d for d in timing["lines"]}
    for ln in lines:
        if timing:
            d = tmap[ln["id"]]
            ln["t0"], ln["t1"] = d["t0"], d["t1"]
            ln["pause"] = d.get("pause_after", ln.get("pause_after", 0.4))
        else:
            dur = speech_duration(ln, cfg)
            ln["t0"] = t
            ln["t1"] = t + dur
            ln["pause"] = float(ln.get("pause_after", 0.4))
            t = ln["t1"] + ln["pause"]
    # captions
    caps = []
    for ln in lines:
        chunks = ln.get("captions") or split_captions(ln["text"], ep.get("caption_max_chars", 22))
        w = _chunk_weights(chunks)
        tot = sum(w)
        span = ln["t1"] - ln["t0"]
        acc = 0.0
        for k, (c, wi) in enumerate(zip(chunks, w)):
            s0 = ln["t0"] + span * acc / tot
            acc += wi
            s1 = ln["t0"] + span * acc / tot
            caps.append(dict(line=ln["id"], k=k, text=c, s0=s0, s1=s1, last_in_line=(k == len(chunks) - 1),
                             hide_after=(ln["is_last_in_scene"] and ln["pause"] >= cfg["hide_gap"])
                             or (k == len(chunks) - 1 and ln.get("hide_caption_after", False))))
    lead = cfg["caption_lead"]
    for i, c in enumerate(caps):
        on = c["s0"] - lead
        if i > 0:
            prev = caps[i - 1]
            on = max(on, prev["s1"] + 0.08 if prev["last_in_line"] else prev["s0"] + cfg["caption_min"])
        c["on"] = max(0.0, on)
    for i, c in enumerate(caps):
        nxt = caps[i + 1]["on"] if i + 1 < len(caps) else c["s1"] + 0.6
        if c["hide_after"]:
            c["off"] = min(nxt, c["s1"] + cfg["hide_after"])
        else:
            c["off"] = nxt
    # shots
    lid = {ln["id"]: ln for ln in lines}
    shots = []
    for sc in ep["scenes"]:
        for sh in sc.get("shots", []):
            first = lid[sh["from"]]
            s = dict(sh)
            s["scene"] = sc["id"]
            s["t_start"] = max(0.0, first["t0"] - float(sh.get("pre", 0.35)))
            shots.append(s)
    end_extra = float(ep.get("end_card_s", 0.0))
    total = lines[-1]["t1"] + lines[-1]["pause"] + end_extra + cfg["tail"]
    for i, s in enumerate(shots):
        s["t_end"] = shots[i + 1]["t_start"] if i + 1 < len(shots) else total
    return dict(cfg=cfg, lines=lines, captions=caps, shots=shots, duration=total, lid=lid)


_off_re = re.compile(r"^(?P<base>.*?)(?P<off>[+-]\d+(?:\.\d+)?)?$")


def resolve(anchor, tl, shot=None):
    """Anchor = BASE [OFFSET]
       BASE:  'LINE' (speech start) | 'LINE@0.4' (40 % into the line) |
              'LINE~낱말' (estimated time the word is spoken) | 'LINE$' (speech end) |
              'shot' (current shot start)
       OFFSET: '+0.8' or '-0.3' seconds
       A bare number = absolute seconds.
    """
    if anchor is None:
        return None
    if isinstance(anchor, (int, float)):
        return float(anchor)
    a = anchor.strip()
    m = _off_re.match(a)
    base, off = m.group("base"), float(m.group("off") or 0.0)
    if base == "shot":
        return (shot["t_start"] if shot else 0.0) + off
    if base.endswith("$"):
        return tl["lid"][base[:-1]]["t1"] + off
    if "@" in base:
        lid, frac = base.split("@", 1)
        ln = tl["lid"][lid]
        return ln["t0"] + float(frac) * (ln["t1"] - ln["t0"]) + off
    if "~" in base:
        lid, word = base.split("~", 1)
        ln = tl["lid"][lid]
        say = ln["say"]
        w = spoken(word)
        pos = say.find(w)
        if pos < 0:
            pos = say.find(word)
        if pos < 0:
            raise ValueError(f"word {word!r} not in line {lid}: {say}")
        before = syllables(say[:pos]) + 0.15 * say[:pos].count(",") * 0  # syllable position
        tot = max(1, syllables(say))
        return ln["t0"] + (ln["t1"] - ln["t0"]) * before / tot + off
    if base in tl["lid"]:
        return tl["lid"][base]["t0"] + off
    raise ValueError(f"bad anchor {anchor!r}")


def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(tl, path):
    with open(path, "w", encoding="utf-8") as f:
        for i, c in enumerate(tl["captions"], 1):
            f.write(f"{i}\n{srt_time(c['on'])} --> {srt_time(c['off'])}\n{c['text']}\n\n")
    return path


def summary(tl):
    import numpy as np
    caps = tl["captions"]
    d = [c["off"] - c["on"] for c in caps]
    ch = [len(c["text"]) for c in caps]
    syl = sum(syllables(ln["say"]) for ln in tl["lines"])
    sp = sum(ln["t1"] - ln["t0"] for ln in tl["lines"])
    pauses = [ln["pause"] for ln in tl["lines"]]
    return dict(duration_s=round(tl["duration"], 2), lines=len(tl["lines"]), captions=len(caps),
                syllables=syl, speech_s=round(sp, 1), articulation_rate=round(syl / sp, 2),
                caption_dur_median=round(float(np.median(d)), 2), caption_chars_median=float(np.median(ch)),
                caption_chars_max=int(max(ch)), pause_median=round(float(np.median(pauses)), 2),
                pause_cv=round(float(np.std(pauses) / np.mean(pauses)), 2))
