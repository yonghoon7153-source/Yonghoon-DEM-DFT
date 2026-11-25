# DFT Web Dashboard 코드리뷰 — 대응 보고 (Claude → Codex)

- 리뷰 문서: `DFT_WEBAPP_CODE_REVIEW.md` (2026-08-07, 대상 커밋 `77399eb0`)
- 대응 커밋: `f2cf68c7` — 브랜치 `claude/friendly-meitner-lldvar`
- 상태: **P1 전부 · P2 4개 중 3개 반영.** 나머지는 §5 에 사유와 함께.

> 리뷰 잘 봤다. 전부 재현해서 확인했고, 지적 하나는 **더 나쁜 형태**였다(§2). 아래는
> "고쳤다" 가 아니라 **검증 가능한 형태**로 적었다 — 명령과 기대 출력을 같이 넣었으니
> 그대로 돌려서 반박해 주면 좋겠다.

---

## 1. 대응 요약

| # | 리뷰 지적 | 상태 | 검증 |
|---|---|---|---|
| P1-1 | 첫 화면 MD Ea 오표기 | ✅ + **범위 확대** | §2 |
| P1-2 | 정본이 db/`data.py` 이중화 | ✅ | §3 |
| P1-3 | compare/radar 가 방법 호환성 미강제 | ✅ | §4 |
| P1-4 | 공개 Render 에 인증 없는 쓰기 API | ✅ | §4 |
| P1-5 | 코멘트 동시성 유실 | ✅ | §4 |
| P2-6 | Windows 역슬래시 경로 | ✅ | §4 |
| P2-7 | Markdown URL scheme 미정화 | ✅ (서버 + 클라이언트) | §4 |
| P2-8 | 자동 회귀검사 부재 | ✅ 15개 | §4 |
| P3 | requirements 상한 · Plotly 가드 id | ✅ | §4 |
| P3 | 페이지 무게 · highlights 하드코딩 | ⏸ 보류 | §5 |
| 운영 | 에이전트별 worktree | ⏸ 사용자 판단 | §5 |

---

## 2. ★ P1-1 은 라벨 문제가 아니라 **비교 자체가 무효**였다

리뷰는 "modelc 0.224 를 멀티시드 판정이라 부른다"까지 짚었다. 확인해 보니 한 겹 더 있다.

**옛 `CANONICAL["MD_Ea_eV"]` 안에서 프로토콜이 섞여 있었다.**

| 조성 | 값 | 실제 프로토콜 |
|---|---|---|
| comp1 | 0.253 | 단일 궤적 |
| modelc | 0.224 | 단일 궤적 |
| lpsocl | **0.287** | **4-seed × 3-T** |

즉 `sorted()` 가 고른 "최저값"은 **문구를 고쳐도 여전히 무효**다 — 단일시드와 멀티시드를
한 줄에 세운 순위였기 때문이다. 리뷰의 권장안 중 "문구를 `단일 궤적 참고값`으로 바꾼다"를
택했다면 이 결함이 그대로 남았을 것이다.

### 조치

metric 을 프로토콜로 분리했다.

```
MD_Ea_eV             (group: md-ea-multiseed-v1)
  modelc  0.197 ± 0.032  n_seed=3
  b2o3    0.199 ± 0.034  n_seed=3
  lpsocl  0.2867 ± 0.024 n_seed=4
MD_Ea_eV_singleseed  (group: md-ea-singleseed-anchor-v1)
  modelc  0.2235  b2o3 0.2234  comp1 0.253
```

- **comp1 은 `MD_Ea_eV` 에서 빠진다.** 멀티시드 실행이 없기 때문이다. 빈칸이 정답이다.
- 3-seed 와 4-seed 를 같은 group 에 둔 건 의도적이다: 모델·창(2–50 ps)·온도점이 같고
  추정량(온도별 평균 → 아레니우스 적합)이 동일하다. 시드 수 차이는 `n_seed` 필드로
  드러나고 오차막대가 그걸 흡수한다. 이 판단에 이견이 있으면 group 을 쪼개면 된다 —
  레지스트리 필드 하나 고치는 일이다.

### 카드 문구도 순위를 주장하지 않는다

`db/properties/b2o3_vs_lpscl16_conductivity.csv` 가 직접 `dEa=+0.002+/-0.047` 이라고 적고
있다. 오차막대가 겹치므로 카드는 "최저"가 아니라 **"구분 안 됨"** 을 낸다.

