$ErrorActionPreference='Stop'
$root='C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/work/microshort_s1_event_receiver_bound_integration_R3_20261108'
$sealPath=Join-Path $root 'PRESEAL.json'
$seal=Get-Content -LiteralPath $sealPath -Raw -ErrorAction Stop|ConvertFrom-Json
$config=Get-Content -LiteralPath (Join-Path $root 'CONFIG.json') -Raw -ErrorAction Stop|ConvertFrom-Json
foreach($row in @($seal.files)+@($seal.engine)){
 $f=Get-Item -LiteralPath $row.path -ErrorAction Stop
 $h=(Get-FileHash -LiteralPath $row.path -Algorithm SHA256 -ErrorAction Stop).Hash.ToLowerInvariant()
 if($f.Length -ne $row.bytes -or $h -ne $row.sha256){throw ('PRELAUNCH_IDENTITY:'+ $row.path)}
}
if(@(Get-ChildItem -LiteralPath (Join-Path $root 'results') -Force -ErrorAction Stop).Count -ne 0){throw 'RESULTS_NOT_EMPTY'}
if(@(Get-ChildItem -LiteralPath (Join-Path $root 'arena') -Force -ErrorAction Stop).Count -ne 0){throw 'ARENA_NOT_EMPTY'}
if(([Diagnostics.Stopwatch]::GetTimestamp()-5348059629301)/10000000 -ge 3600){throw 'WHOLE_BOUND_BEFORE_LAUNCH'}
$reserve=Join-Path $root 'EXECUTION_RESERVATION.json'
$rstream=[IO.File]::Open($reserve,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$bytes=[Text.Encoding]::UTF8.GetBytes('{"kind":"ONE_PARENT_SESSION_RESERVED","attempts":1,"retry":false}');$rstream.Write($bytes,0,$bytes.Length)}finally{$rstream.Dispose()}
$outPath=Join-Path $root 'results/session.stdout.txt'
$errPath=Join-Path $root 'results/session.stderr.txt'
$out=[IO.File]::Open($outPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::Read)
$err=[IO.File]::Open($errPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::Read)
$info=[Diagnostics.ProcessStartInfo]::new()
$info.FileName=$seal.engine.path
$info.Arguments='-I -B "'+(Join-Path $root 'validation/run.py')+'"'
$info.WorkingDirectory=Join-Path $root 'validation'
$info.UseShellExecute=$false
$info.CreateNoWindow=$true
$info.RedirectStandardOutput=$true
$info.RedirectStandardError=$true
$info.RedirectStandardInput=$true
$proc=[Diagnostics.Process]::new()
$proc.StartInfo=$info
$t=[Diagnostics.Stopwatch]::GetTimestamp()
$timedOut=$false
$rc=$null
$started=$false
try{
 if(-not $proc.Start()){throw 'PARENT_START_FALSE'}
 $started=$true
 $proc.StandardInput.Close()
 $copyOut=$proc.StandardOutput.BaseStream.CopyToAsync($out)
 $copyErr=$proc.StandardError.BaseStream.CopyToAsync($err)
 if(-not $proc.WaitForExit(180000)){$timedOut=$true;throw 'PARENT_180S_TIMEOUT_NO_UNAPPROVED_KILL_FALLBACK'}
 $copyOut.GetAwaiter().GetResult()
 $copyErr.GetAwaiter().GetResult()
 $rc=$proc.ExitCode
}finally{
 $out.Dispose();$err.Dispose()
}
$elapsed=([Diagnostics.Stopwatch]::GetTimestamp()-$t)/10000000
$return=[ordered]@{kind='R3_PARENT_PYTHON_SESSION_RETURN';started=$started;parent_sessions=1;argv=$config.parent_argv;cwd=$config.parent_cwd;pid=$proc.Id;process_rc=$rc;elapsed_seconds=$elapsed;limit_seconds=180;timed_out=$timedOut;stdout=[ordered]@{path=$outPath;bytes=(Get-Item -LiteralPath $outPath).Length;sha256=(Get-FileHash -LiteralPath $outPath -Algorithm SHA256).Hash.ToLowerInvariant()};stderr=[ordered]@{path=$errPath;bytes=(Get-Item -LiteralPath $errPath).Length;sha256=(Get-FileHash -LiteralPath $errPath -Algorithm SHA256).Hash.ToLowerInvariant()};native_ready=$false;boundary='After owned Python exit and raw output stream closure; before this return file write/readback and outer tool return.'}
$p=Join-Path $root 'PYTHON_SESSION_RETURN.json'
if(Test-Path -LiteralPath $p){throw 'SESSION_RETURN_EXISTS'}
[IO.File]::WriteAllText($p,($return|ConvertTo-Json -Depth 10)+[Environment]::NewLine,[Text.UTF8Encoding]::new($false))
[void](Get-Content -LiteralPath $p -Raw -ErrorAction Stop|ConvertFrom-Json)
$return|ConvertTo-Json -Depth 10
if($elapsed -gt 180){exit 2}
if($rc -ne 0){exit 1}
exit 0

