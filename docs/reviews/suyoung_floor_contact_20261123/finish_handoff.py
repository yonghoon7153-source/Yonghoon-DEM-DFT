"""Add the registered weekly PNG/CSV from a completed author return to the code handoff."""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import struct
import tarfile
import tempfile
import zipfile
import zlib


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check(value, label):
    if not value:
        raise ValueError(label)


def checksum_table(raw):
    pairs = [line.split("  ", 1) for line in raw.decode("utf-8").splitlines()]
    check(len(pairs) == len({name for _, name in pairs}), "duplicate checksum entry")
    return {name: digest for digest, name in pairs}


def verified_source(path, expected_sha, pin):
    raw = path.read_bytes()
    check(sha(raw) == expected_sha, "source handoff checksum")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names = z.namelist()
        check(len(set(names)) == len(names) and z.testzip() is None, "source ZIP")
        manifest = checksum_table(z.read("SHA256SUMS"))
        check(set(names) == set(manifest) | {"SHA256SUMS"}, "source manifest")
        files = {name:z.read(name) for name in manifest}
    check(all(sha(raw) == manifest[name] for name, raw in files.items()), "source member hash")
    check(json.loads(files["CHAIN.json"])["release"] == pin, "source release differs")
    return files


def pixels(png, width, height):
    check(png.startswith(b"\x89PNG\r\n\x1a\n"), "PNG signature")
    pos, compressed, ended = 8, bytearray(), False
    while pos + 12 <= len(png):
        size = struct.unpack_from(">I", png, pos)[0]
        tag = png[pos+4:pos+8]
        end = pos + size + 8
        check(end+4 <= len(png),"truncated PNG")
        body = png[pos+8:end]
        check(zlib.crc32(tag+body) == struct.unpack_from(">I",png,end)[0],"PNG CRC")
        if pos == 8:
            check(tag == b"IHDR" and body == struct.pack(">II5B",width,height,8,2,0,0,0),"PNG parameters")
        pos = end+4
        if tag == b"IDAT":
            compressed.extend(body)
        if tag == b"IEND":
            ended = size==0
            break
    check(ended and pos == len(png),"PNG end")
    raster = zlib.decompress(compressed)
    check(len(raster) == height*(1+3*width),"PNG decoded length")
    return raster


def check_graph(sources, series, png):
    import numpy as np
    prefix = "snapshot/docs/reviews/suyoung_floor_contact_20261123/"
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)/"render_weekly.py"
        path.write_bytes(sources[prefix+path.name])
        face = path.with_name("weekly_type.npz")
        face.write_bytes(sources[prefix+face.name])
        spec = importlib.util.spec_from_file_location("pinned_weekly_renderer",path)
        plot = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plot)
        with np.load(face, allow_pickle=False) as stored:
            atlas = {key: stored[key] for key in stored.files if key != "license"}
        curves = {key:[(x/plot.DIAMETER,y) for x,y in rows] for key,rows in series.items()}
        img = plot.render_image(curves,atlas)
        expected = b"".join(b"\0"+row.tobytes() for row in img)
        check(pixels(png,plot.WIDTH,plot.HEIGHT) == expected,"PNG pixels differ from native traces")


