# Reviewer-owned read/hash/text-diff audit. No received code is imported or executed.
$ErrorActionPreference = 'Stop'
$reviewRoot = $PSScriptRoot
$priorRoot = Join-Path (Split-Path $reviewRoot -Parent) 'reil_c4_0b2_review_20261014'
$utf8 = [Text.UTF8Encoding]::new($false)
function Digest([byte[]]$bytes, $algorithm = 'SHA256') {
    if ($null -eq $bytes) { $bytes = [byte[]]::new(0) }
    $hash = [Security.Cryptography.HashAlgorithm]::Create($algorithm)
    try { return ([BitConverter]::ToString($hash.ComputeHash($bytes))).Replace('-','').ToLowerInvariant() } finally { $hash.Dispose() }
}
function Blob([byte[]]$bytes) {
    $header = [Text.Encoding]::ASCII.GetBytes(('blob '+$bytes.Length+[char]0))
    return Digest ([byte[]]($header+$bytes)) 'SHA1'
}
function Read-Bytes($relative) { return ,([IO.File]::ReadAllBytes((Join-Path $reviewRoot $relative))) }
function Check($condition,$message) { if (-not $condition) { throw $message } }
$checks = [Collections.Generic.List[object]]::new()
$index = Get-Content -LiteralPath (Join-Path $reviewRoot 'CAPTURE_INDEX.json') -Raw | ConvertFrom-Json
foreach ($item in $index) {
    $bytes = Read-Bytes $item.capture
    Check ($bytes.Length -eq $item.bytes -and (Digest $bytes) -eq $item.sha256 -and (Blob $bytes) -eq $item.git_blob) "Capture mismatch: $($item.capture)"
}
$checks.Add(@{check='48 captures size SHA256 Git blob';count=$index.Count;matched=$true})
$prereg = Get-Content -LiteralPath (Join-Path $reviewRoot 'PREREGISTRATION_RAW.json') -Raw | ConvertFrom-Json
$priorHb = $null
foreach ($item in $prereg) {
    $raw = $utf8.GetBytes($item.content)
    Check ((Blob $raw) -eq $item.git_blob) "Preregistration blob mismatch: $($item.repo_path)"
    $local = 'source/'+$item.repo_path.Substring('bms-balancing/'.Length)
    if ($item.repo_path -eq 'bms-balancing/scripts/reil_c4_hb.py') {
        $priorHb = $raw
        $priorRaw = [IO.File]::ReadAllBytes((Join-Path $priorRoot $local))
        Check ((Digest $priorRaw) -eq (Digest $raw)) 'Pre-patch differs from prior reviewed source'
    } else { Check ((Digest (Read-Bytes $local)) -eq (Digest $raw)) 'Preregistered document changed' }
    $checks.Add(@{check='approval-commit fixed bytes';path=$item.repo_path;ref=$item.ref;git_blob=$item.git_blob;sha256=(Digest $raw);matched=$true})
}
$draft = Read-Bytes 'source/docs/REIL_C4_0B2_FIX_CONTROLS_DRAFT_20261014.py.txt'
Check ((Digest $draft) -eq (Digest (Read-Bytes 'source/tests/test_reil_c4_0b2_fix.py'))) 'Test differs from preregistered draft'
$checks.Add(@{check='new five-test file equals preregistered draft';sha256=(Digest $draft);matched=$true})

