# Track-B — DEM/MPM → COMSOL 파이프라인 (payload → comsol_pkg → .mph)

작성 2026-08-05.  상태: **v1 골격 완성** (커밋 f7c481ac; 7-agent 병렬빌드 + 3렌즈 적대리뷰
11건 반영 + max-effort 심화리뷰 진행 중).  태스크 #51.

---

## 0. 한 줄 정의

> **COMSOL 의 추측 입력(ε·τ·a_s·σ)을 우리 입자-해상 시뮬의 측정 입력으로 바꿔주는
> 상류(upstream) 파라미터화 엔진** + 그 측정값으로 즉시 열리는 하이브리드 기하 모델.

경쟁이 아니라 먹이사슬이다: 교수님 그룹은 익숙한 COMSOL 로 셀-스케일을 돌리되 입력이
방어 가능해지고, 우리 132-케이스 코퍼스는 랩 인프라로 승격된다.

역할분담 (2026-08-05 사용자 확정):
- **우리**: 미세구조 해상 물리 — σ 삼중, coverage, τ, per-particle 전류, 열화 궤적, 다압력.
- **COMSOL**: 셀/스택 스케일 + 우리 약점 2개의 검증 — ① 고 CAM field spreading
  (Bazzoun: RNM 이 f_CAM 75-80 % 에서 과소예측), ② VGCF 단면적 정확화 (1D Edge).

---

## 1. 아키텍처

```
STEP1 DEM → STEP2 MPM(킷 run_mpm.sh)
              └ mpm_webapp_payload.py  ──→  payload + step3.trackb        [배선 완료]
                                              φ_full · τ_full(선형관례) · mixed 가드
                                              τ_geo(AM-여집합 이상화, 크롭 솔브)
                                              kdom_ratio · κ_dom · per_particle face-walk
              scripts/comsol_export.py --kit <킷> --out <pkg>             [완료 29/29]
                                        └──→  comsol_pkg/ (스키마 v1.0, 9파일)
              scripts/build_comsol_mph.py <pkg>                           [완료 20/20]
                                        └──→  model_build.java + README_run.md
   (COMSOL 라이선스 머신)  comsol batch -inputfile model_build.java -outputfile case.mph
                           또는  python build_comsol_mph.py <pkg> --mph   (MPh 런타임)
```

## 2. 물리 설계 결정 (변경 금지 — 2026-08-05 확정)

| 구성 | 표현 | 근거 |
|---|---|---|
| AM 구 (457~2k) | **해상 기하** (Sphere + form UNION) | 반응 사이트·per-particle 물리의 주체 |
| AM-AM 넥 | **DEM δ 그대로** → UNION 렌즈 = Hertz 탄성 넥 | NCM 140 GPa ≫ SE 1.35 → 소성 conforming 은 SE 현상.  Stage-E 소성면적은 TODO 옵션 |
| SE | **연속체** κ_dom | 3.3만~8.2만 구 해상 불가·불필요 |
| VGCF | **1D Edge** (중심선 + 단면 π(75nm)²) | 해상 시 2.4억 tet.  1D 는 단면 **정확** = 우리 복셀 ~3× 과대의 해소 |
| PTFE | **기하 넣지 않음** | 차단 효과가 κ_dom(τ 에 solid 반영)·f_cov(face-walk 가 개재를 봄)·σ_e 에 이미 계량 |
| 전해질 물리 | **single-ion** (t⁺≈1) | 일반 리튬이온/DFN 인터페이스 금지 — 가짜 확산분극 생성 |

### κ_dom 이중계상 가드 (이 파이프라인의 지적 핵심)
하이브리드는 AM 구를 기하로 해상하므로 **AM-장애물 굴곡도는 모델이 스스로 만든다.**
측정 τ_full 을 SE 도메인에 그대로 먹이면 AM 몫이 두 번 걸린다.
```
κ_dom / σ_bulk = (φ_full/τ_full) / (φ_geo/τ_geo)
```
τ_geo = "AM 여집합을 꽉 찬 SE 로 이상화" 한 같은 복셀 Laplace 해 (payload 가 추가 솔브 1회).
재현 항등식 `κ_dom·(φ_geo/τ_geo) = σ_bulk·(φ_full/τ_full)` 이 selftest 로 고정돼 있다.

### τ 관례 (지뢰)
**선형**: σ_eff = σ_bulk·φ/τ.  `build_tau_regime_db` 의 √ 는 **τ² 관례** — 같은 해가
τ=4 ↔ 2 로 갈린다.  Track-B 산출물은 전부 `step3_sigma.tau_from_solve` (선형) 경유,
모든 json 에 관례 문자열 동봉.

