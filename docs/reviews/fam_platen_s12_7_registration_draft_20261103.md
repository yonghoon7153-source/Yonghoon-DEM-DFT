# FAM §12-7 등록 초안 — gabia (RTX A6000) · 확인 런 1 + corner 3

> **초안 2026-11-03 · 결과 0 건** — §12-7 의 런 · 건식 실행 모두 **0 개**.  **1저자 비준 전** — 비준 전에는 gabia 에서 FAM 런을 띄우지 않는다 (사용자 규칙: 보고 → 설명 → 비준 → 실행).
>
> ⚠ **분류 = "선행 결과 (§12-5-9 · §12-6-2) 를 본 뒤의 후속 등록"** — 맹검 사전등록이 **아니다**.  이 등록이 내는 어떤 값도 원고 · 발표 · 보고에서 *"사전등록 예측 적중"* 으로 쓰지 않는다.  결과 문장마다 *"선행 결과에 근거한 후속 시험 · 열람 이력 = §12-7 §0"* 을 붙인다 (prereg §12-3 FAMV2-07 622–623 행 · §12-6 *"예측 가능성 고지"* 868 행과 같은 규칙).
>
> 정본 = `docs/reviews/fam_platen_prereg_20260812.md` (아래 "prereg" · 행 번호는 11-03 판).  비준되면 이 내용을 prereg §12-7 로 옮기고 그 커밋 시각을 봉인 시각으로 한다 (Q13 · prereg 626–627 행 *"같은 문서의 버전 고정 커밋으로 충분하다"*).  그때까지 이 파일은 초안이다.

**근거 — 시점**
- 1저자 11-03 (이 초안을 맡긴 지시에 실린 문구): *"FAM §12-7 을 Rint R 전에 gabia 빈 기간에 돌린다 — 등록 먼저"*.  같은 날 진행 기록 `docs/session_20260923_progress.md` 1267 행 *"FAM §12-7 (A6000 · 확인 1 + corner 3) = 결과 본 뒤의 등록이 먼저 (⬜ 1저자)"* · 1268 행 *"gabia 는 11-22 부터 R 에 비워 둔다 (FAM §12-7 은 그 전 빈 기간에만 · Q1)"*.
- 그 전 이력: 10-20 Q15 *"gabia = Rint · 214 뒤"* (진행 기록 1145 행) → 10-23 인계 Q2 권고 *"Rint R 이 끝난 뒤"* (`docs/handoff_codex_nonrint_20261023.md` 198 행) → **11-03 = Rint R 전 빈 기간** (위).  10-23 Codex 쪽지의 *"기계 배정·실행을 승인한 것으로 취급하지 않는다"* (`docs/collab/codex_to_claude/20261023-1155_nonrint-environment.md` 36 행) 는 그대로 지킨다 — 기계 배정은 이 등록의 비준으로, 발사는 1저자가 정한다.

**이번에 정하는 것 / 정하지 않는 것**

| 정하는 것 | 정하지 않는 것 |
|---|---|
| corner 3 팔의 argv (봉인 줄 + 기계 자리) · 자격 · 분류 · 재시도 · 기한 규칙 · 판정선 (등록된 것 재사용) · gabia 점검 절차 · 일정 (추정) | **확인 런 1 이 무엇인가** (리포 글에 정의 없음 → Q1) · 숫자 결과 · 발사 시각 (1저자) · real_14 네 칸 (미배정 그대로) · Rint R 일정 · 창 · f 값 · 기준 두께 (§12-5-7 봉인 그대로 — 손대지 않는다) |

⛔ **DO-NOT 경계** (`CLAUDE.md` 61–84 행): 이 등록은 MPM 을 "진짜 300 MPa 에 닿게" 하려는 시도가 아니다.  f 팔은 ② (AM 하중분담) 의 시험이고, 아래 `--frames` 는 *"끝까지 돌 수 있는가"* 의 조건 (루프 길이 · 동역학 불변 · prereg 869–870 행) 이지 과압축의 처방이 아니다.  `final_stress_GPa < target` 을 미달로 읽지 않는다 — f 팔의 서보 설정점은 `target·(1 − f)` 이고 `settled_over_target ≈ 1 − f` 가 정상이다 (prereg 858 행).

---

## 0. 열람 이력 · 예측 가능성 고지 (결과 전에 적는다)

### 0-1. 이미 본 것 (이 초안 시점)

| 무엇 | 기록된 값 (그대로) | 출처 |
|---|---|---|
| real_14 `f = 0` (kgy · §12-6) | 적격 · 두께 25.842 µm · I_0 = 0.147 → 거짓 · `porosity_at_target_pct` 2.585 (MPM 관례) | prereg 909 · 912–913 행 |
| real_14 f_(b) 0.8085 (kgy · ⑤ 시도 2) | 적격 · 두께 29.491 µm · I_b 참 · 서보 수렴 frame 266/400 · 시도 1 (정지) 끝 네 줄도 열람 (`SELF-80`) | prereg 851 · 856 행 |
| real_14 f_(a) 0.6703 (kgy · ④ · §12-6) | 두 번 다 `EXECUTION_FAILED` — 400 · 3000 프레임 안 서보 미수렴 (끝 wallP 0.0911 · 0.0917 GPa ↔ SE 설정점 0.0989) · ④ 끝 두 줄과 §12-6 실패 팔 `FINAL` 줄 열람 (미수렴 값 · 어디에도 안 씀) | prereg 816 · 836 · 910 · 927–928 행 |
| real_14 §9 R2.5-v2 (`f = 0` 팔) | v2-a · b · c 빗나감 (pinned False · 상단 흡수 0.770 · f_am_cut 0.9986) · 계측 축퇴 쪽 · v2-e 미채점 | prereg 916–925 행 |
| `am_load_split` 부수 열람 | 09-23 CPU 스모크 f_am_cut ≈ 0.9994 · ⑤ JSON f_am_cut 0.9984 | prereg 456 · 876 행 |
| corner 06-26 — kserver (= gabia A6000) · `hold` · n_grid 384 · **폐기된 f 0.86** (폐기된 v0 von-Mises 값) | f = 0 (조건부 off) porosity 15.90 % · f 0.86 → porosity 25.25 % · 두께 19.3 µm (같은 줄의 SE_target 0.042 GPa = 0.3·(1 − 0.86) → f 0.86 런 값으로 읽힌다) · DEM porosity 28.34 % | `docs/mpm_wallP_conditional_troubleshooting.md` 104–112 · 123–131 · 457 행 · prereg 613–614 · 624–625 행 (폐기값 · 근거로 안 씀 · 열람 이력 병기) |
| corner §12-5 (kgy · 시도 1 · 2) | 필드 할당 단계 메모리 부족 (각 19–35 초) — 프레임 0 · 물리 값 없음 | prereg 818 · 852–854 행 |