# Apply the unified diff solely as data in memory, not to any source on disk.
$old = $utf8.GetString($priorHb).Split([char]10)
$diff = [IO.File]::ReadAllLines((Join-Path $reviewRoot 'source/docs/REIL_C4_0B2_FIX_PATCH_DRAFT_20261014.diff'))
$outLines = [Collections.Generic.List[string]]::new()
$pos = 0; $j = 0; $hunks = 0; $added = 0; $removed = 0
while ($j -lt $diff.Length) {
    if ($diff[$j] -notmatch '^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@') { $j++; continue }
    $start = [int]$Matches[1]-1
    $oldCount = if ($Matches[2]) { [int]$Matches[2] } else { 1 }
    $newCount = if ($Matches[4]) { [int]$Matches[4] } else { 1 }
    while ($pos -lt $start) { $outLines.Add($old[$pos]); $pos++ }
    Check ($pos -eq $start) 'Patch old start mismatch'
    $consumed = 0; $emitted = 0; $j++; $hunks++
    while ($j -lt $diff.Length -and $diff[$j] -notmatch '^@@ ') {
        $line = $diff[$j]
        if ($line.StartsWith(' ')) {
            Check ($old[$pos] -ceq $line.Substring(1)) 'Patch context mismatch'
            $outLines.Add($old[$pos]); $pos++; $consumed++; $emitted++
        } elseif ($line.StartsWith('-')) {
            Check ($old[$pos] -ceq $line.Substring(1)) 'Patch removed text mismatch'
            $pos++; $consumed++; $removed++
        } elseif ($line.StartsWith('+')) {
            $outLines.Add($line.Substring(1)); $emitted++; $added++
        } else { throw 'Unexpected diff data' }
        $j++
    }
    Check ($consumed -eq $oldCount -and $emitted -eq $newCount) 'Patch hunk counts mismatch'
}
while ($pos -lt $old.Length) { $outLines.Add($old[$pos]); $pos++ }
$post = $utf8.GetBytes([string]::Join("`n",$outLines))
Check ((Digest $post) -eq (Digest (Read-Bytes 'source/scripts/reil_c4_hb.py'))) 'Patched data differs from submitted source'
Check ($hunks -eq 9 -and $added -eq 110 -and $removed -eq 34) 'Patch count mismatch'
$checks.Add(@{check='in-memory patch exact post bytes';hunks=$hunks;added=$added;removed=$removed;before_sha256=(Digest $priorHb);after_sha256=(Digest $post);matched=$true})

