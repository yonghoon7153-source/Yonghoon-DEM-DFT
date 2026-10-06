# 우리 트리 재현 — Codex Rint G2 v3 재검토 탐침 (2026-10-07)

- **결론: 판정값 차이 0.**  `evidence_v3.json` 숫자 키 194 중 **192** 비트 동일 · `evidence.json` 97 중 **92** 비트 동일 — 다른 7 개는 LAPACK `lstsq` 끝자리 2 (annulus 맞춤 · 상대 9e−16) + 반복 풀이 (CG) 끝자리 5 (`actual_raster_order` · 10-06 재현 때와 **같은 우리 값**) · 문자열 차이 = 환경 3 칸 (python · numpy · scipy) 뿐 · 두 탐침의 내부 단언 (승자 집합 · 3170/3171 · β 역산 · 정규화 응답) 전부 통과 (rc 0).
- 환경: Linux · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · OMP/OPENBLAS/MKL 스레드 1 (Codex = Windows · 3.12.14 · 2.3.5 · 1.16.3).  솔버 경로 = CPU Jacobi-CG (`probe_prior.py` 의 작은 합성 `solve_sigma_z` 하나뿐).
- 소스: 우리 HEAD `2802c649e` (깨끗한 작업 트리) — 근거 9 파일의 blob = 핀 `c3ff4408c` (9/9 · `run_summary.json` 의 `worktree_blobs`) → 탐침 자신의 blob 단언이 그대로 통과한다.  ⚠ 이 반입 커밋은 v3 머리 줄 (L3) 에 v3.1 포인터를 넣어 v3 blob 이 바뀐다 → 이 커밋 뒤에 다시 돌릴 때는 아래 "다시 돌리는 법" 처럼 **핀의 9 파일**로 돌린다 (그렇게 돌린 결과 = 아래 표와 바이트 같음 · 확인함).

## 실행 셋 — `run_repro.py` (탐침 바이트 그대로 · `python3 -I -B` · 빈 cwd · 리포 밖 폴더)

| 실행 | source/ | rc (probe_v3 · probe_prior) | 결과 |
|---|---|---|---|
| checkout | 리포 루트로 심볼릭 링크 — 우리 체크아웃 (`step3_sigma` 를 리포 `scripts/` 에서 import) | 0 · 0 | 이 폴더의 `evidence_v3.json` · `evidence.json` |
| headcopy | 근거 9 파일만 복사 (Codex 와 같은 배치) | 0 · 0 | checkout 과 두 JSON 바이트 같음 |
| negctl (음성 대조) | headcopy + v3 초안 사본 끝에 1 바이트 | 1 · 1 | 첫 단계 `AssertionError` — blob `808ae4f6acda45e165f4c869e8fc3c2edb7a653a` ≠ manifest `21558d722d0139556b4dc6d19ed8966a466d22ea` · evidence 안 씀 (탐침의 blob 검사가 바뀐 파일 하나를 실제로 잡는다) |

- 탐침이 쓴 파일 = 각 폴더의 evidence JSON 둘뿐 (실행 전후 목록 대조 · `run_summary.json` 의 `new_files` · `changed_files`) · stdout = 그 JSON 과 바이트 같음 · stderr 0 B (negctl 빼고) · 리포 작업 트리 변경 0 (`-B` · pycache 없음).
- 핀 9 파일 (`git archive c3ff4408c …`) 로 다시 돌린 판 = checkout 판과 두 JSON · `run_summary.json` 바이트 같음.

## 핵심 값 — Codex ↔ 우리 (checkout 판)

### `RINTV3-01` (원장 `RINTV-01`) — `epsilon_tie`

