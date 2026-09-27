---
title: "리뷰 CE 프롬프트 — A′ V5 (LPSCl|Ag(111) 작은 주기 계면) VASP 외주 패키지 준비본: QE→VASP 대응 · INCAR · 쌍극자 · D3 · 반송 검사 · G3 경계선 예측"
date: 2026-09-27
updated: 2026-09-27
tags: [review, codex, adhesion, wad, prereg, vasp, outsourcing, lpscl, silver, uma, d3, dipole, g5]
status: 발송 대기 (1저자) — 패키지·개정 3 은 커밋 8f76b912d 에 고정
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 CE — A′ V5 를 VASP 외주로 돌리는 **준비본** 설계 리뷰

> 트랙 W_ad (점착) → 1저자 = 사용자. 정본 브랜치 `claude/friendly-meitner-lldvar` · **커밋 `8f76b912dd70f47b32a23cbcc1ad96525a97e69c`** (아래 해시는 전부 이 커밋의 트리에서 `tools/review_manifest.py --require_pushed` 로 뽑았다 · 원격에 있음).
> 상황: A′ 카드 v5 의 **V5** (SE 2층 + Ag(111) 3층 · 176–200 원자) 는 QE CPU 추정 89–109 GB @70 Ry (축소 변형 61–80 GB) 라 우리 GPU 한 장(48 GB)에 안 들어가 **RESOURCE_BLOCKED → G5 NOT_TESTED** (갈래0 · 전체 계면 UMA 예측은 내부 전용). 1저자가 *"V5 를 VASP 외주건으로 만들어 보고 리뷰 받자 · 될지는 모르지만 준비는 해두자"* 고 했다 — **업체·예산 미정 · 준비본**.
> 이 리뷰는 **보내기 전 필수 수정**을 찾는 것이다. 판정: GO / 조건부 GO / NO-GO.

## §0. 한 장 요약

| 항목 | 내용 |
|---|---|
| 잡 | **18 단일점** (이완 없음) — G5 표본 ①–⑤ 끝점 9 (⑤ 는 bound 만 · far 는 ① 공유) + G3 c+2 셀 3 (표본 ①) + G4 변형 6 (표본 ① · ENCUT 650 · Γ 4×3×1 · SIGMA ½) |
| 기하 | 봉인 S3v2 구조 13 개 그대로 — 빌더가 구조 파일 sha 를 S3v2 manifest(=seal)와 대조, 다르면 패키지를 만들지 않는다. POSCAR 는 종 순서 Li P S Cl Ag · 원래 원자 번호 대응표는 jobs.json |
| INCAR | `GGA=PE · PREC=Accurate · ENCUT=520 · EDIFF=1E-6 · NELM=200 · NELMIN=6 · ALGO=Normal · ISPIN=1 · ISMEAR=1 · SIGMA=0.136 · LASPH=T · LREAL=F · ISYM=0 · IBRION=-1 · NSW=0 · IVDW=12 · VDW_S6/S8/A1/A2=1.0/0.7875/0.4289/4.4407 · LDIPOL=T · IDIPOL=3 · DIPOL=0.5 0.5 z_c · LWAVE=F · LCHARG=F` |
| 쌍극자 | QE 에서 쓰던 톱니 불연속 구간(개정 2: 집합의 진공 중앙 · 폭 1 Å · 양쪽 핵 ≥ 4 Å) 의 중심을 옮긴다: **DIPOL_z = (emaxpos + eopreg/2 − ½) mod 1** — "VASP 보정의 불연속은 DIPOL ± ½ 에 놓인다" 는 전제. 빌더가 VASP 구조에서 여유 ≥ 4 Å 를 다시 잰다 (실측 전 잡 4.0 Å) |
| POTCAR | PAW_PBE **Li_sv · P · S · Cl · Ag** (PBE_54 권장) — 업체 라이선스분을 러너가 `POTCAR.spec` 순서로 조립 · 반송은 TITEL/ZVAL 줄 + sha256 만 |
| k | Γ 3×2×1 (QE 와 같은 격자) · G4 변형 Γ 4×3×1 |
| 재시도 | 미종료·미수렴이면 사전등록 `INCAR.r1` (AMIX 0.1 · BMIX 0.01 · NELM 300 · 그 밖 동일) **1 회만** — 그래도 실패면 그 잡 값 없음 |
| 러너 | `run_all.sh`: MANIFEST `sha256sum -c` → 성능 태그(NCORE/NPAR/KPAR/NSIM/LPLANE/LSCALU/LSCALAPACK)만 `PERF_TAGS_FILE` 로 덧붙임 (허용 밖이면 실행 안 함) → POTCAR 조립 → 실행 → "General timing" · "aborting loop because EDIFF is reached" 검사 → 반송 tgz + sha256 · **파일럿 1 잡 먼저** (V5_s_outer_A_far) |
| 반송 검사 | `--check` fail-closed: MISSING · INPUT_MODIFIED · POTCAR_MISMATCH/UNVERIFIED · NOT_TERMINATED · SCF_NOT_CONVERGED · SYSTEM_MISMATCH (NIONS·NELECT) · D3_UNVERIFIED (Edisp 줄 없음) · D3_MISMATCH (Edisp vs s-dftd3 2체 > 1 %) → OK 아닌 잡은 판정 제외 · r1 은 사전등록 INCAR.r1 일 때만 채택 (첫 시도 상태 보존) |
| 집계 | `--collect`: W = [F(far) − F(bound)]/A (F = TOTEN · E(σ→0) 병기) · ΔD3 = [Edisp(far) − Edisp(bound)]/A · W_PBE = W − ΔD3 · G3 |ΔW| ≤ 0.01 두 검사 · G4 ≤ 0.02 · G5: W_UMA+D3 := W_UMA + ΔD3_VASP (개정 1 구조) → Δ_i = W − W_UMA+D3 · 표본 |Δ| ≤ 0.10 · 종결 군(S ①②⑤ · Li ③④) |mean| ≤ 0.05 · 5/5 · G3·G4 PASS → PASS · 분모 5 고정 |
| 규모 | NIONS 176–200 · NELECT 1356–1452 · 기본 NBANDS ~826 · 평면파 ≤ 2.4e5/k (ENCUT 650 변형) · 파동함수 합 ≤ ~16 GB — 시간은 파일럿 벽시계로 |
| 비교군 | **VASP PBE+D3(BJ) V5 비교군** — QE 값(V2 · V4 · SE|SE)과 빼거나 섞지 않는다 |

