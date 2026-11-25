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

## ✅ 완료·등록 (07-22 낮 — CDD 그림 세팅 + 통찰)

CDD(charge density difference) 3종 = Liu2022(AMI 9,2200011) (f)(g) 대응 비교그림. relaxed 구조 single-point 3-SCF 차분(complex−host−Li). kgy `~/work/vgcf_hbn/cdd/*/`.

| 항목 | 내용 |
|---|---|
| **CDD 3-cube 확정** | graphene(레퍼런스, 깨끗한 상하 다이폴) / hBN / **gallery 2L2L(hero)**. 3패널 = Liu f/g 대응 |
| **전하이동 크기 순위** | hBN(least yellow) < graphene < **gallery/2L2L(most yellow, Δρ ±0.033 ≈ hBN 4×)**. E_bind 방향과 일치하나 배율 다름(CDD 4× vs E_bind 6× = vdW+배위 기여) |
| **논문 통찰 (hBN 전자받음)** | gallery에서 hBN 쪽도 노랑(축적). **hBN이 받개로 변신한 게 아님** — VGCF가 진짜 받개(Cu역할, Shi eq5), 갇힌 Li⁺가 hBN 표면 **유도분극/스크리닝**. 서사: "hBN=passive cap / VGCF=acceptor / Li=양면배위 구속" → gallery 최강결합(−1.626) 설명 |
| **lithiophilicity 해석** | 노랑↑ = 전하이동↑ = 결합경향↑(lithiophilic 쪽). 단 정량순위는 E_bind로(상관관계, vdW+배위 동반) |

**툴 (이번 세션 추가/수정):**
- `tools/electronic/cube_to_vesta_cdd.py`: `--structure-only` 플래그(밀도·등가면 빼고 순수 구조 vesta). 한글 title → ASCII 버그 수정(assert 깨지던 것).
- `tools/vgcf_hbn/supercell_1Li.py`: 시트(B/N/C) n×n 타일 + **Li 1개만**(넓은 시트 그림용, VESTA Boundary는 Li도 n²복제되니까). **최종결정: 원래 단일셀 4×4 유지**(이미 1 Li/4×4 희박, 타일링 왜곡 회피) — 스크립트는 필요시용 백업.

**VESTA 재현 세팅 (모든 CDD 패널 통일):**
- **iso 0.002~0.003** (낮으면 그래핀 π 재분포가 탄소마다 도배 = 노이즈). 3패널 **iso 동일** 필수(안 그럼 전하이동 크기 착시).
- **빨강 제거**: 등가면 mode `Positive and negative`(양쪽 lobe 겹침) → No.1 `Positive`(+iso 노랑)/No.2 `Negative`(−iso 청록).
- **색**: 노랑=축적(받개), 청록=결핍(Li⁺). 원소색 VESTA 표준(Li 보라/B 분홍/N 파랑/C 회색).
- **unit cell 프레임 off**: `Objects → Structural Models →` 하위 unit cell 토글(논문 그림 관례).
- **투영 parallel 표준**(거리·lobe 크기 정직). perspective는 TOC/발표 hero 한 장만.

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
  - 📍 **라이브 (07-22 오후)**: Pass 1(endpoint-B relax) **3/4 완료** — Li_on_hbn/graphene/gallery(1L) ✅,
    **Li_in_gallery_2L2L endpoint-B relax 중**(이온스텝 0 첫 SCF 수렴 中, mag 0.01=슬로싱 없음). 단일 GPU라 순차 —
    2L2L 엔드포인트 끝나면 스크립트가 **Pass 2: 4개 CI-NEB(7이미지) 자동 순차**(hbn→graphene→gallery→2L2L). 전체 ~1~2일.
    출력경로: `~/work/vgcf_hbn/neb/<case>_nebB.out`(Pass1), `~/work/vgcf_hbn/neb/<case>/neb.out`(Pass2).
    기준: hBN Shi 0.10 / graphene 문헌~0.3(drag 0.281 검증) / gallery·2L2L=신규 핵심값. **← 수확 대기, 남겨둠**
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
