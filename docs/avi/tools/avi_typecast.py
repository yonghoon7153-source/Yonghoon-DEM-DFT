#!/usr/bin/env python3
"""Typecast TTS for one AVI episode: tts_typecast.tsv -> EP_DIR/audio_in/<ep>_<line id>.wav (one file per sentence).

  python3 -I avi.py typecast EP_DIR                                  # dry run: plan + character count, no API call
  python3 -I avi.py typecast EP_DIR --run --lines s01_l01,s01_l08    # only these sentences
  python3 -I avi.py typecast EP_DIR --run --all                      # every sentence (after the paid plan is active)

- Voice = Typecast "문정" (tc_68f9c6a72f0f04a417bb136f) · model ssfm-v31.
- mode smart (default · 1저자 11-24 밤 = V2): prompt = emotion_type "smart" + previous_text / next_text = the neighbouring
  sentences of the sheet (none at the ends) · one uniform tempo (--tempo, default 1.0) · the sheet's speed and emotion columns
  are not sent.  Why: preset switching (toneup ↔ normal ↔ tonedown) and per-sentence tempo made the voice jump in pitch between
  sentences (ep01 v1: 27 of 112 joins ≥ 2.5 semitones) · same region in smart mode = max 0.8 semitone.
- mode preset (the old way, kept for comparison): emotion = preset (EMOTION_PRESET table) · tempo = --tempo x sheet speed (0.5-2.0).
- A sentence is skipped when its wav exists AND the ledger entry has the same text · voice · model · mode · preset · tempo ·
  context hash (previous + next text) and the same file hash.  A wav without a matching ledger entry is left alone unless --force
  (so changing one sentence marks its neighbours stale too — their context changed).
- 429 / 5xx / network errors are retried (3 attempts, back-off); any other HTTP error stops that sentence only.
- EP_DIR/audio_in/typecast_ledger.json keeps, per sentence: characters, preset, tempo, status, attempts, sha256, seconds;
  and the characters sent per call (a retry that reached the server counts again).
- Internal (공개 금지) episodes are refused: their script is never sent to an external TTS.
- The API key is not handled here: the session proxy replaces the X-API-KEY header (placeholder below).
"""
import hashlib
import io
import json
import math
import os
import socket
import sys
import time
import urllib.error
import urllib.request
import wave

URL = "https://api.typecast.ai/v1/text-to-speech"
VOICE_ID = "tc_68f9c6a72f0f04a417bb136f"       # 문정 (Moonjung) · ssfm-v31 emotions: normal happy sad angry tonedown toneup whisper
MODEL = "ssfm-v31"
BASE_TEMPO = 1.0                                # 1저자 11-24 밤: 1.0 · 1.1 · 1.2 들어 보고 "1 이 가장 자연스러운데" (1.2 대체)
MODE = "smart"                                  # 1저자 11-24 밤: V0 (preset 섞음) · V1 (모두 normal) · V2 (smart) 중 "v2가 가장 좋다"
MODES = ("smart", "preset")
PRESETS = ("normal", "happy", "sad", "angry", "tonedown", "toneup", "whisper")

# script emotion column -> Typecast preset (the table is also written to EP_DIR/tts_emotion_map.md)
EMOTION_PRESET = {
    "차분": ("normal", "기본 설명 말투"),
    "정리": ("normal", "끝 정리 = 차분과 같은 꼴"),
    "가벼움": ("toneup", "장면 첫머리 · 이음말을 조금 밝게"),
    "강조": ("toneup", "숫자 · 대비 문장에 힘"),
    "궁금": ("toneup", "물음 — 끝이 평서처럼 떨어지지 않게 하려는 후보 (듣기 확인 = 1저자)"),
    "진지": ("tonedown", "한정 · 반론 · '다만' 문장"),
    "밝게": ("happy", "끝 인사"),
}
RETRY_HTTP = (429, 500, 502, 503, 504)
BACKOFF = (3.0, 8.0, 20.0)


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _wav_info(data):
    if data[:4] != b"RIFF":
        raise ValueError(f"not a RIFF wav (first bytes {data[:12]!r})")
    with wave.open(io.BytesIO(data)) as w:
        sr, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
    return dict(sr=sr, channels=ch, seconds=round(n / float(sr), 3))


