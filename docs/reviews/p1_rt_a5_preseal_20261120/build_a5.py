"""Build the preseal review copy from the frozen RT assembly and signed-source inputs."""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import shutil
import sys
import tempfile

HERE = Path(__file__).resolve().parent
OLD_GUARD = 'echo "RT_ASSEMBLY_INACTIVE: no operational seal or author field GO" >&2\nexit 2\n'
SCOPE = '''if [ "${1:-}" != ps_7_3_r45 ] || [ "${2:-}" != RJ ] || [ "${NP:-6}" != 6 ]; then
  echo "A5_SCOPE: reviewed entry is ps_7_3_r45 RJ NP6" >&2; exit 2
fi
if [ "$#" != 3 ] || [ "${3:-}" != --preflight-only ]; then
  if [ "$#" != 2 ] || [ "${A5_AUTHOR_GO:-}" != GO_NEW_PS73_RJ ]; then
    echo "A5_PENDING: explicit review and author release required for a fresh RJ" >&2; exit 2
  fi
fi
'''
PREREQ = '''# >>> RT prerequisites
rt_prerequisites() {
  [ -n "${RT_FIXTURE_SITE:-}" ] || die "original NP6 fixture site required"
  local out
  out=$("$PY" -I -B "$KIT/a5_precheck.py" "$RT_FIXTURE_SITE" --lmp-sha "$LMP_SHA" --bed-input "$WORK_ROOT/$BED/in") || {
    echo "$out"; die "A3 original-site reread or historical A4 binding failed"
  }
  echo "$out"
  out=$("$PY" -I -B "$KIT/rt_dispatch_a5.py" orig_grid "$WORK_ROOT" "$BED" "$JOB") || {
    echo "$out"; die "original writer grid or deck failed"
  }
  echo "$out"
  GRAMMAR_REC+=("rt_grammar_prereq=PASS" "orig_grid_prereq=PASS"
                "rt_grammar_verdict=$KIT/a3_return.json" "rt_grammar_verdict_sha256=@A3@"
                "a3_readback_reader_sha256=@READER@" "a4_historical_sha256=@A4@")
}
# <<< RT prerequisites'''

def load(name, path):
    spec = importlib.util.spec_from_file_location(name,path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def swap(text,before,after,count=1):
    if text.count(before) != count:
        raise ValueError("candidate source anchor changed: " + before[:60])
    return text.replace(before,after)

def embedded_sources(reader):
    scripts = {}
    for node in ast.parse(reader).body:
        if not isinstance(node,ast.Assign) or not isinstance(node.value,ast.Call):
            continue
        call = node.value
        if isinstance(call.func,ast.Name) and call.func.id == "_embed":
            name, encoded = map(ast.literal_eval,call.args[:2])
            scripts[name] = bytes.fromhex(encoded)
    if set(scripts) != {"rt_numeric","rt_binding","rt_contract","history_closure"}:
        raise ValueError("unexpected reader source closure")
    return scripts

def active_rules(kit):
    rules=json.loads((kit/"active_rules.json").read_bytes())
    active={r["id"]:r for r in rules["rules"]}
    if len(active)!=24:
        raise ValueError("historical active rule set changed")
    edits={
        "parse_complete":"G2cp 30열과 연속성의 전역 W·칸별 W 및 표본수를 판독한다.",
        "stage_rc":"UN 뒤 RT1·RT2의 완료/건너뜀과 rc를 기록하고 그 뒤 UK를 처리한다.",
        "restore_complete":"rev5_g2cp, RT 단계·체크포인트 결속, G2cp, 연속성 두 가지와 문법 사전 점검을 확인한다. 새 RJ 증서 원바이트 해시와 발행 전 장부 접두부를 서로 결속하고 완료 영수증과 함께 읽는다.",
        "grammar_prereq":"새 7:3 RJ의 RT 문법 사전 점검은 rt_grammar_prereq로 추가 기록한다.",
    }
    for rule,addition in edits.items():
        active[rule]["rule"] += " "+addition
    rules["rules"].extend([
        {"id":"g2cp_roundtrip","rule":"RT1/RT2 체크포인트와 경로를 결속한다. 쌍·원 쓰기 격자·전역 및 칸별 하중 연속성은 등록 §15-5b와 판독한다.",
         "where":"rt_contract_a5.py:evaluate","where_exists":True,
         "witness":["test_rt_numeric","test_rt_binding","test_rt_contract","test_a5 corrected production parsers"]},
        {"id":"rt_grammar_prereq","rule":"A3 원 위치 367546의 고정 소스·실행 파일·원 입력을 재대조해 20검사 모두 참, A4의 역사 7:3 사전 셈 PASS를 요구한다.",
         "where":"a5_precheck.py:check_site","where_exists":True,
         "witness":["test_a5 full preflight","test_a5 original path","test_rt_fixture","test_rt_prereq"]},
    ])
    return (json.dumps(rules,ensure_ascii=False,indent=2)+"\n").encode("utf8")

def inventory(root, files):
    ordered = sorted(files, key=lambda p:p.relative_to(root).parts)
    return "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root).as_posix()}\n" for p in ordered).encode("ascii")

