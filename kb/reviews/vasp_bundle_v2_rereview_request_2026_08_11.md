---
title: "Codex 재검토 요청 — VASP 번들 v2 (HOLD 10항 반영 완료 · 발송 GO/NO-GO)"
tags: [review/codex, sdcp, vasp, dft+u, handoff, v2]
date: 2026-08-11
status: 회신 대기 (GO/NO-GO)
대상: tools/sdcp/vasp_handoff_bundle.py @ 69ca2244 (첨부)
선행: kb/reviews/vasp_bundle_codex_reply_2026_08_11.md (HOLD 접수분)
---

# 요청

지난 회신의 **발송 재개 조건 10항을 전건 반영**했다. 이번 요청은 두 가지다:
① 아래 대응표·산출물 검수 → **발송 GO/NO-GO** 판정
② §2 의 **계보 사실관계 정정**(당신이 인용한 파일이 repo 에 없다)에 대한 확인

첨부: `vasp_handoff_bundle.py` (생성기 + 내장 analyze_results.py, commit 69ca2244).
아래 INCAR/KPOINTS 블록은 **selftest 가 실제로 산출한 파일 원문**이다 (합성 슬랩이라
MAGMOM 길이만 짧고, 템플릿·값은 실물과 동일).

---

# §1. 10항 대응표

| # | 재개 조건 | 반영 | 근거 위치 |
|---|---|---|---|
| 1 | Ni_pv + canonical AFM seed 계보 | ✅ Ni_pv 고정 + **artifact 정본** seed (§2 — 사실관계 정정 있음) | `POTCAR_SPEC` · `seed_configs()` |
| 2 | tier1 전 끝점 2 magnetic seeds | ✅ `SEEDS_FULL=(afm2424_pm1, afm2424_net4)` — tier1 전 pose + clean. tier2 는 pm1 + 탐침쌍만 2종 (§4-Q2) | `build_bundle()` seeds 분기 |
| 3 | 2×3×1 relax + 3×4×1 final static | ✅ + 대표쌍/clean 에 4×6×1 dense 상. **판정 에너지는 static 만** | `KMESH` · 아래 산출물 |
| 4 | gas IDIPOL=4 · radical spin · 20/24 Å box | ✅ DIPOL=COM(frac 3성분) · NUPDOWN 1/0 · 상자 2종 + \|ΔE\|≤10 meV 게이트 | `_emit_mol_job()` · 분석기 `BOX_TOL` |
| 5 | geometry/bond/registry/magnetic audits | ✅ 공유반경 결합그래프(BOND_CHANGE) · 탈착(>4 Å) · 고정 drift(>0.1 Å) · 자유원자 힘(>0.05 eV/Å) · PAIR_MIGRATED · **PAIR_COLLAPSED**(두 끝점 같은 registry) · REGISTRY_UNVERIFIED | 분석기 `geometry_audit()` |
| 6 | planned matrix 완결성 hard gate | ✅ MANIFEST `planned{}` (required=tier1+refs) — 누락 시 **exit 2** + 목록 | 분석기 말미 |
| 7 | phase runner/restart/반송 아카이브 | ✅ `run_job.sh`(상 순차·CONTCAR/CHGCAR 승계·완료 스킵) + `run_all.sh` · 반송물 = relax/OUTCAR+CONTCAR + static/OUTCAR (.gz 허용) | `RUN_JOB` · README |
| 8 | full SHA-256/POTCAR/VASP provenance | ✅ 전체 sha256(64자) + TITEL 대조(일관변형 강등/혼합 치명) + vasp 버전 기록 | MANIFEST · 분석기 |
| 9 | negative-path selftest | ✅ **심은** migration / F-이탈(BOND_CHANGE) / seed 50 meV 불일치(BLOCKED_MAGNETIC) / 필수누락(exit 2) 전부 발동 확인 + 양성 ΔE/E_ads 복원 | `selftest()` 출력 |
| 10 | analyzer nonzero exit on failure | ✅ 필수 static 누락 → exit 2 (fail-closed) | 분석기 `required_missing` |

