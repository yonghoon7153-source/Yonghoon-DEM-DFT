# 코팅 과정 DEM 구현 가능성 메모 (2026-11-26)

> **지위**: **개발 자료 · 문서만 · 결과 0 건 · 서버/계산 실행 0 건** · 논문 밖 구현 시도 (1저자 11-23 Q3 · 11-26 agy 실무 한 방향 넘김).
> **근거**: `docs/collab/claude_to_codex/20261123-2330_mixer-q1-q4-direction.md` 표 4 번 줄 · `docs/reviews/mixer_direction_feedback_20261123.md` (11-23 Q3) · `docs/collab/claude_to_codex/20261126-1022_coating-dem-status.md` · `CLAUDE.md` 용훈 포메이션 Ⓒ 줄.
> **값 표지**: `[인쇄]` = 정본 litdb 카드가 원문 인쇄값으로 확인 · `[판독]` = 정본 litdb 카드의 그림 판독값 · `[카드 산술]` = 정본 카드가 원문 값으로 계산 · `[리포]` = 이 리포 문서·덱의 실측/고정값 · `[추정]` = 이 메모의 산술·규모 어림(가정 병기) · `[미확인]` = 정본 카드 또는 리포에서 미확인(지어내지 않음).
> **문헌 원칙**: 모든 문헌 수치와 서지는 정본 `origin/claude/friendly-meitner-lldvar` 가지의 `litdb/papers/` 카드에서만 인용했다. 이 메모에 실행·발사 GO 는 포함되지 않으며, 어떤 샌드박스도 별도 사전등록과 1저자 GO 없이 실행하지 않는다.

---

## 0. 핵심 결론 (한 눈에 보기)

1. **먼저 볼 장치 꼴 → 메카노퓨전(Mechanofusion, MF) 꼴** (회전 원통 챔버 + 편심 고정 안쪽 원통/프레스 헤드 + 고정 긁개).
   - 텀블러(현 B2 드럼, `Fr = 0.0827`)는 중력 폭포(cascading) 혼합 체제라 코팅 응력이 없고, 칼날/Hybridizer 꼴은 공기 항력(CFD–DEM)과 초고속 충격(1 % 겹침 유지를 위해 강성 4.6–119 배 상향 필요)이 필수다. MF 꼴만 **공기 없이 정성 일치**(`dave2003` `[인쇄]`), **우리 드럼과 같은 챔버 지름(25 mm)**(`chen2004` `[인쇄]`), **실제 NCM811–LPSCl 건식 코팅 장치(Hosokawa AMS-Mini)와 직접 대응**(`kim2023` · `lee2026_lpscl` `[인쇄]`)을 동시에 만족한다.
2. **규모 어림 (`ibb` NP 20 · 벽시계 상한 48 h 기준, `[추정]`)**:
   - 실제 입경(`CGF = 1`, 1 µm SE, 실 영률 16.5–24 GPa)은 $\Delta t \approx 1.4\text{–}1.7 \times 10^{-10}\,\text{s}$ 로 장치 규모 1 s 계산이 원리적으로 불가하다(`dave2003` ≤ 10⁻⁹ s 장벽 확인).
   - 현 B2 덱 그대로(`CGF = 151.4`, $N = 100{,}000$, $\Delta t = 2.373 \times 10^{-7}\,\text{s}$) 25 mm MF 에 넣으면 1 s 가 **13.7–18.5 h** `[추정]` 이지만, 1.6 mm 틈이 `AM_P` parcel **1.17 개**뿐이라 틈 유동이 뭉개진다. 반대로 3D 전체에서 `틈 / d_AM_P = 4` (`CGF = 44.4`) 를 맞추면 $N \approx 3.95 \times 10^6$, 1 s 가 **1,850–2,490 h** (0.1 s 도 185–249 h) `[추정]` 으로 48 h 상한을 크게 넘는다.
   - **실행 가능한 절충**: (a) **Stage S0 (호스트 단일상 얇은 주기 3D MF, `N = 1,500–3,000`)** 은 2.0 s 가 **0.25–0.56 h** `[추정]` 으로 즉각 검증 가능하고, (b) **Stage S1 (3상 1:9 크기비 보존 · z-주기 얇은 슬라이스 `CGF = 80`, 10 vol% 채움, `N ≈ 89,300`, `gap 2.0 mm / d_AM_P = 2.78`)** 은 0.5 s 가 **11.6–15.6 h**, 1.0 s 가 **23.2–31.2 h** `[추정]` 으로 48 h 안에 들어온다.
3. **건식 코팅 4단계 (`충돌 → SE 파쇄 → 부착 → 소성`, `lee2026_mechanical` Fig. 1b) 가능성 구분**:
   - **현 LIGGGHTS 덱으로 바로 가능**: ① 충돌(유동·빈도·속도·소산 에너지), ② 중 **SE–SE 응집체 해쇄(de-agglomeration)**, ③ **parcel/접촉 수준 부착**(SJKR + 기하평균 `CED_ij` · 단 진짜 JKR 아님), ④ 중 **접촉 이력 소산**(`hooke/hysteresis`, 단 항복압 캡 없음).
   - **현 덱으로 불가**: ② 중 **1차 SE 입자 파쇄(comminution)** (수정 BPM 빌드 + 0.01 ns 급 Δt 필요), ④ 중 **입자 형상(SHAPE) 소성 · 연속 껍질/막 형성**.
   - **다중 규모 역할 분담**: DEM 은 **장치·parcel 규모 충돌 속도/에너지 분포 + 이산 SE-on-AM 피복·해쇄**까지 맡고, 연속 막 형성은 대표 충돌 조건을 뽑아 **단일 충돌 MPM (`DEM → MPM`)** 으로 넘긴다(`20261123-2330` 표 4 번 줄 · `dave2003` 3 가지 단일 충돌 경우와 정합).
4. **첫 샌드박스 끝 기준**: Stage S0 (스크레이퍼 유무 ~2 배 운동 세기 대조 · 안쪽 조각 힘 $F_n \propto \omega^{1.7\text{–}2.2}$ 확인) 통과 뒤에만 Stage S1 (3상 점착 MF 최소 스윕) 진입. 만약 1 % 겹침 계약과 틈 해상도를 지키며 48 h 안에 정상 피복·충돌 신호를 못 얻거나 CGF 아티팩트가 지배하면, 전장치 3상 DEM 확장을 멈추고 **호스트 전용 MF DEM (`SI`/`v_n` 분포 추출) → MPM/PBE 분리 파이프라인**으로 전환한다.

---

## 1. 먼저 볼 장치 꼴 선정 (메카노퓨전 vs 텀블러 vs 칼날)

### 1-1. 세 장치 꼴 비교

