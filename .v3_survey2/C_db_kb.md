# v3_survey2 — 조사 C: db/ · kb/ (값 원장 · 문서)

⚠ **이 보고는 전달 도중 끊겼다.** 마지막 항목([주의] lpscl_vs_lpscl16_FULL_report…)이 문장 중간에서
잘렸고, 그 뒤에 있었을 나머지 발견 · "못 본 것" 절 · "이 영역이 활성인가" 절은 **여기 없다**.
아래는 받은 데까지 그대로다. 종합 시 이 영역은 **불완전 보고**로 취급해야 한다.

읽음 78/501 — 본문 26 · 헤더·grep 52 · 안 봄 423 (별도로 db 전체 JSON 은 키패턴·경로참조를 기계 스캔했고, kb 379 문서는 `kb_wiki.py lint` 로 전수 통과시켰다. 그건 "읽음" 에 안 넣었다)

---

```
[치명] db/compositions/*.json 의 band_gap_eV — DOS-threshold 폐기값이 살아 있는 키에 그대로 있다
· 어디: db/compositions/comp3.json:25 · comp4.json:25 · comp5.json:36 · modelc_v3.json:227
        (comp1.json:39 · modelc.json:24,30 은 옆에 _DEPRECATED 노트만 붙어 있고 키는 그대로)
· 무엇: 조용히 틀린다. `d["band_gap_eV"]` 를 읽는 사람·에이전트는 CLAUDE.md 가 금지한
  DOS-threshold 판독값을 받는다. modelc.json 은 **1.65** 인데 canonical 은 2.099 — 0.45 eV 과소,
  CLAUDE.md 가 적어 둔 "~0.3 eV 과소" 실패 양식 그대로다. comp1 은 2.28/2.25 vs canonical 2.066.
  comp3(2.10)·comp4(1.96)·comp5({basin_A 1.77, basin_B 2.06})·modelc_v3(1.80) 은 **경고 문구가 아예 없다.**
  ⚠ 화면 문제는 아니다 — `grep -rn band_gap_eV webapp/` 는 0건이고, `load_compositions()`
  (webapp/data.py:99) 가 딕셔너리를 통째로 넘기기만 한다. 위험은 db 를 직접 읽는 경로다.
· 근거:
    comp1.json:39  "band_gap_eV": {"v1": 2.28, "v2": 2.25, ...}
    comp1.json:44  "_DEPRECATED_band_gap_eV": "v1 2.28 / v2 2.25 는 DOS-threshold 판독값이라 폐기 …"
    modelc.json:30 "band_gap_eV": 1.65,
    modelc_v3.json:227  "band_gap_eV": 1.80,     ← 노트 없음
  canonical_registry gap_eV 등재는 comp1 2.066 · modelc 2.099 · b2o3 1.9671 · lpsocl 2.2309 ·
  comp2 2.04(provisional) 뿐이다 — comp3/4/5 는 **대체할 canonical 이 없다.**
· 고치는 법: 2026-09-07 에 `Ea_eV_USABLE_segment_600_800 → …_NON_CITABLE_2026_09_07` 로 한 것과
  같은 처방을 쓴다. 키 이름을 `band_gap_eV_DOS_THRESHOLD_DEPRECATED` 로 바꾸고(노트 추가가 아니라
  키 개명이라야 조용한 오독이 막힌다), comp3/4/5 는 "canonical 없음 — 이 방법은 인용 금지" 를
  값 옆에 적는다. comp2 2.04 는 레지스트리 provisional 과 같은 값이라 유지하되 근거를 명시.
```

