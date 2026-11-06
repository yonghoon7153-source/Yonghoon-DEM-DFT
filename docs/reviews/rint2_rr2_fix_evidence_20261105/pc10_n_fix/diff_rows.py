"""PC10 고치기 전 · 뒤 행 덤프 (dump_ct_rows.py 출력 둘) 의 차이 요약 — 받아들이는 꼴 (생산자 꼴 · 한정 별칭) 행이 바뀌었는지 · 바뀐 원인 글 · 재실행 자격의 방향.
python3 -I diff_rows.py <scripts 폴더 (CT_* 표)> <rows_before.json> <rows_after.json> <출력 json>"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import test_rint_r_chain as T  # noqa: E402

b = json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
a = json.loads(Path(sys.argv[3]).read_text(encoding='utf-8'))
out = {'before_module_sha256': b['module_sha256'], 'after_module_sha256': a['module_sha256'], 'test_sha256': a['test_sha256']}

ch = sorted(k for k in a['CT01'] if a['CT01'][k] != b['CT01'][k])
acc_changed = []
for k in ch:
    code, nm = k.split('/')[:2]
    if nm == 'prestart_nolog' or (T.ct_accepted(code, nm) and nm != 'none'):
        acc_changed.append(k)
out['CT01'] = {'rows': len(a['CT01']), 'changed': len(ch),
               'resume_true_to_false': sum(1 for k in ch if b['CT01'][k][1] and not a['CT01'][k][1]),
               'resume_false_to_true': sum(1 for k in ch if not b['CT01'][k][1] and a['CT01'][k][1]),
               'cause_changed': {k: [b['CT01'][k][0], a['CT01'][k][0]] for k in ch if a['CT01'][k][0] != b['CT01'][k][0]},
               'accepted_rows_changed': acc_changed}
ch2 = sorted(k for k in a['CT02'] if a['CT02'][k] != b['CT02'][k])
out['CT02'] = {'rows': len(a['CT02']), 'changed': {k: [b['CT02'][k], a['CT02'][k]] for k in ch2}, 'ctl_changed': [k for k in ch2 if k.startswith('ctl_')]}
out['CT03'] = {k: {'recover': [b['CT03'][k]['recover'], a['CT03'][k]['recover']], 'said': [b['CT03'][k]['said'], a['CT03'][k]['said']],
                   'recount': [b['CT03'][k]['recount'], a['CT03'][k]['recount']]} for k in a['CT03']}
ct4 = {}
for k in a['CT04']:
    if k == 'N4':
        ct4[k] = {'rc': [b['CT04'][k]['rc'], a['CT04'][k]['rc']], 'result': [b['CT04'][k]['result'], a['CT04'][k]['result']],
                  'said': [b['CT04'][k]['said'], a['CT04'][k]['said']]}
    else:
        rb, ra = b['CT04'][k].get('result') or {}, a['CT04'][k].get('result') or {}
        ct4[k] = {'cause': [rb.get('cause'), ra.get('cause')], 'resume_ok': [rb.get('resume_ok'), ra.get('resume_ok')],
                  'resume_rc': [b['CT04'][k].get('resume_rc'), a['CT04'][k].get('resume_rc')]}
out['CT04'] = ct4
Path(sys.argv[4]).write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
print(json.dumps({'CT01': {kk: (v if not isinstance(v, dict) else len(v)) for kk, v in out['CT01'].items()},
                  'CT02_changed': len(out['CT02']['changed']), 'CT02_ctl_changed': out['CT02']['ctl_changed'],
                  'CT03': {k: v['recover'] for k, v in out['CT03'].items()}, 'CT04': out['CT04']}, ensure_ascii=False))