$evidence = 'source/evidence/reil_c4_0b2_fix_20261014/'
$listAudit = @()
foreach ($list in @('02_red.source_sha256.txt','03_green.source_sha256.txt','04_source_sha256_end.txt')) {
    $rows = [IO.File]::ReadAllLines((Join-Path $reviewRoot ($evidence+$list)))
    $n = 0
    foreach ($line in $rows) {
        if (-not $line) { continue }
        Check ($line -match '^([0-9a-f]{64})  (.+)$') 'SHA list format'
        $expected = $Matches[1]; $path = $Matches[2]
        $raw = if ($list -eq '02_red.source_sha256.txt' -and $path -eq 'scripts/reil_c4_hb.py') { $priorHb } else { Read-Bytes ('source/'+$path) }
        Check ((Digest $raw) -eq $expected) "Source binding mismatch: $list $path"
        $n++
    }
    Check ($n -eq 12) 'Expected twelve source entries'
    $listAudit += @{file=$list;count=$n;matched=$true}
}
Check ((Digest (Read-Bytes ($evidence+'03_green.source_sha256.txt'))) -eq (Digest (Read-Bytes ($evidence+'04_source_sha256_end.txt')))) 'GREEN-end list mismatch'
$checks.Add(@{check='RED/GREEN/end source SHA binding';lists=$listAudit;green_end_lists_byte_equal=$true})
$unchanged = @()
foreach ($item in $index) {
    if ($item.capture -notmatch '^source/(scripts|tests)/' -or $item.capture -match '/(reil_c4_hb.py|test_reil_c4_0b2_fix.py)$') { continue }
    $oldPath = Join-Path $priorRoot $item.capture
    Check (Test-Path -LiteralPath $oldPath) "Missing prior source: $oldPath"
    Check ((Digest ([IO.File]::ReadAllBytes($oldPath))) -eq $item.sha256) "Prior source changed: $oldPath"
    $unchanged += $item.capture
}
$checks.Add(@{check='unchanged prior source and test bytes';count=$unchanged.Count;files=$unchanged;matched=$true})
$attachment = 'C:/Users/Administrator/Downloads/REIL_C4_0B2_FIX_RESULT_REVIEW_SEND_20261014.md'
Check ((Digest ([IO.File]::ReadAllBytes($attachment))) -eq (Digest (Read-Bytes 'source/docs/REIL_C4_0B2_FIX_RESULT_REVIEW_SEND_20261014.md'))) 'User attachment differs from fixed send document'
$checks.Add(@{check='attachment matches fixed repository send document';sha256=(Digest ([IO.File]::ReadAllBytes($attachment)));matched=$true})
$red = $utf8.GetString((Read-Bytes ($evidence+'02_red.stdout.log')))
$green = $utf8.GetString((Read-Bytes ($evidence+'03_green.stdout.log')))
Check ($red -match '5 failed' -and ([regex]::Matches($red,'(?m)^FAILED ')).Count -eq 5) 'RED summary mismatch'
Check ($green -match '119 passed in 26.05s') 'GREEN summary mismatch'
$steps = @()
foreach ($name in @('01_identity','02_red','03_green')) {
    $meta = Get-Content -LiteralPath (Join-Path $reviewRoot ($evidence+$name+'.meta.json')) -Raw | ConvertFrom-Json
    Check ($meta.head_start -eq 'a0604c2e62b8bfc5772c4d647c1c6668e9889ddc' -and $meta.head_end -eq $meta.head_start) 'Step HEAD mismatch'
    Check (-not $meta.timed_out -and $meta.elapsed_s -le $meta.timeout_s) 'Step time mismatch'
    Check ((Read-Bytes ($evidence+$name+'.stderr.log')).Length -eq 0) 'Unexpected stderr bytes'
    $steps += @{name=$name;head=$meta.head_start;rc=$meta.rc;elapsed_s=$meta.elapsed_s;limit_s=$meta.timeout_s;max_child_rss_kib=$meta.child_maxrss_kib}
}
$end = Get-Content -LiteralPath (Join-Path $reviewRoot ($evidence+'05_end.json')) -Raw | ConvertFrom-Json
$evFiles = @(Get-ChildItem -LiteralPath (Join-Path $reviewRoot $evidence) -File)
$evBytes = ($evFiles | Measure-Object Length -Sum).Sum
Check ($evFiles.Count -eq 25 -and $evBytes - (Read-Bytes ($evidence+'05_end.json')).Length -eq $end.resources_post_hoc.evidence_bytes) 'Evidence size boundary mismatch'
$checks.Add(@{check='recorded steps and summaries';steps=$steps;elapsed_sum_s=($steps | Measure-Object elapsed_s -Sum).Sum;red_failed=5;green_passed=119;evidence_files=25;current_evidence_bytes=$evBytes;before_end_record_bytes=$end.resources_post_hoc.evidence_bytes;observed_captured_pass_sections=@('test_10_the_cli_requires_explicit_paths','test_d_2_the_phase_b_dry_run_refuses_bad_arrays_data_paths_and_an_existing_output');scope='Recorded executions only; not reviewer reruns'})
$compare = Get-Content -LiteralPath (Join-Path $reviewRoot 'COMPARE_FROM_PRIOR.json') -Raw | ConvertFrom-Json
$codeChanges = @($compare.files | Where-Object { $_.filename -match '^bms-balancing/scripts/' } | ForEach-Object filename)
Check ($codeChanges.Count -eq 1 -and $codeChanges[0] -eq 'bms-balancing/scripts/reil_c4_hb.py') 'Unexpected production source change'
$checks.Add(@{check='compare scope';base=$compare.base;head=$compare.head;ahead_by=$compare.ahead_by;behind_by=$compare.behind_by;changed_files=$compare.files.Count;production_changes=$codeChanges;too_large=$compare.too_large})
$result = [ordered]@{kind='REVIEWER_STATIC_DATA_AUDIT';status='MATCH';reviewed_head=$compare.head;checks=$checks;received_program_execution=0;test_execution=0;data_opening=0;network_mutation=0;limitations=@('Hash binding is not independent OS execution authentication.','Recorded post-hoc RSS is not simultaneous aggregate or enforced memory limit.','125.5-second snapshot precedes commit/push/report; no whole-work duration certification.')}
$outPath = Join-Path $reviewRoot 'STATIC_AUDIT.json'
Check (-not (Test-Path -LiteralPath $outPath)) 'Refuse audit overwrite'
$data = $utf8.GetBytes(($result | ConvertTo-Json -Depth 30)+"`n")
$stream = [IO.File]::Open($outPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try { $stream.Write($data,0,$data.Length) } finally { $stream.Dispose() }
[ordered]@{status='MATCH';captured=$index.Count;preregistered=$prereg.Count;patch_hunks=$hunks;sha_list_entries=36;unchanged_prior_sources=$unchanged.Count;red=5;green=119;output_bytes=$data.Length} | ConvertTo-Json