| 양 | Codex | 우리 |
|---|---|---|
| power [µm²] (관측점 (0,0,0)) | −0.9999985000000001 · −0.9999992499999999 · −1.0000000000000009 | 같음 |
| 쌍 비교 (`pair_winners`) | 0 > 1 · 1 > 2 · 2 > 0 | 같음 |
| 순차 fold 승자 (입력 순서) | 012→2 · 021→1 · 102→2 · 120→0 · 201→1 · 210→0 | 같음 |
| 집합 규칙 띠 T · 승자 | {1, 2} · 6 순열 모두 1 | 같음 |
| 동심 반경 1 · 1.0000002499999687 µm 의 power 차 | 4.999999998478444e−07 µm² (ε 1e−6 안) | 같음 |

### `RINTV3-02` (원장 `RINTV-02`) — `fixed_bridge_AM_mask_permutation`

| 양 | 순서 [0,1] | 순서 [1,0] | Codex ↔ 우리 |
|---|---:|---:|---|
| 브리지 중심 x [µm] | 1.62077720467908 | 1.6207772046790803 | 같음 |
| 브리지 중심 y [µm] | 1.482184199398439 | 1.4821841993984393 | 같음 |
| 셀 (15,15,15) 거리²/h² (비교 5.76) | 5.760000000000001 | 5.759999999999995 | 같음 |
| 그 셀 sid | 0 | 2 | 같음 |
| AM 마스크 셀 수 | 3170 | 3171 | 같음 |

- 탐색 판 `legacy_AM_mask_permutation`: 시도 315 · bridge 0.2399999999999998 · 3170/3171 — 같음.
- 입자 중심 (탐침이 찾은 ulp 이동 뒤): c0 x 1.9748831001799223 · c1 x 1.061199006405326 — 같음.

### `RINTV3-03` (원장 `RINTV-03`) · R6 — `sphere_bc`

| 양 | Codex | 우리 |
|---|---|---|
| β_true · 막 삭제 β | −0.03125000000000001 · 0.75 | 같음 |
| 북극 경계값 (정답 = 막 삭제 오답) | −5.001250000000001 | 같음 |
| 오답 바깥 해 A · B | 1.006287726358149 · 0.7547157947686116 | 같음 |
| 경계 입력에서 역산한 β | −0.03125000000001043 | 같음 |
| annulus (R 2 · 3 · 4) 2 모수 맞춤 A · B | 1.0062877263581487 · 0.7547157947686128 | A 같음 · B 0.7547157947686122 |
| 그 맞춤의 B/(A a³) | 0.7500000000000013 | 0.7500000000000007 |
| R = 2 전위 정답 · 오답 | −2.0078125 · −1.8238965040241448 | 같음 |
| k_eff/k_m (f 0.008) | 0.9992501874531367 | 같음 |
| q_num · q_analytic | −0.09372656835791857 · −0.09372656835791054 | 같음 |
| l ≥ 2 정확 계수 | 0.0 | 같음 |

### R4 탄소 우회 — `carbon_bypass`

| 회로 | Codex | 우리 |
|---|---|---|
| 2 Ω 막 ∥ 0.02 Ω 탄소 | 0.019801980198019802 Ω | 같음 |
| 1 Ω 막 ∥ 0.02 Ω 탄소 | 0.0196078431372549 Ω | 같음 |
| 막 0 + 0.02 Ω 탄소 | 0.02 Ω | 같음 |
| 탄소 전류 몫 · 막 로그 민감도 (2 Ω 판) | 0.9900990099009901 · 0.009900990099009901 | 같음 |

### R5 E4 · 직전 반례 — `evidence.json`

