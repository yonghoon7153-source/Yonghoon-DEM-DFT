# 우리 트리 재현 — Codex 접촉망 세대 2 수정 재검증 묶음 (2026-10-06)

판정문: `docs/reviews/codex_review_gen2_network_reverify_20261006.md` (핀 `165d0cf61` · HOLD · 기존 P1 G2R-01 닫힘 · 새 P1 없음 · 새 P2 G2RR-01 · 02 · 03).
이 폴더 (`docs/reviews/codex_gen2_network_reverify_evidence_20261006/`) = Codex 묶음의 판정문 밖 파일 281 개 (`docs/reviews/codex_gen2_network_reverify_evidence_20261006/bundle_manifest.json` 과 sha256 · 바이트 수 일치) + 이 재현 기록.
우리 재실행 산출물은 스크래치에만 두었다 (리포에 넣지 않음).

## 1. 받은 업로드 zip 9 개와 출처

| zip | bytes | sha256 | 이 묶음에서의 역할 |
|---|---:|---|---|
| a89e4386-verify_evidence.zip | 1,049,029 | 650be0bb5b0b72c62c7c1e7d4e0ea9c27e524551e5c786de7bcdd4f9dfc6af5f | 묶음 최상위 291 + bundle_manifest.json — 판정문 · README · 검증/재현 스크립트 · probes 5 · evidence 279.  **판정문과 이 폴더의 모든 Codex 파일은 이 zip 에서 왔다** |
| fbf35939-CLAUDE.zip | 2,015,842 | adae70342520645eb3d03d1127a9706bb3c9bb01ed78c842b37c77bf9d042596 | source/ — AGENTS.md · CLAUDE.md · scripts 54 · webapp 17 (73) |
| 36294139-area_contract_20260913.zip | 528,895 | 5610ab38f54573ffcb8d5f92eff0242ec657f6502aae9e0ec6b84be6d2f34093 | source/docs — area_contract_20260913.md · reviews 6 (7) |
| 68851d66-lhs_network194_11fcf91e8.zip | 23,905,783 | 6ddf511a4569e00907b755ec431ab7ad22526d4e7081da7652181d33013d9925 | source/docs/data — case15_corner 2 · gen2_design_20261006 74 · lhs_descriptors_cov_1e09f661d 131 · lhs_network194_11fcf91e8 17 (224) |
| 2f78ad1b-lhsx_handover_20261001.zip | 12,140,185 | c67fe6f3c9fb182fbb3c29392a07f8084e6b45dc3f8ca4af590b271a6dd1fda7 | source/docs/data — 인계표 lhs · lhsx · lhs_design · census · perc_audit 2 · union · webapp_contact 2 · real14 덤프 2 (11) |
| 601f9925-probes.zip | 148,971 | cb4b4858925d671a736a97e0b874e4cd385d4d6ba88179d669803cdb262c3cb5 | **이 묶음 아님** (아래) |
| c560a20e-AGENTS.zip | 1,149,831 | 7e67e3e4bcb87c35c30bd1effdc000534845775f3d42798dc22990b2e3f8186d | **이 묶음 아님** |
| 6059d114-reviews.zip | 12,181,674 | aac90e7e5622a4bce25304302f79a902b81d5f0bf6714fedba2908a4fcd8452c | **이 묶음 아님** |
| 2a9b253c-gen2_design_20261006.zip | 21,199,743 | faffee17f14028a283d272ad3e8e36641c6a77cd4b11afac43b8d6e4242b1cd5 | **이 묶음 아님** |

뒤의 네 zip (231 파일) 은 **첫 세대 2 리뷰 묶음** (핀 `c13da95a3`) 이다.  판정문 codex_review_gen2_network_20261006.md 는 `8eb8d08b` 반입본과 바이트 동일 (blob 27224b2f), 최상위 99 파일 + bundle_manifest.json 은 `docs/reviews/codex_gen2_network_review_evidence_20261006/` 과 바이트 동일, source 130 은 c13da95a3 blob 130/130 — 새로 반입할 것이 없다.

