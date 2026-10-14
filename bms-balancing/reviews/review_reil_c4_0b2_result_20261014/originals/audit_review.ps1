# Reviewer-owned byte/JSON/text audit only. Never executes received code or tests.
$ErrorActionPreference = 'Stop'
$rr = [IO.Path]::GetFullPath($PSScriptRoot)
$idx = Get-Content -LiteralPath (Join-Path $rr 'CAPTURE_INDEX.json') -Raw | ConvertFrom-Json
$records = @()
foreach ($c in $idx) {
    $p = Join-Path $rr $c.capture
    $raw = [IO.File]::ReadAllBytes($p)
    $header = [Text.Encoding]::ASCII.GetBytes(('blob ' + $raw.Length + [char]0))
    $both = [byte[]]::new($header.Length + $raw.Length)
    [Array]::Copy($header,0,$both,0,$header.Length)
    [Array]::Copy($raw,0,$both,$header.Length,$raw.Length)
    $sha = [Security.Cryptography.SHA1]::Create()
    try { $blob = ([BitConverter]::ToString($sha.ComputeHash($both))).Replace('-','').ToLowerInvariant() }
    finally { $sha.Dispose() }
    if ($blob -ne $c.git_blob) { throw "Git capture mismatch: $($c.capture)" }
    $records += [ordered]@{capture=$c.capture;repo_path=$c.repo_path;ref=$c.ref;bytes=$raw.Length;git_blob=$blob;sha256=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$source = Join-Path $rr 'source'
$ev = Join-Path $source 'evidence/reil_c4_0b2_20261014'
$prior = Join-Path (Split-Path $rr -Parent) 'reil_c4_0b1_fix2_review_20261014/source/bms-balancing'
$hashChecks = @()
foreach ($file in @('02_red.source_sha256.txt','03_green.source_sha256.txt','04_dryrun.source_sha256.txt','05_source_sha256_end.txt')) {
    foreach ($line in (Get-Content -LiteralPath (Join-Path $ev $file))) {
        if ($line -notmatch '^([a-f0-9]{64})\s+(.+)$') { throw "Unexpected source hash line: $file" }
        $expected=$Matches[1]; $rel=$Matches[2]
        $base=$source
        if ($file -eq '02_red.source_sha256.txt') {
            if ($rel -eq 'scripts/reil_c4_hb.py') { $base=Join-Path $rr 'red_fixed' }
            elseif ($rel -eq 'scripts/reil_c4_h.py') { $base=$prior }
        }
        $actual=(Get-FileHash -LiteralPath (Join-Path $base $rel) -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actual -ne $expected) { throw "Producer source hash mismatch: $file $rel" }
        $hashChecks += @{list=$file;path=$rel;sha256=$actual}
    }
}
$newTest = $records | Where-Object capture -eq 'source/tests/test_reil_c4_0b2.py'
$fixedTest = $records | Where-Object capture -eq 'red_fixed/tests/test_reil_c4_0b2.py'
if ($newTest.sha256 -ne $fixedTest.sha256) { throw 'Test changed after pre-RED commit' }
$attachment='C:/Users/Administrator/Downloads/REIL_C4_0B2_RESULT_REVIEW_SEND_20261014.md'
$attachmentSha=(Get-FileHash -LiteralPath $attachment -Algorithm SHA256).Hash.ToLowerInvariant()
$send=$records | Where-Object capture -eq 'source/docs/REIL_C4_0B2_RESULT_REVIEW_SEND_20261014.md'
if($attachmentSha -ne $send.sha256){throw 'Attachment differs from reviewed HEAD'}
$preserved=@()
foreach($rel in @('tests/test_reil_c4_0b1.py','tests/test_reil_c4_0b1_fix.py','tests/test_reil_c4_0b1_fix2.py','scripts/reil_c4_e3a.py','scripts/reil_c4_monitor.py','scripts/reil_c5_pilot.py')) {
    $old=(Get-FileHash -LiteralPath (Join-Path $prior $rel) -Algorithm SHA256).Hash.ToLowerInvariant()
    $now=(Get-FileHash -LiteralPath (Join-Path $source $rel) -Algorithm SHA256).Hash.ToLowerInvariant()
    if($old -ne $now){throw "Preserved source changed: $rel"}
    $preserved+=@{path=$rel;sha256=$now}
}
$compare=Get-Content -LiteralPath (Join-Path $rr 'COMPARE_FROM_PRIOR.json') -Raw | ConvertFrom-Json
if($compare.status -ne 'ahead' -or $compare.too_large){throw 'Incomplete ancestry comparison'}
$protected=@('bms-balancing/reil_c4_arrays','bms-balancing/reil_c6_rebuild','bms-balancing/evidence/reil_c4_0b1','bms-balancing/scripts/reil_p0.py','bms-balancing/scripts/reil_c6_profile.py')
$changes=@($compare.files | ForEach-Object {$_.filename})
foreach($prefix in $protected){if(@($changes | Where-Object {$_.StartsWith($prefix)}).Count){throw "Protected path changed: $prefix"}}
$end=Get-Content -LiteralPath (Join-Path $ev '05_end.json') -Raw | ConvertFrom-Json
$steps=@('01_identity','02_red','03_green','04_dryrun') | ForEach-Object {Get-Content -LiteralPath (Join-Path $ev ($_+'.meta.json')) -Raw | ConvertFrom-Json}
foreach($s in $steps){$decl=$end.steps.($s.step);if($s.elapsed_s -ne $decl.elapsed_s -or $s.rc -ne $decl.rc -or $s.timed_out){throw 'Stage record mismatch'}}
$sum=($steps | Measure-Object elapsed_s -Sum).Sum
if([Math]::Abs($sum-$end.compute_sum_s) -gt 0.000001){throw 'Stage sum mismatch'}
$red=Get-Content -LiteralPath (Join-Path $ev '02_red.stdout.log') -Raw
$green=Get-Content -LiteralPath (Join-Path $ev '03_green.stdout.log') -Raw
if($red -notmatch '42 failed, 1 passed' -or $green -notmatch '114 passed'){throw 'Reported test count mismatch'}
$stderr=@(Get-ChildItem -LiteralPath $ev -Filter '*.stderr.log' | Select-Object Name,Length)
if(@($stderr | Where-Object Length -ne 0).Count -ne 0 -or $stderr.Count -ne 4){throw 'Unexpected stderr lengths'}
$testText=Get-Content -LiteralPath (Join-Path $source 'tests/test_reil_c4_0b2.py') -Raw
$namedTests=[regex]::Matches($testText,'(?m)^def test_').Count
if($namedTests -ne 39){throw 'Named test count mismatch'}
[ordered]@{
    kind='REVIEWER_READ_ONLY_BYTE_TEXT_AUDIT';reviewed_ref='5810f35559c183a4aafeb91f650e354ba0fbe1a5'
    captured_files=$records.Count;all_git_blob_matches=$true;records=$records
    attachment_sha256=$attachmentSha;attachment_matches=$true
    pre_red_test_matches_head=$true;source_hash_list_checks=$hashChecks
    preserved_against_previous_review=$preserved;protected_prefixes_unchanged_in_git_compare=$protected
    compare_status=$compare.status;commits_ahead=$compare.ahead_by
    steps=@($steps | Select-Object step,rc,elapsed_s,timeout_s,head_start,head_end,timed_out)
    step_elapsed_sum=$sum;compute_limit_s=1560;producer_work_snapshot_s=2502.9;whole_work_completion_observed=$false
    named_new_tests=$namedTests;new_cases=43;red_failed=42;red_passed=1;green_passed=114;stderr=$stderr
    limits=@('This audit reads preserved records; no producer commands were rerun.','Git comparison proves fixed-commit differences, not continuous execution-host preservation.','2502.9 seconds precedes commit, push and final documents.','Own review bookkeeping does not constitute permission to execute C4.')
    received_code_or_test_execution=0;COMSOL=0;raw_REIL_data_opened=0;new_execution_approval=$false
} | ConvertTo-Json -Depth 20
