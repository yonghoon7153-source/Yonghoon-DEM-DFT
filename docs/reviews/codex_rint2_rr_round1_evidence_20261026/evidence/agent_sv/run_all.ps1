$ErrorActionPreference = 'Stop'
$reviewRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$workspaceRoot = Split-Path $reviewRoot -Parent
$python = 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONPATH = "$workspaceRoot/lhs_coverage_review_20260930/deps;$workspaceRoot/gen2_network_reverify3_20261007/deps"
$env:OPENBLAS_NUM_THREADS = '1'
$env:OMP_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:TMP = "$reviewRoot/tmp/sv"
$env:TEMP = $env:TMP
New-Item -ItemType Directory -Path $env:TMP -Force | Out-Null
foreach ($probe in @('probe_rounding.py','probe_actual.py','probe_weighted.py','probe_deferred.py','run_resident_sm.py')) {
    & $python -X utf8 -B "$PSScriptRoot/$probe" *> "$PSScriptRoot/$($probe.Replace('.py','.rerun.log'))"
    if ($LASTEXITCODE -ne 0) { throw "$probe failed ($LASTEXITCODE)" }
    Write-Output "$probe passed"
}
& $python -X utf8 -B "$reviewRoot/repo/scripts/test_carbon_junction.py" --only QD2,QD3,QD4,QD5,QD6,QD7 *> "$PSScriptRoot/resident_qd.log"
if ($LASTEXITCODE -ne 0) { throw 'resident QD failed' }
Get-Content -LiteralPath "$PSScriptRoot/resident_qd.log" -Tail 1
& $python -X utf8 -B "$reviewRoot/repo/scripts/test_ca_ext_b6.py" --only S --skip-payload *> "$PSScriptRoot/resident_b6_s.log"
if ($LASTEXITCODE -ne 0) { throw 'resident B6 S failed (check missing historical fixtures separately)' }
Get-Content -LiteralPath "$PSScriptRoot/resident_b6_s.log" -Tail 1
