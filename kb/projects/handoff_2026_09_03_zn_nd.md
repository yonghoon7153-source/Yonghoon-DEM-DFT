---
title: "인수인계 — 2026-09-03 세션 (Zn ALZIB 협업 · Nd 교수님 지침 · 도구 2개)"
date: 2026-09-03
updated: 2026-09-03
tags: [handoff, zinc, alzib, nd, professor, xrd, pdf, session]
status: 활성
kind: project
system: mixed
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-03
verifiedBy: agent
explored: false
authoredBy: agent
claimType: mixed
evidenceScope: multi-source-primary
---

# 인수인계 — 2026-09-03 세션

> 이 세션은 **C-12 · 폴라론 S0 를 전혀 건드리지 않았다.** 그쪽은 다른 세션이
> v30 / 회신 BF · 회신 Z-2 까지 끌고 갔다. 여기서 한 것은 **완전히 새로운 두 트랙**이다.

## 0. 먼저

```bash
cd ~/Yonghoon-DEM-DFT
git fetch origin claude/friendly-meitner-lldvar
git rev-list --count HEAD..origin/claude/friendly-meitner-lldvar
git pull origin claude/friendly-meitner-lldvar
python3 tools/kb_wiki.py lint | head -3          # 0 errors 확인
```

이 세션의 커밋 6개 (오래된 것부터):

| | |
|---|---|
| `d33d140b` | Zn ALZIB 기여 스코핑 카드 (C1–C7) |
| `7e767e77` | ★ 2026-09-03 그룹미팅 교수님 코멘트 지침 카드 |
| `6d29bb7a` | C1 상 지문표 도구 + PDF 추출기 tools 승격 |
| `5122d769` | 교수님 카드에 발표 덱 부록 (전사 청취값 → 덱 확정값) |
| `a99d421a` | Kyungrok Do BML 세미나 digest (litdb/talks/) |
| `16146eb2` | zhu2026 그림 34장 (digest 본체 작업 중) |

---

## 1. ★★★ 제일 급한 것 — Nd 논문 방향 (교수님 지침)

**`kb/seminars/group_meeting_2026_09_03_nd_professor_directives.md` 를 먼저 읽어라.**
2026-09-03 그룹미팅(48분) 전사에서 뽑은 지침. ★ 표시가 구속력 순위다.

세 줄 요약:
1. **"DFT 자체는 노블티가 아니에요"** — 계산을 *추가*한 건 차별점이 아니다.
2. 조성이 경쟁 Nano Energy 논문과 거의 같고(할로겐리치 1.6 vs 1.7, x=0.02) 메커니즘
   설명도 같다 → 현장에서 **"그냥 duplication이네"** 판정.
3. **"왜 하필 Nd냐"** 가 48분 중 8번 반복됐다. 교수님이 허용한 길은 둘뿐 —
   ① 물리적 당위 ② **"DFT로 스크리닝했더니 얘가 제일 좋더라"**.

### ⚠ P-1 — 우리 DFT 가 실험과 반대 방향이다 (미팅에서 공개됨)

| | 밴드갭 | 산화 안정성 |
|---|---|---|
| 실험 (발표자) | 소폭 **증가** | 대폭 **향상** |
| 우리 DFT | **감소** (2.184 → 1.632 eV) | **저하** (산화 onset 1.92 V < modelc 2.14 V) |

**새 버그가 아니다.** `kb/physics/nd_4f_doping_consolidated_corrected_2026_06_24.md` **C7**
(Nd 5d 가 CBM 을 끌어내림 — 4f-in-gap 금속이 아니다) 과
`kb/syntheses/nd_doping_two_axis_verdict.md` 가 2026-06 에 이미 기록했다.
**두 축 모두 실험과 반대다. 3개월째 미해소이고, 원고에 DFT 를 넣는 순간 리뷰어가 잡는다.**

미팅에서 우리 쪽이 약속한 다음 작업:
1. 실험자(재현)의 **Rietveld CIF** 를 받아 우리 설계 구조와 **PDOS · −ICOHP · 밴드** 대조.
2. ⚠ **DFT 는 정수 원자만 넣을 수 있어 x = 0.02 를 그대로 구현 못 한다.**
   구조 차이가 경향 불일치의 원인인지부터 갈라야 한다.
