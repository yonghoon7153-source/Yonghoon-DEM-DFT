# Codex 믹서 10 차 (강성 축 등록 v2.6) — 반입 + 우리 재현 (2026-09-30 밤)

- 판정문: `docs/reviews/codex_review_mixer_highbo_round10_20260930.md` (= zip 의 `review.md` · 277 행 · sha256 `68c0d03fe2147e5b95a117f690f7d1a77bb689449c34e77d4958429974a10710`) — **새 P1 없음 · P2 셋 (`HBR10-01` · `02` · `03`) · 확인 18 런 HOLD 유지** · Q1 조건부 · Q2 개발 후보로 동의 · Q3 CONFIRMED · Q4 현재 덱 한정 동의.
- 반입 원본: 사용자 전달 zip `codex_mixer_highbo_round10_review_20260930.zip` — 895,739 B · sha256 `74dc3a5b89c622473475107ea15e0e562bb107ff492fd002bb29d5fcdb637320` · 162 파일 · `MANIFEST.json` **161/161 일치**.
- 이 폴더 = zip 의 `README.md` · `audit_round10.py` · `selftest_lf.py` · `package_evidence.py` · `review_status.json` · `MANIFEST.json` · SOURCE_PINS.json (zip 의 source 폴더에서 · 이 폴더 `docs/reviews/codex_review_mixer_highbo_round10_evidence_20260930/SOURCE_PINS.json`) · evidence 폴더 10 파일 + 우리 재현 (`_reproduction_audit_results_linux.json`).
  ⚠ 뺀 것: `source/` 소스 사본 (고정 커밋 `8e8474a68` 의 우리 파일 — **19/19 git blob 이 우리 HEAD 와 같다** · 나머지 3 = 공개 LIGGGHTS 소스 (upstream 핀 3d5c00f20519…) 파일) · `submitted/` (우리가 보낸 요청 묶음 사본).

## 우리 재현 — `audit_round10.py` 무변경 (Linux · Python 3.11.15 · numpy 2.4.6 · scipy 1.17.1 · `--lf-selftests` 없이)

| 대조 | 결과 |
|---|---|
| `evidence/audit_results.json` (Codex) ↔ `_reproduction_audit_results_linux.json` (우리) | rc 0 · 잎 838 ↔ 829 · **판정값 차이 0** — 다른 9 잎 = 우리가 돌리지 않은 `selftests_Linux_newline_emulation` 절 (Windows 에서 Linux 줄바꿈을 흉내 낸 selftest 기록) 뿐 |
| 그 안의 반례 | HBR10-01 경계 (기준 · dt/2 S_R² NaN → PASS · 필드 제거 → 소비자 오류 0) · HBR10-02 (AM–AM 0.02 % → soft WITHIN) · HBR10-03 정규화 반례 · Q3 36 F₀ 비 · Q4 NP20 정확 배분 반례 — 전부 Codex 와 같은 값 |
| 우리 selftest (Linux · 게이트) | Codex 가 Windows 에서 본 실패 (CRLF 텍스트 쓰기 · 0600 권한 · vault) 는 우리 게이트 (✓ 72 · ✗ 0 · `1e09f661d`) 에 없다 |

## 원장 (같은 커밋)

- `HBR10-01` · `02` · `03` 새로 (P2 · 열림).
- `SELF-70` → **verified** (Codex Q4 · 현재 생성 덱 한정 · "NP 20 에서는 어떤 런도 통과할 수 없다" 문장 철회 표지).
- `SELF-71` 열림 유지 (Q1 조건부 · HBR10-01 · 03 해제와 함께).

## 한정 (Codex 그대로)

- DEV7 원자료 (dump · log · 봉인 진단 JSON · blind_log) 는 Codex 입력에 없었다 — 0.732 · 0.892 · 1.018 % 등은 보고값이고, ×20 예측 (0.80 · 0.82 · 0.83 %) 은 그 보고값을 조건부 입력으로 쓴 산술이다 (통과 확률 · 안전 여유 인증 아님).
- 설치 바이너리 동일성 · 실제 미열람 이력 · 개발 런 완주는 인증하지 않았다.  ×20 개발 후보 동의는 새 E0 실측 통과 · 실행 봉인 · 발사 승인을 대신하지 않는다.
- 판정문 안의 `C:/Users/Administrator/Documents/Codex/…` 링크는 Codex 작업 폴더 경로다 (이 리포에 없다).
