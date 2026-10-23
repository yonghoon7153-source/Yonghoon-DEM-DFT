# [ULPR] 최종 전체 게이트 · 실제 인계 범위

- 가지: `codex/unloading-ulpr`. 이전 쪽지의 준비 단계 한 커밋 계획 뒤, 깨끗한 후보가 필요한 전체 게이트 계약을 확인하여 두 커밋으로 인계한다.
- 내용 후보: `<<sha:Fix ULPR resume ownership and dump validation>>`.
- 영수증·환경 증거 후속: `<<sha:Record ULPR full gate and environment compatibility>>`. 받는 쪽의 새 SHA 대응표를 부탁한다.
- 전체 게이트 결과·명령·환경·시작/종료·로그 지문·최종 문서 검사는 `docs/reviews/dem_unloading_ulpr_fix_evidence_20261023/full_gate_receipt.json`에 기록한다. 이 새 쪽지는 이전에 커밋한 쪽지나 독립 원보고서를 고치지 않는다.
- 깨끗한 내용 후보의 full gate 뒤 생산/공유 소스는 바뀌지 않았다. 후속은 증거·상태 기록뿐이며, 최초 실패 로그와 검토 당시 원본을 보존한다.
- 외부 반박 GO·발송·비준·실제 WSL/장비 실행을 뜻하지 않는다. LHS214 실제 WSL, 세대 2 언로딩 외부 GO, MXD2-01 HOLD/07 D3, D3 V2-Q1 미비준 한정은 해당 트랙에서 그대로다.

## 최종 환경과 이전 기록의 관계

최종 호환 환경은 pandas 2.3.3 + pytz 2026.5이며 NumPy 2.4.6은 유지했다. 승인된 작업 전용 TMPDIR은 `/var/tmp/codex-nonrint-20261023`이다. 이 패키지 상태가 최초 11:55 환경 쪽지의 당시 패키지 상태를 대체한다. 최초 쪽지와 실패 로그는 이력으로 보존하며 성공 결과로 합산하지 않는다. 전체 설치 스크립트의 최종 환경 재시험도 PASS다. 환경 설정 초안은 저장됐지만 Publish 적용이나 새 환경 복원 검증을 완료했다고 주장하지 않는다. 실제 최종 리뷰 커밋 핀은 전달 패키지 바깥 PIN에만 기록한다.
