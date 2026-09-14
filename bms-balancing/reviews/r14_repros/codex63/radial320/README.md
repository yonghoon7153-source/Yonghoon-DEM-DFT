# COMSOL63_RADIAL320_HANDOFF — 원문 보존 기록 (2026-09-14)

`.gitattributes` 의 `reviews/r14_repros/codex63/radial320/** -text` 로 bytes 그대로 저장된다. 판정은
`docs/COMSOL_REBUILD_SPEC.md` §14.

| 검사 | 결과 |
|---|---|
| ZIP SHA-256 | `89703ec4a1e47985ddefa9b0270cd317d0356cbe2ec7d4efe31f879703702aa0` — 전달값과 일치 |
| manifest 자체 SHA-256 | `aeb7c0288d3a6217f4186b67034946a81028284a104fb9df015374232d2c1361` — **전달값과 일치** (이번엔 manifest 해시까지 대조했다) |
| 명세 | **147** payload |
| 보존한 항목 | **103** 개 — 크기·sha256 **전부 일치**, 불일치 **0** |
| 제외한 항목 | **44** 개 (mph·로그·java·그림·대용량 profile·py) — 목록 크기 일치 |
| 재계산 | 지정 `requested_grid`(107/187)와 정확 공통 저장 `all_exact_common_stored`(490/571) **네 파일 전부** max\|ΔV\| = **0.6170341087208 mV @0.002 s** · 표면 x 차 **1.0361978499567e-5 @0.002 s · N · z=52 µm** |

## 확인하지 않은 것

COMSOL 재실행 · java 소스 해시(보존 제외) · mph 해시 · 현지 현재 파일(867 개)의 보존 · 물성·OCP 의 물리적 정확성.
수신 측 ZIP 확인값과 역사적 333 보관 바이트는 **사용자 보고**이고 원본 영수증은 고치지 않았다.