| 비교 축 | 메카노퓨전 (MF) 꼴 ★ **선정** | 텀블러 (회전 드럼 · 현 B2 덱) | 칼날 / 고전단 / Hybridizer 꼴 |
|---|---|---|---|
| **기하 · 구동** | 회전 원통 챔버 + 편심 고정 안쪽 원통(press head) + 고정 긁개(scraper) (`chen2004` `[인쇄]`) | 회전 원통 드럼 단일체 (`R = 12.58 mm`, `L = 5.03 mm`, `76.7 rpm`, `in.mixer` `[리포]`) | 고속 회전 날(블레이드/로터) + 고정/회전 용기 + 순환관(Hybridizer) 또는 좁은 벽 틈(Nobilta · Eirich) |
| **지배 응력 체제** | 원심 압축(`Fr ≫ 1`, 2000 rpm 시 `Fr = 55.9` `[카드 산술]`) + 수렴 틈 고전단·압축 충돌; **입자–입자 / 입자–경계 ≈ 7** (`chen2004` `[카드 산술]`) | 중력 폭포(cascading) 체제(`Fr = 0.0827`, 벽 속도 `0.101 m/s`, `mellmann2001` 창 안 `[리포]`) — 저에너지 분산·유동화 | **Hybridizer**: 고속 날·벽 충격 지배(**경계/입자 ≈ 940**, `dave2003` `[판독 · 카드 산술]`, 실기 날 끝 `50–100 m/s`, `kawaguchi2017` · `kawaguchi2018` `[인쇄 · 카드 산술]`). **Nobilta/Eirich**: 날 끝 `4–40 m/s` (`kissel2026` · `wolf2026` · `lischka2025` `[인쇄]`) |
| **공기(유체) 결합 필요성** | **불필요(1차 근사)**: 공기 없이 실험·운동론과 정성 일치 (`dave2003` p.452 `[인쇄]`) | 불필요 (저속 중력 유동) | **Hybridizer 필수** (*"one must include the effect of the fluid … drag force"*, `dave2003` p.452 `[인쇄]`); Eirich 도 10 µm 실입자 `St ≲ 0.1` 로 단방향 CFD 항력 사용 (`hare2026` `[인쇄]`) |
| **충돌 속도 vs 우리 B2-U 1 % 겹침 계약** | 2000 rpm 법선 평균 `0.285 m/s` (`chen2004` `[판독]`) → SE–SE 겹침 `0.32 %`(지름 기준) / `0.65 %`(반지름 기준) `[추정]` (평균은 계약 안; 벽 속도 `2.62 m/s` 꼬리만 초과) | 벽 속도 `0.101 m/s` → `0.14 %`(지름) / `0.28 %`(반지름) `[추정]` — 코팅 응력 부족 | Hybridizer 축소 3D 평균 `2.50–12.74 m/s` (`dave2003` `[판독]`) → 지름 기준 `1.8–6.8 %` 초과, 1 % 유지에 **E 4.6–119 배 · Δt 0.47–0.09 배** 필요 (`dave2003` §7-2 `[카드 산술]`) |
| **황화물 NCM–SE 건식 코팅 실험 대응** | **직접 대응**: Hosokawa AMS-Mini 로 NCM811+LPSCl 233–628 nm 코어–셸 실증 (`kim2023` · `lee2026_lpscl` `[인쇄]`: 틈 3 mm, 긁개 ~0.4 mm, 2000–5000 rpm) | 건식 코팅 선례 없음 (`pfeffer2001` `[인쇄]`: 건식 코팅은 MF 200–1600 rpm · Hybridizer 5000–16,000 rpm 등 고에너지 장치 필요) | 실증 다수 (`kawaguchi2017`/`2018` · `nakamura2020` Hybridizer, `hayakawa2022` 고전단 칼날, `kissel2026`/`wolf2026` Picoline Nobilta) — 단 벽 부착 SE 손실 큼 (`hayakawa2022` 14.5–27.1 % · `kawaguchi2018` 30→20.24 wt% `[인쇄]`) |
| **현 LIGGGHTS 덱 전환 비용** | **최소**: 기존 25.17 mm 드럼 메시 재사용 + 고정 안쪽 원통 STL + 고정 긁개(STL 또는 고정 구) 추가, 회전수·축 방향만 변경 | 변경 없음 (이미 구현 · 단 코팅 공정 아님) | 높음: 고속 회전 다중 날 메시 + 순환관(또는 출구 재투입 로직) + CFD–DEM 결합 + 높은 강성·작은 Δt |

### 1-2. 메카노퓨전(MF) 꼴 선정 근거 4가지와 한정어

1. **현 덱과의 기하 호환성**: `chen2004` 의 모형 MF 챔버 지름은 **25 mm** (`[인쇄]` 표 1)로, 우리 현 B2 드럼 지름 **25.1665 mm** (`R = 12.583 mm`, `in.mixer` `[리포]`)와 사실상 같다. 기존 `make_mixer_deck.py` 의 원통 회전 메시·3상 parcel·SJKR 기하평균 점착(`D2`)을 유지한 채 **고정 편심 원통과 고정 긁개만 추가**하면 최소 MF 덱이 성립한다.
2. **유체 결합 없이 검증 가능한 유일한 고에너지 코팅 꼴**: `dave2003` (p.452 `[인쇄]`)는 세 코팅 장치 중 **MF 만 공기 항력 없이 실험과 정성 일치**한다고 명시했다. 반면 Hybridizer 는 공기 순환이 본질이라 진공 DEM 이 보수적 하한에 그치고(`dave2003` p.460–461 `[인쇄]`), 고속 날 충격 때문에 강성 상향 비용이 폭증한다.
3. **실제 황화물 양극 건식 코팅 문헌과 직접 연결**: NCM811 위에 실제 LPSCl 껍질을 만든 `kim2023` 및 `lee2026_lpscl` 이 모두 **Hosokawa AMS-Mini 메카노퓨전**(프레스 헤드 틈 3 mm · 긁개 틈 ~0.4 mm · 2000–5000 rpm, `[인쇄]`)을 썼다. 또한 `wolf2026` (`[인쇄]`)은 소립 NCM85 (3.8 µm) 가 배치 Nobilta (3000 rpm) 에서 코팅되지 않는 반면 대립 NCM (8.7 µm, 운동에너지 ∝ $D^3$ ≈ 12 배) 은 코팅됨을 보여, **호스트 입경(우리 PC 9 µm vs SC 4 µm, $(9/4)^3 = 11.4$ 배)에 따른 코팅 차**를 MF 꼴에서 직접 질문할 수 있다.
4. **내부 검증 기준선이 존재**: `chen2004` (`[판독 · 인쇄]`)가 긁개 유무 대조(운동 세기 2.37 배 · 법선 충돌 속도 2.0 배 · 벽 고리 회전 KE 9.6 배 변화)와 안쪽 조각 법선 힘의 회전수 멱법칙($F_n \propto \omega^{1.98}$, $F_n/F_t \approx 4.4\text{–}4.6$)을 제공하므로, 점착·게스트를 넣기 전에 **무점착 호스트만으로 덱의 물리 건전성을 먼저 검증**할 수 있다.

> **한정어 (떼지 말 것)**: (i) **긁개(scraper)는 생략 불가** — `chen2004` · `dave2003` (`[인쇄]`)에서 긁개를 빼면 원심력으로 입자가 벽에 달라붙어 강체 회전하므로 법선 충돌 속도와 운동 세기가 반감한다. (ii) **MF 꼴의 결과는 Hybridizer·RAM·압출기로 크기 전이 불가** — `wolf2026` (`[인쇄]`)이 보였듯 전단 지배(압출)와 충격/압축 지배(배치 MF)는 같은 비에너지라도 다른 피복 거동을 낸다. (iii) `chen2004` 의 모형은 2D 무점착·단분산·무중력·연화 강성(`K1 = 20,000 N/m`)이므로, **경향·지수·영역 순위만** 대조하며 힘의 절대값은 옮기지 않는다.

---

## 2. 규모 어림 (입자 수 · Δt · 1 s 계산 시간 · ibb NP 20 기준)

### 2-1. 실측 기준선 (`ibb` Slurm · QOS `cpu-60` · NP 20 · 벽시계 상한 48 h)

우리 기계(`ibb`, NP 20, 60 코어 한도 = 동시 최대 3 슬롯, 잡당 최대 벽시계 48 h `[리포]`)에서 실측된 믹서 LIGGGHTS 성능은 다음과 같다(`docs/reviews/mixer_b2_pair_return_20261124/README.md` · `docs/reviews/mixer_b1_pair_return_20261122/README.md` · `PRECAL_R1_B2_C/in.mixer` `[리포]`):

