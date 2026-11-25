# GitHub 요즘 뜨는 리포 + 세 분야 성능 도구 조사 (2026-11-25)

> J27 (11-25 밤 · 서브 세션 반입) — 외부 리포 안 파일 경로는 `리포:경로` 꼴로 고쳐 적었다 (이 리포의 경로 검사 `scripts/check_doc_refs.py` 가 리포 안 경로로 읽지 않게 · 받은 글에서 바꾼 것은 이것뿐 · 커밋 축약 다섯은 `docs/reviews/doc_refs_sha_exceptions.tsv`).

## 0. 이번에 한 것 / 하지 않은 것

- **한 것**: ① GitHub trending 대신 "2026-10-25 이후 생긴 리포 · 별 순" + 우리 분야 낱말 검색 (api.github.com 검색 약 70 회, 8 초 간격) ② 1저자 새 지시의 세 분야 (AVI 영상 · 벡터 그림 · 그 밖의 연구) 도구를 이름으로 조회하고 MCP 서버가 있는지 검색 ③ PyPI · npm · crates.io 메타데이터로 라이선스 · 최신판 · wheel 크기 · 무거운 의존성 확인 (설치 없이) ④ 얕은 git clone — 다섯 개는 소스까지 읽고 (3 절), 약 30 개는 README · LICENSE 만 읽음.
- **하지 않은 것**: 받은 코드는 실행 · 설치 · 빌드 0. 리포 안 지시문 (README · SKILL.md · AGENTS.md) 은 자료로만 읽음. 품질 수치 (정확도 · 속도 · 토큰 절감) 는 모두 리포가 쓴 값 [README] 이고 우리가 재지 않았다. 청취 비교도 하지 않았다.
- **접속 한계**: github.com/trending · trendshift · ossinsight = 403. 기사 사이트 (analyticsvidhya.com · dev.to · aitoolly.com) 는 이 세션 네트워크 밖 (이름 풀이 실패) → 검색 결과 요약만 썼다. `repo:terrastruct/d2` 조회는 422 (이 이름의 리포를 찾지 못함 — D2 본 리포 상태 미확인).
- **이 컨테이너** (설치 열의 기준): GPU 없음 · CPU 4 · 메모리 15 GB · **디스크 여유 2.1 GB** · ffmpeg · Node 22.23 · npm · cargo · go · java · docker · pandoc · uv · Python 3.11 있음 · Inkscape · rsvg-convert · tesseract · LaTeX 없음.
- **표지**: [소스] = 읽은 코드 · [README] = 리포 문서 · [검색] = 웹 검색 요약 · [추정] = 내 추론 · [API] = GitHub 검색 API · [레지스트리] = PyPI / npm / crates.io 메타데이터. 별 수 = 2026-11-25 API 값. wheel 크기 = 패키지 파일만 (의존성 · 모델 가중치 제외).
- **라이선스 규칙**: MIT · Apache · BSD = 출처 표기 후 코드 옮김 가능 · GPL · AGPL · LGPL 수정본 배포 = 아이디어만 · 라이선스 없음 = 아이디어만. **코드와 모델 가중치 라이선스가 다른 경우가 많다** (표에 따로 적음).

## 1. 결론 요약 — 분야마다 상위 1–3

| 분야 | 1 위 | 2 위 | 3 위 |
|---|---|---|---|
| AVI · 한국어 로컬 TTS | **Qwen3-TTS** (코드 · 공식 가중치 Apache-2.0, 한국어 화자 Sohee, 0.6B / 1.7B, VoiceDesign · 3 초 복제 · 스트리밍) [README] | **VoxCPM2** (가중치 · 코드 Apache-2.0 "상업 가능", 2B, 30 언어 중 한국어, 48 kHz) [README] | Supertonic 3 (CPU ONNX · 코드 MIT · 가중치 OpenRAIL-M · 원 리포 보관 처리) — MeloTTS 는 한국어 난문장 벤치에서 자모 문장 실패 [README] |
| AVI · 낱말 단위 자막 정렬 | **stable-ts `align()`** (MIT · Whisper 가중치 MIT · faster-whisper 백엔드) | WhisperX (BSD-2 · 언어별 wav2vec2 정렬 모델 — 한국어 모델 가중치 라이선스 따로 확인) | ctc-forced-aligner (BSD-2 · 대본 ↔ 음성 강제 정렬 CLI · 한국어는 로마자 변환 · 기본 MMS 계열 가중치 라이선스 확인 필요 [추정]) |
| AVI · 음량 · 강약 | **ffmpeg-skill `loudness.py` · `check.py`** (MIT · MCP 내장 · 2-pass + linear 판정 + 인코딩 뒤 진피크 재측정) [소스] | ffmpeg-normalize (MIT · CLI · 11-24 갱신) | pyloudnorm (MIT · BS.1770-4 측정만) |
| AVI · 장면 · 그림 애니메이션 · 합성 | **HyperFrames** (Apache-2.0 · HTML → 결정적 MP4 · CLI + 에이전트 스킬 · Node 22 + FFmpeg) [README] | Manim CE (MIT · `manim-mcp-server` MIT 있음) | Motion Canvas (MIT · TS) — Remotion 은 자체 라이선스 (조건부) |
| AVI · 레퍼런스 영상 읽기 · 장면 점검 | **rea-video** (Apache-2.0 · 오프라인 컷 검출 + 크기 맞춘 접촉 시트 + 파일 기반 에이전트 루프) [소스] | claude-video-vision (MIT · MCP 있음 · 로컬 whisper 백엔드) [README] | vibe-knowledge `qa.py` 꼴 (MIT · 시트 · OCR ↔ 사실표 · freezedetect) [소스] |
| 벡터 · 도식 | **draw.io 공식 MCP** (Apache-2.0 · 편집 가능한 `.drawio` → 1저자가 draw.io Desktop 에서 고침 · SVG / PDF) [README] | Mermaid + `mcp-mermaid` (MIT · 로컬 svg / file 출력만 쓸 것) | Typst + `typst-mcp` (Apache-2.0 / MIT · 수식 · 도식 · LaTeX → Typst) |
| 벡터 · 래스터 → 벡터 · SVG 다듬기 | **vtracer** (MIT · wheel 1.3 MB · 의존성 0 · 색 이미지 · 스플라인 · 팔레트 고정) | svgo (MIT · npm) + svgutils (MIT · 패널 붙이기 · 배율 통일) | resvg (Apache / MIT · SVG → PNG 렌더 검사) — potrace 는 GPL (아이디어만) |
| 연구 · PDF 논문 읽기 · 그림 · 표 | **Docling + docling-mcp** (MIT · `local` 변환 모드) [README] | marker (코드 Apache-2.0 · 모델 OpenRAIL-M · CPU 모드 [README 수치]) | MinerU (Apache-2.0 + 추가 조항 — 연구실 사용 가능) / GROBID (참고문헌 TEI · 이번에 리포 미조회) |
| 연구 · 논문 검색 MCP | **paper-search-mcp** (MIT · arXiv · PubMed · Semantic Scholar · Crossref · OpenAlex · CORE …) | arxiv-mcp-server (Apache-2.0 · 원 LaTeX 절 단위 읽기 · BibTeX · 로컬 저장) | zotero-mcp (MIT · 1저자 Zotero 를 쓴다면) |
| 연구 · GPU 희소 풀이 | **AmgX** (BSD-3 · GPU AMG · Python = pyamgx BSD-3, PyPI 없음 → 빌드) [소스 LICENSE] | CuPy (이미 씀 · cg / gmres 있고 AMG 없음) | JAX-AMG (Apache-2.0 · JAX 스택) |
| 연구 · 시뮬레이션 가속 | **Quadrants** (Apache-2.0 · Genesis 의 Taichi 포크 · "원 Taichi 는 더 이상 유지보수되지 않는다" [README]) — 우리 Taichi MPM 의 위험 신호 | NVIDIA Warp (Apache-2.0 · wheel 149 MB) | DEM-Engine v3 (GPU DEM · 사용자 접촉 모델 · C++ / Python) [README] |
| 연구 · SEM 이미지 분할 | **micro-sam** (MIT · SAM2 기반 · napari 플러그인 · 미세 조정 · PyPI 2.0.1) | napari-mcp (BSD-3 · Royer lab) / Fiji-ImageJ MCP (BSD-3 · 별 6) | Maskbolt (MIT · Rust 한 파일 · CPU SAM · MCP · SVG 외곽선 — 별 0 · 새 계정) |
| 리뷰 · 검사 게이트 (trending) | **code-review-gate-skill** 꼴 (MIT · 스냅샷 핀 · 증거 필수 · 스크립트 집계) [소스] | Jane Street `socratic-tutor` (MIT · 발표 질의응답 연습) | codegraph (MIT · 코드 그래프 MCP — 설치기가 CLAUDE.md · 권한을 고침 → 그대로는 안 됨) |

## 2. 후보 표

열: 리포 · 별 · 라이선스 · 무엇 · 우리 쓰임새 · 판정 (가져옴 / 아이디어만 / 건너뜀) · **MCP 꼴** (있음 / 감쌀 수 있음 / 안 됨) · **이 컨테이너 설치** · **1저자 PC (Windows · WSL)** · 근거.

### 2-A. trending (2026-10 이후 생기거나 크게 뜬 것)

