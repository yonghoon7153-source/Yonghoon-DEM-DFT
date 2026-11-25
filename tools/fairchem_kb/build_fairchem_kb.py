#!/usr/bin/env python3
"""Build a pinned, source-linked Fair-Chem knowledge bundle.

The builder intentionally stores indexes and paraphrased/curated knowledge, not a
copy of the upstream repository.  It uses only the Python standard library so a
future refresh does not depend on Fair-Chem itself being importable.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import tomllib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "fairchem-kb-v1"
OFFICIAL_REPO = "https://github.com/facebookresearch/fairchem"
OFFICIAL_DOCS = "https://fair-chem.github.io/"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _slug(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "item"


def _git(source: Path, *args: str) -> str:
    cmd = [
        "git",
        "-c",
        f"safe.directory={source.as_posix()}",
        "-C",
        str(source),
        *args,
    ]
    proc = subprocess.run(cmd, check=True, capture_output=True)
    return proc.stdout.decode("utf-8", errors="replace")


def _tracked_files(source: Path) -> list[str]:
    raw = _git(source, "ls-files", "-z")
    return sorted(p for p in raw.split("\0") if p)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _first_h1(text: str, fallback: str) -> str:
    for line in text.splitlines():
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            return re.sub(r"[`*_]", "", m.group(1)).strip()
    return fallback


def _headings(text: str) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if m:
            title = re.sub(r"[`*_]", "", m.group(2)).strip()
            result.append(
                {
                    "level": len(m.group(1)),
                    "title": title,
                    "anchor": _slug(title),
                    "line": lineno,
                }
            )
    return result


def _links(text: str) -> tuple[list[str], list[str], list[str]]:
    found = re.findall(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)", text)
    external = sorted({u for u in found if re.match(r"https?://", u)})
    internal = sorted({u for u in found if not re.match(r"(?:https?://|mailto:|#)", u)})
    images = sorted(
        {
            u
            for u in re.findall(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)", text)
        }
    )
    return internal, external, images


def _myst_navigation(myst_path: Path) -> tuple[dict[str, dict[str, Any]], list[dict[str, str]]]:
    """Parse the small subset of MyST YAML used by docs/myst.yml.

    This is deliberately not a general YAML parser.  It records ordered ``file``
    and external ``url`` entries plus the nearest explicit parent title.
    """

    nav: dict[str, dict[str, Any]] = {}
    external: list[dict[str, str]] = []
    stack: list[tuple[int, str]] = []
    order = 0
    pending_external: dict[str, str] | None = None
    in_toc = False
    raw_lines = _read_text(myst_path).splitlines()
    lines: list[str] = []
    skip_next = False
    for idx, raw in enumerate(raw_lines):
        if skip_next:
            skip_next = False
            continue
        if re.match(r"^\s*-\s*file:\s*>-\s*$", raw) and idx + 1 < len(raw_lines):
            indent = len(raw) - len(raw.lstrip(" "))
            lines.append(" " * indent + "- file: " + raw_lines[idx + 1].strip())
            skip_next = True
        else:
            lines.append(raw)
    for raw in lines:
        if raw.strip() == "toc:":
            in_toc = True
            continue
        if in_toc and raw.startswith("site:"):
            break
        if not in_toc:
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()
        title_match = re.match(r"-?\s*title:\s*(.+)$", stripped)
        file_match = re.match(r"-\s*file:\s*(.+)$", stripped)
        url_match = re.match(r"-\s*url:\s*(.+)$", stripped)
        if title_match:
            title = title_match.group(1).strip().strip("'\"")
            while stack and stack[-1][0] >= indent:
                stack.pop()
            stack.append((indent, title))
            if pending_external is not None:
                pending_external["title"] = title
            continue
        if file_match:
            path = file_match.group(1).strip().strip("'\"")
            while stack and stack[-1][0] >= indent:
                stack.pop()
            order += 1
            nav[path] = {
                "nav_order": order,
                "nav_section": stack[-1][1] if stack else "Home",
                "nav_depth": len(stack),
            }
            pending_external = None
            continue
        if url_match:
            order += 1
            pending_external = {
                "url": url_match.group(1).strip().strip("'\""),
                "title": "External link",
                "nav_order": str(order),
            }
            external.append(pending_external)
    return nav, external


def _parse_papers(text: str, source_path: str, source_url: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    category = "Uncategorized"
    papers: list[dict[str, Any]] = []
    for i, line in enumerate(lines):
        h2 = re.match(r"^##\s+(.+?)\s*$", line)
        if h2:
            category = h2.group(1).strip()
            continue
        h3 = re.match(r"^###\s+(.+?)\s*$", line)
        if not h3:
            continue
        title = h3.group(1).strip()
        block: list[str] = []
        j = i + 1
        while j < len(lines) and not re.match(r"^#{2,3}\s+", lines[j]):
            block.append(lines[j])
            j += 1
        joined = "\n".join(block)
        urls = sorted(set(re.findall(r"https?://[^\s)>]+", joined)))
        arxiv = next((u.rstrip(".,") for u in urls if "arxiv.org" in u), None)
        doi = next((u.rstrip(".,") for u in urls if "doi.org" in u), None)
        papers.append(
            {
                "paper_id": f"fc-paper-{_slug(title)}",
                "title": title,
                "category": category,
                "arxiv_url": arxiv,
                "doi_url": doi,
                "all_urls": urls,
                "source_path": source_path,
                "source_url": source_url,
                "status": "official_index_entry",
            }
        )
    return papers


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def _write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fields})


def _resolve_sources(items: list[dict[str, Any]], files_by_path: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for item in items:
        row = dict(item)
        refs: list[dict[str, Any]] = []
        for path in row.pop("source_paths", []):
            if path not in files_by_path:
                raise ValueError(f"Curated source path is not tracked upstream: {path}")
            src = files_by_path[path]
            refs.append(
                {
                    "source_path": path,
                    "source_url": src["source_url"],
                    "sha256": src["sha256"],
                }
            )
        row["sources"] = refs
        enriched.append(row)
    return enriched


def build(source: Path, repo_root: Path, retrieved_at: str | None = None) -> dict[str, Any]:
    source = source.resolve()
    repo_root = repo_root.resolve()
    if not (source / ".git").exists():
        raise FileNotFoundError(f"Not a Git checkout: {source}")
    output = repo_root / "db" / "knowledge" / "fairchem"
    curated_path = repo_root / "tools" / "fairchem_kb" / "curated_knowledge.json"
    live_status_path = repo_root / "tools" / "fairchem_kb" / "live_doc_status.json"
    live_link_audit_path = repo_root / "tools" / "fairchem_kb" / "live_link_audit.json"
    release_observations_path = repo_root / "tools" / "fairchem_kb" / "release_observations.json"
    license_observations_path = repo_root / "tools" / "fairchem_kb" / "license_observations.json"
    curated = json.loads(_read_text(curated_path))
    live_status = {
        row["source_path"]: row for row in json.loads(_read_text(live_status_path))
    }
    live_link_audit = json.loads(_read_text(live_link_audit_path))
    release_observations = json.loads(_read_text(release_observations_path))
    license_observations = json.loads(_read_text(license_observations_path))

    commit = _git(source, "rev-parse", "HEAD").strip()
    commit_time = _git(source, "show", "-s", "--format=%cI", "HEAD").strip()
    commit_subject = _git(source, "show", "-s", "--format=%s", "HEAD").strip()
    tracked = _tracked_files(source)
    if retrieved_at is None:
        retrieved_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    file_rows: list[dict[str, Any]] = []
    for rel in tracked:
        raw = (source / rel).read_bytes()
        suffix = Path(rel).suffix.lower()
        file_rows.append(
            {
                "source_id": f"fc-src-{commit[:8]}-{_slug(rel)}",
                "path": rel,
                "top_level": rel.split("/", 1)[0],
                "extension": suffix or "[none]",
                "bytes": len(raw),
                "sha256": _sha256(raw),
                "source_url": f"{OFFICIAL_REPO}/blob/{commit}/{rel}",
                "raw_url": f"https://raw.githubusercontent.com/facebookresearch/fairchem/{commit}/{rel}",
            }
        )
    by_path = {row["path"]: row for row in file_rows}
    license_observations_resolved: list[dict[str, Any]] = []
    for item in license_observations:
        row = dict(item)
        source_path = row.get("source_path")
        if source_path not in by_path:
            raise ValueError(f"License observation references unknown source: {source_path}")
        row["source_url"] = by_path[source_path]["source_url"]
        row["source_sha256"] = by_path[source_path]["sha256"]
        license_observations_resolved.append(row)

    nav, nav_external = _myst_navigation(source / "docs" / "myst.yml")
    page_rows: list[dict[str, Any]] = []
    for row in file_rows:
        rel = row["path"]
        if not (rel.startswith("docs/") and rel.endswith(".md")):
            continue
        text = _read_text(source / rel)
        doc_rel = rel.removeprefix("docs/")
        headings = _headings(text)
        internal, external, images = _links(text)
        stem = Path(rel).stem.replace("_", "-").lower()
        derived_route = "/" if rel == "docs/index.md" else f"/{stem}/"
        nav_meta = nav.get(doc_rel, {})
        live = live_status.get(rel, {})
        page_rows.append(
            {
                "page_id": f"fc-page-{_slug(rel)}",
                "source_path": rel,
                "title": _first_h1(text, Path(rel).stem),
                "nav_section": nav_meta.get("nav_section", "Unlisted tracked page"),
                "nav_order": nav_meta.get("nav_order"),
                "nav_depth": nav_meta.get("nav_depth"),
                "in_myst_toc": bool(nav_meta),
                "derived_live_url": OFFICIAL_DOCS.rstrip("/") + derived_route,
                "live_url": live.get("live_url"),
                "http_status": live.get("http_status"),
                "content_status": live.get("content_status", "not_live_checked"),
                "webapp_categories": live.get("webapp_categories", []),
                "live_checked_at": live.get("checked_at"),
                "route_status": "live_verified" if live.get("http_status") == 200 else "source_only_orphan",
                "heading_count": len(headings),
                "headings": headings,
                "internal_links": internal,
                "external_links": external,
                "image_refs": images,
                "code_fence_count": text.count("```") // 2,
                "bytes": row["bytes"],
                "sha256": row["sha256"],
                "source_url": row["source_url"],
            }
        )

    packages: list[dict[str, Any]] = []
    for row in file_rows:
        if not row["path"].endswith("pyproject.toml"):
            continue
        data = tomllib.loads(_read_text(source / row["path"]))
        project = data.get("project", {})
        packages.append(
            {
                "package_id": f"fc-package-{_slug(str(project.get('name', row['path'])))}",
                "name": project.get("name"),
                "version": project.get("version"),
                "description": project.get("description"),
                "requires_python": project.get("requires-python"),
                "dependencies": project.get("dependencies", []),
                "optional_dependency_groups": sorted(project.get("optional-dependencies", {}).keys()),
                "scripts": project.get("scripts", {}),
                "source_path": row["path"],
                "source_url": row["source_url"],
                "sha256": row["sha256"],
            }
        )
    packages.sort(key=lambda r: str(r.get("name")))

    model_path = "src/fairchem/core/calculate/pretrained_models.json"
    model_registry = json.loads(_read_text(source / model_path))
    models: list[dict[str, Any]] = []
    for model_id, meta in model_registry.items():
        models.append(
            {
                "model_id": model_id,
                "registry_status": "registered_in_main_snapshot",
                "repo_id": meta.get("repo_id"),
                "filename": meta.get("filename"),
                "subfolder": meta.get("subfolder"),
                "atom_refs": meta.get("atom_refs"),
                "form_elem_refs": meta.get("form_elem_refs"),
                "source_path": model_path,
                "source_url": by_path[model_path]["source_url"],
                "sha256": by_path[model_path]["sha256"],
            }
        )

    papers_path = "docs/core/fair_chemistry_papers.md"
    papers = _parse_papers(
        _read_text(source / papers_path), papers_path, by_path[papers_path]["source_url"]
    )

    curated_outputs: dict[str, list[dict[str, Any]]] = {}
    for key in ("tasks", "datasets", "technologies", "claims", "lpscl_crosswalk", "webapp_seed"):
        curated_outputs[key] = _resolve_sources(curated[key], by_path)

    top_counts = dict(Counter(row["top_level"] for row in file_rows))
    ext_counts = dict(Counter(row["extension"] for row in file_rows))
    snapshot = {
        "schema_version": SCHEMA_VERSION,
        "artifact_id": "fairchem-official-knowledge-snapshot-2026-08-21",
        "status": "official_source_snapshot_with_project_interpretation",
        "official_repo": OFFICIAL_REPO,
        "official_docs": OFFICIAL_DOCS,
        "source_commit": commit,
        "source_commit_time": commit_time,
        "source_commit_subject": commit_subject,
        "retrieved_at": retrieved_at,
        "coverage_contract": {
            "included": [
                "all files tracked by the official repository default-branch snapshot",
                "all tracked Markdown documentation pages and MyST navigation entries",
                "all pyproject package manifests",
                "all code-registered pretrained model records",
                "the official FAIR Chemistry papers index",
                "curated crosswalks that explicitly distinguish official facts from project policy",
            ],
            "excluded": [
                "Git history before the pinned commit",
                "GitHub Issues, Pull Requests, Discussions and unmerged branches",
                "Hugging Face model and dataset payloads",
                "full upstream source-file contents",
                "third-party papers not yet curated into this project",
            ],
            "exhaustive_meaning": "complete tracked-file and current-doc inventory at one pinned official commit, not the full mutable web/GitHub history",
        },
        "counts": {
            "tracked_files": len(file_rows),
            "tracked_docs_markdown_pages": len(page_rows),
            "myst_toc_pages": sum(bool(r["in_myst_toc"]) for r in page_rows),
            "live_docs_http_200": sum(r.get("http_status") == 200 for r in page_rows),
            "source_only_orphan_docs": sum(r.get("content_status") == "source_only_orphan" for r in page_rows),
            "live_docs_with_rendered_execution_error": sum(r.get("content_status") == "rendered_with_execution_error" for r in page_rows),
            "myst_external_links": len(nav_external),
            "packages": len(packages),
            "registered_models": len(models),
            "official_paper_index_entries": len(papers),
            **{f"curated_{key}": len(value) for key, value in curated_outputs.items()},
        },
        "top_level_file_counts": top_counts,
        "extension_counts": ext_counts,
        "myst_external_navigation": nav_external,
    }

    _write_json(output / "snapshot.json", snapshot)
    _write_json(output / "repo_files.json", file_rows)
    _write_csv(
        output / "repo_files.csv",
        file_rows,
        ["source_id", "path", "top_level", "extension", "bytes", "sha256", "source_url", "raw_url"],
    )
    _write_json(output / "site_pages.json", page_rows)
    _write_json(output / "live_link_audit.json", live_link_audit)
    _write_json(output / "release_observations.json", release_observations)
    _write_json(output / "license_observations.json", license_observations_resolved)
    flat_pages = [
        {
            **{k: row.get(k) for k in ("page_id", "source_path", "title", "nav_section", "nav_order", "nav_depth", "in_myst_toc", "derived_live_url", "live_url", "http_status", "content_status", "webapp_categories", "live_checked_at", "route_status", "heading_count", "code_fence_count", "bytes", "sha256", "source_url")},
            "webapp_categories": " | ".join(row.get("webapp_categories", [])),
            "headings": " | ".join(h["title"] for h in row["headings"]),
            "external_link_count": len(row["external_links"]),
            "image_ref_count": len(row["image_refs"]),
        }
        for row in page_rows
    ]
    _write_csv(
        output / "site_pages.csv",
        flat_pages,
        [
            "page_id", "source_path", "title", "nav_section", "nav_order", "nav_depth",
            "in_myst_toc", "derived_live_url", "live_url", "http_status", "content_status", "webapp_categories", "live_checked_at", "route_status", "heading_count", "headings",
            "code_fence_count", "external_link_count", "image_ref_count", "bytes", "sha256", "source_url",
        ],
    )
    _write_json(output / "packages.json", packages)
    _write_json(output / "models.json", models)
    _write_json(output / "papers.json", papers)
    for key, value in curated_outputs.items():
        _write_json(output / f"{key}.json", value)

    return snapshot


def validate(repo_root: Path) -> list[str]:
    repo_root = repo_root.resolve()
    output = repo_root / "db" / "knowledge" / "fairchem"
    errors: list[str] = []
    required = [
        "snapshot.json", "repo_files.json", "repo_files.csv", "site_pages.json", "site_pages.csv", "live_link_audit.json", "release_observations.json", "license_observations.json",
        "packages.json", "models.json", "tasks.json", "datasets.json", "technologies.json",
        "papers.json", "claims.json", "lpscl_crosswalk.json", "webapp_seed.json",
    ]
    for name in required:
        if not (output / name).exists():
            errors.append(f"missing output: {name}")
    if errors:
        return errors

    snapshot = json.loads(_read_text(output / "snapshot.json"))
    files = json.loads(_read_text(output / "repo_files.json"))
    pages = json.loads(_read_text(output / "site_pages.json"))
    if snapshot.get("schema_version") != SCHEMA_VERSION:
        errors.append("snapshot schema_version mismatch")
    if snapshot.get("counts", {}).get("tracked_files") != len(files):
        errors.append("snapshot tracked_files count mismatch")
    if snapshot.get("counts", {}).get("tracked_docs_markdown_pages") != len(pages):
        errors.append("snapshot docs page count mismatch")
    if any(row.get("content_status") == "not_live_checked" for row in pages):
        errors.append("one or more tracked Markdown pages lack live-status audit")
    paths = [row.get("path") for row in files]
    if len(paths) != len(set(paths)):
        errors.append("duplicate repo file paths")
    ids = [row.get("source_id") for row in files]
    if len(ids) != len(set(ids)):
        errors.append("duplicate source IDs")
    known = set(paths)
    for name in ("tasks", "datasets", "technologies", "claims", "lpscl_crosswalk", "webapp_seed"):
        data = json.loads(_read_text(output / f"{name}.json"))
        for item in data:
            if not item.get("sources"):
                errors.append(f"{name}:{item.get(name[:-1] + '_id', item.get('id'))} has no sources")
            for src in item.get("sources", []):
                if src.get("source_path") not in known:
                    errors.append(f"{name} references unknown source {src.get('source_path')}")
                if not re.fullmatch(r"[0-9a-f]{64}", str(src.get("sha256", ""))):
                    errors.append(f"{name} has invalid source hash")
    for row in files:
        if not re.fullmatch(r"[0-9a-f]{64}", str(row.get("sha256", ""))):
            errors.append(f"bad SHA256 for {row.get('path')}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-repo", type=Path, help="Pinned official fairchem checkout")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--retrieved-at", help="ISO timestamp override for deterministic rebuild")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    if not args.validate_only:
        if args.source_repo is None:
            parser.error("--source-repo is required unless --validate-only is used")
        snapshot = build(args.source_repo, args.repo_root, args.retrieved_at)
        print(json.dumps(snapshot["counts"], ensure_ascii=False, sort_keys=True))

    errors = validate(args.repo_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print("Fair-Chem KB validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
