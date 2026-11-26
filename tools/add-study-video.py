"""Append an approved, immutable dated episode and a poster derived from its actual video."""
import argparse
import contextlib
import datetime
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "study-videos.json"
MEDIA = ROOT / "public" / "study-videos"
LIMIT = 25 * 1024 * 1024


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def inspect(path):
    result = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
        "stream=codec_name,codec_type,codec_tag_string,pix_fmt:chapter=id:format=format_name,duration",
        "-of", "json", str(path)])
    info = json.loads(result)
    streams = info["streams"]
    # QuickTime chapters may use one text-tagged data track alongside the actual media.
    chapters = [s for s in streams if s.get("codec_type") == "data" and s.get("codec_name") == "bin_data"
                and s.get("codec_tag_string") == "text"]
    if len(chapters) == 1 and info.get("chapters"):
        streams = [s for s in streams if s != chapters[0]]
    if not ("mp4" in info["format"]["format_name"].split(",") and len(streams) == 2
            and any(s.get("codec_name") == "h264" and s.get("pix_fmt") == "yuv420p" for s in streams)
            and any(s.get("codec_name") == "aac" for s in streams)):
        raise ValueError("Expected a playable H.264 yuv420p MP4 with one AAC audio stream")
    duration = float(info["format"]["duration"])
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError("Missing video duration")
    return round(duration, 3)


def add(args):
    date = datetime.date.fromisoformat(args.date).isoformat()
    if date != args.date or not re.fullmatch(r"[0-9a-f]{64}", args.approved_sha256):
        raise ValueError("Expected YYYY-MM-DD and the approved SHA-256 in lowercase")
    if any(not text.strip() or len(text) > 180 for text in (args.title, args.japanese_title)):
        raise ValueError("Both public titles must be between 1 and 180 characters")
    with tempfile.TemporaryDirectory(prefix=".episode-", dir=ROOT) as temp:
        stage = Path(temp)
        folder = stage / date
        folder.mkdir()
        movie = folder / "lesson.mp4"
        if not 0 < args.video.stat().st_size <= LIMIT:
            raise ValueError("Video exceeds the Cloudflare Pages single-asset limit or is empty")
        shutil.copyfile(args.video, movie)
        if movie.stat().st_size > LIMIT or digest(movie) != args.approved_sha256:
            raise ValueError("The supplied video does not match the approved bytes")
        duration = inspect(movie)
        entry = {"date": date, "title": args.title.strip(), "japaneseTitle": args.japanese_title.strip(),
                 "durationSeconds": duration, "sha256": args.approved_sha256}
        MEDIA.mkdir(exist_ok=True)
        # The directory lock survives atomic catalog replacement and serializes concurrent appends.
        with contextlib.ExitStack() as cleanup:
            directory = os.open(CATALOG.parent, os.O_RDONLY | os.O_DIRECTORY)
            cleanup.callback(os.close, directory)
            fcntl.flock(directory, fcntl.LOCK_EX)
            catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
            previous = next((ep for ep in catalog if ep["date"] == date), None)
            if previous and any(previous.get(key) != value for key, value in entry.items()):
                raise ValueError(f"{date} already has different published metadata or media")
            dest = MEDIA / date
            if dest.exists():
                if (set(p.name for p in dest.iterdir()) != {"lesson.mp4", "poster.webp"}
                        or digest(dest / "lesson.mp4") != args.approved_sha256):
                    raise ValueError(f"Conflicting files at {dest}")
                if previous:
                    if digest(dest / "poster.webp") != previous["posterSha256"]:
                        raise ValueError("The published poster differs from the recorded bytes")
                    return "unchanged"
            subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", str(min(5, duration / 3)),
                "-i", str(movie), "-frames:v", "1", "-vf", "scale=540:-2", "-c:v", "libwebp",
                "-quality", "84", str(folder / "poster.webp")], check=True)
            if (folder / "poster.webp").stat().st_size == 0:
                raise ValueError("Could not produce a poster")
            entry["posterSha256"] = digest(folder / "poster.webp")
            if previous and previous != entry:
                raise ValueError("Poster differs from the published version")
            if dest.exists():
                if digest(dest / "poster.webp") != entry["posterSha256"]:
                    raise ValueError("Staged episode poster differs from the verified movie frame")
            else:
                folder.rename(dest)
            if previous is None:
                catalog.append(entry)
                catalog.sort(key=lambda ep: ep["date"], reverse=True)
                saved = stage / "catalog.json"
                saved.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                saved.replace(CATALOG)
            return "added"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("date", "title", "japanese-title", "approved-sha256"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--video", type=Path, required=True)
    try:
        print(add(parser.parse_args()))
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        sys.exit(str(error))
