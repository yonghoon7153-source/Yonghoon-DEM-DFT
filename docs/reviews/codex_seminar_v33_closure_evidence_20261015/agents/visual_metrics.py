"""Compute audit metrics from already-inspected delivered files; no producer imports."""
from pathlib import Path
import json
import re
import zipfile
from lxml import etree

REVIEW = Path(__file__).resolve().parents[1]
d = json.loads((REVIEW / "agents/visual_geometry.json").read_text(encoding="utf-8"))
ns = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main", "a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
counts = []
with zipfile.ZipFile(REVIEW / "input/deck/seminar_20261013_v33.pptx") as z:
    for n in range(1, 19):
        x = etree.fromstring(z.read(f"ppt/slides/slide{n}.xml"))
        shapes = []
        for s in x.findall("p:cSld/p:spTree/p:sp", ns):
            name = s.find("p:nvSpPr/p:cNvPr", ns).get("name")
            body = s.find("p:txBody", ns)
            if body is None:
                continue
            text = "\n".join("".join(p.xpath(".//a:t/text()", namespaces=ns)) for p in body.findall("a:p", ns)).strip()
            if not text or text in {"HANYANG UNIVERSITY", "Battery Materials Lab."} or re.fullmatch(r"\d+", text) or name in {"TextBox 69", "Credit", "Lit tag", "TextBox 20", "Bridge"}:
                continue
            shapes.append({"name": name, "words": len(text.split()), "text": text})
        counts.append({"page": n, "words": sum(s["words"] for s in shapes), "counted_shapes": shapes})

words3 = d["pages"][2]["words"]
source = [w for w in words3 if 65 < w["top"] < 95]
title = [w for w in words3 if 95 < w["top"] < 115 and w["text"] != "\uf06e"]
summary = {
    "independently_checked_pdf_pages": 18,
    "submitted_png_byte_identical_pages": [p["page"] for p in d["pages"] if p["submitted_png_byte_equal"]],
    "independent_pdf_pixel_identical_pages": [p["page"] for p in d["pages"] if p["independent_pdf_pixel_compare"]["equal"]],
    "changed_render_bounding_boxes_at_144dpi": {str(p["page"]): p["independent_pdf_pixel_compare"]["changed_bbox"] for p in d["pages"] if not p["independent_pdf_pixel_compare"]["equal"]},
    "source_line_bottom_pdf_points": max(w["bottom"] for w in source),
    "title_top_pdf_points": min(w["top"] for w in title),
    "source_title_clearance_pdf_points": min(w["top"] for w in title) - max(w["bottom"] for w in source),
    "source_line_pdf_font_point_sizes": sorted(set(round(c["size"], 3) for c in d["pages"][2]["chars"] if 65<c["top"]<95)),
    "word_counts_by_declared_rule": counts,
    "outside_page_words": sum(len(p["out_of_bounds_words"]) for p in d["pages"]),
    "powerpoint_app_checked": False,
}
(REVIEW / "agents/visual_metrics.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({k:v for k,v in summary.items() if k != "word_counts_by_declared_rule"}, indent=2))
print("Word counts:", [(p["page"], p["words"]) for p in counts if p["page"] in [7,11,15]])