### 0-2. 예측 가능성 고지

1. **corner `f = 0`** — real_14 `f = 0` 이 과압축했고 (−14.7 %), 06-26 corner 의 f = 0 도 DEM 보다 낮은 porosity 였다 (15.90 ↔ 28.34 %) ⇒ corner I_0 거짓 쪽이 미리 보인다.
2. **corner f_(a) · f_(b)** — 06-26 f 0.86 런의 두께 19.3 µm 는 corner 창 [18.571135, 19.719865] µm 안이다 (\|19.3 / 19.1455 − 1\| = 0.0081).  0.86 은 corner f_(a) 0.8240 과 f_(b) 0.9007 사이다.  프로토콜 (hold ↔ 이 등록 servo) · 격자 (384 ↔ 768) · 코드 세대 · f 출처 (폐기된 v0) 가 다르지만 **I_a · I_b 결과도 맹검 예측이 아니다.**
3. **미수렴** — real_14 f_(a) 는 3000 프레임 안에 수렴하지 않았다 (마지막 창 스프레드 0 % · wallP 가 설정점 아래) — corner f 팔에서도 같은 종류의 미수렴이 날 수 있음을 안다.

⇒ 네 칸 · 순서 결과를 *"사전등록 적중"* 으로 쓰지 않는다 · 결과 문장마다 이 고지를 붙인다 (prereg 868 행과 같은 규칙).

---

## 1. 런 목록

### 1-1. corner 3 — 정의는 봉인 그대로 (prereg §12-5-7 · §12-5-8)

| 팔 | `--am-load-frac` | 출력 태그 | 근거 |
|---|---|---|---|
| corner `f = 0` | 0 | 0 | prereg 793 행 |
| corner f_(a) | 0.8240 | a | prereg 777 행 (AM–AM 119 · AM–SE 28,266 · SE–SE 154,610 접촉) |
| corner f_(b) — **primary** | 0.9007 | b | prereg 777 행 · primary = b (768 행 · §12-2 532 행) |

- 고정 (prereg 768–778 행 · 손대지 않는다): 케이스 `input_1mAh_100_15` (1저자 진술) · 원자료 지문 = `docs/data/case15_corner_20261001/README.md` 의 sha256 · step 1,710,000 · t_DEM **19.1455 µm** (판 메시 평평한 면 z − 바닥 `zplane 0.0`) · 창 **[18.571135, 19.719865] µm** · 추출기 `scripts/dem_am_load_fraction.py` 의 `am_load_fraction_liggghts` (blob e4c956ce5638) · primary b · 허용 오차 상대 ±3 % (§12-2 와 같은 지위 — 결과 열람 전 승인한 실용 허용 오차 · 신뢰구간 아님 · prereg 565–569 행).
- 기록 (prereg 803–804 행 그대로): 조성 표기 *"87:13"* ↔ 덱 *"85:15"* 불일치 — 판정 입력 아님 · ⬜ 1저자 확인 그대로.

### 1-2. 확인 런 1 — ⚠ 리포 글에 정의가 없다 → Q1

- 처음 적힌 곳: 10-02 밤 `CLAUDE.md` FAM 행 (커밋 `510c25371` · 2026-10-02 13:38 UTC = 22:38 KST) *"⬜ §12-7 gabia (A6000 48 GB · 확인 런 1 + corner 3) = 딴 시뮬 끝난 뒤 · kgy 다음"* — **§12-6 발사 (10-03 00:39 KST) 전**이다.
- 다시 적힌 곳: prereg 929 행 (§12-6-2 끝 · 커밋 `eb52d09d3`) *"다음: §12-7 gabia (A6000 48 GB · 확인 런 1 + corner 3) = 딴 시뮬 끝난 뒤 — 이 결과 … 를 본 뒤의 등록이 된다"* · 같은 표현 = `CLAUDE.md` 37 행 · `docs/handoff_codex_nonrint_20261023.md` 146 행 · `docs/worklog/weekly_20261004.md` 386 행 · 진행 기록 1267 행 (*"확인 1"*).
- 어느 곳도 **무엇을** 돌리는지 적지 않았다 ⇒ 이 초안은 고르지 않는다.  글에서 나오는 후보만:

| 후보 | 무엇 | argv 출처 | kgy 기록 | 맞는 점 | 걸리는 점 |
|---|---|---|---|---|---|
| (가) | real_14 f_(b) 0.8085 를 gabia 에서 — ⑤ 와 같은 argv | prereg 721–722 행 (`--frames 400`) | 수렴 frame 266 · 30 분 · 29.491 µm | 기계 확인 — prereg 875 행 *"GPU 재실행의 비트 동일성은 주장하지 않는다"* · 666–667 행 같은 기계 규칙 · 가장 싸다 | kgy 의 I_b · 판정은 바뀌지 않는다 (판정에 안 쓰는 확인) |
| (나) | real_14 `f = 0` 을 gabia 에서 — §12-6 argv | prereg 881–882 행 (`--frames 3000` · `--allow-unconverged-servo`) | 수렴 ≈ 810 프레임 · 2 h 03 m · 25.842 µm | 기계 확인 + corner `f = 0` 과 같은 관문 경로 | (가) 의 약 4 배 시간 |
| (다) | real_14 f_(a) 0.6703 다시 | — | 400 · 3000 둘 다 미수렴 | real_14 네 칸을 채울 유일한 팔 | prereg 872 행 *"3000 안에 미수렴이면 EXECUTION_FAILED 로 적고 끝낸다 (3 차 등록 없음)"* 과 충돌 · "확인 런 1" 은 그 결과 **전**에 적혔다 · 기계가 섞이면 666–667 행대로 순서 판정 보류 |
| (라) | R2 384 다시 | — | 프레임 예산 5441 안 미수렴 (prereg 813 행) | — | 실패 원인이 메모리가 아니다 → A6000 이 바꾸는 것 없음 · argv 변경 = 별도 등록 |
| (마) | 확인 런 없음 | — | — | 일정 여유 | kgy ↔ gabia 차이를 재지 않는다 |

### 1-3. 이 등록 밖

real_14 f_(a) (prereg 872 행 *"3 차 등록 없음"* — Q1 에서 (다) 를 고르지 않는 한) · R2 384 · 256 · real_14 네 칸 · 순서 (미배정 그대로 · prereg 914–915 행) · prereg §5 킷 확장.

---

## 2. 기계 · 코드 · argv · 예산 · 자격 · 재시도

### 2-1. 기계 = gabia

