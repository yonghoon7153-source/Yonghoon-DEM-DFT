# COMSOL63_RADIAL160_HANDOFF — 원문 보존 기록 (2026-09-14)

인계 ZIP 을 사용자 PC(WSL)에서 풀어 md·json·csv·txt 만 `cp --parents` 로 복사해 커밋한 것이다. 이 폴더는
`.gitattributes` 의 `reviews/r14_repros/codex63/radial160/** -text` 로 **줄끝 변환 없이** 저장된다 (CRLF 원문 그대로).
판정은 `docs/COMSOL_REBUILD_SPEC.md` 의 해당 절이다.

## 대조 결과 (이 저장소에서 실행)

| 검사 | 결과 |
|---|---|
| ZIP SHA-256 (`ZIP_SHA256.txt`, 사용자 WSL `sha256sum`) | `39ded591a29568d58b57791bf68147292a9cef06660de40b1c5e45ed16b434bc` — 전달값과 일치 |
| `package_manifest.json` | 명세 **160** 항목 · scope "One new300/160 five-second case; existing40/80 evidence is reference only" |
| 여기 보존한 항목 | **112** 개 — 항목별 크기·sha256 **전부 일치**, 불일치 **0** |
| 제외한 항목 | **48** 개 (mph·로그·java·그림·dmodel·대용량 profile·py) — `FULL_LISTING.tsv` 의 크기가 명세와 일치한 것 **48** 개 |
| 명세 밖 파일 | `ZIP_SHA256.txt` · `FULL_LISTING.tsv` (이쪽이 만든 것) · `package_manifest.json` (자기 자신) |
| 압축 해제본 전체 | 161 파일 · 514,860,294 B |

제외 이유: mph·로그·java 는 공개 저장소에 두지 않는다 (원본 모델 계열 자료·기계 경로 포함 가능), 대용량 CSV 는 결과
요약이 `results/` 에 있다. 필요하면 사용자 PC 의 압축 해제본에서 같은 방법으로 추가한다.

## 확인하지 않은 것

COMSOL 재실행 · java 소스 해시(보존 제외) · mph 해시 · 현지 현재 파일의 보존 · 물성·OCP 의 물리적 정확성.
