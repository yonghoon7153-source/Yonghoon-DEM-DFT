# AVI 생성 — 연구 트랙 설명 영상 파이프라인 (리포 판)

> 1저자가 "AVI 생성" 이라고 하면 이 폴더와 스킬 (`.claude/skills/avi-generate/SKILL.md`) 의 순서대로 만든다.  트랙마다 독립된 한국어 설명 영상 한 편 (정보 전달 · 진행 보고 아님) · 레퍼런스 = 채널 "데이너스: AX | medical AI" (`@dainus2026`) 11 월 네 편의 양식 (양식만 배운다 — 그 채널의 화면 · 썸네일 · 음악 · 문구는 쓰지 않는다).
> **리포 판 (11-24 · ep01 최종판 글 = 11-25)** — 리포에는 글 · 표 · 도구 · 점검 기록만 둔다 (공개 안전한 것만).  렌더 (mp4) · 음성 (wav) · 점검 그림 · 내부판 · 글꼴 · 레퍼런스 자료 (남의 영상 · 측정 원자료) 는 **리포 밖 작업 폴더**에 둔다 (공개 리포 · 크기).  `.gitignore` 가 `docs/avi/` 아래의 mp4 · wav · qa/ · audio/ · internal/ · fonts/ 를 막는다.
> 웹앱에서 보고 받기 = 영상 섹션 `/videos` (아래 §6 · 스킬의 "웹앱 영상 섹션").

## 0. 정본 순서 (S0–S11 · 1저자 11-25)

> 스킬 `.claude/skills/avi-generate/SKILL.md` 의 "★ AVI 제작 전 과정" 절과 같은 순서다 (단계마다의 세부 · 규칙 = 스킬).  ⚠ **정본 확정 = Codex 반박 리뷰 뒤** — 1저자 11-25 승인 순서: 스킬 정립 → ep01 로 새 단계 한 바퀴 (S3 → S4 → S7 → S8) → Codex 반박 리뷰 요청서 (발송 = 1저자).

| 단계 | 무엇 | 누가 | 넘어가는 조건 | 명령 · 파일 |
|---|---|---|---|---|
| S0 목적 | 트랙 · 대상 · 한 줄 질문 · 공개 허락 (기본 없음) | 본 세션 → 1저자 | 질문 + 공개 범위를 받음 | 편 폴더 brief.md |
| S1 레퍼런스 · 자료 | 레퍼런스 양식 (`docs/video_reference/README.md`) · 화면 · 말 숫자마다 litdb 정본 카드 | 대본 조수 · 본 세션 | 카드 없는 숫자는 뺀다 · 빈 칸은 짐작하지 않고 1저자에게 | 편 폴더 sources.md |
| S2 대본 초안 | 장면 · 말 (읽는 꼴) · 자막 · 쉼 · 화면 · 출처 줄 (귀로 듣는 글) | 대본 조수 | 경고 0 · 철회값 스윕 rc 0 | `build_scenes.py` → `avi.py tts` |
| S3 대본 내부 반박 리뷰 (새 · 1저자 11-25) | 대본을 쓰지 않은 조수가 처음 보는 시청자처럼 차갑게 — 기승전결 지도 (장면 → 이야기 역할) · 갈고리 20–30 s · 질문 하나가 일찍 · 전 (반전 · 긴장) · 결 = 그 질문의 답 · 늘어짐 · 강조 낱말 · 이음 (합치기 / 짧은 쉼 / 다시 쓰기) · 긴 문장 숨 · **전환 판단표** (모든 장면 전환 · 화면 (shot) 전환마다 시각 · 앞뒤 화면 · 그 순간 나레이션 · 판정 = 최적 / 늦음 / 이름 (일찍 넘어감) / 자리 틀림 / 불필요 / 빠짐 · 이유 · 고칠 안 = 자르는 자리의 문장 · 낱말 · 합치기 / 나누기 / 순서) · 지적마다 P1 / P2 / P3 + 구체 다시 쓰기 · 사실 · 숫자 · 출처 · 공개 범위는 그대로 | 독립 리뷰 조수 | 리뷰 파일이 남음 | 편 폴더 review/script_review_rN.md |
| S4 고침 → 짧은 재리뷰 | P1 · P2 고침 → 고친 곳만 재리뷰 | 대본 조수 · 리뷰 조수 | 재리뷰 **P1 0** → ★ 1저자 대본 승인 | `build_scenes.py` |
| S5 무음 미리보기 + 0.5 s 장면 점검 | 0.5 s 간격 전부 + 움직임 10 fps · **전환 판단표를 렌더 시각으로 다시** | 음성 / 렌더 조수 | 장면 점검 걸림 0 | `avi.py render` · `avi.py stills` |
| S6 음성 | voice-auto (문정 · smart · 1.0 · 자동 판단 = 아래 §2 의 '음성 단계 자동 판단') · ★ 새 목소리일 때만 오디션 | 음성 / 렌더 조수 | 종료 코드 0 (2 = 1저자에게) | `avi.py voice-auto` |
| S7 강약 · 이음 점검 | 지금 = 이음매 높이 뜀 ≥ 2.5 반음 · 톤 / 빠르기 / 방식 바뀜 · '…요.' 이어지는 말 끊김 / 다음 판 (만드는 중) = 강조 낱말이 힘을 받았나 · 이어지는 말 사이 쉼 · 긴 문장 숨 | 음성 / 렌더 조수 | 큰 뜀 (≥ 3.5 반음) 0 또는 보고 | `avi.py audio-qc` |
| S8 최종 렌더 + 장면 점검 | 렌더 한 번 (고칠 곳이 나오면 고친 뒤 한 번 더 · ep01 = 2 회) · 0.5 s 전부 + 10 fps 필름 · **전환 판단표를 실제 렌더 시각으로 다시** · 자막 = 실제 음성 시각 · 소리 (−14 LUFS · 최고점 · 끊김) · 공개 안전 (내부 숫자 목록 · 철회값) · 썸네일 · 설명란 | 음성 / 렌더 조수 | 자동 검사 걸림 0 | `avi.py render --out … --audio … --timing …` · `final_check.py` · `avi.py thumb` |
| S9 10 점 기준표 | 점수 · 깎은 이유 (장면 · 시각) · 확인한 것 / 못 한 것 | 조수 · 본 세션 대조 | 정확성 10 · 나머지 ≥ 8 | 편 폴더 rubric |
| S10 /videos 꾸러미 | 공개판 · 내부판 (이 컴퓨터에서만) | 본 세션 | 공개 안전 검사 통과 | 아래 §6 |
| S11 ★ 1저자 듣기 피드백 | `/videos` 에서 듣고 점수 · 번호로 → 바뀐 문장만 다시 (원장이 문맥 해시로 앞뒤까지 잡는다) | 1저자 · 조수 | 1저자 OK → 납품 | `avi.py voice-auto --run` |