## §1. QE → VASP 대응 (개정 3 초안 `wad_aprime_pilot_prereg_v5_amendment_3_vasp_v5_2026_09_27.json`)

- **그대로**: 기하 · 표본 ①–⑤ · 끝점(직접 8 · 영상 9) · G3 c+2 두 검사 · G3/G4/G5 식·문턱·분모 · 개정 1 의 D3 장부 구조 · 3체(ATM) 별도 열 결정 · UMA 쪽(S1 결박 · 우리가 `relax_uma_d3.py --energies` 로 9 구조 단일점).
- **바뀜**: QE 7.4.1 → VASP 6.x · GBRV/PSL/ONCV(Ag 19 e) → PAW_PBE (Ag 11 e) · 52/520 Ry → 520 eV (G4 650) · MV 0.01 Ry → MP1 σ 0.136 eV (VASP 에 MV 없음 · 같은 폭 숫자) · QE 내장 D3 → IVDW 12 명시 계수 · QE 톱니 → LDIPOL/IDIPOL 3/DIPOL · conv_thr 1e-8 Ry → EDIFF 1e-6 eV.
- **G5 해석**: UMA(OMat24) 학습 기준이 VASP PBE (PAW) 이라, VASP V5 와의 G5 는 QE 때보다 코드 차이 몫이 적다 — 보증은 여전히 지정 유한 표본의 오차 제한뿐.

## §2. 결과 전 예측 — D3 꼬리만으로 본 G3 (DFT 없음 · s-dftd3 2체 · 기하 고정)

- **V2 검정**: D3 만 예측한 G3(ii) 변화 +0.0132 vs 실측(QE 전체) +0.0136 J/m² — V2 의 G3 FAIL 은 97 % 가 D3 꼬리였다.
- **V5 표본 ①**: (i) 영상 검사 +0.0056 · (ii) 직접 검사 **+0.0095 J/m²** (문턱 0.01 · 여유 0.0005) ⇒ **경계선**. PBE 몫이 V2 처럼 +0.0004 만 보태도 FAIL.
- 카드상 G3 가 PASS 가 아니면 G5 는 PASS 불가(오차표만) — 외주 비용을 쓰고 G5 가 구조적으로 막힐 위험이 있다.
- 참고: V5 의 2체 ΔD3 (8 Å) ① 0.541 · ② 0.547 · ③ 0.591 · ④ 0.591 · ⑤ 0.407 J/m² — W 의 대부분이 분산 몫일 가능성 (V2 는 W_PBE −0.055).

