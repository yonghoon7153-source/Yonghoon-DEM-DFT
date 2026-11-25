#!/usr/bin/env python3
"""pc_img.py — 이미지 파일 검사 도우미 (표준 라이브러리만 · 초안 · 2026-11-25).

PhotoCraft 가 만든 결과를 *PhotoCraft 밖에서* 확인한다.  그림 픽셀을 바꾸는 일은 하지 않는다
(strip 은 메타데이터 덩어리만 빼고 픽셀 바이트는 그대로 복사한다).

하위 명령
  meta    FILE...              메타데이터 덩어리 목록 (PNG · JPEG · TIFF · WebP) + 공개 안전 판정
  strip   IN OUT               PNG · JPEG 의 메타데이터 덩어리를 뺀 새 파일 (IN 은 건드리지 않음)
  pixhash FILE                 PNG 픽셀 바이트의 sha256 (메타데이터 · 압축 차이와 무관)
  pointop IN.png OUT.png       '전체에 같은 점 연산' 검사: 출력 값이 같은 자리 입력 값만의 함수인가
                               (+ 선형 맞춤 잔차).  --offset DX,DY = 출력 (x,y) 가 입력 (x+DX, y+DY)

종료 코드: 0 = 통과 · 1 = 걸림 (공개 안전 아님 / 점 연산 아님 / 비선형) · 2 = 읽을 수 없음 · 지원 안 함.

⚠ 이 파일은 초안이다 — 이 환경에서는 문법 검사 (py_compile) 만 했고 실제 그림으로 돌려 보지 않았다.
⚠ 입력 그림은 믿지 않는 자료로 다룬다: 크기 상한 (--max-mb, 기본 400) 을 넘으면 읽지 않는다.
⚠ 순수 파이썬이라 느리다 — 2000 × 1500 회색 8 비트 PNG 기준 수 초 ~ 수십 초 [추정].
  pointop 은 PNG (인터레이스 아님 · 8 / 16 비트 · 팔레트 아님) 만 읽는다.  TIFF 원본은 먼저
  PhotoCraft 로 PNG 로 바꾼 사본 (convert · 기록) 과 비교한다.
"""
import array
import hashlib
import json
import struct
import sys
import zlib

PNG_SIG = b"\x89PNG\r\n\x1a\n"
# 색 · 해상도에 필요한 보조 청크 (strip 이 남기는 것).  그 밖의 보조 청크는 뺀다.
PNG_KEEP_ANCILLARY = {b"tRNS", b"gAMA", b"cHRM", b"sRGB", b"iCCP", b"pHYs", b"sBIT"}
PNG_PRIVATE = {b"tEXt", b"zTXt", b"iTXt", b"eXIf", b"tIME"}

# TIFF / EXIF 태그 — 사생활 · 출처 정보가 될 수 있는 것.
TIFF_TAGS = {
    270: "ImageDescription", 271: "Make", 272: "Model", 305: "Software", 306: "DateTime",
    315: "Artist", 316: "HostComputer", 700: "XMP", 33432: "Copyright", 33723: "IPTC",
    34377: "Photoshop", 34665: "ExifIFD", 34675: "ICCProfile", 34853: "GPSInfo",
    # 현미경 회사 태그 — 번호는 tifffile 태그 표 기억에 따른 것 [추정 · 원문 대조 전]
    34118: "CZ_SEM (Zeiss SEM)", 34680: "FEI_SFEG", 34682: "FEI_HELIOS",
    50838: "ImageJMetaDataByteCounts", 50839: "ImageJMetaData",
}
TIFF_PRIVATE = {270, 271, 272, 305, 306, 315, 316, 700, 33432, 33723, 34377, 34665, 34853,
                34118, 34680, 34682, 50838, 50839}
TIFF_TYPE_SIZE = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 6: 1, 7: 1, 8: 2, 9: 4, 10: 8, 11: 4, 12: 8, 13: 4,
                  16: 8, 17: 8, 18: 8}


class Unsupported(Exception):
    pass


