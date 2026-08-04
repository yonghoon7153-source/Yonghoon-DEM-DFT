# 📚 LITDB — Argyrodite SE 문헌 단일 시스템

> **앞으로 논문은 여기서만 본다.** 여러 곳(db/literature, kb/papers, db/properties, Excel)에 흩어진 문헌을 한 곳에서 생각·참고·비교하기 위한 통합 MD 시스템.

## 폴더 구조
| 파일/폴더 | 역할 |
|---|---|
| `INDEX.md` | 전체 논문 마스터 표 (Excel 자동 생성). "무슨 논문 있나" 한눈에. |
| `papers/<slug>.md` | **논문 1편 = digest 1개.** 표준 양식 = `papers/_TEMPLATE.md` |
| `our_dft_baseline.md` | 우리 comp1/modelc DFT 기준값 — 모든 비교의 기준점 |
| `comparison_vs_ours.md` | 문헌 물성 ↔ 우리 DFT **차이 + 적용 인사이트** |
| `properties/*.md` | 물성별 교차표 (ionic / oxidation / mechanical / electronic) |
| `figures/<slug>/` | **논문 PDF 에서 잘라낸 그림·표** + `figures.json` (색인). 아래 §🖼 참고 |

## 논문 "먹이는" 워크플로우  (= `litdb-curator` 에이전트)
**트리거: PDF 업로드 후 "논문 에이전트 실행해줘"** (또는 "이 논문 litdb에 넣어줘", "이 논문 정리해줘", "feed this paper")
→ 에이전트가 **(1) 백그라운드로 digest 저장** + **(2) 사용자에게 자세히·체계적으로 설명** + **(3) 질문 답변(토론)**. digest 깊이 기준 = `papers/zuo2022_chlorination_cathode_interface.md` (논문 정독 수준, 분량 무관).
1. PDF 업로드 → 트리거 발화
2. 에이전트가 `_TEMPLATE.md` 양식으로 `papers/<slug>.md` 생성. 특히:
   - **DFT 방법** — code·functional·pseudo·k-points·supercell·U·vdW·무질서 처리
   - **Figure set** — 각 그림이 무엇을 보여주나 + 우리가 참고할 점
   - **Post-processing** — 어떤 후처리(NEB/Bader/COHP/grand-potential…)를 어떻게 적용·기록했나
   - **우리 DFT 대비** — 같은 점 / 다른 점 / 왜
   - **적용 인사이트** — 내 연구에 어떻게 쓰나
3. `INDEX.md` status → ✅, `comparison_vs_ours.md` · `properties/` 갱신
4. 사용자와 인사이트 공유 → 합의된 결론만 deck/paper로

## 통합 대상 (흩어져 있던 기존 DB → 점진 흡수)
- `db/literature/` : argyrodite_computational_littable.csv, argyrodite_dft_littable.csv, refs.json, 개별 MD 7편(damore/fadillah/lee/li/pustorino/sundar/zhao)
- `db/properties/` : **literature_tensions_audit.json**, oxidation_stability.json, electronic/elastic/eos/diffusion.json
- `kb/papers/` : verified_refs_2026_05.md, computational_methods_draft.md, narrative_with_literature_steps.md …
> 흡수 원칙: 각 항목을 해당 `papers/<slug>.md` 또는 `properties/*.md`로 옮기고, 출처 파일은 INDEX에 "통합됨"으로 표기.

## status 범례
✅ digest 완료 · ⬜ PDF만(미digest) · 📄 Excel 메타만

## 🗨️ Q&A 로깅 (recurring)
슬라이드·결과를 보며 나온 질문은 **해당 주제 MD의 "🗨️ Q&A 로그" 섹션**에 누적:
- 산화/ESW 관련 → `comparison_vs_ours.md`
- 특정 논문 관련 → 그 논문 `papers/<slug>.md` 의 §Q&A
**트리거: "Q&A 작성해줘"** (또는 "이 q&A도 적어놔줘") → 직전 질문/답을 자동으로 해당 MD의 "🗨️ Q&A 로그"에 항목 추가.

## 🖼 논문 그림 크로핑 (figures/)
논문을 읽을 때 PDF 를 따로 열지 않게, **캡션을 앵커로 그림·표를 잘라** 저장한다.

처음 한 번만 — Ubuntu 24.04(WSL)는 PEP 668 로 시스템 pip 이 막혀 있어 **venv** 를 쓴다:
```bash
python3 -m venv ~/.venvs/litdb && ~/.venvs/litdb/bin/pip install -q pymupdf pillow
echo "alias litfig='~/.venvs/litdb/bin/python3 ~/Yonghoon-DEM-DFT/tools/litdb/extract_figures.py'" >> ~/.bashrc
source ~/.bashrc
```

**그다음부터는 이 두 줄이면 끝난다** — `litdb/inbox/` 를 훑어 digest 와 자동으로 짝지어 준다:
```bash
litfig --inbox          # 어느 PDF ↔ 어느 논문인지 표만
litfig --inbox --run    # 실제로 자르기 (--skip-done 로 이어서)
```
**하위 폴더까지 훑는다** — 논문을 `★ 랩실 논문/`·`DEM 논문/`·교수님별로 나눠 뒀어도 그대로 찾는다.
inbox 가 다른 데 있으면 `--inbox_dir '/mnt/c/Users/<계정>/Desktop/읽어야되는 논문'`.