## 2. 무결성

- bundle_manifest.json 606 행 (최상위 291 + source 315) — 바이트 수 · sha256 전부 일치.  업로드 다섯 zip 파일 607 = 606 + manifest 자신, 남는 파일 0.
- source_manifest.json 315 blob = 핀 트리 (`git rev-parse 165d0cf61:<path>`) 와 315/315 일치.  핀 트리에서 채운 파일 0 (전부 업로드에 있었다).
- 우리 HEAD (db74ea98) 와는 312/315 같다.  다른 3 = `CLAUDE.md` · `docs/reviews/findings.json` · `scripts/check_all.sh` (핀 뒤 커밋 · 시험과 탐침이 import 하지 않는 파일).
- Codex verify_bundle.py 를 무변경으로, 업로드에서 재조립한 보존본에서 실행: files 606 · pinned_blobs 315 · failures 0.  verify_evidence.py 를 보존 증거 사본에서 실행: 14/14 PASS (다시 쓴 두 JSON 도 보존본과 내용 같음).

## 3. 이 폴더에 넣지 않은 것 — 리포 파일 사본 (blob 으로 대신 가리킨다)

- source/ 315 = 우리 리포의 핀 `165d0cf61` 파일 그대로.  경로 · git blob · sha256 은 `docs/reviews/codex_gen2_network_reverify_evidence_20261006/source_manifest.json` 에 있다.
- evidence/reread_extra/ 아래 리포 자료 사본 10 개 (probes/reread_extra.py 가 대조용으로 복사한 것).  앞 9 개는 핀 blob 과 바이트 동일, 마지막 manifest.json 은 탐침이 json.dumps 로 다시 쓴 사본이라 바이트는 다르고 파싱 내용이 같다.

| 묶음 경로 (evidence/reread_extra/…) | bytes | Codex 파일 git blob | 같은 리포 파일 (핀 165d0cf61) |
|---|---:|---|---|
| reference/docs/data/lhs_handover_20261001.csv | 325,772 | 8a6af0648a1e9c00492a64e9517e8b4194e76b33 | `docs/data/lhs_handover_20261001.csv` |
| reference/docs/data/lhsx_handover_20261001.csv | 164,189 | 59f3e457e357cc64c9d61412f41c633d1ad8d0bf | `docs/data/lhsx_handover_20261001.csv` |
| reference/docs/data/lhs_network194_11fcf91e8/merged/lhs/metrics_flat.csv | 806,256 | f792b311fe2d23bcc58fd6486139e9d9f0a3b354 | `docs/data/lhs_network194_11fcf91e8/merged/lhs/metrics_flat.csv` |
| reference/docs/data/lhs_network194_11fcf91e8/merged/lhs/status.json | 259,293 | 2537c0b0a6ce75ff6b59d3aa031610623258ddf5 | `docs/data/lhs_network194_11fcf91e8/merged/lhs/status.json` |
| reference/docs/data/lhs_network194_11fcf91e8/merged/lhsx/metrics_flat.csv | 394,346 | 49d6c270cb7283a0d7dd196722081338a597033a | `docs/data/lhs_network194_11fcf91e8/merged/lhsx/metrics_flat.csv` |
| reference/docs/data/lhs_network194_11fcf91e8/merged/lhsx/status.json | 126,700 | 906b3238f4438dde1f68aacd65e7f524f52ce0b0 | `docs/data/lhs_network194_11fcf91e8/merged/lhsx/status.json` |
| reference/docs/data/lhs_perc_audit_20261001/lhs_20261001_d1ec42fba/perc_audit.tsv | 79,166 | 1ddc9cb35b33756cce6f5e0050f03c711b24c607 | docs/data/lhs_perc_audit_20261001/lhs_20261001_d1ec42fba/perc_audit.tsv |
| reference/docs/data/lhs_perc_audit_20261001/lhsx_20261001_d1ec42fba/perc_audit.tsv | 39,676 | a40c06d02cf15f5dda5a3a86981dfc93ea995cba | docs/data/lhs_perc_audit_20261001/lhsx_20261001_d1ec42fba/perc_audit.tsv |
| reread_v12.py | 24,053 | ae3924c7fc50c04431988f6bc817ac31e3f1e019 | `docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/reread_v12.py` |
| reference/docs/data/lhs_network194_11fcf91e8/manifest.json | 24,239 | af021b5749e8fad8e0ca877431dbb72bedc4e959 (sha256 cd26489f6085432db0772397700eb4bd6d093d363390792f6a72eca0063fbc52) | `docs/data/lhs_network194_11fcf91e8/manifest.json` (blob facd58ae23d5661323fbd17f2005a0e8272b2d47) 과 파싱 동일 |