| 리포 | 별 | 라이선스 | 무엇 | 우리 쓰임새 | 판정 | MCP 꼴 | 이 컨테이너 설치 | 1저자 PC | 근거 |
|---|---|---|---|---|---|---|---|---|---|
| JuneYaooo/rea-video | 13,164 | Apache-2.0 | 영상 샷 단위 역분석 (컷 · 접촉 시트 · OCR 자막 · ASR · 말 속도) | AVI S1 레퍼런스 실측 · S6 / S9 장면 점검 | **가져옴** (일부 이식) | 감쌀 수 있음 (CLI + 파일 기반 대기 루프) | pip (numpy · opencv-headless · onnxruntime) · ONNX 모델 첫 실행 약 0.4 GB → 디스크 빠듯 | Windows · WSL 모두 (ffmpeg 필요) | [API] s07 · s21 · [소스] |
| kajisho5/ffmpeg-skill | 10,879 | MIT | ffmpeg 도구 42 개 · `--json` · 스스로 검증 · 플랫폼 규격 검사 | AVI 음량 · 규격 검사 · 자막 줄바꿈 · 시트 | **가져옴** (함수 이식) | **있음** (내장 MCP) | 순수 Python + ffmpeg (있음) — 가능 | 가능 (ffmpeg) | [API] s07 · [소스] |
| andyhuo520/vibe-knowledge | 814 | MIT | 출처 달린 해설 숏 (사실표 → 반박 리뷰 → 음성 → 코드 렌더 → QA) | AVI 사실표 꼴 · `qa.py` 다섯 항목 | **가져옴** (꼴 · qa) | 감쌀 수 있음 | qa 는 Python + ffmpeg — 가능 (OCR 만 교체) | 가능 (macOS Vision 부분 제외) | [API] s01 · [소스] |
| neosapience/typecast-autotag | 6 | MIT | Typecast 쪽 TTS 읽기 정규화 (숫자 · 날짜 · 단위 → 한글) | AVI S7 음성 직전 정규화 · 대본 숫자 점검 | **가져옴** | 감쌀 수 있음 | npm (의존성 0) 권장 · pip 판은 미리 빌드한 `.so` | 가능 (Node 또는 Python ≥ 3.11) | [API] s05 · [소스] |
| kyy-logs/code-review-gate-skill | 519 | MIT | 독립 탐침 4 개 · 증거 필수 · 스냅샷 핀 · 스크립트 집계 리뷰 게이트 | 내부 반박 리뷰 skill 개정 | **가져옴** (꼴만 · 새로 짬) | 안 됨 (skill + 스크립트 · MCP 불필요) | Bash · Git · Python 3.9 + PyYAML — 가능 | 가능 (Git Bash · WSL) | [API] s04 · [소스] |
| jamiepine/voicebox | 61,290 | MIT | 로컬 음성 스튜디오 (TTS 엔진 8: Qwen3-TTS · Chatterbox 다국어 …) · 받아쓰기 | 1저자가 목소리를 듣고 고르는 데스크톱 도구 | 아이디어만 | 있음 (README: 에이전트가 MCP 로 호출) | 데스크톱 앱 — 컨테이너 해당 없음 | Windows 앱 (GPU 있으면 빠름) [추정] | [API] t02 · [README] |
| colbymchenry/codegraph | 78,652 | MIT | 미리 색인한 코드 그래프 MCP (파일 읽기 0 · 토큰 62 % 절감 주장) | 큰 리포 탐색 토큰 절감 | 아이디어만 | 있음 — 단 설치기가 CLAUDE.md 에 구역을 쓰고 자동 허용 권한을 넣음 | 프로젝트 안에 `.codegraph/` 를 만든다 → 우리 리포 쓰기 0 규칙 · 게이트와 충돌 | 같음 (`--no-permissions` · 수동 설정이면 검토 가능) | [API] t06 · [README] |
| EL4CTEO/fast-anything | 3,766 | MIT | 느린 5 % 함수만 Rust 로 · 기록한 실제 호출 500 개 + 경계값 (NaN · ±inf · −0.0) 으로 같은 답 증명 | "비트 같음" 증명 꼴 · 전처리 속도 | 아이디어만 (봉인 코드라 이식 안 함) | 있음 (바이너리 내장 MCP · 도구 8) | npm 또는 cargo + Rust 툴체인 | 가능 | [API] trend · [README] |
| janestreet/agent_skills | 11,695 | MIT | `socratic-tutor` skill 하나 (진단 · 0–5 단계 · 한 번에 한 질문 · 반복 복습) | 세미나 · 발표 질의응답 연습 | 아이디어만 (그대로 써도 됨) | 안 됨 (skill 문서) | 문서뿐 | 문서뿐 | [API] s21 · [소스] |
| addyosmani/agent-skills | 120,306 | MIT | 실무 엔지니어링 skill 묶음 (11-11 trending 감시에 잡힘) | 리뷰 · 시험 습관 비교 | 아이디어만 (안 읽음) | 안 됨 (skill) | 문서 | 문서 | [검색] · [API] t06 |
| mattpocock/skills · obra/superpowers | 332,516 · 326,160 | MIT · MIT | skill 모음 · 방법론 (superpowers 는 규율 ② 로 이미 채택) | 비교용 | 건너뜀 (이미 씀 / 안 읽음) | 안 됨 | 문서 | 문서 | [API] t06 · CLAUDE.md |
| morluto/rea | 477,720 | MIT | "무엇이든 역설계" (rea-video 의 원형) | 이번 조사 방법 비교 | 아이디어만 (안 읽음) | 안 됨 | — | — | [API] t06 |
| storytold/craft-anything | 43,136 | Apache-2.0 | 소프트웨어 작동 이해 · 만들기 (PhotoCraft 와 같은 조직) | 다른 조수 담당 범위와 겹칠 수 있음 | 건너뜀 | — | — | — | [API] s21 |
| ersinkoc/AI-Video-Factory | 699 | MIT | 주제 → 다국어 유튜브 영상 (Claude 에이전트) | AVI 흐름 비교 | 아이디어만 (안 읽음) | 감쌀 수 있음 | — | — | [API] s03 |
| LaplacianAI/manimvox | 7 | MIT | 조사 · 출처 단 대본 · Manim · 내레이션 | AVI 출처 줄 비교 | 아이디어만 (안 읽음) | 감쌀 수 있음 | — | — | [API] s08 |
| iamajmeena/neonclipping | 2,546 | AGPL-3.0 | 링크 → 자막 단 9:16 클립 | 자막 자동화 | 아이디어만 (AGPL) | — | — | — | [API] trend |
| chutingyean/Agent-Cockpit | 524 | AGPL-3.0 | 연구 에이전트 근거 사슬 화이트보드 + MCP (주장 → 원자료) | litdb 카드 · 원고 근거 추적 | 아이디어만 (AGPL) | 있음 | — | — | [API] s02 |
| Alto-R/nature-figure-craft · lgwrightlab/schematic-figure | 238 · 218 | MIT · MIT | 논문 그림 skill · 벡터 코드로 개념도 | 그림 원칙 · Figure 1 개념도 비교 | 아이디어만 (안 읽음) | 안 됨 (skill) | — | — | [API] s10 |
| leeandev/stop-slop-ko · hyeonsang010716/OpenDocKit | 84 · 49 | MIT · MIT | 한국어 문서 "AI 티" 걷기 skill · PDF / Office / **HWP · HWPX** → Markdown | 주간보고 문장 · 한글 문서 읽기 | 아이디어만 | 안 됨 / 감쌀 수 있음 | — | — | [API] s19 |
| Yihao-Shi/GeoTaichi | 278 | GPL-3.0 | Taichi DEM / MPM / 결합 시뮬레이터 | [DEM 우선 (수영)] 재설계 참고 | 아이디어만 (GPL) | 안 됨 | — | — | [API] s22 |

### 2-B. 세 분야 도구 (1저자 새 지시)

