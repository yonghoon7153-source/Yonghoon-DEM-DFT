# AVI 생성 — 연구 트랙 설명 영상 파이프라인 (리포 판)

> 1저자가 "AVI 생성" 이라고 하면 이 폴더와 스킬 (`.claude/skills/avi-generate/SKILL.md`) 의 순서대로 만든다.  트랙마다 독립된 한국어 설명 영상 한 편 (정보 전달 · 진행 보고 아님) · 레퍼런스 = 채널 "데이너스: AX | medical AI" (`@dainus2026`) 11 월 네 편의 양식 (양식만 배운다 — 그 채널의 화면 · 썸네일 · 음악 · 문구는 쓰지 않는다).
> **리포 판 (11-24)** — 리포에는 글 · 표 · 도구 · 점검 기록만 둔다 (공개 안전한 것만).  렌더 (mp4) · 음성 (wav) · 점검 그림 · 내부판 · 글꼴 · 레퍼런스 자료 (남의 영상 · 측정 원자료) 는 **리포 밖 작업 폴더**에 둔다 (공개 리포 · 크기).  `.gitignore` 가 `docs/avi/` 아래의 mp4 · wav · qa/ · audio/ · internal/ · fonts/ 를 막는다.
> 웹앱에서 보고 받기 = 영상 섹션 `/videos` (아래 §6 · 스킬의 "웹앱 영상 섹션").

## 1. 폴더

| 자리 | 무엇 |
|---|---|
| `series_plan.md` | 다음 편들 (트랙별 제목 · 한 문단) |
| `tools/` | 파이프라인 코드 (아래 §3) |
| `ep01_mixer/` | 1 편 (믹서) 의 글 자료 — `build_scenes.py` → `scenes.json` → 나머지 전부 · v2 (11-24) · 기준표 = `ep01_mixer/rubric_ep01_v2.md` (공개 사본 — 내부판 절 · 내부판 숫자 목록을 뺐다) |
| (리포 밖) 작업 폴더 | 렌더 · 음성 · 점검 그림 (`qa/`) · 앞 판 (`v1/`) · **내부판** (`internal/` — 파일 이름 `INTERNAL_공개금지` · 공개 영상 · 설명란에 쓰지 않는다) · 글꼴 (Pretendard · SIL OFL 1.1) · 레퍼런스 측정 (`reference_analysis.md` · `analysis/`) |

에피소드 폴더 (예 `ep01_mixer/`):

| 파일 | 만드는 명령 | 뜻 |
|---|---|---|
| `build_scenes.py` | (사람이 고침) | 대본 · 자막 쪼갬 · 쉼 · 빠르기 · 감정 · 화면 개체 · 출처 줄 — **내용의 원본** |
| `scenes.json` | `python3 -I ep01_mixer/build_scenes.py` | 렌더러 입력 (원본에서 생성 · 그림 개체 경로 = 편 폴더 기준 상대 경로) |
| `tts_typecast.tsv` | `avi.py tts` | **1순위** Typecast 입력표 — 한 줄 = 한 문장 |
| `tts_elevenlabs.txt` | `avi.py tts` | 예비 ElevenLabs 판 (`<break time="0.45s" />`) |
| `tts_plain.txt` · `tts_ssml.xml` | `avi.py tts` | 사람이 보는 판 (대괄호 표기) · SSML (예비) |
| `voice_audition.txt` | `avi.py tts` | 목소리 고르기 시험 문장 10 줄 + 들을 점 |
| `script.md` | `avi.py tts` (+ `script_header.md`) | 장면별 대본 · 화면 계획 · 출처 · 챕터 · 참고 문헌 |
| `ep01.srt` · `timeline.json` | `avi.py plan` (또는 render) | 자막 · 시간표 |
| `thumbnail.png` | `avi.py thumb` | 1280×720 |
| `qc.md` | (사람 + 검사 출력) | 글꼴 · 색 · 자막 안전 영역 · 숫자 ↔ 출처 대조 |
| (리포 밖) `preview_silent.mp4` | `avi.py render` | 1920×1080 · 30 fps · H.264 yuv420p · 무음 AAC · `+faststart` · 자막 구워 넣음 |
| (리포 밖) `audio_in/` · `audio/` | 1저자 · `avi.py audio-prep` | TTS 음성 파일 · `narration.wav` · `mix.wav` · `timing.json` · `audio_qc.md` |