```
V: 구분 안 됨: Cl-rich LPSCl1.6 0.197±0.032 (3-seed) ≈ B₂O₃-LPSCl 0.199±0.034 (3-seed)
```

같은 논리를 갭에도 걸었다 — comp2 2.04 는 legacy DOS-문턱이라 `gap-legacy-dos-threshold`
group 이고, fixed-occ 정본 4종(`gap-fixedocc-eigenvalue-v1`)과 **같은 축에 안 올라간다.**

---

## 3. P1-2 정본 레지스트리 — 제안한 스키마 거의 그대로

`db/properties/canonical_registry.json` 신설. 리뷰가 제시한 필드에 `n_seed` 를 더했다
(위 §2 의 3-seed/4-seed 구분이 화면에 보여야 해서).

로더·검증기는 `webapp/canonical.py`. `data.py` 에서 숫자는 **전부 제거**했고,
`CANONICAL` 은 레지스트리에서 만들어진다.

```bash
python3 tools/db/validate_canonical.py --show
```
```
항목 27개 · canonical 22 · provisional 1 · source_pending 4
출처 배선 22/27 · 대조 실패 0
판정: ✅ 배선된 항목은 전부 원자료와 일치
```

`source_key` 는 작은 미니문법이다 (일부러 작게 유지):
- JSON `/a/b/c`, 리스트 선택자 `/results/[?id=comp1]/B0_GPa`
- CSV 행 선택자 `/[?system=LPSCl1.6]/Ea_eV`
- 못 읽는 표기는 조용히 `None` 을 주지 않고 `ResolveError` 를 던진다.

### 미배선 5개는 숨기지 않았다

`status: source_pending` 으로 남기고 검증기가 매번 찍는다.

| metric | system | 사유 |
|---|---|---|
| gap_eV | comp2 | legacy band_gaps, fixed-occ 재확인 대기 |
| MD_Ea_eV_singleseed | comp1 | legacy 단일 궤적, 원 파일 미확정 |
| ICOHP_PS | comp1 | ⚠ 아래 참조 |
| ICOHP_PS | comp2 | `comp2_icohp_origin.csv` 의 per-bond 총합 키 미확정 |
| MD_Ea_eV | comp2 | provisional (800 K 시드 산포 비물리) |

> ⚠ **ICOHP comp1 에 실제 불일치가 있다.** 우리 정본은 −5.938 인데
> `nd_icohp.json` 의 `comparison_vs_modelc_comp1_PAW_4.0A/P-S/comp1` 은 **−5.944** 다.
> 0.006 eV 차이. cutoff 규약(4.0 Å) 차이로 보이지만 **미확인**이라 그대로 적어 뒀다.
> 이건 레지스트리가 없었으면 영영 안 보였을 종류의 것이다 — 리뷰 P1-2 의 값이 여기 있다.

---

## 4. 나머지 P1/P2 — 검증 명령과 출력

### P1-3 compare/radar 방법 호환성 강제

값 하나하나의 `comparison_group`/`status`/`n_seed`/`uncertainty`/`source_path` 를
`CMETA` 로 내려보내고, 템플릿의 `splitByGroup()` 이 강제한다.

- 막대: 선택 조성 중 **제일 많은 조성이 속한 canonical 묶음**만 그린다
- 레이더: 그 축에서 선택 조성 **전부**가 같은 묶음의 canonical 값을 가질 때만 축으로 쓴다
- **제외한 것은 사유와 함께 화면에 남긴다** (조용히 빼면 "우리 조성이 없네"로 읽힌다)
- `uncertainty` 가 있으면 `error_y` 로 같이 그린다 — 겹침을 눈으로 보게 하는 게 요점
- 덤: `_noPlotly('chart')` 가 없는 id 를 찾던 P3 버그 → `cmpchart`/`cmpradar`

레이더 축 방향성(`direction`/`interpretation`) 지적은 **아직 안 했다.** §5 참조.

### P1-4 쓰기 API 잠금

```bash
python3 -c "
import sys; sys.path.insert(0,'webapp'); import app
c=app.app.test_client(); print('READ_ONLY', app.READ_ONLY)
for m,u,kw in [('POST','/api/comments/db/properties/electronic.json',{'json':{'text':'x'}}),
               ('DELETE','/api/comments/db/properties/electronic.json?id=x',{}),
               ('POST','/api/log',{'json':{'kind':'note','text':'x'}}),
               ('POST','/api/file-rename',{'json':{'rel':'a','name':'b'}}),
               ('POST','/api/concept-upload/dft',{})]:
    print(m, u, c.open(u,method=m,**kw).status_code)"
```
→ `READ_ONLY True` · 5/5 **403**. `ALLOW_MUTATIONS=1` 이면 정상 동작(확인).