| 분야 | 리포 | 별 | 라이선스 (코드 / 가중치) | 무엇 | 판정 | MCP 꼴 | 이 컨테이너 설치 | 1저자 PC | 근거 |
|---|---|---|---|---|---|---|---|---|---|
| TTS | QwenLM/Qwen3-TTS | 14,637 | Apache-2.0 / 공식 가중치 Apache-2.0 | 10 언어 (한국어) · CustomVoice 화자 9 (한국어 Sohee) · VoiceDesign · 3 초 복제 · 스트리밍 | **가져옴 (시험 후보 1)** | 감쌀 수 있음 (`generate_custom_voice`) | `pip qwen-tts` 0.1 MB + torch · torchaudio · transformers · accelerate · onnxruntime · librosa, 가중치 0.6B / 1.7B → **GPU 없음 · 디스크 2.1 GB 라 불가** | WSL + CUDA GPU 권장 (FlashAttention 2 권장 [README]) | [API] t02 · [README] · [레지스트리] · korean-tts-bench [README] |
| TTS | OpenBMB/VoxCPM (VoxCPM2) | 42,972 | Apache-2.0 / Apache-2.0 ("상업 가능") | 2B · 30 언어 (한국어) · 48 kHz · VoiceDesign · 복제 · RTF ≈ 0.3 (RTX 4090) | **가져옴 (시험 후보 2)** | 감쌀 수 있음 (Python · vLLM-Omni OpenAI 호환 API) | `pip voxcpm` 0.1 MB + torch · modelscope … → 불가 (GPU) | WSL + CUDA GPU | [API] t06 · [README] · [레지스트리] |
| TTS | supertone-oss-archive/supertonic | 13,761 | MIT / OpenRAIL-M (용도 제한 · 합성물 표시) | ONNX 온디바이스 TTS · v3 = 31 언어 (한국어) · 약 99M | 아이디어만 (CPU 대안 · 원 리포 보관) | 감쌀 수 있음 | `pip supertonic` (onnxruntime 만) — 가능하지만 가중치 다운로드 필요 | Windows CPU 가능 | [API] t01 · [검색] · korean-tts-bench [README] |
| TTS | resemble-ai/chatterbox | 28,095 | MIT / 가중치 미확인 | Multilingual V3 0.5B · 23+ 언어 (한국어) · 모든 출력에 PerTh 워터마크 | 아이디어만 (보관 · 지원 없음) | 감쌀 수 있음 | pip + torch → 불가 (GPU) | WSL + GPU | [API] r01 · [README] |
| TTS | june-oh/korean-tts-bench | 0 | 없음 | 한국어 난문장 16 개 (수사 · 날짜 · 금액 · 분수 · 받침 · 자모 · 영문 · 억양) 청취 비교 · MeloTTS 자모 문장 KeyError | 아이디어만 (시험 문장 꼴) | — | — | — | [API] s05 · [README] |
| 정렬 | jianfch/stable-ts | 2,290 | MIT / Whisper MIT | Whisper 로 대본 ↔ 음성 정렬 (`align`) · 낱말 시간 · faster-whisper 백엔드 | **가져옴** | 감쌀 수 있음 | sdist (순수) + torch · torchaudio 또는 faster-whisper (ctranslate2) → CPU 로도 돌 것 [추정] · 디스크 빠듯 | 가능 (GPU 면 빠름 [추정]) | [API] r02 · [README] · [레지스트리] |
| 정렬 | m-bain/whisperX | 25,661 | BSD-2 / 언어별 정렬 모델 따로 | 단어 시간 (wav2vec2 강제 정렬) · 화자 분리 (HF 토큰 필요) | 아이디어만 (2 순위) | 감쌀 수 있음 | wheel 16.5 MB + torch · torchvision · transformers · ctranslate2 · triton → 무거움 | WSL + GPU | [API] r02 · [README] · [레지스트리] |
| 정렬 | MahmoudAshraf97/ctc-forced-aligner | 578 | BSD-2 / 기본 MMS 계열 [추정 비상업 · 확인 필요] | 대본 ↔ 음성 강제 정렬 CLI · 1,100+ 언어 · 한국어는 `--romanize` | 아이디어만 (가중치 확인 뒤) | 감쌀 수 있음 (CLI) | git 설치 (PyPI wheel 없음) · onnxruntime · librosa | 빌드 필요할 수 있음 [추정] | [API] r02 · [README] |
| 정렬 | linto-ai/whisper-timestamped | 2,859 | AGPL-3.0 | 낱말 시간 + 신뢰도 | 건너뜀 (AGPL) | — | — | — | [API] r02 |
| 음량 | slhck/ffmpeg-normalize | 1,545 | MIT (PyPI) | EBU R128 / RMS / 피크 정규화 CLI · 일괄 | 아이디어만 (ffmpeg-skill 로직이 더 엄격) | 감쌀 수 있음 | pip 0.1 MB + ffmpeg (있음) — 가능 | 가능 | [API] r04 · [레지스트리] |
| 음량 | csteinmetz1/pyloudnorm | 796 | MIT | BS.1770-4 음량 측정 (LUFS) | 가져옴 (점검용 측정) | 감쌀 수 있음 | pip 수 KB (numpy · scipy) — 가능 | 가능 | [API] r04 · [레지스트리] |
| 애니메이션 · 합성 | heygen-com/hyperframes | 89,815 | Apache-2.0 | HTML · CSS · JS · 탐색 가능한 애니메이션 → 결정적 MP4 (헤드리스 Chrome 이 프레임마다 찍고 FFmpeg 인코딩) · `/slideshow` · `/reverse-any-video` 스킬 | **가져옴 (시범)** | 감쌀 수 있음 (로컬 CLI `npx hyperframes render`) · 호스팅 커넥터는 외부 (베타) | Node 22 (있음) + FFmpeg (있음) + 헤드리스 Chrome 다운로드 [추정 수백 MB] → 디스크 빠듯 | Windows 가능 (Node 22 · FFmpeg) | [API] r04 · [README] |
| 애니메이션 | ManimCommunity/manim (+ abhiemj/manim-mcp-server) | 42,887 (+ 664) | MIT (+ MIT) | 수식 · 도식 애니메이션 | 가져옴 (수식 장면) | **있음** (manim-mcp-server, 2025-05 뒤 멈춤 · 임의 Python 실행) | pip 0.7 MB (Python ≥ 3.11) + cairo · pango 시스템 라이브러리 [추정] · LaTeX (없음) | Windows 가능 (MiKTeX 선택) | [API] r03 · m01 · [README] · [레지스트리] |
| 애니메이션 | motion-canvas/motion-canvas | 20,219 | MIT | TS 코드 애니메이션 · 편집기 미리보기 | 아이디어만 (HyperFrames 와 겹침) | 감쌀 수 있음 [추정] | npm 0.9 MB (+ vite) | 가능 | [API] r03 · [레지스트리] |
| 애니메이션 | remotion-dev/remotion | 75,581 | 자체 라이선스 (NOASSERTION · "SEE LICENSE IN LICENSE.md") | React 로 영상 | 건너뜀 (라이선스 조건 확인 전) | 감쌀 수 있음 | npm 2.2 MB + Chrome | 가능 | [API] r03 · [레지스트리] |
| 합성 | Zulko/moviepy · PyAV-Org/PyAV | 15,202 · 3,348 | MIT · BSD-3 | 파이썬 영상 편집 · FFmpeg 바인딩 | 기존 도구 유지 | 감쌀 수 있음 | moviepy 작음 · av 19 = wheel 39.5 MB · **Python ≥ 3.12** | 가능 | [API] r03 · [레지스트리] |
| 영상 보기 | jordanrendric/claude-video-vision | 1,536 | MIT | ffmpeg 프레임 + 음성 전사 (Gemini / 로컬 whisper / OpenAI) 를 Claude 에 넘김 · YouTube URL (yt-dlp) | 아이디어만 (rea-video 와 겹침) | **있음** (npx) | npm + whisper.cpp 또는 openai-whisper | 가능 | [API] m03 · [README] |
| 도식 | jgraph/drawio-mcp | 5,898 | Apache-2.0 | 공식 draw.io MCP: 호스팅 앱 서버 · 로컬 도구 서버 (npm) · 플러그인 (`.drawio` 생성, PNG / SVG / PDF 는 draw.io Desktop) · XML · CSV · Mermaid | **가져옴 (시범)** | **있음** | npm — `.drawio` XML 생성은 가능 · 내보내기는 Desktop 필요 (컨테이너에 GUI 없음) | **잘 맞음** (Windows draw.io Desktop 에서 바로 편집) | [API] f04 · [README] |
| 도식 | mermaid-js/mermaid (+ hustcc/mcp-mermaid) | 91,243 (+ 653) | MIT (+ MIT) | 글 → 흐름도 · 순서도 | 가져옴 (간단 도식) | **있음** — `svg_url` · `png_url` 출력은 외부 렌더로 보일 수 있음 [추정] → `svg` · `file` 만 | mermaid-cli npm 0.1 MB + 헤드리스 Chromium [추정 수백 MB] | 가능 | [API] r05 · m04 · [README] · [레지스트리] |
| 도식 | typst/typst (+ johannesbrandenburger/typst-mcp · cetz-package/cetz) | 57,414 (+ 187 · 1,879) | Apache-2.0 (+ MIT · cetz LGPL-3.0) | 조판 · 수식 · cetz 그리기 · SVG / PDF / PNG · MCP = 문서 조회 · LaTeX → Typst (Pandoc) · 문법 검사 · PNG 렌더 | 가져옴 (수식 · 표 · 도식) | **있음** | `pip typst` wheel 35.8 MB (의존성 0) — 가능 · pandoc 있음 | Windows wheel 29.6 MB | [API] r05 · m06 · [README] · [레지스트리] |
| 도식 | i2y/d2mcp (D2) | 34 | MIT (D2 본체 상태 미확인) | D2 렌더 · SVG / PNG / PDF (PNG · PDF 는 rsvg-convert) | 건너뜀 (본 리포 미확인) | 있음 | go install (go 있음) · rsvg-convert 없음 | 가능 | [API] m05 · [README] |
| 래스터 → 벡터 | visioncortex/vtracer | 7,602 | MIT (crate: MIT OR Apache-2.0) | 색 이미지 벡터화 · 스플라인 / 다각형 · 팔레트 고정 · potrace 보다 빠른 선형 흐름 | **가져옴** | 감쌀 수 있음 (함수 하나) | `pip vtracer` wheel 1.3 MB · 의존성 0 — **가능** | Windows wheel 0.8 MB | [API] r05 · [README] · [레지스트리] |
| SVG | svg/svgo | 22,837 | MIT | SVG 최적화 CLI | 가져옴 | 감쌀 수 있음 | npm 1.5 MB — 가능 | 가능 | [API] r06 · [레지스트리] |
| SVG | btel/svg_utils (svgutils) · mathandy/svgpathtools | 336 · 642 | MIT · MIT | SVG 패널 조립 · 크기 맞춤 / 경로 다루기 | 가져옴 (그림 패널 규칙) | 감쌀 수 있음 | pip 수십 KB — 가능 | 가능 | [API] r06 · [레지스트리] |
| SVG | linebender/resvg | 4,217 | Apache-2.0 (crate: Apache OR MIT) | SVG → PNG 정확한 렌더 (검사 · 미리보기) | 가져옴 | 감쌀 수 있음 | `pip resvg-py` 1.6 MB 또는 cargo — 가능 | 가능 | [API] r06 · [레지스트리] |
| SVG | Kozea/CairoSVG · scour-project/scour · googlefonts/picosvg | 959 · 879 · 223 | LGPL-3.0 · Apache-2.0 · Apache-2.0 | SVG 변환 · 다듬기 (scour 2024-08 뒤 멈춤) | 아이디어만 | 감쌀 수 있음 | CairoSVG 는 libcairo 필요 | 가능 | [API] r06 · [레지스트리] |
| 논문 그림 | llmsresearch/paperbanana | 2,511 | MIT | 글 → 논문 도식 · 통계 그림 (다중 에이전트 · 비평 반복) · CLI / Python / MCP | 아이디어만 (클라우드 VLM · 이미지 API 필요 → 미공개 자료가 밖으로 나감) | 있음 | pip + API 키 | 가능 (키 필요) | [API] m09 · [README] |
| PDF | docling-project/docling (+ docling-mcp) | 71,013 (+ 804) | MIT (+ MIT) | PDF → 구조 문서 · 그림 · 표 · 캡션 · `local` / `remote` 변환 모드 | **가져옴 (litdb)** | **있음** | pip (docling 2.152 은 의존성 1 개뿐인 메타 패키지로 보임 [추정] · 레이아웃 · 표 모델 첫 실행 다운로드 [추정 수백 MB]) → 디스크 빠듯 | 가능 (CPU 도 됨) | [API] r08 · [README] · [레지스트리] |
| PDF | datalab-to/marker | 41,069 | Apache-2.0 / 모델 OpenRAIL-M | PDF → Markdown · JSON · CPU `fast` 모드 (약 18 MB ONNX) · 점수 71.0 대 docling 67.5 [README 주장] | 가져옴 (2 순위 · 비교 시험) | 감쌀 수 있음 (CLI) | pip 0.2 MB + torch · onnxruntime | 가능 | [API] r08 · [README] · [레지스트리] |
| PDF | opendatalab/MinerU | 84,316 | Apache-2.0 + 추가 조항 (월 사용자 1 억 · 매출 2 천만 달러 넘으면 별도 · 온라인 서비스면 표시) | PDF · Office → Markdown / JSON · CPU 추론 기본 | 아이디어만 (3 순위) | 감쌀 수 있음 [MCP 여부 미확인] | pip 4.0 MB + 의존성 41 · 모델 다운로드 → 불가 (디스크) | 가능 (Windows CPU) | [API] r08 · [README] · LICENSE |
| PDF | allenai/pdffigures2 · pymupdf/PyMuPDF | 765 · 11,193 | Apache-2.0 · AGPL-3.0 | 그림 · 표 · 캡션 추출 (Scala, 2024 뒤 멈춤) · PDF 엔진 | 아이디어만 · 건너뜀 (AGPL) | — | — | — | [API] r08 · r09 |
| 논문 검색 | openags/paper-search-mcp | 3,160 | MIT | 여러 출처 동시 검색 · 중복 제거 · 오픈 액세스 PDF 받기 · 키 선택 | **가져옴** | **있음** | pip 0.1 MB — 설치 가능하나 이 컨테이너 네트워크가 외부 API 를 막을 수 있음 [추정] | **잘 맞음** | [API] r10 · [README] · [레지스트리] |
| 논문 검색 | blazickjp/arxiv-mcp-server | 3,299 | Apache-2.0 | 원 LaTeX 절 단위 읽기 · BibTeX · 주제 감시 · 논문은 디스크 (`~/.arxiv-mcp-server/papers`) | 가져옴 | **있음** | pip 0.1 MB (Python ≥ 3.11) — 네트워크 같음 | 가능 | [API] r10 · [README] · [레지스트리] |
| 논문 검색 | 54yyyu/zotero-mcp · zongmin-yu/semantic-scholar-fastmcp | 6,055 · 166 | MIT · MIT | Zotero 서재 연결 · Semantic Scholar API (인용 · 추천) | 아이디어만 (쓰는지 1저자) | 있음 | pip 작음 | 가능 | [API] r10 · m08 · [README] |
| GPU 풀이 | NVIDIA/AMGX (+ shwina/pyamgx) | 709 (+ 73) | BSD-3 (+ BSD-3) | GPU AMG + Krylov · Python 바인딩 (2024-09 뒤 멈춤) | 아이디어만 (Rint ② 다음 세대 전처리 후보 · 봉인 뒤) | 안 됨 (계산 라이브러리 — MCP 이득 없음) | CMake + CUDA Toolkit 빌드 · PyPI 없음 → 불가 | WSL + CUDA 빌드 | [API] r11 · [소스] LICENSES · [README] · [레지스트리] |
| GPU 풀이 | jx-wang-s-group/JAX-AMG · NVIDIA/nvmath-python · cupy/cupy | 60 · 603 · 12,414 | Apache-2.0 · Apache-2.0 · MIT | JAX GPU AMG · NVIDIA 수학 라이브러리 (README 는 행렬곱 · FFT 중심) · NumPy / SciPy for GPU | 아이디어만 · 건너뜀 · 기존 유지 | 안 됨 | cupy wheel 136.6 MB · nvmath 5.7 MB | 가능 | [API] s13 · r11 · [README] · [레지스트리] |
| 가속 | Genesis-Embodied-AI/quadrants | 242 | Apache-2.0 | Taichi 포크 (2025-06) · Python → CUDA / Vulkan / Metal 커널 · "원 Taichi 는 유지보수 중단" | **위험 기록 + 이주 후보** (지금 바꾸지 않음) | 안 됨 | 설치 방법 미확인 | 미확인 | [API] g03 · [README] |
| 가속 | NVIDIA/warp | 7,350 | Apache-2.0 | GPU 시뮬레이션 커널 (Python) | 아이디어만 | 안 됨 | wheel 149.3 MB → 디스크 빠듯 | Windows wheel 134.9 MB | [API] r11 · [레지스트리] |
| 가속 | projectchrono/DEM-Engine | 139 | BSD 계열 [추정 · LICENSE 첫 줄만 봄] | GPU DEM v3 (GPU 1–2 장 · 클럼프 · 메시 · 사용자 접촉 모델 · C++ / Python) | 아이디어만 ([DEM 우선 (수영)] 비교 후보) | 안 됨 | CUDA 필요 → 불가 | WSL + CUDA | [API] r12 · [README] |
| SEM 분할 | computational-cell-analytics/micro-sam | 781 | MIT / 기반 SAM2 = Apache-2.0 · micro-sam2 가중치 미확인 | SAM2 기반 현미경 분할 · 추적 · napari 플러그인 · 미세 조정 | **가져옴 (시범)** | 감쌀 수 있음 · napari-mcp 와 함께 | pip 0.7 MB + torch · torchvision · transformers (의존성 40) → 불가 (디스크) | conda-forge 권장 · Windows 가능 | [API] s18 · [README] · [레지스트리] |
| SEM 분할 | royerlab/napari-mcp · surajinacademia/Fiji_imageJ_mcp | 47 · 6 | BSD-3 · BSD-3 | napari 화면 조작 MCP · Fiji / ImageJ 분석 MCP | 아이디어만 | **있음** | GUI 필요 → 컨테이너 해당 없음 | Windows 가능 | [API] f02 · f03 |
| SEM 분할 | skulitom/Maskbolt | 0 | MIT | Rust 한 파일 · CPU SAM · MCP + CLI · 번호 미리보기 · 마스크 / SVG 외곽선 | 아이디어만 (별 0 · 새 계정 · 생긴 지 한 달) | **있음** | cargo 빌드 + SAM ONNX 모델 다운로드 | 가능 [추정] | [API] f09 · [README] |
| SEM 분할 | facebookresearch/sam2 · sam3 · MouseLand/cellpose | 20,229 · 12,401 · 2,458 | Apache-2.0 · 자체 SAM 라이선스 · BSD-3 | 범용 분할 모델 · 세포 분할 | 기반 모델 (직접은 안 씀) | 감쌀 수 있음 | torch | 가능 | [API] r13 |

