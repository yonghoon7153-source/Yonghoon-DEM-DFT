# 아카이브 — DEM 분석 스킬 2편 (2026-09-18 이관)

옛 위치 `skills/` (지금은 없는 디렉터리) 의 `dem-analysis-standard.md` ·
`dem-analysis-bimodal.md` 를 여기로 옮겼다.
⚠ 옛 경로를 코드표기로 적지 않는다 — `check_doc_refs.py` 가 **실재하지 않는 참조**로
  잡는다 (실제로 잡혔다, 2026-09-18).  이력은 `git log --follow` 로 따라간다.
**지우지 않는다** — 이력이고, 문턱값이 어디서 왔는지 나중에 밝혀질 수 있다.

## 왜 옮겼나 (원장 `GAP3-DOC` ㉟, 2026-09-18)

**이것은 "문턱이 틀린 문서" 가 아니라 유령 문서다.**  넷 다 실측이다:

1. **배선이 없다.**  `.claude/skills/` 디렉터리가 **아예 없다** — Claude Code 가 스킬로 읽는
   자리가 아니다.  리포에서 이 파일들을 참조하는 곳은 **감사 기록 4 개뿐**이고 운영 경로 0 건이다.
2. **워크플로가 실행 불가다.**  두 문서가 시키는 스크립트 중 **standard 7 중 5 · bimodal 6 중 4**
   가 리포에 없다:
   · standard MISSING — `generate_figures.py` · `advanced_analysis.py` ·
     `generate_advanced_figures.py` · `deep_electrode_analysis.py` · `thick_electrode_analysis.py`
   · bimodal  MISSING — `advanced_analysis_bimodal.py` · `bimodal_specific_analysis.py` ·
     `generate_advanced_figures_bimodal.py` · `generate_figures_bimodal.py`
3. **2026-04-24 `chore: import full codebase` 이후 한 번도 갱신되지 않았다.**
4. **문턱에 출처가 없고, 생산 스크립트와 정면 충돌한다** — 그것도 **이 문서가 직접 실행하라고
   시키는** `scripts/analyze_contacts.py` 와:

   | 양 | 이 스킬 (같은 폴더 `dem-analysis-standard.md`) | `scripts/analyze_contacts.py:471,490` |
   |---|---|---|
   | SE-SE CN | `> 2.4` = 퍼콜 문턱 (OK) | `< 3.5` = **critical** |
   | SE 퍼콜 % | `> 70` = "Good" | `< 85` = **critical** · `< 95` = warning |

   ⇒ CN 2.7 · 퍼콜 75 % 침대가 2 단계에서 **"좋음"**, 3 단계에서 **critical 두 개**가 된다.
   ⚠ `CLAUDE.md:1878` 은 같은 `CN=2.7` 을 *"below typical percolation threshold"* 라 부른다
     (그 `CN` 이 SE-SE CN 임은 `generate_comparison_plots.py:4599` 에서 확인).

## 고치지 않고 **옮긴** 이유

살아 있지 않은 문서의 문턱을 고치면 *"고쳤으니 이제 맞다"* 는 **잘못된 신뢰**가 생긴다.
배선도 스크립트도 없는 문서는 고쳐도 아무것도 달라지지 않는다.

⚠⚠ **그러나 진짜 문제는 남았다 — 생산 쪽 문턱에도 출처가 없다.**
`analyze_contacts.py` 의 `3.5` / `85` / `95` 는 **주석뿐이고 전거가 없다**.  그 코드는 실제로
돌고 사용자에게 `critical` 경고를 띄운다.  ⇒ *"스킬을 생산에 맞추면 된다"* 가 **자동 정답이
아니다** (생산 쪽이 틀렸을 수도 있다).  그 항목은 원장에 **따로 열었다** — `GAP3-40`.

## 되살리려면
① 결측 스크립트 9 개를 복원하거나 워크플로를 현존 스크립트로 다시 쓴다
② 문턱에 전거를 붙인다 (`GAP3-40` 이 먼저 닫혀야 한다)
③ `.claude/skills/` 로 실제 배선한다
셋 다 하지 않을 것이면 여기 두는 것이 정직하다.