- Ubuntu 24.04 · RTX A6000 **49,140 MiB** · 드라이버 595.58.03 (CUDA 13.2) · RAM 62 GB · 20 코어 · 디스크 207 GB 남음 · 리포 있음 (진행 기록 1267 행 · 11-03).  같은 기계에서 06-26 ~ 28 에 MPM 이 돈 기록이 있다 ("kserver/Gabia A6000" · `docs/mpm_wallP_conditional_troubleshooting.md` 168 · 457 행).
- §12-7 의 모든 팔 = gabia **한 GPU · 같은 봉인 사본 · 같은 환경 · 한 번에 한 팔** (두 팔 동시는 메모리상 안 된다 — §3-1).
- 10-02 기록: 그때 gabia GPU 는 남의 작업이 43.2 GB 를 쓰고 있었다 (진행 기록 837 행) ⇒ 각 팔 직전 여유 메모리를 적는다 (§5-3).

### 2-2. 코드 · 입력 = 봉인 그대로

| 항목 | 값 | 이 초안이 11-03 에 다시 셈 |
|---|---|---|
| 코드 | 봉인 커밋 `7f44d6534` 의 트리 (prereg 715–739 · 867 행) | `scripts/mpm3d_compaction.py` blob md5 = c31f0512021d416702e162709c6f4400 — prereg 750 행의 c31f0512 와 같다 |
| ⚠ 가지 끝 판 | 같은 파일이 10-14 커밋 `cb5a6a445` (밀도 세대) 에서 바뀜 → 가지 끝 md5 = cae40a894339d3b0db32ac3dfc6c1846 | **쓰지 않는다** — gabia 도 봉인 사본에서 돈다 (kgy `~/dem-fam` 은 git 저장소가 아니라 `SEAL_COMMIT` 파일로 봉인한 사본 · prereg 829–830 행) |
| real_14 스캐폴드 sha256 | `docs/data/real14_am_scaffold.csv` (457 행) `281ad86e0465a13b6ed96dbcf30c76acf4f372ff9d7c4a7e36fe55ecd44413fd` · `docs/data/real14_se_scaffold.csv` (32,832 행) `159f4ac05973197e71019e9f541b6cb1517ef7a75c0790f935d1ccfb4c526640` | 봉인 트리 안 blob = 지금 파일 |
| corner 스캐폴드 sha256 | `docs/data/case15_corner_20261001/case15_am_scaffold.csv` (104 행) `275c56e12fe11294fe6bf2cb304ce4187ee3fb3cb2f7ccdd8a5fc92d770383ba` · `docs/data/case15_corner_20261001/case15_se_scaffold.csv` (65,866 행) `929a495e4599dc55f09b2348b5b8b7fe41ecda131bfdbfae08ca0597d1ae0d1f` — 리포 LF 바이트 · README 앞 16 자리와 같음 | 커밋 `cf5103c94` 의 blob · **봉인 트리 `7f44d6534` 에는 없다** (2 h 39 m 뒤 커밋) → 사본에 따로 넣고 sha256 으로 확인 |

### 2-3. corner argv — 봉인 줄 + 기계 자리만 (prereg 788–794 행 글자 그대로)

```bash
# 바꾼 것 = 기계 자리 셋뿐: $PY (gabia 인터프리터 ⬜) · 작업 자리 (gabia 봉인 사본 뿌리 ⬜) · <OUT> (gabia 출력 자리 ⬜)
#           + 출력 이름 접두 s127 (kgy 기록과 섞이지 않게)
COMMON="--arch cuda --gpu-mem 28 --protocol servo --floor-porosity 0 --compact-to 0 --stop-freeze-probe --platen-mach 0.01 --e-se 1.53 --nu-se 0.49 --sigma-y 0.30 --target-gpa 0.30 --readout wallP --frames 400 --sub 40 --seed 3"
$PY -u scripts/mpm3d_compaction.py --am-scaffold docs/data/case15_corner_20261001/case15_am_scaffold.csv \
  --se-dump docs/data/case15_corner_20261001/case15_se_scaffold.csv --lateral-box 0.1 --n-grid 768 $COMMON \
  --am-load-frac <f> --save-metrics <OUT>/fam_s127_corner_f<태그>.json > <OUT>/fam_s127_corner_f<태그>.log 2>&1
#   f = 0 (태그 0) · 0.8240 (태그 a) · 0.9007 (태그 b)
```

⚠ 이 줄 그대로면 — (i) corner `f = 0` 은 봉인 코드의 런 전 관문 (2951–2962 행: `--stop-freeze-probe` + scaffold + `--am-load-frac ≤ 0` + `--floor-porosity ≤ 0` + `--am-jam` 없음 + `--allow-unconverged-servo` 없음 → `sys.exit`) 에서 **확정 거부**다 (`SELF-78` 이 corner ⑥ 을 이미 적었다 · prereg 824 행) (ii) 예산 400 은 real_14 에서 모자랐던 값이다 (`SELF-79`).  ⇒ §2-4.

### 2-4. 후속 등록이 정할 넷 — prereg 861 행 *"후속 등록 (격자 · 메모리 상한 · 프레임 예산 · `f = 0` 관문) = 1저자"*

| 항목 | §12-5-8 봉인 | 권고 (⬜ 비준) | 근거 |
|---|---|---|---|
| 격자 | `--lateral-box 0.1 --n-grid 768` | **그대로** | 격자 간격 = real_14 팔과 같음 (0.1415 µm · SE 반지름 ≈ 3.5 칸 · prereg 796–798 행) · 384 로 낮추지 않는다 (800 행 *"384 승격 없음"*) · gabia 에서 산술상 들어간다 (§3-1) |
| 메모리 상한 | `--gpu-mem 28` | **그대로** (Q4) | 코드가 min(총 85 %, 여유 90 %) 로 깎는다 (봉인 코드 1742–1763 행) · gabia 총 49,140 MiB → 40.8 · 여유 ≥ 31,858 MiB 면 28 그대로 · 어림 21.06 GiB (§3-1) |
| 프레임 예산 | `--frames 400` | **`--frames 3000`** (Q2) | §12-6 과 같은 근거 — `args.frames` = 루프 길이 · 경고 · 기록뿐 → 동역학 불변 · 수렴 런은 일찍 끝난다 (prereg 869–872 행) · 400 은 real_14 에서 모자랐다 (`SELF-79`) · 3000 안 미수렴 = `EXECUTION_FAILED` · 이 등록 안 추가 시도 없음 |
| `f = 0` 관문 | 없음 | **`f = 0` 팔에만 `--allow-unconverged-servo`** (Q3) | §12-6 과 같음 (R1 레시피 · 코드에서 쓰이는 곳 = 런 전 관문 · 미수렴 내보내기 두 곳뿐 · prereg 873–874 행) · 없으면 확정 거부 |

권고안 argv (⬜ 비준 전 · Q2 – Q5 를 권고대로 받았을 때의 발사 후보 · 순서 = Q5 권고):

