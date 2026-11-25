#!/usr/bin/env python3
"""Local TTS with MeloTTS-Korean (MIT · source github.com/myshell-ai/MeloTTS @ 209145371cff · INTERNAL test only).

내부판 기본 로컬 TTS (AVI 스킬 S6 · 1저자 11-25 청취 — 빠르기 1.2 · 문장 통째 합성 `--speed 1.2 --no-split` · 화자 KR 하나 · MIT) ·
예비 = XTTS-v2 (`avi_xtts.py` · CPML).  ⚠ 한국어 BERT (bert-kor-base) 는 라이선스 표기가 없다 → 내부판 전용 (공개판 음성에 쓰지 않는다).
venv · Hugging Face 캐시 · NLTK 자료 · MeloTTS 소스는 리포 밖 (작업 폴더) — 자리 = 환경 변수 HF_HOME · NLTK_DATA · AVI_MELO_SRC ·
없으면 이 tools/ 폴더 옆의 hf_cache_melo · nltk_data_melo · src/MeloTTS.  torch · melo 는 함수 안에서만 부른다 (모듈 첫머리 = numpy ·
avi_xtts (metrics) 만 · 리포 게이트는 torch 없이 돈다).

Run with the MeloTTS venv (NOT system python, NOT venv_tts · the venv lives outside the repo, e.g. the work folder's venv_melo):
  <MeloTTS venv>/bin/python -I avi_melo.py inspect-ckpt
  <MeloTTS venv>/bin/python -I avi_melo.py sample --out FILE.wav --text "…" --text "…" [--pause 0.45] [--speed 1.0] [--seed 7]
  <MeloTTS venv>/bin/python -I avi_melo.py lines EP_DIR --out DIR --only n1_l01,n3_l03 [--speed 1.0] [--seed 7]

Rules (1저자 · 본 세션 11-25): text never leaves this machine · Hugging Face cache = pinned revisions, offline at run time ·
CPU threads <= 2 · fixed seed per call · torch.load stays weights_only (no pickle execution — allow-list only, never False here).
The other six language front ends (and their BERT tokenizers) are replaced by stubs before MeloTTS is imported, so MeCab-ja /
unidic / g2p_en / gruut / pypinyin / jieba and five extra BERT downloads are never touched; a stub raises if it is ever called.
Metrics = avi_xtts.metrics (the same code that measured the XTTS takes) · output = 44.1 kHz PCM 16 (the model's own rate).
"""
import argparse
import hashlib
import json
import os
import pickletools
import sys
import time
import types
import zipfile

THREADS = 2
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)                             # 작업 폴더 꼴 (tools/ 의 위) — venv · 캐시 · 소스는 리포 밖
for k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ.setdefault(k, str(THREADS))
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("HF_HOME", os.path.join(WORK, "hf_cache_melo"))
os.environ.setdefault("HF_HUB_OFFLINE", "1")             # never fetch anything at run time
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("NLTK_DATA", os.path.join(WORK, "nltk_data_melo"))

import numpy as np  # noqa: E402

SRC = os.environ.get("AVI_MELO_SRC") or os.path.join(WORK, "src", "MeloTTS")
sys.path.insert(0, HERE)
sys.path.insert(1, SRC)
import avi_xtts as X  # noqa: E402  (metrics · lufs only — no XTTS model is loaded)

REPO, REV = "myshell-ai/MeloTTS-Korean", "0207e5adfc90129a51b6b03d89be6d84360ed323"
CKPT_SHA256 = "48e3ff3fd0b5348e095f0468e60ae727507564100f58142ef3a922ead6e0a4d0"
STUBBED = ("chinese", "japanese", "english", "chinese_mix", "french", "spanish", "english_bert", "spanish_bert", "french_bert")


def ckpt_path():
    return os.path.join(os.environ["HF_HOME"], "hub", "models--myshell-ai--MeloTTS-Korean", "snapshots", REV, "checkpoint.pth")


