"""SELF-116: 언로딩 문서가 인용한 에이전트 작업 트리 커밋 (원격에 없음) → 본 가지 번호 · 보낸 첫 요청서 = 표지 + 예외 등재 · 원장 · 진행 · CLAUDE.md."""
import json

R = '/home/user/Yonghoon-DEM-DFT/'
MAP = {  # 에이전트 작업 트리 판 → 본 가지 cherry-pick (git patch-id 12/12 같음 · 10-14 밤 확인)
    '122abaad8': 'f823bad21', 'f5c899453': '5cba214da', '2b6500869': 'eeb99b082', 'a03cff857': 'efa935bd7',
    'fbf59cc78': '1b77fe8e9', 'e90f903f1': 'b7ef99f1c', 'f67f242bb': 'cee186e55', 'd9e51323d': 'c82cbfdde',
    'e6c9049dc': '18b798ecc', 'c696dbf0f': 'b1121b6b6', 'ca59641ca': 'e271bdd48', '82d532c60': '70b3fefed',
}


def rd(path):
    return open(R + path, encoding='utf-8').read()


def wr(path, s):
    open(R + path, 'w', encoding='utf-8').write(s)


def sub(path, old, new, n=1):
    s = rd(path)
    assert s.count(old) == n, (path, old[:60], s.count(old))
    wr(path, s.replace(old, new))


# ── A. 재확인 요청서 (아직 안 보냄) → 정정판 ─────────────────────────────────
A = 'docs/reviews/codex_dem_unloading_kit_reverify_fix_recheck_request_20261014.md'
sub(A, '> **리뷰 핀** = `eaecfba2a` (코드 · 증거 · 이 요청서가 든 본 가지 커밋 · 원장 claimed_fixed 기록 = 그 다음 커밋) · **기준** = `a30fe150e` (판정문 핀) · 이 수정 가지 시작 = `77b5885e0`.',
    '> **리뷰 핀** = 이 정정판이 든 본 가지 커밋 (발송 때 1저자가 번호를 적는다 · 키트 코드 · 증거 바이트 = `eaecfba2a` 와 같다 · 원장 claimed_fixed = `4a8b55013`) · **기준** = `a30fe150e` (판정문 핀) · 이 수정 가지 시작 = `77b5885e0`.\n'
    '> ⚠ **정정 10-14 밤 (`SELF-116`)**: 첫 판 (`eaecfba2a`) §0 · §3 · §6 의 커밋 번호 셋 (시험 먼저 · 수정 · README) 은 수정 작업 트리 (에이전트) 판이라 원격에 없었다 — 본 가지 번호로 바꿨다 '
    '(cherry-pick · `git patch-id` 같음 · 키트 트리 바이트 같음).  증거 폴더 이름 (`before_fix_tests_first_…/` · `after_fix_…/`) · `summary.json` 의 `git_head` 는 로그를 낸 작업 트리 판 그대로 둔다 (대응 = 증거 README §2).')
sub(A, '- 커밋: 시험 먼저 `c696dbf0f` → 수정 `ca59641ca` → README `82d532c60` → 증거 · 이 요청서 (그 다음 커밋).',
    '- 커밋 (본 가지): 시험 먼저 `b1121b6b6` → 수정 `e271bdd48` → README `70b3fefed` → 증거 · 이 요청서 첫 판 `eaecfba2a` → 원장 claimed_fixed `4a8b55013` → 이 정정판.')
sub(A, '| 명령 (`python3 -I …` · 키트 폴더) | 최종 (`82d532c60` · 깨끗) | 시험 먼저 (`c696dbf0f`) |',
    '| 명령 (`python3 -I …` · 키트 폴더) | 최종 (`70b3fefed` 와 같은 키트 트리 · 깨끗) | 시험 먼저 (`b1121b6b6` 와 같은 키트 트리) |')
sub(A, '- ⬜ 원장 (메인 세션): `ULKRR-02` · `03` · `04` → claimed_fixed (`ca59641ca`) · `ULKRR-01` = 실행 2 PASS 뒤.',
    '- ✅ 원장 (`4a8b55013`): `ULKRR-02` · `03` · `04` → claimed_fixed (`e271bdd48`) · `ULKRR-01` = claimed_fixed `039abb141` (남은 증거 = 실행 2 PASS).')

# ── B. 그 증거 README ───────────────────────────────────────────────────────
B = 'docs/reviews/dem_unloading_kit_reverify_fix_evidence_20261014/README.md'
sub(B, '| `before_fix_tests_first_c696dbf0f/` | `c696dbf0f` (새 시험만 더함 · 키트 코드 그대로) |',
    '| `before_fix_tests_first_c696dbf0f/` | 작업 트리 판 (폴더 이름의 번호 · 원격에 없음) = 본 가지 `b1121b6b6` (새 시험만 더함 · 키트 코드 그대로) |')
