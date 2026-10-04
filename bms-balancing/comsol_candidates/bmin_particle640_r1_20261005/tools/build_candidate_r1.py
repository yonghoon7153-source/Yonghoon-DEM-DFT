"""B-min 후보 r1 — v1 (manifest 3722a51f…) 에서 준비 검토의 국소 보완 (BMIN-N1 · BMIN-N2) 만 결정적으로 적용한다.
텍스트 치환 · 블록 교체만 — 후보 코드의 import · 구문 해석 · 컴파일 · 실행 0.

  python3 tools/build_candidate_r1.py            # r1 꾸러미 루트 (comsol_candidates/bmin_particle640_r1_20261005) 에서
  python3 tools/build_candidate_r1.py --check    # 쓰지 않고 지금 candidate/ 와 R1_LITERAL_CHANGES.json 이 이 결과와 같은지만 본다

입력: ../bmin_particle640_20261004/candidate/ (v1 — CODE_MANIFEST 와 8 파일 바이트를 먼저 대조, 다르면 멈춘다).
바뀌는 것: PARENT_COMMAND.ps1 (GNativeAxis 추가 · GFields 교체 · 호출 셋 · GDecision 의 transient DOF 구조 검사) ·
src/diagnostic_consumer.py (mesh_evidence 교체) · CONTRACT.json (expected_transient_dof.status 문구) · 봉인 셋 (manifest SHA).
그대로: src/Bmin640Candidate.java · src/candidate_entry.py (바이트 동일).
"""
import hashlib
import json
import pathlib
import sys

