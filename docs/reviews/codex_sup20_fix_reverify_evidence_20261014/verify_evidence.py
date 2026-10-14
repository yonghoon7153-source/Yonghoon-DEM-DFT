from pathlib import Path
import json,hashlib,re,sys
R=Path(__file__).resolve().parent
def sha(p):
    q=Path('\\\\?\\'+str(p.resolve())) if sys.platform=='win32' else p
    return hashlib.sha256(q.read_bytes()).hexdigest()
m=json.loads((R/'source_manifest.json').read_text(encoding='utf8'))
bad=[e['path'] for e in m['files'] if sha(R/'source'/e['path'])!=e['sha256']]
old=R.parent/'supp20_support_review_20261012'
same={n:sha(R/'probes'/n)==sha(old/'probes'/n) for n in ('design_probe.py','release_probe.py')}
release=(R/'evidence/release.log').read_text(encoding='utf8')
v22=[l for l in release.splitlines() if re.search(r'^\s+(PASS|FAIL)\s+V22',l)]
r=json.loads((R/'evidence/receipt_extra/summary.json').read_text(encoding='utf8'))
new_probes={
 'wrong_tsv_full_accepted':r['wrong_tsv_full_log']['rc']==0,
 'wrong_tsv_grep_accepted':r['wrong_tsv_registered_grep']['rc']==0,
 'grep_logs_identical':r['wrong_tsv_comparison']['registered_grep_byte_identical'],
 'wrong_tsv_direct_rejected':r['wrong_tsv_local_positive_rejection']['rc']==1,
 'off_full_rejected':r['observation_off_full_log']['rc']==1,
 'off_truncated_accepted':r['observation_off_truncated_before_stop']['rc']==0,
 'missing_prerequisites_accepted':r['missing_three_prerequisite_lines']['rc']==0,
}
out=dict(pin=m['pin'],source_files=len(m['files']),source_modified=bad,original_probes_byte_identical=same,
 original_probe_pin_label_note='Unchanged probes retain baseline pin labels; source_manifest pins executed source independently.',
 release_summary=re.findall(r'\d+ PASS · \d+ FAIL',release)[-1],release_v22_count=len(v22),release_v22_all_pass=all('PASS' in s for s in v22),
 new_probe_expected_outcomes=new_probes)
(R/'evidence/final_qa.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
assert not bad and all(same.values()) and len(v22)==22 and out['release_v22_all_pass'] and all(new_probes.values())