### 2-C. 뺀 것 (위험 신호 · 사유만)

| 리포 (묶음) | 사유 |
|---|---|
| Hut-hzf/ung220z-tool | 공유기 자격 증명 추출 도구 |
| Blender AI copilot 묶음 9 개 (`credoksopho1984/…` · `tiobeharxi1987/…` · `Doug-218/…` 등, 2026-11-12 같은 날 생성 · 별 약 500 씩 · 연도 붙은 새 계정) | 별 조작 · 악성 배포 의심 |
| "Office Docs Suite … portable build for Windows" 3 개 (`MohammedPhan34` · `BiluqaTezi5` · `RediliXum16`, 2026-11-24 같은 날 · 같은 설명) | 바이너리 배포 미끼 꼴 |
| "Free … for Windows 10/11" 류 (clipboard-history-manager · steam-achievement-manager · offline-file-converter · bear-notes · Audio-Loudness-Normalizer-Batcher …) | 새 계정 · 바이너리 미끼 꼴 |
| duwqijlk/muse-protocol · AFK-surf/xnulinux · Vincentwei1021/anything2explainer · lemomo-ai/lemo-opuscar | 라이선스 NOASSERTION (가입 우회 프로토콜 · 커널 모듈 · 해설 영상 skill · 영상 스타일) |
| fishaudio/fish-speech · index-tts/index-tts · microsoft/VibeVoice (TTS) | 가중치 라이선스 불명 / 자체 · VibeVoice-TTS-1.5B 는 README 에 "Disabled" |
| 게임 · 에뮬레이터 (VIctory · xcl · Lichii · totk-pc-recomp …) | 우리와 무관 · 불법 복제 소지 |
| danielsimonjr/upmath-mcp · HyperFrames cloud render / share · draw.io 호스팅 앱 서버 · mcp-mermaid URL 출력 | 그림 · 대본이 외부 서버로 나감 — 미공개 자료에는 쓰지 않음 |

검토만 하고 표에 넣지 않은 것: QwenAudio/CosyVoice (Apache-2.0 · 24,501 · 2026-05 뒤 갱신 없음 · 이번에 안 읽음) · SWivid/F5-TTS (코드 MIT · 가중치 비상업 [추정]) · krafton-ai/RAON-OpenTTS ([검색] · 미조회) · SYSTRAN/faster-whisper (MIT · 27,004) · ggml-org/whisper.cpp (MIT · 55,505) · Montreal-Forced-Aligner (MIT · 1,920) · excalidraw-mcp (라이선스 None) · yctimlin/mcp_excalidraw (MIT · 2,687) · icebird1998/drawio-scientific-illustrator (MIT · 1,475 · 옛 판 → scientific-illustrator 로 옮김 · Windows 에서 시험한 draw.io 실시간 MCP) · storytold/vectorcraft (Apache-2.0 · PhotoCraft 와 같은 조직) · joanrod/star-vector · OmniSVG (Apache-2.0 · AI 벡터화 · GPU) · PaddleOCR (Apache-2.0 · 한국어 OCR) · DeepSeek-OCR (MIT) · olmOCR (Apache-2.0 · GPU 7B) · pdfplumber (MIT) · Genesis (`genesis-world` 1.5.0 · wheel 83 MB · 본 리포는 이번 검색에 안 잡힘) · projectchrono/chrono (BSD-3) · ginkgo (BSD-3) · napari (BSD-3).

## 3. 상위 후보 역설계 (코드를 읽은 다섯)

받은 리포는 실행 · 설치 · 빌드하지 않았다. 리포 안 README · SKILL.md · AGENTS.md 의 지시문은 자료로만 읽었다. 커밋은 `clone_log.txt` 에 적었다.

### 3-1. JuneYaooo/rea-video — 레퍼런스 영상을 "볼 수 있게" 만드는 도구 (Apache-2.0 · 별 13,164 · 커밋 `c11f1bd8` 2026-11-25)

**무엇** [README] 영상 하나를 샷 단위로 쪼개 "실사 / AI 생성 / 코드 렌더 / 혼합" 을 판정하고 다시 만드는 계획을 낸다. 비전 모델 API 없이도 돈다 (ffmpeg + Python 3.10). 이미지를 읽을 수 있는 에이전트가 애매한 샷을 접촉 시트로 본다.

