$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$source=Join-Path (Split-Path $root -Parent) 'guard1198_limited_validation_R1_20260928/PARENT_COMMAND.ps1'
if ($PSVersionTable.PSEdition -cne 'Desktop' -or $PSVersionTable.PSVersion.Major -ne 5) {throw 'ENGINE_51_REQUIRED'}
$seal=ConvertFrom-Json ([IO.File]::ReadAllText((Join-Path $root 'PRE_TEST_SEAL.json')))
foreach($pin in $seal.files){if((Get-FileHash -LiteralPath $pin.path).Hash.ToLowerInvariant() -cne $pin.sha256 -or (Get-Item -LiteralPath $pin.path).Length -ne $pin.bytes){throw 'SEAL_CHANGED'}}
$tokens=$null;$errors=$null;$ast=[Management.Automation.Language.Parser]::ParseFile($source,[ref]$tokens,[ref]$errors)
if($errors.Count){throw 'SOURCE_PARSE_ERROR'}
$extracted=@()
foreach($name in @('BSave','BInvoke','GDecision')){
 $f=@($ast.FindAll({param($node) $node -is [Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -ceq $name},$true))
 if($f.Count -ne 1){throw 'EXTRACT_SET'}
 $text=$f[0].Extent.Text;$extracted+=@{name=$name;source=$text;start=$f[0].Extent.StartLineNumber;end=$f[0].Extent.EndLineNumber}
 . ([scriptblock]::Create($text))
}
$bEvidence=Join-Path $root 'ps_fixture';if(Test-Path -LiteralPath $bEvidence){throw 'EXISTING_NO_RETRY'}
[void][IO.Directory]::CreateDirectory($bEvidence)
$bPython='C:/Users/BML/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$bClock=[Diagnostics.Stopwatch]::StartNew();$results=[Collections.Generic.List[object]]::new()
function Check([bool]$Value,[string]$Reason){if(-not $Value){throw $Reason}}
function CopyObject($x){ConvertFrom-Json (ConvertTo-Json -InputObject $x -Depth 40 -Compress)}
function GoodReturn {return @{returned=$true;invocation_succeeded=$true;native_rc=[int]0;new_error=$false;exception=$null;elapsed_seconds=[double]1.0}}
function Case([string]$Group,[string]$Name,[scriptblock]$Body){
 if($bClock.Elapsed.TotalSeconds -gt 60){throw 'SUITE_BUDGET'}
 try{& $Body;$results.Add(@{group=$Group;case=$Name;status='PASS'})}catch{$results.Add(@{group=$Group;case=$Name;status='FAIL';error=$_.ToString()});throw}
}
$positive=ConvertFrom-Json ([IO.File]::ReadAllText((Join-Path $root 'records/positive_result.json')))
$expected=@{run_id=$positive.run_id;manifest_sha256=$positive.code_manifest_sha256};$good=GoodReturn
try{
 Case 'PS01' 'exit0' {BInvoke 'zero' @('-I','-S','-B','-c','raise SystemExit(0)') 'zero.json';Check ($bLastReturn.native_rc -ceq 0 -and $bLastReturn.returned) 'ZERO'}
 $old=$bLastReturn;$h0=(Get-FileHash (Join-Path $bEvidence 'zero.json')).Hash
 Case 'PS01' 'exit7' {BInvoke 'seven' @('-I','-S','-B','-c','raise SystemExit(7)') 'seven.json';Check ($bLastReturn.native_rc -ceq 7 -and -not $bLastReturn.invocation_succeeded) 'SEVEN'}
 Case 'PS01' 'missing_clears_stale' {$script:bPython=Join-Path $bEvidence 'MISSING.exe';BInvoke 'missing' @() 'missing.json';Check ($null -eq $bLastReturn.native_rc -and -not $bLastReturn.returned -and $null -ne $bLastReturn.exception) 'MISSING'}
 Case 'PS02' 'earlier_record_unchanged' {Check ($old.native_rc -ceq 0 -and (Get-FileHash (Join-Path $bEvidence 'zero.json')).Hash -ceq $h0) 'EARLIER_CHANGED'}
 Case 'PS03' 'actual_producer_positive' {Check ((GDecision $good $good $positive $expected 10) -ceq 'AWAITING_LIMITED_EXTERNAL_ACCEPTANCE') 'POSITIVE_REJECTED'}
 foreach($key in @('trigger','sampled_comparison','preservation','process_cleanup','policy_preservation')){
  Case 'PS03' ('missing_'+$key) {$x=CopyObject $positive;$x.PSObject.Properties.Remove($key);Check ((GDecision $good $good $x $expected 10) -ceq 'INCOMPLETE') 'MISSING_AXIS_ACCEPTED'}
  Case 'PS03' ('incomplete_'+$key) {$x=CopyObject $positive;$x.$key='INCOMPLETE';Check ((GDecision $good $good $x $expected 10) -ceq 'INCOMPLETE') 'INCOMPLETE_AXIS_ACCEPTED'}
 }
 foreach($kind in @('rc1','null','newError')){
  Case 'PS04' $kind {$n=GoodReturn;if($kind -ceq 'rc1'){$n.native_rc=1};if($kind -ceq 'null'){$n.native_rc=$null};if($kind -ceq 'newError'){$n.new_error=$true};Check ((GDecision $n $good $positive $expected 10) -ceq 'INCOMPLETE') 'NATIVE_FAILURE_LOST'}
 }
 Case 'PS05' 'summary_only' {$x=CopyObject $positive;foreach($k in @('pair','native_stop','numeric','tables_manifest')){$x.PSObject.Properties.Remove($k)};Check ((GDecision $good $good $x $expected 10) -ceq 'INCOMPLETE') 'SUMMARY_ACCEPTED'}
 foreach($key in @('pair','native_stop','numeric','tables_manifest')){
  Case 'PS05' ('missing_'+$key) {$x=CopyObject $positive;$x.PSObject.Properties.Remove($key);Check ((GDecision $good $good $x $expected 10) -ceq 'INCOMPLETE') 'MISSING_EVIDENCE_ACCEPTED'}
  Case 'PS05' ('empty_'+$key) {$x=CopyObject $positive;$x.$key=[pscustomobject]@{};Check ((GDecision $good $good $x $expected 10) -ceq 'INCOMPLETE') 'EMPTY_EVIDENCE_ACCEPTED'}
 }
 Case 'PS05' 'coverage_empty' {$x=CopyObject $positive;$x.numeric.coverage=[pscustomobject]@{};Check ((GDecision $good $good $x $expected 10) -ceq 'INCOMPLETE') 'COVERAGE_ACCEPTED'}
 Case 'PS05' 'identity_wrong' {$x=CopyObject $positive;$x.code_manifest_sha256='wrong';Check ((GDecision $good $good $x $expected 10) -ceq 'INCOMPLETE') 'IDENTITY_ACCEPTED'}
 Case 'PS05' 'analysis_rc1' {$a=GoodReturn;$a.native_rc=1;Check ((GDecision $good $a $positive $expected 10) -ceq 'INCOMPLETE') 'ANALYSIS_FAILURE_LOST'}
 foreach($bad in @([double]::NaN,[double]::PositiveInfinity,[double]-1,[double]601)){
  Case 'PS06' ('analysis_time_'+$bad) {$a=GoodReturn;$a.elapsed_seconds=$bad;Check ((GDecision $good $a $positive $expected 10) -ceq 'INCOMPLETE') 'TIME_ACCEPTED'}
 }
 Case 'PS06' 'overall3001' {Check ((GDecision $good $good $positive $expected 3001) -ceq 'INCOMPLETE') 'OVERALL_ACCEPTED'}
}finally{
 [IO.File]::WriteAllText((Join-Path $root 'records/PS_EXTRACTED.json'),(ConvertTo-Json -InputObject $extracted -Depth 40))
 [IO.File]::WriteAllText((Join-Path $root 'records/PS_RESULT.json'),(ConvertTo-Json -InputObject @{results=@($results.ToArray());elapsed_seconds=$bClock.Elapsed.TotalSeconds} -Depth 40))
}
[Console]::WriteLine(('PS_PASS subcases='+$results.Count))