3. 4f 입장은 유지 — 4f 는 밴드엣지에 영향 없고, 움직이는 것은 **5d** 다 (C7 과 일치).

> ⛔ **이 대조가 "실험과 맞는 구조를 찾을 때까지 구조를 바꾸는" 작업이 되면 안 된다.**
> 그건 교수님이 반려한 "믿고 싶은 대로 선 긋기"(D-6) 의 계산판이다.
> `kb/templates/estimand_card.md` 를 먼저 채우고 **판정 게이트를 결과 보기 전에** 박아라.

### 원고에 지금 쓸 수 있는 계산 주장은 하나뿐

**Li 이동 장벽: Li₂S 0.305 eV vs Li–Nd alloy 0.229 eV** (덱 확정값).
나머지(밴드갭·산화안정성)는 쓰면 실험과 충돌한다.

### 덱 확정 수치 — 전사 청취값을 이걸로 교체

| 항목 | 값 | 비고 |
|---|---|---|
| Young's modulus | **15.1 → 13.9 GPa** | 전사에선 "14.9" 로 들렸다 — STT 오류 |
| 이온전도 Ea | **0.313 → 0.263 eV** | |
| Li 이동 장벽 | Li₂S **0.305** / Li–Nd alloy **0.229** eV | |

---

## 2. 새 트랙 — Zn ALZIB 협업 (수계 아연)

우리 황화물 SE 와 **완전히 다른 계**다. 절대 수치를 섞지 마라.

- 스코핑: `kb/projects/zn_alzib_dft_md_contribution_2026_09_03.md` (계산 후보 C1–C7)
- 상대 발표 digest: `litdb/talks/do2026_bml_alzib_preconditioning.md`
- 교차 비교: `litdb/comparison_vs_ours.md` **§K** (물성 4축과 수치로 안 섞는다는 금지표 포함)

### C1 은 이미 돌렸다 — 결과가 실험 설계를 바꾼다

`db/properties/zn_cu_phase_fingerprint_2026_09_03.{csv,json}` ·
`docs/figures/zn/zn_cu_phase_fingerprint.png`

**43° ± 1° 안에 8개 상이 1.47° 폭으로 겹친다.**
`Zn(101) 43.221` — `CuZn-β′(110) 43.282` — `Cu(111) 43.318`
→ Cu–Zn 간격 **0.097°**. 게다가 발표자가 "suggest" 만 한 **Zn–Cu 합금(β′)이 정확히 그 사이에 낀다.**
회절 기하가 강제하는 것이라 분해능 문제가 아니다.

**진단창은 31–39°** (Cu 반사 0개): ZnO 31.77/34.42/36.26 · Zn(002) 36.29 · Zn(100) 38.99 ·
Cu₂O(111) 36.42 · CuZn₅(100) 37.94. **ZHS 는 43° 부근에 주선이 없고 기저면이 2θ≈8–11°** 라
저각을 안 찍으면 존재 여부 자체를 모른다.
덤: GI-XRD 정보깊이 — 2–4 µm 층 전체는 ω ≈ 8–15°, 최표면(<0.5 µm)은 ω ≲ 2°.

⚠ **스코프 정정**: 카드의 C1 에 "DFT 이완 → 격자상수" 라고 적었던 것은 **틀렸다.**
DFT 격자상수 오차 ~1 % = 2θ 0.3–0.4° 인데 가르려는 간격이 0.097° 다. **실험 문헌 격자상수가 더 정확하다.**
DFT 가 실제로 필요한 자리는 **convex hull**(어느 Cu–Zn 상이 열역학적으로 가능한가) 이고 아직 안 돌렸다.

### 아직 안 한 것
- estimand(보고량) 카드 미작성 · `db/governance/decisions.json` 미등록 · BML 과 협업 합의 없음.
- `kb/elements/Zn.json` 은 **황화물 SE 도펀트 관점**으로만 쓰여 있다. 수계 Zn 음극으로 인용 금지.
- C2–C7 전부 미착수.