| 실측 기준 런 | 입자 수 $N$ (`AM_P / AM_S / SE`) | `CGF` | $\Delta t$ (s) | 총 step (정착+2바퀴, 1.831 s) | 실측 벽시계 (NP 20) | 처리율 (step/s) | 처리율 (atom·step/s) |
|---|---|---:|---:|---:|---:|---:|---:|
| **B1-U** (저점착 `Bo_SE 0.212`, `368139`) | 100,000 (143 / 699 / 99,158) | 151.4 | $2.373 \times 10^{-7}$ | 7,716,595 | 25 h 07 m 43 s (25.13 h) | 85.30 | $8.53 \times 10^6$ |
| **B2-U** (강점착 비코팅 `Bo_SE 21.244`, `368758`) | 100,000 (143 / 699 / 99,158) | 151.4 | $2.373 \times 10^{-7}$ | 7,716,595 | 30 h 41 m 30 s (30.69 h) | 69.84 | $6.98 \times 10^6$ |
| **B2-C** (강점착 코팅 `Bo_SE 21.244`, `369734`) | 100,000 (143 / 699 / 99,158) | 151.4 | $2.373 \times 10^{-7}$ | 7,716,595 | 33 h 49 m 07 s (33.82 h) | 63.38 | $6.34 \times 10^6$ |

- **시간 간격 규칙 (`scripts/make_mixer_deck.py` `[리포]`)**: 상별 Rayleigh 시간의 20 %, $\Delta t = 0.2 \, \frac{\pi r \sqrt{\rho / G}}{0.1631\nu + 0.8766}$ ($G = E/[2(1+\nu)]$). B2 물성(`AM 4.85`, `SE 1.64 g/cm³`, `E_AM = 1.037 GPa`, `E_SE = 200 MPa`, `ν_AM = 0.25`, `ν_SE = 0.30`)에서 상별 $\Delta t$ 는 `SE 2.373×10⁻⁷ s`, `AM_S 7.092×10⁻⁷ s`, `AM_P 1.596×10⁻⁶ s` 로 **SE 가 Δt 를 결정**한다.
- **비용 비례 가정 `[추정]`**: 접촉 밀도·도메인 부하 균형·덤프 I/O 비중이 B2 와 같다고 가정하고 벽시계 $\propto N \times N_{\text{step}}$ 로 옮긴다. 점착이 강하거나 원심 압축으로 틈 구역 입자 밀도가 편중되면 MPI 부하 불균형으로 **실제 시간이 아래 어림보다 1.3–2 배 더 들 수 있다** `[추정]` (정확한 값은 짧은 벤치마크 1 회로 실측 필요).

### 2-2. 시나리오별 1 s (및 0.5 s) 물리 시간 규모 어림 `[추정]`

기준 MF 기하: 챔버 지름 $D = 25\,\text{mm}$, 안쪽 원통 $D_{\text{in}} = 10\,\text{mm}$ (자유 단면적 $A_{\text{MF}} = \pi(12.5^2 - 5^2) = 412.3\,\text{mm}^2$), 회전수 2000 rpm ($33.3\,\text{rev/s}$, 벽 속도 $v_{\text{wall}} = 2.62\,\text{m/s}$, $Fr = \omega^2 R / g = 55.9$). 조성은 현 B2 활성상 3상 비율(`AM_P 57.14 : AM_S 24.49 : SE 18.37 wt%`, `r_AM_P : r_AM_S : r_SE = 9 : 4 : 1`) 기준이다.

| 시나리오 | CGF (`d_AM_P` / `d_SE`) | 틈 $h$ ($h / d_{\text{AM\_P}}$) | 축 길이 $L_z$ · 채움 | 입자 수 $N$ (`AM_P / AM_S / SE`) | $\Delta t$ (s) | 1 s step 수 | **1 s 벽시계 `[추정]`** (NP 20, B2-U ~ B2-C; 괄호 B1-U) | 판정 (48 h 상한) |
|---|---|---|---|---:|---:|---:|---|---|
| **A. 실입경 미시 (CGF = 1)** | 1 (9 µm / 1 µm, 실 $E_{\text{SE}}$ 16.5–24 GPa) | 1.6 mm (178) | 5.03 mm · 18 % | $\approx 3.47 \times 10^{11}$ (100k 만 잘라도 불가) | $1.43\text{–}1.73 \times 10^{-10}$ | $5.8\text{–}7.0 \times 10^9$ | $N=10^5$ 만 잡아도 **23,050 h (2.6 년)** (전 챔버 불가) | ⛔ **원리적 불가** (`dave2003` ≤ 10⁻⁹ s 장벽) |
| **B. 현 B2 덱 그대로 MF** | 151.4 (1.363 / 0.151 mm, $E_{\text{SE}}$ 200 MPa) | 1.6 mm (**1.17**) | 5.03 mm · 18 % | 100,000 (143 / 699 / 99,158) | $2.373 \times 10^{-7}$ | $4.21 \times 10^6$ | **16.8 – 18.5 h** (13.7 h) | ⚠ 시간은 가능하나 **틈 = AM_P 1.2 개로 뭉개짐** |
| **C. 전 3D 틈 해상 (`gap/d = 4`)** | 44.44 (0.400 / 0.044 mm, $E_{\text{SE}}$ 200 MPa) | 1.6 mm (4.00) | 5.03 mm · 18 % | $\approx 3.95 \times 10^6$ | $6.966 \times 10^{-8}$ | $1.44 \times 10^7$ | **2,257 – 2,487 h** (1,848 h) · 0.1 s 도 226–249 h | ⛔ **48 h 상한 초과** (불가) |
| **D0. Stage S0 (호스트 단일상 검증)** | 44.44 (AM_P 0.400 mm 단일, $E_{\text{AM}}$ 1.037 GPa) | 1.6 mm (4.00) | 1.6 mm (`4d`, z-주기) | **1,500 – 3,000** | $4.684 \times 10^{-7}$ | $2.13 \times 10^6$ | 1 s: **0.13 – 0.28 h** · 2 s: **0.25 – 0.56 h** | ✅ **즉시 가능** (1 h 미만; `chen2004` 대조) |
| **D1. Stage S1-A (3상 1:9 · 얇은 주기 슬라이스 ★ 주추천)** | **80** (0.720 / 0.080 mm, $E_{\text{SE}}$ 200 MPa) | **2.0 mm (2.78)** | 1.44 mm (`2d`, z-주기) · **10 vol%** | **89,258** (128 / 624 / 88,506) | $1.254 \times 10^{-7}$ | $7.98 \times 10^6$ | 1 s: **28.3 – 31.2 h** (23.2 h) · **0.5 s: 14.2 – 15.6 h** (11.6 h) | ✅ **48 h 안** (1:9 크기비·3상 그대로 유지) |
| **D2. Stage S1-B (3상 1:9 · 완화 CGF)** | 100 (0.900 / 0.100 mm, $E_{\text{SE}}$ 200 MPa) | 2.5 mm (2.78) | 1.80 mm (`2d`, z-주기) · 15 vol% | **85,687** (123 / 599 / 84,965) | $1.567 \times 10^{-7}$ | $6.38 \times 10^6$ | 1 s: **21.7 – 24.0 h** (17.8 h) · **0.5 s: 10.9 – 12.0 h** (8.9 h) | ✅ **48 h 안** (여유 큼 · 단 `gap/R` 커짐) |
| **D3. Stage S1-C (2상 1:5 비대칭 CGF 대안)** | `AM` 50 (0.450 mm) / `SE` 90 (0.090 mm) | 1.8 mm (**4.00**) | 1.80 mm (`4d`, z-주기) · 15 vol% | **117,951** (1,401 / 0 / 116,550) | $1.411 \times 10^{-7}$ | $7.09 \times 10^6$ | 1 s: **33.3 – 36.7 h** (27.2 h) · **0.5 s: 16.6 – 18.3 h** (13.6 h) | ✅ **48 h 안** (`gap/d=4` 확보 · 크기비 완화 한정) |

