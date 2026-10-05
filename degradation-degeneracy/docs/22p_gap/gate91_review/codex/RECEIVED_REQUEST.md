# GATE91 리뷰 요청 — G90-N1 정정 결과 (환경 프로필 C 의 origin 축을 경로 검색 범위로 · 이름 · 범위 선언 · 문구 · C1 · 실행 GO 아님)

> 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

91차 게이트 리뷰 요청입니다 — 90차 회신 (`CONDITIONAL_ACCEPTANCE` · G90-N1 P2 · 비차단 C1) 의 정정 결과입니다. 실행 GO 요청이 아닙니다.

## 대상

| 항목 | 값 |
|---|---|
| 저장소 · 브랜치 | `yonghoon7153-source/Yonghoon-DEM-DFT` · `claude/dashboard-standby-e2f56971` |
| 요청 HEAD (발송 SHA) | `43056f78d845741b43357181fcfd64fc78a8ef0c` |
| 판정 대상 코드 | `b08bb6944b03511c97c8deeb38e6a347bbb1f1fb` — 90차 판정 대상 `e2160c2ef276d4944fa4ad76fbaa001671a1a95e` 뒤 RUN_SCOPE 를 바꾼 유일한 커밋 (`tools/env_profile.py` 1 파일 · +30 −17 · source_digest `3f84c0db52d2b9ac` → `f0175fff71132003`) |
| 요청문 | `degradation-degeneracy/docs/22p_gap/GATE91_REQUEST.md` |
| 고정 표 | `degradation-degeneracy/docs/22p_gap/PYBAMM_PIN_ROUND_SPEC.md` §13 — 코드 변경 전 커밋 `69b35f65dda21378287c94ec1fabaf98a2ca94d8` |
| 증거 | `degradation-degeneracy/docs/22p_gap/gate91_evidence/` — README 에 파일별 sha256 · 크기 |
| 발송 뒤 커밋 | `85c9cbe1162b6e4b01390345ff1dfb768c5a61cb` — 발송 HEAD docs-lint 원문 (증거 14) 과 README 한 줄씩만 더했다 |

## 실측 (제출자 원문 — 증거 파일 그대로)

| 항목 | 결과 |
|---|---|
| 전체 회귀 (clean `f27006370`) | pytest **2182 passed / 1 xfailed / rc 0** · strict smoke **rc 0** · 등록부 전체 재생 **412/412 · rc 0** |
| 발송 HEAD docs-lint | **358 passed / rc 0** · 2026-10-05T03:34:42Z → 04:00:40Z · 시작 = 끝 HEAD · dirty 0 (증거 14) |

## 판정 요청

1. **G90-N1** — 확인한 것이 "`PathFinder` 경로 검색 origin 의 RECORD 소속" 으로 좁혀졌고 (이름 · docstring · 요약 · stamp), 로드된 module origin 이
   **미측정**으로 결과에 스스로 선언되는가 (`not_measured`) · 원장 §137 의 최소 종결 조건 (1)–(4) 를 채우는가
2. **C1** — 기록 전용 (D3) 과 측정 기능 회귀 (e06 · e08) 의 적용 경계 문장
3. 이름 변경이 판정 논리 · lock · smoke · `make_receipt.py` 를 건드리지 않았는가
4. 회귀 · 변이 · 영수증 · 전체 회귀

자체 신고는 요청문 §6 a–h — 특히 **a** (90차 §8 "기존 시험 불변" 의 예외 — 이름 따라가기) · **b** (s02 = 검토자 반례의 고정) · **d** (유효 정정 대응) ·
**e** (C1 경계).

## 요청하지 않는 것

실행 GO · 실제로 로드된 module origin 의 측정 (선택지 C) · D guard · C 의 fail-closed · 설치 · lock 재생성 · 새 연구 leg · 운영 v6 계획 · 세대표 · p_ini ·
class · 투영 게시.