def install_stubs():
    import melo.text as mt                       # package init = symbols only
    for name in STUBBED:
        full = "melo.text." + name
        m = types.ModuleType(full)

        def _no(*a, _n=full, **k):
            raise NotImplementedError(f"{_n} is stubbed in the Korean-only driver (avi_melo.py)")
        m.text_normalize = m.g2p = m.get_bert_feature = _no
        m.__doc__ = "stub (avi_melo.py) — this language is not loaded"
        sys.modules[full] = m
        setattr(mt, name, m)


def load_tts():
    import torch
    torch.set_num_threads(THREADS)
    install_stubs()
    from melo.api import TTS
    t = time.time()
    tts = TTS(language="KR", device="cpu")       # use_hf=True → offline cache (pinned revision) · torch.load default = weights_only
    return tts, round(time.time() - t, 1)


def synth(tts, text, seed, speed, split=True):
    """split=True = MeloTTS as shipped (tts_to_file cuts the sentence at every comma / stop into separate model calls,
    each followed by the model's own trailing silence + 0.05 s / speed) · split=False = the same inference code
    (utils.get_text_for_tts_infer → model.infer, same noise settings) on the whole sentence in one call."""
    import torch
    torch.manual_seed(seed)
    spk = tts.hps.data.spk2id["KR"]
    sr = int(tts.hps.data.sampling_rate)
    if split:
        x = tts.tts_to_file(text, spk, output_path=None, speed=speed, quiet=True)
        return np.asarray(x, np.float32).reshape(-1), sr
    from melo import utils
    bert, ja_bert, phones, tones, lang_ids = utils.get_text_for_tts_infer(text, tts.language, tts.hps, tts.device, tts.symbol_to_id)
    with torch.no_grad():
        audio = tts.model.infer(phones.unsqueeze(0), torch.LongTensor([phones.size(0)]), torch.LongTensor([spk]),
                                tones.unsqueeze(0), lang_ids.unsqueeze(0), bert.unsqueeze(0), ja_bert.unsqueeze(0),
                                sdp_ratio=0.2, noise_scale=0.6, noise_scale_w=0.8, length_scale=1.0 / speed)[0][0, 0]
    x = audio.data.cpu().float().numpy().reshape(-1)
    return np.concatenate([x, np.zeros(int(sr * 0.05 / speed), np.float32)]).astype(np.float32), sr


def write_wav(path, x, sr):
    import soundfile as sf
    sf.write(path, np.clip(x, -1, 1), sr, subtype="PCM_16")