## 2. 순서 (한 편)

> 돌리는 자리 = **리포 밖 작업 폴더** (이 폴더의 `tools/` 와 편 폴더를 복사해 간다).  리포 안에서 렌더하면 mp4 · 점검 그림이 작업 트리에 생긴다 (`.gitignore` 가 막지만 자리를 섞지 않는다).  글꼴 = `AVI_FONT_DIR=<Pretendard 폴더>` (없으면 Noto CJK 대체 글꼴 · 글자 폭이 달라 화면 자리가 바뀐다).

1. **대본 · 화면** — `build_scenes.py` 를 고친다 (말 = `say` 에 읽는 꼴 · 화면 = `text` 와 개체 · 숫자마다 `src(...)` 출처 줄).  `python3 -I ep01_mixer/build_scenes.py` 는 50 음절 넘는 문장 · `say` 안의 기호 · 24 자 넘는 자막 · '처음 / 최초 / 가장 먼저' 를 경고한다.
2. **무음 미리보기** — `python3 -I tools/avi.py render ep01_mixer` → `preview_silent.mp4`.  시간은 말 빠르기 모형 (아래 §4) 으로 잡는다.  장면 사진만 빨리 보려면 `python3 -I tools/avi.py stills ep01_mixer --shots` (장면마다 한 장 → `qa/stills/sheet_*.jpg`).
3. **목소리 고르기** — `voice_audition.txt` 10 줄을 후보 목소리로 생성 → `python3 -I tools/avi.py audio-qc ep01_mixer --wav ep01_mixer/audio_in/audition_<목소리>.wav` 로 빠르기 · 쉼 · 끝 억양을 본다.
4. **TTS 생성** — Typecast 에 `tts_typecast.tsv` 의 '문장 (읽는 꼴)' 칸을 한 줄씩 넣고, 줄마다 빠르기 · 쉼 · 감정을 표대로 맞춘다 (감정 프리셋 이름은 목소리마다 다르다 — 가장 가까운 것).  장면 하나를 한 파일로 받는다.
5. **음성 넣기** — 파일을 `ep01_mixer/audio_in/` 에 넣고 `python3 -I tools/avi.py audio-prep ep01_mixer` → 문장 경계를 찾아 문장 사이 쉼을 표의 값으로 다시 맞추고 (`--keep-pauses` 면 TTS 쉼 그대로) −14 LUFS · 참 최고점 −1.5 dBTP 로 맞춘다.  음악을 쓰면 `--bgm 음악.wav --bgm-lufs -28` (레퍼런스: 목소리가 음악보다 13–14 LU 크고 덕킹 없음).
6. **음성 QC** — `python3 -I tools/avi.py audio-qc ep01_mixer` → 편 폴더의 audio/audio_qc.md (리포 밖 · 알림이 있으면 그 문장만 다시 생성).
7. **최종 렌더** — `python3 -I tools/avi.py render ep01_mixer --out ep01_final.mp4 --audio ep01_mixer/audio/mix.wav --timing ep01_mixer/audio/timing.json` (음악 없으면 `narration.wav`).  자막 · 화면 쌓기가 실제 음성 시간에 다시 맞춰진다.  `ep01.srt` 도 다시 쓴다.
8. **썸네일** — `python3 -I tools/avi.py thumb ep01_mixer` (끝 화면의 물체 그림 `assets/powder_obj.png` 도 없으면 함께 만든다 · `--obj` = 다시 만듦 · 그림자는 그림 가장자리 40 px 에서 0 으로 사라지게 해 잘린 선이 안 보인다).
9. **QC** — `qc.md` 표를 다시 확인 (숫자 ↔ 출처 · 화면 금지 문장 · 공저 밝힘).  철회값 = `python3 -I tools/ban_sweep_files.py <파일 …>` (리포 `docs/reviews/claims.json` 을 읽기만 · 다른 자리면 `AVI_CLAIMS_JSON`).
10. **웹앱에 넣기** — §6.

### 1저자가 넣을 음성 파일

