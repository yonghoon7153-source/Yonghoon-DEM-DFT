"""Assemble the import: verdict -> docs/reviews, members -> evidence folder, members TSV.

usage: python3 -I assemble.py <extracted_root> <repo_root>
Status rules (explicit; one row per bundle member):
  verdict        codex_review_lhs214cx_fix_recheck_20261020.md -> docs/reviews/ (bytes as is)
  meta           CONTENTS_SHA256.json (kept in the folder)
  big-hash-only  evidence/tree.json (> 2 MB; content = git ls-tree -r 34713ac96, checked)
  dup-repo       source_review/* (= same path in the repo, = 34713ac96 blob) and
                 baseline_review/* (= repo file or git 685c2bbdb blob) - checked by hash here
  keep           everything else (copied, bytes as is)
"""
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

EVID = 'docs/reviews/codex_lhs214cx_fix_recheck_evidence_20261020'
VERDICT = 'codex_review_lhs214cx_fix_recheck_20261020.md'
BIG = {'evidence/tree.json':
       'GitHub tree 응답 (검토 핀 34713ac96) · 내용 = git ls-tree -r 34713ac96 의 blob 11,443 '
       '(경로 · sha · 모드 같음 · 10-20 확인) · 2 MB 초과 → 해시만'}
BASE_DUP = {
    'baseline_review/codex_review_lhs214s_fix_recheck_20261019.md':
        ('file', 'docs/reviews/codex_review_lhs214s_fix_recheck_20261019.md'),
    'baseline_review/source_manifest.json':
        ('file', 'docs/reviews/codex_lhs214s_fix_recheck_evidence_20261019/lhs214s_recheck_20261019/source_manifest.json'),
    'baseline_review/scripts/supp20_input_receipt.py': ('blob', '685c2bbdb:scripts/supp20_input_receipt.py'),
    'baseline_review/scripts/test_l214r_r01_restored_full.py': ('blob', '685c2bbdb:scripts/test_l214r_r01_restored_full.py'),
}
NOTES = {
    'README.md': 'Codex 전달 안내 (재현 의존성 · 묶음 범위)',
    'intake.py': '실행하지 않음 — GitHub 네트워크 (urllib) · C:/Users/… 에서 요청서 복사 · 스냅샷 쓰기',
    'package_review.py': '실행하지 않음 — 검토 폴더에 ZIP · 영수증을 쓰는 포장 도구',
    'source_manifest.json': '검토 핀 스냅샷 2,135 파일 (경로 · bytes · sha256 · git_blob) = git 34713ac96 blob 2,135/2,135 같음 (10-20)',
    'probes/run_original.py': '실행하지 않음 — 우리 두 시험을 하위 프로세스로 돌리는 래퍼 · 같은 두 시험을 우리 트리에서 직접 돌렸다',
    'probes/s02/adversary.py': '실행 = 묶음 밖 복사본 · 경로 상수만 바꿈 (core · axis · mutants · failclosed · sweep 은 안 돌림) → _repro_ours_20261020/',
    'probes/s06/parser_audit.py': '실행하지 않음 — markdown-it-py 없음 (oracle) · 같은 생성 코드로 우리 판별 → _repro_ours_20261020/',
    'probes/s06/supplementary.py': '실행하지 않음 — parser_audit 을 import (markdown-it-py) · 같은 꼴을 우리 판별로',
    'probes/s06/generation_environment.py': '실행하지 않음 — parser_audit 을 import (markdown-it-py)',
    'probes/scope/cx_scope_audit.py': '실행하지 않음 — Codex 작업 공간의 source/ 스냅샷 필요 · 같은 대조를 git 으로 직접',
    'submitted/codex_lhs214cx_fix_recheck_request_20261019_send.md':
        '발송본 · 리포 요청서 (34713ac96 판) 와 7 행 하나만 다름 (리뷰 핀 자리 표시 ↔ 실제 34713ac9650e… · 가지 이름)',
    'evidence/original_baseline_boundary.log':
        '같은 바이트가 10-19 반입 docs/reviews/codex_lhs214s_fix_recheck_evidence_20261019/lhs214s_recheck_20261019/evidence/s02_new_full.log '
        '에도 있다 (같은 Windows 원본 시험의 같은 출력) · 판정문 §4-1 핵심 증거라 이 폴더에도 둔다',
    'evidence/s02/axis.log': '빈 파일 (0 B · Codex 탐침의 로그 자리)',
    'evidence/s02/sweep.log': '빈 파일 (0 B · Codex 탐침의 로그 자리)',
    'evidence/s06/new_cases': 'Codex Windows write_text 산출 = 줄 끝 CRLF (내용 = 우리 재생성 LF 판과 같음 · 12/12)',
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def blob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def main():
    root, repo = Path(sys.argv[1]), Path(sys.argv[2])
    members = sorted(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file())
    assert len(members) == 142, len(members)
    dest = repo / EVID
    assert not dest.exists(), dest
    rows = []
    for rel in members:
        b = (root / rel).read_bytes()
        h, n = sha(b), len(b)
        if rel == VERDICT:
            out = repo / 'docs/reviews' / VERDICT
            assert not out.exists()
            out.write_bytes(b)
            assert out.read_bytes() == b
            rows.append((h, n, 'verdict', rel, f'→ docs/reviews/{VERDICT} (바이트 그대로)'))
            continue
        if rel == 'CONTENTS_SHA256.json':
            st, note = 'meta', '묶음 뿌리 · 141 항목 sha256 · 크기 = 풀린 파일 전수 같음 (10-20) · 이 폴더에 둔다'
        elif rel in BIG:
            st, note = 'big-hash-only', BIG[rel]
        elif rel.startswith('source_review/'):
            sub = rel[len('source_review/'):]
            assert (repo / sub).read_bytes() == b, rel
            st = 'dup-repo'
            if sub == 'docs/reviews/codex_lhs214cx_fix_recheck_request_20261019.md':
                note = (f'리포 사본 = {sub} (34713ac96 판 · 같은 바이트 — 이 반입 커밋이 머리에 Codex 회신 한 줄을 '
                        f'붙이기 전)')
            else:
                note = f'리포 사본 = {sub} (같은 이름 · 같은 바이트 = 34713ac96 blob)'
        elif rel in BASE_DUP:
            kind, ref = BASE_DUP[rel]
            if kind == 'file':
                assert (repo / ref).read_bytes() == b, rel
                note = f'리포 사본 = {ref} (같은 바이트)'
            else:
                got = subprocess.run(['git', '-C', str(repo), 'rev-parse', ref], capture_output=True,
                                     text=True, check=True).stdout.strip()
                assert got == blob(b), (rel, got)
                note = f'리포 사본 = git {ref} (같은 바이트 · 작업 트리 판은 34713ac96 에서 바뀜)'
            st = 'dup-repo'
        else:
            st = 'keep'
            note = NOTES.get(rel) or next((v for k, v in NOTES.items()
                                           if rel.startswith(k + '/')), '-')
            out = dest / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(b)
        if st == 'meta':
            out = dest / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(b)
        rows.append((h, n, st, rel, note))
    with open(dest / '_members_mini.tsv', 'w', encoding='utf-8', newline='\n') as f:
        f.write('sha256\tbytes\tstatus\tpath (받은 묶음 안)\tnote\n')
        for r in rows:
            f.write('\t'.join(str(x) for x in r) + '\n')
    cnt = {}
    for r in rows:
        cnt[r[2]] = cnt.get(r[2], 0) + 1
    copied = sorted(p.relative_to(dest).as_posix() for p in dest.rglob('*') if p.is_file())
    print('status counts', cnt, '| files in folder', len(copied),
          '| bytes', sum((dest / p).stat().st_size for p in copied))


if __name__ == '__main__':
    main()
