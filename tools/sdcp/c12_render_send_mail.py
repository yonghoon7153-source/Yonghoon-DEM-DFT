#!/usr/bin/env python3
"""SEND_MAIL_v<N>.md 렌더 (C-12 발송 메일) — 번들 README 에서 실행 블록·반송 절·walltime 문장을 **글자 그대로** 뽑는다.

  python3 tools/sdcp/c12_render_send_mail.py --bundle <sdcp_c12_v35 dir> --zip <sdcp_c12_v35.zip> \
      --commit <생성 커밋 sha> --out runs/sdcp_c12_2026_08_30/SEND_MAIL_v35.md [--variant A]

⚠ 손으로 옮기다 PP·dense 를 빠뜨린 전례가 있어 자동으로만 만든다 (v33 교훈).
   렌즈4 P1-2/P1-3/P1-4 · 렌즈5 P2(4.6일→8.16일) · P2-5(그쪽·돕니다·반말) 반영.
"""
import argparse, hashlib, json, pathlib, re

import sys as _sys
_REQ = "--selftest" not in _sys.argv          # 자체시험은 번들 없이 돈다
ap = argparse.ArgumentParser()
ap.add_argument("--bundle", required=_REQ)
ap.add_argument("--zip", required=_REQ)
ap.add_argument("--commit", required=_REQ)
ap.add_argument("--out", required=_REQ)
ap.add_argument("--variant", default="?")
ap.add_argument("--supersede_reason", default=None,
                help="교체 사유 한 문장 (외주처가 읽는 문장). ⚠ 안 주면 '아래 변경 절 참조' "
                     "로 나간다 — **사유를 추측해 박지 않는다** (2026-09-07 P1-3: v36 에 "
                     "이미 있는 clean slab 을 '빠져 있었다' 고 적어 나간 사고).")
ap.add_argument("--supersedes", default=None,
                help="**이미 발송한** 판(예: v35). 주면 메일 맨 앞에 교체 통지가 붙고 "
                     "변경 절 제목이 그 판 기준으로 바뀐다. ⛔ 안 주면 외주처가 두 판을 "
                     "다 돌리거나 옛 판을 돌린다.")
ap.add_argument("--changes_md", default=None,
                help="'이 판에서 바뀐 것' 절 본문(markdown 파일). ⛔ 2026-09-11 (v41): 판별 분기가 "
                     "없는 --supersedes(v37 이후)에 else 절의 v38 시절 문장이 그대로 박히는 것을 "
                     "막는다 — 분기도 파일도 없으면 **렌더하지 않는다** (거짓 변경 절 방지).")
ap.add_argument("--continue_from_hint", default=None,
                help="2026-09-21: 승계 블록(README 정본)의 `<이전 extraction 의 묶음 루트>` 자리에 박을 실제 경로 "
                     "(예: /home/kgy/projects/sdcp_c12_v41_2026_09_11/sdcp_c12_v41). 안 주면 자리표시자 그대로 나간다. "
                     "⚠ README 에 승계 블록이 없으면 이 플래그는 거부된다 (없는 절차를 메일에만 적지 않는다).")
ap.add_argument("--selftest", action="store_true", help="블록 선택·거부 경로 자체시험 (음성 포함)")
a = ap.parse_args()


def _split_blocks(readme_text):
    """README 의 ```…``` 중 실행 블록(하나)과 승계 블록(0 또는 1)을 가른다.

    2026-09-21 — 승계 블록도 `run_staged.sh 1` 을 담는다. 종전 규칙("run_staged.sh 1 이 든 블록이
    하나여야 한다")은 그것을 두 개로 세어 죽었다. 승계 블록은 `CONTINUE_FROM=` 으로 가른다.
    ⛔ 못 하는 것: 블록의 **내용**이 러너와 맞는지는 모른다 — 그것은 생성기 selftest 의 몫이다.
    """
    _all = [b for b in readme_text.split("```") if "run_staged.sh 1" in b]
    _main = [b for b in _all if "CONTINUE_FROM=" not in b]
    _cont = [b for b in _all if "CONTINUE_FROM=" in b]
    assert len(_main) == 1, "README 실행 블록이 %d개 (승계 블록 제외)" % len(_main)
    assert len(_cont) <= 1, "README 승계 블록이 %d개" % len(_cont)
    return _main[0].strip("\n"), (_cont[0].strip("\n") if _cont else None)


