#!/usr/bin/env python3 -I
# -*- coding: utf-8 -*-
"""kgy S0 단계 1 결과 tgz → docs/data/rint2_s0_sbe_<날짜>/ 반입 도구 (인계 §5-2 · 준비판 · 11-08).

쓰임:  python3 -I import_s0_tgz.py <tgz> <out_dir> [--date YYYYMMDD] [--max-copy-mb 8]
  · tgz 는 믿지 않는 자료 — 빈 임시 폴더에 안전하게 풀고 (절대 경로 · `..` · 링크 거부) 읽기만 한다 · 아무것도 실행하지 않는다.
  · 채택 조건 (S0 REPORT §12): rc 0 ∧ 여섯 출력 (s0_stage1_kit_SBE_vgcf100.json · s0_junctions_*.npz · s0_instances_*.npz ·
    cjunc_plan.json · cjunc_plan.sha256 · payload_capture_*.log) 전부 ∧ cjunc_plan.sha256 = cjunc_plan.json 의 sha256.
    하나라도 아니면 FAILED_PRESERVED 로 보존 (지우지 않는다).
  · out_dir 에 쓰는 것: 작은 파일 (JSON · plan · sha256 · 로그 · pair_search.json) 사본 · 큰 npz 는 NPZ_SHA256.txt 에 sha256 · 크기만 ·
    MANIFEST.tsv (tgz 안 전 파일 경로 · 크기 · sha256) · README.md (판정 · 근거 · rc 출처 · rss 최대 · 미확인 목록).
  · rc 의 출처는 **사람이 확인**한다 — 이 도구는 후보 (rc 파일 · 로그의 rc= 줄) 를 모아 보일 뿐이고, 후보가 없거나 서로 다르면 '미확인' 으로 두고 채택하지 않는다.
"""
import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import shutil
import sys
import tarfile

REQUIRED = [
    ('kit_json', re.compile(r'(^|/)s0_stage1_kit_SBE_vgcf100\.json$')),
    ('junctions_npz', re.compile(r'(^|/)s0_junctions_[^/]*\.npz$')),
    ('instances_npz', re.compile(r'(^|/)s0_instances_[^/]*\.npz$')),
    ('plan_json', re.compile(r'(^|/)cjunc_plan\.json$')),
    ('plan_sha', re.compile(r'(^|/)cjunc_plan\.sha256$')),
    ('payload_log', re.compile(r'(^|/)payload_capture_[^/]*\.log$')),
]
OPTIONAL = [
    ('pair_search', re.compile(r'(^|/)pair_search\.json$')),
    ('rss_log', re.compile(r'(^|/)[^/]*rss[^/]*\.log$')),
    ('rc_file', re.compile(r'(^|/)(rc|exit|exitcode|returncode)[^/]*\.(txt|log)$', re.I)),
    ('run_log', re.compile(r'(^|/)(run|s0|stage1|nohup)[^/]*\.(log|out)$', re.I)),
]
RC_LINE = re.compile(r'\b(?:rc|RC|exit(?:\s*code)?|returncode)\s*[=:]\s*(-?\d+)\b')


def sha256_of(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(chunk), b''):
            h.update(b)
    return h.hexdigest()


def safe_extract(tgz, dest):
    """절대 경로 · `..` · 링크 · 장치 파일 거부.  dest 는 비어 있어야 한다."""
    os.makedirs(dest, exist_ok=True)
    if os.listdir(dest):
        raise SystemExit(f'⛔ 임시 폴더가 비어 있지 않다: {dest}')
    with tarfile.open(tgz, 'r:*') as tf:
        for m in tf.getmembers():
            p = m.name
            if p.startswith('/') or p.startswith('\\') or '..' in p.split('/') or ':' in p.split('/')[0]:
                raise SystemExit(f'⛔ 위험한 경로: {p}')
            if m.issym() or m.islnk() or m.isdev() or m.isfifo():
                raise SystemExit(f'⛔ 링크 · 장치 항목: {p}')
            if not (m.isfile() or m.isdir()):
                raise SystemExit(f'⛔ 알 수 없는 항목 종류: {p}')
        tf.extractall(dest)  # 위에서 전수 검사 끝


def walk_files(root):
    out = []
    for dp, dn, fn in os.walk(root):
        dn.sort()
        for n in sorted(fn):
            full = os.path.join(dp, n)
            rel = os.path.relpath(full, root).replace(os.sep, '/')
            out.append((rel, full, os.path.getsize(full)))
    return out


def find(files, rx):
    return [f for f in files if rx.search(f[0])]