sub(B, '| `after_fix_82d532c60/` | `82d532c60` (수정 `ca59641ca` + README) ·',
    '| `after_fix_82d532c60/` | 작업 트리 판 (폴더 이름의 번호 · 원격에 없음) = 본 가지 `70b3fefed` (수정 `e271bdd48` + README) ·')
sub(B, '| 명령 (`python3 -I …`) | 77b5885e0 | 시험 먼저 c696dbf0f | 최종 82d532c60 |',
    '| 명령 (`python3 -I …`) | 77b5885e0 | 시험 먼저 (= b1121b6b6) | 최종 (= 70b3fefed) |')
sub(B, '\n## 3. 명령 · rc · 검사 수',
    '\n- ⚠ **정정 10-14 밤 (`SELF-116`)**: 시험 먼저 · 최종 두 묶음은 수정 작업 트리 (에이전트) 에서 냈다 — 그 판 번호 (폴더 이름 · `summary.json` 의 `git_head`) 는 원격에 없다.  '
    '본 가지 대응 = cherry-pick (`git patch-id` 같음 · 작업 트리 판 ↔ 본 가지의 `git diff -- docs/data/ps45_unload_20261009/` 빈 결과 · 10-14 밤 확인): 시험 먼저 → `b1121b6b6` · 수정 → `e271bdd48` · README → `70b3fefed`.  '
    '로그 · rc · 봉인 sha256 은 그대로 유효하다 (키트 트리 같음).\n\n## 3. 명령 · rc · 검사 수')

# ── C. 키트 README (봉인 밖) ─────────────────────────────────────────────────
C = 'docs/data/ps45_unload_20261009/README.md'
sub(C, '(계획 dem_unloading_kit_reverify_fix_plan_20261014.md · 시험 먼저 `c696dbf0f` → 수정 `ca59641ca`)',
    '(계획 dem_unloading_kit_reverify_fix_plan_20261014.md · 시험 먼저 `b1121b6b6` → 수정 `e271bdd48`)')

# ── D. 첫 수정 계획 §5 표 ────────────────────────────────────────────────────
D = 'docs/reviews/dem_unloading_kit_fix_plan_20261014.md'
s = rd(D)
hdr = '| 커밋 | 무엇 | 시험 (고치기 전 → 고친 뒤) |'
assert s.count(hdr) == 1
s = s.replace(hdr, '> 정정 10-14 밤 (`SELF-116`): 이 표의 커밋 번호 = 본 가지 (cherry-pick · `git patch-id` 같음) — 첫 판은 수정 작업 트리 (에이전트) 판 번호라 원격에 없었다.\n\n' + hdr)
for a in ('122abaad8', 'f5c899453', '2b6500869', 'a03cff857', 'fbf59cc78', 'e90f903f1', 'f67f242bb', 'd9e51323d', 'e6c9049dc'):
    tok = f'| `{a}` |'
    assert s.count(tok) == 1, (a, s.count(tok))
    s = s.replace(tok, f'| `{MAP[a]}` |')
wr(D, s)

# ── E. 보낸 첫 재확인 요청서 = 본문 그대로 + 머리 표지 · 예외 등재 ──────────
E = 'docs/reviews/codex_dem_unloading_kit_fix_recheck_request_20261014.md'
anchor = '\n## 0. 대상 · 지위'
sub(E, anchor,
    '\n> ⚠ **정정 표지 10-14 밤 (`SELF-116`)**: 본문 (§1 표) 의 커밋 번호는 수정 작업 트리 (에이전트) 판이라 원격에 없다 — 본 가지 대응 (cherry-pick · `git patch-id` 같음) = '
    '`docs/reviews/dem_unloading_kit_fix_plan_20261014.md` §5 표 (정정판) · `docs/reviews/doc_refs_sha_exceptions.tsv`.  본문은 보낸 그대로 둔다 (판정 = 핀 `a30fe150e`).\n' + anchor)
X = 'docs/reviews/doc_refs_sha_exceptions.tsv'
x = rd(X).rstrip('\n') + '\n'
for a in ('fbf59cc78', '2b6500869', 'a03cff857', 'f67f242bb', 'd9e51323d', 'e6c9049dc'):
    assert a not in x
    x += (f'{E}\t{a}\t{MAP[a]}\t언로딩 키트 수정 (ULKR) 에이전트 작업 트리 커밋 (로컬 전용 · 가지 지움 10-14 밤) — 본 가지 cherry-pick {MAP[a]} '
          f'(git patch-id 같음).  보낸 요청서라 본문은 그대로 두고 머리 정정 표지가 대응표 (수정 계획 §5 정정판) 를 가리킨다 (SELF-116)\n')
wr(X, x)

