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

## 4. 코드 수정 필요 (미착수)

**브리지 fail-open → fail-closed**: `--step3-sdcp-bridge > 0` 인데 구 스탬프가 꺼져 있으면
**중단**해야 한다 (지금은 조용히 no-op).  회귀 + 돌연변이 동반.
