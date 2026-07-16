# =============================================================================
# watch_papers_inbox.ps1 — 폴더에 논문 PDF가 들어오면 논문 에이전트 자동 실행
#
# 동작: $Inbox 폴더를 스캔 → 처음 보는 PDF마다
#   1) repo의 litdb/inbox/ 로 복사
#   2) claude 헤드리스(-p)로 논문 에이전트(digest → INDEX/comparison 갱신 → commit/push)
#   3) 처리 목록(.processed_inbox.txt)에 기록 (중복 실행 방지)
#
# 설치 (관리자 아님, 한 번만):
#   1) 아래 $Inbox / $Repo 경로를 본인 것으로 수정
#   2) 작업 스케줄러 등록 (매 시간; 원하면 /mo 30 /sc minute 등으로):
#      schtasks /create /tn "litdb-paper-agent" /sc hourly /mo 1 /tr ^
#        "powershell -NoProfile -ExecutionPolicy Bypass -File \"C:\Users\안용훈\Yonghoon-DEM-DFT\tools\local\watch_papers_inbox.ps1\""
#   수동 실행 테스트: powershell -ExecutionPolicy Bypass -File .\watch_papers_inbox.ps1
#
# 주의:
#   - digest 1편 = 토큰 대량 소모 (오늘 리뷰 1편 ≈ 32만 토큰). 인박스에 한꺼번에
#     쏟아넣지 말 것 — 스크립트도 실행당 최대 $MaxPerRun 편만 처리한다.
#   - 폴더에 이미 쌓인 논문들도 전부 처리 대상(시간당 $MaxPerRun편씩 소화).
#     '지금부터 새 파일만' 원하면 아래 한 줄로 기존 파일을 처리완료로 선등록:
#     Get-ChildItem $Inbox -Filter *.pdf -Recurse | %% { Add-Content $Log ($_.FullName.Substring($Inbox.Length+1)) }
#   - --dangerously-skip-permissions 는 이 repo 폴더 안에서만 쓰는 전제.
#     결과는 항상 git 커밋으로 남으니 나중에 diff로 검수.
# =============================================================================

$Inbox     = "C:\Users\안용훈\Desktop\읽어야되는 논문"   # <- 논문 떨어뜨리는 폴더
$Repo      = "C:\Users\안용훈\Yonghoon-DEM-DFT"          # <- 로컬 repo 클론
$MaxPerRun = 2                                           # 실행당 최대 처리 편수

$RepoInbox = Join-Path $Repo "litdb\inbox"
$Log       = Join-Path $Repo "litdb\.processed_inbox.txt"

if (-not (Test-Path $Inbox)) { New-Item -ItemType Directory -Path $Inbox | Out-Null }
if (-not (Test-Path $RepoInbox)) { New-Item -ItemType Directory -Path $RepoInbox | Out-Null }
if (-not (Test-Path $Log)) { New-Item -ItemType File -Path $Log | Out-Null }

$done = Get-Content $Log -ErrorAction SilentlyContinue
# 하위폴더까지 재귀 스캔; 중복 방지 키 = Inbox 기준 상대경로 (하위폴더\파일명)
$new  = Get-ChildItem $Inbox -Filter *.pdf -Recurse |
        ForEach-Object {
            $_ | Add-Member -NotePropertyName Rel -NotePropertyValue ($_.FullName.Substring($Inbox.Length+1)) -PassThru
        } |
        Where-Object { $done -notcontains $_.Rel } |
        Sort-Object LastWriteTime | Select-Object -First $MaxPerRun

if (-not $new) { Write-Host "no new PDFs."; exit 0 }

foreach ($pdf in $new) {
    $category = Split-Path $pdf.Rel -Parent          # 하위폴더 = 분류 태그 (루트면 빈 문자열)
    if (-not $category) { $category = "(미분류)" }
    Write-Host ">>> processing [$category] $($pdf.Name)"
    Copy-Item $pdf.FullName -Destination $RepoInbox -Force
    $rel = "litdb/inbox/$($pdf.Name)"

    $prompt = @"
$rel 파일을 논문 에이전트(litdb-curator) 방식으로 처리해줘. 사용자 분류 폴더: "$category"
— 이 분류를 digest 태그와 INDEX.md 항목에 반영해줘.
1) 전체 페이지를 정독하고 litdb/papers/ 에 표준 digest(md)를 저장
2) litdb/INDEX.md 와 litdb/comparison_vs_ours.md 갱신
3) 처리 후 원본은 litdb/inbox/ 에서 삭제
4) git add litdb && 한 줄 커밋 메시지로 commit && push (브랜치 claude/friendly-meitner-lldvar)
digest는 CLAUDE.md 규율(문헌 수치는 소환값, db 절대값과 혼용 금지)을 따를 것.
"@

    Push-Location $Repo
    git pull origin claude/friendly-meitner-lldvar 2>$null
    claude -p $prompt --dangerously-skip-permissions
    $ok = $LASTEXITCODE
    Pop-Location

    if ($ok -eq 0) {
        Add-Content $Log $pdf.Rel
        Write-Host "<<< done: $($pdf.Name)"
    } else {
        Write-Host "!!! claude exited $ok for $($pdf.Name) — 다음 주기에 재시도" -ForegroundColor Yellow
    }
}