def _selftest():
    ok = [0, 0]
    def chk(c, m):
        ok[0] += 1; ok[1] += bool(c); print(("  ✔ " if c else "  ✘ ") + m)
    _R = "x\n```\nexport PP=1\nbash run_staged.sh 1\n```\ny\n```\nexport PP=1\nexport CONTINUE_FROM=/p\n[ \"$GO\" = 1 ] && bash run_staged.sh 1\n```\n"
    m, c = _split_blocks(_R)
    chk("CONTINUE_FROM" not in m and c is not None and "CONTINUE_FROM=/p" in c,
        "양성: 실행 블록과 승계 블록을 가른다 (둘 다 run_staged.sh 1 을 담는다)")
    m2, c2 = _split_blocks("```\nexport PP=1\nbash run_staged.sh 1\n```\n")
    chk(c2 is None and "PP=1" in m2, "양성: 승계 블록이 없는 README (구판) 도 그대로 읽힌다")
    try:
        _split_blocks(_R + "```\nbash run_staged.sh 1\n```\n"); chk(False, "⛔음성: 실행 블록이 둘이면 죽어야 한다")
    except AssertionError as e:
        chk("2개" in str(e), "⛔음성: 실행 블록이 둘이면 거부한다 (%s)" % e)
    try:
        _split_blocks(_R + "```\nCONTINUE_FROM=/q\nbash run_staged.sh 1\n```\n"); chk(False, "⛔음성: 승계 블록이 둘이면 죽어야 한다")
    except AssertionError as e:
        chk("승계 블록이 2개" in str(e), "⛔음성: 승계 블록이 둘이면 거부한다")
    print("  render selftest %d/%d" % (ok[1], ok[0]))
    return 0 if ok[0] == ok[1] else 1


if a.selftest:
    raise SystemExit(_selftest())

B = pathlib.Path(a.bundle)
readme = (B / "README_REQUEST.md").read_text(encoding="utf-8")
man = json.loads((B / "MANIFEST.json").read_text(encoding="utf-8"))
zsha = hashlib.sha256(pathlib.Path(a.zip).read_bytes()).hexdigest()
msha = hashlib.sha256((B / "MANIFEST.json").read_bytes()).hexdigest()
label = B.name
n_jobs = len(man.get("planned") or {})
zip_mb = pathlib.Path(a.zip).stat().st_size / 1e6

# ── 실행 블록: README 의 ```…``` 중 `run_staged.sh 1` 이 든 것 (승계 블록 제외 · 하나여야 한다) ──
run_block, cont_block = _split_blocks(readme)
if a.continue_from_hint and not cont_block:
    raise SystemExit("⛔ --continue_from_hint 를 줬는데 README 에 승계 블록(CONTINUE_FROM)이 없다 — "
                     "없는 절차를 메일에만 적지 않는다 (번들을 다시 만들어라)")
cont_block_mail = None
if cont_block:
    cont_block_mail = (cont_block
                       .replace("export EXPECT_MANIFEST_SHA256=<메일 본문의 MANIFEST SHA256>",
                                "export EXPECT_MANIFEST_SHA256=%s" % msha)
                       .replace("export EXPECT_ZIP_SHA256=<메일 본문의 ZIP SHA256>",
                                "export EXPECT_ZIP_SHA256=%s" % zsha))
    if a.continue_from_hint:
        assert "/abs/path/to/<이전 extraction 의 묶음 루트>" in cont_block_mail, "승계 블록의 자리표시자가 바뀌었다"
        cont_block_mail = cont_block_mail.replace("/abs/path/to/<이전 extraction 의 묶음 루트>", a.continue_from_hint)
# 메일에는 EXPECT 두 값을 실제 값으로 박는다 (README 는 '<메일 본문의 …>' 자리표시자)
run_block_mail = (run_block
                  .replace("export EXPECT_MANIFEST_SHA256=<메일 본문의 MANIFEST SHA256>",
                           "export EXPECT_MANIFEST_SHA256=%s" % msha)
                  .replace("export EXPECT_ZIP_SHA256=<메일 본문의 ZIP SHA256>",
                           "export EXPECT_ZIP_SHA256=%s" % zsha))