seed-매칭 ΔE(§4.3): 끝점별 독립 min **폐기** — `dE_by_seed[s] = E_Ni(s) − E_Li(s)`,
headline 은 pm1, \|ΔE_pm1 − ΔE_net4\| > 10 meV 면 `BLOCKED_MAGNETIC_SENSITIVITY` 로
쌍 제외. 잡 수 52 정정(내 58 은 오산 — 당신 계산이 맞았다).

---

# §2. ⚠ 계보 사실관계 정정 — 확인 요청

당신 회신의 §2.3/§11 은 canonical AFM 을 `tools/sdcp/ptfe_linio2_uma/vasp_stage.py` 의
`ni_afm_signs()` "12-Ni primitive pattern `[-,+,+,+,-,-,-,+,+,-,-,+]` ×4" 로 인용했다.

**그 파일은 이 repo 에 존재하지 않는다** (`find . -name vasp_stage.py` → 0건,
`runs/sdcp_phaseB_vasp_recheck_vendor_v2_2026_08_08/` 도 없음). 대신 **실제 2026-08-08
납품물**이 있고, 그것을 artifact 정본으로 확정했다:

`runs/sdcp_phaseB_vasp_v1_2026_08_08/slab/INCAR` (원문):
```
# QE 의 Ni1/Ni2 부격자 배정을 그대로 옮겼다. ...
MAGMOM = 0×48  −1×24  +1×24  0×(나머지)
```
즉 정본은 **블록형: Ni 앞 24개 −1 · 뒤 24개 +1 (±1 μB)** 이다. 당신이 제안한 이름
`qe_afm24_24_pm1` 이 가리키는 구조와 일치하므로 실질 충돌은 없다고 본다.
**확인 요청**: ① 12-패턴 인용의 출처가 우리 repo 밖(당신 쪽 작업본)인가?
② 블록형 24/24 를 정본으로 확정하는 데 이견 있나?

또 하나 — 실납품의 실제 프로토콜은 회신이 가정한 것보다 거칠었다:
**LASPH=F · LDIPOL=F · ISMEAR=1/σ0.2 · 단일점(NSW=0) · LREAL=Auto**.
그래서 v2 는 "Phase-B 연속" 이 아니라 **의도된 개선**이고, 차이를 MANIFEST 의
`protocol_delta_vs_phaseB` 에 명시했다 (승계: U 6.2 · IVDW 11 · ENCUT 520 · Ni_pv).
→ v2 결과와 Phase-B 단일점을 같은 표에 놓을 때 이 차이가 각주로 붙는다. 동의하나?

---

# §3. 실산출물 (selftest 가 만든 파일 원문)

## 슬랩 relax INCAR
```
SYSTEM = <pid> Li-top afm2424_pm1 [relax]
GGA=PE / PREC=Accurate / ENCUT=520 / ISMEAR=0 / SIGMA=0.05 / ALGO=Normal
NELM=200 / NELMIN=6 / ISPIN=2 / ISYM=0 / LASPH=.TRUE. / ADDGRID=.TRUE.
LORBIT=11 / AMIN=0.01 / IVDW=11 / NCORE=4
EDIFF=1E-5 / EDIFFG=-0.02 / IBRION=2 / NSW=200 / ISIF=2 / LREAL=Auto
LDIPOL=.TRUE. / IDIPOL=3 / DIPOL=0.5 0.5 <zcom_frac>
LDAU=.TRUE. / LDAUTYPE=2 / LDAUL=<Ni:2 else -1> / LDAUU=<Ni:6.2> / LDAUPRINT=2 / LMAXMIX=4
MAGMOM=<POSCAR 순서 재매핑 · 검산 내장>
LWAVE=.FALSE. / LCHARG=.TRUE.        ← static ICHARG=1 승계용
```