---

## 3. comsol_pkg 스키마 v1.0

```
comsol_pkg_<case>/
  manifest.json      schema_version·case·source(mpm|dem_stageE)·tau_convention·files·git·notes
  am_spheres.csv     id,x,y,z,r[µm],cls,σ_e[S/cm],f_cov_reaction/carbon/block,f_cov_source
  am_am_contacts.csv i,j,δ[µm],a_hertz[µm],g_holm[S]   (Hertz a=√(R*δ), Holm g=2σ_c·a)
  vgcf_fibres.csv    fibre_id,seq,x,y,z  (Ø0.15µm, σ100 S/cm; 부재 시 헤더만+사유)
  se_domain.json     σ_bulk_ion·κ_dom(S/cm·S/m 병기)·kdom_ratio·τ_full/τ_geo·φ_full/φ_geo·
                     porosity(+관례 라벨)·mixed_phase·reason  (§F1: 의도적 null 보존)
  electrochem.json   i0·α·D_s·c_max·x0/x100·ASR·R_int·T_C — 없는 값 null + provenance.reason
  ocp_*.csv          (킷 anchor pack 에서 복사)
  conventions.md     단위(×100 S/m)·τ 선형+√함정·single-ion 경고·a_s Hertz/Tabor 밴드·
                     제작압 갇힘·I_1C TODO
  provenance.json    git commit·입력 md5·UTC  (★ 산출물이 자기 출처를 말한다 — SE 곡선
                     sub/frames 소실 사고의 처방)
```

## 4. 구성요소 상태

| 파일 | 역할 | selftest | 비고 |
|---|---|---|---|
| step3_sigma.py 헬퍼 3종 | τ 선형·κ_dom·face-walk | --selftest-trackb 14/14 | 02f31aca |
| mpm_webapp_payload.py trackb | 측정값 생산 | ast·--selftest-temperature 회귀 | additive, --no-trackb |
| comsol_export.py | pkg 생성 | 29/29 | §F1 null 보존 수정 반영 |
| build_comsol_mph.py | java+README 생성 | 20/20 | reason 전달 E2E 실증 |
| E2E (합성킷→pkg→java) | 관통 | PASS | 스키마 교차대조 정합 |

리뷰 반영 요지 (1차 11건): τ_geo **크롭 솔브** (패딩 캡이 도전층으로 남아 박형 +10-12 %
편향 — 합성 실측) · §F1 sigma_bulk **의도적 null 보존** (mixed 이온상 자기모순 패키지 차단) ·
provenance.reason 서브딕트 **전달** (java TODO 가 사유를 잃던 것) 외 8건.

---

## 5. ★ "이 mesh, repair 없이 들어가나?" — 판정 (real_14 실측 기반)

**결론: 그냥은 안 들어간다.  다만 이유가 통념(STL repair)과 다르고, 해법이 이미 손안에 있다.**

### 경로별 판정

