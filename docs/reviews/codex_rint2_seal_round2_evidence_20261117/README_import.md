# Codex Rint ② 봉인 전 묶음 2/2 (11-17) — 반입 기록

- 판정문 = `docs/reviews/codex_review_rint2_seal_round2_20261117.md` — 받은 묶음 안 원본 FINAL_REVIEW_RINT2_SEAL_ROUND2_f40d005ac_20261117.md 22,848 B · sha256 a5e458b2320ecbc9e742be1d35a830db180e6ca28661bc9115250b10589a5a28 · CR 0 · 주소 꼴 0 → 리포 사본 = 원본과 바이트 같음.
- **판정 = 조건부 GO — 봉인 꼴 · 근거 승계 (봉인 준비) 에 한정 · 새 P1 0 · P2 0 · P3 0** · 네 미정값의 저자 결정과 최종 바이트 확인 전에는 봉인 완료가 아니다 · 연구 실행 · 정량 판정 · 운영 GO · 공유 원장 종결 = 미승인 (판정문 첫 줄 · §7 · 끝 줄).
- 리뷰 핀 = `f40d005ac` (f40d005acce19b6c363e5c10c8668ec081b56f2e · 원격 stoic) · 코드 핀 = `64e4d213e` · 봉인 꼴 후보 = c80d700bd (scratch 가지 seal-form-scratch · 부모 = 코드 핀 · Codex 가 Git 객체로 확인) · 우리가 보낸 ZIP = codex_rint2_seal_round2_f40d005ac_20261117.zip (13,280,385 B · 373 파일 · sha256 7da8e749ed0954d5777bffd0d16f86ce490e2b15ed371077f3174a88e1503f88) · Codex 입력 대조 = CRC · 경로 · 중복 · 목록 371 길이 / sha256 / blob 일치 · 원격 `repo/` 84/84 (판정문 §1).
- 받은 것 = 1저자가 대화에 올린 증거 ZIP (EVIDENCE_RINT2_SEAL_ROUND2_f40d005ac_20261117.zip · 14,533,771 B · sha256 98f95a774bd7be8e4cdb991ac27d8858b7d7f081465614933e50c33abe63b499 · 항목 432) · 빈 폴더에 `python3 -I` 로 풀어 검사 (위험 경로 0 · 중복 0 · CRC 이상 0 · 보통 파일만).
- 넣은 것 = **53 파일** (이 폴더 · ZIP 과 같은 상대 경로 · 목록 = `IMPORT_SHA256SUMS` · `_import_manifest.json`) — 그 가운데 **17 파일 = 윈도 사용자 홈 앞부분 가림** (세 꼴 `C:\Users\<계정>\` · JSON 의 두 겹 역빗금 꼴 · `C:/Users/<계정>/` → `<WINHOME>` · 그 밖 바이트 그대로 · 원본 길이 · sha256 = `_import_manifest.json` 의 `orig_*` 칸) · 나머지 36 = 바이트 그대로.
- 뺀 것 = **379** — `input/` 373 (우리가 보낸 요청 ZIP 의 사본 · `repo/` = 리뷰 핀 blob · `extra/` = scratch 기록 · stoic `f40d005ac` 의 요청서 · ZIP 도구 · 기록 묶음으로 다시 만든다) · 우리 리포 blob 사본 6 (`measurement_review/baseline_1113/` · docs/data/rint2_s0_sbe_20261113/ 의 같은 바이트 · 6,286,644 B kit JSON 포함).
- 우리 트리 재현 = 하지 않았다 — 새 지적 0 · 조건부 GO · 판정문 §7 의 조건 2 (최종 커밋 대조 · 봉인 관문) 는 이 세션이 실제 봉인 커밋에서 다시 잰다 (영수증 = docs/data/rint2_seal_receipts_20261118/).

## 처분 (1저자 11-17 · 본 세션)

| 판정문 | 처분 |
|---|---|
| §7-1 네 값 · 날짜 · 가지 · 정책 · 시간 가정이 바뀌면 예산 갱신 | 1저자 11-17 20:0x KST (결과 전 · σ 열람 0): `max_ladder_points` 16 · `calib_rj_ratio_max` "none" · `sv_cf_threshold` 1.5745499360744093 (= exp(G0/2) · G0 = ln(4.68/1.8877)) · `sv_cf_scope` "all3" · 봉인 날짜 20261118 · 가지 claude/rint2-seal-20261118 · 예산 = 3 판 모형으로 사다리 12 → 16 점 다시 셈 (봉인 기록 README §라) |
| §7-2 `--final` · 최종 커밋 대조 · 봉인 관문 영수증 | 봉인 커밋 (가지 claude/rint2-seal-20261118 · 코드 핀 위 문서 · 자료 한 커밋) · 영수증 = 그 커밋 sha 로 잰 기록 (stoic) |
| §7-3 "완료 보장 아님" · RCA-11 한정 종결 · env_unit ≠ 전체 실행 환경 · 환경 고정 계약의 기준 기록 · 확인 담당 | 봉인본 머리 절 · kgy 명령 문서 §3-1b 머리 · 봉인 기록 README §나 |
| Q7 RCA-11 | 원장 RCA-11 = **open 그대로** · 메모 = "이 R 의 입력 · 선택 고정 (u 입력 = 원래 MPM 경로 표본화 · s_min 0 · 계획 봉인) 만 한정 종결 · 전체 지적 = 부분" |
| Q3 시험 전용 값 (12 · none · 2.0 · all3) | 옮기지 않았다 — 넷 다 1저자 결정 (봉인 기록 README §가) |
| §6 R3-19 · 넘침 r 보수성 | 알려진 한정 그대로 (새 지적 아님) · 봉인 기록 README §나 |
