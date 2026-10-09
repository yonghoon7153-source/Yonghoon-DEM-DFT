$ErrorActionPreference='Stop'
$fixtureRoot=Split-Path -Parent $PSScriptRoot
$candidateRoot=Split-Path -Parent $fixtureRoot
$sessionClock=[Diagnostics.Stopwatch]::StartNew()
$utf8=New-Object Text.UTF8Encoding($false)
$records=New-Object Collections.Generic.List[object]
$global:S1ValidationReached=New-Object Collections.Generic.List[string]
$breakpoints=@()
$producerSeal=$null
$normalDecision=$null
function HHash([byte[]]$Bytes) {
    $sha=[Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($sha.ComputeHash($Bytes))).Replace('-','').ToLowerInvariant() }
    finally { $sha.Dispose() }
}
function HWrite($Name,$Object) {
    $json=$Object|ConvertTo-Json -Depth 100
    [IO.File]::WriteAllText((Join-Path $fixtureRoot ('results/'+$Name)), $json, $utf8)
}
function HProducer([string]$Id) {
    $path=Join-Path $fixtureRoot ('results/producers/'+$Id+'.json')
    $contextPath=Join-Path $fixtureRoot ('results/producers/'+$Id+'.context.json')
    $raw=[IO.File]::ReadAllBytes($path)
    $contextRaw=[IO.File]::ReadAllBytes($contextPath)
    foreach ($item in @(@{relative=('results/producers/'+$Id+'.json');raw=$raw},@{relative=('results/producers/'+$Id+'.context.json');raw=$contextRaw})) {
        $pin=@($producerSeal.files|Where-Object {$_.path -ceq $item.relative})
        HRequire ($pin.Count -eq 1) ('SECOND_SEAL_FILE_COUNT:'+ $item.relative)
        HRequire ($item.raw.Length -eq $pin[0].bytes -and (HHash $item.raw) -ceq $pin[0].sha256) ('SECOND_SEAL_BYTES:'+ $item.relative)
    }
    return @{RawText=$utf8.GetString($raw);Result=($utf8.GetString($raw)|ConvertFrom-Json);Context=($utf8.GetString($contextRaw)|ConvertFrom-Json);
        source=@{producer_id=$Id;path=$path;bytes=$raw.Length;sha256=(HHash $raw);
            context_path=$contextPath;context_bytes=$contextRaw.Length;context_sha256=(HHash $contextRaw)}}
}
function HRequire([bool]$Condition,[string]$Reason) {
    if (-not $Condition) { throw ('HARNESS_FIXTURE_OR_ASSERTION:'+ $Reason) }
}
try {
    $plan=([IO.File]::ReadAllText((Join-Path $fixtureRoot 'VALIDATION_PLAN_CORRECTED.json'))|ConvertFrom-Json)
    $recipes=([IO.File]::ReadAllText((Join-Path $PSScriptRoot 'PS_INPUT_RECIPES.json'))|ConvertFrom-Json)
    $producerSeal=([IO.File]::ReadAllText((Join-Path $fixtureRoot 'results/PS_PRODUCER_SEAL.json'))|ConvertFrom-Json)
    HRequire ($producerSeal.kind -ceq 'S1O_R1_004_REUSED_PRODUCER_SEAL' -and $producerSeal.python_status -ceq 'PASS' -and $producerSeal.python_case_count -eq 99) 'SECOND_SEAL_PYTHON_PASS'
    HRequire ((HHash ([IO.File]::ReadAllBytes((Join-Path $candidateRoot 'CODE_MANIFEST.json')))) -ceq $producerSeal.source_manifest_sha256) 'SECOND_SEAL_SOURCE_MANIFEST'
    HRequire ((HHash ([IO.File]::ReadAllBytes($PSCommandPath))) -ceq $producerSeal.harness_sha256) 'SECOND_SEAL_HARNESS'
    $requiredProducerFiles=@()
    foreach ($producer in @('CHARGE01','CHARGE03','CHARGE_R109','POLICY02','POLICY03')) {
        $requiredProducerFiles+=@(('results/producers/'+$producer+'.json'),('results/producers/'+$producer+'.context.json'))
    }
    HRequire (@($producerSeal.files).Count -eq 10) 'SECOND_SEAL_EXACT_SET_COUNT'
    foreach ($relative in $requiredProducerFiles) {
        $pin=@($producerSeal.files|Where-Object {$_.path -ceq $relative})
        HRequire ($pin.Count -eq 1) ('SECOND_SEAL_EXACT_SET:'+ $relative)
        $raw=[IO.File]::ReadAllBytes((Join-Path $fixtureRoot $relative))
        HRequire ($raw.Length -eq $pin[0].bytes -and (HHash $raw) -ceq $pin[0].sha256) ('SECOND_SEAL_FILE:'+ $relative)
    }
    $sourcePath=Join-Path $candidateRoot 'candidate/Parent.ps1.inactive.txt'
    $sourceBytes=[IO.File]::ReadAllBytes($sourcePath)
    $sourceText=$utf8.GetString($sourceBytes).Replace("`r`n","`n")
    $lines=$sourceText.Split([char]10)
    $functionTexts=New-Object Collections.Generic.List[string]
    $spans=New-Object Collections.Generic.List[object]
    foreach ($span in @($plan.extraction_spans|Where-Object {$_.source -ceq 'candidate/Parent.ps1.inactive.txt'})) {
        $start=[int]$span.start_line; $end=[int]$span.end_line
        if ($span.name -ceq 'S1Sha') {$end=23}
        HRequire ($end -ge $start) 'EXTRACTION_RANGE'
        $text=[string]::Join("`n",$lines[($start-1)..($end-1)])
        $hash=HHash ($utf8.GetBytes($text))
        HRequire ($hash -ceq $span.sha256) ('EXTRACTION_SHA:'+ $span.name)
        if ($span.name -ceq 'S1Sha') { HRequire (($start -eq 23) -and ($end -eq 23) -and ($utf8.GetByteCount($text) -eq 90)) 'S1SHA_CORRECTED_SPAN' }
        $functionTexts.Add($text)
        $spans.Add(@{name=$span.name;start_line=$start;end_line=$end;bytes=$utf8.GetByteCount($text);sha256=$hash;normalization='CRLF to LF; trailing LF excluded'})
    }
    HRequire ($spans.Count -eq 15) 'FUNCTION_SET_COUNT'
    # These are only the sealed pure functions; the inactive terminal throw is excluded.
    . ([scriptblock]::Create([string]::Join("`n`n",$functionTexts)))
    foreach ($span in @($spans.ToArray()|Where-Object {$_.name -in @('S1Decision','S1NativeAxis','S1Fields','S1Coverage','S1ChargeFields','S1ComparisonNumerics','S1FinalReturn')})) {
        $action=[scriptblock]::Create("`$global:S1ValidationReached.Add('"+$span.name+"')")
        $breakpoints+=Set-PSBreakpoint -Command $span.name -Action $action
    }
    HWrite 'ps_extraction_observed.json' @{source_path=$sourcePath;source_bytes=$sourceBytes.Length;source_sha256=(HHash $sourceBytes);spans=@($spans.ToArray())}
    $cases=@($plan.cases|Where-Object {$_.id -like 'PARENT*'})
    HRequire ($cases.Count -eq 3) 'PARENT_CASE_COUNT'
    HRequire (@($recipes.cases).Count -eq 3) 'RECIPE_CASE_COUNT'
    foreach ($case in $cases) {
        if ($sessionClock.Elapsed.TotalSeconds -gt 180) { throw 'PS_SESSION_BUDGET' }
        $id=[string]$case.id
        $global:S1ValidationReached.Clear()
        $currentDiagnostic=@{id=$id;target_entered=$false;reach=@();transport=$null}
        HWrite 'current_case_diagnostic.json' $currentDiagnostic
        $recipe=@($recipes.cases|Where-Object {$_.id -ceq $id})
        HRequire ($recipe.Count -eq 1) ('UNIQUE_RECIPE:'+ $id)
        HRequire ($recipe[0].expected -ceq $case.expected -and $recipe[0].expected_field_path -ceq $case.expected_field_path -and $recipe[0].positive_control_case_id -ceq $case.positive_control_case_id) ('RECIPE_PLAN_BINDING:'+ $id)
        $producerId='CHARGE01'
        if ($id -in @('PARENT02','PARENT_R114')) {$producerId='POLICY03'}
        elseif ($id -in @('PARENT03','PARENT_R105','PARENT_R108')) {$producerId='CHARGE_R109'}
        elseif ($id -eq 'PARENT14') {$producerId='CHARGE03'}
        elseif ($id -in @('PARENT_R113','PARENT_R115')) {$producerId='POLICY02'}
        HRequire ($recipe[0].producer_id -ceq $producerId) ('RECIPE_PRODUCER:'+ $id)
        $p=HProducer $producerId
        $result=$p.Result; $context=$p.Context
        $expected=$context.Expected; $native=$context.Native; $analysis=$context.Analysis; $completion=$context.Completion
        $mutations=@()
        $recipeTransport=$null
        switch ($id) {
            'PARENT04' {$native.rc='0';$mutations=@('Native.rc:int0->string0')}
            'PARENT05' {$native.fatal=$true;$mutations=@('Native.fatal:false->true')}
            'PARENT06' {$result.PSObject.Properties.Remove('comparison_details');$mutations=@('Result.comparison_details:removed')}
            'PARENT07' {$result.comparison='EXCEEDS_LIMITS';$mutations=@('Result.comparison:WITHIN->EXCEEDS')}
            'PARENT08' {$result.effective_coefficients.grade='CONFIG_ONLY';$mutations=@('Result.effective_coefficients.grade:CONFIG_ONLY')}
            'PARENT13' {$expected.PSObject.Properties.Remove('end_s');$mutations=@('Expected.end_s:removed')}
            'PARENT15' {$result.PSObject.Properties.Remove('initial_profile');$mutations=@('Result.initial_profile:removed')}
            'PARENT_R101' {$result.comparison_details.coverage.comparison_times[2]=$result.comparison_details.coverage.comparison_times[1];$mutations=@('Result.comparison_details.coverage.comparison_times[2]:duplicate[1]')}
            'PARENT_R102' {$result.comparison_details.coverage.comparison_times[2]='0.00025';$mutations=@('Result.comparison_details.coverage.comparison_times[2]:0.00025')}
            'PARENT_R103' {$result.comparison_details.coverage.comparison_times[2]='NaN';$mutations=@('Result.comparison_details.coverage.comparison_times[2]:NaN')}
            'PARENT_R104' {$result.comparison_details.coverage.comparison_times[-1]='120.1';$mutations=@('Result.comparison_details.coverage.comparison_times[-1]:120.1')}
            'PARENT_R105' {$result.comparison_details.coverage.comparison_times[-1]='90.1';$mutations=@('Result.comparison_details.coverage.comparison_times[-1]:90.1')}
            'PARENT_R106' {$swap=$result.comparison_details.coverage.comparison_times[1];$result.comparison_details.coverage.comparison_times[1]=$result.comparison_details.coverage.comparison_times[2];$result.comparison_details.coverage.comparison_times[2]=$swap;$mutations=@('Result.comparison_details.coverage.comparison_times[1]<->[2]')}
            'PARENT_R107' {
                $full=$result.comparison_details.coverage.full_intersection
                HRequire ($full[0] -ceq '0' -and $full[1] -ceq '0.0001' -and $full[2] -ceq '0.0002') 'R107_FIXED_NEIGHBOURS'
                HRequire ('0.00015' -cin $native.stored_times_s -and '0.00015' -cnotin $full) 'R107_FIXED_NATIVE_EXTRA'
                $full[1]='0.00015'
                $mutations=@('Result.comparison_details.coverage.full_intersection[1]:0.0001->0.00015')
            }
            'PARENT_R108' {$result.comparison_details.coverage.common_requested_count=[int]255;$result.comparison_details.coverage.comparison_count=[int]255;$result.comparison_details.coverage.comparison_times=@($expected.common_requested_times_s);$mutations=@('Result.comparison_details.coverage.common_requested_count:255','Result.comparison_details.coverage.comparison_count:255','Result.comparison_details.coverage.comparison_times:full255')}
            'PARENT_R109' {$result.charge_budget.grid_binding.actual_end_s='119.9';$mutations=@('Result.charge_budget.grid_binding.actual_end_s:119.9')}
            'PARENT_R110' {$result.charge_budget.records[1].t_s='0.000000015';$mutations=@('Result.charge_budget.records[1].t_s:0.000000015')}
            'PARENT_R111' {$result.charge_budget.grid_binding.global_identity.sha256=('f'*64);$mutations=@('Result.charge_budget.grid_binding.global_identity.sha256:f*64')}
            'PARENT_R112' {$result.charge_budget.PSObject.Properties.Remove('grid_binding');$mutations=@('Result.charge_budget.grid_binding:removed')}
            'PARENT_R113' {
                $pattern='("voltage_V"\s*:\s*\{[^{}]*"value"\s*:\s*)"0\.001"'
                $matches=[regex]::Matches($p.RawText,$pattern)
                HRequire ($matches.Count -eq 1) 'R113_SINGLE_JSON_VALUE_TOKEN'
                $mutant=[regex]::Replace($p.RawText,$pattern,'${1}0.001')
                HRequire ($mutant.Length -eq ($p.RawText.Length-2)) 'R113_QUOTES_ONLY_REMOVED'
                $result=$mutant|ConvertFrom-Json
                $parsedValue=$result.comparison_details.maxima.voltage_V.value
                $typeName=$(if($null -eq $parsedValue){'null'}else{$parsedValue.GetType().FullName})
                $currentDiagnostic.transport=@{source_sha256=$p.source.sha256;mutant_bytes=$utf8.GetByteCount($mutant);mutant_sha256=(HHash ($utf8.GetBytes($mutant)));token_match_index=$matches[0].Index;parsed_clr_type=$typeName;parsed_value=[string]$parsedValue}
                HWrite 'current_case_diagnostic.json' $currentDiagnostic
                HRequire ($null -ne $parsedValue -and $parsedValue -isnot [string] -and $parsedValue -isnot [bool] -and $typeName -in @('System.Decimal','System.Double','System.Single','System.Int32','System.Int64')) 'R113_NUMERIC_PARSE_TYPE'
                HRequire (-not [double]::IsNaN([double]$parsedValue) -and -not [double]::IsInfinity([double]$parsedValue) -and [decimal]$parsedValue -eq [decimal]0.001) 'R113_EXACT_FINITE_VALUE'
                $result.comparison_details.maxima.voltage_V.value=$null
                $restBefore=$result|ConvertTo-Json -Depth 100 -Compress
                $result.comparison_details.maxima.voltage_V.value=[double]$parsedValue
                $castValue=$result.comparison_details.maxima.voltage_V.value
                $currentDiagnostic.transport.cast_clr_type=$castValue.GetType().FullName
                $currentDiagnostic.transport.cast_value_roundtrip=$castValue.ToString('R',[Globalization.CultureInfo]::InvariantCulture)
                $currentDiagnostic.transport.double_bits_hex=([BitConverter]::DoubleToInt64Bits($castValue)).ToString('X16')
                $result.comparison_details.maxima.voltage_V.value=$null
                $restAfter=$result|ConvertTo-Json -Depth 100 -Compress
                $result.comparison_details.maxima.voltage_V.value=$castValue
                $currentDiagnostic.transport.other_leaves_unchanged=($restBefore -ceq $restAfter)
                HWrite 'current_case_diagnostic.json' $currentDiagnostic
                HRequire ($castValue -is [double] -and $restBefore -ceq $restAfter) 'R113_EXPLICIT_SINGLE_LEAF_DOUBLE'
                $recipeTransport=$currentDiagnostic.transport
                $mutations=@('Result.comparison_details.maxima.voltage_V.value:JSON string0.001->JSON number0.001')

            }
            'PARENT_R114' {$result.comparison='WITHIN_LIMITS_THIS_WINDOW';$result.comparison_details.status='WITHIN_LIMITS_THIS_WINDOW';$mutations=@('Result.comparison:WITHIN_LIMITS_THIS_WINDOW','Result.comparison_details.status:WITHIN_LIMITS_THIS_WINDOW')}
        }
        $global:S1ValidationReached.Clear()
        $caseClock=[Diagnostics.Stopwatch]::StartNew()
        $adapterLog=$null
        if ($id -in @('PARENT09','PARENT10','PARENT11','PARENT12','PARENT16')) {
            HRequire ($null -ne $normalDecision) 'FINAL_REUSES_ACTUAL_PARENT01_DECISION'
            $script:clockValues=@([double]99,[double]100)
            $overallLimit=[double]100;$deliveryStart=[double]90;$deliveryLimit=[double]10
            if ($id -eq 'PARENT10') {$script:clockValues=@([double]99,[double]100.1);$deliveryLimit=[double]20}
            if ($id -eq 'PARENT11') {$script:clockValues=@([double]99,[double]100.1);$overallLimit=[double]200}
            if ($id -eq 'PARENT16') {$deliveryStart=[double]100;$script:clockValues=@([double]99,[double]100)}
            $script:clockIndex=0;$script:writerCalls=0;$script:readbackCalls=0
            $clock={ $value=$script:clockValues[$script:clockIndex];$script:clockIndex++;return $value }
            $writer={param($value) $script:writerCalls++;return @{inert_boundary=$true;record=$value}}
            if ($id -eq 'PARENT09') {$writer={param($value) $script:writerCalls++;throw 'INERT_WRITER_FAILURE'}}
            $readback={param($value) $script:readbackCalls++;return @{sha256=('a'*64);byte_equal=$true}}
            $observed=S1FinalReturn $normalDecision $clock $writer $readback $overallLimit $deliveryStart $deliveryLimit
            $field='limited'
            $adapterLog=@{clock_values=$script:clockValues;clock_calls=$script:clockIndex;writer_calls=$script:writerCalls;readback_calls=$script:readbackCalls;overall_limit=$overallLimit;delivery_start=$deliveryStart;delivery_limit=$deliveryLimit;all_adapters_inert=$true}
        } else {
            $currentDiagnostic.target_entered=$true
            $observed=S1Decision $native $analysis $result $expected $completion
            $field=$(if ($case.expected_field_path -ceq 'return_value.reason') {'reason'} else {'status'})
        }
        $caseClock.Stop()
        $reach=@($global:S1ValidationReached.ToArray()|Select-Object -Unique)
        $needed=@('S1Decision')
        if ($id -in @('PARENT09','PARENT10','PARENT11','PARENT12','PARENT16')) {$needed=@('S1FinalReturn')}
        elseif ($case.required_reach -match 'S1Coverage') {$needed=@('S1Decision','S1Fields','S1Coverage')}
        elseif ($case.required_reach -match 'S1ChargeFields') {$needed=@('S1Decision','S1Fields','S1ChargeFields')}
        elseif ($case.required_reach -match 'S1ComparisonNumerics') {$needed=@('S1Decision','S1Fields','S1ComparisonNumerics')}
        elseif ($case.required_reach -match 'S1Fields') {$needed=@('S1Decision','S1Fields')}
        elseif ($case.required_reach -match 'S1NativeAxis') {$needed=@('S1Decision','S1NativeAxis')}
        if ($id -eq 'PARENT03') {$needed=@('S1Decision','S1NativeAxis','S1Fields')}
        $actual=[string]$observed.$field
        $reasonMatches=$actual -ceq [string]$case.expected
        $reachMatches=@($needed|Where-Object {$_ -cnotin $reach}).Count -eq 0
        $extraChecks=$true
        if ($id -eq 'PARENT03') {$extraChecks=($observed.native_completion -ceq 'PROTECTIVE_STOP' -and $observed.evidence_validity -ceq 'VALID')}
        if ($id -eq 'PARENT14') {$extraChecks=($observed.charge_budget -ceq 'INCONCLUSIVE' -and $observed.evidence_validity -ceq 'VALID')}
        if ($id -eq 'PARENT02') {$extraChecks=($observed.comparison -ceq 'EXCEEDS_LIMITS')}
        if ($id -eq 'PARENT_R115') {$extraChecks=($observed.comparison -ceq 'WITHIN_LIMITS_THIS_WINDOW')}
        if ($id -eq 'PARENT09') {$extraChecks=(@($observed.record_errors).Count -eq 1 -and $observed.record_errors[0].reason -match 'INERT_WRITER_FAILURE')}
        if ($id -in @('PARENT10','PARENT11')) {$extraChecks=(@($observed.record_errors).Count -eq 1 -and $observed.record_errors[0].reason -match 'POST_WRITE_BUDGET' -and -not $observed.within_limits -and $observed.prior_decision.status -ceq 'AWAITING_S1_LIMITED_EXTERNAL_REVIEW')}
        if ($id -eq 'PARENT12') {$extraChecks=($observed.within_limits -and @($observed.record_errors).Count -eq 0 -and $observed.snapshot_seconds -eq 100)}
        if ($id -eq 'PARENT16') {$extraChecks=(@($observed.record_errors).Count -eq 1 -and $observed.record_errors[0].reason -match 'PRE_WRITE_BUDGET' -and $script:writerCalls -eq 0)}
        if($id -eq 'PARENT_R113'){$extraChecks=$extraChecks -and $observed.stage -ceq 'comparison_numerics'}
        if($id -eq 'PARENT_R114'){$extraChecks=$extraChecks -and $observed.stage -ceq 'fields'}
        $currentDiagnostic.reach=$reach
        HWrite 'current_case_diagnostic.json' $currentDiagnostic
        $pass=$reasonMatches -and $reachMatches -and $extraChecks
        $record=@{id=$id;input_id=$case.input_id;producer=$p.source;mutations=$mutations;recipe=$recipe[0];json_transport=$recipeTransport;expected_field=$field;expected=[string]$case.expected;observed=$actual;target_reach=$reach;required_functions=$needed;reason_matches=$reasonMatches;reach_matches=$reachMatches;extra_assertions=$extraChecks;result=$(if($pass){'PASS'}else{'FAIL'});elapsed_s=$caseClock.Elapsed.TotalSeconds;raw_return=$observed;adapter_observation=$adapterLog}
        $records.Add($record)
        Write-Output ($record|ConvertTo-Json -Depth 100 -Compress)
        if (-not $pass) {throw ('FIRST_UNEXPECTED_CASE_FAILURE:'+ $id)}
        if ($id -eq 'PARENT01') {$normalDecision=$observed}
    }
    $sessionClock.Stop()
    HRequire ($sessionClock.Elapsed.TotalSeconds -le 180) 'SESSION_LIMIT_AFTER_LAST_CASE'
    HWrite 'ps_results.json' @{status='PASS';case_count=$records.Count;cases=@($records.ToArray());elapsed_s=$sessionClock.Elapsed.TotalSeconds;limit_s=180;actual_native_calls=0;actual_gate_calls=0;actual_job_calls=0;engine_sessions=1}
    exit 0
} catch {
    $failure=@{diagnostic=$currentDiagnostic;status='INCOMPLETE';first_error=$_.ToString();script_stack=$_.ScriptStackTrace;case_count=$records.Count;cases=@($records.ToArray());current_case=$id;elapsed_s=$sessionClock.Elapsed.TotalSeconds;limit_s=180;later_cases_not_run=$true;retry=0}
    try {HWrite 'ps_first_failure.json' $failure} catch {Write-Error ('FOLLOWUP_RECORD_FAILURE:'+ $_.ToString()) -ErrorAction Continue}
    Write-Output ($failure|ConvertTo-Json -Depth 100 -Compress)
    exit 1
} finally {
    if ($breakpoints.Count -gt 0) {$breakpoints|Remove-PSBreakpoint}
    Remove-Variable -Name S1ValidationReached -Scope Global -ErrorAction SilentlyContinue
}