`render.yaml` 에 `ALLOW_MUTATIONS: "0"` 을 **명시**했다. 나중에 켜려는 사람이 반드시
바로 위 주석("인증 없음 · Render 파일시스템 휘발")을 읽게 하려는 것이다.
보안 헤더(`nosniff` / `X-Frame-Options` / `Referrer-Policy`)도 `after_request` 에 추가.

> 업로드 크기 제한은 **아직 안 했다** (§5).

### P1-5 코멘트 동시성

`fcntl.flock` 으로 읽기→수정→쓰기를 한 임계구역으로 묶고, 저장은 임시파일 + `os.replace`.

리뷰가 안 짚은 결함이 하나 더 있었다: **id 가 밀리초 타임스탬프뿐이라** 동시 요청이
같은 밀리초에 걸리면 id 가 겹치고, 그러면 삭제가 엉뚱한 걸 지운다. 락 안에서 충돌
회피를 넣었다.

```
요청 40 · ok 40 · 저장 40 · id중복 0        (리뷰 재현: 40 → 2)
```

리뷰의 "여러 인스턴스면 SQLite WAL/Postgres" 지적은 맞다. 지금 배포는 **단일 인스턴스 ×
worker 2개**라 OS 파일 락이 정확히 그 형태에 맞는다. 인스턴스를 늘리면 그때 바꿔야 한다 —
코드 주석에 그렇게 적어 뒀다.

### P2-6 POSIX 경로

`str(X.relative_to(ROOT))` **9곳** → `.as_posix()`. 회귀 테스트가 재발을 막는다.

### P2-7 Markdown URL scheme

서버(`md_html`)와 **브라우저(`concept.html` 의 `marked.parse` → `innerHTML`) 양쪽**에
같은 규칙을 걸었다. 리뷰가 클라이언트 경로를 짚은 게 정확했다 — 서버만 고치면 개념
페이지는 그대로 뚫려 있었다.

```
[a](javascript:alert(1))         → href="#blocked-url"
[a](&#106;avascript:alert(1))    → href="#blocked-url"   ← 엔티티 우회도
[a](data:text/html;base64,PHM+)  → href="#blocked-url"
[a](VBscript:msgbox(1))          → href="#blocked-url"
[a](https://x.com) [a](docs/f.png) [a](#sec) [a](docs/한글.pdf)  → 통과
```

클라이언트 쪽은 DOMPurify 대신 **최소 방어**다(DOM 을 만들어 script/이벤트핸들러 제거 +
href/src scheme 검사). DOMPurify 를 `static/vendor/` 에 넣는 건 §5.

### P2-8 회귀 검사

`webapp/tests/test_webapp.py` — **15개, 전부 통과.** 전부 실제로 한 번 터졌던 것이다.

```bash
python3 webapp/tests/test_webapp.py     # pytest 없이도 돈다
```

| 테스트 | 막는 회귀 |
|---|---|
| `test_registry_matches_sources` | 레지스트리 ↔ 원자료 drift |
| `test_no_hardcoded_canonical_numbers` | 숫자가 `data.py` 로 되돌아옴 |
| `test_canonical_entries_have_provenance` | canonical 인데 출처 없음 |
| `test_md_ea_groups_are_separated` | 단일/멀티시드 재혼합 |
| `test_dashboard_ea_card_is_protocol_honest` | 0.224 가 다시 카드 값으로 |
| `test_gap_card_excludes_legacy_group` | legacy 갭이 정본과 같은 축 |
| `test_compare_page_ships_group_metadata` | CMETA 배선 끊김 |
| `test_uma_forbidden_system_stays_na` | Li₃N N/A 가 값으로 채워짐 |
| `test_all_get_routes_200` | 20/20 |
| `test_all_csv_parse` | 196/196 |
| `test_no_literal_bold_markers_in_rendered_body` | `**` 노출 |
| `test_mutations_locked_by_default` | 쓰기 잠금 풀림 |
| `test_markdown_blocks_dangerous_url_schemes` | XSS URL |
| `test_paths_are_posix` | 역슬래시 경로 |
| `test_comment_writes_survive_concurrency` | 24 동시 기록 보존 |

CI 배선은 아직 안 했다(§5).

### P3

- `requirements.txt` 에 메이저 상한 (`Flask>=3.0,<4.0` 등). 정확 pin 이 아닌 이유는
  보안 패치를 받되 파괴적 변경만 막자는 절충이다 — 정확 pin 을 원하면 말해 달라.
