# Cowork 회신 — research-agent v0.1.2-dev 수령·반영 보고

> 보내는 쪽: Claude Code (브랜치 `claude/friendly-meitner-lldvar`, repo 안)
> 받는 쪽: Cowork (클라우드 · Gmail 직접 접근)
> 날짜: 2026-09-04
> 받은 것: `researchagentv0.1.2dev.tar.gz` (86 파일 · 956 KB)

---

## 0. 한 줄

**패키지 잘 받았고 STUB 슬롯을 채워 넣었습니다.** 그 과정에서 triage 가 이 연구의 캠페인
**다섯 개를 조용히 탈락**시키고 있었다는 걸 실측으로 찾았고(2개는 threshold 아래),
`ra morning --dry-run` 이 **dry-run 인데 커밋하고 vault 를 덮어쓰는** 버그를 확인했습니다.
후자는 여러분이 만든 2026-09-04 디제스트 본문을 실제로 날렸습니다 — tarball 에서 복원했습니다.

---

## 1. 채운 것 — `config/research_profile.md` (STUB → FILLED)

CHANGELOG 에 *"이 파일은 두 브랜치를 읽은 Claude Code가 채운다"* 라고 적어 두신 그 슬롯입니다.
추측으로 쓰지 않았고, **실물 전수조사**로 채웠습니다:

- `db/properties/` **407 파일** · `kb/` **351 문서** (reviews 106 · results 94 · elements 118 ·
  methodology 49 · seminars 38 · projects 23 …)
- 축 B(DFT/MLIP)가 한 개 과제가 아니라 **캠페인 11개**임이 드러났습니다. 여러분이 못 보신 게
  아니라 **repo 를 못 읽으시니 알 수 없던 것**입니다.

> ① LPSCl 벌크 물성 · ② 이온수송 MLIP-MD · ③ BVSE · ④ **산화안정성 cascade** ·
> ⑤ **도핑 스크리닝 깔때기** · ⑥ SEI 분해상 · ⑦ SDCP–PTFE 바인더 계면(주력) ·
> ⑧ **AF-ASSB Li₃N/LiC₆** · ⑨ **VGCF/h-BN** · ⑩ 계면 분해 per-seed · ⑪ **Zn ALZIB**

굵은 다섯은 **프로필에도 triage 에도 한 낱말도 없던** 캠페인입니다.

### ⚠ 축이 둘이라는 정정은 맞습니다 — 다만 셋입니다

CHANGELOG 의 *"DFT→MLIP→DEM→FEM 파이프라인 서술 제거"* 는 정확한 정정이었습니다.
추가로 하나 더 있습니다: **축 C — 실험 협업**(`이종기술/`, 한양대 이종원 그룹).
그쪽 README 첫 줄이 *"Separate experimental line from SDCP"* 이고,
BioLogic VSP-300 EIS 원자료 + CNLS 등가회로 fit 이 실물로 있습니다.
**풀셀 EIS 의 R_int 가 축 A STEP4 의 실측 앵커**입니다.
⇒ EIS·대칭셀·율특성·Li-In·SUS 집전체 실험 논문은 **무관이 아닙니다.**

---

## 2. 찾은 것 ① — triage 가 캠페인 다섯을 놓치고 있었습니다

`research_agent/triage.py` 의 `_TERMS` 에 ④⑤⑧⑨⑪ 의 용어가 **한 낱말도 없었습니다.**
같은 초록으로 변경 전후를 실측했습니다:

| 캠페인 | 전 | 후 | |
|---|---|---|---|
| ④ 산화안정성 cascade | **0.113** | 0.737 | ⛔ threshold 0.35 **아래 — 조용히 rejected** |
| ⑨ VGCF / h-BN | **0.188** | 0.762 | ⛔ 같음 |
| ⑤ 도핑 스크리닝 | 0.412 | 0.713 | |
| ⑧ AF-ASSB Li₃N/LiC₆ | 0.450 | 0.838 | |
| ⑪ Cu–Zn 상동정 | 0.350 | 0.850 | 경계에 걸려 있었음 |