def read_sheet(ep_dir):
    path = os.path.join(ep_dir, "tts_typecast.tsv")
    rows = []
    with open(path, encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")
        for line in f:
            if not line.strip():
                continue
            c = line.rstrip("\n").split("\t")
            c += [""] * (len(head) - len(c))
            sc, no, say, pause, speed, emo = c[0], c[1], c[2], c[3], c[4], c[5]
            rows.append(dict(id=f"{sc.lower()}_l{int(no):02d}", text=say, pause=float(pause), speed=float(speed or 1.0),
                             emotion=emo or "차분"))
    return rows


def guard(ep_dir, ep):
    parts = [p.lower() for p in os.path.abspath(ep_dir).split(os.sep)]
    bad = "internal" in parts or "internal" in ep.get("episode", "").lower() or "공개 금지" in ep.get("title", "") \
        or "공개금지" in ep.get("title", "")
    if bad:
        raise SystemExit("내부판 (공개 금지) 대본은 외부 TTS 로 보내지 않는다 — 거부 (EP_DIR · episode · title 검사)")


def plan(ep_dir, ep, base_tempo=BASE_TEMPO, mode=MODE):
    rows = read_sheet(ep_dir)
    say = {ln["id"]: ln["say"] for sc in ep["scenes"] for ln in sc["lines"]}
    miss = [r["id"] for r in rows if r["id"] not in say]
    diff = [r["id"] for r in rows if r["id"] in say and say[r["id"]] != r["text"]]
    if miss or diff or len(rows) != len(say):
        raise SystemExit(f"tts_typecast.tsv 와 scenes.json 이 어긋남 (없는 줄 {miss} · 다른 글 {diff} · 줄 수 {len(rows)} ↔ {len(say)})"
                         " — `avi.py tts EP_DIR` 를 다시")
    if mode not in MODES:
        raise SystemExit(f"mode 는 {MODES} 중 하나 — {mode!r}")
    for k, r in enumerate(rows):
        if r["emotion"] not in EMOTION_PRESET:
            raise SystemExit(f"{r['id']}: 감정 '{r['emotion']}' 이 대응표에 없음 ({sorted(EMOTION_PRESET)})")
        r["mode"] = mode
        r["previous_text"] = rows[k - 1]["text"] if k > 0 else None
        r["next_text"] = rows[k + 1]["text"] if k + 1 < len(rows) else None
        r["ctx"] = hashlib.sha256(((r["previous_text"] or "") + "\n" + (r["next_text"] or "")).encode("utf-8")).hexdigest()[:16]
        if mode == "smart":
            r["preset"] = None
            r["tempo"] = round(min(2.0, max(0.5, base_tempo)), 3)
        else:
            r["preset"] = EMOTION_PRESET[r["emotion"]][0]
            r["tempo"] = round(min(2.0, max(0.5, base_tempo * r["speed"])), 3)
        r["chars"] = len(r["text"])
        r["chars_nospace"] = len(r["text"].replace(" ", ""))
    return rows


def write_map(ep_dir, base_tempo=BASE_TEMPO, mode=MODE):
    head = (["- ★ 지금 방식 = **smart** (1저자 11-24 밤 V2) — `emotion_type: smart` + 앞뒤 문장 (`previous_text` · `next_text`) · "
             f"빠르기 `audio_tempo` = {base_tempo} 한 값 (문장별 빠르기 칸 · 아래 프리셋 표는 **보내지 않는다** — preset 방식 비교용)"]
            if mode == "smart" else
            [f"- 지금 방식 = preset · 빠르기 = `audio_tempo` = {base_tempo} × 대본 시트의 빠르기 칸 (0.5–2.0 으로 자름)"])
    lines = ["# 대본 감정 → Typecast 프롬프트", "",
             f"- 목소리 = Typecast 문정 (`{VOICE_ID}`) · 모델 `{MODEL}`"] + head + [
             "- preset 방식의 대응은 들어 보기 전의 가정이었다 — ep01 v1 에서 톤이 바뀌는 이음매마다 목소리 높이가 뛰었다 (이음매 112 중 2.5 반음 넘게 뜀 27 · 그중 톤 바뀜 18)", "",
             "| 대본 감정 | 프리셋 | 왜 |", "|---|---|---|"]
    lines += [f"| {k} | `{v[0]}` | {v[1]} |" for k, v in EMOTION_PRESET.items()]
    p = os.path.join(ep_dir, "tts_emotion_map.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return p


def _body(r):
    """API body for one sentence (r = plan row): smart = context prompt · preset = emotion preset."""
    if r["mode"] == "smart":
        prompt = {"emotion_type": "smart"}
        if r.get("previous_text"):
            prompt["previous_text"] = r["previous_text"]
        if r.get("next_text"):
            prompt["next_text"] = r["next_text"]
    else:
        prompt = {"emotion_type": "preset", "emotion_preset": r["preset"]}
    return {"voice_id": VOICE_ID, "text": r["text"], "model": MODEL, "prompt": prompt,
            "output": {"audio_tempo": r["tempo"], "audio_format": "wav"}}


def _call(r, timeout=120):
    body = _body(r)
    req = urllib.request.Request(URL, data=json.dumps(body, ensure_ascii=False).encode("utf-8"), method="POST",
                                 headers={"X-API-KEY": "placeholder-replaced-by-proxy", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.headers.get("Content-Type", ""), r.read()


def run(ep_dir, ep, ids=None, run_all=False, force=False, dry=True, base_tempo=BASE_TEMPO, mode=MODE, caller=_call,
        sleep=time.sleep):
    guard(ep_dir, ep)
    rows = plan(ep_dir, ep, base_tempo, mode)
    name = ep["episode"].split("_")[0]
    in_dir = os.path.join(ep_dir, "audio_in")
    os.makedirs(in_dir, exist_ok=True)
    led_path = os.path.join(in_dir, "typecast_ledger.json")
    led = json.load(open(led_path, encoding="utf-8")) if os.path.exists(led_path) else dict(lines={}, calls=[])
    if ids:
        want = set(ids)
        unknown = sorted(want - {r["id"] for r in rows})
        if unknown:
            raise SystemExit(f"없는 문장 번호: {unknown}")
        rows_sel = [r for r in rows if r["id"] in want]
    elif run_all:
        rows_sel = rows
    else:
        rows_sel = [] if not dry else rows
    todo, skip, stale = [], [], []
    for r in rows_sel:
        out = os.path.join(in_dir, f"{name}_{r['id']}.wav")
        e = led["lines"].get(r["id"])
        same = e and e.get("status") == "ok" and all(e.get(k) == v for k, v in
                                                       (("text", r["text"]), ("voice_id", VOICE_ID), ("model", MODEL),
                                                        ("mode", r["mode"]), ("preset", r["preset"]), ("tempo", r["tempo"]),
                                                        ("ctx", r["ctx"])))
        if os.path.exists(out) and same and e.get("sha256") == _sha(out) and not force:
            skip.append(r)
        elif os.path.exists(out) and not same and not force:
            stale.append(r)
        else:
            todo.append(r)
    summ = dict(sentences=len(rows), selected=len(rows_sel), to_make=len(todo), skip=len(skip), stale_untouched=len(stale),
                chars_to_send=sum(r["chars"] for r in todo), chars_to_send_nospace=sum(r["chars_nospace"] for r in todo),
                chars_all=sum(r["chars"] for r in rows), chars_all_nospace=sum(r["chars_nospace"] for r in rows),
                mode=mode, presets={p: sum(1 for r in rows if r["preset"] == p) for p in PRESETS if any(r["preset"] == p for r in rows)},
                tempo_range=[min(r["tempo"] for r in rows), max(r["tempo"] for r in rows)])
    if dry:
        summ["dry_run"] = True
        return summ, todo, stale
    made, failed = [], []
    for r in todo:
        out = os.path.join(in_dir, f"{name}_{r['id']}.wav")
        attempts, last_err = 0, None
        while attempts < len(BACKOFF):
            attempts += 1
            t0 = time.time()
            try:
                status, ctype, data = caller(r)
                led["calls"].append(dict(id=r["id"], chars=r["chars"], status=status, t=round(t0, 1)))
                info = _wav_info(data)
                if info["seconds"] < 0.3:
                    raise ValueError(f"too short ({info['seconds']} s)")
                tmp = out + ".part"
                with open(tmp, "wb") as f:
                    f.write(data)
                os.replace(tmp, out)
                led["lines"][r["id"]] = dict(text=r["text"], voice_id=VOICE_ID, model=MODEL, mode=r["mode"], preset=r["preset"],
                                             tempo=r["tempo"], ctx=r["ctx"], emotion=r["emotion"], chars=r["chars"],
                                             chars_nospace=r["chars_nospace"], status="ok", attempts=attempts,
                                             bytes=len(data), content_type=ctype, sha256=_sha(out), **info,
                                             made=time.strftime("%Y-%m-%d %H:%M:%S"),
                                             retake_rounds=0, retake_takes=0)    # a new file = a new version: counts restart
                made.append(r["id"])
                last_err = None
                break
            except urllib.error.HTTPError as ex:
                msg = ex.read()[:300].decode("utf-8", "replace") if hasattr(ex, "read") else ""
                led["calls"].append(dict(id=r["id"], chars=r["chars"], status=ex.code, t=round(t0, 1)))
                last_err = f"HTTP {ex.code} {msg}"
                if ex.code not in RETRY_HTTP:
                    break
            except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, ValueError, wave.Error) as ex:
                last_err = f"{type(ex).__name__}: {ex}"
            if attempts < len(BACKOFF):
                sleep(BACKOFF[attempts - 1])
        if last_err:
            led["lines"][r["id"]] = dict(text=r["text"], voice_id=VOICE_ID, model=MODEL, mode=r["mode"], preset=r["preset"],
                                         tempo=r["tempo"], ctx=r["ctx"], emotion=r["emotion"], chars=r["chars"], status="failed",
                                         attempts=attempts,
                                         error=last_err[:400], made=time.strftime("%Y-%m-%d %H:%M:%S"))
            failed.append(r["id"])
        with open(led_path, "w", encoding="utf-8") as f:           # after every sentence: survives an interruption
            json.dump(led, f, ensure_ascii=False, indent=1)
    sent = [c for c in led["calls"] if c.get("status") == 200]
    summ.update(made=made, failed=failed, ledger=led_path,
                chars_sent_ok_total=sum(c["chars"] for c in sent), calls_total=len(led["calls"]))
    return summ, todo, stale


def _st(f, ref):
    return 12.0 * math.log2(f / ref)


def _measure_f0(path):
    """F0 median (Hz) of one sentence file — same estimator as the audio report (audio_measure.analyse)."""
    import audio_measure
    rep_, _ = audio_measure.analyse(path)
    return rep_["f0"]["median_hz"] or None


PICK_TIE_ST = 0.5    # near-tie (semitones) between the two sides of a jump -> the side on more jump joints is retaken


def pick_sides(rows, joins_):
    """[(joint, sentence to retake)] for every joint flagged as a pitch jump: the sentence that sits further off its own
    neighbours (geometric mean of the neighbours' F0 medians).  Near-tie (< PICK_TIE_ST) -> the sentence that is on more
    jump joints (11-25: the first / last sentence has one neighbour, so its distance equals the jump and tied with the real
    outlier next to it).  rows = audio_qc rows (id · f0_med) · joins_ = audio_qc joins."""
    f = {r["id"]: r.get("f0_med") for r in rows}
    order = [r["id"] for r in rows]

    def dev(i):
        k = order.index(i)
        nb = [f[order[j]] for j in (k - 1, k + 1) if 0 <= j < len(order) and f.get(order[j])]
        if not f.get(i) or not nb:
            return -1.0
        return abs(_st(f[i], math.exp(sum(math.log(x) for x in nb) / len(nb))))
    njump = {}
    for j in joins_:
        if j.get("jump"):
            for s in (j["a"], j["b"]):
                njump[s] = njump.get(s, 0) + 1
    out = []
    for j in joins_:
        if not j.get("jump"):
            continue
        da, db, na, nb_ = dev(j["a"]), dev(j["b"]), njump.get(j["a"], 0), njump.get(j["b"], 0)
        if abs(da - db) < PICK_TIE_ST and na != nb_:
            t = j["a"] if na > nb_ else j["b"]
        else:
            t = j["a"] if da >= db else j["b"]
        out.append((j, t))
    return out


def pick_targets(rows, joins_):
    """The sentences to retake (each once, in joint order) — see pick_sides."""
    out = []
    for _, t in pick_sides(rows, joins_):
        if t not in out:
            out.append(t)
    return out


RETAKE_SESSION_GAP_S = 30.0      # old ledgers (no counter): retake calls more than 30 s apart = separate rounds


def retake_counts(led, i):
    """(rounds, new takes) of retakes for the CURRENT file of sentence i — run() writes 0 / 0 for every new file, retake()
    adds one round per call that made at least one take.  Old ledgers (before 11-25) have no counter: the take calls that
    came after the file was made (`made`, local time of the same machine) are grouped into rounds (gap > 30 s)."""
    e = (led.get("lines") or {}).get(i) or {}
    if "retake_rounds" in e:
        return int(e.get("retake_rounds") or 0), int(e.get("retake_takes") or 0)
    try:
        made = time.mktime(time.strptime(e["made"], "%Y-%m-%d %H:%M:%S"))
    except (KeyError, TypeError, ValueError):
        return 0, 0
    ts = sorted(c["t"] for c in led.get("calls", []) if c.get("id") == i and "take" in c and c.get("status") == 200
                and isinstance(c.get("t"), (int, float)) and c["t"] >= made)
    rounds, last = 0, None
    for t in ts:
        if last is None or t - last > RETAKE_SESSION_GAP_S:
            rounds += 1
        last = t
    return rounds, len(ts)


def retake_rounds(led, i):
    return retake_counts(led, i)[0]


def retake(ep_dir, ep, ids, takes=2, base_tempo=BASE_TEMPO, mode=MODE, caller=_call, measure=None, sleep=time.sleep):
    """Make `takes` more takes of each sentence in ids (same text · context · tempo) and keep the one whose F0 median is
    closest (semitones) to the geometric mean of its neighbours' F0 medians.  The first file is kept as takes/<id>_t0.wav,
    new takes continue the numbering · the ledger line follows the kept file (sha256 · take) · chars are counted per call."""
    import shutil
    guard(ep_dir, ep)
    measure = measure or _measure_f0
    rows = plan(ep_dir, ep, base_tempo, mode)
    by = {r["id"]: (k, r) for k, r in enumerate(rows)}
    unknown = [i for i in ids if i not in by]
    if unknown:
        raise SystemExit(f"없는 문장 번호: {unknown}")
    name = ep["episode"].split("_")[0]
    in_dir = os.path.join(ep_dir, "audio_in")
    tk_dir = os.path.join(in_dir, "takes")
    os.makedirs(tk_dir, exist_ok=True)
    led_path = os.path.join(in_dir, "typecast_ledger.json")
    led = json.load(open(led_path, encoding="utf-8")) if os.path.exists(led_path) else dict(lines={}, calls=[])

    def path(i):
        return os.path.join(in_dir, f"{name}_{i}.wav")
    res = []
    for i in ids:
        k, r = by[i]
        main = path(i)
        if not os.path.exists(main):
            res.append(dict(id=i, error="원래 파일 없음 — 먼저 --run")); continue
        nb = [rows[j]["id"] for j in (k - 1, k + 1) if 0 <= j < len(rows) and os.path.exists(path(rows[j]["id"]))]
        f_nb = [x for x in (measure(path(n)) for n in nb) if x]
        if not f_nb:
            res.append(dict(id=i, error="이웃 F0 를 못 쟀다")); continue
        ref = math.exp(sum(math.log(x) for x in f_nb) / len(f_nb))
        t0 = os.path.join(tk_dir, f"{i}_t0.wav")
        if not os.path.exists(t0):
            shutil.copy2(main, t0)
        have = [int(fn.rsplit("_t", 1)[1][:-4]) for fn in os.listdir(tk_dir) if fn.startswith(f"{i}_t") and fn.endswith(".wav")]
        nxt = max(have) + 1 if have else 1
        rounds0, takes0 = retake_counts(led, i)                   # before this round's calls enter the ledger
        cands = [("cur", main, measure(main))]
        err = None
        for t in range(nxt, nxt + takes):
            data = None
            for attempt in range(len(BACKOFF)):
                t_call = time.time()
                try:
                    status, ctype, data = caller(r)
                    led["calls"].append(dict(id=i, chars=r["chars"], status=status, t=round(t_call, 1), take=t))
                    _wav_info(data)
                    break
                except urllib.error.HTTPError as ex:
                    led["calls"].append(dict(id=i, chars=r["chars"], status=ex.code, t=round(t_call, 1), take=t))
                    err, data = f"HTTP {ex.code}", None
                    if ex.code not in RETRY_HTTP:
                        break
                except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, ValueError, wave.Error) as ex:
                    err, data = f"{type(ex).__name__}: {ex}", None
                sleep(BACKOFF[attempt])
            if data is None:
                break
            tp = os.path.join(tk_dir, f"{i}_t{t}.wav")
            with open(tp + ".part", "wb") as fh:
                fh.write(data)
            os.replace(tp + ".part", tp)
            cands.append((t, tp, measure(tp)))
        best = min(cands, key=lambda c: abs(_st(c[2], ref)) if c[2] else float("inf"))
        if best[0] != "cur":
            shutil.copy2(best[1], main + ".part")
            os.replace(main + ".part", main)
        e = led["lines"].setdefault(i, {})
        n_new = len(cands) - 1
        e.update(sha256=_sha(main), take=(e.get("take", 0) if best[0] == "cur" else best[0]), f0_hz=best[2],
                 f0_neighbours_hz=round(ref, 1), retaken=time.strftime("%Y-%m-%d %H:%M:%S"),
                 retake_rounds=rounds0 + (1 if n_new else 0), retake_takes=takes0 + n_new)
        with open(led_path, "w", encoding="utf-8") as fh:
            json.dump(led, fh, ensure_ascii=False, indent=1)
        res.append(dict(id=i, chosen=(e["take"] if best[0] == "cur" else best[0]), kept_current=best[0] == "cur",
                        ref_hz=round(ref, 1), dev_before_st=round(_st(cands[0][2], ref), 2) if cands[0][2] else None,
                        dev_after_st=round(_st(best[2], ref), 2) if best[2] else None,
                        takes_hz=[round(c[2], 1) if c[2] else None for c in cands], error=err))
    return res


def selftest():
    """Offline test with a fake API: retry, skip, stale-file protection, internal guard, ledger, character count,
    smart mode (1저자 11-24 밤 = V2: emotion_type smart + previous/next text · uniform tempo) and the old preset mode."""
    import shutil
    import struct
    import tempfile
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "selftest")
    os.makedirs(base, exist_ok=True)
    d = tempfile.mkdtemp(prefix="typecast_", dir=base)          # removed at the end (fake API only)
    t1, t2 = "첫 문장입니다.", "두 번째 문장이죠?"

    def write(a, b):
        ep_ = dict(episode="ep98_test", title="시험", scenes=[dict(id="s01", lines=[
            dict(id="s01_l01", say=a, text=a), dict(id="s01_l02", say=b, text=b)])])
        with open(os.path.join(d, "tts_typecast.tsv"), "w", encoding="utf-8") as f:
            f.write("장면 번호\t문장 번호\t문장 (읽는 꼴)\t뒤 쉼 (초)\t빠르기 (1.0 기준 배수)\t감정\t강조 낱말\t메모\n")
            f.write(f"S01\t01\t{a}\t0.45\t1.00\t차분\t\t\nS01\t02\t{b}\t0.85\t0.97\t궁금\t\t\n")
        return ep_
    ep = write(t1, t2)

    def fake_wav(sec=1.0, sr=32000):
        buf = io.BytesIO()
        with wave.open(buf, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes(struct.pack("<h", 0) * int(sec * sr))
        return buf.getvalue()

    calls = []

    def flaky(req):
        calls.append(dict(req))
        if len(calls) == 1:
            raise urllib.error.HTTPError(URL, 503, "busy", {}, io.BytesIO(b"busy"))
        return 200, "audio/wav", fake_wav()

    ok = []

    def check(name_, fn):
        try:
            ok.append((name_, bool(fn())))
        except Exception as ex:                                   # noqa: BLE001 — a crash is a FAIL, not an abort
            ok.append((f"{name_}  [{type(ex).__name__}: {ex}]", False))
    n1, n2 = len(t1), len(t2)
    st = {}
    check("dry run makes no call", lambda: (st.__setitem__("s1", run(d, ep, dry=True)[0]) or True)
          and not calls and st["s1"]["to_make"] == 2 and st["s1"]["chars_all"] == n1 + n2)
    check("503 retried then both made (default = smart)",
          lambda: (st.__setitem__("s2", run(d, ep, ids=["s01_l01", "s01_l02"], dry=False, caller=flaky, sleep=lambda s: None)[0])
                   or True) and st["s2"]["made"] == ["s01_l01", "s01_l02"] and len(calls) == 3)
    check("★ smart prompt: previous_text / next_text = neighbours (none at the ends)",
          lambda: calls[1]["mode"] == "smart" and calls[1].get("previous_text") is None and calls[1]["next_text"] == t2
          and calls[2]["previous_text"] == t1 and calls[2].get("next_text") is None and calls[2]["preset"] is None
          and _body(calls[2])["prompt"] == {"emotion_type": "smart", "previous_text": t1})
    check("★ smart tempo = base (sheet speed column ignored)", lambda: calls[1]["tempo"] == BASE_TEMPO == 1.0
          and calls[2]["tempo"] == 1.0)
    check("second run skips both", lambda: (st.__setitem__("s3", run(d, ep, run_all=True, dry=False, caller=flaky,
                                                                       sleep=lambda s: None)[0]) or True)
          and st["s3"]["skip"] == 2 and st["s3"]["made"] == [] and len(calls) == 3)
    with open(os.path.join(d, "audio_in", "ep98_s01_l01.wav"), "ab") as f:
        f.write(b"x")                                                # file no longer matches the ledger hash
    check("hash change -> remade", lambda: run(d, ep, run_all=True, dry=False, caller=flaky, sleep=lambda s: None)[0]["made"]
          == ["s01_l01"])
    ep2 = write("첫 문장을 바꿨습니다.", t2)
    check("★ neighbour text changed -> both lines stale (context in the ledger key), none silently skipped",
          lambda: sorted(r["id"] for r in run(d, ep2, run_all=True, dry=True)[2]) == ["s01_l01", "s01_l02"])
    check("★ … and --force remakes both", lambda: run(d, ep2, run_all=True, dry=False, force=True, caller=flaky,
                                                       sleep=lambda s: None)[0]["made"] == ["s01_l01", "s01_l02"])
    ep = write(t1, t2)
    check("old preset mode kept: toneup · tempo 1.2 x speed · emotion_type preset",
          lambda: run(d, ep, ids=["s01_l02"], dry=False, force=True, mode="preset", base_tempo=1.2, caller=flaky,
                      sleep=lambda s: None)[0]["made"] == ["s01_l02"]
          and calls[-1]["tempo"] == round(1.2 * 0.97, 3) and calls[-1]["preset"] == "toneup"
          and _body(calls[-1])["prompt"] == {"emotion_type": "preset", "emotion_preset": "toneup"})
    try:
        run(os.path.join(d, "internal"), dict(ep, episode="ep98internal"), dry=True)
        ok.append(("internal refused", False))
    except SystemExit:
        ok.append(("internal refused", True))
    check("ledger counts chars per call", lambda: sum(c["chars"] for c in json.load(open(
        os.path.join(d, "audio_in", "typecast_ledger.json"), encoding="utf-8"))["calls"]) == sum(len(c["text"]) for c in calls))
    # retake (1저자 11-24 밤 "그런 부분들이 없게 전체적으로") — 높이가 뛴 문장을 몇 번 더 만들어 이웃과 가장 맞는 판을 고른다
    ep3 = dict(episode="ep98_test", title="시험", scenes=[dict(id="s01", lines=[
        dict(id=f"s01_l0{k}", say=t_, text=t_) for k, t_ in ((1, "가 문장입니다."), (2, "나 문장이에요."), (3, "다 문장이죠."))])])
    with open(os.path.join(d, "tts_typecast.tsv"), "w", encoding="utf-8") as f:
        f.write("장면 번호\t문장 번호\t문장 (읽는 꼴)\t뒤 쉼 (초)\t빠르기 (1.0 기준 배수)\t감정\t강조 낱말\t메모\n")
        f.write("S01\t01\t가 문장입니다.\t0.45\t1.00\t차분\t\t\nS01\t02\t나 문장이에요.\t0.45\t1.00\t차분\t\t\n"
                "S01\t03\t다 문장이죠.\t0.45\t1.00\t차분\t\t\n")
    f0_of = {}                                                    # file bytes -> fake F0 (Hz) = what measure() returns
    queue = [200.0, 290.0, 201.0, 280.0, 205.0]                   # l01 · l02 (high) · l03 · then the two retakes of l02

    def tone_api(req):
        calls.append(dict(req))
        hz = queue.pop(0)
        data = fake_wav(1.0 + hz / 1e4)                           # distinct bytes per take
        f0_of[hashlib.sha256(data).hexdigest()] = hz
        return 200, "audio/wav", data

    def measure(path):
        return f0_of[_sha(path)]
    check("retake: three sentences made (l02 = 290 Hz between 200 · 201)",
          lambda: run(d, ep3, run_all=True, dry=False, force=True, caller=tone_api, sleep=lambda s: None)[0]["made"]
          == ["s01_l01", "s01_l02", "s01_l03"])
    n_calls = len(calls)
    st["rt"] = None
    check("★ retake: picks the take closest to the neighbours (205 Hz), replaces the file, ledger sha follows",
          lambda: (st.__setitem__("rt", retake(d, ep3, ["s01_l02"], takes=2, caller=tone_api, measure=measure,
                                                sleep=lambda s: None)) or True)
          and st["rt"][0]["chosen"] == 2 and abs(st["rt"][0]["dev_after_st"]) < 0.6 and st["rt"][0]["dev_before_st"] > 6
          and measure(os.path.join(d, "audio_in", "ep98_s01_l02.wav")) == 205.0
          and json.load(open(os.path.join(d, "audio_in", "typecast_ledger.json"), encoding="utf-8"))["lines"]["s01_l02"]["sha256"]
          == _sha(os.path.join(d, "audio_in", "ep98_s01_l02.wav")))
    check("★ retake: same text · smart context as the original (previous / next = neighbours)",
          lambda: len(calls) == n_calls + 2 and calls[-1]["text"] == "나 문장이에요." and calls[-1]["previous_text"] == "가 문장입니다."
          and calls[-1]["next_text"] == "다 문장이죠." and calls[-1]["mode"] == "smart")
    check("★ retake: the kept file is not remade by the next run (ledger still matches)",
          lambda: run(d, ep3, run_all=True, dry=True)[0]["to_make"] == 0)
    check("★ retake: takes kept beside (audio_in/takes/) · chars counted per call",
          lambda: sorted(os.listdir(os.path.join(d, "audio_in", "takes"))) == ["s01_l02_t0.wav", "s01_l02_t1.wav", "s01_l02_t2.wav"]
          and sum(c["chars"] for c in json.load(open(os.path.join(d, "audio_in", "typecast_ledger.json"),
                                                      encoding="utf-8"))["calls"]) == sum(len(c["text"]) for c in calls))
    check("★ retake: pick_targets = the sentence that sits off its neighbours (not the steady one)",
          lambda: pick_targets([dict(id="x1", f0_med=200.0), dict(id="x2", f0_med=202.0), dict(id="x3", f0_med=290.0),
                                dict(id="x4", f0_med=205.0)], [dict(a="x2", b="x3", jump=True), dict(a="x3", b="x4", jump=True)])
          == ["x3"])
    check("★ pick_targets 동률 (첫 문장은 이웃이 하나라 거리가 뜀과 같다): 뜀 이음매가 더 많은 문장 = 가운데 문장",
          lambda: pick_targets([dict(id="y1", f0_med=200.0), dict(id="y2", f0_med=150.0), dict(id="y3", f0_med=198.0),
                                dict(id="y4", f0_med=200.0)], [dict(a="y1", b="y2", jump=True), dict(a="y2", b="y3", jump=True)])
          == ["y2"]
          and pick_targets([dict(id="z1", f0_med=150.0), dict(id="z2", f0_med=200.0), dict(id="z3", f0_med=280.0),
                            dict(id="z4", f0_med=280.0)], [dict(a="z1", b="z2", jump=True), dict(a="z2", b="z3", jump=True)])
          == ["z1", "z3"])
    check("★ retake: 원장에 다시 찍기 횟수 (판 하나 = retake_rounds 1 · retake_takes 2 · 새로 만든 줄 = 0) — 끝말 후보 판단용",
          lambda: (lambda led_: led_["lines"]["s01_l02"]["retake_rounds"] == 1 and led_["lines"]["s01_l02"]["retake_takes"] == 2
                   and retake_rounds(led_, "s01_l02") == 1 and led_["lines"]["s01_l01"]["retake_rounds"] == 0)(
              json.load(open(os.path.join(d, "audio_in", "typecast_ledger.json"), encoding="utf-8"))))
    for name_, good in ok:
        print(("PASS " if good else "FAIL ") + name_)
    shutil.rmtree(d, ignore_errors=True)
    return all(g for _, g in ok)


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ep", nargs="?")
    ap.add_argument("--run", action="store_true", help="call the API (default = dry run)")
    ap.add_argument("--lines", help="comma-separated line ids, e.g. s01_l01,s01_l08")
    ap.add_argument("--all", action="store_true", help="every sentence of the sheet")
    ap.add_argument("--force", action="store_true", help="also remake wavs whose ledger entry does not match")
    ap.add_argument("--tempo", type=float, default=BASE_TEMPO, help=f"base audio_tempo (default {BASE_TEMPO})")
    ap.add_argument("--mode", choices=MODES, default=MODE, help=f"prompt mode (default {MODE} = context-aware · preset = old)")
    ap.add_argument("--retake", help="comma-separated ids: make more takes, keep the one closest in pitch to its neighbours")
    ap.add_argument("--retake-jumps", action="store_true", help="retake the sentences behind the pitch jumps in audio/audio_qc.json")
    ap.add_argument("--takes", type=int, default=2, help="new takes per retaken sentence (default 2)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        sys.exit(0 if selftest() else 1)
    if not a.ep:
        ap.error("EP_DIR required")
    if a.run and not (a.lines or a.all or a.retake or a.retake_jumps):
        ap.error("--run needs --lines … or --all (no accidental full run)")
    ep = json.load(open(os.path.join(a.ep, "scenes.json"), encoding="utf-8"))
    guard(a.ep, ep)
    if a.retake or a.retake_jumps:
        if a.retake_jumps:
            q = json.load(open(os.path.join(a.ep, "audio", "audio_qc.json"), encoding="utf-8"))
            ids = pick_targets(q["rows"], q.get("joins", []))
        else:
            ids = [x.strip() for x in a.retake.split(",") if x.strip()]
        print("retake:", ", ".join(ids) or "(없음)", f"· 판 {a.takes} 개씩 · 보낼 글자 어림",
              sum(len(r["text"]) for r in plan(a.ep, ep, a.tempo, a.mode) if r["id"] in ids) * a.takes)
        if not a.run:
            print("dry run — API 호출 없음 (--run 을 붙이면 만든다)"); sys.exit(0)
        out = retake(a.ep, ep, ids, takes=a.takes, base_tempo=a.tempo, mode=a.mode)
        print(json.dumps(out, ensure_ascii=False, indent=1))
        sys.exit(1 if any(x.get("error") for x in out) else 0)
    print("map:", write_map(a.ep, a.tempo, a.mode))
    ids = [x.strip() for x in a.lines.split(",")] if a.lines else None
    summ, todo, stale = run(a.ep, ep, ids=ids, run_all=a.all, force=a.force, dry=not a.run, base_tempo=a.tempo, mode=a.mode)
    if stale:
        print("⚠ 원장과 맞지 않는 기존 wav (건드리지 않음 · 다시 만들려면 --force):", ", ".join(r["id"] for r in stale))
    print(json.dumps(summ, ensure_ascii=False, indent=1))
    if not a.run:
        print("dry run — API 호출 없음.  만들 줄:", len(todo), "· 보낼 글자", summ["chars_to_send"],
              f"(공백 뺀 {summ['chars_to_send_nospace']})")
    sys.exit(1 if summ.get("failed") else 0)


if __name__ == "__main__":
    main()