```bash
COMMON7="--arch cuda --gpu-mem 28 --protocol servo --floor-porosity 0 --compact-to 0 --stop-freeze-probe --platen-mach 0.01 --e-se 1.53 --nu-se 0.49 --sigma-y 0.30 --target-gpa 0.30 --readout wallP --frames 3000 --sub 40 --seed 3"
#   = prereg §12-6 의 COMMON6 (880 행) 과 글자까지 같다 (= §12-5-8 의 $COMMON 에서 --frames 만 400 → 3000)
$PY -u scripts/mpm3d_compaction.py --am-scaffold docs/data/case15_corner_20261001/case15_am_scaffold.csv \
  --se-dump docs/data/case15_corner_20261001/case15_se_scaffold.csv --lateral-box 0.1 --n-grid 768 $COMMON7 \
  --am-load-frac 0.9007 --save-metrics <OUT>/fam_s127_corner_fb.json > <OUT>/fam_s127_corner_fb.log 2>&1
$PY -u scripts/mpm3d_compaction.py --am-scaffold docs/data/case15_corner_20261001/case15_am_scaffold.csv \
  --se-dump docs/data/case15_corner_20261001/case15_se_scaffold.csv --lateral-box 0.1 --n-grid 768 $COMMON7 \
  --am-load-frac 0.8240 --save-metrics <OUT>/fam_s127_corner_fa.json > <OUT>/fam_s127_corner_fa.log 2>&1
$PY -u scripts/mpm3d_compaction.py --am-scaffold docs/data/case15_corner_20261001/case15_am_scaffold.csv \
  --se-dump docs/data/case15_corner_20261001/case15_se_scaffold.csv --lateral-box 0.1 --n-grid 768 $COMMON7 \
  --am-load-frac 0 --allow-unconverged-servo --save-metrics <OUT>/fam_s127_corner_f0.json > <OUT>/fam_s127_corner_f0.log 2>&1
```

세 팔은 `--am-load-frac` 값 · 출력 이름 · (`f = 0` 의) 관문 인자만 다르다.

### 2-5. 확인 런 argv — Q1 에 따라 (⬜)

```bash
# (가) prereg 721–722 행 (§12-5-5 f 팔 줄 · ⑤ 가 돈 줄) 글자 그대로 + 기계 자리 셋 · $COMMON = --frames 400 판 (위 2-3)
$PY -u scripts/mpm3d_compaction.py --am-scaffold docs/data/real14_am_scaffold.csv --se-dump docs/data/real14_se_scaffold.csv \
  --n-grid 384 $COMMON --am-load-frac 0.8085 --save-metrics <OUT>/fam_s127_confirm_fb.json > <OUT>/fam_s127_confirm_fb.log 2>&1

# (나) prereg 881–882 행 (§12-6 f = 0 줄) 글자 그대로 + 기계 자리 셋 · $COMMON6 = 위 COMMON7
$PY -u scripts/mpm3d_compaction.py --am-scaffold docs/data/real14_am_scaffold.csv --se-dump docs/data/real14_se_scaffold.csv \
  --n-grid 384 $COMMON6 --am-load-frac 0 --allow-unconverged-servo --save-metrics <OUT>/fam_s127_confirm_f0.json > <OUT>/fam_s127_confirm_f0.log 2>&1
```

- 예산: (가) = 400 (⑤ argv 그대로 · kgy 는 frame 266 에 수렴) · (나) = 3000 (§12-6 그대로).

### 2-6. 순서

- 한 GPU · 한 번에 한 팔 (prereg 799 행 *"한 GPU 에서 차례로"*).
- 확인 런 (Q1 이 (가) · (나) 일 때) = **맨 앞** — 새 기계 환경 점검을 겸한다 (기술 관문 · §4-2).
- corner: 봉인 순서 `f = 0 → f_(a) → f_(b)` (prereg 799 행) ↔ 권고 `f_(b) → f_(a) → f = 0` (Q5 — 기한이 고정이라 primary 를 먼저 지킨다 · 팔은 서로 독립 프로세스라 순서가 값을 바꾸지 않는다).

### 2-7. 자격 · 분류 — 판정 전에 prereg 12-4 표 (637–645 행) 로 먼저

1. **적격** = 로그에 `✓ converged: σzz equilibrated at target` **그리고** JSON `porosity_at_target_pct` 가 None 아님 (prereg 874 행) **그리고** §12-5-1 자격 (`servo_status == converged` ∧ `stop_mode ∉ {hard_floor, am_jam}` ∧ `am_load_applied_to == descend+servo_setpoint` · 657–659 행).
2. **재하율** — 실행 당시 `V` · `cP_SE` · `sub` · 실제 `dt` 와 그 비를 로그 · JSON (`platen_mach_V_over_cP` · `dt_effective` · `dt_cfl_limited`) 에서 적는다 · `V/cP_SE ≤ 0.01` (부동소수 반올림 수준만 허용) · 위반 = `RATE_INELIGIBLE` → `NOT_EVALUABLE` (prereg 486–497 · 505 행).  n_grid 768 에서는 CFL 상한이 dt 를 문다 (§3-2 산술) — 식에서 V/cP_SE 는 요청 Mach 로 보존된다 (prereg 476–483 행) · 로그로 확인.
3. `--allow-unconverged-servo` 로 내보내진 **미수렴 JSON** = `EXECUTION_FAILED` (내보냄 ≠ 결과 · prereg 874 행).
4. **프레임 예산 안 미수렴** = `EXECUTION_FAILED` · 재시도 없음 (같은 argv = 같은 결과 · prereg 825 행) · 이 등록 안 추가 시도 · 추가 등록 없음 (prereg 872 행 꼴 · Q2).
5. **런 전 관문 거부** = `EXECUTION_FAILED` · 재시도 없음 (prereg 825 행).
6. **메모리 부족 · 노드 장애 · CUDA 오류** = `EXECUTION_FAILED` → §2-8 재시도.
7. 러너 결함으로 **python 이 시작되지 않은 것** = 런 시도 아님 · 기록만 (prereg 829–830 · 903 행 꼴).
8. **기한 정지** = *"미완주 — 실패 아님 · 판정 없음"* (prereg 817 행 ⑤ 정지와 같은 분류 · Q6).
9. corner 팔 하나라도 `EXECUTION_FAILED` · 미완주면 corner 네 칸 · 순서 **미배정** — 남는 값은 값으로만 (prereg 832 · 914–915 행 꼴).

### 2-8. 재시도 (prereg 647–649 · 730 행 그대로)