- 누가: 백그라운드 조수 셋 (대본 S2 · S4 / 독립 리뷰 S3 · 재리뷰 / 음성 · 렌더 S5–S9 — 규칙대로 스스로 판단 · 끝에 보고) · 본 세션 = 지시 · 결과 대조 · 1저자 전달.  1저자에게 묻는 것 = 결제 · 글자 예산 넘김 (대본 × 3) · 공개 범위 · 뜻이 바뀌는 고침 · 목소리 바꿈 · 길이 (ep01 = 상관없음).

## 1. 폴더

| 자리 | 무엇 |
|---|---|
| `series_plan.md` | 다음 편들 (트랙별 제목 · 한 문단) |
| `tools/` | 파이프라인 코드 (아래 §3) |
| `ep01_mixer/` | 1 편 (믹서) 의 글 자료 — `build_scenes.py` → `scenes.json` → 나머지 전부 · **최종판 (11-25 · 실제 음성 · 렌더 = 리포 밖 `ep01_final.mp4` 9:22.9)** · 기준표 = `ep01_mixer/rubric_ep01_v2.md` · 결정 기록 = `ep01_mixer/DECISIONS.md` (둘 다 공개 사본 — 내부판 절 · 내부판 숫자 · 요금 · 결제 · 글자 예산 수치를 뺐다) |
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
| `script.md` | `avi.py tts` (+ `script_header.md`) | 장면별 대본 · 화면 계획 · 출처 · 챕터 · 참고 문헌 (머리 = `script_header.md` — 고치면 `avi.py tts` 를 다시) |
| `tts_emotion_map.md` | `avi.py typecast` | Typecast 보내는 방식 (smart · 빠르기 1.0) · 감정 → 프리셋 표 (preset 방식 비교용 · 보내지 않음) |
| `ep01.srt` · `timeline.json` | `avi.py plan` (또는 render) | 자막 · 시간표 |
| `thumbnail.png` | `avi.py thumb` | 1280×720 |
| `qc.md` | (사람 + 검사 출력 · 작업 폴더의 make_qc.py) | 최종판 QC — 글꼴 · 색 · 자막 안전 영역 · 숫자 ↔ 출처 대조 (꾸러미의 QC 는 편마다 한 파일 · ep01 리포 사본 = 작업 폴더 qc_final.md) |
| `final_check.md` · `final_check.py` | `python3 -I ep01_mixer/final_check.py` (작업 폴더 · 최종 렌더 뒤) | 영상 ↔ 시간표 ↔ 음성 길이 · 자막 ↔ 실제 음성 · 개체 시각 · 소리 (음량 · 쉼 · 끊김) · 공개 안전 · 첫 · 끝 장면 (작업 폴더 출력 이름 = qc_final_check.md) |
| `qa_frames.py` | (사람이 돌림 · 출력 = qa/ · 리포 밖) | 0.5 s 간격 대조표 · 말하는 중 빈 화면 검사 |
| `DECISIONS.md` | (사람 + `avi.py voice-auto` 한 줄) | 결정 기록 |
| (리포 밖) `preview_silent.mp4` | `avi.py render` | 1920×1080 · 30 fps · H.264 yuv420p · 무음 AAC · `+faststart` · 자막 구워 넣음 |
| (리포 밖) `audio_in/` · `audio/` | `avi.py typecast` · `voice-auto` · `audio-prep` | TTS 음성 파일 (문장마다) · Typecast 원장 · `narration.wav` · `mix.wav` · `timing.json` · `audio_qc.md` · voice-auto 보고 |