def rss_max(path):
    """rss 로그에서 가장 큰 숫자 줄 (단위는 원문 그대로) — 숫자 해석은 사람 몫."""
    best = None
    try:
        with open(path, 'r', errors='replace') as f:
            for line in f:
                nums = re.findall(r'(?<![\w.])(\d+(?:\.\d+)?)(?![\w.])', line)
                for s in nums:
                    v = float(s)
                    if best is None or v > best[0]:
                        best = (v, line.rstrip('\n')[:200])
    except OSError:
        return None
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tgz')
    ap.add_argument('out_dir')
    ap.add_argument('--date', default=_dt.date.today().strftime('%Y%m%d'))
    ap.add_argument('--max-copy-mb', type=float, default=8.0)
    ap.add_argument('--tmp', default=None, help='푸는 임시 폴더 (기본 = out_dir 옆 _unpack_<날짜>)')
    a = ap.parse_args()

    if not os.path.isfile(a.tgz):
        raise SystemExit(f'⛔ tgz 없음: {a.tgz}')
    tgz_sha = sha256_of(a.tgz)
    tgz_size = os.path.getsize(a.tgz)
    tmp = a.tmp or os.path.join(os.path.dirname(os.path.abspath(a.out_dir)) or '.', f'_unpack_s0_{a.date}')
    safe_extract(a.tgz, tmp)
    files = walk_files(tmp)

    found = {}
    missing = []
    for key, rx in REQUIRED:
        hits = find(files, rx)
        found[key] = hits
        if not hits:
            missing.append(key)
    for key, rx in OPTIONAL:
        found[key] = find(files, rx)

    notes = []
    # cjunc_plan.sha256 ↔ cjunc_plan.json
    plan_ok = None
    if found['plan_json'] and found['plan_sha']:
        pj = found['plan_json'][0][1]
        actual = sha256_of(pj)
        try:
            txt = open(found['plan_sha'][0][1], 'r', errors='replace').read()
        except OSError:
            txt = ''
        m = re.search(r'\b([0-9a-f]{64})\b', txt)
        declared = m.group(1) if m else None
        plan_ok = (declared == actual)
        notes.append(f'cjunc_plan.sha256 선언 {declared} · 실제 {actual} → {"같음" if plan_ok else "다름"}')
    # JSON 읽기 (실행 없음)
    kit_summary = None
    if found['kit_json']:
        try:
            with open(found['kit_json'][0][1], 'r', encoding='utf-8') as f:
                kit = json.load(f)
            keys = sorted(kit.keys()) if isinstance(kit, dict) else []
            kit_summary = f'최상위 칸 {len(keys)}: ' + ' · '.join(keys[:40])
        except (OSError, ValueError) as e:
            kit_summary = f'⛔ JSON 읽기 실패: {type(e).__name__}: {e}'
            notes.append(kit_summary)
    # rc 후보
    rc_candidates = []
    for rel, full, size in found['rc_file']:
        try:
            s = open(full, 'r', errors='replace').read(200).strip()
        except OSError:
            s = ''
        mm = re.search(r'-?\d+', s)
        rc_candidates.append((rel, int(mm.group(0)) if mm else None, s[:80]))
    for rel, full, size in found['run_log'] + found['payload_log']:
        if size > 50 * 1024 * 1024:
            continue
        try:
            tail = open(full, 'r', errors='replace').read()[-20000:]
        except OSError:
            continue
        for mm in RC_LINE.finditer(tail):
            rc_candidates.append((rel, int(mm.group(1)), mm.group(0)))
    # ★ 11-09 고침 (SELF — 합성 고정물이 생산자 꼴을 따르지 않아 놓침): rc 근거 = run2.sh 15 줄 (`wait $PID; echo "rc=$?" >> rss.log`) 이
    #   rss.log 에 적는 `rc=<n>` 줄 하나뿐 (수정 계획 docs/reviews/rint2_rr3_fix_plan_20261108.md §5 조건 1 = S0 Python 자식 rc) · 그 밖의 rc= 글은 참고만
    #   (결정에 안 씀) · CAP_TERM 줄 = 메모리 상한 중단 = 채택 안 함.
    rss_rc, cap_term = [], False
    for rel, full, size in found['rss_log']:
        try:
            lines = open(full, 'r', errors='replace').read().splitlines()
        except OSError:
            continue
        for ln in lines:
            t = ln.strip()
            if re.fullmatch(r'rc=-?\d+', t):
                rss_rc.append((rel, int(t[3:]), t))
            if 'CAP_TERM' in t:
                cap_term = True
                notes.append(f'⛔ {rel}: CAP_TERM 줄 (메모리 상한 중단) — {t[:60]}')
    other_rc = rc_candidates
    rc_candidates = rss_rc + [(r, v, '[참고 · 결정에 안 씀] ' + g) for r, v, g in other_rc]
    rc_values = sorted({c[1] for c in rss_rc})
    rc = rc_values[0] if (len(rss_rc) == 1 and len(rc_values) == 1 and not cap_term) else None
    # rss 최대
    rss = [(rel, rss_max(full)) for rel, full, size in found['rss_log']]

    adopt = (rc == 0) and not missing and (plan_ok is True)
    verdict = 'ADOPT_CANDIDATE' if adopt else 'FAILED_PRESERVED'
    reasons = []
    if rc != 0:
        reasons.append('rc ≠ 0 또는 미확인' + (f' (rss.log rc 줄 {[c[2] for c in rss_rc]})' if rss_rc else ' (rss.log 에 rc 줄 없음)')
                       + (' · CAP_TERM' if cap_term else ''))
    if missing:
        reasons.append('빠진 출력: ' + ' · '.join(missing))
    if plan_ok is not True:
        reasons.append('cjunc_plan.sha256 대조 실패 또는 미확인')

    # out_dir 쓰기
    os.makedirs(a.out_dir, exist_ok=True)
    if os.listdir(a.out_dir):
        raise SystemExit(f'⛔ out_dir 이 비어 있지 않다 (덮어쓰지 않는다): {a.out_dir}')
    with open(os.path.join(a.out_dir, 'MANIFEST.tsv'), 'w', encoding='utf-8') as f:
        f.write('path\tbytes\tsha256\n')
        for rel, full, size in files:
            f.write(f'{rel}\t{size}\t{sha256_of(full)}\n')
    copied, hashed_only = [], []
    limit = int(a.max_copy_mb * 1024 * 1024)
    for key in [k for k, _ in REQUIRED] + [k for k, _ in OPTIONAL]:
        for rel, full, size in found[key]:
            if rel.endswith('.npz') or size > limit:
                hashed_only.append((rel, size, sha256_of(full)))
            else:
                dst = os.path.join(a.out_dir, 'files', rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(full, dst)
                copied.append((rel, size))
    with open(os.path.join(a.out_dir, 'NPZ_SHA256.txt'), 'w', encoding='utf-8') as f:
        for rel, size, h in hashed_only:
            f.write(f'{h}  {size}  {rel}\n')
    with open(os.path.join(a.out_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(f'# kgy S0 단계 1 (SBE) 결과 반입 — {a.date}\n\n')
        f.write(f'- 원본 tgz: `{os.path.basename(a.tgz)}` · {tgz_size} B · sha256 `{tgz_sha}` · 안 파일 {len(files)}\n')
        f.write(f'- **판정 = {verdict}**' + ('' if adopt else ' — ' + ' · '.join(reasons)) + '\n')
        f.write('- 채택 조건 (S0 REPORT §12) = rc 0 ∧ 여섯 출력 전부 ∧ cjunc_plan.sha256 = cjunc_plan.json 의 sha256 · 이 판정은 도구의 자동 대조이고, rc 출처는 사람이 한 번 더 확인한다.\n\n')
        f.write('## 여섯 출력\n\n| 항목 | 찾은 파일 (묶음 안 경로 → 이 폴더 사본 자리) |\n|---|---|\n')
        _cp = {r for r, _ in copied}
        def _where(r, s):   # ★ 11-09 — 사본 = 이 폴더 `files/<묶음 안 경로>` (리포에서 열림) · 사본 없음 (npz) = sha 만 (NPZ_SHA256.txt) — 묶음 안 경로를 리포 경로처럼 적지 않는다
            return (f'`files/{r}` ({s} B)' if r in _cp else f'{r} ({s} B · 사본 없음 · sha = `NPZ_SHA256.txt`)')
        for key, _ in REQUIRED:
            f.write(f'| {key} | ' + (' · '.join(_where(r, s) for r, _, s in found[key]) or '**없음**') + ' |\n')
        f.write('\n## rc 근거 (rss.log 의 `rc=` 줄 = run2.sh 15 줄 · S0 Python 자식 rc · 그 밖의 rc= 글 = 참고 · 결정에 안 씀)\n\n')
        if rc_candidates:
            for rel, v, s in rc_candidates:
                f.write((f'- `files/{rel}`' if rel in _cp else f'- {rel}') + f' → {v} (`{s}`)\n')
        else:
            f.write('- 없음 → 미확인\n')
        f.write(f'\n- 결론 rc = {rc if rc is not None else "미확인"}\n')
        f.write('\n## 기타\n\n')
        for n in notes:
            f.write(f'- {n}\n')
        if kit_summary:
            f.write(f'- kit JSON: {kit_summary}\n')
        for rel, best in rss:
            f.write(f'- rss 로그 `files/{rel}` 최대 숫자 줄: ' + (f'{best[0]} — `{best[1]}`' if best else '읽기 실패') + ' (단위 = 원문)\n')
        f.write(f'- 사본 {len(copied)} · sha 만 {len(hashed_only)} (`NPZ_SHA256.txt`) · 전체 목록 `MANIFEST.tsv`\n')
        f.write('- 이 폴더의 파일은 읽기만 했고 아무것도 실행하지 않았다 (업로드 = 믿지 않는 자료 · python -I).\n')
    print(f'{verdict}  rc={rc}  missing={missing}  plan_sha_ok={plan_ok}  files={len(files)}  copied={len(copied)}  npz_sha_only={len(hashed_only)}')
    print(f'README → {os.path.join(a.out_dir, "README.md")}')
    return 0 if adopt else 2


if __name__ == '__main__':
    sys.exit(main())