- `EXECUTION_FAILED` 중 **메모리 부족 · 노드 장애 (계산 실패)** 에 한해 **같은 argv · 같은 기계로 1 회** · 모든 시도를 보고 · 적중한 시도만 고르지 않는다 · 물리 결과가 나온 팔은 재시도 없음.
- kgy 의 corner 두 시도 (§12-5-9 · 메모리 부족) 는 그 봉인에서 닫힌 기록이다 (prereg 861 행) — 이 등록의 시도 수에 넣지 않는다 (Q11) · 결과 문장에 함께 적는다.
- 건식에서 필드 할당이 실패하면 발사 전이므로 시도로 세지 않고 발사하지 않는다 → 1저자 (Q4).

### 2-9. 기한

- **기한** = 11-21 (토) ⬜ 시각 (권고 12:00 KST) 또는 1저자가 Rint R 을 위해 gabia 를 비우라고 한 시각 중 **이른 쪽** (Q6).
- 그 시각에 도는 팔 = 정지 (`setsid` 로 띄운 런은 PGID ≠ `$!` → `pkill -TERM -f <OUT 이름>` · `config/env_db.json` kgy quirks) · 시작 전 팔 = 띄우지 않음 · 분류 = 2-7 의 8.
- 이어 돌리기 = Rint R 뒤 1저자의 새 결정 · 새 등록으로만.

---

## 3. 메모리 · 시간 어림 (리포 기록 숫자만 · 산술 · **추정**)

### 3-1. 메모리 — corner (n_grid 768)

prereg 820–821 행의 산술 (코드의 필드 선언 · 추정) 을 단위까지 다시 셈:

```
격자  768³ = 452,984,832 칸 × 24 B (grid_v 12 · grid_m 4 · am_mask 4 · am_near 4) = 10.87 × 10⁹ B = 10.12 GiB
점    ≤ 65,866 × 1,437 = 94,649,442 (SE 반지름 3.5 칸 구의 dx/2 점 · 겹침 빼기 전 = 상한) × 124 B = 11.74 × 10⁹ B = 10.93 GiB
합    22.61 × 10⁹ B = 21.06 GiB            ← prereg 의 "≈ 22 GB" 는 10⁹ B 단위
```

- 코드 상한 (봉인 코드 1742–1763 행): `round(min(총 MiB × 0.85, 여유 MiB × 0.90) / 1024, 1)` (MiB ÷ 1024 = GiB 로 읽힘) · `--gpu-mem` 가 더 크면 깎는다 · `nvidia-smi` 질의가 실패하면 **20** (안전값).
- kgy (참고): 10-01 발사 직전 2,902 MiB 사용 / 21,254 MiB 여유 (prereg 750 행) → 총 24,156 MiB → min(20,532.6 · 19,128.6) / 1024 = **18.7** < 21.06 → 메모리 부족 두 번 (prereg 818 · 852–854 행) 과 맞는다.  (prereg 821 행의 "≈ 20 GB" 는 총 85 % 쪽 값 20.05 와 맞는다 — 추정.)
- gabia: 총 49,140 MiB × 0.85 = 41,769 MiB → **40.8**.  `--gpu-mem 28` 이 안 깎이려면 여유 ≥ 28 × 1024 / 0.90 = **31,858 MiB**.  그러면 풀 28 − 어림 21.06 = **6.94 GiB 남음 (풀의 24.8 %)** ⇒ **산술상 들어간다 (추정)**.
  - ⚠ 한정: 어림은 prereg 가 센 필드 (격자 24 B/칸 · 점 124 B/점) 뿐이다 — Taichi 런타임 · 다른 버퍼는 안 셌고 점 수는 상한이다.  확인 = 건식 (`--frames 1`) 이 **필드 할당 (`finalize_snode_tree` — kgy 가 19–35 초 만에 멈춘 자리)** 을 지나는가 (§5-3).
- 두 팔 동시 = 안 된다 (산술): 첫 팔이 28 GiB 를 잡으면 남는 여유 ≤ 47.99 − 28 = 19.99 GiB → 두 번째 팔 상한 ≤ 0.90 × 19.99 = 18.0 < 21.06.
- 확인 런 (real_14 · 384): kgy 상한 (18.7 – 20) 안에서 완주했다 (⑤ · §12-6 `f = 0`) ⇒ gabia 에서 메모리 문제 없음 (추정).
- 호스트 RAM 62 GB: 점 생성 · 스캐폴드 읽기의 호스트 메모리는 기록이 없다 → [미확인] · 건식으로 확인.

### 3-2. 시간

kgy 실측 (real_14 스캐폴드 · n_grid 384 · RTX 3090 · 시작 · 컴파일 포함 · 일부 GPU 공유):

| 런 | 시작 → 끝 (KST) | 프레임 | s/프레임 | 출처 |
|---|---|---|---|---|
| ⑤ f_(b) 시도 2 | 16:35:54 → 17:06:16 = 1,822 s | 266 | 6.85 | prereg 847 · 851 행 |
| §12-6 `f = 0` | 00:39:26 → 02:42:18 = 7,372 s | ≈ 810 (프레임 줄 162 × 5) | 9.10 | prereg 905 · 909 행 |
| §12-6 f_(a) | 02:42:18 → 10:02:59 = 26,441 s | 3,000 | 8.81 | prereg 909–910 행 |

- **corner 한 프레임 (kgy 급 · 추정)**: 점 수 비 2.006 (SE 부피 65,866 / 32,832 · prereg 798 행) 과 격자 칸 비 8 (768³ / 384³ · 격자는 정육면체 · prereg 821 행) 사이로 본다 → 6.85 × 2.006 = **13.7** ~ 9.10 × 8 = **72.8 s/프레임**.  A6000 ↔ RTX 3090 속도비 = **[미확인]** (리포 기록 없음) — 이 어림은 "kgy 급 GPU" 기준이다.  gabia 의 MPM 실행 시간 기록도 없다 (06-26 ~ 28 런의 시간 기록 없음).
- **프레임당 판 이동 (격자 칸 단위 · 산술 · 봉인 코드 701 · 1784–1798 · 2937–2941 행)**: 스캐폴드 런의 CFL 은 SE 만 본다 · dt = min(2.0e-4, 0.4·dx/√M) · M = λ+2μ (E 1.53 · ν 0.49) = 26.18 · 판 한 프레임 = 0.01·√M·40·dt → n_grid 384: dt 2.0e-4 (상한 2.04e-4 · 안 묾) · **0.157 칸/프레임** / 768: dt 1.018e-4 (상한이 묾) · **0.160 칸/프레임** ⇒ 같은 칸 수를 내려가는 데 드는 프레임은 real_14 팔과 비슷하다 (산술).  corner 의 수렴 프레임 수 자체는 기록이 없다 (kgy corner = 프레임 0).