## §3. 시험

- `build_v5_vasp_package.py --selftest` **37/37** — 음성: 모르는 원소 · 쌍극자 여유 부족 3 (위쪽 원자 · 기판 바닥 위 영상 · 경계) · 반송 11 상태 (MISSING · INCAR 값 변경 · 허용 밖 태그 추가 · POTCAR 다름 · TITEL 없음 · 미종료 · 미수렴 · NIONS · NELECT · Edisp 없음 · Edisp 1 % 초과) · KPOINTS 변조 · r1 폴더에 사전등록이 아닌 INCAR · G3 FAIL → G5 PASS 아님 · 표본 |Δ| 초과 · 군 평균 초과 · 표본 누락(분모 5).
- **돌연변이 5** 전부 빨간불: DIPOL 에서 −½ 제거 · 성능 태그 허용 제거 · D3 대조 끄기 · G5 군 평균 검사 제거 · G5 가 G3/G4 를 안 봄.
- **끝-끝**: 가짜 VASP + 가짜 POTCAR 로 `run_all.sh` 18 잡 → 한 잡은 첫 시도 미수렴 → r1 수렴 채택 · POTCAR 반송 안 됨 · tgz 를 `--check` 로 전 잡 OK. 러너 음성: 허용 밖 성능 태그 → 실행 거부 · 패키지 변조 → `sha256sum -c` 로 실행 거부.
- QE↔s-dftd3 D3 절대값 차 실측 0.06–0.10 % (V2 두 끝점) → D3_MISMATCH 문턱 1 % 의 근거 (감쇠·3체 오설정은 ≥ 5–7 % 차).

## §4. 질문 (보내기 전 필수 수정만 P0/P1 로 · 나머지는 권고)

- **Q1 코드 교체의 정당성** — V2 · V4 는 QE 인데 V5 만 VASP 로 해도 카드의 G5 목적(UMA+D3 가 PBE+D3 를 재현하나)에 맞는가. "별도 비교군" 규칙으로 충분한가. V2(Ag|그래핀 · 20 원자)를 VASP 로도 한 번 돌려 **코드·PP 다리**(같은 기하에서 ΔW_QE−VASP)를 재 두는 것이 필요/권고인가.
- **Q2 smearing** — MV 0.01 Ry 대신 MP1 σ 0.136 eV · W 에 F(TOTEN) 를 쓰고 E(σ→0) 는 병기 — 금속 Ag + 절연 SE 계면에서 적절한가. σ 를 더 작게(예 0.05) 잡고 G4 를 σ 두 배로 하는 편이 나은가.
- **Q3 쌍극자** — DIPOL_z = 구간 중심 − ½ (VASP 불연속 = DIPOL ± ½) 전제가 맞는가. IDIPOL 3 · LDIPOL T · EFIELD 없음 · ISYM 0 조합에 빠진 것(예: 비대칭 슬랩에서의 권장 태그)이 있는가. 여유 ≥ 4 Å 재검사로 충분한가.
- **Q4 D3** — IVDW 12 + 명시 계수가 PBE-BJ 2체와 같은가 (VASP 는 3체를 넣지 않는다는 전제). 실공간 절단(VDW_RADIUS · VDW_CNRADIUS 기본) 이 QE/s-dftd3 와 달라 생기는 차이가 W 에 의미 있는가. Edisp 1 % 대조가 적절한 문턱인가 · OUTCAR 의 Edisp 줄 문구(버전별)에 대한 대비(파일럿으로 확인) 가 충분한가.
- **Q5 수치 설정** — ENCUT 520 (Li_sv ENMAX 499 의 1.04 배 · 고정 기하 에너지 차) · G4 650 · PREC Accurate · LREAL F · LASPH T · EDIFF 1e-6 · NELM 200 · ALGO Normal · 기본 혼합 → 재시도 AMIX 0.1/BMIX 0.01. 200 원자 Ag 슬랩 + 진공에서 처음부터 다른 혼합(예: Kerker 조정 · ALGO All)을 넣어야 하는가.
- **Q6 POTCAR** — Li_sv/P/S/Cl/Ag · PBE_54 권장 (64 허용?) · TITEL/ZVAL 대조 + sha 기록으로 충분한가. TITEL 날짜까지 고정해야 하는가.
- **Q7 G3 경계선 (§2) · 결과 전 결정 후보** — (3b) G5 의 Δ 에서 D3 항은 정확히 상쇄되므로, **G5 자격용 G3 는 W_PBE(= W − ΔD3) 로 판정**하고 총 W 의 G3 는 보고 라벨로 남기는 안. (3c) G3 FAIL 일 때 G5 상태를 "INCOMPLETE (G3 FAIL · 오차표만)" 으로 명시하는 안 (도구는 지금 이렇게 한다). V2 의 G3 결과를 이미 봤다는 점에서 3b 가 사후 조정인가, 아니면 V5 결과 전이라 정당한가.
- **Q8 반송·무결성** — 상태 어휘·우선순위 · 성능 태그 화이트리스트 · r1 채택 규칙 · MANIFEST 흐름에 구멍이 있는가. 파일럿을 **1 잡 → 2 잡 (① bound+far)** 으로 늘려 W 한 값을 먼저 보는 편이 나은가 (그 경우 결과를 본 뒤 설정을 바꾸지 않는다는 규칙이 필요).
- **Q9 규모·견적** — 업체 견적에 빠진 정보가 있는가 (환원 k 수 · KPAR 권고 · 코어·메모리 · 벽시계 · 재시도 최악).
- **Q10 서술** — 개정 3 의 허용·금지 서술이 충분한가. G5 PASS 뒤 전체 계면 UMA 예측을 DEM 에 넘길 때 (갈래1) 붙여야 할 라벨이 더 있는가.

