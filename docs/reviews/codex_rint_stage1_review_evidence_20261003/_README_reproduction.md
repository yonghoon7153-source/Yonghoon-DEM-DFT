# Codex r_int ① 1단계 독립 리뷰 — 반입 + 우리 재현 (2026-10-03)

- 판정문: `docs/reviews/codex_review_rint_stage1_20261003.md` (= zip 의 `codex_review_rint_stage1_20261003.md` · 359 행 · sha256 `6365b178b786a39901046b25bd9e6c94b243600016d1f3b2ad46106f9fb777d5`) — **G1 HOLD · G2 HOLD** · P1 1 (`RINT-01` = 자기리뷰 P1-1 CONFIRMED) · P2 8 (`RINT-02`~`09`) · 기본 OFF scalar σ 의 새 P1 없음.  원장은 Q7 출처 정정 (`RINT-10`) · P3 열 (`RINT-11`~`20`) 을 더해 20 건.
- 반입 원본: 사용자 전달 zip `codex_rint_stage1_review_20261003.zip` — 1,248,729 B · sha256 `e035bd5847cb076484fed6241c23147a27cde84b590d038a3817fe72c817c405` · 105 파일 · `SHA256SUMS.json` 104/104 일치.
- 핀: 구현 `5e0efdb8d` · 문서/소비처 `62f9e4cb3` — `source_manifest.json` 의 23 파일 git blob 이 **우리 HEAD 와 23/23 같다** (반입 시점 HEAD `62f9e4cb3`).
- 이 폴더 = zip 에서 아래 39 개를 **뺀** 66 파일 + 우리 재현 기록 `_reproduction_compare_linux.json`.  뺀 것 (목록 · sha256 은 그 JSON 의 `excluded_from_repo`):
  `source/` 핀된 원본 23 (우리 파일 그대로) · zip 의 inputs 폴더 request 파일 (우리 요청서 사본 = `docs/reviews/codex_rint_stage1_request_20261003.md`) · 판정문 원본 (위 경로로 반입) · 합성 payload JSON 15 (`evidence_gates/payload_mutation/` 의 summary 외 9 · `compare_contract_*/` 6 · 각 ≈ 370 KB).
  ⇒ 재현은 **zip 원본**을 풀어 그 안에서 `python replay_review.py --full` (이 폴더만으로는 `source/` 가 없어 돌지 않는다).

## 우리 재현 — `replay_review.py --full` 무변경 (Linux · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · 풀어 놓은 사본에서)

| 대조 | 결과 |
|---|---|
| rc · 시간 | 0 · 61 s · 변이 PASS 두 개 (규칙 J 전체 · check_arm) = Codex 가 말한 거짓 초록 그대로 |
| 증거 JSON 27 개 (받은 것 ↔ 재현) | **결정값 차이 0** · 미분류 차이 0 — 차이는 전부 `classes` 분류 안 (환경 필드 · 합성 입력 해시 · CG 잔차 · 상대 ≤ 1e-12 · 0 근처 잔차 둘 · summary 상위집합) |
| 제공 탐침 · selftest stdout | `evidence_gates/reproduction_comparison.json` 재생성본이 받은 것과 같음 (차이 0) |

### 판정의 핵심 값 — 우리 재현에서 읽은 값 (손으로 옮기지 않고 재현 JSON · stdout 에서 뽑음)

| 원장 | 양 | 우리 재현 |
|---|---|---|
| `RINT-01` | pid 상속 가닥 (r=1e−4 Ω·cm²) | r = 0.0001 Ω·cm²: σ_e OFF 11.1111 → pid 상속 0.131752 (-98.81 %) · 원장 faces_by_pair = {'VGCF|VGCF': 2} · pid −1 이면 σ_e 11.1111 · 면 0 |
| `RINT-02` | 주 σ_e OFF / ON / 주 rint 삭제 변이 | 0.00104943322871775 / 0.001035212003644942 / 0.00104943322871775 (변이 = OFF 비트 동일: True) |
| `RINT-02` | wetted rint 만 삭제 → wetted σ · R_geom | 0.0009487 → 0.0009606 S/cm · 0.0 → 0.0544 Ω·cm² (주 σ_e 같음: True) |
| `RINT-03` | 입자별 AM 전류 대리량 (상속 / sid 마스크 배수) | 126.5602 · 120.9457 (탄소 20 셀 중 상속 8) |
| `RINT-04` | σ_eff ON · 계면 소산 몫 · Joule 지도 ON/OFF 최대 차 · hot_frac_50 | 0.0476190476 · 0.9523809539 · 2.03e-06 · 0.425 / 0.425 |
| `RINT-05` | reaction OFF 정규화 vs 막 기준해 · npz 에 rint | [1.0, 1.0] vs [0.1031390135, 1.8968609865] · False (키 10) |
| `RINT-06` | 같은 Σg_film 에서 σON/σOFF (pid 경계 / 접촉 중간면) | h 0.2: 0.6241260201 / 0.6474454905 · h 0.1: 0.6755034001 / 0.6999486508 · 단자 R 1 vs 1.6923076923 |
| `RINT-07` | R_j=100 Ω · 올바른 G / 초안 식 그대로 G | 0.009999990000010001 / 1e-10 S (저항 1e+08 배) |
| `RINT-08` | lead 1 + 접점 5 + lead 1 → R_j 재사용 시 | 7.0 → 9.0 Ω |
| `RINT-09` | 같은 막 1 Ω · baseline 1 / 10 Ω 의 Δlnσ | -0.6931471806 / -0.0953101798 |
| `RINT-19` | caller sid 오용 · pid 변경 뒤 | 계면 몫 0.95238 → 0.0 · |J|max 101.00× · pid 변경 뒤 저장 면 9 · 몫 0.0 |

## 한정 (Codex 그대로)

- 실침대 payload/원 격자가 없어 가짜 접점의 **실생산 빈도 · 오차 분포**는 미측정 · 실제 fid/SE-id 새 구현 · GPU 경로 · TauFactor 실행 · 문헌 재료값 채택은 범위 밖.
- 위 값은 합성 CPU 탐침이고 대리량이다 (입자별 전류는 함수 내부 |J_z| 대리량 — 실험 전류밀도로 인용 금지).
- 판정문 안의 `C:/Users/Administrator/Documents/Codex/…` 링크는 Codex 작업 폴더 경로다 (이 리포에 없다).