**어떻게 작동하나** [소스]
- 흐름 = `rea_video/pipeline.py: decompose()` — `video_info` → `build_track` → `detect_shots` → (선택) `survey.run` → 소리 분석 · 음원 분리 (백그라운드) → 프레임 일괄 디코드 → 자막 층 (OCR) → 샷마다 특징 → `finalize` → `report.html` + `VIDEO.md`.
- **컷 검출** `rea-video:rea_video/shots.py`: 모든 프레임을 폭 96 px 회색 썸네일로 줄이고 HSV 히스토그램 (16×4×4) Bhattacharyya 거리 · 픽셀 차 평균 · 바뀐 픽셀 비율을 낸다. 점수 = 0.6·히스토그램 + 0.4·clip(4·픽셀차). 0.5 초 창의 국소 중앙값을 바닥으로 삼아
  - 하드 컷: 점수 > 0.30 ∧ 점수 > 2.5·바닥 + 0.06 ∧ 바뀐 비율 > 0.25,
  - **"still swap"** (슬라이드식 영상): 앞 3 프레임이 픽셀까지 같고 (차 < 1e-3) 히스토그램이 > 0.25 뛰면 컷 — 우리 PIL 슬라이드 영상과 같은 꼴,
  - 섬광 · 1–2 프레임 글리치 되돌림은 컷 아님, 점프 컷 · 페이드 (밝기 < min(10, 0.35·중앙값) 또는 > 248, 평평한 프레임, ≤ 2.5 초) · 디졸브 (i 프레임 = i−k, i+k 의 선형 섞임) · 와이프 (6×8 블록 격자).
- **접촉 시트 설문** `rea-video:rea_video/survey.py` (핵심 아이디어):
  - 시트 한 장 = 모델이 줄이지 않고 읽는 크기 (긴 변 1568 px · 약 1.15 MP). 이미지 비용 ≈ 픽셀 수라 **타일 크기가 비용을 정한다**.
  - 1 회차 개관: 타일 120×68, 최대 240 장, 절반은 고르게 · 절반은 변화 곡선이 큰 곳에. 타일 사이 간격마다 정해진 꼴의 질문, 답은 산문 없이 `"cut .9"` 꼴.
  - "transition" · "unsure" 로 답한 곳만 다음 회차에 확대 (최대 3 회차). 끝으로 샷마다 상세 시트 1 장에서 키 프레임을 고른다.
  - **API 가 없으면** `run()` 이 질문 파일 · 시트 경로를 내고 `status: waiting` 으로 멈춘다 → 에이전트가 답 파일을 채우고 다시 부르면 이어 간다 (파일 기반 · 이어 하기 · 여러 에이전트 병렬).
  - 결과 `rea-video:survey/timeline.json` = 장면 바뀜 (시각 · 종류 · 확률 · 누가 찾았나) · 샷별 키 프레임 · 0.25 초 간격 변화 곡선 (리듬).
- **소리 · 말** (`audio.py` · `speech.py` · `prosody.py`): 목소리 / 음악 / 효과음 판정 · BPM · 섹션 경계; 음원 분리 ONNX (UVR MDX-Net 약 67 MB + BandIt v2 약 149 MB, 첫 실행 때 내려받음); 로컬 ASR = sherpa-onnx SenseVoice (중 · 영 · 일 · **한** · 광둥, 약 160 MB) + 화자 분리 (+35 MB); 줄마다 **말 속도 (자/초) · 음높이 폭 (반음) · 다른 줄 대비 크기 (±4 dB) · 앞 쉼 (0.6 초) · 감정** — "TTS 가 따라 할 수 있는 숫자" 를 낸다. 한글은 글자로 세지만 속도 기준값은 중 · 영만 있다 (`SLOW, FAST = {"zh": 3.5, "en": 2.0}, {"zh": 6.5, "en": 3.3}`).
- **자막 층** `packaging.py`: 전 영상 OCR (rapidocr) → 자막 줄 시작 · 끝 · 색 · 외곽선 → SRT / ASS.

**우리에게 붙일 자리**
1. AVI **S1 레퍼런스 · 자료**: 지금 `docs/video_reference/README.md` 는 "이 환경은 영상을 보거나 들을 수 없다" 로 빈칸을 1저자 설명에만 기대고 있다. 1저자가 레퍼런스 mp4 파일을 주면 → 컷 수 · 컷 간격 · 자막 줄 시간 · 내레이션 음절/초 · BGM BPM · 줄별 크기 차를 **실측**하고, 접촉 시트를 Claude 가 Read 로 본다 (영상 파일만 있으면 youtube 접속은 필요 없다).
2. AVI **S6 · S9 장면 점검**: 우리 렌더도 같은 시트로 본다. 6 분 영상을 0.5 초 간격으로 보면 720 프레임 → 120×68 타일이면 시트 한 장에 약 140 개 → 5–6 장 [추정 · 산술] — CLAUDE.md "영상 = 0.5–1 초 간격 장면 전체" 를 정해진 토큰 비용으로 지킨다.
3. 컷 검출 결과로 "장면 바뀜 ↔ 대본 문장 경계" 대조 (S8 강약 · 이음 점검).

**일의 크기** 작게 = `shots.py` 핵심 (~150 줄) + 시트 패커 (~150 줄) 만 옮김 (numpy · opencv-headless · Pillow), 1–2 일. 크게 = 별도 venv 에 전체 설치 (ONNX 모델 첫 실행 다운로드 합계 약 0.4 GB → 디스크 확인).

**위험** 생긴 지 4 주 · 별이 빠르게 늘었고 개인 저자. 스킬 문서 · 판정 기준표 · 평가 결과는 중국어. 정확도 98–99 % 는 [README] 수치 (우리가 재 보지 않음). 음원 분리 가중치 BandIt v2 = CC BY-SA 4.0. 남의 영상 재게시 금지는 README 도 적는다 — 구조 · 속도만 배우고 장면은 가져오지 않는다.

**라이선스 처리** Apache-2.0 — 코드 옮길 때 LICENSE · NOTICE 유지, 바꾼 파일에 표시.

### 3-2. kajisho5/ffmpeg-skill — 검사까지 하는 ffmpeg 도구 42 개 (MIT · 별 10,871 · 커밋 `c7dad34c` 2026-11-24)

**무엇** [README · 소스] `scripts/<도구>.py` 42 개 (cut · join · fit · caption · loudness · silence · scenes · sync · check · look · export · render …). 모두 `--json` (숫자는 여기서만) · `--dry-run` · 쓴 결과를 스스로 다시 재서 `verified` 를 낸다. MCP 서버 내장 (기본 12 개 도구 노출, 이름으로 42 개 모두 호출).

**어떻게 작동하나** [소스]
- **음량 `ffmpeg-skill:scripts/loudness.py`** — 2-pass EBU R128:
  - 1 회차 `loudnorm=I:TP:LRA:print_format=json` 로 잰 값 (input_i · tp · lra · thresh · offset) 을 2 회차 `linear=true` 에 그대로 넣는다. 앞에 `aresample=async=1:min_hard_comp=0.01`.
  - `loudnorm_mode()` 가 **ffmpeg 자신의 규칙** (af_loudnorm.c) 으로 linear 가 될지 미리 판정: 측정값이 결측 (tp 99 · thresh −70 · lra 0 · i 0) 이면 dynamic, 아니면 `측정TP + (목표 − 측정I) ≤ TP상한 ∧ 측정LRA ≤ LRA상한` 일 때만 linear. dynamic 으로 조용히 떨어지면 범위를 눌러 목표에서 벗어날 수 있다 (결함 A111).
  - 인코딩 뒤 **다시 잰다**: AAC 가 진피크를 넘기면 비트레이트 256k → 320k, 그래도 넘으면 상한을 (넘친 양 + 0.2 dB) 낮춰 재인코딩 (최대 5 회). 결과 JSON 에 `tp_ceiling_used` · `encodes` · `loudnorm_mode` 를 남긴다 (실측 예: 192k AAC 가 −2.4 dBFS 를 +3.7 dBFS 로).
- **플랫폼 검사 `ffmpeg-skill:scripts/check.py` + `_platforms.py`**: YouTube = 1920×1080 · 16:9 · fps ≤ 60 · 최소 720p · h264/hevc/prores/av1/vp9 · **−14 LUFS ± 2 · TP ≤ −1 dBTP**. 형식 행은 고치고, 길이 · 비율 · fps · 음량은 요청에 들어 있을 때만 고친다.
- **눈 `ffmpeg-skill:scripts/look.py`**: 12 타일 시트 + 시각 · 한 시점 프레임 · 전후 나란히 · 플랫폼 UI 가림 영역 음영 — "PNG 를 Read 로 보고 확인한 뒤 보고".
- **자막 줄바꿈 `ffmpeg-skill:scripts/_common/wrap.py`**: 글자 폭을 em 으로 (한글 1.0), 안전 폭 0.9, **한국어는 어절 사이에서만 끊음** (한글 연속 = 한 낱말), 고아 줄 방지 (1.1 em). `caption.py` 는 **자막 글자를 절대 고쳐 쓰지 않음** (줄바꿈 · 시간 · 크기만 바꿈).
- **보고 꼴**: `Done: … / Steps: … / Check: … / Look: … / Notes: …` — 숫자는 `--json` 에서만, 하지 않은 고침은 쓰지 않는다.
- 결함 원장 `docs/defect-ledger.jsonl` · 재발 방지 `ffmpeg-skill:docs/defect-guards.json` · 독립 채점 평가 `evals/` — 우리 `findings.json` 과 같은 결.

**우리에게 붙일 자리** AVI S9 최종 렌더 직후 음량 (2-pass + linear 판정 + 인코딩 뒤 TP 재측정), S10 기준표의 '음량' 항목 = `check.py` 규격표, 자막 굽기 = 어절 줄바꿈 규칙 + "자막 글자 불변", 장면 점검 = `look.py` (3-1 시트와 하나로).

**일의 크기** 음량 로직 이식 ~120 줄 (반나절) · YouTube 규격 검사 ~100 줄 · 시트는 3-1 과 합침. 또는 MCP 서버를 별도 폴더에 두고 그대로 씀 (설치 판단 = 1저자).

**위험** 저장소가 크고 빨리 바뀜 (스크립트 2.7 만 줄 · CHANGELOG 576 KB) · 새 개인 계정 · `ffmpeg-skill:bin/install.js` (npm) · 플러그인 설치기가 에이전트 설정을 건드릴 수 있음 → 설치기 대신 필요한 함수만 출처 표기하고 옮긴다. "raw ffmpeg 금지" 는 그 스킬 안 규칙이지 우리 규칙이 아니다.

### 3-3. andyhuo520/vibe-knowledge — 문장마다 출처가 붙는 해설 숏 (MIT · 별 814 · 커밋 `c3a13a85` 2026-10-28)

**무엇** [README] 주제 → 조사 → 사실표 → 대본 + 반박 리뷰 → 음성 (Xiaomi MiMo, 낱말 단위 정렬) → 코드 렌더 (1080p60, Playwright 녹화) → QA → 게시 꾸러미. 템플릿 6 · 길이 4 단계 (45 초 – 5 분) · 스타일 44.

