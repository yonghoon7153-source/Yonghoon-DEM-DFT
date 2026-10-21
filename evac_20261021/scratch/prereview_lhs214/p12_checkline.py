#!/usr/bin/env python3
"""P12 — 194 등록 §3 ✅ 줄 · 표 28 행의 sha256 (HEAD 커밋 blob 에서 · 작업 트리 아님) ↔ 실제 HEAD blob sha256 · code_fp 재계산 (blob 기준).
재실행: python3 -I p12_checkline.py <worktree>"""
import hashlib, json, re, subprocess, sys
WT = sys.argv[1]
sys.path.insert(0, f'{WT}/scripts')
import run_network_194_parallel as N    # noqa: E402  (CODE_FILES · code_fp 만 씀 — 파일 읽기는 blob 으로)


def blob(f, rev='HEAD'):
    return subprocess.run(['git', 'show', f'{rev}:{f}'], cwd=WT, capture_output=True, check=True).stdout


doc = blob('docs/reviews/lhs_network_batch_registration_20261007_g2.md').decode('utf-8')
i = doc.index('\n## 3. ')
j = doc.index('\n## 3b.')
s3 = doc[i:j]
rows = dict(re.findall(r'^\| `([^`]+\.py)` \| `([0-9a-f]{64})` \|', s3, re.M))
ck = s3[s3.index('✅ **활성 봉인'):]
ckh = dict(re.findall(r'`((?:scripts|webapp)/[a-z0-9_]+\.py)` `([0-9a-f]{64})`', ck))
act = {f: hashlib.sha256(blob(f)).hexdigest() for f in N.CODE_FILES}
merged = dict(rows)
merged.update({k: v for k, v in ckh.items() if k in N.CODE_FILES})
res = dict(n_table=len(rows), n_checkline=len(ckh), checkline_files=sorted(ckh),
           checkline_eq_actual={k: ckh[k] == hashlib.sha256(blob(k)).hexdigest() for k in ckh},
           table_rows_eq_actual=sum(rows[k] == act[k] for k in rows), table_rows_ne=[k for k in rows if rows[k] != act[k]],
           merged_eq_actual_all=all(merged.get(k) == act[k] for k in N.CODE_FILES), code_fp_merged=N.code_fp(merged), code_fp_actual=N.code_fp(act),
           checkline_code_fp=re.findall(r'`code_fp ([0-9a-f]{64})`', ck))
print(json.dumps(res, ensure_ascii=False, indent=1))
