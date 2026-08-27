# A 트랙 현황 — **INVALID (처치 미적용) → 재실행 대기** (2026-08-27)

> 사용자 지시 2026-08-27: **"A 4런은 기억해 — Table S3 확보 이후 진행하자."**
> ⇒ W2(재압밀) → W4(최종 STEP3 · Table S3) 를 먼저 하고, A 는 그 뒤에 재개한다.

## 1. 1차 4런 판정 = `INVALID_TREATMENT_NOT_APPLIED`

브리지 팔의 σ_e·dof 가 off 팔과 **비트 단위로 동일**했다.  원인: 러너에
`SDCP_SPHERE_D` 를 안 넘겨 **점 스탬프**로 돌았고(OUTDIR 에 `_sph` 없음),
`step3_sigma.rasterize` 의 브리지 가드가

    if sdcp_sphere_d_um and float(sdcp_bridge_um) > 0.0:

라 **앞 조건이 False** 여서 아무 일도 안 했다.  러너·payload 는 `★ 진단 팔 — SDCP 접촉
브리지 0.01 µm` 을 찍었지만 **효과 0** = fail-open.
⇒ 개정 A1 을 형식적으로 적용하면 `A = 1 − ΔR_on/ΔR_off = 0` 이라 h0 이지만, **처치가
가해지지 않았으므로 그 h0 은 가짜다.**  판정하지 않는다.
⚠ 이 부류를 위해 만든 `--compare-dir --expect-differ` 를 **쓰지 않았다** (등록 축이 실제로
다른지 보는 계약).  다음 런에서는 쓴다.

## 2. 그래도 건진 것 — p2 **점 스탬프** 격자 2점 (8팔 봉인, cg 0, gpu)

| | R̄ (쌍대응) | SE |
|---|---:|---:|
| vox 0.15 | **1.016076** | 0.000574 |
| vox 0.125 | **1.009670** | 0.000896 |
| **ΔR (0.125 − 0.15)** | **−0.006406** | 0.001348 |

- 격자를 조이면 비가 **내려간다** (|ΔR| 이 SE 의 4.8배 = 유의).
- ⚠ 점 스탬프는 SDCP 표현부피가 참값의 **0.238배**라 물리 격자가 아니다 (CL-33) —
  **강도 프로브로만** 읽는다.  원고 인용 금지.
- ★ 참고: p1 시절 점 스탬프 값(CL-33 계열)과 자릿수·크기가 비슷하다 ⇒ plate 규칙 p1→p2 가
  **이 축의 비는 크게 안 바꿨다**는 정황.  ⚠ 정량 비교는 안 한다 (p1 값은 hold).

## 3. 재실행 (Table S3 확보 후)

```bash
cd ~/sdcp
for V in 0.15 0.125; do
  ARMS=8 LEAN=2 VOX=$V SDCP_SPHERE_D=0.30 bash ~/Yonghoon-DEM-DFT/scripts/sdcp_gain_vox015_8arm.sh
  ARMS=8 LEAN=2 VOX=$V SDCP_SPHERE_D=0.30 SDCP_BRIDGE=0.01 bash ~/Yonghoon-DEM-DFT/scripts/sdcp_gain_vox015_8arm.sh
done
```
★ 시작 1분 안에 **OUTDIR 에 `_sph` 가 있는지** 확인할 것 (없으면 또 헛돈다).
확인됨: 재실행 시도에서 `prereg_v2_vox015_sph_b048_lean2_r07abecad1459` 로 정상 생성.
판정은 **개정 A1** (`sdcp_bridge_prereg_amendment_A1_20260827.md`, 커밋 `a4636d15`) 대로.
⚠ 완주한 팔은 SKIP 되므로 중단해도 낭비가 없다.

## 4. 코드 수정 — ★ 완료 (2026-08-27)

**브리지 fail-open → fail-closed.**  진단만 남기고 넘어가면 재개 런에서 같은 실수가 그대로
반복된다 (러너 호출은 손으로 쓴다) — 그래서 **기전 자체를 코드에서 막았다.**

### 무엇이 잘못돼 있었나
`step3_sigma.rasterize` 의 가드가
```python
if sdcp_sphere_d_um and float(sdcp_bridge_um) > 0.0:
```
였다.  구 스탬프가 꺼져 있으면 **요청한 브리지를 조용히 버린다**.  매니페스트에는 요청값
`sdcp_bridge_um = 0.08` 이 적히고 격자에는 브리지가 없다 ⇒ 처리팔이 대조팔과 **바이트 동일**.
판정기는 런이 **끝난 뒤에야** 그것을 본다.

### 두 층으로 막았다 (둘 다 필요하다)
| 층 | 자리 | 언제 죽나 | 이것만으론 왜 부족한가 |
|---|---|---|---|
| ① 러너 | `sdcp_gain_vox015_8arm.sh` — `SDCP_BRIDGE` 있는데 `SDCP_SPHERE_D` 비면 `exit 2` | **초 단위** (DEM 전) | 러너를 안 거치는 호출(직접 payload)은 못 막는다 |
| ② 물리 | `rasterize` 가 `ValueError` | 격자 찍기 직전 | 이미 DEM·MPM 을 몇 시간 돌린 뒤다 |

### 검사기가 **무는지** 확인했다 (추가 ≠ 묾)
- 새 selftest `sdcp-bridge-failclosed` — 세 갈래: 거부 · 기본값 무해 · 정상 조합 통과.
- 돌연변이 `SELF-11b`(가드 무력화 = **2026-08-27 결함 그대로 복원**)를 그 시험 **하나만** 물었다.
- 러너 가드는 양방향 실동작 확인 (브리지만 → ABORT · 둘 다 → 통과).
- 배터리 전체 **69/69 초록** (기대 밖 실패 0 · harness 사고 0).

### 못 무는 자리 — 적어 둔다
과발화 방향(가드가 정상 조합까지 거부)은 **돌연변이로 못 문다**.  실제로 넣어 봤고
(`and` → `or`) 결과는 `HARNESS_ERROR` 였다: 과발화한 가드는 `sdcp-bridge-connect` ·
`no-downgrade` · `sbe-noop` 이 rasterize 를 부르는 순간 잡히지 않은 `ValueError` 로 스크립트를
죽여서, 이름 붙은 FAIL 이 아니라 크래시가 된다.  좁게 무는 변이는 **존재하지 않는다** —
legit 조합에 걸면 브리지 시험이, 기본값에 걸면 점 스탬프 시험 전부가 죽는다.
억지로 초록을 만들면 `HARNESS_ERROR` 신호가 무뎌지므로 **넣지 않았다.**  대신
① 시험 안의 양성 대조(`_e5b` 기본 off · `_e5c` 정상 조합) ② 과발화는 **조용하지 않다**
(selftest 가 통째로 크래시 → `check_all` 즉시 빨간불) 로 방어한다.  fail-open 과 정반대의
가시성이라는 점이 요지다.

⚠ 이 봉인은 **1차 런을 되살리지 않는다** — 그 4팔은 여전히 무효이고, 살아남은 숫자는
p2 점 스탬프 프로브뿐이다 (인용 불가).  §3 재실행 명령의 `SDCP_SPHERE_D=0.30` 은 이제
빠지면 30시간을 태운 뒤 무효가 나오는 대신 **시작 즉시** 죽는다.