## 슬랩 static INCAR (판정 정본)
```
(공통부 동일)
EDIFF=1E-6 / IBRION=-1 / NSW=0 / LREAL=.FALSE.
LDIPOL=.TRUE. / IDIPOL=3 / DIPOL=0.5 0.5 <zcom_frac>
ISTART=0 / ICHARG=1 / LCHARG=.TRUE.
```
KPOINTS: relax `2 3 1` · static `3 4 1` · dense `4 6 1` (전부 Γ-centered).

## 기체상 static INCAR
```
(공통부 동일) EDIFF=1E-6 / IBRION=-1 / NSW=0 / LREAL=.FALSE.
LDIPOL=.TRUE. / IDIPOL=4 / DIPOL=<frac COM 3성분>
NUPDOWN=0 (closed) 또는 1 (doped radical · SO3 산소에 +1 μB seed 분배)
```
상자 2종: span+20 / span+24 Å, Γ-only. 분석기 게이트 \|E20−E24\| ≤ 10 meV.

## run_job.sh (상 순차)
```
relax → (CONTCAR·CHGCAR 승계) → static → [dense]
완료 상은 "General timing" 검사로 스킵 · POTCAR 부재 시 즉시 중단
```

## selftest 음성 경로 실행 결과 (원문 꼬리)
```
✔ N4 필수 누락 → exit 2 (fail-closed)
✔ N1 migration → PAIR_MIGRATED
✔ N2 F 이탈 → BOND_CHANGE
✔ N3 seed 50 meV 불일치 → BLOCKED_MAGNETIC_SENSITIVITY
✔ 양성 ΔE 복원 fib00 = 0.045 (심은 값 0.045)
✔ E_ads 복원 = -1.0 (기대 −1.0)
✔ 조각 판정 = NO_VERDICT_n<3 (유효 1/계획 4 → n<3 게이트가 선행)
✔ dense-k 민감도 게이트 통과 (3 meV 심음)
```

---

# §4. 좁은 재확인 질문 (GO/NO-GO 와 함께)

**Q1.** static 의 `ISTART=0 / ICHARG=1` — relax(2×3×1)의 CHGCAR 를 static(3×4×1)이
읽는다. k 가 바뀌므로 WAVECAR 승계 대신 이 경로를 택했다(당신 §2.2 그대로).
CHGCAR 용량 때문에 외주처가 생략하고 ICHARG=2 로 돌릴 위험이 있는데, run_job.sh 가
자동 복사하므로 막았다고 본다. 이견?

**Q2.** tier2(sdcp 2종)는 pm1 + 탐침쌍만 2종으로 남겼다 — tier1(판정 목적)과 달리
tier2 는 UMA 층에서도 미해결이라 DFT 비용을 아꼈다. 수용 가능한가, 아니면 tier2 도
전 끝점 2종이 필수인가? (tier2 전환 시 +22잡.)

**Q3.** `NELMIN=6` 을 relax 상에도 넣었다(당신 템플릿은 static 용이었다). relax 에서
과한가? (이온 스텝마다 최소 6 SCF — 비용 증가는 미미하다고 봤다.)

**Q4.** dense(4×6×1) 민감도를 **대표쌍 1개/조각 + clean** 에만 뒀다. 당신 §7 의
"representative Li/Ni pairs + clean at 4x6x1" 해석과 일치하나?

**Q5.** 분석기의 PAIR_COLLAPSED 를 "두 끝점의 최종 registry 동일" 로 구현했다
(periodic-RMSD basin 비교는 stdlib 범위 밖 — 수동 검토로 남김). 이 단순화의 위험?

**Q6.** 남은 것 중 **발송 전 필수**가 더 있나? 없으면 GO 를 달라 — gabia 에서
실데이터로 생성해 잡 수·자격쌍을 확정한 뒤 발송한다.

# 답 형식
§2 확인 2건 + Q1–Q6 각각 동의/수정/반박, 마지막에 **GO / NO-GO** 한 줄.
