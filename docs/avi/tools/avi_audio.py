#!/usr/bin/env python3
"""Narration intake, re-timing, loudness and QC for AVI episodes.

prep():  EP_DIR/audio_in/<ep>_<line id>.wav (one file per sentence, e.g. ep01_s01_l01.wav from the TTS API)
         or <ep>_sNN.(wav|mp3|m4a|flac)  (one file per scene)  or  <ep>_full.*
         -> sentence alignment (pauses chosen by dynamic programming against the
            syllable-proportional expectation) -> each sentence's speech kept as is,
            pauses between sentences set to the TSV targets (or kept with --keep-pauses)
         -> BS.1770-4 loudness to -14 LUFS (measured on the stereo L=R signal),
            true peak <= -1.5 dBTP with a look-ahead limiter
         -> optional music bed at -28 LUFS (reference: voice ~13-14 LU above music, no ducking)
         -> EP_DIR/audio/narration.wav, mix.wav, timing.json
qc():    per sentence rate, pauses, F0 range and final movement, clipping, loudness;
         flags for 'mechanical' signatures measured on the reference video.
selftest(): synthetic voiced-syllable signals with known boundaries.
"""
import glob
import json
import math
import os
import re
import subprocess
import wave

import numpy as np
from scipy.signal import lfilter, resample_poly
from scipy.ndimage import minimum_filter1d

from korean_text import syllables

SR = 48000


# ------------------------------------------------------------------ io
def decode(path, sr=SR, threads=1):
    """Decode to 48 kHz and return the mid signal (mean of L and R).

    ffmpeg's own stereo->mono downmix sums correlated channels at 0.707 (+3 dB for L=R),
    so we decode two channels and average them here: a mono voice duplicated to L=R keeps
    its amplitude, and lufs(x, channels=2) then equals the loudness of the stereo file."""
    cmd = ["nice", "-n", "10", "ffmpeg", "-v", "error", "-threads", str(threads), "-i", path, "-ac", "2", "-ar", str(sr),
           "-f", "f32le", "-"]
    raw = subprocess.run(cmd, check=True, stdout=subprocess.PIPE).stdout
    st = np.frombuffer(raw, np.float32).astype(np.float64).reshape(-1, 2)
    return st.mean(axis=1)


def write_wav(path, x, sr=SR, stereo=True, seed=0):
    x = np.asarray(x, np.float64)
    if x.ndim == 1 and stereo:
        x = np.stack([x, x], axis=1)
    elif x.ndim == 1:
        x = x[:, None]
    rng = np.random.default_rng(seed)
    d = (rng.random(x.shape) - rng.random(x.shape)) / 32768.0       # TPDF dither
    y = np.clip(np.round((x + d) * 32767.0), -32768, 32767).astype("<i2")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with wave.open(path, "wb") as w:
        w.setnchannels(y.shape[1])
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(y.tobytes())
    return path


# ------------------------------------------------------------------ loudness (BS.1770-4 at 48 kHz)
_K1_B = [1.53512485958697, -2.69169618940638, 1.19839281085285]
_K1_A = [1.0, -1.69065929318241, 0.73248077421585]
_K2_B = [1.0, -2.0, 1.0]
_K2_A = [1.0, -1.99004745483398, 0.99007225036621]


def lufs(x, sr=SR, channels=2):
    """Integrated loudness of a mono signal reproduced on `channels` identical channels."""
    if sr != SR:
        raise ValueError("lufs() expects 48 kHz")
    z = lfilter(_K2_B, _K2_A, lfilter(_K1_B, _K1_A, x)) ** 2
    blk, hop = int(0.4 * sr), int(0.1 * sr)
    if len(z) < blk:
        return -120.0
    c = np.cumsum(np.concatenate([[0.0], z]))
    starts = np.arange(0, len(z) - blk + 1, hop)
    ms = (c[starts + blk] - c[starts]) / blk * channels
    lk = -0.691 + 10 * np.log10(ms + 1e-30)
    g1 = ms[lk > -70]
    if len(g1) == 0:
        return -120.0
    rel = -0.691 + 10 * np.log10(g1.mean()) - 10
    g2 = ms[(lk > -70) & (lk > rel)]
    return float(-0.691 + 10 * np.log10(g2.mean()))


def true_peak_db(x):
    os4 = resample_poly(x, 4, 1)
    return float(20 * np.log10(np.max(np.abs(os4)) + 1e-12))


def limiter(x, ceiling_db=-1.5, look_ms=5.0, release_ms=60.0, sr=SR):
    thr = 10 ** (ceiling_db / 20)
    os4 = np.abs(resample_poly(x, 4, 1))
    env = os4[:len(x) * 4].reshape(-1, 4).max(axis=1)
    if len(env) < len(x):
        env = np.pad(env, (0, len(x) - len(env)), mode="edge")
    req = np.minimum(1.0, thr / np.maximum(env, 1e-12))
    la = max(1, int(look_ms * 1e-3 * sr))
    g = minimum_filter1d(req, size=2 * la + 1)
    rel = math.exp(-1.0 / (release_ms * 1e-3 * sr))
    out = np.empty_like(g)
    cur = 1.0
    for i in range(len(g)):          # release smoothing (attack is instant via look-ahead window)
        cur = g[i] if g[i] < cur else g[i] + (cur - g[i]) * rel
        out[i] = cur
    return x * out