```
[치명] 마감된 b2o3 MD 축의 판정문이 db/properties/b2o3_vs_modelc_md.json 에 표식 없이 살아 있다
· 어디: db/properties/b2o3_vs_modelc_md.json  (uncited — 어젯밤 조사가 열지 않은 파일)
        comparison.verdict · comparison.Ea_verdict · b2o3_doped 블록 전체
· 무엇: 조용히 틀린다. 이 파일의 **SUPERSEDED 접미사가 안 붙은** 키들이 마감 카드가 금지한
  주장을 그대로 말한다. 영문 산문이라 결속 매처의 forbidden_phrases 도 못 잡는다.
· 근거 (파일 원문):
    "verdict": "B2O3 PRESERVES Li conductivity vs LPSCl1.6 (3-seed x 3-T: per-T sigma ratio
                1.08+-0.18 / 0.82+-0.15 / 1.15+-0.12 = statistically equivalent) …"
    "Ea_verdict": "b2o3 and modelc have IDENTICAL Ea (0.223 eV) at the consistent 2-50 ps window."
    "b2o3_doped": { … "D_300K": 1.2547e-07, "sigma_300K_mS_cm": 18.51, "sigma_273K_mS_cm": 8.65 }
  대조 — b2o3_md_closed_retrospective_2026_08_25.json (ratified 2026-09-07) 금지_서술:
    "b2o3 의 D · Ea · sigma · 구간 Ea 중 어느 것도 물질 값으로 인용 — 0.222 eV 포함."
    "b2o3 vs modelc 의 수송 비교·순위·기전 주장"
    "이 축의 어떤 값이든 300 K 로 외삽."
  HZ-sigma-ratio-non-citable(BLOCKED) 의 forbidden_phrases 는 `conductivity_preserved` ·
  `전도도 보존` · `통계적으로 동등` — 이 파일의 "PRESERVES" · "statistically equivalent" 는 안 걸린다.
  HZ-cross-system-Ea(BLOCKED) 가 계간 Ea 비교를 막는데 Ea_verdict 가 정확히 그것이다.
  ★ **자매 파일과 어긋난다**: 똑같은 숫자 D_300K 1.2547e-07 · sigma300 18.51 · sigma273 8.65 를
  b2o3_md_arrhenius.json 은 `…_RETRACTED_2026_08_24` 로 키를 개명해 뒀는데 여기는 안 했다.
· 고치는 법: (a) `verdict`·`Ea_verdict` 를 `verdict_NON_CITABLE_2026_09_07` 로 개명하고
  마감 결정 ID(D-2026-09-07-b2o3-md-closure-retrospective)를 값 안에 박는다.
  (b) `b2o3_doped` 의 D_300K·sigma_300K·sigma_273K 를 자매 파일과 같은 접미사로 통일.
  (c) citation_hazards 의 FP 에 영문형 `"PRESERVES Li conductivity"` · `"statistically equivalent"` 를
  추가할지는 오탐 위험이 있으니 1저자 판단 — 최소한 `binding_scope_why` 에 "영문 산문 미포함" 을 적어야 한다.
```