- **얇은 z-주기 슬라이스의 근거**: `chen2004` (§3-3, 그림 10 `[판독 · 카드 산술]`)가 2D 와 z-주기 3D(두께 10 지름) 를 비교해 운동 세기 지표 차 **+2.3 %**, 평균 충돌 압력 차 **+10.6 %** 임을 보였다(양 끝 강체 벽 3D 는 충돌 압력 +16.7 %). 0.4 s 안에 정상 상태에 도달하므로(`chen2004` `[판독]`), `2000 rpm` 기준 **0.5 s (= 16.7 회전) ~ 1.0 s (= 33.3 회전)** 구간으로 정상 유동과 초기 충돌·부착 통계를 뽑을 수 있다.
- **10 vol% 채움 근거**: `kissel2026` (`[인쇄]`) 의 Picoline Nobilta 배치도 진밀도 기준 고체 충전율 10 vol% (`4.91 mL / ~49 mL`) 에서 운전했으며, `chen2004` 의 채움 스윕 하한도 2D 면적 분율 15 %(`500 개`)였다.

### 2-3. 고속 회전 시 Hertz 1 % 겹침 계약 점검 `[추정]`

현 B2 덱의 SE 강성(`E_SE = 200 MPa`, `E_AM = 1.037 GPa`, `E_wall = 1.48 GPa`)에서 두 입자(또는 입자–벽) 탄성 충돌 $\frac{1}{2} m^* v_n^2 = \frac{8}{15} E^* \sqrt{R^*} \delta_{\max}^{5/2}$ 로 1 % 겹침 한계 속도 $v_{n,1\%}$ 를 검산하면, **겹침 정규화 규약에 따라 두 값이 갈린다**(이 차이를 등록 전에 반드시 고정해야 한다):

| 정규화 규약 | SE–SE $v_{n,1\%}$ | SE–벽 $v_{n,1\%}$ | AM_P–벽 $v_{n,1\%}$ | 평균 충돌 $0.285\,\text{m/s}$ (`chen2004`) | 1000 rpm 벽 $1.31\,\text{m/s}$ | 2000 rpm 벽 $2.62\,\text{m/s}$ |
|---|---:|---:|---:|---|---|---|
| **지름 기준 $\delta/\min(d) \le 1\%$** (`chen2004` p.124 규약) | 1.17 m/s | 1.30 m/s | 1.40 m/s | **0.32 %** (계약 안) | **1.10 %** ($E$ ×1.3) | **1.91 %** ($E$ ×5.0 필요 → $\Delta t \times 0.45$) |
| **반지름 기준 $\delta/\min(r) \le 1\%$** (우리 `in.mixer` L31 규약) | 0.49 m/s | 0.55 m/s | 0.59 m/s | **0.65 %** (계약 안) | **2.19 %** ($E$ ×7.1) | **3.82 %** ($E$ ×28.5 필요 → $\Delta t \times 0.19$) |

> **운용 함의 `[추정]`**: 2000 rpm 에서도 **평균** 법선 충돌 속도(`0.285–0.424 m/s`, `chen2004` 그림 16 `[판독]`)는 **두 규약 모두 1 % 안**(지름 0.32–0.44 %, 반지름 0.65–0.89 %)이다. 문제는 벽·스크레이퍼에 정면 충돌하는 **고속 꼬리**(`1.3–2.6 m/s`)다. 반지름 1 % 를 꼬리 최대값에 강제하려고 $E_{\text{SE}}$ 를 28.5 배 올리면 $\Delta t$ 가 $1/5.34$ 로 줄어 S1-A 0.5 s 가 ~75–83 h 로 48 h 를 넘는다. 따라서 첫 샌드박스에서는 (i) **속도 창을 `1000 rpm` ($Fr = 14.0$, 벽 $1.31\,\text{m/s}$) 과 `2000 rpm` ($Fr = 55.9$, 벽 $2.62\,\text{m/s}$) 두 점**으로 두고, (ii) 겹침은 최대값 하나뿐 아니라 **중앙값·p99·p99.9·최대값 분포를 모두 기록**하며, (iii) 지름 1 % vs 반지름 1 % 초과 빈도가 1 %를 넘으면 $E_{\text{SE}}$ 상향(×2–5) 감도 점검 또는 속도 하향을 택한다.

---

## 3. 건식 코팅 4단계 중 현 LIGGGHTS 덱으로 바로 되는 것 / 안 되는 것

기준 4단계는 우리 랩 공저 논문 `lee2026_mechanical_halogen_argyrodite_drycoating` Fig. 1b (`[인쇄]`, **our-lab 자기인용 표기**) 의 **`① 충돌 → ② SE 파쇄 → ③ 부착 → ④ 소성·치밀화(연속 막)`** 순서다. 아래 표는 우리 `ibb` 바이너리(LIGGGHTS-PUBLIC 3.8 계열, 3d5c00f, `docs/dem1/dem1_kit/test/build_liggghts.sh` `[리포]`)에서 **이미 실측 검증된 것**과 **불가능하거나 별도 구현이 필요한 것**을 가른 결과다.

