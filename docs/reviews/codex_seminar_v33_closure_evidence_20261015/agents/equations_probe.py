"""Independent read-only OOXML inspection; never imports submitted generators.

Writes only this review's evidence JSON. All inspected PPTX files remain unchanged.
Run with bundled Python and lxml. Relationships, not slide-part numeric names,
determine logical slide numbers. Inclusive and exclusive C14N are both recorded.
"""
from __future__ import annotations

import hashlib
import json
import posixpath
import sys
import zipfile
from pathlib import Path
from lxml import etree as E

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
FILES = {
    "v33": ROOT / "input/deck/seminar_20261013_v33.pptx",
    "v32": ROOT / "input/v32/seminar_20261013_v32.pptx",
    "source": ROOT / "input/source_eq/eq.pptx",
}
EXPECTED_SHA = {
    "v33": "e787298ef657d516f43c8255e80cf1a61bbc52ffe94c6fbfbea57faca14dbb8c",
    "v32": "1b6988f3e55dc6bcf7e81d0ba4ec35b11ed2a0790a1357ba6e6185d22b08f28d",
    "source": "8e76819a9f89516d75c7bd40c529cd65ce055e31a2c8b777d1b8e8edfc669223",
}
UNCHANGED = [1, 2, 4, 6, 8, 9, 10, 12, 14, 16, 17, 18]
EXPECTED_CHANGES = {
    3: ["text", "runs", "notes"],
    5: ["notes"],
    7: ["text", "runs"],
    11: ["text", "runs", "notes", "images"],
    13: ["notes"],
    15: ["text", "runs", "notes"],
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canon(el, exclusive=False):
    return E.tostring(el, method="c14n", exclusive=exclusive)


def jsonsha(data):
    return sha(json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8"))


def target(part, reltarget):
    if reltarget.startswith("/"):
        return reltarget.lstrip("/")
    return posixpath.normpath(posixpath.join(posixpath.dirname(part), reltarget))


def rels(z, part):
    relpart = posixpath.join(posixpath.dirname(part), "_rels", posixpath.basename(part) + ".rels")
    if relpart not in z.namelist():
        return {}
    return {el.get("Id"): {"type": el.get("Type"), "target": target(part, el.get("Target")),
                           "external": el.get("TargetMode") == "External"}
            for el in E.fromstring(z.read(relpart))}


def texts(el):
    return el.xpath(".//a:t/text()", namespaces=NS)


def node_identity(el):
    ids = el.xpath(".//p:cNvPr/@id", namespaces=NS)
    names = el.xpath(".//p:cNvPr/@name", namespaces=NS)
    return {"id": ids[0] if ids else None, "name": names[0] if names else None,
            "xpath": el.getroottree().getpath(el)}


def linked_images(z, element, rm):
    ans = []
    for el in element.xpath(".//a:blip", namespaces=NS):
        rid = el.get("{" + NS["r"] + "}embed")
        if not rid:
            continue
        rel = rm[rid]
        data = z.read(rel["target"])
        ans.append({"xpath": el.getroottree().getpath(el), "rid": rid,
                    "part": rel["target"], "bytes": len(data), "sha256": sha(data)})
    return ans


def inspect(path):
    with zipfile.ZipFile(path) as z:
        pres = E.fromstring(z.read("ppt/presentation.xml"))
        prm = rels(z, "ppt/presentation.xml")
        result = {"path": str(path), "sha256": sha(path.read_bytes()), "slides": []}
        for i, sid in enumerate(pres.findall("p:sldIdLst/p:sldId", NS), 1):
            part = prm[sid.get("{" + NS["r"] + "}id")]["target"]
            raw = z.read(part)
            root = E.fromstring(raw)
            rm = rels(z, part)
            slide = {"logical_slide": i, "part": part, "xml_sha256": sha(raw),
                     "xml_c14n_sha256": sha(canon(root)), "shapes": [],
                     "equations": [], "ordinary_pictures": [], "notes": [],
                     "layout_relationships": [
                         {"rid": rid, "part": rel["target"], "sha256": sha(z.read(rel["target"]))}
                         for rid, rel in rm.items() if rel["type"].endswith("/slideLayout")
                     ]}
            for shape in root.find("p:cSld/p:spTree", NS):
                if E.QName(shape).localname in ("nvGrpSpPr", "grpSpPr"):
                    continue
                runs = shape.xpath(".//a:p/a:r | .//a:p/a:fld | .//a:p/a:br", namespaces=NS)
                slide["shapes"].append({**node_identity(shape), "tag": E.QName(shape).localname,
                    "xml_c14n_sha256": sha(canon(shape)), "text": texts(shape),
                    "run_c14n_sha256": [sha(canon(run)) for run in runs],
                    "paragraph_c14n_sha256": [sha(canon(p)) for p in shape.xpath(".//a:p", namespaces=NS)],
                    "text_nodes": [{"xpath": t.getroottree().getpath(t), "text": t.text,
                                    "codepoints": [ord(c) for c in (t.text or "")]}
                                   for t in shape.xpath(".//a:t", namespaces=NS)],
                    "images": linked_images(z, shape, rm)})
            for ac in root.xpath(".//mc:AlternateContent", namespaces=NS):
                formulas = ac.xpath("./mc:Choice//m:oMathPara", namespaces=NS)
                if not formulas:
                    continue
                choice = ac.find("mc:Choice", NS)
                fallback = ac.find("mc:Fallback", NS)
                for formula in formulas:
                    slide["equations"].append({**node_identity(choice),
                        "omml_xpath": formula.getroottree().getpath(formula),
                        "omml_c14n_sha256": sha(canon(formula)),
                        "omml_exclusive_c14n_sha256": sha(canon(formula, exclusive=True)),
                        "omml_serialized_sha256": sha(E.tostring(formula)),
                        "choice_c14n_sha256": sha(canon(choice)),
                        "alternate_c14n_sha256": sha(canon(ac)),
                        "fallback_xml_c14n_sha256": sha(canon(fallback)),
                        "tokens": formula.xpath(".//m:t/text()", namespaces=NS),
                        "omml_xml": E.tostring(formula, encoding="unicode"),
                        "fallback_images": linked_images(z, fallback, rm)})
            for pic in root.xpath(".//p:pic[not(ancestor::mc:Fallback)]", namespaces=NS):
                slide["ordinary_pictures"].append({**node_identity(pic),
                    "images": linked_images(z, pic, rm)})
            for rid, rel in rm.items():
                if not rel["type"].endswith("/notesSlide"):
                    continue
                nr = z.read(rel["target"])
                nx = E.fromstring(nr)
                slide["notes"].append({"part": rel["target"], "xml_sha256": sha(nr),
                    "xml_c14n_sha256": sha(canon(nx)), "text": texts(nx),
                    "paragraphs": [{"xpath": p.getroottree().getpath(p), "text": texts(p),
                                    "xml_c14n_sha256": sha(canon(p))}
                                   for p in nx.xpath(".//a:p", namespaces=NS)]})
            slide["images"] = linked_images(z, root, rm)
            slide["category_hashes"] = {
                "text": jsonsha([s["text"] for s in slide["shapes"]]),
                "runs": jsonsha([s["run_c14n_sha256"] for s in slide["shapes"]]),
                "notes": jsonsha([n["xml_c14n_sha256"] for n in slide["notes"]]),
                "images": jsonsha([m["sha256"] for m in slide["images"]]),
                "equations": jsonsha([m["omml_c14n_sha256"] for m in slide["equations"]]),
            }
            result["slides"].append(slide)
        result["slide_count"] = len(result["slides"])
        result["package_parts"] = {p: sha(z.read(p)) for p in z.namelist() if not p.endswith("/")}
        return result


def compare_slide(a, b):
    categories = {k: a["category_hashes"][k] == b["category_hashes"][k] for k in a["category_hashes"]}
    diff = {"logical_slide": a["logical_slide"], "v32_part": a["part"], "v33_part": b["part"],
            "xml_bytes_equal": a["xml_sha256"] == b["xml_sha256"],
            "notes_xml_bytes_equal": [n["xml_sha256"] for n in a["notes"]] == [n["xml_sha256"] for n in b["notes"]],
            "layout_relationships_equal": a["layout_relationships"] == b["layout_relationships"],
            "categories_equal": categories, "changed_categories": [k for k,v in categories.items() if not v],
            "shape_changes": [], "notes_changes": [], "image_changes": []}
    sa = {s["id"]: s for s in a["shapes"]}
    sb = {s["id"]: s for s in b["shapes"]}
    for sid in list(dict.fromkeys([*sa, *sb])):
        aa, bb = sa.get(sid), sb.get(sid)
        if aa is None or bb is None:
            diff["shape_changes"].append({"id": sid, "added_or_removed": True, "v32": aa, "v33": bb})
        elif aa["xml_c14n_sha256"] != bb["xml_c14n_sha256"]:
            diff["shape_changes"].append({"id": sid, "name": bb["name"], "xpath": bb["xpath"],
                "v32_text": aa["text"], "v33_text": bb["text"],
                "text_equal": aa["text"] == bb["text"],
                "runs_equal": aa["run_c14n_sha256"] == bb["run_c14n_sha256"],
                "paragraphs_equal": aa["paragraph_c14n_sha256"] == bb["paragraph_c14n_sha256"],
                "v32_images": aa["images"], "v33_images": bb["images"]})
    for na, nb in zip(a["notes"], b["notes"]):
        if na["xml_c14n_sha256"] != nb["xml_c14n_sha256"]:
            diff["notes_changes"].append({"v32_part": na["part"], "v33_part": nb["part"],
                "v32_text": na["text"], "v33_text": nb["text"],
                "v32_paragraphs": na["paragraphs"], "v33_paragraphs": nb["paragraphs"]})
    for aa, bb in zip(a["images"], b["images"]):
        if aa["sha256"] != bb["sha256"]:
            diff["image_changes"].append({"v32": aa, "v33": bb})
    return diff


decks = {name: inspect(path) for name, path in FILES.items()}
comparison = [compare_slide(a,b) for a,b in zip(decks["v32"]["slides"], decks["v33"]["slides"])]
dest = decks["v33"]["slides"][2]
old = decks["v32"]["slides"][2]
source_slides = [s for s in decks["source"]["slides"] if s["equations"]]
assert len(source_slides) == 1, "Expected exactly one source equation slide; inspect manually if different"
source = source_slides[0]
source_eq = {e["name"]: e for e in source["equations"]}
old_eq = {e["name"]: e for e in old["equations"]}
eq_matches = []
for e in dest["equations"]:
    ss, oo = source_eq.get(e["name"]), old_eq.get(e["name"])
    assert ss is not None and oo is not None, e["name"]
    eq_matches.append({"name": e["name"], "destination_xpath": e["omml_xpath"],
        "source_xpath": ss["omml_xpath"], "source_part": source["part"],
        "omml_c14n_sha256": e["omml_c14n_sha256"],
        "source_c14n_equal": ss["omml_c14n_sha256"] == e["omml_c14n_sha256"],
        "source_exclusive_c14n_equal": ss["omml_exclusive_c14n_sha256"] == e["omml_exclusive_c14n_sha256"],
        "source_serialized_equal": ss["omml_serialized_sha256"] == e["omml_serialized_sha256"],
        "source_tokens_equal": ss["tokens"] == e["tokens"],
        "source_fallback_equal": [x["sha256"] for x in ss["fallback_images"]] == [x["sha256"] for x in e["fallback_images"]],
        "v32_omml_c14n_equal": oo["omml_c14n_sha256"] == e["omml_c14n_sha256"],
        "v32_omml_serialized_equal": oo["omml_serialized_sha256"] == e["omml_serialized_sha256"],
        "v32_entire_alternate_content_c14n_equal": oo["alternate_c14n_sha256"] == e["alternate_c14n_sha256"],
        "v32_native_choice_c14n_equal": oo["choice_c14n_sha256"] == e["choice_c14n_sha256"],
        "v32_fallback_xml_equal": oo["fallback_xml_c14n_sha256"] == e["fallback_xml_c14n_sha256"],
        "v32_fallback_equal": [x["sha256"] for x in oo["fallback_images"]] == [x["sha256"] for x in e["fallback_images"]],
        "fallback_sha256": [x["sha256"] for x in e["fallback_images"]]})

source_pics = [x["sha256"] for p in source["ordinary_pictures"] for x in p["images"]]
dest_pics = [x["sha256"] for p in dest["ordinary_pictures"] for x in p["images"]]
different_parts = sorted(p for p in set(decks["v32"]["package_parts"]) | set(decks["v33"]["package_parts"])
                         if decks["v32"]["package_parts"].get(p) != decks["v33"]["package_parts"].get(p))
style_prefixes = ("ppt/theme/", "ppt/slideMasters/", "ppt/slideLayouts/", "ppt/notesMasters/", "ppt/handoutMasters/", "ppt/fonts/")
style_names = ("ppt/presentation.xml", "ppt/presProps.xml", "ppt/viewProps.xml", "ppt/tableStyles.xml", "ppt/fontTable.xml")
style_parts = sorted(p for p in set(decks["v32"]["package_parts"]) | set(decks["v33"]["package_parts"])
                     if p.startswith(style_prefixes) or p in style_names or p.endswith((".fntdata", ".odttf")))
style_comparison = [{"part": p, "v32_sha256": decks["v32"]["package_parts"].get(p),
                     "v33_sha256": decks["v33"]["package_parts"].get(p),
                     "equal": decks["v32"]["package_parts"].get(p) == decks["v33"]["package_parts"].get(p)}
                    for p in style_parts]
source_line = next(s for s in dest["shapes"] if s["id"] == "70")
note_text = "\n".join(t for n in dest["notes"] for t in n["text"])
visible_text = "\n".join(t for s in dest["shapes"] for t in s["text"])
semantic_checks = {
    "source_shape_id": "70", "source_shape_xpath": source_line["xpath"],
    "source_paragraphs": source_line["text"],
    "source_paragraph_character_counts": [len(t) for t in source_line["text"]],
    "old_implemented_equations_phrase_absent": "implemented equations" not in visible_text + note_text,
    "representative_visible": "representative equations based on LIGGGHTS-PUBLIC 3.8.0" in visible_text,
    "small_overlap_visible": "Equation ② uses the small-overlap approximation ℓᵢⱼ ≈ Rᵢnᵢⱼ." in visible_text,
    "notes_representative": "representative equations based on the LIGGGHTS-PUBLIC 3.8.0" in note_text,
    "notes_small_overlap": "equation ② uses the small-overlap approximation ℓᵢⱼ ≈ Rᵢnᵢⱼ" in note_text,
    "notes_implemented_magnitude": "implemented lever arm has magnitude Rᵢ − δᵢⱼ/2" in note_text,
    "notes_cdt_zero": "CDT rolling torque is zero when the relative angular velocity is zero" in note_text,
    "notes_cdt_positive_norm_and_torsion_off": "used only for ‖ω_r‖ > 0" in note_text and "torsion torque off" in note_text,
    "unicode_subscript_j": {"character": "ⱼ", "codepoint": "U+2C7C", "decimal": ord("ⱼ")},
    "inherited_omml_em_spaces": [{"name": e["name"], "tokens": [{"text": t, "codepoints": [ord(c) for c in t]}
                                                             for t in e["tokens"] if chr(0x2003) in t]}
                                 for e in dest["equations"] if any(chr(0x2003) in t for t in e["tokens"])],
}
upstream = ROOT / "baseline/upstream"
source_code_checks = []
for fname, ranges in [("surface_model_default.h", [(173,188)]),
                      ("tangential_model_history.h", [(254,261)]),
                      ("rolling_model_cdt.h", [(91,94),(133,157)])]:
    fp = upstream / fname
    data = fp.read_bytes()
    lines = data.decode("utf-8").splitlines()
    source_code_checks.append({"path": str(fp), "sha256": sha(data),
        "previous_review_pinned_commit": "3d5c00f20519e6bb6eb6756f51f1ad36564e649d",
        "line_ranges": [{"start": a, "end": b, "lines": [{"line": n, "text": lines[n-1]}
                                                             for n in range(a,b+1)]}
                        for a,b in ranges]})
summary = {
    "file_sha256_matches_request": {k: d["sha256"] == EXPECTED_SHA[k] for k,d in decks.items()},
    "slide_counts": {k:d["slide_count"] for k,d in decks.items()},
    "all_12_unchanged_slides_category_equal": all(all(comparison[i-1]["categories_equal"].values()) for i in UNCHANGED),
    "all_12_unchanged_slides_xml_byte_equal": all(comparison[i-1]["xml_bytes_equal"] for i in UNCHANGED),
    "all_12_unchanged_notes_xml_byte_equal": all(comparison[i-1]["notes_xml_bytes_equal"] for i in UNCHANGED),
    "all_18_layout_relationships_equal": all(c["layout_relationships_equal"] for c in comparison),
    "global_style_resource_count": len(style_comparison),
    "global_style_resources_all_byte_equal": all(c["equal"] for c in style_comparison),
    "embedded_font_part_count": sum(p.startswith("ppt/fonts/") or p.endswith((".fntdata", ".odttf")) for p in style_parts),
    "changed_categories_match_requested_6_slots": all(c["changed_categories"] == EXPECTED_CHANGES.get(c["logical_slide"], []) for c in comparison),
    "equation_counts": {"source":len(source["equations"]), "v32":len(old["equations"]), "v33":len(dest["equations"])},
    "source_8_omml_c14n_equal": len(eq_matches) == 8 and all(e["source_c14n_equal"] for e in eq_matches),
    "source_8_fallback_media_equal": len(eq_matches) == 8 and all(e["source_fallback_equal"] for e in eq_matches),
    "source_2_ordinary_images_equal_ordered": len(dest_pics) == len(source_pics) == 2 and source_pics == dest_pics,
    "v32_native_choice_8_preserved": len(eq_matches) == 8 and all(e["v32_native_choice_c14n_equal"] for e in eq_matches),
    "v32_omml_serialized_8_equal": len(eq_matches) == 8 and all(e["v32_omml_serialized_equal"] for e in eq_matches),
    "v32_entire_alternate_content_8_preserved": len(eq_matches) == 8 and all(e["v32_entire_alternate_content_c14n_equal"] for e in eq_matches),
    "source_equation_slide": {"logical_slide": source["logical_slide"], "part": source["part"]},
    "destination_equation_slide": {"logical_slide": dest["logical_slide"], "part": dest["part"]},
    "package_part_differences": different_parts,
    "powerpoint_render_performed": False,
}
out = {"method": __doc__, "summary": summary, "equation_matches": eq_matches,
       "slide3_semantic_checks": semantic_checks,
       "local_pinned_source_code_checks": source_code_checks,
       "global_style_comparison": style_comparison,
       "source_picture_sha256": source_pics, "v33_picture_sha256": dest_pics,
       "slide_comparison": comparison, "decks": decks}
outpath = ROOT / "agents/equations_probe.json"
outpath.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))
print("CHANGED SLOTS")
for c in comparison:
    if c["changed_categories"]:
        print(c["logical_slide"], c["v33_part"], c["changed_categories"])
        for ss in c["shape_changes"]:
            print(" ", ss["id"], ss.get("name", "added/removed shape"), ss.get("v32_text"), "=>", ss.get("v33_text"))
print("SLIDE 3 NOTES")
for n in dest["notes"]:
    print(n["part"])
    for p in n["paragraphs"]:
        if p["text"]:
            print(p["xpath"], json.dumps(p["text"], ensure_ascii=False))
print("Evidence:", outpath)
