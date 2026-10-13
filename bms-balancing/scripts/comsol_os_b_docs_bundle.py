"""COMSOL S1 OS B — Microsoft 공식 문서 사본 묶음 만들기 (경로 (b) · 원장 §92 · 범위 docs/COMSOL_S1_OS_B_DOCS_SCOPE_20261013.json).

    python3 -I bms-balancing/scripts/comsol_os_b_docs_bundle.py bms-balancing/docs/COMSOL_S1_OS_B_DOCS_SCOPE_20261013.json <scratchpad>/os_b_docs/bundle

묶음 (원문 HTML) 은 공개 저장소에 넣지 않는다 — scratchpad 에 만들고 식별 (이름 · 크기 · SHA · MANIFEST SHA) 만 원장 · v2 에 적는다.

항목마다 curl 1 회 (--compressed · -L · 재시도 없음) → 본문 · 응답 헤더 저장 → 원 / 최종 URL · UTC · HTTP 상태 · Content-Type ·
Content-Encoding · 본문 크기 · sha256 · <title> · ms.date · h2 / h3 절을 기록한다. 하나라도 HTTP 200 이 아니거나 <title> 에 기대 이름이 없으면
(오류 · 로그인 화면) 묶음을 만들지 않고 멈춘다. 묶음 zip 은 이름 순 · 고정 시각 (재현용) 이다.
"""
import datetime
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

FIXED_ZIP_TIME = (2026, 10, 13, 0, 0, 0)
BUNDLE_NAME = "COMSOL_S1_OS_B_OFFICIAL_DOCS_20261013.zip"


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def last_header_block(raw: bytes) -> dict:
    blocks = [b for b in raw.replace(b"\r\n", b"\n").split(b"\n\n") if b.strip()]
    hdr = {}
    if blocks:
        for ln in blocks[-1].decode("latin-1").splitlines()[1:]:
            if ":" in ln:
                k, v = ln.split(":", 1)
                hdr[k.strip().lower()] = v.strip()
    return hdr


def main() -> int:
    scope_path, out = Path(sys.argv[1]), Path(sys.argv[2])
    if out.exists():
        raise SystemExit(f"{out} 가 이미 있다")
    scope_b = scope_path.read_bytes()
    scope = json.loads(scope_b)
    (out / "pages").mkdir(parents=True)
    (out / "headers").mkdir()
    recs, bad = [], []
    for it in scope["items"]:
        slug = it["url"].rstrip("/").rsplit("/", 1)[-1]
        body_p, hdr_p = out / "pages" / f"{it['id']}_{slug}.html", out / "headers" / f"{it['id']}.txt"
        t = utc()
        cp = subprocess.run(["curl", "-sS", "--compressed", "-L", "--max-time", "60", "-D", str(hdr_p), "-o", str(body_p),
                             "-w", "%{http_code}\t%{url_effective}\t%{content_type}", it["url"]],
                            capture_output=True, text=True, timeout=90)
        status, final, ctype = (cp.stdout.split("\t") + ["", "", ""])[:3]
        body = body_p.read_bytes() if body_p.exists() else b""
        html = body.decode("utf-8", errors="replace")
        m = re.search(r"<title>(.*?)</title>", html, re.S)
        title = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
        d = re.search(r'<meta\s+name="ms\.date"\s+content="([^"]+)"', html)
        secs = [{"level": lv, "id": i, "text": re.sub(r"<[^>]+>", "", tx).strip()}
                for lv, i, tx in re.findall(r'<h([23])\s+id="([^"]+)"[^>]*>(.*?)</h\1>', html, re.S)]
        hdr = last_header_block(hdr_p.read_bytes()) if hdr_p.exists() else {}
        rec = {"id": it["id"], "category": it["category"], "purpose": it["purpose"], "url_original": it["url"], "url_final": final,
               "fetched_utc": t, "curl_rc": cp.returncode, "curl_stderr": cp.stderr.strip()[:300], "http_status": status,
               "content_type": ctype, "content_encoding": hdr.get("content-encoding"), "body_file": f"pages/{body_p.name}",
               "body_bytes": len(body), "body_sha256": sha(body), "headers_file": f"headers/{hdr_p.name}",
               "title": title, "updated_marker_ms_date": d.group(1) if d else None, "sections": secs,
               "expected_title": it["expect_title"], "expected_title_found": bool(title and it["expect_title"] in title)}
        recs.append(rec)
        if cp.returncode != 0 or status != "200" or not rec["expected_title_found"]:
            bad.append({k: rec[k] for k in ("id", "url_original", "curl_rc", "http_status", "title")})
    manifest = {"schema": "comsol-s1-os-b-docs-bundle-v1", "built_utc_end": utc(), "scope_file": scope_path.name,
                "scope_sha256": sha(scope_b), "body_definition": scope["body_definition"],
                "builder": "Yonghoon-DEM-DFT 클라우드 세션 · curl (agent proxy 경유) · 항목당 1 회 · 재시도 없음",
                "provenance_limit": "sha 는 이 사본의 동일성을 묶을 뿐 Microsoft 진본성이나 OS 지원을 단독으로 증명하지 않는다 (검토 회신)",
                "items": recs, "rejected": bad}
    mb = (json.dumps(manifest, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8")
    (out / "MANIFEST.json").write_bytes(mb)
    if bad:
        print(json.dumps({"ok": False, "rejected": bad}, ensure_ascii=False))
        return 3
    (out / "SCOPE.json").write_bytes(scope_b)
    (out / "BUILD_SCRIPT.py").write_bytes(Path(__file__).read_bytes())
    names = ["MANIFEST.json", "SCOPE.json", "BUILD_SCRIPT.py"] + sorted(r["headers_file"] for r in recs) + sorted(r["body_file"] for r in recs)
    zp = out / BUNDLE_NAME
    with zipfile.ZipFile(zp, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for n in names:
            zi = zipfile.ZipInfo(n, date_time=FIXED_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, (out / n).read_bytes())
    zb = zp.read_bytes()
    print(json.dumps({"ok": True, "bundle": BUNDLE_NAME, "bytes": len(zb), "sha256": sha(zb), "manifest_sha256": sha(mb),
                      "items": len(recs), "entries": len(names)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