| 단계 | 물리 현상 | 현 LIGGGHTS 덱으로 바로 되는가 | 지금 덱에서 쓸 수 있는 것 (검증됨) | 안 되는 것 · 구조적 한계 (문헌 근거) | 대안 / 다중 규모 처리 |
|---|---|---|---|---|---|
| **① 충돌** | 호스트–게스트 · 게스트–게스트 · 입자–벽/안쪽조각/긁개 고속 충돌, 원심 유동, 전단대 통과 | **✅ 바로 됨** | `pair_style gran model hertz` (또는 `hooke/hysteresis`), `fix mesh/surface/stress`, `fix move/mesh`, `compute pair/gran/local`, `compute wall/gran/local` (`make_dem_gen2_decks.py` L244–247 `[리포]`) | 연화 강성에서는 **순간 최대 힘·접촉 시간이 부정확**(정성값) — `chen2004` p.133 `[인쇄]`. `pair/gran/local` 의 `force_normal` 은 법선 모델 힘이 아니라 **쌍 전체 힘의 중심선 사영** (`p1_g2c_source_check_20261104.md` §7 `[리포]`) | 순간 힘 대신 **시간 적분량(운동량 전달 · 소산 일 · Kwade 응력 세기 SI · 상대 충돌 속도 분포)** 을 주 지표로 사용 |
| **② SE 파쇄** | (a) **SE–SE 응집체 해쇄(de-agglomeration)**<br>(b) **1차 SE 입자 파쇄(comminution / breakage)** | (a) **✅ 바로 됨** (parcel 군집 단위)<br>(b) **⛔ 안 됨** | (a) `cohesion sjkr` + D2 `CED_ij` 행렬로 SE–SE 군집 형성·분열·크기 분포 추적 가능 (B2 반환 판독기 이미 보유, `mixer_b2_pair_return_20261124/README.md` `[리포]`) | (b) 강체 구는 쪼개지지 않는다. `xu2023` (`[인쇄]`) 은 **수정 LIGGGHTS BPM 빌드**(하위 구 1.59 µm, $\Delta t = 0.01\,\text{ns}$, 압연 2–9 일/28 코어)를 썼고, `tovar2026` (`[인쇄]`) 은 단일 응집체(15,215 결합구, $\Delta t = 2.2\,\text{ps}$)의 210 ns 충돌만 풀었다. 우리 `ibb` 바이너리의 `bond/gran` 포함 여부는 `[미확인]` | 장치 규모 DEM 은 **(a) 응집체 해쇄 + 충돌 에너지 분포**만 풀고, (b) 1차 파쇄는 `asylbekov2023` (`[인쇄]`) 처럼 **DEM 응력 분포 → 0D PBE** 단방향 연계 또는 단일 입자 파쇄 모델로 분리 |
| **③ 부착** | (a) **반데르발스 점착에 의한 parcel 접촉·지속 부착**<br>(b) **진짜 JKR · 정전기 · 기계화학적 결합** | (a) **△ 부분 가능 (대리)**<br>(b) **⛔ 안 됨** | `cohesion sjkr` + D2 기하평균 `CED_ij` 행렬 (`make_mixer_deck.py` `[리포]`). 또한 `hooke/hysteresis + cohesion sjkr` 조합은 우리 바이너리에서 **실측 통과(`rc=0`)** (`dem_scripts/mixing_cohesion_20260919/probe/README.md` `[리포]`: `soft_particles yes` + 키워드 순서 `tangential history cohesion sjkr rolling_friction cdt` 필수) | **LIGGGHTS-PUBLIC 에는 진짜 JKR 이 없다**(`sjkr`, `sjkr2`, `easo_capillary`, `washino_capillary` 뿐 — `mixing_model_design_20260919.md` §19-1 `[리포]`). SJKR 은 $F = \text{CED} \cdot A_{\text{contact}}$ 부피형이라 pull-off 목 늘어남·접촉 전 도약이 없다. 또한 **CGF parcel 의 $\gamma$ 는 실물 $\gamma$ 로 직접 옮길 수 없고**(`lischka2025` §4.3 · `hare2026` §4.3 `[인쇄 · 카드 산술]`) 무차원 Bond 수·상대비($\gamma_{\text{AM}}/\gamma_{\text{SE}}$)로만 다뤄야 한다. 정전기·표면 화학 결합 없음 | 점착은 **상별 대비($\gamma_{\text{AM}}/\gamma_{\text{SE}}$)와 `Bo_code`** 로 스윕하고, 절대 코팅 접착력(`W_ad`)의 실물 연결은 향후 1저자 SE 콜로이드 탐침 AFM 실측 뒤 보정 |
| **④ 소성 · 치밀화** | (a) **접촉 수준 이력 소산 (CONTACT plasticity)**<br>(b) **항복압 캡 접촉(Thornton–Ning / EEPA)**<br>(c) **입자 형상(SHAPE) 소성 · 합체 · 연속 껍질 형성** | (a) **✅ 바로 됨** (`hooke/hysteresis`)<br>(b) **⛔ 현 덱 없음**<br>(c) **⛔ 강체 구 DEM 원리 불가** | (a) `hooke/hysteresis` (`luding2008` eq. 6: `k1`, `k2_max` m6, `k_c` m7, `phi_f` m8) 가 잔류 겹침 $\delta_0$ 와 이력 소산을 제공하며, `cohesion sjkr` 와 동시 구동 검증됨 | (b) `hooke/hysteresis` 는 구간 선형이라 경도/항복압 캡($p_y$)이 없고 대변형에서 한계가 있다(`luding2008` 카드 · `litdb/elasto_plastic_feasibility.md` §0, §5 `[리포]`). `kissel2026` 이 쓴 `Thornton–Ning` (1998) 은 상용 Rocky, `thakur2014` 의 `EEPA` 는 우리 `ibb` 바이너리 탑재 여부 `[미확인]`.<br>(c) **강체 구는 절대로 납작해져 연속 15–500 nm SE 막으로 합체하지 못한다**(`litdb/elasto_plastic_feasibility.md` §0 · `dave2003` p.469 · `kawaguchi2018` · `lee2024` · `wolf2026` `[인쇄]`) | **(a)** 는 S1 감도 팔에서 `hertz` vs `hooke/hysteresis` 로 비교 가능.<br>**(c) 연속 막 형성은 DEM 밖**: DEM 이 뽑은 대표 충돌 속도·에너지 분포 `(v_n, v_t, SI)` 를 **`DEM → MPM 단일 충돌`** (SE J2 소성 · `dave2003` p.468–469 의 세 경우: 호스트 충돌 · 벽 충돌 · 두 면 사이 압축) 로 넘겨 판정 |

- **추가 미포함 물리 (현 덱 밖 · 한정어 유지)**: (i) **열 발생·SE 표면 열화** — `chen2004` (p.122 `[인쇄]`)는 MF 의 열기계 에너지를, `wolf2026` (`[인쇄]`)은 100 °C 혼련 시 LPSCl 표면 상순도 하락(XPS S 2p 97 % → 60 %)을 보고했으나 현 DEM 은 등온(열 0)이다. (ii) **공기 항력** — MF 꼴에서는 1차 생략 가능하나(`dave2003`), Hybridizer 로 확장 시 CFD–DEM 이 필요하다.

---

## 4. 피복률 및 공정 강도 지표 (무엇을 재고, 무엇을 재지 않는가)

구 DEM 은 연속 껍질 두께나 XPS 감쇠비를 직접 만들지 못하므로, **이산 피복 대리 지표(부착·분산)**와 **충돌·응력 강도 분포(에너지·빈도)** 두 축을 결과 전에 고정해 함께 잰다.

### 4-1. 게스트 피복·분산 대리 지표 (이산 DEM 관측량)

| 지표 | 정의 (3D 덤프·접촉 덤프 기준) | 문헌·리포 대응 | 주의 · 한정어 |
|---|---|---|---|
| **순간 / 지속 AM 부착 SE 분율** ($f_{\text{SE}\to\text{AM}}^{\text{inst}}$, $f_{\text{SE}\to\text{AM}}^{\text{pers}}(\tau)$) | 전체 SE 중 AM(`AM_P`/`AM_S`)과 접촉 중인 분율; **지속 부착**은 연속 창 $\tau$ (예: 회전 주기 $T$ 의 0.5–1 배) 동안 **같은 AM 입자 ID** 와 접촉을 유지한 SE 분율 | 현 B2 반환 지표(`AM 순간 접촉 SE`, `mixer_b2_pair_return_20261124/README.md` `[리포]`)를 **지속 부착**으로 확장 | 순간 접촉은 단순 스침·충돌이 섞이므로, **지속 부착 $f^{\text{pers}}$ 를 주 피복 대리**로 두고 순간값과 병기한다 |
| **미부착 자유 SE 분율** ($1 - f_{\text{SE}\to\text{AM}}^{\text{pers}}$) 및 **SE–SE 군집 크기 분포** | AM 에 안 붙은 잔류 SE 몫 + 크기 2 이상 SE–SE 응집 군집에 속한 SE 분율 및 군집 크기 분포($N_{\text{cluster}}$) | `lee2026_mechanical` 잔류 SE 개수 · `pfeffer2001` 1단계 해쇄 · 현 B2 `SE 군집 몫` | 1차 파쇄가 아닌 **parcel 응집체 해쇄** 지표다 |
| **호스트당 게스트 배위수 분포** ($Z_{\text{SE/AM}}$: 평균 · 분산/평균 비 · 0-피복 호스트 몫) | `AM_P` 와 `AM_S` 를 분리해 각 호스트에 지속 부착된 SE 개수 분포를 측정. 분산/평균 비(Fano factor)를 포아송 무작위 기준(= 1)과 대조 | `pfeffer2001` (§8-2 정렬 혼합 3단계 재분배) · `wolf2026` (호스트 크기별 코팅 차: 3.8 vs 8.7 µm) | `AM_P` (큰 호스트) 와 `AM_S` (작은 호스트) 를 합산하면 크기 효과가 가려지므로 **반드시 분리 보고** |
| **이산 입체각/투영 피복률 대리** ($\theta_{\text{disc}}$) | 각 AM 구 표면에 지속 부착된 SE parcel 들이 가리는 투영 원판(겹침 보정) 면적 합 ÷ $4\pi R_{\text{AM}}^2$ | 실험 단면 둘레 피복률(`lee2024` 30.6–67.2 % `[인쇄]`) · 이미지 겹침 분율(`lee2026_lpscl` Table S2 `[인쇄]`) 의 기하 대응 | **연속 막 두께나 XPS 피복률과 같은 양이 아니다** — parcel 크기비(CGF)에 의존하므로 **팔 간 상대 비교 전용** |
| **벽 부착 · 챔버 공회전 분율** ($f_{\text{wall-stuck}}$, $E_r^{(k)}$) | 챔버 벽 접촉 SE/AM 분율 및 챔버 각속도 $\omega$ 를 뺀 회전 운동에너지(`chen2004` 식 8 `[인쇄]`)가 0 에 가까운(벽과 같이 도는) 입자 분율 | `hayakawa2022` 벽 SE 손실(14.5 → 27.1 %) · `kawaguchi2018` 순조성 손실(30 → 20.24 wt%) · `chen2004` 긁개 유무 대조 | rpm 상승의 역효과(원심 고착·벽 손실)와 긁개 작동 여부를 직접 진단 |