for v in ("PP=", "POTCAR_ALLOWLIST=", "BUNDLE_ZIP_SHA256=", "EXPECT_MANIFEST_SHA256=",
          "EXPECT_ZIP_SHA256=", "VASP_LAUNCHER_KIND=", "LAUNCHER_BIN=", "VASP_NPROC=", "VASP_EXE="):
    assert v in run_block_mail, "실행 블록에 %s 없음" % v

# ── 반송 절: README '## 보내 주실 것' 다음 문단들 → 다음 '## ' 전까지 ──
m = re.search(r"## 보내 주실 것\n\n(.*?)(?=\n## )", readme, re.S)
assert m, "README 에 '## 보내 주실 것' 절 없음"
ret = m.group(1).strip("\n")
assert "MANIFEST.json" in ret and "job.json" in ret and "RESULTS.json" in ret, "반송 절에 정본 항목 누락"

# ── walltime 문장: README 의 '⚠ **walltime**' 로 시작하는 불릿 (한 문장 출처) ──
# ⚠ 2026-09-08 — README 의 문장이 "⚠ **walltime — 요청은 단계 기준 하나입니다.**" 로 바뀌었다.
#   접두만 맞춘다 (정확 일치는 문장을 고칠 때마다 렌더러를 깨뜨린다).
mw = re.search(r"- (⚠ \*\*walltime.*?)(?=\n- \*\*POTCAR)", readme, re.S)
assert mw, "README 에 walltime 문장 없음 ('⚠ **walltime' 로 시작하는 불릿이 있어야 한다)"
wall = mw.group(1).strip()

# ── 시작 전 확인·회신 절: README 맨 앞 '## ⛔ 시작 전에 확인·회신해 주실 것' (2026-09-08 · 별도 문의문 대신) ──
mp = re.search(r"## ⛔ 시작 전에 확인·회신해 주실 것[^\n]*\n(.*?)(?=\n## )", readme, re.S)
pre_body = mp.group(1).strip("\n") if mp else ""