**어떻게 작동하나** [소스]
- `vibe-knowledge:skills/vibe-knowledge/templates/facts.md` — **"내레이션과 화면의 모든 숫자 · 이름 · 연도 · 인용은 여기에 한 줄; 출처 없는 것은 화면에 안 올린다."** 열 = 사실 (화면 표기) · 출처 · 등급 (T1 원문 / T2 권위 2 차 / T3 실마리만) · 원문 발췌 · 쓰이는 박자. 이견은 두 설을 다 적고 내레이션은 "한 설은…". 아래에 반박 리뷰 체크 (3 초 안 훅 · 화면당 핵심어 ≤ 8 자 · 출처 없는 단정).
- `vibe-knowledge:templates/narration/A.json` — 박자 (`id`, `narration`, `[[cue]]` 화면 신호) · `voice` (엔진 · 복제 참조 · 연출 문장) · **`lexicon`** (발음 사전, 예 `"AI": "A I"`) · 박자별 글자 상한 · 문장 ≤ 22 자 (중국어).
- `vibe-knowledge:tools/duration.py` — 복잡도 5 축 (개념 수 · 선행 지식 · 인과 사슬 · 증거 밀도 · 반전) 각 0–2 점 → 길이 단계 추천, 완성본 속도 5.5–6 자/초 (중국어).
- `vibe-knowledge:tools/qa.py` (73 줄) — ① N 초마다 프레임 → 6 열 × 400 px 시트 + 시각 (넘친 글자 · 자막 가림 · 빈 화면 · 그림 속 깨진 글자) ② **OCR 로 화면 글자를 모두 읽어 사실표와 대조** (숫자 · 인용 · 출처) ③ `ebur128` LUFS · 진피크 (−14.5 LUFS · ≤ −1 dBTP) ④ `freezedetect n=0.002 d=3` — 3 초 넘게 멈춘 화면 경고, 10 초 넘으면 녹화 사고 ⑤ BGM 상관 ≥ 0.12 · 말할 때 목소리 대비 BGM 차 (기본 약 10 dB 아래).

**우리에게 붙일 자리** AVI 대본 단계 = 사실표 표 꼴 (CLAUDE.md "화면 숫자마다 문헌 출처 줄" 을 표로 강제, T1 = litdb 정본 카드) · 박자 JSON + 발음 사전 (Typecast 에 보내기 전) · S9 점검 = qa.py 다섯 항목, 특히 **② 화면 글자 OCR ↔ 사실표 자동 대조**가 10 점 기준표 '정확성' 의 근거가 된다.

**일의 크기** qa.py 이식 반나절 — OCR 만 리눅스용으로 바꿈 (macOS Vision → 한국어 OCR, 후보는 4 절 표). 사실표 꼴은 문서 일.

**위험** MiMo API · macOS Vision · 유료 Renoise MCP (추천 링크) 에 기대는 부분은 버린다. 기본 BGM 강제는 우리 해설 영상에 맞지 않을 수 있다. 중국어 숏폼 기준값 (자/초 · 글자 상한) 은 한국어 5–8 분 해설에 그대로 쓰지 않는다.

### 3-4. neosapience/typecast-autotag — Typecast 쪽 TTS 읽기 정규화 (MIT · 별 6 · 커밋 `7a4892eb` 2026-11-23)

**무엇** [README · 소스] Typecast 를 만든 회사 (Neosapience) 의 공식 리포. 숫자 · 날짜 · 금액 · 단위를 TTS 가 읽을 한글로 바꾼다. TypeScript 의존성 0 · 브라우저 · Node · Python (≥ 3.11) · Java · C 바인딩.

**어떻게 작동하나** [소스]
- `src/korean/auto-tag.ts` (~2,000 줄 규칙) + `src/korean/tags/*.ts` + `utils/number-to-korean.ts`. 예 `50%` → 오십 퍼센트, `1:2` → 일 대 이, `5개` → 다섯 개 (고유어 수사), `100ms` → 백 밀리초, `-5°C` → 영하 오 도, `2024-01-15` → 이천이십사년 일월 십오일.
- `extractAutoTags(text)` — 바꾸지 않고 `{original, tagType, start, end}` 범위만 돌려준다 → **대본 점검용**.
- `manualTag` — `digits(1234)` → 일 . 이 . 삼 . 사, `name(김철수)` → 김 . 철 . 수.
- `src/voice-agent.ts` — **`pronunciations` 사전** (글자 그대로 · 대소문자 구분 · 긴 것 먼저 · 다시 해석 안 함) + 보호 구간 + `push/flush` 스트리밍. 입력 상한 1 만 자.
- Python 바인딩 `typecast-autotag:python-binding/typecast_autotag/binding.py` = ctypes 로 **미리 빌드된 네이티브 라이브러리** (`lib/linux/libtypecast_autotag_x86_64.so` 등) 를 부른다.
- 빈 곳: MPa · GPa · mS/cm · µm · %p · σ_e · LPSCl 같은 과학 단위 · 기호 규칙은 없다 (소스 grep 0 건).

**우리에게 붙일 자리** AVI S7 음성 직전 '읽기 정규화' 단계: ① `extractAutoTags` 로 대본의 숫자 · 단위 목록을 뽑고 ② 우리 과학 발음 사전 (예 "300 MPa" → 삼백 메가파스칼, "mS/cm" → 밀리지멘스 퍼 센티미터, "%p" → 퍼센트포인트, "σ_e" → 시그마 이) 을 `pronunciations` 로 먼저 적용 ③ 사전에 없는 기호는 DECISIONS 한 줄 (voice-auto) 또는 1저자 질문.

**일의 크기** 작음 — Node 패키지를 얇게 부르는 래퍼 (읽을 수 있는 TS 판 권장) 또는 필요한 규칙만 파이썬으로 이식. 본 일은 과학 발음 사전 작성 (수십 줄).

**위험** Python 바인딩은 바이너리라 읽은 소스와 같다는 보장이 없다 → TS 판 사용. Typecast 엔진이 안에서 따로 정규화하면 이중 변환이 될 수 있다 [추정] → 같은 문장을 정규화 전 · 후로 들어 본다. Typecast API 약관이 벤치마크 · 경쟁 목적 성능 비교를 제한한다는 기록이 있다 (`june-oh/korean-tts-bench` README) [README] → 공개 비교표를 만들 때 약관 확인.

### 3-5. kyy-logs/code-review-gate-skill — 독립 탐침 · 증거 필수 리뷰 게이트 (MIT · 별 519 · 커밋 `a686bc0c` 2026-11-10)

**무엇** [README · 소스] 커밋 전 · PR 병합 전 리뷰 skill. 탐침 4 개 (behavior-review · test-coverage · repo-guard · impact-analysis) 를 독립 에이전트로 병렬 실행하고, 높은 결함이 닫힐 때까지 병합을 막는다.

**어떻게 작동하나** [소스]
- `code-review-gate-skill:skills/code-review-gate/SKILL.md` = 지휘 흐름. 검사 항목은 이 파일에 박지 않고 **등록부 `code-review-gate-skill:references/probes.yaml`** (name · file · required · requires · params · `execution.max_retry: 1`) 가 정한다. 입력이 없으면 `skipped` + 사유, 읽을 수 없으면 `error`.
- `scripts/collect-metrics init {slug} --mode worktree|commits` → **`review-snapshot.json` 이 리뷰 대상 (파일 해시 또는 base/head 커밋) 을 고정** · 같은 slug 재사용 거부. 고친 뒤 `snapshot` 을 다시 찍고 영향 탐침만 재실행 · 대상이 바뀌면 `stale-review`.
- 공용 규칙은 `code-review-gate-skill:references/probes/common.md` 한 곳 — 탐침마다 경로만 넘기고 바꿔 쓰지 않는다.
- 결과 계약 `code-review-gate-skill:references/output-schema.md`: `id` 안정 · `severity` high/medium/low (셋만, 다른 값은 오류) · `status` open/reconciled/wontfix/false-positive · `location` · **`evidence` 필수 ("증거 없으면 결함 아님")** · `repro` = 읽기 전용 명령만 · 확인 못 한 우려는 따로 `unverified_items` (사실 ↔ 추론 구분). 계약을 확인 못 했으면 최대 medium — **"읽지 않은 것을 없다고 치지 않는다"**, "테스트 초록 ≠ 동작 옳음".
- `collect-metrics sync` = 개수를 **JSON 에서 스크립트가 계산** (손으로 채우지 않음). 형식 오류 · 중복 id · 상태 충돌이면 실패하고 옛 값을 쓰지 않는다. high 만 막음: `RECONCILE_PENDING > 0` 이면 병합 금지.
- 리뷰어 자신의 회귀 시험 `eval/regression-suite/` — 동결한 skill 의 sha256 · 기준선 · 깨끗한 대조 사례.

**우리에게 붙일 자리** 우리 "내부 반박 리뷰 (Codex 아님)" 를 같은 꼴로: ① 리뷰 핀을 손으로 적는 대신 snapshot 해시로 자동 고정 · 핀 뒤 바뀐 파일이 있으면 자동 거부 ② 탐침 = CLAUDE.md 사전 공격 ② 의 HOLD 부류 (NaN · inf · 넘침 · 빈 · 중복 · 검사 전 정규화 · 유니코드 숫자 · 증서 ↔ 결과 결합 · 다른 판본 증서) 를 등록부 항목으로 ③ 요청서 · 보고의 개수는 sync 스크립트가 JSON 에서만 (`SELF-124` 부류 방지) ④ high 만 HOLD = 1저자 11-16 결정 (P1 만 HOLD) 과 같음 ⑤ `unverified_items` = 우리 "관찰 · 추정 · 미확인" 표지.

**일의 크기** 중간 — 지휘 문서 + 등록부 + 결과 계약 + sync 스크립트 (~300 줄) 를 우리 `docs/reviews/findings.json` 상태 이름 (open · claimed_fixed · verified) 에 맞춰 새로 짠다. Java/Spring 규칙 팩 (`references/rules/*`) 은 버린다.

**위험** 규칙 팩이 Java 전용 · 새 개인 계정 · 설치 스크립트 (`code-review-gate-skill:scripts/install-remote.py`) 는 쓰지 않는다 · 상태 이름 대응표가 필요하다.


## 4. 세 분야 상위 후보 — 붙일 자리 · MCP 꼴 · 설치

### 4-1. AVI 영상 만들기

