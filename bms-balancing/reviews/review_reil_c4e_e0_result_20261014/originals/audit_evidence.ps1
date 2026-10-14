$ErrorActionPreference='Stop'
$reviewRoot=$PSScriptRoot
$sourceRoot=Join-Path $reviewRoot 'source'
$evidenceRoot=Join-Path $sourceRoot 'evidence/reil_c4e0_20261014'
function HashBytes([byte[]]$raw,[string]$kind='SHA256') {
 $h=[Security.Cryptography.HashAlgorithm]::Create($kind)
 try { ([BitConverter]::ToString($h.ComputeHash($raw))).Replace('-','').ToLowerInvariant() } finally {$h.Dispose()}
}
function NewBytes([string]$dest,[byte[]]$raw) {
 $full=[IO.Path]::GetFullPath($dest)
 if(-not $full.StartsWith($reviewRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Outside review folder'}
 $null=[IO.Directory]::CreateDirectory((Split-Path $full -Parent))
 $s=[IO.File]::Open($full,[IO.FileMode]::CreateNew)
 try {$s.Write($raw,0,$raw.Length)} finally {$s.Dispose()}
}
function ReadJson([string]$p){Get-Content -LiteralPath $p -Raw|ConvertFrom-Json}
$history=@()
foreach($r in (ReadJson (Join-Path $reviewRoot 'HISTORICAL_PAYLOADS.json'))) {
 $raw=[Convert]::FromBase64String($r.content)
 $hdr=[Text.Encoding]::ASCII.GetBytes('blob '+$raw.Length+[char]0)
 if((HashBytes ([byte[]]($hdr+$raw)) 'SHA1') -ne $r.git_blob){throw 'Historical blob mismatch'}
 NewBytes (Join-Path $reviewRoot $r.capture) $raw
 $history+=@{capture=$r.capture;repo_path=$r.repo_path;ref=$r.ref;bytes=$raw.Length;sha256=(HashBytes $raw);git_blob=$r.git_blob}
}
$sealResults=@()
foreach($line in (Get-Content -LiteralPath (Join-Path $evidenceRoot '05_source_sha256_end.txt'))) {
 if($line -notmatch '^([0-9a-f]{64})  (.+)$'){throw 'Seal parse'}
 $sha=$Matches[1];$rel=$Matches[2];$p=Join-Path $sourceRoot $rel
 $actual=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()
 if($actual -ne $sha){throw ('Current source seal mismatch '+$rel)}
 $sealResults+=@{path=$rel;sha256=$sha;match=$true}
}
$greenSeal=[IO.File]::ReadAllBytes((Join-Path $evidenceRoot '03_green.source_sha256.txt'))
$endSeal=[IO.File]::ReadAllBytes((Join-Path $evidenceRoot '05_source_sha256_end.txt'))
if((HashBytes $greenSeal) -ne (HashBytes $endSeal)){throw 'Green/end seals differ'}
$steps=@();$sum=0.0
foreach($name in @('01_identity','02_red','03_green','04_plan_e')) {
 $m=ReadJson (Join-Path $evidenceRoot ($name+'.meta.json'))
 $sum+=$m.elapsed_s
 $steps+=@{step=$name;elapsed_s=$m.elapsed_s;timeout_s=$m.timeout_s;rc=$m.rc;timed_out=$m.timed_out;head_start=$m.head_start;head_end=$m.head_end;stderr_bytes=(Get-Item -LiteralPath (Join-Path $evidenceRoot ($name+'.stderr.log'))).Length}
 if($m.timed_out -or $m.elapsed_s -gt $m.timeout_s){throw 'Step timeout'}
 if($name -eq '02_red'){if($m.rc -ne 1){throw 'RED rc'}}elseif($m.rc -ne 0){throw 'Step rc'}
}
$red=Get-Content -LiteralPath (Join-Path $evidenceRoot '02_red.stdout.log') -Raw
$green=Get-Content -LiteralPath (Join-Path $evidenceRoot '03_green.stdout.log') -Raw
$redNames=@([regex]::Matches($red,'(?m)^FAILED tests/test_reil_c4e.py::(test_[^\s]+)')|ForEach-Object {$_.Groups[1].Value})
$tests=Get-Content -LiteralPath (Join-Path $sourceRoot 'tests/test_reil_c4e.py') -Raw
$testNames=@([regex]::Matches($tests,'(?m)^def (test_[^(]+)\(')|ForEach-Object {$_.Groups[1].Value})
if($testNames.Count -ne 21 -or $redNames.Count -ne 21 -or @(Compare-Object $testNames $redNames).Count){throw 'RED test set'}
$notImplemented=[regex]::Matches($red,'(?m)^E\s+NotImplementedError:').Count
$typeError=[regex]::Matches($red,'(?m)^E\s+TypeError:').Count
if($notImplemented -ne 19 -or $typeError -ne 2 -or $green -notmatch '180 passed in 43\.03s'){throw 'Result text'}
$planPath=Join-Path $evidenceRoot '04_plan_e_out/PLAN_E.json'
$plan=ReadJson $planPath
$planSha=(Get-FileHash -LiteralPath $planPath).Hash.ToLowerInvariant()
if($planSha -ne '1538407567bf1950ff744efe80e39cf3423c0a19f213d9e18db0dd1d91f8fa3a'){throw 'Plan hash'}
$nullModules=@($plan.identity_table.PSObject.Properties|Where-Object {$_.Name.StartsWith('scripts/') -and $null -eq $_.Value.expected}|ForEach-Object {$_.Name})
if($nullModules.Count -ne 5){throw 'Expected module count'}
if(($history|Where-Object capture -eq 'historical/RED_test_reil_c4e.py').sha256 -ne (Get-FileHash -LiteralPath (Join-Path $sourceRoot 'tests/test_reil_c4e.py')).Hash.ToLowerInvariant()){throw 'Test changed after RED'}
$currentRunner=Get-Content -LiteralPath (Join-Path $evidenceRoot '00_step_runner.py') -Raw
$priorRunner=Get-Content -LiteralPath (Join-Path $reviewRoot 'historical/PREV_STEP_RUNNER.py') -Raw
$runnerDiff=@(Compare-Object ($priorRunner -split "`n") ($currentRunner -split "`n"))
$result=[ordered]@{kind='E0_RESULT_STATIC_EVIDENCE_AUDIT';reviewed_head='5cb6ab95c8c461cf940dcf94b90c30e8a3e3659c';historical=$history;steps=$steps;step_sum_s=[Math]::Round($sum,3);step_sum_limit_s=1560;red=@{tests=21;NotImplementedError=$notImplemented;TypeError=$typeError;ids=$testNames};green=@{reported_passed=180;pytest_s=43.03;existing=159;new=21};source_seals=$sealResults;source_seal_count=$sealResults.Count;green_end_seal_raw_equal=$true;red_green_test_bytes_equal=$true;plan=@{bytes=(Get-Item -LiteralPath $planPath).Length;sha256=$planSha;calls=$plan.plan.Count;null_expected_modules=$nullModules;identity_ok=$plan.identity.ok};runner_line_differences=$runnerDiff;review_execution=@{received_code=0;tests=0;raw_data_fetch_open=0;optimizer=0;COMSOL=0};time_scope='2364.4 seconds is submitted pre-commit/push/docs snapshot, not final delivery elapsed';approval_scope='User approval quotation recorded at pre-execution repository commit; not independent original chat capture'}
NewBytes (Join-Path $reviewRoot 'STATIC_AUDIT.json') ([Text.UTF8Encoding]::new($false).GetBytes(($result|ConvertTo-Json -Depth 30)+"`n"))
[ordered]@{source_seals=$sealResults.Count;red_expected=21;green=180;sum_s=$result.step_sum_s;null_expected_modules=$nullModules;history=$history.Count;received_code_execution=0}|ConvertTo-Json -Depth 5
