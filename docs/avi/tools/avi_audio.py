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
         flags for 'mechanical' signatures measured on the reference video;
         S7 강약 · 이어지는 말 · 숨 (avi_prosody · 대리 지표 · 듣기 확인 = 1저자);
         stops when the audio was made from another script version (timing.json ids · ledger text vs scenes.json).
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


def soften_breaths(seg, db, min_s=0.18, rel=18.0, margin=0.02, ramp=0.015):
    """v3.1 (11-25 · 1저자 '숨소리에 약간 기계음'): the quiet stretches INSIDE a sentence — 10 ms level below the sentence's
    speech median − rel dB for ≥ min_s, with speech on both sides (the padded file edges are never touched) — are the
    TTS's breaths at commas.  Scale them by db (≤ 0) with raised-cosine ramps that stay `margin` away from the speech.
    The pause length is unchanged (timing, captions and screen anchors do not move).  Returns (segment, [(t0, t1, peak_db)])."""
    hop = int(0.01 * SR)
    n = len(seg) // hop
    if db >= 0 or n < 5:
        return seg, []
    lv = 20 * np.log10(np.sqrt(np.mean(seg[:n * hop].reshape(n, hop) ** 2, axis=1)) + 1e-12)
    sp = lv > -60
    if not sp.any():
        return seg, []
    med = float(np.median(lv[sp]))
    low = lv < med - rel
    out, found = seg.copy(), []
    g = 10 ** (db / 20.0)
    r = int(ramp * SR)
    w = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, r))          # 0 -> 1
    k = 0
    while k < n:
        if not low[k]:
            k += 1
            continue
        j = k
        while j < n and low[j]:
            j += 1
        if k > 0 and j < n and (j - k) * 0.01 >= min_s:
            s0, s1 = k * hop + int(margin * SR), j * hop - int(margin * SR)
            if s1 - s0 > 2 * r:
                env = np.full(s1 - s0, g)
                env[:r] = 1 - (1 - g) * w
                env[-r:] = g + (1 - g) * w
                out[s0:s1] *= env
                found.append((round(k * 0.01, 2), round(j * 0.01, 2), round(float(lv[k:j].max()), 1)))
        k = j
    return out, found


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
    breath_db = float(vm.get("breath_db", 0.0) or 0.0)                 # v3.1: 0 = off (old behaviour)
    breath_min = float(vm.get("breath_min_s", 0.18))
    gains, gp = {}, os.path.join(in_dir, "line_gain.json")              # v3.1: per-sentence gain, tied to the take (sha256)
    if os.path.exists(gp):
        gains = json.load(open(gp, encoding="utf-8"))
    out = [np.zeros(int(lead * SR))]
    t = lead
    timing, report = [], []
    fade = int(fade_ms * 1e-3 * SR)
    for path, lines in groups:
        x = decode(path, threads=threads)
        g_db, g_note = 0.0, None
        if len(lines) == 1 and lines[0]["id"] in gains:
            import hashlib
            gi = gains[lines[0]["id"]]
            if gi.get("sha256") == hashlib.sha256(open(path, "rb").read()).hexdigest():
                g_db = float(gi.get("db", 0.0))
                x = x * 10 ** (g_db / 20.0)
            else:
                g_note = "sha"                                              # another take now: the gain was not for it
        syl = [max(1, syllables(ln["say"])) for ln in lines]
        spans, info = align(x, syl)
        report.append(dict(file=os.path.basename(path), dur=round(len(x) / SR, 2), lines=len(lines), **info))
        for k, (ln, (a, b)) in enumerate(zip(lines, spans)):
            a2, b2 = max(0.0, a - pad_s), min(len(x) / SR, b + pad_s)
            seg = x[int(a2 * SR):int(b2 * SR)].copy()
            soft = []
            if breath_db < 0:
                seg, soft = soften_breaths(seg, breath_db, min_s=breath_min)
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
                               src_t0=round(a, 3), src_t1=round(b, 3), gain_db=round(g_db, 2), breaths_softened=len(soft),
                               **({"gain_skipped": g_note} if g_note else {})))
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


