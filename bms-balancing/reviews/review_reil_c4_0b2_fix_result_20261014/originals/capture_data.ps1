# Own read-only repository capture serializer; never invokes received code.
$ErrorActionPreference='Stop'
$taskRoot=[IO.Path]::GetFullPath($PSScriptRoot)
$records=Get-Content -LiteralPath (Join-Path $taskRoot 'CAPTURE_PAYLOADS.json') -Raw | ConvertFrom-Json
$index=@()
foreach($record in $records){
  $dest=[IO.Path]::GetFullPath((Join-Path $taskRoot $record.capture))
  if(-not $dest.StartsWith($taskRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Unsafe capture path'}
  if(Test-Path -LiteralPath $dest){throw 'Refuse overwrite'}
  $raw=[Text.UTF8Encoding]::new($false).GetBytes($record.content)
  $prefix=[Text.Encoding]::ASCII.GetBytes('blob '+$raw.Length+[char]0)
  $blob=[byte[]]::new($prefix.Length+$raw.Length)
  [Array]::Copy($prefix,0,$blob,0,$prefix.Length);[Array]::Copy($raw,0,$blob,$prefix.Length,$raw.Length)
  $sha=[Security.Cryptography.SHA1]::Create()
  try{$digest=([BitConverter]::ToString($sha.ComputeHash($blob))).Replace('-','').ToLowerInvariant()}finally{$sha.Dispose()}
  if($digest -ne $record.git_blob){throw "Git blob mismatch: $($record.repo_path)"}
  [IO.Directory]::CreateDirectory((Split-Path $dest -Parent))|Out-Null
  $stream=[IO.File]::Open($dest,[IO.FileMode]::CreateNew)
  try{$stream.Write($raw,0,$raw.Length)}finally{$stream.Dispose()}
  $index += [ordered]@{repo_path=$record.repo_path;capture=$record.capture;git_blob=$digest;ref=$record.ref;bytes=$raw.Length;sha256=(Get-FileHash -LiteralPath $dest -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$out=[Text.UTF8Encoding]::new($false).GetBytes(($index|ConvertTo-Json -Depth 8)+"`n")
$stream=[IO.File]::Open((Join-Path $taskRoot 'CAPTURE_INDEX.json'),[IO.FileMode]::CreateNew)
try{$stream.Write($out,0,$out.Length)}finally{$stream.Dispose()}
[ordered]@{captured=$index.Count;git_blob_matches=$index.Count;received_code_execution=0}|ConvertTo-Json