PKG = pathlib.Path(__file__).resolve().parent.parent
V1 = PKG.parent / "bmin_particle640_20261004" / "candidate"
OUT = PKG / "candidate"
V1_MANIFEST = "3722a51fb1caeddd72fca3751f2ed78ed3e05d5f1938fa452503b3fa5c421a03"
V1_SIDE = {"COMMAND_MAP.json": "1394bf1b390c958c69be644082f5ee67f0bce11353bd2df2529e377328d2e654",
           "NATIVE_APPROVAL_FIELD_SPEC.json": "8a84f8a8aa6c298c2266a4012256dd4a8f274951adb238695be65909f0cb0c1c"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def stop(msg):
    raise SystemExit("✗ " + msg)


def apply(text, table, label):
    for before, after, count, _finding in table:
        got = text.count(before)
        if got != count:
            stop(f"{label}: {before[:60]!r} 횟수 {got} ≠ {count}")
        text = text.replace(before, after)
    return text


def segment(text, start, end, label):
    if text.count(start) != 1 or (end is not None and text.count(end) != 1):
        stop(f"{label}: 경계 표식이 유일하지 않다 ({start!r} · {end!r})")
    a = text.index(start)
    b = len(text) if end is None else text.index(end)
    if b <= a:
        stop(f"{label}: 경계 순서")
    return a, b


def crlf_text(raw, label):
    if raw.count(b"\r\n") != raw.count(b"\n") or b"\r\n" not in raw:
        stop(f"{label}: v1 이 전부 CRLF 가 아니다")
    return raw.decode("ascii").replace("\r\n", "\n")


# ---------------------------------------------------------------- BMIN-N2 — consumer mesh_evidence
NEW_MESH = r"""def mesh_evidence(c,batch,console):
    lines=console.splitlines()
    for expected in c['mesh_readback_required']:need(lines.count(expected)==1,'MESH_READBACK:'+expected)
    # BMIN-N2: the transient DOF read-back is required I-3 evidence, taken only from the single Time-Dependent Solver section.
    opening=list(re.finditer(r'^<---- Time-Dependent Solver.*$',batch,re.M))
    closing=list(re.finditer(r'^----- Time-Dependent Solver.*-+>\s*$',batch,re.M))
    need(len(opening)==len(closing)==1 and opening[0].start()<closing[0].start(),'SOLVER_SECTION')
    pattern=r'Number of degrees of freedom solved for: (\d+) \(plus (\d+) internal DOFs\)\.'
    section=batch[opening[0].end():closing[0].start()]
    mentions=[x for x in section.splitlines() if 'Number of degrees of freedom' in x]
    need(len(mentions)==1,'TRANSIENT_DOF_READBACK_COUNT:'+str(len(mentions)))
    hit=re.search(pattern,mentions[0]);need(hit is not None,'TRANSIENT_DOF_READBACK_FORMAT')
    solved,internal=int(hit.group(1)),int(hit.group(2));need(solved>0,'TRANSIENT_DOF_READBACK_VALUE')
    want={'solved':c['expected_transient_dof']['solved'],'internal':c['expected_transient_dof']['internal']}
    outside=[{'solved':int(a),'internal':int(b)} for a,b in re.findall(pattern,batch[:opening[0].end()]+'\n'+batch[closing[0].start():])]
    same=solved==want['solved'] and internal==want['internal']
    return {'status':'PASS','required_lines':c['mesh_readback_required'],
            'transient_dof':{'solved':solved,'internal':internal,'line':mentions[0].strip()},
            'expected_transient_dof':want,'transient_dof_matches_expected':same,
            'transient_dof_difference':{'solved':solved-want['solved'],'internal':internal-want['internal']},
            'review_note':None if same else 'Observed transient DOF differs from the extrapolated expectation (2045 + 242*640); state the cause in the result review. Not a gate.',
            'dof_outside_transient_section':outside,
            'dof_policy':'I-3: exactly one well-formed DOF line inside the single Time-Dependent Solver section is required (missing, outside-only, ambiguous or malformed is incomplete); a difference from the extrapolated expectation is recorded, not a gate.'}
"""

# ---------------------------------------------------------------- BMIN-N1 — parent GNativeAxis + GFields
NEW_NATIVE_AND_FIELDS = r"""function GNativeAxis($Native,$Result,$Expected) {
    # BMIN-N1: the native terminal observation, checked by the parent on its own (child return, run/manifest binding, termination
    # evidence) and kept apart from comparison, configuration evidence, analysis and delivery acceptance. Labels are never copied unchecked.
    function GHas($Object,[string]$Key) {
        if ($null -eq $Object) { return $false }
        if ($Object -is [System.Collections.IDictionary]) { return $Object.Contains($Key) }
        return $null -ne $Object.PSObject.Properties[$Key]
    }
    function GStruct($Object) {
        return ($null -ne $Object -and (($Object -is [System.Collections.IDictionary] -and $Object.Count -gt 0) -or ($Object -is [pscustomobject] -and @($Object.PSObject.Properties).Count -gt 0)))
    }
    function GNumber($Value,[double]$Min,[double]$Max) {
        $v=0.0
        return ([double]::TryParse([string]$Value,[Globalization.NumberStyles]::Float,[Globalization.CultureInfo]::InvariantCulture,[ref]$v) -and -not [double]::IsNaN($v) -and -not [double]::IsInfinity($v) -and $v -ge $Min -and $v -le $Max)
    }
    if ($null -eq $Native -or $Native.returned -isnot [bool] -or -not $Native.returned -or $Native.invocation_succeeded -isnot [bool] -or $Native.native_rc -isnot [int] -or $Native.new_error -isnot [bool] -or $Native.new_error -or $Native.exception) { return @{native_completion='NOT_ESTABLISHED';cause='NATIVE_CHILD_RETURN_MISSING_OR_ERROR'} }
    if ($Native.native_rc -ne 0 -or -not $Native.invocation_succeeded) { return @{native_completion='NOT_ESTABLISHED';cause='NATIVE_CHILD_RC'} }
    if ($null -eq $Result) { return @{native_completion='NOT_ESTABLISHED';cause='TERMINATION_EVIDENCE_MISSING'} }
    if (-not (GStruct $Result) -or $Result.run_id -cne $Expected.run_id -or $Result.code_manifest_sha256 -cne $Expected.manifest_sha256) { return @{native_completion='NOT_ESTABLISHED';cause='RESULT_IDENTITY'} }
    if (-not (GStruct $Result.termination) -or -not (GStruct $Result.native_termination)) { return @{native_completion='NOT_ESTABLISHED';cause='TERMINATION_EVIDENCE_MISSING'} }
    $term=$Result.termination;$nt=$Result.native_termination;$bad=@{native_completion='NOT_ESTABLISHED';cause='TERMINATION_EVIDENCE_INVALID'}
    if ($nt.no_integration_after_termination -isnot [bool] -or -not $nt.no_integration_after_termination -or -not (GNumber $nt.reported_time 0 150)) { return $bad }
    if ($term.threshold_mol_m3 -cne '0' -or $term.active_guards -isnot [array] -or $term.stored_times_s -isnot [array] -or @($term.stored_times_s).Count -lt 3 -or $nt.step_count -ne @($term.stored_times_s).Count) { return $bad }
    if (-not (GNumber $term.final_time_s 0 150) -or -not (GNumber $term.safe_prefix_end_s 0 150) -or $term.final_time_s -cne $term.stored_times_s[-1]) { return $bad }
    $completion=$null
    if ($term.status -ceq 'NORMAL_150S_REACHED') {
        if ($nt.status -cne 'NATIVE_NORMAL_END_MATCHED' -or $null -ne $nt.stop_reason -or @($term.active_guards).Count -ne 0 -or -not (GNumber $term.final_time_s 150 150) -or -not (GNumber $term.safe_prefix_end_s 150 150)) { return $bad }
        $completion='NORMAL_150S_COMPLETED'
    } elseif ($term.status -ceq 'PROTECTIVE_STOP_OBSERVED') {
        if ($nt.status -cne 'NATIVE_PROTECTIVE_STOP_MATCHED' -or @($term.active_guards).Count -lt 1) { return $bad }
        $reasons=@{electrolyte_guard='Electrolyte minimum <= threshold';ocp_guard='OCP surface outside table';surface_guard='Invalid surface concentration'}
        $matched=$false
        foreach ($guard in $term.active_guards) {
            if (-not $reasons.ContainsKey($guard)) { return $bad }
            if ($nt.stop_reason -ceq $reasons[$guard]) { $matched=$true }
        }
        if (-not $matched -or -not (GNumber $term.t_minus 0 150) -or -not (GNumber $term.t_plus 0 150) -or [double]$term.t_minus -le 0 -or [double]$term.t_minus -ge [double]$term.t_plus -or $term.t_plus -cne $term.final_time_s -or $term.t_minus -cne $term.safe_prefix_end_s) { return $bad }
        $completion='PROTECTIVE_STOP'
    } else { return $bad }
    # The consumer label must agree with this observation; a disagreement is reported, never resolved by copying either side.
    if ($Result.native_completion -cne $completion) { return @{native_completion='NOT_ESTABLISHED';cause='CONSUMER_NATIVE_LABEL_MISMATCH'} }
    return @{native_completion=$completion;cause=$null}
}
function GFields([string]$Limited,$NativeAxis,$Result) {
    # Final three fields (B-min v2 section 6; BMIN-N1). native_completion is the parent's own native axis (GNativeAxis) and is kept when
    # configuration evidence, analysis or delivery later fails; only a parent-accepted normal result carries the consumer comparison verdict.
    $completion='NOT_ESTABLISHED';$cause='NATIVE_AXIS_NOT_EVALUATED'
    if ($null -ne $NativeAxis) { $completion=[string]$NativeAxis.native_completion;$cause=$NativeAxis.cause }
    $seen=$(if ($null -ne $Result) { [string]$Result.native_completion } else { $null })
    if ($Limited -ceq 'AWAITING_BMIN640_150S_EXTERNAL_ACCEPTANCE' -and $completion -ceq 'NORMAL_150S_COMPLETED') { return @{native_completion=$completion;native_completion_cause=$cause;evidence_validity=$Result.evidence_validity;mesh_comparison=$Result.mesh_comparison;consumer_native_completion_unverified=$seen} }
    return @{native_completion=$completion;native_completion_cause=$cause;evidence_validity='INVALID';mesh_comparison='INCONCLUSIVE';consumer_native_completion_unverified=$seen}
}
"""

# (이전, 이후, 횟수, 발견) — 부모의 나머지 연결 (블록 밖)
PS1_LITERALS = [
    ("\n$limited='INCOMPLETE'\nfunction BHash(", "\n$limited='INCOMPLETE'\n$bNativeAxis=$null\nfunction BHash(", 1, "BMIN-N1"),
    ("@{run_id=$c.run_id;manifest_sha256=$ManifestSha} $bClock.Elapsed.TotalSeconds\n",
     "@{run_id=$c.run_id;manifest_sha256=$ManifestSha} $bClock.Elapsed.TotalSeconds\n"
     "    $bNativeAxis=GNativeAxis $bRunReturn $result @{run_id=$c.run_id;manifest_sha256=$ManifestSha}\n", 1, "BMIN-N1"),
    ("fields=(GFields $limited $result)", "fields=(GFields $limited $bNativeAxis $result)", 3, "BMIN-N1"),
    ("$Result.mesh_readback.status -cne 'PASS' -or ",
     "$Result.mesh_readback.status -cne 'PASS' -or -not (GStruct $Result.mesh_readback.transient_dof) -or "
     "$Result.mesh_readback.transient_dof.solved -isnot [int] -or $Result.mesh_readback.transient_dof.solved -le 0 -or ", 1, "BMIN-N2"),
]


def dump(obj):
    return (json.dumps(obj, indent=2, ensure_ascii=True) + "\n").encode("ascii")


def main():
    check_only = "--check" in sys.argv[1:]
    v1m_raw = (V1 / "CODE_MANIFEST.json").read_bytes()
    if sha(v1m_raw) != V1_MANIFEST:
        stop("v1 CODE_MANIFEST 바이트 불일치")
    v1m = json.loads(v1m_raw)
    v1 = {}
    for f in v1m["files"]:
        b = (V1 / f["file"]).read_bytes()
        if len(b) != f["bytes"] or sha(b) != f["sha256"]:
            stop(f"v1 바이트 불일치: {f['file']}")
        v1[f["file"]] = b
    for name, h in V1_SIDE.items():
        b = (V1 / name).read_bytes()
        if sha(b) != h:
            stop(f"v1 바이트 불일치: {name}")
        v1[name] = b

    # BMIN-N2 — consumer
    c_text = crlf_text(v1["src/diagnostic_consumer.py"], "consumer")
    a, b = segment(c_text, "def mesh_evidence(", None, "consumer")
    c_text = c_text[:a] + NEW_MESH
    consumer = c_text.replace("\n", "\r\n").encode("ascii")

    # BMIN-N1 (+ N2 의 부모 구조 검사) — parent
    p_text = crlf_text(v1["PARENT_COMMAND.ps1"], "ps1")
    a, b = segment(p_text, "function GFields(", "\ntry {\n", "ps1")  # 행 머리의 주 try — 들여 쓴 try 는 BInvoke · finally 안에 있다
    p_text = p_text[:a] + NEW_NATIVE_AND_FIELDS + p_text[b + 1:]
    p_text = apply(p_text, PS1_LITERALS, "ps1")
    parent = p_text.replace("\n", "\r\n").encode("ascii")

    # CONTRACT — expected_transient_dof 의 상태 문구만 (BMIN-N2)
    contract_obj = json.loads(v1["CONTRACT.json"])
    if dump(contract_obj) != v1["CONTRACT.json"]:
        stop("v1 CONTRACT 직렬화가 왕복하지 않는다")
    if contract_obj["expected_transient_dof"]["status"] != "RECORD_ONLY":
        stop("v1 CONTRACT expected_transient_dof.status")
    contract_obj["expected_transient_dof"]["status"] = "OBSERVATION_REQUIRED_DIFFERENCE_RECORD_ONLY"
    contract = dump(contract_obj)

    java = v1["src/Bmin640Candidate.java"]
    entry = v1["src/candidate_entry.py"]
    files = [("src/Bmin640Candidate.java", java), ("src/diagnostic_consumer.py", consumer), ("src/candidate_entry.py", entry),
             ("PARENT_COMMAND.ps1", parent), ("CONTRACT.json", contract)]
    manifest_obj = dict(v1m)
    manifest_obj["previous_manifest_sha256"] = V1_MANIFEST
    manifest_obj["files"] = [{"file": f, "bytes": len(raw), "sha256": sha(raw)} for f, raw in files]
    if manifest_obj["approved"] is not False or manifest_obj["usable"] is not False:
        stop("승인 플래그")
    manifest = dump(manifest_obj)
    msha = sha(manifest)

    cmd = json.loads(v1["COMMAND_MAP.json"])
    cmd["manifest_sha256"] = msha
    for k in ("parent", "execute", "analyze"):
        if cmd[k]["argv"][-1] != V1_MANIFEST:
            stop(f"command map argv {k}")
        cmd[k]["argv"][-1] = msha
    if V1_MANIFEST in json.dumps(cmd):
        stop("command map 에 v1 manifest 가 남았다")
    spec = json.loads(v1["NATIVE_APPROVAL_FIELD_SPEC.json"])
    spec["code_manifest_sha256"] = msha
    if V1_MANIFEST in json.dumps(spec):
        stop("field spec 에 v1 manifest 가 남았다")

    outputs = {
        "src/Bmin640Candidate.java": java, "src/candidate_entry.py": entry, "src/diagnostic_consumer.py": consumer,
        "PARENT_COMMAND.ps1": parent, "CONTRACT.json": contract, "CODE_MANIFEST.json": manifest,
        "COMMAND_MAP.json": dump(cmd), "NATIVE_APPROVAL_FIELD_SPEC.json": dump(spec),
    }
    literal_doc = {"from": "../bmin_particle640_20261004/candidate (v1 · manifest " + V1_MANIFEST + ")", "to": "candidate (r1)",
                   "PARENT_COMMAND.ps1": [{"before": b0, "after": a0, "count": n, "finding": k} for b0, a0, n, k in PS1_LITERALS],
                   "blocks": "src/diagnostic_consumer.py mesh_evidence (BMIN-N2) and PARENT_COMMAND.ps1 GFields -> GNativeAxis + GFields (BMIN-N1) are declared in R1_CHANGE_BOUNDARIES.json",
                   "CONTRACT.json": {"expected_transient_dof.status": {"before": "RECORD_ONLY", "after": "OBSERVATION_REQUIRED_DIFFERENCE_RECORD_ONLY", "finding": "BMIN-N2"}}}
    package_outputs = {"R1_LITERAL_CHANGES.json": (json.dumps(literal_doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8")}
    bad = []
    for rel, raw in list(outputs.items()) + list(package_outputs.items()):
        p = (PKG if rel in package_outputs else OUT) / rel
        if check_only:
            if not p.is_file() or p.read_bytes() != raw:
                bad.append(rel)
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(raw)
        print(f"{'✗' if rel in bad else ('=' if check_only else '+')} {rel:36s} {len(raw):>9,d} B  {sha(raw)}")
    print(f"manifest {msha}")
    if bad:
        stop(f"재생성 바이트 불일치 {len(bad)}: {bad}")


if __name__ == "__main__":
    main()
