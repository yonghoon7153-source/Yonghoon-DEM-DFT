# 취성 파괴 → MPM crack-void (초기압밀 균열의 형태적 결과)

**frame[5] 분업:** DEM Auerbach 분류가 **어디서(WHERE)** 균열이 개시하는지 계산하고,
MPM이 그 **형태적 결과(morphology)** — SE가 열린 균열공간으로 흘러들어 국소 공극/피복이
바뀌는 것 — 를 그린다.  A10/real_degrading 문서가 그은 경계(접촉-FACE = DEM 원장 /
AM-내부 crack morphology = MPM/FEM)에서, **AM-내부 절반을 켜는** 기능.

사용자 결정(2026-07-23): **심각도-게이트 구현** (기본 OFF, fragmentation+ 에서만 발동).

---

## 파이프라인

```
DEM 케이스(atoms.csv + contacts.csv)
   │  scripts/dem_fracture_scaffold.py  (AM–AM 접촉 Auerbach 분류 → per-AM 최악단계·F/P_c,
   │                                     am_scaffold 행에 위치-매칭[cKDTree])
   ▼
fracture-scaffold CSV  (am_scaffold + [worst_stage_rank 0..4, f_over_pc], 행-정렬)
   │  mpm3d_compaction.py --fracture-scaffold ... --fracture-min-stage fragmentation
   ▼
fragmentation+ AM 반경 감소  r×(1−v)^⅓  (crack-void → pin-mask↓ → SE ingress)
   ▼
MPM 압밀 → SE가 균열공간 채운 morphology (공극/피복 이동, dg_acc)
```

## 심각도 → crack-void 맵 (ASSUMED-FORM, 스윕-축)

| 단계 (rank) | 열린 부피 | crack-void v (기본) | 반경 인자 (1−v)^⅓ |
|---|---|---|---|
| intact(0)·microcrack(1)·multicrack(2) | ≈ 0 | **0** (near-null → 제외) | 1.0000 |
| fragmentation(3) | 중간 | `--fracture-void-frag` 0.15 | 0.9473 |
| pulverization(4) | 큼 | `--fracture-void-pulv` 0.35 | 0.8662 |

- **micro/multi crack이 제외되는 이유:** 열린 부피 ≈ 0 (표면 cone-crack, 부피 없음).  MPM
  morphology에 near-null → crack-void 맵과 `--fracture-min-stage` 선택지 모두 frag/pulv만.
  DEM 취성의 **전-스펙트럼**(micro 포함)은 여전히 **수송 보정 f_intact**(network solver,
  DEM축)가 담당한다.  두 축은 상보(frame[5]).
- v 값은 `--dv-pct-poly`(=A9 "입계균열이 부피 ~70% 내부흡수")와 같은 **ASSUMED-FORM 스윕
  파라미터** — 문헌앵커 대기.  radius-shrink 근사는 `--cycle-deform`과 동일 규약(정확한
  fragment-split 지오메트리는 v2 후보).

## ⚠ 이중계산 가드 (§guard)

DEM `f_intact`(σ 수송보정, network_conductivity)와 MPM crack-void는 **서로 다른 축**:
- `f_intact` → 깨진 접촉의 **전도도** 감소 (DEM 수송).
- crack-void → 균열의 **형태/공극** (MPM morphology).

둘을 **동시에** 켜면, MPM crack-void가 바꾼 구조 위에서 STEP3 σ를 다시 계산할 때 **frag/pulv**
파괴의 전도-영향이 **한 번 더** 실릴 수 있다(구조-경유 + f_intact).  현재 기본은 crack-void
OFF이므로 프로덕션 이중계산 없음.

