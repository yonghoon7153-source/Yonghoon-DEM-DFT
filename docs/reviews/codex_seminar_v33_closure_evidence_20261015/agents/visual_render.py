"""Independent read-only PDF rendering and page geometry audit.

This does not execute any code from the submitted evidence bundle.
"""
from pathlib import Path
import hashlib
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
import pdfplumber
from PIL import Image, ImageChops

REVIEW = Path(__file__).resolve().parents[1]
PRIOR = REVIEW / "baseline/v32"
OUT = REVIEW / "renders"
OUT.mkdir(parents=True, exist_ok=True)
CURRENT_PDF = REVIEW / "input/deck/seminar_20261013_v33.pdf"
PRIOR_PDF = PRIOR / "deck/seminar_20261013_v32.pdf"
POPPLER = Path("C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def pixel_info(a, b):
    aa, bb = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    result = {"a_size": aa.size, "b_size": bb.size}
    if aa.size != bb.size:
        result["equal"] = False
        return result
    diff = ImageChops.difference(aa, bb)
    result["equal"] = diff.getbbox() is None
    result["changed_bbox"] = diff.getbbox()
    result["changed_pixels"] = sum(1 for p in diff.getdata() if p != (0, 0, 0))
    return result

def render(pdf, prefix):
    subprocess.run([str(POPPLER / "pdftoppm.exe"), "-png", "-r", "144", str(pdf), str(prefix)], check=True)

with ThreadPoolExecutor(max_workers=2) as pool:
    jobs = [pool.submit(render, CURRENT_PDF, OUT / "page"), pool.submit(render, PRIOR_PDF, OUT / "prior-page")]
    for job in jobs:
        job.result()

report = {"renderer": "Poppler pdftoppm 144 dpi", "render_scale": 2,
          "current_pdf_sha256": sha(CURRENT_PDF), "prior_pdf_sha256": sha(PRIOR_PDF),
          "powerpoint_app_checked": False, "pages": []}
current, prior = pdfplumber.open(CURRENT_PDF), pdfplumber.open(PRIOR_PDF)
report["page_counts"] = [len(current.pages), len(prior.pages)]
for i, page in enumerate(current.pages):
    n = i + 1
    p = OUT / f"page-{n:02}.png"
    q = OUT / f"prior-page-{n:02}.png"
    submitted = REVIEW / f"input/png/slide-{n:02}.png"
    oldsubmitted = PRIOR / f"png/slide-{n:02}.png"
    words = page.extract_words()
    chars = [{k: char[k] for k in ["text", "fontname", "size", "x0", "x1", "top", "bottom"]} for char in page.chars]
    row = {"page": n, "rect": [0, 0, page.width, page.height], "text": page.extract_text(),
           "words": words, "chars": chars,
           "out_of_bounds_words": [w for w in words if w["x0"] < 0 or w["top"] < 0 or w["x1"] > page.width or w["bottom"] > page.height],
           "submitted_png_sha256": sha(submitted),
           "prior_submitted_png_sha256": sha(oldsubmitted),
           "submitted_png_byte_equal": submitted.read_bytes() == oldsubmitted.read_bytes(),
           "submitted_png_pixel_compare": pixel_info(submitted, oldsubmitted),
           "independent_pdf_pixel_compare": pixel_info(p, q),
           "independent_render_sha256": sha(p)}
    report["pages"].append(row)
    print(f"Page {n:02}: submitted PNG identical={row['submitted_png_byte_equal']}; actual PDF pixels identical={row['independent_pdf_pixel_compare']['equal']}; out-of-bounds={len(row['out_of_bounds_words'])}")

(REVIEW / "agents/visual_geometry.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
(REVIEW / "agents/visual_text.txt").write_text("\n\n".join(f"PAGE {p['page']}\n{p['text']}" for p in report["pages"]), encoding="utf-8")
print("Complete: all actual PDF pages rendered independently at 144 dpi.")
