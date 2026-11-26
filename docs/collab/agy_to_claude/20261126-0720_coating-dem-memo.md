# 코팅 과정 DEM 가능성 메모 완료 · 인계 (2026-11-26 · agy 실무 → Claude)

| 트랙 | 완료 | 1저자 결정 (Q + 권고) | 다음 |
|---|---|---|---|
| 코팅 과정 DEM (논문 밖 · 개발 자료) | `docs/reviews/coating_dem_feasibility_memo_20261126.md` 작성 (5개 필수 항목 + 정본 litdb 23편 대조 · 계산/실행 0건) | **Q1**: Stage S0/S1 사전등록 초안 작성 착수 시점? **권고**: Rint ② 주 판정 마감(12-05) 전까지는 Rint 운영 1순위를 지키고, Rint 런 대기 틈에 **Stage S0 (호스트 단일상 MF 검증) 사전등록 초안만** 문서로 준비(발사 0). **Q2**: 이번 메모 반입 여부? **권고**: 반입(`cherry-pick -x`). | 1저자 "반입" 뒤 Claude 반입 → Q1 답에 따라 Stage S0 사전등록 초안 착수 |

## 0. 반입 메타

- **바탕 커밋**: `0f62d8eea` (`origin/claude/sdcp-dem-manuscript-si-pqwtv8`)
- **반입 대상 가지**: `agy/coating-dem-1126`
- **커밋 목록**:
  1. `<<sha:Add coating-process DEM feasibility memo and Claude handoff note>>` (1 커밋 · 새 파일 2 · 수정 0 · 삭제·이동 0 · 같이 쓰는 파일 수정 0)
- **바뀐 파일 (전부 신규)**:
  - `docs/reviews/coating_dem_feasibility_memo_20261126.md`
  - `docs/collab/agy_to_claude/20261126-0720_coating-dem-memo.md`
- **지운 · 옮긴 파일**: 없음
- **현장 실행 · 발사 · 계산**: 0 건 (문서 전용 · 개발 자료)
- **인계 ZIP**: 패치(`git format-patch`), `git patch-id --stable`, 변경 파일 바이트 사본, `SHA256SUMS`, `CHAIN.json`, `HANDOFF.md` 를 묶어 1저자에게 별도 전달.

## 1. 메모 요약 (5개 요구 항목 대조)

1. **먼저 볼 장치 꼴**: **메카노퓨전(MF) 꼴** (회전 원통 챔버 25 mm + 편심 고정 안쪽 원통 + 고정 긁개). 공기 항력 없이 정성 일치(`dave2003`), 현 B2 드럼(25.17 mm)과 지름 일치(`chen2004`), 실제 NCM811+LPSCl 코팅 장치(AMS-Mini, `kim2023` · `lee2026_lpscl`)와 직접 대응, 긁개·멱지수 내부 검증선 확보.
2. **규모 어림 (`ibb` NP 20 · 48 h 상한 · 전부 `[추정]`)**:
   - 실측 기준: B2-U 30.69 h (69.8 step/s), B2-C 33.82 h (63.4 step/s), B1-U 25.13 h (85.3 step/s).
   - 실입경(`CGF = 1`, $\Delta t \approx 1.4\text{–}1.7 \times 10^{-10}\,\text{s}$)은 불가; 현 B2 그대로(100k, 16.8–18.5 h/s)는 1.6 mm 틈 = `AM_P` 1.17 개로 뭉개짐; 전 3D 틈 해상(`CGF = 44.4`, 3.95M)은 1 s = 1,850–2,490 h 로 불가.
   - 실행 가능 절충: **Stage S0** (호스트 단일상 1,500–3,000 개, `gap/d = 4.0`, 2 s = **0.25–0.56 h**) + **Stage S1-A** (3상 1:9 보존, `CGF = 80`, z-주기 얇은 슬라이스 `1.44 mm`, 10 vol% 채움, $N \approx 89{,}300$, `gap 2.0 mm / d_AM_P = 2.78`, 0.5 s = **14.2–15.6 h**, 1.0 s = **28.3–31.2 h**).
   - 1 % 겹침 한계 속도를 지름 기준(`chen2004`, SE–SE 1.17 m/s)과 반지름 기준(우리 `in.mixer`, SE–SE 0.49 m/s) 두 규약으로 분리 검산해 고속 벽 꼬리 처리 원칙을 명시.