## 2. 명령 순서 (한 편 · 단계 이름 = §0)

> 돌리는 자리 = **리포 밖 작업 폴더** (이 폴더의 `tools/` 와 편 폴더를 복사해 간다).  리포 안에서 렌더하면 mp4 · 점검 그림이 작업 트리에 생긴다 (`.gitignore` 가 막지만 자리를 섞지 않는다).  글꼴 = `AVI_FONT_DIR=<Pretendard 폴더>` (없으면 Noto CJK 대체 글꼴 · 글자 폭이 달라 화면 자리가 바뀐다).

1. **대본 · 화면 (S2 → S3 · S4)** — `build_scenes.py` 를 고친다 (말 = `say` 에 읽는 꼴 · 화면 = `text` 와 개체 · 숫자마다 `src(...)` 출처 줄).  `python3 -I ep01_mixer/build_scenes.py` 는 50 음절 넘는 문장 · `say` 안의 기호 · 24 자 넘는 자막 · '처음 / 최초 / 가장 먼저' 를 경고한다.  쓴 뒤 마무리하지 않고 독립 조수가 내부 반박 리뷰 (기승전결 지도 · 전환 판단표 · 편 폴더 review/ · 스킬 §4-1) → 고침 → P1 0 까지 짧은 재리뷰 → ★ 1저자 대본 승인.
2. **무음 미리보기 (S5)** — `python3 -I tools/avi.py render ep01_mixer` → `preview_silent.mp4`.  시간은 말 빠르기 모형 (아래 §4) 으로 잡는다.  장면 사진만 빨리 보려면 `python3 -I tools/avi.py stills ep01_mixer --shots` (장면마다 한 장 → `qa/stills/sheet_*.jpg`).  0.5 s 장면 점검 · 전환 판단표를 렌더 시각으로 다시 (스킬 §8).
3. **목소리 고르기 (S6 · 새 목소리일 때만)** — `voice_audition.txt` 10 줄을 후보 목소리로 생성 → `python3 -I tools/avi.py audio-qc ep01_mixer --wav ep01_mixer/audio_in/audition_<목소리>.wav` 로 빠르기 · 쉼 · 끝 억양을 본다.
4. **TTS 생성 (S6)** — Typecast 에 `tts_typecast.tsv` 의 '문장 (읽는 꼴)' 칸을 한 줄씩 넣고, 줄마다 빠르기 · 쉼 · 감정을 표대로 맞춘다 (감정 프리셋 이름은 목소리마다 다르다 — 가장 가까운 것).  장면 하나를 한 파일로 받는다.  **11-25 부터는 아래 '음성 단계 자동 판단'** (`avi.py voice-auto` 가 Typecast API 로 문장마다 만든다 · 손으로 넣는 이 길은 예비).
5. **음성 넣기 (S6)** — 파일을 `ep01_mixer/audio_in/` 에 넣고 `python3 -I tools/avi.py audio-prep ep01_mixer` → 문장 경계를 찾아 문장 사이 쉼을 표의 값으로 다시 맞추고 (`--keep-pauses` 면 TTS 쉼 그대로) −14 LUFS · 참 최고점 −1.5 dBTP 로 맞춘다.  음악을 쓰면 `--bgm 음악.wav --bgm-lufs -28` (레퍼런스: 목소리가 음악보다 13–14 LU 크고 덕킹 없음).
6. **음성 QC (S7)** — `python3 -I tools/avi.py audio-qc ep01_mixer` → 편 폴더의 audio/audio_qc.md (리포 밖 · 알림이 있으면 그 문장만 다시 생성).
7. **최종 렌더 (S8)** — `python3 -I tools/avi.py render ep01_mixer --out ep01_final.mp4 --audio ep01_mixer/audio/mix.wav --timing ep01_mixer/audio/timing.json` (음악 없으면 `narration.wav`).  자막 · 화면 쌓기가 실제 음성 시간에 다시 맞춰진다.  `ep01.srt` 도 다시 쓴다.  0.5 s 장면 점검 + 10 fps 필름 · 전환 판단표를 실제 렌더 시각으로 다시.
8. **썸네일 (S8)** — `python3 -I tools/avi.py thumb ep01_mixer` (끝 화면의 물체 그림 `assets/powder_obj.png` 도 없으면 함께 만든다 · `--obj` = 다시 만듦 · 그림자는 그림 가장자리 40 px 에서 0 으로 사라지게 해 잘린 선이 안 보인다).
9. **QC · 기준표 (S8 · S9)** — `qc.md` 표를 다시 확인 (숫자 ↔ 출처 · 화면 금지 문장 · 공저 밝힘).  철회값 = `python3 -I tools/ban_sweep_files.py <파일 …>` (리포 `docs/reviews/claims.json` 을 읽기만 · 다른 자리면 `AVI_CLAIMS_JSON`).
10. **웹앱에 넣기 (S10)** — §6.
11. **1저자 듣기 (S11)** — `/videos` 에서 듣고 점수 · 번호로 답 → 바뀐 문장만 `build_scenes.py` 에서 고쳐 `avi.py voice-auto` (원장이 문맥 해시로 그 문장 + 앞뒤까지 다시 만든다 · 멀쩡한 판은 그대로).

