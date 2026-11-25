#!/usr/bin/env python3
"""pc_actions.py — PhotoCraft 작업 묶음 도우미 (표준 라이브러리만 · 초안 · 2026-11-25).

작업 하나 = 폴더 하나:  <job>/in (원본 사본 · 읽기 전용)  <job>/actions (action JSON)
                        <job>/out (결과)  <job>/record (실행 기록)  <job>/.pc_config (빈 설정 폴더)

하위 명령
  init    JOB --src FILE [--to SUB] [--source-note TEXT]
                                                  원본을 JOB/in/[SUB/] 에 복사 (원본은 건드리지 않음) + sha256
                                                  (JOB = 오래 쓰는 작업 공간 · SUB = 작업 하나 — MCP 는 JOB 에 한 번 등록)
  check   ACTIONS --mode data|figure              허용 목록 검사만 (PhotoCraft 를 부르지 않음)
  run     JOB ACTIONS --in NAME --out NAME --mode data|figure --bin PHOTOCRAFT_CLI
          [--quality 1-100] [--note TEXT] [--source-ref TEXT] [--ref-png NAME] [--allow-font-fallback]
          [--dry-run]                             검사 → photocraft-cli run → 기록 · 검사 (meta · pointop)
  verify  RECORD.json --bin PHOTOCRAFT_CLI        같은 action 으로 다시 만들어 결과가 같은지 (재현성)
  mcp-cmd JOB --bin PHOTOCRAFT_CLI                claude mcp add 명령을 *출력만* (등록은 1저자)

규칙 (우리 연구실):
  data   = SEM · 현미경 · 시뮬레이션 렌더 · 그래프.  전체에 같은 선형 조정 (레벨 감마 1 · 밝기/대비 legacy)
           · 자르기 · 크기 (고정 커널) · 여백 · 90° 회전 · 비트 깊이만.  선택 영역 · 국소 편집 · 채우기 ·
           지우기 · 복제 · 날카롭게 · 곡선 · 생성형 채우기 (contentAware) 금지.
  figure = 문헌 그림 크롭 · 발표 그림 · 썸네일 · 영상 장면.  data 에 흑백 · 곡선 · 선명 · 글자 · 뒤집기 등을 더함.
  두 경우 모두: 파일 경로를 담는 명령 · 매개변수 (path · file · dir · profile · data …) 금지,
  공개 내보내기 = --metadata none + 메타데이터 검사.

⚠ 초안 — 이 환경에서는 문법 검사 (py_compile) 만 했다.  PhotoCraft 를 실제로 부른 적 없음.
⚠ photocraft-cli 의 run 은 '믿는 로컬' 모드라 폴더 제한이 없다 — 이 도우미의 허용 목록 · 경로 검사가 울타리다.
"""
import datetime
import hashlib
import importlib.util
import json
import os
import platform
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile

SCHEMA = "pc-lab-record/1"
IN_EXT = {".png", ".tif", ".tiff", ".jpg", ".jpeg", ".bmp", ".webp"}  # 평면 래스터만 (PSD · pcraft 등 문서는 MCP 작업 공간으로)
OUT_EXT = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp"}
MAX_STEPS = 64
MAX_INPUT_MB = 400
DATA_RESAMPLE = {"bicubic", "bilinear", "lanczos", "nearest"}  # 고정 커널만 (preserveDetails · automatic = 날카롭게 함)
COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
BANNED_KEYS = {"path", "file", "dir", "profile", "mapPath", "data", "fileName", "target", "layer",
               "eyedropper", "droplet", "input", "output", "script", "url"}


