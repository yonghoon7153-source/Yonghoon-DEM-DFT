---
title: Codex 리뷰 과제 — EIS·DRT·GITT 세 섹션
created: 2026-08-25
updated: 2026-08-25
type: guide
tags: [review, audit, crosscheck, eis, gitt]
sources: [docs/adr/0019-eis-is-its-own-section-with-two-fitting-worlds.md, docs/adr/0020-gitt-pairs-two-different-samples.md]
confidence: high
explored: false
verificationStatus: unverified
---

# Codex 리뷰 — EIS·DRT·GITT (b6df17bb..7b0531d1)

새 측정 세 종류가 통째로 들어왔다: BioLogic `.mpr` 리더, 등가회로 자동 피팅,
DRT, GITT(pOCV·확산계수), 그리고 화면 셋. 73개 파일, +11,143줄. **수치를
만들어 내는 코드가 대부분이라, 조용히 틀린 숫자가 가장 큰 위험이다.**

Claude 쪽에서도 같은 범위를 독립적으로 적대 리뷰 중이다. 두 결과를 교차해서
겹치는 것부터 닫는다. 그쪽 결과를 먼저 읽지 말 것 — 독립성이 교차검증의
값어치다.

## 1. 먼저 동기화

Codex 채팅에 그대로:

```text
클로드 작업하고 왔어

git fetch origin
git merge --no-ff origin/claude/battery-charge-discharge-webapp-dq4ja3

머지 후 확인:
  git log --oneline b6df17bb..HEAD | head -25
  git diff --stat b6df17bb..7b0531d1 | tail -3
```

`7b0531d1 feat: EIS·GITT 결과를 Origin 으로 옮긴다` 까지 보이면 준비된 것이다.
(그 뒤에 이 과제 문서 커밋과 리뷰 대응 커밋이 더 있을 수 있다 — 범위는
`b6df17bb..7b0531d1` 로 고정한다.)

## 2. 리뷰 과제 (붙여넣기)

