---
letter: EM
date: 2026-11-20
kind: internal independent review (prompt)
track: W_ad (DEM 협업) — 1저자 = 사용자
subject: 은 e70 far 재시도 a5 묶음 발송 전 독립 리뷰 (개정 5 v2 · HEAD 28ef1ea3)
reviewer: 새 에이전트 (도구를 만든 갈래 에이전트 · 주 세션과 맥락을 나누지 않음)
---

# EM 프롬프트 — a5 묶음 발송 전 독립 리뷰 (원문 요지)

- 대상: tools/wad/build_a5_vasp_package.py · tools/wad/build_v5_vasp_package.py (a5 부분: load_a5_result · a5_secondary · adopt_a5 · a5_dependency · _g4_status · check/collect/main 배선) · db/inputs/wad_a5_vasp_2026_11_20/ (업체가 받는 폴더) · 맥락 tools/wad/build_round2_vasp_package.py
- 정의: db/properties/wad_aprime_pilot_prereg_v5_amendment_5_e70_retry_2026_11_20.json (개정 5 v2 · 비준) · 판정 계약 · 상태 어휘 · 재시작 기록 · 0 스텝 규칙 · 반송 허용 목록은 개정 4 (…_amendment_4_e70_rerun_2026_10_15.json)
- 찾을 것 (우선순위): ① 거짓 채택 (개정이 금지한 값이 채택되는 경로) ② 업체 쪽 손상·손실 (보존 WAVECAR 원본 · 시도 폴더 덮어쓰기 · 금지 파일 반송 · 상한 · 중복 실행 · 잘못 이끄는 종료 코드/문구) ③ 거짓 거부 (실물 5.4.4 출력 해석 가정 · bash 와 Python 판정 불일치) ④ README · run_a5.sh 의 운영 사용성
- 이미 아는 것: ALGO All OSZICAR 행 머리 (SDA/CGA 예상) 실물 미확인 → 모르는 머리 = SCF_UNVERIFIED · 0 스텝 인프라 상한 = 잡 전체 2 회 (처리가 틀렸다고 보면만 다시 올린다)
- 규칙: 저장소 파일을 고치지 않는다 (scratch 에서만) · W 값을 찍거나 쓰지 않는다
- 회신: 심각도 (P0 거짓 채택·업체 데이터 손상 · P1 현실적 오동작 · P2 경계 · P3 문구) · 파일:줄 · 구체 실패 상황 · 가장 작은 고침 · 확인해서 괜찮았던 영역
