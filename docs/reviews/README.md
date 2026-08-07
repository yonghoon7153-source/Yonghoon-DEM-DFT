# 웹앱 코드리뷰 스레드 (2026-08-07) — **종료**

Codex 와 6라운드 주고받은 기록. **차단 항목 0 으로 종료**했고, 남은 건 아래 §열린 항목 하나뿐이다.

| 라운드 | 문서 | 핵심 |
|---|---|---|
| 1 | (Codex 최초 리뷰, 대화 기록) | P1 5건 + P2 4건 |
| 2 | `webapp_review_response_2026_08_07.md` | 정본 레지스트리 도입 · 프로토콜 강제 · 쓰기 잠금 |
| 3 | `webapp_review_response_round2_2026_08_07.md` | LPSOCl β 게이트 · Windows 락 · live resolve |
| 4 | `webapp_review_response_round3_2026_08_07.md` | source_error · 실행 중 갱신 · 표·카드 상태 표시 |
| 5 | `webapp_review_response_round4_2026_08_07.md` | os.kill 안전버그 · comp2 의미 오류 · 배지 중복 |
| 6 | `webapp_review_response_round5_2026_08_07.md` | _alive 2차 · method_id 감사 7건 · metric UI 이관 |

최종 상태: 회귀 테스트 **32개** · 정본 레지스트리 **28/28 배선, 대조 실패 0** · 전 GET 라우트 200.

---

## 🔴 열린 항목 (하나)

**gap 정본 4종의 계통별 fixed-occ 실행 입력·출력 미확보** — `kb/open_items.md` §N.

값(comp1 2.066 / modelc 2.099 / b2o3 1.9671 / lpsocl 2.2309)을 의심하는 게 아니다.
정본 규칙이 "fixed-occ nscf 고유값만 인정" 인데 **그 값을 만든 실행을 파일로 재현할 수 없다.**
generic 템플릿(`tools/electronic/standard_dos/nscf_gap.in`)은 있고 `occupations='fixed'` 다 —
없는 건 계통별 실행본이다. 계통별로 남은 `*_nscf.in` 은 전부 `tetrahedra_opt`(DOS 용)다.

- 레지스트리 4항목에 `provenance_open`
- `validate_canonical.py` 가 매번 경고를 찍는다
- 화면 세 곳(`/compare` `/explorer` `/composition`)에 `출처⚠` 표식
  ⚠ status 는 **안 내렸다** — 값이 틀린 게 아니라 재현 불가라, 순위에서 빼면 과잉이다
- 닫는 순서: 찾기 → 백업 회수 → 재계산 / 등급 하향

---

## ⬜ 선택적 개선 (P3 — 차단 아님)

페이지 무게(`/cascade` 595 KB 등) · `dashboard_highlights` 본문 분리 ·
Windows 테스트 CI 배선 · 긴 툴팁·묶음 ID 가독성

---

## 이 스레드에서 얻은 방법론

| 라운드 | 검사가 통과해도 틀릴 수 있던 것 |
|---|---|
| 3 | **검사하는 경로 ≠ 쓰이는 경로** (validator vs 화면 / import 시점 vs 요청 시점 / 차트 vs 표) |
| 4 | **검사하는 축 ≠ 틀릴 수 있는 축** (수치는 맞고 method_id 가 다른 계산을 가리킴) |
| 5 | **검사하는 환경 ≠ 도는 환경** (POSIX 에서 맞는 API 가 Windows 에서 정반대) |
| 6 | **나눈 의미가 화면에 안 보임** (묶음을 쪼개 놓고 묶음 ID 를 안 찍음) |

실천 규칙 둘:
1. 플랫폼 분기를 쓸 때는 **그 플랫폼에서 실제로 태우는** 테스트를 같이 넣는다.
   구조 검사(이름·존재 확인)는 런타임 권한 오류를 못 잡는다.
2. 안전장치를 넣을 때 **그 값이 실제로 소비되는 모든 경로**를 먼저 센다.
   이번에는 순위·차트·레이더·표·카드·정렬·인용복사 7곳이었다.