# ── 재개 조건: MANIFEST.kconv_pair (사전등록에서 복사된 것) ──
kp = man.get("kconv_pair") or {}
reopen = next((v for k, v in kp.items() if "재개_조건" in str(k)), {}) or {}
_cf = man.get("cost_frozen") or {}
# 🔴 2026-09-03 — staged 번들은 단계 게이트 반영값을 인용한다 (makespan_d 는 한 물결 가정).
mk = _cf.get("makespan_staged_d") or _cf.get("makespan_d") or {}
conc = int(((man.get("submission") or {}).get("max_concurrency")) or 8)
mk_c = mk.get(str(conc), mk.get(conc))
longest = round((man.get("cost_frozen") or {}).get("longest_job_h") or 0)
_prev = a.supersedes or "v34"
_has_cs = bool((man.get("refs") or {}).get("clean_slab"))
_rqn = (man.get("reported_quantity") or {}).get("name") or ""
if a.supersedes == "v35":
    # v35 → v36 : **기준계가 늘었다.** 외주처가 알아야 하는 건 이것뿐이다.
    _changes = f"""- **잡이 {n_jobs}개로 늘었습니다** (v35 는 16잡). 늘어난 셋은 전부 **기준계(clean slab)** 입니다:
  `refs/clean_slab__afm2424_pm1` · `refs/clean_slab__afm2424_net4` · `vacconv/clean_slab__afm2424_pm1__c2`.
  복합체와 **같은 셀 · 같은 k · 같은 초기 자기배열**이고, 조각(분자)만 없습니다.
- **보고량이 늘었습니다** — v35 는 두 조각의 **차**만 냈는데, 이제 각 조각의 **흡착에너지 절대값**도
  냅니다. 그래서 조각 없는 슬랩 에너지가 필요합니다. 계산 방법·설정은 v35 와 **완전히 같습니다**.
- 기본 동시 실행을 **{conc}잡**으로 잡았습니다 (v35 는 4잡). 늘어난 잡을 같은 일정 안에 넣기 위함입니다 —
  {mk_c}일. 할당이 부족하시면 `JOBS_PARALLEL` 로 줄이셔도 됩니다(일정만 늘어납니다).
- 그 밖의 실행 절차·반송 목록·게이트는 **v35 와 동일**합니다. 새로 익히실 것이 없습니다."""
elif a.supersedes == "v36":
    # v36 → v37 : **계산 입력은 한 글자도 안 바뀌었다.** 바뀐 것은 실행 배치와 시간 계약이다.
    _sa = (_cf.get("stage_alloc_h") or {}).get("NELM_시나리오") or {}
    _sreq = int(-(-max(_sa.get("1") or 0, _sa.get("2") or 0) // 12) * 12) or "?"
    _mmw = (man.get("memory_model") or {})
    _mmr = _mmw.get("권고") or {}
    _cores_j = int((man.get("submission") or {}).get("cores_per_job") or 0)
    _changes = f"""- ⚠ **계산 입력(INCAR·POSCAR·KPOINTS·자세·사전등록)은 v36 과 동일합니다.** 다시 익히실 것이
  없습니다 — 물리적으로 같은 계산이고, 바뀐 것은 **실행 배치와 시간 계약**입니다.
- **랭크 배치를 명시했습니다.** 잡당 랭크 {_cores_j} 개를 **노드 {_mmr.get("권고_노드_per_잡", "?")} 개에
  펼쳐** 주십시오 (`VASP_NODES`). 한 노드에 몰면 최악 잡이
  {_mmw.get("계획_랭크_잡_전체_GB", "?")} GB 를 요구해 OOM 납니다 — 2026-09-04 에 실제로 그렇게
  났습니다. 러너가 **첫 VASP 실행 전에** 계산해 보고 넘치면 멈춥니다.
- **동시 실행 기본을 {conc}잡으로** 낮췄습니다 (v36 은 5잡). 필요한 총 노드
  {_mmr.get("필요_총_노드", "?")} 개.
- **요청하실 walltime 이 잡 단위가 아니라 단계 단위입니다** — 러너는 한 할당 안에서 그 단계를
  다 돌리므로 **단계당 {_sreq} h** 가 필요합니다. 종전 메일의 '잡당 84 h' 만 보시면 잡이 다
  끝나기 전에 할당이 잘릴 수 있었습니다.
- **배치를 선언이 아니라 실측으로 확인합니다.** 러너가 첫 VASP 전에 같은 launcher 로 `hostname` 을
  동시 {conc}개 띄워 랭크가 실제로 어느 노드에 놓이는지 읽고, 잡 사이에 노드가 겹치면 멈춥니다.
  결과 `PLACEMENT_PROBE.json` 을 반송 목록에 넣었습니다. SLURM 밖에서 돌리시면 할당 호스트 목록을
  `VASP_HOSTFILE` 로 주십시오 (SLURM 안에서는 자동).
- ⛔ **시작 전 확인 질문 다섯 가지를 README 맨 앞과 이 메일 §0 에 넣었습니다** — 노드 확보 · 노드별
  CPU 예약/할당 메모리/cgroup 제한(단위까지) · 단계당 {_sreq} h 할당 가능 여부 · 이어가기 운영 방식 · 실행 환경.
  단계당 {_sreq} h 는 알려 주신 잡당 큐 상한 91 h 로는 충족되지 않습니다. **이 답을 받기 전에는 시작하지 말아
  주십시오** — 답에 따라 코어·동시잡·walltime 을 다시 계산해 새 번들을 드릴 수 있습니다.
- **반송 압축에서 POTCAR 를 빼 주십시오** (라이선스). `--exclude=POTCAR` 를 명령에 넣었습니다.
  증빙(`POTCAR_PROVENANCE.json` · `PLACEMENT_PROBE.json` 등)은 그대로 두시면 됩니다.
- **노드 메모리 제한을 실행 노드마다 읽습니다.** 프로브가 각 노드의 cgroup 제한을 **유한 / 무제한(검증) /
  못 읽음** 세 상태로 가르고, 유한이면 그 값으로, 무제한이면 스케줄러 할당·물리 RAM 의 최소로 판정하며,
  **못 읽으면 물리 RAM 으로 대체하지 않고 멈춥니다.** 멈추면 `PLACEMENT_PROBE.json` 의 노드별 상태·사유를
  보내 주십시오 — 저희가 그 환경에 맞춰 다시 드립니다.
- 그 밖의 실행 절차·반송 목록·게이트는 **v36 과 동일**합니다.
- (v37–v40 은 내부 리뷰에서 배치·시간 계약·메모리 판정 결함이 발견돼 **발송 전에 철회**했습니다 —
  받으신 적이 없어야 정상입니다.)"""
elif a.changes_md:
    _changes = pathlib.Path(a.changes_md).read_text(encoding="utf-8").strip("\n")
    assert _changes, "--changes_md 파일이 비어 있다"
elif a.supersedes:
    # ⛔ 2026-09-11 — v41 을 v40 교체로 렌더하며 발견: 아래 else 는 v38 시절 변경 목록이라
    #   v40→v41 에는 거짓이다(attestation·δ_k 는 이번에 안 바뀌었다). P1-3 과 같은 종류의 사고 —
    #   사유뿐 아니라 **변경 절도** 추측해 박지 않는다. 분기가 없는 판은 파일로 받는다.
    raise SystemExit("⛔ --supersedes %s 의 변경 절 분기가 없다 — --changes_md <파일> 로 주어라 "
                     "(else 절의 옛 문장을 재사용하지 않는다)" % a.supersedes)
else:
    _changes = f"""- **선택 attestation 함정 제거**: `MAKE_POTCAR_ATTESTATION.sh` 가 VASP stdout 전문을 적고 봉인은
  토큰만 담아, 돌리면 1단계를 다 돌린 뒤에야 판정이 막히는 결함(렌즈4 P0-1). 둘 다 토큰으로 통일했다.
- **δ_k 설계 제외의 근거를 비준 사전등록에 둔다** (안 {a.variant}). 재개 조건이 기계 평가 구조로
  MANIFEST 에 복사되고 분석기가 `reopen_eval` 로 남긴다.
- `overall_citable_at_0.01eV` 는 δ_k 가 없으면 **False**(None 아님).
- 반송 목록에 `MANIFEST.json`·`job.json`·`RESULTS.json` 과 "통째로 압축" 을 정본으로 넣었다.
- walltime 문장 세 문서 통일 · 일정 {mk_c}일(동시 {conc}잡)."""


# 🔴 2026-09-04 — **이미 보낸 판을 교체하는 메일**이면 그 사실이 맨 앞에 있어야 한다.
#   없으면 외주처가 두 판을 다 돌리거나 옛 판을 돌린다. 제목에도 넣는다.
_subj_pre = ("[교체] " if a.supersedes else "")
# ⛔⛔ 2026-09-07 (Codex v37 P1-3) — 종전엔 교체 사유가 **supersedes 값과 무관하게**
#   "기준계(clean slab) 3잡이 빠져 있었습니다" 로 박혀 있었다. 그건 v35→v36 의 사유이고
#   v36 에는 clean slab 3잡이 **이미 다 있다**(zip 실물 확인). 즉 교체 메일이 거짓 사유를
#   달고 나갔다. ⇒ 사유를 **추측하지 않는다** — 주면 그것을, 없으면 변경 절을 가리킨다.
_reason = (a.supersede_reason if getattr(a, "supersede_reason", None)
           else ("계산해야 할 기준계(clean slab) 3잡이 빠져 있었습니다. 저희 설계 누락이며 "
                 "귀측 실행과는 무관합니다." if a.supersedes == "v35"
                 else "아래 **이 판에서 바뀐 것** 절에 적었습니다. 저희 쪽 수정이며 "
                      "귀측 실행과는 무관합니다."))
_replace_block = ("" if not a.supersedes else f"""
> ## ⛔ 먼저 읽어 주십시오 — **이전에 보내 드린 `sdcp_c12_{a.supersedes}.zip` 은 폐기해 주십시오.**
> 이 메일의 묶음이 그것을 **대체**합니다. 두 개를 같이 돌리지 말아 주십시오.
> · 아직 시작하지 않으셨다면: 이전 zip 을 지우고 이 묶음으로만 진행해 주십시오.
> · 이미 시작하셨다면: **멈추고 알려 주십시오.** 지금까지 쓰신 시간은 저희가 부담하겠습니다.
> · 바뀐 이유: {_reason}
""")

cores = int((man.get("submission") or {}).get("cores_per_job") or (man.get("cost_frozen") or {}).get("cores_per_job") or 48)
# 2026-09-21 — 교체판 + README 승계 블록이 있으면, 메일에서 **승계가 먼저**다 (완주 잡을 다시 돌리게 두지 않는다).
_cont_section = ""
if cont_block_mail and a.supersedes:
    _cont_section = f"""### 1′. 이전 판({a.supersedes})에서 **완주한 잡을 이어 쓰기** — 권장 경로

이전 extraction 에서 완주한 잡은 다시 돌리지 않습니다. ⛔ **완주 폴더를 손으로 옮기지 마십시오** —
새 extraction 에 먼저 복사하면 봉인 스크립트가 "생산 산출물이 이미 있습니다" 로 거부하고, 이전 extraction 에
새 스크립트를 덮으면 census 가 거부합니다. 러너가 봉인 **뒤에** 스스로 옮깁니다. 이 묶음을 **새 빈 디렉터리에** 풀고
(§1 과 같이 해시 대조 뒤), 아래 블록을 그대로 쓰십시오 — `<이 묶음을 푼 디렉터리>` 와 `CONTINUE_FROM` 만 채우시면 됩니다.

```bash
{cont_block_mail}
```

러너 출력에 `✓ 승계 <잡>` 가 완주 잡 수만큼 찍히고 물결 집계에 `건너뜀 N` 으로 잡힙니다. 완주가 증명되지 않은
잡(중단 잔재)은 `승계 안 함 … — <사유>` 로 찍히고 그 자리에서 새로 실행됩니다. 이전 extraction 은 지우지 말고 두십시오
(`CONTINUATION.json` 이 그 경로·MANIFEST·봉인 해시를 가리키며, 반송 목록에 들어갑니다).

"""

mail = f"""# C-12 {label.split('_')[-1]} 발송 메일 (그대로 복붙)
{_replace_block}

> 첨부: `{label}.zip` ({zip_mb:.1f} MB · {n_jobs}잡 · 전부 static)
> ⚠ 이 파일은 **자동 생성**이다 (tools/sdcp/c12_render_send_mail.py). 실행 블록·반송 목록·walltime
>   문장은 번들 README 에서 글자 그대로 뽑았다 — 손으로 고치지 마라.

## 제목
```
{_subj_pre}[DFT 위탁] SDCP/PTFE–LiNiO₂ 계면 단일점 {n_jobs}잡 — 번들 {label.split('_')[-1]}
```

## 본문

안녕하세요.

SDCP·PTFE 바인더 계면 계산 번들을 보내드립니다. **VASP 단일점(static) {n_jobs}잡**이고,
실행·검증·분석 스크립트가 번들 안에 전부 들어 있습니다.

{("### 0. 먼저 회신해 주실 것 — **이 답을 받기 전에는 시작하지 말아 주십시오**" + chr(10) + chr(10) + pre_body + chr(10)) if pre_body else ""}
### 1. 무결성 확인 (먼저)

```
EXPECT_ZIP_SHA256      = {zsha}
EXPECT_MANIFEST_SHA256 = {msha}
```

```bash
sha256sum {label}.zip          # 위 값과 대조 — 다르면 전송이 깨진 것입니다
mkdir -p <이 묶음 전용 빈 디렉터리> && cd <그 디렉터리>
unzip /경로/{label}.zip && cd {label}
sha256sum MANIFEST.json             # 위 값과 대조
```

{_cont_section}### 2. 실행{" — 처음부터 (승계하지 않을 때만)" if cont_block_mail and a.supersedes else ""}

⚠ 아래 변수가 **전부 필수**입니다. 하나라도 빠지면 러너가 즉시 멈춥니다
(조용히 다른 설정으로 도는 것보다 멈추는 게 낫다고 보아 그렇게 만들었습니다).
실행은 **계산 노드 할당 안에서** 해 주십시오 — 러너가 그 자리에서 잡 {conc}개를 동시에 띄웁니다.
{"⚠ 이전 판의 완주 잡을 이어 쓰시려면 이 블록이 아니라 **위 §1′ 승계 블록**을 쓰십시오 — 이 블록은 19잡을 전부 처음부터 돌립니다." if cont_block_mail and a.supersedes else ""}

```bash
{run_block_mail}
```

⛔ **배열 잡으로 한꺼번에 던지지 말아 주십시오.** 2단계가 1단계 결과에 의존해서
동시에 돌리면 결과가 무의미해집니다.

### 3. POTCAR — 보내실 것 없고, 조립하실 것도 없습니다

**POTCAR 파일 자체는 주고받지 않습니다** (라이선스). 귀측 트리를 그대로 쓰시면 됩니다.
**POTCAR 를 따로 조립하지 마십시오** — `run_staged.sh` 가 첫 VASP 실행 전에 `SEAL_POTCAR_ROOT.sh` 로
전 잡을 조립하고, 원본 SHA256 · TITEL · 조립본 SHA256 을 `POTCAR_PROVENANCE.json` 에 남깁니다.
저희는 그 해시로 **"{n_jobs}잡이 한 트리에서 나왔는가"** 만 확인합니다 — 귀측 트리가 어느 배포판인지는
판정하지 않습니다 (이 묶음은 탐색용 정책이라 원고 인용 자격을 주장하지 않습니다).

(선택) PAW release 를 **기록**으로 남기시려면 실행 블록의 주석 한 줄(`MAKE_POTCAR_ATTESTATION.sh`)을
`bash run_staged.sh 1` **앞에서** 돌려 주십시오 — 첫 VASP 실행 뒤에는 만들 수 없습니다. 안 돌리셔도
계산·판정은 그대로입니다. 돌리셨는데 결함이 있으면 러너가 생산 **전에** 멈추고 이유를 찍습니다.

### 4. 반송해 주실 것

{ret}

### 5. 예상 자원

{n_jobs}잡 전부 단일점(static)입니다. 기본 **동시 {conc}잡 · {cores}코어/잡**으로
계획했습니다 (그 조건에서 전체 약 {mk_c}일 — 모형이라 ±2배).
{wall}

---

문제가 생기면 러너가 찍는 메시지를 그대로 보내 주시면 됩니다.

감사합니다.

---

## ⚠ 보내기 전 확인 (1저자)

- [ ] 첨부 zip sha256 == `{zsha[:14]}…`
- [ ] 본문에 두 해시가 정확히 들어갔는가
- [ ] 실행 블록에 `PP`·`POTCAR_ALLOWLIST`·`LAUNCHER_BIN`·`VASP_EXE` 가 살아 있는가
- [ ] 받는 사람 주소

## 이 판에서 바뀐 것 ({_prev} → {label.split('_')[-1]})

{_changes}

🔁 **재개 조건 (비준 사전등록에서 복사 · 결과 보기 전 선언)**
> {reopen.get('규칙')}

## 기록

| | |
|---|---|
| 번들 | `runs/sdcp_c12_2026_08_30/{label}.zip` |
| 증서 | `runs/sdcp_c12_2026_08_30/IDENTITY_{label.split('_')[-1]}.json` |
| 생성 커밋 | `{a.commit[:8]}` (clean · 생성 시점에 origin 에 있던 커밋) |
| 리뷰 | BH(다중 감사 7렌즈) · v34 6렌즈 — `kb/reviews/` |
"""
# 문체 — 외주처 문서에 남기지 않을 표현
for bad in ("그쪽", "돕니다", "판정의 일부다"):
    assert bad not in mail.split("## ⚠ 보내기 전 확인")[0], "메일 본문에 '%s' 잔존" % bad
pathlib.Path(a.out).write_text(mail, encoding="utf-8")
print("→", a.out, "| zip", zsha[:12], "| manifest", msha[:12], "| makespan", mk_c, "일 @", conc)