**한국어 로컬 TTS — Qwen3-TTS (1) · VoxCPM2 (2)**
- 왜: MeloTTS 는 한국어 난문장 벤치 (`june-oh/korean-tts-bench`) 의 자모 문장 (P07) 에서 KeyError 로 실패했고, 같은 벤치가 상업 사용 후보로 "VoxCPM2 와 Qwen3-TTS (공식 체크포인트 Apache 2.0)" 를 먼저 든다 [README]. 우리 체감 ("억양이 약함") 과 방향이 같다.
- 억양 손잡이: Qwen3-TTS = CustomVoice 의 `instruct` (말투 지시, 예 "천천히") · VoiceDesign (말로 목소리 설계) · 한국어 화자 Sohee ("Warm Korean female voice with rich emotion") [README]; VoxCPM2 = Voice Design · 조절 가능한 복제 · 48 kHz [README]. 레퍼런스 영상의 줄별 말 속도 · 음높이 폭 · 쉼 (rea-video `prosody.py` 숫자) 을 지시문 근거로 쓸 수 있다 [추정].
- 라이선스: 두 모델 모두 코드 · 가중치 Apache-2.0 [README] → 연구 · 상업 모두 가능. Supertonic 3 (가중치 OpenRAIL-M) 은 용도 제한 + "기계 생성물 표시" 조건 [검색] — 우리 AVI 는 공개판 표지에 AI 음성을 밝히면 맞출 수 있으나 원 리포가 보관 처리됐다.
- MCP 꼴: 둘 다 MCP 없음 → **감쌀 수 있음**. 도구 2 개면 된다: `tts_speakers()` · `tts_synthesize(text, speaker, instruct, out_wav)`. 앞에 typecast-autotag (3-4) 와 과학 발음 사전을 끼운다.
- 설치: 이 컨테이너 = 불가 (torch · 모델 가중치 수 GB [추정] · GPU 없음 · 디스크 2.1 GB). 1저자 PC = WSL + CUDA GPU 권장 (GPU 유무는 [미확인]) · 다른 GPU 기계에서 돌릴지는 1저자 결정.
- 시험 꼴 (제안): 벤치의 16 문장 유형 + 우리 대본 과학 문장 10 개 (단위 · 기호 · 소수 · 비율 "7:3") × {Typecast · Qwen3-TTS 1.7B · VoxCPM2} → 1저자 청취 10 점 기준표 (억양 · 발음 · 숫자 읽기 · 자연스러움). ⚠ Typecast API 약관이 벤치마크 · 경쟁 비교를 제한한다는 기록 [README] → 결과는 내부 선택용으로만 두고 공개하지 않는다.

**낱말 단위 자막 정렬 — stable-ts (1)**
- 왜: 우리는 TTS 에 넣은 대본 글을 이미 안다 → 받아쓰기 (ASR) 보다 **강제 정렬** 이 맞다. stable-ts 는 Whisper (가중치 MIT) 로 주어진 글을 음성에 맞추는 `align` 과 낱말 시간을 낸다 [README]. WhisperX (BSD-2) 는 언어별 wav2vec2 정렬 모델을 자동으로 고르는데 한국어 모델의 가중치 라이선스를 따로 봐야 한다. ctc-forced-aligner 는 CLI 가 가장 단순하지만 한국어는 로마자 변환을 거치고 기본 가중치 (MMS 계열) 라이선스 확인이 필요하다 [추정].
- 붙일 자리: S7 음성 뒤 → 낱말 시간 JSON → SRT / ASS (ffmpeg-skill 줄바꿈 규칙: 한국어 어절 사이에서만 끊고 글자는 고치지 않음) → S8 강약 · 이음 점검 (문장 경계 ↔ 장면 바뀜 대조).
- MCP 꼴: 감쌀 수 있음 (`align_words(wav, script_txt, lang="ko") → json`).
- 설치: torch 또는 faster-whisper (ctranslate2) 필요 → 이 컨테이너는 디스크 때문에 비권장 · 1저자 PC 는 가능.

**음량 · 강약 — ffmpeg-skill 로직 (1)**: 3-2 의 2-pass + linear 판정 + 인코딩 뒤 진피크 재측정을 S9 에 넣는다. 측정 확인은 pyloudnorm (MIT) 로 따로 (같은 도구로 맞추고 같은 도구로 재지 않기). MCP 꼴 = 있음 (ffmpeg-skill 내장) 이지만 함수 이식이 더 가볍다. 설치 = 이 컨테이너 가능 (ffmpeg 있음).

**장면 · 그림 애니메이션 · 합성 — HyperFrames (1) · Manim (2)**
- HyperFrames: HTML · CSS · JS 장면을 헤드리스 Chrome 이 프레임마다 찍고 FFmpeg 로 인코딩 → 같은 입력 = 같은 영상 (결정적) [README]. 지금 PIL 로 그리는 장면을 HTML 로 바꾸면 한글 글꼴 · 줄바꿈 · 표 · 그림 배치를 CSS 로 다룰 수 있다 [추정]. `/slideshow` (발표 모드 덱) · `/reverse-any-video` 스킬도 있다. 로컬 = CLI (`npx hyperframes init / preview / render`) → MCP 는 **감쌀 수 있음**; 호스팅 커넥터 · 클라우드 렌더 · `share` 는 외부로 나가므로 쓰지 않는다. 요구 = Node 22+ · FFmpeg (이 컨테이너에 둘 다 있음) + 헤드리스 Chrome 다운로드 [추정 수백 MB].
- Manim CE: 수식 · 도식 움직임 장면. `manim-mcp-server` (MIT) 가 있지만 2025-05 뒤 멈췄고 받은 Python 을 그대로 실행한다 → 우리 코드만 넣는다. LaTeX 가 필요한 장면은 1저자 PC (MiKTeX 등) 에서.
- 합성: 지금 ffmpeg 흐름 유지 (PyAV 19 는 Python ≥ 3.12 · MoviePy 는 가벼움).

**레퍼런스 영상 읽기 · 장면 점검 — rea-video (1)**: 3-1. claude-video-vision (MIT, MCP 있음) 은 더 간단하지만 프레임을 고르는 규칙 · 비용 관리가 rea-video 만큼 정교하지 않다 [README 비교 · 추정].

### 4-2. 벡터 그림 만들기

**도식 — draw.io 공식 MCP (1)**
- 꼴 셋 [README]: ① 호스팅 앱 서버 (`mcp.draw.io`, 대화 안 보기) ② 로컬 도구 서버 (npm · 브라우저 편집기로 엶) ③ 어시스턴트 플러그인 (`.drawio` 파일 생성 · PNG / SVG / PDF 내보내기는 draw.io Desktop). XML · CSV · Mermaid 입력.
- 붙일 자리: Figure 1 개념도 · 공정 흐름 · 장치 그림 — 보고자료 원칙 "범례 · 주석은 그림 밖 (편집 가능한 원본)" 과 교수님 어록 "Figure 1 = concept · scheme" 에 맞게 **편집 가능한 원본 (.drawio)** 을 남기고 1저자가 Windows draw.io Desktop 에서 고친 뒤 SVG / PDF 로 낸다.
- 쓰지 않을 것: 호스팅 앱 서버 (미공개 그림이 밖으로 나감).
- 설치: 이 컨테이너 = `.drawio` XML 생성까지 (GUI · Desktop 없음) · 1저자 PC = 잘 맞음.

**간단 도식 · 수식 그림 — Mermaid (2) · Typst (3)**
- Mermaid + `mcp-mermaid` (MIT): `svg` · `file` 출력만 쓴다 (`svg_url` · `png_url` 은 외부 렌더로 보임 [추정]). mermaid-cli 는 헤드리스 Chromium 이 필요하다 [추정].
- Typst + `typst-mcp` (MIT): 문서 조회 · LaTeX → Typst (Pandoc — 이 컨테이너에 있음) · 문법 검사 · PNG 렌더. `pip typst` (wheel 35.8 MB · 의존성 0) 로 SVG / PDF 도 낸다 [레지스트리]. 그리기 패키지 cetz 는 LGPL-3.0 — 그림 파일을 만드는 데 쓰는 것은 괜찮고 cetz 를 고쳐 배포할 때만 의무가 생긴다 [추정].

**래스터 → 벡터 — vtracer (1)**: 색 이미지 · 스플라인 / 다각형 · 팔레트 고정 · 점 잡음 거르기 · `color-cluster` / `bw` / `watershed` [README]. 우리 래스터 그림 (예: 손 스케치 · 옛 그림) 을 SVG 로. 남의 논문 그림을 벡터로 옮겨 싣는 데는 쓰지 않는다 (저작권). MCP 꼴 = 감쌀 수 있음 (`vectorize(png, mode, palette) → svg`). 설치 = 이 컨테이너 가능 (wheel 1.3 MB · 의존성 0) · Windows wheel 있음.

**SVG 다듬기 · 논문 그림 뒤처리 (한 줄 흐름)**: matplotlib (`svg.fonttype = 'none'` 로 글자를 글자로 남김 · 고정 그림 크기) → **svgutils** 로 패널을 같은 배율로 붙임 (보고자료 원칙 "패널 그래프 크기 · 붙이는 배율 통일") → **svgo** 로 정리 (글자 · id 보존 설정) → **resvg** 로 PNG 를 다시 그려 렌더 점검 (화면 결과물은 렌더해서 본다). 모두 MIT / Apache · 가벼움 · 이 컨테이너 가능 (svgo 는 npm). MCP 꼴 = 감쌀 수 있음.

### 4-3. 그 밖의 연구

**PDF 논문 읽기 · 그림 · 표 — Docling + docling-mcp (1) · marker (2) · MinerU / GROBID (3)**
- Docling (MIT): PDF → 구조 문서 (그림 · 표 · 캡션). docling-mcp (MIT) 가 `local` / `remote` 변환 모드를 둔다 → litdb 는 `local` 만. 붙일 자리 = litdb 카드 만들 때 그림 크롭 · 표 추출 1 차안 (원문 대조는 그대로 사람 · 에이전트 몫 — 규율 ⑥ "SI 까지 본 뒤에만 '없다'").
- marker (코드 Apache-2.0 · 모델 OpenRAIL-M): CPU `fast` 모드 (약 18 MB ONNX) 가 docling 보다 높은 점수를 낸다는 README 주장 → 우리 PDF 10 편으로 나란히 비교하고 고른다.
- MinerU: Apache-2.0 + 추가 조항 (월 사용자 1 억 · 월 매출 2 천만 달러 기준 · 온라인 서비스 표시) — 연구실 사용은 걸리지 않는다. GROBID: 참고문헌 · 메타데이터 TEI 에 강함 (Java 서버 · Docker) — 이번에 리포를 조회하지 못했다.
- 설치: 모델 첫 다운로드가 커서 [추정 수백 MB 이상] 이 컨테이너는 비권장 · 1저자 PC 가능.