| 경로 | repair 필요? | 실태 |
|---|---|---|
| **① Track-B java (Sphere+UNION)** — 본선 | **import-repair 자체가 없음** (네이티브 CAD) | 대신 아래 2개 기하 병리 |
| ② viz_mpm_continuum **NASTRAN** (hex 볼륨메시) | **불필요** — 메시로 직수입, domain 태그 유지 | 단 "geometry 없음": 재메싱·불리언·Ball 선택 불가 → B1 σ 대조엔 가능, BV 경계조작엔 부적합 |
| ③ viz_mpm_continuum OBJ/**STL** (표면 2.5M tri) | **사실상 필수** — 표면→솔리드 변환에서 repair/simplify | 사용 비권장 (③은 시각화/타 도구용) |

### ①의 두 병리 (real_14, 457구, rasterize 규약 gap≤0.10µm — 2026-08-05 실측)

**병리 A — sliver 렌즈**: 겹침 접촉 587개, δ 0.2~711 nm (중앙 70 nm).
렌즈 반각 0.4°~29.4° (중앙 7.8°), **반각 <5° 가 161개** — UNION 이 만드는 예리한 이음새가
메셔의 고전적 실패 지점.  → COMSOL geometry finalize 의 상대 repair tolerance 로 대부분
흡수 가능 (기본값이 δ_min 0.2 nm 를 삼킬 수 있음 — 그건 그 접촉의 소멸이므로 확인 필요).

**병리 B — 칼날 틈 (더 심각)**: **근접-비접촉 72쌍** (gap 0.1~95 nm).
- 메시: SE 도메인에 두께 ~0.1 nm~ 의 칼날 틈 → 요소 aspect ~10³⁻⁴:1 → 메시 폭발/실패.
- ★ **물리 불일치가 더 큰 문제**: 이 72쌍은 rasterize 가 1.2·vox 브릿지로 **전기적으로
  연결**하는 접촉들이다 (DEM econn 규약 gap≤0.10µm = 접촉).  매끈 java 기하에선 **개회로**
  — B1 σ_e 대조가 시작부터 다른 회로를 비교하게 된다.

### 처방 (TODO(trackb) 등록)

1. **브릿지 실린더** (표준 DEM→FEM 관행, 권장): 659 접촉 전부에 반지름
   `max(a_hertz, a_floor)` 실린더를 UNION.  `a_floor ≈ 1.2·vox 상당 (~0.15-0.2 µm)` 로
   잡으면 **STEP3 rasterize 브릿지 규약과 정합** — 두 모델이 같은 회로를 보게 된다.
   am_am_contacts.csv 가 a_hertz 를 이미 실으므로 생성기 쪽 루프 하나.
2. repair tolerance 명시 설정 + "δ<tol 접촉 소멸 검사" 를 README 디버깅 절에.
3. (기각) 반지름 일괄 팽창 — AM_S +2.5 % 반지름 = 부피 +7.7 %, porosity 를 깨므로 안 씀.

---

## 6. B1 비교가능성 주의 (심화 리뷰 진행 중 — 결과로 갱신 예정)

java σ_eff ↔ STEP3 대조가 B1 인데, 순수 field-spreading 차이만 남기려면:
- **collector 규약**: STEP3 전자 솔브는 per-column crown 접촉(밴드) — java 가 바닥 전면
  Dirichlet 이면 그 차이가 섞인다.
- **측벽**: 킷 --periodic ↔ java Block 절연벽.  주기 미구현이면 절연-벽 STEP3 런과만 비교.
- **온도**: --temp-c 킷은 trackb σ_bulk 가 이미 T-스케일 — COMSOL 에서 Arrhenius 재적용
  금지 (이중적용).
- **브릿지**: §5-B — 72 개회로를 닫기 전의 σ_e 대조는 무효.

---

## 7. TODO 전체 (코드 내 `TODO(trackb):` 주석과 1:1)

| # | 항목 | 위치 | 상태 |
|---|---|---|---|
| T1 | 실킷 1회 스모크 (trackb 성공경로) | 다음 킷 런 자동 | 대기 |
| T2 | **브릿지 실린더** (72 개회로 + sliver 완화, a_floor=1.2vox 정합) | build_comsol_mph | **신규·우선** |
| T3 | COMSOL 첫 batch 왕복 — feature 명 확정 (fin/setSolveFor/BallSelection/InterpolationCurve) | 라이선스 머신 | 대기 |
| T4 | B1 판정: java σ_eff ↔ STEP3 (comparability §6 통제 후) | README §4 표 | 대기 |
| T5 | B2 BV 결합 (f_cov 파라미터·경계선택 준비됨, i0 앵커 선행) | build_comsol_mph | 대기 |
| T6 | OCP csv → java Interpolation 함수 굽기 | build_comsol_mph | 대기 |
| T7 | Stage-E 소성-넥 옵션 (Tabor 면적 밴드 병기) | comsol_export | 대기 |
| T8 | VGCF --save-fibre npy 자동 인식 | comsol_export | 대기 |
| T9 | mixed 이온상(SDCP) σ_bulk 환원 규약 (현재 §F1 null 이 정직) | payload+export+mph 합의 | 대기 |
| T10 | I_1C 규약 문서화 → electrochem 전류값 | conventions §6 | 대기 |
| T11 | 고립 AM 클러스터 특이계 (퍼콜 라벨로 ec 제외 or 미소 컨덕턴스) | build_comsol_mph | 대기 |
| T12 | 스키마 v1.1: f_cov_source 에 absent_placeholder / sigma_bulk_source 문서화 | 스키마 | 대기 |
| T13 | 심화리뷰 findings 반영 (진행 중 wf_bab2ae8f) | 전체 | 진행 |
| T14 | 교수님 회신 1페이지 (§5 판정 포함) | 문서 | 대기 |

## 8. 함정 대장 (한 줄씩)

`.mph 는 COMSOL 없이 생성 불가(우리 산출물=생성기+데이터)` · `single-ion — DFN 금지` ·
`τ 선형 관례만` · `파라미터는 제작압 P 에 갇힘(P 바꾸면 새 pkg)` · `porosity 관례 페어링 금지
(union↔eps_sphere)` · `κ_dom 은 z-유효전도 스칼라 캘리브레이션 — 국소장 이방성은 미보증` ·
`컨테이너 롤백 5회 — 증분 즉시 푸시`.