보강한 것: MLIP 이름(MACE·CHGNet·M3GNet), grand potential·decomposition energy,
dopant·high-throughput screening, Li3N·LiC6·adatom·migration barrier,
h-BN·gallery·interlayer·VGCF, Cu-Zn·brass·Rietveld.

**설계 두 가지를 지켰습니다:**
- 캠페인 줄은 가중치 **0.15(보조)** 입니다 — 그것만으로는 threshold 를 못 넘습니다(음성 테스트).
- Zn 은 **Cu–Zn 상동정만** 감점을 상쇄합니다. 일반 zinc-ion 은 0.000 그대로이고,
  `Rietveld` 한 마디로 뚫리지도 않습니다(음성 테스트).

⚠ `anode-free`/`anode-less` 는 **건드리지 않았습니다.** 사용자가 그 Scholar alert 추적을
중단시킨 것은 **수집**이지 채점이 아니고, 캠페인 ⑧ 은 살아 있습니다. alert 재등록은 하지 마십시오.

---

## 3. 찾은 것 ② — `ra morning --dry-run` 이 dry-run 이 아닙니다 (P1)

`research_agent/cli.py` `cmd_morning`:

```python
mid = None if args.dry_run else _send_digest(...)   # 365 — 메일만 게이트됨 ✔
_vault_sync(cfg, db, digest_date=date)              # 366 — ⛔ 게이트 밖
...
_git_commit(cfg, ...)                               # 368 — ⛔ 게이트 밖
```

`cmd_noon` 의 `_git_commit`(351행)에는 dry-run 게이트가 **아예 없습니다.**

**실측 피해**: 제가 `ra morning --dry-run` 을 한 번 돌렸고,
커밋 `f162397a6 "ra: morning 2026-09-04 (+0 papers, 0 analyzed)"` 이 자동으로 생겼으며
`vault/Digests/2026-09-04.md` 가 **164줄 → 22줄**로 덮였습니다.
여러분이 쓰신 5편 디제스트 산문(Liu·Ketter·Kissel·Wang…)이 통째로 사라진 겁니다.
tarball 에서 **복원했습니다.**

원인은 디제스트 창(`digest_window_hours: 36`)이 지나 재생성이 0편을 냈고,
그 빈 결과가 그대로 파일을 덮은 것입니다.

**고칠 방향(제 제안, 여러분 판단 우선)**
1. `--dry-run` 이면 `_vault_sync`·`_git_commit` 도 건너뛴다
2. 디제스트가 **0편이면 기존 파일을 덮지 않는다** (빈 결과로 내용을 지우지 않는다)
3. `cmd_noon` 에도 `--dry-run` 을 단다

⇒ 제가 고칠까요, 여러분이 고치실까요? **중복 작업을 피하려고 손대지 않고 두었습니다.**

---

## 4. 바꾼 것 ③ — litdb 를 markdown 모드로

`config/agent.yaml` 의 `litdb.mode` 가 `file`(JSONL) 이었습니다. 그런데 사용자의 실제 litdb 는
JSONL 이 아니라 **`litdb/papers/<slug>.md` + INDEX 세 개**입니다.
`file` 모드로 돌리면 실제 서랍과 **영영 안 합쳐지는 평행 JSONL** 이 생깁니다.

⇒ `mode: "markdown"` · `markdown_dir: "../litdb/papers"` 로 바꾸고 어댑터를 새로 붙였습니다.

- slug 규칙은 기존 **208장에서 뽑았습니다** (`<제1저자성><년도>_<제목낱말>`)
- 중복 판정은 papers/ **전수**로 합니다 — INDEX 로 하면 샙니다(인덱스가 셋입니다)
- 파일명 slug **와** 본문 DOI 를 둘 다 훑습니다 (같은 논문을 두 세션이 각자 digest 한 전례가 있습니다)
- **기존 카드를 절대 덮어쓰지 않습니다**
- `INDEX.md` 는 **건드리지 않습니다** — 손으로 쓴 분석 산문이라, 대신 `_INDEX_proposals.md` 에 제안만 남깁니다
- 실물 없이 채운 칸은 `⏳ 문서 대기` 이고 status 는 `🌱 skeleton` 입니다 — **본 것과 안 본 것을 구분**합니다

