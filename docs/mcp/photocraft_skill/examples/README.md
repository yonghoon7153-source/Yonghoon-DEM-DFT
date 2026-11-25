# PhotoCraft action JSON 예시 (초안 · 실행 안 함 · 2026-11-25)

정본 꼴 = `{"steps": [[명령 id, {매개변수}], …]}` — PhotoCraft `batch --actions` 가 그대로 읽는 꼴 (`apps/photocraft-cli/src/actions.rs:46-56`, `crates/engine-core/src/cmd/automate_cmds.rs:72-98`) 이고, `tools/pc_actions.py run` 이 같은 단계를 `photocraft-cli run --cmd … --params …` 로 바꿔 돌린다.  출처 · 메모는 이 파일에 넣지 않고 기록 (`record/*.record.json`) 에 둔다 (action 파일 = 실행되는 것만).

| 파일 | 모드 | 무엇 | 가정 |
|---|---|---|---|
| `fig_crop_resize_png.actions.json` | figure (data 도 통과) | 자르기 (120, 80, 1600 × 1200) → 가로 1200 px (bicubic · 세로는 비율 유지) → 300 ppi 표기 (재표본 없음) → PNG | 원본 ≥ 1720 × 1280 |
| `sem_levels_global.actions.json` | **data** | 선택 해제 → 전체 레벨 입력 12–238 → 0–255 · 감마 1 (선형) | 8 · 16 비트 회색 SEM |
| `sem_levels_global.record.example.json` | — | 기록 꼴 예시 (`<…>` = 채울 자리 · 지어낸 해시 없음) | — |
| `thumb_1280x720_jpeg.actions.json` | figure | 16:9 자르기 (0, 125, 2400 × 1350) 와 1280 × 720 재표본을 한 단계로 (`targetWidth` · `targetHeight`) → 8 비트 → JPEG 품질 92 | 원본 2400 × 1600 (3:2) |
| `fig_margin_label_png.actions.json` | figure 만 | 300 ppi 표기 → 위 여백 80 px (흰색) → 여백 안에 패널 글자 '(a)' (Aptos 12 pt) | 데이터 그림 위에는 쓰지 않는다 (1저자 Q2) |

## 돌리는 법 (1저자 PC · 설치 뒤)

```bash
T=tools; J=~/pc_jobs/2026-11-25_sem01          # 작업 폴더 하나 = 작업 하나
python3 -I -B $T/pc_actions.py init $J --src /path/to/sem_cs_01.png --source-note "SEM 단면 1 (원자료 위치는 1저자)"
python3 -I -B $T/pc_actions.py check examples/sem_levels_global.actions.json --mode data
python3 -I -B $T/pc_actions.py run $J examples/sem_levels_global.actions.json --mode data \
    --in sem_cs_01.png --out sem_cs_01_lv.png --bin /usr/bin/photocraft-cli --dry-run   # 명령만 보기
python3 -I -B $T/pc_actions.py run $J examples/sem_levels_global.actions.json --mode data \
    --in sem_cs_01.png --out sem_cs_01_lv.png --bin /usr/bin/photocraft-cli             # 실행 + 기록
python3 -I -B $T/pc_actions.py verify $J/record/sem_cs_01_lv.record.json --bin /usr/bin/photocraft-cli  # 재현성
```

Windows (PowerShell) 는 `--bin "$env:LOCALAPPDATA\Programs\ArtCraft\PhotoCraft\photocraft-cli.exe"` · `py -3 -I -B tools\pc_actions.py …`.  ⚠ 손으로 `--params '{"x":1}'` 를 칠 때 Windows PowerShell 5.1 은 안쪽 큰따옴표를 깨뜨린다 [추정 · 알려진 동작] → `pc_actions.py` (인자 목록으로 넘김) 또는 아래 `batch` 를 쓴다.

`pc_actions.py` 없이 같은 일 (bash):

```bash
photocraft-cli run "$J/in/sem_cs_01.png" \
  --cmd select.deselect --params '{}' \
  --cmd image.adjustments.levels --params '{"inBlack":12,"inWhite":238,"gamma":1,"outBlack":0,"outWhite":255}' \
  --cmd document.inspect \
  --out "$J/out/sem_cs_01_lv.png" --metadata none --no-gpu
# 폴더 통째로 (in/ 의 모든 그림 · 결과 이름 = <stem>.<ext>):
photocraft-cli batch --actions examples/sem_levels_global.actions.json --in "$J/in" --out "$J/out" \
  --format png --metadata none --no-gpu --error-log "$J/record/batch_errors.txt"
```

JPEG 썸네일은 `--out …/thumb.jpg --quality 92 --jpeg-format baseline` (확장자가 형식을 고른다 · `apps/photocraft-cli/src/args.rs:44-102`).
