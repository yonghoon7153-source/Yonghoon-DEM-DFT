#!/usr/bin/env python3
"""22p 다리 provenance 추출기 — 단계 C 일회용 도구.

★ 왜 `tools/` 가 아니라 `docs/` 에 있나
   `tools/` 는 RUN_SCOPE 라 파일을 하나 넣기만 해도 `source_digest` 가 바뀌고
   기존 artifact 가 fail-closed 로 무효화된다 (재생성 ~28분 + 10시간).
   이 스크립트는 "무엇이 실제로 존재하는가" 를 먼저 확정하기 위한 일회용이므로
   RUN_SCOPE 밖에 둔다. 영구 `leg_index.yaml` 생성기는 20차 리뷰 발견 10 대응
   으로 단계 B 에서 `tools/` 안에 만든다 — 그때는 digest 변경을 감수한다.

★ 무엇을 답하는가
   - 발견 4.1: `analyze_22p_gap.py:291` 이 code identity 를 set 으로 찍어서,
     커밋된 txt 만으로는 어느 digest 가 왜곡 다리 것인지 알 수 없다. 다리별
     manifest 를 직접 읽으면 확정된다. ocpbias 배선 수정(42b8b5c2) 이전 digest
     로 돌린 **왜곡** 다리가 있으면 그 수치는 폐기 대상이다.
   - 발견 3: 다리별 실제 restart 예산 (지금 문서는 "전부 restart 5" 가 가정이다).
   - 발견 10: 이 표가 곧 `leg_index.yaml` 의 내용이다.

읽기 전용 — `results/` 를 수정하지 않는다.
사용: degradation-degeneracy 안에서 `python3 docs/22p_gap/leg_probe.py`
"""
import yaml
from pathlib import Path

rows = []
for d in sorted(Path("results").iterdir()):
    if not d.is_dir():
        continue
    mp = d / "manifest.yaml"
    if not mp.is_file():
        rows.append((d.name, {"digest": "(manifest 없음)"}))
        continue
    try:
        m = yaml.safe_load(mp.read_text(encoding="utf-8")) or {}
    except Exception as e:
        rows.append((d.name, {"digest": f"ERR {str(e)[:20]}"})); continue
    rs = m.get("run_spec") or {}
    rc = rs.get("halfcell_recipe") or {}
    wob = ",".join(f"{k.replace('_offset_mv','').replace('_stretch','st')}={rc[k]}"
                   for k in ("pe_offset_mv", "ne_offset_mv", "pe_stretch", "ne_stretch")
                   if rc.get(k) not in (None, 0, 0.0, 1, 1.0)) or "-"
    pi = rs.get("p_ini") or m.get("p_ini") or {}
    a_ne = None
    if isinstance(pi, dict):
        for v in pi.values():
            if isinstance(v, (list, tuple)) and len(v) >= 3:
                a_ne = round(float(v[2]), 4); break
    rows.append((d.name, {
        "digest": (rs.get("source_digest") or "-")[:16],
        "commit": (rs.get("git_commit") or m.get("git_commit") or "-")[:8],
        "dirty": str(m.get("git_dirty_tracked", m.get("git_dirty", "-")))[:5],
        "ref": (rs.get("reference") or "-")[:8],
        "recipe": (rc.get("method") or "-")[:8],
        "wobble": wob[:26],
        "rst": rs.get("n_restarts", m.get("n_restarts")),
        "warm": str(rs.get("warm_start", m.get("warm_start")))[:5],
        "ncond": rs.get("n_conditions") or m.get("n_conditions"),
        "a_ne": a_ne,
        "pini_cond": str(rs.get("p_ini_cond") or "-")[:12],
    }))

H = [("digest", 17), ("commit", 9), ("dirty", 6), ("ref", 9), ("recipe", 9),
     ("wobble", 27), ("rst", 4), ("warm", 6), ("ncond", 6), ("a_ne", 8),
     ("pini_cond", 13)]
print(f"{'leg':<34}" + "".join(f"{h:<{w}}" for h, w in H))
print("-" * (34 + sum(w for _, w in H)))
for name, r in rows:
    print(f"{name:<34}" + "".join(f"{str(r.get(h, '-')):<{w}}" for h, w in H))
print(f"\n디렉터리 {len(rows)}개")