- 판정문은 이 폴더가 아니라 `docs/reviews/codex_review_gen2_network_reverify_20261006.md` 에 있다.  원문 sha256 6dfa4f2cce651b51e15dee9a78ce38a1d22487bb9270ab8caef3ee36f89682f6 (24,789 B · bundle_manifest 와 일치).  반입본은 50 행과 234 행의 묶음 상대 증거 경로 둘 (evidence/acceptance.json · evidence/tests.json) 을 이 폴더의 리포 경로로 바꾸고 바로 뒤에 [반입 때 리포 경로로 고침 · 원문은 묶음 최상위 기준 상대 경로] 를 붙인 것뿐이다 (`a1e197e4` 와 같은 관례 · check_doc_refs).  반입본 sha256 27d3abd46682fbe593e652ab6f6ed3f5f1fcff81fb02603512a50821afb6813b (25,083 B).
- 바이트가 리포의 다른 파일과 우연히 같아도 **Codex 가 만든 증거는 넣었다** (100 개): evidence/acceptance/ 의 합성 침대 파일 96 (atoms.csv · contacts.csv · input_params.json · mesh_info.json · 빈 review_run.log 19 폴더씩 + full_metrics.json 1 — 우리 시험 도우미가 만드는 같은 합성 침대) · evidence/prior_real_beds.json (= 첫 리뷰 증거 `docs/reviews/codex_gen2_network_review_evidence_20261006/evidence/real_beds.json` · verify_evidence.py 가 읽는다) · 로그 2 · probes/real_beds.py.

## 4. 재현 방법 (우리 트리 = HEAD db74ea98)

- 묶음을 스크래치에 다시 조립했다.  최상위 291 = 업로드 그대로, source/ 315 = 우리 HEAD blob (위 3 파일만 핀과 다름).  묶음 스크립트와 probes 는 무변경.
- README 순서: verify_bundle → run_tests → probes adversarial · numerics · acceptance · real_beds · reread_extra → verify_evidence.
- 환경 차이만 있다: run_tests.py 대신 같은 14 진입점 · 같은 인자 · cwd = source · 같은 PYTHONPATH 의미를 **한 번에 하나씩** 도는 대역 (원본은 2 병렬).  모든 Python 은 `python3 -I -B` (이 기계는 requests · dateutil 이 사용자 site 에 있어 그 경로만 명시로 넣었다) · HOME · TMP = 스크래치 · 네트워크 변수 없음 · git 탐색 상한 (묶음 안 .git 없음 = Codex 와 같은 조건이라 SKIP 3).
- SKIP 3 은 따로 확인했다: `scripts/test_network_solve_certificate.py` 를 스크래치 bare 저장소 (우리 객체를 alternates 로 읽기만) 와 다시 돌리면 23/23 PASS (고치기 전 모듈 `a0a24c538` 과의 비트 동일 대조 포함).
- 우리: Linux x86_64 · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · NetworkX 3.6.1 · Flask 3.1.3 · pandas 3.0.6.  Codex: Windows 11 · Python 3.12.14 · NumPy 2.3.5 · SciPy 1.16.3 · NetworkX 3.7 · Flask 3.1.3 · pandas 3.0.1.

