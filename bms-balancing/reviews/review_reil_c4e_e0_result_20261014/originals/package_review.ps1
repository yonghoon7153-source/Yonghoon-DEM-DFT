$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$reviewRoot=$PSScriptRoot
$zipName='REIL_C4E_E0_REVIEW_REPLY_20261014.zip'
$zipPath=Join-Path $reviewRoot $zipName
function HashBytes([byte[]]$raw) {
 $h=[Security.Cryptography.SHA256]::Create()
 try {([BitConverter]::ToString($h.ComputeHash($raw))).Replace('-','').ToLowerInvariant()} finally {$h.Dispose()}
}
function WriteNewJson([string]$path,$obj) {
 $raw=[Text.UTF8Encoding]::new($false).GetBytes(($obj|ConvertTo-Json -Depth 30)+"`n")
 $s=[IO.File]::Open($path,[IO.FileMode]::CreateNew)
 try {$s.Write($raw,0,$raw.Length)} finally {$s.Dispose()}
}
$exclude=@('CAPTURE_PAYLOADS.json','HISTORICAL_PAYLOADS.json','EXCERPT_PAYLOAD.json','PACKAGE_MANIFEST.json','DELIVERY_RECEIPT.json',$zipName)
$members=@()
foreach($f in (Get-ChildItem -LiteralPath $reviewRoot -File -Recurse|Sort-Object FullName)) {
 $rel=$f.FullName.Substring($reviewRoot.Length+1).Replace('\','/')
 if($rel -in $exclude){continue}
 if($f.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Link member'}
 $members+=@{path=$rel;bytes=$f.Length;sha256=(Get-FileHash -LiteralPath $f.FullName).Hash.ToLowerInvariant()}
}
WriteNewJson (Join-Path $reviewRoot 'PACKAGE_MANIFEST.json') ([ordered]@{kind='REVIEW_PACKAGE_MANIFEST';reviewed_head='5cb6ab95c8c461cf940dcf94b90c30e8a3e3659c';payload_count=$members.Count;members=$members;excluded_transport_encodings=$exclude[0..2];source_execution=0})
$zf=[IO.File]::Open($zipPath,[IO.FileMode]::CreateNew)
$zip=[IO.Compression.ZipArchive]::new($zf,[IO.Compression.ZipArchiveMode]::Create,$false)
try {
 foreach($r in @($members)+@(@{path='PACKAGE_MANIFEST.json'})) {
  $entry=$zip.CreateEntry($r.path,[IO.Compression.CompressionLevel]::Optimal)
  $dest=$entry.Open();$src=[IO.File]::OpenRead((Join-Path $reviewRoot $r.path))
  try {$src.CopyTo($dest)} finally {$src.Dispose();$dest.Dispose()}
 }
} finally {$zip.Dispose();$zf.Dispose()}
$zip=[IO.Compression.ZipFile]::OpenRead($zipPath)
try {
 $expected=@($members.path)+@('PACKAGE_MANIFEST.json')
 if($zip.Entries.Count -ne $expected.Count){throw 'Entry count'}
 $seen=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
 foreach($entry in $zip.Entries) {
  if(-not $seen.Add($entry.FullName) -or $entry.FullName -notin $expected -or $entry.FullName.Contains('..') -or $entry.FullName.StartsWith('/')){throw 'Unsafe or unexpected entry'}
  $s=$entry.Open();$mem=[IO.MemoryStream]::new()
  try {$s.CopyTo($mem);$bytes=$mem.ToArray()} finally {$s.Dispose();$mem.Dispose()}
  $original=[IO.File]::ReadAllBytes((Join-Path $reviewRoot $entry.FullName))
  if($bytes.Length -ne $original.Length -or (HashBytes $bytes) -ne (HashBytes $original)){throw 'Readback mismatch'}
 }
} finally {$zip.Dispose()}
$receipt=[ordered]@{kind='REIL_C4E_E0_REVIEW_DELIVERY';recipient=$null;archive=@{path=$zipPath;bytes=(Get-Item -LiteralPath $zipPath).Length;sha256=(Get-FileHash -LiteralPath $zipPath).Hash.ToLowerInvariant()};payload_count=$members.Count;entries=$members.Count+1;manifest_sha256=(Get-FileHash -LiteralPath (Join-Path $reviewRoot 'PACKAGE_MANIFEST.json')).Hash.ToLowerInvariant();verification='Exact entry set, case-insensitive uniqueness, safe paths, decompressed lengths and SHA256 match. CRC not separately recomputed.';decision='E0_EVIDENCE_LIMITED_ACCEPTANCE_E1_BLOCKED_SOURCE_IDENTITY';received_code_execution=0;E1_execution_approval=$false;remote_changes=0;utc=[DateTime]::UtcNow.ToString('o');observation_boundary='After ZIP readback; before receipt write and tool return'}
WriteNewJson (Join-Path $reviewRoot 'DELIVERY_RECEIPT.json') $receipt
$receipt|ConvertTo-Json -Depth 8