| 양 | Codex | 우리 |
|---|---|---|
| `interface_face_g` 실측 = g_code | 0.00032679738562091506 | 같음 |
| v2 문서식 몫 · 올바른 몫 · 중심 로그 FD | 0.0334640522875817 · 0.8366013071895424 · 0.8366013071636756 | 같음 |
| 올바른 / 문서식 | 24.999999999999996 | 같음 |
| 직렬 bulk 3 · A 1 · B 2 Ω — 전체 로그비 · A 만 적분 | −0.6931471805599453 · −0.23104906018664842 | 같음 |
| 리드 포함 면 G | 0.00999999000001 S | 같음 |
| J2 경계 올바름 · 문자식 (거리 2.12 µm) | 2.075 · 2.15 µm (접촉 아님 · 문자식 접촉) | 같음 |
| 희석 차/f (L/a 5 → 80) | 2.357308057291521 → 2.3437532901766644 | 같음 |
| support smearing P_true/G · P_spread/G · 차 | 1.0796000000000001 · 1.2304 · 0.13968136346795101 | 같음 |
| raster 순서 — 바뀐 sid 셀 · cg_info · unconverged | 16 · 0 · False (두 팔) | 같음 |
| raster 순서 — σ_OFF [0,1] · [1,0] [S/cm] | 0.0017728521965377632 · 0.0018568975000462676 | 0.0017728521965377382 · 0.001856897500046274 |
| raster 순서 — σ 상대 변화 | 0.04740683045808214 | 0.04740683045810057 |

### Codex 와 다른 숫자 키 — 전부 (7)

| 파일 · 키 | Codex | 우리 | 상대차 |
|---|---:|---:|---:|
| v3 `sphere_bc.annulus_fit_B` | 0.7547157947686128 | 0.7547157947686122 | 8.8e−16 |
| v3 `sphere_bc.beta_from_independent_two_parameter_annulus_fit` | 0.7500000000000013 | 0.7500000000000007 | 8.9e−16 |
| prior `actual_raster_order.rows[0].sigma_eff_S_cm` | 0.0017728521965377632 | 0.0017728521965377382 | 1.4e−14 |
| prior `actual_raster_order.rows[1].sigma_eff_S_cm` | 0.0018568975000462676 | 0.001856897500046274 | 3.5e−15 |
| prior `actual_raster_order.relative_sigma_change` | 0.04740683045808214 | 0.04740683045810057 | 3.9e−13 |
| prior `actual_raster_order.rows[0].resid` | 9.929196490428454e−09 | 9.945726403974921e−09 | 1.7e−3 |
| prior `actual_raster_order.rows[1].resid` | 9.801807272078137e−09 | 9.828538600982548e−09 | 2.7e−3 |

- CG 다섯은 10-06 재현 (`docs/reviews/codex_rint_g2_design_review_evidence_20261006/_README_reproduction.md`) 의 우리 값과 끝자리까지 같다 — `probe_prior.py` 는 10-06 의 `probe_design.py` 와 바이트 같은 탐침이다.  두 팔 모두 잔차 < rtol 1e−8 · 판정값 (+4.740683 %) 은 유효 11 자리까지 같다.

## 독립 대조 — 판정문에 **인쇄된** 소수 그대로 (`independent_check.py` · 탐침 밖)

입력 = 판정문 §2 표 · §3 코드 블록 · §5 표 · §7 의 소수 리터럴.  §3 은 우리 체크아웃의 `rasterize` 를 직접 부른다 (탐침의 탐색 · ulp 이동을 거치지 않는다).  출력 = `independent_check.json`.