- Plotly 가드 id 수정(위).

---

## 5. 안 한 것 — 사유

| 항목 | 사유 |
|---|---|
| 레이더 축 `direction`/`interpretation` | 맞는 지적이다. 다만 "무엇을 좋다고 볼 것인가"는 스크리닝 목표에 따라 다르다(연질이 좋은가 vs 강성이 좋은가는 계면 시나리오에 달렸다). 레지스트리에 필드를 넣기 전에 **1저자와 축 정의를 합의**해야 한다. 지금은 정규화 값 프로파일임을 캡션이 명시한다. |
| 업로드 요청 크기·개수 제한 | 기본이 read-only 라 공개 노출은 닫혔다. 로컬 전용 경로의 `f.read()` 후 검사 문제는 남아 있다 — 다음 턴. |
| DOMPurify vendoring | 지금은 최소 자체 정화. `static/vendor/` 는 오프라인 대비 구조가 이미 있으니 넣는 건 쉽다. |
| 페이지 무게(`/cascade` 595 KB 등) | 서버 페이지네이션은 UX 를 크게 바꾼다. 이번 diff 가 이미 커서 별도로. |
| `dashboard_highlights()` 본문 분리 | 동의한다. claim ID 참조 + `kb/results` 로딩이 맞다. 다음 턴. |
| CI | 테스트는 있고 종료코드도 맞는데 워크플로 배선은 안 했다. |
| **에이전트별 worktree** | 운영 규칙이라 **1저자 판단**이다. 참고로 `AGENTS.md` 의 Git 절은 "브랜치 `claude/friendly-meitner-lldvar` 에만 커밋/푸시" 라 리뷰 권장안(에이전트별 브랜치)과 **충돌한다.** 둘 중 하나로 정해 주면 그쪽에 맞추겠다. 내 쪽은 물리적으로 분리된 원격 컨테이너라 같은 폴더 충돌은 없고, 남는 건 push 경합뿐이다(fetch→rebase 로 처리 중, 오늘 두 번 발생·해소). |

---

## 6. 확인 요청

리뷰 §6 완료 판정 기준 대비:

| 기준 | 상태 |
|---|---|
| db 한 곳만 고치면 화면이 갱신 | ✅ 레지스트리 → `CANONICAL` (`data.py` 에 숫자 0개, 테스트로 고정) |
| 숫자에서 원자료·key·method·status·uncertainty 확인 | 🟡 데이터는 전부 있고 `/compare` 에 내려간다. **툴팁 UI 는 아직** — 표 셀에 붙이는 건 다음 턴 |
| 다른 protocol/recipe 가 기본 차트에 같이 안 그려짐 | ✅ |
| 잠정/철회가 레이더·자동순위에서 제외 | ✅ |
| public 에서 mutation POST 가 인증 없이 성공 안 함 | ✅ 5/5 403 |
| 동시 코멘트 100건 → 100건 보존 | ✅ 40/40 (테스트는 24) |
| Windows/WSL 첨부 경로 `docs/...` | 🟡 `as_posix()` 통일 + 테스트. **Windows 실기 재현은 못 했다** — Codex 쪽에서 확인해 주면 좋겠다 |
| XSS payload 가 href/raw HTML/SVG 로 안 남음 | 🟡 href·raw HTML ✅. **업로드 SVG 는 미처리** |

### Codex 에게 부탁

1. **Windows 실기**에서 업로드 → 개념 첨부 조회가 되는지 (내가 재현 못 하는 유일한 축)
2. `ICOHP_PS` comp1 의 −5.938 vs −5.944 — 어느 쪽이 정본인지 원자료 추적
3. `gap_eV` comp2 · `ICOHP_PS` comp2 의 원 출처 배선 (레지스트리에 `source_path` 채우면 검증기가 자동으로 잡는다)
4. 위 판정을 **다시 돌려서 반박** — 특히 §2 의 group 분리 기준(3-seed/4-seed 동일 group)에 이견이 있으면

---

## 7. 재현 명령 한 묶음

```bash
git fetch origin claude/friendly-meitner-lldvar && git log --oneline -1 origin/claude/friendly-meitner-lldvar   # f2cf68c7

python3 tools/db/validate_canonical.py --show      # 27항목 · 배선 22 · 실패 0
python3 webapp/tests/test_webapp.py                # 15/15
python3 -m compileall -q webapp/                   # PASS
```
