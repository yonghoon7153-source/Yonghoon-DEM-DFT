param([Parameter(Mandatory=$true)][ValidateSet('capture','package','final','deliver')][string]$Mode)
$ErrorActionPreference='Stop'
$root=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$utf8=New-Object Text.UTF8Encoding($false)
$innerName='COMSOL_S1_JOB_COMMIT_EVENT_DETAILED_DESIGN_20261016.zip'
$outerName='COMSOL_S1_JOB_COMMIT_EVENT_DETAILED_DESIGN_DELIVERY_20261016.zip'
function RJ([string]$p) { [IO.File]::ReadAllText($p,$utf8) | ConvertFrom-Json }
function SJ([string]$n,$obj) {
  $p=Join-Path $root $n
  if (Test-Path -LiteralPath $p) { throw "Refusing overwrite: $n" }
  [IO.File]::WriteAllText($p,(($obj | ConvertTo-Json -Depth 50)+[char]10),$utf8)
}
function ID([string]$p) {
  $f=Get-Item -LiteralPath $p
  [ordered]@{path=$f.FullName; bytes=$f.Length; sha256=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()}
}
function BH([byte[]]$b) {
  $h=[Security.Cryptography.SHA256]::Create()
  try { ([BitConverter]::ToString($h.ComputeHash($b))).Replace('-','').ToLowerInvariant() } finally { $h.Dispose() }
}
function Preserve {
  $before=RJ (Join-Path $root 'SELECTED_INPUTS_BEFORE.json')
  $rows=@($before.files | ForEach-Object {
    $v=ID $_.path
    $same=($v.bytes -eq $_.bytes -and $v.sha256 -ceq $_.sha256)
    if (-not $same) { throw 'Selected original changed' }
    [ordered]@{path=$v.path; bytes=$v.bytes; sha256=$v.sha256; matches_before=$same}
  })
  [ordered]@{kind='SELECTED_LOCAL_INPUT_PRESERVATION'; observed_utc=[DateTimeOffset]::UtcNow.ToString('o'); count=$rows.Count; all_match=$true; scope='Selected local input bytes only, not remote or historical machine preservation'; files=$rows}
}
function Bundle([string]$zipName,[string]$manifestName,$names) {
  Add-Type -AssemblyName System.IO.Compression
  Add-Type -AssemblyName System.IO.Compression.FileSystem
  $rows=@($names | ForEach-Object { $v=ID (Join-Path $root $_); [ordered]@{path=$_; bytes=$v.bytes; sha256=$v.sha256} })
  SJ $manifestName ([ordered]@{kind='INACTIVE_DOCUMENT_BUNDLE_MANIFEST'; payload_count=$rows.Count; files=$rows; contract_adopted=$false; native_ready=$false; elapsed_claim=$null})
  $members=@($names)+@($manifestName)
  $zp=Join-Path $root $zipName
  if (Test-Path -LiteralPath $zp) { throw 'ZIP already exists' }
  $z=[IO.Compression.ZipFile]::Open($zp,[IO.Compression.ZipArchiveMode]::Create)
  try { foreach ($n in $members) { [void][IO.Compression.ZipFileExtensions]::CreateEntryFromFile($z,(Join-Path $root $n),$n,[IO.Compression.CompressionLevel]::Optimal) } } finally { $z.Dispose() }
  $z=[IO.Compression.ZipFile]::OpenRead($zp)
  try {
    if ($z.Entries.Count -ne $members.Count) { throw 'Member count mismatch' }
    $seen=@{}
    foreach ($e in $z.Entries) {
      $n=$e.FullName
      if ($n -cnotin $members -or $seen.ContainsKey($n.ToLowerInvariant()) -or $n.Contains('\') -or $n.Contains(':') -or $n.StartsWith('/') -or ($n.Split('/') -contains '..')) { throw 'Unsafe/duplicate/unexpected member' }
      $seen[$n.ToLowerInvariant()]=$true
      $s=$e.Open(); $m=New-Object IO.MemoryStream
      try { $s.CopyTo($m); $b=$m.ToArray() } finally { $s.Dispose(); $m.Dispose() }
      $x=if ($n -ceq $manifestName) { ID (Join-Path $root $n) } else { @($rows | Where-Object { $_.path -ceq $n })[0] }
      if ($b.Length -ne $x.bytes -or (BH $b) -cne $x.sha256) { throw 'ZIP size/SHA mismatch' }
    }
  } finally { $z.Dispose() }
  [ordered]@{archive=(ID $zp); manifest=(ID (Join-Path $root $manifestName)); payload_count=$rows.Count; entries=$members.Count; exact_set_size_sha_safe_paths=$true; crc_independently_recomputed=$false}
}
if ($Mode -eq 'capture') {
  $spec=RJ (Join-Path $root 'BASIS_SPEC.json')
  $rows=@($spec.files | ForEach-Object {
    $p=if ([IO.Path]::IsPathRooted($_.source)) { $_.source } else { Join-Path $root $_.source }
    $v=ID $p
    if ($v.sha256 -cne $_.sha256) { throw "Basis identity mismatch: $p" }
    [ordered]@{path=$v.path; bytes=$v.bytes; sha256=$v.sha256; copy=$_.copy}
  })
  SJ 'SELECTED_INPUTS_BEFORE.json' ([ordered]@{kind='SELECTED_INPUTS_BEFORE'; observed_utc=[DateTimeOffset]::UtcNow.ToString('o'); count=$rows.Count; boundary='After existing-source reading and authoring BASIS_SPEC/data utility; before new design documents and basis copies'; files=$rows})
  foreach ($row in $rows) {
    $d=Join-Path $root $row.copy
    [void][IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($d))
    [IO.File]::Copy($row.path,$d,$false)
    $v=ID $d
    if ($v.sha256 -cne $row.sha256 -or $v.bytes -ne $row.bytes) { throw 'Basis copy mismatch' }
  }
  [ordered]@{kind='BASIS_CAPTURE'; count=$rows.Count; exact_copies=$true; target_execution=0} | ConvertTo-Json
}
if ($Mode -eq 'package') {
  $choice=RJ (Join-Path $root 'USER_DIRECTION_SELECTION.json')
  $protocol=RJ (Join-Path $root 'PROTOCOL_DRAFT.json')
  $fields=RJ (Join-Path $root 'PARENT_EVIDENCE_FIELDS.json')
  $checks=[ordered]@{
    exact_user_quote=($choice.user_message -ceq '1번가자')
    conditional_design_selected=($choice.selected_option -eq 1 -and $choice.direction_selected -eq $true -and $choice.operational_risk_accepted -eq $false)
    no_contract_adoption=($choice.contract_adopted -eq $false -and $protocol.contract_adopted -eq $false)
    three_null_deadlines=($protocol.deadlines.Count -eq 3 -and @($protocol.deadlines | Where-Object { $null -ne $_.duration_seconds }).Count -eq 0)
    no_operational_permission=($protocol.implementation_authorized -eq $false -and $protocol.execution_authorized -eq $false -and $protocol.native_ready -eq $false)
    cutoff_not_OS_barrier=($protocol.cutoff.proves_all_past_OS_events -eq $false)
    blocked_query_not_closed=($protocol.blocked_query.close_in_use_handles -eq $false -and $protocol.blocked_query.expiry_proves_cancellation -eq $false)
    descriptive_schema_only=($fields.executable_schema -eq $false -and $fields.produces_runtime_receipt -eq $false)
    gates_retained=($protocol.retained.JOB_CURRENT_COMMIT -ceq 'OPEN' -and $protocol.retained.overall -ceq 'INCOMPLETE')
  }
  if (@($checks.Values | Where-Object { $_ -ne $true }).Count -gt 0) { throw 'Document consistency check failed' }
  $before=RJ (Join-Path $root 'SELECTED_INPUTS_BEFORE.json')
  foreach ($row in $before.files) { $v=ID (Join-Path $root $row.copy); if ($v.sha256 -cne $row.sha256 -or $v.bytes -ne $row.bytes) { throw 'Reference copy changed' } }
  SJ 'SELECTED_INPUTS_AFTER.json' (Preserve)
  SJ 'STATIC_DOCUMENT_CHECK.json' ([ordered]@{kind='JSON_FILE_CONSISTENCY_NOT_FUNCTIONAL_TEST'; checks=$checks; basis_copies=$before.count; target_tests=0; received_program_execution=0})
  $names=@(Get-ChildItem -LiteralPath $root -Recurse -File | Sort-Object FullName | ForEach-Object { $_.FullName.Substring($root.Length+1).Replace('\','/') })
  $bundle=Bundle $innerName 'PACKAGE_MANIFEST.json' $names
  SJ 'SELECTED_INPUTS_POST_PACKAGE.json' (Preserve)
  SJ 'DELIVERY_RECEIPT.json' ([ordered]@{kind='CONDITIONAL_DIRECTION_DOCUMENT_DESIGN_RECEIPT'; recipient=$null; package=$bundle; selected_local_inputs=$before.count; all_selected_unchanged=$true; conditional_direction_selected=$true; contract_adopted=$false; native_ready=$false; target_tests=0; COMSOL=0; numeric_work_budget=$null; elapsed_claim=$null; boundary='After ZIP readback and selected-input preservation, before receipt write and tool return'})
  [ordered]@{kind='DETAILED_DESIGN_PACKAGE_RETURN'; package=$bundle; receipt=(ID (Join-Path $root 'DELIVERY_RECEIPT.json')); selected_local_inputs=$before.count; contract_adopted=$false; native_ready=$false; target_tests=0} | ConvertTo-Json -Depth 10
}
if ($Mode -eq 'final') {
  $preserved=Preserve
  $receipt=RJ (Join-Path $root 'DELIVERY_RECEIPT.json')
  $current=ID (Join-Path $root $innerName)
  if ($current.sha256 -cne $receipt.package.archive.sha256) { throw 'Inner ZIP changed' }
  $records=@('DELIVERY_RECEIPT.json','SELECTED_INPUTS_POST_PACKAGE.json','PACKAGE_TOOL_RETURN.json','USER_DIRECTION_SELECTION.json','DETAILED_DESIGN_KO.md','PROTOCOL_DRAFT.json','PARENT_EVIDENCE_FIELDS.json','REVIEW_REQUEST_KO.txt' | ForEach-Object { ID (Join-Path $root $_) })
  SJ 'FINAL_CHECK.json' ([ordered]@{kind='DOCUMENT_DESIGN_FINAL_CHECK'; observed_utc=[DateTimeOffset]::UtcNow.ToString('o'); archive=$current; records=$records; selected_local_inputs=$preserved.count; selected_all_match=$preserved.all_match; direction_selected=$true; operational_risk_accepted=$false; contract_adopted=$false; native_ready=$false; target_tests=0; COMSOL=0; elapsed_claim=$null; numeric_work_budget=$null; boundary='After listed readback and hashes, before this check write and tool return'})
  [ordered]@{kind='DETAILED_DESIGN_FINAL_CHECK_RETURN'; archive=$current; final_check=(ID (Join-Path $root 'FINAL_CHECK.json')); selected_all_match=$preserved.all_match; contract_adopted=$false; native_ready=$false; target_tests=0; boundary='After check write/read/hash, before tool return and later serialization'} | ConvertTo-Json -Depth 10
}
if ($Mode -eq 'deliver') {
  $names=@($innerName,'DELIVERY_RECEIPT.json','SELECTED_INPUTS_POST_PACKAGE.json','PACKAGE_TOOL_RETURN.json','FINAL_CHECK.json','FINAL_CHECK_TOOL_RETURN.json','DELIVERY_INDEX.md')
  $bundle=Bundle $outerName 'DELIVERY_MANIFEST.json' $names
  $preserved=Preserve
  [ordered]@{kind='DETAILED_DESIGN_TRANSPORT_READBACK'; package=$bundle; selected_local_inputs=$preserved.count; selected_all_match=$preserved.all_match; conditional_direction_selected=$true; contract_adopted=$false; native_ready=$false; target_tests=0; COMSOL=0; external_transmission=0; elapsed_claim=$null; boundary='New transport wrapper verified; future return not recursively included'} | ConvertTo-Json -Depth 10
}