def delivered(return_dir, pin, sources):
    archive = return_dir/"suyoung_floor_prefix_result.tar.gz"
    manifest = checksum_table((return_dir/"SHA256SUMS").read_bytes())
    check(set(manifest) == {archive.name,"screen.txt"}, "author output file set")
    with archive.open("rb") as stream:
        check(hashlib.file_digest(stream,"sha256").hexdigest() == manifest[archive.name], "author archive")
    screen = (return_dir/"screen.txt").read_bytes()
    lines = screen.splitlines()
    check(sha(screen) == manifest["screen.txt"] and lines[-1:] == [b"COMMAND_RC=0"]
          and sum(line.startswith(b"COMMAND_RC=") for line in lines) == 1
          and all(line in lines for line in (b"DEVELOPMENT_ONLY",b"F8_RC=0",b"F16_RC=0",
                                             b"FOUR_NATIVE_CURVES_AND_WEEKLY_PNG_OK"))
          and b"SYNTHETIC_QA_ONLY" not in lines, "field status")
    with tarfile.open(archive, "r:gz") as z:
        members = z.getmembers()
        check(len(set(e.name for e in members)) == len(members), "duplicate return member")
        check(not any(e.name.endswith(("/incomplete.json","/SYNTHETIC_QA_ONLY")) for e in members), "incomplete run")
        def member(name):
            entry = z.getmember("run/"+name)
            check(entry.isfile(), "missing regular file: "+name)
            return z.extractfile(entry).read()
        check(member("screen.txt") == screen and member("RELEASE").decode().strip() == pin,"screen or release")
        raw_summary = member("summary.json")
        summary = json.loads(raw_summary)
        check(summary["release"] == pin and summary["status"] == "SHORT_PREFIX_COMPLETE"
              and summary["qualification_computed"] is False and summary["stage3_go"] is False, "short-run receipt")
        case = "docs/reviews/suyoung_floor_contact_20261123/"
        for path, key in (("material_floor.py","candidate_sha256"),("floor_operator.py","operator_sha256")):
            check(sha(sources["snapshot/"+case+path]) == summary[key], "source binding "+path)
        check(sha(member("SOURCE_SHA256SUMS")) == summary["release_manifest_sha256"],"execution manifest")
        curves = {}
        originals = {8:"0e5e021706abbc88a728a305807edfce02aa877bcd92d824d5aa2988515aebce",
                     16:"60b31c9055734a24cd9aaa0ed1b5809fad338fb6d5848ab0a49f4d52f9945eca"}
        for model in ("original","candidate"):
            for n, steps in ((8,270),(16,540)):
                path = f"{model}/F{n}/trace.csv"
                trace = member(path)
                check(sha(trace) == summary["trace_sha256"][path] and len(trace.splitlines()) == steps+2,"trace binding")
                if model == "original":
                    check(sha(trace) == originals[n],"original trace")
                curves[model,n] = list(csv.DictReader(io.StringIO(trace.decode("ascii"))))
        for cells in (8,16):
            before = f"original/F{cells}"
            after = f"candidate/F{cells}"
            receipts = summary["receipt_sha256"]
            check(sha(member(after+"/receipt.json")) == receipts[after], "candidate receipt")
            for name in ("cross_receipt.json","prefix_receipt.json"):
                check(sha(member(before+"/"+name)) == receipts[before][name], "prior receipt")
        table = member("pressure_displacement.csv")
        png = member("weekly_pressure_displacement.png")
        check(sha(table) == summary["pressure_displacement_sha256"] and len(table.splitlines()) == 1625,"weekly CSV")
        table_rows = iter(csv.DictReader(io.StringIO(table.decode("ascii"))))
        plot_series = {}
        for (model,n), rows in curves.items():
            initial = float(rows[0]["height"])
            plot_series[model,n] = []
            for trace_row in rows:
                point = next(table_rows)
                check((point["wall_model"], int(point["cells"]), point["step"]) == (model,n,trace_row["step"])
                      and float(point["time_code"]) == float(trace_row["time_code"])
                      and float(point["height"]) == float(trace_row["height"])
                      and float(point["displacement_code"]) == initial - float(trace_row["height"])
                      and float(point["pressure_MPa"]) == 10*float(trace_row["bottom_pressure_E"]),
                      "weekly data point")
                plot_series[model,n].append((float(point["displacement_code"]),float(point["pressure_MPa"])))
        check(sha(png) == summary["weekly_png_sha256"] and png[:8] == b"\x89PNG\r\n\x1a\n"
              and b"CSV_SHA256\0" + sha(table).encode("ascii") in png,"weekly PNG")
        check_graph(sources,plot_series,png)
    return {"weekly/pressure_displacement.csv": table, "weekly/weekly_pressure_displacement.png": png,
            "weekly/summary.json": raw_summary, "weekly/return_SHA256SUMS": (return_dir/"SHA256SUMS").read_bytes()}


def publish(target, raw):
    # A retry after interrupted packaging may reuse complete, identical files.
    # Never truncate an earlier handoff and never expose a partly-written ZIP.
    with tempfile.NamedTemporaryFile(dir=target.parent,delete=False) as tmp:
        stage = Path(tmp.name)
    try:
        stage.write_bytes(raw)
        try:
            if os.name == "nt":
                os.rename(stage,target)  # Windows refuses an existing destination.
            else:
                os.link(stage,target)
        except FileExistsError:
            check(target.read_bytes()==raw,"existing handoff differs")
    finally:
        stage.unlink(missing_ok=True)


def finish(source, expected, returned, pin):
    files = verified_source(source, expected, pin)
    payload = delivered(returned, pin, files)
    check(not (files.keys() & payload.keys()), "duplicate report member")
    files.update(payload)
    files["SHA256SUMS"] = "".join(sha(v)+"  "+k+"\n" for k,v in sorted(files.items())).encode()
    target = returned/("codex_suyoung_floor_contact_"+pin[:12]+"_with_weekly.zip")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,raw in sorted(files.items()):
            z.writestr(zipfile.ZipInfo(name),raw,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(buffer) as z:
        check(z.testzip() is None and all(z.read(k)==v for k,v in files.items()),"final ZIP integrity")
    raw = buffer.getvalue()
    publish(target,raw)
    publish(returned/"HANDOFF_SHA256SUMS",(sha(raw)+"  "+target.name+"\n").encode())
    print("WEEKLY_HANDOFF="+str(target))
    print("WEEKLY_HANDOFF_SHA256="+sha(raw))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source",type=Path)
    parser.add_argument("source_sha256")
    parser.add_argument("return_directory",type=Path)
    parser.add_argument("pin")
    args = parser.parse_args()
    finish(args.source,args.source_sha256,args.return_directory,args.pin)