### 4-2. 충돌 · 응력 강도 분포 (평균만이 아니라 분포·꼬리 필수)

`chen2004` (`[인쇄 · 카드 해석]`)가 평균만 보고한 한계와 `frankenberg2024` · `kissel2026` (`[인쇄]`) 의 Kwade 응력 모델을 결합해 아래 네 묶음을 잰다:

1. **기능 영역 × 상 쌍별 입자당 충돌 빈도** (`chen2004` 식 12 · 표 2 `[인쇄]`):
   - 영역 4 등분: **안쪽 조각(수렴 틈) · 긁개 · 입력 · 자유 확산**.
   - **반드시 영역 내 입자 수로 정규화(입자당 빈도)** — 총 충돌 수는 인구가 많은 입력 영역이 앞서 순위가 뒤집힌다(`chen2004` §3-7 `[인쇄]`).
   - **충돌 셈 정의를 결과 전에 고정** (`dave2003` §3-6 경고: 미정의 시 접촉 시간과 모순) — 예: "새 접촉 쌍 개시(contact birth) 1 회 = 충돌 1 회" 로 세고, `SE–AM`, `SE–SE`, `AM–AM`, `입자–벽`, `입자–안쪽조각`, `입자–긁개` 로 분해한다.
2. **상대 충돌 속도 분포 ($v_n$, $v_t$) 및 상위 분위수(p50 · p90 · p99 · max)**:
   - 코팅(해쇄·소성 펴짐)은 평균이 아니라 **상위 꼬리 충돌**이 지배할 수 있다. 특히 `SE–AM` 및 `SE–벽/안쪽조각` 충돌의 $(v_n, v_t)$ 결합 분포가 **후속 MPM 단일 충돌의 직접 입력 경계 조건**이 된다.
   - `dave2003` (p.468–469 `[인쇄]`)의 세 경우 — (i) SE–AM 충돌, (ii) SE–벽 충돌, (iii) AM–벽/안쪽조각 사이에 SE 가 끼인 3체 압축 접촉 — 의 발생 빈도를 따로 센다.
3. **Kwade 비응력 에너지($SI$) · 응력 횟수($SN$) 분포 (`frankenberg2024` · `kissel2026` `[인쇄]`)**:
   - 연화 강성에서는 순간 최대 힘이 왜곡되므로(`chen2004` p.133 `[인쇄]`), 접촉 1 회의 **소산 에너지 / 입자 질량** ($SI$, J/kg) 분포와 단위 시간당 응력 횟수($SN$)를 잰다. (`frankenberg2024` 에서는 $SI \propto n^{2.17}$, `kissel2026` 에서는 $SI \propto n^{1.76}$ `[인쇄]`.)
4. **장치 수준 거시 점검량 & 접촉 유효성**:
   - **안쪽 조각 장시간 평균 힘** ($F_n$, $F_t$, `fix mesh/surface/stress` 합력) 과 **축 비동력/비에너지** ($P_m = \tau \omega / m$, `kissel2026` · `wolf2026` SME 대응) — 실험 장비의 토크·전력 기록과 대조할 다리다.
   - **접촉 겹침 분포** ($\delta / \min(r)$ 및 $\delta / \min(d)$ 의 p50 · p99 · max) 를 매 팔 무조건 기록한다.

> **이 지표들이 재지 않는 것 (과장 금지)**: 연속 SE 껍질 두께(nm), 껍질 치밀도·기공률, XPS `Li 1s : Ni 3p` 또는 `S : Ni` 면적비(`wolf2026`), 압분체 전자/이온 전도도(`R_inc` · $\sigma_{\text{ion}}$ · $\sigma_e$), LPSCl 열화(S 2p 상순도).

---

## 5. 첫 샌드박스 크기와 끝 기준 (Go / No-Go 및 전환 규칙)

> **원칙**: 모든 실행은 **별도 사전등록(덱·관측기·판정 기준 고정) + 1저자 GO 뒤**에만 수행한다. 아래는 그 등록 초안을 짜기 위한 2단계 샌드박스 크기와 끝(종료·전환) 기준 제안이다.

### 5-1. 2단계 샌드박스 크기 제안 (`ibb` NP 20 · 개발 자료)

| 단계 | 목적 | 기하 · 입자 규모 | 최소 팔 구성 (시드 1 · 개발 자료) | 예상 비용 `[추정]` (ibb NP 20) |
|---|---|---|---|---|
| **Stage S0** *(기하 · 역학 건전성 검증)* | MF 메시·긁개·안쪽 조각 힘 계측 및 `chen2004` 멱지수·긁개 효과 재현 | $D = 25\,\text{mm}$, $D_{\text{in}} = 10\,\text{mm}$, 틈 $1.6\,\text{mm}$, z-주기 $L_z = 1.6\,\text{mm}$ (`4 d`), **호스트 단일상**(`AM_P`, $d = 0.40\,\text{mm}$, `CGF = 44.4`, `gap/d = 4.0`), **$N = 1{,}500\text{–}3{,}000$**, 무점착, 물리 시간 $2.0\,\text{s}$ | **4 팔**: ① `2000 rpm` 긁개 있음, ② `2000 rpm` 긁개 없음, ③ `1000 rpm` 긁개 있음, ④ `3000 rpm` 긁개 있음 | 팔당 **0.25 – 0.56 h** (총 **< 3 h**; 단일 노드 소코어 NP 4–10 으로도 수 시간 이내) |
| **Stage S1** *(최소 3상 점착 MF 샌드박스 · S1-A 기준)* | 실제 3상 1:9 크기비와 D2 점착 대비($\gamma_{\text{AM}}/\gamma_{\text{SE}}$) 하에서 SE 해쇄·AM 지속 부착·충돌 속도 분포 신호 확인 | $D = 25\,\text{mm}$, $D_{\text{in}} = 10\,\text{mm}$, 틈 **$2.0\,\text{mm}$**, z-주기 $L_z = 1.44\,\text{mm}$ (`2 d_AM_P`), **3상 1:9 비율**(`CGF = 80`, `d_AM_P = 0.72 mm`, `d_SE = 0.08 mm`, `gap/d_AM_P = 2.78`), 채움 10 vol%, **$N \approx 89{,}300$** (`AM_P 128` · `AM_S 624` · `SE 88,506`), $\Delta t = 1.254 \times 10^{-7}\,\text{s}$, 물리 시간 **$0.5\,\text{s}$** (2000 rpm 16.7 회전 · 정상 확인 뒤 필요 시 1.0 s) | **핵심 4 팔 (2×2)**: 속도 (`1000` vs `2000 rpm`) × 점착비 (`U: 0.1` vs `C: 1.0`, `Bo_SE 21.244`) + **보조 1 팔**(`hooke/hysteresis + sjkr` 접촉 소성 비교 또는 `Bo_SE = 0` 무점착 기준) | 팔당 **14.2 – 15.6 h** (0.5 s 기준 · 48 h 상한의 약 1/3; 4 팔 총 ~60 h, `cpu-60` 3 슬롯 병렬 시 벽시계 **~1–1.5 일**) |

