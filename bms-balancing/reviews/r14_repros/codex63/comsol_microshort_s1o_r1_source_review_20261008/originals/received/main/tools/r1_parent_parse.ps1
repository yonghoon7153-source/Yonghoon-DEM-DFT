# New static-only parser. No dot-sourcing or invocation of candidate functions.
$ErrorActionPreference='Stop'
$r1Root=Split-Path -Parent $PSScriptRoot
$r1Path=Join-Path $r1Root 'candidate/Parent.ps1.inactive.txt'
$r1Bytes=[IO.File]::ReadAllBytes($r1Path)
$r1Text=[Text.Encoding]::UTF8.GetString($r1Bytes)
$r1Tokens=$null;$r1Errors=$null
$r1Ast=[System.Management.Automation.Language.Parser]::ParseInput($r1Text,[ref]$r1Tokens,[ref]$r1Errors)
$r1Functions=@($r1Ast.FindAll({param($node) $node -is [System.Management.Automation.Language.FunctionDefinitionAst]},$true)|ForEach-Object{
    $start=$_.Extent.StartOffset;$end=$_.Extent.EndOffset
    $span=[Text.Encoding]::UTF8.GetBytes($r1Text.Substring($start,$end-$start))
    $sha=[Security.Cryptography.SHA256]::Create()
    try{$hash=([BitConverter]::ToString($sha.ComputeHash($span))).Replace('-','').ToLowerInvariant()}finally{$sha.Dispose()}
    [ordered]@{name=$_.Name;start_line=$_.Extent.StartLineNumber;end_line=$_.Extent.EndLineNumber;start_utf16=$start;end_utf16_exclusive=$end;start_byte=[Text.Encoding]::UTF8.GetByteCount($r1Text.Substring(0,$start));bytes=$span.Length;sha256=$hash;extraction_rule='UTF-8 bytes of source substring from FunctionDefinitionAst start inclusive to end exclusive; final closing brace included, following newline excluded; no line-ending normalization'}
})
$r1Result=[ordered]@{kind='STATIC_PARSE_NOT_FUNCTIONAL_VALIDATION';utc=[DateTime]::UtcNow.ToString('o');source_sha256=(Get-FileHash -LiteralPath $r1Path).Hash.ToLowerInvariant();parser_assembly=[System.Management.Automation.Language.Parser].Assembly.Location;parser_assembly_sha256=(Get-FileHash -LiteralPath ([System.Management.Automation.Language.Parser].Assembly.Location)).Hash.ToLowerInvariant();parser_version=[System.Management.Automation.Language.Parser].Assembly.FullName;errors=@($r1Errors|ForEach-Object{[ordered]@{message=$_.Message;start_line=$_.Extent.StartLineNumber}});functions=$r1Functions;candidate_executed=$false;ps51_compatibility_claimed=$false}
[IO.File]::WriteAllText((Join-Path $r1Root 'PARENT_STATIC_PARSE.json'),($r1Result|ConvertTo-Json -Depth 9),[Text.UTF8Encoding]::new($false))
[ordered]@{kind=$r1Result.kind;errors=@($r1Errors).Count;functions=$r1Functions.Count;source_sha256=$r1Result.source_sha256;candidate_executed=$false}|ConvertTo-Json -Compress
if(@($r1Errors).Count -gt 0){throw 'PARENT_STATIC_PARSE_ERROR'}
