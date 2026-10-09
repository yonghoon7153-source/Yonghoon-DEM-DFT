param([Parameter(Mandatory=$true)][ValidateSet('python','powershell')][string]$Engine)
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$origin=Get-Content -LiteralPath (Join-Path $root 'ORIGIN.json') -Raw|ConvertFrom-Json
function NowElapsed {([Diagnostics.Stopwatch]::GetTimestamp()-[long]$origin.monotonic_ticks)/[double]$origin.frequency}
function Identity($path){$f=Get-Item -LiteralPath $path;[ordered]@{path=$f.FullName;bytes=$f.Length;sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}}
function WriteNew($name,$obj){$bytes=[Text.UTF8Encoding]::new($false).GetBytes(($obj|ConvertTo-Json -Depth 40));$s=[IO.File]::Open((Join-Path $root $name),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write);try{$s.Write($bytes,0,$bytes.Length)}finally{$s.Dispose()}}
if(Test-Path -LiteralPath (Join-Path $root 'FIRST_FAILURE.json')){throw 'FIRST_FAILURE_ALREADY_RECORDED'}
$sealPath=Join-Path $root 'FIRST_SEAL.json'
$seal=Get-Content -LiteralPath $sealPath -Raw|ConvertFrom-Json
if($seal.status -ne 'READY_FOR_ONE_OFFLINE_VALIDATION' -or $seal.cases -ne 7 -or $seal.preseal_elapsed_s -gt 600){throw 'PRESEAL_NOT_READY'}
foreach($f in $seal.files){$now=Identity $f.path;if($now.bytes -ne $f.bytes -or $now.sha256 -ne $f.sha256){throw ('SEAL_MISMATCH:'+ $f.path)}}
$command=@($seal.commands|Where-Object {$_.engine -eq $Engine})
if($command.Count -ne 1){throw 'ENGINE_COMMAND_NOT_UNIQUE'}
$command=$command[0]
if((NowElapsed) -ge (1200-60)){throw 'INSUFFICIENT_CLOSEOUT_RESERVE'}
if($Engine -eq 'powershell'){
  $prior=Get-Content -LiteralPath (Join-Path $root 'results/PYTHON_SESSION.json') -Raw|ConvertFrom-Json
  $priorResult=Get-Content -LiteralPath (Join-Path $root 'results/PYTHON_RESULTS.json') -Raw|ConvertFrom-Json
  if($prior.rc -ne 0 -or $prior.timed_out -or $priorResult.status -ne 'PASS' -or $priorResult.count -ne 4){throw 'PYTHON_NOT_PASS'}
  if(-not(Test-Path -LiteralPath (Join-Path $root 'results/PS_PRODUCER_SEAL.json'))){throw 'SECOND_SEAL_MISSING'}
}
$label=$Engine.ToUpperInvariant()
$attemptName='results/'+$label+'_ATTEMPT.json'
$stdoutPath=Join-Path $root ('results/'+$label+'_STDOUT.txt')
$stderrPath=Join-Path $root ('results/'+$label+'_STDERR.txt')
$startedUtc=[DateTime]::UtcNow.ToString('o')
$startTick=[Diagnostics.Stopwatch]::GetTimestamp()
WriteNew $attemptName ([ordered]@{engine=$Engine;utc=$startedUtc;tick=$startTick;argv=$command.argv;cwd=$command.cwd;limit_s=$command.limit_s;first_seal=Identity $sealPath;retry=0})
$process=[Diagnostics.Process]::new()
$process.StartInfo=[Diagnostics.ProcessStartInfo]::new()
$process.StartInfo.FileName=[string]$command.argv[0]
$process.StartInfo.WorkingDirectory=[string]$command.cwd
$process.StartInfo.UseShellExecute=$false
$process.StartInfo.CreateNoWindow=$true
$process.StartInfo.RedirectStandardOutput=$true
$process.StartInfo.RedirectStandardError=$true
foreach($arg in @($command.argv|Select-Object -Skip 1)){$process.StartInfo.ArgumentList.Add([string]$arg)}
$outStream=[IO.File]::Open($stdoutPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
$errStream=[IO.File]::Open($stderrPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
$rc=$null;$timeout=$false;$startError=$null;$cleanupError=$null;$pidOwned=$null
$overallLimit=[double]$origin.total_limit_s
$closeoutReserve=[double]$origin.phase_limits_s.incomplete_closeout
$engineOverallDeadline=$overallLimit-$closeoutReserve
$waitBudgetSeconds=$null
try{
  # Recheck after attempt/log creation. Never start a harness without its reserve.
  $already=([Diagnostics.Stopwatch]::GetTimestamp()-$startTick)/[double]$origin.frequency
  $phaseRemaining=[double]$command.limit_s-$already
  $overallRemaining=$engineOverallDeadline-(NowElapsed)
  if($phaseRemaining -le 0 -or $overallRemaining -le 0){$timeout=$true;throw 'ENGINE_START_BUDGET_EXHAUSTED'}
  if(-not $process.Start()){throw 'ENGINE_START_RETURNED_FALSE'}
  $pidOwned=$process.Id
  $outTask=$process.StandardOutput.BaseStream.CopyToAsync($outStream)
  $errTask=$process.StandardError.BaseStream.CopyToAsync($errStream)
  $already=([Diagnostics.Stopwatch]::GetTimestamp()-$startTick)/[double]$origin.frequency
  $phaseRemaining=[double]$command.limit_s-$already
  $overallRemaining=$engineOverallDeadline-(NowElapsed)
  $waitBudgetSeconds=[Math]::Min($phaseRemaining,$overallRemaining)
  $remaining=[int][Math]::Max(0,[Math]::Floor(1000*$waitBudgetSeconds))
  if($remaining -le 0 -or -not $process.WaitForExit($remaining)){
    $timeout=$true
    # This is the exact harness Process object started above; never search/kill other PIDs.
    $process.Kill()
    if(-not $process.WaitForExit(5000)){throw 'OWNED_HARNESS_EXIT_UNCONFIRMED'}
  }
  $rc=$process.ExitCode
  if(-not [Threading.Tasks.Task]::WaitAll([Threading.Tasks.Task[]]@($outTask,$errTask),5000)){throw 'ENGINE_OUTPUT_COLLECTION_INCOMPLETE'}
}catch{$startError=$_.Exception.ToString()}
finally{
  try{$outStream.Dispose();$errStream.Dispose()}catch{$cleanupError=$_.Exception.ToString()}
  $process.Dispose()
}
$elapsed=([Diagnostics.Stopwatch]::GetTimestamp()-$startTick)/[double]$origin.frequency
$overallSnapshot=NowElapsed
$pass=($null -ne $rc -and $rc -eq 0 -and -not $timeout -and $null -eq $startError -and $null -eq $cleanupError -and $elapsed -le [double]$command.limit_s -and $overallSnapshot -le $engineOverallDeadline -and $overallSnapshot -le $overallLimit)
$record=[ordered]@{engine=$Engine;utc_start=$startedUtc;utc_end=[DateTime]::UtcNow.ToString('o');pid_owned=$pidOwned;argv=$command.argv;cwd=$command.cwd;rc=$rc;timed_out=$timeout;elapsed_s=$elapsed;limit_s=$command.limit_s;overall_snapshot_s=$overallSnapshot;overall_limit_s=$overallLimit;engine_overall_deadline_s=$engineOverallDeadline;closeout_reserve_s=$closeoutReserve;effective_wait_budget_s=$waitBudgetSeconds;within_limits=$pass;start_or_collection_error=$startError;cleanup_error=$cleanupError;stdout=Identity $stdoutPath;stderr=Identity $stderrPath;status=if($pass){'ENGINE_RETURNED_RC0'}else{'FIRST_UNEXPECTED_ENGINE_FAILURE'};raw_process_exit_observed=($null -ne $rc);observation_phase='PRE_SESSION_RECORD_WRITE'}
WriteNew ('results/'+$label+'_SESSION.json') $record
if(-not $pass){WriteNew 'FIRST_FAILURE.json' $record}
# The final observation takes precedence if writing the immutable session record
# consumed the remaining phase/overall budget. Do not rewrite a previous record.
$finalElapsed=([Diagnostics.Stopwatch]::GetTimestamp()-$startTick)/[double]$origin.frequency
$finalOverall=NowElapsed
$finalPass=($pass -and $finalElapsed -le [double]$command.limit_s -and $finalOverall -le $engineOverallDeadline -and $finalOverall -le $overallLimit)
$final=[ordered]@{kind='HARNESS_ENGINE_FINAL_RETURN';engine=$Engine;observation_phase='POST_SESSION_RECORD_WRITE';rc=$rc;within_limits=$finalPass;elapsed_s=$finalElapsed;limit_s=$command.limit_s;overall_snapshot_s=$finalOverall;overall_limit_s=$overallLimit;engine_overall_deadline_s=$engineOverallDeadline;session=Identity (Join-Path $root ('results/'+$label+'_SESSION.json'));prior_session_within_limits=$pass;reason=if($pass -and -not $finalPass){'POST_RECORD_ENGINE_OR_OVERALL_BUDGET_EXCEEDED'}elseif(-not $pass){'EARLIER_ENGINE_FAILURE_PRESERVED'}else{$null}}
if(-not $finalPass -and -not(Test-Path -LiteralPath (Join-Path $root 'FIRST_FAILURE.json'))){WriteNew 'FIRST_FAILURE.json' $final}
$final|ConvertTo-Json -Depth 20 -Compress
if(-not $finalPass){exit 1}