## §5. 첨부 (커밋 8f76b912d · sha256)

```
db/properties/wad_aprime_pilot_prereg_v5_amendment_3_vasp_v5_2026_09_27.json  00202e38e5404f0667a0f70cf9b780444ec7103f77d47b221aca9525b82dc587
db/inputs/wad_aprime_v5_vasp_2026_09_27/jobs.json                             9c3a065666477ef63d126e6bd36a21c533b6df32eba6b99ef62a4343ac545f83
db/inputs/wad_aprime_v5_vasp_2026_09_27/MANIFEST.sha256                       ae434e671ba74ef5851d5826a9672ee85eb56f69ecf3a27d0f6859e92ee188b9
db/inputs/wad_aprime_v5_vasp_2026_09_27/run_all.sh                            86d88a3841295025b22f7a3b57792354dcb2be901fcdf58620096cba9343c924
db/inputs/wad_aprime_v5_vasp_2026_09_27/README.md                             78954a0e266884a68e17009f4f8e35ddac6171005dd0b7c06f15c92829938ab9
tools/wad/build_v5_vasp_package.py                                            7ed62ccd527f75af2949b9f3bd098f06b3c1580a2b30f8e7b54a2a4dd72fb818
db/properties/wad_aprime_s3v2_seal_2026_09_26.json                            8862a8e97d007361ee778ff0b643abea870701caabc1429d89c90c20f8b268c2
db/properties/wad_aprime_pilot_prereg_v5_2026_09_25.json                      3d35dfb9e8fbcbc79c757fe9205fa78437f8e250d9c16522ac14f5ef1f2f0059
```

같이 보면 좋은 것: `db/inputs/wad_aprime_v5_vasp_2026_09_27/jobs/V5_s_outer_A_bound/` (INCAR · INCAR.r1 · KPOINTS · POSCAR · POTCAR.spec) · 결정 `D-2026-09-27-wad-aprime-v5-vasp-route` (proposed) · V2 결과 `db/properties/wad_aprime_pilot_result_v2_2026_09_26.json` · V2 ATM 열 `db/raw/wad_aprime_s4_v2s2_2026_09_26/d3_atm_column_2026_09_27.json` · 게이트 읽기 정오 `db/properties/wad_aprime_gate_reading_erratum_2026_09_27.json`.

## §6. 회신 형식

판정 (GO / 조건부 GO / NO-GO) → **보내기 전 필수 수정** (P0 · P1, 재현 가능한 근거와 함께) → 권고 (선택) → Q7 의 3b · 3c 에 대한 명시 의견 (결과 전 개정으로 넣어도 되는지).
