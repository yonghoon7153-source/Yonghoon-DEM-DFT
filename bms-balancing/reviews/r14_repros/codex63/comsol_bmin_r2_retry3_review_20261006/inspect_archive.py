"""Reviewer-owned read-only ZIP inspection. Never imports supplied source."""
import ast
import collections
import hashlib
import json
import pathlib
import stat
import sys
import zipfile

ARCHIVE = pathlib.Path('C:/Users/Administrator/Downloads/BMIN_R2_LIMITED_VALIDATION_RETRY3_RESULT_20261005.zip')
def digest(b):
    return hashlib.sha256(b).hexdigest()
with zipfile.ZipFile(ARCHIVE) as z:
    def j(p):
        return json.loads(z.read(p).decode('utf-8-sig'))
    mode = sys.argv[1]
    if mode == 'verify':
        infos = z.infolist()
        names = [i.filename for i in infos]
        errors = []
        if len(names) != len(set(names)) or len(names) != len({x.casefold() for x in names}):
            errors.append('duplicate_or_case_collision')
        for i in infos:
            p = pathlib.PurePosixPath(i.filename)
            if p.is_absolute() or '..' in p.parts or '\\' in i.filename or ':' in i.filename or stat.S_ISLNK(i.external_attr >> 16):
                errors.append('unsafe_member:' + i.filename)
        m = j('PACKAGE_MANIFEST.json')
        expected = {f['file'] for f in m['files']} | {'PACKAGE_MANIFEST.json'}
        if set(names) != expected:
            errors.append('exact_set')
        for f in m['files']:
            b = z.read(f['file'])
            if len(b) != f['bytes'] or digest(b) != f['sha256']:
                errors.append('member_identity:' + f['file'])
        crc = z.testzip()
        if crc:
            errors.append('crc:' + crc)
        out = {'archive': str(ARCHIVE), 'bytes': ARCHIVE.stat().st_size, 'sha256': digest(ARCHIVE.read_bytes()), 'manifest_bytes': len(z.read('PACKAGE_MANIFEST.json')), 'manifest_sha256': digest(z.read('PACKAGE_MANIFEST.json')), 'payload_count': len(m['files']), 'member_count': len(names), 'uncompressed_bytes': sum(i.file_size for i in infos), 'errors': errors}
        print(json.dumps(out, ensure_ascii=False, indent=2))
    elif mode == 'read':
        for p in sys.argv[2:]:
            print('\nFILE ' + p)
            print('\n'.join(f'{i}: {s}' for i, s in enumerate(z.read(p).decode('utf-8-sig').splitlines(), 1)))
    elif mode == 'plan':
        p = j('fixed_received/LIMITED_VALIDATION_PLAN.json')
        for g in p['groups']:
            if g['id'] in sys.argv[2:]:
                print(json.dumps(g, ensure_ascii=False, indent=2))
        print(json.dumps({k:v for k,v in p.items() if k not in ('groups','v2_section_8_required_items')}, ensure_ascii=False, indent=2))
    elif mode == 'audit':
        errors=[]
        def check(ok, msg):
            if not ok: errors.append(msg)
        names=set(z.namelist())
        manifest=j('fixed_received/candidate/CODE_MANIFEST.json')
        check(digest(z.read('fixed_received/candidate/CODE_MANIFEST.json'))=='4cdca2e6bf7d073f813d97be73825b8cd2043c2fc44e285f4a190bc6fb97cf25','code_manifest')
        for pin in manifest['files']:
            raw=z.read('fixed_received/candidate/'+pin['file'])
            check(len(raw)==pin['bytes'] and digest(raw)==pin['sha256'],'source:'+pin['file'])
        before=j('SOURCE_IDENTITIES_BEFORE.json'); after=j('SOURCE_PRESERVATION_AFTER.json')
        check(before==after,'source_before_after')
        for pin in before:
            suffix=pin['path'].split('/candidate/')[1]
            raw=z.read('fixed_received/candidate/'+suffix)
            check(len(raw)==pin['bytes'] and digest(raw)==pin['sha256'],'source_snapshot:'+suffix)
        for item in j('EXTRACTION_MAP.json'):
            suffix=item['source']['path'].split('/candidate/')[1]
            raw=z.read('fixed_received/candidate/'+suffix)
            part=raw[item['byte_start_inclusive']:item['byte_end_exclusive']]
            member='extracted/'+pathlib.PurePosixPath(item['extracted']['path']).name
            check(part==z.read(member) and digest(part)==item['sha256'],'extraction:'+item['name'])
        plan=j('fixed_received/LIMITED_VALIDATION_PLAN.json')
        expected={(c['id'],i) for g in plan['groups'] for c in g['cases'] for i in range(1,c['inputs']+1)}
        accounting=j('FINAL_INPUT_ACCOUNTING.json')
        actual=[(c['id'],c['input_index']) for c in accounting]
        check(len(actual)==len(set(actual)) and set(actual)==expected,'input_set')
        check(all(c['status']=='PASS' for c in accounting),'accounting_status')
        engine_checks={}
        for engine in ('Python','Java_compile','Java_stub','PS51'):
            ret=j('engine_returns/'+engine+'_RETURN.json')
            for stream in ('stdout','stderr'):
                raw=z.read('engine_returns/'+engine+'_'+stream+'.txt')
                check(len(raw)==ret[stream]['bytes'] and digest(raw)==ret[stream]['sha256'],engine+'_'+stream)
            check(ret['rc']==0 and ret['error'] is None and ret['elapsed_s']<=ret['limit_s'],'engine:'+engine)
            engine_checks[engine]={'rc':ret['rc'],'elapsed_s':ret['elapsed_s'],'limit_s':ret['limit_s']}
        for engine,file in [('Python','PYTHON_RESULTS'),('PS51','PS_RESULTS')]:
            result=j('results/'+file+'.json')
            stdout=z.read('engine_returns/'+engine+'_stdout.txt').decode('utf-8-sig')
            rows=[json.loads(s) for s in stdout.splitlines() if s.strip()]
            check(rows==result['results'],'stdout_results:'+engine)
            bykey={(r['id'],r['input_index']):r for r in result['results']}
            for c in accounting:
                if (c['id'],c['input_index']) in bykey:
                    check(c['observed']==bykey[c['id'],c['input_index']],'accounting_result:'+c['id'])
        helper=z.read('harness/ShapeHarness.java')
        check(z.read('extracted/checkShape.java.txt') in helper,'helper_checkShape_exact')
        check(z.read('extracted/TIMES.java.txt').strip() in helper,'helper_TIMES_exact')
        seal=j('PRE_TEST_SEAL.json'); sealed={p['path'].replace('\\','/'):p for p in seal['files']}
        after_seal=j('SEALED_INPUTS_PRESERVATION_AFTER.json')
        check(len(after_seal)==len(seal['files']),'seal_after_count')
        check([{k:v for k,v in p.items() if k!='unchanged'} for p in after_seal]==seal['files'] and all(p['unchanged'] is True for p in after_seal),'seal_before_after_records')
        matched=[]; absent=[]
        for name in ('python_cases.py','ps_cases.ps1','harness/ShapeHarness.java','COMMANDS.json','EXTRACTION_MAP.json','INPUT_CASE_MAP.json'):
            pins=[p for p in seal['files'] if p['path'].replace('\\','/').endswith('/'+name)]
            raw=z.read(name)
            check(any(p['sha256']==digest(raw) and p['bytes']==len(raw) for p in pins),'preseal:'+name)
        for path,pin in sealed.items():
            if '/bmin_r2_limited_validation_retry3_20261005/' in path:
                member=path.split('/bmin_r2_limited_validation_retry3_20261005/')[1]
            elif '/received/candidate/' in path:
                member='fixed_received/candidate/'+path.split('/received/candidate/')[1]
            else:
                absent.append(path);continue
            if member in names:
                raw=z.read(member)
                check(digest(raw)==pin['sha256'] and len(raw)==pin['bytes'],'preseal_member:'+member)
                matched.append(member)
            else: absent.append(path)
        out={'scope':'Read-only archive/data comparisons; supplied code never imported or run','code_manifest_files':len(manifest['files']),'source_before_after_equal':before==after,'exact_extractions':len(j('EXTRACTION_MAP.json')),'planned_inputs':len(expected),'unique_ids':len({k[0] for k in expected}),'accounted_inputs':len(actual),'engines':engine_checks,'profile_cache':dict(collections.Counter(x['mode'] for x in j('results/PYTHON_RESULTS.json')['cache_records'])),'preseal_sha256':digest(z.read('PRE_TEST_SEAL.json')),'preseal_pins':len(seal['files']),'preseal_after_record_count':len(after_seal),'preseal_members_directly_checked':len(matched),'preseal_pins_not_packaged_or_not_resolved':len(absent),'final_accounting_stale_false_fields':{k:sum(c.get(k) is False for c in accounting) for k in ('fixture_created','actual_call_bound')},'errors':errors}
        print(json.dumps(out,ensure_ascii=False,indent=2))
    elif mode == 'lines':
        p, start, end = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
        for i,s in enumerate(z.read(p).decode('utf-8-sig').splitlines(),1):
            if start <= i <= end: print(f'{i}: {s}')
    elif mode == 'structure':
        for p in sys.argv[2:]:
            o = j(p)
            print(p, type(o).__name__)
            if isinstance(o, dict):
                for k,v in o.items():
                    print(k, type(v).__name__, len(v) if isinstance(v,(list,dict,str)) else v)
                    if isinstance(v,list) and v:
                        print('first:', json.dumps(v[0], ensure_ascii=False)[:2000])
            elif isinstance(o,list):
                print(len(o),json.dumps(o[:1],ensure_ascii=False)[:2000])
