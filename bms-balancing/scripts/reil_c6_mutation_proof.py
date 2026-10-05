"""REIL C6 봉인 변이 증명 — 봉인 사본을 바꾸고 (대부분 MANIFEST 까지 맞춘 '일관된 위조') `reil_c6_profile.py check` 가 잡는지.
같은 버리는 venv 의 python 으로 실행한다 (check 가 그 venv 에서 새로 emit 해 바이트 대조하므로).

    <venv>/bin/python bms-balancing/scripts/reil_c6_mutation_proof.py <sealed_dir> <work_dir>   # work_dir 은 없는 경로 (사본 12 개)

기대: baseline (사람용 기록 둘만 더함) rc 0 · 나머지 11 변이 rc 1. 하나라도 어긋나면 rc 1.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import shutil
import sys
from pathlib import Path

import numpy as np

spec = importlib.util.spec_from_file_location("reil_c6_profile", Path(__file__).resolve().parent / "reil_c6_profile.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

src, work = Path(sys.argv[1]), Path(sys.argv[2])
work.mkdir(parents=True, exist_ok=False)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def copy(tag):
    d = work / tag
    shutil.copytree(src, d)
    return d


def reman(d, names):
    man = json.loads((d / "MANIFEST.json").read_text(encoding="utf-8"))
    for n in names:
        man[n] = sha((d / n).read_bytes())
    (d / "MANIFEST.json").write_text(p._dump(man), encoding="utf-8")


def m_baseline(d):
    (d / "README.md").write_text("사람용 기록\n", encoding="utf-8")
    (d / "C6_RUN.log").write_text("시각\n", encoding="utf-8")


def m_lock_version(d):
    f = d / "REIL_C6.lock.txt"
    t = f.read_text(encoding="utf-8")
    assert "\nnumpy==2.4.6  #" in t
    f.write_text(t.replace("\nnumpy==2.4.6  #", "\nnumpy==2.4.5  #"), encoding="utf-8")
    reman(d, ["REIL_C6.lock.txt"])


def m_lock_collision_line(d):
    f = d / "REIL_C6.lock.txt"
    t = f.read_text(encoding="utf-8")
    assert '"disk_matches": "alive-progress"' in t
    f.write_text(t.replace('"disk_matches": "alive-progress"', '"disk_matches": "about-time"'), encoding="utf-8")
    reman(d, ["REIL_C6.lock.txt"])


def m_sobol_array(d):
    f = d / "sobol_unit_seed0.npy"
    b = bytearray(f.read_bytes())
    b[-1] ^= 0x01
    f.write_bytes(bytes(b))
    a = np.load(f, allow_pickle=False)
    j = json.loads((d / "SOBOL_PHASE_A.json").read_text(encoding="utf-8"))
    j["arrays"]["unit_seed0"]["raw_float64_le_sha256"] = sha(np.ascontiguousarray(a, dtype="<f8").tobytes())
    j["arrays"]["unit_seed0"]["npy_sha256"] = sha(f.read_bytes())
    (d / "SOBOL_PHASE_A.json").write_text(p._dump(j), encoding="utf-8")
    reman(d, ["sobol_unit_seed0.npy", "SOBOL_PHASE_A.json"])


def m_sobol_seed_keyword(d):
    j = json.loads((d / "SOBOL_PHASE_A.json").read_text(encoding="utf-8"))
    j["legacy_seed_keyword"]["seed0"]["seed_keyword_same_array_as_rng"] = True
    (d / "SOBOL_PHASE_A.json").write_text(p._dump(j), encoding="utf-8")
    reman(d, ["SOBOL_PHASE_A.json"])


def m_cobyqa_description(d):
    j = json.loads((d / "COBYQA_OPTIONS.json").read_text(encoding="utf-8"))
    j["options"]["final_tr_radius"]["description"] = j["options"]["final_tr_radius"]["description"].replace("1e-6", "1e-8")
    (d / "COBYQA_OPTIONS.json").write_text(p._dump(j), encoding="utf-8")
    reman(d, ["COBYQA_OPTIONS.json"])


def m_cobyqa_impl_hash(d):
    j = json.loads((d / "COBYQA_OPTIONS.json").read_text(encoding="utf-8"))
    j["implementation_files_sha256"]["scipy/_lib/cobyqa/problem.py"] = "0" * 64
    (d / "COBYQA_OPTIONS.json").write_text(p._dump(j), encoding="utf-8")
    reman(d, ["COBYQA_OPTIONS.json"])


def m_profile_blas(d):
    j = json.loads((d / "PROFILE.json").read_text(encoding="utf-8"))
    j["build_dependencies"]["scipy"]["blas"]["version"] = "0.3.31"
    (d / "PROFILE.json").write_text(p._dump(j), encoding="utf-8")
    reman(d, ["PROFILE.json"])


def m_manifest_hash_only(d):
    man = json.loads((d / "MANIFEST.json").read_text(encoding="utf-8"))
    man["PROFILE.json"] = "f" * 64
    (d / "MANIFEST.json").write_text(p._dump(man), encoding="utf-8")


def m_manifest_entry_dropped(d):
    man = json.loads((d / "MANIFEST.json").read_text(encoding="utf-8"))
    del man["COBYQA_OPTIONS.json"]
    (d / "MANIFEST.json").write_text(p._dump(man), encoding="utf-8")


def m_file_removed(d):
    (d / "sobol_A1_A2_wide_box_seed1.npy").unlink()
    m = json.loads((d / "MANIFEST.json").read_text(encoding="utf-8"))
    del m["sobol_A1_A2_wide_box_seed1.npy"]
    (d / "MANIFEST.json").write_text(p._dump(m), encoding="utf-8")


def m_extra_file(d):
    (d / "sobol_extra.npy").write_bytes((d / "sobol_unit_seed1.npy").read_bytes())


CASES = [("baseline_plus_human_records", m_baseline, 0),
         ("lock_numpy_version", m_lock_version, 1),
         ("lock_collision_line", m_lock_collision_line, 1),
         ("sobol_array_one_bit", m_sobol_array, 1),
         ("sobol_legacy_seed_fact", m_sobol_seed_keyword, 1),
         ("cobyqa_description", m_cobyqa_description, 1),
         ("cobyqa_implementation_hash", m_cobyqa_impl_hash, 1),
         ("profile_blas_version", m_profile_blas, 1),
         ("manifest_hash_only", m_manifest_hash_only, 1),
         ("manifest_entry_dropped", m_manifest_entry_dropped, 1),
         ("file_removed_with_manifest", m_file_removed, 1),
         ("extra_file", m_extra_file, 1)]

fails = 0
for tag, fn, want in CASES:
    d = copy(tag)
    fn(d)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = p.check(d)
    lines = [ln for ln in buf.getvalue().splitlines() if ln]
    ok = rc == want
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {tag:32s} rc={rc} want={want}  | " + " · ".join(lines))
print("mutation proofs:", "ALL PASS" if not fails else f"{fails} FAIL", f"({len(CASES)} cases)")
sys.exit(1 if fails else 0)
