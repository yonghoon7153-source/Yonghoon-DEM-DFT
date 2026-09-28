# INACTIVE CANDIDATE. Not executed/tested. Separate validation release + native approval required.
param([Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ManifestSha)
$ErrorActionPreference='Stop'
$bClock=[Diagnostics.Stopwatch]::StartNew()
$bRoot='C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/guard1198_offline_preparation_20260928'
$bEvidence=Join-Path $bRoot 'future_parent_001'
$bPython='C:/Users/BML/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$bOwned=$false
$bTranscript=$false
$bLastReturn=$null
$bErrors=@()
$bRunReturn=$null
$bAnalysisReturn=$null
$bDeliveryStart=$null
function BHash([string]$Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256 -ErrorAction Stop).Hash.ToLowerInvariant() }
function BRef([string]$Path) { @{path=$Path;bytes=(Get-Item -LiteralPath $Path -ErrorAction Stop).Length;sha256=(BHash $Path)} }
function BRead([string]$Path) { ConvertFrom-Json -InputObject ([IO.File]::ReadAllText($Path)) -ErrorAction Stop }
function BSave([string]$Name,$Value) {
    $p=Join-Path $bEvidence $Name
    $raw=[Text.UTF8Encoding]::new($false).GetBytes((ConvertTo-Json -InputObject $Value -Depth 40 -Compress)+"`n")
    $s=[IO.File]::Open($p,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::Read)
    try { $s.Write($raw,0,$raw.Length); $s.Flush($true) } finally { $s.Dispose() }
    if ([Convert]::ToBase64String([IO.File]::ReadAllBytes($p)) -cne [Convert]::ToBase64String($raw)) { throw 'EVIDENCE_READBACK' }
}