| 항목 | 결과 |
|---|---|
| RINTV3-01 | 쌍 비교 0 > 1 · 1 > 2 · 2 > 0 · fold 승자 012→2 · 021→1 · 102→2 · 120→0 · 201→1 · 210→0 · 집합 규칙 T {1, 2} → 1 (6/6) · 동심 power 차 4.999999998478444e−07 µm² (ε 안) · **중심만 키로 쓰면 동심 쌍의 승자를 입력 순서가 정한다** (01 → 0 · 10 → 1) |
| RINTV3-02 | 판정문 리터럴 c0 · c1 · r 로 `rasterize` 두 순서 → 판정문 표와 같음 (브리지 중심 · 거리² · sid 0 ↔ 2 · 3170 ↔ 3171 · 셀 중심 (1.55, 1.55, 1.55) µm) · 그 밖 sid1 618 · 618 · sid2 2552 ↔ 2553 (바뀐 셀 = 혼합 쌍 브리지 = AM_P sid 2) |
| RINTV3-03 | β −0.03125 · f = (1/5)³ → k_eff/k_m 0.9992501874531367 · q_num −0.09372656835791857 (판정문과 같음) · q_analytic −0.09372656835791052 (판정문 …054 — 판정문은 식으로 계산한 β −0.03125000000000001 을 씀 · 끝자리) · q 에서 다시 만든 β = q/(3 + qf) = −0.031250000000002685 · 섞어 짝지은 비교 β − q_analytic = 0.06247656835791052 (정상해가 실패) · q_num − q_analytic = −8.0e−15 (정확한 식을 float64 로 계산만 해도 생기는 차 — 1/f = 125 배 증폭의 최소 예 · 우리 산술) |
| R4 | 탄소 우회 회로 셋 · 몫 둘 = Codex 와 같음 |

## 다시 돌리는 법

⚠ 이 폴더나 상위 증거 폴더에서 탐침을 직접 돌리지 말 것 — 탐침은 자기 옆 evidence JSON 을 덮어쓰고 (Codex 원본이 사라진다) `source/` 가 없어 import 도 실패한다.

```bash
# 리포 루트에서.  PIN = Codex 핀 · 근거 9 파일은 핀에서 꺼낸다 (이 커밋부터 v3 L3 가 핀과 다르다).
E=docs/reviews/codex_rint_g2_v3_review_evidence_20261007
PIN=c3ff4408c
SRC=$(mktemp -d); RUN=$(mktemp -d); CWD=$(mktemp -d)
FILES=$(python3 -I -B -c 'import json,sys; print(" ".join(r["path"] for r in json.load(open(sys.argv[1]))["files"]))' "$E/source_manifest.json")
git archive --format=tar -o "$SRC.tar" "$PIN" $FILES && tar -xf "$SRC.tar" -C "$SRC"
python3 -I -B "$E/_reproduction_ours/run_repro.py" "$E" "$SRC" "$RUN/runs" "$CWD"     # checkout · headcopy · negctl
python3 -I -B "$E/_reproduction_ours/compare_ev.py" "$E/evidence_v3.json" "$RUN/runs/checkout/evidence_v3.json" v3
python3 -I -B "$E/_reproduction_ours/compare_ev.py" "$E/evidence.json" "$RUN/runs/checkout/evidence.json" prior
python3 -I -B "$E/_reproduction_ours/independent_check.py" "$PWD" "$RUN/independent_check.json"
```

- `run_repro.py` 가 스레드 1 환경을 직접 건다 · 탐침은 `"$RUN/runs/<판>/"` 안의 사본만 돈다.
- 우리 체크아웃 자체로 돌리려면 `"$SRC"` 대신 리포 루트 (`"$PWD"`) — 근거 9 파일이 핀과 같은 커밋에서만 checkout · headcopy 가 통과한다 (다르면 negctl 처럼 blob `AssertionError` = 정상 동작).

## 한정 (Codex 그대로)

- 탐침 = 합성 입력 · 해석식 + 고정 소스의 실제 함수 (`rasterize` · `interface_face_g` · `solve_sigma_z` · `intersection_disc_area`) 의 소규모 검사다 — **v3 · v3.1 owner · CNC · RRM 구현의 시험이 아니다** (구현이 아직 없다).  rc 0 = 리뷰 반례의 재현 성공이지 생산 구현 PASS 가 아니다.
- 실침대 순서 의존 · CNC 편향의 생산 크기 · 섬유/SE 구현 · 물성 출처는 이 재현이 보증하지 않는다.
- `independent_check.py` 는 우리 산술 + `rasterize` 한 번 호출이다 — 새 owner 구현의 시험이 아니다.