- **S0 → S1 관문**: S0 에서 4 팔이 모두 기술·역학 기준을 통과한 뒤에만 S1 덱을 등록·발사한다.
- **S1 초기 상태 주의** (`mixing_model_design_20260919.md` §20 교훈): 처음부터 완전 혼합된 상태로 삽입하면 "코팅·분산 진행"을 잴 수 없으므로, **AM 층과 SE 응집 덩어리(또는 분리된 두 영역)에서 출발**해 시간에 따른 해쇄·지속 부착 증가를 관찰한다.

### 5-2. 끝 기준 (완료 · 다음 단계 진입 · 중단/전환 규칙)

**① Stage S0 완료(S1 진입) 기준 — 전부 충족**
1. **기술 안정성**: 4 팔 모두 `rc = 0`, 입자 손실(lost atoms) = 0, 정상 상태 도달 시간 $\le 0.6\,\text{s}$ (운동 세기·안쪽 조각 힘 이동 평균 변동 $\le 5\,\%$).
2. **긁개 기전 재현** (`chen2004` · `dave2003` 방향 대조): `2000 rpm` 에서 긁개 있음이 없음 대비 **편차 운동 세기 및 법선 충돌 속도 1.5 배 이상 상승**(문헌 2.0–2.4 배), 벽 인접 고리의 상대 회전 KE(챔버 $\omega$ 제외)가 유의하게 증가(벽 강체 공회전 해소).
3. **안쪽 조각 힘 스케일링**: `1000–3000 rpm` 3점에서 장시간 평균 법선 힘의 로그–로그 기울기 $\alpha \in [1.6, 2.3]$ (문헌 계산 1.98 · 실험 그림 판독 1.70), $F_n / F_t > 2$.
4. **기능 영역 순위**: 입자당 충돌 빈도가 **안쪽 조각 또는 입력 영역 > 자유 확산 영역**.

**② Stage S1 완료(코팅 DEM → MPM 연계 진입) 기준**
1. **기술·수치 건전성**: 전 팔 `rc = 0`, 입자 손실 0, 벽시계 $\le 36\,\text{h}$ (48 h 상한 대비 25 % 여유), 겹침 분포가 사전등록 기준 안(p99 기준 지름 1 % 이내; 반지름 1 % 초과 빈도 명시 보고).
2. **코팅 관련 신호 분해**:
   - `1000 → 2000 rpm` 에서 `SE–AM` 상대 법선 충돌 속도 분포(p50·p90·p99) 및 `SI` 분포가 유의하게 우측 이동하고, SE–SE 군집 분율이 감소(또는 벽 공회전 분율과의 맞교환이 관측됨).
   - `U (0.1) → C (1.0)` 점착비 변화에서 **지속 부착 $f_{\text{SE}\to\text{AM}}^{\text{pers}}$** 또는 호스트당 배위수 분포의 방향 차가 정량적으로 분리됨(순간 접촉만이 아닌 지속 부착 기준).
3. **MPM 인계 출력 확보**: 안쪽 조각 수렴 틈·긁개 영역의 `SE–AM` 및 3체 압축 충돌에서 대표 $(v_n, v_t, SI)$ 분위수 묶음(예: p50 · p90 · p99)을 추출해 **단일 충돌 MPM 입력표**로 넘길 수 있는 상태.

**③ 중단 · 전환 기준 (No-Go / Pivot)**
- 아래 셋 중 하나라도 발생하면 **전장치 3상 코팅 DEM 확장을 중단**하고, `asylbekov2023` · `kissel2026` · `dave2003` 방식의 **호스트 전용 MF DEM (`SI` · `v_n` 분포 추출) → MPM 단일 충돌 / 0D PBE 분리 파이프라인**으로 전환한다:
  1. **비용 장벽**: 겹침 기준(p99 ≤ 1 %)과 틈 해상(`gap / d_AM_P ≥ 2.5`)을 동시에 맞추려 할 때 `ibb` NP 20 벽시계가 **48 h 를 초과**(MPI 부하 불균형 실측 포함).
  2. **틈 막힘(jamming) 아티팩트**: `gap / d_AM_P = 2.78` (S1-A) 에서 `AM_P` 가 수렴 틈을 주기적으로 막아 유동이 멎거나 비정상 힘 스파이크가 지배하고, 대안 S1-C(`gap/d = 4.0`, 1:5 크기비)로도 해소되지 않음.
  3. **지속 부착 신호 소실**: CGF 80–100 의 거친 SE parcel 특성상 `U ↔ C` 또는 `1000 ↔ 2000 rpm` 에서 지속 부착 $f^{\text{pers}}$ 변화가 잡음·벽 부착 교락 안에 묻혀 물리적 피복 대리로 성립하지 않음.

---

## 6. 참고 문헌 (litdb 정본 카드 대조표)

모든 서지·수치는 `origin/claude/friendly-meitner-lldvar` 가지의 `litdb/papers/<slug>.md` 정본 카드에서 직접 대조했다.