# ── F. 원장 SELF-116 ────────────────────────────────────────────────────────
p = R + 'docs/reviews/findings.json'
d = json.load(open(p, encoding='utf-8'))
assert not any(f['id'] == 'SELF-116' for f in d['findings'])
d['findings'].append({
    'id': 'SELF-116', 'severity': 'P3', 'status': 'open', 'owner': 'claude',
    'found_by': '10-14 밤 내 점검 (Codex 짧은 재확인 요청서 발송 전 · 문서가 인용한 커밋을 원격 도달 가능성으로 전수 대조)',
    'opened_in': A,
    'title': '에이전트 작업 트리에서 쓴 언로딩 문서가 그 작업 트리의 커밋 번호를 cherry-pick 뒤에도 그대로 인용 — 원격 어디에도 없는 커밋 12 개 (문서 다섯) · '
             '로컬 검사 check_doc_refs (도달 기준 = rev-list --all) 는 로컬 에이전트 가지가 그 커밋을 붙잡고 있어 초록 · GitHub CI 는 시간 제한으로 늘 cancelled 라 못 봄',
    'note': '본 가지 대응 = cherry-pick (git patch-id 12/12 같음 · 키트 트리 바이트 같음): 시험 먼저 c696dbf0f→b1121b6b6 · 수정 ca59641ca→e271bdd48 · README 82d532c60→70b3fefed · '
            '첫 수정 묶음 122abaad8→f823bad21 · f5c899453→5cba214da · 2b6500869→eeb99b082 · a03cff857→efa935bd7 · fbf59cc78→1b77fe8e9 · e90f903f1→b7ef99f1c · f67f242bb→cee186e55 · '
            'd9e51323d→c82cbfdde · e6c9049dc→18b798ecc.  고침 (이 커밋): 살아 있는 문서 넷 (재확인 요청서 = 정정판 · 그 증거 README · 키트 README · 첫 수정 계획 §5) = 본 가지 번호 · '
            '이미 보낸 첫 재확인 요청서 = 본문 그대로 + 머리 정정 표지 + doc_refs_sha_exceptions.tsv 6 줄 · 쓸모 다한 로컬 에이전트 가지 둘 (작업 트리 깨끗 · git cherry 전부 같은 패치 있음 · '
            'tip de089fd94 · 411398d8c) 지움 → 로컬 검사가 원격과 같은 23 자리를 잡는 것을 확인한 뒤 고침.  다른 로컬 에이전트 가지들 = 문서가 인용한 로컬 전용 커밋 0 (전수 대조).  '
            '남은 뿌리 = 검사기의 도달 기준이 로컬 가지까지 센다 (원격 추적 ref + HEAD 로 좁히는 안 = 1저자 결정 대기) → 그때까지 open.',
})
open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')

# ── G. 진행 기록 ────────────────────────────────────────────────────────────
q = 'docs/session_20260923_progress.md'
wr(q, rd(q).rstrip('\n') + '\n' + '- **10-14 밤 19 (내 오기 `SELF-116` · 문서 정정)**: 언로딩 문서 다섯이 에이전트 작업 트리 커밋 12 개 (원격에 없음) 를 인용 — 로컬 검사는 로컬 에이전트 가지 때문에 초록 · '
   'CI 는 늘 cancelled.  살아 있는 문서 넷 = 본 가지 번호 (`b1121b6b6` · `e271bdd48` · `70b3fefed` · 첫 수정 묶음 아홉) · 보낸 첫 재확인 요청서 = 표지 + 예외 6 줄 · 로컬 에이전트 가지 둘 지움 · '
   'Codex 재확인 요청서 = 정정판 (리뷰 핀 = 이 커밋 · 키트 코드 · 증거 바이트 = `eaecfba2a` 와 같다) · ⬜ 검사기 도달 기준 (원격 + HEAD) = 1저자 결정.\n')

# ── H. CLAUDE.md 언로딩 줄 ───────────────────────────────────────────────────
sub('CLAUDE.md', '→ ⬜ ibb 문법 fixture 한 번 (키트 README §1-6) · Codex 짧은 재확인 (`docs/reviews/codex_dem_unloading_kit_fix_recheck_request_20261014.md` · 발송 = 1저자).',
    '→ ✅ 짧은 재확인 발송 · ibb 문법 실행 1 (job 285220) = FAIL = fixture 결함 `SELF-115` (고침 `039abb141`) → ⛔ **Codex 재확인 (10-14 · 핀 `a30fe150e`) = HOLD** '
    '(`docs/reviews/codex_review_dem_unloading_kit_reverify_20261014.md` · ULKR 닫힘 8 · 부분 4 · 새 P1 `ULKRR-01` (= `SELF-115`) · `ULKRR-02` · `03` · P2 `ULKRR-04`) → ✅ 수정 계획 Q1–Q7 권고대로 → '
    '✅ 수정 (시험 먼저 `b1121b6b6` · 수정 `e271bdd48` · README `70b3fefed` · Linux 증거 `eaecfba2a` · 원장 `4a8b55013` · 요청서 정정판 = `SELF-116`) → ⬜ ibb 문법 **실행 2** (키트 README §1-6) · '
    'Codex 짧은 재확인 (`docs/reviews/codex_dem_unloading_kit_reverify_fix_recheck_request_20261014.md` · 핀 = 정정판 커밋 · 발송 = 1저자) · ⛔ 본 R · 10:0 연장 · U = 재확인 GO + 실행 2 PASS 뒤.')
print('ok')