## 5. 결과 — Codex 보존 증거 ↔ 우리 재실행

| 검사 | Codex (보존) | 우리 (HEAD 재실행) | 판정값 |
|---|---|---|---|
| 14 진입점 | rc 0 × 14 · 598 PASS · 3 SKIP | rc 0 × 14 · 598 PASS · 3 SKIP (진입점별 마지막 줄 14/14 같음) · git 객체를 주면 601 PASS | 같음 |
| adversarial 1e14 막다른 간선 | 첫 CG certificate_failed → spsolve_fallback · G 15,000.5 | 같음 | 같음 |
| adversarial 대비 1e6–1e14 의 G | 15,000.5 · 15,000.5 · 15,000.499998 · 15,000.5 · 15,000.5 | 15,000.5 · 15,000.500000015 · 15,000.499998 · 15,000.5 · 15,000.5 | 같음 (상대차 ≤ 9.9e-13) |
| adversarial 0 저항 (GEN2-01) | G None · zero_resistance_requires_contraction | 같음 | 같음 |
| adversarial 옛 세대 변이 8 | 전부 NOT_COMPUTED + 정지 ⑨ | 같음 | 같음 |
| adversarial 직렬 고대비 | 1e16 = not_computed · current_conservation_failed | 같음 | 같음 |
| numerics 13 입력 (참 G 1.45) | G · 방법 · 증서 문제 · 최악 상대오차 1.64427e-7 | 전부 비트 동일 | 같음 |
| acceptance 게시 7 | baseline done · missing_full_cert failed · full_cert_from_cf done (I_bottom 0.1963495408493623) · full_cert_from_h12 done (0.025675122317963317) · missing_cf_cert · cf_bad_conservation · missing_constr_cert done · τ2 hertz 10.980805104698456 | 같은 상태 · I_bottom H12 …963373 · τ2 …454 | 같음 (끝자리만) |
| acceptance 도장 6 (G2RR-01) | control g2 · all_unknown g2 · all_null g2 · one_null_legacy_shape inferred_legacy · g2_declares_legacy g2 · stamp_absent_keys 거부 | 같음 | 같음 |
| real_beds 2 침대 × 4 팔 | clamp · floor · 간선 · 노드 · None 모드 · 사유 · 관통 Rc=0 수 — real14 g2 2,607 · 22 · 2,628 · case15 g2 304 · 8 · 312 · g1_mul 7,487 · 43 · 7,528 / 1,524 · 19 · 1,543 | 같음 | 같음 · 값 상대차 real14 ≤ 6.3e-15 · case15 ≤ 4.2e-9 |
| reread_extra 4 (G2RR-03) | baseline rc 0 PASS 194 · queue_empty rc 0 PASS 0 · plan_absent rc 0 PASS 0 · queue_duplicate rc 0 PASS 194 | 같음 | 같음 |
| verify_evidence | 14/14 PASS | 11/14 — FAIL 3 = float.hex 비트 동일 검사 (이전 Windows 검토값 prior_real_beds.json 대조).  None 양상 (g1 · g2 협착-only 만 None) 은 같다 | 플랫폼 차 (판정 아님) |
| verify_bundle (HEAD 조립본) | — | failures = 위 3 파일 (핀 뒤 변경) | 예상대로 |

**판정값 (상태 · 사유 · 수용 여부 · 세대 · rc · verdict · 개수) 불일치 0.**  수치 차이는 끝자리 (real14 · 합성 침대) 와 반복 풀이 허용 수준 (case15 ≤ 4.2e-9, 그 침대의 FULL 보존 잔차 자체가 1e-9 대) 뿐이다.  판정에 쓰이지 않는 증서 진단값 (residual_rel · conservation_rel · 전류 불균형, 크기 1e-9–1e-19) 은 상대로 더 다르지만 모두 수용 문턱 1e-6 아래다.