function BInvoke([string]$Phase,[string[]]$Argv,[string]$Record) {
    # Foreground call, without pipe/redirection/background process or input injection.
    $start=$bClock.Elapsed.TotalSeconds
    $old=$Error[0]; $returned=$false; $ok=$false; $rc=$null; $exception=$null
    $global:LASTEXITCODE=$null
    try {
        & $bPython @Argv
        $ok=$?
        $rc=$global:LASTEXITCODE
        $returned=$true
    } catch { $exception=$_.ToString() }
    $end=$bClock.Elapsed.TotalSeconds
    $newError= -not [Object]::ReferenceEquals($old,$Error[0])
    $result=@{phase=$Phase;source='USER_VISIBLE_POWERSHELL_PARENT';returned=$returned;invocation_succeeded=$ok;native_rc=$rc;exception=$exception;new_error=$newError;top_error=$(if ($newError) {$Error[0].ToString()} else {$null});start_seconds=$start;end_seconds=$end;elapsed_seconds=($end-$start);executable=$bPython;argv=$Argv;cwd=(Get-Location).Path}
    BSave $Record $result
    $script:bLastReturn=$result
}
function GDecision($Native,$Analysis,$Result,$Expected,[double]$Overall) {
    if ([double]::IsNaN($Overall) -or [double]::IsInfinity($Overall) -or $Overall -lt 0 -or $Overall -gt 3000) { return 'INCOMPLETE' }
    foreach ($r in @($Native,$Analysis)) {
        if ($null -eq $r -or $r.returned -isnot [bool] -or $r.returned -ne $true -or $r.invocation_succeeded -isnot [bool] -or $r.invocation_succeeded -ne $true -or $r.native_rc -isnot [int] -or $r.native_rc -ne 0 -or $r.new_error -isnot [bool] -or $r.new_error -ne $false -or $r.exception) { return 'INCOMPLETE' }
    }
    if ($Analysis.elapsed_seconds -isnot [double] -or [double]::IsNaN($Analysis.elapsed_seconds) -or [double]::IsInfinity($Analysis.elapsed_seconds) -or $Analysis.elapsed_seconds -lt 0 -or $Analysis.elapsed_seconds -gt 600) { return 'INCOMPLETE' }
    if ($null -eq $Result -or $null -eq $Result.errors -or $Result.run_id -cne $Expected.run_id -or $Result.code_manifest_sha256 -cne $Expected.manifest_sha256 -or $Result.limited_result -cne 'TRIGGER_AND_SAMPLED_DATA_ACCEPTABLE' -or $Result.overall -cne 'INCOMPLETE' -or @($Result.errors).Count -ne 0) { return 'INCOMPLETE' }
    return 'AWAITING_LIMITED_EXTERNAL_ACCEPTANCE'
}
try {
    if ($PSVersionTable.PSEdition -cne 'Desktop' -or $PSVersionTable.PSVersion.Major -ne 5) { throw 'POWERSHELL_51_REQUIRED' }
    if ((BHash (Join-Path $PSHOME 'powershell.exe')) -cne '8bb6fa8c283b4d92120b1ef249a9b311b0f804d4cabbe9981159976c8be76a5e') { throw 'POWERSHELL_IDENTITY' }
    if ([Console]::IsInputRedirected) { throw 'INPUT_REDIRECTED' }
    if ((BHash (Join-Path $bRoot 'CODE_MANIFEST.json')) -cne $ManifestSha) { throw 'MANIFEST_IDENTITY' }
    $manifest=BRead (Join-Path $bRoot 'CODE_MANIFEST.json')
    foreach ($r in $manifest.files) {
        $p=Join-Path $bRoot $r.file
        if ((BHash $p) -cne $r.sha256 -or (Get-Item -LiteralPath $p).Length -ne $r.bytes) { throw 'MANIFEST_FILE_IDENTITY' }
    }
    $c=BRead (Join-Path $bRoot 'CONTRACT.json')
    $a=BRead $c.approval_path
    $release=BRead $c.release_path
    if ($a.approved -ne $true -or $a.native1198_one_shot -ne $true -or $a.code_manifest_sha256 -cne $ManifestSha -or $release.code_manifest_sha256 -cne $ManifestSha -or $release.changed_branch_validation -cne 'PASS') { throw 'INACTIVE_NO_NATIVE_AUTHORIZATION' }
    if ((BHash $bPython) -cne $c.python.sha256 -or (Get-Item -LiteralPath $bPython).Length -ne $c.python.bytes) { throw 'PYTHON_IDENTITY' }
    if ((Test-Path -LiteralPath $bEvidence) -or (Test-Path -LiteralPath $c.run_root)) { throw 'EXISTING_PATH_NO_RETRY' }
    Set-Location -LiteralPath $c.cwd -ErrorAction Stop
    [void][IO.Directory]::CreateDirectory($bEvidence);$bOwned=$true
    Start-Transcript -LiteralPath (Join-Path $bEvidence 'PARENT_TRANSCRIPT.txt') -NoClobber -ErrorAction Stop | Out-Host
    $bTranscript=$true
    BSave 'PARENT_START.json' @{source='USER_VISIBLE_POWERSHELL_PARENT';manifest_sha256=$ManifestSha;approval=(BRef $c.approval_path);release=(BRef $c.release_path);cwd=(Get-Location).Path;start_utc=[DateTime]::UtcNow.ToString('o');budget_seconds=3000}
    $entry=Join-Path $bRoot 'src/candidate_entry.py'
    BInvoke 'native' @('-I','-S','-B','-X','utf8',$entry,'execute','--approval',$c.approval_path,'--manifest-sha',$ManifestSha) 'NATIVE_PARENT_RETURN.json'
    $bRunReturn=$bLastReturn
    # Analyze existing failure evidence once as well; it cannot erase native failure.
    if (Test-Path -LiteralPath (Join-Path $c.run_root 'NATIVE_STATE.json')) {
        BInvoke 'analysis' @('-I','-S','-B','-X','utf8',$entry,'analyze','--approval',$c.approval_path,'--manifest-sha',$ManifestSha) 'ANALYSIS_PARENT_RETURN.json'
        $bAnalysisReturn=$bLastReturn
    }
    $bDeliveryStart=$bClock.Elapsed.TotalSeconds
    $result=$null
    $resultPath=Join-Path $c.run_root 'TRIGGER_RESULT.json'
    if (Test-Path -LiteralPath $resultPath) { $result=BRead $resultPath }
    $limited=GDecision $bRunReturn $bAnalysisReturn $result @{run_id=$c.run_id;manifest_sha256=$ManifestSha} $bClock.Elapsed.TotalSeconds
    if ($bClock.Elapsed.TotalSeconds -gt 3000) { $limited='INCOMPLETE';$bErrors+=@{stage='budget';error='OVERALL_BUDGET'} }
    BSave 'PARENT_LOCAL_DECISION.json' @{limited=$limited;overall='INCOMPLETE';native_return=$bRunReturn;analysis_return=$bAnalysisReturn;auto_retry=$false}
} catch {
    $bErrors+=@{stage='parent';error=$_.ToString();elapsed_seconds=$bClock.Elapsed.TotalSeconds}
    [Console]::WriteLine(('STOP: '+$_.ToString()))
} finally {
    if ($bOwned) {
        if ($null -eq $bDeliveryStart) { $bDeliveryStart=$bClock.Elapsed.TotalSeconds }
        try {
            if ($bTranscript) { Stop-Transcript -ErrorAction Stop | Out-Host;$bTranscript=$false }
            $snapshot=$bClock.Elapsed.TotalSeconds
            $within=($snapshot -le 3000 -and ($snapshot-$bDeliveryStart) -le 300)
            BSave 'FINAL_BOUNDARY.json' @{source='USER_VISIBLE_POWERSHELL_PARENT';elapsed_seconds=$snapshot;delivery_elapsed_seconds=($snapshot-$bDeliveryStart);within_limits=$within;errors=$bErrors;transcript=(BRef (Join-Path $bEvidence 'PARENT_TRANSCRIPT.txt'));overall='INCOMPLETE';status='AWAITING_EXTERNAL_ACCEPTANCE';raw_host_rc='not_known_before_return'}
            [Console]::WriteLine((ConvertTo-Json -Compress -Depth 10 @{kind='USER_PARENT_FINAL_RETURN';boundary=(BRef (Join-Path $bEvidence 'FINAL_BOUNDARY.json'));snapshot_seconds=$bClock.Elapsed.TotalSeconds;overall='INCOMPLETE'}))
        } catch { [Console]::WriteLine(('FINAL_RECORD_ERROR: '+$_.ToString()));$bErrors+=@{stage='final_record';error=$_.ToString()} }
    }
    [Console]::WriteLine('STOP. No rerun, cleanup fallback, policy toggle or additional solve. Preserve this output.')
}