### 음성 단계 자동 판단 (`avi.py voice-auto` · 1저자 11-25)

1저자 11-25 *"이런 권고안들은 저절로 판단되게 백그라운드 에이전트로"* — 음성 단계 (TTS → 점검 → 걸린 문장 다시) 는 백그라운드 조수가 규칙대로 스스로 정하고 끝에 한 번 보고한다 (정본 = 스킬 §7-1).  `python3 -I tools/avi.py voice-auto ep01_mixer` = 미리 보기 (API 호출 0 · 파일 안 씀 · 만들 줄 · 글자 · 예산 · 지금 이음매) · `--run` = 실제로 만든다 (`nice -n 19` · 기본 `--rounds 2 --takes 2 --budget-x 3`).  목소리 = Typecast 문정 · **smart** (앞뒤 문장을 같이 보냄) · 빠르기 **1.0** 한 값 · 톤 (프리셋) 을 섞지 않음 · 길이는 상관없음 (대본을 줄이지 않는다) · 원장 (audio_in 의 typecast_ledger.json) 과 안 맞는 줄만 만든다 → audio-prep → audio-qc 의 **이음매 검사** (이웃 문장 높이 차 ≥ 2.5 반음 = 뜀) → **다시 찍기** (뜀마다 이웃에서 더 먼 문장 하나 · 2 판씩 × 2 회 · 지금 판과 새 판 중 이웃 높이에 가장 가까운 판) → 그래도 튀는 문장만 뜻 그대로 끝말을 차분하게 (`build_scenes.py` 의 그 줄 · 조수가 고침 · 명령은 글을 고치지 않는다) 고친 뒤 한 번 더 · 작은 뜀 (< 3.5 반음) 은 그대로.  결제 · 계정 실패 · 글자 예산 넘김 (대본 글자 × 3) · 공개 범위 · 뜻이 바뀌는 고침 · 목소리 바꿈은 멈추고 1저자에게 묻는다 (종료 코드 2).  기록 = 판마다 편 폴더의 audio/voice_auto_report.md (리포 밖) + `DECISIONS.md` 한 줄 — 그 줄에 글자 · 예산 숫자가 들어가므로 리포 공개 사본에서는 뺀다 (ep01 = 뺌).  높이 차는 귀의 대리 지표일 뿐이라 "자연스럽다" 고 쓰지 않는다 (듣기 확인 = 1저자) · 문턱 2.5 · 3.5 반음 = ep01 경험값.  ep01: preset 판 뜀 27 → smart 15 → 다시 찍기 · 끝말 둘 · 마지막 voice-auto = 3 곳 (최대 2.99 반음 · 모두 작은 뜀).

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
| `avi.py` | 명령 진입점 (`plan · stills · render · tts · audio-prep · audio-qc · typecast · voice-auto · thumb · selftest`) · numpy 스레드 1 개 고정 |
| `avi_style.py` | 측정한 색 · 글꼴 (`AVI_FONT_DIR`) · 자막 크기 · 종이 결 배경 |
| `avi_timeline.py` | 문장 → 말 구간 → 자막 구간 → 장면 구간 · 시간 닻 (`LINE~낱말+0.3` 등) · SRT · 그림 개체의 상대 경로를 편 폴더 기준으로 푼다 |
| `avi_render.py` | 개체 (원 · 점 무리 · 글 · 큰 숫자 · 선 · 칠 · 상자 · 사람 · 혼합기 · 묶음 · 그림) → 3 배 초표본 스프라이트 → 프레임 합성 → ffmpeg 파이프 (바뀐 프레임만 새로 그림) |
| `avi_tts.py` | TSV · ElevenLabs · 평문 · SSML · 오디션 · script.md |
| `avi_audio.py` | 음성 받기 · 문장 정렬 (동적 계획법) · 쉼 다시 맞춤 · BS.1770-4 음량 · 참 최고점 제한기 · 음악 섞기 · QC · 합성 시험 |
| `avi_typecast.py` | Typecast 문정 API (smart · 빠르기 1.0) — 문장마다 wav · 원장 (글 · 앞뒤 문장 · 빠르기 · 방식 · 파일 해시) · 다시 찍기 · 내부판 거부 · 키는 세션 프록시가 넣는다 (코드 · 리포에 키 없음) |
| `avi_voice_auto.py` | 음성 단계 자동 판단 (위 '음성 단계 자동 판단' · 스킬 §7-1) — 만들 줄 · 이음매 · 다시 찍기 · 글자 예산 지킴 · 보고 |
| `avi_thumb.py` | 썸네일 (numpy 광선 추적으로 그린 분말 물체 · 부드러운 그림자) |
| `korean_text.py` | 숫자 · 영어를 읽는 꼴로 · 음절 수 |
| `ban_sweep_files.py` | 리포 밖 파일 (대본 · 자막 · 설명란 초안) 의 철회값 스윕 — 리포 `--ban-sweep` 과 같은 등록부 · 같은 정규화 |
| `audio_measure.py` · `ref_*.py` | 레퍼런스 측정 도구 (남의 영상 = 분석용만 · 우리 영상에 쓰지 않음) |

