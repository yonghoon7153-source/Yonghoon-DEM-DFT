# Reviewer-owned handoff packaging only. Does not run received programs.
$ErrorActionPreference='Stop'
$reviewRoot=[IO.Path]::GetFullPath($PSScriptRoot)
$zipName='REIL_C4E_PREREVIEW_REPLY_20261014.zip'
$zipPath=Join-Path $reviewRoot $zipName
$manifestPath=Join-Path $reviewRoot 'PACKAGE_MANIFEST.json'
$receiptPath=Join-Path $reviewRoot 'DELIVERY_RECEIPT.json'
foreach($path in @($zipPath,$manifestPath,$receiptPath,(Join-Path $reviewRoot 'basis'))){if(Test-Path -LiteralPath $path){throw "Refuse overwrite: $path"}}
function Digest([byte[]]$raw){
 $h=[Security.Cryptography.SHA256]::Create()
 try{return ([BitConverter]::ToString($h.ComputeHash($raw))).Replace('-','').ToLowerInvariant()}finally{$h.Dispose()}
}
function NewJson($path,$data){
 $raw=[Text.UTF8Encoding]::new($false).GetBytes(($data|ConvertTo-Json -Depth 40)+"`n")
 $s=[IO.File]::Open($path,[IO.FileMode]::CreateNew)
 try{$s.Write($raw,0,$raw.Length)}finally{$s.Dispose()}
}
$priorRoot=Join-Path (Split-Path $reviewRoot -Parent) 'reil_c4_0b2_fix_review_20261014'
$basis=Join-Path $reviewRoot 'basis'
$null=New-Item -ItemType Directory -Path $basis
foreach($name in @('REVIEW_KO.md','DECISION.json')){
 $src=Join-Path $priorRoot $name; $dest=Join-Path $basis ('PRIOR_C4_0B2_FIX_'+$name)
 [IO.File]::Copy($src,$dest,$false)
 if((Get-FileHash -LiteralPath $src).Hash -ne (Get-FileHash -LiteralPath $dest).Hash){throw 'Prior basis mismatch'}
}
$audit=Get-Content -LiteralPath (Join-Path $reviewRoot 'STATIC_AUDIT.json') -Raw|ConvertFrom-Json
foreach($item in $audit.source_index){
 $raw=[IO.File]::ReadAllBytes((Join-Path $reviewRoot $item.capture))
 if($raw.Length -ne $item.bytes -or (Digest $raw) -ne $item.sha256){throw 'Captured source changed after audit'}
}
$members=@(); $seen=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach($file in (Get-ChildItem -LiteralPath $reviewRoot -Recurse -File|Sort-Object FullName)){
 $relative=$file.FullName.Substring($reviewRoot.Length+1).Replace('\','/')
 if($relative -match '^CAPTURE_.*PAYLOADS\.json$'){continue}
 if(-not $seen.Add($relative) -or $relative -match '(^/|(^|/)\.\.(/|$)|:)' -or ($file.Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Unsafe/duplicate member'}
 if($file.Extension -eq '.json'){$null=Get-Content -LiteralPath $file.FullName -Raw|ConvertFrom-Json}
 $members+=@{path=$relative;bytes=$file.Length;sha256=(Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
NewJson $manifestPath ([ordered]@{kind='PREREVIEW_REPLY_MANIFEST';members=$members;self_excluded=$true;capture_payload_transport_files_omitted=$true;scope='Review only; no execution authority'})
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip=[IO.Compression.ZipFile]::Open($zipPath,[IO.Compression.ZipArchiveMode]::Create)
try{
 foreach($m in $members){$null=[IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip,(Join-Path $reviewRoot $m.path),$m.path,[IO.Compression.CompressionLevel]::Optimal)}
 $null=[IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip,$manifestPath,'PACKAGE_MANIFEST.json',[IO.Compression.CompressionLevel]::Optimal)
}finally{$zip.Dispose()}
$expected=@{};foreach($m in $members){$expected[$m.path]=$m}
$expected['PACKAGE_MANIFEST.json']=@{bytes=(Get-Item -LiteralPath $manifestPath).Length;sha256=(Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash.ToLowerInvariant()}
$zip=[IO.Compression.ZipFile]::OpenRead($zipPath)
try{
 if($zip.Entries.Count -ne $expected.Count){throw 'ZIP count mismatch'}
 $seen=[Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
 foreach($entry in $zip.Entries){
  if(-not $seen.Add($entry.FullName) -or -not $expected.ContainsKey($entry.FullName)){throw 'ZIP path mismatch'}
  $stream=$entry.Open();$memory=[IO.MemoryStream]::new()
  try{$stream.CopyTo($memory);$raw=$memory.ToArray()}finally{$stream.Dispose();$memory.Dispose()}
  $m=$expected[$entry.FullName]
  if($raw.Length -ne $m.bytes -or (Digest $raw) -ne $m.sha256){throw 'ZIP payload mismatch'}
 }
}finally{$zip.Dispose()}
$decision=Get-Content -LiteralPath (Join-Path $reviewRoot 'DECISION.json') -Raw|ConvertFrom-Json
$receipt=[ordered]@{
 kind='PREREVIEW_REPLY_DELIVERY_RECEIPT';recipient=$null;utc=[DateTime]::UtcNow.ToString('o')
 decision=$decision.decision;reviewed_head=$decision.reviewed_head
 archive=@{file=$zipName;bytes=(Get-Item -LiteralPath $zipPath).Length;sha256=(Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash.ToLowerInvariant()}
 manifest=@{bytes=(Get-Item -LiteralPath $manifestPath).Length;sha256=(Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash.ToLowerInvariant()}
 payload_count=$members.Count;zip_entries=$expected.Count;source_git_blob_matches=$audit.captured_git_blob_matches
 verification='Exact member set, uncompressed sizes and decompressed SHA256 matched; CRC not independently recomputed'
 received_code_execution=0;tests=0;new_execution_approval=$false;external_delivery_performed=$false
 boundary='ZIP close and complete readback/hash precede receipt creation; no runtime/OS audit claim'
}
NewJson $receiptPath $receipt
$receipt|ConvertTo-Json -Depth 10