def _load_pc_img():
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("pc_img", os.path.join(here, "pc_img.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def inside(child, parent):
    child, parent = os.path.realpath(child), os.path.realpath(parent)
    return os.path.commonpath([child, parent]) == parent


# --------------------------------------------------------------------------------------------
# action JSON
# --------------------------------------------------------------------------------------------
def load_actions(path):
    """정본 꼴 = {"steps": [[id, {params}], …]}.  PhotoCraft 가 받는 다른 꼴 (bare 목록 · {"command","params"})
    도 읽지만, Actions 세트 ({"actions": [{"name", "steps"}]}) · .atn 은 받지 않는다."""
    if path.lower().endswith(".atn"):
        raise ValueError("Photoshop .atn 은 쓰지 않는다 — 우리 action JSON 만")
    with open(path, "r", encoding="utf-8-sig") as f:
        doc = json.load(f)
    steps = doc.get("steps") if isinstance(doc, dict) else doc
    if isinstance(doc, dict) and "actions" in doc:
        raise ValueError("Actions 세트 꼴은 받지 않는다 — {\"steps\": [...]} 로")
    if not isinstance(steps, list):
        raise ValueError("steps 가 목록이 아니다")
    out = []
    for st in steps:
        if isinstance(st, list) and st and isinstance(st[0], str):
            params = st[1] if len(st) > 1 else {}
            out.append((st[0], params))
        elif isinstance(st, dict) and isinstance(st.get("command", st.get("id")), str):
            out.append((st.get("command", st.get("id")), st.get("params", {})))
        elif isinstance(st, str):
            out.append((st, {}))
        else:
            raise ValueError("알 수 없는 단계 꼴: %r" % (st,))
    return out


def _num(v, lo=None, hi=None):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return False
    if v != v or v in (float("inf"), float("-inf")):
        return False
    return (lo is None or v >= lo) and (hi is None or v <= hi)


def _keys(params, allowed, errs, sid):
    extra = set(params) - set(allowed)
    if extra:
        errs.append("%s: 허용하지 않은 매개변수 %s" % (sid, sorted(extra)))


def v_empty(p, errs, sid, mode):
    if p:
        errs.append("%s: 매개변수 없이 써야 한다" % sid)


def v_crop(p, errs, sid, mode):
    _keys(p, {"x", "y", "width", "height", "deleteCroppedPixels", "contentAware", "angle",
              "targetWidth", "targetHeight", "resolution", "resample"}, errs, sid)
    if not all(k in p for k in ("x", "y", "width", "height")):
        errs.append("%s: x · y · width · height 네 값을 모두 적는다 (선택 영역으로 자르지 않는다)" % sid)
    for k in ("x", "y"):
        if k in p and not (isinstance(p[k], int) and p[k] >= 0):
            errs.append("%s: %s 는 0 이상 정수" % (sid, k))
    for k in ("width", "height"):
        if k in p and not (isinstance(p[k], int) and p[k] > 0):
            errs.append("%s: %s 는 1 이상 정수" % (sid, k))
    if p.get("contentAware", False) is not False:
        errs.append("%s: contentAware (내용 인식 채우기 = 생성형 채우기) 금지" % sid)
    if p.get("deleteCroppedPixels", True) is not True:
        errs.append("%s: deleteCroppedPixels 는 true (기본) 만" % sid)
    if p.get("angle", 0) != 0:
        errs.append("%s: angle (회전 자르기 = 재표본) 금지" % sid)
    if ("targetWidth" in p) != ("targetHeight" in p):
        errs.append("%s: targetWidth · targetHeight 는 둘 다 또는 둘 다 없음" % sid)
    if "resample" in p and p["resample"] not in DATA_RESAMPLE:
        errs.append("%s: resample 은 %s 만" % (sid, sorted(DATA_RESAMPLE)))
    if "resolution" in p and not _num(p["resolution"], 1, 30000):
        errs.append("%s: resolution 은 1–30000 ppi" % sid)


def v_image_size(p, errs, sid, mode):
    _keys(p, {"width", "height", "percent", "resolution", "resample", "units", "keepPrintSize", "scaleStyles"}, errs, sid)
    if p.get("units", "px") != "px":
        errs.append("%s: units 는 px 만 (pt 는 문서 해상도에 따라 달라짐)" % sid)
    rs = p.get("resample", "bicubic")
    if rs not in DATA_RESAMPLE | {"none"}:
        errs.append("%s: resample '%s' 금지 — %s 또는 none (preserveDetails · automatic 은 날카롭게 함)" % (sid, rs, sorted(DATA_RESAMPLE)))
    for k in ("width", "height"):
        if k in p and not _num(p[k], 1, 300000):
            errs.append("%s: %s 범위" % (sid, k))
    if "percent" in p and not _num(p["percent"], 0.01, 100000):
        errs.append("%s: percent 범위" % sid)
    if "resolution" in p and not _num(p["resolution"], 1, 30000):
        errs.append("%s: resolution 범위" % sid)


def v_fit_image(p, errs, sid, mode):
    _keys(p, {"width", "height", "dontEnlarge", "resample"}, errs, sid)
    if not (_num(p.get("width"), 1, 300000) and _num(p.get("height"), 1, 300000)):
        errs.append("%s: width · height 필요" % sid)
    if p.get("resample", "bicubic") not in DATA_RESAMPLE:
        errs.append("%s: resample 은 %s 만" % (sid, sorted(DATA_RESAMPLE)))


def v_canvas(p, errs, sid, mode):
    _keys(p, {"width", "height", "units", "relative", "anchor", "extensionColor"}, errs, sid)
    if p.get("units", "px") not in ("px", "percent"):
        errs.append("%s: units 는 px · percent" % sid)
    col = p.get("extensionColor")
    if not (col in ("white", "black", "gray") or (isinstance(col, str) and COLOR_RE.match(col))):
        errs.append("%s: extensionColor 를 white · black · gray · #rrggbb 로 분명히 적는다" % sid)
    if p.get("anchor", "center") not in ("topLeft", "top", "topRight", "left", "center", "right",
                                         "bottomLeft", "bottom", "bottomRight"):
        errs.append("%s: anchor 값" % sid)


def v_levels(p, errs, sid, mode):
    allowed = {"inBlack", "inWhite", "outBlack", "outWhite", "gamma"}
    if mode == "figure":
        allowed |= {"red", "green", "blue", "gray"}
    _keys(p, allowed, errs, sid)
    if mode == "data" and p.get("gamma", 1) != 1:
        errs.append("%s: data 에서는 gamma = 1 (선형) 만" % sid)
    ib, iw = p.get("inBlack", 0), p.get("inWhite", 255)
    if not (_num(ib, 0, 253) and _num(iw, 2, 255) and ib < iw):
        errs.append("%s: inBlack < inWhite (0–255)" % sid)
    for k in ("outBlack", "outWhite"):
        if k in p and not _num(p[k], 0, 255):
            errs.append("%s: %s 는 0–255" % (sid, k))


def v_bc(p, errs, sid, mode):
    _keys(p, {"brightness", "contrast", "legacy"}, errs, sid)
    if mode == "data" and p.get("legacy") is not True:
        errs.append("%s: data 에서는 legacy: true (선형) 만 — 기본 (현대식) 은 곡선이다" % sid)
    if not _num(p.get("brightness", 0), -150, 150) or not _num(p.get("contrast", 0), -50, 100):
        errs.append("%s: brightness −150–150 · contrast −50–100 (PhotoCraft 매개변수 문서 범위)" % sid)


def v_curves(p, errs, sid, mode):
    _keys(p, {"points", "red", "green", "blue", "gray", "smooth"}, errs, sid)


def v_unsharp(p, errs, sid, mode):
    _keys(p, {"amount", "radius", "threshold"}, errs, sid)


def v_mode_gray(p, errs, sid, mode):
    _keys(p, {"intent", "bpc"}, errs, sid)


def v_blackwhite(p, errs, sid, mode):
    _keys(p, {"reds", "yellows", "greens", "cyans", "blues", "magentas", "tint", "tintColor"}, errs, sid)


def v_trim(p, errs, sid, mode):
    _keys(p, {"basedOn", "top", "bottom", "left", "right"}, errs, sid)


def v_type(p, errs, sid, mode):
    _keys(p, {"x", "y", "text", "box", "name", "align", "font", "fontStyle", "weight", "italic", "size",
              "color", "tracking", "leading"}, errs, sid)
    t = p.get("text", "")
    if not isinstance(t, str) or not t or len(t) > 200:
        errs.append("%s: text 는 1–200 글자" % sid)


DATA_ALLOW = {
    "select.deselect": v_empty,
    "image.crop": v_crop,
    "image.imageSize": v_image_size,
    "file.automate.fitImage": v_fit_image,
    "image.canvasSize": v_canvas,
    "image.adjustments.levels": v_levels,
    "image.adjustments.brightnessContrast": v_bc,
    "image.imageRotation.90cw": v_empty,
    "image.imageRotation.90ccw": v_empty,
    "image.imageRotation.180": v_empty,
    "image.mode.bits8": v_empty,
    "image.mode.bits16": v_empty,
}
FIGURE_ALLOW = dict(DATA_ALLOW)
FIGURE_ALLOW.update({
    "image.adjustments.curves": v_curves,
    "image.adjustments.desaturate": v_empty,
    "image.adjustments.blackWhite": v_blackwhite,
    "image.mode.grayscale": v_mode_gray,
    "image.mode.rgb": v_mode_gray,
    "filter.sharpen.unsharpMask": v_unsharp,
    "filter.sharpen.sharpen": v_empty,
    "type.create": v_type,
    "image.trim": v_trim,
    "image.imageRotation.flipCanvasHorizontal": v_empty,
    "image.imageRotation.flipCanvasVertical": v_empty,
    "layer.flattenImage": v_empty,
})


def validate(steps, mode):
    allow = DATA_ALLOW if mode == "data" else FIGURE_ALLOW
    errs = []
    if not steps:
        errs.append("단계가 없다")
    if len(steps) > MAX_STEPS:
        errs.append("단계 %d 개 > %d" % (len(steps), MAX_STEPS))
    if mode == "data" and (not steps or steps[0][0] != "select.deselect"):
        errs.append("data: 첫 단계는 select.deselect (조정은 선택 영역에만 걸리므로 먼저 푼다)")
    for i, (cid, params) in enumerate(steps):
        sid = "#%d %s" % (i + 1, cid)
        if not isinstance(params, dict):
            errs.append("%s: params 는 객체" % sid)
            continue
        banned = BANNED_KEYS & set(params)
        if banned:
            errs.append("%s: 경로 · 대상 매개변수 금지 %s" % (sid, sorted(banned)))
        fn = allow.get(cid)
        if fn is None:
            errs.append("%s: %s 허용 목록에 없음" % (sid, mode))
            continue
        fn(params, errs, sid, mode)
    return errs


def crop_only_offset(steps):
    """pointop 을 자동으로 할 수 있는 꼴: 크기 · 회전을 바꾸는 단계가 없고, 자르기는 많아야 한 번 (먼저)."""
    geom = [(c, p) for c, p in steps if c in ("image.crop", "image.imageSize", "file.automate.fitImage",
                                                 "image.canvasSize", "image.imageRotation.90cw",
                                                 "image.imageRotation.90ccw", "image.imageRotation.180")]
    if not geom:
        return (0, 0), None
    if len(geom) == 1 and geom[0][0] == "image.crop" and "targetWidth" not in geom[0][1]:
        return (geom[0][1]["x"], geom[0][1]["y"]), None
    return None, "크기 · 회전 · 여백 · 여러 번 자르기가 있어 자동 대응점을 못 정함 (조정만 먼저 따로 돌려 검사 → 크기는 그 뒤)"


# --------------------------------------------------------------------------------------------
# job
# --------------------------------------------------------------------------------------------
def job_dirs(job):
    d = {k: os.path.join(job, k) for k in ("in", "actions", "out", "record", ".pc_config")}
    return d


def cmd_init(job, src, note, sub):
    """원본을 JOB/in/[SUB/]이름 으로 복사한다.  SUB = 작업 하나의 하위 폴더 (JOB 은 오래 쓰는 작업 공간)."""
    d = job_dirs(job)
    for k in d.values():
        os.makedirs(k, exist_ok=True)
    ext = os.path.splitext(src)[1].lower()
    if ext not in IN_EXT:
        raise ValueError("입력 확장자 %s 는 받지 않는다 (%s)" % (ext, sorted(IN_EXT)))
    if os.path.getsize(src) > MAX_INPUT_MB * 1024 * 1024:
        raise ValueError("입력이 %d MB 를 넘는다" % MAX_INPUT_MB)
    rel = os.path.join(sub, os.path.basename(src)) if sub else os.path.basename(src)
    dst = os.path.join(d["in"], rel)
    if not inside(os.path.dirname(os.path.abspath(dst)), d["in"]):
        raise ValueError("--to 는 JOB/in 아래 하위 폴더 이름만")
    if os.path.exists(dst):
        raise ValueError("이미 있다: %s (덮어쓰지 않음)" % dst)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    h0 = sha256_file(src)
    shutil.copy2(src, dst)
    h1 = sha256_file(dst)
    if h0 != h1:
        raise ValueError("복사본 sha256 이 다르다")
    os.chmod(dst, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
    rec = {"schema": SCHEMA + "/source", "created_utc": now_utc(), "name": rel.replace(os.sep, "/"),
           "sha256": h0, "bytes": os.path.getsize(dst), "source_note": note}
    src_rec = os.path.join(d["record"], rel + ".source.json")
    os.makedirs(os.path.dirname(src_rec), exist_ok=True)
    with open(src_rec, "x", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=1)
    print(json.dumps(rec, ensure_ascii=False, indent=1))
    return 0


def build_argv(bin_path, in_path, out_path, steps, quality):
    argv = [bin_path, "run", in_path]
    for cid, params in steps:
        argv += ["--cmd", cid, "--params", json.dumps(params, ensure_ascii=False, separators=(",", ":"))]
    argv += ["--cmd", "document.inspect", "--out", out_path, "--metadata", "none", "--no-gpu"]
    ext = os.path.splitext(out_path)[1].lower()
    if ext in (".jpg", ".jpeg"):
        argv += ["--quality", str(quality or 92), "--jpeg-format", "baseline"]
    elif ext == ".webp" and quality:
        argv += ["--quality", str(quality)]
    return argv


def run_env(job):
    env = dict(os.environ)
    env.pop("PHOTOCRAFT_GPU", None)
    env.pop("PHOTOCRAFT_CONTROL_PORT", None)
    env["PHOTOCRAFT_CONFIG_DIR"] = os.path.abspath(job_dirs(job)[".pc_config"])
    return env


def run_tool(argv, env, timeout):
    # text=True 대신 UTF-8 로 읽는다 (Windows 기본 코드 페이지 cp949 에서 JSON 이 깨지지 않게).
    return subprocess.run(argv, capture_output=True, encoding="utf-8", errors="replace", timeout=timeout, env=env)


def tool_identity(bin_path, env):
    ver = run_tool([bin_path, "--version"], env, 60)
    real = shutil.which(bin_path) or bin_path
    return {"bin": os.path.basename(real), "bin_sha256": sha256_file(real) if os.path.isfile(real) else None,
            "version": ver.stdout.strip() or ver.stderr.strip(), "os": platform.platform(),
            "python": platform.python_version()}


def parse_run_stdout(text):
    inspect, results = None, []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        results.append(obj.get("command"))
        if obj.get("command") == "document.inspect":
            inspect = obj.get("result")
    return inspect, results


def cmd_run(a):
    pc_img = _load_pc_img()
    d = job_dirs(a.job)
    steps = load_actions(a.actions)
    errs = validate(steps, a.mode)
    if errs:
        print("허용 목록 검사 실패:\n  " + "\n  ".join(errs), file=sys.stderr)
        return 1
    in_path = os.path.abspath(os.path.join(d["in"], a.in_name))
    out_path = os.path.abspath(os.path.join(d["out"], a.out_name))
    if not inside(in_path, d["in"]) or not inside(out_path, d["out"]):
        raise ValueError("입력은 JOB/in 아래, 출력은 JOB/out 아래만")
    if os.path.splitext(in_path)[1].lower() not in IN_EXT or os.path.splitext(out_path)[1].lower() not in OUT_EXT:
        raise ValueError("확장자 허용 목록 밖")
    if not os.path.isfile(in_path):
        raise ValueError("입력이 없다: %s" % in_path)
    if os.path.exists(out_path):
        raise ValueError("출력이 이미 있다 (덮어쓰지 않음): %s" % out_path)
    stem = os.path.splitext(a.out_name)[0]
    log_path = os.path.join(d["record"], stem + ".run.log")
    rec_path = os.path.join(d["record"], stem + ".record.json")
    ko_path = os.path.join(d["record"], stem + ".record_ko.md")
    for p in (log_path, rec_path, ko_path):
        if os.path.exists(p):
            raise ValueError("기록이 이미 있다 (덮어쓰지 않음 · 새 출력 이름으로): %s" % p)
    argv = build_argv(a.bin, in_path, out_path, steps, a.quality)
    if a.dry_run:
        print(json.dumps(argv, ensure_ascii=False))
        print(shlex.join(argv))
        return 0
    for k in ("out", "record", ".pc_config"):
        os.makedirs(d[k], exist_ok=True)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    env = run_env(a.job)
    ident = tool_identity(a.bin, env)
    in_sha_before = sha256_file(in_path)
    proc = run_tool(argv, env, 1800)
    with open(log_path, "x", encoding="utf-8") as f:
        f.write("$ " + shlex.join(argv) + "\n--- stdout\n" + proc.stdout + "\n--- stderr\n" + proc.stderr)
    warnings = [ln[len("warning: "):] for ln in proc.stderr.splitlines() if ln.startswith("warning: ")]
    inspect, ran = parse_run_stdout(proc.stdout)
    rec = {"schema": SCHEMA, "created_utc": now_utc(), "mode": a.mode, "note": a.note, "source_ref": a.source_ref,
           "tool": ident, "argv": [os.path.basename(argv[0])] + [os.path.relpath(x, a.job) if os.path.isabs(x) else x for x in argv[1:]],
           "returncode": proc.returncode, "warnings": warnings, "commands_reported": ran,
           "input": {"name": a.in_name, "sha256": in_sha_before},
           "actions": {"name": os.path.basename(a.actions), "sha256": sha256_file(a.actions), "steps": steps},
           "checks": {"allowlist": "ok"}}
    if inspect:
        rec["final_doc"] = {k: inspect.get(k) for k in ("width", "height", "mode", "depth", "resolution", "hasSelection")}
        rec["history"] = inspect.get("history")
    ok = proc.returncode == 0 and os.path.isfile(out_path)
    if sha256_file(in_path) != in_sha_before:
        rec["checks"]["input_unchanged"] = False
        ok = False
    else:
        rec["checks"]["input_unchanged"] = True
    if any(w.startswith("font ") for w in warnings) and not a.allow_font_fallback:
        rec["checks"]["fonts"] = "missing (글꼴 대체됨 — 최종본 아님)"
        ok = False
    if os.path.isfile(out_path):
        rec["output"] = {"name": a.out_name, "sha256": sha256_file(out_path), "bytes": os.path.getsize(out_path)}
        try:
            meta = pc_img.meta_report(out_path, MAX_INPUT_MB)
            rec["checks"]["metadata"] = {"public_safe": meta["public_safe"], "gps": meta["gps"],
                                         "items": [i.get("what") or i.get("name") for i in meta["items"]]}
        except pc_img.Unsupported as exc:
            rec["checks"]["metadata"] = "검사 못 함: %s" % exc
        if out_path.lower().endswith(".png"):
            try:
                rec["output"]["pixel_sha256"] = pc_img.pixel_hash(pc_img.png_decode(pc_img.read_file(out_path, MAX_INPUT_MB)))
            except pc_img.Unsupported as exc:
                rec["output"]["pixel_sha256"] = "못 셈: %s" % exc
        if a.mode == "data":
            ref = os.path.abspath(os.path.join(d["in"], a.ref_png)) if a.ref_png else (in_path if in_path.lower().endswith(".png") else None)
            offset, why = crop_only_offset(steps)
            if ref is not None and not inside(ref, d["in"]):
                rec["checks"]["pointop"] = "건너뜀: --ref-png 는 JOB/in 아래만"
            elif ref is None:
                rec["checks"]["pointop"] = "건너뜀: 입력이 PNG 가 아님 (--ref-png 로 PNG 사본 지정)"
            elif not out_path.lower().endswith(".png"):
                rec["checks"]["pointop"] = "건너뜀: 출력이 PNG 가 아님"
            elif offset is None:
                rec["checks"]["pointop"] = "건너뜀: " + why
            else:
                try:
                    rep = pc_img.pointop(ref, out_path, offset, MAX_INPUT_MB)
                    rec["checks"]["pointop"] = {"verdict": rep["verdict"], "channels": rep["channels"],
                                                "offset": rep["offset"], "examples": rep["examples"][:3]}
                    if rep["verdict"] != "PASS_LINEAR":
                        ok = False
                except pc_img.Unsupported as exc:
                    rec["checks"]["pointop"] = "검사 못 함: %s" % exc
    rec["ok"] = ok
    with open(rec_path, "x", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=1)
    with open(ko_path, "x", encoding="utf-8") as f:
        f.write(summary_ko(rec))
    print(rec_path)
    return 0 if ok else 1


def summary_ko(rec):
    steps = "; ".join("%s %s" % (c, json.dumps(p, ensure_ascii=False, separators=(",", ":"))) for c, p in rec["actions"]["steps"])
    meta = rec["checks"].get("metadata")
    meta_txt = ("메타데이터 공개 안전" if isinstance(meta, dict) and meta.get("public_safe") else "메타데이터 남음 — 확인 필요")
    po = rec["checks"].get("pointop")
    po_txt = po["verdict"] if isinstance(po, dict) else (po or "해당 없음")
    out = rec.get("output", {})
    return (
        "- 그림 처리 기록 (%s · %s)\n"
        "  - 원본 %s (sha256 %s…) → 결과 %s (sha256 %s…)\n"
        "  - 처리 (action %s · sha256 %s…): %s\n"
        "  - 도구: %s · 종료 코드 %s · 입력 그대로 %s · %s · 점 연산 검사 %s\n"
        % (rec["mode"], rec["created_utc"], rec["input"]["name"], rec["input"]["sha256"][:12], out.get("name"),
           (out.get("sha256") or "")[:12], rec["actions"]["name"], rec["actions"]["sha256"][:12], steps,
           rec["tool"]["version"], rec["returncode"], rec["checks"].get("input_unchanged"), meta_txt, po_txt))


def cmd_verify(record_path, bin_path):
    pc_img = _load_pc_img()
    with open(record_path, encoding="utf-8") as f:
        rec = json.load(f)
    cur = os.path.dirname(os.path.abspath(record_path))
    while os.path.basename(cur) != "record":
        parent = os.path.dirname(cur)
        if parent == cur:
            raise ValueError("기록 파일이 JOB/record 아래에 있지 않다")
        cur = parent
    job = os.path.dirname(cur)
    d = job_dirs(job)
    in_path = os.path.join(d["in"], rec["input"]["name"])
    if sha256_file(in_path) != rec["input"]["sha256"]:
        print("입력 sha256 이 기록과 다르다", file=sys.stderr)
        return 1
    errs = validate([tuple(s) for s in rec["actions"]["steps"]], rec["mode"])
    if errs:
        print("기록의 단계가 지금 허용 목록을 통과하지 않음:\n  " + "\n  ".join(errs), file=sys.stderr)
        return 1
    ext = os.path.splitext(rec["output"]["name"])[1]
    tmpdir = tempfile.mkdtemp(prefix="_verify_", dir=d["out"])
    out_path = os.path.join(tmpdir, "again" + ext)
    q = int(rec["argv"][rec["argv"].index("--quality") + 1]) if "--quality" in rec["argv"] else None
    argv = build_argv(bin_path, in_path, out_path, [tuple(s) for s in rec["actions"]["steps"]], q)
    proc = run_tool(argv, run_env(job), 1800)
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        return 1
    same_file = sha256_file(out_path) == rec["output"]["sha256"]
    same_px = None
    if ext.lower() == ".png" and isinstance(rec["output"].get("pixel_sha256"), str):
        same_px = pc_img.pixel_hash(pc_img.png_decode(pc_img.read_file(out_path, MAX_INPUT_MB))) == rec["output"]["pixel_sha256"]
    print(json.dumps({"same_file_sha256": same_file, "same_pixels": same_px, "again": out_path}, ensure_ascii=False))
    return 0 if (same_file or same_px) else 1


def cmd_mcp(job, bin_path):
    d = job_dirs(job)
    r, w = os.path.abspath(d["in"]), os.path.abspath(d["out"])
    if r == w:
        raise ValueError("read root 와 write root 는 달라야 한다")
    argv = ["claude", "mcp", "add", "--scope", "local", "photocraft", "--", bin_path, "mcp", "--headless", "--no-gpu",
            "--automation-read-root", r, "--automation-write-root", w]
    print("# 출력만 한다 — 등록은 1저자가 직접 (자동으로 하지 않음)")
    print(shlex.join(argv))
    return 0


class Args:
    pass


def parse(argv):
    if not argv or argv[0] in ("-h", "--help"):
        return None
    a = Args()
    a.cmd = argv[0]
    pos, opts = [], {}
    flags = {"--dry-run", "--allow-font-fallback"}
    i = 1
    while i < len(argv):
        t = argv[i]
        if t in flags:
            opts[t] = True
            i += 1
        elif t.startswith("--"):
            if i + 1 >= len(argv):
                raise ValueError("%s 값이 없다" % t)
            opts[t] = argv[i + 1]
            i += 2
        else:
            pos.append(t)
            i += 1
    a.pos = pos
    a.job = pos[0] if pos else None
    a.actions = pos[1] if len(pos) > 1 else (pos[0] if a.cmd == "check" and pos else None)
    a.mode = opts.get("--mode")
    a.bin = opts.get("--bin", "photocraft-cli")
    a.in_name, a.out_name = opts.get("--in"), opts.get("--out")
    a.quality = int(opts["--quality"]) if "--quality" in opts else None
    a.note, a.source_ref = opts.get("--note"), opts.get("--source-ref")
    a.ref_png = opts.get("--ref-png")
    a.src, a.source_note, a.to = opts.get("--src"), opts.get("--source-note"), opts.get("--to")
    a.dry_run = bool(opts.get("--dry-run"))
    a.allow_font_fallback = bool(opts.get("--allow-font-fallback"))
    if a.mode not in (None, "data", "figure"):
        raise ValueError("--mode 는 data · figure")
    if a.quality is not None and not 1 <= a.quality <= 100:
        raise ValueError("--quality 는 1–100")
    return a


def main(argv):
    try:
        a = parse(argv)
        if a is None:
            print(__doc__)
            return 0
        if a.cmd == "init" and a.job and a.src:
            return cmd_init(a.job, a.src, a.source_note, a.to)
        if a.cmd == "check" and a.actions and a.mode:
            errs = validate(load_actions(a.actions), a.mode)
            print("통과" if not errs else "걸림:\n  " + "\n  ".join(errs))
            return 0 if not errs else 1
        if a.cmd == "run" and a.job and a.actions and a.mode and a.in_name and a.out_name:
            return cmd_run(a)
        if a.cmd == "verify" and a.pos:
            return cmd_verify(a.pos[0], a.bin)
        if a.cmd == "mcp-cmd" and a.job:
            return cmd_mcp(a.job, a.bin)
        print("인자가 모자란다 — --help", file=sys.stderr)
        return 2
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print("pc_actions: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
