# 운영 노트 — 2026-06-16 세션 (deck 5–7 확정 + cascade 65 champions + NEB endpoint)

> 0611 노트의 후속. 이번 세션은 deck 작성과 cascade 후반부, NEB endpoint relax가 병행됨.

## 1. Seminar deck 진행 (v1.34 → v1.36+)

**확정된 슬라이드 (실물 이미지 검수 통과)**:
| # | 슬라이드 | 메시지 | md 섹션 |
|---|---|---|---|
| 1 | Title (Research Seminar, 연구실 표준 템플릿) | thesis 없음 — slide 2로 흡수 | §1 Layout v2 |
| 2 | Systems & Key finding | "Not electronic — Li vacancies + 4d-Cl anti-sites" + Wyckoff (4a/4b/4d/16e) + primitive→4f.u./5f.u. 분기 | §1B v4 FINAL |
| 3 | 3-tier pipeline | 6 post-processing 분야 (Structure/Electronic/Bonding/Transport/Mechanical/Electrochemical), ESW 포함 | §1C v3 FINAL |
| 5 | MLIP screening detail | "Free S²⁻ ← Cl⁻" + champion 시각화 (cubic ordered ↔ rhombo with 4d-Cl 점선 영역), C(8,4)=70 / C(10,2)=45 | §1 sub FINAL |
| 6 | DFT validation detail | 11-volume BM3 EOS, B₀ 26.2 vs 21.7, "first decoupling signal" (vol contract + bulk soften), BM3 수식 + B₀/B₀′ 정의 | §1 sub FINAL |
| 4 (= 7) | Headline 4 messages | 영어 표 + ICOHP 각주 + Schlem ref + Eₐ EXACT match 회전 라벨 | §1D v2 |

**용어 각주 표준 (Langevin 스타일 — 우상단)**:
- Langevin anneal · MLIP · EOS · BM3 · BFGS · SCF · B₀ · B₀′ · k×L ≥ 40 Å · ICOHP

**Slide 2 footnote refs (확정)**:
- T. Zuo et al., *Angew. Chem. Int. Ed.*, 62, e202213228 (2023).
- P. Adeli et al., *Angew. Chem. Int. Ed.*, 58, 8681 (2019).
- R. Schlem et al., *Adv. Energy Mater.*, 10, 1903719 (2020).
- Y. J. Kim et al., *ACS Mater. Lett.*, 7, 724 (2025). (UPE stiffness, DOI 10.1021/acsmaterialslett.4c02029)

**Slide 3 footnote refs (4d-disorder 도입)**:
- H.-J. Deiseroth et al., *Angew. Chem. Int. Ed.*, 47, 755 (2008).
- M. A. Kraft et al., *J. Am. Chem. Soc.*, 139, 10909 (2017).
- N. Minafra et al., *Solid State Ionics*, 346, 115223 (2020).
- B. J. Morgan, *Chem. Mater.*, 33, 2004 (2021).

**Slide 6 footnote**: F. Birch, *Phys. Rev.*, 71, 809 (1947).
**Slide 7 (Headline) footnote**: Schlem 2020 (위 동일) — Eₐ EXACT match.

**Slide 18 (Oxidation 4-axis) 보강 — delithiation-kinetics 메커니즘 채택 (2026-06-12)**:
- 산화 분해 = delithiation 반응 → σ를 올린 같은 요인 (Li vacancy + 4d-Cl AS)이 분해 kinetics도 가속
- 물질 레벨 분해 ↑ (Zuo CV: S⁰/polysulfide/SO₂ ↑) BUT cell 레벨 R_int ↓ (8.9 vs 13.2 Ω·h⁰·⁵) — Zuo 실제 결론
- Manuscript 지침 (확정): 산화 안정성을 Cl-rich의 "장점"으로 절대 쓰지 않음. 축 분리로만 서술.

## 2. Cascade 273-batch — 65/70 champions (오늘 메시지 기준)

**핵심 변화 (vm db 미반영분)**: B₂O₃, Fe₂O₃, Y₂O₃, La₂O₃, **Nd₂O₃**, Sm₂O₃, ZrO₂, TiO₂, SiO₂, Cr₂O₃ — **11종 추가** (M³⁺ 다수).

| 항목 | 06-09 시점 | 06-16 시점 |
|---|---|---|
| `db/properties/doping_cascade_verified.json` | 14 dopant | 14 (vm 미동기화) |
| gabia 실제 cascade | 14 done | **65 done / 70 expected** |
| slide 22 본문 수치 | "41 champions" | **갱신 필요 → ~65 champions** |
| paper #2 Nd₂O₃ 줄 | "DFT-relaxed run5 완료, EOS+post 대기" | **cascade 결과 추가 필요 (de_post, B₀, E_VRH)** |