def canonical_parent(kit):
    # Reproduce the POSIX parent metadata on hosts with case-folded paths or CRLF.
    path = kit / "RT_DECK_LAYER.json"
    description = json.loads(path.read_bytes())
    saved = description["preserved"]
    description["preserved"] = {k:saved[k] for k in sorted(saved,key=lambda k:PurePosixPath(k).parts)}
    path.write_bytes((json.dumps(description,ensure_ascii=False,indent=2)+"\n").encode("utf8"))
    hist = kit/"history_test"
    listing = hist/"RT_HISTORY_SNAPSHOT_SHA256SUMS"
    listing.write_bytes(inventory(hist,(p for p in hist.iterdir() if p.is_file() and p!=listing)))
    listing = kit/"RT_ASSEMBLY_SHA256SUMS"
    listing.write_bytes(inventory(kit,(p for p in kit.rglob("*") if p.is_file() and p!=listing)))
    if hashlib.sha256(listing.read_bytes()).hexdigest()!="e14f8f2687d04c3cbe0a682fca5b87283e2271d7c05c1dd95ebc15c141965010":
        raise ValueError("preceding 128-file POSIX assembly differs")

def add_candidate(repo,kit):
    reviews = repo/"docs/reviews"
    checker = load("a5_checker_source",HERE/"a5_precheck.py")
    anchors = checker.ANCHORS
    recheck = reviews/"p1_rt_fixture_readback_20261118"
    reader = load("a3_builder",recheck/"build_reader.py").render()
    fixed = {
        "a3_inputs.json":(recheck/"fixture_evidence.json").read_bytes(),
        "a3_return.json":(reviews/"p1_rt_fixture_readback_return_20261120/readback.json").read_bytes(),
        "a3_readback.py":(recheck/"readback.py").read_bytes(),
        "a3_corrected_reader.py":reader,
        "a4_continuity.json":(reviews/"nonrint_go_returns_20261120/a4/continuity.json").read_bytes(),
        "a4_receipt.json":(reviews/"nonrint_go_returns_20261120/a4/receipt.json").read_bytes(),
    }
    if {name:hashlib.sha256(raw).hexdigest() for name,raw in fixed.items()} != anchors:
        raise ValueError("versioned A3 or A4 artifacts differ from the review inputs")
    sources = embedded_sources(reader)
    # Dispatch and restore stay on the same numeric/atom reader that passed at A3.
    contract = swap(sources["rt_contract"],b"_load('rt_numeric',",b"_load('rt_numeric_a5',")
    restore = swap((kit/"rt_restore.py").read_bytes(),b"import rt_contract as C",b"import rt_contract_a5 as C")
    def bound(text):
        return text.replace("@A3@",anchors["a3_return.json"]).replace("@READER@",anchors["a3_corrected_reader.py"]).replace("@A4@",anchors["a4_continuity.json"])
    restore = swap(restore,b"from rt_publish import publish_new",b"import a5_certificate")
    restore = swap(restore,b"publish_new(a.root/a.bed/a.job,r)",
                   b"a5_certificate.issue(a.root/a.bed/a.job,r,Path(a.kit or Path(__file__).resolve().parent))")
    begin=restore.index(b"    old=legacy_reader",restore.index(b"def job_restored("))
    finish=restore.index(b"\ndef main(",begin)
    restore=restore[:begin]+b"    return a5_certificate.admits(Path(root)/bed/job,Path(kit or Path(__file__).resolve().parent))\n"+restore[finish:]
    dispatch = swap((kit/"rt_dispatch.py").read_bytes(),b"import rt_restore as R",b"import rt_restore_a5 as R")
    runner = (kit/"run_unload_rt_candidate.sh").read_text(encoding="utf8")
    runner = swap(runner,OLD_GUARD,SCOPE)
    first = runner.index("# >>> RT prerequisites")
    last = runner.index("# <<< RT prerequisites",first)+len("# <<< RT prerequisites")
    runner = runner[:first]+bound(PREREQ)+runner[last:]
    runner = swap(runner,'exec bash "$KIT/run_unload_rt_candidate.sh"','exec bash "$KIT/run_unload_a5_candidate.sh"')
    runner = swap(runner,'"$KIT/rt_dispatch.py"','"$KIT/rt_dispatch_a5.py"',count=2)
    runner = runner.replace("RT_ASSEMBLY_SHA256SUMS","A5_SHA256SUMS")
    if 'done < "$SELF_DIR/A5_SHA256SUMS"' not in runner or 'sha256sum -c --quiet A5_SHA256SUMS' not in runner:
        raise ValueError("candidate manifest checks not wired")
    additions = {**fixed,"a5_precheck.py":(HERE/"a5_precheck.py").read_bytes(),
                 "a5_certificate.py":(HERE/"a5_certificate.py").read_bytes(),
                 "A5_active_rules.json":active_rules(kit),
                 "rt_contract_a5.py":contract,"rt_numeric_a5.py":sources["rt_numeric"],
                 "rt_restore_a5.py":restore,"rt_dispatch_a5.py":dispatch,
                 "run_unload_a5_candidate.sh":runner.encode("utf8")}
    for name,raw in additions.items():
        with (kit/name).open("xb") as stream:
            stream.write(raw)
    with (kit/"A5_SHA256SUMS").open("xb") as stream:
        stream.write(inventory(kit,(p for p in kit.rglob("*") if p.is_file() and p.name!="A5_SHA256SUMS")))

