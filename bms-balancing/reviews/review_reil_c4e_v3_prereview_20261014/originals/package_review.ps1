# Reviewer-owned packaging; no received source is imported or executed.
$ErrorActionPreference='Stop'
$reviewRoot=[IO.Path]::GetFullPath($PSScriptRoot)
$zipName='REIL_C4E_V3_PREREVIEW_REPLY_20261014.zip'
$zipPath=Join-Path $reviewRoot $zipName
$manifestPath=Join-Path $reviewRoot 'PACKAGE_MANIFEST.json'
$receiptPath=Join-Path $reviewRoot 'DELIVERY_RECEIPT.json'
foreach($p in @($zipPath,$manifestPath,$receiptPath)){if(Test-Path -LiteralPath $p){throw "Refuse overwrite: $p"}}
function Digest([byte[]]$raw){
 $h=[Security.Cryptography.SHA256]::Create()
 try{return ([BitConverter]::ToString($h.ComputeHash($raw))).Replace('-','').ToLowerInvariant()}finally{$h.Dispose()}
}
function NewJson([string]$path,$obj){
 $raw=[Text.UTF8Encoding]::new($false).GetBytes(($obj|ConvertTo-Json -Depth 40)+"`n")
 $s=[IO.File]::Open($path,[IO.FileMode]::CreateNew)
 try{$s.Write($raw,0,$raw.Length)}finally{$s.Dispose()}
 $back=[IO.File]::ReadAllBytes($path)
 if((Digest $back) -ne (Digest $raw)){throw 'Record readback mismatch'}
}
$audit=Get-Content -LiteralPath (Join-Path $reviewRoot 'STATIC_AUDIT.json') -Raw|ConvertFrom-Json
foreach($r in $audit.source_index){
 $raw=[IO.File]::ReadAllBytes((Join-Path $reviewRoot $r.capture))
 if($raw.Length -ne $r.bytes -or (Digest $raw) -ne $r.sha256){throw 'Source changed after audit'}
}
foreach($r in $audit.attachments){
 $p=Join-Path 'C:/Users/Administrator/Downloads' $r.file
 if((Get-Item -LiteralPath $p).Length -ne $r.bytes -or (Get-FileHash -LiteralPath $p).Hash.ToLowerInvariant() -ne $r.sha256){throw 'Attachment changed after audit'}
}
$members=@();$seen=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach($f in (Get-ChildItem -LiteralPath $reviewRoot -Recurse -File|Sort-Object FullName)){
 $rel=$f.FullName.Substring($reviewRoot.Length+1).Replace('\','/')
 if($rel -match '^CAPTURE.*PAYLOADS\.json$'){continue}
 if(-not $seen.Add($rel) -or $rel -match '(^/|(^|/)\.\.(/|$)|:)' -or ($f.Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Unsafe member'}
 if($f.Extension -eq '.json'){$null=Get-Content -LiteralPath $f.FullName -Raw|ConvertFrom-Json}
 $members+=@{path=$rel;bytes=$f.Length;sha256=(Get-FileHash -LiteralPath $f.FullName).Hash.ToLowerInvariant()}
}
NewJson $manifestPath ([ordered]@{kind='V3_PREREVIEW_REPLY_MANIFEST';members=$members;self_excluded=$true;transport_base64_omitted=$true;scope='Document/source review, not execution authority'})
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive=[IO.Compression.ZipFile]::Open($zipPath,[IO.Compression.ZipArchiveMode]::Create)
try{
 foreach($m in $members){$null=[IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive,(Join-Path $reviewRoot $m.path),$m.path,[IO.Compression.CompressionLevel]::Optimal)}
 $null=[IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive,$manifestPath,'PACKAGE_MANIFEST.json',[IO.Compression.CompressionLevel]::Optimal)
}finally{$archive.Dispose()}
$expected=@{};foreach($m in $members){$expected[$m.path]=$m}
$expected['PACKAGE_MANIFEST.json']=@{bytes=(Get-Item -LiteralPath $manifestPath).Length;sha256=(Get-FileHash -LiteralPath $manifestPath).Hash.ToLowerInvariant()}
$archive=[IO.Compression.ZipFile]::OpenRead($zipPath)
try{
 if($archive.Entries.Count -ne $expected.Count){throw 'Archive count mismatch'}
 $seen=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
 foreach($entry in $archive.Entries){
  if(-not $seen.Add($entry.FullName) -or -not $expected.ContainsKey($entry.FullName)){throw 'Archive member set mismatch'}
  $s=$entry.Open();$ms=[IO.MemoryStream]::new()
  try{$s.CopyTo($ms);$raw=$ms.ToArray()}finally{$s.Dispose();$ms.Dispose()}
  $m=$expected[$entry.FullName]
  if($raw.Length -ne $m.bytes -or (Digest $raw) -ne $m.sha256){throw 'Archive decompressed payload mismatch'}
 }
}finally{$archive.Dispose()}
$decision=Get-Content -LiteralPath (Join-Path $reviewRoot 'DECISION.json') -Raw|ConvertFrom-Json
$receipt=[ordered]@{
 kind='V3_PREREVIEW_REPLY_DELIVERY_RECEIPT';recipient=$null;utc=[DateTime]::UtcNow.ToString('o')
 decision=$decision.decision;reviewed_head=$decision.reviewed_head
 archive=@{file=$zipName;bytes=(Get-Item -LiteralPath $zipPath).Length;sha256=(Get-FileHash -LiteralPath $zipPath).Hash.ToLowerInvariant()}
 manifest=@{bytes=(Get-Item -LiteralPath $manifestPath).Length;sha256=(Get-FileHash -LiteralPath $manifestPath).Hash.ToLowerInvariant()}
 payload_count=$members.Count;zip_entries=$expected.Count;source_count=$audit.source_count
 verification='Exact set, case-insensitive uniqueness, safe paths, member sizes and decompressed SHA256 matched; CRC not independently recomputed'
 attachment_originals_unchanged=$true;received_code_execution=0;tests=0;new_execution_approval=$false;external_delivery_performed=$false
 boundary='Archive complete readback/hash before this receipt creation; receipt itself separately reread, no source runtime or OS audit claim'
}
NewJson $receiptPath $receipt
$receipt|ConvertTo-Json -Depth 8
