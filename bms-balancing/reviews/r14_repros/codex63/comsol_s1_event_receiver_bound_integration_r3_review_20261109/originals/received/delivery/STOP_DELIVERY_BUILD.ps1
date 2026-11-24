$ErrorActionPreference='Stop'
$r='C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/work/microshort_s1_event_receiver_bound_integration_R3_20261108'
$utf=New-Object System.Text.UTF8Encoding($false)
function NewJson([string]$p,$v){if(Test-Path -LiteralPath $p){throw "OUTPUT_EXISTS:$p"};[IO.File]::WriteAllText($p,($v|ConvertTo-Json -Depth 30),$utf);$null=Get-Content -LiteralPath $p -Raw|ConvertFrom-Json}
function Identity([string]$p){$f=Get-Item -LiteralPath $p;if($f.PSIsContainer -or ($f.Attributes -band [IO.FileAttributes]::ReparsePoint)){throw "BAD_FILE:$p"};[ordered]@{path=$f.FullName;bytes=$f.Length;sha256=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()}}
function Preserve($rows){$a=@();foreach($x in $rows){$v=Identity $x.path;if($v.bytes -ne $x.bytes -or $v.sha256 -cne $x.sha256){throw "IDENTITY_CHANGED:$($x.path)"};$a+=$v};return ,$a}
function Budget{$w=([Diagnostics.Stopwatch]::GetTimestamp()-5348059629301)/10000000;$d=([Diagnostics.Stopwatch]::GetTimestamp()-5359274339735)/10000000;$s=(Get-ChildItem -LiteralPath $r -File -Recurse|Measure-Object -Property Length -Sum).Sum;if($w -gt 3600 -or $d -gt 600 -or $s -gt 52428800){throw 'LIMIT_EXCEEDED'};@{whole_snapshot_seconds=$w;delivery_snapshot_seconds=$d;root_bytes=$s;whole_limit=3600;delivery_limit=600;bytes_limit=52428800}}
$before=Get-Content -LiteralPath (Join-Path $r 'SELECTED_SOURCES_BEFORE.json') -Raw|ConvertFrom-Json
$selected=Preserve $before.files
NewJson (Join-Path $r 'SELECTED_SOURCES_AFTER.json') @{kind='R3_STOP_CLOSEOUT_SELECTED_AFTER';count=$selected.Count;all_match=$true;files=$selected}
$seal=Get-Content -LiteralPath (Join-Path $r 'PRESEAL.json') -Raw|ConvertFrom-Json
$sealed=Preserve $seal.files
$engine=Preserve @($seal.engine)
$pre=Identity (Join-Path $r 'PRESEAL.json')
if($pre.bytes -ne 48046 -or $pre.sha256 -cne 'b1a0209011f718a0253a707efea4bb5f542775ad339b10fe37c142df2d24abae'){throw 'PRESEAL_CHANGED'}
NewJson (Join-Path $r 'SEALED_SOURCES_AFTER.json') @{kind='R3_STOP_CLOSEOUT_SEALED_AFTER';count=$sealed.Count;all_match=$true;files=$sealed;engine=$engine;preseal=$pre}
$i=Get-Content -LiteralPath (Join-Path $r 'INTAKE.json') -Raw|ConvertFrom-Json
$copies=@();foreach($c in $i.copies){$a=Identity $c.original.path;$b=Identity $c.copy.path;if($a.bytes -ne $c.original.bytes -or $a.sha256 -cne $c.original.sha256 -or $b.bytes -ne $a.bytes -or $b.sha256 -cne $a.sha256){throw 'COPY_CHANGED'};$copies+=@{original=$a;copy=$b}}
NewJson (Join-Path $r 'COPY_PRESERVATION_AFTER.json') @{count=$copies.Count;all_match=$true;copies=$copies}
$results=Get-Content -LiteralPath (Join-Path $r 'results/RESULTS.json') -Raw|ConvertFrom-Json
$session=Get-Content -LiteralPath (Join-Path $r 'PYTHON_SESSION_RETURN.json') -Raw|ConvertFrom-Json
$null=Preserve @($session.stdout,$session.stderr)
NewJson (Join-Path $r 'STOP_CLOSEOUT.json') @{kind='R3_RESULTS_PRESERVED_DELIVERY_PREPARATION_ERROR';test_result=$results;python_process_rc=$session.process_rc;python_seconds=$session.elapsed_seconds;target_sessions_after_error=0;retry=0;error_phase='JavaScript orchestration parser before report/normal packaging';full_procedure_compliance=$false;functional_results_not_revoked=$true;external_acceptance_pending=$true;snapshot=(Budget);native_ready=$false;overall='INCOMPLETE';boundary='Preservation-only closeout after first error, before archive creation.'}
$base=(Get-Item -LiteralPath $r).FullName.TrimEnd('\')+'\'
$files=@(Get-ChildItem -LiteralPath $r -Recurse -File)
$rows=@();$names=New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
foreach($f in ($files|Sort-Object FullName)){$a=Identity $f.FullName;$rel=$f.FullName.Substring($base.Length).Replace('\','/');if($rel.StartsWith('/') -or $rel.Contains('../') -or -not $names.Add($rel)){throw 'UNSAFE_PATH'};$rows+=@{path=$rel;bytes=$a.bytes;sha256=$a.sha256}}
$mp=Join-Path $r 'PACKAGE_MANIFEST.json'
NewJson $mp @{kind='R3_STOP_CLOSEOUT_DELIVERY_MANIFEST';payload_count=$rows.Count;files=$rows;manifest_excludes_itself=$true}
$zp=Join-Path $r 'delivery/COMSOL_S1_EVENT_RECEIVER_BOUND_INTEGRATION_R3_RESULT_AND_DELIVERY_STOP_20261108.zip'
Add-Type -AssemblyName System.IO.Compression
$fs=[IO.File]::Open($zp,[IO.FileMode]::CreateNew,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)
try{$z=[IO.Compression.ZipArchive]::new($fs,[IO.Compression.ZipArchiveMode]::Create,$true);try{foreach($row in (@($rows)+@(@{path='PACKAGE_MANIFEST.json'}))){$e=$z.CreateEntry($row.path,[IO.Compression.CompressionLevel]::Optimal);$s=$e.Open();try{$b=[IO.File]::ReadAllBytes((Join-Path $r $row.path));$s.Write($b,0,$b.Length)}finally{$s.Dispose()}}}finally{$z.Dispose()}}finally{$fs.Dispose()}
$m=Identity $mp;$all=@($rows)+@(@{path='PACKAGE_MANIFEST.json';bytes=$m.bytes;sha256=$m.sha256})
$fs=[IO.File]::OpenRead($zp)
try{$z=[IO.Compression.ZipArchive]::new($fs,[IO.Compression.ZipArchiveMode]::Read);try{if($z.Entries.Count -ne $all.Count){throw 'ZIP_COUNT'};foreach($row in $all){$es=@($z.Entries|Where-Object FullName -CEQ $row.path);if($es.Count -ne 1){throw 'ZIP_MEMBER'};$s=$es[0].Open();$ms=New-Object IO.MemoryStream;try{$s.CopyTo($ms);$b=$ms.ToArray();$h=[Security.Cryptography.SHA256]::Create();try{$hex=([BitConverter]::ToString($h.ComputeHash($b))).Replace('-','').ToLowerInvariant()}finally{$h.Dispose()};if($b.Length -ne $row.bytes -or $hex -cne $row.sha256){throw 'ZIP_HASH'}}finally{$ms.Dispose();$s.Dispose()}}}finally{$z.Dispose()}}finally{$fs.Dispose()}
$post=Preserve $before.files
NewJson (Join-Path $r 'delivery/SELECTED_SOURCES_POST_PACKAGE.json') @{kind='R3_SELECTED_POST_PACKAGE';count=$post.Count;all_match=$true;files=$post;scope='185 same unique selected inputs; not additive to overlapping seal/copy sets.'}
$rp=Join-Path $r 'delivery/DELIVERY_RECEIPT.json'
NewJson $rp @{kind='R3_RESULT_AND_DELIVERY_STOP_RECEIPT';recipient=$null;archive=(Identity $zp);manifest=$m;payload_count=$rows.Count;entries=$all.Count;verification='Exact member set, safe case-unique paths, decompressed sizes/SHA256 matched. CRC32 not independently recomputed.';selected_inputs_preserved=$post.Count;sealed_inputs_preserved=$sealed.Count;original_source_copies=12;functional_counts=$results.counts;normal_live_completions=1;parent_rc=0;child_rc=0;first_error_preserved=$true;full_procedure_compliance=$false;normal_packaging_attempt_executed=$false;failed_call_retry=0;closeout_scope='Preserve already completed results and orchestration error only';native_ready=$false;approved=$false;usable=$false;contract_adopted=$false;overall='INCOMPLETE';normal_gate='INCOMPLETE';snapshot=(Budget);boundary='After archive readback and selected input rehash; before receipt write/readback and tool return.'}
@{kind='R3_STOP_CLOSEOUT_PACKAGE_RETURN';archive=(Identity $zp);receipt=(Identity $rp);payload_count=$rows.Count;entries=$all.Count;pass=12;fail=0;not_run=0;first_error_preserved=$true;native_ready=$false;snapshot=(Budget);boundary='After receipt write/readback; before actual tool return and later transcription.'}|ConvertTo-Json -Depth 12

