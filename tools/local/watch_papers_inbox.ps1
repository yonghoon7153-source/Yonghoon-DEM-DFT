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
$RunLog    = Join-Path $Repo "litdb\.watcher_run.log"

# 중복실행 가드 (CLAUDE.md 관례) — 수동 트리거와 정규 주기가 겹치면 같은 논문 2회 처리됨
$mutex = New-Object System.Threading.Mutex($false, "Global\litdb-paper-agent")
if (-not $mutex.WaitOne(0)) { Write-Host "another instance running — skip."; exit 0 }

Start-Transcript -Path $RunLog -Append | Out-Null

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
git 커밋/푸시와 inbox 정리는 이 스크립트가 하니 하지 말 것.
digest는 CLAUDE.md 규율(문헌 수치는 소환값, db 절대값과 혼용 금지)을 따를 것.
"@

    Push-Location $Repo
    # 무인 실행 가드: pull이 편집기(vim)를 띄우면 영원히 멈춘다 (2026-07-16 실제 사고)
    $env:GIT_EDITOR = "true"; $env:GIT_MERGE_AUTOEDIT = "no"
    git pull --rebase --autostash origin claude/friendly-meitner-lldvar
    if ($LASTEXITCODE -ne 0) {   # 충돌 시 중간상태 남기지 말고 원상복구 (다음 주기에 재시도)
        git rebase --abort 2>$null
        Write-Host "!!! git pull 실패 — repo 정리 후 이번 편은 건너뜀" -ForegroundColor Yellow
        Pop-Location
        continue
    }
    claude -p $prompt --dangerously-skip-permissions
    $ok = $LASTEXITCODE
    Pop-Location

    if ($ok -eq 0) {
        # 커밋/푸시/정리는 스크립트가 결정론적으로 (헤드리스 에이전트가 3회 연속 누락한 전력)
        Push-Location $Repo
        Remove-Item (Join-Path $RepoInbox $pdf.Name) -Force -ErrorAction SilentlyContinue
        git add litdb
        git commit -m "litdb: digest $($pdf.BaseName)"
        git push origin claude/friendly-meitner-lldvar
        Pop-Location
        Add-Content $Log $pdf.Rel
        Write-Host "<<< done: $($pdf.Name)"
    } else {
        Write-Host "!!! claude exited $ok for $($pdf.Name) — 다음 주기에 재시도" -ForegroundColor Yellow
    }
}
Stop-Transcript | Out-Null
