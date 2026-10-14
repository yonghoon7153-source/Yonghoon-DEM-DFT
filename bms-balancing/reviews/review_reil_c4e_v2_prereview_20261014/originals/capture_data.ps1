# Reviewer-owned data-only decoder; supplied programs are never loaded.
$ErrorActionPreference='Stop'
$reviewRoot=[IO.Path]::GetFullPath($PSScriptRoot)
$records=Get-Content -LiteralPath (Join-Path $reviewRoot 'CAPTURE_PAYLOADS.json') -Raw|ConvertFrom-Json
$index=@()
foreach($record in $records){
 $dest=[IO.Path]::GetFullPath((Join-Path $reviewRoot $record.capture))
 if(-not $dest.StartsWith($reviewRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase) -or (Test-Path -LiteralPath $dest)){throw 'Unsafe/existing capture'}
 $raw=[Convert]::FromBase64String($record.content)
 $head=[Text.Encoding]::ASCII.GetBytes('blob '+$raw.Length+[char]0)
 $sha=[Security.Cryptography.SHA1]::Create()
 try{$blob=([BitConverter]::ToString($sha.ComputeHash([byte[]]($head+$raw)))).Replace('-','').ToLowerInvariant()}finally{$sha.Dispose()}
 if($blob -ne $record.git_blob){throw 'Git blob mismatch'}
 [IO.Directory]::CreateDirectory((Split-Path $dest -Parent))|Out-Null
 $s=[IO.File]::Open($dest,[IO.FileMode]::CreateNew)
 try{$s.Write($raw,0,$raw.Length)}finally{$s.Dispose()}
 $index+=@{repo_path=$record.repo_path;capture=$record.capture;ref=$record.ref;git_blob=$blob;bytes=$raw.Length;sha256=(Get-FileHash -LiteralPath $dest -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$matches=@()
foreach($name in @('REIL_C4E_APPROVAL_REQUEST_v2_20261014.md','REIL_C4E_PREREVIEW_SEND_v2_20261014.md')){
 $local=Join-Path 'C:/Users/Administrator/Downloads' $name
 $hash=(Get-FileHash -LiteralPath $local -Algorithm SHA256).Hash.ToLowerInvariant()
 $same=$hash -eq (Get-FileHash -LiteralPath (Join-Path $reviewRoot ('source/docs/'+$name)) -Algorithm SHA256).Hash.ToLowerInvariant()
 if(-not $same){throw 'Attachment mismatch'}
 $matches+=@{attachment=$name;bytes=(Get-Item -LiteralPath $local).Length;sha256=$hash;matches_commit=$same}
}
$result=[ordered]@{reviewed_head='dc6e5b7e043ff11b73095ddb9d60db7837e665c7';sources=$index;attachments=$matches;received_code_execution=0}
$out=[Text.UTF8Encoding]::new($false).GetBytes(($result|ConvertTo-Json -Depth 8)+"`n")
$s=[IO.File]::Open((Join-Path $reviewRoot 'CAPTURE_INDEX.json'),[IO.FileMode]::CreateNew)
try{$s.Write($out,0,$out.Length)}finally{$s.Dispose()}
$result|ConvertTo-Json -Depth 8
