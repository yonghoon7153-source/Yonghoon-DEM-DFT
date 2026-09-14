# COMSOL63_R160_TIMECAP_HANDOFF — 원문 보존 기록 (2026-09-14)

인계 ZIP 을 사용자 PC(WSL)에서 풀어 md·json·csv·txt 만 `cp --parents` 로 복사해 커밋한 것이다. 이 폴더는
`.gitattributes` 의 `reviews/r14_repros/codex63/r160_timecap/** -text` 로 **줄끝 변환 없이** 저장된다.
판정은 `docs/COMSOL_REBUILD_SPEC.md` §13.

## 대조 결과 (이 저장소에서 실행)

| 검사 | 결과 |
|---|---|
| ZIP SHA-256 | `481ce9ebb1455de18ffcc35554d34b8a5fceb5c8cea3018938a200fadd920bdc` — 전달값과 일치 |
| `package_manifest.json` | 명세 **267** 항목 · scope "One new R160H0250 5-second early-cap-halving; prior sources/results reused; corrected prior metadata with original before bytes" · `reference_jobs_rerun: false` |
| 여기 보존한 항목 | **186** 개 — 크기·sha256 **전부 일치**, 불일치 **0** |
| 제외한 항목 | **81** 개 (mph·로그·java·그림·대용량 profile·py) — 목록 크기 일치 |
| 재계산 | `requested_grid`(187/107 행)와 `all_exact_common_stored`(363/282 행) **둘 다** max\|ΔV\| = 0.002175461073 mV @0.005 s · 표면 x 차 4.30032160e-8 @0.002 s · P · z=121 µm |
| `corrections/` | §12-5 의 baseline 식별자 정정 — before `dbcb95c47abad…` → 현행 `6ab32b93310657265906cc858af3847d662923cf7dd8964feb74ed6cbe86f2b1` (우리가 지목한 값과 일치). before bytes 백업 보존, archive manifest 불변, 회귀 24 PASS |

## 확인하지 않은 것

COMSOL 재실행 · java 소스 해시(보존 제외) · mph 해시 · 현지 현재 파일의 보존 · 물성·OCP 의 물리적 정확성.
수신 측 ZIP 확인값(307,305,998 B · payload 267+manifest 1 · CRC·명부·역사적 333)은 **사용자 보고**이고 원본
영수증은 고치지 않았다 (원본의 수신 확인 필드 null 은 당시 기록).
