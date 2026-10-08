$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$source=Split-Path -Parent $root
$origin=Get-Content -LiteralPath (Join-Path $root 'ORIGIN.json') -Raw|ConvertFrom-Json
function Hash($bytes){$h=[Security.Cryptography.SHA256]::Create();try{[BitConverter]::ToString($h.ComputeHash([byte[]]$bytes)).Replace('-','').ToLowerInvariant()}finally{$h.Dispose()}}
function Id($path){$f=Get-Item -LiteralPath $path;[ordered]@{path=$f.FullName;bytes=$f.Length;sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}}
function NewJson($name,$value){$raw=[Text.UTF8Encoding]::new($false).GetBytes(($value|ConvertTo-Json -Depth 80));$s=[IO.File]::Open((Join-Path $root $name),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write);try{$s.Write($raw,0,$raw.Length)}finally{$s.Dispose()}}
$manifestPath=Join-Path $source 'CODE_MANIFEST.json'
$manifest=Get-Content -LiteralPath $manifestPath -Raw|ConvertFrom-Json
if((Id $manifestPath).sha256 -ne '4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da'){throw 'MANIFEST_IDENTITY'}
$pinned=@(Id $manifestPath)
foreach($f in $manifest.files){$now=Id (Join-Path $source $f.path);if($now.bytes -ne $f.bytes -or $now.sha256 -ne $f.sha256){throw 'SOURCE_IDENTITY'};$pinned+=$now}
$plan=Get-Content -LiteralPath (Join-Path $root 'VALIDATION_PLAN_CORRECTED.json') -Raw|ConvertFrom-Json
if($plan.cases.Count -ne 130 -or @($plan.cases.id|Sort-Object -Unique).Count -ne 130 -or @($plan.cases.input_id|Sort-Object -Unique).Count -ne 130){throw 'CASE_SET'}
if(@($plan.cases|Where-Object {$_.engine -eq 'Python'}).Count -ne 99 -or @($plan.cases|Where-Object {$_.engine -eq 'Windows PowerShell5.1'}).Count -ne 31){throw 'ENGINE_CASE_SET'}
$extracts=@()
foreach($span in $plan.extraction_spans){
  $path=Join-Path $source $span.source
  $raw=[IO.File]::ReadAllBytes($path)
  $text=[Text.UTF8Encoding]::new($false,$true).GetString($raw)
  $lf=$text.Replace("`r`n","`n")
  $lines=$lf.Split("`n")
  $start=[int]$span.start_line;$end=[int]$span.end_line
  if($start -lt 1 -or $end -lt $start -or $end -gt $lines.Length){throw ('SPAN_RANGE:'+ $span.name)}
  $chosen=$lines[($start-1)..($end-1)] -join "`n"
  $bytes=[Text.UTF8Encoding]::new($false).GetBytes($chosen)
  $digest=Hash $bytes
  if($bytes.Length -eq 0 -or $digest -ne $span.sha256 -or -not $chosen.Contains([string]$span.name)){throw ('SPAN_IDENTITY:'+ $span.name)}
  $prefix=if($start -eq 1){''}else{($lines[0..($start-2)] -join "`n")+"`n"}
  $offset=[Text.UTF8Encoding]::new($false).GetByteCount($prefix)
  $extracts += [ordered]@{source=$span.source;name=$span.name;start_line=$start;end_line=$end;normalized_begin_byte=$offset;normalized_end_byte_exclusive=$offset+$bytes.Length;bytes=$bytes.Length;sha256=$digest;normalization='UTF8 CRLF to LF; final LF excluded; byte offsets refer to normalized source';raw_source_sha256=Hash $raw}
}
if($extracts.Count -ne 43){throw 'EXTRACTION_REQUIRED_SET'}
NewJson 'EXTRACTION_SEAL.json' ([ordered]@{count=$extracts.Count;all_match=$true;spans=$extracts})
$engines=@()
foreach($e in $plan.engines){$now=Id $e.path;if($now.bytes -ne $e.bytes -or $now.sha256 -ne $e.sha256){throw 'ENGINE_IDENTITY'};$engines+=$now;$pinned+=$now}
# Parse own PS code as text only; never dot-source or invoke candidate functions here.
foreach($file in @((Join-Path $root 'harness/ps_harness.ps1'),(Join-Path $root 'tools/run_engine_once.ps1'))){$tokens=$null;$errors=$null;$null=[Management.Automation.Language.Parser]::ParseFile($file,[ref]$tokens,[ref]$errors);if($errors.Count){throw ('OWN_PS_STATIC_SYNTAX:'+($errors|Out-String))}}
$p0=[IO.File]::ReadAllText((Join-Path $source 'candidate/variants/P0.java.inactive.txt'))
$p0checks=[ordered]@{id='STATIC_N4_01';mode='text_only_not_functional';tout_tsteps=$p0.Contains('set("tout","tsteps")');accepted_stored_summary=($p0 -match 'accepted tsteps storage');requested_tlist_summary_absent=($p0 -notmatch 'storage.*requested tlist');java_compile_or_jvm=0;interpretation='Existing accepted tsteps storage summary and tout=tsteps literal; no new compatibility claim'}
if(-not $p0checks.tout_tsteps -or -not $p0checks.accepted_stored_summary){throw 'P0_STATIC_REQUIRED_TEXT'}
NewJson 'STATIC_N4_01.json' $p0checks
$readiness=Get-Content -LiteralPath (Join-Path $root 'PRESEAL_READINESS.json') -Raw|ConvertFrom-Json
if($readiness.status -ne 'READY' -or $readiness.registered_inputs -ne 130 -or $readiness.unresolved.Count -ne 0){throw 'MANUAL_STATIC_READINESS_INCOMPLETE'}
$commands=@([ordered]@{engine='python';argv=@($engines[0].path,'-I','-B',(Join-Path $root 'harness/python_harness.py'));cwd=$root;limit_s=420},[ordered]@{engine='powershell';argv=@($engines[1].path,'-NoLogo','-NoProfile','-NonInteractive','-File',(Join-Path $root 'harness/ps_harness.ps1'));cwd=$root;limit_s=300})
NewJson 'COMMANDS.json' $commands
$files=@(Get-ChildItem -LiteralPath $root -Recurse -File|Where-Object {$_.FullName -notmatch '[\\/]results[\\/]' -and $_.FullName -notmatch '[\\/]__pycache__[\\/]'}|Sort-Object FullName)
foreach($f in $files){$pinned+=Id $f.FullName}
$fixtureBytes=(Get-ChildItem -LiteralPath $root -Recurse -File|Measure-Object Length -Sum).Sum
$elapsed=([Diagnostics.Stopwatch]::GetTimestamp()-[long]$origin.monotonic_ticks)/[double]$origin.frequency
if($elapsed -gt 720 -or $fixtureBytes -gt 1073741824){throw 'PRESEAL_BUDGET_OR_STORAGE'}
$seal=[ordered]@{schema='S1O_R1_FIRST_ENGINE_SEAL_V1';status='READY_FOR_ONE_OFFLINE_VALIDATION';cases=130;counts=@{python=99;powershell=31};preseal_elapsed_s=$elapsed;preseal_limit_s=720;origin=$origin;engines=$engines;commands=$commands;files=$pinned;source_manifest_sha256='4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da';native_ready=$false;fixture_bytes=$fixtureBytes;second_seal_required_before_powershell=$true}
NewJson 'FIRST_SEAL.json' $seal
[ordered]@{status=$seal.status;first_seal=Id (Join-Path $root 'FIRST_SEAL.json');cases=130;preseal_elapsed_s=$elapsed;fixture_bytes=$fixtureBytes;candidate_function_calls=0}|ConvertTo-Json -Depth 6 -Compress
