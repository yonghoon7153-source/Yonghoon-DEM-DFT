# New static parser call only; does not dot-source or execute the candidate.
$ErrorActionPreference='Stop'
$s1parseTarget=Join-Path $PSScriptRoot 'candidate/Parent.ps1.inactive.txt'
$s1parseTokens=$null
$s1parseErrors=$null
$s1parseAst=[System.Management.Automation.Language.Parser]::ParseFile($s1parseTarget,[ref]$s1parseTokens,[ref]$s1parseErrors)
$s1parseResult=[ordered]@{kind='POWERSHELL_STATIC_PARSE_ONLY';utc=[DateTimeOffset]::UtcNow.ToString('o');source_sha256=(Get-FileHash -LiteralPath $s1parseTarget -Algorithm SHA256).Hash.ToLowerInvariant();errors=@($s1parseErrors|ForEach-Object{[ordered]@{message=$_.Message;start_line=$_.Extent.StartLineNumber}});candidate_executed=$false;parser_assembly=[System.Management.Automation.Language.Parser].Assembly.Location}
$s1parseJson=$s1parseResult|ConvertTo-Json -Depth 6
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'PARENT_STATIC_PARSE.json'),$s1parseJson,[Text.UTF8Encoding]::new($false))
$s1parseJson
if(@($s1parseErrors).Count -gt 0){throw 'PARENT_STATIC_PARSE_ERRORS'}