def _norm_say(t):
    return re.sub(r"\s+", " ", (t or "").strip())


def _same_version(ep, ep_dir, tj):
    """대본 ↔ 음성 판 대조 (S7 · 11-25): timing.json 의 문장 차례가 대본과 다르거나, 원장에 적힌 글이 지금 대본의 읽는 꼴과
    다르면 멈춘다 — 다른 판의 음성을 지금 대본의 낱말 자리 · 강조 낱말로 재면 숫자가 조용히 틀린다 (예: v3 대본 + v2 음성)."""
    want = [ln["id"] for sc in ep["scenes"] for ln in sc["lines"]]
    got = [d["id"] for d in tj.get("lines", [])]
    if want != got:
        k = next((i for i, (u, v) in enumerate(zip(want, got)) if u != v), min(len(want), len(got)))
        raise SystemExit(f"대본 ↔ 음성 판 불일치: 대본 문장 {len(want)} · timing.json {len(got)} · 처음 다른 자리 {k + 1} 번째 "
                         f"(대본 {want[k] if k < len(want) else '없음'} ↔ 음성 {got[k] if k < len(got) else '없음'}) — "
                         "음성을 이 대본으로 다시 만들거나, 이 음성의 대본 (예: 백업 scenes.json) 으로 잰다")
    led_path = os.path.join(ep_dir, "audio_in", "typecast_ledger.json")
    try:
        led = json.load(open(led_path, encoding="utf-8")).get("lines", {}) if os.path.exists(led_path) else {}
    except (OSError, ValueError):
        led = {}
    src = {d["id"]: d.get("src") for d in tj["lines"]}
    bad = []
    import hashlib
    for sc in ep["scenes"]:
        for ln in sc["lines"]:
            e = led.get(ln["id"])
            f_ = os.path.join(ep_dir, "audio_in", src.get(ln["id"]) or "")
            if not (e and e.get("status") == "ok" and e.get("text") is not None and e.get("sha256") and os.path.isfile(f_)):
                continue                                  # no ledger line for this file (hand-made / per-scene input)
            with open(f_, "rb") as fh:
                if hashlib.sha256(fh.read()).hexdigest() != e["sha256"]:
                    continue                              # the file is not the ledger's take -> the ledger text says nothing
            if _norm_say(e["text"]) != _norm_say(ln.get("say") or ln.get("text")):
                bad.append(ln["id"])
    if bad:
        raise SystemExit(f"대본 ↔ 음성 판 불일치: 원장의 글 ≠ 지금 대본의 읽는 꼴 {len(bad)} 문장 ({', '.join(bad[:6])}"
                         f"{' …' if len(bad) > 6 else ''}) — 그 문장 파일은 다른 글로 만든 판이다")