def inspect_ckpt():
    """Globals referenced by checkpoint.pth's pickle (read with pickletools — nothing is unpickled or executed)."""
    p = ckpt_path()
    z = zipfile.ZipFile(p)
    pk = [n for n in z.namelist() if n.endswith("data.pkl")]
    data = z.read(pk[0])
    found, strs = set(), []
    for op, arg, _ in pickletools.genops(data):
        if op.name in ("SHORT_BINUNICODE", "BINUNICODE", "UNICODE", "BINUNICODE8"):
            strs.append(arg)
        elif op.name == "GLOBAL":
            found.add(arg.replace(" ", "."))
        elif op.name == "STACK_GLOBAL" and len(strs) >= 2:
            found.add(f"{strs[-2]}.{strs[-1]}")
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return dict(file=p, sha256_ok=h.hexdigest() == CKPT_SHA256, pickle=pk[0], globals=sorted(found))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("inspect-ckpt")
    a2 = sub.add_parser("sample")
    a2.add_argument("--out", required=True)
    a2.add_argument("--text", action="append", required=True)
    a2.add_argument("--pause", type=float, default=0.45)
    a2.add_argument("--seed", type=int, default=7)
    a2.add_argument("--speed", type=float, default=1.0)
    a2.add_argument("--no-split", action="store_true", help="whole sentence in one model call (default = MeloTTS splits at commas)")
    a4 = sub.add_parser("lines", help="synthesize chosen lines of an episode (scenes.json 'say') -> OUT/<episode>_<line>.wav + lines.json")
    a4.add_argument("ep_dir")
    a4.add_argument("--out", required=True)
    a4.add_argument("--only", required=True, help="comma list of line ids")
    a4.add_argument("--speed", type=float, default=1.0, help="base speed (× each line's own speed)")
    a4.add_argument("--seed", type=int, default=7)
    a4.add_argument("--no-split", action="store_true", help="whole sentence in one model call (default = MeloTTS splits at commas)")
    a = ap.parse_args(argv)
    if a.cmd == "inspect-ckpt":
        print(json.dumps(inspect_ckpt(), ensure_ascii=False, indent=1))
        return 0
    if not (0.5 <= a.speed <= 2.0):
        print("speed out of 0.5–2.0", file=sys.stderr)
        return 2
    try:
        tts, load_s = load_tts()
    except Exception as e:                           # R2: report, never fall back to weights_only=False here
        print(json.dumps(dict(error=type(e).__name__, message=str(e)[:2000], ckpt=inspect_ckpt()), ensure_ascii=False, indent=1))
        return 3
    info = dict(model=REPO, revision=REV, ckpt_sha256=CKPT_SHA256, source_commit="209145371cff8fc3bd60d7be902ea69cbdb7965a",
                speaker="KR (MeloTTS-Korean · single speaker)", threads=THREADS, load_s=load_s, stubbed=list(STUBBED))
    if a.cmd == "sample":
        parts, rows, pos, sr = [], [], 0, None
        for k, txt in enumerate(a.text):
            t = time.time()
            x, sr = synth(tts, txt, seed=a.seed + k, speed=a.speed, split=not a.no_split)
            rows.append(dict(text_no=k + 1, start_s=round(pos / sr, 3), end_s=round((pos + len(x)) / sr, 3),
                             synth_s=round(time.time() - t, 1), **X.metrics(x, sr, txt)))
            parts.append(x)
            pos += len(x)
            if k < len(a.text) - 1:
                parts.append(np.zeros(int(a.pause * sr), np.float32))
                pos += int(a.pause * sr)
        y = np.concatenate(parts)
        write_wav(a.out, y, sr)
        meta = dict(speaker=info["speaker"], seed=a.seed, speed=a.speed, split=not a.no_split, pause=a.pause, texts=a.text, sr=sr,
                    dur_s=round(len(y) / sr, 2), rows=rows, **{k: v for k, v in info.items() if k != "speaker"})
        json.dump(meta, open(os.path.splitext(a.out)[0] + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(json.dumps(meta, ensure_ascii=False))
        return 0
    if a.cmd == "lines":
        ep = json.load(open(os.path.join(a.ep_dir, "scenes.json"), encoding="utf-8"))
        os.makedirs(a.out, exist_ok=True)
        only = {x.strip() for x in a.only.split(",") if x.strip()}
        ledger_p = os.path.join(a.out, "lines.json")
        led = json.load(open(ledger_p, encoding="utf-8")) if os.path.exists(ledger_p) else dict(lines={})
        led.update(tool="tools/avi_melo.py lines", base_speed=a.speed, split=not a.no_split, episode=ep.get("episode"), **info)
        for sc in ep["scenes"]:
            for ln in sc["lines"]:
                if ln["id"] not in only:
                    continue
                sp = round(a.speed * float(ln.get("speed", 1.0) or 1.0), 4)
                seed = a.seed + int(hashlib.sha256(ln["say"].encode("utf-8")).hexdigest()[:6], 16) % 1000
                t = time.time()
                x, sr = synth(tts, ln["say"], seed=seed, speed=sp, split=not a.no_split)
                fn = f"{ep.get('episode', 'ep').split('_')[0]}_{ln['id']}.wav"
                write_wav(os.path.join(a.out, fn), x, sr)
                m = X.metrics(x, sr, ln["say"])
                led["lines"][ln["id"]] = dict(file=fn, say=ln["say"], say_sha256=hashlib.sha256(ln["say"].encode("utf-8")).hexdigest(),
                                              seed=seed, speed=sp, sr=sr, synth_s=round(time.time() - t, 1),
                                              wav_sha256=hashlib.sha256(open(os.path.join(a.out, fn), "rb").read()).hexdigest(), **m)
                json.dump(led, open(ledger_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                print(json.dumps(dict(id=ln["id"], speed=sp, speech_s=m.get("speech_s"), rate=m.get("syl_rate"),
                                      rough=m.get("rough_db"), gap=m.get("gap_max")), ensure_ascii=False), flush=True)
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
