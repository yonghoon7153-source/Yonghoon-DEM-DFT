# ⬜ 미적용 정정 — 2026-09-19 믹싱 DEM 배치에서 나온 것

> **이 파일은 "아직 안 고친 것" 의 목록이다.**  고친 것이 아니라 **고쳐야 하는 것**이고,
> 사용자 비준 전이라 정본 파일을 건드리지 않았다.  ⛔ **이 파일의 주장을 근거로 인용하지 말 것** —
> 정본(카드·CSV)이 여전히 옛 값을 담고 있으므로 **둘이 어긋나 있는 상태**다.  그 어긋남을 숨기지
> 않으려고 이 파일이 있다.

## 0. 경위

2026-09-19 에 믹싱·분산·지표 축 논문 **10편**을 한 배치로 digest 했다 (아래 §3).
그 과정에서 **기존 정본 카드의 오류 여러 건**이 드러났다.  digest 에이전트가 PDF 원문을
직접 읽고 잡은 것이므로 근거는 단단하지만, **정본 수정은 비준 대상**이라 여기에만 적는다.

## 1. ⛔ `varkey2026_multicontact_elastoplastic_dem` — **중복 카드를 만들지 않았다**

2026-09-19 배치의 10번 논문(*"DEM simulation of solid-electrolyte separator and cathode
densification using a stress-based multi-contact elasto-plastic model"*)은
**이미 정본에 있는 `varkey2026_multicontact_elastoplastic_dem` 과 동일 논문**이다
(Adv. Powder Technol. 37 (2026) 105338, `10.1016/j.apt.2026.105338`, 저자·소속·투고일 전부 일치).

⇒ **새 카드를 만들지 않았다.**  기존 카드가 정본이다.

⚠ **이 중복은 하마터면 들어갈 뻔했다.**  배치를 조정한 쪽이 중복 검사에 `grep -E` 와 `\|`(BRE
문법)를 섞어 써서 — ERE 에서 `\|` 는 리터럴 파이프다 — 패턴 전체가 문자열 하나가 됐고
**여덟 축이 전부 조용히 `0건`** 을 냈다.  digest 에이전트가 그 `0건` 을 믿지 않고 `git ls-tree` 를
직접 돌려 잡았다.  ⇒ **CLAUDE.md §litdb 의 2026-09-03 `kang2025` 사고와 같은 구조**이고
(그때는 INDEX 하나만 grep, 이번엔 grep 자체가 죽음), 막은 것은 검사기가 아니라
**"위임받은 쪽이 직접 다시 재라"** 는 지시 한 줄이었다.

## 2. ⬜ `varkey2026_multicontact_elastoplastic_dem` 정정 목록 (미적용)

PDF 원문 + Supplementary(DOCX) 재독으로 확인된 것.  **아직 카드를 고치지 않았다.**

| # | 자리 | 현재 (틀림) | 정정 |
|---|---|---|---|
| A1 | §2·§3 소재 | `Li₃YBrCl₆` | **`Li₃YBrCl₅`** — PDF 두 곳 모두. 전하중성도 `Li₃Y +6 vs 7음이온 −7` 로 안 맞는다 |
| A2 | §7 "Furnas dip" 행 | *"DEM·de Larrard dip @AM70–85 … 일치"* | ⛔ **행 삭제** — 그 논문에 **조성 스윕이 없다**(단일 조성 하나). `@AM70–80` 은 **우리 `mpm2d_PS_rcp` 결과**로 보인다 |
| A3 | §7 multi-contact 행 | *"F_mc ↔ 18× 연화 = 같은 증상(과강성) 다른 처방"* | **부호가 반대다** — `F_mc` 는 접촉을 **뻣뻣하게**, 18× 연화는 **무르게**. `comparison_vs_ours_DEM.md:319-334` 는 이미 정정돼 있는데 카드가 안 따라갔다 |
| A4 | 겹침 온셋 | *">24 % 에서 구속력 추가"* | **δ ≈ 10–12 % 부터 갈라진다**. 24–26 % 는 **잔류겹침 `δ_R`** 이다 |
| A5 | Supplementary 힘 단위 | `×10⁴ N` | **`×10⁵ N`** (Figure S1 y축 직접 판독). TN 은 FEM 을 **42 % 과소**, MC 는 **2.6 % 이내** |
| A6 | eq (7) | 논문 오식을 표지 없이 복제 | `(δ−δ_R)` → **`(δ−δ_R)³` 세제곱 누락** (Thornton–Ning 1998 eq 29). 차원이 안 맞는다 |
| A7 | eq (11) 기호 | `a_ij`(접촉 반경) | **`A_ij`(접촉 면적)** — 차원상 면적이어야 N 이 된다. ⚠ 그리고 **논문이 `β·ν·A_ij` 를 어디에서도 정의하지 않는다** |
| A8 | "ρ>0.7 에서만 유효" | Giannis 2021 Granul. Matter 로 읽힘 | 실제 출처는 **ref[41] = Giannis 2021 *Pharmaceutics* (제약 정제)** 이고, **방정식에는 밀도 게이트가 없다** |

**데이터 파일** `docs/data/varkey2026_ionic_vs_pressure.csv` (메인 리포):
⛔ **`150 MPa` 행은 실재하지 않는다** (Fig 14 마커는 100·200·**250**·300·350 다섯 점).  보간값이
데이터 행으로 들어가 있다 ⇒ 삭제.  `200 MPa` sim `0.0029 → 0.00266`.  접촉면적 열 재판독
`7.95 / 8.1 / 9.25 / 10.4 / 12.85` (실제는 **단조 증가**인데 현재 250 에서 꺾여 내려간다).
`docs/data/densification_porosity_db.csv` 도 `Li3YBrCl6 → Li3YBrCl5` 10행.

## 3. 새로 들어온 카드 (이 커밋)

| slug | 축 |
|---|---|
| `otani2025_dem_se_dispersion_aggregation_compression` | ASSB SE **분산(응집수) 스윕** — 우리에게 없는 공정축 |
| `hare2026_dem_pept_dry_mixing_nmc622_eirich` | **PEPT 실측으로 DEM 유동장 검증** |
| `lischka2025_dem_eirich_intensive_mixer_dry_mixing` | Eirich 집약믹서 · cohesion-number γ 스케일링 |
| `asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing` | CB 분쇄 **PBE + DEM** |
| `nadeem2023_gnn_mixing_index` | 입자 스케일 **혼합지수(GNN)** |
| `chibwe2020_nnsi_segregation_index` | **분리지수(NNSI)** |
| `jadidi2023_dem_batch_solid_mixers_review` | 배치 고체믹서 DEM **리뷰** |
| `lippke2023_dem_drying_structure_formation_lib` | 습식 **건조** 구조형성 — ⛔ 건식 전이 금지 |
| ✅ `sun2026_dem_extrusion_recirculation_dry_electrode` | 건식 **압출** — 후속 커밋으로 들어왔다 (md5 `df6fadb6c1ec406b864d82661ae0fd0a` · 446줄 46,159 B 대조) |

⚠ **`INDEX.md` 는 이 커밋에서 안 고쳤다** (사람이 큐레이션하는 축이라 손대지 않는다).
**`INDEX_DEM.md` 는 고쳤다** — 생성물이므로 `tools/litdb/build_index.py` 를 재실행했다.
⇒ **그 재생성이 손으로 쓴 행 하나를 덮었다. §5 를 볼 것.**

## 4. ⚠ 이 배치에서 난 운영 사고 — 병렬 digest 가 서로의 카드를 지웠다

`scripts/litdb_promote.py` 의 `--open`/`--cleanup` 은 **고정 경로 + 고정 브랜치명**을 쓰고
`shutil.rmtree` 를 한다.  여러 세션이 동시에 돌자 **한 세션의 `--open` 이 다른 세션의 미커밋
카드를 말없이 지웠다** — 실제로 카드가 **여러 번 유실**됐고, 전원이 스크래치패드 백업을
떠 두어 복구했다.

⇒ **처방 (권고, 미적용)**: 병렬 digest 시 ① 세션별 **고유 워크트리 경로·브랜치명**을 쓰거나
② 카드를 쓴 직후 **즉시 커밋**하거나 ③ 각자 파일만 떨어뜨리고 **부모가 모아 한 번에** 커밋한다.
이번 커밋은 ③ 으로 했다.

⚠⚠ **그런데 ③ 에는 ③ 만의 함정이 있고, 이 커밋에서 실제로 밟았다.**
부모가 모아 커밋할 때 집은 것이 에이전트의 **최종본이 아니라 중간 백업**이었다 —
`jadidi2023_dem_batch_solid_mixers_review` 를 **72,572 B(591줄 중 568줄) 판**으로 먼저 커밋했는데,
그 판에는 에이전트가 **스스로 철회한 틀린 문장**이 살아 있었다:

> *"Tables 7–13 의 어느 연구도 [elasto-plastic adhesive 를] 쓰지 않았다 (내 전수 확인)"*

실제로는 **Pantaleev 2017 (Table 12)** 이 Thakur 2014 visco-elasto-plastic adhesive 로 돌렸고,
그 행이 그 카드에서 가장 값진 한 줄(*"FT4 보정이 맞았는데도 혼합속도는 **정성적으로만** 예측"*)을
담고 있었다.  **잡은 방법은 크기 대조 하나** — 에이전트 보고의 `80,599 B` 와 커밋된 `72,572 B` 가
안 맞았다.  최종본으로 교체했다 (푸시 전이라 같은 커밋에 들어간다).

⇒ **③ 의 보강**: 부모는 커밋 전에 **에이전트가 보고한 최종 크기·줄수와 실물을 대조**한다.
백업 경로가 여러 개면(`CARDS_SAFE/` vs 에이전트 자기 디렉터리) **가장 새 것이 아니라 보고된 것**을 집는다.
★ 한 줄 교훈 — **"복구했다" 는 "최신을 복구했다" 가 아니다.**

## 5. ⚠ `INDEX_DEM.md` 재생성이 **손으로 쓴 주석 한 줄을 덮었다**

§3 의 "INDEX 를 안 고쳤다" 는 이 커밋에서 **철회한다** — `INDEX_DEM.md` 는 생성물이므로
`python3 tools/litdb/build_index.py` 를 **돌렸다** (손으로 고친 것이 아니다).  결과:
`digest 121편 → 130편`, 새 카드 8 장이 자동 분류돼 들어갔다.

그런데 재생성이 **기존 행 하나를 덮었다.**  그 행은 배너(*"손으로 고치지 말 것"*)를
어기고 누군가 손으로 써 넣은 것이라 생성기가 알 수 없었다.  ⇒ **지워진 원문을 여기 남긴다.**

```
| `he2026_dem_calendering_inhomogeneity_areal_density` | NCM 양극 **calendering 불균일성**을 DEM 으로 — 면적로딩 15.2→20.0 mg cm⁻² 가 힘분포·접촉수·입자 integrity 를 어떻게 가르나.  ★ 우리 코퍼스에 없는 **AM-만 극한**(NCM622 97.77 wt%, SE 없음) 대조군 · 나노압입 + Hg 압입 이중검증 — He (J. Power Sources 696 (2026) 241479) | DEM (EDEM 2024 상용, EEPA 탄소성 + JKR; 액체계 LIB) | 2026-09-15 | 🖼 — |
```

잃은 것 두 가지:
1. **주석** — *"우리 코퍼스에 없는 **AM-만 극한**(NCM622 97.77 wt%, SE 없음) 대조군"*.
   생성기는 제목을 카드에서 그대로 떠 오므로(`build_index.py:rows()`, 180자 절단) 이 문장은
   **카드 제목에 없다** = 사람이 인덱스에만 적었다.
2. **절 배치** — 손으로는 `공정 — 캘린더링 · 압축 · 건식전극` 에 두었는데 생성기는
   `접촉역학 · 소성` 으로 보낸다.  `group_of()` 가 **위에서부터 먼저 맞는 것**을 쓰는데,
   그 카드의 **유형 문자열에 `EEPA` 가 있어** 접촉역학 묶음이 `calender` 보다 먼저 맞는다.

⬜ **미적용 처방 (비준 대상, 둘 중 하나)**
- (a) 주석을 **카드 제목에 넣는다** — 그러면 생성기가 다음 재생성에서도 싣는다 (근본).
- (b) `group_of()` 의 키워드 우선순위를 손본다 — 단 **다른 논문의 분류가 같이 움직인다.**

⚠ 어느 쪽도 하지 않았다.  지금 `INDEX_DEM.md` 는 **생성기가 낸 그대로**이고, 위 주석은
**이 파일에만** 있다.  (`xu2023_realistic_am_shape_cgmd_calendering` 행도 다시 쓰였지만
그림 수 `— → 🖼 7` 만 바뀐 것이라 잃은 내용은 없다.)