```text
b6df17bb..7b0531d1 을 적대적으로 리뷰해줘. 결과는
docs/reviews/2026-08-25-codex-eis-gitt-result.md 로 같은 브랜치에 커밋해줘.

먼저 읽을 것 (코드보다 먼저):
- docs/adr/0019-eis-is-its-own-section-with-two-fitting-worlds.md
- docs/adr/0020-gitt-pairs-two-different-samples.md
- docs/adr/0018-formationless-schedules-anchor-at-cycle-one.md
- docs/raw/specs/biologic-mpr-format.md
- CLAUDE.md §0 (불변 규칙) — 특히 §0.1 raw 만 저장, §0.4 모르면 None.

규칙:
- 항목마다 **재현 또는 반례**를 적어라. 재현 없는 "의심됨" 은 별도 표로 분리.
- 스타일 지적은 받지 않는다. 잘못된 숫자를 만들거나, 조용히 데이터를 잃거나,
  화면이 거짓을 말하게 되는 결함만.
- 심각도: 높음(틀린 숫자가 측정값처럼 보임) / 중간(데이터·기능 손실) /
  낮음(혼란·불일치).
- 검증 실행:
    make check
    .venv/bin/python -m pytest packages/wrdkit/tests apps/api/tests -q
  실측 파일이 있으면 (없으면 합성 픽스처로만):
    WRDKIT_EIS_SAMPLE=/path/to.mpr .venv/bin/python -m pytest \
      packages/wrdkit/tests/test_eis_biologic.py packages/wrdkit/tests/test_eis_fit.py -q

공격 지점 (우선순위 순):

A. 부호와 단위가 네 층을 일관되게 통과하는가 — 가장 조용한 실패.
   .mpr 은 -Im(Z) 를 저장하고, 리더가 Im(Z) 로 뒤집고(eis/biologic.py),
   화면과 클립보드가 다시 -Z" 로 그린다(SpectrumDetail.tsx, origin.ts의
   nyquistTsv). 읽기→피팅→화면→복사 어디서든 한 번 더 뒤집거나 덜 뒤집는
   경로가 있는지. 특히: 클라이언트 fitCurve() 재계산(SpectrumDetail.tsx)이
   서버 피팅과 다른 곡선을 그릴 수 있는 회로(W/Ws/Wo/L 포함)가 있는지.

B. 물리 수식 검증 — 문헌과 대조해라.
   - Weppner-Huggins (wrdkit/gitt.py diffusion): D = (4/πτ)(mV_M/M_B S)²(ΔE_s/ΔE_t)².
     ΔE_s·ΔE_t 의 정의, IR 제거(펄스 앞 1/10 건너뜀), √t 원점이 펄스 시작인 것,
     τ 가 펄스 지속시간인 것. 시리즈 경계에서: 충전→방전 전환, min_rest_s 로
     건너뛴 휴지 뒤에 ΔE_s 가 무엇과 무엇의 차가 되는지 손으로 짚어봐라.
   - 전도도 (wrdkit/eis/derive.py): σ=L/(RA), 전체는 저항 합으로. 직렬 R0 제외.
     풀셀/구성 미정에서 전도도가 안 나오는 것까지.
   - DRT (wrdkit/eis/drt.py): 커널 1/(1+jωτ)·dlnτ, 비음수 구속, R_inf·L 을
     벌점에서 뺀 것, L 곡선 모서리 + 측정 대역 밖 봉우리 제외 규칙.

C. GITT 분할 (wrdkit/gitt.py segment_pulses).
   부호 있는 누적 용량을 CHARGE Q/DISCHARGE Q 의 차분 누적으로 만든다.
   그 두 컬럼은 **사이클마다 0 으로 리셋**된다 (CLAUDE.md §3). 다사이클
   GITT 파일에서 리셋 순간의 차분이 용량을 망가뜨리지 않는지 합성으로
   재현해봐라 (synthetic.make_gitt 는 cycle 0 고정이라 이 경로를 안 지난다).

D. 피팅 수치 (wrdkit/eis/fit.py).
   - 로그-시그모이드 경계 변환의 야코비안 역변환으로 stderr 를 되돌리는
     _standard_errors — 수학이 맞는지.
   - _order_arcs_by_frequency 가 값·오차를 같은 순열로 옮기는지.
   - 경계에 붙은 파라미터 보고, 미결정(determined) 문턱 0.5.
   - seed 를 바꿔도 (0..7) 같은 답이 나오는지 실제로 돌려봐라.

E. 이진 리더 (wrdkit/eis/biologic.py).
   - 컬럼 폭 표(COLUMNS)가 틀리면 어떻게 되나 — UnknownColumn 이 정말 모든
     경로를 막는지, end-anchor 검산이 우회되는 입력이 있는지.
   - .mpt: 'Nb header lines' 경계, 로케일 소수점, 열 수 불일치 행 처리.
   - .mps 짝짓기 (apps/web/src/pages/Eis.tsx upload): EC-Lab 은 .mpr 에만
     _C01 채널 접미사를 붙인다. 스템 비교가 그 접미사를 처리하는지.

F. API 데이터 무결성 (apps/api/app/routers/eis.py, gitt.py, storage.py).
   - 업로드 dedup(sha256), 셀 존재 검증, 삭제가 원본을 안 지우는 것(§0.2).
   - 실패한 피팅 저장, kind/kind_now 재라벨 규칙.
   - spectra npz 캐시가 사라졌을 때의 동작 vs GITT 의 재파싱-only 선택.
   - DB 에 raw 만 있는가 (§0.1) — 전도도·정규화 값이 저장되는 경로가 없는지.

G. 화면 (apps/web/src/pages/Eis.tsx, SpectrumDetail.tsx, Gitt.tsx,
   GittDetail.tsx, components/DrtPanel.tsx, CellSpectra.tsx, CopyBar.tsx,
   NavMenu.tsx).
   - 화면이 거짓을 말하는 경로: 미결정 파라미터가 숫자로만 보이는 곳,
     뺀 점을 말하지 않는 곳, 빈 그래프가 고장처럼 보이는 곳.
   - origin.ts 새 내보내기 여섯 개의 열 배치와 -- 규칙.

H. 작은 커밋들.
   - ADR 0018 (resolve_reference_cycle): 옛 행 추측 규칙이 사용자 입력을
     잃는 경로가 있는지. POST 로 만든 셀에 reference_cycle 을 함께 준 경우.
   - 셀 이름 인라인 수정 (CellName): 빈 이름, 동시 수정, Esc/blur 경합.
   - massFromName/thicknessFromName/cellConfigFromName 의 경계 정규식.

이미 알고 있는 것 (다시 보고하지 않아도 된다):
- 액체 전해질 EIS 는 실측 파일 검증이 없다 (전고체 .mpr 만 있음).
- GITT 는 합성 픽스처로만 검증됐다 — 실측 파일이 곧 온다.
- 전고체 피팅 회로는 사용자가 따로 줄 예정 (PRESETS/BY_CONFIG 교체 자리).
- knee 대표값(#36)은 결정 대기.

결과 문서 형식:
| # | 심각도 | 파일:줄 | 증상 (틀린 숫자/잃는 데이터/화면의 거짓) | 재현 | 제안 |
재현 못 한 의심은 별도 표로. 마지막에 "리뷰가 못 본 곳" 한 단락 —
시간이 없어 안 연 파일을 숨기지 말 것.
```

## 3. 끝나면

결과 문서가 커밋되면 Claude 쪽 리뷰 결과와 교차해서, 겹치는 것 → 한쪽만 본
것 → 서로 반박되는 것 순으로 처리한다. 대응 현황은 회답 문서에서 갱신한다.
