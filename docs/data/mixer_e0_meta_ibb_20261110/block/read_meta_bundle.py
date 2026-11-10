#!/usr/bin/env python3
"""read_meta_bundle.py — ibb 에서 가져온 믹서 E0 메타 묶음 (mixer_e0_meta_<UTC>.tgz) 을 빈 새 폴더에 안전하게 풀고 대조 · 요약한다.

사용 (리포 밖 · 빈 새 폴더 · 격리 모드 · 이 파일은 풀 폴더와 다른 곳에 둔다):
  python3 -I read_meta_bundle.py <묶음.tgz> <빈 새 폴더> [--expect-md5 <블록 md5>] [--expect-sha256 <화면 sha256>]
하는 일: 묶음 sha256 대조 → 멤버 검사 (절대경로 · '..' · 링크 · 장치 · out/ 밖 · 크기 상한 · 소유자 이름 = 거부) →
  정규 파일만 직접 써서 풂 (extractall 안 씀) → out/SHA256SUMS 전수 대조 → meta_script.sh md5 = 블록 md5 → 요약 출력.
rc 0 = 묶음 구조 정상.  ⚠ 자격 판정 · 실행 승인이 아니다 (관측 메타일 뿐).  원자료를 리포에 쓰지 않는다.
"""
import argparse
import hashlib
import os
import sys
import tarfile

MAX_MEMBERS = 5000
MAX_MEMBER = 50 * 1024 * 1024
MAX_TOTAL = 200 * 1024 * 1024
STATUSES = {'OK', 'FAIL', 'MISSING', 'TIMEOUT', 'TRUNC', 'SKIPPED_BUDGET', 'SKIPPED_SWITCH', 'SKIPPED_NOT_LUSTRE'}


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def parse_kv(text):
    out = {}
    for line in text.splitlines():
        if '=' not in line:
            continue
        k, v = line.split('=', 1)
        out.setdefault(k, []).append(v)
    return out