★ 정정(리뷰 M3): "f_intact를 통째로 끄라"는 blunt 규약은 틀렸다 — crack-void는 **frag/pulv만**
표현하는데 f_intact는 **micro/multi까지** 담당하므로, f_intact를 통째로 끄면 micro/multi의
수송 열화가 **누락**(under-count)된다.  올바른 규약은 **단계별 분리**:
- **frag/pulv 접촉**: 형태(crack-void, STEP3 구조-경유)로 1회 계상 → 이 접촉엔 f_intact **재적용 금지**.
- **micro/multi 접촉**: crack-void가 표현 안 하므로 f_intact(수송)로 계상 **유지**.
즉 "crack-void가 소유한 frag/pulv에만 f_intact를 빼고, micro/multi f_intact는 남긴다."
구현은 f_intact를 stage로 분해(frag/pulv 몫 vs micro/multi 몫)해야 함 — GPU 실런 캘리브 후
확정(사용자 논의 대상).

## ⚠ 근사 한계 (리뷰 L2/L3)

- **질량 비보존 (L2):** `am_r×(1−v)^⅓`는 구의 **고체 부피**를 (1−v)배로 줄인다 = 활물질을
  삭제.  실제 파괴는 AM 질량 보존(파편이 퍼지고 그 **사이**에 void).  → 파괴 구조의 AM-분율/
  용량 readout은 물리보다 활물질을 덜 본다.  또 **비-se-dump(uniform-fill) 경로**에서는
  `se_target ∝ AM_vol`이라 AM 축소가 SE 주입을 **줄인다(역방향 — 균열공간엔 SE가 더 들어와야)**.
  → **`--se-dump` 경로 사용 권장**(se_target 무관, 실제 SE 위치로 seeding하므로 이 back-coupling
  회피).  정확한 fragment-split(질량보존 다-구 분할)은 v2 후보.
- **cycle-deform × fracture 조합 (L3):** 반경 인자는 곱해짐(`am_r·_fac·(1−v)^⅓`, math OK)이나,
  충전-**팽창**(cycle-deform poly)과 균열-**수축**을 같은 입자에 곱하면 서로 다른 기전을 한
  반경에 섞는 것 → 깨끗한 중첩 아님(물리적으로 모호).  조합은 허용하되 해석 주의.

## 정직한 한계 (현 SDCP 케이스 = near-null)

제시된 input_3.18mAh_SDCP: **0.59% microcrack, 전부 AM_S–AM_S, 열린 부피 ≈ 0** →
crack-void 게이트가 **아무것도 주입 안 함**(frag/pulv 0개).  이 기능이 실제로 무는 곳:
- **고압** (F/P_c 상승) + **poly-rich(AM_P, K_IC 0.3 = SC의 1/3, 2차입자 입계균열)**.
- stage-2 감사의 AM_P fragmentation 분기(F/P_c 15.96 while AM_S intact 95.7%)가 대표 케이스.

→ 이 기능은 **고압/poly 레짐 전용 심각도-게이트 capability**로 shipping; 프로덕션 bimodal
저-중압에서는 자동으로 near-null(무영향).

## 사용

```bash
# 1) DEM 케이스 → fracture-scaffold
python scripts/dem_fracture_scaffold.py --case-dir webapp/results/<cid> \
    --am-scaffold docs/data/real14_am_scaffold.csv --out real14_fracture.csv
# 2) MPM 압밀에 crack-void 주입 (fragmentation+ 만)
python scripts/mpm3d_compaction.py --am-scaffold docs/data/real14_am_scaffold.csv \
    --se-dump docs/data/real14_se_scaffold.csv --protocol hold \
    --fracture-scaffold real14_fracture.csv --fracture-min-stage fragmentation
```
`--fracture-scaffold` 미지정 = **bitwise 동일**(기본값 없음 §F1).  `--cycle-deform`과 조합
가능(반경 인자 곱).

## 검증
- `dem_fracture_scaffold.py --selftest`: 합성 pulverization 접촉 검출 + 위치매칭 + CSV 왕복 PASS.
- 게이트 math 단위검증: frag→×0.9473, pulv→×0.8662, min-stage 게이팅(frag=frag+pulv, pulv=pulv만),
  행-불일치 raise 확인.
- GPU 실런(고압/poly 케이스) + 3렌즈 적대리뷰 = 진행.
