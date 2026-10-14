$ErrorActionPreference='Stop'
$reviewRoot=$PSScriptRoot
$priorRoot=Join-Path (Split-Path $reviewRoot -Parent) 'reil_c4e_v3_prereview_20261014'
function HashBytes([byte[]]$raw,[string]$kind='SHA256') {
 $h=[Security.Cryptography.HashAlgorithm]::Create($kind)
 try { ([BitConverter]::ToString($h.ComputeHash($raw))).Replace('-','').ToLowerInvariant() } finally {$h.Dispose()}
}
function NewBytes([string]$dest,[byte[]]$raw) {
 $full=[IO.Path]::GetFullPath($dest)
 if(-not $full.StartsWith($reviewRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Outside review folder'}
 $null=[IO.Directory]::CreateDirectory((Split-Path $full -Parent))
 $s=[IO.File]::Open($full,[IO.FileMode]::CreateNew)
 try {$s.Write($raw,0,$raw.Length)} finally {$s.Dispose()}
}
function CheckBlob([byte[]]$raw,[string]$expected) {
 $header=[Text.Encoding]::ASCII.GetBytes('blob '+$raw.Length+[char]0)
 if((HashBytes ([byte[]]($header+$raw)) 'SHA1') -ne $expected){throw 'Git blob mismatch'}
}
$head=Get-Content -LiteralPath (Join-Path $reviewRoot 'HEAD.json') -Raw|ConvertFrom-Json
$compare=Get-Content -LiteralPath (Join-Path $reviewRoot 'COMPARE.json') -Raw|ConvertFrom-Json
if($compare.base -ne '05614f07abc559a12254db41ce7301574ddc6f50' -or $compare.head -ne $head.sha -or $compare.behind_by -ne 0 -or $compare.total_commits -ne 10){throw 'Comparison binding'}
$index=@()
foreach($r in (Get-Content -LiteralPath (Join-Path $reviewRoot 'CAPTURE_PAYLOADS.json') -Raw|ConvertFrom-Json)) {
 $raw=[Convert]::FromBase64String($r.content)
 CheckBlob $raw $r.git_blob
 NewBytes (Join-Path $reviewRoot $r.capture) $raw
 $index+=@{capture=$r.capture;repo_path=$r.repo_path;ref=$r.ref;git_blob=$r.git_blob;bytes=$raw.Length;sha256=(HashBytes $raw);binding='Direct fixed-commit read'}
}
$directCount=$index.Count
$oldAudit=Get-Content -LiteralPath (Join-Path $priorRoot 'STATIC_AUDIT.json') -Raw|ConvertFrom-Json
$changed=@($compare.files|ForEach-Object {$_.filename})
foreach($r in $oldAudit.source_index) {
 if($r.capture -in $index.capture){continue}
 if($r.repo_path -in $changed){throw 'Changed source reuse'}
 $raw=[IO.File]::ReadAllBytes((Join-Path $priorRoot $r.capture))
 CheckBlob $raw $r.git_blob
 if($raw.Length -ne $r.bytes -or (HashBytes $raw) -ne $r.sha256){throw 'Prior source mismatch'}
 NewBytes (Join-Path $reviewRoot $r.capture) $raw
 $index+=@{capture=$r.capture;repo_path=$r.repo_path;ref=$r.ref;git_blob=$r.git_blob;bytes=$r.bytes;sha256=$r.sha256;binding='Prior bytes; repository path unchanged in base-to-head comparison; pinned external util unchanged source'}
}
foreach($name in @('REVIEW_KO.md','DECISION.json','STATIC_AUDIT.json')) {
 NewBytes (Join-Path $reviewRoot ('basis/V3_'+$name)) ([IO.File]::ReadAllBytes((Join-Path $priorRoot $name)))
}
$attachment='REIL_C4E_E0_RESULT_REVIEW_SEND_20261014.md'
$raw=[IO.File]::ReadAllBytes((Join-Path 'C:/Users/Administrator/Downloads' $attachment))
$expected=$index|Where-Object {$_.capture -eq ('source/docs/'+$attachment)}
if($raw.Length -ne $expected.bytes -or (HashBytes $raw) -ne $expected.sha256){throw 'Attachment mismatch'}
$audit=[ordered]@{kind='E0_RESULT_READONLY_CAPTURE';utc=[DateTime]::UtcNow.ToString('o');reviewed_head=$head.sha;attachment=@{name=$attachment;bytes=$raw.Length;sha256=(HashBytes $raw);matches_fixed_commit=$true};source_index=$index;source_count=$index.Count;direct_count=$directCount;comparison=@{base=$compare.base;head=$compare.head;commits=10;files=$compare.files.Count};received_code_execution=0;tests=0;optimizer=0;raw_data_fetch_open=0;COMSOL=0}
NewBytes (Join-Path $reviewRoot 'SOURCE_AUDIT.json') ([Text.UTF8Encoding]::new($false).GetBytes(($audit|ConvertTo-Json -Depth 30)+"`n"))
[ordered]@{head=$head.sha;attachment=$audit.attachment;sources=$index.Count;direct=$directCount;received_code_execution=0}|ConvertTo-Json -Depth 10