테스트 6건(양성 1 · **음성 5**). 전체 스위트 **18 passed**.

---

## 5. 하지 않은 것 (금지 항목 · 그대로 지켰습니다)

- ❌ `.env` 에 비밀번호 — **만들지 않았습니다** (repo 에 없습니다)
- ❌ Scholar alert 등록·변경
- ❌ vault 폴더 구조 변경 (제안만)
- ❌ `litdb/` 수정 (어댑터만 붙였고 실물 카드는 안 건드렸습니다)
- ❌ 두 브랜치 merge

⚠ **git push 는 했습니다.** 이 컨테이너가 휘발성이라 push 안 하면 작업이 사라지고,
repo CLAUDE.md 와 stop hook 이 커밋·푸시를 요구합니다. 사용자에게 매번 알렸고
되돌리길 원하시면 말씀해 주십시오. 브랜치는 `claude/friendly-meitner-lldvar` 하나뿐입니다.

---

## 6. 그쪽에 부탁드리는 것

1. **§3 의 dry-run 버그** — 고치실지 알려 주십시오. 제가 해도 됩니다.
2. **분석 큐** — `data/analysis/pending/` 가 비어 있습니다. 다음 NOON 에서 채워 주시면
   이쪽에서 `paper-analyst` 로 돌리고 `ra vault && ra litdb` 까지 태우겠습니다.
3. **litdb 실물 카드** — 지금 어댑터는 skeleton 만 만듭니다. 사용자가 PDF 를 주면
   그때 `litdb-curator` 로 본문을 채우는 흐름입니다. 그쪽에서 초록 이상을 확보하시면
   `evidence_level` 을 올려서 `[RA-HANDOFF]` 로 보내 주십시오 — 충돌 규칙대로
   `fulltext > abstract > snippet > title` 로 이쪽이 병합합니다.
4. **축 C 를 프로필에 반영한 채로** 채점해 주십시오 (§1 끝).

---

## 7. 읽으실 때 지켜 주실 규율 (repo CLAUDE.md 에서)

- **프로필이 유일한 근거**입니다. 비어 있으면 연결점을 **지어내지 마십시오** —
  CHANGELOG 에 그쪽이 직접 쓰신 원칙이고 맞습니다.
- **문헌 수치는 소환값**입니다. 우리 db 의 절대값과 **섞지 마십시오**
  (방법 명시 없이 이식 금지).
- 밴드갭은 **fixed-occupations nscf 의 VBM/CBM 고유값만** 인정합니다.
  DOS-threshold 로 읽은 논문은 무관이 아니라 **비판 대상**입니다(~0.3 eV 과소).
- MD σ 는 **절대값 인용 금지**, 비율도 멀티시드 판정만 (단일시드 1.33× 철회 사례).
- 같은 이유로 **단일 시드 MD 로 σ 비를 주장한 논문**, **NEB 를 셀 수렴 없이 절대값으로
  인용한 논문**도 비판 포인트입니다 — 우리가 그 함정을 각각 규율로 닫았기 때문에
  세미나·리뷰어 관점에서 값어치가 큽니다.

---

## 부록 — 이번에 바뀐 파일

| 파일 | 무엇 |
|---|---|
| `config/research_profile.md` | STUB → FILLED (캠페인 11개 · 축 C 추가 · 확보값 표) |
| `config/agent.yaml` | litdb `file` → **`markdown`** · `markdown_dir` |
| `research_agent/triage.py` | `_TERMS` 에 캠페인 용어 보강 + Zn 상쇄 규칙 |
| `research_agent/exporters/litdb.py` | markdown 어댑터 (`export_markdown`) |
| `tests/test_litdb_markdown.py` | 신규 6건 (음성 5) |
| `tests/test_triage_db.py` | 캠페인 용어 4건 추가 (음성 3) |
| `cowork/HANDOFF_PROMPT.md` | 신규 — 연구자·축·캠페인 브리핑 |
| `vault/Digests/2026-09-04.md` | **tarball 에서 복원** (164줄) |
