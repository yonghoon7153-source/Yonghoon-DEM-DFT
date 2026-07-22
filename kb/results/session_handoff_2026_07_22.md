# 세션 핸드오프 — 2026-07-21 밤 → 07-22 새벽

밤새 대량 진행. 컨텍스트 유실 대비 완료/진행/대기 스냅샷.

## ✅ 완료·등록 (오늘 밤)

| 항목 | 파일 | 헤드라인 |
|---|---|---|
| VGCF/hBN 2×2 결합 매트릭스 | `db/properties/vgcf_hbn_binding_matrix.{json,csv}` | gallery 1L1L −1.574 / 1L2L −1.592 / 2L1L −1.580 / **2L2L −1.626** (스프레드 52 meV, 협동항 ~28 meV). Shi eq5 4칸 성립, 전 사이트 lithiophobic(+0.10~0.15), 층수 수렴 → NEB 1L 정당 |
| Phonon 8-시스템 스윕 | `db/properties/phonon_stability_sweep.json` | **현역 3인방(modelc/lpsocl/b2o3) 전원 STABLE** = 동적안정 검증. comp2=깊은 Li-안장, comp1=무해(−3.5 meV), comp3/4/5 안정. 교훈: 허수 크기≠심각도, follow ΔE로 판정 |
| comp2 안장 DFT 확정 | 위 json + `db/structures/comp2_V0_v3_candidate.xyz` | followmin −508.7 meV/cell (UMA −535와 5% 일치). champion 교체 안건 |
| BVSE 3-시스템 결론 | `kb/results/bvse_3system_conclusions_2026_07_21.md` | 그래프=canonical 일치 검증. 6월 σ-1.33× 서사 폐기. **기하≠동역학**(채널 단조↑ 3.32→4.74→6.73 vs Ea 비단조 0.197→0.271→0.199). vesta 3종 검증 + B-중심/경계 크롭 등록 |
| adhesion dW=0.44 유도 완결 | `kb/methodology/adhesion_energy.md`, `tools/adhesion_v30u/` | dW=ΔW_strain(NCM 변형E) 계열 앙상블 평균. v30u 스크립트 백업 회수 |
| LPSOCl Ea 완전판 | `db/properties/lpsocl_md_arrhenius.json` | 0.271±0.033 (3-seed×3-T, hiT 반영) |

## ⏳ 진행중 (서버)

- **kgy GPU** — drag barrier (`vgcfdrag`, frozen-in-plane 수정판):
  - ✅ **Li_on_graphene 0.281 eV** — 대칭 barrier, img3(bridge) 피크, 문헌 ~0.3 일치 = **drag 방법 검증**
  - ⚠ **Li_on_hbn 0.010 eV** — 프로파일 비대칭/무피크 = Li가 hBN ring-hollow에 안 앉음(Shi: hollow−0.56 vs N-top−0.46). **낮 작업: Li의 진짜 hBN 사이트 찾아 홉 재정의**
  - ⏳ Li_in_gallery / 2L2L (핵심 값) 진행중
  - ⚠ **drag 미끄럼 버그 교훈**: 기판 완전자유(1 1 1)면 PBC 시트 병진→barrier=0. 반드시 면내 고정(0 0 1).
- **kgy — NEB 빌드 ✅ 성공 (2026-07-22, conda 3층 오염 격파)** → **GPU NEB 가동 중**:
  QE 7.4.1 from-source GPU 빌드. 실패 원인이 conda(uma env)의 **3층 오염**이었음:
  ① `CFLAGS=-march=nocona`(nvc 컴파일 거부) ② PATH의 `x86_64-conda-linux-gnu-ld/ar`
  ③ **env 변수 `LD`/`AR`**(PATH 지워도 configure가 씀). 3층 다 걷어내야 함
  (`build_qe_neb_gpu_kgy.sh`에 영구 박제: unset 툴체인 env + PATH purge + make.inc sed LD→mpif90).
  neb.x = cufft/cublas 링크 GPU 빌드. `run_neb_kgy.sh`로 hBN→graphene→gallery→2L2L NEB 체인 시작.
  **교훈: conda 오염 = 컴파일(CFLAGS)+링크(binutils PATH)+env변수(LD/AR) 3층, 정답은 셋 다 제거.**
- **drag 결과 (NEB 교차검증용 백업)**: graphene 0.281(검증됨) / hBN 0.010(약결합 평평 PES,
  NEB로 재확인 중) / gallery·2L2L drag는 이미지당 2h로 느려 NEB가 대체.
- **gabia GPU** — pbrefine complex_doped(SDCP DFT+U): iter ~100, acc 하강(5 Ry 아래면 순항). iter 100서 정체면 Γ-선수렴/β0.01 카드
- **gabia CPU** — LPSOCl ELF+CDD(`lpsoclelf`): SCF 도는 중(SG15 NC, np10). cube 3종 → §11 마지막 칸

## 📋 대기 (수확 후)

1. drag barrier → `db` 등록 + 균일분산 가설 **조건② 판정** (gallery 안정+이동가능?)
2. pbrefine verdict → SDCP 마스터 doc 헤드라인 (vertical=자세강제 편향 vs image-clean=sulfonate_down; 도핑 강화/약화 확정)
3. LPSOCl ELF cube → `lpsocl_elf_bonds.csv` (**Li–O 트랩 vs b2o3 0.780** 직접 비교 — "산소는 트랩" 서사 3번째 증거)
4. comp2 v3 후보: gap/EOS 민감도 재검 → champion 교체 최종 결정
5. (빌드 완료 시) neb.x → drag×NEB 한 케이스 교차검증

## 백로그 (논문 전 선택)
LPSOCl Bader/elastic(suite), hull/ESW / b2o3 전단 G/E(strain 0.01) / B₂O₃ Li–B–S 산물상 gap/DOS(설계규칙⑤ 마지막)