```
[치명] b2o3_md_arrhenius.json — 개명한 USABLE 키 옆에 같은 종류가 다섯 개 더 남아 있다
· 어디: db/properties/b2o3_md_arrhenius.json
        FINAL_for_paper (키 이름 자체) · .Ea_eV · .D_per_T_cm2_s · .D0_cm2_s
        .segment_extrapolation_2026_08_24.{Ea_eV, D_300K_cm2_s}
        RETRACTED_2026_08_23.usable
· 무엇: 조용히 틀린다. 2026-09-08 에 `Ea_eV_USABLE_segment_600_800` 하나만 개명했는데,
  같은 파일 안에 표식 없는 형제가 남았다. `FINAL_for_paper.Ea_eV` = **0.2234** 가 아무 접미사 없이
  "논문용 최종" 이라는 이름의 블록에 앉아 있다. 레지스트리에도 이 키는 등재돼 있지 않아
  (`MD_Ea_eV_singleseed@b2o3` 의 source_key 는 lpsocl_md_arrhenius.json 쪽이다)
  **레지스트리 쪽 citable:false 가 이 키까지 못 덮는다.**
· 근거 (파일 원문 발췌):
    "FINAL_for_paper": { "Ea_eV": 0.2234, "D0_cm2_s": 0.0007112,
                         "D_per_T_cm2_s": {"600": 9.174e-06, "800": 3.009e-05, "1000": 5.067e-05},
                         "D_300K_cm2_s_RETRACTED_2026_08_24": "…",     ← 이건 개명됨
                         "Ea_eV_segment_600_800_NON_CITABLE_2026_09_07": "…" }  ← 이것도 개명됨
    "segment_extrapolation_2026_08_24": { "Ea_eV": "0.2241 +/- 0.0606 …",   ← 표식 없음
                                          "D_300K_cm2_s": "2.6018e-07 …",   ← 표식 없음
                                          "sigma_300K_mS_cm": "38.39 … 인용 금지" }  ← sigma 만 표식
    "RETRACTED_2026_08_23": { "usable": "600→800 구간 Ea = 0.222 eV (단일시드 옛 값 0.2234 와
                                            거의 같다 — 저온 구간은 처음부터 맞았다)" }
  → `usable` 키가 마감 카드가 이름을 대서 금지한 그 값("0.222 eV 포함")을 **권하고 있다.**
  이건 레지스트리에서 고친 `usable_instead` 문제(Codex BI P0-1)와 정확히 같은 버그인데
  **원자료 쪽에 같은 문장이 남아 있는 것**을 아무도 안 봤다.
· 고치는 법: `usable` → `superseded_usable_2026_09_07` + sentinel(`{none:true, decision:"D-2026-09-07-…"}`);
  `FINAL_for_paper` → `FINAL_for_paper_RETIRED_2026_08_25`; 그 안의 Ea_eV·D0_cm2_s·D_per_T_cm2_s 와
  segment_extrapolation 의 Ea_eV·D_300K_cm2_s 에 `_NON_CITABLE_2026_09_07` 접미사.
```

```
[주의] 폐기된 beta 0.80 하드게이트가 db 여섯 파일에서 살아 있는 인용 규칙으로 쓰인다
· 어디: db/properties/li_transport.json:320 · comp2_md_arrhenius.json:85 ·
        lpsocl_md_arrhenius.json:118 · b2o3_md_arrhenius.json:96 · b2o3_vs_modelc_md.json:86
        (다섯 개가 **한 글자도 다르지 않은 같은 문자열**) + md_traj_inventory.json:7 (필드 정의)
· 무엇: 조용히 틀린다. 문턱이 폐기된 뒤에도 이 필드가 값의 인용 가부를 선언한다.
  방향이 한쪽만도 아니다 — beta-gate 카드 §7-6 이 "문턱을 내리면 통과했던 것도 무효다" 라고
  양방향임을 못박았으므로, 이 문장을 믿고 "보류" 한 값도 "통과" 한 값도 근거가 없다.
· 근거:
    DIFFUSIVE_GATE_2026_08_01: "… MSD 창 2-50 ps 의 log-log 기울기 beta 가 0.8 미만이면
      케이지 진동을 확산으로 오독한 것이다 … 같은 프로토콜로 낸 Ea 는 …
      게이트를 통과하기 전까지 **인용 보류**."
  대조 — kb/methodology/beta_gate_seed_policy.md 배너(2026-09-09):
    "SUPERSEDED — beta 0.8–1.2 하드게이트는 2026-08-26/27 폐기됐다 …
     현행 판정축: D_inc plateau · 창 안정성 · 실제 독립 hop 수"
  citation_hazards HZ-beta-hard-gate 는 SUPERSEDED 이고 forbidden_phrases 가
  `["beta >= 0.80","베타 하드게이트","beta 하드게이트"]` 인데 — **이 여섯 곳의 표현 "beta 가 0.8 미만" 은
  그 목록에 안 걸린다.** 기계가 못 잡는 자리다.
· 고치는 법: 다섯 파일의 필드를 `DIFFUSIVE_GATE_2026_08_01_SUPERSEDED_2026_08_27` 로 개명하고
  본문에 현행 판정축(D_inc plateau · 창 4개 · hop 수)과 kb/concepts/beta-gate.md §7-8e 를 가리키게 한다.
  md_traj_inventory.json:7 의 `diffusive_beta` 정의는 "beta<0.8 이면 케이지" 를 빼고
  "기록·경보용, 판정축 아님" 으로. FP 에 `"beta 가 0.8 미만"` 추가 검토.
```