---

## 3. 새 도구 2개 (둘 다 selftest 음성 경로 포함)

### `tools/xrd/phase_fingerprint.py` (selftest 49)
분말 XRD 지문표. 일반 역격자 계량텐서 + Cromer-Mann. 다중도는 hkl 전수 나열 후 d 로 묶어 자동.
`--report --csv --json --figure`, `--depth`(GI-XRD 침투깊이), `--target/--window`.
**못 하는 것**: Rietveld 정량 아님(전착 Zn 은 002 texture 라 강도비 안 맞는 게 정상) · 어느 상이
실제 생기는지 못 말함 · γ-brass 는 **위치 전용**(52원자 basis 미확보, 강도 null) · ZHS 미계산.

### `tools/litdb/pdf_text.py` (selftest 27)
**⚠ 앞 세션의 "PDF 라이브러리 못 쓴다" 판단을 정정한다.**
`pip install` 은 실제로 안 된다(`cryptography` pyo3 panic). 그런데 **pdfminer 는 이미 설치돼 있고**,
pdfminer 가 cryptography 를 쓰는 곳은 *암호화 PDF 복호화 하나뿐*이라 그 모듈만 스텁으로 막으면 동작한다.
이 도구가 그 스텁을 자동으로 깐다.

실측 차이: Wiley 논문 1편에서 stdlib 스캐너 **367자(워터마크만)** vs pdfminer **39,482자(본문 전체)**.
Wiley/Elsevier 는 본문이 Form XObject 안이라 stdlib 로는 워터마크만 나온다 —
**stdlib 결과를 논문 내용으로 믿으면 안 된다.**

이 환경에 **없는 것**: poppler(`pdftotext`·`pdftoppm`) · mutool · gs · qpdf →
Read 툴의 PDF 페이지 렌더링도 안 된다. **스캔/이미지 PDF**(`/Font 0`) 는 텍스트가 아예 없으니
내장 JPEG(DCTDecode) 을 바이트로 뽑아 이미지로 Read 하는 우회가 필요하다.

---

## 4. 파일 혼선 — 반드시 알고 있어야 한다

같은 날짜·같은 표시이름으로 **서로 다른 발표자료 2개**가 올라왔다. md5 로 구분해라.

| md5 | 내용 |
|---|---|
| `12fa7c66…` | **Kyungrok Do**, Zn ALZIB pre-conditioning (30쪽) — 수계 Zn |
| `e2035697…` | **Jae Hyun Park**, Argyrodite for ASSLMB (38쪽) — **우리 Nd/O 덱** |

PDF 원본은 repo 밖(업로드 파일)이라 컨테이너와 함께 사라진다.

---

## 5. 다음 한 수 (골라라)

1. **Nd D-3**: `tools/cascade/build_screening_funnel.py` 가 **란탄족을 포함하는지** 확인.
   포함해서 Nd 가 상위로 나오면 교수님이 허용한 경로 ②가 열린다.
   ⚠ 돌리기 전에 "무엇이 나오면 경로 ②로 간다" 를 먼저 적어라 (사후 선택은 마감 규율 위반).
2. **Nd P-1**: 재현 Rietveld CIF 확보 → 구조 대조. 게이트 먼저.
3. **Zn C1 후속**: Cu–Zn convex hull QE 붙여넣기 블록 (gabia/kgy).
4. **Zn C2+C3**: zincophilicity + ΔG_H\* — C-12 슬랩 파이프라인 재사용. 보고량 카드 먼저.

## 6. 하지 말 것

- 전사 기반 수치를 인용하지 마라 (덱이 1차 출처).
- Zn 계 수치를 우리 황화물 db 와 같은 표에 넣지 마라.
- doped 마감(`db/properties/sdcp_doped_closed_2026_08_28.json`)의 금지 서술은 여전히 구속력이 있다.
- 원고·슬라이드·사용자 설명에 `estimand`·`canary`·`claim ceiling`·코드 필드명을 쓰지 마라
  (2026-09-01 용어 규율 — 코드 내부 이름으로만 유지).