def qc(ep, ep_dir, wav=None, text_lines=None, report=None):
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
    if tj is not None and wav is None:
        _same_version(ep, ep_dir, tj)
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
    # S7 강약 · 이어지는 말 · 숨 (11-25 · 대리 지표 · 듣기 확인 = 1저자) — avi_prosody
    import avi_prosody as P
    thr_q, _, _ = _quiet_threshold(lev)
    lv_all = np.interp(tf, np.arange(len(lev)) * hop + 0.015, lev)
    voiced = (ap < 0.2) & (lv_all > ref - 25) & (f0 > 60) & (f0 < 420)
    lid_p = {ln["id"]: dict(ln, _scene=sc["id"]) for sc in ep["scenes"] for ln in sc["lines"]}
    for k_, v_ in lid.items():
        lid_p.setdefault(k_, v_)
    pro = P.analyze(lines, lid_p, rows, tf, f0, voiced, lev, hop, thr_q)
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
    flags += P.flags(pro)                                   # 강조 낱말 · 이어지는 말 쉼 · 긴 문장 숨 (옛 '40 음절' 알림 대신)
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
                join_p95_st=round(float(np.percentile(dsts, 95)), 2) if len(dsts) else None, flags=flags,
                **pro["summary"])
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
    md += P.md(pro)
    md += ["", "## 문장별", "", "| 문장 | 음절 | 길이 s | 음절/s | 뒤 쉼 s | F0 중앙 Hz | 범위 반음 | 끝 반음 | 안 쉼 | 물음 |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['id']} | {r['syl']} | {r['dur']} | {r['rate']} | {r['pause_after']} | {r['f0_med']} | "
                  f"{r['range_st']} | {r['final_st']} | {r['internal_pauses']} | {'예' if r['question'] else ''} |")
    rep_md = report or os.path.join(out_dir, "audio_qc.md" if wav is None else f"audio_qc_{os.path.splitext(os.path.basename(wav))[0]}.md")
    os.makedirs(os.path.dirname(os.path.abspath(rep_md)), exist_ok=True)
    with open(rep_md, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    with open(rep_md[:-3] + ".json", "w", encoding="utf-8") as f:
        json.dump(dict(summary=summ, rows=rows, joins=js, prosody=pro), f, ensure_ascii=False, indent=1)
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


def synth_marked(text_say, boost_word=None, boost_st=4.0, boost_db=5.0, rate=7.0, f0=130.0, seed=0, comma_pause=0.2,
                 chunk_rates=None, pause_noise=0.0005):
    """synth_line + the true time span of every word (and an optional emphasised word: higher F0 · louder).
    For the S7 강약 · 숨 tests only.  Returns (signal, {word_index: (t0, t1)}, words)."""
    rng = np.random.default_rng(seed)
    words = text_say.replace("?", "").replace(".", "").split()
    n_tot = max(1, syllables(text_say))
    out, spans, t, k_glob = [], {}, 0.0, 0
    chunk = 0
    for wi, w in enumerate(words):
        comma = w.endswith(",")
        n = max(1, syllables(w))
        boost = boost_word is not None and w.rstrip(",") == boost_word
        w0 = t
        r_ = chunk_rates[min(chunk, len(chunk_rates) - 1)] if chunk_rates else rate
        for k in range(n):
            dur = 1.0 / r_ * rng.uniform(0.9, 1.1)
            ns = int(dur * SR)
            tt = np.arange(ns) / SR
            u = k_glob / max(1, n_tot - 1)
            f = f0 * 2 ** ((2.0 - 5.0 * u + (boost_st if boost else 0.0)) / 12)
            ph = 2 * np.pi * f * tt
            sig = sum((0.6 / h) * np.sin(h * ph) for h in range(1, 6))
            env = np.clip(np.minimum(1, tt / 0.015) * np.minimum(1, (dur - tt) / 0.03), 0, 1)
            amp = 0.3 * (10 ** (boost_db / 20) if boost else 1.0)
            out.append(sig * env * amp)
            gap = int(0.012 * SR)
            out.append(rng.normal(0, 0.002, gap))
            t += (ns + gap) / SR
            k_glob += 1
        spans[wi] = (w0, t)
        if comma:
            chunk += 1
            out.append(rng.normal(0, pause_noise, int(comma_pause * SR)))
            t += int(comma_pause * SR) / SR
        elif wi < len(words) - 1:
            sp = int(0.03 * SR)                       # a short word gap (no pause)
            out.append(rng.normal(0, 0.002, sp))
            t += sp / SR
    return np.concatenate(out), spans, words


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
    # S7 강약 · 이어지는 말 · 숨 (1저자 11-25 "보이스 강약이나 이음 등이 아직 부족" · 대리 지표 · 듣기 확인 = 1저자)
    try:
        import avi_prosody as P
        w3 = os.path.join(work, "prosody")
        in3 = os.path.join(w3, "audio_in")
        if os.path.isdir(w3):
            shutil.rmtree(w3)
        os.makedirs(in3)
        long_a = "이 문장은 쉼표 없이 아주 길게 이어지는 문장으로서 숨을 쉴 자리가 하나도 없이 끝까지 한 번에 말하는 문장입니다."
        long_b = "이 문장도 아주 길게 이어지지만 가운데에 쉼표가 하나 있어서, 그 자리에서 잠깐 숨을 쉬고 다시 이어 말하는 문장입니다."
        long_c = "이 문장도 아주 길게 이어지고 가운데에 쉼표가 하나 있지만, 그 자리의 쉼이 아주 짧아서 숨을 쉬었다고 듣기 어려운 문장입니다."
        spec = [  # (say, emphasis, boost word, pause_after, joins_prev (True) / new_thought ("new"), comma pause)
            ("오늘은 정말 중요한 낱말을 강조해서 말해 봅니다.", ["중요한"], "중요한", 0.45, False, 0.2),
            ("이번에는 같은 낱말을 그냥 평평하게 말해 봅니다.", ["낱말을"], None, 0.45, False, 0.2),
            ("없는 낱말 시험입니다.", ["바나나"], None, 0.45, False, 0.2),
            ("같은 비율로 섞어도요.", [], None, 0.6, False, 0.2),
            ("결과는 달라집니다.", [], None, 0.45, False, 0.2),
            ("짧게 이어지는 앞 문장입니다.", [], None, 0.2, False, 0.2),
            ("그래서 이 문장은 바로 이어집니다.", [], None, 0.5, True, 0.2),
            ("이 문장도 이어지지만 앞에서 오래 쉬었어요.", [], None, 0.6, True, 0.2),
            ("새 생각은 따로 시작합니다.", [], None, 0.45, False, 0.2),
            (long_a, [], None, 0.45, False, 0.2),
            (long_b, [], None, 0.45, False, 0.25),
            (long_c, [], None, 0.45, False, 0.10),
            ("짧은 끝 문장입니다.", [], None, 1.0, False, 0.2),
            ("첫 마디는 짧게, 둘째 마디에 있는 강조 낱말을 크게 말합니다.", ["강조"], "강조", 1.0, False, 0.6),
            ("이 문장도 길게 이어지고 쉼표 자리의 쉼에 잡음이 조금 섞여 있지만, 그래도 분명히 숨을 쉬는 자리가 있는 긴 문장입니다.",
             [], None, 1.0, False, 0.3),
            ("그래야 같은 출발에서 비교할 수 있거든요.", [], None, 0.6, False, 0.2),
            ("또 하나, 이 문장은 새 생각을 시작합니다.", [], None, 1.0, "new", 0.2),
        ]
        ep3 = dict(episode="ep98_prosody", voice_model=dict(lead_in=0.5), end_card_s=1.0,
                   scenes=[dict(id="s01", title="s01", lines=[], shots=[])])
        marks = {}
        for k, (say, emph, bw, pz, jp, cp) in enumerate(spec):
            lid3 = f"s01_l{k + 1:02d}"
            d = dict(id=lid3, text=say, say=say, pause_after=pz, speed=1.0, emphasis=emph)
            if jp is True:
                d["joins_prev"] = True
            elif jp == "new":
                d["new_thought"] = True
            ep3["scenes"][0]["lines"].append(d)
            y, spans, words = synth_marked(say, boost_word=bw, seed=40 + k, comma_pause=cp,
                                           chunk_rates=[4.0, 9.0] if k == 13 else None,
                                           pause_noise=0.006 if k == 14 else 0.0005)   # l15: comma pause ≈ 28 dB under speech
            lead = 0.2
            marks[lid3] = (lead, spans, words)
            write_wav(os.path.join(in3, f"ep98_{lid3}.wav"),
                      np.concatenate([rng.normal(0, 0.0003, int(lead * SR)), y, rng.normal(0, 0.0003, int(0.3 * SR))]), stereo=False)
        res3 = prep(ep3, w3, in_dir=in3)
        rep3 = qc(ep3, w3)
        q3 = json.load(open(rep3[:-3] + ".json", encoding="utf-8"))
        md3 = open(rep3, encoding="utf-8").read()
        pr = q3.get("prosody") or {}
        em = {(e["id"], e["word"]): e for e in pr.get("emphasis", [])}
        jn = {(j["a"], j["b"]): j for j in pr.get("joins", [])}
        br = {b["id"]: b for b in pr.get("breath", [])}
        checks += [("★ 강약: 올려 말한 강조 낱말 = 힘 받음 (+4 반음 · +5 dB 합성)", em.get(("s01_l01", "중요한"), {}).get("got") is True),
                   ("★ 강약: 평평하게 말한 강조 낱말 = 힘 못 받음", em.get(("s01_l02", "낱말을"), {}).get("got") is False),
                   ("★ 강약: 글에 없는 강조 낱말 = 판정 못 함 (None · 까닭)", ("s01_l03", "바나나") in em
                    and em[("s01_l03", "바나나")].get("got") is None and bool(em[("s01_l03", "바나나")].get("why")))]
        tj3 = json.load(open(res3["timing"], encoding="utf-8"))
        t0_1 = {d["id"]: d for d in tj3["lines"]}["s01_l01"]
        lead, spans1, words1 = marks["s01_l01"]
        wi = words1.index("중요한")
        true_c = t0_1["t0"] - (t0_1["src_t0"] - lead) + (spans1[wi][0] + spans1[wi][1]) / 2
        e1 = em.get(("s01_l01", "중요한"), {})
        est_c = (e1.get("t0", -9) + e1.get("t1", -9)) / 2
        checks.append((f"★ 강약: 낱말 자리 어림 (음절 비례) ≤ 0.3 s 안 (어긋남 {abs(est_c - true_c):.2f} s)", abs(est_c - true_c) <= 0.3))
        t14 = {d["id"]: d for d in tj3["lines"]}["s01_l14"]
        lead14, spans14, words14 = marks["s01_l14"]
        w14 = words14.index("강조")
        true14 = t14["t0"] - (t14["src_t0"] - lead14) + (spans14[w14][0] + spans14[w14][1]) / 2
        e14 = em.get(("s01_l14", "강조"), {})
        est14 = (e14.get("t0", -9) + e14.get("t1", -9)) / 2
        checks.append((f"★ 강약: 쉼표 뒤 낱말 자리 = 쉼표 자리의 쉼에 맞춰 어림 (마디 빠르기 4 ↔ 9 음절/s · 어긋남 {abs(est14 - true14):.2f} s ≤ 0.15)",
                       abs(est14 - true14) <= 0.15 and e14.get("got") is True))
        checks += [("★ 숨: '…요.' 로 이어지는 쌍의 0.6 s 쉼 = 김", jn.get(("s01_l04", "s01_l05"), {}).get("long") is True),
                   ("★ 숨: 대본 이음 표지 + 0.2 s 쉼 = 걸림 없음", jn.get(("s01_l06", "s01_l07"), {}).get("long") is False),
                   ("★ 숨: 대본 이음 표지 + 0.5 s 쉼 = 김", jn.get(("s01_l07", "s01_l08"), {}).get("long") is True),
                   ("★ 숨: 이어지지 않는 쌍 (표지 없음 · 끝 '~어요') = 이음 쌍 아님 (이음 쌍 목록은 있음)", len(jn) >= 3 and ("s01_l08", "s01_l09") not in jn),
                   ("★ 숨: '…거든요.' 뒤라도 대본 표지 '새 생각' (new_thought) 이면 이음 쌍 아님 (0.6 s 쉼 = 걸림 아님)",
                    len(jn) >= 3 and ("s01_l16", "s01_l17") not in jn)]
        checks += [(f"★ 숨: {syllables(long_a)} 음절 · 쉼표 없음 = 숨 없음", syllables(long_a) >= 40 and br.get("s01_l10", {}).get("no_breath") is True),
                   ("★ 숨: 쉼표 자리 0.25 s 쉼 = 숨 있음", syllables(long_b) >= 40 and br.get("s01_l11", {}).get("no_breath") is False),
                   ("★ 숨: 쉼표 자리 0.10 s 쉼 (< 0.15) = 숨 없음", syllables(long_c) >= 40 and br.get("s01_l12", {}).get("no_breath") is True),
                   ("★ 숨: 40 음절 아래 문장은 보지 않는다 (긴 문장 목록은 있음)", len(br) == 4 and "s01_l01" not in br),
                   ("★ 숨: 쉼표 자리의 쉼이 디지털 무음이 아니어도 (말보다 ≈ 28 dB 낮은 잡음 · Typecast 꼴) = 숨 있음 "
                    "(문장마다의 쉼 문턱)", br.get("s01_l15", {}).get("no_breath") is False)]
        checks.append(("★ qc 보고 (md) 에 '## 강약' · '## 숨' 절 · 대리 지표 표지 · json 요약 수",
                       "## 강약" in md3 and "## 숨" in md3 and "대리 지표" in md3 and "듣기 확인 = 1저자" in md3
                       and all(k in q3.get("summary", {}) for k in ("emph_n", "emph_missed", "join_cont_n", "join_cont_long",
                                                                     "breath_n", "breath_missing"))))
        alt = qc(ep3, w3, report=os.path.join(w3, "other", "qc_alt.md"))
        checks.append(("★ qc report= (avi.py audio-qc --out) = 그 자리에 md · json", alt.endswith("qc_alt.md") and os.path.exists(alt)
                       and json.load(open(alt[:-3] + ".json", encoding="utf-8"))["prosody"]["summary"] == pr.get("summary")))
        # 대본 ↔ 음성 판 불일치 = 멈춤 (v3 대본 + v2 음성 같은 상황)
        ep_bad = json.loads(json.dumps(ep3))
        ep_bad["scenes"][0]["lines"].insert(3, dict(id="s01_l99", text="끼워 넣은 문장.", say="끼워 넣은 문장.", pause_after=0.4))
        try:
            qc(ep_bad, w3)
            checks.append(("★ 판 불일치 (대본 문장 ≠ timing.json) = 멈춤", False))
        except SystemExit as ex:
            checks.append(("★ 판 불일치 (대본 문장 ≠ timing.json) = 멈춤", "불일치" in str(ex)))
    except Exception as ex:                                   # noqa: BLE001 — a crash is a FAIL
        checks.append((f"★ 강약 · 숨 점검 [{type(ex).__name__}: {ex}]", False))
    # v3.1 (11-25 · 1저자 듣기 피드백): 문장 안 숨 줄이기 (voice_model.breath_db) · 문장별 음량 (audio_in/line_gain.json ·
    # 그 판의 sha256 이 맞을 때만) — 시험 먼저 (기능 전에는 실패해야 한다)
    try:
        import hashlib

        def _run4(name, breath_db, gain):
            w4 = os.path.join(work, name)
            in4 = os.path.join(w4, "audio_in")
            if os.path.isdir(w4):
                shutil.rmtree(w4)
            os.makedirs(in4)
            vm4 = dict(lead_in=0.5)
            if breath_db:
                vm4["breath_db"] = breath_db
            ep4 = dict(episode="ep97_breath", voice_model=vm4, end_card_s=0.5,
                       scenes=[dict(id="s01", title="s01", lines=[], shots=[])])
            r4 = np.random.default_rng(11)
            tt = np.arange(int(0.8 * SR)) / SR

            def tone(f):
                return 0.3 * np.sin(2 * np.pi * f * tt) * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * tt)) ** 2

            sents = {"s01_l01": np.concatenate([tone(150), r4.normal(0, 0.006, int(0.3 * SR)), tone(160)]),   # 0.3 s 숨
                     "s01_l02": np.concatenate([tone(140), r4.normal(0, 0.006, int(0.12 * SR)), tone(150)]),  # 0.12 s (닫힘)
                     "s01_l03": np.concatenate([tone(150), tone(150)])}
            for lid4, y in sents.items():
                ep4["scenes"][0]["lines"].append(dict(id=lid4, text="문장", say="문장 하나 둘 셋", pause_after=0.5, speed=1.0))
                write_wav(os.path.join(in4, f"ep97_{lid4}.wav"),
                          np.concatenate([np.zeros(int(0.2 * SR)), y, np.zeros(int(0.2 * SR))]), stereo=False)
            if gain is not None:
                sha3 = hashlib.sha256(open(os.path.join(in4, "ep97_s01_l03.wav"), "rb").read()).hexdigest()
                json.dump({"s01_l03": dict(db=-6.0, sha256=sha3 if gain == "ok" else "0" * 64, why="selftest")},
                          open(os.path.join(in4, "line_gain.json"), "w", encoding="utf-8"))
            prep(ep4, w4, in_dir=in4)
            tj4 = json.load(open(os.path.join(w4, "audio", "timing.json"), encoding="utf-8"))
            x4 = decode(os.path.join(w4, "audio", "narration.wav"))
            L4 = {d["id"]: d for d in tj4["lines"]}

            def db(lid, t0, t1):
                a0 = L4[lid]["t0"]
                seg4 = x4[int((a0 + t0) * SR):int((a0 + t1) * SR)]
                return 20 * np.log10(np.sqrt(np.mean(seg4 ** 2)) + 1e-12)
            return dict(tone1=db("s01_l01", 0.1, 0.7), breath=db("s01_l01", 0.86, 1.04), tone2=db("s01_l01", 1.2, 1.9),
                        clos=db("s01_l02", 0.82, 0.9), tone_l2=db("s01_l02", 0.1, 0.7), l3=db("s01_l03", 0.1, 1.5), L=L4)

        b0 = _run4("breath0", 0.0, None)
        b1 = _run4("breath1", -10.0, "ok")
        b2 = _run4("breath2", -10.0, "bad")
        d_breath = (b1["breath"] - b1["tone1"]) - (b0["breath"] - b0["tone1"])
        checks += [(f"★ 숨 줄이기: 문장 안 0.3 s 숨 = −10 dB (잰 값 {d_breath:+.1f} dB · ± 1.5)", abs(d_breath + 10.0) <= 1.5),
                   ("★ 숨 줄이기: 숨 앞뒤 말 = 그대로 (± 0.3 dB)",
                    abs((b1["tone2"] - b1["tone1"]) - (b0["tone2"] - b0["tone1"])) <= 0.3),
                   ("★ 숨 줄이기: 0.18 s 아래 닫힘 (0.12 s) = 건드리지 않음 (± 0.5 dB)",
                    abs((b1["clos"] - b1["tone_l2"]) - (b0["clos"] - b0["tone_l2"])) <= 0.5),
                   ("★ 숨 줄이기: timing.json 에 줄인 숨 수", b1["L"]["s01_l01"].get("breaths_softened") == 1
                    and b0["L"]["s01_l01"].get("breaths_softened", 0) == 0)]
        d_gain = (b1["l3"] - b1["tone1"]) - (b0["l3"] - b0["tone1"])
        d_bad = (b2["l3"] - b2["tone1"]) - (b0["l3"] - b0["tone1"])
        checks += [(f"★ 문장 음량: line_gain.json −6 dB (sha 맞음) = 그 문장만 −6 dB (잰 값 {d_gain:+.2f} · ± 0.3)",
                    abs(d_gain + 6.0) <= 0.3 and b1["L"]["s01_l03"].get("gain_db") == -6.0),
                   (f"★ 문장 음량: sha 가 다른 판 = 안 씀 + 표지 (잰 값 {d_bad:+.2f})",
                    abs(d_bad) <= 0.3 and b2["L"]["s01_l03"].get("gain_skipped") == "sha")]
    except Exception as ex:
        checks.append((f"★ 숨 줄이기 · 문장 음량 [{type(ex).__name__}: {ex}]", False))
    for name, good in checks:
        print(("PASS " if good else "FAIL ") + name)
    print(json.dumps(ok, ensure_ascii=False))
    print("qc report:", rep)
    return all(g for _, g in checks)