**Fe₂O₃ 정상화 기록**: x005·x010 06-06엔 rc=127 (런처 환경 문제 추정) → 06-16 14:29 재시작 후 x005 ✓ DONE (18:13), x010 진행 중. **B₂O₃ x002도 06-06 rc=127 → 재시도 필요**. 모두 launcher env (BATCH_DIR / TOP_K_SIGMA / TOP_K_NCM)가 원인.

**Sc₂O₃ Q&A 카드 (slide 22, 06-11 완주)**:
- x002 de_post = −0.974 / E_VRH = 18.7 (가장 soft) / B₀ = 17.8 / "Sc₂O₃+Clrich" champion
- x005·x010 — `FINAL_RANKING.json` 추출 필요 (농도 trend가 Fig 후보)
- Sc₂O₃ verdict: cascade STRONGEST winner

## 3. Li3N NEB — endpoint B (relax_right) BFGS step 18, fmax 0.020

| 단계 | 상태 |
|---|---|
| Endpoint A (on_N_left) relax | ✓ done |
| **Endpoint B (on_N_right) relax** | **BFGS step 18, fmax 0.020 → target 0.02 임박** |
| CI-NEB band 진입 | 아직 시작 안 함 — 옛 `neb_ci.log` (06-15 20:45 step 14, fmax 0.27)는 죽은 것, 무시 |
| 본 DFT NEB 5–7일 일정 | endpoint B 끝나면 init |

오늘 watch에 "warmup last:" 라인이 endpoint B 단계임. CI band 0 step.

## 4. KISTI Nd SCF — GPU OOM, CPU 빌드로 우회 결정 (06-16)

- gabia 사이드: NEB pw.x (14.2 GB) + cascade UMA σ-MD (Fe₂O₃_x010, 4.97 GB) + driver = 총 ~20 GB / 49 GB
- Nd SCF는 GPU init peak에서 자리 못 잡고 OOM (출력 0 byte)
- **결정**: CPU 빌드로 우회 — NEB·cascade 그대로 두고 진행
- 보안: paper #2 doping 비교용 Nd 결과는 **cascade champion (UMA-relaxed)**이 메인. KISTI SCF는 별도 EOS validation 트랙

## 5. 운영 함정 누적 (0611 노트 + 0616 추가)

이번 세션에서 새로 발견된 것:
- **Fe₂O₃ / B₂O₃ rc=127 (06-06)**: launcher env가 BATCH_DIR 또는 TOP_K 정정 전이라 의존 모듈 미로드 가능. 0611 노트의 #1·#4 trap이 0606 시점에 영향 줬을 가능성.
- **GPU 공존 한계**: NEB pw.x (14 GB) + UMA σ-MD (5 GB) + small python = ~20 GB. **추가 GPU pw.x 시도하면 OOM**. Nd CPU 우회가 정답.
- **vm db pull은 PAT 없는 gabia에서 직접 안 됨**: cascade 결과는 gabia → rsync → vm 수동 동기화 필요 (0611 노트에 이미 기록).

## 6. 남은 작업

- [ ] cascade 70 완주 (Fe₂O₃_x010 stage 10 진행 중 + B₂O₃_x002 재시도 + α₁ 더 있을 수 있음)
- [ ] gabia → vm 동기화: `doping_cascade_verified.json` 갱신 (14 → 65+ dopant), Sc₂O₃ x005/x010 정량값 추가
- [ ] slide 22 본문 갱신: "41 champions" → "65 champions", Nd₂O₃ 줄 정량값 채우기
- [ ] Nd SCF CPU 빌드 launcher (별도 명령, 이 세션 회신에 포함)
- [ ] Headline 표 (slide 7) 영어 표 확정판 검수 — 회전 라벨 오타 수정 후
- [ ] Slide 8–11 (M1–M4 본문) 템플릿 변환

## ⚠ KISTI sbatch JobName 규칙 (정정 2026-06-16)

**모든 KISTI sbatch는 `#SBATCH -J llm_finetuning_test`로 지을 것.**
- 0611 노트에서 "JobName=llm_finetuning_test는 템플릿 잔재"라고 적은 건 **오해**였음 —
  실제로는 KISTI 큐 정책이 이 이름을 요구/기대하는 것 (자유 이름 `nd_k441_short` 등은 지양).
- `--comment qe` directive도 필수 (없으면 제출 거부, 앱 종류 명시).
- 따라서 향후 Nd EOS / B₂O₃ 등 모든 KISTI 잡:
  ```
  #SBATCH -J llm_finetuning_test
  #SBATCH --comment qe
  #SBATCH -p amd_a100nv_8
  ```
- 짧은 walltime(4h) backfill 트릭은 유효 (766470이 priority 40으로도 b2o3 762968 안 밀고 먼저 시작).
