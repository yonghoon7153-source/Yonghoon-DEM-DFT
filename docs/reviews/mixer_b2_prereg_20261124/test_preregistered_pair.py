"""Synthetic registered endpoint and failure examples. No return archives are used."""
import copy
import runpy
import unittest
from pathlib import Path


mod = runpy.run_path(str(Path(__file__).with_name("preregistered_pair.py")))


def specimen(cluster, attached):
    steps = mod["STEPS"]
    n = 97
    data = dict(s1_se_clusters=dict(se_frac_in_clusters=cluster/n, hist_components={"1":n-cluster}),
                s2_am_se_attach=dict(se_attached_any_frac=attached/n), n={"SE":n})
    return dict(contact={"bin": dict(status="OK", bin=1, n=100, steps=steps,
                frames=[dict(step=step, **copy.deepcopy(data)) for step in steps],
                mean={"se_frac_in_clusters":cluster/n, "se_attached_any_frac":attached/n})},
                counts={"observed_by_type":{"3":n}})


def pair():
    u, c = specimen(20, 4), specimen(18, 6)
    modules = {f"source{i}.py":"c"*64 for i in range(9)}
    frames=[dict(step=s, sha256="a"*64, path=f"/sample/post/mix_{s}.liggghts")
            for s in [mod["T0"], *mod["STEPS"]]]
    e0=dict(step=1121000, sha256="d"*64)
    u.update(case="PRECAL_R1_B2_U", job="368758", frames=frames, source_sha256=modules, e0_frame=e0)
    inputs = {f["path"]:f["sha256"] for f in frames}
    inputs.update({"/sample/deck_meta.json":mod["C_META"], "/sample/in.mixer":mod["C_DECK"]})
    c.update(case_id=mod["CASE"], status="OK", provenance=dict(frames=copy.deepcopy(frames),
             binding=dict(case_id=mod["CASE"], seed=32452843, role="C"), reference_frames=[e0],
             input_sha256=inputs, module_sha256={n:dict(path=n,sha256=s) for n,s in modules.items()}))
    return u,c


class Cases(unittest.TestCase):
    def test_exact_counts_and_directions(self):
        u,c=pair()
        out=mod["paired"](u,c)
        self.assertEqual(out["se_frac_in_clusters"]["exact_fraction_delta"],"-2/97")
        self.assertEqual(out["se_attached_any_frac"]["exact_fraction_delta"],"2/97")
        self.assertTrue(all(r["predicted_direction_observed"] for r in out.values()))

    def test_zero_and_opposite_are_not_matches(self):
        u,c=pair()
        c.update(specimen(20,3))
        out=mod["paired"](u,c)
        self.assertEqual(out["se_frac_in_clusters"]["sign"], "zero")
        self.assertEqual(out["se_attached_any_frac"]["sign"], "negative")
        self.assertFalse(any(r["predicted_direction_observed"] for r in out.values()))

    def test_wrong_seed_stale_hash_wrong_window_rounded_value(self):
        for fault in ("seed","hash","steps","rounded"):
            with self.subTest(fault=fault):
                u,c=pair()
                if fault == "seed":
                    c["provenance"]["binding"]["seed"]+=1
                if fault == "hash":
                    c["provenance"]["frames"][5]["sha256"]="0"*64
                if fault == "steps":
                    c["contact"]["bin"]["frames"].reverse()
                if fault == "rounded":
                    row=c["contact"]["bin"]["frames"][0]["s2_am_se_attach"]
                    row["se_attached_any_frac"]=round(row["se_attached_any_frac"],4)
                with self.assertRaises(ValueError):
                    mod["paired"](u,c)

    def test_terminal_record_required(self):
        receipt=dict(case=mod["CASE"], role="C", release_pin=mod["C_PIN"], job_id="369734", job_end_id="369734",
                     scheduler=dict(job_id="369734",state="COMPLETED",exit_code="0:0"), runner_rc=0, return_ready=True,
                     exact_frame_names=True, frame_count=234, post_runtime_matches=True, post_runtime_error=None,
                     w9="LIVE_TERMINAL_MATCH")
        mod["receipt_fields"](receipt)
        for k,v in (("release_pin","wrong"),("return_ready",False),("w9","MISSING"),("frame_count",233)):
            with self.subTest(k=k),self.assertRaises(ValueError):
                mod["receipt_fields"](dict(receipt,**{k:v}))


if __name__ == "__main__":
    unittest.main()
