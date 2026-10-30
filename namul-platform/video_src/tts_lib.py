import re, wave
import numpy as np
import sherpa_onnx
M = "/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/a9086aab-2880-555b-a3e5-137ced4672cf/scratchpad/tts/models"
_tts = _asr = None
def tts():
    global _tts
    if _tts is None:
        v = f"{M}/vits-mimic3-ko_KO-kss_low"
        _tts = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                model=f"{v}/ko_KO-kss_low.onnx", lexicon="", tokens=f"{v}/tokens.txt", data_dir=f"{v}/espeak-ng-data"),
                provider="cpu", num_threads=4), max_num_sentences=1))
    return _tts
def asr():
    global _asr
    if _asr is None:
        d = f"{M}/sherpa-onnx-zipformer-korean-2024-06-24"
        _asr = sherpa_onnx.OfflineRecognizer.from_transducer(
            encoder=f"{d}/encoder-epoch-99-avg-1.int8.onnx", decoder=f"{d}/decoder-epoch-99-avg-1.onnx",
            joiner=f"{d}/joiner-epoch-99-avg-1.int8.onnx", tokens=f"{d}/tokens.txt", num_threads=4, decoding_method="greedy_search")
    return _asr
def synth(text, speed=1.0):
    a = tts().generate(text, sid=0, speed=speed)
    return np.asarray(a.samples, dtype=np.float32), a.sample_rate
def transcribe(x, sr):
    s = asr().create_stream(); s.accept_waveform(sr, x); asr().decode_stream(s); return s.result.text
def _clean(t): return re.sub(r"[^가-힣a-zA-Z0-9]", "", t)
def cer(ref, hyp):
    r, h = _clean(ref), _clean(hyp)
    prev = list(range(len(h) + 1))
    for i, rc in enumerate(r, 1):
        cur = [i] + [0] * len(h)
        for j, hc in enumerate(h, 1):
            cur[j] = min(prev[j] + 1, cur[j-1] + 1, prev[j-1] + (rc != hc))
        prev = cur
    return prev[-1] / max(1, len(r))
def save_wav(path, x, sr):
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
