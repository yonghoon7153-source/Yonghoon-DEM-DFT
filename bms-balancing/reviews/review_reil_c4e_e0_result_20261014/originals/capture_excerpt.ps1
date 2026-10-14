$ErrorActionPreference='Stop'
$r=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'EXCERPT_PAYLOAD.json') -Raw|ConvertFrom-Json
$raw=[Convert]::FromBase64String($r.content)
$sha=[Security.Cryptography.SHA256]::Create()
$actual=([BitConverter]::ToString($sha.ComputeHash($raw))).Replace('-','').ToLowerInvariant()
$sha.Dispose()
if($actual -ne '95cca5f35aaaf72757812068251d72064b464cff6ef3f523c756f33d27d243a9' -or $raw.Length -ne 7543){throw 'Excerpt mismatch'}
$dest=Join-Path $PSScriptRoot $r.capture
$null=[IO.Directory]::CreateDirectory((Split-Path $dest -Parent))
$s=[IO.File]::Open($dest,[IO.FileMode]::CreateNew)
try {$s.Write($raw,0,$raw.Length)} finally {$s.Dispose()}
[ordered]@{path=$r.capture;bytes=$raw.Length;sha256=$actual;expected_match=$true;git_blob_reported=$r.git_blob}|ConvertTo-Json
