"""Package existing independent review evidence; performs no scientific computation."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys, zipfile

ROOT=Path(__file__).resolve().parent
NAME='EVIDENCE_RINT2_SEAL_ROUND2_f40d005ac_20261117'
STAGE=ROOT/(NAME+'_files')
ZIP=ROOT/(NAME+'.zip')
assert not STAGE.exists() and not ZIP.exists(), 'Keep previous deliveries; use a new output name.'
env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0')
candidate=ROOT/'candidate_source'
checks=subprocess.run(['git','-c','safe.directory='+candidate.as_posix(),'-C',str(candidate),'diff','--exit-code','HEAD','--'],env=env,capture_output=True,check=True)
untracked=subprocess.run(['git','-c','safe.directory='+candidate.as_posix(),'-C',str(candidate),'ls-files','--others','--exclude-standard'],env=env,capture_output=True,check=True)
assert not checks.stdout and not untracked.stdout
verification=subprocess.run([sys.executable,'-I','-B',str(ROOT/'verify_input.py'),'--zip',str(Path('<WINHOME>/Downloads/codex_rint2_seal_round2_f40d005ac_20261117.zip'))],capture_output=True,check=True)
input_check=json.loads(verification.stdout)
(ROOT/'final_invariants.json').write_text(json.dumps({'input':input_check,'candidate_tracked_diff':'EMPTY','candidate_untracked':'EMPTY','remote_repo_blobs':'84/84','note':'No operational repository, ledger, or seal written.'},indent=2)+'\n',encoding='utf-8')
prep=ROOT.parent/'rint2_reproduction_prepare_test2_20261117/PREPARATION.json'
assert prep.is_file();shutil.copy2(prep,ROOT/'reproduction_preparation_check.json')
STAGE.mkdir()
paths=[]
paths.extend(p for p in (ROOT/'input').rglob('*') if p.is_file())
paths.extend(p for p in (ROOT/'measurement_review').rglob('*') if p.is_file() and '__pycache__' not in p.parts)
for sub in ('seal_form_review/scripts','seal_form_review/logs'):
    paths.extend(p for p in (ROOT/sub).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
paths.append(ROOT/'seal_form_review/REPORT.md')
paths.extend(p for p in (ROOT/'resume_review').iterdir() if p.is_file())
root_files=['FINAL_REVIEW_RINT2_SEAL_ROUND2_f40d005ac_20261117.md','REPRODUCE.md','prepare_reproduction.py',
 'verify_input.py','intake.json','source_acquisition.json','source_checkout.json','remote_pin_checks.json',
 'final_invariants.json','reproduction_preparation_check.json','package_evidence.py']
paths.extend(ROOT/n for n in root_files)
assert len(paths)==len(set(paths))
for p in paths:
    rel=p.relative_to(ROOT);dest=STAGE/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
readme='''# Rint ② 봉인 전 묶음 2/2 — 독립 판정 전달

판정: 조건부 GO. 봉인 꼴·기존 측정 근거의 승계에 한정하며 실행 GO가 아니다.
먼저 FINAL_REVIEW_RINT2_SEAL_ROUND2_f40d005ac_20261117.md를 읽는다.
새 P1/P2/P3는 없고 네 미정값·최종 봉인 확인·RCA-11 한정이 남는다.

input/은 원 첨부의 373파일 그대로다. 원첨부 내부 manifest와 이 바깥 SHA256SUMS는 별개다.
intake.json은 최초 로컬 검사 기록이다. 그 뒤 원격 핀 귀속84/84는 remote_pin_checks.json에 추가됐다.
final_invariants.json은 입력/후보 소스가 그대로인지 마지막에 확인한 기록이다.
하위 폴더 세 개는 독립 탐침·출력·상세 보고다. 작성측 내부 결과와 합산하지 않는다.

재현은 REPRODUCE.md를 따른다. 로컬 고정 Git 객체와 새 scratch가 필요하다.
원격 fetch, 엔진, 현장, 실제 σ, 운영 원장/봉인, 전체 gate를 실행하지 않는다.
시험 전용 네 값과 합성 Git 커밋은 실제 봉인에 사용하지 않는다.
이 ZIP에는 로컬 검토 경로가 포함된다. 그대로 공개 리포에 반입하지 않는다.
'''
(STAGE/'README.md').write_text(readme,encoding='utf-8')
members=sorted(p for p in STAGE.rglob('*') if p.is_file())
lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(STAGE).as_posix() for p in members]
(STAGE/'SHA256SUMS').write_bytes(('\n'.join(lines)+'\n').encode('utf-8'))
members=sorted(p for p in STAGE.rglob('*') if p.is_file())
with zipfile.ZipFile(ZIP,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in members:z.write(p,p.relative_to(STAGE).as_posix())
with zipfile.ZipFile(ZIP) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(set(z.namelist()))==len(members)
    for line in z.read('SHA256SUMS').decode().splitlines():
        want,name=line.split('  ',1);assert hashlib.sha256(z.read(name)).hexdigest()==want,name
    for p in members:assert z.read(p.relative_to(STAGE).as_posix())==p.read_bytes()
receipt={'zip':str(ZIP),'bytes':ZIP.stat().st_size,'sha256':hashlib.sha256(ZIP.read_bytes()).hexdigest(),
 'files':len(members),'external_hash_rows':len(lines),'crc':'PASS','all_member_bytes':'MATCH',
 'report':str(ROOT/root_files[0]),'report_sha256':hashlib.sha256((ROOT/root_files[0]).read_bytes()).hexdigest()}
(ROOT/'DELIVERY_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