| 예산 | 팔 하나 최악 (예산을 다 씀) | corner 3 최악 |
|---|---|---|
| 400 | 400 × (13.7 – 72.8 s) = 1.5 – 8.1 h | 4.6 – 24.3 h |
| 3000 | 3000 × (13.7 – 72.8 s) = 11.4 – 60.7 h | 34.4 – 182.0 h (1.4 – 7.6 일) |

- 수렴한 팔은 그 전에 끝난다 (루프는 수렴할 때만 일찍 끝남 · prereg 870 행).
- 확인 런: (가) kgy 30 분 · 400 프레임을 다 써도 400 × 9.10 s = 1.0 h / (나) kgy 2.0 h · 3000 을 다 쓰면 3000 × 9.10 s = 7.6 h (둘 다 kgy 급).
- 건식: kgy 두 팔 95 s (prereg 895 행 · 00:15:10 → 00:16:45 · 1 프레임 + 시작) · corner 건식 = [미확인] (768³ 할당).
- 재시도 1 회 여유 = 팔 하나 최악 (예산 3000 이면 ≤ 60.7 h).
- **ETA 다시 내기**: 첫 corner 팔의 처음 1 시간 프레임 줄 간격으로 s/프레임을 재고 (진행 중 watch 허용 · prereg 888 행), 남은 팔이 예산을 다 쓴다고 쳐서 기한을 넘으면 1저자에게 보고한다 (자동으로 바꾸는 것 없음).

---

## 4. 판정선 — 등록된 것만 다시 쓴다 (새 숫자 없음)

### 4-1. corner

| 판독 | 정의 · 창 (그대로) | 근거 |
|---|---|---|
| 1차 관측량 | 서보 수렴 최종 두께 `thickness_um` (하강 정지 두께 = 보조 · 서로 대체 안 함) | prereg 657–661 행 |
| I_x (x = 0 · a · b) | `I_x = abs(t_x / 19.1455 − 1) ≤ 0.03` · 원 정밀도 값 · 창 [18.571135, 19.719865] µm · 반올림 창 금지 | prereg 775–776 행 |
| 네 칸 (I_a × I_b) | 참·참 = 이 endpoint 로 규약 선택 불가 · 거짓·참 = primary b 적중 · a 불일치 · 참·거짓 = primary b 실패 · secondary a 적중 · 거짓·거짓 = 두 규약과 모델의 조합 모두 불일치 — 각 칸의 "허용되지 않는 해석" 그대로 | prereg 577–582 행 |
| I_0 | 값 보고 (네 칸 밖) | prereg 912–913 행 꼴 |
| 순서 R3v2-a | `t(0) < t(a) < t(b)` · 동률 폭 = 런이 기록하는 두께 판독 분해능 (서보 한 스텝 0.12·vmax 와 격자 한 칸 중 큰 쪽) · 실패 = "예측 실패 / 원인 미식별" · 네 칸과 섞지 않는다 | prereg 584–588 · 729 행 |
| ε_sphere (R3v2-d) | 보고 전용 · 이 등록에서 환산하지 않는다 (JSON 에 ε_sphere 필드 없음 · se-dump 겹침 오프셋은 ∝ 1/h 이고 corner 겹침 부피는 잰 적 없음) · JSON porosity 는 "MPM 관례" 표지로만 | prereg 589–591 · 309–338 · 926 행 |
| §9 R2.5-v2 | ⬜ Q8 (권고: 채점 안 함 · `am_load_split` 기록만) | prereg 255–278 · 916–925 행 |

- **구제 금지** (prereg 592–593 행): b 가 빗나가도 f 역산 재실행 · 창 이동 · 정지 시점 교체로 구제하지 않는다 · 두 팔이 다 빗나가도 *"AM 하중분담 모델 일반을 기각"* 이라 쓰지 않는다 · 새 가설 = 실패를 보존한 별도 등록 (prereg §7 191–195 행).
- 모든 결과 문장에 §0 고지를 붙인다.

### 4-2. 확인 런 (⬜ Q1 · Q7)

- **새 판정선을 만들지 않는다** (권고).  (가) 이면 gabia 두께 t_b′ 와 I_b′ (같은 창 [29.3716, 31.1884] µm · prereg 565–566 행) 와 kgy 29.491 µm 와의 차를 **값으로** 적는다 · (나) 이면 kgy 25.842 µm 와 같은 꼴.
- 바꾸지 않는 것: kgy 의 I_b (prereg 851 행) · corner 판정 · real_14 네 칸 (미배정).
- 차가 동률 폭 (prereg 729 행 규칙 · 런이 기록) 보다 크면 corner 결과에 *"기계 한정 (kgy ↔ gabia 차 > 두께 판독 분해능)"* 한정어 (Q7).
- **기술 관문** (값 관문 아님): 확인 런이 python 오류 · CUDA 오류 · 예산 안 미수렴이면 corner 를 띄우지 않고 1저자에게 (kgy 는 같은 argv 로 수렴했으므로 환경 문제를 먼저 본다).

### 4-3. 결과 뒤 적는 순서 (prereg 889 행 꼴)

12-4 분류 (모든 팔 · 모든 시도) → 확인 런 값 → I_0 · I_a · I_b (값) → 네 칸 → 순서 → 보고 전용 (ε · `am_load_split`) → §0 고지 병기 → 열람 이력 추가.

---

## 5. gabia MPM 환경

### 5-1. kgy 에서 기록된 것 (FAM 런이 실제로 돈 환경)

- 인터프리터 `/home/kgy/apps/miniforge3/envs/ti310/bin/python` (prereg 894 행 · ⑤ 와 §12-6 이 같은 절대 경로).
- conda `ti310` = Python 3.10 · taichi 1.7.3 (`docs/reviews/vgcf_e_sensitivity_prereg_20260925.md` 69 행) · 11-02 kg50 런 = Python 3.10.21 (`docs/data/kg50_mpm_20261102/README.md` 3 행) · **numpy · scipy 판 = [미확인]** (리포 기록 없음) · `mpm` env 는 numpy 가 없다 (`config/env_db.json` kgy · prereg 748 행).
- 봉인 코드가 부르는 것: numpy · scipy (`spatial.cKDTree` · `sparse` · `ndimage`) · taichi (CUDA) · `nvidia-smi` (메모리 상한 질의 · 1752–1755 행) · 리포 모듈 `additives` 는 `--add-recipe` 때만 (이 argv 에 없음).
- 참고: Taichi CUDA = 드라이버만 필요 (휠이 CUDA 런타임을 품는다 · `docs/server_setup.md` 10 · 34–35 행) · 09-23 CPU 스모크는 taichi 1.7.4 였다 (`docs/reviews/codex_fam_r3v2_verdicts_20260922.md` 450 행) — 같은 캠페인 안에서도 판이 달랐다.

### 5-2. gabia — 아는 것 · 모르는 것

