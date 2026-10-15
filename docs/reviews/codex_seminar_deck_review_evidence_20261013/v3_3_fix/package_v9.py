"""ZIP v9 (Codex 종결 확인 묶음 · 덱 v3.3) — 목록과 MANIFEST 를 **실제로 넣은 파일**에서 만든다 (SELF-117: v3.2 요청서는 넣지 않은 원 수식 덱을 넣었다고 적었다).

python3 package_v9.py --repo <리포> --out-dir <폴더> --deck <v33.pptx> --pdf <v33.pdf> --png-dir <png 폴더> --eq <원 수식 덱> --v32 <v3.2 덱>

1. <out-dir>/codex_seminar_deck_v3_3_closure_20261015/ 을 새로 만든다 — deck/ · png/ · source_eq/eq.pptx · v32/ · repo/<REPO_FILES> · PIN.txt
2. 요청서 §6 의 ZIP-LIST 블록 = 그 폴더의 실제 파일 (sha256 · 바이트 · 경로) + 요청서 자신 + MANIFEST.sha256 (둘은 해시 없이 이름만)
3. 요청서 §0 의 sha256 (64 자) 이 넣은 파일의 해시인지 확인 (양식 덱은 ZIP 밖 — `--outside` 로 받은 해시만 허용)
4. 요청서 사본 → 폴더 맨 위 · MANIFEST.sha256 = 자기 자신을 뺀 전 항목
5. zip (이름순 · 고정 시각) → 다시 열어: 항목 = MANIFEST + MANIFEST 자신 · 해시 일치 · ZIP-LIST 항목 = ZIP 항목 · 요청서 사본 = 리포 요청서
"""
import argparse
import hashlib
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = 'codex_seminar_deck_v3_3_closure_20261015'
REQUEST = 'docs/reviews/codex_seminar_deck_v3_3_closure_request_20261015.md'
EV = 'docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_3_fix'
REPO_FILES = ['docs/seminar_20261013/build_seminar_v33.py',
              'docs/seminar_20261013/figs_v3/make_seminar_figs_v33.py',
              'docs/seminar_20261013/figs_v3/F_p4_v33.png',
              'docs/seminar_20261013/figs_v3/F_p4_v33.svg',
              'docs/seminar_20261013/figs_v3/F_p4_v33.csv',
              'docs/seminar_20261013/slide_text_v33.md',
              'docs/seminar_20261013/slide_sources_v33.json',
              'docs/seminar_20261013/README.md',
              f'{EV}/testfirst_v33.py', f'{EV}/testfirst_v33.json', f'{EV}/testfirst_render_on_v32.json',
              f'{EV}/checks_v33.json', f'{EV}/finalchecks_on_v32.json',
              f'{EV}/cmp_codex_v32.py', f'{EV}/cmp_codex_v32.json',
              f'{EV}/render_check_v33.py', f'{EV}/render_check_v33.json',
              f'{EV}/package_v9.py']
PIN = ('review pin = the main-branch commit that carries ' + REQUEST + '\n'
       '             (recorded by the main session after cherry-pick; agent-worktree commits are not cited — SELF-116)\n'
       'base       = db04a2a7a (origin/claude/stoic-knuth-NObVQ when v3.3 was built; contains the v3.2 re-check import and fix plan 5393ae855)\n'
       'previous   = 90ca2c8cd (v3.2 review pin)\n')
