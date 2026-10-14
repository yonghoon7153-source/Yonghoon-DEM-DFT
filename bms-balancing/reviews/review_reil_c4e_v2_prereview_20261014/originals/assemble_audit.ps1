# Reviewer-owned evidence copying, hashing, and constant arithmetic only.
# Received source is read as bytes/text and is never imported or executed.
$ErrorActionPreference='Stop'
$reviewRoot=[IO.Path]::GetFullPath($PSScriptRoot)
$priorRoot=Join-Path (Split-Path $reviewRoot -Parent) 'reil_c4e_prereview_20261014'
function HashBytes([byte[]]$raw,[string]$kind='SHA256'){
 $h=[Security.Cryptography.HashAlgorithm]::Create($kind)
 try{return ([BitConverter]::ToString($h.ComputeHash($raw))).Replace('-','').ToLowerInvariant()}finally{$h.Dispose()}
}
function NewBytes([string]$dest,[byte[]]$raw){
 $full=[IO.Path]::GetFullPath($dest)
 if(-not $full.StartsWith($reviewRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Outside review folder'}
 $null=[IO.Directory]::CreateDirectory((Split-Path $full -Parent))
 $s=[IO.File]::Open($full,[IO.FileMode]::CreateNew)
 try{$s.Write($raw,0,$raw.Length)}finally{$s.Dispose()}
}
function NewJson([string]$dest,$obj){NewBytes $dest ([Text.UTF8Encoding]::new($false).GetBytes(($obj|ConvertTo-Json -Depth 30)+"`n"))}
function CheckBlob([byte[]]$raw,[string]$expected){
 $header=[Text.Encoding]::ASCII.GetBytes('blob '+$raw.Length+[char]0)
 if((HashBytes ([byte[]]($header+$raw)) 'SHA1') -ne $expected){throw 'Git blob mismatch'}
}
$current=Get-Content -LiteralPath (Join-Path $reviewRoot 'CAPTURE_INDEX.json') -Raw|ConvertFrom-Json
$compare=Get-Content -LiteralPath (Join-Path $reviewRoot 'COMPARE.json') -Raw|ConvertFrom-Json
if($compare.base -ne '89d18f546cef0172ee53105ae04ba66d1e224370' -or $compare.head -ne $current.reviewed_head -or $compare.too_large -or $compare.behind_by -ne 0){throw 'Comparison binding mismatch'}
$sourceIndex=@()
foreach($r in $current.sources){
 $raw=[IO.File]::ReadAllBytes((Join-Path $reviewRoot $r.capture))
 CheckBlob $raw $r.git_blob
 if($raw.Length -ne $r.bytes -or (HashBytes $raw) -ne $r.sha256){throw 'Current source mismatch'}
 $sourceIndex+=@{capture=$r.capture;repo_path=$r.repo_path;ref=$r.ref;git_blob=$r.git_blob;bytes=$r.bytes;sha256=$r.sha256;binding='Direct fixed-commit retrieval'}
}
foreach($r in (Get-Content -LiteralPath (Join-Path $reviewRoot 'CAPTURE_H_PAYLOADS.json') -Raw|ConvertFrom-Json)){
 $raw=[Convert]::FromBase64String($r.content)
 CheckBlob $raw $r.git_blob
 NewBytes (Join-Path $reviewRoot $r.capture) $raw
 $old=Join-Path (Split-Path $reviewRoot -Parent) ('reil_c4_0b2_fix_review_20261014/'+$r.capture)
 if((Get-FileHash -LiteralPath $old -Algorithm SHA256).Hash.ToLowerInvariant() -ne (HashBytes $raw)){throw 'H/HB source changed from reviewed reference'}
 $sourceIndex+=@{capture=$r.capture;repo_path=$r.repo_path;ref=$r.ref;git_blob=$r.git_blob;bytes=$raw.Length;sha256=(HashBytes $raw);binding='Direct fixed-commit retrieval; same bytes as prior 0b2-fix reference'}
}
$oldAudit=Get-Content -LiteralPath (Join-Path $priorRoot 'STATIC_AUDIT.json') -Raw|ConvertFrom-Json
$changed=@($compare.files | ForEach-Object {$_.filename})
foreach($r in $oldAudit.source_index){
 if($r.capture -eq 'source/docs/REIL_PREREQUISITES_STATUS_20261004.md'){continue}
 $raw=[IO.File]::ReadAllBytes((Join-Path $priorRoot $r.capture))
 CheckBlob $raw $r.git_blob
 if($raw.Length -ne $r.bytes -or (HashBytes $raw) -ne $r.sha256){throw 'Prior capture mismatch'}
 $repoPath='bms-balancing/'+$r.capture.Substring('source/'.Length)
 $binding='Prior fixed-commit capture; path unchanged in complete base-to-head comparison'
 if($r.capture -eq 'source/original_util/util_LFP.py.txt'){
  $repoPath='REIL original util_LFP.py'
  $binding='Prior independently pinned public original source; text-only copy, no data workbook'
 }elseif($changed -contains $repoPath){throw 'Attempted reuse of changed source'}
 NewBytes (Join-Path $reviewRoot $r.capture) $raw
 $sourceIndex+=@{capture=$r.capture;repo_path=$repoPath;ref=$r.ref;git_blob=$r.git_blob;bytes=$r.bytes;sha256=$r.sha256;binding=$binding}
}
foreach($name in @('REVIEW_KO.md','REQUEST_CORRECTIONS_KO.md','DECISION.json','STATIC_AUDIT.json','CAPTURE_INDEX.json','CAPTURE_MORE_INDEX.json','CAPTURE_ANNEX_INDEX.json','CAPTURE_UTIL_INDEX.json')){
 NewBytes (Join-Path $reviewRoot ('basis/PRIOR_'+$name)) ([IO.File]::ReadAllBytes((Join-Path $priorRoot $name)))
}
$attachments=@()
foreach($a in $current.attachments){
 $path=Join-Path 'C:/Users/Administrator/Downloads' $a.attachment
 if((Get-Item -LiteralPath $path).Length -ne $a.bytes -or (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() -ne $a.sha256){throw 'Attachment changed'}
 $attachments+=$a
}
$request=Get-Content -LiteralPath (Join-Path $reviewRoot 'source/docs/REIL_C4E_APPROVAL_REQUEST_v2_20261014.md') -Raw -Encoding UTF8
$matches=[regex]::Matches($request,'(?m)^\| (m_[12]|r_[1-6]|t_1|d_[1-6]|s_[1-6]) \|')
$ids=@($matches|ForEach-Object {$_.Groups[1].Value})
if($ids.Count -ne 21 -or @($ids|Sort-Object -Unique).Count -ne 21){throw 'New test ID count mismatch'}
$limit=[long]1073741824
$audit=[ordered]@{
 kind='STATIC_PREREVIEW_V2_AUDIT';utc=[DateTime]::UtcNow.ToString('o');reviewed_head=$current.reviewed_head
 attachments=$attachments;source_index=$sourceIndex;captured_source_count=$sourceIndex.Count;captured_git_blob_matches=$sourceIndex.Count
 comparison=@{base=$compare.base;head=$compare.head;status=$compare.status;ahead=$compare.ahead_by;behind=$compare.behind_by;total_commits=$compare.total_commits;too_large=$compare.too_large;production_and_seven_tests_changed=$false}
 new_test_ids=$ids;new_tests=21;existing_tests=159;GREEN_tests=(159+21)
 regression_static_counts=@{
  COBYQA_calls=14;per_call_internal_maxfev=50;per_return_independent_reevaluation_max=1
  fake_minimize_max=(8+4+982+1);Sobol_related_tests=15;Sobol_related_tests_are_not_generator_call_count=$true
  old_real_fork_by_family=@{original_0a=3;fix_0a=1;fix_0b1=3;fix2_0b1=1;original_0b2=2};old_real_fork=10;new_proposed_fork=5;GREEN_real_fork=15;GREEN_fork_cap=17
  preserved_util_without_optimizer=@{test06=@{extract_battery_data_max=5;objective_fun_max=3;dVdQ_hc_max=9};b2_h1_h4=@{extract_battery_data_max=4;objective_fun_max=0;dVdQ_hc_max=48};scope='Separate named API entry counts; nested calls not independent optimizer evaluations; static conservative bounds, not observed execution counts'}
 }
 budget_arithmetic=@{E0_steps=(60+600+600+300);E1_measure=9000;E1_record=9900;E1_stage=10800;E1_reserve=(10800-9000)}
 counterexamples=@{
  after_final_record_growth=@{type='Constant arithmetic only; no file growth experiment';limit_bytes=$limit;at_first_check_bytes=($limit-100);later_end_record_bytes=1024;after_end_record_bytes=($limit-100+1024);excess_bytes=924}
  active_stop_done_race=@{type='Static control-flow possibility, not an observed process race';detected_active_s=1800.01;limit_s=1800;done_arrives_only_in_final_drain=$true;final_observation_state='COMPLETED';global_stop_preserved=$true;E3a='INCOMPLETE'}
 }
 received_code_import_calls_or_execution=0;tests=0;optimizer=0;Python=0;Sobol=0;COMSOL_JVM_compile_solve=0;REIL_xlsx_pkl_notebook_download_or_opening=0
 repository_source_changes=0;external_delivery=0;own_PowerShell_data_tools_only=$true;execution_authorization=$false
}
NewJson (Join-Path $reviewRoot 'STATIC_AUDIT.json') $audit
[ordered]@{sources=$sourceIndex.Count;new_test_ids=$ids;GREEN_tests=180;static_fork_total=15;bound=17;received_execution=0}|ConvertTo-Json -Depth 6