- 아는 것 (진행 기록 1267 행): §2-1 하드웨어 · 리포 있음 · `~/rint-venv38` (uv CPython 3.8.20 · `fastrlock` 0.8.2 고정 · kgy `~/dem-venv` 판 = Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1 · cupy 12.3.0 으로 맞추는 중).
- ⛔ `~/rint-venv38` 은 **Rint ② R 전용**이다 — Rint R 은 두 기계 단위를 합치려고 python · numpy · scipy 판을 kgy 와 같게 묶었다 (`docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` 27 · 104 · 210 행 · `docs/handoff_return_to_stoic_knuth_20261103.md` 69 행).  여기에 taichi 를 넣거나 판을 바꾸지 않는다 ⇒ **MPM 은 따로 env** (Q9).
- 모르는 것: gabia 리포의 커밋 · MPM 용 파이썬 · taichi 유무와 판 · 06-26 ~ 28 MPM 런의 환경 (기록 없음) · 호스트 메모리 여유 · A6000 의 프레임 속도.
- 병행: Rint 쪽 gabia 환경 시험 (`scripts/check_kgy_py38.sh` · 합성 시험 · 스크립트에 GPU · cupy · nvidia 낱말 없음) 은 CPU 라 FAM GPU 팔과 함께 돌 수 있다 — 같이 돌면 그 사실을 적는다.

### 5-3. 발사 전 점검 (prereg §12-6-1 · 887 · 891–903 행 꼴 · 결과 0 건 상태)

1. **봉인 사본**: `7f44d6534` 트리 + corner CSV 둘 (커밋 `cf5103c94`) — 러너 앞머리 검사 = `SEAL_COMMIT` = 7f44d6534 · mpm3d md5 c31f0512021d416702e162709c6f4400 · CSV 넷 sha256 (§2-2) · 하나라도 다르면 시작 거부 · 러너는 `git` 을 부르지 않는다 (prereg 829–830 행).
2. **환경**: `$PY` 의 Python · taichi · numpy · scipy 판을 출력해 적는다 · `nvidia-smi --query-gpu=memory.total,memory.free --format=csv,noheader,nounits` 가 숫자 둘을 낸다 (못 내면 코드가 20 으로 깎는다 → corner 메모리 부족).
3. **GPU · 프로세스**: 각 팔 시작 직전 `nvidia-smi` (사용 · 여유) 를 로그에 적는다 · 여유 < 31,858 MiB 면 그 팔을 시작하지 않고 멈춘다 (런 시도 아님) · 다른 MPM 파이썬이 있으면 시작 거부 — `pgrep -f '[m]pm3d_compaction.py'` (watch 명령 자기 매칭 사고 · `docs/reviews/vgcf_e_sensitivity_prereg_20260925.md` 81–83 행).
4. **건식** (`SELF-78` 교훈 · prereg 887 행): 각 팔 줄 끝에 `--frames 1` (argparse 는 마지막 값) · 출력 `dryrun/` · 보는 것 = rc · `[stop]` · `Traceback` · `CUDA_ERROR` · `capping to` 줄 · 프레임 줄 **개수** · JSON 필드 **수** · 걸린 시간 (값 미열람 · prereg 895 행).  기대: corner f_(a) · f_(b) = rc 1 + `[servo] 평형이 …` (1 프레임의 등록된 중단 · JSON 없음 · prereg 900 행 꼴) · corner `f = 0` (플래그) = rc 0 + JSON (prereg 899 행 꼴) · 어느 팔에도 `capping to` 없음 (= 풀 28) · `CUDA_ERROR` 없음 · 확인 런 (가) = rc 1 같은 꼴 · (나) = rc 0.  건식은 런 시도로 세지 않는다.
5. **러너** (이름 = 제안): run_s127.sh (팔 줄 = §2-4 · §2-5 글자 그대로 · `python3` 자리 = `$PY`) · 건식 dry_s127.sh · 시작 줄 `§12-7 시작` (시각) · 로그 batch_s127.log · 두 러너 md5 를 12-7-1 에 적는다.
6. **열람 규칙** (prereg 888 · 927–928 행 교훈): 진행 중 watch = 마지막 프레임 줄 허용 · 정지 · 실패 팔 = 상태 줄만 (`grep -E 'rc=|Error|Traceback|servo_status|\[stop\]|CUDA_ERROR|capping to|converged'`) · `FINAL` 줄과 프레임 줄 (두께 · porosity) 은 적격 완주 팔에서만 · 실패 팔 끝을 `tail` 로 열지 않는다.

### 5-4. 12-7-1 봉인 칸 (발사 전 채움 · 지금 전부 ⬜)

| 칸 | 값 |
|---|---|
| 비준 커밋 = 봉인 시각 (prereg §12-7 로 옮긴 커밋) | ⬜ |
| Q1 – Q13 답 | ⬜ |
| gabia 봉인 사본 경로 · `SEAL_COMMIT` · mpm3d md5 실측 | ⬜ |
| CSV 넷 sha256 실측 | ⬜ |
| `$PY` 경로 · Python · taichi · numpy · scipy 판 | ⬜ |
| `nvidia-smi` 총 · 여유 (각 팔 직전) | ⬜ |
| 러너 · 건식 러너 md5 | ⬜ |
| 건식 표 (팔 · rc · 프레임 줄 수 · 상태 줄 · 걸린 시간) | ⬜ |
| 발사 시각 (= `§12-7 시작` 줄) | ⬜ (= 1저자) |

---

## 6. 일정 (오늘 11-03 (화) · 날짜는 전부 **추정**)

| 날짜 | 할 일 | 비고 |
|---|---|---|
| 11-03 (화) | 이 초안 | 결과 0 건 |
| 11-04 (수) | 1저자 Q1 – Q13 → 비준 (prereg §12-7 로 옮긴 커밋 = 봉인 시각) | ⬜ |
| 11-04 (수) ~ 11-05 (목) | gabia MPM env · 봉인 사본 · 해시 · `nvidia-smi` · 건식 → 12-7-1 칸 | 1저자 기계 작업 · 소요 [미확인] |
| 11-05 (목) ~ 11-06 (금) | 발사 (1저자) — 확인 런 → corner 3 (Q5 순서) | |
| 11-07 (토) ~ 11-13 (금) | 끝 — 예산 3000 · 11-06 0 시 발사 가정 · 모든 팔이 예산을 다 써도 하한 ≈ 35 h · 상한 ≈ 183 h ((가)) – 190 h ((나)) | 수렴한 팔은 더 일찍 |
| ~ 11-16 (월) | 상한 + 재시도 1 회 (+ 60.7 h) | |
| **11-10 (화) 안** | **발사 마감** — 상한 190 h + 재시도 61 h = 251 h ⇒ 11-10 24:00 발사여도 11-21 11 시 무렵 끝 (권고 기한 11-21 12:00 안) | 기한 = Q6 |
| 11-21 (토) ⬜ 시각 | 기한 정지 (Q6) · 결과 반입 · 12-4 분류 | |
| 11-22 (일) | gabia → Rint ② R | 진행 기록 1268 행 |

