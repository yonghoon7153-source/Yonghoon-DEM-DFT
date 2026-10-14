# Reviewer-owned artifact packaging. No received code or test invocation.
$ErrorActionPreference = 'Stop'
$reviewRoot = [IO.Path]::GetFullPath($PSScriptRoot)
$priorRoot = Join-Path (Split-Path $reviewRoot -Parent) 'reil_c4_0b2_review_20261014'
$zipName = 'REIL_C4_0B2_FIX_RESULT_REVIEW_20261014.zip'
$zipPath = Join-Path $reviewRoot $zipName
$manifestPath = Join-Path $reviewRoot 'PACKAGE_MANIFEST.json'
$receiptPath = Join-Path $reviewRoot 'DELIVERY_RECEIPT.json'
foreach ($p in @($zipPath,$manifestPath,$receiptPath,(Join-Path $reviewRoot 'basis'))) {
    if (Test-Path -LiteralPath $p) { throw "Refuse overwrite: $p" }
}
function Save-NewJson($path,$value) {
    $text = ($value | ConvertTo-Json -Depth 40) + "`n"
    $bytes = [Text.UTF8Encoding]::new($false).GetBytes($text)
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($bytes,0,$bytes.Length) } finally { $stream.Dispose() }
}
function Digest-Bytes([byte[]]$bytes) {
    if ($null -eq $bytes) { $bytes = [byte[]]::new(0) }
    $sha = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-','').ToLowerInvariant() }
    finally { $sha.Dispose() }
}
$basis = Join-Path $reviewRoot 'basis'
$null = New-Item -ItemType Directory -Path $basis
$priorCopies = @(
    @{source='REVIEW_KO.md';dest='PRIOR_REVIEW_KO.md'},
    @{source='CLAUDE_REPLY_KO.md';dest='PRIOR_CLAUDE_REPLY_KO.md'},
    @{source='DECISION.json';dest='PRIOR_DECISION.json'},
    @{source='CENTER_COUNTEREXAMPLE.json';dest='CENTER_COUNTEREXAMPLE.json'},
    @{source='source/scripts/reil_c4_hb.py';dest='PRIOR_HB.py.txt'}
)
$basisIndex = @()
foreach ($item in $priorCopies) {
    $sourcePath = Join-Path $priorRoot $item.source
    $destPath = Join-Path $basis $item.dest
    [IO.File]::Copy($sourcePath,$destPath,$false)
    $sha = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ((Get-FileHash -LiteralPath $destPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $sha) { throw 'Prior basis copy mismatch' }
    $basisIndex += @{source=$sourcePath;capture=('basis/'+$item.dest);bytes=(Get-Item -LiteralPath $destPath).Length;sha256=$sha}
}
Save-NewJson (Join-Path $basis 'BASIS_INDEX.json') $basisIndex
$index = Get-Content -LiteralPath (Join-Path $reviewRoot 'CAPTURE_INDEX.json') -Raw | ConvertFrom-Json
foreach ($item in $index) {
    $bytes = [IO.File]::ReadAllBytes((Join-Path $reviewRoot $item.capture))
    $header = [Text.Encoding]::ASCII.GetBytes(('blob '+$bytes.Length+[char]0))
    $both = [byte[]]($header+$bytes)
    $sha = [Security.Cryptography.SHA1]::Create()
    try { $blob = ([BitConverter]::ToString($sha.ComputeHash($both))).Replace('-','').ToLowerInvariant() }
    finally { $sha.Dispose() }
    if ($blob -ne $item.git_blob -or (Digest-Bytes $bytes) -ne $item.sha256 -or $bytes.Length -ne $item.bytes) { throw "Captured bytes mismatch: $($item.capture)" }
}
$files = @(Get-ChildItem -LiteralPath $reviewRoot -Recurse -File | Sort-Object FullName)
$members = @()
$seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($f in $files) {
    $relative = $f.FullName.Substring($reviewRoot.Length+1).Replace('\','/')
    if (-not $seen.Add($relative)) { throw 'Case-insensitive duplicate path' }
    if (($f.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'Reparse point refused' }
    if ($relative -match '(^/|(^|/)\.\.(/|$)|:)') { throw 'Unsafe relative member path' }
    $members += [ordered]@{path=$relative;bytes=$f.Length;sha256=(Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
    if ($f.Extension -eq '.json') { $null = Get-Content -LiteralPath $f.FullName -Raw | ConvertFrom-Json }
}
Save-NewJson $manifestPath ([ordered]@{kind='REVIEW_PACKAGE_MANIFEST';members=$members;self_excluded=$true;scope='Independent limited review evidence, not executable authorization'})
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive = [IO.Compression.ZipFile]::Open($zipPath,[IO.Compression.ZipArchiveMode]::Create)
try {
    foreach ($m in $members) {
        $null = [IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive,(Join-Path $reviewRoot $m.path),$m.path,[IO.Compression.CompressionLevel]::Optimal)
    }
    $null = [IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive,$manifestPath,'PACKAGE_MANIFEST.json',[IO.Compression.CompressionLevel]::Optimal)
} finally { $archive.Dispose() }
$expected = @{}
foreach ($m in $members) { $expected[$m.path]=$m }
$expected['PACKAGE_MANIFEST.json']=@{path='PACKAGE_MANIFEST.json';bytes=(Get-Item -LiteralPath $manifestPath).Length;sha256=(Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash.ToLowerInvariant()}
$archive = [IO.Compression.ZipFile]::OpenRead($zipPath)
try {
    if ($archive.Entries.Count -ne $expected.Count) { throw 'ZIP entry count mismatch' }
    $seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    foreach ($e in $archive.Entries) {
        if (-not $seen.Add($e.FullName) -or -not $expected.ContainsKey($e.FullName)) { throw 'ZIP name mismatch' }
        $inputStream=$e.Open(); $buffer=[IO.MemoryStream]::new()
        try { $inputStream.CopyTo($buffer);$raw=$buffer.ToArray() } finally { $inputStream.Dispose();$buffer.Dispose() }
        $m=$expected[$e.FullName]
        if ($raw.Length -ne $m.bytes -or (Digest-Bytes $raw) -ne $m.sha256) { throw "ZIP bytes mismatch: $($e.FullName)" }
    }
} finally { $archive.Dispose() }
$decision = Get-Content -LiteralPath (Join-Path $reviewRoot 'DECISION.json') -Raw | ConvertFrom-Json
$receipt = [ordered]@{
    kind='REVIEW_DELIVERY_RECEIPT';recipient=$null
    decision=$decision.decision
    reviewed_ref=$decision.reviewed_head
    archive=@{file=$zipName;bytes=(Get-Item -LiteralPath $zipPath).Length;sha256=(Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash.ToLowerInvariant()}
    manifest=@{bytes=(Get-Item -LiteralPath $manifestPath).Length;sha256=(Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash.ToLowerInvariant()}
    payload_count=$members.Count;zip_entries=$expected.Count;capture_git_blob_matches=$index.Count;prior_basis_copies=$priorCopies.Count
    verification='Exact member set, sizes and decompressed SHA256 matched; CRC not separately recomputed.'
    received_code_or_test_execution=0;new_execution_approval=$false;external_delivery_performed=$false
}
Save-NewJson $receiptPath $receipt
$receipt | ConvertTo-Json -Depth 15