- **장면마다 한 파일**: `ep01_s01.wav` … `ep01_s11.wav` (v2 = 11 장면 · 장면 번호 = TSV 의 '장면 번호' 칸 · 파일 안에서 문장 순서 = 표 순서).
- 형식: **WAV 48 kHz (또는 44.1 kHz) · 16 / 24 bit · 모노 또는 스테레오** — MP3 면 **320 kbps**.  m4a · flac · ogg 도 읽는다.
- 한 파일로 받았다면 `ep01_full.wav` 로 넣으면 된다 (v2 = 113 문장 전체를 한 번에 맞춘다 · 장면 파일이 하나라도 있으면 장면 파일을 쓴다).
- 파일 앞뒤 무음 · 문장 사이 쉼 길이는 상관없다 (파이프라인이 다시 맞춘다).  다만 **문장 사이에 쉼이 0.1 초 이상** 있어야 경계를 찾는다.  한 문장 안에서 0.5 초 넘게 쉬면 경계로 오인할 수 있다 → 그런 문장은 따로 다시 생성.
- 음악 · 효과음은 섞지 말고 목소리만.  음악은 따로 `--bgm` 으로 (사용권은 1저자가 확인).
- 가격 · 상업 이용 · 유튜브 수익화 조건 = **1저자가 각 사이트에서 확인** (여기에 적지 않는다).

## 3. 코드 (`tools/`)

| 파일 | 하는 일 |
|---|---|
| `avi.py` | 명령 진입점 (`plan · stills · render · tts · audio-prep · audio-qc · thumb · selftest`) · numpy 스레드 1 개 고정 |
| `avi_style.py` | 측정한 색 · 글꼴 (`AVI_FONT_DIR`) · 자막 크기 · 종이 결 배경 |
| `avi_timeline.py` | 문장 → 말 구간 → 자막 구간 → 장면 구간 · 시간 닻 (`LINE~낱말+0.3` 등) · SRT · 그림 개체의 상대 경로를 편 폴더 기준으로 푼다 |
| `avi_render.py` | 개체 (원 · 점 무리 · 글 · 큰 숫자 · 선 · 칠 · 상자 · 사람 · 혼합기 · 묶음 · 그림) → 3 배 초표본 스프라이트 → 프레임 합성 → ffmpeg 파이프 (바뀐 프레임만 새로 그림) |
| `avi_tts.py` | TSV · ElevenLabs · 평문 · SSML · 오디션 · script.md |
| `avi_audio.py` | 음성 받기 · 문장 정렬 (동적 계획법) · 쉼 다시 맞춤 · BS.1770-4 음량 · 참 최고점 제한기 · 음악 섞기 · QC · 합성 시험 |
| `avi_thumb.py` | 썸네일 (numpy 광선 추적으로 그린 분말 물체 · 부드러운 그림자) |
| `korean_text.py` | 숫자 · 영어를 읽는 꼴로 · 음절 수 |
| `ban_sweep_files.py` | 리포 밖 파일 (대본 · 자막 · 설명란 초안) 의 철회값 스윕 — 리포 `--ban-sweep` 과 같은 등록부 · 같은 정규화 |
| `audio_measure.py` · `ref_*.py` | 레퍼런스 측정 도구 (남의 영상 = 분석용만 · 우리 영상에 쓰지 않음) |

- 움직임 (레퍼런스에서 잰 꼴): `fade` (나타남) · `pop` (작게 시작해 커짐) · `draw` (선 그어짐) · `grow` (막대 자람) · `count` (숫자 세어 올라감 0.9 s · 색 연보라 → 남보라) · 점 무리 `stagger` (0.02–0.04 s 간격) · `moves` (옮겨 감) · 다음 장면에서 `keep` (같은 개체가 새 자리로 미끄러짐 = 레퍼런스의 magic move) · `dim` (흐려져 배경이 됨) · 장면이 바뀌면 남기지 않은 개체는 0.3 s 에 사라진다.  자막은 컷으로 바뀐다.
- 시간 닻: `s03_l05` (문장 시작) · `s03_l05@0.5` (말 구간 절반) · `s03_l05~무게는` (그 낱말을 말하는 때 — 음절 위치로 어림) · `s03_l05$` (문장 끝) · 끝에 `+0.4` / `-0.2` 초.
- 렌더 부하: ffmpeg `-threads 1` 기본 (`--threads` 로 바꿈) · 한 번에 하나만 · 게이트가 도는 기계에서는 `nice -n 19`.  무음 미리보기 8 분 ≈ 10–15 분.
- 시험: `python3 -I tools/avi.py selftest` (합성 음성으로 정렬 ≤ 0.06 s · 쉼 다시 맞춤 · −14 LUFS · 참 최고점 · QC 보고 — 11-24 PASS 5/5 · 작업 폴더에서) — 산출물은 `tools/` 옆 `selftest/` 에 쓴다 (리포에서는 `.gitignore`).

