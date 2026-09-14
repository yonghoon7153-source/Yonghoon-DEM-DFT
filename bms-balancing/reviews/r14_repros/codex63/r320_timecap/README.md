# COMSOL63_R320_TIMECAP_HANDOFF — 원문 보존 기록 (2026-09-14)

`.gitattributes` 의 `reviews/r14_repros/codex63/r320_timecap/** -text` 로 bytes 그대로 저장된다. 판정은
`docs/COMSOL_REBUILD_SPEC.md` §15.

| 검사 | 결과 |
|---|---|
| ZIP SHA-256 | `e38968f13e3fae64948c2234fb020cad1d5f1119fc8535aa7fc8766e69274f67` — 전달값과 일치 (`ZIP_SHA256.txt`) |
| manifest 자체 SHA-256 | `964b681763517190ac2ea84f243134d807a6b468f77ed9d31b57a7a4851e8e1a` — **전달값과 일치** |
| 명세 | **160** payload (`outputs/radial320_timecap/package_manifest.json`, 자기 자신 제외) |
| 보존한 항목 | **114** 개 — sha256 **전부 일치**, 불일치 **0** |
| 제외한 항목 | **46** 개 (mph·로그·java·그림·대용량 profile·py·중첩 ZIP) |
| 재계산 | 네 비교 파일(`requested_grid` 107/187 · `all_exact_common_stored` 484/565) 전부에서 max\|ΔV\| = **0.0012699200233 mV @0.002 s** · 표면 x 차 **-2.1349484521e-8 @0.002 s · N · z=52 µm** |

## 줄끝 복원 — 이 묶음만 순서가 뒤집혔다

앞선 여섯 묶음과 달리 이번에는 **`-text` 규칙보다 커밋이 먼저**였다 (`b0aed7a`). 그래서 git 이 체크인에서 CRLF→LF
정규화를 적용했고, 커밋된 bytes 가 manifest 의 sha256 과 갈렸다. 규칙을 추가한 뒤 원본 bytes 를 되돌렸다.

| 보존 114 개의 내역 | 개수 |
|---|---:|
| `b0aed7a` 의 bytes 와 이미 동일 (원문이 LF) | 34 |
| 전부 CRLF → 복원 | 79 |
| 줄끝이 섞여 있어 복원 | 1 |

섞인 하나는 `outputs/radial320_timecap/TIMECAP320_RESULTS_KO.md` 다 — 104 줄 중 **102 번째 줄만 맨 LF** 이고 나머지
103 줄이 CRLF 다. 일괄 `LF→CRLF` 치환으로는 이 파일이 복원되지 않는다 (102 번째 줄까지 CRLF 가 되어 sha 가 어긋난다).
그래서 복원은 치환이 아니라 **ZIP 원문 bytes 로 덮어쓰기**로 했고, 대조는 manifest 의 항목별 sha256 으로만 했다.

교훈은 순서다 — **`.gitattributes` 의 `-text` 를 먼저 넣고 그 다음에 묶음을 커밋한다.** 반대로 하면 정규화가 이미
일어난 뒤이고, 원본 ZIP 이 손에 없으면 되돌릴 수 없다.

## 확인하지 않은 것

COMSOL 재실행 · java 소스 해시(보존 제외) · mph 해시(1,266,675,445 B, 보존 제외) · 현지 현재 파일 967 개의 보존 ·
물성·OCP 의 물리적 정확성 · 이전 TIME_CAPS raw ZIP 차이 원인(계속 **미확인**). 수신 측 ZIP 확인값은 **사용자 보고**이고
원본 영수증(`outputs/COMSOL63_RADIAL320_HANDOFF_RECEIPT.json`, 이전 R320 전달분)은 고치지 않았다.