```
[주의] kb/results/bvse_3system_conclusions_2026_07_21.md — 배너 없이 금지값을 "교체값" 으로 권한다
· 어디: kb/results/bvse_3system_conclusions_2026_07_21.md:31, 37  (uncited · git 2026-07-21)
· 무엇: 조용히 틀린다. 형제 b2o3 문서 여덟 개는 전부 상단에 경고 배너를 달았는데 이 파일만 없다.
  그리고 하필 **철회된 서사를 무엇으로 바꿀지 지시하는 표** 라, 읽는 사람이 그대로 옮겨 쓴다.
· 근거 (본문 원문):
    31: | "MD 정합: sigma 1.33x, 같은 Ea 0.223 …" | 폐기 — 단일시드 산물 (2026-07-09 철회).
        **교체: 멀티시드 sigma 비율 1.08/0.82/1.15 = 동등, Ea 0.199+-0.034 ~ 0.197+-0.032** |
    37: 그러나 Ea는 단조가 아님: 0.197+-0.032 → 0.271+-0.033 → 0.199+-0.034 (동등).
  "교체" 로 제시된 두 값이 지금 각각 HZ-sigma-ratio-non-citable(BLOCKED)와
  MD_Ea_eV@b2o3(status: retracted, usable_instead = sentinel none)이 막는 값이다.
· 고치는 법: kb/results/b2o3_*.md 여덟 개와 같은 배너 블록을 상단에 복사해 넣고,
  31행 "교체:" 이하와 37행의 0.199 를 취소선 처리 + `db/properties/b2o3_md_closed_retrospective_2026_08_25.json` 링크.
  ⚠ 이 문서를 가리키는 곳은 kb/results/session_handoff_2026_07_22.md:12 와 kb/index.md 둘뿐이고,
  그 핸드오프 12행도 같은 "Ea 비단조 0.197→0.271→0.199" 문장을 그대로 복제하고 있다 — 같이 고쳐야 한다.
```

```
[주의] kb/results/lpscl_vs_lpscl16_FULL_report_2026_06_17.md — 방법 오표기(AIMD) + 금지된 절대 sigma·계간 Ea
· 어디: 같은 파일 :17, :18, :19, :59, :62, :89, :106, :26, :84  (uncited · git 2026-…)
· ⚠ **여기서 보고가 끊겼다.** 이 항목의 무엇/근거/고치는 법과, 이 뒤의 모든 발견,
  그리고 "못 본 것" · "이 영역이 활성인가" 두 절을 **받지 못했다.**
```

---

## 못 본 것 — 무엇을 안 읽었고 왜

원 보고의 이 절은 **전달되지 않았다**. 확실한 것은 보고 첫 줄이 스스로 적은 수치뿐이다:
**읽음 78/501 — 본문 26 · 헤더·grep 52 · 안 봄 423.** 즉 db/kb 영역의 약 84 % 가 미독이다.
db 전체 JSON 은 키패턴·경로참조 기계 스캔만, kb 379 문서는 `kb_wiki.py lint` 전수 통과만 했고
둘 다 "읽음" 으로 세지 않았다.

## 이 영역이 활성인가 — 어떻게 판단했나

원 보고의 이 절도 **전달되지 않았다**. 다만 본문 발견이 2026-09-07 ratify 된 마감 카드
(b2o3_md_closed_retrospective_2026_08_25.json)와 2026-09-08/09 의 키 개명 작업을 직접
대조하고 있으므로, 이 영역이 이번 주에 손대고 있는 활성 영역이라는 것은 본문에서 읽힌다.