## 4. 말 빠르기 모형 (무음 미리보기)

- 레퍼런스 측정: 발화 속도 8.37 음절/s · 문장 끝 쉼 중앙 0.335 s (80 % 가 0.24–0.46 s) · 문장 안 경계 74 % 쉼 없음 · 절 경계 1.3–1.7 s (작업 폴더의 `reference_analysis.md` §4).
- 우리 기본: `base_rate` **7.2 음절/s** × 문장별 빠르기 (0.92–1.05) + 쉼표마다 0.16 s · 문장 뒤 쉼 = 표의 값 (이음 0.3–0.45 · 문단 끝 0.6–0.8 · 물음 뒤 0.85–1.0 · 절 끝 1.4–1.5 s).
- ⚠ **7.2 음절/s 는 잠정값** — 실제 목소리의 기본 빠르기는 모른다 → 오디션 파일 QC 의 '빠르기 중앙' 을 `build_scenes.py` 의 `voice_model.base_rate` 에 넣으면 미리보기 길이가 맞아진다.  최종 영상은 실제 음성 시간 (`timing.json`) 으로 다시 잡으므로 이 값은 미리보기용이다.

## 5. 다른 트랙에 쓰려면

1. `ep01_mixer/` 를 `ep02_<트랙>/` 로 복사 → `build_scenes.py` 의 `EP` (episode · title · series · thumb) 와 장면을 새로 쓴다.
2. 숫자 · 연구는 **litdb 정본 카드** (`origin/claude/friendly-meitner-lldvar` 의 `litdb/papers/`) 에서만 · 우리 연구실 공저 논문은 출판 (학술지 · DOI) 확인 뒤에만 · 비공개 수치 · 봉인 런 값 · 내부 코드 · 기계 이름 금지.
3. 썸네일 물체는 `avi_thumb.py` 에 그 트랙의 장면 함수를 하나 더 만든다 (남의 이미지 금지).

## 6. 웹앱 영상 섹션 (`/videos`)

- 꾸러미 = `python3 -I scripts/avi_package_episode.py <편 폴더> --id <편 id> -o <편 id>.zip` (내부판이면 `--internal` · 렌더가 리포 밖이면 `--video <mp4>` · 다른 목록을 더 대려면 `--deny-list <리포 밖 목록>`).
- **내부 숫자 목록 (1저자 11-24 Q2)** = 작업 폴더 편 폴더의 internal/ 안 `public_deny_list.txt` (예: ep01 = 작업 폴더 ep01_mixer/internal/ · 리포에는 없다 · 내부판 클립의 화면 숫자 · 한 줄에 하나).  공개판을 꾸릴 때 `<편 폴더>/internal/` 과 `--video` 로 고른 영상 폴더의 `internal/` 에 이 파일이 있으면 **늘** 검사한다 (`--deny-list` 없이도 · 걸리거나 목록이 깨졌으면 꾸러미를 만들지 않는다).  내부판 꾸러미는 검사하지 않는다.  목록 파일은 꾸러미 (역할 밖 · 하위 폴더) 에도 리포 (`.gitignore` 의 `public_deny_list*.txt` · `docs/avi/**/internal/`) 에도 들어가지 않는다 — 내부판 숫자가 바뀌면 AVI 조수가 목록도 같이 고친다.
- **내부판 = 이 컴퓨터에서만 (1저자 11-24 Q1)** — 루프백 · 프록시를 거치지 않은 요청에만 목록 · 화면 · 재생 · 받기 · 자막이 있다.  다른 컴퓨터의 요청에는 등록 안 된 편과 같은 404 (있다는 사실도 흘리지 않는다).
- 등록 = `python3 -I scripts/avi_register_episode.py <편 id>.zip` (자리 = `WEBAPP_VIDEO_FOLDER` · 없으면 `webapp/videos/` · git 밖) 또는 웹앱 `/videos` 의 "꾸러미 올리기" (이 컴퓨터에서만 · 같은 등록 함수).
- 규칙 · 화면 · 공개 / 내부 = 스킬 `.claude/skills/avi-generate/SKILL.md` 의 "웹앱 영상 섹션" 절 · 라이브러리 `webapp/video_library.py` · 시험 `webapp/test_video_page.py`.