def main():
    ap = argparse.ArgumentParser(description='믹서 E0 메타 묶음 안전 해제 · 대조 · 요약 (읽기만)')
    ap.add_argument('tgz')
    ap.add_argument('dest', help='없거나 빈 새 폴더')
    ap.add_argument('--expect-md5', default=None, help='블록 마지막 줄의 스크립트 md5')
    ap.add_argument('--expect-sha256', default=None, help='ibb 화면에 찍힌 tgz sha256')
    a = ap.parse_args()
    bad = []

    with open(a.tgz, 'rb') as f:
        blob = f.read()
    tsha = sha256_bytes(blob)
    print(f'묶음 sha256 {tsha} · {len(blob)} 바이트')
    if a.expect_sha256 is not None and a.expect_sha256.strip().lower() != tsha:
        bad.append('묶음 sha256 이 화면 값과 다름')

    if os.path.exists(a.dest):
        if not os.path.isdir(a.dest) or os.listdir(a.dest):
            print('거부: 풀 폴더가 비어 있지 않다 (빈 새 폴더만)')
            return 2
    else:
        os.makedirs(a.dest)

    files = {}
    with tarfile.open(a.tgz, 'r:gz') as tf:
        members = tf.getmembers()
        if len(members) > MAX_MEMBERS:
            print(f'거부: 멤버 {len(members)} 개 > {MAX_MEMBERS}')
            return 2
        total = 0
        for m in members:
            n = m.name
            parts = n.split('/')
            if n.startswith('/') or '..' in parts or not (n == 'out' or n.startswith('out/')):
                bad.append(f'멤버 이름 거부: {n!r}')
                continue
            if m.uname or m.gname or m.uid or m.gid:
                bad.append(f'소유자 정보가 남음: {n} (uname={m.uname!r} uid={m.uid})')
            if m.isdir():
                continue
            if not m.isfile():
                bad.append(f'정규 파일 아님 (링크 · 장치): {n}')
                continue
            if m.size > MAX_MEMBER:
                bad.append(f'멤버 크기 상한 초과: {n}')
                continue
            total += m.size
            if total > MAX_TOTAL:
                bad.append('전체 크기 상한 초과')
                break
            data = tf.extractfile(m).read()
            files[n] = data
    for n, data in files.items():
        p = os.path.join(a.dest, *n.split('/'))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'xb') as f:
            f.write(data)

    sums = files.get('out/SHA256SUMS')
    if sums is None:
        bad.append('out/SHA256SUMS 없음')
    else:
        listed = set()
        for line in sums.decode('utf-8', 'replace').splitlines():
            if not line.strip():
                continue
            h, _, name = line.partition('  ')
            listed.add(name)
            got = files.get('out/' + name)
            if got is None:
                bad.append(f'SHA256SUMS 의 파일이 묶음에 없음: {name}')
            elif sha256_bytes(got) != h:
                bad.append(f'sha256 불일치: {name}')
        extra = sorted(n[4:] for n in files if n.startswith('out/') and n[4:] not in listed and n[4:] != 'SHA256SUMS')
        if extra:
            bad.append(f'SHA256SUMS 에 없는 파일: {extra[:5]}')

    script = files.get('out/meta_script.sh')
    smd5 = hashlib.md5(script).hexdigest() if script is not None else None
    print(f'meta_script.sh md5 {smd5}')
    if a.expect_md5 is not None and smd5 != a.expect_md5.strip().lower():
        bad.append('meta_script.sh md5 이 블록 md5 와 다름 (다른 판의 스크립트가 돌았다)')

    fields = parse_kv(files.get('out/fields.txt', b'').decode('utf-8', 'replace'))
    fields.update(parse_kv(files.get('out/fields_post.txt', b'').decode('utf-8', 'replace')))
    if fields.get('format', [''])[0] != 'mixer_e0_meta/1':
        bad.append(f"형식 칸이 mixer_e0_meta/1 이 아님: {fields.get('format')}")
    probes = []
    for line in files.get('out/probes.txt', b'').decode('utf-8', 'replace').splitlines():
        c = line.split('|')
        if len(c) >= 6:
            probes.append(c)
            if c[1] not in STATUSES:
                bad.append(f'모르는 상태 {c[1]} ({c[0]})')
    counts = {}
    for c in probes:
        counts[c[1]] = counts.get(c[1], 0) + 1

    def f1(k, d='—'):
        return fields.get(k, [d])[0]

    print('── 요약 (관측 메타 · 자격 판정 아님)')
    print(f"형식 {f1('format')} · 블록 {f1('block_id')} · 수집 {f1('captured_start_utc')} → {f1('captured_end_utc')} ({f1('elapsed_seconds')} 초)")
    print('조회 상태 ' + ' · '.join(f'{k} {v}' for k, v in sorted(counts.items())))
    for st in ('MISSING', 'FAIL', 'TIMEOUT', 'TRUNC', 'SKIPPED_BUDGET'):
        names = [c[0] for c in probes if c[1] == st]
        if names:
            print(f'  {st}: ' + ', '.join(names[:40]) + (' …' if len(names) > 40 else ''))
    n_l = int(f1('lmp.n_unique_found', '0') or 0)
    print(f"LIGGGHTS 후보 {f1('lmp.n_candidates')} · 실제 파일 {n_l}")
    for k in range(1, n_l + 1):
        print(f"  lmp{k} {f1(f'lmp{k}.realpath')} · sha256 {f1(f'lmp{k}.sha256')} · 09-28 영수증 바이너리와 {f1(f'lmp{k}.vs_receipt_v2_ibb_20260928')}")
    print(f"mpirun 후보 {f1('mpi.n_candidates')} · 실제 {f1('mpi.n_unique_found')} · first8 E0 덱 = 정적 해시와 {f1('first8.e0_deck_vs_static')}")
    print(f"SLURM squeue rc {f1('slurm.squeue_rc')} · {f1('slurm.my_jobs_summary')}")
    print(f"디스크 HOME {f1('disk.home.fstype')} · 믹서 폴더 {f1('n_mixdirs')} · 봉인 파일 {f1('n_seal_files')} · 체크아웃 {f1('n_repos')}")
    print(f"가림 남은 문자열 {f1('redaction.residual_token_hits')} · 가림 가능 {f1('redaction.available')}")
    if bad:
        print('── 문제 ' + str(len(bad)))
        for b in bad:
            print('  ✗ ' + b)
        return 1
    print('── 구조 정상 (rc 0) — 관측 메타일 뿐 · 자격 · GO 아님')
    return 0


if __name__ == '__main__':
    sys.exit(main())