매칭 앵커는 ① digest 메타의 `inbox #NN` ↔ 파일명 앞 번호 ② 제목 토큰 겹침(**IDF 가중** —
`batteries` 같은 흔한 말은 증거로 안 친다) ③ **PDF 1쪽 본문**(출판사 해시 파일명
`admi…suppmat.pdf` 대응). `Sup)`/`SI`/`ESI`/`mmc` 는 SI 로 보고 같은 논문에 묶는다.

> **원본 PDF 는 repo 에 없다.** `litdb/inbox/` 가 .gitignore 대상이라 digest 는 경로만
> 적어둘 뿐 실물은 각자 로컬에만 있다. 그래서 `--inbox --run` 이 `litdb/figures/_sources.json`
> 에 **slug → 원본 PDF(inbox 상대경로)** 를 남긴다 — 다른 머신에서도 폴더 구조만 같으면
> `--inbox_dir` 하나로 다시 찾는다.

한 편만 콕 집을 때 — ⚠ `<slug>` 는 **자리표시자**다. `litdb/papers/` 의 실제 파일 이름을 넣는다:
```bash
litfig --clean \
    --slug kraft2017_lattice_polarizability_argyrodite_Li6PS5X \
    --pdf "litdb/inbox/31. Influence of Lattice Polarizability….pdf" \
    --pdf "litdb/inbox/31. Sup) Influence of Lattice Polarizability….pdf"
```
- 출력: `litdb/figures/<slug>/fig_3.png` · `tab_S1.png` · `figures.json`
- SI PDF 로 넘긴 것과 `Supplementary Fig. 1` 형태의 캡션은 **자동으로 S 번호**가 된다.
- **임베디드 이미지 추출이 아니라 영역 렌더**다 — 벡터 그림(ACS/RSC 다수)도 똑같이 나온다.
- 오탐(본문의 "Figure 3 shows …" 문단)은 ① 구두점 규칙 ② 그래픽 존재 검증 두 겹으로 막는다.
- 기본 300 dpi (긴 변 3000 px 상한) + PNG 재압축. 그림 1장 ≈ 250 KB — 슬라이드에 바로 써도 된다.
- **점검**: `litfig --audit` — 잘라둔 것 전체에서 의심스러운 것만 (그림 0개 / 번호 구멍 /
  본문 없이 SI만 / 극단 세로비). '번호 구멍'은 대개 정상이다(전면 그림·PDF 에 그림 없음).
  진단이 필요하면 `litfig --slug <slug> --why` 로 캡션별 판정을 좌표째로 본다.

**현황 (2026-08-06)**: 논문 **83편 / 그림 1,126장** (본문 573 + SI 406 + 표 147),
audit 깨끗 65편. digest 주석이 붙은 그림 720장(64%). 작업트리 297 MB.

> 실제로 돌려보고서야 드러난 버그 4개 — 같은 실수를 반복하지 않도록 남긴다:
> ① `\bsup` 이 "**Sup**erionic" 을 잡아 본문 11편이 통째로 SI 번호가 됐다
> ② 그림 **안**의 축 라벨이 크롭 경계로 잡혀 son2025 본문 5장이 통째로 유실됐다
> ③ `id(page.parent)` 캐시 키가 문서 간 **주소 재사용**으로 충돌 — 배치에서만 앞 논문의
>    그래픽이 뒤 논문에 새어 결과가 실행 순서에 따라 달라졌다(단독 실행으론 재현 불가)
> ④ 연도를 안 봐서 `Minnmann_2021` 이 `minnmann2024` digest 에 100% 로 붙었다

**webapp 연동** — digest 본문에서 그림을 `Fig. 3`, `Fig. 5e`, `Table S1` 형태로 언급하면
문헌 화면에서 자동으로 링크가 걸리고, 마우스를 올리거나 **드래그**하면 오른쪽 여백에 그림이 뜬다.
문서 맨 아래에는 그림 카드가 쫙 깔린다 (클릭 → 큰 창 → 저장). "그림 3"·"Fig3" 표기는 안 잡힌다.

그림을 누르면 **두 가지를 구분해서** 보여준다:
- 📄 **논문 캡션 (원문)** — PDF 에서 그대로 가져온 caption
- 📝 **우리 digest 정리** — ① `## Figure set` 표의 그 그림 행 ② 그 그림을 다루는 본문 절 제목

digest 를 쓸 때 `## 10. Figure set` 표를 채워두면(`| Fig | 내용 | 우리 활용 |`) 그게 그대로
그림 주석이 된다. 그 주석을 누르면 digest 본문의 그 줄로 점프한다(옵시디언식).

> ⚠ 저작권: 여기 있는 건 **남의 논문 그림**이다. repo 를 공개로 돌릴 일이 생기면 `litdb/figures/`
> 를 먼저 지운다(`litdb/inbox/` 의 PDF 원본은 이미 .gitignore 대상). 규모가 커지면
> (지금 83편 297 MB · .git 은 재생성 이력 때문에 972 MB) PNG 만 .gitignore 하고 `figures.json` 만 추적하는 쪽으로 바꾼다
> — 그때는 `--inbox --run` 한 번이면 각자 로컬에서 그대로 복원된다.

## 📐 개념/방법 노트 (concepts/)
- `concepts/dos_vbm_efermi_methods.md` — DOS·PDOS 계산(수식), VBM 절대비교 불가+정렬, 절연체 E_F smearing artifact (코드 재현 포함). 슬라이드 21/24/25 방어용.
