# Reviewer-owned byte/JSON/constant checks only. Never loads received code.
$ErrorActionPreference='Stop'
$reviewRoot=[IO.Path]::GetFullPath($PSScriptRoot)
function Sha256([byte[]]$data) {
 $h=[Security.Cryptography.SHA256]::Create()
 try { return ([BitConverter]::ToString($h.ComputeHash($data))).Replace('-','').ToLowerInvariant() } finally { $h.Dispose() }
}
$indexNames=@('CAPTURE_INDEX.json','CAPTURE_MORE_INDEX.json','CAPTURE_UTIL_INDEX.json','CAPTURE_ANNEX_INDEX.json')
$index=@(); foreach($name in $indexNames){ $index+=@(Get-Content -LiteralPath (Join-Path $reviewRoot $name) -Raw | ConvertFrom-Json) }
$checked=@()
foreach($item in $index){
 $path=Join-Path $reviewRoot $item.capture
 $raw=[IO.File]::ReadAllBytes($path)
 $head=[Text.Encoding]::ASCII.GetBytes('blob '+$raw.Length+[char]0)
 $sha=[Security.Cryptography.SHA1]::Create()
 try{$blob=([BitConverter]::ToString($sha.ComputeHash([byte[]]($head+$raw)))).Replace('-','').ToLowerInvariant()}finally{$sha.Dispose()}
 if($raw.Length -ne $item.bytes -or (Sha256 $raw) -ne $item.sha256 -or $blob -ne $item.git_blob){throw "Capture mismatch: $path"}
 $checked+=@{capture=$item.capture;ref=$item.ref;git_blob=$blob;bytes=$raw.Length;sha256=(Sha256 $raw)}
}
$original=[IO.File]::ReadAllBytes((Join-Path $reviewRoot 'source/original_util/util_LFP.py.txt'))
$preserved=[IO.File]::ReadAllBytes((Join-Path $reviewRoot 'source/reviews/prereview_pybamm_reil_20261003/external/util_LFP.py.txt'))
$originalText=[Text.Encoding]::UTF8.GetString($original)
$normal=[Text.Encoding]::UTF8.GetBytes($originalText.Replace("`r`n","`n")+"`n")
if((Sha256 $original) -ne '3c19e45ef8a64ce67cda1f623551e758d4c0f67086bbae02b978428d78de1c76'){throw 'Original util identity mismatch'}
if([Convert]::ToBase64String($normal) -cne [Convert]::ToBase64String($preserved)){throw 'Util newline relation mismatch'}
$counts=@(0,0,0,0); $evals=@(0,0,0,0); $optimizer=0; $calls=0
for($case=0;$case -lt 6;$case++){
 $expected=if($case -eq 0){100000}elseif($case -eq 5){16500}else{5000}
 for($row=0;$row -lt 11;$row++){
  $tid=$case*11+$row; $worker=$tid%4
  $counts[$worker]++; $evals[$worker]+=$expected; $calls++
  $optimizer+=if($case -eq 0){20}else{1}
 }
}
$attachments=@()
foreach($name in @('REIL_C4E_APPROVAL_REQUEST_20261014.md','REIL_C4E_PREREVIEW_SEND_20261014.md')){
 $path=Join-Path 'C:/Users/Administrator/Downloads' $name
 $raw=[IO.File]::ReadAllBytes($path)
 $captured=[IO.File]::ReadAllBytes((Join-Path $reviewRoot ('source/docs/'+$name)))
 $same=[Convert]::ToBase64String($raw) -ceq [Convert]::ToBase64String($captured)
 if(-not $same){throw 'Attachment changed'}
 $attachments+=@{path=$path;bytes=$raw.Length;sha256=(Sha256 $raw);exact_capture_match=$same}
}
$audit=[ordered]@{
 kind='REVIEWER_STATIC_BYTE_AND_CONSTANT_AUDIT';utc=[DateTime]::UtcNow.ToString('o')
 reviewed_head='89d18f546cef0172ee53105ae04ba66d1e224370'
 attachments=$attachments;captured_git_blob_matches=$checked.Count;source_index=$checked
 util_byte_relation=@{original_bytes=$original.Length;original_sha256=(Sha256 $original);preserved_bytes=$preserved.Length;preserved_sha256=(Sha256 $preserved);original_CRLF_count=([regex]::Matches($originalText,"`r`n")).Count;original_final_LF=($original[-1] -eq 10);normalization='Replace CRLF with LF, then append one LF';exact_normalized_plus_LF_match=$true;source_files_modified=$false}
 plan_arithmetic=@{top_level_calls=$calls;optimizer_calls_planned=$optimizer;expected_evaluations_total=($evals|Measure-Object -Sum).Sum;worker_calls=$counts;worker_expected_evaluations=$evals;executed_calls=0;meaning='Independent constant arithmetic, not a call to plan_calls or any candidate'}
 budget_arithmetic=@{E0_step_seconds=60+600+600+300;E1_reserve_seconds=10800-9000;actual_runtime_guarantee=$false}
 P0_result_read='Preserved result JSON only; no xlsx/pkl/notebook access'
 counterexamples='Static control-flow reasoning only; no synthetic or actual test run'
 received_code_import_calls_or_execution=0;tests=0;optimizer=0;Python=0;Sobol=0;COMSOL_JVM_compile_solve=0
}
$dest=Join-Path $reviewRoot 'STATIC_AUDIT.json'
if(Test-Path -LiteralPath $dest){throw 'Refuse audit overwrite'}
$bytes=[Text.UTF8Encoding]::new($false).GetBytes(($audit|ConvertTo-Json -Depth 15)+"`n")
$stream=[IO.File]::Open($dest,[IO.FileMode]::CreateNew)
try{$stream.Write($bytes,0,$bytes.Length)}finally{$stream.Dispose()}
$null=Get-Content -LiteralPath $dest -Raw|ConvertFrom-Json
[ordered]@{audit=$dest;sha256=(Sha256 $bytes);source_count=$checked.Count;util_newline_relation='MATCH';calls=$calls;optimizer_planned=$optimizer;worker_evaluations=$evals;received_code_execution=0}|ConvertTo-Json -Depth 5
