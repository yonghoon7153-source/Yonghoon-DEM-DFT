# Reviewer-owned text hashing only. No supplied modules are imported or executed.
$ErrorActionPreference = 'Stop'
$reviewSnapshot = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'RECEIVED_SNAPSHOT.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$reviewSha1 = [System.Security.Cryptography.SHA1]::Create()
$reviewSha256 = [System.Security.Cryptography.SHA256]::Create()
$reviewRows = @()
foreach ($reviewItem in $reviewSnapshot.files) {
    $reviewBytes = [System.Text.Encoding]::UTF8.GetBytes([string]$reviewItem.content)
    $reviewHeader = [System.Text.Encoding]::UTF8.GetBytes("blob " + $reviewBytes.Length + [char]0)
    [byte[]]$reviewBlobBytes = $reviewHeader + $reviewBytes
    $reviewBlob = [BitConverter]::ToString($reviewSha1.ComputeHash($reviewBlobBytes)).Replace('-', '').ToLowerInvariant()
    $reviewHash = [BitConverter]::ToString($reviewSha256.ComputeHash($reviewBytes)).Replace('-', '').ToLowerInvariant()
    $reviewRows += [ordered]@{path=$reviewItem.path; bytes=$reviewBytes.Length; sha256=$reviewHash; expected_git_blob=$reviewItem.sha; git_blob=$reviewBlob; git_blob_match=($reviewBlob -eq $reviewItem.sha)}
}
$reviewSha1.Dispose()
$reviewSha256.Dispose()
$reviewFailed = @($reviewRows | Where-Object { -not $_.git_blob_match })
[ordered]@{scope='Hash decoded UTF-8 connector text, not raw experimental data'; count=$reviewRows.Count; failures=$reviewFailed.Count; files=$reviewRows} | ConvertTo-Json -Depth 8
if ($reviewFailed.Count -gt 0) { exit 1 }
