# 확보 대기 — 외부 자료 (2026-08-26)

> 여기 있는 것은 **아직 못 받았고, 없이는 못 닫는 질문이 걸려 있는 것**만이다.
> 확보되면 이 파일에서 지우고 해당 digest/record 로 옮긴다.

## ⏳ 구할 수 없어서 대기 중

| # | 무엇 | 왜 못 구하나 | **막혀 있는 것** |
|---|---|---|---|
| **P1** | **OMat24 본문 PDF**<br>*Nat. Comput. Sci.* (2026) `10.1038/s43588-026-00996-w` · arXiv **2410.12771** | 사용자 다운로드 실패. SI(16 pp)와 보충 데이터만 확보 → `db/external/omat24/` | ① **softening 정의식** — 우리는 CSV 값만 있고 `force_softening = ?` 의 식을 모른다<br>② `eqv2/OAM` 포논 중앙값 **0.2565** 이상치 — 같은 이름 힘 softening 은 1.0015 로 모순<br>③ **UMA 와의 관계** — UMA-S 가 표의 어느 행에도 없다 |
| **P2** | **[30]** `Deciphering Surface Hydrolysis Mechanism in Argyrodite via Large-Scale Machine Learning Potential Simulations`<br>Ji Hoon Kim & Sang Uck Lee, ***Adv. Funct. Mater.* 2026** | **accepted · production 대기** (권·쪽·DOI 미발급, 2026-08-26 랩 발표목록 기준). 색인도 아직 안 됐다 | ① **Q4** — H₂S **발생량 정량**(우리 db 의 Taklu 1.07→0.49 cm³/g 와 대조 가능한가)<br>② **T2** — guided MD **유도좌표 정의**(D_S–H · D_O–P)와 ICOHP 기술자 방법 원본<br>③ MD 조건 전부(온도·앙상블·물층 두께·초기배치) — 데이터셋만으론 모른다 |
| **P3** | **He, X.; Zhu, Y.; Epstein, A.; Mo, Y.** *"Statistical variances of diffusional properties from ab initio molecular dynamics simulations"*, **npj Comput. Mater. 4, 18 (2018)** · DOI `10.1038/s41524-018-0074-y` | 웹 접근이 프록시에 막힘(nature.com · semanticscholar · arxiv · ADS 전부 403). 서베이도 **⚠ PDF 미보유** 딱지 | **β 문턱 0.8 의 대안 근거.** 이 논문이 *확산 이벤트 수*로 분산을 정량하는 원전인데 **구체적 수치 기준을 우리가 못 봤다.** `kb/concepts/beta-gate.md` §7-5 가 이것에 걸려 있다 |

**대체 경로 (지금 하고 있는 것)**
- P1 → **보충 데이터로 갈 수 있는 데까지 갔다**(`db/external/omat24/README.md`). 정의식 없이도
  "MPtrj → OMat24 계열에서 5/5 아키텍처 개선" 은 읽힌다. **정의식이 필요한 주장만 보류.**
- P2 → **데이터 저장소를 먼저 확보**했다(`db/external/kim2026_argyrodite_hydrolysis/`,
  `github.com/jhkimmmmm/Hydrolysis-argyrodite`). 500 ps 생성물 3종 + DFT/MLP 검증 123점.
  **기구는 구조에서 재집계 가능, 수량·프로토콜은 논문 대기.**
- P2 대안 → **[78]** Y.S. Kim 외 *Nat. Commun.* 2026 (다른 그룹, 확보 완료 · 판독 대기).
  기구 사슬(P–S 약화 → S–O 치환 → PS₄ 회전 → O-rich Li₆PO₅Cl-like)이 겹치지만
  **실험 XPS + 0 K DFT** 라 [30] 의 대규모 MLIP MD 를 대체하지 못한다.

**저자 직접 요청 (P2)** — 세션에서 질문한 이력이 있어 명분이 있다. 교신저자 주소는
`suleechem@skku.edu` (SSRN 6772406 표지에 인쇄돼 있다).

---

## 📥 확보했고 판독 대기 (inbox)

| 번호 | 무엇 | 상태 |
|---|---|---|
| 74 | Shin 2026 *Small* — BH₄⁻ 회전 ↔ Li⁺ 수송 (Li₆PS₅X) | 🔄 판독중 |
| 75 | Kim 2026 SSRN **6772406** — SEI 신판 | ⏳ **판본 대조**(우리 보유 6020397 대비) |
| 76 | Kim 2026 *ACS Nano* — GA × MLIP Li staging | ⏳ |
| 77 | Batzner 2022 *Nat. Commun.* — **NequIP** | ⏳ |
| 78 | Y.S. Kim 2026 *Nat. Commun.* — 수분 표면열화 (+source data 14시트) | ⏳ |
| 79 | Musaelian 2023 — **Allegro** | ⏳ |

## 💾 대용량 데이터 — **repo 밖**에 둔다

⛔ `.git` 이 이미 1.6 GB 다. 아래는 **계산 머신에만** 두고 파생 결과(MAE 표·CSV)만 repo 에 넣는다.

| 파일 | 크기 | 출처 | 왜 |
|---|---|---|---|
| **`lips.xyz`** | 213 MB | Batzner 2022 (NequIP) | **Li₆.₇₅P₃S₁₁ — 우리 화학계(황화물) 유일**. DFT 에너지+힘 라벨 |
| **`li3po4-joint-together.xyz.zip`** | 261 MB | Musaelian 2023 (Allegro) | **Li₃PO₄, 앞 25k 프레임=melt / 뒤 25k=quench** — 고에너지·비평형 구간이 **라벨로 갈려 있다** |
| `lipo-quench.xyz` | 525 MB | Batzner 2022 | Li₄P₂O₇ quench. 위 둘과 겹쳐 **우선순위 낮음** |
| `Ag_warm_nospin.xyz` · `fcu.xyz` | — | — | ⛔ 우리 축과 무관 |

**용도**: 우리 UMA 를 이 프레임들에 **단일점**으로 돌려 **그들 DFT 와 힘 MAE 대조** → T1 대리지표를
**남의 정답지로 교정**한다. 눈금은 이미 셋 있다 — MTP 자체학습 **0.073** / SevenNet-0 base **0.070** /
SevenNet 반응계 fine-tune **0.57** eV/Å.