| 약칭 | 정본 카드 slug (`litdb/papers/`) | 저자 · 학술지 · 연도 | DOI | 이 메모에서의 용도 및 핵심 한정어 |
|---|---|---|---|---|
| `chen2004` | `chen2004_mechanofusion_dry_coating_dem_2d_host_scraper_inner_piece_collision_frequency` | W. Chen, R.N. Dave\*, R. Pfeffer, O. Walton, *Powder Technol.* 146 (2004) 121–136 | `10.1016/j.powtec.2004.07.014` | MF 25 mm 기하, 긁개 유무 대조(2×), $F_n \propto \omega^{1.98}$, 4영역 입자당 빈도, 2D/3D 점검, 연화 강성 정성 한계 (2D · 무점착 · host 만) |
| `dave2003` | `dave2003_dry_coating_dem_mechanofusion_hybridizer_maic_three_devices` | R. Dave\*, W. Chen, A. Mujumdar, W. Wang, R. Pfeffer, *Adv. Powder Technol.* 14(4) (2003) 449–470 | `10.1163/156855203769710672` *(PDF XMP)* | MF/Hybridizer/MAIC 3장치 비교, MF 공기 불필요 vs Hybridizer 공기 필수, 게스트 Δt ≤ 10⁻⁹ s 장벽, 단일 덩어리 충돌 3경우 (개관 · 점착·게스트 0) |
| `pfeffer2001` | `pfeffer2001_dry_particle_coating_engineered_particulates` | R. Pfeffer\*, R.N. Dave, D. Wei, M. Ramlakhan, *Powder Technol.* 117 (2001) 40–67 | `[미확인]` *(PII `S0032-5910(01)00314-X`)* | 건식 입자 코팅 장치 총설(MF 200–1600 rpm · Hybridizer 5000–16,000 rpm), 해쇄–부착–재분배 개념 (비배터리 재료) |
| `mellmann2001` | `mellmann2001_transverse_bed_motion_rotating_cylinders_slumping_rolling_cascading_froude` | J. Mellmann, *Powder Technol.* 118 (2001) 251–270 | `10.1016/S0032-5910(00)00402-2` | 회전 드럼 운동 꼴 경계식(현 B2 드럼 `Fr = 0.0827` = 폭포 체제 vs MF 원심 체제 구분; 무점착 단분산) |
| `kim2023` | `kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact` | J. Kim, M.J. Kim, …, U. Paik\*, D.S. Jung\*, T. Song\*, *Adv. Funct. Mater.* 33 (2023) 2211355 | `10.1002/adfm.202211355` | Hosokawa AMS-Mini MF 로 NCM811+LPSCl 코어–셸 실증(틈 3 mm, 긁개 ~0.4 mm, 2000–5000 rpm; 실험만) |
| `lee2026_lpscl` | `lee2026_lpscl_coating_thickness_ncm811` | J.W. Lee, D.W. Yoon, J. Kim, …, T. Song\*, Y.C. Kang\*, D.S. Jung\*, *Small Struct.* 7 (2026) e70530 | `10.1002/sstr.70530` | AMS-Mini MF 5000 rpm×5 h, LPSCl 껍질 233–628 nm, 2D EDS 겹침 정량·이온/전자 전도도 맞교환 (실험만) |
| `lee2026_mechanical` | `lee2026_mechanical_halogen_argyrodite_drycoating` | Y. Lee, **Y. An**, …, J.-W. Lee\*, *ACS Nano* (2026) ASAP | `10.1021/acsnano.6c09375` | **[our-lab 자기인용]** 건식 코팅 4단계(Fig. 1b), 할로젠 아지로다이트 AFM 영률(7.6–18.3 GPa)·나노압입 항복(78–120 MPa), RAM 공정 (DEM 없음) |
| `kawaguchi2017` | `kawaguchi2017_dry_coating_parametric_na2so4_model_se` | T. Kawaguchi, H. Nakamura\*, S. Watano, *Powder Technol.* 305 (2017) 241–249 | `10.1016/j.powtec.2016.09.085` | Hybridizer NHS-0 공정 창(선속도·시간·조성), 모델 SE `Na₂SO₄` (황화물 아님 · DEM 없음) |
| `kawaguchi2018` | `kawaguchi2018_dry_coating_model_se_particle_powtec` | T. Kawaguchi, H. Nakamura\*, S. Watano, *Powder Technol.* 323 (2018) 581–587 *(온라인 2016)* | `10.1016/j.powtec.2016.03.055` | Hybridizer 16,000 rpm(끝 98.9 m/s) 벽 손실(30→20.24 wt%), 연성 게스트 소성·합체 기전 제안 (모델 SE · DEM 없음) |
| `nakamura2020` | `nakamura2020_dry_coating_ncm_li3ps4_core_shell` | H. Nakamura\* 외 7인, *J. Power Sources* 448 (2020) 227579 | `10.1016/j.jpowsour.2019.227579` | 실제 유리질 `Li₃PS₄` 건식 충격 코팅 + 3D 복셀 수송 (공정 DEM 없음) |
| `hayakawa2022` | `hayakawa2022_high_shear_mixer_dry_mixing_ncm523_lpscl_composite_cathode` | E. Hayakawa, H. Nakamura\*, S. Ohsaki, S. Watano, *Adv. Powder Technol.* 33 (2022) 103705 | `10.1016/j.apt.2022.103705` | 수평 고전단 칼날 믹서(5,000–25,000 rpm) 에서 rpm 상승에 따른 벽 SE 손실(14.5→27.1 %) 실측 (DEM 없음) |
| `kissel2026` | `kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable` | M. Kissel, F. Frankenberg, …, A. Kwade\*, J. Janek\*, *Nat. Commun.* 17, 3215 (2026) | `10.1038/s41467-026-71305-2` | Picoline Nobilta 10 vol% 채움 + Rocky 거친 입자 DEM(Thornton–Ning · 무점착 · 단일종), Kwade `SI ∝ n^1.76` (할라이드 `Li₃InCl₆`) |
| `frankenberg2024` | `frankenberg2024_dem_high_intensity_mixer_assb` | F. Frankenberg, M. Kissel, …, A. Kwade, *Powder Technol.* 435 (2024) 119403 | `10.1016/j.powtec.2024.119403` | 고강도 믹서 Rocky DEM(JKR + force-scaling), `SI ∝ n^2.17`, Kwade 응력 모델 (LFP+CB+할라이드) |
| `wolf2026` | `wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode` | M. Wolf\*, …, S. Lux\*, *Adv. Sci.* (2026) e78248 | `10.1002/advs.78248` | 트윈스크류 압출(300 kJ/kg, 100 °C) vs 배치 MF(7,140 kJ/kg) 비교, 호스트 입경 효과(3.8 vs 8.7 µm), 100 °C LPSCl 표면 열화 (DEM 없음) |
| `lee2024` | `lee2024_shear_force_dry_process_cathode_coverage` | D. Lee, Y. Shim, …, S.H. Choi\*, K. Kim\*, D.-J. Yoo\*, *Nat. Commun.* 15, 4763 (2024) | `10.1038/s41467-024-49183-3` | 단면 SEM 2D 둘레 피복률 정의(30.6–67.2 %), 전단에 의한 SE 변형 (손반죽·밀대, DEM 없음) |
| `lischka2025` | `lischka2025_dem_eirich_intensive_mixer_dry_mixing` | C. Lischka\*, H. Nirschl, *Particuology* 104 (2025) 52–67 | `10.1016/j.partic.2025.06.002` | Eirich EDEM(CGF 200, JKR, cohesion number), CGF γ → 실물 γ 역전이 불가 경고 (SE 없음 · 단일종) |
| `hare2026` | `hare2026_dem_pept_dry_mixing_nmc622_eirich` | S.D. Hare\*, …, H. Nirschl, E. Kendrick, *Powder Technol.* 469 (2026) 121804 | `10.1016/j.powtec.2025.121804` | Eirich PEPT 유동 검증 + 단방향 CFD 항력, 논문 간 γ 절대값 대신 무차원 Bond 수 전이 증명 (NMC622 단상) |
| `asylbekov2023` | `asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing` | E. Asylbekov\*, H. Nirschl, J. Mayer, A. Kwade, *Energy Technol.* 11 (2023) 2200867 | `10.1002/ente.202200867` | 미세입자 파쇄를 DEM 에서 빼고 DEM 응력 통계 → 0D PBE 로 단방향 연계한 선례 (CB+NCM622, SE 없음) |
| `xu2023` | `xu2023_dem_bonded_particle_fracture_calendering` | J. Xu, …, A.A. Franco\*, *Batteries & Supercaps* 6 (2023) e202300371 | `10.1002/batt.202300371` | 수정 LIGGGHTS BPM 파쇄 모델(하위 구 1.59 µm, Δt 0.01 ns, 28코어 2–9일) — 1차 입자 파쇄의 비용 근거 (액체 LIB 압연) |
| `tovar2026` | `tovar2026_cold_spray_cathode_composite_dem_plastic_elastic_bond` | A.G. Tovar\*, …, J.S. Curtis, *Surf. Coat. Technol.* 541 (2026) 134102 | `10.1016/j.surfcoat.2026.134102` | 탄소성 결합구 단일 충돌 DEM(15,215 구, Δt 2.2 ps, 210 ns) — 결합 파쇄가 장치 규모에 부적합한 근거 (냉간분무) |
| `luding2008` | `luding2008_cohesive_frictional_contact_models` | S. Luding, *Granular Matter* 10(4) (2008) 235–246 | `10.1007/s10035-008-0099-x` | 우리 `hooke/hysteresis` 법선 모델 원전(항복압 캡 부재·대변형 한계 명시) |
| `thorntonning1998` | `thorntonning1998_adhesive_elastoplastic_contact` | C. Thornton, Z. Ning, *Powder Technol.* 99(2) (1998) 154–162 | `10.1016/S0032-5910(98)00099-0` | 항복압 $p_y$ 캡 + JKR 점착 탄소성 접촉 이론(`kissel2026` Rocky 기반; 현 LIGGGHTS 덱 미탑재) |
| `thakur2014` | `thakur2014_eepa_adhesive_elastoplastic_dem` | S.C. Thakur, J.P. Morrissey, J. Sun, J.F. Chen, J.Y. Ooi, *Granular Matter* 16(3) (2014) 383–400 | `10.1007/s10035-014-0506-4` | EEPA 점착 탄소성 접촉 법칙 원전(우리 `ibb` 바이너리 탑재 여부 `[미확인]`) |
