# Read-only analysis of submitted, existing records. No DEM execution.
$ErrorActionPreference = 'Stop'
function FileSha256([string]$path) {
    $hasher = [System.Security.Cryptography.SHA256]::Create()
    $stream = [System.IO.File]::OpenRead($path)
    try { return ([BitConverter]::ToString($hasher.ComputeHash($stream))).Replace('-', '').ToLowerInvariant() }
    finally { $stream.Dispose(); $hasher.Dispose() }
}
$reviewRoot = Split-Path $PSScriptRoot -Parent
$pressurePath = Join-Path $reviewRoot 'source/docs/data/ps73_compaction_curve_20261006/curve/pressure.csv'
$archivePath = Join-Path $reviewRoot 'source/docs/data/ps73_compaction_curve_20261006/raw/ps73_logs.tgz'
$rawMember = 'home/yonghoon/dem_test/ps45/logs/output_ps_7_3_r45_r8_220537.out'
$phasePressure = @(Import-Csv -LiteralPath $pressurePath | Where-Object { $_.phase -eq '4' })
$rawLines = @(tar -xOzf $archivePath $rawMember)
if ($LASTEXITCODE -ne 0) { throw 'Cannot read submitted log archive' }
$phaseOn = $false
$regular = [System.Collections.Generic.List[object]]::new()
$rawLineNumber = 0
foreach ($line in $rawLines) {
    $rawLineNumber++
    if ($line -match '^====== PHASE 4') { $phaseOn = $true; continue }
    if (-not $phaseOn) { continue }
    $fields = $line.Trim() -split '\s+'
    if ($fields.Count -eq 5 -and $fields[0] -match '^\d+$') {
        $step = [int]$fields[0]
        # Exclude setup at 3125000; the CSV phase-4 records begin at 3126000.
        if ($step -gt 3125000 -and $step -le 3225000) {
            $regular.Add([pscustomobject]@{ step=$step; pressure=1000*[double]$fields[4]; ke=[double]$fields[2]; raw_line=$rawLineNumber })
        }
    }
}
function Mean($values) { return [double](($values | Measure-Object -Average).Average) }
function Std($values) {
    $mu = Mean $values
    return [math]::Sqrt((($values | ForEach-Object { ($_-$mu)*($_-$mu) } | Measure-Object -Sum).Sum)/($values.Count-1))
}
$tail = @($regular | Select-Object -Last 25)
$tailPressure = Mean @($tail | ForEach-Object { $_.pressure })
$baseWindows = for ($j=0; $j -lt 5; $j++) { Mean @($tail[($j*5)..($j*5+4)] | ForEach-Object { $_.ke }) }
$baseKe = @($baseWindows | Sort-Object)[2]
$windows = @()
for ($end=3130000; $end -le 3225000; $end+=5000) {
    $window = @($regular | Where-Object { $_.step -gt $end-5000 -and $_.step -le $end })
    $p = @($window | ForEach-Object { $_.pressure })
    $mu = Mean $p
    $ke = Mean @($window | ForEach-Object { $_.ke })
    $delta = if ($windows.Count) { [math]::Abs($mu-$windows[-1].mean_mpa) } else { $null }
    $threshold = [math]::Max(.005*[math]::Abs($mu), .05)
    $windows += [pscustomobject]@{ end=$end; mean_mpa=$mu; sd_mpa=(Std $p); bias_to_tail_mpa=($mu-$tailPressure); ke=$ke; s1=($null -ne $delta -and $delta -le $threshold); s2_translation_only=($ke -le 10*$baseKe); pressure_difference_mpa=$delta; threshold_mpa=$threshold; raw_lines=@($window | ForEach-Object { $_.raw_line }) }
}
$firstS1 = $null
$firstJoint = $null
for ($j=3; $j -lt $windows.Count; $j++) {
    if ($null -eq $firstS1 -and $windows[$j].s1 -and $windows[$j-1].s1) { $firstS1=$windows[$j].end }
    if ($null -eq $firstJoint -and $windows[$j].s1 -and $windows[$j-1].s1 -and $windows[$j].s2_translation_only -and $windows[$j-1].s2_translation_only) { $firstJoint=$windows[$j].end }
}
$csvMap = @{}
foreach ($row in $phasePressure) { $csvMap[[int]$row.step]=[double]$row.pressure_mpa }
$pressureAgreement = ($regular | ForEach-Object { [math]::Abs($_.pressure-$csvMap[$_.step]) } | Measure-Object -Maximum).Maximum
$h0 = 111.052
$coarse = .20
$fine = .05
$pairDelta = .10
$rFine = 100*$fine/$h0
$b = 2*$pairDelta+$rFine
$chosenWindows = @($windows | Where-Object { $_.end -ge 3165000 -and $_.end -le 3205000 })
$peaks = @()
for ($j=1; $j -lt $regular.Count-1; $j++) {
    if ($regular[$j].step -le 3162000 -and $regular[$j].pressure -gt $regular[$j-1].pressure -and $regular[$j].pressure -gt $regular[$j+1].pressure) {
        $peaks += [pscustomobject]@{step=$regular[$j].step; pressure_mpa=$regular[$j].pressure; excess_over_tail_mpa=($regular[$j].pressure-$tailPressure)}
    }
}
$peakEfold = ($peaks[-1].step-$peaks[0].step)/[math]::Log($peaks[0].excess_over_tail_mpa/$peaks[-1].excess_over_tail_mpa)
$result = [ordered]@{
    purpose='Existing CSV/log arithmetic and labelled hypothetical estimator counterexamples; no simulations'
    input_sha256=(FileSha256 $pressurePath)
    phase4_csv_rows=$phasePressure.Count
    phase4_regular_log_rows=$regular.Count
    max_csv_log_pressure_difference_mpa=$pressureAgreement
    sampling_limit='Original records every 1000 steps; proposed fix ave/time every 100 steps cannot be reconstructed. This is a 5-sample window diagnostic, not a replay of future S1/S2.'
    tail25_mean_mpa=$tailPressure
    early_local_maxima=$peaks
    first_to_last_peak_envelope_efold_steps=$peakEfold
    tail_ke_five_window_means=$baseWindows
    base_translation_ke=$baseKe
    first_s1_two_pass_end=$firstS1
    first_s1_translation_s2_two_pass_end=$firstJoint
    joint_test_limit='Rotation KE absent from original log; this is NOT a full S2 or S3/S4 pass.'
    windows=$chosenWindows
    coarse_crossing_counterexample=[ordered]@{ h0_um=$h0; pressures_mpa=@(4,0); bracket_um=$coarse; interpolated_crossing_increment_um=.15; fine_resolution_pp=$rFine; actual_bracket_resolution_pp=(100*$coarse/$h0); ratio=($coarse/$fine) }
    band_semantics_counterexample=[ordered]@{ delta_num_pp=$pairDelta; r_int_pp=$rFine; b_pp=$b; observed_rho_pp=@(5,5.3); claimed_order_by_difference_gt_b=(.3 -gt $b); overlaps_if_b_is_per_bed_half_width=((5+$b) -gt (5.3-$b)); note='Not a proof the intended b is a half-width. Registration must distinguish per-bed interval from pairwise threshold.' }
    nontransitive_indifference_counterexample=[ordered]@{ rho_pp=@(0,.08,.16); pair_threshold_pp=.10; adjacent_differences=@(.08,.08); outer_difference=.16; note='Checking only adjacent pairs misses a resolved outer pair; overlapping/indistinguishable pairs must not be collapsed into equivalence groups.' }
    interpolation_asymmetry_counterexample=[ordered]@{ bracket_um=.05; normalized_linear_crossing=.99; point_error_toward_lower_endpoint_um=.0495; unjustified_half_bracket_um=.025; note='Monotonicity alone bounds the crossing by the whole actual bracket, not +/- half a bracket about a non-midpoint linear interpolant.' }
}
$reviewJson = $result | ConvertTo-Json -Depth 8
$reviewEvidence = Join-Path (Split-Path $PSScriptRoot -Parent) 'evidence/design_arithmetic.json'
[System.IO.File]::WriteAllText($reviewEvidence, $reviewJson, [System.Text.UTF8Encoding]::new($false))
$reviewJson