def build(repo,destination):
    repo, destination = Path(repo).resolve(strict=True), Path(destination)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(destination)
    with tempfile.TemporaryDirectory(dir=destination.parent) as tmp:
        kit = Path(tmp)/"candidate"
        previous = load("a5_preceding_assembly",repo/"docs/reviews/p1_rt_fixture_runner_preparation_20261117/prepare_assembly.py")
        previous.build(repo/"docs/data/ps45_unload_20261009",kit)
        canonical_parent(kit)
        add_candidate(repo,kit)
        # Reserve the destination exclusively. Publish the identifying manifest last.
        destination.mkdir()
        try:
            for p in sorted(kit.rglob("*")):
                target = destination/p.relative_to(kit)
                if p.is_dir():
                    target.mkdir()
                elif p.name != "A5_SHA256SUMS":
                    shutil.copyfile(p,target)
            shutil.copyfile(kit/"A5_SHA256SUMS",destination/"A5_SHA256SUMS")
        except BaseException:
            shutil.rmtree(destination)
            raise

if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("destination",type=Path)
    p.add_argument("--repo",type=Path,default=HERE.parents[2])
    args=p.parse_args()
    build(args.repo,args.destination)
    print(hashlib.sha256((args.destination/"A5_SHA256SUMS").read_bytes()).hexdigest(),"A5_SHA256SUMS")
