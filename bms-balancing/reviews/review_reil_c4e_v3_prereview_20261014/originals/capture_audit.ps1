$ErrorActionPreference='Stop'
$reviewRoot=$PSScriptRoot
$priorRoot=Join-Path (Split-Path $reviewRoot -Parent) 'reil_c4e_v2_prereview_20261014'
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
function NewJson([string]$dest,$obj) {NewBytes $dest ([Text.UTF8Encoding]::new($false).GetBytes(($obj|ConvertTo-Json -Depth 30)+"`n"))}
function CheckBlob([byte[]]$raw,[string]$expected) {
 $header=[Text.Encoding]::ASCII.GetBytes('blob '+$raw.Length+[char]0)
 if((HashBytes ([byte[]]($header+$raw)) 'SHA1') -ne $expected){throw 'Git blob mismatch'}
}
$head=Get-Content -LiteralPath (Join-Path $reviewRoot 'HEAD.json') -Raw|ConvertFrom-Json
$compare=Get-Content -LiteralPath (Join-Path $reviewRoot 'COMPARE.json') -Raw|ConvertFrom-Json
if($compare.base -ne 'dc6e5b7e043ff11b73095ddb9d60db7837e665c7' -or $compare.head -ne $head.sha -or $compare.too_large -or $compare.behind_by -ne 0 -or $compare.total_commits -ne 4){throw 'Comparison binding'}
$index=@()
foreach($r in (Get-Content -LiteralPath (Join-Path $reviewRoot 'CAPTURE_PAYLOADS.json') -Raw|ConvertFrom-Json)) {
 $raw=[Convert]::FromBase64String($r.content)
 CheckBlob $raw $r.git_blob
 NewBytes (Join-Path $reviewRoot $r.capture) $raw
 $index+=@{capture=$r.capture;repo_path=$r.repo_path;ref=$r.ref;git_blob=$r.git_blob;bytes=$raw.Length;sha256=(HashBytes $raw);binding='Direct fixed-commit read'}
}
$oldAudit=Get-Content -LiteralPath (Join-Path $priorRoot 'STATIC_AUDIT.json') -Raw|ConvertFrom-Json
$changed=@($compare.files|ForEach-Object {$_.filename})
foreach($r in $oldAudit.source_index) {
 if($r.capture -in $index.capture){continue}
 if($r.repo_path -in $changed){throw 'Changed source reuse'}
 $raw=[IO.File]::ReadAllBytes((Join-Path $priorRoot $r.capture))
 CheckBlob $raw $r.git_blob
 if($raw.Length -ne $r.bytes -or (HashBytes $raw) -ne $r.sha256){throw 'Prior source mismatch'}
 NewBytes (Join-Path $reviewRoot $r.capture) $raw
 $index+=@{capture=$r.capture;repo_path=$r.repo_path;ref=$r.ref;git_blob=$r.git_blob;bytes=$r.bytes;sha256=$r.sha256;binding='Previously captured bytes; repository path unchanged in base-to-head comparison, except pinned external original util'}
}
foreach($name in @('REVIEW_KO.md','DECISION.json','STATIC_AUDIT.json','REQUEST_CORRECTIONS_KO.md')) {
 NewBytes (Join-Path $reviewRoot ('basis/V2_'+$name)) ([IO.File]::ReadAllBytes((Join-Path $priorRoot $name)))
}
$attachmentIds=@()
foreach($name in @('REIL_C4E_APPROVAL_REQUEST_v3_20261014.md','REIL_C4E_PREREVIEW_SEND_v3_20261014.md')) {
 $raw=[IO.File]::ReadAllBytes((Join-Path 'C:/Users/Administrator/Downloads' $name))
 $captured=$index|Where-Object {$_.capture -eq ('source/docs/'+$name)}
 if($raw.Length -ne $captured.bytes -or (HashBytes $raw) -ne $captured.sha256){throw 'Attachment mismatch'}
 $attachmentIds+=@{file=$name;bytes=$raw.Length;sha256=(HashBytes $raw);matches_fixed_commit=$true}
}
$monitor=Join-Path $reviewRoot 'source/scripts/reil_c4_monitor.py'
if((Get-FileHash -LiteralPath $monitor).Hash -ne (Get-FileHash -LiteralPath (Join-Path $priorRoot 'source/scripts/reil_c4_monitor.py')).Hash){throw 'Monitor changed'}
$request=Get-Content -LiteralPath (Join-Path $reviewRoot 'source/docs/REIL_C4E_APPROVAL_REQUEST_v3_20261014.md') -Raw
$ids=@([regex]::Matches($request,'(?m)^\| (m_[12]|r_[1-6]|t_1|d_[1-6]|s_[1-6]) \|')|ForEach-Object {$_.Groups[1].Value})
if($ids.Count -ne 21 -or @($ids|Sort-Object -Unique).Count -ne 21){throw 'Case ID count'}
$audit=[ordered]@{kind='STATIC_DOCUMENT_PREREVIEW_V3_AUDIT';utc=[DateTime]::UtcNow.ToString('o');reviewed_head=$head.sha;attachments=$attachmentIds;source_index=$index;source_count=$index.Count;direct_fixed_commit_sources=4;comparison=@{base=$compare.base;head=$compare.head;ahead=4;behind=0;changed_files=$compare.files.Count;complete_comparison=$true;production_and_seven_tests_changed=$false};new_test_ids=$ids;new_test_ids_count=21;existing_tests=159;GREEN_tests=180;counts=@{COBYQA_calls=14;internal_maxfev=50;independent_reevaluation_per_normal_return=1;real_old_fork=10;real_new_fork=5;GREEN_real_fork=15;GREEN_fork_cap=17;fake_minimize_max=995;Sobol_related_tests=15;preserved_util_test06=@{extract_max=5;objective_max=3;dVdQ_max=9};preserved_util_h1_h4=@{extract_max=4;objective_max=0;dVdQ_max=48};kind='Static counting units; not runtime observations'};budgets=@{E0_step_sum_s=(60+600+600+300);run_record_deadline_s=9900;runner_process_timeout_s=10800;time_origins_distinct=$true};monitor_current_matches_prior=$true;received_code_execution=0;tests=0;Python=0;optimizer=0;Sobol=0;raw_data_fetch_open=0;COMSOL=0;E0_approved=$false;E1_approved=$false}
NewJson (Join-Path $reviewRoot 'STATIC_AUDIT.json') $audit
[ordered]@{head=$head.sha;attachments=$attachmentIds;source_count=$index.Count;new_test_ids=$ids;monitor_unchanged=$true;received_code_execution=0}|ConvertTo-Json -Depth 10
