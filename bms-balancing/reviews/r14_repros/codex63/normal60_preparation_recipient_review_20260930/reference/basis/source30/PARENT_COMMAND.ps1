# INACTIVE CANDIDATE. Not executed/tested. Separate validation release + native approval required.
param([Parameter(Mandatory=$true)][ValidatePattern('^[0-9a-f]{64}$')][string]$ManifestSha)
$ErrorActionPreference='Stop'
$bClock=[Diagnostics.Stopwatch]::StartNew()
$bRoot='C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/normal30_limited_validation_R1_20260928'
$bEvidence=Join-Path $bRoot 'future_parent_001'
$bPython='C:/Users/BML/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$bOwned=$false
$bTranscript=$false
$bLastReturn=$null
$bErrors=@()
$bRunReturn=$null
$bAnalysisReturn=$null
$bDeliveryStart=$null
$limited='INCOMPLETE'
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
    if (-not (GNumber $Overall 0 5100)) { return 'INCOMPLETE' }
    foreach ($r in @($Native,$Analysis)) {
        if ($null -eq $r -or $r.returned -isnot [bool] -or -not $r.returned -or $r.invocation_succeeded -isnot [bool] -or $r.native_rc -isnot [int] -or $r.new_error -isnot [bool] -or $r.new_error -or $r.exception) { return 'INCOMPLETE' }
    }
    if ($Native.native_rc -ne 0 -or -not $Native.invocation_succeeded) { return 'INCOMPLETE' }
    if (-not (GNumber $Analysis.elapsed_seconds 0 900)) { return 'INCOMPLETE' }
    if (-not (GStruct $Result) -or $Result.errors -isnot [array] -or @($Result.errors).Count -ne 0 -or $Result.run_id -cne $Expected.run_id -or $Result.code_manifest_sha256 -cne $Expected.manifest_sha256) { return 'INCOMPLETE' }
    $normal=($Result.limited_result -ceq 'NORMAL_30S_DIAGNOSTIC_COMPLETE')
    $protected=($Result.limited_result -ceq 'PROTECTED_STOP_30S_INCOMPLETE')
    if (-not $normal -and -not $protected) { return 'INCOMPLETE' }
    if ($normal -and ($Analysis.native_rc -ne 0 -or -not $Analysis.invocation_succeeded)) { return 'INCOMPLETE' }
    if ($protected -and ($Analysis.native_rc -ne 1 -or $Analysis.invocation_succeeded)) { return 'INCOMPLETE' }
    foreach ($axis in @('sampled_comparison','preservation','process_cleanup','policy_preservation')) {
        if ($Result.$axis -cne 'PASS') { return 'INCOMPLETE' }
    }
    if ($Result.overall -cne 'INCOMPLETE' -or $Result.normal_gate -cne 'INCOMPLETE' -or $Result.effective_policy -cne 'UNVERIFIED' -or $Result.native_approved_by_this_result -isnot [bool] -or $Result.native_approved_by_this_result) { return 'INCOMPLETE' }
    foreach ($key in @('termination','native_termination','runtime_settings','numeric','tables_manifest')) {
        if (-not (GStruct $Result.$key)) { return 'INCOMPLETE' }
    }
    $term=$Result.termination;$native=$Result.native_termination;$numeric=$Result.numeric;$coverage=$numeric.coverage
    if ($numeric.status -cne 'PASS' -or -not (GStruct $coverage) -or $coverage.status -cne 'PASS' -or $Result.runtime_settings.status -cne 'PASS' -or $Result.runtime_settings.requested_count -ne 437 -or -not (GStruct $Result.runtime_settings.settings)) { return 'INCOMPLETE' }
    if ($native.no_integration_after_termination -isnot [bool] -or -not $native.no_integration_after_termination -or $native.after_stop_export_allowed -isnot [bool] -or -not $native.after_stop_export_allowed -or -not (GNumber $native.reported_time 0 30)) { return 'INCOMPLETE' }
    if ($term.threshold_mol_m3 -cne '0' -or $term.active_guards -isnot [array] -or $term.stored_times_s -isnot [array] -or @($term.stored_times_s).Count -lt 3 -or $term.ties -isnot [array] -or @($term.ties).Count -ne @($term.stored_times_s).Count -or $native.step_count -ne @($term.stored_times_s).Count) { return 'INCOMPLETE' }
    if (-not (GNumber $term.final_time_s 0 30) -or -not (GNumber $term.safe_prefix_end_s 0 30) -or $term.final_time_s -cne $term.stored_times_s[-1]) { return 'INCOMPLETE' }
    if ($normal) {
        if ($Result.diagnostic -cne 'NORMAL_30S_REACHED' -or $term.status -cne 'NORMAL_30S_REACHED' -or $native.status -cne 'NATIVE_NORMAL_END_MATCHED' -or $null -ne $native.stop_reason -or @($term.active_guards).Count -ne 0 -or -not (GNumber $term.final_time_s 30 30) -or -not (GNumber $term.safe_prefix_end_s 30 30)) { return 'INCOMPLETE' }
    } else {
        if ($Result.diagnostic -cne 'PROTECTIVE_STOP_OBSERVED' -or $term.status -cne 'PROTECTIVE_STOP_OBSERVED' -or $native.status -cne 'NATIVE_PROTECTIVE_STOP_MATCHED' -or @($term.active_guards).Count -lt 1) { return 'INCOMPLETE' }
        $reasons=@{electrolyte_guard='Electrolyte minimum <= threshold';ocp_guard='OCP surface outside table';surface_guard='Invalid surface concentration'}
        $matched=$false
        foreach ($guard in $term.active_guards) {
            if (-not $reasons.ContainsKey($guard)) { return 'INCOMPLETE' }
            if ($native.stop_reason -ceq $reasons[$guard]) { $matched=$true }
        }
        if (-not $matched -or -not (GNumber $term.t_minus 0 30) -or -not (GNumber $term.t_plus 0 30) -or [double]$term.t_minus -le 0 -or [double]$term.t_minus -ge [double]$term.t_plus -or $term.t_plus -cne $term.final_time_s -or $term.t_minus -cne $term.safe_prefix_end_s) { return 'INCOMPLETE' }
    }
    foreach ($tie in $term.ties) {
        if (-not (GHas $tie 'time_s') -or $tie.exact_minimum_domains -isnot [array] -or @($tie.exact_minimum_domains).Count -lt 1 -or $tie.near_tie_domains -isnot [array]) { return 'INCOMPLETE' }
    }
    foreach ($key in @('expected_requested','common_stored','missing_target','missing_baseline','target_noncommon','full_intersection','strict_requested_through_safe_end','missing_strict_requested')) {
        if (-not (GHas $coverage $key) -or $coverage.$key -isnot [array]) { return 'INCOMPLETE' }
    }
    if (@($coverage.expected_requested).Count -lt 2 -or @($coverage.common_stored).Count -lt 2 -or @($coverage.missing_target).Count -ne 0 -or @($coverage.missing_baseline).Count -ne 0 -or @($coverage.missing_strict_requested).Count -ne 0 -or $coverage.common_count -isnot [int] -or $coverage.common_count -ne @($coverage.common_stored).Count -or $coverage.full_intersection_count -ne @($coverage.full_intersection).Count -or $coverage.common_first -cne $coverage.common_stored[0] -or $coverage.common_last -cne $coverage.common_stored[-1]) { return 'INCOMPLETE' }
    if (-not (GNumber $coverage.common_first 0 0) -or -not (GNumber $coverage.common_last 0 5) -or [double]$coverage.common_last -le 0) { return 'INCOMPLETE' }
    if ($normal -and (@($coverage.expected_requested).Count -ne 187 -or @($coverage.strict_requested_through_safe_end).Count -ne 437 -or -not (GNumber $coverage.common_last 5 5) -or -not (GNumber $coverage.comparison_end_s 5 5))) { return 'INCOMPLETE' }
    foreach ($time in $coverage.common_stored) { if ($coverage.full_intersection -cnotcontains $time) { return 'INCOMPLETE' } }
    $maxima=@{maximum_voltage_delta_V=0.001;maximum_surface_delta=0.0001;maximum_Li_relative_drift=0.000001;maximum_voltage_identity_V=0.00000001}
    foreach ($key in $maxima.Keys) { if (-not (GHas $numeric $key) -or -not (GNumber $numeric.$key 0 $maxima[$key])) { return 'INCOMPLETE' } }
    if (-not (GStruct $numeric.initial_Li_components) -or -not (GStruct $numeric.late_interval)) { return 'INCOMPLETE' }
    foreach ($key in @('Li_N_mol_m2','Li_P_mol_m2','Li_electrolyte_mol_m2')) {
        if (-not (GStruct $numeric.initial_Li_components.$key) -or $numeric.initial_Li_components.$key.status -cne 'PASS' -or $numeric.initial_Li_components.$key.unit -cne 'mol/m^2' -or $numeric.initial_Li_components.$key.absolute_limit -cne '1e-9' -or -not (GHas $numeric.initial_Li_components.$key 'absolute_delta') -or -not (GNumber $numeric.initial_Li_components.$key.absolute_delta 0 0.000000001)) { return 'INCOMPLETE' }
    }
    if ($normal -and ($numeric.late_interval.status -cne 'OBSERVED' -or $numeric.late_interval.count -le 0 -or -not (GNumber $numeric.late_interval.last_time_s 30 30) -or -not (GStruct $numeric.late_interval.metrics))) { return 'INCOMPLETE' }
    $required=@('guard_binding.csv','axes_runtime_settings.csv','electrolyte_guard.csv','preflight_global.csv','preflight_boundary1.csv','preflight_boundary4.csv','axes_profile_N.csv','axes_profile_P.csv')
    foreach ($tag in @('eguard','nglobal','point1','point4','MinLinece','MaxLinece','profiletimes','profileN','profileP')) {
        foreach ($phase in @('configured','evaluated')) { $required+=('units_'+$tag+'_'+$phase+'.csv') }
    }
    $required+='units_eguard_inferred.csv'
    foreach ($name in $required) {
        if (-not (GHas $Result.tables_manifest $name)) { return 'INCOMPLETE' }
        $e=$Result.tables_manifest.$name
        if (-not (GStruct $e) -or [string]::IsNullOrWhiteSpace($e.path) -or $e.bytes -isnot [int] -or $e.bytes -le 0 -or $e.sha256 -isnot [string] -or $e.sha256 -cnotmatch '^[0-9a-f]{64}$') { return 'INCOMPLETE' }
    }
    if ($normal) { return 'AWAITING_30S_LIMITED_EXTERNAL_ACCEPTANCE' }
    return 'PROTECTED_STOP_30S_INCOMPLETE'
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
    if ($a.approved -ne $true -or $a.native30_one_shot -ne $true -or $a.code_manifest_sha256 -cne $ManifestSha -or $release.code_manifest_sha256 -cne $ManifestSha -or $release.changed_branch_validation -cne 'PASS') { throw 'INACTIVE_NO_NATIVE_AUTHORIZATION' }
    if ((BHash $bPython) -cne $c.python.sha256 -or (Get-Item -LiteralPath $bPython).Length -ne $c.python.bytes) { throw 'PYTHON_IDENTITY' }
    if ((Test-Path -LiteralPath $bEvidence) -or (Test-Path -LiteralPath $c.run_root)) { throw 'EXISTING_PATH_NO_RETRY' }
    Set-Location -LiteralPath $c.cwd -ErrorAction Stop
    [void][IO.Directory]::CreateDirectory($bEvidence);$bOwned=$true
    Start-Transcript -LiteralPath (Join-Path $bEvidence 'PARENT_TRANSCRIPT.txt') -NoClobber -ErrorAction Stop | Out-Host
    $bTranscript=$true
    BSave 'PARENT_START.json' @{source='USER_VISIBLE_POWERSHELL_PARENT';manifest_sha256=$ManifestSha;approval=(BRef $c.approval_path);release=(BRef $c.release_path);cwd=(Get-Location).Path;start_utc=[DateTime]::UtcNow.ToString('o');budget_seconds=5100}
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
    $resultPath=Join-Path $c.run_root 'DIAGNOSTIC_RESULT.json'
    if (Test-Path -LiteralPath $resultPath) { $result=BRead $resultPath }
    $limited=GDecision $bRunReturn $bAnalysisReturn $result @{run_id=$c.run_id;manifest_sha256=$ManifestSha} $bClock.Elapsed.TotalSeconds
    if ($bClock.Elapsed.TotalSeconds -gt 5100) { $limited='INCOMPLETE';$bErrors+=@{stage='budget';error='OVERALL_BUDGET'} }
    BSave 'PARENT_LOCAL_DECISION.json' @{limited=$limited;overall='INCOMPLETE';native_return=$bRunReturn;analysis_return=$bAnalysisReturn;auto_retry=$false}
} catch {
    $limited='INCOMPLETE'
    $bErrors+=@{stage='parent';error=$_.ToString();elapsed_seconds=$bClock.Elapsed.TotalSeconds}
    [Console]::WriteLine(('STOP: '+$_.ToString()))
} finally {
    if ($bOwned) {
        if ($null -eq $bDeliveryStart) { $bDeliveryStart=$bClock.Elapsed.TotalSeconds }
        try {
            if ($bTranscript) { Stop-Transcript -ErrorAction Stop | Out-Host;$bTranscript=$false }
            $snapshot=$bClock.Elapsed.TotalSeconds
            $within=($snapshot -le 5100 -and ($snapshot-$bDeliveryStart) -le 300)
            if (-not $within -or @($bErrors).Count -ne 0) { $limited='INCOMPLETE' }
            BSave 'FINAL_BOUNDARY.json' @{source='USER_VISIBLE_POWERSHELL_PARENT';observation_phase='PRE_WRITE';elapsed_seconds=$snapshot;delivery_elapsed_seconds=($snapshot-$bDeliveryStart);within_limits=$within;errors=$bErrors;transcript=(BRef (Join-Path $bEvidence 'PARENT_TRANSCRIPT.txt'));overall='INCOMPLETE';status='AWAITING_EXTERNAL_ACCEPTANCE';raw_host_rc=$null;host_boundary='SCRIPT_FINAL_RECORD_NOT_PROCESS_EXIT';body_completed_without_error=(@($bErrors).Count -eq 0);limited=$limited;local_decision=$(if (Test-Path -LiteralPath (Join-Path $bEvidence 'PARENT_LOCAL_DECISION.json')) { BRef (Join-Path $bEvidence 'PARENT_LOCAL_DECISION.json') } else { $null })}
            $boundaryRef=BRef (Join-Path $bEvidence 'FINAL_BOUNDARY.json')
            # One post-write observation after write/read-back/hash; do not rewrite the boundary.
            $postWrite=$bClock.Elapsed.TotalSeconds
            $postDelivery=$postWrite-$bDeliveryStart
            $within=($within -and $postWrite -le 5100 -and $postDelivery -le 300)
            if (-not $within) {
                $limited='INCOMPLETE'
                $bErrors+=@{stage='post_write_budget';error='FINAL_POST_WRITE_BUDGET';pre_write_seconds=$snapshot;post_write_seconds=$postWrite;post_write_delivery_seconds=$postDelivery}
            }
            [Console]::WriteLine((ConvertTo-Json -Compress -Depth 10 @{kind='USER_PARENT_FINAL_RETURN';observation_phase='POST_WRITE';limited=$limited;record_errors=$bErrors;within_limits=$within;host_boundary='SCRIPT_FINAL_RECORD_NOT_PROCESS_EXIT';raw_host_rc=$null;boundary=$boundaryRef;pre_write_seconds=$snapshot;snapshot_seconds=$postWrite;delivery_elapsed_seconds=$postDelivery;overall='INCOMPLETE'}))
        } catch { $limited='INCOMPLETE';[Console]::WriteLine(('FINAL_RECORD_ERROR: '+$_.ToString()));$bErrors+=@{stage='final_record';error=$_.ToString()} }
    }
    [Console]::WriteLine('STOP. No rerun, cleanup fallback, policy toggle or additional solve. Preserve this output.')
}