def read_file(path, max_mb):
    with open(path, "rb") as f:
        f.seek(0, 2)
        size = f.tell()
        if size > max_mb * 1024 * 1024:
            raise Unsupported("%s: %d MB > --max-mb %d" % (path, size // (1024 * 1024), max_mb))
        f.seek(0)
        return f.read()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def short(b, n=80):
    s = b.decode("latin-1", "replace")
    s = "".join(ch if 32 <= ord(ch) < 127 else "." for ch in s)
    return s[:n] + ("…" if len(s) > n else "")


# --------------------------------------------------------------------------------------------
# PNG
# --------------------------------------------------------------------------------------------
def png_chunks(data):
    """(type, body, start, end) — start/end 는 청크 전체 (길이·형식·본문·CRC) 의 바이트 자리."""
    if data[:8] != PNG_SIG:
        raise Unsupported("PNG 서명이 아니다")
    pos, n = 8, len(data)
    while pos + 12 <= n:
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        body_end = pos + 8 + length
        if body_end + 4 > n:
            raise Unsupported("잘린 PNG 청크 %r" % ctype)
        body = data[pos + 8:body_end]
        crc = struct.unpack(">I", data[body_end:body_end + 4])[0]
        if zlib.crc32(ctype + body) & 0xFFFFFFFF != crc:
            raise Unsupported("PNG 청크 %r CRC 불일치" % ctype)
        yield ctype, body, pos, body_end + 4
        pos = body_end + 4
        if ctype == b"IEND":
            break


def png_decode(data):
    ihdr, idat, plte, trns = None, [], None, None
    for ctype, body, _s, _e in png_chunks(data):
        if ctype == b"IHDR":
            ihdr = struct.unpack(">IIBBBBB", body)
        elif ctype == b"IDAT":
            idat.append(body)
        elif ctype == b"PLTE":
            plte = body
        elif ctype == b"tRNS":
            trns = body
    if ihdr is None:
        raise Unsupported("IHDR 없음")
    width, height, bit, ctype, _comp, _filt, interlace = ihdr
    if interlace != 0:
        raise Unsupported("Adam7 인터레이스 PNG 는 지원하지 않음")
    if bit not in (8, 16):
        raise Unsupported("비트 깊이 %d 는 지원하지 않음 (8 · 16 만)" % bit)
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(ctype)
    if channels is None:
        raise Unsupported("색 형식 %d" % ctype)
    bpp = channels * bit // 8
    rowbytes = width * bpp
    raw = zlib.decompress(b"".join(idat))
    if len(raw) < height * (rowbytes + 1):
        raise Unsupported("IDAT 길이가 모자람")
    out = bytearray(height * rowbytes)
    prev = bytearray(rowbytes)
    pos = 0
    for y in range(height):
        f = raw[pos]
        line = bytearray(raw[pos + 1:pos + 1 + rowbytes])
        pos += rowbytes + 1
        if f == 0:
            pass
        elif f == 1:
            for i in range(bpp, rowbytes):
                line[i] = (line[i] + line[i - bpp]) & 0xFF
        elif f == 2:
            line = bytearray((a + b) & 0xFF for a, b in zip(line, prev))
        elif f == 3:
            for i in range(rowbytes):
                left = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif f == 4:
            for i in range(rowbytes):
                a = line[i - bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i - bpp] if i >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                if pa <= pb and pa <= pc:
                    pr = a
                elif pb <= pc:
                    pr = b
                else:
                    pr = c
                line[i] = (line[i] + pr) & 0xFF
        else:
            raise Unsupported("PNG 필터 %d" % f)
        out[y * rowbytes:(y + 1) * rowbytes] = line
        prev = line
    return {"width": width, "height": height, "bit": bit, "ctype": ctype, "channels": channels,
            "rowbytes": rowbytes, "data": bytes(out), "plte": plte, "trns": trns}


def png_row_samples(img, y):
    """한 줄의 표본: 8 비트 = bytes, 16 비트 = array('H') (큰 끝 → 이 기계 순서)."""
    rb = img["rowbytes"]
    row = img["data"][y * rb:(y + 1) * rb]
    if img["bit"] == 8:
        return row
    arr = array.array("H")
    arr.frombytes(row)
    if sys.byteorder == "little":
        arr.byteswap()
    return arr


def png_color_channels(ctype):
    return {0: [0], 2: [0, 1, 2], 3: [0], 4: [0], 6: [0, 1, 2]}[ctype]


def png_alpha_channel(ctype):
    return {4: 1, 6: 3}.get(ctype)


def pixel_hash(img):
    h = hashlib.sha256()
    h.update(struct.pack(">IIBB", img["width"], img["height"], img["bit"], img["ctype"]))
    if img["plte"]:
        h.update(img["plte"])
    if img["trns"]:
        h.update(img["trns"])
    h.update(img["data"])
    return h.hexdigest()


# --------------------------------------------------------------------------------------------
# TIFF (EXIF 안의 TIFF 구조 포함)
# --------------------------------------------------------------------------------------------
def tiff_scan(data, base=0, label="TIFF"):
    found = []
    bo = data[base:base + 2]
    if bo == b"II":
        e = "<"
    elif bo == b"MM":
        e = ">"
    else:
        raise Unsupported("%s: 바이트 순서 표지가 아님" % label)
    magic = struct.unpack(e + "H", data[base + 2:base + 4])[0]
    if magic == 43:
        raise Unsupported("%s: BigTIFF 는 지원하지 않음" % label)
    if magic != 42:
        raise Unsupported("%s: TIFF 표지 42 가 아님" % label)
    off = struct.unpack(e + "I", data[base + 4:base + 8])[0]
    seen, ifd_no = set(), 0
    while off and off not in seen and ifd_no < 64:
        seen.add(off)
        p = base + off
        if p + 2 > len(data):
            break
        count = struct.unpack(e + "H", data[p:p + 2])[0]
        for i in range(count):
            q = p + 2 + 12 * i
            if q + 12 > len(data):
                break
            tag, typ, cnt = struct.unpack(e + "HHI", data[q:q + 8])
            if tag not in TIFF_TAGS:
                continue
            size = TIFF_TYPE_SIZE.get(typ, 1) * cnt
            if size <= 4:
                val = data[q + 8:q + 8 + size]
            else:
                voff = struct.unpack(e + "I", data[q + 8:q + 12])[0]
                val = data[base + voff:base + voff + min(size, 4096)]
            preview = short(val) if typ in (1, 2, 7) else "(형식 %d · 개수 %d)" % (typ, cnt)
            found.append({"where": "%s IFD%d" % (label, ifd_no), "tag": tag, "name": TIFF_TAGS[tag],
                          "private": tag in TIFF_PRIVATE, "preview": preview})
        nxt = p + 2 + 12 * count
        off = struct.unpack(e + "I", data[nxt:nxt + 4])[0] if nxt + 4 <= len(data) else 0
        ifd_no += 1
    return found


# --------------------------------------------------------------------------------------------
# JPEG
# --------------------------------------------------------------------------------------------
def jpeg_segments(data):
    """(marker, start, end, payload_start) — 엔트로피 부호 구간은 marker None."""
    if data[:2] != b"\xff\xd8":
        raise Unsupported("JPEG SOI 가 아님")
    yield (0xD8, 0, 2, 2)
    pos, n = 2, len(data)
    while pos < n:
        if data[pos] != 0xFF:
            raise Unsupported("JPEG 표지 자리 %d 에 0xFF 가 없음" % pos)
        while pos < n and data[pos] == 0xFF:
            pos += 1
        if pos >= n:
            break
        m = data[pos]
        start = pos - 1
        pos += 1
        if m == 0xD9:
            yield (m, start, pos, pos)
            break
        if 0xD0 <= m <= 0xD7 or m == 0x01:
            yield (m, start, pos, pos)
            continue
        if pos + 2 > n:
            raise Unsupported("잘린 JPEG 구간")
        length = struct.unpack(">H", data[pos:pos + 2])[0]
        end = pos + length
        if end > n:
            raise Unsupported("잘린 JPEG 구간 0x%02X" % m)
        yield (m, start, end, pos + 2)
        pos = end
        if m == 0xDA:
            ecs = pos
            while True:
                k = data.find(b"\xff", pos)
                if k < 0 or k + 1 >= n:
                    pos = n
                    break
                nx = data[k + 1]
                if nx == 0x00 or 0xD0 <= nx <= 0xD7:
                    pos = k + 2
                    continue
                if nx == 0xFF:
                    pos = k + 1
                    continue
                pos = k
                break
            yield (None, ecs, pos, ecs)


def jpeg_meta(data):
    found = []
    for m, s, e, p in jpeg_segments(data):
        if m is None:
            continue
        payload = data[p:e]
        if m == 0xE1 and payload.startswith(b"Exif\x00\x00"):
            found.append({"what": "APP1 Exif", "bytes": len(payload), "private": True})
            try:
                found.extend(tiff_scan(data, p + 6, "Exif"))
            except Unsupported as exc:
                found.append({"what": "Exif 해석 실패", "detail": str(exc), "private": True})
        elif m == 0xE1:
            found.append({"what": "APP1 (XMP 등)", "bytes": len(payload), "private": True,
                          "preview": short(payload[:40])})
        elif m == 0xE2 and payload.startswith(b"ICC_PROFILE\x00"):
            found.append({"what": "APP2 ICC", "bytes": len(payload), "private": False})
        elif 0xE2 <= m <= 0xEF and m != 0xEE:
            found.append({"what": "APP%d" % (m - 0xE0), "bytes": len(payload), "private": m != 0xE0,
                          "preview": short(payload[:24])})
        elif m == 0xEE:
            found.append({"what": "APP14 Adobe", "bytes": len(payload), "private": False})
        elif m == 0xE0:
            found.append({"what": "APP0 JFIF", "bytes": len(payload), "private": False})
        elif m == 0xFE:
            found.append({"what": "COM 주석", "bytes": len(payload), "private": True, "preview": short(payload)})
    return found


def jpeg_strip(data):
    out = bytearray()
    for m, s, e, p in jpeg_segments(data):
        payload = data[p:e]
        drop = (m == 0xE1) or (m == 0xFE) or (m is not None and 0xE3 <= m <= 0xED) or (m == 0xEF) \
            or (m == 0xE2 and not payload.startswith(b"ICC_PROFILE\x00"))
        if not drop:
            out += data[s:e]
    return bytes(out)


# --------------------------------------------------------------------------------------------
# WebP
# --------------------------------------------------------------------------------------------
def webp_meta(data):
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise Unsupported("WebP RIFF 가 아님")
    found, pos = [], 12
    while pos + 8 <= len(data):
        fourcc = data[pos:pos + 4]
        size = struct.unpack("<I", data[pos + 4:pos + 8])[0]
        if fourcc in (b"EXIF", b"XMP "):
            found.append({"what": fourcc.decode("ascii").strip(), "bytes": size, "private": True})
        elif fourcc == b"ICCP":
            found.append({"what": "ICCP", "bytes": size, "private": False})
        pos += 8 + size + (size & 1)
    return found


# --------------------------------------------------------------------------------------------
# meta / strip
# --------------------------------------------------------------------------------------------
def png_meta(data):
    found = []
    for ctype, body, _s, _e in png_chunks(data):
        name = ctype.decode("latin-1")
        if ctype == b"tEXt":
            key, _, val = body.partition(b"\x00")
            found.append({"what": "tEXt", "key": short(key), "preview": short(val), "private": True})
        elif ctype == b"zTXt":
            key, _, rest = body.partition(b"\x00")
            try:
                val = zlib.decompress(rest[1:])
            except zlib.error:
                val = b"(decompress failed)"
            found.append({"what": "zTXt", "key": short(key), "preview": short(val), "private": True})
        elif ctype == b"iTXt":
            key, _, rest = body.partition(b"\x00")
            comp = rest[:1] == b"\x01"
            text = rest[2:].split(b"\x00", 2)[-1] if len(rest) > 2 else b""
            if comp:
                try:
                    text = zlib.decompress(text)
                except zlib.error:
                    text = b"(decompress failed)"
            found.append({"what": "iTXt", "key": short(key), "preview": short(text), "private": True})
        elif ctype == b"eXIf":
            found.append({"what": "eXIf", "bytes": len(body), "private": True})
            try:
                found.extend(tiff_scan(body, 0, "eXIf"))
            except Unsupported as exc:
                found.append({"what": "eXIf 해석 실패", "detail": str(exc), "private": True})
        elif ctype == b"tIME":
            found.append({"what": "tIME", "preview": "%04d-%02d-%02d %02d:%02d:%02d" % struct.unpack(">HBBBBB", body),
                          "private": True})
        elif ctype == b"iCCP":
            found.append({"what": "iCCP", "key": short(body.partition(b"\x00")[0]), "private": False})
        elif ctype == b"pHYs":
            ppx, ppy, unit = struct.unpack(">IIB", body)
            dpi = round(ppx * 0.0254, 2) if unit == 1 else None
            found.append({"what": "pHYs", "preview": "%s dpi" % dpi if dpi else "단위 없음", "private": False})
        elif not (65 <= ctype[0] <= 90) and ctype not in PNG_KEEP_ANCILLARY:
            found.append({"what": "보조 청크 " + name, "bytes": len(body), "private": True})
    return found


def detect(data):
    if data[:8] == PNG_SIG:
        return "png"
    if data[:2] == b"\xff\xd8":
        return "jpeg"
    if data[:4] in (b"II*\x00", b"MM\x00*", b"II+\x00", b"MM\x00+"):
        return "tiff"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    return None


def meta_report(path, max_mb):
    data = read_file(path, max_mb)
    kind = detect(data)
    if kind == "png":
        items = png_meta(data)
    elif kind == "jpeg":
        items = jpeg_meta(data)
    elif kind == "tiff":
        items = tiff_scan(data, 0, "TIFF")
    elif kind == "webp":
        items = webp_meta(data)
    else:
        raise Unsupported("%s: 알 수 없는 형식" % path)
    private = [i for i in items if i.get("private")]
    gps = any(i.get("tag") == 34853 for i in items)
    return {"file": path, "format": kind, "sha256": sha256_bytes(data), "bytes": len(data),
            "items": items, "public_safe": not private, "gps": gps}


def strip_file(src, dst, max_mb):
    data = read_file(src, max_mb)
    kind = detect(data)
    if kind == "png":
        out = bytearray(PNG_SIG)
        for ctype, _body, s, e in png_chunks(data):
            critical = 65 <= ctype[0] <= 90
            if critical or ctype in PNG_KEEP_ANCILLARY:
                out += data[s:e]
        out = bytes(out)
        same_pixels = pixel_hash(png_decode(data)) == pixel_hash(png_decode(out))
    elif kind == "jpeg":
        out = jpeg_strip(data)
        same_pixels = None  # 엔트로피 부호 구간을 그대로 복사했다 (디코딩 비교는 하지 않음)
    else:
        raise Unsupported("strip 은 PNG · JPEG 만")
    if src == dst:
        raise Unsupported("IN 과 OUT 이 같다 — 새 파일로만 쓴다")
    with open(dst, "xb") as f:
        f.write(out)
    return {"in": src, "in_sha256": sha256_bytes(data), "out": dst, "out_sha256": sha256_bytes(out),
            "removed_bytes": len(data) - len(out), "same_pixels": same_pixels}


# --------------------------------------------------------------------------------------------
# pointop
# --------------------------------------------------------------------------------------------
def affine_fit(lut, lo, hi):
    """(in → out) 짝에서 잘림 끝 (out == lo 또는 hi) 을 뺀 최소제곱 직선과 최대 잔차."""
    pts = [(x, y) for x, y in lut.items() if lo < y < hi]
    if len(pts) < 3:
        pts = list(lut.items())
    n = len(pts)
    if n < 2:
        return {"slope": None, "intercept": None, "max_residual": 0.0, "points": n}
    mx = sum(x for x, _ in pts) / n
    my = sum(y for _, y in pts) / n
    sxx = sum((x - mx) ** 2 for x, _ in pts)
    if sxx == 0:
        return {"slope": None, "intercept": my, "max_residual": 0.0, "points": n}
    a = sum((x - mx) * (y - my) for x, y in pts) / sxx
    b = my - a * mx
    res = max(abs(y - (a * x + b)) for x, y in pts)
    return {"slope": round(a, 6), "intercept": round(b, 4), "max_residual": round(res, 4), "points": n}


def pointop(in_path, out_path, offset, max_mb, tol=None):
    """tol = 선형 맞춤 최대 잔차 문턱 (출력 단위).  None 이면 8 비트 1.01 · 16 비트 8.0 (8 비트 0.03 단계)."""
    a = png_decode(read_file(in_path, max_mb))
    b = png_decode(read_file(out_path, max_mb))
    if tol is None:
        tol = 1.01 if b["bit"] == 8 else 8.0
    if a["ctype"] == 3 or b["ctype"] == 3:
        raise Unsupported("팔레트 PNG 는 지원하지 않음")
    ca, cb = png_color_channels(a["ctype"]), png_color_channels(b["ctype"])
    if len(ca) == len(cb):
        pairs = list(zip(ca, cb))
    elif len(ca) == 1 and len(cb) == 3:
        pairs = [(ca[0], c) for c in cb]
    else:
        raise Unsupported("채널 수가 맞지 않음 (%d → %d)" % (len(ca), len(cb)))
    dx, dy = offset
    luts = [dict() for _ in pairs]
    conflicts = [0] * len(pairs)
    examples = []
    margin, margin_vals = 0, set()
    na, nb = a["channels"], b["channels"]
    alpha_b = png_alpha_channel(b["ctype"])
    full = (1 << b["bit"]) - 1
    not_opaque = 0
    for y in range(b["height"]):
        rb = png_row_samples(b, y)
        if alpha_b is not None:
            not_opaque += sum(1 for v in rb[alpha_b::nb] if v != full)
        yi = y + dy
        if yi < 0 or yi >= a["height"]:
            margin += b["width"]
            margin_vals.update(rb[cb[0]::nb][:64])
            continue
        ra = png_row_samples(a, yi)
        x0 = max(0, -dx)
        x1 = min(b["width"], a["width"] - dx)
        if x1 <= x0:
            margin += b["width"]
            continue
        margin += x0 + (b["width"] - x1)
        if x0 > 0:
            margin_vals.update(rb[cb[0]::nb][:x0][:64])
        for k, (ci, co) in enumerate(pairs):
            si = ra[ci::na][x0 + dx:x1 + dx]
            so = rb[co::nb][x0:x1]
            lut = luts[k]
            for j, (vi, vo) in enumerate(zip(si, so)):
                pv = lut.setdefault(vi, vo)
                if pv != vo:
                    conflicts[k] += 1
                    if len(examples) < 8:
                        examples.append({"channel": k, "out_xy": [x0 + j, y], "in": vi, "out": vo, "earlier_out": pv})
    out_max = (1 << b["bit"]) - 1
    report = {"in": in_path, "out": out_path, "offset": [dx, dy],
              "in_size": [a["width"], a["height"], a["bit"]], "out_size": [b["width"], b["height"], b["bit"]],
              "margin_pixels": margin, "margin_values_sample": sorted(margin_vals)[:16],
              "out_alpha_not_opaque": not_opaque, "channels": []}
    verdict = "PASS_LINEAR"
    for k in range(len(pairs)):
        vals = sorted(luts[k].items())
        mono_up = all(vals[i][1] <= vals[i + 1][1] for i in range(len(vals) - 1))
        mono_dn = all(vals[i][1] >= vals[i + 1][1] for i in range(len(vals) - 1))
        fit = affine_fit(luts[k], 0, out_max)
        report["channels"].append({"distinct_inputs": len(vals), "conflicts": conflicts[k],
                                   "monotone": "up" if mono_up else ("down" if mono_dn else "no"), "fit": fit})
        if conflicts[k]:
            verdict = "FAIL_NOT_POINTWISE"
        elif verdict != "FAIL_NOT_POINTWISE" and (fit["max_residual"] or 0) > tol:
            verdict = "FAIL_NONLINEAR"
    report["examples"] = examples
    report["verdict"] = verdict
    report["tolerance"] = tol
    return report


# --------------------------------------------------------------------------------------------
def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    max_mb = 400
    if "--max-mb" in rest:
        i = rest.index("--max-mb")
        max_mb = int(rest[i + 1])
        del rest[i:i + 2]
    try:
        if cmd == "meta":
            reports = [meta_report(p, max_mb) for p in rest]
            print(json.dumps(reports, ensure_ascii=False, indent=1))
            return 0 if all(r["public_safe"] for r in reports) else 1
        if cmd == "strip" and len(rest) == 2:
            print(json.dumps(strip_file(rest[0], rest[1], max_mb), ensure_ascii=False, indent=1))
            return 0
        if cmd == "pixhash" and len(rest) == 1:
            print(pixel_hash(png_decode(read_file(rest[0], max_mb))))
            return 0
        if cmd == "pointop":
            offset, tol = (0, 0), None
            if "--offset" in rest:
                i = rest.index("--offset")
                offset = tuple(int(v) for v in rest[i + 1].split(","))
                del rest[i:i + 2]
            if "--tol" in rest:
                i = rest.index("--tol")
                tol = float(rest[i + 1])
                del rest[i:i + 2]
            if len(rest) != 2:
                raise Unsupported("pointop IN.png OUT.png [--offset DX,DY] [--tol T]")
            rep = pointop(rest[0], rest[1], offset, max_mb, tol)
            print(json.dumps(rep, ensure_ascii=False, indent=1))
            return 0 if rep["verdict"] == "PASS_LINEAR" else 1
        raise Unsupported("알 수 없는 하위 명령 — --help")
    except (Unsupported, OSError, ValueError, zlib.error, struct.error) as exc:
        print("pc_img: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
