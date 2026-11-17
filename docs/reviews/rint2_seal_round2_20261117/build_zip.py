#!/usr/bin/env python3
"""Codex 2/2 요청 ZIP 만들기 (Rint ② · 11-17) — 리뷰 핀 blob 그대로 + extra/ + PIN.txt + ZIP_MANIFEST.tsv.

쓰는 법 (리포 뿌리 밖에서도 된다 · git 읽기 명령만):
    python3 -I build_zip.py --repo <리포> --pin <40 자리> --paths <zip_paths.txt> --extra <폴더> --out <출력.zip>

- repo/ = `git ls-tree -r <pin> -- <경로>` 의 blob 을 `git cat-file blob` 으로 읽고 git blob sha1 을 다시 세어 대조한다 (다르면 멈춤).
- extra/ = 주어진 폴더를 이름 차례로 그대로 (링크는 멈춤).
- 같은 입력 = 같은 바이트 (이름 차례 · 고정 시각 1980-01-01 · 고정 권한 · deflate 9).
- 이 도구는 git 에 쓰지 않는다.  GIT_DIR · GIT_WORK_TREE · GIT_INDEX_FILE 이 env 에 있으면 멈춘다.
"""
import argparse
import hashlib
import os
import subprocess
import sys
import zipfile

FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def die(msg):
    sys.stderr.write('build_zip: ' + msg + '\n')
    sys.exit(2)


def git(repo, *args):
    env = dict(os.environ)
    env['GIT_NO_REPLACE_OBJECTS'] = '1'
    return subprocess.run(['git', '-C', repo] + list(args), check=True,
                          stdout=subprocess.PIPE, env=env).stdout


def blob_sha1(data):
    h = hashlib.sha1()
    h.update(b'blob %d\0' % len(data))
    h.update(data)
    return h.hexdigest()


def add(zf, arcname, data):
    zi = zipfile.ZipInfo(arcname, date_time=FIXED_TIME)
    zi.compress_type = zipfile.ZIP_DEFLATED
    zi.external_attr = (0o644 << 16)
    zi.create_system = 3
    zf.writestr(zi, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main():
    for k in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'):
        if k in os.environ:
            die('env %s 가 있다 — 멈춤' % k)
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--pin', required=True)
    ap.add_argument('--paths', required=True)
    ap.add_argument('--extra', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    if len(a.pin) != 40 or any(c not in '0123456789abcdef' for c in a.pin):
        die('--pin 은 40 자리 소문자 hex')
    if git(a.repo, 'cat-file', '-t', a.pin).strip() != b'commit':
        die('핀이 커밋이 아니다')
    wanted = [ln.strip() for ln in open(a.paths, encoding='utf-8')
              if ln.strip() and not ln.lstrip().startswith('#')]
    if not wanted:
        die('경로 목록이 비었다')
    entries = {}
    for p in wanted:
        out = git(a.repo, 'ls-tree', '-r', '-z', '--full-tree', a.pin, '--', p)
        recs = [r for r in out.split(b'\0') if r]
        if not recs:
            die('핀에 없다: %s' % p)
        for r in recs:
            meta, path = r.split(b'\t', 1)
            mode, typ, sha = meta.split(b' ')
            if typ != b'blob':
                die('blob 아님: %r' % path)
            if mode not in (b'100644', b'100755'):
                die('보통 파일 아님 (mode %s): %r' % (mode.decode(), path))
            entries[path.decode('utf-8')] = sha.decode()
    rows = []
    with zipfile.ZipFile(a.out + '.part', 'w') as zf:
        for path in sorted(entries):
            data = git(a.repo, 'cat-file', 'blob', entries[path])
            if blob_sha1(data) != entries[path]:
                die('blob sha1 다름: %s' % path)
            add(zf, 'repo/' + path, data)
            rows.append(('repo/' + path, len(data), hashlib.sha256(data).hexdigest(), entries[path]))
        extra = os.path.abspath(a.extra)
        files = []
        for root, dirs, fs in os.walk(extra):
            dirs.sort()
            for f in fs:
                full = os.path.join(root, f)
                if os.path.islink(full) or not os.path.isfile(full):
                    die('보통 파일 아님: %s' % full)
                files.append(os.path.relpath(full, extra).replace(os.sep, '/'))
        for rel in sorted(files):
            data = open(os.path.join(extra, rel), 'rb').read()
            add(zf, 'extra/' + rel, data)
            rows.append(('extra/' + rel, len(data), hashlib.sha256(data).hexdigest(), '-'))
        tool = open(os.path.abspath(__file__), 'rb').read()
        pin_txt = ('pin %s\nbranch claude/stoic-knuth-NObVQ\nbuild_zip.py sha256 %s\n'
                   % (a.pin, hashlib.sha256(tool).hexdigest())).encode('ascii')
        add(zf, 'PIN.txt', pin_txt)
        man = 'path\tbytes\tsha256\tgit_blob\n' + ''.join(
            '%s\t%d\t%s\t%s\n' % r for r in rows)
        add(zf, 'ZIP_MANIFEST.tsv', man.encode('utf-8'))
    os.replace(a.out + '.part', a.out)
    z = hashlib.sha256(open(a.out, 'rb').read()).hexdigest()
    print('repo %d · extra %d · zip %s · sha256 %s' % (
        sum(1 for r in rows if r[0].startswith('repo/')),
        sum(1 for r in rows if r[0].startswith('extra/')), a.out, z))


if __name__ == '__main__':
    main()