3. **4단계 (`충돌 → SE 파쇄 → 부착 → 소성`) 가능/불가**:
   - 현 LIGGGHTS-PUBLIC 3.8 덱으로 바로 가능: 충돌·유동·빈도/속도 계측, SE–SE 응집체 해쇄, SJKR 접촉 부착(진짜 JKR 부재 명시), `hooke/hysteresis` 접촉 이력 소산(`hooke/hysteresis + sjkr` 실측 `rc=0` 확인).
   - 현 덱 불가: 1차 SE 입자 파쇄(BPM + 0.01 ns 급), 항복압 캡 접촉(Thornton–Ning / EEPA 탑재 `[미확인]`), 입자 형상(SHAPE) 소성·연속 막 형성 → 대표 충돌 $(v_n, v_t, SI)$ 분포를 뽑아 **단일 충돌 MPM (`DEM → MPM`)** 으로 인계.
4. **피복률 및 공정 강도 지표**: 지속 부착 분율 $f_{\text{SE}\to\text{AM}}^{\text{pers}}(\tau)$ (주 지표), 미부착 SE·군집 분포, 호스트(`AM_P`/`AM_S` 분리) 배위수 분포 vs 포아송, 이산 입체각 피복 대리, 벽 공회전 분율 + 기능 영역 4등분 입자당 충돌 빈도(접촉 개시 1회 정의), $(v_n, v_t)$ 상위 분위수, Kwade $SI/SN$, 안쪽 조각 $F_n/F_t$ 및 축 비동력.
5. **첫 샌드박스 크기 및 끝 기준**: Stage S0 (4 팔, < 3 h) 통과 뒤 Stage S1-A (핵심 4 팔 + 보조 1 팔, 팔당 14–16 h) 진입; 비용(48 h 초과)·틈 막힘·지속 부착 신호 소실 시 호스트 전용 MF DEM → MPM/PBE 파이프라인으로 전환하는 명확한 중단 기준 포함.

## 2. 검증 결과

- **문헌 대조**: 인용 23편 전수 정본 `origin/claude/friendly-meitner-lldvar:litdb/papers/` 카드와 DOI·저자·연도·수치 직접 대조 완료(DOI 미인쇄 문헌 `pfeffer2001` 은 `[미확인]` + PII 표기, `lee2026_mechanical` 은 `our-lab` 자기인용 명시).
- **산술 검산**: PowerShell 수치 스크립트로 Rayleigh $\Delta t$, B1/B2 처리율, 4개 시나리오 및 S0/S1-A/B/C 입자 수·벽시계, Hertz 1 % 겹침 속도(지름/반지름 두 규약) 전수 재검산.
- **경로·SHA·비식별화 점검**: `scripts/check_doc_refs.py` 의 경로(`_RE_PATH`)·커밋 SHA(`_RE_SHA`) 정규식 기준으로 신규 두 파일 전수 점검(깨진 리포 경로 0, 도달 불가 SHA 0, 원격 호스트/계정/홈 경로 0, σ 값 0). *(Windows 환경에 Python 미설치 · WSL 접근 제한으로 `python3 scripts/check_doc_refs.py` 직접 실행은 반입 시 Claude 게이트에서 최종 확인 필요.)*

## 3. Claude 반입 시 공유 기록 제안

아래 줄을 `CLAUDE.md` (용훈 포메이션 Ⓒ 줄) 또는 `docs/session_20260923_progress.md` 에 반영 제안한다(이 커밋은 두 파일을 직접 고치지 않았다):

- `docs/session_20260923_progress.md`: `2026-11-26 [믹서 · 코팅 과정 DEM · agy 실무] 가능성 메모 완료 (docs/reviews/coating_dem_feasibility_memo_20261126.md · 개발 자료 · 결과 0 건 · 실행 없음): 1차 장치 꼴 = 메카노퓨전(MF, 25 mm + 편심 안쪽 원통 + 긁개), 규모 어림(S0 호스트 검증 0.3–0.6 h · S1-A 3상 1:9 CGF 80 얇은 주기 슬라이스 89k 0.5 s ≈ 14–16 h @ ibb NP 20 [추정]), 4단계 가능/불가(연속 막 → DEM→MPM 인계), 이산 피복·Kwade SI 지표, S0→S1 끝/전환 기준 정리.`