- Rint R 의 길이 (참고): 두 대 나눔 110.1 – 159.4 h (`docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` 189 행 · 추정) — FAM 이 11-21 을 넘기면 Rint R 시작 (≤ 11-22 · 진행 기록 1268 행) 을 민다 ⇒ 기한 규칙 (2-9) 은 넘겨 돌리지 않는 쪽으로 정했다.

---

## 7. 1저자가 정할 것

**[FAM §12-7]**

- **Q1** 확인 런 1 = 무엇인가 (§1-2 표 (가) – (마) · 리포 글에 정의 없음) — 권고: (가) real_14 f_(b) 0.8085 를 ⑤ argv 그대로 gabia 에서 (가장 싼 기계 확인 · kgy 판정은 그대로).
- **Q2** corner 프레임 예산 400 (봉인 그대로) / 3000 (§12-6 규칙) — 권고: 3000 (루프 길이뿐 · 수렴 런은 비용 0 · 400 은 real_14 에서 모자랐다 · 상한 어림도 기한 안) · 3000 안 미수렴 = `EXECUTION_FAILED` · 추가 등록 없음.
- **Q3** corner `f = 0` 팔에 `--allow-unconverged-servo` (§12-6 의 R1 레시피) — 권고: 넣는다 (안 넣으면 런 전 관문이 확정 거부 · 적격 = 수렴 줄 ∧ `porosity_at_target_pct` 비-None 그대로).
- **Q4** 격자 768 · `--gpu-mem 28` 그대로 — 권고: 그대로 (산술 21.06 GiB < 28 · argv 동일) · 건식이 필드 할당에서 멈추면 발사하지 않고 다시 묻는다 (그때의 안 = `--gpu-mem` 만 올림 · 기계 인자).
- **Q5** corner 순서 = 봉인 `0 → a → b` / `b → a → 0` — 권고: 확인 런 → `b → a → 0` (기한 고정 · 순서는 값에 영향 없음 · primary 먼저).
- **Q6** 기한 시각 · 처리 — 권고: 11-21 (토) 12:00 KST 또는 1저자가 Rint R 에 비우라고 한 시각 중 이른 쪽 · 도는 팔 정지 = *"미완주 — 실패 아님 · 판정 없음"* · 이어 돌리기 = Rint R 뒤 새 등록.
- **Q7** 확인 런의 쓰임 — 권고: 값 보고만 (새 판정선 없음) · kgy I_b · corner 판정 · real_14 네 칸 불변 · 차가 동률 폭보다 크면 corner 에 "기계 한정" · 기술 실패 (오류 · 예산 안 미수렴) 면 corner 전에 멈추고 보고.
- **Q8** §9 R2.5-v2 를 corner `f = 0` 에도 채점하나 — 권고: 채점 안 함 · JSON `am_load_split` 기록만 (§9 는 real_14 등록 · real_14 에서 v2-b 빗나감 = 절단면 판독 무의미를 이미 봤다 · 본 뒤의 새 적용은 사후 시험).
- **Q9** gabia MPM 환경 = 새 env (`~/rint-venv38` 손대지 않음) — 권고: 예 · kgy `ti310` 의 `python -V` · `pip freeze` 를 먼저 받아 같은 판 (Python 3.10 · taichi 1.7.3 기록) 으로 · 다르면 그 차이를 결과에 적는다.
- **Q10** 코드 사본 = gabia 에 `7f44d6534` 트리 + corner CSV 둘 · 러너 앞머리 `SEAL_COMMIT` · md5 · sha256 넷 — 권고: 예 (kgy `~/dem-fam` 방식 · 가지 끝 코드는 쓰지 않는다).
- **Q11** kgy corner 두 시도 (§12-5-9) 를 이 등록의 재시도 수에 넣나 — 권고: 넣지 않는다 (그 봉인에서 닫힌 기록 · 새 등록 · 새 기계) · 결과 문장에 함께 적는다.
- **Q12** 발사 전 Codex 검토 — 권고: §12-6 과 같은 기준 (1저자 비준 + 건식) 유지 · §12-5 봉인 · §12-6 은 Codex 해제 조건 (`docs/reviews/codex_fam_r3v2_verdicts_20260922.md` §8) 을 반영한 뒤 1저자 비준으로 발사했다 (Codex GO 회차 없음) — 넣으려면 발사 마감 (11-10) 안에 회신이 와야 한다.
- **Q13** 정본 위치 — 권고: 비준 뒤 이 내용을 prereg §12-7 로 옮긴 커밋을 봉인으로 · 이 파일은 머리에 "이력 · 정본 = prereg §12-7" 표지.

---

## 부록 — 이 초안이 11-03 에 직접 다시 확인한 것

- 봉인 커밋 `7f44d6534` 의 `scripts/mpm3d_compaction.py` blob md5 = c31f0512021d416702e162709c6f4400 (prereg 750 행과 같음) · 가지 끝 (`claude/stoic-knuth-NObVQ` · origin 같음) md5 = cae40a894339d3b0db32ac3dfc6c1846 · 그 사이 이 파일을 바꾼 커밋 = `dd161fd3f` · `cb5a6a445` (10-14).
- CSV 넷 sha256 (§2-2) · 행 수 (머리 1 줄 빼고 457 · 32,832 · 104 · 65,866) · corner CSV 둘 = 커밋 `cf5103c94` 의 blob 과 같음 · 봉인 트리에 corner CSV 없음 (`7f44d6534` = 2026-09-30 15:01:38 UTC · `cf5103c94` = 17:40:49 UTC).
- 봉인 코드 행 (`7f44d6534` 판): 696 (`--frames` 기본 400) · 700–701 (`--sub` 40 · `--dt` 2.0e-4) · 1742–1763 (메모리 상한) · 1784–1798 (CFL · 스캐폴드는 SE 만) · 2937–2941 (판 속도) · 2951–2962 (관문) · 3093 (프레임 루프) · 3586 (미수렴 내보내기) · 3720 (`frames_budget`).
- `scripts/check_kgy_py38.sh` 에 GPU · cupy · nvidia 낱말 없음.
- 인용한 커밋 여섯 (`7f44d6534` · `cf5103c94` · `510c25371` · `eb52d09d3` · `cb5a6a445` · `dd161fd3f`) = `origin/claude/stoic-knuth-NObVQ` 에서 닿는다.
- 산술 (§3) = 이 초안이 파이썬으로 다시 셈 — 입력은 위 표의 기록 숫자뿐.
