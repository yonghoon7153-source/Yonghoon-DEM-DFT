import difflib,hashlib,io,json,pathlib,posixpath,subprocess,types,zipfile
S=pathlib.Path('/workspace/.cloud-setup/nonrint');O=S/'final-publication-audit';R='/workspace/Yonghoon-DEM-DFT';BASE='7799a2ff64ba462b42ce05edd3e63b7c2854d557';sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git','-C',R,*a])
source=git('show',BASE+':scripts/check_doc_refs.py');m=types.ModuleType('checker');m.__file__=R+'/scripts/check_doc_refs.py';exec(compile(source,m.__file__,'exec'),m.__dict__);base=set(git('ls-tree','-r','--name-only','-z',BASE).decode().strip('\0').split('\0'));out={}
for tag,en in [('dem-gen2','dem_protocol_gen2_design_review_evidence_20261023'),('d3','mixer_d3_design_v2_evidence_20261023')]:
 E='docs/reviews/'+en+'/';N=S/'normalized-imports'/tag;A=S/(tag+'-deliverables');p=json.loads((N/E/'import-paths/provenance.json').read_text());raw=(N/p['archive']).read_bytes();z=zipfile.ZipFile(io.BytesIO(raw));names=set(z.namelist());oldfiles={str(f.relative_to(A)) for f in (A/'docs').rglob('*') if f.is_file()};newfiles={str(f.relative_to(N)) for f in (N/'docs').rglob('*') if f.is_file()};checks={};fail=[]
 def ck(k,v,d=None):
  checks[k]={'ok':bool(v),'detail':d}
  if not v:fail.append(k)
 ck('archive_exact_original_files',len(names)==len(z.namelist())==p['original_docs_count'] and names==oldfiles==set(p['original_members']) and all(z.read(n)==(A/n).read_bytes() and sha(z.read(n))==p['original_members'][n] for n in names),{'original':len(names),'import':len(newfiles)});ck('archive_hash_crc',sha(raw)==p['archive_sha256'] and z.testzip() is None)
 changed={n for n in names if z.read(n)!=(N/n).read_bytes()};declared={r['path'] for r in p['changed_preexisting_files']};ck('changes_exhaustive',changed==declared|{p['current_outer_manifest']},sorted(changed));ck('changed_hashes',all(sha(z.read(r['path']))==r['original_sha256'] and sha((N/r['path']).read_bytes())==r['import_sha256'] for r in p['changed_preexisting_files']))
 substitutions=p['token_substitutions'];mds={r['doc'] for r in substitutions};mds.add(E+'README.md');bad=[]
 for n in mds:
  old=z.read(n).decode();expected=old
  for r in substitutions:
   if r['doc']==n:
    token='`'+r['original_token']+'`';newtoken='`'+r['import_token']+'`';ck('token_count:'+n+':'+r['original_token'],old.count(token)==r['occurrences']);expected=expected.replace(token,newtoken)
  if tag=='dem-gen2' and n==E+'README.md':
   expected=expected.replace('| `author/` | 작성자 자료 16개를 바이트 그대로 복사. 최초 v1·수정 v2, 작성자 산술 탐침·결과, G2IR 대응표·diff, 두 원 manifest 포함. 그 안의 ‘재확인 대기’는 당시 기록이며 고치지 않음 |', '| `author/` | 반입 전 작성자 자료 16개의 원 바이트는 원본 ZIP에 보존. 현재 live 초안 두 개는 경로만 정규화했고 두 manifest는 live 반입 지문이다. 최초 v1·수정 v2, 작성자 산술 탐침·결과, G2IR 대응표·diff, 두 원 manifest는 원본 ZIP에서 확인한다. 그 안의 ‘재확인 대기’는 당시 기록이며 고치지 않음 |')
  actual=(N/n).read_text()
  if n==E+'README.md':
   if not actual.startswith(expected+'\n## 경로 정규화 반입의 원본·현재 구분\n'):bad.append(n)
  elif actual!=expected:bad.append(n)
 ck('markdown_only_tokens_and_context_append',not bad,bad)
 diff=''.join(''.join(difflib.unified_diff(z.read(n).decode().splitlines(True),(N/n).read_text().splitlines(True),fromfile='original/'+n,tofile='import/'+n)) for n in sorted(declared))
 ck('stored_diff_exact',diff==(N/E/'import-paths/original-to-import.diff').read_text())
 # Current affected manifests and the same originals retain their own relative context.
 for mn in [r['path'] for r in p['live_import_manifests']]+[p['current_outer_manifest']]:
  for version in ['original','import']:
   contents=z.read(mn) if version=='original' else (N/mn).read_bytes();bad=[];count=0
   for line in contents.decode().splitlines():
    if not line or line.startswith('#'):continue
    h,rel=line.split('  ',1);member=posixpath.normpath(posixpath.join(posixpath.dirname(mn),rel));count+=1
    try:data=z.read(member) if version=='original' else (N/member).read_bytes()
    except (KeyError,FileNotFoundError):bad.append(member);continue
    if sha(data)!=h:bad.append(member)
   ck(version+'_manifest:'+mn,not bad,{'count':count,'bad':bad})
 # Unchanged source/data/tool payloads are preserved separately from metadata JSON.
 changedscience=[n for n in changed if n.endswith(('.py','.log','.csv'))];ck('source_data_tool_unchanged',not changedscience,changedscience)
 inv=base|newfiles;valid=inv|{str(p) for f in inv for p in pathlib.PurePosixPath(f).parents};virtual='/virtual/repo'
 def exists(q):return posixpath.normpath(q).removeprefix(virtual+'/') in valid
 m.os=types.SimpleNamespace(path=types.SimpleNamespace(exists=exists,join=posixpath.join,dirname=posixpath.dirname));missing=[]
 for n in sorted(x for x in newfiles if x.endswith('.md')):
  g=m.scan_text((N/n).read_text(),virtual,set(),set(),resolve=lambda _:True,rel=n);missing.extend((n,t) for t in g['missing'])
 ck('static_canonical_path_scan',not missing,{'missing':missing,'actual_gate':False})
 if tag=='dem-gen2':
  q=json.loads((N/E/'import-provenance.json').read_text());ck('current_request_hash',sha((N/q['request_import_path']).read_bytes())==q['request_import_sha256']);ck('audit_old_current_hashes',sha(z.read(E+'package-audit/audited_request.md'))==q['package_audit']['audited_request_sha256'] and sha((N/E/'package-audit/audited_request.md').read_bytes())==q['package_audit']['live_audited_request_sha256']);ck('original_author_hashes',all(sha(z.read(E+'author/'+n))==h for n,h in q['preserved_author_files'].items()));ck('independent_files_unchanged',all(sha((N/E/'independent'/n).read_bytes())==h for n,h in q['preserved_independent_files'].items()))
 else:
  q=json.loads((N/E/'PACKAGE_PROVENANCE.json').read_text());ck('d3_current_document_hashes',all(sha((N/'docs/reviews'/n).read_bytes())==h for n,h in q['final_import_documents'].items()));ck('d3_original_document_hashes',all(sha(z.read('docs/reviews/'+n))==h for n,h in q['archived_pre_import_documents'].items()));ck('d3_first_review_input',sha((N/E/'original-draft/mixer_d3_se_flowability_anchor_design_v2_20261023.md').read_bytes())=='24fda5535c511aa5d8930d2971003122180046519c693c2e55dcdec3fde39373')
 out[tag]={'status':'PASS' if not fail else 'MISMATCH','failures':fail,'checks':checks}
(O/'normalized-imports-recheck.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:{'status':v['status'],'failures':v['failures'],'checks':len(v['checks'])} for k,v in out.items()},indent=2))
