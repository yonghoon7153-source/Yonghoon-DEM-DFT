# Reviewer-owned byte and evidence audit. Does not invoke received Python, tests or optimizers.
$ErrorActionPreference='Stop'
$rr=[IO.Path]::GetFullPath($PSScriptRoot)
$cap=Get-Content -LiteralPath (Join-Path $rr 'CAPTURE_INDEX.json') -Raw | ConvertFrom-Json
$records=@()
foreach($c in $cap){
  $p=Join-Path $rr $c.capture
  $b=[IO.File]::ReadAllBytes($p)
  $header=[Text.Encoding]::ASCII.GetBytes(('blob '+$b.Length+[char]0))
  $all=[byte[]]::new($header.Length+$b.Length)
  [Array]::Copy($header,0,$all,0,$header.Length)
  [Array]::Copy($b,0,$all,$header.Length,$b.Length)
  $alg=[Security.Cryptography.SHA1]::Create()
  try{$actual=([BitConverter]::ToString($alg.ComputeHash($all))).Replace('-','').ToLowerInvariant()}finally{$alg.Dispose()}
  if($actual -ne $c.git_blob){throw "Git blob mismatch: $($c.repo_path)"}
  $records+=@{path=$c.repo_path;bytes=$b.Length;git_blob=$actual;sha256=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$bms=Join-Path $rr 'source/bms-balancing'
$intake='C:/Users/Administrator/Downloads/REIL_C4_0B1_FIX2_RESULT_REVIEW_SEND_20261014.md'
$intakeHash=(Get-FileHash -LiteralPath $intake -Algorithm SHA256).Hash.ToLowerInvariant()
$send=$records | Where-Object path -eq 'bms-balancing/docs/REIL_C4_0B1_FIX2_RESULT_REVIEW_SEND_20261014.md'
if($intakeHash -ne $send.sha256){throw 'Attached request differs from frozen repository file'}
$draft=$records | Where-Object path -eq 'bms-balancing/docs/REIL_C4_0B1_FIX2_CONTROLS_DRAFT_20261014.py.txt'
$test=$records | Where-Object path -eq 'bms-balancing/tests/test_reil_c4_0b1_fix2.py'
if($draft.sha256 -ne $test.sha256){throw 'Controls differ from preapproved draft'}
$com=Get-Content -LiteralPath (Join-Path $rr 'COMMIT_d9fac750.json') -Raw | ConvertFrom-Json
$committedCount=0
foreach($f in $com.files){
  $r=$records | Where-Object path -eq $f.filename
  if($null -eq $r -or $r.git_blob -ne $f.sha){throw "Committed file not captured exactly: $($f.filename)"}
  $committedCount++
}
$dirs=Get-Content -LiteralPath (Join-Path $rr 'DIRECTORY_IDENTITIES.json') -Raw | ConvertFrom-Json
$prior=$dirs | Where-Object { $_.ref -like 'c6787db2*' }
$current=$dirs | Where-Object { $_.ref -like '5eeedb4b*' }
$preserved=@()
foreach($d in $prior){
  $now=$current | Where-Object path -eq $d.path
  $selected=@($d.entries)
  foreach($e in $selected){
    $n=$now.entries | Where-Object path -eq $e.path
    if($null -eq $n -or $n.sha -ne $e.sha){throw "Preservation mismatch: $($e.path)"}
    $preserved+=@{path=$e.path;git_object=$e.sha;type=$e.type}
  }
}
$ev=Join-Path $bms 'evidence/reil_c4_0b1_fix2_20261014'
$steps=@('01_identity','02_red','03_green') | ForEach-Object {Get-Content -LiteralPath (Join-Path $ev ($_+'.meta.json')) -Raw | ConvertFrom-Json}
$total=($steps | Measure-Object elapsed_s -Sum).Sum
$green=Get-Content -LiteralPath (Join-Path $ev '03_green.stdout.log') -Raw
$red=Get-Content -LiteralPath (Join-Path $ev '02_red.stdout.log') -Raw
if($green -notmatch '71 passed' -or $red -notmatch '4 failed, 1 passed'){throw 'Test summary mismatch'}
$out=[ordered]@{
  kind='READ_ONLY_REVIEWER_EVIDENCE_AUDIT';reviewed_ref='5eeedb4beade319a040c2453e8b447673d425fd6'
  captured_files=$records.Count;captured_git_blobs_all_match=$true;production_commit_members=$committedCount
  request_attachment_sha256=$intakeHash;request_attachment_matches=$true;controls_match_prefixed_draft=$true
  preserved_git_objects=$preserved;producer_step_seconds=$total
  steps=@($steps | Select-Object step,rc,elapsed_s,timeout_s,head_start,head_end,timed_out)
  records=$records
  limitations=@('Producer logs inspected, not independently rerun.','Git object equality is fixed-commit preservation, not continuous machine observation.','95.4 seconds is precommit work snapshot, not final overall elapsed.')
  received_code_or_test_execution=0;data_opened=0;new_execution_approval=$false
}
$out | ConvertTo-Json -Depth 20