- 움직임 (레퍼런스에서 잰 꼴): `fade` (나타남) · `pop` (작게 시작해 커짐) · `draw` (선 그어짐) · `grow` (막대 자람) · `count` (숫자 세어 올라감 0.9 s · 색 연보라 → 남보라) · 점 무리 `stagger` (0.02–0.04 s 간격) · `moves` (옮겨 감) · 다음 장면에서 `keep` (같은 개체가 새 자리로 미끄러짐 = 레퍼런스의 magic move) · `dim` (흐려져 배경이 됨) · 장면이 바뀌면 남기지 않은 개체는 0.3 s 에 사라진다.  자막은 컷으로 바뀐다.
- 시간 닻: `s03_l05` (문장 시작) · `s03_l05@0.5` (말 구간 절반) · `s03_l05~무게는` (그 낱말을 말하는 때 — 음절 위치로 어림) · `s03_l05$` (문장 끝) · 끝에 `+0.4` / `-0.2` 초.
- 렌더 부하: ffmpeg `-threads 1` 기본 (`--threads` 로 바꿈) · 한 번에 하나만 · 게이트가 도는 기계에서는 `nice -n 19`.  무음 미리보기 8 분 ≈ 10–15 분.
- 시험: `python3 -I tools/avi.py selftest` (합성 음성으로 정렬 ≤ 0.06 s · 쉼 다시 맞춤 · −14 LUFS · 참 최고점 · QC 보고 · 이음매 + Typecast · voice-auto 를 가짜 API 로 — 11-25 PASS 53 · 작업 폴더 · 리포 사본 둘 다 · 네트워크를 끊고 돌려 실제 호출 0) — 산출물은 `tools/` 옆 `selftest/` 에 쓴다 (리포에서는 `.gitignore` · 가짜 API 임시 폴더는 끝에 지운다).

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
