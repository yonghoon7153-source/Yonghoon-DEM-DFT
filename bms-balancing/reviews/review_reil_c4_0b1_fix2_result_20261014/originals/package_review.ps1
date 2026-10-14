# Reviewer-owned packaging only. Never imports or invokes received code/tests.
$ErrorActionPreference = 'Stop'
$reviewRoot = [IO.Path]::GetFullPath($PSScriptRoot)
$zipName = 'REIL_C4_0B1_FIX2_RESULT_REVIEW_20261014.zip'
$zipPath = Join-Path $reviewRoot $zipName
$manifestPath = Join-Path $reviewRoot 'PACKAGE_MANIFEST.json'
$receiptPath = Join-Path $reviewRoot 'DELIVERY_RECEIPT.json'
foreach ($p in @($zipPath,$manifestPath,$receiptPath)) {
    if (Test-Path -LiteralPath $p) { throw "Refuse overwrite: $p" }
}
function Save-NewJson($path,$value) {
    $text = ($value | ConvertTo-Json -Depth 40) + "`n"
    $bytes = [Text.UTF8Encoding]::new($false).GetBytes($text)
    $stream = [IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($bytes,0,$bytes.Length) } finally { $stream.Dispose() }
}
function Digest-Bytes($bytes) {
    $sha = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-','').ToLowerInvariant() }
    finally { $sha.Dispose() }
}
$index = Get-Content -LiteralPath (Join-Path $reviewRoot 'CAPTURE_INDEX.json') -Raw | ConvertFrom-Json
foreach ($item in $index) {
    $bytes = [IO.File]::ReadAllBytes((Join-Path $reviewRoot $item.capture))
    $header = [Text.Encoding]::ASCII.GetBytes(('blob '+$bytes.Length+[char]0))
    $both = [byte[]]::new($header.Length+$bytes.Length)
    [Array]::Copy($header,0,$both,0,$header.Length)
    [Array]::Copy($bytes,0,$both,$header.Length,$bytes.Length)
    $sha = [Security.Cryptography.SHA1]::Create()
    try { $blob = ([BitConverter]::ToString($sha.ComputeHash($both))).Replace('-','').ToLowerInvariant() }
    finally { $sha.Dispose() }
    if ($blob -ne $item.git_blob) { throw "Captured Git blob mismatch: $($item.capture)" }
}
$files = @(Get-ChildItem -LiteralPath $reviewRoot -Recurse -File | Sort-Object FullName)
$members = @()
$seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($f in $files) {
    $relative = $f.FullName.Substring($reviewRoot.Length+1).Replace('\','/')
    if (-not $seen.Add($relative)) { throw 'Case-insensitive duplicate path' }
    if (($f.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'Reparse point refused' }
    $members += [ordered]@{path=$relative;bytes=$f.Length;sha256=(Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
    if ($f.Extension -eq '.json') { $null = Get-Content -LiteralPath $f.FullName -Raw | ConvertFrom-Json }
}
$manifest = [ordered]@{kind='REVIEW_PACKAGE_MANIFEST';members=$members;self_excluded=$true;scope='Review evidence, not executable authorization'}
Save-NewJson $manifestPath $manifest
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
$receipt = [ordered]@{
    kind='REVIEW_DELIVERY_RECEIPT';recipient=$null
    decision='C4_0B1_LIMITED_IMPLEMENTATION_CLOSED'
    reviewed_ref='5eeedb4beade319a040c2453e8b447673d425fd6'
    archive=@{file=$zipName;bytes=(Get-Item -LiteralPath $zipPath).Length;sha256=(Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash.ToLowerInvariant()}
    manifest=@{bytes=(Get-Item -LiteralPath $manifestPath).Length;sha256=(Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash.ToLowerInvariant()}
    payload_count=$members.Count;zip_entries=$expected.Count;capture_git_blob_matches=$index.Count
    verification='Exact member set, sizes and decompressed SHA256 matched; CRC not separately recomputed.'
    received_code_or_test_execution=0;new_execution_approval=$false;external_delivery_performed=$false
}
Save-NewJson $receiptPath $receipt
$receipt | ConvertTo-Json -Depth 15