def normalize(x, target=-14.0, ceiling=-1.5):
    L = lufs(x)
    y = x * 10 ** ((target - L) / 20)
    if true_peak_db(y) > ceiling:
        y = limiter(y, ceiling_db=ceiling - 0.2)
        L2 = lufs(y)
        y = y * 10 ** ((target - L2) / 20)
        if true_peak_db(y) > ceiling:
            y = limiter(y, ceiling_db=ceiling - 0.3)
    return y, dict(lufs_in=round(L, 2), lufs_out=round(lufs(y), 2), true_peak_dbtp=round(true_peak_db(y), 2))


# ------------------------------------------------------------------ speech / pause detection
def frames_db(x, sr=SR, hop=0.01, win=0.03):
    h, w = int(sr * hop), int(sr * win)
    n = max(1, (len(x) - w) // h + 1)
    c = np.cumsum(np.concatenate([[0.0], x * x]))
    s = np.arange(n) * h
    e = (c[s + w] - c[s]) / w
    return 10 * np.log10(e + 1e-14), hop


def _quiet_threshold(lev):
    """Pause threshold relative to the speech level: at least 22 dB below it,
    and 10 dB above the floor when the file has real silence (TTS gaps)."""
    ref = np.percentile(lev, 90)
    floor = np.percentile(lev, 5)
    return min(ref - 22.0, max(floor + 10.0, ref - 35.0)), ref, floor


def silences(x, sr=SR, min_dur=0.10):
    lev, hop = frames_db(x, sr)
    thr, ref, floor = _quiet_threshold(lev)
    q = lev < thr
    d = np.diff(np.concatenate([[0], q.astype(int), [0]]))
    st, en = np.where(d == 1)[0], np.where(d == -1)[0]
    out = [((a + 1.5) * hop, (b + 1.5) * hop) for a, b in zip(st, en) if (b - a) * hop >= min_dur]
    return out, dict(thr=thr, ref=ref, floor=floor)


def speech_bounds(x, sr=SR):
    lev, hop = frames_db(x, sr)
    thr, ref, _ = _quiet_threshold(lev)
    idx = np.where(lev >= thr)[0]
    if len(idx) == 0:
        return 0.0, len(x) / sr
    return max(0.0, idx[0] * hop), min(len(x) / sr, (idx[-1] + 3) * hop + 0.03)


def align(x, line_syl, sr=SR):
    """Return per-line (start, end) speech spans in seconds for one file holding len(line_syl) sentences."""
    n = len(line_syl)
    s0, s1 = speech_bounds(x, sr)
    if n == 1:
        return [(s0, s1)], dict(n_candidates=0, cost=0.0)
    sil, info = silences(x, sr, min_dur=0.10)
    sil = [(a, b) for a, b in sil if a > s0 + 0.2 and b < s1 - 0.2]
    C = len(sil)
    durs = sorted((b - a for a, b in sil), reverse=True)
    tot_sp = max(0.2, (s1 - s0) - sum(durs[:n - 1]))     # speech time if the n-1 longest silences are sentence breaks
    w = np.asarray(line_syl, float)
    if C < n - 1:
        # not enough pauses: proportional split (low confidence)
        cum = np.cumsum(w) / w.sum()
        cuts = [s0 + (s1 - s0) * c for c in cum[:-1]]
        spans, prev = [], s0
        for ct in cuts:
            spans.append((prev, ct))
            prev = ct
        spans.append((prev, s1))
        return spans, dict(n_candidates=C, cost=float("inf"), fallback=True)
    # expected start of line k (cumulative syllable fraction of speaking time incl. pauses)
    def seg_cost(t_a, t_b, k):
        dur = max(0.05, t_b - t_a)
        exp_ = tot_sp * w[k] / w.sum()
        return math.log(dur / exp_) ** 2
    INFv = 1e18
    # dp[k][j] = best cost with line k ending at silence j (k = 0..n-2)
    dp = np.full((n - 1, C), INFv)
    bk = np.full((n - 1, C), -1, int)
    for j in range(C):
        dp[0, j] = seg_cost(s0, sil[j][0], 0) - 0.35 * math.log((sil[j][1] - sil[j][0]) / 0.1)
    for k in range(1, n - 1):
        for j in range(k, C):
            best, arg = INFv, -1
            for i in range(k - 1, j):
                if dp[k - 1, i] >= INFv:
                    continue
                c = dp[k - 1, i] + seg_cost(sil[i][1], sil[j][0], k)
                if c < best:
                    best, arg = c, i
            if arg >= 0:
                dp[k, j] = best - 0.35 * math.log((sil[j][1] - sil[j][0]) / 0.1)
                bk[k, j] = arg
    best, arg = INFv, -1
    for j in range(n - 2, C):
        if dp[n - 2, j] >= INFv:
            continue
        c = dp[n - 2, j] + seg_cost(sil[j][1], s1, n - 1)
        if c < best:
            best, arg = c, j
    chosen = [arg]
    for k in range(n - 2, 0, -1):
        chosen.append(bk[k, chosen[-1]])
    chosen = chosen[::-1]
    spans = []
    prev = s0
    for j in chosen:
        spans.append((prev, sil[j][0]))
        prev = sil[j][1]
    spans.append((prev, s1))
    return spans, dict(n_candidates=C, cost=round(float(best), 3), fallback=False)


# ------------------------------------------------------------------ prep
def _find_inputs(ep, in_dir):
    name = ep["episode"].split("_")[0]
    exts = (".wav", ".mp3", ".m4a", ".flac", ".aac", ".ogg")
    per = {}
    for sc in ep["scenes"]:
        for ext in exts:
            p = os.path.join(in_dir, f"{name}_{sc['id']}{ext}")
            if os.path.exists(p):
                per[sc["id"]] = p
                break
    full = None
    for ext in exts:
        p = os.path.join(in_dir, f"{name}_full{ext}")
        if os.path.exists(p):
            full = p
    return per, full


def _find_line_inputs(ep, in_dir):
    """One file per sentence (TTS API output): <ep>_<line id>.<ext>, e.g. ep01_s01_l01.wav."""
    name = ep["episode"].split("_")[0]
    exts = (".wav", ".mp3", ".m4a", ".flac", ".aac", ".ogg")
    got = {}
    for sc in ep["scenes"]:
        for ln in sc["lines"]:
            for ext in exts:
                p = os.path.join(in_dir, f"{name}_{ln['id']}{ext}")
                if os.path.exists(p):
                    got[ln["id"]] = p
                    break
    return got


def prep(ep, ep_dir, in_dir=None, bgm=None, bgm_lufs=-28.0, keep_pauses=False, target_lufs=-14.0, threads=1,
         fade_ms=8.0, pad_s=0.04):
    in_dir = in_dir or os.path.join(ep_dir, "audio_in")
    out_dir = os.path.join(ep_dir, "audio")
    os.makedirs(out_dir, exist_ok=True)
    per, full = _find_inputs(ep, in_dir)
    per_line = _find_line_inputs(ep, in_dir)
    all_lines = [ln for sc in ep["scenes"] for ln in sc["lines"]]
    groups = []                     # (file, [lines])
    if per_line and len(per_line) == len(all_lines):
        # one file per sentence: the sentence boundary is the file itself (no pause search needed)
        groups = [(per_line[ln["id"]], [ln]) for ln in all_lines]
    elif per_line and not per and not full:
        missing = [ln["id"] for ln in all_lines if ln["id"] not in per_line]
        raise SystemExit(f"sentence files incomplete: {len(missing)} of {len(all_lines)} missing "
                         f"(first: {missing[:6]}) in {in_dir}")
    elif full and not per:
        groups.append((full, [ln for sc in ep["scenes"] for ln in sc["lines"]]))
    else:
        missing = [sc["id"] for sc in ep["scenes"] if sc["id"] not in per]
        if missing:
            raise SystemExit(f"missing audio for scenes: {missing} (expected names like {ep['episode'].split('_')[0]}_s01.wav in {in_dir})")
        for sc in ep["scenes"]:
            groups.append((per[sc["id"]], sc["lines"]))
    vm = ep.get("voice_model", {})
    lead = float(vm.get("lead_in", 0.7))
    out = [np.zeros(int(lead * SR))]
    t = lead
    timing, report = [], []
    fade = int(fade_ms * 1e-3 * SR)
    for path, lines in groups:
        x = decode(path, threads=threads)
        syl = [max(1, syllables(ln["say"])) for ln in lines]
        spans, info = align(x, syl)
        report.append(dict(file=os.path.basename(path), dur=round(len(x) / SR, 2), lines=len(lines), **info))
        for k, (ln, (a, b)) in enumerate(zip(lines, spans)):
            a2, b2 = max(0.0, a - pad_s), min(len(x) / SR, b + pad_s)
            seg = x[int(a2 * SR):int(b2 * SR)].copy()
            if len(seg) > 2 * fade:
                ramp = np.linspace(0, 1, fade)
                seg[:fade] *= ramp
                seg[-fade:] *= ramp[::-1]
            if keep_pauses and k + 1 < len(spans):
                gap = max(0.12, spans[k + 1][0] - b)          # natural gap speech-end -> next speech-start
            else:
                gap = float(ln.get("pause_after", 0.45))       # target gap from the TSV
            if k + 1 == len(spans) and groups and (path, lines) == groups[-1]:
                gap = float(ln.get("pause_after", 0.45))
            timing.append(dict(id=ln["id"], t0=round(t + (a - a2), 4), t1=round(t + (b - a2), 4),
                               pause_after=round(gap, 4), src=os.path.basename(path),
                               src_t0=round(a, 3), src_t1=round(b, 3)))
            out.append(seg)
            t += len(seg) / SR
            sil_n = max(0, int(round((gap - 2 * pad_s) * SR)))  # padding already carries 2 x pad of quiet
            out.append(np.zeros(sil_n))
            t += sil_n / SR
    end = float(ep.get("end_card_s", 0.0))
    out.append(np.zeros(int(end * SR)))
    voice = np.concatenate(out)
    voice_n, ln_info = normalize(voice, target=target_lufs)
    narr = write_wav(os.path.join(out_dir, "narration.wav"), voice_n)
    mix_path = narr
    mix_info = None
    if bgm:
        m = decode(bgm, threads=threads)
        reps = int(math.ceil(len(voice_n) / max(1, len(m))))
        m = np.tile(m, reps)[:len(voice_n)]
        fi, fo = int(1.0 * SR), int(3.0 * SR)
        m[:fi] *= np.linspace(0, 1, fi)
        m[-fo:] *= np.linspace(1, 0, fo)
        m = m * 10 ** ((bgm_lufs - lufs(m)) / 20)
        mix = voice_n + m
        if true_peak_db(mix) > -1.0:
            mix = limiter(mix, ceiling_db=-1.5)
        mix_path = write_wav(os.path.join(out_dir, "mix.wav"), mix)
        mix_info = dict(bgm=os.path.basename(bgm), bgm_lufs=bgm_lufs, mix_lufs=round(lufs(mix), 2),
                        mix_tp=round(true_peak_db(mix), 2))
    tj = dict(lines=timing, total=round(len(voice_n) / SR, 3), lead_in=lead, files=report)
    with open(os.path.join(out_dir, "timing.json"), "w", encoding="utf-8") as f:
        json.dump(tj, f, ensure_ascii=False, indent=1)
    return dict(narration=narr, mix=mix_path, timing=os.path.join(out_dir, "timing.json"), loudness=ln_info,
                mix_info=mix_info, files=report, total_s=tj["total"])


# ------------------------------------------------------------------ qc
def _f0(x, sr=SR):
    import audio_measure as am
    return am.yin_f0(x, sr)


def audition_lines(ep_dir):
    import re
    p = os.path.join(ep_dir, "voice_audition.txt")
    out = []
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            m = re.match(r"^\s*(\d+)\.\s+(.*?)\s{2,}\(", line)
            if m:
                out.append(m.group(2).strip())
    return out


#: 이음매 점검 (1저자 11-24 밤 "14–17 초처럼 ai틱 · 전체적으로 확인 · avi 스킬에 넣어줭").  ep01 v1 (preset 섞음 · 문장별 빠르기)
#: = 이음매 112 중 27 곳이 이웃 문장보다 2.5 반음 넘게 높거나 낮았다 (톤 바뀜 18 · 최대 ±6.7) · 1저자가 짚은 14 초 = −3.3 ·
#: 같은 구간 smart (앞뒤 문맥) = 최대 0.8.  문턱은 그 둘 사이 — 귀로 들은 것과 맞춘 경험값이지 표준이 아니다.
JOIN_JUMP_ST = 2.5
_CONT_END = re.compile(r"(도요|는데요|인데요|고요|지만요|면요|서요|니까요|거든요|데요)[.]?$")


def joins(rows, lid, ledger=None, t_end=None):
    """이웃 문장 이음매마다: 목소리 높이 (F0 중앙) 차 · 원장의 톤 / 빠르기 / 방식 바뀜 · '…요.' 로 이어지는 말이 끊긴 자리.
    rows = qc 문장 행 (id · f0_med · pause_after) · lid = id → 대본 줄 (say) · ledger = id → typecast 원장 줄 · t_end = id → 끝 시각."""
    ledger, t_end = ledger or {}, t_end or {}
    out = []
    for a, b in zip(rows, rows[1:]):
        why, d = [], None
        if a.get("f0_med") and b.get("f0_med"):
            d = round(12 * math.log2(b["f0_med"] / a["f0_med"]), 2)
            if abs(d) >= JOIN_JUMP_ST:
                why.append(f"높이 {d:+.1f} 반음")
        la, lb = ledger.get(a["id"]), ledger.get(b["id"])
        if la and lb:
            if la.get("mode") != lb.get("mode"):
                why.append(f"방식 {la.get('mode')}→{lb.get('mode')}")
            if la.get("preset") != lb.get("preset"):
                why.append(f"톤 {la.get('preset')}→{lb.get('preset')}")
            if la.get("tempo") is not None and lb.get("tempo") is not None and abs(la["tempo"] - lb["tempo"]) >= 0.06:
                why.append(f"빠르기 {la['tempo']}→{lb['tempo']}")
        say = ((lid.get(a["id"]) or {}).get("say") or "").strip()
        if _CONT_END.search(say) and (a.get("pause_after") or 0.0) < 0.6:
            why.append("이어지는 말 끊김 (앞 문장이 '…요.' 로 뒤에 이어짐)")
        out.append(dict(a=a["id"], b=b["id"], t=t_end.get(a["id"]), d_st=d,
                        jump=bool(d is not None and abs(d) >= JOIN_JUMP_ST), why=why))
    return out


def qc(ep, ep_dir, wav=None, text_lines=None):
    out_dir = os.path.join(ep_dir, "audio")
    path = wav or os.path.join(out_dir, "narration.wav")
    x = decode(path)
    tj_path = os.path.join(out_dir, "timing.json")
    tj = json.load(open(tj_path, encoding="utf-8")) if (wav is None and os.path.exists(tj_path)) else None
    lid = {ln["id"]: ln for sc in ep["scenes"] for ln in sc["lines"]}
    if tj is None and wav and text_lines is None and os.path.basename(wav).startswith("audition"):
        text_lines = audition_lines(ep_dir)
    if tj is None and text_lines:
        spans, _ = align(x, [max(1, syllables(t)) for t in text_lines])
        lines = []
        for k, (t_, (a, b)) in enumerate(zip(text_lines, spans)):
            lid[f"a{k + 1:02d}"] = dict(say=t_)
            nxt = spans[k + 1][0] if k + 1 < len(spans) else b
            lines.append(dict(id=f"a{k + 1:02d}", t0=a, t1=b, pause_after=max(0.0, nxt - b)))
        tj = dict(lines=lines)
    if tj is None:
        # stand-alone file (e.g. a voice audition): treat each detected speech run as a 'line'
        sil, _ = silences(x, min_dur=0.25)
        s0, s1 = speech_bounds(x)
        cuts = [s0] + [v for ab in sil for v in ab if s0 < ab[0] < s1] + [s1]
        lines = [dict(id=f"run{k + 1:02d}", t0=cuts[2 * k], t1=cuts[2 * k + 1],
                      pause_after=(cuts[2 * k + 2] - cuts[2 * k + 1]) if 2 * k + 2 < len(cuts) else 0.0)
                 for k in range(len(cuts) // 2)]
    else:
        lines = tj["lines"]
    tf, f0, ap = _f0(x)
    lev, hop = frames_db(x)
    ref = np.percentile(lev, 90)
    rows = []
    for d in lines:
        a, b = d["t0"], d["t1"]
        ln = lid.get(d["id"])
        syl = syllables(ln["say"]) if ln else None
        dur = b - a
        m = (tf >= a) & (tf < b)
        lv = np.interp(tf[m], np.arange(len(lev)) * hop + 0.015, lev)
        v = m.copy()
        v[m] = (ap[m] < 0.2) & (lv > ref - 25) & (f0[m] > 60) & (f0[m] < 420)
        ff, tt = f0[v], tf[v]
        rng = fin = med = None
        if len(ff) > 8:
            med = float(np.median(ff))
            rng = float(12 * np.log2(np.percentile(ff, 90) / np.percentile(ff, 10)))
            last = ff[tt >= tt[-1] - 0.25]
            fin = float(12 * np.log2(np.median(last) / med))
        # internal pauses (breaths at commas) inside the sentence
        seg = x[int(a * SR):int(b * SR)]
        sil, _ = silences(seg, min_dur=0.12) if len(seg) > SR * 0.5 else ([], None)
        q = ln["say"].rstrip().endswith("?") if ln else False
        rows.append(dict(id=d["id"], syl=syl, dur=round(dur, 2), rate=round(syl / dur, 2) if syl else None,
                         pause_after=round(d.get("pause_after", 0.0), 2), f0_med=round(med, 1) if med else None,
                         range_st=round(rng, 1) if rng else None, final_st=round(fin, 1) if fin is not None else None,
                         internal_pauses=len(sil), question=q))
    # 이음매 (원장이 있으면 톤 · 빠르기 · 방식 바뀜도)
    led_path = os.path.join(ep_dir, "audio_in", "typecast_ledger.json")
    try:
        led = json.load(open(led_path, encoding="utf-8")).get("lines", {}) if (tj is not None and wav is None
                                                                            and os.path.exists(led_path)) else {}
    except (OSError, ValueError):
        led = {}
    js = joins(rows, lid, led, {d["id"]: d["t1"] for d in lines})
    jumps = [j for j in js if j["jump"]]
    dsts = np.array([abs(j["d_st"]) for j in js if j["d_st"] is not None])
    # summary + flags
    rates = np.array([r["rate"] for r in rows if r["rate"]])
    pauses = np.array([r["pause_after"] for r in rows[:-1]]) if len(rows) > 1 else np.array([0.0])
    fins = np.array([r["final_st"] for r in rows if r["final_st"] is not None])
    qf = np.array([r["final_st"] for r in rows if r["final_st"] is not None and r["question"]])
    sf = np.array([r["final_st"] for r in rows if r["final_st"] is not None and not r["question"]])
    clip = int(np.sum(np.abs(x) >= 0.999))
    L = lufs(x)
    tp = true_peak_db(x)
    flags = []
    if len(pauses) > 3 and pauses.std() / max(1e-6, pauses.mean()) < 0.25:
        flags.append("문장 뒤 쉼이 너무 고르다 (변동계수 < 0.25) — 레퍼런스의 기계 같은 꼴")
    if len(rates) > 3 and rates.std() / rates.mean() < 0.06:
        flags.append("문장별 빠르기가 너무 고르다 (변동계수 < 0.06)")
    if len(fins) > 3 and fins.std() < 1.5:
        flags.append("문장 끝 억양이 거의 같다 (표준편차 < 1.5 반음)")
    if len(qf) and len(sf) and (qf.mean() - sf.mean()) < 1.0:
        flags.append(f"물음 끝 억양이 평서와 비슷하다 (물음 {qf.mean():.1f} vs 평서 {sf.mean():.1f} 반음)")
    longs = [r["id"] for r in rows if r["syl"] and r["syl"] > 40 and r["internal_pauses"] == 0]
    if longs:
        flags.append(f"40 음절 넘는 문장에 숨 (쉼) 이 없다: {', '.join(longs)}")
    if jumps:
        flags.append(f"이웃 문장보다 목소리 높이가 {JOIN_JUMP_ST} 반음 넘게 뛴 이음매 {len(jumps)} 곳 (최대 {dsts.max():.1f}) — "
                     "'## 이음매' 시각을 귀로 확인 · 그 문장을 앞뒤 문맥 (smart) 으로 다시 만든다")
    if clip:
        flags.append(f"클리핑 표본 {clip} 개")
    if abs(L - (-14.0)) > 1.0 and tj is not None:
        flags.append(f"음량 {L:.1f} LUFS (목표 −14 ± 1)")
    if tp > -1.0:
        flags.append(f"참 최고점 {tp:.1f} dBTP (목표 ≤ −1)")
    summ = dict(file=os.path.basename(path), lines=len(rows), lufs=round(L, 2), true_peak_dbtp=round(tp, 2),
                rate_median=round(float(np.median(rates)), 2) if len(rates) else None,
                rate_cv=round(float(rates.std() / rates.mean()), 3) if len(rates) else None,
                pause_median=round(float(np.median(pauses)), 2), pause_cv=round(float(pauses.std() / max(1e-6, pauses.mean())), 3),
                pause_hist=np.histogram(pauses, [0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.5, 3.0])[0].tolist(),
                final_st_median=round(float(np.median(fins)), 2) if len(fins) else None,
                final_st_sd=round(float(fins.std()), 2) if len(fins) else None,
                clipping=clip, join_n=len(js), join_jumps=len(jumps),
                join_max_st=round(float(dsts.max()), 2) if len(dsts) else None,
                join_p95_st=round(float(np.percentile(dsts, 95)), 2) if len(dsts) else None, flags=flags)
    md = [f"# 음성 QC — {summ['file']}", "",
          f"- 음량 {summ['lufs']} LUFS (스테레오 L=R 기준) · 참 최고점 {summ['true_peak_dbtp']} dBTP · 클리핑 {clip}",
          f"- 빠르기 중앙 {summ['rate_median']} 음절/s (변동계수 {summ['rate_cv']}) · 레퍼런스 8.37 (0.15)",
          f"- 문장 뒤 쉼 중앙 {summ['pause_median']} s (변동계수 {summ['pause_cv']}) · 분포 {summ['pause_hist']} "
          f"(구간 0 · 0.2 · 0.3 · 0.4 · 0.5 · 0.6 · 0.8 · 1.0 · 1.5 · 3.0 s) · 레퍼런스 문장 끝 0.335 s (80 % 가 0.24–0.46)",
          f"- 문장 끝 억양 중앙 {summ['final_st_median']} 반음 (표준편차 {summ['final_st_sd']}) · 레퍼런스 −4.1 반음",
          "", "## 알림", ""] + ([f"- ⚠ {f}" for f in flags] or ["- 없음"]) + [
          "", "## 이음매", "",
          f"- 이음매 {summ['join_n']} · 높이 뜀 (≥ {JOIN_JUMP_ST} 반음) {summ['join_jumps']} · 이웃 높이 차 최대 {summ['join_max_st']} · "
          f"95 % {summ['join_p95_st']} 반음 · 표 = 뜀 또는 까닭이 있는 이음매 (높이 차 큰 순 · 40 개까지)", "",
          "| 시각 (앞 문장 끝) | 앞 → 뒤 | 높이 차 반음 | 까닭 |", "|---|---|---|---|"]
    for j in sorted([j for j in js if j["jump"] or j["why"]], key=lambda j: -abs(j["d_st"] or 0))[:40]:
        tt = j["t"]
        md.append(f"| {int(tt // 60)}:{tt % 60:04.1f} | {j['a']} → {j['b']} | {j['d_st']} | {' · '.join(j['why']) or '—'} |"
                  if tt is not None else f"| — | {j['a']} → {j['b']} | {j['d_st']} | {' · '.join(j['why']) or '—'} |")
    md += ["", "## 문장별", "", "| 문장 | 음절 | 길이 s | 음절/s | 뒤 쉼 s | F0 중앙 Hz | 범위 반음 | 끝 반음 | 안 쉼 | 물음 |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['id']} | {r['syl']} | {r['dur']} | {r['rate']} | {r['pause_after']} | {r['f0_med']} | "
                  f"{r['range_st']} | {r['final_st']} | {r['internal_pauses']} | {'예' if r['question'] else ''} |")
    rep_md = os.path.join(out_dir, "audio_qc.md" if wav is None else f"audio_qc_{os.path.splitext(os.path.basename(wav))[0]}.md")
    os.makedirs(out_dir, exist_ok=True)
    with open(rep_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    with open(rep_md[:-3] + ".json", "w", encoding="utf-8") as f:
        json.dump(dict(summary=summ, rows=rows, joins=js), f, ensure_ascii=False, indent=1)
    return rep_md


# ------------------------------------------------------------------ synthetic test voice
def synth_line(text_say, rate=7.0, speed=1.0, question=False, f0=130.0, seed=0, comma_pause=0.2):
    """Voiced 'syllables' with a declining F0 contour; commas -> pauses.  For pipeline tests only."""
    rng = np.random.default_rng(seed)
    parts = [p for p in text_say.replace("?", "").replace(".", "").split(",")]
    out = []
    n_tot = max(1, syllables(text_say))
    k_glob = 0
    for pi, p in enumerate(parts):
        n = max(1, syllables(p))
        for k in range(n):
            dur = 1.0 / (rate * speed) * rng.uniform(0.85, 1.15)
            ns = int(dur * SR)
            t = np.arange(ns) / SR
            u = k_glob / max(1, n_tot - 1)
            f = f0 * 2 ** ((2.0 - 5.0 * u) / 12) if not (question and u > 0.85) else f0 * 2 ** (3.0 / 12)
            ph = 2 * np.pi * f * t
            s = sum((0.6 / h) * np.sin(h * ph) for h in range(1, 6))
            env = np.minimum(1, t / 0.015) * np.minimum(1, (dur - t) / 0.03)
            env = np.clip(env, 0, 1) * (0.9 + 0.1 * rng.random())
            gap = int(0.012 * SR)
            out.append(s * env * 0.3)
            out.append(rng.normal(0, 0.002, gap))
            k_glob += 1
        if pi < len(parts) - 1:
            out.append(rng.normal(0, 0.0005, int(comma_pause * SR)))
    return np.concatenate(out)


def selftest(work):
    import shutil
    os.makedirs(work, exist_ok=True)
    ep = dict(episode="ep99_test", voice_model=dict(lead_in=0.5), end_card_s=1.0, scenes=[])
    lines_a = ["첫 번째 문장은 이렇게 시작합니다.", "두 번째 문장은, 쉼표가 하나 있어요.", "짧은 문장.",
               "네 번째 문장은 조금 더 길게, 여러 낱말을 이어서 말해 봅니다.", "마지막은 물음일까요?"]
    lines_b = ["다음 장면의 첫 문장입니다.", "그리고 이어지는 두 번째 문장이죠.", "세 번째로 끝납니다."]
    targets = [0.45, 0.6, 0.35, 0.9, 1.5]
    for sid, ls in (("s01", lines_a), ("s02", lines_b)):
        sc = dict(id=sid, title=sid, lines=[], shots=[])
        for k, t in enumerate(ls):
            sc["lines"].append(dict(id=f"{sid}_l{k + 1:02d}", text=t, say=t, pause_after=targets[k % len(targets)], speed=1.0))
        ep["scenes"].append(sc)
    in_dir = os.path.join(work, "audio_in")
    if os.path.isdir(in_dir):
        shutil.rmtree(in_dir)
    os.makedirs(in_dir)
    truth = {}
    rng = np.random.default_rng(3)
    for sc in ep["scenes"]:
        parts = [np.zeros(int(0.3 * SR))]
        t = 0.3
        for k, ln in enumerate(sc["lines"]):
            y = synth_line(ln["say"], rate=7.0, question=ln["say"].endswith("?"), seed=k + 7)
            truth[ln["id"]] = (t, t + len(y) / SR)
            parts.append(y)
            t += len(y) / SR
            gap = 0.4 + 0.02 * rng.standard_normal()   # 'TTS default' pause, nearly uniform
            parts.append(rng.normal(0, 0.0003, int(gap * SR)))
            t += gap
        write_wav(os.path.join(in_dir, f"ep99_{sc['id']}.wav"), np.concatenate(parts), stereo=False)
    res = prep(ep, work, in_dir=in_dir)
    tj = json.load(open(res["timing"], encoding="utf-8"))
    errs = []
    for d in tj["lines"]:
        a, b = truth[d["id"]]
        errs.append(max(abs(d["src_t0"] - a), abs(d["src_t1"] - b)))
    x = decode(res["narration"])
    # retimed pauses = gap between t1 and next t0 (should equal targets within pad/fade tolerance)
    pz = [round(tj["lines"][i + 1]["t0"] - tj["lines"][i]["t1"], 3) for i in range(len(tj["lines"]) - 1)]
    tgt = [ln["pause_after"] for sc in ep["scenes"] for ln in sc["lines"]][:-1]
    perr = max(abs(p - t_) for p, t_ in zip(pz, tgt))
    L, tp = lufs(x), true_peak_db(x)
    rep = qc(ep, work)
    ok = dict(alignment_max_err_s=round(max(errs), 3), pause_retime_max_err_s=round(perr, 3),
              lufs=round(L, 2), true_peak=round(tp, 2))
    checks = [("alignment ≤ 0.06 s", max(errs) <= 0.06), ("pause re-time ≤ 0.03 s", perr <= 0.03),
              ("loudness −14 ± 0.5", abs(L + 14) <= 0.5), ("true peak ≤ −1.0 dBTP", tp <= -1.0),
              ("qc report written", os.path.exists(rep))]
    # one file per sentence (TTS API output): random lead / tail silence, boundaries must come out exact
    w2 = os.path.join(work, "per_line")
    in2 = os.path.join(w2, "audio_in")
    if os.path.isdir(w2):
        shutil.rmtree(w2)
    os.makedirs(in2)
    sp_truth = {}
    for sc in ep["scenes"]:
        for k, ln in enumerate(sc["lines"]):
            y = synth_line(ln["say"], rate=7.0, question=ln["say"].endswith("?"), seed=k + 21)
            lead_s, tail_s = 0.15 + 0.2 * rng.random(), 0.2 + 0.3 * rng.random()
            sig = np.concatenate([rng.normal(0, 0.0003, int(lead_s * SR)), y, rng.normal(0, 0.0003, int(tail_s * SR))])
            sp_truth[ln["id"]] = (lead_s, lead_s + len(y) / SR)
            write_wav(os.path.join(in2, f"ep99_{ln['id']}.wav"), sig, stereo=False)
    res2 = prep(ep, w2, in_dir=in2)
    tj2 = json.load(open(res2["timing"], encoding="utf-8"))
    err2 = max(max(abs(d["src_t0"] - sp_truth[d["id"]][0]), abs(d["src_t1"] - sp_truth[d["id"]][1])) for d in tj2["lines"])
    pz2 = [tj2["lines"][i + 1]["t0"] - tj2["lines"][i]["t1"] for i in range(len(tj2["lines"]) - 1)]
    perr2 = max(abs(p - t_) for p, t_ in zip(pz2, tgt))
    checks += [("per-sentence files: boundaries ≤ 0.06 s", err2 <= 0.06), ("per-sentence files: pause re-time ≤ 0.03 s", perr2 <= 0.03)]
    ok.update(per_line_boundary_max_err_s=round(err2, 3), per_line_pause_max_err_s=round(perr2, 3))
    # 이음매 점검 (1저자 11-24 밤 "14–17 초처럼 ai틱 · 전체적으로 확인 · avi 스킬에 넣어줭")
    try:
        rows_j = [dict(id="a", f0_med=200.0, pause_after=0.45), dict(id="b", f0_med=206.0, pause_after=0.35),
                  dict(id="c", f0_med=290.0, pause_after=0.5), dict(id="d", f0_med=None, pause_after=0.4)]
        lid_j = {"a": dict(say="첫 문장입니다."), "b": dict(say="같은 비율로 섞어도요."), "c": dict(say="결과가 달라집니다."),
                 "d": dict(say="끝.")}
        led_j = {"a": dict(preset="normal", tempo=1.0, mode="preset"), "b": dict(preset="toneup", tempo=1.08, mode="preset"),
                 "c": dict(preset="normal", tempo=1.0, mode="preset"), "d": dict(preset=None, tempo=1.0, mode="smart")}
        js = joins(rows_j, lid_j, led_j, {"a": 1.0, "b": 2.0, "c": 3.0, "d": 4.0})
        by = {(j["a"], j["b"]): j for j in js}
        checks += [("★ 이음매: 이웃 높이 차 ≥ 2.5 반음만 '뜀' (+0.5 반음은 아님 · +5.9 반음은 뜀)",
                    not by[("a", "b")]["jump"] and by[("b", "c")]["jump"] and abs(by[("b", "c")]["d_st"] - 5.89) < 0.05),
                   ("★ 이음매: F0 없는 문장 = 판정 안 함 (None · 뜀 아님)", by[("c", "d")]["d_st"] is None and not by[("c", "d")]["jump"]),
                   ("★ 이음매: 톤 · 빠르기 · 방식 바뀜을 원장에서 적는다",
                    any("톤 normal→toneup" in w for w in by[("a", "b")]["why"]) and any("빠르기" in w for w in by[("a", "b")]["why"])
                    and any("방식" in w for w in by[("c", "d")]["why"])),
                   ("★ 이음매: '~도요.' 다음 짧은 쉼 = 이어지는 말 끊김", any("이어지는 말" in w for w in by[("b", "c")]["why"]))]
        rep_j = json.load(open(rep[:-3] + ".json", encoding="utf-8"))
        checks.append(("★ 이음매: qc 보고 (json · md) 에 이음매 절", "joins" in rep_j and "join_jumps" in rep_j["summary"]
                       and "## 이음매" in open(rep, encoding="utf-8").read()))
    except Exception as ex:                                   # noqa: BLE001 — a crash is a FAIL
        checks.append((f"★ 이음매 점검 [{type(ex).__name__}: {ex}]", False))
    for name, good in checks:
        print(("PASS " if good else "FAIL ") + name)
    print(json.dumps(ok, ensure_ascii=False))
    print("qc report:", rep)
    return all(g for _, g in checks)