DATE = (2026, 10, 15, 0, 0, 0)
BEGIN, END = '<!-- ZIP-LIST:BEGIN -->', '<!-- ZIP-LIST:END -->'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--deck', required=True)
    ap.add_argument('--pdf', required=True)
    ap.add_argument('--png-dir', required=True)
    ap.add_argument('--eq', required=True)
    ap.add_argument('--v32', required=True)
    ap.add_argument('--outside', action='append', default=[], help='§0 에 적혔지만 ZIP 밖인 파일의 sha256 (양식 덱)')
    a = ap.parse_args()
    repo, out = Path(a.repo).resolve(), Path(a.out_dir).resolve()
    stage = out / ROOT
    if stage.exists():
        shutil.rmtree(stage)
    (stage / 'deck').mkdir(parents=True)
    shutil.copyfile(a.deck, stage / 'deck' / Path(a.deck).name)
    shutil.copyfile(a.pdf, stage / 'deck' / Path(a.pdf).name)
    (stage / 'png').mkdir()
    pngs = sorted(Path(a.png_dir).glob('slide-*.png'))
    assert len(pngs) == 18, len(pngs)
    for p in pngs:
        shutil.copyfile(p, stage / 'png' / p.name)
    (stage / 'source_eq').mkdir()
    shutil.copyfile(a.eq, stage / 'source_eq' / 'eq.pptx')
    (stage / 'v32').mkdir()
    shutil.copyfile(a.v32, stage / 'v32' / Path(a.v32).name)
    for rel in REPO_FILES:
        dst = stage / 'repo' / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(repo / rel, dst)
    (stage / 'PIN.txt').write_text(PIN, encoding='utf-8')

    members = sorted(p.relative_to(stage).as_posix() for p in stage.rglob('*') if p.is_file())
    rows = [f'{sha(stage / m)}  {(stage / m).stat().st_size:>10}  {m}' for m in members]
    req_name = Path(REQUEST).name
    block = '\n'.join([BEGIN, '```', 'sha256' + ' ' * 60 + 'bytes  path (ZIP 안 · ' + ROOT + '/ 아래)'] + rows +
                      [f'{"(this file — hash in MANIFEST.sha256)":<76}  {req_name}',
                       f'{"(hash list of every other member)":<76}  MANIFEST.sha256', '```', END])
    req_path = repo / REQUEST
    text = req_path.read_text(encoding='utf-8')
    assert text.count(BEGIN) == 1 and text.count(END) == 1
    text = text[:text.index(BEGIN)] + block + text[text.index(END) + len(END):]
    req_path.write_text(text, encoding='utf-8')

    # §0 의 64 자 해시 = 넣은 파일 (또는 --outside 로 밝힌 ZIP 밖 파일)
    sec0 = text[text.index('## 0.'):text.index('## 1.')]
    staged = {sha(stage / m) for m in members}
    bad = [h for h in re.findall(r'`([0-9a-f]{64})`', sec0) if h not in staged and h not in a.outside]
    assert not bad, f'§0 hashes not in the bundle: {bad}'

    shutil.copyfile(req_path, stage / req_name)
    members = sorted(p.relative_to(stage).as_posix() for p in stage.rglob('*') if p.is_file())
    (stage / 'MANIFEST.sha256').write_text(''.join(f'{sha(stage / m)}  ./{m}\n' for m in members), encoding='utf-8')

    zpath = out / f'{ROOT}.zip'
    if zpath.exists():
        zpath.unlink()
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for m in sorted(members + ['MANIFEST.sha256']):
            zi = zipfile.ZipInfo(f'{ROOT}/{m}', date_time=DATE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, (stage / m).read_bytes())

    # 다시 열어 대조
    with zipfile.ZipFile(zpath) as z:
        names = sorted(n[len(ROOT) + 1:] for n in z.namelist())
        man = {ln.split('  ./', 1)[1]: ln.split('  ./', 1)[0] for ln in z.read(f'{ROOT}/MANIFEST.sha256').decode().splitlines()}
        assert names == sorted(list(man) + ['MANIFEST.sha256']), 'ZIP members ≠ MANIFEST + MANIFEST'
        for n, h in man.items():
            assert hashlib.sha256(z.read(f'{ROOT}/{n}')).hexdigest() == h, n
        listed = re.findall(r'^([0-9a-f]{64})\s+(\d+)\s+(\S+)$', block, flags=re.M)
        listed_names = sorted([p for _, _, p in listed] + [req_name, 'MANIFEST.sha256'])
        assert listed_names == names, 'request list ≠ ZIP members'
        for h, size, p in listed:
            data = z.read(f'{ROOT}/{p}')
            assert hashlib.sha256(data).hexdigest() == h and len(data) == int(size), p
        assert z.read(f'{ROOT}/{req_name}') == req_path.read_bytes(), 'request copy ≠ repo request'
    print(f'zip ok — {len(names)} members · MANIFEST {len(man)} · request list {len(listed)} + 2 · sha256 {sha(zpath)}')
    print(zpath)
    return 0


if __name__ == '__main__':
    sys.exit(main())
