# 원문 확인 기록

확인일 2026-11-10. 문헌 카드는 `../package/litdb/papers/`의 핀 `0991161693d2d8f36975f2c9454472b54bb11c2c` 사본으로 대조했다. 아래 공개 원문/저자본은 웹 도구로 직접 읽었다. PDF 전문이나 추출 전문은 이 폴더에 저장하지 않았다. **원격 파일 바이트를 내려받지 않아 SHA256은 미취득**이다. 페이지는 명시된 PDF/저자본의 페이지이며 다른 판의 페이지와 혼용하지 않는다. 아래는 짧은 검토 요약이고 전문 복제는 없다.

## S1 — Bardenhagen et al. 2001 (BH01)

- 제목: An Improved Contact Algorithm for the Material Point Method and Application to Stress Propagation in Granular Material.
- 출처: CMES 2(4), 509–522 (2001), 대학 제공 원문 PDF.
- [원문 PDF](https://www.sci.utah.edu/~guilkey/MPMPubs/Bardenhagen-ImprovedContact-01.pdf)
- 확인: 인쇄512쪽(파일4쪽), §2.1의 접근/이탈·traction 분리 및 이종/소성 계면 설명. 인쇄513쪽(파일5쪽), §2.2 식14–16과 N=2 제한 및 법선 공선 조건. 인쇄516쪽 부근(파일8쪽), 구 경사면 해상도/강체 해와의 차이. 인쇄520쪽(파일12쪽) 지그재그 접촉과 Poisson비 논의.
- 확인 결과: 계면 traction 평형과 다물체/미끄럼의 수치 조건이 명시된다. 이것이 U5 및 국소 분리 검산을 단순 총운동량/전역 하중방향으로 대체할 수 없다는 근거다.
- 미확인: 새 구현에서 실제 결함 존재 여부. 지름8셀을 모든 구성식·접촉의 충분조건으로 보장하는 주장. 카드의 모든 그림 digitization 및 식22 max→min 교정을 독립 수치구현으로 검증하지 않았다.

## S2 — Nezamabadi et al. 2022 (NZ22)

- 제목: Modelling the compaction of plastic particle packings.
- DOI: [10.1007/s40571-021-00391-4](https://doi.org/10.1007/s40571-021-00391-4), Computational Particle Mechanics9,45–52.
- [White Rose 저자 승인본 PDF](https://eprints.whiterose.ac.uk/id/eprint/172185/1/nezamabadi%20et%20al_mpm_plastic_accepted_23.12.2020.pdf)
- [기관 서지·버전 기록](https://eprints.whiterose.ac.uk/id/eprint/172185/)
- 확인: 논문2쪽(파일3쪽) §2/Eq4 물질점 부피 갱신·암시적 MPM·미소변형 탄소성. 논문3쪽(파일4쪽) §3 및§4 물성/단위,300원판,무마찰,Φ=VS/V. 논문4–5쪽(파일5–6쪽) Fig3·바닥응력·재밍 근처 논의. 논문8쪽(파일9쪽) Appendix1 Eq19 dVS/VS.
- 확인 결과: mass fraction과 다른 현재 입자부피 기준 Φ_d 해석이 Eq4/Φ정의/Appendix19에 일관된다. 원본 구현을 보지 못했으므로 본문 수식과 코드의 일치까지 보증하지 않는다. E10MPa,ν.45,σ_y.4MPa,H0/1/3,암시적CD·2D·미소변형 구성식은 확인했다.
- 미확인: 카드의 .68/1.11MPa 및 .836/.841,비1.09 등 그림값을 새로 digitize하지 않았다. 그 숫자는 카드대조·합성 예시에만 사용했다.

## S3 — Cárdenas-Barrantes et al. 2020 (CB20)

- 제목: Compaction of mixtures of rigid and highly deformable particles: a micro-mechanical model.
- DOI: [10.1103/PhysRevE.102.032904](https://doi.org/10.1103/PhysRevE.102.032904).
- [저자 원문 arXiv PDF](https://arxiv.org/pdf/2006.02867)
- 확인: 파일3쪽 §II.B의 시료·neo-Hookean ν.495·plane strain·등방 압력 제어·관성수. 파일4쪽 Fig3/§III.A의 κ·마찰별 경향. 파일6쪽의 Z0와 준비/마찰 의존 설명.
- 확인 결과: 해당 조건에서 마찰 증가 시 초기/최대 충전율이 낮아지는 경향은 지지된다. 다른 구성식·3D·일축 모든 경우에 순서가 강제되는 정리는 아니다. NSCD와 명시 Bardenhagen을 같다고 놓을 근거는 제공하지 않는다.
- 미확인: 카드의 P0 및 φmax 모든 정밀 판독 수치, CB21·CB22 원문 전체. 해당 값은 카드대조 한정.

## S4 — Nguyen et al. 2017 (NG17)

- 제목: Compaction of granular materials composed of deformable particles.
- DOI: [10.1051/epjconf/201714005013](https://doi.org/10.1051/epjconf/201714005013), EPJ Web of Conferences140,05013.
- [HAL 저자본의 공개 미러 PDF](https://pdfs.semanticscholar.org/6ebb/099b95cb3bfb5e25d1c3d7eade3201018194.pdf) — 표지에 HAL01595248,2017-09-26 및 저자/제목/DOI가 일치한다.
- [HAL 원 식별자](https://hal.science/hal-01595248) — 직접 document URL은 이 회차 도구에서 열리지 않아 동일 저자본 미러로 읽었다. publisher URL도 도구 오류가 났다.
- 확인: 논문2쪽(파일3쪽) 단일입자 재료·설정. 논문3쪽(파일4쪽) §4,바닥반력/σ0 정규화,μ0/.5,Fig2–3. 논문4쪽(파일5쪽) Z 및 재밍 설명.
- 확인 결과: 두 방법은 탄성MPM 대 소성BPM이라 접촉 표현 하나의 ablation이 아니다. Z 차는 응력 순서의 증명이 아니다. 원문은 마찰의 거시 변형 영향이 작다고 기술한다.
- 미확인: 카드의 Z 차 .19–.30 새 digitization, 도표 범례 불일치 해결을 위한 원자료.

## S5 — So et al. 2022

- 제목: Contact model for DEM simulation of compaction and sintering of all-solid-state battery electrodes.
- DOI: [10.1016/j.mex.2022.101857](https://doi.org/10.1016/j.mex.2022.101857).
- [Kyushu 대학 원문 PDF](https://catalog.lib.kyushu-u.ac.jp/opac_download_md/7161227/7161227.pdf)
- 확인: 논문5–6쪽(파일6–7쪽), Eq8–9,면적인자의 실험밀도 맞춤·스프링 보정·최대 overlap 선택. 논문7쪽(파일8쪽) Table1의 마찰 및 물성 출처.
- 확인 결과: 후보의 경험적 선택을 숨기지 말자는 원칙은 원문과 맞는다. c_area를 fitting parameter로 쓰고 스프링·overlap 수치를 선택한다. LPS 문헌이며 LPSCl의 직접 물성 검증이 아니다.
- 미확인: 각 그림의 숫자 새 추출 및 선택 값 전체의 통계적 자유도 해석.

## S6 — PyCompact / Demirtas / BH00의 제한된 확인

- [PyCompact publisher](https://www.sciencedirect.com/science/article/pii/S2352711025004613), DOI10.1016/j.softx.2025.102495: 제목·2026 SoftwareX33·저자·DEM→MPFEM 및 Fe–Si–Al–P 검증 범위 확인. μ=.2 선택·내부5MPa판독 차이는 이번 원문 재검증 미완료로 카드대조 한정.
- [Demirtas2021 publisher](https://www.sciencedirect.com/science/article/pii/S0032591021005210), DOI10.1016/j.powtec.2021.06.004: 제목·저자·MPFEM/DEM 초기배치 및 재료·실험 범위 확인. optimized selection의 정확 문장과1008h 비용은 카드대조 한정.
- [BH00 publisher](https://www.sciencedirect.com/science/article/pii/S0045782599003382), DOI10.1016/S0045-7825(99)00338-2: 접촉 모델 및 논문 범위의 초록 확인. BH00 전문 재검증은 미완료. 격자/접촉의 상세 주장에는 전문을 읽은 BH01을 사용했다.

## S7 — Zunker et al. 2025의 출판 지위

- [Publisher 정식 논문](https://www.sciencedirect.com/science/article/pii/S0032591025003675)
- [저자 연구실 출판목록](https://kamringroup.berkeley.edu/publications/)
- 확인: 동일 제목·다섯 저자, Powder Technology459,120972(2025), DOI10.1016/j.powtec.2025.120972. 제공 카드의 프리프린트본 존재와 정식 출판물 존재를 구분해야 한다.
- 미확인: 제공프리프린트와 정식판의 모든 본문차이, MDR6–8 매개변수의 전면 재대조, 최신 코드 기능. 핀 c6159505의 코드능력을 최신 버전으로 대체하지 않았다.

## 재현 산술

`counterexamples.py`는 표준라이브러리만 쓰며 solver를 import하거나 실행하지 않는다. `counterexamples.json`은 등급만 수렴하는 함수,점별 정의OR,운동량 보존과 에너지 생성의 논리반례를 저장한다. 이는 실제 구현·재료·실험 데이터가 아니다.