**논문 검색 MCP — paper-search-mcp (1) · arxiv-mcp-server (2) · zotero-mcp (3)**
- paper-search-mcp (MIT): arXiv · PubMed · bioRxiv · medRxiv · Google Scholar · Semantic Scholar · Crossref · OpenAlex · PMC · CORE … 동시 검색 · 중복 제거 · 오픈 액세스 PDF 받기 · 키는 선택 [README]. litdb 의 "최근 2 년 먼저 찾기" 와 맞게 날짜 정렬로 쓰고, 찾은 것은 그대로 정본 `papers/` 목록과 대조 (중복 확인 = 파일 목록).
- arxiv-mcp-server (Apache-2.0): 원 LaTeX 를 절 단위로 읽고 BibTeX 를 만든다 · 논문은 로컬 디스크.
- 설치는 가볍다 (pip 0.1 MB) · **이 클라우드 컨테이너는 외부 학술 API 가 허용 목록에 없을 수 있다** [추정] → 1저자 PC 에서 쓰거나 환경 네트워크를 넓혀야 한다 (1저자 결정).

**GPU 희소 풀이 — AmgX (1)**
- 접촉망 Kirchhoff · 복셀 FV 는 대칭 양정치 (SPD) 라플라시안이라 AMG 전처리 CG 의 전형적 대상이다 [추정]. 지금 R 런 풀이 (Rint ②) 가 수십만 회 반복 · 수백 시간 규모라 AMG 전처리로 반복 수를 크게 줄일 여지가 있다 [추정 — 재 보지 않음].
- AmgX (BSD-3 확인) + pyamgx (BSD-3 · PyPI 없음 · 2024-09 뒤 멈춤) → CMake + CUDA Toolkit 빌드. MCP 꼴 = 안 됨 (풀이 코드 안에서 직접 부를 라이브러리).
- ⚠ 봉인 코드 · 등록 순서: 지금 R 사슬에는 넣지 않는다 — 다음 세대에 등록 · 비트 대조 (OFF 경로) 를 먼저.

**시뮬레이션 가속 — Quadrants (위험 기록) · Warp · DEM-Engine**
- Quadrants README 가 "원 Taichi 는 더 이상 유지보수되지 않는다" 고 적는다 (Taichi 의 GitHub 마지막 push = 2026-10-05 [API]). 우리 3D MPM (`scripts/mpm3d_compaction.py`) 은 Taichi 위에 있다 → **유지보수 위험을 원장에 적을 거리** (지금 바꾸지 않음 · 봉인 · 비트 같음 대조가 먼저).
- Warp (Apache-2.0) · DEM-Engine v3 (GPU DEM · 사용자 접촉 모델) 는 [DEM 우선 (수영)] 재설계 비교 후보 — 아이디어만.

**SEM 이미지 분할 — micro-sam (1) · napari-mcp / Fiji MCP (2) · Maskbolt (3)**
- micro-sam (MIT): SAM2 기반 · 몇 번 클릭으로 분할 · 자동 분할 · 우리 자료로 미세 조정 [README]. 복합 양극 단면 (활물질 / 고체전해질 / 기공) 은 학습 분포 밖이라 라벨 몇 장으로 미세 조정이 필요할 것 [추정].
- napari-mcp (BSD-3 · Royer lab) · Fiji-ImageJ MCP (BSD-3) = 에이전트가 GUI 를 조작 (1저자 PC).
- Maskbolt (MIT): CPU · Rust 한 파일 · MCP · 마스크 / SVG 외곽선 — 별 0 · 생긴 지 한 달이라 시범 전 코드 확인 필요.

### 4-4. "감쌀 수 있음" 의 뜻 — 얇은 MCP 공통 꼴
- `fastmcp` (Apache-2.0 · PyPI 4.2.6 · Python ≥ 3.11) 로 도구 1–3 개짜리 서버를 만든다 → stdio 전송 (포트를 열지 않음 — 5001 · 5002 와 충돌 없음).
- 도구마다: 입력 경로 · 출력 경로 · 사용 버전 · 모델 이름 · 소요 시간을 JSON 으로 돌려준다 (ffmpeg-skill 의 `--json` 꼴).
- MCP 추가는 설정 변경 (`.mcp.json` · `settings.json`) → 1저자 승인 뒤. codegraph 처럼 CLAUDE.md 를 고치는 설치기는 쓰지 않는다.

## 5. 가져올 때 할 일 (순서 · 크기 · 결정)

1. **AVI 음량** — ffmpeg-skill `loudness.py` 의 2-pass · linear 판정 · 인코딩 뒤 진피크 재측정을 S9 에 이식 (MIT 출처 표기). 시험 먼저: 합성 신호로 linear ↔ dynamic 판정 · AAC 오버슛 재측정이 옛 코드에서 실패하는지. 크기 반나절.
2. **AVI 시트 · 컷** — rea-video `survey.py` 시트 규칙 (1568 px · 1.15 MP · 타일 120×68) + `shots.py` 컷 검출 핵심을 이식 (Apache-2.0 NOTICE) → S6 · S9 장면 점검 · S1 레퍼런스. 크기 1–2 일. 1저자: 레퍼런스 영상 mp4 파일 전달.
3. **AVI QA** — vibe-knowledge `qa.py` 다섯 항목 (시트 · OCR ↔ 사실표 · 음량 · freezedetect · BGM) 꼴. 1저자 결정: 한국어 OCR 엔진 (설치 필요).
4. **AVI 대본 정규화** — typecast-autotag (TS 판, 의존성 0) + 과학 발음 사전 (`pronunciations`) → `extractAutoTags` 로 대본 숫자 · 단위 점검. 1저자: Typecast 약관 확인 (비교 공개 여부).
5. **로컬 TTS 교체 시험** — Qwen3-TTS 1.7B · VoxCPM2 를 4-1 의 시험 꼴로 청취. 1저자 결정: 돌릴 GPU 기계 · 디스크 (가중치 수 GB [추정]).
6. **자막 낱말 정렬** — stable-ts `align` → 낱말 시간 → SRT / ASS (어절 줄바꿈 · 글자 불변). 1저자 PC (WSL).
7. **벡터 도식 시범** — draw.io 공식 MCP 플러그인으로 Figure 1 개념도 `.drawio` 1 장 → 1저자가 Desktop 에서 고침 → SVG / PDF. 같이: vtracer · svgutils · svgo · resvg 뒤처리 흐름 (이 컨테이너에서 가능한 가벼운 것들).
8. **litdb PDF** — docling-mcp (`local`) 와 marker 를 같은 PDF 10 편으로 비교 → 그림 크롭 · 표 추출 1 차안. 1저자 PC.
9. **논문 검색 MCP** — paper-search-mcp · arxiv-mcp-server (네트워크: 1저자 PC 또는 환경 허용 목록 = 1저자 결정).
10. **리뷰 게이트** — code-review-gate 꼴 (스냅샷 해시 핀 · 등록부 · JSON 에서 스크립트가 센 개수 · high 만 HOLD · `unverified_items`) 로 내부 반박 리뷰 skill 개정안 초안. 1저자 비준 뒤.
11. **위험 기록만** — Taichi 유지보수 중단 (Quadrants README) → MPM 트랙 원장에 한 줄 (지금 이주 안 함). AmgX = Rint ② 다음 세대 전처리 후보 (등록 먼저).
12. **하지 않을 것** — codegraph 설치기 (CLAUDE.md · 권한 수정) · 호스팅 렌더 (draw.io 앱 서버 · mermaid URL · upmath · HyperFrames cloud) · AGPL / GPL 코드 이식 (whisper-timestamped · PyMuPDF · neonclipping · Agent-Cockpit · GeoTaichi · potrace).

## 6. 출처

- GitHub 검색 API 결과 (원자료): `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/gh_trending_1125/api/trend_created.json` (11-11 이후 생성 · 별 순 40) · `…/gh_trending_1125/search/` (s01–s22 · t01–t06) · `…/gh_trending_1125/search3/` (r01–r13 세 분야 이름 조회 · m01–m14 · f01–f12 · g01–g04 MCP 검색; m10–m12 는 `OR` 질의가 깨져 버림).
- 레지스트리 메타데이터: `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/gh_trending_1125/reg/registry.tsv` (PyPI 50 — 그중 `pyamgx` 는 없음 · npm 6 · crates 3 — 최신판 · 라이선스 · wheel 크기 · 무거운 의존성).
- 받은 리포 커밋: `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/gh_trending_1125/clone_log.txt` (받은 폴더 `repos/` 는 조사 뒤 지웠다).
- 웹 검색 (요약만 사용, 페이지 본문은 접속 불가):
  - [Analytics Vidhya — Top 10 GitHub Repositories Trending in October 2026](https://www.analyticsvidhya.com/?p=258844)
  - [aitoolly — agent-skills on GitHub (2026-11-12)](https://aitoolly.com/ai-news/article/2026-11-12-agent-skills-production-grade-engineering-skills-for-ai-coding-agents-on-github)
  - [DEV — Why half of this week's trending GitHub AI tools are called skills](https://dev.to/visesh/why-half-of-this-weeks-trending-github-ai-tools-are-called-skills-5d6f)
  - [trendshift weekly 2026/36](https://trendshift.io/weekly/2026/36?language=C) · [TechTarget — What repos are trending on GitHub](https://www.techtarget.com/searchAppArchitecture/tip/What-repos-are-trending-on-GitHub)
  - [arXiv 2605.20830 (RAON-OpenTTS)](https://arxiv.org/pdf/2605.20830) · [MeloTTS-Korean](https://huggingface.co/myshell-ai/MeloTTS-Korean) · [Supertonic](https://huggingface.co/Supertone/supertonic) · [mt.co.kr — KRAFTON Raon-Speech](https://www.mt.co.kr/en/tech/2026/07/29/2026072910223093786)
  - [Supertonic 3 미러 (라이선스 · 보관 기록, 공식 아님)](https://huggingface.co/jiangzhuo9357/supertonic-3)

